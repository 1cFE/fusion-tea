# Comparison contract: REBCO versus Nb₃Sn at matched duty (r3)

Goal `magnet-material-comparison`, round 1, task T-004. Status: **r3 released for implementation 2026-09-29** (`contract-review.md` § Recheck r3 and design review; `check-nb3sn.md` § Recheck r3; `check-rebco-cryo-cost.md` § Recheck r2), with advisory wording applied after release. r1 is preserved at `comparison-contract-r1.md`. r2 answered the blocking findings B1–B6 and advisories in `contract-review.md` and the corrections in `check-nb3sn.md` and `check-rebco-cryo-cost.md`; r3 answers their `## Recheck r2` sections. Change logs are § 11 and § 12.

**Framing (N4).** The primary matched comparison sits in a Nb₃Sn-native tokamak TF envelope (EU DEMO), not in the Stellaris coil set. REBCO's compactness appears there only through required envelope current density and fit headroom; the Stellaris anchor shows the compact-envelope case. Authority: all choices are `[AGENT]` under the owner-ratified brief (`owner-brief.md`) unless a source is cited. Evidence: `evidence-matrix.md` (v1 + v2), per-class notes in `sources/`, model facts in `binding-audit.md`. Magnitudes quoted from `screen/contract-screen-r2.json` are an unchecked coordinator screen, not results.

## 1. What is compared

Two explicitly supplied winding designs, one per material, that must carry the **same magnetic duty in the same space**: REBCO coated-conductor tape cooled at 20 K, and Nb₃Sn strand in an EU DEMO react-and-wind flat-cable conductor with a 4.5 K helium supply. Each has its own current law, construction and refrigeration temperature. The comparison reports current margin, superconductor and other inventory, winding fit, cold load, refrigerator electrical demand, and subsystem cost within the evaluated categories, and tests which assumptions change the preference.

It is a subsystem screening at a supplied duty. It is not a reactor redesign, not a claim that a lower-field plant keeps its plasma performance, and not a qualified magnet design.

## 2. Duty and geometry boundary

**Excitation varies, geometry does not.** At fixed air-core coil geometry and fixed current distribution, peak field at the conductor is proportional to ampere-turns. Each duty point therefore keeps an anchor's coils, turns, turn length and winding-pack envelope, and sets turn current I = I_ref × B / B_ref. Both materials see the same field, current, conductor length and envelope. No calculation computes field from winding size, so the omitted winding-size field term cannot enter a result **for any design that fits its envelope**. A design that does not fit is not a winding that exists at this duty: it is reported with its required area and required envelope current density, and it gets no cost ranking and no break-even price.

**Two anchors.**

| Anchor | Coils × turns | Reference | Envelope per turn (gross) | Turn length | Role |
|---|---|---|---|---|---|
| **D** — EU DEMO TF (Nb₃Sn-native) | 16 × 142 | 104.95 kA at 12.04 T | 1296 × 411 mm / 142 = 3751.1 mm² | 55.6 m, bounded assumption: ≈1 km layer sections (Demattè p.1) ÷ 18 turns per layer; cross-check ITER 82,249 m / (18 × 134) = 34.1 m × 9.1/6.2 = 50 m; sensitivity 45 and 60 m | **primary matched comparison** |
| **S** — Stellaris coil set (REBCO-native, compact) | 48 × 308 | 50 kA at 24.9 T | 0.36² m² / 308 = 420.8 mm² | 21.75 m (model: 321.6 km / (48 × 308)) | secondary: shows how a compact envelope makes fit a construction verdict |

Stated limits (B1):

- Anchor S's envelope is the nominal pack of the peak-field coil, not a verified space; the model's own 0.30 m radial allocation does not contain it (fit margin −0.12 m at the published design).
- In both anchors every turn is sized at the anchor's peak field (no layer grading). This is conservative and equal for both materials; real graded packs need less superconductor.
- Anchor D's turn length and the anchor D cold-load terms marked below are bounded assumptions. They scale totals, not per-metre comparisons.

**Field points and statuses.** Matched points 8, 9, 10, 11, 12 T; edge point 13 T; REBCO-only extension 14, 16, 18, 20 T (anchor D). Each conductor evaluation carries one status:

