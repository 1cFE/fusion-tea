"""Pydantic data models for concept taxonomy and classification.

Defines typed enums for all design-attribute columns from the fusion concept
taxonomy (table_v2.csv) and structured models for the concept registry and
decision tree. Kept separate from models.py to avoid coupling with the cost
model data layer.

See design.md for design decisions DD-1 through DD-5.
"""

from __future__ import annotations

from enum import StrEnum
from functools import cached_property

from pydantic import BaseModel, computed_field, model_validator

from exploration.concept_explorer.models import ConfinementFamily, FuelType

# ---------------------------------------------------------------------------
# Hierarchical classification enums
# ---------------------------------------------------------------------------


class MFETopology(StrEnum):
    TOKAMAK = "Tokamak"
    STELLARATOR = "Stellarator"
    OPEN_LINEAR = "Open/Linear"
    COMPACT_TOROID = "Compact Toroid"
    DIPOLE = "Dipole"


class IFEDriver(StrEnum):
    LASER = "Laser"
    PROJECTILE = "Projectile"
    HEAVY_ION_BEAM = "Heavy ion beam"
    ACOUSTIC = "Acoustic"


class MIFMethod(StrEnum):
    FRC_COMPRESSION = "FRC compression"
    MAGNETIZED_TARGET = "Magnetized target"


class NonStandardMechanism(StrEnum):
    ELECTROSTATIC = "Electrostatic"
    MUON_CATALYZED = "Muon-catalyzed"
    PLASMA_FOCUS = "Plasma focus"


class TokamakShape(StrEnum):
    COMPACT = "Compact"
    SPHERICAL = "Spherical"
    NEGATIVE_TRIANGULARITY = "Negative triangularity"
    STANDARD = "Standard"


class StellaratorType(StrEnum):
    PLANAR_COIL = "Planar coil"
    QI = "QI"
    MODULAR = "Modular"
    HELICAL_COIL = "Helical coil"


class LaserApproach(StrEnum):
    FAST_IGNITION = "Fast ignition"
    HYBRID_DRIVE = "Hybrid drive"
    INDIRECT_DRIVE = "Indirect drive"
    DIRECT_DRIVE = "Direct drive"
    ULTRASHORT_PULSE = "Ultrashort pulse"
    LIQUID_JET = "Liquid jet"


# ---------------------------------------------------------------------------
# Cross-cutting design choice enums
# ---------------------------------------------------------------------------


class PrimaryHeating(StrEnum):
    RF_ICRH = "RF (ICRH)"
    RF_ECRH = "RF (ECRH)"
    RF_AND_NBI = "RF + NBI"
    NBI = "NBI"
    OHMIC_SELF_PINCH = "Ohmic (self-pinch)"
    MAGNETIC_COMPRESSION = "Magnetic compression"
    PULSED_POWER_IMPLOSION = "Pulsed power implosion"
    MECHANICAL_COMPRESSION = "Mechanical compression"
    LASER_FAST_IGNITION = "Laser (fast ignition)"
    LASER_DIRECT_DRIVE = "Laser (direct drive)"
    LASER_INDIRECT_DRIVE = "Laser (indirect drive)"
    LASER_ULTRASHORT_PULSE = "Laser (ultrashort pulse)"
    PROJECTILE_IMPACT = "Projectile impact"
    HEAVY_ION_BEAM = "Heavy ion beam"
    ACOUSTIC_IMPLOSION = "Acoustic implosion"
    ELECTROSTATIC_ACCELERATION = "Electrostatic acceleration"
    MUON_CATALYSIS = "Muon catalysis"
    ELECTROMAGNETIC_PINCH_DPF = "Electromagnetic pinch (DPF)"
    TBD = "TBD"
    UNKNOWN = "Unknown"


class HeatingType(StrEnum):
    """v3 P8 typed heating-type vocabulary.

    Atoms only — combinations (e.g. ``ICRH + NBI``) are kept as raw strings
    on ``ConceptTaxonomy.heating_type`` and split into atoms on
    ``heating_type_parsed``.
    """

    ICRH = "ICRH"
    ECRH = "ECRH"
    NBI = "NBI"
    OHMIC = "Ohmic"
    NA_COMPRESSION_DRIVEN = "N/A (compression-driven)"
    NA_NON_THERMAL = "N/A (non-thermal)"
    TBD = "TBD"


