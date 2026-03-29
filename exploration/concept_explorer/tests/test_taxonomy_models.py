"""Tests for taxonomy data models and seed script output.

Coverage:
- ConceptTaxonomy round-trip serialization
- Hierarchy validator (rejects invalid combinations)
- TBD vs None (N/A) vs actual value handling
- ConceptRegistry loading, by_id, by_family
- Decision tree structure
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from exploration.concept_explorer.models import ConfinementFamily, FuelType
from exploration.concept_explorer.taxonomy_models import (
    ConceptRegistry,
    ConceptTaxonomy,
    EnergyCapture,
    IFEDriver,
    LaserApproach,
    MagnetType,
    MFETopology,
    OperationMode,
    PlasmaState,
    PrimaryHeating,
    TaxonomyConfidence,
    TokamakShape,
    TritiumBreeding,
)

# Paths to seeded JSON files (Phase 1 output)
_DATA_DIR = Path(__file__).parent.parent / "data"
REGISTRY_PATH = _DATA_DIR / "concept_registry.json"
TREE_PATH = _DATA_DIR / "decision_tree.json"


# ---------------------------------------------------------------------------
# Model unit tests (no dependency on seeded data)
# ---------------------------------------------------------------------------


class TestConceptTaxonomyModel:
    def test_round_trip(self):
        """A hand-built ConceptTaxonomy serializes to JSON and back."""
        concept = ConceptTaxonomy(
            concept_id="hts-compact-tokamak",
            name="HTS Compact Tokamak",
            company="Commonwealth Fusion Systems",
            confinement_family=ConfinementFamily.MFE,
            mfe_topology=MFETopology.TOKAMAK,
            tokamak_shape=TokamakShape.COMPACT,
            fuel=FuelType.DT,
            primary_heating=PrimaryHeating.RF_ICRH,
            energy_capture=EnergyCapture.THERMAL_STEAM,
            plasma_state=PlasmaState.BURNING,
            magnet_type=MagnetType.HTS_WOUND,
            tritium_breeding=TritiumBreeding.FLIBE_BLANKET,
            operation_mode=OperationMode.QUASI_STEADY,
            confidence=TaxonomyConfidence.HIGH,
        )
        data = concept.model_dump(mode="json")
        assert data["tokamak_shape"] == "Compact"
        assert data["ife_driver"] is None  # N/A fields serialize as null
        rebuilt = ConceptTaxonomy.model_validate(data)
        assert rebuilt == concept

    def test_hierarchy_validator_rejects_mfe_with_ife_driver(self):
        """MFE concept with ife_driver set should fail validation."""
        with pytest.raises(ValidationError):
            ConceptTaxonomy(
                concept_id="bad",
                name="Bad",
                confinement_family=ConfinementFamily.MFE,
                mfe_topology=MFETopology.TOKAMAK,
                ife_driver=IFEDriver.LASER,  # Invalid for MFE!
                fuel=FuelType.DT,
                operation_mode=OperationMode.STEADY_STATE,
                confidence=TaxonomyConfidence.MEDIUM,
            )

    def test_hierarchy_validator_rejects_ife_with_mfe_topology(self):
        """IFE concept with mfe_topology set should fail validation."""
        with pytest.raises(ValidationError):
            ConceptTaxonomy(
                concept_id="bad",
                name="Bad",
                confinement_family=ConfinementFamily.IFE,
                ife_driver=IFEDriver.LASER,
                mfe_topology=MFETopology.TOKAMAK,  # Invalid for IFE!
                fuel=FuelType.DT,
                operation_mode=OperationMode.PULSED,
                confidence=TaxonomyConfidence.MEDIUM,
            )

    def test_hierarchy_validator_requires_mfe_topology(self):
        """MFE concept without mfe_topology should fail validation."""
        with pytest.raises(ValidationError):
            ConceptTaxonomy(
                concept_id="bad",
                name="Bad",
                confinement_family=ConfinementFamily.MFE,
                # Missing mfe_topology!
                fuel=FuelType.DT,
                operation_mode=OperationMode.STEADY_STATE,
                confidence=TaxonomyConfidence.MEDIUM,
            )

    def test_hierarchy_validator_requires_ife_driver(self):
        """IFE concept without ife_driver should fail validation."""
        with pytest.raises(ValidationError):
            ConceptTaxonomy(
                concept_id="bad",
                name="Bad",
                confinement_family=ConfinementFamily.IFE,
                # Missing ife_driver!
                fuel=FuelType.DT,
                operation_mode=OperationMode.PULSED,
                confidence=TaxonomyConfidence.MEDIUM,
            )

    def test_tbd_values_serialize_as_strings(self):
        """TBD enum members serialize as 'TBD', not null."""
        concept = ConceptTaxonomy(
            concept_id="test",
            name="Test",
            confinement_family=ConfinementFamily.MFE,
            mfe_topology=MFETopology.TOKAMAK,
            fuel=FuelType.DT,
            magnet_type=MagnetType.TBD,
            operation_mode=OperationMode.STEADY_STATE,
            confidence=TaxonomyConfidence.MEDIUM,
        )
        data = concept.model_dump(mode="json")
        assert data["magnet_type"] == "TBD"  # String, not null

    def test_na_fields_serialize_as_null(self):
        """Optional fields left as None serialize as null in JSON."""
        concept = ConceptTaxonomy(
            concept_id="test",
            name="Test",
            confinement_family=ConfinementFamily.MFE,
            mfe_topology=MFETopology.TOKAMAK,
            fuel=FuelType.DT,
            operation_mode=OperationMode.STEADY_STATE,
            confidence=TaxonomyConfidence.MEDIUM,
        )
        data = concept.model_dump(mode="json")
        assert data["ife_driver"] is None
        assert data["laser_approach"] is None
        assert data["repetition_rate"] is None

    def test_tokamak_shape_only_for_tokamaks(self):
        """tokamak_shape set on a non-Tokamak MFE should fail."""
        with pytest.raises(ValidationError):
            ConceptTaxonomy(
                concept_id="bad",
                name="Bad",
                confinement_family=ConfinementFamily.MFE,
                mfe_topology=MFETopology.STELLARATOR,
                tokamak_shape=TokamakShape.COMPACT,  # Invalid for stellarator!
                fuel=FuelType.DT,
                operation_mode=OperationMode.STEADY_STATE,
                confidence=TaxonomyConfidence.MEDIUM,
            )

    def test_laser_approach_only_for_laser_ife(self):
        """laser_approach set on a non-Laser IFE should fail."""
        with pytest.raises(ValidationError):
            ConceptTaxonomy(
                concept_id="bad",
                name="Bad",
                confinement_family=ConfinementFamily.IFE,
                ife_driver=IFEDriver.PROJECTILE,
                laser_approach=LaserApproach.FAST_IGNITION,  # Invalid!
                fuel=FuelType.DT,
                operation_mode=OperationMode.PULSED,
                confidence=TaxonomyConfidence.MEDIUM,
            )


# ---------------------------------------------------------------------------
# Seeded data tests (depend on seed_registry.py having been run)
# ---------------------------------------------------------------------------


@pytest.fixture
def registry() -> ConceptRegistry:
    """Load the seeded concept registry."""
    assert REGISTRY_PATH.exists(), (
        f"Registry not found at {REGISTRY_PATH}. Run seed_registry.py first."
    )
    return ConceptRegistry.model_validate_json(REGISTRY_PATH.read_text())


@pytest.fixture
def tree() -> dict:
    """Load the seeded decision tree."""
    assert TREE_PATH.exists(), (
        f"Decision tree not found at {TREE_PATH}. Run seed_registry.py first."
    )
    return json.loads(TREE_PATH.read_text())


class TestConceptRegistry:
    def test_loads_all_38_concepts(self, registry: ConceptRegistry):
        """The seeded registry JSON loads and validates all 38 concepts."""
        assert len(registry.concepts) == 38
        ids = [c.concept_id for c in registry.concepts]
        assert len(set(ids)) == 38  # All unique

    def test_by_id(self, registry: ConceptRegistry):
        """by_id returns correct concept or None."""
        concept = registry.by_id("hts-compact-tokamak")
        assert concept is not None
        assert concept.name == "HTS Compact Tokamak"
        assert registry.by_id("nonexistent") is None

    def test_by_family(self, registry: ConceptRegistry):
        """by_family filters correctly."""
        mfe = registry.by_family(ConfinementFamily.MFE)
        assert len(mfe) > 0
        assert all(c.confinement_family == ConfinementFamily.MFE for c in mfe)

    def test_all_families_represented(self, registry: ConceptRegistry):
        """All four confinement families have at least one concept."""
        families = {c.confinement_family for c in registry.concepts}
        assert families == {
            ConfinementFamily.MFE,
            ConfinementFamily.IFE,
            ConfinementFamily.MIF,
            ConfinementFamily.NONSTANDARD,
        }

    def test_known_concept_helion(self, registry: ConceptRegistry):
        """Spot-check Helion FRC: MIF family, D-He3 fuel, pulsed operation."""
        helion = registry.by_id("frc-w-direct-conversion")
        assert helion is not None
        assert helion.confinement_family == ConfinementFamily.MIF
        assert helion.fuel == FuelType.DHE3
        assert helion.operation_mode == OperationMode.PULSED

    def test_known_concept_tae(self, registry: ConceptRegistry):
        """Spot-check TAE p-B11 FRC: MFE/Compact Toroid, p-B11 fuel."""
        tae = registry.by_id("p-b11-frc")
        assert tae is not None
        assert tae.confinement_family == ConfinementFamily.MFE
        assert tae.mfe_topology == MFETopology.COMPACT_TOROID
        assert tae.fuel == FuelType.PB11

    def test_cost_model_id_set_for_known_concepts(self, registry: ConceptRegistry):
        """Concepts with cost models should have cost_model_id set."""
        # Concept 04 = Laser ICF - p-B11 Fast Ignition
        hb11 = registry.by_id("laser-icf-p-b11-fast-ignition")
        assert hb11 is not None
        assert hb11.cost_model_id == "04"

        # Concept without a cost model should have None
        cfs = registry.by_id("hts-compact-tokamak")
        assert cfs is not None
        assert cfs.cost_model_id is None


class TestDecisionTree:
    def test_structure(self, tree: dict):
        """Decision tree has correct root structure."""
        assert tree["version"] == "1.0"
        root = tree["root"]
        assert root["field"] == "confinement_family"
        families = [c["value"] for c in root["children"]]
        assert set(families) == {"MFE", "IFE", "MIF", "Non-Standard"}

    def test_all_concepts_in_tree(self, tree: dict, registry: ConceptRegistry):
        """Every concept in the registry appears exactly once in the tree."""
        concept_ids_in_tree: list[str] = []

        def _collect(node: dict) -> None:
            if "concepts" in node:
                concept_ids_in_tree.extend(node["concepts"])
            if "children" in node:
                for child in node["children"]:
                    _collect(child)

        _collect(tree["root"])
        registry_ids = {c.concept_id for c in registry.concepts}
        tree_ids = set(concept_ids_in_tree)
        assert tree_ids == registry_ids, (
            f"Mismatch: in tree but not registry: {tree_ids - registry_ids}, "
            f"in registry but not tree: {registry_ids - tree_ids}"
        )
        # No duplicates
        assert len(concept_ids_in_tree) == len(tree_ids)

    def test_mfe_has_topology_children(self, tree: dict):
        """MFE branch should have mfe_topology as the branching field."""
        root = tree["root"]
        mfe = next(c for c in root["children"] if c["value"] == "MFE")
        assert mfe["field"] == "mfe_topology"
        topologies = [c["value"] for c in mfe["children"]]
        assert "Tokamak" in topologies
        assert "Stellarator" in topologies
