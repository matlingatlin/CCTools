---
name: enterprise-agent-ops
description: "Use when standing up or running the OPERATIONS around a long-lived, cloud-hosted or continuously running agent system — the ongoing program of runtime lifecycle (start/pause/stop/restart), observability, safety controls (scopes, kill switches), change management (rollout/rollback/audit), and cost governance across the fleet. Triggers on deploying an agent as a service, an on-call/incident runbook for agents, a failure-rate spike in production, setting SLOs/kill-switches/rollback for a running agent, 'operate agents in prod', 'agent ops', 'production agent controls'. NOT for building the agent framework (agentic-os) or auditing its design (agent-architecture-audit); NOT the one-run damage gate before a destructive command (agent-blast-radius-guard), the per-call logging table (llm-call-ledger), the tier-selection decision (cost-aware-model-routing), or classical ML production review (mlops-production-review) — this is the umbrella ops discipline those plug into."
metadata:
  origin: ECC
---

# Enterprise Agent Ops

Use this skill for cloud-hosted or continuously running agent systems that need operational controls beyond single CLI sessions.

## Operational Domains

1. runtime lifecycle (start, pause, stop, restart)
2. observability (logs, metrics, traces)
3. safety controls (scopes, permissions, kill switches)
4. change management (rollout, rollback, audit)

## Baseline Controls

- immutable deployment artifacts
- least-privilege credentials
- environment-level secret injection
- hard timeout and retry budgets
- audit log for high-risk actions

## Metrics to Track

- success rate
- mean retries per task
- time to recovery
- cost per successful task
- failure class distribution

## Incident Pattern

When failure spikes:
1. freeze new rollout
2. capture representative traces
3. isolate failing route
4. patch with smallest safe change
5. run regression + security checks
6. resume gradually

## Deployment Integrations

This skill pairs with:
- PM2 workflows
- systemd services
- container orchestrators
- CI/CD gates
