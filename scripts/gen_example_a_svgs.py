#!/usr/bin/env python3
"""Generate hand-crafted SVG diagrams for Appendix E.7.1 Example A.

Keeps Mermaid sources untouched. Writes:
  assets/diagrams/source/17-appendix-e-implementation-reference_{07,08,09}.svg
Optionally rasterizes to PNG beside them if --png is passed and a converter exists.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "diagrams"
SRC_DIR = OUT_DIR / "source"

# Shared palette — security-doc aesthetic (slate + teal + rose), not purple-glow.
C = {
    "bg": "#F4F6F8",
    "panel": "#FFFFFF",
    "ink": "#0F172A",
    "muted": "#64748B",
    "line": "#94A3B8",
    "untrusted_bg": "#FFF1F2",
    "untrusted_bd": "#E11D48",
    "untrusted_hd": "#9F1239",
    "control_bg": "#ECFDF5",
    "control_bd": "#059669",
    "control_hd": "#065F46",
    "model_bg": "#FFFBEB",
    "model_bd": "#D97706",
    "model_hd": "#92400E",
    "action_bg": "#EFF6FF",
    "action_bd": "#2563EB",
    "action_hd": "#1E40AF",
    "attacker_bg": "#FEE2E2",
    "attacker_bd": "#991B1B",
    "danger": "#B91C1C",
    "ok": "#047857",
    "accent": "#0F766E",
    "plane_a": "#EEF2FF",
    "plane_b": "#D1FAE5",
    "plane_c": "#DBEAFE",
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def defs() -> str:
    # tip at path end (refX=10); userSpaceOnUse keeps heads sized consistently
    mk = (
        'markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="10" refY="5" '
        'markerWidth="9" markerHeight="9" orient="auto"'
    )
    return f"""
  <defs>
    <marker id="arr" {mk}>
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['ink']}"/>
    </marker>
    <marker id="arrR" {mk}>
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['danger']}"/>
    </marker>
    <marker id="arrG" {mk}>
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['ok']}"/>
    </marker>
    <marker id="arrB" {mk}>
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['action_bd']}"/>
    </marker>
    <filter id="soft" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF2F7"/>
    </linearGradient>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="0.8" fill="#CBD5E1" opacity="0.55"/>
    </pattern>
  </defs>
"""


def title_bar(w: int, title: str, subtitle: str, badge: str, badge_color: str) -> str:
    return f"""
  <rect width="{w}" height="78" fill="#0F172A"/>
  <text x="36" y="34" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="22" font-weight="700" fill="#F8FAFC">{esc(title)}</text>
  <text x="36" y="58" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" fill="#94A3B8">{esc(subtitle)}</text>
  <rect x="{w - 170}" y="24" rx="14" ry="14" width="134" height="30" fill="{badge_color}"/>
  <text x="{w - 103}" y="44" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">{esc(badge)}</text>
"""


def zone(x, y, w, h, label, fill, stroke, header) -> str:
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" ry="14" fill="{fill}" stroke="{stroke}" stroke-width="1.5" filter="url(#soft)"/>
  <rect x="{x}" y="{y}" width="{w}" height="28" rx="14" ry="14" fill="{header}"/>
  <rect x="{x}" y="{y + 14}" width="{w}" height="14" fill="{header}"/>
  <text x="{x + 14}" y="{y + 19}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" letter-spacing="0.04em">{esc(label.upper())}</text>
"""


def card(x, y, w, h, num, title, sub, fill, stroke, num_bg) -> str:
    lines = []
    lines.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" ry="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4" filter="url(#soft)"/>'
    )
    lines.append(
        f'<circle cx="{x + 18}" cy="{y + 18}" r="11" fill="{num_bg}"/>'
    )
    lines.append(
        f'<text x="{x + 18}" y="{y + 22}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF">{esc(num)}</text>'
    )
    lines.append(
        f'<text x="{x + 36}" y="{y + 22}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C["ink"]}">{esc(title)}</text>'
    )
    # wrap subtitle
    max_chars = max(18, int((w - 20) / 6.6))
    words = sub.split()
    rows, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                rows.append(cur)
            cur = word
    if cur:
        rows.append(cur)
    for i, row in enumerate(rows[:3]):
        lines.append(
            f'<text x="{x + 14}" y="{y + 42 + i * 15}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">{esc(row)}</text>'
        )
    return "\n  ".join(lines)


