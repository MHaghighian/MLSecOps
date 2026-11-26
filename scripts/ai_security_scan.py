#!/usr/bin/env python3
"""Fast, zero-dependency static security scanner for MCP manifests/configs and ML model artifacts.

Detects 2025-2026 MLSecOps attack surfaces without loading multi-GB model weights into memory:
  1. Invisible Unicode Tag / Bidi / zero-width smuggling (preserving legitimate ZWNJ/ZWJ) & NFKC homoglyph evasion.
  2. MCP tool poisoning, credential-exfil directives, Shadow MCP unpinned runners, obfuscated SSRF, cleartext transport, and inline secrets.
  3. Canonical SHA-256 MCP tools/list pinning & rug-pull drift detection (mcpServers + VS Code servers).
  4. Header-first model serialization audit: pickletools opcode disassembly (Protocol 0-5 STACK_GLOBAL/EOP),
     ZIP CRC-32 anomalies (CVE-2025-10155), path-traversal ZIP entries, TorchScript code/*.py, Keras Lambda, and Safetensors/GGUF checks.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import ipaddress
import json
import pickletools
import re
import struct
import sys
import unicodedata
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

# Smuggling chars: Unicode Tag block (U+E0000..U+E007F), Bidi overrides/isolates, ZWSP/LRM/RLM/WJ/BOM-in-text.
# Intentionally preserves U+200C (ZWNJ) and U+200D (ZWJ) used in legitimate Persian/Arabic/Emoji text.
_STEGO_RE = re.compile(r"[\U000E0000-\U000E007F\u202A-\u202E\u2066-\u2069\u200B\u200E\u200F\u2060\uFEFF]")
_STRIP_INVIS_RE = re.compile(r"[\U000E0000-\U000E007F\u200B-\u200F\u202A-\u202E\u2060\u2066-\u2069\uFEFF]")

_TOOL_POISON_RE = re.compile(
    r"(?is)"
    r"(?:<\s*/?\s*important\b[^>]*>)"
    r"|(?:ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions)"
    r"|(?:override\s+(?:the\s+)?system\s+prompt)"
    r"|(?:do\s+not\s+(?:tell|mention|show|inform)\s+(?:the\s+)?user)"
    r"|(?:before\s+(?:calling|invoking|using)\s+any\s+other\s+tool)"
    r"|(?:~/\.ssh|/etc/(?:passwd|shadow)|\.aws/credentials|\.kube/config|\.(?:npmrc|pypirc)\b|\bid_rsa\b)"
    r"|(?:\b(?:curl|wget)\b[^\n]*(?:https?://|\|)|/dev/tcp/|\bnc\s+-e\b)"
)

_SECRET_LITERAL_RE = re.compile(
    r"(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})"
)

_SSRF_HOST_RE = re.compile(r"(?i)(?:169\.254\.169\.254|100\.100\.100\.200|metadata\.google\.internal|fd00:ec2::254)")
_URL_IN_TEXT_RE = re.compile(r"(?i)\b(?:https?|wss?)://[^\s\"'<>]+")
_CLEARTEXT_REMOTE_RE = re.compile(r"(?i)^(?:http|ws)://(?!(?:localhost|127\.0\.0\.1|\[::1\])(?::|/|$))")
_SHELL_META_RE = re.compile(r"(?:&&|\|\||[;`|]|\$\()")
_UNPINNED_NPX_RE = re.compile(r"^(@[^/]+/)?[A-Za-z0-9._-]+$")
_UNPINNED_UVX_RE = re.compile(r"^[A-Za-z0-9._-]+$")

_DANGEROUS_MODULES = {
    "posix",
    "nt",
    "os",
    "subprocess",
    "builtins",
    "__builtin__",
    "pty",
    "socket",
    "webbrowser",
    "codecs",
    "commands",
    "importlib",
    "operator",
    "sys",
}
_DANGEROUS_ATTRS = {
    "system",
    "popen",
    "Popen",
    "run",
    "call",
    "check_output",
    "eval",
    "exec",
    "__import__",
    "getattr",
    "__subclasses__",
    "attrgetter",
    "methodcaller",
    "decode",
}
_TORCHSCRIPT_DANGEROUS_RE = re.compile(r"(?m)\b(?:os\.system|subprocess\.|__import__|eval\s*\(|exec\s*\(|socket\.socket)\b")
_JINJA_SSTI_RE = re.compile(
    r"(?is)\{\{.*?(?:__globals__|__subclasses__|__builtins__|__import__|__mro__|__class__\s*\.\s*__base__|(?:cycler|lipsum|joiner|namespace)\.__init__).*?\}\}"
    r"|\{%.*?(?:__globals__|__subclasses__|__import__).*?%\}"
)
_HEADER_READ_BYTES = 65_536
_MAX_METADATA_ENTRY_BYTES = 2 * 1024 * 1024
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
        elif cp in (0x200B, 0x200E, 0x200F, 0x2060, 0xFEFF) and "zero-width" not in hits:
            hits.append("zero-width")
        if len(hits) == 3:
            break
    return hits


def _normalize_for_keyword_scan(text: str) -> str:
    """Strip invisible chars and fold NFKC homoglyphs before pattern matching."""
    stripped = _STRIP_INVIS_RE.sub("", text)
    return unicodedata.normalize("NFKC", stripped)


def _has_ssrf_target(text: str) -> bool:
    """Detect both literal metadata hostnames and decimal/hex/IPv4-mapped SSRF URLs."""
    if _SSRF_HOST_RE.search(text):
        return True
    for m in _URL_IN_TEXT_RE.finditer(text):
        try:
            host = urlsplit(m.group(0)).hostname
        except ValueError:
            continue
        if not host:
            continue
        addr: ipaddress.IPv4Address | ipaddress.IPv6Address | None = None
        try:
            addr = ipaddress.ip_address(host)
        except ValueError:
            # Handle decimal (2852039166), hex (0xa9fea9fe), or mixed-radix dotted IPv4 (0251.0376.0251.0376).
            try:
                if "." in host:
                    parts = host.split(".")
                    if len(parts) == 4 and all(re.fullmatch(r"(?:0x[0-9a-f]+|0[0-7]*|[1-9][0-9]*)", p, re.I) for p in parts):
                        octets = [int(p, 16) if p.lower().startswith("0x") else (int(p, 8) if len(p) > 1 and p.startswith("0") else int(p, 10)) for p in parts]
                        if all(0 <= o <= 255 for o in octets):
                            addr = ipaddress.IPv4Address(bytes(octets))
                else:
                    num = int(host, 16) if host.lower().startswith("0x") else (int(host, 8) if len(host) > 1 and host.startswith("0") else (int(host, 10) if host.isdigit() else -1))
                    if 0 <= num <= 0xFFFFFFFF:
                        addr = ipaddress.IPv4Address(num)
            except ValueError:
                addr = None
        if addr is not None:
            if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped:
                addr = addr.ipv4_mapped
            if addr.is_link_local or addr.is_unspecified:
                return True
    return False


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


def _mcp_server_maps(doc: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Support both Claude/Cursor `mcpServers` and VS Code `servers` schemas."""
    out: list[tuple[str, dict[str, Any]]] = []
    for key in ("mcpServers", "servers"):
        mapping = doc.get(key)
        if isinstance(mapping, dict):
            out.append((key, mapping))
    return out


