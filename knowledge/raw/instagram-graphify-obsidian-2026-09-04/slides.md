---
title: On-screen text of the 16 received carousel frames, read 2026-09-04
status: RAW — a read off the frames; the images are not stored
---

# Frame text, in the order received

Screenshots arrived out of slide order (2, 3, 4, then 20 down to 8). Listed below in
**slide order**. Each heading carries the md5 of the screenshot it was read from.

## Slide 2 — THE PROBLEM  (md5 `8d96180aa86d0fcb7dc1eb3ac9f7b70e`)
"Claude Code is **smart**. But if you dump 145 random documents on it, it has to search
through them **one by one**. That's **slow**. And it misses how ideas connect to each other."
THE PROBLEM: "Slow and disconnected." THE IMPACT: "Misses context. Loses connections."
Footer: "What if it could see the WHOLE picture at once?"

## Slide 3 — THE 2 TOOLS  (md5 `e938e0fc0664449180f11ddbf403ac73`)
Browser on `github.com/safshams/graphify` [sic — as rendered in the frame]. Badges legible:
Y Combinator S26, MIT license, downloads 1.4M, Contributors 17, Languages Python 100%,
"Packages: No packages published", a star-history chart, and a long "Read this in other
languages" row. README text: "Type `/graphify` in your AI coding assistant and it maps your
entire project — code, docs, PDFs, images, videos — into a knowledge graph you can query
instead of grepping through files. Works in Claude Code, Codex, OpenCode, Kilo Code, Cursor,
Gemini CLI, GitHub Copilot CLI, VS Code Copilot Chat, Aider, Amp, OpenClaw, Factory, Droid,
Trae, Hermes, Kimi Code, Kiro, Px, Devin CLI, and Google Antigravity." Then "`/graphify .`"
and "That's it. You get three files:" with `graphify.md` visible.
TOOL 1 **Graphify** "turns any documents into a map of connected ideas."
TOOL 2 **Obsidian** "a notebook app where Claude Code can browse that map."
"Alone, each is good. Together, they're **way better**."

## Slide 4 — WHY COMBINE THEM  (md5 `1efa1fa0729e032c3f70a25aa7826e6b`)
"Graphify alone has one problem: it works in a **bubble**. It maps ONE set of documents, but
doesn't know how that fits into everything else you're working on. Obsidian fixes that — it
**connects** the new map to your bigger project."
GRAPHIFY "Works in a bubble" + OBSIDIAN "Connects to your bigger project" = TOGETHER
"Complete. Connected. Unstoppable." / "One maps the ideas. The other puts them in context."

## Slides 5, 6, 7 — NOT RECEIVED

## Slide 8 — STEP 03, "The numbers."  (md5 `260388a32c234d5c19044f41a2588cfe`)
**145** documents · **591** ideas (called "nodes") · **685** connections between ideas ·
**67** topic groups. "145 docs turned into 591 separate, connected ideas."

## Slide 9 — "Big ideas attract more connections."  (md5 `ca1f41d470618d5017a086e10b9e3c75`)
"Some ideas are way more important than others. Example: 'Context Window' connects to tons of
other ideas — like rules, sub agents, and special hooks. The bigger the dot on the map, the
more important that idea is."

## Slide 10 — "See the whole map."  (md5 `e9b9d54b824f3c6f7adc6562bda79cd2`)
Obsidian **graph view of the creator's own vault** — title bar "The Vault", sidebar
`_archive-vault, content, daily-notes, templates, tips, projects, rm, system, ideas, CLAUDE`,
node labels are dated daily notes (`2024-08-08 …`, `2026-08-28 …`). Status bar:
**"1,252 nodes  1,073 edges"**. Caption: "All of this turns into an actual picture. Each dot
= one idea. Each line = a connection between ideas. Bigger dot = more connections = more
important." NOTE: this is not the graphify vault; slide 8 holds those numbers.

## Slide 11 — "Why this matters."  (md5 `bd6b7a09fc7f67b00d6ca3ad3df2c0c3`)
"Now if you ask Claude Code about 'sub agents,' it doesn't just search for the word. It
already knows what sub agents connect to — like 'agent teams' — because it has the map. It
understands the WHY, not just the WHAT. It's not just search. It's understanding."

