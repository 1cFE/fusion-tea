# T-004 independent review: comparison contract draft r1

Reviewer: fresh independent agent, brief `evidence/briefs/t004-contract-review.md`. Scope: the comparison's design, not source transcription. Read: `owner-brief.md`, `modeling_project/REQUIREMENTS.md` § MR-7, `comparison-contract.md` (r1), `evidence-matrix.md`, `binding-audit.md` §§ 2, 4, 6, `screen/contract-screen.json`, `sources/nb3sn-winding.md` (construction anchor rows only), and the Stellaris design values the contract cites. No holdout or ARIES-CS material opened. My arithmetic is in the reviewer scratchpad and restated below where it matters.

## Overall verdict: FINDINGS

The contract's structure is sound: fixed geometry with excitation scaled to field, two genuinely different conductor laws, an explicit common construction, a separately declared offer policy, and honest partial-accounting labels. Six blocking changes are needed before implementation. The largest is that, in the fixed Stellaris envelope, the main matched pairing (common-P) cannot fit any conductor of either material above about 9 T, and the contract does not say what that means for the comparison. No item needs the owner: the brief delegates the duty boundary, construction and accounting choices, and each fix below stays inside that delegation.

## Q1 Duty coherence: finding (blocking B1)

- **The scaling is physically consistent.** At fixed air-core geometry and fixed current distribution, peak field is linear in ampere-turns. The model holds `peak_ratio` fixed (`stellarator_plant.sysml:246`) and never computes field from pack size (`binding-audit.md` § 2). Scaling I = 50 kA × B/24.9 T with 308 turns is therefore a coherent matched duty, and both materials see the same field and plasma-side ampere-turns.
- **It keeps the winding-size term out only for designs that fit.** A design whose required area exceeds the envelope is not a winding that exists at this duty. Building it would need a larger pack, which is exactly the omitted field term. The §2 claim "cannot enter any claimed result" is true only if fit-failing cases carry no inventory or cost claim.
- **The anchor envelope makes fit a construction verdict, not a material one.** The envelope needs 38.2 A/mm² gross at 8 T and 57.3 A/mm² at 12 T (I/420.8 mm²). Construction P's copper plus steel alone, with no superconductor at all, allows at most 47.0 A/mm² at 8 T and 39.5 A/mm² at 12 T. So under common-P nothing fits above about 9 T. The coordinator's screen confirms it: both materials fail fit at 9–12 T. Four of the five matched points are fit failures for both materials, decided by the P basis and the Stellaris envelope.
- **The envelope is the nominal peak-coil pack, not a verified space.** 420.8 mm² is `wp_side`² / 308 for the 0.36 m peak-coil section (`stellarator_plant.sysml:447`). The model's own radial allocation (`coil_t` = 0.30 m, `:305`) does not contain that pack; the published design reads fit margin −0.12 m (`binding-audit.md` § 3). All turns are also sized at the peak-coil peak field (no grading).

**Change needed (B1).** State all three limits in §2. Define how fit-failing pairs enter results: report them as fit failures with required area and required envelope current density (an envelope-independent material metric), but give them no cost ranking and no break-even. Then either accept that the valid-design matched comparison is narrow (report it as a finding), or move the matched duty. Making the envelope a variable offer requires repairing the field-geometry relation first, per the brief.

## Q2 Genuinely different definitions: OK

The Nb₃Sn ITER-form Jc(B, T, ε) strand law with a Tcs root, and the REBCO digitized-shape × exponential temperature law × degradation tape law, differ in properties, equations, temperatures, current-density basis and validity domain. Neither reuses the existing REBCO law. Advisory A4: name the Nb₃Sn reference conductor as an EU DEMO react-and-wind (R&W) flat-cable type using the BEAS II strand law. The −0.30 % strain is an R&W value, not ITER CICC performance.

## Q3 Fairness of construction: finding (blocking B2)

