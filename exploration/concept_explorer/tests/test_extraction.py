"""Tests for extract_explorer_data.py.

Uses mocked costingfe module loading and subprocess calls so that:
- No real costingfe computation runs
- No real claude -p subprocess runs
"""

from __future__ import annotations

import dataclasses
import json
import types
import warnings
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from exploration.concept_explorer.extract_explorer_data import (  # noqa: E402
    ExtractionError,
    apply_display_patches,
    discover_concepts,
    extract_costingfe,
    extract_narrative,
    extract_standalone,
    generate_parameter_metadata,
    load_parameter_display_registry,
    load_parameter_metadata,
    parse_concept_id,
    _build_override_records,
    _resolve_account_name,
    _to_confinement_family,
    parse_frontmatter,
    parse_status,
    run_extraction,
)
from exploration.concept_explorer.models import (  # noqa: E402, I001
    CASAccount,
    ConceptData,
    ConceptManifest,
    ConceptStatus,
    Confidence,
    ConfinementFamily,
    CostModelData,
    ParameterCategory,
    ParameterIndex,
    ParameterMetadata,
    SensitivityAnalysis,
    SensitivityEntry,
    SourcePaths,
    build_manifest,
    build_parameter_index,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_forward_result() -> Any:
    """Build a minimal costingfe ForwardResult dataclass for testing."""

    @dataclasses.dataclass
    class PowerTable:
        p_fus: float = 2000.0
        p_net: float = 1000.0
        q_eng: float = 8.0
        rec_frac: float = 0.12

    @dataclasses.dataclass
    class CostResult:
        cas10: float = 10.0
        cas21: float = 50.0
        cas22: float = 200.0
        cas23: float = 80.0
        cas24: float = 30.0
        cas25: float = 10.0
        cas26: float = 5.0
        cas27: float = 8.0
        cas28: float = 3.0
        cas29: float = 40.0
        cas20: float = 0.0
        cas30: float = 25.0
        cas40: float = 15.0
        cas50: float = 5.0
        cas60: float = 60.0
        cas70: float = 20.0
        cas71: float = 0.0
        cas72: float = 0.0
        cas80: float = 3.0
        cas90: float = 90.0
        total_capital: float = 486.0
        lcoe: float = 75.0
        overnight_cost: float = 5000.0

    @dataclasses.dataclass
    class MockForwardResult:
        power_table: PowerTable = dataclasses.field(default_factory=PowerTable)
        costs: CostResult = dataclasses.field(default_factory=CostResult)
        params: dict[str, float] = dataclasses.field(
            default_factory=lambda: {
                "availability": 0.85,
                "thermal_efficiency": 0.35,
                "interest_rate": 0.07,
                "inflation_rate": 0.025,
                "construction_time_yr": 5.0,
            }
        )
        overridden: list[str] = dataclasses.field(default_factory=list)
        cas22_detail: dict[str, float] = dataclasses.field(
            default_factory=lambda: {
                "C220101": 20.0,
                "C220103": 80.0,
            }
        )
        plasma_state: None = None

    return MockForwardResult()


def _make_mock_model() -> MagicMock:
    """Build a mock CostModel that returns canned sensitivity data."""
    model = MagicMock()
    model.sensitivity.return_value = {
        "engineering": {
            "availability": 0.75,
            "thermal_efficiency": -0.42,
        },
        "financial": {
            "interest_rate": 0.85,
            "inflation_rate": 0.12,
        },
    }
    return model


def _make_concept_dir(
    tmp_path: Path,
    concept_id: str = "04",
    name: str = "Test Concept",
    company: str = "Test Corp",
    status: str = "approved",
    confinement: str = "IFE (Inertial Fusion Energy)",
    with_model_setup: bool = True,
    with_analysis: bool = True,
    with_metadata: bool = False,
) -> Path:
    """Create a minimal concept directory in tmp_path."""
    concept_dir = tmp_path / f"{concept_id}-test-concept"
    concept_dir.mkdir(exist_ok=True)

    if with_analysis:
        # Map legacy `confinement` text (e.g. "IFE (Inertial Fusion Energy)") to
        # the enum value Item 6 frontmatter expects.
        family_key = confinement.strip().split()[0].upper() if confinement else "NONSTANDARD"
        (concept_dir / "analysis.md").write_text(
            f"---\nID: {concept_id}-test-concept\n"
            f"Concept: {name}\nCompany: {company}\nStatus: {status}\n"
            f"Confinement-Family: {family_key}\n---\n\n"
            f"Some analysis text.\n",
            encoding="utf-8",
        )

    if with_model_setup:
        # Stub — patched in tests via load_module_from_path
        (concept_dir / "model_setup.py").write_text(
            "# stub — patched in tests\nmodel = None\nresult_1gw = None\n",
            encoding="utf-8",
        )

    if with_metadata:
        import yaml  # noqa: PLC0415

        meta = {
            "availability": {
                "display_name": "Plant Availability",
                "category": "shared-baseline",
                "confidence": "high",
                "baseline": 0.85,
                "display_multiplier": 100.0,
                "display_unit": "%",
                "range": [0.6, 0.95],
                "source": "test source",
                "modeling_note": None,
            }
        }
        (concept_dir / "model_metadata.yaml").write_text(yaml.dump(meta), encoding="utf-8")

    return concept_dir


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


class TestParseConceptId:
    def test_numeric_prefix(self) -> None:
        assert parse_concept_id("04-laser-icf") == "04"

    def test_alpha_suffix(self) -> None:
        assert parse_concept_id("17a-laser-icf-hybrid") == "17a"

    def test_single_digit(self) -> None:
        assert parse_concept_id("1-test") == "1"

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="Cannot extract concept ID"):
            parse_concept_id("no-id-here")


class TestParseFrontmatter:
    def test_parses_yaml_block(self, tmp_path: Path) -> None:
        p = tmp_path / "analysis.md"
        p.write_text("---\nConcept: Foo\nStatus: approved\n---\nBody text\n")
        fm = parse_frontmatter(p)
        assert fm["Concept"] == "Foo"
        assert fm["Status"] == "approved"

    def test_no_frontmatter(self, tmp_path: Path) -> None:
        p = tmp_path / "analysis.md"
        p.write_text("No frontmatter here")
        assert parse_frontmatter(p) == {}


class TestToConfinementFamily:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("MFE", ConfinementFamily.MFE),
            ("IFE", ConfinementFamily.IFE),
            ("MIF", ConfinementFamily.MIF),
            ("NONSTANDARD", ConfinementFamily.NONSTANDARD),
            ("mfe", ConfinementFamily.MFE),  # case-insensitive
            (" IFE ", ConfinementFamily.IFE),  # strip
            ("BOGUS", ConfinementFamily.NONSTANDARD),  # unknown → fallback
            (None, ConfinementFamily.NONSTANDARD),  # missing → fallback
            ("", ConfinementFamily.NONSTANDARD),
        ],
    )
    def test_mapping(self, raw: Any, expected: ConfinementFamily) -> None:
        assert _to_confinement_family(raw) == expected


