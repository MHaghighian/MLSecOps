# Chapter 16: Kubernetes Deployment Reference

## Purpose

This chapter provides **operational reference patterns** for deploying and hardening ML/LLM inference on Kubernetes. It complements the multi-tenant controls in [Chapter 7](07-llm-rag-security.md) and the lifecycle decision points in [Chapter 6](06-pipeline.md) with concrete cluster-level controls.

> **Scope:** Cloud-native enterprise inference (vLLM, KServe, Triton, Ray Serve, custom gateways). Edge/IoT and confidential-GPU (TEE) patterns remain out of scope — see vendor docs and specialized frameworks.

> **No bundled artifacts:** This guide ships **markdown content only** (no `examples/` folder, no Kubernetes YAML, no CI/CD pipeline templates, no JSON schemas). Patterns below are architectural guidance. Implement and **test** IaC in your environment using maintained upstream references (vLLM production-stack, Kyverno policy samples, KServe docs).

> *Refs - Frameworks: Kubernetes Pod Security Standards; CNCF security TAG guidance; OWASP LLM Top 10: deployment and supply-chain themes (`LLM03`, `LLM05`). This guide: [Multi-tenant RAG](07-llm-rag-security.md#multi-tenant-rag) (Chapter 7); [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6). Author note: Namespace layout and Kyverno policy names are illustrative patterns - validate against your cluster baseline.*

## Reference architecture

![](../assets/diagrams/16-kubernetes-deployment-reference_01.png)

*Figure - Layered reference architecture for ML/LLM inference on Kubernetes, mapping edge, namespace, admission, network, workload, runtime, and supply-chain layers to their security objectives and controls.*

| Layer | Security objective | Example control |
|---|---|---|
| Edge | AuthN, rate limit, prompt policy | AI Gateway (Ch.7) |
| Namespace | Blast-radius isolation | Separate `ai-inference`, `ai-gateway`, `ai-training` |
| Admission | Unsigned image block | Kyverno `verifyImages` / `ImageValidatingPolicy` |
| Network | Lateral movement reduction | Default-deny + explicit egress allowlist |
| Workload | Least privilege | Restricted PSA, non-root, dropped caps, GPU node pools |
| Runtime | Attack detection | Falco/Tetragon rules for GPU abuse, cryptomining |
| Supply chain | Model integrity | Cosign verify at deploy + digest-pinned images |

> *Refs - Frameworks: Kubernetes Pod Security Standards; CNCF security TAG - layered defense model. This guide: [Purpose](#purpose) (this chapter); [Multi-tenant RAG](07-llm-rag-security.md#multi-tenant-rag) (Chapter 7).*

## Prerequisites

| Requirement | Notes |
|---|---|
| Kubernetes 1.25+ | NetworkPolicy support required |
| CNI with policy enforcement | Calico, Cilium, or equivalent |
| Policy engine | Kyverno or OPA Gatekeeper |
| Signed images | Cosign/Sigstore keys configured in cluster |
| GPU operator (if applicable) | NVIDIA GPU Operator or cloud-managed GPU nodes |

> *Refs - Frameworks: [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) (1.25+ baseline). This guide: [Reference architecture](#reference-architecture) (this chapter). Author note: Version and CNI requirements are minimum bars - validate against your platform team's cluster standard.*

## Namespace isolation and RBAC

Treat **training**, **inference**, **gateway**, and **observability** as separate trust zones. Production inference namespaces should:

- Use Pod Security Admission `restricted` (or your org equivalent).
- Run workloads under dedicated ServiceAccounts with **no** cluster-admin bindings.
- Deny `automountServiceAccountToken` unless a sidecar truly needs API access.
- Separate **staging** and **production** namespaces with different registry paths and signing keys.

**Upstream references:** [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/), [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/).

| Anti-pattern | Correct alternative |
|---|---|
| Single `default` namespace for ML workloads | Dedicated namespaces per lifecycle stage |
| Inference SA with secret write access | Read-only SA; secrets via External Secrets Operator |
| Shared cluster-admin for data scientists | Namespace-scoped RBAC + break-glass audit |

> *Refs - Frameworks: [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/); [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/). This guide: [Cloud Native and Multi-Tenant deployment](07-llm-rag-security.md#cloud-native-and-multi-tenant-deployment) (Chapter 7).*

## Network policy — default deny

AI inference pods should not have unrestricted egress. Agentic workloads especially may call unpredictable external APIs at runtime; **visibility + allowlist** beats pretending you can predict every destination at deploy time ([Application Security Standards playbook on AI egress](https://appsecuritystandards.org/blog/ai-workloads-in-kubernetes-a-security-implementation-playbook)).

Recommended pattern:

1. **Default-deny** all ingress and egress in the inference namespace.
2. Allow ingress **only** from the AI gateway namespace/pod label.
3. Allow egress explicitly to: DNS, internal vector DB, observability collector, and approved external APIs (via egress gateway if possible).
4. Log outbound requests at the gateway or egress proxy for SOC correlation (Ch.10).

**Upstream references:** [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/), [Cilium network policy guide](https://docs.cilium.io/en/stable/security/policy/).

For service mesh deployments, complement NetworkPolicy with **Istio/Linkerd authorization policies** (mTLS + L7 rules) as described in Ch.7 multi-tenant table.

> *Refs - Frameworks: [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/); [Cilium network policy guide](https://docs.cilium.io/en/stable/security/policy/); [Application Security Standards - AI egress playbook](https://appsecuritystandards.org/blog/ai-workloads-in-kubernetes-a-security-implementation-playbook). This guide: [Advanced Multi-Tenant hardening](07-llm-rag-security.md#advanced-multi-tenant-hardening) (Chapter 7); [SOC integration](10-monitoring-soc-ir.md#soc-integration) (Chapter 10).*

## Admission control — verify signed images

Unsigned or tampered container/model images must not schedule in production inference namespaces. Align this control with **control point 9 (Integrity and Provenance)** and registry promotion policy (Ch.5).

Kyverno can enforce cosign signatures at admission. OWASP/OpenSSF supply-chain practice maps to:

- **Signature verify** — image signed with org key or keyless GitHub OIDC
- **Optional attestations** — SLSA provenance, SBOM (CycloneDX), custom model-provenance type

**Upstream references:** [Kyverno verifyImages (Sigstore/Cosign)](https://kyverno.io/docs/policy-types/cluster-policy/verify-images/sigstore/), [Kyverno policy library — verify-image](https://artifacthub.io/packages/kyverno/kyverno-policies/verify-image).

For Kyverno 1.18+, consider migrating to [`ImageValidatingPolicy`](https://kyverno.io/docs/policy-types/image-validating-policy/) for clearer audit reports and named verification stages (signature → attestation → digest mutation).

**Admission behavior:** Pod create → verify fail → **Deny**. Record denial events in Evidence Pack `policy` section.

> *Refs - Frameworks: [Kyverno verifyImages (Sigstore/Cosign)](https://kyverno.io/docs/policy-types/cluster-policy/verify-images/sigstore/); [Kyverno ImageValidatingPolicy](https://kyverno.io/docs/policy-types/image-validating-policy/); OpenSSF SLSA / Sigstore supply-chain practice. This guide: [Provenance and signing](05-model-artifact-supply-chain.md#provenance-and-signing) (Chapter 5); [Lifecycle control point 9](06-pipeline.md#lifecycle-control-points) (Chapter 6).*

## vLLM on Kubernetes — secure deployment pattern

The [vLLM production-stack](https://github.com/vllm-project/production-stack) project documents Helm-based deployment with API key protection:

| Control | Implementation |
|---|---|
| API authentication | `vllmApiKey` in Helm values → `VLLM_API_KEY` env; router validates Bearer tokens |
| Multi-tenant keys | Comma-separated key list supported natively by vLLM; production-stack router enforces allowlist ([PR #937](https://github.com/vllm-project/production-stack/pull/937)) |
| HF model access | `HF_TOKEN` from Kubernetes Secret, not plain values in git |
| Health checks | `/health` endpoint for liveness/readiness |

Reference tutorial: `production-stack/tutorials/11-secure-vllm-serve.md`

```yaml
# Minimal pattern (adapt from production-stack values-11-secure-vllm.yaml)
servingEngineSpec:
  vllmApiKey:
    secretName: inference-api-key
    secretKey: VLLM_API_KEY
  modelSpec:
    - name: llama3
      repository: vllm/vllm-openai
      tag: latest   # Prefer digest pin in production: image@sha256:...
      modelURL: meta-llama/Llama-3.1-8B-Instruct
      requestGPU: 1
```

**MLSecOps checklist for vLLM:**

- [ ] Image digest-pinned and cosign-verified before deploy
- [ ] `VLLM_API_KEY` per tenant or per environment (not shared prod/staging)
- [ ] No public LoadBalancer without gateway/WAF in front
- [ ] GPU memory sanitization considered after CVE-class issues (see LeftoverLocals, Ch.13)
- [ ] Router + engine NetworkPolicy restricts who can reach port 8000

**Upstream reference:** [vLLM production-stack — secure vLLM serve tutorial](https://github.com/vllm-project/production-stack/blob/main/tutorials/11-secure-vllm-serve.md) and Helm values in that tutorial — adapt and test in your cluster.

> *Refs - Frameworks: [vLLM production-stack](https://github.com/vllm-project/production-stack); [PR #937 - multi-tenant API keys](https://github.com/vllm-project/production-stack/pull/937). This guide: [LeftoverLocals case study](13-case-studies.md#leftoverlocals-cve-2023-4969--documented-incident) (Chapter 13); [GPU isolation](#gpu-isolation-and-shared-inference) (this chapter). Author note: Helm snippet is illustrative - pin image digests and test in non-production before promotion.*

## KServe and generic model serving

[KServe](https://github.com/kserve/kserve) is a common Kubernetes model-serving layer. MLSecOps controls apply regardless of framework:

| Control | KServe / generic application |
|---|---|
| AuthN/Z | Istio/Knative authorization, OAuth2 proxy, or external AI gateway |
| Model storage | Signed OCI artifacts or signed PVC snapshots; verify before `Predictor` rollout |
| Autoscaling | HPA on GPU workloads — monitor for **compute hijacking** (Ch.3, Ch.10) |
| Canary / shadow | KServe canary traffic split — align with Ch.6 CT cycle controls |

Do not expose `InferenceService` directly to the internet without gateway guardrails.

> *Refs - Frameworks: [KServe](https://github.com/kserve/kserve) project documentation. This guide: [Secure deployment methods for retrained models](06-pipeline.md#secure-deployment-methods-for-retrained-models) (Chapter 6); [AI Compute Hijacking](03-threat-landscape.md#ai-compute-hijacking-demonstrated--active-patterns) (Chapter 3).*

## GPU isolation and shared inference

GPU-related incidents (LeftoverLocals `CVE-2023-4969`, cryptomining on compromised Ray/vLLM clusters) show that **software time-slicing alone is insufficient** for sensitive multi-tenant tiers.

| Risk | Control |
|---|---|
| Cross-process GPU memory leak | Driver updates, memory sanitization, process isolation (Ch.13) |
| `KV Cache` leak between tenants | Tenant-partitioned cache; session cleanup; no shared sticky cache keys |
| GPU colocation side channels | NVIDIA MIG or dedicated GPU per tenant tier |
| Unauthorized GPU workloads | Node taints (`nvidia.com/gpu`), quota, Falco rules on unexpected GPU processes |
| Cryptomining | Runtime monitor + anomaly on GPU util vs expected inference baseline |

Inference security observability should capture **serving-behavior signals** (handler baselines, accelerator usage anomalies), not only model quality metrics ([ARMO inference observability analysis](https://www.armosec.io/blog/observability-for-ai-inference-servers/)).

> *Refs - Frameworks: [CVE-2023-4969](https://nvd.nist.gov/vuln/detail/CVE-2023-4969) (LeftoverLocals); NVIDIA MIG documentation (vendor). This guide: [LeftoverLocals case study](13-case-studies.md#leftoverlocals-cve-2023-4969--documented-incident) (Chapter 13); [Security metrics](10-monitoring-soc-ir.md#security-metrics) (Chapter 10).*

## Runtime security on the cluster

| Tool | Role in MLSecOps |
|---|---|
| **Falco** | Detect shell spawn in inference pods, unexpected outbound connections, crypto miners |
| **Tetragon/eBPF** | Fine-grained process and network observability |
| **KubeArmor** | Enforcement + audit for ML pod hardening |
| **Cilium Hubble** | Flow visibility for NetworkPolicy debugging and threat hunting |

Map runtime alerts to `MITRE ATLAS` techniques in SOC playbooks (Ch.10).

> *Refs - Frameworks: MITRE ATLAS: runtime and infrastructure techniques (map in SOC playbooks); Falco, Tetragon/eBPF, KubeArmor, Cilium Hubble - upstream project docs. This guide: [Detection Engineering](10-monitoring-soc-ir.md#detection-engineering) (Chapter 10); [Threat analysis with MITRE ATLAS](10-monitoring-soc-ir.md#threat-analysis-with-mitre-atlas) (Chapter 10).*

## Egress control for agentic workloads

When agents run **inside** the cluster and generate outbound traffic dynamically:

1. Deploy an **egress gateway** (Envoy/Squid) with domain allowlist + full request logging.
2. Deny direct internet egress from agent executor pods.
3. Require human approval (`Intent Gate`, Ch.8) before adding new egress destinations.
4. Correlate egress logs with prompt/tool telemetry in SIEM.

> *Refs - Frameworks: [Application Security Standards - AI egress playbook](https://appsecuritystandards.org/blog/ai-workloads-in-kubernetes-a-security-implementation-playbook). This guide: [Intent Gate](08-agentic-ai-security.md#intent-gate) (Chapter 8); [Data required for telemetry](10-monitoring-soc-ir.md#data-required-for-telemetry) (Chapter 10).*

## MCP servers on Kubernetes

When MCP tool servers run as cluster workloads (sidecars or standalone Deployments), apply the same isolation model as inference services plus MCP-specific controls from [Chapter 7](07-llm-rag-security.md#model-context-protocol-mcp-security):

| Risk | Control |
|---|---|
| MCP server with ClusterRole | Dedicated namespace; no cluster-admin; RBAC scoped to required API only |
| Unsigned MCP image | Kyverno cosign verify (same as inference) |
| Tool schema rug-pull at runtime | Sidecar MCP gateway with hash-pinned `tools/list`; log schema changes to SIEM |
| Shadow MCP sidecar | Admission deny for unregistered MCP container names; allowlist in Kyverno |
| Egress from MCP pod | Default-deny NetworkPolicy; route tool HTTP via egress gateway |

Pair cluster manifests with an MCP server source review such as `mcps-audit` before deploy (Ch.12).

> *Refs - Frameworks: OWASP MCP Top 10: `MCP03`, `MCP09`. This guide: [Model Context Protocol (MCP) security](07-llm-rag-security.md#model-context-protocol-mcp-security) (Chapter 7); [Appendix: Informative tool command reference](12-threat-control-tools-map.md#appendix-informative-tool-command-reference) (Chapter 12).*

## Mapping to lifecycle control points

| Lifecycle control point | Kubernetes control |
|---|---|
| 3 — Security and quality review | Scan IaC for cluster manifests; scan inference images |
| 8 — Release decision | Policy review: NetworkPolicy + Kyverno + PSA level documented |
| 9 — Integrity and provenance | Cosign sign image/model artifact where applicable; Kyverno verify at admission |
| 10 — Store and monitor | Deploy signed digest; enable runtime + GPU telemetry to SOC |

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): deploy/monitor lifecycle alignment. This guide: [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6); [What is an Evidence Pack?](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11).*

## Tool and reference index

| Resource | URL |
|---|---|
| vLLM production-stack | https://github.com/vllm-project/production-stack |
| KServe | https://github.com/kserve/kserve |
| Kyverno image verification | https://kyverno.io/docs/policy-types/image-validating-policy/ |
| awesome-MLSecOps (community index) | https://github.com/RiccardoBiosas/awesome-MLSecOps |
| OpenSSF Secure MLOps whitepaper | https://openssf.org/wp-content/uploads/2025/08/OpenSSF_MLSecOps_Whitepaper.pdf |
| KubeStellar Console (multi-cluster MLSecOps dashboard) | https://github.com/kubestellar/console |

> *Refs - Frameworks: Upstream URLs in table (vLLM, KServe, Kyverno, OpenSSF whitepaper). This guide: [Commercial Tool Market Map](12-threat-control-tools-map.md#commercial-tool-market-map) (Chapter 12) for broader tooling context. Author note: Tool index is informative - no endorsement; evaluate fit against your threat model.*

## Minimum baseline checklist (Level 2 production)

- [ ] Dedicated namespaces with restricted PSA for inference
- [ ] Default-deny NetworkPolicy + gateway-only ingress
- [ ] Kyverno (or OPA) blocks unsigned images in prod namespaces
- [ ] Inference pods: non-root, dropped capabilities, secrets from External Secrets/Vault
- [ ] vLLM/KServe protected by API key or OAuth at gateway
- [ ] GPU isolation strategy documented (MIG or dedicated nodes for sensitive tenants)
- [ ] Runtime rules for GPU abuse and cryptomining enabled
- [ ] Deploy only digest-pinned, signed images tied to Evidence Pack

> *Refs - Frameworks: Kubernetes Pod Security Standards; Kyverno cosign verification. This guide: [Level 2: Operational](14-maturity-roadmap.md#level-2-operational) (Chapter 14); [Minimum baseline checklist](#minimum-baseline-checklist-level-2-production) items above.*

## Practical principle

Kubernetes secures **where** the model runs; MLSecOps secures **what** runs and **whether** it may be promoted. Cluster hardening without lifecycle integrity controls and release decisions is incomplete — and signed models deployed in wide-open namespaces are equally unsafe.

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): infrastructure + lifecycle integration. This guide: [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6); [Reference architecture](#reference-architecture) (this chapter). Author note: Where/what/whether framing is author synthesis for platform + AppSec alignment.*

## Practical summary

1. Isolate inference in dedicated namespaces with least-privilege RBAC.
2. Default-deny network traffic; expose inference only through an AI gateway.
3. Enforce cosign verification at admission for production namespaces.
4. For vLLM, use production-stack patterns for API keys and secrets — never commit keys to git.
5. Treat GPU memory and shared inference as a first-class threat (LeftoverLocals, KV cache).
6. Pair cluster controls with Evidence Pack records for every promoted artifact.

> *Refs - This guide: [E.1.3 Self-hosted LLM architecture card](17-appendix-e-implementation-reference.md#e13-self-hosted-llm-vllm--kserve-on-kubernetes) (Chapter 17); sections above in this chapter.*
