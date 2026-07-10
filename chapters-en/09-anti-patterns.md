# Chapter 9: Anti-patterns in MLSecOps

## Why anti-patterns matter

Many security failures in AI systems do not stem from lack of advanced tools; they arise from wrong architectural decisions, excessive trust in the model, removal of simple controls, and lack of auditable evidence. This chapter summarizes the most common wrong patterns.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Govern / Map (architecture and control decisions)
- OWASP AI Exchange: [Risk analysis](https://owaspai.org/go/riskanalysis/) — residual risk from missing controls

**Implementation guidance (this guide)**
- [Common anti-patterns](#common-anti-patterns); [Practical principle](#practical-principle)

## Common anti-patterns

| Anti-pattern | Consequence | Correct alternative |
|---|---|---|
| running model without `Gateway` | no input, output, or telemetry control | use `AI Gateway` |
| full trust in model output | execution of wrong or unsafe decisions | output validation and human review |
| using real data in testing | data leakage and privacy violation | masked or controlled synthetic data |
| model without signature | possibility of substitution or tampering | `Model Signing` and attestation |
| RAG without ACL | disclosure of internal documents | authorization at retrieval time |
| Agent with many tools | tool abuse and privilege escalation | `Scoped Tool Access` and [Ch.8 DO/DON'Ts](08-agentic-ai-security.md#agent-security-dos-and-donts) |
| no Evidence Pack | inability to audit or analyze incidents | automatic evidence recording |
| SBOM-only scan without release decision | missing stop point for critical vulns | dependency vulns at control point 4; SBOM/AI-BOM completeness at control point 8 |
| personal ChatGPT/Copilot with prod data | Shadow AI data exfiltration; lifecycle controls give false confidence because unapproved tools bypass them | enterprise AI gateway + AI-AUP — [Ch.11](11-governance-evidence.md#shadow-ai-governance) |
| ungoverned MCP in IDE | tool poisoning, shadow MCP (`MCP09`), rug-pull | MCP allowlist, gateway, `mcps-audit` / Agent Scan — [Ch.7](07-llm-rag-security.md#model-context-protocol-mcp-security) |
| signed model in open K8s namespace | lateral movement, unsigned sidecars, GPU abuse | RBAC, NetworkPolicy, Kyverno — [Ch.16](16-kubernetes-deployment-reference.md) |
| shared `Vector DB` across tenants | information leakage between customers | separate physical index or strict isolation |
| direct Agent connection to `Production DB` | unauthorized data manipulation or export | limited tool, read-only view and `Intent Gate` |
| `Auto-Retrain` without security validation | release of poisoned or degraded model to production | full CT cycle with decision points 4, 7, 8 — [Ch.6](06-pipeline.md) |
| running tools without `Sandbox` | `RCE` or API abuse | separate container, limited egress and allowlist |
| using `Pickle` without scan | deserialization attack and malicious code execution | `ModelScan` and prohibition of unsafe formats |
| no prompt/response logging | inability to analyze incidents | runtime telemetry and controlled retention |
| replacing controls with tools | false sense of security | threat model, policy and evidence |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01`–`LLM10` themes in table
- OWASP Agentic: `ASI02` Tool Misuse; OWASP MCP Top 10 (2025): `MCP03`, `MCP09`
- MITRE ATLAS: `AML.T0053` AI Agent Tool Invocation; `AML.T0080` AI Agent Context Poisoning; `AML.T0110` AI Agent Tool Poisoning

**Implementation guidance (this guide)**
- Cross-references in table above map to Chapters 2, 4–8, 11, 16

**Author practical guidance**
- *Anti-pattern catalog synthesizes recurring field failures; not a normative standard checklist.*

## Model without provenance

One of the most dangerous states is when the team does not know exactly what data, code, dependencies, and parameters were used to build the model. In such a case, even if the model works well, it is not defensible from a security standpoint.

Signs:

- model is in the registry but data origin is unclear.
- training code version is not recorded.
- security test results do not exist.
- model hash and signature are not stored.

### References / Source mapping

**Frameworks and standards**
- OWASP ML Top 10 (draft): `ML06` supply chain, `ML10` model poisoning
- OpenSSF MLSecOps whitepaper (2025): artifact provenance and signing
- MITRE ATLAS: `AML.T0058` publish poisoned models; `AML.T0020` poison training data

**Implementation guidance (this guide)**
- [Model signing and provenance](05-model-artifact-supply-chain.md#provenance-and-signing) (Chapter 5); [Lifecycle control points 2, 8, 9](06-pipeline.md#lifecycle-control-points) (Chapter 6)

## RAG without security boundary

In some architectures, every document in the organization enters the `Vector DB` and the model freely uses it when responding. This turns the chat system into a data disclosure path.

Correct controls:

- `Allowlist` for ingest sources
- access control at query time
- tenant separation
- removal of sensitive or unauthorized documents
- `Retrieval Leakage` testing

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM02` sensitive information disclosure
- MITRE ATLAS: `AML.T0070` RAG poisoning; `AML.T0066` retrieval content crafting

**Implementation guidance (this guide)**
- [RAG security](07-llm-rag-security.md) (Chapter 7); [Data access control](04-data-security-privacy.md) (Chapter 4)

## Agent without tool control

An intelligent agent with access to many sensitive tools can, under `Prompt Injection` or planning error, turn from assistant into an internal attacker. The [agent DO's and DON'Ts checklist in Chapter 8](08-agentic-ai-security.md#agent-security-dos-and-donts) and [six attack domains](08-agentic-ai-security.md#six-attack-domains) provide the positive control model for this anti-pattern.



![](../assets/diagrams/09-anti-patterns_01.png)

### References / Source mapping

**Frameworks and standards**
- OWASP Agentic: `ASI02` Tool Misuse
- OWASP LLM Top 10 (2025): `LLM01` Prompt Injection; `LLM06` Excessive Agency
- MITRE ATLAS: `AML.T0053` AI Agent Tool Invocation; `AML.T0051` LLM Prompt Injection; `AML.T0110` AI Agent Tool Poisoning

**Implementation guidance (this guide)**
- [Agent DO's and DON'Ts](08-agentic-ai-security.md#agent-security-dos-and-donts) (Chapter 8); [Six attack domains](08-agentic-ai-security.md#six-attack-domains) (Chapter 8)

## One-time security testing

The model and its environment constantly change. If security testing runs only at initial release, retraining, data change, prompt change, tool change, or base model change can invalidate previous controls.

Correct pattern:

- security testing on every build
- regression testing for attack scenarios
- signed baseline
- monitoring at `Runtime`

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [Continuous validation](https://owaspai.org/go/continuousvalidation/)
- NIST AI RMF: Measure / Manage (ongoing assurance)
- ISO/IEC 42001: change and monitoring themes

**Implementation guidance (this guide)**
- [Red Team program and security test cadence](06-pipeline.md#red-team-program-and-security-test-cadence) (Chapter 6); [Monitoring](10-monitoring-soc-ir.md) (Chapter 10)

## Practical principle

Wherever the system operates on implicit trust, a likely `Anti-pattern` exists. In `MLSecOps`, trust must be replaced with control, evidence, and limits.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): patterns map to `LLM01`–`LLM10` themes

**Implementation guidance (this guide)**
- [Maturity roadmap — Common mistakes](14-maturity-roadmap.md#common-mistakes-on-the-maturity-path) (Chapter 14)
