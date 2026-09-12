---
name: catalog-budget
layer: D
phase: build-time
status: written
description: Stop a catalog that every session loads from growing without limit. Use when a discovery surface is paid for on every request — skill descriptions, a component library's entries, a tool list, a registry index; when adding an entry to one; when a description will not fit; when someone proposes raising a budget or says an entry is "only a few more tokens"; or when asked how many entries there actually are. Covers an aggregate budget with a per-entry byte cap, a shrink floor beside the growth ceiling, a same-commit ratchet that stops a budget being raised quietly, the two-tier split that makes a byte cap survivable at all, and the single census that makes any of it countable.
---

# catalog-budget

A catalog that is loaded whole, every time, has a cost that grows with its usefulness. That
is the wrong gradient, and it is Layer D's today:

```sql
-- library/store.py:241 — every entry, full JSON, into memory, on every match
SELECT payload FROM library_entry WHERE status <> 'rejected'
```

called again per package at `builder/orchestrate.py:347`, so a seven-package build loads the
whole catalog seven times. At one matchable entry this is free. The mechanism that stops it
being expensive later is four numbers and one split, and gstack has all of them in tests.

**Route to what you need:**

| You are here because | Read |
|---|---|
| adding an entry, or a budget failed | §2 |
| a description will not fit the cap | §3 — and do not raise the cap |
| someone wants the budget raised | §2.3, the ratchet |
| you need to say how many entries exist | §4 |
| you are about to quote a number from here | §5 |

---

## 1 · Source

**gstack**, read at commit in `docs/mined/OTHERS-MINED.md` §1.4 and
`docs/mined/PASS2-GSTACK-TESTS.md` §1.1, §1.6, §2.5, §2.9. Five test files and one library:

- `test/catalog-budget.test.ts` — the aggregate budget, the per-entry cap, the non-empty floor
- `test/skill-size-budget.test.ts` — growth ceiling, corpus ceiling, **shrink floor**
- `test/catalog-trim.test.ts` — the two-tier split and its idempotency
- `test/cso-preserved.test.ts` — PRESERVATION and the ALWAYS-LOADED CONTRACT ordering rule
- `test/helpers/skill-census.ts` + `test/skill-census.test.ts` — one enumerator, three counts
- `lib/context-bill.ts` (1,017 lines) — the measurement instrument and its published error band

Not a paper. A working repository's tests, with their reasoning written in the failure
messages. That is the whole reason the numbers below are theirs and not ours (§5).

---

## 2 · The four instruments, and why one alone is not enough

### 2.1 An aggregate ceiling, on the surface that is always paid for

gstack's discovery surface is the sum, over every entry, of `byteLength(name) +
byteLength(description)` — what every host loads every session before anything is chosen.
Budget **1,150 token-equivalents**; measured 2026-08-12 at **4,420 bytes / 1,105 TE** over 53
skills plus a router alias. Headroom **180 bytes, ~4%**. The dominant entry is named in the
comment (`design-consultation`, 229 bytes).

Two properties of that measurement matter more than the number:

- **It is measured against the committed tree, not the live one.** Their sibling budget test
  says why: parallel workers regenerate files mid-run, and the live estimate read *"4177 solo,
  8356 and 8041 in two parallel runs."* A budget measured against a tree that is being written
  is not a measurement.
- **The test is import-free by design** — *"this test must survive generator refactors."* A
  budget test that imports the generator it is auditing fails at the same time as the thing it
  guards, and for the same reason.

### 2.2 A per-entry cap, and the sentence that makes it stick

**260 bytes per entry**, with the rule stated where the failure prints it:

> *"A description that needs more than 260 bytes is a body paragraph, not a catalog entry."*

The cap is not arithmetic. It is a claim about what an entry is *for*: an entry is a routing
decision, and a routing decision is one sentence. Everything longer is content, and content
belongs behind the decision to load it (§3).

### 2.3 Floors, not only ceilings — and this is the half everyone skips

Three assertions in gstack are floors:

| Floor | What it catches |
|---|---|
| **every entry has a non-empty description** | an entry that empties silently still passes an under-budget check, and is then never selected |
| **per-entry shrink floor ×0.80** against a frozen baseline | *"A skill that was 100 KB at v1.47.0.0 and shrinks to 250 bytes passes [the 200-byte noise floor] despite losing 99.75% of content."* The failure message names the diagnosis: *"accidental body strip (a resolver returning empty, a template losing a section)"* |
| **corpus shrink floor**, same ratio | the same failure across the whole tree at once |

The growth ceilings beside them are **×1.50 per entry and ×1.50 corpus-total**, with the
ratio's own history in the comment — adjusted from 1.05 after a 5% ratio tripped on a
legitimate feature addition, because *"real bloat is 2-3×; this catches that while not
tripping on normal feature scope."* A ratio with no recorded history is a number somebody
picked.

**For Layer D specifically:** a component whose `Contract` summary silently empties passes
every under-budget check and is then never matched — and `Contract.empty` short-circuits
`satisfied_by` to `False` (`identity.py:210`), so the failure is invisible rather than loud.
**Take both directions or neither.**

### 2.4 The ratchet, which is what stops a budget being raised quietly

Printed inside the failure message, not in a document nobody opens:

> *"Adding a skill? Re-measure … Update `CATALOG_BUDGET_TOKEN_EQUIVALENTS` **AND the derivation
> comment (ref/date/value/which skill moved it) in the SAME commit.** Growing an existing
> description? Trim it instead — the catalog is what every host loads at discovery, every
> session."*

Above the constant sits a reproducible `method` block: the enumerator, what is summed, the
conversion, the result, the ceiling, the headroom, the dominant entry. Its header is the
instruction: **"Budget derivation (re-derive it, do not trust the number)."**

A budget with a constant and no derivation gets raised by whoever is blocked by it. A budget
whose constant cannot be changed without changing a dated derivation in the same commit gets
argued about instead, which is the point.

---

## 3 · The split that makes a byte cap survivable

A 260-byte cap is impossible if the entry must also say *when* to use the thing — which
`docs/next/SKILLS.md` requires of every skill description, in words a person would type. Both
demands are right, and they are only compatible because of one mechanism.

**`applyCatalogTrim` splits every description in two.** The **lead sentence** stays in the
always-loaded frontmatter. The **routing prose** moves to a body section headed
`## When to invoke this skill`, which is loaded only when the entry is chosen.

