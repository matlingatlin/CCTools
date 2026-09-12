#!/usr/bin/env python3
"""watch.py — has the source changed since we read it?

Why this exists, and why it is not `kb.py stale`
------------------------------------------------
`kb.py stale` measures the AGE of a fetch. Measured 2026-09-04, that is the wrong clock:
nothing in the base was past the 90-day bar, while eight days had produced one INVERTED claim
(a limit a note called undocumented had become documented) and four missing details, with no
value changing. Age did not predict any of it.

The first proposal was a version clock. The measurement killed it: 18 notes cite a watchable
source and exactly 2 pin a version to compare against, both for the same package. So the
signal is not "a new version exists" but the more general **"the bytes we read are not the
bytes that are there now"** — which needs no version, works for any URL, and is exactly what
would have caught both of the day's failures.

The baseline is the raw layer. `knowledge/raw/WATCH.tsv` maps a stored file to the URL it came
from and the sha256 of what we read. This re-fetches and compares.

Deliberately NOT part of `kb.py check`: that runs offline in CI on every push and must stay
dependency-free and network-free. This one talks to the network, so it is run on purpose.

    python3 knowledge/watch.py            # report: same / CHANGED / unreachable
    python3 knowledge/watch.py --quiet    # only the rows that changed (exit 1 if any)

A CHANGED row is not a defect. It means the page moved under a note that cites it, and the
note is now owed a re-read — the ingest routine's `update` branch, not an automatic edit.
"""
import hashlib, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
TSV = ROOT / "knowledge" / "raw" / "WATCH.tsv"

# --- Is a byte change a CONTENT change? ------------------------------------------------------
# The second real batch (2026-09-08) reported 8 CHANGED of which 4 carried no words at all:
# claude.com/customers/block (a Webflow republish: "Last Published" timestamp plus two CSS
# bundle hashes, byte length IDENTICAL) and augmentcode.com's graphify page (a Vercel `?dpl=`
# deploy id, 297 occurrences, byte length identical), on top of the two unsloth.ai pages the
# first batch had already found. Annotating those rows KNOWN-NOISY did not help the reader: the
# annotation is in the file, the CHANGED line is in the output, and the reader still has to
# diff the page by hand to learn nothing. Four rows of 92 crying change every run is how a
# watcher stops being read -- this file's own fetch() comments say so twice.
#
# The first batch tried to fix this with a normaliser and deleted it. This batch shows why no
# normaliser can work: graphify's deploy id is SPLIT ACROSS <script> boundaries by the RSC
# stream, so the fragment carries no `dpl_` prefix to match on. Neutralising every occurrence
# of the literal id left the page unequal; equality needed scrubbing every prefix AND suffix of
# the id, which means the normaliser needs the answer in order to produce it.
#
# So the question changed from "can the noise be normalised away" to "is the noise even in the
# part we cite". It is not. Measured over the four rows, the visible text is 0.7-4.4% of the
# bytes, and all four are byte-for-byte identical under it. A page whose bytes moved while its
# prose did not is reported NOISE and does not fail the run; its notes are owed nothing.
#
# The blind spot is real and measured, not assumed: 16 mutations over the four pages, 4 each.
# A changed prose word fires. A deleted paragraph fires. A changed LINK TARGET does not, and a
# changed script payload does not. That is the price, and it is why this applies ONLY to stored
# copies that are HTML. Markdown rows keep the strict byte comparison, because `<model-id>` in
# a markdown sentence is content that a tag-stripper would eat -- code.claude.com's own
# model-config.md contains exactly that string.
_BLOCK = re.compile(rb"<(script|style|noscript)\b[^>]*>.*?</\1>", re.S | re.I)
_TAG = re.compile(rb"<[^>]+>")
_WS = re.compile(rb"\s+")
# Anchored at the start on purpose: a markdown page quoting `<html>` inside a code fence must
# not be treated as HTML. Measured over all 92 stored files, this agrees with the .html suffix
# on every one -- so the content test is the safer of two signals that do not disagree.
#
# The anchoring is deliberately doubled and the mutation run says so: `^` and `re.match` each
# hold the code-fence fixture on their own, so removing EITHER one survives the selftest and
# only removing BOTH is caught. That is recorded rather than papered over -- a reader looking
# for the load-bearing line will not find one, because there is not one.
_HTML_START = re.compile(rb"^\s*(?:\xef\xbb\xbf)?<(?:!doctype\s+html|html\b)", re.I)


