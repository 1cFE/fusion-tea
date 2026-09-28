# Executor synthesis

[AGENT executor reading, 2026-09-16] Read committed study `a17f51f0`; snapshot SHA256 `5538c7aca0937fa4826cf4bf8bfe8d51c0b19f5c4ac0655906a5802746b470db`. This is the executor's interpretation of the frozen record, not an independent review.

## What the study set out to do

Eight native cases separate the retained legacy scenario, exact source profiles, coordinated source plasma geometry/field conditioning, explicit current-driven inventory sizing plus 1% reserve, and two local geometry changes. The intake and invariant scope remain in [record.md](record.md) and [protocol.md](protocol.md).

## What it found

Exact source profiles reduce forward auxiliary demand from 49.079601 to 45.172538 MW; coordinated Table5 conditioning reduces it further to 44.003808 MW. Neither recovers any legacy failed predicate. Legacy LCOE changes from $144.747431/MWh to $144.616024/MWh and then $144.656523/MWh. These are conditional forward outputs, not reproduction of a fully integrated published plant. See [report.md](report.md) and [case-summary.csv](results/case-summary.csv).

Current-driven inventory sizing plus 1% reserve recovers the conditional conductor-current screen. The joint intervention raises reference-effective tapes from 112.708720 to 239.983701 and tape procurement cost from $731.57 million to $1,557.69 million. Control LCOE rises by $18.446798/MWh and minimum pack-fit margin worsens from −0.120000 to −0.285309 m. The record does not attribute these changes to the 1% reserve alone. See [contrasts.json](results/contrasts.json) and [report.md](report.md).

## Framing verdict per axis

All eight axes remain sensitivity-framed. Fuel and temperature exponents change together. Table5 radius, volume-shaping factor and operational coil ampere-turns change together, so their individual effects are not identified. Sizing mode and reserve are a joint intervention. The isolated 2% radius increase introduces a sustainment failure; the isolated 2% minor-radius increase introduces a peak-field failure. No search boundary or optimum follows from this finite sample. See [record.md §5–8](record.md).

## Constraint structure

Zero of eight cases passes all twenty raw predicates. Divertor heat and local pack fit fail throughout. The legacy cases also fail current; reserve scenarios pass that conditional screen. Additional off-reference failures remain named above. The [160 per-case applicability rows](results/case-predicate-applicability.json) keep source scope separate from raw verdicts; there is no filtered combined pass.

The exact historical selected mode at multiplier 1.0 remains separate. Its [retained diagnostic](preparation/selected-mode-check.json) preserves 224/226 strict relative scalar matches and 19/20 oracle predicate agreement, including the current-boundary discrepancy. The eight new reserve/scaling cases do not resolve or replace that history.

## Findings carried forward

The four findings in [record.md §15](record.md) retain source-conditioned output attribution, unresolved local cavity/conductor transfer, incompatible coolant/generic-build scope and numerical-verification limits. The [all-point check](results/oracle-all-points.json) passes 1,808 mapped scalars and 160 exact predicates; sixteen native scalar channels remain outside the oracle map. The [source-conditioned divertor account](results/source-conditioned-divertor.json) derives deposited powers 49.5/48.5 MW and peak-equivalent areas 5.210526/9.7 m² from supplied peaks. It earns accounting consistency only.

## What the record does not support

The record does not establish published-reference feasibility, source-qualified conductor capacity or local cavity geometry, spatial target heat-load validation, water-loop hardware or installed costs, or a global feasibility boundary. Source volume, field and divertor peaks supplied as conditioning inputs earn no independent prediction credit. Engineering qualification and several costs remain unresolved. Final independent scientific review is outside this executor synthesis.
