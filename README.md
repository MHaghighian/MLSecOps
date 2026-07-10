# MLSecOps Practical Reference Guide

[![Status](https://img.shields.io/badge/status-stable-blue)](CHANGELOG.md)
[![Version](https://img.shields.io/badge/version-v1.1.0-lightgrey)](CHANGELOG.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21206781.svg)](https://doi.org/10.5281/zenodo.21206781)
[![Documentation](https://img.shields.io/badge/docs-l4tr0d3ctism.github.io%2FMLSecOps-blue)](https://l4tr0d3ctism.github.io/MLSecOps/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-green.svg)](LICENSE)

**Open-source practical reference guide** for securing AI systems across the ML lifecycle — from data and training through deployment, runtime, SOC, and governance.

**Not** a product user manual, an official industry standard, or affiliated with OpenSSF, OWASP, NIST, or ISO.

Start with the [Documentation site](https://l4tr0d3ctism.github.io/MLSecOps/) for the best reading experience, or browse the Markdown chapters directly in this repository.

---

## What this guide adds

This guide **synthesizes** OWASP, MITRE ATLAS, NIST AI RMF, ISO/IEC 42001, OpenSSF Secure MLOps, and CSA MAESTRO. Its operational additions are:

1. **Ten lifecycle control points** — one thread from change initiation through monitoring  
2. **Explicit release decisions** — separate evidence-producing steps from blocking gates (control points 4, 7, 8) and integrity at 9  
3. **`Evidence Pack`** — auditable output bundle per release  
4. **[Implementation Reference](chapters-en/17-appendix-e-implementation-reference.md)** — architecture cards, decision matrix, templates, playbooks  

Learn more: [Chapter 1 — What this guide adds](chapters-en/01-intro.md#what-this-guide-adds-beyond-owasp-openssf-and-nist).

---

## Why MLSecOps?

Traditional DevSecOps does not fully address model artifacts, training data, LLMs, RAG, agents, or runtime AI risks.

**MLSecOps** extends existing security practices with lifecycle-specific controls, evidence generation, and AI-focused governance — without replacing your CI/CD or MLOps platform.

---

## Key features

- Ten-point **lifecycle control model** and release decision points  
- **`Evidence Pack`** methodology per release  
- **[Implementation Reference](chapters-en/17-appendix-e-implementation-reference.md)** — architecture cards, templates, playbooks  
- **Threat / control / tool mapping** ([Ch.12](chapters-en/12-threat-control-tools-map.md))  
- **LLM, RAG, Agent, and MCP** security ([Ch.7](chapters-en/07-llm-rag-security.md) · [Ch.8](chapters-en/08-agentic-ai-security.md))  
- **AI supply chain** and model artifact security ([Ch.5](chapters-en/05-model-artifact-supply-chain.md))  
- **Kubernetes** reference patterns ([Ch.16](chapters-en/16-kubernetes-deployment-reference.md))  
- SOC integration, governance, case studies, and maturity roadmap  

---

## Quick start

| | |
|---|---|
| **Read online** | [Documentation site](https://l4tr0d3ctism.github.io/MLSecOps/) — full guide, search, TOC |
| **Markdown** | [Table of Contents](chapters-en/TABLE-OF-CONTENTS.md) · [Chapter 1](chapters-en/01-intro.md) |
| **Role-based paths** | [GETTING-STARTED.md](GETTING-STARTED.md) |
| **Persian summary** | [GUIDE-SUMMARY.md](GUIDE-SUMMARY.md) |
| **Contribute** | [CONTRIBUTING.md](CONTRIBUTING.md) · [Issues](https://github.com/l4tr0d3ctism/MLSecOps/issues) · [Discussions](https://github.com/l4tr0d3ctism/MLSecOps/discussions) |

| Role | Start here |
|------|------------|
| Executive / risk | [Ch.1](chapters-en/01-intro.md) → [Ch.2](chapters-en/02-scope-risk-threat-model.md) → [Ch.14](chapters-en/14-maturity-roadmap.md) |
| Security engineer | [Ch.2](chapters-en/02-scope-risk-threat-model.md) → [Ch.6](chapters-en/06-pipeline.md) → [Ch.12](chapters-en/12-threat-control-tools-map.md) |
| ML / MLOps | [Ch.6](chapters-en/06-pipeline.md) → [Ch.5](chapters-en/05-model-artifact-supply-chain.md) |
| LLM / RAG / Agent | [Ch.7](chapters-en/07-llm-rag-security.md) → [Ch.8](chapters-en/08-agentic-ai-security.md) |
| Production rollout | [Appendix E](chapters-en/17-appendix-e-implementation-reference.md) → [Ch.6](chapters-en/06-pipeline.md) |

Project status, roadmap, and governance: [GOVERNANCE.md](GOVERNANCE.md) · [CHANGELOG.md](CHANGELOG.md).

---

## Architecture

Executive lifecycle (detail in [Chapter 6](chapters-en/06-pipeline.md)):

![Executive lifecycle overview](assets/diagrams/01-intro_02.png)

**Coverage:** classic ML · LLM · RAG · managed AI APIs · agents · MCP · Shadow AI · supply chain · runtime · SOC · governance · Kubernetes patterns.

---

## Downloads

**Latest release:** **v1.1.0** · [Zenodo DOI](https://doi.org/10.5281/zenodo.21206781) *(publish new Zenodo version from tag `v1.1.0` after release)*

| Format | Link |
|--------|------|
| **Documentation site** | [l4tr0d3ctism.github.io/MLSecOps](https://l4tr0d3ctism.github.io/MLSecOps/) |
| **Markdown** | `chapters-en/` in this repository |
| **Source (ZIP)** | [v1.1.0 archive](https://github.com/l4tr0d3ctism/MLSecOps/archive/refs/tags/v1.1.0.zip) |
| **PDF** | [GitHub Releases](https://github.com/l4tr0d3ctism/MLSecOps/releases/download/v1.1.0/MLSecOps-Practical-Reference-Guide-v1.1.0.pdf) |
| **DOCX** | [GitHub Releases](https://github.com/l4tr0d3ctism/MLSecOps/releases/download/v1.1.0/MLSecOps-Practical-Reference-Guide-v1.1.0.docx) |

All releases: [GitHub Releases](https://github.com/l4tr0d3ctism/MLSecOps/releases).

---

## Repository structure

```text
MLSecOps/
├── chapters-en/          # Guide chapters (English)
├── assets/diagrams/      # Diagram PNGs and Mermaid source (.mmd)
├── GUIDE-SUMMARY.md      # Persian section-by-section summary
├── GETTING-STARTED.md    # Role-based reading paths
├── CITATION.cff          # Citation metadata (DOI)
├── CHANGELOG.md
└── .github/workflows/    # Pages deploy, releases
```

---

## Community feedback

We welcome review from practitioners.

- **Bug or typo:** [Open an issue](https://github.com/l4tr0d3ctism/MLSecOps/issues)  
- **Suggestion / discussion:** [GitHub Discussions](https://github.com/l4tr0d3ctism/MLSecOps/discussions)  
- **Pull request:** see [CONTRIBUTING.md](CONTRIBUTING.md)  

If you review the guide and agree to be listed, we can add your name under **Community reviewers** (with your permission only).

---

## Cite this work

See [CITATION.cff](CITATION.cff) for machine-readable metadata.

```text
Haghighian, M. (2026). MLSecOps Practical Reference Guide (v1.1.0).
Zenodo. https://doi.org/10.5281/zenodo.21206781
```

---

## Frameworks referenced

- OWASP AI Exchange (https://owaspai.org/)  
- OWASP LLM Top 10 (2025)  
- OWASP ML Top 10 (draft)  
- OWASP Agentic / MCP  
- MITRE ATLAS  
- NIST AI RMF  
- ISO/IEC 42001 · ISO/IEC 23894  
- EU AI Act  
- OpenSSF MLSecOps Whitepaper  
- CSA MAESTRO  

---

## Contributing · License

| | |
|---|---|
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | CC BY-SA 4.0 |
| [SECURITY.md](SECURITY.md) | Report issues in this repo |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards |

Questions: [Issues](https://github.com/l4tr0d3ctism/MLSecOps/issues) · [Discussions](https://github.com/l4tr0d3ctism/MLSecOps/discussions).
