#!/usr/bin/env python3
"""Example C — self-hosted serving platform diagrams (_16 unsecured, _17 secured, _18 flows)."""

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
    tmp = SRC_DIR / "_raster_c_tmp.js"
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


def svg_16() -> str:
    W, H = 1480, 940
    p = "c16"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example C — Unsecured self-hosted serving platform",
                  "Unsigned weights on a shared GPU; global prefix KV; one cluster-wide identity; leftover pages and open egress.",
                  "UNSECURED", C["danger"]),
        card(40, 100, 210, 56, "1", "Calling apps", "RAG · agents · batch", C["panel"], C["line"], C["ink"], p),
        card(280, 100, 210, 56, "2", "Edge (thin)", "public Service / :8000", C["untrusted_bg"], C["danger"], C["danger"], p),
        arrow(250, 128, 280, 128, p=p),
        f'<rect x="40" y="180" width="700" height="230" rx="14" fill="{C["untrusted_bg"]}" stroke="{C["untrusted_bd"]}" stroke-width="1.5" filter="url(#{p}soft)"/>',
        label(56, 208, "ARTIFACT PATH — NO ADMIT", C["untrusted_hd"], 13, "start", "800"),
        card(56, 225, 210, 60, "4", "Registry", "anyone can push", C["panel"], C["untrusted_bd"], C["untrusted_bd"], p),
        card(286, 225, 210, 60, "3", "Admission", ":latest · no cosign", C["panel"], C["untrusted_bd"], C["untrusted_bd"], p),
        card(516, 225, 200, 60, "8", "LoRA drop-in", "unsigned adapter", C["panel"], C["danger"], C["danger"], p),
        card(56, 310, 660, 70, "11", "CT pipeline", "hot-reload adapter in prod — skips scan / sign / Evidence Pack", C["panel"], C["danger"], C["danger"], p),
        f'<rect x="770" y="180" width="340" height="230" rx="14" fill="{C["model_bg"]}" stroke="{C["model_bd"]}" filter="url(#{p}soft)"/>',
        label(790, 208, "SHARED COMPUTE", C["model_hd"], 12, "start", "800"),
        card(790, 225, 300, 56, "5", "vLLM / KServe", "one replica, all tenants", C["panel"], C["model_bd"], C["model_bd"], p),
        card(790, 300, 140, 80, "6", "GPU pool", "time-slice only", C["untrusted_bg"], C["danger"], C["danger"], p),
        card(950, 300, 140, 80, "7", "KV cache", "global prefix ON", C["untrusted_bg"], C["danger"], C["danger"], p),
        f'<rect x="1140" y="180" width="300" height="230" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}" stroke-width="1.5"/>',
        label(1290, 210, "What fails", C["danger"], 14, weight="800"),
        label(1160, 240, "• Unsigned weights on GPU", C["ink"], 12, "start"),
        label(1160, 265, "• Adapter skips ModelScan", C["ink"], 12, "start"),
        label(1160, 290, "• Global prefix (no cache_salt)", C["ink"], 12, "start"),
        label(1160, 315, "• One god ServiceAccount", C["ink"], 12, "start"),
        label(1160, 340, "• AuthN only — no serve AuthZ", C["ink"], 12, "start"),
        label(1160, 365, "• Public :8000 + open egress", C["ink"], 12, "start"),
        card(40, 440, 340, 70, "9", "Serving identity", "cluster-wide SA + one engine key", C["untrusted_bg"], C["danger"], C["danger"], p),
        card(400, 440, 340, 70, "10", "Network / egress", "pods can phone home / mine", C["untrusted_bg"], C["danger"], C["danger"], p),
        card(760, 440, 340, 70, "7b", "Persisted form of #7", "CAG/NFS dump · cluster-wide read", C["untrusted_bg"], C["danger"], C["danger"], p),
        f'<path d="M1020,380 C1100,380 1125,300 1140,278" fill="none" stroke="{C["danger"]}" stroke-width="2.2" marker-end="url(#{p}arrR)"/>',
        label(1020, 428, "RED: B measures A's prefix (PromptPeek)", C["danger"], 12),
        f'<rect x="40" y="540" width="1400" height="90" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(60, 575, "Naive mental model: \"if the apps do RAG ACL, the GPU is just infra.\"", C["ink"], 13, "start"),
        label(60, 605, "Reality: shared prefix KV, leftover GPU pages, and unsigned adapters are platform leaks — they bypass application ACL.", C["muted"], 12, "start"),
        label(60, 680, "Components 1–11 match the Example C table.", C["muted"], 11, "start"),
        f'<rect x="40" y="720" width="1400" height="160" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}"/>',
        label(60, 755, "Red paths on this diagram", C["danger"], 14, "start", "800"),
        label(60, 790, "• Hugging Face :latest → GPU with no ModelScan / cosign", C["ink"], 12, "start"),
        label(60, 820, "• Tenant B times TTFT against Tenant A's cached system prefix", C["ink"], 12, "start"),
        label(60, 850, "• Session ends; next job reconstructs leftover KV / GPU residue", C["ink"], 12, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def svg_17() -> str:
    W, H = 1580, 1120
    p = "c17"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        defs(p),
        f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>',
        title_bar(W, "Example C — Secure self-hosted serving platform",
                  "Fail-closed admit · gateway authN+authZ · cache_salt · LoRA↔base digest · isolate over hard sanitize claims.",
                  "SECURED", C["ok"]),
        f'<rect x="36" y="95" width="200" height="36" rx="8" fill="#EEF2FF" stroke="#6366F1"/>',
        label(136, 118, "Plane A — apps", C["ink"], 11),
        f'<rect x="250" y="95" width="240" height="36" rx="8" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(370, 118, "Plane B — serving control", C["ink"], 11),
        f'<rect x="1076" y="95" width="240" height="36" rx="8" fill="{C["action_bg"]}" stroke="{C["action_bd"]}"/>',
        label(1196, 118, "Plane C — cluster / GPU", C["ink"], 11),
        label(560, 118, "Caller→engine authN ≠ data-plane PEP", C["muted"], 12, "start"),
        card(36, 150, 200, 56, "1", "Calling apps", "still own RAG / OBO", "#EEF2FF", "#6366F1", "#6366F1", p),
        gate(260, 152, 300, 56, "G", "AI Gateway", "authN · authZ · quota · audit (no raw prompt)", p),
        arrow(236, 178, 260, 178, "arrG", C["ok"], p=p),
        f'<rect x="36" y="230" width="500" height="300" rx="14" fill="{C["control_bg"]}" stroke="{C["control_bd"]}" stroke-width="1.4" filter="url(#{p}soft)"/>',
        label(56, 258, "ADMIT PATH (artifacts) — fail closed", C["control_hd"], 13, "start", "800"),
        gate(56, 275, 460, 48, "AD", "Admission", "safetensors · cosign · legacy ModelScan · Fail", p),
        card(56, 340, 220, 56, "4", "Registry", "signed OCI / snapshots", C["panel"], C["control_bd"], C["control_bd"], p),
        card(296, 340, 220, 56, "8", "Adapters", "bind base_model_digest · safetensors", C["panel"], C["control_bd"], C["control_bd"], p),
        card(56, 420, 460, 70, "11", "CT / LoRA promote", "scan · sign · admit · Evidence Pack — same Path 1", C["panel"], C["control_bd"], C["control_bd"], p),
        f'<rect x="556" y="230" width="500" height="300" rx="14" fill="{C["control_bg"]}" stroke="{C["control_bd"]}" stroke-width="1.4" filter="url(#{p}soft)"/>',
        label(576, 258, "SERVE PATH (inference) — Plane B", C["control_hd"], 13, "start", "800"),
        gate(576, 275, 460, 48, "AZ", "Authorize", "tenant · model · LoRA · tier · quota", p),
        gate(576, 340, 460, 48, "KV", "Tenant KV bind", "overwrite cache_salt (vLLM ≥ 0.9.0)", p),
        card(576, 405, 220, 56, "5", "vLLM / KServe", "NetworkPolicy to engine", C["panel"], C["control_bd"], C["control_bd"], p),
        card(816, 405, 220, 56, "7", "KV / CAG", "lifecycle: create · purge", C["panel"], C["control_bd"], C["control_bd"], p),
        f'<rect x="1076" y="230" width="468" height="300" rx="14" fill="{C["action_bg"]}" stroke="{C["action_bd"]}" filter="url(#{p}soft)"/>',
        label(1096, 258, "CLUSTER / GPU (Plane C)", C["action_bd"], 12, "start", "800"),
        card(1096, 275, 428, 56, "6", "GPU pool", "MIG device / dedicated · never MPS-as-isolation", C["panel"], C["action_bd"], C["action_bd"], p),
        card(1096, 345, 428, 56, "9", "Serving identity", "mTLS/SPIFFE → engine (not GPU) · rotate/revoke", C["panel"], C["action_bd"], C["action_bd"], p),
        card(1096, 415, 428, 56, "10", "Egress + telemetry", "default-deny · no public :8000 · metadata-only audit", C["panel"], C["action_bd"], C["action_bd"], p),
        f'<rect x="36" y="550" width="1020" height="90" rx="14" fill="{C["model_bg"]}" stroke="{C["model_bd"]}" filter="url(#{p}soft)"/>',
        label(56, 580, "Prefix cache = security setting (PromptPeek / CVE-2025-46570)", C["model_hd"], 12, "start", "800"),
        label(56, 610, "High: OFF or per-tenant replica. Else: gateway OVERWRITES cache_salt=tenant. Never forward client salt.", C["ink"], 12, "start"),
        f'<rect x="1076" y="550" width="468" height="90" rx="14" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(1096, 580, "MIG note (K8s vs VM)", C["ink"], 12, "start", "800"),
        label(1096, 610, "K8s MIG OK for pods; VM multi-tenant needs vGPU.", C["muted"], 11, "start"),
        f'<rect x="36" y="660" width="1508" height="100" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}" stroke-width="1.5"/>',
        label(56, 690, "Primary enforcement chain", C["ok"], 14, "start", "800"),
        label(56, 718, "signed + format-safe artifact → fail-closed admit → GPU tier → gateway authN+authZ → overwrite salt → generate → purge KV", C["ink"], 13, "start"),
        label(56, 742, "Caller→engine ≠ RAG ACL. Shared-process batching ≠ OS isolation. LeftoverLocals ≠ NVIDIA (KV/VRAM still matters).", C["muted"], 12, "start"),
        f'<rect x="36" y="780" width="740" height="280" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(56, 810, "Two identities + AuthZ", C["ink"], 14, "start", "800"),
        label(56, 845, "Engine key / mTLS: may this caller hit this replica?", C["ink"], 12, "start"),
        label(56, 875, "Gateway AuthZ: tenant · model · LoRA · tier · quota", C["ink"], 12, "start"),
        label(56, 905, "App user token: whose data is in the prompt? (not here)", C["ink"], 12, "start"),
        label(56, 940, "Anti-pattern: cluster-wide long-lived engine key", C["danger"], 12, "start"),
        label(56, 970, "Anti-pattern: forward client cache_salt / use MPS as isolation", C["danger"], 12, "start"),
        label(56, 1000, "Anti-pattern: client-supplied adapter_id / LoRA path", C["danger"], 12, "start"),
        f'<rect x="800" y="780" width="744" height="280" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(820, 810, "Control map", C["ink"], 14, "start", "800"),
        gate(820, 835, 340, 48, "AD", "Admit", "safetensors · fail-closed", p),
        gate(1180, 835, 340, 48, "KV", "KV + salt", "overwrite · purge", p),
        gate(820, 905, 340, 48, "G", "Gateway", "authN + authZ · no prompt log", p),
        gate(1180, 905, 340, 48, "GPU", "Isolate", "MIG/dedicated · not MPS", p),
        label(820, 980, "Hard tenancy: separate vLLM pod per trust-group when needed.", C["muted"], 12, "start"),
        label(820, 1010, "YAML stays in Chapter 16 — this card is the composition.", C["muted"], 12, "start"),
        "</svg>",
    ]
    return "\n".join(parts)


