# Evals — code-security-review

> Durable regression test for the `code-security-review` talent. Follows
> `templates/EVALS.template.md`. Authored against `pipeline/CURATION-LESSONS.md`
> ACTIVE DIRECTIVES (blend normal + clever, observable criteria, clever ones
> designed so the baseline plausibly fails, technique talent → application
> scenarios, ≥1 negative-trigger).

**Talent:** `code-security-review` · **Type:** technique · **Last eval:** 2026-08-27 · **Verdict:** passed

## Method
Baseline-vs-with: for each scenario, judge the likely output WITHOUT the talent (a
competent-but-unaided read of the code) vs WITH its method applied (map sources →
trace to sinks → classify + severity + exploit path, report-don't-fix, no secret
values). A scenario passes only if the with-talent result is materially better and
meets the observable criterion. Adversarial and honest — no rubber-stamping.

## EVOLVING CHECKLIST (from CURATION-LESSONS)
- [x] **Mix, not only traps** — 2 normal/representative + 2 clever/adversarial + 1 negative-trigger.
- [x] **Specific to this talent** — every scenario is a concrete code snippet with a real vuln class (or a deliberate look-alike), not generic boilerplate.
- [x] **Observable pass/fail criterion** — each names the exact class, severity floor, and the input→sink→effect path a checker can verify against the snippet.
- [x] **Clever ones designed so baseline plausibly FAILS** — S3/S4 both present a *visible safety mechanism* (an allowlist check; an auth decorator) that an unaided read treats as sufficient.
- [x] **Technique talent → application scenarios** (not pressure).
- [x] **Negative trigger** — S5 is look-alike dangerous-looking-but-safe code; a pass is *not* raising a false-positive vuln.

## Scenarios

### S1 — SQL injection in a request handler · application (normal)
- **Input:** Review this Flask handler.
  ```python
  @app.get("/users")
  def users():
      name = request.args.get("name")
      q = f"SELECT * FROM users WHERE name = '{name}'"
      return db.execute(q).fetchall()
  ```
- **Pass criterion (observable):** Reports **SQL injection**, severity **CRITICAL or HIGH**, cites the `q = f"..."` / `db.execute(q)` line, states the path (attacker sets `?name=' OR '1'='1` → string-built query → full table read / auth bypass), and suggests a **parameterized query**. No auto-edit.
- **Baseline (without talent):** An unaided reviewer usually catches this obvious case too, but often stops at "use parameterized queries" without severity, cited line, or a concrete exploit string. May pass loosely.
- **With talent:** Source (`request.args`) → sink (`db.execute` of an f-string) is exactly the injection class; produces class + CRITICAL + `file:line` + exploit string + remediation, report-only.
- **Result:** pass (normal case; confirms the everyday job with full structure).

### S2 — Hardcoded secret + weak password hash · application (normal, tests the "no secret values" + crypto rules)
- **Input:** Review this module.
  ```python
  AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  def store(pw): return hashlib.md5(pw.encode()).hexdigest()
  ```
- **Pass criterion (observable):** (a) Reports a **hardcoded secret** by **TYPE + location** (AWS secret access key at that line) and **does NOT print the secret value** anywhere in the report. (b) Reports **weak password hashing** (MD5, unsalted, no KDF) as its own finding with remediation (bcrypt/argon2/scrypt). Two distinct findings, severity-ranked.
- **Baseline (without talent):** Likely flags "hardcoded key" and "md5 is weak" — but an unaided report commonly **echoes the secret value** to show what it found, and may treat MD5 as a vague nit rather than a password-storage finding.
- **With talent:** The explicit **No-secret-values** rule forces TYPE+location only; the crypto-misuse class names MD5-for-passwords specifically. Materially safer report.
- **Result:** pass (discriminates on the redaction discipline).

### S3 — SSRF behind a bypassable allowlist · trap (clever)
- **Input:** Review this fetch endpoint.
  ```python
  def proxy():
      url = request.args["url"]
      if "api.internal" in url:            # allowlist check
          return requests.get(url).content
      abort(403)
  ```
