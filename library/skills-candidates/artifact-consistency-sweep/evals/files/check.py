#!/usr/bin/env python3
"""Shape grader for artifact-consistency-sweep. Facts about the run's OUTPUT, no judgement.
usage: python3 check.py <output.md> <truth.json> <artifact_dir>
A finding block = a JSON object in a findings list, or a markdown table row / bullet. A truth row is HIT when some
block names its anchor (e.g. 'step 2', 'rules', 'description', 'check.py') and either quotes the same artefact line (a 20-char run of
the truth quote) or uses one of the four rarest words of the original reviewer's diagnosis. Same defect, any phrasing.
Recall is reported over all rows and over the CLASS rows; MISSED rows (present in the text, missed by that
round's reviewer) are reported separately. The matrix checks: one row per numbered step with 'checkable' and
'graded' verdicts, and every Rules bullet cross-referenced. Exit 1 on any FAIL.
"""
import json, re, sys, pathlib
out = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"); truth = json.loads(pathlib.Path(sys.argv[2]).read_text())
# Rows about the grader's own code (anchor check.py, scope grader-code) are outside the sweep's declared scope -
# its pair types cover the artefact's text (steps, rules, expectations, description, files), not the regexes of a
# grader that a reviewer found by executing it. Triaged as a test-bug at iterate round 3 and excluded from the
# recall denominators; reported separately so the exclusion is visible.
graded_code = [r for r in truth if r.get("scope") == "grader-code"]
truth = [r for r in truth if r.get("scope") != "grader-code"]; art = pathlib.Path(sys.argv[3])
rows = []
def check(name, ok, detail=""):
    rows.append((name, ok)); print(f"{'PASS' if ok else 'FAIL'} {name} {detail if not ok else ''}")
# --- blocks: JSON findings if present, else table rows / bullets
blocks = []
m = re.search(r"\{.*\"findings\".*\}", out, re.S)
if m:
    try:
        j = json.loads(m.group(0)); blocks = [json.dumps(f) for f in j.get("findings", [])]
    except json.JSONDecodeError:
        blocks = []
if not blocks:
    blocks = [l for l in out.splitlines() if l.strip().startswith(("|", "-", "*")) and len(l) > 30]
check("findings are structured (a findings JSON list or table/bullet rows)", len(blocks) >= 3, f"{len(blocks)} blocks")
def _norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
def hit(row):
    """Same defect, any phrasing: the block names the same anchor AND either quotes the same artefact line
    (a 20-character run of the truth quote, whitespace/punctuation-insensitive) or uses one of the diagnosis words."""
    a = row["anchor"].lower(); kws = [k.lower() for k in row["keywords"]]; q = _norm(row.get("quote") or "")
    grams = {q[i:i+20] for i in range(0, max(len(q) - 20, 0) + 1, 4)} if len(q) >= 20 else set()
    for b in blocks:
        bl = b.lower(); nb = _norm(b)
        if a not in bl: continue
        if any(k in bl for k in kws): return True
        if grams and any(g in nb for g in grams): return True
    return False
