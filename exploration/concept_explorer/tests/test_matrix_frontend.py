"""Grep-guards for the ontology matrix front-end (B1, Phase 2).

Static-text guards (no browser), mirroring test_identity_frontend.py. They
enforce the matrix's structural invariants: it consumes Theme A's shared
authorities rather than re-deriving identity/color/facet/caveat/filter logic
(FR-B1.11), authors no color literals of its own (the single-color-authority
invariant), and carries no economics (FR-B1.9). Visual correctness (chips,
bands, honest cells) is verified separately via browser-inspect.
"""

from __future__ import annotations

import re
from pathlib import Path

JS_DIR = Path(__file__).parent.parent / "static" / "js"


def test_matrix_imports_theme_a_authorities():
    """The matrix renders through the five Theme A authorities (FR-B1.11)."""
    src = (JS_DIR / "matrix_page.js").read_text() + (JS_DIR / "matrix_data.js").read_text()
    for sym in ("conceptLabel(", "caveatMarker(", "ontologyPalette", "facetModel", "filterState"):
        assert sym in src, f"matrix front-end does not consume Theme A authority: {sym}"


def test_matrix_has_no_color_literals_or_lcoe_column():
    """No color hex / `--onto-` token authored in the matrix; no LCOE (FR-B1.9)."""
    src = (JS_DIR / "matrix_data.js").read_text() + (JS_DIR / "matrix_page.js").read_text()
    assert "--onto-" not in src, "matrix authors a CSS color token (must read via ontologyPalette)"
    assert not re.search(r"#[0-9a-fA-F]{6}", src), "matrix authors a color hex literal"
    assert "lcoe" not in src.lower(), "FR-B1.9: no LCOE/cost column, sort, or color in the matrix"


def test_matrix_uses_filterstate_and_groups():
    """Filtering goes through the shared filterState; an explicit unspecified band
    exists for dimension re-grouping (FR-B1.5, FR-B1.6)."""
    src = (JS_DIR / "matrix_page.js").read_text() + (JS_DIR / "matrix_data.js").read_text()
    assert "filterState.toggle" in src and "filterState.matches" in src
    assert "unspecified" in src.lower()  # explicit "— unspecified" band (FR-B1.5)


def test_matrix_sort_and_caveat_hover():
    """Sort state (key + direction) exists; hover/caveat goes through caveatMarker
    (FR-B1.7, FR-B1.8)."""
    src = (JS_DIR / "matrix_page.js").read_text() + (JS_DIR / "matrix_data.js").read_text()
    assert "sortKey" in src and "sortDir" in src
    assert "caveatMarker(" in src  # hover/caveat through the one authority
