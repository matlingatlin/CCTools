# Eval cases executed · catalog-budget, tenant-isolation

**Date:** 2026-08-26. First execution of any eval case in this repository.

Six of twenty-seven skills carry named eval cases — 53 in total. None had ever been run. The
twenty-six ablations run today measure whether a skill changes what a model *says*; these cases
mostly ask whether an *implementation* obeys a rule, and that is the half nobody had executed.

Fifteen cases were taken: `catalog-budget` E1–E7 and `tenant-isolation` E1–E8.

Two things about the environment, established before classifying anything rather than assumed:

- **The code the skills cite is real and present.** `tenant-isolation` cites
  `apps/api/prisma/schema.prisma`, `auth/workspace-scope.ts`, `build.service.ts:517-525` and
  `library/verification/client.ts`. None of these are in `/home/user/scio` — that repository holds
  docs and skills only. They are all in **`/home/user/hello-world`**, the predecessor codebase, and
  every static case runs against it.
- **A real Postgres is available.** No server was running and `docker` is absent, but
  `@electric-sql/pglite` — the engine `verification/client.ts` is written for — installs and runs:

  ```
  $ node smoke.mjs
  PostgreSQL 18.3 (PGlite 0.5.8) on wasm32-unknown-emscripten, ... 32-bit
  ```

  So the RLS cases were **not** written off as "no Postgres here". Three of them ran.

---

## Summary

| | RUNNABLE | BLOCKED | NOT A TEST |
|---|---:|---:|---:|
| `catalog-budget` E1–E7 | 3 | 2 | 2 |
| `tenant-isolation` E1–E8 | 6 | 1 | 1 |
| **total** | **9** | **3** | **3** |

Among the nine runnable:

| Case | Outcome |
|---|---|
| `catalog-budget` E1 · discovery surface | **FAIL (reproduction)** — morning figure reproduces to the byte; evening figure is 30 bytes wrong, and the named finding is false |
| `catalog-budget` E6 · three counts | **PASS**, with two findings — one predicted, one new |
| `catalog-budget` E7 · the ratchet | **FAIL** — nothing refuses, at any level |
| `tenant-isolation` E1 · replay reproduction | **PASS as a defect reproduction** — the unguarded path is confirmed in production code; the HTTP half is blocked |
| `tenant-isolation` E2 · scoped-model completeness | **FAIL (counts)** — the defect is real, every headline number in the case is wrong |
| `tenant-isolation` E3 · `SET LOCAL` outside a transaction | **PASS** — reproduced on real Postgres; the no-op leaks every row |
| `tenant-isolation` E4 · a double stricter than production | **PASS** — `FakeScope` refuses what production allows |
| `tenant-isolation` E5 · zero rows per tenant-scoped table | **PASS on the harness, FAIL on the corpus** — no generated app carries a policy to test |
| `tenant-isolation` E8 · the gate declares its own scope | **PASS** — both predicted verdicts hold |

**The three NOT A TESTs are the most useful result of the pass**, and two of them
(`catalog-budget` E2, E3) are cases whose two halves are true by arithmetic: nothing in the corpus
or the code could have made them fail. They are exactly the defect `testing` §1 warns about in
other people's suites, written by the process that wrote that warning.

**One rule has no case at all:** `tenant-isolation` §4b — `USING` versus `WITH CHECK`, added today —
is not covered by E1–E8. Detail at the end of the tenancy section.

---

# `catalog-budget`

## E1 — Measure this repository's own discovery surface

> *"Sum `byteLength(name) + byteLength(description)` from the frontmatter of every
> `.claude/skills/*/SKILL.md`; report bytes, `ceil(bytes/4)` token-equivalents, the per-entry
> distribution, and the dominant entry."*

**Classification · RUNNABLE.** The only case in either skill that needs nothing but this
repository, and the reason `catalog-budget` is not theoretical.

**What was run.** A frontmatter parser over `/home/user/scio/.claude/skills/*/SKILL.md`, summing
`len(name_bytes) + len(description_bytes)`. Every description in the corpus is a single line, so
there is no multi-line-folding ambiguity in the parse. Then the same script over
`git archive` extractions of every revision that touched `.claude/skills`, to test whether the
skill's own two recorded rows reproduce.

**Today's number:**

```
root: /home/user/scio/.claude/skills
entries: 27
bytes:   18320
token-equivalents ceil(bytes/4): 4580
mean bytes/entry: 678.5
over 260 B per-entry cap: 27 of 27

dominant entry: testing at 1025 bytes
```

Top of the distribution:

```
entry                             name   desc   total
testing                              7   1018    1025
architecture                        12    895     907
ais-grounding                       13    879     892
ontoagent-elicitation               21    853     874
gate-verdicts                       13    846     859
tenant-isolation                    16    821     837
...
graph-guard                         11    298     309
```

**Do the skill's own figures reproduce?** One does, exactly. One does not.

| | Entries | Bytes | TE | Source |
|---|---:|---:|---:|---|
| skill's "morning" | 17 | 9,275 | 2,319 | `catalog-budget` §6 E1 |
| **measured at `19b3827`** | **17** | **9,275** | **2,319** | this run — **exact** |
| skill's "evening" | 27 | 18,212 | 4,553 | `catalog-budget` §6 E1 |
| **measured at `b5b6a4f`** | **27** | **18,182** | **4,546** | this run — **30 bytes short** |
| today, `HEAD` | 27 | 18,320 | 4,580 | this run |

`b5b6a4f` is the commit that introduced the skill carrying the table, so it is the right tree to
compare against. The full sweep:

```
e62b04f 22:59  entries: 27 bytes: 18320 TE: 4580
b5b6a4f 20:35  entries: 27 bytes: 18182 TE: 4546     <- the E1 "evening" row was written here
19b3827 19:53  entries: 17 bytes:  9275 TE: 2319     <- the E1 "morning" row reproduces exactly
19c255f 18:35  entries: 17 bytes:  9429 TE: 2358
81c7974 17:52  entries: 16 bytes:  8898 TE: 2225
d56d1a7 17:27  entries: 16 bytes:  8502 TE: 2126
```

**The 30 bytes have one cause, and it is the same entry as the case's headline finding.** E1 states:

> *"`testing`'s description is 1,046 characters — over the 1,024 limit `docs/next/SKILLS.md` states
> as the spec's own maximum."*

Measured directly at every revision in which the file has ever existed:

