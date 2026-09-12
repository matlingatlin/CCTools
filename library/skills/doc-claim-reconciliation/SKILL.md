---
name: doc-claim-reconciliation
description: "Use when code that already landed made a document FALSE — a merged PR, release, or refactor renamed a path, endpoint, flag, env var, or command, changed a default or threshold, or removed a capability, while README, on-call runbooks, ADRs, API references, or --help text still assert the old behaviour. Triggers on 'update the docs after this merge', 'what docs did this break', 'the runbook is wrong', 'docs say X but the code does Y', post-ship doc sync, docs-later debt. From the merged diff, finds every doc asserting the old value behind a positive control (phrasing, file types, excluded paths, generated vs prose, formats/surfaces grep cannot read), and gates completion per claim. NOT regenerating GENERATED architecture maps from code structure (update-codemaps). NOT cutting lines an always-on steering file has not EARNED (steering-doc-pruning — unearned is not false). NOT running commands to prove your own work passes (verification-before-completion — the WORK, not the docs about it)."
---
# Doc Claim Reconciliation

A merged change does not only add behaviour — it makes sentences **false**. Falsity is silent:
nothing fails, no test goes red, and the wrong document keeps being obeyed until someone follows
it under pressure. This talent takes a landed diff, extracts the falsifiable claims it changed,
finds every document still asserting the old value, and refuses to call the work done until each
one has a disposition.

**The unit is a (claim × document) pair, not a document.** A file can be half-reconciled — the
renamed path fixed, the changed default left standing — and a per-file checklist marks it done.

**Not this talent:** regenerating GENERATED architecture maps from code structure →
`update-codemaps` (that rebuilds a derived artifact; this hunts prose assertions). Cutting lines
an always-on steering file has not EARNED → `steering-doc-pruning` (unearned ≠ false; a
load-bearing line can be false and a useless line can be true). Proving your own work passes →
`verification-before-completion` (that gate is satisfied by a green run while every doc about the
change stays wrong).

## The ledger (one artifact, appended by every step)

Create `.reports/doc-claims/<merge-ref>.md` **before step 1**. Each step appends its own fenced
block containing the exact command run and a count — **including zero**. A block that is absent
means the step never ran; a block reading `0` means it ran and found nothing. Never report a
result that is not in the ledger, and never let a step's success and its non-execution look alike.

The ledger quotes old values, so on a later pass **it matches your own searches** — and on an
already-reconciled repo it becomes the *only* hit, which reads as a stale doc forever. The
exclusion is therefore part of every command, not a resolution: carry
`--glob '!.reports/**' --glob '!.git/**'` (written `$X` below) in **every** search here,
control re-runs included. **Tripwire:** if the ledger or a `.git/` path appears in any result,
the command lost its exclusion — fix the command and re-run. Do not classify it.

## Step 1 — Extract the claims (`## claims` block)

Walk every hunk of the merged diff. A **claim** is falsifiable: a value a reader could check.

| Claim kind | Record as |
|---|---|
| path / route / URL / topic | `old → new` |
| identifier, command, flag, env var | `old → new` |
| default, threshold, limit, timeout | `old → new` |
| order of steps, precondition | `old → new` |
| capability removed | `old → REMOVED` |
| exit code, error string | `old → new` |

**Reconcile the walk against a mechanical count before trusting it** — a hunk you never opened
yields no claim, and every later step then reports clean. Print `git diff <ref>~1 <ref> --numstat`
and `git diff <ref>~1 <ref> | grep -c '^@@'`, record both numbers, and give **every changed file**
a row: a claim row or a `no claim` row with the reason. A file with no row is invisible; a count
that disagrees with the command is a walk that skipped something. Silence is not a finding.

Each row gets an id and — in the same row — its **search terms: the old literal AND at least two
paraphrases a human would have written** (`3` → `three`, `three times`, `third attempt`, "retries";
`/auth/callback` → "auth callback", "callback endpoint", "redirect URI").

## Step 2 — Locate the stale documents, behind a POSITIVE CONTROL (`## search` block)

