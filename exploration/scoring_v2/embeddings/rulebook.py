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
