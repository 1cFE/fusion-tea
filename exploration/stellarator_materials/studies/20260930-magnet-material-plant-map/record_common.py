"""Shared record-local names for study 20260930-magnet-material-plant-map (paths, units, the case file).

No model arithmetic. Every script in this record imports it after putting the repository root on sys.path.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RECORD = Path(__file__).resolve().parent
REPO = RECORD.parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

STUDY_ID = RECORD.name
# The record's oracle binding is imported by its dotted name only: oracle_glue itself imports the plant seam as the
# top-level module `oracle_entry` (exploration/stellarator_e2e/studies/oracle_entry.py), so the record's file must never
# be imported as a bare `oracle_entry`.
ORACLE_MODULE = f"exploration.stellarator_materials.studies.{STUDY_ID}.oracle_entry"
ROUTE_MODULE = f"{STUDY_ID}.route_entry"  # imported with sys_path exploration/stellarator_materials/studies
PACKAGE_STUDIES = RECORD.parent
CASES = PACKAGE_STUDIES / "cases.json"
CASES_SHA256 = "f07133acdd561610287ff9dea01f641bf48b1562ec417254c85484ea8645e583"
RESULTS = RECORD / "results"
NATIVE = RESULTS / "native"
UNITS = ("reference", "rebco", "nb3sn")
MATERIALS = ("rebco", "nb3sn")
ARMS = {"reference": "arm-reference", "rebco": "arm-rebco", "nb3sn": "arm-nb3sn"}
K22_CASE = "anchored-1-nb3sn-12T-R12.7-a1.3-reference-none"  # cases.json header baseline_points.nb3sn.k22_candidate


def oracle():
    import importlib

    return importlib.import_module(ORACLE_MODULE)


def manifest_path(unit: str) -> Path:
    return RECORD / f"manifest_{unit}.json"


def axes_path(unit: str) -> Path:
    return RECORD / f"axes_{unit}.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_cases(check: bool = True) -> dict:
    raw = CASES.read_bytes()
    if check and hashlib.sha256(raw).hexdigest() != CASES_SHA256:
        raise RuntimeError(f"{CASES} is not the declared case set (sha256 {CASES_SHA256})")
    return json.loads(raw)


def write_json(obj, path: Path, compact: bool = False) -> Path:
    """Write once; refuse to overwrite evidence."""
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"{path} exists; preserve evidence")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text((json.dumps(obj, separators=(",", ":"), allow_nan=True) if compact
                    else json.dumps(obj, indent=1, sort_keys=False, allow_nan=True)) + "\n")
    tmp.replace(path)
    return path
