# Security Policy

## Reporting a vulnerability

If you discover a security issue **in this repository** (exposed credentials, malicious content in a chapter, or a vulnerability in a documentation build script), please **do not** open a public issue with exploit details.

**Preferred reporting channels (in order):**

1. [GitHub Private Vulnerability Reporting](https://github.com/MHaghighian/MLSecOps/security/advisories/new) (Security Advisories) — preferred  
2. Contact the repository owner privately via the email listed on [mhsec.me](https://mhsec.me) or the GitHub profile for [MHaghighian](https://github.com/MHaghighian), with impact and reproduction steps

### Response targets

| Step | Target |
|------|--------|
| Acknowledge receipt | Within **7 days** |
| Initial assessment / triage | Within **14 days** |
| Fix or public advisory (when applicable) | Coordinated with reporter; timeline depends on severity |

We follow **coordinated disclosure**. Please give us a reasonable window before public discussion of exploit details.

## Scope

This policy covers the **MLSecOps Guide repository** — Markdown content, release assets, documentation build scripts, and GitHub Actions workflows in this repo.

It does **not** cover:

- Third-party tools or vendors mentioned in the guide  
- AI systems, models, or APIs you deploy using the guide  

For vulnerabilities in **your** production AI systems, maintain your own disclosure policy (see Chapter 11).

## Supported versions

| Version | Supported |
|---------|-----------|
| v1.2.1 | Yes |
| v1.2.0 | Yes — security fixes only; use v1.2.1 for current content |
| v1.1.3 | Yes — security fixes only; use v1.2.1 for current content |
| v1.1.2 | Yes — security fixes only; use v1.2.1 for current content |
| v1.1.1 | Yes — security fixes only; use v1.2.1 for current content |
| v1.1.0 | Yes — security fixes only; use v1.2.1 for current content |
| v1.0.x | Yes — security fixes only; use v1.2.1 for current content |

Older draft tags may not receive updates.

## Reader template (optional)

Organizations may adapt this outline for model/API disclosure:

```text
Contact: security@example.com
Policy: https://example.com/.well-known/security.txt
Scope: Production inference APIs and published model artifacts
Out of scope: Third-party tools listed in the guide (report to vendors directly)
```
