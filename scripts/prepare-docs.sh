#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
rm -rf "$ROOT/docs/chapters-en"
cp -r "$ROOT/chapters-en" "$ROOT/docs/chapters-en"
cp "$ROOT/CONTRIBUTING.md" "$ROOT/docs/contributing.md"
echo "Prepared docs/chapters-en and docs/contributing.md"
