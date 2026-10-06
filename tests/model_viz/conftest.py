"""Fixtures for the model-viz viewer tests: one Chromium per session, a fresh page per test.

Page helpers live in viewer_harness.py. Every page fixture fails its test on any page error,
console error or http(s) request (plan PD7).
"""

import pytest
from viewer_harness import (
    FIXTURE,
    FIXTURE_SHA256,
    INSTALL_HELP,
    fixture_digest,
    load_snapshot,
    open_viewer,
)

try:
    from playwright.sync_api import Error as PlaywrightError
except ImportError as exc:  # plan PD4: fail the viewer tests loudly, not the whole collection
    _PLAYWRIGHT_IMPORT_ERROR: ImportError | None = exc
else:
    _PLAYWRIGHT_IMPORT_ERROR = None


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


@pytest.fixture(scope="session")
def fixture_path():
    digest = fixture_digest()
    if digest != FIXTURE_SHA256:
        pytest.fail(
            f"{FIXTURE} changed: SHA-256 {digest}; the spec's counts are for {FIXTURE_SHA256}. "
            "Re-probe the fixture facts; do not edit the expected counts to pass."
        )
    return FIXTURE


@pytest.fixture
def viewer_page(browser):
    page, problems = open_viewer(browser)
    yield page
    page.close()
    problems.assert_clean()


@pytest.fixture
def fixture_page(viewer_page, fixture_path):
    assert load_snapshot(viewer_page, fixture_path) == "ready"
    return viewer_page


@pytest.fixture(scope="module")
def loaded_fixture_page(browser, fixture_path):
    """One loaded page shared by a module's read-only sweeps (plan PD2)."""
    page, problems = open_viewer(browser)
    assert load_snapshot(page, fixture_path) == "ready"
    yield page
    page.close()
    problems.assert_clean()
