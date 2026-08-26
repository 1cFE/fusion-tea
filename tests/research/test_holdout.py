"""Phase 5 — the two holdout checkpoints, and what a hit leaves behind (spec R-D1..R-D4).

Every fixture here trips a rule with a bare bibliographic token. None carries
held-out design or cost content, which is what R-D4 bars.
"""

import pytest

import source_registry
from source_registry import LocalPdfSource, SourceMetadata, UrlSource

METADATA = SourceMetadata(
    title="Marker Page",
    use_for="Trips the content scan; exercises the holdout checkpoint.",
    validation="Not applicable — this is a refusal fixture.",
    caveat="A test fixture.",
)

SEALED_STEM = "08-FST-Najmabadi"


def _nothing_written(tree) -> bool:
    return (
        not list(tree.paths.sources.iterdir())
        and not list(tree.paths.staging.iterdir())
        and tree.manifest.read_text() == ""
        and "###" not in tree.index.read_text()
    )


def test_content_hit_writes_nothing_and_names_the_rule(local_site, knowledge_tree):
    result = source_registry.register(
        UrlSource(url=local_site.url("marker.html")), METADATA, paths=knowledge_tree.paths
    )
    assert result.outcome == "holdout_hit"
    assert result.rule_id == f"term:{SEALED_STEM.lower()}"
    assert result.offsets
    assert _nothing_written(knowledge_tree)


def test_barred_url_is_refused_before_any_fetch(knowledge_tree):
    result = source_registry.register(
        UrlSource(url=f"https://example.org/mirror/{SEALED_STEM}.pdf"),
        METADATA, paths=knowledge_tree.paths,
    )
    assert result.outcome == "holdout_hit"
    assert result.rule_id == f"term:{SEALED_STEM.lower()}"
    assert _nothing_written(knowledge_tree)


def test_barred_title_is_refused_before_any_fetch(local_site, knowledge_tree):
    from dataclasses import replace

    result = source_registry.register(
        UrlSource(url=local_site.url("utf8.html")),
        replace(METADATA, title=f"Notes on {SEALED_STEM}"),
        paths=knowledge_tree.paths,
    )
    assert result.outcome == "holdout_hit"
    assert _nothing_written(knowledge_tree)


def test_barred_local_pdf_input_path_is_refused(knowledge_tree):
    result = source_registry.register(
        LocalPdfSource(path=source_registry.Path("knowledge/holdout/aries-cs/08-FST-Ku.pdf")),
        METADATA, paths=knowledge_tree.paths,
    )
    assert result.outcome == "holdout_hit"
    assert result.rule_id.startswith("path:") or result.rule_id.startswith("term:")
    assert _nothing_written(knowledge_tree)


def test_no_flag_can_waive_a_holdout_hit(local_site, knowledge_tree):
    """D12: the CLI exposes no waiver, so a hit has no in-code way past it."""
    parser = source_registry._build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["register", "--url", "x", "--title", "t", "--use-for", "u",
                           "--validation", "v", "--caveat", "c", "--holdout-ack"])
