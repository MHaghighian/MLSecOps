# MLSecOps Practical Reference Guide

> **Open-source MLSecOps handbook for AI security, LLM/RAG, and secure MLOps.**

[![Status](https://img.shields.io/badge/status-stable-blue)](CHANGELOG.md)
[![Version](https://img.shields.io/badge/version-v1.1.0-lightgrey)](CHANGELOG.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21206781.svg)](https://doi.org/10.5281/zenodo.21206781)
[![Documentation](https://img.shields.io/badge/docs-l4tr0d3ctism.github.io%2FMLSecOps-blue)](https://l4tr0d3ctism.github.io/MLSecOps/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-green.svg)](LICENSE)

**MLSecOps Practical Reference Guide** is an open-source handbook for **AI security**, **machine learning security**, and **secure MLOps** across the full ML lifecycle — from data and training through deployment, runtime monitoring, SOC, and governance.

It covers **LLM security**, **RAG security**, **agentic AI**, **MCP**, **AI supply chain security**, and **DevSecOps** patterns for production AI systems. Use it as a practitioner reference — not a product manual or an official OWASP, NIST, or ISO standard.

| | |
|---|---|
| **Read online (recommended)** | [l4tr0d3ctism.github.io/MLSecOps](https://l4tr0d3ctism.github.io/MLSecOps/) |
| **Source repository** | [github.com/l4tr0d3ctism/MLSecOps](https://github.com/l4tr0d3ctism/MLSecOps) |
| **Latest release** | [v1.1.0](https://github.com/l4tr0d3ctism/MLSecOps/releases/tag/v1.1.0) |
| **Cite (DOI)** | [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) |

---

## Who is this for?

Security engineers, ML/MLOps teams, architects, and risk owners who need a **practical MLSecOps** reference aligned with OWASP AI Exchange, MITRE ATLAS, NIST AI RMF, ISO/IEC 42001, OpenSSF Secure MLOps, and CSA MAESTRO — with operational controls, evidence, and rollout guidance.

---

## What this guide adds

This guide **synthesizes** OWASP, MITRE ATLAS, NIST AI RMF, ISO/IEC 42001, OpenSSF Secure MLOps, and CSA MAESTRO. Its operational additions are:

1. **Ten lifecycle control points** — one thread from change initiation through monitoring  
2. **Explicit release decisions** — separate evidence-producing steps from blocking gates (control points 4, 7, 8) and integrity at 9  
3. **`Evidence Pack`** — auditable output bundle per release  
4. **[Implementation Reference](chapters-en/17-appendix-e-implementation-reference.md)** — architecture cards, decision matrix, templates, playbooks  

Learn more: [Chapter 1 — What this guide adds](chapters-en/01-intro.md#what-this-guide-adds-beyond-owasp-openssf-and-nist).

---

## Topics covered

| Area | Chapters / focus |
|------|------------------|
| **MLSecOps & threat modeling** | Scope, risk, autonomous AI threats |
| **Data security & privacy** | Training data, PII, augmentation confidentiality |
| **AI / ML supply chain** | Model artifacts, provenance, signing |
| **Secure ML pipeline** | Ten control points, CI/CD gates, Evidence Pack |
| **LLM security & RAG** | Gateway, guardrails, prompt injection, retrieval ACL |
| **Agentic AI & MCP** | Tool policy, Intent Gate, scoped execution |
| **Runtime & SOC** | Monitoring, detection, incident response |
| **Governance & compliance** | Evidence, maturity roadmap, Kubernetes patterns |

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

![MLSecOps lifecycle control model — ten control points from change initiation through monitoring and release decisions](assets/diagrams/01-intro_02.png)

**Coverage:** classic ML · LLM · RAG · managed AI APIs · agents · MCP · Shadow AI · supply chain · runtime · SOC · governance · Kubernetes patterns.

---

## Downloads

**Latest release:** **v1.1.0** · [Zenodo DOI](https://doi.org/10.5281/zenodo.21206781)

| Format | Link |
|--------|------|
| **Documentation site** | [l4tr0d3ctism.github.io/MLSecOps](https://l4tr0d3ctism.github.io/MLSecOps/) |
| **Markdown** | `chapters-en/` in this repository |
| **Source (ZIP)** | [v1.1.0 archive](https://github.com/l4tr0d3ctism/MLSecOps/archive/refs/tags/v1.1.0.zip) |
| **PDF** | [GitHub Releases](https://github.com/l4tr0d3ctism/MLSecOps/releases/download/v1.1.0/MLSecOps-Practical-Reference-Guide-v1.1.0.pdf) |
| **DOCX** | [GitHub Releases](https://github.com/l4tr0d3ctism/MLSecOps/releases/download/v1.1.0/MLSecOps-Practical-Reference-Guide-v1.1.0.docx) |

All releases: [GitHub Releases](https://github.com/l4tr0d3ctism/MLSecOps/releases).

### Build DOCX yourself

You can generate the printable Word edition from the markdown sources in this repository:

```bash
pip install -r scripts/requirements-docx.txt
python scripts/build-docx.py --render-mermaid
```

**Output:** `dist/MLSecOps-Practical-Reference-Guide-v{version}.docx` (version read from [CITATION.cff](CITATION.cff)).

| Option | Purpose |
|--------|---------|
| `--render-mermaid` | Render missing diagram PNGs from `assets/diagrams/source/*.mmd` (uses system Chrome or Edge) |
| `--reference path/to/file.docx` | Override the Word style template |
| `--output path/to/file.docx` | Custom output path |
| `--skip-validate` | Skip post-build content checks |

The build uses **Pandoc** with the project Word template (`scripts/templates/reference.docx`, or auto-download from the [v1.0.0 Release DOCX](https://github.com/l4tr0d3ctism/MLSecOps/releases/download/v1.0.0/MLSecOps-Practical-Reference-Guide-v1.0.0.docx) on first run). Template details: [scripts/templates/README.md](scripts/templates/README.md). Maintainer checklist: [RELEASING.md](RELEASING.md).

---

## Frequently asked questions

| Question | Answer |
|----------|--------|
| **What is MLSecOps?** | Security practices for the ML/AI lifecycle — extending DevSecOps with model, data, LLM, RAG, agent, and runtime controls. |
| **Is this an official OWASP or NIST document?** | No. It references those frameworks but is an independent open-source guide (CC BY-SA 4.0). |
| **Where should I start reading?** | [Documentation site](https://l4tr0d3ctism.github.io/MLSecOps/) or [Chapter 1](chapters-en/01-intro.md). |
| **How do I cite this work?** | Use the [Zenodo DOI](https://doi.org/10.5281/zenodo.21206781) or [CITATION.cff](CITATION.cff). |

---

## Repository structure

```text
MLSecOps/
├── chapters-en/          # Guide chapters (English)
├── assets/diagrams/      # Diagram PNGs and Mermaid source (.mmd)
├── scripts/              # DOCX build (build-docx.py, mermaid_to_png.py)
├── dist/                 # Local DOCX output (gitignored)
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

**Share this project:** linking from LinkedIn, blog posts, OWASP community threads, Dev.to, or internal security wikis helps others discover the guide and improves search visibility for `MLSecOps` and `MLSecOps Practical Reference Guide`.

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
