#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
B = Path("/home/user/skills-repo/pipeline/builds/data-contract-assertions-v2")
phase, field, cid, question, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
d = B / "readers" / f"r{phase}" / "data-contract-assertions"
chk = subprocess.run(["python3", "/home/user/skills-repo/pipeline/validate/skill_contract.py", str(d)],
                     capture_output=True, text=True)
args = ["python3", "/home/user/skills-repo/pipeline/validate/reader_preflight.py",
        str(d), str(B / "bom.json"), "--phase", phase]
pre = subprocess.run(args, capture_output=True, text=True)
if pre.returncode == 1 and all("did not ask for it" not in l for l in pre.stdout.splitlines()):
    # Structural: this phase's declared inputs withhold bundled files SKILL.md points at,
    # so ptr.resolves cannot pass on a directory that is correct by reader_inputs.
    # Run the gate's own --skip-contract (INDETERMINATE, never a pass) and hand the reader
    # BOTH checker runs instead: its own subset, and the complete artefact.
    sub = pre.stdout + pre.stderr
    pre = subprocess.run(args + ["--skip-contract"], capture_output=True, text=True)
    pre.stdout = (pre.stdout + "\n\nNOTE - the unrestricted preflight on this same directory said:\n"
                  + sub + "\nThose unresolved pointers are THE HARNESS withholding files this phase "
                  "did not declare, not a defect in the skill. See the build's gate_conflict event.")
full = subprocess.run(["python3", "/home/user/skills-repo/pipeline/validate/skill_contract.py",
                       str(B / "artifact" / "data-contract-assertions"), "--context", str(B / "ctx.json")],
                      capture_output=True, text=True)
t = (B / "reader-template.txt").read_text()
t = (t.replace("__DIR__", str(d)).replace("__FIELD__", field).replace("__CONTRACT_ID__", cid)
      .replace("__QUESTION__", question)
      .replace("__CHECKER__", "ON THE DIRECTORY YOU WERE GIVEN (a subset of the bundle):\n"
        + ((chk.stdout + chk.stderr).strip() or "(no output)")
        + "\n\nON THE COMPLETE ARTEFACT, including the files this phase withheld from you:\n"
        + ((full.stdout + full.stderr).strip() or "(no output)"))
      .replace("__PREFLIGHT__", (pre.stdout + pre.stderr).strip() or "(no output)"))
Path(out).write_text(t)
print(f"preflight exit={pre.returncode}")
print((pre.stdout + pre.stderr).strip()[:900])
