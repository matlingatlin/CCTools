#!/usr/bin/env python3
"""The skills roster, sorted, with the two failures that matter flagged.

The files are the database — one row per SKILL.md, frontmatter as columns. This reads
them rather than adding a second store to keep in sync with the first.

It answers three questions nothing else does:

  * **Where does each skill belong?** `layer` names which of Scio's seven it serves, or
    the build process. `phase` decides which repo it ships in: build-time runs in our
    sessions and stays here; runtime ships into a generated app.
  * **Are two skills the same skill?** `description` is the load-bearing field — it decides
    *when* a skill fires. Two skills whose descriptions overlap will both fire on the same
    request, or neither will fire reliably. Overlap is measured, not judged.
  * **Which are unmeasured?** All of them, today. `status: written` means nobody has shown
    it changes an outcome.

Custom frontmatter keys were verified against `claude plugin validate --strict` and produce
no warning.

Usage:  scripts/skills-index.py [--threshold 0.25]
Exit 1 if any pair exceeds the overlap threshold, so it can gate a commit.
"""
import itertools, pathlib, re, sys

STOP = set(
    "the a an and or of to in for on with when use used using this that is are be as it its "
    "you your they them what which how why not no if then than so do does done from at by "
    "into over under about after before also can may should must our we us one two".split())

THRESHOLD = 0.25
if "--threshold" in sys.argv:
    THRESHOLD = float(sys.argv[sys.argv.index("--threshold") + 1])


def frontmatter(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        f = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if f:
            key = f.group(1)
            out[key] = f.group(2).strip().strip('"')
        elif key:
            out[key] += " " + line.strip()
    return out


def main() -> None:
    root = pathlib.Path(".claude/skills")
    skills = {}
    for d in sorted(root.iterdir()):
        f = d / "SKILL.md"
        if f.is_file():
            skills[d.name] = frontmatter(f.read_text(errors="ignore"))

    print(f"{len(skills)} skills\n")
    by_layer: dict[str, list] = {}
    for name, fm in skills.items():
        by_layer.setdefault(fm.get("layer", "— UNPLACED —"), []).append((name, fm))

    for layer in sorted(by_layer, key=lambda s: (s.startswith("—"), s)):
        print(f"  {layer}")
        for name, fm in sorted(by_layer[layer]):
            phase = fm.get("phase", "?")
            status = fm.get("status", "?")
            repo = {"build-time": "scio", "runtime": "app repo", "both": "both"}.get(phase, "?")
            print(f"      {name:<24} {phase:<11} → {repo:<9} {status}")
        print()

    words = {
        n: {w for w in re.findall(r"[a-z][a-z-]{2,}", fm.get("description", "").lower())
            if w not in STOP}
        for n, fm in skills.items()
    }
    pairs = []
    for a, b in itertools.combinations(sorted(words), 2):
        if words[a] and words[b]:
            j = len(words[a] & words[b]) / len(words[a] | words[b])
            pairs.append((j, a, b))
    pairs.sort(reverse=True)

    print(f"  Description overlap — the field that decides when a skill fires")
    print(f"  (threshold {THRESHOLD}; two skills above it compete for the same request)\n")
    for j, a, b in pairs[:5]:
        flag = "  ← OVER" if j >= THRESHOLD else ""
        print(f"      {j:.2f}   {a}  ×  {b}{flag}")

    over = [p for p in pairs if p[0] >= THRESHOLD]
    unplaced = [n for n, fm in skills.items() if "layer" not in fm]
    unmeasured = [n for n, fm in skills.items() if fm.get("status") != "measured"]

    print(f"\n  {len(over)} pairs over threshold")
    if unplaced:
        print(f"  {len(unplaced)} unplaced: {', '.join(unplaced)}")
    print(f"  {len(unmeasured)} of {len(skills)} unmeasured — no evidence any of them changes an outcome")
    sys.exit(1 if over else 0)


if __name__ == "__main__":
    main()
