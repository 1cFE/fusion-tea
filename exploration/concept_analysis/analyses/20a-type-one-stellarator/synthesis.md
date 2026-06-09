---
ID: 20a-type-one-stellarator
Concept: Type One Stellarator (Type One Energy)
Company: Type One Energy
Type: synthesis
Status: draft
Created: 2026-06-09
---

## 1. Executive Summary

- **Greatest Risk**: HTS coil manufacturing at stellarator geometry is unproven at scale and represents ~40% of direct capital (C220103: $4.1B at 1 GWe). No precedent exists for winding REBCO tape on 3D non-planar forms at the precision required for quasi-isodynamic field quality. First-article yield, fabrication timeline, and unit cost carry 30-50% uncertainty.

- **Greatest Advantage**: Capacity factor claim of 95-97% (2-year continuous burn, 30-day outages) is 15-20% higher than tokamak baselines (75-85%). If the maintenance architecture works as claimed, this directly translates to 15-20% better LCOE at identical overnight capital cost.

- **LCOE Ballpark**: **$310/MWh** (1 GWe NOAK projection, zero overrides). This is pure library stellarator-modular-HTS pricing with no concept-specific cost data to anchor adjustments. The model assumes W7-X modular-coil heritage + CFS HTS unit costs scale to Infinity Two geometry without premium.

- **Confidence Verdict**: **Medium**. Physics design is exceptionally well-documented (seven peer-reviewed papers, complete parameter set, Q > 40 validated via 70,000+ config simulations). Cost model is entirely extrapolative — zero company-published dollar figures, zero independent TEA studies, zero bottom-up engineering cost estimates for the three largest accounts (magnets, blanket, BOP).

## 2. What Matters Most for LCOE

Ranked by sensitivity magnitude and parameter uncertainty:

### 1. Capacity Factor (95-97% claimed)

**Assumed value**: 95.9% (2-year operation / [2 years + 30 days])
**Source**: Type One Energy press release — 2-year continuous cycles with 30-day planned outages
**Sensitivity**: LCOE scales inversely with CF. At 95% CF vs. 75% baseline, LCOE improves by ~21% (same capital amortized over 27% more energy). Dropping to 85% CF (still excellent) degrades LCOE by ~11% from the $310/MWh model result.

**What would flip the conclusion**: If actual planned outages take 60-90 days instead of 30 (credible for stellarator blanket/divertor remote handling with no published time-motion study), CF drops to 88-92%, erasing most of the CF advantage over advanced tokamaks. The $310/MWh LCOE becomes $330-350/MWh, moving Infinity Two from "competitive with fission" to "marginal".

**Risk retirement**: Detailed remote-handling simulation and mock-up validation for stellarator geometry, or actual Infinity One outage data post-2029.

---

### 2. HTS Coil Unit Cost (C220103: $4.1B, 23% of NOAK overnight capital)

**Assumed value**: Library default — CFS/MIT HTS cable cost ($10-20/kA-m NOAK) scaled to stellarator coil surface area and stored energy, no geometry premium
**Source**: Derived from SPARC TF coil data (planar tokamak geometry); W7-X modular coil fabrication time (LTS, 18 years for 50 coils)
**Sensitivity**: C220103 is 23% of overnight capital. A 50% increase in coil cost (plausible if 3D winding precision, reject rates, or first-article learning curve are worse than tokamak TF coils) raises overnight capital by ~11% and LCOE by ~9-10%, pushing LCOE to $340/MWh.

**What would flip the conclusion**: If HTS coil manufacturing at stellarator geometry proves infeasible or prohibitively expensive (e.g., unit cost 2× tokamak coils, adding $2B to C220103), overnight capital rises to $32,000/kW and LCOE to $370-390/MWh. At that point, Infinity Two loses cost competitiveness even with the 95% CF advantage.

**Risk retirement**: Type One Energy bottom-up coil cost estimate, or successful fabrication and field-testing of Infinity One HTS coils (2029 target) with published unit cost and build time.

---

### 3. Blanket and Divertor Replacement Frequency (drives capacity factor and CAS70 replacement cost)

**Assumed value**: Blanket lasts 2-year cycle (implicit in CF calculation); divertor lifetime not specified
**Source**: Inferred from 2-year operation claim; no explicit blanket or divertor fluence limit disclosed
**Sensitivity**: If HCPB blanket requires replacement every 1 year instead of 2 years (due to EUROFER neutron damage limits or pebble bed degradation), planned outages double in frequency. CF drops to ~91% (1-year cycle + 30-day outage), degrading LCOE by ~5%. If blanket *and* divertor both require annual replacement with 45-60 day outages, CF drops to 85-88% and LCOE rises to $340-360/MWh.

**What would flip the conclusion**: HCPB neutronics and structural analysis showing blanket end-of-life at <150 dpa (equivalent to <2 full-power years behind FLiBe/HCPB shielding). EU-DEMO HCPB studies cite 50-200 dpa range depending on EUROFER embrittlement criteria — the pessimistic end of this range forces more frequent replacement.

**Risk retirement**: Infinity Two radial build disclosure with fluence calculations at blanket structure, or EU-DEMO HCPB Test Blanket Module irradiation data validating 150+ dpa lifetime.

---

### 4. Heat Flux Width (λ_q: 1.5-4.4 cm, factor-of-3 uncertainty)

