#!/usr/bin/env python3
"""Positive controls for the skill contract checker.

The checker was shipped without these. Its three over-strict rules were caught by
running it over Anthropic's corpus - a NEGATIVE corpus, which finds rules that fire
when they should not. It cannot find the opposite defect: a rule that stays green on
an artefact that really is broken. That is what this file is for.

One fixture skill the checker accepts cleanly, then one deliberate defect at a time,
asserting three things per case:

  1. the rule that owns the defect FAILS,
  2. it fails on the planted defect, not incidentally,
  3. no OTHER rule changes verdict unless the case declared it as collateral.

Mutations act on a throwaway copy of the fixture, or on the context the checker is
given (content_kind, verifiable, bill_of_materials) - some rules are only decidable
against the build package, and a rule that cannot run is not a rule that passes.

Coverage gate on the selftest itself: every rule the contract marks `check: code`
must be the subject of a case, or this exits 2. Two rules are exempt and say why in
CANNOT_FAIL - an exemption is a written argument, not a silent skip.

    python3 pipeline/validate/selftest_skill.py [-v]

Exit 0 = all controls behaved. 1 = a control failed. 2 = a rule has no control.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_contract as sc  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "skills" / "migration-review"

# Rules whose implementation returns INDETERMINATE unconditionally, so no artefact can
# make them FAIL. Listing one here is a claim about the CHECKER, and the selftest
# verifies it: if such a rule ever fails or passes, the exemption is stale.
CANNOT_FAIL: dict[str, str] = {}


# --- helpers -----------------------------------------------------------------

def read(d: Path, rel: str) -> str:
    return (d / rel).read_text(encoding="utf-8")


def write(d: Path, rel: str, text: str) -> None:
    (d / rel).parent.mkdir(parents=True, exist_ok=True)
    (d / rel).write_text(text, encoding="utf-8")


def sub(d: Path, rel: str, old: str, new: str) -> None:
    txt = read(d, rel)
    assert old in txt, f"fixture drifted: {old!r} not in {rel}"
    write(d, rel, txt.replace(old, new, 1))


def append(d: Path, rel: str, text: str) -> None:
    write(d, rel, read(d, rel) + text)


def fm_line(d: Path, old: str, new: str) -> None:
    sub(d, "SKILL.md", old, new)


def evals(d: Path, fn) -> None:
    data = json.loads(read(d, "evals/evals.json"))
    fn(data)
    write(d, "evals/evals.json", json.dumps(data, indent=2))


def pad_ref(d: Path, lines: int) -> None:
    filler = "\n".join(f"Row {i} of synthetic padding, distinct from the body." for i in range(lines))
    append(d, "references/lock-modes.md", "\n" + filler + "\n")


EMPTY_BODY_COLLATERAL = [
    "purpose.present", "when.present", "body.max-lines", "body.max-words",
    "body.files-exist", "body.critical-first", "ptr.every-file", "ptr.resolves",
    "ref.no-duplication", "whole.no-orphans",
]

ORPHAN_COLLATERAL = ["ptr.every-file", "whole.no-orphans", "ref.dated"]

DROP_REF_COLLATERAL = [
    "body.files-exist", "ptr.resolves", "ptr.every-file", "whole.no-orphans",
    "eval.files-resolve", "whole.bom", "ref.dated", "ref.no-duplication",
]


# --- cases -------------------------------------------------------------------
# (label, mutate(dir, ctx), rule that must FAIL, collateral allowed to change)

CASES = [
    # directory
    ("SKILL.md is lowercased", lambda d, c: (d / "SKILL.md").rename(d / "skill.md"),
     "dir.skillmd",
     ["fm.parses", "name.pattern", "name.matches-dir", "name.max", "name.reserved",
      "desc.present", "desc.max", "desc.no-angle-brackets", "desc.target",
      "fm.task-kind", "fm.script-needs-tools", "fm.portable-fields",
      "purpose.present", "when.present", "body.max-lines", "body.max-words",
      "body.files-exist", "body.critical-first", "ptr.every-file", "ptr.resolves",
      "ref.no-duplication", "eval.name-matches", "whole.no-orphans", "whole.bom",
      "ptr.one-level"]),
    ("directory name is not kebab-case", lambda d, c: c.__setitem__("_rename", "Migration_Review"),
     "dir.kebab", ["name.matches-dir"]),
    ("a README shipped inside the skill", lambda d, c: write(d, "README.md", "# notes\n"),
     "dir.no-readme", ["whole.bom"]),
    ("an unlisted bundled directory", lambda d, c: write(d, "templates/x.md", "x\n"),
     "dir.bundled-known", ["whole.bom", "ptr.one-level"]),

    # name
    ("name is not kebab-case", lambda d, c: fm_line(d, "name: migration-review", "name: Migration_Review"),
     "name.pattern", ["name.matches-dir", "eval.name-matches"]),
    ("name disagrees with the directory",
     lambda d, c: fm_line(d, "name: migration-review", "name: schema-review"),
     "name.matches-dir", ["eval.name-matches"]),
    ("a reserved word in the name",
     lambda d, c: fm_line(d, "name: migration-review", "name: claude-migration-review"),
     "name.reserved", ["name.matches-dir", "eval.name-matches"]),
    ("name over 64 characters",
     lambda d, c: fm_line(d, "name: migration-review", "name: " + "a" * 65),
     "name.max", ["name.matches-dir", "eval.name-matches"]),

    # description
    ("no description", lambda d, c: fm_line(d, "description: Use when", "x-description: Use when"),
     "desc.present", ["desc.max", "desc.target", "fm.portable-fields"]),
    ("description over 1024 characters",
     lambda d, c: sub(d, "SKILL.md", "SYNTHETIC FIXTURE, not a real skill.",
                      "SYNTHETIC FIXTURE, not a real skill. " + "padding word " * 90),
     "desc.max", ["desc.target"]),
    ("angle brackets in frontmatter",
     lambda d, c: sub(d, "SKILL.md", "SYNTHETIC FIXTURE, not a real skill.", "Emits <verdict> tags."),
     "desc.no-angle-brackets", []),
    ("description past the 500-character target",
     lambda d, c: sub(d, "SKILL.md", "SYNTHETIC FIXTURE, not a real skill.",
                      "SYNTHETIC FIXTURE, not a real skill. " + "padding word " * 40),
     "desc.target", []),

    # frontmatter policy
    ("frontmatter never closes",
     lambda d, c: sub(d, "SKILL.md", "allowed-tools: Read, Grep, Bash\n---\n",
                      "allowed-tools: Read, Grep, Bash\n"),
     "fm.parses",
     ["name.pattern", "name.matches-dir", "name.max", "name.reserved", "desc.present",
      "desc.max", "desc.no-angle-brackets", "desc.target", "fm.task-kind",
      "fm.script-needs-tools", "fm.portable-fields", "eval.name-matches"]),
    ("task-kind content without disable-model-invocation",
     lambda d, c: c.__setitem__("content_kind", "task"), "fm.task-kind", []),
    ("scripts bundled with no allowed-tools",
     lambda d, c: sub(d, "SKILL.md", "allowed-tools: Read, Grep, Bash\n", ""),
     "fm.script-needs-tools", []),
    ("a non-portable frontmatter field",
     lambda d, c: sub(d, "SKILL.md", "allowed-tools: Read, Grep, Bash\n",
                      "allowed-tools: Read, Grep, Bash\ndisable-model-invocation: true\n"),
     "fm.portable-fields", []),

    # body
    ("empty body, no purpose", lambda d, c: sub(d, "SKILL.md", "\n# Migration review", "\nZZZ_TRUNCATE"),
     "purpose.present", EMPTY_BODY_COLLATERAL),
    ("empty body, no when-to-use", lambda d, c: sub(d, "SKILL.md", "\n# Migration review", "\nZZZ_TRUNCATE"),
     "when.present", EMPTY_BODY_COLLATERAL),
    ("body over 500 lines", lambda d, c: append(d, "SKILL.md", "\nfiller\n" * 520),
     "body.max-lines", []),
    ("body over 5000 words", lambda d, c: append(d, "SKILL.md", "\n" + "filler " * 5200),
     "body.max-words", ["body.max-lines"]),
    ("the body points at a file that is not there",
     lambda d, c: append(d, "SKILL.md", "\nSee [the rollback list](references/rollbacks.md).\n"),
     "body.files-exist", ["ptr.resolves"]),
    ("Important comes after the steps",
     lambda d, c: [sub(d, "SKILL.md", "## Important — read before the steps", "## Notes"),
                   append(d, "SKILL.md", "\n## Important\n\nA verdict is per statement.\n")],
     "body.critical-first", []),

    # pointers
    ("a reference file nothing points at",
     lambda d, c: write(d, "references/orphan.md", "Fetched 2026-08-30. Unreferenced.\n"),
     "ptr.every-file", ["whole.no-orphans", "whole.bom"]),
    ("a pointer that does not resolve",
     lambda d, c: append(d, "SKILL.md", "\nSee [the rollback list](references/rollbacks.md).\n"),
     "ptr.resolves", ["body.files-exist"]),
    ("a bundled file points at another bundled file",
     lambda d, c: append(d, "references/lock-modes.md", "\nRun `scripts/split_statements.py` first.\n"),
     "ptr.one-level", []),

    # references
    ("a reference named notes.md",
     lambda d, c: [(d / "references" / "lock-modes.md").rename(d / "references" / "notes.md")],
     "ref.descriptive-name", DROP_REF_COLLATERAL),
    ("a long reference with no table of contents", lambda d, c: pad_ref(d, 150),
     "ref.toc-warn", []),
    ("a very long reference with no table of contents", lambda d, c: pad_ref(d, 350),
     "ref.toc-error", ["ref.toc-warn"]),
    ("a huge reference and no grep patterns in the body", lambda d, c: pad_ref(d, 2000),
     "ref.grep-patterns", ["ref.toc-warn", "ref.toc-error"]),
    ("the reference repeats the body",
     lambda d, c: append(d, "references/lock-modes.md",
                         "\nA verdict is per statement, never per file. One safe file is a file whose "
                         "every statement is safe; a single irreversible statement decides the whole verdict.\n"),
     "ref.no-duplication", []),
    ("a reference with no fetch date",
     lambda d, c: sub(d, "references/lock-modes.md", "Fetched 2026-08-30 from", "Fetched from"),
     "ref.dated", []),

    # assets
    ("a template with no fields to fill in",
     lambda d, c: write(d, "assets/verdict-template.md", "Write the verdict here.\n"),
     "asset.has-fields", []),

    # scripts
    ("an undocumented magic number",
     lambda d, c: append(d, "scripts/split_statements.py", "\nCHUNK = 4096\n"),
     "script.documented-constants", []),
    ("a script that reaches the network",
     lambda d, c: append(d, "scripts/split_statements.py", "\ndef fetch(u):\n    return requests.get(u)\n"),
     "script.no-network", []),
    ("a script that reads a credential",
     lambda d, c: append(d, "scripts/split_statements.py", "\nTOKEN = os.environ['API_TOKEN']\n"),
     "script.no-credentials", []),
    ("a script that installs something",
     lambda d, c: append(d, "scripts/split_statements.py", "\n# bootstrap\nRUN = 'pip install psycopg'\n"),
     "script.no-installs", []),

    # evals
    ("evals required and absent",
     lambda d, c: (d / "evals" / "evals.json").unlink(), "eval.exists",
     ["eval.schema", "eval.min", "eval.files-resolve", "eval.name-matches", "whole.bom"]),
    ("an eval id that is not an integer",
     lambda d, c: evals(d, lambda x: x["evals"][0].__setitem__("id", "one")), "eval.schema", []),
    ("a single eval", lambda d, c: evals(d, lambda x: x.__setitem__("evals", x["evals"][:1])),
     "eval.min", []),
    ("an eval fixture file that is not there",
     lambda d, c: evals(d, lambda x: x["evals"][1].__setitem__("files", ["references/gone.md"])),
     "eval.files-resolve", []),
    ("evals名 disagrees with the frontmatter name",
     lambda d, c: evals(d, lambda x: x.__setitem__("skill_name", "schema-review")),
     "eval.name-matches", []),

    # whole artifact
    ("a file that was never planned",
     lambda d, c: write(d, "references/extra.md", "Fetched 2026-08-30. Unplanned.\n"),
     "whole.bom", ["ptr.every-file", "whole.no-orphans"]),
    ("an orphan against the bill of materials",
     lambda d, c: write(d, "references/orphan.md", "Fetched 2026-08-30. Unreferenced.\n"),
     "whole.no-orphans", ["ptr.every-file", "whole.bom"]),
]

# Must change nothing: proves the diff can tell "caught it" from "always red".
NOOP = ("a comment added to the body",
        lambda d, c: append(d, "SKILL.md", "\n<!-- no-op -->\n"))


# --- engine ------------------------------------------------------------------

def base_ctx(d: Path) -> dict:
    bom = [{"file": str(p.relative_to(d))} for p in sorted(d.rglob("*"))
           if p.is_file() and p.name != "SKILL.md"]
    return {"content_kind": "reference", "verifiable": True, "bill_of_materials": bom}


def run(mutate, contract) -> dict[str, str]:
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / FIXTURE.name
        shutil.copytree(FIXTURE, d)
        ctx = base_ctx(d)
        if mutate is not None:
            mutate(d, ctx)
            # a mutation may ask for the directory itself to be renamed
            if "_rename" in ctx:
                new = d.parent / ctx.pop("_rename")
                d.rename(new)
                d = new
            # SKILL.md truncation marker: everything from it onward is dropped
            f = d / "SKILL.md"
            if f.is_file():
                txt = f.read_text(encoding="utf-8")
                if "ZZZ_TRUNCATE" in txt:
                    f.write_text(txt.split("ZZZ_TRUNCATE")[0], encoding="utf-8")
        return {r["id"]: r["verdict"] for r in sc.check_skill(d, contract, ctx)["rows"]}


def main() -> int:
    verbose = "-v" in sys.argv
    contract = sc.load_contract()

    # The other direction. coverage_gate catches a declared rule with no code;
    # this catches code with no declaration, which is never called at all
    # because the checker iterates the contract. Ungated on all three contracts
    # until 2026-09-02, when a rule added to a checker alone ran zero times and
    # every suite still reported each rule controlled.
    orphans = sc.orphan_gate(contract)
    if orphans:
        print("ABORT — implemented but undeclared, so never run: " + ", ".join(orphans),
              file=sys.stderr)
        return 2
    missing = sc.coverage_gate(contract)
    if missing:
        print("ABORT — the engine does not implement:", ", ".join(missing), file=sys.stderr)
        return 2

    code_rules = [r["id"] for r in sc.declared_code_rules(contract)]
    controlled = {c[2] for c in CASES} | set(CANNOT_FAIL)
    uncontrolled = [r for r in code_rules if r not in controlled]
    if uncontrolled:
        print("ABORT — rules with no positive control and no written exemption:", file=sys.stderr)
        for r in uncontrolled:
            print(f"  {r}", file=sys.stderr)
        return 2

    base = run(None, contract)
    bad = {k: v for k, v in base.items() if v == sc.FAIL}
    if bad:
        print(f"FAIL  the fixture itself is not clean: {bad}")
        return 1

    failures = 0

    for rid, why in CANNOT_FAIL.items():
        if base.get(rid) != sc.INDET:
            print(f"FAIL  [exemption] {rid} is listed as unable to fail ({why}) "
                  f"but the fixture scores {base.get(rid)} — the exemption is stale")
            failures += 1

    name, mutate = NOOP
    changed = {k for k, v in run(mutate, contract).items() if v != base[k]}
    if changed:
        print(f"FAIL  [no-op] {name}: changed {sorted(changed)}")
        failures += 1
    elif verbose:
        print(f"ok    [no-op] {name}")

    for label, mutate, expected, collateral in CASES:
        got = run(mutate, contract)
        if got.get(expected) != sc.FAIL:
            print(f"FAIL  {label}: expected {expected} to FAIL, got {got.get(expected)}")
            failures += 1
            continue
        allowed = {expected, *collateral}
        surprises = sorted(k for k, v in got.items() if v != base[k] and k not in allowed)
        if surprises:
            print(f"FAIL  {label}: {expected} caught it, but these also changed "
                  f"and were not declared: {surprises}")
            failures += 1
            continue
        if verbose:
            extra = f"  (+{len(collateral)} collateral)" if collateral else ""
            print(f"ok    {label} -> {expected}{extra}")

    total = len(CASES) + 1
    print(f"\n{total - failures}/{total} controls behaved · {len(code_rules)} code rules, "
          f"{len(CASES)} controlled, {len(CANNOT_FAIL)} exempt")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
