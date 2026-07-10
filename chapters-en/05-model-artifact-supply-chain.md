# Chapter 5: Model, Artifact, and Supply Chain Security

## Model as a security asset

A model is not merely an output file from the training process. A model is a sensitive asset that can contain decision logic, training data, organizational knowledge, and intellectual property value. Therefore it must be managed as a security `Artifact`.

In `MLSecOps`, every model must have defined origin, version, hash, signature, evaluation metrics, security test results, and release authorization.

### References / Source mapping

**Frameworks and standards**
- OWASP ML Top 10; MITRE ATLAS supply-chain and model integrity techniques
- NIST SSDF / SLSA themes for artifact provenance (where applicable)

**Implementation guidance (this guide)**
- [Lifecycle control points 2, 7, 8, 9](06-pipeline.md#lifecycle-control-points) (Chapter 6)

## Model security controls

| Control | Purpose |
|---|---|
| `Model Artifact Scanning` | Identifying unsafe files such as `pickle` and malicious code |
| `Backdoor Detection` | Detecting conditional or `Trigger-based` behavior |
| `Adversarial Robustness Testing` | Measuring resistance to manipulated inputs |
| `Model Signing` | Ensuring authenticity and preventing model replacement |
| `Provenance Tracking` | Recording the model build path from data to release |
| `Access Control` | Restricting model download, loading, and execution |

### References / Source mapping

**Frameworks and standards**
- OWASP ML Top 10 (draft): model integrity and supply-chain themes
- MITRE ATLAS: `AML.T0015` Evade AI Model; `AML.T0058` Publish Poisoned Models
- OWASP AI Exchange: [Model poisoning](https://owaspai.org/go/modelpoison/); [Supply-chain model poisoning](https://owaspai.org/go/supplymodelpoison/)

**Implementation guidance (this guide)**
- [Minimum Adversarial Robustness requirements](#minimum-adversarial-robustness-requirements); [Provenance and signing](#provenance-and-signing)
- [Lifecycle control points 2, 7, 9](06-pipeline.md#lifecycle-control-points) (Chapter 6)

## Minimum Adversarial Robustness requirements

This section is especially important for classic models such as `Tabular`, `Vision`, and `Speech`. In `LLM` systems, security evaluation is usually done with tools such as `Garak` or `Promptfoo`, focusing on `Prompt Injection`, `Jailbreak`, and `Retrieval Leakage`.

The goal of `Adversarial Robustness Testing` is to determine whether an attacker can steer the model to a wrong decision with small, controlled input changes. This test must be part of `Pre-Deployment Security Validation`.

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0015` Evade AI Model; `AML.T0051` LLM Prompt Injection (LLM/RAG validation path)
- OWASP LLM Top 10 (2025): `LLM01` Prompt Injection (LLM systems)
- OWASP ML Top 10 (draft): adversarial evasion and robustness themes
- NIST AI RMF: Measure (model performance and robustness)

**Implementation guidance (this guide)**
- [Defining threat model before testing](#defining-threat-model-before-testing); [Minimum security tests](#minimum-security-tests)
- [Stage 7 test acceptance conditions](06-pipeline.md#stage-7-test-acceptance-conditions) (Chapter 6)

## Defining threat model before testing

The result of a security test without a defined threat model has limited operational value. Before running adversarial tests, at minimum these questions must be answered:

| Question | Example | Topic |
|---|---|---|
| `Who` | External attacker, internal user, bot, or automated service | Who is the attacker? |
| `Where` | Inference APIs, batch scoring, application, or connected service | Where does the attack occur? |
| `Goal` | `Evasion`, `Model Extraction`, or service disruption | What is the attacker's goal? |
| `Knowledge` | `Black-box` or `White-box` | How much knowledge does the attacker have? |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Map (context and risk framing)
- MITRE ATLAS: technique selection by attacker knowledge and goal
- OWASP AI Exchange: [AI security testing overview](https://owaspai.org/go/testing/)

**Implementation guidance (this guide)**
- [Threat modeling scope](02-scope-risk-threat-model.md#threat-modeling-process) (Chapter 2); [Threat landscape](03-threat-landscape.md) (Chapter 3)
- [Model theft and extraction paths](#model-theft-and-extraction-paths)

## Minimum security tests

- Use a versioned `Security Test Suite` so tests are repeatable for every model version.
- Run adversarial tests with tools such as `ART`.
- Use methods such as `FGSM` and `PGD` on vision models.
- Use methods such as `HopSkipJump` to simulate black-box scenarios.
- Check for `Backdoor` or hidden triggers, especially in pretrained or transfer learning models.
- Run robustness tests for multimodal models (`Multimodal/VLM`) against adversarial visual instructions (`Adversarial Visual-Instructions`) and OCR injection using frameworks such as `AVIBench` or multimodal extensions of `ART`.
- Compare results against signed baselines, not just a simple pass/fail.

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0015` Evade AI Model; `AML.T0058` Publish Poisoned Models (backdoor evaluation)
- OWASP AI Exchange: [AI security testing overview](https://owaspai.org/go/testing/)

**Implementation guidance (this guide)**
- [Security acceptance criteria](#security-acceptance-criteria); [Security evaluation output](#security-evaluation-output)
- [Tool mapping and ART examples](12-threat-control-tools-map.md) (Chapter 12)

**Author practical guidance**
- Tool examples (`ART`, `AVIBench`, `FGSM`/`PGD`/`HopSkipJump`) are illustrative; validate attack suites against your modality and threat model.

## Risk of unsafe formats

Some model storage formats such as `pickle` can cause code execution when loaded. In such cases, simply opening a poisoned model may lead to arbitrary code execution by the attacker in the training or deployment environment.

Recommended principles:

- Use safer formats such as `safetensors` when possible
- Scan all `Artifact`s before loading
- Load models in an isolated environment
- Prohibit loading models from unknown sources

> Warning: The "convert to safe format" path itself can be an attack surface. The "SILENT SABOTAGE" study showed a `pickle` to `safetensors` conversion bot on a public platform was abused to produce poisoned artifacts. Therefore choosing a safe format is not enough; the conversion service, bot account, and its credentials must also be hardened and audited.

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0058` Publish Poisoned Models
- OWASP AI Exchange: [Development-time threats](https://owaspai.org/go/developmenttime/); [Supply-chain model poisoning](https://owaspai.org/go/supplymodelpoison/)
- OpenSSF: secure artifact handling and model scanning guidance

**Implementation guidance (this guide)**
- [Model security controls](#model-security-controls); [SBOM and AI-BOM](#sbom-and-ai-bom)
- [Lifecycle control point 2 — Load Artifacts](06-pipeline.md#lifecycle-control-points) (Chapter 6)

**Author practical guidance**
- Prefer `safetensors` and scan-before-load; treat format-conversion bots and public registries as untrusted supply-chain nodes.

## AI supply chain

The AI supply chain is not limited to software packages. This chain also includes data, base model, `Dataset`, `Notebook`, training code, dependencies, container, model registry, and deployment scripts.

| Chain component | Risk |
|---|---|
| Base model | Poisoning, `Backdoor`, or hidden behavior |
| Public dataset | `Data Poisoning` or incorrect labeling |
| Software dependency | Vulnerability or `Typosquatting` |
| `Notebook` | Secret leakage or unsafe code execution |
| `Model Registry` | Replacement of healthy model with poisoned model |
| Container | Operating system or installed tool vulnerabilities |

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0058` Publish Poisoned Models; `AML.T0020` Poison Training Data
- SLSA / NIST SSDF: artifact provenance and dependency integrity themes
- OpenSSF MLSecOps whitepaper: AI supply-chain stages

**Implementation guidance (this guide)**
- [Poisoning taxonomy across the lifecycle](#poisoning-taxonomy-across-the-lifecycle); [SBOM and AI-BOM](#sbom-and-ai-bom)
- [Data security controls](04-data-security-privacy.md) (Chapter 4)

## Poisoning taxonomy across the lifecycle

Poisoning threats are described in several chapters; this table consolidates them for release planning. Detailed controls remain in the linked sections—do not treat this as a second threat catalog.

| Poisoning type | Phase | Example | Lifecycle control points | Detail in this guide |
|---|---|---|---|---|
| Training / finetune data poisoning | Development | Malicious labels in dataset | 2, 3, 4 | [Ch.4 data controls](04-data-security-privacy.md), [Ch.12 mapping](12-threat-control-tools-map.md) |
| Development-time model poisoning | Development | Tampered weights in training env | 3, 4, 7 | [Ch.5 model controls](#model-security-controls), [Ch.4 experimentation](04-data-security-privacy.md#experimentation-environment-security) |
| Supply-chain model poisoning | Staging / load | Poisoned pretrained model from registry | 2, 3, 9 | [AI supply chain](#ai-supply-chain), [SBOM and AI-BOM](#sbom-and-ai-bom) |
| Runtime model poisoning | Production | Altered weights or I/O logic in live system | 9, 10 | [Ch.16 runtime integrity](16-kubernetes-deployment-reference.md), signing verify at deploy |
| Augmentation / RAG poisoning | Configure / runtime | Poisoned corpus, system prompt, tool context | 4, 5, 7, 10 | [Ch.7 RAG](07-llm-rag-security.md#ingest-security-in-rag), [Ch.8 memory](08-agentic-ai-security.md#memory-poisoning) |
| Agent memory / context poisoning | Runtime | Persistent poisoned session state | 7, 10 | [Ch.8](08-agentic-ai-security.md#memory-poisoning) |

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0020` Poison Training Data; `AML.T0058` Publish Poisoned Models; `AML.T0070` RAG Poisoning; `AML.T0080` AI Agent Context Poisoning
- OWASP AI Exchange: [Development-time threats](https://owaspai.org/go/developmenttime/); [Model poisoning](https://owaspai.org/go/modelpoison/); [Data poisoning](https://owaspai.org/go/datapoison/); [Supply-chain model poisoning](https://owaspai.org/go/supplymodelpoison/); [Runtime model poisoning](https://owaspai.org/go/runtimemodelpoison/); [Augmentation data manipulation](https://owaspai.org/go/augmentationdatamanipulation/)

**Implementation guidance (this guide)**
- [Appendix A threat card](15-conclusion-appendix.md#appendix-a-threat-control-and-tool-reference-card) (Chapter 15)
- [Master control matrix](17-appendix-e-implementation-reference.md#e6-master-control-matrix) (Appendix E.6)

## Model theft and extraction paths

`Model theft` is not one attack. Map controls to the path that matches your threat model:

| Path | Mechanism | Primary controls | Guide reference |
|---|---|---|---|
| **Model exfiltration** | Repeated API queries reconstruct model behavior | Rate limit, access control, query monitoring, watermark (supplementary) | [Ch.10 SOC](10-monitoring-soc-ir.md), [Ch.7 gateway](07-llm-rag-security.md#security-controls-for-llm) |
| **Direct runtime leak** | Break-in to registry, GPU memory, or artifact store | Signing, RBAC, runtime integrity, network isolation | [Ch.5 signing](#provenance-and-signing), [Ch.16](16-kubernetes-deployment-reference.md) |
| **Side-channel** | Timing or resource signals infer model internals | Tenant isolation, rate limit, padding (tokenizer timing) | [Ch.7 multi-tenant](07-llm-rag-security.md#advanced-multi-tenant-hardening) |

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0024` Exfiltration via AI Inference API (model exfiltration path)
- OWASP AI Exchange: [Model exfiltration](https://owaspai.org/go/modelexfiltration/); [Direct runtime model leak](https://owaspai.org/go/runtimemodelleak/); [Runtime model confidentiality](https://owaspai.org/go/runtimemodelconfidentiality/)

**Implementation guidance (this guide)**
- [MITRE ATLAS mapping](12-threat-control-tools-map.md#mitre-atlas-mapping) (Chapter 12)
- [Defining threat model before testing](#defining-threat-model-before-testing)

## MLOps infrastructure vulnerabilities

`MLOps` platforms—such as `MLflow`, `ClearML`, `Kubeflow`, model registries, and notebook servers—are attack surfaces themselves. Security research (including HiddenLayer, JFrog *MLOops*, Contrast Security MLflow advisories, and Trail of Bits) has shown:

| Platform / vector | Risk | Control |
|---|---|---|
| `MLflow` | `LFI`/path traversal, access to cloud credentials | Patch, network isolation, auth |
| `ClearML` | Agent compromise and pipeline poisoning | Agent hardening, artifact allowlist |
| `Notebook Server` | Arbitrary code execution, secret leakage | `NB Defense`, sandbox, egress deny |
| Public `Model Registry` | Poisoned model, pickle RCE | `ModelScan`, allowlist, signing |
| `Prefect/Airflow` in ML | Secrets in log or config | Secret manager, log sanitization |

The "Confused Learning" attack shows an attacker can divert the entire training pipeline through a poisoned model or metadata—even before the model reaches inference.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [Development-time threats](https://owaspai.org/go/developmenttime/)
- MITRE ATLAS: `AML.T0058` Publish Poisoned Models (pipeline and registry poisoning)
- CVE-adjacent platform risk: patch and isolate MLOps services like any production application

**Implementation guidance (this guide)**
- [Experimentation environment security](04-data-security-privacy.md#experimentation-environment-security) (Chapter 4)
- [Kubernetes deployment reference](16-kubernetes-deployment-reference.md) (Chapter 16)

**Author practical guidance**
- Platform examples (`MLflow`, `ClearML`, `Kubeflow`, notebook servers) reflect published research and advisories; map controls to your registry and orchestration stack.

## Infrastructure-as-Code security for ML

ML environments usually run on `Kubernetes`, `Terraform`, and cloud managed services. `DevSecOps` controls must also be applied in the ML pipeline:

| Tool | Use |
|---|---|
| `Checkov` / `tfsec` | Scanning misconfiguration in Terraform |
| `terraform-compliance` | Negative testing for IaC |
| `TFlint` | Linting for Terraform |
| `Kyverno` / `OPA Gatekeeper` | Policy in cluster |
| `NetworkPolicy` | Restricting egress of training/inference pods |

### References / Source mapping

**Frameworks and standards**
- NIST SSDF: secure deployment and configuration management
- CSA CCM / cloud hardening baselines for ML workloads
- OpenSSF: DevSecOps integration for ML pipelines

**Implementation guidance (this guide)**
- [MLOps infrastructure vulnerabilities](#mlops-infrastructure-vulnerabilities)
- [Kubernetes deployment reference](16-kubernetes-deployment-reference.md) (Chapter 16)

**Author practical guidance**
- Tool examples (`Checkov`, `Kyverno`, `OPA Gatekeeper`) are representative; select scanners and policy engines approved by your platform team.

## SBOM and AI-BOM

`SBOM` lists software components. AI systems require additional information that can be called `AI-BOM`.

| Document | Contents |
|---|---|
| `SBOM` | Packages, versions, dependencies, and vulnerabilities |
| `AI-BOM` | Data, base model, parameters, metrics, tests, origin, and training evidence |

`SBOM` can be generated with tools such as `Syft` and `CycloneDX`. For `AI-BOM`, model-specific information, dataset, artifacts, and AI components must also be recorded; tools such as `cdxgen` (`aibom` command) and `OWASP AIBOM Generator` are usable in this domain.

The `CycloneDX 1.7` standard (published 2025 and approved as the second version of `ECMA-424`) officially supports `ML-BOM` and enables recording a model as a component, hash of each weight file, and dataset version. Practical recommendation is that `ML-BOM` generation be part of model promotion—exactly like `SBOM` generation in the container build pipeline. Commands and executable examples are in Chapter 12.

### References / Source mapping

**Frameworks and standards**
- CycloneDX 1.7 / ECMA-424: `ML-BOM` and AI component metadata
- SPDX: SBOM baseline for software dependencies
- OpenSSF / OWASP AIBOM Generator: AI-specific bill of materials practices

**Implementation guidance (this guide)**
- [Tool mapping — SBOM/AI-BOM generation](12-threat-control-tools-map.md) (Chapter 12)
- [Lifecycle control points 2 and 9](06-pipeline.md#lifecycle-control-points) (Chapter 6)

## Security acceptance criteria

Before model release, numerical and reviewable criteria must be defined.

> Important note: The numbers in the table below are **examples only** and must be tuned based on threat model, application sensitivity, and each organization's real baseline. These values are not a one-size-fits-all for all systems; they may be stricter for a high-risk credit scoring model and looser for a low-risk internal tool.

| Criterion | Example acceptance condition |
|---|---|
| `Attack Success Rate` | Must not increase more than 2% relative to baseline |
| `Clean Accuracy Drop` | Accuracy drop on clean data must not exceed 1% |
| `Transfer Rate` | Success rate of attack built on surrogate against main model must be at most 5% |
| `Backdoor Activation` | Hidden behavior activation must be zero |
| `Critical Vulnerability` | No critical vulnerability in `Artifact` is allowed |
| Model signature | Model and evidence must be signed with a valid key |

If any criterion exceeds the defined threshold, the model must not enter `Production` and hardening or retraining must be performed.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Measure / Manage (acceptance thresholds and risk treatment)
- OWASP ML Top 10 (draft): validation before deployment themes

**Implementation guidance (this guide)**
- [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6); [Stage 7 test acceptance conditions](06-pipeline.md#stage-7-test-acceptance-conditions)
- [What is an Evidence Pack?](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11)

**Author practical guidance**
- Thresholds in the table are examples only; tune `ASR`, accuracy drop, and backdoor criteria per threat model and baseline.

## Provenance and signing

Every released model must be traceable. It must be possible to answer:

- Which data was the model built from?
- Which version of training code was used?
- Who approved release?
- Which tests were run?
- What are the model hash and signature?
- Was the model altered during the release path?

For model signing, in addition to general tools such as `Cosign`, there is now a dedicated tool `sigstore/model-transparency` (`model-signing` package) built with `OpenSSF`, `NVIDIA`, and `HiddenLayer` for ML models. This tool supports keyless identity-based signing (`OIDC`), which reduces long-term private key management burden (identity provider trust and verification policy still required), and can record signing events in the public `Rekor` transparency log for auditability (commands in Chapter 12).

> **Confidentiality:** Public transparency logs expose signature metadata and artifact hashes. For proprietary models or regulated environments, use private attestation registries, internal object storage with object lock, or organization-controlled provenance—document the choice in the `Evidence Pack`.

In some scenarios, `Watermarking` can also be used to embed an identifiable mark in the model or its output. This mechanism can help prove ownership, identify copied models, or track unauthorized use, but it is a supplementary control and does not replace digital signing or `Provenance Tracking`.

### References / Source mapping

**Frameworks and standards**
- OpenSSF `sigstore/model-transparency` and Cosign signing practices
- SLSA: build and release provenance attestations
- NIST SSDF: integrity verification themes

**Implementation guidance (this guide)**
- [Lifecycle control point 9 — Integrity and Provenance](06-pipeline.md#lifecycle-control-points) (Chapter 6)
- [Signing commands and tool mapping](12-threat-control-tools-map.md) (Chapter 12)

**Author practical guidance**
- Use private attestation stores when public transparency logs (`Rekor`) would expose proprietary model metadata.

## Security evaluation output

At the end of security evaluation, an `Evidence Pack` must be stored with the model. This bundle at minimum includes:

- Full adversarial test report
- Metric results such as `ASR`, `Accuracy`, and `Clean Accuracy Drop`
- Exact version of `Security Test Suite`
- Model hash and digital signature
- Defined threat model documentation
- Attestation related to build and release process

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Measure (documented evaluation evidence)
- ISO/IEC 42001: technical documentation and records for AI systems

**Implementation guidance (this guide)**
- [What is an Evidence Pack?](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11)
- [Security acceptance criteria](#security-acceptance-criteria); [Defining threat model before testing](#defining-threat-model-before-testing)

## Federated Learning

If the system uses `Federated Learning`, specific threats also arise. In this architecture raw data remains on nodes and only model updates are exchanged; but a malicious node can send poisoned updates or attempt to infer information about other participants.

| Control | Purpose |
|---|---|
| `Secure Aggregation` | Central server sees only aggregated update result. |
| `Client Attestation` | Identity and security posture of participating nodes are verified. |
| Resistance to `Byzantine Attacks` | Malicious or incorrect updates have limited effect. |
| `Audit Trail` | Node participation, updates, and aggregation decisions are recorded. |

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0020` Poison Training Data (poisoned client updates)
- NIST AI RMF: Map / Manage (distributed training risk)

**Implementation guidance (this guide)**
- [Poisoning taxonomy across the lifecycle](#poisoning-taxonomy-across-the-lifecycle); [Data security controls](04-data-security-privacy.md) (Chapter 4)

**Emerging / research**
- Byzantine-robust aggregation and secure aggregation remain active research areas; treat client attestation and update validation as mandatory operational controls.

## Key and secret management

AI models and pipelines usually work with API keys, `Model Registry` credentials, model signing keys, and cloud service tokens. This information must not be stored in code, notebooks, images, config files, or model bundles.

Recommended controls:

- Use `Secret Manager` or `KMS` such as `Vault`, `AWS Secrets Manager`, `AWS KMS`, `Azure Key Vault`, or `Google Cloud KMS`
- Proxy gateway for model API keys (API key proxy pattern): agents and pipelines call a gateway that holds credentials; they never receive raw keys, enabling immediate kill switch on compromise
- Apply least privilege for all credentials
- Keep model signing keys outside repository and pipeline
- Log all secret view, use, rotation, and deletion operations
- Rapid key rotation and revocation on disclosure or service decommission

### References / Source mapping

**Frameworks and standards**
- OWASP Secrets Management Cheat Sheet (general secret-handling baseline)
- NIST key-management guidance (KMS-backed signing and API credentials)
- CSA CCM: identity and credential management themes

**Implementation guidance (this guide)**
- [Experimentation environment security](04-data-security-privacy.md#experimentation-environment-security) (Chapter 4)
- [Security controls for LLM — API key proxy](07-llm-rag-security.md#security-controls-for-llm) (Chapter 7)

**Author practical guidance**
- API key proxy and gateway patterns are recommended deployment shapes; implement kill-switch and rotation with your organization's secret manager.

## Practical principle

No anonymous, unsigned, origin-unknown model without security testing should enter `Production`. A model must be as controllable as a sensitive container image or software package.

### References / Source mapping

**Frameworks and standards**
- OpenSSF model signing guidance; SPDX/SBOM practices for ML artifacts

**Implementation guidance (this guide)**
- [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6); [Evidence Pack](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11)