**Assumed value**: Bader et al. reports 1.5-4.4 cm uncertainty; model does not price divertor as a function of λ_q (uses fixed stellarator-island default)
**Source**: Extrapolation from W7-X data (2.5 T, λ_q ~ 4-5 cm) to Infinity Two's 9 T, with large uncertainty in stellarator SOL transport scaling
**Sensitivity**: If λ_q is on the narrow end (1.5 cm), peak heat loads exceed 10 MW/m² unless radiation fraction >90%. This may force adoption of the Large Island Backside Divertor (LIBD), a TRL 1-2 concept with no cost estimate. LIBD capital cost is unknown but likely adds $100-300M to C220108 (currently $62M at 1 GWe NOAK). At $200M LIBD premium, overnight capital rises by ~0.7% and LCOE by ~0.6% — a modest direct impact, but LIBD integration risk could cascade into schedule delays or blanket redesign.

**What would flip the conclusion**: LIBD required *and* LIBD particle exhaust performance worse than classical island divertor. If LIBD fails to achieve >0.5% particle exhaust efficiency (Bader's minimum requirement), the entire divertor concept is in jeopardy and would require a major redesign (helium-cooled plate divertor, larger surface area, or X-divertor analog). This is a low-probability, high-consequence risk.

**Risk retirement**: Infinity One validation of λ_q scaling and classical island divertor performance at detached operation (2029 target). Interim: W7-X high-field campaign data if B > 3 T operation is achieved.

---

### 5. Tritium Breeding Ratio Margin (TBR = 1.30 neutronics, degradation to TBR_eng unknown)

**Assumed value**: TBR = 1.30 (OpenMC ideal geometry); model does not apply engineering degradation factor
**Source**: Saltzman et al. 2025, HCPB + FLiBe dual-zone neutronics with 300M-particle simulation
**Sensitivity**: EU-DEMO HCPB studies show 10-15% TBR degradation from neutronics to engineering design (module gaps, welds, penetrations, shielding around diagnostics/heating ports). Applying 12% degradation: TBR_eng = 1.30 × 0.88 = 1.14. After tritium extraction losses (~5-10%), net TBR ~1.03-1.09. This is adequate but leaves little margin for neutronics uncertainties or beryllium multiplier degradation over lifetime.

If TBR_eng < 1.05, Infinity Two requires external tritium supply to maintain fuel inventory. With global civilian tritium stockpile shrinking (CANDU retirements), this becomes a fleet-scaling constraint. For a single plant, the impact is procurement risk and potential fuel cost escalation (tritium market price ~$30k/g). LCOE impact is <1% (tritium fuel cost is small relative to capital), but availability risk is high if multiple D-T concepts compete for limited supply.

**What would flip the conclusion**: TBR_eng < 1.0 after accounting for engineering degradation, extraction losses, and dual-chemistry integration challenges. At TBR < 1.0, Infinity Two cannot achieve tritium self-sufficiency and becomes dependent on external supply indefinitely. This does not kill the concept but caps fleet size at the number of plants supportable by CANDU byproduct + other breeders in the fusion fleet.

**Risk retirement**: Engineering blanket design with realistic module geometry, gaps, and penetrations, followed by MCNP/OpenMC validation. EU-DEMO HCPB TBM neutronics (Preliminary Design Review expected 2026) provides analogue data.

---

### Summary Table

| Parameter | Current Model Assumption | Pessimistic Bound | LCOE Impact if Pessimistic | Confidence in Assumption |
|-----------|-------------------------|-------------------|---------------------------|------------------------|
| Capacity factor | 95.9% | 85% (60-day outages, annual blanket replacement) | +$30-40/MWh | Low — no maintenance plan published |
| HTS coil unit cost | Library default (~$4.1B @ 1 GWe) | +50% (stellarator geometry premium) | +$30/MWh | Medium — SPARC planar heritage is strong but 3D winding unproven |
| Blanket replacement freq. | Every 2 years (implicit) | Every 1 year (conservative EUROFER damage limit) | +$15-20/MWh (via CF) | Medium — EU-DEMO range is 2-6 FPY; 1 year is pessimistic end |
| Heat flux width | 1.5-4.4 cm (Bader range) | 1.5 cm → LIBD required | +$2-5/MWh (LIBD capital) | Low — W7-X extrapolation factor-of-3 uncertain |
| TBR engineering margin | 1.30 (neutronics ideal) | 1.10 (12% degradation + 5% losses) | <$1/MWh (tritium fuel cost; procurement risk non-monetary) | Medium — EU-DEMO degradation well-documented |

**Combined pessimistic case**: 85% CF + 50% coil cost premium + annual blanket replacement → LCOE ~$380-400/MWh, moving Infinity Two from competitive to marginal.

**Combined optimistic case**: 96% CF + library coil cost + 2-year blanket life → LCOE ~$300/MWh, competitive with advanced fission (Vogtle 3/4 ~$110-130/MWh at $14,000/kW overnight, but sunk-cost; new-build fission likely $8,000-12,000/kW → $80-150/MWh).

## 3. Risk Verdicts

### HTS Coil Manufacturing at Stellarator Geometry (TRL 3-4)

**Verdict**: Genuinely uncertain
**Rationale**: CFS/MIT HTS cable is proven at 20 T on planar TF coils; W7-X modular coils demonstrate 3D stellarator fabrication at LTS. Combining these (HTS + 3D non-planar) at Infinity Two's scale (R = 12.5 m, B = 9 T, 15-18 T peak field on conductor) is first-of-a-kind. Winding fixtures, out-of-plane stress management, quench protection, and field-error alignment are all extrapolative.
**What would retire this risk**: Successful fabrication and magnetic-field testing of Infinity One HTS coils (2029), with published build time, unit cost, and field quality measurements. Alternatively, a bottom-up manufacturing cost study from Type One Energy or CFS quantifying the stellarator geometry premium (if any) over tokamak TF coils.

---

### Classical Island Divertor Heat Flux and Particle Exhaust (TRL 5-6)

**Verdict**: Likely resolvable
**Rationale**: W7-X island divertor operated successfully in detached mode with <10 MW/m² heat loads for 8-minute pulses. Scaling to Infinity Two's 9 T field and steady-state operation requires factor-of-3 extrapolation in field strength and factor-of-10⁶ in pulse length, but the physics is understood and SOLPS-ITER modeling is validated against W7-X data. The λ_q uncertainty (1.5-4.4 cm) is large, but even at the pessimistic end (1.5 cm), achieving 90%+ radiation fraction is feasible with neon or argon seeding (W7-X demonstrated 70-80% radiation; 90% is a stretch but not implausible).
**What would retire this risk**: Infinity One long-pulse detachment experiments (2029) validating radiation fraction >85% and particle exhaust efficiency >0.5% at high field. If classical divertor meets requirements, LIBD becomes unnecessary.

---

### LIBD Integration and Performance (TRL 1-2, Contingency)

**Verdict**: Unlikely resolvable without multi-year R&D
**Rationale**: LIBD is a novel concept with no experimental precedent in any stellarator or tokamak. The dome structure, particle pumping behind the dome, and integration with blanket/FLiBe systems are entirely on paper. SOLPS-ITER simulations suggest 12.6% particle exhaust efficiency (vs. 0.5-5% for classical island), but simulation-to-reality gap for a new divertor concept is historically large (cf. Super-X divertor, snowflake divertor — both required years of experimental iteration to validate).
**What would retire this risk**: Infinity One LIBD demonstration (2029+), followed by engineering design for full-scale LIBD at Infinity Two geometry. If LIBD is required and fails to perform, fallback options are unclear (larger classical divertor surface area? Helical divertor? Radiative mantle?). This is a low-probability, high-consequence risk — most likely the classical divertor works and LIBD remains a backup.

---

### Dual-Zone HCPB/FLiBe Blanket Integration (TRL 2-3)

**Verdict**: Likely resolvable
**Rationale**: HCPB and FLiBe are individually TRL 4-5 (HCPB in EU-DEMO TBM development, FLiBe in MSRE and ORNL loop experiments). Combining them in a single blanket module is novel but not physics-breaking. The challenges are engineering (helium-FLiBe thermal interface, differential expansion, dual tritium extraction pathways) rather than fundamental feasibility. EU-DEMO HCPB costing provides a cost floor; FLiBe adds material cost (~$60M for 200 m³ inventory at $154/kg) and modest integration complexity.
**What would retire this risk**: Type One Energy blanket module CAD and thermal-hydraulic analysis, or EU-DEMO dual-chemistry blanket study (if one exists). If dual-zone proves too complex, fallback to HCPB-only is straightforward (TBR margin of 1.30 allows some breeding volume to be lost without dropping below TBR > 1.05).

---

### 30-Day Planned Outage and 95-97% Capacity Factor (TRL 4-5 for remote handling, unvalidated for stellarator blanket/divertor)

**Verdict**: Genuinely uncertain
**Rationale**: ITER remote handling prototypes demonstrate tokamak blanket/divertor exchange in mock-ups, but no stellarator-specific remote handling exists beyond W7-X coil installation (not remote, not under activation constraints). Replacing a dual-chemistry HCPB/FLiBe blanket module plus island divertor cassettes in 30 days requires pre-assembled modules, parallel robotic operations, and zero integration surprises. ITER's remote-handling timeline for full blanket replacement is measured in months, not weeks (though ITER is FOAK and not optimized for availability).
**What would retire this risk**: Time-motion simulation for Infinity Two maintenance sequence, validated against ITER or EU-DEMO remote-handling studies. Actual Infinity One outage data (post-2029) provides ground truth, though Infinity One is smaller scale and may not have full remote-handling systems. If 30-day outages prove infeasible and actual outages are 60-90 days, CF drops to 88-92% — still excellent, but CF advantage over tokamaks shrinks from 15-20% to 5-10%.

---

### Tritium Self-Sufficiency (TRL 3-4 for HCPB extraction, unvalidated for dual-chemistry)

**Verdict**: Likely resolvable
**Rationale**: TBR = 1.30 (neutronics) provides 30% margin over breakeven. EU-DEMO HCPB degradation factors (10-15%) and extraction losses (5-10%) reduce this to TBR_eng ~1.05-1.15 — adequate but not comfortable. The dual-chemistry integration (HCPB + FLiBe) adds tritium processing complexity (two extraction pathways, FLiBe permeation risk) but does not fundamentally threaten TBR if the neutronics are correct.
**What would retire this risk**: Engineering blanket design with realistic module geometry and neutronics re-run. If TBR_eng > 1.10 after degradation, tritium self-sufficiency is credible. If TBR_eng < 1.05, external tritium supply is required, capping fleet scalability.

## 4. Structural Advantages and Disadvantages

Comparison baseline: D-T tokamak with ITER-like cost structure (pulsed operation, disruption mitigation, current-drive power, TF + PF coil sets).

### Advantages (Cost Items Reduced or Eliminated)

**1. Current-Drive Power Eliminated (~$200-400M capital, ~$5-10M/yr OPEX)**
Stellarators do not require current drive. ITER-scale tokamaks need 50-100+ MW of NBI, ECRH, or LHCD to sustain plasma current in steady-state (or accept pulsed operation with cyclic thermal/mechanical stress). Infinity Two uses ECRH solely for heating (20 MW at Q = 40), a 5-10× reduction in installed heating power compared to current-drive-dependent tokamaks.

Quantified savings: C220104 (supplementary heating) is $100M at 1 GWe NOAK for 20 MW ECRH. A comparable tokamak with 100 MW current drive + heating would pay ~$400-500M for C220104, saving Infinity Two $300-400M (~1% of overnight capital). OPEX savings from reduced gyrotron/NBI replacement and electricity for heating are ~$5-10M/yr.

**2. Disruption Mitigation Systems Eliminated (~$50-100M capital)**
Stellarators have no disruptions (no driven current → no current-driven instabilities). Tokamaks require shattered pellet injection (SPI), resonant magnetic perturbation (RMP) coils, or runaway electron mitigation. ITER's disruption mitigation system is a dedicated CAS line item; stellarators have zero cost here.

**3. Vertical Stabilization Coils Eliminated (~$30-50M capital)**
Tokamak elongated plasmas are vertically unstable and require active feedback coils (part of C220103 for tokamaks). Stellarators are intrinsically 3D and vertically stable. Infinity Two's elongation is κ = 1.0 (no vertical instability), eliminating this coil set.

**4. Capacity Factor Structural Advantage (+15-20% vs. tokamak baseline)**
Disruption-free operation and steady-state burn enable longer continuous cycles. Infinity Two claims 2-year cycles with 30-day outages (95-97% CF) vs. tokamak baselines of 75-85% (EU-DEMO, ARIES-AT). At 95% CF vs. 75% CF and identical overnight capital, LCOE improves by ~21% (same capex amortized over 27% more energy).

This is not a line-item cost saving but a **structural economic advantage** — the same reactor-island capital cost delivers more kWh per year. If overnight capital is $28,000/kW (model result), the effective capital cost per MWh produced is 21% lower at 95% CF than at 75% CF.

**Combined stellarator advantage**: Eliminates ~$400-600M in tokamak-specific subsystems (current drive, disruption mitigation, vertical stabilization) and achieves 15-20% better capital utilization via higher CF. These advantages are shared across all stellarators (comparables 05, 09, 10, 20b, 36).

---

### Disadvantages (Cost Items Added or Increased)

**1. 3D Non-Planar HTS Coils Premium (est. +$500M to +$2B vs. tokamak TF coils)**
Stellarator modular coils are geometrically complex compared to tokamak toroidal-field coils (which are planar or near-planar). W7-X's 50 non-planar LTS coils took 18 years to fabricate and cost ~€1B (2015 basis, not directly comparable to HTS). Type One Energy's HTS non-planar coils have no cost precedent, but the 3D winding precision, tooling complexity, and lower production volume relative to tokamak TF coils plausibly add 20-50% to coil unit cost.

At C220103 = $4.1B (1 GWe NOAK, library default), a 50% stellarator geometry premium adds ~$2B to overnight capital (~7% increase) and ~$20/MWh to LCOE. This offsets part of the current-drive and CF advantages.

The library's stellarator-modular-hts costing already incorporates W7-X modular-coil heritage, so this "disadvantage" may be baked into the $310/MWh result. The question is whether the library *under*estimates the coil premium (if 3D HTS winding is harder than W7-X LTS 3D winding), or *over*estimates it (if modular construction and CFS manufacturing scale reduce costs faster than W7-X suggests).

**2. Dual-Chemistry Blanket Integration Complexity (+$100-300M vs. single-chemistry HCPB or FLiBe)**
Infinity Two's HCPB + FLiBe dual-zone blanket is novel. Single-chemistry blankets (HCPB-only or FLiBe-only) have simpler manifold routing, single tritium extraction pathway, and no helium-molten-salt thermal interfaces. The dual-zone approach adds engineering complexity (design cost, fabrication cost, integration risk) but may save on total blanket volume by using FLiBe in low-breeding, high-shielding zones where HCPB would be overkill.

Without a company cost breakdown, the dual-chemistry premium is speculative. EU-DEMO HCPB-only costing is the library baseline; adding FLiBe zones likely increases C220101 by 10-30% (est. +$50-150M at 1 GWe NOAK). This is a modest cost penalty for TBR margin (1.30 vs. 1.10-1.15 for HCPB-only).

**3. Island Divertor Surface Area (~neutral vs. tokamak poloidal divertor)**
Stellarator island divertors have comparable or slightly larger surface area than tokamak poloidal divertors due to 3D island geometry. The W7-X island divertor uses ~15-20 m² of plasma-facing area per island; Infinity Two with 4 field periods has 4 islands, giving ~60-80 m² total (estimated). ITER's poloidal divertor is ~50-60 m². The cost is comparable.

If LIBD is required, divertor surface area and structural complexity increase significantly (dome structure, internal particle pumping, integration with blanket). LIBD adds an estimated $100-300M to C220108, but this is a contingency, not the baseline design.

**4. Maintenance Complexity for Non-Planar Geometry (schedule risk, not direct cost)**
Remote handling for stellarator blanket/divertor modules is geometrically more complex than tokamak sectors (which have toroidal symmetry and straight-line access). Infinity Two's claim of 30-day outages assumes highly optimized robotic handling and pre-assembled cassettes. If stellarator maintenance proves slower than tokamak maintenance (e.g., 60-day outages vs. tokamak's 45-60 days), the CF advantage shrinks.

