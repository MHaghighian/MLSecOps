# Chapter 2: Scope, Audience, and Threat Model

<div dir="ltr">

## Scope of the article

This article is written for organizations that develop, deploy, or maintain `ML` or `AI` systems in operational environments. These systems may range from classic tabular and computer vision models to `LLM`s, `RAG` architectures, multi-tenant services, and intelligent agents.

`MLSecOps` is not a one-size-fits-all approach for every organization. Security controls must be selected based on architecture, data sensitivity, model type, model access level, user types, compliance requirements, and likely threats.

## Scenarios covered

The scope of the article can be explained more clearly through several specific scenarios. These scenarios show that the attack surface differs for each type of system:

| Scenario | Security focus |
|---|---|
| Classic `ML` models | Data integrity, `Artifact` security, `Adversarial` attacks, and protection of training and deployment pipelines |
| `LLM` and `RAG` systems | `Runtime` risks such as `Prompt Injection`, `Retrieval Poisoning`, data leakage, and unsafe output |
| `Agentic AI` | Tools, memory, automated workflows, inter-agent communication, and risks such as `Tool Abuse` and privilege escalation |
| Enterprise and multi-tenant architectures | Tenant isolation, access control, network segmentation, inference isolation, and data governance |
| `Edge / IoT / TinyML` | Resource constraints, physical device security, secure model updates (`OTA`), and on-device model protection |
| Cyber-physical systems (`CPS/ICS`) | Safety impact, adversarial attacks on sensors, and decision integrity in industrial control |

For `Edge`, `IoT`, and `CPS` systems, in addition to the controls in this article, physical risks, safety, and resource constraints must be assessed separately using specialized frameworks. This guide primarily focuses on cloud-native and enterprise architectures.

Not every topic in this article is equally mandatory for every team. For example, numerical `Adversarial Robustness` tests are highly important for `Tabular` or `Vision` models, but for a `Pure LLM API` without proprietary data, some of that work has more limited applicability.

## Primary audiences

| Audience | Primary need |
|---|---|
| `ML` and `MLOps` teams | Building secure pipelines, model testing, and `Artifact` control |
| Security teams | Threat modeling, defining `Security Gate`s, and monitoring AI attacks |
| Platform teams | Infrastructure isolation, access control, and secure integration with `CI/CD` |
| Governance and risk teams | Recording evidence, framework compliance, and risk management |
| Product teams | Understanding limitations, user risks, and secure release requirements |

## Selecting controls based on threat model

Not all controls are necessary for all systems. `Federated Learning` security matters when federated learning is actually used. Complex controls for `Multi-Agent` systems make sense when agents can invoke real, sensitive tools. `Transparency Log` and advanced `Attestation` chains are more valuable in organizations with serious audit and defensible supply chain requirements.

In many projects, a few simple but correctly implemented controls are worth more than heavy, incomplete architectures:

- Data and `Artifact` scanning
- Model signing and `Provenance` recording
- `Policy Gate` enforcement
- Access control at `Runtime`
- Evidence recording in `Evidence Pack`

The goal of `MLSecOps` is not to add more tools; the goal is to select controls that match architecture, risk, and the team's operational capacity.

## Risk management

Risk management determines which assets matter most to the organization, what level of risk is acceptable, and which legal or organizational requirements must be met. Frameworks such as `NIST AI RMF`, `ISO/IEC 42001`, `ISO/IEC 23894`, and the `EU AI Act` are used at this level.

Threat modeling is a more technical layer. At this stage, it is determined how an attacker can approach the system, which components lie on the attack surface, and which controls must be applied to data, pipeline, model, `Runtime`, or infrastructure.

At this layer, resources such as `OWASP ML Top 10`, `OWASP LLM Top 10`, `MITRE ATLAS`, and methods such as `STRIDE` are typically used so threats can be described in a shared technical and operational language.

> Version note: `OWASP LLM Top 10` version 2025 has been published and finalized, but `OWASP Machine Learning Security Top 10` remains in draft status (approximately version `v0.3`). Therefore, identifiers `ML01`–`ML10` in this article are used as working references and may change in the final version.

## Attack surface matrix

| Attack surface | Example threat | Recommended control |
|---|---|---|
| Data | `Data Poisoning`, data leakage, quality weakness | Validation, `PII Masking`, `Lineage` |
| Model | `Backdoor`, model theft, `Model Inversion` | Security testing, signing, access control |
| Supply chain | Poisoned model or package, `Typosquatting` | `SBOM`, `AI-BOM`, `Allowlist`, scanning |
| `RAG` | `Retrieval Poisoning`, document disclosure | `Ingest` control, tenant isolation, leakage testing |
| Intelligent agent | Tool abuse, privilege escalation | `Intent Gate`, tool restriction, human approval |
| Execution | `Prompt Injection`, unsafe output | `Gateway`, `Guardrail`, logging and monitoring |

## Expected output of threat modeling

The output of threat modeling must be an actionable document, not merely a descriptive report. This document must specify:

- Which assets are critical.
- Which threats are meaningful for the actual system architecture.
- Which controls are mandatory.
- Which criteria cause model release to be blocked.
- What evidence must be stored for audit.

</div>
