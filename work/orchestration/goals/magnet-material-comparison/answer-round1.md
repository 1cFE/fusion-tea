# REBCO versus Nb₃Sn magnet subsystem at matched duty

Round 1 answer, 2026-09-29. Every number below is read from the sealed study `exploration/magnet_materials/studies/20260929-magnet-material-comparison/` (record.md, `results/cases.csv`, `results/summary.json`; sealed at `7836424ca`) against the released comparison contract r3 ([evidence/comparison-contract.md](evidence/comparison-contract.md)). Case ids are given where a single point is quoted. Money is USD 2021; "annualized" is 0.08 × capital plus electricity at 60 USD/MWh and 0.8 availability, for the winding plus its refrigeration only (contract § 7).

[AGENT] **At matched duty where both conductors are supported and fit the envelope (8–11 T on the EU DEMO TF envelope under common construction), a supplied Nb₃Sn winding at 4.5 K is the cheaper subsystem under every checked assumption that leaves the pair rankable, except the REBCO price.** At the reference point (anchor D, 10 T, common construction, reference offers: `D-10T-common-P-reference-none-reference-reference`) Nb₃Sn costs 48.5 M USD/yr and REBCO 286.1 M USD/yr, a difference of 237.6 M USD/yr. REBCO's refrigeration advantage is real (cold-stage electrical input 1.22 MW against 5.80 MW) and worth about 3.6 M USD/yr; it is 1.5 % of the annualized conductor purchase difference (3.46 G USD of tape at 80 USD/m against 0.44 G USD of strand at 8 USD/m, 241 M USD/yr at 0.08). The two subsystems cost the same when REBCO tape costs **11.25 USD/m** (31.7 USD per kA·m); across the 592 rankable pairs where Nb₃Sn is inside its law's supported band the break-even price runs 6.62–23.13 USD/m, median 11.13 (6.62–24.63, median 11.25, over all 610 rankable pairs; the only values above 23.13 are two 14 T law-only pairs under common-C). Only the 10 USD/m volume-price scenario makes Nb₃Sn dearer, and only at 9–11 T on anchor D (12 of 610 pairs).

[AGENT] **The preference is set by conductor price and by which pairs can be ranked at all, not by physics inside the supported range.** Three assumption groups matter. (1) The REBCO tape price: 80 USD/m market gives the headline, 30 USD/m target still leaves REBCO dearer by 64.8 M USD/yr at the reference point, 10 USD/m flips the sign. (2) The Nb₃Sn price and its manufacturing allowance move the break-even by −30 % to +63 %. (3) Conductor-law choices that decide whether fixed Nb₃Sn hardware still passes: −0.6 % intrinsic strain and the two lower strand grades fail the reference offer's temperature margin, so the pair is unranked until more strands are supplied, which raises the break-even to 13.1–18.4 USD/m at the 10 T reference point. The cryogenic and capital-recovery assumptions move the break-even by less than 7 %.

[AGENT] **What the comparison establishes:** under consistent accounting, both materials meet the same duty, fit the same envelope and pass every check from 8 to 11 T on anchor D with common construction; Nb₃Sn needs 0.97–1.48 times as many element-metres and 2.3–3.5 times the conductor mass over 8–11 T, but its strand is ten times cheaper per metre; refrigeration is a second-order cost at this duty. **What it does not establish:** a fit or field limit for Nb₃Sn (the 12 T fit failure on anchor D is decided by a calibrated pack-construction rule, not by the conductor law), anything about a full plant, a stellarator's plasma, or Nb₃Sn on the 24.9 T Stellaris reference. Above 14 T only REBCO is supported; on the Stellaris envelope neither material fits under the common CICC rule (common-P), and ranking is possible only under the compact rule C, which the contract labels hypothetical for Nb₃Sn (protection at that copper level is not evaluated).

Independent coverage: the model was implemented from a reviewed design and checked by a separately written oracle (0 disagreements across 2310 stored points, 2832 declared cases); the contract's source values were checked against original tables and figures ([evidence/check-nb3sn.md](evidence/check-nb3sn.md), [evidence/check-rebco-cryo-cost.md](evidence/check-rebco-cryo-cost.md), [evidence/contract-review.md](evidence/contract-review.md)). The final independent review of this answer is at [evidence/final-review.md](evidence/final-review.md).

