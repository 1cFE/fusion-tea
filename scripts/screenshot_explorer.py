"""Screenshot pages of the concept explorer (or any local URL) into /tmp for visual inspection.

Designed for Claude Code sessions: launch, navigate, optionally interact, then save full-page
PNGs to a known directory so the agent can Read them as image content.

Usage:
    # quick: a few URLs
    uv run python scripts/screenshot_explorer.py \\
        --base http://localhost:8421 \\
        --shot index:/ \\
        --shot concept_19:/concept/19 \\
        --shot compare:/compare?concepts=01,04,12&mode=integrated&left=capex&right=capex

    # custom output dir
    uv run python scripts/screenshot_explorer.py --out /tmp/my_shots --shot home:/

    # interaction recipe (click a button, then screenshot)
    uv run python scripts/screenshot_explorer.py --shot expanded:/concept/19 \\
        --click "button:has-text('Expand CAS22')" --then-shot expanded_cas22

Each --shot is "name:url_path". Names are used as filenames (PNG).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_BASE = "http://localhost:8421"
DEFAULT_OUT = Path("/tmp/explorer_shots")
DEFAULT_VIEWPORT = {"width": 1600, "height": 1100}
DEFAULT_DPR = 2  # device_scale_factor — higher = sharper, ~4x file size


def parse_shot(spec: str) -> tuple[str, str]:
    """'name:/path?qs' -> ('name', '/path?qs')."""
    if ":" not in spec:
        raise ValueError(f"--shot must be 'name:path', got {spec!r}")
    name, _, path = spec.partition(":")
    if not name or not path:
        raise ValueError(f"--shot must be 'name:path', got {spec!r}")
    return name, path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default=DEFAULT_BASE, help=f"base URL (default {DEFAULT_BASE})")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output dir (default {DEFAULT_OUT})")
    ap.add_argument("--shot", action="append", default=[], metavar="NAME:PATH",
                    help="capture this URL. Repeatable. Path is appended to --base.")
    ap.add_argument("--click", default=None, metavar="SELECTOR",
                    help="after the LAST --shot, click this Playwright selector "
                         "(e.g., \"button:has-text('Expand CAS22')\")")
    ap.add_argument("--then-shot", default=None, metavar="NAME",
                    help="after --click, capture again with this name")
    ap.add_argument("--viewport", default=f"{DEFAULT_VIEWPORT['width']}x{DEFAULT_VIEWPORT['height']}",
                    help="WxH (default 1600x1100)")
    ap.add_argument("--dpr", type=int, default=DEFAULT_DPR, help=f"device pixel ratio (default {DEFAULT_DPR})")
    ap.add_argument("--wait-ms", type=int, default=2000,
                    help="extra ms to wait after networkidle (charts often render late). Default 2000.")
    ap.add_argument("--clip-to-viewport", action="store_true",
                    help="capture only the viewport (not full page)")

    args = ap.parse_args()

    if not args.shot:
        ap.error("at least one --shot required")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright not installed. Run: uv pip install playwright && "
                 "uv run python -m playwright install chromium")

    args.out.mkdir(parents=True, exist_ok=True)
    w, _, h = args.viewport.partition("x")
    viewport = {"width": int(w), "height": int(h)}

    shots = [parse_shot(s) for s in args.shot]
    full_page = not args.clip_to_viewport

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport=viewport, device_scale_factor=args.dpr)
        page = ctx.new_page()

        for name, path in shots:
            # Accept absolute URLs (http://, https://, file://) verbatim; else prepend --base
            url = path if "://" in path else args.base.rstrip("/") + path
            print(f"[{name}] {url}")
            page.goto(url)
            page.wait_for_load_state("networkidle")
            if args.wait_ms > 0:
                page.wait_for_timeout(args.wait_ms)
            out_path = args.out / f"{name}.png"
            page.screenshot(path=str(out_path), full_page=full_page)
            print(f"   -> {out_path}")

        if args.click:
            print(f"[click] {args.click}")
            try:
                page.locator(args.click).first.click(timeout=5000)
                page.wait_for_timeout(args.wait_ms)
            except Exception as e:
                print(f"   click failed: {e}", file=sys.stderr)
                browser.close()
                return 2

            if args.then_shot:
                out_path = args.out / f"{args.then_shot}.png"
                page.screenshot(path=str(out_path), full_page=full_page)
                print(f"[{args.then_shot}] -> {out_path}")

        browser.close()

    print(f"\nDone. Screenshots in: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
