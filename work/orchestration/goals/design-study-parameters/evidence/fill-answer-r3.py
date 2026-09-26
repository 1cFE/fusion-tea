"""Write the round-3 answer and the round-3 section of the candidate ledger from the two sealed readouts (presentation arithmetic on stored channels)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
G = ROOT / 'work/orchestration/goals/design-study-parameters'
R3 = ROOT / 'exploration/costed_loop_brayton/studies/20260926-design-study-parameters-b'
rb = json.load(open(R3 / 'results/readout.json'))['rows']
S = rb['ir-f2500-r1.5183']; B = rb['ir-boundary-f2500']; S6 = rb['s6-hx75000-f2500-r1.4000']; L = rb['ir-f2500-r1.4300']
def row(k, label):
    r = rb[k]; d = r['vs_starting_configuration']; e = r['vs_design_flow_boundary']
    checks = 'all 11' if r['passing'] else ', '.join('fails ' + x.split('__')[-1] for x in r['failed_checks'])
    return f"| {label} | {r['flow']:g} / {r['ratio']:.4f} | {r['net']:.1f} | {d['d_net']:+.1f} | {e['d_net']:+.1f} | {r['unmet']:.1f} | {r['bypass_fraction']:.3f} | {r['nonfuel_lcoe']:.1f} | {d['d_nonfuel_lcoe']:+.1f} | {r['contributions']['tritium']:.1f} | {r['lcoe']:.1f} | {checks} |"
table = '\n'.join(["| Case | Flow kg/s / ratio | Net MW | Δnet vs start | Δnet vs matched 2,500 | Unmet MW | Bypass fraction | Nonfuel LCOE | Δnonfuel vs start | Tritium term | Total LCOE | Checks |", "|---|---|---|---|---|---|---|---|---|---|---|---|",
 row('ir-f2500-r1.5183', 'starting configuration (C-1 design point)'), row('ir-boundary-f2500', 'matched exchanger at the design flow (best consistent point)'), row('ir-boundary-f2750', 'matched exchanger at 2,750'), row('ir-boundary-f2250', 'matched exchanger at 2,250'), row('ir-boundary-f3000', 'matched exchanger at 3,000'),
 row('ir-f2500-r1.4300', 'one ladder step inside the boundary at the design flow'), row('ir-f2500-r1.4500', "round 1's screen best at the design flow"), row('ir-f2250-r1.5183', "round 1's best band (superseded)"), row('ir-f2750-r1.3750', "round 1's best band (superseded)"), row('ir-f2500-r1.4250', 'electricity-only best (round 1): not steady'), row('s6-hx75000-f2500-r1.4000', 'S6: 75,000 m² exchanger, 2,500 / 1.40')])
bnd = ' | '.join(f"{rb[k]['flow']:g}: {rb[k]['ratio']:.4f}, {rb[k]['net']:.1f} MW" for k in ['ir-boundary-f2000','ir-boundary-f2250','ir-boundary-f2500','ir-boundary-f2750','ir-boundary-f3000','ir-boundary-f3250','ir-boundary-f3500'])
dS = B['vs_starting_configuration']
text = f"""# Answer: which operating choices improve net electricity and LCOE, and what stops the improvement

Goal `design-study-parameters`, rounds 1–3, 2026-09-26. **Status: answered on sealed evidence with the loop's return requirement enforced.** Two sealed studies: `20260926-design-study-parameters` (272 points on the WI-094 costed assembly; round 1) and `20260926-design-study-parameters-b` (22 points on the WI-095 assembly, which adds an explicit primary-side bypass control and two checks that enforce the loop's return requirement; round 3). Every number below is a stored channel of one of the two records (`results/readout.md` in each) or presentation arithmetic on stored channels; the cycle channels are bit-identical across the two identities. Closure remains the owner's.

## 1. The starting point, in plain terms

