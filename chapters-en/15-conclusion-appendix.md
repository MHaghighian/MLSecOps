# Chapter 15: Conclusion and Appendices

## Conclusion

`MLSecOps` is a response to the reality that AI systems are not merely classic software. They work with data, models, `Artifact`s, prompts, `RAG`, memory, tools, agents, and probabilistic behavior. Therefore, their security must be distributed across the entire lifecycle.

In this guide, security began at the data layer, extended to the model and supply chain, was managed through lifecycle control points and release decisions, continued at `Runtime` with guardrails and telemetry, and ultimately became auditable through the `Evidence Pack` and governance.

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps whitepaper (2025)
- NIST AI RMF 1.0

**Implementation guidance (this guide)**
- [Lifecycle Overview](01-intro.md#lifecycle-overview) (Chapter 1)
- [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6)
- [What is an Evidence Pack?](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11)

## Key Principles

| Principle | Explanation |
|---|---|
| Security is continuous | A single test before release is not enough. |
| Data is a security asset | Poisoned or sensitive data can make a model insecure. |
| Models must be traceable | Without provenance and signature, a model is not trustworthy. |
| Runtime is critical | Many LLM and Agent attacks occur at runtime. |
| Evidence must be automated | Manual audit after an incident is not reliable. |

> **Last reviewed:** June 2026. This guide was developed based on frameworks and published knowledge through the end of 2025. Given the pace of change in LLM and Agentic AI, readers should periodically review new versions of `OWASP LLM Top 10`, `MITRE ATLAS`, and CycloneDX standards.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025)
- MITRE ATLAS
- CycloneDX AI/ML extensions

