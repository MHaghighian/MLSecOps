# Contributing to MLSecOps Reference Model & Practical Guide

Thank you for helping improve an open **practical reference** for AI security across the lifecycle.

## Before you start

- Read [README.md](README.md) and [GETTING-STARTED.md](GETTING-STARTED.md)  
- Check [CHANGELOG.md](CHANGELOG.md) — current release is **v1.5.0**  
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
6. Sign off every commit with the DCO (`git commit -s`) — see [DCO.md](DCO.md)  
7. Run the local checks below before opening the PR  

## Developer Certificate of Origin

All commits **must** include a `Signed-off-by` line. Details: [DCO.md](DCO.md).

## Dependencies (how we select, obtain, and track them)

This project is documentation-first. Direct language dependencies are minimal and declared in-repo:

| File | Purpose | How obtained | How tracked |
|------|---------|--------------|-------------|
| [requirements-pages.txt](requirements-pages.txt) | MkDocs site build (CI + local) | `pip install -r …` | Tracked in git; bump manually in PRs |
| [scripts/requirements-docx.txt](scripts/requirements-docx.txt) | Optional DOCX export | `pip install -r …` | Tracked in git; bump manually in PRs |
| GitHub Actions in [`.github/workflows/`](.github/workflows/) | CI/CD | Action marketplace | Pin/bump action versions in workflow PRs |

We prefer pinned or ranged FLOSS packages from PyPI. New dependencies need a short rationale in the PR. We do not vendor unrelated AI security scanner trees into this guide repository.

## Build instructions

**Readers** do not need to build anything: use the [documentation site](https://mhaghighian.github.io/MLSecOps/) or browse `chapters-en/`.

**Maintainers / contributors** (site build & full QA verification):

Requirements: Python 3.12+, pip, and optionally [Conftest](https://www.conftest.dev/) (`v0.71.1` in CI) for OPA Rego evaluation.

```bash
python -m pip install -r requirements-pages.txt check-jsonschema jsonschema pyyaml beautifulsoup4
conftest verify --policy policies
python scripts/verify_repo.py --require-conftest --with-mkdocs
python -m unittest discover -s tests
python scripts/ai_security_scan.py --mcp schemas/examples/evidence-pack.example.json --pins schemas/examples/evidence-pack.example.json --fail-on HIGH
```

`scripts/verify_repo.py` validates workflow YAMLs, UTF-8 encoding (no BOM on `.py`/`.rego`/`.json`/`.js`), `CITATION.cff` ↔ `mkdocs.yml` ↔ `prepare_pages.py` version sync, strict Draft 2020-12 JSON Schema & negative cases (including calendar RFC-3339 date checks), YAML/JSON/Mermaid parity across all chapters, release manifest file coverage, Python unit tests, scanner smoke checks, Conftest pass/fail fixtures, and a single-pass `site/` HTML broken-link/anchor audit. See `.github/workflows/docs-check.yml` for the exact CI job definitions and [scripts README](scripts/README.md) for CLI details.

Optional (Word export) — also needs [Pandoc](https://pandoc.org/) for `scripts/build-docx.py`:

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
