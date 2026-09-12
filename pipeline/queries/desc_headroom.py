#!/usr/bin/env python3
"""desc_headroom.py — which descriptions are too close to the host's truncation wall?

The wall is DESCRIPTION_LISTING_TRUNCATION in pipeline/CONSTANTS.md, and it is SILENT: the tail
is dropped, and this library's house style puts the NOT-clauses at the tail. So a description
near the wall loses the next disambiguator by the act of adding it.

The target is not "short". It is headroom for one more NOT-clause, sized from the clauses this
library actually writes. See pipeline/decisions/2026-09-08-description-headroom.md, which fixed
the number before any candidate was read.

    python3 pipeline/queries/desc_headroom.py            # the report
    python3 pipeline/queries/desc_headroom.py --check A B # constraint check between two files
"""
import re, sys, pathlib, statistics

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
NOT_CLAUSE = re.compile(r"(?:^|[.;—-]\s*)((?:NOT\b|Not for\b|never\b|Distinct from\b|distinct from\b)[^.;]*[.;]?)")
STOP = set("a an the and or of to in on for with by as is are be it its this that use when "
           "you your not no from at into over under about than then so such each any all "
           "one two both per via vs".split())


def constant(name, default):
    """Read a number from CONSTANTS.md rather than repeating it here. A limit copied into a
    second file is a limit that will disagree with itself."""
    m = re.search(rf"{name}\D{{0,40}}?(\d[\d,]*)", (ROOT / "pipeline" / "CONSTANTS.md").read_text())
    return int(m.group(1).replace(",", "")) if m else default


def descriptions():
    out = {}
    # The neutral, inert paths. Nothing in this repository sits under .claude/ - that path is
    # the activation - so the gate reads the library where it actually lives. A base left
    # pointing at .claude/ would report 0 descriptions and PASS, which is the shape of a gate
    # that has stopped gating: the amnesty list below names five units, and an empty read makes
    # every one of them invisible instead of loud.
    # Two bases, not one, and the separation is load-bearing rather than cosmetic. Merging
    # library/skills-candidates/ in here reads 98 descriptions instead of 92, because the
    # unadopted candidate carries five eval FIXTURES that are each a valid SKILL.md; one of
    # them (artifact-E, 1446 chars) then reports as a talent over the target. Measured
    # 2026-09-12 while moving the library off .claude/.
    for base in ("library/skills", "library/agents"):
        for p in (ROOT / base).rglob("*.md"):
            m = re.match(r"^---\n(.*?)\n---\n", p.read_text(), re.S)
            if not m:
                continue
            d = re.search(r"^description:\s*(.*?)(?=\n[a-z_-]+:|\Z)", m.group(1), re.S | re.M)
            if not d:
                continue
            name = p.parent.name if p.name == "SKILL.md" else p.stem
            out[name] = (p, " ".join(d.group(1).split()).strip().strip("\"'"))
    return out


def tokens(text):
    """Content words. What a cut must not remove."""
    return {w for w in re.findall(r"[a-z0-9][a-z0-9_.-]*", text.lower()) if w not in STOP and len(w) > 2}


def clause_stats(descs):
    lens = sorted(len(m.group(1).strip()) for _, d in descs.values() for m in NOT_CLAUSE.finditer(d))
    return lens


def check(before, after):
    """The three preregistered constraints, as a verdict. Returns (ok, findings)."""
    findings = []
    lost = tokens(before) - tokens(after)
    if lost:
        findings.append(f"trigger tokens lost ({len(lost)}): {', '.join(sorted(lost))}")
    nb, na = len(NOT_CLAUSE.findall(before)), len(NOT_CLAUSE.findall(after))
    if na < nb:
        findings.append(f"NOT-clauses lost: {nb} -> {na}")
    if before.lstrip().lower().startswith("use when") and not after.lstrip().lower().startswith("use when"):
        findings.append("the 'Use when' opening was dropped")
    return (not findings), findings