## Slide 12 — "But there's a catch."  (md5 `7dbf0cb101ef5569b3824528978de305`)
"This map is amazing… but it only exists inside Graphify. It has nothing to do with your other
notes, projects, or your main Obsidian vault. It's stuck in its own bubble. Powerful map. But
isolated."

## Slide 13 — "The big question."  (md5 `a1e189af54776bd2124c99a439a5e4c4`)
"How do we get this map INTO Obsidian, where all your other stuff already lives? Turns out,
there's a one-word answer for that. The 3-step setup →"

## Slide 14 — "One command does it all."  (md5 `52ec5b9b50fed17de4c9143b5e76393b`)
"The magic command: `graphify --obsidian`. This takes all **591** ideas and turns each one
into its own note — automatically linked to every other related note."
Browser shows the README's **Full command reference**, the line `/graphify ./raw --obsidian`
highlighted. Lines legible in the frame:
```
/graphify                          # run on current directory
/graphify ./raw                    # run on a specific folder
/graphify ./raw --mode deep        # more aggressive relationship extraction
/graphify ./raw --update           # re-extract only changed files
/graphify ./raw --directed         # preserve edge direction
/graphify ./raw --cluster-only     # rerun clustering on existing graph
/graphify ./raw --no-viz           # skip HTML visualization
/graphify ./raw --obsidian         # generate Obsidian vault
/graphify ./raw --wiki             # build agent-crawlable markdown wiki
/graphify ./raw --svg              # export graph.svg
/graphify ./raw --graphml          # export for Gephi / yEd
/graphify ./raw --neo4j-push bolt://localhost:7687   # generate cypher.txt for Neo4j
/graphify ./raw --match [reads as --watch in the fetched README]  # auto-sync as files change
/graphify ./raw --mcp              # start MCP stdio server
/graphify add https://arxiv.org/abs/1706.03762
/graphify add <video-url>
/graphify add https://... --author "Name" --contributor "Name"
/graphify query "what connects attention to the optimizer?"
/graphify query "..." --c=1S --c-thoughtt 1500   [blurred; fetched README reads --dfs --budget 1500]
/graphify path "DigestAuth" "Response"
/graphify explain "SwinTransformer"
graphify uninstall                 # remove from all platforms in one shot
graphify uninstall --purge
graphify uninstall --project --platform codex   # remove project-scoped install files only
graphify hook install
graphify hook uninstall
```
Above it: `uv tool upgrade graphify` / `graphify install  # overwrites the skill file`.

## Slide 15 — "You have 4 choices now."  (md5 `72188c07bd0bd8d041dd3e9dfebd6e46`)
"Before dumping 600+ new notes into your vault, you get to pick: **1** Keep it as its own
separate vault. **2** Dump it all into one folder you can delete anytime. **3** Hand-pick only
the notes you want. **4** Spread every note into the 'right' folder in your main vault.
No wrong answer — just depends on how **tidy** you want to be."

## Slide 16 — "The easy path (what I did)."  (md5 `0f43d8e7f09ac2a7ec41f7032508c5ea`)
"I picked the safest combo: make it its own vault first, **THEN** drop it into my main vault as
one folder. That way, if I ever hate it, I delete one folder and it's gone. No mess."
Screenshot: Obsidian graph view, vault **cc-docs**, sidebar full of `_COMMUNITY_…` notes
(`_COMMUNITY_Auto Mode & Loop`, `_COMMUNITY_AWS Enterprise Auth`,
`_COMMUNITY_Checkpointing & Rewind`, `_COMMUNITY_Cloud & Web`, `_COMMUNITY_Community 12 … 41`).