def gate(x, y, w, h, code, title, sub) -> str:
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" ry="10" fill="{C['control_bg']}" stroke="{C['control_bd']}" stroke-width="1.6" filter="url(#soft)"/>
  <rect x="{x}" y="{y}" width="34" height="{h}" rx="10" ry="10" fill="{C['control_bd']}"/>
  <rect x="{x + 16}" y="{y}" width="18" height="{h}" fill="{C['control_bd']}"/>
  <text x="{x + 17}" y="{y + h / 2 + 4}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="800" fill="#FFFFFF">{esc(code)}</text>
  <text x="{x + 44}" y="{y + 20}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['control_hd']}">{esc(title)}</text>
  <text x="{x + 44}" y="{y + 38}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" fill="{C['muted']}">{esc(sub)}</text>
"""


def arrow(x1, y1, x2, y2, color=None, marker="arr", dashed=False, width=1.6) -> str:
    color = color or C["ink"]
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"{dash}/>'


def curve(d: str, color=None, marker="arr", dashed=False, width=1.6) -> str:
    color = color or C["ink"]
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"{dash}/>'


def label(x, y, text, color=None, size=10, anchor="middle", weight="600") -> str:
    color = color or C["muted"]
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>'


def legend_item(x, y, fill, stroke, text) -> str:
    return f"""
  <rect x="{x}" y="{y}" width="16" height="12" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1"/>
  <text x="{x + 22}" y="{y + 10}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['ink']}">{esc(text)}</text>
"""


# ---------------------------------------------------------------------------
# Diagram 07 — Unsecured
# ---------------------------------------------------------------------------

def svg_07() -> str:
    W, H = 1480, 980
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(),
        f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.35"/>',
        title_bar(
            W,
            "Example A — Unsecured AI coding assistant",
            "Untrusted inputs flow straight into the model and tools. Secrets live in context. Open egress is the exfil path.",
            "UNSECURED",
            C["danger"],
        ),
        # Attacker
        f'<rect x="36" y="110" width="150" height="86" rx="12" fill="{C["attacker_bg"]}" stroke="{C["attacker_bd"]}" stroke-width="2" filter="url(#soft)"/>',
        f'<text x="111" y="145" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="14" font-weight="800" fill="{C["attacker_bd"]}">ATTACKER</text>',
        f'<text x="111" y="168" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">poison / rug-pull</text>',
        f'<text x="111" y="184" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">/ exfil sink</text>',
        # IDE
        card(220, 110, 240, 70, "1", "IDE host / client", "sees all tool defs at once", C["panel"], C["line"], C["ink"]),
        # Untrusted zone
        zone(220, 210, 520, 210, "Untrusted inputs — no validation", C["untrusted_bg"], C["untrusted_bd"], C["untrusted_hd"]),
        card(240, 255, 230, 68, "4a", "Codebase index", "vector DB / RAG — shared", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        card(490, 255, 230, 68, "4b", "Live context", "open files / web / docs", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        card(240, 335, 230, 68, "6", "MCP servers", "local + remote, unpinned", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        card(490, 335, 230, 68, "7", "Memory / rules", "persistent, writable", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        # Model zone
        zone(780, 210, 300, 210, "Model zone", C["model_bg"], C["model_bd"], C["model_hd"]),
        card(800, 255, 260, 68, "2", "LLM brain", "untrusted principal", C["panel"], C["model_bd"], C["model_bd"]),
        card(800, 335, 260, 68, "3", "Agent orchestrator", "thin passthrough — no gate", C["panel"], C["model_bd"], C["model_bd"]),
        # Action zone
        zone(220, 460, 860, 250, "Action zone — broad standing authority", C["action_bg"], C["action_bd"], C["action_hd"]),
        card(240, 510, 240, 72, "5", "Tools", "shell / file / git / deploy", C["panel"], C["action_bd"], C["action_bd"]),
        card(500, 510, 240, 72, "8", "Sub-agents", "inherit full privileges", C["panel"], C["action_bd"], C["action_bd"]),
        card(760, 510, 280, 72, "9", "Secrets in context", "API keys / tokens in prompt", C["attacker_bg"], C["danger"], C["danger"]),
        card(240, 600, 240, 72, "10", "Egress (open)", "any destination allowed", C["attacker_bg"], C["danger"], C["danger"]),
        card(500, 600, 240, 72, "11", "Cloud runtime", "shared / no tenant isolate", C["panel"], C["action_bd"], C["action_bd"]),
        # Normal flows — keep clear of zone headers and untrusted cards
        curve("M460,145 C620,120 760,200 800,255", C["ink"], "arr", False, 1.6),
        label(640, 138, "prompt", C["muted"], 10, "start"),
        arrow(720, 289, 800, 289),
        arrow(720, 369, 800, 369),
        arrow(930, 323, 930, 335),
        arrow(860, 403, 860, 460),
        label(880, 438, "dispatch tools", C["muted"], 10, "start"),
        arrow(480, 582, 480, 600),
        # Secrets into model — curve + labels in the gutter between Model/Action and callout
        curve("M900,510 C980,460 1040,380 1040,323", C["danger"], "arrR", True, 2),
        label(1088, 390, "secrets read", C["danger"], 10, "start"),
        label(1088, 404, "into context", C["danger"], 10, "start"),
        # Attack poison paths — labels in the left gutter, clear of curves
        curve("M186,153 C230,170 250,220 280,255", C["danger"], "arrR", True, 2.2),
        label(36, 228, "poison repo / web", C["danger"], 10, "start"),
        curve("M80,196 C80,300 160,350 240,369", C["danger"], "arrR", True, 2.2),
        label(36, 320, "tool poisoning", C["danger"], 10, "start"),
        # Exfil path — left gutter; approach attacker from below with clean tangent
        curve("M240,672 C80,720 70,400 111,196", C["danger"], "arrR", False, 2.8),
        label(36, 750, "EXFIL PATH — open egress → attacker", C["danger"], 12, "start"),
        # Callout — start after secrets gutter so labels are never painted under it
        f'<rect x="1160" y="210" width="280" height="500" rx="14" fill="{C["panel"]}" stroke="{C["danger"]}" stroke-width="1.5" filter="url(#soft)"/>',
        f'<text x="1176" y="242" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="800" fill="{C["danger"]}">What fails by construction</text>',
        *[
            f'<text x="1176" y="{268 + i * 34}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["ink"]}">{esc(t)}</text>'
            for i, t in enumerate(
                [
                    "• No retrieval ACL — any indexed",
                    "  chunk can reach any session",
                    "• No Output Gate — retrieved text",
                    "  treated as instructions",
                    "• No Intent Gate — model proposal",
                    "  = execution",
                    "• No MCP allowlist / schema pin",
                    "• Secrets travel inside the prompt",
                    "• Egress unrestricted → exfil",
                    "• Writes allowed to .env, mcp.json,",
                    "  hooks, CI, rules",
                    "• Sub-agents inherit full scope",
                ]
            )
        ],
        # Legend
        f'<rect x="36" y="900" width="1408" height="52" rx="10" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        legend_item(56, 920, C["untrusted_bg"], C["untrusted_bd"], "Untrusted data"),
        legend_item(220, 920, C["model_bg"], C["model_bd"], "Model zone"),
        legend_item(360, 920, C["action_bg"], C["action_bd"], "Action zone"),
        legend_item(500, 920, C["attacker_bg"], C["attacker_bd"], "Attacker / danger"),
        label(700, 930, "Dashed red = poison / secret leak   •   Solid red = exfil path", C["muted"], 11, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Diagram 08 — Secured
# ---------------------------------------------------------------------------

def svg_08() -> str:
    W, H = 1580, 1100
    controls = [
        ("G", "AI Gateway", "auth · rate · log · route — not an injection filter"),
        ("ACL", "Retrieval ACL", "identity pre-filter + ingest deny for secrets"),
        ("M", "MCP Gateway", "server allowlist · schema pin · rug-pull scan"),
        ("OG", "Output Gate", "untrusted text is DATA, never instructions"),
        ("IG", "Intent Gate", "capability profile · effect metadata · HITL"),
        ("CB", "Credential Broker", "short-lived OBO token in Authorization header"),
        ("EA", "Egress allowlist", "deny-by-default + kill switch"),
    ]
    ctrl_items = []
    for i, (code, title, sub) in enumerate(controls):
        cx = 56 + (i % 4) * 370
        cy = 880 + (i // 4) * 70
        ctrl_items.append(gate(cx, cy, 350, 52, code, title, sub))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(),
        f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.35"/>',
        title_bar(
            W,
            "Example A — Secure-by-design AI coding assistant",
            "Every untrusted→trusted crossing hits a deterministic control. Secrets stay out of the model. Capability profiles bound tools.",
            "SECURED",
            C["ok"],
        ),
        # Plane legend
        f'<rect x="36" y="100" width="210" height="40" rx="8" fill="{C["plane_a"]}" stroke="#6366F1"/>',
        label(141, 125, "Plane A — Product runtime", C["ink"], 11),
        f'<rect x="260" y="100" width="250" height="40" rx="8" fill="{C["plane_b"]}" stroke="{C["control_bd"]}"/>',
        label(385, 125, "Plane B — Your control plane", C["ink"], 11),
        f'<rect x="524" y="100" width="260" height="40" rx="8" fill="{C["plane_c"]}" stroke="{C["action_bd"]}"/>',
        label(654, 125, "Plane C — Downstream systems", C["ink"], 11),
        label(810, 125, "C mandatory · B binds agent to C · A optional", C["muted"], 12, "start"),
        # Top row
        card(36, 165, 220, 68, "1", "IDE host / client", "Plane A — vendor-owned loop", C["plane_a"], "#6366F1", "#6366F1"),
        gate(290, 169, 260, 60, "G", "AI Gateway", "authN · rate limit · log · route"),
        arrow(256, 199, 290, 199, C["ok"], "arrG"),
        # Untrusted
        zone(36, 260, 500, 200, "Untrusted inputs", C["untrusted_bg"], C["untrusted_bd"], C["untrusted_hd"]),
        card(52, 300, 220, 64, "4a", "Codebase index", "vector DB / RAG", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        card(290, 300, 220, 64, "4b", "Live context", "files / web / docs", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        card(52, 376, 220, 64, "6", "MCP servers", "local + remote", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        card(290, 376, 220, 64, "7", "Memory / rules", "persistent state", C["panel"], C["untrusted_bd"], C["untrusted_bd"]),
        # Control plane
        zone(560, 260, 500, 380, "Control plane — Plane B (deterministic)", C["control_bg"], C["control_bd"], C["control_hd"]),
        gate(580, 305, 220, 50, "ACL", "Retrieval ACL", "identity pre-filter"),
        gate(820, 305, 220, 50, "M", "MCP Gateway", "allowlist · schema pin"),
        gate(580, 370, 460, 50, "OG", "Output Gate", "untrusted text = DATA, not instructions"),
        gate(580, 435, 460, 50, "IG", "Intent Gate + HITL", "profile · effect metadata · high-risk HITL"),
        gate(580, 500, 220, 50, "CB", "Credential Broker", "OBO token · header only"),
        gate(820, 500, 220, 50, "EA", "Egress allowlist", "deny-by-default"),
        f'<text x="580" y="580" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["control_hd"]}">{esc("Write-path deny: .env · hooks · mcp.json · rules · CI workflows")}</text>',
        f'<text x="580" y="600" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">{esc("Profiles: ask → edit → vcs → deploy  ·  router fails narrow")}</text>',
        # Model
        zone(1090, 260, 450, 180, "Model zone — untrusted principal", C["model_bg"], C["model_bd"], C["model_hd"]),
        card(1110, 300, 410, 58, "2", "LLM brain", "emits plan only — cannot execute tools", C["panel"], C["model_bd"], C["model_bd"]),
        card(1110, 368, 410, 58, "3", "Agent orchestrator", "plan-then-execute · owns the loop", C["panel"], C["model_bd"], C["model_bd"]),
        # Action
        zone(1090, 470, 450, 170, "Action zone — least privilege (Plane C)", C["action_bg"], C["action_bd"], C["action_hd"]),
        card(1110, 510, 200, 54, "5", "Tools", "profile-scoped only", C["panel"], C["action_bd"], C["action_bd"]),
        card(1320, 510, 200, 54, "8", "Sub-agents", "no privilege inherit", C["panel"], C["action_bd"], C["action_bd"]),
        card(1110, 574, 200, 48, "10", "Egress", "via EA only", C["panel"], C["action_bd"], C["action_bd"]),
        card(1320, 574, 200, 48, "11", "Cloud runtime", "tenant-isolated", C["panel"], C["action_bd"], C["action_bd"]),
        # Secret store
        f'<ellipse cx="200" cy="560" rx="120" ry="50" fill="{C["control_bg"]}" stroke="{C["control_bd"]}" stroke-width="1.8" filter="url(#soft)"/>',
        f'<text x="200" y="548" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C["control_hd"]}">9. Secret store</text>',
        f'<text x="200" y="568" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">never enters model context</text>',
        # Arrows — never cross card interiors; labels sit in gutters
        arrow(272, 332, 580, 330, C["ok"], "arrG"),
        label(426, 252, "identity-scoped retrieve", C["ok"], 10),
        arrow(510, 332, 580, 395, C["ok"], "arrG"),
        label(518, 318, "live → OG", C["ok"], 10, "start"),
        # MCP path under the Untrusted zone (clear of Memory card + labels)
        curve("M162,440 C300,490 650,490 820,355", C["ok"], "arrG"),
        label(420, 508, "via MCP Gateway", C["ok"], 10, "start"),
        arrow(690, 355, 690, 370, C["ok"], "arrG"),
        arrow(930, 355, 810, 370, C["ok"], "arrG"),
        arrow(1040, 395, 1110, 329, C["ok"], "arrG"),
        label(1048, 360, "data channel", C["ok"], 10, "start"),
        curve("M550,199 C900,210 1050,260 1110,329", C["ok"], "arrG"),
        label(820, 188, "validated request", C["ok"], 10),
        arrow(1315, 358, 1315, 368, C["model_bd"], "arr"),
        curve("M1110,397 C1020,420 980,450 1040,460", C["ok"], "arrG"),
        label(980, 418, "proposal (tool+args)", C["ok"], 10),
        arrow(1040, 460, 1110, 537, C["ok"], "arrG"),
        label(1020, 500, "authorize → execute", C["ok"], 10, "start"),
        curve("M320,560 C450,560 520,550 580,550", C["ok"], "arrG", True),
        label(400, 578, "OBO token", C["ok"], 10),
        curve("M690,550 C820,580 1000,560 1110,537", C["ok"], "arrG", True),
        arrow(1040, 550, 1110, 598, C["ok"], "arrG"),
        # Principle strip
        f'<rect x="36" y="670" width="1504" height="70" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}" stroke-width="1.6"/>',
        f'<text x="56" y="698" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C["ok"]}">Primary enforcement chain</text>',
        f'<text x="56" y="720" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C["ink"]}">{esc("capability profile binds tools  →  Intent Gate authorizes by effect metadata  →  brokered user token + downstream authZ  →  egress allowlist. Soft guardrails are supporting only.")}</text>',
        # Bottom legend of gates
        f'<rect x="36" y="760" width="1504" height="300" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        f'<text x="56" y="792" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="14" font-weight="700" fill="{C["ink"]}">Control-plane nodes (Plane B)</text>',
        *ctrl_items,
        f'<text x="56" y="1035" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C["muted"]}">{esc("Closed IDE note: if the orchestrator is vendor-owned, enforce at MCP / API / network / endpoint / secret boundaries — see “Enforcement when the orchestrator is closed”.")}</text>',
        "</svg>",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Diagram 09 — Complete request data flow
# ---------------------------------------------------------------------------

def step_row(
    y: int,
    n: str,
    title: str,
    detail: str,
    left_label: str,
    right_label: str,
    kind: str = "normal",
) -> str:
    """One horizontal step in the flow timeline."""
    colors = {
        "normal": (C["panel"], C["line"], C["ink"]),
        "control": (C["control_bg"], C["control_bd"], C["control_hd"]),
        "model": (C["model_bg"], C["model_bd"], C["model_hd"]),
        "action": (C["action_bg"], C["action_bd"], C["action_hd"]),
        "hitl": ("#FEF3C7", "#D97706", "#92400E"),
        "deny": (C["attacker_bg"], C["danger"], C["danger"]),
    }
    fill, stroke, ink = colors[kind]
    return f"""
  <circle cx="70" cy="{y + 28}" r="16" fill="{stroke}"/>
  <text x="70" y="{y + 33}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="800" fill="#FFFFFF">{esc(n)}</text>
  <line x1="70" y1="{y + 44}" x2="70" y2="{y + 78}" stroke="{C['line']}" stroke-width="2"/>
  <rect x="106" y="{y}" width="980" height="56" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4" filter="url(#soft)"/>
  <text x="124" y="{y + 24}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="14" font-weight="700" fill="{ink}">{esc(title)}</text>
  <text x="124" y="{y + 44}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['muted']}">{esc(detail)}</text>
  <text x="1048" y="{y + 24}" text-anchor="end" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="600" fill="{C['muted']}">{esc(left_label)}</text>
  <text x="1048" y="{y + 44}" text-anchor="end" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{stroke}">{esc(right_label)}</text>
"""


def svg_09() -> str:
    W, H = 1480, 1520
    steps = [
        ("1", "Developer enters prompt in IDE", "User intent is the only trusted instruction channel for this request.", "1. IDE host", "Plane A", "normal"),
        ("2", "IDE → AI Gateway", "Authenticate session, apply rate limits, log request metadata, route to orchestrator. Not an injection filter.", "G. AI Gateway", "Plane B", "control"),
        ("3", "Gateway → Orchestrator", "Trusted code owns the loop. Capability profile is bound here and is immutable for the task.", "3. Orchestrator", "plan-then-execute", "model"),
        ("4", "Retrieve under identity pre-filter", "Codebase index / live context queried with the developer's entitlements (ACL). Over-scoped chunks never become candidates.", "4a + ACL", "Retrieval ACL", "control"),
        ("5", "Output Gate sanitizes context", "Retrieved chunks enter as a data channel. Untrusted text cannot become instructions or rewrite tool args.", "OG. Output Gate", "data ≠ instructions", "control"),
        ("6", "Orchestrator → LLM (trusted + data)", "Model receives user intent (trusted) + sanitized data. No secrets. No write tools unless profile allows.", "2. LLM brain", "untrusted principal", "model"),
        ("7", "LLM emits a proposal only", "Return shape: tool name + arguments. The model cannot execute. Proposal is not authority.", "plan = tool + args", "no side effects", "model"),
        ("8", "Intent Gate authorizes", "Check capability profile membership, tool-effect metadata, identity/role, target binding, write-path deny list.", "IG. Intent Gate", "allow / deny / HITL", "control"),
        ("9", "HITL for high-risk actions", "If effects include destructive / prod / protected branch / new external target: render deterministic facts → human approve/deny.", "Policy / HITL", "Dev decides", "hitl"),
        ("10", "Credential Broker issues token", "Short-lived delegated / OBO token for this tool call. Attached in Authorization header — never in args or model context.", "CB. Broker", "RFC 8693 style", "control"),
        ("11", "Execute via tools / MCP Gateway", "Only allowlisted MCP servers with pinned schemas. Tool runs under the user's scoped token; downstream API enforces authZ.", "5/6 + M", "Plane B → C", "action"),
        ("12", "Tool result → Output Gate again", "MCP/tool output is untrusted. Sanitize before it re-enters the loop as data.", "OG (return path)", "re-quarantine", "control"),
        ("13", "Bounded agentic loop", "Iterations / wall-clock / cost caps + loop detection. Profile still immutable. Repeat 6–12 until done or capped.", "autonomy cap", "LLM10 / ASI08", "model"),
        ("14", "Egress allowlist check", "Any outbound network from tools hits deny-by-default allowlist + kill switch. Blocks exfil even if a tool is tricked.", "EA. Egress", "Plane B/C", "control"),
        ("15", "Final response → Gateway → IDE", "Optional secret/DLP scan on exit. Developer sees the result. Every step above was logged to SOC/SIEM.", "G → 1 → Dev", "audit trail", "normal"),
    ]

    y0 = 110
    gap = 78
    body = []
    for i, step in enumerate(steps):
        body.append(step_row(y0 + i * gap, *step))
    # remove last connector line visually by overlaying white? simpler: shorten last step's line in step_row - instead add a cap
    last_y = y0 + (len(steps) - 1) * gap
    body.append(
        f'<circle cx="70" cy="{last_y + 28}" r="16" fill="{C["ok"]}" opacity="0"/>'  # noop; step already drew
    )
    # Cover the dangling line under last step
    body.append(
        f'<rect x="62" y="{last_y + 44}" width="16" height="40" fill="url(#bgGrad)"/>'
    )

    # Side panel
    side = f"""
  <rect x="1120" y="110" width="320" height="520" rx="14" fill="{C['panel']}" stroke="{C['ok']}" stroke-width="1.6" filter="url(#soft)"/>
  <text x="1140" y="142" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="14" font-weight="800" fill="{C['ok']}">Mental model</text>
  <text x="1140" y="168" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['ink']}">{esc("The LLM does not trigger tools.")}</text>
  <text x="1140" y="186" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['ink']}">{esc("It emits a request for one.")}</text>
  <text x="1140" y="214" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['muted']}">{esc("Only the orchestrator (trusted")}</text>
  <text x="1140" y="232" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['muted']}">{esc("code) can execute — after IG.")}</text>

  <text x="1140" y="270" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C['ink']}">Two valid shapes</text>
  <text x="1140" y="294" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['control_hd']}">Flow A — pipeline</text>
  <text x="1140" y="312" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("Read-only tasks: code retrieves,")}</text>
  <text x="1140" y="328" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("model is text-in/text-out, no tools.")}</text>
  <text x="1140" y="356" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['action_hd']}">Flow B — agentic loop</text>
  <text x="1140" y="374" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("This diagram. Profile bound at")}</text>
  <text x="1140" y="390" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("start; re-checked every iteration.")}</text>

  <text x="1140" y="426" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C['ink']}">SOC / SIEM</text>
  <text x="1140" y="448" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("Every numbered step emits an")}</text>
  <text x="1140" y="464" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("audit event: who / what / when /")}</text>
  <text x="1140" y="480" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("tool / decision / token id.")}</text>

  <text x="1140" y="516" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C['danger']}">Honest residual</text>
  <text x="1140" y="538" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("Poisoned item can still corrupt")}</text>
  <text x="1140" y="554" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("its own summary (LLM09). AuthZ-")}</text>
  <text x="1140" y="570" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("but-harmful within user rights remains.")}</text>

  <rect x="1120" y="660" width="320" height="200" rx="14" fill="{C['control_bg']}" stroke="{C['control_bd']}" stroke-width="1.4"/>
  <text x="1140" y="692" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C['control_hd']}">Capability profile (immutable)</text>
  <text x="1140" y="718" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['ink']}">{esc("ask  →  read_file, search_code")}</text>
  <text x="1140" y="740" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['ink']}">{esc("edit → + edit_file (deny list)")}</text>
  <text x="1140" y="762" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['ink']}">{esc("vcs  → + git_commit, open_pr")}</text>
  <text x="1140" y="784" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="{C['ink']}">{esc("deploy → + deploy (role + HITL)")}</text>
  <text x="1140" y="812" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("Router fails to the narrower profile.")}</text>

  <rect x="1120" y="890" width="320" height="160" rx="14" fill="{C['model_bg']}" stroke="{C['model_bd']}" stroke-width="1.4"/>
  <text x="1140" y="922" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="13" font-weight="700" fill="{C['model_hd']}">Loop annotation (step 13)</text>
  <text x="1140" y="948" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['ink']}">{esc("while steps < cap AND not done:")}</text>
  <text x="1140" y="968" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("  LLM propose → IG → CB → tool")}</text>
  <text x="1140" y="988" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("  → OG → LLM")}</text>
  <text x="1140" y="1012" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" fill="{C['muted']}">{esc("Hard stop: iterations / time / cost")}</text>
