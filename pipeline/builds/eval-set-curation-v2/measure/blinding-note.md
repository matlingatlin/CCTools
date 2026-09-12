# 6.1b — blinding, done BEFORE the expectation set was written

Six arm outputs, relabelled R01..R06 and reordered with a **new** seed (778899, not the one used
for the first, discarded blinding). Key at `key/key.json`, sha256 `89173ccad7725aae28f63b3a34a037783cab8a9e1b792c92e5b57fdd6dda38ab`.

**Order of operations, which is the whole point of this file.** The arms ran (6.1). The outputs
were blinded and the key was closed (6.1b, this file). Only then was the judgement half of the
expectation set written, and it was written from the files under their R-labels. The
fixture-computed half was written earlier still — while the arms were mid-flight — because no
arm's answer can move a count or a Wilson half-width, which is the exception the chain contract
grants and the only part of the expectation set that could honestly be written early.

**What was NOT blind.** Two of the original six runs returned no answer at all and I opened them
with their labels on, because the only way to act on a broken run is to know which run broke. Both
are in `void/`. One is a single sentence about attachments; the other is one paragraph about a
near-duplicate threshold. Neither answers Q1-Q4. The exposure is real and bounded and is recorded
in the build record rather than argued away.

## Content tells, measured rather than assumed

| label | "the method" | "step N" | claim ids | "tolerance" | chars |
|---|---|---|---|---|---|
| R01 | 0 | 1 | 0 | 0 | 8628 |
| R02 | 1 | 1 | 1 | 2 | 9278 |
| R03 | 0 | 0 | 0 | 0 | 12326 |
| R04 | 0 | 0 | 0 | 0 | 8966 |
| R05 | 1 | 0 | 2 | 4 | 8537 |
| R06 | 0 | 0 | 0 | 0 | 7442 |

Read this before the key. Any column where the six split cleanly is a channel a grader could use,
and it is reported as a bound on the blinding rather than as a claim that the blinding is total.
The `tolerance` column is the one to watch here: it is this build's own vocabulary, so it may
separate the with-arm from BOTH others — which is exactly the comparison the verdict turns on, and
a stronger tell than the previous build's, which could not.
