import re

path = r"c:\Users\m.haghighian\Desktop\MLSecOps\github\chapters-en\03-threat-landscape.md"
with open(path, encoding="utf-8") as f:
    text = f.read()

scope = (
    '<div dir="ltr">\n\n'
    "> **Scope note:** Sections marked *emerging* describe research-stage or plausible future "
    "capabilities (e.g., autonomous malware at scale, AI worms such as Morris II). Sections "
    "marked *demonstrated / active patterns* reflect threats with published incidents or active "
    "exploitation patterns (e.g., tool abuse, memory poisoning, compute hijacking). Threat models "
    "should prioritize demonstrated risks first.\n\n"
)

if '<div dir="ltr">' not in text:
    text = text.replace(
        "# Chapter 3: Autonomous AI Threats and Offensive AI Operations\n\n## Overview\n",
        "# Chapter 3: Autonomous AI Threats and Offensive AI Operations\n\n" + scope + "## Overview\n",
    )

lines = text.splitlines()
out = []
chapter_done = False
for line in lines:
    if line.startswith("# ") and not line.startswith("# Chapter 3"):
        if chapter_done:
            line = "#" + line
        else:
            chapter_done = True
    elif line.startswith("## ") and chapter_done:
        line = "#" + line
    elif line.startswith("### ") and chapter_done:
        line = "#" + line
    out.append(line)

text = "\n".join(out)
if not text.rstrip().endswith("</div>"):
    text = text.rstrip() + "\n\n</div>\n"

old_fw = """Particular mappings include:

* LLM01 Prompt Injection
* LLM03 Supply Chain
* LLM06 Excessive Agency
* LLM08 Vector Weaknesses
* MITRE ATLAS Reconnaissance
* MITRE ATLAS Persistence
* MITRE ATLAS Lateral Movement
* MITRE ATLAS Exfiltration"""

new_fw = """Particular mappings include (technique-level examples, not full coverage):

* `LLM01` Prompt Injection → `AML.T0051` LLM Prompt Injection
* `LLM03` Supply Chain → `AML.T0058` Publish Poisoned Models
* `LLM06` Excessive Agency → `AML.T0053` AI Agent Tool Invocation
* `LLM08` Vector and Embedding Weaknesses → `AML.T0070` RAG Poisoning
* AI reconnaissance → `AML.T0067` Discover AI Agent Configuration
* Agent memory/context attacks → `AML.T0080` AI Agent Context Poisoning
* Model extraction → `AML.T0024` Exfiltration via AI Inference API
* Resource abuse → `AML.T0034` Cost Harvesting"""

text = text.replace(old_fw, new_fw)

emerging = [
    "Autonomous AI Malware",
    "Autonomous Exploit Generation",
    "AI Worms and Autonomous Propagation",
    "AI-assisted Persistence",
    "AI-assisted Defensive Evasion",
]
for s in emerging:
    text = text.replace(f"## {s}", f"## {s} *(emerging)*")

demonstrated = [
    "Agent Tool Abuse",
    "Memory Poisoning",
    "AI Compute Hijacking",
    "Autonomous Data Exfiltration",
    "AI-driven Reconnaissance",
    "AI-driven Lateral Movement",
    "Runtime Behavioral Threats",
]
for s in demonstrated:
    text = text.replace(f"## {s}", f"## {s} *(demonstrated / active patterns)*")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
print("Ch3 updated")