Three invariants make the split safe, and each has a test:

1. **Idempotency.** *"Calling on already-trimmed output returns the same parts"* — re-splitting
   keeps `lead` identical and `routingProse` empty. A generator that runs every build must be a
   fixed point after the first pass.
2. **PRESERVATION.** Content survives somewhere in the skeleton-plus-sections union: *"a carve
   relocates, it never drops."*
3. **The ALWAYS-LOADED CONTRACT.** Everything needed to decide *whether to load the body* must
   be in the always-loaded half. gstack states it as ordering — *"a directive that decides which
   sections to read can't sit behind the STOP that reads them"* — and asserts it on **earliest
   position of use, not loose substring presence.**

The third is the one a catalog will get wrong. **For Layer D: everything needed to decide
whether to load a component's `Contract` body must be in its lead, with a test that the
decision logic is not in the half you only read after deciding.**

And the opt-out is tested, not just the default: gstack runs `--catalog-mode=full` for real,
asserts the legacy block returns and the new heading is absent, restores in a `finally`, and
prints `CRITICAL: failed to restore` if the restore itself fails. Invalid values throw.

---

## 4 · One enumerator, three counts

`test/helpers/skill-census.ts` exists because two test files had two different hand-rolled
directory walks and diverged — *"the divergence class `skill-census.ts` exists to kill."*

