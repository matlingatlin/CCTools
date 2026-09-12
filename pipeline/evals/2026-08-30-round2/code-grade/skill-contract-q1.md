# Q1, graded by code — the artefact question

`artifact_check.py` extracts the SKILL.md each answer produced and runs the real contract
checker on it. No judge is involved, so there is nothing to be blind about, and nothing to
argue with.

| repeat | arm | artefact | verdict | detail |
| --- | --- | --- | --- | --- |
| 1 | without | yes | pass | 0 errors, 1 warning (`desc.target`) |
| 1 | with | yes | pass | 0 errors, 1 warning · 2 rules not decidable from a lone file |
| 2 | without | yes | pass | 0 errors, 1 warning |
| 2 | with | yes | **fail** | **3 errors — `fm.parses`, `name.pattern`, `desc.present`** |

## The failure is real, and it is the serious kind

Verified against the raw file rather than reported from the checker's word. The r2 `with`
answer wrote this inside its description, unquoted:

    ... and ends in one mandatory VERDICT: GO / NO-GO line.

A bare `: ` inside an unquoted YAML scalar makes the mapping unparseable. PyYAML: *"mapping
values are not allowed here"*. The frontmatter does not parse, so `name` and `description`
are absent as far as any reader is concerned — which is why three rules go red off one
defect.

**That skill would not load at all.** It is the exact failure the `fm.parses` rule was
written for: three talents in this repo once shipped unloadable for the same class of
reason.

A judge reading for content would very likely have passed it. The description is a good
description — specific triggers, named negative scope, an emitted artefact. It is simply
not valid YAML, and only something that parses it can tell.

## What this says about the arms

Both arms produced a real file in both repeats — the round-1 complaint that answers
described instead of producing is gone, in both arms. The only artefact-level difference in
either repeat runs **against** the method arm: it wrote a richer description and broke the
file doing it.

n=1 on that, and it is one defect rather than a pattern. It is recorded as an observation,
not a regression finding, and the judged expectations for Q1 are scored separately.
