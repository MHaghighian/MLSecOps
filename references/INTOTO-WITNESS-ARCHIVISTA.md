# in-toto, DSSE, Witness & Archivista Supply-Chain Architecture

This guide documents how **MLSecOps Release Evidence Packs** compose cleanly with the CNCF **in-toto Attestation Framework v1**, **DSSE (`Dead Simple Signing Envelope`)**, **Witness** (`in-toto/witness`), and **Archivista** (`in-toto/archivista`) across `CP 5`, `CP 7`, `CP 8 ↔ CP 9` admission, and private audit retrieval.

> **Why combine them with Sigstore / CycloneDX?** Standard model-signing answers *"who signed this weight file?"*; **in-toto + Witness + Archivista** answer *"which exact source commit (`git`), inputs (`material`), evaluation exit code (`command-run`), Evidence Pack (`CP 4/7/8`), and outputs (`product`) formed a tamper-evident chain — without leaking proprietary model metadata to a public transparency log."*

---

## 1. Layered Cryptographic Stack

| Layer | Specification / Tool | Artifact / Schema in This Repo | Role |
|---|---|---|---|
| **Layer 4: Signed Policy + Graph Store** | **Witness** + **Archivista** (`witness run` / `witness verify`, `archivistactl`) | [`policies/witness/mlsecops-witness-policy.json`](../policies/witness/mlsecops-witness-policy.json) · [Witness Guide](../policies/witness/README.md) | Attests live step execution, indexes DSSE envelopes into a queryable GraphQL + blob store, verifies multi-step `material → product` links |
| **Layer 3: Cryptographic Envelope** | **DSSE** (`payloadType: "application/vnd.in-toto+json"`) | [`schemas/dsse-envelope.v1.schema.json`](../schemas/dsse-envelope.v1.schema.json) · [`evidence-pack.dsse.example.json`](../schemas/examples/intoto/evidence-pack.dsse.example.json) | Signs UTF-8 statement bytes using **PAE** (`DSSEv1 <len(type)> <type> <len(payload)> <payload>`) via Cosign, file keys, Fulcio OIDC, or HSM |
| **Layer 2: Statement Binding** | **in-toto Statement v1** (`https://in-toto.io/Statement/v1`) | [`schemas/mlsecops-attestation.v1.schema.json`](../schemas/mlsecops-attestation.v1.schema.json) · [`evidence-pack.intoto.example.json`](../schemas/examples/intoto/evidence-pack.intoto.example.json) | Binds immutable `subject[].digest` (`ResourceDescriptor`, matched strictly by digest) to `predicateType` + `predicate` |
| **Layer 1: AI Control Predicate** | **MLSecOps Evidence Pack** (`CycloneDX 1.6/1.7` themes + `MLS-*`) | [`schemas/evidence-pack.schema.json`](../schemas/evidence-pack.schema.json) · [`policies/cp8_cp9_admission.rego`](../policies/cp8_cp9_admission.rego) | Captures AI-specific gates (`CP4` data/RAG, `CP7` red-team/misalignment, `CP8 ↔ CP9` digest bind, `MCP09`, `E.1.8` `DDP/FSDP/RLHF`) |

---

## 2. Canonical Data Structures (Verified Against Upstream Specs)

### A. `in-toto` Statement v1 (`spec/v1/statement.md` & `resource_descriptor.md`)

- `_type` MUST equal `"https://in-toto.io/Statement/v1"`.
- `subject` is a non-empty array of `ResourceDescriptor` objects. Each `ResourceDescriptor` MUST include **`digest`** (lowercase hex, e.g., `sha256`, `sha512`); `name`, `uri`, `downloadLocation`, `mediaType`, and `annotations` are optional metadata. Matching relies strictly on immutable cryptographic digest.
- `predicateType` for MLSecOps Evidence Packs uses `"https://mhaghighian.github.io/MLSecOps/attestation/evidence-pack/v1"`.
- Generate locally with [`scripts/ai_security_scan.py`](../scripts/README.md):
  ```bash
  python scripts/ai_security_scan.py --emit-intoto schemas/examples/evidence-pack.example.json
  ```

### B. DSSE Envelope & Pre-Authentication Encoding (`PAE`)

