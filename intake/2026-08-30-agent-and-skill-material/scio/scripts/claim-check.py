#!/usr/bin/env python3
"""Find the same countable thing given two different numbers in different documents.

Why this exists
---------------
A measured ablation on 2026-08-26 had an agent answer a question wrongly because two of
our own documents disagreed: `00-INDEX` said "seven rules", `LAYER-C-BUILD-PLAN` said
"nine". Both files existed. Every cross-reference was intact. A link checker — Obsidian's
graph, an orphan report — would have called the corpus clean.

Broken links are not our failure mode. Contradictory claims are, and nothing detects them.
This does, deterministically, with no model call.

Usage:  scripts/claim-check.py docs/            [--all]
Exit 1 if any contradiction is found, so it can gate a commit.
"""
import collections, pathlib, re, sys

WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split())}

# A counted claim: a number, then a noun phrase. The noun must be plural — that is what
# makes it a count rather than an ordinal, a version or a date.
PATTERN = re.compile(
    r"\b(\d{1,4}|" + "|".join(WORDS) + r")\s+"
    r"((?:[a-z][a-z-]{2,}\s+)?[a-z][a-z-]{2,}s)\b", re.I)

# Words that make the match a sentence fragment rather than a thing being counted.
FUNCTION_WORDS = {
    "is", "are", "was", "were", "has", "have", "and", "or", "but", "the", "of", "in", "to",
    "for", "with", "that", "this", "these", "those", "its", "as", "at", "on", "by", "from",
    "not", "no", "all", "any", "more", "most", "other", "same", "such", "than", "then",
    "does", "do", "did", "can", "will", "would", "says", "gives", "goes", "runs", "times",
    "years", "months", "days", "seconds", "lines", "files", "tokens", "chars", "characters",
    "words", "bytes", "nodes", "edges", "commits", "hours", "minutes",
    # Generic nouns that carry no subject, so a disagreement about them means nothing.
    "things", "ways", "ones", "others", "cases", "points", "reasons", "places", "parts",
    "items", "kinds", "sorts", "sections", "paragraphs", "sentences", "examples", "steps",
    "results", "answers", "questions", "options", "choices", "changes", "issues",
}


def value(token: str) -> int:
    t = token.lower()
    return WORDS[t] if t in WORDS else int(t)


def main() -> None:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    show_all = "--all" in sys.argv

    claims: dict[str, set] = collections.defaultdict(set)
    for path in sorted(root.rglob("*.md")):
        # Markdown wraps, so a claim straddles line breaks: the real contradiction this
        # script exists for had "nine good" ending one line and "rules" starting the next.
        # Scan the whole text with newlines flattened, and map each offset back to a line.
        raw = path.read_text(errors="ignore")
        line_starts = [i + 1 for i, ch in enumerate(raw) if ch == "\n"]
        flat = raw.replace("\n", " ")

        def line_of(offset: int, _starts=line_starts) -> int:
            lo, hi = 0, len(_starts)
            while lo < hi:
                mid = (lo + hi) // 2
                if _starts[mid] <= offset:
                    lo = mid + 1
                else:
                    hi = mid
            return lo + 1

        for match in PATTERN.finditer(flat):
            lineno = line_of(match.start())
            phrase = re.sub(r"\s+", " ", match.group(2).lower()).strip()
            words = phrase.split(" ")
            if words[0] in FUNCTION_WORDS or words[-1] in FUNCTION_WORDS:
                continue
            # Group by the HEAD NOUN, not the whole phrase: "seven rules" and
            # "nine good rules" are a claim about the same thing, and an adjective
            # in between is exactly how the real contradiction hid from a first pass.
            try:
                claims[words[-1]].add(
                    (value(match.group(1)), f"{path}:{lineno}", phrase))
            except ValueError:
                continue

    conflicts = {
        phrase: sites for phrase, sites in claims.items()
        if len({n for n, _, _ in sites}) > 1
    }

    def suspicion(noun: str) -> tuple:
        sites = conflicts[noun]
        bare = {n for n, _, seen in sites if seen == noun}
        # Strongest signal: the bare noun itself appears with two different numbers.
        # "seven rules" vs "nine good rules" is a contradiction; "engine tests" vs
        # "intake tests" is two different subjects that happen to share a head noun.
        return (0 if len(bare) > 1 else 1, -len(sites), noun)

    for phrase in sorted(conflicts, key=suspicion):
        sites = sorted(conflicts[phrase])
        files = {loc.rsplit(":", 1)[0] for _, loc, _ in sites}
        # Same file disagreeing with itself is usually prose, not a defect. Across files is the signal.
        if len(files) < 2 and not show_all:
            continue
        print(f"\n  {phrase}  →  {sorted({n for n, _, _ in sites})}")
        for number, location, seen_as in sites:
            print(f"      {number:>5}   {location}   \"{seen_as}\"")

    across = sum(
        1 for p, s in conflicts.items()
        if len({loc.rsplit(':', 1)[0] for _, loc, _ in s}) >= 2
    )
    print(f"\n{across} head nouns carry different numbers in different documents.", file=sys.stderr)
    print(
        "This is a CANDIDATE GENERATOR, not a detector. It cannot tell a contradiction from two\n"
        "correct counts of different things: 'Layer A has 67 tests' and 'Layer D has 74' both\n"
        "group under 'tests' and neither is wrong. Rows are ranked with the strong signal first —\n"
        "the bare noun itself carrying two numbers, which is the shape of the one real\n"
        "contradiction this was built from. Read the top rows; the tail is mostly noise.\n"
        "The fix for a genuine hit is never to pick a number: it is to attach the unit to both.",
        file=sys.stderr)
    sys.exit(1 if across else 0)


if __name__ == "__main__":
    main()
