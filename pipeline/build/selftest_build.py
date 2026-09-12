#!/usr/bin/env python3
"""Positive controls for the build record and the verdict function.

The verdict is the place where a build is most tempting to round in its own
favour, so the controls are weighted at the ways it could pass something it
should not: a missing measurement read as a pass, one repeat treated as a
verdict, a win that did not survive its repeat counted as a win.

Two controls exist only to separate absences that look alike:

  null is not zero     a measured 0 tool calls must ship where a missing count
                       must not. DATA.md records a truthiness test that once
                       filed the fastest possible detection in the worst bucket.
  skipped is not unreached  a phase skipped with a reason and a phase never
                       reached read the same in a record that logs only what ran.

    python3 pipeline/build/selftest_build.py [-v]

Exit 0 = all controls behaved. 1 = a control failed.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decide as dec  # noqa: E402
import record as rec  # noqa: E402

FIXTURE = HERE.parents[1] / "pipeline" / "validate" / "fixtures" / "valid-package.json"

RESULTS: list[tuple[bool, str]] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    # str(detail), because a control that fails with a numeric detail used to
    # crash the harness while formatting its own failure message - so a caught
    # mutation reported as a suite error with zero failing checks named.
    RESULTS.append((ok, f"{label}{'  — ' + str(detail) if detail and not ok else ''}"))


def pkg_at(tmp: Path, **overrides) -> Path:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for k, v in overrides.items():
        if v is _DELETE:
            data.pop(k, None)
        else:
            data[k] = v
    p = tmp / "package.json"
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


class _Delete:
    pass


_DELETE = _Delete()


def fill_chain(root: Path) -> None:
    """Log every v1 phase as skipped, so a verdict control tests the VERDICT.

    Without this the chain gate fires first and every case comes back
    'phases missing' - correct behaviour, and useless for isolating the rule
    logic. The gate gets its own controls below instead of being worked around
    silently.
    """
    for ph in rec.load_chain()["phases"]:
        if ph["v"] > 1:
            continue
        rec.skipped(root, phase=ph["id"], function=ph["fn"],
                    reason="stubbed by the selftest to isolate the verdict logic")


def run(rows, tmp: Path, *, repair_loops: int = 0, fill: bool = True, **pkg_overrides) -> dict:
    """Open a record, file a run_paired event carrying `rows`, decide."""
    d = tmp / f"case{len(list(tmp.iterdir()))}"
    d.mkdir()
    p = pkg_at(d, **pkg_overrides)
    root = rec.open_build_record(p, builds_dir=d / "builds")
    if fill:
        fill_chain(root)
    for _ in range(repair_loops):
        rec.append(root, phase="7", function="triage_failure", triage="skill-bug")
    rec.append(root, phase="6", function="run_paired", rows=rows)
    return dec.decide(root)


def paired(test, repeat, with_ok, without_ok, **cost):
    base = {"tokens": 100, "tool_calls": 4}
    base.update(cost)
    return [
        {"test": test, "repeat": repeat, "arm": "with", "correct": with_ok,
         "tokens": base.get("with_tokens", base["tokens"]),
         "tool_calls": base.get("with_tool_calls", base["tool_calls"])},
        {"test": test, "repeat": repeat, "arm": "without", "correct": without_ok,
         "tokens": base.get("without_tokens", base["tokens"]),
         "tool_calls": base.get("without_tool_calls", base["tool_calls"])},
    ]


def two_repeats(test, with_ok, without_ok, **cost):
    return paired(test, 1, with_ok, without_ok, **cost) + paired(test, 2, with_ok, without_ok, **cost)


def with_only(test, *oks, **cost):
    return [{"test": test, "repeat": i + 1, "arm": "with", "correct": ok,
             "tokens": cost.get("tokens", 100), "tool_calls": cost.get("tool_calls", 4)}
            for i, ok in enumerate(oks)]


def run_fast(rows, tmp: Path, **pkg_overrides) -> dict:
    """Open a FAST record, file a run_paired event carrying `rows`, decide."""
    d = tmp / f"fast{len(list(tmp.iterdir()))}"
    d.mkdir()
    root = rec.open_build_record(pkg_at(d, **pkg_overrides), builds_dir=d / "builds", mode="fast")
    fill_chain(root)
    rec.append(root, phase="6", function="run_paired", rows=rows)
    return dec.decide(root)


def run_mode(rows, tmp: Path, mode: str, *, events=(), **pkg_overrides) -> dict:
    """Open a record in `mode`, stub the chain, file `events`, then run_paired, decide."""
    d = tmp / f"{mode}{len(list(tmp.iterdir()))}"
    d.mkdir()
    root = rec.open_build_record(pkg_at(d, **pkg_overrides), builds_dir=d / "builds", mode=mode)
    fill_chain(root)
    for ph, fn, fields in events:
        rec.append(root, phase=ph, function=fn, **fields)
    rec.append(root, phase="6", function="run_paired", rows=rows)
    return dec.decide(root)


def v3_mode_controls(tmp: Path) -> None:
    d = tmp / "v3mode"; d.mkdir()
    root = rec.open_build_record(pkg_at(d), builds_dir=d / "b1", mode="v3", coordinator_tier="fable")
    h = rec.header(root)
    check(h.get("mode") == "v3", "v3 is a declared mode and is written into the header", h.get("mode"))
    check(h.get("coordinator_tier") == "fable", "the coordinator tier is recorded at open, not inferred",
          h.get("coordinator_tier"))
    check(not [e for e in rec.events(root) if e.get("skipped")],
          "v3 skips NOTHING at open - every phase is still owed")
    full = rec.open_build_record(pkg_at(d), builds_dir=d / "b2")
    check(rec.header(full).get("coordinator_tier") is None,
          "an undeclared coordinator tier is None, never a default")
    ship_rows = two_repeats("T1", True, True) + two_repeats("T2", True, False)
    v_full = run_mode(ship_rows, tmp, "full")
    v_v3 = run_mode(ship_rows, tmp, "v3")
    check(v_full["verdict"] == dec.SHIP, "(the rows ship in full mode)", v_full["verdict"])
    check(v_v3["verdict"] == dec.SHIP, "the same rows SHIP in v3 - same evidence, different order",
          v_v3.get("reason"))
    # fan-out A: a class-level review finding without a re-run is not a measurement
    v = run_mode(ship_rows, tmp, "v3", events=[("5.2", "review_artifact", {"class_finding": True})])
    check(v["verdict"] == dec.UNDECIDABLE and "fan-out A" in v["reason"],
          "a class-level review finding with no rerun=true run_paired -> undecidable", v.get("reason"))
    v = run_mode(ship_rows, tmp, "v3", events=[("5.2", "review_artifact", {"class_finding": True}),
                                               ("6.1", "run_paired", {"rerun": True, "rows": []})])
    check(v["verdict"] == dec.SHIP, "the same finding followed by a rerun=true wave -> ship", v.get("reason"))
    v = run_mode(ship_rows, tmp, "v3", events=[("5.2", "review_artifact", {"class_finding": False})])
    check(v["verdict"] == dec.SHIP, "an instance-level review finding needs no rerun", v.get("reason"))
    # chain 3.1.1: three red reviews and no arm -> abandon (unconverged at review), not undecidable
    d3 = tmp / "v3cap"; d3.mkdir()
    r3 = rec.open_build_record(pkg_at(d3), builds_dir=d3 / "b", mode="v3", coordinator_tier="fable")
    fill_chain(r3)
    for _ in range(3):
        rec.append(r3, phase="5.2", function="review_artifact", class_finding=True)
    v = dec.decide(r3)
    check(v["verdict"] == dec.ABANDON and "unconverged at review" in v["reason"],
          "three class-level-red reviews with no run_paired -> abandon, unconverged at review", v.get("reason"))
    check(not rec.fanout_gate(r3), "a red review that no arm followed is not a missed revert", rec.fanout_gate(r3))
    r4 = rec.open_build_record(pkg_at(d3), builds_dir=d3 / "b2", mode="v3", coordinator_tier="fable")
    fill_chain(r4)
    for _ in range(2):
        rec.append(r4, phase="5.2", function="review_artifact", class_finding=True)
    v = dec.decide(r4)
    check(v["verdict"] != dec.ABANDON, "two red reviews are under the cap: not abandon on the cap rule", v.get("reason"))
    # 4.0.0: candidate mode - filled, checked, reviewed once, rewritten once -> candidate
    d5 = tmp / "cand"; d5.mkdir()
    r5 = rec.open_build_record(pkg_at(d5), builds_dir=d5 / "b", mode="candidate", coordinator_tier="fable")
    skipped = {e["phase"] for e in rec.events(r5) if e.get("skipped")}
    check({"6.1", "6.4", "9.1"} <= skipped, "candidate mode files its own skips at open (arms, grade, deploy)", sorted(skipped))
    fill_chain(r5)
    rec.append(r5, phase="5.1", function="validate_artifact", errors=0)
    rec.append(r5, phase="5.2", function="review_artifact", class_finding=True)
    v = dec.decide(r5)
    check(v["verdict"] == dec.ABANDON and "no rewrite" in v["reason"], "a red review with no rewrite after it is not a candidate", v.get("reason"))
    rec.append(r5, phase="5.1", function="validate_artifact", errors=0, loop=1)
    v = dec.decide(r5)
    check(v["verdict"] == dec.CANDIDATE, "red review + one rewrite + green code check -> candidate", v.get("reason"))
    check([e for e in rec.events(r5) if e.get("function") == "decide"], "decide wrote its own 8.1 event")
    r6 = rec.open_build_record(pkg_at(d5), builds_dir=d5 / "b2", mode="candidate", coordinator_tier="fable")
    fill_chain(r6); rec.append(r6, phase="5.1", function="validate_artifact", errors=2); rec.append(r6, phase="5.2", function="review_artifact", class_finding=False)
    v = dec.decide(r6)
    check(v["verdict"] == dec.ABANDON, "a red code check is never a candidate", v.get("reason"))
    # 4.0.0: promote mode ships on the same rows as full
    v = run_mode(ship_rows, tmp, "promote")
    check(v["verdict"] == dec.SHIP, "promote mode ships on measured rows", v.get("reason"))
    # 4.0.0: coordinator turns derived from run windows, never typed
    d7 = tmp / "turns"; d7.mkdir()
    r7 = rec.open_build_record(pkg_at(d7), builds_dir=d7 / "b", mode="candidate", coordinator_tier="fable")
    t0 = 1_000_000.0
    rec.cost_row(r7, phase="2.1", label="probe.T1.r1", started=t0, ended=t0 + 300, tokens=10, tool_calls=1, tier="opus")
    rec.cost_row(r7, phase="5.2", label="review.5.2.whole", started=t0 + 600, ended=t0 + 900, tokens=10, tool_calls=1, tier="opus")
    rec.cost_row(r7, phase="5.2", label="review.5.2.whole.r1", started=t0 + 9000, ended=t0 + 9300, tokens=10, tool_calls=1, tier="opus")
    rows7 = rec.derive_coordinator_turns(r7, ended=t0 + 9400)
    kinds = [r["kind"] for r in rows7]
    check(kinds == ["waiting", "derived", "waiting", "suspended", "waiting", "derived"], "derived turns: waiting/derived/suspended from windows", kinds)
    check(all(r["duration_ms"] > 0 for r in rows7), "no derived turn has a non-positive duration")
    # fan-out B: a grader that missed its planted defect must be replaced
    v = run_mode(ship_rows, tmp, "v3", events=[("6.3", "calibrate_judge", {"caught": False}),
                                               ("6.4", "grade", {})])
    check(v["verdict"] == dec.UNDECIDABLE and "fan-out B" in v["reason"],
          "calibration caught=false with no fresh_grader grade -> undecidable", v.get("reason"))
    v = run_mode(ship_rows, tmp, "v3", events=[("6.3", "calibrate_judge", {"caught": False}),
                                               ("6.4", "grade", {"fresh_grader": True})])
    check(v["verdict"] == dec.SHIP, "a fresh grader after a blind one -> ship", v.get("reason"))
    # the gate applies to every mode, so a full build cannot hide a blind grader either
    v = run_mode(ship_rows, tmp, "full", events=[("6.3", "calibrate_judge", {"caught": False})])
    check(v["verdict"] == dec.UNDECIDABLE, "the fan-out gate reads events, not the mode", v.get("reason"))
    # ship is contract-driven: fast still cannot, whatever the rows
    v = run_mode(ship_rows, tmp, "fast")
    check(v["verdict"] != dec.SHIP, "fast still never ships after the contract-driven check", v["verdict"])


def runs_paid_twice_controls(tmp: Path) -> None:
    """Probe rows count for correctness, never cost; k follows the probe."""
    def probe_rows(test, *oks):
        return [{"test": test, "repeat": i + 1, "arm": "without", "correct": ok,
                 "tokens": 999999, "tool_calls": 999} for i, ok in enumerate(oks)]
    # with x2 + one paired without (cost) + a probe without for repeat 2 -> two paired repeats
    rows = with_only("T1", True, True) + [{"test": "T1", "repeat": 1, "arm": "without",
                                            "correct": False, "tokens": 100, "tool_calls": 4}]
    ev = [("2.1", "probe_gap", {"rows": probe_rows("T1", False, False)})]
    v = run_mode(rows, tmp, "v3", events=ev)
    check(v["verdict"] == dec.SHIP,
          "a probe row stands in as the without-arm's second repeat for correctness", v.get("reason"))
    cost = [c for c in v["clauses"] if c["clause"].startswith("cost:")]
    check(all(c["verdict"] == "pass" for c in cost) and all("999" not in c["detail"] for c in cost),
          "and the probe's tokens never enter a cost clause", cost)
    v = run_mode(rows, tmp, "v3")
    check(v["verdict"] == dec.UNDECIDABLE and "repeat" in v["reason"],
          "without probe rows the same run is thin: one paired repeat", v.get("reason"))
    v = run_mode(with_only("T1", True, True), tmp, "v3", events=ev)
    check(v["verdict"] == dec.UNDECIDABLE and "cost" in v["reason"],
          "probe rows alone cannot satisfy a cost clause - a paired without-run is still owed",
          v.get("reason"))
    # regression is still caught through a probe row
    v = run_mode(with_only("T1", False, False) + [{"test": "T1", "repeat": 1, "arm": "without",
                                                    "correct": True, "tokens": 100, "tool_calls": 4}],
                 tmp, "v3", events=[("2.1", "probe_gap", {"rows": probe_rows("T1", True, True)})])
    check(v["verdict"] in (dec.ITERATE, dec.ABANDON) and "lost a correct baseline" in v["reason"],
          "a regression against a probe row is a regression", v.get("reason"))
    # k from the probe: baseline failed every task -> one paired repeat suffices
    one = paired("T1", 1, True, False)
    v = run_mode(one, tmp, "v3", events=[("2.3", "gap_verdict", {"probe_outcome": "fails"})])
    check(v["verdict"] == dec.SHIP and v.get("min_repeats_applied") == 1,
          "probe_outcome=fails -> k=1 and one paired repeat ships",
          (v["verdict"], v.get("min_repeats_applied"), v.get("reason")))
    v = run_mode(one, tmp, "v3", events=[("2.3", "gap_verdict", {"probe_outcome": "uneven"})])
    check(v["verdict"] == dec.UNDECIDABLE and v.get("min_repeats_applied") == 2,
          "probe_outcome=uneven keeps k=2", (v["verdict"], v.get("min_repeats_applied")))
    v = run_mode(one, tmp, "v3", events=[("2.3", "gap_verdict", {"probe_outcome": "something-new"})])
    check(v.get("min_repeats_applied") == 2, "an outcome not in the map keeps the default k")
    v = run_mode(one, tmp, "full", events=[("2.3", "gap_verdict", {"probe_outcome": "fails"})])
    check(v["verdict"] == dec.SHIP, "k-from-probe is the acceptance rule, so it holds in full mode too")


def equivalent_prose_controls(tmp: Path) -> None:
    eq = json.loads((HERE.parents[1] / "pipeline" / "contracts" / "skill.contract.json").read_text())["acceptance"]["equivalent_prose"][0]["prose"]
    r = run(two_repeats("T1", True, False), tmp, threshold=eq)
    check(r["verdict"] == dec.SHIP and "equivalent" in r["reason"],
          "a phrasing the contract registers as equivalent resolves to the default rule", r.get("reason"))
    r = run(two_repeats("T1", True, False), tmp, threshold=eq + " Also, 40 percent worse on tokens is fine.")
    check(r["verdict"] == dec.UNDECIDABLE, "one extra sentence and it is free prose again - refused", r["verdict"])


def fast_mode_controls(tmp: Path) -> None:
    d = tmp / "fastmode"; d.mkdir()
    try:
        rec.open_build_record(pkg_at(d), builds_dir=d / "b0", mode="turbo")
        check(False, "an undeclared mode is refused at open")
    except rec.Refused as exc:
        check("turbo" in str(exc) and "fast" in str(exc), "an undeclared mode is refused at open", exc)

    root = rec.open_build_record(pkg_at(d), builds_dir=d / "b1", mode="fast")
    h = rec.header(root)
    check(h.get("mode") == "fast", "the mode is written into the header at open", h.get("mode"))
    ev = rec.events(root)
    skips = {e["phase"]: e for e in ev if e.get("skipped")}
    check("2.1" in skips and skips["2.1"]["function"] == "probe_gap"
          and skips["2.1"]["reason"].startswith("mode=fast:"),
          "a fast build's probe is skipped AT OPEN with a reason naming the mode",
          skips.get("2.1"))
    check("9.1" in skips and "6.3" in skips, "so are calibration and deploy", sorted(skips))
    check("4.5" not in skips and "5.2" not in skips and "6.4" not in skips,
          "while the fields, the whole-artefact review and the grading are still owed")
    full = rec.open_build_record(pkg_at(d), builds_dir=d / "b2")
    check(rec.header(full).get("mode") == "full"
          and not [e for e in rec.events(full) if e.get("skipped")],
          "the default mode is full and skips nothing at open")

    v = run_fast(with_only("T1", True, True) + with_only("T2", True, True), tmp)
    check(v["verdict"] == dec.FAST_PASS and v.get("mode") == "fast",
          "with-arm only, all correct, two repeats -> fast_pass", v)
    check("not ship" in v["reason"].lower() or "Not ship" in v["reason"],
          "and the reason says in words that fast_pass is not ship", v["reason"])
    v = run_fast(with_only("T1", True, False), tmp)
    check(v["verdict"] == dec.ITERATE, "one wrong with-arm run -> iterate", v["verdict"])
    v = run_fast(with_only("T1", True), tmp)
    check(v["verdict"] == dec.UNDECIDABLE, "one repeat never earns fast_pass either", v["verdict"])
    v = run_fast(with_only("T1", True, None), tmp)
    check(v["verdict"] == dec.UNDECIDABLE, "unrecorded correctness is not a pass in fast mode",
          v["verdict"])
    # THE CEILING: rows that would SHIP in full mode do not ship in fast mode.
    rows = two_repeats("T1", True, False) + two_repeats("T2", True, True)
    full_v = run(rows, tmp)
    fast_v = run_fast(rows, tmp)
    check(full_v["verdict"] == dec.SHIP, "(the same rows ship in full mode)", full_v["verdict"])
    check(fast_v["verdict"] == dec.FAST_PASS and fast_v["verdict"] != dec.SHIP,
          "a fast build never ships, even carrying a without-arm that it beat", fast_v["verdict"])
    v = run_fast([], tmp)
    check(v["verdict"] == dec.UNDECIDABLE, "no with-arm rows at all -> undecidable", v["verdict"])


# --- the record --------------------------------------------------------------

def record_controls(tmp: Path) -> None:
    d = tmp / "rec"; d.mkdir()

    # a refused package opens no record
    bad = pkg_at(d, claims=[{"claim": "no quote here", "source_id": "S1",
                             "locator": "x", "verdict": "REPEATED"}])
    try:
        rec.open_build_record(bad, builds_dir=d / "b")
        check(False, "a refused package opens no record", "it opened one")
    except rec.Refused as exc:
        check("pkg.claims.quote" in str(exc), "a refused package opens no record", str(exc))
    check(not (d / "b" / "migration-review").exists(),
          "a refused package leaves no directory behind")

    # discipline is refused at 0.2 as well as at 0.1
    disc = pkg_at(d, failure_kind="discipline")
    try:
        rec.open_build_record(disc, builds_dir=d / "b2")
        check(False, "failure_kind discipline opens no record", "it opened one")
    except rec.Refused:
        check(True, "failure_kind discipline opens no record")

    root = rec.open_build_record(pkg_at(d), builds_dir=d / "b3")
    head_before = rec.header(root)

    # append-only: the header is not rewritten, earlier events are not edited
    rec.append(root, phase="2", function="probe_gap", out="3 runs")
    first = rec.events(root)[0]
    rec.append(root, phase="2", function="code_failures", out="2 failures")
    check(rec.header(root) == head_before, "record.json is written once, never rewritten")
    check(rec.events(root)[0] == first, "an earlier event is never edited by a later one")
    check([e["function"] for e in rec.events(root)][-2:] == ["probe_gap", "code_failures"],
          "events are appended in order")

    # a skip needs a reason
    try:
        rec.skipped(root, phase="3", function="gather", reason="  ")
        check(False, "a skip with no reason is refused", "it was accepted")
    except rec.Refused:
        check(True, "a skip with no reason is refused")

    rec.skipped(root, phase="3", function="gather", reason="the seed covers every observed failure")
    ev = rec.events(root)
    skipped_fns = {e["function"] for e in ev if e.get("skipped")}
    ran_fns = {e["function"] for e in ev if not e.get("skipped")}
    check("gather" in skipped_fns and "gather" not in ran_fns,
          "a skipped phase is distinguishable from one that ran")
    check("verify_claims" not in skipped_fns | ran_fns,
          "a phase never reached leaves no row, so it cannot be read as a skip")

    # ledgers
    ledgers = d / "ledgers"
    rec.field_row(root, field="description", red_code=["desc.max"], red_agent=[],
                  rewrites=2, ledgers_dir=ledgers)
    rec.not_checked(root, what="trigger firing", why="phase 6.5 is v2")
    row = rec.build_row(root, verdict="ship", reason="all clauses hold", ledgers_dir=ledgers)
    fields = [json.loads(l) for l in (ledgers / "fields.jsonl").read_text().splitlines() if l.strip()]
    check(len(fields) == 1 and fields[0]["field"] == "description" and fields[0]["rewrites"] == 2,
          "a field row lands in fields.jsonl")
    check(row["not_checked"] == [{"what": "trigger firing", "why": "phase 6.5 is v2"}],
          "what was not checked is carried into the build row")
    check(row["phases_skipped"] and row["phases_skipped"][0]["reason"].startswith("the seed"),
          "a skip and its reason reach the build row")
    builds = [json.loads(l) for l in (ledgers / "builds.jsonl").read_text().splitlines() if l.strip()]
    check(len(builds) == 1 and builds[0]["verdict"] == "ship", "a build row lands in builds.jsonl")

    # a build id is used once
    try:
        rec.open_build_record(pkg_at(d), builds_dir=d / "b3")
        check(False, "a build id cannot be reused", "a second record opened over the first")
    except rec.Refused:
        check(True, "a build id cannot be reused")


# --- the verdict -------------------------------------------------------------

def decide_controls(tmp: Path) -> None:
    d = tmp / "dec"; d.mkdir()

    r = run(two_repeats("t1", True, False) + two_repeats("t2", True, True), d)
    check(r["verdict"] == dec.SHIP, "a surviving win with equal cost ships", r["reason"])

    r = run(paired("t1", 1, True, False), d)
    check(r["verdict"] == dec.UNDECIDABLE, "one repeat never decides", r["reason"])

    r = run(two_repeats("t1", True, False) + two_repeats("t2", False, True), d)
    check(r["verdict"] == dec.ITERATE and any(c["clause"] == "no_regression" and c["verdict"] == "fail"
                                              for c in r["clauses"]),
          "losing a correct baseline is a regression", r["reason"])

    r = run(two_repeats("t1", True, False, with_tokens=140, without_tokens=100), d)
    check(r["verdict"] == dec.ITERATE and any(c["clause"] == "cost:tokens" and c["verdict"] == "fail"
                                              for c in r["clauses"]),
          "40 percent more tokens breaks the cost clause", r["reason"])

    r = run(two_repeats("t1", True, False, with_tokens=119, without_tokens=100), d)
    check(r["verdict"] == dec.SHIP, "19 percent more tokens is inside tolerance", r["reason"])

    rows = two_repeats("t1", True, False)
    rows[0]["tokens"] = None
    r = run(rows, d)
    check(r["verdict"] == dec.UNDECIDABLE and any(c["clause"] == "cost:tokens"
                                                  and c["verdict"] == "indeterminate"
                                                  for c in r["clauses"]),
          "a missing token count is not a pass", r["reason"])

    r = run(two_repeats("t1", True, True, with_tool_calls=0, without_tool_calls=0), d)
    check(r["verdict"] == dec.ITERATE and any(c["clause"] == "win" and c["verdict"] == "fail"
                                              for c in r["clauses"])
          and all(c["verdict"] != "indeterminate" for c in r["clauses"]),
          "a measured zero is a result, not a missing measurement", r["reason"])

    r = run(two_repeats("t1", True, True) + two_repeats("t2", True, True), d)
    check(r["verdict"] == dec.ITERATE and any(c["clause"] == "win" for c in r["clauses"]),
          "no win means no ship, however clean the run", r["reason"])

    r = run(paired("t1", 1, True, False) + paired("t1", 2, True, True), d)
    fragile = [c for c in r["clauses"] if c["clause"] == "win"]
    check(r["verdict"] == dec.ITERATE and fragile and "survive" in fragile[0]["detail"],
          "a win that did not survive the repeat is not a win", r["reason"])

    rows = two_repeats("t1", True, False)
    rows[0]["correct"] = None
    r = run(rows, d)
    check(r["verdict"] == dec.UNDECIDABLE, "an unrecorded correctness is not a pass", r["reason"])

    r = run(two_repeats("t1", True, True), d, repair_loops=3)
    check(r["verdict"] == dec.ABANDON, "iterate becomes abandon at the repair cap", r["reason"])

    # --- cost measurement ---------------------------------------------------
    import time
    d3 = d / "cost"; d3.mkdir()
    root = rec.open_build_record(pkg_at(d3), builds_dir=d3 / "b")
    t = time.time()
    rec.cost_row(root, phase="6.1", label="with-r1", started=t, ended=t + 1.5,
                 tokens=1000, tool_calls=2, tier="claude-opus-5")
    check(not rec.cost_gate(root), "a run logged with duration, window and tier satisfies the gate")
    r_t = json.loads((root / "cost" / "measured.jsonl").read_text().splitlines()[0])
    check(r_t.get("tier") == "claude-opus-5",
          "the model tier is stored, so the routing rule can actually be obeyed",
          r_t.get("tier"))
    r0 = json.loads((root / "cost" / "measured.jsonl").read_text().splitlines()[0])
    check(r0["duration_ms"] == 1500, "the duration is recorded in milliseconds, from the wall clock")
    check(r0.get("started") and r0.get("ended") and r0["started"] < r0["ended"],
          "the run's WINDOW is stored, not only its length — ts is the row's write time, "
          "and batched writes make every ts identical",
          f"started={r0.get('started')} ended={r0.get('ended')}")

    with (root / "cost" / "measured.jsonl").open("a") as fh:
        fh.write(json.dumps({"phase": "6.1", "label": "without-r1", "tokens": 900}) + "\n")
    g = rec.cost_gate(root)
    check(len(g) == 1 and g[0].startswith("without-r1") and "no duration" in g[0],
          "a run logged WITHOUT a duration is named by the cost gate, with the reason",
          str(g))

    # A duration WITHOUT a run window used to satisfy this gate. It returned
    # clean for a build where 16 of 36 runs had no window, so the build could
    # say how long each run took and not whether any two overlapped - and a
    # dispatch cap can only be judged on whether it was used.
    with (root / "cost" / "measured.jsonl").open("a") as fh:
        fh.write(json.dumps({"phase": "6.1", "label": "no-window-r1",
                             "duration_ms": 1200, "tokens": 900}) + "\n")
    g = rec.cost_gate(root)
    check(any(x.startswith("no-window-r1") for x in g),
          "a duration with no run window is caught, because concurrency needs the window",
          str(g))
    check(any("concurrency" in x for x in g),
          "and the gate says why the window matters, not just that it is missing",
          str(g))

    # The chain contract's routing rule says the tier is recorded per run. Until
    # cost_row took the argument, that rule could not be obeyed by any caller.
    with (root / "cost" / "measured.jsonl").open("a") as fh:
        fh.write(json.dumps({"phase": "6.1", "label": "no-tier-r1", "duration_ms": 1200,
                             "started": "2026-09-02T00:00:00+00:00",
                             "ended": "2026-09-02T00:00:01+00:00", "tokens": 900}) + "\n")
    g = rec.cost_gate(root)
    check(any(x.startswith("no-tier-r1") and "tier" in x for x in g),
          "a run with no model tier is caught, because routing cannot be audited without it",
          str(g))

    # The convergence cap, held by code rather than by the contract text alone.
    d4 = d / "rounds"; d4.mkdir()
    root4 = rec.open_build_record(pkg_at(d4), builds_dir=d4 / "b")
    for lab in ("read.4.1.refs", "read.4.1.refs.r2", "read.4.1.refs.r3",
                "read.4.3.name", "read.4.3.name.r2"):
        rec.cost_row(root4, phase="4", label=lab, started=t, ended=t + 1,
                     tokens=10, tool_calls=1, tier="claude-opus-5")
    check(not rec.round_gate(root4), "three rounds on a field is inside the cap",
          str(rec.round_gate(root4)))
    rec.cost_row(root4, phase="4", label="read.4.1.refs.r4", started=t, ended=t + 1,
                 tokens=10, tool_calls=1, tier="claude-opus-5")
    g4 = rec.round_gate(root4)
    check(len(g4) == 1 and g4[0].startswith("4.1.refs"),
          "a fourth round is named, and only the field that overran", str(g4))
    check(bool(g4) and "cap is 3" in g4[0],
          "and the gate says what the cap was", str(g4))

    # A protected run that silently changed tier breaks comparison with every
    # earlier build, which is the cost the routing rule exists to prevent.
    rec.cost_row(root4, phase="6.1", label="arm.with.r1", started=t, ended=t + 1,
                 tokens=10, tool_calls=1, tier="claude-opus-5")
    check(not rec.routing_gate(root4, ("arm.",)), "protected runs on one tier pass")
    rec.cost_row(root4, phase="6.1", label="arm.with.r2", started=t, ended=t + 1,
                 tokens=10, tool_calls=1, tier="claude-haiku-4-5")
    check(any("more than one tier" in x for x in rec.routing_gate(root4, ("arm.",))),
          "a protected run on a second tier is caught",
          str(rec.routing_gate(root4, ("arm.",))))

    # --- the opener must satisfy the gate it is opening a record for --------
    # It logged one row at phase "0", which matches neither 0.1 nor 0.2, so
    # chain_gate reported 0.1 absent on EVERY build using this opener and
    # decide.py returned UNDECIDABLE until someone logged it by hand.
    d0 = d / "opener"; d0.mkdir()
    root0 = rec.open_build_record(pkg_at(d0), builds_dir=d0 / "b")
    opened = [e["phase"] for e in rec.events(root0)]
    # NOTE the argument order: this suite is check(ok, label, detail) while
    # selftest_preflight.py is check(label, got, want). Same name, opposite
    # order, one repo. Writing the label first here passes the label as the
    # condition, and a non-empty string is truthy, so every such control
    # reports a pass without comparing anything. That happened twice in one
    # session before it was noticed - once in the triggers suite and once here.
    check("0.1" in opened, "0.1 is logged, because admission actually ran", str(opened))
    check("0.2" in opened, "0.2 is logged separately from it", str(opened))
    check("0" not in opened, "nothing is filed under the unmatched phase 0", str(opened))
    zero = [g for g in rec.chain_gate(root0) if str(g.get("id", "")).startswith("0.")]
    check(not zero, "the chain gate finds no phase 0 silence", str(zero))

    # --- the coordinator's own time -----------------------------------------
    d5 = d / "coord"; d5.mkdir()
    root5 = rec.open_build_record(pkg_at(d5), builds_dir=d5 / "b")
    base = t
    rec.cost_row(root5, phase="4.5", label="read.4.5.steps", started=base, ended=base + 100,
                 tokens=10, tool_calls=1, tier="claude-opus-5")
    tl = rec.timeline(root5)
    check(tl["coordinator_elapsed_s"] == 0, "no coordinator rows means zero coordinator time")
    check(tl["waste_s"] == 0, "and no waste is CLAIMED when nothing was recorded as waiting")
    g = rec.coordinator_gate(root5)
    check(any("no coordinator ledger" in x for x in g),
          "the gate says the gaps are unattributable rather than assuming they were idle",
          str(g))

    # A gap that nobody wrote down must be reported as unaccounted, not folded
    # into idle or into work: an unrecorded turn and an idle minute look the
    # same from outside and only one of them is a problem.
    rec.cost_row(root5, phase="4.6", label="read.4.6.pointers", started=base + 200,
                 ended=base + 260, tokens=10, tool_calls=1, tier="claude-opus-5")
    tl = rec.timeline(root5)
    check(round(tl["unaccounted_s"]) == 100,
          "the 100s gap between two runs is unaccounted", tl["unaccounted_s"])
    check(tl["waste_s"] == 0, "and is still not called waste", tl["waste_s"])

    rec.coordinator_turn(root5, kind="authoring", started=base + 100, ended=base + 160,
                         note="wrote the pointers field")
    rec.coordinator_turn(root5, kind="waiting", started=base + 160, ended=base + 200,
                         note="nothing left to dispatch")
    tl = rec.timeline(root5)
    check(round(tl["unaccounted_s"]) == 0, "labelling the gap accounts for it",
          tl["unaccounted_s"])
    check(round(tl["waste_s"]) == 40, "and only the waiting part counts as waste",
          tl["waste_s"])
    check(tl["coordinator_by_kind_s"].get("authoring") == 60,
          "authoring is recorded as work, not as waste",
          tl["coordinator_by_kind_s"])

    # An unknown kind is refused: an unlabelled turn is the thing being fixed.
    try:
        rec.coordinator_turn(root5, kind="dunno", started=base, ended=base + 1)
        check(False, "an unknown turn kind is refused")
    except rec.Refused:
        check(True, "an unknown turn kind is refused")

    # Overlapping dispatched runs are counted once, or concurrency would inflate
    # the elapsed figure and hide the gaps.
    d6 = d / "overlap"; d6.mkdir()
    root6 = rec.open_build_record(pkg_at(d6), builds_dir=d6 / "b")
    for lab in ("a", "b"):
        rec.cost_row(root6, phase="6.1", label=lab, started=base, ended=base + 100,
                     tokens=1, tool_calls=1, tier="claude-opus-5")
    check(rec.timeline(root6)["dispatched_elapsed_s"] == 100,
          "two runs in the same window are 100s elapsed, not 200",
          rec.timeline(root6)["dispatched_elapsed_s"])

    rec.cost_row(root, phase="6.1", label="zero-tools", started=t, ended=t,
                 tokens=None, tool_calls=0)
    rows = [json.loads(l) for l in (root / "cost" / "measured.jsonl").read_text().splitlines() if l.strip()]
    z = next(r for r in rows if r.get("label") == "zero-tools")
    check(z["tokens"] is None and z["tool_calls"] == 0 and z["duration_ms"] == 0,
          "null for not-reported and 0 for a measured zero, kept apart in the same row")

    # --- the chain gate -----------------------------------------------------
    # A phase that left no event is not a phase that went well. This is the
    # defect that created the gate: in the chain's first real run coverage_check
    # left no trace at all, and a clean-looking verdict was computed anyway.
    r = run(two_repeats("t1", True, False), d, fill=False)
    check(r["verdict"] == dec.UNDECIDABLE and r.get("missing_phases"),
          "a chain with phases that left NO event cannot produce a verdict", r["reason"])
    check("3.1" in (r.get("missing_phases") or []),
          "the missing-phase list names coverage_check, the phase this gate exists for")

    # a skip is allowed and is not an absence
    d2 = d / "gate"; d2.mkdir()
    root = rec.open_build_record(pkg_at(d2), builds_dir=d2 / "b")
    fill_chain(root)
    check(not rec.chain_gate(root, 1), "a phase skipped WITH A REASON satisfies the gate")

    # ...but a skip with no reason is refused at the source
    try:
        rec.skipped(root, phase="9.9", function="x", reason="")
        check(False, "the gate cannot be satisfied by a reasonless skip", "it was accepted")
    except rec.Refused:
        check(True, "the gate cannot be satisfied by a reasonless skip")

    # v2 phases are not required at version 1
    chain = rec.load_chain()
    v2 = [p["fn"] for p in chain["phases"] if p["v"] == 2]
    check(all(f not in {m["fn"] for m in rec.chain_gate(root, 1)} for f in v2),
          "v2 phases are not demanded of a v1 run")
    missing_v2 = {m["fn"] for m in rec.chain_gate(root, 2)}
    if v2:
        check(missing_v2 and missing_v2 <= set(v2),
              "asking for v2 DOES demand them, and demands nothing else",
              f"missing at v2: {sorted(missing_v2)}")
    else:
        # Every declared phase now has code or a gate, so the contract has no v2
        # rows left. Assert that rather than skipping: a control that quietly
        # stops checking anything is worse than one that fails.
        check(not missing_v2,
              "with no v2 phases declared, asking for v2 demands nothing extra",
              f"unexpectedly missing: {sorted(missing_v2)}")
        check(all(ph["v"] == 1 for ph in chain["phases"]),
              "every declared phase is v1 — each one has code or a gate behind it")

    r = run(two_repeats("t1", True, False), d,
            threshold="Ship it if it feels better than before.")
    check(r["verdict"] == dec.UNDECIDABLE and "no code can evaluate it" in r["reason"],
          "a prose threshold no code can evaluate is refused, not guessed", r["reason"])

    r = run(two_repeats("t1", True, True), d,
            threshold="Ship it if it feels better than before.",
            threshold_rule={"require_win": False})
    check(r["verdict"] == dec.SHIP and r["rule"]["require_win"] is False,
          "a structured threshold_rule overrides the prose", r["reason"])

    r = run([], d)
    check(r["verdict"] == dec.UNDECIDABLE, "no measurement decides nothing", r["reason"])

    # --- the shape axis -----------------------------------------------------
    # The case the contract's probe_never_gates clause exists for: every test
    # correct in both arms, and the skill earned its place on output shape alone.
    # Scored on correctness only this is a tie and the skill is thrown away.
    rows = two_repeats("t1", True, True) + two_repeats("t2", True, True)
    for x in rows:
        x["shape_ok"] = x["arm"] == "with"
    r = run(rows, d)
    check(r["verdict"] == dec.SHIP and any(c["clause"] == "win" and "shape" in c["detail"]
                                           for c in r["clauses"]),
          "20-of-20 versus 20-of-20 still ships when the skill wins on SHAPE", r["reason"])

    rows = two_repeats("t1", True, True)
    for x in rows:
        x["shape_ok"] = x["arm"] == "with"
    rows[2]["shape_ok"] = False          # the with-arm loses shape in repeat 2
    r = run(rows, d)
    check(r["verdict"] == dec.ITERATE,
          "a shape win that did not survive the repeat is not a win", r["reason"])

    rows = two_repeats("t1", True, True)
    for x in rows:
        x["shape_ok"] = True if x["arm"] == "with" else None   # baseline shape unrecorded
    r = run(rows, d)
    check(r["verdict"] == dec.ITERATE,
          "an unrecorded baseline shape is not a shape win", r["reason"])

    rows = two_repeats("t1", True, False)
    for x in rows:
        x["shape_ok"] = x["arm"] == "without"    # skill wins correctness, loses shape
    r = run(rows, d)
    check(r["verdict"] == dec.SHIP and any(c["clause"] == "win" and "correctness" in c["detail"]
                                           for c in r["clauses"]),
          "a correctness win still counts when the shape axis goes the other way", r["reason"])


def main() -> int:
    verbose = "-v" in sys.argv
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        record_controls(tmp)
        decide_controls(tmp)
        fast_mode_controls(tmp)
        v3_mode_controls(tmp)
        runs_paid_twice_controls(tmp)
        equivalent_prose_controls(tmp)
    bad = [m for ok, m in RESULTS if not ok]
    for ok, m in RESULTS:
        if verbose or not ok:
            print(f"{'ok   ' if ok else 'FAIL '} {m}")
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} controls behaved")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
