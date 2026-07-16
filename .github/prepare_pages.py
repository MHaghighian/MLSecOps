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
    ("RELEASING.md", "releasing.md"),
    ("RELEASE_NOTES.md", "release-notes.md"),
    ("GOVERNANCE.md", "governance.md"),
    ("releases/README.md", "releases-notes.md"),
]

LINK_REWRITES = {
    "README.md": "index.md",
    "GETTING-STARTED.md": "getting-started.md",
    "CHANGELOG.md": "changelog.md",
    "CONTRIBUTING.md": "contributing.md",
    "SECURITY.md": "security.md",
    "RELEASING.md": "releasing.md",
    "RELEASE_NOTES.md": "release-notes.md",
    "GOVERNANCE.md": "governance.md",
    "releases/README.md": "releases-notes.md",
    "../CHANGELOG.md": "../changelog.md",
    "../RELEASING.md": "../releasing.md",
    "../GETTING-STARTED.md": "../getting-started.md",
    "../references/AARM-ALIGNMENT.md": "../references/aarm-alignment.md",
    "references/AARM-ALIGNMENT.md": "references/aarm-alignment.md",
}


def rewrite_links(text: str) -> str:
    for old, new in LINK_REWRITES.items():
        text = text.replace(f"]({old})", f"]({new})")
        text = text.replace(f"]({old}#", f"]({new}#")
    text = re.sub(
        r"#e13-self-hosted-llm-vllm--kserve-on-kubernetes",
        "#e13-self-hosted-llm-vllm-kserve-on-kubernetes",
        text,
    )
    text = re.sub(
        r"#e14-agent-with-tools-mcp--apis",
        "#e14-agent-with-tools-mcp-apis",
        text,
    )
    text = re.sub(
        r"#e16-classic-ml-tabular--vision--no-llm",
        "#e16-classic-ml-tabular-vision-no-llm",
        text,
    )
    text = text.replace("{#reading-paths}", "")
    return text


def write_doc(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(rewrite_links(src.read_text(encoding="utf-8")), encoding="utf-8")


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    (DOCS / "index.md").write_text(
        """# MLSecOps Practical Reference Guide

**Open-source MLSecOps handbook for AI security, LLM/RAG, and secure MLOps.**

**v1.1.1** — practical reference for securing AI systems across the ML lifecycle: data, training, deployment, runtime, SOC, and governance.

[GitHub repository](https://github.com/MHaghighian/MLSecOps) · [Getting Started](getting-started.md) · [Zenodo DOI](https://doi.org/10.5281/zenodo.21206781)

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

1. Ten lifecycle **control points**
2. **Release decisions** separate from evidence-producing steps
3. **`Evidence Pack`** per release
4. Unified thread: threat → runtime → SOC → governance

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

    license_src = ROOT / "LICENSE"
    if license_src.exists():
        shutil.copy2(license_src, DOCS / "LICENSE")
    citation_src = ROOT / "CITATION.cff"
    if citation_src.exists():
        shutil.copy2(citation_src, DOCS / "CITATION.cff")

    seo_dir = ROOT / "seo"
    if seo_dir.exists():
        for verification_file in seo_dir.glob("google*.html"):
            shutil.copy2(verification_file, DOCS / verification_file.name)

    print(f"Prepared {DOCS} ({len(list(CHAPTERS_DST.glob('*.md')))} chapter files)")


if __name__ == "__main__":
    main()
