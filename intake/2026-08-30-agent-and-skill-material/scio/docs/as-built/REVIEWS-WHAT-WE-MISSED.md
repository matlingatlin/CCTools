# What the reviews say that our layer analysis missed

Six review documents in hello-world, ~3,265 lines, read 2026-08-26 after the seven layer
documents were finished. Not a verification of their 35 findings — a check for **what is in
them that our own analysis did not surface.**

Six things. Two change conclusions we had already written down.

---

## 1 · Five placeholder routes, not one

Our `LAYER-F` and `JOURNEY-INVOLVED-PATH` both name Settings as the placeholder. `App.tsx`
lists five:

```ts
const PLACEHOLDERS = [
  { path: "/live",          title: "Refine" },
  { path: "/versions",      title: "Versions" },
  { path: "/settings",      title: "Settings" },
  { path: "/states",        title: "Error & empty states" },
  { path: "/notifications", title: "Notifications" },
];
```

**`/live` — "Refine" — is the one that matters**, and missing it changed a conclusion.

`docs/UX-FLOW.md` defines two involvement levels, and says of Level 1:

> Level 1 does not remove control — it moves shaping to AFTER the build (on the running app)
> instead of BEFORE it (on a preview). The UI should make this clear so Level 1 does not read
> as the lesser path.

**Level 1's entire value proposition is a placeholder page.** A user who chooses "just build
it, I'll shape it after" arrives at a screen that says it is being ported from the prototype
next. `/versions` and `/notifications` are steps 7 of the same flow.

Our journey document concluded that the gap sits at *the two ends* of the user's path. That is
too kind. The whole post-reveal half is unbuilt, and one of the two involvement levels has
nowhere to land.

## 2 · Five product invariants we never carried up

`PRODUCTION_READINESS_DIFF.md` §2 states five non-negotiables. They are *product* contracts and
they do not overlap with the five *code* invariants in `ARCHITECTURE-AS-BUILT.md`:

1. **Nothing is built without a contract.** Every function traceable to an approved
   requirement, a visible assumption, or a technical necessity.
2. **No change without impact analysis.** Affected requirements, architecture nodes, packages,
   files and tests identified **before code is written**.
3. **No unauthorised diff.** Changes outside the decided surface are rejected or require fresh
   approval.
4. **No promotion without verification.**
5. **No hidden failure.** The user sees what changed, was tested, passed, failed, and could not
   be verified.

Number 2 is the one our analysis has no equivalent for. We documented per-marking resolution
in Layer F; *impact analysis before code is written* is a stronger and broader claim, and we
never checked whether it exists.

**And the precisification is better than the promise we have been repeating:**

> The promise is not that literally only the marked component changes. A change can require
> legitimate consequential changes… The right promise is: **only the smallest
> dependency-complete and explained area changes.**

## 3 · There is a written spec for the reveal, and reveal shows a fraction of it

§7 defines "very high quality" as measurable, across functional, code, test, security and UX
quality — and then lists nine things **reveal should show**:

requirements met and unmet · tests and browser flows · security checks · changed packages and
files · verified-unchanged surface · model and build cost · build time · remaining risks ·
version id and export.

We found one symptom of this — `checks_passed` computed, typed, transmitted and never
rendered. The actual specification is nine items wide, and reveal shows a small part of it.

Two of §7's quality bars are directly contradicted by `LAYER-E`:

| §7 requires | Layer E found |
|---|---|
| central user flows have been run in a browser | the two interaction gates are **opt-in** behind `SCIO_VERIFY_DATA=1` |
| unit, component, integration and browser tests | **nothing runs the generated app's own tests** or `next build` |
| dependency and code scanning performed | CI has no SAST, dependency audit or secret scanning |

## 4 · "We have a component library" is not a differentiator

§8 is competitive analysis we never did, and it bears directly on any plan to import a large
component collection.

