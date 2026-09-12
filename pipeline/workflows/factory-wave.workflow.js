// The LOOP's (/piano's) wave composition — it sequences the loop's own stages (scout,
// harvest, build) and uses parallel fan-out (the `factory` muscle) within them. It RETURNS
// all results and writes NO git history: building here is the loop's build STEP, and the
// coordinator does the commit and talent-deploy as a SEPARATE loop step afterward. `factory`
// the skill is the generic fan-out engine; this file is one caller's composition of it.
export const meta = {
  name: 'factory-wave',
  description: 'The /piano loop wave: scout emits sources, harvest fans out over queued sources, build fans out over the candidates harvest surfaced (author -> verify). Driven by args = {scout, harvest, build}. Returns results only — the coordinator commits + deploys as a separate loop step.',
  phases: [
    { title: 'Scout', detail: 'research-scout emits N new sources' },
    { title: 'Harvest', detail: 'one agent per queued source: clone + inventory + candidate extraction' },
    { title: 'Build', detail: 'one author agent per candidate (loop build step, run via fan-out)' },
    { title: 'Verify', detail: 'QUALITY check per built talent (frontmatter/description/method/safety) — NOT the functional eval; eval-harness runs as a separate loop TEST step' },
  ],
}

const REPO = '/home/user/skills-repo'
const A = (typeof args === 'object' && args) ? args : {}
const SCOUT_N = (A.scout === undefined || A.scout === null) ? 6 : A.scout
const HARVEST = Array.isArray(A.harvest) ? A.harvest : []
const BUILD = Array.isArray(A.build) ? A.build : []

const CONV = `AUTHORING CONVENTIONS (dogfood writing-skills): frontmatter MUST have name (kebab-case = directory) + description. description = trigger-first ("Use when…"), third person, keyword-rich, concrete triggers, NON-overlapping with existing talents, under 1536 chars. Body = one-line what/why -> "When to use" (+ when NOT) -> numbered Steps (a real repeatable procedure) -> Rules. No filler, NO external network/CLI calls, NO auto-run hooks (security gate). Method only. ~40-80 lines.`

// --- Scout (producer): emits sources to keep the queue full (skipped when scout=0) ---
let scoutP = Promise.resolve(null)
if (SCOUT_N > 0) {
  phase('Scout')
  scoutP = agent(
    `You are research-scout for a self-improving talent factory (core: AI/ML/LLMs, agents/orchestration, software eng, data, IT, tooling, NLP, prompt engineering; bonus only if it yields a talent). Emit ${SCOUT_N} NEW high-signal SOURCES likely to yield reusable TALENTS or METHODS (not vertical app skills). LESSONS: awesome-lists/web-top-n yield ~0 (skip); vendor/reference repos yield knowledge not talents; the richest sources are single-purpose frameworks and practitioner repos/profiles + recent arXiv methods. For each: type (github|papers|profile), ref, why (expected talent/method). Avoid anything obviously already covered by a mature factory.`,
    { label: 'scout', phase: 'Scout', schema: { type: 'object', properties: { sources: { type: 'array', items: { type: 'object', properties: { type: { type: 'string' }, ref: { type: 'string' }, why: { type: 'string' } }, required: ['type', 'ref', 'why'] } } }, required: ['sources'] } }
  )
}

// --- Harvest: one agent per queued source (clone + inventory + candidate extraction) ---
let harvested = []
if (HARVEST.length) {
  phase('Harvest')
  harvested = await parallel(HARVEST.map((s) => () => agent(
    `Harvest the source ${s.ref} (type ${s.type || 'github'}). If a github repo: git clone --depth 1 https://github.com/${s.ref} into /home/user/${s.ref} (skip if present), then inventory talent surfaces (SKILL.md, agents/, hooks/, commands/) and read the README to judge what METHODS or reusable talents it offers. Apply talent-worthiness (a function we LACK, not a vertical app skill) and note any security concerns (external installs, auto-run hooks, network/creds). Return: what it is, talent-surface counts, and 0-3 candidate talents worth BUILDING (name + one-line brief) or "none".`,
    { label: `harvest:${s.ref}`, phase: 'Harvest', schema: { type: 'object', properties: { ref: { type: 'string' }, summary: { type: 'string' }, candidates: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, brief: { type: 'string' } }, required: ['name', 'brief'] } } }, required: ['ref', 'summary', 'candidates'] } }
  )))
  harvested = harvested.filter(Boolean)
}

// --- Build is the LAST step: it consumes the candidates HARVEST surfaced (plus any passed
//     explicitly in args.build), so a single wave flows scout -> harvest -> build -> verify.
//     One author agent per candidate, then a per-talent verify (pipeline, no barrier). ---
const harvestedCandidates = harvested.flatMap((h) => (h && Array.isArray(h.candidates)) ? h.candidates : [])
const seen = new Set()
const BUILD_ALL = [...BUILD, ...harvestedCandidates].filter((t) => {
  const k = (t.name || '').toLowerCase()
  if (!k || seen.has(k)) return false
  seen.add(k); return true
})

let built = []
if (BUILD_ALL.length) {
  built = await pipeline(
    BUILD_ALL,
    (t) => agent(
      `Author a Claude Code skill (talent). WRITE the complete file to ${REPO}/.claude/skills/${t.name}/SKILL.md (create the dir).\n\nTALENT: ${t.name} — ${t.brief}\n\n${CONV}\n\nReuse-first: make the description NON-overlapping with a mature factory's existing talents. Return ONLY the description line you wrote and the line count.`,
      { label: `build:${t.name}`, phase: 'Build', schema: { type: 'object', properties: { name: { type: 'string' }, description: { type: 'string' }, lines: { type: 'number' } }, required: ['name', 'description', 'lines'] } }
    ),
    (authored, t) => agent(
      `Read ${REPO}/.claude/skills/${t.name}/SKILL.md and audit it. (1) SAFETY: no external CLI/npm/curl/pip installs, no auto-run hooks, no network/credential calls, no obfuscation (security gate). (2) QUALITY: valid frontmatter (name+description), trigger-first non-overlapping description, method-driven body with real steps + rules, no filler. (3) SCOPE: matches "${t.brief}". Return a verdict (ship|fix|reject).`,
      { label: `verify:${t.name}`, phase: 'Verify', schema: { type: 'object', properties: { name: { type: 'string' }, safe: { type: 'boolean' }, quality_ok: { type: 'boolean' }, verdict: { type: 'string', enum: ['ship', 'fix', 'reject'] }, issues: { type: 'array', items: { type: 'string' } } }, required: ['name', 'safe', 'quality_ok', 'verdict'] } }
    )
  )
  built = built.filter(Boolean)
}

const scout = await scoutP
// Everything is RETURNED for the coordinator to land in ONE common commit — the workflow
// writes no git history itself. Build ran last; harvest fed it.
return { scout, harvested, built }
