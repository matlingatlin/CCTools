# Scio — motion & mark scan

**Scanned 2026-08-26.** A domain scan for the animated mark, run the same way every other domain
in this project is run: online, now, cited. It covers the technique decision, the surfaces the mark
must survive, the accessibility floor, the competitive field, and what a standing design process
would consist of.

Companion to `.claude/skills/app-design/SKILL.md`, which already scanned the design-token domain
(DTCG v2025.10, Style Dictionary, Figma MCP). This document does not repeat that scan. Where it
extends or corrects it, §7 says so explicitly.

---

## 1 · What I scanned, and when

Everything below was fetched or searched on **2026-08-26**. Bundle sizes marked *(measured)* were
downloaded from jsDelivr and compressed locally on that date — they are not quoted from a blog.

| Area | Primary sources reached | Confidence |
|---|---|---|
| SMIL status | MDN `<animate>`, CSS-Tricks *SMIL on?*, Chromium blink-dev intent thread | high |
| WAAPI | MDN `updatePlaybackRate`, caniuse `web-animation` | high |
| Rive / Lottie cost | npm registry + jsDelivr file listings, local gzip *(measured)* | high |
| Favicons | caniuse `link-icon-svg`, chromium-dashboard issue #3595 | high |
| SVG isolation | csswg-drafts #7213, MDN, practitioner writing | high |
| WCAG 2.2 / 3.0 | w3.org Understanding docs, W3C WAI news 2026-03-03 | high |
| DTCG motion tokens | designtokens.org format module, Style Dictionary transform reference | high |
| Figma Config 2026 | four independent secondary reports; **figma.com's own post 404'd for me** | medium |
| Competitor motion practice | linear.app/brand (reached), the rest secondary | **low — see §5** |

**Could not verify:**