# Descriptions ALREADY above the headroom target when the gate was introduced (2026-09-08), with
# the length each had at that moment. This is not an amnesty and it is deliberately not a blanket
# one: the gate still fails if any of these GROWS by a single character. That is the exact failure
# the target exists to prevent -- a NOT-clause added to a near-wall description and silently
# truncated at the tail -- so the five below are covered against it from today, trimmed or not.
#
# Trimming them was measured as possible: the floor of a rewrite keeping every distinct content
# word exactly once is 867-1011 characters, leaving 429-488 of slack against the 66-216 needed. It
# was NOT done in the same pass, because a description edit changes ROUTING and this library's own
# rule is that such a change is proven against a baseline (`skill-measure`), which needs a run and
# not an opinion. Shrinking one below the target and deleting its line here is the finished job.
GRANDFATHERED = {
    "data-contract-assertions": 1446,
    "llm-eval-harness": 1445,
    "oracle-weakening-audit": 1442,
    "expand-contract-migration": 1374,
    "stage-ablation-attribution": 1296,
}


# The Agent Skills spec's own maximum for the description field, verbatim: "Must be 1-1024
# characters". Sourced 2026-09-12 from the copy held since 2026-09-04. This is a DIFFERENT constraint
# from the host's 1,536-character truncation wall, and this gate's target answers the wall, not this.
# Reported and never gated on: the target is preregistered and frozen, and moving a threshold after
# seeing a result is the one thing preregistration exists to prevent.
SPEC_MAX_CHARS = 1024


STOPWORDS = frozenset(
    "a an the of to in on for and or is are be as at by with from this that it its when about "
    "into over if then than but each any all every some".split())


def lossless_floor(text, stopwords=STOPWORDS):
    """Shortest this description could be with EVERY content word kept - the zero-loss bound.

    Added 2026-09-12 to answer a question the character count alone cannot: is a unit over the
    spec because it is padded, or because it is dense? Strips connective words and rejoins with
    single spaces. If the floor is still above the spec's maximum, the unit CANNOT comply without
    deleting a word the router matches on, and trimming it is a capability cut rather than a
    formatting fix.

    Approximate on purpose: real prose needs some of these words back, so the floor is a bound and
    not a target. It is used to separate "could be trimmed" from "cannot be", never to propose a
    rewrite.
    """
    kept = [w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'/_.<>-]*", text)
            if w.lower() not in stopwords]
    return len(" ".join(kept))


def over_spec(lengths, spec_max=SPEC_MAX_CHARS):
    """Units longer than the SPEC's maximum, longest first. Reporting only - never fails a build."""
    return sorted(((n, ln) for n, ln in lengths.items() if ln > spec_max),
                  key=lambda kv: (-kv[1], kv[0]))


def gate(lengths, wall, target, allowed):
    """The three ways this can fail, as (findings, improved). Pure, so it can be tested.

    Kept separate from the reporting for the reason this repo keeps learning the hard way: the
    last predicate that lived inside its own caller passed while blind.
    """
    findings, improved = [], []
    for name, ln in sorted(lengths.items()):
        if ln >= wall:
            findings.append(f"{name}: {ln} >= the truncation wall {wall} — the tail is ALREADY "
                            f"being dropped in the listing, and nothing reports it")
        elif name not in allowed:
            if ln > target:
                findings.append(f"{name}: {ln} > target {target} and not declared — a NOT-clause "
                                f"added here would be truncated. Trim it, or add one line to "
                                f"GRANDFATHERED with its length")
        elif ln > allowed[name]:
            findings.append(f"{name}: {ln} > its recorded {allowed[name]}. It is above target and "
                            f"just GREW; the growth is what the target forbids")
        elif ln <= target:
            improved.append(f"{name}: {ln} <= target {target} — it no longer needs its "
                            f"GRANDFATHERED line; delete it")
    for name in sorted(set(allowed) - set(lengths)):
        improved.append(f"{name}: declared in GRANDFATHERED but no longer present; delete the line")
    return findings, improved