def extract_mcp_server_hashes(doc: dict[str, Any]) -> dict[str, str]:
    """Extract canonical SHA-256 hashes for any server declaring a `tools` array."""
    hashes: dict[str, str] = {}
    for _, servers in _mcp_server_maps(doc):
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
    if base in {"npx", "npx.cmd"}:
        for pkg in pkg_tokens:
            if _UNPINNED_NPX_RE.match(pkg):
                findings.append(
                    Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned npx package {pkg!r} enables supply-chain drift")
                )
                break
    elif base == "uvx" and pkg_tokens:
        if _UNPINNED_UVX_RE.match(pkg_tokens[0]):
            findings.append(
                Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned uvx tool {pkg_tokens[0]!r}; pin @version or ==version")
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
        normalized = _normalize_for_keyword_scan(text)
        if _TOOL_POISON_RE.search(normalized):
            findings.append(
                Finding("CRITICAL", "MCP-POISON-01", f"{target}:{jpath}", "Suspected tool-poisoning directive or credential-exfil pattern")
            )
        if _SECRET_LITERAL_RE.search(text) and "mcpSchemaHashes" not in jpath and "Hash" not in jpath:
            findings.append(
                Finding("CRITICAL", "MCP-SEC-01", f"{target}:{jpath}", "Inline API token or credential literal detected")
            )
        if _has_ssrf_target(normalized):
            findings.append(
                Finding("CRITICAL", "MCP-SSRF-01", f"{target}:{jpath}", "Cloud metadata / SSRF target address detected")
            )
        is_endpoint_field = jpath.endswith((".url", ".endpoint", ".uri")) or jpath in {"url", "endpoint", "uri"} or ".args[" in jpath
        if is_endpoint_field and _CLEARTEXT_REMOTE_RE.search(text.strip()):
            findings.append(
                Finding("HIGH", "MCP-TLS-01", f"{target}:{jpath}", f"Cleartext remote MCP endpoint {text!r}")
            )

    for map_key, servers in _mcp_server_maps(doc):
        for name, cfg in servers.items():
            if not isinstance(cfg, dict):
                continue
            label = f"{target}:{map_key}.{name}"
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


def _inspect_pickle_opcodes(blob: bytes) -> str | None:
    """Disassemble pickle opcodes via stdlib pickletools (Protocol 0-5, zero execution)."""
    recent_strings: list[str] = []
    try:
        for opcode, arg, _pos in pickletools.genops(io.BytesIO(blob)):
            op_name = opcode.name
            if op_name in {"GLOBAL", "INST"} and isinstance(arg, str):
                mod, _, attr = arg.partition(" ")
                if not attr:
                    mod, _, attr = arg.partition("\n")
                if mod.split(".")[0] in _DANGEROUS_MODULES or attr in _DANGEROUS_ATTRS:
                    return f"{op_name} {arg!r}"
            elif op_name in {"UNICODE", "SHORT_BINUNICODE", "BINUNICODE", "STRING", "BINSTRING", "SHORT_BINSTRING"} and isinstance(arg, str):
                recent_strings.append(arg)
                if len(recent_strings) > 4:
                    recent_strings.pop(0)
            elif op_name == "STACK_GLOBAL" and len(recent_strings) >= 2:
                mod, attr = recent_strings[-2], recent_strings[-1]
                if mod.split(".")[0] in _DANGEROUS_MODULES or attr in _DANGEROUS_ATTRS:
                    return f"STACK_GLOBAL({mod}.{attr})"
            elif op_name in {"EXT1", "EXT2", "EXT4"}:
                return f"{op_name} extension registry lookup"
    except Exception:
        # Fallback if a pickle stream ends right past the read window after pushing suspicious globals.
        for s in recent_strings:
            if s in _DANGEROUS_MODULES or s in _DANGEROUS_ATTRS:
                return f"partial-stream reference {s!r}"
    return None


def _looks_like_pickle(head: bytes) -> bool:
    """Verify leading bytes represent a valid Pickle protocol header + opcodes."""
    if len(head) >= 2 and head[0] == 0x80 and 2 <= head[1] <= 5:
        return True
    if head.startswith((b"c", b"(dp", b"}q", b"]q", b"\x89", b"I")):
        try:
            ops = [op.name for op, _, _ in zip(pickletools.genops(io.BytesIO(head[:256])), range(3))]
            return bool(ops)
        except Exception:
            return False
    return False


def _has_keras_lambda(node: Any) -> bool:
    stack = [node]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if cur.get("class_name") == "Lambda":
                return True
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return False


def _inspect_zip_archive(path: Path) -> list[Finding]:
    """Inspect ZIP headers & lightweight code/pickle/config entries without unpacking multi-GB weights."""
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

                low = norm.lower()
                if low.endswith((".pkl", ".pickle")):
                    with zf.open(info, "r") as member:
                        head = member.read(_MAX_METADATA_ENTRY_BYTES)
                    hit = _inspect_pickle_opcodes(head)
                    if hit:
                        findings.append(
                            Finding("CRITICAL", "MODEL-PKL-02", f"{target}:{info.filename}", f"Archived pickle dangerous opcode: {hit}")
                        )
                elif low.endswith(".py") and info.file_size <= _MAX_METADATA_ENTRY_BYTES:
                    with zf.open(info, "r") as member:
                        src = member.read(_MAX_METADATA_ENTRY_BYTES).decode("utf-8", errors="replace")
                    if _TORCHSCRIPT_DANGEROUS_RE.search(src):
                        findings.append(
                            Finding("CRITICAL", "MODEL-CODE-01", f"{target}:{info.filename}", "Embedded archive Python code invokes system/exec primitives")
                        )
                elif Path(low).name in {"config.json", "tokenizer_config.json"} and info.file_size <= _MAX_METADATA_ENTRY_BYTES:
                    try:
                        with zf.open(info, "r") as member:
                            cfg = json.loads(member.read(_MAX_METADATA_ENTRY_BYTES).decode("utf-8"))
                        findings.extend(_inspect_model_json_metadata(info.filename, cfg, f"{target}:{info.filename}"))
                    except Exception:
                        pass
    except zipfile.BadZipFile as exc:
        findings.append(Finding("CRITICAL", "MODEL-ZIP-BAD", target, f"Corrupt or non-standard ZIP archive: {exc}"))
    return findings


def _inspect_model_json_metadata(name: str, data: Any, target: str) -> list[Finding]:
    """Check HuggingFace config.json (`auto_map`) and tokenizer_config.json (`chat_template` SSTI)."""
    out: list[Finding] = []
    if not isinstance(data, dict):
        return out
    low_name = Path(name).name.lower()
    if low_name == "config.json":
        if "auto_map" in data and isinstance(data["auto_map"], dict) and data["auto_map"]:
            out.append(
                Finding("HIGH", "MODEL-HF-AUTOMAP", target, "config.json defines custom auto_map remote-code loader hooks")
            )
        if _has_keras_lambda(data):
            out.append(
                Finding("HIGH", "MODEL-KERAS-LAMBDA", target, "Keras Lambda layer embeds arbitrary code execution risk")
            )
    elif low_name == "tokenizer_config.json":
        tmpl = data.get("chat_template")
        templates = [tmpl] if isinstance(tmpl, str) else ([t.get("template", "") for t in tmpl if isinstance(t, dict)] if isinstance(tmpl, list) else [])
        for t in templates:
            if isinstance(t, str) and _JINJA_SSTI_RE.search(t):
                out.append(
                    Finding("CRITICAL", "MODEL-SSTI-01", target, "Jinja2 chat_template contains SSTI/code-execution gadget attributes")
                )
    return out


def scan_model_artifact(path: Path) -> list[Finding]:
    """Perform fast O(header) serialization and format-integrity audit on a model file."""
    findings: list[Finding] = []
    target = str(path)
    if path.is_symlink():
        findings.append(Finding("HIGH", "MODEL-SYMLINK-01", target, "Model artifact path is a symbolic link"))
        return findings

    ext = path.suffix.lower()
    size = path.stat().st_size

    if ext == ".json" and Path(target).name.lower() in {"config.json", "tokenizer_config.json"} and size <= _MAX_METADATA_ENTRY_BYTES:
        try:
            meta_json = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return findings
        findings.extend(_inspect_model_json_metadata(path.name, meta_json, target))
        return findings

    with path.open("rb") as f:
        head = f.read(_HEADER_READ_BYTES)

    is_zip = head.startswith(b"PK\x03\x04")
    has_pickle = (not is_zip) and _looks_like_pickle(head)

    if ext in {".safetensors", ".gguf", ".onnx"} and (is_zip or has_pickle):
        findings.append(
            Finding("CRITICAL", "MODEL-SPOOF-01", target, f"Extension spoofing: {ext} file begins with Pickle/ZIP serialization bytes")
        )

    if is_zip:
        findings.extend(_inspect_zip_archive(path))
        return findings

    if has_pickle or ext in {".pkl", ".pickle", ".dill"}:
        # Read up to 2 MB on standalone pickle files to close padding-evasion offsets while keeping scan bounded.
        if size > len(head) and size <= _MAX_METADATA_ENTRY_BYTES:
            head = path.read_bytes()
        elif size > len(head):
            with path.open("rb") as f:
                head = f.read(_MAX_METADATA_ENTRY_BYTES)
        hit = _inspect_pickle_opcodes(head)
        if hit:
            findings.append(Finding("CRITICAL", "MODEL-PKL-01", target, f"Dangerous Pickle opcode chain detected: {hit}"))
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
                norm_val = _normalize_for_keyword_scan(val)
                if _STEGO_RE.search(val) or _TOOL_POISON_RE.search(norm_val):
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