def is_html(body):
    """Does this stored copy start as an HTML document? Only those get the text comparison."""
    return bool(body) and bool(_HTML_START.match(body[:200]))


# A RENDERED RELATIVE TIMESTAMP -- "Last updated 6 days ago" -- and the reason this one narrow
# rule is not the normaliser this file already deleted twice.
#
# Measured 2026-09-11, third real batch: both unsloth.ai pages reported CHANGED with a
# one-word diff, "Last updated 10" -> "13" and "4" -> "6". The counter is inside the VISIBLE
# TEXT, so the noise verdict is blind to it by construction, and it ticks every single day:
# those two rows would report CHANGED on every run forever.
#
# What makes it different from the deploy id: the counter counts UP FROM A FIXED EDIT DATE, so
# a rising number is positive evidence the page was NOT updated. The token that fires the alarm
# is the token proving nothing changed. And "N <unit> ago" is a universal web idiom rather than
# one site's bundler quirk, so the rule needs no per-row knowledge -- which was exactly the test
# the deploy-id normaliser failed (it needed the answer in order to produce it).
#
# Scoped hard on purpose: the number must be FOLLOWED by a time unit and the word "ago". A bare
# number, a version, a price and a date are all untouched, and selftest asserts each of those.
_AGO = re.compile(rb"\b\d+\s+(second|minute|hour|day|week|month|year)s?\s+ago\b", re.I)


def visible_text(body):
    """The part of an HTML page a note can cite: no scripts, no styles, no tags, no runs of
    whitespace. Everything a bundler, a deploy pipeline or a CDN churns lives outside it -- plus
    the one thing that churns INSIDE it without meaning anything, a relative timestamp."""
    t = _WS.sub(b" ", _TAG.sub(b" ", _BLOCK.sub(b" ", body))).strip()
    return _AGO.sub(b"<RELATIVE-TIME>", t)


def verdict(stored, fetched_body):
    """same | noise | changed -- for one row, given our stored copy and what is there now.

    Kept as a function with fixtures rather than inline, because this repo has already been
    bitten once by a predicate that lived inside its own caller and passed while blind.
    """
    if hashlib.sha256(fetched_body).digest() == hashlib.sha256(stored).digest():
        return "same"
    if is_html(stored) and is_html(fetched_body) \
            and visible_text(stored) == visible_text(fetched_body):
        return "noise"
    return "changed"

# NOT normalised, and the measurement is why. The watcher's first real batch (2026-09-08)
# reported 4 CHANGED rows of which ONE carried a content change. Two of the false three were
# unsloth.ai GitBook pages, and a narrow normaliser was written for them and then DELETED:
# neutralising the deploy id (`?dpl=p-...`, 681 occurrences) still left the page unequal, because
# the bundler's asset hashes churn too -- and past those, the chunk NUMBERS differ (`9495` vs
# `9455`). The bundle splitting itself changes on every deploy. No narrow rule makes such a page
# stable, and a wide one is how a watcher quietly stops watching. Those two rows are recorded as
# structurally noisy instead; see knowledge/raw/WATCH.tsv and the note that cites them.

