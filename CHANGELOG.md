# Changelog

All notable changes to the MLSecOps Guide are documented here.

## [Unreleased]

### Fixed

- **GitHub Pages / sitemap URLs** — after account rename, `site_url`, `robots.txt`, and docs links now use `https://mhaghighian.github.io/MLSecOps/` (the old `l4tr0d3ctism.github.io` host 404s and broke Search Console sitemap reads).

## [1.1.1] — 2026-07-16

### Fixed

- **Issue #1 reference blocks restored** — expanded compacted `> *Refs - …*` lines from PR #3 back to per-section `### References / Source mapping` blocks across Chapters 1–17, keeping the corrected framework IDs and content from that review.

### Changed

- Community review merge ([PR #3](https://github.com/l4tr0d3ctism/MLSecOps/pull/3) by [@Ali-Razmjoo](https://github.com/Ali-Razmjoo)): citation fixes (ATLAS/OWASP IDs), scope clarifications, Evidence Pack / maturity wording, Stage 3 naming, Ch.6 worked example, and related chapter edits.
- **Release packaging** — PDF and DOCX are no longer attached to GitHub Releases or linked from the site; generate locally with `scripts/build-docx.py` when needed.

### Removed

- **GUIDE-SUMMARY.md** and related summary navigation/links from README, GETTING-STARTED, MkDocs, and GitHub Pages.
- Pre-built **PDF / DOCX** download links from README, Getting Started, and release pages (build script remains).

### Added

- **[references/AARM-ALIGNMENT.md](references/AARM-ALIGNMENT.md)** — complementary mapping to CSA AARM (Autonomous Action Runtime Management); links from Ch.8 and GETTING-STARTED.

## [1.1.0] — 2026-07-11

### Added

- **Per-section traceability (Issue #1)** — `References / Source mapping` blocks on every major `##` section across Chapters 1–17; [traceability convention](chapters-en/15-conclusion-appendix.md#traceability-and-source-mapping-convention) in Ch.15; CONTRIBUTING/GOVERNANCE expectations updated.
- **OWASP AI Exchange integration** — complementary positioning and per-section source mapping where applicable: Ch.1 Exchange relationship; Ch.2 AI inventory + risk workflow; Ch.5 poisoning taxonomy + model theft paths; Ch.6 three test categories; Ch.7 augmentation data, downstream injection, verification gaps; Ch.12 periodic table cross-ref; `GETTING-STARTED.md` resource selector; Ch.15 Exchange citation.
- **Ch.1 — Why this guide matters** — explicit reader value proposition, learning outcomes, and practical takeaways ([Issue #2](https://github.com/l4tr0d3ctism/MLSecOps/issues/2)).
- **Ch.1 — Guide at a glance** — audience, goal, outputs, and scope summary after Abstract.

### Changed

- **Ch.1** — intro polish: transition sentence, split paragraphs, lifecycle lead-in, wording fixes per community review.
- **Ch.1–17** — framework source mapping audit: OWASP LLM/ML Top 10 IDs, MITRE ATLAS techniques, NIST AI RMF, ISO/IEC 42001, OpenSSF, and OWASP AI Exchange permalinks aligned to section topics.
- **GETTING-STARTED.md** — Quick Start (5 Minutes), *New to AI Security?* path, renamed production baseline section, *When to use this guide vs. OWASP AI Exchange*.
- **TABLE-OF-CONTENTS.md** — Ch.1 entries for *Why this guide matters* and *What this guide adds*; traceability convention; Exchange-related sections (Ch.1–2, 5–7, 12).
- **Ch.7** — removed duplicate augmentation block under Ingest security (cross-ref only).
- **Ch.12 / Ch.15 Appendix B** — MITRE ATLAS table synchronized (`AML.T0066`, `AML.T0034`).
- **Ch.13** — LangChain case study: added CVE-2025-68664 alongside CVE-2025-27520.
- **prepare_pages.py** — rewrite anchored `GETTING-STARTED.md#…` links for MkDocs; site index banner v1.1.0.
- **README.md** — OWASP AI Exchange in frameworks list; version and download links v1.1.0.
- Version strings aligned to **v1.1.0** across Ch.1, TOC, README, CITATION.cff, CONTRIBUTING, GOVERNANCE, SECURITY, RELEASE_NOTES, and releases README.

## [1.0.1] — 2026-07-05

### Added

- **Zenodo DOI** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) for long-term citation.
- **Zenodo archival release** — no guide content changes; triggers DOI after GitHub–Zenodo integration.

## [1.0.0] — 2026-07-05

### Added

- **GitHub Release v1.0.0** with DOCX and PDF (`MLSecOps Practical Reference Guide`).
- Printable editions aligned with markdown source (16 chapters + Appendix E).
- **Diagram PNG assets** in `assets/diagrams/` (26 static Mermaid exports).

### Changed

- Version bump from **v0.1.2** (public beta) to **v1.0.0** — content scope frozen for citation.
- README, TOC, and site banner aligned to v1.0.0.

## [0.1.2] — 2026-07-05

### Added

- **GitHub Pages** documentation site: https://mhaghighian.github.io/MLSecOps/ (MkDocs Material, Mermaid).
- Public-beta README restructure: Getting Started, Downloads, Community feedback, Releases docs.
- [GETTING-STARTED.md](GETTING-STARTED.md), [RELEASING.md](https://github.com/MHaghighian/MLSecOps/blob/main/RELEASING.md), [releases/README.md](https://github.com/MHaghighian/MLSecOps/blob/main/releases/README.md).
- **Chapter 16** Kubernetes deployment reference.
- **Appendix E: Implementation Reference** — architecture cards, decision matrix, threat model template, Evidence Pack template, playbooks, master control matrix.
- **How to use this guide** (Ch.1) and role-based Quick Start (README, docs site).
- **Managed AI services security reference** (Ch.2) and **Appendix D** checklist with Evidence Pack fields.
- **Agent chapter priority 2:** think–act cycle, conversation manipulation, exfiltration model, defense layers, secure lifecycle, KPIs.
- **LLM verification approach** (Ch.7) complementing OWASP LLMSVS.
- **Positioning:** *MLSecOps Practical Reference Guide*; **What this guide adds** in Ch.1 and Final Conclusion (four operational contributions).
- GitHub Actions workflows: `pages.yml`, manual `release.yml` (v1.0+).

### Changed

- README: live documentation site link; contributor and governance docs updated.
- MkDocs site built in CI from `chapters-en/` (removed committed `docs/` tree).
- **Chapter 3** condensed: demonstrated threats first; emerging topics in summary table (~450 → ~170 lines).
- Ch.12 tool commands relabeled as optional appendix; Ch.12 reading note: primary mapping vs optional CLI appendix.
- Removed `examples/` directory; Ch.16 points to upstream vendor references only.
- README, TOC, and citation text aligned with Practical Reference Guide positioning.

### Fixed

- Unified lifecycle terminology across Ch.1, 6, 9, 11, 15, 16 (`control points`, `release decisions`, `Integrity and Provenance`).
- Appendix order in Ch.15 (A → B → D).

## [0.1.1] — 2026-06-21

### Fixed

- Canonical **policy gate** model (stages 4, 7, 8) vs integrity checkpoint (stage 9); resolved minimum-baseline contradictions.
- **OWASP LLM04** vs **LLM08** mapping for retrieval/RAG corpus poisoning (Appendix A, Claims table).
- **MITRE ATLAS** AI worm mapping (no false 1:1 ID with memory poisoning).
- Softened non-standard overclaims in conclusion; clarified **OpenSSF** relationship (independent, non-affiliated guide).
- Case study citations and **Documented incident** vs **Illustrative pattern** labels.
- Removed unverified tool reference (`BlackVault`); privacy/GDPR section for prompt logging; Feature Store, LoRA/PEFT, MCP sections.
- Maturity Level 3 criteria (process-based, not “zero incidents”); ethics box in Chapter 3.

### Added

- `examples/evidence-pack-schema.json` — starter Evidence Pack schema.
- `GOVERNANCE.md`, `CHANGELOG.md`.

## [0.1.0] — 2026-06

Initial public draft: 15 chapters, MkDocs site, threat/control mapping, maturity roadmap.
