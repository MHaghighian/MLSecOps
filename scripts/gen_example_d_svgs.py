#!/usr/bin/env python3
"""Example D — website RAG + background agents diagrams (_19 unsecured, _20 secured, _21 flows)."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "diagrams"
SRC_DIR = OUT_DIR / "source"

C = {
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
    "danger": "#B91C1C",
    "ok": "#047857",
    "accent": "#0F766E",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def defs(p: str) -> str:
    mk = (
        'markerUnits="userSpaceOnUse" viewBox="0 0 10 10" refX="10" refY="5" '
        'markerWidth="9" markerHeight="9" orient="auto"'
    )
    return f"""
  <defs>
    <marker id="{p}arr" {mk}>
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['ink']}"/>
    </marker>
    <marker id="{p}arrG" {mk}>
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{C['ok']}"/>
    </marker>
    <marker id="{p}arrR" {mk}>
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


def title_bar(w, title, subtitle, badge, color) -> str:
    return f"""
  <rect width="{w}" height="72" fill="#0F172A"/>
  <text x="32" y="32" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="20" font-weight="700" fill="#F8FAFC">{esc(title)}</text>
  <text x="32" y="54" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="#94A3B8">{esc(subtitle)}</text>
  <rect x="{w - 168}" y="22" rx="14" width="136" height="28" fill="{color}"/>
  <text x="{w - 100}" y="41" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="#fff">{esc(badge)}</text>
"""


def card(x, y, w, h, num, title, sub, fill, stroke, num_bg, p="") -> str:
    soft = f' filter="url(#{p}soft)"' if p else ""
    badge = ""
    title_x = x + 12
    if num:
        badge = f"""
  <circle cx="{x + 16}" cy="{y + 16}" r="10" fill="{num_bg}"/>
  <text x="{x + 16}" y="{y + 20}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" font-weight="700" fill="#fff">{esc(num)}</text>"""
        title_x = x + 32
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{soft}/>{badge}
  <text x="{title_x}" y="{y + 20}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['ink']}">{esc(title)}</text>
  <text x="{x + 12}" y="{y + 40}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" fill="{C['muted']}">{esc(sub)}</text>
"""


def gate(x, y, w, h, code, title, sub, p="") -> str:
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{C['control_bg']}" stroke="{C['control_bd']}" stroke-width="1.5" filter="url(#{p}soft)"/>
  <rect x="{x}" y="{y}" width="32" height="{h}" rx="10" fill="{C['control_bd']}"/>
  <rect x="{x + 14}" y="{y}" width="18" height="{h}" fill="{C['control_bd']}"/>
  <text x="{x + 16}" y="{y + h/2 + 4}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" font-weight="800" fill="#fff">{esc(code)}</text>
  <text x="{x + 42}" y="{y + 18}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="{C['control_hd']}">{esc(title)}</text>
  <text x="{x + 42}" y="{y + 34}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" fill="{C['muted']}">{esc(sub)}</text>
"""


def label(x, y, text, color=None, size=11, anchor="middle", weight="600") -> str:
    color = color or C["muted"]
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>'


def arrow(x1, y1, x2, y2, marker="arr", color=None, dashed=False, p="") -> str:
    color = color or C["ink"]
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="1.6" marker-end="url(#{p}{marker})"{dash}/>'


def js_path(p: Path) -> str:
    return str(p).replace("\\", "/")


