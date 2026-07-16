# Chapter 11: Governance, Compliance, and Evidence Pack

## Governance in MLSecOps

Governance means that decisions related to the model, data, risk, and release are explainable, traceable, and auditable. In AI systems, the absence of governance prevents teams from explaining how a model was built, why it was released, and what should be investigated in a security incident.

> *Refs - Frameworks: NIST AI RMF: Govern; ISO/IEC 42001: AI management system; OWASP AI Exchange: [Governance controls](https://owaspai.org/go/governancecontrols/).*

## Shadow AI governance

**Shadow AI** is the use of AI tools (ChatGPT, Claude, Copilot, browser extensions, personal API keys, embedded SaaS AI features) **without IT/security approval, monitoring, or contractual coverage**. It is distinct from shadow IT: the risk is not only unauthorized infrastructure but **data in prompts**, **unaudited model outputs**, and **supply-chain features inside approved SaaS** (Notion AI, Slack AI, M365 Copilot on personal seats).

> **Field reality:** Industry surveys consistently report high employee AI adoption outpacing formal AI security policy coverage. Treat shadow AI as a **governance + data-exfiltration** problem, not a blocking-only problem.

### Why shadow AI matters for MLSecOps

| Risk | Example | Framework mapping |
|---|---|---|
| Regulated data in consumer LLM | PII/PHI/source code pasted into personal ChatGPT | GDPR, HIPAA, EU AI Act literacy (Art. 4) |
| No DPA / vendor review | Consumer-tier tool processes customer data | SOC 2 CC9, ISO 42001 supplier control |
| Unmonitored agent plugins | IDE extension calls external model with repo context | OWASP LLM03 supply chain, LLM02 disclosure |
| Personal API keys in code | Developer key in notebook touching prod data | Ch.6 control point 3 secrets review + shadow key discovery |
| Embedded AI in sanctioned SaaS | Copilot on personal M365 vs corporate tenant | CASB/SSPM gap — traffic looks "approved" |

**Documented pattern:** Samsung restricted generative AI tools after internal data was pasted into ChatGPT (2023). See [Chapter 13 — Shadow LLM usage](13-case-studies.md#shadow-llm-usage-and-data-boundary-documented-incident).

### Shadow AI vs sanctioned MLSecOps path

![](../assets/diagrams/11-governance-evidence_01.png)

*Figure - Data flow contrast between ungoverned shadow AI tools and the sanctioned MLSecOps path with gateway and DLP controls.*

MLSecOps lifecycle controls (Ch.6) do **not** protect data sent to shadow tools. Shadow AI controls are **parallel**: discovery, acceptable use policy, enterprise gateway, and DLP.

### Five-layer detection stack

Based on enterprise governance patterns ([CTAIO Shadow AI guide](https://ctaio.dev/en/ai-security/shadow-ai/), [systemprompt.io governance guide](https://systemprompt.io/guides/shadow-ai-governance), [Proofpoint shadow AI reference](https://www.proofpoint.com/us/threat-reference/shadow-ai)):

| Layer | What it catches | Tooling examples |
|---|---|---|
| L1 — Network / CASB | Traffic to `api.openai.com`, Claude, Gemini, etc.; corporate vs personal OAuth tenant | Netskope, Zscaler, Prisma Access, Cloudflare SWG |
| L2 — SaaS / SSPM | AI features inside approved apps (Notion AI, Slack AI, Salesforce Einstein) | CASB, SSPM (Obsidian, Valence, etc.) |
| L3 — Endpoint / browser | Extensions, desktop apps, clipboard → AI upload | EDR, browser extension inventory, endpoint DLP |
| L4 — Developer environment | Personal Copilot seats, API keys in IDE, `.env` with `OPENAI_API_KEY` | Gitleaks, secret scan (Ch.12), internal dev survey |
| L5 — AI gateway (sanctioned path) | All approved traffic with prompt logging, PII scrub, budget | LiteLLM, Kong AI Gateway, ToTra, ThinkWatch, internal gateway (Ch.7) |

**Gap to document explicitly:** L1–L3 rarely cover 100% of shadow usage (personal devices, embedded SaaS AI, offline local models). Residual risk should be accepted only with **sanctioned alternatives** and executive acknowledgment.

### AI Acceptable Use Policy (AI-AUP) — minimum contents

| Section | Requirement |
|---|---|
| Approved tools | Named list (e.g., ChatGPT Enterprise, Claude for Work, internal RAG) with owners |
| Prohibited data classes | Regulated PII/PHI, credentials, unreleased source, customer contracts in **consumer-tier** tools |
| Account type | **Corporate tenant / SSO only** for work-related AI; personal accounts discouraged or blocked on corp devices |
| Approval process | Fast-track request for new tools (reduces bypass motivation) |
| Incident reporting | How to report accidental paste/leak |
| Training | EU AI Act Art. 4 AI literacy where applicable |

Publish AI-AUP **before** wide blocking — bans without alternatives typically increase underground usage ([systemprompt.io](https://systemprompt.io/guides/shadow-ai-governance)).

### 30-day shadow AI rollout (operational)

| Week | Activity |
|---|---|
| 1 — Discover | Inventory from CASB/SWG/IdP logs; developer survey; extension audit; map personal vs corporate OAuth |
| 2 — Classify | Risk-tier each tool (public LLM, IDE plugin, embedded SaaS AI, local model) |
| 3 — Enable | Launch sanctioned enterprise AI + gateway; SSO; DPA/sub-processor review for regulated data |
| 4 — Enforce | SWG allow/warn/block; DLP in **monitor** mode first, then block for highest-sensitivity classes; tune false positives |

### Technical controls (map to MLSecOps)

| Control | Shadow AI mitigation | Guide reference |
|---|---|---|
| Enterprise AI gateway | Route all approved LLM/API traffic; log prompts; kill switch | Ch.7 gateway, Ch.10 telemetry |
| Presidio / DLP at gateway | Block/mask PII before outbound prompt | Ch.4, Ch.12 |
| SSO + corporate tenant only | Block personal ChatGPT on corp network where policy allows | Governance + IT identity |
| Secret scanning | Find `OPENAI_API_KEY`, Anthropic keys in repos | Ch.6 control point 3, Ch.12 Gitleaks |
| Centralized API proxy | Developers use org proxy, not raw provider keys | Ch.5 key management |
| SIEM correlation | Alert on bulk uploads to AI domains | Ch.10 |

### Open-source gateway references (sanctioned path)

The projects below are non-endorsed examples of open-source gateway patterns. Validate maturity, licensing, and operational fit before use.

| Project | Role in shadow AI reduction |
|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | Self-hosted proxy; virtual keys; team budgets; 100+ providers |
| [Kong AI Gateway](https://github.com/Kong/kong) | Enterprise API management + AI plugins on existing Kong |
| [ToTra](https://github.com/SugaC-275/ToTra) | Go gateway; PII blocking; quota; audit log |
| [ThinkWatch](https://github.com/ThinkWatchProject/ThinkWatch) | Enterprise AI bastion; MCP + API proxy; RBAC; audit |

Providing a **sanctioned, productive alternative** reduces shadow demand more than blocking alone ([CTAIO AI security stack](https://ctaio.dev/en/ai-security/ai-security-stack/)).

### Evidence Pack fields for shadow AI program

| Field | Example |
|---|---|
| `shadow_ai.inventory_date` | 2026-06-01 |
| `shadow_ai.tools_discovered` | 12 unsanctioned destinations |
| `shadow_ai.sanctioned_gateway` | LiteLLM prod URL |
| `shadow_ai.dlp_mode` | monitor → enforce schedule |
| `shadow_ai.ai_aup_version` | v1.2 |
| `shadow_ai.residual_risk_accepted` | personal mobile — documented exception |

### Anti-patterns

| Anti-pattern | Consequence | Alternative |
|---|---|---|
| Blanket ban without enterprise AI | Underground usage increases | Sanctioned ChatGPT Enterprise / internal RAG + gateway |
| DLP block-only on day one | Workarounds (mobile hotspot, personal laptop) | Monitor → tune → enforce high-sensitivity only |
| Ignoring embedded SaaS AI | "Approved" Notion/Slack with ungoverned AI feature | SSPM + feature-level policy |
| No personal vs corporate account distinction | OAuth to personal Google/OpenAI | CASB tenant enforcement |
| Shadow AI excluded from threat model | Lifecycle controls give false confidence because unapproved tools bypass them | Include Shadow AI row in [Ch.2 attack surface](02-scope-risk-threat-model.md#attack-surface-matrix); govern in Ch.11 |

> *Refs - Frameworks: EU AI Act: Art. 4 AI literacy (where applicable); OWASP LLM Top 10: `LLM02`, `LLM03` (shadow data path); MITRE ATLAS: `AML.T0057` LLM Data Leakage; `AML.T0110` AI Agent Tool Poisoning (ungoverned MCP / IDE plugins). This guide: [AI system inventory](02-scope-risk-threat-model.md#ai-system-inventory) (Chapter 2); [MCP security](07-llm-rag-security.md#model-context-protocol-mcp-security) (Chapter 7). Author note: 30-day rollout and gateway vendor lists are operational patterns, not standards.*

## OpenSSF MLSecOps Mapping (Whitepaper 2025)

> **Affiliation:** This guide is **not** published or endorsed by OpenSSF. The table below maps the [OpenSSF Secure MLOps whitepaper](https://openssf.org/wp-content/uploads/2025/08/OpenSSF_MLSecOps_Whitepaper.pdf) lifecycle stages and security measures to chapters in **this** community reference. Use the OpenSSF document as the authoritative source for their architecture; use this guide for lifecycle decision and evidence patterns.

| # | OpenSSF lifecycle stage | OpenSSF security measures (summary) | This guide — chapter / artifact |
|---|---|---|---|
| 1 | Planning and design | Threat modeling, secure design, SBOM visibility | Ch. 2, 6 (prerequisite); Ch. 5 (`AI-BOM`) |
| 2 | Data engineering | Validation, versioning, lineage, anomaly detection, encryption | Ch. 4; control point 4 |
| 3 | Experimentation | Supply chain security, poisoned data detection, experiment tracking | Ch. 4, 6 (stages 2–5) |
| 4 | ML pipeline dev & test | Reproducibility, secure artifact validation, pipeline testing | Ch. 6 (control points 3, 7) |
| 5 | Continuous integration | SAST/SCA, policy enforcement, dependency scan | Ch. 6 (control point 3); Ch. 12 |
| 6 | Continuous deployment | Secure deploy automation, artifact checks, trusted packages | Ch. 6 (control points 8–10); signing |
| 7 | Continuous training | Drift detection, re-validation, authenticated feedback data | Ch. 6 (CT cycle) |
| 8 | Model serving | Input validation, access control, output filtering | Ch. 7, 8; runtime gateway |
| 9 | Continuous monitoring | Drift, anomaly, alerting, adversarial monitoring | Ch. 10; SOC |
| — | Cross-cutting (OpenSSF tools) | Sigstore, SLSA, Scorecard, GUAC | Ch. 5, 12 |
| — | Cross-cutting (DevOps) | Secrets, IaC scan, CI attestation | Ch. 6 control point 3; Ch. 12 |
| — | Evidence | Audit trail of which measures are implemented | `Evidence Pack` (this guide) |

The organization's `Evidence Pack` should record which OpenSSF-aligned measures—plus LLM/RAG/agent controls from OWASP and ATLAS—are implemented for each deployment, aligned with the threat model.

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): lifecycle stages and security measures in table above; NIST AI RMF: Map / Govern across lifecycle. This guide: [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6); [Evidence Pack](#what-is-an-evidence-pack).*

## Optional assurance tiering — illustrative only

> **Non-standard concept:** The tiering below is an optional organizational planning aid. It is **not** an OWASP, ISO, EU, or industry standard. For formal compliance, use `ISO/IEC 42001`, `ISO/IEC 23894`, the `EU AI Act`, and the organization's legal/compliance process.

| Level | Example context | Minimum evidence expectations |
|---|---|---|
| Tier 1 | Internal low-impact assistants | Basic threat model, artifact review where applicable, runtime logging |
| Tier 2 | Customer-facing LLM/RAG services | Lifecycle decision evidence, red team suite, signed or tamper-evident evidence bundle |
| Tier 3 | High-risk domains (medical, finance, critical infrastructure) | Independent security review, continuous monitoring, formal risk register, human oversight |

> *Refs - Frameworks: ISO/IEC 42001; ISO/IEC 23894; EU AI Act - formal compliance frameworks cited in section note; NIST AI RMF: risk-based assurance tiers (conceptual alignment). Author note: Tier 1-3 table is an optional organizational planning aid, not an OWASP, ISO, EU, or industry standard.*

## STRIDE and FMEA applied to ML assets

The methods below apply established threat-modeling techniques to ML/AI assets. They are **not** separate published standards:

| Method | Application |
|---|---|
| `STRIDE-AI` | Mapping threats to ML assets (data, model, API) |
| `FMEA-AI` | Assessing fairness impact and algorithmic harm with Failure Mode and Effects Analysis |
| `Color Teams` | Combining red/blue/purple team for the ML development cycle |

> *Refs - Frameworks: OWASP AI Exchange: [Threat modeling decision tree](https://owaspai.org/go/threatmodel/); ISO/IEC 23894: AI risk assessment methods (FMEA adjacency). This guide: [Threat model template](17-appendix-e-implementation-reference.md#e3-threat-model-template) (Appendix E.3); [Chapter 2 threat modeling](02-scope-risk-threat-model.md) (Chapter 2). Author note: STRIDE-AI and FMEA-AI labels apply established techniques to ML assets; not separate published standards.*

## Reference frameworks

| Framework | Application |
|---|---|
| `NIST AI RMF` | Risk management for AI systems |
| `ISO/IEC 42001` | AI management system |
| `ISO/IEC 23894` | AI risk management |
| `OWASP LLM Top 10` | Threats to language models (2025 edition, stabilized) |
| `OWASP ML Top 10` | Threats to ML models (still `draft`) |
| `OWASP LLMSVS` | Verification standard for LLMs (structured testing and evaluation) |
| `MITRE ATLAS` | Modeling attack techniques against AI |
| `EU AI Act` | Legal requirements based on risk level |

> *Refs - Frameworks: Sources listed in table above; OWASP AI Exchange: [Governance controls](https://owaspai.org/go/governancecontrols/). This guide: [Traceability convention](15-conclusion-appendix.md#traceability-and-source-mapping-convention) (Chapter 15).*

## What is an Evidence Pack?

An `Evidence Pack` is a bundle of technical and managerial evidence showing how an AI system, model, RAG index, agent configuration, or managed AI service configuration was built, evaluated, controlled, and released. It is an **audit evidence pattern**, not a mandatory OWASP file format. Organizations may implement it as signed JSON, a document bundle, a GRC record, an artifact registry entry, or another tamper-evident evidence mechanism.

The Evidence Pack is **raw material for** - not a substitute for - `ISO/IEC 42001` documented information and `EU AI Act` Annex IV technical documentation. It supplies the security evidence those artifacts draw on; it does not by itself satisfy the management-system or conformity-documentation requirements, which have their own mandated structure.

> *Refs - Frameworks: NIST AI RMF: Govern / Measure (documentation and monitoring evidence); ISO/IEC 42001: documented information for AI management system. This guide: [Appendix E.4 - Evidence Pack template](17-appendix-e-implementation-reference.md#e4-evidence-pack-template). Author note: Evidence Pack field names and structure are community implementation guidance, not a published OWASP or ISO file format.*

## Recommended Evidence Pack contents

| Section | Evidence |
|---|---|
| Data | Data origin, version, owner, sensitivity level, scan results |
| Model | Version, parameters, metrics, hash, signature |
| Security | Results of adversarial, backdoor, and prompt injection tests |
| Supply chain | `SBOM`, `AI-BOM`, vulnerabilities, provenance |
| Policy | Gate decisions, policies, approvals |
| Deployment | Environment version, configuration, release method, rollback plan |
| Runtime | Telemetry, alerts, guardrail decisions |

> *Refs - Frameworks: NIST AI RMF: Govern / Measure (documentation evidence); EU AI Act: Art. 11 technical documentation; Art. 12 record-keeping (high-risk adjacency); ISO/IEC 42001: documented information requirements. This guide: [Evidence Pack components](#evidence-pack-components); [Appendix E.4 - Evidence Pack template](17-appendix-e-implementation-reference.md#e4-evidence-pack-template).*

## Evidence Pack components

| Component | Content | Application |
|---|---|---|
| Model identity | hash, version, source, and build date | Tracking in incidents and rollback |
| Supply chain | `SBOM/AI-BOM`, `SLSA`, `in-toto`, and provenance | Supply chain audit |
| Integrity | Digital signature with `Cosign/Sigstore` and verify result where artifacts are controlled; managed-service configuration snapshot where model weights are provider-managed | Preventing artifact substitution or unreviewed configuration drift |
| Security testing | Reports from `ModelScan`, `ART`, prompt injection, and poisoning | Demonstrating due diligence |
| policy | Quality decision log, `OPA/Conftest`, exceptions, and approver | Transparency of `Go/No-Go` decisions |
| runtime | Telemetry, alerts, and prompt trace in incidents | Incident response and postmortem |

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): SBOM, signing, provenance (Sigstore, SLSA themes); OWASP LLM Top 10 (2025): `LLM03` supply chain; OWASP ML Top 10 (draft): `ML06`. This guide: [SBOM and AI-BOM](05-model-artifact-supply-chain.md#sbom-and-ai-bom) (Chapter 5); [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6).*

## Relationship to compliance

| Framework | Relationship to Evidence Pack |
|---|---|
| `NIST AI RMF / ISO 42001` | The Evidence Pack is the operational output of the govern and map sections and shows that controls are actually implemented. |
| `EU AI Act` | For high-risk systems, documentation of data, post-deployment monitoring, and incident recording are fed from evidence and SOC telemetry. |
| `ISO/IEC 23894` | Risks in the risk register must trace to threat mapping, production checklist, and auditable controls. |

### Practical mapping of EU AI Act requirements (High-Risk systems) to controls

| EU AI Act requirement | Technical input this guide provides (not a conformance claim) |
|---|---|
| `Risk Management System` (Art. 9) | Security-risk input: versioned threat model (Chapter 2). Does **not** cover the health/safety/fundamental-rights scope of Art. 9. |
| `Data Governance` (Art. 10) | Data control, lineage, PII masking (Chapter 4). Does **not** cover bias/representativeness assessment. |
| `Technical Documentation` (Art. 11) | `Evidence Pack` and `AI-BOM` (Chapters 5, 11) as raw material - not structured to the Annex IV schema. |
| `Record-Keeping / Logging` (Art. 12) | Telemetry, prompt/tool logging (Chapter 10) |
| `Transparency` (Art. 13) | Model documentation, provenance, user-facing instructions (Chapter 5) |
| `Synthetic-content marking` (Art. 50) | **Mandatory baseline obligation:** machine-readable marking of AI-generated audio/image/video/text and disclosure of AI interaction. Implement watermarking/marking as a required provider control, not an optional anti-theft measure. |
| `Human Oversight` (Art. 14) | `HITL` and `Intent Gate` (Chapter 8). Does **not** cover automation-bias or the two-person-verification rule. |
| `Accuracy, Robustness, Cybersecurity` (Art. 15) | Cybersecurity third: adversarial testing, signing, runtime guardrail (Chapters 5, 6, 7). Accuracy and robustness declarations are only lightly covered. |
| `Post-Market Monitoring` (Art. 72) | Runtime monitoring and SOC (Chapter 10) as input - not a documented PMM plan. |

This mapping shows how MLSecOps technical controls **may provide evidence inputs to** documentation and audit activities relevant to the `EU AI Act` - provided that evidence is maintained automatically, reviewed by legal/compliance teams, and adapted to each deployment context. It is **not** a conformance mapping.

> **Out of scope for this guide.** The table covers only obligations where technical security controls contribute evidence. It does **not** address - and must not be read as covering - prohibited practices (Art. 5), high-risk classification (Art. 6 / Annex III), the quality management system (Art. 17), the fundamental-rights impact assessment (Art. 27), conformity assessment / Declaration of Conformity / CE marking (Art. 43/47/48), EU-database registration (Art. 49), GPAI and systemic-risk obligations (Art. 51-55), or serious-incident reporting (Art. 73). These require the organization's compliance program and legal review.

> *Refs - Frameworks: EU AI Act: articles cited in tables above; NIST AI RMF; ISO/IEC 42001; ISO/IEC 23894. This guide: [Evidence Pack components](#evidence-pack-components).*

### Mapping EU AI Act requirements to Evidence Pack components

The table below shows which section of the `Evidence Pack` (Chapter 11) and what evidence should cover each legal requirement for high-risk systems:

| EU AI Act requirement | Evidence Pack component | Expected evidence |
|---|---|---|
| `Risk Management System` (Art. 9) | policy + threat model | Versioned threat model document, risk register, gate decisions |
| `Data Governance` (Art. 10) | Data | Lineage, data contract, PII scan report, dataset version |
| `Technical Documentation` (Art. 11) | Full bundle | Signed Evidence Pack for each deploy |
| `Record-Keeping / Logging` (Art. 12) | runtime + policy | Prompt/tool/retrieval log, retention policy, gate audit log |
| `Transparency` (Art. 13) | Model identity + supply chain | Provenance, `AI-BOM`, model documentation, deploy instructions; synthetic-content marking per Art. 50 for generative outputs |
| `Human Oversight` (Art. 14) | policy + runtime | `HITL` log, human approval runbook, kill switch |
| `Accuracy, Robustness, Cybersecurity` (Art. 15) | Security testing + integrity | `ART`/red team report, `ASR` relative to baseline, signature and verify |
| `Post-Market Monitoring` (Art. 72) | runtime | Telemetry, SOC alerts, drift report, postmortem |

> This mapping is technical guidance, not legal advice. Final interpretation of `EU AI Act` requirements rests with the organization's legal and compliance teams.

## Policy-as-Code

Security policies should not remain only in documents. Where practical, they should be applied in executable form in release workflows and at runtime. Tools such as `OPA`, `Conftest`, or an internal policy engine can perform this work, but the control objective is policy enforcement and auditable decision-making—not any specific tool.

Example policies:

- A model without a signature is not allowed to be released.
- Data with unmasked `PII` is not allowed for training.
- A critical vulnerability in dependencies causes the build to stop.
- An `LLM` model without prompt injection testing is not allowed to deploy.
- An agent without an `Intent Gate` is not allowed to invoke sensitive tools.

> *Refs - Frameworks: ISO/IEC 42001: operational control and policy enforcement; OWASP AI Exchange: [Governance controls](https://owaspai.org/go/governancecontrols/); OpenSSF MLSecOps whitepaper (2025): CI/CD policy enforcement themes. This guide: [Lifecycle control points 4, 8](06-pipeline.md#lifecycle-control-points) (Chapter 6); [Policy examples in Chapter 12](12-threat-control-tools-map.md#l4--policy-as-code-opa--conftest).*

## Responsibilities

| Role | Responsibility |
|---|---|
| Model owner | Defining purpose, acceptance criteria, and business risk |
| ML team | Training, evaluation, and version recording |
| Security team | Threat model, security testing, and policies |
| Platform team | Infrastructure, access, monitoring, and deployment |
| Governance team | Compliance, audit, and evidence management |

> *Refs - Frameworks: NIST AI RMF: Govern (roles and accountability); ISO/IEC 42001: roles, responsibilities, and authorities (management system); OWASP AI Exchange: [How to organize AI security (GUARD)](https://owaspai.org/go/organize/). This guide: [Personas and shared responsibility](#personas-and-shared-responsibility); [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6).*

## Personas and shared responsibility

| Persona | Security focus | Area of responsibility |
|---|---|---|
| `Solution / ML Architect` | Secure architecture and service boundary | Introduction, lifecycle controls, and MLOps alignment |
| `MLOps / AI Engineer` | Release workflow, deploy, and CT | Lifecycle controls and tools |
| `Data Scientist / Engineer` | Data quality and experimentation | Data and experimentation |
| `Data Governance` | `PII`, compliance, and lineage | Data and compliance |
| `Product Security` | Threat model, release decisions, and assurance | Threats and lifecycle controls |
| `SOC / IR` | Runtime, alerts, and incident evidence | SOC and evidence pack |

> *Refs - Frameworks: OWASP AI Exchange: [How to organize AI security (GUARD)](https://owaspai.org/go/organize/); Cloud provider shared-responsibility models (managed AI services). This guide: [Responsibilities](#responsibilities); [Reading paths](TABLE-OF-CONTENTS.md#reading-paths).*

## Tamper-evident storage

Minimum practical steps for evidence retention:

1. Store the `Evidence Pack` in `S3` or equivalent with `Object Lock`.
2. Sign each bundle with `Cosign` and verify before deploy.
3. Separate write access from read access; audits should be read-only only.
4. In a `P1` incident, store an immediate snapshot in a separate bucket with lock.

For organizations with strict audit requirements, an advanced option is to use `Rekor Transparency Log` or a hash chain in the manifest.

> *Refs - Frameworks: OpenSSF: Sigstore / Rekor transparency log practices; EU AI Act: Art. 12 record-keeping integrity (high-risk adjacency); ISO/IEC 42001: control of documented information. This guide: [Model signing](05-model-artifact-supply-chain.md) (Chapter 5); [Evidence Pack](#what-is-an-evidence-pack).*

## Security validation and assurance

A control without measurement of effectiveness is only a checkbox. The assurance loop must show that gates are actually effective and that deploy decisions are made based on numeric criteria.

![](../assets/diagrams/11-governance-evidence_02.png)

*Figure - The assurance loop linking test harness, security validation, deploy decision, production telemetry, and CT regression.*

| Stage | Output | Owner |
|---|---|---|
| `Test Harness` | Versioned suite in Git | Security + MLOps |
| Security validation | Metric report and suite hash | MLOps |
| Deploy decision | pass/fail relative to baseline | Model Owner |
| Production | Telemetry and feedback related to FP/FN | SOC |
| CT / retrain | Full suite regression | MLOps |

> *Refs - Frameworks: NIST AI RMF: Measure / Manage (validation and monitoring); OWASP AI Exchange: [Continuous validation](https://owaspai.org/go/continuousvalidation/); OWASP LLMSVS. This guide: [Red Team program and security test cadence](06-pipeline.md#red-team-program-and-security-test-cadence) (Chapter 6); [Verification vs. validation](#verification-vs-validation).*

## Assurance metrics

> Example thresholds only — each organization must set acceptance criteria in its threat model and policy.

| Control | Metric | Example acceptance | Frequency |
|---|---|---|---|
| `Policy-as-Code` | Violation detection rate in red team | 100% on critical rules | Every release |
| `LLM Gateway` | False negative on injection suite | Maximum 5% critical prompts | Monthly and after tune |
| `LLM Gateway` | False positive on benign suite | Maximum 2% | Monthly |
| `ART` | `ASR @ epsilon` | Maximum baseline + 2% | Every new model |
| `RAG Ingest` | Poison doc retrieval rate | Zero percent in regression set | Every index change |
| `Agent Output Gate` | Bypass in output-injection cases | Zero critical | Every agent release |

> *Refs - Frameworks: OWASP LLMSVS: structured testing and evaluation thresholds; NIST AI RMF: Measure (control effectiveness). This guide: [Security validation and assurance](#security-validation-and-assurance); [Governance Benchmark Suite](#governance-benchmark-suite). Author note: Example acceptance thresholds are illustrative; each organization must set criteria in its threat model and policy.*

## Optional regression scoring pattern — illustrative only

> **Non-standard concept:** The formula below is an **optional internal planning aid**, not a published metric and not an OWASP standard. Do not use it as a compliance score, public maturity claim, or cross-organization benchmark. Weights (`w1`–`w3`) must be defined per organization; metrics are not directly comparable without normalization.

For decision-making, a conceptual score can be defined:

```text
score = w1 * clean_metric + w2 * (1 - ASR_or_bypass_rate) + w3 * gate_pass_rate
```

One possible internal decision rule is:

```text
score(new) >= score(baseline_signed) - delta
```

The value of `delta` should be set in the organization's threat model. This example should not replace explicit release criteria for critical controls.

> *Refs - Frameworks: NIST AI RMF: Measure (quantitative risk assessment - conceptual alignment); ISO/IEC 23894: risk treatment and acceptance criteria. Author note: Regression scoring formula and weights are an optional internal planning aid, not a published metric or OWASP standard.*

## Governance Benchmark Suite

For assurance to be repeatable, the security benchmark must be versioned and traceable:

1. Maintain the test suite in the repository with a tag such as `security-suite-v1.x`.
2. Any change to a gate or guardrail triggers re-running the suite in CI.
3. Record results in the `Evidence Pack` along with suite hash, execution date, and model version.
4. A false negative—an attack that should have been blocked but passed through—should be tracked as an incident or defect with higher severity than a false positive.

> *Refs - Frameworks: OWASP AI Exchange: [Continuous validation](https://owaspai.org/go/continuousvalidation/); [AI security testing overview](https://owaspai.org/go/testing/); OpenSSF MLSecOps whitepaper (2025): reproducible security testing themes. This guide: [Red Team program and security test cadence](06-pipeline.md#red-team-program-and-security-test-cadence) (Chapter 6); [Evidence Pack](#what-is-an-evidence-pack).*

## Verification vs. validation

| Axis | `Verification` | `Validation` |
|---|---|---|
| Question | Is the control implemented correctly? | Is the model or system sufficient for production? |
| Example | OPA rule deployed and gateway is in the traffic path | `ASR`, bypass rate, and accuracy are acceptable |
| Location | Infrastructure audit and production checklist | Security validation and Canary |

Maturity level 2 means a stable gate and suite exist. Maturity level 3 means automated regression score and false negative error tracking in the SOC are in place.

> *Refs - Frameworks: ISO/IEC 42001: verification and validation themes (management system); NIST AI RMF: Measure (testing vs. operational adequacy). This guide: [Maturity roadmap](14-maturity-roadmap.md) (Chapter 14); [Assurance metrics](#assurance-metrics).*

## Vulnerability disclosure and external intelligence sources

`MLSecOps` governance should not be internal-only. The organization must define a path for receiving and publishing model/AI infrastructure vulnerabilities:

| Source / mechanism | Application |
|---|---|
| `huntr` (huntr.com) | Dedicated AI/ML bug bounty platform for receiving vulnerability reports |
| `AI Vulnerability Database (AVID)` | Database of known model vulnerabilities |
| `AI Incident Database` | Lessons learned from real AI incidents |
| `MITRE ATLAS` | Updates to attacker tactics/techniques |
| Internal `Coordinated Vulnerability Disclosure` | Formal path for reporting vulnerabilities in the organization's models |

Recommendation: Define a `security.txt` or CVD process for the organization's AI models and APIs, and feed these sources back periodically into the threat model (Chapter 2) and test suite (Chapter 6).

> *Refs - Frameworks: MITRE ATLAS: tactic/technique updates - https://atlas.mitre.org/; OpenSSF: coordinated vulnerability disclosure practices; OWASP AI Exchange: [AI program / inventory](https://owaspai.org/go/aiprogram/). This guide: [Threat model](02-scope-risk-threat-model.md) (Chapter 2); [Red Team program](06-pipeline.md#red-team-program-and-security-test-cadence) (Chapter 6).*

## Practical principle

If a model is not auditable, it is not trustworthy from an organizational perspective. Evidence must be produced concurrently with building and releasing the model—not after an incident and not manually.

> *Refs - Frameworks: ISO/IEC 42001; EU AI Act high-risk documentation themes (see [Relationship to compliance](#relationship-to-compliance)). This guide: [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6).*
