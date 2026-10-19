#!/usr/bin/env python3
"""Generate or verify SHA256SUMS for documentation release integrity."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Paths that constitute the published guide (relative to repo root).
INCLUDE_GLOBS = [
    "chapters-en/**/*.md",
    "assets/diagrams/**/*",
    "mkdocs.yml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "CITATION.cff",
    "GETTING-STARTED.md",
    "GOVERNANCE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "DCO.md",
    "DESIGN.md",
    "RELEASE-INTEGRITY.md",
    "requirements-pages.txt",
    "scripts/requirements-docx.txt",
]


def iter_files() -> list[Path]:
    files: set[Path] = set()
    for pattern in INCLUDE_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file() and ".git" not in path.parts:
                files.add(path)
    return sorted(files, key=lambda p: p.as_posix().lower())


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(out: Path) -> None:
    lines = []
    for path in iter_files():
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"{sha256_file(path)}  {rel}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(lines)} entries)", file=sys.stderr)


def verify_manifest(manifest: Path) -> int:
    errors = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, rel = line.partition("  ")
        if not rel:
            print(f"bad line: {line}", file=sys.stderr)
            errors += 1
            continue
        path = ROOT / rel
        if not path.is_file():
            print(f"MISSING {rel}", file=sys.stderr)
            errors += 1
            continue
        actual = sha256_file(path)
        if actual != digest:
            print(f"MISMATCH {rel}", file=sys.stderr)
            errors += 1
        else:
            print(f"OK {rel}")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("SHA256SUMS"),
        help="manifest output path",
    )
    parser.add_argument(
        "--verify",
        type=Path,
        metavar="SHA256SUMS",
        help="verify an existing manifest",
    )
    args = parser.parse_args()
    if args.verify:
        return verify_manifest(args.verify)
    write_manifest(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
