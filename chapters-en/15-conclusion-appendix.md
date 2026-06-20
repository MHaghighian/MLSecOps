# Chapter 15: Conclusion and Appendices

<div dir="ltr">

## Conclusion

`MLSecOps` is a response to the reality that AI systems are not merely classic software. They work with data, models, `Artifact`s, prompts, `RAG`, memory, tools, agents, and probabilistic behavior. Therefore, their security must be distributed across the entire lifecycle.

In this article, security began at the data layer, extended to the model and supply chain, was controlled in the pipeline with enforceable gates, continued at `Runtime` with guardrails and telemetry, and ultimately became auditable through the `Evidence Pack` and governance.

## Key Principles

| Principle | Explanation |
|---|---|
| Security is continuous | A single test before release is not enough. |
| Data is a security asset | Poisoned or sensitive data can make a model insecure. |
| Models must be traceable | Without provenance and signature, a model is not trustworthy. |
| Runtime is critical | Many LLM and Agent attacks occur at runtime. |
| Evidence must be automated | Manual audit after an incident is not reliable. |

> This guide was developed based on frameworks and published knowledge through the end of 2025. Given the pace of change in LLM and Agentic AI, readers should periodically review new versions of `OWASP LLM Top 10`, `MITRE ATLAS`, and CycloneDX standards.

## Compact Checklist

| Domain | Question |
|---|---|
| Data | Are data origin, version, owner, and sensitivity defined? |
| Model | Has the model been scanned, tested, and signed? |
| Supply chain | Has `SBOM/AI-BOM` been produced? |
| Pipeline | Do gates actually stop release on failure? |
| RAG | Is ACL applied at retrieval time? |
| Agent | Does every tool call pass through an `Intent Gate`? |
| Runtime | Are prompt, response, retrieval, and tool call logged? |
| SOC | Do AI incidents enter the SIEM? |
| Governance | Does an auditable evidence pack exist? |

## Production Operational Checklist

This checklist completes the minimum baseline and `Day-2` operations. If time is limited, close `MUST` controls in the pipeline and `Runtime/SOC` first. Each control must have a defined owner, frequency, and evidence.

### Minimum RACI

| Activity | R Responsible | A Accountable | C Consulted | I Informed |
|---|---|---|---|---|
| Threat Model | Product Security | CISO / Head of AI | Legal, Data Governance | Engineering Lead |
| Policy Gate / Pipeline | MLOps | Platform Engineering Manager | Security | Model Owner |
| Runtime Guardrails | Platform / AppSec | Model Owner | SOC | Privacy |
| SOC Alert / IR | SOC Analyst | SOC Manager | Security, MLOps | Legal in case of leakage |
| Evidence Pack / Audit | MLOps | Compliance | Security | Internal Audit |

### Data and Privacy

| Control | Owner | Frequency | Evidence |
|---|---|---|---|
| `Data Contract` and `Schema Validation` | Data Engineer | Each new dataset | Validation report in `MLflow/DVC` |
| `PII Detection & Masking` | Data Governance | Each ingest | Mask log and audit sample |
| `Membership Inference` assessment | Security + ML | Annually or after high-risk model | Privacy test report |
| `Differential Privacy` audit | Privacy Officer | Annually | DP configuration document |

### Model and Supply Chain

| Control | Owner | Frequency | Evidence |
|---|---|---|---|
| `ModelScan` at load | MLOps | Every build | ModelScan report |
| `SBOM/AI-BOM` | MLOps | Every build | `CycloneDX` file or equivalent |
| Signing and verify | MLOps | Every deploy | `Cosign Attestation` |
| `ART / Adversarial Test` and ASR acceptance | Security | Each new model | ART report and ASR vs. baseline |
| Secret in `Vault/KMS` | Platform | Each key cycle | Access audit log |

### Pipeline, CT, RAG, and Agent

| Control | Owner | Frequency | Evidence |
|---|---|---|---|
| Versioned Threat Model | Product Security | Each new AI service and annually | Threat model document |
| Policy Gate without exception | MLOps | Every build | `OPA/Conftest` log |
| Gate 7 for LLM | Security | Every LLM build | Red team report and metrics vs. baseline |
| CT with canary and security regression | MLOps | Each retrain | Canary log and baseline comparison |
| RAG allowlist and reindex playbook | ML Engineer | Each new source | Index hash and regression test |
| Agent intent gate, HITL, and kill switch | AppSec | Each agent release | Policy test and runbook |
| Tool output gate | AppSec | Each agent release | Malicious JSON/Markdown test |
| Multi-agent depth and PEP per hop | Architect | Each new graph | Diagram and escalation test |

