# Review of the whole — contradictions, drift and gaps

Everything in `docs/` and `.claude/skills/` read side by side, once, on 2026-08-26. Where two
documents disagreed about a measurable fact, the fact was checked against
`/home/user/hello-world` (read-only; nothing there was touched). Nothing in this repo was
changed either — this file is the only output.

## Summary

The repo is in better internal shape than its own history predicts, and it is still drifting in
one specific, mechanical way: **corrections land in the document that discovered them and never
travel to the documents that carry the old number.** Every one of the numeric collisions below
has that shape. Nobody is careless; nobody re-checks.

The seven findings that matter most:

1. **`00-INDEX.md` — the file `CLAUDE.md` tells every session to read first — still says Layer C
   runs "seven rules". It runs nine.** `LAYER-C`, `ARCHITECTURE-AS-BUILT`, `PIPELINE` and
   `OPERATING-MODEL` all say nine. The correction in `docs/next/LAYER-C-BUILD-PLAN.md:57` was
   aimed at the wrong file (§1.1).
2. **"Six validation rules" for Layer B survives in four places after `LAYER-B` retracted it in
   its own footer** — including in `ARCHITECTURE-AS-BUILT.md:54`, where it is stated as one of
   the five invariants the system rests on (§1.2).
3. **Three forward documents cite Layer A's metrics harness as "A-3". It is A-2.** One of them
   also says A-3 "comes first in Layer A"; A-1 does (§3.1).
4. **`docs/next/LAYER-B` builds a proposal (B-6) on a cache floor that `docs/next/LAYER-A`
   explicitly corrected.** B-6's stated reason — *"the playbook alone is 668 tokens and will not
   cache"* — is false on the default path, where the floor is 512 (§2.1).
5. **The two REVIEWS documents contradict each other in the same commit.**
   `REVIEWS-WHAT-WE-MISSED.md:166` says the 35 findings were never verified one by one;
   `REVIEWS-FINDINGS-VERIFIED.md` is that verification (§4.2).
6. **Two skills that `docs/next/LAYER-E-BUILD.md:685-691` says were "written" do not exist**, and
   five documents give four different counts of how many skills there are — four, thirteen,
   thirteen, fifteen and sixteen. Sixteen is right, and only the newest document says it
   (§6.1, §7.2).
7. **A verified-still-true security finding — the preview iframe with no `sandbox` attribute —
   has zero forward coverage.** The word "iframe" does not appear once in any of the seven
   `docs/next/` documents, including Layer F, which owns the preview (§5.1).

Categories 2 and 4 are thin, and that is a real result: the layer documents mostly disagree by
*being stale*, not by reasoning to opposite conclusions. Where they genuinely collide (§2.1,
§2.2, §2.3) it is worth reading closely, because in each case the later document is right and
the earlier one is still the one a reader hits first.

---

## 1 · Numbers that disagree

### 1.1 Layer C's plan validation: "seven rules" vs "nine rules" — nine is right, and the correction went to the wrong file

- `docs/as-built/00-INDEX.md:120-121` — *"**Nothing reads Layer C's plan validation.** Seven
  rules run every build"*
- `docs/as-built/LAYER-C-BUILD-PLAN.md:204` — *"`validate_plan` implements nine good rules"*
- `docs/as-built/ARCHITECTURE-AS-BUILT.md:70` — *"`validate_plan` — nine rules, every build"*
- `docs/PIPELINE.md:69-70` — *"It computed nine validation rules and read none of them"*
- `docs/OPERATING-MODEL.md:141` — *"nine validation rules nobody reads"*

**Verified** against `hello-world/apps/engine/src/scio_engine/layerc/validate.py`: **seven check
functions** (`:43, :63, :80, :94, :132, :191, :208`) emitting **nine distinct rule identifiers**
(`node_covered`, `acyclic`, `dependency_exists`, `contract_complete`, `contract_testable`,
`criterion_producible`, `criterion_observable`, `order_respects_dependencies`,
`unique_package_id`). Nine is right.

The sharp part: `docs/next/LAYER-C-BUILD-PLAN.md:57-58` issues the correction —

> **There are nine validation rule identifiers, not seven.** `docs/as-built/LAYER-C-BUILD-PLAN.md`
> says *"seven rules"*, which counts the check *functions*.

— and names the wrong document. `LAYER-C-BUILD-PLAN.md` never says "seven rules"; its only
"seven" is `:59` (*"ADR-0013 lists seven things each package must carry"*), an unrelated count.
The file that says seven is `00-INDEX.md:121`, and because the correction pointed elsewhere,
nobody fixed it. `00-INDEX.md` is the file `CLAUDE.md:17` makes mandatory reading, and the
`as-built` skill (`.claude/skills/as-built/SKILL.md:16`) repeats *"always first"*.

### 1.2 Layer B's architecture validation: "six rules" survives in four places after being retracted

`docs/as-built/LAYER-B-UNDERSTANDING.md:135-138` records the correction explicitly:

> *the earlier "six rules" counted check functions rather than the eleven rule identifiers they
> emit. Both corrected 2026-08-26.*

**Verified** against `layerb/validate.py`: six check functions (`:49, :80, :112, :149, :196,
:215`), eleven distinct rule ids, exactly one (`screen_references_operation`) at warning
severity. Eleven is right, and `LAYER-B-UNDERSTANDING.md:50` and
`docs/next/LAYER-B-UNDERSTANDING.md:52-58` both say so.

Four places still say six, one of them inside the correcting document:

| Where | Text |
|---|---|
| `docs/as-built/LAYER-B-UNDERSTANDING.md:88` | *"**The six validation rules.** Each catches a class of incoherent app"* — §6, uncorrected, while §4 of the same file says eleven |
| `docs/as-built/ARCHITECTURE-AS-BUILT.md:54` | *"The architecture is validated before code is generated — **six rule checks**"* |
| `docs/as-built/JOURNEY-INVOLVED-PATH.md:129` and `:200` | *"validated by **six rule checks**"* / *"Layer B's **six rule checks** are the nearest thing"* |
| `.claude/skills/app-design/SKILL.md:167-168` | *"They belong beside `validate.py`'s **six architecture rules**"* |

`ARCHITECTURE-AS-BUILT.md:54` is the worst instance: it sits in *"The five invariants the system
rests on"*, the file's highest-confidence list, under a header (`:3-4`) promising *"Every claim
here is carried up from one of them; nothing was written straight into this file."* It was
carried up before the correction and never re-carried.

### 1.3 `UsageKind`: "six values" vs eight, inside one document

- `docs/as-built/LAYER-G-CROSS-CUTTING.md:342` — *"a metering ledger with **six** `UsageKind`
  values and four write sites"*
- `docs/as-built/LAYER-G-CROSS-CUTTING.md:263-266` — *"`UsageKind` in shared is **three values
  behind** the database. `entities.ts:14` has `generation | critique | sandbox | storage |
  other`; the Prisma enum also has `intake`, `preview`, `design_change`"*

Those cannot both be true. **Verified**: `schema.prisma`'s `enum UsageKind` has **eight**
values; `packages/shared/src/entities.ts:14` has **five**. §6's "three behind" is right; the
drift section's "six" is wrong. `docs/next/LAYER-G-CROSS-CUTTING.md:226-231` gets it right and
does not flag the as-built error.

### 1.4 The scoped-model arithmetic does not close in `as-built`, and does in `next`

- `docs/as-built/LAYER-G-CROSS-CUTTING.md:81-86` — six models scoped, *"The other **seven**"*,
  named individually
- `docs/as-built/LAYER-G-CROSS-CUTTING.md:212` / `:364` and
  `docs/as-built/ARCHITECTURE-AS-BUILT.md:130` — *"6 of 14"*, *"six of fourteen tables"*

6 + 7 = 13, not 14, and no as-built document accounts for the fourteenth.
`docs/next/LAYER-G-CROSS-CUTTING.md:51-56` resolves it in one clause — *"`Workspace` is the
tenant itself"* — and nothing propagated that back. **Verified**: `schema.prisma` declares 14
models; `Workspace` is the fourteenth and correctly has no `workspaceId`.

Related, and left standing: `docs/next/LAYER-G-CROSS-CUTTING.md:934` (G-3) proposes *"shared-schema
RLS on **all fourteen models**"*, which includes the tenant table itself — the one model where
the proposal makes no sense on its own terms.

### 1.5 A ceiling cited in the wrong file

- `docs/as-built/LAYER-E-BUILD.md:154` — enforced at *"**`relay.py:264`** — one place, for every
  codegen and every critique in the build"*
- `docs/as-built/LAYER-G-CROSS-CUTTING.md:344` — *"a per-build ceiling in the engine relay
  (**`engine/builder/loop.py:256-262`**)"*

