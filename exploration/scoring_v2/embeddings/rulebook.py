"""Embedding rulebook.

Every embedding is a small pure function over declared feature inputs that
returns a 1-5 scalar. Registration is explicit via @embedding(name, inputs).

The module-level REGISTRY is what score.py iterates. No file I/O, no LLM calls,
no global state. Static check: this file imports neither yaml, csv, nor any
LLM client.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

EmbeddingFn = Callable[..., float | int | None]


@dataclass(frozen=True)
class Embedding:
    name: str
    inputs: tuple[str, ...]
    fn: EmbeddingFn


REGISTRY: dict[str, Embedding] = {}


def embedding(name: str, inputs: list[str]) -> Callable[[EmbeddingFn], EmbeddingFn]:
    def _wrap(fn: EmbeddingFn) -> EmbeddingFn:
        if name in REGISTRY:
            raise ValueError(f"embedding {name!r} already registered")
        REGISTRY[name] = Embedding(name=name, inputs=tuple(inputs), fn=fn)
        return fn
    return _wrap


# -----------------------------------------------------------------------------
# Plant-level modularity group (slice 1 content).
# Each embedding maps a few taxonomy features to a 1-5 scalar.
# See design.md "The Plant-Level Modularity Embedding Group" for rationale.
# -----------------------------------------------------------------------------


@embedding(
    "min_viable_device_scale",
    inputs=["confinement_family", "mfe_topology", "ife_driver", "mif_method", "tokamak_shape"],
)
def _min_viable_device_scale(
    confinement_family: str,
    mfe_topology: str,
    ife_driver: str,
    mif_method: str,
    tokamak_shape: str,
) -> float:
    if confinement_family == "MIF":
        return 5
    if confinement_family == "IFE":
        if ife_driver and ("DPSSL" in ife_driver or "Heavy ion" in ife_driver):
            return 4
        return 3
    if confinement_family == "MFE":
        if mfe_topology == "Tokamak":
            if tokamak_shape in ("Compact", "Spherical"):
                return 3
            return 2
        if mfe_topology == "Stellarator":
            return 2
        if mfe_topology == "Open/Linear":
            return 4
        if mfe_topology == "Dipole":
            return 3
        if mfe_topology == "Compact Toroid":
            return 4
        return 3
    return 3  # Non-Standard fallback


@embedding(
    "hardware_topology_complexity",
    inputs=["mfe_topology", "tokamak_shape", "magnet_type", "stellarator_type", "ife_driver"],
)
def _hardware_topology_complexity(
    mfe_topology: str,
    tokamak_shape: str,
    magnet_type: str,
    stellarator_type: str,
    ife_driver: str,
) -> float:
    if magnet_type and "Pulsed EM" in magnet_type:
        return 5
    if mfe_topology == "Open/Linear":
        return 5
    if mfe_topology == "Stellarator":
        return 1
    if mfe_topology == "Tokamak" and magnet_type and "HTS" in magnet_type and tokamak_shape in ("Compact", "Spherical"):
        return 4
    if ife_driver and "DPSSL" in ife_driver:
        return 4
    if mfe_topology == "Tokamak" and magnet_type and ("LTS" in magnet_type):
        return 2
    return 3


@embedding(
    "unit_multiplicity",
    inputs=["confinement_family", "operation_mode", "ife_driver", "mif_method", "driver_technology"],
)
def _unit_multiplicity(
    confinement_family: str,
    operation_mode: str,
    ife_driver: str,
    mif_method: str,
    driver_technology: str,
) -> float:
    if ife_driver and "DPSSL" in ife_driver:
        return 5
    if operation_mode == "Pulsed" and confinement_family == "MIF":
        return 4
    if confinement_family == "IFE":
        return 3
    if mif_method and "Z-pinch" in mif_method:
        return 3
    if operation_mode == "Pulsed":
        return 2
    if operation_mode in ("Steady-state", "Quasi-steady"):
        return 1
    return 2


@embedding(
    "subsystem_stack_burden",
    inputs=["fuel", "tritium_breeding", "neutron_management"],
)
def _subsystem_stack_burden(
    fuel: str,
    tritium_breeding: str,
    neutron_management: str,
) -> float:
    if fuel in ("p-B11", "D-He3"):
        return 5
    if fuel == "D-D":
        return 4
    if fuel == "D-T":
        if neutron_management and "Heavy" in neutron_management:
            return 2
        if tritium_breeding and "FLiBe" in tritium_breeding:
            return 3
        if neutron_management and "Integrated" in neutron_management:
            return 3
        return 2
    return 3


# -----------------------------------------------------------------------------
# Component-level modularity group (slice 2).
# Seven subsystem ratings (1-5) transcribed from the xlsx "Driver Lookups" tab,
# plus an aggregate that blends them by per-concept capex shares (w_*).
# See design.md "The 7 rating functions" for band rationale.
# -----------------------------------------------------------------------------


@embedding(
    "vessel_rating",
    inputs=["confinement_family", "mfe_topology", "tokamak_shape"],
)
def _vessel_rating(
    confinement_family: str,
    mfe_topology: str,
    tokamak_shape: str,
) -> int:
    if confinement_family == "MIF":
        return 5
    if mfe_topology == "Tokamak" and tokamak_shape in ("Compact", "Spherical"):
        return 4
    if mfe_topology == "Tokamak":
        return 2
    if mfe_topology == "Stellarator":
        return 2
    if confinement_family == "IFE":
        return 3
    return 3


@embedding(
    "coils_rating",
    inputs=["magnet_type", "mfe_topology", "ife_driver",
            "tokamak_shape", "stellarator_type"],
)
def _coils_rating(
    magnet_type: str,
    mfe_topology: str,
    ife_driver: str,
    tokamak_shape: str,
    stellarator_type: str,
) -> int:
    if "DPSSL" in (ife_driver or ""):
        return 5
    if "Pulsed EM" in (magnet_type or ""):
        return 5
    if "Flashlamp" in (ife_driver or "") or "KrF" in (ife_driver or ""):
        return 2
    if mfe_topology == "Tokamak" and "HTS" in (magnet_type or "") \
            and tokamak_shape in ("Compact", "Spherical"):
        return 4
    if mfe_topology == "Stellarator" and "HTS" in (magnet_type or ""):
        return 3
    if mfe_topology == "Stellarator":
        return 2
    if mfe_topology == "Tokamak" and "LTS" in (magnet_type or ""):
        return 2
    return 3


@embedding(
    "blanket_rating",
    inputs=["fuel", "tritium_breeding", "mfe_topology"],
)
def _blanket_rating(
    fuel: str,
    tritium_breeding: str,
    mfe_topology: str,
) -> int:
    if fuel in ("p-B11", "D-He3", "D-D"):
        return 5
    if "FLiBe" in (tritium_breeding or ""):
        return 5
    tb_lower = (tritium_breeding or "").lower()
    if "HCPB" in (tritium_breeding or "") or "pebble" in tb_lower:
        return 4
    if mfe_topology == "Stellarator":
        return 2
    if "Heavy" in (tritium_breeding or ""):
        return 2
    return 3


@embedding(
    "bop_rating",
    inputs=["energy_capture", "operation_mode"],
)
def _bop_rating(
    energy_capture: str,
    operation_mode: str,
) -> int:
    ec = energy_capture or ""
    if "Direct" in ec:
        return 4
    if "sCO2" in ec:
        return 5
    if "Thermal" in ec and operation_mode in ("Steady-state", "Quasi-steady"):
        return 4
    if "Thermal" in ec and operation_mode == "Pulsed":
        return 3
    return 3


@embedding(
    "fuel_cycle_rating",
    inputs=["fuel", "tokamak_shape", "mfe_topology"],
)
def _fuel_cycle_rating(
    fuel: str,
    tokamak_shape: str,
    mfe_topology: str,
) -> int:
    if fuel in ("p-B11", "D-He3", "D-D"):
        return 5
    if fuel == "D-T" and mfe_topology == "Tokamak" \
            and tokamak_shape in ("Compact", "Spherical"):
        return 3
    if fuel == "D-T" and mfe_topology == "Tokamak":
        return 2
    if fuel == "D-T" and mfe_topology == "Stellarator":
        return 3
    if fuel == "D-T":
        return 3
    return 3


@embedding(
    "aux_rating",
    inputs=["magnet_type", "confinement_family", "tokamak_shape"],
)
def _aux_rating(
    magnet_type: str,
    confinement_family: str,
    tokamak_shape: str,
) -> int:
    mt = magnet_type or ""
    if confinement_family == "MIF" and "HTS" in mt:
        return 5
    if "HTS" in mt and tokamak_shape in ("Compact", "Spherical"):
        return 3
    if "HTS" in mt:
        return 4
    if "LTS" in mt:
        return 2
    return 3


@embedding(
    "civil_rating",
    inputs=["fuel", "neutron_management", "mfe_topology", "tokamak_shape"],
)
def _civil_rating(
    fuel: str,
    neutron_management: str,
    mfe_topology: str,
    tokamak_shape: str,
) -> int:
    if fuel in ("p-B11", "D-He3"):
        return 5
    if "Heavy" in (neutron_management or ""):
        return 2
    if mfe_topology == "Stellarator":
        return 2
    if mfe_topology == "Tokamak" and tokamak_shape in ("Compact", "Spherical"):
        return 4
    if mfe_topology == "Tokamak":
        return 2
    return 3


@embedding(
    "component_modularity_aggregate",
    inputs=["vessel_rating", "coils_rating", "blanket_rating",
            "bop_rating", "fuel_cycle_rating", "aux_rating", "civil_rating",
            "w_vessel", "w_coils", "w_blanket", "w_bop",
            "w_fuel_cycle", "w_aux", "w_civil"],
)
def _component_modularity_aggregate(
    vessel_rating: int,
    coils_rating: int,
    blanket_rating: int,
    bop_rating: int,
    fuel_cycle_rating: int,
    aux_rating: int,
    civil_rating: int,
    w_vessel: float,
    w_coils: float,
    w_blanket: float,
    w_bop: float,
    w_fuel_cycle: float,
    w_aux: float,
    w_civil: float,
) -> float | None:
    ratings = (vessel_rating, coils_rating, blanket_rating, bop_rating,
               fuel_cycle_rating, aux_rating, civil_rating)
    weights = (w_vessel, w_coils, w_blanket, w_bop,
               w_fuel_cycle, w_aux, w_civil)
    if any(w is None for w in weights):
        return None
    return sum(r * w for r, w in zip(ratings, weights))
