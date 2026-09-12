#!/usr/bin/env python3
"""Triage an incoming skills repository before any of it is adopted.

Built from what twenty-six controlled ablations measured on 2026-08-26, not from taste.
Every check below corresponds to something that was observed to matter:

  * **A description with no when-clause never fires from context.** Our own vendored
    graphify said what it did and never when; it could only be started by an explicit
    command. Necessary condition, not sufficient.
  * **Three of four contract parts are usually missing.** Source, Method, Limits, Eval.
    Limits is the one that makes a skill trustworthy — 419 imperative rules were found in
    one mined corpus with not a single citation behind them.
  * **A runbook is the wrong shape for a decision.** graphify is a linear pipeline: Step 0,
    1, 2, executed in order, no choice. Most skills need the opposite — the list of what
    exists in a domain plus what disqualifies each. Copying a runbook's shape onto a
    decision produces a checklist, and a checklist is what the model already does.
  * **Overlap on the description means two skills compete for one request.** Measured
    threshold 0.25; our own 27 peak at 0.11.
  * **Length without disclosure is a load-time tax.** A skill over ~300 lines with no
    references/ directory loads whole on every invocation.

**What this is, precisely: a lint on form. It cannot judge substance, and it is trivially
gamed.** Demonstrated 2026-08-26 — this skill passes every check:

    ---
    name: be-excellent
    description: Use when writing code, whenever reviewing a change...
    ---
    ## 1 · Source     Widely known.
    ## 2 · Method     Write good code. Choose the right approach rather than the wrong one.
    ## 3 · Limits     Some limits apply.
    ## 4 · Eval       It works.

Four contract headings present, a when-clause present, under the line budget. Worthless.

Which checks mean anything:

  * **Line count and references/** — mechanical facts. Reliable.
  * **Description overlap** — a real relative measure. Reliable.
  * **The when-clause** — a string match. A description can pass and still be useless.
  * **Source / Method / Limits / Eval** — heading *presence* only. Never content.
  * **Shape** — counts step headings against alternative-weighing words. A heuristic.

Two of five measure something. The rest check that someone wrote a heading.

**And the worst consequence: an author who knows these criteria writes to them.** Used on
skills produced by an agent that has read this file, it degrades into a formatting
checklist — which is the same failure this project keeps finding elsewhere, a check that
looks like it measures quality and measures presence.

The only thing that cannot be passed by formatting is the three-arm ablation in
docs/evals/, because it measures behaviour against a control. Use this to reject the
obviously incomplete; use the ablation to decide anything.

Usage:  scripts/skill-intake.py <path-to-skills-dir> [--ours .claude/skills]
"""
import itertools, pathlib, re, sys

STOP = set("the a an and or of to in for on with when use used using this that is are be as "
           "it its you your they them what which how why not no if then than so do does from "
           "at by into over under about after before also can may should must our we us".split())

WHEN = re.compile(r"\buse (when|whenever|for|after|before)\b|\bwhenever\b|\bwhen (someone|you|a|the|two|asked)\b", re.I)
CONTRACT = {"source": re.compile(r"^#+\s*.*\bsources?\b", re.I | re.M),
            "method": re.compile(r"^#+\s*.*\b(method|procedure|how it works)\b", re.I | re.M),
            "limits": re.compile(r"^#+\s*.*\b(limits?|limitations)\b", re.I | re.M),
            "eval":   re.compile(r"^#+\s*.*\b(eval|evals|evaluation|test cases)\b", re.I | re.M)}
# a runbook numbers its steps and executes them; a decision procedure weighs alternatives
RUNBOOK = re.compile(r"^#+\s*(step\s*\d|\d+\.\s)", re.I | re.M)
DECISION = re.compile(r"disqualif|instead of|rather than|choose|when not to|do not use|\bunless\b", re.I)


