# Chapter 6: MLSecOps Lifecycle Control Model

> **Filename note:** This chapter is stored as `06-pipeline.md` for link stability. The content describes the **lifecycle control model**, not a reference CI/CD pipeline implementation.

## Control model objective

The `MLSecOps` lifecycle control model defines where security decisions, evidence collection, and review activities should occur across an AI system lifecycle. The goal is that no model, data, prompt template, `RAG` index, agent configuration, or other AI `Artifact` enters an operational environment without appropriate risk-based controls and auditable evidence.

This chapter is **not** a reference CI/CD implementation. It describes implementation-neutral control points that organizations may apply through MLOps platforms, CI/CD, manual approval workflows, managed AI service governance, or a combination of these mechanisms.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: lifecycle governance across Map / Measure / Manage
- ISO/IEC 42001: AI management system lifecycle controls

**Implementation guidance (this guide)**
- [Lifecycle control points](#lifecycle-control-points); [Golden rule](#golden-rule)

## Control model overview

The model begins with prerequisite `Planning` and `Threat Modeling`, then defines ten lifecycle control points from change initiation to storage and monitoring. **Not every control point is a blocking gate.** Some points produce evidence; others are explicit release decisions. The exact automation level depends on organizational maturity and architecture.

### References / Source mapping

**Frameworks and standards**
- [OpenSSF Secure MLOps whitepaper (2025)](https://openssf.org/wp-content/uploads/2025/08/OpenSSF_MLSecOps_Whitepaper.pdf): lifecycle visualization baseline
- NIST AI RMF: integrated risk management across lifecycle stages

**Implementation guidance (this guide)**
- [Prerequisite: Planning and Threat Modeling](#prerequisite-planning-and-threat-modeling); [Lifecycle control points](#lifecycle-control-points)

## Prerequisite: Planning and Threat Modeling

Before a release, retrain, index change, managed-model configuration change, or agent/tool change is approved, several activities must be completed; otherwise later decision points will lack precise criteria:

- Precise definition of system scope including data, model, API, `RAG`, agent, **MCP servers**, and **Shadow AI** usage (see [Ch.2 attack surface](02-scope-risk-threat-model.md#attack-surface-matrix))
- Threat modeling with `OWASP ML/LLM Top 10` and `MITRE ATLAS`
- Selection of mandatory controls and acceptable risk level
- Versioned recording of threat model output in `Evidence Pack`



### References / Source mapping

**Frameworks and standards**
- OWASP ML Top 10 (draft) and OWASP LLM Top 10 (2025): threat identification baseline
- MITRE ATLAS: technique mapping for AI-specific attacks
- NIST AI RMF: Map function (context, actors, and risks)

**Implementation guidance (this guide)**
- [Attack surface matrix](02-scope-risk-threat-model.md#attack-surface-matrix) (Chapter 2); [Threat landscape](03-threat-landscape.md) (Chapter 3)
- [Release decision model](#release-decision-model)

![](../assets/diagrams/06-pipeline_01.png)


## Lifecycle control points

| # | Control point | Security objective | Evidence / output |
|---|---|---|---|
| 1 | `Initiate Change` | Reliable and authorized start of a release, retrain, index update, or managed-service configuration change | Change record and scope |
| 2 | `Load Artifacts` | Secure loading of data, base model, and dependencies | `Manifest` and hashes |
| 3 | `Security & Quality Review` | Review code, data, model, dependencies, infrastructure, and managed-service configuration | Vulnerability and quality report |
| 4 | `Data / Artifact Decision Point` | Stop or escalate before training/configuration if high risk | `Go/No-Go` or exception decision |
| 5 | `Train or Configure` | Training, fine-tuning, RAG index update, or managed-model configuration in a traceable environment | Trained model, configuration record, or experiment log |
| 6 | `Evaluate Model` | Performance, fairness, and baseline evaluation | Evaluation report |
| 7 | `Security Validation` | Attack, backdoor, prompt injection, RAG leakage, and agent/tool misuse validation | Security validation report |
| 8 | `Release Decision` | Final security, business, and compliance review | Release approval, rejection, or risk acceptance |
| 9 | `Integrity and Provenance` | Model/artifact signing where applicable, managed-service configuration snapshot, provenance recording | Signature, attestation, or configuration evidence |
| 10 | `Store & Monitor` | Secure storage and monitoring activation | `Evidence Pack` and telemetry |

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps whitepaper (2025): lifecycle visualization
- NIST AI RMF: Map / Measure / Manage across lifecycle

**Implementation guidance (this guide)**
- [Appendix E.6 — Master control matrix](17-appendix-e-implementation-reference.md#e6-master-control-matrix)

## Practical notes for each control point

| Control point | Practical note |
|---|---|
| 1. `Initiate Change` | Changes should originate from trusted events such as approved merge request, authorized commit, scheduled review, managed-service configuration change, RAG source update, or manual approval. |
| 2. `Load Artifacts` | Dataset, base model, notebook, and dependencies must be loaded from authorized sources; `ModelScan`, pickle check, and manifest generation including hashes must be done before training. |
| 3. `Security & Quality Review` | Review secrets, dependencies, notebooks, containers, IaC, model artifacts, and managed-service configuration using organization-approved tooling. Tool examples are informative only; validate behavior in your environment. |
| 4. `Data / Artifact Decision Point` | This decision point should block or escalate unmasked sensitive data, critical vulnerabilities, unauthorized data sources, or poisoned artifacts. |
| 5. `Train or Configure` | Training or configuration changes must run with least privilege; parameters, prompts, RAG source versions, and managed-service settings must be recorded. |
| 6. `Evaluate Model` | In addition to accuracy, check metrics such as `F1`, fairness, initial robustness, and baseline alignment. |
| 7. `Security Validation` | Classic models, LLM/RAG systems, agents, and MCP-enabled systems need different validation methods. Use a versioned test suite and acceptance criteria defined in the threat model. |
| 8. `Release Decision` | Security policies, compliance requirements, and business risk criteria must be reviewed before release. |
| 9. `Integrity and Provenance` | Models and controlled artifacts should be signed where possible; managed AI services should instead record approved service/model identifier, region, API version, configuration snapshot, and access policy. |
| 10. `Store & Monitor` | Final artifact stored in secure repository with object lock; telemetry including prompt, tool call, response, and model version sent to `SIEM/SOC`. |

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps whitepaper: stage-by-stage security measures
- NIST SSDF: artifact review and integrity themes at build/load time

**Implementation guidance (this guide)**
- [Lifecycle control points](#lifecycle-control-points); [Release decision model](#release-decision-model)
- [Model and artifact controls](05-model-artifact-supply-chain.md) (Chapter 5)

**Author practical guidance**
- Tool examples cited in the control-point table are informative; validate scanners and policy engines in your environment before gating releases.

## Release decision model

The model distinguishes between **evidence-producing control points** and **blocking release decisions**. Blocking decisions should be explicit, documented, and risk-based. If sensitive data is unmasked, a critical vulnerability exists, security validation fails, or policy review fails, release should be stopped unless an explicit, time-bound, approved exception is recorded.

| Type | Stage | Name | Role |
|---|---|---|---|
| **Release decision** | 4 | `Data / Artifact Decision Point` | Block or escalate on poisoned data, critical vulns, unauthorized sources, or unmasked PII |
| **Security validation decision** | 7 | `Security Validation` | Block release when adversarial, red-team, RAG leakage, or agent/tool acceptance criteria fail |
| **Final release decision** | 8 | `Release Decision` | Block release when compliance, business, or operational policy fails |
| **Integrity checkpoint** | 9 | `Integrity and Provenance` | Block storage/deploy when signature, attestation, verification, or managed-service configuration evidence is missing |
| Evidence-producing control point | 1–3, 5–6, 10 | Scan/review, train/configure, evaluate, monitor | Produce evidence; findings may affect decisions at 4, 7, or 8 |

**Minimum baseline (Level 1):** decision points at **4 and 8** must be explicit and documented; **stage 7 security validation runs on every release** and results are recorded. Stage 7 becomes a **blocking decision** at Level 2+ when acceptance thresholds are defined. Integrity/provenance evidence at **9** is mandatory at all levels, using signatures where the organization controls the artifact and configuration evidence where it consumes a managed AI service.

**Full production baseline (Level 2+):** all three decision points (4, 7, 8) are blocking on every release and CT cycle unless a formal, audited exception exists.

### References / Source mapping

**Frameworks and standards**
- ISO/IEC 42001: change and release governance themes
- EU AI Act: technical documentation and logging (high-risk adjacency)

**Implementation guidance (this guide)**
- [Maturity Level 2 criteria](14-maturity-roadmap.md#level-2-operational) (Chapter 14)

## Continuous Training cycle

After deployment, the model may need retraining due to `Data Drift`, new data, or performance decline. The `Continuous Training` cycle must not have security shortcuts. Retrained models must go through the same controls as the initial model.

In every `CT` cycle, **release decision points 4, 7, and 8** and **integrity verification at control point 9** must not be bypassed. Stages 1–3, 5–6, and 10 still run in full; their outputs feed the decision points above.



### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Manage (monitoring and update of AI systems)
- ISO/IEC 42001: change and continual improvement for AI systems

**Implementation guidance (this guide)**
- [Control points in CT cycle](#control-points-in-ct-cycle); [Release decision model](#release-decision-model)
- [Continuous monitoring](10-monitoring-soc-ir.md) (Chapter 10)

![](../assets/diagrams/06-pipeline_02.png)


## CT cycle risks

| Risk | Recommended control |
|---|---|
| `Catastrophic Forgetting` | Run regression security test on fixed set |
| `Data Drift` | Statistical monitoring with defined threshold |
| `Adversarial Drift` | SOC analysis and manual review of suspicious data |
| `Model Collapse` | Limit synthetic data and monitor output diversity |
| Excessive retraining | Cap frequency and require human approval in sensitive cases |

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [Continuous validation](https://owaspai.org/go/continuousvalidation/)
- MITRE ATLAS: `AML.T0020` Poison Training Data; drift and retraining adjacency

**Implementation guidance (this guide)**
- [Difference between Data Drift and Adversarial Drift](#difference-between-data-drift-and-adversarial-drift)
- [Three categories of security testing](#three-categories-of-security-testing)

## Control points in CT cycle

| Step | Control point | Status | Description |
|---|---|---|---|
| 1 | `Initiate Change` | Automatic or manual activation | By drift monitoring system, new data arrival, or approved change request |
| 2 | `Load Artifacts` | Full execution | Load new data, base model, and dependencies |
| 3 | `Security & Quality Scan` | Full execution | Scan new data, PII detection, and dependency review |
| 4 | `Data / Artifact Decision Point` | Mandatory decision | Data validation before training/configuration; no pass means stop or escalate |
| 5 | `Train or Configure` | Full execution | Retrain or reconfigure on new data with same constraints |
| 6 | `Evaluate Model` | Full execution | Evaluate performance and fairness of retrained model |
| 7 | `Security Validation` | Mandatory security decision (blocking at Level 2+) | Adversarial, prompt injection, backdoor, and ASR acceptance tests |
| 8 | `Release Decision` | Mandatory release decision | Approve compliance policies and acceptance criteria |
| 9 | `Integrity and Provenance` | Mandatory integrity checkpoint | Digital signing where applicable, managed-service configuration snapshot, and verify before promote |
| 10 | `Store & Monitor` | Full execution | Store new version and activate monitoring |

Basic CT cycle controls include validation of new data origin and quality, rescanning artifacts and dependencies, execution of the required decision points, integrity/provenance recording, and recording results in the `Evidence Pack`.

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps whitepaper: continuous training and monitoring stages
- NIST AI RMF: Manage (post-deployment updates)

**Implementation guidance (this guide)**
- [Continuous Training cycle](#continuous-training-cycle); [Secure deployment methods for retrained models](#secure-deployment-methods-for-retrained-models)
- [Provenance and signing](05-model-artifact-supply-chain.md#provenance-and-signing) (Chapter 5)

## Secure deployment methods for retrained models

| Method | Description |
|---|---|
| `Canary Deployment` | Only 1 to 5 percent of real traffic routed to new model; security and performance metrics compared with previous version. |
| `Shadow Mode` | New model runs alongside current model but its response is not delivered to user; used only to observe behavior. |
| `Automated Rollback` | If `Prompt Injection` rate, policy error, or performance decline exceeds threshold, system reverts to previous signed model. |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01` Prompt Injection (rollback trigger)
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection
- NIST AI RMF: Manage (deployment and rollback of AI system changes)
- OpenSSF MLSecOps: safe promotion patterns for model updates

**Implementation guidance (this guide)**
- [Kubernetes deployment reference — canary and rollback](16-kubernetes-deployment-reference.md) (Chapter 16)
- [Monitoring and SOC integration](10-monitoring-soc-ir.md) (Chapter 10)

**Author practical guidance**
- Canary traffic percentages (1–5%) and rollback thresholds are examples; calibrate with SLOs and incident playbooks.

## Difference between Data Drift and Adversarial Drift

`Data Drift` is usually seen as change in feature distribution, `Embedding Drift`, or schema changes. In contrast, `Adversarial Drift` is often accompanied by spikes in suspicious prompts, abnormal tool calls, or suspicious session patterns. These two phenomena must have separate response playbooks.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [Continuous validation](https://owaspai.org/go/continuousvalidation/)
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection; `AML.T0053` AI Agent Tool Invocation (abnormal tool-call drift)

**Implementation guidance (this guide)**
- [CT cycle risks](#ct-cycle-risks); [Three categories of security testing](#three-categories-of-security-testing)
- [SOC detection and response](10-monitoring-soc-ir.md) (Chapter 10)

## Alignment with MLOps lifecycle and OpenSSF

> **OpenSSF relationship:** The [OpenSSF Secure MLOps whitepaper (August 2025)](https://openssf.org/wp-content/uploads/2025/08/OpenSSF_MLSecOps_Whitepaper.pdf) defines a visual lifecycle and security measures across nine stages. **This guide is not an OpenSSF publication.** It is a complementary community reference that maps similar lifecycle stages to **explicit release decision points (4, 7, 8)**, integrity/provenance evidence (9), and an `Evidence Pack`. See the full OpenSSF stage-to-control mapping in [Chapter 11](11-governance-evidence.md).

| Standard `MLOps` stage | Equivalent control point in this guide |
|---|---|
| `Planning and Design` | Threat modeling and scope definition |
| `Data Engineering` | Artifact loading and control point 4 decision |
| `Experimentation` | Train or configure and experiment recording |
| `ML Pipeline Dev & Test` | Security and quality review and security validation |
| `CI` | Change recording and initial decision evidence |
| `CD` | Final approval, integrity/provenance evidence, and release preparation |
| `Continuous Training` | Retraining after monitoring |
| `Model Serving` | Runtime and inference infrastructure |
| `Continuous Monitoring` | Live monitoring and SOC integration |

### References / Source mapping

**Frameworks and standards**
- [OpenSSF Secure MLOps whitepaper (August 2025)](https://openssf.org/wp-content/uploads/2025/08/OpenSSF_MLSecOps_Whitepaper.pdf): nine-stage lifecycle baseline

**Implementation guidance (this guide)**
- [OpenSSF stage mapping](11-governance-evidence.md) (Chapter 11); [Lifecycle control points](#lifecycle-control-points)
- [Release decision model](#release-decision-model)

## Common implementation challenges

| Challenge | Practical recommendation |
|---|---|
| Different nature of `DevSecOps` and `MLSecOps` threats | Define dedicated threat model for data, model, and inference. |
| Complexity of continuous retraining | Mandatory decision points **4, 7, 8** and integrity/provenance evidence at **9** in every CT cycle with canary deployment. |
| Opaque behavior inside models | Combine robustness testing, runtime monitoring, and human review for high-risk cases. |
| Risk of frequent retraining | Limit CT frequency and maintain fixed security baseline for comparison. |
| Output authenticity and reproducibility | Use `AI-BOM`, lineage, and signing integrally. |
| Difficulty of risk assessment | Separate operational risk from technical threat and produce `Evidence Pack` continuously. |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: organizational maturity and risk treatment
- ISO/IEC 42001: continual improvement and resource planning

**Implementation guidance (this guide)**
- [Maturity roadmap](14-maturity-roadmap.md) (Chapter 14); [Minimum security baseline](#minimum-security-baseline)
- [Anti-patterns](09-anti-patterns.md) (Chapter 9)

## Minimum security baseline

| Domain | Minimum control |
|---|---|
| Supply chain | Model scan with `ModelScan` and basic `SBOM/AI-BOM` generation |
| Integrity | Digital model signing and verify before deployment |
| Data | `Schema Validation` and `PII Detection & Masking` |
| Lifecycle decisions | Minimum: explicit documented decisions at **4 and 8**; stage **7** tests run every release (blocking decision at Level 2+); integrity/provenance evidence at **9** |
| Classic model | `ART` test and numerical `ASR` criterion at security validation |
| `LLM/RAG` | Automated `Prompt Injection` test and guardrail evaluation |
| Runtime | Deployment behind `Inference Gateway` |
| Monitoring | Send prompt, tool call, and model version to `SIEM/SOC` |
| Incident | Automated rollback and stable version snapshot |

### References / Source mapping

**Frameworks and standards**
- OWASP ML Top 10 (draft) and OWASP LLM Top 10 (2025): minimum control themes by domain (`LLM01` prompt injection)
- MITRE ATLAS: `AML.T0015` Evade AI Model (classic); `AML.T0051` LLM Prompt Injection; `AML.T0053` AI Agent Tool Invocation (agent/tool monitoring)
- OpenSSF MLSecOps: baseline security measures across lifecycle

**Implementation guidance (this guide)**
- [Lifecycle control prioritization](#lifecycle-control-prioritization); [Maturity Level 1](14-maturity-roadmap.md#level-1-minimum) (Chapter 14)
- [Tool mapping](12-threat-control-tools-map.md) (Chapter 12)

**Author practical guidance**
- Named tools (`ModelScan`, `ART`, `Garak`) are starting points; substitute organization-approved equivalents with equivalent evidence output.

## Lifecycle control prioritization

| Level | Controls |
|---|---|
| `MUST` (Level 1 minimum) | Artifact review, integrity/provenance evidence at stage 9, documented decisions at **4 and 8**, stage **7** security tests (recorded; blocking at Level 2+) |
| `MUST` (Level 2 production) | Blocking decisions at **4, 7, 8** + integrity/provenance evidence at **9** on every release and CT cycle |
| `SHOULD` | Automated `SBOM/AI-BOM` generation, canary in CT, automated `Evidence Pack` recording |
| `ADVANCED` | Full CT automation, advanced regression security test, and event mapping to `MITRE ATLAS` |

### References / Source mapping

**Frameworks and standards**
- ISO/IEC 42001: prioritized controls within an AI management system
- NIST AI RMF: tiered implementation and governance

**Implementation guidance (this guide)**
- [Maturity roadmap](14-maturity-roadmap.md) (Chapter 14); [Release decision model](#release-decision-model)
- [Minimum security baseline](#minimum-security-baseline)

## Stage 7 test acceptance conditions

Acceptance thresholds must be defined and versioned in the organization's threat model; values below are examples, not fixed numbers for all systems:

| System type | Test Suite | Acceptance condition |
|---|---|---|
| Classic model | `ART` and backdoor evaluation | `ASR` and accuracy drop must be within threat model-defined thresholds. |
| `LLM/RAG` | `Prompt Injection` and retrieval leak probes | Bypass rate less than or equal to threat model threshold. |
| Agent | Tool misuse and output injection cases | No critical fail in fixed regression set allowed. |

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [AI security testing overview](https://owaspai.org/go/testing/)
- MITRE ATLAS: `AML.T0015` Evade AI Model; `AML.T0051` LLM Prompt Injection; `AML.T0053` AI Agent Tool Invocation; `AML.T0110` AI Agent Tool Poisoning (agent regression)

**Implementation guidance (this guide)**
- [Three categories of security testing](#three-categories-of-security-testing); [Security acceptance criteria](05-model-artifact-supply-chain.md#security-acceptance-criteria) (Chapter 5)
- [Red Team program and security test cadence](#red-team-program-and-security-test-cadence)

**Author practical guidance**
- Threshold values in the table are examples; version acceptance criteria in the threat model and Evidence Pack.

## Three categories of security testing

Do not conflate these test types—they produce different evidence and run on different cadences:

| Category | Purpose | When | Evidence destination |
|---|---|---|---|
| **Conventional security testing** | App, infra, API pentest (non-AI-specific) | Pre-production / periodic | Standard AppSec report; referenced at control point 3 |
| **Continuous validation** | Model behaves per acceptance criteria; detect drift or poisoning via regression | Every release, CT cycle, and runtime monitoring | Control point 6 evaluation + control point 10 telemetry |
| **AI security testing (red team)** | Simulate adversarial attacks (evasion, injection, extraction) | Control point 7; cadence below | Security validation report in `Evidence Pack` |

Continuous validation answers *"does the model still do what we approved?"* AI security testing answers *"can an attacker break our controls?"* Both are required for production MLSecOps; neither replaces conventional pentest of the hosting application.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [AI security testing overview](https://owaspai.org/go/testing/); [Continuous validation](https://owaspai.org/go/continuousvalidation/)
- MITRE ATLAS: `AML.T0015` Evade AI Model; `AML.T0051` LLM Prompt Injection; `AML.T0053` AI Agent Tool Invocation; `AML.T0054` LLM Jailbreak

**Implementation guidance (this guide)**
- [Red Team program and security test cadence](#red-team-program-and-security-test-cadence)
- [Difference between Data Drift and Adversarial Drift](#difference-between-data-drift-and-adversarial-drift)
- [Verification vs. validation](11-governance-evidence.md#verification-vs-validation) (Chapter 11)

## Red Team program and security test cadence

One-time security testing is not enough (Chapter 9). Red Team program must be versioned, repeatable, and have defined cadence:

| Test type | Example tool | Recommended cadence |
|---|---|---|
| Automated prompt injection / jailbreak test | `Garak`, `Promptfoo`, `PyRIT` | Every release (use a **smoke subset** each build; full suite on release/CT—avoid hitting production LLM APIs on every commit) |
| Classic model adversarial test | `ART` (FGSM, PGD, HopSkipJump—**vision/tabular-appropriate attacks only**; see Chapter 12) | Every new model and every CT |
| Manual / scenario-based Red Team | Internal or external team | Quarterly or before major release |
| Security regression test | Fixed versioned suite | Every build (automated) |
| Agent logic and tool misuse test | Custom scenarios | Every agent release |

Results of each run must be recorded in `Evidence Pack` with test suite hash for baseline comparison (Chapter 11).

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [AI security testing overview](https://owaspai.org/go/testing/)
- MITRE ATLAS: `AML.T0015` Evade AI Model; `AML.T0051` LLM Prompt Injection; `AML.T0053` AI Agent Tool Invocation; `AML.T0054` LLM Jailbreak

**Implementation guidance (this guide)**
- [Three categories of security testing](#three-categories-of-security-testing); [Stage 7 test acceptance conditions](#stage-7-test-acceptance-conditions)
- [Continuous monitoring and test cadence](10-monitoring-soc-ir.md) (Chapter 10)

**Author practical guidance**
- Use a smoke subset on every build and reserve full LLM API suites for release/CT to control cost and rate limits.

## Implementation note

This guide intentionally does not provide a production-ready CI/CD implementation. In a practical implementation, controls should produce structured, reviewable evidence so a human approver, policy engine, MLOps platform, or release workflow can make a documented decision. If required evidence is missing, promotion should stop unless an explicit, audited exception is recorded.

Tool examples in Chapter 12 are informative and must be validated against the organization's environment before they are used for release decisions.

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps: implementation-neutral lifecycle guidance (not a reference pipeline)

**Implementation guidance (this guide)**
- [Tool mapping and executable examples](12-threat-control-tools-map.md) (Chapter 12)
- [Release decision model](#release-decision-model); [Evidence Pack](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11)

**Author practical guidance**
- Promotion should stop when required evidence is missing unless a time-bound, audited exception is recorded.

## Golden rule

No model, RAG index, agent configuration, or managed AI service configuration should reach `Production` without appropriate integrity/provenance evidence, `SBOM/AI-BOM` where applicable, documented release decisions, and an `Evidence Pack` or equivalent audit evidence bundle.

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps: integrity, provenance, and monitoring as release prerequisites
- ISO/IEC 42001: documented approval before operational use

**Implementation guidance (this guide)**
- [Practical principle](05-model-artifact-supply-chain.md#practical-principle) (Chapter 5); [What is an Evidence Pack?](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11)
- [Release decision model](#release-decision-model)

## Operational summary

1. No deploy is allowed without documented release decisions and integrity/provenance evidence.
2. Full scan of model files before training process is mandatory.
3. `CT` cycle must repeat the required lifecycle control points without shortcuts.
4. Retrained models must enter the real environment through canary path.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: lifecycle summary — govern, map, measure, manage, and monitor
- OpenSSF MLSecOps whitepaper: end-to-end secure MLOps checklist themes

**Implementation guidance (this guide)**
- [Release decision model](#release-decision-model); [Continuous Training cycle](#continuous-training-cycle)
- [Minimum security baseline](#minimum-security-baseline); [Golden rule](#golden-rule)
