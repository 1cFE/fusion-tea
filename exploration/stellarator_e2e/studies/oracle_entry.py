"""Package-owned oracle seam for the stellarator package.

`verify.py` is generic: it knows a manifest names a module and a callable, and
nothing else. Everything that is *this package's* knowledge lives here —

* which qualified entry key becomes which oracle input (`ENTRY_KEY_TO_ORACLE_INPUT`),
* which oracle output is which qualified channel (`ORACLE_OUTPUT_TO_CHANNEL`),
* which qualified key or channel each constraint's predicate operand means
  (`operand_bindings`, design D12), and
* the glue values the era adapter feeds per point (`glue_values`, design D13).

Three published surfaces and nothing else: `evaluate`, `operand_bindings`,
`glue_values`. The independent oracle `verify_stellaris.py` is imported and
never modified — it stays independent evidence, and a study-seam edit to it
would compromise that.

Everything here fails closed. An entry key with no declared mapping, two keys
that map to one oracle input but disagree, or an oracle output with no channel
is a mechanical failure, not a silently skipped comparison.

**Editing this file retires every existing study store.** It is one of the era
adapter's three declared sources (design Invariant 4), because it feeds numbers
into a run — so its bytes are part of the effective executable fingerprint.
"""

from __future__ import annotations

import functools
import sys
from collections.abc import Mapping
from pathlib import Path

E2E = Path(__file__).resolve().parent.parent
if str(E2E) not in sys.path:
    sys.path.insert(0, str(E2E))

import verify_stellaris as vs  # noqa: E402  (the independent oracle, unmodified)

# The profile integral depends only on (alpha_n, alpha_T, T_i0), none of which any
# study sweeps, so memoizing it is exact rather than an approximation. Applied once
# at import (`run_design_search.py:79`).
if not hasattr(vs._profile_integral, "cache_info"):
    vs._profile_integral = functools.lru_cache(maxsize=None)(vs._profile_integral)

P = "stellarator_09__stellaris__"

#: Sentinel: the key is fed to the package by glue and is *not* an oracle input —
#: the oracle recomputes the same quantity from its own inputs. Feeding it back
#: would make the check circular, so it is dropped, and the glue ledger discloses it.
GLUE_FED = "<glue-fed, recomputed by the oracle>"

#: Sentinel: the key is a dead schema filler. Nothing in the executed pipeline reads
#: it (the adapter asserts that on every load), so it moves no number either way.
DEAD_FILLER = "<dead schema filler>"

#: Qualified entry key -> oracle input name. Every key that can appear in a proposal
#: or in a recorded case's inputs is declared here; an undeclared key is a failure.
ENTRY_KEY_TO_ORACLE_INPUT: dict[str, str] = {
    f"{P}geom__R": "R",
    f"{P}rb__R": "R",
    f"{P}magnet__R0": "magnet_R0",
    f"{P}geom__a": "a",
    f"{P}rb__a": "a",
    f"{P}cas72_calc__availability": "availability",
    f"{P}fuel_calc__availability": "availability",
    f"{P}lcoe_calc__availability": "availability",
    f"{P}lcoe_1cfe_calc__availability": "availability",
    f"{P}cas23_to_28_capital__cas28_capital": "cas28_capital",
    f"{P}cas2x_pre_contingency__cas28_capital": "cas28_capital",
    f"{P}replacement_cost_per_event__n_mod": "n_mod",
    f"{P}cas23_to_28_capital__special_materials_capital": GLUE_FED,
    f"{P}cas2x_pre_contingency__special_materials_capital": GLUE_FED,
    "mfe_plant__MFE_Power_Plant__p_th": DEAD_FILLER,
    "mfe_plant__MFE_Power_Plant__p_the": DEAD_FILLER,
    "mfe_plant__MFE_Power_Plant__p_et": DEAD_FILLER,
}