def read(d: pathlib.Path) -> dict | None:
    f = d / "SKILL.md"
    if not f.is_file():
        return None
    t = f.read_text(errors="ignore")
    m = re.search(r"^description:\s*(.*?)(?=\n[a-z_]+:|\n---)", t, re.S | re.M)
    desc = re.sub(r"\s+", " ", m.group(1)).strip().strip('"') if m else ""
    body = t[t.index("---", 3) + 3:] if t.startswith("---") else t
    return {
        "name": d.name, "desc": desc, "text": t,
        "lines": t.count("\n") + 1,
        "refs": len(list((d / "references").glob("*.md"))) if (d / "references").is_dir() else 0,
        "evals": (d / "evals").is_dir() or (d / "evals.json").is_file(),
        "when": bool(WHEN.search(desc)),
        "contract": {k: bool(p.search(body)) for k, p in CONTRACT.items()},
        "steps": len(RUNBOOK.findall(body)),
        "decision": len(DECISION.findall(body)),
        "words": {w for w in re.findall(r"[a-z][a-z-]{2,}", desc.lower()) if w not in STOP},
    }


def main() -> None:
    src = pathlib.Path(sys.argv[1])
    ours_path = pathlib.Path(sys.argv[sys.argv.index("--ours") + 1]) if "--ours" in sys.argv else pathlib.Path(".claude/skills")
    incoming = [s for s in (read(d) for d in sorted(src.iterdir()) if d.is_dir()) if s]
    ours = [s for s in (read(d) for d in sorted(ours_path.iterdir()) if d.is_dir()) if s] if ours_path.is_dir() else []

    if not incoming:
        sys.exit(f"no SKILL.md found under {src}")

    print(f"{len(incoming)} incoming, {len(ours)} of ours\n")
    print(f"{'skill':<28}{'fires':>6}{'S':>3}{'M':>3}{'L':>3}{'E':>3}{'lines':>7}{'refs':>6}  shape")
    print("-" * 80)
    fails = []
    for s in incoming:
        c = s["contract"]
        shape = ("runbook" if s["steps"] >= 4 and s["decision"] < 5
                 else "decision" if s["decision"] >= 5 else "prose")
        flag = lambda b: "yes" if b else " NO"
        print(f"{s['name']:<28}{flag(s['when']):>6}"
              f"{'y' if c['source'] else '.':>3}{'y' if c['method'] else '.':>3}"
              f"{'y' if c['limits'] else '.':>3}{'y' if s['evals'] or c['eval'] else '.':>3}"
              f"{s['lines']:>7}{s['refs']:>6}  {shape}")
        why = []
        if not s["when"]:
            why.append("description has no when-clause — it cannot fire from context")
        if not c["limits"]:
            why.append("no Limits — nothing states what the source does not show")
        if not (s["evals"] or c["eval"]):
            why.append("no eval — nothing measurable")
        if shape == "runbook" and s["decision"] < 3:
            why.append("runbook shape with no alternatives weighed — likely a checklist")
        if s["lines"] > 300 and s["refs"] == 0:
            why.append(f"{s['lines']} lines, no references/ — loads whole every time")
        if why:
            fails.append((s["name"], why))

    print(f"\n{len(incoming) - len(fails)} of {len(incoming)} pass every mechanical check\n")
    for name, why in fails:
        print(f"  {name}")
        for w in why:
            print(f"      · {w}")

    if ours:
        print("\nOverlap against ours (0.25 = two skills competing for one request):\n")
        pairs = sorted(
            ((len(a["words"] & b["words"]) / len(a["words"] | b["words"]), a["name"], b["name"])
             for a in incoming for b in ours if a["words"] and b["words"]),
            reverse=True)
        for j, a, b in pairs[:6]:
            print(f"      {j:.2f}   {a}  ×  {b}{'   ← OVER' if j >= 0.25 else ''}")

    print("\n  PASSING THIS MEANS ALMOST NOTHING. Only the line count and the overlap measure\n"
          "  anything real; the contract columns check that a heading exists, never what is\n"
          "  under it. A skill reading 'Limits: some limits apply' passes all four. And an\n"
          "  author who knows these criteria writes to them, so on agent-produced skills this\n"
          "  degrades to a formatting checklist.\n\n"
          "  Use it to reject the obviously incomplete. Decide with the three-arm ablation in\n"
          "  docs/evals/, which measures behaviour against a control and cannot be passed by\n"
          "  formatting. Eighteen of our own twenty-seven changed an outcome; eight did not.")


if __name__ == "__main__":
    main()
