"""Pydantic data models for the Fusion TEA Concept Explorer.

All monetary values are in M$ (millions of USD). Elasticity values are
dimensionless: (dLCOE/dp) * (p/LCOE).
"""

from __future__ import annotations

import warnings
from enum import StrEnum
from typing import Any, ClassVar

from pydantic import BaseModel, Field, model_validator

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ConfinementFamily(StrEnum):
    MFE = "MFE"  # Magnetic Fusion Energy (tokamaks, stellarators, mirrors, FRC)
    IFE = "IFE"  # Inertial Fusion Energy (laser, heavy-ion)
    MIF = "MIF"  # Magneto-Inertial Fusion (magnetized target)
    NONSTANDARD = "NONSTANDARD"  # Exotic or hybrid concepts


class FuelType(StrEnum):
    DT = "DT"
    DD = "DD"
    DHE3 = "DHe3"
    PB11 = "PB11"
    OTHER = "OTHER"


class ModelType(StrEnum):
    COSTINGFE = "costingfe"  # Backed by 1costingfe CostModel.forward()
    STANDALONE = "standalone"  # Custom to_explorer_dict() only


class ParameterCategory(StrEnum):
    SHARED_BASELINE = "shared_baseline"  # Common to most fusion concepts
    WELL_ESTABLISHED = "well_established"  # Physics / engineering consensus
    KEY_INNOVATION = "key_innovation"  # The concept's core performance claim
    CONCEPT_UNIQUE = "concept_unique"  # Specific to this concept only


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DataAvailability(StrEnum):
    FULL = "full"
    PARTIAL = "partial"
    SPARSE = "sparse"
    NONE = "none"


