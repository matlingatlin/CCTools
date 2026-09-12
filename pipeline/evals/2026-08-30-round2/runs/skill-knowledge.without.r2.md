# skill-knowledge — without — round 2

## Q1

Added, but not as a fact. The sentence is a vendor-shaped anecdote ("In our experience…"),
with no n, no baseline, no measurement method, and "roughly in half" is a rounded
recollection, not a result. It goes in as a REPORTED claim with the hedge preserved verbatim,
so nothing downstream can quietly promote it to a number.

Claim row:

| id | claim | verdict | source | source_type | fetched | scope | notes |
|----|-------|---------|--------|-------------|---------|-------|-------|
| C-lint-01 | A team reports that adding a linting step to CI cut code-review time "roughly in half". | REPORTED | <blog post URL + post title + author> | engineering blog, first-party experience report | 2026-08-30 | one team, unnamed; no n, no baseline, no measurement method stated | Quoted hedge is the author's ("In our experience", "roughly"). NOT measured, NOT repeated — a single unaudited self-report. Do not restate as "linting halves review time" or as a 50% figure. Usable as motivation for a skill step, never as its justification. If the skill needs a real effect size here, that is an open research item. |

Two operating consequences, recorded with the row:
- The skill may say "teams report lint-in-CI reduces review load"; it may not say "cuts review
  time by 50%".
- Flagged for corroboration: if a second independent source with an actual measurement turns up,
  the row gets upgraded and the blog becomes supporting, not load-bearing.

## Q2

Knowledge work happens now, in this turn — not at the end of the probe, and not when someone
asks for a write-up. Two things that were not known before are now known and checked, so two
new claims land, and they are marked differently from the nine we already had.

The nine proposal-stage claims were PROPOSED: assertions about what the skill should catch,
written before anything ran. The two probe failures are OBSERVED: they came from an actual run
against an actual agent. That difference is the whole value — do not let them merge into one
undifferentiated list of eleven.

Add:

| id | claim | verdict | source | fetched | notes |
|----|-------|---------|--------|---------|-------|
| C-10 | An agent reviewing a schema migration did not check whether the migration holds a lock past the request timeout. | OBSERVED (probe, 1 run) | probe run <run-id>, 2026-08-30 | 2026-08-30 | Baseline failure. Single observation — a real miss, not yet a rate. Gives the skill a required check: lock duration vs request/statement timeout. |
| C-11 | The same agent did not name which service reads the renamed table, i.e. it did not trace downstream readers of a renamed object. | OBSERVED (probe, 1 run) | probe run <run-id>, 2026-08-30 | 2026-08-30 | Baseline failure. Gives the skill a required check: enumerate readers/writers of every renamed or dropped object before approving. |

Then, in the same turn:
1. Re-check the nine. Each probe failure either (a) corresponds to a proposal claim, which is
   now corroborated by observation and should be re-stamped from PROPOSED to OBSERVED with the
   probe cited, or (b) does not, in which case we just learned the proposal stage had a blind
   spot — record that as a finding about our own proposal process, not only about the skill.
2. Note the inverse too: proposal claims the probe did NOT exercise stay PROPOSED. Do not let a
   passing probe launder them into verified.
3. Each observed failure becomes a named eval scenario (baseline fails, with-skill passes), so
   the two misses are what the skill is tested against, not just what it is documented against.

Explicitly not done: no averaging of proposal and probe into a single confidence, no rewriting
of a proposal claim's wording to match what the probe happened to find.

## Q3

An abstract is a source, but it is the authors' own summary of their result, not the result.
The number is quotable; the conditions under which it holds are not in hand, and effect sizes
in abstracts are routinely the best-case arm. So the row records the claim, and records loudly
that the full text was never read.

| id | claim | verdict | source | source_type | access | fetched | notes |
|----|-------|---------|--------|-------------|--------|---------|-------|
| C-<n> | <Effect as stated, quoted verbatim from the abstract, with its exact percentage and its exact comparison, e.g. "X reduced Y by NN% relative to Z"> | REPORTED — ABSTRACT ONLY, full text not read | <authors, year, title, venue, DOI/arXiv id> | peer-reviewed paper (or preprint — state which) | paywalled; abstract only | 2026-08-30 | UNVERIFIED against the paper body. Not checked: n, population, baseline/control, whether the figure is absolute or relative, confidence interval, preregistration, conflicts of interest, whether NN% is the headline arm or the only significant one. Do not restate without the "abstract only" qualifier. Do not combine with other effect sizes into a pooled number. |