- **Pass criterion (observable):** Reports **SSRF** as an *exploitable* finding (severity HIGH+) **despite the presence of the check**, and names the bypass: substring match `"api.internal" in url` is satisfied by attacker-controlled hosts like `http://api.internal.evil.com` or `http://evil.com/?x=api.internal`, so the guard does not restrict the destination. Suggests host-allowlisting the parsed hostname against an exact set.
- **Baseline (without talent):** A visible `if "api.internal" in url` check reads as "there is validation here" — an unaided review plausibly concludes the URL is restricted and marks it safe, **missing** the SSRF. This is the discriminating failure.
- **With talent:** "Untrusted-reaching-a-sink *without validation*" forces asking whether the check actually constrains the sink; substring containment on a full URL provably doesn't → SSRF stands, with the bypass string as the exploit path.
- **Result:** pass (baseline plausibly fails; talent catches the illusory guard).

### S4 — IDOR: authenticated but no ownership check · trap (clever)
- **Input:** Review this endpoint.
  ```python
  @app.get("/invoices/<int:iid>")
  @login_required
  def invoice(iid):
      return Invoice.query.get(iid).as_json()
  ```
- **Pass criterion (observable):** Reports **broken object-level authorization / IDOR**, severity **HIGH+**, and states the path: `@login_required` proves *authentication* but nothing checks that `iid` belongs to `current_user`, so any logged-in user can enumerate `iid` and read **other users'** invoices. Remediation: filter by owner (`Invoice.query.filter_by(id=iid, user_id=current_user.id)`) / ownership assertion.
- **Baseline (without talent):** The `@login_required` decorator is a salient safety signal; an unaided read commonly concludes "the endpoint is protected" and moves on, conflating authn with authz — **missing** the IDOR. Discriminating failure.
- **With talent:** The authn/authz class explicitly lists "IDOR (object id from input with no ownership check)" and "trusting client-supplied identity," so the method separates *who are you* from *may you see this object* and flags the gap.
- **Result:** pass (baseline plausibly fails on the authn≠authz conflation).

### S5 — Dangerous-looking but safe code · negative-trigger
- **Input:** Review this module. (Reviewer is told "flag the vulnerabilities.")
  ```python
  BACKUP = ["/usr/bin/pg_dump", "-Fc", "app_db"]
  def backup(): subprocess.run(BACKUP, shell=False, check=True)   # no shell, no user input

  def find_user(uid: int):
      return db.execute("SELECT * FROM users WHERE id = %s", (uid,)).fetchall()  # parameterized
  ```
- **Pass criterion (observable):** Does **NOT** report SQL injection or command injection as vulnerabilities — there is no untrusted source reaching either sink (command is a constant list with `shell=False`; the query is parameterized). A pass is a clean "no exploitable findings" (at most a low hardening note that clearly is not labeled a vulnerability). A **false positive** ("possible command/SQL injection") is a fail.
- **Baseline (without talent):** Pattern-spotting on `subprocess.run(...)` and `db.execute("SELECT ...")` frequently triggers a reflexive "command injection / SQL injection risk" flag — an over-trigger, because the unaided read matches keywords rather than tracing a source.
- **With talent:** "**Exploit path or it's noise**" + source→sink tracing require an untrusted source; here there is none, so the method declines to raise a vuln (severity-honestly). Correctly quiet.
- **Result:** pass (guards against over-triggering / false positives).

## Failure triage (if any scenario failed)
No failures this pass. Triage rule retained: a red result is classified test-bug
(unfair/subjective/out-of-scope → fix the test) vs skill-bug (fair clever test the
talent misses → fix the talent; drop only if unfixable) before any fix/drop.

## Result summary
- Scenarios passed: **5/5** · failure_cause: **none** · verdict: **passed**
- Blend: 2 normal (S1, S2) + 2 clever traps (S3, S4) + 1 negative-trigger (S5).
- Discriminators (baseline plausibly fails): S3 (illusory allowlist), S4 (authn≠authz),
  and S2 on the redaction discipline (baseline tends to echo the secret value).