class TestParseStatus:
    def test_approved(self) -> None:
        assert parse_status({"Status": "approved"}) == ConceptStatus.APPROVED

    def test_draft(self) -> None:
        assert parse_status({"Status": "draft"}) == ConceptStatus.IN_PROGRESS

    def test_missing(self) -> None:
        assert parse_status({}) == ConceptStatus.IN_PROGRESS


# ---------------------------------------------------------------------------
# AC-1: costingfe pathway produces ConceptData with non-null sensitivities
# ---------------------------------------------------------------------------


class TestExtractCostingfe:
    def test_produces_concept_with_sensitivities(self, tmp_path: Path) -> None:
        """AC-1: costingfe concept dir yields ConceptData with non-null sensitivities."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=True)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test Concept", "Company": "Corp", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        assert concept.has_cost_model is True
        assert concept.has_sensitivities is True
        assert concept.cost_model is not None
        assert concept.cost_model.sensitivities is not None
        assert "availability" in concept.cost_model.sensitivities.engineering
        assert "interest_rate" in concept.cost_model.sensitivities.financial

    def test_sensitivity_entries_have_baselines(self, tmp_path: Path) -> None:
        """Baselines come from result.params, not hard-coded."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        assert concept.cost_model is not None
        assert concept.cost_model.sensitivities is not None
        avail_entry = concept.cost_model.sensitivities.engineering["availability"]
        assert avail_entry.baseline == pytest.approx(0.85)

    def test_availability_injected_for_capacity_factor(self, tmp_path: Path) -> None:
        """Capacity factor uses availability from params when power_table lacks it."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        assert concept.cost_model is not None
        assert concept.cost_model.headline.capacity_factor == pytest.approx(0.85)

    def test_missing_model_attribute_raises(self, tmp_path: Path) -> None:
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace()  # no model/result_1gw

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            with pytest.raises(ExtractionError, match="module-level 'model'"):
                extract_costingfe(
                    concept_dir=concept_dir,
                    concept_id="04",
                    frontmatter={},
                    analysis_path=concept_dir / "analysis.md",
                    narrative=None,
                    param_metadata={},
                )

    def test_missing_result_1gw_raises(self, tmp_path: Path) -> None:
        """Concept exposing `model` but no `result_1gw` is a contract violation."""
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model)  # no result_1gw

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            with pytest.raises(ExtractionError, match="result_1gw missing"):
                extract_costingfe(
                    concept_dir=concept_dir,
                    concept_id="04",
                    frontmatter={},
                    analysis_path=concept_dir / "analysis.md",
                    narrative=None,
                    param_metadata={},
                )

    def test_generates_parameter_metadata(self, tmp_path: Path) -> None:
        """extract_costingfe() auto-fills parameter_metadata from sensitivities."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        assert len(concept.parameter_metadata) > 0
        assert "availability" in concept.parameter_metadata
        assert "interest_rate" in concept.parameter_metadata
        # Auto-generated entries carry default category / confidence
        assert concept.parameter_metadata["availability"].category == ParameterCategory.UNCLASSIFIED
        assert concept.parameter_metadata["availability"].confidence == Confidence.UNKNOWN

    def test_yaml_overrides_win_over_generated(self, tmp_path: Path) -> None:
        """When yaml param_metadata has an entry for the same key, it replaces
        the auto-generated entry entirely."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        yaml_override = {
            "availability": ParameterMetadata(
                display_name="Plant Availability (Curated)",
                category=ParameterCategory.SHARED_BASELINE,
                confidence=Confidence.HIGH,
                baseline=0.85,
                range=(0.6, 0.95),
                source="curated source",
            )
        }

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata=yaml_override,
            )

        avail = concept.parameter_metadata["availability"]
        assert avail.display_name == "Plant Availability (Curated)"
        assert avail.category == ParameterCategory.SHARED_BASELINE
        assert avail.confidence == Confidence.HIGH
        assert avail.range == (0.6, 0.95)
        # Other sensitivity keys still get generated entries
        assert "interest_rate" in concept.parameter_metadata
        assert concept.parameter_metadata["interest_rate"].category == ParameterCategory.UNCLASSIFIED

    def test_concept_data_validates_as_pydantic(self, tmp_path: Path) -> None:
        """Extracted ConceptData round-trips JSON without data loss."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        json_str = concept.model_dump_json()
        roundtrip = ConceptData.model_validate_json(json_str)
        assert roundtrip.concept_id == concept.concept_id
        assert roundtrip.cost_model is not None
        assert roundtrip.cost_model.sensitivities is not None


# ---------------------------------------------------------------------------
# Display registry: shared display-name patches between generated and per-concept
# ---------------------------------------------------------------------------


