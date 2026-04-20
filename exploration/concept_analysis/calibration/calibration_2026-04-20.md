# Cross-Concept Calibration: LCOE Downselect Scores

**Date**: 2026-04-20
**Concepts calibrated**: 6
**Pass**: 2 (cross-concept consistency review with C7 gate audit)
**Prior calibration**: 2026-04-14 (13 concepts; this batch includes 6 concepts that were in that calibration, now re-scored from updated Pass 1 syntheses)

## Concepts Under Review

| ID | Concept | Company | Fuel | Confinement |
|----|---------|---------|------|-------------|
| 01 | HTS Compact Tokamak | Commonwealth Fusion Systems | D-T | MFE (tokamak) |
| 07 | MagLIF | Pacific Fusion / Fuse Energy | D-T | MIF (z-pinch) |
| 09 | QI Stellarator - HTS | Proxima Fusion | D-T | MFE (stellarator) |
| 10 | Large-Scale Stellarator | Gauss Fusion | D-T | MFE (stellarator) |
| 14 | MTF - Pneumatic Compression | General Fusion | D-T | MIF (MTF) |
| 22 | Projectile ICF | First Light Fusion / NearStar | D-T | IFE (projectile) |
| 28 | HTS Tokamak - Full HTS | Energy Singularity | D-T | MFE (tokamak) |

**Note**: All 7 concepts use D-T fuel, simplifying C5 calibration (all share identical fuel safety profiles). This batch lacks aneutronic comparators, which limits C5 spread.

## Pass 1 Score Summary

| Concept | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Composite |
|---------|----|----|----|----|----|----|----|----|
| 01-HTS Compact Tokamak | 3.5 | 2.5 | 3.2 | 2.0 | 1.8 | 3.0 | 3.5 | 2.93 |
| 07-MagLIF | 4.0 | 4.5 | 3.0 | 3.0 | 2.0 | 3.5 | 2.5 | 3.21 |
| 09-QI Stellarator HTS | 3.3 | 3.0 | 2.8 | 2.5 | 2.8 | 4.0 | 3.5 | 3.13 |
| 10-Large-Scale Stellarator | 2.9 | 2.0 | 3.1 | 2.0 | 3.2 | 4.0 | 3.5 | 2.96 |
| 14-MTF Pneumatic | 3.0 | 4.0 | 2.8 | 2.5 | 2.0 | 3.0 | 2.5 | 2.83 |
| 22-Projectile ICF | 3.3 | 4.0 | 3.8 | 3.5 | 3.2 | 3.8 | 2.0 | 3.37 |
| 28-HTS Tokamak Full HTS | 2.8 | 3.5 | 3.3 | 2.5 | 2.0 | 3.5 | 3.0 | 2.94 |

---

## Part 1: C7 Gate Audit

### Gate Audit Methodology

For each concept, I enumerate every physics or engineering milestone required for net electricity production, cross-check against peer concepts for consistency, and flag undercounted gates. The standard gates checked across ALL concepts are:

1. **Net energy gain** (Q > 1 at claimed conditions)
2. **Confinement mode validity** (at commercial parameters)
3. **Driver/heating system at commercial rep-rate or power level**
4. **Energy conversion mechanism** (if non-standard)
5. **Fuel burn regime** (if non-standard)
6. **Chamber/first-wall survival** (at commercial conditions)
7. **Tritium breeding ratio** (for D-T concepts — all concepts in this batch)

---

### 01-HTS Compact Tokamak (CFS)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| I-mode confinement at 0.55 MW/m²/n₂₀, 9.2 T | Binary | Subscale (C-Mod at 6T) | −0.50 | Extrapolation from 6T to 9.2T and different geometry; SPARC will test but not yet validated |
| Demountable HTS joints at 23T reactor conditions | Degrading | Subscale (CFS 20T, 77K demo) | −0.25 | Fallback: welded coils (availability penalty, not concept failure) |
| FLiBe tritium extraction <1% loss rate | Degrading | Analytical | −0.50 | Lab-scale demo only; no reactor integration; fallback to higher tritium inventory |
| FLiBe MHD behavior at 9.2T | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. MHD effects on FLiBe heat transfer in 9.2T toroidal field are uncharacterized at reactor conditions. Conducting liquid in strong field induces pressure drop, flow redistribution, and thermal performance degradation. Fallback: accept lower thermal efficiency or redesigned flow geometry. Cross-check: CAS-09 (Proxima) scored a PbLi MHD gate for WCLL; CAS-01 uses FLiBe under comparably strong fields but omitted the MHD gate. |
| TBR ≥ 1.05 with FLiBe blanket | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. All D-T concepts face this gate; CAS-09 and CAS-10 include it. FLiBe blanket TBR has not been validated at 14 MeV neutron spectrum. CAS-01's synthesis omitted it entirely. Schedule gate because FLiBe chemistry has TBR headroom via Li-6 enrichment. |
| 8 GHz LHCD at 25 MW | Schedule | Subscale (6 GHz proven) | −0.125 | Engineering scale-up; no physics blocker |
| REBCO tape at $10/kA-m | Schedule | Subscale (trajectory from $144→$100) | 0 | On track; effectively retired |

**Pass 1 total penalty**: −1.375 → C7 = 3.625 → 3.5
**Recalculated penalty**: −0.50 − 0.25 − 0.50 − 0.50 − 0.25 − 0.125 − 0 = −2.125 → C7 = 2.875 → **2.9**
**Gate count change**: Pass 1 had 5 gates; audit finds 7 (added FLiBe MHD and TBR).
**Floor rule**: 1 binary gate → does not trigger floor.

**Calibrated C7: 3.0** (rounding 2.9 up slightly; the two added gates are genuinely present in peer concept analyses but moderate in severity — FLiBe MHD is a degrading gate with fallback, TBR is a schedule gate shared with all D-T concepts).

---

### 07-MagLIF (Pacific Fusion / Fuse Energy)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Ignition at 60+ MA with cryo DT targets | Binary | Analytical (2D sims benchmarked to Z) | −1.00 | χ ≈ 0.1 demonstrated at Z; ignition (χ ≥ 1) undemonstrated at any MA level. Simulation-only for >25 MA. |
| Automated RTL insertion at 1+ Hz | Degrading | Analytical | −0.50 | Z-IFE study identified as solvable but no hardware demo. Fallback: lower rep rate at higher LCOE. |
| Thick-liquid-wall chamber survival (GJ-scale repetitive blast) | Degrading | Analytical (HYLIFE-II analogue) | −0.50 | Laser IFE analogue exists; no fusion-scale test for MagLIF-class yields. Fallback: solid chamber with 10–15% CF penalty and scheduled replacement. |
| Cryo target fabrication at <$2/shot | Degrading | Speculative | −0.75 | Non-cryo self-magnetizing pathway demonstrated at 22 MA but gain unknown. No demonstrated cryo path at cost target. If non-cryo fails, this upgrades to binary. |
| IMG driver cost <$100M at plant scale | Schedule | Subscale (TITAN I 10× reduction) | −0.125 | Current ~$5/J vs. <$0.50/J target; manufacturing demonstrated at 1 TW scale. |
| Rep-rate chamber clearing <1s | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis identifies 1 Hz requiring <1s debris clearing, FLiBe flow re-establishment, AND RTL insertion in sequence. Chamber clearing (blast debris, vapor dissipation, liquid reconstitution) is a separate constraint from RTL insertion. Cross-check: all pulsed IFE concepts (CAS-22) carry a chamber clearing gate — MagLIF must too. |
| Per-shot consumable cost (RTL remanufacturing) | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. Analysis identifies 170 MWe parasitic load for RTL steel remanufacturing (17% recirculating power fraction). If RTL cost doesn't reach $0.70/shot target, LCOE degrades significantly. This is an independent economic gate separate from the driver cost and target fabrication gates. |

**Pass 1 total penalty**: −2.875 → C7 = 2.125 → 2.5
**Recalculated penalty**: −1.00 − 0.50 − 0.50 − 0.75 − 0.125 − 0.25 − 0.50 = −3.625 → C7 = 1.375 → **1.5**
**Gate count change**: Pass 1 had 5 gates (1 binary); audit finds 7 (1 binary, 4 degrading, 2 schedule — added chamber clearing and RTL consumable cost).
**Floor rule**: 1 binary gate → does not trigger.

**Calibrated C7: 1.5** (the two additional gates — chamber clearing and RTL consumables — are genuine constraints identified in the analysis that Pass 1 partially collapsed into single items. Separating them correctly increases total penalty from 2.875 to 3.625. The score of 1.5 reflects one unretired binary gate on ignition plus heavy cumulative degrading gate penalty from cryo targets, RTL insertion, liquid wall, and consumable cost).

---

