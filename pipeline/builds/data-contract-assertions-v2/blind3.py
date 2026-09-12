#!/usr/bin/env python3
"""6.1b - blind the arm outputs BEFORE the expectation set is written.

Per item the three arms are relabelled from a fresh shuffled alphabet and written in
the shuffled order, so a label carries no information across items and reading three
items does not let anyone learn the mapping. The key is written to a file the author
does not open until the grading is in.
"""
import json, random, sys
from pathlib import Path
S = Path("/tmp/claude-0/-home-user/bd691cfa-0047-5b03-b405-d90749bf0624/scratchpad")
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
KEY = Path(sys.argv[2])
rng = random.Random(int(sys.argv[3]))
arms = ["with", "without", "incumbent"]
key = {}
for item in ["E1", "E2", "E3", "E4"]:
    labels = ["A", "B", "C"]; rng.shuffle(labels)
    order = list(arms); rng.shuffle(order)
    for arm, lab in zip(order, labels):
        src = S / "arms3" / f"{item}.{arm}.out"
        if not src.is_file():
            print(f"MISSING {src}"); continue
        (OUT / f"{item}-{lab}.md").write_text(src.read_text())
        key[f"{item}-{lab}"] = arm
KEY.write_text(json.dumps(key, indent=1, sort_keys=True) + "\n")
print(f"blinded {len(key)} answers into {OUT}; key withheld at {KEY}")
