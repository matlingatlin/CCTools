#!/usr/bin/env python3
"""signals.py — the loop-closer. Deterministic, read-only, no deps.

Reads pipeline/metrics.jsonl + pipeline/ledgers/*.jsonl and computes the brain's
improvement signals (the objective). Prints a markdown table; with --write it rewrites
the block between the markers in BRAIN.md so read-back is DATA-DRIVEN, not from memory.

This is what turns "we log data" into "the loop optimizes on the data": every reflect/
record step runs it, so BRAIN §0 always reflects the ledgers. Rule-based on purpose —
the data-science/ML layer stays deferred until volume justifies it (see DATA.md).

Usage:  python3 pipeline/queries/signals.py          # print
        python3 pipeline/queries/signals.py --write   # print + update BRAIN.md §0 block
"""
import json
import sys
import os
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def load(p):
    rows=[]
    fp=os.path.join(ROOT,p)
    if not os.path.exists(fp): return rows
    for l in open(fp):
        l=l.strip()
        if l:
            try: rows.append(json.loads(l))
            except: pass
    return rows

metrics=[r for r in load('pipeline/metrics.jsonl') if 'wave' in r]
talents=load('pipeline/ledgers/talents.jsonl')
evals=[e for e in load('pipeline/ledgers/evals.jsonl') if e.get('talent')!='_meta']
rejections=load('pipeline/ledgers/rejections.jsonl')
proposals=load('pipeline/ledgers/proposals.jsonl')
defects=[d for d in load('pipeline/ledgers/defects.jsonl') if '_schema' not in d]
claims=[c for c in load('pipeline/ledgers/claims.jsonl') if c.get('agent_role')]

# Event-sourced state per talent. MERGE fields forward -- do not take the last row wholesale.
# A later event (e.g. `deployed`) carries no `tested`/`scenarios`, so overwriting would silently
# un-test a talent. Later NON-NULL values win; absent keys leave the earlier value standing.
latest={}
for t in talents:
    cur=latest.setdefault(t['talent'], {})
    for k,v in t.items():
        if v is not None: cur[k]=v
T=list(latest.values())

def pct(a,b): return f"{(a/b*100):.0f}%" if b else "n/a"

import glob as _glob
import re
import yaml as _yaml
# Enumerate EVERY talent category, not just skills. CLAUDE.md defines a talent as "skills, hooks,
# subagents, agents, commands"; globbing only .claude/skills/*/SKILL.md silently excluded
# .claude/agents/ from every number below -- coverage, routing and usage were all computed over a
# denominator that did not contain it, so an unmanaged unit read as full coverage. Same defect
# class as skill-stocktake counting only its own directory: a category nobody enumerates is a
# category nobody maintains, and the metric says 100% either way.
_skill_units=[(os.path.basename(os.path.dirname(q)),'skill') for q in _glob.glob(os.path.join(ROOT,'library/skills/*/SKILL.md'))]
_other_units=[]
for _cat,_pat in (('agent','library/agents/*.md'),('command','library/commands/*.md')):
    for q in _glob.glob(os.path.join(ROOT,_pat)):
        # A unit's TESTS are not a unit. Agent tests live beside the agent as <name>.evals.md, so a
        # bare *.md glob counts each agent twice -- the same "counted files, not units" defect just
        # fixed in skill-stocktake, reintroduced here by the agent-evals naming convention.
        if q.endswith('.evals.md'): continue
        _other_units.append((os.path.splitext(os.path.basename(q))[0],_cat))
unit_cat=dict(_skill_units+_other_units)
all_talents=sorted(unit_cat)
by_category=collections.Counter(unit_cat.values())
non_skill=sorted(t for t in all_talents if unit_cat[t]!='skill')

# ---- OBJECTIVE SIGNALS ----
# Coverage is computed over what EXISTS ON DISK, not over what the ledger happens to mention. A
# unit with no ledger event at all was previously invisible to this number -- neither tested nor
# untested -- so an unregistered unit could not lower coverage, and 'never written about' read
# identically to 'fine'. Anything on disk without a passing test event counts as untested.
tested_names={t['talent'] for t in T if t.get('tested')}
tested=[t for t in T if t.get('tested')]
_on_disk=set(all_talents)
coverage=(len(tested_names & _on_disk), len(_on_disk))
unregistered=sorted(_on_disk - {t['talent'] for t in T})

