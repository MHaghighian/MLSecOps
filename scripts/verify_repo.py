#!/usr/bin/env python3
"""Run local/CI verification across Evidence Pack schemas, Conftest policies, docs, diagrams, and release manifests."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parent.parent


def check_workflows_and_encoding() -> None:
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        yaml.safe_load(wf.read_text(encoding="utf-8"))
        print(f"OK yaml: {wf.relative_to(ROOT).as_posix()}")

    no_bom_paths = [
        ROOT / "assets" / "javascripts" / "mermaid-init.js",
        *(ROOT / "policies").rglob("*.rego"),
        *(ROOT / "schemas").rglob("*.json"),
        *(ROOT / "scripts").glob("*.py"),
    ]
    for p in no_bom_paths:
        if p.read_bytes().startswith(b"\xef\xbb\xbf"):
            raise AssertionError(f"Unexpected UTF-8 BOM in {p.relative_to(ROOT)}")
    print("OK encoding: no UTF-8 BOM in code/policy/schema files")


def check_evidence_pack_schema() -> None:
    schema_path = ROOT / "schemas" / "evidence-pack.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    fixtures = [
        *sorted((ROOT / "schemas" / "examples").glob("*.json")),
        *sorted((ROOT / "policies" / "testdata").glob("*.json")),
    ]
    for fp in fixtures:
        data = json.loads(fp.read_text(encoding="utf-8"))
        validator.validate(data)
        print(f"OK schema: {fp.relative_to(ROOT).as_posix()}")

    managed = json.loads(
        (ROOT / "schemas" / "examples" / "evidence-pack.managed-api.example.json").read_text(encoding="utf-8")
    )
    agentic = json.loads(
        (ROOT / "schemas" / "examples" / "evidence-pack.example.json").read_text(encoding="utf-8")
    )
    negative_cases = [
        ({k: v for k, v in managed.items() if k != "managedApiConfig"}, "Managed-API without managedApiConfig"),
        ({k: v for k, v in agentic.items() if k != "modelArtifact"}, "Non-managed without modelArtifact"),
        ({k: v for k, v in agentic.items() if k != "runtimeAgentConfig"}, "Agentic-MCP without runtimeAgentConfig"),
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

    for ch in chapters:
        txt = ch.read_text(encoding="utf-8")
        mmd_cands = sorted(src_dir.glob(f"{ch.stem}_*.mmd"))
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
                matched = any(
                    "\n".join(l.rstrip() for l in f.read_text(encoding="utf-8").strip().splitlines()) == norm
                    for f in mmd_cands
                )
                if not matched:
                    raise AssertionError(f"Inline mermaid in {ch.name} does not match any {ch.stem}_*.mmd")

        for ref in re.finditer(r"assets/diagrams/([^)\s]+\.png)", txt):
            if not (png_dir / ref.group(1)).is_file():
                raise AssertionError(f"Missing diagram PNG {ref.group(1)} referenced in {ch.name}")

    for mmd in sorted(src_dir.glob("*.mmd")):
        if not (png_dir / f"{mmd.stem}.png").is_file():
            raise AssertionError(f"Missing PNG companion for {mmd.name}")
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
        "scripts/build-docx.py",
        "scripts/verify_repo.py",
        "assets/javascripts/mermaid-init.js",
    ]
    missing = [r for r in required if r not in files]
    if missing:
        raise AssertionError(f"Manifest excludes required paths: {missing}")
    print(f"OK release manifest coverage: {len(files)} files")


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
    ids_by_page = {}
    for p in html_files:
        soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="replace"), "html.parser")
        ids_by_page[p.resolve()] = {el["id"] for el in soup.find_all(id=True)}
        for div in soup.find_all("div", class_="mermaid"):
            nxt = div.find_next_sibling()
            if nxt and nxt.name == "p" and nxt.find("img"):
                raise AssertionError(f"Duplicate Mermaid+PNG block in {p.relative_to(site)}")

    for p in html_files:
        soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="replace"), "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith(("http://", "https://", "mailto:", "javascript:", "#__")):
                continue
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
    run_conftest(args.conftest_bin, args.require_conftest)
    if args.with_mkdocs:
        run_mkdocs_strict()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