The plant is the WI-093 C-1 assembly: the Stellaris helium primary loop delivers 3,301 MW at 773 K (3,126 MW of blanket heat plus 175 MW of loop pump friction) through a 50,000 m² exchanger with 50 MW/K of conductance into the ARIES closed helium Brayton chain (three compressor stages with intercooling, a recuperator of 0.8 effectiveness, one turbine). Its design point is a cycle flow of 2,500 kg/s and an equal stage pressure ratio of 1.518 (overall 3.5). At that point the cycle removes all the heat, the turbine sees 677.5 K, the compressors take 2,451 MW of the turbine's work, the generator makes 666.9 MW gross, and after the loop pumps (175.3 MW) and the ARIES auxiliary register (65 MW electric: 40 heating wall-plug, 10 cryogenic, 5 fuel, 5 control, 5 other) the plant nets {S['net']:.1f} MW. This is the C-1 assembly's own design point; the 423.1 MW ARIES integrated nominal of earlier goals is a different configuration (the ARIES plant on its own loops) and is not this case.

The loop holds its blanket inlet at 573 K and requires the exchanger to return the helium to the circulator at 561.9 K. At the design point the exchanger has 16 % more capability than the duty it is given (3,836.5 against 3,301.2 MW), so left uncontrolled it would return the helium 49 K too cold; the completed model (§ 5) shows that the design point is a consistent operating point only if 31 % of the loop flow bypasses the exchanger. Its cost of electricity has two parts worth keeping apart: the nonfuel part, {S['nonfuel_lcoe']:.1f} USD2004/MWh (capital {S['contributions']['capital']:.1f}, O&M {S['contributions']['om']:.1f}, the rest {S['nonfuel_lcoe']-S['contributions']['capital']-S['contributions']['om']:.1f}), and the fuel part, {S['contributions']['tritium']:.1f} USD/MWh of purchased tritium under the no-breeding-credit convention at an assumed 30 MUSD/kg; the total is {S['lcoe']:.1f}. The nonfuel figure is conditional on an ARIES-scope rest-of-plant constant (2,158 MUSD, `[ASSUMED]`); the fuel figure is a convention. Paired deltas at equal fuel are the comparison (`evidence/comparison-contract.md` § 6).

## 2. What improves net electricity and the cost of electricity

Lowering the stage ratio at fixed flow raises net electricity until the exchanger can no longer take all the heat; raising the flow lowers the ratio at which that happens. With the loop's return requirement enforced, the consistent operating points on the existing equipment are the points where the exchanger is exactly matched to its duty (no bypass, all heat removed), one ratio per flow, and every point above that ratio is consistent with a bypass. The round-3 study located the matched point at each flow and re-evaluated round 1's leading points with their bypass fractions:

{table}

The best point that satisfies the completed model on the existing inventory is the matched exchanger at the design flow: 2,500 kg/s at stage ratio 1.4273 (overall 2.9), {B['net']:.1f} MW. Against the starting configuration that is +{dS['d_net']:.0f} MW (+{dS['d_net']/S['net']:.0%}) of net electricity from operating choices alone with the existing equipment, the annual energy 3.18 → 4.62 TWh, and the nonfuel cost of electricity {S['nonfuel_lcoe']:.0f} → {B['nonfuel_lcoe']:.0f} USD/MWh ({dS['d_nonfuel_lcoe']:+.0f}, −31 %), because every nonfuel cost is a constant of the sweep spread over more electricity. The tritium term falls by {-dS['d_tritium_lcoe']:.0f} USD/MWh for the same reason and dominates the total change only because the assumed tritium price dominates the total; the ranking of operating points does not depend on it. Round 1's best band (2,250 / 1.518 and 2,750 / 1.375, about 595 MW) was a grid-resolution artifact 20–23 MW below the matched point; round 1's "+171 MW" is superseded.

Along the matched-exchanger boundary the net peaks at the design flow and falls by 86 MW across the window ({bnd}); the flow choice matters through the turbine inlet and the compressor work even when the ratio is set by the exchanger.

## 3. What stops the improvement