#: Oracle output name -> qualified channel name. Only channels the package records
#: as single-field floats appear; the oracle returns more than the package does.
ORACLE_OUTPUT_TO_CHANNEL: dict[str, str] = {
    "V": f"{P}geom__V",
    "p_fus": f"{P}fusion__p_fus",
    "p_th": f"{P}pb__p_th",
    "p_the": f"{P}pb__p_the",
    "p_et": f"{P}pb__p_et",
    "p_cryo": f"{P}cryo_elec__p_elec",
    "q_eng": f"{P}pb__q_eng",
    "rec_frac": f"{P}pb__rec_frac",
    "p_net": f"{P}pb__p_net",
    "wall_load": f"{P}wall_load_calc__wall_load",
    "magnet": f"{P}magnet_cost__capital_cost",
    "heating": f"{P}heating_cost__cost",
    "divertor": f"{P}divertor_cost__cost",
    "blanket": f"{P}blanket_cost__cost",
    "shield": f"{P}shield_cost__cost",
    "structure": f"{P}structure_cost__cost",
    "vessel": f"{P}vessel_cost__cost",
    "power_supplies": f"{P}power_supplies_cost__cost",
    "turbine": f"{P}turbine_cost__cost",
    "electric": f"{P}electric_cost__cost",
    "heat_rejection": f"{P}heat_rejection_cost__cost",
    "misc": f"{P}misc_cost__cost",
    "buildings": f"{P}buildings_cost__cost",
    "precon": f"{P}precon_cost__cost",
    # The package's om_cost channel is the *unlevelized* annual O&M; the oracle's
    # `annual_om` is the levelized one. Checked against the committed store, not
    # matched by name — the names agree and the numbers do not.
    "annual_om_unlevelized": f"{P}om_cost__annual_om",
    "powercore_capital": f"{P}powercore_capital__powercore_capital",
    "bop_capital": f"{P}bop_capital__bop_capital",
    "remote_handling": f"{P}remote_handling__cost",
    "installation": f"{P}installation__cost",
    "coolant": f"{P}coolant__cost",
    "aux_cooling": f"{P}aux_cooling__cost",
    "waste": f"{P}waste__cost",
    "fuel_handling": f"{P}fuel_handling__cost",
    "other_rpe": f"{P}other_rpe__cost",
    "inc": f"{P}inc_cost__cost",
    "owner": f"{P}owner__cost",
    "supplementary": f"{P}supplementary__cost",
    "idc_capital": f"{P}idc__cost",
    "cas22_capital": f"{P}cas22_capital__cas22_capital",
    "cas2x_pre_contingency": f"{P}cas2x_pre_contingency__cas2x_pre_contingency",
    "cas20_capital": f"{P}cas20_capital__cas20_capital",
    "cas23_to_28_capital": f"{P}cas23_to_28_capital__cas23_to_28_capital",
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "contingency_capital": f"{P}contingency__cost",
    "indirect_capital": f"{P}indirect__cost",
    "total_capital": f"{P}total_capital__total_capital",
    "lcoe": f"{P}lcoe_calc__lcoe",
    "annual_fuel": f"{P}fuel_calc__annual_fuel",
    "cas72_annual": f"{P}cas72_calc__cost",
    "cas90_1cfe": f"{P}cas90_1cfe_calc__cas90",
    "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
}

#: Qualified entry keys the era adapter injects per point, and the oracle output
#: each one carries (design D13, glue rungs g2/g3). These are *parameters* of the
#: package, not output channels, so they cannot travel through `evaluate`'s return.
GLUE_VALUE_KEYS: dict[str, str] = {
    f"{P}cas23_to_28_capital__special_materials_capital": "special_materials",
    f"{P}cas2x_pre_contingency__special_materials_capital": "special_materials",
    "mfe_plant__MFE_Power_Plant__p_th": "p_th",
    "mfe_plant__MFE_Power_Plant__p_the": "p_the",
    "mfe_plant__MFE_Power_Plant__p_et": "p_et",
}

