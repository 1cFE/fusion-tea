---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-19
Updated: 2026-09-20
---

# WI-073: Matched steam cycle for current comparison

## Outcome and authority

[NEED] Establish a physically justified, reproducible cooling-to-electricity calculation for the current integrated stellarator comparison. The owner selected this path with “yes, pursue that cycle”, in reply to coherent steam-cycle work preserving current helium/salt technology and salt temperatures. Authority: native goal `work/orchestration/goals/current-model-comparison-readiness/goal.md`, owner ruling. This releases research and implementation, not a particular turbine pressure, regenerative arrangement or efficiency assumption.

[NEED] Retain the existing scientific comparison criteria, input-selection rules, physical limits and rubric targets. Preserve r2, historical evidence, unrelated work and sealed ARIES. No broad optimization or tuning to old LCOE. Fresh physical/source review must precede substantial implementation. Final replacement adoption, reveal and formal goal closure remain owner-held.

## Required reading

`knowledge/holdout/aries-cs/PROTOCOL.md`; project Codex/runtime instructions; `modeling_project/MODELING_PROCESS.md`; current goal and Round 1 physical proposal/review v2; `evidence/physical-research/cycle-basis/report.md`; current comparison spec and source/input-selection rules. Do not open held-out or barred material or the excluded demo concept.

## Requirements

- R1 [NEED] Connect available salt heat to a coherent steam-cycle state set across finite, justified temperature differences. Preserve existing helium/salt technology and salt supply/return definitions. Explicitly identify any changed design assumptions separately from corrected calculations.
- R2 [INFERRED] Close cycle mass, energy and internal work accounts, including feedwater heating, expansion, condensation, water pumping and conversion losses. Expose heat-source demand, heat rejection, steam flow, electrical production and cycle auxiliary demand with clear gross/net ownership. Do not count an internal pump twice or silently absorb plant auxiliaries into a fitted efficiency.
- R3 [NEED] Establish source applicability for water properties and performance assumptions. State unsupported installed equipment, cost and operating-domain claims. Verify steam-generator cost ownership without inventing coverage or double charging the primary exchanger.
- R4 [NEED] Preserve adverse engineering outcomes and invalid calculations. Numerical comparison tolerances cannot relax strict engineering inequalities. New supported-domain checks need stated physical/source bases and review.
- R5 [INFERRED] Represent the affected components, functions and heat/work interfaces in the existing model architecture. Keep reusable calculations in the library and scenario choices in the stellarator design; expose producer quantities for downstream consumers. Avoid an executable dependency cycle between cooling equipment and conversion diagnostics.
- R6 [NEED] Independently verify new numerical outputs and predicates; rerun affected regression and historical replay checks under explicit modes. Preserve historical contracts or name incompatibilities. Show baseline changes in thermal balance, efficiency, pumping, net electricity, checks, capital and LCOE.
- R7 [NEED] Evaluate a small justified set of permitted-input/interface cases, regrade affected depth cells and integrate the exact reviewed implementation before candidate freezing. Broad comparison adapter/archive work remains owned by the coding item.

## Scope and current constraints

[INHERITED] Entering package has 956 numeric outputs and 25 predicates, semantic fingerprint `ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a`. These counts describe the entering state, not required final counts. The former480°C fit argument has no demonstrated matching steam cycle at the465°C salt supply. A proposed 445°C/6.2 MPa/171°C-feedwater heat-admission screen does not establish a complete cycle or its efficiency. Its states remain proposed until reviewed design selects a defensible cycle.

[AGENT] Affected owners include power-cycle analysis, turbine structure/assembly, cooling-to-cycle interfaces, power balance and heat rejection, generated executable/contract, independent oracle and verification mappings. Current physical pumping and salt-temperature equations remain the fixed boundary unless evidence triggers an owner decision. Shared generic MFE consumers and explicit historical modes must be inventoried before implementation.

## Acceptance evidence

- [x] Source-grounded state-resolved proposal and prototype; independent source/math review.
- [x] Reviewed interface/design and persistent phased implementation plan.
- [x] Canonical model and executable agree; independent property/state/work checks cover new outputs.
- [x] Baseline and bounded cases preserve raw failures and demonstrate complete accounting.
- [x] Affected full regression/replay scopes finish with explicit residual consequences.
- [x] Fresh affected-cell depth assessment and integrated model audit.

Research is T-008 under the goal, with its own native request and receipts. T-009 implemented the reviewed cycle and corrected an independently discovered mixed-mode heat-budget inconsistency. Fresh scientific audit passes R1–R5; fresh depth grading meets all23 targets and native integration passes all ten gates. Final full regression and fresh independent audit now satisfy R6–R7; actual comparison archive restoration and owner adoption remain separate gates.

SV-122 was updated to passing through the native PM operation after independent property, state, heat/work and failure checks. Evidence: `evidence/sv122-update.log`, `evidence/independent-oracle/README.md` and the goal `evidence/round2/cycle-native-science-review.md`. Numerical tolerances follow the reviewed design; strict engineering inequalities remain unchanged. The PM operation reported inherited malformed legacy Type cells and left them unchanged.
