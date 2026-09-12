#!/usr/bin/env python3
"""Fetch a paper into a graphify corpus. Replaces `graphify add` where that cannot work.

Why this exists
---------------
`graphify add <arxiv-url>` prints "Saved arxiv:" and writes a 302-byte stub with an empty
title, no authors and no abstract. Two separate causes, and only one is graphify's fault:

1. `ingest.py` fetches with a bare `urlopen` and no proxy handling, then `security.py`
   rejects the resolved address. Behind an agent proxy that resolves to 127.0.0.1 the
   fetch can never succeed. Environmental.
2. `_fetch_arxiv` wraps the fetch in `except Exception:` and falls back to
   `title, abstract, paper_authors = arxiv_id, "", ""` — then the caller reports success.
   **That is a real defect** and it applies anywhere, not just here: any transient failure
   silently produces an empty file that looks like a saved paper.

This script fails loudly instead. It exits non-zero and writes nothing rather than writing
a stub, because a corpus that looks populated and is empty is worse than one that is short.

Usage
-----
    scripts/fetch-paper.py <url> [--out DIR] [--contributor NAME]
"""
import argparse, datetime, pathlib, re, subprocess, sys


def fetch(url: str) -> str:
    """Use curl: it honours HTTPS_PROXY, which graphify's urlopen path does not."""
    r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "30", url],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"fetch failed ({r.returncode}): {r.stderr.strip()}")
    return r.stdout


def grab(html: str, pattern: str) -> str:
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default="raw")
    ap.add_argument("--contributor", default="")
    args = ap.parse_args()

    html = fetch(args.url)
    title = re.sub(r"^\[[\d.]+\]\s*", "", grab(html, r"<title>(.*?)</title>"))
    abstract = grab(html, r'class="abstract[^"]*"[^>]*>(.*?)</blockquote>')
    abstract = re.sub(r"^Abstract:?\s*", "", abstract)
    authors = re.sub(r"^Authors:?\s*", "", grab(html, r'class="authors"[^>]*>(.*?)</div>'))

    # The check graphify does not make. An empty extraction is a failure, not a document.
    missing = [n for n, v in (("title", title), ("abstract", abstract)) if not v]
    if missing:
        sys.exit(f"refusing to write: no {', '.join(missing)} extracted from {args.url}. "
                 "The page structure may have changed — fix the patterns rather than "
                 "saving an empty file.")

    arxiv = re.search(r"(\d{4}\.\d{4,5})", args.url)
    stem = f"arxiv_{arxiv.group(1).replace('.', '_')}" if arxiv else re.sub(r"\W+", "_", args.url)[:60]
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{stem}.md"

    path.write_text(
        f'---\nsource_url: "{args.url}"\ntype: paper\ntitle: "{title}"\n'
        f'paper_authors: "{authors}"\n'
        f'captured_at: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n'
        f'contributor: "{args.contributor}"\n---\n\n'
        f"# {title}\n\n**Authors:** {authors}\n\n## Abstract\n\n{abstract}\n"
    )
    print(f"wrote {path} ({path.stat().st_size} bytes) — {title[:60]}")
    print("Then rebuild the graph: semantic extraction of prose needs a model, so run "
          "/graphify --update in the assistant rather than `graphify update`.")


if __name__ == "__main__":
    main()
