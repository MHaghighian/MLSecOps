# Changelog

All notable changes to the MLSecOps Guide are documented here.

## [Unreleased]

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
- README, TOC, Persian summary, and site banner aligned to v1.0.0.

## [0.1.2] — 2026-07-05

### Added

- **GitHub Pages** documentation site: https://l4tr0d3ctism.github.io/MLSecOps/ (MkDocs Material, Mermaid).
- Public-beta README restructure: Getting Started, Downloads, Community feedback, Releases docs.
- [GETTING-STARTED.md](GETTING-STARTED.md), [RELEASING.md](RELEASING.md), [releases/README.md](releases/README.md).
- [GUIDE-SUMMARY.md](GUIDE-SUMMARY.md) — full Persian section-by-section summary.
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
