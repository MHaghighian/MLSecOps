#!/usr/bin/env python3
"""Copy markdown sources into docs/ for MkDocs GitHub Pages build."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CHAPTERS_SRC = ROOT / "chapters-en"
CHAPTERS_DST = DOCS / "chapters-en"
ASSETS_SRC = ROOT / "assets"

COPY_ROOT_FILES = [
    ("GETTING-STARTED.md", "getting-started.md"),
    ("CHANGELOG.md", "changelog.md"),
    ("CONTRIBUTING.md", "contributing.md"),
    ("SECURITY.md", "security.md"),
    ("RELEASE_NOTES.md", "release-notes.md"),
    ("GOVERNANCE.md", "governance.md"),
    ("DCO.md", "dco.md"),
    ("DESIGN.md", "design.md"),
    ("RELEASE-INTEGRITY.md", "release-integrity.md"),
    ("RELEASING.md", "releasing.md"),
]

LINK_REWRITES = {
    "README.md": "index.md",
    "GETTING-STARTED.md": "getting-started.md",
    "CHANGELOG.md": "changelog.md",
    "CONTRIBUTING.md": "contributing.md",
    "SECURITY.md": "security.md",
    "RELEASE_NOTES.md": "release-notes.md",
    "GOVERNANCE.md": "governance.md",
    "DCO.md": "dco.md",
    "DESIGN.md": "design.md",
    "RELEASE-INTEGRITY.md": "release-integrity.md",
    "RELEASING.md": "releasing.md",
    "../CHANGELOG.md": "../changelog.md",
    "../GETTING-STARTED.md": "../getting-started.md",
    "../references/AARM-ALIGNMENT.md": "../references/aarm-alignment.md",
    "references/AARM-ALIGNMENT.md": "references/aarm-alignment.md",
    # Non-doc paths → GitHub (MkDocs --strict cannot resolve repo files)
    "requirements-pages.txt": "https://github.com/MHaghighian/MLSecOps/blob/main/requirements-pages.txt",
    "scripts/requirements-docx.txt": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/requirements-docx.txt",
    ".github/workflows/": "https://github.com/MHaghighian/MLSecOps/tree/main/.github/workflows/",
    "releases/v1.3.0-RELEASE-BODY.md": "https://github.com/MHaghighian/MLSecOps/blob/main/releases/v1.3.0-RELEASE-BODY.md",
    "releases/v1.4.0-RELEASE-BODY.md": "https://github.com/MHaghighian/MLSecOps/blob/main/releases/v1.4.0-RELEASE-BODY.md",
    "scripts/README.md": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/README.md",
    "../scripts/README.md": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/README.md",
    "scripts/ai_security_scan.py": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/ai_security_scan.py",
    "../scripts/ai_security_scan.py": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/ai_security_scan.py",
    "scripts/verify_repo.py": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/verify_repo.py",
    "../scripts/verify_repo.py": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/verify_repo.py",
    "scripts/build-docx.py": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/build-docx.py",
    "scripts/generate_release_manifest.py": "https://github.com/MHaghighian/MLSecOps/blob/main/scripts/generate_release_manifest.py",
    "tests/test_ai_security_scan.py": "https://github.com/MHaghighian/MLSecOps/blob/main/tests/test_ai_security_scan.py",
    "../tests/test_ai_security_scan.py": "https://github.com/MHaghighian/MLSecOps/blob/main/tests/test_ai_security_scan.py",
}


def _normalize_mkdocs_fragment(match: re.Match[str]) -> str:
    label, target, frag = match.group(1), match.group(2), match.group(3)
    if target.startswith(("http://", "https://", "mailto:")):
        return match.group(0)
    # Python-Markdown toc collapses consecutive hyphens (GitHub keeps '--' for ' — ' / ' / ').
    frag = re.sub(r"-{2,}", "-", frag)
    return f"[{label}]({target}#{frag})"


def rewrite_links(text: str, *, rewrite_readme: bool = True) -> str:
    for old, new in LINK_REWRITES.items():
        if not rewrite_readme and old == "README.md":
            continue
        text = text.replace(f"]({old})", f"]({new})")
        text = text.replace(f"]({old}#", f"]({new}#")
    text = re.sub(
        r"\[([^\]]+)\]\(([^)#\s]*)#([^)\s]+)\)",
        _normalize_mkdocs_fragment,
        text,
    )
    text = text.replace("{#reading-paths}", "")
    # On MkDocs Pages, Mermaid blocks render client-side via mermaid.min.js;
    # strip the immediate static PNG fallback to prevent duplicate diagrams.
    text = re.sub(
        r"(```mermaid\s*\n.*?\n```)\s*\n+!\[\]\(\.\./assets/diagrams/[^)]+\)\n?",
        r"\1\n\n",
        text,
        flags=re.DOTALL,
    )
    return text


def write_doc(src: Path, dst: Path, *, rewrite_readme: bool = True) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(rewrite_links(src.read_text(encoding="utf-8"), rewrite_readme=rewrite_readme), encoding="utf-8")


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    (DOCS / "index.md").write_text(
        """# MLSecOps Reference Model & Practical Guide

