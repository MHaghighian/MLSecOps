# Machine-readable Evidence Pack schemas

This folder turns the Chapter 11 **Evidence Pack** pattern into validateable JSON.

| File | Purpose |
|------|---------|
| [`evidence-pack.schema.json`](evidence-pack.schema.json) | JSON Schema (Draft 2020-12) for a release Evidence Pack aligned with CycloneDX 1.6/1.7 *themes*, lifecycle control points (`CP 4 / 7 / 8 / 9`), conditional `Managed-API`/`Agentic-MCP` constraints, `dataProvenance` (Ch.4/Ch.7), `localRunnerConfig` (`E.1.7`), and `runtimeTelemetry` (Ch.10) |
| [`examples/evidence-pack.example.json`](examples/evidence-pack.example.json) | `Agentic-MCP` filled example (CycloneDX 1.6) |
| [`examples/evidence-pack.managed-api.example.json`](examples/evidence-pack.managed-api.example.json) | `Managed-API` filled example (CycloneDX 1.7) |

**How to use**

1. Emit one Evidence Pack JSON per release / CT cycle (registry, CI artifact, or GRC export).
2. Validate in CI, for example:

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/evidence-pack.schema.json schemas/examples/evidence-pack.example.json
check-jsonschema --schemafile schemas/evidence-pack.schema.json schemas/examples/evidence-pack.managed-api.example.json
```

3. Enforce release/admission policy with Conftest / OPA against the same JSON:

```bash
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies schemas/examples/evidence-pack.managed-api.example.json
```

See also: [Chapter 11](../chapters-en/11-governance-evidence.md#machine-readable-evidence-pack), [Appendix E.4](../chapters-en/17-appendix-e-implementation-reference.md#e4-evidence-pack-template), [`policies/`](../policies/README.md).

The schema is **community implementation guidance**, not an ISO/OWASP mandatory file format. Organizations may extend optional fields (`additionalProperties: true`); production Level 2+ should keep `lifecycleControlGates` (`CP 4/7/8`), scope-appropriate digest binding (`modelArtifact` or `managedApiConfig`), and `cryptographicProvenance` (`CP 9`).