# BLEND is a STOCK vs FLOW metric. Backfilled history (waves <=18) dominates the aggregate and
# masks a fix that already landed, so compute both and DRIVE THE DIRECTIVE OFF THE FLOW.
def blend_of(rows):
    c=collections.Counter(e.get('kind') for e in rows)
    tot=sum(c.values())
    return c.get('normal',0), c.get('adversarial',0), c.get('negative-trigger',0), c.get('unclassified',0), tot
bf_rows=[e for e in evals if e.get('backfill')]
live_rows=[e for e in evals if not e.get('backfill')]
bf_n,bf_a,bf_g,bf_u,bf_t = blend_of(bf_rows)
lv_n,lv_a,lv_g,lv_u,lv_t = blend_of(live_rows)

sc_norm=sum(t.get('normal',0) or 0 for t in tested)
sc_adv=sum(t.get('adversarial',0) or 0 for t in tested)
sc_neg=sum(t.get('negative_trigger',0) or 0 for t in tested)
sc_tot=sum(t.get('scenarios',0) or 0 for t in tested)
sc_uncl=sc_tot-sc_norm-sc_adv-sc_neg

# verdict pass-rate (normalize synonyms; only real fail words count as failures)
def norm_verdict(v):
    if not v: return 'unparsed'
    v=str(v).lower()
    if v in ('passed','pass','ok','green','beats-baseline'): return 'passed'
    if v in ('failed','fail','red','regression'): return 'failed'
    return 'unparsed'
verd=collections.Counter(norm_verdict(t.get('test_verdict')) for t in tested)
passed=verd.get('passed',0); failed=verd.get('failed',0); unparsed=verd.get('unparsed',0)

# Yield by source_type. HARVEST is a DISPLAY grouping, not a filter: a hardcoded allowlist here
# silently dropped 13 of 25 rows -- every build wave and every curation pass -- from a table that
# read as if it covered the loop's whole output, and any NEW source_type would have vanished the
# same way, invisibly. Group everything; label the non-harvest types instead of excluding them.
HARVEST={'github','github-practitioner','github-primary','github-vendor','github-vendor-refcode','web-top-n'}
by_src=collections.defaultdict(lambda:[0,0])  # type -> [seen, kept]
for r in metrics:
    st=r.get('source_type')
    if not st: continue
    by_src[st][0]+=r.get('seen',0)
    # A harvest pass is a PRODUCER: it hands candidates to a later build wave. Scoring it by
    # `adopted` reads 0.00 for excellent work and computes to "deprioritize" on the library's
    # best source type. Count candidates when the row records them. (See LESSONS 2026-08-28.)
    by_src[st][1]+=r.get('candidates') if r.get('candidates') is not None else r.get('adopted',0)
unlisted=sorted(set(by_src)-HARVEST)

# gate rejections by reason
# REJECTIONS: the seed rows are AGGREGATE (candidate="(aggregate)") and swamp the per-candidate
# live rows. A blended count is meaningless -- report the live distribution, note the seed apart.
seed_rej=[x for x in rejections if x.get('candidate')=='(aggregate)']
live_rej=[x for x in rejections if x.get('candidate')!='(aggregate)']
by_reason=collections.Counter()
for x in live_rej:
    by_reason[x.get('reason_code','?')]+=x.get('count',1)
seed_total=sum(x.get('count',1) for x in seed_rej)
live_total=sum(x.get('count',1) for x in live_rej)

# drops (talents removed for test-failure) — none if no talent missing/dropped event
drops=[t for t in T if t.get('event')=='dropped' or t.get('test_verdict')=='failed']

# measurement coverage (are we actually measuring, not estimating?)
waves_with_time=sum(1 for r in metrics if r.get('wall_clock_s') not in (None,))
# Waves before instrumentation (<=18) CANNOT be backfilled -- counting them as a gap forever
# produces a directive nobody can act on. Measure compliance on instrumented waves only.
INSTRUMENTED_FROM=19
inst=[r for r in metrics if r.get('wave',0)>=INSTRUMENTED_FROM]
inst_with_time=sum(1 for r in inst if r.get('wall_clock_s') not in (None,))
proposals_open=sum(1 for p in proposals if p.get('outcome')=='pending')
proposals_resolved=[p for p in proposals if p.get('outcome') in ('approved','rejected')]

# blend deviation from ~50/50 normal:clever target (the objective on test quality)
clever=sc_adv+sc_neg
blend_ok = sc_tot>0 and abs(sc_norm/sc_tot - 0.5) <= 0.15
live_blend_ok = lv_t>0 and abs(lv_n/lv_t - 0.5) <= 0.15