This is not a capital cost penalty but a **capacity factor risk** — if maintenance takes longer, CF drops and LCOE rises. The magnitude is captured in the CF sensitivity analysis (Section 2).

---

### Net Structural Cost Impact

| Item | Tokamak Baseline Cost | Infinity Two Cost | Delta |
|------|---------------------|------------------|-------|
| Current drive (C220104) | $400-500M | $100M | **-$300-400M** |
| Disruption mitigation | $50-100M | $0 | **-$50-100M** |
| Vertical stabilization (in C220103) | $30-50M | $0 | **-$30-50M** |
| 3D HTS coils (C220103) | $3-4B (planar tokamak TF) | $4.1B (library default) | **+$500M-1B** (if geometry premium exists) |
| Dual-chemistry blanket (C220101) | $300-350M (HCPB-only) | $350-400M (HCPB+FLiBe estimate) | **+$50-100M** |
| Capacity factor advantage | 75-85% | 95-97% | **-$50-60/MWh LCOE** (not capex, but effective cost/MWh) |

**Total direct capital impact**: Net savings of ~$0-200M on eliminated tokamak subsystems, partially offset by +$500M-1B coil premium and +$50-100M blanket complexity. Overnight capital is likely comparable to an advanced tokamak at the same fusion power, but **LCOE is 15-20% better due to CF advantage** (if 30-day outages hold).

