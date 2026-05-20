"""Embedding rulebook.

Every embedding is a small pure function over declared feature inputs that
returns a 1-5 scalar. Registration is explicit via @embedding(name, inputs).

Lookup-table-based embeddings (modularity v5, supply chain, etc.) may
additionally declare a keyword-only `weights_yaml` parameter; the
@embedding decorator detects this at registration time and the score
driver supplies the parsed weights dict at evaluation time.

The module-level REGISTRY is what score.py iterates. No file I/O, no LLM calls,
no global state. Static check: this file imports neither yaml, csv, nor any
LLM client.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Callable

EmbeddingFn = Callable[..., float | int | None]


@dataclass(frozen=True)
class Embedding:
    name: str
    inputs: tuple[str, ...]
    fn: EmbeddingFn
    needs_weights: bool = False  # set True iff fn has a `weights_yaml` parameter


REGISTRY: dict[str, Embedding] = {}


def embedding(name: str, inputs: list[str]) -> Callable[[EmbeddingFn], EmbeddingFn]:
    def _wrap(fn: EmbeddingFn) -> EmbeddingFn:
        if name in REGISTRY:
            raise ValueError(f"embedding {name!r} already registered")
        sig = inspect.signature(fn)
        needs_weights = "weights_yaml" in sig.parameters
        REGISTRY[name] = Embedding(
            name=name, inputs=tuple(inputs), fn=fn, needs_weights=needs_weights
        )
        return fn
    return _wrap


# =============================================================================
# Modularity axis (v5 three-component formula)
#
#   score = 0.50 × mvs + 0.25 × percent_mod + 0.25 × unit_multiplicity
#
# percent_mod is the capex-weighted average of three subsystem modularity
# ratings (vessel, magnet/driver, blanket). The four other subsystems
# (BOP, fuel cycle, aux, civil) are excluded per v5 calibration.
#
# All four lookups (mvs, vessel, magnet/driver, blanket) live in
# weights/default.yaml under the `modularity:` block; the embeddings read
# them via the `weights_yaml` kwarg. The key-builder helpers below
# implement the disambiguation rules (Tokamak shape split, Z-pinch vs
# Mirror via primary_heating, Xcimer-class via driver_technology, BEST
# LTS-override, MagLIF identification, etc.).
# =============================================================================


# ----- Module-level helper data ---------------------------------------------

_TARGET_USING_IFE_DRIVERS = {"Laser", "Heavy ion beam", "Projectile"}


def _is_lts_override(magnet_type: str) -> bool:
    """BEST-style LTS override: any 'LTS' substring routes a tokamak to the
    non-compact lookup branch even if tokamak_shape says Compact.

    BEST is tagged tokamak_shape=Compact in the v3 ontology but the v5
    matrix treats it as non-compact (large LTS coil set, single bespoke).
    The deterministic disambiguation rule is: presence of "LTS" in the
    magnet_type string overrides the compact-shape default.
    """
    return "LTS" in (magnet_type or "")


# ----- mvs (minimum viable device scale) ------------------------------------


def _mvs_key(
    cf: str, mfe_top: str, ife_driver: str, mif_method: str,
    nsm: str, tok_shape: str, driver_tech: str, magnet_type: str,
    primary_heating: str, laser_approach: str,
) -> str | None:
    """Build the (Confinement Family | Concept) key for mvs_lookup.

    Disambiguates entirely from declared features (no concept_id sniffing):
      - Tokamak shape → "compact" / "spherical" / "negative-T" / "non-compact"
      - LTS magnets in a tokamak override compact-shape → non-compact (BEST)
      - Open/Linear: primary_heating="Ohmic (self-pinch)" → Z-pinch; else Mirror
      - MIF: primary_heating="Pulsed power implosion" → MagLIF; mif_method
        contains "FRC" → FRC compression; else Pneumatic compression
      - IFE Laser: laser_approach="Liquid jet" → Laser (liquid jet);
                   driver_tech contains "KrF"/"excimer" → Xcimer-class
      - Dipole: orbital variant collapses to plain "Levitated dipole" for
        mvs purposes (lookup-key-equal; the spec gives both mvs=3)
    """
    drv_lower = (driver_tech or "").lower()
    ph = primary_heating or ""

    if cf == "MFE":
        if mfe_top == "Tokamak":
            if _is_lts_override(magnet_type):
                return "MFE|Tokamak (non-compact)"
            if tok_shape == "Compact":
                return "MFE|Tokamak (compact)"
            if tok_shape == "Spherical":
                return "MFE|Tokamak (spherical)"
            if tok_shape == "Negative triangularity":
                return "MFE|Tokamak (negative-T)"
            return "MFE|Tokamak (non-compact)"
        if mfe_top == "Stellarator":
            return "MFE|Stellarator"
        if mfe_top == "Compact Toroid":
            return "MFE|FRC"
        if mfe_top == "Open/Linear":
            if ph == "Ohmic (self-pinch)" or "pinch" in drv_lower:
                return "MFE|Z-pinch (sheared-flow)"
            return "MFE|Mirror"
        if mfe_top == "Dipole":
            return "MFE|Levitated dipole"
        return "MFE|Other"

    if cf == "MIF":
        if ph == "Pulsed power implosion":
            return "MIF|MagLIF"
        if "FRC" in (mif_method or ""):
            return "MIF|FRC compression"
        # Magnetized target / pneumatic / mechanical compression collapse here
        return "MIF|Pneumatic compression"

    if cf == "IFE":
        if ife_driver == "Laser":
            if "krf" in drv_lower or "excimer" in drv_lower:
                return "IFE|Laser (Xcimer-class)"
            if (laser_approach or "") == "Liquid jet":
                return "IFE|Laser (liquid jet)"
            return "IFE|Laser"
        if ife_driver == "Heavy ion beam":
            return "IFE|Heavy ion beam"
        if ife_driver == "Projectile":
            return "IFE|Projectile"
        if ife_driver == "Acoustic":
            return "IFE|Acoustic"
        return None

    if cf == "Non-Standard":
        n = (nsm or "").lower()
        # SHINE-style accelerator first (overrides nsm="Electrostatic")
        if "accelerator" in drv_lower or "particle accelerator" in drv_lower:
            return "Non-Standard|Particle accelerator"
        if "electrostatic" in n:
            return "Non-Standard|Electrostatic"
        if "plasma focus" in n:
            return "Non-Standard|Plasma focus"
        if "muon" in n:
            return "Non-Standard|Muon-catalyzed"
        if "accelerator" in n or "particle" in n:
            return "Non-Standard|Particle accelerator"
        return None

    return None


@embedding(
    "min_viable_device_scale",
    inputs=[
        "confinement_family", "mfe_topology", "ife_driver",
        "mif_method", "non_standard_mechanism", "tokamak_shape",
        "driver_technology", "magnet_type", "primary_heating",
        "laser_approach",
    ],
)
def _min_viable_device_scale(
    confinement_family: str, mfe_topology: str, ife_driver: str,
    mif_method: str, non_standard_mechanism: str, tokamak_shape: str,
    driver_technology: str, magnet_type: str, primary_heating: str,
    laser_approach: str,
    *, weights_yaml: dict,
) -> float | None:
    """mvs (minimum viable device scale) rating, 1-5.

    Lookup in weights_yaml['modularity']['mvs_lookup']. The test suite
    enforces full coverage so missing-key fallback should never fire.
    """
    key = _mvs_key(
        confinement_family, mfe_topology, ife_driver, mif_method,
        non_standard_mechanism, tokamak_shape, driver_technology, magnet_type,
        primary_heating, laser_approach,
    )
    lookup = weights_yaml.get("modularity", {}).get("mvs_lookup", {})
    if key is None:
        return None
    if key not in lookup:
        return None
    return float(lookup[key])


# ----- unit_multiplicity ----------------------------------------------------


@embedding(
    "unit_multiplicity",
    inputs=["unit_count_estimate"],
)
def _unit_multiplicity(
    unit_count_estimate: int,
    *, weights_yaml: dict,
) -> float:
    """unit_multiplicity rating, 1-5. Bracket lookup on unit_count_estimate.

    Brackets per v5: N=1 → 1, N=2 → 2, N=5-10 → 3, N=15-30 → 4, N≥50 → 5.
    The curve saturates at unit_count_floor_score (default 5) — beyond N=50
    additional copies don't add modularity.
    """
    if unit_count_estimate is None or unit_count_estimate < 1:
        return 1.0
    cfg = weights_yaml.get("modularity", {})
    brackets = cfg.get("unit_count_brackets", [])
    floor = float(cfg.get("unit_count_floor_score", 5.0))
    for bracket in brackets:
        if unit_count_estimate <= bracket["max_count"]:
            return float(bracket["score"])
    return floor


# ----- vessel modularity rating ---------------------------------------------


def _vessel_key(
    cf: str, mfe_top: str, tok_shape: str, mif_method: str,
    ife_driver: str, nsm: str, fuel: str, magnet_type: str,
) -> str | None:
    """Build the vessel_lookup key.

    Mirror disambiguation isn't needed (Mirror and Z-pinch both score 3
    via MFE|Mirror|* and MFE|Z-pinch|*; both keys are pre-populated). The
    LTS override is applied for tokamaks (same rule as mvs).
    """
    if cf == "MFE":
        if mfe_top == "Tokamak":
            if _is_lts_override(magnet_type):
                return "MFE|Tokamak|non-compact"
            if tok_shape == "Compact":
                return "MFE|Tokamak|compact"
            if tok_shape == "Spherical":
                return "MFE|Tokamak|spherical"
            return "MFE|Tokamak|non-compact"
        if mfe_top == "Stellarator":
            return "MFE|Stellarator|*"
        if mfe_top == "Compact Toroid":
            return "MFE|FRC|*"
        if mfe_top == "Open/Linear":
            # Pinch vs Mirror — both score 3, but keep the keys distinct
            # for traceability in the diagnostic block.
            return "MFE|Mirror|*"   # both Mirror & Z-pinch map to 3 here
        if mfe_top == "Dipole":
            return "MFE|Dipole|*"
        return "MFE|Other|*"
    if cf == "MIF":
        if "MagLIF" in (mif_method or ""):
            return "MIF|MagLIF|*"
        if "FRC" in (mif_method or ""):
            return "MIF|FRC compression|*"
        # Pneumatic / Magnetized target — fuel split
        return f"MIF|Pneumatic compression|{fuel}"
    if cf == "IFE":
        return f"IFE|{ife_driver}|*"
    if cf == "Non-Standard":
        n = (nsm or "").lower()
        if "electrostatic" in n:
            return "Non-Standard|Electrostatic|*"
        if "plasma focus" in n:
            return "Non-Standard|Plasma focus|*"
        if "muon" in n:
            return "Non-Standard|Muon-catalyzed|*"
        if "accelerator" in n or "particle" in n:
            return "Non-Standard|Particle accelerator|*"
        return None
    return None


@embedding(
    "vessel_modularity_rating",
    inputs=[
        "confinement_family", "mfe_topology", "tokamak_shape",
        "mif_method", "ife_driver", "non_standard_mechanism",
        "fuel", "magnet_type",
    ],
)
def _vessel_modularity_rating(
    confinement_family: str, mfe_topology: str, tokamak_shape: str,
    mif_method: str, ife_driver: str, non_standard_mechanism: str,
    fuel: str, magnet_type: str,
    *, weights_yaml: dict,
) -> float | None:
    """Vessel subsystem modularity rating, 1-5."""
    lookup = weights_yaml.get("modularity", {}).get("vessel_lookup", {})
    key = _vessel_key(
        confinement_family, mfe_topology, tokamak_shape,
        mif_method, ife_driver, non_standard_mechanism, fuel, magnet_type,
    )
    if key is None or key not in lookup:
        return None
    return float(lookup[key])


# ----- magnet/driver modularity rating --------------------------------------


def _magnet_driver_key(
    cf: str, magnet_type: str, driver_tech: str, mfe_top: str,
    stellarator_type: str, ife_driver: str, mif_method: str, nsm: str,
    primary_heating: str,
) -> str | None:
    """Build the magnet_driver_lookup key.

    MFE keys by magnet_type with two special cases:
      - primary_heating="Ohmic (self-pinch)" → Magnetic pinch (Z-pinch)
      - mfe_topology=Stellarator AND stellarator_type="Helical coil" →
        continuous helical (Helical Fusion's continuous winding)
    TBD / "None" / missing magnet_type → MFE fallback.

    MIF / IFE / Non-Standard key by driver_technology / driver category.
    Non-Standard Electrostatic disambiguates accelerator concepts (SHINE)
    via driver_technology contains "accelerator".
    """
    drv = driver_tech or ""
    drv_lower = drv.lower()

    if cf == "MFE":
        # Z-pinch special case: detect via primary_heating
        if primary_heating == "Ohmic (self-pinch)":
            return "MFE|Magnetic pinch|*"
        # Helical Fusion's continuous winding: stellarator_type
        if mfe_top == "Stellarator" and stellarator_type == "Helical coil":
            return "MFE|HTS (continuous helical)|*"
        mt = magnet_type or ""
        mt_lower = mt.lower()
        # Match LTS combos BEFORE the bare-HTS check (they share "HTS" substring)
        if "LTS+HTS" in mt or "LTS/HTS" in mt:
            return "MFE|LTS+HTS|*"
        if "LTS" in mt:
            return "MFE|LTS|*"
        if "HTS" in mt and ("wound" in mt_lower or "wind" in mt_lower):
            return "MFE|HTS (wound)|*"
        if "HTS" in mt and "integrated" in mt_lower:
            return "MFE|HTS (integrated)|*"
        if "HTS" in mt and "planar" in mt_lower:
            return "MFE|HTS (planar)|*"
        if "HTS" in mt and ("segment" in mt_lower or "modular" in mt_lower):
            return "MFE|HTS (segmented)|*"
        if "HTS" in mt and ("helical" in mt_lower or "3d" in mt_lower):
            return "MFE|HTS (continuous helical)|*"
        if "HTS" in mt:
            # Generic HTS → treat as wound (matches CFS / ENN class)
            return "MFE|HTS (wound)|*"
        if "Resistive" in mt or "resistive" in mt_lower:
            return "MFE|Resistive|*"
        if mt == "TBD":
            return "MFE|TBD|*"
        if mt in ("", "N/A", "None"):
            return "MFE|N/A|*"
        return "MFE|*|*"   # exotic — fall through to generic MFE fallback

    if cf == "MIF":
        if "pulsed power" in drv_lower or "marx" in drv_lower:
            return "MIF|*|Pulsed power"
        if "pneumatic" in drv_lower or "piston" in drv_lower:
            return "MIF|*|Pneumatic"
        if "capacitor" in drv_lower:
            return "MIF|*|Capacitor compression"
        if "railgun" in drv_lower:
            return "MIF|*|Railgun"
        if "MagLIF" in (mif_method or ""):
            return "MIF|*|Pulsed power"
        if "FRC" in (mif_method or ""):
            return "MIF|*|Capacitor compression"
        if "Pneumatic" in (mif_method or "") or "pneumatic" in (mif_method or "").lower():
            return "MIF|*|Pneumatic"
        return "MIF|*|*"

    if cf == "IFE":
        if ife_driver == "Laser":
            if "krf" in drv_lower or "excimer" in drv_lower or "gas laser" in drv_lower:
                return "IFE|*|Gas Laser"
            return "IFE|*|DPSSL Laser"
        if ife_driver == "Heavy ion beam":
            return "IFE|*|Heavy ion beam"
        if ife_driver == "Projectile":
            return "IFE|*|Projectile"
        if ife_driver == "Acoustic":
            return "IFE|*|Acoustic"
        return "IFE|*|*"

    if cf == "Non-Standard":
        n = (nsm or "").lower()
        # SHINE-style accelerator disambiguation: detect via driver_tech
        if "accelerator" in drv_lower or "particle accelerator" in drv_lower:
            return "Non-Standard|*|Particle accelerator"
        if "electrostatic" in n:
            return "Non-Standard|*|IEC"
        if "plasma focus" in n:
            return "Non-Standard|*|Plasma focus"
        if "accelerator" in n or "particle" in n:
            return "Non-Standard|*|Particle accelerator"
        if "muon" in n or "muon" in drv_lower:
            return "Non-Standard|*|Muon catalysis"
        return "Non-Standard|*|*"

    return None


@embedding(
    "magnet_driver_modularity_rating",
    inputs=[
        "confinement_family", "magnet_type", "driver_technology",
        "mfe_topology", "stellarator_type", "ife_driver", "mif_method",
        "non_standard_mechanism", "primary_heating",
    ],
)
def _magnet_driver_modularity_rating(
    confinement_family: str, magnet_type: str, driver_technology: str,
    mfe_topology: str, stellarator_type: str, ife_driver: str, mif_method: str,
    non_standard_mechanism: str, primary_heating: str,
    *, weights_yaml: dict,
) -> float | None:
    """Magnet/driver subsystem modularity rating, 1-5."""
    lookup = weights_yaml.get("modularity", {}).get("magnet_driver_lookup", {})
    key = _magnet_driver_key(
        confinement_family, magnet_type, driver_technology, mfe_topology,
        stellarator_type, ife_driver, mif_method, non_standard_mechanism,
        primary_heating,
    )
    if key is None or key not in lookup:
        return None
    return float(lookup[key])


# ----- blanket modularity rating --------------------------------------------


@embedding(
    "blanket_modularity_rating",
    inputs=["fuel", "blanket_config"],
)
def _blanket_modularity_rating(
    fuel: str, blanket_config: str,
    *, weights_yaml: dict,
) -> float | None:
    """Blanket subsystem modularity rating, 1-5."""
    lookup = weights_yaml.get("modularity", {}).get("blanket_lookup", {})
    # Aneutronic / no-tritium fuels short-circuit blanket_config
    if fuel in ("p-B11", "D-D", "D-He3"):
        return float(lookup.get(f"{fuel}|*", 5.0))
    # D-T: TBD → liquid metal default (per framework-wide TBD rule)
    effective_blanket = "Liquid metal" if blanket_config == "TBD" else blanket_config
    key = f"{fuel}|{effective_blanket}"
    if key not in lookup:
        return None
    return float(lookup[key])


# ----- percent_mod (capex-weighted average of 3 subsystem ratings) ----------


_PERCENT_MOD_SPARSE_THRESHOLD = 0.30


@embedding(
    "percent_mod",
    inputs=[
        "vessel_modularity_rating", "magnet_driver_modularity_rating",
        "blanket_modularity_rating", "w_vessel", "w_coils", "w_blanket",
    ],
)
def _percent_mod(
    vessel_modularity_rating: float,
    magnet_driver_modularity_rating: float,
    blanket_modularity_rating: float,
    w_vessel: float | None,
    w_coils: float | None,
    w_blanket: float | None,
) -> float | None:
    """Percent modularization: capex-weighted average of three subsystem ratings.

    Renormalizes (w_vessel, w_coils, w_blanket) to sum to 1.0 within this
    embedding (the source shares sum to 1.0 across all 7 subsystems; we
    drop the other 4 and rescale within the retained 3).

    Falls back to equal weighting (1/3 each) in any of three cases:
      1. The concept lacks a model_output.txt (any w_* is None).
      2. The sum of the three retained shares is non-positive (parser
         classified zero dollars to all three).
      3. The sum of the three retained shares is below
         `_PERCENT_MOD_SPARSE_THRESHOLD` (0.30) of plant cost — the
         signal is too sparse to support a confident cost-weighted blend.
         This is the v5-calibration "equal-weight backstop": prevents one
         subsystem with a tiny non-zero share from dominating the score.

    Returns None only if any of the three subsystem ratings is None
    (incomplete lookup coverage).
    """
    ratings = (vessel_modularity_rating, magnet_driver_modularity_rating,
               blanket_modularity_rating)
    if any(r is None for r in ratings):
        return None

    weights = (w_vessel, w_coils, w_blanket)
    if any(w is None for w in weights):
        return sum(ratings) / 3.0

    total = sum(float(w) for w in weights)
    if total <= 0 or total < _PERCENT_MOD_SPARSE_THRESHOLD:
        return sum(ratings) / 3.0

    return (
        (float(w_vessel)  / total) * vessel_modularity_rating
        + (float(w_coils)   / total) * magnet_driver_modularity_rating
        + (float(w_blanket) / total) * blanket_modularity_rating
    )


# =============================================================================
# Supply Chain axis (penalty-stack)
#
#   score = max(1.0, 5.0 - sum(severity_weights_of_triggered_bottlenecks))
#
# 7 bottlenecks: helium3 (Critical 3.0), tritium/li6/Be/V (Severe 1.0 each),
# FLiBe/KDP (Moderate 0.5 each). All triggers use v0.3.0 controlled-
# vocabulary features (fuel / blanket_config / confinement_family /
# primary_heating).
# =============================================================================

_BOTTLENECK_NAMES = (
    "tritium", "lithium6", "helium3", "beryllium",
    "vanadium", "flibe", "kdp",
)

_BREEDING_BLANKET_VALUES = {"Liquid metal", "Molten salt", "Solid breeder", "Other/hybrid"}
_BERYLLIUM_BLANKET_VALUES = {"Solid breeder", "Molten salt", "Other/hybrid"}


def _load_bottleneck_weights(weights_yaml: dict) -> dict[str, float]:
    """Extract bottleneck severity weights from weights/default.yaml.

    Fail-loud if any of the seven expected weights is missing — silent
    defaults to zero would silently produce wrong scores.
    """
    raw = (weights_yaml.get("supply_chain", {})
                       .get("bottleneck_severity_weights", {}))
    missing = [b for b in _BOTTLENECK_NAMES if b not in raw]
    if missing:
        raise ValueError(
            f"weights/default.yaml supply_chain.bottleneck_severity_weights "
            f"missing required keys: {missing}"
        )
    return {b: float(raw[b]) for b in _BOTTLENECK_NAMES}


def _compute_triggered_bottlenecks(
    fuel: str, blanket_config: str, confinement_family: str,
    primary_heating: str, weights: dict[str, float],
) -> dict[str, float]:
    """Pure rule application: features + weights → triggered bottlenecks.

    TBD blanket defaults to "Liquid metal" (matches the framework-wide
    TBD rule); the diagnostic block records this assumption.
    """
    raw_blanket = blanket_config or ""
    blanket = "Liquid metal" if raw_blanket == "TBD" else raw_blanket
    cf = confinement_family or ""
    heating = primary_heating or ""
    triggered: dict[str, float] = {}

    if fuel == "D-T":
        triggered["tritium"] = weights["tritium"]
        if blanket in _BREEDING_BLANKET_VALUES:
            triggered["lithium6"] = weights["lithium6"]
        if blanket in _BERYLLIUM_BLANKET_VALUES:
            triggered["beryllium"] = weights["beryllium"]
        if blanket == "Liquid metal":
            triggered["vanadium"] = weights["vanadium"]
        if blanket == "Molten salt":
            triggered["flibe"] = weights["flibe"]
    elif fuel == "D-He3":
        triggered["helium3"] = weights["helium3"]

    if cf == "IFE" and heating.startswith("Laser"):
        triggered["kdp"] = weights["kdp"]

    return triggered


@embedding(
    "bottleneck_weight",
    inputs=["fuel", "blanket_config", "confinement_family", "primary_heating"],
)
def _bottleneck_weight(
    fuel: str, blanket_config: str, confinement_family: str,
    primary_heating: str,
    *, weights_yaml: dict,
) -> float:
    """Sum of severity weights of all triggered bottlenecks."""
    sev = _load_bottleneck_weights(weights_yaml)
    triggered = _compute_triggered_bottlenecks(
        fuel, blanket_config, confinement_family, primary_heating, sev,
    )
    return sum(triggered.values())


@embedding(
    "supply_chain_score",
    inputs=["bottleneck_weight"],
)
def _supply_chain_score(bottleneck_weight: float) -> float:
    """Supply chain axis score: floor 1.0, ceiling 5.0."""
    return max(1.0, 5.0 - bottleneck_weight)


# =============================================================================
# Customization axis (two sub-factors + rescale to 1-5)
#
#   raw = (thermal_rejection_score + fuel_safety_score) / 2     # 1.0 - 4.0
#   score = 1.0 + (raw - 1.0) * (4.0 / 3.0)                     # 1.0 - 5.0
#
# Ported from C5 framework. Both sub-factors are 1-4; the rescale stretches
# the natural [1, 4] range onto the framework's [1, 5] scale.
# =============================================================================


def _load_customization_weights(weights_yaml: dict) -> tuple[dict, dict]:
    """Load (thermal_rejection_scores, fuel_safety_scores) from default.yaml."""
    cust = weights_yaml.get("customization", {})
    trs = cust.get("thermal_rejection_scores")
    fss = cust.get("fuel_safety_scores")
    if trs is None or fss is None:
        raise ValueError(
            "weights/default.yaml customization axis missing "
            "thermal_rejection_scores or fuel_safety_scores"
        )
    required_thermal = {"direct_conversion", "hybrid", "thermal"}
    missing_t = required_thermal - set(trs)
    if missing_t:
        raise ValueError(
            f"customization.thermal_rejection_scores missing keys: {missing_t}"
        )
    required_fuel = {"p-B11", "D-He3", "D-D", "D-T"}
    missing_f = required_fuel - set(fss)
    if missing_f:
        raise ValueError(
            f"customization.fuel_safety_scores missing keys: {missing_f}"
        )
    return ({k: int(v) for k, v in trs.items()},
            {k: int(v) for k, v in fss.items()})


def _classify_thermal_rejection(energy_capture: str) -> str:
    """Map energy_capture (v0.3.0 vocab) to direct_conversion / hybrid / thermal.

    Thermal (*) / Pulsed power / Projectile impact / Neutron applications /
    TBD all collapse to the standard-thermal bucket.
    """
    energy = energy_capture or ""
    if energy.startswith("Direct"):
        return "direct_conversion"
    if energy == "Hybrid (thermal + direct)":
        return "hybrid"
    return "thermal"


@embedding(
    "thermal_rejection_score",
    inputs=["energy_capture"],
)
def _thermal_rejection_score(
    energy_capture: str,
    *, weights_yaml: dict,
) -> int:
    """Sub-factor A: thermal-rejection footprint, 1-4."""
    trs, _ = _load_customization_weights(weights_yaml)
    return trs[_classify_thermal_rejection(energy_capture)]


@embedding(
    "fuel_safety_score",
    inputs=["fuel"],
)
def _fuel_safety_score(
    fuel: str,
    *, weights_yaml: dict,
) -> int:
    """Sub-factor B: fuel safety profile, 1-4. Unknown/missing → conservative D-T."""
    _, fss = _load_customization_weights(weights_yaml)
    if not fuel or fuel == "Unknown":
        return fss["D-T"]
    if fuel not in fss:
        raise ValueError(f"unknown fuel {fuel!r}; expected one of {sorted(fss)}")
    return fss[fuel]


@embedding(
    "customization_score",
    inputs=["thermal_rejection_score", "fuel_safety_score"],
)
def _customization_score(
    thermal_rejection_score: int, fuel_safety_score: int,
) -> float:
    """Customization axis score: rescaled (A+B)/2 to [1.0, 5.0]."""
    raw = (thermal_rejection_score + fuel_safety_score) / 2.0
    return round(1.0 + (raw - 1.0) * (4.0 / 3.0), 2)


# =============================================================================
# Upper Capacity Factor axis (penalty-stack)
#
#   score = max(1.0, 5.0 - sum(severity_weights_of_triggered_penalties))
#
# 3 operational penalties: pulsed (Moderate 0.5), neutronic fuel (Severe
# 1.0), non-renewable blanket conditional on neutronic (Moderate 0.5).
# =============================================================================

_UPPER_CF_PENALTY_NAMES = (
    "pulsed_operation",
    "neutronic_fuel",
    "non_renewable_blanket",
)

_NEUTRONIC_FUELS = {"D-T", "D-D"}
_STATIC_BLANKET_VALUES = {"Solid breeder", "Molten salt", "Other/hybrid"}
_PULSED_OPERATION_MODES = {"Pulsed"}


def _load_upper_cf_weights(weights_yaml: dict) -> dict[str, float]:
    """Extract operational penalty weights from weights/default.yaml."""
    raw = (weights_yaml.get("upper_cf", {})
                       .get("operational_penalty_weights", {}))
    missing = [p for p in _UPPER_CF_PENALTY_NAMES if p not in raw]
    if missing:
        raise ValueError(
            f"weights/default.yaml upper_cf.operational_penalty_weights "
            f"missing required keys: {missing}"
        )
    return {p: float(raw[p]) for p in _UPPER_CF_PENALTY_NAMES}


def _compute_triggered_cf_penalties(
    fuel: str, blanket_config: str, operation_mode: str,
    weights: dict[str, float],
) -> dict[str, float]:
    """Pure rule application — returns dict of triggered penalty weights.

    TBD blanket → Liquid metal default; Liquid metal is renewable so a
    TBD-defaulted blanket does NOT trigger non_renewable_blanket.
    """
    raw_blanket = blanket_config or ""
    blanket = "Liquid metal" if raw_blanket == "TBD" else raw_blanket
    op_mode = operation_mode or ""
    triggered: dict[str, float] = {}

    if op_mode in _PULSED_OPERATION_MODES:
        triggered["pulsed_operation"] = weights["pulsed_operation"]
    if fuel in _NEUTRONIC_FUELS:
        triggered["neutronic_fuel"] = weights["neutronic_fuel"]
        if blanket in _STATIC_BLANKET_VALUES:
            triggered["non_renewable_blanket"] = weights["non_renewable_blanket"]
    return triggered


@embedding(
    "operational_penalty_weight",
    inputs=["fuel", "blanket_config", "operation_mode"],
)
def _operational_penalty_weight(
    fuel: str, blanket_config: str, operation_mode: str,
    *, weights_yaml: dict,
) -> float:
    """Sum of severity weights of all triggered CF penalties."""
    sev = _load_upper_cf_weights(weights_yaml)
    triggered = _compute_triggered_cf_penalties(
        fuel, blanket_config, operation_mode, sev,
    )
    return sum(triggered.values())


@embedding(
    "upper_cf_score",
    inputs=["operational_penalty_weight"],
)
def _upper_cf_score(operational_penalty_weight: float) -> float:
    """Upper-CF axis score: floor 1.0, ceiling 5.0."""
    return max(1.0, 5.0 - operational_penalty_weight)
