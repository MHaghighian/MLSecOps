#!/usr/bin/env python3
"""Example A — flow + mitigation + infra diagrams (style: loop / sandbox / layers).

Writes assets/diagrams/source/17-appendix-e-implementation-reference_{10,11,12}.svg
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "diagrams"
SRC_DIR = OUT_DIR / "source"

C = {
    "bg": "#F4F6F8",
    "panel": "#FFFFFF",
    "ink": "#0F172A",
    "muted": "#64748B",
    "line": "#94A3B8",
    "untrusted_bg": "#FFF1F2",
    "untrusted_bd": "#E11D48",
    "control_bg": "#ECFDF5",
    "control_bd": "#059669",
    "control_hd": "#065F46",
    "model_bg": "#FFFBEB",
    "model_bd": "#D97706",
    "model_hd": "#92400E",
    "action_bg": "#EFF6FF",
    "action_bd": "#2563EB",
    "hitl_bg": "#FEF3C7",
    "hitl_bd": "#D97706",
    "ok": "#047857",
    "danger": "#B91C1C",
    "accent": "#0F766E",
    "infra_bg": "#F1F5F9",
    "infra_bd": "#475569",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def defs(prefix: str = "") -> str:
    p = prefix
    return f"""
  <defs>
    <marker id="{p}arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['ink']}"/>
    </marker>
    <marker id="{p}arrG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['ok']}"/>
    </marker>
    <marker id="{p}arrR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['danger']}"/>
    </marker>
    <filter id="{p}soft" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
    <linearGradient id="{p}bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF2F7"/>
    </linearGradient>
  </defs>
"""


def title_bar(w: int, title: str, subtitle: str, badge: str, color: str) -> str:
    return f"""
  <rect width="{w}" height="72" fill="#0F172A"/>
  <text x="32" y="32" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="20" font-weight="700" fill="#F8FAFC">{esc(title)}</text>
  <text x="32" y="54" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="#94A3B8">{esc(subtitle)}</text>
  <rect x="{w - 168}" y="22" rx="14" width="136" height="28" fill="{color}"/>
  <text x="{w - 100}" y="41" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="#fff">{esc(badge)}</text>
"""


def box(x, y, w, h, fill, stroke, title, sub="", title_size=13, soft=True, prefix="") -> str:
    f = f' filter="url(#{prefix}soft)"' if soft else ""
    lines = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{f}/>',
        f'<text x="{x + w/2}" y="{y + (26 if not sub else 24)}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="{title_size}" font-weight="700" fill="{C["ink"]}">{esc(title)}</text>',
    ]
    if sub:
        lines.append(
            f'<text x="{x + w/2}" y="{y + 44}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">{esc(sub)}</text>'
        )
    return "\n  ".join(lines)


def pill(x, y, w, h, fill, stroke, text, ink=None) -> str:
    ink = ink or C["ink"]
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>
  <text x="{x + w/2}" y="{y + h/2 + 4}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{ink}">{esc(text)}</text>
"""


def diamond(cx, cy, s, fill, stroke, line1, line2="") -> str:
    # diamond with center cx,cy; half-diagonal s
    pts = f"{cx},{cy - s} {cx + s},{cy} {cx},{cy + s} {cx - s},{cy}"
    t = [
        f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>',
        f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C["ink"]}">{esc(line1)}</text>',
    ]
    if line2:
        t.append(
            f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">{esc(line2)}</text>'
        )
    return "\n  ".join(t)


def arrow(x1, y1, x2, y2, marker="arr", color=None, dashed=False, width=1.7, prefix="") -> str:
    color = color or C["ink"]
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#{prefix}{marker})"{dash}/>'


def label(x, y, text, color=None, size=11, anchor="middle", weight="600") -> str:
    color = color or C["muted"]
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>'


def mit_badge(x, y, text) -> str:
    return f"""
  <rect x="{x}" y="{y}" width="{8 + len(text) * 6.2}" height="20" rx="6" fill="{C['control_bg']}" stroke="{C['control_bd']}"/>
  <text x="{x + 8}" y="{y + 14}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" font-weight="700" fill="{C['control_hd']}">{esc(text)}</text>
"""


# ---------------------------------------------------------------------------
# 10 — Agent loop + memory + where mitigations sit
# ---------------------------------------------------------------------------

