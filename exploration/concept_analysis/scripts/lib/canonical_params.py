"""Canonical LCOE-modeling parameter lookups.

These are project-policy values referenced by ``model_setup.py`` files and by
the ``standardize_*.py`` scripts to enforce cross-concept consistency on
LCOE-driving inputs. See ``prompt_templates/config/scoring_framework.md``
§"Standard LCOE Modeling Parameters" for the full policy, including the
justified-deviation rule.

These values are **not** scoring inputs — they are inputs to the costingfe
forward model. They live here (not in ``lib/scoring.py``) so the modeling
canon stays separate from the C1–C8 scoring rubric.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Canonical η_th by energy capture type
# ---------------------------------------------------------------------------

_CANONICAL_ETA_TH: dict[str, float] = {
    # Thermal cycles
    "thermal (steam) saturated": 0.32,
    "thermal (steam) superheated": 0.35,
    "thermal (steam) supercritical": 0.42,
    "thermal (steam)": 0.35,            # default to superheated
    "thermal (sco2)": 0.48,
    "thermal (helium brayton)": 0.45,
    "thermal (combined cycle)": 0.50,
    "thermal (unspecified)": 0.35,
    # Direct / hybrid
    "hybrid (thermal + direct)": 0.55,
    "direct (inductive)": 0.85,
    "direct (charged particle)": 0.70,
    # Pulsed / unusual
    "pulsed power implosion": 0.30,
    "projectile impact": 0.30,
    "tbd": 0.35,
    "unknown": 0.35,
}


def canonical_eta_th(energy_capture: str) -> float:
    """Return the canonical thermal-to-electric efficiency for an energy capture type.

    The argument should match the ``Energy Capture`` column from ``table.csv``
    (case- and whitespace-insensitive). Returns the canonical η_th defined in
    ``prompt_templates/config/scoring_framework.md``.

    A model file may use a non-canonical value, but it must document the
    deviation explicitly (see scoring_framework.md "Justified deviations").

    Raises ``ValueError`` if the energy capture type is not recognized.
    """
    key = energy_capture.strip().lower()
    if key in _CANONICAL_ETA_TH:
        return _CANONICAL_ETA_TH[key]
    # Tolerate minor variations: strip parenthetical content for fallback
    base = re.sub(r"\s*\([^)]*\)\s*", "", key).strip()
    if base in _CANONICAL_ETA_TH:
        return _CANONICAL_ETA_TH[base]
    raise ValueError(
        f"Unknown energy capture type: {energy_capture!r}. "
        f"Valid keys: {sorted(_CANONICAL_ETA_TH.keys())}"
    )


# ---------------------------------------------------------------------------
# Canonical availability by operating-mode category
# ---------------------------------------------------------------------------

_CANONICAL_AVAILABILITY_MCF_STEADY = 0.85
_CANONICAL_AVAILABILITY_PULSED = 0.75


def canonical_availability(
    confinement_family: str,
    operation_mode: str,
    fuel: str = "D-T",
) -> float:
    """Return the canonical plant availability for a concept's operating mode.

    Arguments are taken from ``table.csv`` columns:
    - ``confinement_family``: ``MFE``, ``IFE``, ``MIF``, or ``Non-Standard``
    - ``operation_mode``: ``Steady-state``, ``Quasi-steady``, ``Pulsed``, etc.
    - ``fuel``: ``D-T``, ``D-D``, ``D-He3``, ``p-B11``

    Lookup rules (see ``prompt_templates/config/scoring_framework.md`` for the
    full canonical table and the justified-deviation policy):

    - MCF + (steady-state or quasi-steady): **0.85**
    - Anything pulsed (MCF, IFE, MIF): **0.75**
    - Non-D-T fuels currently get the steady-state default 0.85 (no fuel-specific
      operations data in literature)

    A model file may use a non-canonical value, but **only** if it cites an
    externally-published availability target with a stated basis. See the
    "Justified deviations" rule in scoring_framework.md.

    Raises ``ValueError`` if the operating mode cannot be classified.
    """
    family = confinement_family.strip().upper()
    mode = operation_mode.strip().lower()

    is_pulsed = "pulsed" in mode
    is_steady = "steady" in mode or "quasi" in mode or "continuous" in mode

    if is_pulsed and not is_steady:
        return _CANONICAL_AVAILABILITY_PULSED

    if is_steady:
        return _CANONICAL_AVAILABILITY_MCF_STEADY

    # Family-based fallback when mode string is ambiguous (e.g., CSV parsing
    # artifacts like "Integrated blanket/shield" for 07-maglif and 22-projectile)
    if family in ("IFE", "MIF"):
        return _CANONICAL_AVAILABILITY_PULSED
    if family == "MFE":
        return _CANONICAL_AVAILABILITY_MCF_STEADY

    raise ValueError(
        f"Cannot classify operating mode for canonical availability: "
        f"family={confinement_family!r}, mode={operation_mode!r}, fuel={fuel!r}"
    )


# ---------------------------------------------------------------------------
# Canonical blanket energy multiplication (mn)
# ---------------------------------------------------------------------------

_CANONICAL_MN_DT = 1.1


def canonical_mn(fuel: str = "D-T") -> float:
    """Return the canonical blanket energy multiplication factor for a fuel.

    ``mn`` captures neutron energy multiplication in the blanket (Be / Pb
    neutron multipliers, exothermic Li capture, etc.). It is not a free
    policy lever — it is a function of blanket technology. The canonical
    here is the costingfe framework default for a generic D-T Li-bearing
    blanket without a dedicated neutron multiplier.

    Lookup rules (see ``prompt_templates/config/scoring_framework.md``
    §"Blanket energy multiplication"):

    - D-T: **1.1** (framework default)
    - Non-D-T: not standardized (raises ValueError)

    A model may use a non-canonical ``mn``, but **only** when it cites a
    named blanket technology with a published multiplication factor
    (e.g., HCPB+Be, FLiBe with specified TBR) or a physics-coupling
    argument that requires a non-default value (e.g., to avoid
    double-counting Li boost already embedded in ``eta_th``).
    """
    f = fuel.strip().upper().replace(" ", "")
    if f in ("D-T", "DT"):
        return _CANONICAL_MN_DT
    raise ValueError(
        f"No canonical mn defined for fuel={fuel!r}. Only D-T is standardized."
    )
