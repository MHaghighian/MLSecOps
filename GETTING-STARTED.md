# Getting Started

Quick entry points for the **MLSecOps Practical Reference Guide**.  
Full section list: [TABLE-OF-CONTENTS.md](chapters-en/TABLE-OF-CONTENTS.md).

---

## Quick Start (5 Minutes)

1. Read [Why this guide matters](chapters-en/01-intro.md#why-this-guide-matters) (Chapter 1)
2. Skim [What this guide adds](chapters-en/01-intro.md#what-this-guide-adds-beyond-owasp-openssf-and-nist) (Chapter 1)  
3. Skim [Attack surface matrix](chapters-en/02-scope-risk-threat-model.md#attack-surface-matrix) (Chapter 2)  
4. Review [Lifecycle control points](chapters-en/06-pipeline.md#lifecycle-control-points) (Chapter 6)  
5. Open [Primary Mapping](chapters-en/12-threat-control-tools-map.md#primary-mapping) (Chapter 12)  

---

## New to AI Security?

Recommended reading order for a first pass:

1. [Chapter 1 — Introduction](chapters-en/01-intro.md)
2. [Chapter 2 — Scope and threat model](chapters-en/02-scope-risk-threat-model.md)
3. [Chapter 3 — Threat landscape](chapters-en/03-threat-landscape.md)
4. [Chapter 6 — Lifecycle pipeline](chapters-en/06-pipeline.md)
5. [Chapter 7 — LLM and RAG security](chapters-en/07-llm-rag-security.md)
6. [Chapter 12 — Threat, control, and tool mapping](chapters-en/12-threat-control-tools-map.md)

Then branch by role or goal using the tables below.

---

## When to use this guide vs. OWASP AI Exchange

| You need… | Start here |
|-----------|------------|
| Threat/control taxonomy for any AI type, risk-analysis decision tree, deep testing methodology | [OWASP AI Exchange](https://owaspai.org) |
| Lifecycle control points, release gates, `Evidence Pack`, K8s/MCP ops patterns | **This guide** ([Chapter 6](chapters-en/06-pipeline.md), [Appendix E](chapters-en/17-appendix-e-implementation-reference.md)) |
| Both | Exchange for *what* threats/controls apply → this guide for *when* to implement and *what evidence* to keep |

Relationship detail: [Chapter 1 — Relationship to OWASP AI Exchange](chapters-en/01-intro.md#relationship-to-owasp-ai-exchange).

---

## By goal

| Goal | Path |
|------|------|
| Executive overview | Ch. [1](chapters-en/01-intro.md) → [2](chapters-en/02-scope-risk-threat-model.md) → [14](chapters-en/14-maturity-roadmap.md) |
| Threat understanding | Ch. [3](chapters-en/03-threat-landscape.md) → [2](chapters-en/02-scope-risk-threat-model.md) → [13](chapters-en/13-case-studies.md) |
| Implement lifecycle controls | Ch. [6](chapters-en/06-pipeline.md) → [12](chapters-en/12-threat-control-tools-map.md) → [15 checklists](chapters-en/15-conclusion-appendix.md#production-operational-checklist) |
| LLM / RAG / Agent | Ch. [7](chapters-en/07-llm-rag-security.md) → [8](chapters-en/08-agentic-ai-security.md) → [9](chapters-en/09-anti-patterns.md) · [AARM alignment](references/AARM-ALIGNMENT.md) |
| Managed AI API only | Ch. [2 managed AI](chapters-en/02-scope-risk-threat-model.md#managed-ai-services-security-reference) → [7](chapters-en/07-llm-rag-security.md) → [Appendix D](chapters-en/15-conclusion-appendix.md#appendix-d-managed-ai-services-security-reference) |
| Shadow AI / governance | Ch. [2](chapters-en/02-scope-risk-threat-model.md) → [11](chapters-en/11-governance-evidence.md) → [13 Samsung case](chapters-en/13-case-studies.md) |
| MCP security | Ch. [7 MCP](chapters-en/07-llm-rag-security.md#model-context-protocol-mcp-security) → [8](chapters-en/08-agentic-ai-security.md) → [12](chapters-en/12-threat-control-tools-map.md) → [13 MCP lab](chapters-en/13-case-studies.md) |
| SOC / operations | Ch. [10](chapters-en/10-monitoring-soc-ir.md) → [11](chapters-en/11-governance-evidence.md) |
| Kubernetes | Ch. [16](chapters-en/16-kubernetes-deployment-reference.md) |
| **Production rollout** | **[Appendix E](chapters-en/17-appendix-e-implementation-reference.md)** → Ch. [6](chapters-en/06-pipeline.md) → Ch. [12](chapters-en/12-threat-control-tools-map.md) |

---

## By role

| Role | Recommended path |
|------|------------------|
| Application / Security Architect | Ch. 2 → 6 → Appendix E → 12 |
| AppSec / AI Security Engineer | Ch. 3 → 6 → 7 → 10 → 12 |
| ML / MLOps Engineer | Ch. 6 → 5 → 4 → 9 |
| Platform / SRE | Ch. 16 → 6 → 10 |
| GRC / Compliance | Ch. 11 → 15 → Appendix D |

---

## Minimum Production Security Baseline

From Chapter 6 and Appendix E:

1. Threat model with release blockers at control points **4, 7, 8, 9**  
2. **Evidence Pack** per release (template in [Appendix E.4](chapters-en/17-appendix-e-implementation-reference.md#e4-evidence-pack-template))  
3. Runtime logging to SOC (Chapter 10)  
4. Architecture card matching your stack ([Appendix E.1](chapters-en/17-appendix-e-implementation-reference.md#e1-architecture-cards))  

Maturity detail: [Chapter 14](chapters-en/14-maturity-roadmap.md).

---

## Formats

| Format | Location |
|--------|----------|
| Markdown (source) | `chapters-en/*.md` in this repo |
| Documentation site | [mhaghighian.github.io/MLSecOps](https://mhaghighian.github.io/MLSecOps/) |
| Word (optional) | Build locally: `python scripts/build-docx.py --render-mermaid` |

---

## Give feedback

Help improve the guide: [open an issue](https://github.com/MHaghighian/MLSecOps/issues) or [start a discussion](https://github.com/MHaghighian/MLSecOps/discussions).
