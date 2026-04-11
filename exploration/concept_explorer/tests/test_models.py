"""Tests for exploration/concept_explorer/models.py.

Each AC is documented as a comment above the test that satisfies it.
The tests use minimal stub data — the goal is to verify the Pydantic contract,
not to test 1costingfe business logic.
"""

import json
import warnings
from typing import Any

import pytest
from pydantic import ValidationError

from exploration.concept_explorer.models import (
    CASAccount,
    ConceptData,
    ConceptManifest,
    ConceptManifestEntry,
    ConceptStatus,
    Confidence,
    ConfinementFamily,
    CostModelData,
    NarrativeData,
    ParameterCategory,
    ParameterMetadata,
    SensitivityAnalysis,
    SensitivityEntry,
    SourcePaths,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_forward_result_dict(
    *,
    cas_override: dict[str, Any] | None = None,
    power_override: dict[str, Any] | None = None,
    cas22_override: dict[str, Any] | None = None,
    overridden: list[str] | None = None,
) -> dict[str, Any]:
    """Build a minimal dict that mimics dataclasses.asdict(ForwardResult)."""
    costs = {
        "cas10": 10.0,
        "cas21": 21.0,
        "cas22": 22.0,
        "cas23": 23.0,
        "cas24": 24.0,
        "cas25": 25.0,
        "cas26": 26.0,
        "cas27": 27.0,
        "cas28": 28.0,
        "cas29": 29.0,
        "cas30": 30.0,
        "cas40": 40.0,
        "cas50": 50.0,
        "cas60": 60.0,
        "cas70": 70.0,
        "cas80": 80.0,
        "cas90": 90.0,
        "lcoe": 120.5,
        "overnight_cost": 8500.0,
        "total_capital": 4200.0,
    }
    if cas_override:
        costs.update(cas_override)

    power = {
        "p_net": 1000.0,
        "q_eng": 3.5,
        "capacity_factor": 0.85,
        "p_fus": 2500.0,
        "rec_frac": 0.30,
    }
    if power_override:
        power.update(power_override)

    cas22 = {"C220101": 50.0, "C220103": 0.0, "C220104": 120.0}
    if cas22_override:
        cas22.update(cas22_override)

    return {
        "costs": costs,
        "power_table": power,
        "cas22_detail": cas22,
        "overridden": overridden or [],
        "params": {"net_electric_mw": 1000.0, "availability": 0.85},
    }


def _make_cost_model(sensitivities: SensitivityAnalysis | None = None) -> CostModelData:
    return CostModelData.from_forward_result(
        _make_forward_result_dict(),
        sensitivities=sensitivities,
    )


def _make_concept(
    *,
    cost_model: CostModelData | None = None,
    parameter_metadata: dict[str, ParameterMetadata] | None = None,
) -> ConceptData:
    return ConceptData(
        concept_id="04",
        name="Laser ICF",
        confinement_family=ConfinementFamily.IFE,
        status=ConceptStatus.APPROVED,
        has_cost_model=cost_model is not None,
        has_sensitivities=cost_model is not None and cost_model.sensitivities is not None,
        cost_model=cost_model,
        parameter_metadata=parameter_metadata or {},
        sources=SourcePaths(model_setup="analyses/04/model_setup.py"),
    )


# ---------------------------------------------------------------------------
# AC-1: from_forward_result populates all CAS10–CAS90 and C220101–C220700
# ---------------------------------------------------------------------------


def test_from_forward_result_all_cas_accounts_present() -> None:
    """AC-1: All top-level and CAS22 sub-accounts are present after construction."""
    result_dict = _make_forward_result_dict()
    cmd = CostModelData.from_forward_result(result_dict, sensitivities=None)

    # Top-level accounts CAS10–CAS90 must all be present
    for field in [
        "cas10",
        "cas21",
        "cas22",
        "cas23",
        "cas24",
        "cas25",
        "cas26",
        "cas27",
        "cas28",
        "cas29",
        "cas30",
        "cas40",
        "cas50",
        "cas60",
        "cas70",
        "cas80",
        "cas90",
    ]:
        account: CASAccount = getattr(cmd, field)
        assert isinstance(account, CASAccount), f"{field} missing"

    # All CAS22 sub-accounts C220101–C220700 must be present (zero-filled if absent)
    for key in CostModelData.CAS22_NAMES:
        assert key in cmd.cas22_detail, f"{key} missing from cas22_detail"
        assert isinstance(cmd.cas22_detail[key], CASAccount)


def test_from_forward_result_values_populated() -> None:
    """AC-1 (values): cost values are read from the dict correctly."""
    cmd = _make_cost_model()

    assert cmd.cas10.cost_m_usd == 10.0
    assert cmd.cas90.cost_m_usd == 90.0
    assert cmd.headline.lcoe_per_mwh == 120.5
    assert cmd.headline.overnight_cost_per_kw == 8500.0
    assert cmd.headline.p_net_mw == 1000.0
    assert cmd.headline.q_eng == 3.5
    assert cmd.headline.capacity_factor == 0.85


def test_from_forward_result_absent_cas22_zero_filled() -> None:
    """AC-1 (zero-fill): CAS22 sub-accounts absent from the dict default to 0.0."""
    result_dict = _make_forward_result_dict(cas22_override={"C220101": 99.0})
    cmd = CostModelData.from_forward_result(result_dict, sensitivities=None)

    assert cmd.cas22_detail["C220101"].cost_m_usd == 99.0
    # C220200 was not in the stub dict — must be zero-filled
    assert cmd.cas22_detail["C220200"].cost_m_usd == 0.0


def test_from_forward_result_overridden_flag() -> None:
    """AC-1 (overridden): accounts listed in 'overridden' carry overridden=True."""
    result_dict = _make_forward_result_dict(overridden=["C220103", "C220104"])
    cmd = CostModelData.from_forward_result(result_dict, sensitivities=None)

    # Sub-accounts
    assert cmd.cas22_detail["C220103"].overridden is True
    assert cmd.cas22_detail["C220104"].overridden is True
    # Accounts NOT in the overridden list
    assert cmd.cas22_detail["C220101"].overridden is False


def test_from_forward_result_capacity_factor_fallback() -> None:
    """AC-1 (fallback): 'availability' key used when 'capacity_factor' absent."""
    result_dict = _make_forward_result_dict(
        power_override={"capacity_factor": None, "availability": 0.70}
    )
    # Manually remove capacity_factor
    del result_dict["power_table"]["capacity_factor"]
    cmd = CostModelData.from_forward_result(result_dict, sensitivities=None)

    assert cmd.headline.capacity_factor == 0.70


# ---------------------------------------------------------------------------
# AC-2: ConceptData warns when sensitivity keys not covered by parameter_metadata
# ---------------------------------------------------------------------------


def test_concept_data_warns_on_uncovered_sensitivity_keys() -> None:
    """AC-2: UserWarning is emitted for uncovered sensitivity keys."""
    sens = SensitivityAnalysis(
        engineering={"eta_th": SensitivityEntry(elasticity=-0.8, baseline=0.35)},
        financial={"interest_rate": SensitivityEntry(elasticity=0.6, baseline=0.07)},
    )
    cost_model = _make_cost_model(sensitivities=sens)

    # parameter_metadata covers only 'eta_th', not 'interest_rate'
    partial_metadata = {
        "eta_th": ParameterMetadata(
            display_name="Thermal efficiency",
            category=ParameterCategory.KEY_INNOVATION,
            confidence=Confidence.MEDIUM,
            baseline=0.35,
            range=(0.25, 0.50),
        )
    }

    with pytest.warns(UserWarning, match="interest_rate"):
        _make_concept(cost_model=cost_model, parameter_metadata=partial_metadata)


def test_concept_data_no_warning_when_fully_covered() -> None:
    """AC-2 (inverse): no warning when all sensitivity keys have metadata."""
    sens = SensitivityAnalysis(
        engineering={"eta_th": SensitivityEntry(elasticity=-0.8, baseline=0.35)},
        financial={},
    )
    cost_model = _make_cost_model(sensitivities=sens)
    full_metadata = {
        "eta_th": ParameterMetadata(
            display_name="Thermal efficiency",
            category=ParameterCategory.KEY_INNOVATION,
            confidence=Confidence.MEDIUM,
            baseline=0.35,
            range=(0.25, 0.50),
        )
    }

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        _make_concept(cost_model=cost_model, parameter_metadata=full_metadata)


# ---------------------------------------------------------------------------
# AC-3: ConceptData round-trips via model_dump_json / model_validate_json
# ---------------------------------------------------------------------------


def test_concept_data_round_trip_json() -> None:
    """AC-3: ConceptData serialises and deserialises without data loss."""
    sens = SensitivityAnalysis(
        engineering={"eta_th": SensitivityEntry(elasticity=-0.8, baseline=0.35)},
        financial={"interest_rate": SensitivityEntry(elasticity=0.6, baseline=0.07)},
    )
    metadata = {
        "eta_th": ParameterMetadata(
            display_name="Thermal efficiency",
            category=ParameterCategory.KEY_INNOVATION,
            confidence=Confidence.MEDIUM,
            baseline=0.35,
            range=(0.25, 0.50),
            source="analysis.md §2",
            modeling_note="Steam Rankine; could be higher for direct conversion.",
        ),
        "interest_rate": ParameterMetadata(
            display_name="Discount rate",
            category=ParameterCategory.SHARED_BASELINE,
            confidence=Confidence.HIGH,
            baseline=0.07,
            display_multiplier=100.0,
            display_unit="%",
            range=(0.04, 0.12),
        ),
    }
    narrative = NarrativeData(
        key_bets=["Gain > 500 via avalanche mechanism"],
        eliminated_costs=["No tritium processing"],
        novel_costs=["Dual-component target factory"],
        risks=[{"description": "Laser wall-plug efficiency undemonstrated", "severity": "high"}],
    )
    original = ConceptData(
        concept_id="04",
        name="Laser ICF",
        confinement_family=ConfinementFamily.IFE,
        company="HB11 Energy",
        status=ConceptStatus.APPROVED,
        illustration="laser_icf.png",
        has_cost_model=True,
        has_sensitivities=True,
        cost_model=_make_cost_model(sensitivities=sens),
        parameter_metadata=metadata,
        narrative=narrative,
        sources=SourcePaths(
            model_setup="analyses/04/model_setup.py",
            analysis="analyses/04/analysis.md",
        ),
    )

    json_str = original.model_dump_json()
    restored = ConceptData.model_validate_json(json_str)

    # Top-level fields
    assert restored.concept_id == original.concept_id
    assert restored.name == original.name
    assert restored.confinement_family == original.confinement_family
    assert restored.company == original.company
    assert restored.status == original.status

    # Cost model
    assert restored.cost_model is not None
    assert restored.cost_model.cas10.cost_m_usd == original.cost_model.cas10.cost_m_usd  # type: ignore[union-attr]
    assert restored.cost_model.headline.lcoe_per_mwh == original.cost_model.headline.lcoe_per_mwh  # type: ignore[union-attr]

    # Sensitivities
    assert restored.cost_model.sensitivities is not None
    assert restored.cost_model.sensitivities.engineering["eta_th"].elasticity == -0.8

    # Parameter metadata
    assert restored.parameter_metadata["eta_th"].display_name == "Thermal efficiency"
    assert restored.parameter_metadata["eta_th"].range == (0.25, 0.50)
    assert restored.parameter_metadata["interest_rate"].display_multiplier == 100.0

    # Narrative
    assert restored.narrative is not None
    assert restored.narrative.key_bets[0] == "Gain > 500 via avalanche mechanism"
    assert restored.narrative.risks[0]["severity"] == "high"

    # Verify JSON is identical (no data loss)
    assert json.loads(json_str) == json.loads(restored.model_dump_json())


# ---------------------------------------------------------------------------
# AC-4: CostModelData with sensitivities=None raises no ValidationError
# ---------------------------------------------------------------------------


def test_cost_model_data_sensitivities_none_is_valid() -> None:
    """AC-4: Standalone concepts with sensitivities=None are valid."""
    cmd = _make_cost_model(sensitivities=None)
    assert cmd.sensitivities is None


def test_concept_data_with_null_sensitivities_no_error() -> None:
    """AC-4 (ConceptData): Concept with sensitivities=None builds without error."""
    cmd = _make_cost_model(sensitivities=None)
    concept = _make_concept(cost_model=cmd)
    assert concept.cost_model is not None
    assert concept.cost_model.sensitivities is None


# ---------------------------------------------------------------------------
# AC-5: Invalid enum values raise ValidationError on model_validate_json
# ---------------------------------------------------------------------------


def test_invalid_confinement_family_raises_validation_error() -> None:
    """AC-5: Unknown ConfinementFamily value raises ValidationError."""
    payload = json.dumps(
        {
            "concept_id": "04",
            "name": "Test",
            "confinement_family": "BOGUS_FAMILY",
            "status": "approved",
            "has_cost_model": False,
            "has_sensitivities": False,
            "sources": {},
        }
    )
    with pytest.raises(ValidationError):
        ConceptData.model_validate_json(payload)


def test_invalid_concept_status_raises_validation_error() -> None:
    """AC-5: Unknown ConceptStatus value raises ValidationError."""
    payload = json.dumps(
        {
            "concept_id": "04",
            "name": "Test",
            "confinement_family": "IFE",
            "status": "published",  # not a valid ConceptStatus
            "has_cost_model": False,
            "has_sensitivities": False,
            "sources": {},
        }
    )
    with pytest.raises(ValidationError):
        ConceptData.model_validate_json(payload)


def test_invalid_confidence_enum_raises_validation_error() -> None:
    """AC-5: Unknown Confidence value on ParameterMetadata raises ValidationError."""
    payload = json.dumps(
        {
            "display_name": "eta_th",
            "category": "key-innovation",
            "confidence": "very_high",  # not a valid Confidence
            "baseline": 0.35,
            "range": [0.25, 0.50],
        }
    )
    with pytest.raises(ValidationError):
        ParameterMetadata.model_validate_json(payload)


# ---------------------------------------------------------------------------
# AC-6: ConceptManifest serialises with data_file on every entry
# ---------------------------------------------------------------------------


def test_concept_manifest_serialises_with_data_file() -> None:
    """AC-6: Every entry in a serialised ConceptManifest has a non-empty data_file."""
    entry = ConceptManifestEntry(
        concept_id="04",
        name="Laser ICF",
        confinement_family=ConfinementFamily.IFE,
        status=ConceptStatus.APPROVED,
        has_cost_model=True,
        has_sensitivities=True,
        lcoe_per_mwh=120.5,
        confidence=Confidence.LOW,
        data_file="data/04.json",
    )
    manifest = ConceptManifest(
        generated_at="2026-03-29T12:00:00Z",
        concepts=[entry],
    )

    parsed = json.loads(manifest.model_dump_json())
    for concept_entry in parsed["concepts"]:
        assert "data_file" in concept_entry
        assert concept_entry["data_file"]  # non-empty


def test_concept_manifest_multiple_entries() -> None:
    """AC-6 (multiple): All entries have data_file in multi-concept manifest."""
    entries = [
        ConceptManifestEntry(
            concept_id=cid,
            name=f"Concept {cid}",
            confinement_family=ConfinementFamily.MFE,
            status=ConceptStatus.IN_PROGRESS,
            has_cost_model=False,
            has_sensitivities=False,
            data_file=f"data/{cid}.json",
        )
        for cid in ["01", "02", "03"]
    ]
    manifest = ConceptManifest(generated_at="2026-03-29T12:00:00Z", concepts=entries)

    parsed = json.loads(manifest.model_dump_json())
    assert len(parsed["concepts"]) == 3
    for entry in parsed["concepts"]:
        assert entry["data_file"].startswith("data/")