**Key takeaway**: Infinity Two does not win on overnight capital cost (stellarator coils and blanket complexity offset tokamak current-drive and disruption-mitigation costs), but wins on **capacity utilization** (95% CF vs. 75-85% tokamak). The economic case hinges on validating the 30-day outage claim.

## 5. Cross-Concept Positioning

### Size and Scale Class

Infinity Two is a **large-scale, high-power stellarator** (R = 12.5 m, P_fus = 800 MW, P_net = 350 MWe). Among stellarator comparables:

- **Larger than**: Proxima Stellaris (09, R ~ 4-5 m estimated), Thea Energy (05, compact), Helical Fusion HESTIA (36, R ~ 6-8 m estimated)
- **Similar scale to**: Gauss Fusion large-scale stellarator (10, R ~ 10-15 m inferred), Renaissance Fusion (20b, R ~ 5-8 m estimated but unclear)
- **Smaller than**: Historical stellarator studies (ARIES-CS: R = 7.75 m but lower field; Helias reactor studies at R ~ 20 m)

At 350 MWe per module, Infinity Two requires **~3 modules** to reach 1 GWe fleet comparison. This is fewer modules than smaller stellarators (Proxima likely needs 5-10 modules at 100-200 MWe each), reducing duplicated structure (buildings, turbines, grid connection) and improving economies of scale for BOP.

