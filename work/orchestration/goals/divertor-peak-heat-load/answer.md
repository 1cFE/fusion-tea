# Divertor peak heat load

[AGENT] Implementation and the frozen study at `ac1b529b` pass independent review. The entering peak calculation is supported as a conditional screen for non-radiated target heat. Its area-scaled diagnostic is also a peak, with an additional unverified assumption about how the footprint grows with radius. WI-065 exposes the power destinations and the area implied by the source profile. It preserves the peak normalization, the 10 MW/m² limit and every existing plant constraint.

## Definitions and power balance

[INHERITED: original Stellaris section 2.6] The source's high transport case sends 50 MW of non-radiated power toward the divertor, captures 99% and peaks at 9.5 MW/m². Its lower transport case captures 97% and peaks at 5 MW/m² at the same incoming power. These are source calculation cases for the represented resonant island divertor. Their peaks already include capture and spatial concentration. Multiplying the normalized peak by capture again would count that effect twice. Original pages and the new island-divertor geometry source were independently checked in [source review](evidence/source-review.md); the full reconstruction is in [entering account](evidence/entering-account.md).

[AGENT DERIVATION] Let H be absorbed plasma heating, C core radiation, F the total radiation fraction and c the target capture fraction. The explicit account is:

```text
Power leaving the confined plasma: S = H − C
Additional edge radiation:         E = F H − C
Non-radiated power before capture: N = H − F H
Deposited non-radiated target heat: D = c N
Uncaptured non-radiated heat:       U = N − D
Conservation:                      H = C + E + D + U
```

[AGENT] H includes retained alpha heating and operating auxiliary heating. Plant thermal power includes total alpha energy, multiplied neutron power, operating auxiliary heat and recovered pumping work. Radiation and target deposition partition existing heat; they do not add thermal generation. Unretained alpha and the inherited small difference between rounded alpha fractions remain outside H. The target account does not create a separate coolant loop or change primary-loop capacity.

[AGENT] Negative required operating heating remains an existing failed-burn diagnostic. The new account-valid flag is zero for that condition or for negative inferred edge radiation. Such points remain in the record with their failures; signed diagnostic values do not represent physical negative heating or radiation.

## Geometry, sharing and concentration

[AGENT DERIVATION] For target groups j, a physically specified account would use deposited shares s_j, effective wetted areas A_wet,j and spatial peaking factors k_j:

```text
sum(s_j) = 1
D_j = s_j D
q_average,j = D_j / A_wet,j
q_peak,j = k_j q_average,j
q_global_peak = max(q_peak,j)
```

[AGENT] A plate's geometric surface area can include unwetted regions. It therefore cannot substitute for A_wet. The source does not supply the group shares, integrated wetted areas or separate concentration factors needed to execute these equations. A quoted strike width alone does not establish total strike length. The reported source profile already includes its transport and target geometry; adding independent flux expansion, incidence-angle, multiplicity or peaking corrections would need evidence that they have not already been included.

[AGENT DERIVATION] What the source does identify is the peak-equivalent area `A_eq = c_ref N_ref/q_ref`: 5.2105263158 m² for the high case and 9.7 m² for the low case. This is integrated deposited power divided by the global peak. For a defined combined wetted region it equals `A_wet/k_peak`. It does not identify those two quantities separately, and it is not physical target surface area. Average surface flux and per-target deposition consequently remain quantified evidence gaps rather than invented outputs.

[AGENT] The live peak remains `q_ref N/N_ref`, or `D/A_eq` for its active source pair. This transfers the reference deposition shape at fixed geometry and transport assumptions while scaling its amplitude with incoming power. It is a linear extrapolation of source cases, not an edge-transport prediction. Changing machine radius changes plasma heating through existing plant equations. The area-scaled diagnostic additionally multiplies the peak by `R_ref/R`, assuming footprint length grows with major radius at held width and concentration. No admitted source establishes that transfer for Stellaris. It remains a conditional diagnostic and does not govern acceptance.

[AGENT] The model now exposes total and edge radiation, deposited and uncaptured non-radiated power, peak-equivalent area and its defined flag, edge-radiation fraction defined status, and power-account validity. Existing incoming power, both peaks and peak margin remain available. See the [native ledger](../../../../models/library/analyses/mfe_divertor_heat.sysml), [plant bindings](../../../../models/designs/stellarator_09/stellarator_plant.sysml) and [independent oracle](../../../../exploration/stellarator_e2e/verify_stellaris.py).

## What changes can be evaluated

| Change | Model response | Physical and cost limit |
|---|---|---|
| Machine radius or current | Plasma power, magnets, fit, plant heat, cost and loop demand respond through existing equations. | Divertor deposition still assumes the transferred source profile; target accommodation is not established. |
| Paired low source profile | Peak falls; capture changes from 99% to 97%, increasing uncaptured heat at fixed incoming power. | This is a transport sensitivity, not a demonstrated actuator or target design. No control or accommodation cost is represented. |
| Total radiation fraction at fixed plasma state | Non-radiated target load falls as radiation increases. Total and edge radiation diagnostics increase. | Total primary-loop source heat and target capital cost do not fall. Radiation control and target radiation deposition remain missing. |
| Larger physical wetted area | No independently supported executable lever. | Requires configuration-specific footprint, target accommodation, breeding interception, cooling, support, maintenance and cost evidence. |

[AGENT] Current divertor capital cost scales with the square root of plant thermal power. It does not price target area, profile shaping or radiation control. Conditional heat-load reductions therefore cannot be treated as free design improvements. Original target-layout discussion and the admitted geometry research link deposition changes to wall interception and engineering limits; neither establishes a transferable major-radius law. See [external research](evidence/external-research.md).

