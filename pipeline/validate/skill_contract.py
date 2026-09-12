#!/usr/bin/env python3
"""Mechanical conformance check for a skill, against pipeline/contracts/skill.contract.json.

The contract file DECLARES the rules — id, text, authority, severity. This file
IMPLEMENTS them. Nothing here restates a rule's text or its authority; those live
in the contract and are read from it at run time. Change a rule there and this
engine picks it up without being rebuilt.

Three verdicts, and the third is the point:

    PASS            the rule was checked and held
    FAIL            the rule was checked and did not hold
    INDETERMINATE   the rule could NOT be checked here — a missing input, or a rule
                    that is not mechanically decidable at all

An INDETERMINATE is never counted as a pass. Most of this library's defects fail
silently — absence of a result is indistinguishable from a correct negative — so a
check that could not run has to say so in the same place a failure would appear.

Coverage is enforced in the other direction too: every rule the contract marks
`check: code` must have an implementation registered here, or the run aborts. A rule
added to the contract cannot sit there unenforced while the output looks clean.

Usage
    python3 pipeline/validate/skill_contract.py <skill-dir> [<skill-dir> ...]
    python3 pipeline/validate/skill_contract.py --all library/skills
    python3 pipeline/validate/skill_contract.py --all /mnt/skills --json

Exit 0 = no error-severity failures. Exit 1 = at least one. Warnings never fail a run.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTRACT = REPO / "pipeline" / "contracts" / "skill.contract.json"

PASS, FAIL, INDET = "PASS", "FAIL", "INDETERMINATE"

# ---------------------------------------------------------------------------
# The skill under test, parsed once.
# ---------------------------------------------------------------------------


class Skill:
    def __init__(self, path: Path):
        self.dir = path
        self.name_on_disk = path.name
        self.skillmd = path / "SKILL.md"
        self.raw = self.skillmd.read_text(encoding="utf-8", errors="replace") if self.skillmd.is_file() else None
        self.fm: dict | None = None
        self.fm_error: str | None = None
        self.body: str = ""
        if self.raw is not None:
            self._split()

    def _split(self) -> None:
        """Line-anchored frontmatter split.

        Line 1 must be exactly `---`; a later line must be exactly `---`. Splitting
        on the string `---` ignores line boundaries and reports green on an
        unterminated file — that is how three talents once shipped unloadable.
        """
        lines = self.raw.split("\n")
        if not lines or lines[0].rstrip("\r") != "---":
            self.fm_error = "line 1 is not exactly ---"
            self.body = self.raw
            return
        close = None
        for i in range(1, len(lines)):
            if lines[i].rstrip("\r") == "---":
                close = i
                break
        if close is None:
            self.fm_error = "no closing --- on its own line"
            self.body = self.raw
            return
        block = "\n".join(lines[1:close])
        self.body = "\n".join(lines[close + 1:])
        try:
            import yaml
            loaded = yaml.safe_load(block)
            if not isinstance(loaded, dict):
                self.fm_error = "frontmatter does not parse to a mapping"
            else:
                self.fm = loaded
        except Exception as exc:  # noqa: BLE001 - report, never crash the run
            self.fm_error = f"YAML error: {exc}"

    # -- convenience -------------------------------------------------------

    def field(self, key: str):
        return self.fm.get(key) if self.fm else None

    @property
    def body_lines(self) -> int:
        return len([l for l in self.body.split("\n")])

    @property
    def body_words(self) -> int:
        return len(self.body.split())

    def bundled_files(self) -> list[Path]:
        out = []
        for p in sorted(self.dir.rglob("*")):
            if p.is_file() and p.name != "SKILL.md":
                out.append(p)
        return out

    def rel(self, p: Path) -> str:
        return str(p.relative_to(self.dir))


# ---------------------------------------------------------------------------
# Rule implementations. Keyed by the rule id in the contract.
# Each returns (verdict, detail).
# ---------------------------------------------------------------------------

REG: dict[str, callable] = {}


def rule(rid):
    def deco(fn):
        REG[rid] = fn
        return fn
    return deco


# --- directory ---------------------------------------------------------------

@rule("dir.skillmd")
def _(s: Skill, ctx):
    names = [p.name for p in s.dir.iterdir() if p.is_file()]
    if "SKILL.md" in names:
        return PASS, "SKILL.md"
    near = [n for n in names if n.lower() == "skill.md"]
    return FAIL, f"no SKILL.md; found {near or names[:5]}"


@rule("dir.kebab")
def _(s: Skill, ctx):
    ok = re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s.name_on_disk)
    return (PASS, s.name_on_disk) if ok else (FAIL, f"directory name {s.name_on_disk!r}")


@rule("dir.no-readme")
def _(s: Skill, ctx):
    hits = [s.rel(p) for p in s.dir.rglob("README.md")]
    return (PASS, "none") if not hits else (FAIL, ", ".join(hits))


@rule("dir.bundled-known")
def _(s: Skill, ctx):
    known = {"references", "assets", "scripts", "evals"}
    dirs = {p.name for p in s.dir.iterdir() if p.is_dir()}
    unknown = sorted(dirs - known)
    return (PASS, "") if not unknown else (FAIL, f"unlisted bundled dirs: {', '.join(unknown)}")


# --- name --------------------------------------------------------------------

@rule("name.pattern")
def _(s: Skill, ctx):
    n = s.field("name")
    if n is None:
        return FAIL, "no name in frontmatter"
    ok = isinstance(n, str) and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n)
    return (PASS, n) if ok else (FAIL, f"name {n!r}")


@rule("name.matches-dir")
def _(s: Skill, ctx):
    n = s.field("name")
    if n is None:
        return INDET, "no name to compare"
    return (PASS, n) if n == s.name_on_disk else (FAIL, f"name {n!r} != directory {s.name_on_disk!r}")


@rule("name.max")
def _(s: Skill, ctx):
    n = s.field("name")
    if not isinstance(n, str):
        return INDET, "no name to measure"
    return (PASS, f"{len(n)}") if len(n) <= 64 else (FAIL, f"{len(n)} chars, cap 64")


@rule("name.reserved")
def _(s: Skill, ctx):
    n = s.field("name")
    if n is None:
        return INDET, "no name to check"
    low = str(n).lower()
    bad = [w for w in ("claude", "anthropic") if w in low]
    return (PASS, "") if not bad else (FAIL, f"reserved word(s) in name: {', '.join(bad)}")


# --- description -------------------------------------------------------------

@rule("desc.present")
def _(s: Skill, ctx):
    d = s.field("description")
    return (PASS, "") if isinstance(d, str) and d.strip() else (FAIL, "missing or empty")


@rule("desc.max")
def _(s: Skill, ctx):
    d = s.field("description")
    if not isinstance(d, str):
        return INDET, "no description to measure"
    n = len(d)
    return (PASS, f"{n} chars") if n <= 1024 else (FAIL, f"{n} chars, cap 1024 (over by {n - 1024})")


@rule("desc.no-angle-brackets")
def _(s: Skill, ctx):
    if s.fm is None:
        return INDET, "frontmatter did not parse"
    hits = [k for k, v in s.fm.items() if isinstance(v, str) and ("<" in v or ">" in v)]
    return (PASS, "") if not hits else (FAIL, f"angle brackets in field(s): {', '.join(hits)}")


@rule("desc.target")
def _(s: Skill, ctx):
    d = s.field("description")
    if not isinstance(d, str):
        return INDET, "no description to measure"
    n = len(d)
    return (PASS, f"{n}") if n <= 500 else (FAIL, f"{n} chars, target 500")


# --- frontmatter policy ------------------------------------------------------

@rule("fm.parses")
def _(s: Skill, ctx):
    if s.raw is None:
        return FAIL, "no SKILL.md"
    if s.fm_error:
        return FAIL, s.fm_error
    return PASS, f"{len(s.fm)} field(s)"


@rule("fm.task-kind")
def _(s: Skill, ctx):
    kind = ctx.get("content_kind")
    if kind is None:
        return INDET, "needs package.content_kind, not supplied"
    if kind != "task":
        return PASS, f"content_kind={kind}"
    return (PASS, "") if s.field("disable-model-invocation") is True else (FAIL, "task kind without disable-model-invocation: true")


@rule("fm.script-needs-tools")
def _(s: Skill, ctx):
    scripts = [p for p in (s.dir / "scripts").rglob("*") if p.is_file()] if (s.dir / "scripts").is_dir() else []
    if not scripts:
        return PASS, "no scripts/"
    at = s.field("allowed-tools")
    return (PASS, str(at)) if at else (FAIL, f"{len(scripts)} script(s) but no allowed-tools")


@rule("fm.portable-fields")
def _(s: Skill, ctx):
    if s.fm is None:
        return INDET, "frontmatter did not parse"
    portable = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    extra = sorted(set(s.fm) - portable)
    return (PASS, "") if not extra else (FAIL, f"non-portable field(s): {', '.join(extra)}")


# --- body --------------------------------------------------------------------

_PURPOSE_UNCHECKABLE = (
    "not mechanically decidable: 'text answering what the purpose is' cannot be "
    "distinguished from any other prose by code. Routed to the agent check."
)


@rule("purpose.present")
def _(s: Skill, ctx):
    if not s.body.strip():
        return FAIL, "body is empty"
    return INDET, _PURPOSE_UNCHECKABLE


@rule("when.present")
def _(s: Skill, ctx):
    if not s.body.strip():
        return FAIL, "body is empty"
    return INDET, _PURPOSE_UNCHECKABLE.replace("what the purpose is", "when to use it")


@rule("body.max-lines")
def _(s: Skill, ctx):
    n = s.body_lines
    return (PASS, f"{n} lines") if n <= 500 else (FAIL, f"{n} lines, cap 500 (over by {n - 500})")


@rule("body.max-words")
def _(s: Skill, ctx):
    n = s.body_words
    return (PASS, f"{n} words") if n <= 5000 else (FAIL, f"{n} words, cap 5000 (over by {n - 5000})")


_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_BUNDLED_RE = re.compile(r"`((?:references|assets|scripts|evals)/[A-Za-z0-9_./-]+)`")
_PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|sh|js|ts|json|txt|csv|sql))`")


def _referenced_paths(s: Skill) -> list[str]:
    """Paths presented as POINTERS to a bundled file.

    A markdown link, or a backticked path under a bundled directory. A bare filename
    in prose is NOT a pointer: our own generality rule requires a portable talent to
    use illustrative paths, and the first version of this function flagged
    settings.json, COSTS.md and src/auth.ts as broken references because it could not
    tell an example from a claim. Contract corrected 2026-08-30.
    """
    out = []
    for m in _LINK_RE.finditer(s.body):
        p = m.group(1)
        if p and not p.startswith(("http://", "https://", "#", "mailto:")):
            out.append(p)
    for m in _BUNDLED_RE.finditer(s.body):
        out.append(m.group(1))
    return out


@rule("body.files-exist")
def _(s: Skill, ctx):
    missing = []
    for p in _referenced_paths(s):
        cand = (s.dir / p)
        if cand.exists():
            continue
        # a path may legitimately be repo-relative rather than skill-relative
        if (REPO / p).exists():
            continue
        missing.append(p)
    return (PASS, "") if not missing else (FAIL, f"unresolved: {', '.join(sorted(set(missing))[:6])}")


@rule("body.no-invented-commands")
def _(s: Skill, ctx):
    """NOT mechanically decidable. Says so rather than guessing.

    A /token in prose is as often a path, an API endpoint, a JSON pointer or a type
    name as it is a slash-command. The heuristic that assumed otherwise produced 27
    false positives in 84 in-house skills and 14 in 38 of Anthropic's, flagging
    /evals, /context, /auth, /oauth2, /integer and /array. Contract corrected
    2026-08-30; this now routes to the agent check, where the sentence around the
    token settles it.
    """
    return INDET, "not mechanically decidable - a /token in prose is as often a path or an endpoint as a command; routed to the agent check"


@rule("body.critical-first")
def _(s: Skill, ctx):
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.*)$", s.body, re.M)]
    crit = [i for i, (_, h) in enumerate(heads) if re.search(r"\b(important|critical)\b", h, re.I)]
    if not crit:
        return PASS, "no Important/Critical heading"
    # Plurals matter: the commonest heading for a step section is "## Steps", and
    # \bstep\b does not match it. The singular-only pattern shipped and made the rule
    # a false negative on its own canonical case; a positive control found it
    # 2026-08-30. Widening flags 0 additional skills across our 84 and the 57 in
    # intake/, so it costs nothing and closes the hole.
    # A critical heading is not the step section it precedes: "Important - read before
    # the steps" names both, and counting it on both sides makes the rule fail on the
    # exact shape it is meant to reward.
    steps = [i for i, (_, h) in enumerate(heads)
             if i not in crit
             and re.search(r"\bsteps?\b|\bprocedures?\b|\bworkflows?\b|\binstructions\b", h, re.I)]
    if not steps:
        return PASS, "no step section to precede"
    return (PASS, "") if min(crit) < min(steps) else (FAIL, "Important/Critical heading appears after the steps")


# --- pointers ----------------------------------------------------------------

@rule("ptr.every-file")
def _(s: Skill, ctx):
    """references/ only.

    Anthropic's text is about files loaded INTO CONTEXT. The first version applied it
    to every bundled file and 35 of 38 shipped Anthropic skills violated it, several
    on LICENSE.txt alone. A rule that 92% of the authority's own artefacts break is
    the rule being wrong. Contract corrected 2026-08-30; severity is now warn.
    """
    d = s.dir / "references"
    if not d.is_dir():
        return PASS, "no references/"
    refs = set()
    for p in _referenced_paths(s):
        refs.add(p.lstrip("./"))
        refs.add(Path(p).name)
    orphans = [s.rel(f) for f in d.rglob("*")
               if f.is_file()
               and not re.match(r"licen[cs]e", f.stem, re.I)
               and s.rel(f) not in refs and f.name not in refs]
    return (PASS, "") if not orphans else (FAIL, f"no pointer in body: {', '.join(sorted(orphans)[:6])}")


@rule("ptr.resolves")
def _(s: Skill, ctx):
    return REG["body.files-exist"](s, ctx)


@rule("ptr.one-level")
def _(s: Skill, ctx):
    """A bundled file must not point at another bundled file.

    Anthropic: nested references get previewed with head -100 rather than read, so
    the information is SILENTLY incomplete.
    """
    offenders = []
    names = {f.name for f in s.bundled_files()}
    for f in s.bundled_files():
        if f.suffix.lower() not in {".md", ".markdown"}:
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in _PATH_RE.finditer(txt):
            tgt = m.group(1) or m.group(2)
            if tgt and Path(tgt).name in names and Path(tgt).name != f.name:
                offenders.append(f"{s.rel(f)} -> {tgt}")
    return (PASS, "") if not offenders else (FAIL, "; ".join(sorted(set(offenders))[:5]))


# --- references --------------------------------------------------------------

def _ref_files(s: Skill) -> list[Path]:
    d = s.dir / "references"
    return [p for p in d.rglob("*.md")] if d.is_dir() else []


@rule("ref.descriptive-name")
def _(s: Skill, ctx):
    bad_re = re.compile(r"^(doc|file|untitled|new|temp|tmp|notes?|misc|ref)\d*$", re.I)
    bad = [s.rel(p) for p in _ref_files(s) if bad_re.fullmatch(p.stem)]
    return (PASS, "") if not bad else (FAIL, ", ".join(bad))


def _has_toc(txt: str) -> bool:
    head = "\n".join(txt.split("\n")[:60])
    if re.search(r"^#{1,6}\s*(table of contents|contents|toc)\b", head, re.I | re.M):
        return True
    links = re.findall(r"^\s*[-*]\s*\[[^\]]+\]\(#", head, re.M)
    return len(links) >= 3


@rule("ref.toc-warn")
def _(s: Skill, ctx):
    bad = [s.rel(p) for p in _ref_files(s)
           if len(p.read_text(encoding="utf-8", errors="replace").split("\n")) > 100
           and not _has_toc(p.read_text(encoding="utf-8", errors="replace"))]
    return (PASS, "") if not bad else (FAIL, f">100 lines without a TOC: {', '.join(bad[:5])}")


@rule("ref.toc-error")
def _(s: Skill, ctx):
    bad = [s.rel(p) for p in _ref_files(s)
           if len(p.read_text(encoding="utf-8", errors="replace").split("\n")) > 300
           and not _has_toc(p.read_text(encoding="utf-8", errors="replace"))]
    return (PASS, "") if not bad else (FAIL, f">300 lines without a TOC: {', '.join(bad[:5])}")


@rule("ref.grep-patterns")
def _(s: Skill, ctx):
    big = [p for p in _ref_files(s) if len(p.read_text(encoding="utf-8", errors="replace").split()) > 10000]
    if not big:
        return PASS, "no reference file over 10k words"
    has = bool(re.search(r"\bgrep\b|\brg\b|search pattern", s.body, re.I))
    return (PASS, "") if has else (FAIL, f"{len(big)} file(s) over 10k words, no grep patterns in SKILL.md")


def _shingles(text: str, n: int = 12) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


@rule("ref.no-duplication")
def _(s: Skill, ctx):
    refs = _ref_files(s)
    if not refs:
        return PASS, "no references/"
    body = _shingles(s.body)
    if not body:
        return INDET, "body too short to compare"
    dup = []
    for p in refs:
        overlap = body & _shingles(p.read_text(encoding="utf-8", errors="replace"))
        if overlap:
            dup.append(f"{s.rel(p)} ({len(overlap)} passage(s))")
    return (PASS, "") if not dup else (FAIL, "; ".join(dup[:4]))


@rule("ref.dated")
def _(s: Skill, ctx):
    refs = _ref_files(s)
    if not refs:
        return PASS, "no references/"
    undated = []
    for p in refs:
        txt = p.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"\b(19|20)\d{2}-\d{2}-\d{2}\b", txt):
            undated.append(s.rel(p))
    return (PASS, "") if not undated else (FAIL, f"no fetch date: {', '.join(undated[:5])}")


# --- assets ------------------------------------------------------------------

@rule("asset.has-fields")
def _(s: Skill, ctx):
    d = s.dir / "assets"
    if not d.is_dir():
        return PASS, "no assets/"
    empty = []
    for p in d.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt", ".json", ".yaml", ".yml"}:
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        has_slot = bool(re.search(r"<[^>\n]{1,60}>|\{\{|\[[ x]\]|^\s*\|.*\|", txt, re.M))
        if not has_slot:
            empty.append(s.rel(p))
    return (PASS, "") if not empty else (FAIL, f"no fields or slots: {', '.join(empty[:5])}")


# --- scripts -----------------------------------------------------------------

def _script_files(s: Skill) -> list[Path]:
    d = s.dir / "scripts"
    return [p for p in d.rglob("*") if p.is_file()] if d.is_dir() else []


@rule("script.documented-constants")
def _(s: Skill, ctx):
    files = _script_files(s)
    if not files:
        return PASS, "no scripts/"
    hits = []
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            if "#" in line or "//" in line:
                continue
            for m in re.finditer(r"(?<![\w.])(\d{2,})(?![\w.])", line):
                if m.group(1) in {"10", "100", "1000", "200", "404", "500"}:
                    continue
                hits.append(f"{s.rel(p)}:{i}:{m.group(1)}")
    if hits:
        return FAIL, f"undocumented numeric constant(s) [heuristic]: {', '.join(hits[:5])}"
    return PASS, "[heuristic]"


def _script_scan(s: Skill, patterns: list[str], label: str):
    files = _script_files(s)
    if not files:
        return PASS, "no scripts/"
    rx = re.compile("|".join(patterns), re.I)
    hits = []
    for p in files:
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            if rx.search(line):
                hits.append(f"{s.rel(p)}:{i}")
    return (PASS, "") if not hits else (FAIL, f"{label}: {', '.join(hits[:5])}")


@rule("script.no-network")
def _(s: Skill, ctx):
    return _script_scan(s, [r"\bcurl\b", r"\bwget\b", r"\brequests\.", r"urllib", r"httpx", r"fetch\(", r"socket\."], "network call")


@rule("script.no-credentials")
def _(s: Skill, ctx):
    return _script_scan(s, [r"os\.environ", r"getenv", r"\$\{?[A-Z_]*(TOKEN|SECRET|KEY|PASSWORD)", r"\.netrc", r"credentials"], "credential read")


@rule("script.no-installs")
def _(s: Skill, ctx):
    return _script_scan(s, [r"pip\s+install", r"npm\s+i(nstall)?\b", r"npx\s", r"apt-get", r"brew\s+install", r"cargo\s+install"], "installer")


# --- evals -------------------------------------------------------------------

def _evals_path(s: Skill) -> Path:
    return s.dir / "evals" / "evals.json"


def _load_evals(s: Skill):
    p = _evals_path(s)
    if not p.is_file():
        return None, "evals/evals.json absent"
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except Exception as exc:  # noqa: BLE001
        return None, f"invalid JSON: {exc}"


@rule("eval.exists")
def _(s: Skill, ctx):
    verifiable = ctx.get("verifiable")
    present = _evals_path(s).is_file()
    if verifiable is None:
        return (PASS, "present") if present else (INDET, "absent, and package.verifiable not supplied — cannot say whether it is required")
    if not verifiable:
        return PASS, "not required (verifiable=false)"
    return (PASS, "present") if present else (FAIL, "required but absent")


@rule("eval.schema")
def _(s: Skill, ctx):
    data, err = _load_evals(s)
    if data is None:
        return (INDET, err) if "absent" in err else (FAIL, err)
    problems = []
    if not isinstance(data.get("skill_name"), str):
        problems.append("skill_name missing or not a string")
    evals = data.get("evals")
    if not isinstance(evals, list):
        problems.append("evals missing or not a list")
    else:
        seen = set()
        for i, e in enumerate(evals):
            if not isinstance(e, dict):
                problems.append(f"evals[{i}] not an object")
                continue
            if not isinstance(e.get("id"), int):
                problems.append(f"evals[{i}].id missing or not an integer")
            elif e["id"] in seen:
                problems.append(f"duplicate id {e['id']}")
            else:
                seen.add(e["id"])
            for k in ("prompt", "expected_output"):
                if not isinstance(e.get(k), str) or not e[k].strip():
                    problems.append(f"evals[{i}].{k} missing or empty")
            exp = e.get("expectations", e.get("assertions"))
            if exp is not None and not isinstance(exp, list):
                problems.append(f"evals[{i}].expectations not a list")
    return (PASS, "") if not problems else (FAIL, "; ".join(problems[:5]))


@rule("eval.min")
def _(s: Skill, ctx):
    data, err = _load_evals(s)
    if data is None:
        return (INDET, err) if "absent" in err else (FAIL, err)
    n = len(data.get("evals") or [])
    return (PASS, f"{n}") if n >= 2 else (FAIL, f"{n} eval(s), minimum 2")


@rule("eval.files-resolve")
def _(s: Skill, ctx):
    data, err = _load_evals(s)
    if data is None:
        return (INDET, err) if "absent" in err else (FAIL, err)
    missing = []
    for e in data.get("evals") or []:
        for f in (e.get("files") or []) if isinstance(e, dict) else []:
            if not (s.dir / f).exists():
                missing.append(f)
    return (PASS, "") if not missing else (FAIL, f"unresolved: {', '.join(sorted(set(missing))[:5])}")


@rule("eval.name-matches")
def _(s: Skill, ctx):
    data, err = _load_evals(s)
    if data is None:
        return (INDET, err) if "absent" in err else (FAIL, err)
    fn = s.field("name")
    en = data.get("skill_name")
    if fn is None:
        return INDET, "no frontmatter name to compare"
    return (PASS, "") if fn == en else (FAIL, f"evals skill_name {en!r} != frontmatter name {fn!r}")


# --- whole artifact ----------------------------------------------------------

@rule("whole.bom")
def _(s: Skill, ctx):
    bom = ctx.get("bill_of_materials")
    if bom is None:
        return INDET, "needs the build's bill of materials, not supplied"
    planned = {r.get("file") for r in bom if isinstance(r, dict)}
    actual = {s.rel(p) for p in s.bundled_files()}
    miss, extra = sorted(planned - actual), sorted(actual - planned)
    if not miss and not extra:
        return PASS, f"{len(planned)} planned, all present"
    return FAIL, f"planned but absent: {miss[:4]}; present but unplanned: {extra[:4]}"


@rule("whole.no-orphans")
def _(s: Skill, ctx):
    return REG["ptr.every-file"](s, ctx)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def declared_rules(contract: dict) -> list[dict]:
    """Every rule the contract declares, whatever kind of check it names."""
    out = []
    for r in contract.get("directory", {}).get("rules", []):
        out.append(dict(r, _field="directory"))
    for f in contract.get("fields", []):
        for r in f.get("rules", []):
            out.append(dict(r, _field=f["id"]))
    for r in contract.get("whole_artifact", {}).get("code_rules", []):
        out.append(dict(r, _field="whole"))
    return out


def declared_code_rules(contract: dict) -> list[dict]:
    out = []
    for r in contract.get("directory", {}).get("rules", []):
        out.append(dict(r, _field="directory"))
    for f in contract.get("fields", []):
        for r in f.get("rules", []):
            out.append(dict(r, _field=f["id"]))
    for r in contract.get("whole_artifact", {}).get("code_rules", []):
        out.append(dict(r, _field="whole"))
    return [r for r in out if r.get("check") == "code"]


def coverage_gate(contract: dict) -> list[str]:
    """Every code rule the contract declares must have an implementation.

    Without this, a rule added to the contract sits unenforced while the output
    still reads clean — the silent-absence shape this library keeps hitting.
    """
    return [r["id"] for r in declared_code_rules(contract) if r["id"] not in REG]


def orphan_gate(contract: dict) -> list[str]:
    """Implemented rules the contract does not declare - dead code that looks live.

    The checker iterates the CONTRACT's rule list, so a rule registered in REG
    but absent from the contract is never called. It imports, it registers, it
    reads as enforcement, and it runs zero times. coverage_gate() guards the
    other direction only, so this half was ungated on all three contracts until
    2026-09-02, when a rule added to the checker alone was silently never run
    and the selftest still reported every rule controlled.
    """
    # Compared against EVERY declared rule, not only the code ones. An
    # implementation legitimately exists for an agent-checked rule: it returns
    # INDETERMINATE to route the question onward. Comparing against code rules
    # alone flagged body.no-invented-commands, which was deliberately downgraded
    # from code to agent on 2026-08-30 because a /token in prose is as often a
    # path as a command - a design decision, reported as dead code. That was the
    # second false alarm on this gate's first outing; the first was a flat
    # contract["rules"] lookup against a nested contract, which flagged all 43.
    declared = {r["id"] for r in declared_rules(contract)}
    return sorted(rid for rid in REG if rid not in declared)


def check_skill(path: Path, contract: dict, ctx: dict) -> dict:
    s = Skill(path)
    rows = []
    for r in declared_code_rules(contract):
        fn = REG[r["id"]]
        try:
            verdict, detail = fn(s, ctx)
        except Exception as exc:  # noqa: BLE001 - a checker bug is not a skill defect
            verdict, detail = INDET, f"checker error: {type(exc).__name__}: {exc}"
        rows.append({
            "id": r["id"],
            "field": r["_field"],
            "severity": r.get("severity", "error"),
            "verdict": verdict,
            "detail": detail,
        })
    return {"skill": path.name, "path": str(path), "rows": rows}


def summarize(result: dict) -> dict:
    e = [r for r in result["rows"] if r["verdict"] == FAIL and r["severity"] == "error"]
    w = [r for r in result["rows"] if r["verdict"] == FAIL and r["severity"] == "warn"]
    i = [r for r in result["rows"] if r["verdict"] == INDET]
    p = [r for r in result["rows"] if r["verdict"] == PASS]
    return {"errors": len(e), "warns": len(w), "indeterminate": len(i), "passes": len(p)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("targets", nargs="*", help="skill directories")
    ap.add_argument("--all", metavar="ROOT", help="check every skill directory under ROOT")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="one line per skill")
    ap.add_argument("--context", metavar="FILE", help="JSON with content_kind / verifiable / bill_of_materials")
    args = ap.parse_args()

    contract = load_contract()
    missing = coverage_gate(contract)
    if missing:
        print("ABORT — contract declares code rules with no implementation:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        return 2

    ctx = json.loads(Path(args.context).read_text()) if args.context else {}

    targets: list[Path] = [Path(t) for t in args.targets]
    if args.all:
        root = Path(args.all)
        for p in sorted(root.rglob("SKILL.md")):
            targets.append(p.parent)
    targets = [t for t in targets if t.is_dir()]
    if not targets:
        print("no skill directories found", file=sys.stderr)
        return 2

    results = [check_skill(t, contract, ctx) for t in targets]

    if args.json:
        print(json.dumps({"contract_version": contract["contract_version"], "results": results}, indent=2))
    else:
        tot = {"errors": 0, "warns": 0, "indeterminate": 0, "passes": 0}
        for res in results:
            sm = summarize(res)
            for k in tot:
                tot[k] += sm[k]
            flag = "FAIL" if sm["errors"] else "ok  "
            print(f"{flag} {res['skill']:<38} err {sm['errors']:>2} · warn {sm['warns']:>2} · indet {sm['indeterminate']:>2} · pass {sm['passes']:>2}")
            if not args.quiet:
                for r in res["rows"]:
                    if r["verdict"] == PASS:
                        continue
                    mark = {FAIL: "E" if r["severity"] == "error" else "w", INDET: "?"}[r["verdict"]]
                    print(f"       [{mark}] {r['id']:<26} {r['detail']}")
        print(f"\n{len(results)} skill(s) · {tot['errors']} error(s) · {tot['warns']} warning(s) · "
              f"{tot['indeterminate']} indeterminate · {tot['passes']} pass")
        print("An indeterminate is NOT a pass — it is a check that could not run.")

    return 1 if any(summarize(r)["errors"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
