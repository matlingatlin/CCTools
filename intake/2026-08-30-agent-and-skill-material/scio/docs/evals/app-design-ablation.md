# Ablation · `app-design`

**Date:** 2026-08-26. Control: same `CLAUDE.md` and as-built docs, no project skills.

**Confound, stated up front:** `graphify` is installed at account level and loads in **both** arms.
So does `session-start-hook`. The arms differ only by the 27 project skills in
`/home/user/scio/.claude/skills/`.

**Two questions were run.** The first — aimed at the skill's own flagged counter-instinctive rule —
did not discriminate. The second did.

## The discriminating rule, and why the obvious answer is wrong

**Candidate A — §3, the tinted grey.** *"A grey chosen with a slight hue bias toward the accent reads
as considered. A pure neutral grey reads as untouched default. That single choice separates most
designed interfaces from most generated ones."* The obvious answer is a pure neutral ramp: greys are
"neutral" by definition, and neutrality sounds like the safe choice. **It failed as a discriminator;
see Q1.**

**Candidate B — §4a, the motion admission test.** *"Motion must do at least one of these, or it is
removed: guide attention · communicate state · preserve spatial continuity."* Three admitting reasons
and a **default of removal**. The skill is explicit about the trap: *"decorative motion is not a lesser
reason on this list — it is not on the list,"* and *"the honest answer is usually 'none of the three',
which is why the default has to be removal rather than discretion."* Two precedence rules sit under it:
**responsiveness outranks smoothness**, and **reduced motion overrides everything**, with the only
permitted fallback being an opacity-only fade at ≤ 0.2s.

The obvious answer is wrong because polish *is* the goal a person states, and the natural professional
response is to grant it and constrain it — a shared easing curve, a duration scale, keep it subtle.
That answer treats decoration as legitimate motion with a taste budget. The skill treats decoration as
inadmissible and makes removal the default, which is a different procedure with a different output.

## The questions

**Q1 (§3):**

> *I am setting the greys for our product UI — page background, card background, borders, secondary
> text. What should I actually base those values on? Four bullets maximum.*

**Q2 (§4a), run after Q1 failed to discriminate:**

> *Our generated app feels static and a bit cheap. I want to add motion to make it feel more polished —
> hover transitions, fades, a little page-transition animation. What rules should I set so it stays
> tasteful? Four bullets maximum.*

Neither names a skill or a file. Q2 states the decorative motive in the question, which is the point:
it points straight at the natural wrong answer.

## Control answer

**Q1:**

> - **Nothing invented in isolation** — derive greys mathematically from a single hue/chroma seed shared
>   with your brand color (e.g. same hue at near-zero saturation, or a slight tint of your primary), not
>   picked independently, so the neutral scale doesn't clash with accent colors.
> - **A perceptually-uniform scale** (OKLCH or HSL-adjusted-for-perception) with fixed lightness steps,
>   not raw hex guesses — so contrast ratios between adjacent steps stay predictable as you add more.
> - **WCAG contrast targets**, checked, not eyeballed: body/secondary text ≥4.5:1 against its background,
>   borders and dividers ≥3:1 against adjacent surfaces (WCAG non-text contrast) — pick the grey step
>   that clears the ratio, don't pick a step and hope.
> - **An existing scale as the base**, only if the stack is settled — e.g. Radix Colors'
>   Gray/Sand/Slate/Mauve or Tailwind's slate/gray/zinc — since per this project's CLAUDE.md the stack
>   (and thus any UI library) is still open, treat this as the fallback once that ADR lands, not the
>   starting point now.

**Q2:**

> - **One motion vocabulary, everywhere**: pick a single easing curve and duration scale (e.g. ~150-200ms
>   for hovers, ~250-350ms for transitions, standard ease-out) and reuse it exactly — never let two
>   components animate with different timing signatures.
> - **Motion confirms state, it doesn't perform**: only animate things that are actually changing (hover,
>   focus, enter/exit, route change) — no looping, bouncing, or attention-seeking animation on static
>   elements.
> - **Distance and scale stay small**: fades, subtle opacity/translate (a few px), or gentle scale
>   (~1-2%) only — nothing that moves far, rotates, or overshoots/springs unless it's a single deliberate
>   accent, not a default.
> - **Respect `prefers-reduced-motion`** and never block interaction on an animation (no waiting for a
>   transition to finish before a click registers) — motion should be decoration, not a gate.

## Treatment answer

**Q1:**

> - **Contrast, not vibe**: derive each grey pair (background/text) to clear WCAG AA at minimum, computed
>   against the token set — this is checkable, not a judgement call.
> - **A slight hue bias toward your accent color**, not a pure neutral (0% saturation) grey — that single
>   choice is what separates "considered" from "default Tailwind slate."
> - **A fixed step scale** (e.g. 8–10 lightness steps from surface → raised-surface → border → muted-text
>   → text), generated algorithmically from one seed rather than picked independently per use — so
>   "border" and "secondary text" aren't two unrelated decisions.
> - **Both themes at once**: define light and dark as paired outputs of the same scale/formula, not as an
>   inverted copy of one — a dark mode that's just inverted light greys is one of the tells this skill
>   flags.

**Q2:**

