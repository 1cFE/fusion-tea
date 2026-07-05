# IFE End-to-End Demonstration — WI-015 Report

**Date**: 2026-07-05
**One line**: the validated IFE/HIF SysML models went through live extraction → code generation → execution for the first time, reproduced all three verified LCOE anchors exactly, and produced a 11,505-point viability map of the (η, G, f) space.

## What this demonstrates

Until this week, no SysML model in this program had ever been turned into executable code and run. WI-013 closed that loop on a toy solar-battery fixture. This item closes it on the models that matter: the Hawker 14-parameter IFE cost model and its Heavy Ion Fusion (Osiris) instantiation — and adds the piece the pipeline always lacked, a real correctness oracle.

The chain that ran, end to end:

1. **Live extraction** — sysml-codegen parsed the 11 IFE model files (`exploration/ife_e2e/models/`, staged from `models/library/` + `models/designs/`) through syside. First live extraction since the license lapse, and the first ever of these models.
2. **Generation** — 6 calc defs → a 6-module computation graph → a complete Python package: Pydantic schemas, teax module wrappers, pipeline YAML, registry (`exploration/ife_e2e/generated/`).
3. **Implementation** — all six calculation bodies were emitted automatically from the compiled SysML expressions, correct on first try. The planned AI implementation pass had nothing to translate: everything in these models is flat arithmetic, and live extraction preserves the expression ASTs that the WI-013 snapshot path lost.
4. **Execution** — the teax executor ran the generated pipeline three times (one per anchor point), producing per-channel JSON outputs (`exploration/ife_e2e/outputs/`).
5. **Anchor check** — generated-code LCOE asserted against `scripts/verify_ife_lcoe.py`, the hand-verified mirror of the SysML model. Registered as **SV-023 (passing)**.
6. **Viability sweep** — 11,505 grid points over driver efficiency η, target gain G, and rep rate f, classified against the ηG > 10 constraint (DI-001) with a $100/MWh overlay (`data/ife_sweep/`).

## Anchor table (expected vs generated)

Tolerance: **relative 1e-6** — the model is flat float arithmetic, so the generated code must agree to float precision; 1e-6 leaves room for expression reassociation while catching any wrong term or constant. Observed agreement: exact to at least 9 decimals on every check.

| Point | Expected | Generated pipeline | Verdict |
|---|---|---|---|
| Hawker 14-parameter defaults | $252.299963/MWh | $252.299963/MWh | OK |
| Realistic HIF (f=5 Hz, η=0.25) | $68.690202/MWh | $68.690202/MWh | OK |
| Osiris hif_plant point (SV-013, ~$270) | $270.121178/MWh | $270.121178/MWh | OK |
| Meier driver γ (Eq. 5 at Osiris) | $68.247088/J | $68.247088/J | OK |
| Meier driver direct cost | $0.974958B | $0.974958B | OK |
| Meier COE (Osiris) | 4.735404 c/kWh | 4.735404 c/kWh | OK |
| f_recirc at each anchor (3 checks) | 0.041667 / 0.083333 / 0.072223 | same | OK |

Nine assertions, nine passes (`run_anchors.py`). The Osiris expected value $270.12 was computed from the same oracle at the exact `hif_plant.sysml` bindings, γ included — consistent with the epic's "~$270 (SV-013)".

## What the viability map shows

Figures: `data/ife_sweep/ife_viability_eta_gain.png` (η–G plane at f=5 Hz) and `ife_viability_by_freq.png` (same map at f = 1, 2, 5, 10, 20 Hz). Grid data: `data/ife_sweep/sweep_results.csv` (11,505 rows; 39 η × 59 G × 5 f; non-swept parameters at the realistic-HIF baseline).

**Caption / physical reading**: LCOE across the driver-efficiency × target-gain plane. Two physics boundaries cut the plane: the dashed curve is where net electric power reaches zero (ηG ≈ 4.2 at this blanket/thermal point — below it the plant consumes more than it makes), and the solid curve is the ηG = 10 economic viability threshold (DI-001) — between them the plant makes net power but recirculates so much to the driver that cost blows up. LCOE falls steeply as you cross ηG = 10 and then flattens: this is the knee. Past the knee, extra gain or efficiency buys little — the $100/MWh contour (red) hugs the knee rather than the map's cheap interior. The white star is the realistic-HIF anchor ($68.69/MWh), comfortably inside the feasible region.

**Numbers**: 90.7% of the grid is power-positive, 75.8% viable (ηG > 10), 64.5% additionally under $100/MWh. The small-multiples figure shows the feasible region is nearly invariant in rep rate (attractive fraction 63% → 65% from 1 to 20 Hz): at this baseline the knee is set by ηG, not f — rep rate scales the plant, and per-MWh cost saturates. The on-grid anchor point reproduces $68.6902/MWh, tying the sweep to the executor-verified code.

**Method note**: viability is classified harness-side (`sweep_ife.py`) because `assert constraint` does not survive codegen extraction (Phase 6 gap, per WI-014) — as the epic planned. The sweep calls the generated implementation functions directly (the same code the executor ran), so 11,505 points take 0.1 s.

## What broke and how it was handled

Full detail with file:line in `findings.md`. Summary:

- **Model-side (3 fixes, all in-repo, all value-neutral, all pass syside check)**: the six calc defs' `return` outputs converted to `out attribute` (return parameters parse as ReferenceUsage, which extraction ignores); `cost_billions` promoted to an output (it's referenced cross-part); a concrete `hif_driver_instance` part usage added (codegen indexes part usages by their *first* type, which for a redefining usage is the inherited type, so 'HIF Driver' looked uninstantiated and its calc was dropped).
- **Codegen (workaround + finding)**: quoted SysML names ('IFE LCOE') leak raw into Python file names, imports, and class names — the generated package can't import. Fixed by a deterministic post-processor (`sanitize_names.py`), filed as a finding.
- **Codegen (finding, no workaround needed for the anchors)**: cross-part bindings (`driver.cost_per_joule = meier_cost.gamma`) are not wired in the generated pipeline — they fall to unresolved entry-point inputs with no pre-filled values. The harness closes the γ → LCOE loop by feeding one run's outputs into the next run's inputs. This is the most important gap for the upcoming MFE plant models.
- **teax**: the two WI-013 gaps (primitive-typed exit channels) reproduce; same OutputRouter workaround.

## Artifact index

| Artifact | Path |
|---|---|
| Spec (anchors + tolerance) | `work/active/WI-015_ife-end-to-end-demo/spec.md` |
| Gap record | `work/active/WI-015_ife-end-to-end-demo/findings.md` |
| Staged model snapshot | `exploration/ife_e2e/models/` |
| Generated package | `exploration/ife_e2e/generated/` |
| Name sanitizer (codegen workaround) | `exploration/ife_e2e/sanitize_names.py` |
| Anchor harness | `exploration/ife_e2e/run_anchors.py` |
| Executor run outputs | `exploration/ife_e2e/outputs/{hawker_defaults,realistic_hif,osiris}/` |
| Sweep harness / plotter | `exploration/ife_e2e/sweep_ife.py`, `plot_sweep.py` |
| Sweep grid + figures | `data/ife_sweep/sweep_results.csv`, `ife_viability_eta_gain.png`, `ife_viability_by_freq.png` |
| Validation entry | SV-023 (passing) in `modeling_project/VALIDATION_MATRIX.md` |
| Oracle | `scripts/verify_ife_lcoe.py` |
