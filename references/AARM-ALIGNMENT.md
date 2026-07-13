# AARM Alignment

**AARM** ([Autonomous Action Runtime Management](https://aarm.dev/)) is an open system specification from the [Cloud Security Alliance](https://cloudsecurityalliance.org/research/working-groups/autonomous-action-runtime-management-aarm) for securing AI-driven actions at runtime — intercept, authorize, and audit before execution.

This page maps AARM concepts to sections of the **MLSecOps Practical Reference Guide**. It is **complementary alignment**, not an official AARM document or conformance claim. For normative requirements, use the [AARM specification](https://aarm.dev/spec).

---

## Mapping

| AARM | MLSecOps |
|------|----------|
| Runtime Authorization | [Chapter 8 — Agentic AI Security](../chapters-en/08-agentic-ai-security.md) |
| Context | [Chapter 7](../chapters-en/07-llm-rag-security.md) (retrieval / prompt context) · [Chapter 8](../chapters-en/08-agentic-ai-security.md) (agent memory) · [Chapter 11 — Evidence Pack](../chapters-en/11-governance-evidence.md#what-is-an-evidence-pack) (audit receipts) |
| Intent | [Intent Gate](../chapters-en/08-agentic-ai-security.md#intent-gate) (Ch.8) |
| Runtime Monitoring | [Chapter 10 — Monitoring, SOC, and IR](../chapters-en/10-monitoring-soc-ir.md) |
| Threat Model | [Chapter 2 — Scope and Threat Model](../chapters-en/02-scope-risk-threat-model.md) |
| Implementation | [Appendix E — Implementation Reference](../chapters-en/17-appendix-e-implementation-reference.md) |

---

## AARM requirements (quick cross-ref)

| AARM requirement | MLSecOps pointer |
|------------------|------------------|
| R1 Pre-execution interception | Ch.8 — Intent Gate, tool policy |
| R2 Context accumulation | Ch.7, Ch.8 |
| R3 Policy + intent alignment | Ch.8 — Intent Gate |
| R4 Authorization decisions (allow / deny / modify / step-up / defer) | Ch.8 — HITL, scoped tools |
| R5 Tamper-evident receipts | Ch.11 — Evidence Pack |
| R6 Identity binding | Ch.2, Ch.8 |
| R7 Semantic distance / intent drift (Extended) | Ch.8, Ch.10 |
| R8 Telemetry export (Extended) | Ch.10 |
| R9 Least-privilege enforcement (Extended) | Ch.8 — scoped tools, MCP |

---

## Related frameworks

- OWASP Agentic Security Initiative — [Chapter 8](../chapters-en/08-agentic-ai-security.md)
- OWASP AI Exchange — [Chapter 1](../chapters-en/01-intro.md#relationship-to-owasp-ai-exchange)
- CSA MAESTRO — [Chapter 15 References](../chapters-en/15-conclusion-appendix.md#references)

---

*Alignment page · MLSecOps Practical Reference Guide · not an AARM conformance statement*
