# CP8 ↔ CP9 admission policy (`cp8_cp9_admission.rego`)

Executable Conftest/OPA sample (`package main` for Conftest default evaluation) implementing the Chapter 4–16 release and admission controls in Rego v1.

- Source: [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) · Unit tests: [`cp8_cp9_admission_test.rego`](cp8_cp9_admission_test.rego)
- Negative fixtures: [`testdata/evidence-pack.fail-digest.json`](testdata/evidence-pack.fail-digest.json) · [`testdata/evidence-pack.fail-unpinned-mcp.json`](testdata/evidence-pack.fail-unpinned-mcp.json)
- Overview: [policies README](README.md) · Kubernetes companion: [`policies/k8s/`](k8s/README.md)

## Rules enforced (fail closed)

| Control / Chapter | Condition blocked (`deny`) |
|---|---|
| **Metadata / Ownership** | Missing/empty `metadata.systemScope` or `sharedResponsibilityRecord` owners (`modelOwner`, `platformOwner`, `socOwner`) |
| **CP4 / Data & RAG ACL** | `cp4_dataAndRagAclGate.status != "PASS"`, `dataProvenance.piiScanResult == "FAIL"`, or `vectorIndexVersionHash` present with `backupRevocationVerified == false` |
| **CP7 / Validation & Alignment** | `cp7_adversarialAndRedTeamGate.status != "PASS"`, `agentMisalignmentScore > 0.15`, `redTeamPhasesCompleted < 4` (for `LLM-RAG`/`Agentic-MCP`), or `unreadableArtifactsDetected == true` |
| **CP8 ↔ CP9 Digest Bind** | `decision != "APPROVED"`, missing/malformed `boundToCp9Digest` (`sha256:<64-hex>`), digest mismatch against `modelArtifact.sha256Digest` (non-managed) or `managedApiConfig.configSnapshotHash` (`Managed-API`), missing `cp9_checkpointVerified`, or placeholder `signatureMethod` (`none`, `n/a`, `na`, `null`, `tbd`) |
| **CycloneDX Components (Ch.5)** | `aisbom:unreadable == "true"` (case-insensitive), `MD5`/`SHA-1` hashes, malformed `SHA-256` component hashes, or `machine-learning-model` component SHA-256 list missing `modelArtifact.sha256Digest` (supports multi-model BOMs) |
| **Local Runner (`E.1.7`) & Telemetry** | `localRunnerConfig.tcpHostExposed == true` without `networkIsolated == true`, or `runtimeTelemetry.rawPromptLoggingDisabled == false` |
| **MCP Security & Shadowing (`MCP09`)** | Server absent from `mcpSchemaHashes`, malformed 64-hex pins/`currentSchemaHash`, schema hash drift (`MCP` rug pull), duplicate or case/whitespace-conflicting `serverName`, cleartext `http`/`ws` transport or spoofed `http://`/`ws://` remote endpoints (excluding `localhost`/`127.0.0.1`/`[::1]`), and cloud metadata SSRF (`169.254.x.x`, `100.100.100.200`, `metadata.google.internal`, `metadata.azure.internal`, `fd00:ec2::254`, `::ffff:169.254.`, `0.0.0.0`) |
| **Agentic Controls (`ASI02`/`03`/`06`/`07`/`08`) & KV** | Missing `killSwitchEnabled`, `scopedCredentialsRequired`, or `intentGateEnabled` under `Agentic-MCP`; persistent memory without `memoryProvenanceVerified`; `delegationDepthMax > 4`; `samplingEnabled` without `samplingBudgetCapped`; or `crossModelKvCacheReuse` without alignment control / tenant KV partitioning |

## Run locally

```bash
conftest verify --policy policies
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies schemas/examples/evidence-pack.managed-api.example.json
conftest test --policy policies policies/testdata/evidence-pack.fail-digest.json
```

See [Chapter 6 — binding CP 8 to CP 9](../chapters-en/06-pipeline.md#binding-cp-8-to-cp-9-close-the-toctou-gap) and [Chapter 8 — Agentic AI Security](../chapters-en/08-agentic-ai-security.md).
