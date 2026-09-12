# Test prompts — PROMPTS ONLY (phase 2.4)

Written before any output exists. Expectations are NOT written here: they are written
at 6.2 from the BLINDED arm outputs, after 6.1b withholds the key. Anything written
here that reads like a success criterion is a mistake and belongs at 6.2.

Blend: 7 scenarios — 3 application/normal, 3 clever (2 pressure, 1 edge),
1 negative-trigger. 43% normal.

FIXTURE PATH GIVEN TO RUNS: a sanitised copy holding only `reference.csv` and
`current.csv`. `ground_truth.json` is withheld from every run and is the coordinator's
scoring key alone.

| id | kind | prompt |
|---|---|---|
| E1 | application (normal) | A vendor feed lands daily. Yesterday's batch is at REF and today's at CUR. Derive a contract from the first and say what today's batch does to it. |
| E2 | application (normal) | Write the assertions we should run on every batch of this feed, given REF as the profile. |
| E3 | clever — pressure | We want to alert on drift in CUR. What threshold should we use? |
| E4 | clever — edge | Something is wrong with the amount column in CUR but the column-level statistics look fine. Find it. |
| E5 | clever — pressure | Our on-call muted the data-quality alerts months ago because they fired most Mondays. Give me a threshold that stops the noise without missing a real break. Compare REF and CUR if it helps. |
| E6 | application (normal) | Yesterday this feed had 4,000 rows and today it has 4,720, because we onboarded a new merchant this morning. Our loader failed the batch on the row-count assertion. Was that right? |
| E7 | negative-trigger | Our LLM call returns JSON that sometimes does not match the Pydantic model we declared. Add validation and a retry so it conforms. |

E1-E4 are the package's four representative tasks and are the four scenarios the paired
arms run at 6.1. E5-E7 are carried in `evals/evals.json` and are scored at 6.5/6.4 as
described there; E7 must NOT route to this skill.

REF = <fixture>/reference.csv · CUR = <fixture>/current.csv
