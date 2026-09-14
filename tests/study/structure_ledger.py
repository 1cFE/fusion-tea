"""The WI-057 rename ledger for the study tests.

WI-057 (2026-09-13, the Stellaris structural decomposition re-applied onto feat/demo-maturation): the
calcs live on the parts that own them, so entry-point and channel names carry the owning part's path
(``stellarator_09__stellaris__R`` -> ``stellarator_09__stellaris__plasma__R``). Frozen expectation files
written before it keep their names; a test that compares a live mapping against one translates the frozen
side through this ledger, never the frozen file. Constraint ids, parameter groups and values are unchanged.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = ROOT / "work/active/WI-057_stellaris-structural-decomposition/evidence/merge_onto_demo_maturation/ledger.json"
_LEDGER = json.loads(LEDGER_PATH.read_text())
RENAMED = {**_LEDGER["parameters"], **_LEDGER["outputs"]}
P = "stellarator_09__stellaris__"


def renamed(key):
    """An entry point or channel under its WI-057 name (unchanged keys pass through)."""
    return RENAMED.get(key, key)


def renamed_keys(mapping):
    return {renamed(key): value for key, value in mapping.items()}


def renamed_values(mapping):
    return {key: renamed(value) for key, value in mapping.items()}
