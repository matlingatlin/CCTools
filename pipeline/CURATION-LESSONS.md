# CURATION LESSONS — the operating journal of running this knowledge base and library

**What belongs here:** a lesson from *doing* the work — running a curation pass, a watcher batch,
an ingest, a build, a graph, a source fetch, a measurement. Dated, one entry per lesson, newest
appended at the end of the section for its pass.

**What does NOT belong here:** a directive a test author applies before writing a suite. Those go
to `pipeline/TEST-AUTHORING-LESSONS.md`, which both the `library-curator` and the loop's TEST step
read *before* authoring tests. If your entry is addressed to the next test author, it is in the
wrong file.

**Why there are two files.** Until 2026-09-12 there was one, named `CURATION-LESSONS.md` and
headed `# TEST-AUTHORING LESSONS`. A writer looking for where curation lessons go greps the
filename, lands on a header about tests, and appends anyway — which is not a careless reader but a
name that misroutes one. Measured on 2026-09-12: of 22 entries added that day, **3** were about
authoring tests, and the dilution ran roughly 85 entries deep. A test author instructed to read
that file before writing tests was reading a session journal to find the three lines addressed to
them, which is `steering-doc-pruning`'s failure exactly: a document with a named reader, diluted
until the reader pays for content addressed to someone else.

The split renamed the file to match its header, gave this name back to the job it always promised,
and **promoted the nine journal entries that were genuinely about test authoring** into the other
file's directives rather than leaving them here to be missed. The measurement, the three options
considered and their costs: `pipeline/reviews/2026-09-12-lessons-file-dilution.md`.

**Deliberately not rewritten by the split:** eval records under `.claude/skills/*/evals.md`, the
contract fixtures under `pipeline/packages/fixtures/`, the build artefacts under
`pipeline/builds/`, and `pipeline/metrics.jsonl`. Each is a record of what a run actually saw, and
a fixture in particular asserts specific content — editing one to match a rename would weaken the
test it exists to be. They name the old path because the old path is what was true then.

## 2026-08-28 · Curator-batch mätt men EJ körd — W var mättad av piano-vågen

`W_MAX_AGENTS=2` är GLOBAL och delad. (**Taket är 4 sedan 2026-09-01, mätt** — lärdomen om delat tak står, siffran i den här posten är historik.) Piano-cronen fyrade fem minuter före kuratorn och hade
redan två scouter i luften, så fan-out enligt STEG 4 hade blivit tre samtidiga mot ett mätt tak
av två. Batchen är därför **mätt och köad, inte körd**. Det är ett medvetet uppskov, inte ett
missat trigger-fyrande.

**Kuratorprompten har ruttnat igen — tredje gången.** Den säger *"~70% av våra defekter är
tysta"*. `signals.py` säger **84% (67/80)**. Prompten varnar själv för precis detta (*"en
schemalagd prompt är en fryst kopia som ingen read-back når"*) och ber en säga till. Sagt.
Följ signalerna, inte prompten.

**STEG 3(a), mätt:**
- Talanger utan `evals.md`: **0**.
- SKILL.md nyare än senaste testning: 23 — men det är en ÖVERSKATTNING, och cronens egen regel
  skiljer redan på fallen. Diffat frontmatter-nycklar + brödtext mellan testdatumet och nu:

**Ren beskrivningsändring → bara triggerkontroll (16):** agent-blast-radius-guard,
context-budget, cost-aware-model-routing, decision-council, graphify-harvest, llm-call-ledger,
llm-eval-harness, llm-judge-calibration, loop-design-check, measured-optimization-loop,
repo-map, test-coverage, test-driven-development, unified-memory, update-codemaps,
verification-before-completion. Dessa fick NOT-klausuler när vågens fem nya talanger stängde
sina gränser åt båda håll. Metoden är orörd.

**Substantiell metodändring → KRÄVER omtestning (7):** eval-harness, library-curator,
mlops-production-review, piano, skill-description-optimizer, subagent-driven-development,
systematic-debugging.

Det är nästa batchs kö. Att köra alla 23 hade kostat tre gånger så mycket för samma resultat.

- `[2026-09-04]` **A number without its column header is not evidence.** Verifying "SWE-bench
  Verified Qwen3.6-35B-A3B 70.1" against the vendor's card, `70.12` was found in seconds — in a
  six-column table. Only reading the header row (`| Task | Nemotron… | Qwen 3.6 35B A3B | …`)
  turned "the figure appears on the page" into an attribution. Finding the number is the easy
  half; the claim is the number PLUS whose column it sits in.
- `[2026-09-04]` **Test every absolute — one counterexample ends it, and a table offers as many
  chances as it has rows.** A note said a model "loses on every row of NVIDIA's own table".
  Checked: 13 of 14 rows lose, one wins (IFBench loose, 71.88 vs 63.71). The note's actual
  argument survived; the absolute did not. "Every", "always" and "never" are the cheapest claims
  to write and the cheapest to refute, so write them last and check them first.
- `[2026-09-04]` **A verdict records PROVENANCE, not confidence.** Four claims were marked
  REPEATED to mean "small sample, treat with care" when they were our own measurements at n=2 and
  n=3. `claims.contract.json` reserves REPEATED for *the source restates a finding measured by
  someone else* and says outright the two "are not strong and weak". The cost was concrete: a
  verification queue ranked on REPEATED counts sent a reader after work that did not exist,
  because no source existed to re-read. Carry uncertainty in the stated **n**, never in the
  verdict. `kb.py lint` now flags a REPEATED line with a sample size and no other measurer named.
