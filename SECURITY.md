# Security Policy

## Reporting a vulnerability

If you discover a security issue **in this repository** (exposed credentials, malicious content in a chapter, or a vulnerability in a documentation build script), please **do not** open a public issue with exploit details.

**Preferred reporting channels (in order):**

1. [GitHub Private Vulnerability Reporting](https://github.com/MHaghighian/MLSecOps/security/advisories/new) (Security Advisories) — preferred  
2. Contact the repository owner privately via the email listed on [mhsec.me](https://mhsec.me) or the GitHub profile for [MHaghighian](https://github.com/MHaghighian), with impact and reproduction steps

### Response targets (coordinated vulnerability disclosure)

| Step | Target |
|------|--------|
| Acknowledge receipt | Within **7 days** |
| Initial assessment / triage | Within **14 days** |
| Fix or public advisory (when applicable) | Coordinated with reporter; timeline depends on severity |

We follow **coordinated disclosure**. Please give us a reasonable window before public discussion of exploit details.

## Public disclosure of vulnerabilities

Confirmed vulnerabilities in **this repository** are published via:

- [GitHub Security Advisories](https://github.com/MHaghighian/MLSecOps/security/advisories) (public advisory when disclosure is agreed), and/or  
- Notes in [CHANGELOG.md](CHANGELOG.md) / the relevant GitHub Release  

There are no published advisories to date if the Advisories list is empty — that means none have been confirmed for public release yet, not that reporting is closed.

## Scope

This policy covers the **MLSecOps Guide repository** — Markdown content, release assets, documentation build scripts, and GitHub Actions workflows in this repo.

It does **not** cover:

- Third-party tools or vendors mentioned in the guide  
- AI systems, models, or APIs you deploy using the guide  

For vulnerabilities in **your** production AI systems, maintain your own disclosure policy (see Chapter 11).

## Security assessment (this repository)

Most likely / impactful issues for **this docs project** (not reader deployments):

| Risk | Impact | Mitigation |
|------|--------|------------|
| Malicious or misleading content in chapters | Reader harm / reputational | PR review, citations, CI docs build |
| Compromised GitHub account or Actions secrets | Site defacement, secret leak | Owner-only admin; secrets in Actions only; MFA on GitHub |
| Supply-chain issue in MkDocs/pip tooling | Bad site build | Pinned requirement ranges; Dependabot; review Dependabot PRs |
| Leaked credentials in git history | Unauthorized access | No secrets in repo; rotate if exposed ([GOVERNANCE.md](GOVERNANCE.md)) |

Deeper product threat modeling for AI systems is the subject of the guide itself (e.g. Chapters 2–3, 6–8), not a runtime service in this repository. System actors: [DESIGN.md](DESIGN.md).

## Secrets and credentials

- **Do not** commit API keys, tokens, private keys, or `.env` files.  
- CI secrets (if any) live only in **GitHub Actions secrets** / environments.  
- Rotate any credential that may have been exposed; open a private advisory if impact is unclear.  
- Collaborators are not given secrets access by default ([GOVERNANCE.md](GOVERNANCE.md)).

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

Older draft tags may not receive updates; when a line is no longer supported, that is stated here and in release notes.

## Reader template (optional)

Organizations may adapt this outline for model/API disclosure:

```text
Contact: security@example.com
Policy: https://example.com/.well-known/security.txt
Scope: Production inference APIs and published model artifacts
Out of scope: Third-party tools listed in the guide (report to vendors directly)
```
