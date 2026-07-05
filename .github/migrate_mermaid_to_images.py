#!/usr/bin/env python3
"""Replace Mermaid fences with PNG images; save .mmd source for regeneration."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters-en"
SOURCE_DIR = ROOT / "assets" / "diagrams" / "source"
PNG_DIR = ROOT / "assets" / "diagrams"

# Mermaid block, optional following PNG line we added earlier
BLOCK_RE = re.compile(
    r"```mermaid\s*\n(.*?)\n```(?:\s*\n!\[[^\]]*\]\(\.\./assets/diagrams/[^)]+\))?",
    re.DOTALL,
)


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    stem = path.stem
    idx = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal idx
        idx += 1
        src = match.group(1).strip() + "\n"
        SOURCE_DIR.mkdir(parents=True, exist_ok=True)
        mmd = SOURCE_DIR / f"{stem}_{idx:02d}.mmd"
        mmd.write_text(src, encoding="utf-8")
        png = PNG_DIR / f"{stem}_{idx:02d}.png"
        if not png.exists():
            print(f"  WARNING: missing {png.name}", file=sys.stderr)
        return f"\n\n![](../assets/diagrams/{stem}_{idx:02d}.png)\n"

    new_text, n = BLOCK_RE.subn(repl, text)
    if n:
        path.write_text(new_text, encoding="utf-8")
    return n


def main() -> int:
    total = 0
    for path in sorted(CHAPTERS.glob("*.md")):
        n = process_file(path)
        if n:
            print(f"{path.name}: {n} diagram(s) → PNG only")
            total += n
    print(f"Done. Migrated {total} diagram(s); sources in assets/diagrams/source/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
