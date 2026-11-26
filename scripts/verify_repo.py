#!/usr/bin/env python3
"""Run fast local/CI verification across Evidence Pack schemas, Conftest policies, unit tests, docs, and manifests."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parent.parent


def _strict_format_checker() -> FormatChecker:
    checker = FormatChecker()

    @checker.checks("date-time")
    def _is_rfc3339(value: object) -> bool:
        if not isinstance(value, str) or "T" not in value:
            return False
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None

    return checker


def check_workflows_and_encoding() -> None:
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        yaml.safe_load(wf.read_text(encoding="utf-8"))
        print(f"OK yaml: {wf.relative_to(ROOT).as_posix()}")

    no_bom_paths = [
        ROOT / "assets" / "javascripts" / "mermaid-init.js",
        *(ROOT / "policies").rglob("*.rego"),
        *(ROOT / "schemas").rglob("*.json"),
        *(ROOT / "scripts").glob("*.py"),
        *(ROOT / "tests").glob("*.py"),
    ]
    for p in no_bom_paths:
        if p.read_bytes().startswith(b"\xef\xbb\xbf"):
            raise AssertionError(f"Unexpected UTF-8 BOM in {p.relative_to(ROOT)}")
    print("OK encoding: no UTF-8 BOM in code/policy/schema/test files")


def check_evidence_pack_schema() -> None:
    schema_path = ROOT / "schemas" / "evidence-pack.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=_strict_format_checker())

    fixtures = [
        *sorted((ROOT / "schemas" / "examples").glob("*.json")),
        *sorted((ROOT / "policies" / "testdata").glob("*.json")),
    ]
    for fp in fixtures:
        validator.validate(json.loads(fp.read_text(encoding="utf-8")))
        print(f"OK schema: {fp.relative_to(ROOT).as_posix()}")

    managed = json.loads(
        (ROOT / "schemas" / "examples" / "evidence-pack.managed-api.example.json").read_text(encoding="utf-8")
    )
    agentic = json.loads(
        (ROOT / "schemas" / "examples" / "evidence-pack.example.json").read_text(encoding="utf-8")
    )
    bad_ts = json.loads(json.dumps(agentic))
    bad_ts["metadata"]["timestamp"] = "not-a-timestamp"

    negative_cases = [
        ({k: v for k, v in managed.items() if k != "managedApiConfig"}, "Managed-API without managedApiConfig"),
        ({k: v for k, v in agentic.items() if k != "modelArtifact"}, "Non-managed without modelArtifact"),
        ({k: v for k, v in agentic.items() if k != "runtimeAgentConfig"}, "Agentic-MCP without runtimeAgentConfig"),
        (bad_ts, "Invalid RFC-3339 metadata.timestamp"),
    ]
    for payload, label in negative_cases:
        try:
            validator.validate(payload)
        except ValidationError:
            print(f"OK schema reject: {label}")
            continue
        raise AssertionError(f"Expected ValidationError for {label}")


def check_chapters_code_and_diagrams() -> None:
    chapters = sorted((ROOT / "chapters-en").glob("*.md"))
    src_dir = ROOT / "assets" / "diagrams" / "source"
    png_dir = ROOT / "assets" / "diagrams"
    fence_re = re.compile(r"```([a-zA-Z0-9_-]*)\s*\n(.*?)```", re.S)

    mmd_norms = {
        f.name: "\n".join(l.rstrip() for l in f.read_text(encoding="utf-8").strip().splitlines())
        for f in sorted(src_dir.glob("*.mmd"))
    }

    for ch in chapters:
        txt = ch.read_text(encoding="utf-8")
        prefix = ch.stem + "_"
        cand_norms = [norm for name, norm in mmd_norms.items() if name.startswith(prefix)]
        for m in fence_re.finditer(txt):
            lang = m.group(1).lower()
            body = m.group(2)
            if lang in ("yaml", "yml"):
                for doc in body.split("\n---"):
                    list(yaml.safe_load_all(doc))
            elif lang == "json":
                json.loads(body)
            elif lang == "mermaid":
                norm = "\n".join(l.rstrip() for l in body.strip().splitlines())
                if norm not in cand_norms:
                    raise AssertionError(f"Inline mermaid in {ch.name} does not match any {ch.stem}_*.mmd")

        for ref in re.finditer(r"assets/diagrams/([^)\s]+\.png)", txt):
            if not (png_dir / ref.group(1)).is_file():
                raise AssertionError(f"Missing diagram PNG {ref.group(1)} referenced in {ch.name}")

    for mmd_name in mmd_norms:
        png_name = mmd_name[:-4] + ".png"
        if not (png_dir / png_name).is_file():
            raise AssertionError(f"Missing PNG companion for {mmd_name}")
    print(f"OK chapters & diagrams: {len(chapters)} files, syntax/parity verified")


def check_release_manifest() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import generate_release_manifest as grm

    files = {p.relative_to(ROOT).as_posix() for p in grm.iter_files()}
    required = [
        "policies/cp8_cp9_admission.rego",
        "policies/cp8_cp9_admission_test.rego",
        "policies/k8s/inference_workload.rego",
        "policies/k8s/inference_workload_test.rego",
        "schemas/evidence-pack.schema.json",
        "schemas/examples/evidence-pack.managed-api.example.json",
        "scripts/ai_security_scan.py",
        "scripts/build-docx.py",
        "scripts/verify_repo.py",
        "tests/test_ai_security_scan.py",
        "assets/javascripts/mermaid-init.js",
    ]
    missing = [r for r in required if r not in files]
    if missing:
        raise AssertionError(f"Manifest excludes required paths: {missing}")
    print(f"OK release manifest coverage: {len(files)} files")


def run_python_unit_tests() -> None:
    tests_dir = ROOT / "tests"
    if not tests_dir.is_dir():
        return
    suite = unittest.defaultTestLoader.discover(str(tests_dir), pattern="test_*.py", top_level_dir=str(tests_dir))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise AssertionError(f"Python unit tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
    print(f"OK unit tests: {result.testsRun} tests passed")


def run_conftest(conftest_bin: str | None, require: bool) -> None:
    exe = conftest_bin or shutil.which("conftest")
    if not exe:
        if require:
            raise FileNotFoundError("conftest binary not found (--require-conftest set)")
        print("SKIP conftest: binary not on PATH")
        return

    def run(args: list[str], expect_fail: bool = False, expect_substr: str | None = None) -> None:
        proc = subprocess.run([exe, *args], cwd=ROOT, text=True, capture_output=True)
        combined = proc.stdout + proc.stderr
        if expect_fail:
            if proc.returncode == 0:
                raise AssertionError(f"Expected failure for conftest {' '.join(args)}:\n{combined}")
        elif proc.returncode != 0:
            raise AssertionError(f"Conftest failed ({proc.returncode}) for {' '.join(args)}:\n{combined}")
        if expect_substr and expect_substr not in combined:
            raise AssertionError(f"Expected {expect_substr!r} in conftest output:\n{combined}")

    run(["verify", "--policy", "policies"])
    print("OK conftest verify: policies/ + policies/k8s/")

    for ok_pack in sorted((ROOT / "schemas" / "examples").glob("*.json")):
        run(["test", "--policy", "policies", str(ok_pack.relative_to(ROOT))])
        print(f"OK conftest pass: {ok_pack.relative_to(ROOT).as_posix()}")

    run(
        ["test", "--policy", "policies", "policies/testdata/evidence-pack.fail-digest.json"],
        expect_fail=True,
        expect_substr="CRITICAL [CP8->CP9]",
    )
    run(
        ["test", "--policy", "policies", "policies/testdata/evidence-pack.fail-unpinned-mcp.json"],
        expect_fail=True,
        expect_substr="CRITICAL [Ch.8 MCP09]",
    )
    run(["test", "--policy", "policies/k8s", "--namespace", "mlsecops.k8s", "policies/k8s/testdata/inference-pass.yaml"])
    run(
        ["test", "--policy", "policies/k8s", "--namespace", "mlsecops.k8s", "policies/k8s/testdata/inference-fail.yaml"],
        expect_fail=True,
        expect_substr="CRITICAL [Ch.16/CP9]",
    )
    print("OK conftest fixtures: Evidence Pack + Kubernetes workload checks passed")


def run_mkdocs_strict() -> None:
    subprocess.run([sys.executable, str(ROOT / ".github" / "prepare_pages.py")], cwd=ROOT, check=True)
    subprocess.run(["mkdocs", "build", "--strict"], cwd=ROOT, check=True)
    from bs4 import BeautifulSoup

    site = ROOT / "site"
    html_files = list(site.rglob("*.html"))
    ids_by_page: dict[Path, set[str]] = {}
    links_by_page: list[tuple[Path, str]] = []

    # Single DOM parse per HTML page (~2x faster than separate ID + link passes).
    for p in html_files:
        soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="replace"), "html.parser")
        resolved = p.resolve()
        ids_by_page[resolved] = {el["id"] for el in soup.find_all(id=True)}
        for div in soup.find_all("div", class_="mermaid"):
            nxt = div.find_next_sibling()
            if nxt and nxt.name == "p" and nxt.find("img"):
                raise AssertionError(f"Duplicate Mermaid+PNG block in {p.relative_to(site)}")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.startswith(("http://", "https://", "mailto:", "javascript:", "#__")):
                links_by_page.append((p, href))

    for p, href in links_by_page:
        target_str, frag = (href.split("#", 1) + [""])[:2]
        if not target_str:
            target = p.resolve()
        else:
            if target_str.startswith("/MLSecOps/"):
                cand = site / target_str[len("/MLSecOps/") :]
            elif target_str.startswith("/"):
                cand = site / target_str.lstrip("/")
            else:
                cand = p.parent / target_str
            if cand.is_dir():
                cand = cand / "index.html"
            elif not cand.exists() and Path(str(cand) + "/index.html").exists():
                cand = Path(str(cand) + "/index.html")
            target = cand.resolve()
            if not target.exists():
                raise AssertionError(f"Broken built link in {p.relative_to(site)}: {href}")
        if frag and frag not in ids_by_page.get(target, set()):
            raise AssertionError(f"Broken built anchor in {p.relative_to(site)}: {href}")
    print(f"OK mkdocs & HTML audit: {len(html_files)} pages, 0 broken links/anchors")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-mkdocs", action="store_true", help="Prepare docs/ and verify mkdocs build --strict + site/ links")
    parser.add_argument("--require-conftest", action="store_true", help="Fail if conftest is unavailable")
    parser.add_argument("--conftest-bin", help="Explicit path to conftest executable")
    args = parser.parse_args()

    check_workflows_and_encoding()
    check_evidence_pack_schema()
    check_chapters_code_and_diagrams()
    check_release_manifest()
    run_python_unit_tests()
    run_conftest(args.conftest_bin, args.require_conftest)
    if args.with_mkdocs:
        run_mkdocs_strict()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
