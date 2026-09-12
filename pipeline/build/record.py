#!/usr/bin/env python3
"""The build record — phase 0.2, and the spine every later phase appends to.

One directory per build. Two files, and the split between them is the point:

  record.json   the header, written once at open and never rewritten
  events.jsonl  append-only, one row per function that ran

A phase cannot quietly revise what an earlier phase found. If 4.5 disagrees with
what 2.2 observed, both rows are in the file and the disagreement is visible; a
mutable record would have shown only the last writer.

The record is opened ONLY for an admitted package. `open_build_record` runs the
admission gate itself rather than trusting a caller's word that it passed — a
build record for a refused package is a record of something that should not have
started.

Three things are recorded that a successful run has no natural reason to write
down, and each exists because its absence is unrecoverable later:

  skipped   a phase that did not run, WITH its reason. Phase 3 skipped because
            the seed covered the gap, and phase 3 never reached, look identical
            in a record that only logs what happened.
  not_checked  what this build did not establish. A build record that lists only
            what was verified reads as though everything else was fine.
  null vs 0 a measured zero is not the same as not-measured. DATA.md: a
            truthiness test once filed the fastest possible detection in the
            worst bucket.

    python3 pipeline/build/record.py open <package.json> [--builds-dir DIR]
    python3 pipeline/build/record.py show <build-dir>

Exit 0 = done. 1 = refused or malformed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validate"))
import package_contract as pkgc  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
BUILDS = REPO / "pipeline" / "builds"
LEDGERS = REPO / "pipeline" / "ledgers"

RECORD = "record.json"
EVENTS = "events.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


class Refused(Exception):
    """The package did not pass admission. No record is opened."""


# --- opening -----------------------------------------------------------------

def open_build_record(package_path: Path, builds_dir: Path | None = None,
                      mode: str = "full", coordinator_tier: str | None = None) -> Path:
    """Phase 0.2. Admits the package first; a refusal raises rather than returns.

    `mode` is one of the chain contract's modes. It is written into the header
    at open because it decides which phases are owed and which verdicts are
    reachable, and a finished build cannot be asked what it was opened as.
    """
    package_path = Path(package_path)
    pkg = json.loads(package_path.read_text(encoding="utf-8"))
    contract = pkgc.load_contract()
    modes = {k: v for k, v in (load_chain().get("modes") or {}).items() if isinstance(v, dict)
             and "skips" in v}
    if mode not in modes:
        raise Refused(f"mode {mode!r} is not declared in the chain contract "
                      f"(declared: {', '.join(sorted(modes))})")

    missing = pkgc.coverage_gate(contract)
    if missing:
        raise Refused(f"the admission engine does not implement: {', '.join(missing)}")

    rows = pkgc.admit(pkg, contract)
    errs = [r for r in rows if r["verdict"] == pkgc.FAIL and r["severity"] == "error"]
    if errs:
        detail = "; ".join(f"{r['id']}: {r['detail']}" for r in errs[:4])
        raise Refused(f"{len(errs)} admission error(s) — {detail}")

    build_id = pkg["id"]
    root = Path(builds_dir or BUILDS) / build_id
    if root.exists():
        raise Refused(f"{root} already exists — a build id is used once, so its record "
                      f"cannot be overwritten by a rerun")
    root.mkdir(parents=True)

    warns = [r["id"] for r in rows if r["verdict"] == pkgc.FAIL and r["severity"] == "warn"]
    indet = [r["id"] for r in rows if r["verdict"] == pkgc.INDET]

    header = {
        "id": build_id,
        "opened": now(),
        "mode": mode,
        # The model the COORDINATOR ran on, declared at open. Recorded, never
        # inferred: a finished build cannot be asked what wrote it, and v3's bet
        # is a stronger writer in fewer turns - a bet nobody can settle without
        # this field. None when not declared; None is not a tier.
        "coordinator_tier": coordinator_tier,
        "package": {
            "path": str(package_path),
            "sha256": sha256(package_path),
            "candidate_sentence": pkg.get("candidate_sentence"),
            "content_kind": pkg.get("content_kind"),
            "verifiable": pkg.get("verifiable"),
            "failure_kind": pkg.get("failure_kind"),
            "threshold": pkg.get("threshold"),
            "threshold_rule": pkg.get("threshold_rule"),
            "budget": pkg.get("budget"),
            # Recorded at open, because these are properties of the INPUT and a
            # finished build cannot be asked what it started from.
            "origin": pkg.get("origin"),
            "filled_by": pkg.get("filled_by"),
            "gap_kind": pkg.get("gap_kind"),
            "n_claims": len(pkg.get("claims") or []),
            "n_measured_claims": sum(1 for c in (pkg.get("claims") or [])
                                     if isinstance(c, dict) and c.get("verdict") == "MEASURED"),
            "n_sources": len(pkg.get("sources") or []),
        },
        "admission": {
            "package_contract_version": contract["contract_version"],
            "errors": 0,
            "warnings": warns,
            "indeterminate": indet,
        },
        "note": "record.json is written once. Everything that happened is in events.jsonl.",
    }
    (root / RECORD).write_text(json.dumps(header, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    (root / EVENTS).write_text("", encoding="utf-8")
    # TWO events, because the contract declares two phases and this function
    # performs both. It used to log a single row at phase "0", which matches
    # neither 0.1 nor 0.2, so chain_gate reported phase 0.1 absent on EVERY
    # build that used this opener and decide.py returned UNDECIDABLE until
    # someone logged it by hand. The admission genuinely ran - pkgc.admit is
    # called above and a refusal raises - so the row was owed and missing, not
    # merely mislabelled. Found by a build that thought it was complete.
    append(root, phase="0.1", function="admit_package",
           out=f"admitted against package contract {contract['contract_version']}",
           warnings=warns, indeterminate=indet)
    append(root, phase="0.2", function="open_build_record",
           out=f"record opened at {root}", mode=mode)
    # A mode that skips phases skips them HERE, mechanically, each with a skip
    # event naming the mode and the contract's reason. The chain principle is
    # that a phase may be skipped with a reason but never be absent; a mode is
    # that reason declared once in the contract instead of fourteen times by
    # hand, where one of the fourteen would eventually be forgotten.
    fn_of = {ph["id"]: ph["fn"] for ph in load_chain()["phases"]}
    for pid, why in (modes[mode].get("skips") or {}).items():
        skipped(root, phase=pid, function=fn_of[pid], reason=f"mode={mode}: {why}")
    return root


# --- appending ---------------------------------------------------------------

def append(root: Path, *, phase: str, function: str, **fields) -> dict:
    """One event. Append-only: an earlier row is never edited."""
    root = Path(root)
    if not (root / RECORD).is_file():
        raise Refused(f"{root} is not a build record")
    row = {"ts": now(), "phase": str(phase), "function": function}
    row.update(fields)
    with (root / EVENTS).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def skipped(root: Path, *, phase: str, function: str, reason: str) -> dict:
    """A phase that did not run, and why.

    Required, not optional. 'Skipped because the seed covered the gap' and
    'never reached' are the same absence in a record that logs only what ran.
    """
    if not reason or not reason.strip():
        raise Refused("a skip needs a reason — an unexplained skip is indistinguishable "
                      "from a phase that was never reached")
    return append(root, phase=phase, function=function, skipped=True, reason=reason)


def not_checked(root: Path, *, what: str, why: str) -> dict:
    """Something this build did not establish."""
    return append(root, phase="record", function="not_checked", what=what, why=why)


def events(root: Path) -> list[dict]:
    txt = (Path(root) / EVENTS).read_text(encoding="utf-8")
    return [json.loads(l) for l in txt.splitlines() if l.strip()]


def header(root: Path) -> dict:
    return json.loads((Path(root) / RECORD).read_text(encoding="utf-8"))


def last(root: Path, function: str) -> dict | None:
    hits = [e for e in events(root) if e["function"] == function and not e.get("skipped")]
    return hits[-1] if hits else None


# --- cost, measured -----------------------------------------------------------

def dt_iso(epoch: float) -> str:
    """A wall-clock instant, so a run's window survives a batched write."""
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat(timespec="seconds")


