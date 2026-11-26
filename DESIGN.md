# Design — actors and actions

This repository publishes a **reference model, operational handbook, and executable reference samples** (JSON Schemas, OPA/Conftest policies, and read-only static verification helpers), not a hosted runtime service. The system below is the project itself (authoring, automated verification, build, release, and hosting).

## Actors

| Actor | Role |
|-------|------|
| **Readers & adopters** | Consume the guide via [GitHub Pages](https://mhaghighian.github.io/MLSecOps/) or Markdown in `chapters-en/`, and adapt sample `schemas/`, `policies/`, and `scripts/`. |
| **Contributors** | Propose changes via fork + pull request ([CONTRIBUTING.md](CONTRIBUTING.md), [DCO.md](DCO.md)). |
| **Repository owner / maintainer** | Merge policy, releases, security contact, GitHub admin ([GOVERNANCE.md](GOVERNANCE.md)). |
| **GitHub Actions** | Automated schema/Conftest/scanner/MkDocs verification, dependency audits, Pages deploy, release signing, and DOCX/PDF builds ([`.github/workflows/`](.github/workflows/)). |
| **Zenodo** (optional) | DOI deposit on GitHub Release publish. |

## Actions (happy path)

```text
Contributor  --PR-->  DCO check + docs-check (JSON Schema, Conftest v0.71.1,
                      unittest, ai_security_scan.py, verify_repo --with-mkdocs)
                         |
                         v
                   Maintainer review -> merge to main
                         |
          +--------------+--------------+
          v                             v
   docs-check (strict CI)        Pages build + deploy
          |                             |
          v                             v
   status on PR/main              public documentation site
```

**Release path:** maintainer tags a version → `create-release` generates and Cosign-signs `SHA256SUMS` ([RELEASE-INTEGRITY.md](RELEASE-INTEGRITY.md)) → `handbook-artifacts` builds DOCX/PDF (`HANDBOOK-SHA256SUMS.txt`) and attaches to the draft release → maintainer publishes per [RELEASING.md](RELEASING.md).

## Dependency monitoring

Handbook build dependencies (`requirements-pages.txt`, `scripts/requirements-docx.txt`) are scanned by **`pip-audit`** (`.github/workflows/dependency-audit.yml`) on relevant PRs and on a weekly schedule. Reference runtime checks (`scripts/ai_security_scan.py`) rely strictly on the Python 3.12 standard library (zero external packages). **Dependabot auto-PRs stay disabled** (same ops choice as #21): manual maintainer PRs handle Action/pin bumps without PR noise.

## Trust boundaries

- Public content, schemas, policies, and CI workflows live in this git repository.  
- Secrets (e.g. Search Console verification tokens) use **GitHub Actions secrets**, never committed files ([SECURITY.md](SECURITY.md)).  
- `scripts/ai_security_scan.py` operates strictly as a zero-execution header/opcode/JSON inspector (`O(header)` slices via stdlib `pickletools`, `zipfile`, `json`, `struct`) so scanning untrusted model weights or MCP configs never invokes `pickle.loads` or spawns MCP server commands.  
- Reference **Policy-as-Code** samples (`policies/` + `policies/k8s/`) and Evidence Pack schemas (`schemas/`) illustrate admission/release gating, not a hosted enforcement service.
