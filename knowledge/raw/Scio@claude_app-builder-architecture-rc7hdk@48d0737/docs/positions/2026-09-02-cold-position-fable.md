# Cold position — what I would build, before reading the history

**Status:** cold. Written 2026-09-02 before opening `docs/as-built/`, `docs/next/`, the reviews,
or the predecessor. Inputs seen so far: `CLAUDE.md`, the `run` skill, the finding counts per layer
(no finding text), and the user's one-paragraph brief. Weigh accordingly.

## The problem, restated

Two customers, one artefact. A person who cannot write software describes what they want. A
developer who did not write it opens the result and is impressed. The second customer is the
differentiator: Lovable-class tools already satisfy the first. "Impressed" for a developer means:
the structure is one they would have chosen, the tests can fail, the types are honest, the data
model is sane, secrets and tenancy are handled, there are no placeholders, and the README explains
why things are where they are.

## Ten positions

1. **The product is a spec-to-verified-software pipeline, not a code generator.** Every build
   ships with evidence: tests shown capable of failing, typecheck, lint, an accessibility pass, a
   security pass, and a written architecture. Developers trust evidence, not prose. The evidence
   report is the product surface that makes a developer say "this is well built".

2. **Deterministic where possible, model where necessary.** Project layout, tooling config, CI,
   auth wiring, database conventions, migrations scaffolding, deployment — all generated from
   templates and generators, never by a model. The model fills domain logic inside a fixed
   skeleton. Professional quality has to be *repeatable*; a model cannot be made repeatable, a
   generator can.

3. **One opinionated target stack, deep not broad.** Pick one stack for generated apps and go
   deep: one framework, one database, one auth pattern, one component system. Breadth is what
   makes generated output shallow. Developers are impressed by depth in a stack they know.

4. **The spec is the contract.** Intake produces a structured spec — roles, entities, screens,
   flows, rules, non-goals — that the user confirms in plain language. The build is checked
   against the spec, not against the prompt. Anything the user did not say is marked as inferred
   and shown as such.

5. **Build is an agent loop in a sandbox with real tools**, not one-shot generation: run the
   tests, run the typecheck, open the app in a browser, read the errors, fix, stop under a written
   stop rule and a written budget. The loop's stop rule and budget are product decisions, written
   down, not tuning knobs.

6. **Ownership means a repository.** The output is a GitHub repository the user owns, with CI
   green and a deploy, from the first build. Not a preview in our tool. The repo *is* the product.

7. **Do not rebuild the agent harness.** The rebuild's biggest lever is to not re-implement what
   Claude Code / the Agent SDK already does: tool loop, sandboxing, subagents, skills, hooks. Scio
   is the wrapper — intake, spec, library, gates, evidence, UI — over a harness someone else
   maintains. The predecessor's size (26k lines) is a hint that it built plumbing it should have
   bought.

8. **The component library is a curated registry in a standard format, not a garden.** Use the
   registry standard the ecosystem already uses; curate entries, do not invent a catalogue
   format. Matching is deterministic and index-then-verify.

9. **Scio's own code should be small.** Excluding templates and skills, a rebuild that follows 2
   and 7 should land well under 10k lines. If it is heading past that, something is being rebuilt
   that should have been bought or templated.

10. **Build Scio with the talents.** Scio's own 27 skills are governance (what a gate may say,
    when a loop stops, what a spec field may be). The general talents are method (brainstorm,
    TDD, verification-before-completion, eval-harness). Use the second to build under the first.
    The failure mode to avoid is a talent library nobody invokes.

## What I expect to be wrong about

- Position 3 may be too narrow if the product has to target several app kinds (mobile, API-only).
- Position 7 assumes the Agent SDK is fit for a multi-tenant hosted product; that is a scan item,
  not a fact.
- Position 9 is a guess from the brief; the as-built documents will show what those 26k lines
  actually pay for.

## What this position does not decide

Stack names, model names, prices, layer count. Those are looked up and dated, then proposed as
ADRs — never taken from memory.
