# The third batch, 2026-09-11 — the first one that ran over real time

Three days, not three minutes. **40 of 96 rows moved: 34 CHANGED, 6 noise.** The first batch
tested whether the watcher could tell noise from content; this one tested whether it is worth
reading, and the answer came from the shape of the diffs rather than their count.

| words changed | rows | what they were |
|---|---|---|
| 1 | 7 | a day-counter, a star count, an added error code, a renamed API symbol, a moved link anchor, a nav item, a logo filename |
| 2–50 | 8 | README edits, a pricing table, a version bump |
| 100–500 | 6 | `code.claude.com` docs with real new sections |
| 500–2,130 | 5 | `skills.md` alone moved **2,130 words** |

## The one that mattered, and it is why the row exists

`docs.z.ai/guides/overview/pricing` was added on 2026-09-08 for one stated reason: *"a source
whose entire purpose is that the figure changes is the last one that should be unwatched."*
Three days later it changed, and the change was material.

**GLM-5.3-Flash doubled.** It had been `$0.075 / $0.015 / $0.25` under a 50% launch discount
whose own page said *"The promotion ends at 24:00 on September 9, 2026 (UTC+8, Singapore
time)."* It ended. The page now shows the single list column: **`$0.15 / $0.03 / $0.50`**.
GLM-5.3 and GLM-5.2 are unchanged at `$1.4 / $0.26 / $4.4`.

**Two notes cited it and only one survived.** `glm-5.3-local` recorded the discounted price *and
the list price beside it*, with the words "50% launch discount" — so the correction was a
deletion. `model-routing-free-and-local` cited the discounted pair flat, inside a cost table used
to decide routing, and was **2× wrong the moment the promotion lapsed**. Same fact, two notes,
and the one that wrote down *why* the number was low is the one that did not rot.

## A third noise class, inside the visible text this time

Both unsloth pages reported CHANGED with a **one-word** diff: `Last updated 10 → 13` and
`4 → 6`. A rendered relative timestamp — and it ticks every day, so those rows would have
reported CHANGED forever.

The `noise` verdict was blind to it **by construction**: the counter is prose, and the verdict
only removes what is not. What makes this one narrow rule different from the deploy-id
normaliser this file deleted twice:

- the counter counts **up from a fixed edit date**, so a rising number is positive evidence the
  page was *not* updated — **the token that fires the alarm is the token proving nothing
  changed**;
- `N <unit> ago` is a universal web idiom, not one site's bundler quirk, so the rule needs no
  per-row knowledge. That was exactly the test the deploy-id rule failed: it needed the answer in
  order to produce it.

Scoped hard — the number must be followed by a time unit **and** the word "ago" — and asserted in
both directions: a price, a version and a bare `6 days` with no "ago" must all still fire. Four
mutations; three caught immediately. The fourth, applying the rule *before* tags are stripped,
survived — and was a missing fixture, not a redundancy: frameworks wrap the number in its own
element (`Last updated <b>6</b> days ago`), and in raw HTML the pattern would not match across
the tag, so the rule would silently stop working on exactly the pages it exists for. That fixture
now exists and the mutation is caught.

## Seven rows triaged and re-baselined here; the rest are a queue, not a finish

Triaged, each checked against the notes that cite it:

| source | change | verdict |
|---|---|---|
| `docs.z.ai` pricing | the discount expired | **REAL**, two notes corrected |
| `prime-agent` README | `rlm(...)` → `rlm.spawn(...)` | an API change, but **no note cites that symbol** — checked, not assumed |
| `hooks-guide.md` | a new error code `cloud_credential_error` | real, **no note cites the error list** |
| `features-overview.md` | a link anchor moved to `#resolve-skills-that-share-a-name` | link target only — and note it was **caught** here, because markdown keeps the strict byte comparison; the same change inside HTML is the documented blind spot |
| augmentcode graphify | star count 883 → 884 | immaterial |
| `Graphify-Labs` README | logo filename and height | immaterial |
| openrouter limits | one nav item added | immaterial |

**The remaining 27 rows are deliberately left CHANGED.** Ten are `code.claude.com` docs this base
cites heavily — `skills.md` moved 2,130 words, `hooks.md` 1,090, `model-config.md` 1,051 — and
re-reading those is a real ingest pass, not a triage. Re-baselining them without reading them
would convert an honest backlog into a silent one, which is the failure this whole branch exists
to prevent. They stay red until they are read.

## Triage cost, which `BRAIN.md` asked to be measured

Batch 1: ~1 hour, 4 rows, 1 finding. Batch 2: ~20 minutes, 8 rows, 4 findings. Batch 3: **~15
minutes to classify all 34 and settle 7**, because the work became a script — fetch every changed
row, strip to visible text, count the word-level diff, and read the small ones first. The seven
one-word diffs were decided in a single glance at their changed words. **The cost per row fell
because the ordering changed: by size of prose diff, smallest first.** A 2,130-word diff needs an
ingest pass; a one-word diff needs one look, and there are more of the latter.

Nothing here was edited after fetching. The 2026-09-08c copies are kept as the provenance of the
rows these superseded.

---

## The ingest pass — ten `code.claude.com` docs re-read

The 27-row queue's real half. Four readers, one diff each or a cluster, all read-only; the
coordinator applied every edit. 408 added lines across ten pages — far less than the word counts
implied, because most of the diff was rewriting rather than adding.

