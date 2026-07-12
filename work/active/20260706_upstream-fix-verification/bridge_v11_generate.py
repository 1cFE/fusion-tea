"""LOCAL BRIDGE — NOT A FIX. Emits the IFE package by hand-filling the 10 V11 offenders.

The upstream-findings epic left 10 cross-part bindings unwired (sysml-codegen
BACKLOG P1 "fusion-tea whole-plant cross-part wiring"). The V11 params-coverage
check therefore aborts whole-plant generation: the 10 offender entry points exist
in the derived parameter groups but are valueless, so the input JSONs never mint
their keys.

This script bridges that gap FOR VERIFICATION ONLY. It fills the 10 valueless
defaults with the model's own cross-part literal values (read from
hif_driver.sysml / hif_plant.sysml — the values the missing wiring would fetch),
then runs the exact same emission steps as `sysml-codegen generate`. Everything
downstream of the known gap (naming, stencils, wiring, registry, YAML, anchors)
is exercised unmodified.

Anything proven with this bridge is labeled BRIDGED in the verification report,
never FIXED. When the upstream P1 lands, this script is dead — delete it.

Run:  cd ~/1cfe/sysml-codegen && set -a && source ~/1cfe/agentic-mbse/.env && set +a && \
      uv run python ~/1cfe/fusion-tea/work/active/20260706_upstream-fix-verification/bridge_v11_generate.py
"""

import sys
from pathlib import Path

WORK = Path(__file__).parent
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else WORK.parent.parent.parent / "exploration" / "ife_e2e" / "generated_bridged"
SNAPSHOT = Path(sys.argv[2]) if len(sys.argv) > 2 else WORK / "snapshots" / "ife_workaround_applied.snapshot.json"

# The 10 V11 offenders and the model's own values for them.
# Sources: hif_driver.sysml:81-84 (efficiency/energy/lifetime_shots),
# hif_plant.sysml:48,63-64 (cost_per_target, blanket_energy_multiple, yield_cost_constant).
# recirc_calc.eta/blanket_multiplier bind to driver.efficiency / chamber.blanket_energy_multiple
# (ife_plant.sysml calc-usage bindings).
BRIDGE_VALUES = {
    "hif_plant_pkg__hif_plant__driver__meier_cost__driver_efficiency": 0.35,
    "hif_driver__hif_driver_instance__meier_cost__driver_efficiency": 0.35,
    "hif_plant_pkg__hif_plant__recirc_calc__eta": 0.35,
    "hif_plant_pkg__hif_plant__recirc_calc__blanket_multiplier": 1.15,
    "hif_plant_pkg__hif_plant__lcoe_calc__blanket_energy_multiple": 1.15,
    "hif_plant_pkg__hif_plant__lcoe_calc__driver_efficiency": 0.35,
    "hif_plant_pkg__hif_plant__lcoe_calc__driver_energy": 14.286e6,
    "hif_plant_pkg__hif_plant__lcoe_calc__driver_lifetime_shots": 6.0e9,
    "hif_plant_pkg__hif_plant__lcoe_calc__target_cost_constant": 10.0,
    "hif_plant_pkg__hif_plant__lcoe_calc__yield_cost_constant": 5.0e6,
}


def main() -> None:
    from sysml_codegen.cli import (
        GenerationConfig,
        _check_duplicate_output_paths,
        _clear_output_directory,
        _generate_backlog,
        _generate_entry_points,
        _generate_modules,
        _generate_pipeline,
        _generate_primitives,
        _generate_registry,
        _generate_schemas,
        _generate_stencils,
        _generate_tests,
        _get_template_env,
        _reconcile_params_coverage,
        _setup_output_directories,
    )
    from sysml_codegen.orchestration.snapshot_context import (
        build_pipeline_context_from_snapshot,
    )
    from sysml_codegen.resolution.graph_builder import collect_uncovered_params

    ctx = build_pipeline_context_from_snapshot(SNAPSHOT)
    graph = ctx.computation_graph

    before = collect_uncovered_params(graph)
    print(f"[bridge] V11 offenders before bridge: {len(before)}")

    # THE BRIDGE: fill the valueless defaults for exactly the offender keys.
    bridged = []
    for group in graph.entry_point_groups:
        for param in group.parameters:
            if param.qualified_name in BRIDGE_VALUES and param.default_value is None:
                param.default_value = BRIDGE_VALUES[param.qualified_name]
                bridged.append(f"{group.name}.{param.qualified_name}")
    print(f"[bridge] filled {len(bridged)} valueless entry-point defaults:")
    for b in bridged:
        print(f"  BRIDGED {b}")
    if len(bridged) != 10:
        sys.exit(f"[bridge] expected to bridge exactly 10, bridged {len(bridged)} — ABORT")

    after = collect_uncovered_params(graph)
    print(f"[bridge] V11 offenders after bridge: {len(after)}")
    if after:
        sys.exit(f"[bridge] still uncovered: {after} — ABORT")

    # Standard emission path, identical to run_codegen() steps 1.5-8.
    config = GenerationConfig(
        output_path=OUTPUT,
        from_snapshot=SNAPSHOT,
        package_name="ife_tea",
        pipeline_name="ife_hif",
        overwrite=True,
    )
    _check_duplicate_output_paths(graph.modules)
    _reconcile_params_coverage(graph)  # must pass now
    _clear_output_directory(config)
    _setup_output_directories(config)
    _generate_primitives(config)
    env = _get_template_env()
    _generate_schemas(ctx, config, env)
    _generate_modules(ctx, config, env)
    _generate_stencils(ctx, config, env)
    _generate_pipeline(ctx, config, env)
    _generate_registry(ctx, config, env)
    _generate_entry_points(ctx, config, env)
    _generate_backlog(ctx, config)
    _generate_tests(ctx, config, env)
    print(f"[bridge] package emitted to {OUTPUT}")


if __name__ == "__main__":
    main()
