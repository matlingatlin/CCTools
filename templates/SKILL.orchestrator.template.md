---
name: <kebab-case-name-matching-directory>
description: "Use when <the user or the brain deliberately invokes this multi-step orchestration — name the entry, e.g. /name>. <What the orchestration does end to end.>"
disable-model-invocation: true
---

# <Orchestrator Name>

<One or two sentences: the multi-step job this coordinates, and that it is invoked
deliberately (not auto-triggered). Name the state files / talents it drives.>

## When to use
- <The explicit trigger — e.g. the user runs /name, or another talent hands off here.>

## Procedure
1. **Read state.** <Which files / inputs it reads first.>
2. **<Step: route / delegate.>** <Which talents it chains, in order; dogfood, don't hand-roll.>
3. **<Step: apply gates / checks.>** <The gates or safety checks and where.>
4. **<Step: produce + persist.>** <Coordinator writes results; commit.>
5. **<Step: log + decide continue/stop.>** <Stop-condition + human gate on irreversible.>

## Rules
- <Coordinator commits; agents produce (if it fans out).>
- <Human gate before anything irreversible (merge/delete/push-outward).>
- <Bounded per invocation — one job/wave, not an unbounded run.>
