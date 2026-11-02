# Policy-as-Code samples (OPA / Conftest)

Executable examples for controls described in Chapters 6, 8, 12, and 16.

| File | Purpose |
|------|---------|
| [`cp8_cp9_admission.rego`](cp8_cp9_admission.rego) | Deny release/deploy when CP8↔CP9 digest drifts, unreadable model binaries are flagged, MCP schema hashes change, agent kill-switch is missing, or unsafe cross-model KV reuse is enabled |
| [`testdata/`](testdata/evidence-pack.fail-digest.json) | Pass/fail Evidence Pack fixtures |

**Run locally**

```bash
# Install: https://www.conftest.dev/
conftest test --policy policies schemas/examples/evidence-pack.example.json
conftest test --policy policies policies/testdata/evidence-pack.fail-digest.json
```

Wire the same check into CI before promoting an artifact, and again at **Kubernetes admission** (Kyverno/Gatekeeper calling OPA, or Conftest in the deploy pipeline) so CP 9 is a **hard store/deploy gate**, not a post-hoc checklist.

These policies are **reference samples**. Tune thresholds and field names to your Evidence Pack producer.
