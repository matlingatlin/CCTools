#!/usr/bin/env python3
"""One script per dispatching phase (chain 4.0.0). Each subcommand writes what it needs,
dispatches, grades where a code grader exists, and logs its own events - in ONE process, so
a failed write can never be followed by a run on stale text (that happened twice in one day
when a rewrite script and a dispatch shared a shell command).

    python3 pipeline/build/run_phase.py probe   <package.json> [--k 1] [--reuse-from <build-id>]
    python3 pipeline/build/run_phase.py review  <package.json> [--round N]
    python3 pipeline/build/run_phase.py arms    <package.json> [--incumbent <dir>]
    python3 pipeline/build/run_phase.py close   <package.json>

Conventions the package carries (package contract 1.3.0):
    representative_tasks[i].task            the prompt's job sentence
    representative_tasks[i].fixture         a directory mounted as ./artifact for the run (optional)
    representative_tasks[i].fixture_kind    what sort of artefact it is
    representative_tasks[i].truth           a truth file for the code grader (optional)
    grader_cmd      a command template, e.g. "python3 {skill}/evals/files/check.py {output} {truth} {fixture}";
                    exit 0 = correct. Absent -> correctness is not recorded (None), never guessed.
    artefact_dir    where the skill lives; default library/skills-candidates/<id>
The arm prompt names the CONTENT a reply must carry and never its shape (measured 2026-09-03:
a dictated shape under-measures the baseline).
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import record as rec, dispatch as dp  # noqa: E402
REPO = Path(__file__).resolve().parents[2]

def load(pkg_path: Path):
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    root = REPO / "pipeline" / "builds" / pkg["id"]
    if not root.exists():
        raise SystemExit(f"no build record at {root}; open one first (record.py open)")
    fn = {p["id"]: p["fn"] for p in rec.load_chain()["phases"]}
    skill = Path(pkg.get("artefact_dir") or (REPO / ".claude" / "skills-candidates" / pkg["id"]))
    if not skill.is_absolute(): skill = REPO / skill
    return pkg, root, fn, skill

def task_prompt(t: dict) -> str:
    base = t["task"]
    if t.get("fixture"):
        base = base.replace(t["fixture"], "./artifact") + "\n\nThe artefact is the directory ./artifact in your working directory."
    return base + " " + (t.get("reply_content") or "Report what you found and say what you examined.")

def grade(pkg, skill, t, out_path: Path) -> dict:
    cmd = pkg.get("grader_cmd")
    if not cmd or not out_path.exists():
        return {"correct": None, "checks_passed": None, "checks_total": None}
    fixture = str(REPO / t["fixture"]) if t.get("fixture") else ""
    truth = str(REPO / t["truth"]) if t.get("truth") else ""
    full = cmd.format(skill=str(skill), output=str(out_path), truth=truth, fixture=fixture)
    p = subprocess.run(full, shell=True, capture_output=True, text=True)
    m = re.search(r"(\d+)/(\d+) checks pass", p.stdout)
    row = {"correct": p.returncode == 0, "checks_passed": int(m.group(1)) if m else None, "checks_total": int(m.group(2)) if m else None,
           "failed_checks": [l[5:].strip() for l in p.stdout.splitlines() if l.startswith("FAIL")][:12]}
    for key, pat in (("recall_all", r"recall all ([\d.]+)"), ("recall_class", r"class ([\d.]+)")):
        mm = re.search(pat, p.stdout)
        if mm: row[key] = float(mm.group(1))
    return row

def row_of(r, t, i, rep, arm, pkg, skill, source="paired"):
    row = {"test": f"T{i+1}", "repeat": rep, "arm": arm, "label": r["label"], "tokens": r.get("tokens"), "tool_calls": r.get("tool_calls"),
           "duration_ms": r.get("duration_ms"), "status": r.get("status"), "source": source}
    row.update(grade(pkg, skill, t, Path(r["output"])) if r.get("status") in ("ok", "cached") else {"correct": None})
    return row

def cmd_probe(a):
    pkg, root, fn, skill = load(Path(a.package))
    tasks = pkg["representative_tasks"][: a.max_tasks] if a.max_tasks else pkg["representative_tasks"]
    if a.reuse_from:
        src = REPO / "pipeline" / "builds" / a.reuse_from
        ev = [json.loads(l) for l in (src / "events.jsonl").read_text().splitlines()]
        pe = [e for e in ev if e.get("function") == "probe_gap" and e.get("rows")]
        if not pe: raise SystemExit(f"no probe rows in {src}")
        rows = pe[-1]["rows"]
        for r in rows:
            f = src / "runs" / f"{r['label']}.md"
            if f.exists(): (root / "runs").mkdir(exist_ok=True); shutil.copy2(f, root / "runs" / f.name)
        rec.append(root, phase="2.1", function=fn["2.1"], rows=rows, runs=len(rows), reused_from=a.reuse_from,
                   out=f"{len(rows)} probe rows carried over from {a.reuse_from} (same prompt, fixtures, tier, effort); no run dispatched, no cost row here")
    else:
        jobs = []
        for i, t in enumerate(tasks):
            for rep in range(1, a.k + 1):
                jobs.append(dict(root=root, phase="2.1", label=f"probe.T{i+1}.r{rep}", arm="without", prompt=task_prompt(t), tier="opus", effort="high",
                                 add_dirs=[REPO / t["fixture"]] if t.get("fixture") else [], note=f"probe T{i+1} r{rep} ({t.get('fixture_kind')})"))
        res = dp.dispatch_many(jobs, stagger_s=20)
        rows = []
        for r, (i, t, rep) in zip(res, [(i, t, rep) for i, t in enumerate(tasks) for rep in range(1, a.k + 1)]):
            rows.append(row_of(r, t, i, rep, "without", pkg, skill, source="probe"))
        rec.append(root, phase="2.1", function=fn["2.1"], rows=rows, runs=len(rows),
                   out="; ".join(f"{r['label']} {r['status']} correct={r['correct']} {r.get('checks_passed')}/{r.get('checks_total')} tokens={r['tokens']}" for r in rows))
    valid = [r for r in rows if r.get("correct") is not None]
    outcome = "unmeasured" if not valid else ("fails" if all(r["correct"] is False for r in valid) else ("clean" if all(r["correct"] for r in valid) else "uneven"))
    fails = [{"task": r["test"], "what": "baseline run fails the grader", "quote": ", ".join(r.get("failed_checks") or [])[:600], "consequence": "the skill must clear these", "all_runs": outcome == "fails"} for r in valid if r["correct"] is False]
    rec.append(root, phase="2.2", function=fn["2.2"], failures=fails, out=f"{len(fails)} coded failure(s) from {len(valid)} graded probe row(s); {len(rows) - len(valid)} ungraded (no grader or run error)")
    rec.append(root, phase="2.3", function=fn["2.3"], verdict=outcome, probe_outcome=outcome, classification=outcome,
               out=f"baseline {outcome}; with-arm repeats per acceptance.repeats_by_probe")
    print(json.dumps({"outcome": outcome, "rows": [(r["label"], r["status"], r["correct"], r["tokens"]) for r in rows]}, indent=0))

def cmd_review(a):
    pkg, root, fn, skill = load(Path(a.package)); rnd = a.round; suffix = "" if rnd == 0 else f".r{rnd}"
    ws = root / "phase-review" / f"r{rnd}"; shutil.rmtree(ws, ignore_errors=True); (ws / "reader").mkdir(parents=True); (ws / "review").mkdir()
    shutil.copy2(skill / "SKILL.md", ws / "reader" / "SKILL.md")
    sib = root / "siblings.json"
    if sib.exists(): shutil.copy2(sib, ws / "reader" / "siblings.json")
    shutil.copytree(skill, ws / "review" / "skill", ignore=shutil.ignore_patterns("files"))
    bom = root / "bom.json"
    if not bom.exists():
        rows = [{"file": str(p.relative_to(skill)), "kind": "bundled", "why": "listed from the bundle", "status": "exists"} for p in sorted(skill.rglob("*")) if p.is_file() and p.name != "SKILL.md"]
        bom.write_text(json.dumps({"bill_of_materials": rows}, indent=1))
    shutil.copy2(bom, ws / "review" / "bom.json")
    jobs = [dict(root=root, phase="4.7", label="read.4.7.description" + suffix, arm=None, tier="opus", effort="medium",
                 inputs=[ws / "reader" / "SKILL.md"] + ([ws / "reader" / "siblings.json"] if sib.exists() else []), allowed_tools=("Read", "Glob", "Grep"), permission_mode="default",
                 prompt="You are reviewing ONLY the `description` field of the skill in ./SKILL.md" + (" against its neighbours in ./siblings.json" if sib.exists() else "") +
                        ". For each neighbour, say which of the two a router should pick for (a) the neighbour's own job and (b) this skill's job, quoting the words that decide it. Does the description name symptoms a person types, or the solution's vocabulary? Under 1024 chars? Return JSON: "
                        '{"collisions":[{"sibling":..,"query":..,"picked":..,"why":..}],"symptom_words":[..],"solution_words":[..],"verdict":"pass|red","reasons":[..]}'),
            dict(root=root, phase="5.2", label="review.5.2.whole" + suffix, arm=None, tier="opus", effort="high",
                 inputs=[ws / "review" / "skill", ws / "review" / "bom.json"], allowed_tools=("Read", "Glob", "Grep", "Bash"), permission_mode="default",
                 prompt="Review the whole skill in ./skill (SKILL.md, references/, evals/evals.json) against ./bom.json (the eval fixture files are listed but withheld here; judge the prompts and expectations as text). You cannot see how it was written. Only the whole artefact can answer: "
                        "(1) do the steps contradict each other, the rules, or the description? (2) does every step end in something checkable, and which eval expectation grades it? (3) is anything in the body a rule with no observed failure behind it? (4) is the 'In this repo' section the only place naming the host repository? Classify each finding CLASS (changes the steps or description for every instance) or INSTANCE. Return JSON: "
                        '{"findings":[{"level":"CLASS|INSTANCE","where":..,"finding":..,"quote":..}],"class_finding":true|false,"verdict":"pass|red"}')]
    if a.log_only:  # the runs exist in runs/ (a crash after dispatch); log from their outputs, dispatch nothing
        res = [{"label": j["label"], "output": str(root / "runs" / f"{j['label']}.md"), "tokens": None, "duration_ms": None} for j in jobs]
    else:
        res = dp.dispatch_many(jobs, stagger_s=15)
    out = {}
    for r in res:
        r["phase"] = "4.7" if r["label"].startswith("read.") else "5.2"
        txt = Path(r["output"]).read_text() if r.get("output") and Path(r["output"]).exists() else ""
        m = re.search(r"\{.*\}", txt, re.S)
        try: j = json.loads(m.group(0)) if m else {}
        except json.JSONDecodeError: j = {}
        if r["phase"] == "4.7":
            rec.append(root, phase="4.7", function=fn["4.7"], loop=rnd, verdict=j.get("verdict"), reader=f"{r['label']} ({r.get('tokens')} tokens, {(r.get('duration_ms') or 0)//1000} s)",
                       out="description reader: %s; reasons: %s" % (j.get("verdict"), "; ".join(map(str, j.get("reasons", [])))[:800]))
            out["reader"] = j.get("verdict"); out["reader_reasons"] = j.get("reasons", [])
        else:
            cls = bool(j.get("class_finding")); fs = j.get("findings", [])
            rec.append(root, phase="5.2", function=fn["5.2"], loop=rnd, class_finding=cls, verdict=j.get("verdict"), findings=fs, advisory=True,
                       reviewer=f"{r['label']} ({r.get('tokens')} tokens, {(r.get('duration_ms') or 0)//1000} s)",
                       out=f"review: {j.get('verdict')}; {sum(1 for f in fs if f.get('level')=='CLASS')} CLASS, {sum(1 for f in fs if f.get('level')!='CLASS')} INSTANCE (advisory: one rewrite, no cap)")
            out["review"] = j.get("verdict"); out["class_finding"] = cls; out["findings"] = fs
    (root / "phase-review" / f"r{rnd}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "findings"}, indent=0)); print(f"{len(out.get('findings', []))} findings -> {root / 'phase-review' / f'r{rnd}.json'}")
    sys.exit(3 if out.get("class_finding") else 0)

def cmd_arms(a):
    pkg, root, fn, skill = load(Path(a.package)); tasks = pkg["representative_tasks"]
    gv = rec.last(root, "gap_verdict"); outcome = (gv or {}).get("probe_outcome")
    k = {"fails": 1}.get(outcome, 2)
    jobs, meta = [], []
    for i, t in enumerate(tasks):
        base = task_prompt(t); fx = [REPO / t["fixture"]] if t.get("fixture") else []
        withp = base + f"\n\nA skill for this job is mounted read-only at the directory named {skill.name} (its SKILL.md and references). Read it first and follow it."
        for rep in range(1, k + 1):
            jobs.append(dict(root=root, phase="6.1", label=f"arm.T{i+1}.with.r{rep}", arm="with", prompt=withp, tier="opus", effort="high", add_dirs=fx, method_dir=skill)); meta.append((i, t, rep, "with"))
        jobs.append(dict(root=root, phase="6.1", label=f"arm.T{i+1}.without.r1", arm="without", prompt=base, tier="opus", effort="high", add_dirs=fx)); meta.append((i, t, 1, "without"))
        if a.incumbent:
            inc = Path(a.incumbent); incp = base + f"\n\nA skill for this job is mounted read-only at the directory named {inc.name} (its SKILL.md and references). Read it first and follow it."
            jobs.append(dict(root=root, phase="6.1", label=f"arm.T{i+1}.incumbent.r1", arm="with", prompt=incp, tier="opus", effort="high", add_dirs=fx, method_dir=inc)); meta.append((i, t, 1, "incumbent"))
    res = dp.dispatch_many(jobs, stagger_s=20)
    rows = [row_of(r, t, i, rep, arm, pkg, skill) for r, (i, t, rep, arm) in zip(res, meta)]
    inc_rows = [r for r in rows if r["arm"] == "incumbent"]; rows = [r for r in rows if r["arm"] != "incumbent"]
    # blinded copies for 6.2
    blind = root / "blind"; shutil.rmtree(blind, ignore_errors=True); blind.mkdir(); key = {}
    import secrets
    for r in rows + inc_rows:
        lab = "item-" + secrets.token_hex(3); key[lab] = r["label"]; src = root / "runs" / f"{r['label']}.md"
        if src.exists(): shutil.copy2(src, blind / f"{lab}.md")
    (root / "blind_key.json").write_text(json.dumps(key, indent=1))
    rec.append(root, phase="6.2", function=fn["6.2"], out=f"{len(key)} blinded copies in blind/ (key withheld in blind_key.json); expectations are written from them by the coordinator", n_blinded=len(key))
    if pkg.get("grader_cmd"):
        rec.skipped(root, phase="6.3", function=fn["6.3"], reason="the grader is code (grader_cmd); nothing to calibrate")
        rec.append(root, phase="6.4", function=fn["6.4"], grader=pkg["grader_cmd"], rows=rows, out="; ".join(f"{r['label']}: correct={r['correct']} {r.get('checks_passed')}/{r.get('checks_total')}" for r in rows))
    if inc_rows:
        rec.append(root, phase="6.1", function=fn["6.1"], incumbent=True, rows=inc_rows, out="incumbent arm: " + "; ".join(f"{r['label']}: correct={r['correct']}" for r in inc_rows))
    rec.append(root, phase="6.1", function=fn["6.1"], rows=rows, runs=len(rows), out=f"with x{k}, without x1 per task (k from probe outcome {outcome!r}); probe rows are the other without repeats")
    print(json.dumps([(r["label"], r["status"], r["correct"], r["tokens"], r["tool_calls"]) for r in rows + inc_rows], indent=0))

def cmd_close(a):
    import decide as dec
    pkg, root, fn, skill = load(Path(a.package))
    rec.derive_coordinator_turns(root)
    d = dec.decide(root)
    rec.append(root, phase="8.1", function=fn["8.1"], verdict=d["verdict"], reason=d.get("reason"), clauses=d.get("clauses"))
    row = rec.build_row(root, verdict=d["verdict"], reason=d.get("reason") or "")
    tl = rec.timeline(root)
    print(json.dumps({"verdict": d["verdict"], "reason": d.get("reason"), "clauses": d.get("clauses"), "timeline": {k: v for k, v in tl.items() if not isinstance(v, (list, dict)) and k != "note"},
                      "gates": {"fanout": rec.fanout_gate(root), "cost": rec.cost_gate(root), "chain_missing": [m["id"] for m in rec.chain_gate(root)]}}, indent=1))

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("probe"); p.add_argument("package"); p.add_argument("--k", type=int, default=1); p.add_argument("--reuse-from"); p.add_argument("--max-tasks", type=int, default=0); p.set_defaults(f=cmd_probe)
    p = sub.add_parser("review"); p.add_argument("package"); p.add_argument("--round", type=int, default=0); p.add_argument("--log-only", action="store_true"); p.set_defaults(f=cmd_review)
    p = sub.add_parser("arms"); p.add_argument("package"); p.add_argument("--incumbent"); p.set_defaults(f=cmd_arms)
    p = sub.add_parser("close"); p.add_argument("package"); p.set_defaults(f=cmd_close)
    a = ap.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