hits = {r["id"]: hit(r) for r in truth}
cls = [r for r in truth if r["level"] == "CLASS"]; missed = [r for r in truth if "missed_in" in r]
rec_all = sum(hits.values()) / max(len(truth), 1); rec_cls = sum(hits[r["id"]] for r in cls) / max(len(cls), 1)
rec_missed = sum(hits[r["id"]] for r in missed) / max(len(missed), 1) if missed else None
for r in truth: print(f"  {'hit ' if hits[r['id']] else 'miss'} {r['id']:<8} {r['level']:<8} {r['anchor']:<12} {r['keywords']}")
check(f"recall over the known findings >= 0.60 (got {rec_all:.2f})", rec_all >= 0.60)
check(f"recall over CLASS findings >= 0.70 (got {rec_cls:.2f})", rec_cls >= 0.70)
if missed: check(f"recall over findings the round's own reviewer MISSED >= 0.50 (got {rec_missed:.2f})", rec_missed >= 0.50)
check("precision proxy: at most 3x as many blocks as known findings", len(blocks) <= 3 * max(len(truth), 1), f"{len(blocks)} blocks vs {len(truth)}")
# --- the matrix: one row per numbered step in SKILL.md with checkable/graded verdicts
sk = (art / "SKILL.md").read_text(encoding="utf-8")
steps = re.findall(r"^\s*(\d+)\.\s+\*\*", sk, re.M)
n_steps = len(set(steps))
step_rows = [b for b in blocks if re.search(r"step\s*\d", b, re.I) and re.search(r"checkable|graded|ends in|observable|ungraded", b, re.I)]
if m:
    try:
        jj = json.loads(m.group(0)); js = jj.get("steps") or jj.get("matrix") or []
        step_rows = [json.dumps(s) for s in js if isinstance(s, dict) and ("checkable" in s or "graded_by" in s or "graded" in s)] or step_rows
    except json.JSONDecodeError:
        pass
check(f"a matrix row per step: {n_steps} steps in the artefact, rows with a checkable/graded verdict found {len(step_rows)}", len(step_rows) >= n_steps)
rules = re.findall(r"^## Rules\n((?:- .*\n?)+)", sk, re.M)
n_rules = len(re.findall(r"^- ", rules[0], re.M)) if rules else 0
rule_rows = [b for b in blocks if re.search(r"\brule", b, re.I)]
if n_rules: check(f"the Rules bullets are examined: {n_rules} rules, rule-referencing rows {len(rule_rows)}", len(rule_rows) >= 1)
ledger = None
if m:
    try: ledger = json.loads(m.group(0)).get("ledger")
    except json.JSONDecodeError: ledger = None
check("a ledger says what was examined: plan and examined counts per pair type (JSON 'ledger' or a counts table)",
      (isinstance(ledger, (dict, list)) and len(ledger) >= 3) or re.search(r"(plan|planned|owed)[^\n]{0,40}(examined|rows)", out, re.I) is not None)
if m:
    try:
        jf = json.loads(m.group(0)).get("findings", [])
        qlists = [f.get("quotes") if isinstance(f.get("quotes"), list) else ([f.get("quote")] if f.get("quote") else []) for f in jf]
        flat = [q for ql in qlists for q in ql if isinstance(q, str) and q.strip()]
        # two findings on the same PLACE sharing a quote = one defect reported twice
        def _place(f): return set(re.findall(r"step\s*\d+|rule\s*\d+|bullet\s*\d+|expectation\s*\d+|clause\s*\d+", str(f.get("where", "")).lower()))  # numbered places only: two findings quoting one definition from different angles are not one defect
        dup = 0
        for a in range(len(jf)):
            for b in range(a + 1, len(jf)):
                qa = set(q for q in (qlists[a] or []) if isinstance(q, str)); qb = set(q for q in (qlists[b] or []) if isinstance(q, str))
                if qa & qb and (_place(jf[a]) & _place(jf[b])): dup += 1
        check("no two findings on the same place share a quote (a defect reported twice is one finding)", dup == 0, f"{dup} pair(s)")
        check("findings carry a quotes LIST (or a quote), none empty", all(ql for ql in qlists), f"{sum(1 for ql in qlists if not ql)} without")
    except json.JSONDecodeError:
        pass
def _pair_ids(o):
    """Count pair ids anywhere under the ledger: lists under keys named pairs / examined_pairs / rows, at any depth."""
    n = 0
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("pairs", "examined_pairs", "pair_ids", "rows") and isinstance(v, list): n += len(v)
            else: n += _pair_ids(v)
    elif isinstance(o, list):
        for v in o: n += _pair_ids(v)
    return n
