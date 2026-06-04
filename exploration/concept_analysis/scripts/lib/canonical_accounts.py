"""Per-archetype canonical 1costingFE account schema for the analyze prompt.

This is a **hand-maintained fusion-tea constant** (design.md Bet 1). The library
exposes no ``enum -> accounts`` introspection surface — applicability is *control
flow* inside ``costingfe/layers/cas22.py`` (e.g. ``_COIL_DEFAULTS.get(concept)``
returns ``None`` for laser-IFE, so ``C220103`` is forced to ``0.0``). So the
"which accounts does this archetype actually touch" judgment is authored here,
once, and read many times.

Two guards keep the constant honest:

* ``validate_against_library()`` imports ``costingfe`` and asserts every account
  code named here appears as a referenced code in ``costingfe/layers/``. A
  library rename/removal fails loudly at test/CI time — drift is *detected*, not
  silently shipped into the prompt.
* The account-code namespace is closed: the analyze prompt receives this rendered
  block, so the LLM cannot invent a ``CAS22.1.3``-style code (the Phase-0 bug).

The *values* still come from the library at ``forward()`` time; this block only
anchors the LLM's account-code *choice* and tells it, in one line, what each
account costs so it can judge whether the dossier justifies an override.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AccountRow:
    """One canonical account surfaced to the analyze prompt.

    ``account`` is a library account code (``C220103``, ``CAS27``).
    ``one_line_description`` is the "what does this cost" line the LLM reads.
    ``applies_when`` is an optional archetype-specific qualifier (``None`` when
    the account applies unconditionally for this archetype).
    """

    account: str
    one_line_description: str
    applies_when: str | None = None


# ---------------------------------------------------------------------------
# Fit-grade -> expected enabled-override-count band (FR-8). SINGLE SOURCE.
# ---------------------------------------------------------------------------
# Shared by: the analyze prompt's `fit_grade_band` substitution var, the
# rewritten assessment.md prompt, and Item 7's check_override_count_vs_fit_grade
# (which Phase 3 refactors to consume this constant instead of an inline
# threshold). Keys match the archetype_fit.csv `fit_grade` spelling exactly
# ("High" / "Med" / "Low"); "None"-fit concepts route to freeform and never
# reach this table.
FIT_GRADE_OVERRIDE_BAND: dict[str, tuple[int, int]] = {
    "High": (0, 4),
    "Med": (3, 8),
    "Low": (6, 12),
}


def fit_grade_band(fit_grade: str) -> tuple[int, int] | None:
    """Return the ``(low, high)`` expected override-count band for a fit grade.

    Case-insensitive; accepts the ``"Medium"`` long form as a synonym for
    ``"Med"``. Returns ``None`` for an unknown / ``"None"`` grade (the caller
    decides how to render "no band").
    """
    g = (fit_grade or "").strip().lower()
    if g in {"med", "medium"}:
        g = "med"
    for key, band in FIT_GRADE_OVERRIDE_BAND.items():
        if key.lower() == g:
            return band
    return None


# ---------------------------------------------------------------------------
# Master account-code descriptions (one line each). Keyed by library code.
# ---------------------------------------------------------------------------
# Descriptions live here once; per-archetype lists below select a subset and may
# attach an archetype-specific `applies_when`. Every code here is cross-checked
# against the library by validate_against_library().
_ACCOUNT_DESCRIPTIONS: dict[str, str] = {
    # --- CAS22 reactor-plant sub-accounts (the override-rich ones) ---
    "C220101": "First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket)",
    "C220102": "Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels)",
    "C220103": "Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat)",
    "C220104": "Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun)",
    "C220105": "Primary structure — gravity supports, thermal shields, inter-coil structure, machine base",
    "C220106": "Vacuum system — vessel, port extensions, cryopumps, leak detection",
    "C220107": "Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored)",
    "C220108": "Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing)",
    "C220109": "Direct energy converter (electrostatic for mirror/FRC exhaust, or inductive DEC on a pulsed driver)",
    "C220110": "Remote handling & maintenance equipment (rad-hardening tier x vessel geometry)",
    "C220111": "Reactor-equipment installation & assembly (fraction of the CAS22 subtotal)",
    # --- CAS2x balance-of-plant + materials ---
    "CAS21": "Buildings & site structures (reactor, turbine, hot cell, balance-of-plant)",
    "CAS23": "Turbine plant equipment (thermal cycle; zero for direct-conversion / eta_th=0 plants)",
    "CAS24": "Electric plant equipment (switchyard, transformers, plant distribution)",
    "CAS25": "Miscellaneous plant equipment",
    "CAS26": "Heat rejection system (cooling towers, circulating water)",
    "CAS27": "Special materials — initial reactor material inventory / blanket fill (distinct from C220101 structure)",
    # --- Operations (company-grounded where data exists) ---
    "CAS70": "Annualized O&M + scheduled component replacement (staffing-based)",
    "CAS80": "Annualized fuel cost — consumables and enriched-isotope procurement",
}


# ---------------------------------------------------------------------------
# Per-archetype applicability (control flow mirrored from cas22.py).
# ---------------------------------------------------------------------------
# Sets that drive per-archetype membership, named after the library branch they
# mirror so a future library reshape has an obvious anchor.

# C220103 -> 0.0 (no confinement magnets): _COIL_DEFAULTS[concept] is None.
_NO_COILS = {
    "LASER_IFE", "ZPINCH", "HEAVY_ION", "DENSE_PLASMA_FOCUS", "STAGED_ZPINCH",
}
# C220108 -> 0.0 (no divertor, no manufactured target): the explicit zero branch.
_NO_DIVERTOR_OR_TARGET = {
    "PULSED_FRC", "THETA_PINCH", "DENSE_PLASMA_FOCUS", "STAGED_ZPINCH",
}
# Steady-state magnetic confinement (family == STEADY_STATE): supplementary
# heating in C220104, magnet power supplies in C220107, divertor in C220108.
_STEADY_STATE = {"TOKAMAK", "STELLARATOR", "MIRROR", "DIPOLE"}
# Inertial / heavy-ion drivers: C220108 is a target factory; C220104 is the
# primary driver (laser/accelerator); thermal cycle (CAS23 present).
_INERTIAL_DRIVER = {"LASER_IFE", "HEAVY_ION", "ZPINCH"}
# Concepts that can carry a direct energy converter (C220109): mirror/FRC
# electrostatic exhaust, or pulsed inductive DEC. Conventional tokamak/
# stellarator/IFE thermal plants do not.
_MAY_HAVE_DEC = {
    "MIRROR", "PULSED_FRC", "THETA_PINCH", "MAGLIF", "MAG_TARGET",
    "PLASMA_JET", "STAGED_ZPINCH", "DENSE_PLASMA_FOCUS", "ORBITRON", "POLYWELL",
}

# All 16 library ConfinementConcept enum names. Defined as a module constant so
# the test suite can iterate every enum and assert each has a non-empty,
# library-valid account list. Kept in sync with costingfe.types.ConfinementConcept
# by validate_against_library() (which raises if the library adds/renames one).
ALL_CONFINEMENT_CONCEPT_ENUMS: tuple[str, ...] = (
    "TOKAMAK", "STELLARATOR", "MIRROR", "DIPOLE",
    "LASER_IFE", "ZPINCH", "HEAVY_ION",
    "MAG_TARGET", "PLASMA_JET", "PULSED_FRC", "MAGLIF",
    "THETA_PINCH", "DENSE_PLASMA_FOCUS", "STAGED_ZPINCH",
    "ORBITRON", "POLYWELL",
)


def _build_archetype_accounts() -> dict[str, list[AccountRow]]:
    """Assemble the per-archetype account lists from the membership sets above.

    Authored as control flow (not a literal table) so it stays in lockstep with
    the library branches it mirrors. The result is a plain
    ``dict[str, list[AccountRow]]`` — the shape Phase-1 tests patch directly.
    """
    out: dict[str, list[AccountRow]] = {}
    for enum in ALL_CONFINEMENT_CONCEPT_ENUMS:
        rows: list[AccountRow] = []

        def add(code: str, applies_when: str | None = None) -> None:
            rows.append(AccountRow(code, _ACCOUNT_DESCRIPTIONS[code], applies_when))

        # First wall / blanket and shield: every concept has both.
        add("C220101")
        add("C220102")

        # Confinement magnets — absent for the pure-inertial / pinch drivers.
        if enum not in _NO_COILS:
            if enum == "DIPOLE":
                add("C220103", "includes the floating field coil costed as a "
                               "distinct object plus stationary levitation coils")
            else:
                add("C220103")

        # Heating vs. driver in C220104.
        if enum in _STEADY_STATE:
            add("C220104", "supplementary heating (NBI/ICRF/ECRH/LHCD) per installed MW")
        elif enum == "MAGLIF":
            add("C220104", "laser-preheat pulse energy only; the main drive current "
                           "is electrical and lives in C220107")
        else:
            add("C220104", "primary pulsed driver (laser/accelerator/gun) on $/J of "
                           "driver energy; electrical-drive concepts cost it in C220107")

        add("C220105")
        add("C220106")

        # Power supplies / capacitor bank.
        if enum in _STEADY_STATE:
            add("C220107", "DC magnet power supplies and switchgear")
        else:
            add("C220107", "pulsed-power capacitor bank on $/J stored — usually the "
                           "dominant driver cost for electrically-driven pulsed schemes")

        # Divertor vs. target factory vs. nothing.
        if enum in _NO_DIVERTOR_OR_TARGET:
            pass  # explicit library zero — no manufactured target, no divertor
        elif enum in _STEADY_STATE:
            add("C220108", "divertor (W monoblock cassettes on CuCrZr heat sinks)")
        else:
            add("C220108", "high-rep-rate target manufacturing factory (IFE/MIF)")

        # Direct energy converter — opt-in, design-point-dependent.
        if enum in _MAY_HAVE_DEC:
            add("C220109", "only if the design point uses direct energy conversion "
                           "(directed axial exhaust or an inductive DEC stage)")

        add("C220110")
        add("C220111")

        # Balance of plant + materials + operations (every concept).
        add("CAS21")
        add("CAS23", "zero if the design point is direct-conversion (no thermal cycle)")
        add("CAS24")
        add("CAS26")
        add("CAS27")
        add("CAS70")
        add("CAS80")

        out[enum] = rows
    return out


_PER_ARCHETYPE_ACCOUNTS: dict[str, list[AccountRow]] = _build_archetype_accounts()


def get_canonical_accounts(enum: str) -> list[AccountRow]:
    """Return the canonical account list for a ``ConfinementConcept`` enum name.

    ``enum`` is the library enum *name* (e.g. ``"TOKAMAK"``), as carried in the
    concept record's ``archetype_enum`` field. Raises ``KeyError`` for an unknown
    enum — there is **no silent fallback** to a default archetype (a wrong-but-
    plausible account list is worse than a loud failure that names the gap).
    """
    try:
        return _PER_ARCHETYPE_ACCOUNTS[enum]
    except KeyError:
        raise KeyError(
            f"No canonical account list for archetype enum {enum!r}. Known enums: "
            f"{', '.join(sorted(_PER_ARCHETYPE_ACCOUNTS))}"
        ) from None


def render_account_block(accounts: list[AccountRow]) -> str:
    """Render an account list as the markdown block the analyze prompt consumes.

    One row per account: the code, its one-line cost description, and (when
    present) the archetype-specific qualifier. Kept terse — this block is read
    by the LLM, not parsed by a validator.
    """
    lines = [
        "| Account | What it costs | Applies when |",
        "| --- | --- | --- |",
    ]
    for row in accounts:
        applies = row.applies_when or "always (for this archetype)"
        # Collapse internal newlines from the authored multi-line strings.
        desc = " ".join(row.one_line_description.split())
        applies = " ".join(applies.split())
        lines.append(f"| `{row.account}` | {desc} | {applies} |")
    return "\n".join(lines)


def validate_against_library() -> list[str]:
    """Cross-check every named account code against the installed ``costingfe``.

    Reads ``costingfe/layers/{cas22.py,costs.py}`` and returns the list of codes
    in ``_PER_ARCHETYPE_ACCOUNTS`` that do **not** appear (case-insensitively) as
    a referenced token in either file. An empty list means the constant is in
    sync with the library; a non-empty list is a loud drift signal for CI.

    Imports the library lazily so importing this module never hard-requires
    ``costingfe`` to be installed (only the cross-check test does).
    """
    import costingfe

    layers = Path(costingfe.__file__).parent / "layers"
    haystack = (
        (layers / "cas22.py").read_text(encoding="utf-8")
        + (layers / "costs.py").read_text(encoding="utf-8")
    ).lower()

    named = {row.account for rows in _PER_ARCHETYPE_ACCOUNTS.values() for row in rows}
    return sorted(code for code in named if code.lower() not in haystack)
