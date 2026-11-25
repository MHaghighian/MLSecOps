# Kubernetes Inference Workload Policy (OPA / Conftest)

Executable Kubernetes admission sample implementing **Chapter 16** and **Appendix E.7.3** Pod/Deployment controls (`Pod`, `Deployment`, `StatefulSet`, `DaemonSet`, `Job`, `CronJob`).

Uses `package mlsecops.k8s` so Evidence Pack checks (`conftest test --policy policies ...`, which run `package main`) and Kubernetes manifest checks never collide when Conftest loads `policies/` recursively.

## Controls enforced

- **Digest-pinned images (`CP 9`):** deny `:latest` or unpinned tags missing `@sha256:<64-hex>`
- **Non-root (`restricted` PSS):** enforce `securityContext.runAsNonRoot: true`
- **Least privilege:** deny `privileged: true`, require `allowPrivilegeEscalation: false`, require `capabilities.drop: ["ALL"]`
- **Token minimization:** require `automountServiceAccountToken: false`

## Run locally

```bash
conftest verify --policy policies
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-pass.yaml
conftest test --policy policies/k8s --namespace mlsecops.k8s policies/k8s/testdata/inference-fail.yaml
```

See [Chapter 16 — Kubernetes Deployment Reference](../../chapters-en/16-kubernetes-deployment-reference.md) and [policies README](../README.md).
