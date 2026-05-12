# Decision Dossier — Draft v0

**Status:** First exercise of the terminal output. Built from triage shortlist (`triage_v0_results.md`) + 2 traces + synthesis exec summaries. The point is to find out whether the methodology closes — whether 12 → 5 can be defended without all 12 traces.

**Method note:** This skips trace #3+. The 5-pick selection logic is run with whatever evidence is currently available (2 traces, 12 synthesis exec summaries). Cells where evidence is thin are flagged `[thin]` — that's the methodology testing itself.

---

## Part A — Set-level rationale

### A.1 Decision-load-bearing spanning axes

The terminal artifact must teach the cross-concept story. Not every taxonomic axis matters for that story; only axes that *change a TEA conclusion* count. Five candidate axes:

| Axis | Why it changes a TEA conclusion |
|---|---|
| **Confinement family + geometry** | Drives CAS22 reactor-plant cost structure (closed-toroidal vs linear vs pulsed/transient vs implosion chamber). Different first-wall, vacuum, magnet topologies. |
| **Fuel cycle** | Drives blanket presence/cost, tritium handling, neutron wall load, thermal-cycle vs direct-conversion architecture. D-T vs D-He3 vs p-B11 are not the same TEA. |
| **Driver / compression class** | Drives CAS22 sub-allocation: steady-state SC magnet, pulsed-power capacitor bank, mechanical/pneumatic, laser, beam. Different fixed-vs-marginal cost shapes. |
| **Cohort & financing pathway** | Drives discount rate, learning curve assumption, supply-chain singleton vs shared. State-backed, cohort-rich-private, isolated-private, adjacent-to-NIF are different *cost-of-capital* and *gigafactory amortization* stories. |
| **Failure-locus stage** | Where the kill chain bites — Stage-1 physics, Stage-2 FOAK affordability, Stage-3 chasm. Sets the *value-of-information* of the TEA itself: if Stage 1 fails, downstream cost numbers are moot. |

Two axes from the taxonomy that did **not** make this list and why:
- *Magnet class (HTS vs copper)* — already encoded inside "driver class" and reflected in cost via REBCO singleton; redundant.
- *Modularity / replication unit size* — output of cost modeling, not input. Promote to a Part-B field, not a spanning axis.

### A.2 The 5 picks

| # | Concept | Confinement | Fuel | Driver | Cohort | Failure locus |
|---|---|---|---|---|---|---|
| 01 | HTS compact tokamak (CFS ARC) | MFE / closed toroidal | D-T | steady-state SC magnet (HTS) | first-mover, cohort-rich (private) | Stage-2/3 (REBCO singleton × $12.6B FOAK) |
| 08 | FRC + direct conversion (Helion) | FRC / pulsed-merge | D-He3 | pulsed inductive + direct conversion | first-mover, isolated (private) | Stage-1 binary (D-He3 ignition + capacitor 10× cost) |
| 14 | MTF pneumatic (General Fusion) | MTF / liquid-metal liner | D-T | pneumatic mechanical compression | first-mover, isolated (private) | Stage-1 engineering (LM26 → integrated reactor) |
| 26 | Laser ICF indirect drive (NIF-heritage) | IFE / hohlraum implosion | D-T | DPSSL / laser | adjacent to NIF cohort | Stage-2 (laser driver $/J and rep rate) |
| 28 | Full-HTS tokamak (China HH380) | MFE / closed toroidal | D-T | steady-state SC magnet (HTS) | state-backed, fast-follower | Stage-3 (chasm financing pathway distinct from private) |

### A.3 Spanning claim

- **Confinement family:** MFE×2, FRC×1, MTF×1, IFE×1. Toroidal-closed (×2), pulsed-merge, liquid-liner-implosion, hohlraum-implosion. The four major geometric archetypes are represented; only stellarator (closed toroidal, distinct coil geometry) is absent.
- **Fuel cycle:** D-T×4, D-He3×1. The aneutronic pole is represented exactly once, by the candidate with deepest documentation (Helion). p-B11 is unrepresented — accepted because TAE's 50–80× T_i extrapolation is too thin to anchor cost.
- **Driver class:** 5 distinct — HTS-SC-magnet, pulsed-inductive + direct-conversion, pneumatic mechanical, laser, HTS-SC-magnet (different supply-chain context). The MagLIF/pulsed-power capacitor class is unrepresented; trade-off justified below.
- **Cohort/financing:** 4 distinct — cohort-rich private, isolated private (×2), adjacent-to-NIF, state-backed. The financing-pathway diversity is the main reason 28 is in over 21 (both tokamak HTS, but 21 is private-cohort-redundant with 01).
- **Failure locus:** Stage-1 binary (08), Stage-1 engineering (14), Stage-2 (01, 26), Stage-3 (28). Stage 4 (mature ops) is not the binding stage for any concept — accepted.

