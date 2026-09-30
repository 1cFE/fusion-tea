"""Package-owned oracle seam for magnet_materials_tea (name mapping only; no physics, no tolerance).

`scripts/study/verify.py` is generic: it imports the module the manifest names and requires two published
surfaces, `evaluate` and `operand_bindings`. Everything that is this package's knowledge lives here:

* `evaluate(point)` takes the complete generated entry map of one case and returns the independent oracle's
  value for every non-constant package channel, keyed by the package channel name.
* `operand_bindings()` names, for each executing constraint, which package channel each predicate operand is
  bound to (read from the design binding in exploration/magnet_materials/input_models/magnet_subsystem.sysml:
  every assert takes the part-level alias of a calc output).

Both mappings go through the reviewed studies/interface_data.py and delegate every number to the independently
authored exploration/magnet_materials/oracle.py (`evaluate_case`, `turn_current`). Nothing here computes anything.

Not covered: the nine constant formula channels (nb3sn/rebco eps_min, k_a, k_d, k_g, k_i), which the oracle
carries as fixed design values and which no case can move; `constant_channels()` lists them so a verifier can
exclude them explicitly. The tolerance the comparison runs at is declared in studies/manifest.json
(`absolute_tolerances`, contract r3 section 8), not here.

The sealed record 20260929-magnet-material-comparison binds the same mapping through its own record-local
`oracle_entry.py` (written before this module existed; finding 20260929-magnet-material-comparison#2). That copy
stays sealed; this module is the package's authoritative entry from the stock manifest onward.
"""
from __future__ import annotations

from exploration.magnet_materials import oracle
from exploration.magnet_materials.studies import interface_data

INTERFACE = interface_data.INTERFACE
_ENTRY_TO_ATTRIBUTE = {entry: name for name, entry in INTERFACE["design_attributes"].items()}
_CONSTANT_CHANNELS = {fixed["channel"] for fixed in INTERFACE["fixed_constants"].values()}
PARTS = ("duty", "economics", "nb3sn", "rebco")
CALCS = ("conductor", "area", "inventory", "cold_load", "refrigeration", "annualized")


def case_from_point(point: dict) -> dict:
    """Design section 6 nested case from a generated entry map; fixed design values are ignored (the oracle owns them)."""
    case = {part: {} for part in PARTS}
    for entry, value in point.items():
        name = _ENTRY_TO_ATTRIBUTE.get(entry)
        if name is None:
            if entry not in INTERFACE["fixed_entries"]:
                raise KeyError(f"unknown entry key {entry}")
            continue
        part, attribute = name.split(".", 1)
        case[part][attribute] = float(value)
    missing = [name for name in INTERFACE["design_attributes"] if name.split(".", 1)[1] not in case[name.split(".", 1)[0]]]
    if missing:
        raise KeyError(f"case lacks design section 6 attributes: {missing}")
    return case


def evaluate(point: dict) -> dict:
    """Independent oracle value for every non-constant package channel of one generated entry map."""
    case = case_from_point(point)
    result = oracle.evaluate_case(case)
    channels = {}
    for name, channel in INTERFACE["output_channels"].items():
        if channel in _CONSTANT_CHANNELS:
            continue
        parts = name.split(".")
        if parts[0] == "duty" and parts[1] == "turn_current":
            value = oracle.turn_current(case["duty"])
        elif parts[0] == "pair":
            value = result["pair"][parts[1]]
        elif len(parts) == 2:
            value = result[parts[0]][parts[1]]
        elif parts[1] in CALCS:
            value = result[parts[0]][parts[1]][parts[2]]
        else:
            raise KeyError(f"no oracle value for channel {name}")
        channels[channel] = float(value)
    return channels


def constant_channels() -> list[str]:
    """Package channels the oracle carries as fixed design values; excluded from comparison, never compared."""
    return sorted(_CONSTANT_CHANNELS)


def operand_bindings() -> dict:
    """Predicate operand -> package channel, per constraint id, from the design's assert bindings. A fresh copy per call."""
    channel = INTERFACE["output_channels"]
    table = {}
    for name, constraint_id in INTERFACE["constraint_ids"].items():
        material, local = name.split(".", 1)
        if local == "acceptance_ok":
            operands = {"supported_in": channel[f"{material}.conductor.supported"],
                        "margin_in": channel[f"{material}.conductor.acceptance_margin"]}
        elif local == "fit_ok":
            operands = {"fit_margin_in": channel[f"{material}.area.fit_margin"]}
        elif local == "copper_ok":
            operands = {"cu_margin_in": channel[f"{material}.area.cu_margin"]}
        elif local == "steel_ok":
            operands = {"steel_margin_in": channel[f"{material}.area.steel_margin"]}
        elif local == "capacity_ok":
            operands = {"capacity_margin_in": channel[f"{material}.refrigeration.capacity_margin"]}
        else:
            raise KeyError(f"unknown constraint {name}")
        table[constraint_id] = {operand: {"kind": "channel", "key": key} for operand, key in operands.items()}
    return table


__all__ = ["evaluate", "operand_bindings", "constant_channels", "case_from_point"]
