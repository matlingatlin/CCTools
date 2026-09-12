# Source log

**What this file is, corrected 2026-09-04.** It used to claim "every source consulted for the
knowledge base". Measured that day: the notes' frontmatter carries **130 distinct source URLs
and 112 of them are named nowhere here** (a handful of the 130 are endpoints rather than
sources, e.g. `http://localhost:11434`, so the shortfall is a little smaller than the count —
the claim is false either way). The file did not rot; the knowledge base outgrew it. Provenance
moved into each note's frontmatter, where it belongs, because that is where a claim's `url`,
`fetched` and `note` sit beside the claim they support.

So this file is **the hand-written batch record**: dated rounds of work, what each round was
for, and which pages it fed. The complete, machine-checkable register is the frontmatter
itself — query it with `python3 knowledge/kb.py sql "SELECT note, url, fetched FROM source"`,
which is rebuilt from the files and cannot drift from them. A backfill of the missing 112 rows
was deliberately not done: each row needs Type, Status and Feeds-into, which is authoring, not
transcription, and it would produce a second register to keep in sync with the first.

Status column: `verified` (read in full, cross-checked), `partial` (relevant sections read),
`secondary` (news/blog, used for verification only).

| Date | Source | Type | Status | Feeds into |
| --- | --- | --- | --- | --- |
| 2026-08-27 | https://code.claude.com/docs/en/skills | Official docs | verified | skill-anatomy |
| 2026-08-27 | obra/superpowers `skills/writing-skills/SKILL.md` @ b36e082 | Community (high quality) | verified | skill-authoring-best-practices |
| 2026-08-27 | obra/superpowers `skills/writing-skills/anthropic-best-practices.md` @ b36e082 | Mirror of official authoring guide | verified | skill-authoring-best-practices |
| 2026-08-27 | affaan-m/ECC `skills/token-budget-advisor/SKILL.md` @ be2a406* | Community | verified | long-text-comprehension |
| 2026-08-27 | affaan-m/ECC `.agents/skills/documentation-lookup/SKILL.md` | Community | verified | research-methodology |
| 2026-08-27 | affaan-m/ECC `.agents/skills/deep-research/SKILL.md` | Community | verified | research-methodology |
| 2026-08-27 | obra/superpowers `skills/writing-skills/testing-skills-with-subagents.md` @ b36e082 | Community (high quality) | verified | testing-skills-methodology |
| 2026-08-27 | https://code.claude.com/docs/en/features-overview | Official docs | verified | claude-code-extension-layer |
| 2026-08-27 | https://code.claude.com/docs/en/memory | Official docs | verified | claude-md-and-memory |
| 2026-08-27 | https://code.claude.com/docs/en/sub-agents | Official docs | verified | subagents |
| 2026-08-27 | https://code.claude.com/docs/en/workflows | Official docs | verified | dynamic-workflows |
| 2026-08-27 | https://code.claude.com/docs/en/mcp | Official docs | verified | mcp |
| 2026-08-27 | https://code.claude.com/docs/en/hooks-guide + /docs/en/hooks | Official docs | verified | hooks |
| 2026-08-27 | https://code.claude.com/docs/en/plugins + /docs/en/plugin-marketplaces | Official docs | verified | plugins-and-marketplaces |
| 2026-08-27 | https://github.com/safishamsi/graphify + PyPI graphifyy | Tool repo | verified | graphify-assessment |
| 2026-08-27 | https://stevescargall.com/blog/2026/05/graphify--memmachine-79-token-reduction-zero-vector-database/ | Independent benchmark | verified | graphify-assessment |
| 2026-08-27 | https://decodeclaude.com/ultrathink-deprecated/ | Blog | secondary | long-text-comprehension |
| 2026-08-27 | anthropics/claude-code issue #19098 | GitHub issue | secondary | long-text-comprehension |
| 2026-08-27 | Snyk ToxicSkills audit (Feb 2026, via search) | Security report | secondary | security gate (README) |

| 2026-09-02 | https://www.primeintellect.ai/blog/prime-agent | Vendor blog (primary) | verified | harness-over-model-prime-agent |
| 2026-09-02 | claude.com, supabase.com, vercel.com, clerk.com, stripe.com, resend.com, posthog.com, sentry.io, upstash.com, pinecone.io — /pricing | Vendor pricing pages | verified | production-site-checklist (startup stack) |

| 2026-09-02 | https://github.com/Alishahryar1/free-claude-code | Tool repo | partial (README) | model-agnostic-agent-harnesses, claude-code-ecosystem-plugins |
| 2026-09-02 | https://ornith.ai/ornith_1_5.html | Vendor blog (primary) | verified | model-agnostic-agent-harnesses |
| 2026-09-02 | https://code.claude.com/docs/en/llm-gateway (re-read) | Official docs | verified | model-agnostic-agent-harnesses |

