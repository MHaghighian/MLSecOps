# Standards Alignment & Conformance Profile

This reference consolidates clause-level cross-walks from the **MLSecOps Reference Model & Practical Guide** to external AI security standards alongside a formal, machine-verifiable **MLSecOps Conformance Profile (`MLS-*`)**.

> **Boundary note:** This document provides independent community cross-walks and a technical conformance schema. It is **not** an official certification scheme, normative ISO standard reproduction (ISO/IEC copyrighted text is referenced by clause topic only), or legal compliance determination.

---

## 1. MLSecOps Conformance Profile (`MLS-*` Levels 1–3)

Controls are declared per release in Evidence Pack `conformanceProfile` (`profileVersion`, `targetLevel` `1 | 2 | 3`, `controlIds`) defined in [`schemas/evidence-pack.schema.json`](../schemas/evidence-pack.schema.json) and wrapped optionally in a canonical **`https://in-toto.io/Statement/v1`** envelope ([`schemas/mlsecops-attestation.v1.schema.json`](../schemas/mlsecops-attestation.v1.schema.json)).

| Control ID | Min Level | Domain | Technical Requirement | Executable Enforcement |
|---|---|---|---|---|
| `MLS-DT-01` | L1 | Data & RAG (`CP 4`) | Dataset lineage URI, sensitivity class, and PII scan pass recorded before training/ingestion | `cp4_dataAndRagAclGate.status == "PASS"`, `dataProvenance.piiScanResult` |
| `MLS-DT-02` | L2 | Data & RAG (`CP 4`) | Vector DB index hash tracked; deletion/revocation covers replicas, cold backups, and snapshots | `cp8_cp9_admission.rego` checks `backupRevocationVerified != false` when `vectorIndexVersionHash` is set |
| `MLS-SC-01` | L1 | Supply Chain (`CP 5, 9`) | Cryptographic SHA-256 weight digest bound across `CP 8` approval and `CP 9` admission (`configSnapshotHash` for `Managed-API`) | `cp8_cp9_admission.rego` `boundToCp9Digest` equality + `cp9_checkpointVerified` |
| `MLS-SC-02` | L2 | Supply Chain (`CP 5, 6`) | CycloneDX AI-BOM components with valid SHA-256 hashes (no MD5/SHA-1), zero `aisbom:unreadable`, static model artifact inspection | `cp8_cp9_admission.rego` `components` rules + `ai_security_scan.py --model` (`MODEL-*`) |
| `MLS-SC-03` | L3 | Supply Chain (`CP 8, 9`) | Release Evidence Pack wrapped in signed `in-toto` v1 Statement + DSSE (`application/vnd.in-toto+json`), Witness step collections / Archivista graph storage, and TEE provenance | `mlsecops-attestation.v1.schema.json`, `dsse-envelope.v1.schema.json`, `--emit-dsse`, `policies/witness/mlsecops-witness-policy.json`, [INTOTO-WITNESS-ARCHIVISTA](INTOTO-WITNESS-ARCHIVISTA.md) |
| `MLS-CP-01` | L1 | Lifecycle Gates (`CP 1–8`) | Named `sharedResponsibilityRecord` (`modelOwner`, `platformOwner`, `socOwner`) + blocking `CP 4 / 7 / 8` gates | `cp8_cp9_admission.rego` ownership & gate rules |
| `MLS-CP-02` | L2 | Validation (`CP 7`) | Quantitative adversarial/red-team threshold (`agentMisalignmentScore <= 0.15`, `redTeamPhasesCompleted >= 4` for LLM/Agentic) | `cp8_cp9_admission.rego` `CP7` gate rules |
| `MLS-AG-01` | L2 | Agentic & MCP (`CP 7, 10`) | Kill switch, scoped non-human identity credentials, `Intent Gate`, bounded delegation (`<= 4`), and capped MCP sampling | `cp8_cp9_admission.rego` `runtimeAgentConfig` rules + `MCP-SAMP-01` / `MCP-AUTHZ-01` |
| `MLS-AG-02` | L2 | MCP Integrity (`MCP09`) | Pinned `tools/list` SHA-256 hashes in `mcpSchemaHashes`, TLS/non-SSRF endpoints, zero tool-poisoning/Unicode-tag smuggling | `cp8_cp9_admission.rego` `MCP` rules + `ai_security_scan.py --mcp --pins` |
| `MLS-RT-01` | L1 | Runtime & Serving (`CP 9, 10`) | Non-root container, dropped capabilities, secrets via secret store, local runner network isolation (`E.1.7`), `rawPromptLoggingDisabled` + SIEM feed | `policies/k8s/inference_workload.rego` + `cp8_cp9_admission.rego` |
| `MLS-RT-02` | L2 | KV & Inference Isolation | Multi-tenant KV cache partitioning and cross-model KV reuse alignment guard (`PromptPeek`/`KV-Cloak`/`VReparo`) | `inferenceConfig.crossModelKvCacheReuse` + `tenantKvPartitioned` rules |
| `MLS-TR-01` | L2 | Distributed Training (`E.1.8`) | Collective network (NCCL/RoCE) isolation, worker node attestation, checkpoint signing, preference data provenance, and SFT-to-DPO intermediate validation | `trainingClusterConfig` schema + `cp8_cp9_admission.rego` `Pretraining-Distributed` rules |
| `MLS-TR-02` | L3 | Distributed Training (`E.1.8`) | Gradient norm clipping active and Differential Privacy (`DP-SGD`/`DP-DPO`) privacy accounting applied on sensitive corpora | `trainingClusterConfig.gradientClippingActive` & `dpTrainingApplied` |