**Verified**: enforcement is `execution/relay.py:261-267` (`raise BudgetExceeded`).
`builder/loop.py:250-262` is the `BuildOptions.budget_usd` / `BuildOptions.spend` declaration —
and `budget_usd` is the field `docs/as-built/LAYER-E-BUILD.md:393-397` lists under **Obsolete**.
Layer G cites a deprecated field as the enforcement point.

### 1.6 The reveal's nine items: "two and a half" vs "three", with three rows judged differently

Both documents assess the same nine-item list from `PRODUCTION_READINESS_DIFF.md` §7, both on
2026-08-26, both against `RevealPage.tsx`:

| §7 item | `docs/next/LAYER-E-BUILD.md:515-526` | `docs/next/LAYER-F-DESIGN-WINDOW.md:361-371` |
|---|---|---|
| model and build cost | *"cost only"* — `BuildFinished.model` transmitted, not rendered | *"**yes**, and well — estimate *and* actual, side by side"* |
| remaining risks | *"partly"* | *"**yes** (`RevealPage.tsx:59-67`)"* |
| version id and export | *"yes"* | *"half"* — export does not exist |

Totals: `LAYER-E:531` says **"Two and a half of nine"**; `LAYER-F:373` says **"Three of nine"**.
The E-10 and F-10 proposals inherit the split (`LAYER-E-BUILD.md:959`, `LAYER-F-DESIGN-WINDOW.md:909`).
Nothing reconciles them, and both are cited as the size of the gap the reveal has to close.

### 1.7 `NotImplementedException`: 14 vs 8 — eight is right

- `docs/as-built/REVIEWS-FINDINGS-VERIFIED.md:106` — *"**14** `NotImplementedException` across
  **six** modules … Broader than either review reported"*, and `:160` — *"the 501 surface is
  wider than either review said — six modules, not three"*
- `docs/next/LAYER-G-CROSS-CUTTING.md:1030` (footer) — *"the `NotImplementedException` count (14
  across 6 modules) … produced by reading the tree, not recalled"*
- `docs/next/LAYER-F-DESIGN-WINDOW.md:145-152` — *"**Eight** throwing 501 endpoints across six
  modules, not fourteen.** Fourteen is the count of `NotImplementedException` *mentions*; six of
  those are imports and one (`usage/usage.service.ts:8`) is a comment"*

**Verified**: `grep -rn 'NotImplementedException' apps/api/src` returns 14 lines;
`grep -rn 'throw new NotImplementedException'` returns exactly **8**, in six modules — `user.me`,
`workspace.current`, `notification.list`, `notification.markRead`, `reference.list`,
`reference.create`, `deployment.list`, `deployment.create`. Layer F is right. The "14 endpoints"
figure is still the headline in a document whose whole purpose is verification, and it is
repeated in `LAYER-G`'s footer under a claim of having read the tree.

### 1.8 "Two confirmed cases of tests passing for the wrong reason" vs three

- `docs/as-built/ARCHITECTURE-AS-BUILT.md:127` — *"**Two confirmed instances, not one.**"*
- `docs/OPERATING-MODEL.md:99` — *"the predecessor has **two confirmed cases** of tests passing
  for the wrong reason"*
- `docs/next/LAYER-E-BUILD.md:171-172` — *"That is the **third** confirmed instance in this
  repository"* (`FakeScope`, `test_interaction_channel.py`, and the Layer C seam it sits on)

Three is the current count. `OPERATING-MODEL.md` uses "two" to size a proposed skill
(`test-design`, now written as `testing`), so the number is load-bearing where it is stale.

### 1.9 The playbook is 668 tokens in Layer B and 667 in Layer C

- `docs/next/LAYER-B-UNDERSTANDING.md:594`, `:617`, `:629`, `:696` (B-6) — **668**, *"measured"*
- `docs/next/LAYER-C-BUILD-PLAN.md:141`, `:696`, `:764` — **667**, *"measured"*

One token, and both say measured, on the same artifact (`Playbook.as_prompt_section()`), on the
same day, by the same method (chars ÷ 4). Trivial in itself; listed because §2.1 shows B-6's
whole argument turns on which side of a threshold this number sits, and because it is the only
evidence that the two documents measured independently rather than one copying the other.

### 1.10 Layer E's own test arithmetic does not add up

`docs/as-built/LAYER-E-BUILD.md:487-493` claims *"247 passed, 9 skipped"* and then enumerates the
suites: 30 + 37 + 36 + 21 + 21 + 18 + 16 + 16 + 14 + 11 + 10 + 7 + 6 + 6 = **249 collected**.
249 collected minus 9 skipped is **240 passed**, not 247. Either the enumeration is incomplete —
it does not say so, and it reads as exhaustive — or the headline is wrong. The same 247 appears
at `LAYER-E-BUILD.md:4`, and `00-INDEX.md:86` independently reports the whole engine suite at
640 passed / 21 skipped, which neither confirms nor contradicts it.

### 1.11 Two different baseline commits for the same day's verification

- `docs/as-built/LAYER-C-BUILD-PLAN.md:351` — *"`hello-world` at **`00408d3`**"*
- `docs/as-built/REVIEWS-FINDINGS-VERIFIED.md:6` — *"the working tree at **`bd4f6d7`**"*
- `docs/next/LAYER-E-BUILD.md:20` and `docs/next/LAYER-F-DESIGN-WINDOW.md:25` — **`00408d3`**

Three documents say `00408d3`, one says `bd4f6d7`, all dated 2026-08-26, and nothing reconciles
them. `REVIEWS-FINDINGS-VERIFIED.md` is the document whose entire value is reproducibility.

### 1.12 The dollar figures three documents quote are 1.5× high, and only one says so

`docs/next/LAYER-G-CROSS-CUTTING.md:833-839` establishes that `matrix.yaml:57-58` prices
`claude-sonnet-5` at $3/$15 when the list rate is $2/$10 (**verified**: `input_cost_per_mtok:
3.0`, `cost_per_mtok: 15.0`), that the three real calibration runs in `estimate.py` were on
Sonnet, and therefore that *"`feature = $0.857`, `foundation = $0.168–$0.312`, and the headline
'five-package plan… $1.42 in 14 minutes' are each 1.5× the true spend. At list, the same tokens
are ≈ $0.95."*

Two documents quote those figures with no such caveat:

- `docs/next/LAYER-C-BUILD-PLAN.md:296-302` — a table headed *"observed cost"*: feature $0.857,
  foundation $0.168–$0.312, and `:775` *"a five-package build at **$1.42** in 14 minutes"*
- `docs/next/LAYER-E-BUILD.md:124-125` — *"The as-built quotes $1.42 and $2.69"*

`LAYER-C` then builds §3.2's argument (*"The one package kind with no size limit is 5–10× every
other kind and dominates the invoice"*) on the uncorrected column. The ratio survives the
correction; the absolute dollars do not, and C-3 is argued in dollars.

(Minor, in the same sentence: `LAYER-E-BUILD.md:124` attributes $1.42 and $2.69 to *"the
as-built"*. No `docs/as-built/` file contains either figure; `docs/next/LAYER-C-BUILD-PLAN.md:775`
does.)

### 1.13 `00-INDEX.md`'s test total mixes collected with passed

`docs/as-built/00-INDEX.md:61`:

> **884 total** — engine 661, API 135, app 109.

661 + 135 + 109 = **905**. The sentence's own breakdown does not sum to its own headline.

Where 884 comes from is visible nineteen lines later. `00-INDEX.md:86-88` reports the verified
baseline as engine **640 passed**, 21 skipped, API 135, app 109 — and 640 + 135 + 109 = **884**.
So the headline counts the engine's *passed* tests while the breakdown beside it counts the
engine's *collected* tests, in one sentence, with no marker that the two are different units.

This is the same collected-versus-passed confusion `.claude/skills/testing/SKILL.md:247` sets a
rule against (*"'27 passed, 9 skipped' is never reported as '36 tests pass'"*) and
`:253` codifies (*"**Three numbers or none.** `ran / passed / skipped`"*) — in the file every
session is told to read first, in the one place the whole system's test count is stated.

The rest of the section is internally coherent: `00-INDEX.md:91` reconciles `/suites`' 655
passed / 6 skipped against 640 / 21 as a 15-test environment gate, and 655 + 6 = 640 + 21 = 661
collected both ways.

### 1.14 Where the numbers now agree

Worth recording, because the brief named several of these as previously broken and they are
fixed:

- `test_interaction_channel.py` — **36 collected / 27 run / 9 skipped** in all five places it
  appears: `00-INDEX.md:70` (as a collected count in a table), `LAYER-C-BUILD-PLAN.md:354-355`,
  `LAYER-E-BUILD.md:488-489`, `LAYER-F-DESIGN-WINDOW.md:431`, `ARCHITECTURE-AS-BUILT.md:133`.
