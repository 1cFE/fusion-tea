"""Fixtures for the research seam suite.

`knowledge_tree` builds a throwaway registry tree and points both the legacy
Zotero writer (which reads module-level path constants) and the new seam code
(which takes an injected paths object) at it. No `chdir`.
"""

import json
from dataclasses import dataclass
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


def _point_legacy_constants_at(tree: KnowledgeTree, monkeypatch) -> None:
    """The pre-seam writer reads module constants; redirect them at the temp tree.

    `zotero_ingest` imported the constants by value, so both modules are patched.
    """
    for module in (zotero_lib, zotero_ingest):
        monkeypatch.setattr(module, "SOURCES_DIR", tree.paths.sources, raising=False)
        monkeypatch.setattr(module, "SOURCE_INDEX_PATH", tree.paths.index, raising=False)
        monkeypatch.setattr(module, "MANIFEST_PATH", tree.paths.manifest, raising=False)
        monkeypatch.setattr(module, "RAW_DIR", tree.paths.raw, raising=False)


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