### A.4 What each pick uniquely teaches

| Pick | Uniquely informative output |
|---|---|
| 01 ARC | The MFE-mainline LCOE band character — tight, engineering-bounded $200–300/MWh, with REBCO supply curve as the dominant sensitivity. Anchors what "best-pedigreed D-T tokamak" looks like. |
| 08 Helion | The thermal-cycle-free / blanket-free cost structure. Direct-conversion replaces CAS22 turbine plant + CAS23 with capacitor-bank economics. *No other shortlist concept omits the thermal cycle.* |
| 14 General Fusion | Liquid-wall + pneumatic compression — no laser/no pulsed-power, no first-wall replacement, no SC magnet. Removes three of the canonical fusion CAS22 line items. |
| 26 NIF-heritage IFE | Laser driver $/J cost structure with the only near-gate physics (ignition demonstrated). Tests "does NIF heritage actually translate to a commercializable LCOE?" |
| 28 China HH380 (state-backed) | Cost-of-capital + manufacturing-scale discount distinct from private-VC discount. Same physics class as 01 — *the only way to isolate the financing-pathway contribution.* |

### A.5 What we are deliberately not covering

- **Stellarator geometry** (would have been 05/09). Accepted: 3D coil cost is a known cost adder vs tokamak; ARC + 28 already span the closed-toroidal axis; stellarator's TEA story is "tokamak with worse magnet cost, better disruption profile" — predictable from ARC's analysis.
- **p-B11 aneutronic** (would have been 18 TAE). Accepted: Helion covers aneutronic + direct conversion; TAE's 50–80× T_i extrapolation makes its cost numbers structurally weaker than Helion's. Aneutronic-via-D-He3 covers the axis adequately.
- **Pulsed-power MIF** (would have been 07 MagLIF, 15 Zap). Accepted with regret: 07 is genuinely orthogonal to all 5 picks (capacitor-bank driver economics at 10⁸ shots), but 14 already covers MIF-adjacent mechanical compression, and IFE laser-driver (26) covers the pulsed-driver-cost axis. Marginal information from adding 07 is real but smaller than the 5 included. If the set expanded to 6, 07 is the next pick.
- **Spherical tokamak** (21 Tokamak Energy). Accepted: same fuel + same magnet class as 01; spherical-vs-conventional aspect ratio doesn't change CAS22 *structure*, only magnitudes.
- **Levitated dipole, NT divertor, Realta mirror.** Accepted: each is a single-feature variation on existing covered concepts.

### A.6 Concentration risks acknowledged

- **D-T over-represented (4/5).** Mirrors where private capital + data sufficiency live. Not a bug; refusing this concentration would force inclusion of p-B11 with structurally weak cost basis (18) just for representational balance, which violates the data-sufficiency triage.
- **Closed-toroidal over-represented (2/5).** Justified only by the financing-pathway axis (01 private vs 28 state-backed). If financing-pathway is downgraded in scope, 28 should be replaced by 07 MagLIF or 14 General Fusion's pulsed driver.

---

## Part B — Per-pick decision rows

**Caveat:** Only 01 and 15 have full traces. Rows for 08, 14, 26, 28 are populated from synthesis exec summaries; cells without trace evidence are `[thin]`. This is itself a methodology finding — the dossier *can* be drafted without 5 full traces, but the gate-conditional and binary/degrading qualifiers require trace-depth evidence. Where they're `[thin]`, the dossier asserts but doesn't defend.