- **The pairing scheme is fair.** Common-P isolates material. Native shows what the source designs imply. Common-C tests construction. Under common-P the only material-dependent area is element count × element area, less element copper; I reproduced the screen's 12 T difference (84 mm²) from that alone.
- **Protection copper is not double-counted.** Element copper is credited against I/100, which is correct for both materials.
- **P does not reproduce its own anchor.** Applied to EU DEMO layer 1 (399 × 1 mm strands, 104.95 kA, 12.04 T), the P formula gives 2267 mm² bare against the source's 68 × 37.9 = 2577 mm² (−12 %). Missing terms: the 10 % void on the stabilizer Rutherford cables, the cooling channel inside the cable space, the 0.97 cabling factor, and 100 versus 93.4 A/mm² copper. The 8 T fit margins are only 12–17 % (44 and 62 mm²). Restoring the missing terms adds about 48 mm² gross at 8 T, which flips the Nb₃Sn 8 T fit verdict.
- **Change needed (B2).** Either model the missing terms, or state them as a declared simplification with their size. In both cases add anchor-reproduction tests: P against DEMO layer 1, and C against Stellaris Table 7.
- **Advisory A7.** Scaling steel with B·I omits coil size; DEMO coils are far larger than Stellaris coils. State the bound, for example C steel as the lower bound. Insulation is a fixed thickness in reality, so a fixed 23.7 % fraction understates it for these smaller conductors. The CICC void on REBCO is a Nb₃Sn-motivated feature; label it (about 7 mm² at 12 T). State what "other materials" in P contains for REBCO, since C carries solder. C lists no insulation, which favours REBCO in the native pairing; say so.

## Q4 Margins: OK with advisory A3

Using each community's rule is defensible when both operating fraction and temperature margin are reported for both materials. The two rules are close in current terms: the Nb₃Sn temperature rule gives operating fractions of 0.70–0.77 at 5.2 K, against REBCO's 0.80. REBCO's 0.80 fraction equals a 4.9 K temperature margin at T* = 22 K. Two changes:

- The symmetric rule Tcs ≥ 21.5 K omits the nuclear-heating temperature rise that Nb₃Sn receives (+0.7 K). That is part of B4 below.
- A3: also swap the other way, applying the 0.8 fraction to Nb₃Sn, and present both rules side by side in the answer rather than one as reference.

## Q5 MR-7: finding (blocking B5, B6)

- **Roles are right.** n, construction, temperatures and refrigerator rating are supplied. Ic against I, area against envelope, and demand against rating are all calculated and compared. Superconductor inventory follows the supplied n. The offer policy is separate and identifiable, and its offers are evaluable without it provided case records store n and rating explicitly.
- **B5: copper and steel are demand-scaled inventory.** Copper = I/100 A/mm² and steel = allowance × B·I size those materials from required performance, so they are adequate by construction. MR-7 requires this to be disclosed. In the role table, mark them as demand-scaled allowances (policy-selected), not "chosen". State that protection and structural adequacy are not evaluated, and record the resulting per-case areas as the supplied design.
- **B6: validation is self-consistency only.** Oracle agreement to 1e−9 shows the code matches its own formula, which the brief says is not sufficient. Add source-point reproduction with source-reading tolerances: Tsui points for Nb₃Sn, digitized Molodyk points for REBCO, the construction anchors (B2), and Green efficiency points.
- **B6: missing MR-7 test.** Add the fixed-hardware test: vary duty B with n and rating held, and show the demand and verdicts change while inventory does not.
- **B6: unsupported cases.** Assert that an unsupported case produces no economic ranking, not only an unsupported status.
- **Acceptance wording.** "Cost comparisons use offers that meet their acceptance rule" must name margin, fit and capacity together. Note that a sufficient-fit case under P exists only at 8 T.

## Q6 Cryogenics and accounting: finding (blocking B3, B4)

- **B3: lead staging is inconsistent.** 47 W/kA (4.2 K) and 46.9 W/kA (20 K) are the ideal lead values from 300 K straight to the cold end with no intercept. The contract also has a 77 K intercept stage, and the model's inventory segments the lead at 77 K (`mfe_cryo_inventory.sysml`, Qlead per segment). That segmented value is about 12 W/kA. With 12 leads and f_lead = 1.25 at 12 T, the contract gives 17.0 kW against 4.2 kW intercepted. That is 3.5 times the nuclear load (4.85 kW), and it would dominate the 4.7× Carnot-weighted difference. Use the intercepted cold segment, or justify the unintercepted lead, and carry the lead basis as a sensitivity.
- **B4: which temperature sets the Carnot factor.** "Cold stage at the conductor temperature" would evaluate Nb₃Sn at 5.2 K instead of the 4.5 K supply temperature, a 16 % understatement of electrical demand. Use the refrigerator supply temperature for both. State whether REBCO's 20 K is inlet or conductor temperature, and apply the nuclear-heating rise symmetrically, including in the symmetric margin rule.
- **A2: efficiency and capital use different size bases.** The reference evaluates efficiency at cooling capacity (0.325 at 25 kW, 20 K) but capital at input-power equivalence (a 5.3 kW 4.5 K machine, whose efficiency would be 0.228). This follows Strobridge's own framing, so it is acceptable. But both choices favour 20 K, so also test the combined adverse corner, not only one variable at a time.
- **A1: add a cold-load magnitude uncertainty.** 4.5 K load magnitudes are unavailable (`evidence-matrix.md` § 4), and the brief names cryogenic load as a likely consequential uncertainty. Vary the lead basis (including HTS leads), nuclear heating, and joint resistance by material. State the joint-resistance assumption, which is currently the same for both materials by I² scaling.
- **A6: state the boundary items.** The boundary is otherwise consistent and the exclusions are honestly labelled partial. Still, say whether 77 K stage capital, helium inventory (material-dependent density), insulation material and forced-flow circulator work are included or excluded.
- **Break-even is computable as claimed.** Cost is linear in REBCO price at fixed n. Restrict it to pairs passing margin, fit and capacity, and report it across the Nb₃Sn 5–11 USD/m range (A8).

