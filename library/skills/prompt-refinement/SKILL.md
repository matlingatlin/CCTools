---
name: prompt-refinement
description: Use when a prompt or task request is vague, ambiguous, or underspecified before acting on it — a request like "make it better", "clean this up", or "add auth" with no acceptance criteria, unclear scope, missing constraints, or no success metric. Diagnoses the ambiguity and rewrites the request into a precise, testable instruction (objective + acceptance criteria + constraints + output format) so work starts from a sharp target. Sharpens the request itself; use writing-plans to plan the work once the request is clear.
---

# Prompt Refinement

Turn a fuzzy request into a precise, testable instruction before any work begins. A sharp prompt prevents wasted work, wrong guesses, and unverifiable "done".

## When to use
- The request is vague ("make it better", "improve this", "handle errors") with no metric.
- Scope, constraints, output format, or success criteria are missing or ambiguous.
- Multiple reasonable interpretations exist and picking wrong is costly.

**When NOT to use:** the prompt is already precise (clear objective, testable acceptance criteria, known constraints and format) — just do the work. Don't interrogate a clear request.

## Steps
1. **Detect ambiguity by class.** Scan the request for gaps in each: **goal** (what outcome?), **scope** (what's in / out?), **format** (what shape is the output?), **constraints** (limits, tech, style, budget, deadline), **success metric** (how do we know it's done / good?). Note which classes are unresolved.
2. **Resolve the gaps.** For each unresolved class, either ask the *minimum* set of clarifying questions (only what blocks starting), or — when asking isn't possible or worthwhile — state explicit assumptions the reader can veto.
3. **Rewrite** the request into four parts: **Objective** (one sentence, concrete) · **Acceptance criteria** (a checklist of observable, testable conditions) · **Constraints** (must / must-not) · **Output format** (exact deliverable shape).
4. **Verify testability.** Read each acceptance criterion and confirm you could objectively mark it pass/fail. If any criterion is subjective ("looks good", "fast"), replace it with a measurable one ("p95 < 200ms", "passes `npm test`").

## Example
**Before:** "Make the signup page better."

**After:**
- **Objective:** Reduce signup drop-off by fixing validation UX on the signup page.
- **Acceptance criteria:** (1) inline field errors show on blur, not only on submit; (2) password rules stated before the user types; (3) submit disabled until valid; (4) all states have keyboard focus + ARIA labels.
- **Constraints:** existing component library only; no new dependencies; no backend changes.
- **Output format:** a PR editing `SignupForm` + a test covering the four criteria.

## Rules
- Ask the fewest questions that unblock the work; never interrogate.
- Every acceptance criterion must be objectively pass/fail — no subjective adjectives.
- If you assume rather than ask, state each assumption explicitly so it can be vetoed.
- Refine the request only; do not start the work or plan it here.
