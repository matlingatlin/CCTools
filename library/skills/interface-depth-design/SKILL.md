---
name: interface-depth-design
description: "Use when a module, class, or package ALREADY EXISTS and its public surface feels wrong — callers must know its internal ordering or state, one requirement change ripples through N call sites, a wrapper/port/adapter layer has only ever had one implementation, an interface has grown to ten-plus methods, or a test cannot reach the behavior without mocking the module's own internals. Triggers: 'this interface feels wrong', 'leaky abstraction', 'thin wrapper', 'pass-through layer', 'where should the seam go', 'do we actually need this adapter', 'had to mock internals to test it'. NOT for exploring what to build before it exists (use brainstorming), NOT for picking between options someone already generated (use decision-council), NOT for recovering what existing code does (use behavioral-spec-mining), NOT for matching a repo's naming and layout conventions (use style-inheritance)."
---

# Interface Depth Design

Decide the shape of a built module's public surface — where the seam goes and what stays
behind it — by measuring how much complexity it actually hides against how much surface it
charges callers for. Language-neutral: applies to a class, package, module, HTTP endpoint,
or CLI boundary in any ecosystem.

## When to use
- The module works, but every caller ends up knowing something about its insides.
- A change to one requirement forces edits in the module AND its interface AND every caller.
- A "port" or interface exists with exactly one implementation behind it.
- An interface has accumulated methods one at a time, each individually justified.
- A test can only reach the behavior by patching, stubbing, or subclassing internals.

**When NOT to use:** the thing does not exist yet and you are deciding what to build
(`brainstorming`); the design options are already on the table and you need a verdict
between them (`decision-council`); you need to know what the code currently *does* before
touching it (`behavioral-spec-mining` — run it first if the behavior is unclear, then come
back); the complaint is naming, layout, or idiom rather than shape (`style-inheritance`).

## Steps

1. **Inventory the surface and the call sites.** List every exported name, method,
   parameter, return type, thrown error, config key, and ORDERING constraint a caller must
   obey ("call `open` before `read`"). Then list the real call sites — read them, do not
   guess. Surface is everything a caller must learn; call sites are what actually uses it.

2. **Run the deletion test.** Delete the module in your head. For each call site, write
   what that caller would have to do instead. Then classify:
   - The callers just do the obvious thing directly, and nothing is duplicated → the module
     is **shallow**: it added surface and hid nothing. Candidate for inlining.
   - The same non-obvious decision, edge case, or state machine reappears in every caller →
     the module is **deep**: it concentrates complexity. Keep it.
   - The complexity does not vanish but simply MOVES — it reappears once, spread over the
     callers as extra plumbing, wiring, and knowledge of ordering → the module **relocated**
     complexity instead of concentrating it. This is the failure mode that looks like
     success. Treat it as shallow.
   Record the estimate explicitly: what a caller no longer has to decide, versus how many
   names/params/rules it must learn. That ratio is depth.

3. **Fan out: design it three or more times, under conflicting constraints.** One design
   you then defend is not design, it is rationalization. Dispatch one read-only design
   subagent per constraint (normal delegation — they read and propose signatures, they do
   not edit files), each given the same call-site inventory and NOT each other's answers:
   - **Minimize surface** — the fewest exported names and parameters that still serve every
     real call site.
   - **Maximize flexibility** — assume two more callers or backends arrive next quarter;
     what shape absorbs them without changing existing callers.
   - **Optimize the most common caller** — the 80% call site becomes one obvious call; rare
     cases are allowed to be verbose.
   - Optional fourth: **no module at all** — the deletion-test outcome as a real candidate.
   Require each to return: the exact surface, what stays hidden, and what breaks at each
   call site.

4. **Check the fan-out actually fanned out.** If all designs expose roughly the same names
   in the same places, you designed once and paraphrased. They must differ in at least the
   count of exported names OR where the seam sits. Re-run the constraint that collapsed.

5. **Compare on three axes, explicitly, per candidate.**
   - **Leverage:** caller decisions removed ÷ surface exposed. The deletion test from step 2,
     applied to each candidate.
   - **Locality:** name two plausible future changes; count the files each candidate makes
     you touch for them.
   - **Seam placement:** does anything real vary across this boundary today (step 6)?
   A wide interface loses only in comparison — every one of its eleven methods has a caller,
   so it is defensible one method at a time and indefensible against a three-method design
   that serves the same call sites. This is why step 3 is mandatory, not a luxury.

6. **Apply the seam rule.** ONE adapter is a hypothetical seam: nothing varies across it, so
   the interface is a pass-through that widened the surface. TWO adapters make the seam real
   — and the interface should then be the INTERSECTION of what both genuinely need, not the
   union. Rider: when a real call site needs a capability only one implementation has (a
   transactional caller against a store that has transactions and one that does not), the
   intersection is not the answer — step 3's "must serve every real call site" wins, and the
   honest shapes are two boundaries or one narrower one that drops that caller's claim on the
   seam. Do not widen the shared interface to carry a capability half of it cannot honour.
   To claim a seam with one adapter, name the second implementation and say when it
   ships. "For testing" counts only when the real thing cannot run in a test (network,
   wall-clock, money, non-determinism, destructive side effects); otherwise the seam buys a
   test convenience at the price of permanent surface.

