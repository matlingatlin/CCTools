#!/usr/bin/env python3
"""Positive controls for the dispatch harness.

The load-bearing cases are the three contaminations of build 3, reconstructed
one each. If any of them can still be expressed through this module, the
module has not earned its place over the shell it replaces.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dispatch as dp  # noqa: E402
import record as rec  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "validate"))

FAILS = 0


def check(ok, label, detail=""):
    global FAILS
    if not ok:
        FAILS += 1
    print(f"{'ok  ' if ok else 'FAIL'} {label}{('  — ' + str(detail)) if detail and not ok else ''}")


def fake_runner(text="an answer", tokens=1234, turns=3, model="claude-opus-5", rc=0):
    """Stands in for the CLI. Records the cwd and command it was given."""
    calls = []

    def run(cmd, cwd, timeout_s):
        calls.append({"cmd": cmd, "cwd": Path(cwd)})
        if rc != 0:
            return rc, "", "boom"
        payload = {"result": text, "num_turns": turns,
                   "usage": {"input_tokens": tokens, "output_tokens": 0},
                   "modelUsage": {model: {}, "claude-haiku-4-5-20251001": {}},
                   "duration_ms": 1000, "duration_api_ms": 700}
        return 0, json.dumps(payload), ""
    run.calls = calls
    return run


def pkg_at(d: Path) -> Path:
    src = json.loads((Path(__file__).resolve().parents[2] / "pipeline" / "packages"
                      / "eval-set-curation-v2.json").read_text(encoding="utf-8"))
    src["id"] = "dispatch-selftest"
    src["budget"] = {"max_agents": 4, "max_paired_runs": 100}  # these controls test isolation, not the budget guard (selftest_dispatch_400.py does)
    for i, tk in enumerate(src.get("representative_tasks", [])):  # package contract 1.3.0: two kinds
        tk.setdefault("fixture_kind", ["skill bundle", "runbook without expectations"][i % 2])
    p = d / "p.json"
    p.write_text(json.dumps(src))
    return p


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        root = rec.open_build_record(pkg_at(tmp), builds_dir=tmp / "b")
        fixture = tmp / "fixture"; fixture.mkdir(); (fixture / "data.csv").write_text("a,b\n1,2\n")
        method = tmp / "method"; method.mkdir(); (method / "SKILL.md").write_text("# m\n")

        # --- CONTAMINATION 1: a shared working directory ----------------------
        r = fake_runner()
        a = dp.dispatch(root=root, phase="2.1", label="probe.p1.r1", arm="without",
                        prompt="x", add_dirs=[fixture], _runner=r)
        b = dp.dispatch(root=root, phase="2.1", label="probe.p1.r1", arm="without",
                        prompt="x", add_dirs=[fixture], _runner=r)
        check(a["cwd"] != b["cwd"], "two dispatches of the SAME label get different directories",
              f"{a['cwd']} == {b['cwd']}")
        check(r.calls[0]["cwd"] != r.calls[1]["cwd"],
              "and the CLI was actually run in different directories")

        # --- CONTAMINATION 2: the arm name in the path ------------------------
        for arm in dp.ARMS:
            x = dp.dispatch(root=root, phase="6.1", label=f"arm.E1.{arm}", arm=arm,
                            prompt="x", add_dirs=[fixture],
                            method_dir=(method if arm == "with" else None), _runner=fake_runner())
            check(arm not in Path(x["cwd"]).name.lower(),
                  f"the {arm}-arm's directory name carries no arm string", Path(x["cwd"]).name)

        # --- CONTAMINATION 3: the method mounted for every arm ----------------
        for arm in ("without", "incumbent"):
            try:
                dp.dispatch(root=root, phase="6.1", label="arm.E1.x", arm=arm, prompt="x",
                            method_dir=method, _runner=fake_runner())
                check(False, f"method_dir for the {arm}-arm is refused")
            except ValueError as exc:
                check("Only the with-arm" in str(exc), f"method_dir for the {arm}-arm is refused")
        w = fake_runner()
        dp.dispatch(root=root, phase="6.1", label="arm.E1.with", arm="with", prompt="x",
                    method_dir=method, _runner=w)
        wm = [c for c in w.calls[0]["cmd"] if c.endswith("/method")]
        check(len(wm) == 1 and (Path(wm[0]) / "SKILL.md").is_file(),
              "and the with-arm DOES get the method mounted (as a view carrying SKILL.md)", w.calls[0]["cmd"][-1])
        wo = fake_runner()
        dp.dispatch(root=root, phase="6.1", label="arm.E1.without", arm="without", prompt="x",
                    add_dirs=[fixture], _runner=wo)
        check(str(method.resolve()) not in " ".join(wo.calls[0]["cmd"]),
              "while the without-arm's command names no method directory")

        # --- THE COST GAP: tokens captured, and a usage-less run is not ok ----
        x = dp.dispatch(root=root, phase="6.1", label="arm.E2.with", arm="with", prompt="x",
                        method_dir=method, _runner=fake_runner(tokens=5000, turns=7))
        check(x["tokens"] == 5000 and x["tool_calls"] == 7, "tokens and tool calls come back",
              (x["tokens"], x["tool_calls"]))
        rows = [json.loads(l) for l in (root / "cost" / "measured.jsonl").read_text().splitlines()
                if l.strip()]
        last = rows[-1]
        check(last.get("tokens") == 5000 and last.get("tier") == "opus" and last.get("started"),
              "and the cost row carries tokens, tier and a window", last)
        y = dp.dispatch(root=root, phase="6.1", label="arm.E3.with", arm="with", prompt="x",
                        method_dir=method, _runner=fake_runner(tokens=0))
        check(y["ok"] is False and y["status"] == "no_usage",
              "a run reporting no usage is NOT ok, whatever it answered", y["status"])

        # --- the leak check: a run that names its own arm is flagged ----------
        z = dp.dispatch(root=root, phase="6.1", label="arm.E4.with", arm="with", prompt="x",
                        method_dir=method,
                        _runner=fake_runner(text="Artefacts are in the with-arm output dir."))
        check(z["arm_leak"] is True, "an answer that names its arm is flagged as a leak")
        q = dp.dispatch(root=root, phase="6.1", label="arm.E5.with", arm="with", prompt="x",
                        method_dir=method, _runner=fake_runner(text="The cut is 0.506."))
        check(q["arm_leak"] is False, "and an answer that does not is not")

        # --- failures are failures, not silent successes ----------------------
        f = dp.dispatch(root=root, phase="6.1", label="arm.E6.with", arm="with", prompt="x",
                        method_dir=method, _runner=fake_runner(rc=1))
        check(f["ok"] is False and f["status"] == "error", "a non-zero exit is an error")

        # --- inputs are COPIED in, so the run sees no siblings ----------------
        inp = tmp / "SKILL.md"; inp.write_text("---\nname: x\n---\n")
        g = dp.dispatch(root=root, phase="4.3", label="read.4.3", arm=None, prompt="x",
                        inputs=[inp], _runner=fake_runner())
        check((Path(g["cwd"]) / "SKILL.md").is_file(), "a declared input is copied into the run")
        check(not (Path(g["cwd"]) / "data.csv").exists(),
              "and nothing undeclared is there with it")

        # --- memo: the same key replays from disk; a changed method misses ------
        m1 = fake_runner(text="first answer", tokens=777, turns=2)
        a1 = dp.dispatch(root=root, phase="2.1", label="probe.M.r1", arm="without", prompt="memo-q",
                         add_dirs=[fixture], memo=True, _runner=m1)
        m2 = fake_runner(text="SHOULD NOT RUN", tokens=1, turns=1)
        a2 = dp.dispatch(root=root, phase="2.1", label="probe.M.r1b", arm="without", prompt="memo-q",
                         add_dirs=[fixture], memo=True, _runner=m2)
        check(a1["cached"] is False and a2["cached"] is True and not m2.calls,
              "a memoised replay does not run the CLI", (a1["cached"], a2["cached"], len(m2.calls)))
        check(a2["text"] == "first answer" and a2["tokens"] == 777,
              "and returns the first run's answer and tokens")
        rows = [json.loads(l) for l in (root / "cost" / "measured.jsonl").read_text().splitlines()
                if l.strip()]
        check(rows[-1].get("cached") is True and rows[-1].get("duration_ms") == 0,
              "the replay's cost row says cached=true with a zero window", rows[-1])
        check(rows[-2].get("cached") is None, "a real run's row carries no cached field")
        m3 = fake_runner(text="fresh", tokens=5)
        dp.dispatch(root=root, phase="2.1", label="probe.M.r1c", arm="without", prompt="memo-q",
                    add_dirs=[fixture], memo=False, _runner=m3)
        check(len(m3.calls) == 1, "memo=False always runs, even with a hit on disk")
        mw1 = fake_runner(text="with v1", tokens=9)
        dp.dispatch(root=root, phase="6.1", label="arm.M.with", arm="with", prompt="memo-q",
                    method_dir=method, memo=True, _runner=mw1)
        (method / "SKILL.md").write_text("# m v2\n")
        mw2 = fake_runner(text="with v2", tokens=9)
        w2 = dp.dispatch(root=root, phase="6.1", label="arm.M.with2", arm="with", prompt="memo-q",
                         method_dir=method, memo=True, _runner=mw2)
        check(w2["cached"] is False and len(mw2.calls) == 1,
              "a changed skill misses the memo by construction (method bytes are in the key)")
        # --- the with-arm sees the method, never its evals -----------------------
        (method / "evals").mkdir(exist_ok=True); (method / "evals" / "answers.json").write_text("{}")
        (method / "references").mkdir(exist_ok=True); (method / "references" / "r.md").write_text("ref")
        mv = fake_runner()
        v = dp.dispatch(root=root, phase="6.1", label="arm.MV.with", arm="with", prompt="x", method_dir=method, _runner=mv)
        mounted = [c for c in mv.calls[0]["cmd"] if c.endswith("/method")]
        check(len(mounted) == 1 and mounted[0] != str(method.resolve()),
              "the with-arm mounts a VIEW of the method, not the skill directory itself", mv.calls[0]["cmd"][-1])
        vdir = Path(mounted[0])
        check((vdir / "SKILL.md").is_file() and (vdir / "references" / "r.md").is_file()
              and not (vdir / "evals").exists(),
              "the view holds SKILL.md and references and NO evals directory", sorted(p.name for p in vdir.iterdir()))
        # --- a run can edit its own directory: permission mode pre-approved -----
        pm = fake_runner()
        dp.dispatch(root=root, phase="2.1", label="probe.PM.r1", arm="without", prompt="x", _runner=pm)
        cmdline = " ".join(pm.calls[0]["cmd"])
        check("--permission-mode acceptEdits" in cmdline and "--allowedTools" in cmdline and "Edit" in cmdline,
              "a run gets edits pre-approved (headless runs cannot answer a prompt)", cmdline[-160:])
        rows = [json.loads(l) for l in (root / "cost" / "measured.jsonl").read_text().splitlines() if l.strip()]
        check(rows[-1].get("permission_mode") == "acceptEdits", "and the mode is on the cost row")
        # --- effort goes on the command AND the row -----------------------------
        ef = fake_runner()
        e = dp.dispatch(root=root, phase="6.1", label="arm.E7.with", arm="with", prompt="x",
                        method_dir=method, effort="high", _runner=ef)
        check("--effort" in ef.calls[0]["cmd"] and "high" in ef.calls[0]["cmd"],
              "effort is passed to the CLI")
        rows = [json.loads(l) for l in (root / "cost" / "measured.jsonl").read_text().splitlines()
                if l.strip()]
        check(rows[-1].get("effort") == "high", "and recorded on the cost row")
        check("--effort" not in " ".join(w.calls[0]["cmd"]), "no effort given, no flag sent")
        # --- dispatch_many: stagger and rate-limit retry -----------------------
        slept = []
        jobs = [dict(root=root, phase="6.1", label=f"arm.S{i}.with", arm="with", prompt="x",
                     method_dir=method, _runner=fake_runner()) for i in range(3)]
        rs = dp.dispatch_many(jobs, concurrency=3, stagger_s=7, _sleep=slept.append)
        check(len(rs) == 3 and slept.count(7) == 2,
              "every job after the first waits stagger_s before launching", slept)
        state = {"n": 0}
        def flaky(cmd, cwd, timeout_s):
            state["n"] += 1
            if state["n"] == 1:
                return 1, "", "API error 429: rate limit exceeded"
            return 0, json.dumps({"result": "ok now", "num_turns": 1,
                                  "usage": {"input_tokens": 10, "output_tokens": 1},
                                  "modelUsage": {"claude-opus-5": {}}}), ""
        slept = []
        rs = dp.dispatch_many([dict(root=root, phase="6.1", label="arm.R.with", arm="with",
                                    prompt="x", method_dir=method, _runner=flaky)],
                              concurrency=1, _sleep=slept.append)
        check(rs[0]["ok"] and rs[0]["rate_limit_retries"] == 1 and slept == [30],
              "a 429 is retried after the first backoff and the retry count comes back",
              (rs[0]["status"], rs[0].get("rate_limit_retries"), slept))
        def always429(cmd, cwd, timeout_s):
            return 1, "", "429 too many requests"
        slept = []
        rs = dp.dispatch_many([dict(root=root, phase="6.1", label="arm.R2.with", arm="with",
                                    prompt="x", method_dir=method, _runner=always429)],
                              concurrency=1, max_rate_limit_retries=2, _sleep=slept.append)
        check(rs[0]["ok"] is False and rs[0]["rate_limit_retries"] == 2 and slept == [30, 60],
              "a run still rate-limited after the cap is a failure, not a silent success",
              (rs[0]["status"], slept))
        def plain_error(cmd, cwd, timeout_s):
            return 1, "", "segfault"
        rs = dp.dispatch_many([dict(root=root, phase="6.1", label="arm.R3.with", arm="with",
                                    prompt="x", method_dir=method, _runner=plain_error)],
                              concurrency=1, _sleep=slept.append)
        check(rs[0]["rate_limit_retries"] == 0, "an error that is not a rate limit is not retried")
        # --- the cost gate now catches missing tokens -------------------------
        with (root / "cost" / "measured.jsonl").open("a") as fh:
            fh.write(json.dumps({"phase": "6.1", "label": "hand-written-row", "duration_ms": 1,
                                 "started": "2026-09-02T00:00:00+00:00",
                                 "ended": "2026-09-02T00:00:01+00:00", "tier": "opus"}) + "\n")
        gate = rec.cost_gate(root)
        check(any("hand-written-row" in x and "tokens" in x for x in gate),
              "cost_gate names a dispatched run with no tokens", str(gate)[:120])

    print(f"\n{'PASS' if FAILS == 0 else 'FAIL'}: {FAILS} failing check(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
