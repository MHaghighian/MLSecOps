# Companion scripts & verification tooling

Zero-overhead helper scripts and tests backing the **MLSecOps Reference Model & Practical Guide** (Chapters 5, 7, 8, 11, 12, 16, and Appendix E).

| Script / Suite | Purpose | Key flags / usage |
|---|---|---|
| [`ai_security_scan.py`](ai_security_scan.py) | Fast, zero-dependency (`stdlib` only) O(header)/O(N) static scanner for MCP configs/manifests and ML model artifacts | `--mcp`, `--model`, `--pins`, `--emit-pins`, `--json`, `--fail-on {CRITICAL,HIGH,MEDIUM,NEVER}` |
| [`verify_repo.py`](verify_repo.py) | End-to-end QA suite (workflow YAML, BOM/version sync, strict Draft 2020-12 JSON Schema + 5 negative tests, chapter YAML/JSON/Mermaid parity, release manifest coverage, Python `unittest`, scanner smoke check, Conftest verify/fixtures, single-pass `site/` HTML audit) | `--require-conftest`, `--conftest-bin PATH`, `--with-mkdocs` |
| [`generate_release_manifest.py`](generate_release_manifest.py) | Generates and verifies release `SHA256SUMS` over repo content, schemas, policies, scripts, tests, workflows, and `.github/seo/` | `-o SHA256SUMS`, `--verify SHA256SUMS` |
| [`build-docx.py`](build-docx.py) | Compiles the handbook to `dist/MLSecOps-Reference-Model-v{version}.docx` via Pandoc | `--render-mermaid`, `--reference`, `--output`, `--skip-validate` |
| [`mermaid_to_png.py`](mermaid_to_png.py) | Renders `assets/diagrams/source/*.mmd` to PNG fallback images | `--force`, `--quiet`, `--keep-temp` |
| [`restore_mermaid_fences.py`](restore_mermaid_fences.py) | Restores inline Mermaid fences in chapters from `.mmd` sources | See script header |
| `gen_example_{a..d}*.py` | Regenerates hand-crafted Appendix E.7 SVG architecture/flow diagrams | `python scripts/gen_example_c_svgs.py --png` |
| [`tests/test_ai_security_scan.py`](../tests/test_ai_security_scan.py) | Targeted, non-redundant unit tests covering scanner bypasses, polyglots, VM disassembly, SSTI, ONNX varints, SSRF, and CLI behavior | `python -m unittest discover -s tests` |

---

## `ai_security_scan.py` detection coverage

Designed to inspect multi-GB artifacts safely without running `pickle.loads` or executing `stdio` MCP commands:

### MCP manifests & configs (`--mcp`, `--pins`)

| Rule ID | Severity | What it detects |
|---|---|---|
| `MCP-UNI-01` | CRITICAL | Invisible Unicode Tags (`U+E0000..U+E007F`), Bidi overrides/isolates, or zero-width chars (explicitly preserves legitimate Persian/Arabic `ZWNJ` `U+200C` & `ZWJ` `U+200D`) |
| `MCP-POISON-01` | CRITICAL | Tool-poisoning directives, HTML-comment smuggling, NFKC homoglyph/invisible-split keywords, or credential-exfil paths (`~/.ssh`, `/var/run/secrets/kubernetes.io/serviceaccount/token`, etc.) |
| `MCP-SEC-01` | CRITICAL | Inline API/token literals (`sk-`, `hf_`, `ghp_`, `github_pat_`, `glpat-`, `xox*-`, `AKIA`/`ASIA`) and URL `user:pass@` creds (narrowly exempts hash pin fields) |
| `MCP-SSRF-01` | CRITICAL | Cloud metadata SSRF (`169.254.169.254`, `169.254.170.2`, `100.100.100.200`, `metadata.google.internal`, `metadata.azure.internal`, `fd00:ec2::254`, including decimal/octal/hex/IPv6-mapped encodings) |
| `MCP-TLS-01` | HIGH | Cleartext remote `http://` / `ws://` endpoints (allows `localhost` / `127.0.0.1` / `[::1]`) |
| `MCP-EXEC-01` | CRITICAL | Shell wrappers (`sh -c`, `bash -c`, `pwsh -enc`) or shell metacharacters in `stdio` commands/args |
| `MCP09-SHADOW-01` | HIGH | Unpinned `npx`, `uvx`, `bunx`, `pnpx`, `pipx run`, `uv tool run`, or `docker`/`podman run` missing `@sha256:` across `mcpServers` and VS Code `servers` |
| `MCP09-SHADOW-02` | HIGH | Empty, duplicate, or case/whitespace/NFKC-homoglyph-colliding server names across `mcpServers` + `servers` |
| `MCP-SAMP-01` | HIGH | `samplingEnabled: true` without `samplingBudgetCapped: true` |
| `MCP-AUTHZ-01` | HIGH | Wildcard `autoApprove: ["*"]` / `alwaysAllow: ["*"]` or `dangerouslySkipPermissions: true` |
| `MCP09-UNPINNED-01` / `MCP-RUGPULL-01` | CRITICAL | Server missing from pinned `mcpSchemaHashes` or canonical SHA-256 `tools/list` digest drift (supports both MCP manifests and Evidence Pack `runtimeAgentConfig.mcpTools`) |

