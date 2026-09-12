# Can a stdlib-only extractor read our held PDFs? — preregistered 2026-09-11

**Written before any extractor existed.** The environment has no PDF toolchain (all five
poppler tools absent, `pypdf` installed but panicking on a missing `_cffi_backend`), and
installing one is the fourth gate's business. But `zlib` is stdlib and PDF content streams are
usually FlateDecode, so an extractor that never leaves the standard library may be possible.
If it is, it unblocks the verification path for four notes at zero install cost; if it is not,
that is a fact worth having, because it turns "nobody tried" into "tried and measured".

## The metric, fixed now

The base quotes this guide. The test is therefore not "does text come out" — garbled text also
comes out — but **can a claim the base rests on be verified against the extraction.**

**PASS** = the extractor recovers, from
`knowledge/raw/pdf-sources-2026-09-11/resources.anthropic.com_hubfs_The-Complete-Guide-to-Building-Skill-for-Claude.pdf`,
the verbatim string that `knowledge/notes/skill-anatomy.md` attributes to it:

> does not execute automated test suites or produce quantitative evaluation results

matched after whitespace normalisation only — no fuzzy matching, no edit distance, no
hand-repair of the output. A quote the base already claims is in the document is the strictest
available oracle and needs no new ground truth.

**FAIL** = anything else, including text that is clearly the right passage but mis-encoded.
Mis-encoded text is worse than none: it reads as evidence and is not.

## The three constraints

1. **Standard library only.** The moment it needs a wheel, the fourth gate applies and the whole
   reason for trying is gone.
2. **Read-only, and the raw layer is never edited.** The extractor may open a held PDF; it may
   never write one.
3. **A negative result ships too.** If it fails, the failure and its cause are recorded and the
   PDF-toolchain question goes to the human with one more measurement attached — not silently
   dropped because it did not work.

## Stop rule

One implementation attempt, extended only for causes *diagnosed from the file's own structure*
(a filter this PDF actually uses, an operator it actually contains). If the diagnosis is "the
fonts carry custom encodings", that is a FAIL and not a next iteration: rebuilding CMap handling
is writing a PDF library, which is exactly the dependency this was trying to avoid.

## Outcome — FAIL, on the cause the stop rule named in advance

Written before the result was used for anything.

The extractor was built (stdlib only: `re` + `zlib`), run against the held guide, and the
preregistered string was **not recovered**. Every component phrase of it is present —
`automated test suites`, `quantitative`, `evaluation` all appear — but the sentence's opening
words are missing, so the quote cannot be matched and the claim cannot be verified. **FAIL.**

The cause, measured rather than guessed:

| | |
|---|---|
| streams | 125, of which 123 FlateDecode cleanly — decompression is not the problem |
| pages | 33, as the note says |
| text bytes inside showing operators | 10,618 literal `(...)` · **48,498 hex `<....>`** |
| **recoverable without a ToUnicode CMap** | **17.6% of bytes · 30.5% of characters** |
| fonts | `C2_0`…`C2_4` (CID, hex-coded) outnumber `TT0`…`TT8` in `Tf` count |

**The extractor is not the weak part.** It recovers essentially *all* of what a literal-string
reader can reach; the remainder is CID text whose codes mean nothing without the 25 `/ToUnicode`
CMaps the file carries, and parsing those is writing a PDF library — **the exact condition the
stop rule declared a FAIL rather than a next iteration.** The rule is honoured: no further attempt.

*Two numbers, because the unit is not obvious and the first one written down was wrong.* An
interim hand-diagnostic said 25.4%; the shipped tool says 17.6%, and the tool is right — its
operator set also catches bare `<hex> Tj` runs, which the throwaway pattern missed, so it finds
more hex than the first pass did. And bytes are not characters: these are 2-byte Identity/
CIDFontType2 codes, so the same document is 30.5% decodable counted in characters. The tool
reports the **byte** ratio because it is the lower of the two, and a guard's errors should fall
on refusing a document it could have read, never on passing one it could not. Every reading —
17.6%, 25.4%, 30.5% — is a FAIL, which is why the verdict never depended on settling this; but a
measurement is a measurement, and the wrong one does not get to stand because the conclusion held.

**The result the rule was designed to protect against.** The output reads like clean English.
`"...automated test suites or produce quantitative evaluation results."` is a grammatical
sentence and a *fragment*, and nothing in the text marks where the missing 74.6% was. A quote
check against it yields a false negative; a human skimming it would not notice. This is the
"mis-encoded text is worse than none" clause, and it arrived exactly as anticipated — which is
the argument for having written the clause down before seeing any output.

