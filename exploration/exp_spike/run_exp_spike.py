"""exp() mini-spike execution harness.

Runs the generated exp_toy pipeline through the teax executor at 3 input
points (plus the design point) and asserts every output channel against an
independent hand computation using math.exp / math.log directly.

The two out-of-envelope calc bodies (BoschHaleReactivity, GainDoublings)
were hand-written by the AI pass — that is the claim under test. The
in-envelope control (ExpControl, e spelled as a literal ** x) was
auto-implemented by codegen.

Run:  ../pipeline_spike/.venv-exec/bin/python run_exp_spike.py
      (venv has teax-simkit editable; same executor as WI-013/WI-015)
"""

import json
import math
import sys
from pathlib import Path

SPIKE = Path(__file__).parent

# Make the generated package importable as `exp_toy_tea`
pkg_dir = SPIKE / "pkg"
pkg_dir.mkdir(exist_ok=True)
link = pkg_dir / "exp_toy_tea"
if not link.exists():
    link.symlink_to(SPIKE / "generated")
sys.path.insert(0, str(pkg_dir))

from simkit.core.pipeline import execute_pipeline  # noqa: E402
from simkit.io.output_router import (  # noqa: E402
    WriteHandler,
    create_output_router_with_json_schemas,
)

from exp_toy_tea import ExpToyParams, create_exp_toy_tea_registry  # noqa: E402

REL_TOL = 1e-12  # float-representation tolerance; same expression shape both sides

P = "exp_toy__exp_plant__"
CH_SIGMA = f"{P}reactivity_calc__sigma_v"
CH_DOUB = f"{P}doublings_calc__doublings"
CH_ECTRL = f"{P}exp_control_calc__e_to_x"

INPUTS_JSON = SPIKE / "generated/inputs/exp_toy_params.json"

# --- Input points -----------------------------------------------------------
# Point 1 is the SysML design point (exp_plant bindings, exp_toy.sysml:100).
POINTS = [
    dict(name="design (T=10 keV)", t_kev=10.0, c_coeff=6.4e-14, b_gamow=19.98,
         gain=100.0, ctrl_x=10.0),
    dict(name="hot (T=20 keV)", t_kev=20.0, c_coeff=6.4e-14, b_gamow=19.98,
         gain=350.0, ctrl_x=2.5),
    dict(name="cold (T=5 keV)", t_kev=5.0, c_coeff=1.1e-13, b_gamow=19.98,
         gain=30.0, ctrl_x=-1.0),
]


def oracle(pt: dict) -> dict:
    """Independent hand computation with math.exp / math.log directly."""
    t, c, b = pt["t_kev"], pt["c_coeff"], pt["b_gamow"]
    return {
        CH_SIGMA: c * math.exp(-b / t ** (1.0 / 3.0)) / t ** (2.0 / 3.0),
        CH_DOUB: math.log(pt["gain"]) / math.log(2.0),
        CH_ECTRL: 2.718281828459045 ** pt["ctrl_x"],
    }


def run_point(pt: dict, router) -> dict:
    INPUTS_JSON.write_text(json.dumps({
        f"{P}reactivity_calc__t_kev": pt["t_kev"],
        f"{P}reactivity_calc__c_coeff": pt["c_coeff"],
        f"{P}reactivity_calc__b_gamow": pt["b_gamow"],
        f"{P}doublings_calc__target_gain": pt["gain"],
        f"{P}exp_control_calc__exponent_arg": pt["ctrl_x"],
    }, indent=2))
    result = execute_pipeline(
        SPIKE / "generated/pipelines/exp_toy.yaml",
        output_dir=SPIKE / "outputs",
        registry=create_exp_toy_tea_registry(),
        output_router=router,
        custom_schema_types=[ExpToyParams],
    )
    return result.outputs


def main() -> None:
    # Same two executor gaps as WI-013 (run_pipeline.py): the ExitPoint
    # declares primitive types the default router can't write.
    router = create_output_router_with_json_schemas(
        ["RootModel[float]", "ExpToyParams"]
    )
    router.register_handler(
        "float",
        WriteHandler(
            fn=lambda value, path: Path(path).write_text(json.dumps(value)),
            extension=".json",
        ),
    )

    failures = 0
    total = 0
    hdr = f"{'point':20s} {'channel (leaf)':28s} {'executed':>24s} {'oracle':>24s} {'rel dev':>10s}"
    print(hdr)
    print("-" * len(hdr))
    for pt in POINTS:
        outputs = run_point(pt, router)
        expected = oracle(pt)
        for chan, exp_val in expected.items():
            val = outputs[chan]
            actual = float(val.root) if hasattr(val, "root") else float(val)
            denom = max(abs(actual), abs(exp_val), 1e-300)
            dev = abs(actual - exp_val) / denom
            ok = dev <= REL_TOL
            leaf = "__".join(chan.split("__")[-2:])
            print(f"{pt['name']:20s} {leaf:28s} {actual:24.12e} {exp_val:24.12e} {dev:10.1e}  {'OK' if ok else 'FAIL'}")
            total += 1
            if not ok:
                failures += 1

    print()
    if failures:
        raise SystemExit(f"{failures}/{total} assertion(s) FAILED")
    print(f"ALL {total} ASSERTIONS PASSED (rel tol {REL_TOL})")


if __name__ == "__main__":
    main()