\* ECC commit hash refers to the shallow clone taken 2026-08-27.

Local clones (working material, not committed here):
- `/home/user/obra/superpowers` @ b36e082
- `/home/user/composiohq/awesome-claude-skills` @ be2a406
- `/home/user/affaan-m/ECC`

Added 2026-09-02 (token economy / routing):
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching — floors, multipliers, breakpoints, availability (fetched 2026-09-02)
- https://platform.claude.com/docs/en/about-claude/pricing — list prices, Batch, tokenizer note (fetched 2026-09-02)
- https://docs.ollama.com/api/anthropic-compatibility — endpoint, env vars, unsupported features (fetched 2026-09-02)
- https://openrouter.ai/docs/api-reference/limits — free-model rate limits (fetched 2026-09-02)
- https://code.claude.com/docs/en/llm-gateway and /llm-gateway-protocol — unsupported non-Claude routing, subscription rule, forwarding requirements (fetched 2026-09-02)

Added 2026-09-02 (LLM wiki implementations):
- https://github.com/Astro-Han/karpathy-llm-wiki and its SKILL.md — MIT, 2.1k stars; layout, page fields, three lint tiers (fetched 2026-09-02) → llm-wiki-pattern
- https://github.com/kfchou/wiki-skills — MIT; six skills, pre-commit hook, contradiction script (fetched 2026-09-02) → llm-wiki-pattern
- https://github.com/toolboxmd/karpathy-wiki — MIT; session hook, CLI, tier-1 lint at every ingest (fetched 2026-09-02) → llm-wiki-pattern


Added 2026-09-04 (graphify → Obsidian, from a forwarded carousel):
- Instagram carousel, @divyannshisharma, 16 of 20 slides received as screenshots 2026-09-04 — the doc-corpus → vault route end to end; all its numbers graded REPEATED → `knowledge/VAULT.md`, raw at `knowledge/raw/instagram-graphify-obsidian-2026-09-04/`
- https://raw.githubusercontent.com/safishamsi/graphify/v8/README.md (fetched 2026-09-04) — the two command surfaces, `--obsidian` / `--obsidian-dir`, `--watch` → graphify-features, graphify-assessment
- https://raw.githubusercontent.com/safishamsi/graphify/main/README.md (fetched 2026-09-04) — the default branch is a v1-era README; v9/v10 are 404; `Graphify-Labs` and `safishamsi` serve byte-identical `main` → graphify-features

Added 2026-09-04 (re-fetch of the Claude Code mechanics set, raw kept at `knowledge/raw/claude-code-docs-2026-09-04/`):
- https://code.claude.com/docs/en/{skills,sub-agents,mcp,hooks-guide,hooks,plugins,plugin-marketplaces,features-overview} (fetched 2026-09-04) — every version-tied value in the six notes re-verified; none had changed; four additions folded into `subagents` → skill-anatomy, subagents, mcp, hooks, plugins-and-marketplaces, claude-code-extension-layer

Added 2026-09-04b (the same eight pages, re-fetched hours later after `watch.py` flagged them):
- https://code.claude.com/docs/en/{skills,sub-agents,mcp,hooks} (fetched 2026-09-04, second run) — four pages changed within hours: nested `.claude/skills/` do not load at startup and `/add-dir` loads them early (v2.1.257+), `/skill-doctor` measures per-skill context cost and invocation count, `--append-subagent-system-prompt-file` (v2.1.261+), removing a remote MCP server deletes its OAuth tokens → skill-anatomy, subagents, mcp