- **35 review findings, not 34** — `REVIEWS-FINDINGS-VERIFIED.md:35`, `REVIEWS-WHAT-WE-MISSED.md:4`,
  `.claude/skills/as-built/SKILL.md:80`. Claude F-01…F-17 plus GPT F-01…F-18 = 35.
- **CVSS** — `docs/next/LAYER-G-CROSS-CUTTING.md:164-179` reconciles 9.3 (MITRE, CVE record) and
  8.26 (the reporting researcher) with the rule *"never present one as a correction of the
  other"*, and `docs/next/LAYER-B-UNDERSTANDING.md:344-345` follows it exactly.
- **Five placeholder routes** — `JOURNEY-INVOLVED-PATH.md:90-92`, `REVIEWS-WHAT-WE-MISSED.md:11-24`,
  `docs/next/LAYER-F-DESIGN-WINDOW.md:77-81`, `.claude/skills/as-built/SKILL.md:82`,
  `OPERATING-MODEL.md:141-142`. **Verified**: `apps/app/src/App.tsx:16-22` lists exactly five.
- **Layer B has 60 tests, not 30** — `LAYER-B-UNDERSTANDING.md:135-137`,
  `docs/next/LAYER-B-UNDERSTANDING.md:41-50`, consistently.
- **The graph** — 5,173 nodes / 12,054 edges, ~5.5 MB, in every one of the six places it is
  quoted. **Verified** by loading it.
- **The library's matchable catalog is one entry** — `00-INDEX.md:122`, `LAYER-D-LIBRARY.md:276-278`,
  `ARCHITECTURE-AS-BUILT.md:90`, `docs/next/LAYER-D-LIBRARY.md:49-57`, consistently.

---

## 2 · Conclusions that collide

Three real collisions. Each is a case where a later document reasoned its way to the opposite of
an earlier one and the earlier one was left standing.

### 2.1 B-6's stated reason is refuted by A §7.3, and C says so without fixing B

`docs/next/LAYER-B-UNDERSTANDING.md:626-639`, under the heading *"The correction: the playbook
cannot be cached alone"*:

> The previous draft called the playbook *"the single best caching target in the system."*
> Measured, it is **668 tokens** — and the minimum cacheable prefix is **~1,024 tokens**. A
> breakpoint on the playbook alone caches nothing, silently.

`docs/next/LAYER-A-INTAKE.md:594-610` retracts exactly that assumption:

> The previous draft said the minimum cacheable prefix is ~1,024 tokens… **The floor is
> model-dependent and non-monotonic:** Claude Opus 5 **512** · Opus 4.8, Sonnet 5 1,024 ·
> Opus 4.7 2,048 · Opus 4.6, Haiku 4.5 **4,096**.

668 > 512. **On the default path — Opus 5, which `matrix.yaml` ranks first for `architecture` and
`codegen` — the playbook alone caches.** B-6's headline reason
(`LAYER-B-UNDERSTANDING.md:696`: *"**The playbook alone is 668 tokens and will not cache**"*) is
false, and so is the "clears the 1,024 floor with 2.3–4× margin" arithmetic at `:638`, which
computes the wrong margin against the wrong floor.

The 512 table is carried correctly by five of seven forward documents:
`LAYER-A-INTAKE.md:600-605`, `LAYER-C-BUILD-PLAN.md:744-749`, `LAYER-E-BUILD.md:829-834`,
`LAYER-F-DESIGN-WINDOW.md:811-812`, `LAYER-G-CROSS-CUTTING.md:808`. `LAYER-B` and
`LAYER-D-LIBRARY.md:538` still use ~1,024.

`docs/next/LAYER-C-BUILD-PLAN.md:764-766` **names the error and does not fix it**:

> Layer B's **B-6** proposes caching the playbook prefix and measures it at 668 tokens — *"the
> playbook alone… will not cache"*. Combined with the whole, the vocabulary and the scope guard,
> as §2.2 arranges them, it does.

And `LAYER-C` then contradicts itself in the same document: §7.1 (`:741-754`) carries the correct
table and concludes *"The 892-token constant block **clears the Opus 5 floor by 1.7×** as it
stands"*, while §2.2 (`:157`) says the same block is *"under the ~1,024-token cache floor"* and
proposal **C-5** (`:836`) asks for *"a test asserting the constant prefix stays above the
~1,024-token cache floor"*. Three positions, one document.

**Consequence if unresolved.** C-5's test would be written against a threshold twice the real
one and would fail a correct implementation; B-6 would be argued on a reason that does not hold;
and both would be *defensible* on the current text.

### 2.2 `freeze` is obsolete in `as-built`, and the unbuilt half of the layer in `next`

- `docs/as-built/LAYER-F-DESIGN-WINDOW.md:327-335`, under **Obsolete**:

  > **`POST /projects/:id/design-versions` — "Freeze the approved design as a new version"** …
  > **nothing calls it** … If it were ever called it would create a *current* design version with
  > no workspace, which `designToPromote` would then read as "nothing to promote" and rebuild
  > from scratch. **Dead, and dangerous if revived.**

- `docs/next/LAYER-F-DESIGN-WINDOW.md:154-161`:

  > **(i) There is no gate 2.** … The as-built called it obsolete. It is not obsolete; **it is
  > the unbuilt half of the layer's own name.** Only one of the two contracts the product is
  > built on exists.

These are opposite verdicts on the same endpoint, and the disagreement is substantive rather than
verbal: one says delete, the other says this is the missing second approval gate that
`UX-FLOW.md:93` requires. Proposal **F-7** holds both options open (*"or `freeze` is deleted"*),
which is the honest resolution — but the as-built document still files it under a heading whose
own definition is *"Obsolete — remove"* (`.claude/skills/as-built/SKILL.md:64`), and that heading
is what `PIPELINE.md:99` says stage 5 will act on: *"**Obsolete** | do not carry it"*. As written,
the pipeline would delete the thing Layer F says is the missing gate.

### 2.3 The scored coverage view: wanted in four documents, retracted in the one that owns it

Four documents call for a per-area readiness score:

- `docs/as-built/LAYER-B-UNDERSTANDING.md:100-102` — *"nothing that could render 'security 86%,
  data 90%, UI 40%'"*
- `docs/as-built/ARCHITECTURE-AS-BUILT.md:105-108` — *"The missing fourth is a **scored** view…
  It is the smallest high-value gap in the system"*
- `docs/as-built/JOURNEY-INVOLVED-PATH.md:199` — *"**No score.** Computable today"*
- `docs/next/LAYER-B-UNDERSTANDING.md:92` — *"The scored coverage view (Layer A §3.2)"*

`docs/next/LAYER-A-INTAKE.md:184-204` retracts it, in the layer that would compute it:

> **The previous draft proposed `area_score = (stated·1.0 + derived·0.6 + default·0.2) / n`.
> Retracted.** Those weights were invented, they are unfalsifiable, and a number a user can
> haggle with is worse than a list they can act on.

and replaces it with a **29148 characteristic vector** — proposal **A-9**, whose text ends
*"**not** an invented percentage"* (`:689`). `LAYER-B`'s citation is also wrong on its face:
Layer A §3.2 is *Requirement identity*, not coverage; the coverage material is §2.6, which is the
retraction.

So `ARCHITECTURE-AS-BUILT.md`'s *"smallest high-value gap in the system"* is a thing Layer A has
decided not to build, and `LAYER-B` proposes to assemble it citing a section that says so.

### 2.4 The CVE is "disputed by the supplier" in a skill and undisputed in two layer documents

`.claude/skills/architecture/SKILL.md:68-69`, `:210` and `:352`:

> CVE-2025-48757 … CVSS v3.1 9.3 Critical, **disputed by the supplier**, who argues isolation is
> the customer's responsibility.

