# Releasing the Guide

Checklist for maintainers publishing **v1.1.0** and later versions.

**Current release:** v1.1.0 (2026-07-11)

---

## v1.1.0 release checklist

### Pre-release (content)

- [x] Per-section `References / Source mapping` across Chapters 1–17 ([Issue #1](https://github.com/l4tr0d3ctism/MLSecOps/issues/1))
- [x] OWASP AI Exchange complementary integration
- [x] Ch.1 reader value / guide at a glance ([Issue #2](https://github.com/l4tr0d3ctism/MLSecOps/issues/2))
- [x] Version strings: README, TOC, Ch.1, CHANGELOG, CITATION.cff, CONTRIBUTING, GOVERNANCE, GUIDE-SUMMARY, SECURITY, RELEASE_NOTES, releases README, `prepare_pages.py`
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

## Version numbering

| Tag | Meaning |
|-----|---------|
| `v1.0.0` | First stable public release (content scope frozen) |
| `v1.1.0` | Per-section traceability, mapping audit, Exchange integration, intro clarity |
| `v2.0.0` | Lifecycle model or major structural change |

Document every release in [CHANGELOG.md](CHANGELOG.md).

---

## Build assets (local workspace)

Word/PDF builds run **outside this repo** (see maintainer workspace):

1. Sync markdown → DOCX from `chapters-en/`
2. Export PDF from DOCX or pandoc
3. Upload both files to GitHub Release — do not commit large binaries to `main` unless using Git LFS

---

## General pre-release (any version)

- [ ] No new chapters unless planned for next minor/major
- [ ] Review [GUIDE-SUMMARY.md](GUIDE-SUMMARY.md) version line
- [ ] Update [SECURITY.md](SECURITY.md) supported versions table
