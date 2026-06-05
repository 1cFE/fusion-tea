"""Per-archetype canonical ``spec`` field descriptions for the model-setup prompt.

This is a **hand-maintained fusion-tea constant** (parallel to
``canonical_accounts.py``). It addresses the failure mode surfaced by concepts
05 and 09 of the regen run: the LLM saw "fusion power = 958 MW" in the source
paper and transcribed it directly into ``spec["p_input"]`` because the prompt
template did not document what ``p_input`` actually means.

Two guarantees:

* The LLM is told, at the exact moment it is authoring the ``spec`` dict, what
  each canonical field means, what units it expects, what a typical value range
  looks like for the archetype it is modeling, and (most importantly) which
  common confusions to avoid (``p_fus`` vs ``p_input``, ``B`` vs ``b_center``,
  ``plasma_volume`` vs geometric volume, ``e_driver_mj`` not in kJ, etc.).
* The constant is concept-agnostic but archetype-aware: ``render_spec_keys_
  block(enum)`` filters to the fields the archetype's ``forward()`` actually
  consumes, so the prompt does not invite an analyst to set ``chamber_length``
  on a tokamak or ``elon`` on a mirror.

Companion AST guard (``F9``) lives in ``validators.py`` and rejects spec value
ratios that fall outside ``_SPEC_RATIO_BOUNDS`` — a backstop in case the prompt
guidance is ignored or future model versions drift.
"""

from __future__ import annotations

from dataclasses import dataclass

# Library-side source of truth for "what kwargs does each archetype's forward()
# actually accept": the per-archetype YAML (engineering defaults) + the
# cross-cutting optional-override keys CostModel reads via params.get(). The
# glossary derives from this rather than re-stating it, so the glossary cannot
# diverge from the strict-kwarg validator (1costingfe model.py:494).
from costingfe.defaults import load_engineering_defaults
from costingfe.types import CONCEPT_TO_FAMILY, ConfinementConcept

# Mirror of CostModel._OPTIONAL_OVERRIDE_KEYS (1costingfe model.py:1102). These
# are cross-cutting kwargs that CostModel.forward() reads via params.get() but
# that the per-archetype YAML may not declare. Kept in sync with the library;
# omitting a key here surfaces as a spurious "rejected by strict validator"
# at forward() time.
_OPTIONAL_OVERRIDE_KEYS = frozenset(
    {
        # Power-cycle / coupling knobs injected or derived by forward()
        "eta_th", "eta_pin", "eta_couple", "f_rad", "f_rad_fus",
        # 0D plasma model (TOKAMAK)
        "use_0d_model", "0d_mode", "fw_area",
        # Coil / magnet knobs not in every concept YAML
        "n_coils", "lev_coil_markup", "lev_coil_cryostat_cost",
        "stationary_lift_coil_fraction",
        # Pulsed conversion + driver knobs
        "pulsed_conversion", "e_stored_mj", "q_sci",
        "laser_driver_type",
    }
)

# Power-conversion / wall-plug efficiencies are NEVER surfaced as spec keys,
# regardless of what the YAML or cross-cutting key set advertises. They are
# library-managed via per-archetype YAML + CostingConstants so cross-concept
# LCOE comparisons stay apples-to-apples. To express a different efficiency,
# update the YAML / CostingConstants in 1costingfe — not the per-concept spec.
# See also commit 9142788 (first sweep, May 29 2026) which removed a subset of
# these from existing model_setup.py files but did not update the glossary;
# this set is the complete corpus-wide policy.
_FORBIDDEN_EFFICIENCY_KEYS = frozenset(
    {
        "eta_th",
        "eta_pin",
        "eta_pin1",
        "eta_pin2",
        "eta_couple",
        "eta_de",
        "eta_dec",
        "eta_p",
        # Per-method source efficiencies are CostingConstants, not spec keys.
        "eta_source_nbi",
        "eta_source_icrf",
        "eta_source_ecrh",
        "eta_source_lhcd",
    }
)


def _library_allowed_keys(enum: str) -> set[str]:
    """Return the kwarg set 1costingfe's strict validator accepts for ``enum``.

    The set is ``YAML_engineering_defaults ∪ _OPTIONAL_OVERRIDE_KEYS``, matching
    the allow-list computed at CostModel.forward() entry. By deriving from this
    same source the glossary cannot drift away from what the library actually
    accepts. ``_FORBIDDEN_EFFICIENCY_KEYS`` are removed before return.
    """
    concept = ConfinementConcept(enum.lower())
    family = CONCEPT_TO_FAMILY[concept]
    yaml_keys = set(load_engineering_defaults(f"{family.value}_{concept.value}"))
    return (yaml_keys | _OPTIONAL_OVERRIDE_KEYS) - _FORBIDDEN_EFFICIENCY_KEYS