def fetch(url):
    """curl, because the environment's proxy and CA bundle are already configured for it.

    `-f` is not optional and was missing in the first version, which cost a false alarm the
    same afternoon: without it curl exits 0 on an HTTP 429 or 500 and hands back the ERROR
    PAGE's body, which the caller then hashes and reports as "the source changed". A watcher
    that cries change on a rate limit is a watcher nobody reads. `-g` is not optional either:
    curl treats `{}` in a URL as a glob, so a malformed source URL silently fetches something
    else entirely — which is exactly how a brace-expansion shorthand in a note's frontmatter
    ended up baselined as if it were a real page.
    """
    r = subprocess.run(["curl", "-sSfLg", "--max-time", "30", url], capture_output=True)
    if r.returncode != 0:
        # One retry after a real pause, because "unreachable" must mean the source, not us.
        # ~30 of these rows are raw.githubusercontent.com: a single pass hammers a handful of
        # hosts, and measured on 2026-09-04 a run reported 9 unreachable that all answered 200
        # individually. The pause below plus this retry took that to 0. A watcher that cries
        # unreachable teaches the reader to discount the row that is finally real.
        time.sleep(3)
        r = subprocess.run(["curl", "-sSfLg", "--max-time", "30", url], capture_output=True)
    # A run of ~75 fetches hits a handful of hosts, and without a pause it rate-limits ITSELF:
    # runs on 2026-09-04 reported one to three sources unreachable, and every one of them
    # answered 200 when fetched individually seconds later. A watcher that manufactures its own
    # "unreachable" rows teaches the reader to discount them, which is how a real dead citation
    # gets missed. Measured cost of the fix: about 25 seconds added to a weekly job.
    time.sleep(0.35)
    return r.stdout if r.returncode == 0 and r.stdout else None


# Raw files that will never appear in WATCH.tsv, and the reason. A file that matches none of
# these and is not watched FAILS the offline check -- which is the point: today the raw layer's
# 106 unwatched files are accounted for by inspection, and inspection does not survive the next
# ingest. Each entry is a directory prefix or an exact path, and adding one costs a line.
NEVER_WATCHED = {
    # No URL exists to re-fetch. The transcript IS the artefact.
    "knowledge/raw/video-transcripts-": "a transcript, not a page",
    "knowledge/raw/instagram-": "screenshots of a carousel; no addressable URL",
    # arXiv is versioned and immutable at a version id; watching it reports nothing. Recorded
    # in MANIFEST.md alongside the 33 doi.org/usenix.org URLs deliberately not baselined.
    "knowledge/raw/untried-surfaces-2026-09-08/arxiv.org_": "arXiv version ids are immutable",
    # A news article whose sidebar rotates other articles' headlines. Dropped 2026-09-11 after
    # THREE hand-verified chrome-only changes in one day - the body was stable every time. The
    # decisive argument is not the noise but the VALUE: every claim this base took from it was
    # already corrected against the primary paper (the benchmark is v1.5 not v1.6; "state of the
    # art" is a 0.02-point lead), so it is a superseded secondary and change-detection on it buys
    # nothing. Re-entry condition, recorded so the drop is recoverable the way the 2026-09-04
    # drops were: a chrome test that needs no per-site pattern - the same diff appearing across
    # several pages of one host - would make this row watchable again.
    # Both dated copies, because dropping the row leaves the OLDER one with nothing to be
    # superseded by - which the accounting caught immediately and correctly.
    "knowledge/raw/watch-2026-09-11/the-decoder.com_unlimited-ocr.html":
        "sidebar rotates other articles hourly; a superseded secondary",
    "knowledge/raw/watch-2026-09-08c/the-decoder.com_unlimited-ocr.html":
        "the earlier copy of the same dropped article",
    # The HF listing's payload carries download counters, so every fetch differs for a reason
    # that is not a change. Its model CARD is watched instead.
    "knowledge/raw/untried-surfaces-2026-09-08/huggingface.co_api_models_author-zai-org.json":
        "payload carries download counters",
    # The first binaries in the raw layer (2026-09-11), held because four notes cited PDF sources
    # and none was kept. Not watched, and the reason is a real limit of this tool rather than a
    # preference: the noise verdict works by falling back to VISIBLE TEXT when bytes differ, and a
    # PDF has no such fallback. Its bytes move when a producer re-stamps a timestamp; asking
    # whether the WORDS moved means extracting them, and `knowledge/pdftext.py` measures that the
    # Anthropic guide is only 17.6% extractable here (hex-coded CID text needing ToUnicode CMaps).
    # So a row for it could only report CHANGED with no way to triage - the cry-wolf failure the
    # noise verdict exists to end. Re-entry condition: if it ever reads above
    # pdftext.COVERAGE_FLOOR, it is watchable on the same terms as any HTML page.
    "knowledge/raw/pdf-sources-2026-09-11/resources.anthropic.com_hubfs_":
        "a PDF: no visible-text fallback, and only 17.6% of it extracts here",
    # These two DO read at 100.0%, so the tool is not the reason. They are finished documents - a
    # 1981 journal article and a 2014 conference paper - and a revision would be a new URL, not an
    # edit to this one. Watched for what a future change could tell you, per the 2026-09-11 rule;
    # for these the answer is nothing.
    "knowledge/raw/pdf-sources-2026-09-11/www.cs.umd.edu_":
        "a finished 1981 journal article; a revision would be a new URL",
    "knowledge/raw/pdf-sources-2026-09-11/www.microsoft.com_":
        "a finished 2014 conference paper; a revision would be a new URL",
    # The five arXiv primaries held the same day, for the same reason the three above were: cited
    # by two notes, never kept.
    #
    # The reason first recorded here -- "an arXiv version id is immutable, so the URL cannot change
    # under us" -- was WRONG, and measured wrong on 2026-09-12 by the very file it excluded. The
    # version id is immutable; `arxiv.org/pdf/<id>` WITHOUT a version suffix resolves to the LATEST
    # version, and that is the form all five are stored under. 2605.17193 has since been revised:
    # the held copy is 93 pages and titles itself "(NMI Revision)", while `.../2605.17193v1` is 64
    # pages and says twelve intervention strategies and 45 tested conditions where the revision
    # says thirteen and 73. A note's figures matched v1 exactly -- the note was right and the paper
    # moved under it. So an unpinned preprint URL is a MOVING source, and the reason it is not
    # watched is the same one as the Anthropic guide above: a PDF has no visible-text fallback, so
    # a row could only report CHANGED with no way to triage it.
    #
    # The operational fix is at the citation, not here: cite a version-pinned URL (`<id>v1`) when a
    # claim rests on a specific reading, so a revision cannot silently invalidate it. Re-entry
    # condition, same as the guide's: a PDF text surface this repo actually depends on would make
    # these watchable on the same terms as any HTML page.
    "knowledge/raw/pdf-sources-2026-09-11/arxiv.org_pdf_":
        "a PDF: no visible-text fallback. NB the URL is unpinned, so it follows the latest version",
    # And the version-pinned copy held 2026-09-12 so the pinned citation is producible from this
    # repo. Here the original reasoning IS true: `<id>v1` cannot change under us.
    "knowledge/raw/pdf-sources-2026-09-12/arxiv.org_pdf_":
        "a version-pinned arXiv PDF: genuinely immutable, and a PDF has no visible-text fallback",
}


