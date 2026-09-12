# Per-field inputs and the reader's question

Written 2026-08-30. This table is the part of phase 4 that changes least; the rules
themselves live in the contract file and are read from there at write time, never
copied here.

Each row: what must already exist before the field can be written, and the single
question handed to the independent reader afterwards. The reader gets the field, the
contract rule and nothing else — they must not be able to see how it was produced,
because a critique of your own reasoning measures worse than no critique at all.

| Field | Must already exist | The reader is asked |
| --- | --- | --- |
| bill of materials | the scope sentence, the probe's findings | Is any row unclassified, or classified with a reason that is not a reason? |
| references | the claim set, each with a verbatim quote | Does each quote carry the claim beside it, or is it adjacent text? |
| assets | the shape of the output the skill emits | Could someone fill this in without asking what a field means? |
| name | the directory it will live in | — decided by the contract |
| what and when | the scope sentence, the observed failures | Would a reader who has this problem recognise it here in one line? |
| the steps | the observed failures, quoted | Is every rule traceable to a named observation? Does every step end in something checkable? |
| pointers | the finished bundled files | Does each pointer say what is inside and when to open it? |
| description | the finished body, the trigger vocabulary, the neighbours | Which unit would a router pick for the neighbour's job, and why not this one? |
| frontmatter | the content kind | — decided by the contract |

## Two failure modes worth naming

**Writing the description first.** It is the field most often drafted at the start
because it feels like a summary of intent. It is not: it is a router's only input, and
it can only be written once the scope has stopped moving. A description written first
describes the skill somebody meant to build.

**Rules with no observation.** The steps section attracts general good advice, which is
free to write and expensive to carry — it occupies context on every single invocation
and it cannot be measured, because nothing was failing without it. The test is
mechanical: name the run.
