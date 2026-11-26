# Evidence Pack JSON Schema

Machine-readable JSON Schema ([Draft 2020-12](evidence-pack.schema.json)) aligned with CycloneDX 1.6/1.7 themes and MLSecOps control points **4 / 7 / 8 / 9**.

- Schema files: [`evidence-pack.schema.json`](evidence-pack.schema.json) · [`mlsecops-attestation.v1.schema.json`](mlsecops-attestation.v1.schema.json) (`in-toto` v1 Statement) · [`dsse-envelope.v1.schema.json`](dsse-envelope.v1.schema.json) (DSSE Envelope)
- Filled examples: [examples guide](evidence-pack.example.md) (`Agentic-MCP` + `Managed-API` + `Pretraining-Distributed` + `in-toto` v1 + `DSSE`)
- Conformance & provenance guides: [Standards Alignment & `MLS-*` Profile](../references/STANDARDS-ALIGNMENT.md) · [in-toto, Witness & Archivista](../references/INTOTO-WITNESS-ARCHIVISTA.md)
- Overview: [schemas README](README.md) · Admission policy: [`policies/cp8_cp9_admission`](../policies/cp8_cp9_admission.md)

## Top-level structure & field contract

| Object / Field | Required | Key constraints |
|---|---|---|
| `bomFormat` / `specVersion` / `version` | Yes | `"CycloneDX"`, `"1.6"` or `"1.7"`, integer `>= 1` |
| `metadata` | Yes | Strictly formatted RFC-3339 `timestamp` (`date-time` + `pattern`), `systemScope` enum (`Classical-ML`, `LLM-RAG`, `Agentic-MCP`, `Multimodal-Edge`, `Managed-API`, `Pretraining-Distributed`), `sharedResponsibilityRecord` (`modelOwner`, `platformOwner`, `socOwner`) |
| `lifecycleControlGates` | Yes | `cp4_dataAndRagAclGate.status` (`PASS`/`BLOCK`), `cp7_adversarialAndRedTeamGate` (`status`, `unreadableArtifactsDetected`, `redTeamPhasesCompleted` `0..8`, `agentMisalignmentScore` `0..1`), `cp8_releaseDecisionGate` (`decision`: `APPROVED`/`REJECTED`, `approverRole`, `boundToCp9Digest`: `sha256:<64-hex>`) |
| `cryptographicProvenance` | Yes | `cp9_checkpointVerified` (`boolean`), `signatureMethod` (`minLength: 1`), optional `teeAttestationProvider`, optional `mcpSchemaHashes` (`serverName -> 64-hex SHA-256`) |
| `conformanceProfile` | Optional | `profileVersion`, `targetLevel` (`1` / `2` / `3`), `controlIds[]` matching `^MLS-(?:CP\|SC\|DT\|AG\|RT\|TR)-[0-9]{2}$` |
| `components` | Optional | BOM array (`name`, `type`, `hashes[]`, `properties[]` such as `aisbom:unreadable`) |
| `modelArtifact` | Conditional | Required unless `systemScope == "Managed-API"`; `sha256Digest` (`sha256:<64-hex>`) |
| `managedApiConfig` | Conditional | Required when `systemScope == "Managed-API"`; `configSnapshotHash` (`sha256:<64-hex>`), `provider`, `deploymentId`, `region`, `apiVersion` |
| `dataProvenance` | Optional | `datasetVersion`, `lineageUri`, `piiScanResult` (`PASS`/`FAIL`), `vectorIndexVersionHash`, `backupRevocationVerified` |
| `localRunnerConfig` | Optional | Appendix `E.1.7` fields (`modelOciDigest`, `modelRegistry`, `engineVersion`, `tcpHostExposed`, `networkIsolated`) |
| `trainingClusterConfig` | Conditional | Required when `systemScope == "Pretraining-Distributed"` (`E.1.8`); `topology` (`DDP`/`FSDP`/`Zero-3`/`RLHF-PPO`/`DPO`/`Hybrid`), `collectiveNetworkIsolated`, `workerAttestationVerified`, `checkpointSignedAndDigestBound`, `preferenceDataProvenanceVerified`, `gradientClippingActive`, `intermediateStageValidated`, `dpTrainingApplied` |
| `inferenceConfig` | Optional | `crossModelKvCacheReuse`, `kvAlignmentControlActive`, `tenantKvPartitioned` |
| `runtimeAgentConfig` | Conditional | Required when `systemScope == "Agentic-MCP"` (requires `killSwitchEnabled`, `scopedCredentialsRequired`); also types `intentGateEnabled`, `memoryStoreEnabled`, `memoryProvenanceVerified`, `delegationDepthMax` (`0..10`), `samplingEnabled`, `samplingBudgetCapped`, and `mcpTools[]` (`serverName`, `transport`, `endpoint`, `currentSchemaHash`) |
| `runtimeTelemetry` | Optional | `siemFeedActive`, `rawPromptLoggingDisabled` |

## Conditional `allOf` & negative QA guarantees

1. **Managed-API scope:** requires `managedApiConfig.configSnapshotHash`; `modelArtifact` is not required.
2. **All non-managed scopes (`Classical-ML`, `LLM-RAG`, `Agentic-MCP`, `Multimodal-Edge`, `Pretraining-Distributed`):** require `modelArtifact.sha256Digest`.
3. **Agentic-MCP scope:** requires `runtimeAgentConfig` with `killSwitchEnabled` and `scopedCredentialsRequired`.
4. **Pretraining-Distributed scope:** requires `trainingClusterConfig` (`topology`, `collectiveNetworkIsolated`, `workerAttestationVerified`, `checkpointSignedAndDigestBound`, `preferenceDataProvenanceVerified`).
5. **`in-toto` v1 envelope (`mlsecops-attestation.v1.schema.json`):** validates `_type == "https://in-toto.io/Statement/v1"` and `predicate` against `evidence-pack.schema.json` via local `referencing.Registry`.
6. **Strict timestamp validation:** `scripts/verify_repo.py` tests structural pattern failures **and** out-of-range calendar dates (e.g. `2026-99-99T00:00:00Z`) via `@checker.checks("date-time", raises=ValueError)`.

## Validate

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/evidence-pack.schema.json path/to/evidence-pack.json
python scripts/verify_repo.py
```

See [Chapter 11 — Machine-readable Evidence Pack](../chapters-en/11-governance-evidence.md#machine-readable-evidence-pack) and [Appendix E.4](../chapters-en/17-appendix-e-implementation-reference.md#e4-evidence-pack-template).
