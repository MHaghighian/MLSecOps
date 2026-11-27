# Releasing the MLSecOps Reference Model & Practical Guide

Checklist for maintainers publishing **v1.5.0** and later versions.

**Current release:** v1.5.0 (2026-11-27)

Pre-built **DOCX** (and **PDF** when conversion succeeds) are attached automatically by the **Handbook Artifacts** workflow (`.github/workflows/handbook-artifacts.yml`) when a `v*.*.*` tag is pushed, or via that workflow’s `workflow_dispatch`. Readers can still build locally with `scripts/build-docx.py --render-mermaid` if needed.

### Release integrity (required for new official releases)

1. Prefer an annotated **signed** tag when GPG is configured: `git tag -s vX.Y.Z -m "…"`.  
2. Generate `SHA256SUMS` for the tagged tree:

```bash
python scripts/generate_release_manifest.py -o SHA256SUMS
```

3. Sign the manifest (maintainer GPG **or** cosign in the Create Release workflow):

```bash
gpg --detach-sign -a SHA256SUMS
# → SHA256SUMS.asc
```

4. Attach `SHA256SUMS` + signature to the GitHub Release.  
5. Readers verify per [RELEASE-INTEGRITY.md](RELEASE-INTEGRITY.md).

The **Create Release** workflow generates `SHA256SUMS` and a cosign keyless signature when publishing.

---

## v1.5.0 release checklist

### Pre-release (content & verification)

- [x] `ISO/IEC 27090:2026` primary standards elevation, `MLS-*` Conformance Profile (`references/STANDARDS-ALIGNMENT.md`), `in-toto` v1 / DSSE / Witness / Archivista (`schemas/`, `policies/witness/`, `references/INTOTO-WITNESS-ARCHIVISTA.md`), `Pretraining-Distributed` (`E.1.8`), hardened `scripts/ai_security_scan.py`, and controlled benchmark (`scripts/eval_benchmark.py` / `references/EVALUATION-BENCHMARK.md`)
- [x] Version strings synced to `v1.5.0` (`CITATION.cff`, `mkdocs.yml`, `.github/prepare_pages.py`, docs, chapters)
- [ ] Run `python scripts/verify_repo.py --require-conftest --with-mkdocs` and confirm 0 findings from `ai_security_scan.py` before tagging

### Git

- [ ] Push `main` with DCO-signed commits (`git push origin main`)
- [ ] `git tag -s v1.5.0 -m "MLSecOps Reference Model & Practical Guide v1.5.0"`
- [ ] `git push origin v1.5.0`

### GitHub Release

1. Create release from tag **v1.5.0** (integrity assets via Create Release workflow; handbook DOCX/PDF attached to draft via Handbook Artifacts workflow)
2. Title: **MLSecOps v1.5.0 — MLSecOps Reference Model & Practical Guide**
3. Body: [releases/v1.5.0-RELEASE-BODY.md](releases/v1.5.0-RELEASE-BODY.md)
4. Verify `SHA256SUMS` + `SHA256SUMS.sigstore.json` and handbook assets on the draft release, then click **Publish release**.

### Zenodo

1. Auto via GitHub webhook on release publish
2. Sync version DOI into README / CITATION if a new record appears

### Post-release

- [ ] Verify GitHub Pages (Mermaid + PNG)
- [ ] Confirm release URL

---

## GitHub SEO (discoverability)

Based on GitHub + Google indexing best practices. Apply once per repo; refresh after major releases.

### 1. Repository name

| Current | Status |
|---------|--------|
| `MLSecOps` | Good — short, readable, primary keyword matches project brand |

Do not rename unless branding changes. The full title **MLSecOps Reference Model & Practical Guide** lives in README, Pages, and releases.

### 2. About (Settings → General)

Copy-paste into **Description** (starts with main keyword; ~12 words):

```text
MLSecOps Reference Model & Practical Guide — open-source AI and ML security architecture.
```

**Website:**

```text
https://mhaghighian.github.io/MLSecOps/
```

### 3. Topics (Settings → General → Topics)

Add all (GitHub allows up to 20):

```text
mlsecops
ai-security
llm-security
machine-learning-security
devsecops
mlops-security
cybersecurity
owasp
secure-ai
rag-security
agentic-ai
supply-chain-security
nist-ai-rmf
mitre-atlas
open-source
documentation
kubernetes
```

### 4. README (done in repo)

- [x] Keyword-rich opening paragraph (`MLSecOps`, AI security, LLM, RAG, DevSecOps)
- [x] Official links table (Pages, repo, release, DOI)
- [x] Topics covered + FAQ sections
- [x] Descriptive image alt text
- [x] Share / backlink note for promotion

### 5. GitHub Pages (Google indexing)

- [x] Site live: https://mhaghighian.github.io/MLSecOps/
- [x] `site_description` in `mkdocs.yml` (meta description for Google)
- [x] `robots.txt` + `sitemap.xml` on Pages deploy
- [x] Google Search Console HTML tag hook (`inject_google_verification.py`)

