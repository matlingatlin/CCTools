# Lock modes

Fetched 2026-08-30 from a synthetic fixture source. Invented content; cite nothing here.

| Statement | Typical lock | Upgrades under load |
| --- | --- | --- |
| add nullable column | brief metadata | no |
| add column with default | rewrite on older engines | yes |
| create index concurrently | shared | no |
| rename table | exclusive | already exclusive |

Where an engine rewrites the whole heap, duration scales with row count, so a change
that finishes instantly on an empty development copy can hold production for minutes.
