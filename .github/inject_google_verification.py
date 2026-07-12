#!/usr/bin/env python3
"""Inject Google Search Console verification meta tag into mkdocs.yml before build."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "mkdocs.yml"
CODE_FILE = ROOT / "seo" / "google-site-verification.code"
PLACEHOLDER = "PASTE_GOOGLE_VERIFICATION_CODE_HERE"
META_BLOCK = (
    "  meta:\n"
    '    - name: google-site-verification\n'
    '      content: "{code}"\n'
)


def read_code() -> str | None:
    env_code = os.environ.get("GOOGLE_SITE_VERIFICATION", "").strip()
    if env_code:
        return env_code

    if CODE_FILE.exists():
        code = CODE_FILE.read_text(encoding="utf-8").strip()
        if code and code != PLACEHOLDER and not code.startswith("#"):
            return code.splitlines()[0].strip()

    return None


def inject(code: str) -> None:
    text = MKDOCS.read_text(encoding="utf-8")
    block = META_BLOCK.format(code=code)

    if "google-site-verification" in text:
        text = re.sub(
            r"  meta:\n(?:    - .*\n)+",
            block,
            text,
            count=1,
        )
    elif "\nextra:\n" in text:
        text = text.replace("\nextra:\n", f"\nextra:\n{block}", 1)
    else:
        text = text.rstrip() + f"\n\nextra:\n{block}"

    MKDOCS.write_text(text, encoding="utf-8")
    print("Google site verification meta tag injected into mkdocs.yml")


def main() -> None:
    code = read_code()
    if not code:
        print(
            "Google verification skipped: set GOOGLE_SITE_VERIFICATION secret "
            f"or paste code in {CODE_FILE.relative_to(ROOT)}",
            file=sys.stderr,
        )
        return

    inject(code)


if __name__ == "__main__":
    main()
