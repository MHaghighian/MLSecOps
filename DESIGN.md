# Design — actors and actions

This repository publishes a **documentation handbook**, not a runtime application. The system below is the project itself (authoring, review, build, release, and hosting).

## Actors

| Actor | Role |
|-------|------|
| **Readers** | Consume the guide via [GitHub Pages](https://mhaghighian.github.io/MLSecOps/) or Markdown in `chapters-en/`. |
| **Contributors** | Propose changes via fork + pull request ([CONTRIBUTING.md](CONTRIBUTING.md), [DCO.md](DCO.md)). |
| **Repository owner / maintainer** | Merge policy, releases, security contact, GitHub admin ([GOVERNANCE.md](GOVERNANCE.md)). |
| **GitHub Actions** | Automated docs build, Pages deploy, optional release draft ([`.github/workflows/`](.github/workflows/)). |
| **Dependabot** | Opens PRs for dependency updates (`requirements-pages.txt`, Actions). |
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

**Release path:** maintainer tags a version → GitHub Release (+ integrity manifest; see [RELEASE-INTEGRITY.md](RELEASE-INTEGRITY.md)) → CHANGELOG / CITATION updated per [RELEASING.md](RELEASING.md).

## Trust boundaries

- Public content and workflows live in this git repository.  
- Secrets (e.g. Search Console verification) use **GitHub Actions secrets**, never committed files ([SECURITY.md](SECURITY.md)).  
- Readers do not execute project “software”; optional local builds use documented FLOSS tooling (Python, MkDocs, Pandoc).
