# Abstention threshold decision record

<!-- Shape only. Every angle-bracketed slot is filled from measurement, not from judgement.
     A slot with no number is an unfinished decision, not a stylistic gap. -->

**System:** <what produces the answer being gated>
**Decided on:** <date>   **Holdout:** <n cases, drawn from what, over what period>
**Re-validate by:** <date or event - new model, new prompt, new index, traffic shift>

## 0. Is there anything to threshold?

**Scored, labelled holdout in hand:** <yes / NO>
**Where it is:** <file, table, query or ticket - a locator someone else can open>
**What is in it:** <n cases> · <date range> · <how sampled> · <who labelled them>

Every number in sections 2, 3 and 6 is computed from the holdout named on this line, and
each of those tables states the n it was computed over. A row whose n cannot be traced back
to this locator does not belong in the record.

**If NO - stop here.** Sections 2 to 4 are DELETED, not left blank, and the record is
delivered with sections 0, 1 and 5 only. Name what has to be pulled (scores plus a
correct/incorrect label, n cases, from where) and who pulls it. A coverage number with no
locator above it is a guess wearing a table.

*What this section cannot do: nothing here can force the yes to be true. It can only make a
false yes a specific written claim with a locator attached, which is checkable by whoever
receives the record, instead of an unstated assumption.*

## 1. The two numbers, fixed before the scores were read

| | value | owner (person or role who agreed it) | agreed on |
|---|---|---|---|
| precision / quality target on the ANSWERED segment | <value> | <name> | <date> |
| minimum acceptable coverage (the floor) | <value> | <name> | <date> |

## 2. Signals tested for separation

| signal | AUROC vs correct/incorrect | bucket accuracy monotone? | verdict |
|---|---|---|---|
| <signal> | <value> | <yes / no - which buckets invert> | <usable / discarded> |

Signal carried forward: <name>. Discarded: <name(s)>, because <reason>.
**If every candidate came back at chance:** say so and stop. There is no cut on a signal that
does not separate; sections 3 and 4 stay empty and the next action is a different signal, not
a different number.

## 3. Sweep

| cut | coverage | answered n | precision on answered | abstained volume / <period> |
|---|---|---|---|---|
| <cut> | <value> | <n> | <value> | <n> |

Every row is computed from section 0's holdout. If section 0 says NO, this table has no rows -
it does not get a range, an estimate, or a band.

## 4. The cut, and what it cost

**Chosen cut:** <value> - the HIGHEST-coverage row meeting the target.
**Buys:** <coverage> coverage at <precision> precision.
**Rejected in favour of it:** <cut> at <coverage>/<precision> - it would have surrendered
<n> points of coverage, <n> cases per <period>, to gain <n> points of precision.
**If no cut met both numbers:** <which target was missed, by how much, and who was asked to
choose - relax, improve the signal, or do not ship autonomously>

## 5. The abstained path

**Receiver:** <person, team, queue, fallback, or degraded answer>
**Capacity:** <n per period> against **<n per period>** abstained. Headroom: <value>.
**Latency the user sees:** <value>   **What the user is shown:** <text>

## 6. Slice check

| slice | coverage | precision on answered | meets the target? |
|---|---|---|---|
| <slice> | <value> | <value> | <yes/no> |

## 7. Monitoring

**Abstention rate now:** <value>. **Alarm if it leaves:** <band>.
**What the alarm means:** the score distribution moved, so the same cut is now a different
decision - re-run sections 2 to 4.