"""

    # Loop brace visual on steps 6-12
    loop_y1 = y0 + 5 * gap
    loop_y2 = y0 + 11 * gap + 56
    loop = f"""
  <path d="M48,{loop_y1} C20,{loop_y1} 20,{loop_y2} 48,{loop_y2}" fill="none" stroke="{C['model_bd']}" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="18" y="{(loop_y1 + loop_y2) / 2}" transform="rotate(-90 18 {(loop_y1 + loop_y2) / 2})" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="{C['model_hd']}">BOUNDED LOOP</text>
"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(),
        f'<rect width="{W}" height="{H}" fill="url(#bgGrad)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.3"/>',
        title_bar(
            W,
            "Example A — Secure request data flow (end-to-end)",
            "From developer prompt through retrieval, proposal, authorization, brokered execution, bounded loop, egress, and audit.",
            "DATA FLOW",
            C["accent"],
        ),
        loop,
        *body,
        side,
        # Footer legend
        f'<rect x="36" y="{H - 70}" width="1060" height="44" rx="10" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        legend_item(56, H - 56, C["control_bg"], C["control_bd"], "Control"),
        legend_item(160, H - 56, C["model_bg"], C["model_bd"], "Model / loop"),
        legend_item(290, H - 56, C["action_bg"], C["action_bd"], "Action"),
        legend_item(400, H - 56, "#FEF3C7", "#D97706", "HITL"),
        legend_item(500, H - 56, C["panel"], C["line"], "IDE / response"),
        label(640, H - 46, "Green nodes = deterministic enforcement   ·   Amber = human decision", C["muted"], 11, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def write_svg(name: str, content: str) -> Path:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    path = SRC_DIR / name
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path}")
    return path