Run the search per claim, then **prove the search works before you trust any empty result.** A
grep that misses a phrasing emits a report byte-identical to a genuinely reconciled repo.

Five ways a doc search silently under-reports. Each needs its own control — one control does not
cover another's failure mode. Every control names a file **and** the command that returned it.

| Dim | Failure | Control |
|---|---|---|
| **D1 phrasing** | Doc states the fact in words, not the literal token | A hit on a doc you read BY EYE, **which the LITERAL run did not return**. See the anchor rule below |
| **D2 file type** | Glob was `*.md`; the claim also lives in `.mdx/.rst/.txt/.adoc/.ipynb`, OpenAPI/JSON schema `description`, docstrings, `--help` text, `.env.example`, alert/dashboard definitions | A hit outside `.md` — one stating the NEW value still passes, this tests REACH not staleness. `n/a` only with the command showing no non-`.md` doc file exists |
| **D3 path** | Default search skips hidden and ignored paths (`rg` does), `.github/`, `docs/archive/`, vendored/submodule docs, or `--maxdepth` cut it off | Re-run with `rg -uu` **plus `$X`**, diff the FILE LISTS, name a DOCUMENT the wide run added, and use that run. Without `$X` this self-passes: `-uu` enters `.git/`, where a rename's old value sits in the reflog by construction, so the lists always differ and prove nothing. Identical lists → `n/a` **with both commands** |
| **D4 generated vs prose** | A generated artifact hand-edited is overwritten on next build and the staleness returns | A hit classified `generated` (freshness header, `AUTO-GENERATED`, build output path). With no such hit, `n/a` needs the command **enumerating the generated artifacts** and proof the search reached them — "the search returned none" is the empty result this control exists to distrust |
| **D5 unsearchable channel** | The claim sits where no matcher can read it: undecodable bytes (PDF, `.docx`, `.pptx`, images, diagram exports), a non-English locale, or a surface outside the repo (wiki, Confluence, help centre, in-product copy). D1–D4 ask WHERE you searched; this asks whether the file was searchable at all — `rg` on a PDF exits 1 in silence | List every doc-shaped file the matcher skipped or could not decode (`find` by extension for the binaries; `file(1)` for the rest), plus every doc surface not in this repo. Each is extracted and searched, or recorded `UNSEARCHED` with an owner — never absent |

**Establishing the D1 anchor.** Read by eye the two or three documents a reader of this subsystem
would reach for (README, the ops doc, the relevant ADR). **The anchor must be a statement the
LITERAL run did not return.** A doc spelling the old token out is not an anchor: confirming a hit
on it passes the control while testing nothing — the exact failure D1 exists to catch. If
everything you read states the fact literally, or nothing states it at all, **seed** — write a
paraphrase in the stale doc's voice **before looking at your term list** (else you test the regex
against its own author), append it to a scratch file inside the search scope, confirm the search
returns it, delete it, and record the seed, the command, and a clean `git status`. Seeding is not
a last resort: on a reconciled repo it is the only route that passes D1, and this method writes to
the repo from step 0 anyway. An anchor not returned means the search is broken — widen and re-run
everything.

**Verdict words are not interchangeable:**
- Every control passed or is `n/a` on its stated evidence, **and** no surviving hit asserts the
  old value → `CLEAN`. Zero raw hits is not required and usually will not happen: the mandated
  paraphrases are value-agnostic, so on a healthy repo they return the docs that were correctly
  updated. `CLEAN` means nothing stale survived, never that grep was quiet.
- Any control failed, absent, asserted without a named file and command, or any `UNSEARCHED`
  surface → `UNKNOWN`. Not clean.

Reporting `UNKNOWN` as `CLEAN` is the defect this step exists to prevent. Its mirror costs as much
and is what an over-eager agent does to a healthy repo: treating a hit as a finding without
reading whether it states the old value, and "fixing" a true sentence.

## Step 3 — Give every hit a disposition (`## dispositions` block)

**Read the matched line before classifying the file.** Two filters run first, in order, each row
quoting the line so an outsider can check the call:

1. **Not stale** — the text states the NEW value, or is conditional, or is about another system.
   Row: `not-stale` + the quoted line. Not optional, and the common case on a healthy repo: the
   paraphrases match "does not retry by default" as readily as "retries three times". Every
   doc-class row below is a licence to EDIT; sending a true sentence into one is how this method
   breaks a correct repo.
2. **Not an assertion** — source code and tests (they hold the new value or the implementation,
   not a statement about it), VCS internals. Row: `out-of-scope` + a count.

Both are counted, never dropped, never edited. The ledger and `.git/` should never reach this
step; if they do, see the tripwire.

**The binding outcome: a reader who arrives at that document, at that location, can no longer be
led to the old behaviour.** Judge the outcome, not the edit. Deleting the sentence, moving it to
an appendix, archiving the page, adding a banner, or redirecting to a new doc satisfy the rule
only if that outcome holds — a runbook reduced to a stub fails it, its reader now has no
procedure. Filing a ticket never satisfies it: nothing at the document changed.

**Those verbs are available only where the row below allows them.** A protected record is
protected against every verb reaching the same outcome, not the one verb named — delete, archive,
move, stub, summarize away, redirect the reader past it, "it's still in git history" — all are
the same act as rewriting it.

| Doc class | Disposition |
|---|---|
| Prose reference (README, guide, help text) | `corrected` — fix in place |
| **Immutable historical record** (ADR, changelog entry, release note, RFC, postmortem, minutes) | `superseded` — **do not rewrite, delete, archive or move the record.** Write a NEW record stating the new decision, and touch only the old one's status line to `Superseded by <id>`. The body stays as written; a record edited to match today is no longer evidence of what was decided. |
| Generated artifact | `regenerated` — fix the generator or its source, re-run it, commit the output. Hand-editing here is a defect. |
| **Owner-gated** (on-call runbook, customer-facing doc, security policy, another team's doc) | `proposed` — write the exact diff and reason into the ledger, name the owner, **send it to that owner by a channel they read**, and stop; never land the body change unilaterally. **This is the one disposition that leaves the binding outcome UNMET** — the reader still arrives at the old behaviour — so the row also records the residual risk and the smallest mitigation available without the owner (usually a dated banner naming the new value, not a body rewrite). A proposal filed in the ledger and nowhere else is the ticket the table below rejects. |
| Genuinely fine | `no-change` — **with the reason** (already conditional, explicitly historical, different system) |
| Matched but true | `not-stale` — the quoted line, not edited |
| Source code, tests, VCS internals | `out-of-scope` — counted, not edited |

Superseding an ADR and gating a runbook are both human-gated *outcomes*: an unreviewed rewrite of
either is not reconciliation, it is a second silent falsehood.

## Step 4 — Completion gate (`## verdict` block)

You may claim reconciliation only by quoting the ledger's counts. Refuse if any holds:
- a claim has no `CLEAN` verdict and no disposition row;
- any row is `UNKNOWN`, or a control is recorded without a named file and command;
- a `proposed` row has no owner, no diff, or no evidence it reached the owner — and while any
  `proposed` row is unaccepted the verdict is NOT DONE, however complete the rest is;
- a `regenerated` row has no re-run output;
- any surface is `UNSEARCHED` (D5), or any hit carries a disposition without a quoted line.

If controls failed, the honest report is **"search unreliable — N claims unverified"**, never
"docs are clean".

| Rationalization | Reality |
|---|---|
| "grep found nothing, docs are fine" | A miss and a clean repo produce the same output. Run the control. |
| "grep found things, so the docs are stale" | Read the line. On a reconciled repo the paraphrases return the docs that were correctly updated. |
| "I updated the file I touched" | The dangerous doc is the one you did not touch. |
| "The ADR is historical, leave it" | Correct not to edit it — and it still needs a superseding record and a status line. |
| "I'll file a ticket for the runbook" | A ticket does not stop the 3am reader. Send the diff to the owner and put a banner on the doc. |
| "Docs later, ship now" | Later is the page at 3am. |

## Worked example (run, not imagined)

A merged PR renames `/auth/callback` → `/oauth2/callback` and flips `DEFAULT_RETRIES` 3 → 0. The
author updated README's path and nothing else. Fixture: README, an on-call runbook, ADR-0007, a
generated codemap, `api/openapi.yaml`, `.github/workflows/smoke.yml`.

```
rg -n $X --glob '*.md' '/auth/callback' .   → 1 hit  (the GENERATED codemap only)
rg -n $X '/auth/callback' .                 → +api/openapi.yaml        (D2)
rg -n $X -uu '/auth/callback' .             → +.github/workflows/...   (D3)
rg -ni $X -uu 'auth.?callback|callback (endpoint|url|path)|redirect.?uri' .
                                            → +docs/runbook-oncall.md  (D1)
rg -n $X --glob '*.md' 'retr(y|ies|ied).{0,20}3' . → 1 hit (README)
rg -ni $X -uu 'retr(y|ies|ied|ying)|three attempts|third attempt' .
                                            → +runbook, +ADR-0007, +openapi (D1)
```

The naive first line returns one hit, all of it generated, and **never returns the runbook** —
which says "the auth callback endpoint" and "retries three times", with no literal token to
match. Fixing that hit by hand is wrong twice over: it is generated, so the edit is overwritten
on the next build. `src/auth.ts` came back holding the NEW value — `out-of-scope`, and a thing an
unwary agent would have "fixed".

**The D1 trap, run and failed once.** README says "retried 3 times" — literally. Eye-reading
README and confirming the naive run returns it satisfies a D1 written as "any old-behaviour
statement you find", names a file and a command, and leaves the runbook undiscovered. Only the
anchor rule rejects README and forces the widening that finds the runbook.

Dispositions: README `corrected` (retry sentence — path already fixed, half-reconciled file),
runbook `proposed` to `@platform-oncall` (outcome UNMET, banner as interim), ADR-0007
`superseded` by a new ADR with a status line, codemap `regenerated`, `openapi.yaml` `regenerated`
or `corrected` per its source of truth, workflow comment `corrected`.

```
claims 2 | rows 7 | UNKNOWN 0 | corrected 2 | superseded 1 | regenerated 2
| proposed 1 (owner @platform-oncall, diff attached, sent) | no-change 1 (reason given)
| out-of-scope 1 (src/auth.ts)
controls: D1 PASS runbook-oncall.md · D2 PASS openapi.yaml · D3 PASS .github/workflows/smoke.yml
          · D4 PASS docs/CODEMAPS/backend.md · D5 PASS 0 undecodable, 0 external surfaces
GATE: NOT DONE — the runbook proposal is unaccepted.
```

**The same merge on a repo reconciled in the PR** separates this method from a grep. Every
literal run returns nothing; the mandated paraphrase runs return five docs, all stating the NEW
value; D1 has no eye-read anchor and passes by seeding; D4 is `n/a` against an enumeration of the
generated artifacts. Verdict `CLEAN` — reached by classifying five hits `not-stale` with their
lines quoted, not by a quiet grep. Every one of the five sits in a doc-class row saying "fix in
place".

## In this repo (one instance)

Ledger under `.reports/doc-claims/`; ADRs in `docs/decisions/` (template `0000-adr-template.md`,
status line `Superseded by NNNN`); generated maps in `docs/CODEMAPS/` carry a `Generated:` header
and belong to `update-codemaps`. Paths are examples, not requirements.

## Source

Method built from first principles. `garrytan/gstack` `/document-release` (read in full,
`document-release/SKILL.md` + `sections/release-body.md`) supports three parts: a diff-driven
post-ship audit of every doc file, an outcome-shaped human gate ("Only stop for:
risky/questionable doc changes… Never stop for: factual corrections clearly from the diff"), and
immutability of a historical record ("Never clobber CHANGELOG… Never delete, replace, or
regenerate entries." — added after a real incident). It does **not** support the rest: no claim
extraction, no ADR supersede rule, no ran-vs-never-ran artifact, no positive control — its own
discovery step is `find . -maxdepth 2 -name "*.md"`, the D2/D3 under-reporting failure this
talent exists to catch.
