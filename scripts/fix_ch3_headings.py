path_file = r"c:\Users\m.haghighian\Desktop\MLSecOps\github\chapters-en\03-threat-landscape.md"
with open(path_file, encoding="utf-8") as f:
    text = f.read()

marker = "# Chapter 3: Autonomous AI Threats and Offensive AI Operations\n"
if marker not in text:
    raise SystemExit("chapter marker not found")
title, body = text.split(marker, 1)

body = body.replace('<div dir="ltr">\n\n', '', 1)
body = body.replace('\n</div>\n', '\n', 1)

scope = (
    '<div dir="ltr">\n\n'
    "> **Scope note:** Sections marked *emerging* describe research-stage or plausible future "
    "capabilities (e.g., autonomous malware at scale, AI worms such as Morris II). Sections "
    "marked *demonstrated / active patterns* reflect threats with published incidents or active "
    "exploitation patterns (e.g., tool abuse, memory poisoning, compute hijacking). Threat models "
    "should prioritize demonstrated risks first.\n\n"
)

body = body.replace("####", "@@@@")
body = body.replace("###", "$$$$")
body = body.replace("##", "####")
body = body.replace("$$$$", "###")
body = body.replace("@@@@", "####")

lines = []
for line in body.splitlines():
    if line.startswith("# ") and not line.startswith("##"):
        line = "#" + line
    lines.append(line)
body = "\n".join(lines)

emerging = [
    "Autonomous AI Malware",
    "Autonomous Exploit Generation",
    "AI Worms and Autonomous Propagation",
    "AI-assisted Persistence",
    "AI-assisted Defensive Evasion",
]
for s in emerging:
    body = body.replace(f"## {s}", f"## {s} *(emerging)*")

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
    body = body.replace(f"## {s}", f"## {s} *(demonstrated / active patterns)*")

text = marker + scope + body.rstrip() + "\n\n</div>\n"
with open(path_file, "w", encoding="utf-8") as f:
    f.write(text)
print("Ch3 headings fixed")
