"""Fixtures for fusion-tea's research tests: the Zotero callers and the hold-out wiring.

The registry itself is the installed `agentic_mbse.research` package and is
tested there. Its `default_paths()` is relative to the current directory, so
`knowledge_tree` builds a throwaway project and makes it the current directory
(`monkeypatch.chdir`). Code that reaches the default paths, as the Zotero
callers do, then lands in the temp tree. A session check fails the run if any
test wrote to the repository's own registry anyway.
"""

from dataclasses import dataclass
from pathlib import Path

import pytest
from agentic_mbse.research import RegistryPaths

REPO_ROOT = Path(__file__).resolve().parents[2]

MINIMAL_INDEX = """# Source Index

Source registry for the fusion TEA investigation.

## Primary Sources

## How Sources Are Used

1. **Domain research** is conducted against extracted sources.
"""


@dataclass(frozen=True)
class KnowledgeTree:
    """A temp project's registry. Its project root is the current directory during the test."""

    paths: RegistryPaths

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


@pytest.fixture
def knowledge_tree(tmp_path, monkeypatch) -> KnowledgeTree:
    """An empty registry in a temp project, which becomes the current directory."""
    paths = RegistryPaths(knowledge_dir=tmp_path / "knowledge")
    paths.sources.mkdir(parents=True)
    paths.raw.mkdir(parents=True)
    paths.index.write_text(MINIMAL_INDEX)
    paths.manifest.write_text("")
    monkeypatch.chdir(tmp_path)
    return KnowledgeTree(paths=paths)


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


# --- the repository's own registry stays untouched ----------------------------------

_REAL_KNOWLEDGE = REPO_ROOT / "knowledge"
_REGISTRY_FILES = ("MANIFEST.jsonl", "SOURCE_INDEX.md", "RETIRED.jsonl", ".registry.lock")
_REGISTRY_DIRS = ("sources", "raw", ".staging")


def _registry_state() -> dict[str, object]:
    """What a stray write to the repository's registry would change: mtimes and listings."""
    state: dict[str, object] = {}
    for name in _REGISTRY_FILES:
        path = _REAL_KNOWLEDGE / name
        state[name] = path.stat().st_mtime_ns if path.exists() else None
    for name in _REGISTRY_DIRS:
        path = _REAL_KNOWLEDGE / name
        state[name] = sorted(entry.name for entry in path.iterdir()) if path.is_dir() else None
    return state


@pytest.fixture(scope="session", autouse=True)
def repository_registry_untouched():
    """Fail the session if any test wrote to, or took the lock of, the repository's `knowledge/`."""
    before = _registry_state()
    yield
    assert _registry_state() == before, "a research test wrote to the repository's own knowledge/"