def _floor_fixtures():
    """(label, ok) pairs for lossless_floor, kept beside the other fixtures."""
    dense = "vendor feed ETL Kafka Parquet warehouse ingest freshness drift quarantine"
    padded = "Use this when you are in the middle of the thing that is on the top of the list"
    return [
        # a string of nothing but content words cannot shrink
        ("dense is its own floor", lossless_floor(dense) == len(dense)),
        # one made of connectives collapses hard
        ("padded shrinks", lossless_floor(padded) < len(padded) / 2),
        # the floor never exceeds the text
        ("floor <= length", lossless_floor(padded) <= len(padded)
                            and lossless_floor(dense) <= len(dense)),
        # A compound token must not be SPLIT - splitting would inflate the floor with spaces and
        # could push a compliant unit over the line. `CSV/JSON` and `top-k` are one word each.
        # Written first as an equality against the input and it FAILED, which was the fixture
        # being wrong rather than the code: a leading `<` is not a word character, so the angle
        # brackets of `<framework>` are dropped. That keeps the result a valid lower BOUND, which
        # is all this is for, so the assertion is on the property instead of the byte count.
        # A separator BETWEEN two words is length-neutral when split - one character becomes one
        # space - so a fixture built on `CSV/JSON` cannot tell the two implementations apart, and
        # the first one written could not: the mutation that splits compound tokens survived it.
        # The case that separates them is punctuation at a token's EDGE, which splitting drops.
        ("compound tokens stay whole",
         lossless_floor("rerank top-k.") == len("rerank top-k.")
         and lossless_floor("CSV/JSON top-k") == len("CSV/JSON top-k")),
        ("empty", lossless_floor("") == 0),
    ]


def selftest(wall=1536, target=1230):
    """Offline. The gate decides whether CI fails, so it is tested like one."""
    allowed = {"legacy": 1400, "walled": 1536}
    cases = [
        ("a short one passes",            {"x": 500},      0),
        ("over target, undeclared, fails", {"x": 1300},    1),
        ("over target, declared, passes",  {"legacy": 1400}, 0),
        ("declared but GROWN, fails",      {"legacy": 1401}, 1),
        ("declared and shrunk, passes",    {"legacy": 1399}, 0),
        ("at the wall, declared, STILL fails", {"legacy": 1536}, 1),
        ("at the wall, declared AT the wall, still fails", {"walled": 1536}, 1),
        ("exactly on target passes",       {"x": 1230},    0),
        ("one over target fails",          {"x": 1231},    1),
    ]
    fails = []
    for label, lengths, want in cases:
        got = len(gate(lengths, wall, target, allowed)[0])
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got} finding(s), expected {want}")
        if not ok:
            fails.append(label)
    # The last two use their OWN allowlist rather than the shared one above: a fixture that
    # depends on the size of a dict another fixture edits breaks the moment a case is added,
    # which is exactly what happened when the wall case was written.
    solo = {"legacy": 1400}
    # A declared entry that fell to target is not a failure -- it is a line to delete.
    f, imp = gate({"legacy": 1000}, wall, target, solo)
    ok = not f and len(imp) == 1
    print(f"  {'ok  ' if ok else 'FAIL'} declared entry now under target: reported as improvement, not failure")
    if not ok:
        fails.append("improvement")
    # A stale GRANDFATHERED line for a deleted talent is also an improvement, never a failure.
    f, imp = gate({}, wall, target, solo)
    ok = not f and len(imp) == 1
    print(f"  {'ok  ' if ok else 'FAIL'} declared entry for a talent that is gone: improvement, not failure")
    if not ok:
        fails.append("stale-line")
    # over_spec reports a SECOND constraint this gate does not enforce. Tested because a
    # reporting-only path is exactly where a silent break goes unnoticed.
    spec_cases = _floor_fixtures() + [
        ("over_spec finds what the gate's target hides",
         over_spec({"a": 1037, "b": 1024, "c": 900}) == [("a", 1037)]),
        ("the spec maximum is inclusive - exactly 1024 is fine", over_spec({"x": 1024}) == []),
        ("over_spec sorts longest first",
         [n for n, _ in over_spec({"s": 1100, "l": 1400, "m": 1200})] == ["l", "m", "s"]),
        ("over_spec never reports a short description", over_spec({"z": 10}) == []),
        ("a unit over the SPEC but under the gate's TARGET is invisible to the gate and visible here",
         gate({"q": 1100}, wall, target, {})[0] == [] and over_spec({"q": 1100}) == [("q", 1100)]),
    ]
    for label, ok in spec_cases:
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            fails.append(label)
    print(f"\n{'PASS' if not fails else 'FAIL: ' + ', '.join(fails)} — desc_headroom gate, "
          f"{11 + len(spec_cases)} fixtures")
    return 1 if fails else 0