- `[2026-09-04]` **A join key exists so that guessing is unnecessary — and every time it was
  skipped, the number was wrong.** Three crude string-matches lied in one day: raw-layer coverage
  came out as 11%, 61% and 0% by three defensible methods; an "unwatched URLs" count included
  pages already watched under their `.md` twin; and a "is a source held" column read zero for
  every note. Each was fixed by using the real mapping (`WATCH.tsv`'s URL→path) instead of
  matching mangled filenames. If a number is derived by fuzzy matching, report the method with
  it — or better, build the key.
- `[2026-09-04]` **An ownership move keeps the old URL alive, so nothing breaks to tell you.**
  Two projects changed hands under their notes in one day: graphify (`safishamsi` ↔
  `Graphify-Labs`) and goose (`block` → `aaif-goose`). GitHub follows a transfer and serves
  **byte-identical** content, so no fetch fails, no hash moves, and a content-watcher is
  structurally blind to it. The signal that does move is the project's own self-links —
  `kb.py owners` reads them out of the stored READMEs, and the strength of a hit is the ratio
  (4-of-4 self-links is a move; 1-of-1 is a mention).
- `[2026-09-08]` **A check that reports two populations as one ranks the wrong work — and it
  happened again, one layer up from the verdict lesson above.** The related-only rule reported
  **212** unargued edges. Split against the graph: **76** were the reciprocal half of an edge
  already argued at the other end — which this repo *requires*, since a new note's neighbours
  must name it back — and 2 were argued in a source's `note:` field. The debt was **134**, and
  those turned out to be exactly **67 symmetric pairs**: two notes naming each other, neither
  saying why. Same shape as the REPEATED-verdict finding four days earlier: a label doing two
  jobs, invisible until someone split the population. The rule now reports only the 67, by
  name, so the count is a worklist.
- `[2026-09-08]` **The KIND of link decides an ownership move; the COUNT does not.** The
  `owners` check shipped with the heuristic "4-of-4 self-links is a move, 1-of-1 is a mention".
  Both standing candidates were settled the same afternoon and went **opposite ways**, decided
  entirely by what the links were. goose's four are a CI workflow badge, a
  `releases/download/stable` URL and two `blob/main` docs — every one 404s at a wrong address,
  so the README carrying them is maintained *there*, and our `block/goose` citation was stale.
  graphify's one is a `git clone` line the rename left behind, and its other two `safishamsi`
  URLs are a sponsors page and a gumroad book — personal accounts, correctly personal. The
  ratio would have called the weak case a mention and the strong case a move by luck. A live
  link is load-bearing; an inert one can rot for years.
- `[2026-09-08]` **A 401 to the fetcher is not an answer about the source — try the other
  surface.** Ornith-1.5's licence and owning org sat REPEATED for six days because the rendered
  Hugging Face model card returned 401. The same card answers at `/raw/main/README.md`, and the
  three `config.json` files with it. The re-read **refuted** the claim both secondary sources
  agreed on (weights under `deepreinforce-ai`; the HF API returns zero models for that org),
  upgraded five others to MEASURED, and turned up something no source had said at all: all
  three models are **vision-language**, not text. Two secondaries agreeing is not corroboration
  when neither read the primary — and the primary was one URL shape away the whole time.
- `[2026-09-08]` **A failed fetch is a dated observation, not a property of the source — and
  "not fetched" in a source line is a worklist, not a disclaimer.** Five claims came off the
  REPEATED tail in one pass, and the surface for every one of them was named in the note
  itself: a Hugging Face card that returned 401 (Ornith-1.5), an arXiv paper "not read"
  (Unlimited-OCR, and again for ICM/MWP), three READMEs "not fetched" (the context-window
  tools), and an arcprize.org page that "did not render its numbers to two fetchers". All five
  answered. Two of them answered at a *different shape of the same URL* — `/raw/main/` instead
  of the rendered page — and one simply answered on a later day. Order the verification queue
  by **whether an untried surface exists**, not by how weak the claim looks: the weakest claims
  in the base are the ones with no surface at all, and they are the ones that will never move.
- `[2026-09-08]` **When the claim is a RATE, fetch the index, not the page.** "v0.30 with
  frequent breaking changes" needed a time series, and a README is a snapshot. PyPI's release
  index settled both halves at once: `graphiti-core` is at 0.30.1 (so the version belonged to
  Graphiti, not to the project the bullet sat under), and the cadence went 10 releases in
  January 2026 → 6 → **one a month**, two in the last ninety days. The review was accurate when
  written and is now a warning about a project that has settled down. A registry, a releases
  feed or a commit history answers "how fast", where a page can only answer "what now".
- `[2026-09-08]` **An inference about provenance is not provenance, and it fails differently
  from a wrong number.** A note marked the ICM layer figures REPEATED with the reasoning "these
  come from secondary write-ups, not the abstract". They are Figure 1 of the paper. The figures
  were right, the verdict was wrong, and no amount of re-reading the *secondaries* would have
  found it — only opening the primary the note had already admitted it never opened. Write the
  verdict from where you looked, never from where you assume the number came from.
- `[2026-09-08]` **Three times in one pass the unread source was MORE careful than our summary
  of it.** code-review-graph disowns its own headline baseline as "an upper bound no real agent
  pays", publishes the benchmark where it "reports ratios below 1", and re-captured its numbers
  *downward*; the Unlimited-OCR paper names its own failure mode and calls its speed table a
  "theoretical ceiling"; the ICM paper scopes cross-model evaluation out as future work. The
  carousel, the video and the write-up were the lossy layer — not the primary. Scepticism aimed
  at the source rather than at the summary of it points the wrong way.
- `[2026-09-08]` **A registry hit on a matching name is not an identity check — and I made this
  mistake, in this repo, hours after writing the lesson above about verifying against primaries.**
  A correction cited "gbrain ships on npm at 1.3.1" as half its evidence. The npm package `gbrain`
  is `stormcolor/gbrain`, *"GPU Javascript Library for Machine Learning"*, created 2018-04-02 and
  last published 2018-11-15. The project it was being used to describe is Garry Tan's 2026 agent
  brain, whose README carries a warning about exactly that collision: *"GBrain is NOT distributed
  on npm … it can shadow the real binary on your PATH."* Read the `repository` field and the
  publish dates before treating a package as the same project. The conclusion survived on the
  other leg of the evidence, which is luck, not method — and the failure is instructive precisely
  because the previous lesson (fetch the index when the claim is a rate) is what led me to a
  registry in the first place. **A new instrument brings its own new failure mode.**
- `[2026-09-08]` **When two numbers about one project disagree, name the benchmark, not the
  number.** Switchyard travels as "74% cheaper". NVIDIA's own README reports Terminal-Bench 2.1
  against a $98.06 / 76.0% Opus 4.8 baseline: **13-30% cheaper at 71-76% accuracy**. Both are
  real; they are different suites measuring different things, and only one of them carries the
  accuracy cost (0.3 to 4.8 points) alongside the saving. The shape is the finding: the cheapest
  route is the least accurate and the most accurate is the least cheap. A number without its
  benchmark is not a claim, it is a badge — and a trade stated by the vendor is better evidence
  than a saving quoted alone.
- `[2026-09-08]` **A check's trigger must cover the check's own input — and the tell was a run
  count, not an error.** `kb-check.yml` fired on `knowledge/**` while `kb.py` indexes eight areas:
  666 documents, only 177 of them under `knowledge/`. **73% sat outside the trigger**, including
  `intake/`, which `selftest` asserts on directly. Nothing was red; what was visible was that a
  commit touching only `pipeline/` produced **one** CI run where every previous push had produced
  two. Asking *which* trigger had matched, instead of reading "green" and moving on, is what found
  it. The failure this prevents is not a missing check but a **delayed, mis-attributed** one: the
  breakage would have surfaced at the next unrelated `knowledge/` push and been blamed on that
  commit. The filter now lists every indexed area and `selftest` fails if `AREAS` gains a glob the
  workflow does not cover, so the pair cannot drift silently again.
- `[2026-09-08]` **Optimise what is PAID, not what is slow — and measure both before choosing.**
  Asked to optimise, the obvious target was runtime. Measured: `kb.py check` is 1.26 s, of which
  ~1.0 s is two full builds (`check` builds, then `selftest` builds again so it stands alone).
  Real redundancy — and **deliberately kept**, because that 1.26 s sits inside an 8-11 s CI job
  that is mostly checkout and `setup-python`. A 40% saving on 15% of a job nobody waits for is a
  number nobody pays. Recorded as a *keep* with its reason so it is not re-derived.
  What **is** paid is the always-on context surface, and it had never been measured:
  **~22,592 tokens, 2.26% of a 1M window** (`pipeline/queries/context_surface.py`, new).
  Repo bytes were measured the same way and produced a surprise worth keeping: the largest single
  line item in the repository's history is **`pipeline/STATUS.md` at 1,295,134 B packed over 43
  revisions — 30,119 B per revision**, against 14,689 for `CURATION-LESSONS.md`, 11,569 for
  `kb.py` and 9,470 for the largest note. Delta compression is working (30 KB stored for a 113 KB
  file); STATUS.md simply costs 2-3x per revision because it is edited *across its whole length*
  rather than appended at one end. Hypothesis, untested: a strictly append-only log would store
  roughly the appended bytes. Not acted on — restructuring the operation record is a judgement
  call, and this is the finding, not the fix.
- `[2026-09-08]` **"Nothing has broken yet" is a headroom question, and nobody had asked it.**
  CONSTANTS.md recorded the over-cap descriptions as spec-non-compliant but noted that "none is
  truncated by Claude Code today, which is why nothing visibly broke." True — and it was hiding
  the margin. Measured: `when_to_use` is used by **0 of 92** units, so the whole 1,536-character
  listing budget is the description's, and the largest sits at **1,446. Ninety characters.** Three
  are within a hundred. The failure is silent and self-inflicted in a nasty way: truncation takes
  the **tail**, the house style puts the NOT-clauses at the tail, so the next disambiguator added
  to one of those three is **removed by the act of adding it**, with nothing reporting it. When a
  document says a limit is not being hit, ask by how much — a violation with no margin is a
  different finding from a violation with room, and only one of them is about to become a defect.
- `[2026-09-08]` **Three optimisation passes, and the most useful output was three negatives.**
  Descriptions: an n-gram sweep found **0.16%** repeated phrasing, so there is no boilerplate to
  reclaim and any cut removes meaning. Bodies: measured against the four incompatible length bars
  the sources give, **2 of 89** exceed the most-stated one and the median is under a quarter of
  it — the disagreement between those sources has never bitten this library because it is nowhere
  near where they disagree. Runtime: real redundancy, deliberately kept, because it sits inside a
  job nobody waits for. **A measured "there is nothing here" is a deliverable**, not a failed
  pass: it stops the next person spending a day on the same hunch, and each of these three is the
  kind of thing that *feels* like an obvious win until someone counts. The one place the counting
  did find something was the surface nobody thought to count at all — the always-on context, where
  a pinned "~1%" was 2.26%.
- `[2026-09-08]` **A normaliser that needs the answer to produce it is not a normaliser — and
  that is what redirected the question.** The watcher's first batch wrote a deploy-id normaliser
  for two GitBook pages and deleted it when asset hashes and chunk numbers turned out to churn
  too. The second batch found the harder reason on a Next.js page: the deploy id is **split
  across `<script>` boundaries** by the RSC stream, so the fragment carries no `dpl_` prefix for
  a regex to match. Neutralising every occurrence of the literal id left the page unequal;
  equality needed scrubbing every prefix *and* suffix of the id, ≥8 chars — which requires
  knowing the id, i.e. having already diffed the pages. The lesson is not "normalisation is
  hard". It is that **two failed attempts at the same fix are the signal to change the
  question**: from "can the noise be normalised away" to "is the noise even in the part we
  cite". It is not — visible text is **0.7–4.4%** of those pages' bytes, and all four were
  byte-identical under it. The fix that worked was 30 lines and needed no per-row knowledge at
  all, which is why it classified a fifth noisy page (goose-docs) correctly before anyone knew
  that page was noisy.
- `[2026-09-08]` **I relaxed a check to turn a red run green. That is the accusation, and it is
  worth answering rather than dodging.** `oracle-weakening-audit` exists in this library for
  exactly this move, so the honest form is to state the case against first: four of 92 rows were
  failing every run, I made a comparison looser, and now they pass. What separates it from
  weakening is not intent, it is what was **fixed in place**: the byte comparison and the
  `TAMPERED` check are untouched and never relaxed; the looser question is asked *only* after
  bytes differ, *only* for an HTML stored copy, and *only* when that copy verifies against its
  recorded sha, because a tampered baseline is not evidence about today's page; markdown keeps
  the strict comparison, since `<model-id>` is real content in one of the very pages watched and
  a tag-stripper eats it. And the blind spot is **measured and named rather than discovered
  later**: 16 mutations across the four live pages showed a changed prose word fires, a deleted
  paragraph fires, and a changed **link target does not** — which is a fixture literally called
  `KNOWN BLIND SPOT`, so the day it matters, the decision is revisited where it was made. The
  general rule: a relaxation is defensible when it is scoped by a *mechanism* (the noise lives
  outside the cited text), the strict check survives beside it, and the new blindness is asserted
  in a test instead of assumed away. Absent those three, it is weakening.
- `[2026-09-08]` **Five mutations, two survivors, and the survivors taught more than the hits.**
  Mutating the new predicate caught "apply the text compare to markdown too" and "keep script
  bodies" immediately. Two survived. (1) *Fold case* survived because no fixture distinguished
  case — a real gap, and a nasty one, since the first batch's single true change was a new
  `## Web UI` heading that a case-folding comparison would have called noise. Fixed with a
  fixture. (2) *Unanchor the HTML sniff* survived, and the honest finding is that it **should**:
  `^` and `re.match` each hold the fixture alone, so only removing **both** is catchable. That is
  recorded in the code rather than papered over with a redundant test — a reader hunting for the
  load-bearing line will not find one, because there is not one. **A surviving mutant is either a
  missing fixture or a redundant defence, and the two demand opposite responses**; guessing which
  is how a mutation report becomes theatre.
- `[2026-09-08]` **A threshold derived from the population it judges can be raised by the edit it
  should refuse.** The description-headroom gate computed its target live: the truncation wall
  minus the p75 of the NOT-clauses this library actually writes. Sound-looking, and wrong. During
  the live proof — padding a description to check the gate fires — the target moved from **1,230
  to 1,231**, because the padding added NOT-clauses and shifted p75. Nobody was gaming it; the
  drift is structural, and it points the one direction that matters: *longer descriptions license
  longer descriptions.* The fix is to FREEZE the number as a measured constant with its date and
  derivation, and print today's distribution beside it so drift stays visible without being
  automatic. The general form: **a gate may be CALIBRATED from its population, but it must not be
  COMPUTED from it at judgement time.** This is the same family as a moved goalpost, arriving
  through arithmetic rather than intent — and it was found by a live proof, not by eleven fixtures
  that all passed.
- `[2026-09-08]` **I read a feasibility bound wrong, in the safe direction, and it nearly settled
  the question.** Asking what could be cut from five over-long descriptions without losing a
  trigger token, I counted the *duplicate* content words: 97–187 bytes against a 66–216 need,
  which reads as "three of five are impossible" — a tidy, defensible-sounding no. It ignored
  stopwords, punctuation and connective prose, which are most of the text. The real floor (every
  distinct content word once, single-spaced) is 867–1,011, leaving **429–488 bytes of slack**. The
  lesson is not "check your arithmetic". It is that **a bound computed from the wrong subset tends
  to fail toward "impossible", and "impossible" ends the inquiry** — a false negative here costs
  the whole question, where a false positive would merely have cost an attempt. Prefer the bound
  that over-estimates what is possible, then let the attempt fail honestly.
- `[2026-09-08]` **The right answer to a silent failure was a gate, not the fix.** Five
  descriptions sit above the headroom target and all five are trimmable. They were not trimmed,
  because a description edit changes routing and this library's own rule is that such a change is
  proven against a baseline — which needs a run. What shipped instead fails the build when a
  declared description **grows by a single character**, which is the actual failure mode: the next
  NOT-clause deleted by the act of adding it. **Fixing five instances by hand would have left the
  sixth to happen silently; the gate covers all 92 and costs one named line to except.** That is
  `preflight.py`'s pattern, already proven in this repo, and it is the shape to reach for whenever
  the defect is *silent* rather than merely present.
- `[2026-09-08]` **The watcher checked 92 sources and nobody checked the list of 92.** A routine
  audit of the machinery around the knowledge base — not of the notes, of the tooling — found the
  same URL watched **twice**, at two paths holding byte-identical copies. Every run fetched it
  twice, paused twice, and reported the same source to the reader twice, and had done since the
  re-fetch that stored a second copy instead of recognising unchanged bytes. Trivial in cost and
  not trivial in kind: **the tool that validates the inputs had no validation of its own inputs.**
  Every check now in `watch.py --offline` — four fields, well-formed sha, no duplicate path or
  URL, the named file present and still matching its sha, every raw file accounted for — needed
  no network and could have run on every push since the day the file was created. The general
  form: *when a checker reads a hand-maintained manifest, the manifest is an input and inputs get
  checked.* Ask it of every config, allowlist and index in a repo, including the ones a gate
  reads to decide what to except.
- `[2026-09-08]` **A weekly network job was holding a check that never needed a network.** The
  TAMPER check compares OUR stored bytes to OUR recorded sha. It lived in `watch.py`, which talks
  to the internet, so it inherited that file's weekly schedule and its exclusion from the offline
  CI job — the raw layer's immutability was verified once a week for no reason at all, and not at
  all until this branch merges, since GitHub runs `schedule:` only on the default branch. Moving
  it to every push cost one CI step. **Look for checks that inherited a schedule from the file
  they happen to live in rather than from what they actually need**, and split the offline half
  out; the network is the only thing that has to wait.
- `[2026-09-08]` **A coverage number nobody can recompute is an inspection, not a fact.** "106 of
  198 raw files are unwatched, and that is fine" was true and unfalsifiable: the reasons lived in
  four directory READMEs and in my head. It is now a check — each file must be watched, superseded
  by a newer copy of the same page, pinned at a commit, or named with the reason it cannot be
  watched — so the answer is **198 = 91 watched + 107 accounted + 0 unexplained** and the next
  ingest cannot quietly add a 108th. The one soft spot is stated where it lives: recognising a
  *superseded* baseline is a filename heuristic, and a file wrongly judged superseded is a file
  nobody watches, so its fixture asserts both directions.
- `[2026-09-08]` **A tool that got better makes old rejections wrong, and nothing goes back to
  look.** Four sources were dropped from the watch list on 2026-09-04 for returning different
  bytes seconds apart — correct on the evidence, with the reasoning written down. Hours after the
  watcher learned to separate a byte change from a CONTENT change, all four turned out to be
  byte-different and **visible-text identical**: they were never unstable in the part any note
  cites. Nobody would have revisited them; the drop was documented, reasoned, and closed. **When a
  tool gains a capability, the queue to re-run is not the pending work — it is the work already
  rejected for the reason the new capability addresses.** Rejections should be recorded with the
  *limitation that caused them*, not only the verdict, so that queue can be reconstructed. One of
  the four was worse than stale: it had come back byte-STABLE, dropped on an intermittent property
  its own note had warned could not be proven either way.
- `[2026-09-08]` **The gate caught its own author, in the same minute.** Adding five recovered
  sources, I also added two Hugging Face licence rows that were already watched — the exact defect
  the duplicate-URL check had been written for hours earlier. It failed the run before the commit.
  Worth recording because the usual argument for a gate is about *other people, later*, and the
  usual counter-argument is that the person who just built it will not need it. I did, immediately.
  A check earns its keep on the author's own next mistake, not on a hypothetical successor's.
- `[2026-09-08]` **A coverage number is only as honest as its notion of sameness.** Measuring which
  cited sources go unwatched, naive URL equality said **84 of 138** — alarming, and wrong. The
  watcher deliberately watches *the form that carries the claim*: a note cites `github.com/o/r`
  while the row watches that repo's raw README, because the repo page changes on every star. With
  the forms mapped it was 22, and two of THOSE were still artifacts of forms the map did not know
  (a HF `/blob/` licence, a PyPI project page). Real answer: **10, every one already declared
  volatile-by-design.** Two lessons, and the second is the one that changed a decision: an
  identity check across representations is where a measurement quietly manufactures its own
  finding — and because the map is incomplete by construction, the check ships as a **report that
  can never fail the build**. A gate on it would cry wolf, and this repo has already recorded twice
  that a noisy check is one nobody reads.
- `[2026-09-08]` **Every check looked outward; the one page built from the base itself fell
  between them.** Going through the whole knowledge base found a *compiled* page — a summary
  written back as a note, whose sources are `path:` entries pointing at five other notes rather
  than URLs. It declares `fetched: 2026-09-02`; all five inputs had been rewritten since, two of
  them now declaring later fetches. Nothing could have said so: `watch.py` watches external URLs,
  the lint checks schema and link structure, `contradictions` compares typed values across pairs.
  **A page whose inputs are other pages has no watcher, because its sources never move on the
  network.** The fix is a join key of the same kind the raw layer already uses — `compiled_from:`
  records each input's declared fetch at compile time, and the lint compares it to each input's
  current one. Deliberately declared dates rather than git or mtime: CI checks out shallow so
  `git log` is empty there, and a fresh clone gives every file the same mtime — a content join key
  works in both places. Generalise it as: **whenever a document is derived from other documents in
  the same repo, the derivation needs a recorded input state, or it is stale the moment it is
  written and nothing will ever say so.**
- `[2026-09-08]` **A field that only ever holds one value is not a field.** All 44 notes carry
  `status: verified`. Either the base genuinely has no provisional page — in which case the field
  costs a line per note and tells a reader nothing — or pages are being marked verified on
  arrival, which is worse, because the word then means "written" rather than "checked". Recorded
  rather than acted on: deciding what the other values mean, and re-grading 44 pages against them,
  is a judgement about the base's own standard and not a curator's fix. **The general check is
  cheap and worth running on any schema: for each enumerated field, count its distinct values in
  practice — a cardinality of one is either a redundant field or an unenforced one.**
- `[2026-09-11]` **The token that fires the alarm was the token proving nothing changed.** Both
  unsloth pages reported CHANGED with a one-word diff: `Last updated 10 → 13`. A rendered relative
  timestamp, inside the visible text, which the `noise` verdict is blind to by construction
  because the verdict only removes what is *not* prose. It ticks daily, so those rows would have
  cried wolf forever. The rule added for it is narrow — the number must be followed by a time unit
  **and** the word "ago" — and what makes it legitimate where the deploy-id normaliser was not is
  two things worth generalising: the counter counts **up from a fixed edit date**, so a rising
  number is positive evidence of *no* edit; and `N <unit> ago` is a universal idiom, needing no
  per-row knowledge, which is exactly the test the deploy-id rule failed (it needed the answer in
  order to produce it). **A normaliser is defensible when it removes a token whose CHANGE carries
  no information, and indefensible when it removes a token whose change you merely find
  inconvenient.**
- `[2026-09-11]` **Sorting the queue by diff size cut the triage cost by four.** Batch 1 took about
  an hour for 4 rows and 1 finding; batch 2 about twenty minutes for 8 rows and 4 findings; batch 3
  settled **7 of 34 in about fifteen minutes**, and the difference was not effort but ORDER. The
  script fetches every changed row, strips to visible text, counts the word-level diff, and prints
  the list smallest-first. Seven rows had a **one-word** diff and each was decided by looking at
  that one word — a day counter, a star count, a renamed API symbol, a moved anchor. The big ones
  (2,130 words in `skills.md`) are a re-ingest, not a triage, and pretending otherwise is how a
  backlog becomes silent. **Rank a review queue by the size of the difference, not by the
  importance of the source:** importance decides what you must eventually read, size decides what
  you can finish now, and the cheap end is where most of the queue lives.
- `[2026-09-11]` **The note that wrote down WHY a number was low is the one that did not rot.**
  Z.ai's 50% launch discount expired on the date its own page named. Two notes cited the discounted
  price. `glm-5.3-local` had recorded it as "$0.075 … (50% launch discount; list $0.15/…)" — the
  correction was a deletion. `model-routing-free-and-local` had the bare pair inside a routing cost
  table, and became **2× wrong** the moment the promotion lapsed, with nothing in the sentence to
  warn a reader. Same fact, same source, same day; the difference was one parenthesis. **Record the
  CONDITION attached to a number, not only the number** — a price under a promotion, a benchmark
  under a harness, a limit under a plan tier. The condition is what tells the next reader whether
  the figure can still be true.
- `[2026-09-11]` **Site chrome lives inside the visible text, and that is the one noise class that
  should NOT get a rule.** Three rows in the same batch changed only in furniture: both
  `anthropic.com/engineering` pages moved by the *same three words* (a nav menu gained "Commerce",
  "Research Labs" became "Scientists"), and the-decoder article changed only in its "Top Stories"
  and "Most Popular" sidebars — headlines for *other* articles. The `noise` verdict cannot see any
  of it, because chrome is prose. The relative-timestamp rule was safe to write because `N <unit>
  ago` is a bounded idiom whose change carries no information; **a nav menu is neither bounded nor
  meaningless**, and a regex wide enough to catch one is wide enough to swallow a real heading.
  So this class is recorded and NOT normalised — the opposite decision to the one taken the same
  week, and for a reason that can be stated in advance rather than discovered. **The signal worth
  keeping for later:** two pages from one host changed by identical words. A cross-row agreement
  test — *the same diff appearing on several rows of the same domain is chrome* — would catch this
  class without a single site-specific pattern. Not built: one batch is not evidence, and this
  file already records what happens when a rule is written before the class is measured.
- `[2026-09-11]` **A verbatim MEASURED quote outlived the page it came from, and that is the whole
  argument for the raw layer.** `temporal-kg-agent-memory` carries "100+ operations exposed as MCP
  tools — MEASURED", quoted word for word. The gbrain README was repositioned three days later and
  **that sentence is gone**; the current README states no tool count at all, while neighbouring
  claims survive, so it was a targeted removal. The claim is not refuted and was not re-dated: it
  is still checkable against held bytes. What changed is its future — it can no longer be
  confirmed against the live page, so it must not be cited as current capability. **A vendor
  deleting a number is weak evidence about the number and strong evidence about the positioning.**
- `[2026-09-11]` **The denominator stopped being shown, and nothing became false.** Graft's README
  kept every controlled figure (42% fewer tokens, 46% fewer tool calls, 60% less time, 162 runs)
  and dropped the raw SWE-bench pair this base cites, `33/50 vs 27/50`. The same six instances now
  appear as **"66% (+12 pts)"** in a table and **"+22% more instances resolved"** in a badge. All
  three are arithmetically identical; the framing that travels is the one where six of fifty looks
  biggest. No contradiction, no correction — and the n=50 caveat this base wrote became *more*
  valuable than when it was written. **Record the sample size at the moment you read it**, because
  the version of a result that survives contact with marketing is the one without a denominator.
- `[2026-09-11]` **The same sentence has now gone stale three times, and the fix was never a better
  number.** `subagents` carried "that version number is **29 releases above** the highest this
  knowledge base cites". Corrected on 2026-09-08 to "**4 releases**, the highest cited elsewhere is
  v2.1.257" — and two independent readers of this batch flagged it again within minutes of each
  other, because the re-read adds **v2.1.259, v2.1.260, v2.1.265 and v2.1.267**. The cited ceiling
  is wrong, the derived gap is wrong, and the version the sentence is *about* (v2.1.261) is now
  below the ceiling rather than above it. Each correction reproduced the defect it was correcting,
  which is the tell: **a statement whose truth depends on the state of the whole corpus cannot be
  repaired by updating it — it has to stop being a stored value.** The instruction beside it
  ("compute it, do not read it here") was already right; the number sitting next to the
  instruction was the bug. Delete the figure, keep the instruction. The general rule for this base:
  *if a sentence would be falsified by an unrelated edit elsewhere, it is a query, not a claim.*
- `[2026-09-11]` **A number correct against the wrong reference.** `token-economy-playbook` divides
  its always-on share by a 1M window. The re-read adds, verbatim, that models with a native 1M
  window *"compact before the window fills, at about **967K tokens** by default"* — so the window a
  session actually fills is ~3.3% smaller and the honest share is **2.34%, not 2.26%**. Tiny, and
  recorded for the shape: it is the third instance in this file of the same class — a pinned
  running statistic, a promotional price quoted as a standing one, and now a correct numerator over
  a nominal denominator. **The fix is not a second pinned constant.** The compaction threshold
  varies by provider, so what is recorded is the limit on the figure, not a new figure.
- `[2026-09-11]` **Two readers, given different documents, found the same defect — and that is an
  argument about fan-out, not luck.** The `skills.md` reader and the `model-config.md` reader were
  briefed on disjoint pages and disjoint note sets. Both independently flagged the stale
  highest-version sentence, each from versions in its own diff. A single reader would have reported
  it once and the severity would have looked like one page's problem; two reports from two sources
  showed it is a property of the *base*, not of either page. **When a finding arrives from two
  independently-scoped readers, it is evidence about the system rather than the source** — worth
  weighting above anything either reader says alone, and worth briefing for deliberately: give
  overlapping *questions* to non-overlapping scopes.
- `[2026-09-11]` **One gate caught its own author four times in a day, and never once was the gate
  wrong.** The raw-layer accounting check fired on three re-baselines where the new filename broke
  the superseded-baseline join, and then on a documentation file named `README-docs.md` when the
  exclusion list names exactly `README.md`. Every fix was to the naming, never to the check —
  widening the exclusion to `README*` would have made every future stray `.md` in the raw layer
  invisible, which is the hole the check exists to close. Two things worth separating here. **The
  repetition is not evidence the check is too strict; it is evidence the convention is
  undiscoverable at the moment of choosing a name** — two naming forms are live side by side and
  nothing tells an author which applies. And the fourth catch is the one that matters most: it
  **reached CI**, the only failure in this branch a local run did not catch first, purely because
  the check was run before the file was written rather than after. *Run the gate last, after
  everything including the write-up* — a check that passed earlier in the turn is not a check that
  passed.
- `[2026-09-11]` **A floor claim was the only phrasing in the table that could not rot.** The
  eight-row queue produced one material change and seven negatives, and the seven are where the
  method showed. `agency-agents` gained new rows; this base cites **"230+ agent prompt files in
  16+ divisions"**, so additions *cannot* falsify it — the `+` does the work. Beside it,
  `OmniRoute` moved two counters (an i18n language count, a migration count) that this base has
  now declined to cite for the **second** time, and `claude-mem`'s five named hooks all survived a
  version bump because they were listed by name rather than counted. **Prefer a floor to a point,
  and a named list to a count**: the phrasings that survive a source's own churn are the ones that
  say what they are about rather than how many there are.
- `[2026-09-11]` **A release version is a surface with a multiplier, which is why the watcher sees
  it.** `claude-code-router` went v3.0.22 → v3.1.0, and the diff was four lines — every desktop
  installer link in the README carries the version, so one bump moves four URLs at once. That is
  the difference between a version buried in prose (invisible to a byte watcher until someone
  reads it) and one embedded in download links (loud). Worth knowing when deciding whether a
  source is worth watching at all: **ask where the version is rendered, not just whether it
  exists.**
- `[2026-09-11]` **The decisive argument for dropping a watched source was its VALUE, not its
  noise.** The-decoder's article changed three times in one day and every one was hand-verified as
  chrome — a rotating "Top Stories" sidebar carrying *other* articles' headlines, with the body
  stable each time. The tempting fix is a regex for sidebars, and this file has already recorded
  why that is wrong: chrome is prose, unbounded, and a pattern wide enough to catch a carousel is
  wide enough to swallow a real heading. The tempting second fix is to leave it crying wolf, which
  is the failure the `noise` verdict exists to prevent. **What actually settled it was asking what
  the row buys:** every claim this base took from that article had already been corrected against
  the primary paper — the benchmark is v1.5 not v1.6, "state of the art" is a 0.02-point lead — so
  it is a *superseded secondary*, and change detection on one is worth nothing. **Watch a source
  for what its future changes could still tell you, not for the fact that you once cited it.**
  The drop carries a re-entry condition, recorded so it is recoverable the way the 2026-09-04
  drops turned out to be: a chrome test needing no per-site pattern — the same diff appearing
  across several pages of one host — makes the row watchable again.
- `[2026-09-11]` **Dropping a row orphaned the copy behind it, and the accounting caught it in the
  same breath.** Removing the watch row left the *older* stored copy with nothing to be superseded
  by, so it became an unaccounted raw file instantly. Two things worth keeping. The superseded-
  baseline heuristic is **transitive through the live row** — cut the row and every historical copy
  behind it loses its justification at once, which is not obvious when you write the rule. And the
  check found it the moment it happened, which is the fifth time in two days this one gate has
  caught its own author: **a deletion has downstream accounting, and the only reason that is cheap
  to discover is that something recomputes the whole invariant rather than the part you touched.**
- `[2026-09-11]` **The highest-value open item was unexecutable, and the check cost four commands.**
  Unlimited-OCR-vs-our-`pdf`-path had been carried for three days as "the single highest-value item
  in the base, and it is a measurement, not a re-read" — in the note, in BRAIN, and in two successive
  batch entries that each said the batch was not a substitute for it. It was never attempted, so
  nobody had asked whether it *could* be. It cannot: 0 PDFs in the repo, 7 of 8 scripts in the public
  `pdf` skill failing at import, no `torch`, no GPU. *(Both PDF figures were superseded within a day
  and the correction is recorded at `knowledge/notes/long-document-ocr.md`, which owns the
  measurement: nine PDFs are now held, and 4 of those 7 import failures were the poisoned system
  `cryptography` rather than an absent package — isolation alone takes the skill to 5 of 8.)* **The block was in the BASELINE arm, not the
  novel one** — attention had been on whether the 3B model would run, and the thing that was already
  ours turned out to be the missing half. Two rules. An item that names a run should carry, from the
  day it is written, **one line saying which arms exist**; without it "needs a run" and "needs an
  environment nobody has costed" look identical in a queue and are not the same work. And **priority
  is not feasibility**: calling something the highest-value item three times raised its rank without
  ever testing its floor, and a ranking loop with no feasibility check will keep the most attractive
  impossible item at the top indefinitely.
- `[2026-09-11]` **An import that fails is not a package that is missing.** The first probe ran
  `import pypdf`, saw it fail, and wrote `pypdf ABSENT` into a findings list. pypdf is installed —
  it is on disk at `dist-packages/pypdf` and five of the pdf skill's eight scripts import it — and it
  is *broken*: it reaches `cryptography.hazmat.bindings._rust`, which needs `_cffi_backend`, which is
  absent, and the failure arrives as a Rust `PanicException` rather than an `ImportError`, so pypdf's
  own fallback chain never catches it. The wrong diagnosis pointed at the wrong fix (install pypdf,
  which is already there) and hid the real one (install `cffi`). **Probe for presence and for
  usability separately** — `importlib.util.find_spec` answers the first, and only executing the import
  answers the second; a single try/except conflates them. It also conflates them *silently in the safe
  direction*, which is why this is the second time in a week a bound has been read pessimistically and
  had to be corrected before it reached a decision.
- `[2026-09-11]` **A capability map lists what exists; nothing in it says what runs.** `CLAUDE.md`
  routes "Understand a long doc/paper/repo → `deep-reading` (PDF via the `pdf` skill first)", and in
  this environment that first hop does not execute at all. The map is not wrong — the method is real
  and portable, which is exactly what the generality rule demands of it — but a reader following the
  route gets a dead end, and no audit of the map's *contents* could ever have found it. The check that
  finds this class is an execution probe of the routed entry point, not a review of the routing line.
- `[2026-09-11]` **Having found one dead route, I checked how wide the class was, and the answer was
  reassuring in one direction and worse in the other.** Probing every executable thing our own talents
  ship — six shell scripts across `.claude/skills` and `.claude/agents` — all six parse, all six have
  their interpreter, and every external command they invoke (jq, node, git, awk, sed, diff, sort,
  grep) is present. **Our own surface is executable here; the dead route is one we point at and do not
  own.** That is the generality rule paying off rather than luck: a talent written as a portable
  method has nothing to be missing. Worth keeping as a NEGATIVE result, because the instinct after one
  finding is to assume a field of them, and the measurement says otherwise.
- `[2026-09-11]` **I stopped at the first candidate and named one skill where the evidence covered
  two.** The finding went out as "the `pdf` skill does not execute here". There is also a separate
  `pdf-reading` skill on the same path — the one a reading task actually wants — and it fails the same
  way, on all five poppler tools plus the same broken pypdf. The conclusion got *stronger*, which is
  the dangerous case: a stronger-on-recheck claim gives no signal that the first pass was incomplete,
  so nothing would have prompted the recheck. **When a finding is about what a directory contains,
  list the directory** — `ls` was the missing step, and it cost nothing. The correction is an addendum,
  not a rewrite: the commit is pushed and the blemish costs less than a force-push.
- `[2026-09-11]` **The preregistered rule failed and the capability was real — because the rule's test
  case was chosen for importance, not for typicality.** "Can a stdlib-only extractor read our held
  PDFs?" was tested against the Anthropic skills guide, the base's most-cited PDF. It reads at 17.6%:
  CID-encoded, needing ToUnicode CMaps. FAIL, honoured, no iteration. But the same extractor reads
  BOTH academic PDFs at **100.0%**, so the true answer is not "stdlib cannot read PDFs here" but
  "stdlib reads two of our three, and a typographer's font choice decides which". **Picking the
  highest-value instance as the test case answers "can this be done on the hardest case", and quietly
  substitutes that for "can this be done at all".** The two questions have different answers here and
  the preregistration could not tell them apart, because it named one document. A rule of this shape
  should name a SET and state what fraction must pass.
- `[2026-09-11]` **The refusal is the feature, and it was nearly not built.** The obvious tool returns
  the text it extracted. Run on the guide, that output is grammatical English prose — the sentence
  `"...automated test suites or produce quantitative evaluation results."` reads as complete and is a
  fragment with its subject missing. Nothing in the text marks the 82% that is absent. So the shipped
  tool reports the decodable fraction and WITHHOLDS the text below a floor: it can say "I cannot read
  this" but never hand back a convincing piece of a document. The mutation that lowers that floor below
  the measured 17.6% is caught by a fixture, deliberately, because a one-character edit would otherwise
  turn a refusal into an answer with no test objecting. **A partial reader without a coverage number is
  not a weaker tool than a complete one; it is a different and more dangerous kind of tool.**
- `[2026-09-11]` **The raw-layer gate demanded a machine-readable reason, and a prose README was not
  it.** Holding the three PDFs, I wrote a README explaining each one — the convention every other raw
  directory follows — and `watch.py --offline` still failed all three: *watch it, or declare it in
  NEVER_WATCHED with the reason it cannot be watched.* The README satisfies a reader; the gate wanted a
  declaration in code. That is the right design and it is the **sixth** time in three days this one
  check has caught its own author. Worth naming the pattern: the checks that keep working are the ones
  that recompute a whole invariant and accept only a structured answer, because prose satisfies the
  author writing it and nothing else.
- `[2026-09-11]` **The guard passed a document at 100% that had one space in 74,422 letters.** Having
  built a coverage guard specifically so a partial reader could not pass off a fragment as a document,
  I shipped it, gated it in CI, and then used it — and the first file it called READABLE came out as an
  unbroken run of letters. PDF word gaps are *kerning numbers* inside a TJ array, not space characters,
  and the reader discarded them. **Coverage was structurally incapable of seeing this**: every byte it
  counted really had been decoded. The metric was honest and measured the wrong quantity. A second
  defect of the same shape is still there and is now declared rather than fixed — `fi`/`fl`/`ff`
  ligatures drop silently (41 "bene", zero "benefit" in one paper), so the verdict no longer promises
  an exact quote. **A guard is only as honest as the quantity it measures, and "how much decoded" is
  not "is this usable".** What found both was using the output for its real purpose within minutes of
  shipping; the test suite was green throughout, and would have stayed green.
- `[2026-09-11]` **The predicates were tested and the wiring between them was not.** A mutation that
  unhooked the fidelity check from the verdict inside `main()` survived a 37-fixture suite untouched,
  because every fixture called the pure functions directly and nothing called the path that joins
  them. The fix was to lift the decision out of `main()` into a `report()` function and add three
  fixtures over real PDF bytes end to end. Worth generalising: **mutation-testing the predicates
  proves the predicates, and an untested `main()` is where a well-tested tool quietly stops using its
  own checks.** Lift the decision path out of the entry point so a fixture can reach it.
- `[2026-09-11]` **The suite was 40 green while the tool's primary output path raised NameError on
  every real file.** After lifting the decision out of `main()` into a testable `report()`, the line
  that actually PRINTS the text still referred to the old variable — an earlier patch had silently
  no-op'd on an indentation mismatch — so `pdftext.py FILE.pdf` produced nothing at all. I did not
  notice for two commits, because I was running it with stderr to `/dev/null` and never checking the
  exit code. **Three compounding causes, and the last is mine:** a string-replace that reports success
  when it matches nothing; a test suite that covered every pure function and not the entry point that
  joins them; and a caller discarding the channel the error was on. The fix tests `main()` itself
  through a temp file, capturing stdout and stderr and asserting the exit code. **If you redirect
  stderr while developing, you have disabled the only thing that would have told you.**
- `[2026-09-11]` **A near-miss match is not evidence of absence.** Verifying this base's claims against
  a newly-readable primary, I searched for a quoted phrase — *the benefit "is multi-dimensional and not
  consistent"* — found a similar-sounding sentence elsewhere in the paper (*"measuring the impact of
  refactoring requires multi-dimensional assessment"*), and was one step from recording a fabricated
  quotation. The two sentences make different claims, which is exactly what made the near-miss
  convincing. Searching the whole document for the exact string found the real one, twice, verbatim.
  **The failure mode is specific and repeatable: a partial search returns the nearest thing, and the
  nearest thing reads as a refutation.** Search for the claimed string across the whole document before
  concluding it is not there, and say which you did.
- `[2026-09-11]` **Five claims checked against two newly-held primaries; five confirmed.** Worth
  recording precisely because nothing was wrong: the page's Boehm & Basili and Kim et al. rows survive
  contact with the documents, including the exact hedges ("often", 5:1, "even for large critical
  systems") that are the whole reason those rows exist. The base's habit of quoting the hedge rather
  than the headline is what made them checkable at all.
- `[2026-09-11]` **A measured number became a constant in nine files within three hours, while the
  thing measuring it was still being repaired.** The PDF reader's coverage figure for the Anthropic
  guide, 18.0%, was quoted into this file, BRAIN, the decision record, four notes, `watch.py`'s
  NEVER_WATCHED reasoning and a CI comment. Then a genuine fix — stop scanning embedded fonts and
  images as if they were page text — moved it to 17.6%, and all nine went stale at once. The verdict
  never changed, which is exactly why it was tempting to leave them. **A number produced by a tool
  still under active repair is not yet a fact to cite.** Quote it in the one document that owns the
  measurement and point at that document from everywhere else; this repo even has a talent for the
  cleanup (`doc-claim-reconciliation`), which is a sign the shape recurs rather than an excuse to keep
  causing it.
- `[2026-09-11]` **An exclusion list can only name the stream types someone thought of.** The reader
  was scanning every Flate stream in a PDF as if it were page text — including raster images (90+
  seconds of regex backtracking on 302 KB of pixels, and any byte run resembling a text operator would
  have been counted as REAL TEXT and inflated the coverage metric with pixel data). Excluding images
  by their dictionary fixed one file; the next still hung, on an embedded OpenType font that is not an
  image and carried no marker the code knew. **The list was the wrong shape of answer.** What works is
  a property of the bytes themselves — page content is operators and numbers, overwhelmingly printable
  ASCII, and a binary blob is not — which rejects every wrong type including the ones not invented yet.
  Prefer a positive test of what the thing IS over an enumeration of what it might be instead.
- `[2026-09-11]` **Four observations now, and the cadence is no longer a guess: `code.claude.com`
  pages move several times per day.** `skills.md`, `plugins.md` and `plugin-marketplaces.md` changed
  within two hours of being re-baselined; then `hooks-guide.md` and `sub-agents.md` changed again the
  same evening; then `plugin-evals.md` an hour after that. The READMEs beside them in `WATCH.tsv` move
  weekly. Weekly `kb-watch.yml` is therefore the wrong cadence **for this host specifically** — but
  the change to make is a per-row or per-host interval, not a faster global schedule, because
  quickening every row to suit one host multiplies fetches for ninety that do not need it. Still not
  changing the schedule on a branch whose whole argument is that unmeasured conventions fail; the
  number to record next is how many of these re-reads carry a *substantive* diff. So far three of
  three did, which is the surprising part — a page that moves hourly could easily have been all
  chrome, and it is not.
- `[2026-09-11]` **A quoted figure absent from the documents you searched is not a refuted figure.**
  Verifying `llm-idea-generation` against its held primaries, two numbers (`3.73/4` vs `1.00/4`, and
  `6.14` vs `2.38`) appeared in neither readable paper. The tempting conclusion, especially an hour
  after finding a near-miss that nearly cost a real quotation, is that they are wrong. They are not
  checkable either way here: they belong to an HTML render never held and to an arXiv PDF that
  **refuses at 0.0%**, every glyph hex-coded. The page now says so at the point of the claim, which
  costs two sentences and saves the next reader the same search. **Record the boundary of what a
  verification pass could see, not only what it found** — otherwise a later pass reads silence as
  agreement.
- `[2026-09-12]` **The fifth pass was 0 changed, and that is evidence AGAINST the claim the previous
  four were building.** Three `code.claude.com` pages moved within hours of being re-baselined, twice
  in one evening, and the shape forming was "this host changes several times a day". An hour later:
  `86 unchanged · 0 changed · 10 noise · 0 tampered`. So the evidence supports a **burst** — three
  changes clustered in one evening — and not a steady hourly rate, and a per-host interval proposed
  from the burst would over-fetch every quiet hour. **A run of consecutive positives is the easiest
  thing in the world to read as a rate**, and the correction costs one quiet observation that nobody
  would have bothered to write down, because nothing happened. Record the passes where nothing moved:
  they are the denominator, and without them every watched source looks volatile. The proposal stays
  unmade and now needs a spread of quiet and busy passes, not more of the busy ones.
- `[2026-09-12]` **The substantive rate broke its own streak, and the streak was the interesting
  claim.** `code.claude.com` changes had been 3 of 3 SUBSTANTIVE — the striking part of the cadence
  measurement, because a page moving hourly could easily have been all chrome. The fourth change is
  30 words of `/model` picker UX (a key made rebindable) and **owes no note a re-read**. So the rate
  is 3 of 4, and the honest reading is now two separate quantities: *how often* a host moves, and
  *how often a move matters*, which is the one that decides whether watching it more closely is
  worth anything. The first streak made them look like the same number. Worth noting that this took
  only one counter-example to correct, and that the counter-example arrived as an ordinary quiet
  triage nobody would have written up — the same shape as the quiet passes being the denominator.
- `[2026-09-12]` **I spent five hours arguing that fetch frequency should match change frequency, while
  polling my own PR hourly against a state that had not changed once.** The cadence measurement's whole
  point is that watching a source more often than it moves buys nothing and costs every quiet fetch.
  Five consecutive empty watcher passes, a PR green and mergeable with no reviews, and nothing I could
  do to advance it — and the check-in kept firing every hour anyway, because that is the interval it was
  first given. **The rule I derived for external sources applies to my own loop, and I did not notice
  it there.** A monitoring loop is a watched source: its interval should follow how fast the thing it
  watches changes, and a PR waiting on a human reviewer changes on human time, not on the hour.
  Stretched to three hours — not cancelled, because the standing rule is that the check-in survives
  until the PR is merged or closed, and a slower heartbeat honours that where stopping would not.
  Worth recording because of how the blind spot was shaped: the reasoning was already written down,
  applied carefully to ninety-six URLs, and simply never turned on the thing doing the reasoning.
- `[2026-09-12]` **A vendor published, about its own installer, the argument this base had already made
  about a different one.** Prime Intellect's README changed 34 words: SHA-256 verification is now
  stated as **integrity, not authenticity**, *"because the inventory and archive come from the same
  origin"*, with HTTPS named as the authenticity boundary and `--proto '=https' --proto-redir '=https'`
  added to refuse a plaintext redirect. `graphify-assessment` had written *"integrity against a broken
  download, not authenticity — checksum and binary come from the same channel"* weeks earlier, reached
  from graphify's code with no vendor saying so. **An independent party publishing your own reasoning
  back to you is the strongest confirmation available that an analysis generalises** rather than being
  a quibble about one project's wording — and it is worth recording as such at both ends, because the
  two notes now support each other where each alone was one reading of one installer. The transferable
  rule for the fourth gate: **do not ask whether an installer verifies a checksum, ask where the
  checksum came from.** Two of the two `curl | sh` installers examined here got the wording wrong;
  one has since corrected itself.
- `[2026-09-12]` **Eighth catch, and the naming convention was the thing I got wrong again.** Storing
  the new baseline as `..._README@2026-09-12.md` orphaned both older copies instantly: the
  superseded-baseline heuristic matches on the filename stem with `@<date>` stripped, and every other
  GitHub README in this layer is stored under its plain URL-derived name — `..._README.md.md` — with
  the *directory* carrying the date. Two conventions coexist for good reasons (docs pages are dated in
  the filename because several versions live in one directory), and I applied the wrong one. The fix
  was a rename. **A convention that varies by file class is a convention you will get wrong from
  memory; the gate that recomputes the whole invariant is what makes that cheap** — this is the eighth
  time in four days it has caught its own author, and the eighth time the fix was to the data.
- `[2026-09-12]` **The PDF block is a REGRESSION, and the base's own provenance is what proved it.**
  For a day I recorded the missing PDF toolchain as a limitation of this environment — something never
  present, whose absence made three notes unverifiable. Then a source entry gave it away:
  `anthropic-skill-authoring-contract` says its guide was *"text-extracted with pdfminer.six"* and
  re-counted *"on a fresh download with pypdf"*, on 2026-09-04. Measured 2026-09-12: `pdfminer` is not
  installed and `pypdf` panics on import. **The capability existed, was used, and disappeared, and
  nothing noticed for eight days.** Two things follow. The question standing for the human changes
  shape — restoring a dependency the base already relies on is a smaller decision than adding one, and
  it has a precedent rather than needing a justification. And the general point: **a knowledge base
  that records HOW each claim was verified can detect the loss of its own verification tooling** —
  the provenance field did a job nobody designed it for, which is an argument for recording the method
  and not only the source.
- `[2026-09-12]` **Four of the eleven open proposals were resolvable with evidence already in the
  base, and had been sitting for four days.** Two were contradictions *inside* a single note — the
  `graphify-features` Export block listed exports as flags while the same page, 130 lines below,
  explained the two command surfaces correctly and named the flag form as its own lesson. One was a
  label (AUTHORITATIVE retracted to FIRST-PARTY, with the grading deferred to the page that actually
  graded it). One was an over-claim reconciled against its better-qualified companion. **None needed a
  fetch, a run, or a human** — they needed someone to read two pages at once, which is exactly what a
  review pass produces and then nobody does. Worth noting that the proposals were correct and specific
  when written; the gap was purely between "written down" and "applied".
- `[2026-09-12]` **The answer to a question marked "unresolvable" had been in the raw layer for eight
  days, and the provenance field is what hid it.** Two notes recorded a contradiction — `skill-anatomy`
  says the frontmatter fields are "all optional", `skill-authoring-eval-methodology` says name and
  description are mandatory — as *not resolvable*, on the grounds that `agentskills.io/specification`
  was "not held as raw and its fetch date is `null`". The `null` was true **of the note's citation**.
  The raw layer had the page, watched, baselined 2026-09-04, and it carries the answer verbatim:
  *"The **required** `name` field"*, *"The **required** `description` field"*, against *"The
  **optional**"* for four other fields. **A missing fetch DATE is not a missing FILE**, and I re-fetched
  429 KB to learn something already on disk. The gate caught the duplicate row — ninth time — and the
  fresh copy turned out to be byte-different and prose-identical to the held one, so the `noise`
  classifier had been right about it all along. Before fetching a source a note calls unheld, grep the
  raw layer for its URL.
- `[2026-09-12]` **A constant marked `decided` was actually `sourced`, and the difference was thirteen
  violations nobody had counted.** `DESCRIPTION_CAP_CHARS = 1024` read as a house-style choice — "we
  author to the spec limit because it travels". The spec states it as a hard bound: *"Must be 1-1024
  characters"*. Once it is a limit rather than a preference, the obvious question follows, and the
  answer is **13 units over it**, 1,037 to 1,446 characters. The existing gate sees **5** of them,
  because its frozen target of 1,230 answers a *different* constraint — the host's silent 1,536
  truncation wall. Both numbers are correct and they are not the same measurement. **Two limits on one
  field will hide each other unless something names both**, so the gate now reports the spec count
  beside its own verdict and gates on neither anything new: moving a preregistered threshold after
  seeing a result is precisely what preregistration exists to prevent, and a reporting line is not a
  threshold. Four mutations against the new path, four caught — a reporting-only code path is exactly
  where a silent break goes unnoticed.
- `[2026-09-12]` **The gateway-discovery contradiction dissolved into two code paths, and both were
  already documented here.** A vendor screenshot showed `open_router/google/gemma-3-4b-it:free` in
  Claude Code's `/model` picker — an id that cannot pass discovery's filter, which keeps only ids
  containing `claude` or `anthropic`. `model-routing-free-and-local` already recorded, from the same
  docs, that a **pinned** third-party model's row shows *"the raw id"* when unrecognised. Pinning does
  not go through discovery. So the filter governs what is *discovered* and says nothing about what is
  *pinned*, and the screenshot is evidence about pinning. **Two notes each held half of a resolution and
  the halves read as a conflict for four days** — the same shape as the four proposals applied earlier
  today, and the reason a cross-note reading pass finds things no single-page review can.
- `[2026-09-12]` **I recommended a design from a plausible mechanism, and one measurement refuted it an
  hour later.** Asked whether multi-level graphify graphs are worth building, I answered from the held
  READMEs: communities are flat, so derive the hierarchy by nesting a fine partition inside a coarse
  one — *"both from the same extraction, every edge intact"*. Measured: **76.6% single-parent against a
  90% threshold fixed before the run.** 18 of 77 fine communities straddle up to 4 coarse ones. The
  reason is obvious once looked at and I never looked: **each Leiden call is an independent optimisation
  over the whole graph, so a finer partition is not a refinement of a coarser one.** Nothing constrains
  them to nest. I had correctly defended the half that was not in question — edges do survive — and
  asserted the half that mattered without checking it. **A mechanism that would explain a result is not
  evidence that the result holds**, and "both come from the same graph" felt like a reason while being
  only a reassurance. The right mechanism turned out to be one function call away, in a dependency
  graphify already installs: `hierarchical_leiden`, 100% single-parent by construction.
- `[2026-09-12]` **The CLI's `--help` under-documents flags the README documents, and either source
  alone produces a wrong answer.** `--resolution` and `--exclude-hubs` do not appear in
  `graphify cluster-only --help` in 0.9.58; they are parsed at `cli.py:2034` and `cli.py:3311`. A reader
  who trusted `--help` would have called the README stale; a reader who trusted the README would never
  have learned that `cluster.py` documents a **Louvain fallback** on Python ≥3.13, which I had recorded
  as "undocumented" hours earlier. **Three surfaces — README, `--help`, source — and the source is the
  only one that was right about all three questions.** `source-grounded-implementation` says to read the
  resolved version's source and cite file+symbol per claim; this is why.
- `[2026-09-12]` **"29% outside the giant component" was a number I wrote as a caveat and had not
  understood.** Left as a percentage it reads as fringe. One line of measurement turned it into
  architecture: **48 components, only 8 lone nodes, and a second component of 1,089 nodes** — the
  Python engine in one island and the TypeScript stack (`apps/api`, `apps/app`, `packages/shared`) in
  the other, disconnected because they talk over HTTP rather than importing each other. **A caveat
  stated as a percentage hides whether it is dust or a subsystem**, and those demand opposite designs:
  the first you note and move on, the second makes a tree built on the giant component alone omit a
  quarter of the graph including the half a web developer would look for. The fix was also the reward —
  **connected component gives you level 0 for free**, with no algorithm and no parameter, and it means
  something (language/workspace boundary) where a Leiden level does not. Two days of reasoning about
  resolutions, and the most useful level in the hierarchy needed no clustering at all. **When a caveat
  is a proportion, resolve it into a count and a shape before writing it down.**
- `[2026-09-12]` **The "unchecked" sentence I wrote an hour earlier was true and worth checking, and it
  took two minutes.** I closed a finding with *"whether Scio's held graph is also a forest is unchecked
  here"* — an honest limit, and exactly the kind that stays unchecked forever. It is a **77-component
  forest**: giant 3,201 of 5,173 (**61.9%**), **1,972 outside**, only 25 lone nodes, the same
  Python/TypeScript split plus a third island of 279 documentation nodes. So the fraction outside is
  **larger** there than in my own run (38% against 29%), and the repo's steering file tells readers to
  *"Query it for symbols and dependencies instead of reading source"* — advice that, followed literally
  on one connected structure, misses the whole frontend and every doc node. **Writing "unchecked" is
  the right move; leaving it written is not.** A flagged gap should carry either a check or a reason the
  check is not cheap, and here it was one traversal of a file already on disk.
- `[2026-09-12]` **Two documents that looked contradictory turned out to describe a real gap in a
  shipped tool, and this library had already filled it without recording that it had.** The standing
  contradiction read *"the contract says evals BEFORE writing; the eval note's step list is the
  opposite order"*. Side by side they are not opposite orderings of the same steps: the contract's own
  steps run **without-skill baseline → establish baseline → write MINIMAL instructions**, and what it
  defers is *extensive* documentation, not all writing. `skill-creator`'s shipped loop opens at *"write
  a draft"* and has **no without-skill step at all**. So the contract's claim that the eval note
  "confirmed" its ordering **could not have been true** — a loop cannot confirm an ordering whose first
  step it omits — and that claim is retracted. The useful part: our `skill-measure` says *"the baseline
  probe runs"* first and `eval-harness` owns baseline-vs-with, so **the baseline arm is our addition
  over the vendor's loop**, and nobody had written down that it was an addition. **When two sources
  disagree on an ordering, check whether one of them is missing a step rather than reordering the same
  ones.**
- `[2026-09-12]` **Scio's ADR-0001 had independently found the same thing about graphify's `--help`,
  three weeks earlier.** It records that *"`graphify hook` exists and works, though it is absent from
  the tool's own top-level help"*; today `--resolution` and `--exclude-hubs` turned out to be parsed at
  `cli.py:2034`/`cli.py:3311` and present in the README while missing from `--help`. Two independent
  observations of the same pattern make it a **property of the tool rather than a one-off omission**:
  graphify's help is a floor, not an inventory, and the README or the source is the surface to trust.
  Worth recording because the second observation cost an hour of treating `--help` as authoritative —
  the first one was already written down, in another repo, by this same project.
- `[2026-09-12]` **A re-baseline would have destroyed a release's measurements that were never read
  in.** The Soup README changed, and the diff replaced its **v0.74.0** block with **v0.75.0** — so
  v0.74's figures (fp32 upcast of the frozen base, 48,241 → 18,658 MiB peak, 2.59×, four SSRF bypasses
  by alternate IPv4 spellings) had been sitting in the 2026-09-11 baseline for a day, unread, and the
  only copy was about to be superseded. They are recorded now, both releases. **This is the concrete
  argument for the standing rule that a row is read before it is re-baselined** — usually defended as
  "an honest backlog beats a silent one", which is abstract. Here the cost was specific: a release's
  worth of measured numbers, one command from being gone.
- `[2026-09-12]` **One release fixed three separate instances of the shape this base keeps collecting,
  and a third project names it in the same words.** Soup v0.75.0: an unknown config key was *"dropped
  while the run proceeded with the setting not applied"*; six training options were *"each validated and
  then dropped on `backend: mlx`"*, so one config trained a different recipe per backend; and validation
  loss *"was computed on every backend and thrown away"*. Scio's ADR-0001 calls its own version **"an
  honest signal computed and then dropped"**, documented in its predecessor *five times over*. Three
  independent projects, one failure shape — **accepted, then silently not used** — which is enough
  recurrence to treat it as a design law rather than a recurring accident. Two details worth copying:
  the deprecation was **telegraphed one release ahead by name** (*"v0.74 warned and named this release
  as the deadline"*), and 24 of 32 unsupported optimizer names are **refused by name instead of
  falling back to a default** — the same choice `knowledge/pdftext.py` makes about a PDF it cannot read.
- `[2026-09-12]` **A day of "the toolchain is missing" was one poisoned dependency in one
  site-packages.** The PDF blocker held three notes hostage and reframed a decision twice — first *add
  a toolchain*, then *restore one we lost*. Both were wrong. The system `pypdf` is **6.17.0**: present
  and current. It panics because the **system `cryptography`** reaches a Rust binding needing an absent
  `_cffi_backend`. In a clean virtualenv, `pypdf` 6.18.1 reads the guide — **33 pages, 35,765
  characters**, preregistered string present verbatim. **The environment was never missing the
  capability; one import path into it was broken, and every conclusion inherited that one fault.**
  Three lessons, and the third is the one that cost the day: probe for *presence* and *usability*
  separately (already learned, and it was not enough); a version number is the first thing to check
  before calling something absent-or-old (6.17.0 was neither); and **when a dependency fails, test it in
  isolation before concluding anything about the environment** — a venv costs seconds and would have
  retired this on the first day rather than the second.
- `[2026-09-12]` **The last blocked item resolved into "stale, not false", and only a file's own
  metadata could tell those apart.** `skill-anatomy` quoted the guide saying `skill-creator` *"does not
  execute automated test suites or produce quantitative evaluation results"*, then described the tool
  emitting `pass_rate` and a delta ~130 lines later. Read from the now-readable PDF: the guide's
  `/CreationDate` is **2026-01-26**, `pass_rate` appears **0 times** in it, and the tool's metrics were
  read **2026-08-30**. Seven months, and the guide makes no claim at all about the metrics observed. So
  it is a **dated vendor claim the vendor's own product overtook** — true when written. **Without the
  creation date there is no way to distinguish a source that is wrong from one that is old**, which is
  an argument for capturing document metadata at ingest and not only the fetch date: the fetch date
  tells you when *you* read it, and only the document's own date tells you what it could have known.
- `[2026-09-12]` **Second time today a `str.replace` matched nothing and reported success, and this
  time it left a wrong number standing in a status summary.** The review doc's heading said *"Eight
  resolved, three open"*; the table below it said nine resolved and two open; and I told the user
  "nine", then "ten", on two successive turns. **Three numbers, none of them the table's.** Cause: I
  wrote the replacement target from memory instead of from the file, so two corrections no-op'd — the
  same fault that had `pdftext.py`'s `main()` printing nothing for two commits, there on an indentation
  mismatch. The fix is not "be careful": the count is now **derived from the table** by counting
  verdict rows, so a hand-written summary cannot disagree with the data under it. **A number that
  restates data sitting three lines below it should be computed, not typed** — and a string-replace
  that changes nothing must be asserted, which is why every edit script in this session asserts its
  target and why these two were the ones that slipped through a `.replace` without one.
- `[2026-09-12]` **I predicted two defects from the forest finding and the measurement refuted both — the
  third time today a plausible mechanism failed a test.** Reconciling the finding against our *own*
  talents, I expected `graphify-harvest`'s `god-nodes --top 15` to contain **no** entries from the
  smaller island, and `repo-map`'s PageRank to starve a small component out of a budget-packed map.
  Measured on the 4,499-node graph whose second island holds 24% of the nodes:
  **god-nodes gave it 2 of 15 (13%)** — under-weighted but present, so the skew is mild rather than
  blinding; and **PageRank gave it 11 of the global top-40 (27.5%)** — *above* its share. The reason
  PageRank is fine is the part I had not thought about: **its teleport term distributes mass to every
  node regardless of connectivity**, so a disconnected component is never starved. So one skill gets a
  small measured caveat about reading the component spread, and the other gets **no change and a
  recorded negative result**.
  The pattern across all three of today's refutations is the same: I reasoned from a mechanism that
  *would* produce the effect, without checking whether the mechanism is actually present. Nesting Leiden
  resolutions "should" nest; a global degree rank "should" drown a small island; PageRank "should"
  starve one. **Twice the effect was absent because a counter-mechanism existed that I had not
  enumerated.** The cheap habit that would have caught all three: before writing a predicted defect
  down, name what would have to be true for it *not* to happen.
- `[2026-09-12]` **The field that only ever held one value was the unenforced kind, and today
  proved which.** `status: verified` stood in all 44 notes. The 2026-09-08 entry above posed the
  fork — *either the base genuinely has no provisional page, in which case the field tells a reader
  nothing, or pages are marked verified on arrival, which is worse* — and recorded it rather than
  acting, because grading 44 pages is a judgement about the base's standard. **The second horn is
  now measured.** Four notes said `verified` while the primary they rest on could not be opened in
  this container at all, and one of them (`llm-idea-generation`) carried a claim that turned out
  **inverted** against that unopened source. `verified` meant *written*.
  Resolved by **deriving it instead of asserting it**, because a value another file can falsify is
  a query and not a claim: `reproducible` if the page names a held raw copy, `cited-only` if not,
  `note-only` if it cites nothing retrievable. Deliberately not verified/unverified — a page whose
  sources predate the raw layer *was* checked, just not reproducibly, and the field must not say
  otherwise. It comes out **22 / 22**, which is the first time this field has discriminated
  anything. Two `status='verified'` filters in staleness queries went with it: they scoped nothing,
  and a page we cannot re-derive is *more* urgent to re-read when stale, not less. Three lint
  checks that were gated on the same constant are now unconditional, which is what they always
  were in practice.
  **And the general check the 09-08 entry asked for now ships:** `single_valued()` reports any
  frontmatter field whose distinct-value count is one across the corpus. It is silent today, which
  is the point — it fires the next time someone adds a field everyone agrees on.
- `[2026-09-12]` **A directive promoted in the morning caught a real hole in the afternoon, in the
  code written to close the item that promoted it.** Seven mutations against the two new predicates;
  six caught. The survivor loosened the regex that decides whether a frontmatter line *names* a raw
  copy or merely *mentions* one in prose — and it survived because `derive_status` takes counts and
  cannot see how they were produced. That is exactly *"test the WIRING, not only the predicates"*,
  promoted into `TEST-AUTHORING-LESSONS.md` hours earlier out of this very file. The fixture now
  feeds `frontmatter()` one real bullet and one quoted prose line naming a path, and asserts the
  count is 1. Seven of seven. **A directive is worth what it catches, and this one caught its own
  author the same day it was written down.**
- `[2026-09-12]` **The compiled page's two standing warnings are cleared, and the fix was one row.**
  `third-party-landscape` is 31 KB compiled over five notes; the `compiled_from:` join key had been
  warning since 2026-09-08 that two inputs had moved past its compile date. The proposal treated
  this as "recompile the page", which is why it sat for four days — 31 KB of synthesis is a rewrite.
  It was not a rewrite. **The check names WHICH inputs moved**, so the work was to re-read two notes
  and find what they changed: `graphify-assessment`'s obsidian chain was already carried here (the
  page says "settled 2026-09-04"), and the Ornith-1.5 row was stale on a **provenance label** —
  MIT had been upgraded REPEATED → MEASURED against the model card's own frontmatter, and the
  ownership claim both secondary sources agreed on had been refuted. One row, edited.
  **A compiled page rots one row at a time, and a join key that names the moved input is what makes
  reconciling it affordable instead of a rewrite.** The proposal's cost estimate was wrong because
  it priced the page, not the diff.
  Two limits written into the page where they can be acted on. The snapshot records each input's
  **own** declared fetch, not the reconcile date — a snapshot saying 09-12 would claim the input
  declared something it never did, and the key's whole value is that both sides of the comparison
  are the input's words. And **the key is self-reported**: bumping the dates clears the warning
  whether or not a row was re-read. It says when to look, never that you looked, and no script can
  close that — but the narrowing is real, and it is the difference between two notes and five.
- `[2026-09-12]` **The overage was content, not padding, and a character count could never have
  said so.** 13 descriptions exceed the spec's 1,024 and the item had stood open because trimming
  changes routing and no baseline existed. Two measurements closed it without one. First: of the
  quoted trigger phrases in those 13, **zero** could be deleted with no content word lost — in 12
  of 13 the overage carries no restatement at all. Second, and decisive: strip **every** connective
  word and rejoin, and **7 of the 13 are still over 1,024**. For those, complying requires deleting
  a word the router matches on, so it is a capability cut wearing a formatting fix's clothes.
  Decision: **do not trim**, reported per unit with its floor instead of as a count.
  Two general things fall out. **A limit you cannot meet is a fact about the limit as much as about
  the thing** — this library's house style (triggers-only, keyword-rich, explicit NOT-clauses
  naming siblings) and a 1,024-character field are not both satisfiable, and the spec asks for the
  keywords in the same breath as the cap. And **half a migration is worse than either end**: fixing
  only the six that can comply changes routing for six working skills while leaving the library
  exactly as unusable on a conforming host, because such a host rejects on the first violation.
  `pipeline/decisions/2026-09-12-description-spec-limit.md` carries the table and the reopen
  condition.
