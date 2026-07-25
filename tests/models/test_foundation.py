"""Foundation package regression tests.

Tests verify the foundation library (types, units, materials) exists,
parses correctly, and contains expected elements per spec requirements.

Requirements tested:
- MR-001: 13 enum definitions in types.sysml
- MR-002: Placeholder enum variants included
- MR-003: 6 custom units/types in units.sysml
- MR-004: 12 material part definitions in materials.sysml
- MR-005: Materials have required attributes (density, thermal_conductivity, unit_cost)
- MR-007: All files parse without errors
- MR-009: Enum variant names match PyFECONS exactly

Usage:
    pytest tests/models/test_foundation.py -v
"""
import pytest
from pathlib import Path

from agentic_mbse.sysml.syside_adapter import get_syside

# Path to models directory
MODELS_DIR = Path(__file__).parent.parent.parent / "models"
FOUNDATION_DIR = MODELS_DIR / "library" / "foundation"


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def types_model():
    """Load types.sysml only."""
    types_file = FOUNDATION_DIR / "types.sysml"
    if not types_file.exists():
        pytest.skip("types.sysml not found")

    model, diagnostics = get_syside().try_load_model([str(types_file)])
    return model, diagnostics


@pytest.fixture
def units_model():
    """Load units.sysml only."""
    units_file = FOUNDATION_DIR / "units.sysml"
    if not units_file.exists():
        pytest.skip("units.sysml not found")

    model, diagnostics = get_syside().try_load_model([str(units_file)])
    return model, diagnostics


@pytest.fixture
def materials_model():
    """Load materials.sysml only."""
    materials_file = FOUNDATION_DIR / "materials.sysml"
    if not materials_file.exists():
        pytest.skip("materials.sysml not found")

    model, diagnostics = get_syside().try_load_model([str(materials_file)])
    return model, diagnostics


@pytest.fixture
def foundation_model():
    """Load all foundation files together."""
    files = list(FOUNDATION_DIR.glob("*.sysml"))
    if not files:
        pytest.skip("No foundation files found")

    model, diagnostics = get_syside().try_load_model([str(f) for f in files])
    return model, diagnostics


# ============================================================================
# Parse Tests (MR-007)
# ============================================================================


class TestFoundationParsing:
    """Verify foundation files parse without syntax errors."""

    def test_foundation_types_parse_without_errors(self, types_model):
        """types.sysml should parse without errors."""
        model, diagnostics = types_model
        syside = get_syside()

        errors = [d for d in diagnostics.parser if d.severity == syside.DiagnosticSeverity.Error]
        assert len(errors) == 0, f"types.sysml has {len(errors)} parse errors: {errors}"

    def test_foundation_units_parse_without_errors(self, units_model):
        """units.sysml should parse without errors."""
        model, diagnostics = units_model
        syside = get_syside()

        errors = [d for d in diagnostics.parser if d.severity == syside.DiagnosticSeverity.Error]
        assert len(errors) == 0, f"units.sysml has {len(errors)} parse errors: {errors}"

    def test_foundation_materials_parse_without_errors(self, materials_model):
        """materials.sysml should parse without errors."""
        model, diagnostics = materials_model
        syside = get_syside()

        errors = [d for d in diagnostics.parser if d.severity == syside.DiagnosticSeverity.Error]
        assert len(errors) == 0, f"materials.sysml has {len(errors)} parse errors: {errors}"


# ============================================================================
# Enum Tests (MR-001, MR-002, MR-009)
# ============================================================================


class TestEnumDefinitions:
    """Verify enum definitions exist with correct structure."""

    def test_enum_definitions_count(self, types_model):
        """types.sysml should have at least 13 enum definitions."""
        model, _ = types_model
        syside = get_syside()

        enum_defs = list(model.elements(syside.EnumerationDefinition))
        assert len(enum_defs) >= 13, (
            f"Expected >= 13 enum definitions, found {len(enum_defs)}. "
            f"Found: {[e.name for e in enum_defs]}"
        )

    def test_reactor_type_variants(self, types_model):
        """ReactorType should have variants: MFE, IFE, MIF."""
        model, _ = types_model
        syside = get_syside()

        enum_defs = list(model.elements(syside.EnumerationDefinition))
        reactor_type = next((e for e in enum_defs if e.name == "ReactorType"), None)

        assert reactor_type is not None, "ReactorType enum not found"

        # Get variant names
        variant_names = {v.name for v in reactor_type.owned_members if hasattr(v, 'name') and v.name}

        expected = {"MFE", "IFE", "MIF"}
        assert expected <= variant_names, (
            f"ReactorType missing expected variants. "
            f"Expected: {expected}, Found: {variant_names}"
        )

    def test_confinement_type_variants_count(self, types_model):
        """ConfinementType should have at least 12 variants (3 active + 9 placeholder)."""
        model, _ = types_model
        syside = get_syside()

        enum_defs = list(model.elements(syside.EnumerationDefinition))
        confinement_type = next((e for e in enum_defs if e.name == "ConfinementType"), None)

        assert confinement_type is not None, "ConfinementType enum not found"

        # Count variants (EnumerationUsage members)
        variants = [v for v in confinement_type.owned_members if hasattr(v, 'name') and v.name]
        assert len(variants) >= 12, (
            f"ConfinementType should have >= 12 variants, found {len(variants)}. "
            f"Variants: {[v.name for v in variants]}"
        )

    def test_all_expected_enums_exist(self, types_model):
        """All 13 expected enum definitions should exist."""
        model, _ = types_model
        syside = get_syside()

        enum_defs = list(model.elements(syside.EnumerationDefinition))
        enum_names = {e.name for e in enum_defs if e.name}

        expected_enums = {
            "ReactorType",
            "ConfinementType",
            "EnergyConversion",
            "FuelType",
            "BlanketFirstWall",
            "BlanketType",
            "BlanketPrimaryCoolant",
            "BlanketSecondaryCoolant",
            "BlanketNeutronMultiplier",
            "BlanketStructure",
            "StructurePga",
            "MagnetType",
            "MagnetMaterialType",
        }

        missing = expected_enums - enum_names
        assert not missing, f"Missing enum definitions: {missing}"


