# Policy-as-Code samples (OPA / Conftest)

Executable examples implementing controls described in Chapters 3, 4, 5, 6, 7, 8, 10, 12, and 16.

| File | Purpose |
|---|---|
| [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) | Evidence Pack admission policy (`package main`) enforcing blocking gates (`CP4`/`CP7`/`CP8`, quantitative `agentMisalignmentScore <= 0.15` & `redTeamPhasesCompleted >= 4`), `CP8↔CP9` SHA-256 digest binding, CycloneDX component SHA-256 validation & weak-hash denial (`MD5`/`SHA-1`), `aisbom:unreadable`, `dataProvenance` PII & backup revocation, `localRunnerConfig` (`E.1.7`), `runtimeTelemetry.rawPromptLoggingDisabled`, `MCP09` pinning/drift/shadowed names/cleartext/SSRF, OWASP `ASI02`/`ASI03`/`ASI06`/`ASI07`/`ASI08` (`delegationDepthMax <= 4`), capped MCP sampling, and KV cache isolation |
| [`cp8_cp9_admission_test.rego`](cp8_cp9_admission_test.rego) | Non-redundant Rego unit tests covering allow/deny and fail-closed edge cases (`conftest verify`) |
| [`k8s/`](k8s/README.md) | Kubernetes inference workload & `Service` hardening (`package mlsecops.k8s` — digest-pinned `@sha256:` images, `--trust-remote-code` / risky `--allowed-local-media-path`, inline env & CLI secrets, `vLLM` auth, `host*`/`hostPort`/`LoadBalancer`/`NodePort`/`externalIPs`, `restricted` PSS `runAsNonRoot` + `seccompProfile` + non-`Unmasked` `procMount` + `capabilities.drop: ["ALL"]` + `readOnlyRootFilesystem` + `resources.limits.memory` + `automountServiceAccountToken: false`) |
| [`testdata/`](testdata/evidence-pack.fail-digest.json) | Negative Evidence Pack fixtures ([`evidence-pack.fail-digest.json`](testdata/evidence-pack.fail-digest.json), [`evidence-pack.fail-unpinned-mcp.json`](testdata/evidence-pack.fail-unpinned-mcp.json)) |

## Run locally

```bash
# Run all Rego unit tests across policies/ and policies/k8s/
conftest verify --policy policies

# Evaluate Evidence Packs
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies schemas/examples/evidence-pack.managed-api.example.json
conftest test --policy policies policies/testdata/evidence-pack.fail-digest.json
conftest test --policy policies policies/testdata/evidence-pack.fail-unpinned-mcp.json

# Evaluate Kubernetes inference manifests
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-pass.yaml
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-fail.yaml

# Companion static scanner (MCP manifests/pins + header-first Pickle/ZIP/Safetensors/GGUF/ONNX/NumPy checks)
python scripts/ai_security_scan.py --mcp path/to/mcp.json --pins schemas/examples/evidence-pack.example.json --model path/to/weights/
```

> `cp8_cp9_admission.rego` uses Conftest's default `package main` so `conftest test --policy policies ...` evaluates rules without extra namespace flags, while `policies/k8s/` uses `package mlsecops.k8s` so Evidence Pack checks and Kubernetes manifest checks never collide.

Wire the Evidence Pack check into CI before promoting an artifact, pair Kubernetes manifest/cluster admission controls (Kyverno/`policies/k8s/`, OPA Gatekeeper, or Conftest in deploy pipelines) so **CP 9** is a **hard store/deploy gate**, and see [companion scripts README](../scripts/README.md) for rule IDs and CLI options.

These policies are **reference samples**. Tune thresholds and field names to your Evidence Pack producer.