@dataclass(frozen=True)
class SpecKey:
    """One canonical spec field surfaced to the model-setup prompt.

    ``field`` is the literal kwarg name accepted by ``forward()``
    (and listed in ``CostingInput.model_fields``).
    ``unit`` is the SI / SI-prefix unit the library expects.
    ``description`` is the one-line "what does this control" line the LLM reads.
    ``typical`` is an archetype-appropriate range; values outside are usually
    transcription errors.
    ``warning`` (optional) names the common analyst confusion this field invites.
    """

    field: str
    unit: str
    description: str
    typical: str
    warning: str | None = None


# ---------------------------------------------------------------------------
# Geometry — radial build inputs the library reads from spec.
# ---------------------------------------------------------------------------
_GEOMETRY: dict[str, SpecKey] = {
    "R0": SpecKey(
        "R0", "m",
        "Major radius (tokamak/stellarator) or chamber radius (mirror/IFE/sphere)",
        "3-20 (tokamak/stellarator); 0 for cylinder/sphere dispatch",
    ),
    "plasma_t": SpecKey(
        "plasma_t", "m",
        "Plasma minor radius `a` (tokamak/stellarator) or plasma column radius (mirror). "
        "If the source publishes only R0 and aspect ratio A, derive `plasma_t = R0 / A`. "
        "REQUIRED for TOKAMAK/STELLARATOR — drives r_coil = vessel_or in the bilinear "
        "coil cost; YAML default (1.1m tokamak / 1.8m stellarator) over-states most "
        "published commercial designs.",
        "0.05-2 (most MFE); larger for dipole-class spherical plasmas",
        "DIPOLE-class plasmas can be 10-25 m; tokamak/stellarator stay 0.05-3.",
    ),
    "elon": SpecKey(
        "elon", "—",
        "Elongation kappa (tokamak only)",
        "1.0-3.0; 1.0 = circular cross-section",
    ),
    "chamber_length": SpecKey(
        "chamber_length", "m",
        "Central cell length (mirror only)",
        "10-100",
    ),
    "blanket_t": SpecKey(
        "blanket_t", "m",
        "Blanket layer thickness",
        "0.3-1.0 (DT breeding); thinner for aneutronic / dipole shell blankets",
    ),
    "ht_shield_t": SpecKey(
        "ht_shield_t", "m",
        "High-temperature shield thickness",
        "0.1-0.3 (DT); near-zero for aneutronic",
    ),
    "structure_t": SpecKey(
        "structure_t", "m",
        "Primary structure thickness",
        "0.1-0.3",
    ),
    "vessel_t": SpecKey(
        "vessel_t", "m",
        "Vacuum vessel wall thickness",
        "0.05-0.30 (steel); ~0.008 for dipole's Inconel membrane",
    ),
}

# ---------------------------------------------------------------------------
# Coils — MFE only.
# ---------------------------------------------------------------------------
_COILS: dict[str, SpecKey] = {
    "b_center": SpecKey(
        "b_center", "T",
        "Magnetic field at the geometric center of the coil loop (axis)",
        "5-25 for SC HTS; 0.5-3 for resistive copper FRC/orbitron coils",
        "NOT the peak field on the conductor. Peak-on-conductor is ~3x higher "
        "for high-field SC; the kA*m formula NI = 2*B_center*R/mu_0 is "
        "derived for B_center, not B_max.",
    ),
    "r_bore": SpecKey(
        "r_bore", "m",
        "Effective coil winding-bore radius (NOT the conductor cross-section)",
        "0.3-5",
    ),
}

