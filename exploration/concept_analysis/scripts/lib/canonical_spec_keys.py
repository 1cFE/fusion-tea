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
        "Plasma minor radius (tokamak/stellarator) or plasma column radius (mirror)",
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
    "eta_couple": SpecKey(
        "eta_couple", "—",
        "Heating-method delivered-to-plasma coupling factor",
        "0.4-1.0",
        "eta_pin = eta_source_<method> x eta_couple is derived. "
        "eta_pin itself is NOT settable for heated MFE concepts.",
    ),
    "eta_p": SpecKey("eta_p", "—", "Pumping efficiency", "0.4-0.7"),
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
    """Build the per-archetype canonical spec-key dictionary."""
    fields: dict[str, SpecKey] = {}
    # Geometry — most apply to all
    for k in ("R0", "plasma_t", "blanket_t", "ht_shield_t", "structure_t", "vessel_t"):
        fields[k] = _GEOMETRY[k]
    if enum in {"TOKAMAK"}:
        fields["elon"] = _GEOMETRY["elon"]
    if enum in {"MIRROR", "STEADY_FRC"} or enum in _PULSED_FUSION:
        fields["chamber_length"] = _GEOMETRY["chamber_length"]

    # Coils — MFE + electrostatic
    if enum in _STEADY_STATE_MFE or enum in _ELECTROSTATIC:
        fields.update(_COILS)

    # Power balance
    fields["p_input"] = _POWER["p_input"]
    if enum in _STEADY_STATE_MFE:
        for k in ("p_nbi", "p_icrf", "p_ecrh", "p_lhcd"):
            fields[k] = _POWER[k]
    for k in ("p_coils", "p_cool", "p_pump", "p_cryo", "p_house", "p_trit"):
        fields[k] = _POWER[k]
    if enum in {"MIRROR", "PULSED_FRC", "THETA_PINCH", "MAG_TARGET", "PLASMA_JET",
                "STAGED_ZPINCH", "DENSE_PLASMA_FOCUS", "MAGLIF",
                "ORBITRON", "POLYWELL"}:
        fields["f_dec"] = _POWER["f_dec"]

    # Plasma physics
    fields.update(_PLASMA)

    # Pulsed-only
    if enum in _PULSED_FUSION:
        fields.update(_PULSED)

    # Misc
    fields.update(_MISC)

    return fields


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
