# Five sources recovered, 2026-09-08c — the drops of 2026-09-04 reversed

Nothing new was discovered here. These are pages this base already cited and had **given up on
watching**, and the reason they are watchable today is a change made to the tool this morning.

## What was dropped, and why

`baseline-2026-09-04/README.md` records four pages *"dropped from the watch list for returning
different bytes on two fetches seconds apart"*, with the reasoning: **"A baseline that reports
CHANGED every run is worse than no baseline: it trains the reader to ignore the watcher."** That
was right, and it was the best available answer while the watcher could only compare bytes.

It also predicted its own successor: *"The first weeks of running `watch.py` are the real test:
a row that reports CHANGED with no content difference gets dropped then, for the same reason
these four were."* The tool learned to tell the difference instead, so nothing had to be dropped.

## Re-tested against the `noise` verdict

| source | double-fetch | verdict now | prose as % of bytes |
|---|---|---|---|
| `openrouter.ai/docs/api-reference/limits` | different bytes | **noise** | 1.5% |
| `stevescargall.com/…graphify-memmachine…` | different bytes | **noise** | 37.3% |
| `the-decoder.com/…unlimited-ocr…` | different bytes | **noise** | 7.7% |
| `anthropic.com/engineering/managed-agents` | **identical** bytes | **same**, then noise on the live run | 8.2% |

Every one of them: bytes moved, **visible text byte-identical**. They were never unstable in the
part any note cites. The fourth is the sharper case — it came back byte-*stable* today, which is
exactly what its own drop note warned about (*"one double-fetch can PROVE instability and can
never prove stability"*). It was dropped on an intermittent property.

## One more added, for the opposite reason

`docs.z.ai/guides/overview/pricing` was never dropped; it was simply never watched, and it is a
**pricing page cited for its numbers**. A source whose entire purpose is that the figure changes
is the last one that should be unwatched. Stable across a double-fetch.

## Two rows this batch tried to add and could not

The two Hugging Face `LICENSE` files (`zai-org/GLM-5.3`, `moonshotai/Kimi-K3`) were already
watched from `baseline-2026-09-04`. **The duplicate-URL gate written earlier the same day caught
it in the same minute** — which is the first time one of these checks has stopped its own author
rather than a hypothetical future editor. The two copies made minutes earlier were removed before
being committed; nothing that had ever been provenance for a claim was touched.

## Coverage now

`watch.py --coverage` (a report, never a gate): **135 cited URLs — 85 watched, 40 immutable by
kind, 10 to check by hand.** All ten were checked and all ten are the MANIFEST's declared
volatile-by-design class: two gists, two social posts, a leaderboard, a YouTube playlist, a Chrome
Web Store listing, a GitHub issue thread, a licence pinned at a tag, and a news article.

The number that check first produced was **84**, and it was wrong. Naive URL equality does not
know that the watcher deliberately watches *the form that carries the claim*: a note cites
`github.com/o/r`, the row watches that repo's raw README. With the forms mapped it was 22, and two
of those 22 were still artifacts of forms the map did not yet know. That is why the coverage check
ships as a **report and not a gate** — a false hole is worse than no report.

Live run after this batch: **87 unchanged · 0 changed · 9 noise · 0 unreachable · 0 tampered ·
96 watched.** Nothing here was edited after fetching.
