# Appendix E: Implementation Reference

> **Purpose:** Operational artifacts for teams implementing MLSecOps in production. This appendix is **not** production code or vendor-specific IaC. It complements the reference chapters with architecture cards, decision matrices, fill-in templates, playbooks, and a master control matrix.
>
> **Relationship to other appendices:** Appendix A/B summarize threat and ATLAS mappings; Appendix D covers managed AI checklists. This appendix ties them to **your architecture choice**.

### References / Source mapping

**Implementation guidance (this guide)**
- [Traceability convention](15-conclusion-appendix.md#traceability-and-source-mapping-convention) (Chapter 15)
- [Master control matrix](#e6-master-control-matrix) maps to [lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6)

**Author practical guidance**
- *Architecture cards, templates, and matrices are operational aids—not normative standard text.*

---

## E.1 Architecture Cards

Each card lists minimum security boundaries, primary control points ([Chapter 6](06-pipeline.md)), and deep-dive chapters. Adapt names and namespaces to your environment.

### E.1.1 Enterprise RAG (internal knowledge base)

**When to use:** Organization-owned documents retrieved at query time; model may be managed API or self-hosted.



![](../assets/diagrams/17-appendix-e-implementation-reference_01.png)


| Area | Minimum controls | Control points | Guide |
|---|---|---|---|
| Ingest | Allowlist sources, PII scan, hash per document version | 2, 3, 4 | [Ch.7 ingest](07-llm-rag-security.md#ingest-security-in-rag) |
| Retrieval | Tenant ACL at query time, no cross-tenant index | 7, 10 | [Ch.7 three-layer](07-llm-rag-security.md#three-layer-controls-in-rag) |
| Runtime | Gateway, output gate, prompt-injection tests | 7, 10 | [Ch.7](07-llm-rag-security.md), [Ch.10](10-monitoring-soc-ir.md) |
| Re-index | Playbook on source change or poison suspicion | 4, 5 | [Ch.7 Reindex](07-llm-rag-security.md#reindex-playbook) |

---

### E.1.2 Managed AI API (Azure OpenAI, Amazon Bedrock, Google Vertex AI)

**When to use:** Provider hosts base model weights; customer controls prompts, RAG, gateway, keys, and logging.



![](../assets/diagrams/17-appendix-e-implementation-reference_02.png)


| Area | Minimum controls | Control points | Guide |
|---|---|---|---|
| Identity | No long-lived keys in code; RBAC per deployment | 1, 3, 8 | [Ch.2 managed AI](02-scope-risk-threat-model.md#managed-ai-services-security-reference), [Appendix D](15-conclusion-appendix.md#appendix-d-managed-ai-services-security-reference) |
| Configuration | Approved model/deployment ID, region, API version snapshot | 5, 8, 9 | Appendix D Evidence fields |
| Data boundary | DLP on prompt/response; RAG ACL | 4, 7, 10 | [Ch.4](04-data-security-privacy.md), [Ch.7](07-llm-rag-security.md) |
| Evidence | Cannot sign weights → config snapshot + test report | 9 | [Ch.11 Evidence Pack](11-governance-evidence.md#what-is-an-evidence-pack) |

**Vendor notes (informative):**

| Provider | Customer records in Evidence Pack |
|---|---|
| Azure OpenAI | Resource name, deployment name, API version, content-filter config hash |
| Amazon Bedrock | Model ID, guardrail ID/version, region, inference profile ARN |
| Google Vertex AI | Model resource path, region, safety settings snapshot |

---

### E.1.3 Self-hosted LLM (vLLM / KServe on Kubernetes)

**When to use:** Organization controls model weights, inference stack, and cluster.



![](../assets/diagrams/17-appendix-e-implementation-reference_03.png)


| Area | Minimum controls | Control points | Guide |
|---|---|---|---|
| Supply chain | ModelScan, signing, verify before serve | 2, 3, 9 | [Ch.5](05-model-artifact-supply-chain.md), [Ch.16](16-kubernetes-deployment-reference.md) |
| Cluster | Namespace isolation, NetworkPolicy, signed images | 3, 9, 10 | [Ch.16](16-kubernetes-deployment-reference.md) |
| Runtime | API key on inference, rate limits, egress allowlist | 10 | [Ch.16 vLLM pattern](16-kubernetes-deployment-reference.md#vllm-on-kubernetes-secure-deployment-pattern) |
| CT / retrain | Same lifecycle as initial release | 4, 7, 8, 9 | [Ch.6 CT cycle](06-pipeline.md#continuous-training-cycle) |

---

### E.1.4 Agent with tools (MCP / APIs)

**When to use:** LLM can invoke tools, read files, or perform multi-step actions.



![](../assets/diagrams/17-appendix-e-implementation-reference_04.png)


| Area | Minimum controls | Control points | Guide |
|---|---|---|---|
| Tools | Least privilege, allowlist, schema pin | 7, 10 | [Ch.8](08-agentic-ai-security.md#tool-trust-boundary), [Ch.7 MCP](07-llm-rag-security.md#model-context-protocol-mcp-security) |
| High-risk actions | HITL for financial/destructive operations | 7, 8 | [Ch.8 Intent Gate](08-agentic-ai-security.md#intent-gate) |
| Memory | Sanitize on write, TTL, tenant isolation | 7, 10 | [Ch.8 Memory Poisoning](08-agentic-ai-security.md#memory-poisoning) |
| MCP | Gateway, `mcps-audit` / Agent Scan, no shadow MCP | 3, 7 | [Ch.7 MCP hardening](07-llm-rag-security.md#mcp-server-hardening-checklist-minimum-bar) |

---

### E.1.5 Multi-agent system

**When to use:** Multiple agents delegate tasks, share memory, or call each other.



![](../assets/diagrams/17-appendix-e-implementation-reference_05.png)


| Area | Minimum controls | Control points | Guide |
|---|---|---|---|
| Delegation | Sub-agent cannot exceed parent tool scope | 7, 10 | [Ch.8 Multi-Agent](08-agentic-ai-security.md#multi-agent) |
| Trust | Treat inter-agent messages as untrusted input | 7 | [Ch.8 MAESTRO](08-agentic-ai-security.md#maestro-framework-csa) |
| Observability | Trace ID across agent chain | 10 | [Ch.10 telemetry](10-monitoring-soc-ir.md#data-required-for-telemetry) |

---

### E.1.6 Classic ML (tabular / vision — no LLM)

**When to use:** Traditional training pipeline; no prompt/RAG/agent surface.

| Area | Minimum controls | Control points | Guide |
|---|---|---|---|
| Data | Lineage, PII, poison checks | 2, 4 | [Ch.4](04-data-security-privacy.md) |
| Model | ModelScan, adversarial test for modality | 3, 7 | [Ch.5](05-model-artifact-supply-chain.md) |
| Release | Sign artifacts, Evidence Pack | 8, 9 | [Ch.6](06-pipeline.md), [Ch.11](11-governance-evidence.md) |

---

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Map (architecture-dependent controls); OWASP LLM Top 10 / ASI / MCP themes per card

**Implementation guidance (this guide)**
- Architecture cards E.1.1–E.1.6 cross-link Chapters 2, 4–8, 10–11, 16, and [Appendix D](15-conclusion-appendix.md#appendix-d-managed-ai-services-security-reference)

**Author practical guidance**
- *Cards are fill-in operational patterns—not normative standard text.*

## E.2 Decision Matrix

Use this matrix to select **mandatory control themes** by architecture. Map each row to control points in [Chapter 6](06-pipeline.md) and evidence in E.4.

| If your primary architecture is… | You must prioritize… | Blocking release decisions at… | Integrity evidence at… | Start chapters |
|---|---|---|---|---|
| **Managed AI API only** | Gateway, DLP, config snapshot, Shadow AI policy | 4 (data in prompts/RAG), 7 (injection/leak tests), 8 | 9 (deployment ID, region, config hash—not weight signature) | Ch.2, 7, Appendix D |
| **Enterprise RAG** | Ingest ACL, retrieval ACL, reindex playbook, output gate | 4 (poisoned corpus), 7 (RAG leakage tests), 8 | 9 (index version hash + model/config evidence) | Ch.4, 7 |
| **Self-hosted LLM** | Model scan, signing, K8s isolation, admission verify | 4, 7, 8 | 9 (signature + attestation) | Ch.5, 6, 16 |
| **Agent + MCP** | Intent Gate, tool allowlist, MCP scan, HITL | 7 (tool misuse tests), 8 | 9 (agent config + tool manifest hash) | Ch.7, 8 |
| **Multi-agent** | Delegation policy, session trace, bus isolation | 7, 8 | 9 + inter-agent policy version | Ch.8, 10 |
| **Classic ML** | Data validation, adversarial test, signing | 4, 7, 8 | 9 (model signature) | Ch.4, 5, 6 |

**Reference implementation flow (implementation-neutral):**

Organizations often implement the lifecycle through existing delivery tooling. A typical **pattern** (not a mandated stack):



![](../assets/diagrams/17-appendix-e-implementation-reference_06.png)


| Stage | Example capabilities (informative) | Control points |
|---|---|---|
| Change trigger | GitLab/GitHub merge, ticket, scheduled CT | 1 |
| Scan layer | Gitleaks, Trivy, ModelScan | 2, 3 |
| Security validation | Garak, Promptfoo, ART (by modality) | 7 |
| Policy decision | OPA/Conftest, GRC workflow | 4, 8 |
| Evidence Pack | JSON bundle, GRC record, registry metadata | 8, 9, 10 |
| Deploy | Canary, signed image verify, gateway policy version | 9, 10 |

> This guide does not ship CI/CD templates. Implement and test flows in your environment. Tool examples: [Chapter 12 appendix](12-threat-control-tools-map.md#appendix-informative-tool-command-reference).

---

### References / Source mapping

**Frameworks and standards**
- OpenSSF MLSecOps whitepaper (2025): lifecycle stage mapping (informative)

**Implementation guidance (this guide)**
- [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6); [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6)

**Author practical guidance**
- *Decision matrix rows and example CI/CD stages are illustrative—mandatory themes vary by threat model.*

## E.3 Threat Model Template

Copy this table per system or architecture card. Replace placeholders. Output should feed control point criteria and Evidence Pack requirements ([Chapter 2](02-scope-risk-threat-model.md#expected-output-of-threat-modeling)).

**System:** _________________________ **Architecture card:** _________________________ **Date / version:** _________

| Asset | Threat (STRIDE / OWASP / ATLAS ref) | Control (prevent / detect / respond) | Lifecycle control point(s) | Residual risk (accept / mitigate / transfer) | Evidence required |
|---|---|---|---|---|---|
| Training dataset | e.g. `Data Poisoning`, `ML01` | Validation, lineage, PII mask | 2, 3, 4 | | Scan report, lineage ID |
| Model weights | e.g. backdoor, unsigned swap | ModelScan, signing | 3, 7, 9 | | Hash, signature verify log |
| RAG index | e.g. `Retrieval Poisoning` | Ingest ACL, reindex playbook | 4, 5, 7 | | Index version hash |
| Prompt / system instructions | e.g. `LLM01` injection | Gateway, guardrails, red team | 7, 10 | | Test report URI |
| Agent tools / MCP | e.g. `ASI02`, `MCP09` | Intent Gate, allowlist, scan | 3, 7, 10 | | Tool manifest hash, scan PDF |
| API keys / secrets | e.g. exposure in agent trace | Vault, proxy, rotation | 3, 10 | | Secret scan clean, rotation log |
| Inference endpoint | e.g. model theft, GPU abuse | AuthN/Z, rate limit, Falco | 10 | | Access log sample |
| Managed API config | e.g. wrong region/model ID | Config review, snapshot | 5, 8, 9 | | `config_snapshot_hash` |

**Release blockers (define explicitly):**

- [ ] Unmasked PII in training or RAG ingest → block at control point **4**
- [ ] Security validation below threat-model threshold → block at **7**
- [ ] Policy/compliance review failed → block at **8**
- [ ] Missing signature or config snapshot → block at **9**

---

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10 (`LLM01`); OWASP ML Top 10 (`ML01`, `ML02`); MITRE ATLAS technique IDs in table placeholders; STRIDE (informative)

**Implementation guidance (this guide)**
- [Expected output of threat modeling](02-scope-risk-threat-model.md#expected-output-of-threat-modeling) (Chapter 2); [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6)

**Author practical guidance**
- *Template table and release blockers are fill-in worksheets—not a certified threat-modeling method.*

## E.4 Evidence Pack Template

An `Evidence Pack` is an **audit evidence pattern** ([Chapter 11](11-governance-evidence.md#what-is-an-evidence-pack)). Use the structure below as a fill-in template (JSON, YAML, or GRC form). Field names are illustrative.

```yaml
# Evidence Pack — template (informative; validate in your GRC/tooling)
evidence_pack:
  id: "ep-YYYY-MM-DD-<release-id>"
  system_name: ""
  architecture_card: ""  # e.g. enterprise-rag, managed-api, self-hosted-vllm
  release_version: ""
  control_point_8_approval:
    approver: ""
    decision: "approve | reject | risk_accept"
    timestamp: ""
    exception_id: ""  # if risk_accept

  data:
    dataset_version: ""
    lineage_uri: ""
    pii_scan_result: "pass | fail"
    sensitivity_class: ""

  model:
    model_id: ""
    artifact_hash: ""
    signature_verify: "pass | n/a-managed-api"
    ai_bom_uri: ""

  managed_api:  # omit if self-hosted
    provider: "azure-openai | bedrock | vertex"
    deployment_id: ""
    region: ""
    api_version: ""
    config_snapshot_hash: ""

  rag:  # omit if not applicable
    index_version_hash: ""
    source_allowlist_version: ""
    reindex_playbook_run: "yes | no"

  agent_mcp:  # omit if not applicable
    agent_config_hash: ""
    tool_allowlist_version: ""
    mcp_scan_report_uri: ""

  security_validation:
    report_uri: ""
    test_suite_hash: ""
    control_point_7_result: "pass | fail"

  supply_chain:
    sbom_uri: ""
    vulnerability_summary: ""

  policy:
    opa_bundle_version: ""
    gate_decisions: []

  deployment:
    environment: ""
    canary_result: ""
    rollback_plan_uri: ""

  runtime:
    gateway_policy_version: ""
    siem_feed_active: "yes | no"
```

**Minimum sections for Level 1 maturity:** `data`, `security_validation`, `policy`, `release approval`, and either `model.signature_verify` or `managed_api.config_snapshot_hash`.

---

### References / Source mapping

**Frameworks and standards**
- CycloneDX AI/ML BOM themes; NIST AI RMF: Measure (evidence and documentation)

**Implementation guidance (this guide)**
- [What is an Evidence Pack?](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11); [Recommended Evidence Pack contents](11-governance-evidence.md#recommended-evidence-pack-contents) (Chapter 11); [Appendix D Evidence fields](15-conclusion-appendix.md#evidence-pack-fields-managed-api) (Chapter 15)

**Author practical guidance**
- *YAML field names and minimum sections are illustrative implementation patterns.*

## E.5 Operational Playbooks

Short runbooks for SOC and platform teams. Expand with your tooling, contacts, and SLAs ([Chapter 10](10-monitoring-soc-ir.md)).

### E.5.1 Runtime prompt injection (direct or indirect)

| Phase | Actions | Owner | Evidence |
|---|---|---|---|
| **Detect** | SIEM alert: guardrail block spike, jailbreak pattern, or user report | SOC | Alert ID, `Prompt Trace` |
| **Contain** | Tighten gateway rules; disable high-risk tools if agent involved; rate-limit source IP/session | Platform / SOC | Change ticket, policy version |
| **Preserve** | Snapshot prompt, response, model version, session/trace ID, retrieved context hash | SOC | [Ch.10 first 30 min](10-monitoring-soc-ir.md#first-30-minutes-of-an-incident) |
| **Eradicate** | If RAG indirect: remove/quarantine document, re-index; if model-specific: rollback to last signed release | ML / Platform | Reindex log, rollback record |
| **Recover** | Restore service with updated tests at control point 7; monitor false positive rate | ML / SOC | Updated test report in Evidence Pack |
| **Lessons learned** | Update threat model, detection rules, ingest allowlist; postmortem within SLA | Security | Postmortem URI in governance record |

---

### E.5.2 RAG corpus contamination / retrieval poisoning

| Phase | Actions | Owner | Evidence |
|---|---|---|---|
| **Detect** | Abnormal answers citing unknown doc IDs; ingest anomaly; user report | SOC / ML | Retrieval log, document hash |
| **Contain** | Disable affected collection or tenant; stop ingest pipeline | Platform | Index isolation record |
| **Preserve** | Export poisoned document metadata, ingest audit trail, query logs | SOC | Evidence Pack runtime section |
| **Eradicate** | Delete poisoned objects; run [Reindex Playbook](07-llm-rag-security.md#reindex-playbook); ACL review | ML Engineer | New `index_version_hash` |
| **Recover** | Regression prompt suite at control point 7; canary traffic | ML / Platform | Validation report |
| **Lessons learned** | Tighten ingest scan; update source allowlist | Security / Data | Updated threat model row |

---

### E.5.3 Agent tool abuse / unauthorized action

| Phase | Actions | Owner | Evidence |
|---|---|---|---|
| **Detect** | Spike in sensitive tool calls; DLP hit; anomalous API egress | SOC | `Tool Invocation Logs`, trace ID |
| **Contain** | Disable tool or agent; invoke kill switch on API keys | Platform | Disable timestamp |
| **Preserve** | Full session trace, agent config version, tool argument logs | SOC | [Ch.10 evidence table](10-monitoring-soc-ir.md#evidence-required-for-incident-analysis) |
| **Eradicate** | Review Intent Gate policy; rotate secrets; patch tool scope | AppSec | Policy diff, rotation log |
| **Recover** | Re-enable with HITL for high-risk tools; red-team agent scenarios | ML / AppSec | Control point 7 agent tests |
| **Lessons learned** | Update tool allowlist; add SOC correlation rule | Security | Updated E.3 threat model |

---

### References / Source mapping

**Frameworks and standards**
- NIST AI RMF: Manage (incident response and recovery)

**Implementation guidance (this guide)**
- [Incident response](10-monitoring-soc-ir.md#incident-response) (Chapter 10); [First 30 minutes of an incident](10-monitoring-soc-ir.md#first-30-minutes-of-an-incident) (Chapter 10); [Reindex Playbook](07-llm-rag-security.md#reindex-playbook) (Chapter 7)

**Author practical guidance**
- *Playbook phases and owners are starter runbooks—expand with your SLAs and tooling.*

## E.6 Master Control Matrix

Unified view: **threat → prevent / detect / respond → lifecycle layer → control point → evidence**. Detailed tool names: [Chapter 12](12-threat-control-tools-map.md).

| Threat / attack | Prevent | Detect | Respond | Layer | Control point(s) | Evidence |
|---|---|---|---|---|---|---|
| `Data Poisoning` | Validation, lineage, ingest ACL | Drift, quality anomalies | Stop CT, quarantine dataset | Data | 2, 3, 4 | Scan report, lineage ID |
| `PII` leakage | Masking, DLP ingress/egress | DLP alerts, retrieval audit | Block output path, purge logs | Data / Runtime | 4, 10 | DLP log, mask proof |
| Poisoned model / pickle RCE | ModelScan, safe formats | Artifact scan in CI | Block promote, quarantine artifact | Model / Supply chain | 3, 7, 9 | ModelScan JSON, hash |
| Unsigned / swapped artifact | Signing, admission verify | Verify fail at deploy | Deny deploy, rollback | Supply chain | 9 | Signature log |
| `Prompt Injection` | Gateway, input limits | Guardrail blocks, SIEM rules | Contain session, tighten policy | Runtime | 7, 10 | Prompt trace, test report |
| `RAG` / retrieval poisoning | Ingest scan, ACL | Bad citation patterns | Reindex, isolate collection | RAG | 4, 5, 7 | Index hash, reindex log |
| `Tool Abuse` / `ASI02` | Intent Gate, scoped IAM | Tool rate anomalies | Disable tool, HITL | Agent | 7, 10 | Tool logs, policy version |
| MCP tool poisoning / `MCP09` | Allowlist, gateway, static scan | Schema rug-pull detection | Revoke server, re-consent | MCP | 3, 7 | `mcps-audit` report |
| Memory poisoning | Sanitize on write, TTL | Conversation drift | Clear memory store | Agent | 7, 10 | Memory purge record |
| Shadow AI | AI-AUP, CASB | Egress to consumer LLM | Block, user outreach | Governance | 1, 11 | AUP version, CASB alert |
| K8s / infra exposure | NetworkPolicy, RBAC | Falco, unsigned image deny | Isolate namespace | Infrastructure | 3, 10 | Admission denial log |
| Adversarial drift | Baseline prompts, canary | Session anomaly vs baseline | Stop auto-CT, manual review | Runtime | 7, 10 | Drift playbook ref |

---

### References / Source mapping

**Frameworks and standards**
- OWASP LLM Top 10, OWASP ML Top 10, OWASP ASI (`ASI02`), OWASP MCP Top 10 (`MCP09`); MITRE ATLAS techniques referenced in [Chapter 12](12-threat-control-tools-map.md#mitre-atlas-mapping)

**Implementation guidance (this guide)**
- [Primary Mapping](12-threat-control-tools-map.md#primary-mapping) (Chapter 12); [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6)

**Author practical guidance**
- *Matrix consolidates guide guidance for gap analysis—it does not add new normative requirements.*

## Practical summary

1. Pick an **architecture card** (E.1) and confirm rows in the **decision matrix** (E.2).
2. Complete the **threat model template** (E.3) and define release blockers at control points 4, 7, 8, 9.
3. Instantiate the **Evidence Pack template** (E.4) in your GRC or registry workflow.
4. Wire **playbooks** (E.5) into SOC runbooks and on-call.
5. Use the **master control matrix** (E.6) for design review and gap analysis against [Chapter 12](12-threat-control-tools-map.md).

This appendix does not add new normative requirements beyond the lifecycle model in [Chapter 6](06-pipeline.md). It packages existing guidance for production implementation.