class TestDisplayRegistry:
    def test_apply_patches_updates_only_display_fields(self) -> None:
        """Registry patches display_name/_unit/_multiplier; baseline/range/category preserved."""
        generated = {
            "eta_th": ParameterMetadata(
                display_name="Eta Th",
                category=ParameterCategory.UNCLASSIFIED,
                confidence=Confidence.UNKNOWN,
                baseline=0.46,
                range=(0.32, 0.6),
            )
        }
        patches = {
            "eta_th": {
                "display_name": "Thermal Efficiency",
                "display_unit": "%",
                "display_multiplier": 100.0,
            }
        }

        out = apply_display_patches(generated, patches)

        assert out["eta_th"].display_name == "Thermal Efficiency"
        assert out["eta_th"].display_unit == "%"
        assert out["eta_th"].display_multiplier == 100.0
        # Generated fields preserved
        assert out["eta_th"].baseline == 0.46
        assert out["eta_th"].range == (0.32, 0.6)
        assert out["eta_th"].category == ParameterCategory.UNCLASSIFIED
        assert out["eta_th"].confidence == Confidence.UNKNOWN

    def test_apply_patches_skips_unknown_keys(self) -> None:
        """Patches for parameters not in this concept's sensitivities are ignored."""
        generated = {
            "availability": ParameterMetadata(
                display_name="Availability",
                category=ParameterCategory.UNCLASSIFIED,
                confidence=Confidence.UNKNOWN,
                baseline=0.75,
                range=(0.5, 1.0),
            )
        }
        patches = {
            "availability": {"display_name": "Plant Availability"},
            "not_in_this_concept": {"display_name": "Should Not Appear"},
        }

        out = apply_display_patches(generated, patches)

        assert set(out.keys()) == {"availability"}
        assert out["availability"].display_name == "Plant Availability"

    def test_load_registry_drops_unknown_fields_and_warns(self, tmp_path: Path) -> None:
        """Registry loader silently drops unknown fields with a warning."""
        path = tmp_path / "registry.yaml"
        path.write_text(
            "eta_th:\n"
            "  display_name: Thermal Efficiency\n"
            "  display_unit: '%'\n"
            "  display_multiplier: 100.0\n"
            "  baseline: 0.5\n"  # not allowed in registry
            "  category: shared-baseline\n"  # not allowed in registry
            "bad_entry: not a dict\n",
            encoding="utf-8",
        )

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            out = load_parameter_display_registry(path)

        # Unknown fields stripped; entry retained
        assert "eta_th" in out
        assert set(out["eta_th"].keys()) == {"display_name", "display_unit", "display_multiplier"}
        # Non-dict entry skipped
        assert "bad_entry" not in out
        # Warnings fired for both issues
        msgs = [str(w.message) for w in caught]
        assert any("unknown fields" in m for m in msgs)
        assert any("non-dict" in m for m in msgs)

    def test_load_registry_returns_empty_when_missing(self, tmp_path: Path) -> None:
        out = load_parameter_display_registry(tmp_path / "does-not-exist.yaml")
        assert out == {}

    def test_per_concept_yaml_still_wins_over_registry(self, tmp_path: Path) -> None:
        """Three-layer merge order: per-concept yaml beats registry beats generated."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        # Per-concept yaml provides a full ParameterMetadata for availability
        per_concept = {
            "availability": ParameterMetadata(
                display_name="CONCEPT_OVERRIDE",
                category=ParameterCategory.SHARED_BASELINE,
                confidence=Confidence.HIGH,
                baseline=0.85,
                range=(0.6, 0.95),
            )
        }
        # Registry patches just the display_name
        registry_patches = {
            "availability": {"display_name": "REGISTRY_NAME", "display_unit": "%"},
            "interest_rate": {"display_name": "Interest Rate", "display_unit": "%"},
        }

        with patch(
            "exploration.concept_explorer.extract_explorer_data._DISPLAY_REGISTRY",
            registry_patches,
        ), patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata=per_concept,
            )

        # Per-concept beats registry on availability
        avail = concept.parameter_metadata["availability"]
        assert avail.display_name == "CONCEPT_OVERRIDE"
        assert avail.category == ParameterCategory.SHARED_BASELINE
        # Registry beats generated on interest_rate (no per-concept override)
        ir = concept.parameter_metadata["interest_rate"]
        assert ir.display_name == "Interest Rate"
        assert ir.display_unit == "%"
        # Generated baseline/range preserved on the registry-patched entry
        assert ir.baseline > 0
        assert ir.range[0] < ir.range[1]


# ---------------------------------------------------------------------------
# AC-2: standalone pathway produces ConceptData with sensitivities == null
# ---------------------------------------------------------------------------


class TestExtractStandalone:
    def test_no_python_script_produces_null_cost_model(self, tmp_path: Path) -> None:
        """AC-2: standalone concept with no Python script → cost_model=None."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False, with_analysis=True)

        concept = extract_standalone(
            concept_dir=concept_dir,
            concept_id="01",
            frontmatter={"Concept": "Standalone Concept", "Status": "approved"},
            analysis_path=concept_dir / "analysis.md",
            narrative=None,
            param_metadata={},
        )

        assert concept.has_cost_model is False
        assert concept.cost_model is None
        assert concept.has_sensitivities is False

    def test_script_with_to_explorer_dict_populates_cost_model(self, tmp_path: Path) -> None:
        """Standalone script that defines to_explorer_dict() → cost_model populated."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False, with_analysis=True)
        (concept_dir / "analysis_script.py").write_text("# standalone\n")

        valid_cost_model = _build_minimal_cost_model_dict()

        def fake_to_explorer_dict() -> dict[str, Any]:
            return valid_cost_model

        mock_module = types.SimpleNamespace(to_explorer_dict=fake_to_explorer_dict)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_standalone(
                concept_dir=concept_dir,
                concept_id="07",
                frontmatter={"Concept": "MagLIF", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        assert concept.has_cost_model is True
        assert concept.cost_model is not None
        assert concept.cost_model.sensitivities is None

    def test_missing_to_explorer_dict_warns(self, tmp_path: Path) -> None:
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False, with_analysis=True)
        (concept_dir / "analysis_script.py").write_text("# no to_explorer_dict\n")
        mock_module = types.SimpleNamespace()  # no to_explorer_dict

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                extract_standalone(
                    concept_dir=concept_dir,
                    concept_id="07",
                    frontmatter={"Concept": "Test", "Status": "draft"},
                    analysis_path=concept_dir / "analysis.md",
                    narrative=None,
                    param_metadata={},
                )
        assert any("no to_explorer_dict" in str(warning.message) for warning in w)


# ---------------------------------------------------------------------------
# Routing detection: import-based costingfe vs freeform
# ---------------------------------------------------------------------------


class TestRoutingDetection:
    """Verify that run_extraction routes based on module content, not filename."""

    def test_freeform_model_setup_routes_to_standalone(self, tmp_path: Path) -> None:
        """model_setup.py without costingfe import → standalone pathway."""
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        concept_dir = _make_concept_dir(
            analyses_dir, concept_id="12", with_model_setup=False, with_analysis=True
        )
        # Freeform model_setup.py — no costingfe imports
        (concept_dir / "model_setup.py").write_text(
            "# freeform script\nparams = None\n"
            "def to_explorer_dict(): return {}\n",
            encoding="utf-8",
        )

        valid_cost_model = _build_minimal_cost_model_dict()

        def fake_to_explorer_dict() -> dict[str, Any]:
            return valid_cost_model

        mock_module = types.SimpleNamespace(to_explorer_dict=fake_to_explorer_dict)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ) as mock_load:
            run_extraction(
                analyses_dir=analyses_dir,
                data_dir=tmp_path / "data",
                skip_narrative=True,
            )

        # Verify the module was loaded (standalone pathway loads it)
        mock_load.assert_called_once()
        # Verify output was written and has cost model from to_explorer_dict
        data = json.loads((tmp_path / "data" / "12.json").read_text())
        assert data["has_cost_model"] is True

    def test_costingfe_model_setup_routes_to_costingfe(self, tmp_path: Path) -> None:
        """model_setup.py with CostModel import → costingfe pathway."""
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        concept_dir = _make_concept_dir(
            analyses_dir, concept_id="01", with_model_setup=False, with_analysis=True
        )
        # Costingfe model_setup.py
        (concept_dir / "model_setup.py").write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel()\nresult = model.forward()\n",
            encoding="utf-8",
        )

        result = _make_forward_result()
        model = _make_mock_model()
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            run_extraction(
                analyses_dir=analyses_dir,
                data_dir=tmp_path / "data",
                skip_narrative=True,
            )

        data = json.loads((tmp_path / "data" / "01.json").read_text())
        assert data["has_sensitivities"] is True  # Only costingfe pathway sets this

    def test_costingfe_constants_only_routes_to_standalone(self, tmp_path: Path) -> None:
        """import costingfe for constants (no CostModel) → standalone pathway."""
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        concept_dir = _make_concept_dir(
            analyses_dir, concept_id="15", with_model_setup=False, with_analysis=True
        )
        # Imports costingfe but no CostModel usage
        (concept_dir / "model_setup.py").write_text(
            "from costingfe.constants import SOME_VALUE\n"
            "params = None\n"
            "def to_explorer_dict(): return {}\n",
            encoding="utf-8",
        )

        valid_cost_model = _build_minimal_cost_model_dict()

        def fake_to_explorer_dict() -> dict[str, Any]:
            return valid_cost_model

        mock_module = types.SimpleNamespace(to_explorer_dict=fake_to_explorer_dict)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            run_extraction(
                analyses_dir=analyses_dir,
                data_dir=tmp_path / "data",
                skip_narrative=True,
            )

        data = json.loads((tmp_path / "data" / "15.json").read_text())
        # Routed to standalone — has_sensitivities is False (no compute_sensitivity on mock)
        assert data["has_sensitivities"] is False
        assert data["has_cost_model"] is True

    def test_standalone_prefers_model_setup_py(self, tmp_path: Path) -> None:
        """When model_setup.py exists alongside other .py, it's loaded first."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False, with_analysis=True)
        # Create two .py files — aaa.py sorts first alphabetically
        (concept_dir / "aaa_script.py").write_text("# should not be loaded\n")
        (concept_dir / "model_setup.py").write_text("# freeform\n")

        valid_cost_model = _build_minimal_cost_model_dict()

        def fake_to_explorer_dict() -> dict[str, Any]:
            return valid_cost_model

        mock_module = types.SimpleNamespace(to_explorer_dict=fake_to_explorer_dict)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ) as mock_load:
            extract_standalone(
                concept_dir=concept_dir,
                concept_id="12",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        # model_setup.py should be the file loaded, not aaa_script.py
        loaded_path = mock_load.call_args[0][0]
        assert loaded_path.name == "model_setup.py"

    def test_compute_sensitivity_populates_sensitivities(self, tmp_path: Path) -> None:
        """Standalone module with compute_sensitivity() → has_sensitivities=True."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False, with_analysis=True)
        (concept_dir / "model_setup.py").write_text("# freeform\n")

        valid_cost_model = _build_minimal_cost_model_dict()
        valid_cost_model["params"] = {"availability": 0.85, "interest_rate": 0.07}

        def fake_to_explorer_dict() -> dict[str, Any]:
            return valid_cost_model

        def fake_compute_sensitivity() -> dict[str, dict[str, float]]:
            return {
                "engineering": {"availability": 0.75},
                "financial": {"interest_rate": 0.85},
            }

        mock_module = types.SimpleNamespace(
            to_explorer_dict=fake_to_explorer_dict,
            compute_sensitivity=fake_compute_sensitivity,
        )

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_standalone(
                concept_dir=concept_dir,
                concept_id="12",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )

        assert concept.has_sensitivities is True
        assert concept.cost_model is not None
        assert concept.cost_model.sensitivities is not None
        assert "availability" in concept.cost_model.sensitivities.engineering
        assert concept.cost_model.sensitivities.engineering["availability"].elasticity == pytest.approx(0.75)
        assert concept.cost_model.sensitivities.engineering["availability"].baseline == pytest.approx(0.85)


# ---------------------------------------------------------------------------
# FR-A4: warn-and-tolerate when model_setup.py present but analysis.md absent
# ---------------------------------------------------------------------------


class TestEmptyFrontmatterWarning:
    """The 12 old-shape concepts (PR #39 refreshed model_setup.py but did not
    produce analysis.md). Extraction tolerates them with a single UserWarning
    that names the fields that fell back to defaults.
    """

    def test_warns_on_missing_analysis_md(self, tmp_path: Path) -> None:
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        concept_dir = analyses_dir / "04-old-shape-concept"
        concept_dir.mkdir()
        # model_setup.py present, analysis.md absent — the old-shape case.
        (concept_dir / "model_setup.py").write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel()\nresult_1gw = model.forward()\n",
            encoding="utf-8",
        )

        result = _make_forward_result()
        model = _make_mock_model()
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            with pytest.warns(UserWarning, match=r"04:.*no analysis\.md.*defaulted"):
                run_extraction(
                    analyses_dir=analyses_dir,
                    data_dir=tmp_path / "data",
                    skip_narrative=True,
                )

        # Extraction still produces a JSON with safe defaults.
        data = json.loads((tmp_path / "data" / "04.json").read_text())
        assert data["concept_id"] == "04"
        assert data["confinement_family"] == "NONSTANDARD"
        # name falls back to the directory name
        assert data["name"] == "04-old-shape-concept"

    def test_no_warning_when_analysis_md_present(self, tmp_path: Path) -> None:
        """Sanity: the warning fires only for the empty-frontmatter case."""
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        concept_dir = _make_concept_dir(
            analyses_dir, concept_id="01", with_model_setup=False, with_analysis=True
        )
        (concept_dir / "model_setup.py").write_text(
            "from costingfe.model import CostModel\n"
            "model = CostModel()\nresult_1gw = model.forward()\n",
            encoding="utf-8",
        )

        result = _make_forward_result()
        model = _make_mock_model()
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                run_extraction(
                    analyses_dir=analyses_dir,
                    data_dir=tmp_path / "data",
                    skip_narrative=True,
                )

        old_shape_warnings = [
            w for w in caught
            if "no analysis.md" in str(w.message)
        ]
        assert old_shape_warnings == []


# ---------------------------------------------------------------------------
# AC-3: --skip-narrative skips claude call, narrative=null
# ---------------------------------------------------------------------------


class TestSkipNarrative:
    def test_no_subprocess_call_with_skip_narrative(self, tmp_path: Path) -> None:
        """AC-3: --skip-narrative must not invoke subprocess."""
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        analyses_dir.mkdir()
        _make_concept_dir(analyses_dir, with_model_setup=False, with_analysis=True)

        mock_module = types.SimpleNamespace()

        with (
            patch(
                "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
                return_value=mock_module,
            ),
            patch("exploration.concept_explorer.extract_explorer_data.subprocess.run") as mock_run,
        ):
            run_extraction(
                analyses_dir=analyses_dir,
                data_dir=data_dir,
                concept_filter=None,
                skip_narrative=True,
            )

        mock_run.assert_not_called()

        written = json.loads((data_dir / "04.json").read_text())
        assert written["narrative"] is None


# ---------------------------------------------------------------------------
# AC-4: manifest validates as ConceptManifest with one entry per extracted concept
# ---------------------------------------------------------------------------


class TestBuildManifest:
    def test_manifest_validates_and_matches_count(self) -> None:
        """AC-4: manifest validates as ConceptManifest with correct entries."""
        concepts = _make_three_concepts()
        manifest = build_manifest(concepts)

        reloaded = ConceptManifest.model_validate_json(manifest.model_dump_json())
        assert len(reloaded.concepts) == 3
        assert {e.concept_id for e in reloaded.concepts} == {"01", "04", "07"}

    def test_data_file_present_on_each_entry(self) -> None:
        concepts = _make_three_concepts()
        for entry in build_manifest(concepts).concepts:
            assert entry.data_file == f"data/{entry.concept_id}.json"

    def test_lcoe_null_for_no_cost_model(self) -> None:
        concepts = _make_three_concepts()
        manifest = build_manifest(concepts)
        entry_01 = next(e for e in manifest.concepts if e.concept_id == "01")
        assert entry_01.lcoe_per_mwh is None


# ---------------------------------------------------------------------------
# AC-5: parameter index contains every sensitivity parameter
# ---------------------------------------------------------------------------


class TestBuildParameterIndex:
    def test_validates_as_pydantic(self) -> None:
        """AC-5: parameter_index.json validates as ParameterIndex."""
        concepts = _make_three_concepts()
        reloaded = ParameterIndex.model_validate_json(
            build_parameter_index(concepts).model_dump_json()
        )
        assert "availability" in reloaded.parameters
        assert "interest_rate" in reloaded.parameters

    def test_each_param_lists_contributing_concepts(self) -> None:
        concepts = _make_three_concepts()
        index = build_parameter_index(concepts)
        contributing = {c.concept_id for c in index.parameters["availability"].concepts}
        assert "04" in contributing

    def test_standalone_concepts_excluded_from_index(self) -> None:
        """Concepts with sensitivities=None don't appear in parameter index."""
        concepts = _make_three_concepts()
        index = build_parameter_index(concepts)
        for entry in index.parameters.values():
            ids = {c.concept_id for c in entry.concepts}
            assert "01" not in ids
            assert "07" not in ids


# ---------------------------------------------------------------------------
# AC-6: narrative validation failure → ExtractionError
# ---------------------------------------------------------------------------


class TestNarrativeExtractionFailure:
    def test_bad_narrative_json_raises_extraction_error(self, tmp_path: Path) -> None:
        """AC-6: invalid NarrativeData JSON raises ExtractionError."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False, with_analysis=True)

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = json.dumps({"key_bets": "not a list"})  # Wrong type
        mock_proc.stderr = ""

        with patch(
            "exploration.concept_explorer.extract_explorer_data.subprocess.run",
            return_value=mock_proc,
        ):
            with pytest.raises(ExtractionError, match="NarrativeData validation failed"):
                extract_narrative(concept_dir, "07")

    def test_subprocess_failure_raises_extraction_error(self, tmp_path: Path) -> None:
        """claude -p non-zero exit → ExtractionError."""
        concept_dir = _make_concept_dir(tmp_path, with_model_setup=False, with_analysis=True)

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stdout = ""
        mock_proc.stderr = "claude error"

        with patch(
            "exploration.concept_explorer.extract_explorer_data.subprocess.run",
            return_value=mock_proc,
        ):
            with pytest.raises(ExtractionError, match="claude -p exited 1"):
                extract_narrative(concept_dir, "07")

    def test_run_extraction_collects_narrative_failure(self, tmp_path: Path) -> None:
        """Keep-going: a narrative failure is recorded, not propagated.

        Previously run_extraction re-raised the ExtractionError from
        extract_narrative and aborted the whole batch. Now it catches the
        failure, counts it, and returns the failure count without raising.
        """
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        data_dir = tmp_path / "data"
        _make_concept_dir(analyses_dir, with_model_setup=False, with_analysis=True)

        mock_proc = MagicMock()
        mock_proc.returncode = 1
        mock_proc.stdout = ""
        mock_proc.stderr = "fail"

        with patch(
            "exploration.concept_explorer.extract_explorer_data.subprocess.run",
            return_value=mock_proc,
        ):
            failures = run_extraction(
                analyses_dir=analyses_dir,
                data_dir=data_dir,
                skip_narrative=False,
            )

        assert failures == 1
        # Failed concept wrote no JSON — it failed before the write step.
        assert not (data_dir / "04.json").exists()


# ---------------------------------------------------------------------------
# Batch resilience: one concept's failure must not abort the run (FR-1..FR-5)
# ---------------------------------------------------------------------------


def _write_concept(
    analyses_dir: Path,
    concept_id: str,
    *,
    analysis: str | None = None,
    model_setup: str | None = None,
) -> None:
    """Create a concept dir with optional analysis.md / model_setup.py bodies."""
    d = analyses_dir / f"{concept_id}-test"
    d.mkdir(parents=True, exist_ok=True)
    if analysis is not None:
        (d / "analysis.md").write_text(analysis, encoding="utf-8")
    if model_setup is not None:
        (d / "model_setup.py").write_text(model_setup, encoding="utf-8")


# A model_setup.py that routes to costingfe (source contains the detection
# substrings) but raises on import. The substrings live in a comment so the
# failure is a guaranteed RuntimeError, independent of whether costingfe is
# importable — it stands in for "any per-concept failure, deep origin, non-
# ExtractionError type."
_RAISING_COSTINGFE = (
    "# from costingfe import CostModel\n"
    "raise RuntimeError('boom on import')\n"
)


class TestBatchResilience:
    def test_failure_does_not_abort_batch(self, tmp_path: Path) -> None:
        """A failing concept is skipped; a later healthy concept still extracts."""
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        # 01 fails on import; 04 is a bare standalone (analysis only) that extracts.
        _write_concept(
            analyses_dir, "01", analysis="---\nID: 01\n---\n", model_setup=_RAISING_COSTINGFE
        )
        _write_concept(analyses_dir, "04", analysis="---\nID: 04\nConcept: Ok\n---\n")

        failures = run_extraction(
            analyses_dir=analyses_dir, data_dir=data_dir, skip_narrative=True
        )

        assert failures == 1
        # Later concept reached despite the earlier failure.
        assert (data_dir / "04.json").exists()
        assert not (data_dir / "01.json").exists()

    def test_failure_is_error_agnostic(self, tmp_path: Path, capsys: Any) -> None:
        """A non-ExtractionError (RuntimeError on import) is caught and reported."""
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        _write_concept(
            analyses_dir, "01", analysis="---\nID: 01\n---\n", model_setup=_RAISING_COSTINGFE
        )

        failures = run_extraction(
            analyses_dir=analyses_dir, data_dir=data_dir, skip_narrative=True
        )

        assert failures == 1
        out = capsys.readouterr().out
        assert "EXTRACTION FAILED" in out
        assert "01" in out
        # Type-agnostic catch, but the type is still shown to a human.
        assert "RuntimeError" in out

    def test_skip_and_failure_are_distinct(self, tmp_path: Path, capsys: Any) -> None:
        """pending-design-point lands under skipped; a crash lands under failed."""
        analyses_dir = tmp_path / "analyses"
        data_dir = tmp_path / "data"
        _write_concept(
            analyses_dir,
            "01",
            analysis="---\nID: 01\nComparison-Status: pending-design-point\n---\n",
        )
        _write_concept(
            analyses_dir, "04", analysis="---\nID: 04\n---\n", model_setup=_RAISING_COSTINGFE
        )

        failures = run_extraction(
            analyses_dir=analyses_dir, data_dir=data_dir, skip_narrative=True
        )

        assert failures == 1  # only 04 counts as a failure
        out = capsys.readouterr().out
        assert "Skipped 1 concept(s)" in out
        assert "pending-design-point" in out
        assert "EXTRACTION FAILED — 1 concept(s)" in out


# ---------------------------------------------------------------------------
# AC-7: missing model_metadata.yaml sensitivity keys → warning (not error)
# ---------------------------------------------------------------------------


class TestParameterMetadataWarning:
    def test_no_warning_when_metadata_auto_generated(self, tmp_path: Path) -> None:
        """Empty param_metadata is now safe — extract_costingfe auto-generates
        an entry for every sensitivity key, so the validator's coverage warning
        never fires."""
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                extract_costingfe(
                    concept_dir=concept_dir,
                    concept_id="04",
                    frontmatter={"Concept": "Test", "Status": "approved"},
                    analysis_path=concept_dir / "analysis.md",
                    narrative=None,
                    param_metadata={},
                )

        assert not any(
            "sensitivity keys not covered" in str(w.message) for w in caught
        ), "Auto-generation should cover every sensitivity key"

    def test_metadata_missing_file_returns_empty(self, tmp_path: Path) -> None:
        """Missing model_metadata.yaml returns empty dict (no exception)."""
        concept_dir = tmp_path / "04-test"
        concept_dir.mkdir()
        assert load_parameter_metadata(concept_dir, "04") == {}

    def test_metadata_loads_valid_entries(self, tmp_path: Path) -> None:
        concept_dir = _make_concept_dir(tmp_path, with_metadata=True, with_model_setup=False)
        result = load_parameter_metadata(concept_dir, "04")
        assert "availability" in result
        assert result["availability"].display_name == "Plant Availability"
        assert result["availability"].baseline == pytest.approx(0.85)


# ---------------------------------------------------------------------------
# generate_parameter_metadata: derive ParameterMetadata from sensitivities
# ---------------------------------------------------------------------------


class TestGenerateParameterMetadata:
    def test_basic(self) -> None:
        sens = SensitivityAnalysis(
            engineering={
                "availability": SensitivityEntry(elasticity=0.75, baseline=0.85),
                "R0": SensitivityEntry(elasticity=-0.3, baseline=5.0),
            },
            financial={
                "interest_rate": SensitivityEntry(elasticity=0.85, baseline=0.07),
            },
        )
        meta = generate_parameter_metadata(sens)
        assert set(meta.keys()) == {"availability", "R0", "interest_rate"}
        # Fractional param clamped to [0, 1]
        assert meta["availability"].range[1] <= 1.0
        assert meta["availability"].range[0] >= 0
        # Non-fractional: baseline ± 30%
        assert meta["R0"].range == pytest.approx((3.5, 6.5))
        # All entries are valid ParameterMetadata (Pydantic didn't reject)
        assert meta["R0"].display_name == "R0"
        # Defaults
        assert meta["R0"].category == ParameterCategory.UNCLASSIFIED
        assert meta["R0"].confidence == Confidence.UNKNOWN

    def test_fractional_clamping(self) -> None:
        """Efficiency/availability/eta/fraction params clamp to [0, 1]."""
        sens = SensitivityAnalysis(
            engineering={
                "availability": SensitivityEntry(elasticity=0.7, baseline=0.95),
                "thermal_efficiency": SensitivityEntry(elasticity=-0.4, baseline=0.85),
                "eta_th": SensitivityEntry(elasticity=-0.3, baseline=0.9),
                "burn_fraction": SensitivityEntry(elasticity=0.2, baseline=0.8),
                "f_cu": SensitivityEntry(elasticity=0.1, baseline=0.9),
            },
            financial={},
        )
        meta = generate_parameter_metadata(sens)
        # All would have baseline*1.3 > 1 — verify clamp
        for name in ("availability", "thermal_efficiency", "eta_th", "burn_fraction", "f_cu"):
            assert meta[name].range[1] <= 1.0, f"{name} hi exceeds 1.0"
            assert meta[name].range[0] >= 0
            assert meta[name].range[0] < meta[name].range[1]

    def test_zero_baseline_fallback(self) -> None:
        """Zero baseline produces fallback (0, 1) range, not degenerate (0, 0)."""
        sens = SensitivityAnalysis(
            engineering={
                "weird_zero": SensitivityEntry(elasticity=0.1, baseline=0.0),
            },
            financial={},
        )
        meta = generate_parameter_metadata(sens)
        assert "weird_zero" in meta
        lo, hi = meta["weird_zero"].range
        assert lo < hi  # Non-degenerate
        assert lo >= 0

    def test_empty_sensitivities(self) -> None:
        sens = SensitivityAnalysis(engineering={}, financial={})
        assert generate_parameter_metadata(sens) == {}

    def test_non_fractional_with_subunit_baseline(self) -> None:
        """Param with baseline in (0,1] but no fractional name → no [0,1] clamp."""
        sens = SensitivityAnalysis(
            engineering={},
            financial={
                # interest_rate baseline 0.9 → range (0.63, 1.17), no clamp
                "interest_rate": SensitivityEntry(elasticity=0.5, baseline=0.9),
            },
        )
        meta = generate_parameter_metadata(sens)
        assert meta["interest_rate"].range == pytest.approx((0.63, 1.17))


# ---------------------------------------------------------------------------
# AC-8: --concept filter writes only matching concept
# ---------------------------------------------------------------------------


class TestConceptFilter:
    def test_filters_to_single_concept(self, tmp_path: Path) -> None:
        """AC-8: --concept 01 writes only data/01.json."""
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        data_dir = tmp_path / "data"

        _make_concept_dir(analyses_dir, concept_id="01", with_model_setup=False)
        _make_concept_dir(analyses_dir, concept_id="04", with_model_setup=False)

        mock_module = types.SimpleNamespace()

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            run_extraction(
                analyses_dir=analyses_dir,
                data_dir=data_dir,
                concept_filter=["01"],
                skip_narrative=True,
            )

        assert (data_dir / "01.json").exists()
        assert not (data_dir / "04.json").exists()
        # Extraction no longer writes manifest.json — the contract is just
        # "filtered run only writes matching per-concept JSONs".
        assert not (data_dir / "manifest.json").exists()
        assert not (data_dir / "parameter_index.json").exists()

    def test_multiple_concept_filter(self, tmp_path: Path) -> None:
        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        data_dir = tmp_path / "data"

        for cid in ["01", "04", "07"]:
            _make_concept_dir(analyses_dir, concept_id=cid, with_model_setup=False)

        mock_module = types.SimpleNamespace()

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            run_extraction(
                analyses_dir=analyses_dir,
                data_dir=data_dir,
                concept_filter=["01", "07"],
                skip_narrative=True,
            )

        assert (data_dir / "01.json").exists()
        assert not (data_dir / "04.json").exists()
        assert (data_dir / "07.json").exists()

    def test_filtered_extraction_preserves_other_concepts(self, tmp_path: Path) -> None:
        """AC-4 regression: filtered re-extraction must not hide existing concepts.

        Pre-populate data/ with 01.json…05.json, then re-extract only "01".
        After server-startup _load_data() runs, all 5 concepts must remain
        visible. (Before this work, extraction overwrote manifest.json with
        a single-entry manifest, hiding 02–05 from the UI.)
        """
        from exploration.concept_explorer.server import _load_data

        analyses_dir = tmp_path / "analyses"
        analyses_dir.mkdir()
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        # Pre-populate with five existing per-concept JSONs.
        for cid in ["01", "02", "03", "04", "05"]:
            placeholder = ConceptData(
                concept_id=cid,
                name=f"Pre-existing {cid}",
                confinement_family=ConfinementFamily.MFE,
                status=ConceptStatus.IN_PROGRESS,
                has_cost_model=False,
                has_sensitivities=False,
                sources=SourcePaths(),
            )
            (data_dir / f"{cid}.json").write_text(placeholder.model_dump_json())

        # Set up only the "01" analyses dir so the filter has something to extract.
        _make_concept_dir(analyses_dir, concept_id="01", with_model_setup=False)
        mock_module = types.SimpleNamespace()

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            run_extraction(
                analyses_dir=analyses_dir,
                data_dir=data_dir,
                concept_filter=["01"],
                skip_narrative=True,
            )

        # All five per-concept JSONs are still on disk.
        for cid in ["01", "02", "03", "04", "05"]:
            assert (data_dir / f"{cid}.json").exists()

        # And the server's startup-computed manifest sees all five.
        concepts, manifest, _ = _load_data(data_dir)
        assert set(concepts.keys()) == {"01", "02", "03", "04", "05"}
        assert {e.concept_id for e in manifest.concepts} == {"01", "02", "03", "04", "05"}


# ---------------------------------------------------------------------------
# Discover concepts
# ---------------------------------------------------------------------------


class TestDiscoverConcepts:
    def test_finds_dirs_with_analysis_or_model_setup(self, tmp_path: Path) -> None:
        (tmp_path / "04-has-model").mkdir()
        (tmp_path / "04-has-model" / "model_setup.py").write_text("")

        (tmp_path / "01-has-analysis").mkdir()
        (tmp_path / "01-has-analysis" / "analysis.md").write_text("---\n---\n")

        (tmp_path / "10-empty").mkdir()  # neither file — should be skipped

        dirs = discover_concepts(tmp_path, concept_filter=None)
        names = {d.name for d in dirs}
        assert "04-has-model" in names
        assert "01-has-analysis" in names
        assert "10-empty" not in names

    def test_filter_excludes_non_matching(self, tmp_path: Path) -> None:
        for cid in ["01", "04", "07"]:
            d = tmp_path / f"{cid}-concept"
            d.mkdir()
            (d / "analysis.md").write_text("---\n---\n")

        dirs = discover_concepts(tmp_path, concept_filter=["01"])
        assert len(dirs) == 1
        assert parse_concept_id(dirs[0].name) == "01"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_minimal_cost_model_dict() -> dict[str, Any]:
    """Return a nested dict matching the to_explorer_dict() contract.

    This is the format real freeform scripts produce — nested under
    "costs", "power_table", "cas22_detail", "params", "overridden".
    CostModelData.from_forward_result() unpacks this into the flat model.
    """
    return {
        "costs": {
            "cas10": 0.0, "cas21": 0.0, "cas22": 100.0, "cas23": 0.0,
            "cas24": 0.0, "cas25": 0.0, "cas26": 0.0, "cas27": 0.0,
            "cas28": 0.0, "cas29": 0.0, "cas30": 0.0, "cas40": 0.0,
            "cas50": 0.0, "cas60": 0.0, "cas70": 0.0, "cas80": 0.0,
            "cas90": 0.0,
            "total_capital": 100.0,
            "lcoe": 80.0,
            "overnight_cost": 6000.0,
        },
        "power_table": {
            "p_net": 500.0,
            "q_eng": 5.0,
            "capacity_factor": 0.8,
        },
        "cas22_detail": {k: 0.0 for k in CostModelData.CAS22_NAMES},
        "params": {},
        "overridden": [],
    }


def _make_three_concepts() -> list[ConceptData]:
    """Build three minimal ConceptData objects: one standalone, two with cost models."""
    zero_cas = CASAccount(name="zero", cost_m_usd=0.0)
    cas22_detail = {k: CASAccount(name=k, cost_m_usd=0.0) for k in CostModelData.CAS22_NAMES}

    def _cost_with_sens() -> CostModelData:
        return CostModelData(
            cas10=zero_cas,
            cas21=zero_cas,
            cas22=CASAccount(name="RPE", cost_m_usd=200.0),
            cas23=zero_cas,
            cas24=zero_cas,
            cas25=zero_cas,
            cas26=zero_cas,
            cas27=zero_cas,
            cas28=zero_cas,
            cas29=zero_cas,
            cas30=zero_cas,
            cas40=zero_cas,
            cas50=zero_cas,
            cas60=zero_cas,
            cas70=zero_cas,
            cas80=zero_cas,
            cas90=zero_cas,
            cas22_detail=cas22_detail,
            headline={  # type: ignore[arg-type]
                "lcoe_per_mwh": 75.0,
                "overnight_cost_per_kw": 5000.0,
                "p_net_mw": 1000.0,
                "q_eng": 8.0,
                "capacity_factor": 0.85,
            },
            sensitivities=SensitivityAnalysis(
                engineering={
                    "availability": SensitivityEntry(elasticity=0.75, baseline=0.85),
                    "thermal_efficiency": SensitivityEntry(elasticity=-0.42, baseline=0.35),
                },
                financial={
                    "interest_rate": SensitivityEntry(elasticity=0.85, baseline=0.07),
                },
            ),
        )

    def _make(concept_id: str, name: str, has_cost: bool) -> ConceptData:
        cost = _cost_with_sens() if has_cost else None
        return ConceptData(
            concept_id=concept_id,
            name=name,
            confinement_family=ConfinementFamily.IFE,
            company="Test Corp",
            status=ConceptStatus.APPROVED,
            has_cost_model=has_cost,
            has_sensitivities=has_cost,
            cost_model=cost,
            sources=SourcePaths(),
        )

    return [
        _make("01", "Standalone A", has_cost=False),
        _make("04", "Costingfe B", has_cost=True),
        _make("07", "Standalone C", has_cost=False),
    ]


# ---------------------------------------------------------------------------
# Omit list enforcement (Consumer #1: extraction) — FR-3, FR-6, I-2
# ---------------------------------------------------------------------------


class TestOmitListExtraction:
    """The extractor honors the omit list independently of the server (FR-6)."""

    def test_discover_concepts_excludes_omitted(self, tmp_path: Path) -> None:
        """FR-3: omitted IDs are dropped from the discovered set; others remain."""
        analyses = tmp_path / "analyses"
        analyses.mkdir()
        _make_concept_dir(analyses, concept_id="05", with_model_setup=False, with_analysis=True)
        _make_concept_dir(analyses, concept_id="27", with_model_setup=False, with_analysis=True)

        ids = [parse_concept_id(d.name) for d in discover_concepts(analyses, None, {"27"})]

        assert "05" in ids
        assert "27" not in ids

    def test_discover_concepts_none_omit_keeps_all(self, tmp_path: Path) -> None:
        """omitted=None means omit nothing (used to report the unfiltered set)."""
        analyses = tmp_path / "analyses"
        analyses.mkdir()
        _make_concept_dir(analyses, concept_id="05", with_model_setup=False, with_analysis=True)
        _make_concept_dir(analyses, concept_id="27", with_model_setup=False, with_analysis=True)

        ids = {parse_concept_id(d.name) for d in discover_concepts(analyses, None, None)}

        assert ids == {"05", "27"}

    def test_run_extraction_does_not_write_omitted_data_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """I-2/FR-3: no data/{id}.json is written for an omitted concept, while a
        non-omitted concept still extracts; the omitted concept is reported."""
        analyses = tmp_path / "analyses"
        analyses.mkdir()
        for cid in ("05", "27"):
            cdir = _make_concept_dir(
                analyses, concept_id=cid, with_model_setup=False, with_analysis=True
            )
            # Freeform model_setup.py → standalone pathway (no costingfe import)
            (cdir / "model_setup.py").write_text(
                "params = None\ndef to_explorer_dict(): return {}\n", encoding="utf-8"
            )

        # Isolate from the real omit_list.yaml — omit only 27 for this test.
        monkeypatch.setattr(
            "exploration.concept_explorer.extract_explorer_data.load_omit_list",
            lambda: {"27"},
        )

        valid_cost_model = _build_minimal_cost_model_dict()
        mock_module = types.SimpleNamespace(to_explorer_dict=lambda: valid_cost_model)

        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            run_extraction(
                analyses_dir=analyses,
                data_dir=tmp_path / "data",
                skip_narrative=True,
            )

        data_dir = tmp_path / "data"
        assert (data_dir / "05.json").exists()  # non-omitted still extracted
        assert not (data_dir / "27.json").exists()  # omitted: never written (I-2)

        # FR-3: the omitted concept is surfaced in the run's skipped report.
        out = capsys.readouterr().out
        assert "27" in out
        assert "omit_list" in out

    def test_run_extraction_does_not_refresh_existing_omitted_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """I-2: a pre-existing stale data/{id}.json for an omitted concept is left
        untouched (not refreshed/overwritten) by extraction."""
        analyses = tmp_path / "analyses"
        analyses.mkdir()
        cdir = _make_concept_dir(
            analyses, concept_id="27", with_model_setup=False, with_analysis=True
        )
        (cdir / "model_setup.py").write_text(
            "params = None\ndef to_explorer_dict(): return {}\n", encoding="utf-8"
        )

        data_dir = tmp_path / "data"
        data_dir.mkdir()
        stale = data_dir / "27.json"
        stale.write_text('{"stale": "sentinel"}', encoding="utf-8")

        monkeypatch.setattr(
            "exploration.concept_explorer.extract_explorer_data.load_omit_list",
            lambda: {"27"},
        )

        run_extraction(
            analyses_dir=analyses,
            data_dir=data_dir,
            skip_narrative=True,
        )

        # Untouched — still the stale sentinel, not a regenerated ConceptData.
        assert stale.read_text(encoding="utf-8") == '{"stale": "sentinel"}'


class TestOverrideRecords:
    """Item 2 / FR-1, FR-5, FR-6: the full override registry is carried through."""

    def test_resolve_account_name_top_level_and_sub(self) -> None:
        # Top-level codes are authored upper-case but the map keys are lower.
        assert _resolve_account_name("CAS27") == "Special Materials"
        # CAS22 sub-account codes resolve from the CAS22 map.
        assert _resolve_account_name("C220103") == "Magnets / Coils"
        # Unknown codes fall back to the bare code (visible, not blank).
        assert _resolve_account_name("C999999") == "C999999"

    def test_build_records_carries_all_fields(self) -> None:
        raw = [
            {
                "account": "C220103", "value": 1030.0, "enabled": True,
                "provenance": "derived", "source": "src §6", "rationale": "why",
                "cost_basis": "noak",
            },
            {
                "account": "CAS27", "value": 183.0, "enabled": False,
                "provenance": "derived", "source": "src §6", "rationale": "why2",
                "cost_basis": "noak", "blocked_by": "1cFE/1costingfe#103",
            },
        ]
        recs = _build_override_records(raw)
        assert [r.account for r in recs] == ["C220103", "CAS27"]
        assert recs[0].account_name == "Magnets / Coils"
        assert recs[0].enabled is True
        assert recs[0].blocked_by is None
        # FR-5: disabled entry carried with its blocked_by reference.
        assert recs[1].enabled is False
        assert recs[1].blocked_by == "1cFE/1costingfe#103"

    def test_missing_field_is_none_not_empty(self) -> None:
        """FR-6: an absent narrative field is None (panel renders 'not recorded'),
        never coerced to ''."""
        recs = _build_override_records(
            [{"account": "CAS27", "value": 5.0, "enabled": True}]
        )
        assert recs[0].source is None
        assert recs[0].rationale is None
        assert recs[0].cost_basis is None

    def test_extract_costingfe_emits_records(self, tmp_path: Path) -> None:
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        overrides = [
            {"account": "C220103", "value": 1030.0, "enabled": True,
             "provenance": "derived", "source": "s", "rationale": "r", "cost_basis": "noak"},
            {"account": "CAS27", "value": 183.0, "enabled": False,
             "provenance": "derived", "source": "s", "rationale": "r",
             "cost_basis": "noak", "blocked_by": "1cFE/1costingfe#103"},
        ]
        mock_module = types.SimpleNamespace(
            model=model, result_1gw=result, overrides=overrides,
        )
        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="01",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )
        # Count is enabled-only; records carry both enabled and disabled.
        assert concept.analyst_override_count == 1
        assert len(concept.overrides) == 2
        disabled = [o for o in concept.overrides if not o.enabled]
        assert len(disabled) == 1
        assert disabled[0].account == "CAS27"
        assert disabled[0].blocked_by == "1cFE/1costingfe#103"

    def test_no_overrides_means_empty_list(self, tmp_path: Path) -> None:
        result = _make_forward_result()
        model = _make_mock_model()
        concept_dir = _make_concept_dir(tmp_path)
        mock_module = types.SimpleNamespace(model=model, result_1gw=result)
        with patch(
            "exploration.concept_explorer.extract_explorer_data.load_module_from_path",
            return_value=mock_module,
        ):
            concept = extract_costingfe(
                concept_dir=concept_dir,
                concept_id="04",
                frontmatter={"Concept": "Test", "Status": "approved"},
                analysis_path=concept_dir / "analysis.md",
                narrative=None,
                param_metadata={},
            )
        assert concept.overrides == []