## Q7 Outputs and claims: finding (advisory A5, A6; the claim fix is part of B1)

- **Statuses and tolerances.** The status set, tolerances and robustness rule meet the answer contract. A5: define statuses for the 13 T edge point and the REBCO-only extension. Report distance to threshold or a marginal flag, since REBCO at 9 T misses fit by 2.2 mm² (0.5 %).
- **Define the preference.** "Preference" must be defined only over pairs that pass margin, fit and capacity (B1).
- **Partial-accounting claims.** Material-specific manufacturing is excluded, and one-sided evidence shows it can be as large as the result. ITER cabling and jacketing at 985 USD/m of turn length is about 0.32 G$ over 321.6 km. The screen's conductor cost difference at 12 T is about 0.43 G$ (72,700 km × 8 USD/m against 33,800 km × 30 USD/m). The answer must phrase any preference as "within evaluated categories" and show that scale (A6).

## Required changes

Blocking, before implementation:

- **B1 (anchor envelope and fit):** state the fit limits of the anchor envelope, and restrict cost and break-even claims to valid pairs.
- **B2 (construction anchors):** make P reproduce its DEMO anchor, or declare the omitted terms, and add the anchor tests.
- **B3 (lead staging):** make lead loads consistent with the 77 K stage.
- **B4 (temperatures):** set the Carnot temperature to supply temperature, and apply the nuclear temperature rise symmetrically.
- **B5 (MR-7 disclosure):** disclose the demand-scaled copper and steel.
- **B6 (validation):** add source-point validation, the fixed-hardware test and the no-ranking test for unsupported cases.

Advisory: A1–A8 above.

## Recheck r2

Same reviewer, rechecking `comparison-contract.md` r2 (§ 11 change log) against B1–B6 and A1–A8. I read r2 in full and the coordinator's unchecked screen `screen/contract-screen-r2.json` and its script `contract_screen_r2.py`. My arithmetic is in the reviewer scratchpad; the key numbers are below.

### Verdict: FINDINGS (one small blocking change)

All six r1 blocking findings are resolved. The calibration that fixed B2 introduced one new fairness problem (N1): the "common" construction now gives the two materials different protection copper. It needs a one-line contract change and a study variant before implementation. N2–N4 are advisory.

### r1 findings

- **B1 resolved.** The primary anchor is now the EU DEMO TF envelope (3751 mm² per turn), where fit is not binding for either material at 8–11 T. Stellaris is kept as the secondary anchor, and its three limits are stated. Fit-failing and unsupported offers get no ranking or break-even (§§ 2, 7, 8). Statuses are defined for edge, law-only and extension.
- **B2 resolved in structure.** Construction P gains the cabling factor, stabilizer void and a cooling residual, and anchor-reproduction tests are added for P and C. Two leftovers go to N1 and N3.
- **B3 resolved.** Lead cold ends now use the 77 K-intercepted segment. Anchor S reconstructs the 21.93 kW rating; I checked the lead term, 12 leads × 1.25 × 50 kA × 11.64 W/kA = 8.73 kW.
- **B4 resolved.** The Carnot factor uses the supply temperature. REBCO gets the same 0.7 K rise (conductor at 20.7 K, temperature rule 22.2 K), and the screen evaluates REBCO at 20.7 K.
- **B5 resolved.** Component areas are supplied per offer and marked demand-matched at the reference duty. The allowance requirements are reported as margins. The MR-7 insufficient/sufficient tests cover protection copper and steel.
- **B6 resolved.** Tests now cover source data points, the construction anchors, fixed hardware and the unsupported no-ranking case. Advisory: give tolerances for the approximate source points ("≈197 A", "≈30 %").
- **A1–A6 and A8 resolved.**
- **A7 mostly resolved.** REBCO on construction P still carries no solder or copper-profile allowance, while C carries 1.01 mm²/kA of solder. State this.