# --- USAGE & ROUTING (are talents findable at the right time, and do they get used?) ---
# meta/loop talents run BY the piano loop itself; disuse of DOMAIN talents in-loop is by design
META={'skill-scout','eval-harness','agent-surface-security-audit','deep-reading','factory','writing-skills',
      'library-curator','research-scout','wave-reflect','talent-deploy','skill-stocktake','skill-description-optimizer',
      'writing-plans','piano','loop-design-check','verification-before-completion'}
used=collections.Counter()
for r in metrics:
    for t in r.get('talents_used',[]): used[t]+=1
used_set=set(used)
meta_talents=[t for t in all_talents if t in META]
domain_talents=[t for t in all_talents if t not in META]
meta_used=sum(1 for t in meta_talents if t in used_set)
# routing coverage: every talent must be findable in the capability map or ROUTING (else it can't be selected)
_cmap=open(os.path.join(ROOT,'CLAUDE.md')).read() if os.path.exists(os.path.join(ROOT,'CLAUDE.md')) else ''
_routing=open(os.path.join(ROOT,'pipeline/ROUTING.md')).read() if os.path.exists(os.path.join(ROOT,'pipeline/ROUTING.md')) else ''
_wired=_cmap+_routing
unrouted=[t for t in all_talents if t not in _wired]
# DEPLOY GAP: routing says a talent is FINDABLE; only a reload makes it LIVE. A shipped talent
# with no `deployed` event is wired but possibly not activated -- a gap only memory was closing.
born={t['talent'] for t in talents if t.get('event') in ('born','snapshot')}
deployed={t['talent'] for t in talents if t.get('event')=='deployed'}
shipped_recent={t['talent'] for t in talents if t.get('event')=='born'}
undeployed=sorted(shipped_recent - deployed)
# TIME-TO-DETECT: is the curator catching defects faster? null lived_waves = never tested until now.
# Test `is not None`, NOT truthiness: lived_waves 0 is the FASTEST possible detection (caught in the
# wave the talent was born), and a truthiness test files that best-case row under "since inception",
# which is the worst-case bucket. Scored the best outcome as the worst until 2026-08-28.
ttd=[d['lived_waves'] for d in defects if d.get('lived_waves') is not None]
ttd_inception=sum(1 for d in defects if d.get('lived_waves') is None and d.get('talent'))

lines=[]
lines.append("| Signal | Direction wanted | Reading (from ledgers) |")
lines.append("| --- | --- | --- |")
lines.append(f"| Test coverage (tested / total) | **up → 100%** | {coverage[0]}/{coverage[1]} = {pct(*coverage)} |")
lines.append(f"| Test verdict pass-rate | **stay high** | {passed} passed · {failed} failed"+(f" · {unparsed} verdict-line-not-parsed (seed)" if unparsed else "")+f" of {len(tested)} |")
lines.append(f"| Test blend · LIVE (scenarios written since instrumentation) | **~50 : 50** | normal {pct(lv_n,lv_t)} · clever {pct(lv_a,lv_t)} · neg {pct(lv_g,lv_t)} of {lv_t} — {'BALANCED' if live_blend_ok else 'SKEWED: too few normal'} |")
lines.append(f"| Test blend · backfilled history (context only, cannot be changed) | n/a | normal {pct(bf_n,bf_t)} · clever {pct(bf_a,bf_t)} of {bf_t} — the aggregate's skew lives here |")
lines.append(f"| Talents dropped (test-failed, unfixable) | **~0 (fix, don't drop)** | {len(drops)} |")
lines.append("| Gate rejections by reason · LIVE (per-candidate) | learn the waste shapes | "+("; ".join(f"{k}={v}" for k,v in by_reason.most_common())+f" ({live_total} total) |" if by_reason else "none |"))
lines.append(f"| Gate rejections · seed rows (aggregate, no per-candidate reason) | context only | {seed_total} across {len(seed_rej)} aggregate rows — excluded from the distribution above |")
for st in sorted(by_src):
    seen,kept=by_src[st]
    if st in HARVEST:
        lines.append(f"| Harvest yield · {st} | **up** | {kept}/{seen} kept = {pct(kept,seen)} |")
    else:
        # NOT a yield: these passes are not measured by "kept out of seen", and the
        # seek-more/deprioritize rule must never be applied to them. A curation pass produces
        # talents tested and defects fixed; reading it as 0% yield would compute to
        # "deprioritize the curator" -- the same producer-vs-consumer error, third variant.
        lines.append(f"| Pass output · {st} (NOT a yield — rule 1 does not apply) | context only | {kept}/{seen} — see the note below |")