| Concept | Disruptive verdict | LCOE floor (point, band, basis, epistemic) | Dominant failure | Dominant leverage | Cohort role | Spanning role (1 sentence) | Risk-if-dropped | T1 |
|---|---|---|---|---|---|---|---|---|
| 01 ARC | yes | ($240/MWh, $200–300, NOAK conditional on REBCO $10/kA-m, engineering-bounded) | F2.d × F2.a (REBCO singleton + $12.6B FOAK) — degrading | E2.a (HTS crossover MRI/grid/transport) — unconditional, regime-overlap=high | first-mover, cohort-rich | MFE-mainline anchor: tight LCOE band, REBCO supply curve sensitivity | lose the cohort-shared HTS curve baseline; no anchor for stellarator/ST/state-backed analyses | sufficient |
| 08 Helion | conditional + architecture-proof-unconditional | ($50/MWh point, $50–$500+ band + D-T-fallback shelf $150–200/MWh, joint-gate-conditional on D-He3 ignition + capacitor $0.50/J + 90% direct recovery, physics×manufacturing-bounded) — see trace #3 | F1 binary-with-fallback (D-He3 gate; fallback to D-T) × F2.d capability-gap degrading (capacitor $/J 10× short) × F7 binary-sharp-cliff (90% recovery) | Layer A unconditional: direct-conversion architecture proof + pulsed-power capacitor learning curve (regime-overlap=partial). Layer B gate-conditional: F3.b modularization (50 MWe × 20) | first-mover, isolated | only aneutronic + only thermal-cycle-free architecture in set; **only concept whose architectural proof has portfolio value independent of company success** | lose the "no blanket, no turbine" cost structure entirely; lose direct-conversion architecture proof; no test of multi-gate-conditional epistemic | sufficient |
| 14 General Fusion | conditional (Layer-A-empty: portfolio-fragile axis-coverage pick) | ($104/MWh at 300 MWe FOAK, $78 at 1 GWe; band $70-$150; engineering-gated on commercial pneumatic compression feasibility; within-gate co-dominant on driver capital × q_eng × availability) — see trace #4 | F_engineering binary-terminal, gate-type=engineering (pneumatic compression never built; "no fallback" per synthesis §5) × F2.d capability-gap, information-absent (q_eng undisclosed) | Layer A: empty (no unconditional leverage; nominal regime-overlap). Layer B gate-conditional: liquid-metal-wall architecture (4π breeding + self-renewing PFC + zero consumables + HTS-elimination) contingent on pneumatic compression viability | first-mover, isolated | only MTF; only liquid wall; only mechanical-compression driver; removes 3 canonical CAS22 line items **if the engineering gate closes** | lose MTF entirely; lose the "no first-wall replacement" cost variant; lose the engineering-gated basis-type from the basis-type taxonomy | sufficient |
| 26 Laser ICF indirect (NIF-heritage) | conditional (HIGH Layer A; cohort-mutualized via in-family pivots) | ($98/MWh baseline, band $80-$160; joint-multi-gate-conditional on gain G>100 (binary-terminal-economically) × laser $/J ≤ $300/J (degrading) × availability ≥ 75% (degrading-dominant via elasticity −0.97); availability is dominant uncertainty) — see trace #5 | F1 binary-terminal-economically, gate-type=physics (synthesis §5 line 163: "economically nonviable" if G<10) × F2.d capability-gap degrading, gate-type=manufacturing-cost (DPSSL $/J 3× short) × F_operational capability-gap degrading, gate-type=engineering-operational (availability unvalidated, 1992 SOMBRERO baseline 68-69%) | Layer A unconditional (HIGH, 3 sub-threads): (i) NNSA-funded NIF ignition demos (government-funded-independent-architecture-proof); (ii) DPSSL industrial supply-chain overlap with defense/LIDAR/industrial-laser (regime-overlap=high); (iii) HYLIFE-III liquid-wall design-lineage. Layer B gate-conditional: <$1/target factory, 10 Hz cycle, $98/MWh numbers. Cohort mutualization via HDD/Fast-Ignition/HIB pivot paths | adjacent to NIF cohort | only IFE; only laser driver; only near-gate-physics in IFE family; **only government-funded-independent architecture proof in set** | lose IFE entirely; lose laser-driver cost structure; lose the strongest-Layer-A profile in set | sufficient |
| 28 China HH380 (state-backed) | conditional [thin] | ($70/MWh scaled, basis [thin], engineering-bounded but financing-pathway-conditional) | F3.a state-priority risk + F2.d HTS supply (shared with 01) — degrading [thin] | state-coordinated supply chain + manufacturing scale — unconditional [thin] | state-backed, fast-follower | only state-backed; isolates financing-pathway contribution from physics/engineering | lose the cost-of-capital comparison; cannot decompose private-VC discount vs technology cost | sufficient |

