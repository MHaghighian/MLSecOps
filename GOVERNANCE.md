# Governance

## Project status

The **MLSecOps Practical Reference Guide** is an independent, open-source **practical reference** maintained on GitHub. It is **not**:

- An official standard from OpenSSF, OWASP, NIST, ISO, or the EU
- A certified compliance product or legal advice
- Affiliated with employers or vendors mentioned in case studies

## Relationship to OpenSSF MLSecOps

The term *MLSecOps* appears in the [OpenSSF Secure MLOps whitepaper (2025)](https://openssf.org/wp-content/uploads/2025/08/OpenSSF_MLSecOps_Whitepaper.pdf). **This repository is not an OpenSSF project.** We cite OpenSSF as a primary reference and map lifecycle stages in Chapter 11; for OpenSSF normative architecture, use their publication and [ossf/ai-ml-security](https://github.com/ossf/ai-ml-security).

## Members with access to sensitive resources

Sensitive resources for this project include: GitHub repository admin settings, Actions secrets, Pages deploy environment, release publishing, and security advisories.

| Person | GitHub | Access |
|--------|--------|--------|
| Moslem Haghighian | [@MHaghighian](https://github.com/MHaghighian) | Repository owner / admin (all sensitive resources) |

No other accounts hold admin or secrets access unless listed here after review. Collaborators receive **least privilege** (typically triage/write via invite) and are not granted admin or secrets by default.

## Roles and responsibilities

| Role | Who | Responsibility |
|------|-----|----------------|
| Repository owner / maintainer | Moslem Haghighian | Merge policy, release tagging, SECURITY contact, Actions secrets, branch/rules settings |
| Contributors | Community (via PR) | Content fixes and improvements per [CONTRIBUTING.md](CONTRIBUTING.md) and [DCO.md](DCO.md) |
| Readers | Public | Consume documentation; no write access |

Actors and system actions: [DESIGN.md](DESIGN.md).

## Versioning

- **Major (x.0):** First stable release or structural revision (e.g. v1.0.0 lifecycle model frozen).
- **Minor (0.x):** Content updates, mapping fixes, Appendix E improvements.
- **Current release:** v1.3.0 — Markdown source and documentation site; optional DOCX via `scripts/build-docx.py`.

Document versions in [README.md](README.md), [CHANGELOG.md](CHANGELOG.md), and [RELEASE_NOTES.md](RELEASE_NOTES.md). Release process: [RELEASING.md](RELEASING.md). Integrity: [RELEASE-INTEGRITY.md](RELEASE-INTEGRITY.md).

## Decision process

1. Significant structural changes: GitHub Discussion or Issue with 14-day comment period when possible.
2. Technical corrections: Pull request with chapter reference and source citation.
3. Security issues in **this repository**: see [SECURITY.md](SECURITY.md)—not model vulnerabilities in reader deployments.
4. Escalated permissions (admin, secrets): granted only by the repository owner after reviewing the collaborator’s need and trust.

## Review expectations

Contributions should include:

- Primary source or framework reference for factual claims
- Per-section **`References / Source mapping`** where applicable (see [Ch.15 traceability convention](chapters-en/15-conclusion-appendix.md#traceability-and-source-mapping-convention))
- Consistent OWASP/MITRE IDs with Chapter 2 version notes
- Disclaimer when introducing non-standard concepts or optional organizational scoring/tiering aids
- DCO sign-off on every commit ([DCO.md](DCO.md))

Peer review is open via GitHub pull requests; formal third-party certification is not claimed.
