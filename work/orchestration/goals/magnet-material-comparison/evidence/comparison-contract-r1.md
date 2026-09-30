# Comparison contract: REBCO versus Nb₃Sn at matched duty (draft r1)

Goal `magnet-material-comparison`, round 1. Status: **draft for independent review; not released**. Authority: all choices here are `[AGENT]` under the owner-ratified brief (`evidence/owner-brief.md`), except where a source is cited. Evidence: `evidence/evidence-matrix.md` (v1 + v2) and the per-class notes in `evidence/sources/`; model facts: `evidence/binding-audit.md`. Source interpretations marked “(check)” await the independent source/math check and may change numbers but not the structure below.

## 1. What is compared

Two explicitly supplied winding designs, one per material, that must carry the **same magnetic duty in the same space**: REBCO coated-conductor tape at 20 K, and Nb₃Sn ITER-type strand in a cable-in-conduit conductor with a 4.5 K helium inlet. Each has its own current law, construction and refrigeration temperature. The comparison reports current margin, superconductor and other inventory, winding fit, cold load, refrigerator electrical demand, and subsystem cost, and tests which assumptions change the preference.

It is a subsystem screening at a supplied duty. It is not a reactor redesign, not a claim that a lower-field Stellaris plant keeps its plasma performance, and not a qualified magnet design.

## 2. Duty and geometry boundary

**Anchor coil set (fixed geometry).** [AGENT] The Stellaris coil set as represented in the project model: 48 coils, 308 turns per coil, winding-pack envelope 0.36 m × 0.36 m (0.1296 m² per coil, 420.8 mm² available per turn), conductor length 321.6 km for the set (mean turn length 21.75 m), winding cold volume 136.56 m³ (`models/designs/stellarator_09/stellarator_plant.sysml:223,254,447`; replay `summary.json` s0). Why this anchor: it is the only coil set with a complete, sourced length, space and cold-load basis in the repository, and it is the consumer's model. EU DEMO and ITER supply constructions and margins, not the anchor.

**Excitation, not geometry, varies.** [AGENT] At fixed coil geometry with no magnetic material, peak field at the conductor is proportional to ampere-turns. The reference is the published 50 kA per turn at 24.9 T, so each duty point sets turn current I = 50 kA × B/24.9 T with 308 turns unchanged. This keeps geometry, conductor length and current distribution identical for both materials, so the omitted winding-size term of the field relation (evaluation.md item 4) cannot enter any claimed result: both windings occupy the same envelope at the same ampere-turns. Nothing in this contract computes field from winding size.

| Duty quantity | Value | Role |
|---|---|---|
| Coils, turns per coil, turn length | 48, 308, 21.75 m | fixed (anchor geometry) |
| Envelope per turn | 420.8 mm² gross | fixed supplied allocation; fit is required area versus this |
| Peak field B at conductor | matched points 8, 9, 10, 11, 12 T; edge point 13 T; REBCO-only extension 14, 16, 18, 20 T | varied duty |
| Turn current | 50 kA × B/24.9 T (16.06 kA at 8 T, 24.10 kA at 12 T) | derived from B at fixed geometry |
| Field orientation for REBCO | perpendicular to the tape face (worst case) | fixed, conservative |
| Nuclear environment | same winding volume and heat density for both | fixed |

**Common supported range.** [AGENT] 8–12 T is the matched range: the Nb₃Sn law is measured over 8–14.5 T at 4.2 and 8 K (Tsui Table 5c domain) and EU DEMO/ITER conductors operate at 11.8–12.2 T; REBCO tape is measured at 20 K over 5–24 T (Molodyk Fig. 1a). 13 T is an edge point: the EU DEMO 13.5 T conductor is a design never tested at full current. From 14 T upward the comparison is REBCO-only; Nb₃Sn is evaluated at 14 T but labelled “law-only, no fusion design” and above 14.5 T “unsupported”.

## 3. The two conductor definitions

