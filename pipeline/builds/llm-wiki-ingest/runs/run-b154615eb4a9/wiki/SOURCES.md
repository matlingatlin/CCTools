# Source log

Every source consulted for the knowledge base. Status: `verified` (read in full,
cross-checked), `partial` (relevant sections read), `secondary` (news/blog, used
for verification only).

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
  - **Re-read in full and kept raw, 2026-09-02**: `raw/2026-09-02-astro-han-karpathy-llm-wiki-SKILL.md`
    (md5 `60184773c75ed3693ce45a30c7227645`, 14342 bytes, 233 lines) → llm-wiki-pattern
    (grounding invariant, fidelity-of-form, no-material log key, parallel-search/serial-compile,
    cascade-past-the-index, archive and depth carve-outs) and research-methodology (cascade).
    The row above was written from the README plus a partial read; the "50K–100K tokens" and
    "no source hashes / vector search / MCP" quotes belong to the README, not to this file.
- https://github.com/kfchou/wiki-skills — MIT; six skills, pre-commit hook, contradiction script (fetched 2026-09-02) → llm-wiki-pattern
- https://github.com/toolboxmd/karpathy-wiki — MIT; session hook, CLI, tier-1 lint at every ingest (fetched 2026-09-02) → llm-wiki-pattern