def svg_18() -> str:
    W, H = 1480, 1220
    p = "c18"

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
        title_bar(W, "Example C — Admit + serve data flows",
                  "Left: fail-closed admit. Right: authN → authZ → overwrite cache_salt (vLLM ≥ 0.9.0) → generate → purge.",
                  "DATA FLOW", C["accent"]),
        f'<rect x="36" y="95" width="700" height="40" rx="8" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(386, 120, "PATH 1 — ADMIT (artifacts)", C["control_hd"], 13),
        step(150, "A1", "Pull candidate release", "image digest + weights + adapters", "action"),
        step(210, "A2", "Format + signature", "safetensors allowlist · cosign — fail closed", "control"),
        step(270, "A3", "LoRA ↔ base bind", "base_model_digest · arch/dtype · legacy ModelScan if needed", "control"),
        step(330, "A4", "Admission policy", "digest pin · GPU tier · webhook Fail + HA", "control"),
        step(390, "A5", "Evidence Pack", "hash · sig · validation URI · CP8 approval", "control"),
        f'<rect x="760" y="95" width="680" height="40" rx="8" fill="{C["action_bg"]}" stroke="{C["action_bd"]}"/>',
        label(1100, 120, "PATH 2 — SERVE (generate)", C["action_bd"], 13),
        step_r(150, "S1", "Authenticate to engine", "mTLS / SPIFFE / short-lived key — not data ACL", "control"),
        step_r(210, "S2", "Authorize request", "tenant · model · LoRA · GPU tier · quota", "control"),
        step_r(270, "S3", "Overwrite cache_salt", "gateway sets salt (vLLM ≥ 0.9.0) — never client", "control"),
        step_r(330, "S4", "Generate", "engine.generate(..., kv_partition, cache_salt, lora)", "model"),
        step_r(390, "S5", "Cleanup", "purge KV · prefer MIG/dedicated over hard sanitize", "control"),
        f'<rect x="36" y="470" width="700" height="220" rx="12" fill="{C["panel"]}" stroke="{C["ok"]}"/>',
        label(56, 500, "CT / LoRA re-enter Path 1", C["ok"], 14, "start", "800"),
        label(56, 530, "No side door for adapters. Registry resolves LoRA — never client adapter_id.", C["ink"], 12, "start"),
        label(56, 555, "Caller→engine authN is not application authorization.", C["ink"], 12, "start"),
        label(56, 580, "Safetensors = format control; ModelScan = legacy serialization — signed ≠ safe.", C["ink"], 12, "start"),
        label(56, 615, "YAML/Helm in Chapter 16. Managed API? Skip C → E.1.2 + Appendix D.", C["muted"], 12, "start"),
        f'<rect x="760" y="470" width="680" height="220" rx="12" fill="{C["panel"]}" stroke="{C["danger"]}"/>',
        label(780, 500, "Attacks stopped on this diagram", C["danger"], 14, "start", "800"),
        label(780, 535, "• Unsigned / :latest image reaches a GPU", C["ink"], 12, "start"),
        label(780, 560, "• PromptPeek / CVE-2025-46570 (no overwritten salt)", C["ink"], 12, "start"),
        label(780, 585, "• LoRA hot-load / client adapter_id spoof", C["ink"], 12, "start"),
        label(780, 610, "• Leftover session KV after request end", C["ink"], 12, "start"),
        label(780, 635, "• Anonymous generate on public :8000", C["ink"], 12, "start"),
        label(780, 660, "• Admit continues when cosign/gates are down", C["ink"], 12, "start"),
        f'<rect x="36" y="710" width="1404" height="120" rx="12" fill="{C["panel"]}" stroke="{C["line"]}"/>',
        label(56, 740, "Honest residual", C["ink"], 13, "start", "800"),
        label(56, 768, "Host/CSP can read externalized KV. K8s MIG helps pods; VM multi-tenant needs MIG+vGPU. MPS ≠ isolation.", C["muted"], 12, "start"),
        label(56, 793, "PagedAttention shares one process. LeftoverLocals CVE is non-NVIDIA; KV/VRAM reuse still matters on NVIDIA.", C["muted"], 12, "start"),
        label(56, 818, "App still owns RAG ACL: isolated GPU answers from Bob's chunk if the app put it in the prompt (B/D).", C["muted"], 12, "start"),
        f'<rect x="36" y="850" width="1404" height="310" rx="12" fill="{C["control_bg"]}" stroke="{C["control_bd"]}"/>',
        label(56, 880, "Pseudo-code (serve)", C["control_hd"], 13, "start", "800"),
        label(56, 910, "app = verify_engine_caller(req)                 # mTLS / SPIFFE — not data ACL", C["ink"], 12, "start"),
        label(56, 938, "authorize(app, req)                            # tenant · model · LoRA · tier · quota", C["ink"], 12, "start"),
        label(56, 966, "lora = registry.adapter_for(app.tenant)        # never body.adapter_id", C["ink"], 12, "start"),
        label(56, 994, "req.cache_salt = app.tenant                   # OVERWRITE client salt (vLLM ≥ 0.9.0)", C["ink"], 12, "start"),
        label(56, 1022, "out = engine.generate(req.prompt, kv_partition=kv, cache_salt=req.cache_salt, lora=lora)", C["ink"], 12, "start"),
        label(56, 1050, "cleanup_kv(kv)                                 # prefer MIG/dedicated over claiming full sanitize", C["ink"], 12, "start"),
        label(56, 1085, "High sensitivity: prefix OFF or dedicated replica. Omit/forward client salt ⇒ unsafe share.", C["muted"], 12, "start"),
        label(56, 1115, "Telemetry: tenant/model/tokens/latency only — no raw prompt/completion by default.", C["muted"], 12, "start"),
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
        ("17-appendix-e-implementation-reference_16.svg", svg_16),
        ("17-appendix-e-implementation-reference_17.svg", svg_17),
        ("17-appendix-e-implementation-reference_18.svg", svg_18),
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
