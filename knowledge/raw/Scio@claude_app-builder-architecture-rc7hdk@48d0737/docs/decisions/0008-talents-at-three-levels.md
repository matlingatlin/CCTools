# ADR-0008 · Talents at three levels: guarantees as hooks, boundaries as subagents, advice as skills

**Status:** Proposed
**Date:** 2026-09-02
**Layer:** C (build) and D (ship) per ADR-0005; cross-cutting for level 1
**Supersedes / relates to:** relates to ADR-0001 (graph in every repo), ADR-0004 (buy the harness), ADR-0006 (slices); extends `docs/SKILLS-LIBRARY.md`

## Context

Talents — skills, subagents, hooks, MCP servers, plugins — have two addressees in this project's
own rules: the build process and the product. `docs/SKILLS-LIBRARY.md` (2026-08-26) sharpened that
to three levels: build-time, generation-time, delivered. It also measured that the Playbook Layer B
ships into every build prompt is a skills library with one entry, byte-identical for a booking app
and a tender platform.

The predecessor implemented its generation-time talents by hand: a relay, a provider abstraction,
an untrusted-text fence, reply chunking, an instrumentation verifier with rollback, a console
classifier, a critic. Under ADR-0004 the build loop runs on the Claude Agent SDK, and Anthropic's
documentation fetched 2026-09-02 shows the SDK offers each of those as a first-class kind:
`PreToolUse` hooks that deny, rewrite or defer a tool call before it runs; `PostToolUse` hooks that
replace a tool's output; subagents with a tool subset, their own model, `maxTurns`, preloaded
skills and structurally isolated context; a per-session `skills` allow-list; `maxBudgetUsd`.

The distinction that decides placement: a hook runs code without the model's consent, a subagent
cannot see what it was not handed, a skill is advice the model may follow.

## Decision

Talents are placed by kind at each level, per `docs/TALENTS-THREE-LEVELS-2026-09-02.md`:

- **A guarantee is a hook.** Instrumentation guard, package stamp, file-plan fence, secret sink,
  spend ceiling checked before the call, render-boundary neutralisation, console classification,
  the stop rule and command trust are hooks on the build session. A hook reports what it examined;
  one that did not fire is a missing row in the evidence report, never a pass.
- **A boundary is a subagent.** Package builder, critic, security reviewer, interaction runner and
  spec writer are subagents with tool subsets; the critic and the security reviewer cannot edit.
- **Advice is a skill, selected not constant.** The Playbook splits into a fixed core and entries
  selected per build by Layer D's `Contract` test over the spec's app-kind, roles, sensitivity and
  integrations, passed as the query's `skills` allow-list. The model never chooses the list.
- **Deterministic functions stay code.** The intake gate, the validation rules, Kahn ordering,
  `Contract` matching, the criteria model, the size classifier and the evidence report are called
  by the harness between turns and are not talents.
- **Level 3 ships with the app.** The foundation package emits the graph and its hooks (ADR-0001),
  the app's `CLAUDE.md`, its ADRs, its evidence, the stack skill level 2 used, test and lint hooks,
  and for a model-bearing app its eval suite. Slice 1 ships the first four; the rest follow the
  order `SKILLS-LIBRARY.md` fixed.
- **Every level-2 skill is re-measured on the model it will run on before it is selected.** Anthropic's
  Fable 5 prompting page (skills-repo note `loop-engineering-and-fable-prompting`, verified 2026-09-02):
  *"Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade
  output quality."* Scio's 27 and skills-repo's 85 were written and measured on Opus. `skill-measure`'s
  baseline-versus-with arms are the instrument; a with-arm that loses to the bare arm on Fable is a
  skill that has become a cost and is not selected. The same page's *"separate, fresh-context verifier
  subagents tend to outperform self-critique"* is the vendor's statement of the critic rule above.
- **A hook's stop rule is a gates file, not prose.** Per unlazy (MIT; skills-repo note
  `claude-code-ecosystem-plugins`): one line per gate with the command, the expected marker and the
  evidence line; "pending" is unmet; the `Stop` hook returns `block` while any gate is unmet. That is
  `verification-before-completion` in a shape a hook can read.
- **Scaffolding has an expiry.** Gates and playbook lines added for a model's weakness are reviewed
  when the model changes (LOOPS.md rule 8, attribution unverified, the rule itself sound); a gate that
  no longer fires on the bare arm is deleted, not kept.
- **Level 1 gains one hook and one mechanism.** The agent cap becomes a `SubagentStart` hook that
  denies past `W_MAX_AGENTS`; Scio's skills reach the build repo as a SHA-pinned plugin.

## Alternatives considered

| Alternative | Why it lost |
|---|---|
| Keep the predecessor's hand-built mechanisms and port them | Rebuilds, in TypeScript, what the harness now provides with tests and a maintainer; and keeps the "guarantee in a prompt" shape for the fence and the critic |
| Express the gates as skills ("always run the secret scan") | A skill is advice; the predecessor's own docstring says the gate must be "impossible for a model to talk its way past" |
| One agent with everything preloaded | Self-review measured negative, separation measured positive (predecessor ADR-0021's sources); and a critic that can edit will edit |
| A constant Playbook, larger | The measured problem is that it is constant, not that it is small |
| Ship level 3 in Slice 1 in full | `SKILLS-LIBRARY.md` puts it last for a reason: it needs measured level-2 skills to be worth shipping |

## Consequences

**What this buys.** The deterministic-first doctrine stops being five independent implementations
and becomes one placement rule the harness enforces. The build's evidence gains a row per hook.
The delivered repository arrives knowing how to extend itself.

**What it costs.** Re-measuring every candidate skill on Fable before Slice 1 selects any. Hooks are code Scio owns and tests; each is a small program with the failure
modes `validation-evidence` lists. The skill library inherits the consent, drift and duplicate
problems `SKILLS-LIBRARY.md` records, and must run its index check as a gate.

**What it forecloses.** Running Scio's build loop on a harness without hooks and isolated
subagents; Managed Agents is re-tested against this list when it leaves beta.

## How we will know it was wrong

A guarantee placed in a hook is bypassed by a tool path the matcher did not cover; a subagent
boundary leaks through the Agent prompt; or the selected Playbook measurably does no better than
the constant one on the same eval — which would mean the library's second entry was the wrong one,
not that the placement rule was.