### Runtime, Cloud-native, and SOC

| Control | Owner | Frequency | Evidence |
|---|---|---|---|
| `Inference Gateway` and guardrails | Platform | Continuous | Block/allow metrics |
| `K8s RBAC` and `NetworkPolicy` | Platform | Each cluster change | Manifest in Git |
| `Service Mesh mTLS/AuthZ` | Platform | Each service change | Mesh policies |
| Multi-tenant isolation | Architect | Each new tenant | Diagram and penetration test |
| Telemetry to SIEM and ATLAS rules | SOC | Continuous | Sample alert and playbook |
| Separate playbook for data drift and adversarial drift | SOC | Seasonal | Updated runbook |
| Rule tuning and FP review | SOC | Monthly | False positive rate report |
| P1/P2 incident SLA | SOC Manager | Each incident | Ticket with acknowledge and contain times |

### Governance and Evidence Pack

| Control | Owner | Frequency | Evidence |
|---|---|---|---|
| Complete evidence pack for each deploy | MLOps | Every deploy | Signed bundle |
| Security suite in Git and regression score | Product Security | Each gate/guardrail change | Suite hash and score vs. baseline |
| Tamper-evident storage | Security | Seasonal audit | Object lock and signature verify |
| Prompt trace and snapshot on incident | SOC | Each incident | Ticket and artifact |
| Mandatory postmortem for high severity | Engineering Manager | Each incident | Postmortem document |

## Short Glossary

Frequently used terms in this article:

| Term | Meaning |
|---|---|
| `MLSecOps` | Applying security across the lifecycle of ML and AI systems |
| `RAG` | Retrieving relevant documents and injecting them into model context |
| `Prompt Injection` | Attempt to change model behavior through a malicious instruction |
| `Artifact` | Storable output such as model, dataset, image, or manifest |
| `Provenance` | Origin and build path of an asset; includes data, code, dependencies, and build process |
| `Evidence Pack` | Auditable collection of evidence about model build, test, release, and runtime |
| `Guardrail` | Control of model input, output, or behavior at runtime |
| `Intent Gate` | Authorization control before agent action or tool invocation |
| `Output Gate` | Review and validation of model or tool output before delivery to downstream |
| `Tool Abuse` / `Tool Misuse` | One concept with two names; identified as `ASI02` in `OWASP ASI` |
| `ASR` | `Attack Success Rate` — adversarial attack success rate relative to baseline |
| `Security Gate` / `Quality Gate` | Stop point in pipeline; on failure, release is halted |
| `Fail-closed` | If a control or gate is undefined or faulty, the system blocks rather than passes |
| `Baseline` | Signed reference version or metric for comparing models and regression tests |
| `Attestation` | Digital document proving an artifact was built with a specified process and policy |
| `SBOM` | Inventory of software components (package, version, dependency) |
| `AI-BOM` / `ML-BOM` | Inventory of AI components including data, base model, metrics, and training evidence |
| `Policy-as-Code` | Converting security policy into executable rules in pipeline or runtime |
| `Tamper-evident` | Storage or signature where any unauthorized change is detectable |
| `HITL` | `Human-in-the-Loop` — human approval for high-risk actions |
| `Canary Deployment` | Gradual release of a new model on a small portion of real traffic |
| `Data Drift` | Change in data or embedding distribution relative to training baseline |
| `Adversarial Drift` | Change in attack behavior at runtime; usually accompanied by suspicious prompt or tool call patterns |
| `Schema Validation` | Checking JSON structure or typed fields and key allowlist |
| `Content-policy Enforcement` | Applying allow/block/redact on prompt or output |
| `Content Safety Check` | Detecting malicious instructions in text, such as ignore previous |
| `Action-policy Verification` | Matching planned tool with policy engine such as `OPA/Cedar` |
| `Constrained Decoding` | Output restriction at tokenizer level, such as JSON mode or grammar |
| `Semantic Consistency Check` | Matching response with retrieved context in RAG |

