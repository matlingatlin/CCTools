# Ablation · `graphify`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

## This one cannot be measured by this ablation, and here is why

`graphify` is installed at **account level**, at `/root/.claude/skills/graphify/`. Account-level
skills load in every directory. The control arm is defined as *"no **project** skills"* — it strips
`/home/user/scio/.claude/skills/`, and it does not and cannot strip `~/.claude/skills/`. The user's
global `CLAUDE.md` also names the skill by path and instructs that `/graphify` route to it.

So `graphify` is present in **both** arms. A with/without comparison on it compares *with* against
*with*. The expected effect size is zero by construction, and any difference observed would be
noise or would belong to some other skill.

This confound is stated in all five files in this pass; here it is not a caveat, it is the result.

### Confirmed, not assumed

Run in the **control** directory:

> I want to be able to ask questions about how the pieces of this project connect to each other,
> rather than grepping around. How would you set that up here? Four bullets max.

The control answered, verbatim, opening line:

> This is exactly what the graphify skill and the existing `docs/as-built/graph/graph.json` are
> for — no need to design something new.

…and closed with *"Want me to run `/graphify` on this repo now to generate its graph?"* The control
arm named the skill, described its mechanism (*"a persistent knowledge graph with god nodes and
community detection"*, *"query/path/explain tools"*), and offered to invoke it. The skill is live in
the control. The ablation is void.

The treatment arm answered the same way and reached for the same tool, adding references to *other*
project skills (`graph-guard`, `run`, `as-built`) — which is a measurement of those skills, not of
this one.

## What was measured instead: what the vendored copy adds over the account-level one

The substitute measurement the brief asks for. It is not a model comparison — it is a file
comparison, and it is decisive.

```
md5  1656a8a8e4a05bbe69f32cd15de81e87  /root/.claude/skills/graphify/SKILL.md
md5  1656a8a8e4a05bbe69f32cd15de81e87  /home/user/scio/.claude/skills/graphify/SKILL.md
diff -rq  …/references  …/references   →  no differences
```

| | Account level | Vendored in `scio` |
|---|---|---|
| `SKILL.md` | 713 lines, 41,276 bytes | **byte-identical** |
| `references/` | 8 files | **byte-identical**, all 8 |
| version marker | `.graphify_version` → `0.9.50` | `VENDORED.md` → package `graphifyy` 0.9.50 |

**The vendored copy adds exactly one thing to the loaded skill surface: nothing.** Its only unique
file, `VENDORED.md`, is documentation *about* the vendoring — the package name, the pinned version,
the refresh command, and the record of the previous copy being 1,208 lines of stale and wrong API
(`check_semantic_cache` returning three values where the package returns four). That file is not
part of the skill's instructions; it is a provenance note for whoever refreshes it next.

So the honest statement of value is: **the vendored copy contributes no behaviour, and contributes
one real thing — a pin, and the standing rule that came out of the last drift** (*"a vendored skill
that drifts is worse than no skill, because it is trusted"*). That is a supply-chain artefact, not a
capability, and it cannot be ablated because there is nothing behavioural to remove.

Both copies were refreshed the same day (2026-08-26, `graphify install --platform claude`), which is
why they agree. The value of the vendored copy is realised only when they **stop** agreeing — when
the account-level install is upgraded and the project wants the pinned version. Today that value is
zero and measurable as zero; it is insurance, and insurance pays nothing while nothing goes wrong.

## Verdict

**Unmeasurable with this control** — `graphify` loads in both arms, so a with/without ablation on it
has no treatment condition. Recorded as unmeasurable rather than as a null, because a null result
implies a comparison was made.

**The vendored-versus-account comparison is measurable and returns no difference**: the two copies
are byte-identical, so the vendored copy changes no outcome today. It exists as a version pin.

No result is claimed either way about whether `graphify` is a good skill. This pass does not know.

## How it could be measured, if someone wants a number

Not done here; it needs a control the brief does not permit substituting.

- A control with `~/.claude/skills/graphify/` moved aside — an account-level ablation, not a
  project-level one. That is the only true with/without for this skill.
- The second confound would remain and is larger for this skill than for any other: the treatment
  directory contains **`graphify-out/`** (a built graph, `graph.json`, `manifest.json`,
  `GRAPH_REPORT.md`) and the control does not. The skill's own description says a question should
  be *"treated as a graphify query first"* when `graphify-out/` exists. Any difference measured
  between these two directories on a graph question is partly the data, not the skill, and the two
  cannot be separated without also copying `graphify-out/` into the control.

## Limits of this measurement

n=1 per arm, unblinded, one question — and for the ablation proper, n does not matter, because the
two arms are the same condition.

The file comparison is exact and not subject to sampling: two md5 sums and a recursive diff, taken
2026-08-26. It says nothing about whether the vendored copy will still match tomorrow, which is the
whole reason it exists.

The shared confounds, stated for consistency with the other four files:

1. **`graphify` is installed at account level and loads in both arms.** Here that is the finding
   rather than a caveat.
2. **The control directory is not the treatment directory minus skills.** It holds `CLAUDE.md` and
   `docs/as-built/` only; the treatment is the live `scio` repo, which also holds `docs/next/`,
   `docs/mined/`, `docs/triage/`, `scripts/` and — decisively for this skill — `graphify-out/`.
