# Two blanket coolant branches execute with separate heat boundaries

[AGENT] The new native model has helium and PbLi branches, a single owned internal transfer and an energy ledger. Two unchanged offered-capacity screens evaluate independently supplied hypothetical exchanger ratings. It demonstrates the missing two-branch accounting structure; it does not predict ARIES hydraulic performance or qualify its installed exchangers. Independent completion review accepted this bounded result.

## Native result

| Case | He duty MW | PbLi duty MW | Combined MW | Internal energy residual MW | He / PbLi scalar capacity |
|---|---:|---:|---:|---:|---|
| Source-derived boundaries | 1192 | 1444 | 2636 | 0 | Satisfied / satisfied |
| He rating reduced to 1100 MW | 1192 | 1444 | 2636 | 0 | Violated / satisfied |
| PbLi rating reduced to 1400 MW | 1192 | 1444 | 2636 | 0 | Satisfied / violated |
| Depositions increased 10%, original ratings | 1286 | 1599.5 | 2885.5 | 0 | Violated / violated |
| Transfer changed 111 → 200 MW | 1281 | 1355 | 2636 | 0 | Violated / satisfied |
| He friction changed 141 → 0 MW | 1051 | 1444 | 2495 | 0 | Satisfied / satisfied |
| He offered conditions unsupported | 1192 | 1444 | 2636 | 0 | Undefined capability / satisfied |

[AGENT] Original hypothetical ratings are 1250 MW He and 1500 MW PbLi. They stay unchanged during the deposition, transfer and friction perturbations. In the unsupported case the native constraint reports `violated` because definedness is zero; `supported=false` distinguishes that result from a physical duty shortage. These checks assess only scalar duty under assumed conditions, not UA, pinch, pressure or material limits.

[AGENT] Baseline source-derived depositions are 940 and 1555 MW, totaling 2495 MW. The separate report/test comparison to the printed 2496 MW is -1 MW. That source residual is not the native conservation residual, which is zero. The model receives no 2496 MW physical input and does not force its branch inputs to match it. Reproducing the source duties from inferred deposition inputs is accounting reconstruction, not independent thermal prediction. Outside the source case, the persisted comparison to 2496 MW is simply a scenario difference.

## What changed and what was reused

[AGENT] Added two concept-neutral definitions: a coolant branch energy balance and a two-branch energy ledger. One design contains four owners: internal exchange, helium branch, PbLi branch and ledger. Two branch calculations use the same exchange input with opposite signs; the ledger consumes their actual exposed heat duties. The generic `Offered Capacity Screen` calculation and `Offered Equipment Capacity` constraint remain unchanged, each instantiated twice. Two new guarded native completions implement the energy identities. The existing capacity completion is copied with only its package import prefix changed. [Build hashes](evidence/build-hashes.json) verify staged source identity and exact completion carry.

[AGENT] Five calculation usages execute: two branch balances, two capacity screens and one ledger. Two executable constraints and their report aggregator also run. This is actual connected reuse: generated pipeline edges take each branch's calculated duty into its existing capacity screen and independently supplied rating, then take the same duty into the ledger. No caller provides computed branch outputs. Existing DEMO hydraulics, HITEC equipment and Rankine physics are not relabeled as ARIES components.

## Verification and limits

[AGENT] The final native candidate passes seven supported scenarios with 42 independent 50-digit decimal heat comparisons. Each scenario also checks both capacity margins, support/definedness, expected verdicts, unchanged selected ratings and two assessed executable constraints. Explicit tests verify exchange cancellation and the 141 MW one-for-one friction effect. Two additional generated-wrapper calls produce signed ledger residuals -1 and +1 MW, confirming that diagnostics are not clamped or forced to zero.

[AGENT] Eleven full-pipeline invalid cases are refused: negative deposition, transfer or friction; negative net PbLi branch heat; nonfinite deposition, NaN transfer or infinite transfer; negative/nonfinite offered capacity; heat overflow; and an attempted override of a removed absent-direction input. Rejections must name the intended domain defect. [All effective inputs, outputs and refusals](evidence/results.json), [final execution log](evidence/execution.log), [first execution log](evidence/execution-attempt-01.log), and generation/sealing logs are retained.

[AGENT] Review caught two public absent-direction zero inputs in the first candidate. Because literal zeros also become public entries on this generator route, a generated same-part identity supplies the topology zero; the final schema exposes only the shared transfer input and rejects NaN/Inf and attempted absent-direction overrides. This adds one computed-attribute module, not a physical definition. The first candidate's inputs, results and hashes remain in `evidence/*-attempt-01.*`.

[AGENT] Scoped full validation returns exit 1: L1–L5 pass; L6 reports six unsupported `.` operators on plain EXPOSE attributes. Their [locations](evidence/expose-locations.txt) and [validator output](evidence/validation.log) are retained. Successful generation and execution resolve those exact branch and capacity edges. Independent review accepts a narrow static-tool exception; this is not a six-level validation pass. No shared-model regression claim follows from this isolated package.

[AGENT] Source inspection distinguishes the 141 MW He friction term from printed 156 MW pumping electricity and the cycle's separate compressor efficiency. PbLi recovered friction is explicitly approximated as zero for this printed balance, neglecting the source's 1–10 kW pumping scale; it is not zero physical pumping. The approximately 1 MW source residual remains visible. Source images and their hashes are retained. No coefficient or property was tuned.

[AGENT] This Raffray engineering case is separate from Lyon's 2436 MW systems reference and the supplied-profile WI-083 model. Divertor heat, cycle states and conversion efficiency are outside this two-blanket-branch sum. Flow, pressure drop, conductance, actual equipment, cost, electrical recirculation and LCOE remain unqualified. MR-7 preservation applies to the represented independent ratings and supplied heat choices; there is no sizing policy.

## Reproduce

```bash
.codex-test/run python exploration/aries_transfer/dual_blanket_heat/build.py
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/dual_blanket_heat/run.py
.codex-test/run agentic-mbse validate --complete exploration/aries_transfer/dual_blanket_heat/input_models
```

[AGENT] Build stages source files, generates the new package, carries the two authored and one unchanged guarded completions, then regenerates with `--preserve-handwritten` to refresh contracts. Run loads the package through the provisional loader and executes real TEAx pipelines. Staging, import links and run stores are ignored; source, generated contracts, completions, scripts and compact evidence are retained.

[AGENT] Final acceptance: `work/orchestration/aries-transfer-experiment/evidence/heat-transport-review.md` accepts the repaired single-exchange interface, independent native replay and six named L6 EXPOSE exceptions. The removed-input override is rejected by the generated entry schema; it is not a thermal-domain test. SV-130 and both new definition traces are recorded.
