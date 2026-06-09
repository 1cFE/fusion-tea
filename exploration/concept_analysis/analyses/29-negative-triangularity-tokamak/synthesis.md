---
ID: 29-negative-triangularity-tokamak
Concept: Negative-Triangularity Tokamak
Company: Firefly Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

## Executive Summary

- **Single most important risk**: NT confinement scaling (H_98y2 = 1.44) is extrapolated from small experiments at TCV and DIII-D. If this scaling fails at reactor parameters, the design collapses: machine size grows, magnetic field increases, auxiliary heating becomes mandatory, and the claimed cost advantage over positive-triangularity tokamaks evaporates entirely.

- **Single most important advantage**: Plasma shaping inverts the tokamak cross-section to eliminate edge-localized modes passively and reduce scrape-off-layer power by 3.6× versus conventional tokamaks. This translates to M₁ = 57.3 MW·T/m (vs. 263 for ARC, 99 for EU-DEMO) — the divertor operates in a fundamentally less punishing environment than any other high-field tokamak concept.

- **LCOE ballpark**: Model yields **$507/MWh at 1 GWe NOAK projection** (native 90 MWe design point: $589/MWh). This is 17% higher than the library's generic tokamak baseline at the same scale ($432/MWh with overrides off). The MANTA academic study claims $396/MWh for a 550 MWe scaled plant; the discrepancy likely reflects optimistic capacity factor and magnet cost assumptions in the academic analysis versus library conservatism on component replacement cycles and REBCO tape pricing.

- **Confidence verdict**: **Medium**. The design-point physics is well-documented (MANTA paper provides complete reactor specifications and cost breakdowns), but two critical parameters are extrapolated from small-scale experiments without reactor validation: (1) NT confinement enhancement H_98y2 = 1.44, and (2) ohmic-only heating feasibility at B = 11 T. The FLiBe liquid immersion blanket is TRL 2-3 and has never been demonstrated in a tokamak. REBCO magnet lifetime under 14 MeV neutron flux is unproven. These are resolvable uncertainties, not fundamental barriers, but they dominate cost projection confidence.

## What Matters Most for LCOE

Ranked by LCOE sensitivity magnitude:

### 1. NT Confinement Scaling (H_98y2 = 1.44) — Assumed; Baseline Sensitivity Elasticity Unknown, Directionally Dominant

**Assumed value**: H_98y2 = 1.44 (DIII-D NT campaign extrapolation, manta-reference-design.md §2 Table 1)

**Source confidence**: Low. Extrapolated from DIII-D experiments with I_p < 2 MA, β_N ~ 3.5, limited high-density radiative operation. No reactor-scale (I_p = 10 MA, ⟨n⟩ = 1.95 × 10²⁰ m⁻³, f_GW = 0.88) NT plasma has been demonstrated.

**Sensitivity magnitude**: The model does not expose H_98y2 as a direct input parameter — it back-solves fusion power from net electric output and auxiliary heating. However, confinement sets Q, which determines whether the machine can produce the target fusion power at the specified size and field. If H_98y2 drops from 1.44 to 1.1 (positive-triangularity H-mode baseline), MANTA at R0 = 4.55 m, B = 11 T, p_input = 40 MW would fail to reach 450 MW fusion power. The design would require either larger size (higher R0 → higher capital cost proportionally) or stronger field (higher B → higher REBCO tape cost and structural loads) to compensate. A ~25% drop in confinement would plausibly increase overnight cost by 30-50%, translating to LCOE rising from $507/MWh to $650-750/MWh.

**What would flip the economic conclusion**: If H_98y2 falls below ~1.2, NT tokamaks lose compactness advantage over conventional PT designs. The concept reverts to "tokamak with unusual plasma shape" and offers no cost benefit. Conversely, if H_98y2 = 1.44 validates and stabilizes, NT becomes the preferred tokamak variant for compact high-field machines.

---

### 2. REBCO Tape Cost — $40/kA·m Assumed; Model Elasticity ~20-25% LCOE per 2× Tape Cost

**Assumed value**: $40/kA·m (manta-reference-design.md §7.1, commercial target pricing)