**Positioning**: Infinity Two occupies the "large stellarator, fewer modules, higher capital intensity per unit but lower cost per GWe" niche. This is the stellarator analogue of ITER-scale tokamaks vs. compact high-field tokamaks (CFS SPARC, Tokamak Energy ST80).

---

### Magnet Technology and Risk Profile

**HTS modular non-planar coils** place Infinity Two in the **moderate-risk, proven-heritage** camp:

- **Lower risk than**: Renaissance (20b, laser-patterned HTS — TRL 2-3, unproven manufacturing), Helical Fusion (36, helical HTS — continuous winding at HTS is unproven)
- **Higher risk than**: Thea Energy (05, planar HTS pancake coils — tokamak-like manufacturing)
- **Similar risk to**: Proxima Fusion (09, modular HTS QI stellarator — same coil architecture, smaller scale)

Infinity Two leverages **CFS/MIT HTS cable** (proven at 20 T on planar TF coils) and **W7-X modular-coil assembly heritage** (proven at LTS). The combination (HTS + 3D non-planar) is FOAKE, but both ingredients are TRL 5-6 individually. This is a **"build on proven tech, integrate at scale"** strategy vs. Renaissance's **"invent new manufacturing, scale if it works"** strategy.

**Positioning**: Infinity Two is the **conservative stellarator** among HTS concepts — not the cheapest if everything works (Renaissance's laser-patterned HTS could undercut by 30-50% if successful), but the highest probability of delivering a working plant on schedule.

---

### Blanket and Fuel Cycle

**HCPB + FLiBe dual-zone** is a **high-cost, low-risk** blanket choice:

- **More expensive than**: FLiBe-only blankets (Thea, possibly Renaissance), flowing liquid-wall concepts (Renaissance Li-LiH wall)
- **Less risky than**: Flowing liquid walls (TRL 2-3, no operating precedent), FLiBe-only with marginal TBR (requires near-perfect neutronics)
- **Similar to**: EU-DEMO HCPB baseline (institutional R&D backing, Test Blanket Modules in development)

The TBR = 1.30 margin is **conservative** — Infinity Two pays for breeding capacity beyond strict breakeven (TBR > 1.05) to hedge against engineering degradation and extraction losses. This is a **"buy margin with dollars"** approach: HCPB is more expensive than FLiBe per unit volume (solid breeder pebbles, helium cooling at 8 MPa, complex manifolds), but TBR margin reduces tritium supply-chain risk.

**Positioning**: Infinity Two prioritizes **tritium self-sufficiency** over blanket capital cost minimization. This makes sense for a 2030s deployment timeline when CANDU tritium supply is shrinking and multiple D-T concepts compete for limited inventory.

---

### Divertor and Power Exhaust

**Classical island divertor** (W7-X heritage) is the **mainstream stellarator choice**:

- **Proven precedent**: W7-X operated island divertor successfully in detached mode (<10 MW/m² heat loads, 8-minute pulses)
- **Unproven at scale**: Factor-of-3 extrapolation in field strength (2.5 T → 9 T), factor-of-10⁶ in pulse length (8 min → 2 years)
- **Backup plan**: LIBD (TRL 1-2, contingency if classical divertor fails heat-flux requirements)

Among stellarator comparables:

- **Same as**: Proxima (09, QI → natural edge islands → island divertor), likely Gauss (10, if large-scale stellarator uses island divertor)
- **Different from**: Thea (05, planar coils may not generate natural islands → divertor architecture unclear), Renaissance (20b, flowing liquid wall → no solid divertor), Helical Fusion (36, helical divertor)

**Positioning**: Infinity Two follows the **W7-X-validated playbook** for stellarator power exhaust. This is a **"let someone else prove it first, then scale"** strategy — W7-X retired the concept risk, Infinity One (2029) will retire the scaling risk, Infinity Two (2030s) inherits validated technology.

---

### Economic Niche: High-Availability, Capital-Intensive

Infinity Two's **95-97% capacity factor** (if validated) places it in the **baseload power** economic niche:

- **Better availability than**: Pulsed tokamaks (60-75% CF due to thermal cycling and longer maintenance), ITER-era tokamaks (75-85% CF NOAK), molten-salt fission (MSR capacity factors unproven but likely 85-92%)
- **Comparable to**: Advanced fission LWRs (90-93% CF for Gen III+ fleet average), geothermal baseload (90-95% CF)
- **Worse than**: Natural gas combined-cycle (95-98% CF but carbon-emitting), run-of-river hydro (95%+ CF where available)

At $310/MWh LCOE (1 GWe NOAK), Infinity Two is **not cost-competitive with fission or natural gas** in regions with low-cost capital and fuel. However, in **decarbonization-constrained, high-electricity-price markets** (California, Germany, Japan), $310/MWh is within the range of offshore wind + storage or solar + storage (LCOE ~$150-250/MWh for renewables + 4-8 hour storage; higher for 24/7 firm power).

**Positioning**: Infinity Two targets the **firm, dispatchable, carbon-free baseload** segment — competing with advanced fission, deep geothermal, and renewable + long-duration storage. The value proposition is **no fuel supply-chain risk** (D-T breeding on-site after tritium startup), **no geological constraints** (vs. geothermal), and **smaller footprint than renewables + storage** (GW-scale on <100 acres vs. square-mile solar farms + battery warehouses).

---

### Summary: Where Infinity Two Sits in the Landscape

| Axis | Infinity Two Position | Closest Analogues | Differentiation |
|------|---------------------|------------------|----------------|
| **Scale** | Large stellarator (R=12.5m, 350 MWe/module) | Gauss Fusion (10), ARIES-CS historical | Fewer modules per GWe than compact stellarators |
| **Magnet tech** | Modular HTS non-planar (proven-heritage risk profile) | Proxima (09), W7-X LTS legacy | More conservative than Renaissance laser-HTS, less conservative than Thea planar-HTS |
| **Blanket** | HCPB+FLiBe dual-zone (high cost, high TBR margin) | EU-DEMO HCPB baseline | More expensive than FLiBe-only, less risky than flowing liquid wall |
| **Divertor** | Classical island (W7-X heritage, LIBD backup) | Proxima (09), W7-X | Proven concept, unproven at 9 T / steady-state scale |
| **Availability** | 95-97% CF (aggressive, unvalidated) | Advanced fission (90-93%), geothermal | Best-in-class if validated; high risk if not |
| **LCOE** | $310/MWh (1 GWe NOAK, zero overrides) | Mid-pack among stellarators (pending cost data from comparables) | LCOE driven by CF advantage, not overnight capital |

**In one sentence**: Infinity Two is a **large-scale, high-availability stellarator with conservative subsystem choices (HCPB blanket, island divertor, wound HTS coils) and aggressive operational assumptions (95% CF, 30-day outages)** — it bets on execution and maintenance efficiency rather than breakthrough technology to achieve competitive LCOE.

## 6. Modeling Confidence

**Rating: Medium**

### What We Know Well (High Confidence, <20% Uncertainty)

**Plasma physics baseline**: Exceptionally strong. Seven peer-reviewed papers in J. Plasma Phys. 2025 provide complete parameter set (R₀, B, β, density, Q, etc.), validated via 70,000+ configuration simulations on DOE's Frontier supercomputer. QI/maximum-J optimization is a mature stellarator design methodology (IPP Greifswald, UW-Madison heritage). Confinement scaling, MHD stability, and ignition access (Q > 40) are credible.

**Fuel cycle neutronics**: TBR = 1.30 from OpenMC 300M-particle simulation is a high-fidelity result (modern Monte Carlo with ENDF/B-VIII cross-sections). The dual-zone HCPB+FLiBe architecture is novel but the neutronics are straightforward. Uncertainty is in engineering degradation (10-15% from ideal geometry to real modules), not fundamental breeding physics.

**Stellarator subsystem heritage**: W7-X provides operating data for island divertor (detached operation, <10 MW/m² heat loads, 8-min pulses), modular non-planar coil assembly (LTS), and stellarator-specific engineering (vacuum vessel tolerances, port integration, 3D diagnostics). This is a 15+ year experimental database, the strongest stellarator validation since LHD.

---

### What We're Guessing (Medium Confidence, 30-50% Uncertainty)

**HTS coil cost at stellarator geometry**: The library's C220103 = $4.1B (1 GWe NOAK) is derived from CFS/MIT HTS cable unit cost ($10-20/kA-m NOAK) and W7-X modular-coil fabrication time (18 years for 50 LTS coils). This is a **cross-domain extrapolation** — CFS cable is proven on planar tokamak TF coils, W7-X coils are proven at LTS, but HTS + 3D non-planar at Infinity Two's scale is FOAKE. The unit cost could be 30-50% higher if 3D winding precision, reject rates, or first-article learning are worse than planar HTS. Alternatively, modular construction and CFS manufacturing scale could reduce costs faster than W7-X suggests, dropping the cost by 20-30%.

**Capacity factor and maintenance architecture**: The 95-97% CF claim rests on 30-day planned outages for blanket/divertor replacement. No published maintenance plan, time-motion study, or remote-handling design exists. ITER's remote-handling timeline for blanket replacement is months (though ITER is FOAK and not optimized for availability). EU-DEMO targets 75% CF NOAK with optimized maintenance — Infinity Two's 95% CF is a 27% improvement. If actual outages are 60-90 days (credible for stellarator non-planar geometry), CF drops to 88-92%, degrading LCOE by 5-10%.

**Heat flux width scaling**: Bader et al. report factor-of-3 uncertainty (λ_q = 1.5-4.4 cm) in scrape-off-layer heat flux width at Infinity Two parameters. W7-X data at 2.5 T gives λ_q ~ 4-5 cm; extrapolating to 9 T with unknown stellarator SOL transport scaling is uncertain. If λ_q is narrow (1.5 cm), radiation fraction must exceed 90% to stay below 10 MW/m² peak heat load, possibly forcing LIBD adoption. LIBD capital cost is unknown (TRL 1-2). Infinity One (2029) will retire this uncertainty, but until then it is a **design-choice risk** (classical vs. LIBD) with cost implications.

**Blanket and divertor lifetime**: The 2-year operation cycle assumes blanket and divertor last at least 2 full-power years. EU-DEMO HCPB studies cite 2-6 FPY blanket lifetime depending on EUROFER embrittlement (50-200 dpa range). At pessimistic end (50 dpa → 1-2 FPY), blanket requires annual replacement and CF drops. Infinity Two's radial build and shielding are not disclosed, so neutron fluence at blanket structure is unknown. Divertor lifetime is similarly unspecified (tungsten monoblocks degrade under 14 MeV neutrons and thermal cycling; ITER divertor replacement is planned every 2-5 years depending on fluence and erosion).

---

### What We Have No Data On (Low Confidence, >50% Uncertainty or "Unknown Unknown")

**Dual-chemistry blanket integration cost**: HCPB and FLiBe are priced separately in the library, but the dual-zone architecture (helium-molten-salt thermal interfaces, dual tritium extraction, differential thermal expansion) has no cost analogue. EU-DEMO HCPB is single-chemistry; Renaissance FLiBe is single-chemistry. Type One Energy has not disclosed blanket module cost, relative HCPB/FLiBe volumes, or integration complexity. The library's C220101 = $346M (1 GWe NOAK) is a **placeholder** — could be 30-50% too low if dual-chemistry integration is complex, or 10-20% too high if FLiBe zones are cheap filler.

**LIBD capital cost** (if required): Large Island Backside Divertor is TRL 1-2 with no engineering design or cost estimate. The dome structure, internal pumping, and blanket integration are entirely conceptual. If LIBD adds $200-300M to C220108 (currently $62M at 1 GWe NOAK), overnight capital rises by ~1% and LCOE by ~1%. If LIBD integration cascades into blanket redesign or schedule delay, the cost impact is larger.

**First-of-a-kind execution risk**: Infinity Two is the first large-scale stellarator with HTS coils, first dual-chemistry HCPB+FLiBe blanket, first island divertor at 9 T steady-state. FOAKE projects historically overrun cost and schedule by 50-200% (ITER, NIF, Vogtle 3/4). The library's NOAK projection ($28,000/kW overnight, $310/MWh LCOE) assumes learning from Infinity One and modular construction efficiency. The **FOAK plant** (presumably Infinity Two itself, or possibly a second plant after Infinity One validation) could be 50-100% more expensive, pushing FOAK LCOE to $450-600/MWh.

---

### Dominant Source of LCOE Uncertainty

**Capacity factor** (95-97% claimed vs. 85-90% credible baseline) is the single largest uncertainty. LCOE scales inversely with CF; a 10-percentage-point CF error translates to ~10-12% LCOE error at constant overnight capital. The $310/MWh model result assumes 95.9% CF; at 85% CF, LCOE rises to ~$340-350/MWh.

This uncertainty is **knowable but not yet known** — it depends on stellarator maintenance architecture and remote-handling execution, which are engineering challenges rather than physics unknowns. Infinity One (2029) and detailed maintenance planning will resolve this.

**HTS coil cost** (C220103 = 23% of overnight capital) is the second-largest uncertainty. A 50% error in coil unit cost translates to ~11% error in overnight capital and ~9-10% error in LCOE. This is also **knowable but not yet known** — it depends on 3D HTS winding learning curve, yield rates, and manufacturing scale.

**Combined**: If CF is 85% (not 96%) and HTS coils are 50% more expensive than library default, LCOE rises to ~$390-410/MWh — a 26-32% increase over the $310/MWh model result. This is the **pessimistic-but-not-implausible** bound.

**Confidence in $310/MWh LCOE**: **±30%** (range $220-400/MWh), with the pessimistic end ($350-400/MWh) more likely than the optimistic end ($220-250/MWh) given FOAKE risk and aggressive CF assumptions.

## 7. What Would Change My Mind

### 1. Type One Energy Publishes Bottom-Up HTS Coil Cost Estimate (↓ or ↑ LCOE by 5-15%)

**What it is**: Engineering cost model for Infinity Two HTS coils — unit cost per coil ($/coil), fabrication timeline (months/coil), and total C220103 account estimate. Breakdown of winding labor, REBCO tape cost, structural forms, quench protection, assembly/alignment, and first-article learning curve.

**Why it matters**: C220103 = $4.1B (23% of 1 GWe overnight capital) is entirely extrapolated from CFS planar TF coils + W7-X LTS modular coils. If Type One Energy's actual coil cost is 30-50% lower (due to modular construction efficiency, CFS tape supply chain, or simplified winding fixtures), LCOE drops to $280-290/MWh. If coil cost is 50-100% higher (due to 3D winding complexity, tight field-error tolerances, or low first-article yield), LCOE rises to $340-370/MWh.

**What would convince me**: Published cost estimate with traceable unit costs ($/kA-m for REBCO tape, $/hour for winding labor, $/kg for structural alloys, etc.) cross-checked against CFS SPARC coil data or independent bottom-up model from ORNL/MIT/IPP.

**Direction**: Could go either way — modular construction optimism says coils are cheaper than library default; FOAKE pessimism says coils are more expensive. My prior is **coils are 20-40% more expensive** due to stellarator geometry premium, pushing LCOE to $340-360/MWh.

---

### 2. Infinity One Validates 30-Day Outage for Blanket/Divertor Replacement (↓ LCOE by 10-15%)

**What it is**: Time-motion study or actual operational data from Infinity One (post-2029) demonstrating blanket and/or divertor cassette replacement in ≤30 days using remote handling and pre-assembled modules.

**Why it matters**: The 95-97% CF claim is the single largest LCOE driver. At 95% CF, LCOE is $310/MWh. At 85% CF (if outages take 60-90 days), LCOE rises to $340-360/MWh. Validating the 30-day outage confirms the CF advantage and locks in the $310/MWh result.

**What would convince me**: Infinity One maintenance campaign report showing: (1) shutdown → module removal → new module installation → startup in ≤30 days, (2) robotic handling with no unplanned delays, (3) modular cassette interfaces (blanket, divertor, FLiBe/helium manifolds) that decouple cleanly without field welding or extended leak-checking. Alternatively, a full-scale mock-up maintenance simulation (ITER-style) validating the timeline.

**Direction**: If validated, **LCOE stays at $310/MWh** (confirms model assumption). If invalidated (outages take 60+ days), **LCOE rises to $340-360/MWh** (CF drops to 85-90%).

My prior: **60-day outages are more credible** for stellarator geometry, pushing CF to 88-92% and LCOE to $330-350/MWh. Infinity Two's claim is aggressive but not impossible — EU-DEMO targets 30-60 day outages for tokamak maintenance with optimized remote handling.

---

### 3. Classical Island Divertor Fails at Infinity One → LIBD Required (↑ LCOE by 3-8%)

**What it is**: Infinity One divertor experiments (2029+) show that classical island divertor cannot achieve (1) <10 MW/m² peak heat loads at λ_q = 1.5 cm, or (2) >0.5% particle exhaust efficiency, forcing adoption of the Large Island Backside Divertor for Infinity Two.

**Why it matters**: LIBD is TRL 1-2 with no cost estimate. If LIBD adds $200-300M to C220108 (currently $62M at 1 GWe NOAK), overnight capital rises by ~1% and LCOE by ~1%. However, LIBD integration complexity could cascade into blanket redesign (FLiBe/HCPB interfaces in island region), schedule delay (2-3 years to engineer LIBD dome structure and particle pumping), or TBR degradation (if LIBD dome blocks breeding volume). Worst case: LIBD + blanket redesign + 3-year schedule slip → LCOE rises by 5-10% due to capital escalation and financing costs.

**What would convince me**: Infinity One detached-operation experiments showing radiation fraction <80% at acceptable density (too low to stay below 10 MW/m² heat loads), or particle exhaust efficiency <0.5% (insufficient to remove helium ash). If classical divertor performance is marginal, LIBD becomes necessary.

**Direction**: **Upward** — LIBD required, adding $200-500M capital and 2-3 year schedule risk. LCOE rises to $320-340/MWh (direct capital impact + financing cost of delay).

My prior: **Classical island divertor works** — W7-X validation is strong, and radiation fraction >85% is achievable with neon/argon seeding. LIBD remains a backup, not the baseline.

---

### 4. TBR Engineering Degradation Worse Than Expected → External Tritium Required (non-LCOE impact, fleet-scaling constraint)

**What it is**: Engineering blanket design for Infinity Two (with realistic module gaps, welds, penetrations, shielding around ports) shows TBR degradation >20% from ideal neutronics (1.30 → <1.04 after degradation + extraction losses).

**Why it matters**: If TBR_eng < 1.05, Infinity Two cannot achieve tritium self-sufficiency and requires external tritium supply indefinitely. This caps fleet scalability at the number of plants supportable by CANDU byproduct + other fusion breeders. For a **single plant**, the LCOE impact is minimal (tritium fuel cost ~$0.5-1/MWh even at $30k/g market price). For a **fusion industry**, this is a gating constraint — if no D-T concept achieves TBR > 1.05 in practice, the D-T pathway cannot scale beyond ~10-20 plants globally.

**What would convince me**: EU-DEMO HCPB engineering design showing TBR degradation >15% (pushing Infinity Two's 1.30 neutronics to <1.10 engineering), or Infinity Two radial build analysis revealing thin blanket zones at penetrations where TBR contribution is lost.

**Direction**: **Non-LCOE impact** (tritium fuel cost is small), but **fleet-scaling risk**. If TBR < 1.05 is common across D-T concepts, the fusion industry pivots to D-He3, aneutronic, or breeder-blanket optimization R&D.

My prior: **TBR_eng = 1.10-1.15** after 12-15% degradation — adequate for self-sufficiency but thin margin. This is a **"watch closely"** item, not a showstopper.