if unlisted:
    lines.append(f"| Work types outside the harvest grouping | listed, never scored | {', '.join(unlisted)} — shown so a new source_type cannot vanish silently |")
lines.append(f"| Measurement coverage · instrumented waves (>={INSTRUMENTED_FROM}) | **100%** | {inst_with_time}/{len(inst)} — waves 1-{INSTRUMENTED_FROM-1} predate instrumentation and can never be filled |")
lines.append(f"| Human-gate proposals (resolved / open) | track hit-rate | {len(proposals_resolved)} resolved · {proposals_open} open |")
lines.append(f"| Deploy gap (shipped but never reloaded) | **0 — routing is findable, deploy is LIVE** | {len(undeployed)}"+(f" NOT deployed: {', '.join(undeployed)}" if undeployed else " — every shipped talent has a deployed event")+" |")
if ttd:
    import statistics as _st
    # DEFECT FAMILIES: make defects predictive, not merely counted. The silent share is the one that
# matters -- a silent defect cannot be found by reading, only by running a positive control.
_fam=collections.Counter(d.get('family') for d in defects if d.get('family'))
_silent=sum(1 for d in defects if d.get('silent'))
if _fam:
    lines.append("| Defect families (where to look next) | learn the recurring shapes | "+"; ".join(f"{k}={v}" for k,v in _fam.most_common())+" |")
    lines.append(f"| Defects that fail SILENTLY (absence looks like success) | **down** | {_silent}/{len(defects)} = {pct(_silent,len(defects))} — these need a positive control, not a reading |")
# AGENT RELIABILITY: we grade the talents with agents whose accuracy was never measured.
if claims:
    _cv=collections.Counter(c.get('verdict') for c in claims)
    _conf=_cv.get('confirmed',0)
    lines.append(f"| Independent-agent claim precision | **high, and MEASURED** | {_conf}/{len(claims)} = {pct(_conf,len(claims))} confirmed · {_cv.get('partial',0)} partial (right finding, wrong mechanism) · {_cv.get('refuted',0)} refuted |")
# CONSTANTS DRIFT: pipeline/CONSTANTS.md is the one place a pinned value lives. This does not
# rewrite it -- it CHECKS the live library against what that file claims, so a constant cannot
# quietly stop being true. A constants file nothing verifies is a second copy that drifts.
_const_path=os.path.join(ROOT,'pipeline/CONSTANTS.md')
if os.path.exists(_const_path):
    _ct=open(_const_path).read()
    _cap=int(re.search(r'`DESCRIPTION_CAP_CHARS`\s*\|\s*\*\*(\d+)\*\*',_ct).group(1)) if re.search(r'`DESCRIPTION_CAP_CHARS`\s*\|\s*\*\*(\d+)\*\*',_ct) else None
    if _cap:
        _over=[]
        for _q in _glob.glob(os.path.join(ROOT,'library/skills/*/SKILL.md')):
            _L=open(_q).read().splitlines()
            _c=next((i for i,l in enumerate(_L[1:],1) if l.strip()=='---'),None)
            if _c is None: continue
            try: _fm=_yaml.safe_load("\n".join(_L[1:_c]))
            except Exception: continue
            if _fm and len(_fm.get('description','') or '')>_cap: _over.append(os.path.basename(os.path.dirname(_q)))
        lines.append(f"| Descriptions over the pinned cap ({_cap}) | **0** | {len(_over)} of {len(_glob.glob(os.path.join(ROOT,'library/skills/*/SKILL.md')))}"+(f" — {', '.join(sorted(_over)[:4])}{'…' if len(_over)>4 else ''}" if _over else "")+" |")
lines.append(f"| Time-to-detect (waves a defect lived before an independent test caught it) | **down** | median {_st.median(ttd):.0f} of {len(ttd)} measurable · {ttd_inception} more existed since inception (untested until now) |")
if unregistered:
    lines.append(f"| Units on disk with NO ledger history | **0** | {len(unregistered)}: {', '.join(unregistered)} — never born/tested/deployed in any ledger |")
lines.append("| Library composition (every talent category) | all categories managed | "+("; ".join(f"{k}={v}" for k,v in sorted(by_category.items()))+(f" — non-skill units: {', '.join(non_skill)}" if non_skill else "")+" |"))
lines.append(f"| Routing coverage (findable when needed) | **100% (else can't be selected)** | {len(all_talents)-len(unrouted)}/{len(all_talents)} in map/ROUTING"+(f" — {len(unrouted)} UNROUTED" if unrouted else " — all wired")+" |")
lines.append(f"| Meta/loop-talent usage (used in a wave) | **most should fire** | {meta_used}/{len(meta_talents)} of the loop's own talents |")
lines.append(f"| Domain talents used in-loop | n/a — cross-project, no in-loop signal | {len([t for t in domain_talents if t in used_set])}/{len(domain_talents)} (disuse in-loop is BY DESIGN, never a prune trigger) |")

