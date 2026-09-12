#!/usr/bin/env python3
"""The one way a build dispatches a run.

Every build before this one dispatched its runs from shell written that day
- ten scripts in build 3 alone - and every contamination that build suffered
lived there: a working directory shared between runs, so a later run read an
earlier run's answer; the arm's name in the directory path, so six of twelve
answers carried it into the text the blinding relabelled; and the method
directory mounted for every arm, so the bare baseline read the skill's
evidence. None was visible to a gate. All three cost a full wave of arm runs.

This module exists so those cannot recur, and so the cost row is complete:
the same ad hoc scripts never captured the usage payload, which is why a
build's cost clauses had no tokens to judge against.

    from dispatch import dispatch, dispatch_many

    r = dispatch(root=build_dir, phase="6.1", label="arm.E1.r1", arm="with",
                 prompt=open("prompts/E1.txt").read(), tier="opus",
                 add_dirs=[fixture_dir], method_dir=method_dir)

A run gets: an isolated working directory whose name carries no arm string;
read access to the listed directories; the method directory ONLY when the arm
is `with`; and a cost row with tokens, tool calls, tier and window. What it
wrote comes back with an `arm_leak` flag if its own text names the arm.

Exit codes are not the interface; the returned dict is. `ok` is False when the
run failed, timed out, or reported no usage - never when the answer was wrong.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import record as rec  # noqa: E402

REPO = Path(__file__).resolve().parents[2]

ARMS = {"with", "without", "incumbent"}
# Model aliases the CLI accepts, kept here so a build never types a tier twice.
TIERS = {"opus": "claude-opus-5", "sonnet": "claude-sonnet-5", "haiku": "claude-haiku-4-5-20251001"}
RUN_TIMEOUT_S = 900
# What a with-arm may see of the skill under test. evals/ is deliberately absent.
METHOD_VIEW = ("SKILL.md", "references", "assets", "scripts")

# Words a run's output must not contain if the blinding is to mean anything.
# The three arm names, and the two words builds have used for the incumbent.
_LEAK = re.compile(r"\b(with|without|incumbent|baseline|bare)[-_.]?(arm|out|run)?\b", re.I)


def _cwd_name(label: str) -> str:
    """A directory name that says NOTHING about which arm this is.

    Hash of the label plus a fresh nonce: two dispatches of the same label
    never share a directory, and the arm cannot be read off the path.
    """
    h = hashlib.sha256(f"{label}:{secrets.token_hex(8)}".encode()).hexdigest()[:12]
    return f"run-{h}"


def _read_only_runner(cmd: list[str], cwd: Path, timeout_s: int) -> tuple[int, str, str]:
    """Default runner: the real CLI. Replaced in tests."""
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout_s)
    return p.returncode, p.stdout, p.stderr


def dispatch(*, root: Path, phase: str, label: str, arm: str | None, prompt: str,
             tier: str = "opus", add_dirs: list[Path] | tuple[Path, ...] = (),
             method_dir: Path | None = None, inputs: list[Path] | tuple[Path, ...] = (),
             workspace: Path | None = None, timeout_s: int = RUN_TIMEOUT_S,
             note: str | None = None, effort: str | None = None, memo: bool = False,
             permission_mode: str = "acceptEdits",
             allowed_tools: tuple[str, ...] = ("Read", "Edit", "Write", "MultiEdit", "Glob", "Grep", "Bash"),
             _runner=_read_only_runner) -> dict:
    """Run one headless session under the isolation every arm run needs.

    arm         with / without / incumbent for a measured run, None otherwise
    add_dirs    directories the run may READ (fixtures). Never the method.
    method_dir  the skill under test. Mounted for arm == "with" ONLY; passing
                it for any other arm raises, because that is the third
                contamination and it must not be expressible.
    inputs      files copied INTO the run's directory (a reader's declared
                inputs). Copied, so the run cannot see siblings.
    effort      the CLI's --effort level for this run. The contract fixes the
                TIER of a protected run, not its effort; declare one effort per
                job class before the build and it is recorded on the row.
    permission_mode / allowed_tools
                a headless run cannot answer a permission prompt, so a run that
                must edit its own directory needs the edits pre-approved. Found
                by the first v3 build's probes (2026-09-02): six runs planned the
                right ingest and wrote nothing, every Write and Edit refused. The
                directory is fresh and isolated, which is what makes acceptEdits
                safe here; both are recorded on the row and in the memo key.
    memo        replay a run whose key - prompt, tier, arm, effort, model id,
                the bytes of every input and of the method - was dispatched
                before under this build root. An iterate round re-runs the same
                probes and the same without-arm on the same fixture; with memo
                those come back from disk, the cost row says cached=true, and
                nobody mistakes the replay for a measurement of load. Never for
                the with-arm of a changed artefact: the method bytes are in the
                key, so a changed skill misses by construction.
    """
    if arm is not None and arm not in ARMS:
        raise ValueError(f"arm must be one of {sorted(ARMS)} or None, got {arm!r}")
    if method_dir is not None and arm != "with":
        raise ValueError(
            f"method_dir given for arm {arm!r}. Only the with-arm may see the method; "
            f"mounting it for every arm is how a baseline came to cite the skill's own "
            f"evidence in build 3, and it cost a full wave of runs.")
    if tier not in TIERS:
        raise ValueError(f"tier must be one of {sorted(TIERS)}, got {tier!r}")

    ws = Path(workspace or (Path(root) / "runs"))
    ws.mkdir(parents=True, exist_ok=True)

    key = _memo_key(prompt, tier, arm, effort, inputs, method_dir, add_dirs,
                    extra=[permission_mode, list(allowed_tools)])
    memo_path = Path(root) / "memo" / f"{key}.json"
    if memo and memo_path.is_file():
        hit = json.loads(memo_path.read_text(encoding="utf-8"))
        t = time.time()
        row = rec.cost_row(root, phase=phase, label=label, started=t, ended=t,
                           tokens=hit["tokens"], tool_calls=hit["tool_calls"], tier=tier,
                           note=note or (f"arm={arm}" if arm else None),
                           extra={"cached": True, "memo_key": key,
                                  **({"effort": effort} if effort else {})})
        out_path = ws / f"{label}.md"
        out_path.write_text(hit["text"], encoding="utf-8")
        return {"ok": True, "status": "cached", "label": label, "arm": arm, "tier": tier,
                "model_served": hit.get("model_served", []), "cwd": None, "output": str(out_path),
                "tokens": hit["tokens"], "tool_calls": hit["tool_calls"], "duration_ms": 0,
                "duration_api_ms": None, "arm_leak": bool(arm) and bool(_LEAK.search(hit["text"])),
                "stderr_tail": "", "text": hit["text"], "cached": True, "memo_key": key}

    cwd = ws / _cwd_name(label)
    cwd.mkdir(parents=False, exist_ok=False)          # fresh by construction
    for src in inputs:
        src = Path(src)
        dst = cwd / src.name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    cmd = ["claude", "-p", prompt, "--model", TIERS[tier], "--output-format", "json"]
    if effort:
        cmd += ["--effort", effort]
    if permission_mode:
        cmd += ["--permission-mode", permission_mode]
    if allowed_tools:
        cmd += ["--allowedTools", ",".join(allowed_tools)]
    for d in add_dirs:
        cmd += ["--add-dir", str(Path(d).resolve())]
    if method_dir is not None:
        # Mount a VIEW of the method - SKILL.md and its bundled references,
        # assets and scripts - never its evals. The first v3 build mounted the
        # whole skill directory, so every with-arm could list and read the
        # fixture wiki and, in general, the answers its evals carry. The view is
        # a fresh directory named after the skill, so the prompt's "mounted at
        # the directory named <skill>" still holds.
        method_dir = Path(method_dir).resolve()
        view = ws / f"{_cwd_name(label)}-method" / method_dir.name
        view.mkdir(parents=True)
        for item in METHOD_VIEW:
            src = method_dir / item
            if src.is_file():
                shutil.copy2(src, view / item)
            elif src.is_dir():
                shutil.copytree(src, view / item)
        cmd += ["--add-dir", str(view)]

    # 4.0.0: the package's budget is enforced here, not remembered by the
    # coordinator. Counted from the cost ledger, so a killed or errored run
    # still counts - it was paid for.
    if phase == "6.1" and arm is not None:
        cap = None
        if (Path(root) / "record.json").exists():
            pk = (rec.header(root).get("package") or {})
            budget = pk.get("budget")
            if budget is None and pk.get("path") and Path(pk["path"]).exists():
                budget = json.loads(Path(pk["path"]).read_text(encoding="utf-8")).get("budget")
            cap = (budget or {}).get("max_paired_runs")
        if isinstance(cap, int):
            ledger = Path(root) / "cost" / "measured.jsonl"
            spent = sum(1 for l in ledger.read_text(encoding="utf-8").splitlines() if l.strip() and json.loads(l).get("phase") == "6.1") if ledger.exists() else 0
            if spent >= cap:
                raise rec.Refused(f"budget: {spent} paired run(s) already in the ledger against max_paired_runs={cap}; "
                                  f"refusing {label!r}. Raise the budget in the package, with a reason, or measure less.")

    started = time.time()
    status, stdout, stderr = "ok", "", ""
    try:
        rc, stdout, stderr = _runner(cmd, cwd, timeout_s)
    except subprocess.TimeoutExpired:
        rc, status = -1, "timeout"
    ended = time.time()

    payload: dict = {}
    if status == "ok":
        if rc != 0:
            status = "error"
        else:
            try:
                payload = json.loads(stdout)
            except json.JSONDecodeError:
                status = "unparseable"

    usage = payload.get("usage") or {}
    tokens = sum(v for k, v in usage.items() if k.endswith("tokens") and isinstance(v, int)) or None
    tool_calls = payload.get("num_turns")
    served = sorted((payload.get("modelUsage") or {}).keys())
    text = payload.get("result") or ""
    if status == "ok" and not tokens:
        status = "no_usage"

    # The blinding relabels files. It cannot relabel what a run wrote about
    # itself, so the check happens here, once, on every run.
    leak = bool(arm) and bool(_LEAK.search(text))

    row = rec.cost_row(root, phase=phase, label=label, started=started, ended=ended,
                       tokens=tokens, tool_calls=tool_calls, tier=tier,
                       note=note or (f"arm={arm}" if arm else None),
                       extra={**({"effort": effort} if effort else {}),
                              "permission_mode": permission_mode})
    out_path = ws / f"{label}.md"
    out_path.write_text(text, encoding="utf-8")
    if status == "ok":
        memo_path.parent.mkdir(parents=True, exist_ok=True)
        memo_path.write_text(json.dumps({"text": text, "tokens": tokens, "tool_calls": tool_calls,
                                         "model_served": served, "label": label,
                                         "written": rec.now()}), encoding="utf-8")

    return {"ok": status == "ok", "status": status, "label": label, "arm": arm,
            "tier": tier, "model_served": served, "cwd": str(cwd), "output": str(out_path),
            "tokens": tokens, "tool_calls": tool_calls,
            "duration_ms": row["duration_ms"], "duration_api_ms": payload.get("duration_api_ms"),
            "arm_leak": leak, "stderr_tail": stderr[-400:] if stderr else "",
            "text": text, "cached": False, "memo_key": key,
            "rate_limited": _rate_limited(status, stderr)}


def _hash_path(h, p: Path) -> None:
    p = Path(p)
    if p.is_dir():
        for f in sorted(x for x in p.rglob("*") if x.is_file()):
            h.update(str(f.relative_to(p)).encode()); h.update(f.read_bytes())
    elif p.is_file():
        h.update(p.name.encode()); h.update(p.read_bytes())


def _memo_key(prompt, tier, arm, effort, inputs, method_dir, add_dirs, extra=None) -> str:
    """Everything that could change the answer, hashed. Model id, not alias."""
    h = hashlib.sha256()
    h.update(json.dumps([prompt, TIERS[tier], arm, effort, extra]).encode())
    for p in inputs:
        _hash_path(h, p)
    if method_dir is not None:
        _hash_path(h, method_dir)
    for d in add_dirs:
        _hash_path(h, d)
    return h.hexdigest()[:24]


_RATE = re.compile(r"\b429\b|rate[ _-]?limit|too many requests|overloaded", re.I)


def _rate_limited(status: str, stderr: str) -> bool:
    return status == "error" and bool(_RATE.search(stderr or ""))


RATE_LIMIT_BACKOFF_S = (30, 60, 120, 240, 480)


def dispatch_many(jobs: list[dict], concurrency: int | None = None, *,
                  stagger_s: float = 0.0, max_rate_limit_retries: int = 5,
                  _sleep=time.sleep) -> list[dict]:
    """A refilling queue: a slot takes the next job the moment it frees.

    Dispatching in waves - all of a wave finishes before the next starts -
    was measured at 0.7 minutes over a build; this is the cheap end of the
    fixes. Concurrency defaults to W_MAX_AGENTS as pinned in CONSTANTS.md.

    stagger_s   every job after the first waits this long before launching, so
                the first run can open the shared prefix's cache entry before
                the rest ask for it. A cache entry exists only after the first
                response begins; eight runs launched at once all miss.
    rate limit  a run that failed with a 429 / rate-limit / overloaded error is
                retried after a backoff (30 s doubling to 8 min), at most
                max_rate_limit_retries times, and its cost row carries the
                retry count. W_MAX_AGENTS guards CPU contention; nothing before
                this guarded quota, and 196 of the 495 dispatched minutes across
                five builds were spent waiting on it.
    """
    if concurrency is None:
        concurrency = _w_max_agents()

    def one(idx_job):
        idx, j = idx_job
        if stagger_s and idx > 0:
            _sleep(stagger_s)
        tries = 0
        dead_retry = 0
        while True:
            r = dispatch(**j)
            # 4.0.0: a run that dies with no output and no stderr (seen once per
            # build since the first) is retried exactly once; the dead row stays
            # in the ledger with tokens null.
            if r.get("status") == "error" and not (r.get("stderr_tail") or "").strip() and r.get("tokens") is None and dead_retry < 1:
                dead_retry += 1
                r["dead_retry"] = dead_retry
                continue
            if not r.get("rate_limited") or tries >= max_rate_limit_retries:
                r["rate_limit_retries"] = tries
                r["dead_retries"] = dead_retry
                return r
            _sleep(RATE_LIMIT_BACKOFF_S[min(tries, len(RATE_LIMIT_BACKOFF_S) - 1)])
            tries += 1

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        return list(pool.map(one, list(enumerate(jobs))))


def _w_max_agents() -> int:
    txt = (REPO / "pipeline" / "CONSTANTS.md").read_text(encoding="utf-8")
    m = re.search(r"`W_MAX_AGENTS`\s*\|\s*\*\*(\d+)\*\*", txt)
    return int(m.group(1)) if m else 2


if __name__ == "__main__":
    print(__doc__)
