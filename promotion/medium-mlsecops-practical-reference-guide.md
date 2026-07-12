# MLSecOps Practical Reference Guide: An Open-Source Handbook for Securing AI in Production

**Suggested Medium title:** MLSecOps Practical Reference Guide — Securing AI Systems Across the Full Lifecycle  
**Suggested subtitle:** A free, practitioner-oriented reference for LLM, RAG, agent, and ML supply chain security — built on OWASP, NIST, MITRE ATLAS, and ISO/IEC 42001.  
**Author:** Moslem Haghighian  
**Tags (Medium):** MLSecOps, AI Security, LLM Security, DevSecOps, Cybersecurity, Machine Learning, Open Source

---

DevSecOps taught us to ship software with security woven into the pipeline. That model works — until the system you are protecting is not just code.

Modern AI systems introduce risks that live in training data, model artifacts, prompts, embeddings, retrieval indexes, autonomous agents, and runtime behavior. A passing SAST scan does not tell you whether a RAG pipeline will leak another tenant’s documents. A container image signature does not stop prompt injection at the gateway. A quarterly penetration test does not replace continuous evidence that your release gates actually ran.

Teams are not short on frameworks. OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF, ISO/IEC 42001, OpenSSF Secure MLOps, and CSA MAESTRO each cover important ground. What practitioners still lack is a **single, implementation-oriented thread** that connects threats, controls, release decisions, SOC integration, and governance across the full ML lifecycle.

That gap is why I published the **MLSecOps Practical Reference Guide** — an open-source handbook for securing AI systems in real production environments.