Added 2026-09-08b (the watcher's second batch, raw kept at `knowledge/raw/watch-2026-09-08b/`):
- https://code.claude.com/docs/en/{model-config,llm-gateway-protocol} (fetched 2026-09-08) — one theme across both: a pinned or discovered model's picker row now shows the **model's name** when Claude Code *recognises* the id (`us.anthropic.claude-sonnet-4-5-20250929-v1:0` reads `Sonnet 4.5`; `my-gateway-claude-sonnet-4-6` reads `Sonnet 4.6`) and the raw id when it does not, never on Microsoft Foundry; `display_name` is used only when it differs from the id; the `availableModels` guidance dropped "list the same provider-form ID the picker shows". The discovery id filter (`claude`/`anthropic` anywhere, case-insensitive; began-with before v2.1.223) is **unchanged and re-verified** → model-routing-free-and-local §9
- https://code.claude.com/docs/en/skills.md (fetched 2026-09-08) — one sentence added to the `/skill-doctor` report: "Of the skills it tells you where to turn off, start with the ones that have the highest context cost." First-party guidance to act on the cost ranking; this repo's drop-only-on-failed-tests rule holds, and now says why → skill-anatomy
- https://code.claude.com/docs/en/hooks.md (fetched 2026-09-08) — a link target moved (`/docs/en/settings#available-settings` → `/docs/en/settings-reference#wslinheritswindowssettings`). **No claim touched**, checked rather than assumed: no note in this base cites `/docs/en/settings`. Row re-baselined so the next real change is not buried under this one
- Four further rows reported CHANGED with **zero words changed** (claude.com/customers/block, augmentcode's graphify page, both unsloth glm-5.3 pages) and a fifth appeared between two runs (goose-docs providers). All transport: Webflow republish stamps, Vercel `?dpl=` deploy ids, GitBook asset hashes, a Docusaurus runtime bundle hash. No note owed anything → `watch.py` now reports these as `noise` rather than `CHANGED`

Added 2026-09-11 (the third watch batch and the ingest pass it queued, raw at `knowledge/raw/watch-2026-09-11/`):
- https://docs.z.ai/guides/overview/pricing (fetched 2026-09-11) — **GLM-5.3-Flash doubled.** The 50% launch discount expired on the date its own page named (*"The promotion ends at 24:00 on September 9, 2026"*); Flash is now **$0.15 / $0.03 / $0.50**, was $0.075 / $0.015 / $0.25. GLM-5.3 and GLM-5.2 unchanged at $1.4 / $0.26 / $4.4 → glm-5.3-local, model-routing-free-and-local
- https://code.claude.com/docs/en/{skills,hooks,memory,model-config,llm-gateway-protocol,sub-agents,mcp,workflows,plugins,plugin-marketplaces} (fetched 2026-09-11) — 408 added lines over ten pages, read by four concurrent readers. **Four notes were false:** workflow runs *do* resume across sessions from `~/.claude/projects/`; `managedMcpServers` outranks the whole MCP precedence chain (v2.1.259+); `/reload-plugins` does not apply plugin-MCP changes in a non-interactive session; and the pinned highest-version figure was stale for the third time and is now deleted rather than updated. **Behaviour changes nobody had recorded either side of:** the gateway token-count fallback became a character-based estimate; a subagent can no longer escalate to `bypassPermissions` (v2.1.267); `disallowedTools` with a specifier removes the whole tool; `mcp_tool` hooks are skipped rather than errored before MCP is up; `SessionStart` re-fires and can have its output discarded; `stopReason` is model-visible; a classifier-blocked `agent()` resolves to `null`; `opts.schema` gets a pre-flight check and five retries; the 1M window really compacts at **~967K**; and `context: fork` is explicitly *not* a conversation fork → subagents, mcp, dynamic-workflows, plugins-and-marketplaces, hooks, skill-anatomy, model-routing-free-and-local §10, token-economy-playbook
- https://raw.githubusercontent.com/garrytan/gbrain/HEAD/README.md (fetched 2026-09-11) — the README was repositioned and the sentence this base quotes verbatim ("100+ operations exposed as MCP tools") **no longer exists**; the page now states no tool count at all, while neighbouring claims survive. The claim stays MEASURED against held bytes and is dated to them → temporal-kg-agent-memory
- https://raw.githubusercontent.com/NanoNets/Graft/HEAD/README.md (fetched 2026-09-11) — every controlled figure survives (42% / 46% / 60%, 162 runs); the raw SWE-bench pair `33/50 vs 27/50` is gone, replaced by "66% (+12 pts)" and "+22% more instances resolved". Arithmetically identical, and the denominator stopped being shown → claude-code-ecosystem-plugins
- PyPI release indexes (fetched 2026-09-11) — `graphiti-core` 0.30.1 → **0.30.2**, `graphifyy` 0.9.56 → **0.9.58**. Neither moves a finding; both are re-dated so a stale MEASURED figure does not teach a reader to distrust the ones that matter → temporal-kg-agent-memory, graphify-assessment, graphify-features
- **Deliberately still CHANGED and unread:** `claude-code-router` (v3.0.22 → v3.1.0), `claude.com/customers/block`, OmniRoute, OpenMAIC, agency-agents, claude-mem. Re-baselining a row without reading its notes turns an honest backlog into a silent one
- https://code.claude.com/docs/en/plugin-evals.md (fetched 2026-09-11, **new watched source, 97 rows**) — `claude plugin eval` shipped (the page names **v2.1.269**): runs a suite, judge-scored graders, **compares against a no-plugin baseline** ("the with-arm and the without-arm"), gates CI on the score, and `init` proposes the cases. **Our standing caveat survives, which is the finding:** the page states *"Its case format is separate from the `evals/evals.json` file the skill-creator plugin uses"* — a suite is `evals/` with one subdirectory per case. So Anthropic now ships **three** eval formats for skills and a runner for exactly one of them, and *"There is not currently a built-in way to run these evaluations"* remains true of the other two. It also spends real money: eval runs and `init` "count against your plan's usage limits or your API bill" → anthropic-skill-authoring-contract, skill-authoring-best-practices

Added 2026-09-11 (the fourth watch batch, raw at `knowledge/raw/watch-2026-09-11b/`; and eight PDF primaries at `knowledge/raw/pdf-sources-2026-09-11/`):
- https://code.claude.com/docs/en/sub-agents.md (re-fetched 2026-09-11, **second time that day**) — the subagent tool pool is **not purely subtractive**: *"On macOS, Linux, and WSL, a subagent can also receive the Glob and Grep tools when the main conversation doesn't have them."* Platform-conditional and in the WIDENING direction, so a mental model of "inherit, then remove" predicts the wrong tool list → subagents
- https://code.claude.com/docs/en/hooks-guide.md (re-fetched 2026-09-11, **second time that day**) — a fourth silent failure: *"When your hook returns `permissionDecision` or `additionalContext` at the top level instead of inside `hookSpecificOutput`, the JSON still parses, and Claude Code ignores the misplaced fields without reporting an error."* A hook denying a tool call with the field one level too high is indistinguishable from one that allowed it. Visible only via `claude --debug` and the string `Hook JSON output had unrecognized keys`. Second cause: anything on stdout before the JSON (an `echo` in a shell profile) breaks parsing → hooks
- **Eight PDF primaries held for the first time** — the Anthropic skills guide, Boehm & Basili 2001, Kim et al. 2014 and five arXiv papers. Four notes cited PDF sources and **not one was held** (read 2026-08-29, before the raw layer existed). Read here by `knowledge/pdftext.py`, stdlib-only: **five at 100.0%**, three refuse (0.0%, 0.0%, 17.6% — CID-encoded, needing ToUnicode CMaps this environment cannot parse). `requirements-discovery` was re-verified against its two: **5 claims checked, 5 confirmed verbatim** → requirements-discovery, llm-idea-generation, skill-anatomy, anthropic-skill-authoring-contract, agent-builder-prior-art, long-document-ocr
- https://code.claude.com/docs/en/plugin-evals.md (re-fetched 2026-09-11, **second time that day**) — **the cost formula doubled when it was spelled out**: *"a suite makes roughly cases × runs agent runs with the plugin and as many again for the no-plugin baseline, plus three short judge calls per `llm` or `baseline` grader per run"* (was the undefined *"cases × runs × arms"*). And **an `llm` judge does not see the whole transcript**: *"A `regex` grader sees every message; an `llm` judge sees the first 12 and the last 12."* Past 24 messages the judge is blind to the middle and its verdict does not say so → anthropic-skill-authoring-contract
- https://raw.githubusercontent.com/PrimeIntellect-ai/prime-agent/HEAD/README.md (re-fetched 2026-09-12) — **a vendor narrowing a security property it had implied.** Was *"downloads a versioned release, verifies its SHA-256 checksum"*; now *"requires HTTPS for release downloads... The checksum detects corruption or an inconsistent transfer; because the inventory and archive come from the same origin, HTTPS is the authenticity boundary."* The install line gained `--proto '=https' --proto-redir '=https'`, refusing a redirect to plaintext. **This base had already written that argument for graphify, from the code, weeks earlier** — a vendor publishing the identical distinction is the strongest confirmation it generalises → harness-over-model-prime-agent, graphify-assessment

Added 2026-09-12 (raw at `knowledge/raw/watch-2026-09-12/`):
- https://raw.githubusercontent.com/MakazhanAlpamys/Soup/HEAD/README.md (re-fetched 2026-09-12) — the diff replaced the **v0.74.0** release block with **v0.75.0**, so v0.74's measured figures had been in the 2026-09-11 baseline and were never read in; a blind re-baseline would have destroyed them. **Both now recorded.** v0.75.0 fixes, in one release, THREE cases of a setting accepted then silently ignored: an unknown config key *"dropped while the run proceeded with the setting not applied"* (now refuses the load, breaking and telegraphed one release ahead); six training options *"each validated and then dropped on `backend: mlx`"*, with 24 of 32 optimizer names now **refused by name** rather than silently becoming AdamW; and validation loss *"computed on every backend and thrown away"*. Also `grpo_variant: gspo` → arXiv:2507.18071, with existing configs no longer reproducing prior runs. v0.74.0's measured numbers kept: fp32 upcast of the frozen base, **48,241 → 18,658 MiB peak, 2.59×**, and four SSRF bypasses by alternate IPv4 spellings → local-finetuning-layer-streaming

