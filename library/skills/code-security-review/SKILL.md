---
name: code-security-review
description: "Use when reviewing SOURCE CODE for security vulnerabilities before running, shipping, or adopting it — a diff, a file, a module, or a whole repo. Traces untrusted input to dangerous sinks and checks the standard vulnerability classes: injection (SQL/command/template/LDAP), unsafe deserialization, path traversal, SSRF, hardcoded secrets, unsafe eval/exec, XSS, insecure crypto, and authn/authz gaps. Read-only, severity-ranked, cites file:line. Distinct from agent-surface-security-audit (an agent's config/instruction surface) and llm-redteam-scan (a running LLM app's behavior) — this reviews the CODE itself."
---

# code-security-review — find vulnerabilities in source code

Review code for the ways it can be exploited, before it runs or ships. A method (SAST-style
by reading, not by running a scanner): follow untrusted input to where it can do damage, and
check each vulnerability class along the way. Read-only — auditing must never be riskier than
the code audited.

## When to use
- Before running/adopting third-party code, before shipping generated code, or on a diff.
- Complements: `agent-surface-security-audit` (config/hooks/allowlists), `llm-redteam-scan`
  (LLM app behavior). This one is the traditional code-vulnerability pass.

**When NOT to use:** auditing an agent's config surface (use `agent-surface-security-audit`),
or probing a deployed model's behavior (use `llm-redteam-scan`).

## Method
1. **Map the attack surface.** List the entry points where untrusted input enters — HTTP
   params/bodies/headers, CLI args, file contents, env, message queues, DB reads, third-party
   API responses. These are the sources.
2. **Trace each source to a sink.** Follow tainted data to dangerous operations and check the
   class at each sink (below). Untrusted-reaching-a-sink without validation/escaping is the bug.
3. **Classify + severity.** Rank each finding CRITICAL / HIGH / MEDIUM / LOW by exploitability
   × impact, cite `file:line`, and give the concrete exploit path (input → sink → effect).
4. **Report, don't fix.** List findings with a suggested remediation each; do not auto-edit.

## Vulnerability classes to check (at each sink)
- **Injection** — SQL/NoSQL (string-built queries vs parameterized), OS command
  (`exec`/`system`/`subprocess shell=True` with tainted args), template/SSTI, LDAP, XPath.
- **Unsafe deserialization** — `pickle`/`yaml.load`/`Marshal`/native `readObject` on untrusted data.
- **Path traversal / file** — user-controlled paths joined without normalization + allowlist;
  arbitrary file read/write/include; zip-slip.
- **SSRF** — server-side fetch of a user-supplied URL without host allowlisting.
- **Secrets** — hardcoded keys/tokens/passwords/connection strings in source or history
  (report file:line + TYPE, never the value).
- **Unsafe dynamic exec** — `eval`/`exec`/`Function()`/`system` on data influenced by input.
- **XSS / output encoding** — untrusted data rendered to HTML/JS without escaping; `dangerouslySetInnerHTML`.
- **Crypto misuse** — home-rolled crypto, ECB, static IV/nonce, weak hashes for passwords
  (MD5/SHA1, no salt/KDF), `Math.random` for tokens, disabled TLS verification.
- **Authn/authz** — missing access checks on an endpoint/action, IDOR (object id from input
  with no ownership check), auth bypass, trusting client-supplied role/identity.
- **Other high-signal** — race/TOCTOU on security decisions, open redirect, mass assignment,
  regex catastrophic backtracking (ReDoS) on untrusted input.

## Rules
- **Read-only.** Use only Read/Grep/Glob (and a project's own SAST/lint if the user runs it) —
  never install or run an external scanner yourself, never auto-edit, never auto-commit.
- **No secret values.** Report location + type; never print or log a secret's value.
- **Exploit path or it's noise.** Every finding names input → sink → effect; if you can't
  articulate the path, mark it a hardening note, not a vulnerability.
- **Severity honestly.** Don't inflate; a theoretical issue behind auth is not CRITICAL.
- **Fail loud on unread code.** Code you couldn't read is unreviewed — say so; don't imply it's clean.

## In this repo (one instance)
The factory harvests METHODS and does not run third-party code, so the adopt-gate leans on
`agent-surface-security-audit`; use this talent when a wave must actually read a harvested
repo's source for vulnerabilities, or to review code the AI-app-builder generates before it ships.