def svg_10() -> str:
    W, H = 1280, 980
    p = "a10"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(
            W,
            "Example A — Agent loop: flow + mitigations + memory",
            "Payload can enter at context assembly or tool_result. Actions die at the policy diamond. Memory is untrusted data, not policy.",
            "LOOP + GATES",
            C["accent"],
        ),
        # User goal
        pill(520, 100, 200, 36, C["panel"], C["ink"], "Developer goal", C["ink"]),
        arrow(620, 136, 620, 168, "arr", C["ink"], prefix=p),
        # Context assembled — with entry callouts
        box(390, 168, 460, 78, C["untrusted_bg"], C["untrusted_bd"], "Context assembled", "system · config · memory · history · RAG · open files", prefix=p),
        mit_badge(390, 252, "MIT: Retrieval ACL + Output Gate (data ≠ instructions)"),
        # Entry sources
        box(40, 160, 280, 100, C["panel"], C["untrusted_bd"], "ENTRY channels", "", 13, True, p),
        label(180, 200, "prompt · repo/RAG · web", C["danger"], 11),
        label(180, 218, "MCP/tool output · rules", C["danger"], 11),
        label(180, 236, "memory from prior session", C["danger"], 11),
        arrow(320, 210, 390, 210, "arrR", C["danger"], True, 1.6, p),
        label(350, 200, "payload in", C["danger"], 10),
        # Model decides
        arrow(620, 246, 620, 290, "arr", C["ink"], prefix=p),
        box(400, 290, 440, 64, C["model_bg"], C["model_bd"], "Model decides", "answer  ·  or emit tool proposal {name, args}", prefix=p),
        # Final output left
        arrow(400, 322, 220, 322, "arr", C["ink"], prefix=p),
        label(310, 310, "final output", C["muted"], 10),
        pill(60, 304, 160, 36, C["panel"], C["line"], "Return to developer"),
        # tool_use down
        arrow(620, 354, 620, 400, "arr", C["ink"], prefix=p),
        label(640, 380, "tool_use (proposal only)", C["model_hd"], 11, "start"),
        # Policy diamond
        diamond(620, 470, 72, C["control_bg"], C["control_bd"], "Intent Gate", "allow · HITL · deny"),
        mit_badge(710, 450, "MIT: capability profile + effect metadata"),
        mit_badge(710, 474, "MIT: param binding · write-path deny"),
        # deny branch (left)
        arrow(548, 470, 360, 470, "arr", C["danger"], prefix=p),
        pill(200, 452, 160, 36, C["untrusted_bg"], C["danger"], "Deny / stop", C["danger"]),
        # HITL branch (right) — only high-risk; not on the default path
        arrow(692, 470, 860, 470, "arr", C["hitl_bd"], prefix=p),
        box(860, 430, 280, 80, C["hitl_bg"], C["hitl_bd"], "HITL if high-risk", "deploy · protected push · new egress · secrets paths → human decides", prefix=p),
        arrow(1000, 510, 1000, 580, "arrG", C["ok"], prefix=p),
        label(1010, 550, "approved", C["ok"], 10, "start"),
        arrow(1000, 580, 840, 700, "arrG", C["ok"], prefix=p),
        # allow (low-risk) straight down — default path
        arrow(620, 542, 620, 670, "arrG", C["ok"], prefix=p),
        label(640, 600, "allow (in-policy)", C["ok"], 11, "start"),
        # Tool execute
        box(400, 670, 440, 70, C["action_bg"], C["action_bd"], "Tool / MCP executes", "brokered user token in header — never in model context", prefix=p),
        mit_badge(400, 748, "MIT: Credential Broker + MCP Gateway + downstream authZ"),
        # tool result loop
        arrow(840, 705, 980, 705, "arr", C["ink"], prefix=p),
        box(980, 640, 260, 70, C["untrusted_bg"], C["untrusted_bd"], "tool_result", "re-enters as DATA via Output Gate", prefix=p),
        arrow(1110, 640, 1110, 322, "arr", C["ink"], True, 1.6, p),
        arrow(1110, 322, 840, 322, "arr", C["ink"], True, 1.6, p),
        label(1125, 480, "bounded loop", C["model_hd"], 11, "start"),
        mit_badge(980, 720, "MIT: OG again + autonomy caps"),
        # Durable memory
        f'<ellipse cx="180" cy="700" rx="120" ry="55" fill="{C["infra_bg"]}" stroke="{C["infra_bd"]}" stroke-width="1.6"/>',
        label(180, 692, "Durable memory / rules", C["ink"], 12),
        label(180, 712, "UNTRUSTED store", C["danger"], 11),
        # write dashed
        f'<path d="M400,700 C320,700 280,700 300,700" fill="none" stroke="{C["control_bd"]}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#{p}arrG)"/>',
        label(340, 688, "write", C["ok"], 10),
        mit_badge(40, 770, "MIT: write-path deny for rules/mcp.json/hooks · no imperative-as-policy"),
        # read to context
        f'<path d="M180,645 C180,500 300,230 390,210" fill="none" stroke="{C["untrusted_bd"]}" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#{p}arrR)"/>',
        label(200, 520, "read next session", C["danger"], 10, "start"),
        label(200, 536, "(still untrusted data)", C["muted"], 10, "start"),
        # Footer axiom
        f'<rect x="32" y="860" width="1216" height="88" rx="12" fill="{C["panel"]}" stroke="{C["control_bd"]}" stroke-width="1.5"/>',
        label(52, 890, "Axiom", C["ok"], 13, "start", "800"),
        label(52, 912, "Memory / RAG / tool_result can be poisoned — treat as untrusted DATA. Never let them grant tools, set payee/path/account, or rewrite rules.", C["ink"], 12, "start"),
        label(52, 934, "Stop unauthorized ACTION at Intent Gate + param binding + brokered token + egress/write deny. Sanitize-on-write is supporting only.", C["muted"], 12, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 11 — Runtime / infra hardening (sandbox, network, approval)
# ---------------------------------------------------------------------------

def svg_11() -> str:
    W, H = 1280, 860
    p = "a11"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(
            W,
            "Example A — Runtime & infra mitigations",
            "Cloud/agent runtime isolation, workspace write limits, egress deny-by-default, then approval policy before consequential actions.",
            "INFRA",
            C["infra_bd"],
        ),
        # Cloud runtime box (left)
        f'<rect x="32" y="100" width="360" height="280" rx="14" fill="{C["infra_bg"]}" stroke="{C["infra_bd"]}" stroke-width="1.6" filter="url(#{p}soft)"/>',
        label(52, 128, "Cloud / agent runtime", C["ink"], 14, "start", "800"),
        box(52, 148, 320, 70, C["panel"], C["line"], "Setup phase", "network ON · secrets available for bootstrap", 12, False, p),
        arrow(212, 218, 212, 248, "arr", C["ink"], prefix=p),
        box(52, 248, 320, 90, C["control_bg"], C["control_bd"], "Agent phase (hardened)", "network OFF or allowlisted · secrets removed from env · brokered tokens only", 12, False, p),
        label(52, 360, "Stops: secret theft from env + open exfil", C["ok"], 11, "start"),
        # Main task flow
        box(460, 100, 280, 48, C["panel"], C["ink"], "Agent task starts", "", 13, True, p),
        arrow(600, 148, 600, 180, "arr", C["ink"], prefix=p),
        diamond(600, 240, 58, C["control_bg"], C["control_bd"], "Sandbox", "mode on"),
        # two parallel mitigations
        arrow(542, 240, 420, 240, "arrG", C["ok"], prefix=p),
        arrow(658, 240, 780, 240, "arrG", C["ok"], prefix=p),
        box(280, 300, 240, 70, C["control_bg"], C["control_bd"], "Writes → workspace only", "deny .env · hooks · mcp.json · rules · CI", 12, True, p),
        box(700, 300, 280, 70, C["control_bg"], C["control_bd"], "Network deny-by-default", "egress allowlist + kill switch (EA)", 12, True, p),
        # merge to approval
        arrow(400, 370, 400, 420, "arr", C["ink"], prefix=p),
        arrow(840, 370, 840, 420, "arr", C["ink"], prefix=p),
        arrow(400, 430, 600, 470, "arr", C["ink"], prefix=p),
        arrow(840, 430, 600, 470, "arr", C["ink"], prefix=p),
        diamond(600, 530, 70, C["hitl_bg"], C["hitl_bd"], "Approval", "policy"),
        # outcomes
        arrow(530, 530, 360, 530, "arr", C["hitl_bd"], prefix=p),
        box(160, 500, 200, 70, C["hitl_bg"], C["hitl_bd"], "Ask the human", "leave sandbox · new host · untrusted cmd · deploy", 12, True, p),
        arrow(670, 530, 860, 530, "arrG", C["ok"], prefix=p),
        box(860, 500, 200, 70, C["action_bg"], C["action_bd"], "Execute", "in-policy · profile-scoped · brokered token", 12, True, p),
        label(360, 490, "out of policy", C["hitl_bd"], 11),
        label(780, 490, "in policy", C["ok"], 11),
        # Bottom mapping to Example A controls
        f'<rect x="32" y="620" width="1216" height="200" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(52, 650, "Maps to Example A controls", C["ink"], 14, "start", "800"),
        label(52, 680, "Sandbox / workspace writes  →  Principle 11 write-path deny + capability profile (ask/edit/vcs/deploy)", C["ink"], 12, "start"),
        label(52, 708, "Network deny-by-default      →  EA egress allowlist + kill switch (Plane B/C)", C["ink"], 12, "start"),
        label(52, 736, "Approval policy              →  Intent Gate + HITL on high-risk effects (destructive / prod / protected branch / new egress)", C["ink"], 12, "start"),
        label(52, 764, "Secrets removed from env    →  Credential Broker (OBO token in Authorization header only)", C["ink"], 12, "start"),
        label(52, 792, "Closed IDE note: if you cannot insert the diamond inside the vendor loop, enforce the same rules at MCP proxy, API authZ, corporate egress, and MDM.", C["muted"], 12, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 12 — Layered architecture: surfaces + mitigations on edges
# ---------------------------------------------------------------------------

def svg_12() -> str:
    W, H = 1400, 980
    p = "a12"
    # layer colors
    app = "#DBEAFE"
    agent = "#E0E7FF"
    model = "#FEF3C7"
    infra = "#D1FAE5"
    data = "#FFE4E6"

    def layer(y, h, fill, label_text):
        return f"""
  <rect x="120" y="{y}" width="1000" height="{h}" rx="16" fill="{fill}" stroke="{C['line']}" stroke-width="1"/>
  <text x="40" y="{y + h/2 + 5}" text-anchor="middle" transform="rotate(-90 40 {y + h/2})" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="800" fill="{C['muted']}">{esc(label_text)}</text>
"""

    def node(x, y, w, h, title, sub, fill="#fff", stroke=None):
        stroke = stroke or C["line"]
        return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4" filter="url(#{p}soft)"/>
  <text x="{x + w/2}" y="{y + 22}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['ink']}">{esc(title)}</text>
  <text x="{x + w/2}" y="{y + 40}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" fill="{C['muted']}">{esc(sub)}</text>
"""

    def edge_mit(x, y, text):
        return f"""
  <rect x="{x}" y="{y}" width="{min(280, 16 + len(text)*5.8)}" height="22" rx="6" fill="{C['control_bg']}" stroke="{C['control_bd']}"/>
  <text x="{x + 8}" y="{y + 15}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" font-weight="700" fill="{C['control_hd']}">{esc(text)}</text>
"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(
            W,
            "Example A — Layers: attack surfaces and mitigations on the edges",
            "Same coding-assistant stack as your reference diagrams — but every risky crossing shows the deterministic control that stops unauthorized action.",
            "LAYERS",
            C["action_bd"],
        ),
        # layers
        layer(100, 100, app, "IDE / App"),
        layer(210, 280, agent, "Agent"),
        layer(500, 140, model, "Model"),
        layer(650, 140, infra, "Infra / Plane B"),
        layer(800, 120, data, "Data"),
        # IDE
        node(160, 120, 200, 60, "IDE host (1)", "chat · webview · MCP client", "#fff", "#6366F1"),
        node(400, 120, 200, 60, "AI Gateway (G)", "auth · rate · log · route", C["control_bg"], C["control_bd"]),
        node(640, 120, 200, 60, "Developer identity", "SSO / session claims", "#fff", C["line"]),
        edge_mit(400, 90, "Plane A → B: session authN"),
        # Agent internals
        node(160, 240, 180, 70, "Perception", "user prompt (trusted intent)", "#fff", C["action_bd"]),
        node(370, 240, 160, 70, "Tools (5)", "profile-scoped", "#fff", C["action_bd"]),
        node(550, 240, 160, 70, "RAG / index (4a)", "ACL pre-filter", C["untrusted_bg"], C["untrusted_bd"]),
        node(730, 240, 160, 70, "Memory (7)", "untrusted store", C["untrusted_bg"], C["untrusted_bd"]),
        node(910, 240, 180, 70, "Rendering", "sanitize + CSP + no remote", "#fff", C["action_bd"]),
        node(370, 350, 520, 70, "Orchestrator / Reasoning (3)", "plan-then-execute · owns dispatch · binds capability profile", C["model_bg"], C["model_bd"]),
        edge_mit(370, 320, "MIT before tools: Intent Gate + HITL"),
        edge_mit(550, 430, "MIT on retrieve: ACL → Output Gate"),
        edge_mit(730, 430, "MIT on memory: write deny · read as data"),
        # External
        node(1160, 250, 200, 80, "External / MCP (6)", "servers · APIs · git · deploy", C["untrusted_bg"], C["untrusted_bd"]),
        arrow(1090, 275, 1160, 275, "arrG", C["ok"], prefix=p),
        edge_mit(1160, 220, "MCP Gateway + schema pin"),
        arrow(1260, 330, 1260, 700, "arr", C["ink"], True, 1.4, p),
        # Model
        node(300, 530, 200, 70, "Input handling", "trusted intent + data channel", "#fff", C["model_bd"]),
        node(560, 530, 200, 70, "LLM brain (2)", "untrusted principal", C["model_bg"], C["model_bd"]),
        node(820, 530, 200, 70, "Output handling", "proposal or text only", "#fff", C["model_bd"]),
        edge_mit(300, 505, "No secrets in context"),
        # Infra plane B
        node(180, 680, 150, 70, "Intent Gate", "allow/deny/HITL", C["control_bg"], C["control_bd"]),
        node(360, 680, 150, 70, "Cred Broker", "OBO header token", C["control_bg"], C["control_bd"]),
        node(540, 680, 150, 70, "MCP Gateway", "allowlist · pin", C["control_bg"], C["control_bd"]),
        node(720, 680, 150, 70, "Egress (EA)", "deny-by-default", C["control_bg"], C["control_bd"]),
        node(900, 680, 150, 70, "SIEM / SOC", "every step logged", C["control_bg"], C["control_bd"]),
        # Data
        node(200, 830, 200, 60, "Codebase index", "vector / embeddings", C["untrusted_bg"], C["untrusted_bd"]),
        node(440, 830, 200, 60, "Secret store (9)", "never in model", C["control_bg"], C["control_bd"]),
        node(680, 830, 200, 60, "Rules / memory files", "write-path deny", C["untrusted_bg"], C["untrusted_bd"]),
        node(920, 830, 200, 60, "Downstream APIs", "Plane C authZ", C["action_bg"], C["action_bd"]),
        # Side legend
        f'<rect x="1160" y="360" width="200" height="280" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}"/>',
        label(1260, 390, "How to read", C["ok"], 13),
        label(1175, 420, "Red-tint boxes =", C["ink"], 11, "start"),
        label(1175, 438, "untrusted data / entry", C["muted"], 11, "start"),
        label(1175, 468, "Green badges =", C["ink"], 11, "start"),
        label(1175, 486, "deterministic mitigations", C["muted"], 11, "start"),
        label(1175, 516, "Model never executes.", C["ink"], 11, "start"),
        label(1175, 534, "Orchestrator + gates do.", C["muted"], 11, "start"),
        label(1175, 564, "Infinite prompts →", C["ink"], 11, "start"),
        label(1175, 582, "finite crossings.", C["muted"], 11, "start"),
        label(1175, 610, "Defend the edges.", C["ok"], 11, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def write_svg(name: str, content: str) -> Path:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    path = SRC_DIR / name
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path}")
    return path


def rasterize(svg_path: Path, png_path: Path) -> None:
    js = f"""
const {{ Resvg }} = require('@resvg/resvg-js');
const fs = require('fs');
const svg = fs.readFileSync({str(svg_path)!r});
const resvg = new Resvg(svg, {{ fitTo: {{ mode: 'width', value: 1600 }} }});
fs.writeFileSync({str(png_path)!r}, resvg.render().asPng());
console.log('png', {str(png_path)!r});
"""
    tmp = SRC_DIR / "_raster_tmp.js"
    tmp.write_text(js, encoding="utf-8")
    try:
        r = subprocess.run(["node", str(tmp)], capture_output=True, text=True, timeout=60)
        print(r.stdout or r.stderr)
    finally:
        tmp.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true")
    args = ap.parse_args()
    mapping = {
        "17-appendix-e-implementation-reference_10.svg": svg_10(),
        "17-appendix-e-implementation-reference_11.svg": svg_11(),
        "17-appendix-e-implementation-reference_12.svg": svg_12(),
    }
    for name, content in mapping.items():
        svg_path = write_svg(name, content)
        out_svg = OUT_DIR / name
        out_svg.write_text(content, encoding="utf-8")
        if args.png:
            # caller installs resvg; we try anyway
            pass


if __name__ == "__main__":
    main()
