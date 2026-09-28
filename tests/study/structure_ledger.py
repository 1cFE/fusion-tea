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
BACKWARD = {new: old for old, new in RENAMED.items() if old != new}
P = "stellarator_09__stellaris__"


def renamed(key):
    """An entry point or channel under its WI-057 name (unchanged keys pass through)."""
    return RENAMED.get(key, key)


def renamed_keys(mapping):
    return {renamed(key): value for key, value in mapping.items()}


def renamed_values(mapping):
    return {key: renamed(value) for key, value in mapping.items()}


def historical_name(key):
    """A live entry point or channel under the pre-decomposition name the frozen records use."""
    return BACKWARD.get(key, key)


def historical_package_view(package_dir, destination):
    """A copy of the live package whose input files carry the pre-decomposition key names, so a frozen study
    module can read `route.PACKAGE_DIR / "inputs" / ...` under its own lineage's names at import and export
    time. Values, groups, constraint ids and every other file are the live package's, byte for byte."""
    import shutil
    shutil.copytree(package_dir, destination, ignore=shutil.ignore_patterns("__pycache__"))
    for path in (destination / "inputs").glob("*.json"):
        values = json.loads(path.read_text())
        path.write_text(json.dumps({historical_name(k): v for k, v in values.items()}, indent=2) + "\n")
    return destination
