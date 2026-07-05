# WI-014 Findings: SysML Wiring Construct Validation

**Date**: 2026-07-04 (live checks 2026-07-05)
**Status**: Complete — static validation 2026-07-04; the three deferred live checks were run 2026-07-05 after the syside license was renewed (see "Live checks — license restored" below)

## Blocker (affects steps 3-5)

The syside license expired and cannot be refreshed from this machine:

- The underlying license (key `76018C-368D9B-...` in `.env` and the system keyring) expired **2026-05-25**; the cached machine file (`~/.local/share/syside/syside-license.lic`) expired **2026-06-01**.
- `uv run syside-license check` (the `syside-license` package was installed into the venv for this) reaches the vendor server, which answers "License expired" — the subscription itself lapsed, so no local action can renew it. A new key from Sensmetry (syside.support@sensmetry.com) is required.
- This blocks `syside check`, the syside Python evaluation API, **and** sysml-codegen extraction (its `SysideAdapter` imports syside). Upgrading syside 0.8.6 → 0.10.2 does not help (same license file); the venv was reverted to the locked 0.8.6.

*(2026-07-05: license renewed; the static findings below were re-verified live and the tables updated with live verdicts. See "Live checks — license restored".)*

## Toy model (live-validated 2026-07-05)

- `exploration/construct_validation/toy_library.sysml` — `'Panel Area'` and `'Panel Cost'` calc defs, `'Cost Within Budget'` constraint def.
- `exploration/construct_validation/toy_plant.sysml` — `part def 'Toy Plant'` with the chained calc usages, a derived attribute reading a calc result, a part-level `assert constraint` fed by a calc output, and a `part demo_plant : 'Toy Plant';` instance. Expected numbers are in the doc comment (area 12.0, cost 3000.0, constraint true).

## Construct (a): usage-level calc chaining (`in x = someCalc.result`)

| Depth | Verdict | Evidence |
|---|---|---|
| Parse | **pass (live)** | `uv run python -m syside check` on both toy files: "Checks passed!" (2026-07-05). Corpus proxies (`models/designs/hif_ife/hif_plant.sysml:199,214`, sysml-codegen `tests/fixtures/chain_spike_model/design.sysml:19-26`) confirmed. |
| Evaluate | **pass (live)** | `demo_plant.total_cost` = **3000.0** via `syside.Compiler.evaluate_feature` — the chain evaluates end to end. Required one toy fix first: self-named bindings (`in length = length;`) infinite-recurse at evaluation (see live-checks section). |
| Extract | **pass (live)** | `sysml-codegen generate` over the toy wires `cost_calc`'s `area` input to `toy_plant__demo_plant__area_calc__area` in `pipeline.yaml` — the chain survives into the graph. Required one toy fix first: outputs must be `out attribute`, not `return` (see live-checks section). Also matches committed baseline `chain_spike/computation_graph.json`. |

**Inside a part def specifically** (the WI-010 shape): proven by the committed extraction snapshot `sysml-codegen/tests/fixtures/unresolvable_attr_probe/extraction_snapshot.json` — `my_calc` is declared inside `part def 'Design Derived'` (design.sysml:20) and extraction projects it onto the part *usage* instance (`instance_name: ...__design_derived_instance__my_calc`, `parent_part_path: design_derived_instance`, `owning_part_def_qn` recorded). Consequence for WI-010: **the plant part def must be instantiated by a part usage** for codegen to emit modules; a def with no usage produces nothing.

**Derived attribute reading a calc result** (`attribute total_cost : Real = cost_calc.cost`): parses and **evaluates live** (3000.0). But in the toy's live extraction it does **not** survive: codegen extracts it as a computed attribute, then fails to alias it (`WARNING: EXPOSE_PURE total_cost: could not identify instance/output from refs ['cost', 'cost_calc']`) and drops it from all generated artifacts. Nothing is lost computationally — the underlying channel `cost_calc__cost` is still a graph output — but do not rely on the derived attribute name appearing in generated code. (catf_mfe's `volume = volume_calc.volume` baseline sits in a different scoping shape; the def+usage toy shape is what failed.)

## Construct (b): part-level `assert constraint` on calc outputs

| Depth | Verdict | Evidence |
|---|---|---|
| Parse | **pass (live)** | The toy's `assert constraint affordable : 'Cost Within Budget' { in cost = cost_calc.cost; ... }` — an `in` bound to a calc output — passes `syside check` (2026-07-05). |
| Evaluate | **pass (live), with a mechanism nuance** | The predicate evaluates to **True** (3000.0 <= 5000.0). But `Compiler.evaluate_feature(assert_usage, scope)` does *not* return the boolean — it returns the usage element itself. To get the boolean you evaluate the constraint *def*'s predicate expression (the `OperatorExpression` for `cost <= budget`) with `scope=` the assert usage: `compiler.evaluate(predicate_expr, scope=affordable_usage)` → `True`. Analysis code that wants constraint verdicts must do this two-step, not a single feature evaluation. |
| Extract | **FAIL (live-confirmed) — constraints never enter the graph** | Live run 2026-07-05: `sysml-codegen generate` completes without error, but `affordable` and `plant_budget` are **silently absent** from every generated artifact (`pipeline.yaml`, params JSON, modules, tests; the only "constraint" match in output is boilerplate text in `IMPLEMENTATION_BACKLOG.md`). No crash, no warning — the constraint just vanishes. Root cause as predicted statically: `sysml-codegen/src/sysml_codegen/extraction/extractor.py:106-107` stubs `constraints = []`; `constraint_extractor.py` has zero callers. Matches the epic's open Phase 6 TODO. |