class RiskSeverity(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ConceptStatus(StrEnum):
    APPROVED = "approved"  # Cost model complete, reviewed
    IN_PROGRESS = "in_progress"  # Analysis started, not finalised


# ---------------------------------------------------------------------------
# Cost model sub-structures
# ---------------------------------------------------------------------------


class CASAccount(BaseModel):
    """Single CAS account entry. All costs in M$."""

    name: str
    cost_m_usd: float
    overridden: bool = False


class HeadlineEconomics(BaseModel):
    """Top-line economic outputs derived from the cost model forward result."""

    lcoe_per_mwh: float  # Levelised cost of electricity [$/MWh]
    overnight_cost_per_kw: float  # Overnight capital cost [$/kW]
    p_net_mw: float  # Net electric output [MW]
    q_eng: float  # Engineering Q (fusion power / recirculating power)
    capacity_factor: float  # Plant availability / annual capacity factor [0–1]


class SensitivityEntry(BaseModel):
    """Sensitivity of LCOE to a single parameter."""

    elasticity: float  # (dLCOE/dp) * (p/LCOE) — dimensionless
    baseline: float  # Parameter value at which elasticity was computed


class SensitivityAnalysis(BaseModel):
    """Full sensitivity decomposition for a concept."""

    engineering: dict[str, SensitivityEntry]  # Physics / plant parameters
    financial: dict[str, SensitivityEntry]  # Interest rate, lifetime, etc.


class CostModelData(BaseModel):
    """Complete cost model output for one concept.

    All CAS accounts are always present; zero-valued if not applicable.
    Monetary values are in M$ throughout.
    """

    # Top-level CAS accounts
    cas10: CASAccount  # Preconstruction
    cas21: CASAccount  # Buildings & structures
    cas22: CASAccount  # Reactor plant equipment (aggregate)
    cas23: CASAccount  # Turbine plant equipment
    cas24: CASAccount  # Electrical plant equipment
    cas25: CASAccount  # Miscellaneous plant equipment
    cas26: CASAccount  # Heat rejection systems
    cas27: CASAccount  # Special materials
    cas28: CASAccount  # Digital twin & simulation infrastructure
    cas29: CASAccount  # Contingency
    cas30: CASAccount  # Indirect costs
    cas40: CASAccount  # Owner's costs
    cas50: CASAccount  # Supplementary costs
    cas60: CASAccount  # Interest during construction (IDC)
    cas70: CASAccount  # O&M costs (annualised)
    cas80: CASAccount  # Fuel costs (annualised)
    cas90: CASAccount  # Financial costs

    # CAS22 sub-account detail (always present; zero if not used)
    cas22_detail: dict[str, CASAccount]

    headline: HeadlineEconomics
    sensitivities: SensitivityAnalysis | None = None
    params: dict[str, float] = Field(default_factory=dict)

    # Human-readable names for top-level and CAS22 sub-accounts
    CAS_NAMES: ClassVar[dict[str, str]] = {
        "cas10": "Preconstruction",
        "cas21": "Buildings & Structures",
        "cas22": "Reactor Plant Equipment",
        "cas23": "Turbine Plant Equipment",
        "cas24": "Electrical Plant Equipment",
        "cas25": "Miscellaneous Plant Equipment",
        "cas26": "Heat Rejection Systems",
        "cas27": "Special Materials",
        "cas28": "Digital Twin & Simulation",
        "cas29": "Contingency",
        "cas30": "Indirect Costs",
        "cas40": "Owner's Costs",
        "cas50": "Supplementary Costs",
        "cas60": "Interest During Construction",
        "cas70": "O&M Costs (annualised)",
        "cas80": "Fuel Costs (annualised)",
        "cas90": "Financial Costs",
    }

    CAS22_NAMES: ClassVar[dict[str, str]] = {
        "C220101": "First Wall & Blanket",
        "C220102": "Radiation Shield",
        "C220103": "Magnets / Coils",
        "C220104": "Heating & Driver Systems",
        "C220105": "Primary Structure & Support",
        "C220106": "Vacuum System",
        "C220107": "Power Conditioning & Energy Storage",
        "C220108": "Fuel Handling & Target Factory",
        "C220200": "Maintenance Equipment",
        "C220300": "Remote Handling & Hot Cell",
        "C220400": "Instrumentation & Control",
        "C220500": "Plasma / Feedback Control",
        "C220600": "Cryogenic Cooling System",
        "C220700": "Neutron Source & Moderator",
    }

    @classmethod
    def from_forward_result(
        cls,
        result: dict[str, Any],
        sensitivities: SensitivityAnalysis | None,
    ) -> CostModelData:
        """Construct from ``dataclasses.asdict(forward_result)``.

        Expected dict structure (from 1costingfe ``CostModel.forward()``)::

            {
                "costs": {
                    "cas10": float,   # M$
                    "cas21": float,
                    "cas22": float,
                    "cas23": float,
                    "cas24": float,
                    "cas25": float,
                    "cas26": float,
                    "cas27": float,
                    "cas28": float,
                    "cas29": float,
                    "cas30": float,
                    "cas40": float,
                    "cas50": float,
                    "cas60": float,
                    "cas70": float,
                    "cas80": float,
                    "cas90": float,
                    "lcoe": float,           # $/MWh
                    "overnight_cost": float, # $/kW
                    "total_capital": float,  # M$
                },
                "power_table": {
                    "p_net": float,   # MW
                    "q_eng": float,
                    "capacity_factor": float,  # [0–1] (may be "availability")
                    ...
                },
                "cas22_detail": {
                    "C220101": float,   # M$
                    "C220103": float,
                    ...
                },
                "overridden": ["C220103", ...],
                "params": {"net_electric_mw": float, ...},
            }

        All CAS accounts absent from the dict are zero-filled.
        All C220101–C220700 sub-accounts absent from ``cas22_detail`` are zero-filled.
        """
        costs = result.get("costs", {})
        power = result.get("power_table", {})
        detail_raw: dict[str, float] = result.get("cas22_detail", {})
        overridden_set: set[str] = set(result.get("overridden", []))
        params: dict[str, float] = result.get("params", {})

        def _cas(field_name: str) -> CASAccount:
            """Build a CASAccount from the costs sub-dict."""
            cost = float(costs.get(field_name, 0.0))
            return CASAccount(
                name=cls.CAS_NAMES.get(field_name, field_name),
                cost_m_usd=cost,
                overridden=field_name.upper() in overridden_set,
            )

        def _cas22_sub(key: str) -> CASAccount:
            """Build a CAS22 sub-account CASAccount from cas22_detail."""
            cost = float(detail_raw.get(key, 0.0))
            return CASAccount(
                name=cls.CAS22_NAMES.get(key, key),
                cost_m_usd=cost,
                overridden=key in overridden_set,
            )

        # Capacity factor: prefer explicit field; fall back to availability
        capacity_factor = float(power.get("capacity_factor", power.get("availability", 0.0)))

        headline = HeadlineEconomics(
            lcoe_per_mwh=float(costs.get("lcoe", 0.0)),
            overnight_cost_per_kw=float(costs.get("overnight_cost", 0.0)),
            p_net_mw=float(power.get("p_net", 0.0)),
            q_eng=float(power.get("q_eng", 0.0)),
            capacity_factor=capacity_factor,
        )

        cas22_detail = {key: _cas22_sub(key) for key in cls.CAS22_NAMES}

        return cls(
            cas10=_cas("cas10"),
            cas21=_cas("cas21"),
            cas22=_cas("cas22"),
            cas23=_cas("cas23"),
            cas24=_cas("cas24"),
            cas25=_cas("cas25"),
            cas26=_cas("cas26"),
            cas27=_cas("cas27"),
            cas28=_cas("cas28"),
            cas29=_cas("cas29"),
            cas30=_cas("cas30"),
            cas40=_cas("cas40"),
            cas50=_cas("cas50"),
            cas60=_cas("cas60"),
            cas70=_cas("cas70"),
            cas80=_cas("cas80"),
            cas90=_cas("cas90"),
            cas22_detail=cas22_detail,
            headline=headline,
            sensitivities=sensitivities,
            params=params,
        )


# ---------------------------------------------------------------------------
# Parameter metadata and narrative
# ---------------------------------------------------------------------------


class ParameterMetadata(BaseModel):
    """Authored context for a single model parameter (from model_metadata.yaml)."""

    display_name: str
    category: ParameterCategory
    confidence: Confidence
    baseline: float  # Canonical baseline value used in sensitivity analysis
    display_multiplier: float = 1.0  # Multiply to get display units
    display_unit: str = ""
    range: tuple[float, float]  # [low, high] for slider / tornado bounds
    source: str | None = None  # Citation string or file path
    modeling_note: str | None = None  # Analyst note shown in parameter card


class NarrativeData(BaseModel):
    """LLM-extracted narrative context for a concept (from claude -p pipeline)."""

    key_bets: list[str]  # Technical claims the concept depends on
    eliminated_costs: list[str]  # Costs this concept avoids vs. conventional
    novel_costs: list[str]  # Unique cost drivers not present in other concepts
    risks: list[dict[str, Any]]  # Each entry: {"description": str, "severity": str}


class SourcePaths(BaseModel):
    """File-system paths to the concept's source scripts (repo-relative)."""

    model_setup: str | None = None  # Path to model_setup.py (costingfe-backed)
    analysis: str | None = None  # Path to analysis.md or standalone script


# ---------------------------------------------------------------------------
# Top-level concept payload
# ---------------------------------------------------------------------------


class ConceptData(BaseModel):
    """Complete data payload for a single fusion concept."""

    concept_id: str  # e.g. "04"
    name: str
    confinement_family: ConfinementFamily
    company: str | None = None
    status: ConceptStatus
    illustration: str | None = None  # Filename under static/images/concepts/
    has_cost_model: bool
    has_sensitivities: bool
    cost_model: CostModelData | None = None
    parameter_metadata: dict[str, ParameterMetadata] = Field(default_factory=dict)
    narrative: NarrativeData | None = None
    sources: SourcePaths

    @model_validator(mode="after")
    def _warn_on_uncovered_sensitivity_keys(self) -> ConceptData:
        """Emit UserWarning for sensitivity keys not present in parameter_metadata.

        Coverage gaps mean the tornado chart will render a bar without a card.
        The validator warns rather than errors to allow incremental authoring.
        """
        if self.cost_model is None or self.cost_model.sensitivities is None:
            return self

        sensitivity_keys: set[str] = set(self.cost_model.sensitivities.engineering) | set(
            self.cost_model.sensitivities.financial
        )

        uncovered = sensitivity_keys - set(self.parameter_metadata)
        if uncovered:
            warnings.warn(
                f"ConceptData '{self.concept_id}': sensitivity keys not covered by "
                f"parameter_metadata: {sorted(uncovered)}",
                UserWarning,
                stacklevel=2,
            )
        return self


# ---------------------------------------------------------------------------
# Manifest and parameter index (entry view + cross-concept lookups)
# ---------------------------------------------------------------------------


class ConceptManifestEntry(BaseModel):
    """Lightweight summary of a concept, used by the entry view grid."""

    concept_id: str
    name: str
    confinement_family: ConfinementFamily
    company: str | None = None
    status: ConceptStatus
    illustration: str | None = None
    has_cost_model: bool
    has_sensitivities: bool
    lcoe_per_mwh: float | None = None
    confidence: Confidence | None = None
    data_file: str  # Path to the per-concept JSON under data/, e.g. "data/04.json"


class ConceptManifest(BaseModel):
    """Index of all extracted concepts, generated by the extraction script."""

    generated_at: str  # ISO 8601 timestamp
    concepts: list[ConceptManifestEntry]


class ParameterConceptEntry(BaseModel):
    """A concept's sensitivity to a single parameter (for cross-concept index)."""

    concept_id: str
    name: str
    elasticity: float


class ParameterIndexEntry(BaseModel):
    """Cross-concept sensitivity summary for one parameter."""

    param_name: str
    display_name: str
    category: ParameterCategory
    concepts: list[ParameterConceptEntry]  # All concepts sensitive to this param


class ParameterIndex(BaseModel):
    """Full cross-concept sensitivity index, keyed by parameter name."""

    parameters: dict[str, ParameterIndexEntry]


# ---------------------------------------------------------------------------
# Session state and computation API
# ---------------------------------------------------------------------------


class ExplorerState(BaseModel):
    """Frontend session state, persisted in-memory on the server."""

    current_concept_id: str | None = None
    slider_overrides: dict[str, float] = Field(default_factory=dict)
    comparison_set: list[str] = Field(default_factory=list)
    # Set server-side on POST; empty on default GET
    timestamp: str = ""


class ComputeRequest(BaseModel):
    """Request body for POST /api/compute (slider-driven recompute)."""

    concept_id: str
    overrides: dict[str, float]  # Param name → new value