**Implementation guidance (this guide)**
- [MLSecOps Principles](01-intro.md#mlsecops-principles) (Chapter 1)

**Author practical guidance**
- *Principle table is author synthesis of lifecycle themes across this guide - not verbatim standard text*

## Compact Checklist

| Domain | Question |
|---|---|
| Data | Are data origin, version, owner, and sensitivity defined? |
| Model | Has the model been scanned, tested, and signed? |
| Supply chain | Has `SBOM/AI-BOM` been produced? |
| Lifecycle controls | Do required decision points block or escalate release when critical criteria fail? |
| RAG | Is ACL applied at retrieval time? |
| Agent | Does every tool call pass through an `Intent Gate`? |
| MCP | Are MCP servers allowlisted, scanned, and routed through a gateway? |
| Shadow AI | Is unsanctioned LLM use covered in threat model and AI-AUP? |
| K8s / infra | Are inference namespaces isolated with NetworkPolicy and signed-image admission? |
| Runtime | Are prompt, response, retrieval, and tool call logged? |
| SOC | Do AI incidents enter the SIEM? |
| Governance | Does an auditable evidence pack exist? |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Map / Govern (control coverage checklist)

**Implementation guidance (this guide)**
- [Minimum security baseline](06-pipeline.md#minimum-security-baseline) (Chapter 6)
- [Production Operational Checklist](#production-operational-checklist) (this chapter)

## Production Operational Checklist

This checklist completes the minimum baseline and `Day-2` operations. If time is limited, close `MUST` lifecycle controls and `Runtime/SOC` controls first. Each control must have a defined owner, frequency, and evidence.

### Minimum RACI

| Activity | R Responsible | A Accountable | C Consulted | I Informed |
|---|---|---|---|---|
| Threat Model | Product Security | CISO / Head of AI | Legal, Data Governance | Engineering Lead |
| Lifecycle Decision Controls | MLOps | Platform Engineering Manager | Security | Model Owner |
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

### Lifecycle Controls, CT, RAG, and Agent

| Control | Owner | Frequency | Evidence |
|---|---|---|---|
| Versioned Threat Model | Product Security | Each new AI service and annually | Threat model document |
| Release decision without undocumented exception | MLOps | Every release | Decision log |
| Security validation for LLM | Security | Every LLM release | Red team report and metrics vs. baseline |
| CT with canary and security regression | MLOps | Each retrain | Canary log and baseline comparison |
| RAG allowlist and reindex playbook | ML Engineer | Each new source | Index hash and regression test |
| Agent intent gate, HITL, and kill switch | AppSec | Each agent release | Policy test and runbook |
| Tool output gate | AppSec | Each agent release | Malicious JSON/Markdown test |
| Multi-agent depth and PEP per hop | Architect | Each new graph | Diagram and escalation test |
| MCP server static scan (`mcps-audit`) | Security | Each MCP server release | `mcp-audit.json` in Evidence Pack |
| MCP gateway and schema pin | Platform | Each MCP server change | Gateway config + hash log |
| Shadow AI AI-AUP and discovery | Governance | Quarterly + on hire | CASB report, exception register |

### Runtime, Cloud-native, and SOC

| Control | Owner | Frequency | Evidence |
|---|---|---|---|
| `Inference Gateway` and guardrails | Platform | Continuous | Block/allow metrics |
| `K8s RBAC` and `NetworkPolicy` | Platform | Each cluster change | Manifest in Git — [Ch.16](16-kubernetes-deployment-reference.md) |
| Kyverno signed-image admission | Platform | Each cluster change | ClusterPolicy in Git |
| MCP workstation audit (Agent Scan) | Security | Monthly / on IDE policy change | Scan report |
| Shadow AI CASB/DLP rules | Security | Continuous | Alert samples + AI-AUP exceptions |
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
| Security suite in Git and regression baseline | Product Security | Each control or guardrail change | Suite hash and score vs. baseline |
| Tamper-evident storage | Security | Seasonal audit | Object lock and signature verify |
| Prompt trace and snapshot on incident | SOC | Each incident | Ticket and artifact |
| Mandatory postmortem for high severity | Engineering Manager | Each incident | Postmortem document |

### References / Source mapping

**Frameworks and standards**
- ISO/IEC 42001: operational control and accountability themes
- NIST AI RMF: Govern / Manage

**Implementation guidance (this guide)**
- [Responsibilities](11-governance-evidence.md#responsibilities) (Chapter 11)
- [Incident response](10-monitoring-soc-ir.md#incident-response) (Chapter 10)
- [Kubernetes deployment reference](16-kubernetes-deployment-reference.md) (Chapter 16)

**Author practical guidance**
- *RACI, frequencies, and evidence columns are illustrative operational patterns - adapt to your org model*

## Short Glossary

Frequently used terms in this guide:

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
| `Security Decision Point` | Decision point where a release is blocked, escalated, or accepted with documented risk |
| `Fail-closed` | If a control or gate is undefined or faulty, the system blocks rather than passes |
| `Baseline` | Signed reference version or metric for comparing models and regression tests |
| `Attestation` | Digital document proving an artifact was built with a specified process and policy |
| `SBOM` | Inventory of software components (package, version, dependency) |
| `AI-BOM` / `ML-BOM` | Inventory of AI components including data, base model, metrics, and training evidence |
| `Policy-as-Code` | Converting security policy into executable rules in release workflows or runtime |
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

### References / Source mapping

**Implementation guidance (this guide)**
- Terminology aligned with [Chapter 1](01-intro.md), [Chapter 6](06-pipeline.md), [Chapter 9](09-anti-patterns.md), and [Chapter 11](11-governance-evidence.md)

**Author practical guidance**
- *Glossary definitions are guide-local usage for consistency - not normative standard definitions*

## Appendix A: Threat, Control, and Tool Reference Card

This card is the consolidated and complete version of the Chapter 12 table and is repeated here for use as a standalone quick reference. Detailed description of each control and layered tool mapping appears in Chapter 12.

> Canonical source: [Chapter 12](12-threat-control-tools-map.md); duplicated here for standalone use - keep in sync.

| Threat | Framework | Surface | Lifecycle | Phase | Risk | Primary Control | Tool/Stage |
|---|---|---|---|---|---|---|---|
| `Prompt Injection` | `LLM01` | Prompt | Deploy/Monitor | Execution | Critical | Gateway and sanitization | Runtime |
| `Sensitive Data Leak` | `LLM02` | Prompt/Model | Monitor | Execution | High | Output moderation | Gateway |
| `Supply Chain Attack` | `LLM03` | Model/Infra | Train/Deploy | Staging | Critical | Sign and scan | Load |
| `Data Poisoning` | `ML02` | Data | Train | Staging | High | Dataset validation | Control point 4 |
| `Model Poisoning / Backdoor` | `ML10` | Model | Train | Staging | Critical | Backdoor test | `ART` |
| `Adversarial Evasion` | `ML01` | Model | Deploy | Execution | High | Robustness and ASR validation | Security validation |
| `Model Artifact RCE` | — | Model/Infra | Deploy | Staging | Critical | `ModelScan` | Load |
| `Retrieval Poisoning` | `LLM04` *(RAG corpus poisoning)* | Data/Prompt | Deploy | Execution | High | Allowlist ingest | RAG |
| `Embedding Poisoning` | `LLM08` | Data | Train/Deploy | Staging | High | Source hygiene | RAG |
| `Cross-tenant Leakage` | Arch/Infra (related to `LLM08`) | Infra | Deploy | Execution | Critical | Physical isolation | Multi-tenant |
| `System Prompt Leakage` | `LLM07` | Prompt | Deploy/Monitor | Execution | Critical | Output gate | Gateway |
| `Unbounded Consumption` | `LLM10` | API | Monitor | Execution | Medium | Rate limit | Gateway |
| `Gradient Leakage` | — | Data | Train | Staging | High | Secure aggregation | Federated |
| `Tool Misuse` | `ASI02` | Tool | Monitor | Execution | High | `Intent Gate` | Agent |
| `Model Collapse` | — | Model | Train | Staging | Medium | Diversity evaluation | Security validation |
| `Overrefusal` | LLM | Prompt | Monitor | Execution | Medium | Threshold tuning | Gateway |
| `Agent Memory Poisoning` | ASI | Tool/Prompt | Monitor | Execution | High | Sanitize and TTL | Memory |
| `Tool Output Injection` | `ASI/LLM01` | Tool | Monitor | Execution | High | `Output Gate` | Agent |
| `Multi-Agent Escalation` | ASI | Tool | Monitor | Execution | High | PEP per hop | Multi-agent |
| `MCP Tool Poisoning` | `MCP03`/MCP09 | Tool | Deploy/Monitor | Execution | Critical | Gateway + schema pin | `mcps-audit`, gateway |
| `Shadow MCP Server` | MCP09 | Tool/IDE | Monitor | Execution | High | Allowlist + Agent Scan | Workstation audit |
| `Shadow AI Data Exfil` | Governance | Prompt | Monitor | Execution | Critical | AI-AUP + enterprise gateway | CASB/DLP |
| `K8s Inference Exposure` | Infra | Infra | Deploy | Staging | Critical | RBAC + NetworkPolicy | Ch.16 manifests |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025)
- OWASP ML Top 10
- OWASP Agentic (`ASI02`)
- OWASP MCP Top 10 (`MCP03`, `MCP09`)

**Implementation guidance (this guide)**
- [Primary Mapping](12-threat-control-tools-map.md#primary-mapping) (Chapter 12); duplicate card for standalone use in this appendix

## Appendix B: MITRE ATLAS Mapping

More detailed `MITRE ATLAS` mapping for SOC analysis in Chapter 10 and control-oriented mapping in Chapter 12 is provided there; this table is a summary reference.

> Canonical source: [Chapter 12](12-threat-control-tools-map.md); duplicated here for standalone use - keep in sync.

| Threat | Technique | ID |
|---|---|---|
| `Prompt Injection` | `LLM Prompt Injection` | `AML.T0051` |
| `Jailbreak` | `LLM Jailbreak` | `AML.T0054` |
| `Data Poisoning` | `Poison Training Data` | `AML.T0020` |
| `Model Extraction` | `Exfiltration via AI Inference API` | `AML.T0024` |
| `Adversarial Evasion` | `Evade AI Model` | `AML.T0015` |
| `Supply Chain` | `Publish Poisoned Models` | `AML.T0058` |
| `RAG Poisoning` | `RAG Poisoning` | `AML.T0070` |
| `Retrieval Content Crafting` | `Retrieval Content Crafting` | `AML.T0066` |
| `Memory Poisoning` | `AI Agent Context Poisoning` | `AML.T0080` |
| `Tool Abuse` | `AI Agent Tool Invocation` | `AML.T0053` |
| `AI Reconnaissance` | `Discover AI Agent Configuration` | `AML.T0084` |
| `LLM Data Leakage` | `LLM Data Leakage` | `AML.T0057` |
| `Agent-tool Exfiltration` | `Exfiltration via AI Agent Tool Invocation` | `AML.T0086` |
| AI Worm Propagation *(emerging)* | LLM Prompt Self-Replication (closest match); related RAG/context poisoning | `AML.T0061` |
| Model Resource Abuse | `Cost Harvesting` | `AML.T0034` |

> **Appendix numbering:** Appendix C was reserved in earlier drafts and removed in v0.1.2. Numbering skips to Appendix D to avoid renumbering existing cross-references. **Appendix E** (Implementation Reference) is a separate chapter: [17-appendix-e-implementation-reference.md](17-appendix-e-implementation-reference.md).

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: techniques cited in table (e.g. `AML.T0051`, `AML.T0020`, `AML.T0066`, `AML.T0070`, `AML.T0034`)

**Implementation guidance (this guide)**
- [MITRE ATLAS Mapping](12-threat-control-tools-map.md#mitre-atlas-mapping) (Chapter 12)
- [Threat analysis with MITRE ATLAS](10-monitoring-soc-ir.md#threat-analysis-with-mitre-atlas) (Chapter 10)

## Appendix D: Managed AI Services Security Reference

Use this checklist when the organization consumes provider-hosted models (Azure OpenAI, Amazon Bedrock, Google Vertex AI, or similar) and does not control base model weights.

### Shared responsibility

| Provider typically manages | Customer must manage |
|---|---|
| Base model, platform patching, provider safety features | Prompt/RAG data boundary, tenant authz, gateway, DLP, keys, logging, IR |
| Platform SLA and regional deployment options | Configuration review, enabled safety settings, evidence at control points 8–9 |

### Pre-production checklist

- [ ] Shared-responsibility boundary documented in threat model ([Ch.2](02-scope-risk-threat-model.md#managed-ai-services-security-reference))
- [ ] Approved model/deployment ID, region, and API version recorded (control point 9)
- [ ] Enterprise gateway or API proxy; no long-lived keys in application code
- [ ] DLP on prompt ingress and response egress
- [ ] RAG ingest allowlist and retrieval-time ACL
- [ ] Prompt-injection and leakage test suite at control point 7 ([Ch.7 verification](07-llm-rag-security.md#llm-verification-approach))
- [ ] Runtime logging to SIEM with retention and access control
- [ ] If agents/tools enabled: [Ch.8](08-agentic-ai-security.md) controls (Intent Gate, scoped tools, HITL)
- [ ] Shadow AI policy blocks unsanctioned consumer tools for same data class ([Ch.11](11-governance-evidence.md#shadow-ai-governance))

### Evidence Pack fields (managed API)

| Field | Example |
|---|---|
| `provider` | `azure-openai`, `bedrock`, `vertex` |
| `model_deployment_id` | deployment or endpoint name |
| `region` | `eastus`, `eu-west-1` |
| `api_version` | provider API version string |
| `config_snapshot_hash` | hash of safety/content-filter settings |
| `gateway_policy_version` | internal gateway rule set version |
| `security_validation_report` | control point 7 test report URI |
| `release_decision` | control point 8 approval record |

### OWASP v1 publication readiness (community guide)

This guide is a **community reference**, not an OWASP publication. Before external submission or major release, reviewers should confirm:

1. Terminology aligned across Ch.1, 6, 9, 11 (lifecycle **control points** and **release decisions**)
2. OWASP relationship stated in Ch.1; no implied OWASP endorsement
3. Tool examples marked informative; commands in Ch.12 appendix only
4. Case studies labeled documented vs illustrative (Ch.13)
5. Managed AI and agent paths documented for non-training audiences
6. `CHANGELOG.md` and version in README updated

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025)
- cloud provider shared-responsibility models (Azure, AWS, Google - vendor docs)

**Implementation guidance (this guide)**
- [Managed AI services security reference](02-scope-risk-threat-model.md#managed-ai-services-security-reference) (Chapter 2)
- [LLM verification approach](07-llm-rag-security.md#llm-verification-approach) (Chapter 7)
- [Evidence Pack fields](#evidence-pack-fields-managed-api) (this appendix)

**Author practical guidance**
- *Publication readiness checklist is for community guide maintainers - not an OWASP submission requirement*

## Traceability and source mapping convention

This guide distinguishes four types of security content. Per-section **`References / Source mapping`** blocks (from v1.1.0) make that distinction explicit for audit, governance, and peer review—addressing community feedback on traceability ([GitHub Issue #1](https://github.com/l4tr0d3ctism/MLSecOps/issues/1)).

| Type | Meaning | How it appears |
|---|---|---|
| **Frameworks and standards** | Controls or threats defined by OWASP, MITRE ATLAS, NIST AI RMF, ISO/IEC 42001, OpenSSF, CSA MAESTRO, EU AI Act, or OWASP AI Exchange | Cited with ID or permalink |
| **Framework interpretation** | Practical reading of a standard for MLSecOps lifecycle (e.g., mapping to control points) | Cited framework + pointer to this guide's lifecycle model |
| **Implementation guidance (this guide)** | Operational patterns: control points, Evidence Pack fields, playbooks, tool examples | Labeled *this guide*; not normative standard text |
| **Emerging / research** | Research-stage or plausible threats not yet standardized | Paper/preprint citation or *emerging — not standardized* note |

### Reference block template

Each major section may end with:

```markdown
### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): LLM01
- MITRE ATLAS: AML.T0051
- NIST AI RMF: Map / Measure
- ISO/IEC 42001: (relevant clause, when applicable)

**Implementation guidance (this guide)**
- [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6)

**Emerging / research** *(if applicable)*
- Author et al. (year). *Title*. venue/URL — *emerging / not standardized*

**Author practical guidance** *(if applicable)*
- *Evidence Pack field names and release thresholds are illustrative implementation patterns.*
```

**Rollout status (v1.1.0):** All guide chapters (1–17) include per-section `References / Source mapping` blocks on every major `##` section, using the template above. The chapter-level [References](#references) section below is the master bibliography and does not repeat a self-referential mapping block.

## References

### Frameworks and Standards

- OpenSSF (2025). *Visualizing Secure MLOps (MLSecOps) Whitepaper*. https://openssf.org/blog/2025/01/22/visualizing-secure-mlops/
- NIST (2023). *AI Risk Management Framework (AI RMF 1.0)*. https://www.nist.gov/itl/ai-risk-management-framework
- NIST (2024). *Generative AI Profile (NIST-AI-600-1)*.
- ISO/IEC 42001:2023. *Artificial Intelligence — Management System*.
- ISO/IEC 23894:2023. *Artificial Intelligence — Guidance on Risk Management*.
- European Union (2024). *EU AI Act*. https://artificialintelligenceact.eu/
- Cloud Security Alliance (2025). *MAESTRO — Multi-Agent Environment Security Framework*.

### Threat Taxonomy and Security Guides

- OWASP (2024–2025). *AI Exchange* — comprehensive AI security and privacy framework. https://owaspai.org/
- OWASP (2025). *Top 10 for LLM Applications (2025)*. https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP. *Top 10 for Agentic Applications* / *Agentic Security Initiative*.
- OWASP. *Machine Learning Security Top 10* (`draft` status).
- OWASP. *LLM Verification Standard (LLMSVS)*.
- OWASP. *MCP Top 10* (2025). https://owasp.org/www-project-mcp-top-10/
- OWASP Cheat Sheet Series. *MCP Security*. https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html
- Hou et al. (2025). *Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions*. arXiv:2503.23278
- Radosevich, B. & Halloran, J. T. (2025). *MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits*. arXiv:2504.03767
- Narajala, V. S. & Habler, I. (2025). *Enterprise-Grade Security for the Model Context Protocol (MCP): Frameworks and Mitigation Strategies*. arXiv:2504.08623
- e2b-dev. *awesome-mcp-gateways*. https://github.com/e2b-dev/awesome-mcp-gateways
- AIM-Intelligence. *awesome-mcp-security*. https://github.com/AIM-Intelligence/awesome-mcp-security
- Puliczek. *awesome-mcp-security* (community). https://github.com/Puliczek/awesome-mcp-security
- SlowMist. *MCP Security Checklist*. https://github.com/slowmist/MCP-Security-Checklist
- razashariff. *mcps-audit*. https://github.com/razashariff/mcps-audit
- invariantlabs-ai. *mcp-scan* (Snyk Agent Scan). https://github.com/invariantlabs-ai/mcp-scan
- riseandignite. *MCP-Shield*. https://github.com/riseandignite/mcp-shield
- eqtylab. *MCP Guardian*. https://github.com/eqtylab/mcp-guardian
- StacklokLabs. *ToolHive*. https://github.com/StacklokLabs/toolhive
- harishsg993010. *Damn Vulnerable MCP Server*. https://github.com/harishsg993010/damn-vulnerable-MCP-server
- MITRE. *ATLAS — Adversarial Threat Landscape for AI Systems*. https://atlas.mitre.org/
- *AI Vulnerability Database (AVID)*. https://avidml.org/
- *AI Incident Database*. https://incidentdatabase.ai/

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
- Trail of Bits (2024). *LeftoverLocals (CVE-2023-4969)*. https://blog.trailofbits.com/2024/01/16/leftoverlocals-local-llm-data-leakage/
- HiddenLayer. *SILENT SABOTAGE* — abuse of Pickle-to-SafeTensors conversion bot. https://hiddenlayer.com/research/silent-sabotage/
- HiddenLayer. *NOT SO CLEAR: How MLOps Solutions Can Muddy the Waters of Your Supply Chain* (ClearML). https://hiddenlayer.com/research/not-so-clear/
- Mithril Security (2023). *PoisonGPT*. https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-malicious-model-on-hugging-face/
- Röttger, P. et al. (2024). *Safety-Tuned LLMs Are Not Safer* (Overrefusal and safety trade-offs).
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

This appendix maps key claims in the guide to verifiable references:

| Topic / Claim | Suggested Reference |
|---|---|
| `Model Collapse` | Shumailov et al., *The Curse of Recursion* (2023) |
| `Indirect / Tool-mediated Injection` | Greshake et al., *Not what you've signed up for* (2023) |
| `RAG / Retrieval Poisoning` | Zou et al., *PoisonedRAG* (2024); `OWASP LLM04` (RAG corpus poisoning) |
| `Adversarial Evasion` | Goodfellow et al. (2015); Carlini & Wagner (2017); `MITRE ATLAS AML.T0015` |
| `Overrefusal` | Röttger et al., *Safety-Tuned LLMs Are Not Safer* (2024); operational threshold tuning (not an OWASP Top 10 category) |
| `Agentic Threats` / `Tool Misuse` | `OWASP Top 10 for Agentic Applications`; CSA `MAESTRO` |
| `System Prompt Leakage` / `LLM07` | `OWASP Top 10 for LLM Applications (2025)` |
| `Vector & Embedding Weaknesses` / `LLM08` | `OWASP Top 10 for LLM Applications (2025)` |
| `LeftoverLocals` (GPU memory leakage) | Trail of Bits, `CVE-2023-4969` (2024); https://blog.trailofbits.com/2024/01/16/leftoverlocals-local-llm-data-leakage/ |
| Unsafe HuggingFace models (Pickle RCE) | ReversingLabs / Protect AI `ModelScan` (2025); https://www.reversinglabs.com/blog/unsafe-machine-learning-models-on-hugging-face |
| `AI Worm / Zero-click` | Cohen et al., *Here Comes the AI Worm (Morris II)* (2024) |
| `Models-as-Malware` | ZJU-SEC, *TensorAbuse* |
| `Package Hallucination` | Spracklen et al., *We Have a Package for You* (2024) |
| `Embedding Inversion` | Morris et al., *Text Embeddings Reveal (Almost) As Much As Text* (2023) |
| `Advanced Backdoors (RLHF/CoT/Edit)` | Rando & Tramèr (2024), Xiang et al. (2024), Li et al. (2024) |
| `SILENT SABOTAGE / ClearML` | HiddenLayer Research; https://hiddenlayer.com/research/silent-sabotage/ ; https://hiddenlayer.com/research/not-so-clear/ |
| `PoisonGPT` supply-chain demo | Mithril Security, *PoisonGPT* (2023); https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-malicious-model-on-hugging-face/ |
| Agent API key exposure pattern | Design anti-pattern (illustrative); see Chapter 13 |
| 22 MLOps security controls | OpenSSF *MLSecOps Whitepaper* (2025) |
| Shadow AI (Samsung pattern) | Ch.13 case study; CTAIO / Proofpoint shadow-AI references in Ch.11 |
| MCP security lab | Ch.13 MCP red team lab; OWASP MCP Top 10 v0.1; `mcps-audit`, Agent Scan |
| BentoML / LangChain deserialization RCE | CVE-2025-27520 (BentoML, GHSA-33xw-247w-6hmc); CVE-2025-68664 (LangChain core, GHSA-c67j-w6g6-q2cm) |
| Kubernetes MLSecOps baseline | Ch.16 (patterns + upstream refs; no bundled manifests) |

### References / Source mapping

**Frameworks and standards**
- Primary sources cited in [References](#references) (this chapter); CVE/NVD and vendor research URLs in table rows

**Implementation guidance (this guide)**
- [Case studies](13-case-studies.md) (Chapter 13) for incident labels; per-chapter claims map to lifecycle controls in Chapters 5-11

## Mermaid Diagram Guide

Diagrams in `chapters-en/` are **PNG images** (`assets/diagrams/`). Mermaid **source** for regeneration lives in `assets/diagrams/source/*.mmd` (edit there, then re-export PNG for Word/PDF).

GitHub's built-in Mermaid viewer is unreliable for complex flowcharts (layout errors, old parser); PNG avoids the loading spinner and *Unable to render rich display* errors.

### References / Source mapping

**Implementation guidance (this guide)**
- Diagram assets: `assets/diagrams/`; Mermaid source: `assets/diagrams/source/*.mmd`

**Author practical guidance**
- *PNG-first publishing choice is a maintainer workflow decision - not a security standard*

## GitHub Version

**Current release:** v1.1.1 (2026-07-16). See [CHANGELOG.md](../CHANGELOG.md) and [GitHub Releases](https://github.com/l4tr0d3ctism/MLSecOps/releases/tag/v1.1.1).

This guide is maintained as Markdown in the [MLSecOps repository](https://github.com/l4tr0d3ctism/MLSecOps). Technical terms use `inline code` formatting where helpful for scanability.

### References / Source mapping

**Implementation guidance (this guide)**
- [GitHub Version](#github-version) (this section); repository README and `CHANGELOG.md` for release metadata

## Final Conclusion

AI security is not solved by a single tool, a secure prompt, or a simple test. Security is defensible only when data, model, supply chain, lifecycle decisions, runtime, and security operations are viewed as a single, auditable flow.

### What this guide contributes

Beyond compiling OWASP, OpenSSF, NIST, and related sources, this **Practical Reference Guide** adds four operational constructs:

1. **Ten lifecycle control points** from change initiation through monitoring—not only a threat list.
2. **Explicit separation** of evidence-producing steps from **blocking release decisions** (control points 4, 7, 8) and **integrity verification** (9).
3. **`Evidence Pack`** as the auditable output bundle per release.
4. A **single lifecycle thread** linking threat modeling, runtime, SOC, and governance.

Teams implementing in production should use [Appendix E: Implementation Reference](17-appendix-e-implementation-reference.md) (architecture cards, decision matrix, templates, playbooks, master control matrix).

By separating `Risk Management` from `Threat Modeling`, lifecycle control points, measurable assurance, runtime controls, and the `Evidence Pack`, organizations can deploy models in production with security and auditable defensibility.

Organizations that adopt the practices in this guide—risk management, threat modeling, lifecycle release decisions, runtime controls, and the `Evidence Pack`—can improve the **auditability and defensibility** of production AI deployments. This guide is one input among many (OpenSSF, OWASP, NIST, ISO, legal counsel); it is **not** a certified standard or a sole prerequisite for trustworthy AI.

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps whitepaper (2025)
- NIST AI RMF
- OWASP LLM Top 10 (2025)
- ISO/IEC 42001

**Implementation guidance (this guide)**
- [What this guide contributes](#what-this-guide-contributes) (this section)
- [Appendix E: Implementation Reference](17-appendix-e-implementation-reference.md) (Chapter 17)

**Author practical guidance**
- *Four operational constructs (control points, release decisions, Evidence Pack, lifecycle thread) are author additions beyond cited frameworks*
