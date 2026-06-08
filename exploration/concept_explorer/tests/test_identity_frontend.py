"""Grep-guard for the front-end identity spine (Theme A / A1, Phase 2).

These are static-text guards (no browser): they assert that every naming
surface routes through the single `conceptLabel()` helper and that no surface
renders a raw payload `.name` directly — the invariant that makes the
four-strings divergence structurally unable to recur. Visual correctness
(#code + Name (Fuel) rendering) is verified separately via browser-inspect.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_JS_DIR = Path(__file__).parent.parent / "static" / "js"
_TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

# Naming surfaces wired through conceptLabel() (spec.md:67 enumeration + the two
# surfaces the audit flagged: the selection tray and the neighborhood heading).
_TOUCHED = [
    "index_page.js",
    "concept_page.js",
    "sticky_headline.js",
    "comparison.js",
    "constellation.js",
    "taxonomy_card.js",
    "parameter_card.js",
    "selection_tray.js",
    "taxonomy.js",
]

# Files the raw-`.name` glob guard skips, each for a documented reason:
#   - concept_label.js: the helper itself defines/reads `.name`.
#   - Out-of-scope naming surfaces (spec.md:67 deliberately keeps the #code on
#     the identity chrome, NOT inside chart axes or cytoscape graph nodes): the
#     compare integrated chart views + the neighborhood relationship graph. Their
#     canonical name still renders (server overlay); only the code chip is absent.
#   - cas_breakdown.js: renders CAS-account tile names (`t.name`), not concepts.
_RAW_NAME_EXCLUDED = {
    "concept_label.js",
    "view_capex.js",
    "view_summary.js",
    "view_categorical.js",
    "view_sensitivity.js",
    "neighborhood_graph.js",
    "cas_breakdown.js",
}

# Templates that load a naming surface, each must pull in concept_label.js.
_TEMPLATES = ["index.html.j2", "concept.html.j2", "compare.html.j2"]

# A `<recv>.name` read is legitimate when <recv> is a conceptLabel() *result*.
# Result objects are named with the convention `lbl` / `*Lbl` / `*Label`.
_LABEL_RECEIVER = re.compile(r"(?:lbl|Lbl|Label)$")
_NAME_READ = re.compile(r"(\w+)\.name\b")


def test_helper_module_exists_and_exports_global():
    text = (_JS_DIR / "concept_label.js").read_text()
    assert "window.conceptLabel" in text


@pytest.mark.parametrize("fname", _TOUCHED)
def test_surface_uses_conceptlabel(fname: str):
    """Every touched surface routes naming through the one helper."""
    text = (_JS_DIR / fname).read_text()
    assert "conceptLabel(" in text, f"{fname} does not call conceptLabel()"


def test_no_raw_name_label_render():
    """No in-scope surface renders a raw payload `.name` directly.

    Globs EVERY JS file (not a fixed allowlist — that gave false confidence and
    couldn't catch a new surface), skipping only `_RAW_NAME_EXCLUDED` (documented
    above). A `<recv>.name` is permitted when it is (a) read off a conceptLabel()
    result (`lbl`/`*Lbl`/`*Label`), (b) an object-literal data field
    `name: <recv>.name`, or (c) fed into a `conceptLabel({...})` call. Anything
    else is a raw render that re-opens the divergence this spine fixes.
    """
    offenders: list[str] = []
    for path in sorted(_JS_DIR.glob("*.js")):
        if path.name in _RAW_NAME_EXCLUDED:
            continue
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            for m in _NAME_READ.finditer(line):
                recv = m.group(1)
                if _LABEL_RECEIVER.search(recv):
                    continue  # reading off a conceptLabel() result — correct
                if re.search(r"name:\s*" + re.escape(recv) + r"\.name", line):
                    continue  # object-literal data field, not a label render
                ctx = "\n".join(lines[max(0, i - 3) : i + 1])
                if "conceptLabel(" in ctx:
                    continue  # feeding the helper, not rendering raw
                offenders.append(f"{path.name}:{i + 1}: {line.strip()}")
    assert not offenders, "raw .name renders found:\n" + "\n".join(offenders)


@pytest.mark.parametrize("template", _TEMPLATES)
def test_template_loads_helper_before_surfaces(template: str):
    """concept_label.js must be loaded before any surface script that uses it."""
    text = (_TEMPLATES_DIR / template).read_text()
    helper = "/static/js/concept_label.js"
    assert helper in text, f"{template} does not load {helper}"
    helper_pos = text.index(helper)
    # Every other surface <script> that names concepts must come after the helper.
    for surface in _TOUCHED:
        ref = f"/static/js/{surface}"
        if ref in text:
            assert text.index(ref) > helper_pos, (
                f"{template}: {surface} loads before concept_label.js"
            )
