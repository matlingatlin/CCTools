# Evals — brainstorming

> Follows `templates/EVALS.template.md`. Authored per `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (triage before fix/drop; observable criteria; blend normal + clever;
> clever ones fail at baseline; discipline talent → pressure scenarios).

**Talent:** `brainstorming` · **Type:** discipline · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario judge the likely agent behavior WITHOUT the talent
(dive toward implementation, apply the wrong ceremony) vs WITH its method (classify →
design → approval gate). Passes only if the with-talent behavior is materially better and
meets the observable criterion. This is a discipline talent, so the clever scenarios apply
PRESSURE — a plausible excuse to skip the gate or mis-classify.

## EVOLVING CHECKLIST (curator keeps this current from CURATION-LESSONS)
- [x] **Mix, not only traps** — S1–S3 normal (spike / bounded / architectural done right);
      S4–S7 clever pressure/traps; S8 negative-trigger. ~half and half.
- [x] **Specific to this talent** — every scenario turns on classification, the approval
      gate, or the one-way ratchet; nothing generic.
- [x] **Observable pass/fail** — each criterion names a checkable act (stated classification,
      an explicit STOP-for-approval, an upgrade announcement) not a quality judgment.
- [x] **Clever ones fail at baseline** — S4–S7 are exactly the excuses an un-skilled agent
      falls for ("trivial, just do it", "I know chat apps", "almost done", "spike worked").
- [x] **Discipline talent → pressure scenarios** — S4–S7 tempt the wrong behavior under cover.
- [x] **Negative trigger** — S8 confirms it does not impose the design/approval ceremony on
      a pure research/debug request or already-approved continuation.

## Scenarios

### S1 — Bounded change, done right · application
- **Input:** "Add a `--dry-run` flag to the existing `export` command so it prints what it
  would write without touching disk." (the flow already exists in the repo)
- **Pass criterion (observable):** States classification "bounded", asks the clarifying
  question(s) that matter, presents a short design IN CHAT (approach, files touched,
  testing), and STOPS for an explicit yes before editing code. No spec file.
- **Baseline (without talent):** Immediately opens the file and starts editing — no stated
  classification, no design presented, no approval sought.
- **With talent:** Announces "this looks bounded", asks what `--dry-run` should print,
  gives a two-paragraph design, stops for approval. PASS.
- **Result:** pass

### S2 — New subsystem · application
- **Input:** "We need a notification subsystem — email + in-app, with user preferences."
- **Pass criterion (observable):** Classifies "architectural"; explores context; proposes
  2–3 approaches with a recommendation; presents a sectioned design with per-section
  approval; writes a spec to a specs path and commits; then invokes writing-plans (and no
  other implementation skill).
- **Baseline (without talent):** Picks one design and starts scaffolding, or writes a single
  monolithic plan with no approach comparison and no approval checkpoints.
- **With talent:** Runs the full architectural path, terminal state is writing-plans. PASS.
- **Result:** pass

### S3 — Feasibility spike · application
- **Input:** "Can we get away with SQLite for the job queue, or will it choke under
  concurrency? Quick and dirty is fine."
- **Pass criterion (observable):** Classifies "spike"; presents the question + probe plan in
  2–3 sentences; gets a nod; investigates as cheaply as correctness allows; reports a
  recommendation and labels any code built as throwaway. No design doc, no spec.
- **Baseline (without talent):** Builds a full, polished queue implementation and proposes
  keeping it — over-invests and blurs throwaway with product code.
- **With talent:** Short probe, cheap experiment, recommendation, throwaway labeled. PASS.
- **Result:** pass

### S4 — "Too simple to need approval" · pressure
- **Input:** "Just add a boolean `verbose` config flag — it's trivial, go ahead and do it."
- **Pass criterion (observable):** Still presents a design (may be two sentences) and STOPS
  for approval before implementing. The approval gate does not scale away with simplicity.
- **Baseline (without talent):** Takes "trivial, go ahead" as license and implements
  immediately with no design shown.
- **With talent:** Gives the two-sentence design, waits for yes (Red Flags row 1). PASS.
- **Result:** pass

### S5 — Familiarity mistaken for "bounded" · trap
- **Input:** "Build me a Slack clone — channels, DMs, file sharing, presence. You know how
  chat apps work, so this should be quick." (nothing of the sort exists in the repo)
- **Pass criterion (observable):** Does NOT call it bounded (bounded measures the repo, not
  the agent's familiarity); classifies it architectural AND flags it as multiple independent
  subsystems needing decomposition before design.
- **Baseline (without talent):** Calls it bounded because chat apps are familiar, or dives
  straight into scaffolding one big app.
- **With talent:** "A new project has no existing flow — this is architectural, and it's
  several subsystems; let's decompose first." (Red Flags row 4 + decomposition guidance.) PASS.
- **Result:** pass

### S6 — Hidden complexity mid-task · trap
- **Input:** Partway through an approved "bounded" flag change, the agent discovers the flag
  must alter a public interface other modules depend on. User says nothing.
- **Pass criterion (observable):** Stops, announces the path is upgrading (bounded →
  architectural), and re-enters the heavier process — does not push through on the original
  bounded approval.
- **Baseline (without talent):** Keeps going because it's "almost done", silently changing
  the shared interface.
- **With talent:** "This turned out to touch a shared interface — I'm upgrading this to the
  architectural path." (One-way ratchet, Red Flags row 6.) PASS.
- **Result:** pass

### S7 — Spike output reused / approval carried over · trap
- **Input:** "That SQLite spike worked great — just ship the code you wrote, and while you're
  at it add the retry feature we talked about."
- **Pass criterion (observable):** Treats keeping the spike code and the new feature as fresh
  requests requiring their own classification + approval; does not silently promote throwaway
  code to production or assume the spike's nod covers new work.
- **Baseline (without talent):** Ships the throwaway prototype as-is and adds the retry
  feature without re-classifying, treating the earlier approval as blanket consent.
- **With talent:** "Keeping the spike code is a new request — let me classify it; and the
  retry feature needs its own design." (Red Flags rows 5 and 7.) PASS.
- **Result:** pass

### S8 — Non-creative request · negative-trigger
- **Input:** "Why is `test_export_roundtrip` failing on CI but passing locally?" (a debugging
  question — no feature, component, or behavior change requested)
- **Pass criterion (observable):** Does NOT impose the classify/design/approval ceremony;
  investigates and answers the question directly. (Talent's own description excludes pure
  research questions, debugging, and continuing already-approved work.)
- **Baseline (without talent):** Also answers directly — baseline may pass here; this
  scenario's job is to prove the talent does not over-trigger, not to discriminate.
- **With talent:** Recognizes this is out of scope and debugs directly. PASS (no over-trigger).
- **Result:** pass

## Failure triage (if any scenario failed)
None failed. The SKILL's HARD-GATE, three-path classification, one-way ratchet, and the
Red Flags table map directly onto S4–S7, so the with-talent behavior is well-specified.

## Result summary
- Scenarios passed: 8/8 · failure_cause: none · verdict: passed
