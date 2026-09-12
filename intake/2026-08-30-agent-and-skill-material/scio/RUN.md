# Starting a new project

Two steps. Then say **run**.

---

## 1 · Point the new repo at this one

In the new repository, create `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "scio": { "source": { "source": "github", "repo": "matlingatlin/scio" } }
  },
  "enabledPlugins": { "scio@scio": true }
}
```

That registers this repo as a marketplace and enables its plugin once the folder is trusted. The
plugin carries **sixteen skills**, and the knowledge in `docs/` comes with it.

**Pin it when the work gets serious.** A source takes a `sha`, and the resolved commit is itself the
version when no `version` is set — so a build repo can be pinned to an exact commit of this one and
will not drift underneath itself.

### Trying it without installing

```bash
claude --plugin-dir /path/to/scio
```

Loads the plugin for one session. Use this to test changes here before anyone depends on them.

### Checking it still works

```bash
claude plugin validate /path/to/scio --strict
```

Checks the manifest and the frontmatter of every skill, and treats warnings as errors. **It checks
schema, not truth** — it will not notice that a skill describes a function whose signature changed.
That is what version pinning is for.

---

## 2 · Say run

```
run
```

or `/scio:run` if you want to be explicit.

That loads `.claude/skills/run/SKILL.md`, which is the actual bootstrap: the three repos and which
one is writable, how to load knowledge by retrieval instead of packing, the order of work, and the
rules that make the output trustworthy.

**Read that file if you want to know what will happen.** It is short, and it is the real document —
this page is only how to reach it.

---

## 3 · Turn on the graph, in that order

Do this in the build repo the day it is created, and in any repo the app itself generates.

```bash
graphify update .          # full build, once
graphify hook install      # then it stays current on every commit
```

**The order is not cosmetic.** The hook rebuilds only the files in the commit, so installing it
first gives you a graph of your recent commits and nothing else — which looks complete and is not.
Measured: hook alone produced 3 nodes and 2 edges on a two-file repo; a full build immediately
afterwards produced 6 and 8.

What it costs, measured on 2026-08-26: a full build of **5,955 files and 1.34M lines takes 9.5
seconds** and **zero model calls**. The hook forks the rebuild into the background, so the commit
itself pays **222 ms**. That last number is why it survives — a hook that made every commit wait
nine seconds gets disabled within a week.

Then query it instead of reading source:

```bash
graphify explain "is_buildable" --graph <graph.json>
graphify path "A" "B" --graph <graph.json>
```

Measured on a real question — *what does the intake gate check, and what touches it* — reading the
layer document costs **≈2,318 tokens**; the graph query costs **≈546**. Four times cheaper, and the
answer is better: exact file and line, and all 26 call sites.

**The caveat:** `update` re-extracts code. Documents need semantic extraction, which does need a
model — so a prose corpus does not stay current under this hook. Rebuild those deliberately.

---

## What you are pointing at

| | |
|---|---|
| `docs/as-built/` | what the predecessor system actually does — seven layers, its twenty ADRs, the user journey, the verified review findings. Written so nobody has to open the old repo |
| `docs/next/` | the forward view, one document per layer, nine sections each. Roughly **85 numbered proposals**, none of them decided |
| `docs/decisions/` | where a proposal becomes a decision. Currently holds the template and nothing else |
| `docs/as-built/graph/` | 5,173 nodes and 12,054 edges over the old repo. Query it instead of reading source |
| `.claude/skills/` | sixteen skills — the procedures for brainstorming, architecture, testing, design, and the research each one rests on |
| `docs/REVIEW-WHOLE.md` | what the documents get wrong about each other. Read before trusting a number |

## What is not ready

**Nothing is decided.** 85 proposals, zero ADRs. The stack is open, the architecture is open, and
the layer count is open — seven describes the predecessor, it does not specify the rebuild.

**No skill has an eval.** `claude plugin eval` exists and its default ablation runs a no-plugin
baseline and reports the delta, which is the one measurement that would tell us whether any of
these sixteen changes the outcome. None has been run.

Both are deliberate: the decisions come from the brainstorm and architect passes, per layer, and
those have not been run either.
