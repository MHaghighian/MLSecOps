#!/usr/bin/env python3
"""Fast, zero-dependency static security scanner for MCP manifests/configs and ML model artifacts.

Detects 2025-2026 MLSecOps attack surfaces without loading multi-GB model weights into memory:
  1. Invisible Unicode Tag / Bidi / zero-width smuggling in MCP schemas, prompts, and metadata.
  2. MCP tool poisoning, credential-exfil directives, Shadow MCP unpinned runners, SSRF, cleartext transport, and inline secrets.
  3. Canonical SHA-256 MCP tools/list pinning & rug-pull drift detection.
  4. Header-first model serialization audit: extension-spoofed Pickle payloads, ZIP CRC-32 parser discrepancies
     (CVE-2025-10155 class), path-traversal ZIP entries, and Safetensors/GGUF header integrity checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

# Invisible Tag block (U+E0000..U+E007F), Bidi overrides/isolates, zero-width controls.
_STEGO_RE = re.compile(r"[\U000E0000-\U000E007F\u202A-\u202E\u2066-\u2069\u200B-\u200F\u2060]")

_TOOL_POISON_RE = re.compile(
    r"(?is)"
    r"(?:<\s*/?\s*important\b[^>]*>)"
    r"|(?:ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions)"
    r"|(?:do\s+not\s+(?:tell|mention|show|inform)\s+(?:the\s+)?user)"
    r"|(?:before\s+(?:calling|invoking|using)\s+any\s+other\s+tool)"
    r"|(?:~/\.ssh|/etc/(?:passwd|shadow)|\.aws/credentials|\bid_rsa\b)"
    r"|(?:\b(?:curl|wget)\b[^\n]*(?:https?://|\|)|/dev/tcp/|\bnc\s+-e\b)"
)

_SECRET_LITERAL_RE = re.compile(
    r"(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})"
)

_SSRF_HOST_RE = re.compile(r"(?i)(?:169\.254\.169\.254|100\.100\.100\.200|metadata\.google\.internal|fd00:ec2::254)")
_CLEARTEXT_REMOTE_RE = re.compile(r"(?i)^(?:http|ws)://(?!(?:localhost|127\.0\.0\.1|\[::1\])(?::|/|$))")
_SHELL_META_RE = re.compile(r"(?:&&|\|\||[;`|]|\$\()")
_UNPINNED_NPX_RE = re.compile(r"^(@[^/]+/)?[A-Za-z0-9._-]+$")
_UNPINNED_UVX_RE = re.compile(r"^[A-Za-z0-9._-]+$")

# Dangerous Pickle module/opcode signatures scanned only in small leading windows (<64 KB).
_DANGEROUS_PICKLE_RE = re.compile(
    rb"(?:posix|nt|os|subprocess|builtins|pty|socket|webbrowser|codecs|commands)\n(?:system|popen|Popen|run|call|check_output|eval|exec|__import__|getoutput)"
    rb"|(?:builtins|__builtin__)\x94?(?:eval|exec|__import__|getattr)"
)
_PICKLE_MAGIC_RE = re.compile(rb"^\x80[\x02-\x05]")
_HEADER_READ_BYTES = 65_536
_MAX_SAFETENSORS_HEADER = 100 * 1024 * 1024


@dataclass(frozen=True)
class Finding:
    severity: str
    rule_id: str
    target: str
    message: str


def scan_unicode_smuggling(text: str) -> list[str]:
    """Return compact labels for steganographic or bidi control characters present in text."""
    hits: list[str] = []
    for ch in text:
        cp = ord(ch)
        if 0xE0000 <= cp <= 0xE007F and "unicode-tag" not in hits:
            hits.append("unicode-tag")
        elif (0x202A <= cp <= 0x202E or 0x2066 <= cp <= 0x2069) and "bidi-override" not in hits:
            hits.append("bidi-override")
        elif (0x200B <= cp <= 0x200F or cp == 0x2060) and "zero-width" not in hits:
            hits.append("zero-width")
        if len(hits) == 3:
            break
    return hits


def _iter_strings(obj: Any, prefix: str = "") -> list[tuple[str, str]]:
    """Iteratively extract (json_path, string_value) pairs without recursion-limit risks."""
    out: list[tuple[str, str]] = []
    stack: list[tuple[str, Any]] = [(prefix, obj)]
    while stack:
        path, cur = stack.pop()
        if isinstance(cur, str):
            out.append((path, cur))
        elif isinstance(cur, dict):
            for k, v in cur.items():
                key_path = f"{path}.{k}" if path else str(k)
                if isinstance(k, str):
                    out.append((f"{key_path}<key>", k))
                stack.append((key_path, v))
        elif isinstance(cur, list):
            for idx, item in enumerate(cur):
                stack.append((f"{path}[{idx}]", item))
    return out


def canonical_tools_hash(tools: list[dict[str, Any]]) -> str:
    """Compute canonical SHA-256 digest matching Evidence Pack mcpSchemaHashes."""
    payload = json.dumps(tools, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def extract_mcp_server_hashes(doc: dict[str, Any]) -> dict[str, str]:
    """Extract canonical SHA-256 hashes for any server declaring a `tools` array."""
    hashes: dict[str, str] = {}
    servers = doc.get("mcpServers")
    if isinstance(servers, dict):
        for name, cfg in servers.items():
            if isinstance(cfg, dict) and isinstance(cfg.get("tools"), list):
                hashes[str(name)] = canonical_tools_hash(cfg["tools"])
    if isinstance(doc.get("serverName"), str) and isinstance(doc.get("tools"), list):
        hashes[doc["serverName"]] = canonical_tools_hash(doc["tools"])
    return hashes


def _check_stdio_command(cmd: str, args: list[Any], server_label: str, findings: list[Finding]) -> None:
    cmd_l = cmd.strip().lower()
    arg_strs = [str(a) for a in args]
    joined = " ".join([cmd, *arg_strs])

    if _SHELL_META_RE.search(joined) or (
        Path(cmd_l).name in {"sh", "bash", "zsh", "cmd", "cmd.exe", "powershell", "pwsh"}
        and any(a.lower() in {"-c", "/c", "-enc", "-encodedcommand"} for a in arg_strs)
    ):
        findings.append(
            Finding("CRITICAL", "MCP-EXEC-01", server_label, "Shell wrapper or metacharacters in stdio MCP command/args")
        )

    base = Path(cmd_l).name
    pkg_tokens = [a for a in arg_strs if a and not a.startswith("-")]
    if base in {"npx", "npx.cmd"} and pkg_tokens:
        pkg = pkg_tokens[0]
        # Allow local paths or git URLs only if pinned; flag bare unversioned registry package names.
        if _UNPINNED_NPX_RE.match(pkg):
            findings.append(
                Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned npx package {pkg!r} enables supply-chain drift")
            )
    elif base == "uvx" and pkg_tokens:
        pkg = pkg_tokens[0]
        if _UNPINNED_UVX_RE.match(pkg):
            findings.append(
                Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned uvx tool {pkg!r}; pin @version or ==version")
            )


def scan_mcp_document(doc: dict[str, Any], target: str, pinned_hashes: dict[str, str] | None = None) -> list[Finding]:
    """Scan an MCP client config, server tools/list manifest, or Evidence Pack runtimeAgentConfig."""
    findings: list[Finding] = []

    for jpath, text in _iter_strings(doc):
        if _STEGO_RE.search(text):
            kinds = ", ".join(scan_unicode_smuggling(text))
            findings.append(
                Finding("CRITICAL", "MCP-UNI-01", f"{target}:{jpath}", f"Hidden Unicode/Bidi control sequence ({kinds})")
            )
        if _TOOL_POISON_RE.search(text):
            findings.append(
                Finding("CRITICAL", "MCP-POISON-01", f"{target}:{jpath}", "Suspected tool-poisoning directive or credential-exfil pattern")
            )
        if _SECRET_LITERAL_RE.search(text) and "mcpSchemaHashes" not in jpath and "Hash" not in jpath:
            findings.append(
                Finding("CRITICAL", "MCP-SEC-01", f"{target}:{jpath}", "Inline API token or credential literal detected")
            )
        if _SSRF_HOST_RE.search(text):
            findings.append(
                Finding("CRITICAL", "MCP-SSRF-01", f"{target}:{jpath}", "Cloud metadata / SSRF target address detected")
            )
        is_endpoint_field = jpath.endswith((".url", ".endpoint", ".uri")) or jpath in {"url", "endpoint", "uri"} or ".args[" in jpath
        if is_endpoint_field and _CLEARTEXT_REMOTE_RE.search(text.strip()):
            findings.append(
                Finding("HIGH", "MCP-TLS-01", f"{target}:{jpath}", f"Cleartext remote MCP endpoint {text!r}")
            )

    servers = doc.get("mcpServers")
    if isinstance(servers, dict):
        for name, cfg in servers.items():
            if not isinstance(cfg, dict):
                continue
            label = f"{target}:mcpServers.{name}"
            cmd = cfg.get("command")
            if isinstance(cmd, str) and cmd.strip():
                args = cfg.get("args") if isinstance(cfg.get("args"), list) else []
                _check_stdio_command(cmd, args, label, findings)
            if cfg.get("samplingEnabled") is True and cfg.get("samplingBudgetCapped") is not True:
                findings.append(
                    Finding("HIGH", "MCP-SAMP-01", label, "MCP sampling enabled without explicit samplingBudgetCapped=true")
                )

    if doc.get("samplingEnabled") is True and doc.get("samplingBudgetCapped") is not True:
        findings.append(
            Finding("HIGH", "MCP-SAMP-01", target, "MCP sampling enabled without explicit samplingBudgetCapped=true")
        )

    if pinned_hashes is not None:
        observed = extract_mcp_server_hashes(doc)
        for srv, digest in observed.items():
            if srv not in pinned_hashes:
                findings.append(
                    Finding("CRITICAL", "MCP09-UNPINNED-01", f"{target}:{srv}", "Server absent from pinned mcpSchemaHashes")
                )
            elif pinned_hashes[srv] != digest:
                findings.append(
                    Finding(
                        "CRITICAL",
                        "MCP-RUGPULL-01",
                        f"{target}:{srv}",
                        f"Tool schema hash drift: expected {pinned_hashes[srv]}, got {digest}",
                    )
                )

    return findings


def _inspect_zip_archive(path: Path) -> list[Finding]:
    """Inspect ZIP headers & central directory without unpacking multi-GB weight tensors."""
    findings: list[Finding] = []
    target = str(path)
    try:
        with zipfile.ZipFile(path, "r") as zf, path.open("rb") as raw:
            for info in zf.infolist():
                norm = info.filename.replace("\\", "/")
                if norm.startswith("/") or ".." in Path(norm).parts:
                    findings.append(
                        Finding("CRITICAL", "MODEL-ZIP-02", f"{target}:{info.filename}", "Path-traversal entry inside model archive")
                    )
                if info.flag_bits & 0x1:
                    findings.append(
                        Finding("HIGH", "MODEL-ZIP-03", f"{target}:{info.filename}", "Encrypted ZIP entry hides payload from scanners")
                    )

                # Compare local header CRC-32 against central directory CRC (CVE-2025-10155 parser-discrepancy defense).
                raw.seek(info.header_offset)
                local_hdr = raw.read(30)
                if len(local_hdr) == 30 and local_hdr[:4] == b"PK\x03\x04":
                    _, _, _, _, _, _, local_crc, _, _, _, _ = struct.unpack("<IHHHHHIIIHH", local_hdr)
                    if local_crc != info.CRC or (info.file_size > 0 and (local_crc == 0 or info.CRC == 0)):
                        findings.append(
                            Finding(
                                "CRITICAL",
                                "MODEL-ZIP-01",
                                f"{target}:{info.filename}",
                                f"ZIP CRC-32 anomaly (local={local_crc:#x}, central={info.CRC:#x}, size={info.file_size})",
                            )
                        )

                if norm.lower().endswith((".pkl", ".pickle")):
                    with zf.open(info, "r") as member:
                        head = member.read(_HEADER_READ_BYTES)
                    if _DANGEROUS_PICKLE_RE.search(head):
                        findings.append(
                            Finding(
                                "CRITICAL",
                                "MODEL-PKL-02",
                                f"{target}:{info.filename}",
                                "Archived pickle references executable module callables (os/subprocess/eval)",
                            )
                        )
    except zipfile.BadZipFile as exc:
        findings.append(Finding("CRITICAL", "MODEL-ZIP-BAD", target, f"Corrupt or non-standard ZIP archive: {exc}"))
    return findings


def scan_model_artifact(path: Path) -> list[Finding]:
    """Perform fast O(header) serialization and format-integrity audit on a model file."""
    findings: list[Finding] = []
    target = str(path)
    ext = path.suffix.lower()
    size = path.stat().st_size

    with path.open("rb") as f:
        head = f.read(_HEADER_READ_BYTES)

    is_zip = head.startswith(b"PK\x03\x04")
    has_pickle_magic = bool(_PICKLE_MAGIC_RE.match(head)) and any(op in head[:512] for op in (b"\x93", b"R", b"c", b"\x81", b"\x92"))
    has_ascii_pickle = head.startswith(b"c") and b"\n" in head[:256] and (has_pickle_magic or _DANGEROUS_PICKLE_RE.search(head) is not None)

    if ext in {".safetensors", ".gguf", ".onnx"} and (is_zip or has_pickle_magic or has_ascii_pickle):
        findings.append(
            Finding("CRITICAL", "MODEL-SPOOF-01", target, f"Extension spoofing: {ext} file begins with Pickle/ZIP serialization bytes")
        )

    if is_zip:
        findings.extend(_inspect_zip_archive(path))
        return findings

    if has_pickle_magic or has_ascii_pickle or ext in {".pkl", ".pickle", ".dill"}:
        if _DANGEROUS_PICKLE_RE.search(head):
            findings.append(
                Finding("CRITICAL", "MODEL-PKL-01", target, "Pickle stream contains dangerous callable/module opcode imports")
            )
        elif ext in {".pkl", ".pickle", ".dill"}:
            findings.append(
                Finding("HIGH", "MODEL-PKL-LEGACY", target, "Unsafe executable serialization format; prefer Safetensors or GGUF")
            )
        return findings

    if ext == ".safetensors":
        if size < 10:
            findings.append(Finding("CRITICAL", "MODEL-ST-01", target, "Truncated Safetensors header (<10 bytes)"))
            return findings
        header_len = struct.unpack("<Q", head[:8])[0]
        if header_len < 2 or header_len > _MAX_SAFETENSORS_HEADER or 8 + header_len > size:
            findings.append(
                Finding("CRITICAL", "MODEL-ST-01", target, f"Invalid Safetensors metadata length {header_len} (file size {size})")
            )
            return findings
        with path.open("rb") as f:
            f.seek(8)
            raw_hdr = f.read(header_len)
        try:
            meta = json.loads(raw_hdr.decode("utf-8"))
            if not isinstance(meta, dict):
                raise ValueError("Safetensors header must be a JSON object")
        except Exception as exc:
            findings.append(Finding("CRITICAL", "MODEL-ST-02", target, f"Unreadable/corrupt Safetensors JSON header: {exc}"))
            return findings
        if isinstance(meta.get("__metadata__"), dict):
            for k, val in _iter_strings(meta["__metadata__"], "__metadata__"):
                if _STEGO_RE.search(val) or _TOOL_POISON_RE.search(val):
                    findings.append(
                        Finding("HIGH", "MODEL-ST-META", f"{target}:{k}", "Suspicious hidden text or prompt directive in __metadata__")
                    )

    elif ext == ".gguf":
        if len(head) < 8 or head[:4] != b"GGUF":
            findings.append(Finding("CRITICAL", "MODEL-GGUF-01", target, "Missing GGUF magic bytes"))
        else:
            ver = struct.unpack("<I", head[4:8])[0]
            if ver not in (1, 2, 3):
                findings.append(Finding("HIGH", "MODEL-GGUF-02", target, f"Unsupported GGUF format version {ver}"))

    return findings


def _load_pins(pin_path: Path | None) -> dict[str, str] | None:
    if pin_path is None:
        return None
    data = json.loads(pin_path.read_text(encoding="utf-8"))
    if "cryptographicProvenance" in data and isinstance(data["cryptographicProvenance"].get("mcpSchemaHashes"), dict):
        return dict(data["cryptographicProvenance"]["mcpSchemaHashes"])
    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items()}
    raise ValueError(f"Unsupported pins JSON format in {pin_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mcp", type=Path, action="append", default=[], help="MCP config / manifest JSON file or directory")
    parser.add_argument("--model", type=Path, action="append", default=[], help="Model weight file or directory")
    parser.add_argument("--pins", type=Path, help="Evidence Pack or server->sha256 map JSON to verify MCP schema hashes")
    parser.add_argument("--emit-pins", type=Path, help="Print canonical mcpSchemaHashes JSON for an MCP file")
    parser.add_argument("--json", action="store_true", dest="json_out", help="Emit findings as JSON")
    parser.add_argument(
        "--fail-on",
        choices=("CRITICAL", "HIGH", "MEDIUM", "NEVER"),
        default="HIGH",
        help="Minimum severity triggering non-zero exit (default: HIGH)",
    )
    args = parser.parse_args()

    if args.emit_pins:
        doc = json.loads(args.emit_pins.read_text(encoding="utf-8"))
        print(json.dumps(extract_mcp_server_hashes(doc), indent=2, sort_keys=True))
        return 0

    pins = _load_pins(args.pins)
    findings: list[Finding] = []

    for target in args.mcp:
        paths = sorted(target.rglob("*.json")) if target.is_dir() else [target]
        for p in paths:
            findings.extend(scan_mcp_document(json.loads(p.read_text(encoding="utf-8")), str(p), pinned_hashes=pins))

    for target in args.model:
        paths = sorted(p for p in target.rglob("*") if p.is_file()) if target.is_dir() else [target]
        for p in paths:
            findings.extend(scan_model_artifact(p))

    if args.json_out:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        for f in findings:
            print(f"[{f.severity}] {f.rule_id} ({f.target}): {f.message}")
        if not findings:
            print("OK ai_security_scan: 0 findings")

    rank = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "NEVER": 99}
    cutoff = rank[args.fail_on]
    if any(rank.get(f.severity, 0) >= cutoff for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