> Four rules, straight from the motion-admission test in this repo's design skill:
>
> - **Justify or remove.** Every animation must guide attention, communicate state, or preserve spatial
>   continuity — decorative motion isn't a lesser reason, it isn't on the list. If a hover/fade/transition
>   can't point to one of the three, cut it.
> - **Animate only `transform` and `opacity`.** Nothing else — animating layout/paint properties (width,
>   top, box-shadow, background-position) costs performance and is the tell that gives away unpolished
>   motion. Ban `transition: all` and `will-change: all` outright.
> - **Responsiveness beats smoothness.** A gorgeous 60fps transition that delays the user's next input is
>   worse than no animation. Never gate an interaction behind its own transition finishing.
> - **`prefers-reduced-motion` wins over everything**, including your design preference. The only allowed
>   fallback is an opacity-only fade ≤0.2s — full removal is always acceptable.
>
> Practical takeaway: keep durations short (~150–250ms), keep the palette of motion small (fade, slight
> translate, scale), and never animate two things nobody asked to see at once — one purposeful transition
> per state change reads as polish; three reads as cheap.

## Comparison

**Q1 — on mechanism. Convergent.**

| | **Control** | **Treatment** |
|---|---|---|
| **Hue bias toward the accent** | **yes, bullet 1** — *"same hue at near-zero saturation, or a slight tint of your primary"* | yes, bullet 2 — *"not a pure neutral (0% saturation) grey"* |
| One seed, algorithmic scale | yes, perceptually uniform (OKLCH) | yes, 8–10 steps from one seed |
| WCAG contrast | yes, with the ratios (4.5:1 text, 3:1 non-text) — **more specific than the treatment** | yes, "AA at minimum", no ratios |
| Both themes | **absent** | yes — and not an inverted copy |
| Stack caution | Radix/Tailwind named, then correctly deferred *"since per this project's CLAUDE.md the stack is still open"* | absent |

The skill's own flagged counter-instinctive rule was **reached by the control, in its first bullet.**
The treatment's real addition is the paired-theme rule (§3's *"a dark mode that is the light palette
inverted"*); the control's real addition is the explicit WCAG numbers and the deferral to the
undecided-stack ADR — which is `CLAUDE.md` working on the control, not a skill.

**Q2 — on mechanism. Divergent, and directly contradictory on the key point.**

| | **Control** | **Treatment (`app-design` §4a)** |
|---|---|---|
| Is decoration a legitimate reason? | **yes** — bullet 4 closes *"motion should be **decoration**, not a gate"* | **no** — *"decorative motion isn't a lesser reason, it isn't on the list"* |
| Default for an unjustified animation | keep it, small and consistent | **remove it** |
| Admission test | none — a taste vocabulary (one curve, one duration scale) | three named reasons, checkable by a second reader |
| Property restriction | *"subtle opacity/translate"* as a matter of degree | **only `transform` and `opacity`**; `transition: all` and `will-change: all` banned outright, as greps |
| Why that restriction | not given | layout/paint cost per frame |
| Responsiveness vs smoothness | *"never block interaction on an animation"* | same rule, stated as a **precedence**: it fails regardless of which reason it claimed |
| `prefers-reduced-motion` | *"respect"* it | overrides **everything**; only permitted fallback is opacity-only ≤ 0.2s; *"none"* always acceptable |
| Durations | 150–200 / 250–350ms, one easing curve | 150–250ms, offered as a *"practical takeaway"* after the gate |

The two arms give **opposite answers to the question the person actually asked.** The person wants
decorative polish. The control grants it and bounds it. The treatment refuses the category and then
offers durations as an afterthought. Bullet 2 of the control (*"motion confirms state, it doesn't
perform"*) lands near one of the three admitting reasons, but as a stylistic preference with no default
and no test — a designer can disagree with it; they cannot disagree with *"name one of these three or
it is cut."*

The property restriction is the other clean split. `transition: all` and `will-change: all` are on §3's
generated-app tell list precisely because they are **one grep each**; the control never mentions them,
and no amount of "keep it subtle" catches them.

## Verdict

**Q1: no difference.** **Q2: changed the outcome.**

Q1 is a result about the question, and it is worth stating against the skill's own claim. §3 asserts the
tinted grey is *"that single choice"* separating designed from generated interfaces — but a model asked
directly about greys already reaches for a tinted seed. The rule is not wrong; it is **not the thing a
prompt is missing.** Where it earns its place is as a frozen token set enforced by a gate on seven
package prompts that were never asked the question — which is §1 and §5 of the skill, and is not
reachable by asking anybody anything.

Q2 changed the outcome, on the mechanism rather than the wording. The control produced good, ordinary,
defensible motion guidance whose closing clause — *motion should be decoration* — the skill explicitly
refuses. A four-way test with a default of removal is a different procedure from a taste budget, it
produces a different set of surviving animations, and its output is checkable by a second reader in a
way *"keep it subtle"* is not.

One honest deduction: the treatment opened with *"straight from the motion-admission test in this repo's
design skill"*, so this run also shows the skill is being **read and recited**, which is not the same as
it being right. §4a's own limit says the three admitting reasons are *"a taxonomy nobody has tested for
inter-rater agreement"*, and the treatment did not carry that caveat across.

## Limits of this measurement

n=1 per arm, unblinded, two questions. I wrote both questions knowing which rules they targeted and
judged the answers knowing which arm was which. The Q2 divergence rests on one generation per arm; a
second control run might have refused decoration on its own, and a second treatment run might have
answered as the control did. Nothing here measures generated apps — no screen was built, nothing was
rendered, and no user preferred anything. What was measured is which rule each arm reaches for when
asked, which is upstream of every claim this skill makes about how apps end up looking.
