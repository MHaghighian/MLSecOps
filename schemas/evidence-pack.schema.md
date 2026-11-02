# Evidence Pack JSON Schema

Machine-readable Evidence Pack schema aligned with CycloneDX 1.6 themes and MLSecOps control points **4 / 7 / 8 / 9**.

- Schema file: [`evidence-pack.schema.json`](evidence-pack.schema.json)
- Example instance: [`examples/evidence-pack.example.json`](examples/evidence-pack.example.json) · [example notes](evidence-pack.example.md)
- Overview: [schemas README](README.md)

```bash
pip install check-jsonschema
check-jsonschema --schemafile schemas/evidence-pack.schema.json path/to/evidence-pack.json
```

See [Chapter 11 — Machine-readable Evidence Pack](../chapters-en/11-governance-evidence.md#machine-readable-evidence-pack).
