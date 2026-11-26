# Kubernetes Inference Workload Policy (OPA / Conftest)

Executable Kubernetes admission sample implementing **Chapters 3, 5, 16**, and **Appendix E.7.3** Pod/Deployment controls (`Pod`, `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, `CronJob`).

Uses `package mlsecops.k8s` so Evidence Pack checks (`conftest test --policy policies ...`, which run `package main`) and Kubernetes manifest checks never collide when Conftest loads `policies/` recursively.

## Controls enforced

- **Digest-pinned images (`CP 9`):** deny `:latest` or unpinned tags missing `@sha256:<64-hex>`
- **Supply-chain & secret hygiene (`Ch.5/16`):** reject `--trust-remote-code` / `TRUST_REMOTE_CODE`, and forbid plaintext secrets (`HF_TOKEN`, `VLLM_API_KEY`, `*_API_KEY`, `*_TOKEN`, `*_SECRET`) instead of `valueFrom`
- **Node & host isolation (`Ch.16`):** deny `hostNetwork`, `hostPID`, `hostIPC`, and `hostPath` volume mounts
- **Restricted Pod Security Standards (`Ch.16`):** enforce `runAsNonRoot: true`, `seccompProfile` (`RuntimeDefault`/`Localhost`), `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`, `readOnlyRootFilesystem: true`, and forbid `privileged: true`
- **Compute hijacking & token minimization (`Ch.3/16`):** require `resources.limits.memory` and `automountServiceAccountToken: false`

## Run locally

```bash
conftest verify --policy policies
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-pass.yaml
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-fail.yaml
```

See [Chapter 16 — Kubernetes Deployment Reference](../../chapters-en/16-kubernetes-deployment-reference.md) and [policies README](../README.md).