## Appendix A: Threat, Control, and Tool Reference Card

This card is the consolidated and complete version of the Chapter 12 table and is repeated here for use as a standalone quick reference. Detailed description of each control and layered tool mapping appears in Chapter 12.

| Threat | Framework | Surface | Lifecycle | Phase | Risk | Primary Control | Tool/Stage |
|---|---|---|---|---|---|---|---|
| `Prompt Injection` | `LLM01` | Prompt | Deploy/Monitor | Execution | Critical | Gateway and sanitization | Runtime |
| `Sensitive Data Leak` | `LLM02` | Prompt/Model | Monitor | Execution | High | Output moderation | Gateway |
| `Supply Chain Attack` | `LLM03` | Model/Infra | Train/Deploy | Staging | Critical | Sign and scan | Load |
| `Data Poisoning` | `ML02` | Data | Train | Staging | High | Dataset validation | Data gate |
| `Model Poisoning / Backdoor` | `ML10` | Model | Train | Staging | Critical | Backdoor test | `ART` |
| `Adversarial Evasion` | `ML01` | Model | Deploy | Execution | High | Robustness and ASR gate | Gate 7 |
| `Model Artifact RCE` | — | Model/Infra | Deploy | Staging | Critical | `ModelScan` | Load |
| `Retrieval Poisoning` | `LLM08` | Data/Prompt | Deploy | Execution | High | Allowlist ingest | RAG |
| `Embedding Poisoning` | `LLM08` | Data | Train/Deploy | Staging | High | Source hygiene | RAG |
| `Cross-tenant Leakage` | Arch/Infra (related to `LLM08`) | Infra | Deploy | Execution | Critical | Physical isolation | Multi-tenant |
| `System Prompt Leakage` | `LLM07` | Prompt | Deploy/Monitor | Execution | Critical | Output gate | Gateway |
| `Unbounded Consumption` | `LLM10` | API | Monitor | Execution | Medium | Rate limit | Gateway |
| `Gradient Leakage` | — | Data | Train | Staging | High | Secure aggregation | Federated |
| `Tool Misuse` | `ASI02` | Tool | Monitor | Execution | High | `Intent Gate` | Agent |
| `Model Collapse` | — | Model | Train | Staging | Medium | Diversity evaluation | Gate 7 |
| `Overrefusal` | LLM | Prompt | Monitor | Execution | Medium | Threshold tuning | Gateway |
| `Agent Memory Poisoning` | ASI | Tool/Prompt | Monitor | Execution | High | Sanitize and TTL | Memory |
| `Tool Output Injection` | `ASI/LLM01` | Tool | Monitor | Execution | High | `Output Gate` | Agent |
| `Multi-Agent Escalation` | ASI | Tool | Monitor | Execution | High | PEP per hop | Multi-agent |

## Appendix B: MITRE ATLAS Mapping

More detailed `MITRE ATLAS` mapping for SOC analysis in Chapter 10 and control-oriented mapping in Chapter 12 is provided there; this table is a summary reference.

| Threat | Technique | ID |
|---|---|---|
| `Prompt Injection` | `LLM Prompt Injection` | `AML.T0051` |
| `Jailbreak` | `LLM Jailbreak` | `AML.T0054` |
| `Data Poisoning` | `Poison Training Data` | `AML.T0020` |
| `Model Extraction` | `Exfiltration via AI Inference API` | `AML.T0024` |
| `Adversarial Evasion` | `Evade AI Model` | `AML.T0015` |
| `Supply Chain` | `Publish Poisoned Models` | `AML.T0058` |
| `RAG Poisoning` | `RAG Poisoning` | `AML.T0070` |
| `Memory Poisoning` | `AI Agent Context Poisoning` | `AML.T0080` |
| `Tool Abuse` | `AI Agent Tool Invocation` | `AML.T0053` |

## References

> Note: This section is provided as a working reference list. For official publication, each reference should be converted to a standard bibliography format (e.g., `IEEE` or `APA`) with author, year, publisher, and `DOI`/`URL` where available.

### Frameworks and Standards