## What ships from a failed rule — including a capability the rule's own document hid

Three things, all real.

**The sources are held.** `knowledge/raw/pdf-sources-2026-09-11/` now carries all three PDFs
(2.0 MB on disk). Four notes cited PDF sources and **not one was held as raw** — they were read
2026-08-29, before the raw layer existed, and nothing was kept. That was true regardless of how
this experiment turned out.

**The extractor ships with a guard.** `knowledge/pdftext.py`, stdlib only, 25 fixtures and 12
mutations with no survivors. It never returns text without the decodable fraction, and it refuses
below a floor, so it cannot hand back a plausible fragment as if it were a document.

**And the capability is real — the chosen document was the unreadable one.** Run over all three
held PDFs:

| document | verdict |
|---|---|
| Anthropic, *The Complete Guide to Building Skills* | **REFUSED**, 17.6% |
| Basili, `J81.pdf` (cited by `requirements-discovery`) | **READABLE, 100.0%** |
| Kim et al. 2014, `kim-tse-2014.pdf` (same note) | **READABLE, 100.0%** |

So the honest verdict is not "stdlib cannot read PDFs here". It is **"stdlib reads two of our
three held PDFs completely, and the third not at all"** — a designer's choice of font, made years
ago, decides it. The preregistered rule failed because it named the single document in the set
that is CID-encoded, and it named that one *because* it was the most-cited. Worth keeping as a
lesson about rule design: **picking the highest-value instance as the test case conflates "can
this be done" with "can this be done on the hardest case", and only the second was answered.**
The first, unasked, had a better answer than anyone expected.


## Postscript, same day — the guard was measuring the wrong thing, twice

The tool shipped, and using it immediately found two defects that its own coverage number was
structurally unable to see. Both are fixed; both are worth recording, because the pattern is the
same one the guard was built against, reappearing one level up.

**1. No word spaces.** The Kim et al. paper reported **100.0% coverage** and came out with **one
space in 74,422 letters** — an unbroken run of letters, useless for quoting. A PDF draws most word
gaps as *kerning numbers* inside a `TJ` array, not as space characters, and the first version
discarded them. Coverage could never have caught this: every byte it counted *was* decoded. Fixed
by treating a kern of `-140` thousandths of an em or wider as a space; the same file now reads
12,520 spaces, 0.168 per letter, against ~0.19 for English prose. A `fidelity()` check now reports
a space ratio below 0.02 and the verdict becomes **SUSPECT** rather than READABLE.

**2. Ligatures drop silently, and this is NOT fixed — the claim changed instead.** `fi`, `fl` and
`ff` are single glyphs mapped through a font's `/Differences` encoding, which this tool does not
read. In the Kim paper: **41 occurrences of "bene" and zero of "benefit".** A statistical detector
was considered (f-ligature bigrams run 1.37 per 1,000 letters there against 5.81 in this repo's own
prose) and **rejected** — that is an unvalidated threshold on a fuzzy signal, and this repo does not
ship those. So the *verdict text* changed instead: READABLE no longer says "whole enough to quote
from", it says ligatures and symbols can drop silently and quotes must be matched loosely. A fixture
asserts that wording, so the promise cannot quietly return.

**3. The wiring was untested while the predicates were tested.** A mutation that unhooked
`fidelity()` from the verdict inside `main()` survived the entire suite. The decision path is now a
`report()` function with three end-to-end fixtures over real PDF bytes. 40 fixtures, 12 mutations,
no survivors.

**The lesson this makes concrete.** A guard is only as honest as the quantity it measures, and
"how much decoded" is not "is this usable". Both defects passed the guard at 100%. What caught them
was *using the output for its actual purpose* within minutes of shipping — which is the argument for
having a real first task lined up behind a new tool, rather than a green test suite and a commit.


## Second postscript — two more defects, and a number that moved in nine files

Running the reader over five more cited papers (arXiv) found two further defects of the same
family as the first: the tool was **scanning streams that are not page content at all.**

**4. It scanned images, then it scanned fonts.** A PDF Flate-compresses raster images, embedded
font programs, metadata and attachments with the *same filter* as page content, and the first
version decompressed and regex-scanned all of them. On arXiv 2106.09482 that meant running the
text-operator scan across 302 KB of pixel bytes: **over 90 seconds, versus 0.03 s once skipped.**
Worse than slow — any byte run that happened to resemble `(...)Tj` inside an image would have been
counted as literal text and *inflated the coverage figure with pixels*.

