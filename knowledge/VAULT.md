---
title: The Obsidian vault — this repository opened as one
status: verified
fetched: 2026-09-04
tags: [obsidian, knowledge-base, graphify, tooling]
related: ["[[graphify-assessment]]", "[[graphify-features]]", "[[llm-wiki-pattern]]"]
---

# The Obsidian vault

**Open the repository root as a vault.** Obsidian → *Open folder as vault* → this directory.
`.obsidian/` is committed with the settings that make the knowledge base readable as one:
wikilinks on, shortest-path link resolution (a note's `[[subagents]]` resolves to
`knowledge/notes/subagents.md` wherever the reader stands), and `userIgnoreFilters` that
keep build artefacts, fixtures and ledgers out of search and the graph. Per-machine state
(`workspace.json`, cache, installed plugins) is gitignored, so opening the vault changes
nothing anyone else sees.

Start at [[INDEX]]. Graph view colours: notes green, `knowledge/raw` orange, `intake/` grey,
skills blue, agents purple, pipeline yellow, catalog light grey.

## Why no graphify step for the knowledge base itself

Graphify **does** have an Obsidian mode — checked 2026-09-02 on the installed `graphify
0.9.53`:

```
graphify export obsidian [--graph PATH] [--labels PATH] [--dir PATH]
```

On a 23-node test graph it wrote 29 notes (one per node, YAML frontmatter with
`source_file`, `type`, `community`, tags `graphify/code`, `graphify/EXTRACTED`, a
`## Connections` list of `[[wikilinks]]` with the edge type), one `_COMMUNITY_*` note per
Leiden community, a `graph.canvas`, and its own `.obsidian/graph.json`. The flag form
`extract --obsidian` is silently ignored; the subcommand is the one that works
([[graphify-assessment]] records the correction chain).

But graphify exports a **graph it built**, and for a markdown corpus the graph comes from
the LLM semantic pass, which costs the tokens the tool exists to save and produces a worse
graph than the `[[wikilinks]]` the notes already carry ([[graphify-assessment]] §(b)). The
knowledge base *is* a graph; Obsidian reads it directly. So the vault above is the answer
for `knowledge/`, and graphify's export is the answer for **code** — the predecessor's
as-built graph, for instance:

```
# a vault of hello-world's 5,173-node code graph, regenerated on demand, gitignored
graphify export obsidian \
  --graph intake/2026-08-30-agent-and-skill-material/scio/docs/as-built/graph/graph.json \
  --dir knowledge/vaults/hello-world-code
```

That vault is opened separately; it is excluded from this one's graph by the ignore filter,
because five thousand code nodes would drown thirty-seven notes.

## The index and the vault are the same files

`knowledge/kb.py` and Obsidian read the same markdown. `kb.py links` reports the dangling and
one-way wikilinks Obsidian's graph shows as unresolved nodes; fix them in the notes and both
views agree.

## Someone else ran the doc-corpus route, and what it changes here (read 2026-09-04)

A 20-slide Instagram carousel (@divyannshisharma, 16 of 20 slides received as screenshots)
walks `graphify --obsidian` over 145 Claude Code doc files and into an existing vault. Raw
and the frame text: `knowledge/raw/instagram-graphify-obsidian-2026-09-04/`. It is a social
post, not a measurement — every number below is **REPEATED** unless it says otherwise — but it
is the first end-to-end account of the route this page declined, by someone with no stake in
our answer, and it confirms the shape.

**The generated vault is a separate vault, and stays one.** This is the part worth having.
Graphify writes `vaults/cc-docs`; it is opened on its own (Obsidian → *Open folder as vault*),
edited there, and only at the very end moved into the main vault **as one folder**. The
carousel lists four merge options — own vault · one deletable folder · hand-pick notes ·
spread into the "right" folders — and picks the first two combined, for the reason this
repository picked them independently: *"if I ever hate it, I delete one folder and it's gone."*
That is what `knowledge/vaults/hello-world-code` already is, and what the `userIgnoreFilters`
already enforce. **Outcome: keep.** Nothing to change; the reason is now written down so the
question does not come back. (v8's `--obsidian-dir ~/vault` writes straight into an existing
vault and claims never to overwrite your notes or `.obsidian` config — see
[[graphify-features]]. Untested here, and the separate-vault path costs one `mv`.)

