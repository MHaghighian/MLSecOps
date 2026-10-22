# Getting Started

Quick entry points for the **MLSecOps Practical Reference Guide**.  
Full section list: [TABLE-OF-CONTENTS.md](chapters-en/TABLE-OF-CONTENTS.md).

> **Start here before diving into chapters.** This repository is a **handbook of control intent**, not a shipped CI/CD product and not a certified standard. Tables and tool names are examples you adapt to your platform.

---

## Terms in 60 seconds

| Term | Means | Does **not** mean |
|------|--------|-------------------|
| **Control point (CP) 1–10** | Where evidence or a decision happens in the lifecycle ([Ch.6](chapters-en/06-pipeline.md)) | A mandatory Jenkins/GitHub Actions job |
| **Release decisions** | **CP 4, 7, 8** — policy go/no-go | Signing / config snapshot |
| **Integrity checkpoint** | **CP 9** — blocks **store/deploy** if signature/attest/verify (or managed config evidence) is missing | A fourth “policy release gate” of the same type as 4/7/8 |
| **Maturity Level 1 / 2 / 3** | How strong the program is ([Ch.14](chapters-en/14-maturity-roadmap.md)) | ISO/EU certification |
| **Evidence Pack** | Auditable bundle per release ([Ch.11](chapters-en/11-governance-evidence.md#what-is-an-evidence-pack)) | A product you download from this repo |
| **`Baseline` (metrics)** | Signed reference model/metric for regression | The “minimum security baseline” MUST set (different idea) |

Canonical decision card: [Release decision model](chapters-en/06-pipeline.md#release-decision-model).

---

## Which framework first?

| You need… | Read first |
|-----------|------------|
| Threat/control taxonomy | [OWASP AI Exchange](https://owaspai.org) |
| When to block release + what evidence to keep | **This guide** ([Ch.6](chapters-en/06-pipeline.md), [Appendix E](chapters-en/17-appendix-e-implementation-reference.md)) |
| Org AI risk program / CSF language | NIST AI RMF; optional gap lens: NIST IR 8596 (**iprd draft — not certification**) |
| Tool examples (do **not** install everything) | [Ch.12](chapters-en/12-threat-control-tools-map.md) — pick by maturity label |

Relationship detail: [Chapter 1 — Relationship to OWASP AI Exchange](chapters-en/01-intro.md#relationship-to-owasp-ai-exchange).

---

## Quick Start (5 Minutes)

1. Read [Why this guide matters](chapters-en/01-intro.md#why-this-guide-matters) (Chapter 1)
2. Skim [What this guide adds](chapters-en/01-intro.md#what-this-guide-adds-beyond-owasp-openssf-and-nist) (Chapter 1)  
3. Skim [Attack surface matrix](chapters-en/02-scope-risk-threat-model.md#attack-surface-matrix) (Chapter 2)  
4. Review [Lifecycle control points](chapters-en/06-pipeline.md#lifecycle-control-points) + [Release decision model](chapters-en/06-pipeline.md#release-decision-model) (Chapter 6)  
5. Open [Primary Mapping](chapters-en/12-threat-control-tools-map.md#primary-mapping) (Chapter 12)  

---

## New to AI Security?

Recommended reading order for a first pass:

1. [Chapter 1 — Introduction](chapters-en/01-intro.md)
2. [Chapter 2 — Scope and threat model](chapters-en/02-scope-risk-threat-model.md)
3. [Chapter 3 — Threat landscape](chapters-en/03-threat-landscape.md)
4. [Chapter 6 — Lifecycle control model](chapters-en/06-pipeline.md)
5. [Chapter 7 — LLM and RAG security](chapters-en/07-llm-rag-security.md)
6. [Chapter 12 — Threat, control, and tool mapping](chapters-en/12-threat-control-tools-map.md)

Then branch by role using the paths below (avoid jumping straight into the middle of Ch.7/12).

---

## Reader paths by role (5 links each)

| Role | Path |
|------|------|
| **Architect** | [Ch.2 attack surface](chapters-en/02-scope-risk-threat-model.md#attack-surface-matrix) → [Ch.6 release decisions](chapters-en/06-pipeline.md#release-decision-model) → [Appendix E.1 cards](chapters-en/17-appendix-e-implementation-reference.md#e1-architecture-cards) → [E.2 matrix](chapters-en/17-appendix-e-implementation-reference.md#e2-decision-matrix) → [Ch.12 primary map](chapters-en/12-threat-control-tools-map.md#primary-mapping) |
| **AppSec / AI Security** | [Ch.3 threats](chapters-en/03-threat-landscape.md) → [Ch.6 CP7 acceptance](chapters-en/06-pipeline.md#control-point-7-test-acceptance-conditions) → [Ch.7 LLM/RAG](chapters-en/07-llm-rag-security.md) → [Ch.10 SOC](chapters-en/10-monitoring-soc-ir.md) → [Ch.12 tools](chapters-en/12-threat-control-tools-map.md) |
| **ML / MLOps** | [Ch.6 control points](chapters-en/06-pipeline.md#lifecycle-control-points) → [Ch.5 supply chain](chapters-en/05-model-artifact-supply-chain.md) → [Ch.4 data/privacy](chapters-en/04-data-security-privacy.md) → [Ch.9 anti-patterns](chapters-en/09-anti-patterns.md) → [E.4 Evidence Pack](chapters-en/17-appendix-e-implementation-reference.md#e4-evidence-pack-template) |
| **Platform / SRE** | [Ch.16 K8s](chapters-en/16-kubernetes-deployment-reference.md) → [Ch.6](chapters-en/06-pipeline.md) → [Ch.10](chapters-en/10-monitoring-soc-ir.md) → [E.7.3 self-hosted](chapters-en/17-appendix-e-implementation-reference.md#e73-example-c-self-hosted-model-platform-vllmkserve-on-kubernetes) → [Ch.5 signing](chapters-en/05-model-artifact-supply-chain.md#provenance-and-signing) |
| **GRC / Compliance** | [Ch.11 Evidence Pack](chapters-en/11-governance-evidence.md#what-is-an-evidence-pack) → [Ch.14 maturity](chapters-en/14-maturity-roadmap.md) → [Ch.15 glossary](chapters-en/15-conclusion-appendix.md#short-glossary) → [Cyber AI Profile map](chapters-en/15-conclusion-appendix.md#appendix-cyber-ai-profile-mapping-nist-ir-8596) → [Appendix D managed AI](chapters-en/15-conclusion-appendix.md#appendix-d-managed-ai-services-security-reference) |

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

## Minimum security baselines (do not mix Levels)

From [Release decision model](chapters-en/06-pipeline.md#release-decision-model):

1. **Level 1 (foundational):** Documented decisions at **CP 4 and 8**; **CP 7** runs every release and is **recorded** (not yet required to block); **CP 9** integrity evidence is **mandatory** (signature **or** managed-API config snapshot).  
2. **Level 2+ / production:** **CP 4, 7, and 8** are **blocking** on every release/CT cycle (unless a formal audited exception); **CP 9** still **blocks store/deploy** when integrity evidence is missing.  
3. **Evidence Pack** per release (template + filled sample: [Appendix E.4](chapters-en/17-appendix-e-implementation-reference.md#e4-evidence-pack-template)).  
4. Runtime telemetry to SOC with privacy-aware prompt/response handling (Chapters 10 and 4).  
5. Architecture card matching your stack ([Appendix E.1](chapters-en/17-appendix-e-implementation-reference.md#e1-architecture-cards)).  

Maturity detail: [Chapter 14](chapters-en/14-maturity-roadmap.md).

> **Pipelines:** Sample Jenkins/control-plane labs (if any) live outside the published guide tree—use Chapters 6 and 12 for control intent, not as drop-in workflows.

---

## Formats

| Format | Location |
|--------|----------|
| Markdown (source) | `chapters-en/*.md` in this repo |
| Documentation site | [mhaghighian.github.io/MLSecOps](https://mhaghighian.github.io/MLSecOps/) |
| Maintainer site | [mhsec.me](https://mhsec.me) |
| Word (optional) | Build locally: `python scripts/build-docx.py --render-mermaid` |

---

## Give feedback

Help improve the guide: [open an issue](https://github.com/MHaghighian/MLSecOps/issues) or [start a discussion](https://github.com/MHaghighian/MLSecOps/discussions).
