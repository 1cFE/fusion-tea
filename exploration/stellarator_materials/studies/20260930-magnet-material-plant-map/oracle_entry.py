"""Record-local binding of the WI-100 independent oracle (no physics, no tolerance of its own beyond the clause below).

The oracle is `exploration/stellarator_materials/oracle_glue.py` (T-015 separate author, design section 6.3 and
contract r4): `evaluate_material_case(inputs, material)` for the two material units and `evaluate_reference_case(inputs)`
for the reference unit (which delegates to the plant oracle `exploration/stellarator_e2e/studies/oracle_entry.evaluate`
unchanged). This module only maps names:

* the unit is read from the key prefix (one unit per case);
* package entry keys the oracle does not accept under their package names are checked and dropped: the five
  non-negative NIST 316 coefficients `cryoplant__nist_k_{b,c,e,f,h}` must equal Round 1's `NIST316_COEFFS` (the oracle
  holds the fit as Round 1's constant, oracle-notes G1; the package names them `nist_k_*` per amendment A1) and
  `magnet__inventory__manufacturing_per_m_in` must be 0.0 (the oracle binds Round 1's manufacturing rate at 0, N4);
  any other value is refused, never passed;
* oracle channels are returned under the package's qualified channel names (prefix + suffix);
* `operand_bindings()` keys the oracle's operand bindings by the packages' constraint ids, matched through each
  package's own catalog (owner instance path + source-local identity), for all three units at once.

Tolerance clause (contract r5 sections 5 and 9; the oracle author's own test rule,
tests/models/test_stellarator_materials_oracle.py:155-158): a channel agrees when |native - oracle| <= 1e-9 |oracle|,
or |native - oracle| <= 1e-12 absolute for channels whose value is zero to rounding (the closure residuals); nonfinite
values must match exactly. Constant channels (the package's negative design literals) are excluded and listed by
`constant_channels()`; package channels the oracle does not produce are listed by `uncovered_channels()`.
"""
from __future__ import annotations

import json
import math
import sys
from functools import lru_cache
from pathlib import Path

RECORD = Path(__file__).resolve().parent
REPO = RECORD.parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from exploration.stellarator_materials import oracle_glue as og  # noqa: E402
from exploration.stellarator_materials.studies.interface_data import INTERFACE  # noqa: E402

REL = 1e-9
ABS_FLOOR = 1e-12
PREFIXES = {name: INTERFACE["units"][name]["prefix"] for name in ("reference", "rebco", "nb3sn")}
PACKAGE_DIRS = {name: REPO / "exploration/stellarator_materials/units" / name / f"stellarator_materials_{name}_tea"
                for name in PREFIXES}
NIST_PACKAGE_KEYS = {f"cryoplant__nist_{n}": v for n, v in zip(og.NIST_NAMES, og.r1.NIST316_COEFFS) if v >= 0.0}
MANUFACTURING_KEY = "magnet__inventory__manufacturing_per_m_in"


class OracleEntryError(Exception):
    """A name mapping this module refuses. Never a silent pass."""


def unit_of(point) -> str:
    units = {name for key in point for name, prefix in PREFIXES.items() if key.startswith(prefix)}
    # the reference prefix 'stellarator_09__stellaris__' is not a prefix of the material ones, and vice versa
    if len(units) != 1 or any(not any(k.startswith(PREFIXES[u]) for u in units) for k in point):
        raise OracleEntryError(f"a case names exactly one unit; found {sorted(units)}")
    return units.pop()


def oracle_inputs(point, unit: str) -> dict:
    """The case's inputs as the oracle accepts them (names only; values unchanged)."""
    if unit == "reference":
        return dict(point)
    P = PREFIXES[unit]
    out = {}
    for key, value in point.items():
        suffix = key[len(P):]
        if suffix in NIST_PACKAGE_KEYS:
            if float(value) != NIST_PACKAGE_KEYS[suffix]:
                raise OracleEntryError(f"{key} = {value!r} differs from Round 1's NIST 316 coefficient the oracle holds")
            continue
        if suffix == MANUFACTURING_KEY:
            if float(value) != 0.0:
                raise OracleEntryError(f"{key} = {value!r}; the oracle binds Round 1's manufacturing rate at 0")
            continue
        out[key] = value
    return out