```
b5b6a4f  bytes=1018  chars=1016  under
45f4636  bytes=939   chars=937   under
19b3827  bytes=684   chars=682   under
d56d1a7  bytes=684   chars=682   under
```

`testing`'s description has **never** been 1,046 characters. Its maximum in git history is
**1,016**, which is *under* `SKILLS.md:33`'s `≤1,024 chars`. And 1,046 − 1,016 = **30** — the entire
discrepancy in the corpus total. One entry was mis-measured by 30 characters; that error set the
recorded total (18,182 → 18,212), the recorded TE (4,546 → 4,553), and produced a spec violation
that does not exist.

**Two further checks on the case's own prose:**

- *"Two measurements, both 2026-08-26, six hours apart."* The 9,275-byte state cannot predate
  `19c255f` at 18:35 (which measures 9,429), and the 18,182-byte state begins at `b5b6a4f`, 20:35.
  The two trees are **at most two hours apart**, not six.
- *"The always-loaded surface grew 96% in one working day."* This **holds**: 9,275 → 18,182 is
  +96.0%. The headline claim survives its own arithmetic error.

**Outcome · FAIL, as a reproduction.** The method is sound and the case is worth keeping — it is
the only instrument in the repo that would have caught any of this. But the numbers it published
were not re-derived before being written down, in a skill whose §2.4 is *"re-derive it, do not trust
the number."* The corpus is now 18,320 bytes / 4,580 TE over 27 entries, all 27 over the 260-byte
per-entry cap, and gstack still carries 53 entries at 4,420 bytes.

---

## E2 — The floor catches what the ceiling cannot

> *"Empty one entry's description to the empty string and re-run E1. A check that only sums bytes
> **passes**. Add the non-empty floor; it must fail, and the failure must name the entry."*

**Classification · NOT A TEST.** Both halves are true by arithmetic before anything is run, and the
case's premise — that a budget check exists — is false.

Emptying a description strictly *reduces* the sum, so an under-ceiling check cannot fail; and a
floor whose definition is "description length > 0" cannot pass on a zero-length description. There
is no input to this case that produces any other result. Separately: `/home/user/scio` contains no
budget constant, no ceiling, no check and no CI (`grep` for `BUDGET|CATALOG_BUDGET|TOKEN_EQUIVALENT`
across `scripts/`, `hooks/`, `.claude/` and `.git/hooks/` returns nothing; there is no `.github/`).
So the ceiling that "passes" has to be invented by whoever runs the case, and its value decides the
result.

**Run anyway, on a copy** at `$SCRATCH/corpus/skills`, with the ceiling set to 18,400 — the smallest
round number above today's measured surface. `graph-guard`'s description (312 bytes on the line) was
replaced with the empty string.

Before:

```
CHECK A  aggregate byte-sum ceiling  (18320 bytes vs ceiling 18400)
CHECK A  PASS  18320 <= 18400  (headroom 80 bytes)
CHECK B  non-empty description floor  (27 entries)
CHECK B  PASS  every entry has a non-empty description
exit=0
```

After emptying `graph-guard`:

```
CHECK A  aggregate byte-sum ceiling  (18022 bytes vs ceiling 18400)
CHECK A  PASS  18022 <= 18400  (headroom 378 bytes)
CHECK B  non-empty description floor  (27 entries)
CHECK B  FAIL  entry 'graph-guard': description is empty (0 bytes). An emptied
         description is never matched at discovery; it passes every under-budget
         check while being unreachable.
exit=1
```

**Outcome · NOT A TEST.** The demonstration is real and it is the right demonstration — the
ceiling did not merely pass, it got *happier*, headroom improving from 80 bytes to 378 while an
entry became unreachable. That is a good illustration of §2.3. It is not a test of anything in this
repository, because nothing in this repository was measured: both checks were written for the
occasion, and both verdicts follow from their own definitions.

**To become a test** this case needs a committed check with a committed ceiling. Then E2 stops
asserting arithmetic and starts asserting that *our* check has the floor — which is a claim that
could be false.

---

## E3 — The shrink floor catches a body strip

> *"Take one `SKILL.md`, truncate it to 250 bytes, re-run against a frozen baseline. A per-file
> noise floor of 200 bytes passes it. The ×0.80 shrink floor must fail it, and the message must name
> the diagnosis, not the ratio."*

**Classification · NOT A TEST**, for the same reason as E2, plus one worse one.

The arithmetic is fixed before the run: 250 > 200, so a noise floor of 200 cannot flag the file;
and 250/6,965 = 0.036 < 0.80, so a shrink floor cannot pass it. The third clause — *"the message
must name the diagnosis"* — is worse than tautological, it is **unfalsifiable by construction**: no
such check exists in this repo, so whoever runs the case writes the failure message and then grades
it. There is no way to fail a requirement on text you author in the same step.

**Run anyway.** `graph-guard/SKILL.md` (6,965 bytes) truncated to its first 250 bytes on a copy, with
a baseline frozen from the pristine tree.

Noise-floor-only check, on the truncated corpus:

```
noise floor = 200 bytes; files below it: 0
graph-guard is 250 bytes -> NOT FLAGGED
NOISE-FLOOR-ONLY CHECK: PASS
```

Shrink floor ×0.80 against the frozen baseline, same corpus:

```
FAIL  graph-guard: 6965 B -> 250 B.
      A file this much smaller is not an edit. Diagnosis: accidental body strip —
      a resolver returning empty, a template losing a section, a truncated write.
      Restore the content or, if the removal is deliberate, re-freeze the baseline
      in the same commit and say which section went.
  ok  graphify                 41276 -> 41276 B
  ok  ontoagent-elicitation    13351 -> 13351 B
...
result: 1 failure(s)
exit=1
```

**Outcome · NOT A TEST.** A 99.6% content loss passing one check and failing the other is a clean
illustration of why gstack carries both. But nothing was measured that could have come out
differently, and the one clause with real content — *name the diagnosis, not the ratio* — cannot be
evaluated by the person who writes the message. That clause belongs in a review of a **committed**
failure message, not in a case run against a check invented at run time.

---

## E4 — The split is a fixed point

> *"Run the splitter twice over the same description. Second run: `lead` identical, routing prose
> empty."*

**Classification · BLOCKED.**

**What must be built:** a splitter. `applyCatalogTrim` is gstack's; grep across `/home/user/scio` for
`applyCatalogTrim|catalogTrim|routingProse|catalog-mode` finds mentions in exactly two places —
`docs/mined/PASS2-GSTACK-TESTS.md`, where it was mined, and `catalog-budget/SKILL.md` §3, where it is
described. There is no implementation, and no build step that would run one.

