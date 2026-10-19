# Contributing to MLSecOps Practical Reference Guide

Thank you for helping improve an open **practical reference** for AI security across the lifecycle.

## Before you start

- Read [README.md](README.md) and [GETTING-STARTED.md](GETTING-STARTED.md)  
- Check [CHANGELOG.md](CHANGELOG.md) — current release is **v1.2.1**  
- Prefer fixes, mappings, traceability, case studies, and Appendix E improvements over new chapters unless discussed in an issue  

## How to contribute

### Report an issue

1. Search [existing issues](https://github.com/MHaghighian/MLSecOps/issues)  
2. Open an issue with: chapter, section, expected vs actual  
3. For ideas, use [Discussions](https://github.com/MHaghighian/MLSecOps/discussions)  

### Submit a pull request

1. Fork the repository  
2. Branch: `fix/chapter-6-typo` or `docs/readme-clarity`  
3. Edit Markdown under `chapters-en/` (or project docs at repo root)  
4. Keep PRs focused — one topic per PR when possible  
5. Reference chapter and source for factual claims  
6. Run the local checks below before opening the PR  

## Local checks (documentation “tests”)

This repository is primarily a Markdown handbook. Continuous checks verify that the documentation site still builds.

```bash
python -m pip install -r requirements-pages.txt
python .github/prepare_pages.py
mkdocs build --strict
```

GitHub Actions runs the same MkDocs build on pull requests and on `main` (see `.github/workflows/docs-check.yml`).

Optional (Word export):

```bash
python -m pip install -r scripts/requirements-docx.txt
python scripts/build-docx.py
```

## Content guidelines

### Writing style

- Clear, professional English  
- Match existing terminology: **control points**, **release decisions**, **Evidence Pack**  
- Cite frameworks (OWASP, MITRE ATLAS, NIST) for factual mappings  
- Mark illustrative patterns vs documented incidents (see Chapter 13)  

### Format

- Markdown only for chapter content  
- Diagrams: edit `assets/diagrams/source/*.mmd` (and the matching ` ```mermaid ` fence in the chapter), export PNG to `assets/diagrams/`; chapters keep both Mermaid + `![](../assets/diagrams/…png)` so GitHub/Word stay reliable if Mermaid fails to render
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
3. CI docs build must pass  
4. Merge when aligned with the current release scope  

## Security issues in this repo

See [SECURITY.md](SECURITY.md) — do not file public issues for credential leaks or exploit details.

## License

By contributing, you agree your contributions are licensed under [CC BY-SA 4.0](LICENSE).

## Questions?

[Open a discussion](https://github.com/MHaghighian/MLSecOps/discussions) or an issue.