Lovable already publicly ships: versioned design systems with tokens and adherence checks, a
managed private npm registry, cross-project referencing of components, layouts, auth flows and
integrations, and remix/templates.

> This means "we have a component library" is not in itself a sufficient differentiator.

What is *not* publicly documented at Lovable — and therefore where Scio's edge could be:
automatic contribution from every successful build; generalisation away from project-specific
terms; re-verification after generalisation; **contract-based automatic matching before
generation**; quality evidence per reused feature; Pareto replacement of older
implementations; assembly first with generation as fallback.

**The consequence for the plan to download a large block library:** thousands of shadcn blocks
give *visual* components. §8 says the advantage has to be **feature-based, contract-matched,
tested and security-reviewed**. Importing a visual collection buys the half that is explicitly
not the differentiator — and each import would arrive without a `Contract`, which
`LAYER-D` shows is the thing that makes matching decidable at all.

The document also warns against over-weighting the library:

> The library is an amplifier, not the precondition for proving the core. The core loop must
> work well even when everything has to be generated.

## 5 · A defined MVP, and a defined not-yet list

§9 names what Lovable is far ahead on and says not to chase parity first: hosting and custom
domains, managed backend, GitHub sync, collaboration, payments, a connector catalogue, mobile
and desktop, enterprise SSO and governance, compliance, support.

§10 defines the minimum product that proves Scio, as a numbered external-user journey.

`docs/PRD.md` and backlog item B005 (MVP scope, non-goals, metrics) are recorded as still open
in `RETHINK-BRIEF.md`. **§9 and §10 are most of that unfinished artifact**, written and
apparently never promoted into the PRD.

## 6 · Our verified baseline is less solid than we stated

The consultant review records **B105: `design.test.tsx` is flaky** — two different tests failed
on two consecutive runs, three later runs were clean, cause not found.

We ran each suite **once**, got green, and wrote it down as a verified baseline. One green run
does not refute an intermittent failure. The baseline in `00-INDEX.md` should be read as *one
observation*, not as proof of stability.

The consultant is explicit about the same class of limit elsewhere: the CI workflow had never
run, the Docker sandbox had never run a build, and no load, soak or failure testing was
performed — *"everything about concurrency in this document is reasoned from code, not
measured."*

---

## What the reviews got right, and the code has since fixed

Worth recording so nobody re-opens them. The consultant's two non-negotiables:

**B2 — the Docker sandbox silently discarded the environment it was given.** Fixed. There is
now a provider conformance suite, and the test names the original bug:
`test_every_provider_passes_the_callers_env_to_the_app` — *"The one the Docker provider failed
for a long time."*

**B3 — Docker containers orphaned on shutdown.** Fixed:
`test_shutdown_reaches_both_kinds` — *"The first version of this walked only the local
registry, so on the host `choose_sandbox` prefers it reported success and leaked every
container."*

`sandbox.py` also carries the reasoning for the secret leak it closed: the child used to start
with `**os.environ`, so *"`process.env.ANTHROPIC_API_KEY` was one line away, and an app that
merely logged its own environment would have put the platform's key in a log."* There is a test
asserting the *absence* of a secret, which is the hard direction to test.

---

## Still outstanding

The 35 findings in the two root reviews have **not** been verified one by one. Four have been
checked, incidentally rather than systematically:

| Finding | State | How |
|---|---|---|
| F-03 · idempotency replay precedes ownership guard | **live** | verified here, three ways |
| F-16 · suspicious package names `httpx2`/`httpcore2` | **false positive** | genuine Pydantic-org packages by httpx's author. The other half — no hashes in the lockfile — stands |
| F-17 · clickable `div` cards | already fixed | per `RETHINK-BRIEF.md`, not re-checked |
| F-04 · active build reaped during silence | live | per `RETHINK-BRIEF.md`, not re-checked |

Two of those four are taken on the brief's word rather than checked against code.

*Read 2026-08-26. `RUNBOOK-CONTINUOUS-IMPROVEMENT-LOOP.md` excluded by request.*
