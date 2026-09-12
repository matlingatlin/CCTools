---
name: deep-reading
description: Use when a long text needs to be summarized, digested, or ingested into the knowledge base — a document, research paper, spec, article, report, or pasted wall of text — especially when the request sounds simple ("summarize this", "what does this really say") but the source may hide contradictions or unverifiable claims. Also use when reading a large file for genuine understanding or when verifying claims against a source.
---

# Deep Reading

Produce verified understanding of a long text, captured as structured notes that
survive the session. The notes are the deliverable; writing them while reading is
what forces comprehension.

## Workflow

Copy this checklist and tick items off as you go:

```
Deep-read progress:
- [ ] 1. Secure the source as a file
- [ ] 2. Structure pass (outline)
- [ ] 3. Deep pass (notes per section)
- [ ] 4. Interrogation pass
- [ ] 5. Concept map
- [ ] 6. Self-test
- [ ] 7. Persist notes
```

**1. Secure the source.** Work from a file, never from pasted text: save pasted
content to a file first. Record source URL/origin and today's date. Estimate
size (prose ≈ words × 1.3 tokens; code ≈ chars / 4). Over ~15,000 tokens →
consider the fan-out variant below.

**2. Structure pass.** Read headings, abstract/intro, and conclusion only.
Write a one-screen outline: what the document is, its parts, and what each part
appears to claim.

**3. Deep pass.** Read section by section. For each section append to the notes
file:

```
## <section>
- Claims: <what it asserts, with location reference>
- Evidence: <what supports each claim>
- Relations: <which other sections this depends on or contradicts>
- Open questions: <what is unclear or unstated>
```

**4. Interrogation pass.** Write 3–7 questions about how the parts interact
(not recall questions — interaction questions: "how does X constrain Y?").
Answer each from the text with a location reference. Any question you cannot
answer → targeted re-read of the relevant sections, then update the notes.

**5. Concept map.** List the document's core entities and their relations as
`A —(relation)→ B` lines. Contradictions and tensions are relations too.

**6. Self-test.** Without looking at the source, write a summary from the notes
alone. Then verify it against the source. Every mismatch marks something not yet
understood: fix the notes, not just the summary.

**7. Persist.** Store the notes where the project keeps knowledge (in this repo:
`knowledge/notes/`, with frontmatter: source, date, status, tags). State claims
as `verified` / `unverified` / `outdated` — never inherit a source's confidence.

## Fan-out variant (very large documents)

Split by the structure pass's outline. Dispatch one subagent per part with: the
file path, its line range, and the section-notes template above. Then run passes
4–6 yourself across the merged notes — interrogation and self-test never
delegate.

## Scaling to the request

- Summary-framed requests ("summarize", "what does it say", "digest this") need
  the full workflow: without it, contradictions in the source get smoothed into
  a coherent story and unsourced claims get repeated as fact.
- Critique-framed requests ("review the assumptions", "find the flaws") already
  direct scrutiny at the text; passes 4–6 may confirm more than they discover.
  Never skip passes 1, 3, and 7 — location-referenced notes and persistence are
  the workflow's floor.

## Rules

- Every claim in the notes carries a location reference in the source.
- Separate what the document says from what you infer; label inferences.
- A source's citations are claims too: unverifiable citations → mark the claim
  `unverified`, don't drop it silently.
- If the text contradicts itself, record the contradiction; don't resolve it
  invisibly.
