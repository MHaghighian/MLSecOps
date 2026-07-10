# Chapter 10: Monitoring, SOC, and Incident Response

## Monitoring in AI systems

AI monitoring is not just checking uptime or latency. Model behavior, data, prompts, tools, outputs, drift, and security incidents must also be observed.

Monitoring in `MLSecOps` must see three layers simultaneously:

| Layer | Sample indicators |
|---|---|
| `Model Performance Monitoring` | `Accuracy`, quality metric, latency, `P95/P99`, throughput, error rate, CPU/GPU/Memory consumption |
| `Data Health Monitoring` | `Data Drift`, `Concept Drift`, `Schema Deviation`, missing values, data distribution change and user behavior patterns |
| `Security Monitoring` | `Prompt Injection`, `Jailbreak`, `Tool Abuse`, Shadow AI egress, MCP tool-call anomalies, `Model Extraction`, `RAG Poisoning`, `Memory Poisoning`, `Context Poisoning`, and abnormal user or Agent behavior |



![](../assets/diagrams/10-monitoring-soc-ir_01.png)

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)
- NIST AI RMF: Measure / Manage
- MITRE ATLAS: `AML.T0051` LLM Prompt Injection; `AML.T0053` AI Agent Tool Invocation; `AML.T0070` RAG Poisoning; `AML.T0080` AI Agent Context Poisoning; `AML.T0110` AI Agent Tool Poisoning

**Implementation guidance (this guide)**
- [Three categories of security testing](06-pipeline.md#three-categories-of-security-testing) (Chapter 6)

## Data required for telemetry

| Data | Reason for importance |
|---|---|
| `Prompt` | analysis of prompt injection and abuse |
| `Response` | review of data leakage and unsafe output |
| `Session ID` | reconstruction of interaction path |
| `Trace ID` | linking incidents across services |
| `Model Version` | identification of compromised version |
| `Tool Call` | review of tool abuse |
| `Retrieval Event` | analysis of leakage or poisoning in RAG |
| `Policy Decision` | review of allow or block reason |
| `Guardrail Decision` | review of which control allowed/blocked/redacted input or output |
| `User Identity` | access and user behavior analysis |
| `Access Context` | reconstruction of user access level, tenant, role, and request source |
| `Authentication Event` | analysis of login, token, and authentication state |
| `Authorization Event` | review of authorization and access decisions |

> **Privacy:** Full prompt/response logging may contain personal data (GDPR, CCPA). Apply data minimization, retention limits, access control, and legal review—see [Chapter 4](04-data-security-privacy.md).

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)

**Implementation guidance (this guide)**
- [Chapter 4 — Prompt and telemetry logging](04-data-security-privacy.md#prompt-and-telemetry-logging-vs-privacy-gdpr--ccpa)

## SOC integration

AI incidents must not be managed separately from the organization's security view. AI logs and alerts must enter `SIEM`, `SOAR`, incident management systems, and threat hunting processes.

| Tool or capability | Application |
|---|---|
| `SIEM` | log collection and correlation |
| `SOAR` | incident response automation |
| `Threat Intelligence` | attack analysis enrichment |
| `Case Management` | incident case management |
| `Threat Hunting` | discovery of hidden attack patterns |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Manage (incident visibility)
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)