## What was compared

[AGENT] Two conductor definitions with their own laws, temperatures and validity domains (WI-099, `models/library/analyses/magnet_conductor_alternatives.sysml`, `models/designs/magnet_materials/magnet_subsystem.sysml`):

- **Nb₃Sn** at 4.5 K supply (5.2 K conductor after the 0.7 K nuclear rise): ITER-form strand critical-current law in field, temperature and strain (Tsui & Hampshire form, WST TFCN5-6 production median set, 0.82 mm strand, 50 % copper, −0.3 % intrinsic strain). Its customary acceptance rule is a current-sharing temperature margin of at least 1.5 K. The law is reported as supported to 12 T, edge at 13 T, law-only at 14 T and unsupported from 16 T.
- **REBCO** at 20 K supply (20.7 K conductor): 4 mm × 56 µm tape with the digitized Molodyk 20 K field shape (198 A at 20 T anchor, 8–20 T), an exponential temperature law (T* 22 K) and a 0.90 cabling/handling degradation. Its customary acceptance rule is an operating fraction of at most 0.80. Supported at every evaluated point.

[AGENT] The duty is set by an anchor envelope, and the turn current scales linearly with field from the anchor's own operating point (contract § 2):

- **Anchor D (primary):** EU DEMO TF winding pack, 16 coils × 142 turns, 3751.1 mm² and 55.6 m per turn, 104.95 kA at 12.04 T. At 10 T the turn current is 87.17 kA and the conductor length 126.3 km.
- **Anchor S (secondary):** Stellaris, 48 coils × 308 turns, 420.8 mm² and 21.753 m per turn, 50 kA at 24.9 T.

[AGENT] Both materials are evaluated as **supplied** windings (MR-7): the element count, the copper and steel areas and the installed refrigerator rating are inputs. The declared offer policy proposes the smallest element count meeting the acceptance rule at each case and the smallest listed refrigerator covering the load; insufficient (⌊0.9 n⌋, next-lower refrigerator) and generous (⌈1.2 n⌉) offers are evaluated alongside so the checks are seen to fail and pass. Construction rules: **common-P** (EU DEMO layer-1 calibrated cable-in-conduit for both), **native** (P for Nb₃Sn, the Stellaris-derived compact rule C for REBCO), **common-C** (C for both). Five checks per material: acceptance (which requires a supported conductor status), fit in the envelope, copper allowance, steel allowance and refrigerator capacity; a pair is rankable only when both materials pass all five (contract § 8).

## Results at reference offers

Anchor D, common-P, reference rule family, reference offers and refrigerators (`D-{B}T-common-P-reference-none-reference-reference`). The other tables and every figure are in [evidence/figures/](evidence/figures/).

| B, T | Nb₃Sn strands | Nb₃Sn fit margin, mm² | Nb₃Sn Tcs − T, K | Nb₃Sn cold-stage MW | REBCO tapes | REBCO fit margin, mm² | REBCO I/Ic | REBCO cold-stage MW | Rankable | REBCO − Nb₃Sn, M USD/yr | Break-even, USD/m |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--:|---:|---:|
| 8 | 232 | +1676 | 1.51 | 5.46 | 240 | +1717 | 0.798 | 1.15 | yes | +171.9 | 9.14 |
| 9 | 320 | +1279 | 1.51 | 5.62 | 289 | +1349 | 0.799 | 1.18 | yes | +204.3 | 10.03 |
| 10 | 438 | +842 | 1.51 | 5.80 | 342 | +955 | 0.798 | 1.22 | yes | +237.6 | 11.25 |
| 11 | 599 | +360 | 1.51 | 5.31 | 404 | +534 | 0.799 | 1.12 | yes | +274.3 | 12.82 |
| 12 | 822 | −179 | 1.50 | 5.48 | 471 | +88 | 0.799 | 1.15 | no (Nb₃Sn fit) | (+310.4) | (14.78) |
| 13 | 1139 | −788 | 1.50 (edge) | 5.66 | 546 | −385 | 0.800 | 1.19 | no (fit, both) | (+345.5) | (17.39) |

