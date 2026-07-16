# Chapter 2: Scope, Audience, and Threat Model

## Scope of the article

This article is written for organizations that develop, deploy, or maintain `ML` or `AI` systems in operational environments. These systems may range from classic tabular and computer vision models to `LLM`s, `RAG` architectures, multi-tenant services, and intelligent agents.

`MLSecOps` is not a one-size-fits-all approach for every organization. Security controls must be selected based on architecture, data sensitivity, model type, model access level, user types, compliance requirements, and likely threats.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Govern / Map (context and scope)
- ISO/IEC 42001: scope of the AI management system

**Implementation guidance (this guide)**
- [Scenarios covered](#scenarios-covered)
- [Selecting controls based on threat model](#selecting-controls-based-on-threat-model)

## Scenarios covered

The scope of the article can be explained more clearly through several specific scenarios. These scenarios show that the attack surface differs for each type of system:

| Scenario | Security focus |
|---|---|
| Classic `ML` models | Data integrity, `Artifact` security, `Adversarial` attacks, and protection of training and deployment pipelines |
| `LLM` and `RAG` systems | `Runtime` risks such as `Prompt Injection`, `Retrieval Poisoning`, data leakage, and unsafe output |
| Managed AI services | Shared responsibility for Azure OpenAI, Amazon Bedrock, Vertex AI, or similar APIs; customer-side controls such as gateway, data boundary, key management, logging, and RAG authorization |
| `Agentic AI` | Tools, memory, automated workflows, inter-agent communication, and risks such as `Tool Misuse`/`Tool Abuse` (`ASI02`) and privilege escalation — see [Chapter 8 reference architecture and six-domain model](08-agentic-ai-security.md#agent-reference-architecture) |
| `MCP` tool servers and IDE agents | Tool poisoning, shadow MCP (`MCP09`), schema rug-pull, token exposure — see [Chapter 7 — MCP security](07-llm-rag-security.md#model-context-protocol-mcp-security) |
| Shadow AI (unsanctioned LLM use) | Data exfiltration via consumer ChatGPT/Copilot, personal API keys, ungoverned browser extensions — see [Chapter 11 — Shadow AI governance](11-governance-evidence.md#shadow-ai-governance) |
| Enterprise and multi-tenant architectures | Tenant isolation, access control, network segmentation, inference isolation, and data governance — see [Chapter 16](16-kubernetes-deployment-reference.md) for K8s patterns |
| `Edge / IoT / TinyML` | Resource constraints, physical device security, secure model updates (`OTA`), and on-device model protection |
| Cyber-physical systems (`CPS/ICS`) | Safety impact, adversarial attacks on sensors, and decision integrity in industrial control |

For `Edge`, `IoT`, and `CPS` systems, in addition to the controls in this guide, physical risks, safety, and resource constraints must be assessed separately using specialized frameworks; these scenarios are **out of scope for this version's control set** and are listed here only for completeness. This guide primarily focuses on cloud-native and enterprise architectures.

> **Risk scope:** This guide manages **security risk**. **Safety** (harm to people, property, or the environment) is a first-class AI risk source under ISO/IEC 23894 that this guide **defers** rather than covers - it is not absent because it is unimportant. Assess safety, fairness, and societal/fundamental-rights risk through ISO/IEC 23894 and ISO/IEC 42001 alongside the security controls here.

**Out of scope for v1.1.1:** localized non-English editions; full legal interpretation of sector regulations; hardware TEE/confidential-GPU deployment patterns (see vendor docs); exhaustive Shadow-AI or MCP product catalog. **Shadow AI governance** (Ch.11), **MCP security** (Ch.7), and **Kubernetes deployment reference** (Ch.16) are in scope as operational patterns - not as vendor surveys. Case studies: [Chapter 13](13-case-studies.md).

Not every topic in this guide is equally mandatory for every team. For example, numerical `Adversarial Robustness` tests are highly important for `Tabular` or `Vision` models, but for a `Pure LLM API` without proprietary data, some of that work has more limited applicability.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [threats overview](https://owaspai.org/go/threatsoverview/) - threat applicability varies by AI type
- OWASP LLM Top 10 (2025)
- OWASP Agentic (`ASI02`)
- OWASP MCP Top 10 (`MCP09`) - scenario rows above

**Implementation guidance (this guide)**
- [Attack surface matrix](#attack-surface-matrix)
- [Chapter 8](08-agentic-ai-security.md), [Chapter 11 Shadow AI](11-governance-evidence.md#shadow-ai-governance), [Chapter 16](16-kubernetes-deployment-reference.md)

### Managed AI service scope

Many organizations consume AI through managed services rather than training and hosting model weights directly. In these cases, the organization usually cannot sign or scan the provider's base model weights. MLSecOps still applies, but the evidence changes:

| Provider-managed area | Customer-managed area |
|---|---|
| Base model weights, provider training infrastructure, provider-side model patching | Prompt and system instruction design, RAG sources, tenant authorization, gateway policy, logging, DLP, key management, incident response, vendor configuration review |
| Provider content safety features and platform logs, where available | Verification that provider controls are enabled, configured, monitored, and included in the organization's evidence record |

For managed AI APIs, the organization should document the shared-responsibility boundary in the threat model. When model signing or artifact scanning is not possible, collect alternative evidence such as approved model/service identifier, region, tenant, API version, configuration snapshot, access policy, gateway controls, red-team test results, and runtime telemetry.

## Managed AI services security reference

Organizations that consume Azure OpenAI, Amazon Bedrock, Google Vertex AI, or similar APIs rarely control base model weights. MLSecOps still applies on the **customer side** of the shared-responsibility boundary. Use this section when [Chapter 6](06-pipeline.md) control points 5–9 refer to "configure" or "integrity evidence" instead of train/sign.

### Customer control stack

| Layer | What to control | Lifecycle control points | Guide reference |
|---|---|---|---|
| Identity and access | API keys, OAuth, RBAC, tenant isolation | 1, 3, 8 | [Ch.5 secrets](05-model-artifact-supply-chain.md), [Ch.16](16-kubernetes-deployment-reference.md) |
| Data boundary | What may enter prompts/RAG; DLP on ingress/egress | 4, 7, 10 | [Ch.4](04-data-security-privacy.md), [Ch.7 gateway](07-llm-rag-security.md) |
| Configuration | Approved model/deployment ID, region, API version, safety settings | 5, 8, 9 | [Evidence Pack](11-governance-evidence.md#what-is-an-evidence-pack) |
| RAG on managed API | Ingest ACL, retrieval authz, re-index on source change | 4, 5, 7 | [Ch.7 RAG](07-llm-rag-security.md#secure-architecture-for-rag) |
| Runtime | Gateway, guardrails, logging, rate limits | 10 | [Ch.7](07-llm-rag-security.md), [Ch.10 SOC](10-monitoring-soc-ir.md) |
| Agents on managed models | Scoped tools, Intent Gate, MCP allowlist | 7, 10 | [Ch.8](08-agentic-ai-security.md) |

### Evidence when you cannot sign model weights

| Instead of… | Record… |
|---|---|
| Model weight hash + signature | Approved provider, model/deployment name, region, API version, configuration snapshot |
| Training data lineage | RAG source manifest, ingest approvals, index version |
| Backdoor scan on weights | Prompt-injection suite, RAG leakage tests, output policy tests ([Ch.7 verification](07-llm-rag-security.md#llm-verification-approach)) |
| Registry promotion | Documented release decision at control points **4, 7, 8** plus configuration evidence at **9** |

### Minimum baseline for managed AI

1. Enterprise gateway or proxy in front of provider API (no raw keys in apps).
2. DLP on prompt ingress and response egress.
3. RAG ingest allowlist and ACL at retrieval.
4. Runtime logging to SIEM with retention policy.
5. Documented shared-responsibility record in threat model and `Evidence Pack`.

Extended checklist: [Appendix D — Managed AI Services](15-conclusion-appendix.md#appendix-d-managed-ai-services-security-reference).

### References / Source mapping

**Frameworks and standards**
- Cloud provider shared-responsibility models (Azure OpenAI, Amazon Bedrock, Google Vertex AI - vendor documentation)
- ISO/IEC 42001: supplier and third-party AI service themes

**Implementation guidance (this guide)**
- [Appendix D - Managed AI Services](15-conclusion-appendix.md#appendix-d-managed-ai-services-security-reference) (Chapter 15)
- [Lifecycle control points 5-9 in configure mode](06-pipeline.md#lifecycle-control-points) (Chapter 6)

**Author practical guidance**
- *The customer control stack and evidence substitution table are implementation patterns, not provider requirements*

## Primary audiences

| Audience | Primary need |
|---|---|
| `ML` and `MLOps` teams | Building secure pipelines, model testing, and `Artifact` control |
| Security teams | Threat modeling, defining lifecycle release decision criteria, and monitoring AI attacks |
| Platform teams | Infrastructure isolation, access control, and secure integration with `CI/CD` |
| Governance and risk teams | Recording evidence, framework compliance, and risk management |
| Product teams | Understanding limitations, user risks, and secure release requirements |

### References / Source mapping

**Implementation guidance (this guide)**
- [How to use this guide](01-intro.md#how-to-use-this-guide) (Chapter 1)
- [Reading paths](TABLE-OF-CONTENTS.md#reading-paths)

## Selecting controls based on threat model

Not all controls are necessary for all systems. `Federated Learning` security matters when federated learning is actually used. Complex controls for `Multi-Agent` systems make sense when agents can invoke real, sensitive tools. `Transparency Log` and advanced `Attestation` chains are more valuable in organizations with serious audit and defensible supply chain requirements.

In many projects, a few simple but correctly implemented controls are worth more than heavy, incomplete architectures:

- Data and `Artifact` scanning
- Model signing and `Provenance` recording
- Release decision enforcement
- Access control at `Runtime`
- Evidence recording in `Evidence Pack`

The goal of `MLSecOps` is not to add more tools; the goal is to select controls that match architecture, risk, and the team's operational capacity.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [risk analysis](https://owaspai.org/go/riskanalysis/) - control selection follows threat applicability
- NIST AI RMF: Map (context-driven risk prioritization)

**Author practical guidance**
- *The "few simple controls over heavy incomplete architectures" position is this guide's operational opinion*

## AI system inventory

Before threat modeling or lifecycle controls apply, the organization must know **which AI systems exist**. Maintain one inventory that covers both **sanctioned** production systems (in scope for Chapter 6) and **shadow** tools (parallel track in [Chapter 11](11-governance-evidence.md#shadow-ai-governance)).

| Field | Sanctioned system | Shadow / unsanctioned tool |
|---|---|---|
| Name / ID | Service or product identifier | Tool name (e.g. consumer ChatGPT, IDE MCP) |
| Architecture | Classic ML, LLM, RAG, agent, managed API | Browser, desktop, personal API key |
| Data sensitivity | Max classification processed | Risk if prod data pasted |
| Owner | Engineering + security contact | Discovery source (CASB, survey) |
| Lifecycle path | MLSecOps control points 1–10 | AI-AUP, gateway, block/allow policy |
| Threat model ref | Versioned document + `Evidence Pack` | Recorded risk acceptance or remediation |

Record the inventory at control point 1 (`Initiate Change`) and refresh when new services, RAG sources, agents, or MCP servers are introduced. Shadow AI discovery steps remain in Chapter 11; this inventory **links** sanctioned and shadow rows so governance and MLSecOps teams share one view.

### References / Source mapping

**Frameworks and standards**
- [AI program / inventory](https://owaspai.org/go/aiprogram/)
- [How to organize AI security (GUARD)](https://owaspai.org/go/organize/)

**Implementation guidance (this guide)**
- [Lifecycle control point 1](06-pipeline.md#lifecycle-control-points) (Chapter 6)
- [Shadow AI governance](11-governance-evidence.md#shadow-ai-governance) (Chapter 11)
- [Threat model template](17-appendix-e-implementation-reference.md#e3-threat-model-template) (Appendix E.3)

## Risk management

Risk management determines which assets matter most to the organization, what level of risk is acceptable, and which legal or organizational requirements must be met. Frameworks such as `NIST AI RMF`, `ISO/IEC 42001`, `ISO/IEC 23894`, and the `EU AI Act` are used at this level.

Threat modeling is a more technical layer. At this stage, it is determined how an attacker can approach the system, which components lie on the attack surface, and which controls must be applied to data, pipeline, model, `Runtime`, or infrastructure.

At this layer, resources such as `OWASP ML Top 10`, `OWASP LLM Top 10`, `OWASP MCP Top 10`, `MITRE ATLAS`, and methods such as `STRIDE` are typically used so threats can be described in a shared technical and operational language. Include **Shadow AI**, **MCP servers**, and **Kubernetes inference** rows from the [attack surface matrix](#attack-surface-matrix) when they apply to your architecture.

### MLSecOps risk analysis workflow

Use this operational workflow after the [AI system inventory](#ai-system-inventory) is current. It connects governance risk management with lifecycle release decisions—not a replacement for organizational risk registers or legal review.

| Step | Action | Output for MLSecOps |
|---|---|---|
| 1. Scope | Confirm architecture, data class, managed vs self-hosted, agents/MCP | Inventory row + attack surface rows |
| 2. Identify threats | Map assets to threats (Exchange decision tree, OWASP Top 10, ATLAS) | Threat list per component |
| 3. Select controls | Choose mandatory controls; map to control points 2–10 | Control matrix in threat model |
| 4. Estimate risk | Likelihood × impact per threat; note supplier vs customer responsibility | Residual risk register |
| 5. Define blockers | Set release blockers at points **4, 7, 8, 9** and test thresholds | Versioned threat model |
| 6. Record evidence | Specify `Evidence Pack` fields per control | Template in Appendix E.4 |
| 7. Monitor | Re-assess on architecture change, CT, index update, or incident | Updated threat model version |

For threat identification, the [OWASP AI Exchange threat-model decision tree](https://owaspai.org/go/threatmodel/) narrows which Exchange threats apply; record the chosen threats in the threat model and implement controls through this guide's lifecycle.

> Version note: `OWASP LLM Top 10` version 2025 has been published and finalized, but `OWASP Machine Learning Security Top 10` remains in draft status (approximately version `v0.3`). Therefore, identifiers `ML01`–`ML10` in this guide are used as working references and may change in the final OWASP release.

### References / Source mapping

**Frameworks and standards**
- [Risk analysis](https://owaspai.org/go/riskanalysis/)
- [Threat modeling decision tree](https://owaspai.org/go/threatmodel/)
- [Threats overview](https://owaspai.org/go/threatsoverview/)

**Implementation guidance (this guide)**
- [Attack surface matrix](#attack-surface-matrix)
- [Expected output of threat modeling](#expected-output-of-threat-modeling)
- [STRIDE and FMEA](11-governance-evidence.md#stride-and-fmea-applied-to-ml-assets) (Chapter 11)

## Attack surface matrix

| Attack surface | Example threat | Recommended control |
|---|---|---|
| Data | `Data Poisoning`, data leakage, quality weakness | Validation, `PII Masking`, `Lineage` |
| Model | `Backdoor`, model theft, `Model Inversion` | Security testing, signing where the organization controls artifacts, access control |
| Managed AI API | Provider misconfiguration, unsafe prompt path, weak tenant boundary, unmanaged API keys | Shared-responsibility record, gateway, DLP, key proxy, vendor configuration review |
| Supply chain | Poisoned model or package, `Typosquatting` | `SBOM`, `AI-BOM`, `Allowlist`, scanning |
| `RAG` | `Retrieval Poisoning`, document disclosure | `Ingest` control, tenant isolation, leakage testing |
| Intelligent agent | Tool misuse/abuse (`ASI02`), privilege escalation, memory poisoning, poisoned files | Six-domain agent model, `Intent Gate`, scoped tools, HITL — [Ch.8](08-agentic-ai-security.md#agent-attack-surface) |
| MCP / IDE tools | Tool poisoning, shadow MCP (`MCP09`), schema rug-pull | MCP gateway, allowlist, `mcps-audit` / Agent Scan — [Ch.7](07-llm-rag-security.md#model-context-protocol-mcp-security) |
| Shadow AI | Paste of prod data into consumer LLM, personal API keys | AI-AUP, enterprise gateway, CASB/DLP — [Ch.11](11-governance-evidence.md#shadow-ai-governance) |
| Infrastructure / K8s | Open namespace, unsigned images, GPU memory leak | RBAC, NetworkPolicy, Kyverno, MIG — [Ch.16](16-kubernetes-deployment-reference.md) |
| Execution | `Prompt Injection`, unsafe output | `Gateway`, `Guardrail`, logging and monitoring |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01`, `LLM02`, `LLM03`
- OWASP ML Top 10 (draft)
- OWASP MCP Top 10: `MCP09`
- MITRE ATLAS: full technique mapping in [Chapter 12](12-threat-control-tools-map.md#mitre-atlas-mapping)
- OWASP AI Exchange: [AI security matrix](https://owaspai.org/go/aisecuritymatrix/)

**Implementation guidance (this guide)**
- Row-level deep dives: [Ch.4 data](04-data-security-privacy.md), [Ch.5 supply chain](05-model-artifact-supply-chain.md), [Ch.7 RAG/MCP](07-llm-rag-security.md), [Ch.8 agents](08-agentic-ai-security.md), [Ch.16 K8s](16-kubernetes-deployment-reference.md)

## Expected output of threat modeling

The output of threat modeling must be an actionable document, not merely a descriptive report. This document must specify:

- Which assets are critical.
- Which threats are meaningful for the actual system architecture.
- Which controls are mandatory.
- Which criteria cause model release to be blocked.
- What evidence must be stored for audit.

### References / Source mapping

**Frameworks and standards**
- [Risk analysis - risk treatment and residual risk](https://owaspai.org/go/riskanalysis/)

**Implementation guidance (this guide)**
- [MLSecOps risk analysis workflow](#mlsecops-risk-analysis-workflow)
- [Threat model template](17-appendix-e-implementation-reference.md#e3-threat-model-template) (Appendix E.3)
- [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6)
