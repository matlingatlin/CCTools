# The watcher's first real batch, 2026-09-08

Four rows reported CHANGED. **One carried a content change.** That ratio is the first
measurement of this watcher's signal-to-noise, and it is why the row-level triage below matters
more than the count.

| source | what actually changed | verdict |
|---|---|---|
| `MakazhanAlpamys/Soup` README | a new `## Web UI` section — `soup ui` serves a local dashboard at `127.0.0.1:7860`, `pip install "soup-cli[ui]"` | **REAL.** The note is updated |
| `diegosouzapw/OmniRoute` README | "169 migrations" → "171 migrations" | true change, **immaterial**: we cite stars, the free-token pool and the compression range, never the migration count |
| `unsloth.ai/docs/models/glm-5.3` | GitBook deploy id, asset hashes, chunk numbers | **noise.** Zero words changed |
| `unsloth.ai/docs/models/glm-5.3-flash` | same | **noise** |

## The normaliser that was written and deleted

The two GitBook pages looked like a fixable noise class, so a narrow normaliser was written for
the deploy id (`?dpl=p-…`, **681 occurrences per page**). It did not close the gap: the bundler's
asset content-hashes churn too, and past those the **chunk numbers themselves differ** (`9495`
against `9455`) — the bundle splitting changes on every deploy. No narrow rule makes such a page
stable, and a wide one is how a watcher quietly stops watching. It was removed rather than
widened, and `watch.py` carries the measurement in place of the code.

Both rows are **kept**: the pages carry claims this base cites (the quantisation table in
`glm-5.3-local`). They are annotated as KNOWN-NOISY in `WATCH.tsv` so a reader triages the diff
instead of trusting the row.

## What the batch added to the watcher

A second, different question the tool was never asking: **is our own stored copy still the bytes
we recorded?** The raw layer is immutable by rule and nothing checked it. `watch.py` now verifies
each stored file against its recorded sha and reports `TAMPERED` separately from `CHANGED`, and
fails on either. Currently 0.

Nothing here was edited after fetching; every file is stored as received.
