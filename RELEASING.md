# Releasing the Guide

Checklist for maintainers publishing **v1.0.0** and later versions.

---

## Pre-release (content freeze)

- [ ] No new chapters — fixes and editorial only  
- [ ] Run internal link validation and Word sync in the **local build workspace** (outside this repo)  
- [ ] Export PDF from DOCX or pandoc  
- [ ] Update version strings: README, TOC, Ch.1 banner, CHANGELOG, citation block  
- [ ] Remove or fix stale links (e.g. old docs site URLs)  
- [ ] Review [GUIDE-SUMMARY.md](GUIDE-SUMMARY.md) version line  

---

## Version numbering

| Tag | Meaning |
|-----|---------|
| `v1.0.0` | First stable public release (content scope frozen) |
| `v1.1.0` | Mapping updates, new case studies, Appendix tweaks |
| `v2.0.0` | Lifecycle model or major structural change |

Document every release in [CHANGELOG.md](CHANGELOG.md).

---

## GitHub Release

1. `git tag -a v1.0.0 -m "MLSecOps Practical Reference Guide v1.0.0"`  
2. `git push origin v1.0.0`  
3. Create release on GitHub with notes from CHANGELOG  
4. Attach assets:
   - `MLSecOps-Guide-v1.0.docx`
   - `MLSecOps-Guide-v1.0.pdf`
   - Optional: zip of `chapters-en/`  

Release title example: **v1.0.0 — MLSecOps Practical Reference Guide**

---

## Zenodo (after first GitHub Release)

1. Connect GitHub repo to [Zenodo](https://zenodo.org)  
2. Create Zenodo record from tag `v1.0.0`  
3. Add DOI to README **Cite this work** section  
4. Add DOI badge to README  

---

## Post-release

- [ ] Announce in GitHub Discussions  
- [ ] Optional: LinkedIn post (framework intro, not marketing)  
- [ ] Collect community feedback for v1.1  
- [ ] List reviewers in README (with permission only)  

---

## Build assets (local workspace)

If the Word build scripts live outside this repository:

1. Run markdown → DOCX sync in the build workspace  
2. Copy `MLSecOps-Guide-v1.0.docx` into release assets  
3. Export PDF (Word → Save as PDF, or pandoc)  

Do not commit large binary files to `main` unless using Git LFS; prefer **Release attachments**.