### Model serialization & header integrity (`--model`)

| Rule ID | Severity | What it detects |
|---|---|---|
| `MODEL-SYMLINK-01` | HIGH | Symbolic-link model artifact path |
| `MODEL-SPOOF-01` | CRITICAL | `.safetensors` / `.gguf` / `.onnx` file containing Pickle or ZIP polyglot bytes |
| `MODEL-PKL-01` / `MODEL-PKL-02` / `MODEL-PKL-LEGACY` | CRITICAL / HIGH | Abstract VM stack+memo `pickletools` Protocol `0–5` disassembly catching `GLOBAL`/`INST`/`STACK_GLOBAL`, `MEMOIZE`/`BINGET`/`BINUNICODE8` obfuscation, `asyncio`/`marshal`/`runpy`/`ctypes` (`CVE-2025-10157` class), plus disguised extensionless pickles inside ZIPs |
| `MODEL-NPY-OBJ` | HIGH | NumPy `.npy` object dtype (`|O`) triggering `pickle` deserialization (`CVE-2019-6446` class) |
| `MODEL-ZIP-01` / `-02` / `-03` / `-04` / `BAD` | CRITICAL / HIGH | CRC-32 anomalies (`CVE-2025-10156`), ZIP path traversal, encrypted members, Local-vs-Central filename spoofing (`CVE-2025-1945`), and corrupt ZIPs with per-member `ZIP_STORED` fallback |
| `MODEL-CODE-01` / `MODEL-KERAS-LAMBDA` | CRITICAL / HIGH | Unsafe `os.system`/`subprocess`/`exec`/`eval` in TorchScript `.py` and Keras `Lambda` layers in `config.json` |
| `MODEL-HF-AUTOMAP` / `MODEL-SSTI-01` / `MODEL-JSON-BAD` | CRITICAL / HIGH | HuggingFace `config.json` `auto_map` hooks, Jinja2 `chat_template` SSTI (including `|attr()` bypasses), and malformed JSON metadata |
| `MODEL-ST-01` / `-02` / `-03` / `MODEL-ST-META` | CRITICAL / HIGH | Truncated/corrupt Safetensors headers, out-of-bounds or overlapping tensor `data_offsets`, and poisoned `__metadata__` |
| `MODEL-GGUF-01` / `-02` / `MODEL-GGUF-SSTI` | CRITICAL / HIGH | Bad magic/version/count overflow and bounded binary KV header walking beyond 64 KB for `tokenizer.chat_template` Jinja2 SSTI (`CVE-2024-34359` class) |
| `MODEL-ONNX-TRAV` | CRITICAL | Varint-safe protobuf + tail-slice scan for `external_data.location` path traversal (`CVE-2024-5187` class) |

### Examples

```bash
# Pin tools/list hashes for an MCP config
python scripts/ai_security_scan.py --emit-pins path/to/mcp.json

# Scan MCP manifests against pinned Evidence Pack hashes and audit model files
python scripts/ai_security_scan.py \
  --mcp path/to/mcp.json \
  --pins schemas/examples/evidence-pack.example.json \
  --model path/to/models/ \
  --json --fail-on HIGH
```