#### Google Search Console setup

1. **Property type:** URL prefix (not Domain)
2. **URL:** `https://mhaghighian.github.io/MLSecOps/`
3. **Verification method:** HTML tag
4. Google shows something like:
   ```html
   <meta name="google-site-verification" content="YOUR_CODE_HERE" />
   ```
5. Paste **only** `YOUR_CODE_HERE` (the `content` value) in **one** of:
   - **Option A (recommended):** GitHub → Settings → Secrets → Actions → `GOOGLE_SITE_VERIFICATION`
   - **Option B:** edit `.github/seo/google-site-verification.code` (first line only) and push
6. Re-run **Deploy GitHub Pages** workflow (or push to `main`)
7. In Search Console click **Verify**
8. Submit sitemap: `https://mhaghighian.github.io/MLSecOps/sitemap.xml`
9. URL Inspection → home page → **Request indexing**

Note: you cannot add `github.com/MHaghighian/MLSecOps` to Search Console (not your domain). Use **GitHub Pages URL** only.

### 6. Stars, watchers, forks (social proof)

GitHub ranks repos partly on engagement. Promote via:

| Channel | Suggested post angle |
|---------|---------------------|
| LinkedIn | MLSecOps practical guide — LLM/RAG/agent security + lifecycle controls |
| Dev.to / Medium | Tutorial-style post linking to Ch.7 or Appendix E |
| Reddit | r/cybersecurity, r/MachineLearning, r/netsec (follow sub rules) |
| OWASP community | AI security / LLM Top 10 threads — cite, do not spam |
| Hacker News | `Show HN: MLSecOps Practical Reference Guide` (once, when ready) |
| GitHub Discussions | Announce release with link to Pages + source |

Quality content drives stars; promotion amplifies discoverability.

### 7. Post-release SEO check

After each release:

- [ ] README version badge and download links updated
- [ ] GitHub Release published (tags help indexing)
- [ ] Zenodo version DOI (mint after release; cite concept 10.5281/zenodo.21206780 until then)
- [ ] Re-request indexing in Search Console for Pages home
- [ ] One announcement post with link to Pages (not only repo)

---

## Version numbering

| Tag | Meaning |
|-----|---------|
| `v1.0.0` | First stable public release (content scope frozen) |
| `v1.1.0` | Per-section traceability, mapping audit, Exchange integration, intro clarity |
| `v1.1.1` | Community review fixes, Issue #1 format restore, no packaged PDF/DOCX |
| `v1.1.2` | Secure by design (Ch.1/4/7/8), PI L0–L3 defenses, tool maturity labels |
| `v1.1.3` | KV Cache security (Ch.7), CAG/KV-Cloak notes, mhsec.me on docs site |
| `v1.2.0` | Example C secure-by-design hardening (authZ, cache_salt, MIG/MPS/LeftoverLocals) |
| `v1.2.1` | Restore inline Mermaid diagrams + MkDocs Mermaid render |
| `v1.3.0` | NIST Cyber AI Profile (IR 8596 iprd) mapping, release-gate/privacy/nav integrity, OpenSSF baseline-2 |
| `v1.4.0` | Reference Model & Practical Guide identity, CycloneDX 1.6/1.7 Evidence Pack schemas (`schemas/`), OPA/Conftest policies (`CP4`/`CP7`/`CP8`/`CP9` + `policies/k8s/`), zero-dep static MCP/model scanner (`scripts/ai_security_scan.py` + `tests/`), DMR/Vector DB revocation, hardened CI/QA/release workflows |
| `v1.5.0` | ISO/IEC 27090:2026 primary baseline, `MLS-*` Conformance Profile + OWASP AISVS/MAESTRO/ISO 42001/ATLAS crosswalks, `in-toto` v1 + DSSE + Witness + Archivista, `Pretraining-Distributed` (`E.1.8`), deepened pickle/GGUF/ZIP/ONNX/MCP09 scanner, and controlled benchmark (`eval_benchmark.py`) |
| `v2.0.0` | Lifecycle model or major structural change |

Document every release in [CHANGELOG.md](CHANGELOG.md).

---

## Build Word/PDF (CI default; local optional)

```bash
# From repository root
python scripts/build-docx.py --render-mermaid
# Output: dist/MLSecOps-Reference-Model-v1.5.0.docx
```

The build uses Pandoc with the Word **reference template** (`scripts/templates/reference.docx`, or auto-download from the v1.0.0 Release DOCX). Diagram PNGs are taken from `assets/diagrams/`; missing PNGs can be rendered from `assets/diagrams/source/*.mmd` with `--render-mermaid`. Export PDF from Word or Pandoc if required. Do not commit large binaries to `main`.

---

## General pre-release (any version)

- [ ] No new chapters unless planned for next minor/major
- [ ] Review [GETTING-STARTED.md](GETTING-STARTED.md) role-based paths
- [ ] Update [SECURITY.md](SECURITY.md) supported versions table
