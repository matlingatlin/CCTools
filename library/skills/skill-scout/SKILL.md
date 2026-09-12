---
name: skill-scout
description: "Use when the user wants to find, discover, or fork an existing skill — searches local, marketplace, GitHub, and web sources before any new skill is created. Discovery step, not authoring, editing, or auditing skills. NOT for finding duplicate FUNCTIONS in code (use semantic-duplicate-sweep) -- this searches the skill library. NOT deriving the library-wide job-to-owner routing table for units that already exist (use capability-routing-table)."
metadata:
  origin: community
---

# Skill Scout

Use this skill before creating a new skill. The goal is to avoid duplicating
existing community or marketplace work, while still vetting anything external
before adoption.

Source: salvaged from stale community PR #1232 by `redminwang`.

## When to Use

- The user says "create a skill", "build a skill", "make a skill", or "new
  skill".
- The user asks "is there a skill for X?" or "does a skill exist that does Y?"
- The user describes a workflow and you are about to suggest creating a new
  skill.
- The user wants to fork or extend an existing skill.

If the user explicitly says to skip search or create from scratch, acknowledge
that and proceed with the requested creation workflow.

## How It Works

### Step 1 - Capture Intent

Extract:

- The task the skill should perform.
- The trigger conditions for using it.
- The domain, tools, frameworks, or data sources involved.
- Three to five search keywords plus useful synonyms.

### Step 2 - Search Local Sources

Search installed and marketplace skill names first. Local sources are preferred
because they are already part of the user's environment.

```bash
# PROJECT scope FIRST — a repo's own skills live here and are the likeliest match
find .claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null | grep -iE "keyword|synonym"
# then user + marketplace scope
find ~/.claude/skills -maxdepth 2 -name SKILL.md 2>/dev/null | grep -iE "keyword|synonym"
find ~/.claude/plugins/marketplaces -path '*/skills/*/SKILL.md' 2>/dev/null | grep -iE "keyword|synonym"
```

Then search frontmatter descriptions across ALL THREE scopes:

```bash
grep -RilE "keyword|synonym" .claude/skills ~/.claude/skills ~/.claude/plugins/marketplaces 2>/dev/null
```

**Search the project scope or the dedup gate runs blind.** Omitting `.claude/skills`
is a silent failure, not an error: the searches return zero, "nothing exists" looks
proven, and a duplicate gets built. Verified 2026-08-28 in a repo whose 65 skills are
all project-scoped — a keyword returning 4 project matches returned 0 without it.

### Step 3 - Search Remote Sources

Use available GitHub and web search tools. Prefer concise queries:

```bash
gh search repos "claude code skill keyword" --limit 10 --sort stars
gh search code "name: keyword" --filename SKILL.md --limit 10
```

For web search, use at most three targeted queries such as:

```text
"claude code skill" keyword
"SKILL.md" keyword
"everything-claude-code" keyword
```

### Step 4 - Vet External Matches

Before recommending any external skill for adoption or forking:

- Read the `SKILL.md` frontmatter and instructions.
- Look for unexpected shell commands, file writes, network calls, credential
  handling, or package installs.
- Check whether the repository appears maintained.
- Prefer copying into a fresh local branch and reviewing the diff over editing
  marketplace originals.

### Step 5 - Rank Results

Rank candidates by:

1. Exact keyword match in the skill name.
2. Keyword or synonym match in description.
3. Local installed or marketplace source.
4. Maintained GitHub source with recent activity.
5. Web-only mention.

Cap the final list at 10 results.

### Step 6 - Present Decision Options

Give the user a short table:

| Option | Meaning |
| --- | --- |
| Use existing | Invoke or install a matching skill as-is. |
| Fork or extend | Copy the closest skill and modify it. |
| Create fresh | Build a new skill after confirming no close match exists. |

Only create a new skill after the user chooses that path or after the search
finds no close match.

## Examples

### Result Table

```markdown
| # | Skill | Source | Why it matches | Gap |
| --- | --- | --- | --- | --- |
| 1 | article-writing | Local ECC | Drafts articles and guides | Not focused on release notes |
| 2 | content-engine | Local ECC | Multi-format content workflow | Heavier than needed |
| 3 | blog-writer | GitHub | Blog writing skill with recent commits | Needs security review |
```

### User-Facing Summary

```markdown
I found two close local matches and one external candidate. The closest fit is
`article-writing`; it covers drafting and revision, but it does not include the
release-note checklist you asked for. I can either use it as-is, fork it into a
release-note variant, or create a fresh skill.
```

## Anti-Patterns

- Do not jump directly to new skill creation when a search is reasonable.
- Do not install external skills without reading them first.
- Do not present a long unranked list of weak matches.
- Do not treat web-only mentions as trusted sources.
- Do not edit installed marketplace originals in place.

## Related

- `skill-stocktake` - Audit installed skills for health, duplicates, and gaps.
