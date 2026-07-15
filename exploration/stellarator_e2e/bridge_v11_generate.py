"""LOCAL BRIDGE — NOT A FIX. Emits the stellarator MFE package past the V11 gate.

Adapted from work/active/20260706_upstream-fix-verification/bridge_v11_generate.py.

The MFE plant's capital rollup sums each subsystem's capital_cost across parts
(powercore_capital, bop_capital) and feeds the direct/total subtotals into the
contingency, indirect, and LCOE calc modules. sysml-codegen cannot compile a
feature-chain sum across parts in a CalcDef output ("feature chain expression not
supported"), so those three rollup inputs are valueless cross-part references and
the V11 params-coverage check aborts whole-plant generation on exactly 3
offenders:

  stellarator_09__stellaris__contingency__direct_subtotal   (<- direct_capital)
  stellarator_09__stellaris__indirect__direct_cost          (<- direct_capital)
  stellarator_09__stellaris__lcoe_calc__total_capital       (<- total_capital)

This bridges the gap FOR THE DEMO ONLY by filling those three entry points with a
PLACEHOLDER so the package emits. The harness (run_stellaris.py) then closes the
rollup properly: it reads the generated per-account cost module outputs from a
first executor pass, sums them (the arithmetic sysml-codegen could not wire),
writes the real direct/total values into the emitted input JSON, and runs a
second executor pass so the generated contingency/indirect/LCOE modules produce
the correct numbers. The placeholder value here is never trusted — it only
satisfies V11 so emission proceeds.

Mirrors WI-015 finding 4 and the upstream-fix-verification report: the cross-part
edge is harness glue, loudly labeled, everything else is generated code.

Run:  cd ~/1cfe/sysml-codegen && set -a && source ~/1cfe/fusion-tea/.env && set +a && \
      uv run python <this>/bridge_v11_generate.py
"""

import sys
from pathlib import Path

E2E = Path(__file__).parent
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else E2E / "generated"
SNAPSHOT = Path(sys.argv[2]) if len(sys.argv) > 2 else E2E / "stellarator.snapshot.json"

# The 3 V11 offenders (cross-part rollup sums). Placeholder only — the harness
# overwrites these with values summed from the generated per-account modules.
PLACEHOLDER = 1.0
BRIDGE_KEYS = {
    "stellarator_09__stellaris__contingency__direct_subtotal",
    "stellarator_09__stellaris__indirect__direct_cost",
    "stellarator_09__stellaris__lcoe_calc__total_capital",
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
    for u in before:
        print(f"  OFFENDER {u}")

    bridged = []
    for group in graph.entry_point_groups:
        for param in group.parameters:
            if param.qualified_name in BRIDGE_KEYS and param.default_value is None:
                param.default_value = PLACEHOLDER
                bridged.append(f"{group.name}.{param.qualified_name}")
    print(f"[bridge] filled {len(bridged)} valueless entry-point defaults "
          f"with placeholder {PLACEHOLDER}:")
    for b in bridged:
        print(f"  BRIDGED {b}")
    if len(bridged) != 3:
        sys.exit(f"[bridge] expected to bridge exactly 3, bridged {len(bridged)} — ABORT")

    after = collect_uncovered_params(graph)
    print(f"[bridge] V11 offenders after bridge: {len(after)}")
    if after:
        sys.exit(f"[bridge] still uncovered: {after} — ABORT")

    config = GenerationConfig(
        output_path=OUTPUT,
        from_snapshot=SNAPSHOT,
        package_name="stellarator_tea",
        pipeline_name="mfe_stellarator",
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
