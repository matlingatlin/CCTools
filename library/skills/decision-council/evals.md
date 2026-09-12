# Evals — decision-council

Functional regression test. The talent is a **process/discipline** talent: given a
consequential, costly-to-reverse go/no-go or A-vs-B decision, it frames the choice +
an explicit rubric, dispatches N *blind, independent* subagent voices (proponent /
skeptic / cost / user / long-term), collects a scored verdict per voice, then
synthesizes by **majority overridden by severity**, preserving the strongest dissent
and recording an ADR. It also disciplines *when not to convene* (trivial / cheaply
reversible → skip; options don't exist yet → brainstorm; one claim → santa-method).

Method under test: step 1 frame+rubric → step 2 fan out blind identical-input voices →
step 3 structured scored returns → step 4 severity-over-majority synthesis with kept
dissent, recorded.

These scenarios exercise (i) the two load-bearing wins — a fatal objection a lone
anchored agent rationalizes past, and the severity-override rule that a raw majority
vote would bury; (ii) the discipline boundary — not convening when it would be waste or
the wrong tool; (iii) an adversarial gap in the protocol itself.

Legend: **baseline** = a capable single agent asked to make the same call WITHOUT the
talent (frames it in its head, weighs it, decides, writes a short justification).
**with** = the talent's frame → blind council → severity-synthesis → recorded protocol.
Pass criterion per scenario is the decision AND the specific reasoning artifact the
method must produce.

---

## Scenario A — adopt a proprietary runtime with a hidden one-way door (trap; core value: severity overrides majority)

- **Input:** "Adopt Vendor-X's proprietary managed execution runtime as our core app
  substrate, or build the same on open OSS?" Four axes favor adopt (fastest
  time-to-ship, strong DX, cheapest for the first 12 months, proponent's happy path);
  the long-term-maintenance / skeptic axis surfaces that Vendor-X stores app state in an
  **undocumented proprietary format with no export path** — leaving is a full rewrite.
- **Pass criterion:** decision is NOT a naked "adopt." Either don't-adopt or
  adopt-only-with-a-funded-exit-plan, and the synthesis EXPLICITLY states that the
  4-vs-1 numeric majority was **overridden by the severity** of the irreversible
  lock-in, with that dissent recorded verbatim.
- **Baseline:** LIKELY MISS the override. A lone agent anchors on the vivid near-term
  wins ("ships in a week, cheapest, great DX"), notes lock-in as a line item, and
  rationalizes it — "we can migrate later," "worry about it if we scale." Numeric gut
  weighing lets 4 pros outvote 1 con; that is exactly the anchoring the talent exists
  to break.
- **With talent:** CATCH. A dedicated long-term/exit-cost lens is *guaranteed* a seat
  and scores lock-in on its own axis; step 4's stated rule makes a credible one-way-door
  outrank a numeric majority and forces "say so explicitly." Decision flips or gates,
  dissent kept. **PASS. Beats baseline on the load-bearing case.**

## Scenario B — ship gate that is green on everything except a security hole (trap; core value: anti-anchoring + severity)

- **Input:** "Launch the new public share-links feature today — go / no-go?" Perf, UX,
  cost, and PM-pressure all point GO; one lens (skeptic/security) finds that share
  tokens are sequential integers → trivial enumeration exposes every user's private
  doc.
- **Pass criterion:** NO-GO (or go-behind-flag until fixed), citing the auth/IDOR
  finding, with the synthesis stating severity overrode the launch majority.
- **Baseline:** MIXED / LIKELY SHIP. Under ship-day momentum a single agent scores the
  visible axes green and treats one dissent as "a follow-up ticket," shipping. The
  failure mode is precisely majority-over-severity.
- **With talent:** CATCH. Blind voices mean the security lens isn't softened by the
  room's GO energy; a credible security hole is the archetypal severity override. NO-GO,
  recorded. **PASS. Beats baseline.**

## Scenario C — rename a folder (false-ceremony guard; discipline; expect SKIP)

- **Input:** "Should we rename the `utils/` folder to `lib/`? Convene the council."
- **Pass criterion:** talent DECLINES to convene — states this is trivial and cheaply
  reversible (a one-commit rename), decides in-line, and does NOT spin up subagents or
  write an ADR. A 5-voice council here is a failure (waste + false ceremony).
- **Baseline:** PASS (correctly). A lone agent just renames it; it would never over-
  ceremonialize this on its own.
- **With talent:** PASS. The "When NOT to use" / "match size to stakes / skip trivial"
  rules fire and the coordinator declines the council. **PASS. Ties baseline (correct
  boundary).** This is a guard, not a value-add — its job here is to *not* make things
  worse, and it doesn't.

## Scenario D — options don't exist yet (neighbor-distinction; expect ROUTE-AWAY)

- **Input:** "Pick our caching strategy." No candidate strategies have been enumerated.
- **Pass criterion:** talent does NOT convene a council to "decide" among nonexistent
  options; it routes to `brainstorming` to GENERATE candidates first (its own stated
  boundary: "If the options themselves don't exist yet, brainstorm first").
- **Baseline:** PARTIAL. A lone agent may start reasoning and, usefully, may itself list
  a few options before picking — so it doesn't obviously fail; but it tends to conflate
  generate + decide in one anchored pass, choosing the first strategy it names.
- **With talent:** PASS. The DECIDE-vs-GENERATE distinction is explicit; it refuses to
  score an empty option set and hands off. **PASS. Slight edge — enforces the clean
  separation baseline blurs.**

## Scenario F — monolith vs microservices for a 3-person team (representative positive; dissent preservation + ADR)

- **Input:** "A-vs-B: build the new product as a modular monolith or microservices?
  Team is 3 engineers, pre-PMF." Real tradeoffs both ways; cost, user-latency, and
  long-term lenses lean monolith, proponent leans microservices (future scale).
- **Pass criterion:** a decision (monolith) tied to the criteria, AND an ADR in
  `docs/decisions/` that records the rule that decided it (majority, no severity
  override) AND preserves the microservices dissent verbatim rather than smoothing it
  into "we chose monolith because it's simpler."
- **Baseline:** WEAKER. A lone agent usually reaches the same answer (monolith is the
  standard call at this scale) but writes a one-sided justification that *discards* the
  scale-out case; six months later nobody can see the tradeoff was weighed or when to
  revisit. Also prone to trend-anchoring (microservices as default-modern).
- **With talent:** PASS. Blind voices force the scale case to be argued at full
  strength; synthesis records decision + rule + kept dissent as an ADR — auditable, and
  aligned with this repo's ADR ethos. **PASS. Beats baseline on rigor and
  auditability**, even when the final answer matches.

## Scenario E — biased frame / un-critiqued rubric (adversarial gap; expect the method to fail)

- **Input:** "Adopt Postgres or MongoDB for the primary store?" The coordinator (per
  step 1) writes the rubric as **{write-throughput, schema-flexibility,
  horizontal-scale-out}** — three axes that structurally favor the document store — and
  omits transactional integrity, relational query needs, and operational maturity. All
  N voices are handed ONLY this frame, as the talent mandates (identical inputs, and
  "no freelancing the rubric").
- **Pass criterion (ideal):** the method should catch that the *rubric itself is
  skewed* — some voice or coordinator step should red-team the criteria before the
  council scores against them — and not hand back a falsely-confident verdict.
- **Baseline:** EQUALLY BIASED, but honestly so. A lone agent carrying the same blind
  spot picks MongoDB with one voice's worth of confidence.
- **With talent:** WORSE / FRAGILE. Every voice scores the *same* skewed axes, and the
  rules explicitly forbid a voice from adding the missing axis ("no freelancing the
  rubric") — the skeptic lens argues *against MongoDB on the given axes*, not *against
  the axes*. Five independent voices converging on MongoDB then **launder the
  coordinator's framing bias as multi-voice consensus**, producing higher confidence in
  a wrong-rubric decision than baseline had. The talent notes "a council on the wrong
  criteria decides the wrong thing" but supplies **no lens, step, or check that
  interrogates the frame itself** — and "coordinator does not vote" plus "identical
  inputs" actively concentrate that unchecked power in the framer. **FAIL — this is the
  gap.** The anti-anchoring machinery protects against option-anchoring but not against
  *criteria*-anchoring, which is the single point the whole protocol funnels through.

---

## Result summary

| Scenario | Expected | Baseline | With talent | Beats baseline? |
|---|---|---|---|---|
| A proprietary runtime, hidden lock-in | gate/no, severity>majority | miss (anchors on ship-fast) | override + kept dissent | Yes (core value) |
| B ship gate w/ IDOR hole | NO-GO, severity>majority | mixed / ships | NO-GO, recorded | Yes (core value) |
| C rename a folder | SKIP council | skips (correct) | declines, no ceremony | Ties (correct boundary) |
| D no options yet | route to brainstorm | partial (blurs gen+decide) | refuses, hands off | Slight edge |
| F monolith vs micro | decide + ADR + dissent | same answer, thin/one-sided | ADR w/ kept dissent | Yes (rigor/audit) |
| E biased rubric | catch skewed frame | biased, 1 voice | biased, 5-voice false consensus | **No — worse** |

**5 / 6 pass.** The decisive, repeated win over baseline is A and B: a lone agent under
near-term or ship-day momentum numerically outvotes a fatal objection and rationalizes
it away; the talent guarantees the dissenting lens a seat and, via the explicit
**severity-overrides-majority** rule, makes a one-way-door or security hole outrank the
count — and forces it to be written down. F adds durable value (dissent-preserving ADR)
even when the answer matches baseline. C and D show the discipline boundary holds — it
doesn't manufacture ceremony for trivial calls or try to decide among options that don't
exist. That is real value an unaided agent does not reliably reproduce.

**Gap (E):** the entire protocol funnels through one artifact the coordinator writes
alone — the decision criteria — and *nothing in the method critiques it*. Because every
voice gets identical inputs and is forbidden from "freelancing the rubric," a skewed
frame is not corrected but *amplified*: N independent voices converging on the
frame-favored option launder the framing bias into false high-confidence consensus,
leaving the with-talent result worse than an honest single biased agent. The skeptic
lens argues against the leading *option*, never against the *criteria*.

**Fix needed:** add a frame-critique step before the council votes. Concretely: (a) a
mandatory **"red-team the rubric"** pass — one voice (or an explicit coordinator step)
whose only job is to attack the criteria: what dimension is missing, what's over-
weighted, whose interest does this rubric encode? — run and resolved *before* step 2
fan-out; and (b) relax "no freelancing the rubric" into "score the rubric, but any voice
MUST flag a decision-relevant dimension the rubric omits, and the coordinator must fold
a credible omission into the criteria and re-run." Also add to the synthesis rule:
**unanimity is a flag, not a comfort** — when all voices agree, check the frame before
trusting the consensus. (A/B/F are unaffected: their rubrics include the axis that
carries the fatal objection, so the severity override still fires.)

**Verdict: FIX** — clearly beats baseline on its load-bearing cases (severity-over-
majority on A/B, dissent-preserving record on F) and holds its discipline boundary
(C/D), with one specific, structural gap: the coordinator-authored rubric is a single
un-critiqued point of failure that the council can amplify rather than correct.