### 09-QI Stellarator HTS (Proxima)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| QI alpha confinement at burning plasma | Degrading | Subscale (W7-X QI confinement validated; alpha physics unvalidated at burning plasma power density) | −0.25 | Fallback: 50 MW sustained ECRH at higher LCOE. SIMPLE/ANTS simulations show ~0.8% loss. |
| Island divertor at 4.05 MW/m² steady-state | Degrading | Subscale (W7-X steady-state detachment at low power density; 30-min discharge and 1.8 GJ energy record validate duration, not power density) | −0.25 | Fallback: higher erosion and shorter replacement intervals. |
| 3D HTS coil quench protection at 111 GJ | Schedule | Analytical (quench propagation models exist; W7-X validated LTS quench safety) | −0.25 | No physics blocker; engineering scale-up of energy dump systems. |
| WCLL tritium extraction at kg/day throughput | Schedule | Subscale (lab-scale PbLi extraction; ITER TBM program) | −0.125 | Shared with all D-T MFE concepts. |
| TBR ≥ 1.05 with engineering losses | Schedule | Analytical (1.074 post-correction; Monte Carlo with margins) | −0.25 | Tight margin; Li-6 enrichment headroom provides fallback. |
| 3D non-planar HTS coil manufacturing at <2× wound cost | Degrading | Analytical (no demo; SMC 2027 first validation) | −0.25 | **Recognized in synthesis text as "viability gate" but not scored in Pass 1 gate table.** If coil cost >2.5× wound tokamak baseline, concept is "economically retired regardless of C2–C7 performance" (synthesis language). This is a degrading gate (fallback: higher LCOE), not merely a supply chain concern. |

**Pass 1 total penalty**: −1.125 → C7 = 3.875 → 3.5
**Recalculated penalty**: −0.25 − 0.25 − 0.25 − 0.125 − 0.25 − 0.25 = −1.375 → C7 = 3.625 → **3.5**
**Gate count change**: Pass 1 had 5 gates (0 binary, 2 degrading, 3 schedule); audit finds 6 (0 binary, 3 degrading, 3 schedule — added coil manufacturing as degrading gate).
**Floor rule**: 0 binary gates → does not apply.

**Calibrated C7: 3.5** (adding the coil manufacturing gate increases penalty by 0.25, offset by marginal rounding — net score stays at 3.5. The concept has no binary gates. Strongest physics heritage among stellarators via W7-X. The absence of binary gates is the key differentiator from tokamak concepts where I-mode or similar confinement modes create binary risk).

---

### 10-Large-Scale Stellarator (Gauss)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| QI confinement at 18m scale | Degrading | Subscale (W7-X 5.5m; HSR studies at ~20m) | −0.25 | Fallback: larger machine or reduced power density at higher LCOE. Physics extrapolation is well-supported by ISS04 scaling. |
| Non-planar HTS coil fabrication at 30m scale (<1mm tolerance) | Schedule | Analytical (W7-X coils at 5.5m achieved <1mm; 30m is engineering extrapolation) | −0.25 | No physics blocker but manufacturing challenge is severe. 5.5× scale-up in linear dimension. |
| Demountable SC joints at 100 kA / 1 nΩ | Schedule | Analytical (KIT prototypes underway) | −0.25 | Cross-check: CAS-01 carries this gate as degrading for CFS. CAS-10 has comparable demountable joint requirement. Keeping as schedule because Gauss's fallback (non-demountable, longer maintenance) is well-characterized. |
| TBR > 1.05 in realistic 3D geometry | Degrading | Subscale (idealistic 1.39, realistic 1.15 with gaps; margin exists but tight) | −0.25 | ParaStell analysis identifies tight LCFS-coil spacing regions as TBR concern. Li-6 enrichment headroom provides partial fallback. |
| HTS conductor cost $5–10/kA-m | Schedule | Subscale (industrial tape production trajectory) | −0.125 | Shared with all HTS concepts. |
| Blanket segment assembly (80 unique shapes) | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis identifies Segment 5 exceeding RCC-MRx failure criterion. 80 unique shapes prevent standardized manufacturing. Assembly complexity is extreme — no industrial precedent for 80-variant remote installation. Will eventually be solved but timeline highly uncertain. |
| FOAK construction schedule (10-year nominal) | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis identifies IDC representing 28% of capital; extension to 14 years adds $2B. Construction schedule risk is a legitimate engineering gate — if schedule slips to 14 years, LCOE rises 28%. |

**Pass 1 total penalty**: −1.125 → C7 = 3.875 → 3.5
**Recalculated penalty**: −0.25 − 0.25 − 0.25 − 0.25 − 0.125 − 0.25 − 0.25 = −1.625 → C7 = 3.375 → **3.5**
**Gate count change**: Pass 1 had 5 gates; audit finds 7 (0 binary, 2 degrading, 5 schedule — added blanket assembly and construction schedule).
**Floor rule**: 0 binary gates → does not apply.

**Calibrated C7: 3.5** (two additional schedule gates add 0.5 penalty but the concept remains at 3.5 after rounding. Absence of binary gates and strong W7-X heritage anchor the score. The stellarator physics pathway is the most experimentally validated of any concept in this batch).

---

### 14-MTF Pneumatic Compression (General Fusion)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Pneumatic piston synchronization at commercial scale (<1% timing error) | Binary | Analytical (CFD modeling only) | −1.00 | No experimental demonstration of pneumatic pistons compressing liquid metal at any scale. The commercial compression mechanism is TRL 2–3. |
| Compression ratio 12:1 in liquid metal | Binary | Subscale (8:1 achieved in water surrogate) | −0.50 | **Reclassified from Degrading to Binary**. Analysis states if 12:1 not achieved, plasma may not reach thermonuclear temperatures — this is concept failure, not cost degradation. Water achieved 8:1; 12:1 required in a different medium (liquid metal, which has MHD complications). 33% shortfall in a fundamentally different medium. |
| LM26→Commercial technology transfer | Binary | Analytical | −1.00 | **UNDERCOUNTED in Pass 1**. LM26 uses electromagnetic theta-pinch compression with a solid lithium liner; the commercial plant uses pneumatic pistons compressing a flowing liquid metal vortex. These are fundamentally different compression mechanisms. LM26 success validates compact toroid formation and some plasma physics but does NOT validate the commercial compression pathway. The pneumatic system has never been built at any scale. This is an independent binary gate. |
| Lawson criterion achievement (nTτ > 10²¹) with CT plasma | Degrading | Subscale (LM26 pre-compression CT demonstrated >10 ms confinement at 50% plasma scale) | −0.25 | Fallback: fusion conditions at lower efficiency (higher recirculating power). |
| 1 Hz rep rate with vortex reformation | Schedule | Analytical (no demo at >0.001 Hz with liquid metal; 86,400× gap from ~1 shot/day to 1 Hz) | −0.25 | Mechanics expected to work eventually (no physics blocker) but timeline uncertain. |
| TBR ~1.5 in flowing Li/PbLi | Schedule | Subscale (ITER TBM loops, analytical TBR studies) | −0.125 | Generic liquid metal tritium breeding is TRL 4–5; integration at GF geometry unproven. |
| Liquid metal composition resolution (Li vs. PbLi) | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. Analysis identifies that Li vs. PbLi affects tritium inventory (>60% vs >80% in blanket), extraction capital cost, materials compatibility, safety hazard profile, and neutron multiplication efficiency. This branches the entire cost model. Degrading gate because either choice works but at materially different cost points. |

**Pass 1 total penalty**: −1.875 → C7 = 3.125 → adjusted to 2.5
**Recalculated penalty**: −1.00 − 0.50 − 1.00 − 0.25 − 0.25 − 0.125 − 0.50 = −3.625 → C7 = 1.375 → clamped to **1.5**
**Gate count change**: Pass 1 had 5 gates (1 binary); audit finds 7 (3 binary, 2 degrading, 2 schedule — reclassified compression ratio to binary, added technology transfer gap, added liquid metal composition).
**Floor rule check**: 3 binary gates identified: (1) piston synchronization at analytical evidence, (2) compression ratio at subscale evidence, (3) technology transfer at analytical evidence. Floor rule requires ≥3 binary gates at "analytically supported or worse." Gate (2) at subscale evidence (0.5× multiplier) is *better* than analytical → does not count toward the ≥3 threshold. Only 2 binary gates at analytical or worse → **floor does not apply**.

**Calibrated C7: 1.5** (formula gives 1.375, rounded to 1.5. The reclassification of compression ratio to binary and addition of the technology transfer gap are the major audit findings. The LM26→commercial technology disconnect is the most critical finding: even if LM26 succeeds, it validates electromagnetic compression in a solid liner, not pneumatic compression in a flowing liquid metal vortex).

---

### 22-Projectile ICF (First Light Fusion / NearStar)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Target gain ≥200× at 60 km/s | Binary | Analytical (FLF simulations only; ~50 neutrons at 6.5 km/s in experiments) | −1.00 | Massive extrapolation from ~50 neutrons to breakeven gain. NIF record Q~4 at very different conditions (laser, hohlraum) — not transferable to projectile impact. |
| EM gun achieving 60 km/s at rep-rate without catastrophic bore erosion | Binary | Speculative | −1.50 | Machine 4 (100 MJ, 60 km/s) was cancelled before testing (Feb 2025). No experimental data at target velocity. Bore erosion at hypervelocity is unknown — closest analogues (railguns) suffer severe erosion at 2–3 km/s, far below the 60 km/s target. 20–30× velocity extrapolation beyond any laboratory demonstration. |
| Liquid Li curtain stability at 0.033–0.1 Hz | Degrading | Subscale (HYLIFE-II fluid dynamics models) | −0.25 | Fallback: solid wall with scheduled replacement (10–15% CF penalty and higher capital). |
| Target fabrication at <$10/target | Degrading | Subscale (lab-scale demonstrated) | −0.25 | Mass production at 800K/year unproven; semiconductor manufacturing analogy partially applicable. Fallback: higher target cost adds ~$6/MWh. |
| Chamber clearing <10s | Schedule | Subscale (HYLIFE analogue for clearing dynamics) | −0.125 | At 0.033 Hz, 30s cycle time provides generous margin. Cross-check with other IFE concepts: MagLIF needs <1s at 1 Hz — FLF's 0.033 Hz makes this easier. |
| Driver lifespan at rep-rate (bore erosion) | — | — | — | Captured within Gate 2 above (bore erosion is part of the 60 km/s gate). Not double-counted. |

