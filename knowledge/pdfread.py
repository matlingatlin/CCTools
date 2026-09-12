#!/usr/bin/env python3
"""Read a held PDF with a real PDF library, using nothing this container did not already have.

WHY THIS EXISTS. `knowledge/pdftext.py` is the stdlib reader with a coverage guard, and it is
what CI runs, because it needs no virtualenv and no wheel. It also refuses three of the nine
held PDFs: they are CID-encoded, and decoding them means parsing ToUnicode CMaps, which is
writing a PDF library. On 2026-09-12 those three were read anyway, and the whole capability
turned out to be sitting in the container the entire time:

  - the system `pypdf` is 6.17.0, present and current;
  - it panics on import because the SYSTEM `cryptography` reaches a Rust binding that needs an
    absent `_cffi_backend`, and the failure arrives as a `PanicException`, not an `ImportError`,
    so pypdf's own fallback never fires;
  - in a virtualenv with `include-system-site-packages = false` there is nothing poisoned to
    reach, and THE SAME VERSION reads every held PDF.

Three verification passes and one skill-surface measurement leaned on that, and the venv lived
in `/tmp`, so nothing in this repo could reproduce any of it. This file is that reproduction.

ZERO NETWORK, ZERO PACKAGE MANAGER, and that is the point rather than a nicety. The reader is
not downloaded: `python3 -m venv` makes an empty isolated environment and the already-present
system `pypdf` is COPIED into it. Nothing is fetched, nothing is installed, the fourth gate has
nothing to weigh, and the recipe works with the network off. If it ever needs a wheel, it has
stopped being this tool.

Read-only, and the raw layer is never edited: the reader opens a held file and this script
refuses a path outside `knowledge/raw/`.

  python3 knowledge/pdfread.py --selftest            # pure predicates, no venv, no I/O
  python3 knowledge/pdfread.py --build              # make the reader (idempotent)
  python3 knowledge/pdfread.py <path-under-raw>     # print the text
  python3 knowledge/pdfread.py --report             # every held PDF: pages, chars, reader

The VENV BUILD is deliberately not in `kb-check.yml` - it is filesystem work and no gate depends
on it; `pdftext.py`'s 52 fixtures are the PDF gate. The PREDICATES below do run there, because
they are offline and free and one of them is a path check, and a predicate with no CI is a
predicate that rots.
"""
import os, pathlib, re, shutil, subprocess, sys, sysconfig

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = "knowledge/raw/"
DEFAULT_VENV = pathlib.Path(os.environ.get("KB_PDF_VENV") or
                            (pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "kb-pdfreader"))


def site_packages(prefix, version=None):
    """Where a venv at `prefix` keeps its packages. Pure, so a fixture can pin the shape.

    Written from `sysconfig` rather than hard-coded, because `python3.11` is this container's
    version and not a property of the method. Windows keeps them at `Lib/site-packages` with no
    version segment, which is why the separator is not assumed.
    """
    version = version or f"{sys.version_info.major}.{sys.version_info.minor}"
    if os.name == "nt":
        return pathlib.Path(prefix) / "Lib" / "site-packages"
    return pathlib.Path(prefix) / "lib" / f"python{version}" / "site-packages"


def under_raw(path, raw=RAW):
    """Is this a path inside the raw layer? The reader opens held bytes and nothing else.

    Answered on the NORMALISED path, so `knowledge/raw/../../etc/passwd` is not inside the raw
    layer merely because it starts with the prefix. A prefix test on the string as typed is the
    classic way this check passes something it should not.

    Normalisation is the WHOLE check, and that is a measured claim rather than a preference. The
    first version also rejected any path containing `..`, and a mutation run found both clauses
    survived independently - each caught every fixture on its own. Worked through: after
    `normpath`, a `..` can only remain when it is leading, and a leading `..` cannot start with
    the prefix, so the second clause was UNREACHABLE. It was also wrong in the other direction,
    rejecting `knowledge/raw/a/../x.pdf`, which resolves inside the layer and is a legitimate way
    to name a held file. Deleted rather than kept as belt-and-braces: a clause that cannot fire is
    not a defence, and one that rejects a valid path is a bug wearing a defence's clothes. Both
    directions now have a fixture.
    """
    p = os.path.normpath(str(path)).replace(os.sep, "/")
    return p.startswith(raw)


def needs_build(venv_dir, exists=None):
    """Does the reader have to be built? Pure: takes the answer to "is the interpreter there?".

    Separated from the filesystem so the decision is testable, which is the lesson this repo
    learned the hard way - a predicate with no fixture is where the defect hides.
    """
    interp = pathlib.Path(venv_dir) / ("Scripts" if os.name == "nt" else "bin") / "python"
    if exists is None:
        exists = interp.exists()
    return (not exists), interp


