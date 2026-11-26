# Policy-as-Code samples (OPA / Conftest)

Executable examples for controls described in Chapters 4, 5, 6, 7, 8, 10, 12, and 16.

| File | Purpose |
|------|---------|
| [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) | Enforce blocking gates (`CP4`/`CP7`/`CP8` + quantitative `agentMisalignmentScore`/`redTeamPhasesCompleted`), bind `CP8↔CP9` SHA-256 digests (`modelArtifact` or `Managed-API` `managedApiConfig`), cross-check CycloneDX ML `components` SHA-256 format & reject weak hashes (`MD5`/`SHA-1`), guard `dataProvenance` PII & backup revocation, flag unisolated `localRunnerConfig` (`E.1.7`), enforce `runtimeTelemetry.rawPromptLoggingDisabled`, block unpinned (`MCP09`)/shadowed/cleartext-endpoint/SSRF/drifted MCP configs, require `Agentic-MCP` kill-switch, scoped credentials, Intent Gate (`ASI02`/`ASI03`), memory provenance (`ASI06`), delegation depth bound (`ASI07`/`ASI08`), and capped MCP sampling, plus KV reuse isolation |
| [`cp8_cp9_admission_test.rego`](cp8_cp9_admission_test.rego) | Non-redundant Rego unit tests covering allow/deny and fail-closed edge cases (`conftest verify`) |
| [`k8s/`](k8s/README.md) | Kubernetes inference Pod/Deployment/Service hardening (`package mlsecops.k8s` — digest-pinned `@sha256:` images, disallow `--trust-remote-code`, risky `--allowed-local-media-path`, & plaintext secrets, require `vLLM` auth, block `hostNetwork`/`hostPID`/`hostIPC`/`hostPort`/`hostPath` & `LoadBalancer`/`NodePort`/`externalIPs`, enforce `restricted` PSS `runAsNonRoot` + `seccompProfile` + non-`Unmasked` `procMount` + `readOnlyRootFilesystem` + drop `ALL` caps + `resources.limits.memory` + `automountServiceAccountToken: false`) |
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

# Optional static scan for MCP manifests (Unicode/Bidi, tool poisoning, Shadow MCP, canonical pins) & model headers:
python scripts/ai_security_scan.py --mcp path/to/mcp.json --model path/to/weights/
```

> `cp8_cp9_admission.rego` uses Conftest's default `package main` so `conftest test --policy policies ...` evaluates rules without extra namespace flags, while `policies/k8s/` uses `package mlsecops.k8s` so Evidence Pack checks and Kubernetes manifest checks never collide.

Wire the Evidence Pack check into CI before promoting an artifact, and pair Kubernetes manifest/cluster admission controls (Kyverno/`policies/k8s/`, OPA Gatekeeper, or Conftest in deploy pipelines) so CP 9 is a **hard store/deploy gate**, not a post-hoc checklist.

These policies are **reference samples**. Tune thresholds and field names to your Evidence Pack producer.
