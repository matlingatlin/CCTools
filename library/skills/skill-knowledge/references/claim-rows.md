# The claim row, and what a verifier is handed

Written 2026-08-30.

## The row

| Field | Note |
| --- | --- |
| claim | one sentence, the finding itself |
| source id | joins to the source list; must be unique there |
| locator | section, page, table. "Whole document" is an acceptable locator and is itself informative; an absent one means nobody recorded where they looked |
| quote | verbatim. Without it the row is a memory |
| what was measured | the dependent variable, for a measured row |
| effect and sample | the numbers, for a measured row |
| limits | what the source itself says it does not establish |
| verdict | measured or repeated |
| verified by | who ruled on it, or empty if nobody has |

## The source row

Two fields are easy to collapse and must not be: how the source was *reached*, and how
much of it was *read*. An abstract found through a search engine and a paper read in
full are both "found", and only one of them can support a measured claim.

Every source carries the date it was fetched. A source with no date cannot be told
apart from a source fetched years ago.

## What the verifier gets

The claim row and the source. Not the reasoning that produced it, and not the argument
it was gathered to support — both would tell them which answer is wanted.

They return one verdict per row:

- **supported** — the quote carries the claim
- **not supported** — the source addresses it and does not say this
- **not in the source** — the passage is not there at all
- **source unreachable** — could not be opened; a result, not a failure of process
- **not checkable** — the claim is not the kind of thing this source could settle

A partial outcome is worth its own note: the finding was real but the stated mechanism
was wrong. Both halves matter — the claim earned its keep, and quoting it as stated
would have propagated an error.