def system_pypdf():
    """The system copy to clone, found WITHOUT importing it - importing is what panics.

    `importlib.util.find_spec` also imports parent packages, so it is not safe here either; the
    directory is located from the interpreter's own purelib/platlib paths. Returns None when the
    package genuinely is not there, which is a different answer from "it raises", and confusing
    the two is what cost this repo a day.
    """
    for key in ("purelib", "platlib"):
        d = pathlib.Path(sysconfig.get_paths()[key]) / "pypdf"
        if (d / "__init__.py").exists():
            return d
    for p in map(pathlib.Path, sys.path):
        if (p / "pypdf" / "__init__.py").exists():
            return p / "pypdf"
    return None


def build(venv_dir=DEFAULT_VENV):
    must, interp = needs_build(venv_dir)
    if not must:
        return interp
    src = system_pypdf()
    if src is None:
        sys.exit("no system pypdf to copy: this tool clones what is here, it never downloads")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True,
                   stdout=subprocess.DEVNULL)
    dest = site_packages(venv_dir)
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest / "pypdf", dirs_exist_ok=True)
    for meta in src.parent.glob("pypdf-*.dist-info"):
        shutil.copytree(meta, dest / meta.name, dirs_exist_ok=True)
    return interp


READ = r'''
import sys, pypdf
r = pypdf.PdfReader(sys.argv[1])
pages = [p.extract_text() or "" for p in r.pages]
sys.stderr.write("pypdf %s | %d pages | %d chars\n"
                 % (pypdf.__version__, len(pages), len("".join(pages))))
sys.stdout.write("\n".join(pages))
'''


def read(path, venv_dir=DEFAULT_VENV):
    """Text of a held PDF, plus a one-line provenance stamp on stderr.

    The page join is `"\\n".join(...)`, and the stamp counts the CONCATENATION, so the two
    numbers this repo has quoted for one document (35,733 and 35,765) cannot drift apart again
    without someone saying which they meant: 33 pages joined by a newline is 32 characters more
    than the same pages concatenated, and that is the entire difference.
    """
    if not under_raw(path):
        sys.exit(f"{path} is not under {RAW} - this reader opens held bytes only")
    interp = build(venv_dir)
    r = subprocess.run([str(interp), "-c", READ, str(ROOT / path)], capture_output=True, text=True)
    sys.stderr.write(r.stderr)
    if r.returncode:
        sys.exit(r.returncode)
    return r.stdout


def selftest():
    sp = site_packages("/v", "3.11")
    sp_ok = (sp.as_posix() == "/v/lib/python3.11/site-packages") if os.name != "nt" else True
    raw_ok = under_raw("knowledge/raw/dir/x.pdf")
    raw_no = not under_raw("pipeline/x.pdf")
    # the traversal a plain startswith() would wave through
    raw_esc = not under_raw("knowledge/raw/../../etc/passwd")
    raw_dot = not under_raw("knowledge/raw/a/../../../x.pdf")
    # an absolute path is outside the layer however it is spelled
    raw_abs = not under_raw("/etc/passwd") and not under_raw("/home/user/knowledge/raw/x.pdf")
    # and the other direction, which the deleted ".." clause got wrong: a path that RESOLVES
    # inside the layer is allowed, even though it contains a parent segment on the way.
    raw_ok2 = under_raw("knowledge/raw/a/../dir/x.pdf")
    must, interp = needs_build("/v", exists=False)
    have, _ = needs_build("/v", exists=True)
    build_ok = must and not have and interp.as_posix().endswith("/v/bin/python")
    ok = (sp_ok and raw_ok and raw_no and raw_esc and raw_dot and raw_abs
          and raw_ok2 and build_ok)
    print(f"pdfread selftest: site-packages shape={sp_ok} under-raw yes={raw_ok} no={raw_no} "
          f"traversal-refused={raw_esc and raw_dot} absolute-refused={raw_abs} "
          f"resolves-inside-allowed={raw_ok2} build-decision={build_ok}")
    print("PASS — pdfread predicates, 10 fixtures" if ok else "FAIL")
    return 0 if ok else 1


def report():
    interp = build()
    rows = sorted(pathlib.Path(ROOT / RAW).rglob("*.pdf"))
    print(f"{len(rows)} held PDF(s), read with the cloned system pypdf\n")
    for f in rows:
        rel = f.relative_to(ROOT).as_posix()
        r = subprocess.run([str(interp), "-c", READ, str(f)], capture_output=True, text=True)
        stamp = (r.stderr.strip().splitlines() or ["(no output)"])[-1]
        print(f"  {rel}\n      {stamp}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
    elif a[0] == "--selftest":
        sys.exit(selftest())
    elif a[0] == "--build":
        print(f"reader at {build()}")
    elif a[0] == "--report":
        report()
    else:
        sys.stdout.write(read(a[0]))
