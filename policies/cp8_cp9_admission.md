# CP8 ↔ CP9 admission policy (Rego)

Executable Conftest/OPA sample that binds the digest approved at **CP 8** to the artifact verified at **CP 9**, and denies MCP schema drift, unreadable model binaries, missing agent kill-switch, and unsafe cross-model KV reuse.

- Source: [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) (in-repo; clone to run Conftest)
- Fixtures: [`testdata/evidence-pack.fail-digest.json`](testdata/evidence-pack.fail-digest.json)
- Overview: [policies README](README.md)

```bash
conftest test --policy policies schemas/examples/evidence-pack.example.json
```

See [Chapter 6 — binding CP 8 to CP 9](../chapters-en/06-pipeline.md#binding-cp-8-to-cp-9-close-the-toctou-gap).