Filtering images by their dictionary fixed that file, and arXiv 2605.17193 still hung — on an
embedded **OpenType font program** (GDEF/GPOS/GSUB tables), which is not an image and carried no
marker the tool knew. That is the lesson: **a list of stream types to exclude is always
incomplete**, because it can only name the ones someone thought of. The fix asks the *bytes*
instead — page content is operators and numbers, overwhelmingly printable ASCII; a binary blob is
not — which rejects every wrong stream type including ones not invented yet. A fixture feeds it
that exact font header with no dictionary hint at all, and asserts it is both skipped and fast.

**5. And the headline number moved: 18.0% → 17.6%.** Excluding non-content streams removed text
bytes that had been counted, so the guide's coverage fell slightly. The verdict is unchanged —
REFUSED under every reading — but the figure was already written into **nine files**: this
document, BRAIN, CURATION-LESSONS, four notes, `watch.py`'s NEVER_WATCHED reasoning and the CI
workflow's comment. All nine are reconciled.

That spread is worth naming, because this repo has a talent for exactly it —
`doc-claim-reconciliation`, "after a diff merges, find every doc still asserting the OLD behaviour"
— and the situation that produced it was self-inflicted: **a measured number was quoted as a
constant in nine places within three hours of first being measured, while the thing measuring it
was still being fixed.** A number from a tool under active repair is not yet a fact to cite. The
honest pattern is to quote it in the one document that owns the measurement and point at that
document from everywhere else.

Final state of the reader: **52 fixtures, 7 mutation rounds with no survivors**, and eight held
PDFs measured — five readable at 100.0%, three refused (0.0%, 0.0%, 17.6%).

## Third postscript, 2026-09-12 — the blocker was a POISONED DEPENDENCY, not a missing toolchain

**The preregistered rule above still FAILS and its verdict is unchanged.** It asked whether a
*stdlib-only* extractor could verify the quote; it cannot, and 17.6% stands. What follows is a
different instrument answering a different question, recorded here because it retires the blocker this
document created.

**Measured.** The system `pypdf` is **6.17.0** — not old, and not the problem. It panics because the
*system* `cryptography` 41.0.7 reaches a Rust binding needing an absent `_cffi_backend`. In a clean
virtualenv with no poisoned site-packages to reach for, **`pypdf` 6.18.1 imports fine** and reads the
held guide: **33 pages, 35,765 characters**, and the preregistered string is present **verbatim** —
*"skill-creator helps you design and refine skills but does not execute automated test suites or
produce quantitative evaluation results."*

**So the PDF question was never "install a toolchain".** It was one broken dependency in one
site-packages, and a venv sidesteps it. That is a far smaller decision than the one standing for the
human, and it reframes it again: from *restore a capability we lost* to *stop reaching into a
site-packages that is already broken*. `graphifyy[pdf]` turns out to be exactly `pypdf>=6.12.0` plus
`markdownify` — nothing exotic.

**Nothing was installed system-wide.** The measurement ran in a scratch venv outside the repo.
Whether this becomes part of the repo's tooling is still the human's call; that it *works* is now a
fact rather than a hope.

**What it immediately paid for.** The `skill-anatomy` internal contradiction — the last item the
review doc listed as BLOCKED — is resolved: the guide's `/CreationDate` is **2026-01-26**, `pass_rate`
appears **0 times** in it, and the tool's metrics were read **2026-08-30**. The sentence is **stale,
not false**, and only the file's own date could have told them apart.

### Positive control, 2026-09-12 — the version was not the variable either

The postscript above named the poisoned system `cryptography` as the cause and demonstrated it
with `pypdf` **6.18.1** in a virtualenv. That left one confound: the system copy is **6.17.0**, so
a reader could conclude the fix was the version bump.

It was not. A second isolated virtualenv holding **6.17.0 — the same version the system carries —**
imports fine and reads the held guide identically:

| interpreter | `pypdf` | pages | chars | preregistered quote present |
|---|---|---|---|---|
| system `python3` | 6.17.0 | — | — | `PanicException` on import |
| venv A (isolated) | **6.17.0** | 33 | 35,733 | **yes, verbatim** |
| venv B (isolated) | 6.18.1 | 33 | 35,733 | **yes, verbatim** |