Instead of signing raw JSON whitespace directly, **DSSE** wraps the UTF-8 `Statement v1` bytes in Base64 inside `payload` alongside `payloadType: "application/vnd.in-toto+json"` and `signatures[]`. Both Witness and Archivista verify signatures over the exact **DSSEv1 PAE** byte sequence:

```text
DSSEv1 <byte_len(payloadType)> <payloadType> <byte_len(payload)> <payload_bytes>
```

Emit a canonical unsigned DSSE wrapper ready for Witness / Cosign / HSM signing:

```bash
python scripts/ai_security_scan.py --emit-dsse schemas/examples/evidence-pack.example.json
```

### C. Witness Collections (`https://witness.dev/attestations/collection/v0.1`) & Policy Format

During `witness run --step <name>`, Witness executes configured **attestors** (`git`, `material`, `product`, `command-run`, `slsa`) and wraps the collected claims inside an in-toto DSSE Statement whose `predicateType` is `"https://witness.dev/attestations/collection/v0.1"`.

- In a **Witness JSON policy** ([`policies/witness/mlsecops-witness-policy.json`](../policies/witness/mlsecops-witness-policy.json)), each step lists trusted `functionaries` (`publickey` / key root) and required attestation `type` URIs with **Base64-encoded** `regopolicies[].module` scripts defining a `deny[msg]` rule evaluated against that sub-attestation's JSON (`package commandrun`, `package git`, etc.).
- Passing verification requires **empty** `deny` sets plus valid cryptographic signatures matching a trusted functionary across unbroken `material → product` digests.

### D. Archivista Storage & GraphQL Discovery (`in-toto/archivista`)

Because public Sigstore `Rekor` transparency logs expose hashes and signer identities globally (see [Chapter 5 confidentiality warning](../chapters-en/05-model-artifact-supply-chain.md#provenance-and-signing)), proprietary ML organizations can run a private **Archivista** instance (`ARCHIVISTA_ENABLE_GRAPHQL=TRUE` and `ARCHIVISTA_ENABLE_SQL_STORE=TRUE`):

| Operation | HTTP / CLI Interface | Notes |
|---|---|---|
| **Auto-upload on step completion** | `witness run ... --enable-archivista --archivista-server https://archivista.internal` | Default upstream URL is `https://archivista.testifysec.io`; override for private deployments (`--archivista-headers "Authorization=Bearer ..."` if authenticated) |
| **Store DSSE envelope manually** | `archivistactl store <attestation.json>` or `POST /v1/upload` | Indexes subject digests in SQL + stores raw DSSE object in S3/filesystem, returning the envelope `gitoid` |
| **Query provenance graph** | `POST /query` GraphQL: `{ subjects { edges { node { name subjectDigests { algorithm value } } } } }` | Lets `witness verify` traverse all upstream build/eval steps linked to a model digest |
| **Download / offline bundle** | `archivistactl retrieve envelope <gitoid>` or `GET /v1/download/{gitoid}` | Supports air-gapped registry verification or compliance archival |
| **Verify at `CP 9` admission** | `witness verify --policy policy-signed.json --publickey pub.pem --artifactfile model.safetensors --enable-archivista --archivista-server ...` | Combine with `conftest test --policy policies evidence-pack.json` for semantic AI gates |

---

## 3. End-to-End MLSecOps Gate Mapping

1. **Before `witness run` (`CP 4` / `CP 5`):** Dataset manifests, model base weights, and configs are hashed by the Witness `material` attestor and source state by `git`.
2. **During `witness run --step cp7-cp9-gate` (`CP 7`):** Static scanning (`ai_security_scan.py`) and red-team suites execute cleanly; `command-run` captures non-spoofable `exitcode == 0` while `product` hashes outputs (including Evidence Pack JSON).
3. **At `CP 8 ↔ CP 9` Admission:**
   - Wrap the final Evidence Pack as DSSE (`--emit-dsse` or signed via Witness/Cosign) and store in private **Archivista**.
   - Run **both** `witness verify` (proving cryptographic chain integrity from git/materials to checkpoint & non-zero exit rejection) **and** `conftest test --policy policies` (proving `agentMisalignmentScore <= 0.15`, `boundToCp9Digest` match, `MCP09` schema pinning, and `E.1.8` cluster isolation).
