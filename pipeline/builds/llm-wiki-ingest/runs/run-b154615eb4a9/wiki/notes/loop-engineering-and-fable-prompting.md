---
title: Loop engineering (LOOPS.md) and Anthropic's own Fable 5 prompting rules
sources:
  - url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
    note: "Primary source for every Anthropic rule below. Read in full."
    fetched: 2026-09-02
  - url: https://platform.claude.com/docs/en/models/fable-5/overview
    fetched: 2026-09-02
  - url: https://www.aibuilderclub.com/blog/loops-md-karpathy
    note: "Secondary. The only source found that tried to trace LOOPS.md to a primary; its finding is quoted below."
    fetched: 2026-09-02
  - note: "Short video (TikTok, creator reposting @8xMoysei's X post 'Master Claude With Fable 5: 6 Rules Straight From Anthropic's Docs', 124k views, 5 Jul 2026), transcribed locally 2026-09-02. The video's own claims are graded, not trusted."
status: verified
tags: [prompting, agents, loops, fable-5, effort, harness, claims-graded]
related: ["[[effective-agents-anthropic]]", "[[api-agent-loop]]", "[[subagents]]", "[[skill-authoring-best-practices]]", "[[prompt-patterns-kernel]]", "[[harness-over-model-prime-agent]]", "[[llm-wiki-pattern]]", "[[third-party-landscape]]", "[[glm-5.3-local]]", "[[best-local-llm-2026-09]]", "[[system-prompt-transparency]]", "[[adversarial-plan-review-claudex]]"]
---

# Loop engineering and Fable 5 prompting

Two things travel together in the video that prompted this note: a circulating document
called LOOPS.md ("nine rules for building agents that run for days") and a summary of
Anthropic's model-specific prompting page for Claude Fable 5. They are of very different
evidential weight, so they are separated here.

## LOOPS.md — "Field Notes on Agents That Run for Days (v060726)"

**Attribution to Andrej Karpathy: UNVERIFIED.** The one write-up that tried to trace it
(aibuilderclub, fetched 2026-09-02) reports "unverified, not disproven": no LOOPS.md on
karpathy.ai, in his GitHub repositories, or in public gists; the claim originates from a
secondhand social post with no primary link. The video additionally calls him "one of the
godfathers of AI", which is the label normally attached to Hinton, Bengio and LeCun; it is
not evidence either way, only a sign the creator did not check.

The nine rules as they circulate (REPEATED — copied consistently across secondary sources;
no primary text read):

1. Write a loop, not a prompt
2. Separate the planner, generator, and evaluator roles
3. Negotiate the contract for "done" first
4. Write state to disk, not to context
5. Let the loop restart cleanly
6. Grade subjective quality with an explicit rubric
7. Debug by reading the raw trace
8. Delete harness scaffolding as models improve
9. The bottleneck always moves

Whoever wrote them, rules 2, 4, 6 and 7 are what this repo already runs on: the
skill-builder separates author from reader from grader, keeps its state in
`pipeline/builds/<id>/events.jsonl`, grades with a preregistered rubric, and its every
expensive defect was caught by reading raw output rather than by a gate
(`pipeline/REVIEW-2026-09-02-skill-builder.md`). Rule 8 is the one we have not practised:
gates added on 2026-09-01 were kept, not deleted, when the model stopped needing them.

## Anthropic's Fable 5 prompting page — what the "6 rules" video got right

Everything below is MEASURED against the docs page unless marked.

- **Effort is the primary control.** "Use `high` as the default for most tasks, with
  `xhigh` for the most capability-sensitive workloads and `medium` or `low` for routine
  work. Lower effort settings on Claude Fable 5 still perform well and often exceed
  `xhigh` performance on prior models." Default effort on the API is `high` for Fable
  5.1, Fable 5, Opus 5 and Sonnet 5; Haiku 4.5 has no effort parameter.
- **Give the reason, not only the request.** Template verbatim: "I'm working on [the
  larger task] for [who it's for]. They need [what the output enables]. With that in
  mind: [request]."
- **State the boundaries.** The page's own examples of unrequested action are "drafting
  an email when none was asked for, creating defensive git-branch backups" — the video's
  "explicit negatives" rule is a paraphrase of this section.
- **Ground progress claims.** Verbatim: "Before reporting progress, audit each claim
  against a tool result from this session. Only report work you can point to evidence
  for; if something is not yet verified, say so explicitly." Anthropic says this "nearly
  eliminated fabricated status reports even on tasks designed to elicit them" — their
  testing, numbers not published.
- **Fable 5 facts** (overview page): released June 9 2026; $10 / $50 per MTok; 1M context;
  128K max output; adaptive thinking always on; now *legacy*, Fable 5.1 is current.

**Claims in the video NOT verified:** that Anthropic "pulled it offline, then redeployed it
on July 1 with updated cybersecurity safeguards" and that "until July 7 you can burn up to
50% of your weekly plan limits on it at no extra cost". Neither appears on the two docs
pages read; not checked further. Treat as UNVERIFIED.

## What on that page matters for this repo

These are the lines that change what we do, all MEASURED from the page:

1. **"Skills developed for prior models are often too prescriptive for Claude Fable 5 and
   can degrade output quality. Review and consider removing older instructions if default
   performance is better."** Our library was written and measured on Opus. The
   skill-builder's baseline-vs-with measurement is exactly the instrument for this: a
   with-arm that loses to the bare arm on Fable is a skill that has become a cost.
2. **"Separate, fresh-context verifier subagents tend to outperform self-critique."**
   Corroborates the agent's rule "you do not grade your own work" from Anthropic's side.
3. **"Don't instruct Claude to reproduce its reasoning in the response"** — such
   instructions can trigger the `reasoning_extraction` refusal category and fall back to
   Opus 4.8. Action: audit skills for "show your thinking" / "explain your reasoning"
   wording before measuring on Fable.
4. **Effort per run.** `dispatch.py` fixes the model tier per run but not the effort; the
   contract's "never route down" list should say which effort the measurement runs at,
   or two builds on the same tier are still not comparable.
5. **"Prefer asynchronous communication between orchestrator and subagents over blocking"**
   — the same conclusion the review reached from the coordinator-time measurement
   ("do not idle on a run").

## Verdict summary

| claim | verdict |
|---|---|
| LOOPS.md is by Karpathy | UNVERIFIED (searched, not found at any primary) |
| the nine rules' text | REPEATED (consistent across copies) |
| effort levels and their recommended use | MEASURED (docs) |
| the "why" template, boundaries, audit-before-reporting block | MEASURED (docs, verbatim) |
| Fable 5 GA date, price, context, output | MEASURED (docs) |
| pulled offline / July 1 redeploy / 50% free until July 7 | UNVERIFIED |
