#!/usr/bin/env python3
"""Stdlib-only PDF text extraction, with a coverage guard.

Why this exists. This environment has no PDF toolchain: every poppler binary is absent and
`pypdf` is installed but panics on a missing `_cffi_backend`. Four notes in this base cite PDF
sources. `zlib` and `re` are stdlib, and PDF content streams are usually FlateDecode, so *some*
PDFs can be read here with no install at all.

Why the guard is the point. A PDF's text lives in two forms: literal `(strings)`, which are
readable directly, and hex `<codes>` under CID fonts, which mean nothing without the font's
ToUnicode CMap. A reader that handles only the first silently returns whatever it found — and
that output looks like clean prose, because it IS clean prose with most of the words missing.
Measured on the Anthropic skills guide 2026-09-11: 25.4% of text BYTES decodable, and the
extracted text read as grammatical English sentences. Nothing in the output marked the holes.

The unit is bytes, deliberately. A literal string is one byte per character; a CID code in that
file is TWO bytes per character (Identity encoding, CIDFontType2, codespace <0000>-<FFFF>), so
the same document is 40.6% decodable counted in characters. Both are true. This tool reports the
byte ratio because it is the LOWER of the two, and every error in a guard like this should fall
on the side of refusing a document it could have read, never on passing one it could not.

So this tool never just returns text. It returns text AND the decodable byte fraction, and it
refuses below a floor. Use it to answer "can this PDF be read here at all?" before trusting
anything it hands back.

What it does NOT do: ToUnicode CMaps, CID fonts, encrypted PDFs, DCTDecode images, OCR. Those
need a real library. This is a probe, not a replacement.

    python3 knowledge/pdftext.py FILE.pdf              # text, or a refusal
    python3 knowledge/pdftext.py FILE.pdf --coverage   # just the verdict
    python3 knowledge/pdftext.py --selftest
"""
import re
import sys
import time
import zlib

# Below this share of decodable glyphs the output is a fragment wearing the shape of a document.
# Not tuned: any floor under 1.0 admits silent holes, so the number only decides how loudly.
COVERAGE_FLOOR = 0.98

_STREAM = re.compile(rb"stream\r?\n")
# Streams whose own dictionary says they are not page content: raster images, embedded font
# programs (/FontFile*, and /Length1 which font programs carry), XMP metadata, attachments.
_NOT_CONTENT = re.compile(rb"/Subtype\s*/Image|/FontFile\d?|/Length1\b|/Subtype\s*/XML"
                          rb"|/Type\s*/Metadata|/Type\s*/EmbeddedFile")
_STR = re.compile(rb"\((?:\\.|[^()\\])*\)", re.S)
_HEX = re.compile(rb"<([0-9A-Fa-f]{4,})>")
# Inside a TJ array the numbers between strings are kerning, in thousandths of an em, negative
# meaning "move right". A word space is drawn as a gap, not as a character, so a reader that
# ignores these produces one unbroken string of letters. Measured 2026-09-11 before this existed:
# the Kim et al. paper came out with ONE space in 74,422 letters and still reported 100% coverage.
# -140 is the usual break point between letter-fit kerning (tens) and a real space (hundreds).
KERN_SPACE = -140.0

# One pass over a showing operator, in document order, so kerning lands BETWEEN its neighbours.
_PIECE = re.compile(rb"(\((?:\\.|[^()\\])*\))"      # 1: literal string
                    rb"|(<[0-9A-Fa-f]{2,}>)"          # 2: hex string (undecodable here)
                    rb"|(-?\d+(?:\.\d+)?)", re.S)    # 3: a kerning number

_SHOW = re.compile(rb"\[(?:[^\[\]]|\\.)*\]\s*TJ"          # [ (a) -20 (b) ] TJ
                   rb"|\((?:\\.|[^()\\])*\)\s*(?:Tj|'|\")"  # (a) Tj
                   rb"|<[0-9A-Fa-f]*>\s*Tj"                 # <00A1> Tj
                   rb"|(?:TD|Td|T\*|ET)", re.S)
_ESC = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f",
        b"(": b"(", b")": b")", b"\\": b"\\"}


