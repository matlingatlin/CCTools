```json
{
  "collisions": [
    {
      "sibling": "deep-reading",
      "query": "(a) neighbour's job: \"summarize this paper / what does this 40-page spec really say\"",
      "picked": "deep-reading",
      "why": "deep-reading owns \"a long text needs to be summarized, digested\", \"reading a large file for genuine understanding\", \"the source may hide contradictions or unverifiable claims\" — the deliverable is comprehension. llm-wiki-ingest's decider is \"is about to become a note in an LLM-maintained wiki\" plus artefact nouns (\"raw, notes, schema\", \"index and log rows\", \"lint\"); a summarize request names no wiki and no note, so nothing in llm-wiki-ingest fires. Its own exclusion \"NOT summarising a text (deep-reading)\" confirms it from both ends."
    },
    {
      "sibling": "deep-reading",
      "query": "(b) this skill's job: \"add this fetched page to the knowledge base / this contradicts the note\"",
      "picked": "llm-wiki-ingest",
      "why": "CONTESTED — deep-reading also claims \"or ingested into the knowledge base\". llm-wiki-ingest wins on specificity: it names the artefact and the procedure (\"a note\", \"Karpathy LLM Wiki: raw, notes, schema\", \"quote before write\", \"neighbours name it back\", \"index and log rows\", \"lint\") and quotes the literal typed phrases \"add this to the knowledge base, ingest this source, put this in the wiki, update the note, this contradicts the note\". deep-reading's ingest clause is four words with no procedure and no artefact, and its own subject is \"a long text\" — it cannot handle a repo, screenshot or measurement. But the clause is a genuine one-way overlap: deep-reading does not name llm-wiki-ingest back."
    },
    {
      "sibling": "kb-curator (agent)",
      "query": "(a) \"walk the wiki and fix dangling links / pages missing from the index / near-duplicate pages\"",
      "picked": "kb-curator",
      "why": "kb-curator's decider is scope-wide and after-the-fact: \"walk an LLM-maintained knowledge base ... and fix what has rotted\", \"Dispatch after a batch of ingests, before a release ... or on a schedule\". llm-wiki-ingest is single-source and forward: \"a fetched page ... is about to become a note\". It cedes explicitly: \"whole-wiki clean-up is the kb-curator agent\", and kb-curator names it back (\"NOT for ingesting a new source (llm-wiki-ingest)\") — the cleanest boundary in the set."
    },
    {
      "sibling": "kb-curator (agent)",
      "query": "(b) \"I just fetched this page, put it in the wiki\"",
      "picked": "llm-wiki-ingest",
      "why": "One incoming source, no rot yet. kb-curator's trigger nouns are all defects (\"dangling and one-way links\", \"schema drift\", \"stale fetches\", \"orphan pages\") over an existing corpus; llm-wiki-ingest's is \"a fetched page, paper, repo, transcript or measurement\". Note the shared substrings \"index\", \"lint\", \"neighbours/one-way links\" — both mention lint, so the discriminator carrying the weight is one-source vs whole-base, not the mechanism words."
    },
    {
      "sibling": "skill-knowledge",
      "query": "(a) \"does this skill need external facts, and can I quote them before bundling?\"",
      "picked": "skill-knowledge",
      "why": "Its decider is the destination: \"before they are bundled into an artefact\", plus \"the coverage check that decides whether to fetch at all\". llm-wiki-ingest's destination is \"a note in an LLM-maintained wiki\". Both share \"quote\" (\"a claim without a verbatim quote is not a finding\" vs \"quote before write\") — the quoting discipline is common ground, the artefact is the discriminator."
    },
    {
      "sibling": "skill-knowledge",
      "query": "(b) \"ingest this source into the wiki\"",
      "picked": "llm-wiki-ingest",
      "why": "\"put this in the wiki\", \"index and log rows\" vs skill-knowledge's \"bundled into an artefact\". Named back explicitly: \"NOT claims for a skill bundle (skill-knowledge)\"."
    },
    {
      "sibling": "unified-memory",
      "query": "(a) \"save durable work state / hand off to another agent / resume a task\"",
      "picked": "unified-memory",
      "why": "\"save durable work state, hand off or resume another agent's task ... via the local ECC Memory Vault\" — machine-read rows for agents, a named store. llm-wiki-ingest produces human-readable pages (\"notes, schema\", \"index\", \"neighbours name it back\"). Excluded explicitly: \"NOT agent memory (unified-memory)\"."
    },
    {
      "sibling": "unified-memory",
      "query": "(b) \"record this verified finding so it survives compaction\"",
      "picked": "llm-wiki-ingest",
      "why": "Weakest boundary in the set. \"search shared project knowledge\" and \"durable\" overlap the durability motive, and this skill's body argues from compaction loss too. What decides it is the artefact vocabulary present in only one description — \"wiki\", \"note\", \"raw\", \"index and log rows\", \"lint\" — not the motive. A query phrased as \"remember this fact\" with no wiki named would legitimately go to unified-memory."
    },
    {
      "sibling": "memory-provenance-separation",
      "query": "(a) \"memory has an undated claim a user asserted, still steering decisions\"",
      "picked": "memory-provenance-separation",
      "why": "\"origin (asserted / observed / derived)\", \"as-of date\", \"staleness horizon\", \"gates read-time trust\" — it governs an already-stored row's believability. llm-wiki-ingest governs the write path (\"quote before write, claim verdicts\"). No name-back either way, but no real contest: neither description's trigger nouns appear in the other."
    },
    {
      "sibling": "memory-provenance-separation",
      "query": "(b) \"is this new claim true enough to write down?\"",
      "picked": "llm-wiki-ingest",
      "why": "\"quote before write, claim verdicts\" is a pre-write gate on a new source; the sibling's trigger is a row \"asserted once in an old session and still steering decisions\" — post-write, on stored state."
    },
    {
      "sibling": "doc-claim-reconciliation",
      "query": "(a) \"a merged PR renamed a flag and the runbook is now wrong\"",
      "picked": "doc-claim-reconciliation",
      "why": "\"code that already landed made a document FALSE\", \"From the merged diff\" — the input is a diff, and the docs are project docs (README, ADRs, --help). llm-wiki-ingest's input is \"a fetched page, paper, repo, transcript or measurement\". Named back: \"NOT docs broken by code (doc-claim-reconciliation)\"."
    },
    {
      "sibling": "doc-claim-reconciliation",
      "query": "(b) \"this new source contradicts an existing note\"",
      "picked": "llm-wiki-ingest",
      "why": "\"this contradicts the note\" and \"triage new/update/disputed\" are verbatim in llm-wiki-ingest; the sibling's contradiction is always code-vs-doc (\"docs say X but the code does Y\")."
    },
    {
      "sibling": "library-curator",
      "query": "(a) \"audit the adopted skill library for test coverage and overlapping descriptions\"",
      "picked": "library-curator",
      "why": "\"a library of capabilities that is ALREADY in place ... database 2\", \"sharpen mis-triggering/overlapping descriptions\", \"health scorecard\". Its object is skills; llm-wiki-ingest's is \"a note in an LLM-maintained wiki\". Disjoint, though neither names the other — the confusable pair is library-curator/kb-curator, not this one."
    },
    {
      "sibling": "library-curator",
      "query": "(b) \"ingest a source into the knowledge base\"",
      "picked": "llm-wiki-ingest",
      "why": "library-curator says \"rather than to add new ones\" — it self-excludes from any add path."
    }
  ],
  "symptom_words": [
    "add this to the knowledge base",
    "ingest this source",
    "put this in the wiki",
    "update the note",
    "this contradicts the note",
    "a fetched page, paper, repo, transcript or measurement",
    "is about to become a note",
    "knowledge base",
    "wiki"
  ],
  "solution_words": [
    "Raw kept",
    "triage new/update/disputed/no material",
    "quote before write",
    "claim verdicts",
    "neighbours name it back",
    "index and log rows",
    "lint",
    "Karpathy LLM Wiki: raw, notes, schema",
    "one source, one shape"
  ],
  "verdict": "pass",
  "reasons": [
    "650 characters (line 3 is 666 bytes including the 'description: \"' wrapper) — comfortably under the 1024 cap.",
    "Trigger clause leads with the user-typed phrasings verbatim: 'add this to the knowledge base, ingest this source, put this in the wiki, update the note, this contradicts the note'. A router matching a raw request has literal strings to hit; it does not require the user to know the method.",
    "The solution vocabulary ('quote before write', 'neighbours name it back', 'triage new/update/disputed', 'lint') sits in a second sentence AFTER the triggers, where it discriminates against siblings rather than gating entry. That is the right order; it would be a red only if it were the sole entry path.",
    "Boundary section is explicit and mostly reciprocal: skill-knowledge, unified-memory, doc-claim-reconciliation, kb-curator are each named with the job they own. kb-curator names back; the pairing is symmetric.",
    "deep-reading DOES claim wiki ingestion — 'or ingested into the knowledge base' sits in its own trigger clause. llm-wiki-ingest should own it: it names the artefact ('a note', 'raw, notes, schema'), the procedure (quote, verdict, neighbours, index, log, lint), the non-text inputs deep-reading cannot take (repo, transcript, measurement), and the literal user phrasings. deep-reading's clause carries no procedure and no artefact — it is a destination mentioned in passing, and its real subject stays 'a long text ... summarized, digested'.",
    "FIX (does not block pass, but the collision is one-way): deep-reading's description should drop 'or ingested into the knowledge base' or amend it to '(ingesting into a wiki: llm-wiki-ingest)'. As written, a query like 'read this paper and add it to the KB' matches both, and only one side of the pair declares the boundary. This is an edit to deep-reading, not to the skill under review.",
    "Softest remaining edge is unified-memory: both promise durability across sessions and both are reachable from 'record this so we don't lose it'. Separation currently rests on the reader recognising 'wiki'/'note' vs 'memory vault'. Acceptable, since a request with no wiki named genuinely belongs to unified-memory."
  ]
}
```

Two things worth pulling out of that JSON: the description is 650 chars, well inside the cap, and it leads with typed symptoms before method vocabulary, so it passes. The one real defect is not in this file — `deep-reading` claims "or ingested into the knowledge base" in its own triggers and names no boundary back, so that phrase is where a mis-route would come from. `llm-wiki-ingest` should own the job and `deep-reading`'s description should shed the clause.