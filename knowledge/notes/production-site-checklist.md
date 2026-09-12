---
title: What a vibe-coded site is missing — a 19-item production checklist
sources:
  - note: "8-second short video, on-screen list 'Your vibe coded site is fake. It's missing 20 things that make it real.' Items 1-19 readable in the frame; item 20 is cut off. Creator unidentified (badge reads '...amesh'). Received and transcribed 2026-09-02."
tags: [web, checklist, launch, app-builder, product]
related: ["[[requirements-discovery]]", "[[agent-builder-prior-art]]", "[[claude-code-ecosystem-plugins]]", "[[third-party-landscape]]"]
raw: "none, and none is possible: the only source is an 8-second video transcribed by hand, creator unidentified, no URL. The lint's note-only INFO on this page is correct output, not debt - there is nothing retrievable to re-derive it from, and nothing to watch. What makes the page usable anyway is that all nineteen items are checkable against the site itself rather than against the source."
---

# Production checklist for a generated site

The list is not a claim; it is a checklist, and every item is a fact about the site that
a script can check. That is why it is kept: it is the shape of a `shape` eval — code can
grade all nineteen without a judge.

1. Custom 404 page
2. CTA above the fold
3. Meta title per page
4. Meta description per page
5. Open Graph image
6. Favicon set
7. robots.txt
8. sitemap.xml
9. Alt text on every image
10. Mobile breakpoints
11. Sticky mobile CTA
12. Loading states
13. Form error states
14. Thank-you page
15. Privacy policy page
16. Terms page
17. Cookie banner
18. Analytics installed
19. Real contact address
20. *(cut off in the frame — not invented here)*

## Why it is in this knowledge base

Two of the three repos this session works in are an AI app builder (`hello-world`, and its
rebuild `Scio`). "Generated apps ship without the things a real site has" is exactly the
gap Addy Osmani's `agent-skills` (see [[agent-builder-prior-art]]) and this list are both
pointing at, from opposite ends: one as engineering workflow, one as a launch checklist.
For the product, this list is a candidate **definition of done for a generated site** and
a candidate code-graded eval; for this repo, it is a ready-made `shape` fixture.

Items 15-17 are jurisdiction-dependent (GDPR/ePrivacy for a Swedish builder), which the
list does not say; that is the one place a script cannot decide alone.

## The security twin — "20 things to have Claude do before launching your app" (added 2026-09-02)

Source: a 25-second video (creator unidentified), items 1–18 on screen, 19–20 from the
spoken list; transcribed 2026-09-02. Again a checklist, not a claim; again nearly all
code-checkable.

1. Hide API keys · 2. Purge Git secrets · 3. Use public DB key · 4. Enable row-level
security · 5. Encrypt sensitive data · 6. Enforce server-side auth · 7. Lock record
access · 8. Block field tampering · 9. Secure session cookies · 10. Hash passwords ·
11. Rate-limit login · 12. Add bot protection · 13. Parameterize queries · 14. Validate
all input · 15. Escape user content · 16. Restrict file uploads · 17. Trim API responses ·
18. Add security headers · 19. Force HTTPS · 20. Scan dependencies.

Gradability: seventeen are code-gradable over the repository or a request; three are not
decidable without a definition — "encrypt sensitive data" (which data, at rest or in
transit: the intake's sensitivity level answers it), "lock record access" beyond RLS, and
"trim API responses" beyond a field allow-list. And the framing is a prompt list: an item
the model was *told* to do is not an item that was done — each of the seventeen is a gate
row that returns what it examined, or it is a wish.

Items 3, 4 and 6 are Supabase-shaped (anon key + RLS + server-side auth), which tells
you the stack the author assumes — the same one below. `code-security-review` covers
13–16 and 18–20 with sources; 1–2 are `agent-surface-security-audit`'s credential rule.

## The stack these lists assume — "run a startup for ~$21/month" (two videos, same list)

Two creators, same list, one silent (on-screen only), one with "we might not make it"
as its whole audio. REPEATED, and prices are the creators' as of 2026-09-02, not checked:

Claude $20/mo (coding) · Supabase (backend) · Vercel (deploy) · Namecheap $12/yr (domain)
· Stripe 2.9%/txn · GitHub · Resend (email) · Clerk (auth) · Cloudflare (DNS) · PostHog
(analytics) · Sentry (errors) · Upstash (Redis) · Pinecone (vector DB) — "all free tiers".

**Priced from the vendors' own pages, 2026-09-02** (a second session fetched ten of the
thirteen; Namecheap, GitHub and Cloudflare not fetched):

