# CP8 ↔ CP9 admission policy (Rego)

Executable Conftest/OPA sample (`package main` for Conftest default evaluation) that binds the digest approved at **CP 8** to the artifact (or `Managed-API` config snapshot) verified at **CP 9**, and fails closed on missing `systemScope`/`boundToCp9Digest`, missing digests, unpinned MCP servers (`MCP09`), missing/drifted MCP schema hashes, unreadable model binaries, missing agent kill-switch/scoped credentials, and unsafe cross-model KV reuse.

- Source: [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) · Unit tests: [`cp8_cp9_admission_test.rego`](cp8_cp9_admission_test.rego) (clone repo to run Conftest)
- Fixtures: [`testdata/evidence-pack.fail-digest.json`](testdata/evidence-pack.fail-digest.json) · [`testdata/evidence-pack.fail-unpinned-mcp.json`](testdata/evidence-pack.fail-unpinned-mcp.json)
- Overview: [policies README](README.md)

```bash
conftest verify --policy policies
conftest test --policy policies schemas/examples/evidence-pack.example.json
```

See [Chapter 6 — binding CP 8 to CP 9](../chapters-en/06-pipeline.md#binding-cp-8-to-cp-9-close-the-toctou-gap).
