# WI-015 Findings: IFE End-to-End Demonstration

**Date**: 2026-07-05
**Verdict: the chain closed.** The IFE/HIF SysML models ran live syside extraction → sysml-codegen generation → teax execution for the first time, and all three LCOE anchors reproduce **bit-exactly** (relative deviation 0.0; spec tolerance was 1e-6). This is the first live extraction since the license lapse and the first ever of these models.

Artifacts: `exploration/ife_e2e/` (staged models, generated package, harnesses, run outputs), `data/ife_sweep/` (sweep CSV + figures), `demo_report.md` (this dir). SV-023 registered, passing.

## Model fixes made (read this first)

Three trivially-safe edits to the canonical models were required to get through extraction. All verified with `uv run python -m syside check` (full file set — checks pass).

1. **Six `return x : Real = expr` → `out attribute x : Real = expr` conversions.** `ife_lcoe.sysml:122` (lcoe), `fusion_cycle.sysml:26` (f_recirc), `hif_economics.sysml:40,60,80,103` (gamma, reactor_cost_billions, total_capital_billions, coe_cents_kwh). Reason: codegen finding 1 below. Same trap independently recorded by WI-014's live checks (`work/learnings/RAW_LEARNINGS.md`, trap 2).
2. **One `attribute` → `out attribute` promotion**: `cost_billions` in 'Meier HIF Driver Cost' (`hif_economics.sysml:34`). It is consumed by hif_plant's Meier chain but was invisible as a channel. Also exercises multi-output generation (1 multi-output schema generated, works).
3. **Added `part hif_driver_instance : 'HIF Driver'`** (`hif_driver.sysml:100`), bound at the Osiris point. The WI-014 rider: codegen keys calc modules off part *usages*, and the only usage of 'HIF Driver' was the redefining `part :>> driver` inside hif_plant, which codegen misses (finding 2 below). Without it, the `meier_cost` calc template is dropped.

## Codegen findings (file in sysml-codegen)