Same version, two outcomes, and the only variable is whether `site-packages` can reach the broken
`cryptography`. `include-system-site-packages = false` is the whole fix. This is what the first
postscript's lesson asks for and did not have: **a control that isolates the claimed cause.**

**And a number in the postscript above needs its unit.** It says 35,765 characters; the table here
says 35,733. Both are right, and the difference is 32 — one separator per page boundary, 33 pages.
Concatenating `extract_text()` gives 35,733; joining with a newline gives 35,765. Nothing depended
on it, which is exactly why it went unstated — the same shape as the 17.6% / 25.4% / 30.5%
byte-versus-character episode earlier in this document, and the second time in two days that a
figure from this one file needed its convention named before it could be compared.

**Neither of these changes the preregistered verdict.** The rule asked whether a *stdlib-only*
extractor could verify the quote. It cannot, 17.6% stands, and `pdftext.py` remains what CI runs,
because it needs no virtualenv and no wheel. What the control retires is the last reading under
which the environment looked short of a capability it has had all along.

### The ligature failure has a worse cousin, found 2026-09-12 in the same guide

Defect 2 above is that `fi`/`fl`/`ff` drop silently. Reading the same guide with `pypdf` found the
same *class* on a different glyph, with a consequence that is not merely lossy but **misleading**.

Inside the guide's fenced code blocks, `##` extracts as `-#` and `###` as `--#`. Consistently, at
every depth, in every template in the document. It is not a general failure to read hashes:
`# Your Skill Name`, `# Bad` and `# Good` come out correctly in the same blocks, and the prose
sentence `Use ## Important or ## Critical headers` extracts with both hashes intact. In a run of N
hashes the **last survives and the first N-1 become hyphens** — the signature of a
programming-ligature font, where the ligature is drawn as N-1 placeholder glyphs plus one composite
and the placeholders carry no useful `/ToUnicode` entry.

Why it is worse than a dropped `fi`: **a missing ligature reads as a typo, and a rewritten heading
level reads as valid markdown.** `-# Instructions` is not obviously broken; it is plausible text of
the wrong depth. Anyone copying a markdown template out of a PDF this way gets a document one
heading level flat with nothing to flag it. `pdftext.py` is not changed for this — the same
argument as defect 2 applies, a detector here would be an unvalidated threshold on a fuzzy signal —
but the artefact is recorded where the extraction measurements live, and at the page that quotes
the template.

**The general form, which is the part worth keeping:** an extraction defect that produces
*syntactically valid output in the target language* cannot be caught by a coverage number, a
fidelity ratio, or a reader's eye. It can only be caught by knowing what the source said. That is a
third instance of this document's standing lesson — coverage measured 100% for the missing spaces,
100% for the dropped ligatures, and would measure 100% here.

### And it is a tool now, 2026-09-12 — `knowledge/pdfread.py`

Three verification passes and one skill-surface measurement leaned on the isolated reader, and it
lived in `/tmp`. Nothing in this repo could reproduce a single one of them, which is the same defect
as citing a source the raw layer does not hold.

`knowledge/pdfread.py` builds it, and the thing worth stating is **how**: `python3 -m venv` makes an
empty isolated environment and the already-present system `pypdf` is **copied** into it. No network,
no package manager, no wheel — so the fourth gate has nothing to weigh, and the recipe works with
the network off. If it ever needs a download, it has stopped being this tool. `--report` reads all
nine held PDFs; the reader refuses any path outside `knowledge/raw/`, answered on the normalised
path so `knowledge/raw/../../etc/passwd` is not inside the layer merely because it starts with the
prefix.

`pdftext.py` is unchanged and is still the gate: it needs neither virtualenv nor filesystem work,
which is what CI can run. Two readers, two jobs — the stdlib one guards, the cloned one verifies.

**The mutation round found the security-relevant predicate had two clauses and neither was
load-bearing.** `under_raw` normalised the path *and* rejected any path containing `..`, and both
survived independently: each caught every fixture alone. Worked through rather than padded with a
test — after `normpath` a `..` can only remain when it is leading, and a leading `..` cannot start
with the prefix, so the second clause was **unreachable**; it was also wrong in the other
direction, rejecting `knowledge/raw/a/../x.pdf`, which resolves inside the layer. Deleted, with a
fixture for each direction. **A clause that cannot fire is not a defence, and one that rejects a
valid input is a bug wearing a defence's clothes** — and a mutation round is how you tell which of
the two you have. 10 fixtures, 5 mutations, no survivors.