def main():
    descs = descriptions()
    wall = constant("DESCRIPTION_LISTING_TRUNCATION", 1536)
    target = constant("DESCRIPTION_HEADROOM_TARGET", 1230)
    # Today's distribution is printed BESIDE the frozen target rather than replacing it, so
    # drift is visible without being automatic. If these disagree, that is a prompt to
    # re-measure deliberately -- not a licence for the gate to move on its own.
    lens = clause_stats(descs)
    p75 = lens[int(0.75 * len(lens))]
    print(f"wall {wall} · target {target} (frozen, CONSTANTS.md) · today's p75 NOT-clause {p75} "
          f"of {len(lens)} clauses (median {statistics.median(lens):.0f}) "
          f"-> a target derived now would be {wall - p75}\n")
    over = sorted(((len(d), n) for n, (_, d) in descs.items() if len(d) > target), reverse=True)
    if not over:
        print(f"PASS — all {len(descs)} descriptions have headroom for a p75 NOT-clause.")
        return 0
    print(f"{len(over)} of {len(descs)} lack that headroom:")
    for ln, n in over:
        print(f"  {ln:>5}  {n:<34} needs -{ln - target}")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--gate" in sys.argv:
        _d = descriptions()
        _wall = constant("DESCRIPTION_LISTING_TRUNCATION", 1536)
        # FROZEN, not recomputed. A live p75 moved from 1230 to 1231 during a test that
        # lengthened a description: a threshold derived from the population it judges can be
        # raised by the very edit it exists to refuse. See CONSTANTS.md for the derivation.
        _target = constant("DESCRIPTION_HEADROOM_TARGET", 1230)
        _f, _i = gate({n: len(t) for n, (_, t) in _d.items()}, _wall, _target, GRANDFATHERED)
        for x in _i:
            print(f"  improved  {x}")
        for x in _f:
            print(f"  FAIL      {x}")
        _over = over_spec({n: len(t) for n, (_, t) in _d.items()})
        if _over:
            print(f"\n  note      {len(_over)} description(s) exceed the SPEC maximum of "
                  f"{SPEC_MAX_CHARS} ({_over[0][1]} longest) — reported, NOT gated: the spec's limit "
                  f"and the host's {_wall} truncation wall are different constraints, and this gate's "
                  f"target is frozen against the wall. A standing item for the human.")
            print(f"              {'chars':>5} {'floor':>6} {'slack':>6}  unit")
            for _n, _ln in _over:
                _fl = lossless_floor(_d[_n][1])
                _sl = SPEC_MAX_CHARS - _fl
                print(f"              {_ln:5d} {_fl:6d} {_sl:+6d}  {_n}"
                      f"{'' if _sl >= 0 else '   <- cannot comply without deleting a keyword'}")
            _hard = sum(1 for _n, _ in _over if lossless_floor(_d[_n][1]) > SPEC_MAX_CHARS)
            print(f"              {_hard} of {len(_over)} are above the spec even with every "
                  f"connective word removed. See pipeline/decisions/2026-09-12-description-spec-limit.md")
        print(f"\ndescription headroom: {len(_d)} descriptions, wall {_wall}, target {_target}, "
              f"{len(GRANDFATHERED)} declared above it, {len(_over)} above the spec's "
              f"{SPEC_MAX_CHARS} — "
              f"{'PASS' if not _f else str(len(_f)) + ' finding(s)'}")
        sys.exit(1 if _f else 0)
    if "--check" in sys.argv:
        a, b = sys.argv[sys.argv.index("--check") + 1:sys.argv.index("--check") + 3]
        ok, f = check(pathlib.Path(a).read_text(), pathlib.Path(b).read_text())
        print("PASS" if ok else "FAIL")
        for x in f:
            print("  -", x)
        sys.exit(0 if ok else 1)
    sys.exit(main())