**Source confidence**: Medium. Current commercial tape (superOx, Shanghai Superconductor) meets J_c = 1000 A/mm² at 25 K, 25 T. CFS and Tokamak Energy target $10/kA·m for long-term viability; MANTA uses $40/kA·m as a near-term NOAK estimate. Industry consensus is that $20-50/kA·m is achievable with learning curve, but not yet demonstrated at >5,000 km production scale.

**Sensitivity magnitude**: TF coil cost is $1,500M at the native 90 MWe scale — 44% of the $3.4B overnight cost. MANTA sensitivity analysis (not quantified in detail) states that ±50% REBCO cost keeps overnight below $5B, implying a band of [$3.0B, $4.7B]. Translating to LCOE via the model's overnight-to-LCOE relationship: at 2× tape cost ($80/kA·m), TF coils rise from $1,500M to ~$2,200M, adding $700M to overnight ($4.1B total, +21%). LCOE scales slightly sublinearly with overnight cost due to fixed O&M and fuel components, so 2× REBCO → ~+18-22% LCOE, putting the 1 GWe NOAK projection at $600-620/MWh instead of $507/MWh.

**What would flip the economic conclusion**: If REBCO tape costs stay above $60/kA·m at scale, NT tokamaks are marginally more expensive than fission ($100-150/MWh LCOE) by a factor of 4-5×, making them uncompetitive without substantial carbon pricing ($200+/tonne CO₂). If REBCO reaches $10/kA·m (CFS long-term target), TF coils drop to ~$400M, overnight falls to $2.9B, and LCOE approaches $380-400/MWh — within striking distance of natural gas with carbon capture.

---

### 3. Ohmic-Only Heating Feasibility — Uncertain; Binary $370M Capex Swing + Opex Reduction

**Assumed value**: 40 MW ICRF auxiliary heating (p_input = 40 MW in model spec). Ball et al. claim ohmic-only operation viable at Q = 500 for the same MANTA parameters (B = 11 T, H_NA = 2.0).

**Source confidence**: Low. Ball et al. demonstrate that ohmic NT is field-strength-conditional: it fails at ITER-level fields (B ~ 5.3 T) but succeeds sharply at SPARC-level fields (B ~ 12.2 T, Q ≈ 80 vs. Q ≈ 12 for PT H-mode). MANTA at B = 11 T sits near the lower edge of the viable regime. The threshold depends on H_NA = 2.0 holding at reactor scale, which is unvalidated. MANTA retains 40 MW ICRF as a conservative fallback.

**Sensitivity magnitude**: MANTA reports ICRF capital cost at $370M (Table C1). The model does not override C220104 (auxiliary heating), so the library computes heating cost from p_input = 40 MW, yielding C220104 = $222.8M at native scale (Table output). This is 40% below MANTA's $370M — the discrepancy suggests the library's heating cost scaling is optimistic or MANTA includes integration/balance-of-plant margins not captured in the library default. If ohmic-only validates and auxiliary heating is eliminated entirely, the native overnight cost drops by $220-370M (5-8% of $4.4B), and LCOE falls by ~$30-50/MWh. Additionally, recirculating power for heating (40 MW wallplug ≈ 80 MW thermal dissipation) is eliminated, improving net plant efficiency and reducing cooling system size — a further ~1-2% LCOE reduction.

**What would flip the economic conclusion**: Ohmic-only alone does not change the competitive position (the LCOE reduction is modest, $30-50/MWh). However, if ohmic-only validates *and* NT confinement scaling holds, the combination delivers compactness + capital cost reduction + simpler plant integration. This would make NT the preferred tokamak configuration for pilot plants and early commercial units. If ohmic-only fails and H_98y2 = 1.44 fails, NT loses all differentiation versus conventional PT tokamaks.

---

### 4. Capacity Factor — 79% Assumed; ~1:1 Elasticity (LCOE ∝ 1/Availability)

**Assumed value**: 79% effective availability (90% thermal storage duty cycle × 88% maintenance availability, with PF2 replacement every ~2 full-power years taking 2 months downtime)

