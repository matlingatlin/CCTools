# Ownership re-fetch, 2026-09-08

One file, fetched to settle a question `kb.py owners` had left open as a candidate since
2026-09-04: goose's README names `aaif-goose/goose` in every self-link while this base cited
`github.com/block/goose`.

- `raw.githubusercontent.com_aaif-goose_goose_HEAD_README.md.md` — 3,449 B, sha256
  `0f1df85a…`, **byte-identical to the `block/goose` baseline taken four days earlier**, which
  is what a GitHub repository transfer looks like from the outside: both paths serve the same
  bytes and neither 404s.

**What settled it was the KIND of self-link, not the count.** The four hits are a CI workflow
badge, a `releases/download/stable` install URL and two `blob/main` document links — all of
which 404 at a wrong address, so a README carrying them is maintained at that address.
Graphify's single hit, by contrast, is a `git clone https://github.com/safishamsi/graphify.git`
line the rename left behind, plus two personal accounts (`/sponsors/`, gumroad) that are
correctly personal. Same check, same shape, opposite verdicts. `kb.py owners` now reports the
live count and says which of the two it is.

## Ornith-1.5 — four files, same day, different question

The Hugging Face model card that returned **401** to the fetcher on 2026-09-02 answers at its
`/raw/main/` path. Four files kept, all watched:

| Stored | Bytes | Settles |
|---|---|---|
| `huggingface.co_ornith-ai_Ornith-1.5-9B_raw_main_README.md` | 26,794 | `license: mit` in the card's own frontmatter; "Ornith Team"; built on Qwen3.5 and Gemma4 |
| `huggingface.co_ornith-ai_Ornith-1.5-9B_raw_main_config.json` | 2,910 | 32 layers, dense, hybrid attention (full every 4th), 256K context, vision + video tokens |
| `huggingface.co_ornith-ai_Ornith-1.5-35B-A3B_raw_main_config.json` | 3,295 | 40 layers, 256 experts, 8 routed + 1 shared → ~34B total, ~3B active |
| `huggingface.co_ornith-ai_Ornith-1.5-397B_raw_main_config.json` | 3,756 | 60 layers, 512 experts, 10 routed → ~394B |

The refuted claim is the one worth naming: two secondary write-ups placed the weights under
`deepreinforce-ai`. The HF API returns **zero** models for that org and 26 under `ornith-ai`,
and the model card does not contain the string. Both secondaries were wrong about the same
thing — which is the failure mode REPEATED exists to flag rather than to excuse.

Nothing here was edited after fetching; every file is stored as received.
