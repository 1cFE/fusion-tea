"""Fixtures for the model evolution page tests: the built page, and one Chromium per session.

The page is built once per session by running build.py the way a person would. A page fixture fails
its test on any page error, console error or http(s) request, as the v2 viewer fixtures do.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
BUILDER = REPO / "src/model_viz/evolution/build.py"
MANIFEST = REPO / "src/model_viz/evolution/frames.json"
INSTALL_HELP = (
    "The evolution page tests need Playwright and Chromium: `uv sync --extra e2e` "
    "then `uv run playwright install chromium`."
)

try:
    from playwright.sync_api import Error as PlaywrightError
except ImportError as exc:  # fail these tests loudly, not the whole collection
    _PLAYWRIGHT_IMPORT_ERROR: ImportError | None = exc
else:
    _PLAYWRIGHT_IMPORT_ERROR = None


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True
    ).stdout


@pytest.fixture(scope="session")
def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def built(tmp_path_factory) -> dict:
    """The built page, its frame data, and the worktree status before and after the build."""
    out = tmp_path_factory.mktemp("evolution")
    page, data = out / "evolution.html", out / "data.json"
    before = git("status", "--porcelain")
    result = subprocess.run(
        [sys.executable, str(BUILDER), "-o", str(page), "--data-out", str(data)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"build.py failed (are the manifest's commits in this clone?):\n{result.stderr}"
    )
    return {
        "page": page,
        "data": json.loads(data.read_text(encoding="utf-8")),
        "status_before": before,
        "status_after": git("status", "--porcelain"),
    }


@pytest.fixture(scope="session")
def browser(playwright_manager):
    if _PLAYWRIGHT_IMPORT_ERROR is not None:
        pytest.fail(f"{INSTALL_HELP}\nImport failed: {_PLAYWRIGHT_IMPORT_ERROR}")
    try:
        chromium = playwright_manager.chromium.launch()
    except PlaywrightError as exc:
        pytest.fail(f"{INSTALL_HELP}\nChromium launch failed: {exc}")
    yield chromium
    chromium.close()


@pytest.fixture
def evo_page(browser, built):
    problems: list[str] = []
    page = browser.new_page(viewport={"width": 1400, "height": 1000})
    page.on("pageerror", lambda err: problems.append(f"page error: {err}"))
    page.on(
        "console",
        lambda msg: (
            problems.append(f"console {msg.type}: {msg.text}") if msg.type == "error" else None
        ),
    )
    page.on(
        "request",
        lambda req: (
            problems.append(f"network request: {req.url}") if req.url.startswith("http") else None
        ),
    )
    page.goto(built["page"].as_uri(), wait_until="load")
    page.wait_for_selector("body[data-evo-state=ready]", timeout=30_000)
    yield page
    page.close()
    assert problems == [], "\n".join(problems)
