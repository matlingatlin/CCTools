---
title: The preview and sandbox boundary - iframe sandboxing, frame-ancestors, and a sandbox egress firewall with live policy updates, as fetched 2026-09-09
sources:
  - url: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe
    note: "The sandbox attribute: empty value applies all restrictions; the allow-* tokens; the allow-scripts + allow-same-origin warning; credentialless, csp and allow attributes."
    fetched: 2026-09-09
  - url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
    note: "What frame-ancestors controls; 'none'; not supported in a meta element."
    fetched: 2026-09-09
  - url: https://vercel.com/docs/sandbox/concepts/firewall
    note: "last_updated 2026-08-31 in the page's front matter. Three modes, live updates, user-defined allowlists, the stated limits, credentials brokering, request proxying, Postgres over TLS only."
    fetched: 2026-09-09
status: verified
tags: [security, sandbox, iframe, csp, egress, firewall, preview, exfiltration, scio]
related: ["[[claude-agent-sdk-hosting-and-limits-2026-09]]", "[[otel-genai-semantic-conventions-2026-09]]", "[[supabase-row-level-security-2026-09]]"]
---
# The preview and sandbox boundary, as of 2026-09-09

Why this note exists: Scio renders model-written application code in a preview and runs it in
a sandbox. Its predecessor rendered the preview in two iframes with no `sandbox` attribute
inside its own origin (a verified-still-true finding) and had no network policy. ADR-0025 rests
on the facts below, read from the primary pages on the date given.

## Claims

| # | Claim | Source | Verbatim / value | Verdict |
|---|---|---|---|---|
| 1 | An empty `sandbox` applies every restriction; tokens lift them one by one | MDN iframe | "The value of the attribute can either be empty to apply all restrictions, or space-separated tokens to lift particular restrictions" | MEASURED (fetched 2026-09-09) |
| 2 | Without `allow-same-origin` the frame is an opaque origin | MDN iframe | "If this token is not used, the resource is treated as being from a special origin that always fails the same-origin policy" | MEASURED |
| 3 | `allow-scripts` with `allow-same-origin` on a same-origin document defeats the sandbox | MDN iframe | "it is strongly discouraged to use both `allow-scripts` and `allow-same-origin`, as that lets the embedded document remove the `sandbox` attribute — making it no more secure than not using the `sandbox` attribute at all" | MEASURED |
| 4 | The other tokens | MDN iframe | `allow-forms`, `allow-modals`, `allow-popups`, `allow-popups-to-escape-sandbox`, `allow-top-navigation`, `allow-top-navigation-by-user-activation`, `allow-downloads`, `allow-pointer-lock`, `allow-orientation-lock`, `allow-presentation`, `allow-storage-access-by-user-activation`, `allow-top-navigation-to-custom-protocols` | MEASURED |
| 5 | `credentialless` and `csp` attributes exist | MDN iframe | credentialless: "loaded in a new, ephemeral context. It doesn't have access to the network, cookies, and storage data associated with its origin"; csp: "A Content Security Policy enforced for the embedded resource" | MEASURED (browser support not checked here) |
| 6 | `frame-ancestors` names who may embed a page; header only | MDN CSP | "specifies valid parents that may embed a page using <frame>, <iframe>, <object>, or <embed>"; `'none'`: "This resource may not be embedded"; "This directive is not supported in the <meta> element" | MEASURED |
| 7 | A sandbox egress firewall with three modes and a deny-by-default allowlist exists as a product | Vercel firewall | `allow-all` (default), `deny-all` ("Denies all outbound network access, including DNS"), user-defined ("deny traffic by default and let you allow specific destinations") | MEASURED (page last_updated 2026-08-31) |
| 8 | Policies change on a running sandbox | Vercel firewall | "three distinct modes, which can be updated at runtime, without restarting the process"; use case "Start with Internet access, get required data, lock access and start untrusted process" | MEASURED |
| 9 | The limits, stated by the vendor | Vercel firewall | HTTPS matched "using the SNI"; "Plain-text HTTP cannot be filtered by domain"; domain fronting possible because "the firewall does not prevent the mismatch by default"; "`subnets.allow` leaves DNS unrestricted"; "An empty policy behaves as `deny-all`"; "Broad ranges override domain scoping" | MEASURED |
| 10 | Credentials brokering keeps the secret outside the sandbox | Vercel firewall | "Credentials brokering injects credentials into egressing traffic. The secrets never enter the sandbox"; "Matchers select requests for transformation. They never block a request." | MEASURED |
| 11 | Request proxying is the only way to restrict a domain to paths, and it carries an OIDC token | Vercel firewall | "Forwarding is also how you restrict a domain to specific paths"; headers `vercel-forwarded-host`, `vercel-sandbox-oidc-token` with `aud` = the `forwardURL` | MEASURED |
| 12 | Postgres through the firewall needs TLS; brokering does not apply to it | Vercel firewall | "TLS is required. Clients must connect with `sslmode=require` or stricter"; "Credentials brokering and other request transformations are not supported on Postgres connections" | MEASURED |

## What it means here

- **The preview never shares Scio's origin.** With claim 3, the only safe shape for a preview
  that must run scripts is a *different* origin (a per-tenant-app host) inside an iframe with
  `sandbox="allow-scripts allow-forms"` and no `allow-same-origin`; the Scio pages that embed it
  carry `frame-ancestors 'none'` themselves (claim 6) so nobody embeds Scio.
- **Two-phase egress is a product pattern, not an invention** (claims 7–8): install with the
  registry allowed, then narrow to the verification database and the app's own origin before
  generated code runs. The vendor's own limits (claim 9) say what the allowlist is *not*: a
  determined adversary with DNS or an allowed API's free-form fields still has a channel.
- **Credentials never enter the sandbox** (claim 10): Scio's env allow-list
  (`packages/platform/src/adapters/env.ts`, `sandboxEnv`) already omits the provider key; brokering is
  how an app that needs a credential gets one at the edge. Postgres is the exception (claim 12),
  which is why the verification database gets a scoped, short-lived role rather than a brokered
  header.
- The Agent SDK's own isolation settings are in [[claude-agent-sdk-hosting-and-limits-2026-09]];
  the telemetry that must never carry the preview's content is in
  [[otel-genai-semantic-conventions-2026-09]].
- The database side of the same boundary - which rows the generated app's browser key may read
  once it is inside - is [[supabase-row-level-security-2026-09]].