> **Maturity enforcement note:** In `policies/cp8_cp9_admission.rego`, Evidence Packs claiming `conformanceProfile.targetLevel >= 2` must declare non-empty `MLS-*` `controlIds`.

---

## 2. OWASP AISVS v1.0 (`C1`–`C12`) Cross-Walk

Maps the twelve verified verification chapters of the **OWASP AI Security Verification Standard (AISVS v1.0)** to MLSecOps lifecycle controls, chapters, and executable checks.

| AISVS Category | AISVS Focus | MLSecOps Control Points | Primary Chapters & Artifacts | Executable Verification |
|---|---|---|---|---|
| **C1** Training Data Integrity & Traceability | Data provenance, poisoning resistance, PII scrubbing, lineage | `CP 2, 4` | [Ch.4](../chapters-en/04-data-security-privacy.md), [E.1.8](../chapters-en/17-appendix-e-implementation-reference.md#e18-pretraining--distributed-fine-tuning-cluster-ddp--fsdp--rlhf--dpo) | `cp4_dataAndRagAclGate`, `dataProvenance`, `preferenceDataProvenanceVerified` |
| **C2** Input Validation | Prompt injection filtering, parser hardening, modality input bounds | `CP 7, 10` | [Ch.7](../chapters-en/07-llm-rag-security.md), [Ch.12](../chapters-en/12-threat-control-tools-map.md) | `ai_security_scan.py` (`MCP-UNI-01`, `MCP-POISON-01`, `MODEL-GGUF-SSTI`) |
| **C3** Model Lifecycle Management & Change Control | Change initiation, CI gates, checkpoint immutability, retirement | `CP 1, 5, 6, 8, 9` | [Ch.6](../chapters-en/06-pipeline.md), [Ch.11](../chapters-en/11-governance-evidence.md) | `cp8_releaseDecisionGate.boundToCp9Digest`, `intermediateStageValidated` |
| **C4** Infrastructure, Configuration & Deployment Security | Serving isolation, GPU memory hygiene, Pod Security, network policy | `CP 9, 10` | [Ch.16](../chapters-en/16-kubernetes-deployment-reference.md), [E.1.3](../chapters-en/17-appendix-e-implementation-reference.md#e13-self-hosted-llm-vllmkserve-on-kubernetes), [E.1.7](../chapters-en/17-appendix-e-implementation-reference.md#e17-developer-local-inference-docker-model-runner) | `policies/k8s/inference_workload.rego`, `localRunnerConfig`, `collectiveNetworkIsolated` |
| **C5** Access Control & Identity for AI Components & Users | Scoped NHI credentials, RAG retrieval ACLs, auth on serving endpoints | `CP 4, 8, 10` | [Ch.4](../chapters-en/04-data-security-privacy.md), [Ch.8](../chapters-en/08-agentic-ai-security.md), [Ch.16](../chapters-en/16-kubernetes-deployment-reference.md) | `scopedCredentialsRequired`, K8s `VLLM_API_KEY`/`--api-key` rule, `MCP-AUTHZ-01` |
| **C6** Supply Chain Security for Models | Weight serialization scanning, AI-BOM, Cosign/`in-toto` provenance | `CP 3, 5, 9` | [Ch.5](../chapters-en/05-model-artifact-supply-chain.md), [`schemas/`](../schemas/README.md) | `MODEL-*` checks (`PKL`, `ZIP`, `ST`, `ONNX`, `NPY`), `mlsecops-attestation.v1.schema.json` |
| **C7** Model Behavior, Output Control & Safety Assurance | Guardrails, red-team validation, misalignment thresholds, SSTI prevention | `CP 7, 10` | [Ch.7](../chapters-en/07-llm-rag-security.md), [Ch.12](../chapters-en/12-threat-control-tools-map.md) | `cp7_adversarialAndRedTeamGate` (`agentMisalignmentScore`, `redTeamPhasesCompleted`), `MODEL-SSTI-01` |
| **C8** Memory, Embeddings & Vector Database Security | RAG corpus ACLs, embedding inversion, persistent agent memory, backup purge | `CP 4, 7, 10` | [Ch.4](../chapters-en/04-data-security-privacy.md), [Ch.7](../chapters-en/07-llm-rag-security.md), [Ch.8](../chapters-en/08-agentic-ai-security.md) | `vectorIndexVersionHash` + `backupRevocationVerified`, `memoryProvenanceVerified`, `tenantKvPartitioned` |
| **C9** Orchestration & Agentic Security | Intent Gate, bounded multi-agent delegation, HITL kill switches | `CP 7, 8, 10` | [Ch.8](../chapters-en/08-agentic-ai-security.md), [AARM Alignment](AARM-ALIGNMENT.md) | `killSwitchEnabled`, `intentGateEnabled`, `delegationDepthMax <= 4` |
| **C10** Model Context Protocol (MCP) Security | Schema pinning (`MCP09`), SSRF, command injection, TLS, shadowing | `CP 7, 9, 10` | [Ch.8](../chapters-en/08-agentic-ai-security.md), [Ch.13](../chapters-en/13-case-studies.md) | `mcpSchemaHashes`, `MCP-*` scanner checks (`MCP09-SHADOW-*`, `MCP-SSRF-01`, `MCP-EXEC-01`) |
| **C11** Adversarial Robustness & Attack Resistance | Evasion/backdoor testing, KV side-channels, RLHF gradient/preference bounds | `CP 2, 7` | [Ch.3](../chapters-en/03-threat-landscape.md), [Ch.7](../chapters-en/07-llm-rag-security.md), [E.1.8](../chapters-en/17-appendix-e-implementation-reference.md#e18-pretraining--distributed-fine-tuning-cluster-ddp--fsdp--rlhf--dpo) | `gradientClippingActive`, `crossModelKvCacheReuse` + `kvAlignmentControlActive` |
| **C12** Monitoring, Logging & Anomaly Detection | AI SIEM feeds, privacy-safe telemetry (no raw prompt logging), IR triggers | `CP 10` | [Ch.10](../chapters-en/10-monitoring-soc-ir.md), [E.5](../chapters-en/17-appendix-e-implementation-reference.md#e5-operational-playbooks) | `runtimeTelemetry.siemFeedActive`, `rawPromptLoggingDisabled` |

---

## 3. CSA MAESTRO 7-Layer Architecture Cross-Walk

Maps the **Cloud Security Alliance (CSA) MAESTRO** seven-layer agentic threat modeling stack to MLSecOps lifecycle controls.

| MAESTRO Layer | Scope | MLSecOps Controls & Artifacts |
|---|---|---|
| **Layer 1: Foundation Models** | Base weights, alignment stability, cross-model KV safety, pretraining/DPO backdoors | [Ch.5](../chapters-en/05-model-artifact-supply-chain.md), [Ch.7 KV Safety](../chapters-en/07-llm-rag-security.md), [E.1.8](../chapters-en/17-appendix-e-implementation-reference.md#e18-pretraining--distributed-fine-tuning-cluster-ddp--fsdp--rlhf--dpo) |
| **Layer 2: Data Operations** | Corpus lineage, PII classification, RAG ACLs, vector backup revocation, preference datasets | [Ch.4](../chapters-en/04-data-security-privacy.md), `CP 4`, `dataProvenance` |
| **Layer 3: Agent Frameworks** | Intent Gate, bounded delegation, persistent memory integrity, `samplingBudgetCapped` | [Ch.8](../chapters-en/08-agentic-ai-security.md), `runtimeAgentConfig`, [AARM Alignment](AARM-ALIGNMENT.md) |
| **Layer 4: Deployment Infrastructure** | Kubernetes Pod Security, non-root serving, NCCL collective isolation, DMR local isolation | [Ch.16](../chapters-en/16-kubernetes-deployment-reference.md), `policies/k8s/inference_workload.rego`, `localRunnerConfig` |
| **Layer 5: Evaluation and Observability** | Red-team gates (`CP 7`), misalignment scoring, privacy-preserving SOC/SIEM telemetry | [Ch.10](../chapters-en/10-monitoring-soc-ir.md), [Ch.12](../chapters-en/12-threat-control-tools-map.md), `runtimeTelemetry` |
| **Layer 6: Security and Compliance** | Cryptographic release binding (`CP 8 ↔ CP 9`), Evidence Pack, `in-toto` Statement v1, ISO 42001/27090 | [Ch.6](../chapters-en/06-pipeline.md), [Ch.11](../chapters-en/11-governance-evidence.md), [`mlsecops-attestation.v1.schema.json`](../schemas/mlsecops-attestation.v1.schema.json) |
| **Layer 7: Agent Ecosystem** | MCP server registry/pinning (`MCP09`), cross-server name collision checks, external tool SSRF/TLS guards | [Ch.8](../chapters-en/08-agentic-ai-security.md), `ai_security_scan.py --mcp`, `mcpSchemaHashes` |

---

## 4. ISO/IEC 27090:2026, ISO/IEC 42001:2023, NIST AI RMF & MITRE ATLAS Bridge

| Governance / Risk Clause | ISO/IEC 27090:2026 Focus | ISO/IEC 42001:2023 (AIMS) | NIST AI RMF 1.0 Function | MITRE ATLAS Core Anchor | MLSecOps Control Point & Verification |
|---|---|---|---|---|---|
| Context, Scope & Accountability | Clause 5 (Security objectives & context) | Clauses 4–5 (Context, Leadership, Roles) | **Govern** (`GV-1`, `GV-3`) | — (Scope boundary) | `CP 1` + `metadata.sharedResponsibilityRecord` |
| Risk Assessment & Threat Modeling | Clauses 6.2–6.5 (Poisoning, Evasion, MIA, Inversion) | Clauses 6.1, 8.2 (Risk assessment & impact) | **Map** (`MP-2`, `MP-4`, `MP-5`) | `AML.TA0002`, `AML.T0020`, `AML.T0015` | `CP 2, 3, 4` + [Ch.2](../chapters-en/02-scope-risk-threat-model.md) + `E.3` |
| Data, Preference & Supply Chain Provenance | Clause 6.2 & Annex B/C (Data & distributed training) | Clause 8.4 & Annex B.7 (Data management) | **Govern** (`GV-SC`) / **Map** | `AML.T0010`, `AML.T0018` | `CP 4, 5, 9` + `in-toto` v1 + `MODEL-*` checks |
| Validation, Adversarial Testing & Tradeoffs | Clauses 6.6–6.11 & Clause 7 (Mitigation tradeoffs) | Clauses 8.3, 9.1 (Verification & evaluation) | **Measure** (`MS-2`, `MS-4`) | `AML.T0043`, `AML.T0051`, `AML.T0054` | `CP 7` (`agentMisalignmentScore`, red-team phases) |
| Release Admission, Runtime SOC & Continuous Improvement | Annex A/B (Deployment & runtime monitoring) | Clauses 9.2, 10 (Audit & continual improvement) | **Manage** (`MG-1`–`MG-4`) | `AML.TA0011`, `AML.T0040`, `AML.T0057` | `CP 8 ↔ CP 9` + `CP 10` (`E.5` playbooks & telemetry) |