def snapshot_dir(path):
    """A repo snapshot pinned at a commit: `name@ref@<sha>` in a path segment. Immutable by
    construction, so watching it is meaningless -- the sha IS the version."""
    return bool(re.search(r"@[0-9a-f]{7,40}(/|$)", path))


def account(watched, urls, present):
    """Every stored raw file must be watched, superseded, pinned or declared. Returns the ones
    that are NONE of those -- a file nobody can say anything about.

    `urls` maps a stored path to the URL its row watches; a file NOT in WATCH.tsv whose own
    basename is watched at another path is a superseded baseline, which is the normal outcome
    of a re-baseline and is exactly what must not be reported as a hole.
    """
    # Two storage conventions live side by side: `<host>_<path>.<ext>` and `<page>@<date>.<ext>`.
    # Stripping a trailing `@<tag>` reconciles them, so `skills@2026-09-04.md` and
    # `skills@2026-09-08b.md` are recognised as the same page at two dates. This is a HEURISTIC
    # on filenames, and it is the one place here that could hide a real hole -- a file wrongly
    # judged superseded is a file nobody watches. It is narrow on purpose: the stem must match a
    # WATCHED file exactly, and the raw layer's names encode host and path, not titles.
    stem = lambda n: re.sub(r"@[^.@/]+(?=\.[^.]*$)", "", n)
    watched_names = {stem(pathlib.PurePath(p).name) for p in watched}
    orphans = []
    for f in present:
        if f in watched or snapshot_dir(f):
            continue
        if any(f.startswith(k) or f == k for k in NEVER_WATCHED):
            continue
        if stem(pathlib.PurePath(f).name) in watched_names:
            continue                      # superseded baseline: the URL is watched at its newer copy
        orphans.append(f)
    return orphans