### New findings

- **N1 (blocking): common-P no longer isolates material.** r2 uses J_Cu = 93.4 A/mm² for Nb₃Sn and 100 A/mm² for REBCO. At anchor D, 12 T, that difference alone costs Nb₃Sn 108 mm² of gross area.
  - With the reference 93.4, the OST reference strand misses fit by 135.5 mm².
  - With a common 100, it misses by only 27.8 mm² (0.7 %, near-threshold).
  - So the only fit verdict that separates the materials in the primary matched range depends mostly on this choice.
  - 93.4 is DEMO's design result, while 100 is SPC's HTS requirement. Keep one J_Cu for both in common-P, or relabel the pair as a material-attributed protection allowance. Either way, add the other option as a variant.
- **N2 (advisory): the reference P rejects DEMO's own conductor.** At DEMO's own duty, P with steel 12.66 mm²/kA gives DEMO's 399-strand conductor 3823 mm² against its 3751 mm² envelope (−72 mm², −1.9 %). The cause is peak-field sizing of every turn. So fit failures of a few percent at D-12 T come from the construction's conservatism plus strand grade (OST needs 753 strands; DEMO used 399 higher-grade strands). Record this as a test result, and do not claim a Nb₃Sn fit limit at 12 T.
- **N3 (advisory): the calibration is close, not exact.** With layer-1 steel (9.36), P gives 2570.7 mm² against 2577.2 mm² (−0.25 %). The test should use 9.36, not the reference 12.66, and state a tolerance, or the residual should be recalibrated.
- **N4 (advisory): state the anchor framing in the answer.** The primary anchor is a Nb₃Sn-native tokamak TF envelope, not the consumer's stellarator coil set. The answer should say so first. It should also say that REBCO's compactness appears there only through required envelope current density, and in anchor S. The brief delegates this choice, so it is not an owner gate.

## Recheck r3 and design review

Same reviewer. This section rechecks `comparison-contract.md` r3 (change log § 12) against N1–N4 and A7, and reviews `model-design-draft.md` for MR-7, contract fidelity, MR-3/EXPOSE placement and the verification plan. The Breschi transcription is left to the Nb₃Sn checker; I judged only its design role. My arithmetic is in the reviewer scratchpad.

### Verdict: FINDINGS (one small blocking design change)

Contract r3 resolves every open item and is ready for release. The design is MR-7-sound and faithful to the contract, with one blocking gap: it does not say how at-threshold areas survive the exact-comparison rule (D1). D2–D7 are advisory.

### Recheck of r2 findings

- **N1 resolved.** Common J_Cu = 93.4 A/mm² for both materials. Common 100 and material-specific 93.4/100 are variants.
- **N2 resolved.** § 2 now makes no Nb₃Sn fit-limit claim at 12 T, and states the conservatism behind near-12 T fit failures.
- **N3 resolved.** With steel fixed at layer 1's 9.3635 mm²/kA, construction P gives 2577.201 mm² (relative 4e−7) against the 1e−6 tolerance.
- **N4 resolved.** The framing paragraph now opens the contract.
- **A7 resolved.** The missing REBCO solder allowance on P is stated.
- **Reference strand, design role only.** Using the ITER TF production median as the counterpart of REBCO's production-average anchor is a sound choice. OST, BEAS and BEAS II bracket it as sensitivities. My independent evaluation of the WST TFCN5-6 set gives 127.30 A at (12 T, 6.7 K, −0.3 %), matching the contract.

### Design review

**MR-7: compliant.**

- n, the component areas, the insulation fraction, both temperatures and the cold-stage rating are all supplied.
- The copper and steel requirements, the fit (gross area against the envelope) and the capacity (q_cold against the rating) are all calculated and compared, never bound back to an input.
- Refrigerator capital follows the rating, and efficiency is evaluated at the installed rating.
- Inventory and cost follow n and the supplied areas.
- The offer policy lives only in study scripts.
- Deriving turn current from B_peak at fixed geometry is a documented duty direction, not a hidden sizing rule.

**Contract fidelity: faithful.**

- The strain function, Tc*, Bc2*, the Ic form and the C → C1 conversion match the contract.
- The REBCO closed-form Tcs is exact: my check gives Ic(Tcs) − I = −1e−11 A.
- The P and C area rules match the contract, and the copper space and copper mass handle the stabilizer void consistently.
- The η modes (0, 1, 2) and the capital modes (0, 1) reproduce the reference, the sensitivities and the combined unfavourable case. The capital input-power factor is 0.2132.
- The break-even formula is algebraically exact; with a numeric check the annualized costs match to 0.
- Both the Carnot factor and the lead cold end use the supply temperature.