**Source confidence**: Medium-Low. The 88% maintenance availability is aggressive for a first-of-a-kind plant with undemonstrated remote handling under full neutron activation. ITER targets 30% availability initially, ramping to 50% over decades. MANTA assumes NOAK maturity but does not quantify remote handling system reliability or demonstrate 2-month PF coil replacement turnaround at high activation levels.

**Sensitivity magnitude**: LCOE scales inversely with capacity factor when capital-dominated. At 79% → 60% availability (plausible for FOAK), revenue falls by 24% while capital costs remain fixed, increasing LCOE by ~1.3× to $660/MWh. At 85% availability (optimistic NOAK), LCOE drops to $470/MWh. The model does not expose availability as a swept parameter, but the relationship is near-linear for capital-intensive plants.

**What would flip the economic conclusion**: If real-world availability settles at 60-65% (fission PWR typical levels for mature plants, but fusion has no operating fleet to benchmark), LCOE exceeds $650/MWh and NT tokamaks are uncompetitive even with carbon pricing. If demountable TF coils and modular FLiBe blanket enable fractional replacement strategies (Schwartz et al. 2024 show 15% value gain from optimized seasonal maintenance timing), LCOE could drop below $450/MWh at 85% effective availability with maintenance timed to low-price grid periods.

---

### 5. FLiBe Blanket TBR and Supply Chain — TBR = 1.15 Assumed; Material Cost $28.6M Native, Underscaled at Fleet

**Assumed value**: TBR = 1.15 (neutronics prediction for liquid immersion FLiBe blanket, manta-reference-design.md §2 Table 1). FLiBe material cost: 169 t × $169/kg = $28.6M.

**Source confidence**: Low for TBR (predictive neutronic calculation, never demonstrated in tokamak); Medium for material cost (FLiBe pricing is known from molten salt fission reactor community, but beryllium supply is constrained at 300 t/year global production).

**Sensitivity magnitude**: The model treats CAS27 (breeder material) as a per-site fixed cost, not per-module, so fleet cost stays at $28.6M regardless of n_mod. In reality, each of the ~11 modules at 1 GWe needs its own 169 t FLiBe inventory, making the true fleet total ~$314M (~$28.6M × 11). The gap (~$285M) translates to ~$3/MWh LCOE undercount at 1 GWe. This is a modeling artifact, not a design feature.

More critically, if TBR falls below 1.0 in real-world operation (due to impurities, thermal gradients, incomplete neutron capture, or tritium extraction losses), the plant cannot sustain D-T fusion without external tritium supply — which does not exist at scale. TBR < 1.0 is a show-stopper. TBR = 1.15 provides 15% margin, but the liquid immersion blanket is TRL 2-3 with no experimental validation. If TBR falls to 1.05, the margin shrinks to 5% and tritium inventory management becomes a knife-edge operational constraint. If TBR < 1.0, the concept is non-viable regardless of cost.

**What would flip the economic conclusion**: TBR validation above 1.10 with demonstrated tritium extraction at kg/day rates would retire the tritium self-sufficiency risk entirely. TBR below 1.05 would force blanket redesign (likely reverting to modular solid breeder schemes like ITER TBM baseline), eliminating the liquid blanket's serviceability advantage and adding first-wall replacement complexity.

---

## Risk Verdicts

### 1. NT Confinement Scaling (H_98y2 = 1.44) at Reactor Parameters

**Verdict**: **Genuinely uncertain**

**Rationale**: DIII-D and TCV NT experiments show promise (H_98y2 ~ 1.0-1.5 in diverted configurations, ELM-free operation, high β_N), but the database is thin and limited to I_p < 2 MA, β_N ~ 3.5. Scaling to I_p = 10 MA, f_GW = 0.88, sustained radiative divertor operation is unvalidated. The physics is not ruled out, but it is not proven.

**What would retire this risk**: High-power long-pulse NT experiments on DIII-D, KSTAR, or EAST with reactor-relevant heating (P_input > 10 MW), density (f_GW > 0.8), and impurity seeding for radiative divertor detachment. If H_98y2 > 1.3 holds for >100 s pulses at high β_N, the scaling is likely robust. If H_98y2 drops below 1.2, the concept requires larger size or higher field to compensate.

