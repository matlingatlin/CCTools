---
title: Agent harness principles, 2026 — what the practitioner canon says the harness owns, and what is measured
sources:
  - url: https://raw.githubusercontent.com/humanlayer/12-factor-agents/main/README.md
    note: "12-Factor Agents (HumanLayer). Twelve factor titles read from the README's own list; the four-step loop quoted verbatim. Raw: knowledge/raw/web-2026-09-03-harness-and-evidence/12-factor-agents-README.md"
    fetched: 2026-09-03
  - url: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
    note: "Published Nov 26, 2025. Initializer agent + coding agent; init.sh, claude-progress.txt, feature_list.json; the one-shot failure. No numbers. Raw: anthropic-effective-harnesses-long-running.html"
    fetched: 2026-09-03
  - url: https://addyosmani.com/blog/agent-harness-engineering/
    note: "April 19, 2026. Definition, the ratchet rule for AGENTS.md, the 60-line figure (HumanLayer's), the Terminal Bench 2.0 claim attributed to two third-party write-ups and carried without numbers. Raw: osmani-agent-harness-engineering.html"
    fetched: 2026-09-03
  - url: https://www.infoq.com/articles/agentic-fitness-functions-evolutionary-architecture/
    note: "Deterministic versus agentic fitness functions; the two sentences quoted below. Article publication date not located in the raw (only event dates); fetched 2026-09-03. Raw: infoq-agentic-fitness-functions.html"
    fetched: 2026-09-03
  - url: https://arxiv.org/abs/2604.18071
    note: "Hu Wei, submitted 20 Apr 2026. 70 projects, five design dimensions. Abstract only. Raw: arxiv-2604.18071-abs.html"
    fetched: 2026-09-03
  - url: https://arxiv.org/abs/2606.20631
    note: "Boming Xia et al., submitted 29 May 2026. Ten patterns (five core, five supporting), four responsibility layers, 8 systems. Abstract only. Raw: arxiv-2606.20631-abs.html"
    fetched: 2026-09-03
status: verified
tags: [harness, agents, architecture, fitness-functions, skills, hooks, context, principles, 2026]
related: ["[[effective-agents-anthropic]]", "[[managed-agents-architecture]]", "[[loop-engineering-and-fable-prompting]]", "[[harness-over-model-prime-agent]]", "[[architecture-evidence]]", "[[agent-builder-prior-art]]", "[[build-evidence-tooling-2026]]", "[[evidence-artefact-schemas-2026-09]]", "[[subagents]]", "[[hooks]]", "[[claude-agent-sdk-hosting-and-limits-2026-09]]"]
---

# Agent harness principles, 2026

Written 2026-09-03 for Scio's architecture pass (ADR-0005, the five-layer form), to answer:
*what does the 2026 practitioner canon say a harness owns, and which of it is measured?* Six
sources; one number among them is a corpus count, the rest are guidance. The vendor's own
architecture note is [[managed-agents-architecture]]; the vendor's workflow patterns are
[[effective-agents-anthropic]]. This note holds what those two do not.

## Claims