- `supported`: inside the conductor law's domain and the sourced design range (Nb₃Sn ≤ 12.2 T; REBCO 8–20 T at 20 K with the measured shape, 5–24 T for the power-law sensitivity).
- `edge`: Nb₃Sn 12.2–13.5 T (the EU DEMO 82.4 kA / 13.5 T design was tested only to 70 kA).
- `law-only`: Nb₃Sn 13.5–14.5 T (inside the law's fitted field range, no fusion design).
- `unsupported`: outside the law's domain (Nb₃Sn above 14.5 T or outside 4.2–12 K or the reversible strain range; REBCO outside its active shape's field range at 20 K or outside 4.2–50 K). Unsupported evaluations are neither pass nor fail and carry no economic ranking.
- A case at a REBCO-only extension point is labelled `extension`: it has no Nb₃Sn comparator.

Support wording (check A): for Nb₃Sn, 8–12 T at 5.2–6.7 K is interpolation of a fitted law. The Tsui data lie at 4.2, 8, 10 and 12 K; 8 T is the weakest point, measured only at strongly compressive strain at 8 K, and the OST strand has no 4.2 K data below 10 T, so 8–9.5 T has no 4.2 K anchor. The Breschi production parameterizations do not state their fitted domain; applying them over the Tsui-measured range for ITER TF strands of the same specification is a bounded assumption.

**No Nb₃Sn fit-limit claim at 12 T (N2).** With every turn sized at peak field and pack-average steel, the reference construction rejects EU DEMO's own layer-1 conductor at its own design point by about 2 %. Nb₃Sn fit failures of a few percent near 12 T therefore reflect that conservatism and strand grade, not a material limit, and are reported as such.

## 3. The two conductor definitions

**Nb₃Sn** (new library definition). ITER-form critical surface (Tsui & Hampshire 2012 eq. 6–7; the same form in Breschi et al. 2017), strand critical current Ic = (C1/B)·s(εI)·(1 − t^1.52)(1 − t²)·b^p(1 − b)^q for the whole 0.82 mm strand (Cu:non-Cu 1.0), with C1 in A·T per strand (equivalently C × strand area), 10 µV/m, intrinsic strain εI as a fraction. Conductor critical current = n strands × Ic_strand(B, T, εI). Current-sharing temperature Tcs solves n·Ic_strand(B, Tcs, εI) = I.

