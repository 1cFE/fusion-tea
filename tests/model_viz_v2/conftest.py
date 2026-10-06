"""Fixtures for the model viewer v2 tests: one Chromium per session, 1,400 × 900 pages.

Page helpers live in viewer2_harness.py. Every page fixture fails its test on any page error,
console error, policed warning or http(s) request (plan PD11). Page sharing follows plan PD1.
"""

import pytest
from viewer2_harness import (
    FIXTURE,
    FIXTURE_SHA256,
    INSTALL_HELP,
    fixture_digest,
    load_snapshot,
    open_v1,
    open_v2,
)

try:
    from playwright.sync_api import Error as PlaywrightError
except ImportError as exc:  # fail the viewer tests loudly, not the whole collection
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
def v2_page(browser):
    """A fresh, unloaded page for tests that assert zoom, pan or reference geometry (PD1)."""
    page, problems = open_v2(browser)
    yield page
    page.close()
    problems.assert_clean()


@pytest.fixture(scope="module")
def loaded_v2_page(browser, fixture_path):
    """One loaded page shared by a module's read-only sweeps (PD1)."""
    page, problems = open_v2(browser)
    assert load_snapshot(page, fixture_path) == "ready"
    yield page
    page.close()
    problems.assert_clean()


@pytest.fixture
def reset_v2(loaded_v2_page):
    """Put the shared page back to all open before a test (PD1)."""
    loaded_v2_page.evaluate("() => window.modelVizApp.expandAll()")
    return loaded_v2_page


@pytest.fixture
def v1_page(browser):
    """A fresh, unloaded v1 page for the load-error comparison (plan PD9)."""
    page, problems = open_v1(browser)
    yield page
    page.close()
    problems.assert_clean()


@pytest.fixture(scope="module")
def v1_loaded(browser, fixture_path):
    """v1's page with the fixture loaded, for the differential panel check (design D45)."""
    page, problems = open_v1(browser)
    assert load_snapshot(page, fixture_path) == "ready"
    yield page
    page.close()
    problems.assert_clean()