if isinstance(ledger, (dict, list)):
    ids = _pair_ids(ledger)
    check("the ledger names the examined pairs, not only counts", ids >= 10, f"{ids} pair ids")
# --- the seven pair types: a ledger row (JSON entry or table line) naming each of them
J = r"[\W_]*(x|×|vs|against)?[\W_]*"  # the join between the two names of a pair type: 'step × rule', 'step_x_rule', 'step-rule', 'steps vs rules'
TYPES = {"step x rule": "steps?" + J + "rules?", "step x step": "steps?" + J + "(steps?|each other|the next)", "step x check": "steps?" + J + "(checks?|expectations?|evals?)", "description x body": r"description",
         "file x bom": r"(bom|bill.of.materials|files?)", "step x instance": r"instance", "claim x rationale": r"rationale"}
ledger_txt = json.dumps(ledger, ensure_ascii=False) if ledger is not None else ""  # keep × as ×, not \u00d7
if not ledger_txt:
    ml = re.search(r"(ledger|examined)(.*?)(finding|matrix)", out, re.I | re.S); ledger_txt = ml.group(0) if ml else ""
named = [k for k, p in TYPES.items() if re.search(p, ledger_txt, re.I)]
check(f"the ledger carries a row for each of the seven pair types: {len(named)} named", len(named) >= 7, f"missing {[k for k in TYPES if k not in named]}")
# --- shortfall: when a type's examined count is under its plan, the ledger says so
short = []
if isinstance(ledger, dict):
    for k, v in ledger.items():
        if isinstance(v, dict):
            plan = v.get("plan", v.get("planned", v.get("plan_count"))); ex = v.get("examined", v.get("examined_count"))
            try:
                if plan is not None and ex is not None and int(ex) < int(plan): short.append(k)
            except (TypeError, ValueError):
                pass
if short:
    check(f"the ledger states the shortfall for {short}", re.search(r"shortfall|short by|not examined|unexamined|fewer than plan", ledger_txt + out[:0], re.I) is not None or any(isinstance(ledger[k], dict) and any(kk in ledger[k] for kk in ("shortfall", "short", "unexamined")) for k in short))
# --- examined == plan for every type, or the unruled pairs are named
if isinstance(ledger, dict):
    unruled = []
    for k, v in ledger.items():
        if isinstance(v, dict):
            plan = v.get("plan", v.get("planned", v.get("plan_count"))); ex = v.get("examined", v.get("examined_count"))
            try:
                if plan is not None and ex is not None and int(ex) < int(plan): unruled.append(f"{k} {ex}/{plan}")
            except (TypeError, ValueError):
                pass
    check(f"examined equals plan for every pair type: short {unruled}", not unruled)
    sr = next((v for k, v in ledger.items() if isinstance(v, dict) and re.search(r"steps?[\W_]*(x|×)?[\W_]*rules?", k, re.I)), None)
    if sr is not None and n_rules:
        try:
            plan_sr = int(sr.get("plan", sr.get("planned", sr.get("plan_count"))))
            check(f"step x rule plan count {plan_sr} is at least steps x Rules bullets = {n_steps * n_rules}", plan_sr >= n_steps * n_rules)
        except (TypeError, ValueError):
            check("step x rule plan count is a number", False, str(sr)[:80])
# --- findings cap: at most non-consistent pair rows + unchecked/ungraded step rows
if m and isinstance(ledger, dict):
    try:
        jj = json.loads(m.group(0)); nf = len(jj.get("findings", []))
        ncr = None
        for v in ledger.values():
            if isinstance(v, dict) and "non_consistent_rows" in v: ncr = int(v["non_consistent_rows"])
        if ncr is None:
            ncr = sum(len(v.get("non_consistent", v.get("non_consistent_rows", []))) for v in ledger.values() if isinstance(v, dict) and isinstance(v.get("non_consistent", v.get("non_consistent_rows")), list))
        mx = jj.get("matrix") or jj.get("steps") or jj.get("step_matrix") or []
        bad_steps = sum(1 for s in mx if isinstance(s, dict) and (str(s.get("checkable")).lower() in ("false", "unchecked", "no") or "ungraded" in str(s.get("graded_by", "")).lower()))
        if ncr: check(f"findings cap: {nf} findings <= {ncr} non-consistent rows + {bad_steps} unchecked/ungraded steps", nf <= ncr + bad_steps)
    except (json.JSONDecodeError, TypeError, ValueError):
        pass