- **Reference strand: the ITER TF production median.** Breschi et al. 2017 Table III (printed p.22) lists ten TF production parameter sets; at (12 T, 6.7 K, −0.3 %) they give 112.0–138.9 A (coordinator arithmetic, to be rechecked), median between ChMP TFRF4-7 (126.99 A) and WST TFCN5-6 (127.31 A). Reference: **WST TFCN5-6** (p 0.578, q 2.211, Ca1 47.52, Ca2 0, ε0,a 0.00218, Bc20 34.22 T, Tc0 16.26 K, C1 20823 A·T). This is the Nb₃Sn counterpart of REBCO's production-average anchor. **Sensitivities:** upper end OST TFEU9 (identical to Tsui Table 5(a); 138.9 A); lower end BEAS TFEU10-12 (112.0 A); Tsui BEAS II Table 5(c) (106.8 A) as a below-production check. The EU DEMO sizing implies a higher-grade strand (673 A/mm² non-Cu) that no captured parameter set reproduces; recorded, not adopted.
- **Median definition (check A r3 advisory).** The production median is defined at the reference point (12 T, 6.7 K, −0.3 %). At −0.6 % WST ranks 3rd of 10 (61.2 A against a production median of 73.1 A, range 58.0–81.4 A), so the −0.6 % strain sensitivity also carries a strand-grade effect; the study therefore evaluates the upper and lower production sets at −0.6 % too and reports that spread.
- **Strain:** reference εI = −0.30 % (EU DEMO react-and-wind design; prototypes −0.27 % and −0.33 %). Transferring a conductor effective strain fitted with another strand's parameterization to this strand is a bounded assumption (check A). Sensitivity −0.60 % (wind-and-react, inside the ITER TF band −0.55 to −0.97 %). If applied strain is ever converted, the rule is εI = εA + εM(table value).
- **Temperatures:** refrigerator supply 4.5 K; conductor 5.2 K = supply + 0.7 K nuclear rise (Sedlak 2020).
- **Validity:** B in [8, 14.5] T with the statuses above, T in [4.2, 12] K, intrinsic strain εI in [−1.0, +0.2] % (Tsui's reversible applied range −1.0 to +0.5 % shifted by the table εM of about −0.3 %; for OST [−1.28, +0.22] %). The evaluated strains −0.3 % and −0.6 % lie inside it.

**REBCO** (new library definition). 4 mm × 56 µm fusion tape (Molodyk 2021). Tape Ic(B, 20 K) = anchor × g(B), with g the measured 20 K, B∥c field shape normalized at 20 T (Molodyk Fig. 1a; two independent digitizations agree within 0.01: 2.11, 1.85, 1.61, 1.33 at 8, 10, 12, 15 T) interpolated log-log, and the anchor 198 A (production average 1.13 × 175 A). Temperature dependence × exp(−(T − 20 K)/T*), T* = 22 K (Senatore form; 22.4 and 21.4 K from Molodyk's two samples). Cable critical current = n tapes × tape Ic × degradation 0.90 (SPC 10–20 % after cycling; VIPER < 5 % plus 2–4 %).

- **Temperatures:** supply 20.0 K; conductor 20.7 K = supply + the same 0.7 K nuclear rise (bounded assumption, applied symmetrically per B4).
- **Sensitivities:** power-law shape g = (B/20 T)^−0.6 (the current model's law); anchor 225 A (measured sample); T* 17 and 33 K; degradation 0.80 and 0.95.
- **Validity:** B in [8, 20] T with the measured shape (its digitized knots) and [5, 24] T for the power-law sensitivity, at 20 K; T in [4.2, 50] K for the temperature law; field perpendicular to the tape face (the worst orientation, Molodyk Fig. 2 caption) assumed everywhere.

**Margin rules, reported side by side for both materials** (A3). Every evaluation reports operating fraction I / Ic(B, T_conductor) and Tcs.

- **Temperature rule:** Tcs ≥ supply + 0.7 K + 1.5 K (6.7 K for Nb₃Sn, Sedlak; 22.2 K for REBCO).
- **Fraction rule:** I ≤ 0.8 × Ic(B, T_conductor) ([AGENT] existing model convention, WI-062).
- **Reference acceptance:** Nb₃Sn temperature rule (sourced); REBCO fraction rule ([AGENT]). **Symmetric variants:** both on the temperature rule; both on the fraction rule. Nb₃Sn sizing-temperature variant: 6.5 K (Demattè).

These are genuinely different definitions: different properties, laws, temperatures, current-density bases and validity domains. The Stellaris plant's REBCO definition is untouched.

## 4. Winding construction and fit

Each offer **supplies** its per-turn component areas; the evaluator sums them and compares the gross area with the envelope. The offer policy (§ 5) generates the areas from the construction rules below at the offer's reference duty, and the evaluator separately computes each rule's requirement at the evaluated duty and reports the margin (B5). Protection and structural adequacy are allowance rules, not evaluated physics.

**Construction P** (protection/structure, EU DEMO/SPC type), calibrated to reproduce EU DEMO layer 1 exactly (test):

- superconducting cable = n × element area / 0.97 (cabling) / (1 − 0.20 void);
- stabilizer copper space = max(0, I/J_Cu − element copper) / (1 − 0.10 Rutherford void), with a **common** J_Cu = 93.4 A/mm² for both materials (Demattè; reproduces the anchor), so the pairing isolates material (N1). Variants: common 100 A/mm² (SPC HTS TF requirement, stated at 4.5 K; its use at 20 K is a bounded assumption) and material-specific 93.4/100. Element copper is half the Nb₃Sn strand and 10/56 of the tape;
- structural steel = s × I × (B / 12.04 T), s = 12.66 mm²/kA (EU DEMO pack average). Layer 1's 9.36 is set by the 5 mm manufacturing-minimum jacket, and layer 8 is 16.24; both are sensitivities, plus a variant without field scaling. Scaling with B at fixed geometry (Lorentz load ∝ B·I) is a bounded assumption;
- cooling channel, steel strip and gaps = 1.1077 mm²/kA (calibrated residual 116.25 mm² at 104.95 kA, including the 6.06 mm² strip, reproducing the 68 × 37.9 mm = 2577.2 mm² layer-1 conductor when steel is set to layer 1's 9.3635 mm²/kA);
- REBCO on construction P carries no solder or copper-profile allowance beyond the rule copper (A7); a REBCO CICC-type conductor (SPC) is the closest sourced analogue;
- insulation, ground insulation and filler = 0.237 of gross, a **pack-wide** fraction (1 − 406,531 / 532,656 from the per-layer conductor areas). A fixed fraction understates insulation for small conductors; noted, not modeled. The 20 % cable void applied to REBCO is a CICC feature (about 7 mm² at 12 T); labelled.

**Construction C** (compact, Stellaris Table 7 type), calibrated to reproduce Table 7 at 50 kA and 24.9 T (test): per kA, copper 2.945, solder 1.010, helium 0.673 mm²/kA, steel 3.030 mm²/kA × (B/24.9 T); no insulation listed.

**Pairings:** **common-P** (primary; isolates material), **native** (Nb₃Sn on P, REBCO on C; what the source designs imply), **common-C** (hypothetical for Nb₃Sn: protection at this copper level is not evaluated and is labelled). Differences between pairings attribute fit and cost to construction rather than material.

## 5. Offered designs and MR-7 roles

[INHERITED: MR-7] Every design quantity is supplied to the evaluator and evaluated as given. A declared offer policy outside the evaluator proposes offers; the evaluator never resizes.

| Quantity | Units | Role | Binding |
|---|---|---|---|
| Elements per turn n (strands or tapes) | 1 | chosen (offer) | case input |
| Per-turn copper, steel, cooling/misc, solder, helium, insulation areas | mm² | chosen (offer), generated by the declared construction rule at the offer's reference duty; disclosed as demand-matched there | case input |
| Supply and conductor temperatures | K | chosen | case input |
| Installed refrigerator rating per stage | W | installed capacity (offer) | case input |
| Critical current, Tcs, operating fraction | A, K, 1 | calculated | conductor definitions |
| Protection-copper and steel requirements | mm² | requirement (allowance rule) | construction calculation; compared with supplied areas |
| Required gross area per turn | mm² | calculated from supplied components | compared with the envelope |
| Cold load, refrigerator input power | W, MW | calculated demand | cryogenic calculation; compared with rating |
| Margin rules, envelope, validity domains | — | requirement/limit | case input or definition |
| Inventory and cost | m, t, USD | calculated from the supplied design | never from demand |

**Offer policy (declared search, separate).** For each anchor, field, material, pairing and margin-rule family: the reference offer is the smallest integer n meeting the material's acceptance rule under reference assumptions, with component areas from its construction rule at that duty. Also evaluated: an insufficient offer (⌊0.9 n_ref⌋ with the same component areas) and a generous offer (⌈1.2 n_ref⌉). Refrigerator ratings come from a fixed list (1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 30, 50, 75 kW at the cold stage); the policy picks the smallest listed rating at or above the reference offer's demand, and the next lower listed rating is evaluated as the insufficient refrigerator. Under each sensitivity variant the reference offers are **re-evaluated unchanged** (fixed-hardware robustness), and, separately labelled, the policy proposes **variant offers** under that variant's assumptions. Each case record stores every supplied quantity, so any offer is evaluable without the policy.

**Acceptance tests** (B6), through the generated package and independent of the implementation's own formulas where stated:

- Source data (tolerances in brackets): Tsui BEAS II Ic(12 T, 4.22 K, εI = 0) = 201.3 A [0.01 A] against the ITER TF specification (> 190 A) and the Tsui Fig. 9(a) peak reading ≈197 A [±5 A, plot reading]; OST and BEAS II values at the check-A points [0.01 A]; the ten Breschi production sets at (12 T, 6.7 K, −0.3 %) as rechecked [0.01 A]. REBCO shape ratios at 10, 12, 15 T within the two digitizations [±0.02]. Construction P with 399 × 1 mm strands, J_Cu 93.4 A/mm² and steel fixed at 9.3635 mm²/kA reproduces EU DEMO layer 1, 2577.2 mm² [relative 1e−6]; construction C reproduces Stellaris Table 7 at 50 kA and 24.9 T [relative 1e−6]. Carnot specific power 65.67 and 14.00 W/W; Ballarino 46.95 and 46.85 W/kA [0.01]; 316 conductivity integral 326.0 and 307.4 W/m [0.5 %, numerical integration of the NIST fit]; Green η(18 kW) = 15.5 × 18^0.23 % = 30.2 % [formula, 1e−9]; anchor S 20 K inventory 21.93 kW [0.1 %].
- MR-7: for current margin, fit, refrigerator capacity, protection copper and structural steel, one insufficient and one sufficient supplied design inside the domain; the supplied design is unchanged by evaluation; inventory and cost follow it.
- Field varied with hardware fixed: margin, requirement checks and demand change; inventory and conductor cost do not.
- One unsupported case per conductor receives `unsupported`, no verdict, and no economic ranking.

## 6. Cryogenics

- **Stages.** Cold stage at the supply temperature (4.5 K or 20 K); 77 K intercept stage common to both. Loads and electrical demand are reported per stage. Carnot specific power uses the **supply** temperature (B4).
- **Cold-stage load categories.** Nuclear heating = 35.5 W/m³ (Stellaris model value) × envelope volume (anchor S 136.56 m³ from the model; anchor D 16 coils × 0.5327 m² × 55.6 m turn length ≈ 474 m³, a bounded assumption) — equal for both materials. Radiation from the 77 K shield, independent of cold temperature (ratio 0.996). Support conduction scaled by the 316 conductivity integral (326.0 W/m from 4.5 K, 307.4 W/m from 20 K). Current-lead cold ends with the 77 K intercept: f_lead × n_leads × I × √(L0 (77² − T²)) (Ballarino form as in the model's thermal inventory; ≈12.0 W/kA at 4.5 K, 11.6 W/kA at 20 K per lead before f_lead). Joints ∝ I².
- **Anchor values.** S: the model's inventory at 20 K reconstructs its 21.93 kW rating exactly (nuclear 4.85, joints 7.5 at 50 kA, leads 8.73 at 50 kA, radiation 0.27, supports 0.59 kW). D: static radiation 1.3 kW and thermal-anchor plus support conduction 4.6 kW (Končar 2017, EU DEMO 4 K magnets; attributed wholly to the TF, a bounded upper assumption); leads with n_leads = 4 and f_lead = 1.25 (bounded assumption); joints at the EU DEMO 1 nΩ requirement with 16 joints per coil (bounded assumption).
- **Excluded, labelled:** forced-flow circulator work and helium inventory (ITER's circulating pumps were 11.4 kW at 4.5 K, so this exclusion favours Nb₃Sn); 77 K stage capital (common). A cold-load multiplier of 0.5 and 2 on the whole cold stage is a sensitivity.
- **Electrical demand** = load × (300 − T_supply)/T_supply ÷ η. Reference η = Green 2015, 0.155 × R(kW)^0.23 of Carnot at the stage's cooling capacity for both temperatures (Strobridge: losses proportionally the same at 10–30 K); Green's fitted data reach about 35 kW. Sensitivities: constant η = 0.24; 20 K efficiency on an input-power basis, η(R_equiv) with R_equiv = rating × 0.2132; and the **combined unfavourable case** for 20 K (input-power η with capacity-basis capital). The 77 K stage uses the model's fraction of Carnot 0.20 for both.
- **Refrigerator capital** from the installed rating, Green C = 3.1 × R_equiv^0.65 M$2015. For the 4.5 K plant R_equiv = rating. For the 20 K plant R_equiv = rating × (300 − 20)/20 ÷ (300 − 4.5)/4.5 = rating × 14.00 / 65.67 = rating × 0.2132 (input-power equivalence; Strobridge's input-power cost law spans 1.8–90 K). Sensitivity: capacity basis, R_equiv = rating.

## 7. Cost accounting and boundary

Single currency: 2021 USD, using the registered CPI series (factors to 2021: 1974 ×5.50, 1990 ×2.07, 2014 ×1.145; 2015 and 2016 from the same series). Strobridge's 1974 dollars are nominal mixed-year and are used only as a cross-check.

- **Superconductor purchase** = element length × price per physical metre, with element length = n × turns × coils × turn length (cabling twist ignored, stated). Prices (2021 USD, check B):
  - Nb₃Sn 0.82 mm strand: reference 8 USD/m (Cooley & Pong per-kg 1.5–2 M$/t → 7.9–10.6); range 5.4–13.5. The lower end converts Chislett-McDonald's 8.0 USD/kA·m at 6 T, 4.2 K with the reference strand's Ic there (680 A at εI = 0; 6 T lies below the law's supported field range, so this evaluation is a price conversion only, not a performance claim); the upper end is PROCESS ITER TF strand cost on whole-strand mass.
  - REBCO 4 mm tape: reference **80 USD/m, the 2021 market** (Chislett-McDonald 80 USD/kA·m at 6 T, 4.2 K → 69–100; Cooley & Pong 80 USD/m in 2016 → 90); **target 30** (Chislett near-term, 26–38); **volume 10** (8.6–12.5).
- **Other winding materials** = mass × price for copper, steel and solder, using the model's existing densities and prices.
- **Refrigerator capital** from the installed rating (§ 6).
- **Refrigeration electricity** = total input power × 8760 h × 0.8 availability × 60 USD/MWh ([AGENT]; sensitivity 30 and 120).
- **Annualized subsystem cost** = 0.08 × capital + annual electricity ([AGENT] capital recovery factor; sensitivity 0.05 and 0.11).
- **Break-even REBCO price** per metre (also per kA·m at the operating point) at which annualized costs are equal, computed per matched pair from recorded outputs (cost is linear in that price), **only for pairs in which both offers pass every evaluated check**, and reported across the Nb₃Sn price range.
- **Manufacturing allowance sensitivity:** ITER TF cabling and jacketing, 985 USD/m (2014) = 1128 USD/m (2021) per conductor metre, applied to Nb₃Sn only and to both. Check B notes this is comparable in size to the conductor cost difference.
- **Excluded and reported as partial accounting:** winding labour per turn-metre (common, cancels), other material-specific manufacturing (reaction heat treatment, REBCO stacking and soldering), coil case and external structure, current-lead and power-supply hardware, quench-protection systems, cryostat and distribution, 77 K stage capital, circulators and helium inventory. Any preference is stated as “within the evaluated categories”.

## 8. Outputs, statuses and criteria

Per case: status; n and all supplied areas; critical current, operating fraction, Tcs, temperature margin, and both rule verdicts; element length (km), superconductor, copper, steel and solder mass (t); protection-copper and steel requirement margins; required gross area per turn, fit margin and verdict, required envelope current density; cold-stage load by category and intercept load (kW); η, electrical demand by stage (MW); installed ratings and capacity verdicts; superconductor, materials and refrigerator capital; annual electricity; annualized cost; for matched pairs, the cost difference and break-even price.

- **Failed and unsupported cases stay in the record** with distinct statuses; a **near-threshold** flag marks any margin within 2 % of its requirement.
- **Preference** is defined only over matched pairs in which both offers pass every evaluated check. A fit-failing or unsupported offer has no economic ranking.
- **Numerical tolerance:** oracle agreement relative 1e−9 (absolute 1e−9 per unit); Tcs root to 1e−9 K; verdicts use exact comparisons on computed values.
- **Materially different result:** a sign change of the annualized cost difference; a fit, margin or capacity verdict change; or more than 10 % change in the break-even price. A preference is called robust only if its sign holds across every tested variant; otherwise the answer states the reversal condition or the break-even price.
- **Consequential uncertainties tested:** construction basis (pairings, steel base and scaling), Nb₃Sn strand grade, strain and margin rule, REBCO shape, anchor, T*, degradation and margin rule, refrigerator efficiency and capital basis (including the combined unfavourable case), cold-load multiplier, conductor prices (via break-even and price levels), manufacturing allowance, electricity price and capital recovery, and anchor D turn length.

## 9. Effects evaluated and effects that limit interpretation

Evaluated: critical-surface current margin under two rule families, winding-area fit, allowance-rule copper and steel, static and nuclear cold loads with staged refrigeration, conductor, material and refrigerator cost. Not evaluated, and therefore not claimable: mechanical stress and strain (steel is an allowance; the REBCO transverse limit is not checked), quench protection beyond the copper allowance, irradiation limits and lifetime, AC and ramp losses, joint and current-lead design, layer grading, field-geometry change from any winding-size change, and plasma performance. A case that passes every evaluated check is a screening pass, not a qualified design.

## 10. Model and study route

- New library file with the two conductor definitions (and their Tcs and operating fractions), the construction requirement and fit calculation, the staged cold load, refrigerator demand/offer screen and subsystem cost, and a matched-pair comparison calculation; a new design file supplying the anchor duty and the two windings per case; an isolated package under `exploration/magnet_materials/`. The Stellaris plant, its package and studies are not modified; regression evidence shows the existing package fingerprint unchanged.
- Handwritten bodies where codegen cannot express the calculation (Tcs root, log-log shape interpolation, conductivity integral), each mirrored by an independent oracle.
- One native study over both anchors, all field points, pairings, rule families, offers and variants, with failed and unsupported cases retained.

## 11. Changes from r1

- B1: primary anchor moved to the EU DEMO TF envelope; Stellaris kept as a secondary anchor; limits stated; fit-failing and unsupported offers excluded from ranking and break-even; statuses defined for edge, law-only, extension.
- B2: construction P calibrated to reproduce EU DEMO layer 1 (cabling factor, stabilizer void, cooling residual, 93.4 A/mm² for Nb₃Sn); anchor-reproduction tests added; steel base changed to the pack average 12.66 mm²/kA with 9.36/16.24 and no-scaling variants; insulation fraction restated as pack-wide.
- B3: current-lead cold ends use the 77 K-intercepted segment form.
- B4: Carnot factor at the supply temperature; the 0.7 K nuclear rise applied to REBCO too; symmetric temperature rule 22.2 K.
- B5: construction areas are supplied per offer and checked against their allowance rules; role table updated.
- B6: source-data, anchor, fixed-hardware and unsupported-ranking tests added.
- Check A: Nb₃Sn support wording corrected; effective-strain transfer labelled a bounded assumption; εI = εA + εM(table) recorded; reference strand changed to OST with BEAS II as sensitivity (Breschi production cross-check).
- Check B: 20 K input-power factor written out (0.2132); price labels corrected (REBCO reference is the 2021 market 80 USD/m; 30 target, 10 volume; Nb₃Sn 8 from per-kg); 2021 USD with CPI factors.
- Advisories: both margin rules side by side and swapped; combined unfavourable 20 K case; cold-load multiplier; boundary exclusions named; near-threshold flag; “within the evaluated categories” wording; manufacturing allowance sensitivity.

## 12. Changes from r2 (answering the `## Recheck r2` sections)

- N1 (blocking): construction P now uses one common protection-copper density, 93.4 A/mm², for both materials; common 100 and material-specific 93.4/100 are variants.
- N2: no Nb₃Sn fit-limit claim at 12 T; the conservatism behind near-12 T fit failures is stated in § 2.
- N3 and check-A residual: the cooling/strip residual is 1.1077 mm²/kA including the 6.06 mm² strip; the anchor test fixes steel at 9.3635 mm²/kA and states tolerances for every source-point test.
- N4: framing paragraph added at the top.
- A7: REBCO on construction P has no solder or copper-profile allowance; stated.
- Check A wording: OST has no 4.2 K data below 10 T; intrinsic strain domain restated as [−1.0, +0.2] %.
- Check A strand grade: the reference strand is now the ITER TF production median (Breschi Table III, WST TFCN5-6), with OST TFEU9 (upper), BEAS TFEU10-12 (lower) and Tsui BEAS II (below production) as sensitivities. The Breschi values are a coordinator transcription from the rendered table and need recheck.
- Check B advisory: Nb₃Sn price lower bound recomputed from the reference strand (5.4 USD/m), labelled a price conversion outside the law's supported field.