def integrity(raw_lines, root=None):
    """The offline half of this tool, and it used to run only once a week over the network.

    Every check here needs no network at all, so it belongs on every push: a malformed row, a
    row pointing at a file that is not there, the same URL watched twice (one wasted fetch per
    run, forever, and the same source reported to the reader twice -- found 2026-09-08, one
    instance), and above all the TAMPER check, which is about OUR bytes and never needed the
    internet to answer.
    """
    root = ROOT if root is None else root
    findings, rows = [], []
    for i, l in enumerate(raw_lines, 1):
        if not l or l.startswith("#"):
            continue
        parts = l.split("\t")
        if len(parts) != 4:
            findings.append(f"line {i}: {len(parts)} tab-separated fields, expected 4")
            continue
        rows.append((i, *parts))
    seen_path, seen_url = {}, {}
    for i, path, url, fetched, sha in rows:
        if not re.fullmatch(r"[0-9a-f]{64}", sha):
            findings.append(f"line {i}: sha is not 64 hex characters")
        if path in seen_path:
            findings.append(f"line {i}: path already watched at line {seen_path[path]}")
        if url in seen_url:
            findings.append(f"line {i}: URL already watched at line {seen_url[url]} — one wasted "
                            f"fetch every run, and the reader sees the source twice")
        seen_path[path], seen_url[url] = i, i
        f = root / path
        if not f.exists():
            findings.append(f"line {i}: stored file is missing: {path}")
        elif hashlib.sha256(f.read_bytes()).hexdigest() != sha:
            findings.append(f"line {i}: TAMPERED — {path} no longer matches its recorded sha. "
                            f"The raw layer is immutable by rule; restore it from git")
    return findings, rows


