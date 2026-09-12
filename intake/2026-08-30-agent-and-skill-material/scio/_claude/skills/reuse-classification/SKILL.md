---
name: reuse-classification
layer: D
phase: build-time
status: written
description: Classify and find reusable software parts without the library fragmenting into near-duplicates nobody can find. Use when working on the component library's categories, hashtags or contracts, when a proposed category name has to be judged, when deciding whether two entries are the same thing, or when explaining why contributed entries fail to match each other. Covers faceted classification, the vocabulary problem, and how to measure whether a reuse library is converging or scattering.
---

# reuse-classification

Scio's library splits identity across three mechanisms
(`library/categories.py`, `library/identity.py`):

- **category** — one canonical name per entry. *Narrows* the search. Never decides.
- **hashtags** — overlapping labels for a person browsing. Never a match key.
- **contract** — operations, routes and files with the project's own words removed. **Decides.**

That split was arrived at independently. It is also, almost exactly, a solved problem from
1991 — and the failure mode it does *not* yet handle was named in 1987. This skill supplies
both, and the measurement that tells you which one you are suffering from.

---

## 1 · Source

**Ruben Prieto-Díaz — *Implementing faceted classification for software reuse.***
Communications of the ACM 34(5), May 1991.
[ACM DL](https://dl.acm.org/doi/10.1145/103167.103176). Reports the development,
implementation and deployment of reuse-library technology built on faceted classification, after
his earlier *A software classification scheme* (1987).

**G. W. Furnas, T. K. Landauer, L. M. Gomez, S. T. Dumais — *The Vocabulary Problem in
Human-System Communication.*** Communications of the ACM 30(11), 1987. The finding: two people
spontaneously choose the same term for the same familiar thing **less than 20% of the time**.

---

## 2 · Method, in the form we use it

### 3.1 Facets, not a tree

Prieto-Díaz's argument against hierarchical classification is that reusable parts do not have
one home — the same part is *a booking thing*, *a form thing*, *a server-action thing*, and any
tree forces a choice that makes it unfindable along the other axes.

A **facet** is an independent axis with a controlled vocabulary. A part is classified once per
facet. Retrieval is a conjunction across facets, with a defined *distance* when nothing matches
exactly, so a query degrades to near-misses rather than to nothing.

Mapped onto what Scio already has:

| Prieto-Díaz | Scio | State |
|---|---|---|
| controlled vocabulary per facet | `CategoryRegistry` with aliases, growing only by proposal | **built** — `categories.py` |
| free-text terms, never a retrieval key | `hashtags` | **built**, and correctly excluded from matching |
| a *conceptual distance* between terms | — | **missing.** Match is binary; a near-miss is indistinguishable from no match |
| classification effort per part | automatic, from the build | **better than the paper's** — this is where 1991 libraries died |

The one facet Scio has is `category`. The gap is not more facets, it is the **distance**: the
paper's libraries could say *"nothing exact, here are three at distance 1"*, and ours cannot.
That is the near-miss ledger, in 1991 vocabulary.

### 3.2 The vocabulary problem is our recall cost, named

`Contract.of` generalises by substituting every spelling of the entity (`identity.py:100`,
`:116`). It is exact and it works — `bookings` and `appointments` produce the same contract.

It works **only for operations that contain the entity name**. A project that calls its
operations `reserve_table`, `confirm_slot` or `hold_seat` keeps its own vocabulary in its
contract and can never equal another project's, because there is no shared word to blank out.

Furnas et al. predict exactly this and give it a magnitude: unaided, people agree on a term
under 20% of the time. Their proposed remedy — **unlimited aliasing**, many surface terms
mapping to one referent — is precisely what `CategoryRegistry.aliases` does for categories and
what nothing does for operations.

So the design question this skill exists to frame: **operations are the one facet with no
controlled vocabulary.** Either they get aliases the way categories did, or the miss rate is
accepted — but it has to be measured before it is accepted.

### 3.3 The measurement: convergence or scatter

A reuse library either converges (later builds keep hitting the same contracts) or scatters
(every build invents a new one). Prieto-Díaz's libraries scattered; the cost of classifying by
hand was what killed them. Ours classifies for free, so the failure mode moves to the key.

Four numbers, all computable from data that already flows through `library/`:

| Number | How | Reads as |
|---|---|---|
| **contract keys per category, over builds** | count distinct `Contract.key` per category | flat-ish = converging. Linear in builds = scattering |
| **vocabulary-miss rate** | fraction of `package_operations` containing no `entity_forms` match | Furnas's number, in our data |
| **near-miss distance** | `|contract.operations − entry.operations|`, `|routes|`, `|files|` per considered entry | which facet is doing the damage |
| **reuse depth** | assemblies per entry | Prieto-Díaz's own success measure. A library with a long unmatched tail is a scrapyard with a search box |

**Interpretation rule, and it is the point of the whole skill:** a rising key count with a *low*
vocabulary-miss rate means the **contract is too fine-grained** — the fix is structural (see
`docs/next/LAYER-D-LIBRARY.md` §2.1, route-parametric entries). A rising key count with a *high*
vocabulary-miss rate means the **naming is unaliased** — the fix is a controlled vocabulary for
operations. These need opposite work, and without both numbers you cannot tell them apart.

---

## 3 · Limits — what the papers show versus what we are assuming

- **Prieto-Díaz's libraries were classified by people.** His central cost — the classifier's
  time and the classifier's disagreement — barely applies to us. What transfers is the
  *taxonomy* and its failure modes, not the economics.
- **The paper reports deployment experience, not a controlled comparison.** There is no measured
  effect size to quote, and any claim that facets "improve retrieval by X" would be invented.
- **Furnas et al. measured people naming everyday objects and commands**, not developers naming
  operations in code. Code naming is more conventional than natural language — `create_*`,
  `list_*` — so the true agreement rate here is plausibly *better* than 20%. **We do not know by
  how much, and the skill must not imply the 20% figure is ours.** Measuring it is the whole
  point of §2.3.
- **The four numbers are proposals, not an implemented harness.** Nothing in the repo computes
  any of them as of 2026-08-26.
- **Unlimited aliasing has a cost the 1987 paper is honest about**: more aliases means more false
  hits. In our system a false hit is bounded — the contract still has to be satisfied exactly —
  so we can afford more aliasing than they could. That is a genuine asymmetry in our favour and
  it should be stated when the operation-alias proposal is argued.

---

## 4 · Eval

| # | Case | Expected |
|---|---|---|
| 1 | `bookings` (entity `booking`) vs `appointments` (entity `appointment`), same operations | identical `Contract.key`. Regression guard on `entity_forms` |
| 2 | `reserve_table` / `release_table` with entity `booking` | contract retains `reserve_table` — **the miss is visible, not hidden.** Any change that makes this silently match is wrong |
| 3 | Category `logins` proposed by the relay | resolves to `auth` through the registry, does not create a category (`suggest_labels`, `generalize.py`) |
| 4 | A category nothing resolves | recorded as *proposed*, unconfirmed, matched by nothing |
| 5 | Two entries differing only in hashtags | same contract key; hashtags never affect the match |
| 6 | 20 synthetic builds across 4 app kinds | report the four §2.3 numbers. **No expected value — this case exists to produce the baseline**, and the first run of it is the answer to `LAYER-D-LIBRARY.md` §4.4 |

Case 2 is the one that matters. The temptation, once the miss rate is known, is to make the
generalisation cleverer until the miss disappears. That trades a *visible* miss for an
*invisible* wrong match, which is the trade `library/matcher.py:1` exists to refuse.
