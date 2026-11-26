# Machine-readable Evidence Pack schemas

This folder turns the Chapter 11 **Evidence Pack** pattern into validateable JSON (Draft 2020-12).

| File | Purpose |
|---|---|
| [`evidence-pack.schema.json`](evidence-pack.schema.json) | JSON Schema (Draft 2020-12) for a release Evidence Pack aligned with CycloneDX 1.6/1.7 *themes*, lifecycle control points (`CP 4 / 7 / 8 / 9`), conditional `allOf` constraints per scope (including `Pretraining-Distributed`), `dataProvenance`, `localRunnerConfig`, `trainingClusterConfig`, `conformanceProfile` (`MLS-*`), `runtimeAgentConfig`, and `runtimeTelemetry` |
| [`mlsecops-attestation.v1.schema.json`](mlsecops-attestation.v1.schema.json) | Canonical `https://in-toto.io/Statement/v1` attestation envelope (`ResourceDescriptor` subject matched by digest) wrapping Evidence Pack JSON under `predicateType: "https://mhaghighian.github.io/MLSecOps/attestation/evidence-pack/v1"` |
| [`dsse-envelope.v1.schema.json`](dsse-envelope.v1.schema.json) | Canonical **DSSE** envelope (`payloadType: "application/vnd.in-toto+json"`) compatible with Cosign, **Witness**, and **Archivista** |
| [`evidence-pack.schema.md`](evidence-pack.schema.md) | Full field-by-field contract & validation behavior reference |
| [`examples/evidence-pack.example.json`](examples/evidence-pack.example.json) | `Agentic-MCP` filled example (CycloneDX 1.6, pinned `mcpSchemaHashes`, KV partition, SOC telemetry) |
| [`examples/evidence-pack.managed-api.example.json`](examples/evidence-pack.managed-api.example.json) | `Managed-API` filled example (CycloneDX 1.7, `configSnapshotHash`, RAG `dataProvenance`, backup revocation) |
| [`examples/evidence-pack.pretraining.example.json`](examples/evidence-pack.pretraining.example.json) | `Pretraining-Distributed` filled example (`FSDP`, isolated collective network, worker attestation, checkpoint digest binding, `MLS-*` `conformanceProfile`) |
| [`examples/intoto/evidence-pack.intoto.example.json`](examples/intoto/evidence-pack.intoto.example.json) | Filled `in-toto.io/Statement/v1` attestation wrapping the `Agentic-MCP` Evidence Pack |
| [`examples/intoto/evidence-pack.dsse.example.json`](examples/intoto/evidence-pack.dsse.example.json) | Filled **DSSE** envelope carrying Base64-encoded `in-toto Statement v1` for Witness / Archivista workflows |

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