---

### 2. FLiBe Liquid Immersion Blanket TBR = 1.15 and Tritium Extraction at kg/day Rates

**Verdict**: **Unlikely resolvable without major demonstration campaign**

**Rationale**: The toroidally continuous FLiBe blanket is architecturally novel for tokamaks. No tokamak has operated with a liquid blanket at any scale. TBR = 1.15 is a neutronic prediction; real-world breeding performance depends on FLiBe purity, thermal stratification, tritium extraction efficiency, and V-4Cr-4Ti vacuum vessel permeation losses — none of which are validated. Tritium extraction from flowing molten salt at kg/day rates is TRL 3 (lab-scale only). This is not a "table-stakes" engineering problem; it requires a multi-year, multi-hundred-million-dollar demonstration program.

**What would retire this risk**: A dedicated FLiBe blanket test facility with 14 MeV neutron source (e.g., IFMIF-DONES or a D-T neutron source) operating at fusion-relevant thermal power (tens of MW) for thousands of hours, with validated tritium extraction and TBR measurement. Alternatively, a pilot tokamak (D-D or low-power D-T) operating with a scaled liquid FLiBe blanket to demonstrate flow stability, thermal management, and tritium accountability. Timeline: 10-15 years minimum.

---

### 3. REBCO HTS Magnet Lifetime Under 14 MeV Neutron Flux at >50 dpa

**Verdict**: **Likely resolvable** (shared with all HTS tokamak concepts)

**Rationale**: REBCO tape degradation under neutron irradiation is a known challenge but is being actively addressed by CFS, Tokamak Energy, and the broader HTS magnet community. Neutron irradiation campaigns at facilities like LANSCE and HFIR are ongoing. Tape insulation radiation hardening and joint reliability under thermal/mechanical cycling are TRL 5-6. This is not specific to NT tokamaks — every HTS tokamak concept faces the same neutron lifetime question.

**What would retire this risk**: Neutron irradiation testing of REBCO tape, insulation, and demountable joints at >50 dpa (fusion-relevant fluence for 30-year lifetime) with post-irradiation J_c and mechanical strength measurements. CFS SPARC and Tokamak Energy Demo4 magnet campaigns will provide data by 2028-2030. If REBCO tape retains >80% of initial J_c at 50 dpa, magnet lifetime risk is retired. If degradation exceeds 30%, magnet replacement cycles shorten and LCOE rises proportionally.

---

### 4. Ohmic-Only Heating at B = 11 T with H_NA = 2.0

**Verdict**: **Genuinely uncertain** (conditional on NT confinement scaling)

