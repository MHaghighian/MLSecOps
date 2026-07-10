# Chapter 7: LLM and RAG Security

> **Chapter guide:** This chapter covers LLM runtime threats (§ threats and controls), RAG architecture and poisoning (§ RAG sections), multi-tenant and gateway patterns (mid-chapter), and MCP security (§ MCP — often used by agents). If you only consume a **managed API** without custom training, prioritize gateway, RAG ACL, verification approach, and MCP sections; pair with [Ch.2 managed AI](02-scope-risk-threat-model.md#managed-ai-services-security-reference). Agent runtime controls: [Chapter 8](08-agentic-ai-security.md).

## How LLM security differs from classic ML

In classic models, security focus is mostly on training data, the model, numeric or image input, and `Artifact`. But in `LLM` and `RAG` systems, a large share of risk shifts to runtime. The model interacts with the user, documents, tools, memory, and organizational policies—and each can be an attack surface.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): runtime-focused risks (`LLM01`–`LLM10`)
- NIST AI RMF (2023): Map / Measure — runtime behavior and generative AI profile (NIST-AI-600-1)
- OWASP AI Exchange: [Threats overview](https://owaspai.org/go/threatsoverview/)

**Implementation guidance (this guide)**
- [Primary LLM threats](#primary-llm-threats); [Security controls for LLM](#security-controls-for-llm)

## Primary LLM threats

| Threat (`OWASP LLM 2025`) | Description | Control |
|---|---|---|
| `LLM01` Prompt Injection | Bypassing instructions or changing model behavior | `AI Gateway`, input/output validation, privilege separation, red team testing (do not rely on system prompt as a security control — see `LLM07`) |
| `LLM02` Sensitive Information Disclosure | Disclosure of sensitive or confidential data | `DLP`, context control, output restrictions |
| `LLM03` Supply Chain | Compromised models, plugins, datasets, or dependencies | Model signing, `ModelScan`, `AI-BOM`, provenance (see Chapter 5) |
| `LLM04` Data and Model Poisoning | Poisoned training data, fine-tuning, or RAG corpus | Data validation, ingest controls, re-index playbook |
| `LLM05` Improper Output Handling | Unsafe use of model output by another system | Output validation and sandbox |
| `LLM06` Excessive Agency | Agent or tool actions beyond intended scope | Tool allowlist, `Intent Gate`, human approval |
| `LLM07` System Prompt Leakage | Extraction of system instructions or internal policy | Output gate, no secrets in prompt, error sanitization |
| `LLM08` Vector and Embedding Weaknesses | Poisoned or leaked retrieval/embedding data | ACL at retrieval, tenant isolation, ingest scan |
| `LLM09` Misinformation | Harmful or unreliable generated content | Human review, grounding, output policy |
| `LLM10` Unbounded Consumption | High token consumption or expensive requests | Rate limit, quota, and cost monitoring |

> Note: `Overreliance` appeared in OWASP LLM Top 10 (2023) but was removed in the 2025 edition; related risks are partly covered by `LLM09` Misinformation and operational human-review controls. `Overrefusal` is not an OWASP Top 10 category; it is discussed below as a security-adjacent operational risk with separate research literature.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01`–`LLM10` (table above)
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection; `AML.T0070` RAG Poisoning; `AML.T0053` AI Agent Tool Invocation (agent path)
- OWASP AI Exchange: [Periodic table of AI security](https://owaspai.org/go/periodictable/)

**Implementation guidance (this guide)**
- [Chapter 12 — Primary mapping](12-threat-control-tools-map.md#primary-mapping)

## Security controls for LLM

LLM security is not solved by installing a single tool. A set of capabilities must work together:

| Control | Description |
|---|---|
| Runtime guidance and prompt filtering | Tools such as `NeMo Guardrails`, `Lakera Guard`, or an internal gateway inspect incoming prompts before they are sent to the model. |
| `Pre-Inference Scanning` | Inputs are scanned for malicious patterns, bypass attempts, or sensitive data. |
| Output management and risk scoring | Model output is checked for information leakage and, when needed, blocked, redacted, or reviewed. |
| `AI Gateway` | A single entry point for applying security policies, rate limits, logging, and access control. |
| `Session Risk Scoring` | User behavior throughout the session is analyzed; if a suspicious pattern appears, response level or access is restricted. |
| Prompt anomaly detection | Sudden changes in prompt structure, length, or content relative to normal behavior are identified. |
| `Egress Filtering` | Attempts to exfiltrate sensitive data through model responses or tools are blocked. |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01`, `LLM02`, `LLM05`, `LLM10`
- OWASP AI Exchange: [Input threats — monitor use, rate limit](https://owaspai.org/go/inputthreats/); [Limit unwanted behaviour](https://owaspai.org/go/limitunwanted/)
- NIST AI RMF: Measure — runtime monitoring and abuse detection

**Implementation guidance (this guide)**
- [SOC telemetry](10-monitoring-soc-ir.md#data-required-for-telemetry) (Chapter 10)
- [Guardrails](#guardrails)

## Augmentation data (runtime behavior assets)

The OWASP AI Exchange groups **augmentation data**—material inserted into model input to steer behavior—with the same confidentiality and integrity concerns as training data. In this guide that includes:

- `RAG` corpus and retrieved chunks — [Ingest security](#ingest-security-in-rag), [Retrieval Poisoning](#retrieval-poisoning)
- System prompts and instruction templates — [System Prompt Leakage](#system-prompt-leakage-llm07)
- Tool and MCP outputs re-injected into context — [MCP security](#model-context-protocol-mcp-security), [Chapter 8 tool output injection](08-agentic-ai-security.md#tool-output-injection)

Protect augmentation data at control points **4** (ingest decision), **5** (index/configuration), **7** (validation), and **10** (runtime integrity and monitoring). Re-index when sources change — [Reindex Playbook](#reindex-playbook).

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04` Data and Model Poisoning; `LLM08` Vector and Embedding Weaknesses
- OWASP AI Exchange: [Augmentation data manipulation](https://owaspai.org/go/augmentationdatamanipulation/); [Augmentation data integrity](https://owaspai.org/go/augmentationdataintegrity/); [Augmentation data confidentiality](https://owaspai.org/go/augmentationdataconfidentiality/)

**Implementation guidance (this guide)**
- [Poisoning taxonomy](05-model-artifact-supply-chain.md#poisoning-taxonomy-across-the-lifecycle) (Chapter 5)
- [Data security in RAG](04-data-security-privacy.md#data-security-in-rag) (Chapter 4)

## Secure architecture for RAG



![](../assets/diagrams/07-llm-rag-security_01.png)


### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04`, `LLM08` (RAG corpus and retrieval)
- OWASP AI Exchange: [Augmentation data integrity](https://owaspai.org/go/augmentationdataintegrity/)

**Implementation guidance (this guide)**
- [Ingest security in RAG](#ingest-security-in-rag); [Three-layer controls in RAG](#three-layer-controls-in-rag)
- [Chapter 4 — Data security in RAG](04-data-security-privacy.md#data-security-in-rag)

## Ingest security in RAG

In `RAG`, every document that enters the knowledge base can later affect the model's response. Therefore, the `Ingest Pipeline` must be treated as a serious security boundary.

Essential controls:

- Only authorized sources are indexed.
- Documents are checked for malicious content and sensitive data before indexing.
- Document access level is stored alongside the embedding.
- Data for each tenant is kept separate.
- Document changes are versioned and traceable.

See [Augmentation data (runtime behavior assets)](#augmentation-data-runtime-behavior-assets) for the Exchange framing and control-point mapping for RAG corpora, system prompts, and tool context.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04` Data and Model Poisoning (RAG corpus)
- MITRE ATLAS: `AML.T0070` RAG Poisoning
- OWASP AI Exchange: [Augmentation data manipulation](https://owaspai.org/go/augmentationdatamanipulation/)

**Implementation guidance (this guide)**
- [Lifecycle control points](06-pipeline.md#lifecycle-control-points) — control points 4 and 5 (Chapter 6)
- [Augmentation data (runtime behavior assets)](#augmentation-data-runtime-behavior-assets)

## Three-layer controls in RAG

| Layer | Control |
|---|---|
| `Retriever` | source allowlist, integrity check, hash verification and document source signature |
| `Reranker` | security scoring alongside relevance and removal of documents with low security scores |
| `Context` | separation of `System Prompt`, `User Prompt`, and `Retrieved Context`, length limits and sanitization before concatenation into the prompt |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM08` Vector and Embedding Weaknesses
- OWASP AI Exchange: [Augmentation data confidentiality](https://owaspai.org/go/augmentationdataconfidentiality/)

**Implementation guidance (this guide)**
- [Retrieval Poisoning](#retrieval-poisoning); [Embedding Poisoning](#embedding-poisoning)

## Retrieval Poisoning

In `Retrieval Poisoning`, an attacker introduces a document or content into the knowledge source that causes retrieval of malicious or biased context. This attack is dangerous because the user may not have sent any malicious prompt, yet the model may follow instructions from a poisoned document.

| Failure point | Impact | Control |
|---|---|---|
| ingest without review | poisoned document entry | scan and approval |
| no ACL in retrieval | unauthorized document disclosure | authorization at query time |
| shared index across tenants | data leakage between customers | separate index |
| no cleanup | persistence of contamination | re-index and lifecycle policy |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04` Data and Model Poisoning
- MITRE ATLAS: `AML.T0070` RAG Poisoning; `AML.T0066` Retrieval Content Crafting

**Emerging / research**
- Zou et al. (2024). *PoisonedRAG: Knowledge Poisoning Attacks to RAG* — *research / not standardized*

**Implementation guidance (this guide)**
- [Reindex Playbook](#reindex-playbook); [Chapter 13 — RAG knowledge base pattern](13-case-studies.md#rag-in-organizational-knowledge-base--illustrative-pattern)

## Embedding Poisoning

Sample scenario: an attacker introduces a poisoned document through a webhook, user upload, or automatic sync. After conversion to an embedding, this document becomes close to seemingly unrelated queries and is retrieved as context at inference time.

| Stage | Attack | Technical control |
|---|---|---|
| `Ingestion` | entry of poisoned document | source allowlist, antivirus scan and metadata, human approval for new sources, quarantine bucket |
| `Index` | storage of poisoned vector | content hash before indexing, index versioning, separate index per tenant |
| `Retrieval` | deviation in top-k | reranking with security signals, minimum number of sources, blocking suspicious clusters |
| `Response` | execution of instructions from context | mandatory citation, grounding check and output gate |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM08` Vector and Embedding Weaknesses
- MITRE ATLAS: `AML.T0070` RAG Poisoning

**Implementation guidance (this guide)**
- [Three-layer controls in RAG](#three-layer-controls-in-rag); [Chapter 4 — Information leakage from Embedding](04-data-security-privacy.md#information-leakage-from-embedding)

## Reindex Playbook

1. Identify the poisoned batch using `Lineage`.
2. Remove that batch from the index.
3. Regenerate embeddings with an approved embedding model.
4. Run security regression tests for prompt and RAG before publishing the new index.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04` (RAG corpus remediation)
- NIST AI RMF: Manage — incident response and recovery

**Implementation guidance (this guide)**
- [LLM verification approach](#llm-verification-approach); [Lifecycle control point 7](06-pipeline.md#stage-7-test-acceptance-conditions) (Chapter 6)

## Cloud Native and Multi-Tenant deployment

> **Extended reference:** For namespace isolation, NetworkPolicy, Kyverno admission, vLLM Helm patterns, and GPU hardening patterns, see [Chapter 16 — Kubernetes Deployment Reference](16-kubernetes-deployment-reference.md) (vendor references; no bundled cluster YAML).

| Layer | Control | Implementation example |
|---|---|---|
| tenant identification | every request must have a valid `Tenant ID` | `JWT Claim` or signed header |
| Kubernetes RBAC | separate namespace for model workload | separate `Role`, `RoleBinding`, and service account |
| network | only gateway has access to inference pod | default deny egress |
| Service Mesh | mTLS and authorization | `Istio` or `Linkerd` |
| Vector DB | physical separation of indexes | avoid metadata filter on shared index |
| shared inference | quota and queue per tenant | rate limit and prevention of cache leakage |

In `vLLM` or shared GPU scenarios, model weights may be shared, but context and `KV Cache` must never be shared between tenants. Session stickiness and cache cleanup after session end must be mandatory.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM02` Sensitive Information Disclosure; `LLM08` (tenant isolation)
- OWASP AI Exchange: [SEGREGATE DATA](https://owaspai.org/go/segregatedata/)
- ISO/IEC 42001:2023 — multi-tenant AI service controls (organizational)

**Implementation guidance (this guide)**
- [Chapter 16 — Kubernetes Deployment Reference](16-kubernetes-deployment-reference.md) (namespace isolation, NetworkPolicy, vLLM patterns)

## Advanced Multi-Tenant hardening

| Risk | Control |
|---|---|
| `KV Cache Leak` | partition by tenant and cleanup after session |
| `GPU Colocation` | use `MIG` or dedicated GPU for sensitive tiers |
| `Model Multiplexing` | tenant-aware batching and separation with padding |
| `Speculative Decoding` | separate draft state or disable shared state |
| `Tokenizer Timing Side-Channel` | rate limit, fixed padding and temporal anomaly auditing |
| `Shared Inference Cache` | cache key includes tenant ID and prompt hash |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM02` (cross-tenant leakage)
- MITRE ATLAS: `AML.T0024` Exfiltration via AI Inference API (adjacent)

**Emerging / research**
- Trail of Bits (2024). *LeftoverLocals (CVE-2023-4969)* — GPU memory leakage — *documented incident*

**Implementation guidance (this guide)**
- [Chapter 16 — GPU isolation and shared inference](16-kubernetes-deployment-reference.md#gpu-isolation-and-shared-inference)

## Fine-tuning risks

| Threat | Security risk | Control |
|---|---|---|
| `Model Collapse` | repetitive output, quality degradation and failure of safety policies | synthetic data ceiling, output diversity evaluation, run security validation after every fine-tuning |
| `Overrefusal` | users are pushed toward bypass techniques | measure false positive block rate, secure usability testing and policy threshold tuning |

Research on `Model Collapse` (Shumailov et al., 2023) and on `Overrefusal` in LLM safety systems (e.g., Röttger et al., 2024, *Safety-Tuned LLMs Are Not Safer*) show that these are not merely response quality issues; both can directly affect security and the ability to bypass controls.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM04` Data and Model Poisoning (fine-tuning data path)

**Emerging / research**
- Shumailov et al. (2023). *The Curse of Recursion* (Model Collapse)
- Röttger et al. (2024). *Safety-Tuned LLMs Are Not Safer* (Overrefusal)

**Implementation guidance (this guide)**
- [LoRA, PEFT, and adapter supply chain](#lora-peft-and-adapter-supply-chain); [Chapter 5 — Model security controls](05-model-artifact-supply-chain.md#model-security-controls)

## System Prompt Leakage (LLM07)

In `System Prompt Leakage`, an attacker or user attempts to extract system instructions, internal policy, tool names, or moderation rules. This disclosure can make subsequent bypass easier.

| Vector | Control |
|---|---|
| explicit request to "repeat your instructions" | output gate and pattern blocklist |
| gradual extraction across multiple turns | session risk scoring and rate limit |
| leakage through error message or stack trace | error sanitization and separation of debug from production |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM07` System Prompt Leakage
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection (extraction vectors)
- OWASP AI Exchange: [Direct prompt injection](https://owaspai.org/go/directpromptinjection/)

**Implementation guidance (this guide)**
- [Augmentation data (runtime behavior assets)](#augmentation-data-runtime-behavior-assets); [Guardrails](#guardrails)

## Advanced Prompt Injection techniques

Beyond simple text prompts, the following attacks have been reported in production environments:

| Technique | Description | Control |
|---|---|---|
| `Token Smuggling` | hiding instructions in unusual tokenization or encoding | input normalisation, tokenizer audit |
| `ASCII Art Bypass` | malicious instruction as ASCII art characters that bypass text filters | Unicode normalization, pattern detection, length/entropy heuristics |
| `Invisible Unicode` | use of Unicode `TAG` block (`U+E0000–U+E007F`) for hidden text | Unicode normalisation, character whitelist |
| `Markdown/HTML Injection` | hidden link or comment in retrieved document | strip HTML, plain-text context |
| `Many-shot Jailbreak` | repetition of jailbreak examples in long context | context length limit, multi-stage moderation |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01` Prompt Injection
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection; `AML.T0054` LLM Jailbreak
- OWASP AI Exchange: [Testing against prompt injection](https://owaspai.org/go/testingpromptinjection/)

**Implementation guidance (this guide)**
- [Direct and indirect Prompt Injection](#direct-and-indirect-prompt-injection); [Guardrail limitations](#guardrail-limitations)

## Direct and indirect Prompt Injection

Direct `Prompt Injection` occurs when the user explicitly sends a malicious instruction. Indirect `Prompt Injection` occurs when a malicious instruction is hidden inside an external source and enters the model context through `RAG` or a tool.

Sample attack path:



![](../assets/diagrams/07-llm-rag-security_02.png)


### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01` Prompt Injection
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection; `AML.T0070` RAG Poisoning (indirect injection via retrieval)
- OWASP AI Exchange: [Direct prompt injection](https://owaspai.org/go/directpromptinjection/); [Indirect prompt injection](https://owaspai.org/go/indirectpromptinjection/)

**Emerging / research**
- Greshake et al. (2023). *Not What You've Signed Up For* (indirect prompt injection) — *research / not standardized*

**Implementation guidance (this guide)**
- [Retrieval Poisoning](#retrieval-poisoning); [Chapter 8 — Tool Output Injection](08-agentic-ai-security.md#tool-output-injection)

## Guardrails

`Guardrail`s must run both before and after the model. Pre-model control inspects input and context. Post-model control inspects output for data leakage, dangerous content, executable instructions, and policy violations.

| Control location | Example control |
|---|---|
| before model | prompt injection detection, removal of suspicious context, token limits |
| during retrieval | ACL enforcement, source filtering, secure rerank |
| after model | DLP, output validation, moderation |
| after action | logging, alert, human approval requirement |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01`, `LLM05` Improper Output Handling
- OWASP AI Exchange: [Limit unwanted behaviour](https://owaspai.org/go/limitunwanted/)

**Implementation guidance (this guide)**
- [Security controls for LLM](#security-controls-for-llm); [Chapter 12 — L6 Runtime Guardrail](12-threat-control-tools-map.md#l6--runtime-guardrail-nemo-guardrails)

## Guardrail limitations

`Guardrail` is a useful defensive layer, but not complete or definitive control. Relying solely on guardrails is an `Anti-pattern` (Chapter 9). Main limitations:

| Limitation | Description |
|---|---|
| bypass via obfuscation | techniques such as `Token Smuggling`, invisible Unicode, or multilingual content can bypass filters. |
| false positive/negative rate | strict thresholds cause `Overrefusal` and loose thresholds allow attacks to pass. |
| lack of full semantic understanding | guardrail classifiers often see patterns, not true intent. |
| latency and cost | adding multiple moderation layers increases latency and inference cost. |
| no coverage of business logic | guardrails do not know whether an action is permitted; that is the job of `Intent Gate` and authorization. |

For this reason, guardrails should be part of a `Defense-in-Depth` including `Gateway`, authorization, `Intent Gate`, telemetry, and threat modeling—not a replacement for them.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01` (guardrails are not sole control)

**Implementation guidance (this guide)**
- [Chapter 9 — Guardrail-only anti-pattern](09-anti-patterns.md#common-anti-patterns)
- [Chapter 8 — Intent Gate](08-agentic-ai-security.md#intent-gate)

**Author practical guidance**
- *Guardrail bypass and threshold trade-offs reflect operational patterns, not normative standard text.*

## Downstream conventional injection

LLM output is often passed to parsers, databases, shells, or browsers. If output is treated as trusted structured data, classic injection risks apply (`SQL Injection`, `XSS`, command execution)—independent of whether the model was "jailbroken."

| Pattern | Risk | Control |
|---|---|---|
| LLM generates SQL or shell | Database or host compromise | Parameterized queries; no direct execution of model text; output encoding |
| LLM output rendered as HTML/MD | `XSS` in chat UI | Encode on render; CSP; sanitize markdown |
| Tool/agent passes LLM text to API | Second-hop injection | Validate tool inputs; schema-only APIs; [Intent Gate](08-agentic-ai-security.md#intent-gate) (Chapter 8) |

Treat model output as **untrusted input** to every downstream component—same as user-supplied data in classic AppSec.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM05` Improper Output Handling
- OWASP AI Exchange: [Output contains conventional injection](https://owaspai.org/go/outputcontainsconventionalinjection/); [Encode model output](https://owaspai.org/go/encodemodeloutput/)

**Implementation guidance (this guide)**
- [Tool output injection](08-agentic-ai-security.md#tool-output-injection) (Chapter 8)
- [Guardrails](#guardrails)

## LoRA, PEFT, and adapter supply chain

Fine-tuning with `LoRA`, `QLoRA`, or other `PEFT` adapters introduces smaller artifacts that still alter model behavior. Treat adapters like model weights:

| Control | Application |
|---|---|
| Source allowlist | Load base model and adapters only from trusted registries |
| Scan and hash | `ModelScan` (where applicable), hash adapter + base pair in `Evidence Pack` |
| Signing | Sign adapter bundles or attest base+adapter combination at deploy |
| Provenance | Record base model version, adapter training data, and training job in `AI-BOM` |

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM03` Supply Chain
- MITRE ATLAS: `AML.T0058` Publish Poisoned Models
- OWASP AI Exchange: [Supply-chain model poisoning](https://owaspai.org/go/supplymodelpoison/)

**Implementation guidance (this guide)**
- [Chapter 5 — Provenance and signing](05-model-artifact-supply-chain.md#provenance-and-signing); [SBOM and AI-BOM](05-model-artifact-supply-chain.md#sbom-and-ai-bom)

## Model Context Protocol (MCP) security

Agents and IDEs (Cursor, Claude Desktop, VS Code extensions) connect to tools via the **Model Context Protocol (MCP)** — a JSON-RPC layer between MCP clients and MCP servers. Unlike fixed APIs, the **LLM chooses tools at runtime** from descriptions supplied by every connected server. That creates a combined attack surface: prompt injection + supply chain + confused deputy + cross-server tool shadowing.

> **References:** [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/), [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html), [AISVS C10 MCP Security](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C10-MCP-Security.md) (planned requirements).

### Architecture and trust boundaries



![](../assets/diagrams/07-llm-rag-security_03.png)


| Component | Security note |
|---|---|
| MCP Host | AI app (Cursor, Claude Desktop) — sees **all** tool definitions in context |
| MCP Client | Connects to multiple servers; passes schemas to the model |
| MCP Server | Exposes tools — **treat as untrusted** even if "internal" |
| Transport | `stdio` (local) vs streamable HTTP/SSE (remote) — production should prefer authenticated HTTPS |

**Critical property:** The LLM sees tool descriptions from **all** connected servers simultaneously — enabling **tool shadowing** (one server's description manipulates use of another server's tools).

### OWASP MCP Top 10 (2025) — control mapping

> **Mapping note:** The MCP01–MCP10 labels below follow the risk themes in the [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) and MCP Security Cheat Sheet. Verify IDs against the published OWASP release before compliance mapping; this table is an operational control reference for MLSecOps.

| ID | Risk | MLSecOps control |
|---|---|---|
| MCP01 | Token mismanagement & secret exposure | Vault/short-lived tokens; never in MCP config files; Ch.5 key management |
| MCP02 | Privilege escalation via scope creep | Narrow OAuth scopes; per-server credentials |
| MCP03 | Tool poisoning | Scan `tools/list`; pin schema hashes; output validation |
| MCP04 | Supply chain / dependency tampering | Package allowlist; typosquatting checks; SBOM scan |
| MCP05 | Command injection & execution | Sandboxed server; input validation; no shell from LLM params |
| MCP06 | Intent flow subversion | Intent Gate (Ch.8); HITL for destructive tools |
| MCP07 | Insufficient authentication & authorization | OAuth 2.1 + PKCE; per-request token validation |
| MCP08 | Lack of audit and telemetry | Log every tool call → SIEM (Ch.10) |
| MCP09 | Shadow MCP servers | Allowlist servers; IDE policy; CASB/SWG (Ch.11 Shadow AI) |
| MCP10 | Context injection & over-sharing | Sanitize tool outputs before re-injection; egress limits |

Research note: Multiple CVEs were reported against MCP servers/clients in 2025–2026 (including command injection classes). Run **static scan + gateway + runtime logging**, not one control alone.

### MCP gateway pattern (recommended for production)

Route all MCP traffic through a **governed gateway** instead of direct host → server connections:

| Capability | Why it matters |
|---|---|
| Authentication (OAuth 2.1 / JWT) | MCP07 — no anonymous tool endpoints |
| Per-tool RBAC | MCP02 — restrict who may invoke which tool |
| Rate limits / budgets | Abuse and cost control (LLM10 adjacent) |
| Audit log | MCP08 — Evidence Pack + SOC |
| Tool definition pinning | MCP03/MCP04 — detect rug pulls |
| Kill switch | Emergency block all tools (incident response) |

**Open-source gateway index:** [awesome-mcp-gateways](https://github.com/e2b-dev/awesome-mcp-gateways). Notable projects:

| Project | Role |
|---|---|
| [agentgateway](https://github.com/agentgateway/agentgateway) | MCP-native proxy; RBAC; multi-tenant |
| [Microsoft MCP Gateway](https://github.com/microsoft/mcp-gateway) | K8s session-aware MCP routing |
| [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry) | OAuth; registry; enterprise IdP |
| [Pomerium](https://github.com/pomerium/pomerium) | Auth + per-tool policies |
| [ThinkWatch](https://github.com/ThinkWatchProject/ThinkWatch) | Enterprise AI bastion incl. MCP (Ch.11) |

Reference architecture combining gateway + scanner: [agentgateway-mcp-firewall](https://github.com/skmahe1077/agentgateway-mcp-firewall) (agentgateway + MCP tool firewall + K8s `MCPServer` CRD via kmcp).

### MCP server hardening checklist (minimum bar)

Based on OWASP MCP Cheat Sheet and AISVS C10 themes:

| # | Control | Fail-closed? |
|---|---|---|
| 1 | OAuth 2.1 / OIDC on remote endpoints | Yes — deny if auth fails |
| 2 | Streamable HTTPS transport in production; restrict `stdio` to local dev | Yes |
| 3 | Sandbox: non-root container, read-only FS, dropped caps, network egress allowlist | Yes |
| 4 | Validate tool inputs with strict JSON Schema (`additionalProperties: false`) | Yes |
| 5 | Pin tool definition hash; alert on `tools/list` changes (rug pull) | Yes |
| 6 | Sanitize tool **outputs** before returning to model context | Yes |
| 7 | HITL for delete/pay/export/IAM-changing tools | Yes |
| 8 | Bind MCP HTTP servers to `127.0.0.1` unless gateway-terminated | Yes |
| 9 | Log tool name, params, user, session, outcome → SIEM | N/A |
| 10 | Include MCP servers in `AI-BOM` (Ch.5) | N/A |

### MCP scanning and tooling

Use **complementary** scanners — they target different surfaces:

| Tool | Surface | When to use |
|---|---|---|
| [mcps-audit](https://github.com/razashariff/mcps-audit) | MCP **server source code** | Lifecycle control point 3 for repos you build |
| [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) / **Snyk Agent Scan** | **Installed** MCP configs (Cursor, Claude, VS Code, …) | Developer workstation audit; MCP09 discovery |
| [MCP-Shield](https://github.com/riseandignite/mcp-shield) | Installed servers — poisoning, exfiltration, cross-origin | Alternative/complement to Agent Scan |
| [MCP Guardian](https://github.com/eqtylab/mcp-guardian) | **Runtime** — control which MCP servers the assistant may use | Production user machines |
| [ToolHive](https://github.com/StacklokLabs/toolhive) | **Deploy/manage** MCP servers with consistent security defaults | Platform teams shipping MCP |
| [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server) | Intentionally vulnerable lab | Red team training (Ch.13) |
| [mcp-injection-experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments) | Tool poisoning PoCs | Security research and test harness design |

**Curated indexes:** [awesome-mcp-security](https://github.com/AIM-Intelligence/awesome-mcp-security) (papers + tools), [Puliczek/awesome-mcp-security](https://github.com/Puliczek/awesome-mcp-security) (broader community list), [awesome-mcp-gateways](https://github.com/e2b-dev/awesome-mcp-gateways) (gateways). **Checklist:** [SlowMist MCP Security Checklist](https://github.com/slowmist/MCP-Security-Checklist) for self-assessment across client, server, and multi-MCP scenarios.

#### Source code scan — mcps-audit

[mcps-audit](https://github.com/razashariff/mcps-audit) scans MCP server source against OWASP MCP Top 10 and Agentic AI Top 10 patterns:

```bash
npm install -g mcps-audit
mcps-audit ./my-mcp-server
# PDF report: ./mcps-audit-report.pdf
mcps-audit ./my-mcp-server --json   # CI-friendly output
```

**Lifecycle placement:** Run during control point 3 (`Security & Quality Review`) for MCP server repos; critical findings should block or escalate release; attach report to Evidence Pack `security_testing.reports`.

#### Installed MCP scan — Snyk Agent Scan (mcp-scan)

The [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) project (CLI: **Snyk Agent Scan**, `snyk-agent-scan`) auto-discovers agent MCP configs and scans for tool poisoning, prompt injection, tool shadowing, and toxic flows. It **starts stdio MCP servers** to read `tools/list` — run in a **sandbox** for untrusted configs.

```bash
export SNYK_TOKEN=your-token   # from https://app.snyk.io/account
uvx snyk-agent-scan@latest
uvx snyk-agent-scan@latest ~/.cursor/mcp.json --json
# Non-interactive CI (trusted configs only):
uvx snyk-agent-scan@latest --ci --dangerously-run-mcp-servers
```

**Use case:** MCP09 shadow server discovery on developer laptops; quarterly security hygiene — not a substitute for source review during lifecycle control point 3.

> **Warning:** Scanning executes MCP server commands from config files. Review consent prompts; use `--dangerously-run-mcp-servers` only in trusted CI.

#### Runtime control — MCP Guardian

[MCP Guardian](https://github.com/eqtylab/mcp-guardian) provides realtime allow/deny over which MCP servers an LLM assistant may access — useful when users can edit local MCP configs faster than central policy updates.

#### Secure deployment — ToolHive

[ToolHive](https://github.com/StacklokLabs/toolhive) simplifies deploying and operating MCP servers with consistent packaging — pair with gateway (above) and K8s hardening ([Chapter 16](16-kubernetes-deployment-reference.md)).

#### Research papers (MCP threat landscape)

- Hou et al., *MCP: Landscape, Security Threats, and Future Research Directions* ([arXiv:2503.23278](https://arxiv.org/abs/2503.23278))
- *MCP Safety Audit: LLMs with MCP Allow Major Security Exploits* ([arXiv:2504.03767](https://arxiv.org/abs/2504.03767))
- *Enterprise-Grade Security for MCP* ([arXiv:2504.08623](https://arxiv.org/pdf/2504.08623))

Additional dynamic testing (evaluate in your environment): [operant-mcp](https://github.com/operantlabs/operant-mcp), Garak MCP probes ([NVIDIA/garak#1639](https://github.com/NVIDIA/garak/issues/1639)).

### MCP on Kubernetes

Deploy MCP servers like any privileged microservice (see [Chapter 16](16-kubernetes-deployment-reference.md)):

- Dedicated namespace; NetworkPolicy default-deny
- Sidecar or standalone **agentgateway** in front of MCP pods
- Kyverno verify signed MCP server images
- No cluster-wide `ClusterRole` for MCP service accounts
- Microsoft MCP Gateway for session-aware routing at scale

### MCP and Shadow AI overlap (MCP09)

**Shadow MCP servers** are the MCP equivalent of Shadow AI: developers add unapproved MCP configs to Cursor/Claude (`mcp.json`), npm-installed servers, or local `stdio` binaries without security review. Controls:

- IDE/MCP config allowlist via MDM or enterprise IDE policy
- Registry of approved MCP servers with signed packages
- Periodic audit of `~/.cursor/mcp.json`, Claude config, VS Code MCP settings
- Cross-reference [Chapter 11 — Shadow AI governance](11-governance-evidence.md#shadow-ai-governance)

### Evidence Pack — MCP fields

| Field | Example |
|---|---|
| `mcp.servers_allowlisted` | `["corp-git-mcp", "jira-mcp-prod"]` |
| `mcp.gateway_url` | `https://mcp-gw.internal` |
| `mcp.tool_schema_pins` | SHA-256 hashes per server/tool |
| `mcp.mcps_audit_report` | URI to lifecycle control point 3 scan/review report |
| `mcp.agent_scan_report` | Optional workstation Agent Scan JSON (MCP09 hygiene) |
| `mcp.oauth_scopes` | Documented per server |

Include MCP servers in threat modeling ([Chapter 2](02-scope-risk-threat-model.md)) and `AI-BOM` ([Chapter 5](05-model-artifact-supply-chain.md), [Chapter 12](12-threat-control-tools-map.md)).

> **Agent chapter:** Reference architecture, six-domain attack surface, Intent Gate, memory poisoning (including financial workflows), and the DO/DON'T checklist — [Chapter 8](08-agentic-ai-security.md).

### References / Source mapping

**Frameworks and standards**
- OWASP MCP Top 10 (2025): `MCP01`–`MCP10` (mapping table above)
- [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
- OWASP AISVS: C10 MCP Security (planned requirements)
- OWASP Agentic Security Initiative: tool misuse and intent subversion themes (`ASI02`)
- MITRE ATLAS: `AML.T0053` AI Agent Tool Invocation; `AML.T0110` AI Agent Tool Poisoning
- OWASP AI Exchange: [Agentic AI threats](https://owaspai.org/go/agenticaithreats/)

**Emerging / research**
- Hou et al. (2025). *MCP: Landscape, Security Threats, and Future Research Directions* ([arXiv:2503.23278](https://arxiv.org/abs/2503.23278))
- Radosevich & Halloran (2025). *MCP Safety Audit* ([arXiv:2504.03767](https://arxiv.org/abs/2504.03767))

**Implementation guidance (this guide)**
- [Chapter 8 — MCP tool connections](08-agentic-ai-security.md#mcp-tool-connections); [Chapter 11 — Shadow AI governance](11-governance-evidence.md#shadow-ai-governance)
- [Chapter 16 — MCP servers on Kubernetes](16-kubernetes-deployment-reference.md#mcp-servers-on-kubernetes)

## If only three LLM/RAG controls can be implemented

1. Deploy `Inference Gateway` with prompt filtering and output management.
2. Use allowlist and integrity check for ingestion in RAG.
3. Record runtime logging and enable rapid rollback to the last signed model.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): `LLM01`, `LLM04`, `LLM10` (minimum viable controls)

**Implementation guidance (this guide)**
- [Security controls for LLM](#security-controls-for-llm); [Ingest security in RAG](#ingest-security-in-rag)
- [Chapter 5 — Provenance and signing](05-model-artifact-supply-chain.md#provenance-and-signing)

**Author practical guidance**
- *Three-control minimum is an illustrative prioritization for resource-constrained teams.*

## LLM and RAG control prioritization

| Level | Controls |
|---|---|
| `MUST` | gateway, automated prompt injection testing, ingestion allowlist |
| `SHOULD` | session risk scoring, security reranking, tenant separation |
| `ADVANCED` | full service mesh, automated reindex with complex lineage |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Govern / Manage — risk-based control prioritization
- OpenSSF MLSecOps Whitepaper (2025): lifecycle security controls

**Implementation guidance (this guide)**
- [Chapter 14 — Maturity levels](14-maturity-roadmap.md#maturity-levels); [Minimum security baseline](06-pipeline.md#minimum-security-baseline) (Chapter 6)

## LLM verification approach

This guide complements `OWASP LLMSVS` / verification literature—it does not replace official test procedures. Use the pattern below to define **what to verify**, **when**, and **what evidence to keep**.

### Verification scope by system type

| System type | Minimum test categories | When to run | Evidence |
|---|---|---|---|
| Chatbot / completion API | direct/indirect injection, leakage, unsafe output | every release; smoke subset per change | control point 7 report |
| RAG | above + retrieval leakage, poisoned document probes | every index change and release | ingest manifest + test report |
| Agent + tools | above + tool misuse, output injection, memory cases | every tool/memory connector change | agent regression suite hash |
| Managed API | provider-enabled safety + customer gateway/DLP tests | config change and quarterly | configuration snapshot at point 9 |

### Acceptance criteria (define in threat model)

1. **Version the suite** — fixed prompt/tool scenarios with hash stored in `Evidence Pack`.
2. **Set thresholds** — e.g. max bypass rate, zero critical tool-misuse failures (see [Ch.6 stage 7](06-pipeline.md#stage-7-test-acceptance-conditions)).
3. **Separate smoke vs full** — smoke on frequent builds; full suite on release/CT to avoid production API abuse.
4. **Map to OWASP** — tag cases with `LLM01`–`LLM10` (and `ASI02` for agents) for traceability.
5. **Human review** — high-risk domains require manual scenarios beyond automation.

**Procedure gaps to close** (extend your suite; full step-by-step methodology is in the Exchange):

- **Indirect injection path** — present attacks through RAG ingest or tool output routes, not only the user chat field.
- **Variation / perturbation** — retry failed attacks with encoding, synonym, and formatting changes to test detections, not only static prompts.
- **Non-determinism** — run critical cases multiple times at fixed model version and production configuration; record variance in the control point 7 report.

Informative tool examples: [Chapter 12](12-threat-control-tools-map.md) (`Promptfoo`, `Garak`, `PyRIT`). Validate tools in your environment before using results for release decisions.

### References / Source mapping

**Frameworks and standards**
- OWASP LLMSVS / LLM verification literature (complementary — not replaced by this guide)
- OWASP LLM Top 10 (2025): `LLM01`–`LLM10` traceability
- OWASP AI Exchange: [Testing against prompt injection](https://owaspai.org/go/testingpromptinjection/); [Direct prompt injection](https://owaspai.org/go/directpromptinjection/); [Indirect prompt injection](https://owaspai.org/go/indirectpromptinjection/); [Generative AI testing tools overview](https://owaspai.org/go/testingtoolsgenai/)
- OWASP Agentic: `ASI02` (agent verification scope)
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection; `AML.T0053` AI Agent Tool Invocation; `AML.T0080` AI Agent Context Poisoning (memory cases)

**Implementation guidance (this guide)**
- [Stage 7 acceptance](06-pipeline.md#stage-7-test-acceptance-conditions) (Chapter 6)
- [Three categories of security testing](06-pipeline.md#three-categories-of-security-testing) (Chapter 6)
- [Garak / Promptfoo commands](12-threat-control-tools-map.md#appendix-informative-tool-command-reference) (Chapter 12)

## Practical principle

In `LLM` systems, security is not solved by hardening the prompt alone. A secure architecture must include `Gateway`, knowledge source control, authorization, guardrails, telemetry, and continuous testing.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): defense-in-depth across runtime controls
- OWASP AI Exchange: [Limit unwanted behaviour](https://owaspai.org/go/limitunwanted/)

**Implementation guidance (this guide)**
- [LLM and RAG control prioritization](#llm-and-rag-control-prioritization); [Chapter 1 — MLSecOps principles](01-intro.md#mlsecops-principles)

## Practical summary

- Most security risks of large language models occur at `Runtime`, not only at build time.
- `Prompt Injection` is one of the most common attack vectors in production environments.
- Deploying `RAG` without data source validation is very high risk.
- The minimum practical set includes `Gateway` with runtime logging.
- `Guardrails` never replace threat modeling.

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (2025): runtime threat summary (`LLM01`, `LLM04`, `LLM08`)
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection; `AML.T0070` RAG Poisoning

**Implementation guidance (this guide)**
- [If only three LLM/RAG controls can be implemented](#if-only-three-llmrag-controls-can-be-implemented)
- [Chapter 2 — Attack surface matrix](02-scope-risk-threat-model.md#attack-surface-matrix) (LLM/RAG rows)
