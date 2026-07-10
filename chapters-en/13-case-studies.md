# Chapter 13: Case Studies and Lessons Learned

## Chapter objective

Case studies show that `MLSecOps` risks are not theoretical. Many incidents arise from the combination of data, model, supply chain, access, and runtime.

> **Sources:** Primary references for each case appear inline below and in the [Claims & Evidence](15-conclusion-appendix.md#appendix-claims-evidence) appendix (Chapter 15).

**Legend:** **Documented incident** = published CVE, vendor research, or widely cited report with primary source. **Illustrative pattern** = design anti-pattern for threat modeling, not a single vendor CVE.

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS case studies: https://atlas.mitre.org/studies
- OWASP AI Incident Database (community): https://owaspai.org/go/incidentdatabase/

**Implementation guidance (this guide)**
- [Claims & Evidence appendix](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15); [Threat–control map](12-threat-control-tools-map.md) (Chapter 12)

## LeftoverLocals (CVE-2023-4969) — **Documented incident**

`Trail of Bits` reported the `LeftoverLocals` vulnerability in January 2024: leftover LLM response data in GPU memory was readable across processes, leading to cross-application data leakage (Apple, Qualcomm, AMD, and Imagination GPUs).

**Reference:** [Trail of Bits — LeftoverLocals (2024)](https://blog.trailofbits.com/2024/01/16/leftoverlocals-local-llm-data-leakage/); [CVE-2023-4969](https://nvd.nist.gov/vuln/detail/CVE-2023-4969)

Lessons learned:

- Update GPU drivers
- Memory sanitization after inference
- Process isolation in multi-tenant GPU environments

### References / Source mapping

**Frameworks and standards**
- [CVE-2023-4969](https://nvd.nist.gov/vuln/detail/CVE-2023-4969); Trail of Bits — [LeftoverLocals (2024)](https://blog.trailofbits.com/2024/01/16/leftoverlocals-local-llm-data-leakage/)

**Implementation guidance (this guide)**
- [GPU isolation](16-kubernetes-deployment-reference.md#gpu-isolation-and-shared-inference) (Chapter 16); [Claims & Evidence — LeftoverLocals](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## MLflow and MLOps platform vulnerabilities — **Documented incident**

Multiple CVEs affect `MLflow` (e.g. path traversal and authentication weaknesses in historical versions). Unpatched registry and experiment tracking without hardening can expose cloud credentials and artifacts.

**Reference:** [NVD — MLflow CVE list](https://nvd.nist.gov/vuln/search/results?query=mlflow); [MLflow security advisories](https://github.com/mlflow/mlflow/security/advisories)

Lessons learned:

- Regular patching of the MLOps platform
- Authentication and network segmentation
- Do not expose MLflow to the internet without auth

### References / Source mapping

**Frameworks and standards**
- [NVD — MLflow CVE list](https://nvd.nist.gov/vuln/search/results?query=mlflow); [MLflow security advisories](https://github.com/mlflow/mlflow/security/advisories)

**Implementation guidance (this guide)**
- [MLOps infrastructure vulnerabilities](05-model-artifact-supply-chain.md#mlops-infrastructure-vulnerabilities) (Chapter 5)

## ClearML and Confused Learning — **Documented incident**

`HiddenLayer` research on the `ClearML` platform showed that an attacker who compromises an agent or manipulates metadata can poison the entire training pipeline (an attack known as `Confused Learning`).

**Reference:** [HiddenLayer — NOT SO CLEAR: How MLOps Solutions Can Muddy the Waters of Your Supply Chain](https://hiddenlayer.com/research/not-so-clear/)

Lessons learned:

- Harden MLOps agents
- Use allowlists for artifacts
- Separate training environments from one another

### References / Source mapping

**Frameworks and standards**
- HiddenLayer — [NOT SO CLEAR: How MLOps Solutions Can Muddy the Waters of Your Supply Chain](https://hiddenlayer.com/research/not-so-clear/)

**Implementation guidance (this guide)**
- [Poisoning taxonomy across the lifecycle](05-model-artifact-supply-chain.md#poisoning-taxonomy-across-the-lifecycle) (Chapter 5); [Claims & Evidence — SILENT SABOTAGE / ClearML](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## SILENT SABOTAGE (HuggingFace Conversion Bot) — **Documented incident**

In a real supply chain attack, attackers abused a public bot on HuggingFace whose job was converting `pickle` models to `safetensors` to embed malicious code in seemingly safe artifacts.

**Reference:** [HiddenLayer — SILENT SABOTAGE](https://hiddenlayer.com/research/silent-sabotage/)

Lessons learned:

- Changing format to `safetensors` alone does not guarantee security.
- Conversion tools and bots are attack surfaces in their own right.
- Artifact scanning must be performed even on safe formats.

### References / Source mapping

**Frameworks and standards**
- HiddenLayer — [SILENT SABOTAGE](https://hiddenlayer.com/research/silent-sabotage/)

**Implementation guidance (this guide)**
- [AI supply chain](05-model-artifact-supply-chain.md#ai-supply-chain) (Chapter 5); [Claims & Evidence — SILENT SABOTAGE / ClearML](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## BentoML and LangChain deserialization RCE — **Documented incident**

Historical CVEs in `BentoML` and `LangChain` allowed unsafe deserialization paths leading to `RCE` on inference or tooling hosts when malicious artifacts were loaded.

**Reference:** [CVE-2025-27520 (BentoML deserialization RCE)](https://nvd.nist.gov/vuln/detail/CVE-2025-27520); [CVE-2025-68664 (LangChain core serialization injection)](https://nvd.nist.gov/vuln/detail/CVE-2025-68664); [LangChain security advisories](https://github.com/langchain-ai/langchain/security/advisories)

Lessons learned:

- Disable unsafe deserialization
- Sandbox for model serving
- Immediate update after CVE

### References / Source mapping

**Frameworks and standards**
- [CVE-2025-27520 (BentoML deserialization RCE)](https://nvd.nist.gov/vuln/detail/CVE-2025-27520); [CVE-2025-68664 (LangChain core serialization injection)](https://nvd.nist.gov/vuln/detail/CVE-2025-68664); [LangChain security advisories](https://github.com/langchain-ai/langchain/security/advisories)

**Implementation guidance (this guide)**
- [Risk of unsafe formats](05-model-artifact-supply-chain.md#risk-of-unsafe-formats) (Chapter 5); [Claims & Evidence — BentoML / LangChain deserialization RCE](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## HuggingFace: unsafe models at scale — **Documented incident**

`ModelScan` and ReversingLabs research (February 2025) identified more than 3,300 unsafe models on HuggingFace—primarily pickle-based RCE.

**Reference:** [ReversingLabs — Unsafe ML models on Hugging Face (2025)](https://www.reversinglabs.com/blog/unsafe-machine-learning-models-on-hugging-face)

Lessons learned:

- Mandatory scan before load
- Prefer `safetensors` over pickle
- Model source allowlist

### References / Source mapping

**Frameworks and standards**
- ReversingLabs — [Unsafe ML models on Hugging Face (2025)](https://www.reversinglabs.com/blog/unsafe-machine-learning-models-on-hugging-face)

**Implementation guidance (this guide)**
- [Model security controls](05-model-artifact-supply-chain.md#model-security-controls) (Chapter 5); [Claims & Evidence — unsafe HuggingFace models](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## Agent API key exposure pattern — **Illustrative pattern**

In agent architectures, storing provider API keys in prompts, tool configs, or agent memory creates a realistic exposure path: an attacker who achieves prompt injection or tool-output manipulation may cause the agent to leak credentials from context. This is a **design pattern to avoid**, not a single documented vendor incident.

Lessons learned:

- Proxy gateway for API keys (the agent should never see the real key)
- Immediate key rotation after an incident
- Credential isolation from model context

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM02` (sensitive data disclosure); OWASP Agentic: `ASI02` (tool misuse enabling credential paths)

**Implementation guidance (this guide)**
- [Intent Gate](08-agentic-ai-security.md#intent-gate) (Chapter 8); [Key and secret management](05-model-artifact-supply-chain.md#key-and-secret-management) (Chapter 5)

**Author practical guidance**
- *Agent API key exposure is an illustrative design anti-pattern, not a single vendor CVE.*

## Pickle-based RCE in model repositories — **Documented incident (pattern class)**

Published models in unsafe formats such as `pickle` can execute code when loaded. Research and scanning campaigns (see HuggingFace case above and Chapter 5) document widespread exposure.

Lessons learned:

- Model loading must be performed in a sandbox.
- Unsafe formats must be restricted or prohibited.
- `ModelScan` and artifact controls must run before load.

### References / Source mapping

**Frameworks and standards**
- ReversingLabs — [Unsafe ML models on Hugging Face (2025)](https://www.reversinglabs.com/blog/unsafe-machine-learning-models-on-hugging-face); MITRE ATLAS: `AML.T0058` (publish poisoned models)

**Implementation guidance (this guide)**
- [Risk of unsafe formats](05-model-artifact-supply-chain.md#risk-of-unsafe-formats) (Chapter 5); [HuggingFace unsafe models case](#huggingface-unsafe-models-at-scale--documented-incident) (this chapter)

## PoisonGPT and the AI supply chain — **Documented incident (research demo)**

In the `PoisonGPT` demonstration (Mithril Security, 2023), researchers intentionally uploaded a poisoned GPT-2 model to Hugging Face to show that a public registry can deliver a backdoored model that generates attacker-controlled output while appearing legitimate. The risk is supply-chain trust in public model hubs—not name typosquatting alone.

**Reference:** [Mithril Security — PoisonGPT (2023)](https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-malicious-model-on-hugging-face/)

Lessons learned:

- Use allowlists for model sources
- Verify signature and provenance
- Record base model hash
- Control for similar names and typosquatting (supplementary; PoisonGPT itself was a deliberate poisoned upload, not a naming collision)

### References / Source mapping

**Frameworks and standards**
- Mithril Security — [PoisonGPT (2023)](https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-malicious-model-on-hugging-face/)

**Implementation guidance (this guide)**
- [Provenance and signing](05-model-artifact-supply-chain.md#provenance-and-signing) (Chapter 5); [Claims & Evidence — PoisonGPT](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## Prompt injection in public systems — **Documented incident (class)**

Public reports include bypass of chatbot guardrails, instruction leakage, and jailbreaks affecting customer-facing LLM products (e.g. early Bing/Sydney interactions, ChatGPT plugin abuse patterns). Specific CVEs are rare; treat as an operational threat class requiring continuous red team.

**Reference:** OWASP LLM Top 10 `LLM01`; [AI Incident Database](https://incidentdatabase.ai/) (search: prompt injection)

Lessons learned:

- LLM security is not solved by prompt alone.
- `Gateway` and `Output Gate` are essential.
- Red team testing must be performed continuously.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01`; [AI Incident Database](https://incidentdatabase.ai/) (search: prompt injection)

**Implementation guidance (this guide)**
- [Direct and indirect Prompt Injection](07-llm-rag-security.md#direct-and-indirect-prompt-injection) (Chapter 7); [Red Team program](06-pipeline.md#red-team-program-and-security-test-cadence) (Chapter 6)

## Shadow LLM usage and data boundary — **Documented incident**

Employees entering source code, logs, or customer data into public LLM tools moves data outside the organizational boundary. Samsung publicly reported restricting ChatGPT use after sensitive code was pasted into the service (2023); similar patterns affect many enterprises.

**Reference:** [Reuters — Samsung ChatGPT leak policy (2023)](https://www.reuters.com/technology/samsung-bans-use-generative-ai-tools-like-chatgpt-after-april-internal-data-leak-2023-05-02/)

Lessons learned:

- A clear policy for public LLM use is required.
- Production data must not enter public services.
- Organizational gateway and output `DLP` must be enabled.

### References / Source mapping

**Frameworks and standards**
- [Reuters — Samsung ChatGPT leak policy (2023)](https://www.reuters.com/technology/samsung-bans-use-generative-ai-tools-like-chatgpt-after-april-internal-data-leak-2023-05-02/)

**Implementation guidance (this guide)**
- [Shadow AI governance](11-governance-evidence.md#shadow-ai-governance) (Chapter 11); [Claims & Evidence — Shadow AI](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## Indirect prompt injection in Copilot and RAG — **Documented incident (research)**

Greshake et al. (2023) demonstrated indirect injection via retrieved content in LLM-integrated applications; Microsoft Copilot and similar tools have since been studied for retrieval-mediated manipulation.

**Reference:** Greshake, K. et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*; [Microsoft Copilot security guidance](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)

Lessons learned:

- External sources must be assumed untrusted.
- Retrieval output must be sanitized.
- Context must not enter the model without control.

### References / Source mapping

**Frameworks and standards**
- Greshake, K. et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*; [Microsoft Copilot security guidance](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)

**Implementation guidance (this guide)**
- [Retrieval Poisoning](07-llm-rag-security.md#retrieval-poisoning) (Chapter 7); [Claims & Evidence — indirect injection](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

## AI tools inside DevOps — **Illustrative pattern**

Integrating AI into the development workflow—such as code suggestions or chat on a repository—expands the attack surface to code, secrets, and repository permissions. AI-assisted IDE and CI integrations require a separate threat model from production LLM APIs.

Lessons learned:

- Model access to the repository must be limited based on the user's actual permissions.
- Context sent to the model must not include secrets or sensitive data.
- Secret scanning remains a mandatory `DevSecOps` and `MLSecOps` control.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM03` (supply chain); OWASP ASI: `ASI02` (excessive tool/repo access)

**Implementation guidance (this guide)**
- [Common anti-patterns](09-anti-patterns.md#common-anti-patterns) (Chapter 9); [Agent reference architecture](08-agentic-ai-security.md#agent-reference-architecture) (Chapter 8)

**Author practical guidance**
- *AI-in-DevOps integration risks are an illustrative pattern for threat modeling, not a single published CVE.*

## RAG in organizational knowledge base — **Illustrative pattern**

When all organizational knowledge is ingested into a `Vector DB` without filtering, internal chat can become a path to document disclosure. If ACL is not applied at retrieval time, a user may receive answers based on documents they are not authorized to view.

Lessons learned:

- ACL must be applied at query time.
- A shared index across tenants is dangerous.
- Retrieval leakage testing must be part of the pipeline.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04` (RAG corpus poisoning); MITRE ATLAS: `AML.T0070` (RAG poisoning)

**Implementation guidance (this guide)**
- [Three-layer controls in RAG](07-llm-rag-security.md#three-layer-controls-in-rag) (Chapter 7); [RAG without security boundary](09-anti-patterns.md#rag-without-security-boundary) (Chapter 9)

**Author practical guidance**
- *Organizational RAG ACL failure is an illustrative pattern; map to your tenant model and data classification.*

## MCP red team lab — **Illustrative pattern**

Use [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server) and [mcp-injection-experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments) to train teams on tool poisoning, rug pulls, and cross-server shadowing before production MCP rollout. Pair lab exercises with **Snyk Agent Scan** or **mcps-audit** so participants see scanner output on vulnerable configs.

Validate fixes using the [SlowMist MCP Security Checklist](https://github.com/slowmist/MCP-Security-Checklist) as a self-assessment worksheet.

### References / Source mapping

**Frameworks and standards**
- [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server); [mcp-injection-experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments); [SlowMist MCP Security Checklist](https://github.com/slowmist/MCP-Security-Checklist); OWASP MCP Top 10: `MCP03`, `MCP09`

**Implementation guidance (this guide)**
- [Model Context Protocol (MCP) security](07-llm-rag-security.md#model-context-protocol-mcp-security) (Chapter 7); [Claims & Evidence — MCP security lab](15-conclusion-appendix.md#appendix-claims-evidence) (Chapter 15)

**Author practical guidance**
- *MCP red team lab is a training pattern using deliberately vulnerable configs—not a production control.*

## Summary of lessons

| Failure pattern | Key control |
|---|---|
| Poisoned model from public repository | Signature, allowlist, scan |
| Prompt injection | Gateway, guardrail, red team |
| Data leakage to public LLM | Policy, DLP, employee training |
| RAG without ACL | Authorization at retrieval |
| Agent with excessive access | Scoped tool access and intent gate |
| Ungoverned MCP servers | Allowlist, gateway, Agent Scan / mcps-audit |

### References / Source mapping

**Frameworks and standards**
- CVE/NVD entries cited per case above; MITRE ATLAS studies where mapped

**Implementation guidance (this guide)**
- [Anti-patterns](09-anti-patterns.md) (Chapter 9)

## Practical principle

In most incidents, failure is not from the model alone. Failure arises from excessive trust in data, tools, supply chain, context, or the user.

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS case studies: https://atlas.mitre.org/studies

**Implementation guidance (this guide)**
- [Summary of lessons](#summary-of-lessons) (this chapter); [Anti-patterns](09-anti-patterns.md) (Chapter 9)

**Author practical guidance**
- *Composite failure thesis is author synthesis across case studies above—not a single framework control.*
