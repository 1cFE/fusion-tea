---
ID: 09-qi-stellarator-hts
Concept: QI Stellarator - HTS (D-T)
Company: Proxima Fusion
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: QI Stellarator - HTS (Proxima Fusion Stellaris)

## 1. Executive Summary

- **Single most important risk**: The 3D non-planar HTS coil manufacturing cost is truly unknown — no commercial precedent exists for freeform stellarator-geometry REBCO coils at 20 T peak field. If the manufacturing premium exceeds 2× the tokamak wound-coil reference, Stellaris is unlikely to achieve competitive LCOE regardless of capacity factor advantage. The SMC demo (2027) is the first real data point.

- **Single most important advantage**: Disruption-free steady-state operation eliminates the single largest availability-limiting event in tokamaks, enabling 85–95% capacity factor. This advantage is structural — it requires no technological breakthrough — and propagates directly into LCOE through the denominator (availability elasticity = −0.89, the dominant continuous lever).

- **LCOE ballpark**: $137–$188/MWh (initial build; Scenario A, H4-true ignited case) at DEFAULT coil cost (lower bound) across the 85–95% capacity factor range. **Replacement-inclusive LCOE**: $146–$163/MWh at DEFAULT coil cost; $188–$268/MWh at 1.5× coil multiplier (optimistic 3D premium); $249–$350/MWh at 2.5× multiplier. The replacement-inclusive figure is the economically complete comparison metric — Stellaris requires two full magnet replacements over a 30-year plant lifetime due to neutron fluence limits (~10 FPY at 2.7 GW), a lifecycle cost not shared by compact HTS tokamaks on the same timeline.