Parenthesized values are recorded for the pair but carry no ranking: a non-fitting design has no cost ranking and no break-even price (contract §§ 2, 8).

[AGENT] Reading the table:

- **Current margin.** Both reference offers sit at their rule by construction: Nb₃Sn at 1.51 K temperature margin (operating fraction 0.735 at 10 T), REBCO at 0.798 of Ic (temperature margin 4.96 K at 10 T). Under a common rule the counts move (both-temperature: REBCO 293 tapes, break-even 13.13 USD/m; both-fraction: Nb₃Sn 403 strands, break-even 10.43 USD/m) but the preference does not.
- **Conductor inventory.** At 10 T: Nb₃Sn 55.3 million strand-metres (260 t), REBCO 43.2 million tape-metres (86 t); superconductor purchase 442.6 M against 3,456 M USD. Copper and steel (16–17 M USD each side) are the same order for both.
- **Winding fit.** In the 3751.1 mm² DEMO envelope, Nb₃Sn fits to 11 T and misses by 179 mm² at 12 T; REBCO fits to 12 T under common-P and at every field under its native construction (≥ +2237 mm²). Under common-C both fit through 14 T. On the Stellaris envelope (420.8 mm²) neither fits under common-P at any field (Nb₃Sn −57 to −625 mm², REBCO −48 to −532 mm²); both fit under common-C (hypothetical for Nb₃Sn, contract § 4), where 36 of the 72 declared pairs at 8–13 T are rankable (every reference and generous element offer with the reference refrigerator; the insufficient element and refrigerator offers fail by design) and the break-even at the reference offers runs 8.81–17.31 USD/m, the same band as anchor D (8.32–20.20 over all 36).
- **Refrigeration.** The cold loads are almost equal (29.9 kW at 4.5 K against 29.5 kW at 20 K at 10 T; nuclear heating 16.8 kW dominates both) and both take the 30 kW listed refrigerator. The electrical input differs by the Carnot ratio: 5.80 MW against 1.22 MW at the cold stage, on top of a common 16.2 MW for the 77 K shield and lead intercept; totals 22.0 and 17.5 MW. Refrigerator capital 32.3 M against 11.8 M USD. From 11 T on anchor D the listed rating is 50 kW, outside the Green cost-fit range; the record flags this (`green_extrapolated`).
- **Subsystem cost.** Annualized 48.5 M (Nb₃Sn) against 286.1 M USD/yr (REBCO) at 10 T; the gap grows with field (171.9 → 274.3 M USD/yr from 8 to 11 T) because both inventories grow while the tape price does not fall.

## Which assumptions determine the preference

[AGENT] One-at-a-time variants at anchor D, 10 T, common-P, reference rule family (`D-10T-common-P-{variant}-…`). "Fixed hardware" re-evaluates the reference offer unchanged; "re-offered" is the policy's new offer under the variant.