# --- other rows become findings against the pair-type table; part counts with rule quotes
if m and isinstance(ledger, dict):
    try:
        jj = json.loads(m.group(0)); others = []
        for k, v in ledger.items():
            if "other" in k.lower() and isinstance(v, list): others += v
        if others:
            check("an other row is also a finding whose where names the pair-type table", any(re.search(r"pair.type table|reference|other", str(f.get("where", "")), re.I) for f in jj.get("findings", [])))
        pc = next((v for k, v in ledger.items() if isinstance(v, dict) and re.search(r"part|count", k, re.I) and any(re.search(r"^steps?$|^rules?$", kk) for kk in v)), None)
        check("the ledger carries the part counts (steps, rules, ...)", pc is not None)
        if pc is not None:
            outside = next((v for k, v in pc.items() if "outside" in k.lower()), None)
            if isinstance(outside, dict) and outside:
                check("rules counted outside a Rules heading are quoted", all(isinstance(q, str) and len(q) > 12 for q in outside.values()))
            elif isinstance(outside, list) and outside:
                check("rules counted outside a Rules heading are quoted", all(isinstance(q, (str, dict)) and len(str(q)) > 12 for q in outside))
    except (json.JSONDecodeError, TypeError, ValueError):
        pass
# --- no BOM supplied: the ledger says so (every bundled fixture lacks a bom.json)
if not (art / "bom.json").exists():
    check("no bom.json in the artefact: the ledger says no BOM supplied", re.search(r"no bom|no bill of materials|bom[^\n]{0,40}not supplied", ledger_txt + out[:3000], re.I) is not None)
# --- report order: ledger, findings, matrix
if m:
    try:
        keys = list(json.loads(m.group(0)).keys()); pos = {k: i for i, k in enumerate(keys)}
        lk = next((k for k in keys if "ledger" in k.lower()), None); fk = next((k for k in keys if "finding" in k.lower()), None); mk = next((k for k in keys if k.lower() in ("matrix", "steps", "step_matrix")), None)
        if lk and fk and mk: check("the report order is ledger, findings, matrix", pos[lk] < pos[fk] < pos[mk], f"order {keys}")
    except json.JSONDecodeError:
        pass
# --- the matrix rows carry the closing sentence as a quote
quoted_rows = [r for r in step_rows if re.search(r"\"(quote|closing|closing_sentence|sentence)\"", r) or re.search(r"[\"\u201c'][^\"\u201d']{12,}[\"\u201d']", r)]
check(f"matrix rows carry a quote (the closing sentence): {len(quoted_rows)} of {len(step_rows)}", len(step_rows) > 0 and len(quoted_rows) >= min(n_steps, len(step_rows)))
check("every finding carries a quote (JSON 'quote' key or a quoted span)", (m is not None and all('"quote"' in b for b in blocks)) or sum(1 for b in blocks if re.search(r"[\"“'][^\"”']{12,}[\"”']", b)) >= max(3, len(blocks) // 2))
if graded_code: print(f"  (excluded from recall: {len(graded_code)} grader-code rows; hits among them {sum(1 for r in graded_code if hit(r))})")
bad = [r for r in rows if not r[1]]
print(f"\n{len(rows)-len(bad)}/{len(rows)} checks pass · recall all {rec_all:.2f} class {rec_cls:.2f}" + (f" missed {rec_missed:.2f}" if missed else ""))
sys.exit(1 if bad else 0)
