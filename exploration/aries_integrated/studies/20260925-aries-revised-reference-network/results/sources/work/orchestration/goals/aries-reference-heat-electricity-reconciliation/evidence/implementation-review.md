# Implementation review — WI-092 executed behaviour

Reviewed at repository HEAD `6828df18`. Fresh reviewer; entry files only; model and build not run; 13 tool calls.

**Verdict: PASS** — notes only, nothing blocking or correct-before-use.

## Checks

- **Code versus design.** Mode 1 runs helium on the whole flow, then PbLi on `s·C` and divertor on `(1−s)·C` from the helium outlet, and mixes `s·Tp + (1−s)·Td` (`native_completions/network_heat_driven_closure_impl.py:31,78–82`). Residual, bracket, tolerances and cap match the design. Both refusals precede the mode branch (lines 25–26), so one domain rule holds in both modes; the three refusal cases refuse with the expected messages. In all ten mode-1 cases `mixed_outlet` equals `turbine_temperature` within 8e-10 K, consistent with the 1e-8 MW residual tolerance over C ≈ 8.3 MW/K.
- **Mode-0 exactness.** 27 replay rows: 546/546 channels exact, worst relative 0.0, verdicts equal. Five outputs added, none removed; two new public keys with defaults 0 and 0.85.
- **Direction triple.** PbLi unmet 197.33 → 56.36 → 18.99 MW at s = 0.55/0.85/0.98; helium unmet 0 → 53.51 → 0; divertor unmet 0 → 0 → 149.49 MW. The only input differing across the three is `pbli_split_fraction`; areas (50 000 each) and cycle flow (1600) are identical.
- **No hidden sizing.** `network-c3-zero-divertor-area` differs from `split-0.85` only in the divertor area and reports `divertor_transferred` 0, `divertor_unmet` 191.41 MW (the full delivered duty). `network-c3-1800-rating-1800` differs from `network-c3-1800` only in the compressor rating; its 35 changed outputs are all compressor-screen, purchase, cost and LCOE channels, no thermal output.
- **Oracle.** `studies/oracle_entry.py:103–131` re-derives the network and solves `t − heater_pass(t)` with brentq; self-check worst relative ≤ 2.4e-10 on the seven listed channels over 37 cases.
- **Preservation and validation.** Preservation passed (18 725 files, none changed or missing). L2 105 → 105. L6 493 → 498; all five additions are the pre-existing "Unsupported operator '.'" class on the five new mirror attributes.

## Findings

1. **Note.** "Line for line" (docstring, calc-def doc, design) overstates textual identity: mode 0 is the reviewed loop refactored into a `stage()` helper with the capacity rate parametrised. Behaviour is bit-exact per the replay. Reword to "equation for equation, bit-exact on replay".
2. **Note.** The design names the echo outputs `network_mode` and `pbli_split`; the library (`integrated_heat_electricity.sysml:182–183`), plant binding and migration report use `network_mode_used` and `pbli_split_used`. Sensible (no clash with the part's input attributes); update the design text.
3. **Note.** Design [r1] asks for one shared disclosure sentence; the calc-def doc and docstring disclose the split's role in different wording.
4. **Note.** `migration-report.json` reports `new_channels: 20` per replay against five added outputs; state what the other 15 are.

## MR-7

**MR-7: compliant** for the affected scope on executed evidence. The split only moves unmet heat between streams; no case enlarges an exchanger, no quantity becomes an installed capacity, and the resized alternative is a declared input. The 0.85 default is not the best sampled split for net electric (0.9 gives 882.1 vs 879.7 MW), consistent with the claim that it was not fitted to an output.

## Not covered

Source truth, attribution and study design (excluded). The four passing validation levels and the preservation entry commit `9691429` are not evidenced in the entry files. Consumers beyond `plant.sysml:244–335` not inspected. The retained `'Heat Driven Closure'` was confirmed present (library line 46), not diffed.

— fresh implementation reviewer, 2026-09-25