| # | Claim | Source | Locator | Verbatim | Verdict |
|---|---|---|---|---|---|
| 1 | The agent loop has one model decision and three deterministic steps | 12-Factor Agents README | "Agents as loops" | "1. LLM determines the next step in the workflow, outputting structured json (\"tool calling\") 2. Deterministic code executes the tool call 3. The result is appended to the context window 4. Repeat until the next step is determined to be \"done\"" | REPEATED — a design statement, no measurement |
| 2 | The twelve factors | same | "The Short Version" list | Factor 1 Natural Language to Tool Calls · 2 Own your prompts · 3 Own your context window · 4 Tools are just structured outputs · 5 Unify execution state and business state · 6 Launch/Pause/Resume with simple APIs · 7 Contact humans with tool calls · 8 Own your control flow · 9 Compact Errors into Context Window · 10 Small, Focused Agents · 11 Trigger from anywhere, meet users where they are · 12 Make your agent a stateless reducer | REPEATED (titles verbatim from the README list) |
| 3 | Long-running work is two agents: an initializer and an incremental coder, bridged by files | Anthropic, long-running harnesses | body | "an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session" | REPEATED — engineering guidance from one internal prototype; no numbers in the post |
| 4 | The bridging artefacts are a setup script, a progress log and a structured feature list | same | body | "an init.sh script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git commit"; the session transcript shows `read - feature_list.json` | REPEATED |
| 5 | The named failure is one-shotting | same | body | "the agent tended to try to do too much at once—essentially to attempt to one-shot the app" | REPEATED |
| 6 | Harness = model + everything around it | Osmani | opening line | "A coding agent is the model plus everything you build around it." | REPEATED |
| 7 | Every steering line must trace to a failure | Osmani | body | "Every line in a good AGENTS.md should be traceable back to a specific thing that went wrong." | REPEATED |
| 8 | Keep the steering file short; HumanLayer's is under 60 lines | Osmani | body | "HumanLayer keeps theirs under 60 lines." | REPEATED (a second-hand count) |
| 9 | The same model scores lower in Claude Code than in a custom harness on Terminal Bench 2.0 | Osmani, citing two third-party write-ups | body | "On Terminal Bench 2.0, Claude Opus 4.6 running inside Claude Code scores far lower than the same model running in a custom harness." | REPEATED — no score given; the underlying write-ups were not fetched; the "Top 30 to Top 5" phrase in a search summary was not located in the raw and is not taken |
| 10 | Deterministic checks first; model judgement only for evidence-bound but judgement-heavy risk | InfoQ | body | "Deterministic fitness functions should remain the primary enforcement mechanism for measurable invariants such as dependency direction, contract shape, latency budgets, security posture, and policy checks. Agentic fitness functions add value when architectural risk is evidence-bound but judgement-heavy, such as boundary fidelity, semantic contract drift, workflow…" | REPEATED — a position piece; no measurement |
| 11 | A 70-project corpus shows five recurring harness decision dimensions | arXiv 2604.18071 | abstract | "a protocol-guided, source-grounded empirical study of 70 publicly available agent-system projects"; "five recurring design dimensions (subagent architecture, context management, tool systems, safety mechanisms, and orchestration)"; "the corpus favors file-persistent, hybrid, and hierarchical context strategies" | MEASURED as a corpus count; descriptive of what was built, not of what worked |
| 12 | Skill harnessing has a four-layer reference architecture | arXiv 2606.20631 | abstract | "ten empirically grounded architectural patterns (five core, five supporting)"; "four responsibility layers: Supply Chain, Mediation, Execution Control, and Evidence & Feedback"; "cross-instantiation across 8 selected systems" | REPEATED at abstract level — the pattern names and the per-system evidence are in the PDF, not fetched |

## What it means here

- **The deterministic-first doctrine has independent restatements in three genres** — a
  manifesto (claim 1, 10 of the 12 factors are about what the code owns), a vendor post
  (claims 3–5: the harness owns files and the feature list, the model owns the increment), and
  an architecture-governance article (claim 10). None measures it. Scio's own record is the
  only place it is measured at all, and there it is measured negatively (the predecessor's
  compute-and-drop habit). Treat the doctrine as a design commitment with the vendor's
  weight behind it, not as a finding.
- **The four-layer skill architecture (claim 12) is a map for Scio's talent placement.**
  Supply Chain = where a skill comes from (the allow-listed registries and the four gates);
  Mediation = which skills a build gets (`Contract`-selected allow-list, model never chooses);
  Execution Control = hooks that deny and stop; Evidence & Feedback = the evidence report and
  the per-skill measurement. ADR-0008's three levels are a different cut of the same
  responsibilities; the paper supplies the vocabulary, not a verdict.
- **Claim 9 is the one that would change a decision if it were measured** — a harness that
  loses points against the same model elsewhere argues for owning the loop (ADR-0004's
  "how we will know it was wrong"). It is carried at second hand without a number and cannot
  move anything yet.
- **Claims 7–8 are a rule for Scio's generated `CLAUDE.md` (level 3):** every line earned by a
  failure the build observed, and a length ceiling in lines, not prose. The
  `steering-doc-pruning` talent already encodes the cadence; the 60-line figure is a
  reference point, not a target.

## What is open

- Terminal Bench 2.0 scores (claim 9): the two write-ups Osmani cites were not fetched.
- The ten skill-harnessing patterns by name (claim 12): PDF not read.
- 12-Factor's "Factor 13: pre-fetch context" appears in a search-result summary and not in the
  README's twelve-item list; not taken.
- The InfoQ article's publication date: not located in the raw.

## Added 2026-09-03 (later the same day)
The vendor harness these principles are applied to in Scio — its options, hook events, subagent caps and isolation settings at version 0.3.259 — is [[claude-agent-sdk-hosting-and-limits-2026-09]].

## Added 2026-09-06
The artefact side of "a gate emits one standard file" is now measured: [[evidence-artefact-schemas-2026-09]] records the required fields and enums of CTRF, SARIF, the in-toto Statement and SLSA provenance.