# ---------------------------------------------------------------------------
# Power balance — the most error-prone family. p_input is THE field that
# concepts 05/09 misused; lots of warning text here is intentional.
# ---------------------------------------------------------------------------
_POWER: dict[str, SpecKey] = {
    "p_input": SpecKey(
        "p_input", "MW",
        "Auxiliary heating wallplug power (NBI / ICRH / ECRH / LHCD delivered to plasma)",
        "5-15% of P_native for steady-state MFE; 1-10% for pulsed driver concepts",
        "DO NOT pass fusion power here. p_fus is computed by the library "
        "via the inverse power balance and is NOT settable through spec. "
        "If your source paper publishes p_fus = X MW, find the SEPARATE "
        "stated heating power (often labelled 'auxiliary heating', 'NBI', "
        "'ICRH', 'p_aux') and use THAT as p_input. Concepts 05 and 09 of "
        "the prior bulk run hit this exact bug: p_input was set to fusion "
        "power, library back-solved to a 5 GW plant masquerading as a "
        "stellarator. F9 sanity check (validators.py) now rejects "
        "p_input/P_native > 0.5 to prevent regressions.",
    ),
    "p_nbi": SpecKey(
        "p_nbi", "MW",
        "NBI fraction of p_input (must sum with p_icrf/p_ecrh/p_lhcd to p_input)",
        "0-100",
    ),
    "p_icrf": SpecKey(
        "p_icrf", "MW",
        "ICRH fraction of p_input",
        "0-100",
    ),
    "p_ecrh": SpecKey(
        "p_ecrh", "MW",
        "ECRH fraction of p_input",
        "0-100",
    ),
    "p_lhcd": SpecKey(
        "p_lhcd", "MW",
        "LHCD fraction of p_input",
        "0-100",
    ),
    "p_coils": SpecKey("p_coils", "MW", "Coil-system power (cooling, control)", "1-10"),
    "p_cool": SpecKey("p_cool", "MW", "Primary cooling pump power", "5-50"),
    "p_pump": SpecKey("p_pump", "MW", "Vacuum pumping power", "0.5-5"),
    "p_cryo": SpecKey("p_cryo", "MW", "Cryogenic wallplug", "0.5-5"),
    "p_house": SpecKey("p_house", "MW", "Housekeeping power", "2-10"),
    "p_trit": SpecKey(
        "p_trit", "MW",
        "Tritium processing power (zero for aneutronic / non-DT fuels)",
        "0-15 for DT; 0 for DD/DHE3/PB11",
    ),
    "f_dec": SpecKey(
        "f_dec", "—",
        "Fraction of fusion power routed through direct energy conversion",
        "0.0 (thermal-only) to 0.85 (DEC-dominant aneutronic)",
        "f_dec IS allowed in spec (architecture property, not efficiency). "
        "Distinct from eta_dec (efficiency, ENUM-owned, NOT allowed).",
    ),
}

# ---------------------------------------------------------------------------
# Plasma physics — radiation calc inputs.
# ---------------------------------------------------------------------------
_PLASMA: dict[str, SpecKey] = {
    "n_e": SpecKey(
        "n_e", "m^-3",
        "Volume-averaged electron density",
        "1e19 - 5e20 for MFE",
        "SI base unit (m^-3). NOT in units of 1e20 / m^3.",
    ),
    "T_e": SpecKey(
        "T_e", "keV",
        "Volume-averaged electron temperature",
        "5-30 keV",
        "keV, not eV.",
    ),
    "Z_eff": SpecKey("Z_eff", "—", "Effective charge", "1.2-2.0"),
    "plasma_volume": SpecKey(
        "plasma_volume", "m^3",
        "Plasma volume (used for radiation calc, not for cost-bearing geometry)",
        "100-1000 for tokamak/stellarator; 100-300 for mirror; "
        "dipole has a calibrated YAML default — see DIPOLE blocklist",
        "DIPOLE: do NOT pass plasma_volume in spec (1cFE/1costingfe#24 "
        "library bug — MFE radiation calc breaks at dipole-scale plasma "
        "volumes). Tokamak/stellarator/mirror: use the volume-averaged value.",
    ),
    "B": SpecKey(
        "B", "T",
        "Characteristic plasma-region magnetic field (for radiation calc)",
        "1-15",
        "Different from `b_center` (which is the COIL field at the loop "
        "center, used for kA*m costing). B is the plasma field for "
        "bremsstrahlung/synchrotron calculations.",
    ),
}

# ---------------------------------------------------------------------------
# Pulsed-specific. e_driver_mj is the canonical name for per-pulse driver
# energy; concepts that try `laser_pulse_energy_kJ` or `pulse_energy_J` get
# silently dropped by forward() and caught by F7.
# ---------------------------------------------------------------------------
_PULSED: dict[str, SpecKey] = {
    "f_rep": SpecKey(
        "f_rep", "Hz",
        "Repetition rate (pulsed driver cadence)",
        "0.1-10 Hz",
        "Hz, not 1/s. The library multiplies e_driver_mj by f_rep to get "
        "average driver power.",
    ),
    "e_driver_mj": SpecKey(
        "e_driver_mj", "MJ",
        "Per-pulse driver energy (laser/heavy-ion/EM-gun/Z-pinch)",
        "1-50 MJ",
        "Library expects MJ, not kJ. 30 kJ → e_driver_mj=0.030. NOT settable "
        "via laser_pulse_energy_kJ or pulse_energy_J — those names are not "
        "in CostingInput and would be silently dropped by forward().",
    ),
    "e_preheat_mj": SpecKey(
        "e_preheat_mj", "MJ",
        "MAGLIF preheat-laser per-pulse energy (0 if no preheat)",
        "0-0.1 MJ",
    ),
    "p_target": SpecKey(
        "p_target", "MW",
        "Target factory power (IFE consumable targets)",
        "0.5-5 MW",
    ),
    "q_eng": SpecKey(
        "q_eng", "—",
        "Pulsed-driver engineering gain target",
        "2-10",
    ),
}

