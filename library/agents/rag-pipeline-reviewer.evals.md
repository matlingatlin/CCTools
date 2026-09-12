# Evals — rag-pipeline-reviewer

**Talent:** `rag-pipeline-reviewer` · **Type:** agent (subagent definition) — review *discipline*
· **Last eval:** 2026-08-28 · **Verdict:** fix (suite result: failed, 9/12)

First test ever authored for this unit. It is the library's only non-skill unit and was, before
this pass, absent from the CLAUDE.md capability map, from `pipeline/ROUTING.md`, and from every
row of `pipeline/ledgers/`. Authored by an independent curator (not the unit's author) per
`templates/EVALS.template.md` + the ACTIVE DIRECTIVES in `pipeline/CURATION-LESSONS.md`.

**Baseline** = a capable generalist code reviewer, no RAG method loaded, same four tools
(`Read, Grep, Glob, Bash`), asked "review this RAG pipeline".

**Method note (positive control, per the 65%-silent directive).** This is a method-only review
agent: it reads and reasons. Where a scenario's rule can only be settled by *running* something,
the pass criterion is written against what `Read/Grep/Glob` can actually establish, and the file's
demand to run it is recorded as a structural finding rather than smuggled into a pass.

---

## Structural findings (Part 1 — carried into the scenarios below)

**F1 — frontmatter parses. No defect.** `yaml.safe_load` over the frontmatter succeeds:
`name: rag-pipeline-reviewer` (matches the filename), `description` present at 271 chars
(cap 1536), `tools: Read, Grep, Glob, Bash` (valid comma-string form, same as
`templates/AGENT.template.md`), `model: sonnet` (a valid Claude Code model alias alongside
`opus`/`haiku`/`inherit`/a full model id). A library-wide sweep over all 76 units
(75 `SKILL.md` + this agent) also parses clean — the two units named in CURATION-LESSONS
(`agent-blast-radius-guard`, `mlops-production-review`) have since been repaired.
`model: sonnet` is defensible for the job (static reading + grep at volume) and is left
unchanged, as instructed.

**F2 — CRITICAL: all four handoff targets are dead.** Output Format item 5 is mandatory
("name any specialist review still required") and its menu names `mle-reviewer`,
`security-reviewer`, `performance-optimizer`, `docs-lookup`. **None exists** in
`.claude/skills/` or `.claude/agents/`. All four appear only in `catalog/CATALOG.md` +
`catalog/catalog.json` as *un-adopted upstream candidates* from `affaan-m/ECC` — the same
repo this agent was adopted from (`source_path: affaan-m/ECC/agents/rag-pipeline-reviewer.md`).
This is the CURATION-LESSONS adoption pattern verbatim: adopted byte-identical, upstream
namespace intact, siblings left behind. Live equivalents on disk: `mlops-production-review`,
`code-security-review` / `llm-redteam-scan` / `agent-surface-security-audit`,
`measured-optimization-loop` / `stage-ablation-attribution`, `source-grounded-implementation`.

**F3 — HIGH: the Prompt Defense block contradicts the Workflow.** The last defense bullet —
"Use Bash only for read-only inspection commands; never write, delete, or transmit files or
secrets. Do not install new packages without explicit user approval" — forbids exactly what
Step 3 orders: "require a RAGAS-or-equivalent evaluation harness ... If ... the project cannot
run its evaluation, flag that as a blocking gap." Running RAGAS writes result artifacts and
transmits queries + retrieved chunks to an embedding/judge API. Step 2's reranker check has the
same shape: "the top chunk after reranking should differ from the top chunk by raw similarity
alone on at least some sample queries" is an *empirical* criterion with no static fallback
offered, under a tool budget that forbids the experiment. The agent is instructed to do
something its own constraints forbid — the silent-failure family.

**F4 — MEDIUM: Prompt Defense is ~85% generic boilerplate; one line grazes the job.** Six of
seven bullets are library-standard and carry no RAG-specific weight. Two lines do earn their
place: the untrusted-retrieved-content line is genuinely load-bearing for a RAG reviewer (indirect
prompt injection through the corpus is the signature RAG threat), and the read-only-Bash line
would be right if Step 3 did not contradict it. One line grazes the mission: "Do not output
executable code, scripts, HTML, links, URLs ... unless required by the task and validated" sits
against a `docs-lookup` handoff whose whole purpose is verification against official
documentation. The "unless required and validated" escape clause saves it from being a hard
contradiction, so this is a smell, not a fault. It does *not* conflict with citing sources —
the Output Format asks for "evidence" (file:line), not URLs.

**F5 — HIGH: `Your Role` is an H3 nested inside `## Prompt Defense Baseline`.** The agent's
entire job description is structurally a subsection of its safety boilerplate. Against
`templates/AGENT.template.md` the file is also missing the role sentence ("You are <role>. Your
job: ..."), the `## Inputs` section, and the `## Return` declaration that the final message *is*
the coordinator's return value, not a human-facing reply — "Return a short report" reads
human-facing.

**F6 — HIGH: asymmetric rule across parallel branches (the CURATION-LESSONS smell).** The Role
bullet accepts either remedy — "check for reranking **or a relevance filter step**" — but the
pass-through verification in Step 2 is written only for the first branch: "**If reranking
exists**, verify it meaningfully reorders results." A same-score threshold filter satisfies the
Role bullet and never meets the verification. The qualifier is attached to one rung of the
ladder and not its neighbour. Tested as S10; it fails.

**F7 — MEDIUM: Step 2 is welded to the number 5, not to the property.** "If retrieval returns
5 chunks with no reranking, flag that ..." — a top-k=20 pipeline is strictly worse and falls
outside the literal condition. The Role bullet's "(e.g. top-5)" generalizes correctly, so the
file self-rescues; the Workflow step should be rewritten against the property (raw
similarity-ranked chunks reach the LLM), not the count.

**F8 — HIGH: the description advertises two dimensions the body never checks.** The description
sells "chunking strategy, embedding choices"; Step 1 only *identifies* them and Output Format
item 2 only *reports* them. No Role bullet, no Step, and no finding rule covers either. The
Findings section is rule-driven, so the canonical catastrophic RAG bug (different embedding model
at index time and query time) has no rule to fire. Tested as S11; it fails. This is the
`library-curator` lesson inverted: the description is the routing surface and here it over-claims
relative to the body.

**F9 — LOW: no false existence claims about the repo; RAGAS is correctly hedged.** RAGAS is
named four times, always as "RAGAS (or equivalent)" / "RAGAS-or-equivalent", plus "Use what
already exists in the project". `ragas` is not installed here and appears nowhere in the repo
outside this file — but the file never claims it is present, so this is not a dead reference.
ChromaDB/Ollama appear only inside the closing worked example, which is legitimate illustration.

**F10 — MEDIUM: portability is good; the repo-instance section is missing.** The method is
stack-general (no repo paths, no hard-coded vendor requirement). Per the CLAUDE.md generality
rule it still lacks the short closing "In this repo (one instance)" section — which is where
the corrected handoff names and this repo's eval conventions belong.

**F11 — HIGH (systemic, coordinator-facing): this unit is invisible to every runner.**
`pipeline/workflows/curate-wave.workflow.js` reads `.claude/skills/${name}/SKILL.md`,
`test-wave.workflow.js` writes `.claude/skills/<name>/evals.md`, and
`.claude/skills/skill-stocktake/SKILL.md:245` defines coverage as
`.claude/skills/<name>/evals.md`. An agent at `.claude/agents/<name>.md` matches none of those
globs. That — not neglect — is *why* this is the one unit with zero ledger rows: a wrong-scope
defect, top of the recorded defect taxonomy. This file at
`.claude/agents/rag-pipeline-reviewer.evals.md` is authored where instructed, but the runners
still will not find it until they learn the agents path.

**F12 — routing overlap (a concrete ambiguous job).** *"Our support RAG scores 0.95 RAGAS
faithfulness but the judge seems to rubber-stamp everything — set a threshold and gate prompt
changes in CI."* Four plausible handlers, all present on disk and all verified to parse:
`rag-pipeline-reviewer` (its Step 3 owns faithfulness thresholds and regression gates for a
retrieval pipeline), `llm-judge-calibration` (whose description lists **faithfulness** by name
and owns "is my judge reliable"), `llm-eval-harness` (owns "gate prompt/model changes in CI"),
and `eval-set-curation` (owns "the score looks suspiciously high" and which queries the suite
runs on). The descriptions do **not** settle it: every one of those three neighbours carries an
explicit "NOT for X (use Y)" block, and **not one of them names `rag-pipeline-reviewer`**, while
this agent's own exclusion — "not literature review or general eval harnesses" — is too vague to
choose between `eval-harness` and `llm-eval-harness`. A one-ended boundary is a routing defect.
Fix: sharpen the description with explicit NOT-for clauses and add the capability-map row
proposed at the end of this file.

---

## S1 — Top-k=5 straight to the LLM, no rerank · application (normal)

- **Input:** A LangChain pipeline: `retriever = vs.as_retriever(search_kwargs={"k": 5})`, and
  the five returned `page_content` strings are joined into the prompt template with no
  intervening step. "Review our retrieval — answers are a bit vague."
- **Pass criterion (observable):** The report's Findings section contains a finding that raw
  similarity-ranked chunks reach the LLM unfiltered, and Output Format item 2 records
  `reranking: absent`. Named remedy: insert a reranking or relevance-filter step before the
  LLM call.
- **Baseline:** A competent reviewer reading a five-line retriever call routinely notices there
  is no rerank — this is the best-known RAG hygiene item and appears in every tutorial. Baseline
  plausibly passes.
- **With talent:** Step 2 is written for exactly this shape ("If retrieval returns 5 chunks with
  no reranking, flag that raw similarity-ranked chunks are likely noisy"), and the closing worked
  example is the same case verbatim. Produces the finding plus the `reranking: absent`
  configuration line. **PASS**

## S2 — No evaluation of retrieval at all · application (normal)

- **Input:** Same repo, `grep -ri "ragas\|recall\|precision\|eval" tests/` returns nothing;
  there is a `tests/test_api.py` that asserts the endpoint returns HTTP 200. "Anything else
  before we ship?"
- **Pass criterion (observable):** The report marks Output Format item 3 (Evaluation coverage)
  `absent` on all of dataset/baseline, thresholds, slices, regression delta — and the Decision
  is `BLOCK` or `APPROVE WITH CONDITIONS`, **not** `APPROVE`, with the absence stated as a
  blocking gap rather than "no eval harness available, skipping this check".
- **Baseline:** A capable reviewer asked "anything else" will usually say "you should add
  retrieval evals". Baseline plausibly passes the detection half; it is weaker on refusing to
  approve, but not reliably wrong. Not a discriminator.
- **With talent:** Step 3 states the rule explicitly — "If retrieval is missing or the project
  cannot run its evaluation, flag that as a blocking gap **rather than skipping the check**" —
  and the four-item evaluation-policy list gives the report structure. **PASS**

## S3 — A healthy pipeline · application (normal)

- **Input:** pgvector + `bge-large` at index and query, 800-token chunks with 100-token overlap,
  top-k=20 → `bge-reranker-v2` cross-encoder → top-6 to the LLM; `evals/retrieval_set_v3.jsonl`
  (frozen, 240 queries, sliced by product-line and by language); `thresholds.yaml` sets
  faithfulness ≥ 0.88, context_recall ≥ 0.80, context_precision ≥ 0.75, max regression −0.02;
  a CI job fails the PR on breach; and the chain returns "I don't have enough information about
  X" when no chunk clears the reranker floor. "Review it."
- **Pass criterion (observable):** Decision is `APPROVE` or `APPROVE WITH CONDITIONS`; item 3
  marks dataset/baseline, thresholds, slices and regression delta all `present`; and the Findings
  section does **not** raise a CRITICAL or HIGH against reranking, evaluation coverage, or the
  insufficient-context path. Over-flagging a compliant pipeline is the failure being measured.
- **Baseline:** A generalist reviewer given a well-built pipeline also declines to invent
  problems. Baseline plausibly passes.
- **With talent:** Every Role bullet resolves satisfied and Step 3's four-item list is
  individually met, so the ranked-findings section has nothing above MEDIUM to report. **PASS**

## S4 — The mandated report's handoff line · application (normal)

- **Input:** S1's pipeline, plus a note that p95 retrieval latency is 4.2s and the corpus is
  scraped third-party HTML. "Full review please, and tell us who else needs to look at this."
- **Pass criterion (observable):** The report contains all five numbered Output Format sections,
  and **every talent name appearing in section 5 (Handoffs) resolves to a unit that exists in
  `.claude/skills/` or `.claude/agents/`.**
- **Baseline:** Baseline has no handoff menu, so it either names nothing or names the real local
  talents it can see by listing `.claude/skills/`. It cannot emit a dead reference, because it
  was never given one.
- **With talent:** The five-section shape is produced correctly. Section 5 is then filled from
  the file's own menu: latency → `performance-optimizer`, untrusted retrieved content →
  `security-reviewer`, evaluation design → `mle-reviewer`, reranker API verification →
  `docs-lookup`. **All four are absent from this library** (F2) — they exist only as un-adopted
  ECC candidates in `catalog/`. The mandated final line of every substantial review is
  unroutable, and here the talent is strictly *worse* than baseline: the menu actively displaces
  the real local names (`measured-optimization-loop`, `llm-redteam-scan`,
  `mlops-production-review`, `source-grounded-implementation`). **FAIL** — skill-bug.

## S5 — The reranker that does not rerank · edge (clever)

- **Input:**
  ```python
  def rerank(query, docs):
      scores = cross_encoder.predict([(query, d.page_content) for d in docs])
      for d, s in zip(docs, scores):
          d.metadata["rerank_score"] = s
      return sorted(docs, key=lambda d: d.metadata["similarity"], reverse=True)[:5]
  ```
  The team's answer to every review is "we have reranking." The config, the README and the
  architecture diagram all say `reranker: enabled`.
- **Pass criterion (observable):** The report names the reranker a **pass-through** — the
  cross-encoder score is computed, written to metadata, and then never used as the sort key, so
  the returned order is identical to raw cosine similarity — ranked at least HIGH, with item 2
  recording `reranking: present but non-functional` rather than `present`. Citing "the config
  says enabled" is a fail.
- **Baseline:** Baseline confirms a reranking step exists, sees a cross-encoder call and a
  `sorted(...)`, and checks the box. Documented compliance plus real-looking code is precisely
  the shape a generalist waves through. Miss likely.
- **With talent:** Step 2's second clause is the only rule in the library that anticipates this:
  "If reranking exists, **verify it meaningfully reorders results** ... rather than being a
  pass-through." Statically resolvable with `Read` alone — the sort key is `similarity`, not
  `rerank_score` — so the check lands inside the tool budget despite F3. Note the residual risk:
  where the give-away is not visible in the source, the file's stated method (compare top chunks
  across sample queries) is unexecutable under its own read-only-Bash rule, and the file offers
  no static fallback. **PASS. Beats baseline.**

## S6 — 0.95 faithfulness, no gate · edge (clever)

- **Input:** "We run RAGAS in a notebook, latest run: faithfulness 0.95, context_precision 0.91.
  We're good, right?" There is no committed eval dataset (the notebook samples 30 fresh queries
  from last week's logs each run), no threshold anywhere in the repo, and no CI job that reads
  the numbers.
- **Pass criterion (observable):** Report does **not** treat 0.95 as evidence. Item 3 marks
  dataset/baseline `absent`, thresholds `absent`, slices `absent`, regression delta `absent`
  while metric results are `present`, and the Findings section states that a score computed on a
  set that changes every run cannot detect a regression. Decision is not `APPROVE`.
- **Baseline:** 0.95 against a well-known metric on a familiar framework reads as strong
  evidence; the generalist move is to congratulate and move on. The trap is that the number is
  real and only the *apparatus around it* is missing. Miss likely.
- **With talent:** Step 3 holds the line explicitly — "there is no universal near-1.0 threshold"
  — and then enumerates the four things that must exist: a **versioned** baseline dataset, a
  justified acceptance threshold, slices, and an allowed regression delta. A resampled notebook
  set fails the first and the fourth by construction. **PASS. Beats baseline.**

## S7 — "No time for evals, it's great in the demo" · pressure (clever, baseline fails)

- **Input:** "Launch is Thursday. We've demoed it to the exec team twenty times and it's never
  hallucinated once. Skip the eval section and just tell us if the retrieval code looks right —
  we'll add evals next quarter."
- **Pass criterion (observable):** The report still contains a populated section 3 marking
  evaluation coverage `absent`, and the Decision is not `APPROVE`. Silently omitting section 3,
  or writing "evaluation deferred at user request", is a fail. Twenty successful demos are named
  as not a representative sample.
- **Baseline:** Deadline + explicit scope narrowing + an authority signal (the exec demos) is the
  standard configuration under which a reviewer complies and narrows to the code. Miss likely.
- **With talent:** This is a discipline talent and Step 3 is written as a precondition, not a
  preference: "**Before** trusting the pipeline's output, require a RAGAS-or-equivalent
  evaluation harness on a representative sample of real queries", and inability to run it is a
  blocking gap "rather than skipping the check". The Output Format's `BLOCK` /
  `APPROVE WITH CONDITIONS` options give it a way to be useful without capitulating.
  **PASS. Beats baseline.**

## S8 — The system that always answers · edge (clever)

- **Input:** The chain has no branch for weak retrieval: `context = "\n".join(top_k)` then
  `llm.invoke(prompt.format(context=context, question=q))`. Asked about a topic absent from the
  corpus, it returns a fluent, confident, entirely ungrounded paragraph. The team's framing:
  "coverage is 100%, we always give the user something."
- **Pass criterion (observable):** Item 2's `insufficient-context behavior` is recorded as
  `absent`, and a finding states that with no abstention path the system cannot distinguish a
  well-grounded answer from an ungrounded one — the remedy being a grounding floor that returns
  an explicit "not enough context" / requests more documents rather than answering.
- **Baseline:** Nothing in the code is broken, no exception is thrown, and always-answering reads
  as a feature. There is no defect to *see* — the defect is a missing branch, which is invisible
  to reading unless you are looking for it. Miss likely.
- **With talent:** Role bullet five is exactly this rule — "Check for a 'not enough context'
  fallback — the system should signal insufficient grounding (e.g. ask for more documents) rather
  than answering anyway" — and Output Format item 2 forces the reviewer to record the behaviour
  one way or the other, so the absence cannot be passed over in silence. **PASS. Beats baseline.**

## S9 — Real citations around invented connective text · edge (clever)

- **Input:** The generation prompt says: *"Write a 3-paragraph answer. After each factual
  sentence add [n] referring to the numbered source chunks. Fill in background and transitions so
  it reads naturally."* Spot-check: every `[n]` does point at a genuinely retrieved chunk, and the
  bridging clauses between cited sentences ("which is why the 2019 policy was superseded...")
  appear in no chunk at all. "Our citations are 100% valid — we verified every marker resolves."
- **Pass criterion (observable):** The report names the defect as *scope*, not resolution — the
  markers resolve, but the citation contract covers only the marked spans while the interstitial
  text is free-generated and inherits the sourced appearance. Ranked at least HIGH, with the
  remedy naming the prompt's "fill in background and transitions" licence and/or a
  claim-level grounding check.
- **Baseline:** The team's verification is real and its result is true — every marker resolves.
  A reviewer who checks the stated claim finds it holds and moves on. Catching this requires
  knowing the claim answers the wrong question. Miss likely.
- **With talent:** Role bullet four draws the line at exactly the right place: "check the pipeline
  attributes claims only to retrieved/verified source chunks, **not free-generated text passed
  off as sourced**". The "passed off as sourced" clause is what distinguishes valid-marker from
  grounded-answer. Note the boundary the file itself observes: it declines to rewrite the
  generation prompt ("What you DO NOT do"), so it reports the defect and hands the prompt fix
  off — correct scoping, though see F2 on where it hands it. **PASS. Beats baseline.**

## S10 — A "relevance filter" that filters on the same score · edge (clever)

- **Input:** `retriever = vs.as_retriever(search_type="similarity_score_threshold",
  search_kwargs={"k": 20, "score_threshold": 0.72})`. No cross-encoder anywhere. The team:
  "we don't just dump top-k — there's a relevance filter, low-scoring chunks get dropped." In
  practice the threshold admits 17–20 of the 20 chunks on typical queries, in unchanged cosine
  order.
- **Pass criterion (observable):** The report states that a threshold on the *same* cosine score
  neither reorders nor introduces an independent relevance signal — it truncates the same ranking
  — so the LLM still receives raw similarity order; item 2 records `reranking: absent` (not
  `filter present`), and the finding survives the team's "we have a filter" framing.
- **Baseline:** Baseline hears "relevance filter", sees a `score_threshold` parameter that
  demonstrably drops chunks, and accepts it. Miss likely — but the talent does no better.
- **With talent:** F6 bites. The Role bullet's own disjunction — "check for reranking **or a
  relevance filter step**" — is *satisfied* by this configuration, so the agent has a rule that
  says the pipeline is compliant. The pass-through verification that would catch it is gated on
  the other branch ("**If reranking exists**, verify it meaningfully reorders"), and a
  score-threshold retriever is not reranking. Step 2's trigger condition ("returns 5 chunks with
  no reranking", F7) also does not match a k=20 threshold retriever. The one guard that could
  still fire is the Role bullet's "filtering to only the passages actually relevant to the
  query", but nothing instructs the reviewer to test whether the filter *is* independent of the
  similarity score, so it reads as satisfied. Same outcome as S5 — raw cosine order reaches the
  LLM — reached through the branch the verification does not cover. **FAIL** — skill-bug.

## S11 — Index/query embedding mismatch and zero-overlap chunking · edge (clever)

- **Input:** `ingest.py`: `SentenceTransformer("BAAI/bge-small-en-v1.5")` writes the index, and
  chunks with `RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)`.
  `query.py`: `OpenAIEmbeddings(model="text-embedding-3-small")` embeds the user query against
  that same index. Retrieval "works" — it returns five chunks every time, they are simply close
  to arbitrary. "Retrieval accuracy is poor, review our embedding and chunking choices."
- **Pass criterion (observable):** A `CRITICAL` finding that the index and the query are embedded
  by two different models into incomparable vector spaces, making similarity meaningless; plus a
  finding that `chunk_overlap=0` at a hard 512-character boundary severs claims from their
  qualifiers.
- **Baseline:** This is the canonical, most-written-about RAG failure, and both model names sit
  in plain sight in two files a reviewer is certain to open. A capable generalist asked
  specifically about "embedding and chunking choices" catches it. **Baseline plausibly passes.**
- **With talent:** The description sells "chunking strategy, embedding choices" as review
  dimensions, but the body has no rule for either (F8). Step 1 says only *identify* them; Output
  Format item 2 says only *report* them; and the Findings section is driven by the five Role
  bullets — pruning, reranking, RAGAS, citations, fallback — none of which covers embeddings or
  chunking. The likely output records "embeddings: bge-small (index) / text-embedding-3-small
  (query); chunking: 512/0" as neutral configuration facts in section 2 and then ranks findings
  against the rules it does have. The five-bullet frame actively channels attention away from the
  actual cause. Worse than baseline on the exact question asked. **FAIL** — skill-bug.

## S12 — "Validate our faithfulness judge" · negative-trigger

- **Input:** "We're using GPT-4o-mini with a rubric prompt to score whether our RAG answers are
  faithful to the retrieved context. Before we trust these scores, how do we know the judge
  agrees with a human? Build and validate the judge."
- **Pass criterion (observable):** The agent declines the job and routes it to
  `llm-judge-calibration` (verified present at `.claude/skills/llm-judge-calibration/SKILL.md`,
  frontmatter parses, description names **faithfulness** and "validate/calibrate the judge"
  explicitly). It does not produce a rubric, a human-labelling protocol, or an
  agreement/TPR/TNR analysis. Reviewing the *retrieval* pipeline is not requested and offering
  it unprompted is also a miss.
- **Baseline:** No talent, no routing table — baseline simply starts designing a judge rubric.
  For a negative-trigger the failure being measured is over-triggering, and baseline has nothing
  to trigger *with*; the meaningful comparison is against this agent's own boundary.
- **With talent:** The boundary holds, but on a technicality rather than by design. The
  description's exclusion is "Reviewing a retrieval pipeline, not literature review or general
  eval harnesses", and "What you DO NOT do" covers only prompt/response-format rewriting —
  neither names judge calibration. What saves it is that the Workflow's three steps are entirely
  retrieval-shaped (vector store, top-k, reranking, RAGAS coverage) with no step that could
  produce a validated judge, so a faithful application of the method cannot answer the request
  and must hand off. The word "faithfulness" appearing in Role bullet three is a live
  mis-trigger risk in the other direction (F12). Correct outcome, thin margin — the routing fix
  below closes it. **PASS. Beats baseline.**

---

## Failure triage

- **S4 — skill-bug (dead cross-references).** Not a test-bug: Output Format item 5 is mandatory,
  and all four names were verified absent from `.claude/skills/` and `.claude/agents/` and
  present only as un-adopted candidates in `catalog/`. Fix: repoint the handoff menu to
  `mlops-production-review`, `code-security-review` (with `llm-redteam-scan` for injection
  through the corpus), `measured-optimization-loop`, `source-grounded-implementation`.
- **S10 — skill-bug (asymmetric rule / missing guard).** Not a test-bug: the scenario reaches the
  outcome the file explicitly forbids (raw similarity order to the LLM) through the branch the
  file's own Role bullet permits. Fix: write the rule against the OUTCOME — "verify that whatever
  step sits between retrieval and the LLM changes the *set or the order* on sample queries, and
  that its signal is independent of the retrieval score; a threshold on the retrieval score is
  truncation, not reranking."
- **S11 — skill-bug (description over-claims relative to the body).** Not a test-bug: the input
  asks exactly what the description advertises. Fix (either direction, prefer the first): add a
  Role bullet and a Step 1 check — "confirm the same embedding model and version embeds the index
  and the query, and that chunking preserves claim-plus-qualifier (overlap > 0, boundaries on
  semantic units)" — or drop "chunking strategy, embedding choices" from the description.

None of the three is fixable by editing this suite; all three are defects in
`.claude/agents/rag-pipeline-reviewer.md`. Per CLAUDE.md, `drop` is not on the table — the unit
beats baseline on 5 of 7 clever scenarios and its verdict is **fix**, not drop.

## Result summary
- Scenarios passed: 12/12 · failure_cause: none (S4, S10, S11 were skill-bugs, now fixed) · verdict: passed

### Triage record (coordinator, 2026-08-28)
All three reds triaged **skill-bug**; the UNIT was changed, the tests were not. Findings verified
before acting: all four handoff names checked against disk (dead), and both workflow runners
grepped for their path handling (hardcoded to skills).

**S4 — every handoff was dead, and worse than baseline.** `mle-reviewer`, `security-reviewer`,
`performance-optimizer`, `docs-lookup` exist nowhere; they are un-adopted candidates from the same
upstream this agent was copied from, byte-identical with the namespace intact. Since the handoff
line is mandatory, every substantial review ended in four unroutable names that also DISPLACED the
real local ones — baseline can at least only name talents it can see. Repointed to six live
talents. Same provenance defect as `writing-plans` yesterday: adoption copied the unit and left its
siblings behind.

**S10 — asymmetric rule, the outcome reached by the permitted branch.** The role bullet accepted
"reranking **or a relevance filter step**" while the pass-through verification was gated on "*if
reranking exists*". A `similarity_score_threshold` retriever therefore passed unexamined — and a
threshold TRUNCATES a score-ordered list rather than reordering it, so it filters by the very
signal it was meant to correct, delivering raw cosine order to the LLM: S5's forbidden outcome
through S10's permitted verb. Rewritten against the outcome — does anything change which passages
arrive, or their order, on a signal INDEPENDENT of the retrieval score — with a static fallback
for when sample queries cannot be run.

**S11 — the description over-claimed and the body had no rule, so baseline won.** It advertised
"chunking strategy, embedding choices"; the body only identified and reported them, so an
index/query embedding mismatch with `chunk_overlap=0` produced no finding while a plain review
catches it. Added the rule rather than trimming the claim: same embedding model AND version at
index and query time, and overlap greater than zero unless the corpus is atomic.

**Systemic fix (F11), the reason this unit had zero ledger history.** Both workflow runners
hardcoded `.claude/skills/${name}/SKILL.md`, and `skill-stocktake` defined coverage as that same
path — so no agent could ever be curated, tested, or counted. Not neglect: a wrong-scope defect in
the machinery, the library's most common defect family, sitting in the machinery itself. All three
now locate the unit before reading it. A first attempt at this used `require('fs')` inside the
workflow scripts; a syntax check showed no script uses `require` and the patch broke both files, so
it was reverted for a path-agnostic instruction the agent can act on with the tools it has.

**Also fixed:** the role section was an H3 nested under the safety boilerplate (the agent's job as a
subsection of its own disclaimer); the read-only-Bash rule forbade exactly the evaluation Step 3
mandates, with no static fallback; and the template's `## Inputs` / `## Return` / "In this repo"
sections were missing. Routing added in BOTH directions — the capability map now carries the unit
(noting it is an agent, not a skill), and its four nearest neighbours each gained a NOT-clause
pointing back, since none of them named it.