---

## Part C — Per-eliminated-concept lines

(One line each. Includes the 7 shortlist members not picked, plus 26 triage-eliminations.)

### Shortlist members not picked (7)

| ID | Concept | Stage cut | Reason (one clause) | Retain-for-future |
|---|---|---|---|---|
| 05 | Planar-coil stellarator | Part-A spanning | 3D coil cost is predictable from ARC's analysis; no new TEA structure | yes — re-include if stellarator-cohort emerges or if disruption-immunity is priced |
| 07 | MagLIF (Pacific Fusion) | Part-A spanning | pulsed-power driver covered partially by 26; marginal info < 5 included picks | **strong defer — pick #6 if set expands** |
| 11 | Realta mirror | Part-A spanning | linear-vs-toroidal is a single-feature variant; no distinct cost structure | yes |
| 12 | Levitated dipole | Part-A spanning | disruption-immunity is a narrow value-add; sacrificial-magnet model is bounded | low |
| 15 | Zap SFS Z-pinch | Part-A spanning | Stage-1-failure-locus is methodologically interesting but portfolio-redundant with 08/14 binary risks | retain as methodology control |
| 17a | Xcimer (DPSSL+FLiBe) | Part-A spanning | laser-IFE axis covered by 26; DPSSL vs hohlraum is a sub-axis | yes |
| 18 | TAE p-B11 FRC | Part-A spanning | aneutronic covered by 08 with stronger data; 50–80× T_i extrap weakens cost basis | yes — re-include if p-B11 data matures |
| 21 | Tokamak Energy ST | Part-A spanning | same fuel + magnet class as 01; ST geometry doesn't change CAS22 structure | low |
| 29 | NT tokamak (Firefly/MANTA) | Part-A spanning | NT divertor is a sub-axis of MFE; ARC analysis predicts NT cost delta | low |

### Triage eliminations (24)

Already documented in `triage_v0_results.md` §Results table. Eliminate-reason taxonomy: far-thin physics (14), T2 floor catastrophic (5), orphaned (2), insufficient docs (3), near-duplicate (4 — these become Part-C entries above, not triage-eliminations).

---

## Part D — Methodology findings from this exercise

1. **The 5-set can be drafted without all 12 traces.** Picking is driven by spanning axes (Part A.1), not by per-concept trace depth. Traces *defend* picks; they don't *generate* picks. This inverts what entries 002–006 implicitly assumed.

2. **Picks 01 and 08 are forced.** Any 5-set must include an MFE-mainline anchor (01) and the aneutronic/thermal-cycle-free representative (08, since 18 has weaker data). These two are not contested.

3. **Picks 14, 26, 28 are the contested slots.** Defensible alternatives exist: 14↔07 (mechanical vs pulsed driver), 26↔17a (IFE sub-axis), 28↔(no replacement; financing-pathway slot is unique to 28). The 12→5 has at least three reasonable variants depending on what TEA scope is prioritized.

4. **The "set expansion to 6" question is unstated in the methodology but operationally important.** A 5-set is documented as the target, but 07 MagLIF is *strictly orthogonal* to all 5 picks. The methodology should explicitly state whether 5 is a soft target (set can grow) or hard (5 picks ranked, 6th deferred).

5. **Part-B columns "Risk-if-dropped" and "Spanning role" don't need a trace.** They come from Part A and triage. v1 grammar work (entries 003–004) was further from these fields than entry 005 estimated — those columns survive on synthesis+triage alone.

6. **Trace-required cells exist but are fewer than expected.** Only the LCOE-floor *band character* (basis + epistemic) and the failure/leverage qualifiers (binary/degrading, conditional/unconditional) genuinely require trace depth. That is **~4 cells per row × 5 rows = 20 trace-derived cells**, total. The remaining ~25 dossier cells come from triage + synthesis. The cost of "doing this right" is ≤5 traces of ARC/Zap depth — affordable.

