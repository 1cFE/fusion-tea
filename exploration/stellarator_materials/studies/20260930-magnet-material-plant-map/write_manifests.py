"""Step 5 (manifests): place the three per-unit manifests in the record directory.

* reference, rebco: the stock `studies/<unit>/manifest.json` copied unchanged except the oracle block, which names this
  record's binding (the stock block names `exploration.stellarator_materials.studies.oracle_entry`, which was never
  written; implementation notes deviation 6). Every fingerprint, the baseline point, headline and verdicts are kept.
* nb3sn: written here, because the unit's generated default refuses (design K22) and no stock manifest exists. The
  baseline point is the policy's first evaluable Nb3Sn design, the case the case-file header names as the K22 candidate
  (`anchored-1-nb3sn-12T-R12.7-a1.3-reference-none`): its declared inputs over the package's own defaults (the
  interface baseline point), less `magnet__eps_min`, a package constant equal to the case's value. The pinned headline
  and verdicts are the independent oracle's at that point, so the baseline gate compares the package against the
  oracle. Fingerprints are the unit's live contracts and the indicator-input recipe over the package.
* r5a (contract section 9 amended at 97fabad31, coordinator ruling on the gate-8 BLOCKER): both material manifests
  declare `absolute_tolerances` of 1e-9 per unit, in Round 1's record-manifest form (channel, value, units, basis), on
  every channel scripts/study/verify.py compares that the offer policy sizes at allowance: the conductor acceptance
  margin (the smallest passing element count) and the area fit, copper and steel margins (pack at the 5 mm step, areas
  rounded up to 1e-6 mm2). verify.py refuses an absolute tolerance on a channel it does not compare, so the other
  at-allowance channels (e.g. `magnet__conductor__temp_rule_margin`) carry the r5a clause in the record's full
  comparison (verify_all.py), not here. The reference manifest is unchanged: its one point is the pin, sized by no
  policy. No fingerprint, baseline, headline or verdict changes.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/write_manifests.py [unit ...]'
"""
from __future__ import annotations

import json

import record_common as rc
from exploration.stellarator_materials.studies.interface_data import INTERFACE
from scripts.study import manifest as manifest_mod

def oracle_block(unit: str) -> dict:
    return {
    "kind": "python_callable",
    "module": f"exploration.stellarator_materials.studies.{rc.STUDY_ID}.oracle_{unit}",
    "callable": "evaluate",
    "sys_path": ".",
    "note": ("Record-local per-unit surface (oracle_<unit>.py over oracle_entry.py) of the name-mapping binding of the independent WI-100 oracle exploration/stellarator_materials/"
             "oracle_glue.py (evaluate_material_case / evaluate_reference_case; separate author, design section 6.3). "
             "It maps unit prefixes, drops the five NIST coefficient keys and the zero manufacturing rate after "
             "checking they equal the constants the oracle holds, and keys operand bindings by package constraint id; "
             "it adds no arithmetic. Imported by dotted name because oracle_glue imports the plant seam as the "
             "top-level module oracle_entry. The stock studies/<unit>/manifest.json names "
             "exploration.stellarator_materials.studies.oracle_entry, which was not written at build time."),
    }


R5A_BASIS = ("plant-contract.md r5a section 9: every recorded channel compared at 1e-9 relative or 1e-9 absolute per "
             "unit of the channel, whichever is looser (Round 1's clause, restored after the Nb3Sn seam refused at gate "
             "8); the offer policy sizes this margin at allowance, where a relative test alone measures the package's "
             "root tolerance or rounding, not disagreement")
AT_ALLOWANCE = {  # channel suffix -> units, per material
    "rebco": {"magnet__conductor__acceptance_margin": "1 (fraction rule: 0.80 - I/Ic)",
              "magnet__area__fit_margin": "mm^2 per turn", "magnet__area__cu_margin": "mm^2 per turn",
              "magnet__area__steel_margin": "mm^2 per turn"},
    "nb3sn": {"magnet__conductor__acceptance_margin": "K (temperature rule: T_cs - T_supply - 0.7 K - 1.5 K)",
              "magnet__area__fit_margin": "mm^2 per turn", "magnet__area__cu_margin": "mm^2 per turn",
              "magnet__area__steel_margin": "mm^2 per turn"},
}


