# Component Catalog — schema & process

The catalog is the single searchable index of every reusable component harvested
from source repos, so we can review, test, and always pick the best-fitting one
for a task. `catalog.json` is the source of truth; `CATALOG.md` is the readable view.

## What's cataloged

All four reusable component types, deduped across mirror directories
(`.cursor/`, `.kiro/`, `.codex/`, `.opencode/`, `docs/`, `legacy-command-shims/`
are excluded as mirrors/generated). Sub-components bundled inside a skill (its own
`agents/`, `hooks/`) are recorded in that skill's `bundles` field, not as separate
entries.

| Type | Count | Source |
| --- | --- | --- |
| skill | 301 | superpowers `skills/`, ECC `skills/` + `.agents/skills/` |
| agent | 68 | ECC top-level `agents/` |
| command | 97 | ECC `commands/`, `.claude/commands/` |
| hook | 3 | superpowers + ECC top-level `hooks/` |

## Entry schema (catalog.json)

```
type            skill | agent | command | hook
name            component name (from frontmatter, else dir/file name)
repo            superpowers | ecc
source_path     path within the source repo
description     from frontmatter (what it does + when to use)
files           file count in the component dir
has_scripts     bundles executable .py/.sh/.js/.ts
bundles         sub-component dirs present (agents/hooks/commands)
security_flags  [network, secret-ref, exec]  (see below)
also_in         other paths the same name appears (mirrors)
status          cataloged → reviewed → adopted | rejected
decision        pending | adopt | adapt | reject | defer
test            untested | passed | failed | n/a
```

## Security flags — a marker, not a verdict

Flags come from a coarse regex scan and mean **"read this before adopting"**, not
"malicious":

- `network` — mentions curl/wget/fetch/http to a non-Claude host. Could be a real
  outbound call, or just documentation.
- `secret-ref` — mentions API_KEY/TOKEN/SECRET/etc. Usually a skill that *uses* an
  API and documents its key, not a leaked secret — but must be read.
- `exec` — mentions rm -rf/sudo/eval/subprocess/base64 -d/chmod. Could be a
  legitimate script or a red flag.

**Gate rule (per the project's security posture):** no third-party component is
adopted into `.claude/skills/` without a human/agent reading it. A flag routes it
to manual review first; nothing auto-installs. The enforcement backing this is a
`PreToolUse` hook (see `knowledge/notes/hooks.md`), the only mechanism a downloaded
component cannot talk its way past.

## This is a cross-project library, not a factory-only toolbox

The factory we are building now is **infrastructure** that gets reused across
future projects — app development, trading platforms, contract platforms, social
media, marketing. So a component being language-specific or vertical (finance,
frontend, social, a specific framework) does **not** make it low value: it is
exactly what gets pulled when such a project comes up. **Nothing is rejected for
being niche.** `reject` is reserved for true duplicates or components that fail the
security read — never for narrow scope.

The `fit` score therefore means *immediacy*, not worth:

- **fit 3 — build now:** the factory's own infrastructure (research, testing/eval,
  skill/hook authoring, agent orchestration, context/token). Full-evaluated now.
- **fit 2 — broadly reusable** across many project types.
- **fit 1 — domain/vertical library:** retained, organized by domain, evaluated
  on demand when a project in that domain starts.

## Status lifecycle

```
cataloged  → every harvested component starts here (Phase A, done)
reviewed   → triaged into a domain + fit + security-read (Phase B)
adopted    → passed evaluation, copied into .claude/skills/ (Phase D)
library    → kept, organized by domain, evaluated on demand for a matching project
rejected   → ONLY a true duplicate or a security-read failure (never "too niche")
```

## Process (tiered — full-eval only the shortlist)

- **Phase A — Harvest** ✅ all 469 cataloged with descriptions + security scan.
- **Phase B — Triage** — classify into domains; flag overlaps with what we already
  have; security-read the flagged ones. (batch subagents)
- **Phase C — Prioritize** — select a shortlist that fits this project (research,
  testing, skill-authoring, context/token, deep reading, orchestration).
- **Phase D — Evaluate & adopt** — full baseline-vs-component eval (application or
  pressure scenario per type) on the shortlist; adopt winners into `.claude/skills/`,
  record verdict here. The other ~450 stay cataloged and are evaluated on demand
  when a task calls for them.
