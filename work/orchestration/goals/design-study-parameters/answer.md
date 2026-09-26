# Answer: which operating choices improve net electricity and LCOE, and what stops the improvement

Goal `design-study-parameters`, round 1, 2026-09-26. **Status: provisional.** The study `20260926-design-study-parameters` executed (272 stored points) and is recorded and committed, but its seal is parked on owner gate G-001: the all-point verification refused one channel of one case at 1.466e-9 relative (a 0.363 K margin whose two temperatures agree to 5e-10 K) against the 1e-9 rule with no declared class, and the contract forbids adding a class after a result is seen (`evidence/owner-gate-verification-class.md`). Every number below is a stored channel of the committed record (`exploration/costed_loop_brayton/studies/20260926-design-study-parameters/results/readout.md`); none moves under either ruling. Closure remains the owner's.

## 1. The starting point, in plain terms

The plant is the WI-093 C-1 assembly: the Stellaris helium primary loop delivers 3,301 MW at 773 K (3,126 MW of blanket heat plus 175 MW of loop pump friction) through a 50,000 m² exchanger with 50 MW/K of conductance into the ARIES closed helium Brayton chain (three compressor stages with intercooling, a recuperator of 0.8 effectiveness, one turbine). Its design point is a cycle flow of 2,500 kg/s and an equal stage pressure ratio of 1.518 (overall 3.5). At that point the cycle removes all the heat, the turbine sees 677.5 K, the compressors take 2,451 MW of the turbine's work, the generator makes 666.9 MW gross, and after the loop pumps (175.3 MW) and the ARIES auxiliary register (65 MW electric: 40 heating wall-plug, 10 cryogenic, 5 fuel, 5 control, 5 other) the plant nets 426.579 MW. That is the "423 MW" of earlier work, on this assembly.

Costed on the re-selected inventory I-R (the WI-093 case ratings: compressor 3,200 MW, turbine 7,000, generator 3,600, heat rejection 5,000, helium duty 3,500, all extrapolated beyond 1.5× their ARIES reference), the overnight capital is 4,873 MUSD2004 and the conditional LCOE 1,559.4 USD2004/MWh under the no-breeding-credit convention, of which 1,426.3 is purchased tritium and 133.1 is the plant side (capital 103.5, O&M 22.0, the rest 7.6). The absolute figure is conditional on an ARIES-scope rest-of-plant constant (2,158 MUSD, `[ASSUMED]`) and the fuel convention; the paired deltas at equal fuel are the comparison (`evidence/comparison-contract.md` § 6).

## 2. What improves net electricity and LCOE

Lowering the stage ratio at fixed flow raises net electricity until the heat-removal check fails; raising the flow lowers the ratio at which that happens. On the 8 × 16 grid (2,000–4,000 kg/s, ratio 1.20–1.80, refined near the boundary), 52 of 100 stored I-R points satisfy every check. The best passing band is:

| Case | Flow kg/s | Ratio | Net MW | Δnet | Unmet heat | LCOE USD/MWh | ΔLCOE | Plant-side ΔLCOE | Checks |
|---|---|---|---|---|---|---|---|---|---|
| starting point | 2,500 | 1.5183 | 426.579 | | 0 | 1,559.438 | | | 9 of 9 |
| `ir-f2250-r1.5183` | 2,250 | 1.5183 | 597.481 | +170.902 | 0 | 1,113.379 | −446.059 | −38.069 | 9 of 9 |
| `ir-f2750-r1.3750` | 2,750 | 1.375 | 594.567 | +167.988 | 0 | 1,118.836 | −440.602 | −37.604 | 9 of 9 |
| `ir-f2500-r1.4500` (the screen's best) | 2,500 | 1.45 | 575.617 | +149.038 | 0 | 1,155.670 | −403.768 | −34.460 | 9 of 9 |
| `ir-f2500-r1.4250` (electricity-only best) | 2,500 | 1.425 | 620.008 | +193.430 | 7.775 MW | 1,072.926 | | | heat removal fails |

The two top points are 2.9 MW apart, below the contract's 5 MW materiality, so they are one band: about +170 MW (+40 %) of net and −446 USD/MWh (−29 %) of LCOE against the starting point, with annual energy rising from 3.18 to 4.45 TWh. Within one inventory every cost term is a constant of the sweep, so the whole LCOE change is the denominator effect of the net gain: −408 of the −446 is the fixed tritium purchase spread over more energy, −38 is the plant side.

## 3. What stops the improvement

**Below the passing band, the thermal limit is heat removal at the exchanger.** As the ratio falls, the compressor exit cools less and the recuperator returns more heat, so the helium arriving at the heater is hotter (453 K at 2,250 / 1.5183, 473 K at the electricity-only best, 423 K at the design point). The 773 K source can only deliver what 50 MW/K of conductance carries across that temperature difference; once the heater inlet is too hot, source heat goes unremoved (7.8 MW at 2,500 / 1.425, 46 MW at 2,250 / 1.50, 52 MW at 2,750 / 1.35) and the case fails. The ridge of net sits one grid step on the failing side at every flow (figure `results/figures/flow-ratio-map.svg`): that is why the best passing point differs from the electricity-only best, by 22 MW at the design flow.

**Above the band, the equipment limit is the compressor rating**, then net itself. On I-R the 3,200 MW compressor is exceeded at 2,250 / 1.80, 2,500 / 1.80, 2,750 / 1.70 and 3,000 / 1.60; from 3,250 kg/s upward the net goes nonpositive before any rating binds (55 such points refused by the scan, plus one Brayton guard at 4,000 / 1.80). Higher flow lowers the turbine inlet (735.8 K at 2,250, 708.0 K at 2,750 at their best ratios) and the compressor work rises with the flow, so the band narrows and its best point falls beyond 3,000 kg/s.

**The ARIES-selected inventory I-A supports none of it.** At the same 100 points its 1,500 MW helium-duty package is 1,801 MW short of the constant 3,301 MW duty, the 1,600 MW compressor is exceeded at 79 points and the 2,500 MW heat rejection at 52; I-A prices the best band 8–11 USD/MWh lower (booked purchases 461 against 812 MUSD) because its ratings are too small for the operation. Hardware is selected before the sweep and priced from what was selected (MR-7); no point was resized.

## 4. Under the declared uncertainties

| Sensitivity | Effect at the anchors | Does the best passing point move? |
|---|---|---|
| S1 machine efficiency (compressor 0.85 / 0.92, turbine 0.90 / 0.95) | net −95 to −108 / +66 to +75; −42 to −92 / +26 to +59 MW | yes, by one grid step: 2,250 / 1.5183 fails at compressor 0.85 (2.8 MW unmet) and turbine 0.90 (70.7 MW); 2,500 / 1.45 passes under every level; 2,250 / 1.50 passes at turbine 0.95 |
| S2 auxiliaries (register ×0.5 / ×1.5; wired fuel term; Stellaris-equivalent register) | net +32.5 / −32.5; −1.8; −50.2 MW at every anchor; LCOE −57 to +208 | no; a constant cannot reorder points |
| S3 loop pump law (dp ×0.5 / ×2) | ×0.5: +25 to +58 MW, 2,250 / 1.50 passes; ×2: −50 MW at the starting point but −126 to −178 MW and 103–224 MW unmet at the boundary anchors | yes: the doubled friction heat cannot be removed at the boundary, so the band retreats toward the starting point |
| S4 prices (equipment ×0.5 / ×1.5; rest-of-plant ×0.5 / ×2) | LCOE ∓9 to 13; −25 to −35 / +50 to +70 USD/MWh | no |
| S5 fuel convention (feed 100 kg/year, 30 MUSD/year service) | LCOE 446 at the best point, 624 at the start (−668 / −935) | no; plant-side unchanged |
| S6 exchanger 75,000 m² (87.5 MUSD, +29 MUSD) | boundary at 2,500 kg/s moves 1.45 → 1.40: 671.6 MW passing (LCOE 991); 2,250 / 1.50 passes at 632.5 | yes, up by 74 MW: the exchanger is the priced lever |

## 5. How flow and ratio should be chosen together

Choose the ratio at each flow just above the heat-removal boundary, and choose the flow where that boundary point has the most net: on this assembly that is 2,250–2,750 kg/s at ratios 1.375–1.518, about 595 MW. The best band sits on the boundary, so a robust choice at fixed machine efficiencies is one step inside it: 2,750 / 1.375 keeps an 8.6 K helium margin against 0.7 K at 2,250 / 1.5183, and 2,500 / 1.45 (575.6 MW) passes every S1 level and every S2 level. Rankings between flows far from 2,500 kg/s are model exploration at fixed efficiency (contract § 8 a). If more net is wanted than the band gives, the lever is hardware, not operation: a 50 % larger exchanger buys 74 MW for 0.7 USD/MWh of capital; the compressor rating is the next limit.

## 6. What this answer does not claim

Fixed isentropic efficiencies at every flow and ratio (no off-design map; S1 bounds the first-order effect); the ARIES auxiliary register on a Stellaris loop (S2 bounds it, including the 13 MW of heat-rejection pumping the balance omits); the Stellaris pump relation as a hydraulic model (S3); an ARIES-scope rest-of-plant (S4); unsupported breeding (S5); the loop returning helium colder than the blanket inlet (not checked). No point is qualified as a design by passing the checks. The seal of the study awaits owner gate G-001.

## 7. Evidence and replay

- Record: `exploration/costed_loop_brayton/studies/20260926-design-study-parameters/record.md` (17 sections), `results/readout.md`, `results/figures/`, `oracle-window-scan.json` (the refused edge), `axis-plan.json` (anchors).
- Contract and reviews: `evidence/comparison-contract.md` (v2, fresh-reviewed), `evidence/contract-review.md`, `evidence/design-review.md`, `evidence/implementation-review.md`, `evidence/integration-t004/integration_return.json` (CANDIDATE).
- Package: `work/active/WI-094_costed-loop-brayton/report.md`; the C-1 controls replay bit-exactly.
- Candidate ledger: `candidate-ledger.md`. Proposed write-up passage: `proposed-passage.md`.
- Replay: the commands in `results/execution-context.json`, run from the repository root through `.codex-test/run` into a scratch record directory (never into the committed one); `prepare` composes and scans, `baseline` and `preflight.py gates` gate, `execute` needs the integration return, `verify` re-checks the store, `flow_ratio_reporting.py` and `flow_ratio_figures.py` regenerate the readout and figures.
