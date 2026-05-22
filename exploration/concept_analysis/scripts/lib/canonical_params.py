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
# Canonical (η_th, η_de) by energy capture type
# ---------------------------------------------------------------------------
# Each entry is a (eta_th, eta_de) tuple matched to costingfe's actual parameter
# semantics: eta_th is thermal-cycle-only (drives p_the = eta_th * p_th), eta_de
# is DEC-only (drives p_dee = f_dec * eta_de * p_transport). Costingfe adds the
# two channels: p_et = p_the + p_dee. Conflating them under a single canonical
# (the pre-2026-05 shape) caused the eta_th double-count bug fixed by issue #30.

_CANONICAL_EFFICIENCIES: dict[str, tuple[float, float]] = {
    # Thermal cycles: cycle-only, no DEC channel.
    "thermal (steam)":            (0.35, 0.0),
    "thermal (sco2)":             (0.48, 0.0),
    "thermal (unspecified)":      (0.35, 0.0),
    # Hybrid: both a thermal blanket cycle AND a DEC channel on end-loss alphas.
    "hybrid (thermal + direct)":  (0.35, 0.54),
    # Direct: no thermal cycle; DEC carries the entire useful-electric channel.
    "direct (inductive)":         (0.0,  0.85),
    "direct (charged particle)":  (0.0,  0.70),
    # Unspecified / placeholder: default to a steam-Rankine thermal cycle.
    "tbd":                        (0.35, 0.0),
    "unknown":                    (0.35, 0.0),
}


def _lookup_efficiencies(energy_capture: str) -> tuple[float, float]:
    """Look up the (eta_th, eta_de) tuple for an Energy Capture key.

    Case- and whitespace-insensitive. Falls back to a parenthetical-stripped
    form if the literal key isn't found (e.g. "tbd (whatever)" → "tbd").
    """
    key = energy_capture.strip().lower()
    if key in _CANONICAL_EFFICIENCIES:
        return _CANONICAL_EFFICIENCIES[key]
    base = re.sub(r"\s*\([^)]*\)\s*", "", key).strip()
    if base in _CANONICAL_EFFICIENCIES:
        return _CANONICAL_EFFICIENCIES[base]
    raise ValueError(
        f"Unknown energy capture type: {energy_capture!r}. "
        f"Valid keys: {sorted(_CANONICAL_EFFICIENCIES.keys())}"
    )


def canonical_eta_th(energy_capture: str) -> float:
    """Return the canonical thermal-cycle efficiency for an energy capture type.

    Returns the eta_th component of the (eta_th, eta_de) tuple from
    ``_CANONICAL_EFFICIENCIES``. This is the *cycle* efficiency that costingfe
    multiplies by the thermal-blanket heat load (``p_the = eta_th * p_th``) —
    NOT an overall plant efficiency. Direct-conversion concepts return 0.0
    because they have no thermal cycle; their useful-electric channel comes
    from ``canonical_eta_de``.

    Argument matches the ``Energy Capture`` column from ``table.csv``
    (case/whitespace insensitive). See ``scoring_framework.md`` §"Energy
    capture efficiencies (η_th, η_de)" for the full policy, including the
    justified-deviation rule.

    Raises ``ValueError`` if the energy capture type is not recognized.
    """
    return _lookup_efficiencies(energy_capture)[0]


def canonical_eta_de(energy_capture: str) -> float:
    """Return the canonical Direct Energy Conversion (DEC) efficiency.

    Returns the eta_de component of the (eta_th, eta_de) tuple from
    ``_CANONICAL_EFFICIENCIES``. This is the DEC channel efficiency that
    costingfe multiplies by the charged-particle end-loss transport
    (``p_dee = f_dec * eta_de * p_transport``). Pure-thermal concepts return
    0.0 because they have no DEC channel.

    Argument matches the ``Energy Capture`` column from ``table.csv``
    (case/whitespace insensitive). See ``scoring_framework.md`` §"Energy
    capture efficiencies (η_th, η_de)" for the full policy.

    Raises ``ValueError`` if the energy capture type is not recognized.
    """
    return _lookup_efficiencies(energy_capture)[1]


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


# ---------------------------------------------------------------------------
# Canonical plant lifetime (lifetime_yr)
# ---------------------------------------------------------------------------

_CANONICAL_LIFETIME_YR = 30.0


def canonical_lifetime_yr(fuel: str = "D-T") -> float:
    """Return the canonical plant lifetime in years.

    Lookup rules (see ``prompt_templates/config/scoring_framework.md``
    §"Plant lifetime"):

    - All concepts: **30 yr** (standard commercial-plant finance horizon,
      consistent with the WACC-based LCOE convention).

    The ``fuel`` argument is accepted for signature symmetry with the other
    canonical_* helpers; it is currently unused.

    A model may use a non-canonical ``lifetime_yr``, but **only** when the
    concept's own published design literature commits to a specific plant
    or major-component (magnet, vacuum vessel) design life with a stated
    basis. Author-judged values are not sufficient.
    """
    del fuel  # accepted for symmetry; not yet used
    return _CANONICAL_LIFETIME_YR
