#!/usr/bin/env python3
"""Fast, zero-dependency static security scanner for MCP manifests/configs and ML model artifacts.

Detects 2025-2026 MLSecOps attack surfaces without loading multi-GB model weights into memory:
  1. Invisible Unicode Tag / Bidi / zero-width smuggling (preserving legitimate ZWNJ/ZWJ) & NFKC homoglyph evasion.
  2. MCP tool poisoning, HTML-comment/delimiter smuggling, credential-exfil directives, Shadow MCP unpinned runners,
     cross-map server shadowing, decimal/hex/octal/IPv6 SSRF, cleartext transport, and inline/URL secrets.
  3. Canonical SHA-256 MCP tools/list pinning & rug-pull drift detection (`mcpServers` + VS Code `servers`).
  4. Header-first model serialization & integrity audit: stack+memo-simulated `pickletools` disassembly (Protocol 0-5
     `GLOBAL`/`STACK_GLOBAL`/memo-shuffled gadgets & asyncio/marshal CVE-2025-10157), ZIP polyglots, Local-vs-Central
     header filename spoofing (CVE-2025-1945), CRC-32 anomalies (CVE-2025-10156), path traversal, disguised pickles,
     TorchScript `.py`, Keras `Lambda`, HuggingFace `auto_map` / Jinja2 SSTI, bounded binary GGUF KV walk (CVE-2024-34359
     beyond 64 KB), ONNX protobuf `external_data` traversal (CVE-2024-5187), NumPy `.npy` object pickles, and
     Safetensors offset-overlap / bounds integrity.
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
    r"(?:<\s*/?\s*(?:important|system|instructions?|secret)\b[^>]*>)"
    r"|(?:\[(?:SYSTEM|IMPORTANT)\]|<\|(?:im_start\|system|system)\|?>)"
    r"|(?:<!--.*?(?:ignore|override|exfiltrate|do not (?:tell|mention)|curl|wget|ssh|token|secret).*?-->)"
    r"|(?:ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions)"
    r"|(?:override\s+(?:the\s+)?system\s+prompt)"
    r"|(?:(?:do\s+not|never)\s+(?:tell|mention|show|inform)\s+(?:the\s+)?user|(?:without|before)\s+(?:telling|informing|letting)\s+(?:the\s+)?user)"
    r"|(?:before\s+(?:calling|invoking|using)\s+any\s+other\s+tool|(?:instead\s+of|rather\s+than)\s+calling)"
    r"|(?:~/\.(?:ssh|gitconfig|netrc|docker/config\.json)|/etc/(?:passwd|shadow)|\.aws/credentials|\.kube/config|\.(?:npmrc|pypirc|env)\b|\bid_rsa\b|/var/run/secrets/kubernetes\.io/serviceaccount/token)"
    r"|(?:\b(?:curl|wget)\b[^\n]*(?:https?://|\|)|base64\s+(?:-d|--decode)\s*\||/dev/tcp/|\bnc\s+-e\b)"
)

_SECRET_LITERAL_RE = re.compile(
    r"(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|A(?:KIA|SIA)[0-9A-Z]{16}|(?:https?|wss?)://[^/\s:@]+:[^/\s@]{4,}@)"
)
_EXEMPT_HASH_KEY_RE = re.compile(
    r"(?:^|\.)(?:mcpSchemaHashes(?:\.[^.]+)?|currentSchemaHash|sha256Digest|configSnapshotHash|vectorIndexVersionHash|modelOciDigest)(?:\[\d+\])?(?:<key>)?$"
)

_SSRF_HOST_RE = re.compile(
    r"(?i)(?:169\.254\.169\.254|169\.254\.170\.2|100\.100\.100\.200|metadata\.google\.internal|metadata\.azure\.internal|fd00:ec2::254)"
)
_URL_IN_TEXT_RE = re.compile(r"(?i)\b(?:https?|wss?)://[^\s\"'<>]+")
_CLEARTEXT_REMOTE_RE = re.compile(r"(?i)^(?:http|ws)://(?!(?:localhost|127\.0\.0\.1|\[::1\])(?::|/|$))")
_SHELL_META_RE = re.compile(r"(?:&&|\|\||[;`|]|\$\()")
_UNPINNED_PKG_RE = re.compile(r"^(@[^/]+/)?[A-Za-z0-9._-]+$")
_URL_EMBEDDED_IPV4_OCTET = re.compile(r"(?:0x[0-9a-f]+|0[0-7]*|[1-9][0-9]*)", re.I)

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
    "asyncio",
    "marshal",
    "types",
    "runpy",
    "ctypes",
    "pdb",
    "code",
    "cProfile",
    "profile",
    "shutil",
    "pip",
    "ensurepip",
    "xmlrpc",
    "distutils",
    "setuptools",
}
_DANGEROUS_MOD_PREFIXES = ("torch.hub", "numpy.f2py", "numpy.testing", "urllib.request", "http.client")
_DANGEROUS_QUALNAMES = {
    "uuid._get_command_stdout",
    "yaml.load",
    "yaml.unsafe_load",
    "jsonpickle.decode",
    "pickle.loads",
    "_pickle.loads",
    "dill.loads",
    "cloudpickle.loads",
    "torch.load",
    "torch.serialization.load",
    "numpy.load",
}
_DANGEROUS_ATTRS = {
    "system",
    "popen",
    "Popen",
    "check_output",
    "check_call",
    "getoutput",
    "getstatusoutput",
    "spawn",
    "spawnl",
    "execv",
    "execve",
    "eval",
    "exec",
    "execfile",
    "__import__",
    "getattr",
    "__subclasses__",
    "attrgetter",
    "methodcaller",
    "FunctionType",
    "CodeType",
    "InteractiveInterpreter",
}

_TORCHSCRIPT_DANGEROUS_RE = re.compile(
    r"(?m)\b(?:os\.system|os\.popen|subprocess\.|__import__|eval\s*\(|exec\s*\(|socket\.socket|ctypes\.)\b"
)
_JINJA_SSTI_RE = re.compile(
    r"(?is)(?:\{\{|\{%).*?(?:__globals__|__subclasses__|__builtins__|__import__|__mro__|__base__|__init__|__code__|__closure__|__dict__|__getattribute__|\\x5f\\x5f|\|\s*attr\s*\(|(?:cycler|lipsum|joiner|namespace)\b).*?(?:\}\}|%\})"
)
_ONNX_TRAV_TAIL_RE = re.compile(rb"(?:\.\.[\\/]|%2e%2e|/(?:etc|root|proc|home|var|app)/|\\\\[a-z0-9_.-]+|[A-Za-z]:[\\/])", re.I)

_HEADER_READ_BYTES = 65_536
_GGUF_READ_BYTES = 8 * 1024 * 1024
_ONNX_TAIL_BYTES = 1024 * 1024
_MAX_METADATA_ENTRY_BYTES = 2 * 1024 * 1024
_MAX_SAFETENSORS_HEADER = 100 * 1024 * 1024

_PUSH_PLACEHOLDER = object()
_MARK = object()
_ALIBABA_METADATA_IP = ipaddress.IPv4Address("100.100.100.200")


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
    return unicodedata.normalize("NFKC", _STRIP_INVIS_RE.sub("", text))


def _decode_obfuscated_ip(host: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    host = host.rstrip(".")
    try:
        return ipaddress.ip_address(host)
    except ValueError:
        pass
    try:
        if "." in host:
            parts = host.split(".")
            if len(parts) == 4 and all(_URL_EMBEDDED_IPV4_OCTET.fullmatch(p) for p in parts):
                octets = [
                    int(p, 16) if p.lower().startswith("0x") else (int(p, 8) if len(p) > 1 and p.startswith("0") else int(p, 10))
                    for p in parts
                ]
                if all(0 <= o <= 255 for o in octets):
                    return ipaddress.IPv4Address(bytes(octets))
        else:
            num = (
                int(host, 16)
                if host.lower().startswith("0x")
                else (int(host, 8) if len(host) > 1 and host.startswith("0") else (int(host, 10) if host.isdigit() else -1))
            )
            if 0 <= num <= 0xFFFFFFFF:
                return ipaddress.IPv4Address(num)
    except ValueError:
        return None
    return None


def _has_ssrf_target(text: str) -> bool:
    """Detect literal metadata hostnames and decimal/octal/hex/IPv4-mapped SSRF URLs."""
    if _SSRF_HOST_RE.search(text):
        return True
    for m in _URL_IN_TEXT_RE.finditer(text):
        raw_url = m.group(0).rstrip(".,;)]}")
        try:
            host = urlsplit(raw_url).hostname
        except ValueError:
            continue
        if not host:
            continue
        addr = _decode_obfuscated_ip(host)
        if addr is not None:
            if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped:
                addr = addr.ipv4_mapped
            if addr.is_link_local or addr.is_unspecified or addr == _ALIBABA_METADATA_IP:
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
    base = Path(cmd_l).name

    if _SHELL_META_RE.search(joined) or (
        base in {"sh", "bash", "zsh", "cmd", "cmd.exe", "powershell", "pwsh"}
        and any(a.lower() in {"-c", "/c", "-enc", "-encodedcommand"} for a in arg_strs)
    ):
        findings.append(
            Finding("CRITICAL", "MCP-EXEC-01", server_label, "Shell wrapper or metacharacters in stdio MCP command/args")
        )

    pkg_tokens = [a for a in arg_strs if a and not a.startswith("-")]
    if base in {"npx", "npx.cmd", "bunx", "pnpx"}:
        for pkg in pkg_tokens:
            if _UNPINNED_PKG_RE.match(pkg):
                findings.append(
                    Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned {base} package {pkg!r} enables supply-chain drift")
                )
                break
    elif base == "uvx" and pkg_tokens and _UNPINNED_PKG_RE.match(pkg_tokens[0]):
        findings.append(
            Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned uvx tool {pkg_tokens[0]!r}; pin @version or ==version")
        )
    elif base == "pipx" and len(pkg_tokens) >= 2 and pkg_tokens[0] == "run" and _UNPINNED_PKG_RE.match(pkg_tokens[1]):
        findings.append(
            Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned pipx run tool {pkg_tokens[1]!r}; pin ==version")
        )
    elif base == "uv" and pkg_tokens[:2] == ["tool", "run"] and len(pkg_tokens) >= 3 and _UNPINNED_PKG_RE.match(pkg_tokens[2]):
        findings.append(
            Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Unpinned uv tool run package {pkg_tokens[2]!r}; pin @version or ==version")
        )
    elif base in {"docker", "podman"} and pkg_tokens and pkg_tokens[0] == "run":
        img = pkg_tokens[-1]
        if "@sha256:" not in img:
            findings.append(
                Finding("HIGH", "MCP09-SHADOW-01", server_label, f"Container MCP runner {base} run image {img!r} is not digest-pinned (@sha256:)")
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
        if _SECRET_LITERAL_RE.search(text) and not _EXEMPT_HASH_KEY_RE.search(jpath):
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

    seen_norm_names: dict[str, str] = {}
    for map_key, servers in _mcp_server_maps(doc):
        for name, cfg in servers.items():
            label = f"{target}:{map_key}.{name}"
            norm_name = _normalize_for_keyword_scan(str(name)).strip().lower()
            if not norm_name:
                findings.append(Finding("HIGH", "MCP09-SHADOW-02", label, "Empty/whitespace MCP server name"))
            elif norm_name in seen_norm_names:
                findings.append(
                    Finding(
                        "HIGH",
                        "MCP09-SHADOW-02",
                        label,
                        f"Case/whitespace/homoglyph-colliding MCP server name with {seen_norm_names[norm_name]}",
                    )
                )
            else:
                seen_norm_names[norm_name] = f"{map_key}.{name}"
            if not isinstance(cfg, dict):
                continue
            cmd = cfg.get("command")
            if isinstance(cmd, str) and cmd.strip():
                args = cfg.get("args") if isinstance(cfg.get("args"), list) else []
                _check_stdio_command(cmd, args, label, findings)
            if cfg.get("samplingEnabled") is True and cfg.get("samplingBudgetCapped") is not True:
                findings.append(
                    Finding("HIGH", "MCP-SAMP-01", label, "MCP sampling enabled without explicit samplingBudgetCapped=true")
                )
            auto_lists = [cfg.get("autoApprove"), cfg.get("alwaysAllow")]
            if cfg.get("dangerouslySkipPermissions") is True or any(isinstance(lst, list) and "*" in lst for lst in auto_lists):
                findings.append(
                    Finding("HIGH", "MCP-AUTHZ-01", label, "Wildcard autoApprove/alwaysAllow or dangerouslySkipPermissions bypasses human-in-the-loop")
                )

    if doc.get("samplingEnabled") is True and doc.get("samplingBudgetCapped") is not True:
        findings.append(
            Finding("HIGH", "MCP-SAMP-01", target, "MCP sampling enabled without explicit samplingBudgetCapped=true")
        )

    if pinned_hashes is not None:
        observed = extract_mcp_server_hashes(doc)
        rac = doc.get("runtimeAgentConfig")
        if isinstance(rac, dict) and isinstance(rac.get("mcpTools"), list):
            for entry in rac["mcpTools"]:
                if isinstance(entry, dict) and isinstance(entry.get("serverName"), str) and isinstance(entry.get("currentSchemaHash"), str):
                    observed.setdefault(entry["serverName"], entry["currentSchemaHash"])
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


def _is_dangerous_global(mod: str, attr: str) -> bool:
    if mod.split(".")[0] in _DANGEROUS_MODULES:
        return True
    if mod.startswith(_DANGEROUS_MOD_PREFIXES):
        return True
    if f"{mod}.{attr}" in _DANGEROUS_QUALNAMES:
        return True
    return attr in _DANGEROUS_ATTRS


def _pop_to_mark(stack: list[Any]) -> None:
    while stack:
        if stack.pop() is _MARK:
            return


def _inspect_pickle_opcodes(blob: bytes) -> str | None:
    """Abstract VM stack+memo interpreter over stdlib pickletools (Protocol 0-5, zero execution)."""
    stack: list[Any] = []
    memo: dict[int, Any] = {}
    memo_next = 0
    seen_strings: list[str] = []

    push_const_ops = {
        "INT", "BININT", "BININT1", "BININT2", "LONG", "LONG1", "LONG4",
        "FLOAT", "BINFLOAT", "NONE", "NEWTRUE", "NEWFALSE",
        "BYTES", "SHORT_BINBYTES", "BINBYTES", "BINBYTES8", "BYTEARRAY8",
        "EMPTY_LIST", "EMPTY_TUPLE", "EMPTY_DICT", "EMPTY_SET", "FROZENSET",
    }
    str_ops = {"UNICODE", "SHORT_BINUNICODE", "BINUNICODE", "BINUNICODE8", "STRING", "BINSTRING", "SHORT_BINSTRING"}

    try:
        for opcode, arg, _pos in pickletools.genops(io.BytesIO(blob)):
            op = opcode.name
            if op in str_ops and isinstance(arg, str):
                stack.append(arg)
                seen_strings.append(arg)
                if len(seen_strings) > 8:
                    seen_strings.pop(0)
            elif op in push_const_ops:
                stack.append(_PUSH_PLACEHOLDER)
            elif op == "MARK":
                stack.append(_MARK)
            elif op == "POP" and stack:
                stack.pop()
            elif op in {"POP_MARK", "LIST", "TUPLE", "DICT"}:
                _pop_to_mark(stack)
                if op != "POP_MARK":
                    stack.append(_PUSH_PLACEHOLDER)
            elif op == "TUPLE1" and len(stack) >= 1:
                stack[-1:] = [_PUSH_PLACEHOLDER]
            elif op == "TUPLE2" and len(stack) >= 2:
                stack[-2:] = [_PUSH_PLACEHOLDER]
            elif op == "TUPLE3" and len(stack) >= 3:
                stack[-3:] = [_PUSH_PLACEHOLDER]
            elif op == "DUP" and stack:
                stack.append(stack[-1])
            elif op in {"PUT", "BINPUT", "LONG_BINPUT"} and isinstance(arg, int):
                memo[arg] = stack[-1] if stack else _PUSH_PLACEHOLDER
            elif op == "MEMOIZE":
                memo[memo_next] = stack[-1] if stack else _PUSH_PLACEHOLDER
                memo_next += 1
            elif op in {"GET", "BINGET", "LONG_BINGET"} and isinstance(arg, int):
                stack.append(memo.get(arg, _PUSH_PLACEHOLDER))
            elif op == "OBJ":
                _pop_to_mark(stack)
                stack.append(_PUSH_PLACEHOLDER)
            elif op in {"REDUCE", "NEWOBJ"} and len(stack) >= 2:
                del stack[-2:]
                stack.append(_PUSH_PLACEHOLDER)
            elif op == "NEWOBJ_EX" and len(stack) >= 3:
                del stack[-3:]
                stack.append(_PUSH_PLACEHOLDER)
            elif op in {"BUILD", "APPEND"} and stack:
                stack.pop()
            elif op in {"APPENDS", "ADDITEMS", "SETITEMS"}:
                _pop_to_mark(stack)
            elif op == "SETITEM" and len(stack) >= 2:
                del stack[-2:]
            elif op in {"GLOBAL", "INST"} and isinstance(arg, str):
                mod, _, attr = arg.partition(" ")
                if not attr:
                    mod, _, attr = arg.partition("\n")
                if _is_dangerous_global(mod, attr):
                    return f"{op} {mod}.{attr}"
                if op == "INST":
                    _pop_to_mark(stack)
                stack.append((mod, attr))
            elif op == "STACK_GLOBAL":
                attr = stack.pop() if stack else _PUSH_PLACEHOLDER
                mod = stack.pop() if stack else _PUSH_PLACEHOLDER
                if isinstance(mod, str) and isinstance(attr, str) and _is_dangerous_global(mod, attr):
                    return f"STACK_GLOBAL({mod}.{attr})"
                stack.append((mod, attr))
            elif op in {"EXT1", "EXT2", "EXT4"}:
                return f"{op} extension registry lookup"
    except Exception:
        for s in seen_strings:
            if s.split(".")[0] in _DANGEROUS_MODULES or s.startswith(_DANGEROUS_MOD_PREFIXES) or s in _DANGEROUS_ATTRS:
                return f"partial-stream reference {s!r}"
    return None


def _looks_like_pickle(head: bytes, min_opcodes: int = 1) -> bool:
    """Verify leading bytes represent a valid Pickle protocol header + opcodes."""
    if len(head) >= 2 and head[0] == 0x80 and 2 <= head[1] <= 5:
        if min_opcodes <= 1:
            return True
    elif not head.startswith((b"c", b"(dp", b"}q", b"]q", b"\x89", b"I")):
        return False

    try:
        ops = []
        for idx, (op, _, _) in enumerate(pickletools.genops(io.BytesIO(head[:256])), start=1):
            ops.append(op.name)
            if idx >= max(min_opcodes, 3):
                break
        return len(ops) >= min_opcodes
    except Exception:
        return len(head) >= 2 and head[0] == 0x80 and 2 <= head[1] <= 5 and min_opcodes <= 1


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


def _inspect_model_json_metadata(name: str, data: Any, target: str) -> list[Finding]:
    """Check HuggingFace config.json (`auto_map`), Keras `Lambda`, and `tokenizer_config.json` SSTI."""
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
        templates = (
            [tmpl]
            if isinstance(tmpl, str)
            else ([t.get("template", "") for t in tmpl if isinstance(t, dict)] if isinstance(tmpl, list) else [])
        )
        for t in templates:
            if isinstance(t, str) and (_JINJA_SSTI_RE.search(t) or _STEGO_RE.search(t)):
                out.append(
                    Finding("CRITICAL", "MODEL-SSTI-01", target, "Jinja2 chat_template contains SSTI/code-execution gadget or hidden control chars")
                )
    return out


def _read_zip_member_bytes(zf: zipfile.ZipFile, raw: Any, info: zipfile.ZipInfo, max_bytes: int) -> tuple[bytes | None, str | None]:
    """Read up to max_bytes from a ZIP member, falling back to raw STORED data on LFH header tampering."""
    try:
        with zf.open(info, "r") as member:
            return member.read(max_bytes), None
    except zipfile.BadZipFile as exc:
        if info.compress_type == zipfile.ZIP_STORED:
            raw.seek(info.header_offset)
            lh = raw.read(30)
            if len(lh) == 30 and lh[:4] == b"PK\x03\x04":
                _, _, _, _, _, _, _, _, _, fn_len, extra_len = struct.unpack("<IHHHHHIIIHH", lh)
                raw.seek(info.header_offset + 30 + fn_len + extra_len)
                to_read = min(max_bytes, info.file_size) if info.file_size > 0 else max_bytes
                return raw.read(to_read), f"{exc} (inspected raw STORED stream)"
        return None, str(exc)


def _inspect_zip_archive(path: Path) -> list[Finding]:
    """Inspect ZIP headers, LFH/CD parity, encrypted/traversal entries, pickles, code, and configs."""
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
                    _, _, _, lfh_flags, _, _, local_crc, _, _, lfh_fn_len, _ = struct.unpack("<IHHHHHIIIHH", local_hdr)
                    local_fn = raw.read(lfh_fn_len).decode("utf-8", errors="replace") if lfh_fn_len else ""
                    if local_fn and local_fn != info.filename:
                        findings.append(
                            Finding(
                                "CRITICAL",
                                "MODEL-ZIP-04",
                                f"{target}:{info.filename}",
                                f"ZIP Local/Central filename mismatch (local={local_fn!r}, central={info.filename!r}; CVE-2025-1945 pattern)",
                            )
                        )
                    has_data_desc = bool((info.flag_bits & 0x8) or (lfh_flags & 0x8))
                    if (not has_data_desc and local_crc != info.CRC) or (info.file_size > 0 and (info.CRC == 0 or (not has_data_desc and local_crc == 0))):
                        findings.append(
                            Finding(
                                "CRITICAL",
                                "MODEL-ZIP-01",
                                f"{target}:{info.filename}",
                                f"ZIP CRC-32 anomaly (local={local_crc:#x}, central={info.CRC:#x}, size={info.file_size})",
                            )
                        )

                low = norm.lower()
                fname = Path(low).name
                if low.endswith((".pkl", ".pickle")):
                    head, err = _read_zip_member_bytes(zf, raw, info, _MAX_METADATA_ENTRY_BYTES)
                    if err:
                        findings.append(Finding("HIGH", "MODEL-ZIP-BAD", f"{target}:{info.filename}", err))
                    if head:
                        hit = _inspect_pickle_opcodes(head)
                        if hit:
                            findings.append(
                                Finding("CRITICAL", "MODEL-PKL-02", f"{target}:{info.filename}", f"Archived pickle dangerous opcode: {hit}")
                            )
                elif low.endswith(".py") and info.file_size <= _MAX_METADATA_ENTRY_BYTES:
                    raw_py, err = _read_zip_member_bytes(zf, raw, info, _MAX_METADATA_ENTRY_BYTES)
                    if err:
                        findings.append(Finding("HIGH", "MODEL-ZIP-BAD", f"{target}:{info.filename}", err))
                    if raw_py and _TORCHSCRIPT_DANGEROUS_RE.search(raw_py.decode("utf-8", errors="replace")):
                        findings.append(
                            Finding("CRITICAL", "MODEL-CODE-01", f"{target}:{info.filename}", "Embedded archive Python code invokes system/exec primitives")
                        )
                elif fname in {"config.json", "tokenizer_config.json"} and info.file_size <= _MAX_METADATA_ENTRY_BYTES:
                    raw_cfg, err = _read_zip_member_bytes(zf, raw, info, _MAX_METADATA_ENTRY_BYTES)
                    if err:
                        findings.append(Finding("HIGH", "MODEL-ZIP-BAD", f"{target}:{info.filename}", err))
                    if raw_cfg is not None:
                        try:
                            cfg = json.loads(raw_cfg.decode("utf-8"))
                            findings.extend(_inspect_model_json_metadata(info.filename, cfg, f"{target}:{info.filename}"))
                        except Exception as exc:
                            findings.append(
                                Finding("HIGH", "MODEL-JSON-BAD", f"{target}:{info.filename}", f"Malformed JSON metadata in archive: {exc}")
                            )
                elif not info.is_dir() and info.file_size >= 4:
                    peek, err = _read_zip_member_bytes(zf, raw, info, 64)
                    if err:
                        findings.append(Finding("HIGH", "MODEL-ZIP-BAD", f"{target}:{info.filename}", err))
                    if peek and _looks_like_pickle(peek, min_opcodes=3):
                        body, _ = _read_zip_member_bytes(zf, raw, info, _MAX_METADATA_ENTRY_BYTES)
                        if body:
                            hit = _inspect_pickle_opcodes(body)
                            if hit:
                                findings.append(
                                    Finding(
                                        "CRITICAL",
                                        "MODEL-PKL-02",
                                        f"{target}:{info.filename}",
                                        f"Disguised archived pickle dangerous opcode: {hit}",
                                    )
                                )
    except zipfile.BadZipFile as exc:
        findings.append(Finding("CRITICAL", "MODEL-ZIP-BAD", target, f"Corrupt or non-standard ZIP archive: {exc}"))
    return findings


def _check_safetensors_offsets(meta: dict[str, Any], payload_len: int, target: str) -> list[Finding]:
    """Validate Safetensors tensor offsets are non-negative, non-overlapping, and in bounds."""
    spans: list[tuple[int, int, str]] = []
    for name, info in meta.items():
        if name == "__metadata__":
            continue
        if not isinstance(info, dict) or not isinstance(info.get("data_offsets"), list) or len(info["data_offsets"]) != 2:
            return [Finding("CRITICAL", "MODEL-ST-03", target, f"Malformed tensor descriptor for {name!r}")]
        begin, end = info["data_offsets"]
        if isinstance(begin, bool) or isinstance(end, bool) or not isinstance(begin, int) or not isinstance(end, int) or begin < 0 or end < begin or end > payload_len:
            return [Finding("CRITICAL", "MODEL-ST-03", target, f"Out-of-bounds Safetensors offsets {info['data_offsets']} on {name!r}")]
        if end > begin:
            spans.append((begin, end, str(name)))

    spans.sort()
    prev_end = 0
    prev_name = ""
    for begin, end, name in spans:
        if begin < prev_end:
            return [
                Finding("CRITICAL", "MODEL-ST-03", target, f"Overlapping Safetensors tensor buffers between {prev_name!r} and {name!r}")
            ]
        prev_end = end
        prev_name = name
    return []


def _walk_gguf_templates(blob: bytes) -> tuple[bool, list[str], str | None]:
    """Safely walk GGUF KV metadata header (past huge token arrays) up to blob limit."""
    ver = struct.unpack_from("<I", blob, 4)[0]
    if ver not in (1, 2, 3):
        return False, [], f"Unsupported GGUF format version {ver}"
    pair_fmt = "<II" if ver == 1 else "<QQ"
    count_fmt = "<I" if ver == 1 else "<Q"
    count_sz = struct.calcsize(count_fmt)
    if len(blob) < 8 + count_sz * 2:
        return False, [], "Truncated GGUF header"

    tensor_count, kv_count = struct.unpack_from(pair_fmt, blob, 8)
    if kv_count > 100_000 or tensor_count > 1_000_000:
        return False, [], f"Suspicious GGUF header counts (tensors={tensor_count}, kv={kv_count})"
    if kv_count == 0:
        return True, [], None

    pos = 8 + count_sz * 2
    limit = len(blob)
    scalar_sizes = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 4, 7: 1, 10: 8, 11: 8, 12: 8}
    templates: list[str] = []

    def read_u32() -> int | None:
        nonlocal pos
        if pos + 4 > limit:
            return None
        val = struct.unpack_from("<I", blob, pos)[0]
        pos += 4
        return val

    def read_len() -> int | None:
        nonlocal pos
        if pos + count_sz > limit:
            return None
        val = struct.unpack_from(count_fmt, blob, pos)[0]
        pos += count_sz
        return val

    for _ in range(min(kv_count, 8192)):
        klen = read_len()
        if klen is None or klen > 4096 or pos + klen > limit:
            break
        key = blob[pos : pos + klen].decode("utf-8", errors="ignore")
        pos += klen
        vtype = read_u32()
        if vtype is None:
            break
        if vtype in scalar_sizes:
            pos += scalar_sizes[vtype]
        elif vtype == 8:
            slen = read_len()
            if slen is None or pos + slen > limit:
                break
            if "template" in key.lower() and slen <= _MAX_METADATA_ENTRY_BYTES:
                templates.append(blob[pos : pos + slen].decode("utf-8", errors="ignore"))
            pos += slen
        elif vtype == 9:
            elem_type = read_u32()
            alen = read_len()
            if elem_type is None or alen is None or alen > 2_000_000:
                break
            if elem_type in scalar_sizes:
                step = alen * scalar_sizes[elem_type]
                if pos + step > limit:
                    break
                pos += step
            elif elem_type == 8:
                is_tmpl_arr = "template" in key.lower()
                ok = True
                for _ in range(alen):
                    slen = read_len()
                    if slen is None or pos + slen > limit:
                        ok = False
                        break
                    if is_tmpl_arr and slen <= _MAX_METADATA_ENTRY_BYTES:
                        templates.append(blob[pos : pos + slen].decode("utf-8", errors="ignore"))
                    pos += slen
                if not ok:
                    break
            else:
                break
        else:
            break
        if pos > limit:
            break

    return True, templates, None


def _read_varint(buf: bytes, pos: int) -> tuple[int, int]:
    val = 0
    shift = 0
    limit = len(buf)
    while pos < limit and shift <= 35:
        b = buf[pos]
        pos += 1
        val |= (b & 0x7F) << shift
        if not (b & 0x80):
            return val, pos
        shift += 7
    return -1, pos


def _scan_onnx_traversal(sample: bytes) -> str | None:
    """Detect ONNX external_data.location path traversal regardless of string length (>32 byte varint safe)."""
    idx = 0
    while True:
        hit = sample.find(b"location", idx)
        if hit == -1:
            break
        after = hit + 8
        if after < len(sample) and sample[after] == 0x12:  # protobuf field #2 wire type LEN
            slen, val_start = _read_varint(sample, after + 1)
            if 1 <= slen <= 4096 and val_start + slen <= len(sample):
                loc = sample[val_start : val_start + slen].decode("utf-8", errors="ignore")
                low = loc.replace("\\", "/").lower()
                if ".." in Path(low).parts or "%2e%2e" in low or loc.startswith(("/", "\\\\", "~")) or re.match(r"^[a-z]:[/\\]", loc, re.I):
                    return loc
        # Fallback for textual/non-standard field separators
        snippet = sample[after : after + 256]
        m = _ONNX_TRAV_TAIL_RE.search(snippet)
        if m and m.start() <= 16:
            return snippet[:64].decode("utf-8", errors="ignore")
        idx = after
    return None


def scan_model_artifact(path: Path) -> list[Finding]:
    """Perform fast O(header) serialization and format-integrity audit on a model file."""
    findings: list[Finding] = []
    target = str(path)
    if path.is_symlink():
        findings.append(Finding("HIGH", "MODEL-SYMLINK-01", target, "Model artifact path is a symbolic link"))
        return findings

    ext = path.suffix.lower()
    size = path.stat().st_size

    if ext == ".json" and path.name.lower() in {"config.json", "tokenizer_config.json"} and size <= _MAX_METADATA_ENTRY_BYTES:
        try:
            meta_json = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(Finding("HIGH", "MODEL-JSON-BAD", target, f"Malformed model metadata JSON: {exc}"))
            return findings
        findings.extend(_inspect_model_json_metadata(path.name, meta_json, target))
        return findings

    with path.open("rb") as f:
        head = f.read(_HEADER_READ_BYTES)

    is_zip = head.startswith(b"PK\x03\x04") or zipfile.is_zipfile(path)
    has_pickle = (not is_zip) and _looks_like_pickle(head)

    if ext in {".safetensors", ".gguf", ".onnx"} and (is_zip or has_pickle):
        findings.append(
            Finding("CRITICAL", "MODEL-SPOOF-01", target, f"Extension spoofing: {ext} file begins with or contains Pickle/ZIP serialization")
        )

    if is_zip:
        findings.extend(_inspect_zip_archive(path))
        return findings

    if head.startswith(b"\x93NUMPY") or ext == ".npy":
        nl = head.find(b"\n")
        if nl != -1 and (b"'|O'" in head[:nl] or b'"|O"' in head[:nl] or b"'O'" in head[:nl]):
            findings.append(
                Finding("HIGH", "MODEL-NPY-OBJ", target, "NumPy .npy object dtype triggers pickle deserialization (CVE-2019-6446 class)")
            )
            hit = _inspect_pickle_opcodes(head[nl + 1 :])
            if hit:
                findings.append(Finding("CRITICAL", "MODEL-PKL-01", target, f"Dangerous Pickle opcode inside .npy object array: {hit}"))
        return findings

    if has_pickle or ext in {".pkl", ".pickle", ".dill"}:
        if size > len(head):
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
        findings.extend(_check_safetensors_offsets(meta, size - 8 - header_len, target))
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
            with path.open("rb") as f:
                gguf_hdr = f.read(_GGUF_READ_BYTES)
            ok, templates, err = _walk_gguf_templates(gguf_hdr)
            if not ok and err:
                findings.append(Finding("HIGH", "MODEL-GGUF-02", target, err))
            for tmpl in templates:
                if _JINJA_SSTI_RE.search(tmpl) or _STEGO_RE.search(tmpl):
                    findings.append(
                        Finding("CRITICAL", "MODEL-GGUF-SSTI", target, "Binary GGUF header metadata embeds Jinja2 SSTI payload (CVE-2024-34359 class)")
                    )
                    break
            else:
                if b"{{" in head or b"{%" in head:
                    hdr_text = head.decode("utf-8", errors="ignore")
                    if _JINJA_SSTI_RE.search(hdr_text):
                        findings.append(
                            Finding("CRITICAL", "MODEL-GGUF-SSTI", target, "Binary GGUF header metadata embeds Jinja2 SSTI payload (CVE-2024-34359 class)")
                        )

    elif ext == ".onnx":
        if size <= _MAX_METADATA_ENTRY_BYTES:
            onnx_sample = path.read_bytes()
        else:
            with path.open("rb") as f:
                first = f.read(_ONNX_TAIL_BYTES)
                f.seek(max(0, size - _ONNX_TAIL_BYTES))
                last = f.read(_ONNX_TAIL_BYTES)
            onnx_sample = first + b"\n" + last
        trav = _scan_onnx_traversal(onnx_sample)
        if trav:
            findings.append(
                Finding("CRITICAL", "MODEL-ONNX-TRAV", target, f"ONNX external_data location contains path-traversal sequence ({trav!r}; CVE-2024-5187 class)")
            )

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
        if not target.exists():
            findings.append(Finding("HIGH", "SCAN-MISSING", str(target), "Target MCP path does not exist"))
            continue
        paths = sorted(target.rglob("*.json")) if target.is_dir() else [target]
        for p in paths:
            if p.is_symlink():
                findings.append(Finding("HIGH", "MCP-SYMLINK-01", str(p), "MCP manifest path is a symbolic link"))
                continue
            try:
                doc = json.loads(p.read_text(encoding="utf-8"))
                if not isinstance(doc, dict):
                    findings.append(Finding("HIGH", "MCP-JSON-BAD", str(p), "MCP JSON root must be an object"))
                else:
                    findings.extend(scan_mcp_document(doc, str(p), pinned_hashes=pins))
            except Exception as exc:
                findings.append(Finding("CRITICAL", "MCP-JSON-BAD", str(p), f"Malformed JSON manifest: {exc}"))

    for target in args.model:
        if not target.exists():
            findings.append(Finding("HIGH", "SCAN-MISSING", str(target), "Target model path does not exist"))
            continue
        paths = sorted(p for p in target.rglob("*") if p.is_file() or p.is_symlink()) if target.is_dir() else [target]
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