def unescape(s):
    """PDF literal-string escapes, including octal. Unknown escapes drop their backslash."""
    out, i = bytearray(), 0
    while i < len(s):
        c = s[i:i + 1]
        if c == b"\\" and i + 1 < len(s):
            nxt = s[i + 1:i + 2]
            if nxt in _ESC:
                out += _ESC[nxt]
                i += 2
                continue
            if nxt.isdigit():
                j = i + 1
                while j < len(s) and j < i + 4 and s[j:j + 1].isdigit():
                    j += 1
                out.append(int(s[i + 1:j], 8) & 0xFF)
                i = j
                continue
            i += 2
            continue
        out += c
        i += 1
    return bytes(out)


def streams(data):
    """Decompressed FlateDecode CONTENT streams. Anything else is skipped, not guessed at.

    Images are excluded deliberately, and it is not only a speed question. A raster XObject is
    Flate-compressed exactly like a content stream, so an earlier version decompressed 302 KB of
    pixel data and ran the text-operator scan over it: minutes of regex backtracking, and any
    byte run that happened to look like `(...)Tj` would have been counted as literal text and
    inflated the coverage figure with pixels. Found 2026-09-11 on arXiv 2106.09482, whose stream
    24 is a solid run of `{` bytes.
    """
    for m in _STREAM.finditer(data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end < 0:
            continue
        head = data[max(0, m.start() - 400):m.start()]
        if b"/FlateDecode" not in head or _NOT_CONTENT.search(head):
            continue
        try:
            body = zlib.decompress(data[start:end].rstrip(b"\r\n"))
        except zlib.error:
            continue
        if not is_content(body):
            continue
        yield body


def is_content(body, sample=1024, floor=0.9):
    """Does this decompressed stream look like page-content operators at all?

    The dictionary sniff above can only skip the stream types someone thought to name, and the
    list will always be incomplete: a PDF Flate-compresses images, font programs, metadata and
    attachments with exactly the same filter as page content. Found the hard way 2026-09-11 --
    filtering images fixed one file and arXiv 2605.17193 still hung, on an embedded OpenType font
    (GDEF/GPOS/GSUB tables) that is not an image and carries no marker this tool knew.

    So this asks the bytes instead of the dictionary, and needs to know nothing about formats:
    real content streams are operators and numbers, overwhelmingly printable ASCII. Binary blobs
    are not. That is a catch-all for every wrong stream type, including the ones not invented yet.
    """
    head = body[:sample]
    if not head:
        return False
    ok = sum(1 for b in head if 32 <= b < 127 or b in (9, 10, 13))
    return ok / len(head) >= floor


def show(stream):
    """(text, literal_bytes, hex_bytes) for one content stream.

    The two counts are the whole point: hex bytes are text this tool cannot read, and counting
    them is the only way the caller learns the output has holes. Bytes, not characters - see
    the module docstring on why the guard takes the more pessimistic of the two units.
    """
    out, lit, hexb = [], 0, 0
    for m in _SHOW.finditer(stream):
        tok = m.group(0)
        if tok in (b"TD", b"Td", b"T*", b"ET"):
            out.append(b"\n")
            continue
        for piece in _PIECE.finditer(tok):
            lit_s, hex_s, kern = piece.group(1), piece.group(2), piece.group(3)
            if lit_s is not None:
                d = unescape(lit_s[1:-1])
                lit += len(d)
                out.append(d)
            elif hex_s is not None:
                hexb += (len(hex_s) - 2) // 2
            elif kern is not None and float(kern) <= KERN_SPACE:
                out.append(b" ")
    return b"".join(out), lit, hexb


def extract(data):
    """(text, coverage) over a whole PDF. coverage is None when there is no text at all."""
    chunks, lit, hexb = [], 0, 0
    for s in streams(data):
        t, l, h = show(s)
        chunks.append(t)
        lit += l
        hexb += h
    total = lit + hexb
    return b"\n".join(chunks), (None if total == 0 else lit / total)


# Prose has word spaces. A PDF draws most of them as kerning gaps rather than characters, so a
# reader that drops kerning returns one unbroken run of letters -- which coverage cannot see,
# because every byte WAS decoded. Measured on English prose in this repo: 0.19 spaces per letter.
# A tenth of that is not prose. This is the second half of the guard and it exists because the
# first half passed a document at 100.0% that had one space in 74,422 letters.
SPACE_RATIO_FLOOR = 0.02


def fidelity(text):
    """Concerns about text that DECODED cleanly but may not be faithful. Pure; separate from
    coverage on purpose -- coverage asks how much came out, this asks whether it reads."""
    concerns = []
    letters = sum(1 for c in text if c.isalpha())
    if letters >= 200:
        ratio = text.count(" ") / letters
        if ratio < SPACE_RATIO_FLOOR:
            concerns.append(f"{ratio:.3f} spaces per letter (prose is ~0.19): word gaps were "
                            f"drawn as kerning and have been lost, so the words are run together")
    return concerns


def verdict(coverage, floor=COVERAGE_FLOOR, concerns=()):
    """What the caller is allowed to do with the text. Pure, so it can be tested."""
    if coverage is None:
        return "NO-TEXT", ("no text-showing operators at all - a scanned or image-only PDF, "
                           "which needs OCR and not this")
    pct = f"{100 * coverage:.1f}%"
    if coverage >= floor and concerns:
        return "SUSPECT", (f"{pct} of text bytes decoded, but the output does not read as prose: "
                           + "; ".join(concerns))
    if coverage >= floor:
        # Deliberately NOT "whole enough to quote from". Ligature and symbol glyphs (fi, fl, ff,
        # dashes) are single glyphs mapped through a font's /Differences encoding, which this tool
        # does not read, so they drop SILENTLY and coverage stays at 100%. Measured 2026-09-11 on
        # the Kim et al. paper: 41 occurrences of "bene" and zero of "benefit". Compare quotes with
        # a ligature-tolerant match, never an exact substring.
        return "READABLE", (f"{pct} of text bytes decoded and it reads as prose - but ligatures "
                            f"(fi/fl/ff) and symbols can drop silently, so match quotes loosely")
    return "REFUSED", (f"only {pct} of text bytes decoded; the rest is hex-coded CID text needing a "
                       f"ToUnicode CMap. The text that WOULD be returned reads as clean prose "
                       f"with the holes invisible, so it is withheld rather than shown")


def report(data):
    """(text, tag, why) for a whole PDF file's bytes.

    The decision path lives here rather than in main() so a fixture can reach it. It was in main
    for one revision, and a mutation that unhooked the fidelity check from the verdict survived
    the whole suite -- the predicates were tested and the wiring between them was not.
    """
    text, cov = extract(data)
    decoded = text.decode("utf-8", "replace")
    return decoded, *verdict(cov, concerns=fidelity(decoded))


def selftest():
    """Fixtures over the predicates. Built by hand so each one names a real failure."""
    def flate(payload):
        return b"x 0 obj<</Filter/FlateDecode>>stream\n" + zlib.compress(payload) + b"\nendstream"

    cases = []
    # -- unescape --
    cases.append(("octal escape becomes its byte", unescape(rb"A\101B") == b"AAB"))
    cases.append(("named escape becomes its byte", unescape(rb"a\nb") == b"a\nb"))
    cases.append(("escaped paren survives", unescape(rb"f\(x\)") == b"f(x)"))
    cases.append(("unknown escape drops the backslash", unescape(rb"a\qb") == b"ab"))
    # -- show: literal vs hex accounting --
    t, l, h = show(b"[(Chap)22.5 (t)9.5 (er 6)]TJ")
    cases.append(("kerned array rejoins into a word", t == b"Chapter 6"))
    cases.append(("literal bytes counted", l == 9))
    cases.append(("no hex bytes claimed when there are none", h == 0))
    t, l, h = show(b"[<002C>30 <003B00490045>10 ]TJ")
    cases.append(("hex-only run yields no text", t == b""))
    cases.append(("hex bytes are COUNTED though undecodable", (l, h) == (0, 8)))
    t, l, h = show(b"[(Mix)10 <0049004B>]TJ")
    cases.append(("mixed run counts both sides", (t, l, h) == (b"Mix", 3, 4)))
    t, _, _ = show(b"(a) Tj TD (b) Tj")
    cases.append(("TD breaks the line", t == b"a\nb"))
    _, l, h = show(b"<004A> Tj")
    cases.append(("a bare hex Tj is counted, not ignored", (l, h) == (0, 2)))
    # -- streams --
    cases.append(("a flate stream round-trips", list(streams(flate(b"(hi) Tj"))) == [b"(hi) Tj"]))
    # The payload here is VALID zlib. Without the filter guard it would decompress happily and
    # its bytes would be read as text, so this is the only fixture that can catch the guard's
    # removal - a fixture with junk bytes passes either way, because zlib raises regardless.
    cases.append(("a non-flate stream is skipped even when its bytes WOULD decompress",
                  list(streams(b"x<</Filter/DCTDecode>>stream\n"
                               + zlib.compress(b"(leak) Tj") + b"\nendstream")) == []))
    cases.append(("junk in a flate stream is dropped, not raised",
                  list(streams(b"x<</Filter/FlateDecode>>stream\nJUNK\nendstream")) == []))
    cases.append(("corrupt flate data does not raise",
                  list(streams(b"x<</Filter/FlateDecode>>stream\nNOTZLIB\nendstream")) == []))
    # -- extract + verdict --
    _, cov = extract(flate(b"[(all literal)]TJ"))
    cases.append(("all-literal PDF reports full coverage", cov == 1.0))
    _, cov = extract(flate(b"[(abcd)]TJ [<00410042>]TJ"))
    cases.append(("half-hex PDF reports half coverage", abs(cov - 0.5) < 1e-9))
    _, cov = extract(flate(b"[(ab)]TJ [<00410042>]TJ"))
    cases.append(("hex is counted in BYTES, so 2 chars vs 2 codes is one third, not half",
                  abs(cov - 2 / 6) < 1e-9))
    _, cov = extract(flate(b"0 0 100 100 re f"))
    cases.append(("a PDF with no text reports None, not zero", cov is None))
    cases.append(("full coverage is READABLE", verdict(1.0)[0] == "READABLE"))
    cases.append(("quarter coverage is REFUSED", verdict(0.254)[0] == "REFUSED"))
    cases.append(("no text is NO-TEXT, distinct from REFUSED", verdict(None)[0] == "NO-TEXT"))
    cases.append(("the floor is exclusive of nothing - at the floor it passes",
                  verdict(COVERAGE_FLOOR)[0] == "READABLE"))
    cases.append(("just under the floor is refused",
                  verdict(COVERAGE_FLOOR - 1e-9)[0] == "REFUSED"))
    # -- kerning becomes word spaces: the regression that shipped and had to be fixed --
    t, _, _ = show(b"[(word)-200(next)]TJ")
    cases.append(("a wide kern becomes a space", t == b"word next"))
    t, _, _ = show(b"[(Chap)22.5(t)9.5(er)]TJ")
    cases.append(("letter-fit kerning does NOT become a space", t == b"Chapter"))
    t, _, _ = show(b"[(a)-140(b)]TJ")
    cases.append(("the threshold itself counts as a space", t == b"a b"))
    t, _, _ = show(b"[(a)-139.9(b)]TJ")
    cases.append(("just inside the threshold does not", t == b"ab"))
    t, _, _ = show(b"[(a)-300<0041>-300(b)]TJ")
    cases.append(("kerns around an UNDECODABLE hex run still space it", t == b"a  b"))
    # -- fidelity: what coverage cannot see --
    cases.append(("run-together text is a concern", fidelity("ab" * 200) != []))
    cases.append(("normal prose is not", fidelity("the cat sat on the mat " * 40) == []))
    cases.append(("a short string is not judged at all - too little to measure",
                  fidelity("abcdefghij") == []))
    cases.append(("full coverage PLUS a concern is SUSPECT, not READABLE",
                  verdict(1.0, concerns=["run together"])[0] == "SUSPECT"))
    cases.append(("full coverage with no concern is READABLE",
                  verdict(1.0, concerns=[])[0] == "READABLE"))
    cases.append(("a concern does not rescue low coverage - still REFUSED",
                  verdict(0.18, concerns=[])[0] == "REFUSED"))
    cases.append(("READABLE no longer promises an exact quote",
                  "quote" in verdict(1.0)[1] and "loosely" in verdict(1.0)[1]))
    # -- the wiring, end to end over real PDF bytes: coverage AND fidelity must both reach the tag --
    prose = b" ".join(b"[(the cat sat on the mat)]TJ" for _ in range(40))
    cases.append(("a whole readable PDF reports READABLE",
                  report(b"%PDF-1.4" + flate(prose))[1] == "READABLE"))
    runon = b"".join(b"[(abcdefghij)]TJ" for _ in range(40))
    cases.append(("a whole run-together PDF reports SUSPECT, so fidelity IS wired in",
                  report(b"%PDF-1.4" + flate(runon))[1] == "SUSPECT"))
    cases.append(("a whole hex-heavy PDF reports REFUSED, so coverage IS wired in",
                  report(b"%PDF-1.4" + flate(b"[(ab)]TJ[<" + b"0041" * 40 + b">]TJ"))[1]
                  == "REFUSED"))
    # -- main() itself, because the line that PRINTS the text lived outside every fixture above
    # and referred to a name that no longer existed. The suite was 40 green while the tool's
    # primary output path raised NameError on every real file. --
    import contextlib
    import io as _io
    import tempfile

    def run_main(body, *flags):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as fh:
            fh.write(b"%PDF-1.4" + flate(body))
            name = fh.name
        out, err = _io.StringIO(), _io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["pdftext", name, *flags])
        return code, out.getvalue(), err.getvalue()

    code, out, _ = run_main(b" ".join(b"[(the cat sat on the mat)]TJ" for _ in range(40)))
    cases.append(("main PRINTS the text of a readable PDF", "the cat sat on the mat" in out))
    cases.append(("and exits 0", code == 0))
    code, out, err = run_main(b"[(ab)]TJ[<" + b"0041" * 40 + b">]TJ")
    cases.append(("main prints NO text for a refused PDF", out == ""))
    cases.append(("and says why, on stderr, and exits 1", "REFUSED" in err and code == 1))
    # -- not every Flate stream is page content, and the tool used to scan all of them --
    cases.append(("an image XObject is skipped by its dictionary",
                  list(streams(b"x<</Subtype/Image/Filter/FlateDecode>>stream\n"
                               + zlib.compress(b"(leak) Tj") + b"\nendstream")) == []))
    cases.append(("an embedded font program is skipped by /Length1",
                  list(streams(b"x<</Length1 900/Filter/FlateDecode>>stream\n"
                               + zlib.compress(b"(leak) Tj") + b"\nendstream")) == []))
    # The catch-all, and the regression for a real hang: arXiv 2605.17193 carries an OpenType font
    # stream that is neither an image nor marked /Length1 here. Scanning its bytes as operators
    # backtracked for minutes. It must be rejected on the BYTES, with no dictionary hint at all.
    font = b"\x00\x01\x00\x00\x00\x13\x01\x00\x00\x04\x000GDEF\x08\xcb\x11_" * 80
    cases.append(("a binary blob with NO dictionary marker is skipped on its bytes",
                  list(streams(b"x<</Filter/FlateDecode>>stream\n"
                               + zlib.compress(font) + b"\nendstream")) == []))
    cases.append(("is_content accepts real operators", is_content(b"BT /F1 12 Tf (hi) Tj ET")))
    cases.append(("is_content rejects binary", not is_content(font)))
    cases.append(("is_content rejects an empty stream", not is_content(b"")))
    cases.append(("is_content tolerates a little binary in real content",
                  is_content(b"BT (caf\xe9 and more plain ascii operators here) Tj ET" * 20)))
    t0 = time.time()
    list(streams(b"x<</Filter/FlateDecode>>stream\n" + zlib.compress(font * 40) + b"\nendstream"))
    cases.append(("and it does so FAST - the hang is the bug being tested",
                  time.time() - t0 < 1.0))

    bad = [n for n, ok in cases if not ok]
    for n, ok in cases:
        print(f"  {'ok  ' if ok else 'FAIL'} {n}")
    print(f"\n{'PASS' if not bad else 'FAIL'} — pdftext predicate, {len(cases)} fixtures")
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[-3].strip(), file=sys.stderr)
        return 2
    path = argv[1]
    with open(path, "rb") as fh:
        data = fh.read()
    if not data.startswith(b"%PDF-"):
        print(f"{path}: not a PDF (no %PDF- header)", file=sys.stderr)
        return 2
    decoded, tag, why = report(data)
    if "--coverage" in argv or tag != "READABLE":
        print(f"{path}\n  {tag}: {why}", file=sys.stderr)
        return 0 if tag == "READABLE" else 1
    sys.stdout.write(decoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