**Would it then be a good test of it?** Yes, and it is the right first test — idempotency is the
property a generator that runs every build must have, and a fixed-point assertion is cheap and
catches the whole class in one line. It is also the case that most needs writing before the code, so
that the splitter is designed to be a fixed point rather than patched into one.

---

## E5 — The decision is not behind the load

> *"For any two-tier entry, assert that the text deciding whether to load the body appears at an
> **earlier position** than the load itself. Assert on position, not on presence."*

**Classification · BLOCKED**, and by the same absence as E4 — but the block is sharper: there is no
two-tier entry in the corpus to assert *about*.

Every `## ` heading across all 27 skills, counted:

```
     20 ## 1 · Source
     11 ## 4 · Eval
      8 ## 2 · Method, in the form we use it
      6 ## 5 · When this skill is the wrong tool
      ...
```

Not one `## When to invoke this skill`. Zero entries are split, so the set the case quantifies over
is empty — and a `for all` over an empty set is vacuously true, which is the third way a case can
fail to be a test. Classified BLOCKED rather than NOT A TEST because the emptiness is a missing
implementation, not a defect in the case's design.

**What must be built:** the §3 split — a generator that moves routing prose out of frontmatter into a
body section, and the frontmatter/body distinction in the loader that makes the move mean anything.

**Would it then be a good test of it?** Yes, and it is the most valuable of the four blocked cases,
because it is the one whose obvious implementation is wrong. A substring check on the always-loaded
half passes when the directive sits after the STOP that reads it; the case explicitly demands
earliest-position-of-use instead. That distinction is not something an implementer arrives at
unprompted, which is what an eval case written ahead of its code is for.

---

## E6 — Three counts, not one

> *"One census module returns physical files, distinct entries and addressable entries. Assert
> `addressable ≤ physical` and that every addressable entry resolves back to a physical file."*

**Classification · RUNNABLE**, with a caveat recorded honestly: the *assertions* are close to
tautological on a corpus with no symlinks and no aliases — `addressable ≤ physical` can only be
violated by a name appearing without a file, which needs a router alias this corpus does not have.
What makes the case runnable and worth running is its second half, the resolution check and the
census itself, and the finding it was written to expose.