class DriverType(StrEnum):
    """v3 P9 typed driver-type vocabulary."""

    MAGNETIC = "Magnetic"
    MAGNETIC_PINCH = "Magnetic pinch"
    DPSSL_LASER = "DPSSL Laser"
    GAS_LASER = "Gas Laser"
    ION_PARTICLE_BEAM = "Ion/particle beam"
    MECHANICAL_KINETIC = "Mechanical/kinetic"
    ELECTROSTATIC = "Electrostatic"
    OTHER = "Other"
    TBD = "TBD"


class EnergyCapture(StrEnum):
    THERMAL_STEAM = "Thermal (steam)"
    THERMAL_UNSPECIFIED = "Thermal (unspecified)"
    THERMAL_SCO2 = "Thermal (sCO2)"
    DIRECT_INDUCTIVE = "Direct (inductive)"
    DIRECT_CHARGED_PARTICLE = "Direct (charged particle)"
    HYBRID_THERMAL_DIRECT = "Hybrid (thermal + direct)"
    TBD = "TBD"


# PlasmaState and NeutronManagement enums removed per schema 0.3.0
# (Plasma State derivable from Confinement Concept + Operation Mode;
#  Neutron Management implied by Fuel.)


class MagnetType(StrEnum):
    HTS_WOUND = "HTS (wound)"
    HTS_PLANAR_ARRAY = "HTS (planar array)"
    HTS_3D_STELLARATOR = "HTS (3D stellarator)"
    HTS_LEVITATED_DIPOLE = "HTS (levitated dipole)"
    LTS = "LTS"
    LTS_HTS = "LTS+HTS"
    RESISTIVE = "Resistive"
    NONE = "None"
    ELECTROSTATIC = "Electrostatic"
    NA = "N/A"
    TBD = "TBD"
    UNKNOWN = "Unknown"


class BlanketConfig(StrEnum):
    LIQUID_METAL = "Liquid metal"
    MOLTEN_SALT = "Molten salt"
    SOLID_BREEDER = "Solid breeder"
    OTHER_HYBRID = "Other/hybrid"
    NA_NO_TRITIUM = "N/A (no tritium)"
    NA_NON_POWER = "N/A (non-power)"
    TBD = "TBD"


class OperationMode(StrEnum):
    STEADY_STATE = "Steady-state"
    QUASI_STEADY = "Quasi-steady"
    PULSED = "Pulsed"
    TBD = "TBD"


class RepetitionRate(StrEnum):
    SUB_HZ = "Sub-Hz"
    ABOUT_1_HZ = "~1 Hz"
    ABOUT_10_HZ = "~10 Hz"
    KHZ = "kHz"
    HIGH_GT_10_HZ = "High (>10 Hz)"
    UNKNOWN = "Unknown"


class TaxonomyConfidence(StrEnum):
    HIGH = "high"
    MEDIUM_HIGH = "medium-high"
    MEDIUM = "medium"
    MEDIUM_LOW = "medium-low"
    LOW = "low"


# ---------------------------------------------------------------------------
# Core model
# ---------------------------------------------------------------------------


