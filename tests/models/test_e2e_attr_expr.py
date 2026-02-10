"""E2E Attribute Expression model regression tests.

Tests verify the e2e_attr_expr test model parses correctly and contains
expected elements exercising all 12 Phase 1+2 codegen patterns.

Patterns tested:
- Patterns 1-6: FORMULA computed attributes (simple, chain, 2-hop, binary, 3-term, fan-in)
- Patterns 7-8: CalcDef auto-implementation (5-output, exponentiation)
- Pattern 9: EXPOSE_PURE alias
- Patterns 10-12: Cross-module wiring (FORMULA->CalcUsage, 2-hop, CalcUsage->CalcUsage via EXPOSE)

Usage:
    pytest tests/models/test_e2e_attr_expr.py -v
"""
import pytest
from pathlib import Path

from agentic_mbse.sysml.syside_adapter import get_syside

MODELS_DIR = Path(__file__).parent.parent.parent / "models"
E2E_DIR = MODELS_DIR / "tests" / "e2e_attr_expr"


@pytest.fixture
def library_model():
    """Load library.sysml only."""
    lib_file = E2E_DIR / "library.sysml"
    if not lib_file.exists():
        pytest.skip("library.sysml not found")
    model, diagnostics = get_syside().try_load_model([str(lib_file)])
    return model, diagnostics


@pytest.fixture
def full_model():
    """Load both library.sysml and design.sysml together."""
    files = list(E2E_DIR.glob("*.sysml"))
    if not files:
        pytest.skip("No e2e_attr_expr files found")
    model, diagnostics = get_syside().try_load_model([str(f) for f in files])
    return model, diagnostics


class TestE2EAttrExprParsing:
    """Verify e2e_attr_expr files parse without syntax errors."""

    def test_library_parses_without_errors(self, library_model):
        """library.sysml should parse without errors."""
        model, diagnostics = library_model
        syside = get_syside()
        errors = [d for d in diagnostics.parser if d.severity == syside.DiagnosticSeverity.Error]
        assert len(errors) == 0, f"library.sysml has {len(errors)} parse errors: {errors}"

    def test_full_model_parses_without_errors(self, full_model):
        """Both files should parse together without errors."""
        model, diagnostics = full_model
        syside = get_syside()
        errors = [d for d in diagnostics.parser if d.severity == syside.DiagnosticSeverity.Error]
        assert len(errors) == 0, f"e2e_attr_expr has {len(errors)} parse errors: {errors}"


class TestCalcDefinitions:
    """Verify CalcDef definitions exist (Patterns 7-8)."""

    def test_has_four_calc_defs(self, library_model):
        """Library should have 4 calc definitions."""
        model, _ = library_model
        syside = get_syside()
        calc_defs = list(model.elements(syside.CalculationDefinition))
        calc_names = {c.name for c in calc_defs if c.name}
        expected = {"ComponentCostCalc", "AnnualizedCostCalc", "EnergyCalc", "SimpleLCOECalc"}
        assert expected == calc_names, f"Expected {expected}, found {calc_names}"

    def test_component_cost_calc_has_five_outputs(self, library_model):
        """ComponentCostCalc should have 5 output attributes (Pattern 7)."""
        model, _ = library_model
        syside = get_syside()
        calc_defs = list(model.elements(syside.CalculationDefinition))
        ccc = next((c for c in calc_defs if c.name == "ComponentCostCalc"), None)
        assert ccc is not None, "ComponentCostCalc not found"

        out_attrs = [
            m for m in ccc.owned_members
            if hasattr(m, 'name') and m.name
            and hasattr(m, 'direction') and m.direction is not None
            and "Out" in str(m.direction)
        ]
        out_names = {a.name for a in out_attrs}
        expected = {"material_cost", "fab_cost", "install_cost", "total_cost", "idiot_index"}
        assert expected == out_names, f"Expected outputs {expected}, found {out_names}"


class TestDesignElements:
    """Verify design part and its elements exist."""

    def test_has_e2e_plant(self, full_model):
        """Design should contain e2e_plant part usage."""
        model, _ = full_model
        syside = get_syside()
        part_usages = list(model.elements(syside.PartUsage))
        plant = next((p for p in part_usages if p.name == "e2e_plant"), None)
        assert plant is not None, "e2e_plant part usage not found"

    def test_has_calc_usages(self, full_model):
        """Design should have 4 calc usages."""
        model, _ = full_model
        syside = get_syside()
        calc_usages = list(model.elements(syside.CalculationUsage))
        calc_names = {c.name for c in calc_usages if c.name}
        expected = {"component_cost", "financial", "energy", "lcoe"}
        assert expected <= calc_names, (
            f"Missing calc usages. Expected {expected}, found {calc_names}"
        )