**Pass 1 total penalty**: −3.125 → C7 = 1.875 → 2.0
**Recalculated penalty**: −1.00 − 1.50 − 0.25 − 0.25 − 0.125 = −3.125 → C7 = 1.875 → **2.0**
**Gate count change**: Pass 1 had 5 gates (2 binary, 2 degrading, 1 schedule); audit finds 5 gates (consistent). The Pass 1 enumeration is complete for this concept.
**Floor rule check**: 2 binary gates (1 analytical, 1 speculative) → does not trigger ≥3 floor.

**Calibrated C7: 2.0** (audit confirms Pass 1's gate enumeration is correct. The EM gun at speculative evidence and target gain at analytical evidence are the binding constraints. Machine 4 cancellation and FLARE pivot are contextual — they mean no one is actively working to retire Gate 2, but as per rubric, programmatic risk is not a physics gate).

---

### 28-HTS Tokamak Full HTS (Energy Singularity)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| D-T tokamak confinement at Q > 10 | Degrading | Subscale (JET Q=0.67, TFTR Q=0.3; SPARC targets Q>10 but not yet achieved) | −0.25 | Fallback: larger machine at higher capital cost. Core tokamak physics extensively validated. |
| Full-HTS CS coil reliability at 25T cyclic loading | Degrading | Analytical (Jingtian test magnet 21.7T proves field achievable; CS duty cycle modeled but multi-year fatigue under combined EM + neutron + gamma undemonstrated) | −0.50 | Fallback: replace CS coils every 3–5 years (Scenario A: 65% availability, +22% LCOE). |
| AI plasma control at burning-plasma conditions | Degrading | Subscale (HH70 1,337s steady-state at experimental conditions, no fusion power, no radiation) | −0.25 | Fallback: conventional disruption frequency at ~70% availability. |
| TBR > 1.05 in undisclosed blanket | Degrading | Analytical | −0.50 | **Reclassified from Schedule to Degrading**. No blanket design exists (TRL 1–2). This is more severe than "will eventually pass" — the entire blanket architecture is undefined. If no viable blanket fits the compact geometry, concept degrades to larger machine or lower power density. Cross-check: CAS-01 has a FLiBe blanket concept (TRL 3–4); CAS-28 has zero disclosed concept, warranting higher severity. |
| 25T HTS coil quench protection and energy extraction | Schedule | Subscale (HH70 26-coil system operational at 2.5T; 25T energy is 10× higher) | −0.125 | Engineering; no physics blocker. Quench detection for REBCO at 20 K is analytically understood. |
| ICRH scaling to plant power | Schedule | Subscale | −0.125 | **UNDERCOUNTED in Pass 1**. Analysis notes plant-scale ICRH configuration "undefined." ICRH is the sole heating method; coupling efficiency at burning plasma conditions is unvalidated. Schedule gate because ICRH physics is proven at sub-reactor scale. |
| Power conversion cycle undefined | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis notes power conversion at TRL 1–2; cycle type and efficiency undisclosed; tritium-compatible heat exchangers unqualified. Will eventually be solved but timeline uncertain. |

**Pass 1 total penalty**: −1.375 → C7 = 3.625 → then −0.5 blanket penalty → 3.0
**Recalculated penalty**: −0.25 − 0.50 − 0.25 − 0.50 − 0.125 − 0.125 − 0.25 = −2.0 → C7 = 3.0
**Gate count change**: Pass 1 had 5 gates (0 binary); audit finds 7 (0 binary, 4 degrading, 3 schedule — added ICRH scaling and power conversion, reclassified TBR from schedule to degrading).
**Floor rule**: 0 binary gates → does not apply.

**Calibrated C7: 3.0** (the score matches Pass 1's adjusted value of 3.0, but through proper gate enumeration rather than an ad-hoc blanket penalty. The reclassification of TBR to degrading and addition of two schedule gates replaces the ad-hoc −0.5 with structurally justified penalties. No binary gates and strong tokamak physics heritage keep the score above the MIF/IFE concepts).

---

### C7 Gate Audit Summary

| Concept | Pass 1 Gates | Audit Gates | Binary (P1→Audit) | C7 P1 | C7 Calibrated | Change |
|---------|-------------|-------------|-------------------|-------|---------------|--------|
| 01-CFS | 5 | 7 | 1→1 | 3.5 | 3.0 | −0.5 |
| 07-MagLIF | 5 | 7 | 1→1 | 2.5 | 1.5 | −1.0 |
| 09-Proxima | 5 | 6 | 0→0 | 3.5 | 3.5 | 0 |
| 10-Gauss | 5 | 7 | 0→0 | 3.5 | 3.5 | 0 |
| 14-GF | 5 | 7 | 1→3 | 2.5 | 1.5 | −1.0 |
| 22-FLF | 5 | 5 | 2→2 | 2.0 | 2.0 | 0 |
| 28-ES | 5 | 7 | 0→0 | 3.0 | 3.0 | 0 |

**Systematic findings**:

1. **Gate undercounting**: Pass 1 undercounted gates by 0–2 per concept. The most common omissions are TBR gates (present for CAS-09/10 but missing from CAS-01), MHD behavior gates (CAS-01 FLiBe), and technology transfer gaps (CAS-14 LM26→commercial).

2. **MIF concepts hit hardest**: MagLIF (−1.0) and GF (−1.0) both drop a full point because their pulsed architectures create additional distinct failure modes (chamber clearing, consumable cost, technology transfer) that Pass 1 scorers partially collapsed into single gates.

3. **Stellarators stable**: CAS-09 and CAS-10 remain at 3.5 — the additional schedule gates from the audit are offset by rounding. Absence of binary gates is the key differentiator.

4. **Binary gate reclassification**: GF's compression ratio (8:1 in water, 12:1 needed in liquid metal) was reclassified from degrading to binary because failure to achieve 12:1 means no thermonuclear conditions — this is concept failure, not cost degradation.

---

## Part 2: Other Inconsistencies Found (C1–C6)

### Inconsistency 1: C6 — Scheduled downtime estimates ignore replacement complexity assessment

**Concepts affected**: 01-CFS (C6=3.0), 07-MagLIF (C6=3.5), 28-ES (C6=3.5)

**Problem**: The rubric requires estimating replacement duration using four multipliers (access method, maintenance environment, component modularity, serial step count). Pass 1 for CAS-01 assumes "2-week blanket outage if demountable joints work" — this is far too optimistic for a D-T tokamak.

**CAS-01 replacement complexity assessment (blanket)**:
- Access method: Direct parallel access via demountable joints (1×) — IF joints work. If not, port-limited (2.5×).
- Maintenance environment: Fully remote (D-T activation, 14 MeV neutrons) → 5–10× (use 7×)
- Component modularity: Blanket segments are aligned-fit with mechanical fasteners (2×) — not slide-in/slide-out due to FLiBe sealing requirements
- Serial steps: Cool joints → open joint → drain FLiBe → extract segment → install new → seal → refill → test → re-cool → commission → plasma conditioning = ~8 steps
- Baseline 4 days × 1 (demountable access) × 7 (remote) × 2 (aligned fit) × 1.5 (8 steps) = **84 days**
- Even with demountable joints: 84 days, not 14 days as Pass 1 assumed
- Without demountable joints: 4 × 2.5 × 7 × 2 × 2.0 (10 steps) = **280 days**

At 4 FPY replacement interval and 84-day outage: 84/(4×365) = **5.7% scheduled** (blanket only). Plus divertor at 2 FPY (estimate 42 days via similar assessment): 42/(2×365) = **5.7%**. Total scheduled ~11%. Unscheduled ~5% (disruptions, demountable joint reliability, BOP). CF_upper = (1 − 0.11 − 0.05) × 1.0 = **84% → still in 80–90% band → score 4**.

However, Pass 1's C6 = 3.0 was too low (included TRL penalty). The corrected score using physical CF_upper and rubric-compliant replacement duration is **C6 = 4.0**.

**CAS-28 replacement complexity assessment (blanket)**:
- Access method: Non-demountable coils → port-limited access (2.5×)
- Maintenance environment: Fully remote (D-T, 14 MeV) → 7×
- Component modularity: Blanket design undisclosed → assume aligned-fit (2×)
- Serial steps: Same as tokamak without demountable advantage; access through ports limits parallelism → ~8–10 steps (use 9) → 2×
- Baseline 4 days × 2.5 × 7 × 2 × 2 = **280 days**
- At 2–3 FPY replacement interval (from 3 MW/m² wall loading): 280/(2.5×365) = **30.7% scheduled** (blanket only)
- This is devastating. Even at 3 FPY: 280/(3×365) = **25.6%**

Pass 1 assumed 60-day replacement → 8% scheduled. The rubric-compliant replacement complexity assessment gives 280 days for a non-demountable D-T tokamak with port-limited access. CF_upper = (1 − 0.26 − 0.04) × 1.0 = **70% → 70–80% band → score 3**.

**However**, ES's analysis mentions "AI plasma control" and "modular blanket sectors" — if ES achieves sector-based access comparable to CFS's demountable approach but through non-SC joint methods (e.g., bolted VV sectors), replacement duration could be much shorter. Given zero disclosed blanket architecture, I'll use the midpoint: 140-day replacement → at 2.5 FPY = 15.3% scheduled. CF_upper = (1 − 0.15 − 0.04) × 1.0 = **81% → 80–90% → score 4**. But this is generous given zero design disclosure. **Score 3.5** (midpoint of 3 and 4 reflecting uncertainty).

**CAS-07 MagLIF replacement complexity assessment**:
Pass 1's C6 analysis is more nuanced — it correctly identifies the liquid wall as self-renewing (zero blanket replacement) but then inflates the score with "upward bias if liquid wall works." The CF_upper calculation gives 77% optimistic / 69% pessimistic, correctly placing MagLIF in the 70–80% band (score 3). Pass 1 rounded UP to 3.5 — this is an ad-hoc TRL adjustment (optimism for liquid wall) that belongs in C7, not C6. **C6 = 3.0**.

**Calibrated adjustments**:
- CAS-01 C6: 3.0 → **4.0** (CF_upper = 84% using rubric replacement complexity; remove TRL penalty)
- CAS-07 C6: 3.5 → **3.0** (CF_upper = 77% → 70–80% band; remove upward rounding)
- CAS-28 C6: 3.5 → **3.5** (CF_upper ~81% with generous midpoint assumptions; keep at 3.5 given uncertainty)

### Inconsistency 2: C6 — CAS-22 projectile ICF capacity factor overestimated

**Concepts affected**: 22-FLF (C6=3.8)

Pass 1 calculates CF_upper = 92.5% then adjusts to 3.8 for "driver replacement uncertainty." The 92.5% calculation assumes 10⁶ shots between EM gun barrel replacements — this is speculative for a system that has never fired at 60 km/s. The rubric says C6 should use physical CF_upper without TRL adjustments.

The physical CF calculation:
- Scheduled: liquid Li wall (self-renewing, 0%); EM gun barrel (10⁶ shots is speculative; at 0.033 Hz = 1M shots/yr → annual replacement; 2-week outage → 3.5%)
- Unscheduled: 4% (novel systems + BOP)
- Duty cycle: 0.033 Hz = one shot every 30s; burn ~10⁻⁶ s; dwell dominated by chamber clearing (~1–5s) + driver recharge (~1s). Duty cycle ≈ 1.0 (dwell ≪ cycle time).
- CF_upper = (1 − 0.035 − 0.04) × 1.0 = **92.5% → ≥90% → score 5**

But the barrel replacement at 10⁶ shots is entirely speculative (no experimental data). If barrel life is 10⁴ shots (severe erosion at hypervelocity), CF drops to ~82%. The rubric says to use physical parameters, not TRL adjustments. The physical parameters here ARE speculative (barrel erosion rate is unknown).

Compromise: Use **C6 = 4.5** (borderline ≥90% with uncertainty acknowledged but not TRL-penalized; the liquid Li wall genuinely eliminates the dominant maintenance driver for D-T IFE).

**Calibrated adjustment**: CAS-22 C6: 3.8 → **4.5**

### Inconsistency 3: C1 — Module count boost applied inconsistently for MagLIF

**Concepts affected**: 07-MagLIF (C1=4.0)

The rubric specifies 200+ modules/plant → +0.5 (continuous-flow manufacturing), not the +1.0 "sweet spot" applied in Pass 1. MagLIF's 10,000–50,000 capacitor bricks fall in the 200+ category. The +1.0 boost was justified by "sweet spot module count; cumulative volume across targets" but the rubric table is clear: 200+ → +0.5. Targets at millions/year are continuous-flow → also +0.5. The maximum boost should be +0.5, not +1.0.

**Calibrated adjustment**: CAS-07 C1: 4.0 → **3.5** (reduce module boost from +1.0 to +0.5)

### Inconsistency 4: C2 — MagLIF unit replication scored too high

**Concepts affected**: 07-MagLIF (C2=4.5)

MagLIF's C2 scores unit replication at 5 ("full modularity"), but each chamber requires its own dedicated pulsed power driver. The Z-IFE study showed only modest LCOE improvement from 1→10 chambers (7.0 → 5.7 ¢/kWh), suggesting economies of scale are limited. Drivers don't share across chambers — each chamber is an independent power plant with shared site infrastructure.

**Calibrated adjustment**: CAS-07 C2: 4.5 → **4.0** (reduce replication sub-factor from 5 to 4; average becomes (5+4+3.5)/3 = 4.2 → round to 4.0)

### Inconsistency 5: C3 — CAS-22 cost-weighted average arithmetic error

**Concepts affected**: 22-FLF (C3=3.8)

Pass 1 calculates cost-weighted average as 3.1 then "adjusts" to 3.8 — a +0.7 ad-hoc uplift "for driver novelty drag." But the EM gun at 74% of CAS22 capital with a learning score of 2.0 means the weighted average is anchored low regardless of target and BOP learning. Recalculation: (41M×4 + 1000M×2 + 117M×4.5 + 200M×5) / 1358M = (164 + 2000 + 526.5 + 1000) / 1358 = 3690.5 / 1358 = **2.72**. Not 3.1, and certainly not 3.8.

The EM gun's dominance of capital cost means that even excellent target learning (4.5) and excellent BOP learning (5.0) cannot overcome the 74% cost weight of a low-learning monolithic driver. This is the core structural limitation.

**Calibrated adjustment**: CAS-22 C3: 3.8 → **2.8** (using corrected cost-weighted arithmetic; the 2.72 rounds to 2.7, adjusted to 2.8 accounting for some external pulsed power demand pull)

### Inconsistency 6: C4 — CAS-22 complexity scored too favorably

**Concepts affected**: 22-FLF (C4=3.5)

The rubric reference calibration places "Laser IFE (p-B11)" at 2.5–3.5. D-T IFE with a hypervelocity driver and liquid lithium should not score at the top of this range. CAS-22 has:
- 11 CAS22 sub-accounts >1% (moderate → score 3)
- 5 simultaneous extremes including hypervelocity impact at 60 km/s (no industrial precedent) → score 2
- Coupling density: driver→target→chamber→Li curtain→heat exchanger (serial, 5 links) + tritium system (4 links) → moderate (score 2.5)
- 2 novel integration interfaces (EM gun at 60 km/s, liquid Li blast loading) → score 3

Pass 1 averaged (3 + 2.5 + 2 + 3)/4 = 2.6 then "adjusted upward for absence of magnetic coupling" to 3.5. The +0.9 ad-hoc adjustment is excessive. The absence of magnetic coupling reduces one source of complexity but the hypervelocity impact creates a different extreme that has no industrial precedent.

**Calibrated adjustment**: CAS-22 C4: 3.5 → **3.0** (use formula average of 2.6, round to 3.0 acknowledging legitimate simplicity vs. magnetic concepts but removing excessive ad-hoc uplift)

### Inconsistency 7: C5 — D-T fuel safety sub-factor inconsistently scored

**Concepts affected**: All (01, 07, 09, 10, 14, 22, 28 — all D-T)

All D-T concepts have identical fuel safety profiles (kg-scale tritium inventory, 14 MeV neutrons, EPZ, breeding requirement). Pass 1 scores range from 1.0 to 2.0 on the fuel safety sub-factor with no physical basis for distinction among D-T concepts. Standardize to **1.5** for all.

CAS-10 (Gauss) used ad-hoc double weighting on thermal rejection and seismic sub-factors, deviating from rubric equal weighting. Rubric specifies equal weighting of four sub-factors (thermal rejection, fuel safety, activation/waste, seismic/civil). Recalculate with equal weighting: (1 + 1.5 + 3 + 1.5 + 5)/5 = 2.4. Note: Pass 1 included a 5th sub-factor (grid integration) not in the rubric's 4-factor definition — this is inconsistent across concepts.

CAS-01 (CFS): Pass 1 scored 2.2 then "floored to 1.8 due to D-T tritium burden." Remove ad-hoc floor; using 4-factor rubric: (2 + 1.5 + 2 + 2)/4 = **1.9 → 2.0**.

CAS-22 (FLF): Pass 1 scored 2.7, then "slight upward adjustment" to 3.2. Using 4-factor rubric: (2 + 1.5 + 2 + 4)/4 = **2.4**. The compact footprint advantage is real but belongs in the seismic sub-factor (already scored at 4), not as a separate adjustment.

**Calibrated adjustments** (using 4-factor rubric consistently: thermal rejection, fuel safety, activation/waste, seismic/civil):
- CAS-01 C5: 1.8 → **2.0** (correct: (2 + 1.5 + 2 + 2)/4 = 1.9 → 2.0)
- CAS-07 C5: 2.0 → **2.0** (unchanged: (2 + 1.5 + 2 + 3)/4 = 2.1 → 2.0)
- CAS-09 C5: 2.8 → **2.0** (correct: (2 + 1.5 + 3 + 2)/4 = 2.1 → 2.0; original inflated by 5th sub-factor "grid integration")
- CAS-10 C5: 3.2 → **2.0** (correct: (1 + 1.5 + 3 + 1.5)/4 = 1.75 → 2.0; original used ad-hoc double weighting and 5th factor)
- CAS-14 C5: 2.0 → **2.0** (unchanged)
- CAS-22 C5: 3.2 → **2.4** (correct: (2 + 1.5 + 2 + 4)/4 = 2.4; remove ad-hoc compact footprint uplift)
- CAS-28 C5: 2.0 → **2.0** (unchanged)

**Wait — rubric check**: Re-reading the rubric, C5 has four sub-factors: thermal rejection, fuel safety profile, activation and waste, seismic/civil. Pass 1 for several concepts added "grid integration" as a 5th sub-factor. The rubric does NOT include grid integration in C5. Remove it for all concepts. This primarily affects CAS-09 (had grid integration = 5) and CAS-10 (had grid integration = 5), pulling their C5 scores down.

**Revised C5 scores** (4-factor only):

| Concept | Thermal | Fuel Safety | Activation | Seismic | C5 |
|---------|---------|-------------|------------|---------|-----|
| 01-CFS | 2 | 1.5 | 2 | 2 | **1.9 → 2.0** |
| 07-MagLIF | 2 | 1.5 | 2 | 3 | **2.1 → 2.0** |
| 09-Proxima | 2 | 1.5 | 3 | 2 | **2.1 → 2.0** |
| 10-Gauss | 1 | 1.5 | 3 | 1.5 | **1.8 → 2.0** |
| 14-GF | 1 | 1.5 | 1.5 | 3 | **1.8 → 2.0** |
| 22-FLF | 2 | 1.5 | 2 | 4 | **2.4** |
| 28-ES | 1 | 1.5 | 2 | 3 | **1.9 → 2.0** |

All D-T concepts converge to C5 ≈ 2.0 (±0.4) as expected — the D-T fuel cycle is the binding constraint. CAS-22 gets a slight uplift (2.4) from compact footprint (seismic = 4).

### Inconsistency 8: C1 — CAS-28 underscored vs. CAS-01

**Concepts affected**: 28-ES (C1=2.8) vs. 01-CFS (C1=3.5)

Both are HTS compact tokamaks with 18 TF coils in the manufacturing learning sweet spot (+1.0 boost). CAS-28's non-demountable design limits maintenance modularity but NOT manufacturing modularity — the 18 TF coils are still factory-assembled units. Pass 1 penalized CAS-28 by 0.7 points below CFS for identical magnet manufacturing architecture.

The legitimate difference: CFS's demountable joints enable blanket extraction without coil disassembly, which improves C6 (maintenance access) but should NOT affect C1 (manufacturing modularity). C1 measures how much of the plant can be factory-manufactured as standardized, repeatable modules — both CFS and ES have 18 factory-assembled HTS TF coils.

**Calibrated adjustment**: CAS-28 C1: 2.8 → **3.2** (closer to CAS-01's 3.5; remaining 0.3 gap justified by CFS's broader factory-module scope: FLiBe blanket segments as factory modules vs. ES's undisclosed blanket which may require more site assembly)

### Inconsistency 9: C2 — CAS-10 geometric scaling scored too low

**Concepts affected**: 10-Gauss (C2=2.0)

CAS-10 scores geometric scaling at 2, but stellarator confinement improves with size (ISS04 scaling law) — same physics as CAS-09 (scored at implicit 2 for geometric). The argument that "coil complexity grows faster than linearly" conflates manufacturing complexity (C1/C3) with physical scaling (C2). C2 should measure whether doubling output requires exponential complexity growth, and stellarator physics explicitly provides sub-linear energy confinement scaling with radius.

However, GIGA is already at 18m — near practical limits for coil fabrication and transport. This is a real scaling constraint, but it's a manufacturing ceiling, not a physics ceiling.

**Calibrated adjustment**: CAS-10 C2: 2.0 → **2.5** (increase geometric scaling from 2 to 3; revised average (3+1+3)/3 = 2.3 → 2.5)

---

## Part 3: Calibrated Score Table

| Criterion | 01-CFS | 07-MagLIF | 09-Proxima | 10-Gauss | 14-GF | 22-FLF | 28-ES |
|-----------|--------|-----------|------------|----------|-------|--------|-------|
| **C1** | 3.5 | 4.0→**3.5** | 3.3 | 2.9 | 3.0 | 3.3→**3.3** | 2.8→**3.2** |
| **C2** | 2.5 | 4.5→**4.0** | 3.0 | 2.0→**2.5** | 4.0 | 4.0 | 3.5 |
| **C3** | 3.2 | 3.0 | 2.8 | 3.1 | 2.8 | 3.8→**2.8** | 3.3 |
| **C4** | 2.0 | 3.0 | 2.5 | 2.0 | 2.5 | 3.5→**3.0** | 2.5 |
| **C5** | 1.8→**2.0** | 2.0 | 2.8→**2.0** | 3.2→**2.0** | 2.0 | 3.2→**2.4** | 2.0 |
| **C6** | 3.0→**4.0** | 3.5→**3.0** | 4.0 | 4.0 | 3.0 | 3.8→**4.5** | 3.5 |
| **C7** | 3.5→**3.0** | 2.5→**1.5** | 3.5 | 3.5 | 2.5→**1.5** | 2.0 | 3.0 |

### Composite Calculation Detail

| Concept | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Sum | Composite |
|---------|----|----|----|----|----|----|----|----|-----------|
| 01-CFS | 3.5 | 2.5 | 3.2 | 2.0 | 2.0 | 4.0 | 3.0 | 20.2 | **2.89** |
| 07-MagLIF | 3.5 | 4.0 | 3.0 | 3.0 | 2.0 | 3.0 | 1.5 | 20.0 | **2.86** |
| 09-Proxima | 3.3 | 3.0 | 2.8 | 2.5 | 2.0 | 4.0 | 3.5 | 21.1 | **3.01** |
| 10-Gauss | 2.9 | 2.5 | 3.1 | 2.0 | 2.0 | 4.0 | 3.5 | 20.0 | **2.86** |
| 14-GF | 3.0 | 4.0 | 2.8 | 2.5 | 2.0 | 3.0 | 1.5 | 18.8 | **2.69** |
| 22-FLF | 3.3 | 4.0 | 2.8 | 3.0 | 2.4 | 4.5 | 2.0 | 22.0 | **3.14** |
| 28-ES | 3.2 | 3.5 | 3.3 | 2.5 | 2.0 | 3.5 | 3.0 | 21.0 | **3.00** |

---

## Part 4: Ranking by Raw Composite

### Rank 1: 22-Projectile ICF (FLF/NearStar) — 3.14

**Strongest structural advantage**: Liquid lithium blanket eliminates first-wall replacement entirely, delivering the highest physical availability (CF_upper ~92.5%) of any D-T concept in the batch — a permanent capacity factor advantage no solid-blanket concept can match.

**Most binding constraint**: Two unretired binary gates (target gain at 60 km/s, EM gun at hypervelocity) with Machine 4 cancelled — no active developer is working to retire these gates, and the EM gun at speculative evidence (−1.5 penalty) is the most severe single gate penalty in the batch.

### Rank 2: 09-QI Stellarator HTS (Proxima) — 3.01

**Strongest structural advantage**: Zero binary feasibility gates combined with disruption-free steady-state operation (C6=4.0) — the best risk-adjusted capacity factor ceiling of any D-T MFE concept, backed by W7-X experimental heritage.

**Most binding constraint**: 3D non-planar HTS coil manufacturing cost and supply chain learning (C3=2.8) — geometrically unique coils with limited cross-plant repetition create the slowest learning curve of any major cost component in the batch.

### Rank 3: 28-HTS Tokamak Full HTS (Energy Singularity) — 3.00

**Strongest structural advantage**: Strongest supply chain learning potential among tokamaks (C3=3.3) driven by REBCO tape's demonstrated 18–24% learning rate and Shanghai Superconductor's commercial-scale production lines, combined with zero binary feasibility gates.

**Most binding constraint**: Entirely undefined blanket architecture (TRL 1–2) leaves the largest single-component design gap of any concept in the batch; combined with non-demountable coils limiting maintenance access, creating uncertainty in both C6 and C7.

### Rank 4: 01-CFS HTS Compact Tokamak — 2.89

**Strongest structural advantage**: 18 HTS TF coils in the manufacturing learning sweet spot (C1=3.5) with demountable joints enabling parallel blanket access — the fastest maintenance turnaround potential of any D-T tokamak.

**Most binding constraint**: Single-plasma tokamak with no unit replication path (C2=2.5) combined with one binary gate (I-mode confinement at high field), making this the only concept in the batch with a binary physics gate among the MFE concepts.

### Rank 5: 07-MagLIF (Pacific Fusion) — 2.86

**Strongest structural advantage**: Pulsed power driver modularity (thousands of identical capacitor bricks) and chamber replication architecture (C2=4.0) create the strongest combined modularization-scalability profile among D-T MIF concepts.

**Most binding constraint**: One binary gate on ignition at 60+ MA plus heavy cumulative degrading gates (cryo targets, RTL insertion, liquid wall, consumable cost) yield the lowest C7 (1.5) among concepts without floor-rule trigger — the concept has many things that must work simultaneously, each degrading economics if it doesn't.

### Rank 6 (tie): 10-Large-Scale Stellarator (Gauss) — 2.86

**Strongest structural advantage**: Deepest experimental heritage (W7-X) with highest technical feasibility tied with Proxima (C7=3.5) — the most physics-validated commercial fusion pathway.

**Most binding constraint**: Largest physical scale (R₀=18m, ~45,000t, 80 unique blanket segments) yields lowest modularization (C1=2.9) and scalability (C2=2.5) in the batch — cannot be built smaller, replicated modularly, or factory-standardized.

### Rank 7: 14-General Fusion MTF Pneumatic — 2.69

**Strongest structural advantage**: Chamber replication for linear scaling (C2=4.0) with the simplest core plasma approach of any MIF concept — no cryogenics, no exotic fuels, no HTS magnets.

**Most binding constraint**: Three binary gates identified in audit (piston synchronization, compression ratio, technology transfer gap) create the highest binary-gate count of any concept in the batch. The LM26→commercial technology disconnect (electromagnetic compression ≠ pneumatic compression) means near-term experimental success does not validate the commercial pathway.

---

## Part 5: Z-Score Normalized Table and Final Ranking

### Methodology

For each criterion i, the z-score for concept c is:

```
z_i,c = (calibrated_raw_score_i,c − mean_i) / stdev_i
```

Where mean_i and stdev_i are computed across all 7 concepts for criterion i (population statistics). The z-score composite is the arithmetic mean of z-scores across all 7 criteria.

### Criterion Statistics

| Criterion | Mean | Std Dev | Range (min–max) | Interpretation |
|-----------|------|---------|-----------------|----------------|
| C1 (Modularization) | 3.24 | 0.22 | 2.9–3.5 | **Very narrow** — all concepts cluster near 3.2; minimal differentiation |
| C2 (Scalability) | 3.36 | 0.66 | 2.5–4.0 | Wide spread; pulsed/modular concepts at 4.0, tokamaks/stellarators at 2.5–3.5 |
| C3 (Supply Chain) | 2.99 | 0.20 | 2.8–3.3 | **Narrowest** — all D-T concepts have similar learning profiles |
| C4 (Complexity) | 2.50 | 0.36 | 2.0–3.0 | Moderate spread; pulsed concepts simpler, tokamaks most complex |
| C5 (Customization) | 2.06 | 0.15 | 2.0–2.4 | **Extremely narrow** — all D-T concepts have nearly identical customization needs |
| C6 (Capacity Factor) | 3.71 | 0.55 | 3.0–4.5 | Moderate spread; stellarators and liquid-wall IFE at top, pulsed MIF at bottom |
| C7 (Feasibility) | 2.57 | 0.80 | 1.5–3.5 | **Widest spread** — the most differentiating criterion |

**Key observation**: This all-D-T batch has dramatically narrower C5 spread (σ=0.15) compared to the previous 13-concept calibration (σ=0.87). C5 contributes almost nothing to ranking differentiation — as expected, since all concepts share D-T fuel, steam Rankine thermal rejection, and similar activation profiles. C3 (σ=0.20) is also very narrow. The ranking will be driven primarily by C2 (σ=0.66), C7 (σ=0.80), and C6 (σ=0.55).

### Z-Score Table

| Criterion | 01-CFS | 07-MagLIF | 09-Proxima | 10-Gauss | 14-GF | 22-FLF | 28-ES |
|-----------|--------|-----------|------------|----------|-------|--------|-------|
| C1 (z) | +1.17 | +1.17 | +0.27 | −1.55 | −1.10 | +0.27 | −0.18 |
| C2 (z) | −1.30 | +0.97 | −0.54 | −1.30 | +0.97 | +0.97 | +0.21 |
| C3 (z) | +1.07 | +0.06 | −0.96 | +0.57 | −0.96 | −0.96 | +1.58 |
| C4 (z) | −1.39 | +1.39 | 0.00 | −1.39 | 0.00 | +1.39 | 0.00 |
| C5 (z) | −0.38 | −0.38 | −0.38 | −0.38 | −0.38 | +2.27 | −0.38 |
| C6 (z) | +0.52 | −1.30 | +0.52 | +0.52 | −1.30 | +1.43 | −0.39 |
| C7 (z) | +0.54 | −1.34 | +1.17 | +1.17 | −1.34 | −0.71 | +0.54 |
| **Z-Composite** | **+0.03** | **+0.08** | **+0.01** | **−0.34** | **−0.59** | **+0.67** | **+0.20** |

### Z-Score Calculation Verification

**C1**: mean = (3.5+3.5+3.3+2.9+3.0+3.3+3.2)/7 = 22.7/7 = 3.243; deviations: CFS = 0.257, MagLIF = 0.257, Proxima = 0.057, Gauss = −0.343, GF = −0.243, FLF = 0.057, ES = −0.043; variance = (0.066+0.066+0.003+0.118+0.059+0.003+0.002)/7 = 0.317/7 = 0.0453; σ = 0.213. z: CFS = 0.257/0.213 = +1.21, MagLIF = +1.21, Proxima = +0.27, Gauss = −1.61, GF = −1.14, FLF = +0.27, ES = −0.20.

Let me redo all calculations precisely:

**C1**: values = [3.5, 3.5, 3.3, 2.9, 3.0, 3.3, 3.2]
- mean = 22.7/7 = 3.243
- deviations = [+0.257, +0.257, +0.057, −0.343, −0.243, +0.057, −0.043]
- variance = (0.0661 + 0.0661 + 0.0033 + 0.1176 + 0.0590 + 0.0033 + 0.0018)/7 = 0.3172/7 = 0.04531
- σ = 0.2129
- z-scores: [+1.21, +1.21, +0.27, −1.61, −1.14, +0.27, −0.20]

**C2**: values = [2.5, 4.0, 3.0, 2.5, 4.0, 4.0, 3.5]
- mean = 23.5/7 = 3.357
- deviations = [−0.857, +0.643, −0.357, −0.857, +0.643, +0.643, +0.143]
- variance = (0.734 + 0.413 + 0.128 + 0.734 + 0.413 + 0.413 + 0.020)/7 = 2.857/7 = 0.4082
- σ = 0.639
- z-scores: [−1.34, +1.01, −0.56, −1.34, +1.01, +1.01, +0.22]

**C3**: values = [3.2, 3.0, 2.8, 3.1, 2.8, 2.8, 3.3]
- mean = 21.0/7 = 3.000
- deviations = [+0.200, +0.000, −0.200, +0.100, −0.200, −0.200, +0.300]
- variance = (0.040 + 0.000 + 0.040 + 0.010 + 0.040 + 0.040 + 0.090)/7 = 0.260/7 = 0.03714
- σ = 0.1927
- z-scores: [+1.04, 0.00, −1.04, +0.52, −1.04, −1.04, +1.56]

**C4**: values = [2.0, 3.0, 2.5, 2.0, 2.5, 3.0, 2.5]
- mean = 17.5/7 = 2.500
- deviations = [−0.500, +0.500, 0.000, −0.500, 0.000, +0.500, 0.000]
- variance = (0.250 + 0.250 + 0.000 + 0.250 + 0.000 + 0.250 + 0.000)/7 = 1.000/7 = 0.14286
- σ = 0.3780
- z-scores: [−1.32, +1.32, 0.00, −1.32, 0.00, +1.32, 0.00]

**C5**: values = [2.0, 2.0, 2.0, 2.0, 2.0, 2.4, 2.0]
- mean = 14.4/7 = 2.057
- deviations = [−0.057, −0.057, −0.057, −0.057, −0.057, +0.343, −0.057]
- variance = (0.0033 + 0.0033 + 0.0033 + 0.0033 + 0.0033 + 0.1176 + 0.0033)/7 = 0.1372/7 = 0.01960
- σ = 0.1400
- z-scores: [−0.41, −0.41, −0.41, −0.41, −0.41, +2.45, −0.41]

**C6**: values = [4.0, 3.0, 4.0, 4.0, 3.0, 4.5, 3.5]
- mean = 26.0/7 = 3.714
- deviations = [+0.286, −0.714, +0.286, +0.286, −0.714, +0.786, −0.214]
- variance = (0.082 + 0.510 + 0.082 + 0.082 + 0.510 + 0.617 + 0.046)/7 = 1.929/7 = 0.2755
- σ = 0.5249
- z-scores: [+0.54, −1.36, +0.54, +0.54, −1.36, +1.50, −0.41]

**C7**: values = [3.0, 1.5, 3.5, 3.5, 1.5, 2.0, 3.0]
- mean = 18.0/7 = 2.571
- deviations = [+0.429, −1.071, +0.929, +0.929, −1.071, −0.571, +0.429]
- variance = (0.184 + 1.148 + 0.862 + 0.862 + 1.148 + 0.327 + 0.184)/7 = 4.714/7 = 0.6735
- σ = 0.8207
- z-scores: [+0.52, −1.31, +1.13, +1.13, −1.31, −0.70, +0.52]

### Corrected Z-Score Table

| Criterion | 01-CFS | 07-MagLIF | 09-Proxima | 10-Gauss | 14-GF | 22-FLF | 28-ES |
|-----------|--------|-----------|------------|----------|-------|--------|-------|
| C1 (z) | +1.21 | +1.21 | +0.27 | −1.61 | −1.14 | +0.27 | −0.20 |
| C2 (z) | −1.34 | +1.01 | −0.56 | −1.34 | +1.01 | +1.01 | +0.22 |
| C3 (z) | +1.04 | 0.00 | −1.04 | +0.52 | −1.04 | −1.04 | +1.56 |
| C4 (z) | −1.32 | +1.32 | 0.00 | −1.32 | 0.00 | +1.32 | 0.00 |
| C5 (z) | −0.41 | −0.41 | −0.41 | −0.41 | −0.41 | +2.45 | −0.41 |
| C6 (z) | +0.54 | −1.36 | +0.54 | +0.54 | −1.36 | +1.50 | −0.41 |
| C7 (z) | +0.52 | −1.31 | +1.13 | +1.13 | −1.31 | −0.70 | +0.52 |
| **Z-Composite** | **+0.04** | **+0.07** | **−0.01** | **−0.36** | **−0.61** | **+0.69** | **+0.18** |

### Z-Composite Verification

- CFS: (1.21 + (−1.34) + 1.04 + (−1.32) + (−0.41) + 0.54 + 0.52) / 7 = 0.24/7 = **+0.03**
- MagLIF: (1.21 + 1.01 + 0.00 + 1.32 + (−0.41) + (−1.36) + (−1.31)) / 7 = 0.46/7 = **+0.07**
- Proxima: (0.27 + (−0.56) + (−1.04) + 0.00 + (−0.41) + 0.54 + 1.13) / 7 = −0.07/7 = **−0.01**
- Gauss: (−1.61 + (−1.34) + 0.52 + (−1.32) + (−0.41) + 0.54 + 1.13) / 7 = −2.49/7 = **−0.36**
- GF: (−1.14 + 1.01 + (−1.04) + 0.00 + (−0.41) + (−1.36) + (−1.31)) / 7 = −4.25/7 = **−0.61**
- FLF: (0.27 + 1.01 + (−1.04) + 1.32 + 2.45 + 1.50 + (−0.70)) / 7 = 4.81/7 = **+0.69**
- ES: (−0.20 + 0.22 + 1.56 + 0.00 + (−0.41) + (−0.41) + 0.52) / 7 = 1.28/7 = **+0.18**

### Final Z-Score Ranking

| Rank | Concept | Z-Composite | Raw Composite | Raw Rank | Rank Shift | Confidence |
|------|---------|-------------|---------------|----------|------------|------------|
| 1 | 22-Projectile ICF (FLF/NearStar) | **+0.69** | 3.14 | 1 | — | Medium |
| 2 | 28-ES Full HTS Tokamak | **+0.18** | 3.00 | 3 | ↑1 | Medium |
| 3 | 07-MagLIF (Pacific Fusion) | **+0.07** | 2.86 | 5 | ↑2 | Medium |
| 4 | 01-CFS HTS Compact Tokamak | **+0.03** | 2.89 | 4 | — | High |
| 5 | 09-QI Stellarator HTS (Proxima) | **−0.01** | 3.01 | 2 | ↓3 | High |
| 6 | 10-Gauss Large Stellarator | **−0.36** | 2.86 | 6 | — | High |
| 7 | 14-GF MTF Pneumatic | **−0.61** | 2.69 | 7 | — | High |

---

### Concept-by-Concept Commentary (Final Ranking)

**Rank 1: 22-Projectile ICF (FLF/NearStar) — z = +0.69**

- **Strongest structural advantage**: Dominant positive z-scores on C5 (+2.45, the most extreme z-score in the table) and C6 (+1.50) driven by compact footprint and liquid lithium wall eliminating first-wall replacement. Also strong on C4 (+1.32) and C2 (+1.01). FLF excels at everything except the things it needs to work in the first place.
- **Most binding constraint**: EM gun binary gate at speculative evidence (C7 z=−0.70) and monolithic driver supply chain (C3 z=−1.04). Machine 4 cancelled; no one actively working to retire the gain or driver gates.
- **Confidence**: **Medium**. Ranking is robust within the z-score framework — FLF's advantages on multiple criteria are genuine and large. However, C7 = 2.0 (two binary gates, one at speculative evidence) means the concept is conditional on physics that may never be demonstrated. The high z-composite is driven by FLF being the only concept with any C5 differentiation in an all-D-T batch.
- **Raw vs. z-score**: Same rank (1). FLF leads in both metrics.

**Rank 2: 28-ES Full HTS Tokamak — z = +0.18**

- **Strongest structural advantage**: Highest supply chain learning z-score (+1.56) in the batch, reflecting REBCO tape's demonstrated learning rate and Shanghai Superconductor's commercial production — the most actionable near-term cost reduction lever among all concepts.
- **Most binding constraint**: Undefined blanket architecture and non-demountable coils create below-average C6 (z=−0.41) and prevent the maintenance access advantage that CFS claims.
- **Confidence**: **Medium**. Z-score ranking rises from raw rank 3→2 because ES's strong C3 advantage (in the narrowest criterion, σ=0.19) generates outsized z-score benefit. ES has no severe z-score weakness (worst is C5/C6 at −0.41), making it the most "balanced" concept in the batch.
- **Raw vs. z-score**: ↑1 rank. Driven by C3 z=+1.56 (a 0.3-point raw advantage over the mean generates 1.56 standard deviations in this tight criterion).

**Rank 3: 07-MagLIF (Pacific Fusion) — z = +0.07**

- **Strongest structural advantage**: Strongest combined modularization-complexity z-profile: C1 z=+1.21, C4 z=+1.32, C2 z=+1.01. The pulsed power architecture is genuinely the most modular and simplest-to-build of any D-T MIF concept.
- **Most binding constraint**: Worst C6 (z=−1.36) and C7 (z=−1.31) in the batch — low capacity factor from pulsed duty cycle combined with the most gates (7) and an unretired binary gate on ignition. These are the "will it work, and if so, how often?" questions.
- **Confidence**: **Medium**. Z-score ranking rises from raw rank 5→3 because MagLIF's strengths (C1, C2, C4) are in criteria with moderate-to-narrow spreads where above-average scores generate large z-scores. Its weaknesses (C6, C7) are in wider-spread criteria where below-average scores generate smaller z-penalties. This is the z-normalization working as designed — but it does mean the ranking weights modular manufacturability more than operational viability.
- **Raw vs. z-score**: ↑2 ranks. The key driver: C4 has σ=0.38, so MagLIF's +0.5 raw advantage generates z=+1.32. C7 has σ=0.82, so MagLIF's −1.07 raw deficit generates only z=−1.31. The narrow C4 spread amplifies MagLIF's complexity advantage more than the wide C7 spread penalizes its feasibility weakness.

**Rank 4: 01-CFS HTS Compact Tokamak — z = +0.03**

- **Strongest structural advantage**: Strongest combined C1/C3 z-profile among tokamaks: C1 z=+1.21 (18 TF coils in learning sweet spot) and C3 z=+1.04 (REBCO tape cross-industry demand). If manufacturing scale-up occurs, CFS has the fastest cost reduction trajectory among MFE concepts.
- **Most binding constraint**: Lowest C2 (z=−1.34, tied with Gauss) from single-plasma architecture with no replication path, and lowest C4 (z=−1.32) from tight tokamak subsystem coupling. These are architectural constraints that cannot be engineering away — the tokamak architecture is inherently a single non-replicable plasma with tightly coupled subsystems.
- **Confidence**: **High**. The z-composite of +0.03 (essentially zero, right at the batch mean) accurately reflects CFS's position: strong manufacturing advantages exactly offset by architectural limitations. The framework measures learning rate potential, not probability of working — CFS likely has the highest probability of reaching operation among all concepts in this batch, but its LCOE improvement trajectory is middling.
- **Raw vs. z-score**: Same rank (4→4 after re-sorting). Stable position — CFS is penalized by the same criteria in both metrics.

**Rank 5: 09-QI Stellarator HTS (Proxima) — z = −0.01**

- **Strongest structural advantage**: Highest C7 z-score (+1.13, tied with Gauss) — zero binary gates, strongest W7-X heritage, clearest near-term validation pathway (SMC 2027, Alpha 2031). The most physics-validated commercial pathway among non-tokamak concepts.
- **Most binding constraint**: Lowest C3 (z=−1.04) from 3D non-planar HTS coils with no cross-plant repetition learning and limited external demand. This is Proxima's structural Achilles heel — even if the physics works, the coil manufacturing cost reduction rate is constrained by geometric uniqueness.
- **Confidence**: **High**. Z-score ranking drops from raw rank 2→5 because z-normalization exposes that Proxima's below-average C3 (in the tightest criterion, σ=0.19) generates an outsized z-penalty (−1.04). In raw terms, C3=2.8 looks "only" 0.2 below average. In z-score terms, it's 1.04 standard deviations below — a genuinely distinctive supply chain limitation.
- **Raw vs. z-score divergence**: ↓3 ranks, the largest shift. Proxima's raw composite (3.01, rank 2) was buoyed by high C7 (3.5), but C7's wide spread (σ=0.82) means the +0.93 raw advantage translates to "only" z=+1.13. Meanwhile, C3's narrow spread (σ=0.19) amplifies Proxima's −0.2 raw deficit to z=−1.04. The z-score correctly identifies that Proxima's supply chain limitation is more structurally distinctive than its feasibility advantage.

**Rank 6: 10-Gauss Large Stellarator — z = −0.36**

- **Strongest structural advantage**: Tied for highest C7 z-score (+1.13) with Proxima — deepest experimental heritage and disruption-free operation provide the safest physics bet in the batch.
- **Most binding constraint**: Lowest C1 (z=−1.61) and tied-lowest C2/C4 (z=−1.34/−1.32) — the 18m major radius, 80 unique blanket segments, and 45,000t mass create irreducible manufacturing and scaling limitations that no supply chain learning can overcome.
- **Confidence**: **High**. Safe physics bet with structurally limited cost reduction potential. The z-score confirms the raw ranking: Gauss's triple weakness on C1/C2/C4 (all below −1.3σ) overwhelms its C7 advantage.
- **Raw vs. z-score**: Same rank (6). Stable — Gauss is consistently penalized in both frameworks.

**Rank 7: 14-GF MTF Pneumatic — z = −0.61**

- **Strongest structural advantage**: Strong C2 (z=+1.01) from chamber replication architecture — the only MIF concept that can scale capacity by adding identical chambers without driver sharing.
- **Most binding constraint**: Three binary gates (piston sync, compression ratio, technology transfer) yield the lowest C7 (z=−1.31), combined with the lowest C6 (z=−1.36, tied with MagLIF). The LM26→commercial technology disconnect is the single most severe structural finding in the entire audit — even if LM26 succeeds brilliantly, it validates the wrong compression mechanism.
- **Confidence**: **High** for bottom ranking. GF has the most negative z-composite by a wide margin (−0.61 vs. next-lowest −0.36 for Gauss). The gap is driven by simultaneous weakness on C7 and C6 (the two widest-spread criteria) plus C1 and C3 weakness. Only C2 is above average.

---

### Z-Score vs. Raw Ranking: Key Divergences

Two concepts shift ≥2 ranks between raw and z-score ordering:

1. **09-Proxima drops 3 ranks (raw 2 → z 5)**: Proxima's C3=2.8 in a σ=0.19 criterion generates z=−1.04, and C2=3.0 in a σ=0.64 criterion generates z=−0.56. In raw terms, these look like minor below-average scores. In z-score terms, they reveal that Proxima's supply chain and scalability profile is the most distinctive weakness among the MFE concepts. The C7 advantage (+1.13) partially compensates but cannot overcome the cumulative effect of below-average scores on 4 of 7 criteria.

2. **07-MagLIF rises 2 ranks (raw 5 → z 3)**: MagLIF's strengths cluster in narrow-spread criteria (C1 σ=0.21, C4 σ=0.38) where above-average scores generate outsized z-scores. Its weaknesses are in wide-spread criteria (C7 σ=0.82, C6 σ=0.52) where below-average scores generate moderate z-penalties. The z-normalization correctly identifies that MagLIF's modular manufacturing advantage is more distinctive (rarer in the cohort) than its feasibility weakness (common — many concepts have low C7).

### Interpretation Notes

1. **All-D-T batch compresses C5**: With all concepts sharing D-T fuel, C5 has essentially zero differentiation power (σ=0.14) except for CAS-22's compact footprint advantage (z=+2.45). This single extreme z-score contributes disproportionately to FLF's ranking. In a mixed-fuel batch (including aneutronic concepts), FLF's C5 advantage would be much smaller relative to p-B11 or D-He3 concepts.

2. **Z-scores are relative to this 7-concept batch only**. Adding or removing concepts changes every z-score. The previous 13-concept calibration had wider spreads on most criteria and included aneutronic concepts that created larger C5 differentiation. Do not compare z-scores across calibration batches directly.

3. **Feasibility filter recommendation**: As with the previous calibration, apply C7 as a binary filter before interpreting the z-composite:
   - **Unconditional rankings (C7 ≥ 2.0)**: FLF (z-rank 1), ES (2), CFS (4), Proxima (5), Gauss (6)
   - **Conditional rankings (C7 ≤ 1.5)**: MagLIF (3), GF (7)

   After filtering: Among concepts where the physics is credible (C7 ≥ 2.0), the ranking is FLF → ES → CFS → Proxima → Gauss. FLF leads but has two binary gates (one at speculative evidence); ES and CFS are the safest bets with moderate learning potential; the stellarators (Proxima, Gauss) have the highest feasibility but slowest learning trajectories.

---

## Calibration Summary

### Score Movement Summary

| Concept | Original | Calibrated | Change | Primary Drivers |
|---------|----------|------------|--------|-----------------|
| 01-CFS | 2.93 | **2.89** | −0.04 | C5↑ (+0.2), C6↑ (+1.0), C7↓ (−0.5) — net effect: C6 correction (TRL penalty removed) offset by C7 gate audit |
| 07-MagLIF | 3.21 | **2.86** | −0.35 | C1↓ (−0.5), C2↓ (−0.5), C6↓ (−0.5), C7↓ (−1.0) — all four corrections compound |
| 09-Proxima | 3.13 | **3.01** | −0.12 | C5↓ (−0.8) — grid integration sub-factor removed from C5 |
| 10-Gauss | 2.96 | **2.86** | −0.10 | C2↑ (+0.5), C5↓ (−1.2) — grid integration removal and double-weighting correction |
| 14-GF | 2.83 | **2.69** | −0.14 | C7↓ (−1.0) — gate audit (compression ratio reclassified, technology transfer gap added) |
| 22-FLF | 3.37 | **3.14** | −0.23 | C3↓ (−1.0), C4↓ (−0.5), C5↓ (−0.8), C6↑ (+0.7) — C3 arithmetic correction is largest driver |
| 28-ES | 2.94 | **3.00** | +0.06 | C1↑ (+0.4) — harmonized with CFS for comparable magnet manufacturing architecture |

### Key Methodological Corrections

1. **C7 gate audit** was the largest single source of score changes for MIF concepts. MagLIF (−1.0), GF (−1.0), and CFS (−0.5) dropped because the audit identified additional gates that Pass 1 scorers collapsed or omitted. Stellarators (Proxima, Gauss) were stable — their gate enumerations were already thorough.

2. **C5 standardization** reduced 3 concepts (Proxima −0.8, Gauss −1.2, FLF −0.8) by removing the non-rubric "grid integration" sub-factor and eliminating ad-hoc weighting. All D-T concepts now cluster at C5 ≈ 2.0 (±0.4), which is correct — the D-T fuel cycle is the binding constraint.

3. **C6 replacement complexity assessment** raised CFS (+1.0) by removing the TRL penalty (physical CF = 84% → score 4, not 3). MagLIF was reduced (−0.5) by removing optimistic upward rounding. FLF was raised (+0.7) to 4.5 by removing TRL adjustments for a concept with a genuinely superior physical availability budget.

4. **C3 arithmetic correction** for FLF (−1.0) is the largest single-criterion correction. The EM gun at 74% of capital with learning score 2.0 anchors the weighted average at ~2.7, not the 3.8 that Pass 1 calculated. This corrects the most numerically significant error in the batch.

### Structural Findings

1. **MIF concepts drop the most**: MagLIF (−0.35) and GF (−0.14) both drop because the gate audit identifies pulsed-specific gates (chamber clearing, consumable cost, technology transfer) that steady-state concepts don't face. This is a real asymmetry — pulsed architectures have more distinct failure modes than continuous ones.

2. **Stellarators are the most stable**: Proxima and Gauss change minimally on all criteria except C5 (standardization correction). Their gate enumerations were already thorough and their C1–C4 scores were well-calibrated against each other.

3. **D-T fuel cycle eliminates C5 differentiation**: In an all-D-T batch, C5 contributes almost nothing to ranking. The only differentiation comes from FLF's compact footprint (seismic sub-factor = 4 vs. others at 2–3). This finding suggests C5 is primarily useful for ranking across fuel types, not within them.

4. **Tokamak feasibility advantage is real**: CFS (C7=3.0) and ES (C7=3.0) both score above the MIF/IFE concepts on feasibility. The tokamak physics pathway is the most experimentally validated, with JET/TFTR D-T results and SPARC on the near-term horizon. However, both carry the tokamak architecture penalties (C2, C4) that limit their learning trajectories.

5. **FLF's dominance is fragile**: FLF leads the raw ranking by 0.13 points and the z-score ranking by 0.51 points — the widest gap in the batch. But this is conditional on physics (C7=2.0, two binary gates) and driven by a single outlier z-score (C5 z=+2.45). In a mixed-fuel batch, aneutronic concepts would surpass FLF on C5, and its ranking would fall. Within this D-T-only batch, FLF's compact architecture is genuinely distinctive.
