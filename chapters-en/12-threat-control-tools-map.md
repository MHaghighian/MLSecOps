# Chapter 12: Threat, Control, and Tool Mapping

## Purpose of Mapping

Threat, control, and capability mapping helps teams understand which control is required for each risk and what type of implementation can support it. Specific tools are listed only as **informative examples**. They are not endorsed by this guide, may change over time, and must be validated in the reader's environment before being used for release decisions.

> **Reading note:** The [Primary Mapping](#primary-mapping) and [layered architecture](#layered-tool-architecture) sections are the main reference for threat modeling. Detailed CLI examples are optional and live in the [appendix below](#appendix-informative-tool-command-reference)—skip them unless you are implementing evidence collection.

## Primary Mapping

| Threat | Control | Example capability / non-endorsed tool examples |
| --- | --- | --- |
| `Data Poisoning` | Data validation, lineage, anomaly detection | `Great Expectations`, `Evidently` |
| `PII` leakage | Sensitive data identification and masking | `Presidio`, enterprise `DLP` |
| Poisoned model | Artifact scan and backdoor test | `ModelScan`, internal test |
| Vulnerable dependency | `SCA` and container scan | `Trivy`, `Syft`, `Grype` |
| Secret in code or notebook | Secret scanning | `Gitleaks`, `TruffleHog` |
| `Prompt Injection` | Gateway, red team test, guardrail | `Promptfoo`, `Garak`, internal gateway |
| `RAG Poisoning` | Ingest and retrieval ACL control | Ingest review, policy engine, access-controlled retriever |
| `Tool Abuse` | Intent gate and scoped access | Policy engine, IAM |
| `Memory Poisoning` | Sanitization, TTL, and provenance | Internal memory gateway |
| Runtime leakage | Telemetry and output DLP | `SIEM`, `DLP`, `AI Gateway` |
| `Gradient Leakage` (federated) | Secure aggregation, DP | `TensorFlow Privacy`, `OpenDP` |
| Attack on ML security (IDS/malware) | Adversarial robustness in detection model | `ART`, retraining |
| Multimodal injection | OCR/audio moderation | Multimodal gateway |
| API key for LLM | Proxy gateway, kill switch | HashiCorp `Vault`, cloud secret manager, internal API proxy |
| Autonomous AI Malware | Agent behavior monitoring, sandboxing, runtime restriction | AI Gateway, Agent Monitoring |
| AI Worm Propagation *(emerging)* | Propagation detection, isolation, trust boundaries | Runtime monitoring, EDR/XDR; map to `AML.T0070` / `AML.T0080` patterns—not a single ATLAS worm ID |
| AI-driven Reconnaissance | Asset discovery monitoring, attack surface management | ASM tools, SIEM analytics |
| Autonomous Exploit Generation | Vulnerability intelligence, exploit detection | Threat intelligence platform |
| AI-driven Lateral Movement | Least privilege, segmentation, agent authorization | IAM, Policy Engine |
| Compute Hijacking | GPU workload monitoring, resource anomaly detection | GPU telemetry, infrastructure monitoring |
| MCP tool poisoning | Gateway; schema pin; static + host scan | `mcps-audit`, `mcp-scan` (Snyk Agent Scan), MCP-Shield |
| MCP09 Shadow MCP server | IDE allowlist; registry; Shadow AI program | Ch.11, enterprise MCP gateway |
| MCP rug pull / schema change | Hash pin on `tools/list`; re-consent on change | Gateway + CI scan |
| MCP token exposure | Short-lived OAuth; no secrets in mcp.json | Vault, ThinkWatch, gateway |
| Agent Persistence | Memory validation, session control | Agent gateway, memory security layer |

## Tool Layers



![](../assets/diagrams/12-threat-control-tools-map_01.png)


## Capabilities by lifecycle area

| Lifecycle area | Control capability | Example implementation |
| --- | --- | --- |
| Data ingestion | Schema, PII, quality | `Great Expectations`, `Presidio` |
| Code and notebook | Secret and dependency scan | `Gitleaks`, `Trivy`, `NB Defense` |
| Model | Artifact scan, adversarial test | `ModelScan`, `ART` |
| Supply chain | `SBOM` and signing | `Syft`, `CycloneDX`, `Cosign` |
| Release decisions | Policy-as-code | `OPA`, `Conftest`, internal policy engine |
| Runtime | Guardrail and gateway | `NeMo Guardrails`, `Llama Guard`, internal gateway |
| SOC | Telemetry and detection | `ELK`, `Grafana`, `SIEM` |

## Layered Tool Architecture

| Layer | Role | Lifecycle area | Example tool |
| --- | --- | --- | --- |
| `L1 — Data and Experimentation` | Lineage, versioning, and reproducibility | 2, 5 | `MLflow`, `DVC`, `Great Expectations` |
| `L2 — Security Scanning and Testing` | `SAST/SCA`, artifact scan, IaC, adversarial and LLM testing | 3, 7 | `Gitleaks`, `Trivy`, `Checkov`, `tfsec`, `SonarQube`, `lintML`, `ModelScan`, `ART`, `Garak`, `PyRIT`, `Promptfoo`, `Agentic Security`, `PurpleLlama`, `Mindgard`, `AI-exploits`, `AI-Infra-Guard` |
| `L3 — AI Supply Chain` | `SBOM/AI-BOM`, signing, and provenance | 2, 9 | `Syft`, `CycloneDX`, `Cosign`, `Sigstore`, `SLSA` |
| `L4 — Policy-as-Code` | Release decision and dataset compliance | 4, 8 | `OPA`, `Conftest`, `Kyverno` |
| `L5 — Registry and Deployment` | Signed model storage, secret, and key | 9, 10 | `Model Registry`, `S3/Nexus`, `Vault/KMS` |
| `L6 — Runtime and Guardrails` | Prompt filtering, moderation, and AI gateway | Production | Internal gateway, `NeMo Guardrails`, `Llama Guard`, `Lakera Guard`, `Patronus` |
| `L7 — Observability and SOC` | Drift, alert, and SIEM | 10 | `ELK`, `Grafana`, `Evidently`, `WhyLabs`, `HiddenLayer`, `Protect AI AIRS` |

### Additional runtime controls (L6):

| Control | Purpose |
| --- | --- |
| Agent Behavior Monitoring | Detect abnormal autonomous decisions |
| Tool Execution Policy | Restrict agent actions |
| Runtime Isolation | Prevent propagation between systems |
| Resource Monitoring | Detect unauthorized AI workloads |
| Session Analysis | Detect multi-step attack behavior |

## Appendix: Informative tool command reference

> **Optional section.** The mappings and lifecycle layers above are sufficient for architecture and governance reviews. Use this appendix when selecting tools and drafting evidence-collection commands.

### Design principle: controls must support a documented decision

```text
observe → parse result → decision (pass/fail/exception) → evidence → review

```

A tool that only reports but is never reviewed or tied to a release decision is an `Anti-pattern` (Chapter 9). In automated environments, tools may return `exit code != 0` or structured `JSON`; in manual or managed-service environments, outputs may be reviewed by an approver or GRC workflow. The requirement is **documented decision-making**, not a specific automation mechanism.

### L2 — Model Artifact Scan: ModelScan

Purpose: Detect malicious code and unsafe operations in model files (`pickle`, `H5`, `SavedModel`, `PyTorch`) before `load`.

```bash
pip install modelscan
# Scan a model file or folder
modelscan -p ./models/model.pkl
# JSON output for Evidence Pack
modelscan -p ./models/ -r json -o modelscan-report.json

```

Decision behavior: `modelscan` returns exit codes that can support an automated or manual release decision:

| Exit Code | Meaning | Recommended decision |
| --- | --- | --- |
| `0` | Clean, no vulnerabilities | Continue |
| `1` | Scan successful, **vulnerability found** | Reject or escalate release |
| `2` | Scan error | Investigate and stop |
| `3` | Unsupported file | Warning |
| `4` | Usage error | Fix command |

Evidence: `modelscan-report.json` file. This control maps to lifecycle control point 2 (`Load Artifacts`).

### L2 — Secret Scanning: Gitleaks

Purpose: Find API keys, tokens, and credentials in code, notebooks, and git history.

```bash
# Scan repository and return non-zero if a secret is found
gitleaks detect --source . --report-format json --report-path gitleaks-report.json --exit-code 1

```

Decision behavior: With `--exit-code 1`, finding any secret should reject or escalate the release decision. Evidence: `gitleaks-report.json`.

### L2 — Dependency and Container Scan: Trivy

Purpose: `SCA` for dependencies, container image scan, and IaC misconfiguration.

```bash
# Scan project dependencies
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 .
# Scan inference service image
trivy image --severity CRITICAL --exit-code 1 myorg/llm-serving:1.4.0

```

Decision behavior: `--exit-code 1` combined with `--severity CRITICAL` identifies findings that should block or escalate release. Evidence: output with `--format json`.

### L2 — Notebook Scan: NB Defense and lintML

Purpose: Notebooks and ML code often contain secrets, sensitive output, and unsafe patterns.

```bash
# NB Defense for notebook scanning
pip install nbdefense && nbdefense scan ./notebooks/
# lintML: security linter for ML code (from Nvidia); requires Docker for underlying scanners
pipx run lintml ./src/

```

Decision behavior: Finding a secret or high-risk pattern should block or escalate release. This control maps to lifecycle control point 3.

### L2 — Classic Model Adversarial Test: ART

Purpose: Measure resistance of `Tabular/Vision/Speech` models against manipulated input and compute `ASR`.

```python
from art.estimators.classification import SklearnClassifier
# Use vision/tabular-appropriate attacks only (PGD/FGSM are typical for image models;
# for tabular/text models, select attack classes supported by ART for your modality)
from art.attacks.evasion import FastGradientMethod, ProjectedGradientDescent

classifier = SklearnClassifier(model=model)
attack = ProjectedGradientDescent(estimator=classifier, eps=0.1)
x_adv = attack.generate(x=x_test)
asr = compute_attack_success_rate(model, x_test, x_adv, y_test)
assert asr <= BASELINE_ASR + 0.02, "ASR exceeded threat model threshold"

```


Decision behavior: Compare `ASR` with baseline; exceeding the threat-model threshold should block or escalate release. Evidence: `ASR @ epsilon` report and test set hash.

### L2 — LLM Security Test: Garak

Purpose: Scan `LLM` vulnerabilities with configurable probe plugins (prompt injection, jailbreak, encoding, leakage, toxicity). Probe count varies by version and configuration—see [Garak documentation](https://github.com/NVIDIA/garak) for the current probe list.

```bash
python -m pip install -U garak
# Run OWASP LLM01-related probes on a model
python -m garak --target_type openai --target_name gpt-4o \
  --probes promptinject,dan,encoding,leakreplay \
  --report_prefix garak-ci
# Filter probes by OWASP tag
python -m garak --target_type huggingface --target_name my-model --probe_tags owasp:llm01

```

Decision behavior: `garak` produces a `JSONL` report with success rate per probe; reviewers or automation must compare `bypass rate` with the threat model threshold and block or escalate release if exceeded. Evidence: `garak-ci.report.jsonl`.

### L2 — Red Team and LLM/RAG/Agent Evaluation: Promptfoo

Purpose: Framework-based automated red team with pluggable frameworks (e.g. `owasp:llm`, custom suites). Map organizational policies to tests; **EU AI Act** coverage depends on your own test corpus—do not assume a built-in legal compliance pack without verifying Promptfoo plugin docs for your version.

Example `promptfooconfig.yaml`:

```yaml
targets:
  - id: https
    label: prod-assistant
    config:
      url: https://api.staging.example/llm   # use staging endpoint; authenticate via CI secret
      method: POST
      headers: { 'Content-Type': 'application/json' }
      body: { prompt: '{{prompt}}' }
redteam:
  frameworks:
    - owasp:llm
    - mitre:atlas
  plugins:
    - owasp:llm
    - pii
    - rag-poisoning
  strategies:
    - prompt-injection
    - jailbreak

```

```bash
# Run red team in CI with context logging
npx promptfoo@latest redteam run -c promptfooconfig.yaml -o results.json \
  --tag git.sha="$CI_COMMIT_SHA"

```

Decision behavior: `results.json` output is compared with acceptance threshold (e.g., zero critical bypass). Evidence: `results.json` + commit tag.

### L2 — Multi-Stage Red Team: Microsoft PyRIT

Purpose: Multi-turn attack automation and advanced jailbreak for LLM and agent.

```bash
pip install pyrit
# PyRIT is typically run as an orchestrator script (multi-turn attack)
python redteam/pyrit_orchestrator.py --target prod-assistant --strategy crescendo

```

Decision behavior: Suitable for deep seasonal testing or before major release, not every build. Evidence: conversation report and outcome.

### L2 — MCP Server Static Scan: mcps-audit

Purpose: Scan MCP server source (`.js`, `.ts`, `.py`, `.json`) for OWASP MCP Top 10 and Agentic AI Top 10 anti-patterns before deploy.

```bash
npm install -g mcps-audit
mcps-audit ./services/my-mcp-server
mcps-audit ./services/my-mcp-server --json > mcp-audit.json
```

Decision behavior: Parse CLI exit status and `--json` output; critical MCP01/MCP03/MCP04/MCP05/MCP07 class findings should block or escalate release. Evidence: `mcp-audit.json` in Evidence Pack. Run as part of lifecycle control point 3 for repos that ship MCP servers; pair with MCP gateway at runtime (Ch.7).

Reference: [razashariff/mcps-audit](https://github.com/razashariff/mcps-audit)

### L2 — Installed MCP Config Scan: Snyk Agent Scan (mcp-scan)

Purpose: Discover and scan **installed** MCP configurations (Cursor, Claude Desktop, VS Code, Windsurf, etc.) for tool poisoning, shadowing, and prompt injection in live `tools/list` output.

```bash
export SNYK_TOKEN=your-token
uvx snyk-agent-scan@latest --json > agent-scan.json
uvx snyk-agent-scan@latest ~/.cursor/mcp.json
```

Decision behavior: **Not a model release control** — use for developer workstation audits, MCP09 discovery, and SOC hygiene. Parsing `--json` output is experimental; do not hard-code on issue codes without version pinning. Run inside a **sandbox** when configs are untrusted.

Reference: [invariantlabs-ai/mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) (Snyk Agent Scan)

### L2 — Installed MCP Scan (alternative): MCP-Shield

Purpose: Scan installed MCP servers for tool poisoning, exfiltration channels, and cross-origin escalation — complementary to Agent Scan.

Reference: [riseandignite/mcp-shield](https://github.com/riseandignite/mcp-shield)

### L3 — SBOM Generation: Syft

Purpose: Software dependency inventory for the supply chain.

```bash
# Install
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
# SBOM from project environment and image
syft dir:. -o cyclonedx-json=sbom.cdx.json
syft myorg/llm-serving:1.4.0 -o spdx-json=image-sbom.spdx.json

```

Evidence: `sbom.cdx.json`. This is produced at stages 2 and 9.

### L3 — AI-BOM (ML-BOM) Generation: CycloneDX / cdxgen

Purpose: Beyond SBOM; record model, dataset, prompt, and AI services. The `CycloneDX 1.7` standard (approved 2025, ECMA-424) supports `ML-BOM`.

```bash
# With cdxgen (OWASP CycloneDX project)
# Generate dedicated AI-BOM including model, prompt, and MCP
npx @cyclonedx/cdxgen@latest aibom .
# Or full mode with governance audit
npx @cyclonedx/cdxgen@latest -r --include-formulation -o aibom.json --bom-audit --bom-audit-categories ai-bom

```

For HuggingFace models, `OWASP AIBOM Generator` extracts model card metadata. Evidence: `aibom.json` (includes hash of each weight file, dataset version, and provenance). For compliance, AI-BOM can be compared against `EU AI Act Annex IV` requirements (Chapter 11).

### L3 — Model Signing: Sigstore model-signing

Purpose: Cryptographic model signing to prove authenticity and prevent tampering. This project (`sigstore/model-transparency`, version 1.0 in 2025, in collaboration with OpenSSF/NVIDIA/HiddenLayer) is designed specifically for ML models and records signatures in the `Rekor` transparency log.

```bash
pip install model-signing
# Keyless signing with Sigstore (default)
model_signing sign ./models/model.safetensors --signature model.sig
# Verify before deployment
model_signing verify ./models/model.safetensors \
  --signature model.sig \
  --identity "ci@myorg.com" \
  --identity_provider "https://token.actions.githubusercontent.com"

```

Decision behavior: If `verify` fails, deployment must stop or be formally escalated. Evidence: `model.sig` + Rekor record (where used). **Confidentiality:** public transparency logs may not be acceptable for proprietary models—use private attestation storage or organization-controlled logs when required; see Chapter 5. `Cosign` can also be used for container and general artifact signing.

### L4 — Policy-as-Code: OPA / Conftest

Purpose: Convert security policies into executable code for lifecycle decision points such as control points 4 and 8.

Example policy (`Rego`) requiring signature and absence of critical vulnerabilities:

```rego
package mlsecops.gate

deny[msg] {
  input.modelscan.issues_count > 0
  msg := "Model contains unsafe artifact"
}

deny[msg] {
  not input.model.signed
  msg := "Model is not signed"
}

deny[msg] {
  input.trivy.critical_count > 0
  msg := "Dependency with critical vulnerability"
}

```

```bash
# Evaluate aggregated scan output against policy
conftest test evidence-bundle.json --policy ./policies/

```

Decision behavior: Any `deny` should block or escalate the release decision. Evidence: `OPA/Conftest` decision log.

### L6 — Runtime Guardrail: NeMo Guardrails

Purpose: Control LLM input/output at runtime (jailbreak detection, topic control, output moderation).

```bash
pip install nemoguardrails

```

```yaml
# config/rails.yaml
rails:
  input:
    flows:
      - check jailbreak
      - check sensitive data
  output:
    flows:
      - self check output
      - mask pii

```

Runtime behavior: This control runs in production, not in build; but its block/allow telemetry must go to `SIEM` (Chapter 10). Alternative tools: `Lakera Guard`, `Llama Guard`, internal gateway.

### L2 — MLOps Infrastructure and Agent Testing

Purpose: In addition to model and LLM, the `MLOps` infrastructure itself and agent logic must also be tested (Chapter 5).

```bash
# AI-exploits (Protect AI): known exploits against MLOps systems such as MLflow/Ray
git clone https://github.com/protectai/ai-exploits && cd ai-exploits
# AI-Infra-Guard (Tencent): discover security risks in AI infrastructure
# Agentic Security: red team for agents and tool misuse
pip install agentic_security

```

Behavior: These tests are typically run in staging and on a seasonal basis or before release, not every build. Critical findings must stop release.

### L2 — Model Privacy Audit

Purpose: Measure `Membership Inference` and `Model Inversion` risk before publishing a model trained on sensitive data (Chapter 4).

```bash
# PrivacyRaven (Trail of Bits): black-box privacy leakage test
pip install privacyraven
# ML Privacy Meter: quantitative leakage risk assessment
pip install ml-privacy-meter

```

Decision behavior: If membership inference success rate exceeds the threat model threshold, the model should be retrained with `DP-SGD`, hardened, or escalated for risk acceptance. Evidence: privacy risk report.

### Summary table: tool, command, and decision behavior

| Tool | Control point / area | Representative command | Decision criterion |
| --- | --- | --- | --- |
| `ModelScan` | 2 Load | `modelscan -p model.pkl -r json` | Unsafe artifact finding |
| `Gitleaks` | 3 Scan | `gitleaks detect --exit-code 1` | Any secret found |
| `Trivy` | 3 Scan | `trivy fs --exit-code 1 --severity CRITICAL` | Critical CVE |
| `lintML` / `NB Defense` | 3 Scan | `lintml ./src` / `nbdefense scan` | Unsafe pattern/secret |
| `ART` | 7 Test | Python script + assert ASR | `ASR > baseline+δ` |
| `Garak` | 7 Test | `garak --probes promptinject ...` | High bypass rate |
| `Promptfoo` | 7 Test | `promptfoo redteam run` | critical bypass > 0 |
| `Syft` | 2, 9 | `syft dir:. -o cyclonedx-json` | — (evidence generation) |
| `cdxgen aibom` | 2, 9 | `aibom .` | — (evidence generation; enforce completeness via `Conftest/OPA`) |
| `model-signing` | 9 Sign | `model_signing sign/verify` | Verify failure |
| `Conftest/OPA` | 4, 8 Decision | `conftest test evidence.json` | Any `deny` |
| `mcps-audit` | 3 Scan (MCP repos) | `mcps-audit scan ./mcp-server --json` | Critical MCP01/MCP03/MCP04/MCP05/MCP07 |
| `mcp-scan` (Snyk Agent Scan) | Workstation / SOC hygiene | `mcp-scan --json` | Shadow MCP / tool poisoning (not CI gate) |
| `MCP-Shield` | Workstation / SOC hygiene | per tool docs | Tool poisoning / exfil channel |
| `NeMo Guardrails` | Runtime | config rails | N/A (runtime; block metrics to SIEM) |

## OWASP ML Top 10 Mapping to MLOps Stages

This table is important for classic models and the `MLOps` lifecycle. Note that `OWASP ML Top 10` is still a draft and identifiers may change:

| `MLOps` Stage | Related Threats |
| --- | --- |
| `Planning and Design` | All threats, because weak design spreads risk across the entire lifecycle |
| `Data Engineering` | `ML02 Poisoning`, `ML06 Supply Chain`, `ML08 Skewing` |
| `Experimentation` | `ML06`, `ML07 Transfer Learning`, `ML10 Model Poisoning` |
| `Pipeline Dev & Test` | `ML02`, `ML06`, `ML10` |
| `CI / CD` | `ML06 Supply Chain` |
| `Continuous Training` | `ML02`, `ML06`, `ML08`, `ML10` |
| `Model Serving` | `ML01 Input Manipulation`, `ML03 Inversion`, `ML04 Membership`, `ML05 Theft`, `ML09 Output Integrity` |
| `Continuous Monitoring` | `ML01`, `ML02`, `ML08 Skewing`, `ML09` |

## Threat, Control, and Tool Reference Card

The consolidated and complete version of this card (with a `Phase` column and additional details) appears in **Appendix A of Chapter 15**. To avoid duplication, please refer to that appendix for the full table mapping threats to tools and lifecycle stages.

## MITRE ATLAS Mapping

| Threat | Technique | ID |
| --- | --- | --- |
| `Prompt Injection` | `LLM Prompt Injection` | `AML.T0051` |
| `Jailbreak` | `LLM Jailbreak` | `AML.T0054` |
| `Data Poisoning` | `Poison Training Data` | `AML.T0020` |
| `Model Extraction` | `Exfiltration via AI Inference API` | `AML.T0024` |
| `Adversarial Evasion` | `Evade AI Model` | `AML.T0015` |
| `Supply Chain` | `Publish Poisoned Models` | `AML.T0058` |
| `RAG Poisoning` | `RAG Poisoning` | `AML.T0070` |
| `Retrieval Content Crafting` | `Retrieval Content Crafting` | `AML.T0066` |
| `Memory Poisoning` | `AI Agent Context Poisoning` | `AML.T0080` |
| `Tool Abuse` | `AI Agent Tool Invocation` | `AML.T0053` |
| AI Reconnaissance | `Discover AI Agent Configuration` | `AML.T0084` |
| LLM data leakage | `LLM Data Leakage` | `AML.T0057` |
| Agent-tool exfiltration | `Exfiltration via AI Agent Tool Invocation` | `AML.T0086` |
| AI Worm Propagation *(emerging)* | Related: `AML.T0070`, `AML.T0080` (see Chapter 3 Morris II note) | — |
| Model Resource Abuse | `Cost Harvesting` | `AML.T0034` |

## Commercial Tool Market Map

In addition to open-source tools, the commercial `MLSecOps` ecosystem is growing. The purpose of this table is to introduce **categories** for build-vs-buy decisions, not to endorse or promote specific products; selection should be based on the "Tool Selection Criteria" in the next section:

| Category | Example Market Players | Use Case |
| --- | --- | --- |
| Comprehensive AI security platform | `HiddenLayer`; `Protect AI` (Palo Alto Networks / Prisma AIRS, 2025); `Robust Intelligence` (Cisco, 2024) | Model scan, threat detection, audit |
| Guardrail / Runtime LLM | `Lakera`, `Prompt Security`, `CalypsoAI`, `Lasso Security` | Prompt/output filtering in production |
| AI governance and compliance | `Credo AI`, `Cranium` | Governance, policy, and compliance documentation |
| Specialized red teaming | `Adversa`, `Mindgard` | Adversarial testing of models and agents |
| Privacy and synthetic data | `Private AI`, `Nightfall`, `Gretel`, `Tonic`, `Skyflow` | PII masking, DLP, and synthetic data |
| Secure federated learning | `Mithril Security`, `DynamoFL`, `Devron` | Distributed training with privacy preservation |

Note: Mentioning a product does not constitute a recommendation. Vendor ownership and product integration may have changed since publication; verify current status before procurement. For selection, first identify the threat and control, then evaluate open-source and commercial options against the criteria below.

## Tool Selection Criteria

A suitable tool should have several characteristics:

* Integrate with existing `CI/CD`.
* Provide structured output for the `Evidence Pack`.
* Be capable of producing a clear pass/fail/exception signal for release decisions.
* Be versionable and auditable.
* Align with organizational policies.
* Not require permanent manual exceptions.

## Emerging AI-native Threats

Modern MLSecOps must consider threats beyond traditional ML attacks. AI-native threats introduce autonomous behavior, where attackers can use AI systems to discover targets, generate attack strategies, move through connected environments, and abuse AI infrastructure.

Therefore, future MLSecOps programs must include:

* Agent behavior security
* Runtime autonomy control
* AI workload monitoring
* Propagation detection
* Adaptive red teaming

Security validation must evaluate not only whether a model is accurate or safe, but whether the complete AI system can resist autonomous attack behavior.

## Practical Principle

Tools should make security controls actionable, not replace security thinking. First identify the threat and control, then select the tool.
