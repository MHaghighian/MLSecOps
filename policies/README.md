# Policy-as-Code samples (OPA / Conftest)

Executable examples for controls described in Chapters 6, 8, 12, and 16.

| File | Purpose |
|------|---------|
| [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) | Deny release/deploy when `systemScope` or `boundToCp9Digest` is missing, CP8↔CP9 digest drifts or is missing (`modelArtifact` or `Managed-API` `managedApiConfig`), unreadable model binaries are flagged, MCP servers are unpinned (`MCP09`), missing `currentSchemaHash`, or drifted, agent kill-switch or scoped credentials are missing (`Agentic-MCP`), or unsafe cross-model KV reuse is enabled |
| [`cp8_cp9_admission_test.rego`](cp8_cp9_admission_test.rego) | Rego unit tests covering allow/deny and fail-closed edge cases (`conftest verify`) |
| [`testdata/`](testdata/evidence-pack.fail-digest.json) | Pass/fail Evidence Pack fixtures (`evidence-pack.fail-digest.json`, [`evidence-pack.fail-unpinned-mcp.json`](testdata/evidence-pack.fail-unpinned-mcp.json)) |

**Run locally**

```bash
# Install Conftest (v0.54+ / OPA Rego v1): https://www.conftest.dev/
conftest verify --policy policies
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies policies/testdata/evidence-pack.fail-digest.json
conftest test --policy policies policies/testdata/evidence-pack.fail-unpinned-mcp.json
```

> `cp8_cp9_admission.rego` uses Conftest's default `package main` so `conftest test --policy policies ...` evaluates rules without extra namespace flags. If you rename `package main` in a multi-bundle OPA deployment, pass `--namespace <pkg>` or `--all-namespaces` so Conftest does not silently skip rules (`0 tests`).

Wire the same check into CI before promoting an artifact, and again at **Kubernetes admission** (Kyverno/Gatekeeper calling OPA, or Conftest in the deploy pipeline) so CP 9 is a **hard store/deploy gate**, not a post-hoc checklist.

These policies are **reference samples**. Tune thresholds and field names to your Evidence Pack producer.