Even if wired in, `constraint_extractor.py` would not capture the WI-010 shape correctly today: it reads the expression off the constraint *usage* (`_extract_constraint_expression`, line 96) — for a usage typed by a constraint def, the predicate lives in the def and the usage holds only `in` bindings, and referenced variables are recovered by regex over the expression text (line 120), not by resolving bindings to calc output channels.

## Verdict for the WI-010 plant idiom

**Usable as sketched, with two riders:**

1. **The behavior wiring works end to end** (parse + evaluate + extract, all live-confirmed 2026-07-05): chained calcs in a part def, derived attributes reading calc results (evaluate; the *name* is dropped at extraction — see construct a), all projected per part-usage instance. WI-010 must give the plant def a concrete part usage (the design instance already planned) — codegen keys modules off usages.
2. **`assert constraint` is model-documentation only for now**: it should parse and belongs in the model (it is the source of truth for viability), but it will not survive codegen extraction. WI-010/WI-012 must not rely on generated code enforcing viability — the sweep classifier has to apply the constraint (e.g., ηG > 10) in analysis code, exactly as the epic's Item 3 already plans. File the codegen gap against sysml-codegen: wire `extract_all_constraints` into `SysMLDataExtractor` (extractor.py:106) and resolve constraint-usage `in` bindings the same way calc-usage bindings are resolved (usage_extractor.py:369ff).

No architectural decision (AD) is forced: the idiom stands; the constraint gap is a tooling TODO, not a modeling choice.

## Live checks — license restored (2026-07-05)

The syside license was renewed; all three deferred checks were executed. Note the CLI binary is not installed — parse checks run as `uv run python -m syside check <files>`.

### Check 1: `syside check` on the toy — PASS

"Checks passed!" on `toy_library.sysml` + `toy_plant.sysml`. This held both before and after the two syntax fixes below (both original constructs already parsed; the failures were downstream).

### Check 2: evaluate `demo_plant.total_cost` — PASS (3000.0), after one toy fix

- **As originally written, evaluation failed**: `evaluate_feature(total_cost, demo_plant)` returned `None` with `error (expression-error): Evaluating expression took too long...` at the calc bindings.
- **Root cause — self-named bindings**: `in length = length;` (calc parameter shadowing a same-named part attribute) parses fine, but at evaluation syside resolves the right-hand `length` to the calc usage's *own* `in` parameter, giving infinite recursion. Raising `Compiler.max_steps` does not help — it is genuine recursion, not a tight budget.
- **Fix (applied to the toy)**: rename the part attributes so bindings are unambiguous (`plant_length`, `plant_width`, `plant_unit_cost`, `plant_budget`; bindings now `in length = plant_length;` etc.). After the rename: `total_cost` = **3000.0**, matching the doc-comment expectation, with clean diagnostics.
- **Asserted constraint**: evaluates to **True**, but only via the two-step described in the construct (b) table — evaluate the def's predicate `OperatorExpression` with `scope=` the assert usage. Evaluating the assert usage as a feature returns the usage element, not a boolean.
- API note for future scripts: `element.qualified_name` returns a `QualifiedName` object, not a `str` — `str()` it before dict keying/comparison.

### Check 3: `sysml-codegen generate` over the toy — PASS for the chain, constraint absent as predicted, after one toy fix

- **As originally written, generation crashed**: `jinja2 UndefinedError: list object has no element 0` in `teax_module.py.jinja2:118` — each toy calc def used `return area : Real = ...`, and codegen only recognizes `out attribute` parameters as module outputs, so both modules had zero outputs. syside parses and evaluates both forms; codegen requires `out attribute`.
- **Fix (applied to the toy)**: `return x : Real = expr;` → `out attribute x : Real = expr;` in both calc defs. syside check and evaluation still pass (3000.0 / True) after the change.
- **Chain in the graph — confirmed**: `pipeline.yaml` wires `cost_calc`'s `area` input to `toy_plant__demo_plant__area_calc__area.root`; entry points (`plant_length` 4.0, `plant_width` 3.0, `plant_unit_cost` 250.0) land in `toy_plant_params.json`; modules are keyed off the `demo_plant` part **usage** (`toy_plant__demo_plant__area_calc`), confirming the def-needs-a-usage rider.
- **Constraint out of the graph — confirmed, and it is silent**: generation completes with no error or constraint-specific warning; `affordable` and `plant_budget` appear in no generated artifact. Exactly the expected Phase 6 stub behavior (`extractor.py:106-107`).
- **New nuance — derived attribute dropped**: `attribute total_cost : Real = cost_calc.cost` triggers `WARNING: EXPOSE_PURE total_cost: could not identify instance/output from refs ['cost', 'cost_calc']` and `total_cost` appears nowhere in the output. The value is still reachable as channel `cost_calc__cost`, but the alias is lost. Benign for WI-010 unless generated code is expected to expose the derived-attribute *name*.
- Benign warnings: `Registry unresolved: ...|length source_path='toy_plant::'Toy Plant'::plant_length'` (and width/unit_cost) — these fall through to entry-point parameters with correct literals, which is the right outcome.

### Syntax deltas for WI-010 (the reason the toy needed fixing)

1. **Never self-name calc bindings inside a part def.** `in x = x;` parses but infinite-recurses at syside evaluation. Give part attributes distinct names from the calc parameters they feed. (sysml-codegen's own chain_spike fixture uses self-named bindings and extracts fine — the failure is syside-evaluation-only, so it hides until someone evaluates.)
2. **Use `out attribute`, not `return`, for calc outputs.** `return` is legal SysML and evaluates in syside, but sysml-codegen sees zero outputs and crashes at template rendering.
