---
name: app-design
layer: B, F
phase: both
status: written
description: Make a generated application look designed rather than generated. Use when deciding an app's visual system, writing or reviewing design tokens, building UI packages, extending Layer B's playbook, or whenever generated screens look generic. Covers the token contract, the deterministic design gate, the defaults that make AI-built apps recognisable, and the states most generators forget.
---

# app-design

Every AI app builder ships the same app. Blue-600 primary, `rounded-lg` on everything, cards
with soft shadows, Inter, one weight of everything, and no empty state. A user can tell in two
seconds what made it.

That is not a taste problem. It is an **architecture** problem: the model is being asked to
invent an appearance per screen, so it reaches for the median of its training data, and the
median is what everyone else also shipped.

The fix follows the same principle as the rest of this system: **deterministic first.** The
design system is decided once, frozen, and enforced. The model works *inside* it and never
invents it.

---

## 1 · Tokens are a contract

The component library already has `Contract` — what an entry provides, matched by subset and
equality rather than judgement. Appearance needs the same thing.

**A design token set is frozen at the design gate and every package must consume it.** No
package picks a colour. No package picks a spacing value. A hex literal or a bare
`text-[13px]` in a generated file is a contract violation, exactly as an undeclared import
would be.

### Use the standard format, not a bespoke one