The census returns **three counts that deliberately differ**, and the test pins their
*relationships* rather than their totals (*"No hardcoded totals here — the catalog-budget test
owns the ratchet"*):

| Count | gstack | Layer D's twin |
|---|---|---|
| physical files | every `SKILL.md` on disk, router and symlink dups included | component files under `library/catalog/**` |
| authored entries | symlink-deduped, router excluded | distinct components |
| registry entries | unique frontmatter names + alias | catalog-addressable `Contract`s |

With two relations asserted: `registryEntries ≤ physicalFiles`, because *"it can only collapse
entries relative to physical, **never invent them**"*; and *"every registry entry a host would
see resolves back to a physical SKILL.md."*

**They are not equal, and a system that reports one number is reporting the wrong one.** Layer
D already has this problem: four seed entries on disk, one of which is matchable — the
as-built document and `docs/next/LAYER-D-LIBRARY.md` §1 disagree with any count of "components"
that does not say which count it means.

---

## 5 · Limits — what the source shows versus what we would be assuming

- **Every number here is gstack's, on gstack's corpus, at one date.** 1,150 TE, 260 bytes, ×1.50,
  ×0.80, 7,000: none of them is derived from Scio's catalog, and adopting any of them without
  re-deriving is exactly the failure §2.4's ratchet exists to prevent. **The method transfers;
  the constants do not.**
- **A byte-to-token divisor is not a constant.** gstack fits per-content-class divisors
  (`frontmatter` 3.99, `skillmd` 4.21, `reference` 4.15, `artifact` 3.67, `legacy` 3.47) because
  *"measured bytes-per-token spans 2.36 to 4.72 and the spread is largely structural."* Classes
  cut mean per-file error from **11.1% to 7.4%** — and they publish the worst case, near **40%
  on heterogeneous files**, with the rule *"use `--exact` when a single file's number has to be
  right."* The divisors are tokenizer-specific and **expire on the next model**. `ceil(bytes/4)`
  is a token-*equivalent*, and calling it a token count is the first dishonest step.
- **This is a working repo's tests, not a study.** There is no controlled comparison showing a
  budget improved anything. What it shows is that the mechanism is cheap enough to have been
  built and specific enough to have caught things — their own comments name the catches.
- **The 260-byte cap is inseparable from the split.** Quoting the cap without §3 produces
  entries that no longer say when to use them, which `docs/next/SKILLS.md` establishes is the
  field that decides whether a skill fires at all. **Do not adopt §2.2 without §3.**
- **Scio has measured its skills catalog twice and its component catalog never.** Both
  measurements in §6 E1 were taken while writing this skill, on the same day. Two points are
  a delta, not a trend, and neither is a measurement of `library_entry` — which is the catalog
  this skill is filed under and the one nobody has counted.

---

## 6 · Eval

Runnable. Case 1 is runnable **now** and is the reason this skill is not theoretical.

### E1 · Measure this repository's own discovery surface

Sum `byteLength(name) + byteLength(description)` from the frontmatter of every
`.claude/skills/*/SKILL.md`; report bytes, `ceil(bytes/4)` token-equivalents, the per-entry
distribution, and the dominant entry.

**Two measurements, both 2026-08-26, six hours apart:**

| | Entries | Bytes | Token-equivalents | Mean/entry | Over 260 B |
|---|---:|---:|---:|---:|---:|
| morning | 17 | 9,275 | 2,319 | 546 | 17 of 17 |
| evening | 27 | 18,212 | 4,553 | 674 | 27 of 27 |
| gstack, 2026-08-12 | 53 | 4,420 | 1,105 | 83 | 0 |

**The always-loaded surface grew 96% in one working day, and nothing anywhere noticed.** That
is not a hypothetical about a catalog someday getting large; it is this repository, today, and
it is the entire argument for §2.4. gstack carries **twice our entries at a quarter of our
cost**.

Two findings fell straight out of running it, neither of which any other check in the repo
would have produced:

- **`testing`'s description is 1,046 characters — over the 1,024 limit `docs/next/SKILLS.md`
  states as the spec's own maximum.** A per-entry cap of any size would have caught it at
  write time.
- The mean is climbing (546 → 674) as well as the total, so this is not "more skills"; it is
  more skills *and* longer entries.

The diagnosis is not carelessness: §3 is the mechanism we do not have, and `SKILLS.md`
correctly demands the routing prose that gstack moves out of frontmatter and we keep in it.
**The expected outcome of this case is the number and the diagnosis, not a pass.** Re-running
it after any skill is added or edited is the ratchet, and the two rows above are the first two
entries of the derivation block §2.4 describes.

### E2 · The floor catches what the ceiling cannot
Empty one entry's description to the empty string and re-run E1. A check that only sums bytes
**passes**. Add the non-empty floor; it must fail, and the failure must name the entry.

### E3 · The shrink floor catches a body strip
Take one `SKILL.md`, truncate it to 250 bytes, re-run against a frozen baseline. A per-file
noise floor of 200 bytes passes it. The ×0.80 shrink floor must fail it, and the message must
name the diagnosis, not the ratio.

### E4 · The split is a fixed point
Run the splitter twice over the same description. Second run: `lead` identical, routing prose
empty. Anything else means the generator is not idempotent and the budget will oscillate.

### E5 · The decision is not behind the load
For any two-tier entry, assert that the text deciding whether to load the body appears at an
**earlier position** than the load itself. Assert on position, not on presence — a substring
check passes when the directive sits after the STOP that reads it.

### E6 · Three counts, not one
One census module returns physical files, distinct entries and addressable entries. Assert
`addressable ≤ physical` and that every addressable entry resolves back to a physical file.
**Against `.claude/skills/` today this case has a known finding: `graphify` carries no `layer`,
`phase` or `status`, so `scripts/skills-index.py` reports it UNPLACED** — a physical file that
is not a fully-formed registry entry, which is exactly the gap three counts exist to show.

### E7 · The ratchet is enforced, not documented
Change a budget constant without changing its derivation comment in the same commit. Something
must refuse. If nothing does, the budget is a suggestion.

---

## 7 · When this skill is the wrong tool

- **A catalog that is not loaded whole.** If entries are fetched by an indexed query, the cost
  does not scale with the catalog and this skill is solving somebody else's problem. See
  `contract-retrieval` §3 for that direction.
- **Choosing Scio's actual numbers.** A budget for `library_entry`, or for
  `.claude/skills/`, is a decision with a cost attached — it constrains what future entries may
  say. That is an ADR. This skill says how to derive one and what to assert around it; it does
  not get to pick it.
