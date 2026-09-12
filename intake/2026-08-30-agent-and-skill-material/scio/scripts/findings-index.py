#!/usr/bin/env python3
"""Consolidate the mining findings into one index, and find the ones said twice.

Why this exists
---------------
The mined documents each carry a verdict table, and every one uses a different column
order — some name a layer, some a source file, some neither. Nobody can answer "what do
we have for Layer D?" without reading all of them, and a finding stated in two documents
is invisible: `ECC-AGENTS` and `ECC-SKILLS` both propose the plateau detector, arrived at
independently, and neither knows about the other.

This parses tolerantly and **reports what it could not parse** rather than pretending to
completeness. An imperfect index that admits its gaps beats a clean one that hides them.

Usage:  scripts/findings-index.py [docs/mined docs/ECC-MINED.md ...]
"""
import itertools, pathlib, re, sys

VERDICT = re.compile(r"\b(take|adopt|adapt|leave|skip|build)\b", re.I)
# NOT case-insensitive on the letter. With re.I the English article "a" matched as layer A
# and "e.g." as layer E, which inflated every per-layer count reported before 2026-08-26.
LAYER = re.compile(
    r"\b(?:[Ll]ayer\s+)?([A-G])\b(?:\s*[·,/]\s*([A-G]))?|(\b[Bb]uild[- ][Pp]rocess\b)")
STOP = set(
    "the a an and or of to in for on with is are be as it its that this from at by not no "
    "our we one two into over under when what which about above after again against all "
    "already also although always among another any anything around because been before "
    "being below between both but came cannot could does doing done down during each "
    "either else enough even ever every everything except first following gets give given "
    "goes going hard have having here高 how however itself just keep kept less like made "
    "make making many more most much must never next nothing now often once only other "
    "others otherwise ours out over own part rather really same seen several should since "
    "some something still such take taken than that their them then there these they thing "
    "things those three through thus together too under until upon used using very want "
    "was were what whatever when where whether which while whole will with within without "
    "would alongside approval already anything".split())


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main() -> None:
    targets = sys.argv[1:] or ["docs/mined", "docs/ECC-MINED.md"]
    paths: list[pathlib.Path] = []
    for t in targets:
        p = pathlib.Path(t)
        paths.extend(sorted(p.rglob("*.md")) if p.is_dir() else [p])

    findings, unparsed = [], []
    for path in paths:
        if not path.is_file():
            continue
        for lineno, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if not line.startswith("|") or set(line) <= set("|-: "):
                continue
            cols = cells(line)
            if len(cols) < 3 or not any(VERDICT.search(c) for c in cols):
                continue
            # the verdict is the shortest cell containing a verdict word
            v = min((c for c in cols if VERDICT.search(c)), key=len)
            # the item is the longest cell that is not the verdict
            item = max((c for c in cols if c is not v), key=len, default="")
            if len(item) < 15:
                unparsed.append(f"{path.name}:{lineno}")
                continue
            m = LAYER.search(" ".join(c for c in cols if c is not item))
            layer = ("build-process" if m and m.group(3)
                     else "/".join(x.upper() for x in (m.group(1), m.group(2)) if x) if m
                     else "— none —")
            findings.append((layer, VERDICT.search(v).group(1).lower(),
                             re.sub(r"[*`]", "", item)[:110], f"{path.name}:{lineno}"))

    print(f"{len(findings)} findings across {len(paths)} documents\n")
    by_layer: dict[str, list] = {}
    for layer, verdict, item, src in findings:
        by_layer.setdefault(layer, []).append((verdict, item, src))

    for layer in sorted(by_layer, key=lambda s: (s.startswith("—"), s)):
        rows = by_layer[layer]
        takes = sum(1 for v, _, _ in rows if v in ("take", "adopt", "adapt", "build"))
        print(f"  {layer}  —  {len(rows)} findings, {takes} to take")
        for verdict, item, src in sorted(rows)[:4]:
            print(f"      {verdict:<6} {item[:78]}")
            print(f"             {src}")
        if len(rows) > 4:
            print(f"      … {len(rows)-4} more")
        print()

    # Said twice, in different documents. Word overlap is the wrong signal: the two
    # statements of the plateau detector share only "plateau" and "stop", which scores
    # 0.2 and hides under any useful threshold. What identifies a repeated finding is a
    # RARE term appearing in findings from two different documents.
    import collections
    term_docs: dict[str, set] = collections.defaultdict(set)
    term_rows: dict[str, list] = collections.defaultdict(list)
    for idx, (_, _, item, src) in enumerate(findings):
        doc = src.split(":")[0]
        # length 7+: a technical noun naming a mechanism, not a connective
        for w in {w for w in re.findall(r"[a-z][a-z-]{6,}", item.lower()) if w not in STOP}:
            term_docs[w].add(doc)
            term_rows[w].append(idx)

    print("  Stated twice — a distinctive term appearing in two documents:\n")
    seen_pairs, dupes = set(), 0
    # rarest first: a term in exactly two findings is a stronger signal than one in four
    for term in sorted(term_docs, key=lambda t: (len(term_rows[t]), -len(t))):
        # rare enough to be distinctive, spanning more than one document
        if not (2 <= len(term_rows[term]) <= 4 and len(term_docs[term]) >= 2):
            continue
        rows = term_rows[term]
        key = tuple(sorted(rows))
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        dupes += 1
        if dupes > 10:
            print("      … truncated; this is a candidate generator, not a detector")
            break
        print(f"      \"{term}\"")
        for idx in rows:
            print(f"          {findings[idx][3]:<34} {findings[idx][2][:64]}")
        print()
    if not dupes:
        print("      none found")

    print(f"\n  {dupes} cross-document duplicates", file=sys.stderr)
    print(f"  {len(unparsed)} table rows had a verdict but no readable item — not counted:",
          file=sys.stderr)
    print(f"      {', '.join(unparsed[:8])}{' …' if len(unparsed) > 8 else ''}", file=sys.stderr)
    print("  Column order differs per document, so this parse is tolerant and incomplete\n"
          "  by design. Treat counts as a floor, never a total.", file=sys.stderr)


if __name__ == "__main__":
    main()
