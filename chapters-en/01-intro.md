# Chapter 1: Abstract and Introduction

> **Guide type:** *MLSecOps Practical Reference Guide* **v1.1.0** — a community reference with operational patterns and an **Implementation Reference** ([Appendix E](17-appendix-e-implementation-reference.md)). This is **not** a product user manual, a certified standard, or an academic paper.

## Abstract

`MLSecOps` is a practical security framework for securing AI-based systems throughout their entire lifecycle—from data collection and model training to deployment, execution, monitoring, and incident response. This approach transforms security from a one-time pre-release check into an engineered, measurable, repeatable, and auditable process.

This guide focuses on AI supply chain threats, `Adversarial ML` attacks, large language model security, `RAG` systems, intelligent agents, and security controls at `Runtime`. The goal is to provide a practical architecture for teams that develop or maintain `ML` and `AI` systems in real-world operational environments.

**Problem:** Traditional `DevSecOps` controls are insufficient for AI systems because security risks extend beyond source code into data, models, prompts, embeddings, retrieval pipelines, and autonomous agents. Security failures in production AI systems often occur outside the application code layer—in training data, model artifacts, `RAG` indexes, and runtime behavior.

**Method:** This guide was developed by combining reference frameworks (`OWASP LLM/ML Top 10`, `MITRE ATLAS`, `NIST AI RMF`, `ISO/IEC 42001`, `OpenSSF MLSecOps`, `CSA MAESTRO`), real-world case studies, and operational implementation patterns. This guide is based on frameworks and knowledge published through the end of 2025.

**Author's position (not a research finding):** AI system security is more defensible when viewed as a continuous, auditable flow from data through runtime and SOC—not as periodic controls. This guide synthesizes published frameworks and operational patterns; it does not present original empirical results.

**Limitations:** This guide focuses on enterprise ML/LLM/Agent systems; `Edge/IoT/CPS` domains, safety, and industry-specific legal requirements are covered only briefly and require specialized resources.

**Keywords:** `MLSecOps`, `LLM Security`, `RAG Security`, `Agentic AI`, `Adversarial ML`, `AI Supply Chain`, `Model Signing`, `Lifecycle Security Controls`, `Evidence Pack`, `AI Governance`.

### Guide at a glance

