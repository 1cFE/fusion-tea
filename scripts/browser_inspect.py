"""browser_inspect — drive Playwright with chained step flags, capture screenshots + page state.

Designed for Claude Code sessions working on browser-rendered UIs (the concept explorer, HTML
explainers, anything served on localhost). Each --shot writes a PNG **and** a JSON sidecar so
the agent can Read the image AND check console errors / page errors / element text without
re-running the script.

Step flags execute in the order they appear on the command line. Mix and match.

Examples:
    # quick: load a page, screenshot it
    uv run python scripts/browser_inspect.py --base http://localhost:8421 \\
        --goto / --shot home

    # multi-step: navigate, screenshot, click, screenshot
    uv run python scripts/browser_inspect.py --base http://localhost:8421 \\
        --goto /concept/19 --shot before \\
        --click "button:has-text('Expand CAS22')" --wait 500 --shot after

    # structured inspection: read element text, run JS
    uv run python scripts/browser_inspect.py --base http://localhost:8421 \\
        --session lcoe-check --clear --goto /concept/19 \\
        --read ".headline-lcoe=lcoe" --eval "document.title"

Output goes to /tmp/browser_inspect/{session}/ (session defaults to 'default').
Each --shot writes <name>.png + <name>.json (url, title, console, page_errors).
--read appends to reads.json; --eval appends to evals.json.
session.json summarizes every step (always written, even on failure).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_SESSION = "default"
SESSION_ROOT = Path("/tmp/browser_inspect")
DEFAULT_VIEWPORT = (1600, 1100)
DEFAULT_DPR = 2
DEFAULT_WAIT_MS = 800

STEP_FLAGS: dict[str, tuple[str, str, str]] = {
    "--goto":      ("goto",      "PATH",            "navigate to URL (or path appended to --base)"),
    "--shot":      ("shot",      "NAME",            "full-page PNG + JSON sidecar"),
    "--shot-vp":   ("shot_vp",   "NAME",            "viewport-only PNG + JSON sidecar"),
    "--click":     ("click",     "SELECTOR",        "click first element matching selector"),
    "--fill":      ("fill",      "SELECTOR=VALUE",  "type VALUE into input"),
    "--press":     ("press",     "[SELECTOR=]KEY",  "press key on element, or globally if no '='"),
    "--hover":     ("hover",     "SELECTOR",        "hover over element"),
    "--wait":      ("wait",      "MS",              "wait fixed milliseconds"),
    "--wait-for":  ("wait_for",  "SELECTOR",        "wait for element to be visible (10s timeout)"),
    "--scroll-to": ("scroll_to", "SELECTOR",        "scroll element into view"),
    "--read":      ("read",      "SELECTOR[=NAME]", "capture text content to reads.json"),
    "--eval":      ("eval",      "JS_EXPR",         "evaluate JS, capture result to evals.json"),
}


class StepAction(argparse.Action):
    """Append (kind, value) tuples in command-line order."""
    def __call__(self, parser, namespace, values, option_string=None):
        steps = getattr(namespace, "steps", None)
        if steps is None:
            steps = []
            setattr(namespace, "steps", steps)
        kind = STEP_FLAGS[option_string][0]
        steps.append((kind, values))


def split_kv(spec: str, allow_keyless: bool = False) -> tuple[str | None, str]:
    if "=" in spec:
        key, _, value = spec.partition("=")
        return key, value
    if allow_keyless:
        return None, spec
    raise ValueError(f"expected KEY=VALUE, got {spec!r}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="browser_inspect",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--base", default="",
                   help="base URL prefix; --goto PATH becomes base+path unless PATH is absolute")
    p.add_argument("--session", default=DEFAULT_SESSION,
                   help=f"session name; outputs go to {SESSION_ROOT}/<session>/ (default: %(default)s)")
    p.add_argument("--out", type=Path, default=None,
                   help="explicit output dir (overrides --session)")
    p.add_argument("--viewport", default=f"{DEFAULT_VIEWPORT[0]}x{DEFAULT_VIEWPORT[1]}",
                   help="WxH (default %(default)s)")
    p.add_argument("--dpr", type=int, default=DEFAULT_DPR,
                   help="device pixel ratio (default %(default)s)")
    p.add_argument("--default-wait", type=int, default=DEFAULT_WAIT_MS,
                   help=f"ms to wait after networkidle on each --goto (default %(default)s)")
    p.add_argument("--clear", action="store_true",
                   help="delete the session dir before running (else files accumulate)")
    p.add_argument("--quiet", action="store_true", help="suppress per-step prints")

    for flag, (_kind, metavar, helptext) in STEP_FLAGS.items():
        p.add_argument(flag, action=StepAction, metavar=metavar, help=helptext)

    return p


def main() -> int:
    args = build_parser().parse_args()
    steps: list[tuple[str, str]] = getattr(args, "steps", []) or []
    if not steps:
        sys.exit("no steps given. Add at least one --goto/--shot/--click/etc. (-h for help)")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright not installed. Run: uv add playwright && "
                 "uv run python -m playwright install chromium")

    out_dir = args.out if args.out else SESSION_ROOT / args.session
    if args.clear and out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    w_str, _, h_str = args.viewport.partition("x")
    viewport = {"width": int(w_str), "height": int(h_str)}

    def info(msg: str) -> None:
        if not args.quiet:
            print(msg)

    started = time.time()
    console: list[dict[str, Any]] = []
    page_errors: list[dict[str, Any]] = []
    reads: list[dict[str, Any]] = []
    evals: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    step_log: list[dict[str, Any]] = []

    def now_ms() -> int:
        return int((time.time() - started) * 1000)

    def write_shot(name: str, page, full_page: bool) -> None:
        png_path = out_dir / f"{name}.png"
        json_path = out_dir / f"{name}.json"
        page.screenshot(path=str(png_path), full_page=full_page)
        sidecar = {
            "name": name,
            "url": page.url,
            "title": page.title(),
            "viewport": viewport,
            "full_page": full_page,
            "ms": now_ms(),
            "console": list(console),
            "page_errors": list(page_errors),
        }
        json_path.write_text(json.dumps(sidecar, indent=2))
        artifacts.append({"name": name, "png": str(png_path), "json": str(json_path)})
        info(f"   -> {png_path}")

    def record(i: int, kind: str, value: Any, ok: bool, note: str = "") -> None:
        step_log.append({"i": i, "kind": kind, "value": value, "ok": ok, "ms": now_ms(), "note": note})

    exit_code = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport=viewport, device_scale_factor=args.dpr)
        page = ctx.new_page()

        page.on("console", lambda msg: console.append(
            {"type": msg.type, "text": msg.text, "ms": now_ms()}))
        page.on("pageerror", lambda err: page_errors.append(
            {"message": str(err), "ms": now_ms()}))

        try:
            for i, (kind, value) in enumerate(steps):
                info(f"[{i:02d}] {kind}: {value}")
                if kind == "goto":
                    url = value if value.startswith(("http://", "https://")) \
                        else args.base.rstrip("/") + value
                    if not url:
                        raise ValueError("--goto requires a URL (or set --base)")
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    if args.default_wait > 0:
                        page.wait_for_timeout(args.default_wait)
                elif kind in ("shot", "shot_vp"):
                    write_shot(value, page, full_page=(kind == "shot"))
                elif kind == "click":
                    page.locator(value).first.click(timeout=5000)
                elif kind == "fill":
                    sel, val = split_kv(value)
                    page.locator(sel).first.fill(val, timeout=5000)
                elif kind == "press":
                    sel, key = split_kv(value, allow_keyless=True)
                    if sel is None:
                        page.keyboard.press(key)
                    else:
                        page.locator(sel).first.press(key, timeout=5000)
                elif kind == "hover":
                    page.locator(value).first.hover(timeout=5000)
                elif kind == "wait":
                    page.wait_for_timeout(int(value))
                elif kind == "wait_for":
                    page.locator(value).first.wait_for(state="visible", timeout=10000)
                elif kind == "scroll_to":
                    page.locator(value).first.scroll_into_view_if_needed(timeout=5000)
                elif kind == "read":
                    sel, name = (value.split("=", 1) if "=" in value else (value, value))
                    text = page.locator(sel).first.text_content(timeout=5000)
                    reads.append({"name": name, "selector": sel, "text": text, "ms": now_ms()})
                    info(f"   read [{name}] = {text!r}")
                elif kind == "eval":
                    result = page.evaluate(value)
                    evals.append({"expr": value, "result": result, "ms": now_ms()})
                    info(f"   eval = {result!r}")
                else:
                    raise RuntimeError(f"unknown step kind: {kind}")
                record(i, kind, value, True)
        except Exception as e:
            msg = f"{type(e).__name__}: {e}"
            print(f"   ERROR at step [{i:02d}] {kind}: {msg}", file=sys.stderr)
            record(i, kind, value, False, msg)
            try:
                write_shot(f"_fail_{i:02d}_{kind}", page, full_page=False)
            except Exception as cap_err:
                print(f"   (failure-shot capture also failed: {cap_err})", file=sys.stderr)
            exit_code = 2
        finally:
            (out_dir / "reads.json").write_text(json.dumps(reads, indent=2))
            (out_dir / "evals.json").write_text(json.dumps(evals, indent=2))
            (out_dir / "session.json").write_text(json.dumps({
                "session": args.session,
                "out_dir": str(out_dir),
                "base": args.base,
                "viewport": viewport,
                "dpr": args.dpr,
                "duration_ms": now_ms(),
                "steps": step_log,
                "artifacts": artifacts,
                "reads_count": len(reads),
                "evals_count": len(evals),
                "console_count": len(console),
                "page_errors_count": len(page_errors),
                "exit_code": exit_code,
            }, indent=2))
            browser.close()

    info(f"\nSession: {out_dir}")
    info(f"  shots: {len(artifacts)}, reads: {len(reads)}, evals: {len(evals)}, "
         f"console: {len(console)}, page_errors: {len(page_errors)}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
