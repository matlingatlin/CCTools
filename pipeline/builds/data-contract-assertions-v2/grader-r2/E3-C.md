Before picking a number: I compared `current.csv` against `reference.csv` in the same directory. Most of what a threshold would fire on here isn't drift.

## What's actually in the file

| Column | PSI | What it really is |
|---|---|---|
| `settled_days` | **3.54** | Format bug — `"1"` → `"1 d"` on 1,184 rows. Normalize the suffix and PSI is **0.0016**. Zero real drift. |
| `merchant` | 0.67 | New merchant `harborview` (6%). Business event, not a defect. |
| `customer_age` | 0.45 | Null rate 1.4% → 17.8%. **655 of 713 nulls are `android`** — 83% of android rows. Localized ingestion bug. Age distribution among non-nulls is unchanged (48.17 → 48.16). |
| `status` | 0.23 | New category `chargeback` (2.25%), spread evenly across all 9 merchants. Looks genuinely new. |
| `amount` | 0.11 | **`belltower` is reporting in cents** — all 440 rows whole-numbered, median 2726.50 vs 32.75; ÷100 gives 27.27. Excluding it, amount PSI is **0.006**. |
| `channel` | 0.06 | ios +10.8pp, web −10.1pp. The one thing here that looks like real behavioral drift. |

## The problem with a single threshold

The standard 0.1 warn / 0.25 alert would fire on `settled_days`, `merchant`, `customer_age`, `status` — three bugs and one business event. Meanwhile:

- **`channel` (0.06) stays silent** — the only plausible genuine drift sits below any threshold you'd reasonably pick.
- **The cents bug scores 0.109** — barely at the warn line, despite inflating total volume 12× (164K → 1.99M). PSI bins on reference deciles, so everything oversized lands in the top bucket and the magnitude is invisible.

Tuning a threshold to this file means tuning it to bugs, and you'd still miss the two things that matter most.

## What I'd do

**Fix the three defects first** — the ` d` suffix, belltower's cents, android's null ages. Any threshold calibrated before that is calibrated to noise.

**Then PSI 0.1 warn / 0.25 page is fine**, applied post-normalization and per-column, with `merchant` excluded from paging (new merchants are expected; alert on unseen categories as an info-level event instead).

**Add the guards PSI structurally can't provide:**
- **Schema/format assertions** — `settled_days` matches `^\d+$`, `amount` parses as 2-decimal currency. Catches the format bug at ingest, at full severity, instead of as a PSI score.
- **Null rate per column *per segment*** — a global null check would've read 17.8% and shrugged; sliced by channel it's an 83% failure on one path. Alert at ~3× reference rate.
- **Magnitude checks on `amount`** — per-merchant median ratio vs reference, alert outside 0.5–2×. Belltower's 83× ratio trips this instantly; PSI gave it 0.109.

For `channel`, if that ios/web shift matters to you, it needs its own explicit rule — a PSI threshold low enough to catch 0.06 would fire constantly on everything else.

One thing I'd flag rather than assert: `harborview` has a normal median (35.00) but 35 of 240 rows above 600 and a mean of 608. Could be legitimate large transactions for a new merchant, or the same cents bug on a subset — worth confirming with whoever onboarded them, since it's too few rows to call from the data alone.