The **W3C Design Tokens Format Module** reached its first stable version (v2025.10) in
October 2025, backed by 24+ organisations including Adobe, Amazon, Google, Microsoft, Meta,
Figma, Sketch, Salesforce, Shopify, Disney and the NYT. JSON, with token properties prefixed
`$`. [designtokens.org](https://www.designtokens.org/tr/drafts/format/) ·
[spec repo](https://github.com/design-tokens/community-group)

**Emit DTCG.** Three reasons, in order of weight:

1. **It is the ownership promise, applied to design.** ADR-0001 sells code the user owns with
   a smooth handoff to a developer. A bespoke token file is a lock-in the user did not agree
   to; a DTCG file opens in Figma, Tokens Studio, Style Dictionary and anything else.
2. **The transform pipeline already exists.** Style Dictionary v4 has first-class DTCG
   support — CSS variables, Tailwind config, iOS, Android, from one source. We do not write
   that.
3. **It is boring, which is the point.** A format 24 companies agreed on will outlive our
   opinion about it.

Caveat worth knowing: Style Dictionary v4 supports DTCG, but full v2025.10 support is still
landing in v5. Pin and verify rather than assume.

What the token set fixes:

| Group | Decided once |
|---|---|
| Ground and ink | surface, raised surface, border, text, muted text — **for both themes** |
| Accent | one, plus its on-colour. Not three |
| Semantic | success / warning / danger, held **separate from the accent** |
| Type | one display face, one text face, an explicit scale, and the weights that exist |
| Rhythm | a spacing scale, a radius scale, one border weight |
| Density | compact / regular / roomy — **one choice per app, not per screen** |

Six groups. If a screen needs a seventh value, the token set is wrong — fix the set, not the
screen.

## 2 · Derive the system from the app, not from taste

A restaurant booking app and a B2B tender platform must not share a palette. The inputs exist
already in Layer A's spec:

- **app-kind** — consumer booking, internal tool, marketplace, dashboard, content site
- **`look`** — the user's own words, when they gave any (it is a defaulted-and-flagged field,
  so most of the time they did not)
- **`data_ownership_sensitivity`** — an app handling health or payment data should not look
  playful, and that is a design consequence of a spec field nobody currently reads for design
- **`users_and_roles`** — one role or many decides whether navigation is a bar or a shell

Deriving from those is a **rule**, not a judgement. Same shape as `derive.py` turning tagged
fields into an architecture: tagged fields turn into a token set.

The model's job is then narrow and appropriate: name the palette's hues so they feel like the
domain, within constraints the rules already fixed.

### The trade-off against presets, named

**v0's answer to the same problem is pre-built design systems** — "Soft Pop", "Cosmic Knight"
— described as comprehensive frameworks controlling typography, spacing, components and
overall aesthetic, not colour schemes. Reviewers single that out as the reason its output
looks better than the field's.

Presets are safe and instantly good, and they make every app on the platform a member of a
visible family. Derivation is differentiated and riskier.

**The synthesis is probably: derive a choice among curated systems, then tune within it.**
The app-kind and sensitivity fields pick the system; the user's `look` field and the domain
tune it. That keeps the floor a preset guarantees while letting a tender platform and a
restaurant app stop looking related.

Note also what the field says about audience: *"AI can create a screen for 'students' or
'business owners', but real users have specific problems, habits, fears and goals."* Layer A
already collects `users_and_roles` — and it is currently read only for access rules, never
for design.

## 3 · The defaults that give it away

Where nothing is specified, do **not** spend the freedom on these. They are the current
generated-app cluster and they read as machine-made:

- Blue-600 (or violet) as primary on white, with `rounded-lg` everywhere
- Cards with a soft shadow as the answer to every grouping problem
- Inter — or Space Grotesk as the "designed" alternative — for everything
- One type size for headings, one for body, no scale between them
- Gradient hero, centred, on an otherwise flat page
- Emoji as section markers or empty-state art
- Equal visual weight for everything, so nothing reads as important
- A dark mode that is the light palette inverted, with grey text on grey
- `transition: all` and `will-change: all` — both are model defaults, both are a performance
  bug, and both are one grep. `will-change: all` in particular forces the compositor to promote
  a layer it cannot predict
- Animating anything other than `transform` and `opacity`. Everything else runs layout or paint
  on every frame

The 2026 practitioner name for this is **"AI design slop"**, and the cluster they list is
worth adding verbatim, because it has moved since the one above: *glassmorphism, gradients,
floating cards, soft shadows, 3D icons, minimal dashboards*. Popular, therefore common in
training data, therefore what a model reaches for when nothing directs it.

The diagnosis in the field matches this skill's: *"'Looks designed' isn't in an AI model's
objective, so absent direction, it reaches for the most statistically common pattern."* The
disagreement is only about the fix — most advice is "prompt better", which does not survive
contact with a seven-package build.

**A grey chosen with a slight hue bias toward the accent reads as considered. A pure neutral
grey reads as untouched default.** That single choice separates most designed interfaces from
most generated ones.

## 4 · The states that are always missing

`PRODUCTION_READINESS_DIFF.md` §7 lists these as a **quality bar**, not a nicety: *"Fel-,
loading- och empty states fungerar."*

Every list, every form, every fetch needs four designed states, and they are part of the
package's acceptance criteria — not a follow-up:

| State | The failure to avoid |
|---|---|
| **Empty** | a blank area. It needs one sentence saying what goes here and the action that puts something there |
| **Loading** | a spinner in the middle of a white page. Prefer skeletons in the shape of the content that is coming |
| **Error** | "Something went wrong." Say what failed and what the person can do next |
| **Partial** | some data arrived and some did not, shown honestly rather than as complete |

The fourth is the one nobody builds, and it is the one this system already has a vocabulary
for — `unjudged`, `needs_look`. Honest partial state is a house style here, and it should
reach the UI.

## 4a · The motion admission test

Added 2026-08-26 from `docs/mined/PASS2-ECC-SKILLS.md` §1.6 (`motion-foundations`), verdicted the
best-formed rule in its cluster. §5's animation-properties check already covers *how* something
animates. This covers **whether it should**, which no grep can answer.

> **Motion must do at least one of these, or it is removed:**
> **guide attention** · **communicate state** · **preserve spatial continuity**.

A four-way test: three admitting reasons and a default of removal. Decorative motion is not a
lesser reason on this list — it is not on the list. Applied to a proposed animation, the honest
answer is usually *"none of the three"*, which is why the default has to be removal rather than
discretion.

Two rules underneath it, in strict precedence:

1. **Responsiveness outranks smoothness.** *"A 60fps animation that causes input delay is worse
   than no animation."* A transition on an interaction that delays the interaction fails
   regardless of which of the three reasons it claimed.
2. **Reduced motion overrides everything** — above device adaptation, above design preference. The
   only permitted fallback is an opacity-only fade at ≤ 0.2s, and *"none"* is always acceptable.
   The Playbook's `accessibility` section says *"respect prefers-reduced-motion"* and stops there;
   this is what respecting it means.

**Why this is here and not in the Playbook.** The precedence rules are candidate house-rule text
and are queued as such (`docs/triage/LAYER-BC-TRIAGE.md`, and they must clear
`.claude/skills/playbook-admission` §2 first). The admission test itself is a **decision
procedure** — three named reasons and a default — which is what a skill carries and what a prompt
sentence would flatten into *"use motion thoughtfully"*.

**Deliberately not taken from the same source:** its token system, spring presets and duration
table. A house style naming `snappy` and `bouncy` has started choosing taste, which §2 of this
skill argues against on the same grounds it rejects presets.

## 5 · The design gate — deterministic, no model

Every other quality mechanism in this system is a rule that runs before or instead of a model
call. Appearance can have the same, and none of these need judgement:

| Check | Fails when |
|---|---|
| **Token adherence** | a generated file contains a hex literal, an arbitrary Tailwind value, or a spacing number outside the scale |
| **Contrast** | any text/ground pair falls below WCAG AA — computable from the token set alone, in both themes |
| **Scale adherence** | a font size or spacing value that is not on the declared scale |
| **State coverage** | a list, form or fetch without all four states from §4 |
| **Theme completeness** | a token defined in one theme and not the other |
| **Focus visibility** | an interactive element with no visible focus state |
| **Animation properties** | a rule animates a property other than `transform` or `opacity`, or declares `transition: all` or `will-change: all` |
| **Queryable role** | an interactive element has no accessible role or name. **A `data-testid` does not satisfy this** — see below |

Eight checks, all free, all runnable before anything renders. They belong beside `validate.py`'s
eleven architecture rule identifiers — same place in the order, same reason: *a design error should cost a
function call rather than a relay run.*

Contrast is the highest-value one. It is the single most common accessibility failure in
generated UI, it is fully determined by the token set, and it can be checked before a single
component is written.

### `data-testid` is a marking anchor, not a substitute for a role

Added 2026-08-26 from `docs/mined/PASS2-ECC-SKILLS.md` row 75. Two rules that look like they
conflict, and the reconciliation is the useful part:

- **Generate the attribute.** A stable id on every interactive and list element is what the
  design window resolves a marking through — it is Layer F's anchor, and `data-scio-id` already
  plays this role.
- **Generate the *test* against role and label**, never against the id. Testing-library's query
  priority exists because *"a testid, preferred over accessible queries, lets tests pass when
  real users would fail."*

**The reconciliation:** a component with no queryable role is **the accessibility check
failing**, and reaching for the testid hides it. So the two rules are not in tension — the id
is for machinery that must survive regeneration, the role is for anything that stands in for a
user. A generated component that can only be found by its testid has a defect, and the gate
above is where it should surface.

The honest sentence for any automated pass, here and anywhere: **"the automatable share
passed"** — never "accessible". Contrast, name/role/value and language-of-page are the bulk of
real defects, and only part of that is machine-decidable.

## 6 · Where this belongs

Layer B's `Playbook` already ships fixed house rules with every build prompt: stack, folder
structure, naming, secure-by-default list. **It has no design section.** That is the hole this
skill fills, and the natural home for §1–§4 is the playbook — carried into every package
prompt, exactly as the security defaults already are.

§5 belongs beside the other gates in Layer E.

Both are proposals. Neither is decided — see `docs/next/`.

## 6b · What exists, so we build only what does not

| Thing | What it gives us | Verdict |
|---|---|---|
| **W3C DTCG format** | the token interchange standard, 24+ backers | **adopt** — do not invent a format |
| **Style Dictionary v4** | DTCG → CSS vars, Tailwind, iOS, Android | **adopt** — do not write transforms |
| **Figma MCP** | `get_variable_defs`, `get_design_context`, `create_design_system_rules`; and `use_figma` can write to the canvas — define tokens, create components and variants | **later.** Only earns its place when a user brings an existing Figma design system |
| **Figma Skills for MCP** | Figma's own markdown skills teaching agents its workflows | reference for how a vendor writes skills |
| **shadcn / Radix / Tailwind** | the generated stack, fixed by ADR-0011 | already ours |
| **v0 design systems** | proof that frozen systems beat per-screen invention | competitor evidence, not a dependency |

The honest reading: **most of the machinery for this already exists and is standardised.** What
does not exist anywhere is deriving the system from a structured spec and enforcing it as a
contract — which is the part Scio would actually be building.

## 7 · Reviewing a screen

In order. Stop at the first failure.

1. Does every value trace to a token?
2. Does the type scale exist, and is it obeyed?
3. Is there one accent, used sparingly, and is semantic colour separate from it?
4. Do both themes resolve, with contrast passing in each?
5. Are all four states present?
6. Is anything on the §3 list present without a stated reason?
7. **Only then:** does it look good?

Question 7 is last on purpose. Six of these are checkable, and a screen that fails any of them
will not be rescued by taste.

---

## Sources

- W3C Design Tokens Community Group — [format module](https://www.designtokens.org/tr/drafts/format/),
  [repository](https://github.com/design-tokens/community-group). First stable version
  v2025.10, October 2025.
- [Style Dictionary — DTCG support](https://styledictionary.com/info/dtcg/)
- [Figma — Design systems and AI: why MCP servers are the unlock](https://www.figma.com/blog/design-systems-ai-mcp/),
  and [Figma skills for MCP](https://help.figma.com/hc/en-us/articles/39166810751895-Figma-skills-for-MCP)
- Practitioner writing on "AI design slop" and on v0's design-system approach, scanned
  2026-08-26. Opinion, not measurement — treated as evidence of consensus, not of effect.

- **Mined, 2026-08-26** — `docs/mined/PASS2-ECC-RULES-COMMANDS.md` row 2.9 (animate
  `transform`/`opacity` only, tagged *merge into `app-design`*), `docs/mined/PASS2-ECC-SKILLS.md`
  row 68 (`transition: all` and `will-change: all` as greps — *"a linter could have guaranteed
  them, so it should"*) and row 75 (the `data-testid` reconciliation, from testing-library's
  query priority). Triage: `docs/triage/LAYER-DFG-TRIAGE.md` F3, P19.
  **Limit on all three: they are playbook rules from another repository, not measurements.**
  What each shows is that the pattern is common enough for somebody to have written a rule about
  it; none carries an effect size, and §5 lists them as deterministic checks precisely because
  a check does not need one.

- **Mined, 2026-08-26** — `docs/mined/PASS2-ECC-SKILLS.md` §1.6 (`motion-foundations`), the source
  of §4a's admission test and its two precedence rules. Triage:
  `docs/triage/LAYER-BC-TRIAGE.md` row 24. **Limit: 301 lines of one community skill file with an
  `author:` and a `version:`, read once, no evaluation.** *"A 60fps animation that causes input
  delay is worse than no animation"* is an argument, not a measurement, and the three admitting
  reasons are a taxonomy nobody has tested for inter-rater agreement — unlike, say, MAST's κ = 0.88
  (`.claude/skills/architecture` §6). It is adopted because the *default* it sets is removal, which
  fails safe, and because "none of the three" is an answer a second reader can check.

Scanned 2026-08-26. **The first draft of this skill was written without this scan**, and the
scan changed it materially: it had invented a token shape where a standard exists.