**The bare-stub finding, against our own measurement.** The carousel's complaint is that the
exported notes are empty: slide 18 shows one note at **15 words, 143 characters** — a title, a
`## Connections` list with a single `references [EXTRACTED]` edge, and frontmatter
`source_file: claude-code-docs/sub-agents.md`, `type: concept`, `community: Sessions & Skills`,
`tags: #graphify/concept #graphify/EXTRACTED`. That is *exactly* the shape measured here on
2026-09-02 (23 nodes → 29 notes, frontmatter + `## Connections`), so the two agree and this
page's description was right. The correction is to what that shape is **worth**: the export
does record provenance, as a **path in frontmatter**, but the source document is not in the
vault, so the path opens nothing and the note has no body. A vault of such stubs is navigable
and unreadable at the same time.

**The fix is not a graphify flag.** The carousel's repair is an instruction to the coding
agent afterwards — *"pull the source docs in and wire every node to its origin"* — which
copies the corpus into `sources/` and adds a "Source doc" callout per note. Reported result:
`146` source docs pulled in, `589` nodes wired, `657` node stubs in the vault (REPEATED).
Against slide 8's `145` documents → `591` nodes · `685` edges · `67` communities: `591 + 67 =
658`, so the stub count includes the `_COMMUNITY_*` notes and is one short; `589` of `591`
concept nodes got a callout, so two did not; and `146` pulled docs against `145` counted is off
by one (all DERIVED, none explained on the slides).

**Do not read slide 10's numbers as graphify's.** The carousel intercuts the creator's own
"AGENTIC OS" vault — a dashboard note with token-burn and subscriber panels — with the
generated one, and the graph view captioned "See the whole map" reads **1,252 nodes · 1,073
edges** over daily notes going back to 2024. That is their vault, not the 591-node build.

**What changes here: nothing for `knowledge/`, one line for code vaults.** The argument above
stands — our notes already are the graph. But when the code-graph vault is regenerated, its
notes carry the same `source_file` frontmatter, and it is only readable **beside the repo it
was built from**; the vault alone is stubs. So: regenerate it next to the source, or not at
all. We do not pull sources into it — the raw layer and `intake/` already hold them, and
copying a corpus into a gitignored vault would make a fourth copy of files we hash for a
living.

## The on-demand command, actually run (MEASURED 2026-09-04)

The command above had been written and never executed — and the day's correction chain is
three passes long precisely because an invocation form was quoted rather than run. So it was
run, on the 5,173-node as-built graph of the predecessor:

```
uv tool install graphifyy                     # graphify 0.9.53, 2.1 s
graphify export obsidian \
  --graph intake/2026-08-30-agent-and-skill-material/scio/docs/as-built/graph/graph.json \
  --dir knowledge/vaults/hello-world-code     # 2.4 s, 0 LLM tokens
```

**It works as documented.** 5,401 notes + `graph.canvas`, 24 MB. The arithmetic checks:
**5,173 node notes** (exactly the graph's node count, each carrying `source_file`) **+ 228
`_COMMUNITY_` notes = 5,401** — the same shape as the carousel's 591 + 67 ≈ 657, and the reason
a "node count" and a "note count" are never the same number.

**The bare-stub finding, now measured on our own artefact.** Node notes: **median 42 words**,
p90 86, and **4,815 of 5,173 are under 100 words**. A typical one is frontmatter
(`source_file`, `type`, `community`, `location`, tags), an H1, and a `## Connections` list of
one or two tagged wikilinks. The `_COMMUNITY_` notes are the readable layer: median 271 words.
So the carousel's complaint reproduces here without borrowing its numbers.

**And the reachability claim is no longer an argument.** The vault holds **380 distinct
`source_file` paths**. **377 of 380 resolve inside the hello-world repository. 1 of 380
resolves inside skills-repo, where the vault itself sits.** A vault of stubs whose provenance
resolves 0.3% of the time in its own repository is the "stub with a footnote" case exactly.
Hence the rule above, now with a measurement behind it: **regenerate it beside the source, or
not at all** — and it stays gitignored, because two seconds of CPU is cheaper than 24 MB in git.