**Open-source MLSecOps reference model and practical guide for AI security, LLM/RAG, agentic AI, and secure MLOps.**

**v1.4.0** — lifecycle control model (`CP 1–10`), machine-readable Evidence Pack schema, OPA/Conftest Policy-as-Code suites (Evidence Pack + Kubernetes workloads), zero-dependency static MCP/model scanner (`scripts/ai_security_scan.py`), and Secure-by-Design blueprints across data, training, deployment, runtime, SOC, and governance.

[GitHub repository](https://github.com/MHaghighian/MLSecOps) · [mhsec.me](https://mhsec.me) · [Getting Started](getting-started.md) · [Zenodo DOI](https://doi.org/10.5281/zenodo.21206780) · [OpenSSF Best Practices](https://www.bestpractices.dev/projects/15668)

## Topics

| Area | Start here |
|------|------------|
| MLSecOps lifecycle | [Chapter 6 — Lifecycle control model](chapters-en/06-pipeline.md) |
| LLM & RAG security | [Chapter 7](chapters-en/07-llm-rag-security.md) |
| Agentic AI & MCP | [Chapter 8](chapters-en/08-agentic-ai-security.md) |
| AI supply chain | [Chapter 5](chapters-en/05-model-artifact-supply-chain.md) |
| Implementation rollout | [Appendix E](chapters-en/17-appendix-e-implementation-reference.md) |

## Start reading

| | |
|---|---|
| [Chapter 1 — Introduction](chapters-en/01-intro.md) | Scope, principles, lifecycle overview |
| [Chapter 6 — Lifecycle control model](chapters-en/06-pipeline.md) | Ten control points and release decisions |
| [Appendix E — Implementation Reference](chapters-en/17-appendix-e-implementation-reference.md) | Architecture cards, templates, playbooks |
| [Full table of contents](chapters-en/TABLE-OF-CONTENTS.md) | All sections |

## What this guide adds

This reference model defines an independent operational control architecture cross-mapped to OWASP, MITRE ATLAS, NIST, ISO, OpenSSF, and CSA:

1. Ten lifecycle **control points** (`CP 1–10`) with **CP 8** release approval bound to **CP 9** admission
2. Explicit separation of **release decisions** (`CP 4, 7, 8`) from **integrity verification** (`CP 9`) and evidence steps
3. Machine-readable **`Evidence Pack`** ([`schemas/`](schemas/README.md)) and OPA/Conftest admission samples ([`policies/`](policies/README.md))
4. **Secure-by-Design** blueprints ([Appendix E.7](chapters-en/17-appendix-e-implementation-reference.md#e7-secure-by-design-worked-examples)) linking threat modeling, runtime, SOC, and governance

Details in [Chapter 1](chapters-en/01-intro.md#what-this-guide-adds-beyond-owasp-openssf-and-nist).
""",
        encoding="utf-8",
    )

    CHAPTERS_DST.mkdir(parents=True)
    for src in CHAPTERS_SRC.glob("*.md"):
        write_doc(src, CHAPTERS_DST / src.name)

    for src_rel, dst_name in COPY_ROOT_FILES:
        src = ROOT / src_rel
        if src.exists():
            write_doc(src, DOCS / dst_name)

    refs_src = ROOT / "references"
    refs_dst = DOCS / "references"
    if refs_src.exists():
        refs_dst.mkdir(parents=True, exist_ok=True)
        for src in refs_src.glob("*.md"):
            write_doc(src, refs_dst / src.name.lower())

    if ASSETS_SRC.exists():
        shutil.copytree(ASSETS_SRC, DOCS / "assets", dirs_exist_ok=True)
        extra_readme = DOCS / "assets" / "diagrams" / "README.md"
        if extra_readme.exists():
            extra_readme.unlink()

    # Policy-as-Code and Evidence Pack schema samples are linked from chapters.
    for sample_dir in ("schemas", "policies"):
        src_dir = ROOT / sample_dir
        if src_dir.exists():
            shutil.copytree(src_dir, DOCS / sample_dir, dirs_exist_ok=True)
            for md_src in src_dir.rglob("*.md"):
                write_doc(md_src, DOCS / sample_dir / md_src.relative_to(src_dir), rewrite_readme=False)

    license_src = ROOT / "LICENSE"
    if license_src.exists():
        shutil.copy2(license_src, DOCS / "LICENSE")
    citation_src = ROOT / "CITATION.cff"
    if citation_src.exists():
        shutil.copy2(citation_src, DOCS / "CITATION.cff")

    seo_dir = ROOT / ".github" / "seo"
    if seo_dir.exists():
        for verification_file in seo_dir.glob("google*.html"):
            shutil.copy2(verification_file, DOCS / verification_file.name)

    print(f"Prepared {DOCS} ({len(list(CHAPTERS_DST.glob('*.md')))} chapter files)")


if __name__ == "__main__":
    main()