Follow-ups attached to the row so they are not lost:
- Try the accessible routes before treating this as settled: author preprint or institutional
  copy, arXiv/PMC version, the author's own request line. If a full text is obtained, re-verify
  every field above and re-stamp the verdict.
- If the paper stays out of reach, the skill may cite the paper as motivation but must not rest
  a threshold, a default, or a rule on NN%.

## Q4

Do not average them, do not pick the friendlier one, and do not delete the loser. A 15/40 spread
is not noise to be tidied away — it is the finding. Almost always the two numbers are measuring
different things, and the cleanup is to make that visible.

What I do to the reference file:

1. Split the single claim into two rows, one per source, each with its own verdict, date, and
   scope. Neither row is allowed to state the bare number without its scope clause.
2. Add a CONFLICT row above them that names the disagreement and holds the resolution state:

   | id | claim | verdict | notes |
   |----|-------|---------|-------|
   | C-<n>-conflict | Sources disagree on <quantity>: <source A> reports 15%, <source B> reports 40%. | CONTESTED — unresolved | Candidate explanations, unchecked: different denominators; different populations or time windows; different definitions of the measured event; one is self-reported, the other instrumented; one is relative and one absolute; different versions/dates of the same system. Until one of these is confirmed, no single number for <quantity> may be used downstream. Anything that needs a number uses the range 15–40% and says it is contested. |

3. Give the contested quantity one owning entry so the two figures cannot drift into separate
   corners of the file and be cited independently as if uncontested.
4. Then the actual tidy, which is separate from the conflict and should not hide it: one row per
   claim, stable ids, every row carrying source + fetch date + verdict, no orphan numbers with no
   source, duplicates merged only where the claim AND the scope are genuinely identical, and
   superseded rows marked superseded rather than deleted so the history of what we believed
   survives.

If ten minutes of reading the two sources' methods sections resolves it, do that now and record
the resolution with the reason — a resolved conflict is worth more than either number was. If it
does not resolve, it stays CONTESTED, in writing. "The file is messy" is not a reason to make a
disagreement disappear.

## Q5

Not yet — one thing first, and it is quick.

Verdicts by themselves are not enough to bundle on, because the reference file has to carry not
just what you concluded but what a reader needs to re-check it. Before it goes in, each row needs:

- the source identified precisely enough to re-fetch (URL/DOI + title, not "the blog post"),
- the fetch/read date, since a live page's claim is only true as of a date,
- the scope the claim actually holds at (population, n, time window, version),
- the verdict stamped per claim, not per source — one document routinely contains one verified
  claim and three unsupported ones, and a source-level verdict launders the weak ones,
- and, for anything you marked verified, the specific thing in the source that verified it —
  the quote, section, or figure. "I checked it" is not re-checkable; "Table 3, p.7" is.

So: send me the verdicts with those fields filled and it bundles immediately. Two checks I will
run on the way in, both cheap:

- Any claim whose verdict is verified but whose evidence pointer is missing gets downgraded, not
  bundled — no exceptions, because that is exactly how an unsupported number becomes load-bearing
  three weeks later.
- Contested or hedged claims keep their hedge verbatim into the file. Bundling is the step where
  hedges quietly get dropped.

One more thing worth doing at bundle time rather than after: check the set against what already
exists in the reference file. If an existing entry already owns a topic, extend it rather than
adding a rival row — parallel-authored duplicates are much more expensive to reconcile later
than to prevent now.

## consulted

- /home/user/skills-repo/pipeline/evals/2026-08-30-round2/prompts/skill-knowledge.without.txt (the prompt itself)
- /home/user/skills-repo/CLAUDE.md (loaded automatically into context; not opened for this task)
- No skills invoked, and no files under pipeline/skills/, pipeline/contracts/ or pipeline/build/ were read. Answers are from general judgement.
