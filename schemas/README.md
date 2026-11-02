# Machine-readable Evidence Pack schemas

This folder turns the Chapter 11 **Evidence Pack** pattern into validateable JSON.

| File | Purpose |
|------|---------|
| [`evidence-pack.schema.json`](evidence-pack.schema.json) | JSON Schema (Draft 2020-12) for a release Evidence Pack aligned with CycloneDX 1.6 *themes* and the ten lifecycle control points |
| [`examples/evidence-pack.example.json`](examples/evidence-pack.example.json) | Minimal filled example for tooling tests |

**How to use**

1. Emit one Evidence Pack JSON per release / CT cycle (registry, CI artifact, or GRC export).
2. Validate in CI, for example:

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/evidence-pack.schema.json path/to/evidence-pack.json
```

3. Enforce release/admission policy with Conftest / OPA against the same JSON:

```bash
conftest test --policy policies path/to/evidence-pack.json
```

See also: [Chapter 11](../chapters-en/11-governance-evidence.md#machine-readable-evidence-pack), [Appendix E.4](../chapters-en/17-appendix-e-implementation-reference.md#e4-evidence-pack-template), [`policies/`](../policies/README.md).

The schema is **community implementation guidance**, not an ISO/OWASP mandatory file format. Organizations may subset fields; production Level 2+ should keep `lifecycleControlGates` and `cryptographicProvenance` for CP 4/7/8/9.