**Rationale**: Ball et al. provide a clear physics argument: ohmic heating power scales as B⁴, and NT confinement scales better than PT at high field, so there is a field-strength threshold above which ohmic-only becomes viable. MANTA at B = 11 T sits near this threshold. If H_NA = 2.0 holds (already uncertain per Risk #1), ohmic-only is plausible. If H_NA drops to 1.5, the threshold shifts upward and MANTA requires auxiliary heating.

**What would retire this risk**: Experimental demonstration of ohmic-only NT plasma at Q > 10 on a high-field device (B > 10 T). This could be done on a dedicated NT pilot experiment (e.g., Firefly's commercial prototype or a DIII-D upgrade campaign with stronger field). If ohmic-only achieves Q > 20 at B = 11-12 T with H_NA > 1.8, the risk is retired. If Q saturates at <5, ohmic-only is ruled out and auxiliary heating is mandatory.

---

### 5. Remote Handling Turnaround Time (2-Month PF2 Replacement)

**Verdict**: **Likely resolvable** (shared with all tokamaks)

**Rationale**: Remote handling at fusion activation levels is TRL 6-7 (ITER prototypes exist). The 2-month PF coil replacement timeline is aggressive but not implausible if demountable TF coils enable vertical access. The challenge is operational reliability and dose accumulation for maintenance staff, not fundamental technology readiness.

**What would retire this risk**: ITER or a pilot tokamak demonstrating full remote handling cycle for activated components (blanket cassettes, divertor segments, or PF coils) with measured turnaround time and dose tracking. If ITER achieves <3 months for divertor cassette replacement, MANTA's 2-month PF2 cycle is credible. If ITER turnaround exceeds 6 months, MANTA's availability assumption (88%) is optimistic and LCOE rises.

---

### 6. V-4Cr-4Ti Vacuum Vessel Fabrication and FLiBe Compatibility at Multi-Hundred-Tonne Scale

**Verdict**: **Unlikely resolvable without dedicated supply chain development** (but not a show-stopper)

**Rationale**: V-4Cr-4Ti has been produced at kg to tonne scale for fusion materials testing but never at reactor-vessel scale (hundreds of tonnes). Vanadium is a byproduct of steel/titanium processing, and global V-4Cr-4Ti alloy production capacity is near-zero. This is a supply chain development challenge, not a materials science barrier. Alternatively, MANTA could substitute ODS ferritic steels or explore SiC/SiC composites (both at similar TRL).

**What would retire this risk**: Industrial-scale V-4Cr-4Ti heat production (>100 t batches) with controlled impurities (O/C/N/H) and demonstrated welding/joining at reactor-vessel scale. Alternatively, validation of an alternative structural material (ODS, SiC/SiC) for FLiBe compatibility and neutron damage resistance. This is a 5-10 year development program with moderate capital investment ($50-100M for heat production and qualification testing).

---

## Structural Advantages and Disadvantages

Comparison baseline: conventional D-T tokamak (positive triangularity, solid ceramic breeder blanket, REBCO HTS magnets, ICRF/ECRH auxiliary heating). Quantified where model or sources permit.

### Advantages (+)

**1. Divertor Heat Load Reduction: P_SOL = 23.5 MW vs. ~80 MW for PT Tokamaks**

NT plasma shaping naturally redistributes heat flux to reduce scrape-off-layer power. MANTA's M₁ = 57.3 MW·T/m vs. ARC V1 (PT) = 263, EU-DEMO = 99. This is a genuine physics advantage — the plasma edge is intrinsically more benign.

**TEA impact**: Divertor capital cost is comparable ($150M MANTA vs. ~$100-200M typical tokamak), but *replacement frequency* should be lower. MANTA does not quantify divertor lifetime, but if NT extends tungsten monoblock life from 5 years to 10 years (halving replacement cycles), capacity factor improves and replacement capex per MWh falls proportionally. **Magnitude: ~1-2% LCOE reduction if divertor lifetime doubles.** Confidence: medium (physics is validated on DIII-D; engineering lifetime is undemonstrated).

**2. Passive ELM Elimination: No RMP Coils Required**

PT tokamaks require resonant magnetic perturbation coils or pellet pacing systems to suppress edge-localized modes (ELMs). NT eliminates ELMs passively through plasma shaping.

**TEA impact**: RMP coil cost is small ($30-50M estimated), but system integration, power supplies, and operational complexity are avoided. **Magnitude: ~$50M capital cost saved (1% of overnight).** Confidence: high (NT ELM-free operation is experimentally validated on TCV and DIII-D).

**3. Potential Ohmic-Only Operation: Eliminates $220-370M Auxiliary Heating Capex**

If Ball et al. ohmic-only heating validates at B = 11 T with H_NA = 2.0, ICRF/ECRH systems are unnecessary. This also eliminates waveguide penetrations, reduces first-wall complexity, and eliminates ~40 MW recirculating power.

**TEA impact**: $220-370M capex reduction + ~2-3% net efficiency improvement from eliminating heating recirculating power. **Magnitude: ~$40-60/MWh LCOE reduction.** Confidence: low (ohmic-only is field-strength-conditional and depends on unvalidated H_NA scaling).

**4. Conventional Aspect Ratio Enables Higher TBR: 1.15 vs. <1.05 for Spherical Tokamaks**

NT tokamaks use A ~ 3-4, allowing thicker inboard blanket compared to spherical tokamaks (A < 2). MANTA achieves TBR = 1.15 with liquid FLiBe blanket; spherical tokamaks struggle to exceed 1.05 due to inboard space constraints.

**TEA impact**: Tritium self-sufficiency margin is larger, reducing breeding risk. **Magnitude: qualitative advantage (no direct LCOE impact unless TBR < 1, which is existential).** Confidence: medium (TBR = 1.15 is neutronic prediction, not demonstrated).

### Disadvantages (−)

**1. NT Confinement Scaling Uncertainty: H_98y2 = 1.44 Unvalidated at Reactor Scale**

If H_98y2 drops to PT H-mode baseline (~1.0-1.1), MANTA requires larger R0 or higher B to compensate. This eliminates compactness advantage and increases capital cost.

**TEA impact**: If H_98y2 = 1.1 (30% degradation), overnight cost rises by 30-50% to maintain fusion power. **Magnitude: +$150-250/MWh LCOE penalty.** Confidence: medium-low (DIII-D shows H_98y2 ~ 1.4 at small scale, but reactor extrapolation is unproven).

**2. Passive Vertical Stabilizer Plates Required: NT Intrinsically Less Stable Than PT**

NT is less vertically stable than PT at the same elongation (κ = 1.8), and stability degrades at higher poloidal beta. Passive conducting plates (HFS + LFS) are required to reduce vertical instability growth rates by ~75% (Guizzo et al. 2025).

**TEA impact**: Plates add fabrication complexity and VV integration constraints. Cost increment is small (~$10-30M estimated) but is NT-specific. **Magnitude: <1% LCOE penalty.** Confidence: medium (Guizzo et al. analyses are specific to NT pilot plants).

**3. FLiBe Liquid Immersion Blanket is TRL 2-3: No Tokamak Demonstration Exists**

The toroidally continuous FLiBe tank is architecturally novel. Conventional tokamaks use modular solid breeder blankets (ITER TBM baseline at TRL 5-6). Liquid blanket technology requires FLiBe flow stability, tritium extraction at kg/day rates, and V-4Cr-4Ti vacuum vessel compatibility under neutron flux — all undemonstrated.

**TEA impact**: If FLiBe blanket fails validation, MANTA reverts to modular solid breeder (Li₄SiO₄ pebbles), losing the serviceability advantage and adding first-wall replacement complexity. **Magnitude: reverting to solid breeder likely adds $200-400M blanket cost (5-9% LCOE penalty) and reduces TBR margin.** Confidence: low (liquid blanket is speculative for tokamaks; solid breeder fallback is technically feasible but defeats the design rationale).

**4. V-4Cr-4Ti Vacuum Vessel Supply Chain Does Not Exist at Scale**

V-4Cr-4Ti production is kg to tonne scale; MANTA requires hundreds of tonnes. Global vanadium production is adequate (100,000 t/year), but V-4Cr-4Ti alloy with controlled impurities has never been produced at reactor-vessel scale.

**TEA impact**: Supply chain development requires 5-10 years and $50-100M investment. If V-4Cr-4Ti fails to scale, alternatives (ODS ferritic steels, SiC/SiC composites) are at similar TRL and require parallel qualification. **Magnitude: supply chain delay is a schedule risk, not a cost penalty if substitutes are viable.** Confidence: medium (vanadium supply is adequate; alloy production scale-up is solvable with investment).

**5. Demountable TF Coils Add Resistive Losses and Power Supply Cost**

Demountable joints enable vertical maintenance access but add $45M in power supplies and resistive leads (18 coils × $2.5M per coil). Resistive losses in joints reduce net efficiency by ~0.5-1%.

**TEA impact**: $45M capex penalty + ~1% efficiency loss. **Magnitude: ~$5-10/MWh LCOE penalty.** Confidence: high (MANTA explicitly includes demountable joint costs).

---

## Cross-Concept Positioning

### Where NT Sits in the Tokamak Landscape

**Negative-triangularity tokamaks occupy the "compact high-field tokamak with passive edge stability" niche.**

They share the HTS magnet technology base with CFS (ARC), Tokamak Energy (ST40), Energy Singularity (HH70), and Neo Fusion (BEST), but differentiate through plasma shaping to achieve lower divertor heat loads and potentially eliminate auxiliary heating. The closest comparable is **01-hts-compact-tokamak (CFS ARC)**, which uses similar R0, B, and REBCO magnets but with positive triangularity plasma shaping. NT trades PT's larger experimental database for claimed improvements in divertor power handling and confinement at high field.

### What Concepts Share Similar Economics?

**All HTS tokamak concepts (CFS, Tokamak Energy, Energy Singularity, Neo Fusion, Firefly)** share:
- REBCO tape supply chain and learning curve
- Tritium breeding requirement (TBR > 1 mandatory)
- Remote handling complexity under 14 MeV neutron activation
- Balance-of-plant thermal cycle (Rankine or Brayton)
- Tungsten divertor and first-wall materials

The primary cost differentiators are:
1. **Plasma confinement scaling** (sets machine size for given fusion power)
2. **Magnet cost** (REBCO tape cost × total conductor length)
3. **Auxiliary heating requirement** (P_input scales capital cost and recirculating power)
4. **Blanket architecture** (modular solid vs. liquid, TBR margin)
5. **Capacity factor** (maintenance turnaround time, component replacement cycles)

NT's claimed advantages in confinement (#1) and heating (#3) are the primary economic levers. If both validate, NT is the lowest-cost HTS tokamak variant. If either fails, NT is indistinguishable from conventional PT tokamaks at similar cost.

### What Makes This One Fundamentally Different?

**The plasma shape inversion (δ = -0.5 vs. δ = +0.4) is the only fundamental architectural difference.**

This single geometric change drives:
- Passive ELM suppression (PT requires active control)
- Lower scrape-off-layer power (3.6× reduction vs. PT)
- Different confinement scaling (H_98y2 claimed higher for NT, but database is thin)
- Worse vertical stability (requires passive plates, PT does not)
- Conditional ohmic-only heating viability (field-strength-dependent threshold)

Everything else — magnets, blanket, vacuum vessel, thermal cycle, tritium fuel cycle, remote handling — is tokamak-standard technology shared across the family. **NT is a plasma physics bet, not a technology bet.** If the plasma physics validates, the cost structure improves. If it fails, the concept is a conventional tokamak with marginally higher fabrication complexity (passive plates, liquid blanket integration).

---

## Modeling Confidence

**Rating: Medium**

### How Many Parameters Are Data-Anchored vs. Speculative?

**Data-anchored** (from MANTA paper or commercial tape specs):
- Geometry: R0, a, κ (high confidence — reactor design is explicit)
- Magnetic field: B, I_p (high confidence)
- Power performance: P_fus, P_net, P_input (medium confidence — MANTA specifies, but depends on confinement)
- Magnet cost: REBCO tape at $40/kA·m (medium confidence — industry target pricing, not guaranteed)
- Divertor cost: $150M (medium confidence — MANTA publishes, but NT-specific lifetime is undemonstrated)
- FLiBe material cost: $169/kg × 169 t = $28.6M (medium confidence — pricing known from MSR community, supply constrained)

**Speculative**:
- H_98y2 = 1.44 (low confidence — extrapolated from DIII-D, no reactor-scale validation)
- H_NA = 2.0 for ohmic-only (low confidence — Ball et al. extrapolate from TCV, undemonstrated at reactor scale)
- TBR = 1.15 for FLiBe liquid blanket (low confidence — neutronic prediction, never demonstrated in tokamak)
- Capacity factor 79% (low confidence — assumes NOAK remote handling and 2-month PF2 replacement, undemonstrated)
- REBCO magnet lifetime >1,000 MW-yr (medium-low confidence — CFS/Tokamak Energy magnets exist, but 14 MeV neutron damage at >50 dpa is unproven)

**Parameter count**: ~60% of critical cost drivers are data-anchored; ~40% are speculative or extrapolated. This is better than many fusion concepts (e.g., IFE target gain, MIF liner implosion symmetry) but worse than fission (where all subsystems are TRL 8-9 with operating fleet data).

### What Is the Dominant Source of LCOE Uncertainty?

**NT confinement scaling (H_98y2) is the single dominant uncertainty.**

If H_98y2 validates at 1.3-1.5, the machine operates as designed and LCOE is driven by REBCO tape cost learning curve and capacity factor execution. If H_98y2 falls to 1.0-1.2, the machine must grow or increase field to compensate, adding 30-50% to overnight cost and pushing LCOE above $650/MWh.

Secondary uncertainties:
- **REBCO tape cost** (±$150/MWh swing for 2× cost variation)
- **Capacity factor** (±$100/MWh swing for 60-85% availability range)
- **Ohmic-only heating** (±$50/MWh if validated/rejected)
- **FLiBe blanket TBR** (qualitative — TBR < 1.0 is existential, but TBR = 1.05-1.20 range does not materially affect LCOE)

The confinement uncertainty propagates into machine size, which cascades into magnet cost, blanket cost, vacuum vessel cost, and balance-of-plant cost. This is why confinement is the dominant lever.

---

## What Would Change My Mind

### 1. High-Power Long-Pulse NT Experiments Demonstrating H_98y2 > 1.3 at Reactor-Relevant Density

**Specific milestone**: DIII-D, KSTAR, or EAST NT campaign achieving:
- I_p > 5 MA
- β_N > 2.5
- f_GW > 0.8 (high Greenwald fraction)
- P_input > 10 MW (ICRF or ECRH heating)
- Sustained radiative divertor detachment for >100 s
- Measured H_98y2 > 1.3 with <15% shot-to-shot variability

**Impact if achieved**: Retires the confinement scaling uncertainty entirely. LCOE confidence rises from Medium to Medium-High. MANTA parameters become credible for reactor design, and NT tokamaks become the preferred HTS tokamak configuration for compact pilot plants.

**Impact if failed** (H_98y2 < 1.2 at reactor scale): NT tokamaks revert to conventional PT baseline with no cost advantage. Firefly and academic NT programs either redesign for larger R0 or abandon the concept.

---

### 2. CFS or Tokamak Energy REBCO Tape Cost Reaching $15/kA·m at >10,000 km/year Production Scale

**Specific milestone**: Industry announcement (CFS, Shanghai Superconductor, or Faraday Factory Japan) of REBCO tape production at:
- $15/kA·m delivered cost (vs. $40/kA·m MANTA assumption)
- >10,000 km/year production capacity (sufficient for 2+ reactors per year)
- J_c > 1000 A/mm² at 25 K, 25 T maintained in production tape
- Radiation hardening validated at >30 dpa with <20% J_c degradation

**Impact if achieved**: TF coil cost drops from $1,500M to ~$600M at native scale. Overnight cost falls from $4.4B to $3.5B (−20%), and LCOE drops from $507/MWh to $400-420/MWh. NT tokamaks approach natural gas with CCS cost range ($80-120/MWh + $40-60/MWh carbon capture = $120-180/MWh).

**Impact if failed** (tape cost stays above $50/kA·m): HTS tokamak economics remain marginal. Fission SMRs and advanced geothermal become preferred firm low-carbon baseload options.

---

### 3. ITER or SPARC Demonstrating >70% Availability Over 5+ Years of D-T Operation

**Specific milestone**: ITER or CFS SPARC operating with:
- >70% effective availability (including scheduled maintenance, unplanned outages, and component replacements)
- Demonstrated remote handling turnaround <4 months for divertor cassette or blanket module replacement
- Tritium breeding and fuel cycle closed-loop operation (for ITER TBM or SPARC breeding blanket)
- Magnet reliability >95% uptime (no unplanned quenches or coil failures requiring shutdown)

**Impact if achieved**: Validates tokamak availability assumptions and retires capacity factor uncertainty. MANTA's 79% assumption becomes credible for NOAK plants. LCOE confidence rises to High.

**Impact if failed** (ITER/SPARC availability <50% over 5 years): Tokamak capacity factor assumptions are optimistic. LCOE rises to $600-700/MWh even if confinement and magnet costs validate. Fusion becomes a niche application (remote off-grid power, desalination, process heat) rather than grid baseload competitor.