#: constraint_id -> source_name -> {"kind", "key"} (design D12).
#:
#: Hand-authored because it cannot be inferred: of the nine `feature_ref` operands
#: across the five constraints, `net_positive.net_electric` resolves to no parameter
#: and no key by name at all (it is the `pb__p_net` channel), and the three that
#: could be name-matched use three different composition rules. A tool that guessed
#: would compare the wrong number and read as a pass.
OPERAND_BINDINGS: dict[str, dict[str, dict[str, str]]] = {
    f"{P}beta_ok__82b78aad420730d5": {
        "beta": {"kind": "input", "key": f"{P}beta"},
        "beta_limit": {"kind": "input", "key": f"{P}beta_limit"},
    },
    f"{P}net_positive__484521d56c02667a": {
        # No parameter and no key contains "net_electric": it is the power-balance
        # net electric channel, which the era store does not record but the oracle
        # returns. This operand is why bindings are published rather than inferred.
        "net_electric": {"kind": "channel", "key": f"{P}pb__p_net"},
    },
    f"{P}recirc_ok__afc3be66f0a3421b": {
        "rec_frac": {"kind": "channel", "key": f"{P}pb__rec_frac"},
        # Constraint-id-prefixed: one of the three composition rules in play.
        "threshold": {"kind": "input", "key": f"{P}recirc_ok__afc3be66f0a3421b__threshold"},
    },
    f"{P}tbr_ok__2cd198f674d413e4": {
        "tbr": {"kind": "input", "key": f"{P}tbr"},
        "tbr_floor": {"kind": "input", "key": f"{P}tbr_floor"},
    },
    f"{P}wall_load_ok__ab2c790419af93bb": {
        "wall_load": {"kind": "channel", "key": f"{P}wall_load_calc__wall_load"},
        "wall_load_limit": {"kind": "input", "key": f"{P}wall_load_limit"},
    },
}


class OracleSeamError(Exception):
    """A point, key, or output this seam cannot map. Always a mechanical failure."""


def _oracle_overrides(point: Mapping[str, float]) -> dict[str, float]:
    """Translate qualified entry keys into oracle inputs, refusing anything undeclared.

    Several keys carry one physical quantity (``geom__R`` and ``rb__R`` are both the
    major radius). They must agree: a proposal that set them apart would be two
    different geometries, and the oracle can only be given one.
    """
    overrides: dict[str, float] = {}
    for key, value in point.items():
        name = ENTRY_KEY_TO_ORACLE_INPUT.get(key)
        if name is None:
            raise OracleSeamError(
                f"entry key has no declared oracle mapping: {key!r} "
                f"(declare it in ENTRY_KEY_TO_ORACLE_INPUT, or as GLUE_FED/DEAD_FILLER)"
            )
        if name in (GLUE_FED, DEAD_FILLER):
            continue
        if name in overrides and overrides[name] != float(value):
            raise OracleSeamError(
                f"entry keys disagree on oracle input {name!r}: already {overrides[name]}, "
                f"then {key!r} = {float(value)}"
            )
        overrides[name] = float(value)
    return overrides


def _compute(overrides: Mapping[str, float]) -> dict[str, float]:
    """Run the independent oracle at a point, restoring its module globals after."""
    saved = dict(vs.IN)
    vs.IN.update(overrides)
    try:
        return vs.compute()
    finally:
        vs.IN.clear()
        vs.IN.update(saved)


def evaluate(point: Mapping[str, float]) -> dict[str, float]:
    """Recompute a point through the independent oracle. Qualified keys in, channels out.

    The returned map is keyed by the package's qualified channel names, so a generic
    tool can compare it to a recorded case's outputs without knowing anything about
    this package.
    """
    result = _compute(_oracle_overrides(point))
    channels = {}
    for name, channel in ORACLE_OUTPUT_TO_CHANNEL.items():
        if name not in result:
            raise OracleSeamError(
                f"oracle returned no output {name!r} declared for channel {channel!r}"
            )
        channels[channel] = float(result[name])
    return channels


def operand_bindings() -> dict[str, dict[str, dict[str, str]]]:
    """Publish which qualified key or channel each predicate operand means (D12)."""
    return {
        cid: {name: dict(binding) for name, binding in ops.items()}
        for cid, ops in OPERAND_BINDINGS.items()
    }


def glue_values(point: Mapping[str, float]) -> dict[str, float]:
    """The per-point values the era adapter injects as glue (D13, rungs g2/g3).

    These are package *parameters*, not channels, so they travel on their own call
    rather than through `evaluate`. One mapping and one save/restore, in one file,
    so the adapter's injection and the verifier's recompute cannot drift apart.
    """
    result = _compute(_oracle_overrides(point))
    values = {}
    for key, name in GLUE_VALUE_KEYS.items():
        if name not in result:
            raise OracleSeamError(f"oracle returned no output {name!r} declared for key {key!r}")
        values[key] = float(result[name])
    return values
