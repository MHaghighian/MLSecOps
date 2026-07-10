# Chapter 4: Data Security and Privacy

## Importance of data security

Model behavior largely comes from the data it was trained on or uses at runtime. If data is poisoned, incomplete, sensitive, of unknown origin, or outside data contract scope, the model can also produce unsafe, biased, or non-auditable output.

In `MLSecOps`, data security is not only a pre-training control. Data must be controlled throughout its entire path: collection, cleaning, labeling, storage, versioning, training, `Fine-tuning`, retrieval in `RAG`, and monitoring.

### References / Source mapping

**Frameworks and standards**
- OWASP ML Top 10 (draft): `ML02` Data Poisoning; data pipeline integrity themes
- MITRE ATLAS: `AML.T0020` Poison Training Data
- OWASP AI Exchange: [Data poisoning](https://owaspai.org/go/datapoison/); [Development-time data leak](https://owaspai.org/go/devdataleak/)

**Implementation guidance (this guide)**
- [Lifecycle control point 4](06-pipeline.md#lifecycle-control-points) (Chapter 6)

## Basic data controls

| Control | Purpose |
|---|---|
| `Schema Validation` | Ensuring correct data structure, field types, and value ranges |
| `PII Detection & Masking` | Identifying and removing or masking sensitive information |
| Dataset anonymization | Tools such as `ARX`, `Presidio`, or `DeepPrivacy2` for anonymization before training |
| `Dataset Lineage` | Recording origin, changes, and data movement path |
| `Data Contract` | Defining a formal agreement between data producer and consumer |
| `Data Versioning` | Enabling training reproduction and review of previous versions |
| Access control | Restricting data access based on role and actual need |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Map (data context); Measure (data quality)
- ISO/IEC 42001: data for AI systems (management system)
- OWASP AI Exchange: [Data limitation](https://owaspai.org/go/datalimit/); [SEGREGATE DATA](https://owaspai.org/go/segregatedata/)

**Implementation guidance (this guide)**
- [Poisoning taxonomy](05-model-artifact-supply-chain.md#poisoning-taxonomy-across-the-lifecycle) (Chapter 5)

## Privacy

Training data may include personal information, organizational data, internal correspondence, source code, operational logs, or confidential documents. Using this data without appropriate controls can cause direct or indirect leakage.

Important privacy risks include:

- Reproduction of training data in model output
- Data disclosure through `RAG`
- Retrieval of a document the user is not authorized to view
- Storage of sensitive information in logs or agent memory
- Use of real data in experimental environments or `Notebook`s

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [AI privacy overview](https://owaspai.org/go/aiprivacy/) — *legal/privacy program depth; this guide covers operational MLSecOps data controls only*
- NIST AI RMF: Govern / Map (privacy and harm context)

**Implementation guidance (this guide)**
- [Prompt and telemetry logging vs privacy](#prompt-and-telemetry-logging-vs-privacy-gdpr--ccpa)

## Sensitive data classification for scanning

Before a dataset enters training, it must be defined which categories of information should be identified, masked, or removed. This classification is the basis for the data decision point in the lifecycle control model (Chapter 6):

| Category | Example | Recommended action |
|---|---|---|
| Direct `PII` | Name, national ID, phone number, email | Remove or mask before training |
| Indirect `PII` / quasi-identifier | Postal code, date of birth, occupation | Aggregation or generalization |
| Financial data | Card number, IBAN, transaction | Tokenization and access control |
| Health data | Diagnosis, medication, medical history | Anonymization and compliance requirements |
| Credentials and secrets | API key, token, password | Secret scanning and complete removal |
| Organizational proprietary data | Source code, internal document, contract | Source allowlist and confidentiality classification |

This table can be implemented as rules in tools such as `Presidio` or custom scripts so checks run automatically in the pipeline.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM02` Sensitive Information Disclosure
- ISO/IEC 42001: data governance for AI systems

**Implementation guidance (this guide)**
- [Control point 4 — Data / Artifact Decision](06-pipeline.md#lifecycle-control-points) (Chapter 6)

## Differential Privacy

`Differential Privacy` is a method for reducing the likelihood of extracting individual information from training data. It is especially important against attacks such as `Membership Inference`, `Model Inversion`, and `Data Reconstruction`.

The goal of `Differential Privacy` is for the model or statistical system to depend as little as possible on whether a specific individual's data is present in the dataset. Ideally, if one person's record is removed from training data and the model is retrained, model behavior should not change enough for an attacker to detect that person's presence or absence.

To achieve this goal, a controlled amount of noise is usually added to data, training gradients, or model output. This noise makes individual information extraction harder but must be tuned carefully so model quality does not drop excessively.

| Use case | Advantage | Limitation |
|---|---|---|
| Training on sensitive data | Reduced individual disclosure risk | Model accuracy may decrease |
| Statistical analysis | More publishable output | Requires careful parameter tuning |
| Regulated environments | Helps with compliance | Not a substitute for access control |

An important limitation is that `Differential Privacy` alone does not guarantee complete data security. If individuals' data are correlated, or noise parameters are not set correctly, information inference remains possible. Therefore it must be used alongside access control, masking, lineage, and data leakage testing.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [Model inversion and membership inference](https://owaspai.org/go/modelinversionandmembership/)
- NIST AI RMF: Measure (privacy-related metrics)

**Emerging / research**
- Differential privacy parameter trade-offs are domain-specific — validate with privacy audit tools below

## Information leakage from Embedding

A common misconception is that `Embedding` vectors stored in a `Vector DB` are not "raw" data and therefore are not sensitive. Research (including *Text Embeddings Reveal (Almost) As Much As Text*) has shown that source text can largely be reconstructed from embeddings through inversion attacks. Therefore:

- `Vector DB` must be protected like a sensitive data store (access control, encryption at-rest, tenant isolation).
- Storing embeddings instead of text alone is not considered a privacy control.
- Long-term agent memory (`Agent Memory`) is also exposed to the same leakage and [memory poisoning](08-agentic-ai-security.md#memory-poisoning) paths (Chapter 8).

### References / Source mapping

**Emerging / research**
- Morris et al., *Text Embeddings Reveal (Almost) As Much As Text* — embedding inversion risk

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM08` Vector and Embedding Weaknesses

**Implementation guidance (this guide)**
- [Chapter 7 — Embedding Poisoning](07-llm-rag-security.md#embedding-poisoning)

## Privacy audit tools

To practically measure `Membership Inference` and `Model Inversion` risk, these tests can be run in the pipeline (periodically):

| Tool | Use |
|---|---|
| `PrivacyRaven` (Trail of Bits) | Black-box model inversion and membership inference testing |
| `ML Privacy Meter` | Quantitative assessment of model privacy leakage risk |
| `TensorFlow Privacy` | Training with `DP-SGD` and membership inference tools |
| `OpenDP` | Implementation of differential privacy algorithms |

> Warning about Synthetic data: Model-generated synthetic data is not necessarily secure. Meeus et al. (2025), *The Canary's Echo: Auditing Privacy Risks of LLM-Generated Synthetic Text* (ICML 2025), showed synthetic text can reveal traces of real training data; therefore synthetic data must also be tested for leakage.

### References / Source mapping

**Emerging / research**
- Meeus et al. (2025). *The Canary's Echo* (ICML 2025) — synthetic data leakage

**Implementation guidance (this guide)**
- [Chapter 12 — Model Privacy Audit](12-threat-control-tools-map.md#l2--model-privacy-audit)

## Experimentation environment security

Experimental environments, `Notebook`s, and research scripts are usually the weakest security point in `ML` projects. Real data is used in these environments, dependencies are installed quickly, and outputs are sometimes stored or published without review.

Minimum controls for these environments:

- Do not use real production data except with authorization and masking
- Scan `Notebook`s for secrets and sensitive outputs
- Run experimental environments in a `Sandbox`
- Restrict network and file access
- Record data version, code, and experiment parameters

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [DEV SECURITY](https://owaspai.org/go/devsecurity/); [SEGREGATE DATA](https://owaspai.org/go/segregatedata/)

**Implementation guidance (this guide)**
- [Chapter 5 — MLOps infrastructure vulnerabilities](05-model-artifact-supply-chain.md#mlops-infrastructure-vulnerabilities)

## Supplementary controls for experimental environments

Several practical controls are needed at this stage:

| Control | Description |
|---|---|
| Development environment isolation | Running notebooks and experimental scripts in containers or sandboxes to reduce risk of poisoned code and data leakage |
| Notebook review | Scanning code, outputs, secrets, and unnecessary access with tools such as `NB Defense` |
| Experiment versioning | Recording experiments, parameters, and artifacts with tools such as `MLflow` |
| Data versioning | Tracking datasets and their changes with tools such as `DVC` |
| Environment separation | Separating `Development`, `Staging`, and `Production` and limiting experimental environment access to operational data and services |
| Raw data protection | Removing, masking, or anonymizing `PII` before use in notebooks or temporary scripts |

### References / Source mapping

**Implementation guidance (this guide)**
- [Chapter 12 — Notebook Scan](12-threat-control-tools-map.md#l2--notebook-scan-nb-defense-and-lintml)

**Author practical guidance**
- *Tool names in this section are informative examples, not endorsements.*

## Data security in RAG

In `RAG` systems, data matters not only at training time; documents retrieved at response time are also part of the attack surface. If the knowledge source is poisoned or overly open, the model may produce unsafe or confidential responses.

| Risk | Control |
|---|---|
| Poisoned document entering `Vector DB` | `Ingest` control and input content scanning |
| Unauthorized document retrieval | Applying access control at read time |
| Cross-customer leakage | Separate index per tenant |
| Stale or incorrect context retrieval | Periodic `Re-index` and source cleanup |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04` Data and Model Poisoning (RAG corpus); retrieval leakage themes
- MITRE ATLAS: `AML.T0070` RAG Poisoning

**Implementation guidance (this guide)**
- [Chapter 7 — Ingest security in RAG](07-llm-rag-security.md#ingest-security-in-rag)

## Practical principle

Every piece of data entering the AI lifecycle must have defined origin, owner, version, sensitivity level, and usage authorization. Without this information, model output will not be defensible or auditable.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Map (data governance); GDPR / CCPA data-protection themes — [prompt and telemetry logging](#prompt-and-telemetry-logging-vs-privacy-gdpr--ccpa)
- ISO/IEC 42001: data and documented information for AI management system

**Implementation guidance (this guide)**
- [Basic data controls](#basic-data-controls); [Lifecycle control point 4](06-pipeline.md#lifecycle-control-points) (Chapter 6)

## Feature Store security

When a `Feature Store` is used, features are long-lived training and serving assets—not ephemeral pipeline outputs. Minimum controls:

| Risk | Control |
|---|---|
| PII or secrets in feature values | Scan and classify at write; block unmasked sensitive features |
| Stale or poisoned features | Versioning, lineage, and schema validation on publish |
| Cross-team leakage | RBAC on feature groups; separate online/offline stores per tenant where required |
| Serving skew | Align training-serving feature definitions; audit transformations |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Map (feature and data lineage)

**Implementation guidance (this guide)**
- [Basic data controls](#basic-data-controls) in this chapter

**Author practical guidance**
- *Feature Store patterns are implementation guidance for teams using Feast/Tecton-style architectures.*

## Training data licensing and copyright

Public or scraped datasets may impose license, attribution, or use restrictions. Record **license type, provenance, and permitted use** in the `Evidence Pack` and block training when license or contractual scope is unclear—this is a supply-chain and legal risk, not only a quality issue.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [Copyright and AI training data](https://owaspai.org/go/copyright/)

**Implementation guidance (this guide)**
- [Evidence Pack components](11-governance-evidence.md#evidence-pack-components) (Chapter 11)

## Prompt and telemetry logging vs privacy (GDPR / CCPA)

Production logging of full prompts and responses (Chapter 10) can contain personal data. Before enabling SIEM export:

| Requirement | Practice |
|---|---|
| Data minimization | Log hashes, truncated text, or tokenized fields where full content is not required for IR |
| Lawful basis / notice | Align with privacy policy and employment agreements; involve DPO/legal for EU/UK |
| Retention | Time-bound retention and deletion; separate security logs from analytics |
| Access control | Restrict SIEM views; mask PII in dashboards |
| Cross-border transfer | Document regions for LLM providers and log storage |

See also [Chapter 10](10-monitoring-soc-ir.md) for operational telemetry guidance.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [AI privacy](https://owaspai.org/go/aiprivacy/) — *consult legal/privacy teams for GDPR/CCPA program requirements*

**Implementation guidance (this guide)**
- [Chapter 10 — Data required for telemetry](10-monitoring-soc-ir.md#data-required-for-telemetry)
