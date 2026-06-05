#!/usr/bin/env python3
"""Tests for lib/canonical_accounts.py — Phase 1 (Item 8).

The canonical-account schema is the first de-risk gate: it must author cleanly,
surface the right accounts per archetype, fail loudly on library drift, and
render to a prompt-appropriate block. Stencil from
.project/active/concept-rework-prompt-templates/plan.md, Phase 1.
"""

from unittest.mock import patch

import pytest

from lib.canonical_accounts import (
    ALL_CONFINEMENT_CONCEPT_ENUMS,
    FIT_GRADE_OVERRIDE_BAND,
    AccountRow,
    _PER_ARCHETYPE_ACCOUNTS,
    fit_grade_band,
    get_canonical_accounts,
    render_account_block,
    validate_against_library,
)

# ---------------------------------------------------------------------------
# Plan stencil
# ---------------------------------------------------------------------------


def test_get_canonical_accounts_returns_rows_for_each_enum():
    for enum in ALL_CONFINEMENT_CONCEPT_ENUMS:
        rows = get_canonical_accounts(enum)
        assert len(rows) > 0
        for row in rows:
            assert row.account.startswith(("C220", "CAS"))
            assert row.one_line_description


def test_validate_against_library_passes_for_authored_constant():
    missing = validate_against_library()
    assert missing == [], f"unknown library accounts: {missing}"


def test_validate_against_library_catches_typo():
    with patch.dict(
        _PER_ARCHETYPE_ACCOUNTS,
        {"TOKAMAK": [AccountRow("C999999", "fake", None)]},
    ):
        assert "C999999" in validate_against_library()


def test_render_account_block_for_tokamak_includes_C220103():
    block = render_account_block(get_canonical_accounts("TOKAMAK"))
    assert "C220103" in block
    assert "coil" in block.lower()


# ---------------------------------------------------------------------------
# Per-archetype membership smoke tests (control-flow mirror of cas22.py)
# ---------------------------------------------------------------------------


def _codes(enum: str) -> set[str]:
    return {r.account for r in get_canonical_accounts(enum)}


def test_unknown_enum_raises_no_silent_fallback():
    with pytest.raises(KeyError):
        get_canonical_accounts("NOT_A_REAL_ENUM")


def test_laser_ife_has_no_confinement_magnets():
    # _COIL_DEFAULTS[LASER_IFE] is None -> C220103 forced to 0.0 in the library.
    codes = _codes("LASER_IFE")
    assert "C220103" not in codes
    # ...but it DOES carry the driver (C220104) and a target factory (C220108).
    assert "C220104" in codes
    assert "C220108" in codes


def test_pulsed_frc_has_no_divertor_or_target_factory():
    # The explicit library zero branch: no manufactured target, no divertor.
    codes = _codes("PULSED_FRC")
    assert "C220108" not in codes
    # FRC keeps its coils and (optionally) a direct energy converter.
    assert "C220103" in codes
    assert "C220109" in codes


def test_tokamak_is_steady_state_with_divertor():
    codes = _codes("TOKAMAK")
    assert {"C220103", "C220108"} <= codes
    # Conventional thermal tokamak: no direct energy converter candidate.
    assert "C220109" not in codes


def test_every_archetype_has_balance_of_plant_and_operations():
    for enum in ALL_CONFINEMENT_CONCEPT_ENUMS:
        codes = _codes(enum)
        assert {"CAS21", "CAS27", "CAS70", "CAS80"} <= codes, enum


def test_all_enums_match_library():
    # The authored enum tuple must equal the library's ConfinementConcept set —
    # a library add/rename should fail here loudly, not drift silently.
    from costingfe.types import ConfinementConcept

    assert set(ALL_CONFINEMENT_CONCEPT_ENUMS) == {c.name for c in ConfinementConcept}


# ---------------------------------------------------------------------------
# Fit-grade band (FR-8) — single source of truth shared with Item 7 (Phase 3)
# ---------------------------------------------------------------------------


def test_fit_grade_band_constant_single_source():
    assert FIT_GRADE_OVERRIDE_BAND["High"] == (0, 4)
    assert FIT_GRADE_OVERRIDE_BAND["Med"] == (3, 8)
    assert FIT_GRADE_OVERRIDE_BAND["Low"] == (6, 12)


def test_fit_grade_band_lookup_is_case_and_synonym_tolerant():
    assert fit_grade_band("High") == (0, 4)
    assert fit_grade_band("med") == (3, 8)
    assert fit_grade_band("Medium") == (3, 8)
    assert fit_grade_band("None") is None
    assert fit_grade_band("") is None


def test_render_account_block_is_concise_and_readable():
    # One header (2 lines) + one row per account; ARC/tokamak should stay well
    # under the ~20-row prompt budget the design calls for.
    block = render_account_block(get_canonical_accounts("TOKAMAK"))
    body_rows = [ln for ln in block.splitlines() if ln.startswith("| `")]
    assert len(body_rows) == len(get_canonical_accounts("TOKAMAK"))
    assert len(body_rows) <= 20
    # No authored newline leaks into a table cell.
    assert "\n|" not in block.replace("\n| ", "")