**Implementation guidance (this guide)**
- [Monitoring in AI systems](#monitoring-in-ai-systems); [Data required for telemetry](#data-required-for-telemetry)

## Detection Engineering

Logging alone is not enough. Threat detection rules must be defined for specific AI behaviors.

Sample detectable cases:

- increase in `Prompt Injection`
- `Jailbreak` attempts
- abnormal `Tool Call` rate
- model extraction attempts
- increased access to sensitive documents
- suspicious patterns in `Retrieval`
- outputs containing sensitive data
- abnormal agent behavior
- `Agent Misbehavior`
- `Excessive Tool Invocation`
- `Suspicious Retrieval Activity`
- agent privilege escalation

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: techniques in [Threat analysis with MITRE ATLAS](#threat-analysis-with-mitre-atlas)
- OWASP LLM Top 10 (2025): `LLM01`, `LLM06`; OWASP Agentic: `ASI02`

**Implementation guidance (this guide)**
- [Sample SIEM scenarios](#sample-siem-scenarios); [Appendix A threat card](15-conclusion-appendix.md#appendix-a-threat-control-and-tool-reference-card) (Chapter 15)

## Threat analysis with MITRE ATLAS

`MITRE ATLAS` can be a common language for SOC, Blue Team, and Red Team in analyzing AI incidents. Primary threat–control mapping is in [Chapter 12](12-threat-control-tools-map.md); this table is a SOC-oriented subset. Full threat–control reference including MCP and Shadow AI rows: [Appendix A of Chapter 15](15-conclusion-appendix.md#appendix-a-threat-control-and-tool-reference-card). MITRE technique summary: [Appendix B of Chapter 15](15-conclusion-appendix.md#appendix-b-mitre-atlas-mapping).

| Threat | ATLAS technique | ID |
|---|---|---|
| `Prompt Injection` | `LLM Prompt Injection` | `AML.T0051` |
| `Jailbreak` | `LLM Jailbreak` | `AML.T0054` |
| `Data Poisoning` | `Poison Training Data` | `AML.T0020` |
| `Model Extraction` | `Exfiltration via AI Inference API` | `AML.T0024` |
| `RAG Poisoning` | `RAG Poisoning` | `AML.T0070` |
| `Memory Poisoning` | `AI Agent Context Poisoning` | `AML.T0080` |
| `Tool Abuse` | `AI Agent Tool Invocation` | `AML.T0053` |
| `LLM Data Leakage` | `LLM Data Leakage` | `AML.T0057` |
| `Agent-tool Exfiltration` | `Exfiltration via AI Agent Tool Invocation` | `AML.T0086` |
| `AI Reconnaissance` | `Discover AI Agent Configuration` | `AML.T0084` |
| `Shadow MCP / Tool Poisoning` | Related: `AML.T0110` AI Agent Tool Poisoning | — |

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: techniques in table above — [Appendix B](15-conclusion-appendix.md#appendix-b-mitre-atlas-mapping)
- OWASP LLM Top 10 / Agentic mappings: [Chapter 12](12-threat-control-tools-map.md#mitre-atlas-mapping)

**Implementation guidance (this guide)**
- [Appendix A threat card](15-conclusion-appendix.md#appendix-a-threat-control-and-tool-reference-card)

## Sample SIEM scenarios

| Scenario | Detection flow | Observable indicators |
|---|---|---|
| `Prompt Injection` attempt | user sends suspicious prompt, gateway blocks it, SIEM counts blocks per user/session. | number of blocked prompts, jailbreak attempt, block rate to total requests |
| tool abuse | agent invokes multiple or sensitive tools at abnormal volume and SIEM analyzes variety and volume of use. | tool call count, number of tools used, error rate, access to sensitive tool |
| Shadow AI / consumer LLM | CASB or proxy detects bulk uploads or sustained traffic to `chat.openai.com`, `claude.ai`, or personal API endpoints from corporate identity | egress volume to AI SaaS domains, OAuth to personal tenant, DLP hits on paste events — [Ch.11](11-governance-evidence.md#shadow-ai-governance) |
| MCP schema rug-pull | gateway logs hash change on `tools/list` for registered MCP server; Agent Scan diff alerts | tool schema hash mismatch, new tool without re-consent, MCP09 shadow server discovery — [Ch.7](07-llm-rag-security.md#model-context-protocol-mcp-security) |
| GPU / inference anomaly | Falco or GPU telemetry shows cryptomining or unexpected process on inference node | GPU util spike without matching request volume, shell in inference pod — [Ch.16](16-kubernetes-deployment-reference.md) |

Thresholds must be set based on real baseline from staging or production environment. Fixed values without baseline can both create many false positives and hide real attacks.

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: `AML.T0051`, `AML.T0053`, `AML.T0054`, `AML.T0110` (MCP tool poisoning)
- OWASP MCP Top 10: `MCP09` shadow MCP server

**Implementation guidance (this guide)**
- [Shadow AI governance](11-governance-evidence.md#shadow-ai-governance) (Chapter 11); [MCP security](07-llm-rag-security.md#model-context-protocol-mcp-security) (Chapter 7)

## Sample attack chain



![](../assets/diagrams/10-monitoring-soc-ir_02.png)

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: kill-chain patterns in [Chapter 12](12-threat-control-tools-map.md#mitre-atlas-mapping)
- OWASP AI Exchange: [Threats overview](https://owaspai.org/go/threatsoverview/)

**Implementation guidance (this guide)**
- [Incident response](#incident-response); [First 30 minutes of an incident](#first-30-minutes-of-an-incident)

## Incident response

Incident response in AI must cover model and data in addition to service and infrastructure. It may be necessary to rollback the model, clean the index, delete agent memory, or review training data.

| Scenario | Initial action |
|---|---|
| data leakage from model output | stop output path, review logs, activate DLP |
| RAG contamination | remove poisoned document, re-index, review access |
| Agent tool abuse | disable tool, review trace, require human approval |
| poisoned or backdoored model | rollback to previous signed model |
| adversarial drift | stop automatic retraining and manual data review |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Manage (incident response)
- ISO/IEC 42001: incident and monitoring themes (management system)

**Implementation guidance (this guide)**
- [Appendix E.5 — Operational playbooks](17-appendix-e-implementation-reference.md#e5-operational-playbooks)

## False positive management

In AI systems, user and Agent behavior is diverse and simple rules can produce many false alerts. False positive management must be a permanent part of SOC operations.

| Control | Goal |
|---|---|
| periodic baseline | collect 2 to 4 weeks of normal traffic to set real thresholds |
| `Context-Aware Severity` | set alert severity based on full session behavior, not a single event |
| feedback loop | use SOC analyst feedback to refine rules |
| use-case segmentation | separate rules for internal user, public API, and Agent |
| temporary suppression | reduce unnecessary alerts during controlled deploy or maintenance |

The rule improvement cycle should include alert generation, SOC review, true/false positive labeling, rule refinement, new version release, and re-monitoring.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Measure (monitoring effectiveness)
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)

**Implementation guidance (this guide)**
- [Detection Engineering](#detection-engineering); [Day-2 operations](#day-2-operations)

## Incident response SLA

| Level | Sample incident | Acknowledge | Containment | Postmortem |
|---|---|---|---|---|
| `P1 Critical` | active data leakage, malicious tool execution or successful Agent abuse | **Target:** 15 minutes (adjust for team size, timezone, on-call model) | **Target:** 1 hour | mandatory, maximum 5 business days |
| `P2 High` | repeated bypass attempts, jailbreak or suspicious adversarial drift | 1 hour | 4 hours | recommended |
| `P3 Medium` | spike in block rate or anomaly without leakage evidence | 4 hours | 1 business day | if recurring |
| `P4 Low` | single block or internal test | 1 business day | not required | optional |

Incident severity must be determined based on actual impact on confidentiality, integrity, and availability—not merely alert count.

### References / Source mapping

**Frameworks and standards**
- ISO/IEC 42001: incident and monitoring themes (management system)
- EU AI Act: Art. 72 post-market monitoring (high-risk adjacency)

**Implementation guidance (this guide)**
- [Incident response](#incident-response); [Appendix E.5 — Operational playbooks](17-appendix-e-implementation-reference.md#e5-operational-playbooks)

**Author practical guidance**
- *Sample SLA targets are operational examples; adjust for team size, timezone, and on-call model.*

## Evidence required for incident analysis

| Artifact | Goal |
|---|---|
| `Prompt Trace` | reconstruction of attacker interaction |
| `Response Trace` | analysis of model response |
| `Model Version Snapshot` | identification of exact model version |
| `Conversation Evidence` | full session analysis |
| `Tool Invocation Logs` | review of Agent actions and multi-agent chain |
| `Session ID / Trace ID` | linking incidents |
| `Evidence Pack` | tamper-evident evidence retention |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Manage (incident documentation)
- EU AI Act: Art. 12 record-keeping (high-risk adjacency)
- ISO/IEC 42001: documented information for incidents

**Implementation guidance (this guide)**
- [Evidence Pack](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11); [Data required for telemetry](#data-required-for-telemetry)

## First 30 minutes of an incident

1. `Snapshot`: record prompt, response, tool call, model version, session id, and trace id.
2. `Containment`: disable high-risk tool, suspicious agent, or compromised endpoint.
3. `Verify`: check model signature, artifact integrity, and latest deploy or CT.
4. `Rollback`: return to last signed and approved version.
5. `Timeline`: record time and actions for postmortem.

Without an initial snapshot, analysis of many AI incidents will practically fail.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Manage (containment and recovery)
- MITRE ATLAS: incident technique mapping in [Chapter 12](12-threat-control-tools-map.md#mitre-atlas-mapping)

**Implementation guidance (this guide)**
- [Appendix E.5 — Operational playbooks](17-appendix-e-implementation-reference.md#e5-operational-playbooks); [Incident response](#incident-response)

## Day-2 operations

| Operation | Goal |
|---|---|
| `Secret Rotation` | reduce credential disclosure risk |
| `Agent Permission Review` | remove old or unnecessary access |
| `Embedding Cleanup` | reduce leakage in RAG |
| `Prompt Template Review` | prevent drift and bypass |
| `Prompt Trace Retention Review` | control privacy and log volume |
| `Model Retirement` | remove obsolete model and artifacts |
| `SIEM Rule Tuning` | reduce false positives |

Many incidents arise from post-deploy neglect, not only model weakness.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Manage (ongoing operations)
- OWASP AI Exchange: [Continuous validation](https://owaspai.org/go/continuousvalidation/)

**Implementation guidance (this guide)**
- [Lifecycle control point 10](06-pipeline.md#lifecycle-control-points) (Chapter 6); [False positive management](#false-positive-management)

## Security metrics

| Metric | Application |
|---|---|
| prompt injection rate | measure attack attempts |
| guardrail block rate | health of runtime controls |
| sensitive tool call count | detect abuse |
| retrieval rate from sensitive documents | detect potential leakage |
| drift score | detect data behavior change |
| rollback count | measure model release stability |

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Measure / Manage
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)

**Implementation guidance (this guide)**
- [Agent security metrics](08-agentic-ai-security.md#agent-security-metrics) (Chapter 8); [Assurance metrics](11-governance-evidence.md#assurance-metrics) (Chapter 11)

## SOC control prioritization

| Level | Control |
|---|---|
| `MUST` | runtime telemetry, prompt logging, tool logging, model version tracking and incident runbook |
| `SHOULD` | detection rule, correlation rule, SLA and threat hunting |
| `ADVANCED` | full `MITRE ATLAS` mapping, automation with `SOAR`, behavioral analytics and automated response |

### References / Source mapping

**Frameworks and standards**
- MITRE ATLAS: SOC-oriented subset in [Threat analysis with MITRE ATLAS](#threat-analysis-with-mitre-atlas)
- NIST AI RMF: Map / Measure / Manage (prioritized controls)

**Implementation guidance (this guide)**
- [Maturity roadmap](14-maturity-roadmap.md) (Chapter 14); [If only three SOC/Runtime controls](#if-only-three-socruntime-controls-can-be-implemented)

## If only three SOC/Runtime controls can be implemented

1. Send unified telemetry including prompt, tool call, model version, and trace id to SIEM.
2. At least one detection rule for prompt injection and tool abuse with false positive process.
3. Incident runbook including snapshot, containment, and rollback.

### References / Source mapping

**Frameworks and standards**
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)
- MITRE ATLAS: `AML.T0051`, `AML.T0053` detection focus

**Implementation guidance (this guide)**
- [First 30 minutes of an incident](#first-30-minutes-of-an-incident); [Evidence required for incident analysis](#evidence-required-for-incident-analysis)

**Author practical guidance**
- *Minimum viable SOC triad is this guide's prioritization when resources are constrained.*

## Practical principle

If AI behavior is not seen at `Runtime`, its security cannot be managed. Monitoring must be part of design from day one—not an add-on after deployment. For agent-specific KPIs (tool policy blocks, anomaly rate, MTTR), see [Chapter 8 — Agent security metrics](08-agentic-ai-security.md#agent-security-metrics).

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Measure / Manage (runtime visibility)
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)

**Implementation guidance (this guide)**
- [Lifecycle control point 10](06-pipeline.md#lifecycle-control-points) (Chapter 6); [Agent security metrics](08-agentic-ai-security.md#agent-security-metrics) (Chapter 8)

## Practical summary

- `Pipeline Security` alone is not sufficient; runtime must be continuously monitored.
- `Runtime Telemetry` is the foundation of AI security operations.
- detection rules must be tuned based on real baseline.
- false positive management is a permanent part of SOC operations.
- `Day-2 Operations` matters as much as deploy.
- success of AI incident response largely depends on quality of the initial snapshot.

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Measure / Manage (runtime visibility)
- OWASP AI Exchange: [MONITOR USE](https://owaspai.org/go/monitoruse/)

**Implementation guidance (this guide)**
- [Practical principle](#practical-principle); [Monitoring in AI systems](#monitoring-in-ai-systems)
