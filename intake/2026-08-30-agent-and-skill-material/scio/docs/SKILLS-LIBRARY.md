# Skills at three levels — and the one we already have is a library of one

**Status: proposed.** Nothing decided. Written 2026-08-26 from what the mining measured.

---

## The observation that makes this worth writing down

Layer B ships a **`Playbook`** into every build prompt. The as-built table marks it in one word:
**`constant`**.

A restaurant booking app and a B2B tender platform get byte-identical house rules. The stack is the
same, the folder structure is the same, the secure-by-default list is the same — and so is
everything else, because there is nothing else.

**The Playbook is a skills library with one entry.** Framed that way, the question stops being
*should we build a skills library* and becomes *why does the library have one entry when Layer D
already knows how to select from many?*

That is the whole proposal.

---

## The three levels, and why they are genuinely different

| Level | Runs when | Lives in | What it shapes |
|---|---|---|---|
| **1 · Build-time** | we work on Scio | `scio` | how *we* build |
| **2 · Generation-time** | Scio builds someone's app | Scio's engine | how the *generated app* is written |
| **3 · Delivered** | the user works on their own app, later | the generated repo | how *they* keep building |

The existing rule — *build-time here, runtime there* — collapses levels 2 and 3, and they are not the
same thing. Level 2 shapes generation and the user never sees it. Level 3 ships **with** the app,
and is the natural completion of ADR-0001's promise: code the user owns, with a smooth handoff to a
developer. Handing over the code and withholding the instructions for working on it is half a
handover.

Level 3 is also the only one with a business shape. A generated app that arrives knowing how to
extend itself is worth more than the same code without that, and it costs nothing extra to ship
files we already have.

---

## What level 2 would actually be

Not new machinery. **Layer D's machinery, pointed at instructions instead of components.**

`Contract` is three sorted string lists plus a subset-and-equality test — deliberately decidable
without judgement. A skill entry needs the same shape: *what does this app need,* matched against
*what does this skill cover,* with no model deciding.

The inputs already exist in Layer A's spec: **app-kind**, `users_and_roles`,
`data_ownership_sensitivity`, the declared integrations. A booking app pulls the booking-domain
skill; an app touching health data pulls the sensitivity rules; an app with one role pulls neither
the multi-tenancy nor the permissions material.

Two of the three things this needs are already measured and sitting in `docs/mined/`:

- **Selection by concern × context**, with the selection made at install time rather than per
  request — ECC's `rules/` matrix.
- **A catalog that stays inside a budget**: an aggregate token cap, a **260-byte per-entry** limit,
  and the mechanism that makes the cap survivable — **split every description**, lead sentence in
  always-loaded frontmatter, routing prose in a body section fetched only when the entry is chosen.
  Plus a **shrink floor** beside the growth cap, because an entry that collapses to 250 bytes passes
  a noise check while losing everything.

The third — which entry wins when two match — is Layer D's existing problem and does not need a
second answer.

---

## Where this collides with what we have measured, and it collides hard

**We have 302 findings and zero evals.** A skills library is a mechanism for *scaling* the delivery
of skills. Scaling something we cannot verify multiplies an unmeasured thing.

The one skill measured today **made the answer worse** — `as-built` produced a confidently wrong
count because our own documents disagreed, while the arm without it got the answer right. That is a
single observation on one question and not a verdict on the skill. It is, however, the only
evidence we have about any of them.

So the ordering is not negotiable: **a library needs the eval before it needs the second entry.**
Otherwise it distributes confident wrongness at scale, which is exactly what a library is good at.

Three more, from our own record:

- **Consent and licence.** The component library already assembles entries derived from one tenant's
  build into another's app with **zero consent, licence or attribution anywhere**, and
  `library_entry` has no origin key, so a contribution can be neither traced nor withdrawn. A skills
  library inherits that problem on day one rather than acquiring it later — and one repository we
  mined carries a Commons Clause defining "the software" as every file including prompt JSON, so
  the question is live, not theoretical.
- **Drift.** The vendored `graphify` skill was 1,208 lines and wrong against a package that ships
  713. One skill drifted. Seventeen can. A library of a hundred certainly will, and the pin plus a
  loud staleness check has to exist before the hundredth entry, not after.
- **Duplicates.** Measured today: highest description overlap across our seventeen is **0.11**, well
  under threshold. No duplicates *yet* — and 253 take-verdicts are queued. The check exists
  (`scripts/skills-index.py`); the discipline of running it does not.

---

## What is already true and should not be re-invented

- `claude plugin eval` exists, is ablation-controlled, and is **early-access gated** for us. The
  measurement has a destination and no road yet.
- `skill-comply` — 1,421 lines of working Python — measures behavioural compliance with scenarios up
  to actively competing instructions. **Theirs is better than ours because ours does not exist.**
- Plugins plus a marketplace are the distribution mechanism, settled by the documentation, and a
  plugin already bundles skills, agents, hooks and MCP config in one install. **A skills library is
  a marketplace with more than one plugin in it.** That is not new infrastructure; it is the same
  infrastructure with entries.

---

## The order this has to happen in

1. **Measure one skill properly.** Not seventeen — one, with an eval that survives repetition.
2. **Split the Playbook's fixed content from its selected content.** The house rules that apply to
   every app stay constant; anything that varies by app-kind becomes an entry. This is a Layer B
   change and it is where the value starts.
3. **Second entry.** The library exists the moment there are two, and every mechanism above is
   testable at two that is untestable at one.
4. **Consent, licence and origin — before any entry derives from a user's build**, not after.
5. **Level 3 last.** Shipping skills with a generated app is the most valuable and the least
   urgent: it needs levels 1 and 2 to be worth shipping.

Steps 2 and 3 are small. Step 1 is blocked on nothing but effort. Step 4 is a decision, not a build.

---

*Per `CLAUDE.md`: propose, do not assume. Each numbered step above becomes an ADR before it becomes
a fact.*
