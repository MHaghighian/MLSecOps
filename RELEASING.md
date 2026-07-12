# Releasing the Guide

Checklist for maintainers publishing **v1.1.0** and later versions.

**Current release:** v1.1.0 (2026-07-11)

---

## v1.1.0 release checklist

### Pre-release (content)

- [x] Per-section `References / Source mapping` across Chapters 1–17 ([Issue #1](https://github.com/l4tr0d3ctism/MLSecOps/issues/1))
- [x] OWASP AI Exchange complementary integration
- [x] Ch.1 reader value / guide at a glance ([Issue #2](https://github.com/l4tr0d3ctism/MLSecOps/issues/2))
- [x] Version strings: README, TOC, Ch.1, CHANGELOG, CITATION.cff, CONTRIBUTING, GOVERNANCE, SECURITY, RELEASE_NOTES, releases README, `prepare_pages.py`
- [ ] Run internal link validation in local build workspace
- [ ] Export **DOCX** → `MLSecOps-Practical-Reference-Guide-v1.1.0.docx`
- [ ] Export **PDF** → `MLSecOps-Practical-Reference-Guide-v1.1.0.pdf`

### Git

- [ ] Commit all changes with message: `docs: release v1.1.0 — traceability and Exchange integration (closes #1)`
- [ ] `git push origin main`
- [ ] `git tag -a v1.1.0 -m "MLSecOps Practical Reference Guide v1.1.0"`
- [ ] `git push origin v1.1.0`

### GitHub Release

1. Create release from tag **v1.1.0**
2. Title: **v1.1.0 — MLSecOps Practical Reference Guide**
3. Body: copy from [RELEASE_NOTES.md](RELEASE_NOTES.md) v1.1.0 section
4. Attach assets:
   - `MLSecOps-Practical-Reference-Guide-v1.1.0.docx`
   - `MLSecOps-Practical-Reference-Guide-v1.1.0.pdf`

### Zenodo

1. Publish new version from tag `v1.1.0` on [Zenodo record](https://zenodo.org/records/21206781)
2. Confirm DOI landing page lists v1.1.0
3. Update README DOI note if Zenodo assigns a version-specific DOI

### Post-release

- [ ] Close [Issue #1](https://github.com/l4tr0d3ctism/MLSecOps/issues/1) with thank-you to @Wapiti08
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
| GitHub Discussions | Announce v1.1.0 with link to Pages + PDF |

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
| `v2.0.0` | Lifecycle model or major structural change |

Document every release in [CHANGELOG.md](CHANGELOG.md).

---

## Build assets (local workspace)

Word/PDF builds use `scripts/build-docx.py` in this repository:

```bash
# From repository root
python scripts/build-docx.py --render-mermaid
# Output: dist/MLSecOps-Practical-Reference-Guide-v1.1.0.docx
```

The build uses Pandoc with the existing Word **reference template** (`scripts/templates/reference.docx`, or auto-download from the v1.0.0 Release DOCX). Diagram PNGs are taken from `github/assets/diagrams/`; missing PNGs can be rendered from `assets/diagrams/source/*.mmd` with `--render-mermaid`.

1. Sync markdown → DOCX: `python scripts/build-docx.py --render-mermaid`
2. Export PDF from DOCX in Word (or pandoc)
3. Upload both files to GitHub Release — do not commit large binaries to `main` unless using Git LFS

---

## General pre-release (any version)

- [ ] No new chapters unless planned for next minor/major
- [ ] Review [GETTING-STARTED.md](GETTING-STARTED.md) role-based paths
- [ ] Update [SECURITY.md](SECURITY.md) supported versions table