- `[2026-09-12]` **A fixture built on a length-neutral case cannot catch the mutation it was
  written for.** `lossless_floor`'s compound-token fixture used `CSV/JSON`, and the mutation that
  splits compound tokens **survived** it — because a separator BETWEEN two words costs one
  character and its replacement costs one space, so both implementations return the same number.
  The case that separates them is punctuation at a token's **edge**, which splitting drops.
  Generalises past this function: when a fixture is meant to catch a transformation, check that the
  transformation actually CHANGES the value you are asserting on. A test can be about the right
  thing and still be blind.
- `[2026-09-12]` **A map line had been routing "edit a skill" to the talent whose description refuses
  it.** The capability-map trim tested each line by asking whether any of its content words were
  absent from the owning talent's own description — a line that adds nothing cannot change which
  talent is chosen, because selection reads descriptions. 25 of 83 lines added ≤2 words and were cut,
  3,886 → 3,341 tokens per turn. Then the **no-op test after the cut** found four lines had been
  carrying a trigger keyword the description lacked: `done`, `handoff`, `improve` — and `edit`.
  The first three went **into the descriptions**, not back into the map: that is what the router
  reads, it is portable, and it costs 5-10 characters against a line's 60-100. The fourth was the
  find. `writing-skills` says *"Use when AUTHORING a new skill from scratch"* and explicitly NOT for
  sharpening an existing one, so *"Author / edit a skill → writing-skills"* was **a misroute the map
  had been publishing for as long as the line existed.** Adding the keyword would have entrenched it;
  cutting the line removed it.
  Three general things. **A count of novel words cannot tell a connective from a trigger keyword** —
  the ≤2 threshold is exactly what let those four through, and only the no-op test caught it. **A
  second routing index can contradict the first**, and nothing checks that it doesn't. And **a
  keyword's cheapest home is the description**, because the map costs tokens every turn while the
  description was already paid for.