def absolute_tolerances(unit: str) -> list[dict]:
    P = INTERFACE["units"][unit]["prefix"]
    return [{"channel": P + suffix, "value": 1e-9, "units": units, "basis": R5A_BASIS}
            for suffix, units in AT_ALLOWANCE[unit].items()]


def copied(unit: str) -> dict:
    data = json.loads((rc.PACKAGE_STUDIES / unit / "manifest.json").read_text())
    data["oracle"] = oracle_block(unit)
    if unit in AT_ALLOWANCE:
        data["absolute_tolerances"] = absolute_tolerances(unit)
    return data


def nb3sn_manifest() -> dict:
    U = INTERFACE["units"]["nb3sn"]
    P = U["prefix"]
    case = next(c for c in rc.load_cases()["cases"] if c["case_id"] == rc.K22_CASE)
    header = rc.load_cases(check=False)["header"]["baseline_points"]["nb3sn"]
    if header["k22_candidate"] != rc.K22_CASE:
        raise RuntimeError("the case file names a different K22 candidate")
    point = {k: float(v) for k, v in U["baseline_point"].items()}
    for key, value in case["inputs"].items():
        if key not in point:
            constant = U["constant_channels"].get(key)
            if constant is None or float(value) != float(constant["value"]):
                raise RuntimeError(f"{key} is neither an entry key nor its package constant")
            continue
        point[key] = float(value)
    oracle = rc.oracle()
    result = oracle.evaluate_full(point)
    headline = result["channels"][P + "lcoe_calc__lcoe"]
    if headline != case["expected"]["channels"]["lcoe_calc__lcoe"]:
        raise RuntimeError("the oracle does not reproduce the policy's recorded LCOE at the K22 candidate")
    verdicts = [{"source_local_identity": local, "expected": status}
                for local, status in sorted(result["verdicts"].items())]
    if any(v["expected"] not in ("satisfied", "violated") for v in verdicts):
        raise RuntimeError("an indeterminate verdict cannot be pinned")
    package = rc.REPO / "exploration/stellarator_materials/units/nb3sn/stellarator_materials_nb3sn_tea"
    fingerprint = manifest_mod.indicator_input_fingerprint(package)
    rebco = json.loads((rc.PACKAGE_STUDIES / "rebco" / "manifest.json").read_text())
    objectives = [dict(o, channel=o["channel"].replace(INTERFACE["units"]["rebco"]["prefix"], P))
                  for o in rebco["objective_catalog"]]
    return {
        "schema_version": "study-package-manifest/v1",
        "package": {"name": "stellarator_materials_nb3sn_tea",
                    "path": manifest_mod.repo_relative_posix(package)},
        "fingerprints": {
            "indicator_inputs": {"recipe": fingerprint["recipe"], "digest": fingerprint["digest"],
                                 "files": [f["path"] for f in fingerprint["files"]]},
            "recorded_provenance": {"executable_fingerprint": manifest_mod.read_executable_fingerprint(package),
                                    "semantic_fingerprint": manifest_mod.read_semantic_fingerprint(package)},
        },
        "objective_catalog": objectives,
        "ties": [],
        "baseline": {"point": dict(sorted(point.items())),
                     "headline": {"channel": P + "lcoe_calc__lcoe", "value": headline},
                     "verdicts": verdicts},
        "oracle": oracle_block("nb3sn"),
        "absolute_tolerances": absolute_tolerances("nb3sn"),
    }


if __name__ == "__main__":
    import sys

    for unit in (sys.argv[1:] or rc.UNITS):
        data = nb3sn_manifest() if unit == "nb3sn" else copied(unit)
        manifest_mod.validate(data)
        path = rc.manifest_path(unit)
        with path.open("x") as stream:
            json.dump(data, stream, indent=2)
            stream.write("\n")
        loaded = manifest_mod.load(path)
        package = rc.REPO / loaded.data["package"]["path"]
        manifest_mod.assert_package_identity(loaded, package)
        manifest_mod.assert_pin_matches(loaded, manifest_mod.indicator_input_fingerprint(package))
        print(unit, path.name, "pin", loaded.pinned_digest, "headline", loaded.data["baseline"]["headline"]["value"],
              "violated", [v["source_local_identity"] for v in loaded.data["baseline"]["verdicts"]
                           if v["expected"] == "violated"])