def try_png(svg_path: Path, png_path: Path) -> bool:
    import shutil

    npx = shutil.which("npx.cmd") or shutil.which("npx")
    try:
        if not npx:
            raise FileNotFoundError("npx not on PATH")
        cmd = [npx, "--yes", "@resvg/resvg-js-cli", str(svg_path), str(png_path)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode == 0 and png_path.exists():
            print(f"wrote {png_path} (resvg-cli)")
            return True
        print("resvg-cli failed:", (r.stderr or r.stdout)[:400])
    except Exception as e:
        print("resvg-cli error:", e)

    js = f"""
const {{ Resvg }} = require('@resvg/resvg-js');
const fs = require('fs');
const svg = fs.readFileSync({js_path(svg_path)!r});
const resvg = new Resvg(svg, {{ fitTo: {{ mode: 'width', value: 1600 }} }});
fs.writeFileSync({js_path(png_path)!r}, resvg.render().asPng());
console.log('ok');
"""
    tmp = SRC_DIR / "_raster_d_tmp.js"
    try:
        tmp.write_text(js, encoding="utf-8")
        r = subprocess.run(["node", str(tmp)], capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and png_path.exists():
            print(f"wrote {png_path} (resvg-js)")
            return True
        print("resvg-js failed:", (r.stderr or r.stdout)[:400])
    except Exception as e:
        print("resvg-js error:", e)
    finally:
        tmp.unlink(missing_ok=True)
    return False


def svg_19() -> str:
    W, H = 1480, 960
    p = "d19"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example D — Unsecured support website",
                  "One tool-bound loop for anonymous and logged-in users; mixed KB+accounts soup; CRM-admin worker.",
                  "UNSECURED", C["danger"]),
        card(40, 100, 200, 56, "1", "Chat widget", "public page", C["panel"], C["line"], C["ink"], p),
        card(270, 100, 200, 56, "2", "Thin API", "no CSRF / quota", C["panel"], C["line"], C["ink"], p),
        card(500, 100, 220, 56, "3", "Session ignored", "anonymous = admin tools", C["untrusted_bg"], C["danger"], C["danger"], p),
        arrow(240, 128, 270, 128, p=p),
        arrow(470, 128, 500, 128, p=p),
        f'<rect x="40" y="180" width="700" height="220" rx="14" fill="{C["untrusted_bg"]}" stroke="{C["untrusted_bd"]}" stroke-width="1.5" filter="url(#{p}soft)"/>',
        label(56, 208, "ONE LOOP — TOOLS IN CHAT", C["untrusted_hd"], 13, "start", "800"),
        card(56, 225, 210, 60, "4", "Orchestrator", "retrieve + dispatch", C["panel"], C["untrusted_bd"], C["untrusted_bd"], p),
        card(286, 225, 210, 60, "5", "LLM", "calls CRM tools", C["panel"], C["model_bd"], C["model_bd"], p),
        card(516, 225, 200, 60, "8", "No confirm", "model acts", C["panel"], C["danger"], C["danger"], p),
        card(56, 310, 320, 60, "6", "KB + accounts soup", "no labels / no RLS", C["panel"], C["danger"], C["danger"], p),
        card(396, 310, 320, 60, "7", "Any customer's order", "filter from chat text", C["panel"], C["danger"], C["danger"], p),
        f'<rect x="770" y="180" width="340" height="220" rx="14" fill="{C["action_bg"]}" stroke="{C["danger"]}" filter="url(#{p}soft)"/>',
        label(790, 208, "WORKER = GOD ACCOUNT", C["danger"], 12, "start", "800"),
        card(790, 230, 300, 56, "10", "Background worker", "tools always on", C["panel"], C["danger"], C["danger"], p),
        card(790, 305, 300, 70, "12", "CRM_TOKEN=admin", "NHI is the deputy", C["untrusted_bg"], C["danger"], C["danger"], p),
        f'<rect x="1140" y="180" width="300" height="220" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}" stroke-width="1.5"/>',
        label(1290, 210, "What fails", C["danger"], 14, weight="800"),
        label(1160, 240, "• Tools bound in public chat", C["ink"], 12, "start"),
        label(1160, 265, "• Anonymous account RAG", C["ink"], 12, "start"),
        label(1160, 290, "• Mixed KB + all orders", C["ink"], 12, "start"),
        label(1160, 315, "• Queue text = policy", C["ink"], 12, "start"),
        label(1160, 340, "• CRM-admin worker", C["ink"], 12, "start"),
        label(1160, 365, "• No CSRF on /act", C["ink"], 12, "start"),
        card(40, 430, 340, 70, "9", "Job queue", "chat transcript trusted as instructions", C["untrusted_bg"], C["danger"], C["danger"], p),
        card(400, 430, 340, 70, "11", "CRM / orders / pay", "accepts god token", C["untrusted_bg"], C["danger"], C["danger"], p),
        card(760, 430, 350, 70, "13", "Render open", "remote img/link (EchoLeak path)", C["untrusted_bg"], C["danger"], C["danger"], p),
        f'<path d="M716,255 H790" fill="none" stroke="{C["danger"]}" stroke-width="2" marker-end="url(#{p}arrR)"/>',
        label(753, 236, "chat → CRM", C["danger"], 10),
        f'<rect x="40" y="530" width="1400" height="90" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(60, 565, "Naive mental model: \"the website chatbot is just RAG, and a helper agent files tickets.\"", C["ink"], 13, "start"),
        label(60, 595, "Reality: one tool-bound loop plus a CRM-admin NHI is Example A's confused deputy on a public origin.", C["muted"], 12, "start"),
        f'<rect x="40" y="650" width="1400" height="240" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}"/>',
        label(60, 685, "Red paths on this diagram", C["danger"], 14, "start", "800"),
        label(60, 720, "• Anonymous visitor: \"look up order 12345\" retrieves another customer's record", C["ink"], 12, "start"),
        label(60, 750, "• Poisoned KB: \"refund to attacker@evil.com\" dispatches from the chat loop", C["ink"], 12, "start"),
        label(60, 780, "• Injected chat: \"create a ticket for every customer\" runs as CRM admin", C["ink"], 12, "start"),
        label(60, 810, "• Markdown image in the widget phones home with the answer (EchoLeak-class)", C["ink"], 12, "start"),
        label(60, 850, "Components 1–13 match the Example D table.", C["muted"], 11, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def svg_20() -> str:
    W, H = 1580, 1020
    p = "d20"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example D — Secure support website",
                  "Chat is a no-tool pipeline. Actions enqueue after confirm. Worker uses OBO, not a CRM-admin NHI.",
                  "SECURED", C["ok"]),
        f'<rect x="36" y="95" width="180" height="36" rx="8" fill="#EEF2FF" stroke="#6366F1"/>',
        label(126, 118, "Plane A — UI", C["ink"], 11),
        f'<rect x="230" y="95" width="240" height="36" rx="8" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(350, 118, "Plane B — split runtimes", C["ink"], 11),
        f'<rect x="484" y="95" width="240" height="36" rx="8" fill="{C["action_bg"]}" stroke="{C["action_bd"]}"/>',
        label(604, 118, "Plane C — IdP / CRM", C["ink"], 11),
        label(750, 118, "Compose A + B; inference is managed API or Example C", C["muted"], 12, "start"),
        card(36, 150, 180, 56, "1", "Widget", "CSP · no authz fields", "#EEF2FF", "#6366F1", "#6366F1", p),
        gate(240, 152, 220, 52, "G", "AI Gateway", "session · CSRF · quota", p),
        card(490, 150, 210, 56, "3", "Identity", "anonymous | authenticated", C["action_bg"], C["action_bd"], C["action_bd"], p),
        arrow(216, 178, 240, 178, "arrG", C["ok"], p=p),
        arrow(460, 178, 490, 178, "arrG", C["ok"], p=p),
        f'<rect x="36" y="230" width="500" height="320" rx="14" fill="{C["control_bg"]}" stroke="{C["control_bd"]}" stroke-width="1.4" filter="url(#{p}soft)"/>',
        label(56, 258, "PATH 1 — CHAT (no tools)", C["control_hd"], 13, "start", "800"),
        card(56, 275, 460, 50, "4", "Chat orchestrator", "Ex. A Flow A — empty tools", C["panel"], C["control_bd"], C["control_bd"], p),
        gate(56, 340, 460, 48, "KB", "KB labels", "anonymous → public only", p),
        gate(56, 400, 460, 48, "RLS", "Account pre-filter", "authenticated · Example B", p),
        gate(56, 460, 220, 56, "OG", "Output Gate", "chunks = DATA", p),
        card(290, 460, 226, 56, "5", "LLM", "answer only", C["model_bg"], C["model_bd"], C["model_bd"], p),
        f'<rect x="556" y="230" width="500" height="320" rx="14" fill="{C["control_bg"]}" stroke="{C["control_bd"]}" stroke-width="1.4" filter="url(#{p}soft)"/>',
        label(576, 258, "PATH 2 — ACTION (queued)", C["control_hd"], 13, "start", "800"),
        gate(576, 275, 460, 48, "CF", "Confirm / HITL", "orchestrator-rendered facts", p),
        card(576, 340, 220, 56, "9", "Queue", "transcript = untrusted", C["panel"], C["control_bd"], C["control_bd"], p),
        card(816, 340, 220, 56, "12", "OBO broker", "RFC 8693 user token", C["panel"], C["control_bd"], C["control_bd"], p),
        gate(576, 410, 460, 48, "IG", "Intent Gate", "Example A on the worker", p),
        card(576, 475, 460, 50, "10", "Worker NHI", "queue + logs only — not CRM admin", C["panel"], C["control_bd"], C["control_bd"], p),
        f'<rect x="1076" y="230" width="468" height="180" rx="14" fill="{C["action_bg"]}" stroke="{C["action_bd"]}" filter="url(#{p}soft)"/>',
        label(1096, 258, "SYSTEMS OF RECORD", C["action_bd"], 12, "start", "800"),
        card(1096, 275, 428, 56, "11", "CRM / orders / pay", "token authZ — user's rights only", C["panel"], C["action_bd"], C["action_bd"], p),
        card(1096, 345, 428, 48, "6+7", "Two corpora", "KB labels  ∪  account RLS", C["panel"], C["action_bd"], C["action_bd"], p),
        f'<rect x="1076" y="430" width="468" height="120" rx="14" fill="{C["model_bg"]}" stroke="{C["model_bd"]}" filter="url(#{p}soft)"/>',
        label(1096, 460, "Inference", C["model_hd"], 12, "start", "800"),
        label(1096, 488, "Managed API (E.1.2) or Example C.", C["ink"], 12, "start"),
        label(1096, 512, "D does not re-teach KV / GPU isolation.", C["muted"], 11, "start"),
        f'<rect x="36" y="575" width="1508" height="100" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}" stroke-width="1.5"/>',
        label(56, 605, "Primary enforcement chain", C["ok"], 14, "start", "800"),
        label(56, 633, "session → (chat: labeled KB ± account RLS → Output Gate → no tools)  |  (act: confirm → bound args → OBO worker → CRM authZ)", C["ink"], 13, "start"),
        label(56, 657, "The public chat process has no tool registry. A CRM-admin NHI is never the worker's identity.", C["muted"], 12, "start"),
        f'<rect x="36" y="695" width="740" height="260" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(56, 725, "Split runtimes", C["ink"], 14, "start", "800"),
        label(56, 760, "Chat = Example A Flow A (pipeline), as on B's chat path", C["ink"], 12, "start"),
        label(56, 790, "Action = Example A Flow B, queued + OBO", C["ink"], 12, "start"),
        label(56, 820, "Anonymous is a capability class, not UX", C["ink"], 12, "start"),
        label(56, 860, "Anti-pattern: tools bound in the public widget loop", C["danger"], 12, "start"),
        label(56, 890, "Anti-pattern: CRM_TOKEN=admin on the worker", C["danger"], 12, "start"),
        f'<rect x="800" y="695" width="744" height="260" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(820, 725, "Control map", C["ink"], 14, "start", "800"),
        gate(820, 750, 340, 48, "KB", "KB labels", "public vs internal", p),
        gate(1180, 750, 340, 48, "RLS", "Account RLS", "from session claims", p),
        gate(820, 820, 340, 48, "IG", "Intent Gate", "worker only", p),
        gate(1180, 820, 340, 48, "OBO", "Broker", "user token, not NHI", p),
        label(820, 905, "Render: CSP lockdown (Example B principle 7).", C["muted"], 12, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def svg_21() -> str:
    W, H = 1480, 1120
    p = "d21"

    def step(y, n, title, detail, kind="control"):
        colors = {
            "control": (C["control_bg"], C["control_bd"]),
            "model": (C["model_bg"], C["model_bd"]),
            "data": (C["untrusted_bg"], C["untrusted_bd"]),
            "action": (C["action_bg"], C["action_bd"]),
        }
        fill, stroke = colors[kind]
        return f"""
  <circle cx="60" cy="{y + 24}" r="14" fill="{stroke}"/>
  <text x="60" y="{y + 28}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="800" fill="#fff">{esc(n)}</text>
  <rect x="90" y="{y}" width="620" height="48" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>
  <text x="106" y="{y + 20}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['ink']}">{esc(title)}</text>
  <text x="106" y="{y + 38}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" fill="{C['muted']}">{esc(detail)}</text>
"""

    def step_r(y, n, title, detail, kind="control"):
        colors = {
            "control": (C["control_bg"], C["control_bd"]),
            "model": (C["model_bg"], C["model_bd"]),
            "data": (C["untrusted_bg"], C["untrusted_bd"]),
            "action": (C["action_bg"], C["action_bd"]),
        }
        fill, stroke = colors[kind]
        return f"""
  <circle cx="790" cy="{y + 24}" r="14" fill="{stroke}"/>
  <text x="790" y="{y + 28}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="800" fill="#fff">{esc(n)}</text>
  <rect x="820" y="{y}" width="600" height="48" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>
  <text x="836" y="{y + 20}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['ink']}">{esc(title)}</text>
  <text x="836" y="{y + 38}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" fill="{C['muted']}">{esc(detail)}</text>
"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example D — Chat + enqueue data flows",
                  "Left: answer path (no tools). Right: action path (confirm → OBO worker). Queue transcript is data, never policy.",
                  "DATA FLOW", C["accent"]),
        f'<rect x="36" y="95" width="700" height="40" rx="8" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(386, 120, "PATH 1 — CHAT (no tools)", C["control_hd"], 13),
        step(150, "C1", "Verify session", "anonymous | authenticated — discard body identity", "control"),
        step(210, "C2", "Retrieve", "anon: public KB · auth: KB labels ∪ account RLS", "control"),
        step(270, "C3", "Output Gate", "hits enter as DATA, not instructions", "control"),
        step(330, "C4", "LLM complete", "tools=[] — Example A Flow A (as on B chat)", "model"),
        step(390, "C5", "CSP-hardened render", "no remote img/connect · encode markdown", "action"),
        f'<rect x="760" y="95" width="680" height="40" rx="8" fill="{C["action_bg"]}" stroke="{C["action_bd"]}"/>',
        label(1100, 120, "PATH 2 — ENQUEUE + WORKER", C["action_bd"], 13),
        step_r(150, "A1", "Require auth + CSRF", "step-up if anonymous · bind session", "control"),
        step_r(210, "A2", "Confirm facts", "order_id / amount from CRM records, not the model", "control"),
        step_r(270, "A3", "Enqueue", "bound args + untrusted transcript + obo_subject", "data"),
        step_r(330, "A4", "Broker + Intent Gate", "RFC 8693 user token · Example A gates", "control"),
        step_r(390, "A5", "Dispatch to CRM", "downstream token authZ — worker NHI cannot", "action"),
        f'<rect x="36" y="470" width="700" height="210" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}"/>',
        label(56, 500, "Split runtimes", C["ok"], 14, "start", "800"),
        label(56, 530, "The public chat process has no tool registry.", C["ink"], 12, "start"),
        label(56, 555, "Anonymous cannot retrieve accounts or enqueue.", C["ink"], 12, "start"),
        label(56, 580, "Worker NHI: queue + logs. CRM: user OBO token.", C["ink"], 12, "start"),
        label(56, 620, "Inference: managed API or Example C — not re-taught here.", C["muted"], 12, "start"),
        f'<rect x="760" y="470" width="680" height="210" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}"/>',
        label(780, 500, "Attacks stopped on this diagram", C["danger"], 14, "start", "800"),
        label(780, 535, "• Anonymous \"look up my order\" hits account RAG", C["ink"], 12, "start"),
        label(780, 560, "• Poisoned KB dispatches refund from chat", C["ink"], 12, "start"),
        label(780, 585, "• Mass-create tickets as CRM admin", C["ink"], 12, "start"),
        label(780, 610, "• CSRF enqueue from a third-party origin", C["ink"], 12, "start"),
        label(780, 635, "• Recipient taken from model / article text", C["ink"], 12, "start"),
        f'<rect x="36" y="710" width="1404" height="100" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(56, 745, "Honest residual", C["ink"], 13, "start", "800"),
        label(56, 770, "A user can still get a wrong summary of a public KB article they may read (LLM09).", C["muted"], 12, "start"),
        label(56, 795, "A user who confirms a harmful action within their own rights is reduced by binding + HITL, not eliminated. KV → Example C.", C["muted"], 12, "start"),
        f'<rect x="36" y="840" width="1404" height="230" rx="12" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(56, 870, "Pseudo-code (split)", C["control_hd"], 13, "start", "800"),
        label(56, 900, "if anonymous: hits = kb_search(q, label=\"public\")     # no account, no tools", C["ink"], 12, "start"),
        label(56, 925, "else: hits = kb(labels) + account_search(prefilter=claims)", C["ink"], 12, "start"),
        label(56, 950, "answer = llm.complete(user=q, data=output_gate(hits), tools=[])", C["ink"], 12, "start"),
        label(56, 985, "job = enqueue(bound_args, obo_subject=user)   # worker: broker.exchange + intent_gate", C["ink"], 12, "start"),
        label(56, 1020, "CRM_TOKEN=admin on the worker is a fail.", C["muted"], 12, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", action="store_true", help="Also rasterize to PNG in assets/diagrams/")
    args = ap.parse_args()
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, fn in [
        ("17-appendix-e-implementation-reference_19.svg", svg_19),
        ("17-appendix-e-implementation-reference_20.svg", svg_20),
        ("17-appendix-e-implementation-reference_21.svg", svg_21),
    ]:
        content = fn()
        src = SRC_DIR / name
        out = OUT_DIR / name
        src.write_text(content, encoding="utf-8")
        out.write_text(content, encoding="utf-8")
        print("wrote", name)
        if args.png:
            try_png(src, OUT_DIR / name.replace(".svg", ".png"))


if __name__ == "__main__":
    main()
