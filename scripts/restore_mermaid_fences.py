#!/usr/bin/env python3
"""Restore ```mermaid fences from assets/diagrams/source/*.mmd before matching PNG embeds."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters-en"
SOURCE = ROOT / "assets" / "diagrams" / "source"
FENCE = "`" * 3


def strip_mermaid(text: str) -> str:
    # Proper fences
    text = re.sub(rf"{re.escape(FENCE)}mermaid\n.*?{re.escape(FENCE)}\n*", "", text, flags=re.DOTALL)
    # Broken single-tick fences from PowerShell escaping
    text = re.sub(r"`mermaid\n.*?`\n*", "", text, flags=re.DOTALL)
    return text


def restore(text: str) -> tuple[str, int]:
    text = strip_mermaid(text)
    img_re = re.compile(r"!\[\]\(\.\./assets/diagrams/([A-Za-z0-9_\.-]+\.png)\)")
    out: list[str] = []
    added = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        m = img_re.fullmatch(stripped) if stripped.startswith("![") else None
        if not m:
            # also allow image with nothing else on line via search
            m = img_re.search(stripped) if stripped.startswith("![") else None
        if m:
            png = m.group(1)
            mmd_path = SOURCE / png.replace(".png", ".mmd")
            if mmd_path.exists():
                src = mmd_path.read_text(encoding="utf-8").strip() + "\n"
                out.append(f"{FENCE}mermaid\n{src}{FENCE}\n\n")
                added += 1
        out.append(line if line.endswith("\n") else line + "\n")
    return "".join(out), added


def main() -> None:
    for path in sorted(CHAPTERS.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated, n = restore(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            fences = len(re.findall(rf"{re.escape(FENCE)}mermaid", updated))
            print(f"{path.name}: restored {n} (fences now {fences})")
        else:
            print(f"{path.name}: unchanged")


if __name__ == "__main__":
    main()
