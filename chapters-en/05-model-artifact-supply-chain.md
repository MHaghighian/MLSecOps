# Chapter 5: Model, Artifact, and Supply Chain Security

## Model as a security asset

A model is not merely an output file from the training process. A model is a sensitive asset that can contain decision logic, training data, organizational knowledge, and intellectual property value. Therefore it must be managed as a security `Artifact`.

In `MLSecOps`, every model must have defined origin, version, hash, signature, evaluation metrics, security test results, and release authorization.

## Model security controls

| Control | Purpose |
|---|---|
| `Model Artifact Scanning` | Identifying unsafe files such as `pickle` and malicious code |
| `Backdoor Detection` | Detecting conditional or `Trigger-based` behavior |
| `Adversarial Robustness Testing` | Measuring resistance to manipulated inputs |
| `Model Signing` | Ensuring authenticity and preventing model replacement |
| `Provenance Tracking` | Recording the model build path from data to release |
| `Access Control` | Restricting model download, loading, and execution |

## Minimum Adversarial Robustness requirements

This section is especially important for classic models such as `Tabular`, `Vision`, and `Speech`. In `LLM` systems, security evaluation is usually done with tools such as `Garak` or `Promptfoo`, focusing on `Prompt Injection`, `Jailbreak`, and `Retrieval Leakage`.

The goal of `Adversarial Robustness Testing` is to determine whether an attacker can steer the model to a wrong decision with small, controlled input changes. This test must be part of `Pre-Deployment Security Validation`.

## Defining threat model before testing

The result of a security test without a defined threat model has limited operational value. Before running adversarial tests, at minimum these questions must be answered:

| Question | Example | Topic |
|---|---|---|
| `Who` | External attacker, internal user, bot, or automated service | Who is the attacker? |
| `Where` | Inference APIs, batch scoring, application, or connected service | Where does the attack occur? |
| `Goal` | `Evasion`, `Model Extraction`, or service disruption | What is the attacker's goal? |
| `Knowledge` | `Black-box` or `White-box` | How much knowledge does the attacker have? |

## Minimum security tests

- Use a versioned `Security Test Suite` so tests are repeatable for every model version.
- Run adversarial tests with tools such as `ART`.
- Use methods such as `FGSM` and `PGD` on vision models.
- Use methods such as `HopSkipJump` to simulate black-box scenarios.
- Check for `Backdoor` or hidden triggers, especially in pretrained or transfer learning models.
- Run robustness tests for multimodal models (`Multimodal/VLM`) against adversarial visual instructions (`Adversarial Visual-Instructions`) and OCR injection using frameworks such as `AVIBench` or multimodal extensions of `ART`.
- Compare results against signed baselines, not just a simple pass/fail.

## Risk of unsafe formats

Some model storage formats such as `pickle` can cause code execution when loaded. In such cases, simply opening a poisoned model may lead to arbitrary code execution by the attacker in the training or deployment environment.

Recommended principles:

- Use safer formats such as `safetensors` when possible
- Scan all `Artifact`s before loading
- Load models in an isolated environment
- Prohibit loading models from unknown sources

> Warning: The "convert to safe format" path itself can be an attack surface. The "SILENT SABOTAGE" study showed a `pickle` to `safetensors` conversion bot on a public platform was abused to produce poisoned artifacts. Therefore choosing a safe format is not enough; the conversion service, bot account, and its credentials must also be hardened and audited.

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

## Infrastructure-as-Code security for ML

ML environments usually run on `Kubernetes`, `Terraform`, and cloud managed services. `DevSecOps` controls must also be applied in the ML pipeline:

| Tool | Use |
|---|---|
| `Checkov` / `tfsec` | Scanning misconfiguration in Terraform |
| `terraform-compliance` | Negative testing for IaC |
| `TFlint` | Linting for Terraform |
| `Kyverno` / `OPA Gatekeeper` | Policy in cluster |
| `NetworkPolicy` | Restricting egress of training/inference pods |

## SBOM and AI-BOM

`SBOM` lists software components. AI systems require additional information that can be called `AI-BOM`.

| Document | Contents |
|---|---|
| `SBOM` | Packages, versions, dependencies, and vulnerabilities |
| `AI-BOM` | Data, base model, parameters, metrics, tests, origin, and training evidence |

`SBOM` can be generated with tools such as `Syft` and `CycloneDX`. For `AI-BOM`, model-specific information, dataset, artifacts, and AI components must also be recorded; tools such as `cdxgen` (`aibom` command) and `OWASP AIBOM Generator` are usable in this domain.

The `CycloneDX 1.7` standard (published 2025 and approved as the second version of `ECMA-424`) officially supports `ML-BOM` and enables recording a model as a component, hash of each weight file, and dataset version. Practical recommendation is that `ML-BOM` generation be part of model promotion—exactly like `SBOM` generation in the container build pipeline. Commands and executable examples are in Chapter 12.

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

## Security evaluation output

At the end of security evaluation, an `Evidence Pack` must be stored with the model. This bundle at minimum includes:

- Full adversarial test report
- Metric results such as `ASR`, `Accuracy`, and `Clean Accuracy Drop`
- Exact version of `Security Test Suite`
- Model hash and digital signature
- Defined threat model documentation
- Attestation related to build and release process

## Federated Learning

If the system uses `Federated Learning`, specific threats also arise. In this architecture raw data remains on nodes and only model updates are exchanged; but a malicious node can send poisoned updates or attempt to infer information about other participants.

| Control | Purpose |
|---|---|
| `Secure Aggregation` | Central server sees only aggregated update result. |
| `Client Attestation` | Identity and security posture of participating nodes are verified. |
| Resistance to `Byzantine Attacks` | Malicious or incorrect updates have limited effect. |
| `Audit Trail` | Node participation, updates, and aggregation decisions are recorded. |

## Key and secret management

AI models and pipelines usually work with API keys, `Model Registry` credentials, model signing keys, and cloud service tokens. This information must not be stored in code, notebooks, images, config files, or model bundles.

Recommended controls:

- Use `Secret Manager` or `KMS` such as `Vault`, `AWS Secrets Manager`, `AWS KMS`, `Azure Key Vault`, or `Google Cloud KMS`
- Proxy gateway for model API keys (API key proxy pattern): agents and pipelines call a gateway that holds credentials; they never receive raw keys, enabling immediate kill switch on compromise
- Apply least privilege for all credentials
- Keep model signing keys outside repository and pipeline
- Log all secret view, use, rotation, and deletion operations
- Rapid key rotation and revocation on disclosure or service decommission

## Practical principle

No anonymous, unsigned, origin-unknown model without security testing should enter `Production`. A model must be as controllable as a sensitive container image or software package.
