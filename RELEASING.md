# Releasing the Guide

Checklist for maintainers publishing **v1.1.1** and later versions.

**Current release:** v1.1.1 (2026-07-16)

Pre-built PDF/DOCX are **not** uploaded to GitHub Releases. Readers who need Word/PDF run `scripts/build-docx.py` locally.

---

## v1.1.1 release checklist

### Pre-release (content)

- [x] Issue #1 `References / Source mapping` restored after PR #3
- [x] Community review citation/content fixes retained
- [x] PDF/DOCX download links removed from site-facing docs
- [x] Version strings: README, TOC, Ch.1, CHANGELOG, CITATION.cff, CONTRIBUTING, GOVERNANCE, SECURITY, RELEASE_NOTES, releases README, `prepare_pages.py`

### Git

- [ ] Commit: `docs: release v1.1.1 — review fixes and Issue #1 restore`
- [ ] `git push origin main`
- [ ] `git tag -a v1.1.1 -m "MLSecOps Practical Reference Guide v1.1.1"`
- [ ] `git push origin v1.1.1`

### GitHub Release

1. Create release from tag **v1.1.1** (no PDF/DOCX assets)
2. Title: **v1.1.1 — MLSecOps Practical Reference Guide**
3. Body: copy from [releases/v1.1.1-RELEASE-BODY.md](releases/v1.1.1-RELEASE-BODY.md) or [RELEASE_NOTES.md](RELEASE_NOTES.md)

### Zenodo

1. Publish new version from tag `v1.1.1` on [Zenodo record](https://zenodo.org/records/21206781)
2. Confirm DOI landing page lists v1.1.1

### Post-release

- [ ] Verify GitHub Pages deploy (https://l4tr0d3ctism.github.io/MLSecOps/)
- [ ] Optional: announce in GitHub Discussions

---

## GitHub SEO (discoverability)

Based on GitHub + Google indexing best practices. Apply once per repo; refresh after major releases.

### 1. Repository name

| Current | Status |
|---------|--------|
| `MLSecOps` | Good — short, readable, primary keyword matches project brand |

Do not rename unless branding changes. The full title **MLSecOps Practical Reference Guide** lives in README, Pages, and releases.

### 2. About (Settings → General)

Copy-paste into **Description** (starts with main keyword; ~12 words):

```text
MLSecOps Practical Reference Guide — open-source AI and ML security handbook.
```

**Website:**

```text
https://l4tr0d3ctism.github.io/MLSecOps/
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

- [x] Site live: https://l4tr0d3ctism.github.io/MLSecOps/
- [x] `site_description` in `mkdocs.yml` (meta description for Google)
- [x] `robots.txt` + `sitemap.xml` on Pages deploy
- [x] Google Search Console HTML tag hook (`inject_google_verification.py`)

#### Google Search Console setup

1. **Property type:** URL prefix (not Domain)
2. **URL:** `https://l4tr0d3ctism.github.io/MLSecOps/`
3. **Verification method:** HTML tag
4. Google shows something like:
   ```html
   <meta name="google-site-verification" content="YOUR_CODE_HERE" />
   ```
5. Paste **only** `YOUR_CODE_HERE` (the `content` value) in **one** of:
   - **Option A (recommended):** GitHub → Settings → Secrets → Actions → `GOOGLE_SITE_VERIFICATION`
   - **Option B:** edit `seo/google-site-verification.code` (first line only) and push
6. Re-run **Deploy GitHub Pages** workflow (or push to `main`)
7. In Search Console click **Verify**
8. Submit sitemap: `https://l4tr0d3ctism.github.io/MLSecOps/sitemap.xml`
9. URL Inspection → home page → **Request indexing**

Note: you cannot add `github.com/l4tr0d3ctism/MLSecOps` to Search Console (not your domain). Use **GitHub Pages URL** only.

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
- [ ] Zenodo DOI updated
- [ ] Re-request indexing in Search Console for Pages home
- [ ] One announcement post with link to Pages (not only repo)

---

## Version numbering

| Tag | Meaning |
|-----|---------|
| `v1.0.0` | First stable public release (content scope frozen) |
| `v1.1.0` | Per-section traceability, mapping audit, Exchange integration, intro clarity |
| `v1.1.1` | Community review fixes, Issue #1 format restore, no packaged PDF/DOCX |
| `v2.0.0` | Lifecycle model or major structural change |

Document every release in [CHANGELOG.md](CHANGELOG.md).

---

## Build Word/PDF locally (optional)

```bash
# From repository root
python scripts/build-docx.py --render-mermaid
# Output: dist/MLSecOps-Practical-Reference-Guide-v1.1.1.docx
```

The build uses Pandoc with the Word **reference template** (`scripts/templates/reference.docx`, or auto-download from the v1.0.0 Release DOCX). Diagram PNGs are taken from `assets/diagrams/`; missing PNGs can be rendered from `assets/diagrams/source/*.mmd` with `--render-mermaid`. Export PDF from Word or Pandoc if required. Do not commit large binaries to `main`.

---

## General pre-release (any version)

- [ ] No new chapters unless planned for next minor/major
- [ ] Review [GETTING-STARTED.md](GETTING-STARTED.md) role-based paths
- [ ] Update [SECURITY.md](SECURITY.md) supported versions table