7. **The next forced choice is which 3 concepts get traced next.** Trace #1 (01) and #2 (15) are done. Of the remaining 4 picks (08, 14, 26, 28), all four need trace-depth to fill the binary/degrading + conditional/unconditional cells defensibly. Trace #3 candidate is 08 Helion (per entry 006), still defensible. But the methodology now says trace #4 = 14, trace #5 = 26, trace #6 = 28 — *and after that, the dossier is defensible.* The trace-work envelope is bounded at ~4 more traces.

8. **15 Zap was traced but is not in the 5-set.** This is fine — it served as a methodological control (low-data + far-gate + isolated). But the dossier should explicitly note that *some traces are methodology-control traces*, not portfolio members. This is a category the methodology hadn't named.

---

## Part E — Robustness test of the 5 picks

### E.1 Coverage matrix

12 shortlist concepts × 5 spanning axes. Each cell is the value the concept takes; bold = unique values brought into the set by that pick.

| Concept | Confinement | Fuel | Driver | Cohort | Failure locus |
|---|---|---|---|---|---|
| 01 ARC | MFE-tokamak | D-T | SC-HTS-steady | cohort-rich-private | Stage-2 supply |
| 05 Thea / 09 Proxima | MFE-stellarator | D-T | SC-HTS-steady (3D) | isolated-private | Stage-2 coil cost |
| 07 MagLIF (Pacific Fusion) | MIF-Z | D-T | pulsed-power-capacitor | cohort-thin-private | Stage-3 rep-rate |
| 08 Helion | FRC | D-He3 | pulsed-inductive + direct-conv | isolated-private | Stage-1 binary |
| 11 Realta mirror | MFE-mirror | D-T | SC-HTS-linear | cohort-thin-private | Stage-1 confinement |
| 12 Levitated dipole | levitated-dipole | D-T | SC-coil-sacrificial | isolated-private | Stage-1/2 magnet life |
| 14 General Fusion | MTF | D-T | mechanical-pneumatic | isolated-private | Stage-1 engineering |
| 15 Zap | Z-pinch | D-T | pulsed-power-capacitor | isolated-private | Stage-1 binary (Q-gate) |
| 17a Xcimer | IFE | D-T | laser-other (excimer) | adjacent-NIF | Stage-2 driver |
| 18 TAE | FRC | p-B11 | pulsed-inductive (beam) | cohort-thin-private | Stage-1 temperature |
| 21 Tokamak Energy ST | MFE-spherical-tokamak | D-T | SC-HTS-steady | cohort-rich-private | Stage-2 supply |
| 26 NIF-heritage IFE | IFE | D-T | laser-DPSSL | adjacent-NIF | Stage-2 driver |
| 28 China HH380 | MFE-tokamak | D-T | SC-HTS-steady | state-backed | Stage-3 financing |
| 29 NT (Firefly/MANTA) | MFE-tokamak | D-T | SC-Cu-NT | cohort-thin-private | Stage-2 divertor |

### E.2 Coverage scoring of candidate 5-sets

Unique axis-values covered = sum over 5 axes of distinct values present:

| 5-set | Conf | Fuel | Driver | Cohort | Failure | Total |
|---|---|---|---|---|---|---|
| **Chosen: 01, 08, 14, 26, 28** | 4 | 2 | 4 | 4 | 5 | **19** |
| Alt-A: 01, 07, 08, 14, 26 | 5 | 2 | 5 | 4 | 5 | **21** |
| Alt-B: 01, 07, 08, 14, 28 | 4 | 2 | 5 | 5 | 5 | **21** |
| Alt-C: 01, 08, 18, 26, 28 | 3 | 3 | 3 | 4 | 4 | **17** |
| Alt-D: 01, 05, 08, 14, 26 | 5 | 2 | 5 | 4 | 5 | **21** |
| Alt-E: 01, 07, 08, 18, 26 | 5 | 3 | 5 | 4 | 5 | **22** |

**Finding:** The chosen set is **not spanning-optimal**. Alt-A, Alt-B, Alt-D all reach 21; **Alt-E reaches 22** (gains MIF-Z + p-B11 + pulsed-power-capacitor over the chosen set, loses MTF + state-backed). The chosen set's weakness is concentrated in **slot 5 = 28** — its unique axis-contributions are exactly one (state-backed cohort) and one (Stage-3 financing-pathway), both on cohort/financing rather than physics/engineering.

### E.3 Defending 28 (or not)