- `[2026-09-12]` **"Redundant with nothing" is not redundancy.** One of the 26 candidates pointed at
  `templates/` — a **directory**, not a talent — so the predicate compared its words against the
  empty string, found none novel, and called it redundant. Spared on inspection. An absent value and
  a zero value read the same to a comparison that does not check which it has, and this is the third
  time that shape has appeared in this base.
- `[2026-09-12]` **A positive control caught an eval suite that was scoring an empty plugin.** The
  library is now packaged for `claude plugin eval`, and the first run of the suite was clean: four
  cases, a written report, mean Δ 0.00, and every `tool_used: Skill` grader failing with
  `Skill called 0x` **in both arms**. No error. The tool's own troubleshooting page says that shape
  is *"usually a real finding, meaning the skill's description doesn't trigger on the prompt's
  phrasing"* — and taking that at face value would have recorded **four false routing failures** and
  sent someone to rewrite four descriptions that had never been consulted.
  The control was one case whose prompt says *"Use the budget-cut-triage skill"* by name: a named
  skill that does not fire cannot be a description problem. It scored 0.00, so the skills were never
  reaching the runs, and every score in that run was an artefact. Cause: a plugin reads its skills
  from **`skills/`** and this repo keeps them at **`.claude/skills/`**. `skills -> .claude/skills`
  fixes it; with the skills loaded the same suite scores **5 of 5, mean Δ +0.70, $1.09**.
  *The failure was not that it errored, it is that it parsed* — fourth recorded instance here, second
  today. **Before believing a suite's verdict, run one case the suite must pass for a reason that has
  nothing to do with what you are measuring.** A green report over an empty plugin looks exactly like
  a red result about a real library.
