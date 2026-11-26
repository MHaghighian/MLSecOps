# Changelog

All notable changes to the MLSecOps Reference Model & Practical Guide are documented here.

## [Unreleased]

### Added

- **Standards Conformance Profile (`MLS-*`), `in-toto` v1 / DSSE / Witness / Archivista & Controlled Benchmark** — added formal machine-verifiable `conformanceProfile` (`MLS-*` control IDs across Levels 1–3) to `schemas/evidence-pack.schema.json`; wrapped Evidence Packs in canonical `https://in-toto.io/Statement/v1` + **DSSE (`application/vnd.in-toto+json`)** via `schemas/mlsecops-attestation.v1.schema.json`, `schemas/dsse-envelope.v1.schema.json`, `--emit-intoto`, `--emit-dsse`, and `schemas/examples/intoto/` samples; added **Witness** (`in-toto/witness`) & **Archivista** (`in-toto/archivista`) policy/workflow ([`policies/witness/`](policies/witness/README.md) & [`references/INTOTO-WITNESS-ARCHIVISTA.md`](references/INTOTO-WITNESS-ARCHIVISTA.md)); added full cross-walks to `OWASP AISVS v1.0 (C1–C12)`, `CSA MAESTRO (L1–L7)`, `MITRE ATLAS`, `ISO/IEC 42001`, and `NIST AI RMF` in [`references/STANDARDS-ALIGNMENT.md`](references/STANDARDS-ALIGNMENT.md); extended scope to distributed `DDP`/`FSDP`/`RLHF`/`DPO` pretraining clusters in `Appendix E.1.8` + `trainingClusterConfig` + Rego rules; and added `scripts/eval_benchmark.py` + [`references/EVALUATION-BENCHMARK.md`](references/EVALUATION-BENCHMARK.md) (`11/11` adversarial recall, `0/5` FPR, `0.909 ms` median latency, `7/7` policy accuracy on deterministic CVE-pattern & benign/multilingual fixtures).
- **`scripts/ai_security_scan.py` & `tests/test_ai_security_scan.py`** — fast zero-dependency O(header)/O(N) static security scanner covering invisible Unicode Tag / Bidi smuggling (while preserving legitimate ZWNJ/ZWJ), NFKC homoglyph & HTML-comment obfuscated MCP tool poisoning, Shadow MCP unpinned `npx`/`uvx`/`bunx`/`pnpx`/`pipx`/`docker`/`podman` & shell execution (supporting `mcpServers`, VS Code `servers`, wildcard `autoApprove`/`alwaysAllow`/`dangerouslySkipPermissions`, and cross-map shadowing), decimal/octal/hex/IPv6 SSRF, cleartext endpoints & inline/URL secrets, canonical `mcpSchemaHashes` pinning/rug-pull verification (including Evidence Pack `mcpTools`), abstract VM stack+memo `pickletools` Protocol 0–5 disassembly (catching `MEMOIZE`/`BINGET`/`BINUNICODE8` & `asyncio`/`marshal` `CVE-2025-10157` gadgets), ZIP polyglots, Local/Central filename spoofing (`CVE-2025-1945`), CRC-32 anomalies (`CVE-2025-10156`), disguised extensionless archive pickles, TorchScript `.py`, Keras `Lambda`, HuggingFace `auto_map` / Jinja2 SSTI (`|attr()` bypasses), bounded binary GGUF KV walking beyond 64 KB (`CVE-2024-34359`), varint-safe ONNX `external_data` path traversal (`CVE-2024-5187`), NumPy `.npy` object pickles (`CVE-2019-6446`), symlink/malformed-JSON guards, and Safetensors buffer overlap/OOB validation.
- **Deeper Rego & K8s detection rules** — `policies/cp8_cp9_admission.rego` enforces `sharedResponsibilityRecord` owners, `CP7` quantitative gates (`agentMisalignmentScore <= 0.15`, `redTeamPhasesCompleted >= 4`), `dataProvenance` PII/backup-revocation, `localRunnerConfig` TCP isolation (`E.1.7`), `runtimeTelemetry.rawPromptLoggingDisabled`, case-insensitive `aisbom:unreadable`, multi-model-compatible CycloneDX `components` SHA-256 format/weak-hash denial, OWASP `ASI02`/`ASI03` `intentGateEnabled`, `ASI06` `memoryProvenanceVerified`, `ASI07`/`ASI08` `delegationDepthMax <= 4`, capped MCP sampling, and SSRF/cleartext-endpoint/shadowed `serverName` checks; `policies/k8s/inference_workload.rego` adds `--trust-remote-code`, plaintext env & CLI-arg token secrets, container-level `runAsUser: 0`/`runAsNonRoot: false`/`seccompProfile: Unconfined`/`procMount: Unmasked`/non-`NET_BIND_SERVICE` caps override protection, `--allowed-local-media-path` root LFI protection, `hostNetwork`/`hostPID`/`hostIPC`/`hostPath`/`hostPort`, non-empty `vLLM` `VLLM_API_KEY`/`--api-key` auth, public `LoadBalancer`/`NodePort`/`externalIPs` `Service` exposure blocking, `readOnlyRootFilesystem`, and `resources.limits.memory`.

