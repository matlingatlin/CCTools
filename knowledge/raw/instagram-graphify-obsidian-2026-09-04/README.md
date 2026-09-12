---
title: Raw layer — an Instagram carousel on graphify → Obsidian, and the READMEs it was checked against
imported: 2026-09-04
by: the session that read it (single writer for this commit)
status: RAW — frame text and fetched pages, never edited; the notes cite these
---

# Instagram carousel "graphify + Obsidian", received 2026-09-04

A 20-slide Instagram carousel by **@divyannshisharma** ("Comment SEND I will send you the
link!"), forwarded as an Instagram DM ("Marcus Verdejo Har skickat en reel till dig") and
received here as **16 phone screenshots**. Slides present: **2, 3, 4, 8, 9, 10, 11, 12, 13,
14, 15, 16, 17, 18, 19, 20**. Slides **1, 5, 6, 7 were never received** — the note must not
assume what they said.

The screenshots themselves are **not stored**: they are session uploads, they are the
creator's, and the house precedent for video and image sources
(`../video-transcripts-2026-09-02/`) is to keep the text and say so. `slides.md` is the
on-screen text read off the frames — a read that cannot be repeated from this directory,
which is the honest limit of this raw. The md5 of each screenshot is recorded there so a
re-send is recognised as a duplicate.

## What was fetched to check it (primary source, 2026-09-04)

| File | URL | sha256 (16) | Bytes |
|---|---|---|---|
| `graphify-README@v8@2026-09-04.md` | `https://raw.githubusercontent.com/safishamsi/graphify/v8/README.md` | `0fb868544a527dff` | 62,662 |
| `graphify-README@main@2026-09-04.md` | `https://raw.githubusercontent.com/safishamsi/graphify/main/README.md` | `86382f46b8ebc269` | 7,106 |

`Graphify-Labs/graphify` and `safishamsi/graphify` returned byte-identical `main` READMEs
(7,106 bytes each) — the mirror is live. Branch READMEs v1–v8 all resolve (v9, v10 are 404);
`--obsidian` appears in v2–v8 and **not** in `main`/v1.

## The mix in the screenshots (read carefully, 2026-09-04)

The carousel intercuts **three different things**, and a careless read merges them:

1. **The generated vault** (`C:\Users\Chase\vaults\cc-docs`) — what graphify built from 145
   Claude Code doc files. Slides 8, 16, 18, 19, 20.
2. **The creator's own main vault** ("The Vault" / "AGENTIC OS" command centre, with
   `daily-notes/`, `content/`, `ops/`, token-burn and YouTube-subscriber panels). Slides 10
   and 17. **Slide 10's "1,252 nodes · 1,073 edges" belongs to THIS vault, not to the
   graphify build** — the graphify build's own numbers are slide 8's.
3. **The graphify GitHub README** in a browser. Slides 3 and 14.

The two vaults stay **separate** for the whole carousel: cc-docs is opened on its own
(slide 17, *Open folder as vault*), worked on there (slides 18–19), and only at the very end
moved into the main vault as one folder (slide 20).

## Second fetch, 2026-09-04b — reviewed and immaterial

`watch.py` reported the v8 README changed the same day. Re-read: the only diff is the project's
**Discord invite link** (`598Ad9zQZ` → `2DDrEgvZb4`), which no claim on any page of ours rests on.
The new bytes are kept as `graphify-README@v8@2026-09-04b.md` and the watch baseline advanced to
them, so the row stops reporting. This is the watcher's honest shape: it detects that bytes moved,
never that a claim did — the same run flagged four Claude Code doc pages whose changes WERE
material and this one, which was not.