def try_png(svg_path: Path, png_path: Path) -> bool:
    """Best-effort SVG→PNG via npx resvg-cli or playwright."""
    import shutil
    import subprocess

    # Try resvg via npx
    try:
        cmd = [
            "npx",
            "--yes",
            "@resvg/resvg-js-cli",
            str(svg_path),
            str(png_path),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode == 0 and png_path.exists():
            print(f"wrote {png_path} (resvg)")
            return True
        print("resvg failed:", r.stderr[:400] if r.stderr else r.stdout[:400])
    except Exception as e:
        print("resvg error:", e)

    # Try sharp-cli style alternative: use playwright screenshot of SVG data URL
    try:
        js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const fs = require('fs');
  const path = require('path');
  const svg = fs.readFileSync({str(svg_path)!r}, 'utf8');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const m = svg.match(/viewBox="0 0 (\\d+) (\\d+)"/);
  const w = m ? Number(m[1]) : 1400;
  const h = m ? Number(m[2]) : 1000;
  await page.setViewportSize({{ width: w, height: h }});
  await page.setContent(`<!DOCTYPE html><html><body style="margin:0">${{svg}}</body></html>`, {{ waitUntil: 'load' }});
  await page.screenshot({{ path: {str(png_path)!r}, fullPage: true, type: 'png' }});
  await browser.close();
  console.log('ok');
}})();
"""
        tmp = SRC_DIR / "_render_svg_tmp.js"
        tmp.write_text(js, encoding="utf-8")
        r = subprocess.run(["node", str(tmp)], capture_output=True, text=True, timeout=180)
        tmp.unlink(missing_ok=True)
        if r.returncode == 0 and png_path.exists():
            print(f"wrote {png_path} (playwright)")
            return True
        print("playwright failed:", r.stderr[:500] if r.stderr else r.stdout[:500])
    except Exception as e:
        print("playwright error:", e)

    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true", help="Also rasterize to PNG in assets/diagrams/")
    args = ap.parse_args()

    # Fix: remove broken svg_08 from call path
    mapping = {
        "17-appendix-e-implementation-reference_07.svg": svg_07(),
        "17-appendix-e-implementation-reference_08.svg": svg_08(),
        "17-appendix-e-implementation-reference_09.svg": svg_09(),
    }
    for name, content in mapping.items():
        svg_path = write_svg(name, content)
        if args.png:
            png_path = OUT_DIR / name.replace(".svg", ".png")
            try_png(svg_path, png_path)


if __name__ == "__main__":
    main()
