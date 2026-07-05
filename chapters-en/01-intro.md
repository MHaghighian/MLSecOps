# Chapter 1: Abstract and Introduction

> **Guide type:** *MLSecOps Practical Reference Guide* **v1.0.0** — a community reference with operational patterns and an **Implementation Reference** ([Appendix E](17-appendix-e-implementation-reference.md)). This is **not** a product user manual, a certified standard, or an academic paper.

## Abstract

`MLSecOps` is a practical security framework for securing AI-based systems throughout their entire lifecycle—from data collection and model training to deployment, execution, monitoring, and incident response. This approach transforms security from a one-time pre-release check into an engineered, measurable, repeatable, and auditable process.

This guide focuses on AI supply chain threats, `Adversarial ML` attacks, large language model security, `RAG` systems, intelligent agents, and security controls at `Runtime`. The goal is to provide a practical architecture for teams that develop or maintain `ML` and `AI` systems in real-world operational environments.

**Problem:** Traditional `DevSecOps` controls are insufficient for AI systems because security risks extend beyond source code into data, models, prompts, embeddings, retrieval pipelines, and autonomous agents. Security failures in production AI systems often occur outside the application code layer—in training data, model artifacts, `RAG` indexes, and runtime behavior.

**Method:** This guide was developed by combining reference frameworks (`OWASP LLM/ML Top 10`, `MITRE ATLAS`, `NIST AI RMF`, `ISO/IEC 42001`, `OpenSSF MLSecOps`, `CSA MAESTRO`), real-world case studies, and operational implementation patterns. This guide is based on frameworks and knowledge published through the end of 2025.

**Author's position (not a research finding):** AI system security is more defensible when viewed as a continuous, auditable flow from data through runtime and SOC—not as periodic controls. This guide synthesizes published frameworks and operational patterns; it does not present original empirical results.

**Limitations:** This guide focuses on enterprise ML/LLM/Agent systems; `Edge/IoT/CPS` domains, safety, and industry-specific legal requirements are covered only briefly and require specialized resources.

**Keywords:** `MLSecOps`, `LLM Security`, `RAG Security`, `Agentic AI`, `Adversarial ML`, `AI Supply Chain`, `Model Signing`, `Lifecycle Security Controls`, `Evidence Pack`, `AI Governance`.

## Introduction

In classic software, `DevSecOps` successfully narrowed the gap between development, operations, and security. However, AI systems have several fundamental characteristics that make the same security model insufficient for them.

## What this guide adds beyond OWASP, OpenSSF, and NIST

This guide **synthesizes** published frameworks; it does not replace them. Its operational contribution is a single, auditable lifecycle view. In an interview or design review, the distinct additions are:

| # | Contribution | Where to read |
|---|---|---|
| 1 | **Ten lifecycle control points** spanning data, model, RAG, agent, and runtime—not only a threat taxonomy | [Chapter 6](06-pipeline.md) |
| 2 | **Separation of evidence-producing steps from blocking release decisions** (control points 4, 7, 8 vs integrity at 9) | [Chapter 6 — Release decision model](06-pipeline.md#release-decision-model) |
| 3 | **`Evidence Pack` as the auditable output per release**—one bundle tying data, tests, policy, and runtime evidence | [Chapter 11](11-governance-evidence.md#what-is-an-evidence-pack) |
| 4 | **Unified thread** from threat modeling through runtime, SOC, and governance in one lifecycle—not siloed LLM, agent, or MLOps docs | Ch.2 → 6 → 7/8 → 10 → 11; [Appendix E](17-appendix-e-implementation-reference.md) |

For architecture-specific controls, decision matrices, templates, and playbooks, use [Appendix E: Implementation Reference](17-appendix-e-implementation-reference.md).

## How to use this guide

This guide is long by design. Use the paths below based on role and architecture—not every chapter applies to every deployment.

| If you are… | Start here | Then read |
|---|---|---|
| Executive / risk owner | [AI Threat Surface](#ai-threat-surface-executive-overview), [Ch.2 scope](02-scope-risk-threat-model.md) | [Ch.14 maturity](14-maturity-roadmap.md), [Ch.11 governance](11-governance-evidence.md) |
| Security engineer | [Ch.2 threat model](02-scope-risk-threat-model.md), [Ch.3 threats](03-threat-landscape.md) | [Ch.6 lifecycle controls](06-pipeline.md), [Ch.12 mapping](12-threat-control-tools-map.md) |
| ML / MLOps engineer | [Ch.6 lifecycle controls](06-pipeline.md), [Ch.5 supply chain](05-model-artifact-supply-chain.md) | [Ch.4 data](04-data-security-privacy.md), [Ch.9 anti-patterns](09-anti-patterns.md) |
| LLM / RAG builder | [Ch.7 LLM/RAG](07-llm-rag-security.md) | [Ch.8 agents](08-agentic-ai-security.md) if tools/agents exist |
| Platform / K8s owner | [Ch.16 K8s reference](16-kubernetes-deployment-reference.md) | [Ch.7 gateway/MCP](07-llm-rag-security.md), [Ch.10 SOC](10-monitoring-soc-ir.md) |
| Managed AI API only (no training) | [Ch.2 managed AI](02-scope-risk-threat-model.md#managed-ai-services-security-reference) | [Ch.7 runtime](07-llm-rag-security.md), [Appendix D managed AI](15-conclusion-appendix.md#appendix-d-managed-ai-services-security-reference) |
| **Implementing in production** | [Appendix E Implementation Reference](17-appendix-e-implementation-reference.md) | [Ch.6](06-pipeline.md), [Ch.12 mapping](12-threat-control-tools-map.md) |

Full reading paths: [TABLE-OF-CONTENTS.md](TABLE-OF-CONTENTS.md#reading-paths). Tool command examples are optional implementation detail in [Chapter 12 appendix](12-threat-control-tools-map.md#appendix-informative-tool-command-reference).

## Why DevSecOps Is Insufficient

| Characteristic | Security impact |
|---|---|
| Heavy dependence on data | Data quality, privacy, and integrity directly determine model behavior. |
| Probabilistic behavior | A successful test does not guarantee the same attack will not recur in `Production`. |
| Broad attack surface | In addition to code, data, models, `Artifact`s, prompts, memory, tools, and `Retrieval` are also attackable. |
| Environmental variability | `Data Drift`, dependency changes, and shifts in user patterns can turn a secure model yesterday into an insecure one today. |

Probabilistic behavior in AI systems creates a serious security difference. In classic software, identical input usually yields identical output; but in AI models, the same prompt or the same data can produce different responses depending on conversation context, model settings such as `temperature`, model version, or data retrieved in `RAG`. From a security perspective, this means a successful test does not guarantee an attack will recur in `Production`; many attacks such as `Prompt Injection` take effect only in a specific combination of context—not like classic `SQL Injection` with a fixed, fully predictable input.

`MLSecOps` means security is not just a step before release. Security must be applied at every decision point in the model lifecycle: when data enters, when a base model is selected, during training, evaluation, signing, deployment, when user requests are received, when tools are invoked, when documents are retrieved, and when model behavior is monitored.

## AI Threat Surface (Executive Overview)

Threats in AI systems span multiple layers—not only application code. The overview below orients security teams before detailed analysis in later chapters.

| Layer | Example risks |
|---|---|
| Data | `Data Poisoning`, sensitive data leakage, training data extraction |
| Model | `Backdoor`, weight tampering, model theft, `Model Inversion` |
| Application | `Prompt Injection`, `RAG`/`Retrieval Poisoning`, `Tool Misuse`/`Tool Abuse` (`ASI02`), MCP tool poisoning, unsafe output handling |
| Governance (parallel) | Shadow AI (unsanctioned LLM use), ungoverned MCP in IDE | AI-AUP, enterprise gateway, MCP allowlist — [Ch.11](11-governance-evidence.md#shadow-ai-governance), [Ch.7 MCP](07-llm-rag-security.md#model-context-protocol-mcp-security) |
| Infrastructure | Open K8s namespace, unsigned images, GPU memory leak | RBAC, NetworkPolicy, signing verify — [Ch.16](16-kubernetes-deployment-reference.md) |
| Runtime | `Data Drift`, evasion, guardrail bypass, unmonitored agent actions |

> Autonomous/offensive AI threats: [Chapter 3](03-threat-landscape.md). Agent reference architecture, six-domain attack surface, and controls: [Chapter 8](08-agentic-ai-security.md). Full threat–control–tool mapping: [Chapter 12](12-threat-control-tools-map.md). Operational threat model and attack surface matrix: [Chapter 2](02-scope-risk-threat-model.md).

## MLSecOps Principles

These principles define how security decisions are made across the AI lifecycle:

| # | Principle | Summary |
|---|---|---|
| 1 | **Evidence before deployment** | No AI artifact enters production without traceable security evidence. |
| 2 | **Explicit release decisions** | Train, evaluate, sign, and deploy only after defined risk-based decision criteria pass. |
| 3 | **Continuous runtime validation** | Production behavior is monitored; drift, injection, and tool abuse are detected and responded to. |
| 4 | **Traceable AI supply chain** | `SBOM`, `AI-BOM`, signing, and provenance record model origin, data lineage, and test history. |
| 5 | **Threat-modeled controls** | Controls match architecture and risk—not generic AI security checklists. |
| 6 | **Measurable, repeatable, auditable process** | Security decisions use defined criteria, run on every build or retrain, and leave reviewable records. |

**Principle 1 in practice:** Evidence must show where data came from, how the model was built, which tests were run, who approved release, which `Artifact`s were signed, and which behaviors are monitored at runtime.

## Relationship between MLSecOps and DevSecOps

`DevSecOps` provides the foundation for securing code, infrastructure, dependencies, containers, secrets, and `CI/CD`. `MLSecOps` extends this foundation for AI-specific assets: data, models, `Model Registry`, `Prompt`, `Embedding`, `Vector DB`, `RAG`, and intelligent agents. `Feature Store` security (access control, lineage, PII in features) is covered in [Chapter 4](04-data-security-privacy.md).

| Dimension | `DevSecOps` | `MLSecOps` |
|---|---|---|
| Primary asset | Code, image, dependency | Data, model, embedding, prompt |
| Supply chain artifact | Package, container image | Model weights, dataset, vector index, prompt template |
| Security testing | SAST, SCA, DAST | Adversarial test, LLM red team, backdoor scan |
| Attack surface | API, container, IaC | Inference API, RAG, agent tool, GPU memory |
| Promotion control | Build and deploy gate | Risk-based release decision before train/configure, evaluate, integrity check, and deploy |
| Monitoring | Log, metric, alert | Drift, prompt injection, tool abuse |
| Evidence | SBOM, attestation | SBOM + `AI-BOM`, model signing, `Evidence Pack` |

`MLSecOps` does not replace `DevSecOps`; without a solid `DevSecOps` foundation, `MLSecOps` cannot endure. Both must be integrated into the organization's delivery and operations lifecycle.

### AI supply chain evidence (`AI-BOM`)

`AI-BOM` extends `SBOM` for AI-specific artifacts. At minimum it should describe model origin, dataset lineage, training framework, fine-tuning history, dependencies, evaluation results, security tests, and deployment artifacts. Full requirements, tooling, and lifecycle integration are covered in [Chapter 5](05-model-artifact-supply-chain.md).



![](../assets/diagrams/01-intro_01.png)


## Lifecycle Overview



![](../assets/diagrams/01-intro_02.png)


Each stage in this lifecycle maps to security control points, evidence collection, and release decisions described in [Chapter 6](06-pipeline.md). The table below maps this executive view (8 stages) to the 10-part lifecycle control model in Chapter 6. The model is intentionally implementation-neutral; organizations may implement it through CI/CD, MLOps platforms, manual approval workflows, or managed AI service governance depending on their architecture and maturity.

| Executive lifecycle (Ch.1) | Lifecycle control points (Ch.6) |
|---|---|
| Data Ingest | 1 `Initiate Change`, 2 `Load Artifacts`, 3 `Security & Quality Review`, 4 `Data / Artifact Decision Point` |
| Train / Fine-tune | 5 `Train or Configure` |
| Evaluate | 6 `Evaluate Model` |
| Security Test | 7 `Security Validation` |
| Sign & Register | 8 `Release Decision`, 9 `Integrity and Provenance` |
| Deploy | 9 `Integrity and Provenance` (verify before serve) + 10 `Store & Monitor` (registry and serving path) |
| Runtime Monitor | 10 `Store & Monitor` (telemetry, guardrails, canary/shadow) |
| SOC / IR | 10 `Store & Monitor` + [Chapter 10](10-monitoring-soc-ir.md) SOC integration |

> **Relationship to OpenSSF:** The term `MLSecOps` is also used by the [OpenSSF Secure MLOps whitepaper (2025)](https://openssf.org/wp-content/uploads/2025/08/OpenSSF_MLSecOps_Whitepaper.pdf). This guide is an **independent, non-normative community reference**—not published, endorsed, or maintained by OpenSSF. Where concepts overlap, we cite OpenSSF explicitly and map controls in [Chapter 11](11-governance-evidence.md); this guide adds explicit lifecycle decision points and evidence collection patterns on top of lifecycle stages described in industry literature.

## Relationship to OWASP projects

This guide is designed to complement—not replace—existing OWASP AI security work:

| OWASP project | Primary role | How this guide uses it |
|---|---|---|
| `OWASP Top 10 for LLM Applications` | Threat categories for LLM applications | Used as a threat taxonomy for prompt injection, data leakage, supply chain, agentic risk, and runtime controls |
| `OWASP LLMSVS` / `AISVS` | Verification requirements and test expectations | Used as verification references; this guide does not redefine detailed test procedures |
| `OWASP MCP Top 10` and MCP Security Cheat Sheet | MCP-specific risks and mitigations | Used for MCP gateway, tool schema, shadow MCP, and tool-output control guidance |
| `OWASP Agentic Security Initiative` | Agentic threat taxonomy and controls | Used for tool misuse, intent gates, memory poisoning, and multi-agent boundaries |
| `OWASP Machine Learning Security Top 10` | Classic ML threat categories | Referenced as draft/working terminology until finalized |

The contribution of this guide is the **lifecycle view**: selecting and sequencing controls across data, model, supply chain, RAG, agents, runtime, SOC, and governance. It is not a replacement for OWASP verification standards, tool documentation, or legal/compliance review.

## Focus of this guide and distinction from AISecOps

This guide focuses specifically on `MLSecOps`: securing the full lifecycle of `ML/AI` systems from data and training through artifacts, lifecycle controls, deployment, runtime, and monitoring.

`MLSecOps` must not be confused with the similar term `AISecOps`, because these are two different domains:

| Term | Definition | Central question |
|---|---|---|
| `MLSecOps` | Security of the model lifecycle and AI systems (subject of this guide) | "How do I build, release, and run an AI system securely?" |
| `AISecOps` | Using artificial intelligence within security operations itself—employing AI for threat detection, alert triage, analysis, and automated response in the `SOC` (per NSFOCUS definition, combining `AIOps` + `AISec` + `SecOps`) | "How do I use AI to automate security operations?" |

In simple terms: `MLSecOps` means "securing AI," while `AISecOps` means "using AI for security." This guide is entirely within the `MLSecOps` domain and does not enter the realm of `AISecOps`; although in Chapter 10, which addresses integration with the `SOC`, the practical point of contact between these two domains is shown.

In short, `MLSecOps` applies the same logic as `DevSecOps`, but for securing data, models, lifecycle decision points, `Runtime`, and the behavior of AI systems—not just code and infrastructure.
