"""Pydantic data models for the Fusion TEA Concept Explorer.

All monetary values are in M$ (millions of USD). Elasticity values are
dimensionless: (dLCOE/dp) * (p/LCOE).
"""

from __future__ import annotations

import math
import warnings
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, ClassVar

import yaml
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


# Display form for each fuel — the single authority for the `(Fuel)` parenthetical
# in canonical concept names (A1, `resolve_identity`). These match the CSV's
# authored `Fuel` column strings (see seed_registry.FUEL_MAP, the parse-direction
# inverse). OTHER maps to "" so a fuel with no canonical display form yields a
# bare name with no parenthetical — never `(OTHER)` or `(None)` (FR-A1.5).
FUEL_DISPLAY: dict[FuelType, str] = {
    FuelType.DT: "D-T",
    FuelType.DD: "D-D",
    FuelType.DHE3: "D-He3",
    FuelType.PB11: "p-B11",
    FuelType.OTHER: "",
}


class ModelType(StrEnum):
    COSTINGFE = "costingfe"  # Backed by 1costingfe CostModel.forward()
    STANDALONE = "standalone"  # Custom to_explorer_dict() only


class ParameterCategory(StrEnum):
    SHARED_BASELINE = "shared-baseline"  # Common to most fusion concepts
    WELL_ESTABLISHED = "well-established"  # Physics / engineering consensus
    KEY_INNOVATION = "key-innovation"  # The concept's core performance claim
    CONCEPT_UNIQUE = "concept-unique"  # Specific to this concept only
    HIGH_RISK = "high-risk"  # Poorly constrained AND high LCOE impact
    UNCLASSIFIED = "unclassified"  # No authored metadata yet


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


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
    cas70: CASAccount  # O&M costs (annualised) — combined = cas71 + cas72
    # Annualised-O&M split. Optional because some concepts' cost models do not
    # separate fixed O&M from scheduled replacement (e.g. 37/39); for those the
    # split is genuinely *not recorded* and stays None — an honest-degradation
    # signal the cost-landscape renders as a combined-O&M segment, never a
    # fabricated zero account. When present, cas71 + cas72 == cas70.
    cas71: CASAccount | None = None  # Fixed O&M (annualised)
    cas72: CASAccount | None = None  # Scheduled replacement (annualised)
    cas80: CASAccount  # Fuel costs (annualised)
    cas90: CASAccount  # Financial costs

    # CAS22 sub-account detail (always present; zero if not used)
    cas22_detail: dict[str, CASAccount]

    headline: HeadlineEconomics
    # `sensitivities` holds the *analyst-applied* tornado (Bet 3) — consistent
    # with the applied headline and the default toggle state; existing readers
    # (validator, parameter index, tornado.js) silently become applied-based.
    # `sensitivities_bare` is the library-bare alternate the frontend swaps to
    # when the toggle is off. Both are honest `model.sensitivity(...)` calls;
    # neither is derived from the other (INV-3). Equal when the registry is empty.
    sensitivities: SensitivityAnalysis | None = None
    sensitivities_bare: SensitivityAnalysis | None = None
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
        "cas71": "Fixed O&M (annualised)",
        "cas72": "Scheduled Replacement (annualised)",
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
        "C220108": "Divertor / Target Factory",
        "C220109": "Direct Energy Converter",
        "C220110": "Remote Handling & Maintenance Equipment",
        "C220111": "Installation Labor",
        "C220112": "Isotope Separation Plant",
        "C220200": "Main & Secondary Coolant",
        "C220300": "Auxiliary Cooling & Cryoplant",
        "C220400": "Radioactive Waste Management",
        "C220500": "Fuel Handling & Storage",
        "C220600": "Other Reactor Plant Equipment",
        "C220700": "Instrumentation & Control",
    }

    @classmethod
    def from_forward_result(
        cls,
        result: dict[str, Any],
        sensitivities: SensitivityAnalysis | None,
        sensitivities_bare: SensitivityAnalysis | None = None,
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
                    "cas71": float,   # optional: annualised fixed O&M
                    "cas72": float,   # optional: annualised scheduled replacement
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
        params: dict[str, float] = {
            k: v for k, v in result.get("params", {}).items() if isinstance(v, (int, float))
        }

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
            # Build the O&M split only when the forward result carries it; a
            # missing key means the concept's model never separated the two, so
            # leave it None rather than fabricate a zero account (honest
            # degradation — the cost-landscape shows combined O&M for these).
            cas71=_cas("cas71") if "cas71" in costs else None,
            cas72=_cas("cas72") if "cas72" in costs else None,
            cas80=_cas("cas80"),
            cas90=_cas("cas90"),
            cas22_detail=cas22_detail,
            headline=headline,
            sensitivities=sensitivities,
            sensitivities_bare=sensitivities_bare,
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


class OverrideRecord(BaseModel):
    """One analyst cost-override registry entry, carried to the explorer payload.

    A 1:1 projection of the ``Override`` TypedDict in
    ``model_setup_helpers.py`` (the analyst-authored, version-controlled
    registry), plus a resolved ``account_name`` so the front-end never has to
    re-derive CAS account semantics (single source of names = the CAS_NAMES /
    CAS22_NAMES maps on ``CostModelData``).

    Narrative fields are ``str | None``: a genuinely absent field is ``None``
    (rendered as an explicit "not recorded" state by the inspection panel),
    NOT coerced to ``""``. The panel must distinguish "recorded empty" from
    "not recorded" (FR-6 — honest degradation, no silent vanish).

    ``value`` is at the concept's *native per-module* M$ scale, which is not the
    1 GWe projection the cost tables display — the panel labels the scale so the
    two numbers don't read as a contradiction.
    """

    account: str  # CAS code as authored, e.g. "C220103" or "CAS27"
    account_name: str  # Human-readable, resolved from CAS_NAMES / CAS22_NAMES
    value: float  # Per-module M$ at the design point's native scale
    enabled: bool  # False entries stay in the registry but are not applied
    provenance: str | None = None  # "direct" | "derived"
    source: str | None = None  # Free-text citation
    rationale: str | None = None  # Why the override departs from the library default
    cost_basis: str | None = None  # Vintage basis (strict registry requires "noak")
    blocked_by: str | None = None  # Required iff enabled is False — "<org>/<repo>#<NN>"


# ---------------------------------------------------------------------------
# Top-level concept payload
# ---------------------------------------------------------------------------


class ConceptData(BaseModel):
    """Complete data payload for a single fusion concept."""

    concept_id: str  # e.g. "04" — also serves as the visible concept code (#NN)
    # Canonical display name. The raw `name` persisted in data/NN.json is the
    # analyst frontmatter phrasing (the *company* form, e.g. "HTS Compact Tokamak
    # (Commonwealth Fusion / ARC)") — NOT the display name. At server load it is
    # overwritten in memory by `resolve_identity` with the CSV-backed canonical
    # "Name (Fuel)" (A1); the raw phrasing is retained on `analyst_name` below.
    name: str
    confinement_family: ConfinementFamily
    company: str | None = None
    # --- Canonical identity overlay (A1) — stamped at server load, absent on disk ---
    # The original frontmatter `name` (analyst/company phrasing), preserved so any
    # page that wants the analyst's words still has them. None until stamped.
    analyst_name: str | None = None
    # Structured fuel from the CSV-backed registry; part of canonical identity.
    # None only when a served concept is absent from the registry (honest
    # degradation — `resolve_identity` never fabricates a fuel).
    fuel: FuelType | None = None
    status: ConceptStatus
    illustration: str | None = None  # Filename under static/images/concepts/
    has_cost_model: bool
    has_sensitivities: bool
    cost_model: CostModelData | None = None
    parameter_metadata: dict[str, ParameterMetadata] = Field(default_factory=dict)
    narrative: NarrativeData | None = None
    sources: SourcePaths
    # Count of *enabled* analyst override registry entries (Bet 4). Drives the
    # toggle label ("Apply analyst cost adjustments (N entries)") and the
    # hide/disable decision (INV-5). 0 for freeform/empty-registry concepts.
    # The full records (display) are Item 2's concern, not this field.
    analyst_override_count: int = 0
    # Full analyst override registry (Item 2). Every entry — enabled AND
    # disabled — carried through for the inspection panel; the count above is
    # just the enabled tally. Empty for freeform/empty-registry concepts.
    # Rides the concept payload (loaded once); the panel never fetches per click.
    overrides: list[OverrideRecord] = Field(default_factory=list)
    # True iff orchestrator routed this concept as `costingfe-asterisked`
    # (Comparison-Status, set on Grounding-Confidence: low). Render-side
    # signal for the comparison view's asterisk badge.
    asterisk_in_comparison: bool = False
    # Archetype-fit grade from tables/archetype_fit.csv, stamped at server load
    # (A3). One of "High"/"Med"/"Low"/"None" — where the *string* "None" is a
    # RECORDED grade (no costing-library archetype matches) and is distinct from
    # the field being absent (Python None = not recorded). Drives the honest
    # caveat marker (FR-A3.2). Absent on disk; None until stamped / when the
    # concept has no fit row.
    fit_grade: str | None = None

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
    asterisk_in_comparison: bool = False
    # Archetype-fit grade (A3) — carried on the lightweight manifest so landing
    # cards and the compare picker can render the caveat without a per-concept
    # fetch. Same semantics as ConceptData.fit_grade (string "None" = recorded).
    fit_grade: str | None = None
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
    # Per-concept toggle (explorer-slider-override-semantics, FR-SO5): when True
    # (default) the slider recompute, headline, and tornado describe the
    # analyst-applied LCOE; when False, the library-bare LCOE. Default True is
    # what makes FR-SO1 hold (no-op recompute reproduces the stored headline).
    apply_analyst_overrides: bool = True
    # Set server-side on POST; empty on default GET
    timestamp: str = ""


class ComputeRequest(BaseModel):
    """Request body for POST /api/compute (slider-driven recompute)."""

    concept_id: str
    overrides: dict[str, float]  # Param name → new value
    # FR-SO5: select the analyst-applied (True, default) vs library-bare (False)
    # LCOE function for the recompute. Optional with a True default so existing
    # callers/tests are unaffected. Rides the LRU cache key in _compute_cached.
    apply_analyst_overrides: bool = True


# ---------------------------------------------------------------------------
# Omit list (shared by extractor and server)
# ---------------------------------------------------------------------------

_OMIT_LIST_PATH = Path(__file__).parent / "omit_list.yaml"


def load_omit_list(path: Path | None = None) -> set[str]:
    """Load the set of concept IDs to exclude from the explorer.

    Reads the hand-authored ``omit_list.yaml`` (ID -> reason map) and returns
    just the set of IDs; the reasons are documentation for humans and are
    discarded here. This is the single shared reader for both enforcement
    points (extraction and the server), so each consumer enforces exclusion
    independently from one source of truth.

    Tolerant by design (FR-8): a missing or empty file yields an empty set
    (omit nothing). IDs are coerced to ``str`` so a numeric-looking YAML key
    such as ``26`` (which ``yaml.safe_load`` parses as the int ``26``) still
    matches the string IDs produced by ``parse_concept_id`` (e.g. ``"26"``).
    A malformed YAML file is left to raise — that is an authoring bug worth
    failing loudly on, not a no-op.
    """
    omit_path = path if path is not None else _OMIT_LIST_PATH
    if not omit_path.exists():
        return set()
    raw = yaml.safe_load(omit_path.read_text(encoding="utf-8"))
    if not raw:
        return set()
    return {str(key) for key in raw}


# ---------------------------------------------------------------------------
# Manifest and parameter index builders
# ---------------------------------------------------------------------------


def build_manifest(concepts: list[ConceptData]) -> ConceptManifest:
    """Build a ConceptManifest from extracted concepts."""
    entries: list[ConceptManifestEntry] = []
    for concept in concepts:
        lcoe: float | None = None
        confidence: Confidence | None = None

        if concept.cost_model is not None:
            lcoe = concept.cost_model.headline.lcoe_per_mwh

        if concept.parameter_metadata:
            conf_values = [pm.confidence for pm in concept.parameter_metadata.values()]
            # Pick the most common confidence level as the overall concept confidence
            counts = {c: conf_values.count(c) for c in set(conf_values)}
            confidence = max(counts, key=lambda c: counts[c])

        entries.append(
            ConceptManifestEntry(
                concept_id=concept.concept_id,
                name=concept.name,
                confinement_family=concept.confinement_family,
                company=concept.company,
                status=concept.status,
                illustration=concept.illustration,
                has_cost_model=concept.has_cost_model,
                has_sensitivities=concept.has_sensitivities,
                lcoe_per_mwh=lcoe,
                confidence=confidence,
                asterisk_in_comparison=concept.asterisk_in_comparison,
                fit_grade=concept.fit_grade,
                data_file=f"data/{concept.concept_id}.json",
            )
        )

    return ConceptManifest(
        generated_at=datetime.now(UTC).isoformat(),
        concepts=entries,
    )


def build_parameter_index(concepts: list[ConceptData]) -> ParameterIndex:
    """Build a cross-concept ParameterIndex from all sensitivity data."""
    # param_name → list of per-concept entries
    param_concepts: dict[str, list[ParameterConceptEntry]] = {}
    # param_name → (display_name, category) — first match wins
    param_info: dict[str, tuple[str, ParameterCategory]] = {}

    for concept in concepts:
        if concept.cost_model is None or concept.cost_model.sensitivities is None:
            continue

        sens = concept.cost_model.sensitivities
        all_entries = {**sens.engineering, **sens.financial}

        for param_name, entry in all_entries.items():
            param_concepts.setdefault(param_name, []).append(
                ParameterConceptEntry(
                    concept_id=concept.concept_id,
                    name=concept.name,
                    elasticity=entry.elasticity,
                )
            )
            if param_name not in param_info:
                pm = concept.parameter_metadata.get(param_name)
                if pm is not None:
                    param_info[param_name] = (pm.display_name, pm.category)
                else:
                    param_info[param_name] = (param_name, ParameterCategory.UNCLASSIFIED)

    parameters: dict[str, ParameterIndexEntry] = {
        param_name: ParameterIndexEntry(
            param_name=param_name,
            display_name=param_info[param_name][0],
            category=param_info[param_name][1],
            concepts=concept_entries,
        )
        for param_name, concept_entries in param_concepts.items()
    }

    return ParameterIndex(parameters=parameters)


# ---------------------------------------------------------------------------
# Cost landscape (Theme F) — the cross-concept LCOE-decomposition aggregate
# ---------------------------------------------------------------------------


class CostComponent(StrEnum):
    """The four annualised LCOE segments the cost-landscape bar stacks.

    These are the only buckets additive to the headline LCOE (capital = CAS90
    annualised charge, fixed_om = CAS71, replacement = CAS72, fuel = CAS80). The
    single authority for the segment vocabulary on both the override roll-up and
    the front-end traces.
    """

    CAPITAL = "capital"
    FIXED_OM = "fixed_om"
    REPLACEMENT = "replacement"
    FUEL = "fuel"


class CostComponents(BaseModel):
    """A concept's annualised cost components, in M$ (the bar's raw inputs).

    ``capital`` (CAS90) and ``fuel`` (CAS80) are always present. The O&M split —
    ``fixed_om`` (CAS71) and ``replacement`` (CAS72) — is ``None`` when the
    concept's cost model never separated it (honest degradation; the front-end
    then renders a single combined-O&M segment). ``om_combined`` (CAS70) is
    always present and equals ``fixed_om + replacement`` when the split exists —
    it is what the combined-O&M segment draws from when the split is absent.

    Values are raw M$; the page derives each segment's $/MWh as
    ``component / (capital + om_combined + fuel) × lcoe`` (D2).
    """

    capital: float  # CAS90 annualised capital charge
    fixed_om: float | None  # CAS71; None when the split is not recorded
    replacement: float | None  # CAS72; None when the split is not recorded
    fuel: float  # CAS80
    om_combined: float  # CAS70 = fixed_om + replacement (always present)


class CompactOverride(BaseModel):
    """One analyst override, projected to what the cost-landscape hover needs.

    A summary projection of ``OverrideRecord``: which segment the override lands
    on (``component``), its source, a one-line ``rationale_short``, and the
    enabled/blocked state. The full multi-paragraph rationale stays on the
    concept page (D6) — this is the summary-on-hover, not the whole story.

    ``source`` and ``rationale_short`` are ``str | None``: a genuinely absent
    field stays ``None`` (the front-end renders an explicit "not recorded",
    FR-F10), never coerced to "".
    """

    account: str  # CAS code as authored, e.g. "C220103" or "CAS70"
    component: CostComponent  # which annualised segment this override lands on
    source: str | None  # free-text citation, or None when not recorded
    rationale_short: str | None  # first sentence / structured basis, or None
    enabled: bool  # False entries are recorded but not applied
    blocked_by: str | None  # "<org>/<repo>#NN" when disabled, else None


class CostLandscapeEntry(BaseModel):
    """One costed concept's row in the cost-landscape aggregate."""

    concept_id: str
    lcoe: float  # headline LCOE [$/MWh] — the bar's total height
    components: CostComponents
    overrides: list[CompactOverride]


class CostLandscape(BaseModel):
    """The cross-concept cost-decomposition aggregate served at /api/cost-landscape.

    One entry per costed concept with a finite headline LCOE; non-costed and
    non-finite-LCOE concepts are absent (the page renders only costed concepts
    and accounts for any it drops, I5/FR-F10). Outlier (in-range) filtering is a
    page concern (D5), not this aggregate's.
    """

    generated_at: str  # ISO 8601 timestamp
    concepts: list[CostLandscapeEntry]


# CAS10–CAS60 top-level accounts: the overnight-capital accounts that feed the
# annualised capital charge (CAS90). Every analyst capital override lands here
# or on a CAS22 sub-account (C22*); both roll up to the capital segment (I6).
_CAPITAL_TOP_ACCOUNTS: frozenset[str] = frozenset(
    {
        "CAS10", "CAS21", "CAS22", "CAS23", "CAS24", "CAS25", "CAS26", "CAS27",
        "CAS28", "CAS29", "CAS30", "CAS40", "CAS50", "CAS60",
    }
)

_RATIONALE_SHORT_MAX = 200

# Abbreviations whose trailing period is not a sentence end — without these, a
# rationale like "Sorbom et al. 2015 reports…" truncates to a useless "Sorbom
# et al." Stored lowercased and period-stripped for comparison.
_SENTENCE_ABBREVIATIONS: frozenset[str] = frozenset(
    {"al", "e.g", "i.e", "etc", "vs", "cf", "fig", "no", "eq", "ref", "approx", "est"}
)


def _override_component(account: str) -> CostComponent:
    """Map an override's CAS account to its annualised LCOE segment (I6).

    Total over the registry's account vocabulary by construction:

    * ``CAS70`` (combined O&M) and ``CAS71`` (fixed O&M) → ``fixed_om``. Analysts
      author O&M overrides at the combined ``CAS70`` level, which has no split of
      its own; it lands on the O&M segment (the dominant, persistent component).
    * ``CAS72`` → ``replacement``; ``CAS80`` → ``fuel``.
    * Every capital account — CAS10–60 and every CAS22 sub-account (``C22*``) →
      ``capital`` (the segment is the annualised CAS90 charge those costs feed).

    An account outside this vocabulary raises: a cost account the landscape can't
    attribute is a real gap to surface, not something to silently bucket.
    """
    a = account.strip().upper()
    if a in {"CAS70", "CAS71"}:
        return CostComponent.FIXED_OM
    if a == "CAS72":
        return CostComponent.REPLACEMENT
    if a == "CAS80":
        return CostComponent.FUEL
    if a.startswith("C22") or a in _CAPITAL_TOP_ACCOUNTS:
        return CostComponent.CAPITAL
    raise ValueError(
        f"override account {account!r} has no LCOE-component mapping (I6) — "
        "extend the cost-landscape roll-up to cover it"
    )


def _first_sentence(text: str, max_len: int) -> str:
    """First sentence of *text* (whitespace collapsed), capped at *max_len*.

    Treats ``". "`` as a sentence boundary, but skips boundaries that fall after
    a known abbreviation (``et al.``, ``e.g.``, …) so a citation-heavy rationale
    yields a real sentence rather than a truncated fragment.
    """
    collapsed = " ".join(text.split())
    start = 0
    sentence = collapsed
    while True:
        end = collapsed.find(". ", start)
        if end == -1:
            break
        last_word = collapsed[:end].rsplit(" ", 1)[-1].lower().rstrip(".")
        if last_word in _SENTENCE_ABBREVIATIONS:
            start = end + 2
            continue
        sentence = collapsed[: end + 1]
        break
    if len(sentence) > max_len:
        sentence = sentence[:max_len].rstrip() + "…"
    return sentence


def _override_rationale_short(override: OverrideRecord) -> str | None:
    """A one-line rationale for the hover, or None when nothing was recorded.

    Prefers the first sentence of the analyst prose rationale; when no prose was
    recorded, surfaces the structured basis/provenance so the hover still shows
    *recorded* context. Returns None only when neither exists — the front-end
    renders that as an explicit "not recorded" (FR-F10), never a fabricated note.
    """
    if override.rationale:
        return _first_sentence(override.rationale, _RATIONALE_SHORT_MAX)
    recorded = [b for b in (override.cost_basis, override.provenance) if b]
    return " · ".join(recorded) if recorded else None


def build_cost_landscape(concepts: list[ConceptData]) -> CostLandscape:
    """Build the cost-landscape aggregate from in-memory concepts (pure).

    Includes every concept with a cost model and a finite headline LCOE, sorted
    by concept_id for deterministic output. Each entry carries the annualised
    components (raw M$) and the analyst overrides projected onto their segments.
    Concepts without a cost model, or with a non-finite LCOE, are omitted — the
    page renders only costed concepts and accounts for any it excludes (I5).
    """
    entries: list[CostLandscapeEntry] = []
    for concept in sorted(concepts, key=lambda c: c.concept_id):
        cm = concept.cost_model
        if cm is None:
            continue
        lcoe = cm.headline.lcoe_per_mwh
        if not math.isfinite(lcoe):
            continue

        components = CostComponents(
            capital=cm.cas90.cost_m_usd,
            fixed_om=cm.cas71.cost_m_usd if cm.cas71 is not None else None,
            replacement=cm.cas72.cost_m_usd if cm.cas72 is not None else None,
            fuel=cm.cas80.cost_m_usd,
            om_combined=cm.cas70.cost_m_usd,
        )
        overrides = [
            CompactOverride(
                account=ov.account,
                component=_override_component(ov.account),
                source=ov.source,
                rationale_short=_override_rationale_short(ov),
                enabled=ov.enabled,
                blocked_by=ov.blocked_by,
            )
            for ov in concept.overrides
        ]
        entries.append(
            CostLandscapeEntry(
                concept_id=concept.concept_id,
                lcoe=lcoe,
                components=components,
                overrides=overrides,
            )
        )

    return CostLandscape(generated_at=datetime.now(UTC).isoformat(), concepts=entries)
