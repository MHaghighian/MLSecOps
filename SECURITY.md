# Security Policy

## Reporting a vulnerability

If you discover a security issue **in this repository** (exposed credentials, malicious content in a chapter, or a vulnerability in a documentation build script), please **do not** open a public issue with exploit details.

Instead:

1. Open a [GitHub Security Advisory](https://github.com/l4tr0d3ctism/MLSecOps/security/advisories/new) (preferred), or  
2. Contact the maintainer through a private channel with impact and reproduction steps.

We will acknowledge reports within a reasonable timeframe and coordinate disclosure.

## Scope

This policy covers the **MLSecOps Guide repository** — Markdown content, release assets, and any GitHub Actions workflows in this repo.

It does **not** cover:

- Third-party tools or vendors mentioned in the guide  
- AI systems, models, or APIs you deploy using the guide  

For vulnerabilities in **your** production AI systems, maintain your own disclosure policy (see Chapter 11).

## Supported versions

| Version | Supported |
|---------|-----------|
| v1.1.0 | Yes |
| v1.0.x | Yes — security fixes only; use v1.1.0 for current content |

Older draft tags may not receive updates.

## Reader template (optional)

Organizations may adapt this outline for model/API disclosure:

```text
Contact: security@example.com
Policy: https://example.com/.well-known/security.txt
Scope: Production inference APIs and published model artifacts
Out of scope: Third-party tools listed in the guide (report to vendors directly)
```