**The thermal limit is heat removal at the exchanger, and with the return requirement enforced it is not a boundary the operating point can sit beyond but the locus it must sit on.** As the ratio falls, the compressor exit cools less and the recuperator returns more heat, so the helium arriving at the heater is hotter (472 K at the matched point, 423 K at the design point); the 773 K source can only deliver what 50 MW/K of conductance carries across that temperature difference. Below the matched ratio, source heat goes unremoved (7.8 MW at 2,500 / 1.425, 5.2–32.6 MW at 2,250 / 1.505–1.515) and the loop's return runs too warm; above it, the exchanger's excess capability must be absorbed by a bypass that grows with the ratio (0.019 at 1.430, 0.107 at 1.445, 0.130 at 1.45, 0.311 at the design ratio). The electricity-only best of round 1 (2,500 / 1.425, 620.0 MW) lies 0.0023 in ratio beyond the matched point and is not a steady operating point.

**Above the band, the equipment limit is the compressor rating**, then net itself (round 1: the 3,200 MW compressor binds at 2,250 / 1.80, 2,500 / 1.80, 2,750 / 1.70 and 3,000 / 1.60; from 3,250 kg/s upward the net goes nonpositive first).

**Exchanger capacity limits further improvement.** With the existing 50,000 m² exchanger the passing net cannot exceed the matched point's {B['net']:.1f} MW; a 75,000 m² exchanger (priced 87.5 MUSD through the same purchase law, +29.2 MUSD, not extrapolated) reaches {S6['net']:.1f} MW at 2,500 / 1.40 with a 3.9 % bypass, {S6['net']-B['net']:.0f} MW above the matched point; its price adds 0.95 USD/MWh to the capital contribution at unchanged net (round 1, the S6 case at the starting point), and its own matched point was not solved.

**The ARIES-selected inventory I-A supports none of it** (round 1: the 1,500 MW helium-duty package is 1,801 MW short of the constant duty, the 1,600 MW compressor is exceeded at 79 of 100 points; round 3: the same at the starting point with the same 31 % bypass). Hardware is selected before the sweep and priced from what was selected (MR-7); no point was resized.

## 4. Under the declared uncertainties (round 1, unchanged on the completed model's cycle side)

| Sensitivity | Effect at the anchors | Does the best point move? |
|---|---|---|
| S1 machine efficiency (compressor 0.85 / 0.92, turbine 0.90 / 0.95) | net −95 to −108 / +66 to +75; −42 to −92 / +26 to +59 MW | yes, by about one grid step of the matched ratio: round 1's 2,250 / 1.5183 fails heat removal at compressor 0.85 (2.8 MW unmet) and turbine 0.90 (70.7 MW); 2,500 / 1.45 (13 % bypass at nominal efficiency) passes under every level |
| S2 auxiliaries (register ×0.5 / ×1.5; wired fuel term; Stellaris-equivalent register) | net +32.5 / −32.5; −1.8; −50.2 MW at every anchor; total LCOE −110 to +208 | no; a constant cannot reorder points |
| S3 loop pump law (dp ×0.5 / ×2) | ×0.5: +25 to +58 MW; ×2: −50 MW at the design point but −126 to −178 MW and 103–224 MW unmet at the boundary anchors | yes: the doubled friction heat cannot be removed at the matched point, so the locus retreats toward the design ratio |
| S4 prices (equipment ×0.5 / ×1.5; rest-of-plant ×0.5 / ×2) | nonfuel LCOE ∓9 to 13; −25 to −35 / +50 to +70 USD/MWh | no |
| S5 fuel convention (feed 100 kg/year, 30 MUSD/year service) | total LCOE 446 at 2,250 / 1.5183, 624 at the start (−668 / −935); nonfuel unchanged | no |
| S6 exchanger 75,000 m² (+29 MUSD) | {S6['net']:.1f} MW at 2,500 / 1.40 with 3.9 % bypass | yes, up by {S6['net']-B['net']:.0f} MW |

The sensitivity cases' bypass fractions were not computed (round 1 ran before WI-095); their heat-removal verdicts are the completed model's feasibility, unchanged.

## 5. The helium return condition, enforced