- OpenSSF (2025). *Visualizing Secure MLOps (MLSecOps) Whitepaper*. OpenSSF AI/ML Security Working Group.
- NIST (2023). *AI Risk Management Framework (AI RMF 1.0)*.
- NIST (2024). *Generative AI Profile (NIST-AI-600-1)*.
- ISO/IEC 42001:2023. *Artificial Intelligence — Management System*.
- ISO/IEC 23894:2023. *Artificial Intelligence — Guidance on Risk Management*.
- European Union (2024). *EU AI Act*.
- Cloud Security Alliance (2025). *MAESTRO — Multi-Agent Environment Security Framework*.

### Threat Taxonomy and Security Guides

- OWASP (2025). *Top 10 for LLM Applications (2025)*.
- OWASP. *Top 10 for Agentic Applications* / *Agentic Security Initiative*.
- OWASP. *Machine Learning Security Top 10* (`draft` status).
- OWASP. *LLM Verification Standard (LLMSVS)*.
- MITRE. *ATLAS — Adversarial Threat Landscape for AI Systems*. atlas.mitre.org
- *AI Vulnerability Database (AVID)*. avidml.org
- *AI Incident Database*. incidentdatabase.ai

### Open-Source Tools and Projects

- `Adversarial Robustness Toolbox (ART)` — classic model adversarial testing
- `Microsoft PyRIT` — multi-stage LLM red team
- `ModelScan` (Protect AI) — model artifact scan
- `Garak` (NVIDIA) — LLM vulnerability scanner
- `Vigil`, `Promptfoo`, `Giskard` — LLM/RAG test and red team
- `NeMo Guardrails`, `Lakera Guard`, `Patronus AI` — guardrail and gateway
- `lintML` (NVIDIA), `NB Defense` (Protect AI) — linter and notebook/ML code scan
- `Gitleaks`, `Trivy`, `Syft`, `Grype` — secret/SCA/SBOM
- `Checkov`, `tfsec`, `OPA`/`Conftest`, `Kyverno` — IaC and policy-as-code
- `Sigstore / Cosign / Rekor`, `sigstore/model-transparency` (`model-signing`), `SLSA` — model signing and provenance
- `CycloneDX 1.7 (ECMA-424)`, `cdxgen` (`aibom`), `OWASP AIBOM Generator` — SBOM and ML-BOM/AI-BOM
- `AI-exploits` (Protect AI), `AI-Infra-Guard` (Tencent), `Agentic Security`, `PurpleLlama` (Meta), `Mindgard CLI` — MLOps infrastructure and agent testing
- `PrivacyRaven` (Trail of Bits), `ML Privacy Meter`, `TensorFlow Privacy`, `OpenDP` — privacy audit and differential privacy
- `huntr.com` — dedicated AI/ML bug bounty platform
- `awesome-MLSecOps`, `Awesome-LM-SSP`, `awesome-llm-security`, `awesome-llm-supply-chain-security` — MLSecOps reference lists

### Reference Papers and Reports

- Shumailov, I. et al. (2023). *The Curse of Recursion: Training on Generated Data Makes Models Forget* (Model Collapse).
- Greshake, K. et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*.
- Zou, W. et al. (2024). *PoisonedRAG: Knowledge Poisoning Attacks to RAG*.
- Goodfellow, I. et al. (2015). *Explaining and Harnessing Adversarial Examples* (FGSM).
- Carlini, N. & Wagner, D. (2017). *Towards Evaluating the Robustness of Neural Networks*.
- Trail of Bits (2024). *LeftoverLocals (CVE-2023-4969)*.
- HiddenLayer. *SILENT SABOTAGE* — abuse of Pickle-to-SafeTensors conversion bot.
- HiddenLayer. *NOT SO CLEAR: How MLOps Solutions Can Muddy the Waters of Your Supply Chain* (ClearML).
- Sigstore Blog (2025). *Practical Model Signing with Sigstore — model-transparency v1.0*.
- Cohen, S. et al. (2024). *Here Comes the AI Worm (Morris II): Zero-click Worms Targeting GenAI-Powered Applications*.
- Spracklen, J. et al. (2024). *We Have a Package for You: Package Hallucinations by Code-Generating LLMs (Slopsquatting)*.
- ZJU-SEC. *TensorAbuse — Transforming AI Models into Malware by Abusing TensorFlow APIs*.
- Li, Y. et al. (2024). *BadEdit: Backdooring Large Language Models by Model Editing*.
- Xiang, Z. et al. (2024). *BadChain: Backdoor Chain-of-Thought Prompting for LLMs*.
- Morris, J. X. et al. (2023). *Text Embeddings Reveal (Almost) As Much As Text* (Embedding Inversion).
- Rando, J. & Tramèr, F. (2024). *Universal Jailbreak Backdoors from Poisoned Human Feedback*.

