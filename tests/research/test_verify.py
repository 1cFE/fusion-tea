"""Phase 6 — `verify` reports registry drift and never repairs it (design D14, SC4 support)."""

import json

import source_registry
from source_registry import SourceMetadata, UrlSource

METADATA = SourceMetadata(
    title="Widget Coil Note",
    use_for="Synthetic winding-pack geometry; exercises verify.",
    validation="Compare against the fixture page itself.",
    caveat="A test fixture.",
)


def _snapshot(tree) -> tuple:
    return (
        tree.index.read_bytes(),
        tree.manifest.read_bytes(),
        sorted(p.name for p in tree.paths.sources.iterdir()),
    )


def _append_row(tree, row: dict) -> None:
    with open(tree.manifest, "a") as handle:
        handle.write(json.dumps(row) + "\n")


def _make_orphan_dir(tree, name="orphan_source") -> None:
    (tree.paths.sources / name).mkdir()
    (tree.paths.sources / name / "output.md").write_text("orphan\n")


def _make_row_without_block(tree, slug="rowless") -> None:
    (tree.paths.sources / slug).mkdir()
    _append_row(tree, {"source_id": "a" * 64, "source_kind": "url", "slug": slug,
                       "title": "Rowless"})


def _make_unresolvable_row(tree, slug="vanished") -> None:
    _append_row(tree, {"source_id": "b" * 64, "source_kind": "url", "slug": slug,
                       "title": "Vanished"})


def test_each_drift_shape_is_reported(knowledge_tree):
    _make_orphan_dir(knowledge_tree)
    _make_row_without_block(knowledge_tree)
    _make_unresolvable_row(knowledge_tree)
    (knowledge_tree.paths.sources / "LOOSE.md").write_text("not a source dir\n")

    report = source_registry.verify(knowledge_tree.paths)
    assert {f.kind for f in report.findings} == {
        "orphan_source_dir", "row_without_block", "unresolvable_path", "loose_file",
    }
    assert all(f.klass == "fault" for f in report.findings)
    assert report.has_faults


def test_a_registered_source_produces_no_finding(local_site, knowledge_tree):
    result = source_registry.register(
        UrlSource(url=local_site.url("utf8.html")), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "registered"
    report = source_registry.verify(knowledge_tree.paths)
    assert report.findings == [] and not report.has_faults


def test_baseline_entries_are_legacy_not_faults(knowledge_tree_factory):
    tree = knowledge_tree_factory({
        "generated": "2026-08-25",
        "note": "pre-seam drift",
        "orphan_source_dirs": ["knowledge/sources/orphan_source"],
        "loose_files": ["knowledge/sources/LOOSE.md"],
    })
    _make_orphan_dir(tree)
    (tree.paths.sources / "LOOSE.md").write_text("not a source dir\n")
    _make_row_without_block(tree)

    report = source_registry.verify(tree.paths)
    by_kind = {f.kind: f for f in report.findings}
    assert by_kind["orphan_source_dir"].klass == "legacy"
    assert by_kind["loose_file"].klass == "legacy"
    assert by_kind["row_without_block"].klass == "fault"
    assert report.has_faults


def test_verify_writes_nothing(knowledge_tree):
    _make_orphan_dir(knowledge_tree)
    _make_unresolvable_row(knowledge_tree)
    before = _snapshot(knowledge_tree)
    source_registry.verify(knowledge_tree.paths)
    assert _snapshot(knowledge_tree) == before


def test_a_clean_registry_has_no_faults(knowledge_tree):
    report = source_registry.verify(knowledge_tree.paths)
    assert report.findings == [] and not report.has_faults
