"""Audit: model_type ⟺ resolvable model_setup.py (INV-2 / B2).

The explorer no longer stores a path to each concept's ``model_setup.py``;
the compute endpoint derives it from the concept_id by scanning the
``concept_analysis/analyses`` tree for a ``{concept_id}-*`` directory (the same
mechanism the findings endpoint uses for ``analysis.md``). That derivation is
only correct if the data's ``model_type`` field is a faithful proxy for "has a
runnable model_setup.py":

    model_type == COSTINGFE  ⟺  a resolvable {id}-*/model_setup.py exists.

This test asserts that equivalence across the real, server-loaded concept set.
It guards the design's central bet (B2) and would have caught a concept whose
model_type and on-disk reality disagree before the schema field was removed.

See:
- .project/active/explorer-model-setup-path-normalization/design.md (INV-2, B2)
- findings.py:find_concept_dir (the production resolver this mirrors)
"""

from __future__ import annotations

from pathlib import Path

from exploration.concept_explorer.findings import find_concept_dir
from exploration.concept_explorer.models import (
    ConceptData,
    ModelType,
    load_omit_list,
)

# tests/ -> concept_explorer/ -> exploration/
_CONCEPT_EXPLORER = Path(__file__).resolve().parents[1]
_DATA_DIR = _CONCEPT_EXPLORER / "data"
_ANALYSES_ROOT = _CONCEPT_EXPLORER.parent / "concept_analysis" / "analyses"


def _served_concept_files() -> list[Path]:
    """The concept JSONs the server would actually load (digit-stem, not omitted)."""
    omit = load_omit_list()
    return [f for f in sorted(_DATA_DIR.glob("[0-9]*.json")) if f.stem not in omit]


def test_costingfe_concepts_resolve_to_a_model_setup() -> None:
    """Every COSTINGFE concept must have a resolvable {id}-*/model_setup.py."""
    assert _ANALYSES_ROOT.is_dir(), f"analyses tree missing at {_ANALYSES_ROOT}"

    unresolved: list[str] = []
    for path in _served_concept_files():
        concept = ConceptData.model_validate_json(path.read_text(encoding="utf-8"))
        if concept.model_type != ModelType.COSTINGFE:
            continue
        concept_dir = find_concept_dir(concept.concept_id, _ANALYSES_ROOT)
        if concept_dir is None or not (concept_dir / "model_setup.py").exists():
            unresolved.append(concept.concept_id)

    assert not unresolved, (
        "COSTINGFE concepts with no resolvable model_setup.py "
        f"under {_ANALYSES_ROOT}: {unresolved}"
    )