| Service | The "Free" tier, as the vendor states it | The clause the frame cannot show |
|---|---|---|
| Claude Pro | $20/mo monthly, $17/mo annual; includes Claude Code | a consumer subscription with usage limits — the developer's tool, not the product's runtime |
| Supabase Free | 2 active projects, 500 MB, 50,000 MAU | **"Free projects are paused after 1 week of inactivity"**; Pro $25/mo |
| Vercel Hobby | $0 | **"for personal, non-commercial use"** (FAQ); Pro $20/mo per developer seat |
| Clerk | 50,000 **MRU** (retained users, counted 24 h after signup), 3 seats, 7-day fixed session | Pro $25/mo ($20 annual) for MFA and branding removal; $0.02/MRU above 50k |
| Stripe | 2.9% **+ $0.30** per successful domestic card transaction; no monthly fee | the list omits the $0.30 |
| Resend | 100/day, 3,000/mo, 3 domains | Pro $20/mo for 50,000 |
| PostHog | 1M events, 5K replays, 1M flag requests per month; no card, "not a trial" | — |
| Sentry Developer | 5k errors/mo, **1 user** | Team $26/mo annual |
| Upstash Redis | 256 MB, 500K commands/mo | $0.20 per 100K commands after |
| Pinecone Starter | 2 GB, 2M write / 1M read units per month | Builder $20/mo flat |

So the total is right for a hobby project and wrong for the caption: on Vercel's own terms
a *startup* is on Pro, and the floor is ~$41/mo (Claude Pro + a Vercel seat + a domain)
before a second Sentry seat, a Supabase project that must not pause, or MFA on Clerk.
Two consequences for the app builder: the buyer's alternative cost to a hosted tier is
~$40/mo plus their own time, and **Vercel Hobby is a buy-out trap** — a transferred app on
the customer's free account is out of terms the day it earns money; the transfer
checklist should name it.

Why it is here: this is what a vibe-coded product *is* in 2026 — and it is nearly the
stack `hello-world` chose (Clerk, Vercel-style deploy, Postgres) without having written
it down as a market default. For Scio's open stack decision it is evidence of the
default, not a recommendation; every "Free" is a tier with a ceiling.

## The "slop" trio (added 2026-09-02)

A 41-second video ("how to not make slop with Claude Code") names three tools. Graded:

- **UI UX Pro Max** (`nextlevelbuilder/ui-ux-pro-max-skill`, MEASURED 2026-09-02): MIT,
  **124.1k stars**, 79 UI styles (50 active), 192 palettes, 74 font pairings, 22 stacks,
  192 "reasoning rules"; standard-library Python, **no network calls, no key**;
  `npm install -g ui-ux-pro-max-cli && uipro init --ai claude`. No benchmark of any kind.
  The single most-starred skill seen in this whole exercise, and a reuse-first read
  before any design talent is written.
- **CodeRabbit** — commercial AI code review (the frame shows it flagging a hard-coded
  key and a SQL-concatenation injection). Product, not a talent; `code-security-review`
  is our equivalent for the same two findings.
- **21st.dev** — commercial component/theme library. Product.

The video's diagnosis ("generic font, AI glow, dark theme, basic accent colour") is
opinion, but it is the same observation as the 19-item list above from the design side.
