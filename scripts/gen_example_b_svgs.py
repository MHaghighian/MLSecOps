#!/usr/bin/env python3
"""Example B — multi-tenant RAG SaaS diagrams (_13 unsecured, _14 secured, _15 flows)."""

from __future__ import annotations

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


def title_bar(w, title, subtitle, badge, color) -> str:
    return f"""
  <rect width="{w}" height="72" fill="#0F172A"/>
  <text x="32" y="32" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="20" font-weight="700" fill="#F8FAFC">{esc(title)}</text>
  <text x="32" y="54" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" fill="#94A3B8">{esc(subtitle)}</text>
  <rect x="{w - 168}" y="22" rx="14" width="136" height="28" fill="{color}"/>
  <text x="{w - 100}" y="41" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="#fff">{esc(badge)}</text>
"""


def zone(x, y, w, h, label, fill, stroke, header) -> str:
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.5" filter="url(#soft)"/>
  <rect x="{x}" y="{y}" width="{w}" height="26" rx="14" fill="{header}"/>
  <rect x="{x}" y="{y + 12}" width="{w}" height="14" fill="{header}"/>
  <text x="{x + 12}" y="{y + 18}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="#fff">{esc(label.upper())}</text>
"""


def card(x, y, w, h, num, title, sub, fill, stroke, num_bg, p="") -> str:
    soft = f' filter="url(#{p}soft)"' if p else ""
    # fix: use p in filter id
    soft = f' filter="url(#{p}soft)"' if p else ' filter="url(#soft)"'
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{soft}/>
  <circle cx="{x + 16}" cy="{y + 16}" r="10" fill="{num_bg}"/>
  <text x="{x + 16}" y="{y + 20}" text-anchor="middle" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="10" font-weight="700" fill="#fff">{esc(num)}</text>
  <text x="{x + 32}" y="{y + 20}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="12" font-weight="700" fill="{C['ink']}">{esc(title)}</text>
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


def svg_13() -> str:
    W, H = 1480, 920
    p = "b13"
    # Fix zone filter - use p
    def z(x, y, w, h, lab, fill, stroke, header):
        return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="1.5" filter="url(#{p}soft)"/>
  <rect x="{x}" y="{y}" width="{w}" height="26" rx="14" fill="{header}"/>
  <rect x="{x}" y="{y + 12}" width="{w}" height="14" fill="{header}"/>
  <text x="{x + 12}" y="{y + 18}" font-family="Segoe UI, Helvetica Neue, Arial, sans-serif" font-size="11" font-weight="700" fill="#fff">{esc(lab.upper())}</text>
"""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example B — Unsecured multi-tenant RAG chatbot",
                  "Shared index, client-supplied filters, chunks as instructions, open render egress → cross-user / cross-tenant leak.",
                  "UNSECURED", C["danger"]),
        card(40, 100, 200, 56, "1", "Client", "upload + chat UI", C["panel"], C["line"], C["ink"], p),
        card(280, 100, 200, 56, "2", "API (thin)", "weak auth / no quota", C["panel"], C["line"], C["ink"], p),
        arrow(240, 128, 280, 128, p=p),
        z(40, 190, 700, 200, "Untrusted corpus — shared soup", C["untrusted_bg"], C["untrusted_bd"], C["untrusted_hd"]),
        card(60, 230, 200, 60, "6", "Ingest (open)", "any file → index", C["panel"], C["untrusted_bd"], C["untrusted_bd"], p),
        card(280, 230, 200, 60, "7", "Object store", "loose IAM", C["panel"], C["untrusted_bd"], C["untrusted_bd"], p),
        card(500, 230, 220, 60, "8", "Vector index", "ONE shared index", C["attacker"] if False else C["panel"], C["untrusted_bd"], C["untrusted_bd"], p),
        card(60, 310, 320, 56, "9", "ACL metadata", "client can set owner/tenant", C["panel"], C["danger"], C["danger"], p),
        card(400, 310, 320, 56, "", "filter from request.json", "attacker sets tenant/user", C["untrusted_bg"], C["danger"], C["danger"], p),
        z(780, 190, 320, 200, "Model zone", C["model_bg"], C["model_bd"], C["model_hd"]),
        card(800, 230, 280, 56, "5", "LLM", "treats chunks as policy", C["panel"], C["model_bd"], C["model_bd"], p),
        card(800, 310, 280, 56, "4", "Orchestrator", "passthrough, no gate", C["panel"], C["model_bd"], C["model_bd"], p),
        z(780, 420, 320, 140, "Render", C["action_bg"], C["action_bd"], "#1E40AF"),
        card(800, 460, 280, 70, "11", "Chat render", "remote img/link allowed", C["untrusted_bg"], C["danger"], C["danger"], p),
        # attacker
        f'<rect x="1140" y="190" width="280" height="370" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}" stroke-width="1.5"/>',
        label(1280, 220, "What fails", C["danger"], 14, weight="800"),
        label(1160, 250, "• No tenant partition", C["ink"], 12, "start"),
        label(1160, 275, "• Filter from client body", C["ink"], 12, "start"),
        label(1160, 300, "• No per-user RLS pre-filter", C["ink"], 12, "start"),
        label(1160, 325, "• Ingest without scan/hash", C["ink"], 12, "start"),
        label(1160, 350, "• Chunks = instructions", C["ink"], 12, "start"),
        label(1160, 375, "• Open CSP → EchoLeak path", C["ink"], 12, "start"),
        label(1160, 400, "• Same-tenant ⇒ readable", C["ink"], 12, "start"),
        label(1160, 440, "RED PATHS", C["danger"], 12, "start", "800"),
        label(1160, 465, "Alice query → Bob's docs", C["danger"], 12, "start"),
        label(1160, 490, "Tenant A → Tenant B index", C["danger"], 12, "start"),
        label(1160, 515, "Markdown img → evil.com", C["danger"], 12, "start"),
        # red flows
        f'<path d="M720,260 C760,260 780,260 800,258" fill="none" stroke="{C["danger"]}" stroke-width="2" marker-end="url(#{p}arrR)"/>',
        label(740, 248, "poisoned chunks", C["danger"], 10),
        f'<path d="M940,530 C940,600 600,620 400,340" fill="none" stroke="{C["danger"]}" stroke-width="2.2" marker-end="url(#{p}arrR)"/>',
        label(700, 600, "EXFIL / cross-user retrieve", C["danger"], 12),
        f'<rect x="40" y="640" width="1060" height="80" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(60, 675, "Naive mental model: \"the chatbot searches everything and the model is careful.\"", C["ink"], 13, "start"),
        label(60, 700, "Reality: the model will answer from whatever unauthorized chunks you put in the prompt.", C["muted"], 12, "start"),
        label(60, 850, "Components 1–11 match the Example B table.", C["muted"], 11, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def svg_14() -> str:
    W, H = 1580, 980
    p = "b14"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example B — Secure multi-tenant RAG chatbot",
                  "Tenant partition + server-built RLS pre-filter + gated ingest + data-channel chunks + CSP lockdown.",
                  "SECURED", C["ok"]),
        # planes
        f'<rect x="36" y="95" width="180" height="36" rx="8" fill="#EEF2FF" stroke="#6366F1"/>',
        label(126, 118, "Plane A — UI", C["ink"], 11),
        f'<rect x="230" y="95" width="220" height="36" rx="8" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(340, 118, "Plane B — control plane", C["ink"], 11),
        f'<rect x="464" y="95" width="220" height="36" rx="8" fill="{C["action_bg"]}" stroke="{C["action_bd"]}"/>',
        label(574, 118, "Plane C — IdP / data plane", C["ink"], 11),
        label(710, 118, "Both: cross-tenant partition AND intra-tenant RLS", C["muted"], 12, "start"),
        # top row
        card(36, 150, 180, 56, "1", "Client", "no authz fields trusted", "#EEF2FF", "#6366F1", "#6366F1", p),
        gate(240, 152, 220, 52, "G", "AI Gateway", "authN · quota · audit", p),
        card(490, 150, 200, 56, "3", "Identity", "tenant + user claims", C["action_bg"], C["action_bd"], C["action_bd"], p),
        arrow(216, 178, 240, 178, "arrG", C["ok"], p=p),
        arrow(460, 178, 490, 178, "arrG", C["ok"], p=p),
        # ingest column
        f'<rect x="36" y="230" width="460" height="320" rx="14" fill="{C["control_bg"]}" stroke="{C["control_bd"]}" stroke-width="1.4" filter="url(#{p}soft)"/>',
        label(56, 258, "INGEST PATH (write)", C["control_hd"], 13, "start", "800"),
        gate(56, 275, 400, 48, "IN", "Ingest gates", "type · size · AV · hash · PII policy", p),
        card(56, 340, 190, 56, "7", "Object store", "prefix per tenant", C["panel"], C["control_bd"], C["control_bd"], p),
        card(270, 340, 190, 56, "6", "Chunk + embed", "server-stamped meta", C["panel"], C["control_bd"], C["control_bd"], p),
        card(56, 420, 400, 70, "9", "ACL store (server-only writes)", "owner + shares · private by default", C["panel"], C["control_bd"], C["control_bd"], p),
        label(56, 520, "Metadata stamped from JWT — never from upload form", C["ok"], 11, "start"),
        # retrieval column
        f'<rect x="520" y="230" width="520" height="320" rx="14" fill="{C["control_bg"]}" stroke="{C["control_bd"]}" stroke-width="1.4" filter="url(#{p}soft)"/>',
        label(540, 258, "RETRIEVE PATH (read)", C["control_hd"], 13, "start", "800"),
        gate(540, 275, 460, 48, "RLS", "Pre-filter from claims", "tenant partition ∩ (owner ∪ shares)", p),
        card(540, 340, 220, 56, "8", "Vector index", "namespace per tenant", C["panel"], C["control_bd"], C["control_bd"], p),
        gate(780, 340, 220, 56, "OG", "Output Gate", "chunks = DATA channel", p),
        card(540, 420, 460, 70, "4", "Orchestrator", "build_prefilter(claims) only — discards body tenant/user", C["panel"], C["control_bd"], C["control_bd"], p),
        label(540, 520, "Hard partition + RLS — both required", C["ok"], 11, "start"),
        # model + render
        f'<rect x="1060" y="230" width="480" height="200" rx="14" fill="{C["model_bg"]}" stroke="{C["model_bd"]}" filter="url(#{p}soft)"/>',
        label(1080, 258, "MODEL (untrusted principal)", C["model_hd"], 12, "start", "800"),
        card(1080, 280, 440, 56, "5", "LLM", "answer only — no filter authority", C["panel"], C["model_bd"], C["model_bd"], p),
        card(1080, 350, 440, 56, "", "Prefer no tools", "pipeline chat (Example A Flow A)", C["panel"], C["model_bd"], C["model_bd"], p),
        f'<rect x="1060" y="450" width="480" height="100" rx="14" fill="{C["action_bg"]}" stroke="{C["action_bd"]}" filter="url(#{p}soft)"/>',
        card(1080, 470, 440, 60, "11", "Render surface", "CSP lockdown · no remote img/connect", C["control_bg"], C["control_bd"], C["control_bd"], p),
        # arrows
        arrow(266, 400, 520, 300, "arrG", C["ok"], p=p),
        arrow(1000, 460, 1060, 308, "arrG", C["ok"], p=p),
        arrow(1300, 430, 1300, 450, "arrG", C["ok"], p=p),
        # bottom axiom
        f'<rect x="36" y="580" width="1504" height="100" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}" stroke-width="1.5"/>',
        label(56, 610, "Primary enforcement chain", C["ok"], 14, "start", "800"),
        label(56, 638, "verified claims → tenant partition → RLS pre-filter → Output Gate → answer (no tools) → CSP render", C["ink"], 13, "start"),
        label(56, 662, "Managed model APIs do not enforce your RAG ACL. If Bob's chunk is in the prompt, the model may answer from it.", C["muted"], 12, "start"),
        # isolation callout
        f'<rect x="36" y="700" width="740" height="220" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(56, 730, "Two isolation layers", C["ink"], 14, "start", "800"),
        label(56, 760, "Cross-tenant: separate index/namespace per customer", C["ink"], 12, "start"),
        label(56, 785, "Intra-tenant RLS: Alice must not see Bob's private docs", C["ink"], 12, "start"),
        label(56, 810, "Sharing = explicit ACL rows (not \"same tenant\")", C["ink"], 12, "start"),
        label(56, 845, "Anti-pattern: filter = request.json[\"acl\"]", C["danger"], 12, "start"),
        label(56, 875, "Anti-pattern: post-filter after global top-k only", C["danger"], 12, "start"),
        f'<rect x="800" y="700" width="740" height="220" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(820, 730, "Control map", C["ink"], 14, "start", "800"),
        gate(820, 750, 340, 48, "IN", "Ingest", "allowlist · AV · hash", p),
        gate(1180, 750, 340, 48, "RLS", "Pre-filter", "from JWT + share DB", p),
        gate(820, 820, 340, 48, "OG", "Output Gate", "data ≠ instructions", p),
        gate(1180, 820, 340, 48, "CSP", "Render", "no live egress", p),
        "</svg>",
    ]
    return "\n".join(parts)


