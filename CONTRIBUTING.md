# Contributing to MLSecOps Practical Reference Guide

Thank you for helping improve an open **practical reference** for AI security across the lifecycle.

## Before you start

- Read [README.md](README.md) and [GETTING-STARTED.md](GETTING-STARTED.md)  
- Check [CHANGELOG.md](CHANGELOG.md) — current release is **v1.1.1**  
- **No new chapters** for v1.1 — prefer fixes, mappings, traceability, case studies, and Appendix E improvements  

## How to contribute

### Report an issue

1. Search [existing issues](https://github.com/l4tr0d3ctism/MLSecOps/issues)  
2. Open an issue with: chapter, section, expected vs actual  
3. For ideas, use [Discussions](https://github.com/l4tr0d3ctism/MLSecOps/discussions)  

### Submit a pull request

1. Fork the repository  
2. Branch: `fix/chapter-6-typo` or `docs/readme-clarity`  
3. Edit Markdown under `chapters-en/` (or project docs at repo root)  
4. Keep PRs focused — one topic per PR when possible  
5. Reference chapter and source for factual claims  

## Content guidelines

### Writing style

- Clear, professional English  
- Match existing terminology: **control points**, **release decisions**, **Evidence Pack**  
- Cite frameworks (OWASP, MITRE ATLAS, NIST) for factual mappings  
- Mark illustrative patterns vs documented incidents (see Chapter 13)  

### Format

- Markdown only for chapter content  
- Diagrams: edit `assets/diagrams/source/*.mmd`, export PNG to `assets/diagrams/`; chapters use `![](../assets/diagrams/…png)` (GitHub’s Mermaid viewer is unreliable for complex charts)
- Tables for mappings  
- Tool commands belong in [Ch.12 appendix](chapters-en/12-threat-control-tools-map.md#appendix-informative-tool-command-reference) — optional reading  
- End major sections with **`### References / Source mapping`** when adding factual controls or threat claims — see [Ch.15 traceability convention](chapters-en/15-conclusion-appendix.md#traceability-and-source-mapping-convention)

### Technical accuracy

- Do not add unverified tools or CVE claims without a primary source  
- Do not imply OWASP/OpenSSF/NIST endorsement of this guide  
- Templates in Appendix E are **informative** — state when adding examples  

## Review process

1. Maintainer review for accuracy and consistency  
2. Link check for internal references  
3. Merge when aligned with v1.1 scope  

## Security issues in this repo

See [SECURITY.md](SECURITY.md) — do not file public issues for credential leaks.

## License

By contributing, you agree your contributions are licensed under [CC BY-SA 4.0](LICENSE).

## Questions?

[Open a discussion](https://github.com/l4tr0d3ctism/MLSecOps/discussions) or an issue.

