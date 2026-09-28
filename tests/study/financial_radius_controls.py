from tests.models.current_mfe_regressions import CURRENT_NUMERIC, CURRENT_PREDICATES, PARTITIONS, assert_historical_native
"""Current radius controls: exact frozen physics, independently checked finance roundoff."""

from tests.models.current_mfe_regressions import WI061_PARAMETERS, WI061_MAPPED_PARAMETERS, WI061_CHANNELS, WI062_CHANNELS, WI063_CHANNELS

import json
import math
import sys
from collections.abc import Mapping
from pathlib import Path
from tests.study.structure_ledger import renamed, renamed_keys


ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "exploration/stellarator_e2e/studies")]
import oracle_entry as oracle  # noqa: E402 — runtime import path established above
import study_route as route  # noqa: E402 — runtime import path established above

from tests.study.financial_channels import FINANCIAL_CHANNELS
from tests.models.current_mfe_regressions import (WI040_CHANNELS, WI040_CHANGED_ECONOMICS, LIVE_CONDUCTOR_CHANNELS, WI060_CHANNELS, WI059_CHANNELS, WI059_REPLAY, wi059_native_additions)

from scripts.study import common, verify  # noqa: E402 — runtime import path established above


def check_controls(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    frozen_dir = ROOT / "work/active/WI-051_mfe-model-owned-major-radius/prototype"
    frozen = json.loads((frozen_dir / "frozen-results.json").read_text())
    expectations = json.loads((frozen_dir / "expectations.json").read_text())
    # WI-058 (2026-09-14): the winding length follows the coil bore; the frozen R14 row was produced with
    # the R-form (c_coil = k_coil * R). At a = 1.3 the bore ratio is 1.0, so binding the reference
    # circumference to k_coil * R reproduces the R-form length exactly and the frozen row stays the exact
    # expectation (tests.models.current_mfe_regressions.K_COIL_RETIRED; the bore response is tested in
    # tests/models/test_winding_length_bore.py).
    from tests.models.current_mfe_regressions import K_COIL_RETIRED
    proposals = [WI059_REPLAY, WI059_REPLAY | {route.P + "plasma__R": 14.0, route.P + "magnet__coil__c_coil_ref": K_COIL_RETIRED * 14.0}]
    cases, db = route.run_points("radius-controls", proposals, out / "_work")
    assert len(cases) == 2 and all(c.state == "completed" for c in cases)
    comparisons = {}
    for proposal, name, old_name in zip(proposals, ["baseline", "R14"], ["baseline", "tied_R14"]):
        case = next(c for c in cases if dict(c.inputs) == proposal)
        expected = frozen["cases"][old_name]["native"]
        # WI-057 (2026-09-13): the frozen WI-051 expectations under the new channel names.
        frozen_outputs = renamed_keys(expected["outputs"])
        channels=oracle.evaluate(proposal)
        partition=PARTITIONS['fixture_partitions']['radius-'+old_name]
        changed=set(partition['changed_current_equation_channels'])
        additions=set(partition['added_channels'])
        assert set(frozen_outputs)==set(partition['unaffected_exact_channels']) | changed
        expected_outputs=dict(frozen_outputs)
        expected_outputs.update({k:channels[k] for k in changed | additions})
        assert set(case.outputs)==set(expected_outputs)==CURRENT_NUMERIC
        for key,value in expected_outputs.items():
            if key in changed | additions | FINANCIAL_CHANNELS:
                assert math.isclose(case.outputs[key],value,rel_tol=1e-9,abs_tol=0.0),(name,key,case.outputs[key],value)
            else:
                assert case.outputs[key]==value,(name,key,case.outputs[key],value)
        assert set(channels)==CURRENT_NUMERIC
        rows = {}
        for key, value in channels.items():
            assert math.isclose(value, case.outputs[key], rel_tol=1e-9, abs_tol=1e-9), (
                name,
                key,
                value,
                case.outputs[key],
            )
            deviation = common.relative_deviation(value, case.outputs[key])
            assert deviation < verify.TOLERANCE, (name, key, deviation)
            rows[key] = {
                "relative_deviation": deviation,
                "oracle": value,
                "native": case.outputs[key],
                "frozen": frozen_outputs.get(key),
                "expected_current": expected_outputs[key],
            }
        comparisons[name] = {
            "inputs": dict(case.inputs),
            "outputs": dict(case.outputs),
            "verdicts": route.short_verdicts(case),
            "oracle_channels": rows,
        }
        assert set(case.verdicts) == CURRENT_PREDICATES
    ratios = {}
    for suffix, expected in expectations["ratios"].items():
        key = renamed(route.P + suffix)  # WI-057
        actual = comparisons["R14"]["outputs"][key] / comparisons["baseline"]["outputs"][key]
        assert math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9), key
        ratios[key] = {"expected": expected, "actual": actual}
    identity = route.write_identity_document(route.PACKAGE_DIR, out / "package_identity.json")
    summary = verify.build_summary(
        route.PACKAGE_DIR, route.MANIFEST_PATH, identity, [db], 2, None, []
    )
    assert {row["constraint_id"] for row in summary["constraints_rederived"]} == CURRENT_PREDICATES
    assert summary["worst_channel_rel_dev"] < 1e-9
    for filename, data in [
        ("controls.json", comparisons),
        ("ratios.json", ratios),
        ("verification_summary.json", summary),
    ]:
        (out / filename).write_text(
            json.dumps(
                data, indent=2, default=lambda x: dict(x) if isinstance(x, Mapping) else str(x)
            )
            + "\n"
        )
    print(
        json.dumps(
            {
                "native_channels": len(case.outputs),
                "oracle_channels": len(channels),
                "authored_verdicts": len(case.verdicts),
                "worst_rel_dev": summary["worst_channel_rel_dev"],
            },
            indent=2,
        )
    )
    return comparisons


if __name__ == "__main__":
    check_controls(sys.argv[1])
