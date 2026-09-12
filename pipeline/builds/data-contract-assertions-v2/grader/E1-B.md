Contract derived, asserted, and run. Files in the working directory: `contract.yml`, `assert_batch.py`, `assertions_2026-09-02.csv`, `assertions_v1_2026-09-02.csv`, `holdout_coverage.txt`.

## Verdict: BLOCK = 4, WIDEN = 4

Eight differences, each on exactly one side. Row counts are on both sides of every measurement.

### BLOCK (4) — contradicts something the producer is committed to

| | Difference | Segment | Reference → Current |
|---|---|---|---|
| **B1** | `settled_days` type break: `" d"` suffix on 1184 rows | none — batch-wide | 4000/4000 bare int → 2816 int + 1184 suffixed |
| **B2** | `amount` in cents while `currency`='USD' | merchant=belltower | zero-cent share .0104 (n=479) → **1.0000** (n=440) |
| **B3** | 38 large zero-cent amounts | merchant=harborview | no prior rows → .1583 (n=240) |
| **B4** | `customer_age` presence collapse | channel=android | .0161 (n=806) → **.8312** (n=788) |

Each carries its rival benign reading and the measurement that beats it. B1's "deliberate format change" reading dies on the suffix share being flat at .264–.375 across all 9 merchants, 4 channels and 4 statuses — a partial per-row branch, not a migration. B2's "belltower got expensive" reading dies on 440/440 rows losing the cents place, and on ÷100 reproducing the reference belltower distribution (median 27.29 vs 32.75, p95 108.21 vs 109.84). B4's "vendor stopped collecting age" reading dies on ios/web/phone being unchanged.

**B3 is not resolved, and I am not reporting this as belltower-only.** The zero-cent signature separates belltower from the seven incumbents (1.0000 vs ≤.0148) but does **not** separate harborview at .1583. Both readings stay open: 202 of its 240 rows are ordinary fractional amounts with a median (29.68) inside the reference merchant range, and the 38 large rows are scattered through the file — a genuine B2B tail. But those 38 are structurally identical to belltower's confirmed cents rows (arbitrary integers, 3/38 multiples of 10; ÷100 lands them on the reference distribution). Any bound in (.0256, .1583] flags harborview; any bound in (.1583, 1.0) does not. **The harborview verdict is decided by where the bound is put, not by the data.** I assigned it BLOCK scoped to the 38 rows because unblocking is the irreversible direction — harborview's other 202 rows pass, and the merchant itself is ratified.

Also worth knowing: viewed per *merchant*, B4 shows all nine merchants elevated (.1416–.2004). The merchant cut is the wrong segmentation and would have produced nine findings instead of one.

### WIDEN (4) — extends a set the producer never closed

**W1** `harborview` (240 rows) and **W2** `chargeback` (90 rows) are amendments, not failures. Both applied: `ALLOWED_MERCHANTS`/`ALLOWED_STATUSES` widened, and the re-run confirms those two assertions go FAIL→PASS (v1: BLOCK=4 WIDEN=3 → v2: BLOCK=4 WIDEN=1). **W3** status-mix drift is the chargeback carve-out — band voided, not re-set, because re-deriving from the firing batch fits one day. **W4** channel mix (web .5172→.4165, ios .2605→.3685) is not the new merchant: excluding harborview the mix is unchanged (.4162/.3691) and all 8 incumbents show the ios rise independently.

The onboarding batch is not refused.

## On the numbers

**No harm bound exists in this contract, and none can be derived from this feed.** There is no control total, remittance file, bill, or labelled outcome to observe moving. Every distributional bound is a **noise** bound — it licenses "this batch is unusual", nothing about cost (threshold-evidence C12, Contradiction 3). The four BLOCK verdicts rest on type/unit contradictions and on separations wide enough that the bound's value is not load-bearing: belltower fires at any bound in (.026, 1.0), android at any bound in (.025, .83). The one place the number *does* decide the outcome is B3, and that is flagged rather than quietly settled.

Two numbers are `NOT DERIVED` and non-gating: the **capacity bound** (no owner and no read-budget were given — the contract emits 34 rows per batch, 13 of them per-segment cells that grow with merchant count) and **row_count** (two data points is not a range).

Held-out coverage (derived on reference rows 1–2000, measured on 2001–4000): all exact assertions and both banded checks 1.0000. **Profiled min/max was tested and not shipped** — `amount between [1.56, 499.68]` scores 0.9990 on held-out *clean reference data*, failing before any batch arrives (C6, C7).

**`NOT BACKTESTED — history: one prior batch.`** No firing count exists, so every distributional check is held observe-only. Only the exact assertions gate now — they have no derived bound and fire on type/key violations, not thresholds. The channel-mix band (0.06) is the weakest number in the file and I've said so in place: it was derived from two halves of *one day*, which measures within-day variation when a mix band needs day-to-day.

Not exercised: no consuming code was run against the schema. W2 is the live case — nothing in the batch is wrong about `chargeback`, but a consumer whose revenue sum has no chargeback branch is now wrong, and no assertion here can see it (C5).

**Next action:** ask the vendor two questions — the unit on belltower and on harborview's 38 rows, and what changed in the android client. A per-merchant settlement total from the remittance file is the single artefact that would convert B2/B3 from "unusual" to "off by 100× against money actually moved" and resolve B3, which the data alone cannot.