- **Adoption of `prefers-reduced-motion` by users.** No browser-vendor telemetry found. What *is*
  measured is authoring, not usage: the query appears on 49.99% of desktop and 50.55% of mobile
  pages ([Web Almanac 2025, accessibility chapter](https://almanac.httparchive.org/en/2025/accessibility),
  published Jan 2026). Anyone quoting a user-percentage is guessing.
- **Whether any dev-tool brand binds *logo* motion to real system state.** I found one product
  binding *an icon* to state (GitHub's favicon, §5) and no logo precedent. Absence of evidence here
  is weak evidence — brand motion is not documented in public brand guidelines.
- **Rive editor export limits on the free tier.** [rive.app/pricing](https://rive.app/pricing) lists
  "Exports" under paid tiers while also saying the free tier has "all import/export formats". Ambiguous.
- **Measured effect of a spinning logo on task performance.** The literature I found is about
  instructional animation, not decoration. See §4.

---

## 2 · The technique decision

**Recommendation: inline SVG inside a React component, animated with the Web Animations API,
with CSS `@keyframes` retained only as the no-JS / reduced-motion floor.**

The deciding primitive is `Animation.updatePlaybackRate()` — [Baseline widely available since
March 2020](https://developer.mozilla.org/en-US/docs/Web/API/Animation/updatePlaybackRate). It changes
an animation's speed *after synchronising with its current playback position*, which is precisely the
thesis of this mark: `thinking → building` is a speed change on a gear that is already turning, and it
must not teleport. Nothing else on the list has this. WAAPI is at
[96.2% global support](https://caniuse.com/web-animation) (Chrome 84+, Safari 13.1+, Firefox 75+).
Cost: **0 KB added**. It is in the browser.

Keep the rotation and the piston travel on `transform`, and any pulse on `opacity`. Chromium has
hardware-accelerated SVG animations by default [since Chromium 89](https://developer.chrome.com/blog/hardware-accelerated-animations),
matching Firefox. One caveat that caps the design: **Chrome never divides a single SVG graphic into
separate GPU layers.** Three independently-animated groups (gear ring, pistons, pupils) is fine;
twelve is not, and no amount of `will-change` fixes it.

### Runner-up: Rive — lost on measured cost, not on capability

Rive's state machine *is* the correct abstraction for this mark. Named states, typed inputs, transitions
— that is literally the model in `logo-sketches.html`, built properly.

It loses on arithmetic. Measured 2026-08-26 from `@rive-app/canvas@2.40.1`:

| File | raw | gzip *(measured)* |
|---|---|---|
| `rive.js` | 410,792 B | **91,461 B** |
| `rive.wasm` | 1,808,114 B | **744,179 B** |
| **total before the `.riv`** | 2.2 MB | **~835 KB** |

Eight hundred and thirty-five kilobytes, for one logo, in a product whose pitch is engineering
restraint. (`@rive-app/webgl2` is [50 KB gz of JS](https://bundlephobia.com/package/@rive-app/webgl2)
but carries its own WASM.) The runtime is **MIT** (verified from the npm registry), so licensing is not
the blocker — cost is. Two further costs that are not size: the mark becomes an opaque `<canvas>`, so it
cannot read a CSS custom property or `currentColor` and the theme must be pushed in as state-machine
inputs; and it introduces a second design tool (the Rive editor, free tier capped at 3 files) into a
pipeline the project has not decided on.

**Revisit Rive the day Scio ships an illustration system**, not for one mark.

### Rejected

- **Lottie / dotLottie.** `lottie-web@5.13.0` is 76,046 B gz for the full player, 46,396 B gz for
  `lottie_light` *(measured)*. `@lottiefiles/dotlottie-web@0.79.2` is 30,013 B gz of JS plus a
  489,933 B gz WASM *(measured)*. All MIT. But Lottie is an After Effects export pipeline and the
  colours are baked into the JSON — which breaks the token contract `app-design/SKILL.md` §1 makes
  every generated app keep. Paying ~500 KB to lose theming is the wrong direction twice.
- **SMIL.** The received wisdom is wrong and worth correcting: **SMIL is not deprecated in 2026.**
  MDN marks [`<animate>` as *Baseline widely available*, since January 2020](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/animate);
  Chrome filed an intent to deprecate and [never carried it out](https://css-tricks.com/smil-on/).
  Reject it anyway, for a design reason rather than a survival one: SMIL puts the timeline inside the
  SVG document, and our timeline lives in React, driven by build events.
- **CSS `@keyframes` as the primary mechanism** — i.e. what the sketch currently does. Rejected in §7.1
  and §7.2 for two concrete, reproducible defects. Retained as the fallback layer.

### Where the timings live

DTCG v2025.10 defines **`duration`**, **`cubicBezier`** and a composite **`transition`** type
([format module](https://www.designtokens.org/tr/drafts/format/), draft report dated 30 July 2026;
the stable revision remains [v2025.10, announced 2025-10-28](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)).
Style Dictionary ships `time/seconds`, `cubicBezier/css` and `transition/css/shorthand`
([transform reference](https://styledictionary.com/reference/hooks/transforms/predefined/)); latest
version **5.5.2**, verified from the npm registry on 2026-08-26.

So the state timings are tokens, not CSS literals. See §7.8.

---

## 3 · Where the mark lives, and what breaks there

| Surface | Motion? | Token colours? | What breaks |
|---|---|---|---|
| Inline SVG in the app | yes | yes | nothing — this is the only surface that works fully |
| SVG favicon | **no** | OS-scheme only | see below |
| `.ico` / PNG favicon | no | baked | still required — Safari |
| OG / social image | **no** | baked | 1200×630 static |
| Apple touch / PWA icon | no | baked | 180, 192, 512 static |
| `<img src="scio.svg">` | CSS-only, sandboxed | **no** | no custom properties, no `currentColor` |

**The constraint that spans every row: an SVG referenced from outside the document is CSS-sandboxed.**
External stylesheets cannot reach in, page custom properties do not resolve, and `currentColor` resolves
against the SVG's own initial value, not the page's
([frontendmasters.com, *Using currentColor in 2025*](https://frontendmasters.com/blog/using-currentcolor-in-2025/);
CSS Linked Parameters is on the standards track and is not shipping today). The sketch draws its colours
from `var(--ink)` / `var(--accent)`, which is exactly right in-app and impossible everywhere else. The
mark therefore needs **two builds**: the live React component, and a set of flattened per-theme assets
with token values baked in at build time by the same Style Dictionary run. That is pipeline work, and it
is how the token contract actually reaches the brand assets instead of stopping at the app boundary.

### Animated favicons — the thing that sounds possible

It is not, and the negative result is worth having in writing.

- **Chromium: closed, "not planned."**
  [chromium-dashboard issue #3595](https://github.com/GoogleChrome/chromium-dashboard/issues/3595),
  opened 2024-01-19, asked for animated GIF/SVG/SMIL favicons. Closed as not planned.
- **Firefox animates them. Safari does not.**
- **SVG favicon support at all** is Chrome 80+, Firefox 41+, and — the surprise —
  **Safari only from version 26.0** ([caniuse `link-icon-svg`](https://caniuse.com/link-icon-svg)).
  The `.ico`/PNG fallback is not legacy hygiene in 2026; it is the live Safari path.
- **The JS frame-swap workaround has a fatal property for our use case.** `canvas.toDataURL('image/png')`
  is expensive, and in Chrome/Edge `requestAnimationFrame` throttles to roughly **1 fps once the tab is
  in the background** — which is exactly the moment a build-progress favicon would earn its keep.

**Rule: never animate the favicon. Swap between a small set of static per-state icons.** That is
cheap, works in every browser, survives background tabs, and has a precedent (§5).

### Dark mode in an off-page SVG

`prefers-color-scheme` inside an SVG works **only if the `<style>` is inline in the SVG file** — which
is the standard technique and is fine. Two traps:

1. It resolves against the **OS setting**, not the page's `color-scheme` or our `data-theme`.
   [csswg-drafts #7213](https://github.com/w3c/csswg-drafts/issues/7213) asked whether it should be
   context-dependent; it is closed with a CSSWG resolution, and today browsers render every SVG image on
   a page identically regardless of the container's scheme. A user on OS-light with Scio forced to dark
   gets the wrong-polarity favicon, and we cannot fix it from the page.
2. Browsers do not re-evaluate the favicon on a scheme change without a reload.

In-app, use [`light-dark()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark)
(Baseline 2024, since May 2024) or plain tokens. Off-page, ship both polarities and accept the mismatch.

### Social and app icons

OG images are static. 1200×630 (1.91:1) is the cross-platform figure; an animated GIF as `og:image`
animates on Discord and **shows frame one everywhere else**. Keep total OG weight ≤ ~300 KB for
WhatsApp. This means one frame of the mark becomes the public face of it — choose it deliberately, and
choose **idle**, because a still frame of a spinning gear is a lie about the product's thesis.

### Responsive logo

Current practice is a *system* of marks at declining detail — full, simplified, icon, monogram — tested at
16 px, in dark mode, in motion, and as an app icon. The sketch's "drop the teeth below 24 px" is the right
instinct. Verify the 16 px case by rendering: two eye rings, two pupils and a beak inside an 8 px inner
circle is five shapes in very few pixels.

---

## 4 · Restraint — the floor, stated as rules

The bar is **WCAG 2.2 AA**. WCAG 3.0 is a Working Draft — [updated 2026-03-03](https://www.w3.org/WAI/news/2026-03-03/wcag3),
now ~174 requirements, Candidate Recommendation not anticipated before Q4 2027 and Recommendation not
before 2028. Do not build to it. Do watch APCA.

1. **Motion runs only when a state is true.** This is a design position that happens to buy compliance.
   [SC 2.2.2 Pause, Stop, Hide (Level A)](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
   requires a pause/stop/hide mechanism for auto-starting motion that lasts **more than five seconds** and
   is presented alongside other content. A mark that is still at idle never triggers it. A `building`
   state, however, routinely exceeds five seconds — so either the motion is argued as *essential* to
   conveying build progress (defensible, since that is its entire function) or the app offers a global
   "reduce motion" control. **Ship the control.** It is one token flip and it removes the argument.
2. **`prefers-reduced-motion: reduce` means reduce, not delete.** MDN is explicit that the intent is a
   muted alternative, and its own example swaps a `scale` pulse for an `opacity` fade. Our five states must
   remain readable with zero motion — via colour, opacity, or a discrete step — or the mark's honest
   signal is withheld from exactly the users least served by other feedback. See §7.4.
3. **The state must also be non-visual.**
   [SC 4.1.3 Status Messages (Level AA)](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
   covers indicators reporting "the progress of a process" and requires they be programmatically
   determinable without taking focus. A `role="status"` live region carrying the state name is mandatory,
   not a nicety. A logo is not an accessible progress indicator.
4. **Compositor properties only, in loops.** `transform` and `opacity`. The `done` state's
   `stroke` change is a one-shot paint and is acceptable; a `stroke` or `fill` in a repeating keyframe is not.
5. **Stop on `visibilitychange`.** A gear turning in an unfocused tab is battery with no observer.
   (This is also a documented practitioner rule for dynamic favicons.)
6. **No claim about how many users have reduced motion enabled** — see §1.

### On the evidence for restraint

Be honest about its strength. The cognitive-load research is real but is about *instructional*
animation: irrelevant motion adds extraneous load and the "seductive details" effect reduces learning
([ScienceDirect, attention-guiding effect and cognitive load in animations](https://www.sciencedirect.com/science/article/abs/pii/S0747563210001469);
[TPGi, *The impact of motion animation on cognitive disability*](https://www.tpgi.com/the-impact-of-motion-animation-on-cognitive-disability/) —
practitioner synthesis, not a controlled study of logos). **I found no measurement that a continuously
spinning logo degrades task performance.** The CPU/battery case is stronger and mechanical: non-compositor
animation forces layout/paint every frame; compositor-only animation does not.

So the argument for state-bound motion is **an honesty argument, not an ergonomics one**, and it should be
made that way. A logo that spins during idle is telling the user something is happening when nothing is.
That is the failure this project already names in its own diagnosis.

---

## 5 · The field

### Motion bound to state: one verified precedent, and it isn't a logo

**GitHub changes the favicon on pull-request and Actions pages to reflect check status** — pending,
success (green check), failure (red X), merged (purple). It is a static swap, not an animation, and it
works because it extends the UI into the browser chrome where the user is already looking.
([Detail, *Dynamic Favicon*](https://detail.design/detail/dynamic-favicon);
[refined-github #368](https://github.com/sindresorhus/refined-github/issues/368) shows the community
building it before GitHub shipped it.) **This is the pattern Scio should copy for the favicon, exactly.**

Beyond that, verification thins out fast, and I will not pad it:

- **Linear** publishes a brand page. It covers spacing, sizing and monochrome use, says *"Do not alter
  these files in any way"*, and **says nothing about motion at all**
  ([linear.app/brand](https://linear.app/brand), fetched 2026-08-26).
- **Vercel** is reported to use the triangle in loading animations within a strict monochrome system —
  secondary sources only; I could not verify a binding to deployment state.
- **Anthropic, OpenAI, Cursor, Replit, Lovable, v0, Raycast, Figma** — no primary documentation of
  state-bound mark motion for any of them. Trade coverage asserts a 2026 trend of "motion-first"
  identities where the static logo is a hero frame extracted from a kinetic sequence
  ([We and the Color](https://weandthecolor.com/best-logo-design-trends-of-2026-whats-working-whats-tired-and-whats-next/209969);
  [marcocagnina.com](https://marcocagnina.com/blog/logo-animations-trends-2026)). **That is opinion, from
  people who sell logo animation.** Treat it as evidence of fashion, not of effect.

**Conclusion: "brand mark as loading indicator" is a recognised, common pattern** — splash screens,
spinners with the logo centred. **"Brand mark as a state machine driven by real backend events" is not a
pattern I could find in this field.** We are not inventing animated logos. We may be inventing the
discipline of running one only when something is true — and that is a defensible thing to be first at,
provided we say it that way rather than claiming the animation itself is novel.

### Gear iconography: saturated, and the risk is functional, not aesthetic

Blunt numbers, all 2026-08-26: Flaticon lists **17,590** free "cog gear" icons and **13,696** "settings
cog"; Adobe Stock returns **537,315** for "cog icon"; iStock **203,900+**. Font Awesome ships `gear` in
its core solid set. Design writing lists gears among the standard clichés — "heavy, clunky, and
remarkably un-innovative in a digital-first economy"
([Inkbot, *25 Worst Logo Design Clichés*](https://inkbotdesign.com/logo-design-cliches/)) — and notes
that clichéd marks are harder to protect because they are not original.

The aesthetic objection is survivable. **The functional objection is not, and the sketch does not address
it:** a gear glyph is *the* settings affordance in essentially every interface, including the ones Scio
generates. A gear sitting in the product chrome is a control a first-time user will try to click. The
synthesis sketch partly escapes this by putting a face inside the ring, which no settings icon has — that
is the strongest argument for direction 3 and it is currently made on aesthetic grounds when it should be
made on this one.

### Owl iconography: less crowded, but occupied by a giant

Counts: Noun Project ~**2,946** owl icons; Flaticon **4,551**. Roughly a quarter of the gear volume.

Volume is not the problem. Recognition is:

- **Duolingo** owns the most recognised owl in software, registered with the USPTO
  (Reg. No. 4588574, filed 2014-01-21, registered 2014-08-19) — and it means *knowledge and learning*,
  which is precisely Scio's intended reading of *scio*.
- **Hootsuite**'s Owly has been the brand's mascot since 2008, though
  [Owly left the logo](https://www.hootsuite.com/newsroom/press-releases/owly-disappears-from-the-hootsuite-logo).
- **Owl Labs Inc.** holds a registration whose mark is *"the image of an owl to the left of the words
  OWL LABS"* in Class 9 ([USPTO 88000095](https://uspto.report/TM/88000095)); **Owl Technologies**
  holds OWL3D ([98877017](https://uspto.report/TM/98877017)); **Arcadyan** holds OWL in the
  computer/software category.
- In AI agents specifically: **CAMEL-AI's OWL** (Optimized Workforce Learning), 🦉-branded, GAIA
  leaderboard #1, accepted at NeurIPS 2025 ([github.com/camel-ai/owl](https://github.com/camel-ai/owl)).

**Not legal advice, and I am not qualified to give it.** But: a stylised owl inside a gear, for a
developer tool, is very unlikely to be confused with a green cartoon owl teaching Spanish, and the
existing registrations are word-plus-design marks in adjacent goods. The honest recommendation is that a
**professional clearance search in Classes 9 and 42 before the mark goes on a public site** is cheap
relative to the cost of a rename after launch, and that it should happen before this becomes an ADR.

---

## 6 · Design as a standing process

What exists today, verified, that an ongoing design agent could actually stand on.

**Agent-facing design tools**

- **Figma MCP** — remote and desktop servers. Figma's
  [May 2026 release-notes roundup](https://help.figma.com/hc/en-us/articles/40219873508247-Release-notes-roundup-May-2026)
  documents agents, MCP, skills and write-to-canvas, with `/figma-use`, `/figma-generate-design` and
  `/figma-generate-library`. At **Config 2026 (2026-06-24)** Figma shipped **Figma Motion** — a native
  keyframe timeline with easing and springs — **and animation export from Dev Mode to CSS, JSON, React,
  animated SVG, MP4/WebM/GIF** (four independent secondary reports; figma.com's own post 404'd for me).
  That last item is directly relevant: it is a motion source-of-truth that emits code. It still inherits
  the skill's existing verdict — **later**, only if a user brings a Figma system.
- **Penpot MCP** — official, first version December 2025, five tools, tokens returned as CSS rather than
  proprietary units. Open source and self-hostable. **This fits ADR-0001's ownership promise better than
  Figma does**, and it is the cheaper thing to try first.
- **Chrome DevTools MCP** — launched September 2025, v0.26.0 in May 2026, 44 tools including
  `take_screenshot`, `performance_start_trace`/`stop_trace` and `performance_analyze_insight`
  ([Chrome for Developers](https://developer.chrome.com/blog/chrome-devtools-mcp);
  [repo](https://github.com/ChromeDevTools/chrome-devtools-mcp)). **This is the piece that makes a design
  agent deterministic rather than opinionated** — it can measure the mark's frame cost instead of judging
  its vibe.

**Deterministic gates — extending `app-design/SKILL.md` §5 with motion**

The existing six checks (token adherence, contrast, scale, state coverage, theme completeness, focus
visibility) have no motion row. Four more, all computable, none needing a model:

| Check | Fails when | How |
|---|---|---|
| **Motion-token adherence** | a duration or easing literal appears in a component | grep, same rule as hex literals |
| **Idle stillness** | any animation is running while state is `idle` | `document.getAnimations().filter(a => a.playState === 'running').length === 0` |
| **Reduced-motion honoured** | same assertion under emulated `prefers-reduced-motion: reduce` | Playwright emulation + the same one-liner |
| **Frame cost** | the `building` state exceeds a frame budget | Chrome DevTools MCP performance trace |

The idle-stillness gate is the one that enforces this document's entire thesis, and **nothing off the
shelf does it.** It is four lines of Playwright.

Supporting, already-existing machinery: **axe-core 4.13.0** (MPL-2.0, verified on npm) covers `blink`
and `marquee` for SC 2.2.2 and **nothing else about motion**; Deque's own figure for automated coverage
is ~57% of issues by volume. **Playwright `toHaveScreenshot` with `animations: 'disabled'`** — which
finishes transitions instantly and pauses infinite animations — gives per-state, per-theme visual
regression; capture all five states × two themes as a single baseline grid.

**Cadence.** Most of this domain moves slowly and a weekly scan would be theatre:

- **Quarterly** — DTCG spec revision, Style Dictionary major, Baseline changes we depend on.
- **Twice a year** — the browser-capability claims in §3. They go stale silently and cost most when wrong.
- **Event-triggered, never scheduled** — the competitive field in §5. Scan it when a competitor rebrands.
- **Every time the mark changes** — re-run §3's surface list. A checklist, not research.

---

## 7 · What this changes about the sketches already drawn

*Scanned against `logo-sketches.html`. `logo-factory.html` was written in parallel and independently
avoids §7.2; every other item applies to both unless noted.*

This is the part worth reading. `logo-sketches.html` is right about the *idea* and has concrete defects in
the *mechanism*, and one of them undermines the idea.

**7.1 · The `thinking → building` transition visibly jumps. This is the transition the product performs
most often.** The sketch sets `animation-duration: 14s` for thinking and `2.2s` for building on the same
`.rotor`. Changing `animation-duration` mid-flight does not restart the animation — the browser keeps the
elapsed time and recomputes progress against the new duration
([CSSWG discussion of dynamic changes to animation properties](https://lists.w3.org/Archives/Public/www-style/2014Oct/0314.html)).
Concretely, at t = 5 s: `5/2.2` → 98.2°; `5/14` → 128.6°. **A 30.4° jump.** Fix: WAAPI +
`updatePlaybackRate()` (§2), which exists for exactly this.

> **Corrected on review.** This item originally read *"nearly two tooth pitches on the 22-tooth
> ring"*. Both halves are wrong. `stroke-dasharray="22 21.98"` is a 22-unit **dash**, not 22 teeth:
> 2π·84 = 527.79 over a 44-unit period is **12 teeth**, so the pitch is 30.0° and the jump is
> **one tooth pitch**, not two. The defect is real and the fix is unchanged; the magnitude was
> overstated 2×. Verified by computation, 2026-08-26.

**7.2 · `idle` and `done` teleport the gear back to 0°.** *(Applies to `logo-sketches.html` only.
`logo-factory.html`, written after this scan was commissioned, already uses
`animation-play-state: paused` throughout and does not have this defect. The finding stands for the
earlier file and as a rule for the build.)* `animation: none` removes the animation, so the
element reverts to its untransformed rotation. The document's own argument is *"it stops, so the stop is
visible"* — but a stop that snaps backwards reads as a glitch, not as a stop. Fix: `animation.pause()`,
never cancel.

**7.3 · The `done` settle animates `scale`.** Scale is a vestibular trigger and MDN's canonical
reduced-motion example replaces exactly this with an opacity fade. Use opacity or a stroke step for the
settle. Compositor-safe either way; safer for the same cost.

**7.4 · The reduced-motion block deletes the signal instead of reducing it.**
`animation: none !important` on everything means a user with reduced motion sees an inert mark in all five
states. **The mark's entire justification — that motion is the cheapest honest signal in the product —
silently fails for that user.** Every state needs a non-motion representation: teeth colour, pupil size,
an opacity step. That is a missing design requirement, not an implementation detail, and it is the same
"honest signal computed and discarded" failure the project already diagnoses.

**7.5 · There is no state announced to assistive technology.** `role="img"` with a fixed `aria-label` is
correct for the drawing and useless for the state. SC 4.1.3 (AA) applies. Add a `role="status"` region
carrying the state name.

**7.6 · There is no `failed` state.** idle / listening / thinking / building / done. A build system with
no visible failure state repeats precisely the omission `app-design/SKILL.md` §4 calls a quality bar —
and failure is the state a user most needs to read from a background tab, which is where the favicon
swap (§3, §5) earns its place. **Add `failed`. Five states become six.**

**7.7 · Direction 2's "gear train" is a circle rotating about its own centre.** `.rotor-sm` contains
`<circle cx="100" cy="100" r="17">` with `transform-origin: 100px 100px`. **Rotating it is a visual
no-op.** The caption says "gear train and two cylinders, out of phase"; the file contains one gear, one
hub, and two cylinders. Either draw a real second gear off-axis with meshing teeth, or drop the claim.

**7.8 · Every timing is a CSS literal.** 9 s, 4.5 s, 1.6 s, 0.53 s, 14 s, 2.2 s, 0.75 s, 900 ms. DTCG has
`duration`, `cubicBezier` and `transition` types, and Style Dictionary transforms all three (§2). The
skill froze colour, spacing, type and radius as a contract and **left motion out**. As written, the mark
is the only component in the system permitted to invent values — which is the exact thing §1 of the skill
forbids. **Motion joins the token set.**

**7.9 · Minor: the tooth dash is not commensurate with the circumference.** `r="84"` gives
2π·84 = 527.79; `stroke-dasharray="22 22"` is a 44-unit period, 11.995 repeats. The seam is sub-pixel at
200 px and roughly half a pixel on a 512 px app icon. Compute the dash from the circumference
(`527.7876 / 12 / 2 = 21.9911`) rather than rounding. Direction 2 already does this more carefully.

**7.10 · Three animated groups is the right budget and should be treated as a ceiling** — Chrome does not
split a single SVG into multiple GPU layers (§2).

### Contradictions with `app-design/SKILL.md`

- **§6b's "what exists" table has no motion row.** It should gain three: *DTCG duration / cubicBezier /
  transition — **adopt**, do not invent timing conventions*; *Rive — **rejected** for a single mark on
  measured cost (~835 KB gz), revisit for an illustration system*; *Figma Motion (June 2026) —
  **later**, same verdict as Figma MCP and for the same reason.*
- **The Style Dictionary caveat is half stale.** The skill says "v4 supports DTCG, full v2025.10 support
  still landing in v5. Pin and verify rather than assume." v5 has shipped — **5.5.2** as of today — and
  the caveat's substance still holds: [styledictionary.com/info/dtcg](https://styledictionary.com/info/dtcg/)
  still states full 2025.10 support is a work in progress in v5. Update the version, keep the warning.
- **§5's design gate needs the four motion checks from §6 above.** Contrast is still the highest-value
  check; idle-stillness is the highest-value *new* one, because it is the only gate that can fail a mark
  for dishonesty.
- **No contradiction on tokens, presets, or the derivation argument.** That scan holds.

### What does not change

The synthesis is still the right drawing, and for a better reason than the sketch gives. Direction 3
survives not because a gear is an O but because **the face is what stops it being a settings icon**
(§5). And the governing idea — motion bound to state — survives every check in this document: it is the
cheapest route through SC 2.2.2, it is the only version of the mark that is not lying at idle, and it is
the one thing in the competitive field I could not find anyone else doing.

---

## 8 · Sources

All accessed **2026-08-26**.

**Technique** — MDN: [`<animate>` (SMIL)](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/animate), [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API), [`updatePlaybackRate()`](https://developer.mozilla.org/en-US/docs/Web/API/Animation/updatePlaybackRate), [`prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion), [`light-dark()`](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark) · caniuse: [WAAPI](https://caniuse.com/web-animation), [SVG favicons](https://caniuse.com/link-icon-svg) · [CSS-Tricks — SMIL on?](https://css-tricks.com/smil-on/) · [blink-dev — Intent to deprecate SMIL](https://groups.google.com/a/chromium.org/g/blink-dev/c/5o0yiO440LM/m/YGEJBsjUAwAJ) · [Chrome — hardware-accelerated animations (Chromium 89)](https://developer.chrome.com/blog/hardware-accelerated-animations) · [CSSWG — changes to animation-* while running](https://lists.w3.org/Archives/Public/www-style/2014Oct/0314.html) · sizes measured locally from jsDelivr: [`@rive-app/canvas` 2.40.1](https://www.jsdelivr.com/package/npm/@rive-app/canvas), [`lottie-web` 5.13.0](https://www.jsdelivr.com/package/npm/lottie-web), [`@lottiefiles/dotlottie-web` 0.79.2](https://www.jsdelivr.com/package/npm/@lottiefiles/dotlottie-web) · [Bundlephobia `@rive-app/webgl2`](https://bundlephobia.com/package/@rive-app/webgl2) · [Rive pricing](https://rive.app/pricing) · [rive-react](https://github.com/rive-app/rive-react)

**Surfaces** — [chromium-dashboard #3595, animated favicons closed not-planned](https://github.com/GoogleChrome/chromium-dashboard/issues/3595) · [csswg-drafts #7213, prefers-color-scheme in SVG images](https://github.com/w3c/csswg-drafts/issues/7213) · [Frontend Masters — Using currentColor in 2025](https://frontendmasters.com/blog/using-currentcolor-in-2025/) · [tomayac — prefers-color-scheme in SVG favicons](https://blog.tomayac.com/2019/09/21/prefers-color-scheme-in-svg-favicons-for-dark-mode-icons/) · [Favicon.im — animated favicons demo](https://favicon.im/blog/animated-favicon-live-demo) · [Cloudinary — dynamic favicon with JS](https://cloudinary.com/blog/guest_post/build-dynamic-favicon-with-javascript) · [Detail — Dynamic Favicon (GitHub status favicon)](https://detail.design/detail/dynamic-favicon) · [refined-github #368](https://github.com/sindresorhus/refined-github/issues/368) · [OG image sizes & platform specs](https://opengraphimage.com/blog/og-image-sizes-specs-and-the-one-mistake-that-breaks-every-preview) · [webtoolkit — favicons in 2026](https://www.webtoolkit.tech/guides/favicons-in-2026)

**Accessibility** — W3C WAI: [SC 2.2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html), [SC 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html), [WCAG 3 Working Draft 2026-03-03](https://www.w3.org/WAI/news/2026-03-03/wcag3) · [Web Almanac 2025 — Accessibility](https://almanac.httparchive.org/en/2025/accessibility) · [TPGi — motion animation and cognitive disability](https://www.tpgi.com/the-impact-of-motion-animation-on-cognitive-disability/) *(practitioner synthesis)* · [ScienceDirect — attention-guiding effect and cognitive load in animations](https://www.sciencedirect.com/science/article/abs/pii/S0747563210001469) *(instructional animation, not logos)* · [axe-core 4.13.0](https://github.com/dequelabs/axe-core) · [Deque automated coverage report](https://www.deque.com/automated-accessibility-coverage-report/)

**Tokens & process** — [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/) · [first stable version, 2025-10-28](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) · [Style Dictionary predefined transforms](https://styledictionary.com/reference/hooks/transforms/predefined/) · [Style Dictionary DTCG support](https://styledictionary.com/info/dtcg/) · [Figma May 2026 release notes](https://help.figma.com/hc/en-us/articles/40219873508247-Release-notes-roundup-May-2026) · [Figma MCP server guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) · Config 2026 (2026-06-24), secondary only — figma.com's own post 404'd: [CMSWire](https://www.cmswire.com/digital-experience/figma-launches-code-layers-motion-at-config-2026/), [Qubika](https://qubika.com/blog/figma-config-2026-announcements-for-designers/), [uinkits](https://www.uinkits.com/blog-post/figma-config-2026-everything-announced-from-code-layers-to-figma-motion) · [Chrome DevTools MCP](https://developer.chrome.com/blog/chrome-devtools-mcp) + [repo](https://github.com/ChromeDevTools/chrome-devtools-mcp) · [Penpot MCP coverage](https://www.buildmvpfast.com/blog/penpot-mcp-ai-agent-design-system-open-source-figma-2026) *(secondary)* · [BrowserStack — Playwright snapshot testing 2026](https://www.browserstack.com/guide/playwright-snapshot-testing)

**Field & iconography** — [linear.app/brand](https://linear.app/brand) *(primary; no motion guidance)* · Flaticon: [cog gear](https://www.flaticon.com/free-icons/cog-gear), [settings cog](https://www.flaticon.com/free-icons/settings-cog), [owl](https://www.flaticon.com/free-icons/owl) · Noun Project: [owl](https://thenounproject.com/browse/icons/term/owl/), [gear-cog](https://thenounproject.com/browse/icons/term/gear-cog/) · [Inkbot — 25 worst logo clichés](https://inkbotdesign.com/logo-design-cliches/) *(opinion)* · [We and the Color — logo trends 2026](https://weandthecolor.com/best-logo-design-trends-of-2026-whats-working-whats-tired-and-whats-next/209969) *(opinion)* · [marcocagnina — logo animations 2026](https://marcocagnina.com/blog/logo-animations-trends-2026) *(opinion)* · [camel-ai/owl](https://github.com/camel-ai/owl) · [USPTO 88000095 — Owl Labs](https://uspto.report/TM/88000095) · [USPTO 98877017 — OWL3D](https://uspto.report/TM/98877017) · [Hootsuite — Owly leaves the logo](https://www.hootsuite.com/newsroom/press-releases/owly-disappears-from-the-hootsuite-logo)

---

*Scan only. No decision is made here and no ADR is proposed yet — per `CLAUDE.md`, propose, do not
assume. The recommendations in §2 and the defects in §7 are the input to that decision, not the decision.*