[AGENT] A passing divertor predicate covers non-radiated transport under an active supported profile and valid account. Surface deposition of radiation is absent. Transients, erosion, lifetime and cooling qualification are also outside this model. Passing this screen does not establish acceptable total surface heat or combined plant feasibility.

## Bounded study result

[AGENT] All 27 native diagnostic cases complete; none passes all 20 predicates. The sample separates five matched controls, paired source-profile changes, radiation changes and six radius perturbations. It also retains a dedicated failed-burn control. Both that control and the R = 12.9 m perturbation of the informative rejection have invalid power accounts; neither supports a physical heat-load gain. Full evidence is in the [study record](../../../../exploration/stellarator_e2e/studies/20260915-divertor-heat-account/record.md).

[AGENT] Default peaks and predicates are unchanged from the entering package. The plant reference has H = 553.570608 MW and incoming non-radiated power = 55.357061 MW, above the source normalization of 500/50 MW. That existing power difference explains its 10.517842 MW/m² peak; no coefficient was fitted to recover either 9.5 or 10 MW/m². The low profile and 92% radiation columns below are separate conditional sensitivities, not combined changes. Every listed case remains rejected by at least one other plant constraint even when its divertor screen passes.

| Matched case | Default peak, MW/m² | Default divertor | Other default failures | Low profile peak | 92% radiation peak |
|---|---:|---|---|---:|---:|
| Reference | 10.517842 | Fail | Conductor current, pack fit | 5.535706 | 8.414273 |
| Current-sized reference | 10.517842 | Fail | Pack fit | 5.535706 | 8.414273 |
| Allocated current-sized reference | 10.517842 | Fail | Peak field | 5.535706 | 8.414273 |
| `r-12.7-1.35-1.62e+07` | 9.603709 | Pass | Peak field | 5.054583 | 7.682967 |
| `r-13.1-1.45-1.54e+07` | 11.156873 | Fail | Primary-loop capacity | 5.872039 | 8.925499 |

[AGENT] At the informative last case, H = 587.203858 MW, S = 323.702408 MW, edge radiation = 264.982022 MW, incoming non-radiated power = 58.720386 MW, deposited power = 58.133182 MW and uncaptured power = 0.587204 MW. The peak margin is −1.156873 MW/m². Its separate area-scaled peak is 10.816205 MW/m², also above the limit. Required primary-loop flow remains 245.272965 kg/s per loop against 225.077778 kg/s capacity; changing profile or radiation does not resize it.

[AGENT] Radius perturbations expose coupled consequences rather than a free area benefit. At the reference, R = 12.5/12.9 m gives peaks of 10.089460/10.959702 MW/m². Around the field-only rejection, R = 12.5/12.9 m gives 9.224486/9.994830 MW/m², both still field-rejected. Around the informative rejection, R = 12.9 m is burn-invalid, while R = 13.3 m gives 11.601348 MW/m² and also fails wall load. None establishes a feasible geometry option or a transferable footprint law. The earlier joint study's bounded negative conclusion remains intact.

## Necessary reductions, not demonstrated options

[AGENT DERIVATION] Holding incoming power and capture fixed, passing requires an equivalent-area factor of at least q/10. Holding the profile fixed instead requires a target-power reduction of at least 1−10/q. At held H and a starting total radiation fraction of 90%, the conditional threshold is F = 1−0.1×10/q.

| Case | Required target-power reduction | Required A_eq increase at fixed deposited power | Conditional total radiation threshold |
|---|---:|---:|---:|
| Reference and its two sizing controls | 4.9235% | 5.1784% | 90.49235% |
| Informative joint rejection | 10.3692% | 11.5687% | 91.03692% |

[AGENT] These are alternative requirements under held assumptions, not additive improvements. A_eq cannot be enlarged independently in the supported model. A real area or concentration change needs configuration-specific evidence; a radiation change needs control, deposition and accommodation evidence. The lower source profile is evidence of a calculated sensitivity, not evidence that the plant can achieve it. The 10 MW/m² acceptance limit remains unchanged.

## Verification

[AGENT] Native/generated/independent-oracle evidence and seven exact entering-native controls are in the [WI-065 audit](../../../active/WI-065_divertor-deposited-power-and-peak-area-account/audit.md). Source/interface and implementation independent reviews pass. Component tests cover conservation, physical responses, source pairs, domain boundaries, undefined ratios and invalid arithmetic. Signed failed-burn cases retain all old outputs and responses. Native integration passes all ten gates at pin `6e427038e8515501e9c42c39823f85e3b0bcbd9f54f830b2779a792851f02551`.

[AGENT] Sixteen retained native channels remain outside independent oracle coverage. Inherited static L2/L6 limitations, the omitted integration read-set check and the exact-current-boundary native/oracle sign difference remain explicit in the audit. Executable agreement does not imply clean full static validation or physical qualification. The frozen native study compares all 6,102 mapped scalar values and 540 exact predicate verdicts with the independent oracle, with zero mismatches. Its isolated entering-oracle comparison preserves all 5,886 existing mapped scalars and every sampled predicate. Separate stratified verification and native-store custody checks pass. Thirteen cases pass the valid-account divertor screen; none passes all predicates.

[AGENT] Record/template/goal checks pass 71. The frozen study retains both native SQLite stores, 28 content-addressed evidence records and 184 hash-checked snapshot artifacts. The [final independent review](evidence/final-review.md) verifies the frozen artifact hashes and store joins, independently replays every sampled current and entering-oracle comparison, and accepts the bounded answer. Technical work is complete; formal goal closure and native item archival remain owner-held.
