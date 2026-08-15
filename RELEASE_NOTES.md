# Release Notes

Official releases: [GitHub Releases](https://github.com/MHaghighian/MLSecOps/releases)

---

## v1.2.0 — 2026-08-15

**Example C secure-by-design hardening** — Appendix E self-hosted serving platform deepened with researched controls (gateway authZ, overwritten `cache_salt`, fail-closed admit, MIG/MPS/LeftoverLocals accuracy) and regenerated diagrams.

**DOI:** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) (publish a new Zenodo version from tag `v1.2.0` after GitHub Release)

| Format | Link |
|--------|------|
| Source (ZIP) | [Source code (zip)](https://github.com/MHaghighian/MLSecOps/archive/refs/tags/v1.2.0.zip) |
| Markdown | `chapters-en/` in this repository |
| Site | https://mhaghighian.github.io/MLSecOps/ |
| Maintainer | https://mhsec.me |
| Word (optional) | `python scripts/build-docx.py --render-mermaid` |

### Highlights

- Example C: caller→engine authN + gateway authZ; overwrite `cache_salt` (vLLM ≥ 0.9.0 / CVE-2025-46570)
- Safetensors allowlist; ModelScan for legacy formats; fail-closed Kyverno + HA
- MIG K8s vs VM wording; MPS not isolation; LeftoverLocals NVIDIA nuance
- Regenerated Example C diagrams `_16`–`_18`

Full change history: [CHANGELOG.md](CHANGELOG.md).

---

## v1.1.3 — 2026-07-26

**KV Cache security** — Ch.7 section on inference KV privacy (reconstruction vs side-channel), `CAG`, and Emerging KV-Cloak-class controls; maintainer site [mhsec.me](https://mhsec.me) on the documentation site.

**DOI:** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) (publish a new Zenodo version from tag `v1.1.3` after GitHub Release)

| Format | Link |
|--------|------|
| Source (ZIP) | [Source code (zip)](https://github.com/MHaghighian/MLSecOps/archive/refs/tags/v1.1.3.zip) |
| Markdown | `chapters-en/` in this repository |
| Site | https://mhaghighian.github.io/MLSecOps/ |
| Maintainer | https://mhsec.me |
| Word (optional) | `python scripts/build-docx.py --render-mermaid` |

### Highlights

- KV Cache primer + threat classes (direct reconstruction / PromptPeek) + control maturity table
- `CAG` treated as durable sensitive KV; baseline = tenant isolation + cleanup
- Docs social/home link to mhsec.me

Full change history: [CHANGELOG.md](CHANGELOG.md).

---

## v1.1.2 — 2026-07-25

**Secure by design + prompt-injection architecture** — L0–L3 design-level prompt-injection defenses; Secure by design defaults across Ch.1/4/7/8 ([PR #5](https://github.com/MHaghighian/MLSecOps/pull/5)); tool maturity labels; Pages/sitemap host fix after account rename.

**DOI:** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) (publish a new Zenodo version from tag `v1.1.2` after GitHub Release)

| Format | Link |
|--------|------|
| Source (ZIP) | [Source code (zip)](https://github.com/MHaghighian/MLSecOps/archive/refs/tags/v1.1.2.zip) |
| Markdown | `chapters-en/` in this repository |
| Site | https://mhaghighian.github.io/MLSecOps/ |
| Word (optional) | `python scripts/build-docx.py --render-mermaid` |

### Highlights

- Secure by design: assume-injection, authorization outside the model, credential insulation, intra-tenant vector RLS, zero-egress rendering (EchoLeak / `CVE-2025-32711`), delegated/NHI agent identity
- Prompt injection defenses L0–L3 (filters → Dual-LLM / CaMeL / IFC-style patterns)
- Tool maturity labels (`Mature` / `Emerging` / `Research/Lab`) in Ch.11–12
- GitHub Pages URLs pointed at `mhaghighian.github.io`

Full change history: [CHANGELOG.md](CHANGELOG.md).

---

## v1.1.1 — 2026-07-16

**Community review + Issue #1 format restore** — citation and content fixes from [PR #3](https://github.com/l4tr0d3ctism/MLSecOps/pull/3); per-section `References / Source mapping` blocks restored; PDF/DOCX no longer attached to releases.

**DOI:** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) (publish a new Zenodo version from tag `v1.1.1` after GitHub Release)

| Format | Link |
|--------|------|
| Source (ZIP) | [Source code (zip)](https://github.com/l4tr0d3ctism/MLSecOps/archive/refs/tags/v1.1.1.zip) |
| Markdown | `chapters-en/` in this repository |
| Site | https://mhaghighian.github.io/MLSecOps/ |
| Word (optional) | `python scripts/build-docx.py --render-mermaid` |

### Highlights

- Restored Issue #1 `### References / Source mapping` blocks (keeping corrected IDs from PR #3)
- Community review: ATLAS/OWASP citation fixes, scope and Evidence Pack clarifications
- AARM alignment page; GUIDE-SUMMARY removed from public site
- Releases ship source + docs site only (no pre-built PDF/DOCX)

Full change history: [CHANGELOG.md](CHANGELOG.md).

---

## v1.1.0 — 2026-07-11

**Traceability and mapping release** — per-section `References / Source mapping` across all chapters; OWASP AI Exchange complementary integration; community Issues [#1](https://github.com/l4tr0d3ctism/MLSecOps/issues/1) and [#2](https://github.com/l4tr0d3ctism/MLSecOps/issues/2) addressed.

**DOI:** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781)

| Format | Link |
|--------|------|
| Source (ZIP) | [Source code (zip)](https://github.com/l4tr0d3ctism/MLSecOps/archive/refs/tags/v1.1.0.zip) |
| Markdown | `chapters-en/` in this repository |
| Site | https://mhaghighian.github.io/MLSecOps/ |

### Highlights

- **Traceability convention** (Ch.15) — four content types: frameworks, implementation guidance, author opinion, emerging/research
- **`References / Source mapping`** on every major section (`##`) in Chapters 1–17
- **OWASP AI Exchange** — complementary taxonomy and permalinks where topics align (not a full duplicate)
- **Ch.1** — reader value proposition, guide at a glance, Exchange positioning
- **MITRE ATLAS** mapping audit and Appendix B sync
- **Ch.13** — CVE-2025-68664 added to LangChain deserialization case study

Full change history: [CHANGELOG.md](CHANGELOG.md).

---

## v1.0.1 — 2026-07-05

**Zenodo archival release** — identical guide content to v1.0.0.

**DOI:** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) · [Zenodo record](https://zenodo.org/records/21206781)

| Format | Link |
|--------|------|
| Source (ZIP) | [Source code (zip)](https://github.com/l4tr0d3ctism/MLSecOps/archive/refs/tags/v1.0.1.zip) |
| Markdown | `chapters-en/` in this repository |
| Site | https://mhaghighian.github.io/MLSecOps/ |

---

## v1.0.0 — 2026-07-05

**MLSecOps Practical Reference Guide** — first stable release.

### Downloads

| Format | Link |
|--------|------|
| Source (ZIP) | [Source code (zip)](https://github.com/l4tr0d3ctism/MLSecOps/archive/refs/tags/v1.0.0.zip) — auto-generated by GitHub |
| Markdown | `chapters-en/` in this repository |
| Site | https://mhaghighian.github.io/MLSecOps/ |

Historical note: v1.0.0 also published optional DOCX/PDF assets; from **v1.1.1** onward, printable editions are built locally with `scripts/build-docx.py`.

### Highlights

- Ten lifecycle **control points** and **release decision** model (Ch.6)
- LLM, RAG, Agent, MCP, Shadow AI, SOC, and governance (Ch.7–11)
- Threat / control / tool mapping (Ch.12)
- Case studies and maturity roadmap (Ch.13–14)
- Production checklists and appendices (Ch.15)
- Kubernetes deployment reference (Ch.16)
- **Appendix E:** Implementation Reference — architecture cards, templates, playbooks

### Citation

See [CITATION.cff](CITATION.cff) or the **Cite this work** section in [README.md](README.md).

Full change history: [CHANGELOG.md](CHANGELOG.md).