table="\n".join(lines)

# derived directives (the "what to do about it")
directives=[]
if not live_blend_ok and lv_t:
    directives.append(f"- LIVE test blend is {pct(lv_n,lv_t)} normal vs ~50% target → next TEST/curate passes ADD normal/representative scenarios, not more traps.")
elif lv_t:
    directives.append(f"- Test blend is HEALTHY on live work ({pct(lv_n,lv_t)} normal of {lv_t} scenarios). The library aggregate still reads {pct(sc_norm,sc_tot)} because {bf_t} backfilled scenarios dominate it — that is history, not a defect to fix. Do NOT add normal scenarios to correct the aggregate.")
if coverage[0]<coverage[1]:
    # Untested = on disk without a passing test event. Reading it off the ledger alone missed
    # units with no ledger row at all -- the very case the disk-based denominator exists to catch.
    un=sorted(_on_disk - tested_names)
    directives.append(f"- {coverage[1]-coverage[0]} untested ({', '.join(un[:6])}{'…' if len(un)>6 else ''}) → curator/TEST authors evals for these first.")
if inst_with_time<len(inst):
    directives.append(f"- {len(inst)-inst_with_time} INSTRUMENTED waves lack measured time → every wave from {INSTRUMENTED_FROM} on must write wall_clock_s.")
if undeployed:
    directives.append(f"- {len(undeployed)} shipped talent(s) have no `deployed` event ({', '.join(undeployed[:4])}) → run talent-deploy + register_repo_root. Routing makes a talent findable; only the reload makes it live.")
if unrouted:
    directives.append(f"- {len(unrouted)} talents UNROUTED ({', '.join(unrouted[:6])}{'…' if len(unrouted)>6 else ''}) → add to CLAUDE.md capability map / ROUTING so they can be selected at the right time (a talent nothing routes to never fires).")
if not directives:
    directives.append("- All tracked signals within target; deepen coverage on the thinnest suites.")

# Directives from the two perishable stores.
try:
    if _cap and _over:
        directives.append(f"- {len(_over)} description(s) exceed CONSTANTS.md's pinned cap of {_cap}. That number is corroborated by measurement (44 shipped skills on this machine: max 982, none above 1024), so the library is over the WALL, not a guideline. Trimming a description changes routing -- treat each as an edit with a trigger check, never a mechanical truncation.")
except NameError:
    pass
if _fam:
    _top=_fam.most_common(1)[0]
    directives.append(f"- Most common defect family is {_top[0]} ({_top[1]} of {len(defects)}) -> when auditing, look for THAT shape first; a ranked taxonomy is a search order, not a tally.")
if defects and _silent/len(defects) > 0.5:
    directives.append(f"- {pct(_silent,len(defects))} of defects fail SILENTLY (absence looks identical to success). Reading a file cannot find these: every audit must RUN the method's own search/enumeration and confirm a known-present item comes back (a positive control).")
if claims:
    _unver=[c for c in claims if not c.get('verified_how')]
    if _unver:
        directives.append(f"- {len(_unver)} claim(s) recorded with no `verified_how` -> record WHAT was checked, not just the outcome; an unverified claim acted on is indistinguishable from a verified one.")
    if len(claims) < 25:
        directives.append(f"- Claim precision rests on {len(claims)} claims (seeded from wave 27 triage records; earlier waves are not reconstructable). Treat the number as provisional until ~25-30 and keep logging every claim at verification time.")
out=f"{table}\n\nDerived directives (recomputed):\n"+"\n".join(directives)
print(out)

if '--write' in sys.argv:
    bp=os.path.join(ROOT,'pipeline/BRAIN.md')
    txt=open(bp).read()
    A,B="<!-- SIGNALS:auto (computed by pipeline/queries/signals.py --write) -->","<!-- /SIGNALS:auto -->"
    block=f"{A}\n{out}\n{B}"
    if A in txt and B in txt:
        pre=txt[:txt.index(A)]; post=txt[txt.index(B)+len(B):]
        open(bp,'w').write(pre+block+post)
        print("\n[written to BRAIN.md §0 signal block]")
    else:
        print(f"\n[markers not found in BRAIN.md — add:\n{A}\n{B}\nto the §0 signals area, then re-run --write]")