| | |
|---|---|
| **Audience** | AI Security, `AppSec`, `DevSecOps`, ML / `MLOps` engineers, architects, governance stakeholders |
| **Goal** | Translate AI security frameworks into practical lifecycle controls |
| **Key outputs** | Lifecycle control points, release gates, `Evidence Pack`, threat–control mappings, architecture references ([Appendix E](17-appendix-e-implementation-reference.md)) |
| **Scope** | Enterprise ML, LLM, and agent systems in production |
| **Not covered in depth** | Safety engineering, sector-specific regulations, `Edge`/`IoT`/`CPS` (see [Limitations](#abstract) above) |

> *Refs - Frameworks: OWASP LLM Top 10 (2025); MITRE ATLAS; NIST AI RMF; ISO/IEC 42001; OpenSSF MLSecOps whitepaper (2025); CSA MAESTRO - cited in Abstract method paragraph; full bibliography in [Chapter 15 References](15-conclusion-appendix.md#references). Author note: Keywords, limitations, and author's position are this guide's framing, not framework text.*

## Introduction

In classic software, `DevSecOps` successfully narrowed the gap between development, operations, and security. However, AI systems have several fundamental characteristics that make the same security model insufficient for them.

Despite the growing number of AI security frameworks, practitioners still lack a single implementation-oriented reference that connects threats, controls, governance, and operational deployment across the entire AI lifecycle.

> *Refs - Frameworks: OWASP AI Exchange; NIST AI RMF; OpenSSF MLSecOps whitepaper (2025). This guide: [Why this guide matters](#why-this-guide-matters); [What this guide adds](#what-this-guide-adds-beyond-owasp-openssf-and-nist).*

## Why this guide matters

**Who this is for:** security engineers, `AppSec` teams, `DevSecOps` practitioners, ML and `MLOps` engineers, platform owners, and governance stakeholders responsible for AI systems in production.

AI systems introduce security risks that traditional `DevSecOps` and `MLOps` practices do not fully address—model artifacts, training data, prompts, `RAG` pipelines, agents, runtime behavior, and AI supply-chain dependencies.

Security guidance for these topics is spread across multiple frameworks and publications (`OWASP`, `MITRE ATLAS`, `NIST AI RMF`, `ISO/IEC 42001`, `OpenSSF`, `CSA MAESTRO`). This guide helps practitioners translate that guidance into **lifecycle controls** they can apply in real deployments.

**What problem it helps solve:** teams need a single, implementation-oriented reference to identify AI-specific risks, select controls, define release gates, and produce auditable evidence—without treating any one framework as the only source of truth.

**After reading this guide, you should be able to:**

- identify AI-specific security risks across the ML lifecycle;
- map threats to concrete security controls and framework references;
- define release gates and evidence requirements for AI systems;
- build auditable `Evidence Pack` outputs for governance or security review;
- prioritize controls based on risk, maturity, and deployment context.

**Practical takeaways:** lifecycle control points and release decisions ([Chapter 6](06-pipeline.md)), threat–control–tool mappings ([Chapter 12](12-threat-control-tools-map.md)), architecture cards and playbooks ([Appendix E](17-appendix-e-implementation-reference.md)), and role-based reading paths ([How to use this guide](#how-to-use-this-guide), [GETTING-STARTED.md](../GETTING-STARTED.md)).

Rather than introducing another framework, this guide focuses on helping practitioners operationalize and connect existing guidance into a coherent MLSecOps lifecycle.

> *Refs - Frameworks: OWASP LLM Top 10 (2025); OWASP AI Exchange; MITRE ATLAS; NIST AI RMF; ISO/IEC 42001; OpenSSF MLSecOps whitepaper (2025); CSA MAESTRO - full citations in [Chapter 15 References](15-conclusion-appendix.md#references). Author note: The learning outcomes and reader value proposition are this guide's own framing, not framework text.*

## What this guide adds beyond OWASP, OpenSSF, and NIST

This guide **synthesizes** published frameworks; it does not replace them. Its operational contribution is a single, auditable lifecycle view. Compared with existing references, this guide contributes the following operational additions:

| # | Contribution | Where to read |
|---|---|---|
| 1 | **Ten lifecycle control points** spanning data, model, RAG, agent, and runtime—not only a threat taxonomy | [Chapter 6](06-pipeline.md) |
| 2 | **Separation of evidence-producing steps from blocking release decisions** (control points 4, 7, 8 vs integrity at 9) | [Chapter 6 — Release decision model](06-pipeline.md#release-decision-model) |
| 3 | **`Evidence Pack` as the auditable output per release**—one bundle tying data, tests, policy, and runtime evidence | [Chapter 11](11-governance-evidence.md#what-is-an-evidence-pack) |
| 4 | **Unified thread** from threat modeling through runtime, SOC, and governance in one lifecycle—not siloed LLM, agent, or MLOps docs | Ch.2 → 6 → 7/8 → 10 → 11; [Appendix E](17-appendix-e-implementation-reference.md) |

For architecture-specific controls, decision matrices, templates, and playbooks, use [Appendix E: Implementation Reference](17-appendix-e-implementation-reference.md).

> *Refs - This guide: [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6); [Evidence Pack](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11). Author note: The four contributions in the table are this guide's own positioning relative to OWASP, OpenSSF, and NIST - an author claim, not an external assessment.*

## Assumed foundations and what this guide does not cover

This guide is an **AI security implementation layer**. It assumes - and does not itself provide - the following foundations:

- **A general information security management system (ISMS).** ISO/IEC 27001 clauses 4-10 (context, security policy, risk treatment and Statement of Applicability, internal audit, management review, corrective action) and its non-technical Annex A themes (people/HR security, physical security, business continuity and backup, cryptography policy) are **prerequisites**, not contents of this guide.
- **An AI management system (AIMS).** ISO/IEC 42001 clauses 4-10 - AI policy, AI system impact assessment, objectives, competence, internal audit, management review, nonconformity - sit above this guide's technical controls.
- **AI risk beyond security.** This guide manages **security risk** (attacker -> asset -> control), which is one subset of AI risk. Fairness, safety, societal and environmental impact, fundamental-rights, accountability, and explainability risks must be managed through ISO/IEC 23894 and ISO/IEC 42001.

Framework alignment in this guide is **thematic, not a clause-by-clause conformance mapping**. Regulatory obligations it does **not** cover include, for the EU AI Act: prohibited practices (Art. 5), high-risk classification (Art. 6 / Annex III), conformity assessment and CE marking (Art. 43/47/48), EU-database registration (Art. 49), fundamental-rights impact assessment (Art. 27), synthetic-content transparency (Art. 50), GPAI / systemic-risk obligations (Art. 51-55), serious-incident reporting (Art. 73), and the quality management system (Art. 17). Use the named standards and your legal/compliance process for those.

> *Refs - Frameworks: ISO/IEC 27001 (ISMS); ISO/IEC 42001 (AIMS); ISO/IEC 23894 (AI risk management); EU AI Act (Regulation (EU) 2024/1689). Author note: This scope boundary is the author's positioning; the named standards are the authoritative sources for the excluded obligations.*

## How to use this guide

Readers are not expected to read every chapter sequentially. Use the paths below based on role and architecture—not every chapter applies to every deployment.

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

> *Refs - This guide: [Reading paths](TABLE-OF-CONTENTS.md#reading-paths); [Appendix E](17-appendix-e-implementation-reference.md); [GETTING-STARTED.md](../GETTING-STARTED.md). Author note: Role-based reading paths are this guide's navigation aid, not a framework requirement.*

## Why DevSecOps Is Insufficient

| Characteristic | Security impact |
|---|---|
| Heavy dependence on data | Data quality, privacy, and integrity directly determine model behavior. |
| Probabilistic behavior | A successful test does not guarantee the same attack will not recur in `Production`. |
| Broad attack surface | In addition to code, data, models, `Artifact`s, prompts, memory, tools, and `Retrieval` are also attackable. |
| Environmental variability | `Data Drift`, dependency changes, and shifts in user patterns can turn a secure model yesterday into an insecure one today. |

Probabilistic behavior in AI systems creates a serious security difference. In classic software, identical input usually yields identical output; but in AI models, the same prompt or the same data can produce different responses depending on conversation context, model settings such as `temperature`, model version, or data retrieved in `RAG`. From a security perspective, this means a successful test does not guarantee an attack will recur in `Production`; many attacks such as `Prompt Injection` take effect only in a specific combination of context—not like classic `SQL Injection` with a fixed, fully predictable input.

`MLSecOps` means security is not just a step before release. Security must be applied at every decision point in the model lifecycle: when data enters, when a base model is selected, during training, evaluation, signing, deployment, when user requests are received, when tools are invoked, when documents are retrieved, and when model behavior is monitored.

> *Refs - Frameworks: NIST AI RMF: characteristics of AI risk vs traditional software (Map function); OWASP AI Exchange: [AI security overview](https://owaspai.org/go/about/). This guide: [Relationship between MLSecOps and DevSecOps](#relationship-between-mlsecops-and-devsecops).*

## AI Threat Surface (Executive Overview)

Threats in AI systems span multiple layers—not only application code. The overview below orients security teams before detailed analysis in later chapters.

| Layer | Example risks |
|---|---|
| Data | `Data Poisoning`, sensitive data leakage, training data extraction |
| Model | `Backdoor`, weight tampering, model theft, `Model Inversion` |
| Application | `Prompt Injection`, `RAG`/`Retrieval Poisoning`, `Tool Misuse`/`Tool Abuse` (`ASI02`), MCP tool poisoning, unsafe output handling |
| Governance (parallel) | Shadow AI (unsanctioned LLM use), ungoverned MCP in IDE - controls: AI-AUP, enterprise gateway, MCP allowlist ([Ch.11](11-governance-evidence.md#shadow-ai-governance), [Ch.7 MCP](07-llm-rag-security.md#model-context-protocol-mcp-security)) |
| Infrastructure | Open K8s namespace, unsigned images, GPU memory leak - controls: RBAC, NetworkPolicy, signing verify ([Ch.16](16-kubernetes-deployment-reference.md)) |
| Runtime | `Data Drift`, evasion, guardrail bypass, unmonitored agent actions |

> Autonomous/offensive AI threats: [Chapter 3](03-threat-landscape.md). Agent reference architecture, six-domain attack surface, and controls: [Chapter 8](08-agentic-ai-security.md).

> *Refs - Frameworks: OWASP LLM Top 10 (2025): `LLM01` prompt injection, `LLM03` supply chain; MITRE ATLAS: tactic/technique layers map to rows above - [Chapter 12 ATLAS table](12-threat-control-tools-map.md#mitre-atlas-mapping); OWASP Agentic: `ASI02` tool misuse. This guide: [Attack surface matrix](02-scope-risk-threat-model.md#attack-surface-matrix) (Chapter 2).*

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

> *Refs - Frameworks: NIST AI RMF: Govern / Map / Measure / Manage (principles 1-3, 6); OpenSSF MLSecOps whitepaper (2025): supply-chain traceability (principle 4). Author note: The six-principle formulation is this guide's synthesis; the underlying requirements derive from the frameworks above.*

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
*Figure - How MLSecOps extends the DevSecOps foundation to AI-specific assets and supply-chain evidence such as SBOM and AI-BOM.*

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): MLOps vs MLSecOps asset comparison; SPDX / CycloneDX: SBOM and `AI-BOM` profile work. This guide: [SBOM and AI-BOM](05-model-artifact-supply-chain.md#sbom-and-ai-bom) (Chapter 5).*

## Lifecycle Overview

The following lifecycle provides the conceptual foundation for the remainder of this guide.

![](../assets/diagrams/01-intro_02.png)
*Figure - The end-to-end MLSecOps lifecycle stages, from data ingest through runtime and SOC, that structure the rest of this guide.*

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

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): lifecycle stages - mapped in [Chapter 11](11-governance-evidence.md#openssf-mlsecops-mapping-whitepaper-2025). This guide: [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6) - the 10-point model in the mapping table is this guide's operational layer.*

## Relationship to OWASP projects

This guide is designed to complement—not replace—existing OWASP AI security work:

| OWASP project | Primary role | How this guide uses it |
|---|---|---|
| **`OWASP AI Exchange`** | Comprehensive threat, control, and testing framework for all AI types | Used as the primary OWASP taxonomy and control reference; this guide maps Exchange threats to lifecycle control points, release gates, and `Evidence Pack` fields |
| `OWASP Top 10 for LLM Applications` | Threat categories for LLM applications | Used as a threat taxonomy for prompt injection, data leakage, supply chain, agentic risk, and runtime controls |
| `OWASP LLMSVS` / `AISVS` | Verification requirements and test expectations | Used as verification references; this guide does not redefine detailed test procedures |
| `OWASP MCP Top 10` and MCP Security Cheat Sheet | MCP-specific risks and mitigations | Used for MCP gateway, tool schema, shadow MCP, and tool-output control guidance |
| `OWASP Agentic Security Initiative` | Agentic threat taxonomy and controls | Used for tool misuse, intent gates, memory poisoning, and multi-agent boundaries |
| `OWASP Machine Learning Security Top 10` | Classic ML threat categories | Referenced as draft/working terminology until finalized |

The contribution of this guide is the **lifecycle view**: selecting and sequencing controls across data, model, supply chain, RAG, agents, runtime, SOC, and governance. It is not a replacement for OWASP verification standards, tool documentation, or legal/compliance review.

> *Refs - Frameworks: OWASP AI Exchange; OWASP Top 10 for LLM Applications (2025); OWASP LLMSVS / AISVS; OWASP MCP Top 10; OWASP Agentic Security Initiative; OWASP ML Top 10 (draft) - project links in [Chapter 15 References](15-conclusion-appendix.md#references).*

## Relationship to OWASP AI Exchange

The [OWASP AI Exchange](https://owaspai.org) is the OWASP Flagship resource for AI security and privacy fundamentals: threats, controls, testing methodology, and alignment with standards such as ISO/IEC 27090. This guide **builds on** the Exchange—it does not duplicate it.

| Question | Use **OWASP AI Exchange** | Use **this guide** |
|---|---|---|
| What threats and controls exist for my AI system? | Threat matrix, periodic table, risk-analysis decision tree | — |
| How do I test prompt injection or adversarial robustness in depth? | AI security testing procedures and tool reviews | Control point 7 acceptance criteria + tool examples in Ch.12 |
| How do I run an AI program or full privacy/GDPR program? | GUARD steps, AI privacy chapter | Shadow AI ops (Ch.11); operational data controls (Ch.4) |
| How do I implement MLSecOps in CI/CD and production? | General control descriptions | Ten lifecycle control points, release gates, `Evidence Pack`, Appendix E |
| Where is my evidence and who blocks release? | Control rationale | Control points 4, 7, 8, 9 and auditable bundle (Ch.11) |

**Practical division of labor:** start threat and control selection in the Exchange (or its [risk analysis](https://owaspai.org/go/riskanalysis/) section), then implement and evidence the chosen controls using this guide's lifecycle model. Per-section **References / Source mapping** blocks cite Exchange topics alongside guide sections as traceability rolls out across chapters.

> *Refs - Frameworks: [OWASP AI Exchange - About](https://owaspai.org/go/about/); [AI at OWASP - positioning](https://owaspai.org/go/aiatowasp/); [Risk analysis](https://owaspai.org/go/riskanalysis/); [Periodic table of AI security](https://owaspai.org/go/periodictable/). This guide: [What this guide adds](#what-this-guide-adds-beyond-owasp-openssf-and-nist); [Traceability convention](15-conclusion-appendix.md#traceability-and-source-mapping-convention) (Chapter 15); [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6); [When to use which resource](../GETTING-STARTED.md#when-to-use-this-guide-vs-owasp-ai-exchange) (`GETTING-STARTED.md`).*

## Focus of this guide and distinction from AISecOps

This guide focuses specifically on `MLSecOps`: securing the full lifecycle of `ML/AI` systems from data and training through artifacts, lifecycle controls, deployment, runtime, and monitoring.

`MLSecOps` must not be confused with the similar term `AISecOps`, because these are two different domains:

| Term | Definition | Central question |
|---|---|---|
| `MLSecOps` | Security of the model lifecycle and AI systems (subject of this guide) | "How do I build, release, and run an AI system securely?" |
| `AISecOps` | Using artificial intelligence within security operations itself—employing AI for threat detection, alert triage, analysis, and automated response in the `SOC` (per NSFOCUS definition, combining `AIOps` + `AISec` + `SecOps`) | "How do I use AI to automate security operations?" |

In simple terms: `MLSecOps` means "securing AI," while `AISecOps` means "using AI for security." This guide is entirely within the `MLSecOps` domain and does not enter the realm of `AISecOps`; although in Chapter 10, which addresses integration with the `SOC`, the practical point of contact between these two domains is shown.

In short, `MLSecOps` applies the same logic as `DevSecOps`, but for securing data, models, lifecycle decision points, `Runtime`, and the behavior of AI systems—not just code and infrastructure.

> *Refs - Frameworks: NSFOCUS: `AISecOps` definition (AIOps + AISec + SecOps). This guide: [SOC integration](10-monitoring-soc-ir.md#soc-integration) (Chapter 10) - the practical contact point between MLSecOps and AISecOps.*