def evaluate_full(point) -> dict:
    """The oracle's whole result for one case: {'unit', 'channels' (qualified), 'verdicts' (package local identity),
    'labels', 'checks', 'resolved'}. Domain refusals propagate as the oracle's own exceptions."""
    unit = unit_of(point)
    if unit == "reference":
        return {"unit": unit, "channels": og.evaluate_reference_case(oracle_inputs(point, unit)), "verdicts": None,
                "labels": None, "checks": None, "resolved": None}
    result = og.evaluate_material_case(oracle_inputs(point, unit), unit)
    verdicts = {local.split("__")[-1]: status for local, status in result["verdicts"].items()}
    if len(verdicts) != len(result["verdicts"]):
        raise OracleEntryError("oracle verdict names collide after dropping the owner path")
    return {"unit": unit, "channels": og.qualified(result), "verdicts": verdicts, "labels": result["labels"],
            "checks": result["checks"], "resolved": result["inputs"]}


def evaluate(point) -> dict:
    """Study API (scripts/study/verify.py): package channel name -> oracle value."""
    return evaluate_full(point)["channels"]


def constant_channels(unit: str) -> list[str]:
    return sorted(c["channel"] for c in INTERFACE["units"][unit]["constant_channels"].values())


def uncovered_channels(unit: str, oracle_channels) -> list[str]:
    """Published package channels, other than the constants, that the oracle returns no value for."""
    published = set(INTERFACE["units"][unit]["channels"])
    return sorted(published - set(oracle_channels) - set(constant_channels(unit)))


def agree(native, oracle) -> tuple[bool, float, float, str]:
    """(agrees, relative deviation, absolute error, clause used)."""
    native, oracle = float(native), float(oracle)
    if not (math.isfinite(native) and math.isfinite(oracle)):
        same = (math.isnan(native) and math.isnan(oracle)) or native == oracle
        return same, (0.0 if same else math.inf), (0.0 if same else math.inf), "nonfinite"
    err = abs(native - oracle)
    rel = err / max(abs(oracle), 1e-30)
    if err <= REL * abs(oracle):
        return True, rel, err, "relative"
    if err <= ABS_FLOOR:
        return True, rel, err, "absolute-floor"
    return False, rel, err, "none"


def _catalog(unit: str) -> list[dict]:
    contract = json.loads((PACKAGE_DIRS[unit] / "contracts" / "model_contract.json").read_text())
    return contract["constraint_catalog"]["concrete_entries"]


@lru_cache(maxsize=None)
def _bindings() -> dict:
    table = {}
    reference_ids = {e["constraint_id"] for e in _catalog("reference")}
    plant = og.oe.OPERAND_BINDINGS
    if set(plant) != reference_ids:
        raise OracleEntryError("the plant oracle's operand bindings do not name the reference unit's constraint ids")
    table.update({cid: {name: dict(binding) for name, binding in operands.items()} for cid, operands in plant.items()})
    for unit in ("rebco", "nb3sn"):
        P = PREFIXES[unit]
        by_local = og.operand_bindings(unit)
        owner_root = P[:-2]
        for entry in _catalog(unit):
            owner = entry["owner_instance_path"]
            if owner == owner_root:
                local = entry["source_local_identity"]
            elif owner.startswith(owner_root + "__"):
                local = owner[len(owner_root) + 2:] + "__" + entry["source_local_identity"]
            else:
                raise OracleEntryError(f"{entry['constraint_id']}: unexpected owner {owner}")
            if local not in by_local:
                raise OracleEntryError(f"{entry['constraint_id']}: the oracle binds no constraint {local!r}")
            table[entry["constraint_id"]] = by_local[local]
        if sum(1 for cid in table if cid.startswith(P)) != len(by_local):
            raise OracleEntryError(f"{unit}: binding count differs from the oracle's {len(by_local)}")
    return table


def operand_bindings(unit: str | None = None) -> dict:
    """Predicate operand -> {'kind': 'input'|'channel', 'key'}, per package constraint id: one unit's table (what
    scripts/study/verify.py needs, through oracle_<unit>.py), or all three units' when `unit` is None."""
    table = json.loads(json.dumps(_bindings()))
    if unit is None:
        return table
    ids = {e["constraint_id"] for e in _catalog(unit)}
    return {cid: operands for cid, operands in table.items() if cid in ids}


__all__ = ["evaluate", "evaluate_full", "operand_bindings", "constant_channels", "uncovered_channels", "agree",
           "oracle_inputs", "unit_of", "REL", "ABS_FLOOR"]
