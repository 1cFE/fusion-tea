"""Record-local baseline entry points over the package route (no model arithmetic, no glue).

The integration seam invokes `<callable>(out_dir, package_dir=..., manifest_path=...)`
(scripts/study/read_coverage.py:258). The package route's own `study_route.execute_baseline(name, out_dir)` takes a unit
name and reads the unit's stock manifest, and the Nb3Sn unit has no stock manifest (implementation notes, deviation 4).
These three callables adapt only the call signature: each runs the given manifest's pinned baseline point for one unit
through `study_route.run_points` (stock strict loader, PreparedEvaluator, StudyRunner, PreparedListStrategy,
StudyStore) and deposits the same two documents `execute_baseline` deposits.

Invoked by the seam with --route-sys-path exploration/stellarator_materials/studies and
--route-module 20260930-magnet-material-plant-map.route_entry, so every Python source the route reads (study_route.py,
interface_data.py, this file) lies under the declared route directory.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RECORD = Path(__file__).resolve().parent
REPO = RECORD.parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from exploration.stellarator_materials.studies import study_route as route  # noqa: E402
from scripts.study import common  # noqa: E402


def execute_unit_baseline(name: str, out_dir, *, package_dir=None, manifest_path=None, suffix: str = "") -> dict:
    unit = route.unit_of(name)
    out = Path(out_dir)
    package_dir = Path(package_dir or unit.package_dir)
    if package_dir.resolve() != unit.package_dir.resolve():
        raise route.RouteError(f"{name}: package {package_dir} is not the unit's package {unit.package_dir}")
    manifest_path = Path(manifest_path or RECORD / f"manifest_{name}.json")
    manifest = json.loads(manifest_path.read_text())
    if manifest["package"]["name"] != unit.package_name:
        raise route.RouteError(f"{name}: manifest names package {manifest['package']['name']}")
    point = dict(manifest["baseline"]["point"])
    cases, db = route.run_points(name, f"stellarator-materials-{name}-baseline-r3", [point], out / "_work",
                                 package_dir=package_dir)
    case = route.completed(cases, f"{name} baseline point")[0]
    catalog = route._catalog_by_constraint_id(package_dir)
    identity_path = route.write_identity_document(name, out / f"package_identity{suffix}.json")
    result = {
        "schema_version": route.BASELINE_RESULT_SCHEMA_VERSION,
        "executed_under": {
            "identity_digest": case.executable_fingerprint,
            "store_id": common.manifest_mod.repo_relative_posix(db) if db.resolve().is_relative_to(REPO) else db.name,
            "case_id": case.candidate_id,
        },
        "point": {key: float(value) for key, value in sorted(point.items())},
        "channels": {key: float(value) for key, value in sorted(case.outputs.items())},
        "verdicts": [{"constraint_id": cid, "definition_qualified_name": catalog[cid]["definition_qualified_name"],
                      "source_local_identity": catalog[cid]["source_local_identity"], "status": status}
                     for cid, status in sorted(case.verdicts.items())],
    }
    result_path = common.write_document(result, out / f"baseline_result{suffix}.json")
    return {"identity": identity_path, "baseline_result": result_path}


def execute_baseline_reference(out_dir, package_dir=None, manifest_path=None):
    return execute_unit_baseline("reference", out_dir, package_dir=package_dir, manifest_path=manifest_path)


def execute_baseline_rebco(out_dir, package_dir=None, manifest_path=None):
    return execute_unit_baseline("rebco", out_dir, package_dir=package_dir, manifest_path=manifest_path)


def execute_baseline_nb3sn(out_dir, package_dir=None, manifest_path=None):
    return execute_unit_baseline("nb3sn", out_dir, package_dir=package_dir, manifest_path=manifest_path)
