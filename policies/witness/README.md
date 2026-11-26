# Witness & Archivista Policy Samples (`policies/witness/`)

Executable **Witness** (`in-toto/witness`) policy template and workflow wiring **in-toto Attestations**, **DSSE Envelopes**, **Witness step collections (`https://witness.dev/attestations/collection/v0.1`)**, and **Archivista** graph provenance storage alongside MLSecOps `CP 7 / CP 8 ↔ CP 9` gates.

- Template file: [`mlsecops-witness-policy.json`](mlsecops-witness-policy.json)
- Detailed architecture & protocol reference: [`references/INTOTO-WITNESS-ARCHIVISTA.md`](../../references/INTOTO-WITNESS-ARCHIVISTA.md)
- Companion schemas: [`schemas/mlsecops-attestation.v1.schema.json`](../../schemas/mlsecops-attestation.v1.schema.json) · [`schemas/dsse-envelope.v1.schema.json`](../../schemas/dsse-envelope.v1.schema.json)

---

## 1. What [`mlsecops-witness-policy.json`](mlsecops-witness-policy.json) verifies

In **Witness**, step policies define required attestor URIs inside a signed `https://witness.dev/attestations/collection/v0.1` envelope plus **Base64-encoded** embedded OPA Rego modules (`regopolicies[].module`) that fail closed when `deny[msg]` matches:

| Attestor Type | Enforced Check | Rationale |
|---|---|---|
| `https://witness.dev/attestations/git/v0.1` | Denies non-empty `input.status` (dirty git workspace) | Prevents untracked local patches from slipping into released checkpoints |
| `https://witness.dev/attestations/material/v0.1` | Records pre-step input file SHA-256 digests | Binds dataset/config inputs into the provenance graph |
| `https://witness.dev/attestations/product/v0.1` | Records post-step output file SHA-256 digests | Binds model weights and Evidence Pack outputs |
| `https://witness.dev/attestations/command-run/v0.1` | Denies `input.exitcode != 0` (`package commandrun`) | Proves the `CP 7` evaluation / `CP 9` packaging command succeeded without bypass |

> **Why Rego inside JSON is Base64-encoded (and kept separate from `policies/*.rego`):** Witness policy JSON stores `regopolicies[].module` in Base64 and evaluates Rego modules written with `deny[msg] { ... }` (`package commandrun` / `package git`), whereas Conftest (`v0.71+` / OPA `v1`) evaluates `policies/cp8_cp9_admission.rego`. Keeping this template under `policies/witness/` prevents Conftest dialect collisions while allowing `scripts/verify_repo.py` and `tests/test_ai_security_scan.py` to decode and validate every embedded module automatically.

---

## 2. CI / CD & Admission Commands

Before verifying with `witness verify`, sign `mlsecops-witness-policy.json` with your release authority key (`REPLACE-WITH-KEY-SHA256` populated with the public key ID / PEM) and replace sample DSSE envelopes:

```bash
# 1. Wrap CP7 / Evidence Pack generation inside Witness + push DSSE collection to private Archivista
witness run \
  --step cp7-cp9-gate \
  --attestations git,material,product,command-run \
  --signer-file-key-path signer.pem \
  --enable-archivista \
  --archivista-server https://archivista.internal.example \
  -o cp7-cp9.witness.json \
  -- python scripts/ai_security_scan.py --mcp configs/mcp.json --model dist/model.safetensors --fail-on HIGH

# 2. Wrap the release Evidence Pack in an in-toto Statement v1 or DSSE envelope (ready for Cosign / Archivista)
python scripts/ai_security_scan.py --emit-intoto schemas/examples/evidence-pack.example.json > evidence-pack.intoto.json
python scripts/ai_security_scan.py --emit-dsse schemas/examples/evidence-pack.example.json > evidence-pack.dsse.json

# 3. Verify artifact & provenance graph at CP9 admission using signed policy + Archivista
witness verify \
  --policy policy-signed.json \
  --publickey policy-pub.pem \
  --artifactfile dist/model.safetensors \
  --enable-archivista \
  --archivista-server https://archivista.internal.example
```

Pair `witness verify` (step provenance + materials/products chain) with `conftest test --policy policies evidence-pack.json` (AI-specific `CP4`/`CP7`/`CP8↔CP9`/`MCP09`/`E.1.8` admission rules).
