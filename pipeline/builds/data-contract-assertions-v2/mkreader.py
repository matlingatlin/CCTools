#!/usr/bin/env python3
"""Build the exact directory a phase's reader is allowed to see, from the chain
contract's declared `inputs`. Both directions: nothing missing, nothing extra."""
import json, shutil, sys
from pathlib import Path
A = Path("/home/user/skills-repo/pipeline/builds/data-contract-assertions-v2/artifact/data-contract-assertions")
R = Path("/home/user/skills-repo/pipeline/builds/data-contract-assertions-v2/readers")
CHAIN = json.loads(Path("/home/user/skills-repo/pipeline/contracts/chain.contract.json").read_text())
phase = sys.argv[1]
inputs = None
for p in CHAIN["phases"]:
    if p["id"] == phase:
        inputs = p.get("inputs")
if inputs is None:
    print(f"phase {phase} declares no inputs"); sys.exit(2)
d = R / f"r{phase}" / "data-contract-assertions"
if d.parent.exists(): shutil.rmtree(d.parent)
d.mkdir(parents=True)
for tok in inputs:
    if tok == "skill_md":
        shutil.copy2(A / "SKILL.md", d / "SKILL.md")
    elif tok in ("references", "assets", "evals"):
        src = A / tok
        if src.is_dir(): shutil.copytree(src, d / tok)
print(json.dumps({"dir": str(d), "inputs": inputs}))