# ---------------------------------------------------------------------------
# Misc shared.
# ---------------------------------------------------------------------------
_MISC: dict[str, SpecKey] = {
    "mn": SpecKey(
        "mn", "—",
        "Neutron energy multiplier",
        "1.0-1.3 (DT); 1.0 (aneutronic)",
    ),
    # eta_couple and eta_p deliberately omitted — power-conversion efficiencies
    # are never surfaced as spec keys. See _FORBIDDEN_EFFICIENCY_KEYS above.
    "f_sub": SpecKey("f_sub", "—", "Subsystem-power fraction of gross electric", "0.02-0.05"),
    "burn_fraction": SpecKey("burn_fraction", "—", "Single-pass fuel burn fraction", "0.02-0.10"),
    "fuel_recovery": SpecKey("fuel_recovery", "—", "Fraction of unburned fuel recovered", "0.95-1.0"),
}

# ---------------------------------------------------------------------------
# Per-archetype field membership. Mirrors the structure of
# canonical_accounts.py: the same archetype enum, the same family discriminators,
# selecting which fields apply where.
# ---------------------------------------------------------------------------
_STEADY_STATE_MFE = {"TOKAMAK", "STELLARATOR", "MIRROR", "DIPOLE", "STEADY_FRC"}
_PULSED_FUSION = {
    "LASER_IFE", "HEAVY_ION", "PLASMA_JET", "STAGED_ZPINCH",
    "PULSED_FRC", "MAGLIF", "MAG_TARGET", "THETA_PINCH", "DENSE_PLASMA_FOCUS",
    "ZPINCH",
}
_ELECTROSTATIC = {"ORBITRON", "POLYWELL"}


def _archetype_fields(enum: str) -> dict[str, SpecKey]:
    """Build the per-archetype canonical spec-key dictionary.

    Surfaces the intersection of:
      1. ``_library_allowed_keys(enum)`` — the strict-kwarg validator's
         allow-list (per-archetype YAML keys ∪ cross-cutting optional keys,
         minus ``_FORBIDDEN_EFFICIENCY_KEYS``).
      2. The hand-maintained ``_GEOMETRY ∪ _COILS ∪ _POWER ∪ _PLASMA ∪
         _PULSED ∪ _MISC`` registry — which keys have an analyst-facing
         description, unit, typical range, and warning.

    A key is surfaced to the model-setup prompt only when it appears in both:
    the library actually accepts it AND the project has documented it for the
    LLM. Anything missing from either is intentionally omitted.
    """
    # All glossary entries the project has authored, keyed by canonical name.
    documented: dict[str, SpecKey] = {
        **_GEOMETRY, **_COILS, **_POWER, **_PLASMA, **_PULSED, **_MISC,
    }
    allowed = _library_allowed_keys(enum)
    return {k: documented[k] for k in documented if k in allowed}


def get_canonical_spec_keys(enum: str) -> list[SpecKey]:
    """Return the canonical spec-key list for a ``ConfinementConcept`` enum name.

    Raises ``KeyError`` for an unknown enum (no silent fallback; same discipline
    as ``canonical_accounts.get_canonical_accounts``).
    """
    # canonical_accounts ships a hand-maintained list of allowed enum names;
    # we import it lazily to keep this file independently testable.
    from lib.canonical_accounts import ALL_CONFINEMENT_CONCEPT_ENUMS

    if enum not in ALL_CONFINEMENT_CONCEPT_ENUMS:
        raise KeyError(
            f"No canonical spec-key list for archetype enum {enum!r}. "
            f"Known enums: {', '.join(sorted(ALL_CONFINEMENT_CONCEPT_ENUMS))}"
        )
    return list(_archetype_fields(enum).values())


def render_spec_keys_block(spec_keys: list[SpecKey]) -> str:
    """Format a per-archetype canonical spec-key block for LLM consumption.

    Output mirrors ``canonical_accounts.render_account_block``: a markdown
    section the prompt template substitutes via {{canonical_spec_keys}}.
    Warnings (the "do NOT pass fusion power here" lines) are indented one
    level so the LLM can visually parse "field | rule | warning".
    """
    lines = [
        "| Field | Unit | Description | Typical range |",
        "|-------|------|-------------|---------------|",
    ]
    warnings_block: list[str] = []
    for sk in spec_keys:
        lines.append(
            f"| `{sk.field}` | {sk.unit} | {sk.description} | {sk.typical} |"
        )
        if sk.warning:
            warnings_block.append(f"- **`{sk.field}`**: {sk.warning}")

    if warnings_block:
        lines.append("")
        lines.append("**Common confusions to avoid:**")
        lines.append("")
        lines.extend(warnings_block)

    return "\n".join(lines)
