# Policy-as-Code samples (OPA / Conftest)

Executable examples for controls described in Chapters 6, 8, 12, and 16.

| File | Purpose |
|------|---------|
| [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) | Enforce blocking gates (`CP4`/`CP7`/`CP8`), bind `CP8↔CP9` SHA-256 digests (`modelArtifact` or `Managed-API` `managedApiConfig`), reject missing `systemScope`/`boundToCp9Digest`/placeholder `signatureMethod`, flag unreadable binaries, block unpinned (`MCP09`)/missing/drifted MCP hashes, require `Agentic-MCP` kill-switch + scoped credentials, and guard cross-model KV reuse |
| [`cp8_cp9_admission_test.rego`](cp8_cp9_admission_test.rego) | Rego unit tests covering allow/deny and fail-closed edge cases (`conftest verify`) |
| [`k8s/`](k8s/README.md) | Kubernetes inference Pod/Deployment hardening (`package mlsecops.k8s` — digest-pinned `@sha256:` images, non-root `restricted` PSS, `allowPrivilegeEscalation: false`, drop `ALL` caps, `automountServiceAccountToken: false`) |
| [`testdata/`](testdata/evidence-pack.fail-digest.json) | Pass/fail Evidence Pack fixtures (`evidence-pack.fail-digest.json`, [`evidence-pack.fail-unpinned-mcp.json`](testdata/evidence-pack.fail-unpinned-mcp.json)) |

**Run locally**

```bash
# Install Conftest (v0.54+ / OPA Rego v1): https://www.conftest.dev/
conftest verify --policy policies
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies schemas/examples/evidence-pack.managed-api.example.json
conftest test --policy policies policies/testdata/evidence-pack.fail-digest.json
conftest test --policy policies policies/testdata/evidence-pack.fail-unpinned-mcp.json
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-pass.yaml
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-fail.yaml
```

> `cp8_cp9_admission.rego` uses Conftest's default `package main` so `conftest test --policy policies ...` evaluates rules without extra namespace flags, while `policies/k8s/` uses `package mlsecops.k8s` so Evidence Pack checks and Kubernetes manifest checks never collide.

Wire the Evidence Pack check into CI before promoting an artifact, and pair Kubernetes manifest/cluster admission controls (Kyverno/`policies/k8s/`, OPA Gatekeeper, or Conftest in deploy pipelines) so CP 9 is a **hard store/deploy gate**, not a post-hoc checklist.

These policies are **reference samples**. Tune thresholds and field names to your Evidence Pack producer.