`docs/next/LAYER-G-CROSS-CUTTING.md:164-186` reconciles the two scores in careful detail and
records vendor acknowledgement and "Patches and Updates: None available" — and never mentions the
dispute. `docs/next/LAYER-B-UNDERSTANDING.md:459-471` builds a positioning claim on it
(*"the market leader shipped 170+ applications with unenforced row-level security, at CVSS 9.3
Critical"*) with no dispute noted, in a section titled *"now with a CVSS number"*.

This is not a numeric disagreement — it is a material qualifier that lives in one file and not in
the two that would use the claim externally. `LAYER-B:470` already sets the right bar
(*"Making the claim before the rule exists would be the same failure with our name on it"*); the
same discipline should apply to the disputed status.

---

## 3 · ADR proposals that collide or depend silently

**85 proposals exist**, not ~90: A 10 · B 10 · C 12 · D 10 · E 15 · F 14 · G 14. (`PIPELINE.md:57`
says *"roughly 90"*, which is close enough to be fine and worth correcting when that line is next
touched.)

The good news first, because it is unusual: **cross-layer dependencies are mostly declared, not
silent.** `LAYER-C-BUILD-PLAN.md:864-867`, `LAYER-F-DESIGN-WINDOW.md:940-943` and
`LAYER-E-BUILD.md:956` each end with an explicit "dependencies across documents" paragraph naming
what waits on what, and the big chain (B-1 → C-6 → F-6) is stated identically in all three places
with a division of labour table repeated in each. No proposal was found that contradicts a
**settled** ADR in `01-DECISIONS.md` without engaging its stated reason — the constraint
paragraphs at the top of each forward document (`LAYER-A:46`, `LAYER-C:52`, `LAYER-D:41`,
`LAYER-E:49`, `LAYER-F:69`) exist precisely to prevent that, and they hold.

What is broken is the **identifiers**.

### 3.1 Three documents cite Layer A's metrics harness as "A-3". It is A-2.

`docs/next/LAYER-A-INTAKE.md:682` — **A-2** is *"The replay harness is a prerequisite, on
published metrics"*. `:683` — **A-3** is *"Prompt-cache the conversation prefix"*. The ordering
note at `:694-696` puts **A-1** first (fence the question prompt), then A-2.

| Where | Text | Wrong how |
|---|---|---|
| `docs/next/LAYER-C-BUILD-PLAN.md:851` | *"**C-12 next**, for the same reason **A-3** comes first in Layer A"* | wrong id **and** wrong ordinal — A-1 comes first |
| `docs/next/LAYER-E-BUILD.md:951` (E-2) | *"Nothing else here is decidable without it, exactly as **A-3** and C-12 are for their layers"* | wrong id |
| `docs/next/LAYER-F-DESIGN-WINDOW.md:921` | *"for the same reason **A-3** comes first in Layer A and C-12 in Layer C"* | wrong id and wrong ordinal |

The `C-12` half of each citation is correct, which is what makes this a renumbering that three
dependent documents never picked up rather than three independent mistakes. It is the cheapest
possible instance of the drift this repo's own `CLAUDE.md` says killed its predecessor, and it
sits in the **ordering** paragraphs — the part a reader uses to decide what to build first.

### 3.2 `SKILLS.md` cites B-5 for the design playbook. It is B-7.

- `docs/next/SKILLS.md:53` — *"`app-design` … §1–§4 proposed as playbook content (**B-5**)"*
- `docs/next/LAYER-B-UNDERSTANDING.md:697` — **B-7** is *"A design section in the playbook | see
  `.claude/skills/app-design` §1–§4"*
- `docs/next/LAYER-B-UNDERSTANDING.md:695` — **B-5** is *"`origin ∈ {requirement, assumption,
  necessity}` on every node"*

`docs/next/LAYER-C-BUILD-PLAN.md:158` cites it correctly as *"Layer B §2.4, B-7"*.

### 3.3 `LAYER-B` cites B-3 for the reflexion model twice, and B-4 once, in one document

- `docs/next/LAYER-B-UNDERSTANDING.md:456` — *"That is what makes **B-3** a build rather than a
  research project"*, in §4.3, which is entirely about reflexion models
- `docs/next/LAYER-B-UNDERSTANDING.md:510` — *"Murphy, Notkin & Sullivan … **adopt** → skill,
  underpins **B-3**"*
- `docs/next/LAYER-B-UNDERSTANDING.md:538` — *"`.claude/skills/reflexion-conformance/` … Underpins
  **B-4**"*

**B-3** is the RLS policy proposal (`:693`); **B-4** is the reflexion model (`:694`). Two of the
three are wrong, and the ordering paragraph at `:715` (*"B-4 is the one to argue about properly"*)
confirms B-4 is intended. The `reflexion-conformance` skill itself carries no proposal id, so
nothing outside `LAYER-B` propagates the error.

### 3.4 Two cross-document section references point at the wrong section

- `docs/next/LAYER-D-LIBRARY.md:217` — *"The match-and-miss ledger — a prerequisite, exactly as
  **Layer A §3.3** is"*. Layer A §3.3 is *"Style is structurally never elicited"*; the harness is
  **§3.4**.
- `docs/next/LAYER-D-LIBRARY.md:203` — *"for the same reason **Layer A §6** cannot"*, about
  retention. Layer A §6 is *Retrieval versus packing*; the retention constraint is **§8**.

Every other `Layer X §n` cross-reference in `docs/next/` — 39 of them — resolves correctly. These
two and `LAYER-B:92` (§2.3 above) are the exceptions.

### 3.5 No proposal contradicts another proposal outright

Checked pairwise across the obvious collision surfaces — caching (B-6 / C-5 / E-12 / F-2),
metrics harnesses (A-2 / C-12 / D-2 / E-2 / F-13), impact analysis (B-1 / C-6 / F-6), the
interaction gates (C-1 / E-7), the library (D-6 / D-9 against ADR-0016), and tenancy
(G-1 / G-2 / G-3). The only genuine incompatibility found is the **reason** behind B-6 versus the
C/E/F cache-floor table (§2.1), not the proposal itself: B-6 and C-5 want the same edit for
different arithmetic.

Worth noting as *nearly* a silent dependency: **G-3** (RLS on all fourteen models) and **E-7** /
**G-2** all assume `SCIO_VERIFY_DATA` defaults on, and E-7 states its blocker
(`LAYER-E-BUILD.md:956`: *"Blocked on Layer C's **C-1**, without which there is nothing to
drive"*). G-2's consequences paragraph (`LAYER-G-CROSS-CUTTING.md:984-988`) asserts the same
flip *"makes builds slower and more expensive"* and mentions the two Layer C criteria — but never
names **C-1** as its prerequisite. A reader working only from `LAYER-G` would turn the flag on
and find nothing to drive.

---

## 4 · Claims refuted elsewhere in the repo

### 4.1 `LAYER-E` refutes a claim `00-INDEX` and `LAYER-A` no longer make

`docs/as-built/LAYER-E-BUILD.md:225-226`, and again as item 5 of its "Documentation drift found"
list at `:481-485`:

> **The `A → E` edges are not what the index guessed.** `00-INDEX.md` and `LAYER-A-INTAKE.md`
> both attribute them partly to cost estimation.

Both cited documents were corrected *before* this was written and now say the opposite in as many
words: `00-INDEX.md:50-53` (*"~~Probably cost estimation.~~ **Wrong — corrected.**"*) and
`LAYER-A-INTAKE.md:91-94` (*"The `A → E` edges are **not** cost estimation… (Corrected 2026-08-26;
the first reading was wrong.)"*). `git log` confirms the order: `bb14a82 docs: correct what the
blind test caught` precedes `fffbfc7 docs: Layers C through G as built`.

So `LAYER-E`'s drift list contains an item that is not drift, aimed at two documents that agree
with it. A reader who trusts `LAYER-E` will go looking for an error that is not there.

### 4.2 `REVIEWS-WHAT-WE-MISSED` says the 35 findings were never verified; `REVIEWS-FINDINGS-VERIFIED` is that verification

- `docs/as-built/REVIEWS-WHAT-WE-MISSED.md:164-176` — *"## Still outstanding … The 35 findings in
  the two root reviews have **not** been verified one by one. Four have been checked, incidentally
  rather than systematically"*, followed by a four-row table
- `docs/as-built/REVIEWS-FINDINGS-VERIFIED.md:3-4` — *"The verification pass `RETHINK-BRIEF.md`
  step 4 demands and that had not been done. **Every finding in both root reviews, checked against
  current code.**"*, followed by 27 rows across four outcome tables

`git log` shows `9eb714e docs: what the reviews say that we missed` then `9e3bcc3 docs: the review
findings, verified one by one` — and **`9e3bcc3` touched both files**. The verification document
was added and the older document's "not verified" section was left standing in the same commit.

The `as-built` skill routes to both (`.claude/skills/as-built/SKILL.md:36-37`), so a session asking
"has finding X been checked?" can land on either answer depending on which row of the routing table
it matches.

### 4.3 `REVIEWS-WHAT-WE-MISSED` §1 corrects a `JOURNEY` document that has since been rewritten

`REVIEWS-WHAT-WE-MISSED.md:12-14` — *"Our `LAYER-F` and `JOURNEY-INVOLVED-PATH` **both name
Settings as the placeholder**"* — and `:38-40` — *"Our journey document concluded that the gap
sits at *the two ends* of the user's path. That is too kind."*

`JOURNEY-INVOLVED-PATH.md:90-92` now says *"**five routes are placeholders**, not one"* and lists
all five; `:224-225` now says *"The gap is not distributed evenly… **the entire post-reveal half
is unbuilt** — five placeholder routes, not one."* The journey document absorbed the correction
and the correcting document was never updated, so it still presents a fixed error as live. (The
`LAYER-F` half of the sentence does still stand — `LAYER-F-DESIGN-WINDOW.md:327-356` names only
`/live` and Settings.)

### 4.4 "`svix` is not installed" is true and beside the point — verified

- `docs/as-built/LAYER-G-CROSS-CUTTING.md:245-247` — *"The TODO names the library — *"`svix` is
  the library"* — and **`svix` is not installed**"*, and open question (c) at `:326-329`: *"Either
  install `svix` and verify, or remove the route"*
- `docs/as-built/REVIEWS-FINDINGS-VERIFIED.md:103` — *"`svix` absent from `package.json`"*
- `docs/next/LAYER-G-CROSS-CUTTING.md:58-93` — *"**The webhook TODO is obsolete: the verifier is
  already installed.** … `@clerk/backend: ^3.16.1` … declares **`standardwebhooks: ^1.0.0` as a
  direct dependency** and exports a `./webhooks` entry point"*

**Verified**: `apps/api/package.json:16` declares `@clerk/backend: ^3.16.1`, and
`node_modules/.pnpm` contains `standardwebhooks@1.0.0`. The forward document is right and the
as-built open question is now answerable in one direction — G-5's *"No new dependency"* is
correct. Neither as-built file records this, so a session reading only `docs/as-built/` will
schedule a dependency decision that does not exist.

### 4.5 "No rate-limit handling" is half wrong — verified at source by the later document

- `docs/as-built/LAYER-E-BUILD.md:369-371` — *"**No rate-limit handling.** `_complete_with_retry`
  retries once with a 0.2s linear sleep and has no 429 branch … `grep -rn "429\|rate_limit"`
  returns nothing"*
- `docs/next/LAYER-E-BUILD.md:312-324` — *"the as-built is half right, and the half it misses
  matters. … `AnthropicProvider._complete` constructs `AsyncAnthropic(…)` (`provider.py:169`)
  without overriding `max_retries`, and the SDK's default is **2 retries on 408/409/429/5xx with
  `Retry-After` honoured**. The Anthropic path *does* have rate-limit handling; it is inherited,
  invisible and untested."*

A genuine "later document verified what an earlier one inferred from a grep". The as-built entry
still reads as an absolute absence.

### 4.6 `LAYER-E`'s "correction (a)" corrects nobody

`docs/next/LAYER-E-BUILD.md:58` opens its nine corrections with *"**(a) `test_interaction_channel.py`
does not have 36 passing tests.**"* No as-built document claims it does:
`LAYER-E-BUILD.md:488-489` says *"(36 — 9 skipped)"* and `LAYER-F-DESIGN-WINDOW.md:431` says
*"36 collected; 27 passed, 9 skipped"*. The only bare 36 is `00-INDEX.md:70`, in a table column
headed "Tests" that is a collected count everywhere else in the same table. Listed here because a
"correction" that corrects nothing is indistinguishable, later, from one that did.

---

## 5 · Gaps visible only across documents

### 5.1 A verified-still-true finding with zero forward coverage: the unsandboxed preview iframe

`docs/as-built/REVIEWS-FINDINGS-VERIFIED.md:104` records **C-F10 / G-F12** under *"Verified: still
true"*:

> **2** `<iframe>` in `apps/app/src`, **0** `sandbox=` attributes

**Verified**: `apps/app/src/pages/RevealPage.tsx:154` and `apps/app/src/pages/DesignPage.tsx:635`;
`grep -rn 'sandbox=' apps/app/src` returns nothing. Those are the two iframes that render
**model-generated application code inside the Scio origin** — the preview the design window is
built around and the reveal's "try it".

`grep -ril iframe docs/next/*.md` returns **nothing**. Not Layer F, which owns the preview, the
bridge, the marking loop and 978 lines of forward analysis including a full competitor scan of
how Lovable, v0 and Figma Make render previews. Not Layer E, which owns the sandbox and proposes
a two-phase egress policy (E-9) for the *server* side of exactly this trust boundary. Not Layer G,
whose G-6 covers CI security and whose §3.1 is titled "The authorization model".

The finding is verified, live, in the layer with the most forward analysis in the repo, and no
proposal picks it up. It is only visible by putting `REVIEWS-FINDINGS-VERIFIED.md` beside
`docs/next/`, which is what nobody had done.

### 5.2 Three more verified findings that no forward document picked up

Same method — the "still true" table in `REVIEWS-FINDINGS-VERIFIED.md:95-107` against all seven
forward documents:

| Finding | Status | Forward coverage |
|---|---|---|
| **C-F05** · `enableShutdownHooks` — 0 occurrences in `apps/api/src` (**verified**) | still true | none. `grep -ri 'shutdown' docs/next/*.md` → nothing |
| **C-F11 / G-F12** · security headers — 0 helmet or CSP references (**verified**) | still true | half. G-6 (`LAYER-G-CROSS-CUTTING.md:937`) covers *"a guard on `/docs`"*; `grep -ri 'helmet\|CSP' docs/next/*.md` → nothing |
| **G-F10** · reveal may bind the wrong usage event | not verifiable statically | none |

`C-F03 / G-F05` (observability), `C-F06 / G-F07`, `C-F07 / G-F08`, `C-F08 / G-F06`, `C-F12 / G-F13`,
`C-F14`, `C-F15`, `G-F01`, `G-F03`, `G-F04`, `G-F09` and `G-F11` **are** all carried forward, most
of them by name. So the pickup rate is high and the misses are specific — which is what makes
them worth naming rather than a general complaint.

### 5.3 `docs/decisions/` does not exist, and 85 proposals plus the pipeline point at it

- `CLAUDE.md:61` — *"ADRs: one decision per file in `docs/decisions/`, numbered, with status"*
- `docs/next/README.md:17-18` — *"Every behavioural change lands as an ADR proposal … per
  `CLAUDE.md`: propose, do not assume"*
- `docs/PIPELINE.md:19` — stage 3 produces *"the architecture, plus the ADRs that record it"*
- `docs/OPERATING-MODEL.md:14` — `scio` holds *"`as-built/`, `next/`, `decisions/`, the graph, the
  skills"*
- `.claude/skills/brainstorm/SKILL.md:313-314` — *"Ideas that survive validation become proposals
  in the layer document's `## 9 · ADR proposals`"*
- `docs/as-built/01-DECISIONS.md:82` — *"Copy `0000-adr-template.md`"*

**`ls docs/decisions` → No such file or directory.** There is no directory, no template, no
numbering, and no ADR. Every one of the 85 proposals is written as *"becomes an ADR"* and there is
nowhere for one to become. `OPERATING-MODEL.md:14` describes the directory as already held.

This is the single largest thing every document assumes exists and no document owns. It is also
the cheapest to close.

### 5.4 `JOURNEY`'s feasibility check is asked for once and answered nowhere

`docs/as-built/JOURNEY-INVOLVED-PATH.md:200`, in the *Intended versus today* table:

> | 5 | Preview includes a **feasibility check** | Not found as a distinct step. Layer B's six rule
> checks are the nearest thing, and they run earlier |

`grep -rn feasibility docs/ --include='*.md'` returns **that line and nothing else**. No forward
document proposes it, refuses it, or explains that Layer B's validation is meant to be it. The
journey document is the only place in the repo that states what the user was promised at step 5,
and the question dies there. (The same line also carries the retracted "six rule checks" from
§1.2, so the one surviving statement of the gap is stated in a number the repo has corrected.)

### 5.5 Nothing owns the brand work

`docs/brand/MOTION-SCAN.md` (469 lines), `logo-sketches.html` and `logo-factory.html` are cited
exactly once outside their own directory: `OPERATING-MODEL.md:160` — *"Design —
`.claude/skills/app-design` plus the ongoing motion scan in `docs/brand/`."* No layer document,
no ADR proposal, no pipeline stage and no skill references them. `PIPELINE.md`'s seven stages have
no place for a mark, and `app-design`'s §6 (*"Where this belongs"*) routes tokens into Layer B's
playbook and the gate into Layer E, and says nothing about brand.

The scan itself is the most carefully hedged document in the repo — it separates measured from
quoted, marks four things it could not verify, and scopes its §7.2 defect finding to one of the
two sketch files. That quality is what makes the orphaning notable rather than tidy.

### 5.6 The "run document" is designed twice and owned by neither

`docs/PIPELINE.md:106-126` §5 *"The run document"* and `docs/OPERATING-MODEL.md:108-124` §3
*"The run document"* describe the same artifact, reach the same two conclusions (it is probably a
plugin; it must not pack), cite the same precedent (`as-built/SKILL.md`'s *"load in this order,
and stop"*), and give the same instruction (*"scan first"*). Neither says which document owns it.
They disagree only on the number of skills it must not load — thirteen and fifteen (§7.2).

`PIPELINE.md:125-126` adds *"Written after stage 7 reports"* — stage 7 is this review — so the
owner question becomes live now.

### 5.7 Nothing computes what the pipeline says it needs: a validation budget

`docs/PIPELINE.md:52-71` §2 is the sharpest paragraph in the repo:

> Every stage in this chain **adds** … `docs/next/` is already ~6,000 lines carrying roughly
> **90 ADR proposals** … **So validation needs a number, not a mood.** … *stage 3 receives at most
> N proposals per layer, ranked, with every rejection carrying its reason.*

Stage 2 (Validate) is **not started**, N is unset, and the `brainstorm` skill —
`.claude/skills/brainstorm/SKILL.md:162` — sets its own output budget (*"`Ship: <= 10 ideas`"*)
without reference to it. So the only budget that exists is one skill's self-imposed cap on its own
output, and the constraint `PIPELINE.md` says is the difference between an architecture that
considered its input and one that ignored it has no owner and no number.

---

## 6 · Skill drift and frontmatter defects

### 6.1 Two skills `LAYER-E` says were written do not exist

`docs/next/LAYER-E-BUILD.md:685-691`:

> **Skills specific to Layer E**, for the build process. **Two written**, and the reasons two
> others were not are part of the answer.
>
> | `execution-feedback-economics` | **new** — … | E-1, E-6 |
> | `sandbox-isolation` | **new** — … | E-8, E-9 |

`ls .claude/skills/` — neither exists. The sixteen present are: `ais-grounding`, `app-design`,
`architecture`, `as-built`, `brainstorm`, `change-impact-analysis`, `contract-retrieval`,
`design-rule-hierarchy`, `ears-requirements`, `graph-guard`, `graphify`, `ontoagent-elicitation`,
`reflexion-conformance`, `req-elicit-gym`, `reuse-classification`, `testing`.

For contrast, `docs/next/LAYER-C-BUILD-PLAN.md:628-633` uses the same table under the honest
header *"Changes made to `.claude/skills/` while writing this document"* and both of its rows are
real (`design-rule-hierarchy` exists; `ears-requirements` §6 exists). `LAYER-F-DESIGN-WINDOW.md:682-689`
and `LAYER-G-CROSS-CUTTING.md:718-720` hedge correctly (*"skills specific to Layer F"* as a
proposal list; *"**new, proposed**"*). Only `LAYER-E` asserts two files into existence.

This matters beyond bookkeeping: E-1 and E-6 are the two proposals that turn on measured evidence
about self-correction and test overfitting, and `LAYER-E:690` names the missing skill as the thing
carrying *"four evals a change to `codegen_passes` or `max_attempts` must pass"*. The evals do not
exist.

### 6.2 The `graphify` drift is real, still live, and cannot be fixed by re-fetching

`docs/next/SKILLS.md:55-57` records it:

> The vendored `graphify/SKILL.md` calls `check_semantic_cache` expecting three return values;
> the installed 0.9.50 returns four. Pin the package version and re-fetch the vendored file
> deliberately.

**Verified, and worse than recorded.** `.claude/skills/graphify/SKILL.md:155` unpacks three:

```python
cached_nodes, cached_edges, uncached = check_semantic_cache(all_files)
```

The installed `graphifyy==0.9.50` signature returns four —
`tuple[list[dict], list[dict], list[dict], list[str]]`, `return cached_nodes, cached_edges,
cached_hyperedges, uncached`. That line raises `ValueError` on every semantic run.

The recommended fix does not work. `sha256sum .claude/skills/graphify/SKILL.md` is
`f138783724b92036c211d4b3ed1799e8b7d6f071c0c477acd2d1861ccedaa2d3` — **byte-identical to the pin
recorded in `.claude/skills/graphify/README.md:8`**. The vendored file has not drifted from
upstream; *upstream* has drifted from the package. Re-fetching returns the same broken line.
`README.md` says *"Do not hand-edit it; re-run the fetch below instead"* (`:3-4`), which forecloses
the only fix available.

Two further inconsistencies around it:

- `SKILLS.md:56` says *"Pin the package version"*; `README.md:34` shows the bootstrap as
  `pip install graphifyy -q --break-system-packages` — unpinned — and `README.md` names no version
  at all. So the document recording the hazard and the document describing the install disagree
  about whether a pin exists.
- `README.md` does not mention the `check_semantic_cache` defect anywhere, while
  `.claude/skills/graph-guard/SKILL.md:111-115` and `docs/OPERATING-MODEL.md:43-47` both do. The
  one file a person editing the skill would read is the one that does not warn them.

### 6.3 `graph-guard`'s layer table would fire on four dependencies the as-built documents call legitimate

`.claude/skills/graph-guard/SKILL.md:67-79` declares the permitted cross-layer edges and says
*"Anything else is a finding."* Four of the as-built documents' own findings fall outside it:

| Table says | as-built says |
|---|---|
| `C build plan → may use: B, E primitives` | `LAYER-C-BUILD-PLAN.md:148` records **`C → D` 9** and **`C → G` 4**, and `:164-167` calls `C → D` deliberate — *"the library is asked before the build, not during it"* |
| `F design → may use: E, G` | `LAYER-F-DESIGN-WINDOW.md:225-229` records **`F → B` 13** and **`F → A` 3** and concludes *"Both are legitimate"* |
| `E build → may use: C, D` | `LAYER-G-CROSS-CUTTING.md:166-169` records `build.service.ts:24` importing `UsageService` — a real **E → G** edge the graph missed |
| `G cross-cut → may use: nothing above it` | `LAYER-G-CROSS-CUTTING.md:163-164` records **`G → D` 2** — *"`engine.client.ts` and the library verification client"* |

The skill is honest that a finding *"is **not** auto-rejected — some are legitimate and the table
is what should change"* (`:77-79`), so this is not a bug so much as a table written without
reading the four layer documents that already answered it. It is listed because
`.claude/skills/architecture/SKILL.md:83` cites graph-guard as the mechanism that *"enforces the
boundaries"*, and `docs/next/SKILLS.md:51` marks graph-guard *"written, not yet exercised"* — so
the first exercise would produce four false positives against documents that pre-emptively
refuted them.

### 6.4 `SKILLS.md` promises `intake-replay` reports "the five metrics" — Layer A retracted that set

`docs/next/SKILLS.md:67`:

> `intake-replay` | runs Layer A's replay harness and reports **the five metrics**

`docs/next/LAYER-A-INTAKE.md:296-321`:

> **The previous draft invented five metrics.** Retracted; three published ones exist, from
> ReqElicitGym … **IRE · ESR · TKQR** (plus **ORA**, in the repo, not the paper) … Three
> Scio-specific metrics stay …

So the retracted set is what the skill roster still specifies, and A-2 (`:682`) requires the
opposite — *"no change to Layer A ships without moving IRE / ESR / TKQR against a named
baseline"*. `docs/next/LAYER-D-LIBRARY.md:461` then refers to *"the Layer D twin of
`intake-replay`"*, propagating the name of a skill that does not exist and whose specification is
retracted.

### 6.5 `OPERATING-MODEL`'s skill roster names three skills that were built under other names, and parks one that was built

`docs/OPERATING-MODEL.md:94-104`:

| Roster entry | Verdict given | Reality |
|---|---|---|
| `architecture-patterns` | *"earns it only as the list + selection procedure"* | built as **`architecture`** — and it *is* the list plus the procedure, so the verdict was met and the name was not updated |
| `test-design` | *"earns it, and it has a specific job"* | built as **`testing`** |
| `brainstormer` | *"**weakest** — this is a prompt, not a procedure … **Park it until it has one**"* | built as **`brainstorm`**, 465 lines, with a method, a retrieval budget, a parseable output contract and six evals |
| `data-model` | *"earns it"* | not built. `docs/next/LAYER-G-CROSS-CUTTING.md:720` proposes **`tenant-isolation`** instead, a different scope, with no reference to `data-model` |
| `skill-writer` | *"**strongest candidate**"* | not built. `PIPELINE.md:16` still lists it as a stage-0 deliverable |

The `brainstorm` row is the sharp one: the roster's standing verdict is *park it*, and the file
exists and is one of the three most substantial skills in the repo.

### 6.6 Frontmatter: one defect across sixteen skills

Checked mechanically on all sixteen `SKILL.md` files.

- **`name` matches the folder exactly** — 16/16. No defects.
- **No angle brackets anywhere in frontmatter** — 16/16 clean.
- **`description` present** — 16/16.
- **`description` says *when* to use it** — 15/16. The exception is **`graphify`**:

  ```yaml
  description: any input (code, docs, papers, images) → knowledge graph → clustered communities → HTML + JSON + audit report
  trigger: /graphify
  ```

  That is a pipeline diagram, not a triggering condition. `docs/next/SKILLS.md:39-42` states the
  rule and the reason: *"A description that says only what a skill does will never fire."* It also
  carries an extra `trigger:` key that no other skill has and that `SKILLS.md:28-29` describes as
  *"optional and spec-compliant runtimes ignore keys they do not recognise"* — so the skill's only
  documented invocation path is a field the format says may be ignored.

  The mitigating fact: `graphify` is vendored verbatim at a pinned sha, so fixing the description
  means hand-editing a file `README.md:3-4` forbids hand-editing. That is the same trap as §6.2,
  and it is the second reason the vendoring policy needs a decision rather than a re-fetch.

  **Independently confirmed.** `docs/TOOLING-SCAN.md:399-405` reaches the same three findings
  from the other direction — the description says only what the skill does, the `trigger:` key is
  *"not in the frontmatter reference and is not part of the Agent Skills spec's six fields"*, and
  the vendored copy drifts from the installed package. Two reviewers, arriving separately at the
  same defect on the same day, is the strongest evidence in this document that it is real.

### 6.7 Small skill-to-document mismatches

- **`.claude/skills/as-built/SKILL.md:57-64`** lists **five** State verdicts (adding *"Deliberate,
  easy to break by accident"*). `docs/as-built/README.md:26` and `CLAUDE.md:24` list **four**
  (*"solid · wrong-shaped · missing · obsolete"*). The seven layer documents all use five, and
  `PIPELINE.md:90-99` builds its copy rule on five. The two four-item lists are the stale ones,
  and one of them is `CLAUDE.md`.
- **`.claude/skills/brainstorm/SKILL.md:17`, `:349`, `:418`** cite
  `docs/next/LAYER-A-INTAKE.md:188` as the invented-coverage-formula example, three times. The
  retraction is at `:184`; `:188` is the ISO 29148 paragraph. The example is right, the line is not.
- **`.claude/skills/architecture/SKILL.md:83`** says graph-guard *"enforces the boundaries"*.
  `docs/next/SKILLS.md:51` says graph-guard is *"written, not yet exercised — no code in this
  repo"*, and there is no code and no hook installed. Present tense for something never run.
- **`.claude/skills/testing/SKILL.md:247`** states the rule *"`27 passed, 9 skipped` is never
  reported as `36 tests pass`"* while `00-INDEX.md:70` lists `test_interaction_channel | 36` in a
  column headed **Tests**. The column is a collected count throughout, so this is a labelling
  question rather than an error — but the skill's rule is stated absolutely, and the index is the
  first thing every session reads.
- **`.claude/skills/architecture/SKILL.md:3`** advertises *"fourteen patterns"*; the table at
  `:81-96` has exactly fourteen rows. **Verified, correct** — noted because it was the kind of
  count that has gone wrong four times elsewhere.

### 6.8 `TOOLING-SCAN.md`'s central "ours is better" claim is off by two

`docs/TOOLING-SCAN.md:380-381`:

> **Ours is better on provenance, and it is not close.** **Fifteen of our sixteen** skills open
> with a `## 1 · Source` heading naming authors, venue and date, and carry an explicit Limits
> section separating what a paper shows from what we are assuming.

**Verified**: **thirteen** of sixteen do. `as-built`, `graph-guard` and `graphify` have no Source
heading. The point survives — thirteen is still remarkable against the 289 official and 2,282
community plugins the scan searched — and a defensible reading is that the three exceptions are
not research-derived skills, so the four-part contract was never meant to apply to them. But the
sentence as written is a count, it is presented as the document's headline finding, and it is
wrong by two.

Two of its other counts check out exactly: **zero** `evals/` directories across sixteen skills
(`:392`), and `graphify/SKILL.md` at **1,204 lines** (`:394-395`). Both verified.

---

## 7 · Stale status

### 7.1 `docs/next/README.md` describes seven headings; every document has nine

`docs/next/README.md:7-16` — *"One document per layer, same seven headings"* — then lists: 1 Where
the layer stands · 2 Refining what exists · 3 What is missing · 4 The means · 5 Token economy ·
6 Data worth owning · 7 ADR proposals.

All seven `docs/next/LAYER-*.md` carry **nine**. `§4 · Out of the box` and `§6 · Retrieval versus
packing` were inserted, pushing The means to §5, Token economy to §7, Data worth owning to §8 and
**ADR proposals to §9**. Verified across all seven files.

`docs/next/README.md:17-18` then says *"Every behavioural change lands as an ADR proposal in
**§7**"*, which now points at Token economy in every document it governs. `README.md:20` compounds
it: *"**Two axes** run through every document"* followed by **three** bullets — the third being
Retrieval versus packing, which is the §6 the heading list omits. The document knows about the
section and still counts it as an axis rather than a heading.

`.claude/skills/brainstorm/SKILL.md:313-314` gets it right: *"proposals in the layer document's
`## 9 · ADR proposals`"*.

### 7.2 Five documents give five different counts of how many skills exist, and only the newest is right

| Where | Count | Reality |
|---|---|---|
| `docs/next/SKILLS.md:48-53` — *"Ours today"* table | **four** (`as-built`, `graph-guard`, `graphify`, `app-design`) | 16 |
| `docs/OPERATING-MODEL.md:120` | *"**thirteen** skills"* | 16 |
| `docs/next/LAYER-G-CROSS-CUTTING.md:715` | *"`.claude/skills/` holds **thirteen** (counted, 2026-08-26)"* | 16 |
| `docs/PIPELINE.md:120` | *"**fifteen** skills"* | 16 |
| `docs/TOOLING-SCAN.md:380`, `:392` | *"our **sixteen** skills"* | **correct** |

`TOOLING-SCAN.md` is the newest document in the repo and the only one that has the number right,
which is the shape of the problem rather than an exception to it: the count is correct in the
document written after the skills landed and stale in the four written before, and the commit
that added the three skills (`d56d1a7`) updated none of them.

The `LAYER-G` line is the instructive one: it was correct when written — `git log` shows
`d56d1a7 skills: brainstorm, architecture and testing` is the newest commit in the repo, and
13 + 3 = 16 — and it is labelled *"(counted, 2026-08-26)"*, the same date. So a count taken and
dated on the day it was taken went stale within the same day, and the commit that made it stale
touched neither it, nor `SKILLS.md`, nor `PIPELINE.md`, nor `OPERATING-MODEL.md`.

`SKILLS.md` is the worst of the five: it is the document whose stated job is *"This document holds
all of them"* (`:3-5`), and it lists a quarter of them. Twelve skills — including the nine that
`SKILLS.md`'s own rule (*"Every paper we actually adopt becomes a skill"*, `:77`) generated — do
not appear anywhere in it.

`SKILLS.md`'s *Proposed* section is stale in the other direction: `layer-audit` and `adr-propose`
(`:68-69`) are still listed as future work, and its research-skill candidate table (`:96-102`)
lists OntoAgent, LLMREI, ClarifySTL, DSPy and hierarchical summarisation — while **nine**
research-derived skills now exist (`ais-grounding`, `change-impact-analysis`, `contract-retrieval`,
`design-rule-hierarchy`, `ears-requirements`, `ontoagent-elicitation`, `reflexion-conformance`,
`req-elicit-gym`, `reuse-classification`) and exactly one of them — `ontoagent-elicitation` — is on
that list. LLMREI and ClarifySTL appear nowhere else in the repo.

### 7.3 `PIPELINE.md`'s stage table is behind its own repo

`docs/PIPELINE.md:14-23`:

| Stage | Says | Reality |
|---|---|---|
| 0 · Tooling | *"`brainstorm`, `architecture`, `testing`, `skill-writer` skills — **3 in progress**"* | three of the four are **written and committed** (`d56d1a7`); `skill-writer` is not started |
| 1 · Brainstorm | *"skill in progress"* | `.claude/skills/brainstorm/SKILL.md` exists, 465 lines |
| 3 · Architect | *"skill in progress"* | `.claude/skills/architecture/SKILL.md` exists, 395 lines |
| 6 · Test | *"skill in progress"* | `.claude/skills/testing/SKILL.md` exists, 465 lines |
| 7 · Review | *"running now"* | correct — this document |

`PIPELINE.md:39` also lists five skills as living in `scio` (`brainstorm`, `architecture`,
`testing`, `as-built`, `graph-guard`) in a table whose purpose is deciding which repo each skill
belongs to. Eleven skills are absent from that decision, including `graphify` — the one skill
whose repo placement `README.md` argues about at length.

### 7.4 `docs/as-built/README.md`'s phase table is complete and the directory is not

`docs/as-built/README.md:54-62` lists five phases, all *done*, ending at *"5 · Blind test with a
fresh agent | done — failed on two stale claims in `00-INDEX.md`, corrected"*. The directory has
since gained `JOURNEY-INVOLVED-PATH.md`, `REVIEWS-WHAT-WE-MISSED.md` and
`REVIEWS-FINDINGS-VERIFIED.md` — three documents, three commits, no phase row. The "How to use
this directory" table at `:9-15` lists `JOURNEY-INVOLVED-PATH.md` but neither REVIEWS document,
while `.claude/skills/as-built/SKILL.md:36-37` routes to both. So the directory's own README and
the skill that navigates it disagree about what is in it.

### 7.5 Claims that are no longer "not yet"

- `docs/as-built/LAYER-G-CROSS-CUTTING.md:326-329` — open question (c), *"install `svix` and
  verify"*. Answered: the verifier is already installed (§4.4).
- `docs/OPERATING-MODEL.md:102` — *"`brainstormer` … **Park it until it has one**"*. It has one
  (§6.5).
- `docs/next/README.md:38-46` — the per-layer status table reads `done` for all seven, which is
  accurate. Noted as the one status table in the repo that is current.

---

## 8 · What is consistent

Stated at length because a review that only lists faults misrepresents the repo.

**The as-built ↔ next boundary holds.** Every one of the seven forward documents opens by naming
its as-built counterpart as its starting point, and five of them open §1 with an explicit
*"corrections to the as-built record"* section. The corrections are specific, cited to
`file:line`, and — with the exceptions in §4 — genuine. That is the mechanism working as designed;
the failure is only that corrections do not propagate *back*.

**The constraint paragraphs work.** `LAYER-A:46` (*"Any change that lets the model decide which
required field gets asked is out of scope"*), `LAYER-C:52-53` (*"Proposals may add rules; they may
not move a rule into a prompt"*), `LAYER-D:41-42` (*"Proposals may change what is **retrieved**;
they may not change what **decides**"*), `LAYER-E:49-51`, `LAYER-F:69-71` — five documents, five
statements of the deterministic-first boundary, no contradiction between them and no proposal
found that violates its own layer's constraint. `01-DECISIONS.md`'s settled ADRs are engaged
rather than routed around: `LAYER-G-CROSS-CUTTING.md:967` refuses Cedar as a runtime *"because
changing it supersedes an accepted ADR for no user-visible gain"*, `LAYER-B:125-127` refuses to
ship Zanzibar into generated apps *"against ADR-0011's fixed stack"*, and `LAYER-E:957` (E-8)
explicitly names ADR-0004↔ADR-0005 as *"a tension between two ADRs [that] must be written as one"*.

**The graph numbers reconcile.** 5,173 nodes / 12,054 edges appears in six documents and matches
the file. The per-layer edge counts in `00-INDEX.md:33-44` are independently recomputed and
reproduced in `LAYER-D-LIBRARY.md:177`, `LAYER-F-DESIGN-WINDOW.md:185-187` (*"reproduce the index's
73 and 70 exactly"*) and `LAYER-C-BUILD-PLAN.md:141-148`, with the two known extraction artifacts
(`D → E`'s conflated `_normalise`, `E → G`'s missing TypeScript edges) named in both directions.

**The structural totals agree everywhere** (with the one exception in §1.13). 155 files /
22,990 lines / seven layers; the verified baseline of engine 640 passed / 21 skipped, API 135,
app 109 is carried identically into `.claude/skills/as-built/SKILL.md:86-87`; and the 22,990 /
"~23,000 lines" figure reaches `.claude/skills/architecture/SKILL.md:88` and
`OPERATING-MODEL.md:13` unchanged.

**The honesty discipline is uniform and unusual.** Every forward document ends with a footer
distinguishing measured from estimated from read-at-abstract-level, every one of them flags
chars÷4 as an estimate with a stated error bar and names `count_tokens` as the correct instrument,
and three of them (`LAYER-A:325-330`, `LAYER-E:702-707`, `LAYER-F:700-707`) carry an explicit
"honesty rule" paragraph stating what a cited number does *not* support. `MOTION-SCAN.md:31-43`
carries a "Could not verify" list. `LAYER-F:163-178` re-runs a flaky test eight times and then
argues the result is *weak* evidence. That is a standard most engineering repos do not hold, and
it holds across authors.

**The product-invariant thread is coherent.** The five `PRODUCTION_READINESS_DIFF.md` §2
invariants surface first in `REVIEWS-WHAT-WE-MISSED.md:42-59`, then in `LAYER-A:76-81` (identity),
`LAYER-B:64-75` (impact analysis), `LAYER-C:19-20` (consumer), `LAYER-F:398-412` (invariant #2),
each time with the same numbering and the same text, each time adding rather than restating.
Likewise the nine-item reveal spec: named in `REVIEWS-WHAT-WE-MISSED.md:67-77`, then assessed in
`LAYER-E:512-531`, `LAYER-F:356-380` and `LAYER-G:661-667` — with the arithmetic disagreement in
§1.6, but with the same nine items every time.

**The system-wide pattern is stated identically by six documents.** *"The system computes an
honest signal and drops it before it reaches anyone"* — `ARCHITECTURE-AS-BUILT.md:61-83`,
`LAYER-E:102-103`, `LAYER-F:30-33`, `LAYER-G:633-635`, `LAYER-C:491-516`, `LAYER-D:259-276`. Six
authors, one diagnosis, five different instances of it, no contradiction.

**Frontmatter is clean.** 16/16 on name-matches-folder, 16/16 on no angle brackets, 15/16 on
description-says-when.

---

## Method and limits

**What was read.** All 29 markdown files under `docs/` (≈10,400 lines, including
`TOOLING-SCAN.md`, which arrived mid-review — see below), all 16 `.claude/skills/*/SKILL.md` plus
`graphify/README.md` (≈4,300 lines), `CLAUDE.md`, `README.md`.
`docs/brand/logo-sketches.html` and `logo-factory.html` were **not** read — only
`MOTION-SCAN.md`'s findings about them, so §5.5 is about the scan's placement in the repo, not
about whether its defect findings are right.

**How.** An index of factual claims — counts, file:line citations, verdicts, proposal ids,
prices, cross-references — was built while reading, then cross-checked against itself rather than
by re-reading. Cross-document references (`Layer X §n`, `[A-G]-n`, skill paths, section counts)
were extracted mechanically and resolved one by one.

**What was verified against `hello-world`.** Read-only, nothing modified. `layerc/validate.py` and
`layerb/validate.py` (rule counts and severities), `schema.prisma` (14 models, 8 `UsageKind`
values), `packages/shared/src/entities.ts` (5 values), `execution/matrix.yaml` (Sonnet 5 at
$3/$15), `execution/relay.py` and `builder/loop.py` (ceiling location), `apps/api/package.json`
and `node_modules/.pnpm` (`standardwebhooks@1.0.0`), `apps/api/src` (`NotImplementedException`
counts, no helmet, no `enableShutdownHooks`), `apps/app/src` (five placeholders, two iframes, no
`sandbox=`, zero `checks_passed`), and the installed `graphifyy==0.9.50`
(`check_semantic_cache` returns four). The graph was loaded and its node/edge counts confirmed.

**What was not verified.** Test counts were not re-run — §1.10 is an arithmetic inconsistency
*inside* `LAYER-E-BUILD.md`, which holds regardless of what the suite actually reports, but which
of "247" and "240" is right was not established. Token measurements (chars ÷ 4) were not
re-measured; §1.9's one-token gap is reported as an inconsistency, not adjudicated. External
claims — paper results, competitor behaviour, CVE scoring, model prices, cache floors — were
checked only for **internal** consistency across documents; where documents disagree about an
external fact (§2.1's cache floor) this review says which document the repo's own majority
follows, not which is true of the Anthropic API. `PRODUCTION_READINESS_DIFF.md`,
`PRODUCTION_READINESS_REVIEW.GPT.md`, `PRODUCTION_READINESS_REVIEW_CLAUDE.md`, `docs/STRATEGY.md`
and `docs/UX-FLOW.md` live in `hello-world` and were **not** opened — every claim about them here
is a claim about how two or more scio documents quote them, which is the only thing this review is
scoped to check.

**Known blind spots.** Prose-level contradictions between long analytical passages that use
different vocabulary for the same thing would not have been caught by an index of measurable
claims; §2 is thin partly for that reason and partly because, on inspection, the documents
genuinely do not reason to opposite conclusions very often. Reading order was
`as-built` → `next` → skills → the three loose `docs/*.md`, so a contradiction introduced by the
loose documents against something read early had one pass rather than two.

**One thing that happened during the review.** `docs/TOOLING-SCAN.md` (482 lines) was written and
committed by another session while this review was in progress — commit `832aeb2 docs: tooling
scan — what to adopt and where it attaches`, landing after most of this review's index had been
built. It was read and cross-checked afterwards, and its findings are folded into §6.6, §6.8 and
§7.2; it is the only document in the repo with the right skill count. It has had **one pass, not
two**, so it is the least thoroughly reviewed document here, and a contradiction between it and
something read early would more likely have been caught than one in the other direction.

*Reviewed 2026-08-26. Nothing was fixed, committed, or pushed. No file other than this one was
written.*
