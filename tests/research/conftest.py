"""Fixtures for the research seam suite.

`knowledge_tree` builds a throwaway registry tree and points both the legacy
Zotero writer (which reads module-level path constants) and the new seam code
(which takes an injected paths object) at it. No `chdir`.
"""

import json
import threading
import urllib.request
from dataclasses import dataclass, fields
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
import zotero_ingest
import zotero_lib

MINIMAL_INDEX = """# Source Index

Source registry for the fusion TEA investigation.

## Primary Sources

## How Sources Are Used

1. **Domain research** is conducted against extracted sources.
"""


@dataclass(frozen=True)
class KnowledgeTree:
    """A temp registry tree plus the paths object the seam code takes."""

    root: Path
    paths: zotero_lib.RegistryPaths

    @property
    def index(self) -> Path:
        return self.paths.index

    @property
    def manifest(self) -> Path:
        return self.paths.manifest

    @property
    def sources(self) -> Path:
        return self.paths.sources

    @property
    def raw(self) -> Path:
        return self.paths.raw


def _build_tree(root: Path, baseline: dict) -> KnowledgeTree:
    paths = zotero_lib.RegistryPaths.under(root)
    paths.sources.mkdir(parents=True)
    paths.raw.mkdir(parents=True)
    paths.index.write_text(MINIMAL_INDEX)
    paths.manifest.write_text("")
    paths.baseline.write_text(json.dumps(baseline))
    return KnowledgeTree(root=root, paths=paths)


# Every RegistryPaths field, and the module constant `default_paths()` builds it
# from. All seven must be redirected or the suite is not hermetic: any code path
# that reaches `default_paths()` — the Zotero callers do — would otherwise stage
# into the real repository's `knowledge/.staging` and take the real registry lock.
_PATH_CONSTANTS = {
    "sources": "SOURCES_DIR",
    "index": "SOURCE_INDEX_PATH",
    "manifest": "MANIFEST_PATH",
    "raw": "RAW_DIR",
    "staging": "STAGING_DIR",
    "lock": "LOCK_PATH",
    "baseline": "BASELINE_PATH",
}
assert set(_PATH_CONSTANTS) == set(f.name for f in fields(zotero_lib.RegistryPaths))


def _point_legacy_constants_at(tree: KnowledgeTree, monkeypatch) -> None:
    """Redirect every registry path constant at the temp tree.

    This patches constants rather than only injecting `RegistryPaths` for two
    reasons: the pre-seam writer reads the constants directly, and
    `default_paths()` builds from them — so redirecting them is what keeps an
    un-injected call site inside the temp tree too. `zotero_ingest` imported the
    constants by value, so both modules are patched.
    """
    for module in (zotero_lib, zotero_ingest):
        for field, constant in _PATH_CONSTANTS.items():
            monkeypatch.setattr(module, constant, getattr(tree.paths, field),
                                raising=False)


EMPTY_BASELINE = {
    "generated": "2026-08-25",
    "note": "test tree; no pre-seam drift",
    "orphan_source_dirs": [],
    "loose_files": [],
}


@pytest.fixture
def knowledge_tree(tmp_path, monkeypatch):
    tree = _build_tree(tmp_path / "knowledge", EMPTY_BASELINE)
    _point_legacy_constants_at(tree, monkeypatch)
    return tree


@pytest.fixture
def knowledge_tree_factory(tmp_path, monkeypatch):
    """Build a tree with a caller-supplied legacy baseline."""

    def _make(baseline: dict, name: str = "knowledge") -> KnowledgeTree:
        tree = _build_tree(tmp_path / name, baseline)
        _point_legacy_constants_at(tree, monkeypatch)
        return tree

    return _make


# --- offline capture fixtures (design D11) -----------------------------------
#
# `file://` is rejected by `agentic-mbse extract`, so the fixture URL has to be
# real HTTP. A thread-local server over `fixtures/web/` lets the seam run the
# actual extract subprocess without touching the network.

FIXTURE_WEB = Path(__file__).parent / "fixtures" / "web"

# Declared charset per fixture. The header is what the fetcher decodes by, so a
# page has to be served as iso-8859-1 to exercise the re-encoding asymmetry.
FIXTURE_CHARSET = {"latin1.html": "iso-8859-1"}


class _FixtureHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        charset = FIXTURE_CHARSET.get(Path(path).name)
        if charset:
            return f"text/html; charset={charset}"
        return super().guess_type(path)

    def log_message(self, *args):
        pass


@dataclass(frozen=True)
class LocalSite:
    port: int

    def url(self, name: str) -> str:
        return f"http://127.0.0.1:{self.port}/{name}"

    def fetched_bytes(self, name: str) -> bytes:
        with urllib.request.urlopen(self.url(name)) as response:
            return response.read()


@pytest.fixture(scope="session")
def local_site():
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(_FixtureHandler, directory=str(FIXTURE_WEB)),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield LocalSite(port=server.server_address[1])
    finally:
        server.shutdown()
        server.server_close()


@pytest.fixture(scope="session")
def generated_pdf(tmp_path_factory) -> Path:
    """A small text PDF, drawn with matplotlib so the suite adds no dependency."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lines = [
        "Widget Coil Note (synthetic fixture)",
        "",
        "The widget winding pack measures 1000 mm by 400 mm.",
        "The invented conductor carries 100.0 kA across 150 turns.",
        "This document exists only to exercise the local-PDF capture path.",
    ]
    figure = plt.figure(figsize=(8.5, 11))
    for i, line in enumerate(lines):
        figure.text(0.1, 0.9 - 0.04 * i, line, fontsize=12)
    path = tmp_path_factory.mktemp("pdf") / "widget_coil_note.pdf"
    figure.savefig(path)
    plt.close(figure)
    return path
