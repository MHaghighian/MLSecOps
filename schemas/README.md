# Machine-readable Evidence Pack schemas

This folder turns the Chapter 11 **Evidence Pack** pattern into validateable JSON (Draft 2020-12).

| File | Purpose |
|---|---|
| [`evidence-pack.schema.json`](evidence-pack.schema.json) | JSON Schema (Draft 2020-12) for a release Evidence Pack aligned with CycloneDX 1.6/1.7 *themes*, lifecycle control points (`CP 4 / 7 / 8 / 9`), conditional `allOf` constraints per scope, `dataProvenance`, `localRunnerConfig`, `runtimeAgentConfig`, and `runtimeTelemetry` |
| [`evidence-pack.schema.md`](evidence-pack.schema.md) | Full field-by-field contract & validation behavior reference |
| [`examples/evidence-pack.example.json`](examples/evidence-pack.example.json) | `Agentic-MCP` filled example (CycloneDX 1.6, pinned `mcpSchemaHashes`, KV partition, SOC telemetry) |
| [`examples/evidence-pack.managed-api.example.json`](examples/evidence-pack.managed-api.example.json) | `Managed-API` filled example (CycloneDX 1.7, `configSnapshotHash`, RAG `dataProvenance`, backup revocation) |

## How to use

1. Emit one Evidence Pack JSON per release / CT cycle (registry, CI artifact, or GRC export).
2. Validate structurally against Draft 2020-12 + strict RFC-3339 date-time:

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/evidence-pack.schema.json schemas/examples/evidence-pack.example.json
check-jsonschema --schemafile schemas/evidence-pack.schema.json schemas/examples/evidence-pack.managed-api.example.json
```

3. Enforce semantic admission rules (`CP4` / `CP7` / `CP8↔CP9` / `MCP09`) with Conftest / OPA:

```bash
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies schemas/examples/evidence-pack.managed-api.example.json
```

4. Verify pinned MCP tool hashes and scan for injection/SSRF/secret literals via the zero-dependency scanner ([scripts/README.md](../scripts/README.md)):

```bash
python scripts/ai_security_scan.py --mcp schemas/examples/evidence-pack.example.json --pins schemas/examples/evidence-pack.example.json --fail-on HIGH
```

See also: [Chapter 11 — Machine-readable Evidence Pack](../chapters-en/11-governance-evidence.md#machine-readable-evidence-pack), [Appendix E.4](../chapters-en/17-appendix-e-implementation-reference.md#e4-evidence-pack-template), [`policies/`](../policies/README.md).

The schema is **community implementation guidance**, not an ISO/OWASP mandatory file format. Organizations may extend optional fields (`additionalProperties: true`); production Level 2+ should keep `lifecycleControlGates` (`CP 4/7/8`), scope-appropriate digest binding (`modelArtifact` or `managedApiConfig`), and `cryptographicProvenance` (`CP 9`).