1. **`return`-style calc outputs are invisible to extraction; generation crashes.** A `return x : Real = expr` parses in syside as a **ReferenceUsage** with direction Out, but `extraction/extractor.py:152-153` only inspects `AttributeUsage` members, so the calc def extracts with `output_attributes = []` and module generation dies at `templates/teax_module.py.jinja2:118` (`output_attributes[0]` on an empty list). Every proven fixture uses `out attribute`, so this had never been hit. Either handle ReferenceUsage/Return members or reject `return` with a clear diagnostic.
2. **Template expansion misses part usages that reference a subtype via redefinition.** `_build_part_usage_index` (`extraction/usage_extractor.py:160-167`) indexes each PartUsage under `next(iter(usage.types))` only. For `part :>> driver : 'HIF Driver'` (hif_plant.sysml:28), syside returns `types = ['IFE Driver', ..., 'HIF Driver']` — supertype first — so the usage is indexed under 'IFE Driver' and 'HIF Driver' appears uninstantiated; its template calc (`meier_cost`) is dropped with "no PartUsage instantiations". Index all types (or the most-specific declared type), not the first.
3. **Quoted SysML names leak raw into Python identifiers — generated package is not valid Python.** Calc defs named with quotes ('IFE LCOE') produce file names (`'ife lcoe'.py`), import paths (`from ife_tea.modules.ife_lcoe.'ife lcoe' import ...`), and class names (`class 'IFE LCOE'Input`) containing quotes and spaces. The registry's import lines *do* sanitize class names (`IFE_LCOEModule`), so the package is also internally inconsistent. Workaround: `exploration/ife_e2e/sanitize_names.py`, a deterministic post-processor (global textual replace + file renames + py_compile check). Fix: apply `sanitize_name` uniformly in module/stencil/schema template contexts.
4. **Cross-part references drop to unresolved entry points; no channel wiring and no literal pre-fill.** All lcoe_calc inputs bound to subsystem attributes (`driver.efficiency`, `chamber.blanket_energy_multiple`, `target_factory.cost_per_target`) and the calc-chain bindings (`driver.cost_per_joule = meier_cost.gamma`, `driver.driver_cost_billions` → meier_capital) come out "Registry unresolved" and become bare entry points: the generated input JSONs are mostly empty (even literals like `availability = 0.90` don't pre-fill), and the gamma → lcoe.driver_cost_constant edge is absent from the YAML. Harness closes the loop by feeding run-A outputs (gamma, cost_billions) into run C's inputs (`run_anchors.py`). This is the biggest functional gap for plant-idiom models — WI-010/WI-012 should expect it.
5. **Stencil/docstring expression reconstruction corrupts both literals and precedence.** Known WI-013 finding (literals render as `LiteralRationalEvaluation()`) plus a new twist: parenthesization is lost (`lcoe = a * b + c * d / e * f`). Doc-only — the executable bodies are generated from compiled ASTs and are correct — but the docstring now shows *wrong math* next to a correct body, which is worse than showing nothing.
6. **Positive finding — the AI implementation pass had zero work to do.** With live extraction, `compilation_results` is populated and codegen auto-implemented all 6 bodies (`AUTO_IMPLEMENTED = True`) from the expression ASTs: correctly parenthesized, literals intact, intermediates topologically sorted. All six bodies were reviewed line-by-line against the SysML — faithful. Nothing outside flat arithmetic (`+ - * / **`) exists in these models, so nothing needed hand translation. The anchor results confirm: bit-exact.
7. **Constraint predicates still not emitted** (Phase 6 gap, unchanged from WI-013/WI-014). The `assert constraint viability` in `ife_plant.sysml:155` does not appear anywhere in the generated package. Viability is applied harness-side in the sweep (ηG > 10, DI-001), exactly as planned.

## teax findings

No new gaps. The two WI-013 contract gaps (no default handlers for `RootModel[float]`/`float` exit channels; `write_json_model` assumes a Pydantic model) still require the harness-built OutputRouter + scalar WriteHandler; the workaround was reused verbatim in `run_anchors.py`.

## Anchor results

| Anchor | Point | Expected ($/MWh) | Executed ($/MWh) | Rel. dev |
|---|---|---|---|---|
| A | Hawker 14-parameter defaults | 252.29996307119066 | 252.29996307119066 | 0.0 |
| B | Realistic HIF (f=5 Hz, η=0.25) | 68.69020165241004 | 68.69020165241004 | 0.0 |
| C | Osiris hif_plant point (SV-013) | 270.1211779380445 | 270.1211779380445 | 0.0 |

Plus: f_recirc at all three points, Meier gamma $68.247/J, Meier driver cost $0.975B, Meier COE 4.735 c/kWh (vs Meier's published ~5, inside SV-014's ±15%). Oracle: `scripts/verify_ife_lcoe.py`. Tolerance stated in spec: relative 1e-6; observed: exact.

## Sweep

11,505 points (39 η × 59 G × 5 f), 0.1 s, generated module impls called in-process (same code the executor ran). 90.7% power-positive, 75.8% viable (ηG > 10), 64.5% attractive (viable ∧ LCOE ≤ $100/MWh). On-grid anchor-B check passes. Outputs: `data/ife_sweep/sweep_results.csv`, `ife_viability_eta_gain.png`, `ife_viability_by_freq.png`. Physics reading in `demo_report.md`.

## Reproduce

```bash
# 1. generate (live syside extraction; license valid)
cd ~/1cfe/sysml-codegen && uv run sysml-codegen generate \
  --models ~/1cfe/fusion-tea/exploration/ife_e2e/models \
  --output ~/1cfe/fusion-tea/exploration/ife_e2e/generated \
  --package-name ife_tea --pipeline-name ife_hif --overwrite
# 2. sanitize quoted names (codegen finding 3)
cd ~/1cfe/fusion-tea && uv run python exploration/ife_e2e/sanitize_names.py
# 3. anchors through the teax executor
cd exploration/ife_e2e && ../pipeline_spike/.venv-exec/bin/python run_anchors.py
# 4. sweep + figures
../pipeline_spike/.venv-exec/bin/python sweep_ife.py
cd ../.. && uv run python exploration/ife_e2e/plot_sweep.py
```
