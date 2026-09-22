"""Inspect generated artifacts and pin an existing native manifest without evaluation."""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.study import common, indicators, manifest
from exploration.aries_integrated.studies import study_route as route


def discover(package_dir: Path) -> dict:
    """Return working inventory using the native strict artifact readers.

    This is preparation data, not an executable manifest or a study snapshot.
    It loads no generated Python and computes no physical quantity.
    """
    package_dir = Path(package_dir).resolve()
    fingerprint = manifest.indicator_input_fingerprint(package_dir)
    parsed = indicators.read_pipelines(package_dir)
    pinned_paths = {path.resolve() for path in manifest.indicator_input_read_set(package_dir)}
    for path in parsed.artifact_paths:
        if not path.resolve().is_relative_to(package_dir) or path.resolve() not in pinned_paths:
            raise route.RouteError(f"pipeline read is outside the fingerprint read set: {path}")
    graph = indicators.build_graph(parsed)
    contract = indicators.read_model_contract(package_dir)
    entries = {}
    point = {}
    for module in parsed.modules.values():
        if module.module_type != "EntryPoint":
            continue
        for group, port in module.inputs.items():
            source = (module.file.parent / port.ref).resolve()
            values = common.read_json(source, "generated entry defaults")
            for key, value in values.items():
                if key in entries:
                    raise route.RouteError(f"duplicate entry field: {key}")
                entries[key] = group
                point[key] = value
    if set(entries) != set(graph.input_keys):
        raise route.RouteError("entry mapping and native graph key set differ")
    concrete = contract.concrete_entries
    constraint_ids = [entry["constraint_id"] for entry in concrete]
    if len(set(constraint_ids)) != len(constraint_ids):
        raise route.RouteError("duplicate emitted constraint IDs")
    after = manifest.indicator_input_fingerprint(package_dir)
    if after != fingerprint:
        raise route.RouteError("package artifacts changed during discovery")
    return {
        "package": {"name": manifest.read_package_name(package_dir),
                    "path": manifest.repo_relative_posix(package_dir)},
        "fingerprints": {
            "indicator_inputs": fingerprint,
            "recorded_provenance": {
                "executable_fingerprint": manifest.read_executable_fingerprint(package_dir),
                "semantic_fingerprint": contract.semantic_fingerprint,
            },
        },
        "entry_keys": dict(sorted(entries.items())),
        "entry_types": dict(sorted(contract.entry_types.items())),
        "point": dict(sorted(point.items())),
        "produced_channels": dict(sorted(graph.producer.items())),
        "constraint_catalog": {"concrete_entries": concrete},
    }


def pin_manifest(manifest_path: Path, package_dir: Path) -> dict:
    """Repin a complete native manifest; never invent headline or verdict values."""
    common.assert_tree_clean(package_dir)
    loaded = manifest.load(manifest_path)
    manifest.assert_package_identity(loaded, package_dir)
    inventory = discover(package_dir)
    document = loaded.data
    if set(document["baseline"]["point"]) != set(inventory["entry_keys"]):
        raise route.RouteError("manifest baseline must contain the complete entry map")
    unknown = {entry["channel"] for entry in document["objective_catalog"]} - set(
        inventory["produced_channels"])
    if unknown:
        raise route.RouteError(f"manifest channels absent from generated graph: {sorted(unknown)}")
    fingerprints = inventory["fingerprints"]
    document["fingerprints"] = {
        **fingerprints,
        "indicator_inputs": {
            **fingerprints["indicator_inputs"],
            "files": [entry["path"] for entry in fingerprints["indicator_inputs"]["files"]],
        },
    }
    manifest.validate(document)
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=route.PACKAGE_DIR)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--pin-manifest", type=Path,
                        help="Existing complete native manifest; baseline is retained, not executed")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("output already exists; use a fresh path to preserve preparation evidence")
    document = (pin_manifest(args.pin_manifest, args.package) if args.pin_manifest
                else discover(args.package))
    common.write_document(document, args.out)


if __name__ == "__main__":
    main()