# ============================================================================
# Custom Units Tests (MR-003)
# ============================================================================


class TestCustomUnits:
    """Verify custom unit/type definitions exist."""

    def test_custom_units_defined(self, units_model):
        """units.sysml should define M_USD, USD_KG, USD_M3, USD_W, Percent, Ratio."""
        model, _ = units_model
        syside = get_syside()

        attr_defs = list(model.elements(syside.AttributeDefinition))
        attr_names = {a.name for a in attr_defs if a.name}

        expected_units = {"M_USD", "USD_KG", "USD_M3", "USD_W", "Percent", "Ratio"}
        missing = expected_units - attr_names

        assert not missing, (
            f"Missing custom unit definitions: {missing}. "
            f"Found: {attr_names}"
        )

    def test_custom_units_count(self, units_model):
        """units.sysml should have at least 6 custom attribute definitions."""
        model, _ = units_model
        syside = get_syside()

        attr_defs = list(model.elements(syside.AttributeDefinition))
        assert len(attr_defs) >= 6, (
            f"Expected >= 6 attribute definitions, found {len(attr_defs)}. "
            f"Found: {[a.name for a in attr_defs]}"
        )


# ============================================================================
# Materials Tests (MR-004, MR-005)
# ============================================================================


class TestMaterialDefinitions:
    """Verify material part definitions exist with required attributes."""

    def test_materials_exist(self, materials_model):
        """materials.sysml should have at least 10 part definitions."""
        model, _ = materials_model
        syside = get_syside()

        part_defs = list(model.elements(syside.PartDefinition))
        assert len(part_defs) >= 10, (
            f"Expected >= 10 material part definitions, found {len(part_defs)}. "
            f"Found: {[p.name for p in part_defs]}"
        )

    def test_material_has_required_attributes(self, materials_model):
        """Tungsten material should have density, thermal_conductivity, unit_cost."""
        model, _ = materials_model
        syside = get_syside()

        part_defs = list(model.elements(syside.PartDefinition))
        tungsten = next((p for p in part_defs if p.name == "Tungsten"), None)

        assert tungsten is not None, "Tungsten material not found"

        # Get attribute names from owned members
        attr_names = set()
        for member in tungsten.owned_members:
            if hasattr(member, 'name') and member.name:
                attr_names.add(member.name)

        expected_attrs = {"density", "thermal_conductivity", "unit_cost"}
        missing = expected_attrs - attr_names

        assert not missing, (
            f"Tungsten missing required attributes: {missing}. "
            f"Found: {attr_names}"
        )

    def test_all_materials_have_required_attributes(self, materials_model):
        """All materials should have density, thermal_conductivity, unit_cost."""
        model, _ = materials_model
        syside = get_syside()

        part_defs = list(model.elements(syside.PartDefinition))
        required_attrs = {"density", "thermal_conductivity", "unit_cost"}

        materials_missing_attrs = []
        for part_def in part_defs:
            attr_names = {
                m.name for m in part_def.owned_members
                if hasattr(m, 'name') and m.name
            }
            missing = required_attrs - attr_names
            if missing:
                materials_missing_attrs.append((part_def.name, missing))

        assert not materials_missing_attrs, (
            f"Materials missing required attributes: {materials_missing_attrs}"
        )


# ============================================================================
# Integration Tests
# ============================================================================


class TestFoundationIntegration:
    """Verify all foundation files work together."""

    def test_all_foundation_files_parse_together(self, foundation_model):
        """All foundation files should parse together without errors."""
        model, diagnostics = foundation_model
        syside = get_syside()

        errors = [d for d in diagnostics.parser if d.severity == syside.DiagnosticSeverity.Error]
        assert len(errors) == 0, f"Foundation has {len(errors)} parse errors: {errors}"

    def test_foundation_element_counts(self, foundation_model):
        """Foundation should contain its core concept-agnostic definitions.

        The foundation library was slimmed to the shared base interfaces
        (WI-006+): the 'Costed Component' part def, the 'Economic Parameter'
        attribute def, and the 'CAS Scope' enum. The old types/units/materials
        files (13 enums, 6 units, 12 materials) were removed. Assert the
        current definitions are present rather than the stale counts.
        """
        model, _ = foundation_model
        syside = get_syside()

        enum_names = {e.name for e in model.elements(syside.EnumerationDefinition) if e.name}
        attr_names = {a.name for a in model.elements(syside.AttributeDefinition) if a.name}
        part_names = {p.name for p in model.elements(syside.PartDefinition) if p.name}

        assert "CAS Scope" in enum_names, \
            f"Expected 'CAS Scope' enum def, found {enum_names}"
        assert "Economic Parameter" in attr_names, \
            f"Expected 'Economic Parameter' attribute def, found {attr_names}"
        assert "Costed Component" in part_names, \
            f"Expected 'Costed Component' part def, found {part_names}"
