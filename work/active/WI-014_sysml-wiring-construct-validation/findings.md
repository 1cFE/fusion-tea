# WI-014 Findings: SysML Wiring Construct Validation

**Date**: 2026-07-04
**Status**: Partial — static validation complete, live validation blocked by expired syside license

## Blocker (affects steps 3-5)

The syside license expired and cannot be refreshed from this machine:

- The underlying license (key `76018C-368D9B-...` in `.env` and the system keyring) expired **2026-05-25**; the cached machine file (`~/.local/share/syside/syside-license.lic`) expired **2026-06-01**.
- `uv run syside-license check` (the `syside-license` package was installed into the venv for this) reaches the vendor server, which answers "License expired" — the subscription itself lapsed, so no local action can renew it. A new key from Sensmetry (syside.support@sensmetry.com) is required.
- This blocks `syside check`, the syside Python evaluation API, **and** sysml-codegen extraction (its `SysideAdapter` imports syside). Upgrading syside 0.8.6 → 0.10.2 does not help (same license file); the venv was reverted to the locked 0.8.6.

Everything below is established from the existing corpus and from sysml-codegen's **committed** fixtures, baselines, and snapshots — no live syside run was possible. The toy model is ready to run the moment the license is renewed.

## Toy model (ready, unvalidated live)

- `exploration/construct_validation/toy_library.sysml` — `'Panel Area'` and `'Panel Cost'` calc defs, `'Cost Within Budget'` constraint def.
- `exploration/construct_validation/toy_plant.sysml` — `part def 'Toy Plant'` with the chained calc usages, a derived attribute reading a calc result, a part-level `assert constraint` fed by a calc output, and a `part demo_plant : 'Toy Plant';` instance. Expected numbers are in the doc comment (area 12.0, cost 3000.0, constraint true).

## Construct (a): usage-level calc chaining (`in x = someCalc.result`)

| Depth | Verdict | Evidence |
|---|---|---|
| Parse | **pass** (by corpus proxy) | Identical syntax already parses in this repo: `models/designs/hif_ife/hif_plant.sysml:199,214` chains calc results inside a part usage. sysml-codegen fixtures do the same (`tests/fixtures/chain_spike_model/design.sysml:19-26`, `catf_mfe .../radial_build.sysml:104` `in a = minor_calc.a`). Toy files themselves not yet checked (license). |
| Evaluate | **blocked** | Needs the syside Compiler API. |
| Extract | **pass** | Committed baseline `sysml-codegen/tests/fixtures/baseline_outputs/chain_spike/computation_graph.json` wires `producer_channel: ...area_calc__area` into the downstream calc's input — the chain survives into the graph and is regression-tested (`tests/conformance/test_baselines.py`). |

**Inside a part def specifically** (the WI-010 shape): proven by the committed extraction snapshot `sysml-codegen/tests/fixtures/unresolvable_attr_probe/extraction_snapshot.json` — `my_calc` is declared inside `part def 'Design Derived'` (design.sysml:20) and extraction projects it onto the part *usage* instance (`instance_name: ...__design_derived_instance__my_calc`, `parent_part_path: design_derived_instance`, `owning_part_def_qn` recorded). Consequence for WI-010: **the plant part def must be instantiated by a part usage** for codegen to emit modules; a def with no usage produces nothing.

**Derived attribute reading a calc result** (`attribute total_cost : Real = cost_calc.cost`): supported — same probe's pattern D3 (`my_calc.result * base_rate`) and catf_mfe's `attribute volume : Real = volume_calc.volume` (radial_build.sysml:109-110), with committed catf_mfe baseline.

## Construct (b): part-level `assert constraint` on calc outputs

| Depth | Verdict | Evidence |
|---|---|---|
| Parse | **pass** (by corpus proxy) | `models/designs/generic_ife/ife_plant.sysml:155` has a part-def-level `assert constraint viability : 'Viability Threshold' { in eta = driver.efficiency; ... }` and that model passed Level 1 historically. Binding an `in` to a calc output instead of an attribute is the one untested delta — same expression grammar as calc-usage bindings (construct a), so low parse risk, but unconfirmed. |
| Evaluate | **blocked** | Unknown whether syside evaluates asserted constraints to a boolean; needs the license. |
| Extract | **FAIL — constraints never enter the graph** | `sysml-codegen/src/sysml_codegen/extraction/extractor.py:106-107`: `# Extract constraints (stub for now)` / `constraints = []`. A full `constraint_extractor.py` exists (`extract_all_constraints` walks `ConstraintUsage` elements and classifies part_def/part_usage owners, constraint_extractor.py:50,162-172) but **has zero callers** anywhere in src/ or tests/. No committed baseline `computation_graph.json` contains a constraint. This matches the epic's note that constraint predicate emission is an open codegen TODO (Phase 6). |

Even if wired in, `constraint_extractor.py` would not capture the WI-010 shape correctly today: it reads the expression off the constraint *usage* (`_extract_constraint_expression`, line 96) — for a usage typed by a constraint def, the predicate lives in the def and the usage holds only `in` bindings, and referenced variables are recovered by regex over the expression text (line 120), not by resolving bindings to calc output channels.

## Verdict for the WI-010 plant idiom

**Usable as sketched, with two riders:**

1. **The behavior wiring works end to end** (parse + extract, evaluation pending license): chained calcs in a part def, derived attributes reading calc results, all projected per part-usage instance. WI-010 must give the plant def a concrete part usage (the design instance already planned) — codegen keys modules off usages.
2. **`assert constraint` is model-documentation only for now**: it should parse and belongs in the model (it is the source of truth for viability), but it will not survive codegen extraction. WI-010/WI-012 must not rely on generated code enforcing viability — the sweep classifier has to apply the constraint (e.g., ηG > 10) in analysis code, exactly as the epic's Item 3 already plans. File the codegen gap against sysml-codegen: wire `extract_all_constraints` into `SysMLDataExtractor` (extractor.py:106) and resolve constraint-usage `in` bindings the same way calc-usage bindings are resolved (usage_extractor.py:369ff).

No architectural decision (AD) is forced: the idiom stands; the constraint gap is a tooling TODO, not a modeling choice.

## Remaining once license is renewed

1. `uv run syside check exploration/construct_validation/*.sysml` — confirm Level 1 on the toy itself.
2. Evaluate `demo_plant.total_cost` via `syside.Compiler` — expect 3000.0; check whether the asserted constraint evaluates.
3. Run `sysml-codegen generate` over the toy — confirm the chain appears in the graph and the constraint (predictably) does not.
