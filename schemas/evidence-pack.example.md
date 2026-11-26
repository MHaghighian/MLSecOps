# Evidence Pack example instances

Filled Evidence Pack instances verified continuously by `check-jsonschema`, `scripts/verify_repo.py`, `conftest test`, and `scripts/ai_security_scan.py`:

| Instance | Scope / Format | Key controls demonstrated |
|---|---|---|
| [`examples/evidence-pack.example.json`](examples/evidence-pack.example.json) | `Agentic-MCP` (CycloneDX `1.6`) | `CP4`/`CP7` (`8` red-team phases, `0.02` misalignment)/`CP8↔CP9` matching `sha256:aaaa...`, `ML` component hash alignment, `tenantKvPartitioned: true`, `killSwitchEnabled`, `scopedCredentialsRequired`, `intentGateEnabled`, `memoryProvenanceVerified`, `delegationDepthMax: 2`, pinned `payments-mcp` `tools/list` SHA-256 over HTTPS, and `rawPromptLoggingDisabled: true` |
| [`examples/evidence-pack.managed-api.example.json`](examples/evidence-pack.managed-api.example.json) | `Managed-API` (CycloneDX `1.7`) | Binds `CP8` `boundToCp9Digest` to `managedApiConfig.configSnapshotHash` (`sha256:cccc...`), includes Ch.4/Ch.7 `dataProvenance` (`piiScanResult: "PASS"`, `vectorIndexVersionHash`, `backupRevocationVerified: true`), `signatureMethod: "managed-config-snapshot"`, and SOC telemetry |

- Schema definition & rules: [evidence-pack.schema.md](evidence-pack.schema.md) · [schemas README](README.md)
- Admission failures (negative fixtures for Conftest): [`policies/testdata/`](../policies/testdata/evidence-pack.fail-digest.json)

```bash
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies schemas/examples/evidence-pack.managed-api.example.json
python scripts/ai_security_scan.py --mcp schemas/examples/evidence-pack.example.json --pins schemas/examples/evidence-pack.example.json
```
