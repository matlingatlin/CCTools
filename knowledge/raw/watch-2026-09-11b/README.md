# The fourth batch, 2026-09-11 (evening) — two rows, both re-baselined the same day

**84 unchanged · 2 changed · 10 noise · 0 unreachable · 0 tampered · 96 watched.** Both changed
rows are `code.claude.com` docs that had been re-baselined **earlier the same day**, which is a
third observation of a pattern already under measurement: these pages move several times per day,
while the READMEs beside them in `WATCH.tsv` move weekly. If it holds, weekly `kb-watch.yml` is the
wrong cadence for these rows specifically — but three observations is still not a frequency, and
the change is to be measured before the schedule is touched.

Both were triaged immediately rather than queued, under the standing rule: a row is read at once
when it touches a source this base carries a **correction or caveat** on. `sub-agents` carries one
recorded today — a version sentence found stale for the third time and deleted rather than updated.

## `sub-agents.md` — 28 diff lines, one real sentence

The subagent tool pool is **not purely subtractive**, and every mental model built from "inherit,
then remove" predicts the wrong list. Added verbatim:

> On macOS, Linux, and WSL, a subagent can also receive the Glob and Grep tools when the main
> conversation doesn't have them.

Platform-conditional, in the *widening* direction — so a capability that exists on three platforms
is invisible to anyone testing on the fourth. → `subagents`

## `hooks-guide.md` — 128 diff lines, and a fourth silent failure

A new troubleshooting section for *"hook prints valid JSON but the decision doesn't take effect and
no error appears"*, with two causes, both silent:

> When your hook returns `permissionDecision` or `additionalContext` at the top level instead of
> inside `hookSpecificOutput`, the JSON still parses, and Claude Code ignores the misplaced fields
> without reporting an error.

A hook that denies a tool call, written with the field one level too high, is indistinguishable
from a hook that allowed it — which matters most exactly where this repo's fourth gate puts a hook
as the enforcement. Diagnosable only with `claude --debug`, searching the log for
`Hook JSON output had unrecognized keys`. The second cause: anything on stdout before the JSON (an
unconditional `echo` in a shell profile) stops the output starting with `{`, so a hook can be
broken by a file the hook does not mention. → `hooks`

Both belong to the shape this base keeps finding in this product's surface and now names:
**the failure is not that it errors, it is that it parses.**

## Third row, an hour later — `plugin-evals.md`, and the cadence measurement gets a fourth point

`85 unchanged · 1 changed · 10 noise · 0 tampered`. The changed row is `code.claude.com` again,
baselined the same day again — a **fourth** observation of pages moving several times per day. It
was triaged on sight rather than queued, because the base carries an explicit **caveat** on this
source (that our "no built-in way to run these evaluations" line survives the arrival of a runner).

Most of the diff is editorial. Two changes are not:

**The cost formula doubled when it was spelled out.** *"cases × runs × arms"* became *"cases × runs
agent runs with the plugin **and as many again for the no-plugin baseline**, plus three short judge
calls per `llm` or `baseline` grader per run."* The baseline arm that makes the instrument worth
having is also what doubles its bill — relevant to the open decision about packaging this library
as a plugin, which is the user's to make.

**An `llm` judge sees only the first 12 and the last 12 messages.** *"A `regex` grader sees every
message; an `llm` judge sees the first 12 and the last 12."* On any run longer than 24 messages the
judge is blind to the middle and its verdict says nothing about that. A talent whose effect shows
up mid-run is invisible to the grader meant to detect it. → `anthropic-skill-authoring-contract`

Also recorded there so a later diff is not re-read from scratch: `schema_version` `"1.1"`;
`type: agent` mocks now answer via `--judge-model`, so changing the judge changes the mocks; the
replay path is `mocks/.replay/`; and an unusable evals directory is an error as a flag but prints a
`Warning:` and silently falls back to `evals/` as a manifest value.

## Fourth row, 2026-09-12 02:0xZ — the first change on this host that owes nothing

`84 unchanged · 1 changed · 11 noise · 0 tampered`. `model-config.md` moved, 30 words, and the
whole diff is `/model` picker UX: the session-only `s` key is now documented as rebindable via
`modelPicker:thisSessionOnly`, plus one clarifying sentence on switching for a single session. No
note in this base claims anything about that key, so **no note is owed a re-read.**

Recorded because of what it does to the tally rather than what it says. The run had been **3 of 3
substantive**, which was the surprising part — a host that changes hourly could easily have been all
chrome and was not. It is now **3 of 4**. Re-baselined; nothing else to do.

## Fifth row, 2026-09-12 08:2xZ — a different host, and a vendor retracting a security claim

`84 unchanged · 1 changed · 11 noise · 0 tampered`. **The first changed row in this whole tally that
is not `code.claude.com`** — a GitHub README, the class that moves weekly — and it arrived in the
08Z window, the first pass from outside 00–05Z. Both facts matter to the cadence measurement: the
time-window hypothesis gains its first out-of-window observation, and it is a *different host*, so it
says nothing either way about `code.claude.com`.

34 words, and substantive. Prime Intellect narrowed a security property their README had implied:
SHA-256 verification is now stated as **integrity, not authenticity**, *"because the inventory and
archive come from the same origin"*, with HTTPS named as the authenticity boundary and
`--proto '=https' --proto-redir '=https'` added to refuse a plaintext redirect.

**This base wrote that argument first, for graphify, from the code.** Both notes now carry it and
name each other. → `harness-over-model-prime-agent`, `graphify-assessment`