class ConceptTaxonomy(BaseModel):
    """Complete taxonomy record for a single fusion concept."""

    # Identity
    concept_id: str  # Analysis directory ID, e.g. "01"
    slug: str  # URL-safe slug, e.g. "hts-compact-tokamak"
    name: str
    company: str | None = None

    # Hierarchical classification
    confinement_family: ConfinementFamily
    mfe_topology: MFETopology | None = None
    ife_driver: IFEDriver | None = None
    mif_method: MIFMethod | None = None
    non_standard_mechanism: NonStandardMechanism | None = None
    tokamak_shape: TokamakShape | None = None
    stellarator_type: StellaratorType | None = None
    laser_approach: LaserApproach | None = None

    # Cross-cutting design choices
    fuel: FuelType
    primary_heating: PrimaryHeating | None = None
    heating_type: str | None = None  # raw CSV value; may be a "+"-joined combo
    driver_type: DriverType | None = None
    energy_capture: EnergyCapture | None = None
    magnet_type: MagnetType | None = None
    blanket_config: BlanketConfig | None = None
    operation_mode: OperationMode
    repetition_rate: RepetitionRate | None = None
    driver_technology: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def heating_type_parsed(self) -> list[HeatingType]:
        """Split combination heating values (e.g. ``ICRH + NBI``) into atoms."""
        if not self.heating_type:
            return []
        atoms: list[HeatingType] = []
        for part in self.heating_type.split(" + "):
            atoms.append(HeatingType(part.strip()))
        return atoms

    # Metadata
    confidence: TaxonomyConfidence

    @model_validator(mode="after")
    def _validate_hierarchy(self) -> ConceptTaxonomy:
        """Validate hierarchical consistency.

        MFE concepts MUST have mfe_topology; non-MFE MUST NOT.
        IFE concepts MUST have ife_driver; non-IFE MUST NOT.
        Tokamak concepts MAY have tokamak_shape; non-Tokamak MUST NOT.
        Laser IFE concepts MAY have laser_approach; non-Laser MUST NOT.
        Stellarator concepts MAY have stellarator_type; non-Stellarator MUST NOT.
        MIF concepts MUST have mif_method; non-MIF MUST NOT.
        Non-Standard concepts MUST have non_standard_mechanism; others MUST NOT.
        """
        errors: list[str] = []
        family = self.confinement_family

        # --- MFE ---
        if family == ConfinementFamily.MFE:
            if self.mfe_topology is None:
                errors.append("MFE concept must have mfe_topology")
            if self.ife_driver is not None:
                errors.append("MFE concept must not have ife_driver")
            if self.mif_method is not None:
                errors.append("MFE concept must not have mif_method")
            if self.non_standard_mechanism is not None:
                errors.append("MFE concept must not have non_standard_mechanism")
        # --- IFE ---
        elif family == ConfinementFamily.IFE:
            if self.ife_driver is None:
                errors.append("IFE concept must have ife_driver")
            if self.mfe_topology is not None:
                errors.append("IFE concept must not have mfe_topology")
            if self.mif_method is not None:
                errors.append("IFE concept must not have mif_method")
            if self.non_standard_mechanism is not None:
                errors.append("IFE concept must not have non_standard_mechanism")
        # --- MIF ---
        elif family == ConfinementFamily.MIF:
            if self.mif_method is None:
                errors.append("MIF concept must have mif_method")
            if self.mfe_topology is not None:
                errors.append("MIF concept must not have mfe_topology")
            if self.ife_driver is not None:
                errors.append("MIF concept must not have ife_driver")
            if self.non_standard_mechanism is not None:
                errors.append("MIF concept must not have non_standard_mechanism")
        # --- Non-Standard ---
        elif family == ConfinementFamily.NONSTANDARD:
            if self.non_standard_mechanism is None:
                errors.append("Non-Standard concept must have non_standard_mechanism")
            if self.mfe_topology is not None:
                errors.append("Non-Standard concept must not have mfe_topology")
            if self.ife_driver is not None:
                errors.append("Non-Standard concept must not have ife_driver")
            if self.mif_method is not None:
                errors.append("Non-Standard concept must not have mif_method")

        # --- Sub-type validators ---
        if self.tokamak_shape is not None and self.mfe_topology != MFETopology.TOKAMAK:
            errors.append("tokamak_shape only valid for Tokamak topology")
        if self.stellarator_type is not None and self.mfe_topology != MFETopology.STELLARATOR:
            errors.append("stellarator_type only valid for Stellarator topology")
        if self.laser_approach is not None and self.ife_driver != IFEDriver.LASER:
            errors.append("laser_approach only valid for Laser IFE driver")

        if errors:
            raise ValueError("; ".join(errors))
        return self


# ---------------------------------------------------------------------------
# Registry container
# ---------------------------------------------------------------------------


class ConceptRegistry(BaseModel):
    """Complete concept taxonomy registry -- the source of truth."""

    version: str
    generated_from: str | None = None
    concepts: list[ConceptTaxonomy]

    def by_id(self, concept_id: str) -> ConceptTaxonomy | None:
        """Look up a concept by ID."""
        for c in self.concepts:
            if c.concept_id == concept_id:
                return c
        return None

    def by_slug(self, slug: str) -> ConceptTaxonomy | None:
        """Look up a concept by slug (e.g. 'hts-compact-tokamak')."""
        for c in self.concepts:
            if c.slug == slug:
                return c
        return None

    def by_family(self, family: ConfinementFamily) -> list[ConceptTaxonomy]:
        """Filter concepts by confinement family."""
        return [c for c in self.concepts if c.confinement_family == family]
