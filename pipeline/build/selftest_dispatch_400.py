"""Controls for the 4.0.0 dispatch rules: the package budget is enforced in code, and a run that dies with no output is retried once."""
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import record as rec, dispatch as dp  # noqa: E402
FAILS = []
def check(ok, what, detail=""):
    print(("ok   " if ok else "FAIL ") + what + ("" if ok else f" — {detail}"))
    if not ok: FAILS.append(what)
def runner(script):
    """script: list of (rc, stdout_payload_or_None, stderr). None payload = empty stdout (a dead run)."""
    calls = []
    def run(cmd, cwd, timeout_s):
        calls.append(cmd); rc, payload, err = script[min(len(calls) - 1, len(script) - 1)]
        if payload is None: return rc, "", err
        return rc, json.dumps({"result": payload, "usage": {"input_tokens": 100, "output_tokens": 50}, "num_turns": 2, "modelUsage": {"claude-opus-5": {}}, "duration_ms": 1000, "duration_api_ms": 700}), err
    run.calls = calls; return run
def pkg(d):
    src = json.loads((Path(__file__).resolve().parents[2] / "pipeline/packages/eval-set-curation-v2.json").read_text())
    src["id"] = "dispatch-400"; src["budget"] = {"max_agents": 4, "max_paired_runs": 2}
    for i, tk in enumerate(src["representative_tasks"]): tk.setdefault("fixture_kind", ["a", "b"][i % 2])
    p = d / "p.json"; p.write_text(json.dumps(src)); return p
def main():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td); root = rec.open_build_record(pkg(tmp), builds_dir=tmp / "b", mode="promote", coordinator_tier="fable")
        fx = tmp / "fx"; fx.mkdir(); (fx / "a.txt").write_text("x")
        for i in range(2):
            dp.dispatch(root=root, phase="6.1", label=f"arm.T1.without.r{i+1}", arm="without", prompt="x", add_dirs=[fx], _runner=runner([(0, "ok", "")]))
        try:
            dp.dispatch(root=root, phase="6.1", label="arm.T1.without.r3", arm="without", prompt="x", add_dirs=[fx], _runner=runner([(0, "ok", "")]))
            check(False, "a third paired run against max_paired_runs=2 is refused")
        except rec.Refused as e:
            check("budget" in str(e), "a third paired run against max_paired_runs=2 is refused", str(e))
        r = dp.dispatch(root=root, phase="2.1", label="probe.T1.r1", arm="without", prompt="x", add_dirs=[fx], _runner=runner([(0, "ok", "")]))
        check(r["status"] == "ok", "a non-6.1 phase is not budget-gated")
        # dead run: rc 1, empty stdout, empty stderr -> retried once by dispatch_many
        rr = runner([(1, None, ""), (0, "alive", "")])
        res = dp.dispatch_many([dict(root=root, phase="2.1", label="probe.T2.r1", arm="without", prompt="x", add_dirs=[fx], _runner=rr)], concurrency=1)
        check(res[0]["status"] == "ok" and res[0].get("dead_retries") == 1 and len(rr.calls) == 2, "a run that died with no output and no stderr is retried exactly once", (res[0]["status"], res[0].get("dead_retries"), len(rr.calls)))
        rr2 = runner([(1, None, ""), (1, None, "")])
        res = dp.dispatch_many([dict(root=root, phase="2.1", label="probe.T3.r1", arm="without", prompt="x", add_dirs=[fx], _runner=rr2)], concurrency=1)
        check(res[0]["status"] == "error" and len(rr2.calls) == 2, "a second death is not retried", (res[0]["status"], len(rr2.calls)))
        rr3 = runner([(1, None, "Traceback: boom")])
        res = dp.dispatch_many([dict(root=root, phase="2.1", label="probe.T4.r1", arm="without", prompt="x", add_dirs=[fx], _runner=rr3)], concurrency=1)
        check(len(rr3.calls) == 1, "a run that died WITH stderr is not retried (that is a real error)", len(rr3.calls))
    print(f"\n{'PASS' if not FAILS else 'FAIL'}: {len(FAILS)} failing check(s)"); return 1 if FAILS else 0
if __name__ == "__main__": sys.exit(main())
