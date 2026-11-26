# Controlled Evaluation Benchmark

Reproducible, self-contained evaluation suite ([`scripts/eval_benchmark.py`](../scripts/eval_benchmark.py)) measuring detection recall, false-positive rate (FPR), execution latency, and admission policy accuracy across deterministic adversarial CVE-pattern fixtures and benign/multilingual edge cases.

> **Honest methodology boundary:** This benchmark evaluates controlled, synthetic CVE-class binary/JSON/YAML fixtures constructed from documented vulnerability mechanics and tricky benign edge cases inside the repository. It does **not** claim to represent longitudinal multi-organization production telemetry across enterprise deployments. Use it as a fast, deterministic regression gate alongside dedicated production scanners (`ModelScan`, `Garak`, `Promptfoo`, `Kyverno`).

---

## Summary Metrics (Measured Locally)

Command executed:

```bash
python scripts/eval_benchmark.py --conftest-bin <conftest_0.71.1> --json
```

| Metric | Value | Notes |
|---|---:|---|
| **Total scanner evaluation cases** | **16** | `11` adversarial (`8` model serialization + `3` MCP) + `5` benign/multilingual |
| **True Positives (TP) / False Negatives (FN)** | **11 / 0** | `Recall (TPR) = 1.000 (100.0%)` |
| **False Positives (FP) / True Negatives (TN)** | **0 / 5** | `False Positive Rate (FPR) = 0.000 (0.0%)` |
| **Median per-artifact scan latency** | **0.909 ms** | `max = 8.115 ms` (`std` library only, O(header)/bounded stream) |
| **Conftest admission policy accuracy** | **7 / 7 (100.0%)** | Evaluated across `schemas/examples/` and `policies/testdata/` (`Conftest 0.71.1`) |

---

## Per-Case Breakdown (`ai_security_scan.py`)

| Case ID | Category | Expected Flag | Detected | Matched Rules | Latency (ms) | Vulnerability Class / Benign Edge Case |
|---|---|:---:|:---:|---|---:|---|
| `pkl_memo_asyncio_cve_2025_10157` | `model` | True | True | `MODEL-PKL-01` | 0.892 | `MEMOIZE` + `BINGET` stack-tracked `asyncio` call evasion (`CVE-2025-10157` class) |
| `safetensors_pickle_spoof` | `model` | True | True | `MODEL-PKL-01`, `MODEL-SPOOF-01` | 0.819 | Pickle payload disguised with `.safetensors` extension |
| `zip_polyglot_crc_lfh_cve_2025_1945` | `model` | True | True | `MODEL-PKL-02`, `MODEL-ZIP-01`, `MODEL-ZIP-04`, `MODEL-ZIP-BAD` | 1.864 | Zip Local-vs-Central filename mismatch + CRC anomaly (`CVE-2025-1945` / `CVE-2025-10156` class) |
| `gguf_past_64kb_attr_ssti_cve_2024_34359` | `model` | True | True | `MODEL-GGUF-SSTI` | 2.699 | GGUF `tokenizer.chat_template` Jinja2 `\|attr()` SSTI past 64 KB (`CVE-2024-34359` class) |
| `onnx_varint_traversal_cve_2024_5187` | `model` | True | True | `MODEL-ONNX-TRAV` | 1.026 | ONNX `external_data.location` path traversal (`CVE-2024-5187` class) |
| `safetensors_offset_overlap` | `model` | True | True | `MODEL-ST-03` | 0.742 | Safetensors overlapping `data_offsets` tensor corruption |
| `npy_object_pickle_cve_2019_6446` | `model` | True | True | `MODEL-NPY-OBJ` | 0.909 | NumPy `.npy` `|O` object dtype triggering implicit pickle load (`CVE-2019-6446` class) |
| `hf_auto_map_remote_code` | `model` | True | True | `MODEL-HF-AUTOMAP` | 0.862 | HuggingFace `config.json` `auto_map` remote code hook |
| `mcp_unicode_nfkc_comment_poison` | `mcp` | True | True | `MCP-POISON-01`, `MCP-UNI-01` | 0.079 | Unicode Tag smuggling (`U+E0000`) + NFKC/HTML-comment hidden tool poison |
| `mcp_ssrf_decimal_shadow_wildcard` | `mcp` | True | True | `MCP-AUTHZ-01`, `MCP-SSRF-01`, `MCP-TLS-01`, `MCP09-SHADOW-01`, `MCP09-SHADOW-02` | 0.125 | Decimal IP `2852039166` SSRF + cleartext URL + unpinned `npx` + colliding name + `*` auto-approve |
| `mcp_rugpull_schema_drift` | `mcp` | True | True | `MCP-RUGPULL-01` | 0.036 | Canonical `tools/list` schema SHA-256 mismatch (`MCP09` rug pull) |
| `benign_streamed_zip_and_dict_pkl` | `model` | False | False | `—` | 8.115 | Benign streamed 5 MB PyTorch checkpoint zip containing primitive dictionary weights |
| `benign_32k_vocab_gguf` | `model` | False | False | `—` | 6.824 | Benign GGUF header with `32,000` vocabulary array items |
| `benign_64mb_sparse_safetensors` | `model` | False | False | `—` | 2.208 | Large sparse Safetensors header declaring 64 MB buffer bounds validly |
| `benign_jinja_chat_template` | `model` | False | False | `—` | 2.555 | Standard clean Jinja2 Llama-style `chat_template` without SSTI gadgets |
| `benign_persian_zwnj_and_pinned_ipv6` | `mcp` | False | False | `—` | 0.284 | Legitimate Persian ZWNJ (`U+200C`) description + pinned local `[::1]` MCP server |

---

## Reproducing Locally & In CI

`scripts/verify_repo.py` executes the scanner benchmark automatically during every CI run (`python scripts/verify_repo.py --require-conftest --with-mkdocs`), ensuring regressions in recall, latency bounds, or benign false positives fail the build immediately.

See [`STANDARDS-ALIGNMENT.md`](STANDARDS-ALIGNMENT.md) for how these rules enforce `MLS-*` Conformance Profile levels and OWASP `AISVS` categories.