The loop definition states the requirement (the exchanger must return the helium at the circulator inlet temperature so that the held 300 °C blanket inlet holds) and no assembly checked it before WI-095. WI-095 chose the arrangement and enforced it: an explicit primary-side bypass control that routes the fraction of loop flow the exchanger does not need around it and mixes it back, with the exchanger's performance at the reduced flow computed from its own effectiveness-NTU form (the bypass lowers the exchanger's effectiveness, which is why the solved fractions are larger than round 2's mixing estimate: 31.1 % at the design point against the 18.8 % estimated, 13.0 % against 6.0 % at 2,500 / 1.45); two checks, 'Return Condition Held' at the root-solve closure (1e-6 K against residuals of order 1e-11 K; the physical deficit when infeasible) and 'Bypass Within Limit' against a declared maximum; both fresh-reviewed and integrated, with every existing channel of the assembly replaying bit for bit. Consistent operating settings on the cycle side (no bypass) are the same model's zero-bypass family, the matched-exchanger points of § 2, located on the package-owned oracle and executed with the located ratio as a chosen input.

Under either arrangement the best point is the same, the matched exchanger at the design flow, and the residual there is 1e-11 K. The arrangements differ in what they say about the starting configuration: with a bypass it is a consistent operating point at 31 % bypass; without one it is not an operating point. 'Bypass Within Limit' is vacuous at the declared maximum of 1.0: whether a 31 % bypass is acceptable at the design point is a design limit the owner has not declared, and the best point needs none. Not modeled and disclosed: the bypass's own pressure loss (which would feed the circulator's inlet temperature through the loop's pressure-drop law), its valve hardware and cost; the closure's uncontrolled return and hot-side temperatures are reported as what they are.

## 6. How flow and ratio should be chosen together

At each flow, choose the ratio at which the exchanger is exactly matched to the loop's duty (all heat removed, no bypass): that ratio falls with flow (1.651 at 2,000 kg/s, 1.517 at 2,250, 1.427 at 2,500, 1.363 at 2,750, 1.314 at 3,000, 1.276 at 3,250, 1.244 at 3,500). Then choose the flow where that point nets the most: the design flow, 2,500 kg/s, at {B['net']:.1f} MW, with 2,750 kg/s within 3 MW; the design ratio of 1.518 at the design flow wastes exchanger capability that only a 31 % bypass can absorb. Operating one ladder step inside the matched point (2,500 / 1.430, {L['net']:.1f} MW, 1.9 % bypass) costs 5 MW and buys a margin against the boundary; 2,500 / 1.45 (575.6 MW, 13 % bypass) is the point round 1 showed robust under every efficiency and auxiliary level. Rankings between flows far from 2,500 kg/s are model exploration at fixed efficiency (contract § 8 a). Further improvement beyond the matched point is limited by exchanger capacity: a 50 % larger exchanger adds about {S6['net']-B['net']:.0f} MW at 2,500 / 1.40 for 0.95 USD/MWh of added capital contribution; the compressor rating is the next limit.

## 7. What this answer does not claim

Fixed isentropic efficiencies at every flow and ratio (no off-design map; S1 bounds the first-order effect); the ARIES auxiliary register on a Stellaris loop (S2 bounds it, including the 13 MW of heat-rejection pumping the balance omits); the Stellaris pump relation as a hydraulic model (S3); an ARIES-scope rest-of-plant (S4); unsupported breeding (S5); the bypass's loss, hardware and cost (§ 5); the S6 inventory's own matched point; anything below ratio 1.20 at 4,000 kg/s, where the matched point lies outside the declared window. No point is qualified as a design by passing the checks. Offered, not opened: an owner-declared bypass limit; the exchanger area as a chosen design variable with its own screen; off-design machine maps.

## 8. Evidence and replay

