# 2026-09-12 — one row, two releases, and three instances of one failure shape

`84 unchanged · 1 changed · 11 noise · 0 tampered`. The changed row is
`MakazhanAlpamys/Soup`'s README — a GitHub README, the weekly class, and the second non-`code.claude.com`
change in the tally.

The diff replaced the **v0.74.0** release block with **v0.75.0**, which means **v0.74's figures had been
sitting in the 2026-09-11 baseline and were never read into the note.** A re-baseline would have
destroyed them. Both releases are now recorded in `local-finetuning-layer-streaming`; that is the
argument for reading a diff before re-baselining, stated concretely rather than as a principle.

## Why this one earned a long write-up

**v0.75.0 fixes, in a single release, three separate cases of a setting being accepted and then
silently ignored** — the shape this base keeps finding in other people's surfaces:

1. an unknown config key was *"dropped while the run proceeded with the setting not applied"*; now it
   refuses the load, **breaking, and telegraphed** — *"v0.74 warned and named this release as the
   deadline"*;
2. six training options were *"each validated and then dropped on `backend: mlx`"*, so one `soup.yaml`
   trained a different recipe per backend, silently. 24 of 32 optimizer names are now **refused by
   name** instead of falling back to AdamW;
3. validation loss *"was computed on every backend and thrown away"* — an honest signal computed and
   then dropped, which is word for word the failure Scio's ADR-0001 says that project documented in its
   predecessor five times over.

Three independent projects, one shape. Kept as a vendor's worked example of fixing it rather than as
one more instance of suffering it.

Also: `grpo_variant: gspo` moved to the published objective (arXiv:2507.18071) and **existing gspo
configs will not reproduce prior runs** — a reproducibility break stated plainly; SSE and Web UI reads
now need auth via short-lived single-use tickets rather than a query-string token; `torch>=2.6.0`
closes v0.74's own published known limitation, under which every preference trainer was dead.