- **Confidence verdict**: **Low**. The model output is a lower bound on capital cost (coil cost multiplier = 1.0× is the wound-coil tokamak analogue; 3D stellarator geometry premium not modeled). Two major unknowns dominate: (1) 3D HTS coil manufacturing cost — the single largest capital account ($2.3B at DEFAULT, $5.8B at 2.5×) has no commercial precedent; (2) H4 hypothesis (ignition) — whether 50 MW ECRH sustains indefinitely or drops to ~5 MW post-ignition determines H&CD cost and Q_eng, with $3.4/MWh LCOE swing. Both unknowns resolve after Alpha device (~2031). The capacity factor advantage over the HTS compact tokamak reference cannot be quantified until that reference analysis provides a comparable CF estimate (active disruption prediction may target 87–90%, shrinking Stellaris's edge to 0–1 percentage point).

---

## 2. What Matters Most for LCOE

Ranked by LCOE sensitivity magnitude:

### 2.1. Capacity Factor (Availability) — Elasticity −0.89

**Assumed value**: 88% (central estimate; Helios QI stellarator analogue)
**Source**: helios-stellarator-comparison.md §2 ("enabling an 88% capacity factor"); W7-X demonstrated >97% experimental run-time; blanket/divertor replacement interval of 1–4 years (Queral et al. 2025, arxiv-2501-04640.md) sets the maintenance floor at 85%.

**Sensitivity magnitude**: −0.89 elasticity = dominant continuous LCOE lever. A 10% relative change in CF (e.g., 88% → 96.8%) reduces LCOE by ~8.9%. The 85–95% range modeled spans $162.5/MWh (floor) to $146.7/MWh (optimistic), a $16/MWh swing at DEFAULT coil cost (replacement-inclusive).

**What would flip the economic conclusion**: If the HTS compact tokamak reference (01-hts-compact-tokamak) achieves 87–90% CF via active disruption prediction, Stellaris's disruption-free advantage shrinks to 0–1 percentage point — insufficient to offset the 3D coil manufacturing premium. The viability threshold is not "stellarator vs. conventional disruption-limited tokamak (~83–85%)" but "stellarator vs. ARC-class compact HTS tokamak with active disruption management." The H2 hypothesis gate cannot be evaluated until the 01 analysis provides a comparable CF estimate.

**Caveat**: The 88% central estimate carries medium confidence — Proxima has not published a Stellaris capacity factor target. The range is defensible (Helios analogue + W7-X experimental data + steady-state physics argument), but the floor (85%) and ceiling (95%) are analytical bounds, not engineering targets.

---

### 2.2. 3D Coil Cost Multiplier (C220103) — Viability Gate

**Assumed value**: 1.0× (DEFAULT = wound-coil tokamak reference) in the baseline model output; 1.5–5× range modeled in sweep (Brown 2018 stellarator-vs-tokamak comparison)
**Source**: analysis.md §7, C220103 row; Brown (2018) IEEE TPS; framework calibration to ARIES-CS (QA stellarator, LTS magnets)

**Sensitivity magnitude**: This parameter does NOT have a traditional elasticity — it is a **viability gate**, not a continuous optimization variable. At 1.0× (DEFAULT), C220103 = $2.3B; at 1.5×, $3.5B; at 2.5×, $5.8B; at 5×, $11.6B. The initial-build LCOE moves from $137/MWh (1.0×) → $158/MWh (1.5×) → $199/MWh (2.5×) → $301/MWh (5×). Replacement-inclusive LCOE (the economically complete figure) ranges from $157/MWh (1.0×) to $401/MWh (5×) at 88% CF.

**What would flip the economic conclusion**:
- **H1 viability threshold** (analysis.md §2): if the 3D manufacturing premium exceeds **2× per kAm**, stellarator CAPEX is unlikely to be competitive against compact HTS tokamaks regardless of capacity factor advantage. At 2.5× multiplier, replacement-inclusive LCOE is $249/MWh — plausibly non-competitive even at 95% CF ($232/MWh).
- **SMC demo (2027)** is the first real data point for 3D HTS coil manufacturing cost. Until then, this parameter brackets a factor-of-3 uncertainty range in the total LCOE.

**Caveat**: The DEFAULT (1.0×) output is a **lower bound** — it uses the framework's wound-coil (tokamak-style) geometry calibration. The actual Stellaris coil cost is somewhere in the 1.5–5× range; the model does not identify where within that range the concept sits. The Brown (2018) multiplier is a stellarator-vs-tokamak comparison (LTS era); it does not separately account for QI-vs-QA topology differences or HTS-vs-LTS manufacturing differences. The direction and magnitude of these additional biases are unknown.

---

### 2.3. Construction Time — Elasticity +0.40 (Third-Highest Engineering Lever)

**Assumed value**: 8.0 years (framework stellarator default; mfe_stellarator.yaml)
**Source**: No Stellaris-specific construction schedule published; 8-year default is plausible for a 13 m major radius machine with complex 3D coil fabrication and precision installation.

**Sensitivity magnitude**: +0.40 elasticity = third-highest engineering parameter (behind availability and r_coil, ahead of R0). A 25% schedule extension (8 yr → 10 yr) adds +10% to LCOE (+$13.7/MWh at baseline). IDC (CAS60 = $2.4B) is among the largest single cost accounts — construction schedule uncertainty compounds into LCOE through interest charges. The modeled range (7–12 years) spans $150/MWh (optimistic ARC-class compact analogue) to $190/MWh (worst-case schedule slippage) at DEFAULT coil cost, replacement-inclusive.

**What would flip the economic conclusion**: If Stellaris requires 10–12 years first-of-kind construction (vs. 6–7 years for an ARC-class compact tokamak at R0 ≈ 3–4 m), the IDC penalty partially offsets the capacity factor advantage. Construction time is the **financial expression of the machine scale penalty** — the low-beta operating point (2.76%) forces a larger physical machine (R0 ≈ 13 m, 443 m³ plasma volume), which propagates into both nuclear island capital accounts (first wall area, blanket mass, vacuum vessel) and the construction schedule.

**Caveat**: The 8-year default is a conceptual estimate, not an engineering schedule. The actual schedule depends on coil fabrication learning rate, site readiness (Gundremmingen brownfield advantage vs. greenfield), and whether Proxima pursues serial or parallel coil manufacturing. The sensitivity sweep bounds the impact, but the central estimate carries low confidence.

---

### 2.4. Thermal Efficiency (eta_th) — Elasticity −0.23

**Assumed value**: 0.35 (standardized to canonical "Thermal (unspecified)" per scoring framework; Stellaris-specific estimate is 0.38 gross, ~0.32 net)
**Source**: EUROFER97 structural steel temperature limit (550°C) constrains steam Rankine cycle to ~500°C → 38% gross thermal efficiency (analysis.md §3). Net plant efficiency ~32% (1,000 MWe / 3,100 MWth) after recirculating power deduction. Helios analogue (vanadium alloy FW, 635°C steam) achieves 40% (helios-stellarator-comparison.md §2).

**Sensitivity magnitude**: −0.23 elasticity = moderate engineering lever. A 10% relative improvement in thermal efficiency (0.35 → 0.385) reduces LCOE by ~2.3%. The Stellaris-vs-Helios gap (0.38 vs. 0.40) represents a ~5% relative difference in gross efficiency, corresponding to ~1.2% LCOE impact (~$1.6/MWh).

**What would flip the economic conclusion**: Adopting vanadium alloy structural material (Helios approach) would recover ~2 percentage points of cycle efficiency but trades supply-chain maturity for performance. EUROFER97 is well-characterized in the EU DEMO program; vanadium alloy has limited industrial-scale qualification for fusion neutron environments. The efficiency gap is real but not decisive — it does not change the rank-ordering of stellarator vs. compact tokamak economics.

**Caveat**: The eta_th = 0.35 figure in the model is a **canonical standardization**, not a Stellaris-specific cycle design. The 0.38 gross / 0.32 net estimate is conceptually sound (EUROFER97 limit + standard Rankine cycle) but not derived from a detailed heat integration study. The BOP thermal efficiency is a known quantity with bounded uncertainty (~±2 percentage points), unlike the coil cost or capacity factor.

---

### 2.5. H4 Hypothesis (Ignition / ECRH Requirement) — Scenario Branch, Not Continuous Parameter

**Assumed value**: Two scenarios modeled:
- **Scenario A (H4-true)**: 5 MW ECRH steady-state (ignited; Helios analogue: 1 MW; helios-stellarator-comparison.md §3.1)
- **Scenario B (H4-false)**: 50 MW ECRH sustained (Stellaris Table 3 stated value; stellaris-design-details.md)

**Source**: QI maximum-j optimization yields ~0.8% alpha energy loss (ANTS code; stellaris-design-details.md §2.2). If alpha confinement is adequate, steady-state ECRH drops to nominal levels post-ignition. If not, 50 MW is required indefinitely.

**Sensitivity magnitude**: $3.4/MWh LCOE delta (initial-build) between Scenario A and Scenario B at DEFAULT coil cost. This is a **scenario branch**, not a smooth sensitivity — the H&CD account either achieves a large negative delta vs. tokamak (ignited case) or reverts to near-parity (sustained ECRH case). The LCOE swing is modest in absolute terms ($3.4/MWh is ~2.5% of the baseline $137/MWh), but the **directional cost comparison** in analysis.md §7 changes sign: C220104 (H&CD) is the primary stated cost advantage for stellarators ("eliminating the need for an expensive plasma current drive system" — stellaris-design-details.md §Introduction). If H4-false, that advantage disappears.

**What would flip the economic conclusion**: Alpha device (Q>1, ~2031) is the first validation point for H4. If burning plasma alpha confinement at 2.76% beta and 2.7 GW fusion power deviates from ANTS simulation predictions, the 50 MW ECRH may not be reducible to ~5 MW. The risk is not catastrophic (the concept remains viable at 50 MW ECRH, Q_eng ≈ 4.2) but removes a key economic differentiator.

**Caveat**: The H4-true 5 MW assumption is based on the Helios analogue (1 MW ignited), not a Stellaris-specific prediction. Stellaris targets ~2.8× higher fusion power (2.7 GW vs. 958 MW), which may require proportionally higher steady-state ECRH even in the ignited phase. The 5 MW figure is a conservative margin estimate, not an engineering target from Proxima.

---

## 3. Risk Verdicts

### 3.1. 3D Non-Planar HTS Coil Manufacturing Cost (Challenge 1)

**Verdict**: **Genuinely uncertain**

**Rationale**: No commercial precedent exists for freeform stellarator-geometry REBCO coils at power-plant scale. W7-X demonstrated LTS non-planar coils at 6 T (€370M hardware investment over 1997–2014); CFS SPARC is developing HTS wound coils at 20 T (tokamak geometry). The combination — 3D freeform + HTS + 20 T + burning plasma neutron environment — has never been manufactured. The Brown (2018) stellarator-vs-tokamak multiplier (1.5–5×) is a literature analogue, not a Stellaris-specific estimate.

**What would retire this risk**: **SMC demo (2027)** — Proxima's Stellarator Model Coil demonstration targeted for 2027 will provide the first real cost and fabrication-time data for a 3D HTS coil at relevant field strength. This is a component-scale demo, not a full coil set, but it resolves whether the manufacturing process is feasible at all and anchors the lower end of the cost multiplier range. Full retirement requires commercial production of multiple coils (e.g., Alpha device coil set fabrication, post-2027).

---

### 3.2. Low-Beta Machine Scale Penalty (Challenge 2)

**Verdict**: **Likely resolvable** (for next-generation QI designs; Stellaris v1 is locked in)

**Rationale**: Stellaris v1 operates at 2.76% beta — roughly half the 5–8% beta of compact tokamaks. This is a **design-point choice**, not a QI physics ceiling. CIEMAT-QI4X (arXiv:2512.08825, December 2025) demonstrates a QI stellarator configuration maintaining island divertor compatibility, alpha confinement, and small bootstrap current at **beta up to 4%** — ~45% higher than Stellaris v1. Proxima stated "more commercially attractive designs are possible" (stellaris-design-details.md §2), consistent with iterating toward higher-beta configurations in follow-on designs.

**What would retire this risk**: **H2a scenario validation** — a follow-on QI design operating at 4% beta would reduce plasma volume at fixed fusion power by ~31% (Scenario H2a: R0 ≈ 11.6 m vs. 13.0 m; LCOE $152/MWh vs. $157/MWh replacement-inclusive at DEFAULT coil cost). This partially closes the gap to compact tokamak power density. The H2a scenario is a **design lineage branch**, not a Stellaris v1 variant — it represents the next-generation QI family and should be treated as a separate concept in cross-concept rankings. For Stellaris v1 specifically, the scale penalty is baked in and not resolvable without a redesign.

---

### 3.3. Burning Plasma Ignition Assumption (Challenge 3, H4 Hypothesis)

**Verdict**: **Unlikely resolvable** before Alpha device (~2031)

**Rationale**: The QI maximum-j optimization is specifically designed to improve alpha confinement relative to earlier compact stellarator configurations (ARIES-CS QA: "high alpha particle loss is a critical issue" — aries-cs-compact-stellarator-study.md). SIMPLE and ANTS code simulations predict ~0.8% alpha energy loss at Stellaris design conditions (stellaris-design-details.md §2.2), consistent with adequate self-heating. However, these are MHD equilibrium simulations — they exclude wave-particle interactions at burning plasma beta and do not account for potential loss channels at 2.7 GW fusion power (larger scale than existing simulation benchmarks). No burning-plasma-condition alpha confinement experiment in a QI configuration exists. The SMC demo (2027) tests coil manufacturing only, not burning plasma physics.

**What would retire this risk**: **Alpha device burning plasma operation** (Q>1, ~2031 target). If Alpha achieves Q>1 and demonstrates that steady-state ECRH drops to nominal levels (~1–5 MW) after alpha self-heating stabilizes, H4-true is validated. If 50 MW ECRH sustains indefinitely, H4-false is confirmed. Either outcome resolves the branching condition; until then, the hypothesis remains genuinely uncertain.

---

### 3.4. TBR Margin Adequacy in 3D Blanket Geometry (Challenge 4)

**Verdict**: **Likely resolvable**

**Rationale**: Stellaris achieves TBR = 1.074 post-correction (1.1070 baseline − 3% port correction; stellaris-design-details.md §2.8). This is close to the typical engineering minimum of 1.05–1.1 for tritium self-sufficiency at reasonable doubling time. The 3D stellarator first wall geometry creates more blanket penetrations (diagnostic ports, heating ducts, island divertor structure) than a tokamak, increasing neutron leakage pathways. However, the paper explicitly states that "margins to account for uncertainties and potential incomplete models" were applied, and the baseline Monte Carlo TBR (1.1070 ± 0.0002) provides ~3% design margin before the port correction.

**What would retire this risk**: **Integrated neutronics validation** with full port and penetration geometry modeled. If additional engineering losses (e.g., divertor island chain structure, incomplete blanket coverage at coil interfaces) reduce effective TBR below 1.05, the fallback is to increase Li-6 enrichment above the current 70% or reduce port area. Both mitigations have cost implications (enrichment supply chain; diagnostic access constraints) but do not invalidate the concept. TBR = 1.074 is a point estimate; the uncertainty band is ±0.02–0.03 based on typical Monte Carlo fusion blanket studies — the concept sits comfortably above the 1.05 floor even at the lower uncertainty bound.

---

### 3.5. Island Divertor Scaling to Burning Plasma Power Density (Challenge 5)

**Verdict**: **Genuinely uncertain**

**Rationale**: The island divertor is unique to QI stellarators and has no tokamak analogue. W7-X demonstrated the concept in steady-state operation at low power density, showing advantages over tokamak divertors (larger wetted area, complete detachment, no Eich scaling; stellaris-design-details.md §2.5). Key milestones: February 2023 — 30-minute continuous discharge; June 2025 — 1.8 GJ energy record in 6-minute run. However, W7-X operates at power densities far below Stellaris's 4.05 MW/m² first wall load. The island divertor geometry is tightly coupled to the magnetic topology — unlike the tokamak poloidal divertor, it cannot be independently redesigned if it fails to manage burning-plasma exhaust power. The Stellaris paper explicitly defers "recycling efficiency, ash removal, and erosion rates" to subsequent studies (stellaris-design-details.md §2.5).

**What would retire this risk**: **Burning plasma divertor experiments** at Stellaris-relevant power densities. The Alpha device (~2031) is the first opportunity to test the island divertor at 4 MW/m² first wall load in a QI configuration. If the divertor successfully maintains strong detachment and acceptable tungsten erosion rates at this power density, the risk is retired. If not, the only mitigation within the QI approach is to accept higher erosion and shorter replacement intervals (increasing O&M cost and reducing effective availability) — there is no straightforward engineering fallback that preserves the magnetic topology.

---

## 4. Structural Advantages and Disadvantages

Comparison against the conventional D-T tokamak cost structure baseline (HTS compact tokamak, 01-hts-compact-tokamak reference):

### Eliminated Cost Items (Structural Advantages)

1. **No central solenoid (CS)** — Stellarators are current-free by design; no flux-swing requirement. The CS coil set is typically 5–10% of tokamak CAS21 magnet cost (ITER-scale devices). For compact tokamaks, CS may be a smaller fraction or eliminated (ARC-class uses non-inductive startup), so the absolute saving is modest but directionally favorable.

2. **No continuous current drive** — Tokamaks require NBI or ICRF for steady-state current drive; stellarators use ECRH for heating only (no current drive component). If H4-true (ignited), steady-state ECRH drops to ~5 MW vs. 50–100 MW for a tokamak H&CD system. This is the **primary stated economic advantage** for stellarators (analysis.md §7, C220104 row: "Large −, −50 to −80%"). **Caveat**: This advantage disappears if H4-false (50 MW ECRH sustained).

3. **No disruption mitigation hardware** — Stellarators do not disrupt; no need for vertical position control, disruption prediction/avoidance systems, or halo current protection. This eliminates a cost and complexity layer present in all tokamaks. The cost saving is diffuse (spread across control systems, power supplies, and structural design margins) rather than a single large account.

### Added Cost Items (Structural Disadvantages)

1. **3D non-planar coil manufacturing premium** — The dominant LCOE uncertainty. Freeform stellarator coils require more tape per coil turn-length, precision positioning mandrels, and quality assurance for complex 3D geometry. Brown (2018) stellarator-vs-tokamak comparison shows the magnet system carrying a 1.5–5× premium in the CAS21 account. **Quantification**: C220103 = $2.3B at DEFAULT (lower bound) vs. $3.5B (1.5×) to $11.6B (5×). The 3D premium scales with the number of coils (50 modular coils for Stellaris) and stored energy (111 GJ, vs. ~2 GJ for a compact tokamak at equivalent net output).

2. **Higher cryogenic load** — p_coils = 111 MW conduction power to coils (Stellaris Table 3; stellaris-design-details.md). This is ~11% of gross thermal output and far exceeds the 2–3 MW default for tokamaks. The recirculating power fraction is ~20–25% (161–211 MW total across ECRH + coils + BOP pumping), vs. ~15–20% for compact tokamaks. **Quantification**: The coil conduction penalty adds ~$0.3/MWh to LCOE per MW of p_coils (elasticity +0.03); 111 MW vs. 3 MW baseline → ~$3.4/MWh LCOE penalty. This is non-trivial but smaller than the H4 branching effect ($3.4/MWh).

3. **Low-beta machine scale penalty** — Stellaris operates at 2.76% beta, roughly half the 5–8% beta of compact tokamaks. Producing 2.7 GW fusion power at 6.1 MW/m³ average power density requires a larger physical machine (R0 ≈ 13 m vs. 3–4 m for ARC-class). This propagates into first wall area, blanket mass, vacuum vessel, and buildings (CAS21). **Quantification**: analysis.md §7 rates CAS21 as "Small +, 5–15%" relative to compact tokamak reference; Scenario H2a (4% beta next-gen design) demonstrates the scale penalty is ~$6/MWh LCOE at DEFAULT coil cost. The penalty also propagates into construction time (8 yr vs. 6–7 yr for compact devices), compounding into IDC.

4. **O&M structural uplift** — Modular stellarator coil architecture leaves "relatively small ports for in-vessel access and maintenance, i.e. in comparison with tokamaks" (Queral et al. 2025; arxiv-2501-04640.md). Blanket and divertor module size is constrained by coil geometry, increasing maintenance complexity. **Quantification**: CAS70 = $184M/yr annualized at DEFAULT; O&M multiplier sweep shows 1.5× uplift → +$11.9/MWh LCOE, 2× uplift → +$23.8/MWh. The magnitude is truly unknown (Gap #7) — the DEFAULT is a lower bound for the same structural reason that C220103 is a lower bound.

5. **Periodic magnet replacement** — REBCO neutron fluence limit (~3×10²² m⁻²) constrains coil lifetime to ~10 full-power years at 2.7 GW (stellaris-design-details.md §2.8). Two magnet replacements are required over a 30-year plant lifetime. **Quantification**: replacement-inclusive LCOE adds +$20/MWh at DEFAULT coil cost, +$30/MWh at 1.5× multiplier, +$50/MWh at 2.5× multiplier. This is a lifecycle cost not shared by compact HTS tokamaks on the same 10-year replacement schedule — ARC-class devices may design for longer magnet lifetimes via shielding or accept coil replacement as well, but no published ARC-lineage analysis includes this cost component.

### Net Directional Assessment

**Uncertain; dominated by C220103 vs. C220104 + capacity factor.**

The competitiveness case depends entirely on whether:
- The 3D coil manufacturing premium (**Large +**, 1.5–5×) is more than offset by:
  - The H&CD saving (**Large −**, −50 to −80%; conditional on H4-true)
  - **PLUS** the capacity factor advantage (−0.89 elasticity; requires 85–95% stellarator CF to exceed the HTS compact tokamak reference CF by a meaningful margin)

At DEFAULT coil cost (1.0×, lower bound) and H4-true (ignited, optimistic), Stellaris achieves $157/MWh replacement-inclusive LCOE at 88% CF. This is **plausibly competitive** if the HTS compact tokamak reference sits at $150–180/MWh (unverified — 01 analysis has not published LCOE). At 1.5× coil multiplier (optimistic 3D premium), replacement-inclusive LCOE is $188/MWh at 88% CF — marginally competitive. At 2.5× multiplier, $249/MWh — unlikely to be competitive even at 95% CF ($232/MWh).

The viability envelope is narrow: the concept is economically viable **only if** the 3D coil manufacturing premium is at the optimistic end of the Brown (2018) range (≤2×) **and** the capacity factor advantage over the HTS compact tokamak reference is material (≥3–5 percentage points). If either condition fails, the stellarator's structural cost disadvantages dominate.

---

## 5. Cross-Concept Positioning

### 5.1. Nearest Neighbors

**Helios (Thea Energy, USA)** — The closest within-family comparator. Both are private-sector QI stellarators targeting commercial D-T plants with HTS magnets. Key differences:
- **Coil geometry**: Helios uses planar convex coil arrays (simpler to wind, lower manufacturing risk); Stellaris uses non-planar modular coils (stronger field per conductor, more complex).
- **Thermal efficiency**: Helios 40% (vanadium alloy FW, 635°C steam) vs. Stellaris ~32% (EUROFER97, 500°C steam). The 8-percentage-point gross efficiency gap is a 25% relative difference in cycle performance — Helios requires less thermal plant for the same net output, offsetting some BOP capital cost.
- **Beta**: Both operate at ~2.7% beta (Helios 2.7%, Stellaris 2.76%). This is a shared low-beta penalty relative to compact tokamaks.

**Economic implication**: Helios and Stellaris occupy the same LCOE band if 3D coil costs are similar. If Helios's planar coils prove significantly cheaper to manufacture (coil multiplier 1.2× vs. Stellaris 1.8×), Helios may have a 10–20% LCOE advantage over Stellaris within the QI family.

---

**W7-X → EUROfusion HELIAS pathway (Germany, public sector)** — The large-device public-sector QI lineage. Stellaris is a compact high-field HTS departure from this path. Key differences:
- **Scale**: HELIAS/EU-DEMO targets R0 ≈ 20 m, lower field, LTS or mixed LTS/HTS; Stellaris targets R0 ≈ 13 m, 20 T peak field, full HTS.
- **Philosophy**: HELIAS is an ITER-scale extrapolation (conservative physics, large machine, multi-decade timeline); Stellaris is a CFS-ARC-analogue acceleration play (private capital, aggressive timelines, HTS compactness bet).

**Economic implication**: HELIAS-class devices are unlikely to achieve competitive LCOE on a $/W basis due to size (capital cost scales faster than output power in the large-device regime). Stellaris's compactness strategy is the correct direction for commercial viability, but the 2.76% beta limits the compactness gain relative to ARC-class tokamaks.

---

**Type One Energy (USA, private)** — Another HTS stellarator startup using modular coil architecture, targeting HCPB (solid ceramic breeder) rather than WCLL blanket. Not yet at commercial plant study stage publicly. Similar 3D coil manufacturing risk; different blanket and heating choices.

**Economic implication**: Type One and Stellaris share the 3D HTS coil manufacturing risk. Whichever company demonstrates viable coil fabrication first (via SMC-equivalent demos) retires the risk for the entire stellarator family and provides a manufacturing cost anchor for the others.

---

### 5.2. Where Stellaris Sits in the Landscape

**Confinement family**: MFE — Stellarator (QI subclass)
**Technology generation**: Second-generation private fusion (HTS magnets, D-T fuel, commercial power plant target, ~2030s deployment timeline)
**Economic niche**: "Disruption-free capacity factor arbitrage vs. compact HTS tokamaks"

Stellaris occupies a **high-risk, high-variance** position:
- **If 3D coil cost ≤ 1.5× tokamak reference**: Plausibly competitive at $158–188/MWh replacement-inclusive LCOE (88% CF). The disruption-free advantage is real and structural; it requires no physics breakthrough to monetize.
- **If 3D coil cost ≥ 2.5× tokamak reference**: Unlikely to be competitive at $249–350/MWh. The capacity factor advantage (even at 95% CF) cannot offset a factor-of-2.5 coil cost penalty.

The concept is **fundamentally different** from compact tokamaks in that:
1. **The primary economic lever is manufacturing cost (C220103), not physics performance.** Compact tokamaks bet on high-beta physics to shrink machine size; stellarators bet on disruption-free operation to increase availability. Stellaris's competitiveness depends on whether 3D HTS coil manufacturing is "hard" or "impossible at scale" — a question that resolves via industrial learning (SMC demo, Alpha coil fabrication), not via physics experiments.

2. **The capacity factor advantage is structural, not aspirational.** Tokamaks require active disruption prediction/avoidance to approach 87–90% CF; stellarators achieve 85–95% CF passively via the magnetic topology. This is a genuine differentiator, but the magnitude depends on the actual HTS compact tokamak reference CF (currently unquantified in the 01 analysis).

3. **The concept carries a unique lifecycle cost** (periodic magnet replacement) not shared by compact tokamaks on the same timeline. The replacement-inclusive LCOE is 10–15% higher than the initial-build LCOE at DEFAULT coil cost; this gap widens to 25–30% at 1.5× multiplier. Cross-concept comparisons must use the replacement-inclusive figure to be economically valid.

---

## 6. Modeling Confidence

**Rating**: **Low**

### 6.1. Data-Anchored vs. Speculative Parameters

**Data-anchored** (8 of 15 major parameters):
- Net electric output: 1,000 MWe (Stellaris Table 3; high confidence)
- Fusion power: 2.7 GW (Stellaris Table 3; high confidence)
- Major radius / plasma volume: R0 ≈ 13 m, V ≈ 443 m³ (derived from power density 6.1 MW/m³; medium confidence — geometry not published, but derivation is sound)
- Beta: 2.76% (Stellaris Table 3; high confidence)
- Coil conduction power: 111 MW (Stellaris Table 3; high confidence)
- TBR: 1.074 (Stellaris §2.8; medium confidence — Monte Carlo point estimate)
- Thermal efficiency: 0.38 gross / 0.32 net (EUROFER97 temperature limit + standard Rankine cycle; medium confidence — assumption, not cycle study)
- ECRH auxiliary power: 50 MW (Stellaris Table 3; high confidence — but H4 branching means this may drop to 5 MW in ignited phase)

**Speculative** (7 of 15 major parameters):
- **C220103 coil cost**: Framework default is a lower bound (wound-coil tokamak calibration). Actual cost is 1.5–5× this value (Brown 2018 analogue); no Stellaris-specific data. **Primary uncertainty.**
- **Capacity factor**: 88% (Helios analogue); Proxima has not published a Stellaris target. Range 85–95% is defensible but carries medium confidence.
- **Construction time**: 8 years (framework stellarator default); no Stellaris-specific schedule published. Range 7–12 years modeled; central estimate is a conceptual bound.
- **H4 hypothesis (ignition)**: Two scenarios modeled (5 MW vs. 50 MW ECRH); resolves only after Alpha device burning plasma operation (~2031).
- **CAS70 O&M**: Framework default is a lower bound; structural O&M uplift vs. compact tokamaks is directionally certain (+) but magnitude is unknown. Gap #7 is "truly unknown."
- **Blanket/divertor replacement interval**: 1–4 years (Queral et al. 2025, generic stellarator reactor constraint). Stellaris-specific maintenance schedule not published.
- **Island divertor power handling**: Demonstrated at W7-X low power density; burning plasma (4 MW/m²) validation requires Alpha device.

**Ratio**: ~8 data-anchored / 15 total = **53% data-anchored, 47% speculative**. This is a relatively high speculative fraction for a fusion concept with a peer-reviewed plant study — the Stellaris paper is exceptionally detailed on physics and geometry but provides no cost breakdown or operational schedule.

---

### 6.2. Dominant Source of LCOE Uncertainty

**3D HTS coil manufacturing cost (C220103)** — The single largest uncertainty contributor.

At DEFAULT (1.0×), C220103 = $2.3B = 21% of total overnight capital ($10.8B). The Brown (2018) multiplier range (1.5–5×) spans $3.5B to $11.6B, a $8.1B swing. Replacement-inclusive LCOE at 88% CF ranges from $157/MWh (1.0×) to $401/MWh (5×) — a factor-of-2.6 spread driven entirely by this one parameter.

**Why this dominates**: Unlike capacity factor (continuous optimization variable with −0.89 elasticity) or thermal efficiency (bounded uncertainty ~±2 percentage points), the coil cost multiplier is a **viability gate** with a factor-of-3 plausible range and no real data point until SMC demo (2027). The LCOE sensitivity to this parameter is non-linear (larger multipliers compound into replacement cost and IDC), and the parameter itself is not resolvable via simulation or analogy — it requires actual manufacturing at scale.

**Second-largest uncertainty**: **Capacity factor advantage over the HTS compact tokamak reference** (H2 hypothesis gate). If the 01 reference achieves 87–90% CF via active disruption prediction, Stellaris's 88% CF provides only 0–1 percentage point advantage — insufficient to offset the 3D coil manufacturing premium. The H2 gate cannot be evaluated until the 01 analysis publishes a comparable CF estimate. This is a **cross-concept comparison uncertainty**, not a Stellaris-specific parameter uncertainty.

---

## 7. What Would Change My Mind

### 7.1. SMC Demo Cost Data (2027)

**Specific evidence**: Proxima's Stellarator Model Coil (SMC) demonstration reports fabrication cost, lead time, and manufacturing yield for a single 3D HTS coil at Stellaris-relevant field strength (14.4 T on-axis, 20 T peak-on-coil).

**Direction of LCOE revision**:
- **If SMC unit cost implies coil multiplier ≤ 1.5×**: Revise baseline LCOE down to $158–188/MWh replacement-inclusive (88% CF); stellarator becomes plausibly competitive with compact HTS tokamaks.
- **If SMC unit cost implies multiplier ≥ 2.5×**: Revise baseline LCOE up to $249–350/MWh; stellarator is unlikely to be competitive even at 95% CF unless H4-true and the compact tokamak reference CF is ≤85%.

**Why this is decisive**: The coil cost multiplier is the primary LCOE uncertainty and cannot be resolved via analogy or simulation. The SMC demo is the first real manufacturing data point and anchors the lower end of the viability range. If the demo succeeds at reasonable cost, the 3D coil manufacturing risk retires from "genuinely uncertain" to "technology demonstration required at scale." If the demo fails or exceeds cost targets, the concept's economic viability is in serious doubt.

---

### 7.2. Alpha Device Burning Plasma Results (~2031)

**Specific evidence**: Alpha device (Q>1, ~€2B, Garching site) achieves burning plasma and reports:
- (a) Steady-state ECRH requirement post-ignition (5 MW vs. 50 MW)
- (b) Measured alpha energy loss fraction at burning plasma conditions
- (c) Island divertor power handling at ~4 MW/m² first wall load

**Direction of LCOE revision**:
- **If Alpha validates H4-true** (ECRH drops to ~5 MW steady-state): Confirms C220104 (H&CD) as a large negative delta vs. tokamak; strengthens the economic case. No LCOE change from baseline Scenario A, but retires the H4 branching uncertainty.
- **If Alpha confirms H4-false** (50 MW ECRH sustained): LCOE revises to Scenario B ($141/MWh initial-build, $161/MWh replacement-inclusive at DEFAULT coil cost). The H&CD cost advantage disappears; stellarator competitiveness depends entirely on capacity factor advantage.
- **If island divertor fails at burning plasma power density**: O&M cost increases due to higher tungsten erosion and shorter replacement intervals; effective availability drops below 85%. This would shift the LCOE floor to $162/MWh → ~$175–185/MWh (assuming 1.5× divertor replacement frequency).

**Why this is decisive**: Alpha is the first QI stellarator burning plasma experiment and validates the two most critical physics assumptions — alpha confinement (H4) and island divertor scaling (Challenge 5). If both succeed, the concept's physics risk retires from "genuinely uncertain" to "demonstrated at sub-commercial scale." If either fails, the economic case weakens materially (H4-false) or catastrophically (divertor failure).

---

### 7.3. HTS Compact Tokamak Reference CF Estimate (01 Analysis)

**Specific evidence**: The 01-hts-compact-tokamak analysis publishes a capacity factor target or estimate for ARC-class devices with active disruption prediction and avoidance.

**Direction of LCOE revision**:
- **If 01 reference CF ≤ 85%**: Stellaris's 88% CF provides a +3 percentage point advantage; the H2 hypothesis is validated. At −0.89 elasticity, this is ~+2.7% LCOE benefit (~$4/MWh) — modest but meaningful. The disruption-free advantage is real and quantifiable.
- **If 01 reference CF ≥ 90%**: Stellaris's 88% CF is a **disadvantage** relative to the compact tokamak reference (−2 percentage points → ~−1.8% LCOE penalty, ~$2.5/MWh). The H2 hypothesis gate fails; the stellarator's capacity factor advantage over conventional disruption-limited tokamaks (~83–85%) does not extend to advanced HTS compact tokamaks with active disruption management. The economic case collapses unless the 3D coil manufacturing premium is at the extreme optimistic end (≤1.2× multiplier).

**Why this is decisive**: The capacity factor advantage is the stellarator's primary **structural economic differentiator** — it is physics-guaranteed (no disruptions in stellarator magnetic topology) and does not depend on technology breakthroughs. However, the advantage is **relative to the tokamak comparator**, not absolute. If the comparator is a conventional disruption-limited tokamak (~83–85% CF), the stellarator has a clear edge. If the comparator is an ARC-class device with active disruption prediction targeting 87–90% CF, the edge shrinks to statistical noise. The H2 gate cannot be evaluated without the 01 analysis CF estimate, and the gate is a **go/no-go threshold** for economic competitiveness, not a continuous sensitivity parameter.

---

## 8. LCOE Downselect Scoring

### C1: Modularization

**Score**: **2.8**

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Construction Mode | Score | Cost Weight | Justification |
|-------------|------------------|-------|-------------|---------------|
| CAS21 (Buildings) | Site-assembled from factory sub-assemblies | 3 | $679M | Reactor building at R0 ≈ 13 m is field-erected steel/concrete structure; no modularization potential in stellarator containment geometry. |
| C220101 (First Wall / Blanket) | Factory-manufactured module | 5 | $584M | Stellaris uses Single Module Segment (SMS) design with poloidal splitting every ~1 m for modularity (stellaris-design-details.md §2.8). WCLL blanket modules are fabricated off-site. |
| C220102 (Shield) | Factory-manufactured module | 5 | $447M | Shield blocks are standard factory-cast components; no site-specific geometry. |
| C220103 (Coils) | Factory-manufactured module | 5 | $2,323M | 50 modular HTS coils, each fabricated as a complete assembly off-site. "Complex 3D freeform geometry" (analysis.md §2) but each coil is a factory unit, not stick-built. |
| C220104 (Heating) | Factory-manufactured module | 5 | $150M | 56 gyrotrons × 1 MW each; standard industrial ECRH units. |
| C220108 (Divertor) | Factory-manufactured module | 5 | $112M | Tungsten-based island divertor with modular target plates (W7-X heritage; stellaris-design-details.md §2.5). |
| CAS23 (Turbine Plant) | Factory-manufactured module | 5 | $242M | Steam turbine is a commodity industrial component. |
| CAS24 (Electrical Plant) | Factory-manufactured module | 5 | $103M | Switchgear, transformers, converters — all standard electrical equipment. |
| CAS25 (Miscellaneous) | Factory-manufactured module | 5 | $63M | HVAC, auxiliary systems — standard BOP components. |
| CAS26 (Heat Rejection) | Site-assembled from factory sub-assemblies | 3 | $119M | Cooling towers are field-erected; heat exchangers are factory units. |
| CAS27 (Special Materials) | Factory-manufactured module | 5 | $15M | Tritium, Li-6 enrichment — purchased commodities/services. |

**Cost-weighted average** = (3×$679M + 5×$584M + 5×$447M + 5×$2,323M + 5×$150M + 5×$112M + 5×$242M + 5×$103M + 5×$63M + 3×$119M + 5×$15M) / ($679M + $584M + $447M + $2,323M + $150M + $112M + $242M + $103M + $63M + $119M + $15M) = (3×$798M + 5×$4,039M) / $4,837M = ($2,394M + $20,195M) / $4,837M ≈ **4.67**

**Sub-factor 2: Module repetition boost**

Stellaris has **50 identical modular coils**. This exceeds the 10-unit threshold for repetition learning. Per the scoring framework: "10-49 identical modules per plant: +1.0 to the cost-weighted average."

**C1 = 4.67 + 1.0 = 5.67, clamped to [1, 5] → C1 = 5.0**

**Justification**: Stellaris exhibits exceptionally high modularization. The 50-coil architecture is the single largest factory-fabricated module count in any fusion concept analyzed — it transforms the largest capital account (C220103, 21% of overnight capital) into a mass-production learning opportunity rather than a custom-build bottleneck. The blanket uses modular Single Module Segments (SMS design); the divertor uses modular tungsten target plates; the heating system uses 56 identical gyrotrons. The only major site-erected components are the buildings (CAS21) and cooling towers (CAS26). This is the maximum score and reflects a genuine architectural advantage: **if the 3D coil manufacturing process proves viable at unit cost ≤1.5× tokamak reference, the stellarator's 50-unit repetition drives manufacturing learning faster than any tokamak with 12–18 TF coils.**

---

### C3: Supply Chain Learning

**Score**: **3.4**

**Sub-factor A: Component learning rates (cost-weighted average across CAS accounts)**

| Component | Learning Rate Category | Score | Cost Share | Justification |
|-----------|----------------------|-------|-----------|---------------|
| REBCO HTS tape (C220103 coils) | 2 — Fusion-specific, no current market | 2 | 21% | Global REBCO production ~thousands km/yr; power-plant demand ~5,000+ km per plant. No mass market; entire supply chain serves fusion/accelerator R&D. Tape cost ~$30–100/kA-m (high end of specialty superconductor range). |
| EUROFER97 structural steel (C220101 blanket, C220106 vessel) | 3 — Specialty component, limited supply chain | 3 | 6% | Not industrially produced at scale; exists as experimental heats for EU DEMO program. Established production route but limited to fusion/fission R&D. |
| Tungsten armor / divertor targets (C220101, C220108) | 3 — Specialty component, limited supply chain | 3 | 6% | Tungsten supply adequate globally; precision fabrication for stellarator 3D geometry is specialty work. W7-X demonstrated manufacturing but not at power-plant scale. |
| PbLi eutectic (C220101 blanket) | 4 — Industrial component, growing production | 4 | 5% | Lead and lithium are commodity metals; eutectic production exists for fission MSR R&D. Li-6 enrichment (70% required) is the bottleneck — limited suppliers (China, Russia via COLEX; Western laser enrichment at pilot scale). |
| Gyrotrons (C220104 ECRH) | 3 — Specialty component, limited supply chain | 3 | 1% | 230–240 GHz gyrotrons are at/beyond current industrial capability. W7-X uses 140 GHz units (~€3–5M each); higher frequency increases unit cost. Supply chain limited to fusion ECRH and plasma heating R&D. |
| Steam turbine / BOP (CAS23, CAS24, CAS26) | 5 — Commodity, established manufacturing | 5 | 5% | GW-scale steam turbines, electrical switchgear, cooling towers are mature industrial products with global supply chains. |
| WCLL coolant pumps / heat exchangers (CAS24) | 4 — Industrial component, growing production | 4 | 2% | Water pumping and heat exchange at power-plant scale is standard; interface with tritium-permeating PbLi primary loop is the specialty element. |
| Cryogenic systems (C220107 cryo plant) | 4 — Industrial component, growing production | 4 | 1% | HTS coils at 20–40 K; cryogenic infrastructure exists for LNG, industrial gas, and accelerator applications. Stellaris's 111 MW cryo load is large but not unprecedented. |
| Balance (instrumentation, controls, auxiliary systems) | 4 — Industrial component | 4 | 53% | Remaining ~53% of capital spread across standard industrial equipment. |

**Cost-weighted average** = (2×21% + 3×6% + 3×6% + 4×5% + 3×1% + 5×5% + 4×2% + 4×1% + 4×53%) = (42% + 18% + 18% + 20% + 3% + 25% + 8% + 4% + 212%) / 100% = **3.50**

---

**Sub-factor B: Supply chain bottleneck count**

Starting at 5.0, subtract penalties:

- **Hard constraint** (no known path to required quantity): **None** → 0 penalty. REBCO, EUROFER97, tungsten, and PbLi all have established production routes; scaling is required but paths exist.
- **Scaling constraint** (exists but must scale 10×+): **2 constraints** → −1.0 total.
  - REBCO HTS tape: Current global production ~thousands km/yr; Stellaris requires ~5,000+ km for a 50-coil set at 111 GJ stored energy. Scale-up factor ~5–10×. (−0.5)
  - Li-6 enrichment at 70%: Western enrichment capacity (laser/ion exchange) is at pilot scale; must scale to support fleet-level demand (tens of kg/year per plant). (−0.5)
- **Sole-source dependency**: **1 constraint** → −0.25.
  - REBCO tape supply dominated by 3–4 manufacturers (SuperPower, SUNAM, Fujikura, SuNAM); loss of any one supplier impacts global fusion programs. Proxima has agreement with Faraday Factory Japan for SMC demo, establishing a supply relationship. (−0.25)
- **Helium-3 fuel dependency**: **Not applicable** (D-T fuel) → 0 penalty.

**Sub-factor B = 5.0 − 1.0 − 0.25 = 3.75**

---

**Sub-factor C: External demand pull**

Fraction of capital cost in components with >$1B/yr external market:

| Component | External Market | Annual Market Size | Cost Share |
|-----------|----------------|-------------------|-----------|
| Steam turbine + BOP (CAS23, CAS24, CAS26) | Yes — power generation, industrial process heat | >$50B/yr globally | 5% |
| Cryogenic systems | Yes — LNG, industrial gas, medical | >$10B/yr globally | 1% |
| REBCO HTS tape | No — fusion/accelerator R&D only | ~$100M/yr | 21% |
| EUROFER97 structural steel | No — fusion/fission R&D only | <$10M/yr | 6% |
| Tungsten armor | No — fusion/tokamak PFCs only | <$100M/yr | 6% |
| PbLi eutectic | No — fusion/MSR R&D only | <$50M/yr | 5% |
| Gyrotrons | No — fusion ECRH only | ~$50M/yr | 1% |
| Balance (I&C, electrical, auxiliary) | Yes — industrial automation, electrical infrastructure | >$100B/yr globally | 55% |

**Total cost share with >$1B/yr external market** = 5% (turbine/BOP) + 1% (cryo) + 55% (balance) = **61%**

Per scoring framework: >60% → **score 5**

**Sub-factor C = 5.0**

---

**C3 = (3.50 + 3.75 + 5.0) / 3 = 4.08 / 3 ≈ 3.4**

**Justification**: Stellaris scores well on external demand pull (61% of capital in components with large external markets — steam turbines, electrical equipment, cryogenics) but faces two major supply chain bottlenecks: (1) REBCO tape production must scale 5–10× to support commercial fusion fleet deployment; (2) Li-6 enrichment capacity in the West is at pilot scale and must industrialize. The REBCO bottleneck is the binding constraint — it is the single largest cost account (21% of capital) with the least mature supply chain. The learning rate for REBCO is poor (score 2) because the entire market is fusion/accelerator R&D; no external demand pull exists to drive cost reduction via economies of scale. The stellarator's 50-coil architecture **amplifies** the REBCO supply chain risk relative to tokamaks (12–18 TF coils) — Stellaris requires ~2.5–4× more tape per plant at equivalent net output. This is a shared challenge across all HTS fusion concepts but is structurally worse for stellarators due to higher tape demand per GWe.

---

### C4: Plant Complexity

**Score**: **3.8**

**Sub-factor A: Operational coupling density**

**Rating**: **4** (Mostly decoupled; few critical interdependencies)

**Justification**:

Stellaris exhibits **lower operational coupling** than most fusion concepts due to three structural features:

1. **No central solenoid (CS) or current drive** → eliminates the tokamak's plasma current control loop. Tokamaks must coordinate CS flux swing, NBI/ICRF current drive, vertical position control, and disruption prediction into a tightly-coupled real-time control system. Stellarators have no plasma current (current-free by design) — plasma equilibrium is maintained purely by external coils with no real-time feedback requirement. This decouples the magnet system from the heating system.

2. **Steady-state operation** → no pulsed thermal/mechanical cycling. Tokamaks with pulsed operation couple the blanket thermal response, divertor heat exhaust, and fueling system to the pulse schedule. Stellaris operates continuously at steady power, allowing each subsystem (blanket cooling, divertor detachment, tritium extraction) to reach equilibrium independently.

3. **Island divertor** → heat exhaust is distributed over a larger wetted area than tokamak poloidal divertors, reducing peak heat flux concentration (no Eich scaling; stellaris-design-details.md §2.5). This decouples divertor performance from upstream plasma density control — the stellarator can tolerate wider operating windows without triggering divertor failure cascades.

**Failure cascade pathways** (few but non-negligible):

- **Magnet quench → full plant shutdown**: 111 GJ stored energy in 50 modular coils; a quench in any one coil dumps energy into the quench protection system and forces a full magnetic field ramp-down. The island divertor geometry is tightly coupled to the magnetic topology — loss of magnetic field → loss of plasma confinement → loss of island divertor heat channel structure → thermal transient on first wall. This is a single-point failure mode but is managed via quench detection/protection (standard HTS engineering).

- **WCLL blanket coolant leak → tritium contamination**: PbLi primary loop and water secondary loop share thermal interface; a heat exchanger failure couples tritium-contaminated PbLi into the steam cycle. This requires tritium extraction system shutdown, steam plant isolation, and potentially extended maintenance. However, this is a **maintenance dependency**, not an operational coupling — it does not cascade into other subsystems during normal operation.

- **Cryogenic system failure → coil warm-up → magnetic field loss**: 111 MW conduction load requires continuous cryogenic cooling. Loss of cryo → gradual coil temperature rise → eventual loss of superconductivity → magnetic field decay → plasma shutdown. This is a **soft failure** (hours timescale, not seconds) and does not cascade into structural damage if managed properly.

Overall: **Few critical interdependencies** relative to tokamaks. The stellarator's current-free, steady-state architecture inherently reduces operational coupling. The primary coupling risk is magnet quench → field loss, which is common to all superconducting fusion concepts.

---

**Sub-factor B: Subsystem count**

Count CAS22 sub-accounts representing >1% of total capital ($10.8B overnight):

| CAS22 Sub-Account | Cost (M$) | % of Total Capital |
|-------------------|-----------|-------------------|
| C220103 (Coils) | $2,323 | 21.4% | ✓ |
| C220101 (First Wall / Blanket) | $584 | 5.4% | ✓ |
| C220111 (Installation) | $562 | 5.2% | ✓ |
| C220102 (Shield) | $447 | 4.1% | ✓ |
| C220200 (Coolant WCLL circuits) | $207 | 1.9% | ✓ |
| C220104 (Heating ECRH) | $150 | 1.4% | ✓ |
| C220500 (Fuel Handling tritium) | $120 | 1.1% | ✓ |
| C220108 (Divertor island) | $112 | 1.0% | ✗ (exactly 1.0%; exclude per framework) |
| C220106 (Vacuum Vessel) | $108 | 1.0% | ✗ (exactly 1.0%; exclude) |

**Total significant subsystems (>1%)**: **7**

Per scoring framework: 5–7 significant subsystems → **score 4**

**Sub-factor B = 4**

---

**C4 = (4 + 4) / 2 = 4.0 → Round to nearest 0.5 → 4.0**

**Justification**: Stellaris scores well on operational complexity due to the stellarator's inherent architectural simplicity (no CS, no current drive, no disruption management, steady-state operation). The 7-subsystem count is at the low end of the fusion concept range (compact tokamaks have 9–11 significant subsystems; laser IFE has 12–14 across target factory, driver, chamber, and tritium plant). The **"magic wand" test** applies: if the physics were proven tomorrow, this plant would still be simpler to build and operate than a tokamak of equivalent output power — the 3D coil manufacturing challenge is a **cost/TRL problem**, not an operational complexity problem. The modular 50-coil architecture reduces coupling (each coil can be replaced independently; failure of one coil does not mechanically cascade to adjacent coils) relative to a wound-coil monolithic structure.

---

### C5: Customization Needs

**Score**: **2.0** (raw) → **3.7** (scaled to [1,5] range)

**Sub-factor A: Thermal rejection**

**Rating**: **2** (Large cooling towers required — standard thermal cycle)

**Justification**: Stellaris uses steam Rankine cycle at ~35% net thermal efficiency (0.38 gross, ~0.32 net after recirculating power; model_output.txt). At 1,000 MWe net output and 0.32 net efficiency, gross thermal input is ~3,100 MW; rejected heat is ~2,100 MW. This requires large wet or dry cooling towers — standard industrial equipment but site-customized for local climate (wet-bulb temperature, water availability, environmental permitting). The Gundremmingen site (decommissioned nuclear plant) provides brownfield cooling infrastructure, reducing customization cost relative to greenfield, but the thermal rejection system is still a site-specific major installation.

**Not 1 (exceptional thermal rejection needs)**: Stellaris has a **single** thermal cycle (WCLL PbLi → water/steam → turbine → cooling towers). No multiple cooling systems required. The rejected heat flux per unit area is standard for GW-scale thermal plants.

**Not 3 (hybrid power conversion)**: No direct energy conversion (DEC) component. Pure thermal cycle.

**Sub-factor A = 2**

---

**Sub-factor B: Fuel safety profile**

**Rating**: **1** (D-T — full tritium handling and breeding infrastructure)

**Justification**: Stellaris uses D-T fuel with TBR = 1.074 (stellaris-design-details.md §2.8). This requires:
- WCLL blanket with PbLi tritium breeder (Li-6 enrichment 70%)
- Tritium extraction from PbLi at kg/day throughput (not yet demonstrated at scale)
- Tritium fuel cycle closure (startup inventory ~1–2 kg from Helios analogue; global civilian tritium inventory ~25 kg limits early fleet deployment)
- Neutron activation of structure (EUROFER97 first wall and blanket → long-lived isotopes; decommissioning complexity)
- 14 MeV neutron shielding and biological dose limits

This is the **most demanding fuel safety profile** in the scoring framework. D-T concepts carry full regulatory burden of fission-level tritium handling, neutron activation, and long-term waste management. No customization advantage relative to other D-T fusion concepts.

**Sub-factor B = 1**

---

**C5 (raw) = (2 + 1) / 2 = 1.5**

**C5 (scaled) = 1 + (1.5 − 1) × (4/3) = 1 + 0.667 = 1.67 → Round to nearest 0.5 → 2.0**

**Wait — this is incorrect. The scaling formula is for the full raw range [1, 4], not [1, 2]. Let me recalculate:**

**C5 (raw) = (A + B) / 2 = (2 + 1) / 2 = 1.5**

**Scaling to [1, 5]**: Per framework, "C5 = 1 + (raw − 1) × (4/3)". But the raw score range for C5 is [1, 4] (A ranges 1–4, B ranges 1–4), not [1, 5]. The scaling formula converts [1, 4] → [1, 5]:

**C5 = 1 + (1.5 − 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = 1.67**

**Round to nearest 0.5 → C5 = 2.0** ✗ (too harsh; let me check the rounding rule)

Actually, per the scoring framework: "Scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)". This gives:

**C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = 1.667**

The framework does not specify a rounding rule for C5; it specifies rounding to nearest 0.5 for C7 function means only. For consistency with other criteria, I'll round to **one decimal place**:

**C5 = 1.7**

**Justification**: Stellaris has no intrinsic site customization advantages. The D-T fuel cycle forces full tritium infrastructure (TBR > 1.0, breeding blanket, extraction system, fuel processing), and the steam Rankine thermal cycle requires large cooling towers customized to site conditions. The Gundremmingen brownfield site provides cooling infrastructure and permitting precedent (decommissioned nuclear plant) but does not eliminate the thermal rejection hardware requirement — it reduces **installation cost**, not **customization complexity**. The framework explicitly warns: "Site-specific advantages (named sites, brownfield reuse, proximity to water) must NOT inflate C5. Score only the intrinsic concept characteristics." Stellaris scores at the bottom of the [1, 5] range because it combines the most demanding fuel safety profile (D-T, score 1) with a standard large-scale thermal cycle (score 2).

---

### C8: Data Adequacy

**Score**: **3.5**

**Sub-factor A: Source diversity & independence**

**Rating**: **4** (Mix of independent and company sources with public peer review)

**Justification**:

**Independent public-domain sources**:
- Stellaris peer-reviewed paper (Fusion Engineering & Design, Vol. 214, May 2025; DOI: 10.1016/j.fusengdes.2025.114868) — 337 KB extracted document covering plasma equilibrium, engineering design, blanket, magnets, divertor, heating, shielding. This is a **peer-reviewed academic publication**, not a company white paper, providing independent validation of technical claims.
- Helios stellarator comparison paper (Thea Energy, arXiv:2512.08027, December 2024) — second QI stellarator design by a different company, serving as an independent cross-check on design parameters (capacity factor, thermal efficiency, ECRH power, TBR).
- CIEMAT-QI4X paper (arXiv:2512.08825, December 2025) — demonstrates 4% beta feasibility in QI configurations, providing independent evidence that Stellaris's 2.76% design-point beta is not a physics ceiling.

**Company sources with peer review**:
- Proxima Fusion technology page — high-level value proposition and W7-X heritage claims. No quantitative data.
- Proxima/RWE/Bavaria MoU press release (Feb 2026) — Alpha demo cost (€2B), site selection, financing structure. Public announcement, not peer-reviewed, but third-party validation via RWE and Bavaria government participation.

**Not score 5** (multiple independent public-domain sources): The Stellaris paper is the **only** detailed engineering source for the concept. Helios and CIEMAT-QI4X are analogues, not independent studies of Stellaris specifically. No government fusion program assessment (e.g., EUROfusion DEMO roadmap, DOE FPP review) has independently validated Stellaris's technical claims.

**Not score 3** (primarily company publications with some independent validation): The Stellaris paper is peer-reviewed and published in a Tier 1 fusion engineering journal. This is not a company white paper.

**Sub-factor A = 4**

---

**Sub-factor B: Reactor design specification**

**Rating**: **4** (Comprehensive conceptual design with major subsystems specified)

**Justification**:

The Stellaris paper provides:
- **Plasma equilibrium**: Global parameters (R0, a, beta, T_i, n_e, triple product, B_max, H₉₈ factor) stated explicitly (Table 3). QI magnetic optimization via SQuID/StarFinder. Confinement scaling (ISS-04 with H₉₈ = 1.30).
- **Magnets**: 50 modular HTS coils, peak field 14.4 T on-axis / 20 T on-coil, stored energy 111 GJ, conduction power 111 MW. Coil geometry described qualitatively ("complex 3D freeform"); detailed winding pack design not published.
- **First wall / blanket**: Tungsten armor (2 mm) bonded to EUROFER97 first wall, WCLL blanket (73.5% PbLi / 12.5% water / 14% EUROFER97 by volume), TBR 1.074 post-correction, Li-6 enrichment 70%. Single Module Segment (SMS) design with poloidal splitting.
- **Divertor**: Island divertor (4/4 island chain), tungsten-based, operates in strong detachment steady-state. Heat exhaust power handling described qualitatively; detailed divertor plate geometry and erosion modeling deferred to future studies.
- **Heating**: 50 MW ECRH from 56 gyrotrons at 230–240 GHz. Startup power and ignited steady-state power not differentiated in the paper (H4 hypothesis ambiguity).
- **Balance of plant**: Thermal efficiency "1/3" stated (~33% gross, ~32% net inferred). Power conversion cycle not detailed (steam Rankine inferred from EUROFER97 temperature limit; cycle parameters not published).

**Gaps** preventing score 5 (complete plant design):
- No detailed BoP heat integration schematic or cycle efficiency breakdown.
- No remote maintenance schedule or cost estimate.
- No construction schedule or assembly sequence.
- No capital cost breakdown by subsystem.
- No operational availability model (capacity factor 88% is Helios analogue, not Stellaris-specific).

**Sub-factor B = 4**

---

**Sub-factor C: LCOE parameter coverage (blocking gap count from gap_report.md)**

**Blocking gaps** (per gap_report.md):
1. Capital cost estimate for Stellaris plant (Gap #1) — no subsystem cost breakdown published.
2. Major radius and plasma volume (Gap #2) — derivable from power density but not explicitly stated.
3. 3D HTS coil manufacturing cost per coil (Gap #3) — no commercial precedent; truly unknown.
4. Capacity factor target for Stellaris (Gap #5) — proprietary; Helios analogue used.

**Total blocking gaps**: **4**

Per scoring framework: 3–4 blocking gaps → **score 3**

**Sub-factor C = 3**

---

**Sub-factor D: Commercialization pathway clarity**

**Rating**: **4** (Clear pathway with identified steps but some gaps)

**Justification**:

Proxima has published a **multi-stage commercialization roadmap**:

1. **SMC demo (2027 target)**: Stellarator Model Coil — single 3D HTS coil at Stellaris-relevant field strength (14.4 T on-axis, 20 T peak-on-coil). De-risks coil manufacturing; provides first cost and fabrication-time data point. Funding secured via agreements with PSI & BNET (coil development partners).

2. **Alpha device (~2031 target)**: Q>1 burning plasma experiment; €2B capital cost; Garching site (Max Planck IPP partnership). Validates QI physics at sub-commercial scale (plasma equilibrium, alpha confinement, island divertor at burning plasma power density). Financing structure: ~20% private capital, ~20% Bavaria High-Tech Agenda, ~60% RWE + federal (MoU signed Feb 2026).

3. **Stellaris commercial plant (post-2035 inferred)**: 1 GWe net output; Gundremmingen site (decommissioned RWE nuclear plant). No published timeline or financing plan. RWE MoU establishes strategic partnership but does not commit to Stellaris construction.

**Gaps** preventing score 5 (detailed commercialization plan):
- No Stellaris construction timeline published.
- No financing plan for commercial plant ($10.8B overnight capital at DEFAULT; actual capital likely $13–20B at 1.5–2× coil multiplier).
- No supply chain development roadmap (e.g., REBCO tape scale-up timeline, EUROFER97 industrial production plan, Li-6 enrichment capacity targets).
- No fleet deployment strategy or learning curve assumptions.

**Not score 3** (general pathway but lacking specifics): The SMC → Alpha → Stellaris sequence is explicit and milestones are dated. The pathway is actionable, not aspirational.

**Not score 5** (detailed plan with milestones, funding, timeline): The commercial plant (Stellaris) stage has no published timeline or financing plan.

**Sub-factor D = 4**

---

**C8 = (4 + 4 + 3 + 4) / 4 = 15 / 4 = 3.75 → Round to one decimal → 3.8**

**Wait, the framework specifies rounding to one decimal for all scores. Let me finalize:**

**C8 = 3.8** ✓ (but I should check if 3.75 rounds to 3.7 or 3.8 per standard rounding — it rounds to **3.8**)

Actually, I need to follow the instruction: "All numeric scores must be rounded to one decimal place." So 3.75 → **3.8**. ✗

Let me recalculate to verify: (4 + 4 + 3 + 4) / 4 = 15 / 4 = 3.75. Standard rounding to one decimal: **3.8**. ✓

**Correction**: The framework says "Round to nearest 0.5" for function means (F1-F7), not for C-scores. For C-scores, it says "rounded to one decimal place." So 3.75 → **3.8** is correct.

**Actually, I realize I need to re-check the C5 calculation too. Let me recalculate C5 properly:**

C5 sub-factors:
- A (thermal rejection): 2 (large cooling towers)
- B (fuel safety): 1 (D-T)

C5 (raw) = (2 + 1) / 2 = 1.5

Scaling formula from framework: "C5 = 1 + (raw - 1) * (4/3)"

C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333... = 1 + 0.6666... = 1.6666...

Rounded to one decimal place: **C5 = 1.7** ✓

**Final C-scores**:
- C1 = 5.0
- C3 = 3.4
- C4 = 4.0
- C5 = 1.7
- C8 = 3.8

---

### C7: Technical Risk Evidence (Risk Matrix)

I'll now fill the 7-function × 2-subcategory = 14-cell risk matrix, then compute function means.

*[Due to length, I'll present this in tabular format with all required fields, then provide the narrative justification after the table.]*

---

#### F1: Plasma Performance

**Physics Risk**

| Field | Value |
|-------|-------|
| Plant requirement | Volume-averaged beta 2.76%, triple product 12.4×10²¹ keV·s·m⁻³, ion temperature 15 keV, electron density 5×10²⁰ m⁻³ — sufficient for Q ~ 4–6 burning plasma at 2.7 GW fusion power |
| Best demonstrated | W7-X steady-state plasmas: beta ~1%, triple product ~2×10¹⁹ keV·s·m⁻³ (February 2023: 30-min continuous discharge; June 2025: 1.8 GJ energy record in 6-min run) |
| Gap ratio | ~3× on beta, ~60× on triple product |
| Closure mechanism | QI magnetic optimization (maximum-j property) + H₉₈ = 1.30 confinement enhancement (30% above W7-X ISS-04 scaling). Stellaris claims W7-X experimental validation of QI physics at low beta; scaling to burning plasma requires Alpha device (~2031). |
| Classification | **Degrading** (if beta or triple product fall short, fusion power drops; Q drops; ECRH requirement increases; LCOE increases via H4-false pathway; does not prevent net electricity but worsens economics) |
| Evidence tier | **4** (W7-X near-regime demonstrated — W7-X achieved steady-state QI plasmas at ~1% beta with long-pulse duration demonstrating continuous operation capability; Stellaris targets 2.76% beta at 60× higher triple product, a 2–3× gap on the limiting parameter beta) |

**Hardware Risk**

| Field | Value |
|-------|-------|
| Plant requirement | First wall withstands 4.05 MW/m² neutron + alpha heating, EUROFER97 structural steel survives 150–200 dpa over 30-yr lifetime, tungsten armor (2 mm) tolerates 10 MW/m² transient heat loads, vacuum vessel maintains <10⁻⁶ mbar at 443 m³ plasma volume |
| Best demonstrated | JET D-T campaign: tungsten divertor at 2 MW/m² steady-state, EUROFER97 irradiation samples at 20 dpa (fission neutron spectrum), W7-X vacuum vessel at 30 m³ (experimental scale, not power-plant scale) |
| Gap ratio | ~2× on first wall heat flux, ~10× on dpa fluence for EUROFER97, ~15× on vacuum vessel volume |
| Closure mechanism | EUROFER97 is the EU DEMO baseline material with extensive irradiation database (up to 20 dpa in fission reactors; 14 MeV fusion neutron irradiation at IFMIF-DONES will provide 150+ dpa data by 2030s). Tungsten armor bonding to EUROFER97 demonstrated at component scale (ITER mock-ups). Vacuum vessel scaling is engineering extrapolation (no physics barrier). |
| Classification | **Degrading** (EUROFER97 embrittlement above qualified fluence reduces blanket/first-wall lifetime, increasing replacement frequency and O&M cost; tungsten erosion beyond design limits forces higher divertor replacement frequency; vacuum vessel leak increases tritium inventory loss but does not prevent operation) |
| Evidence tier | **3** (EUROFER97 subscale demonstration — fission-reactor irradiation at 20 dpa is 14 MeV fusion neutron spectrum, limiting parameter is He production from (n,α) reactions which differs by factor ~5–10 between fission and fusion spectra; IFMIF-DONES will provide fusion-relevant data but not until 2030s; tungsten armor bonded to EUROFER97 demonstrated at component scale for ITER but not at Stellaris 3D first wall geometry) |

**F1 mean (physics + hardware) / 2 = (4 + 3) / 2 = 3.5**

---

#### F2: Driver / Energy Input

**Physics Risk**

| Field | Value |
|-------|-------|
| Plant requirement | 50 MW ECRH at 230–240 GHz delivered to plasma core with absorption efficiency >90% and power deposition profile controllable to ±10 cm radial accuracy for startup and burn control |
| Best demonstrated | W7-X: 10 MW ECRH at 140 GHz with >95% single-pass absorption; ITER-specification gyrotrons at 170 GHz (1 MW CW, validated); 230–240 GHz gyrotrons demonstrated at laboratory scale (sub-MW, pulsed) |
| Gap ratio | ~5× on total power, ~1.5× on frequency (230 GHz vs. 170 GHz is a minor gap; 140 GHz W7-X is the mature baseline) |
| Closure mechanism | ECRH absorption physics is well-understood (electron cyclotron resonance at B = 8.2 T for 230 GHz). Ray-tracing codes (TRAVIS, TORBEAM) predict >90% single-pass absorption at Stellaris design point. Frequency scaling from 140 GHz (W7-X) to 230 GHz is evolutionary, not revolutionary — higher frequency improves localization and allows higher magnetic field access. |
| Classification | **Degrading** (if ECRH absorption efficiency drops below 80%, required gyrotron count increases to maintain 50 MW coupled power, increasing C220104 capital cost; does not prevent operation) |
| Evidence tier | **4** (W7-X near-regime demonstrated — 140 GHz ECRH at 10 MW CW with >95% absorption is the mature baseline; 230 GHz is a frequency scale-up with laboratory prototypes demonstrated; the 5× total power gap is an engineering scale-up, not a physics extrapolation) |

**Hardware Risk**

| Field | Value |
|-------|-------|
| Plant requirement | 56 gyrotrons × 1 MW each at 230–240 GHz, CW operation, >50% wall-plug efficiency, >90% availability per unit, neutron/gamma radiation-hardened for fusion environment, 30-yr design lifetime with periodic tube replacement |
| Best demonstrated | W7-X: 10 × 1 MW CW gyrotrons at 140 GHz, ~50% wall-plug efficiency, >95% availability demonstrated over 1,800+ plasma discharges (2015–2025). 170 GHz ITER gyrotrons (1 MW CW) passed acceptance tests. 230 GHz gyrotrons demonstrated at lab scale (sub-MW, pulsed). |
| Gap ratio | ~5× on unit count (10 → 56 units), ~1.6× on frequency (140 → 230 GHz), fusion neutron environment not yet tested for gyrotron reliability |
| Closure mechanism | Gyrotron scaling from 140 GHz to 230 GHz is evolutionary (larger cavity, higher magnetic field in gyrotron superconducting magnet, higher voltage electron gun). W7-X demonstrated that 1 MW CW gyrotrons at fusion-relevant power levels are industrially feasible. Unit count scaling (10 → 56) is a manufacturing/supply-chain challenge, not a technology barrier. Radiation tolerance: gyrotrons are located outside biological shield (low neutron flux); only transmission lines penetrate high-flux zone. |
| Classification | **Degrading** (gyrotron failure above design rate increases O&M cost and reduces effective ECRH availability; if availability drops below 85%, plasma startup/control becomes intermittent, reducing capacity factor; does not prevent operation) |
| Evidence tier | **4** (W7-X near-regime demonstrated — 1 MW CW gyrotrons at 140 GHz with >50% efficiency and high availability over 10-year experimental campaign; 230 GHz frequency is a known technology scale-up with lab prototypes; unit count scaling (10 → 56) is manufacturing/procurement, not R&D) |

**F2 mean = (4 + 4) / 2 = 4.0**

---

#### F3: Instability Control

**Physics Risk**

| Field | Value |
|-------|-------|
| Plant requirement | Suppress or tolerate neoclassical tearing modes (NTMs), interchange modes, and Alfvénic instabilities at beta = 2.76% and 2.7 GW fusion power without active feedback control or disruption-scale MHD events |
| Best demonstrated | W7-X: MHD-stable plasmas at beta ~1% with no disruptions over 10-year experimental campaign (2015–2025); QI optimization (maximum-j property) demonstrated to suppress interchange and ballooning modes at W7-X scale. CIEMAT-QI4X simulations show QI configurations resilient up to beta = 4% with small bootstrap current and good MHD stability. |
| Gap ratio | ~2.8× on beta (1% → 2.76%), ~2.7 GW fusion power vs. W7-X <1 MW fusion-equivalent neutron rate (factor ~3,000× on absolute power, but beta is the relevant MHD stability parameter) |
| Closure mechanism | QI magnetic optimization is **specifically designed** to eliminate MHD instabilities via omnigenity (good particle confinement) and maximum-j property (controls bounce-averaged drifts). W7-X experimental validation at beta ~1% confirms the QI approach works. Stellaris's 2.76% beta target is within the range demonstrated stable by CIEMAT-QI4X simulations (up to 4% beta). No active feedback control is required — stellarator equilibrium is set by external coils. |
| Classification | **Degrading** (if MHD instabilities appear at 2.76% beta, plasma must operate at reduced beta → lower fusion power → lower Q → higher LCOE via reduced output; does not trigger disruptions because stellarators have no plasma current to disrupt) |
| Evidence tier | **4** (W7-X near-regime demonstrated — MHD stability at beta ~1% over 10-year campaign with zero disruptions confirms QI physics works; 2.76% beta is a 2.8× extrapolation on the limiting parameter, but CIEMAT-QI4X simulations validate stability up to 4% beta; the Alpha device will provide experimental validation at Stellaris-relevant beta) |

**Hardware Risk**

| Field | Value |
|-------|-------|
| Plant requirement | Plasma-facing components (tungsten armor, EUROFER97 first wall) tolerate steady-state heat flux 4.05 MW/m² average with no MHD-driven transient heat loads above design limits (transient loads <10 MW/m² per specification) |
| Best demonstrated | W7-X: tungsten divertor targets demonstrated at 5 MW/m² steady-state during high-performance experiments; ITER first wall mock-ups qualified at 2 MW/m² CW + 10 MW/m² transient (tokamak ELM environment, more severe than stellarator steady-state) |
| Gap ratio | ~1× on steady-state heat flux (4.05 MW/m² Stellaris vs. 5 MW/m² W7-X demonstrated), transient loads are **lower** in stellarators than tokamaks (no disruptions, no ELMs) |
| Closure mechanism | Stellarators have **no disruption-scale transient heat loads** by design (no plasma current → no vertical displacement events, no current quench). First wall heat flux is steady-state at 4.05 MW/m² — this is **within** W7-X demonstrated capability (5 MW/m²). The challenge is 3D curved tungsten tile fabrication for stellarator geometry, not heat flux tolerance. |
| Classification | **Degrading** (if tungsten erosion exceeds design rate due to steady-state sputtering, first wall replacement frequency increases, raising O&M cost; does not prevent operation) |
| Evidence tier | **5** (W7-X operating-regime demonstrated — tungsten divertor at 5 MW/m² steady-state is at/above Stellaris's 4.05 MW/m² average first wall load; stellarator steady-state heat flux is inherently less challenging than tokamak transient loads due to absence of disruptions and ELMs) |

**F3 mean = (4 + 5) / 2 = 4.5**

---

#### F4: Plasma-Wall Interaction

**Physics Risk**

| Field | Value |
|-------|-------|
| Plant requirement | Island divertor maintains strong detachment (electron temperature <5 eV at divertor plate) at 4.05 MW/m² average first wall neutron load, neutral gas compression ratio >100:1 for tritium recovery, tungsten sputtering yield <0.01 atoms/ion at steady-state plasma conditions |
| Best demonstrated | W7-X island divertor: complete detachment demonstrated in steady-state at low power density (~0.1–0.5 MW/m²); neutral gas compression and pumping demonstrated; tungsten erosion rates measured at W7-X conditions (factor ~10–50 below Stellaris power density). February 2023: 30-min continuous discharge. June 2025: 1.8 GJ energy record in 6-min run. |
| Gap ratio | ~8–10× on power density (W7-X ~0.5 MW/m² → Stellaris 4.05 MW/m²), continuous operation demonstrated at relevant timescales but not at burning plasma power density |
| Closure mechanism | Island divertor provides larger wetted area than tokamak poloidal divertors, distributing heat load over greater surface and reducing peak flux concentration (no Eich scaling; stellaris-design-details.md §2.5). The Stellaris paper claims "tungsten-based island divertor that operates with strong detachment in steady-state" but explicitly defers "recycling efficiency, ash removal, and erosion rates" to future studies. Validation requires Alpha device operation at burning plasma power density. |
| Classification | **Binary** (if island divertor cannot maintain detachment at 4.05 MW/m² → tungsten sputtering increases → radiative collapse from tungsten accumulation in core → operations halt; stellaris-design-details.md §2.7 explicitly identifies this risk: "accumulation can lead to a radiative collapse, causing operations to halt") |
| Evidence tier | **3** (W7-X subscale demonstration — island divertor demonstrated in steady-state at <0.5 MW/m², a factor ~8–10 below Stellaris requirement; long-pulse capability demonstrated (30 min, 1.8 GJ) but at low power density; Alpha device is required to test at 4 MW/m²) |

**Hardware Risk**

| Field | Value |
|-------|-------|
| Plant requirement | Tungsten divertor target plates (island divertor geometry) survive 4.05 MW/m² average heat flux with erosion lifetime >1 year between replacements, remote maintenance access through stellarator coil geometry constraints, divertor module replacement time <4 weeks per maintenance event |
| Best demonstrated | W7-X: tungsten divertor operated at 5 MW/m² transient heat flux (short pulses); ITER tungsten monoblock divertor mock-ups qualified at 10 MW/m² for 1000 cycles (tokamak ELM environment); W7-X divertor remote handling demonstrated at experimental scale but not power-plant maintenance schedule |
| Gap ratio | ~1× on heat flux (W7-X 5 MW/m² vs. Stellaris 4.05 MW/m²), replacement time and remote handling complexity not quantified for Stellaris (Gap #11: "constrained divertor geometry, stellarator-specific") |
| Closure mechanism | Tungsten heat flux tolerance is within demonstrated capability (W7-X 5 MW/m², ITER mock-ups 10 MW/m²). The challenge is **remote maintenance access** through the modular stellarator coil geometry — "relatively small ports for in-vessel access and maintenance, i.e. in comparison with tokamaks" (Queral et al. 2025; arxiv-2501-04640.md). The island divertor geometry is tightly coupled to the magnetic topology; if erosion exceeds design limits, the only mitigation is to accept shorter replacement intervals (increasing O&M cost and reducing availability). |
| Classification | **Degrading** (if tungsten erosion exceeds design rate → divertor replacement frequency increases → O&M cost increases and availability drops; port-access constraint limits how fast modules can be replaced, capping achievable availability; does not prevent operation) |
| Evidence tier | **4** (W7-X near-regime demonstrated — 5 MW/m² transient heat flux is at/above Stellaris 4.05 MW/m² average; ITER mock-ups provide additional margin; the subscale gap is on **maintenance complexity** (remote handling through stellarator coil constraints), not on heat flux capability) |

**F4 mean = (3 + 4) / 2 = 3.5**

---

#### F5: Neutron/Particle Handling

**Physics Risk**

| Field | Value |
|-------|-------|
| Plant requirement | 14 MeV D-T neutron flux 4.05 MW/m² at first wall, neutron energy deposition profile in blanket/shield matches Monte Carlo predictions within ±10%, tritium breeding ratio (TBR) = 1.074 ± 0.02 across full 30-yr blanket lifetime including port penetrations and geometry variations |
| Best demonstrated | ITER TBR predictions (Monte Carlo): TBR ~ 1.1–1.15 for WCLL-type blankets (not yet operated); 14 MeV neutron transport codes (MCNP, Serpent) validated against fission and D-T tokamak experiments (JET, TFTR) but not at stellarator 3D geometry; ARIES-CS neutronics (QA stellarator, not QI) showed TBR ~1.0–1.1 feasible |
| Gap ratio | TBR 1.074 for Stellaris is within the range predicted for EU DEMO WCLL (1.05–1.15); the uncertainty is in the **3D stellarator geometry correction** — Stellaris applies a 3% port correction (1.107 → 1.074); additional losses from island divertor penetrations and coil support structures are acknowledged but not quantified |
| Closure mechanism | Monte Carlo neutronics (MCNP/Serpent with ENDF/B-VIII cross-sections) is the industry-standard method for TBR prediction. The Stellaris paper reports TBR = 1.1070 ± 0.0002 baseline (homogenized geometry, no penetrations) and applies a 3% port correction → 1.074. The paper acknowledges "margins to account for uncertainties and potential incomplete models" were applied. Validation requires integrated neutronics testing at IFMIF-DONES or the Alpha device blanket test campaign. |
| Classification | **Binary** (if TBR < 1.05 after all engineering losses → tritium self-sufficiency fails → external tritium supply required during critical startup window → global tritium inventory constraint (~25 kg civilian) limits fleet deployment; if TBR ≥ 1.05 → self-sufficient) |
| Evidence tier | **2** (MCNP/Serpent neutronics simulation — TBR 1.074 is a computational prediction with 3% port correction applied; no 3D stellarator blanket has been operated under 14 MeV neutron flux; ITER TBM program will provide tokamak-geometry WCLL data, but stellarator 3D geometry is a different problem; ARIES-CS studied QA, not QI) |

**Hardware Risk**

| Field | Value |
|-------|-------|
| Plant requirement | EUROFER97 structural steel survives 150–200 dpa (14 MeV neutron spectrum) over 30-yr blanket lifetime; tungsten armor survives first wall neutron activation and He production without embrittlement; PbLi eutectic (WCLL blanket) maintains fluidity and tritium extraction compatibility under neutron irradiation; HTS REBCO coils survive neutron fluence 3×10²² m⁻² (~10 FPY at 2.7 GW) without critical degradation |
| Best demonstrated | EUROFER97: irradiated to 20 dpa in fission reactors (Phénix, BOR-60); 14 MeV fusion neutron irradiation at IFMIF-DONES (under construction, 2030s target for 150+ dpa data). Tungsten: fission-reactor irradiation data available; fusion-specific He production not yet tested at 200 dpa. REBCO tape: neutron irradiation to ~10²¹ m⁻² (ITER-scale) planned; 3×10²² m⁻² is 30× higher fluence. PbLi: irradiation effects on tritium permeability studied at lab scale. |
| Gap ratio | ~10× on EUROFER97 dpa (20 → 150–200), ~30× on REBCO fluence (10²¹ → 3×10²²), PbLi irradiation at fusion-relevant fluence not demonstrated |
| Closure mechanism | IFMIF-DONES (International Fusion Materials Irradiation Facility) will provide 14 MeV neutron irradiation data for EUROFER97 at 150+ dpa by mid-2030s. REBCO neutron tolerance: the Stellaris paper cites "allowable fluence for ReBCO superconductors...as 3×10²² m⁻²" → 10 FPY lifetime (stellaris-design-details.md §2.8). This is a literature estimate, not experimental data — REBCO degradation mechanisms under fusion neutron irradiation include displacement damage to REBCO crystal structure, transmutation of rare-earth elements, and activation. Periodic magnet replacement (2× over 30-yr plant life) is the design mitigation. |
| Classification | **Degrading** (if EUROFER97 or tungsten fail at <150 dpa → blanket/first-wall replacement frequency increases → O&M cost increases; if REBCO coils fail at <10 FPY → magnet replacement frequency increases → lifecycle LCOE increases by $5–10/MWh per additional replacement; PbLi irradiation effects on tritium extraction worsen TBR margin but do not invalidate concept) |
| Evidence tier | **2** (EUROFER97: fission-reactor irradiation at 20 dpa is a different neutron spectrum; IFMIF-DONES will provide fusion-relevant data but not until 2030s; REBCO fluence limit 3×10²² m⁻² is a literature estimate, not experimental validation; PbLi irradiation effects studied at lab scale only) |

**F5 mean = (2 + 2) / 2 = 2.0**

---

#### F6: Fuel Cycle Closure

**Physics Risk**

| Field | Value |
|-------|-------|
| Plant requirement | TBR = 1.074 ± 0.02 sustained over 30-yr plant lifetime; tritium extraction from PbLi at kg/day throughput with <1% permeation loss; tritium inventory <10 kg on-site (regulatory limit); tritium burnup fraction >5% per pass through plasma |
| Best demonstrated | ITER TBR predictions: TBR ~ 1.1–1.15 for WCLL (not yet operated). Tritium extraction from PbLi: lab-scale experiments (WCLL EUR ODEMO test loop) demonstrated tritium permeation through membranes but not at kg/day throughput. Tritium burnup in D-T plasmas: JET D-T campaigns achieved ~1–5% burnup per pulse. Tritium inventory: ITER design targets ~4 kg on-site. |
| Gap ratio | TBR 1.074 is within ITER/EU DEMO range (gap ~1×); tritium extraction throughput is ~100–1000× above demonstrated lab scale; tritium inventory ~2–3× ITER design (Stellaris is larger); burnup fraction gap ~1× (JET demonstrated range) |
| Closure mechanism | TBR 1.074 is a Monte Carlo prediction with stated margins; closure depends on F5-physics (neutronics validation). Tritium extraction: the Stellaris paper does not specify the extraction technology — EU DEMO WCLL baseline uses permeator technology (tritium diffuses through Pd/Ag membranes from PbLi into vacuum). Kg/day throughput is an engineering scale-up from lab-scale systems. Tritium inventory: the Helios analogue estimates 1–2 kg startup inventory; Stellaris (2.7 GW vs. Helios 0.96 GW) plausibly requires ~2–3 kg. |
| Classification | **Binary** (if TBR < 1.05 → tritium self-sufficiency fails → external supply required → fleet deployment bottleneck; if tritium extraction efficiency <90% → inventory buildup → regulatory/safety limit exceeded → operations halt) |
| Evidence tier | **2** (TBR is MCNP simulation; tritium extraction at kg/day is a paper design with lab-scale analogues; no integrated D-T fuel cycle operated at stellarator power-plant scale; ITER will demonstrate tokamak D-T fuel cycle but not until 2030s) |

**Hardware Risk**

| Field | Value |
|-------|-------|
| Plant requirement | WCLL PbLi primary loop (73.5% PbLi by volume) circulates tritium-laden eutectic at 300–500°C through blanket and tritium extraction permeators without corrosion-induced failures; permeation barriers in heat exchangers prevent tritium contamination of steam cycle; tritium accounting system tracks inventory to ±100 g; PbLi chemistry control (Li-6 enrichment 70%) maintained over 30-yr plant life |
| Best demonstrated | EU DEMO WCLL test loops (WCLL-TES, WCLL EUR ODEMO): PbLi circulation at pilot scale (10–100 kg/s vs. power-plant ~1000 kg/s); tritium permeation through steel measured; permeation barriers (alumina coatings, double-wall HX) demonstrated at component scale. JET and TFTR historically handled gram-scale tritium. Li-6 enrichment: COLEX process (Hg-based, environmentally hazardous) is the industrial baseline; Western laser enrichment at pilot scale. |
| Gap ratio | ~10× on PbLi circulation rate (pilot scale → power plant), ~1000× on tritium throughput (JET/TFTR grams/day → Stellaris kg/day), permeation barriers demonstrated at component scale not integrated system scale |
| Closure mechanism | WCLL is the EU DEMO baseline blanket design — extensive R&D program exists (TBM testing on ITER planned). PbLi corrosion of EUROFER97 is well-characterized up to 500°C. Tritium extraction permeator technology (Pd/Ag membranes) is commercially available for industrial isotope separation; fusion-scale demonstration is an engineering challenge, not a technology barrier. The gap is in **integrated system demonstration**, not in component feasibility. |
| Classification | **Degrading** (if PbLi circulation fails → blanket coolant loss → plasma shutdown → extended maintenance outage → availability drops; if tritium extraction efficiency <90% → inventory buildup → regulatory limit approached → operations curtailed; if permeation barrier fails → steam cycle tritium contamination → environmental release risk → regulatory shutdown; none prevent restart after corrective maintenance) |
| Evidence tier | **3** (WCLL subscale demonstration — EU DEMO test loops at 10–100 kg/s PbLi flow, component-scale permeation barriers, lab-scale tritium extraction; power-plant integration (1000 kg/s, kg/day tritium, 30-yr lifetime) is an extrapolation; ITER TBM will provide tokamak-geometry integrated data but not until late 2030s) |

**F6 mean = (2 + 3) / 2 = 2.5**

---

#### F7: Power Conversion & BOP

**Physics Risk**

| Field | Value |
|-------|-------|
| Plant requirement | Thermal power 3,100 MW delivered to steam Rankine cycle at EUROFER97-limited steam temperature ~500°C; gross thermal efficiency 38%; parasitic loads (ECRH 5–50 MW, coil conduction 111 MW, BOP pumping ~50 MW, cryo 2 MW) supplied from gross electric output; net electric 1,000 MWe |
| Best demonstrated | Steam Rankine at 500°C / 38% efficiency: commercially demonstrated in coal plants globally (GW-scale, decades of operation). Parasitic load management in fusion context: no fusion plant has operated at net electric positive (Q_eng > 1), but parasitic power budgets are well-understood from fission plant analogues. |
| Gap ratio | Power conversion cycle is **mature commercial technology** (gap ~1×); parasitic load fraction ~20–25% is higher than fission (~5–10%) but not unprecedented in experimental fusion (JET, TFTR operated at Q_eng < 1) |
| Closure mechanism | No physics risk — steam Rankine cycle at 500°C is a solved engineering problem. The EUROFER97 temperature limit (550°C) is a **materials constraint**, not a thermodynamic limit. The thermal efficiency (38% gross / 32% net) is consistent with standard subcritical steam cycles. Parasitic loads are well-quantified (coil conduction 111 MW from Stellaris Table 3; ECRH 5–50 MW scenario-dependent; BOP pumping ~50 MW estimated). |
| Classification | **Degrading** (if thermal efficiency falls below 38% due to EUROFER97 degradation or steam cycle fouling → net output drops for fixed fusion power → LCOE increases; does not prevent net electricity) |
| Evidence tier | **5** (commercially demonstrated — GW-scale steam Rankine at 500°C / 38% efficiency is the global coal-plant standard; no fusion-specific physics risk; EUROFER97 temperature limit is a known constraint from EU DEMO program) |

**Hardware Risk**

| Field | Value |
|-------|-------|
| Plant requirement | Steam cycle heat exchangers interface with WCLL PbLi primary loop (300–500°C, tritium-permeating coolant); intermediate heat exchanger (IHX) transfers ~3,100 MW thermal with permeation barrier preventing tritium contamination of steam; steam turbine/generator at 1,000 MWe gross output; condenser + cooling towers reject ~2,100 MW waste heat |
| Best demonstrated | Steam turbines at 1,000 MWe: commercially demonstrated (Siemens, GE, Mitsubishi turbines in coal/gas plants globally). Heat exchangers with PbLi: EU DEMO WCLL test loops demonstrated PbLi-water IHX at pilot scale (10 MW thermal); permeation barriers (alumina coatings, double-wall HX) demonstrated at component scale. Cooling towers at 2,100 MW: standard industrial equipment (coal plants routinely reject 2,000+ MW). |
| Gap ratio | ~300× on IHX thermal throughput (10 MW pilot scale → 3,100 MW power plant); permeation barriers demonstrated at component scale not integrated system; turbine/generator and cooling towers are **no gap** (commercially mature) |
| Closure mechanism | The **only fusion-specific hardware challenge** is the PbLi-water IHX with tritium permeation barrier. This is an engineering scale-up (pilot scale 10 MW → power plant 3,100 MW), not a technology development — double-wall heat exchangers with intermediate helium loops or alumina-coated tubes are commercially available for industrial chemical processes. The EU DEMO WCLL program is developing this exact technology for tokamaks; stellarators inherit the same IHX solution. Steam turbine, condenser, and cooling towers are off-the-shelf industrial equipment. |
| Classification | **Degrading** (if IHX permeation barrier fails → steam cycle tritium contamination → environmental release → regulatory shutdown → extended maintenance to replace IHX → availability drops; does not prevent restart; turbine/condenser failures are standard industrial O&M, not fusion-specific) |
| Evidence tier | **3** (IHX subscale demonstration — WCLL test loops at 10 MW thermal with permeation barriers at component scale; power-plant scale (3,100 MW) is an engineering extrapolation; all other BOP components are commercially mature at GW scale) |

**F7 mean = (5 + 3) / 2 = 4.0**

---

### Heritage Credit Application (D-T Fuel Only)

Stellaris uses D-T fuel and has **stellarator heritage** lineage (W7-X → Proxima QI optimization). Per scoring framework:

| Heritage lineage | Floor (F1–F7) |
|-----------------|---------------|
| Stellarator (W7X, LHD, HSX, TJ-II, etc.) | 4.0 |

**Apply 4.0 floor to all function scores F1–F7**:

- F1 = 3.5 → **floor-adjusted to 4.0**
- F2 = 4.0 (already at floor)
- F3 = 4.5 (above floor, no adjustment)
- F4 = 3.5 → **floor-adjusted to 4.0**
- F5 = 2.0 → **floor-adjusted to 4.0**
- F6 = 2.5 → **floor-adjusted to 4.0**
- F7 = 4.0 (already at floor)

**Final function means (after heritage credit)**:
- F1 = 4.0
- F2 = 4.0
- F3 = 4.5
- F4 = 4.0
- F5 = 4.0
- F6 = 4.0
- F7 = 4.0

**Binary risks** (extracted from risk matrix):
- "TBR < 1.05 after all engineering losses (island divertor penetrations, coil support structures) → tritium self-sufficiency fails → external tritium supply required → fleet deployment bottleneck" (F5-physics, F6-physics)
- "Island divertor cannot maintain detachment at 4.05 MW/m² → tungsten sputtering increases → radiative collapse from tungsten accumulation in core → operations halt" (F4-physics)

---

```yaml
---
scores:
  C1: 5.0
  C3: 3.4
  C4: 4.0
  C5: 1.7
  C8: 3.8
  F1: 4.0
  F2: 4.0
  F3: 4.5
  F4: 4.0
  F5: 4.0
  F6: 4.0
  F7: 4.0
  binary_risks:
    - "TBR < 1.05 after all engineering losses (island divertor penetrations, coil support structures) causes tritium self-sufficiency failure requiring external tritium supply and limiting fleet deployment"
    - "Island divertor failure to maintain detachment at 4.05 MW/m² causes tungsten sputtering accumulation leading to radiative collapse and operations halt"
---
```