**MR-3/EXPOSE: compliant.**

- The library is new, concept-agnostic and imports only `ScalarValues`, with neutral defaults.
- Parameter sets and anchor values live in the design.
- Consumers bind producer attributes.
- Nothing existing is modified; none of the new paths exist yet.
- Duplicating Carnot and refrigerator logic instead of reusing `mfe_cryo_plant.sysml` is justified by the Green efficiency law and the isolation requirement.

**Verification plan: adequate, with D1 and D5.**

### Findings

- **D1 (blocking): at-threshold areas and exact comparisons.** Reference offers carry copper and steel areas generated by the same formula as the requirement, so their margins are exactly zero. The contract compares margins exactly. If those areas are written with less than full precision, the margins go negative. My check: 12 significant digits gives cu_margin = −8.9e−10 mm², a spurious copper failure. That makes the offer unrankable and removes its break-even price.
  - Fix, in the design: pass generated areas at full double precision (repr round-trip), or round them up at a stated resolution.
  - Add a test that every reference offer has copper and steel margins ≥ 0.
  - Report allowance margins that sit at zero by construction as "at allowance", not as near-threshold.
- **D2 (advisory): edge and law-only pairs can be ranked unlabelled.** `rankable` checks only `supported ≠ 0`, so edge (13 T) and law-only pairs pass. Carry both status codes into `'Matched Pair Comparison'` so any ranking there is labelled.
- **D3 (advisory): the REBCO measured-shape domain is narrower than the contract says.** In the design it is 8–20 T, while contract §§ 2–3 say the REBCO law is supported over 5–24 T. Align the contract wording. No planned point falls outside 8–20 T.
- **D4 (advisory): T_conductor is supplied separately from T_supply.** The 0.7 K rise is a physical assumption, not an offer choice. Make it an input and derive T_conductor from it, or have the oracle check consistency.
- **D5 (advisory): make two MR-7 tests explicit in design § 5.**
  - Varying n changes element length and superconductor cost in proportion, while demand and the areas stay unchanged.
  - Varying the rating changes capital and the capacity verdict, but not q_cold or electrical demand.
- **D6 (advisory): the Green efficiency law is extrapolated for the largest ratings.** Green's data reach about 35 kW. A 50 kW rating (the D-12 T cold load is about 32 kW) or a 75 kW rating (under the ×2 multiplier) extrapolates it. Output a refrigeration-domain flag.
- **D7 (advisory): defaults and outputs.** State that `manufacturing_per_m` is 0 in the reference. Output the break-even price per kA·m that the contract names, or state that post-processing computes it from `ic_tape_op`.

## Recheck D1–D7

Same reviewer. I checked only the changed passages: `model-design-draft.md` §§ 2.1, 2.2, 2.4, 2.6, 2.8, 5 and 6, and `comparison-contract.md` § 3 (REBCO validity).

### Verdict: PASS

Release contract r3 and the design for implementation. Two wording leftovers remain; neither blocks.

### D1–D7

- **D1 resolved.** Generated areas are rounded up to the next 1e−6 mm². There is a test that every reference offer has copper and steel margins ≥ 0, and margins in [0, 1e−6] mm² are labelled `at allowance`.
- **D2 resolved.** The pair calculation takes both status codes. `pair_status` labels edge and law-only pairs, and `rankable` still requires supported status on both sides.
- **D3 resolved in the design and in contract § 3.** Leftover: the status bullets in contract § 2 still say "REBCO 5–24 T at 20 K". Change them to 8–20 T for the measured shape (5–24 T for the power-law sensitivity).
- **D4 resolved.** `nuclear_rise` and `margin_rise` are explicit inputs. T_conductor is derived, and the temperature rule is T_supply + nuclear_rise + margin_rise. Leftover: the design § 4 role table still lists T_conductor as a chosen input; mark it derived.
- **D5 resolved.** The hardware-isolation tests are explicit. The design's wording is more precise than mine was: because efficiency is evaluated at the rating, changing the rating also changes efficiency and therefore electrical demand. That is correct.
- **D6 resolved.** `green_extrapolated` flags any argument outside 0.01–35 kW.
- **D7 resolved.** `manufacturing_per_m` defaults to 0. `breakeven_rebco_price_per_kAm` uses the tape critical current at the operating point, without degradation, as stated.
