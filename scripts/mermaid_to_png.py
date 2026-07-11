#!/usr/bin/env python3
"""Render Mermaid diagrams to high-resolution PNG for Word export."""
from __future__ import annotations

import asyncio
import re
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

# High-DPI export defaults (override with MERMAID_SCALE / MERMAID_VIEWPORT_WIDTH env if needed).
SCALE_FACTOR = 3
VIEWPORT_WIDTH = 5200
VIEWPORT_HEIGHT = 2000
MIN_FONT_PX = 22

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  html, body {{
    margin: 0;
    padding: 24px;
    background: white;
    width: max-content;
    min-width: 100%;
  }}
  .mermaid {{
    display: inline-block;
  }}
  .mermaid svg {{
    max-width: none !important;
    width: auto !important;
    height: auto !important;
  }}
</style>
</head>
<body>
<div class="mermaid">{diagram}</div>
<script>
  (async () => {{
    mermaid.initialize({{
      startOnLoad: false,
      theme: "default",
      securityLevel: "loose",
      flowchart: {{
        useMaxWidth: false,
        htmlLabels: true,
        curve: "basis",
        padding: 24,
        nodeSpacing: 60,
        rankSpacing: 80
      }},
      themeVariables: {{
        fontSize: "{font_px}px",
        fontFamily: "Segoe UI, Arial, sans-serif"
      }}
    }});
    try {{
      await mermaid.run({{ querySelector: ".mermaid" }});
      window.__MERMAID_READY__ = true;
    }} catch (e) {{
      window.__MERMAID_ERROR__ = String(e);
      window.__MERMAID_READY__ = false;
    }}
  }})();
