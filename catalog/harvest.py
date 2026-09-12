#!/usr/bin/env python3
"""Harvest ALL reusable components (skills, agents, hooks, commands) from
superpowers + ECC into one unified, component-type-aware catalog with a
security scan. Mirror dirs are ignored; bundled sub-components are noted on
their parent skill, not as separate entries."""
import json
import re
from pathlib import Path
from collections import Counter

SP = Path("/home/user/obra/superpowers")
ECC = Path("/home/user/affaan-m/ECC")

# directories that are mirrors / generated / vendored -> never a canonical source
IGNORE_PARTS = {'.cursor', '.kiro', '.codex', '.opencode', '.git', 'docs',
                'legacy-command-shims', 'node_modules', 'tests', 'ecc2'}

def ignored(p: Path) -> bool:
    return any(part in IGNORE_PARTS for part in p.parts)

NET_RE = re.compile(r'\b(curl|wget|fetch\(|urllib|requests\.(get|post)|axios|\bnc\b|netcat|socket\.)|https?://(?!code\.claude|docs\.claude|platform\.claude|agentskills|github\.com)', re.I)
SECRET_RE = re.compile(r'(API[_-]?KEY|SECRET|PASSWORD|BEARER|AWS_|PRIVATE[_-]?KEY|ssh-rsa)', re.I)
EXEC_RE = re.compile(r'(rm\s+-rf|sudo |eval\s|os\.system|subprocess|child_process|base64\s+-d|chmod\s+\+x)', re.I)

def parse_fm(text):
    if not text.startswith('---'):
        return {}
    end = text.find('\n---', 3)
    if end == -1:
        return {}
    fm, out = text[3:end], {}
    m = re.search(r'^name:\s*(.+)$', fm, re.M)
    if m: out['name'] = m.group(1).strip().strip('"\'')
    m = re.search(r'^description:\s*(.*?)(?=^\w[\w-]*:\s|\Z)', fm, re.M | re.S)
    if m:
        d = re.sub(r'^[>|][-+]?\s*', '', m.group(1).strip())
        out['description'] = ' '.join(l.strip() for l in d.splitlines()).strip().strip('"\'')[:400]
    return out

def scan(paths):
    flags = set()
    for f in paths:
        if f.is_file() and f.suffix in ('.md', '.py', '.sh', '.js', '.ts', '.json', ''):
            try: t = f.read_text(errors='ignore')
            except Exception: continue
            if NET_RE.search(t): flags.add('network')
            if SECRET_RE.search(t): flags.add('secret-ref')
            if EXEC_RE.search(t): flags.add('exec')
    return sorted(flags)

catalog = {}  # (type,key) -> entry ; first-seen wins, later mirrors appended to also_in

def add(ctype, name, d: Path, repo, desc, extra=None):
    key = (ctype, name.lower())
    if key in catalog:
        catalog[key]['also_in'].append(str(d).replace('/home/user/', ''))
        return
    files = [p for p in d.rglob('*') if p.is_file()] if d.is_dir() else [d]
    fnames = [str(p.relative_to(d)) for p in files] if d.is_dir() else [d.name]
    e = {
        'type': ctype, 'name': name, 'repo': repo,
        'source_path': str(d).replace('/home/user/', ''),
        'description': (desc or '')[:400],
        'files': len(files),
        'has_scripts': any(f.endswith(('.py', '.sh', '.js', '.ts')) for f in fnames),
        'bundles': sorted({sub for sub in ('agents', 'hooks', 'commands')
                           if d.is_dir() and (d / sub).is_dir()}),
        'security_flags': scan(files),
        'also_in': [], 'status': 'cataloged', 'decision': 'pending', 'test': 'untested',
    }
    if extra: e.update(extra)
    catalog[key] = e

# ---- SKILLS ----
for base, repo in [(SP / 'skills', 'superpowers'),
                   (ECC / 'skills', 'ecc'), (ECC / '.agents/skills', 'ecc')]:
    if not base.exists(): continue
    for sm in sorted(base.glob('*/SKILL.md')):
        if ignored(sm): continue
        fm = parse_fm(sm.read_text(errors='ignore'))
        add('skill', fm.get('name', sm.parent.name), sm.parent, repo, fm.get('description', ''))

# ---- STANDALONE AGENTS (top-level agents/ only; skill-bundled agents are noted via 'bundles') ----
for base, repo in [(ECC / 'agents', 'ecc')]:
    if not base.exists(): continue
    for am in sorted(base.rglob('*.md')):
        if ignored(am): continue
        fm = parse_fm(am.read_text(errors='ignore'))
        add('agent', fm.get('name', am.stem), am, repo, fm.get('description', ''))

# ---- STANDALONE COMMANDS (top-level commands/, excluding shims/mirrors) ----
for base, repo in [(ECC / 'commands', 'ecc'), (ECC / '.claude/commands', 'ecc')]:
    if not base.exists(): continue
    for cm in sorted(base.rglob('*.md')):
        if ignored(cm): continue
        fm = parse_fm(cm.read_text(errors='ignore'))
        add('command', fm.get('name', cm.stem), cm, repo, fm.get('description', ''))

# ---- HOOKS (top-level hooks/ dirs; represent each repo's hook set) ----
for base, repo in [(SP / 'hooks', 'superpowers'), (ECC / 'hooks', 'ecc')]:
    if not base.exists(): continue
    for hj in sorted(base.rglob('*')):
        if hj.is_file() and hj.name in ('hooks.json',) and not ignored(hj):
            add('hook', f"{repo}:{hj.parent.name}", hj.parent, repo, f"hook config {hj.relative_to(base.parent)}")
    # also individual hook scripts at top of hooks/
    for hs in sorted(base.glob('*')):
        if hs.is_file() and hs.suffix in ('.py', '.sh', '.js', '.ts') and not ignored(hs):
            add('hook', f"{repo}:{hs.stem}", hs, repo, f"hook script {hs.name}")

entries = sorted(catalog.values(), key=lambda e: (e['type'], e['repo'], e['name'].lower()))
out = {'generated': '2026-08-27', 'total': len(entries), 'entries': entries}
Path('/tmp/claude-0/-home-user-hello-world/166da4b5-1b2a-5916-b4ac-2e347fa567c1/scratchpad/catalog.json').write_text(json.dumps(out, indent=2))

by_type = Counter(e['type'] for e in entries)
by_repo = Counter(e['repo'] for e in entries)
flagged = [e for e in entries if e['security_flags']]
print(f"TOTAL unique components: {len(entries)}")
print(f"by type: {dict(by_type)}")
print(f"by repo: {dict(by_repo)}")
print(f"security-flagged: {len(flagged)}  (network={sum('network' in e['security_flags'] for e in entries)}, secret-ref={sum('secret-ref' in e['security_flags'] for e in entries)}, exec={sum('exec' in e['security_flags'] for e in entries)})")
print(f"skills bundling sub-agents/hooks: {sum(1 for e in entries if e['type']=='skill' and e['bundles'])}")
print(f"missing description: {sum(not e['description'] for e in entries)}")