- Records (sealed): `exploration/costed_loop_brayton/studies/20260926-design-study-parameters/` (round 1: `record.md` with the seal addendum, `snapshot.json` `d84c7dac…`, `results/readout.md`, `results/figures/`) and `…/20260926-design-study-parameters-b/` (round 3: `record.md`, `snapshot.json` `f0f72112…`, `results/readout.md`, `axis-plan.json` with the boundary solve).
- The model increment: `work/active/WI-095_loop-return-control/` (`spec.md`, `design.md`, `report.md`); `models/library/analyses/loop_return_control.sysml`; the reviews `evidence/design-review-r3.md`, `evidence/implementation-review-r3.md`; the seam `evidence/integration-t010/`.
- Contract, rulings and directions: `evidence/comparison-contract.md` (v2), `evidence/owner-ruling-g001.md`, `evidence/owner-direction-round3.md`; the earlier reviews under `evidence/` (contract, design, implementation, round 1, round 2).
- Candidate ledger: `candidate-ledger.md`. Proposed write-up passage: `proposed-passage.md`.
- Replay: each record's `results/execution-context.json` lists its commands, run from the repository root through `.codex-test/run` into a scratch record directory (never into a committed one); the round-3 `prepare` composes, scans and solves the boundary family on the oracle, `baseline` and `preflight.py gates` gate, `execute` needs the integration return, `verify` re-checks the store, `return_control_reporting.py` regenerates the readout.
"""
(G / 'answer.md').write_text(text)
led = (G / 'candidate-ledger.md').read_text().replace("# Candidate ledger: design-study-parameters, rounds 1–2", "# Candidate ledger: design-study-parameters, rounds 1–3")
extra = [('ir-f2500-r1.4300','ladder','consistent with 1.9 % bypass'),('ir-f2500-r1.4350','ladder','5.2 % bypass'),('ir-f2500-r1.4400','ladder','8.1 % bypass'),('ir-f2500-r1.4450','ladder','10.7 % bypass'),('ir-f2500-r1.4500',"round 1's screen best",'13.0 % bypass; robust under S1/S2'),('ir-f2250-r1.5183',"round 1's best band",'1.0 % bypass; superseded as best'),('ir-f2750-r1.3750',"round 1's best band",'8.0 % bypass; superseded as best'),('ir-f3000-r1.3250','third (round 1)','7.5 % bypass'),('ir-f2500-r1.4250','electricity-only best','infeasible: heat removal and return condition violated'),('ir-f2250-r1.5050','ladder','infeasible'),('ir-f2250-r1.5100','ladder','infeasible'),('ir-f2250-r1.5150','ladder','infeasible'),('s6-hx75000-f2500-r1.4000','S6 alternative','3.9 % bypass; separate inventory'),('ia-f2500-r1.5183','I-A starting point','ratings violated; 31 % bypass')]
def lrow(k, lab, st):
    r = rb[k]; v = '11 of 11' if r['passing'] else ', '.join(x.split('__')[-1] + ' violated' for x in r['failed_checks'])
    return f"| {lab} | `{k}` | {r['flow']:g} / {r['ratio']:.4f} | {r['net']:.3f} | {r['bypass_fraction']:.4f} | {r['return_residual_K']:+.1e} | {v} | {r['nonfuel_lcoe']:.2f} / {r['lcoe']:.2f} | {st} |"
led += "\n## Round 3 (the completed loop model, study `20260926-design-study-parameters-b`, identity `20260926-design-study-parameters-b:<candidate>`)\n\n| Candidate | Case | Flow / ratio | Net MW | Bypass fraction | Return residual K | Verdicts | Nonfuel / total LCOE | Standing |\n|---|---|---|---|---|---|---|---|---|\n"
led += lrow('ir-f2500-r1.5183', 'starting configuration', 'consistent only with 31 % bypass (B); not an operating point under A') + '\n'
led += lrow('ir-boundary-f2500', 'best consistent point', 'the matched exchanger at the design flow; best under A and B') + '\n'
led += '\n'.join(lrow(k, 'matched exchanger', 'arrangement A family') for k in ['ir-boundary-f2000','ir-boundary-f2250','ir-boundary-f2750','ir-boundary-f3000','ir-boundary-f3250','ir-boundary-f3500']) + '\n'
led += '\n'.join(lrow(k, lab, st) for k, lab, st in extra) + "\n\nThe round-2 bypass-equivalent fractions quoted above (18.8 %, 0.3 %, 3.9 %, 6.0 %, 1.4 %) were a mixing estimate; the solved control settings are the round-3 column.\n"
(G / 'candidate-ledger.md').write_text(led)
print('answer and ledger written')
