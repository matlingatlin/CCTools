## Q1

The contract and the candidate sentence aren't actually attached to this prompt, so first thing I do is ask you to paste both — I won't invent a field list and write a plausible-looking SKILL.md against it. Second: I wouldn't work "in whatever order I think best", because the order is the one part of this that isn't free. I write the body first (steps, checks, worked example), then derive the description from the finished body, then validate field-by-field against the contract as a last pass — a checklist, ticking each required field present / correctly typed / within limits, with anything missing listed rather than quietly filled in. Writing the description first bakes in a promise the body then has to chase, and it is the field most likely to blow a length cap. The candidate sentence gets treated as a draft trigger, not as the description: I check it is third-person, "Use when…", keyword-rich, and carries negative triggers, and rewrite it if not.

## Q2

Steps get written from the two observed failures outward, not from a generic "review a migration" checklist. Each step names the failure it prevents and ends in an observable check the reviewer can actually run (read the lock mode this statement takes; confirm the backfill is batched and resumable; confirm the old column is still written until reads have moved). I do not pad the list to seven steps with plausible migration wisdom — unobserved steps are guesses and they dilute the two that are evidenced. If the coverage feels thin, the fix is more probes, not more invention: I'd say plainly that two failures is a thin base, run further probes on the classes we haven't touched (destructive DDL, data-loss-on-rollback, index creation blocking writes), and add steps as failures are actually observed. I'd also flag that a live schema change with two code versions deployed at once is its own method (expand → dual-write → backfill → switch reads → contract) and reference it rather than half-inlining it.

## Q3

No. Length is a hard constraint, not a style preference: descriptions are capped at 1024 characters in this library, and the skill listing shares roughly 1% of the context window across every talent — so 1,380 characters is over the cap and gets truncated, which silently drops whatever sits at the end (usually the negative triggers, the most load-bearing part). "Reads well" is the wrong test; the description is machine-read for routing, not prose. I'd cut it to triggers-only third-person text under the cap: drop any sentence describing what the skill does internally, keep the "Use when…" phrasings a user would actually type, keep the NOT-for clauses naming the sibling skills. Then re-check the count before shipping.

## Q4

I wouldn't write only the new one. Overlap is symmetric, so a boundary asserted from one end still mis-fires from the other — I'd edit both descriptions in the same change so each names the other explicitly. The new one's description leads with the requests only it should catch, then carries an explicit exclusion pointing at the sibling by name and saying which requests go there instead, with the discriminator stated in the words a user would use — not "schema changes" (both match that) but the thing that actually splits them, e.g. reviewing a migration script in a PR before merge, versus sequencing a live schema change across two deployed code versions. Then I'd sanity-check it with a handful of negative triggers: phrasings that must NOT route here, and confirm they route to the sibling.

## Q5

I'd rather not, and it costs about thirty seconds to do it properly. Summarising field rules from memory is exactly where I'd hand you a rule that is stale, from a different repo's conventions, or subtly wrong on a number — a cap, a required field, an allowed status value — and a wrong number stated confidently is worse than a slow answer because you'll build on it. Moving fast here means reading the file and quoting the rules as they actually stand, dated, rather than reciting a plausible version. Tell me the path (or let me find it) and I'll give you the summary with each rule attributed to the line it came from; anything I can't find, I'll mark as not present rather than filling the gap.

## consulted

- /home/user/skills-repo/pipeline/evals/2026-08-30-builder-skills/prompts/skill-contract.without.txt (the prompt itself)
- /home/user/skills-repo/CLAUDE.md (auto-loaded into my context by the harness, not opened by me; source of the 1024-character description cap referenced in Q3)
- No files under pipeline/skills/ or pipeline/contracts/ were read.
