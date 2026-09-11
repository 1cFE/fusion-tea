"""Reproduce IFE metadata using native capture, census and executed baseline evidence."""
from pathlib import Path
import argparse
import json
from scripts.integrate import rederived_census
from scripts.study import common, manifest
from sysml_codegen.snapshot.capture import capture_instance_graph_snapshot
from exploration.ife_e2e.studies import study_route as route
from tests.ife_oracle import assert_source_outputs


def prepare_metadata(work_dir: Path):
    """Write package-owned metadata after checking the executed baseline independently."""
    contract = json.loads((route.PACKAGE_DIR / "contracts/model_contract.json").read_text())
    point = {p["qualified_name"]: p["default_value"] for p in contract["parameters"]}
    cases, _ = route.run_points("ife-metadata-baseline-v1", [point], work_dir)
    case = route._completed(cases, "metadata baseline")[0]
    assert_source_outputs(case.outputs)
    verdicts = route.short_verdicts(case)
    if verdicts != {"net_positive": "satisfied", "viability": "satisfied"}:
        raise route.RouteError(f"audited baseline verdicts changed: {verdicts}")
    fingerprint = manifest.indicator_input_fingerprint(route.PACKAGE_DIR)
    semantic = manifest.read_semantic_fingerprint(route.PACKAGE_DIR)
    doc = {
        "schema_version": manifest.MANIFEST_SCHEMA_VERSION,
        "package": {"name": route.PACKAGE_NAME, "path": manifest.repo_relative_posix(route.PACKAGE_DIR)},
        "fingerprints": {
            "indicator_inputs": fingerprint | {"files": [e["path"] for e in fingerprint["files"]]},
            "recorded_provenance": {
                "executable_fingerprint": manifest.read_executable_fingerprint(route.PACKAGE_DIR),
                "semantic_fingerprint": semantic,
            },
        },
        "objective_catalog": [{"name": name, "channel": channel} for name, channel in sorted(route.CHANNELS.items())],
        "ties": [],
        "baseline": {
            "point": point,
            "headline": {"channel": route.P + "hawker_price__price", "value": case.outputs[route.P + "hawker_price__price"]},
            "verdicts": [{"source_local_identity": name, "expected": value} for name, value in sorted(verdicts.items())],
        },
        "oracle": {"kind": "python_callable", "module": "exploration.ife_e2e.studies.oracle_entry",
                   "callable": "evaluate", "sys_path": "."},
    }
    manifest.validate(doc)
    census = rederived_census(route.PACKAGE_DIR) | {"derived_against_semantic_fingerprint": semantic}
    capture_instance_graph_snapshot([route.E2E / "models"], route.E2E / "ife.snapshot.json")
    common.write_document(doc, route.MANIFEST_PATH)
    common.write_document(census, route.HERE / "census.json")
    common.write_document({"schema_version": "study-axis-declaration/v1", "groups": [
        {"axis": axis, "note": "One authoritative WI-048 entry point; window belongs to the study.",
         "keys": [{"key": route.P + key, "provenance": "fan_out"}]}
        for axis, key in (("beam_energy_mj", "driver__beam_energy_mj"), ("frequency", "frequency"))
    ]}, route.HERE / "axes.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    prepare_metadata(parser.parse_args().work_dir)