### Changed

- **QA & performance refactoring** — refactored `scripts/verify_repo.py` to single-pass HTML parsing (~2x fewer BeautifulSoup passes), pre-normalized `.mmd` lookup, strict stdlib RFC-3339 `date-time` checking, `CITATION.cff`/`mkdocs.yml`/`prepare_pages.py` version sync, automated `tests/` discovery, and added `minLength`/`timestamp` pattern + `runtimeAgentConfig` `ASI02`/`ASI06`/MCP transport fields in `schemas/evidence-pack.schema.json`.
- **ISO/IEC 27090:2026 primary standards elevation & peer comparison** — elevated **ISO/IEC 27090:2026** (*Cybersecurity — AI — Addressing security threats and compromises to AI systems*, Clauses `5–7` and `Annexes A–C`) as the primary technical AI security baseline ahead of OWASP where scope overlaps (across `README.md`, `GETTING-STARTED.md`, Chapters `1–12`, `14`, and [Chapter 15 Appendix](chapters-en/15-conclusion-appendix.md#appendix-isoiec-270902026-clause-cross-reference)), while crediting `OWASP AI Exchange` as an open contributor/companion and adding a transparent comparison table + limitations section to `README.md`.
- **Full repository documentation alignment** — added [`scripts/README.md`](scripts/README.md) (documenting every `MCP-*`/`MODEL-*` scanner rule and verification workflow); expanded [`schemas/`](schemas/README.md) (`evidence-pack.schema.md`, `evidence-pack.example.md`) and [`policies/`](policies/README.md) (`cp8_cp9_admission.md`, `policies/k8s/README.md`) rule tables; updated `README.md`, `GETTING-STARTED.md`, `CONTRIBUTING.md`, `DESIGN.md`, `SECURITY.md`, `GOVERNANCE.md`, `RELEASING.md`, `RELEASE_NOTES.md`, `RELEASE-INTEGRITY.md`, `releases/v1.4.0-RELEASE-BODY.md`, `releases/README.md`, PR/issue templates, and Chapters 5, 7, 8, 11, 12, 16, and 17 to match all executable schemas, policies, and static checks cleanly.
- **Repo root cleanup** — removed `promotion/` (Medium draft out of scope for the reference model tree); moved Search Console assets from `seo/` to `.github/seo/` (updated Pages/`prepare_pages`/`inject_google_verification`/manifest/`RELEASING.md`); ignore local `_log_*/` build leftovers.

## [1.4.0] — 2026-11-25

### Added

- **Vector DB backup / snapshot revocation** — Ch.4 embedding leakage: data revocation must cover replicas, cold backups, snapshots, and caches (classification vs DLP clarified); Ch.7 Reindex Playbook extended for revoke + offline-copy purge.
- **Docker Model Runner / OCI model artifacts** — Ch.5 distribution-layer controls; Appendix E.1.7 developer-local architecture card (+ `_e17.mmd`/`.png`); Ch.12 CP 7 local OpenAI-compatible runners; Ch.16 explicit DMR ≠ K8s serving; Ch.2/Ch.11 cross-links for threat model and Shadow AI hygiene.
- **`schemas/`** — machine-readable Evidence Pack JSON Schema (`evidence-pack.schema.json`, Draft 2020-12, CycloneDX 1.6/1.7-aligned themes) with `Agentic-MCP` (`evidence-pack.example.json`) and `Managed-API` (`evidence-pack.managed-api.example.json`) examples, plus typed `dataProvenance`, `localRunnerConfig`, and `runtimeTelemetry` sections.
- **`policies/`** — OPA/Conftest admission samples (`cp8_cp9_admission.rego` + `cp8_cp9_admission_test.rego` unit tests + negative fixtures) and Kubernetes inference workload hardening suite (`policies/k8s/inference_workload.rego` + unit tests + YAML fixtures).
- **Tooling & CI** — `dependency-audit.yml` (`pip-audit`); `handbook-artifacts.yml` attaches DOCX/PDF (+ checksums) on `v*.*.*` tags without prematurely publishing draft releases; `docs-check.yml` validates JSON Schema (`check-jsonschema` + `jsonschema`) and runs SHA-256-pinned Conftest (`v0.71.1`) via `scripts/verify_repo.py`.
- **Content** — CP8↔CP9 TOCTOU / hard admission guidance; binary-header supply-chain note (Ch.5); cross-model KV reuse (Ch.7); agent-as-insider-threat (Ch.8); SOC active-defense note (Ch.10); machine-readable Evidence Pack (Ch.11); GenAI red-team phases (Ch.12); OpenSSF personas + PQC roadmap note (Ch.14); admission digest bind (Ch.16).

### Changed

- **Reference Model identity & framing** — repositioned the project across `README.md`, `GETTING-STARTED.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`, `CITATION.cff`, `mkdocs.yml` (`site_name` and full sidebar navigation including `Reference Artifacts` & `Project` sections), `.github/prepare_pages.py`, `scripts/build-docx.py`, `references/AARM-ALIGNMENT.md`, Ch.1, Ch.2, Ch.15, `TABLE-OF-CONTENTS.md`, `RELEASING.md`, and `promotion/` as **MLSecOps Reference Model & Practical Guide** (retaining explicit *not official OWASP/NIST/ISO/OpenSSF* and *not legal advice* boundaries).
- **`Operational & scope notes` convention** — replaced `Author practical guidance` blocks across chapters with `Operational & scope notes`, updated Ch.15 source-traceability conventions, and removed self-deprecating disclaimers.
- **`schemas/` & `policies/` hardening** — enforced Draft 2020-12 `allOf` conditionals (`Managed-API` requires `managedApiConfig.configSnapshotHash`; non-managed scopes require `modelArtifact.sha256Digest`; `Agentic-MCP` requires `runtimeAgentConfig` with `killSwitchEnabled` & `scopedCredentialsRequired`); switched `policies/cp8_cp9_admission.rego` to `package main` (matching Conftest CLI defaults), enforced blocking `CP4`/`CP7`/`CP8` statuses, regex-checked SHA-256 digest formats and non-placeholder `signatureMethod`, and closed `undefined` fail-open paths (`metadata.systemScope`, `boundToCp9Digest`, `currentSchemaHash`, `scopedCredentialsRequired`).
- **`scripts/generate_release_manifest.py` & `scripts/build-docx.py`** — extended `SHA256SUMS` coverage to `scripts/*.py`, `scripts/templates/README.md`, `assets/javascripts/*.js`, `promotion/*.md`, `releases/*.md`, `seo/*`, `.github/workflows/*.yml`, `.github/*.py`, `RELEASING.md`, and `RELEASE_NOTES.md`; added SHA-256 digest verification for template downloads in `scripts/build-docx.py` and updated default output naming to `MLSecOps-Reference-Model-v{version}.docx`.
- **Diagrams & build pipeline** — added Appendix `E.1.7` diagram (`_e17.mmd`/`.png`), aligned `_06.mmd`/`.png` to `CP4`/`CP7`/`CP8` -> `CP9`, added dark-mode (`slate`) and `securityLevel: "strict"` support in `assets/javascripts/mermaid-init.js` (UTF-8 BOM removed), deduplicated Mermaid+PNG rendering in `.github/prepare_pages.py` and `scripts/build-docx.py`, and hardened `handbook-artifacts.yml` (`--with-deps chromium` and `gh release upload`/`--draft`).
- **RELEASING / DESIGN / SECURITY / RELEASE-INTEGRITY** — aligned PDF/DOCX CI attachment policy across `README.md`, `RELEASE-INTEGRITY.md`, `releases/README.md`, and `DESIGN.md`; updated `SECURITY.md` supported versions table for `v1.4.0`; kept dependency monitoring on **`pip-audit`** (Dependabot auto-PRs disabled after #27/#35).

### Fixed

- **Release workflow & history fixes** — fixed `.github/workflows/release.yml` (`SHA256SUMS.sigstore.json` filename reference and tag-scoped changelog extraction), restored missing `## v1.1.0` heading in `RELEASE_NOTES.md`, restored missing `## v1.1.3` entry and fixed wrong `v1.0.1` Zenodo DOI (`10.5281/zenodo.21206781`) in `releases/README.md`, and set `edit_uri: ""` in `mkdocs.yml`.
- **Links, anchors, TOC & cross-references** — normalized `--` to `-` heading anchors in `.github/prepare_pages.py`, fixed broken internal/external links across chapters and docs, completed `TABLE-OF-CONTENTS.md`, placed Appendix `E.1.7` ahead of `E.1` References and added `E.4` YAML-to-JSON mapping in Ch.17, synced `RELEASING.md` and `README.md`, and resolved content mismatches in Ch.1, Ch.11, Ch.12, Ch.15, and Ch.16.

## [1.3.0] — 2026-10-22

### Added

- **NIST Cyber AI Profile (IR 8596 iprd)** — CSF 2.0 Community Profile mapping for Secure themes: Ch.11 section, Ch.15 appendix card, Ch.5 AI SBOM/`GV.SC-02` note, Ch.8 AI NHI/least privilege (`PR.AA`), Ch.10 four-way AI traffic classes + IR metadata (dataset/hyperparams), academic CTI (`ID.RA-02`). Explicitly labeled preliminary draft — not a certification claim.
- **Ch.12 L6** — clarify NeMo Guardrails vs Meta Llama Guard vs Guardrails Hub LlamaGuard7B (archived hub repo).

### Changed

- **Release decision wording** — normalize across README, Getting Started, Ch.1–2, Ch.6, Appendix E: blocking release decisions at **4, 7, 8** (7 at Level 2+); mandatory integrity checkpoint at **9** before store/deploy (not conflated as a fourth “release decision” of the same type).
- **SOC / baseline privacy** — co-locate privacy-aware prompt/response handling with MUST telemetry (Ch.6 minimum baseline, Ch.10 SOC prioritization and “only three controls”).
- **Navigation fixes** — Ch.7 TOC (dedupe MCP; add LLM verification); fix Level 1 and AI Compute Hijacking internal anchors.
- **Scope clarity** — handbook ≠ bundled CI product (Getting Started + README Implementation Reference note).
- **Dependencies** — disable Dependabot (remove `.github/dependabot.yml`); track Action/pip bumps manually via maintainer PRs.
- **OpenSSF Best Practices** — earned [Passing](https://www.bestpractices.dev/projects/15668) (Metal) and [baseline-2](https://www.bestpractices.dev/projects/15668); README embeds both badges separately. Scorecard intentionally not used (documentation handbook).
- **Baseline-2 readiness** — DCO (`DCO.md` + PR check), dependency/build docs in `CONTRIBUTING.md`, member/roles in `GOVERNANCE.md`, `DESIGN.md`, release integrity (`RELEASE-INTEGRITY.md` + manifest script + signed `SHA256SUMS` in Create Release workflow), expanded `SECURITY.md` (CVD public disclosure, secrets, repo security assessment).

### Clarified (same version — reader confusion pass)

- **Getting Started** — terms card (CP vs Level vs Evidence Pack), framework order, role paths (5 links each), Level 1 vs Level 2+ baselines split so production MUST is not mixed with foundational.
- **CP8 vs CP9 order** — Appendix E.2 flow diagram/table corrected (release decisions → integrity checkpoint → deploy); Ch.6 decision card + Stage→control-point wording; Ch.1 / README / Ch.2 / Ch.11 policy examples aligned.
- **Glossary** — `Control point`, `Release decision`, `Integrity checkpoint`, `Maturity Level`; `Baseline` (metrics) ≠ minimum security baseline.
- **NeMo / Llama Guard / Hub** — three-way distinction in Ch.12 skim tables + Ch.15 tool list.
- **NIST IR 8596 map** — stronger iprd / non-certification lead-in; release row includes CP7; CP9 separated from Evidence Pack/AI-BOM themes.
- **Filled Evidence Pack sample** — Appendix E.4 managed RAG example.
- **Ch.14 starting controls / Level tables** — CP 9 managed-API alternative; TOC disambiguates repeated “Secure by design” / “Practical principle” labels.

### Citation

- Cite via concept DOI [10.5281/zenodo.21206780](https://doi.org/10.5281/zenodo.21206780) until a version-specific Zenodo DOI is minted for v1.3.0.

## [1.2.1] — 2026-08-15


### Changed

- **Citation / Zenodo** — version DOI [10.5281/zenodo.21950241](https://doi.org/10.5281/zenodo.21950241) for v1.2.1 (concept DOI [10.5281/zenodo.21206780](https://doi.org/10.5281/zenodo.21206780)).

- **Diagrams** — restore inline Mermaid fences from `assets/diagrams/source/*.mmd` alongside PNG fallbacks (29 diagrams); enable Mermaid rendering on MkDocs Pages. Appendix E `_10`–`_21` remain SVG/PNG-first (no `.mmd`).

## [1.2.0] — 2026-08-15

### Changed

- **Citation / Zenodo** — version DOI [10.5281/zenodo.21946726](https://doi.org/10.5281/zenodo.21946726) for v1.2.0 (concept DOI [10.5281/zenodo.21206780](https://doi.org/10.5281/zenodo.21206780)).

- **Appendix E.7.3 Example C** — deepen secure-by-design composition: caller→engine authN (not "to the GPU"); gateway serve-path authZ; gateway-**overwritten** vLLM `cache_salt` (`CVE-2025-46570` / ≥ 0.9.0); safetensors allowlist with ModelScan on legacy formats; fail-closed admit + Kyverno HA; LoRA↔`base_model_digest`; MIG K8s-vs-VM wording; MPS not isolation; LeftoverLocals NVIDIA nuance + KV/VRAM hygiene; credential lifecycle; telemetry without raw prompts. Regenerated diagrams `_16`–`_18`.

- **Appendix E.7.3 / Ch.7 — gateway + prefix-cache trust break** — engine key ≠ tenant PEP; omit `cache_salt` ⇒ global share even on vLLM ≥ 0.9.0; stable (not per-request) gateway-overwritten salt; reuse isolation ≠ capacity isolation; prefer crypto-safe prefix hash on shared replicas. Sources: vLLM prefix-caching docs, cache-salting RFC #16016, `CVE-2025-46570`.

## [1.1.3] — 2026-07-26

### Added

- **Ch.7 — KV Cache security** — Transformer KV Cache primer (not a separate AI product); direct reconstruction threats (Inversion / Collision / Injection, **KV-Cloak**) vs cross-tenant prefix timing (**PromptPeek**); Cache-Augmented Generation (`CAG`) relation and durable-cache controls; maturity-labeled control table; cross-links from multi-tenant sections, Appendix E.1.3, and Ch.16 GPU isolation. Citations: Luo et al. NDSS 2026, Wu et al. NDSS 2025, Chan et al. 2024 (`CAG`).
- **Site / maintainer link** — documentation site footer and home page link to [mhsec.me](https://mhsec.me).

## [1.1.2] — 2026-07-25

### Added

- **Ch.7 — Prompt injection defenses: from filters to architecture** — L0–L3 defense layers (runtime filter, instruction hierarchy, spotlighting, Dual-LLM / structural patterns, IFC/capability); citations to Wallace et al. (2024), Hines et al. (2024), Willison (2023), Debenedetti et al. CaMeL (2025), Beurer-Kellner et al. design patterns (2025), Costa et al. FIDES (2025), AgentDojo (2024).
- **Secure by design sections (Ch.1, 4, 7, 8)** — authorization- and output-channel defaults complementing the prompt-injection defense layers: assume-injection axiom and authorization-outside-the-model (Ch.1); no-direct-data-store-credentials / authorizing-service pattern (Ch.4); identity propagation with credential insulation, model-controlled-parameter constraints, intra-tenant vector-store RLS pre-filter, and zero-egress rendering (Ch.7); agent-never-selects-its-own-scope (delegated / NHI identity), credential insulation at the tool boundary, orchestrator-driven approval surface, and structurally-bounded autonomy (Ch.8); Appendix E.1.1 intra-tenant RLS access-model row and E.1.4 identity/data-access row; TOC Ch.8 title restored. Mapped to OWASP `LLM01`/`LLM02`/`LLM06`/`LLM08`, OWASP Top 10 for Agentic Applications (`ASI02`/`ASI03`/`ASI08`/`ASI09`), OWASP Non-Human Identities Top 10, RFC 8693, MITRE ATLAS, CSA AARM, and EchoLeak (`CVE-2025-32711`). ([PR #5](https://github.com/MHaghighian/MLSecOps/pull/5) by [@ariangh001](https://github.com/ariangh001))
- **Tool maturity labels** (`Mature` / `Emerging` / `Research/Lab`) in Ch.11–12 MCP/gateway tables; Evidence Pack MCP control worded as capability (static scan report), not a single product name.

### Changed

- Ch.8 agent defense layers and Ch.9 anti-patterns: detect-only injection defense called out; Appendix E.1.4 / threat-model template aligned.
- Ch.15 bibliography and production checklist updated for design-level PI refs and MCP scan capability wording.

### Fixed

- **GitHub Pages / sitemap URLs** — after account rename, `site_url`, `robots.txt`, and docs links now use `https://mhaghighian.github.io/MLSecOps/` (the old `l4tr0d3ctism.github.io` host 404s and broke Search Console sitemap reads).

## [1.1.1] — 2026-07-16

### Fixed

- **Issue #1 reference blocks restored** — expanded compacted `> *Refs - …*` lines from PR #3 back to per-section `### References / Source mapping` blocks across Chapters 1–17, keeping the corrected framework IDs and content from that review.

### Changed

- Community review merge ([PR #3](https://github.com/MHaghighian/MLSecOps/pull/3) by [@Ali-Razmjoo](https://github.com/Ali-Razmjoo)): citation fixes (ATLAS/OWASP IDs), scope clarifications, Evidence Pack / maturity wording, Stage 3 naming, Ch.6 worked example, and related chapter edits.
- **Release packaging** — PDF and DOCX are no longer attached to GitHub Releases or linked from the site; generate locally with `scripts/build-docx.py` when needed.

### Removed

- **GUIDE-SUMMARY.md** and related summary navigation/links from README, GETTING-STARTED, MkDocs, and GitHub Pages.
- Pre-built **PDF / DOCX** download links from README, Getting Started, and release pages (build script remains).

### Added

- **[references/AARM-ALIGNMENT.md](references/AARM-ALIGNMENT.md)** — complementary mapping to CSA AARM (Autonomous Action Runtime Management); links from Ch.8 and GETTING-STARTED.

## [1.1.0] — 2026-07-11

### Added

- **Per-section traceability (Issue #1)** — `References / Source mapping` blocks on every major `##` section across Chapters 1–17; [traceability convention](chapters-en/15-conclusion-appendix.md#traceability-and-source-mapping-convention) in Ch.15; CONTRIBUTING/GOVERNANCE expectations updated.
- **OWASP AI Exchange integration** — complementary positioning and per-section source mapping where applicable: Ch.1 Exchange relationship; Ch.2 AI inventory + risk workflow; Ch.5 poisoning taxonomy + model theft paths; Ch.6 three test categories; Ch.7 augmentation data, downstream injection, verification gaps; Ch.12 periodic table cross-ref; `GETTING-STARTED.md` resource selector; Ch.15 Exchange citation.
- **Ch.1 — Why this guide matters** — explicit reader value proposition, learning outcomes, and practical takeaways ([Issue #2](https://github.com/MHaghighian/MLSecOps/issues/2)).
- **Ch.1 — Guide at a glance** — audience, goal, outputs, and scope summary after Abstract.

### Changed

- **Ch.1** — intro polish: transition sentence, split paragraphs, lifecycle lead-in, wording fixes per community review.
- **Ch.1–17** — framework source mapping audit: OWASP LLM/ML Top 10 IDs, MITRE ATLAS techniques, NIST AI RMF, ISO/IEC 42001, OpenSSF, and OWASP AI Exchange permalinks aligned to section topics.
- **GETTING-STARTED.md** — Quick Start (5 Minutes), *New to AI Security?* path, renamed production baseline section, *When to use this guide vs. OWASP AI Exchange*.
- **TABLE-OF-CONTENTS.md** — Ch.1 entries for *Why this guide matters* and *What this guide adds*; traceability convention; Exchange-related sections (Ch.1–2, 5–7, 12).
- **Ch.7** — removed duplicate augmentation block under Ingest security (cross-ref only).
- **Ch.12 / Ch.15 Appendix B** — MITRE ATLAS table synchronized (`AML.T0066`, `AML.T0034`).
- **Ch.13** — LangChain case study: added CVE-2025-68664 alongside CVE-2025-27520.
- **prepare_pages.py** — rewrite anchored `GETTING-STARTED.md#…` links for MkDocs; site index banner v1.1.0.
- **README.md** — OWASP AI Exchange in frameworks list; version and download links v1.1.0.
- Version strings aligned to **v1.1.0** across Ch.1, TOC, README, CITATION.cff, CONTRIBUTING, GOVERNANCE, SECURITY, RELEASE_NOTES, and releases README.

## [1.0.1] — 2026-07-05

### Added

- **Zenodo DOI** [10.5281/zenodo.21206781](https://doi.org/10.5281/zenodo.21206781) for long-term citation.
- **Zenodo archival release** — no guide content changes; triggers DOI after GitHub–Zenodo integration.

## [1.0.0] — 2026-07-05

### Added

- **GitHub Release v1.0.0** with DOCX and PDF (`MLSecOps Practical Reference Guide`).
- Printable editions aligned with markdown source (16 chapters + Appendix E).
- **Diagram PNG assets** in `assets/diagrams/` (26 static Mermaid exports).

### Changed

- Version bump from **v0.1.2** (public beta) to **v1.0.0** — content scope frozen for citation.
- README, TOC, and site banner aligned to v1.0.0.

## [0.1.2] — 2026-07-05

### Added

- **GitHub Pages** documentation site: https://mhaghighian.github.io/MLSecOps/ (MkDocs Material, Mermaid).
- Public-beta README restructure: Getting Started, Downloads, Community feedback, Releases docs.
- [GETTING-STARTED.md](GETTING-STARTED.md), [RELEASING.md](https://github.com/MHaghighian/MLSecOps/blob/main/RELEASING.md), [releases/README.md](https://github.com/MHaghighian/MLSecOps/blob/main/releases/README.md).
- **Chapter 16** Kubernetes deployment reference.
- **Appendix E: Implementation Reference** — architecture cards, decision matrix, threat model template, Evidence Pack template, playbooks, master control matrix.
- **How to use this guide** (Ch.1) and role-based Quick Start (README, docs site).
- **Managed AI services security reference** (Ch.2) and **Appendix D** checklist with Evidence Pack fields.
- **Agent chapter priority 2:** think–act cycle, conversation manipulation, exfiltration model, defense layers, secure lifecycle, KPIs.
- **LLM verification approach** (Ch.7) complementing OWASP LLMSVS.
- **Positioning:** *MLSecOps Practical Reference Guide*; **What this guide adds** in Ch.1 and Final Conclusion (four operational contributions).
- GitHub Actions workflows: `pages.yml`, manual `release.yml` (v1.0+).

### Changed

- README: live documentation site link; contributor and governance docs updated.
- MkDocs site built in CI from `chapters-en/` (removed committed `docs/` tree).
- **Chapter 3** condensed: demonstrated threats first; emerging topics in summary table (~450 → ~170 lines).
- Ch.12 tool commands relabeled as optional appendix; Ch.12 reading note: primary mapping vs optional CLI appendix.
- Removed `examples/` directory; Ch.16 points to upstream vendor references only.
- README, TOC, and citation text aligned with Practical Reference Guide positioning.

### Fixed

- Unified lifecycle terminology across Ch.1, 6, 9, 11, 15, 16 (`control points`, `release decisions`, `Integrity and Provenance`).
- Appendix order in Ch.15 (A → B → D).

## [0.1.1] — 2026-06-21

### Fixed

- Canonical **policy gate** model (stages 4, 7, 8) vs integrity checkpoint (stage 9); resolved minimum-baseline contradictions.
- **OWASP LLM04** vs **LLM08** mapping for retrieval/RAG corpus poisoning (Appendix A, Claims table).
- **MITRE ATLAS** AI worm mapping (no false 1:1 ID with memory poisoning).
- Softened non-standard overclaims in conclusion; clarified **OpenSSF** relationship (independent, non-affiliated guide).
- Case study citations and **Documented incident** vs **Illustrative pattern** labels.
- Removed unverified tool reference (`BlackVault`); privacy/GDPR section for prompt logging; Feature Store, LoRA/PEFT, MCP sections.
- Maturity Level 3 criteria (process-based, not “zero incidents”); ethics box in Chapter 3.

### Added

- `examples/evidence-pack-schema.json` — starter Evidence Pack schema.
- `GOVERNANCE.md`, `CHANGELOG.md`.

## [0.1.0] — 2026-06

Initial public draft: 15 chapters, MkDocs site, threat/control mapping, maturity roadmap.