## Four notes were FALSE, not merely incomplete

| note | said | actually |
|---|---|---|
| `dynamic-workflows` | a workflow run is *"resumable **within the same session only** (exit → next session starts fresh)"* | **Wrong, and wrong before the diff that corrected it.** Results are saved under the session's directory in `~/.claude/projects/` and replay after `claude --resume`; in a **cloud session** they survive the VM being reclaimed. The boundary was never "same session" but *same session id with its saved results present*. Missing results give an explicit **`nothing to resume`** rather than a silent re-run. The held 2026-09-04 bytes already carried the `--resume` half — our misreading, not a vendor change. |
| `mcp` | a complete precedence chain headed by Local | **`managedMcpServers`** (managed settings, **v2.1.259+**) ranks above all of them. An organisation can replace a server a project pinned, and the project's `.mcp.json` will not win. |
| `plugins-and-marketplaces` | `/reload-plugins` (no restart) | Not for **plugin MCP servers in a session without an interactive terminal** — which is exactly what `claude -p` is, so it covers this repo's own dispatch runs. |
| `subagents` | the highest version cited is v2.1.257, so the gap is 4 releases | **Third time stale.** The pass brings v2.1.259, .260, .265 and **.267**, putting v2.1.261 *below* the ceiling. The figure is **deleted**, not updated — see below. |

## The finding that outranks all of them

**A sentence whose truth depends on the whole corpus is a query, not a claim.** The
highest-version sentence has now gone stale three times, and each correction reproduced the defect
it was correcting. **Two readers, briefed on disjoint documents and disjoint note sets, flagged it
independently** — which is what turned it from one page's problem into a property of the base. The
instruction beside it ("compute it, do not read it here") was always right; the number sitting next
to the instruction was the bug. Deleted, with the command that computes it left in its place.

## Behaviour changes this base had recorded *neither* side of

- **Token counting through a gateway.** Held: without `count_tokens`, Claude Code *"falls back to
  counting context usage through the inference endpoint"*, remedy *"so token counts don't consume
  inference requests"*. Live: *"falls back to a **character-based estimate**"*, remedy *"for exact
  token counts"*. Three signals agree it is a change — mechanism, cost, and the remedy rewritten
  to match. `/context` is now an estimate.
- **A subagent can no longer escalate itself** (v2.1.267): under a `default`/`dontAsk`/`plan`
  parent, a declared `bypassPermissions` is refused and the parent's mode kept.
- **`disallowedTools` with a specifier removes the whole tool.** `Bash(git push *)` deletes Bash
  from the subagent. The fix lives in `permissions.deny`, which binds the main conversation too —
  a wider blast radius than the trap. Same shape as the `tools:`-omitted-inherits-ALL default.
- **`mcp_tool` hooks are skipped, not errored**, before MCP servers are available — on `Setup`
  always. Bootstrap wiring buys silence.
- **`SessionStart` is not once per session**; it re-fires on `/clear` and compaction, and its
  output is **discarded** if you clear or resume again while it runs.
- **`stopReason` is model-visible now** (it read *"Not shown to Claude"*).
- **A workflow `agent()` blocked by the auto-mode classifier resolves to `null`** — so
  `.filter(Boolean)` turns a *blocked* agent into an absent one, and anything counting results
  under-reports without erroring.
- **`opts.schema` is enforced**: a self-contradicting schema fails before the subagent starts; five
  validation attempts otherwise, tunable with `MAX_STRUCTURED_OUTPUT_RETRIES`.
- **The always-on denominator is wrong**: models with a native 1M window *"compact before the
  window fills, at about **967K** tokens by default"*, so 2.26% is really 2.34%.
- **`context: fork` is not a conversation fork**, said explicitly for the first time. This base
  held *both* meanings, each correct, in two notes that link to each other.
- **Two documented fan-out paths** a subagent has that our n=1 measurement never tried, neither
  needing an `Agent` tool: `SendMessage` resumes a completed subagent in the background, and a
  subagent may hold `SendMessage` itself.

## The gate caught its author three times, on one mechanism

Re-baselining renames files, and the superseded-baseline join is a **filename stem heuristic**. It
failed three times in one session because the author kept inventing names: once on the
2026-09-11 triage batch, once here, and once more after that. It never produced a wrong *pass* —
every failure was loud and at the right moment — but the repetition says the heuristic's weak
point is not the matching, it is that **nothing tells you the convention at the moment you choose
a name**, and two conventions are live side by side (`skills@<date>.md` and
`code.claude.com_docs_en_<page>.md`). The fix applied was to match each new file to its own
predecessor's form, automatically, rather than to loosen the check.

**Then it caught the author a fourth time, on this very file.** The ingest pass was written up as
`README-docs.md`, and the accounting excludes exactly three names — `README.md`, `MANIFEST.md`,
`WATCH.tsv` — so a second documentation file in a raw directory is, correctly, an unaccounted raw
file. **This one reached CI**, which is the first failure in this branch that a local run did not
catch first, and only because the check was run before the file was written rather than after.
Fixed the same way as the other three: the two READMEs are merged into the one the convention
expects, rather than the exclusion list being widened to `README*`. Widening it would have made
every future stray `.md` in the raw layer invisible — which is exactly the hole this check exists
to close.
