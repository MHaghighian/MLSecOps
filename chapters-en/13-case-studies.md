# Chapter 13: Case Studies and Lessons Learned

<div dir="ltr">

## Chapter objective

Case studies show that `MLSecOps` risks are not theoretical. Many incidents arise from the combination of data, model, supply chain, access, and runtime.

> Note on sources: Dates and `CVE` identifiers mentioned in this chapter are based on publicly published reports (including Trail of Bits, HiddenLayer, ReversingLabs, and OWASP). For formal citation, the full mapping of claims to sources appears in the "Claims & Evidence" appendix in Chapter 15; it is recommended to add a direct link to the report for each case before publication.

## LeftoverLocals (CVE-2023-4969)

`Trail of Bits` reported the `LeftoverLocals` vulnerability in January 2024: leftover LLM response data in GPU memory was readable across processes, leading to cross-application data leakage (Apple, Qualcomm, AMD, and Imagination GPUs).

Lessons learned:

- Update GPU drivers
- Memory sanitization after inference
- Process isolation in multi-tenant GPU environments

## MLflow and MLOps platform vulnerabilities

Vulnerabilities in `MLflow` (including path traversal and credential access) show that registry and experiment tracking without hardening can expose the entire cloud account to risk.

Lessons learned:

- Regular patching of the MLOps platform
- Authentication and network segmentation
- Do not expose MLflow to the internet without auth

## ClearML and Confused Learning

`HiddenLayer` research on the `ClearML` platform showed that an attacker who compromises an agent or manipulates metadata can poison the entire training pipeline (an attack known as `Confused Learning`).

Lessons learned:

- Harden MLOps agents
- Use allowlists for artifacts
- Separate training environments from one another

## SILENT SABOTAGE (HuggingFace Conversion Bot)

In a real supply chain attack, attackers abused a public bot on HuggingFace whose job was converting `pickle` models to `safetensors` to embed malicious code in seemingly safe artifacts.

Lessons learned:

- Changing format to `safetensors` alone does not guarantee security.
- Conversion tools and bots are attack surfaces in their own right.
- Artifact scanning must be performed even on safe formats.

## BentoML, LangChain, and RCE

Deserialization vulnerabilities in `BentoML` and `LangChain` led to `RCE` on inference servers. Common pattern: unsafe artifact or pickle load without sandbox.

Lessons learned:

- Disable unsafe deserialization
- Sandbox for model serving
- Immediate update after CVE

## HuggingFace: more than 3,300 unsafe models

`ModelScan` and ReversingLabs research (February 2025) identified more than 3,300 unsafe models on HuggingFace—primarily pickle-based RCE.

Lessons learned:

- Mandatory scan before load
- Prefer `safetensors` over pickle
- Model source allowlist

## Agent API key exposure pattern (illustrative)

In agent architectures, storing provider API keys in prompts, tool configs, or agent memory creates a realistic exposure path: an attacker who achieves prompt injection or tool-output manipulation may cause the agent to leak credentials from context. This is a **design pattern to avoid**, not a single documented vendor incident.

Lessons learned:

- Proxy gateway for API keys (the agent should never see the real key)
- Immediate key rotation after an incident
- Credential isolation from model context

## Pickle-based RCE in model repositories

Some published models in unsafe formats such as `pickle` can execute code when loaded. If a team loads a model from a public repository without scanning and isolation, malicious code execution is possible in the training or inference environment. (Technical details on unsafe formats and controls appear in Chapter 5.)

Lessons learned:

- Model loading must be performed in a sandbox.
- Unsafe formats must be restricted or prohibited.
- `ModelScan` and artifact controls must run before load.

## PoisonGPT and the AI supply chain

In the `PoisonGPT` demonstration (Mithril Security, 2023), researchers intentionally uploaded a poisoned GPT-2 model to Hugging Face to show that a public registry can deliver a backdoored model that generates attacker-controlled output while appearing legitimate. The risk is supply-chain trust in public model hubs—not name typosquatting alone.

Lessons learned:

- Use allowlists for model sources
- Verify signature and provenance
- Record base model hash
- Control for similar names and typosquatting (supplementary; PoisonGPT itself was a deliberate poisoned upload, not a naming collision)

## Prompt injection in public systems

Incidents related to `Prompt Injection` have shown that language models may ignore system instructions, bypass restrictions, or disclose information that should not appear in the output.

Lessons learned:

- LLM security is not solved by prompt alone.
- `Gateway` and `Output Gate` are essential.
- Red team testing must be performed continuously.

## Data leakage from organizational use of public LLMs

In some organizations, employees entered source code, logs, customer data, or internal documents into public LLM tools. This moves data outside the organization's control boundary.

Lessons learned:

- A clear policy for public LLM use is required.
- Production data must not enter public services.
- Organizational gateway and output `DLP` must be enabled.

## Indirect prompt injection in Copilot and RAG

In an indirect attack, a malicious instruction is placed inside an email, document, web page, or ticket. The `RAG` system or copilot retrieves that document and the model accepts the hidden instruction as context.

Lessons learned:

- External sources must be assumed untrusted.
- Retrieval output must be sanitized.
- Context must not enter the model without control.

## AI tools inside DevOps

Integrating AI into the development workflow—such as code suggestions or chat on a repository—expands the attack surface to code, secrets, and repository permissions. Examples such as `GitLab Duo` show that the threat model for AI inside IDE/CI must be defined separately.

Lessons learned:

- Model access to the repository must be limited based on the user's actual permissions.
- Context sent to the model must not include secrets or sensitive data.
- Secret scanning remains a mandatory `DevSecOps` and `MLSecOps` control.

## RAG in organizational knowledge base

When all organizational knowledge is ingested into a `Vector DB` without filtering, internal chat can become a path to document disclosure. If ACL is not applied at retrieval time, a user may receive answers based on documents they are not authorized to view.

Lessons learned:

- ACL must be applied at query time.
- A shared index across tenants is dangerous.
- Retrieval leakage testing must be part of the pipeline.

## Summary of lessons

| Failure pattern | Key control |
|---|---|
| Poisoned model from public repository | Signature, allowlist, scan |
| Prompt injection | Gateway, guardrail, red team |
| Data leakage to public LLM | Policy, DLP, employee training |
| RAG without ACL | Authorization at retrieval |
| Agent with excessive access | Scoped tool access and intent gate |

## Practical principle

In most incidents, failure is not from the model alone. Failure arises from excessive trust in data, tools, supply chain, context, or the user.

</div>