| Group | Variant | Effect on fixed hardware | Break-even after re-offer, USD/m (change from 11.25) |
|---|---|---|---:|
| Price | REBCO 30 USD/m (target) | rankable; REBCO dearer by 64.8 M USD/yr | 11.25 (0 %) |
| Price | REBCO 10 USD/m (volume) | rankable; **Nb₃Sn dearer by 4.3 M USD/yr** | 11.25 (0 %) |
| Price | Nb₃Sn 5.4 / 13.5 USD/m | rankable | 7.92 (−30 %) / 18.29 (+63 %) |
| Price | manufacturing allowance, Nb₃Sn only | rankable | 14.55 (+29 %) |
| Nb₃Sn law | −0.6 % intrinsic strain | fails acceptance; unranked | 18.36 (+63 %) |
| Nb₃Sn law | −0.6 % strain with OST TFEU9 / BEAS TFEU10-12 grade | fails acceptance; unranked | 14.51 (+29 %) / 16.47 (+46 %) |
| Nb₃Sn law | BEAS II (Tsui) / BEAS TFEU10-12 grade | fails acceptance; unranked | 13.56 (+21 %) / 13.07 (+16 %) |
| Nb₃Sn law | OST TFEU9 grade; 6.5 K supply rule | rankable | 10.27 (−9 %); 10.76 (−4 %) |
| REBCO law | power-law shape; T* 17 K; degradation 0.80 | fails acceptance; unranked | 9.23 (−18 %); 11.15 (−1 %); 10.02 (−11 %) |
| REBCO law | anchor 225 A; T* 33 K; degradation 0.95 | rankable | 12.78 (+14 %); 11.38 (+1 %); 11.87 (+6 %) |
| Construction | steel base layer 8; no field scaling of steel | steel allowance fails (both materials); unranked | 11.25 (0 %) after re-offer |
| Cryogenics | cold load ×2 | capacity fails (both); unranked | 11.98 (+7 %) after re-offer |
| Cryogenics | cold load ×0.5; 20 K efficiency or capital basis; constant η 0.24; combined unfavourable 20 K | rankable | 10.71–11.48 (−5 % to +2 %) |
| Economics | capital recovery 0.05 / 0.11; electricity 30 / 120 USD/MWh; turn length 45 / 60 m | rankable (60 m: capacity fails until re-offered) | 10.97–11.80 (−3 % to +5 %) |

[AGENT] Three conclusions follow:

1. **The sign is a price question.** At every conductor-law, construction, cryogenic and economic variant the annualized REBCO subsystem is dearer at 80 and at 30 USD/m; the sign flips only at 10 USD/m, and then only at 9–11 T (at 8 T REBCO stays dearer even at 10 USD/m). The whole break-even range (6.62–23.13 USD/m over the 592 supported-status pairs; 6.62–24.63 including the 13–14 T edge and law-only common-C pairs) lies below the 30 USD/m target price and overlaps the Nb₃Sn price band (5.4–13.5 USD/m).
2. **The Nb₃Sn conductor law decides rankability, not the sign.** Strain of −0.6 % or a lower production grade fails acceptance on fixed hardware in 26 of 32 cases per variant (the other 6 are the already-unsupported 16–20 T points), removing all 8 of that variant's rankable pairs until more strands are supplied; supplying them raises the break-even to at most 18.4 USD/m at 10 T and 23.1 USD/m at 11 T (12.8–23.1 over the variant's eight re-offered pairs at 8–11 T). The REBCO-side flips (power-law shape, T* 17 K, degradation 0.80) behave the same way and move the break-even by −18 % to −1 %.
3. **Refrigeration does not move the decision at this duty.** REBCO's 20 K advantage is 4.6 MW of cold-stage electrical input and 20.5 M USD of refrigerator capital, about 3.6 M USD/yr in total; doubling every cold load or changing the efficiency and capital bases moves the break-even by at most 7 %.

## What the comparison does and does not establish

[AGENT] Established, within the declared subsystem and accounting:

- Genuinely different conductor definitions, each with its own law, temperature, acceptance rule and validity domain, evaluated as supplied hardware at the same duty, envelope and construction rule, with consistent cost accounting (goal § Answered when, invariants "Comparison" and "Modeling requirements").
- The requested consequences quantified at every evaluated case: current margin, conductor inventory, fit margin, cold load and cold-stage electrical input, and annualized subsystem cost, with failed, unranked and unsupported statuses retained (2222 of 2832 cases are unranked, each for a named check).
- Sensitivity of the preference to more than two consequential uncertainties (prices, strand grade and strain, REBCO shape and degradation, construction rule, cold load), with the response and the rankability effect of each recorded.
- MR-7 behaviour visible in the record: every insufficient element offer fails acceptance (0 of 144 per material), every insufficient refrigerator fails capacity (0 of 144), generous offers pass wherever the conductor is supported, and nothing is resized by the model.

[AGENT] Not established, and not claimed:

- **No Nb₃Sn field limit.** The 12 T fit failure on anchor D is a consequence of the calibrated common-P construction rule (steel 12.66 mm²/kA scaled with field, copper at 93.4 A/mm², insulation 23.7 %) applied to a strand count chosen at a 1.5 K margin; under the compact rule C the same conductor fits through 16 T. The 13 T "edge" and 14 T "law-only" labels are validity flags of the fitted law, not performance limits.
- **No high-field ranking.** Above 14 T only REBCO is supported; Nb₃Sn is evaluated at 16–20 T so that its unsupported status is recorded, and no pair there is ranked. The Stellaris 24.9 T point is not compared.
- **No reactor, plasma or plant claim.** Scaling turn current with field on a fixed envelope is a subsystem calculation; it says nothing about what a lower-field stellarator would produce, and the economics exclude everything outside the winding and its refrigeration (structure, assembly, quench protection, power supplies, buildings).
- **Partial accounting.** Conductor manufacturing (cabling, jacketing, insulation labour) is 0 by default and shown as a variant; joint counts, terminations and current leads are not priced.
- **Bounded, not measured.** Four inputs are bounded assumptions rather than sourced values, and their effect is bounded by the sensitivity rows above: the anchor D turn length (55.6 m; 45 and 60 m move the break-even by less than 2 %, and 60 m fails capacity until re-offered), the cold-load terms (×0.5/×2: −4 % to +7 %), the 0.7 K nuclear temperature rise applied symmetrically to REBCO (contract § 3), and no layer grading (every turn is sized at peak field for both materials, so real graded packs need less superconductor than either offer; contract § 2). Forced-flow circulator work and helium inventory are excluded, and the exclusion favours Nb₃Sn (contract § 6). A pass is a screening pass: stress, quench beyond the copper allowance, irradiation, AC loss and joint/lead design are not evaluated (contract § 9).
- **Anchor S is rankable only under common-C, which is hypothetical for Nb₃Sn.** Under common-P and native, Nb₃Sn does not fit the 420.8 mm² Stellaris turn area at any field; the compact rule C fits both, but the contract labels it hypothetical for Nb₃Sn because protection at that copper level is not evaluated (contract § 4).

## Deliverables

| Brief item | Where |
|---|---|
| Goal, trail, learnings | `goal.md`, `trail.md`, `learnings.md` in this directory |
| Evidence matrix and data-sufficiency finding | [evidence/evidence-matrix.md](evidence/evidence-matrix.md) |
| Reviewed comparison contract and alternative definitions | [evidence/comparison-contract.md](evidence/comparison-contract.md) r3; review [evidence/contract-review.md](evidence/contract-review.md); WI-099 `work/active/WI-099_magnet-conductor-alternatives/` (spec, design, implementation notes) |
| Sealed, verified study with replay instructions | `exploration/magnet_materials/studies/20260929-magnet-material-comparison/` (record.md § 10–11, 16–17; `execute_study.py`, `verify_all.py`) |
| Results table and figures with data and renderer | [evidence/figures/](evidence/figures/) (`results-table.md`, `data/*.csv`, `render_figures.py`, F1–F6 SVG/PNG, README) |
| Proposed narrative and category assessment | [evidence/proposed-narrative.md](evidence/proposed-narrative.md) |
| Final independent review | [evidence/final-review.md](evidence/final-review.md) |

## Unmet criteria and next evidence

[AGENT] The goal's answer contract is met for the matched range 8–11 T on the DEMO envelope (and 8–13 T on the Stellaris envelope under common-C). Three things would sharpen the answer if the owner wants a second round; none is required to read the result above:

- A **sourced Nb₃Sn winding-pack construction at 12–13 T** (a DEMO or ITER-class CICC at a higher field) would replace the extrapolated common-P steel and copper allowances that decide the 12 T fit. This is the one place where a model assumption, not a price, decides a status.
- A **REBCO conductor-cost basis at the cable level** (manufacturing, joints, leads) would close the partial-accounting gap; the Nb₃Sn-only manufacturing variant already shows it can move the break-even by about 30 %.
- A **refrigerator cost law valid to 50 kW at 4.5 K** would remove the `green_extrapolated` flag at 11 T and above on anchor D; the record shows its effect on the preference is small.

Formal closure of the goal and of WI-099 stays with the owner (goal § Close rule).