def cost_row(root: Path, *, phase: str, label: str, started: float, ended: float,
             tokens: int | None = None, tool_calls: int | None = None,
             tier: str | None = None, note: str | None = None,
             extra: dict | None = None) -> dict:
    """One row per dispatched run. Duration is REQUIRED, not optional.

    extra: named facts about the run that a later query keys on - cached (a
    memoised replay, never a measurement of load), effort, warm. Written as
    given; a fact not given is absent, never defaulted.

    In the first agent-run of this chain, 12 of 18 dispatched runs logged tokens
    and no duration, so two thirds of the run was invisible to anyone trying to
    make it faster. You cannot cut what you cannot see, and the same rule that
    keeps spend_measured null applies here: a measurement that was available and
    not taken is a measurement lost, because the run is over.

    started/ended are wall-clock seconds (time.time()). Pass tokens as None when
    the harness did not report them - never 0, which is a measured zero.

    tier is the model the run was dispatched to. The chain contract's routing
    rule says the tier is recorded per run alongside its result, and until this
    argument existed that rule could not be obeyed by any caller - a rule the
    code made impossible to follow. It is also what makes a cheaper-tier saving
    auditable after the fact: a run whose tier is unknown cannot be shown to
    have kept the tier its measurement required.
    """
    # started and ended are stored, not just the duration. ts is when the ROW was
    # written, and rows get written in batches - so twelve runs can carry one
    # identical ts and the real windows are gone. Without the window, the one
    # question the log exists to answer, "did these run at the same time", cannot
    # be asked. Found 2026-09-01 when an overlap analysis over ts produced
    # nonsense: twelve runs apparently ending on the same second.
    row = {"ts": now(), "phase": str(phase), "label": label,
           "started": dt_iso(started), "ended": dt_iso(ended),
           "duration_ms": int(round((ended - started) * 1000)),
           "tokens": tokens, "tool_calls": tool_calls}
    if tier:
        row["tier"] = tier
    if note:
        row["note"] = note
    for k, v in (extra or {}).items():
        row[k] = v
    d = Path(root) / "cost"
    d.mkdir(parents=True, exist_ok=True)
    with (d / "measured.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def cost_gate(root: Path) -> list[str]:
    """Dispatched runs whose duration OR run window was never recorded.

    Reported per build, so the gap is visible while the run is still fresh
    rather than discovered when someone later asks where the time went.

    The window matters as much as the duration and used not to be checked. On
    2026-09-01 this gate returned empty for a build in which 16 of 36 runs
    carried a duration but no started/ended pair - so the build could say how
    long its runs took and could not say whether any two of them overlapped.
    Concurrency was therefore unanswerable for 44 percent of the runs, and the
    gate reported clean. A duration alone cannot tell you whether the agent
    used the fan-out budget at all, which is the one question a dispatch cap
    exists to be judged on.
    """
    p = Path(root) / "cost" / "measured.jsonl"
    if not p.is_file():
        return ["no cost log at all"]
    bad = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("_schema"):
            continue
        who = r.get("label") or r.get("phase") or "?"
        if not isinstance(r.get("duration_ms"), int):
            bad.append(f"{who}: no duration")
        elif not (r.get("started") and r.get("ended")):
            bad.append(f"{who}: duration but no run window, so concurrency is unanswerable")
        elif not r.get("tier"):
            bad.append(f"{who}: no model tier recorded, so routing cannot be audited")
        elif r.get("tokens") is None and not r.get("note", "").startswith("hand:"):
            # A dispatched run that reported no usage. This gate returned CLEAN
            # for a build whose every arm run had tokens=None, and the cost
            # clauses that decided the previous build's verdict therefore had
            # nothing to judge against. A row a human wrote by hand may say so
            # with a note beginning "hand:"; a dispatched run may not.
            bad.append(f"{who}: no tokens recorded, so the cost clauses cannot be judged")
    return bad


MEASURED, PARTIAL, INDETERMINATE = "measured", "partial", "indeterminate"

# What a coordinator turn was FOR. Only one of these is waste; the rest is the
# work itself, and a timeline that cannot tell them apart invites cutting the
# wrong thing.
TURN_KINDS = {
    "authoring": "writing or rewriting the artefact - this IS the work",
    "code_check": "running a script and reading its output",
    "reading_verdict": "reading a dispatched run's result and deciding what it means",
    "planning": "deciding what to dispatch next, or triaging a red",
    "waiting": "nothing dispatched and nothing to do but wait - THE WASTE",
    "derived": "coordinator active between two run windows - derived from cost/measured.jsonl, not estimated",
    "suspended": "a gap longer than max_gap_s between run windows - the session was not running",
}


def coordinator_turn(root: Path, *, kind: str, started: float, ended: float,
                     note: str | None = None) -> dict:
    """One span of coordinator time, labelled by what it was for.

    The cost ledger records dispatched runs only, so the gaps between them are
    a single undifferentiated block. On the build of 2026-09-01 that block was
    33.5 of 95 minutes - larger than everything concurrency could ever save -
    and nothing in the record could say how much of it was the coordinator
    writing a field, which is the work, and how much was idle waiting on a run
    with an empty queue, which is not. Optimising against an unsplit number is
    guessing with arithmetic attached.
    """
    if kind not in TURN_KINDS:
        raise Refused(f"unknown coordinator turn kind {kind!r}; "
                      f"have {', '.join(sorted(TURN_KINDS))}")
    row = {"ts": now(), "kind": kind, "started": dt_iso(started), "ended": dt_iso(ended),
           "duration_ms": int(round((ended - started) * 1000))}
    if note:
        row["note"] = note
    d = Path(root) / "cost"
    d.mkdir(parents=True, exist_ok=True)
    with (d / "coordinator.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def derive_coordinator_turns(root: Path, *, max_gap_s: float = 1800.0, ended: float | None = None) -> list[dict]:
    """Rewrite cost/coordinator.jsonl from the run windows in cost/measured.jsonl.

    4.0.0. Three estimated rows in one build had negative durations and a fourth
    hid a five-hour suspension; the run windows were exact the whole time. So:
    the union of run windows is `waiting`, a gap between windows shorter than
    max_gap_s is `derived` coordinator time, a longer gap is `suspended`, and the
    tail from the last window to `ended` (now) is `derived`. Nothing is typed in.
    """
    root = Path(root)
    wins = sorted((s, e) for s, e, _ in _windows(root / "cost" / "measured.jsonl"))
    rows = []
    if not wins:
        return rows
    merged = [list(wins[0])]
    for s, e in wins[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    out = root / "cost" / "coordinator.jsonl"
    if out.exists():
        out.rename(root / "cost" / "coordinator.typed-superseded.jsonl")
    def add(kind, s, e, note):
        rows.append(coordinator_turn(root, kind=kind, started=s, ended=e, note=note))
    for i, (s, e) in enumerate(merged):
        add("waiting", s, e, "run window(s) from measured.jsonl")
        if i + 1 < len(merged):
            gap = merged[i + 1][0] - e
            add("suspended" if gap > max_gap_s else "derived", e, merged[i + 1][0],
                "gap between run windows" + (" longer than max_gap_s" if gap > max_gap_s else ""))
    tail_end = ended if ended is not None else time.time()
    if tail_end > merged[-1][1]:
        add("derived", merged[-1][1], tail_end, "after the last run window, to close")
    return rows


def _windows(path: Path) -> list[tuple[float, float, dict]]:
    if not path.is_file():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("started") and r.get("ended"):
            out.append((datetime.fromisoformat(r["started"]).timestamp(),
                        datetime.fromisoformat(r["ended"]).timestamp(), r))
    return sorted(out, key=lambda x: (x[0], x[1]))


def _union(spans: list[tuple[float, float]]) -> float:
    """Elapsed time covered by at least one span - overlaps counted once."""
    total, end = 0.0, None
    for s, e in sorted(spans):
        if end is None or s > end:
            total += e - s
            end = e
        elif e > end:
            total += e - end
            end = e
    return total


def timeline(root: Path) -> dict:
    """Where a build's wall clock went, with the unexplained part named.

    Three buckets and one confession: dispatched, coordinator (split by kind),
    and UNACCOUNTED - span that neither ledger claims. The last is reported,
    never folded into idle or into work, because an unrecorded turn and an idle
    minute look identical from outside and only one of them is a problem.
    """
    disp = _windows(Path(root) / "cost" / "measured.jsonl")
    coord = _windows(Path(root) / "cost" / "coordinator.jsonl")
    runs_without_window = 0
    p = Path(root) / "cost" / "measured.jsonl"
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if not (r.get("started") and r.get("ended")):
                    runs_without_window += 1

    if not disp and not coord:
        return {"verdict": INDETERMINATE, "reason": "no windowed rows in either ledger"}

    starts = [s for s, _, _ in disp + coord]
    ends = [e for _, e, _ in disp + coord]
    span = max(ends) - min(starts)
    disp_elapsed = _union([(s, e) for s, e, _ in disp])
    by_kind: dict[str, float] = {}
    for s, e, r in coord:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0.0) + (e - s)
    coord_elapsed = _union([(s, e) for s, e, _ in coord])
    covered = _union([(s, e) for s, e, _ in disp + coord])

    return {
        "verdict": MEASURED if not runs_without_window else PARTIAL,
        "span_s": round(span, 1),
        "dispatched_elapsed_s": round(disp_elapsed, 1),
        "coordinator_elapsed_s": round(coord_elapsed, 1),
        "coordinator_by_kind_s": {k: round(v, 1) for k, v in sorted(by_kind.items())},
        "unaccounted_s": round(span - covered, 1),
        "unaccounted_share": round((span - covered) / span, 3) if span else None,
        "runs_without_a_window": runs_without_window,
        "waste_s": round(by_kind.get("waiting", 0.0), 1),
        "note": ("unaccounted is span that NEITHER ledger claims. It is not idle time and it is "
                 "not work; it is time nobody wrote down, and calling it either would be "
                 "inventing a measurement."),
    }


def coordinator_gate(root: Path, max_unaccounted: float = 0.10) -> list[str]:
    """The coordinator's own time, held to the same standard as a dispatched run."""
    tl = timeline(root)
    if tl.get("verdict") == INDETERMINATE:
        return [tl["reason"]]
    bad = []
    if not (Path(root) / "cost" / "coordinator.jsonl").is_file():
        bad.append("no coordinator ledger at all, so every gap between dispatches is "
                   "unattributable - the largest single block in the last build")
    share = tl.get("unaccounted_share")
    if share is not None and share > max_unaccounted:
        bad.append(f"{share:.0%} of the span is claimed by neither ledger "
                   f"(cap {max_unaccounted:.0%})")
    if tl.get("runs_without_a_window"):
        bad.append(f"{tl['runs_without_a_window']} dispatched run(s) carry no window, so the "
                   f"timeline is incomplete by construction")
    return bad


def round_gate(root: Path, max_rounds: int = 3) -> list[str]:
    """Fields whose reader rounds exceeded the convergence cap.

    Read off the cost ledger's labels, which already carry the round: a reader
    is logged as read.<phase>.<field>[.rN]. The convergence rule says three
    rounds and the fourth is not attempted, and a rule that only lives in a
    contract is a convention. This makes it checkable after the run, which is
    the most a post-hoc gate can do - dispatch itself has no hook to refuse a
    fourth round before it starts.

    One field went 7 rounds and its last round took 3.9x its first.
    """
    p = Path(root) / "cost" / "measured.jsonl"
    if not p.is_file():
        return ["no cost log at all"]
    seen: dict[str, set[int]] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        lab = str(r.get("label") or "")
        if not lab.startswith("read."):
            continue
        parts = lab.split(".")
        rnd = 1
        if parts[-1].startswith("r") and parts[-1][1:].isdigit():
            rnd = int(parts[-1][1:])
            parts = parts[:-1]
        field = ".".join(parts[1:]) or lab
        seen.setdefault(field, set()).add(rnd)
    return [f"{f}: {max(rs)} rounds, cap is {max_rounds}"
            for f, rs in sorted(seen.items()) if max(rs) > max_rounds]


def routing_gate(root: Path, fixed_tier_labels: tuple[str, ...] = ()) -> list[str]:
    """Runs that must keep their tier but did not record one, or changed it.

    The routing rule protects the probe, the arm runs, the whole-artefact review
    and the graders: making those cheaper produces a different measurement
    wearing the same name. That is only auditable if the tier is on the row.
    """
    p = Path(root) / "cost" / "measured.jsonl"
    if not p.is_file():
        return ["no cost log at all"]
    tiers: dict[str, set[str]] = {}
    bad = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        lab = str(r.get("label") or "")
        if fixed_tier_labels and not lab.startswith(fixed_tier_labels):
            continue
        if not r.get("tier"):
            bad.append(f"{lab or r.get('phase')}: protected run with no tier recorded")
        else:
            tiers.setdefault("protected", set()).add(r["tier"])
    if len(tiers.get("protected", set())) > 1:
        bad.append(f"protected runs span more than one tier: {sorted(tiers['protected'])} - "
                   f"comparison with earlier builds is broken")
    return bad


def fanout_gate(root: Path) -> list[str]:
    """Speculative fan-outs whose revert did not happen (chain contract `fanout`).

    v3 dispatches the review alongside the arms, and calibration alongside the
    graders. That is only sound if a class-level review finding re-runs the arms
    and a blind grader is replaced. Both reverts leave an event; both absences
    are visible here. Empty when no fan-out event carries a trigger.
    """
    ev = events(root)
    bad = []
    for i, e in enumerate(ev):
        fn = e.get("function")
        if fn == "review_artifact" and e.get("class_finding") is True:
            # Chain 3.1.1: a red review that no arm ever followed is the correct
            # path under review_before_arms (nothing was measured on the red
            # text). What is wrong is an arm measured on it: arms BEFORE the
            # review with no rerun=true after, or arms AFTER it with neither a
            # rerun flag nor a green review in between.
            earlier = [x for x in ev[:i] if x.get("function") == "run_paired" and not x.get("skipped")]
            later_all = [x for x in ev[i + 1:]]
            rerun = [x for x in later_all if x.get("function") == "run_paired" and x.get("rerun") is True]
            if earlier and not rerun:
                bad.append("fan-out A: the review recorded a class-level finding and no run_paired "
                           "with rerun=true followed it - the arms measured the pre-review artefact")
            elif not earlier:
                for x in later_all:
                    if x.get("function") == "review_artifact" and x.get("class_finding") is False:
                        break
                    if x.get("function") == "run_paired" and not x.get("skipped"):
                        if x.get("rerun") is not True:
                            bad.append("fan-out A: arms ran after a class-level review finding with "
                                       "neither rerun=true nor a green review between - they measured "
                                       "the red text")
                        break
        if fn == "calibrate_judge" and e.get("caught") is False:
            later = [x for x in ev[i + 1:] if x.get("function") == "grade" and x.get("fresh_grader") is True]
            if not later:
                bad.append("fan-out B: calibration recorded caught=false and no grade with "
                           "fresh_grader=true followed it - the verdict rests on a grader that "
                           "missed its planted defect")
    return bad


# --- the chain gate ----------------------------------------------------------

CHAIN = REPO / "pipeline" / "contracts" / "chain.contract.json"


def load_chain() -> dict:
    return json.loads(CHAIN.read_text(encoding="utf-8"))


def chain_gate(root: Path, version: int = 1, chain: dict | None = None) -> list[dict]:
    """Phases that left NO event. Not run, not skipped - absent.

    The two contracts already abort when a declared rule has no implementation.
    This is the same defect one level up: a phase that leaves no trace cannot be
    told apart from one that was deliberately skipped, and the difference is the
    whole reason skips carry a reason.

    It exists because of one observed failure. In the chain's first real run,
    coverage_check left no event at all. The question had been answered
    implicitly while the body was written, and the record could not show that -
    in the phase whose own rule forbids it, with the function that prevents it
    sitting unused in the same file.

    Returns the offending phase rows, empty when the chain is complete. A phase
    marked skippable still needs a SKIP event; skippable means it may be skipped,
    never that it may be missing.
    """
    chain = chain or load_chain()
    ev = events(root)
    seen = {e["function"] for e in ev}
    seen |= {e["phase"] for e in ev}
    missing = []
    for ph in chain["phases"]:
        if ph["v"] > version:
            continue
        if ph["fn"] in seen or ph["id"] in seen:
            continue
        missing.append(ph)
    return missing


def chain_report(root: Path, version: int = 1) -> str:
    missing = chain_gate(root, version)
    if not missing:
        return "chain complete: every v%d phase left an event" % version
    lines = [f"INCOMPLETE - {len(missing)} phase(s) left no event, neither a run nor a skip:"]
    for ph in missing:
        tail = "" if ph["skippable"] else "   (never skippable)"
        lines.append(f"  {ph['id']:<6} {ph['fn']}{tail}")
    return "\n".join(lines)


# --- ledgers -----------------------------------------------------------------

def ledger_row(name: str, row: dict, ledgers_dir: Path | None = None) -> None:
    d = Path(ledgers_dir or LEDGERS)
    d.mkdir(parents=True, exist_ok=True)
    with (d / name).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# The chain contract names phases; a field row must speak that vocabulary or the
# gate cannot match what ran to what was declared.
FIELD_PHASE = {
    "bill_of_materials":  {"id": "4.0", "fn": "plan_bundle"},
    "references":         {"id": "4.1", "fn": "write_references"},
    "assets":             {"id": "4.2", "fn": "write_assets"},
    "name":               {"id": "4.3", "fn": "write_name"},
    "body_what_and_when": {"id": "4.4", "fn": "write_what_and_when"},
    "body_steps":         {"id": "4.5", "fn": "write_steps"},
    "pointers":           {"id": "4.6", "fn": "write_pointers"},
    "description":        {"id": "4.7", "fn": "write_description"},
    "frontmatter":        {"id": "4.8", "fn": "write_frontmatter"},
}


def field_row(root: Path, *, field: str, red_code: list[str], red_agent: list[str],
              rewrites: int, ledgers_dir: Path | None = None) -> dict:
    """One row per field per build — `fields.jsonl`.

    This is what makes the builder measurable on ITSELF. Without it we learn only
    that a skill came out good or bad; with it we learn where in the chain it did.
    """
    row = {"ts": now(), "build": header(root)["id"], "field": field,
           "red_code": red_code, "red_agent": red_agent,
           "n_red_code": len(red_code), "n_red_agent": len(red_agent),
           "rewrites": rewrites}
    ledger_row("fields.jsonl", row, ledgers_dir)
    # Log under the chain contract's own phase id and function name. The first
    # run logged every field as field_done, which the gate could not match to any
    # declared phase - so eight phases that really ran looked absent.
    ph = FIELD_PHASE.get(field)
    append(root, phase=ph["id"] if ph else "4", function=ph["fn"] if ph else "field_done",
           field=field, red_code=red_code, red_agent=red_agent, rewrites=rewrites)
    return row


def _cost_totals(root: Path) -> dict:
    """Totals, with null kept apart from a measured zero."""
    p = Path(root) / "cost" / "measured.jsonl"
    if not p.is_file():
        return {"runs": 0, "duration_ms": None, "tokens": None}
    runs = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()
            if l.strip() and not json.loads(l).get("_schema")]
    dur = [r.get("duration_ms") for r in runs]
    tok = [r.get("tokens") for r in runs]
    return {"runs": len(runs),
            "duration_ms": sum(d for d in dur if isinstance(d, int)) if all(isinstance(d, int) for d in dur) and dur else None,
            "tokens": sum(t for t in tok if isinstance(t, int)) if all(isinstance(t, int) for t in tok) and tok else None}


def build_row(root: Path, *, verdict: str, reason: str, ledgers_dir: Path | None = None) -> dict:
    """One row per build — `builds.jsonl`. Written at 8.2, whatever the verdict.

    An abandoned build is a row, not a silence: the abandon rate and its shapes
    are the thing the loop learns from.
    """
    h = header(root)
    ev = events(root)
    # The probe outcome is the single most valuable row in this ledger and the
    # one that cannot be reconstructed: it is whether the hypothesis SURVIVED
    # contact with a run. Twice now it has been refuted, and both times we found
    # that out by reading prose afterwards.
    probe = last(root, "gap_verdict") or {}
    won_on = None
    dec = last(root, "decide") or {}
    for c in dec.get("clauses") or []:
        if c.get("clause") == "win" and c.get("verdict") == "pass":
            won_on = c.get("detail")
    pk = h["package"]
    row = {
        "ts": now(),
        "build": h["id"],
        "verdict": verdict,
        "reason": reason,
        "mode": h.get("mode", "full"),
        "origin": pk.get("origin"),
        "filled_by": pk.get("filled_by"),
        "gap_kind": pk.get("gap_kind"),
        "n_claims": pk.get("n_claims"),
        "n_measured_claims": pk.get("n_measured_claims"),
        "n_sources": pk.get("n_sources"),
        "probe_outcome": probe.get("probe_outcome") or probe.get("verdict"),
        "won_on": won_on,
        "failure_kind": pk.get("failure_kind"),
        "content_kind": pk.get("content_kind"),
        "verifiable": pk.get("verifiable"),
        "phases_run": sorted({e["phase"] for e in ev if not e.get("skipped")}),
        "phases_skipped": [{"phase": e["phase"], "function": e["function"],
                            "reason": e.get("reason")} for e in ev if e.get("skipped")],
        "not_checked": [{"what": e.get("what"), "why": e.get("why")}
                        for e in ev if e["function"] == "not_checked"],
        "events": len(ev),
        "unmeasured_runs": cost_gate(root),
        "cost": _cost_totals(root),
    }
    ledger_row("builds.jsonl", row, ledgers_dir)
    append(root, phase="8", function="build_row", verdict=verdict, reason=reason)
    return row


# --- cli ---------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("open"); o.add_argument("package"); o.add_argument("--builds-dir")
    o.add_argument("--mode", default="full",
                   help="a mode declared in the chain contract: full (default), v3 or fast")
    o.add_argument("--coordinator-tier", default=None,
                   help="the model the coordinator runs on (e.g. fable, opus); recorded, never inferred")
    s = sub.add_parser("show"); s.add_argument("build_dir")
    args = ap.parse_args()

    if args.cmd == "open":
        try:
            root = open_build_record(Path(args.package),
                                     Path(args.builds_dir) if args.builds_dir else None,
                                     mode=args.mode, coordinator_tier=args.coordinator_tier)
        except Refused as exc:
            print(f"REFUSED — no build record opened: {exc}", file=sys.stderr)
            return 1
        print(root)
        return 0

    root = Path(args.build_dir)
    h = header(root)
    print(f"{h['id']}  opened {h['opened']}  mode={h.get('mode', 'full')}  "
          f"failure_kind={h['package'].get('failure_kind')}")
    for e in events(root):
        mark = "skip" if e.get("skipped") else "  · "
        extra = e.get("reason") or e.get("out") or e.get("what") or ""
        print(f"  [{e['phase']:>6}] {mark} {e['function']:<22} {extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