## Slide 17 — "Open it in Obsidian."  (md5 `616f2e31404dbb06ebb3d9fad90aa89a`)
"To open the new vault, go to Obsidian → **'Open folder as vault'** → pick the folder Graphify
just created. Just like that, it shows up as a real, working notebook."
Screenshot: the creator's **main** vault, an "AGENTIC OS" dashboard note — tabs
OVERVIEW / AUDIENCE / RESEARCH, "TOKEN BURN · 5H WINDOW · LIVE 3%", "YOUTUBE SUBS 132,000",
"LATEST UPLOAD ultracode is the notebook 1.2K views 37 likes", buttons PLAN TODAY /
CONTENT CASCADE / DEEP RESEARCH / PULL METRICS, QUICK ACTIONS (OPEN CONTENT OPPORTUNITIES,
RUN CONTENT CASCADE, OPEN TODAY'S NOTE, OPEN VAULT, LOG TOKENS), an ACTIVITY FEED
(`METRICS-PULL Pulled 4/4`, `MORNING-REPORT File already created`,
`GITHUB-TRENDING Wrote inbox/research/github-trending[2026-09-0?] 10 weekly / 5 monthly ◇ 5 AI-flagged`),
"runner online · last pull 5h 58m ago · next in 9m"; sidebar `_archive-vault, content,
daily-notes, inbox, ops, projects, raw, system, wiki, _index, _sfc-managed-mcp,
Bash Permission Rules, CLAUDE, Subagent Separate Co…`. Over it the Windows dialog
**"Open folder as vault"** at `This PC > Local Disk (C:) > Users > Chase > vaults > cc-docs`,
which contains one folder `obsidian`; "Folder: cc-docs".

## Slide 18 — "One problem: bare notes."  (md5 `52b45cb132224ac9765d6ca05acf5d1a`)
"At first, each note is pretty empty — just a title and some links. Example: 'Auto Mode' note
just says it connects to 'Claude Code on Amazon Bedrock.' That's it. Not very useful…"
[caption cut off by the frame]
Screenshot: cc-docs vault, note **"agents Command"**, Properties:
`source_file  claude-code-docs/sub-agents.md` · `type  concept` ·
`community  Sessions & Skills` · `tags  #graphify/concept  #graphify/EXTRACTED
#community/Sessions_Skills`. Body: "/agents Command → Connections → • Subagent – references
[EXTRACTED]". Status bar: **"3 backlinks · 4 properties · 15 words · 143 characters"**.

## Slide 19 — "Fix it: link back to the source."  (md5 `6bdb8c28cb22dace7808463aeacff66f`)
"I gave one more instruction: **'Pull the source docs in and link every note back to where it
came from.'** Now every note shows exactly which original document it's based on."
Screenshot: cc-docs note "Auto Mode" with Properties, and the Claude Code terminal running the
instruction. Status bar: "3 backlinks · 4 properties · 19 words · 160 characters".

## Slide 20 — "Move it into the main vault."  (md5 `e33a0f8ea01d2cfa69e096cfd7ab5e05`)
"Last step: **'Move this vault into my main vault, in its own folder.'** Done in under a
minute. Now it's part of my bigger system — not stuck in a bubble anymore. 145 random docs →
one searchable, connected, second brain."
Terminal text legible in the frame:
```
> pull the source docs in and wire every node to its origin in the cc-docs folder
• On it — both steps in the cc-docs vault: pull the 145 source docs in, wire every node
  to its origin.
• PowerShell($(folder = "C:\Users\Chase\vaults\cc-docs"
             $raw    = "C:\Users\Chase\demo\claude-code-docs"…)
  STEP 1 — source docs pulled into sources/:   146
  STEP 2 — nodes wired to their source:        589
  ~181 lines (ctrl+o to expand)
• Done — the cc-docs vault is now the full build:
  vaults\cc-docs\
    657 node stubs        + 589 now have the "Source doc" callout under
    sources\                 their source:
      _src-mcp.md …       + 146 source docs pulled in
    graph.canvas
```
Status line: "the vault | Opus 4.8 (1M context) | 22% | bypass permissions on (Shift+tab to
cycle)". Sidebar of the cc-docs vault shows node stubs alphabetically (`Auto-Fix Pull
Requests`, `architecture`, `Automatic Compaction`, `availableModels Setting`,
`AWS SigV4 Authentication`, `Bash Permission Rules`, `Bash Tool`, `Binary Integrity & Code
Signing`, `Bundle Split`, `BypassPermissions Mode`, `Cache Refresh (TTL)`, `Changelogs`,
`Channel MCP Server (push events)`, `Channels_1..3`, …) and an open note `src-skills` quoting
Claude Code's own docs ("Bundled skills … including: /code-review, /batch, /debug, /docs, and
/claude-md").