Still not measured: opening it in the Obsidian desktop app (no desktop in this session). The
markdown and canvas validate; the rendering does not.

**One caveat for the `--wiki` feed** (the "candidate input to our knowledge base" in
[[graphify-assessment]]): `graphify export wiki` takes no `--dir`, ignores one if given, and
writes 238 articles beside the graph file. Point `--graph` at a scratch copy, never at the
graph inside `intake/` — measured the hard way on 2026-09-04, see [[graphify-features]].

## Runbook — doing this on your own machine

None of this can be finished in a session container: Obsidian is a desktop app, and the
container is ephemeral. This is the copy-paste version for a real machine. Every command below
was either **run here on 2026-09-04** (marked ✓) or **read from `graphify --help` on 0.9.53**
(marked ⌁); nothing is quoted from a README, which is the mistake this page has already paid
for three times.

**Prerequisite:** Python ≥3.10.

```bash
uv tool install graphifyy          # ✓ 2.1 s, installs `graphify` + `graphify-mcp`
# or: pipx install graphifyy / pip install graphifyy
graphify --version                 # ✓ 0.9.53
```

### Route A — this repository as a vault (no graphify, no cost)

Clone it, then Obsidian → *Open folder as vault* → the repository root. `.obsidian/` is
committed, so the settings, the ignore filters and the graph colours come with it. Start at
[[INDEX]]. This is the one that needs nothing installed.

### Route B — a code repository as a separate vault (0 LLM tokens)

```bash
graphify extract /path/to/repo --code-only          # ⌁ local AST, no API key; writes
                                                    #   /path/to/repo/graphify-out/graph.json
                                                    #   (--out DIR to put it elsewhere)
graphify export obsidian \                          # ✓ 2.4 s on a 5,173-node graph
  --graph /path/to/repo/graphify-out/graph.json \
  --dir  ~/vaults/<name>
```

Then Obsidian → *Open folder as vault* → `~/vaults/<name>`. **Keep it beside the repository it
was built from.** Measured here: of 380 distinct `source_file` paths in such a vault, 377
resolve inside the source repository and **1** resolves anywhere else — the notes are stubs
(median 42 words) whose value is the link back to code you can actually open.

### Route C — a folder of documents (the route the carousel demonstrates)

Same shape, but drop `--code-only`: documents have no AST, so extraction goes through the
**LLM semantic pass and costs real tokens**. This repository's standing arithmetic is a payback
of roughly 240 queries ([[graphify-assessment]]), so this is worth it for a corpus you will
interrogate repeatedly and not worth it for one you will read twice. It is also why
`knowledge/` itself is not run through it: these notes are already a graph.

### Merging into an existing vault

Build it as its own vault, look at it, then move the folder in. One `mv`, and one `rm -rf` if
you dislike it. The skill surface also offers `/graphify … --obsidian --obsidian-dir ~/vault`,
which claims never to overwrite your own notes or `.obsidian` config — **untested here**, and
the separate-vault path costs one move.

### The four traps, all measured 2026-09-04

1. **`export wiki` ignores `--dir`.** It accepts the flag, returns no error, and writes
   `wiki/` (238 articles) *beside the file `--graph` points at*. Export from a scratch copy of
   the graph, never from one sitting in a directory you care about. `export obsidian` does
   honour `--dir`; the two are not symmetrical.
2. **Two surfaces.** `/graphify … --obsidian` is a *skill* flag; `graphify export obsidian` is
   the *CLI* subcommand; `graphify extract … --obsidian` is neither and is silently ignored.
   The same trap sits on `--no-viz`, which belongs to `cluster-only`, not to `extract`.
3. **The default branch's README is a v1-era document.** Read `.../graphify/v8/README.md`.
4. **A node count is not a note count.** The vault carries one note per node *plus* one per
   Leiden community — 5,173 + 228 = 5,401 here.

Untested anywhere in this page: how any of it renders in the Obsidian desktop app.
