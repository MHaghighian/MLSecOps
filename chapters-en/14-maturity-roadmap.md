# Chapter 14: MLSecOps Maturity Roadmap

## Why Phased Maturity Matters

Implementing full `MLSecOps` in a single phase is usually impractical. Teams must progress based on their risk, capacity, and architecture. The maturity roadmap helps an organization start with foundational controls and gradually reach an auditable, operational architecture.

> *Refs - Frameworks: NIST AI RMF: Govern / Map (phased capability building); OpenSSF MLSecOps whitepaper (2025): lifecycle visualization. This guide: [Maturity Levels](#maturity-levels); [Recommended 90-Day Path](#recommended-90-day-path). Author note: Phased maturity framing is community guidance for prioritization - not a certified assessment framework.*

## Maturity Levels

These levels are **descriptive prioritization guidance, not a numeric scoring rubric**, and they measure the maturity of *security* controls only. **No maturity level - including Level 1 - confers conformance with ISO/IEC 42001, ISO/IEC 27001, or the EU AI Act.** Those regimes require a management system (policy, impact assessment, internal audit, management review, conformity assessment) whose mandatory clauses apply regardless of maturity level; track them separately.

| Level | Status | Characteristics |
|---|---|---|
| Level 0 | No coherent controls | Models are built and released manually; evidence is scarce. |
| Level 1 | Foundational | Threat model, data validation, artifact scan, and team awareness are in place. |
| Level 2 | Operational | Explicit release decisions, integrity/provenance evidence, security validation, runtime telemetry, and SOC runbook exist. |
| Level 3 | Mature | Automated evidence, advanced SOC, tamper-evident storage, multi-tenant hardening, and regression tracking are in place. |

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): lifecycle visualization; NIST AI RMF: phased capability building. This guide: [Minimum starting controls](#minimum-starting-controls); [OpenSSF mapping](11-governance-evidence.md#openssf-mlsecops-mapping-whitepaper-2025) (Chapter 11). Author note: Level 0-3 definitions and 90-day path are community maturity guidance, not a certified assessment framework.*

## Level 1: Foundational

The goal of Level 1 is to prevent fundamental errors before entering `Production`. The entry criterion for this level is implementation of a minimum baseline.

| Capability | Readiness Criterion |
|---|---|
| `Threat Model` and planning | `ATLAS/OWASP` document before the first release workflow |
| `Data Validation` | Schema and PII check before train |
| Artifact scan | `ModelScan` at load stage |
| Awareness | Team is aware of `Prompt Injection`, supply chain, Shadow AI, and MCP hygiene |

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): foundational control themes; OWASP LLM Top 10 (2025); OWASP MCP Top 10 - awareness rows in threat model. This guide: [Minimum security baseline](06-pipeline.md#minimum-security-baseline) (Chapter 6); [Minimum Starting Controls](#minimum-starting-controls).*

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

> *Refs - Frameworks: NIST AI RMF: Measure / Manage (operational monitoring and response); ISO/IEC 42001: operational control and evidence themes. This guide: [Release decision model](06-pipeline.md#release-decision-model) (Chapter 6); [SOC integration](10-monitoring-soc-ir.md#soc-integration) (Chapter 10); [Kubernetes deployment reference](16-kubernetes-deployment-reference.md) (Chapter 16).*

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

> *Refs - Frameworks: NIST AI RMF: Govern (continuous improvement); EU AI Act / ISO/IEC 42001: audit and management-system maturity themes (map to your jurisdiction). This guide: [What is an Evidence Pack?](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11); [Appendix E.4 - Evidence Pack template](17-appendix-e-implementation-reference.md#e4-evidence-pack-template) (Chapter 17); [Shadow AI governance](11-governance-evidence.md#shadow-ai-governance) (Chapter 11); [MCP security](07-llm-rag-security.md#model-context-protocol-mcp-security) (Chapter 7).*

## Minimum Starting Controls

For a practical start, these controls deliver the most value:

- Record data and model versions
- Scan secrets and dependencies
- Scan model artifacts
- Define release decision criteria that actually block or escalate risk
- Sign models before release
- Record a basic evidence pack
- Monitor prompt, response, and tool call

> *Refs - Frameworks: OpenSSF MLSecOps whitepaper (2025): 22 control themes (informative baseline). This guide: [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6); [Model security controls](05-model-artifact-supply-chain.md#model-security-controls) (Chapter 5).*

## Recommended 90-Day Path

> **Capacity note:** This path assumes a dedicated core team (security + MLOps + one product squad). Larger enterprises or regulated environments may require longer phases; smaller teams should prioritize Level 1 minimum controls first.

| Period | Focus | Output |
|---|---|---|
| Day 1 to 30 | Discovery and foundation | Threat model (incl. Shadow AI + MCP rows), asset inventory, data control, AI-AUP draft |
| Day 31 to 60 | Lifecycle controls | Release decision criteria, scan/review process, security validation, MCP server review, evidence pack |
| Day 61 to 90 | Runtime | Gateway, K8s baseline (Ch.16), telemetry, alert, and rollback |

> *Refs - Frameworks: NIST AI RMF: Map -> Measure phased rollout (informative alignment). This guide: [Level 1](#level-1-foundational) and [Level 2](#level-2-operational) readiness tables; [Shadow AI governance](11-governance-evidence.md#shadow-ai-governance) (Chapter 11); [Appendix E.4 - Evidence Pack template](17-appendix-e-implementation-reference.md#e4-evidence-pack-template) (Chapter 17). Author note: 90-day path assumes a dedicated core team; adjust duration for regulated or resource-constrained environments.*

## Maturity Metrics

| Metric | Sign of Maturity |
|---|---|
| Reproducibility | Model can be rebuilt with the same data and code. |
| Auditability | All release decisions have evidence. |
| Automatic stop | Critical criteria actually block or escalate release. |
| Runtime security | Prompt, response, retrieval, and tool call are monitored. |
| Incident response | Rollback and playbook are defined. |

> *Refs - Frameworks: NIST AI RMF: Measure (metrics and monitoring). This guide: [Assurance metrics](11-governance-evidence.md#assurance-metrics) (Chapter 11); [Security metrics](10-monitoring-soc-ir.md#security-metrics) (Chapter 10).*

## Common Mistakes on the Maturity Path

- Starting with many tools without a threat model
- Ignoring data and focusing solely on the model
- Creating controls that only warn and are never tied to a release decision
- Forgetting runtime and SOC
- Manually producing evidence after an incident

> *Refs - Frameworks: NIST AI RMF: Govern (common failure modes in AI risk programs). This guide: [Common anti-patterns](09-anti-patterns.md#common-anti-patterns) (Chapter 9); [One-time security testing](09-anti-patterns.md#one-time-security-testing) (Chapter 9). Author note: Mistake list is practitioner synthesis from maturity engagements - not a formal standard checklist.*

## Practical Principle

`MLSecOps` maturity does not start with buying tools. It starts with understanding assets, defining threats, implementing foundational controls, and producing reliable evidence.

> *Refs - This guide: [Lifecycle control points](06-pipeline.md#lifecycle-control-points) (Chapter 6); [Evidence Pack](11-governance-evidence.md#what-is-an-evidence-pack) (Chapter 11); [Appendix E.4 - Evidence Pack template](17-appendix-e-implementation-reference.md#e4-evidence-pack-template) (Chapter 17).*