**Nb₃Sn** (new library definition). ITER-form critical surface Jc(B, T, ε) for the BEAS II bronze-route ITER TF strand, full-range parameter set (Tsui & Hampshire 2012 Table 5c), engineering current density over the whole 0.82 mm strand (Cu:non-Cu 1.0) at 10 µV/m. Conductor critical current = n strands × Ic_strand(B, T, ε_eff). The intrinsic effective strain ε_eff enters the strain function directly (check: that SULTAN “effective strain” is the same intrinsic strain the law takes). Current-sharing temperature Tcs solves n·Ic_strand(B, Tcs, ε_eff) = I.

- Operating conductor temperature 5.2 K = 4.5 K inlet + 0.7 K nuclear heating (Sedlak 2020).
- Reference ε_eff = −0.30 % (EU DEMO react-and-wind design; prototypes −0.27 % and −0.33 %). Sensitivity −0.60 % (wind-and-react, inside the ITER TF band −0.55 to −0.97 %).
- Acceptance: Tcs ≥ 6.7 K (Sedlak: 4.5 + 0.7 + 1.5 K). Sensitivity: 6.5 K sizing temperature (Demattè).
- Validity: B in [8, 14.5] T, T in [4.2, 12] K, ε in the reversible range; outside it the evaluation is **unsupported**, never pass or fail.

**REBCO** (new library definition). 4 mm × 56 µm fusion tape (Molodyk). Tape Ic at 20 K = anchor × g(B), where g is the measured 20 K field shape normalized at 20 T (digitized Molodyk Fig. 1a, check) and the anchor is the 198 A production average at 20 T. Temperature dependence × exp(−(T − 20 K)/T*), T* = 22 K (Senatore form; Molodyk/Pierro-derived value, check). Cable critical current = n tapes × tape Ic × degradation, with degradation 0.90 (SPC 10–20 % after cycling; VIPER < 5 % plus 2–4 %).

