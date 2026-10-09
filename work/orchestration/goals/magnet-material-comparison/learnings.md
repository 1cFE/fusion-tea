# Learnings: REBCO versus Nb₃Sn magnet subsystem at matched duty

What this run now knows. Append-only, newest last, ISO dates, never edited in place. An entry is appended only after a round review has accepted or corrected the delta the round result proposed (`work/orchestration/GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

[AGENT] L-001–L-004 accepted at the Round 1 review on 2026-09-29 (trail.md § Round 1 review). They are reviewed engineering, model and process findings, not owner-originated settled requirements. Evidence: [answer.md](answer.md), [final review](evidence/final-review.md), sealed study `exploration/magnet_materials/studies/20260929-magnet-material-comparison/` at `7836424ca`.

## L-001 — At matched duty in the common supported range, the REBCO/Nb₃Sn preference is a conductor-price question

Where both supplied windings are supported and fit the EU DEMO envelope (8–11 T, common construction), the annualized Nb₃Sn subsystem is cheaper under every checked conductor-law, construction, cryogenic and financing variant that leaves the pair rankable; the sign reverses only when REBCO tape reaches the 10 USD/m volume price, and then only at 9–11 T. The break-even REBCO price runs 6.62–23.13 USD/m over the 592 supported-status pairs (11.25 at the 10 T reference point). REBCO's 20 K refrigeration advantage (4.6 MW of cold-stage input, 20.5 M USD of refrigerator capital) is about 3.6 M USD/yr, 1.5 % of the annualized conductor purchase difference. Report the break-even price, not the sign; economics are winding plus refrigeration only.

## L-002 — Fit boundaries in a fixed envelope are construction-rule results, not conductor-law results

Nb₃Sn first fails the 3751.1 mm² DEMO envelope at 12 T under the calibrated CICC rule (−178.6 mm²) and at 18 T under the compact rule; on the 420.8 mm² Stellaris envelope neither material fits under the CICC rule at any field. Every turn is sized at peak field with pack-average steel, conservative and equal for both materials. Read such a failure as a verdict on the supplied construction, never as a material field limit; the law's edge (13 T) and law-only (14 T) bands are validity flags of the fit, not performance limits.

## L-003 — Conductor-law uncertainty moves the rankability of supplied hardware, not the preference sign

Under −0.6 % intrinsic strain or a lower Nb₃Sn production grade, and under the REBCO power-law shape, T* 17 K or degradation 0.80, fixed reference hardware fails its acceptance rule and the pair is unranked until more elements are supplied; re-offered hardware restores the ranking and moves the break-even by −18 % to +63 % (at most 23.1 USD/m at 11 T). MR-7 supplied offers make this visible: a model that resized automatically would have hidden the unranked state and reported a continuous cost instead.

## L-004 — Process: the isolated-package route needs three things settled before the pin

The integration seam refuses a CANDIDATE pin until the package's canonical SysML files are registered in `tests/model_families.py` (finding #1); sysml-codegen cannot emit a negative design literal as an entry point, so any such value must be supplied by every case and the package must never run on generated defaults; and the stock study manifest must name a real oracle module (finding #2, still open). A separately authored oracle written from the contract and design alone, with a different root finder and integrator, agreed with the package to 1e−9 on every channel of 2310 points and surfaced three design and reference-case ambiguities (A1 domain guard, A2 unrounded construction C, A6 double-counted shield load) that were then corrected in the design, the reference case and the contract test value before the study ran.

[AGENT] L-005–L-007 accepted on 2026-10-05 with the Round 2 review, after [independent final assurance](evidence/pr-readiness/independent-review.md). These are reviewed agent findings, not owner-originated settled rules. Evidence: sealed `20260930-magnet-material-plant-map@a9683fa1d`, [answer](answer.md) and case-linked reporting data. Round 2 T-010 resolves L-004's historical missing Round 1 oracle-entry/manifest seam; the distinct Round 2 stock-manifest finding remains open as recorded in the discovery log.

## L-005 — Plant consequences change the conditional material price threshold

The plant comparison changes the subsystem price threshold through geometry, plasma, equipment and energy consequences. The eight base-cell break-even prices span 5.68–37.66 USD2021/m; anchored × 1.0 has no comparator. This is an envelope over tested supplied designs under the declared policy and mixed-year accounts, not a universal material threshold or a continuous optimum.

## L-006 — Supported ingredients do not qualify an assembled configuration

Sourced confinement values and field ratios do not establish support for the selected coil/plasma configurations. Every comparative best design carries U physical-transfer evidence. Numerical agreement and a source-derived slope do not upgrade that evidence grade; failed breeding, open divertor geometry and unpriced capacities remain separate obligations.

## L-007 — Field plots must distinguish own-sized choices from paired duty labels

Equal-duty REBCO designs can have an actual peak field different from the Nb₃Sn target used as their label. Plot own-sized field targets or actual peaks and retain paired duty explicitly. The current field panels use own-sized designs; interaction data keeps actual peaks and equal-duty flags.