# The forms one source is addressable AS. The watcher deliberately watches the form that CARRIES
# THE CLAIM, not the form a note cites: a GitHub repo page changes on every star, its README does
# not; a HF model page carries download counters, its card does not; a PyPI project page carries
# download counts, its JSON API does not. So a note citing `github.com/o/r` and a row watching
# `raw.githubusercontent.com/o/r/HEAD/README.md` are the same source, and naive URL equality
# reports a hole that is not there.
#
# THIS MAP IS INCOMPLETE BY CONSTRUCTION and the measurement it feeds is a REPORT, never a gate.
# Measured 2026-09-08: naive equality claimed 84 unwatched citations; with the map it was 22, and
# two of those 22 were still artifacts of forms the map did not yet know (a HF `/blob/` licence
# and a PyPI project page). A gate built on this would manufacture false holes, and a check that
# cries wolf is one nobody reads -- this file has learned that twice already. Every line it prints
# is a CANDIDATE to check by hand.
def url_forms(u):
    u = u.strip().strip("\"'").rstrip("/").replace("http://", "https://")
    out = {u, u + "/"}
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)$", u)
    if m:
        out |= {f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{b}/README.md"
                for b in ("HEAD", "main", "master")}
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)$", u)
    if m:
        out.add(f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{m.group(3)}/{m.group(4)}")
    m = re.match(r"https://huggingface\.co/([^/]+)/([^/]+)$", u)
    if m:
        out.add(f"https://huggingface.co/{m.group(1)}/{m.group(2)}/raw/main/README.md")
    m = re.match(r"https://huggingface\.co/([^/]+)/([^/]+)/blob/(.+)$", u)
    if m:
        out.add(f"https://huggingface.co/{m.group(1)}/{m.group(2)}/raw/{m.group(3)}")
    m = re.match(r"https://pypi\.org/project/([^/]+)$", u)
    if m:
        out.add(f"https://pypi.org/pypi/{m.group(1)}/json")
    if re.match(r"https://(code|platform)\.claude\.com/docs/", u) and not u.endswith(".md"):
        out.add(u + ".md")
    if u.endswith(".md"):
        out.add(u[:-3])
    return out


# Source kinds that do not change under their own identifier, so watching one can only ever
# return "same" -- and a wall of green would imply the whole base is watched when it is not.
IMMUTABLE_KIND = re.compile(
    r"(arxiv\.org|doi\.org|usenix\.org|zenodo|/abs/|\.pdf$|apps\.dtic\.mil|cacm\.acm\.org|"
    r"insights\.sei\.cmu\.edu)", re.I)


def coverage():
    """Which sources the NOTES cite are not watched? A report, never a gate -- see url_forms."""
    watched = {l.split("\t")[1].rstrip("/").replace("http://", "https://")
               for l in TSV.read_text().splitlines() if l and not l.startswith("#")}
    cited = {}
    for f in sorted((ROOT / "knowledge" / "notes").glob("*.md")):
        m = re.match(r"^---\n(.*?)\n---\n", f.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        for u in re.findall(r"^\s*-?\s*url:\s*(\S+)", m.group(1), re.M):
            u = u.strip().strip("\"'")
            if u.startswith("http"):
                cited.setdefault(u, set()).add(f.stem)
    covered = [u for u in cited if url_forms(u) & watched]
    imm = [u for u in cited if u not in covered and IMMUTABLE_KIND.search(u)]
    open_ = sorted(u for u in cited if u not in covered and u not in imm)
    for u in open_:
        print(f"  candidate  {u}\n             cited by {', '.join(sorted(cited[u]))}")
    print(f"\ncoverage (REPORT, not a gate): {len(cited)} cited URLs — {len(covered)} watched, "
          f"{len(imm)} immutable by kind, {len(open_)} to check by hand")
    return 0


def offline():
    """Everything this tool can say without touching the network. Runs in CI on every push."""
    lines = TSV.read_text().splitlines()
    findings, rows = integrity(lines)
    watched = {r[1] for r in rows}
    present = [str(p.relative_to(ROOT)) for p in (ROOT / "knowledge" / "raw").rglob("*")
               if p.is_file() and p.name not in ("README.md", "MANIFEST.md", "WATCH.tsv")]
    orphans = account(watched, {r[1]: r[2] for r in rows}, present)
    for o in sorted(orphans):
        findings.append(f"unaccounted raw file: {o} — watch it, or declare it in NEVER_WATCHED "
                        f"with the reason it cannot be watched")
    for f in findings:
        print(f"  FAIL  {f}")
    print(f"\nwatch.py offline: {len(rows)} rows, {len(present)} raw files "
          f"({len(present) - len(orphans) - len(watched)} accounted for without being watched) — "
          f"{'PASS' if not findings else str(len(findings)) + ' finding(s)'}")
    return 1 if findings else 0


def main():
    quiet = "--quiet" in sys.argv
    rows = [l.split("\t") for l in TSV.read_text().splitlines() if l and not l.startswith("#")]
    changed, same, noise, dead, tampered = [], [], [], [], []
    for path, url, fetched, sha in rows:
        # Two different questions, and they were being asked as one.
        #
        # (1) Is OUR stored copy still the bytes we recorded? The raw layer is immutable by
        #     rule and nothing checked it. This is that check, and it uses the RAW sha.
        stored = ROOT / path
        base = stored.read_bytes() if stored.exists() else None
        intact = base is not None and hashlib.sha256(base).hexdigest() == sha
        if base is not None and not intact:
            tampered.append((path, url))
        # (2) Has the SOURCE changed? The byte comparison is against the recorded sha and is
        #     never relaxed. Only when the bytes differ does the NOISE question get asked, and
        #     only for a stored copy that is HTML and verified intact -- a tampered baseline is
        #     not evidence that today's page says the same thing.
        body = fetch(url)
        if body is None:
            dead.append((path, url)); continue
        now = hashlib.sha256(body).hexdigest()
        if now == sha:
            same.append((path, url, fetched, sha[:12], now[:12]))
        elif intact and verdict(base, body) == "noise":
            pct = 100 * len(visible_text(base)) / max(1, len(base))
            noise.append((path, url, fetched, pct))
        else:
            changed.append((path, url, fetched, sha[:12], now[:12]))
    if not quiet:
        for p, u, f, _, _ in same:
            print(f"  same       {u}  (read {f})")
        for p, u in dead:
            print(f"  UNREACHABLE {u}  — could not fetch; not evidence of anything")
    for p, u, f, pct in noise:
        print(f"  noise      {u}\n             bytes moved, visible text identical "
              f"(prose is {pct:.1f}% of the page). No note is owed a re-read.")
    for p, u in tampered:
        print(f"  TAMPERED   {p}\n             the stored bytes no longer match the sha recorded "
              f"for them. The raw layer is immutable by rule; restore it from git.")
    for p, u, f, was, now in changed:
        print(f"  CHANGED    {u}\n             read {f} as {was}, now {now}\n             baseline: {p}")
    print(f"\n{len(same)} unchanged · {len(changed)} changed · {len(noise)} noise "
          f"· {len(dead)} unreachable · {len(tampered)} tampered · {len(rows)} watched")
    if changed:
        print("A changed page owes its citing notes a re-read (llm-wiki-ingest, update branch).")
    # Tampering fails too: an edited raw file is a broken invariant, not a notice. NOISE does
    # not fail: a page whose prose did not move owes nobody anything, and failing on it is what
    # trained the reader to skip the output in the first place.
    sys.exit(1 if (changed or tampered) else 0)


def selftest():
    """Offline. Runs in CI, because the predicate above decides whether a run fails.

    Every fixture is a pair that must NOT fire and a pair that MUST, and the mutations are the
    ones measured against the four live pages on 2026-09-08.
    """
    page = (b'<!DOCTYPE html><html><head><style>a{color:red}</style>'
            b'<script src="/_next/x.js?dpl=dpl_AAAA"></script></head>'
            b'<body><h1>Graphify</h1><p>It builds a code graph.</p>'
            b'<a href="/learn/graphify">docs</a></body></html>')
    fails = []

    def check(label, got, want):
        print(f"  {'ok  ' if got == want else 'FAIL'} {label}: {got!r}")
        if got != want:
            fails.append(label)

    # A deploy id churns; the prose does not.
    check("deploy id only -> noise",
          verdict(page, page.replace(b"dpl_AAAA", b"dpl_BBBB")), "noise")
    # A CSS bundle hash churns, byte length identical (the block.html shape).
    check("asset hash, same length -> noise",
          verdict(page, page.replace(b"a{color:red}", b"a{color:blu}")), "noise")
    # Identical bytes are not noise, they are the same page.
    check("identical bytes -> same", verdict(page, page), "same")
    # A prose word MUST fire -- this is the whole reason the row is still watched.
    check("prose word -> changed",
          verdict(page, page.replace(b"code graph", b"knowledge graph")), "changed")
    check("paragraph deleted -> changed",
          verdict(page, page.replace(b"<p>It builds a code graph.</p>", b"")), "changed")
    # The measured blind spot, asserted rather than hoped for: a link-target-only change is
    # reported as noise. If that ever becomes unacceptable for a row, the row needs a note that
    # cites the target, and this fixture is where the decision gets revisited.
    check("link target only -> noise (KNOWN BLIND SPOT)",
          verdict(page, page.replace(b"/learn/graphify", b"/learn/moved")), "noise")
    # Case is content. The first real batch's one true change was a new `## Web UI` heading,
    # and a comparison that folded case would have called it noise.
    check("capitalisation only -> changed",
          verdict(page, page.replace(b"code graph", b"Code Graph")), "changed")
    # A rendered relative timestamp ticks daily and means the page was NOT edited.
    ago = b"<html><body><p>Docs.</p><span>Last updated 6 days ago</span></body></html>"
    check("relative timestamp only -> noise",
          verdict(ago, ago.replace(b"6 days ago", b"13 days ago")), "noise")
    check("unit change in a relative timestamp -> noise",
          verdict(ago, ago.replace(b"6 days ago", b"3 weeks ago")), "noise")
    # ORDER MATTERS, and this fixture is what proves it. Frameworks routinely wrap the number in
    # its own element; applied to raw HTML the pattern would not match across the tag and the rule
    # would silently stop working on exactly the pages it exists for. Strip tags FIRST, then
    # neutralise. A mutation that reorders these two survived every other fixture here.
    split = b"<html><body><p>Docs.</p><span>Last updated <b>6</b> days ago</span></body></html>"
    check("a tag-split relative timestamp -> noise",
          verdict(split, split.replace(b"<b>6</b>", b"<b>13</b>")), "noise")
    # ...and everything number-shaped that is NOT a relative timestamp must still fire.
    price = b"<html><body><p>Flash is $0.075 per MTok.</p></body></html>"
    check("a price is not a relative time -> changed",
          verdict(price, price.replace(b"$0.075", b"$0.15")), "changed")
    ver = b"<html><body><p>Requires v2.1.257 or later.</p></body></html>"
    check("a version is not a relative time -> changed",
          verdict(ver, ver.replace(b"2.1.257", b"2.1.261")), "changed")
    bare = b"<html><body><p>It ships 6 days of logs.</p></body></html>"
    check("a bare number with no 'ago' -> changed",
          verdict(bare, bare.replace(b"6 days", b"13 days")), "changed")
    # Markdown never gets the relaxed comparison. `<model-id>` is real content in
    # code.claude.com/docs/en/model-config.md, and a tag-stripper eats it.
    md = b"Claude Code uses `Custom model (<model-id>)` when you omit the description.\n"
    check("markdown is not html", is_html(md), False)
    check("markdown, tag-shaped content changed -> changed",
          verdict(md, md.replace(b"<model-id>", b"<model_id>")), "changed")
    # A code fence quoting an HTML doctype is still markdown.
    fence = b"Paste this:\n\n```html\n<!DOCTYPE html><html></html>\n```\n"
    check("code fence quoting a doctype is not html", is_html(fence), False)
    # An empty or unreadable stored copy must not be classified as HTML.
    check("empty body is not html", is_html(b""), False)


    # --- the offline half: accounting and TSV integrity -------------------------------------
    # A pinned snapshot is immutable by construction and must never be reported as a hole.
    check("repo@sha snapshot is pinned", snapshot_dir("knowledge/raw/x@main@a4ce143/docs/a.md"), True)
    check("a dated dir is NOT a pinned snapshot", snapshot_dir("knowledge/raw/watch-2026-09-08/a.md"), False)
    # A date tag is stripped before the superseded test, so two dates of one page reconcile...
    check("superseded baseline is accounted",
          account({"raw/b/skills@2026-09-08b.md"}, {}, ["raw/a/skills@2026-09-04.md"]), [])
    # ...but a page nobody watches is still a hole. If this ever passes, the heuristic above has
    # started hiding exactly what it was written not to hide.
    check("an unwatched page IS a hole",
          account({"raw/b/skills@2026-09-08b.md"}, {}, ["raw/a/hooks@2026-09-04.md"]),
          ["raw/a/hooks@2026-09-04.md"])
    check("a declared file is accounted",
          account(set(), {}, ["knowledge/raw/video-transcripts-2026-09-02/t.md"]), [])

    row = "p\tu\t2026-09-08\t" + "a" * 64
    check("a well-formed row with a missing file is caught",
          len(integrity([row])[0]), 1)
    check("three fields is caught", len(integrity(["a\tb\tc"])[0]), 1)
    check("a short sha is caught", len(integrity(["p\tu\td\tabc"])[0]), 2)  # bad sha + missing file
    check("a duplicate URL is caught",
          any("already watched" in f for f in integrity([row, "q\tu\td\t" + "b" * 64])[0]), True)
    check("comments and blank lines are skipped", integrity(["# c", ""]), ([], []))

    # The tamper branch needs a file that EXISTS, so it gets one. Without this the check can be
    # deleted outright and every other fixture still passes -- which is exactly what a mutation
    # run showed before this was written.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        (tmp / "kept.md").write_bytes(b"the bytes we recorded")
        good = hashlib.sha256(b"the bytes we recorded").hexdigest()
        check("an intact stored file passes",
              integrity([f"kept.md\tu\td\t{good}"], tmp)[0], [])
        check("a stored file that no longer matches its sha is TAMPERED",
              any("TAMPERED" in f for f in integrity([f"kept.md\tu\td\t{'0' * 64}"], tmp)[0]), True)

    print(f"\n{'PASS' if not fails else 'FAIL: ' + ', '.join(fails)} "
          f"— watch.py predicate, 29 fixtures")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--offline" in sys.argv:
        sys.exit(offline())
    if "--coverage" in sys.argv:
        sys.exit(coverage())
    main()