</script>
</body>
</html>
"""


def ensure_playwright() -> None:
    try:
        from playwright.async_api import async_playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])


async def _launch_browser(p):
    try:
        return await p.chromium.launch(channel="chrome", headless=True)
    except Exception:
        return await p.chromium.launch(channel="msedge", headless=True)


class MermaidRenderer:
    """Reuse one browser for all diagrams in a sync run (avoids 20+ cold starts)."""

    def __init__(self) -> None:
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    async def start(self) -> None:
        from playwright.async_api import async_playwright

        self._playwright = await async_playwright().start()
        self._browser = await _launch_browser(self._playwright)
        self._context = await self._browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            device_scale_factor=SCALE_FACTOR,
        )
        self._page = await self._context.new_page()

    async def close(self) -> None:
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        self._page = None

    async def render(self, mermaid_src: str, output: Path, retries: int = 2) -> None:
        if self._page is None:
            raise RuntimeError("MermaidRenderer not started")

        html = HTML_TEMPLATE.format(diagram=mermaid_src.strip(), font_px=MIN_FONT_PX)
        output.parent.mkdir(parents=True, exist_ok=True)

        is_horizontal = "flowchart LR" in mermaid_src or "graph LR" in mermaid_src
        viewport_w = VIEWPORT_WIDTH if is_horizontal else max(2800, VIEWPORT_WIDTH // 2)
        await self._page.set_viewport_size({"width": viewport_w, "height": VIEWPORT_HEIGHT})

        last_err: Exception | None = None
        for attempt in range(retries + 1):
            try:
                await self._page.set_content(html, wait_until="domcontentloaded")
                await self._page.wait_for_function(
                    "() => window.__MERMAID_READY__ === true || window.__MERMAID_ERROR__",
                    timeout=90_000,
                )
                err = await self._page.evaluate("() => window.__MERMAID_ERROR__ || null")
                if err:
                    raise RuntimeError(f"Mermaid JS error: {err}")

                await self._page.wait_for_selector(".mermaid svg", timeout=30_000, state="attached")
                await asyncio.sleep(0.4)

                await self._page.evaluate(
                    """() => {
                      const root = document.querySelector('.mermaid');
                      const svg = root && root.querySelector('svg');
                      if (!root || !svg) return;
                      root.style.display = 'inline-block';
                      root.style.visibility = 'visible';
                      root.style.overflow = 'visible';
                      const vb = svg.viewBox && svg.viewBox.baseVal;
                      if (vb && vb.width > 0 && vb.height > 0) {
                        svg.setAttribute('width', String(vb.width));
                        svg.setAttribute('height', String(vb.height));
                        root.style.width = vb.width + 'px';
                        root.style.height = vb.height + 'px';
                      }
                      svg.removeAttribute('max-width');
                      svg.style.maxWidth = 'none';
                      svg.style.visibility = 'visible';
                      svg.style.display = 'block';
                    }"""
                )
                await asyncio.sleep(0.2)

                target = self._page.locator(".mermaid").first
                box = await target.bounding_box()
                if not box or box["width"] < 1 or box["height"] < 1:
                    box = await self._page.locator("svg").first.bounding_box()
                if not box:
                    raise RuntimeError("Could not measure Mermaid diagram bounds")

                await self._page.screenshot(
                    path=str(output),
                    type="png",
                    scale="device",
                    clip={
                        "x": max(0, box["x"] - 8),
                        "y": max(0, box["y"] - 8),
                        "width": box["width"] + 16,
                        "height": box["height"] + 16,
                    },
                )
                if output.exists() and output.stat().st_size >= 500:
                    return
                raise RuntimeError(f"PNG too small: {output}")
            except Exception as exc:
                last_err = exc
                if attempt < retries:
                    await asyncio.sleep(1.5)
        raise RuntimeError(f"Mermaid render failed after {retries + 1} attempts: {last_err}") from last_err


_active_renderer: MermaidRenderer | None = None
_session_loop: asyncio.AbstractEventLoop | None = None


@contextmanager
def mermaid_renderer_session() -> Iterator[MermaidRenderer]:
    """Open one shared browser for an entire docx sync."""
    global _active_renderer, _session_loop
    ensure_playwright()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    renderer = MermaidRenderer()
    loop.run_until_complete(renderer.start())
    _active_renderer = renderer
    _session_loop = loop
    try:
        yield renderer
    finally:
        loop.run_until_complete(renderer.close())
        _active_renderer = None
        _session_loop = None
        loop.close()


async def render_one(mermaid_src: str, output: Path) -> None:
    renderer = MermaidRenderer()
    await renderer.start()
    try:
        await renderer.render(mermaid_src, output)
    finally:
        await renderer.close()


def render_mermaid_to_png(mermaid_src: str, output: Path) -> Path:
    if _active_renderer is not None and _session_loop is not None:
        _session_loop.run_until_complete(_active_renderer.render(mermaid_src, output))
    else:
        asyncio.run(render_one(mermaid_src, output))
    if not output.exists() or output.stat().st_size < 500:
        raise RuntimeError(f"Mermaid render failed or too small: {output}")
    return output


def replace_mermaid_with_images(text: str, assets_dir: Path, prefix: str) -> str:
    counter = {"n": 0}

    def repl(match: re.Match) -> str:
        counter["n"] += 1
        src = match.group(1).strip()
        png = assets_dir / f"{prefix}_{counter['n']:02d}.png"
        if not (png.exists() and png.stat().st_size >= 500):
            render_mermaid_to_png(src, png)
        path = png.resolve().as_posix()
        caption = "Lifecycle flow diagram" if "flowchart" in src else "Architecture diagram"
        return f"\n\n![{caption}]({path}){{width=6.3in}}\n\n"

    return re.sub(r"```mermaid\s*\n(.*?)\n```", repl, text, flags=re.DOTALL)


if __name__ == "__main__":
    sample = """flowchart LR
    A[1 Initiate Change] --> B[2 Load Artifacts]
    B --> C[3 Security & Quality Review]
    C --> D[4 Data / Artifact Decision]
    D --> E[5 Train or Configure]
    E --> F[6 Evaluate]
    F --> G[7 Security Validation]
    G --> H[8 Release Decision]
    H --> I[9 Integrity and Provenance]
    I --> J[10 Store and Monitor]"""
    out = Path("_mermaid_test/hires_pipeline.png")
    render_mermaid_to_png(sample, out)
    print(f"Wrote {out} ({out.stat().st_size:,} bytes)")
