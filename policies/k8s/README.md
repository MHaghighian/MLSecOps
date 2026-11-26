# Kubernetes Inference Workload Policy (OPA / Conftest)

Executable Kubernetes admission sample implementing **Chapters 3, 5, 16**, and **Appendix E.7.3** controls across `Pod`, `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, `CronJob`, and `Service`.

Uses `package mlsecops.k8s` so Evidence Pack checks (`conftest test --policy policies ...`, which run `package main`) and Kubernetes manifest checks never collide when Conftest loads `policies/` recursively.

- Policy: [`inference_workload.rego`](inference_workload.rego) · Unit tests: [`inference_workload_test.rego`](inference_workload_test.rego)
- Fixtures: [`testdata/inference-pass.yaml`](testdata/inference-pass.yaml) · [`testdata/inference-fail.yaml`](testdata/inference-fail.yaml)

## Controls enforced

| Area | Rules enforced (`deny`) |
|---|---|
| **Immutable images (`CP 9`)** | All `containers` and `initContainers` must pin images with `@sha256:<64-hex>` (rejects `:latest` and mutable tags) |
| **Model load & secret hygiene (`Ch.5/16`)** | Forbid `--trust-remote-code` CLI flags and `TRUST_REMOTE_CODE`/`HF_HUB_TRUST_REMOTE_CODE` env vars; reject root/system `--allowed-local-media-path` (`/`, `/etc`, `/root`, `/var`, `/home`) LFI vectors; block inline env secrets (`HF_TOKEN`, `VLLM_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `AWS_SECRET_ACCESS_KEY`, `*_TOKEN`/`*_SECRET`/`*_API_KEY`/`*_PASSWORD`) and hardcoded CLI token literals (`sk-`, `hf_`, `ghp_`, `glpat-`, `xox*-`, `AKIA`/`ASIA`) |
| **Inference auth & exposure (`Ch.16`)** | Require non-empty `VLLM_API_KEY` (via `valueFrom` or non-empty value) or `--api-key` on `vllm` containers; deny `hostNetwork`, `hostPID`, `hostIPC`, `hostPath` volumes, `ports[].hostPort`, and `Service` `LoadBalancer`/`NodePort` or `spec.externalIPs` (`CVE-2020-8554`) |
| **Restricted Pod Security Standards** | Deny `privileged: true` and `procMount: Unmasked`; enforce `allowPrivilegeEscalation: false`, Pod+container non-root `runAsNonRoot: true` / UID `!= 0` (blocking container overrides and inherited Pod `runAsUser: 0`), `seccompProfile` `RuntimeDefault`/`Localhost`, `capabilities.drop: ["ALL"]` (no extra caps added except optional `NET_BIND_SERVICE`), and `readOnlyRootFilesystem: true` |
| **Compute & SA token limits (`Ch.3/16`)** | Require `resources.limits.memory` on inference containers and `automountServiceAccountToken: false` |

## Run locally

```bash
conftest verify --policy policies
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-pass.yaml
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-fail.yaml
```

See [Chapter 16 — Kubernetes Deployment Reference](../../chapters-en/16-kubernetes-deployment-reference.md) and [policies README](../README.md).