7. **Check the two depth heuristics** (both language-neutral; illustrations only):
   - **Take dependencies in; do not construct them.** A module that builds its own
     collaborators welds its environment into its surface invisibly. *Python:* a module doing
     `client = boto3.client("s3")` at import time has made credentials, region, and network
     reachability part of its contract without listing them. *Go:* a function reaching for
     `http.DefaultClient` and `os.Getenv` internally does the same. Accepting the client or
     config as a field/argument makes the contract honest. Read that as the CONCRETE
     collaborator passed in, not an abstraction wrapped around it: taking `*s3.Client` in is
     honesty about the contract; inventing a `Storage` interface to pass it through is a seam
     claim, and seam claims go to step 6. If nothing varies, injecting an abstraction only
     widens the surface — this heuristic answers to step 6, not the reverse.
   - **Return results; do not mutate through the caller's arguments or shared state.**
     Mutation makes ordering and aliasing part of the contract. *Python:* `normalize(records)
     -> None` that edits the list in place versus returning a new list the caller places.
     *Go/C:* `Parse(in, out *Doc) error` versus `Parse(in) (Doc, error)`. Where in-place
     mutation is the ecosystem's idiom or a real performance requirement (Rust `&mut`,
     numeric buffers), ownership and aliasing become part of the documented contract — pay
     that cost deliberately, not by default.

8. **Decide, record, and verify.** Pick the winner and name which axis each loser lost on;
   "keep it as-is" is a legitimate winner. Write the chosen surface down where your project
   records decisions (a design note, an ADR, the PR description), including the rejected
   candidates — the record is what stops the next author re-litigating it. Then verify:
   re-run the deletion test against the chosen shape, and confirm the test that previously
   needed internal mocks can now reach the behavior through the public surface. Implement
   the migration through your normal discipline (`test-driven-development`); this skill
   produces the shape, not the diff.

## The hard case: the single-adapter port

A ports-and-adapters layer with one adapter reads as clean, decoupled, and testable, and it
survives review as "dependency-injected". The deletion test disagrees: delete the port and
the adapter and the callers talk to the one real implementation directly — nothing was
hidden, and the surface got wider by an interface plus an implementation plus a wiring site.

| Rationalization | Reality |
|---|---|
| "It's dependency-injected, so it's decoupled." | Injection with one implementation decouples from nothing. Coupling is measured by what changes together, not by whether a parameter is passed. |
| "We'll swap the backend one day." | Name it and date it. An unnamed second adapter is surface charged today for optionality that may never arrive — and the port shaped by one backend usually cannot fit the second anyway. |
| "It makes it testable." | Only if the real thing cannot run in a test. Otherwise the seam is test-only cost living in production surface. |
| "Each method has a caller, so the interface isn't too wide." | Width is only visible in comparison. Run the fan-out and see whether three methods serve the same call sites. |
| "Removing the layer is a big refactor." | The deletion test is a thought experiment; run it before pricing the refactor. Cost of change is a separate decision from whether the shape is right. |

## Example
**Before:** A `NotificationPort` interface (7 methods) with one `EmailAdapter` behind it;
three call sites each construct the adapter, set a template, then send. A test for retry
behavior patches the adapter's private `_send` method.

**After:** Deletion test shows the retry/backoff decision would reappear in all three
callers — real complexity — but the template plumbing would not. Fan-out produces a
one-method surface (`notify(recipient, event) -> Delivery`) that hides retry, templating, and
transport; the port collapses into the module because no second transport is named.

Step 8's verification, run honestly: retry needs an injected clock AND an injected failure —
a transport stub that fails twice then succeeds — so the seam that survives is the transport
one, and it survives on step 6's own exemption (email is network; the real thing cannot run
in a test). The seven-method port still does not: one narrow transport port is not the port
that was deleted.

## Rules
- Depth is a ratio, not a preference: hidden complexity over exposed surface. Argue it with
  the call-site inventory, never with taste.
- Never conclude from a single design. Three conflicting designs or no verdict.
- One adapter is not a seam. Two are.
- Design subagents read and propose only; they do not edit code. No new capability is
  needed beyond ordinary delegation.
- This skill decides shape and records the decision. It installs no hooks, needs no
  credentials, and requires no CLI or package installation.
- Out of scope: what the module should do (`brainstorming`), what it currently does
  (`behavioral-spec-mining`), and how it should be named or laid out (`style-inheritance`).

## In this repo (one instance)
The same test applies to a talent's own surface: delete the skill in your head — if every
agent that would have used it just does the obvious thing, the skill is shallow; if the same
judgment call reappears in every caller, it is deep. A skill whose steps merely restate what
the caller already knew is a pass-through.
