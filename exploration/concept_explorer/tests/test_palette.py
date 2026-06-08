"""Tests for the ontology palette + facet/filter model (Theme A / A2, Phase 4).

Static-text guards (no browser):
  - The single color authority is CSS :root — ontology_palette.js holds NO hex
    literals (it reads tokens via getComputedStyle).
  - The former 5× FAMILY_COLORS duplications are gone; each consumer re-sources
    from ontologyPalette.family; no family hex remains in the family-color files.
  - Family tokens are unchanged (zero visual change); dimension tokens match the
    PNG generator (traceability, FR-A2.2).
  - Templates load ontology_palette.js before its consumers.

Runtime behavior (ontologyPalette.family.MFE, facetModel, filterState) and the
zero-visual-change check are verified live via browser-inspect.
"""

from __future__ import annotations

import re

import pytest

from exploration.concept_explorer.server import BASE_DIR

_JS_DIR = BASE_DIR / "static" / "js"
_CSS = (BASE_DIR / "static" / "css" / "explorer.css").read_text()
_TEMPLATES_DIR = BASE_DIR / "templates"

# Files that previously hard-coded FAMILY_COLORS and now re-source it.
_FAMILY_CONSUMERS = [
    "constellation.js",
    "neighborhood_graph.js",
    "view_capex.js",
    "view_summary.js",
    "view_sensitivity.js",
]
_TEMPLATES = ["index.html.j2", "concept.html.j2", "compare.html.j2", "taxonomy.html.j2"]

# The distinctive family-identity hexes. The 4th family color, grey #6b7280
# (NONSTANDARD), is deliberately excluded here — it's a generic UI grey also
# used as the CAS-account / fallback grey in other color systems, so it can't be
# guarded per-file by hex alone. The literal-dict and re-source checks cover it.
_FAMILY_HEXES = ["#3b82f6", "#a855f7", "#f59e0b"]
_HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")


# ---------------------------------------------------------------------------
# Single authority — CSS :root holds the colors; the JS map holds none
# ---------------------------------------------------------------------------


def test_palette_module_has_no_hex_literals():
    """ontology_palette.js reads every color from CSS :root — so the JS source
    contains no color hex at all (the CSS is the single authority)."""
    text = (_JS_DIR / "ontology_palette.js").read_text()
    hexes = _HEX_RE.findall(text)
    assert not hexes, f"ontology_palette.js should hold no hex literals; found {hexes}"


def test_palette_module_exports_three_globals():
    text = (_JS_DIR / "ontology_palette.js").read_text()
    assert "window.ontologyPalette" in text
    assert "window.facetModel" in text
    assert "window.filterState" in text


# ---------------------------------------------------------------------------
# Family-color de-duplication
# ---------------------------------------------------------------------------


def test_no_family_colors_literal_dict_anywhere():
    for path in _JS_DIR.glob("*.js"):
        assert "FAMILY_COLORS = {" not in path.read_text(), (
            f"{path.name} still defines a literal FAMILY_COLORS dict"
        )


@pytest.mark.parametrize("fname", _FAMILY_CONSUMERS)
def test_consumer_resources_family_from_authority(fname: str):
    text = (_JS_DIR / fname).read_text()
    assert "ontologyPalette.family" in text, f"{fname} does not re-source family colors"
    lowered = text.lower()
    for hexv in _FAMILY_HEXES:
        assert hexv not in lowered, f"{fname} still hard-codes family hex {hexv}"


# ---------------------------------------------------------------------------
# CSS tokens — unchanged family + PNG-traceable dimensions
# ---------------------------------------------------------------------------


def test_family_tokens_unchanged_zero_visual_change():
    for name, hexv in [
        ("--color-badge-mfe", "#3b82f6"),
        ("--color-badge-ife", "#a855f7"),
        ("--color-badge-mif", "#f59e0b"),
        ("--color-badge-nonstandard", "#6b7280"),
    ]:
        assert f"{name}: {hexv};" in _CSS, f"family token {name} changed (must stay {hexv})"


def test_dimension_tokens_trace_to_png_generator():
    """Representative dimension tokens match generate_ontology_chart.py PALETTES
    (the source that produced concept_ontology_v3.png) — FR-A2.2 traceability."""
    for name, hexv in [
        ("--onto-fuel-dt", "#2f3b54"),
        ("--onto-fuel-pb11", "#e0843a"),
        ("--onto-magnet-hts-wound", "#2c3e8f"),
        ("--onto-driver-dpssl-laser", "#e8a4b9"),
        ("--onto-capture-thermal-steam", "#2f6478"),
        ("--onto-opmode-steady", "#3a8a4a"),
        ("--onto-reprate-khz", "#c54a4a"),
        ("--onto-na", "#bdbdbd"),
    ]:
        assert f"{name}: {hexv};" in _CSS, f"dimension token {name} != generator value {hexv}"


# ---------------------------------------------------------------------------
# Template load order
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("template", _TEMPLATES)
def test_template_loads_palette_before_consumers(template: str):
    text = (_TEMPLATES_DIR / template).read_text()
    pal = "/static/js/ontology_palette.js"
    assert pal in text, f"{template} does not load {pal}"
    pal_pos = text.index(pal)
    for consumer in _FAMILY_CONSUMERS:
        ref = f"/static/js/{consumer}"
        if ref in text:
            assert text.index(ref) > pal_pos, (
                f"{template}: {consumer} loads before ontology_palette.js"
            )
