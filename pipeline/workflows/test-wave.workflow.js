// The loop's TEST step, run via the factory fan-out muscle: for each talent, one agent
// AUTHORS specific tests for that talent, runs eval-harness baseline-vs-with-talent on them,
// persists them as .claude/skills/<name>/evals.md, and returns a verdict. Writes no git
// history beyond the evals.md drafts — the coordinator commits + marks the catalog as a
// separate loop step. Driven by args = { talents: [name, ...] }.
export const meta = {
  name: 'test-wave',
  description: 'Loop TEST step: author SPECIFIC tests per talent + run eval-harness baseline-vs-with, persist evals.md, return passed/fix/drop. Coordinator commits results separately.',
  phases: [
    { title: 'Test', detail: 'per talent: author specific scenarios, run baseline-vs-with, write evals.md, verdict' },
  ],
}

const REPO = '/home/user/skills-repo'
const A = (typeof args === 'object' && args) ? args : {}
const TALENTS = Array.isArray(A.talents) ? A.talents : []

phase('Test')
const results = await parallel(TALENTS.map((name) => () => agent(
  `Test the talent "${name}" the way our eval-harness prescribes — a REAL functional test, not a style review.\n\n0. Read ${REPO}/templates/EVALS.template.md (the test scaffold + its EVOLVING CHECKLIST) and ${REPO}/pipeline/TEST-AUTHORING-LESSONS.md (ACTIVE DIRECTIVES) FIRST, and apply both — this is how tests get fairer and cleverer over time. Write evals.md following that template's shape.\n1. LOCATE the unit, then read it. A SKILL lives at ${REPO}/.claude/skills/${name}/SKILL.md; an AGENT lives at ${REPO}/.claude/agents/${name}.md. Check both — a runner that only looked in .claude/skills made every agent invisible. Read it to understand exactly what it claims to do and when it should trigger.\n2. AUTHOR SPECIFIC TESTS for THIS talent — a BLEND of 4-6 scenarios tailored to its function: ~half NORMAL/REPRESENTATIVE (the everyday job it should do well — does it handle the common case?) and ~half CLEVER/ADVERSARIAL (traps, planted defects it should catch, edge/boundary), plus at least one NEGATIVE-TRIGGER (a look-alike where it should NOT fire). Not only traps and not only happy-path — both, all specific to this talent. For the clever ones, design so the WITHOUT-talent baseline plausibly FAILS (those prove it earns its place); normal ones confirm everyday behavior. If a discipline talent, use pressure scenarios; if a technique talent, application scenarios. State, per scenario, the input and the observable pass criterion.\n3. RUN baseline-vs-with: for each scenario, reason through the likely output WITHOUT the talent (baseline) vs WITH the talent's method applied, and judge whether the talent produces a materially better, criterion-meeting result. Be adversarial and honest — do not rubber-stamp.\n4. WRITE the scenarios + results BESIDE the unit you read in step 1 — ${REPO}/.claude/skills/${name}/evals.md for a skill, ${REPO}/.claude/agents/${name}.evals.md for an agent (a durable regression test: list each scenario, its pass criterion, and baseline vs with-talent outcome).\n5. VERDICT: "passed" only if the talent clearly beats baseline on its own tests; "fix" if it helps but has a gap (say what); "drop" if it does not beat baseline (say why).\n\nReturn the verdict, a one-line justification, how many scenarios passed / total, and any fix needed.`,
  { label: `test:${name}`, phase: 'Test', schema: { type: 'object', properties: { name: { type: 'string' }, verdict: { type: 'string', enum: ['passed', 'fix', 'drop'] }, scenarios_passed: { type: 'number' }, scenarios_total: { type: 'number' }, justification: { type: 'string' }, fix_needed: { type: 'string' } }, required: ['name', 'verdict', 'scenarios_total', 'justification'] } }
)))

return { tested: results.filter(Boolean) }