28 stays in the set *if* "state-backed financing pathway" is a TEA conclusion that **cannot be derived as a sensitivity on 01**. The case for 28:
- State-backed implies fundamentally different cost-of-capital (sovereign discount rate ~3% vs private VC ~12%) — this is a sensitivity parameter, derivable from 01.
- State-backed also implies different *supply-chain assumptions* (state-coordinated REBCO scaling, captive manufacturing, no IP licensing markup) — *not* a sensitivity on 01.
- State-backed implies different *learning-rate* assumptions (standardized fleet vs bespoke FOAK) — partially derivable from 01.

If the TEA only needs cost-of-capital sensitivity, drop 28. If it needs supply-chain-structure comparison, keep 28. **This is a user-judgment call, not a derivable one** — flag for the user.

### E.4 Defending dropping 14 vs 26 (if 28 stays + 07 added means dropping someone)

If 07 enters (Alt-A or Alt-B), something else exits. Trade-offs:
- **Drop 14:** lose MTF entirely + liquid-wall + pneumatic — three unique CAS22 modifications.
- **Drop 26:** lose IFE entirely + laser-driver economics + near-gate IFE physics.
- **Drop 28:** lose state-backed financing-pathway only.

If the trade is "lose 28's financing slot to gain 07's pulsed-power MIF slot," that's defensible. If the trade is "lose IFE to gain pulsed-power MIF," that's harder — IFE is a whole confinement family.

**Conclusion:** Alt-A (01, 07, 08, 14, 26) is the strongest alternative to the chosen set. The dossier should present **chosen vs Alt-A** as the binary choice and let the user pick based on whether financing-pathway diversity outranks driver-class diversity.

### E.5 Methodology finding from the robustness test

The coverage-matrix scoring is **cheap and decisive** — it took 15 minutes to build and produced a quantitative ranking. The methodology should make this a required step between Part-A spanning claim and Part-B per-pick rows. Without it, the Part-A claim is asserted, not tested.

### E.6 Verdict on the chosen-vs-Alt-A binary — **chosen set holds**

Resolved via a targeted source review of `33-state-backed-tokamak-best/synthesis.md` and `28-hts-tokamak-full-hts/synthesis.md`. The two syntheses **explicitly separate three structurally distinct cost levers** that travel together in the state-backed cohort:

1. **Cost of capital** (sovereign discount rate, IDC) — 33 §4 advantage #4, 28 §1 "concessional financing 3-4%" sensitivity (line 35). *Derivable as a sensitivity on 01.*
2. **Supply-chain localization / captive manufacturing** — 33 §4 advantage #1 ("ASIPP manufactures >70% of China's ITER components, eliminating supply chain risk"); 28 §4 ">95% China-domestic localization … 10-20% on unit prices … eliminates export control friction" (lines 102, 132). ***Not* derivable as a sensitivity on 01** — ARC has no captive supply chain and no equivalent industrial-policy substrate.
3. **Manufacturing-scale unit cost + construction tempo** — 33 §4 advantage #3 ("Chinese Construction Economics, 2-4× cost reduction"); 28 §4 advantage #4 (HH70 built in <2 years; HH380 5-year construction vs 6-8 years for ITER-scale; IDC drops 15-25%). *Joint cultural/industrial output, not a free parameter on the Western baseline.*

The clinching framing is 28's §5 line 132: "Energy Singularity may be competitive in China at LCOE levels (80-100 $/MWh at scale) that would be uneconomical for Western concepts in Western markets." The syntheses themselves treat this as a **bifurcated economic story**, not as a sensitivity branch on the Western baseline.

**Verdict:** The state-backed slot earns its keep. The supply-chain-structure + manufacturing-tempo bundle is *structurally distinct* from anything derivable from 01 ARC. The chosen set (**01, 08, 14, 26, 28**) locks. Alt-A (swap 28 → 07) is rejected: 07's pulsed-power-capacitor lever is a per-component CAS22 differentiator that can be partially captured via 26's driver economics with a sensitivity branch, whereas 28's bundle cannot be captured at all from any other pick.

**What this leaves on the table:** 07 MagLIF's MIF-with-capacitor-bank niche remains uncovered. The methodology should flag this as a *known coverage gap* in Part-A, not as a methodology failure. If the user expands to 6 picks, 07 is the highest-value addition (advances coverage from 19 → 22 on the matrix). The "5 vs 6" question stays flagged for user judgment.