**What was run.** `scripts/skills-index.py` (the repository's own indexer), plus a census enumerating
the three counts separately.

```
physical files      : 27
distinct entries    : 27  (symlink-deduped)
addressable entries : 27  (unique frontmatter names)

RELATION 1  addressable <= physical : 27 <= 27 -> HOLDS
RELATION 2  every addressable entry resolves to a physical SKILL.md : HOLDS

duplicate names     : none
symlinks            : none
physical files that are NOT fully-formed registry entries: 1
   graphify: missing ['layer', 'phase', 'status']
```

`scripts/skills-index.py`, ending its output:

```
  — UNPLACED —
      graphify                 ?           → ?         ?
```

**The predicted finding reproduces.** E6 states it in advance: *"`graphify` carries no `layer`,
`phase` or `status`, so `scripts/skills-index.py` reports it UNPLACED — a physical file that is not
a fully-formed registry entry."* Confirmed, and it is still the only one of 27.

**A second finding, not predicted, which running the case turned up.** Both plugin manifests report
a count, and both are wrong:

```
.claude-plugin/marketplace.json:
  "description": "Scio's build knowledge: sixteen skills, ..."
.claude-plugin/plugin.json:
  "description": "Scio's build knowledge: the sixteen skills, ..."
```

**Sixteen, against 27 physical files, 27 distinct entries and 27 addressable entries.** This is
precisely §4's claim — *"a system that reports one number is reporting the wrong one"* — except that
the single number here is not merely the wrong one of three, it is stale by eleven. It is also the
number a user installing the plugin reads.

**Outcome · PASS.** Both relations hold, the predicted finding reproduces, and the case produced one
new finding that no other check in the repository would have surfaced.

---

## E7 — The ratchet is enforced, not documented

> *"Change a budget constant without changing its derivation comment in the same commit. Something
> must refuse. If nothing does, the budget is a suggestion."*

**Classification · RUNNABLE.** The case is self-executing: it names the action, and the pass
condition is that *something* refuses. It can be run even though there is no budget constant — the
absence is itself part of the answer.

**What was run.** A throwaway clone of `/home/user/scio` in the scratchpad. A budget constant was
created **with** the derivation block §2.4 describes, committed, then raised without touching the
derivation, and committed again. Nothing in the real repository was modified.

```
$ git clone -q /home/user/scio $SCRATCH/ratchet
hooks in the clone:
```

The clone inherits no hooks — and the source repository has none that could refuse either. Its
`.git/hooks/` holds exactly two, both installed by `graphify`:

```
-rwxr-xr-x post-checkout
-rwxr-xr-x post-commit
```

Both are `post-`. There is no `pre-commit`, no `pre-push`, and no `.github/` directory: `ls
.git/hooks/pre-commit .git/hooks/pre-push .github` returns three `No such file or directory`. The
only configured hook in `hooks/hooks.json` is a `SessionStart` graph rebuild.

The run:

```
$ git commit -m "chore: add a budget constant with its derivation"
baseline commit: OK

--- now raise the constant and leave the derivation comment untouched ---
 scripts/budget.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
[main 3a0c889] chore: raise the budget
 1 file changed, 1 insertion(+), 1 deletion(-)
exit=0

--- did anything refuse? ---
3a0c889 chore: raise the budget
4:#   measured:   2026-08-26, 27 entries, 18,320 bytes
6:CATALOG_BUDGET_TOKEN_EQUIVALENTS = 9999
```

The budget more than doubled, 4,580 → 9,999. The derivation directly above it still says 27 entries
and 18,320 bytes. The commit was accepted, exit 0, no warning.

**Outcome · FAIL.** Nothing refuses, at any level — no `pre-commit`, no `pre-push`, no CI. The
ratchet exists as three paragraphs in §2.4 and as a quoted failure message belonging to another
repository. In the case's own words: **the budget is a suggestion.** It is also, today, not even
that, since there is no constant to suggest anything.

---

# `tenant-isolation`

All static cases run against **`/home/user/hello-world`** — the predecessor codebase every code
position in the skill refers to. Every position cited in §3.1 was checked, and **all of them are
exact**: `build.service.ts:517` is `if (idempotencyKey) {`, `:518` the `buildFor` call, `:525` the
ownership check; `ensureCanStart` is at `:195` with its early return at `:202` and its ownership
check at `:233`; `workspace-scope.ts:62` is `if (!WORKSPACE_SCOPED_MODELS.has(model)) return args;`;
`build.controller.ts:76` is `@Headers("idempotency-key")`. A skill that cites line numbers and gets
them right is not the norm, and it is worth saying before the numbers that do not hold up.

**Baseline for everything below** — the API suite, run first, so no case is reported against an
already-broken tree:

```
$ npx vitest run
 ✓ test/build.e2e.spec.ts (44 tests) 316ms
 ✓ test/tenant-discipline.spec.ts (2 tests) 12ms
 ✓ test/workspace-scope.spec.ts (9 tests) 9ms
 ...
 Test Files  12 passed (12)
      Tests  135 passed (135)
```

**135 tests, twelve files, all green, and no database is involved at any point.** Hold that next to
E1 and E4.

---

## E1 — The replay reproduction

> *"Two workspaces, one project UUID and one idempotency key. Call the build endpoint from the wrong
> workspace with the matching key. **Expected: 404.** Today it returns the other tenant's `git_sha`,
> honest-status summary, `total_cost_usd` and `total_tokens`."*

**Classification · RUNNABLE in part.** The mechanism is executable against production code today.
The HTTP half is not: it needs the Nest app on a real Postgres with two seeded workspaces, and
`prisma` cannot speak to pglite over a socket without `@electric-sql/pglite-socket`, which the repo
does not carry. The endpoint call is therefore **BLOCKED**; the defect it is meant to expose is not.

**What was run.** The production `applyWorkspaceScope` — imported, not re-implemented — against the
exact arguments `buildFor` passes.

```
$ npx vitest run test/zz-e4-double-vs-production.spec.ts

  double     -> null
  production -> {"where":{"projectId":"p-theirs","idempotencyKey":"k"}}
  production added a workspace filter? false
```

And the code path, read at source:

```ts
// build.service.ts:517-525
if (idempotencyKey) {
  const already = await this.buildFor(workspaceId, projectId, idempotencyKey);
  if (already) {
    await emit("finished", this.replayOf(workspaceId, projectId, already));
    return;                                     // :522 — returns here
  }
}

const project = await this.project(workspaceId, projectId);   // :525 — the ownership check
```

```ts
// build.service.ts:365-373
private async buildFor(workspaceId, projectId, idempotencyKey) {
  return this.client(workspaceId).buildVersion.findFirst({
    where: { projectId, idempotencyKey },       // no workspace anywhere in the predicate
  });
}
```

`BuildVersion` is not in `WORKSPACE_SCOPED_MODELS`, so `applyWorkspaceScope` returns at `:62` and
`workspaceId` selects the client without entering the query. The key is client-supplied
(`build.controller.ts:76`). The same shape is at `ensureCanStart` `:202`, ownership at `:233`.

**Outcome · PASS as a defect reproduction, BLOCKED as an endpoint test.** The unguarded ordering is
confirmed in production code and the scope is confirmed to be a no-op on the model in question, on
the real function. What could not be produced is the HTTP response body — so *"today it returns the
other tenant's `git_sha`, … `total_cost_usd` and `total_tokens`"* remains an inference from
`replayOf`, not something this pass observed.

**To run the case as written:** a Postgres reachable by Prisma (`docker compose up db`, or
`@electric-sql/pglite-socket`), `prisma migrate deploy`, and a two-workspace seed. Everything else
is already in the repo.

---

## E2 — Scoped-model completeness

> *"Enumerate every model in `schema.prisma` and every model named in `WORKSPACE_SCOPED_MODELS`. For
> each model in neither set, report every non-test query site that touches it. **Expected today:
> eight models unscoped, 26 call sites, 24 of which open with an ownership check.**"*

**Classification · RUNNABLE.** Three published numbers, all falsifiable. This is the best-formed
case in either skill.

**What was run.** `grep -c '^model '` over `schema.prisma`; the `WORKSPACE_SCOPED_MODELS` set read
from source; then a script attributing every query site on an unscoped model to its enclosing method
and checking whether an ownership call precedes it in that method.

**Models — this number reproduces.** 14 declared, 6 scoped, 8 unscoped:

```
Workspace  User  Project  Message  SpecVersion  DesignVersion  BuildJob
BuildVersion  Deployment  ReferenceAsset  ReferenceEmbedding  UsageEvent
Notification  AuditLog                                    count: 14

WORKSPACE_SCOPED_MODELS = { Project, UsageEvent, Notification, AuditLog, User, BuildJob }   -> 6
unscoped                = { Workspace, Message, SpecVersion, DesignVersion,
                            BuildVersion, Deployment, ReferenceAsset, ReferenceEmbedding }  -> 8
```

**Call sites — this number does not.** 27, not 26:

```
workspace: 1   message: 3   specVersion: 10   designVersion: 7   buildVersion: 6
deployment: 0  referenceAsset: 0  referenceEmbedding: 0
total non-test sites: 27
```

**And the 24 does not survive under any unit I could construct.** Attributed per method:

```
file:line                            method            ownership check first?
spec/spec.service.ts:50              list              yes
spec/spec.service.ts:101,115,119     approve           yes
spec/spec.service.ts:192,248,252     amend             yes
design/design.service.ts:92          currentSpec       NO
design/design.service.ts:107         currentDesign     NO
design/design.service.ts:165,170,174 record            NO
design/design.service.ts:212         list              yes
design/design.service.ts:511         restore           yes
build/build.service.ts:65            list              yes
build/build.service.ts:96,105        latest            yes
build/build.service.ts:370           buildFor          NO
build/build.service.ts:528,541       run               yes
build/build.service.ts:698           designToPromote   NO
build/build.service.ts:728,732       persist           NO
intake/intake.service.ts:211         messages          NO
intake/intake.service.ts:225,263     step              yes
auth/provisioning.service.ts:27      getOrCreate       NO

total call sites on unscoped models : 27
with an ownership check first       : 16
without                             : 11
```

Sixteen, not twenty-four. Tracing the eleven to their callers gives a different and fairer picture —
every one of them is a **private** helper, and every caller checks first, **except `buildFor`**:

```
buildFor is called at build.service.ts:202  (ownership at :233)
                  and build.service.ts:518  (ownership at :525)
```

So the *shape* of the claim is exactly right: **one helper, two call paths, both ahead of the
ownership check, and those two are E1.** `provisioning.service.ts:27` is the twelfth and is correct
by design — it creates the workspace. What does not hold is the arithmetic: 27 sites under the
literal reading, 16 checked; 26 sites and 25 checked if `provisioning` is excluded and callers are
traced. There is no counting rule that yields 26 and 24 together.

**A finding the case's own counts hide.** Three of the eight unscoped models —
**`Deployment`, `ReferenceAsset`, `ReferenceEmbedding` — have zero query sites.** They are declared
in the schema and never read or written anywhere in `src/`. "Eight models unscoped" and "seven
models protected by a convention kept at 26 call sites" both treat a model nobody queries the same as
`SpecVersion` with ten. The convention is not keeping those three safe; nothing is touching them.
That is the difference between an attack surface and a schema.

**Outcome · FAIL on the numbers, PASS on the map.** The defect the case exists to locate is real,
reproduced, and sits exactly where the case says. Every headline figure attached to it is wrong.
E2 says *"this case is the map, and it must be re-run whenever a model is added"* — it evidently was
not re-run after the last one was.

---

## E3 — `SET LOCAL` outside a transaction

> *"Set the tenant GUC outside a transaction, then run a scoped query. **Expected: the query returns
> rows it must not**, and the harness must detect it rather than pass. A test that cannot produce
> this failure is not testing RLS."*

**Classification · RUNNABLE.** This is the case the task expected to be blocked. It is not:
`@electric-sql/pglite` — the engine `verification/client.ts` is written against — installs and runs
a real Postgres 18.3.

**What was run.** Two tenants in one `booking` table, RLS enabled *and forced*, a non-superuser
`authenticated` role, and a policy reading the claim GUC. The identical query in two arms.

```
rows in table, as superuser: 2

ARM 1  SET LOCAL *inside* a transaction, acting as tenant A
       rows returned: 1 ["alice@a.test"]

ARM 2  SET LOCAL *outside* a transaction, acting as tenant A
       'set local role authenticated' -> "(no error raised)"
       current role now: postgres
       claim now: ""
       rows returned: 2 ["alice@a.test","bob@b.test"]

ASSERTION  a tenant-A session must see exactly 1 row
  ARM 1 (in txn) : 1 -> correct
  ARM 2 (no txn) : 2 -> LEAK, sees 2 rows including other tenants'
```

**Outcome · PASS.** Both halves hold, and the run shows *why* the trap is silent rather than merely
that it exists: `set local role authenticated` outside a transaction **raises no error at all**,
the session stays `postgres`, and a superuser bypasses RLS — so traps 1 and 2 of §5.1 compound. The
query does not fail; it succeeds with the wrong answer. The assertion detects it because it asserts
a row *count*, which is the design point the case is making.

This is also the only case in either skill that reproduces its source's reasoning verbatim:
`verification/client.ts:18-23` says *"`SET LOCAL` outside a transaction is a silent no-op; that is
why the transaction is not optional."* Measured: silent, and a no-op.

---

## E4 — A double stricter than production

> *"Diff every method a test double implements against the production function it stands in for.
> **Any operation the double refuses and production allows fails the case.**"*

**Classification · RUNNABLE.** Both sides are in the repo and the comparison is mechanical.

**What was run.** The double's rule, lifted verbatim from `build.e2e.spec.ts:46` and `:109`, and the
**production** `applyWorkspaceScope` imported from `src/auth/workspace-scope.ts`, given the same
arguments.

```
  double     -> null
  production -> {"where":{"projectId":"p-theirs","idempotencyKey":"k"}}
  production added a workspace filter? false

  Workspace            scoped by applyWorkspaceScope: false
  Message              scoped by applyWorkspaceScope: false
  SpecVersion          scoped by applyWorkspaceScope: false
  DesignVersion        scoped by applyWorkspaceScope: false
  BuildVersion         scoped by applyWorkspaceScope: false
  Deployment           scoped by applyWorkspaceScope: false
  ReferenceAsset       scoped by applyWorkspaceScope: false
  ReferenceEmbedding   scoped by applyWorkspaceScope: false
```

The two sides at source:

```ts
// build.e2e.spec.ts:106-109 — the double
buildVersion: {
  async findFirst({ where }: any) {
    if (!owns(where.projectId)) return null;      // refuses
```

```ts
// workspace-scope.spec.ts:37-40 — production, with a test asserting it does NOT
it("leaves non-scoped models untouched (scoped via project instead)", () => {
  const args = applyWorkspaceScope("SpecVersion", "findMany", { where: { projectId: "p1" } }, "w1");
  expect(args.where).toEqual({ projectId: "p1" });
});
```

**Outcome · PASS.** The reference instance holds exactly as §6.2 describes: `FakeScope` enforces
`owns(where.projectId)` on `buildVersion.findFirst` — the one call that is unguarded in production —
while `workspace-scope.spec.ts:37` asserts in a passing test that production does not. Two suites
assert opposite things about the same mechanism and **both are green in the 135**.

The consequence is worth stating plainly, because it is what makes E1 unfindable from inside the
suite: every cross-tenant assertion in `build.e2e.spec.ts` passes for two reasons at once and cannot
distinguish them. A double stricter than production cannot fail; it can only certify.

---

## E5 — Zero rows, per tenant-scoped table

> *"For every table with a tenant column, a cross-tenant read as `authenticated` inside a transaction
> with the other tenant's claims. **Expected: 0 rows, every table, no exceptions.** Generated beside
> the policy, not written later."*

**Classification · RUNNABLE as an assertion, and it exposes the reason it cannot yet run as
specified.**

**First, what the case quantifies over.** Grepping the whole repository for `create policy` /
`enable row level security` outside `node_modules`:

```
apps/engine/scripts/verify_build_plan.py:188   (fixture)
apps/engine/tests/test_verification_data.py:243,245,248   (fixture)
apps/engine/tests/test_builder_orchestrate.py:172   (fixture)
apps/engine/tests/test_library.py:399   (fixture)
apps/engine/tests/test_interaction_channel.py:638,640,641   (fixture)
spikes/local-data/app/lib/supabase.ts:35,38   (spike)
```

**Every one is a test fixture or a spike. The engine emits no policy SQL at any point.** Searching
the engine for policy generation returns only the boolean and the prose that carries it:

```
layerb/architecture.py:49    row_level_security: bool = True
layerb/architecture.py:144   row_level_security: bool = True
layerb/derive.py:384         row_level_security=True,
layerc/contract.py:57        f"table {table.name} (row-level security: {table.row_level_security})"
layerc/contract.py:114       f"security posture: RLS={posture.row_level_security}, "
layerc/scripts.py:195        if table is None or not owner or not table.row_level_security:
```

`scripts.py:190-200` is `isolation_script` — *"Two users, one table: each sees their own row and only
their own"* — and it emits a **browser** script driving two users through the UI, not a SQL
assertion. So §4.1's claim is confirmed at source: the artefact handed to the build prompt is
`RLS=True`, a boolean with one value, and there is no generated policy for a zero-rows test to be
generated beside.

**Second, run the assertion against the policies that do exist** — on real Postgres, as
`authenticated`, inside a transaction, with `force row level security` so the table owner does not
bypass:

```
TRIAL 1 · spikes/local-data/app/lib/supabase.ts:38
   policy: create policy bookings_read on bookings for select using (true);
   cross-tenant read (A asking for B's rows): 1 row(s) ["bob"]
   full table read as A:                      2 row(s) ["alice","bob"]
   E5 ASSERTION "0 rows, every table, no exceptions": FAIL — 1 foreign row(s) visible

TRIAL 2 · apps/engine/tests/test_verification_data.py:245
   policy: create policy bookings_own on bookings for select using (owner_id = auth.uid());
           create policy bookings_insert on bookings for insert with check (true);
   cross-tenant read (A asking for B's rows): 0 row(s) []
   full table read as A:                      1 row(s) ["alice"]
   E5 ASSERTION "0 rows, every table, no exceptions": PASS
```

**Outcome · PASS on the assertion, FAIL on the corpus.** The assertion is a real test — it
discriminates, one trial each way — and running it immediately caught the `using (true)` policy sitting
in this repository's own spike, which is precisely what `LAYER-B` §3.5 forbids. It cannot be run "for
every table with a tenant column" because **no table with a generated tenant policy exists**.

**To run it as written:** step 2 of §4.1 — derive the policy from the typed permission instead of
prompting for it. The assertion is then generated from the same `Permission` that generates the SQL,
which is the point of the ordering.

---

## E6 — The plan still uses a tenant-leading index

> *"`EXPLAIN` the same query. **Expected: an index scan on a tenant-leading index.** A policy that
> forces a sequential scan is a policy with an expiry date."*

**Classification · RUNNABLE**, and running it shows the case is **not stable as written**.

**What was run.** The same RLS-protected query, `EXPLAIN (costs off)` as `authenticated` in a
transaction, at two data volumes, with and without a `(owner_id, id)` index.

```
rows=50  tenant-leading index: yes
      Seq Scan on booking
        Filter: (owner_id = (NULLIF(current_setting('request.jwt.claim.sub'...
   E6 ASSERTION: FAIL — planner chose SEQ

rows=50  tenant-leading index: no
      Seq Scan on booking
   E6 ASSERTION: FAIL — planner chose SEQ

rows=200000  tenant-leading index: yes
      Bitmap Heap Scan on booking
        Recheck Cond: (owner_id = ...)
        ->  Bitmap Index Scan on booking_owner_idx
              Index Cond: (owner_id = ...)
   E6 ASSERTION: PASS

rows=200000  tenant-leading index: no
      Seq Scan on booking
   E6 ASSERTION: FAIL — planner chose SEQ
```

**Outcome · INCONCLUSIVE, and the reason is the finding.** At 200,000 rows the assertion
discriminates perfectly — index present passes, index absent fails, exactly as intended. At 50 rows
it **fails with the index present**, because a sequential scan over a tiny table is the correct plan
and the planner is right to choose it.

A generated app verified against fixture data has tens of rows, not hundreds of thousands. Run there,
E6 fails every app, including every correctly-indexed one — a check that always fails is discarded
within a week, which is the same fate as a check that always passes. The case needs a stated data
floor, or `enable_seqscan = off`, or an assertion on the index's *existence and column order* rather
than on the chosen plan.

One further trap the run exposes: the passing plan is a **`Bitmap Index Scan`**, not an `Index Scan`.
An implementer asserting on the string `"Index Scan"` gets the right answer by accident here (it is a
substring) and the wrong answer on an `Index Only Scan` — the same position-versus-presence mistake
`catalog-budget` E5 warns about, in a different file.

---

## E7 — A labelled column in a leaky place

> *"Label one column `'PII: …'`. Grep the generated app for that column name in a route path, a
> `console.log`, a `localStorage.setItem`, and a client component's props. **Expected: each hit is a
> finding with a file and a line.** With no label, the same search is a name heuristic and this case
> cannot be written."*

**Classification · BLOCKED**, and the case says so itself in its own last sentence.

```
$ grep -rn "COMMENT ON COLUMN|comment on column|PHI:|PII:" apps/ packages/ spikes/
(no matches)
```

Not one sensitivity label exists — no `COMMENT ON COLUMN`, no `PHI:`/`PII:` marker, anywhere outside
`node_modules`. Neither `Playbook` nor the architecture model carries a field that could produce one.

**What must be built:** §4.2's mechanism — a classification on the Layer B field type, and an emitter
that writes it as a column comment so it survives into the generated database.

**Would it then be a good test of it?** Yes, and it is the one blocked case whose *value* is in the
label rather than the assertion. The four leak rules are trivial greps; what makes them decidable is
having a labelled column to grep *for*. Written before the labels exist, the case is a specification
for what the label has to make possible — which is the right order, and the skill is honest that the
case is not yet a test.

---

## E8 — The gate declares its own scope

> *"For each security-relevant gate, assert its file states whether it is the enforcement point.
> **`ci.yml` passes. `tenant-discipline.spec.ts` fails** — it claims a boundary it does not check."*

**Classification · RUNNABLE.** Two named files, two predicted verdicts.

**`ci.yml` — predicted pass.** Its opening comment states its scope positively and claims nothing
about security:

```
# The check that would have caught this week.
#
# Three of the four bugs the first Codespace run found were invisible to every
# suite, because every suite ran on a machine where the artefacts already
# existed... All three are the same bug — "it works here" — and the only cure is
# a machine that has never seen this repo before.
```

A hermeticity check that says it is a hermeticity check. **PASS.**

**`tenant-discipline.spec.ts` — predicted fail, and it fails harder than predicted.** Its docblock
declares itself the enforcement point in as many words:

> *"Postgres RLS is the backstop we do not have yet; until we do, **this test is the fence**: a
> service that reaches for the raw client fails the suite and has to say why."*

and it names the defect in advance:

> *"One future `buildVersion.findMany({ where: { projectId } })` on the raw client reads across
> tenants with nothing to stop it — an external reviewer named exactly this."*

Its actual assertion greps for `this.prisma.<model>.<op>` — the **raw** client. The live defect is on
the **scoped** one. Run against the file that contains it:

```
fence regex  this.prisma.<model>.<op>  matches build.service.ts: False
the defective call site (build.service.ts:371): where: { projectId, idempotencyKey },
does the fence regex match that line? False
```

The regex matches nothing in `build.service.ts` at all — and `tenant-discipline.spec.ts` is green in
the 135.

**Outcome · PASS.** Both predicted verdicts hold. The case's own words — *"a fence that names the
failure and misses it in code is worse than no fence, because it is counted as coverage"* — are
confirmed by execution: the prose prediction and the executed check differ by one word, `prisma`
versus `client`, and that word is the whole of the fence.

---

## §4b has an assertion, no case, and the assertion does not do what it says

The task asked whether §4b — added today, `USING` versus `WITH CHECK` — has a case. **It does not.**
E1–E8 were written before §4b and none of them mentions `WITH CHECK`, mass assignment, a writable-column
allowlist, or a write that must be refused. Every one of the eight is a *read* assertion or a code
audit. A rule added to a skill without a case added beside it is exactly the gap this pass exists to
find, and here it is.

But §4b does carry an inline assertion, so that was run instead:

> *"As tenant A, update your own row setting `workspace_id` to tenant B's. **The write must fail**,
> and a subsequent read as tenant B must return zero rows. A policy with only `USING` passes the
> first half of that test and fails the second."*

```
TRIAL A · USING only — the trap §4b names
   create policy member_write on member for update using (owner_id = auth.uid());
   A updates own row, setting owner_id -> B: REFUSED: new row violates row-level
                                             security policy for table "member"
   subsequent read as tenant B: 1 row(s) ["member"]
   §4b ASSERTION (write must fail AND B's read unchanged): PASS

TRIAL B · USING + WITH CHECK — the fix §4b prescribes
   ... with check (owner_id = auth.uid());
   A updates own row, setting owner_id -> B: REFUSED: new row violates row-level
                                             security policy for table "member"
   §4b ASSERTION: PASS
```

**Both pass. The assertion cannot tell the two policies apart**, which is the one thing §4b says it
is for. The reason is documented Postgres semantics: **when an `UPDATE` policy omits `WITH CHECK`,
the `USING` expression is used for the new row as well.** So a policy whose `USING` *is* the tenant
predicate already refuses the tenant-hop, and §4b's claim — *"a policy with `USING` alone will
happily let a user `UPDATE` a row out of their own tenant and into another"* — **is false for the
policy shape it is written about.**

Where the claim becomes true is when `USING` is *broader* than the intended write rule:

```
TRIAL D · USING broader than the write rule
   for update using (true), no WITH CHECK        : A pushes OWN row into tenant B
       -> SUCCEEDED — the row now belongs to 22222222-2222-2222-2222-222222222222
   for update using (true) with check (own row)  : A pushes OWN row into tenant B
       -> REFUSED: new row violates row-level security policy for table "member"
```

That is a real and important trap. It is not the one §4b describes, and the missing precondition —
*`USING` broader than the write rule* — is the entire content of the rule.

**And `WITH CHECK` does not address the failure §4b is a section about.** §4b opens with mass
assignment: a user setting their own row's `role`. Measured:

```
TRIAL C · does WITH CHECK stop MASS ASSIGNMENT on a non-policy column?
   USING only              : A sets own row role='owner' -> SUCCEEDED, role is now owner
   USING + WITH CHECK      : A sets own row role='owner' -> SUCCEEDED, role is now owner
```

Neither stops it, and neither could: the resulting row still satisfies `owner_id = auth.uid()`, so
every policy passes. **Only mechanism 1 — the writable-column allowlist — catches mass assignment.**
§4b says *"Two mechanisms, and you need both"*; the run says they address two different failures, and
presenting `WITH CHECK` as the second half of the mass-assignment answer is the error.

**What §4b needs:** the precondition on the `USING`-only claim; the assertion rewritten so it can
fail (start from `using (true)`, or assert on the allowlist rather than the policy); and the mass
assignment and the tenant-hop separated, since one mechanism each.

---

# What the cases reveal about the skills that wrote them

**1 · The code positions are right and the counts are wrong, consistently.** Every line number
`tenant-isolation` cites resolves to the statement it claims — `:517`, `:518`, `:525`, `:202`,
`:233`, `:62`, `:76`, `:11-23`, `identity.py:210`. Every aggregate number in either skill that
could be re-derived was off: 18,212 against 18,182; 1,046 characters against 1,016; 26 call sites
against 27; 24 checked against 16. **Reading is reliable; counting is not**, and the two are
presented in the same voice with the same confidence. `catalog-budget` §2.4's own instruction —
*"Budget derivation (re-derive it, do not trust the number)"* — was not applied to the derivation
inside `catalog-budget`.

**2 · An arithmetic error propagated into a spec violation that does not exist.** E1's 30-byte
overcount and its *"`testing`'s description is over the 1,024 limit"* finding are the same error.
The description has never exceeded 1,016 characters. The skill then cites that non-finding as
justification for a per-entry cap — *"a per-entry cap of any size would have caught it at write
time."* The recommendation survives; the evidence offered for it does not. This is the failure mode
the skills call *"a fence that names the failure"*, in the arithmetic rather than in the code.

**3 · Two of the fifteen cases cannot fail, and both are in the skill that warns about this.**
`catalog-budget` E2 and E3 are arithmetic identities dressed as experiments: emptying a description
must reduce a sum; a floor at zero must reject zero; 250 must exceed 200 and fall below 0.8 × 6,965.
Neither reads anything about this repository. E3 is worse than tautological in its third clause —
*"the failure must name the diagnosis"* grades a message the runner writes in the same step. Both
became demonstrations only because I supplied the ceiling, the baseline and the message that were
missing; **the case was measuring my scaffolding, not the corpus.**

**4 · A case can be near-tautological and still be worth running.** E6 is the counter-example that
keeps the previous point honest. `addressable ≤ physical` cannot fail without symlinks or aliases,
and the corpus has neither — yet running it reproduced the predicted `graphify` finding and turned
up a new one nobody had recorded: **both plugin manifests advertise "sixteen skills" against 27**.
The value was in the enumeration, not the assertion. A case whose assertion is weak but whose
*procedure* forces you to look at every entry is not the same defect as one that looks at nothing.

**5 · The strongest cases are the ones that name a file and a predicted verdict.** E4 and E8 are the
two that passed cleanly, and both have the same shape: *this specific artefact, this specific
verdict*. E4 names `FakeScope` versus `applyWorkspaceScope`; E8 names `ci.yml` passes and
`tenant-discipline.spec.ts` fails. Both were confirmed by execution, and neither could have been
confirmed by reading the skill. Contrast E2, whose numbers were wrong precisely because they were
aggregates over a set nobody re-enumerated.

**6 · A rule added without a case is a rule nobody has run — and §4b shows why that matters.**
§4b was added today after an ablation found a gap, and no case was added with it. Run against real
Postgres, its central claim is **false for the policy shape it describes**: Postgres reuses `USING`
as the new-row check when `WITH CHECK` is omitted, so the tenant-hop it warns about is already
refused. Its own assertion passes identically with and without `WITH CHECK`, so it cannot detect
the thing it exists to detect. And `WITH CHECK` does not stop the mass assignment the section opens
with — only the allowlist does. **Three errors, in a section written to fix an error, none of which
would have survived one execution.** This is the single strongest argument in this document for
running cases at the moment a rule is written.

**7 · The suite that certifies tenancy has never touched a database.** 135 tests, twelve files,
green, no Postgres involved. `FakeScope` refuses the exact cross-tenant call production allows, and
`workspace-scope.spec.ts:37` asserts in a passing test that production allows it. Both suites are
counted as coverage of the same mechanism. E4 predicted this and E4 is right; what execution adds is
that **the green run is not weak evidence of tenant safety, it is evidence of nothing at all** on the
seven models the scope does not cover.

**8 · Availability was assumed rather than checked, and the assumption was wrong.** The RLS cases
were expected to be blocked for want of Postgres. There is no server and no Docker, but
`@electric-sql/pglite` — the engine's own dependency — installs in one second and runs Postgres 18.3.
**Three of the four "needs a database" cases ran**, and two of them (E3, and the §4b assertion)
produced findings that no amount of reading would have produced. The lesson generalises past this
document: *check, do not assume*, applied to the eval harness and not only to the code.

---

# What must exist before the blocked cases can run

| Case | What must be built | Would the case then test it well? |
|---|---|---|
| `catalog-budget` E4 · splitter idempotency | An `applyCatalogTrim` equivalent: a build-time generator that splits each description into a frontmatter lead and a `## When to invoke this skill` body section. Nothing of the kind exists — the only occurrences of the name in the repo are the mining note and the skill's own §3. | **Yes.** Idempotency is the property a generator that runs every build must have, and a fixed-point assertion is one line. Written before the code, it makes the splitter be designed as a fixed point rather than patched into one. |
| `catalog-budget` E5 · decision not behind the load | The same splitter, plus the loader distinction that makes the split mean anything. Today **zero of 27 skills** carry a `## When to invoke this skill` section, so the set the case quantifies over is empty. | **Yes — the most valuable of the four.** Its whole content is *assert on earliest position of use, not on presence*, which is the mistake an implementer makes unprompted. A substring check passes when the directive sits behind the STOP that reads it. |
| `catalog-budget` E2, E3 · floors | Not a build so much as a commitment: **a committed check with a committed ceiling and a frozen baseline**, and a failure message someone else reviewed. Until then both cases assert arithmetic. | **Only then.** With a real check they stop asserting that zero is not positive and start asserting that *our* check has the floor — a claim that can be false. E3's third clause must move to a review of a committed message; it can never be graded by its own author. |
| `catalog-budget` E7 · the ratchet | A `pre-commit` or `pre-push` hook, or CI. `/home/user/scio` has **neither, and no `.github/` at all**; its only two hooks are `graphify`'s `post-checkout` and `post-commit`, both after the fact. Plus a budget constant to ratchet. | **Yes, and it is already a passing test of the absence.** It ran and it failed honestly: 4,580 → 9,999 committed with the derivation untouched, exit 0. |
| `tenant-isolation` E1 · the HTTP half | A Postgres reachable by Prisma — `docker compose up db` (the compose file is there; no daemon is), or `@electric-sql/pglite-socket` — then `prisma migrate deploy` and a two-workspace seed. | **Yes.** The mechanism is already proven against production code; what is missing is the response body, and *"it returns the other tenant's `total_cost_usd`"* should not be asserted in prose until someone has seen it. |
| `tenant-isolation` E5 · as specified | §4.1 step 2: **derive the policy from the typed permission instead of prompting for it.** Today `row_level_security` is `True` at all three declaration sites, `derive.py:384` sets it unconditionally, and no code path anywhere emits `create policy`. | **Yes**, and the assertion is already proven to discriminate — it caught the `using (true)` in `spikes/local-data`. It becomes generatable the moment the policy is generated, from the same `Permission`. |
| `tenant-isolation` E6 · as specified | Nothing needs building; the **case** needs fixing. It must state a data floor, or set `enable_seqscan = off`, or assert on the index's existence and column order rather than the chosen plan — otherwise it fails every correctly-indexed generated app at fixture scale. | **Not as written.** It discriminates at 200,000 rows and fails a correct schema at 50. |
| `tenant-isolation` E7 · labelled columns | §4.2: a sensitivity classification on the Layer B field type, and an emitter writing it as `COMMENT ON COLUMN`. **Zero labels exist in the repository.** | **Yes**, and the case is really a specification for the label. The four leak rules are trivial greps; the label is what makes them decidable rather than name heuristics. |
| `tenant-isolation` §4b | **A case, and a corrected rule.** The `USING`-only claim needs its missing precondition (`USING` broader than the write rule); the assertion needs to start from a policy it can fail; and mass assignment and the tenant-hop need separating, since they have one mechanism each. | The assertion **as written cannot fail** on the policy shape it describes — measured, both arms pass. It is the clearest instance in this document of a rule that has never been run. |

**One thing needs no build at all.** Nine of fifteen cases ran today using only what was already on
this machine — `git`, `python3`, the repository's own `vitest` suite and indexer, and an npm package
the engine already depends on. The obstacle to running these was never the tooling.