def svg_15() -> str:
    W, H = 1480, 1100
    p = "b15"

    def step(y, n, title, detail, kind="control"):
        colors = {
            "control": (C["control_bg"], C["control_bd"]),
            "model": (C["model_bg"], C["model_bd"]),
            "data": (C["untrusted_bg"], C["untrusted_bd"]),
            "ui": (C["panel"], C["line"]),
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

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example B — Ingest + chat data flows",
                  "Left: upload path (write). Right: chat path (read). Both stamp and filter from verified identity — never from the client body.",
                  "DATA FLOW", C["accent"]),
        # Left column ingest
        f'<rect x="36" y="95" width="700" height="40" rx="8" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(386, 120, "PATH 1 — INGEST (write)", C["control_hd"], 13),
        step(150, "I1", "Authenticate upload", "JWT → tenant_id + user_id", "control"),
        step(210, "I2", "Ingest gates", "type allowlist · size · AV · decompress limits · hash", "control"),
        step(270, "I3", "Store object", "key = tenant/user/uuid — IAM prefix isolation", "action"),
        step(330, "I4", "Chunk + embed", "server stamps metadata (owner, tenant, acl, hash)", "control"),
        step(390, "I5", "Upsert into tenant partition only", "private ACL by default; shares are explicit rows", "control"),
        # Right column chat
        f'<rect x="760" y="95" width="680" height="40" rx="8" fill="{C["action_bg"]}" stroke="{C["action_bd"]}"/>',
        label(1100, 120, "PATH 2 — CHAT (read)", C["action_bd"], 13),
        # right steps with x offset - redefine inline
    ]
    def step_r(y, n, title, detail, kind="control"):
        colors = {
            "control": (C["control_bg"], C["control_bd"]),
            "model": (C["model_bg"], C["model_bd"]),
            "data": (C["untrusted_bg"], C["untrusted_bd"]),
            "ui": (C["panel"], C["line"]),
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
    parts += [
        step_r(150, "C1", "Authenticate chat", "same verified claims — discard body tenant/user", "control"),
        step_r(210, "C2", "build_prefilter(claims)", "partition ∩ (owner ∪ shares ∪ groups)", "control"),
        step_r(270, "C3", "ANN search with pre-filter", "unauthorized vectors never become candidates", "control"),
        step_r(330, "C4", "Output Gate", "hits enter prompt as DATA, not instructions", "control"),
        step_r(390, "C5", "LLM complete (no tools)", "answer text only — pipeline shape", "model"),
        step_r(450, "C6", "CSP-hardened render", "no remote img/connect · encode markdown", "action"),
        # connectors note
        f'<rect x="36" y="480" width="700" height="200" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}"/>',
        label(56, 510, "Identity is the spine", C["ok"], 14, "start", "800"),
        label(56, 540, "Upload and chat both derive tenancy from the token.", C["ink"], 12, "start"),
        label(56, 565, "The model never sees credentials and never sets filters.", C["ink"], 12, "start"),
        label(56, 590, "Poisoned files stay under the uploader's ACL;", C["ink"], 12, "start"),
        label(56, 615, "they cannot widen retrieval for other users.", C["ink"], 12, "start"),
        label(56, 650, "If you add tools later → Example A gates.", C["muted"], 12, "start"),
        f'<rect x="760" y="520" width="680" height="160" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}"/>',
        label(780, 550, "Attacks stopped on this diagram", C["danger"], 14, "start", "800"),
        label(780, 580, "• Client forges tenant_id / user_id", C["ink"], 12, "start"),
        label(780, 605, "• Alice retrieves Bob's private doc", C["ink"], 12, "start"),
        label(780, 630, "• Markdown image phones home (EchoLeak-class)", C["ink"], 12, "start"),
        label(780, 655, "• Upload becomes global corpus without ownership", C["ink"], 12, "start"),
        # bottom residual
        f'<rect x="36" y="720" width="1404" height="100" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(56, 755, "Honest residual", C["ink"], 13, "start", "800"),
        label(56, 780, "A user can still receive a wrong summary of a file they own if that file is poisoned (LLM09).", C["muted"], 12, "start"),
        label(56, 805, "Deliberate oversharing and shared-inference KV side channels are out of band for RAG ACL — see Ch.7 KV Cache / Example C.", C["muted"], 12, "start"),
        f'<rect x="36" y="850" width="1404" height="200" rx="12" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(56, 880, "Pseudo-code (chat)", C["control_hd"], 13, "start", "800"),
        label(56, 910, "claims = verify_jwt(req)", C["ink"], 12, "start"),
        label(56, 935, "filt = build_prefilter(claims)          # NOT from req.json", C["ink"], 12, "start"),
        label(56, 960, "hits = search(tenant_ns(claims.tenant), q, prefilter=filt)", C["ink"], 12, "start"),
        label(56, 985, "return render(llm(user=q, data=output_gate(hits)), csp=LOCKDOWN)", C["ink"], 12, "start"),
        label(56, 1020, "No tools bound by default.", C["muted"], 12, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def main() -> None:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, fn in [
        ("17-appendix-e-implementation-reference_13.svg", svg_13),
        ("17-appendix-e-implementation-reference_14.svg", svg_14),
        ("17-appendix-e-implementation-reference_15.svg", svg_15),
    ]:
        content = fn()
        (SRC_DIR / name).write_text(content, encoding="utf-8")
        (OUT_DIR / name).write_text(content, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
