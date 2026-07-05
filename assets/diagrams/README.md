# Diagram assets (PNG)

Static diagram exports used in the guide (GitHub, Word, PDF, MkDocs).

| Chapter file | PNG files | Mermaid source |
|---|---|---|
| `01-intro.md` | `01-intro_01.png`, `01-intro_02.png` | `source/01-intro_01.mmd`, … |
| `06-pipeline.md` | `06-pipeline_01.png`, `06-pipeline_02.png` | `source/06-pipeline_01.mmd`, … |
| `07-llm-rag-security.md` | `07-llm-rag-security_01.png` … `_03.png` | `source/07-llm-rag-security_*.mmd` |
| `08-agentic-ai-security.md` | `08-agentic-ai-security_01.png` … `_06.png` | `source/08-agentic-ai-security_*.mmd` |
| `09-anti-patterns.md` | `09-anti-patterns_01.png` | `source/09-anti-patterns_01.mmd` |
| `10-monitoring-soc-ir.md` | `10-monitoring-soc-ir_01.png`, `_02.png` | `source/10-monitoring-soc-ir_*.mmd` |
| `11-governance-evidence.md` | `11-governance-evidence_01.png`, `_02.png` | `source/11-governance-evidence_*.mmd` |
| `12-threat-control-tools-map.md` | `12-threat-control-tools-map_01.png` | `source/12-threat-control-tools-map_01.mmd` |
| `16-kubernetes-deployment-reference.md` | `16-kubernetes-deployment-reference_01.png` | `source/16-kubernetes-deployment-reference_01.mmd` |
| `17-appendix-e-implementation-reference.md` | `17-appendix-e-implementation-reference_01.png` … `_06.png` | `source/17-appendix-e-implementation-reference_*.mmd` |

**Regenerate PNGs:** edit `source/*.mmd`, then run `scripts/mermaid_to_png.py` from the local build workspace (parent folder).

**Why not ` ```mermaid ` in markdown?** GitHub's Mermaid renderer often fails on long `flowchart LR` chains and special characters, showing a spinner then *Unable to render rich display* even when the PNG below would display correctly.
