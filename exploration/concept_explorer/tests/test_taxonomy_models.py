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
    BlanketConfig,
    ConceptRegistry,
    ConceptTaxonomy,
    EnergyCapture,
    IFEDriver,
    LaserApproach,
    MagnetType,
    MFETopology,
    NonStandardMechanism,
    OperationMode,
    PrimaryHeating,
    TaxonomyConfidence,
    TokamakShape,
)
from exploration.concept_explorer.seed_registry import tree_group

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
            concept_id="01",
            slug="hts-compact-tokamak",
            name="HTS Compact Tokamak",
            company="Commonwealth Fusion Systems",
            confinement_family=ConfinementFamily.MFE,
            mfe_topology=MFETopology.TOKAMAK,
            tokamak_shape=TokamakShape.COMPACT,
            fuel=FuelType.DT,
            primary_heating=PrimaryHeating.RF_ICRH,
            energy_capture=EnergyCapture.THERMAL_STEAM,
            magnet_type=MagnetType.HTS_WOUND,
            blanket_config=BlanketConfig.MOLTEN_SALT,
            operation_mode=OperationMode.QUASI_STEADY,
            confidence=TaxonomyConfidence.HIGH,
        )
        data = concept.model_dump(mode="json")
        assert data["tokamak_shape"] == "Compact"
        assert data["blanket_config"] == "Molten salt"
        assert data["ife_driver"] is None  # N/A fields serialize as null
        rebuilt = ConceptTaxonomy.model_validate(data)
        assert rebuilt == concept

    def test_blanket_config_round_trip(self):
        """Every BlanketConfig enum member round-trips through JSON."""
        for member in BlanketConfig:
            concept = ConceptTaxonomy(
                concept_id="bt",
                slug="bt",
                name="BT",
                confinement_family=ConfinementFamily.MFE,
                mfe_topology=MFETopology.TOKAMAK,
                fuel=FuelType.DT,
                blanket_config=member,
                operation_mode=OperationMode.STEADY_STATE,
                confidence=TaxonomyConfidence.MEDIUM,
            )
            data = concept.model_dump(mode="json")
            assert data["blanket_config"] == member.value
            rebuilt = ConceptTaxonomy.model_validate(data)
            assert rebuilt.blanket_config == member

    def test_blanket_config_enum_covers_v3_values(self):
        """BlanketConfig must cover the v3 controlled vocabulary."""
        assert {m.value for m in BlanketConfig} >= {
            "Liquid metal", "Molten salt", "Solid breeder", "Other/hybrid",
            "N/A (no tritium)", "N/A (non-power)", "TBD",
        }

    def test_hierarchy_validator_rejects_mfe_with_ife_driver(self):
        """MFE concept with ife_driver set should fail validation."""
        with pytest.raises(ValidationError):
            ConceptTaxonomy(
                concept_id="bad",
                slug="bad",
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
                slug="bad",
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
                slug="bad",
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
                slug="bad",
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
            slug="test",
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
            slug="test",
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
                slug="bad",
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
                slug="bad",
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
    def test_loads_all_40_concepts(self, registry: ConceptRegistry):
        """The seeded registry JSON loads and validates all 40 v3 concepts."""
        assert len(registry.concepts) == 40
        ids = [c.concept_id for c in registry.concepts]
        assert len(set(ids)) == 40  # All unique

    def test_by_id(self, registry: ConceptRegistry):
        """by_id returns correct concept or None."""
        concept = registry.by_id("01")
        assert concept is not None
        assert concept.name.startswith("HTS Compact Tokamak")
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

    def test_known_concept_frc(self, registry: ConceptRegistry):
        """Spot-check FRC w/ Direct Conversion (08): MIF family, D-He3 fuel."""
        c = registry.by_id("08")
        assert c is not None
        assert c.confinement_family == ConfinementFamily.MIF
        assert c.fuel == FuelType.DHE3

    def test_known_concept_tae(self, registry: ConceptRegistry):
        """Spot-check p-B11 FRC (18): MFE/Compact Toroid, p-B11 fuel."""
        tae = registry.by_id("18")
        assert tae is not None
        assert tae.confinement_family == ConfinementFamily.MFE
        assert tae.mfe_topology == MFETopology.COMPACT_TOROID
        assert tae.fuel == FuelType.PB11

    def test_concept_id_is_analysis_id(self, registry: ConceptRegistry):
        """concept_id is the leading token of the directory ID (e.g. 17a, 20b)."""
        for cid in ("01", "17a", "17b", "20a", "20b", "39"):
            c = registry.by_id(cid)
            assert c is not None, f"missing concept_id {cid}"

    def test_by_slug(self, registry: ConceptRegistry):
        """by_slug returns correct concept for v3 slug shapes."""
        c = registry.by_slug("hts-compact-tokamak-d-t")
        assert c is not None
        assert c.concept_id == "01"
        assert registry.by_slug("nonexistent") is None


class TestDecisionTree:
    def test_structure(self, tree: dict):
        """Decision tree root uses v3 tree_group with six top-level groups."""
        assert tree["version"] == "1.0"
        root = tree["root"]
        assert root["field"] == "tree_group"
        groups = [c["value"] for c in root["children"]]
        assert set(groups) == {"MFE", "IFE", "MIF", "Cmpt-Tor", "Estatic", "Other"}

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
        assert len(concept_ids_in_tree) == len(tree_ids)

    def test_mfe_has_topology_children(self, tree: dict):
        """MFE group branches on mfe_topology (Compact Toroid now under Cmpt-Tor)."""
        root = tree["root"]
        mfe = next(c for c in root["children"] if c["value"] == "MFE")
        assert mfe["field"] == "mfe_topology"
        topologies = [c["value"] for c in mfe["children"]]
        assert "Tokamak" in topologies
        assert "Stellarator" in topologies
        # Compact Toroid is its own group under Cmpt-Tor, not under MFE
        assert "Compact Toroid" not in topologies


class TestTreeGroup:
    """v3 display-only sibling grouping (FR-2)."""

    def _make(self, **kwargs) -> ConceptTaxonomy:
        defaults = dict(
            concept_id="tg",
            slug="tg",
            name="TG",
            fuel=FuelType.DT,
            operation_mode=OperationMode.STEADY_STATE,
            confidence=TaxonomyConfidence.MEDIUM,
        )
        defaults.update(kwargs)
        return ConceptTaxonomy(**defaults)

    def test_mfe_tokamak_returns_mfe(self):
        c = self._make(
            confinement_family=ConfinementFamily.MFE,
            mfe_topology=MFETopology.TOKAMAK,
        )
        assert tree_group(c) == "MFE"

    def test_compact_toroid_returns_cmpt_tor(self):
        c = self._make(
            confinement_family=ConfinementFamily.MFE,
            mfe_topology=MFETopology.COMPACT_TOROID,
            fuel=FuelType.PB11,
        )
        assert tree_group(c) == "Cmpt-Tor"

    def test_electrostatic_returns_estatic(self):
        c = self._make(
            confinement_family=ConfinementFamily.NONSTANDARD,
            non_standard_mechanism=NonStandardMechanism.ELECTROSTATIC,
        )
        assert tree_group(c) == "Estatic"

    def test_nonstandard_non_electrostatic_returns_other(self):
        c = self._make(
            confinement_family=ConfinementFamily.NONSTANDARD,
            non_standard_mechanism=NonStandardMechanism.MUON_CATALYZED,
        )
        assert tree_group(c) == "Other"

    def test_ife_returns_ife(self):
        c = self._make(
            confinement_family=ConfinementFamily.IFE,
            ife_driver=IFEDriver.LASER,
            operation_mode=OperationMode.PULSED,
        )
        assert tree_group(c) == "IFE"

    def test_every_registry_concept_lands_in_one_group(
        self, registry: ConceptRegistry
    ):
        """Partition check: every concept maps to exactly one of the six groups."""
        valid = {"MFE", "IFE", "MIF", "Cmpt-Tor", "Estatic", "Other"}
        for c in registry.concepts:
            assert tree_group(c) in valid, (
                f"{c.concept_id} {c.name}: tree_group returned "
                f"{tree_group(c)!r}, not in {valid}"
            )


def test_csv_has_typed_heating_and_driver_columns():
    """Phase 2: typed Heating Type / Driver Type columns exist and are populated."""
    import csv
    rows = list(csv.DictReader(open("exploration/concept_analysis/table.csv")))
    assert "Heating Type" in rows[0], "missing Heating Type column"
    assert "Driver Type" in rows[0], "missing Driver Type column"
    assert all(r["Heating Type"].strip() for r in rows), "empty Heating Type cell"
    assert all(r["Driver Type"].strip() for r in rows), "empty Driver Type cell"
