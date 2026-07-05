# Chapter 13: Case Studies and Lessons Learned

## Chapter objective

Case studies show that `MLSecOps` risks are not theoretical. Many incidents arise from the combination of data, model, supply chain, access, and runtime.

> **Sources:** Primary references for each case appear inline below and in the [Claims & Evidence](15-conclusion-appendix.md#appendix-claims-evidence) appendix (Chapter 15).

**Legend:** **Documented incident** = published CVE, vendor research, or widely cited report with primary source. **Illustrative pattern** = design anti-pattern for threat modeling, not a single vendor CVE.

## LeftoverLocals (CVE-2023-4969) — **Documented incident**

`Trail of Bits` reported the `LeftoverLocals` vulnerability in January 2024: leftover LLM response data in GPU memory was readable across processes, leading to cross-application data leakage (Apple, Qualcomm, AMD, and Imagination GPUs).

**Reference:** [Trail of Bits — LeftoverLocals (2024)](https://blog.trailofbits.com/2024/01/16/leftoverlocals-local-llm-data-leakage/); [CVE-2023-4969](https://nvd.nist.gov/vuln/detail/CVE-2023-4969)

Lessons learned:

- Update GPU drivers
- Memory sanitization after inference
- Process isolation in multi-tenant GPU environments

## MLflow and MLOps platform vulnerabilities — **Documented incident**

Multiple CVEs affect `MLflow` (e.g. path traversal and authentication weaknesses in historical versions). Unpatched registry and experiment tracking without hardening can expose cloud credentials and artifacts.

**Reference:** [NVD — MLflow CVE list](https://nvd.nist.gov/vuln/search/results?query=mlflow); [MLflow security advisories](https://github.com/mlflow/mlflow/security/advisories)

Lessons learned:

- Regular patching of the MLOps platform
- Authentication and network segmentation
- Do not expose MLflow to the internet without auth

## ClearML and Confused Learning — **Documented incident**

`HiddenLayer` research on the `ClearML` platform showed that an attacker who compromises an agent or manipulates metadata can poison the entire training pipeline (an attack known as `Confused Learning`).

**Reference:** [HiddenLayer — NOT SO CLEAR: How MLOps Solutions Can Muddy the Waters of Your Supply Chain](https://hiddenlayer.com/research/not-so-clear/)

Lessons learned:

- Harden MLOps agents
- Use allowlists for artifacts
- Separate training environments from one another

## SILENT SABOTAGE (HuggingFace Conversion Bot) — **Documented incident**

In a real supply chain attack, attackers abused a public bot on HuggingFace whose job was converting `pickle` models to `safetensors` to embed malicious code in seemingly safe artifacts.

**Reference:** [HiddenLayer — SILENT SABOTAGE](https://hiddenlayer.com/research/silent-sabotage/)

Lessons learned:

- Changing format to `safetensors` alone does not guarantee security.
- Conversion tools and bots are attack surfaces in their own right.
- Artifact scanning must be performed even on safe formats.

## BentoML and LangChain deserialization RCE — **Documented incident**

Historical CVEs in `BentoML` and `LangChain` allowed unsafe deserialization paths leading to `RCE` on inference or tooling hosts when malicious artifacts were loaded.

**Reference:** [CVE-2025-27520 (BentoML deserialization RCE)](https://nvd.nist.gov/vuln/detail/CVE-2025-27520); [LangChain security advisories](https://github.com/langchain-ai/langchain/security/advisories)

Lessons learned:

- Disable unsafe deserialization
- Sandbox for model serving
- Immediate update after CVE

## HuggingFace: unsafe models at scale — **Documented incident**

`ModelScan` and ReversingLabs research (February 2025) identified more than 3,300 unsafe models on HuggingFace—primarily pickle-based RCE.

**Reference:** [ReversingLabs — Unsafe ML models on Hugging Face (2025)](https://www.reversinglabs.com/blog/unsafe-machine-learning-models-on-hugging-face)

Lessons learned:

- Mandatory scan before load
- Prefer `safetensors` over pickle
- Model source allowlist

## Agent API key exposure pattern — **Illustrative pattern**

In agent architectures, storing provider API keys in prompts, tool configs, or agent memory creates a realistic exposure path: an attacker who achieves prompt injection or tool-output manipulation may cause the agent to leak credentials from context. This is a **design pattern to avoid**, not a single documented vendor incident.

Lessons learned:

- Proxy gateway for API keys (the agent should never see the real key)
- Immediate key rotation after an incident
- Credential isolation from model context

## Pickle-based RCE in model repositories — **Documented incident (pattern class)**

Published models in unsafe formats such as `pickle` can execute code when loaded. Research and scanning campaigns (see HuggingFace case above and Chapter 5) document widespread exposure.

Lessons learned:

- Model loading must be performed in a sandbox.
- Unsafe formats must be restricted or prohibited.
- `ModelScan` and artifact controls must run before load.

## PoisonGPT and the AI supply chain — **Documented incident (research demo)**

In the `PoisonGPT` demonstration (Mithril Security, 2023), researchers intentionally uploaded a poisoned GPT-2 model to Hugging Face to show that a public registry can deliver a backdoored model that generates attacker-controlled output while appearing legitimate. The risk is supply-chain trust in public model hubs—not name typosquatting alone.

**Reference:** [Mithril Security — PoisonGPT (2023)](https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-malicious-model-on-hugging-face/)

Lessons learned:

- Use allowlists for model sources
- Verify signature and provenance
- Record base model hash
- Control for similar names and typosquatting (supplementary; PoisonGPT itself was a deliberate poisoned upload, not a naming collision)

## Prompt injection in public systems — **Documented incident (class)**

Public reports include bypass of chatbot guardrails, instruction leakage, and jailbreaks affecting customer-facing LLM products (e.g. early Bing/Sydney interactions, ChatGPT plugin abuse patterns). Specific CVEs are rare; treat as an operational threat class requiring continuous red team.

**Reference:** OWASP LLM Top 10 `LLM01`; [AI Incident Database](https://incidentdatabase.ai/) (search: prompt injection)

Lessons learned:

- LLM security is not solved by prompt alone.
- `Gateway` and `Output Gate` are essential.
- Red team testing must be performed continuously.

## Shadow LLM usage and data boundary — **Documented incident**

Employees entering source code, logs, or customer data into public LLM tools moves data outside the organizational boundary. Samsung publicly reported restricting ChatGPT use after sensitive code was pasted into the service (2023); similar patterns affect many enterprises.

**Reference:** [Reuters — Samsung ChatGPT leak policy (2023)](https://www.reuters.com/technology/samsung-bans-use-generative-ai-tools-like-chatgpt-after-april-internal-data-leak-2023-05-02/)

Lessons learned:

- A clear policy for public LLM use is required.
- Production data must not enter public services.
- Organizational gateway and output `DLP` must be enabled.

## Indirect prompt injection in Copilot and RAG — **Documented incident (research)**

Greshake et al. (2023) demonstrated indirect injection via retrieved content in LLM-integrated applications; Microsoft Copilot and similar tools have since been studied for retrieval-mediated manipulation.

**Reference:** Greshake, K. et al. (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*; [Microsoft Copilot security guidance](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)

Lessons learned:

- External sources must be assumed untrusted.
- Retrieval output must be sanitized.
- Context must not enter the model without control.

## AI tools inside DevOps — **Illustrative pattern**

Integrating AI into the development workflow—such as code suggestions or chat on a repository—expands the attack surface to code, secrets, and repository permissions. AI-assisted IDE and CI integrations require a separate threat model from production LLM APIs.

Lessons learned:

- Model access to the repository must be limited based on the user's actual permissions.
- Context sent to the model must not include secrets or sensitive data.
- Secret scanning remains a mandatory `DevSecOps` and `MLSecOps` control.

## RAG in organizational knowledge base — **Illustrative pattern**

When all organizational knowledge is ingested into a `Vector DB` without filtering, internal chat can become a path to document disclosure. If ACL is not applied at retrieval time, a user may receive answers based on documents they are not authorized to view.

Lessons learned:

- ACL must be applied at query time.
- A shared index across tenants is dangerous.
- Retrieval leakage testing must be part of the pipeline.

## MCP red team lab — **Illustrative pattern**

Use [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server) and [mcp-injection-experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments) to train teams on tool poisoning, rug pulls, and cross-server shadowing before production MCP rollout. Pair lab exercises with **Snyk Agent Scan** or **mcps-audit** so participants see scanner output on vulnerable configs.

Validate fixes using the [SlowMist MCP Security Checklist](https://github.com/slowmist/MCP-Security-Checklist) as a self-assessment worksheet.

## Summary of lessons

| Failure pattern | Key control |
|---|---|
| Poisoned model from public repository | Signature, allowlist, scan |
| Prompt injection | Gateway, guardrail, red team |
| Data leakage to public LLM | Policy, DLP, employee training |
| RAG without ACL | Authorization at retrieval |
| Agent with excessive access | Scoped tool access and intent gate |
| Ungoverned MCP servers | Allowlist, gateway, Agent Scan / mcps-audit |

## Practical principle

In most incidents, failure is not from the model alone. Failure arises from excessive trust in data, tools, supply chain, context, or the user.
