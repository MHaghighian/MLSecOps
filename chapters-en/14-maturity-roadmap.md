# Chapter 14: MLSecOps Maturity Roadmap

## Why Phased Maturity Matters

Implementing full `MLSecOps` in a single phase is usually impractical. Teams must progress based on their risk, capacity, and architecture. The maturity roadmap helps an organization start with foundational controls and gradually reach an auditable, operational architecture.

## Maturity Levels

| Level | Status | Characteristics |
|---|---|---|
| Level 0 | No coherent controls | Models are built and released manually; evidence is scarce. |
| Level 1 | Foundational | Threat model, data validation, artifact scan, and team awareness are in place. |
| Level 2 | Operational | Explicit release decisions, integrity/provenance evidence, security validation, runtime telemetry, and SOC runbook exist. |
| Level 3 | Mature | Automated evidence, advanced SOC, tamper-evident storage, multi-tenant hardening, and regression tracking are in place. |

## Level 1: Foundational

The goal of Level 1 is to prevent fundamental errors before entering `Production`. The entry criterion for this level is implementation of a minimum baseline.

| Capability | Readiness Criterion |
|---|---|
| `Threat Model` and planning | `ATLAS/OWASP` document before the first release workflow |
| `Data Validation` | Schema and PII check before train |
| Artifact scan | `ModelScan` at load stage |
| Awareness | Team is aware of `Prompt Injection`, supply chain, Shadow AI, and MCP hygiene |

## Level 2: Operational

The goal of Level 2 is repeatable release decision control and runtime defense.

| Capability | Readiness Criterion |
|---|---|
| Release decision control | No undocumented manual exceptions for deploy |
| Signing | All production models are signed and verified |
| `Adversarial / LLM Test` | `ART` or prompt suite with acceptance criteria runs before release |
| Runtime | `Inference Gateway`, telemetry, and tracking for FN/bypass |
| SOC | Runbook, SIEM rule, and incident SLA |

The condition for advancing to Level 3 is **demonstrated process maturity**: evidence on every release for at least 6 months, release decisions operating without routine undocumented override, regression suite tracked in SOC, and **no unmitigated P1 control failures** (reporting incidents does not block maturity—cover-ups do).

## Level 3: Mature

The goal of Level 3 is automated audit, organizational compliance, and continuous improvement.

| Capability | Readiness Criterion |
|---|---|
| Automated evidence pack | Produced in every build without manual intervention |
| Advanced SOC | Alerts mapped and correlated to `MITRE ATLAS` |
| Tamper-evident evidence | Use of `Rekor`, `WORM`, or object lock |
| Multi-tenant / K8s | RBAC, service mesh, NetworkPolicy, signed-image admission — [Ch.16](16-kubernetes-deployment-reference.md) |
| Shadow AI program | AI-AUP, CASB/DLP, enterprise gateway, discovery — [Ch.11](11-governance-evidence.md#shadow-ai-governance) |
| MCP governance | Server allowlist, gateway, static + workstation scan — [Ch.7](07-llm-rag-security.md#model-context-protocol-mcp-security) |
| Compliance | Trace from `NIST AI RMF`, `ISO 42001`, and `EU AI Act` to controls |
| Continuous improvement | Periodic red team and regression tracking |

## Minimum Starting Controls

For a practical start, these controls deliver the most value:

- Record data and model versions
- Scan secrets and dependencies
- Scan model artifacts
- Define release decision criteria that actually block or escalate risk
- Sign models before release
- Record a basic evidence pack
- Monitor prompt, response, and tool call

## Recommended 90-Day Path

> **Capacity note:** This path assumes a dedicated core team (security + MLOps + one product squad). Larger enterprises or regulated environments may require longer phases; smaller teams should prioritize Level 1 minimum controls first.

| Period | Focus | Output |
|---|---|---|
| Day 1 to 30 | Discovery and foundation | Threat model (incl. Shadow AI + MCP rows), asset inventory, data control, AI-AUP draft |
| Day 31 to 60 | Lifecycle controls | Release decision criteria, scan/review process, security validation, MCP server review, evidence pack |
| Day 61 to 90 | Runtime | Gateway, K8s baseline (Ch.16), telemetry, alert, and rollback |

## Maturity Metrics

| Metric | Sign of Maturity |
|---|---|
| Reproducibility | Model can be rebuilt with the same data and code. |
| Auditability | All release decisions have evidence. |
| Automatic stop | Critical criteria actually block or escalate release. |
| Runtime security | Prompt, response, retrieval, and tool call are monitored. |
| Incident response | Rollback and playbook are defined. |

## Common Mistakes on the Maturity Path

- Starting with many tools without a threat model
- Ignoring data and focusing solely on the model
- Creating controls that only warn and are never tied to a release decision
- Forgetting runtime and SOC
- Manually producing evidence after an incident

## Practical Principle

`MLSecOps` maturity does not start with buying tools. It starts with understanding assets, defining threats, implementing foundational controls, and producing reliable evidence.
