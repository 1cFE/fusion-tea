"""Phase 5 — a failure at any commit rung leaves the repository byte-identical (SC4).

Failures are injected into the real rung functions, so the code path that runs is
the production one; only the rung's own body is replaced.
"""

import pytest

import source_registry
from source_registry import RegistrationError, SourceMetadata, UrlSource

METADATA = SourceMetadata(
    title="Widget Coil Note",
    use_for="Synthetic winding-pack geometry; exercises the rollback ladder.",
    validation="Compare against the fixture page itself.",
    caveat="A test fixture.",
)

RUNGS = {
    "before_rename": "_rename_into_sources",
    "after_rename": "_append_manifest_row",
    "after_manifest_append": "_insert_index_block",
}


def _snapshot(tree) -> tuple:
    return (
        tree.index.read_bytes(),
        tree.manifest.read_bytes(),
        sorted(p.name for p in tree.paths.sources.iterdir()),
        sorted(p.name for p in tree.paths.raw.iterdir()),
    )


@pytest.mark.parametrize("rung", sorted(RUNGS))
def test_failure_at_each_rung_leaves_nothing(rung, knowledge_tree, local_site, monkeypatch):
    before = _snapshot(knowledge_tree)

    def boom(*args, **kwargs):
        raise OSError(f"injected failure at {rung}")

    monkeypatch.setattr(source_registry, RUNGS[rung], boom)

    with pytest.raises(RegistrationError, match=rung):
        source_registry.register(
            UrlSource(url=local_site.url("utf8.html")), METADATA, paths=knowledge_tree.paths
        )

    assert _snapshot(knowledge_tree) == before
    assert not list(knowledge_tree.paths.staging.iterdir())


@pytest.mark.parametrize("rung", sorted(RUNGS))
def test_rollback_preserves_an_earlier_registration(rung, knowledge_tree, local_site, monkeypatch):
    """The ladder undoes its own rungs and nothing else."""
    kept = source_registry.register(
        UrlSource(url=local_site.url("utf8.html")), METADATA, paths=knowledge_tree.paths
    )
    assert kept.outcome == "registered"
    before = _snapshot(knowledge_tree)

    def boom(*args, **kwargs):
        raise OSError(f"injected failure at {rung}")

    monkeypatch.setattr(source_registry, RUNGS[rung], boom)

    from dataclasses import replace

    with pytest.raises(RegistrationError):
        source_registry.register(
            UrlSource(url=local_site.url("latin1.html")),
            replace(METADATA, title="Cable Note"),
            paths=knowledge_tree.paths,
        )

    assert _snapshot(knowledge_tree) == before
    assert (kept.path / "output.md").is_file()
