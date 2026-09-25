# Implementation review brief — WI-092 executed behaviour (fresh reviewer)

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 14 tool calls and a 500-word return, written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/implementation-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks, goal trails or other work items. Do not run the model.

## Exact question

Does the implemented and executed WI-092 increment do what its reviewed design says, keep the original series case exactly, and stay MR-7 compliant in executed behaviour?

## Entry files

1. `work/active/WI-092_aries-parallel-exchanger-network/design.md` — the reviewed design (equations § Equations; role table § MR-7; migration § Migration; validation plan).
2. `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py` — the new completion (mode 0 must be a line-for-line copy of `exploration/aries_integrated/native_completions/heat_driven_closure_impl.py`; compare them).
3. `models/library/analyses/integrated_heat_electricity.sysml` — search for `'Network Heat Driven Closure'`; and `models/designs/aries_cs_integrated/plant.sysml` lines 244–335 (the rebound `heat_exchangers` part).
4. `work/active/WI-092_aries-parallel-exchanger-network/evidence/migration-report.json` — mode-0 replay comparison (27 sealed points), added outputs, type change.
5. `work/active/WI-092_aries-parallel-exchanger-network/evidence/development-cases.json` — 40 native development cases (use a short Python one-liner or jq to extract, do not print the whole file): for each non-replay case read `outputs` channels `aries_integrated_plant__heat_exchangers__evaluate__{turbine_temperature,unmet_heat,he_unmet,pbli_unmet,divertor_unmet,pbli_stream_out,divertor_stream_out,mixed_outlet}` and `aries_integrated_plant__plant_ledger__evaluate__{gross_electric,net_electric,plant_residual}`, plus `effective_inputs` for `…heat_exchangers__network_mode`, `…pbli_split_fraction`, `…he_hx__selected_area`, `…pbli_hx__selected_area`, `…divertor_hx__selected_area`, `…cycle__selected_flow`.
6. `exploration/aries_integrated/studies/oracle_entry.py` lines 95–135 — the independent checker's network branch; and `work/active/WI-092_aries-parallel-exchanger-network/evidence/oracle-self-check.json`.
7. `work/active/WI-092_aries-parallel-exchanger-network/evidence/validation-comparison.json` and `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/preservation-check-wi092.json`.

## Expected checks

- **Code versus design:** the mode-1 stage evaluation (helium on the whole flow, PbLi and divertor on split flows from the helium-stage outlet, adiabatic mixing), the identity turbine temperature = mixed outlet at convergence (check `mixed_outlet` equals `turbine_temperature` in the mode-1 cases), refusals for split ∉ (0,1) and mode ∉ {0,1}, the single domain rule, the docstring disclosure.
- **Mode-0 exactness:** every replay row worst relative 0 and verdicts equal; new outputs listed; no removed outputs.
- **Direction triple (MR-7 executed evidence):** at the C3 inputs `network-c3-split-0.55 / 0.85 / 0.98` — PbLi unmet falls from ≈ 197 to ≈ 56 MW, divertor unmet appears at 0.98, selected areas and flows identical across the three; `network-c3-zero-divertor-area` reports divertor heat unmet rather than manufacturing transfer.
- **No hidden sizing:** confirm no input in the three cases changed except mode/split; confirm `network-c3-1800-rating-1800` changes only the compressor rating (a declared resized alternative) and not any thermal output.
- **Oracle independence:** the network branch in `oracle_entry.py` is a separate derivation (brentq on `t − heater_pass(t)`) and its self-check agreement with the native outputs is within 1e-9 on the listed channels.
- **Preservation and validation:** preservation check passed; validation levels 4 passed / 2 failed with the L2/L6 counts compared against the inherited 105/493.

Return `MR-7: compliant / violated / unverified` for the affected scope on executed evidence.

## Exclusions

Source truth, the goal's attribution and the study design. Do not run the model or the build.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; numbered findings with severities (blocking / correct-before-use / note); the MR-7 statement; what the review did not cover. Sign as "fresh implementation reviewer, 2026-09-25".