- `[2026-09-12]` **Two commands disagree about symlinks on purpose, and only one of them says so.**
  The runtime follows `skills -> .claude/skills` (proved: the control fires). `claude plugin validate`
  does not, and prints *"this directory is a symlink and nothing in it was read … validate the real
  directory separately."* So validating the plugin root now reads **zero** skills, and
  `claude plugin validate .claude/skills` is its own step. A check that silently examines nothing is
  the same failure class as the empty-plugin run above; this one at least announces it.
- `[2026-09-12]` **The cost objection was right about the mechanism and had no number.** The
  with/without ablation really does double the agent runs, and an `llm` grader really does see only
  the first 12 and last 12 trace messages. But **four of the six grader types cost nothing** —
  `regex`, `tool_used`, `tool_order`, `file_exists` are computed from the transcript and files — so a
  suite with no `llm` grader pays for agent runs alone, `--max-cost-usd` caps that before each run
  launches, and the whole thing measured **$1.09**. An objection stated as a mechanism ("it doubles")
  survives indefinitely; the same objection with a dollar figure is settled in one pass.
- `[2026-09-12]` **Three runs per case, and zero spread — so the smoke test was right for a reason.**
  The routing suite at the tool's default (5 cases × 3 runs × 2 arms, 30 runs, 893 s, **$3.41**)
  returned **5 of 5 passing, mean Δ +0.70, and not one case varying between its three runs.** For
  graders that ask *which skill fired*, that is the finding: routing on these prompts is not a coin
  flip. The conclusion is not "one run is enough" — it is that **the variance is now measured
  instead of assumed**, and has to be re-measured when a case is added. Cost scaled linearly,
  $1.09/10 runs to $3.41/30, so a budget for this suite is arithmetic now.
- `[2026-09-12]` **A run that hit the turn limit still scored 1.00, and that is the suite's ceiling
  rather than a bug.** One run ended `Reached maximum number of turns (8)` and scored full marks,
  because both its graders are `tool_used` checks on which skill fired — which happens in the first
  turns. Not patched: raising the limit costs more for no extra signal and lowering it truncates
  every run. What it names is what the suite can and cannot claim. **These cases prove the right
  talent is SELECTED; they say nothing about whether the work was good.** An outcome grader is what
  buys the second claim, and only then does the turn limit have to reach an outcome.
- `[2026-09-12]` **A sandbox that announces it did not hold is doing its job.** The eval harness ran
  as root, so the directory mode it uses to seal the scaffold did not bind, and it said so: the tree
  may be agent-written, do not run git or load configuration from anywhere inside it, here is the
  command to remove it. Removed exactly that way, from outside, without entering it. The failure mode
  to fear is the silent version — an agent-writable tree left in `/tmp` with a `config/` that a later
  command picks up. **Before running any eval suite unattended in a container, check who the harness
  is running as**, because the OS-level confinement its documentation describes is not in force as
  root.