- Operating temperature 20 K (Stellaris).
- Acceptance: I ≤ 0.8 × cable Ic at 20 K ([AGENT] existing model convention, WI-062; equivalent to Tcs ≥ 24.9 K at T* = 22 K). Sensitivity: the symmetric temperature-margin rule Tcs ≥ 21.5 K.
- Sensitivities: power-law shape g = (B/20 T)^−0.6 (the current model's law, conservative below 20 T); anchor 225 A (measured sample); T* 17 and 33 K; degradation 0.80 and 0.95.
- Validity: B in [5, 24] T at 20 K; T in [4.2, 50] K for the temperature law.

These are genuinely different definitions: different properties, laws, temperatures, current-density bases and validity domains. Neither is the existing REBCO calculation with changed inputs; the Stellaris plant's REBCO definition is untouched.

## 4. Winding construction and fit

[AGENT] The evidence matrix shows the non-superconducting construction dominates winding size, so it is declared explicitly and tested. Each turn's required gross area is the sum of the superconducting cable (elements divided by (1 − cable void)), extra copper, structural steel, other materials, divided by (1 − insulation/filler fraction). Fit margin = 420.8 mm² − required gross area per turn.

| Construction basis | Protection copper (total, element copper counts) | Structural steel | Cable void | Insulation, ground, filler | Source |
|---|---|---|---|---|---|
| **P** (protection/structure, EU DEMO/SPC type) | I / (100 A/mm²) | 9.36 mm²/kA × (B / 12.04 T) | 20 % | 23.7 % of gross | SPC HTS TF requirement; EU DEMO layer 1 (Demattè Table I); steel scaling with B·I is a bounded assumption |
| **C** (compact, Stellaris Table 7 type) | 2.95 mm²/kA copper + 1.01 mm²/kA solder | 3.03 mm²/kA × (B / 24.9 T) | 0.67 mm²/kA helium | none listed | Stellaris Table 7 at 50 kA, 24.9 T |

Pairings evaluated: **common-P** (main matched comparison), **native** (Nb₃Sn on P, REBCO on C: what the source designs imply), and **common-C** (hypothetical; Nb₃Sn protection at this copper level is not evaluated and is labelled so). Differences between pairings attribute fit and cost to construction rather than material.

## 5. Offered designs and MR-7 roles

[INHERITED: MR-7] Every design choice below is supplied to the evaluator and evaluated as given. A declared offer policy outside the evaluator proposes offers; the evaluator never resizes.

| Quantity | Units | Role | Binding |
|---|---|---|---|
| Superconducting elements per turn n (strands or tapes) | 1 | chosen (design offer) | design input per case |
| Construction basis and its per-kA allowances | mm²/kA | chosen (construction) | design input |
| Operating temperature, inlet temperature | K | chosen | design input |
| Installed refrigerator rating at the cold stage | W | installed capacity (chosen offer) | design input; compared with demand |
| Critical current, Tcs, operating fraction | A, K, 1 | calculated | conductor definitions |
| Required gross area per turn | mm² | requirement | construction calculation; compared with 420.8 mm² |
| Cold load, refrigerator input power | W, MW | calculated demand | cryogenic calculation |
| Margin rules, envelope, validity domains | — | requirement/limit | design input or definition |
| Inventory and cost | m, t, USD | calculated from the supplied design | never from demand |

**Offer policy (declared search, separate).** For each field, material and pairing, the reference offer is the smallest integer n meeting that material's reference acceptance rule under reference assumptions. Also evaluated: an insufficient offer (⌊0.9 n_ref⌋) and a generous offer (⌈1.2 n_ref⌉). Refrigerator offers come from a fixed list of ratings; the policy picks the smallest listed rating at or above the reference offer's demand, and one listed rating below it is evaluated as the insufficient refrigerator. Under each sensitivity variant, the reference offers are **re-evaluated unchanged** (robustness of fixed hardware) and, separately labelled, the same policy proposes variant-specific offers (what a designer who knew that assumption would buy). Cost comparisons use offers that meet their acceptance rule under the evaluated assumptions.

## 6. Cryogenics

- **Stages.** Cold stage at the conductor temperature; 77 K shield/intercept stage common to both materials. Loads and electrical demand are reported per stage.
- **Cold-stage load** = nuclear (35.5 W/m³ × 136.56 m³, Stellaris model value, same for both) + radiation from the 77 K shield + support conduction + current-lead cold ends + joints. Radiation is taken as independent of cold temperature (0.996 ratio, cryo-loads note). Lead cold-end load per kA is the Ballarino ideal, 47 W/kA at 4.2 K and 46.9 W/kA at 20 K. Support conduction uses the 316 conductivity integral from the cold temperature to 77 K (check: NIST 316 integral at 4.5 K versus 20 K). Lead and joint loads scale with turn current (I and I²). Geometry factors and counts come from the Stellaris thermal inventory; the existing library definition's 10–30 K domain is not reused at 4.5 K.
- **Electrical demand** = load × (300 − T)/T ÷ η. Reference η = Green 2015 large-refrigerator law, 0.155 × R(kW)^0.23 of Carnot, evaluated at the stage's cooling capacity for both temperatures (Strobridge: losses proportionally the same at 10–30 K). Sensitivities: constant η = 0.24 (ITER plant level); and a 20 K plant whose efficiency tracks input power (η evaluated at the 4.5 K capacity with the same input power). The 77 K stage keeps the model's fraction of Carnot 0.20 for both.
- **Installed rating** is the supplied offer; demand greater than rating fails the capacity check. Electrical demand follows the operating load; capital follows the installed rating.

## 7. Cost accounting and boundary

Single currency: 2021 USD, converted with the registered CPI series (check availability of the needed years).

- **Superconductor purchase** = element length × price per metre. Element length = n × 308 × 48 × 21.75 m (cabling twist ignored, stated). Price per metre is an input with a declared range, derived from sources and recorded in the evidence (check): Nb₃Sn ITER-type strand about 5–11 USD/m (ITER per-kg values and the 8.0 USD/kA·m at 6 T, 4.2 K); REBCO 4 mm tape about 10–100 USD/m (Chislett-McDonald 10/30/80 USD/kA·m at 6 T, 4.2 K; Cooley & Pong 80 USD/m). Reference: Nb₃Sn 8 USD/m; REBCO 30 USD/m.
- **Other winding materials** = mass × price for extra copper, steel and solder, using the model's existing material prices and densities.
- **Refrigerator capital** from the installed rating: Green C = 3.1 R^0.65 M$2015 on a 4.5 K-equivalent basis where R is the rating scaled by input-power equivalence (Strobridge's input-power cost law spans 1.8–90 K); sensitivity: capacity basis with no temperature credit.
- **Refrigeration electricity** = total input power × 8760 h × 0.8 availability × electricity price 60 USD/MWh ([AGENT]; sensitivity 30 and 120 USD/MWh).
- **Annualized subsystem cost** = 0.08 × capital + annual electricity ([AGENT] capital recovery factor, roughly 7 % over 30 years; sensitivity 0.05 and 0.11).
- **Break-even REBCO price**: for each matched pair, the REBCO price per metre (also expressed per kA·m at the operating point) at which annualized costs are equal, computed from recorded case outputs because cost is linear in that price.
- **Excluded and reported as partial accounting:** winding labour per turn-metre (common to both, cancels), material-specific manufacturing (Nb₃Sn reaction heat treatment, conduit jacketing, REBCO stacking and soldering; no common-basis sources), coil case and external structure (same duty and forces), current-lead and power-supply hardware, quench-protection systems, cryostat and distribution.

## 8. Outputs, statuses and criteria

Per case: validity status (`supported`, `law-only`, `unsupported`); n; critical current, operating fraction, Tcs and temperature margin, margin verdict; element length (km), superconductor mass (t), copper/steel/solder mass (t); required gross area per turn, fit margin and verdict, required envelope current density; cold-stage load by category and shield load (kW); η, electrical demand by stage (MW); installed rating and capacity verdict; superconductor, materials and refrigerator capital, annual electricity, annualized cost.

- **Failed and unsupported cases stay in the record** with distinct statuses. An unsupported conductor evaluation never counts as pass or fail and carries no economic ranking.
- **Numerical tolerance:** oracle agreement relative 1e−9 (absolute 1e−9 in each unit); Tcs root to 1e−9 K; verdicts use exact comparisons on computed values.
- **Materially different result:** a preference reversal is a sign change of the annualized cost difference between matched offers; a fit or margin verdict change; or a change of more than 10 % in the REBCO break-even price. A preference is called robust only if its sign holds across every tested variant; otherwise the answer reports the reversal condition or a break-even price.
- **Consequential uncertainties tested (at least two required):** construction basis (pairings), Nb₃Sn strain and margin convention, REBCO field shape/anchor/T*/degradation, refrigerator efficiency and capital basis, superconductor prices (via break-even), electricity price and capital recovery.

## 9. Effects evaluated and effects that limit interpretation

Evaluated: critical-surface current margin, winding-area fit, static and nuclear cold loads with staged refrigeration, conductor, material and refrigerator cost. Not evaluated, and therefore not claimable: mechanical stress and strain (steel is an allowance, and the REBCO transverse limit is not checked), quench protection beyond the copper allowance, irradiation limits and lifetime, AC and ramp losses, joint design, current-lead design, field-geometry change from any winding-size change, and plasma performance at reduced field. A case that passes every evaluated check is a screening pass, not a qualified design.

## 10. Model and study route (for the reviewer's MR-7 and design check)

- New library file with the two conductor definitions, their Tcs/operating-fraction calculations, the construction/fit calculation, the staged cold load, refrigerator demand/offer screen and subsystem cost; new design file for the anchor duty and the two supplied windings; an isolated package under `exploration/magnet_materials/`. The Stellaris plant, its package and its studies are not modified; regression evidence shows the existing package fingerprint unchanged.
- Handwritten bodies where codegen cannot express the calculation (Tcs root, digitized-shape interpolation), each mirrored by an independent oracle.
- MR-7 acceptance tests: for current margin, fit and refrigerator capacity, one insufficient and one sufficient supplied design within the domain, plus an unsupported-domain case per conductor; verify the supplied design is unchanged by evaluation and inventory/cost follow it.
- One native study over the matched and extension points, all pairings, offers and variants; failed and unsupported cases retained.
