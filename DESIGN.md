# Design — actors and actions

This repository publishes a **documentation handbook**, not a runtime application. The system below is the project itself (authoring, review, build, release, and hosting).

## Actors

| Actor | Role |
|-------|------|
| **Readers** | Consume the guide via [GitHub Pages](https://mhaghighian.github.io/MLSecOps/) or Markdown in `chapters-en/`. |
| **Contributors** | Propose changes via fork + pull request ([CONTRIBUTING.md](CONTRIBUTING.md), [DCO.md](DCO.md)). |
| **Repository owner / maintainer** | Merge policy, releases, security contact, GitHub admin ([GOVERNANCE.md](GOVERNANCE.md)). |
| **GitHub Actions** | Automated docs build, Pages deploy, optional release draft ([`.github/workflows/`](.github/workflows/)). |
| **Zenodo** (optional) | DOI deposit on GitHub Release publish. |

## Actions (happy path)

```text
Contributor  --PR-->  Maintainer review + CI (docs-check)
                         |
                         v
                      merge to main
                         |
          +--------------+--------------+
          v                             v
   docs-check (MkDocs)           Pages build + deploy
          |                             |
          v                             v
   status on PR/main              public documentation site
```

**Release path:** maintainer tags a version → GitHub Release (+ integrity manifest; see [RELEASE-INTEGRITY.md](RELEASE-INTEGRITY.md)) → Handbook Artifacts attaches DOCX/PDF → CHANGELOG / CITATION updated per [RELEASING.md](RELEASING.md).

## Dependency monitoring

Handbook build dependencies (`requirements-pages.txt`, `scripts/requirements-docx.txt`) and GitHub Actions are monitored by:

1. **Dependabot** (`.github/dependabot.yml`) — weekly PRs; DCO skips Dependabot authors.  
2. **`pip-audit`** (`.github/workflows/dependency-audit.yml`) — PR path filter + weekly schedule.

This keeps the docs supply chain aligned with the chain-of-custody themes in Chapter 5 without treating Dependabot noise as a reason to disable scanning.

## Trust boundaries

- Public content and workflows live in this git repository.  
- Secrets (e.g. Search Console verification) use **GitHub Actions secrets**, never committed files ([SECURITY.md](SECURITY.md)).  
- Readers do not execute project “software”; optional local builds use documented FLOSS tooling (Python, MkDocs, Pandoc).  
- Reference **Policy-as-Code** samples live under [`policies/`](policies/README.md) and machine-readable Evidence Pack schema under [`schemas/`](schemas/README.md) — illustrative controls, not a hosted enforcement service.