> Note on AISecOps: The term `AISecOps` (e.g., in NSFOCUS (2023), *AISecOps Whitepaper*) refers to "using AI in security operations/SOC" and is a separate domain from this guide; this source is cited only for conceptual distinction in Chapter 1.

## Appendix: Claims & Evidence

This appendix maps key claims in the article to verifiable references:

| Topic / Claim | Suggested Reference |
|---|---|
| `Model Collapse` | Shumailov et al., *The Curse of Recursion* (2023) |
| `Indirect / Tool-mediated Injection` | Greshake et al., *Not what you've signed up for* (2023) |
| `RAG / Retrieval Poisoning` | Zou et al., *PoisonedRAG* (2024); `OWASP LLM08` |
| `Adversarial Evasion` | Goodfellow et al. (2015); Carlini & Wagner (2017); `MITRE ATLAS AML.T0015` |
| `Overrefusal` | `OWASP LLM Top 10 (2025)` |
| `Agentic Threats` / `Tool Misuse` | `OWASP Top 10 for Agentic Applications`; CSA `MAESTRO` |
| `System Prompt Leakage` / `LLM07` | `OWASP Top 10 for LLM Applications (2025)` |
| `Vector & Embedding Weaknesses` / `LLM08` | `OWASP Top 10 for LLM Applications (2025)` |
| `LeftoverLocals` (GPU memory leakage) | Trail of Bits, `CVE-2023-4969` (2024) |
| Unsafe HuggingFace models (Pickle RCE) | ReversingLabs / Protect AI `ModelScan` (2025) |
| `AI Worm / Zero-click` | Cohen et al., *Here Comes the AI Worm (Morris II)* (2024) |
| `Models-as-Malware` | ZJU-SEC, *TensorAbuse* |
| `Package Hallucination` | Spracklen et al., *We Have a Package for You* (2024) |
| `Embedding Inversion` | Morris et al., *Text Embeddings Reveal (Almost) As Much As Text* (2023) |
| `Advanced Backdoors (RLHF/CoT/Edit)` | Rando & Tramèr (2024), Xiang et al. (2024), Li et al. (2024) |
| `SILENT SABOTAGE / ClearML` | HiddenLayer Research |
| `PoisonGPT` supply-chain demo | Mithril Security, *PoisonGPT* (2023) |
| Agent API key exposure pattern | Design anti-pattern (illustrative); see Chapter 13 |
| 22 MLOps security controls | OpenSSF *MLSecOps Whitepaper* (2025) |

## Mermaid Diagram Guide

Diagrams render in GitHub, GitLab, and Cursor Preview. For PDF or Word output, PNG or SVG can be exported from `Mermaid Live Editor`. Node labels should preferably be in English, with explanatory captions in the text below the figure.

The figure list includes the `DevSecOps/MLSecOps` view, pipeline, `CT` cycle, `Tool Output Injection`, `Memory Contamination`, `Multi-Agent`, and tool layers.

## GitHub Version

This version is written in Markdown and ready for display on GitHub. Each chapter is wrapped in a `div` with left-to-right direction, and technical terms are written with `inline code`.

## Final Conclusion

AI security is not solved by a single tool, a secure prompt, or a simple test. Security is defensible only when data, model, supply chain, pipeline, runtime, and security operations are viewed as a single, auditable flow.

By separating `Risk Management` from `Threat Modeling`, the 10-stage pipeline, measurable assurance, runtime controls, and the `Evidence Pack`, organizations can deploy models in production with security and auditable defensibility.

`MLSecOps` is a prerequisite for the trustworthiness of AI systems in real environments. An organization that takes `MLSecOps` seriously not only reduces risk but also increases the speed of secure deployment; and this is the difference between "using AI" and "trusting AI."

</div>