**Read the guide:** [l4tr0d3ctism.github.io/MLSecOps](https://l4tr0d3ctism.github.io/MLSecOps/)  
**Source & downloads:** [github.com/l4tr0d3ctism/MLSecOps](https://github.com/l4tr0d3ctism/MLSecOps)  
**Cite (DOI):** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781)  
**License:** CC BY-SA 4.0

---

## What MLSecOps means in practice

**MLSecOps** extends DevSecOps and MLOps with lifecycle-specific security controls, evidence generation, and AI-focused governance. It does not replace your CI/CD platform, model registry, or LLM gateway. It defines **where** controls belong, **what** must be evidenced before release, and **how** runtime and SOC teams detect and respond when models behave unexpectedly.

The guide treats AI security as a continuous, auditable flow — from the moment a change is proposed through monitoring and incident response — not as a one-time checklist before go-live.

---

## Why traditional DevSecOps is not enough

Classic application security assumes that the primary attack surface is application code and its dependencies. AI systems break that assumption in several ways:

**Data is part of the attack surface.** Poisoned training data, PII in fine-tuning sets, and augmentation pipelines that pull from untrusted sources can compromise models before inference ever runs.

**Models are artifacts with supply-chain risk.** Unsigned checkpoints, tampered weights, and opaque third-party models introduce integrity risks that binary scanning alone cannot address.

**LLMs and RAG add semantic attack vectors.** Prompt injection, jailbreaks, retrieval leakage, and cross-tenant data exposure require controls at the gateway, policy layer, and output gate — not only in application logic.

**Agents introduce action risk.** When models can call tools, APIs, terminals, or MCP servers, intent validation and scoped execution matter as much as input filtering.

**Runtime behavior is unpredictable.** Drift, abuse, shadow AI, and unbounded consumption are operational security problems that belong in SOC workflows, not only in pre-release review.

The guide does not argue that existing frameworks are wrong. It argues that teams need a **practical architecture** to operationalize them together.

---

## What this guide adds beyond individual frameworks

The MLSecOps Practical Reference Guide **synthesizes** published frameworks. It is not an official OWASP, NIST, or ISO document, and it does not introduce a competing standard. Its operational additions are:

### 1. Ten lifecycle control points

Instead of listing controls in isolation, the guide defines **ten control points** along one thread: from change initiation and data handling through training, validation, release decisions, deployment integrity, runtime monitoring, and governance. Each point has a clear security purpose and connects to evidence expectations.

### 2. Explicit release decisions

Not every security step should block a release. The guide separates **evidence-producing steps** from **blocking gates** at control points 4, 7, and 8, with integrity checks at point 9. That distinction helps teams move fast without pretending that a green build equals a secure AI deployment.

### 3. Evidence Pack methodology

Governance and security reviews need auditable outputs, not slide decks. The guide defines an **Evidence Pack** — a structured bundle per release that teams can attach to change records, risk committees, or compliance workflows.

### 4. Implementation Reference (Appendix E)

Frameworks describe *what* to protect. Appendix E helps teams decide *how* to implement: architecture cards, decision matrices, templates, and playbooks for patterns such as LLM gateways, RAG with ACL, agent tool policy, and Kubernetes deployment references.

### 5. Per-section traceability (v1.1.0)

Version 1.1.0 adds **`References / Source mapping`** across all chapters — distinguishing framework text, implementation guidance, author opinion, and emerging research. OWASP AI Exchange is integrated as a complementary taxonomy where topics align, without duplicating the Exchange itself.

---

## What the guide covers

The guide is organized for practitioners who need to go deep on specific topics without losing the lifecycle thread:

- **Scope and threat modeling** — AI-specific risk framing and autonomous AI threats  
- **Data security and privacy** — training data, PII, augmentation confidentiality  
- **Model and supply chain** — artifacts, provenance, signing, dependency risk  
- **Secure ML pipeline** — ten control points, CI/CD integration, release gates  
- **LLM and RAG security** — gateways, guardrails, prompt injection, retrieval ACL  
- **Agentic AI and MCP** — tool policy, Intent Gate, scoped execution  
- **Anti-patterns** — what teams get wrong when scaling AI security  
- **Monitoring and SOC** — detection, telemetry, incident response for AI systems  
- **Governance and evidence** — policies, maturity, audit-ready outputs  
- **Threat–control–tool mapping** — practical selection support  
- **Case studies** — real-world failure modes and lessons  
- **Maturity roadmap** — staged adoption for organizations at different levels  
- **Kubernetes reference** — deployment patterns for ML and LLM workloads  

Coverage spans classic ML, managed AI APIs, LLMs, RAG, agents, MCP, shadow AI, supply chain, runtime, SOC, and governance.

---

## Who should read it

The guide is written for:

- **Security engineers and AppSec** teams rolling out AI controls  
- **ML and MLOps engineers** who own pipelines and model releases  
- **Architects** designing gateway, RAG, and agent stacks  
- **Risk and governance stakeholders** who need evidence, not buzzwords  

If you are an executive looking for a ten-page overview, start with Chapter 1 and the maturity roadmap. If you are shipping an LLM copilot next quarter, start with Chapters 7, 8, and Appendix E.

---

## How to use it

You do not need to read all seventeen chapters before doing anything useful.

| Role | Suggested path |
|------|----------------|
| Executive / risk | Ch.1 → Ch.2 → Ch.14 (maturity roadmap) |
| Security engineer | Ch.2 → Ch.6 → Ch.12 (threat–control map) |
| ML / MLOps | Ch.6 → Ch.5 (supply chain) |
| LLM / RAG / Agent | Ch.7 → Ch.8 → Appendix E |
| Production rollout | Appendix E → Ch.6 |

The documentation site includes search, table of contents, and chapter navigation:  
[https://l4tr0d3ctism.github.io/MLSecOps/](https://l4tr0d3ctism.github.io/MLSecOps/)

Downloads (PDF, DOCX, source ZIP) are available on [GitHub Releases v1.1.0](https://github.com/l4tr0d3ctism/MLSecOps/releases/tag/v1.1.0).

---

## What this guide is not

Clarity matters for an open reference:

- It is **not** a product user manual for any vendor tool.  
- It is **not** an official OWASP, NIST, ISO, or OpenSSF publication.  
- It is **not** a replacement for legal, safety, or sector-specific compliance advice.  
- It does **not** present original empirical research — it synthesizes frameworks and operational patterns.  

It is a **community reference** you can fork, cite, adapt, and improve under CC BY-SA 4.0.

---

## Why open source

AI security guidance ages quickly. Models, attack techniques, and vendor capabilities change faster than printed books. Publishing the guide as open source on GitHub and Zenodo means:

- practitioners can use it without paywalls;  
- teams can trace guidance to framework sources (especially after v1.1.0 traceability);  
- the community can file issues, suggest fixes, and discuss trade-offs;  
- citations have a stable DOI for academic and professional use.  

If you review the guide and find gaps, open an issue or discussion on GitHub. If you use it in production, a star, citation, or link from your blog helps other teams discover it.

---

## A practical closing thought

The hardest part of AI security is not naming the threats. It is **operationalizing** controls without blocking delivery, **proving** that controls ran, and **detecting** when runtime behavior diverges from what you tested.

Frameworks give us vocabulary. MLSecOps, in this guide, is an attempt to give teams a **lifecycle** — one thread from data to SOC that security, ML, and platform engineers can actually follow.

If you are building or securing AI systems in production, I hope this reference saves you time and sparks better conversations with your team.

**Start reading:** [MLSecOps Practical Reference Guide](https://l4tr0d3ctism.github.io/MLSecOps/)  
**Repository:** [github.com/l4tr0d3ctism/MLSecOps](https://github.com/l4tr0d3ctism/MLSecOps)  
**DOI:** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781)

---

## Publishing notes (remove before publishing on Medium)

**Canonical link:** Set canonical URL to `https://l4tr0d3ctism.github.io/MLSecOps/` if Medium allows it, or link prominently in the first paragraph (already done).

**Featured image ideas:** Executive lifecycle diagram from the guide (`01-intro_02.png`) or a simple architecture graphic (gateway → policy → LLM → DLP).

**First 100 words** are optimized for Medium preview and search snippets — keep them when pasting.

**Bio line suggestion:** Moslem Haghighian — author of the MLSecOps Practical Reference Guide; focuses on AI security, secure MLOps, and operational controls for LLM/RAG/agent systems.

**Cross-post:** Dev.to (shorter excerpt + link), LinkedIn (summary + link to Medium or directly to Pages).

---

*Draft for Medium · v1.0 · 2026-07-12 · MLSecOps Practical Reference Guide promotion*
