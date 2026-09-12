"""Execute current proposals and compare every declared oracle channel to frozen controls."""

import json
import math
import sys
from collections.abc import Mapping
from pathlib import Path

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT), str(ROOT / "exploration/stellarator_e2e/studies")]
import oracle_entry as oracle  # noqa: E402 — runtime import path established above
import study_route as route  # noqa: E402 — runtime import path established above

from scripts.study import common, verify  # noqa: E402 — runtime import path established above


def check_controls(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    frozen_dir = ROOT / "work/active/WI-051_mfe-model-owned-major-radius/prototype"
    frozen = json.loads((frozen_dir / "frozen-results.json").read_text())
    expectations = json.loads((frozen_dir / "expectations.json").read_text())
    proposals = [{}, {route.P + "R": 14.0}]
    cases, db = route.run_points("radius-controls", proposals, out / "_work")
    assert len(cases) == 2 and all(c.state == "completed" for c in cases)
    comparisons = {}
    for proposal, name, old_name in zip(proposals, ["baseline", "R14"], ["baseline", "tied_R14"]):
        case = next(c for c in cases if dict(c.inputs) == proposal)
        expected = frozen["cases"][old_name]["native"]
        assert set(case.outputs) == set(expected["outputs"]) == set(expectations["channels"])
        for key, value in expected["outputs"].items():
            assert (
                case.outputs[key] == value
                if name == "baseline"
                else math.isclose(case.outputs[key], value, rel_tol=1e-9, abs_tol=1e-9)
            ), (name, key)
        channels = oracle.evaluate(proposal)
        assert set(channels) == set(oracle.ORACLE_OUTPUT_TO_CHANNEL.values())
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
                "frozen": expected["outputs"][key],
            }
        comparisons[name] = {
            "inputs": dict(case.inputs),
            "outputs": dict(case.outputs),
            "verdicts": route.short_verdicts(case),
            "oracle_channels": rows,
        }
        assert len(case.verdicts) == 18
    ratios = {}
    for suffix, expected in expectations["ratios"].items():
        key = route.P + suffix
        actual = comparisons["R14"]["outputs"][key] / comparisons["baseline"]["outputs"][key]
        assert math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9), key
        ratios[key] = {"expected": expected, "actual": actual}
    identity = route.write_identity_document(route.PACKAGE_DIR, out / "package_identity.json")
    summary = verify.build_summary(
        route.PACKAGE_DIR, route.MANIFEST_PATH, identity, [db], 2, None, []
    )
    assert len(summary["constraints_rederived"]) == 18
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
