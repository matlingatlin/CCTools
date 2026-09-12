# The routing evals — what they assert, and why they cannot run in this repository

Five cases, each a prompt plus one or more graders of `type: tool_used` over the `Skill` tool.
They test **routing**: whether the right unit fires on a request that never names it.

| case | asserts |
|---|---|
| `routing-budget-will-not-cover-plan` | `budget-cut-triage` fires |
| `routing-green-after-loosening` | `oracle-weakening-audit` fires |
| `routing-edit-an-existing-skill` | `skill-description-optimizer` fires **and** `writing-skills` does not |
| `control-skill-named-explicitly` | `budget-cut-triage` fires when the prompt names it (the control) |
| `negative-plain-factual-question` | **no** skill fires on "In which year was the Treaty of Westphalia signed?" |

## They are inert here, and that is the point

Four of the five name a specific skill and pass only if that skill **fires**. Firing requires the
skill to be installed under a project's `.claude/skills/`, and nothing in this repository is:
the library sits in `library/`, which is not an activation path, and the plugin manifest that
made this directory a runnable eval suite is archived at `docs/steering/plugin-json-archived.json`
rather than at `.claude-plugin/plugin.json`.

So run against this repository as it stands, the four positive cases would fail and
`negative-plain-factual-question` would pass **for the wrong reason** — nothing fires because
nothing exists, not because routing declined. A green negative case next to four reds is exactly
the shape that reads as "mostly working"; it is worth naming before someone runs it.

They are kept, and deliberately not deleted or weakened. The sole removal criterion for a test is
that the unit under test cannot beat baseline; "the harness is not wired up in the repository that
stores it" is not that. Weakening the graders so they pass here would buy a green suite by
removing the assertion, which is the defect `oracle-weakening-audit` — itself one of the units
under test — exists to catch.

## To run them

1. Install the units the cases name under the project's `.claude/skills/`:
   `budget-cut-triage`, `oracle-weakening-audit`, `skill-description-optimizer`, `writing-skills`.
   `negative-plain-factual-question` is only meaningful with a **full** library installed — its
   claim is that none of ~89 descriptions grabs a plain factual question, and with four installed
   it proves nothing.
2. Restore the manifest to `.claude-plugin/plugin.json`; its `experimental.evals` key points here.
3. Run the suite from that project, not from this repository.
