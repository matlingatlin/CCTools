**Length:** the `description` value is **650 characters** (line 3 is 666 bytes including `description: `, the quotes, and the newline) — comfortably under 1024.

```json
{
  "collisions": [
    {
      "sibling": "deep-reading",
      "query": "ingest this paper into the knowledge base",
      "picked": "llm-wiki-ingest",
      "why": "REAL COLLISION. deep-reading claims 'or ingested into the knowledge base' verbatim — the exact phrase a person types — while our description claims 'about to become a note in an LLM-maintained wiki or knowledge base ... add this to the knowledge base, ingest this source, put this in the wiki'. For deep-reading's OWN job ('summarize this', 'what does this really say', 'reading a large file for genuine understanding') the router must pick deep-reading: those words are only in its description. For the write itself, llm-wiki-ingest wins on 'raw kept', 'triage new/update/disputed/no material', 'index and log rows', 'lint' — deep-reading names no wiki artefact, no schema, no index, no lint, so it cannot execute the ingest it advertises. The disclaimer is ONE-WAY: we say 'NOT summarising a text (deep-reading)'; deep-reading does not name us back. Fix belongs in deep-reading: drop 'or ingested into the knowledge base' and end its first clause at 'digested', then chain deep-reading (comprehend) -> llm-wiki-ingest (write the note)."
    },
    {
      "sibling": "skill-knowledge",
      "query": "gather and verify claims from a paper before bundling them into a skill",
      "picked": "skill-knowledge",
      "why": "Both quote-before-write and grade claims, so the discriminator is the DESTINATION, and both descriptions state it. skill-knowledge: 'before they are bundled into an artefact', 'whether a skill needs knowledge fetched from outside'. Ours: 'become a note in an LLM-maintained wiki or knowledge base', plus the explicit 'NOT claims for a skill bundle (skill-knowledge)'. For our job ('put this in the wiki', 'update the note') skill-knowledge has no wiki, index, or lint vocabulary at all. Two-way separation on the destination noun — no ambiguity."
    },
    {
      "sibling": "unified-memory",
      "query": "save this so the next agent can resume the task",
      "picked": "unified-memory",
      "why": "unified-memory owns 'durable work state', 'hand off or resume another agent's task', 'ECC Memory Vault'. Ours owns the artefact a human reads: 'note', 'wiki', 'Claims', 'index and log rows'. Our 'NOT agent memory (unified-memory)' names it back and unified-memory's 'not an in-task aside' keeps to state. Clean."
    },
    {
      "sibling": "memory-provenance-separation",
      "query": "grade this claim and stamp when it was checked",
      "picked": "memory-provenance-separation for a memory row, llm-wiki-ingest for a wiki claim row",
      "why": "NEAR-MISS on shared vocabulary: it says 'origin (asserted / observed / derived)', 'as-of date', 'staleness horizon'; we say 'claim verdicts' and the body's MEASURED/REPEATED/DERIVED with as-of dates. The words are almost the same taxonomy. What decides is the STORE each names: 'durable agent memory' / 'an agent citing memory' (theirs) vs 'a note in an LLM-maintained wiki or knowledge base' (ours). Our negative clause names unified-memory, not this sibling, so the separation rests entirely on the wiki/knowledge-base anchor in the first sentence — it holds, but it is the thinnest boundary in the set."
    },
    {
      "sibling": "doc-claim-reconciliation",
      "query": "this contradicts what we already wrote down",
      "picked": "depends on WHAT contradicts: llm-wiki-ingest for a fetched source, doc-claim-reconciliation for merged code",
      "why": "Our trigger phrase 'this contradicts the note' sits close to their 'docs say X but the code does Y'. The discriminator is stated on both sides: theirs opens 'Use when code that already landed made a document FALSE ... a merged PR, release, or refactor', ours opens 'a fetched page, paper, repo, transcript or measurement'. Source-driven vs diff-driven. We also carry 'NOT docs broken by code (doc-claim-reconciliation)'. Resolved."
    },
    {
      "sibling": "kb-curator (agent)",
      "query": "the knowledge base has dangling links and pages missing from the index",
      "picked": "kb-curator",
      "why": "Scope, and both descriptions state it. kb-curator: 'walk ... and fix what has rotted', 'Dispatch after a batch of ingests, before a release'. Ours is one source at a time and hands off explicitly: 'whole-wiki clean-up is the kb-curator agent'. kb-curator names us back ('NOT for ingesting a new source (llm-wiki-ingest)'). Best-separated pair in the set."
    },
    {
      "sibling": "library-curator",
      "query": "audit and improve the units already in the library",
      "picked": "library-curator",
      "why": "No real overlap. It governs 'a library of capabilities that is ALREADY in place (the tested/adopted tier)' — skills, not notes; ours governs pages in a wiki. Different object entirely; no disclaimer needed on either side."
    }
  ],
  "symptom_words": [
    "add this to the knowledge base",
    "ingest this source",
    "put this in the wiki",
    "update the note",
    "this contradicts the note",
    "a fetched page, paper, repo, transcript or measurement",
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
    "LLM-maintained"
  ],
  "verdict": "pass",
  "reasons": [
    "650 characters, under the 1024 cap, with room to spare.",
    "Structure is correct for a router: a symptom clause first (the five phrases a person actually types, in their words, including the two failure-shaped ones — 'update the note', 'this contradicts the note'), a mechanism clause second, negative triggers third. The solution vocabulary is real but it is quarantined in the mechanism clause where it disambiguates rather than gates.",
    "Four of five negative triggers are earned: skill-knowledge, unified-memory, doc-claim-reconciliation and kb-curator each contest a plausible query, and each is separated by a word present in both descriptions (destination, store, what contradicts, scope). Three of them name us back.",
    "deep-reading is the one unresolved collision and it CANNOT be closed from this side. Our description already disclaims it and already out-specifies it on every wiki artefact; deep-reading still asserts 'or ingested into the knowledge base' with nothing behind it. Ownership: llm-wiki-ingest, because it names the raw, the schema, the index row, the source-log row and the lint — deep-reading names none and would leave the wiki unwritten. Required neighbour edit: strike that clause from deep-reading and have it point here.",
    "memory-provenance-separation is a soft edge: near-identical claim-grading vocabulary, separated only by the wiki-vs-memory anchor and not by a negative trigger. Not a blocker — the anchor is in the first ten words — but it is the row to watch if either description drifts.",
    "'neighbours name it back' is opaque as a standalone phrase; it earns its place only because a reader has already been anchored by 'wiki'. Acceptable in the mechanism clause, would be a defect in the trigger clause."
  ]
}
```