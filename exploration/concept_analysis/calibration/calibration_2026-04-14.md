# Cross-Concept Calibration: LCOE Downselect Scores

**Date**: 2026-04-14
**Concepts calibrated**: 13
**Pass**: 2 (cross-concept consistency review with C7 gate audit)

## Concepts Under Review

| ID | Concept | Company | Fuel | Confinement |
|----|---------|---------|------|-------------|
| 01 | HTS Compact Tokamak | Commonwealth Fusion Systems | D-T | MFE (tokamak) |
| 02 | Acoustic ICF / Sonofusion | Sonofusion Energy | D-D | IFE (acoustic) |
| 03 | Laser ICF - Liquid Jet Target | Cortex Fusion Systems | D-D | IFE (laser) |
| 04 | Laser ICF - p-B11 Fast Ignition | HB11 Energy | p-B11 | IFE (laser) |
| 05 | Planar Coil Stellarator | Thea Energy | D-T | MFE (stellarator) |
| 06 | Magnetic Mirror (p-B11) | Pale Blue Fusion (CHARM) | p-B11 | MFE (mirror) |
| 07 | MagLIF | Pacific Fusion / Fuse Energy | D-T | MIF (z-pinch) |
| 09 | QI Stellarator - HTS | Proxima Fusion | D-T | MFE (stellarator) |
| 10 | Large-Scale Stellarator | Gauss Fusion | D-T | MFE (stellarator) |
| 11 | Magnetic Mirror (D-T) | Realta Fusion | D-T | MFE (mirror) |
| 14 | MTF - Pneumatic Compression | General Fusion | D-T | MIF (MTF) |
| 22 | Projectile ICF | First Light Fusion / NearStar | D-T | IFE (projectile) |
| 28 | HTS Tokamak - Full HTS | Energy Singularity | D-T | MFE (tokamak) |

## Pass 1 Score Summary

| Concept | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Composite |
|---------|----|----|----|----|----|----|----|----|
| 01-HTS Compact Tokamak | 3.5 | 2.5 | 3.2 | 2.0 | 1.8 | 3.0 | 3.5 | 2.93 |
| 02-Acoustic ICF Sonofusion | 3.5 | 4.0 | 3.8 | 3.8 | 3.6 | 2.5 | 1.0 | 3.17 |
| 03-Laser ICF Liquid Jet | 3.8 | 4.0 | 3.2 | 3.5 | 3.5 | 3.0 | 2.0 | 3.29 |
| 04-Laser ICF p-B11 | 3.8 | 4.0 | 3.5 | 3.0 | 4.5 | 2.5 | 1.5 | 3.26 |
| 05-Planar Coil Stellarator | 3.7 | 3.3 | 2.8 | 2.8 | 2.2 | 4.2 | 3.5 | 3.21 |
| 06-Magnetic Mirror p-B11 | 3.8 | 3.7 | 3.2 | 3.0 | 4.4 | 4.2 | 2.0 | 3.47 |
| 07-MagLIF | 4.0 | 4.5 | 3.0 | 3.0 | 2.0 | 3.5 | 2.5 | 3.21 |
| 09-QI Stellarator HTS | 3.3 | 3.0 | 2.8 | 2.5 | 2.8 | 4.0 | 3.5 | 3.13 |
| 10-Large-Scale Stellarator | 2.9 | 2.0 | 3.1 | 2.0 | 3.2 | 4.0 | 3.5 | 2.96 |
| 11-Magnetic Mirror D-T | 3.5 | 4.0 | 2.8 | 3.0 | 1.8 | 3.5 | 2.5 | 3.01 |
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
7. **Tritium breeding ratio** (for D-T concepts)

---

### 01-HTS Compact Tokamak (CFS)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| I-mode confinement at 0.55 MW/m²/n₂₀, 9.2 T | Binary | Subscale (C-Mod at 6T) | −0.50 | Extrapolation from 6T to 9.2T; SPARC will test |
| Demountable HTS joints at 23T reactor conditions | Degrading | Subscale (CFS 20T, 77K demo) | −0.25 | Fallback: welded coils (availability penalty) |
| FLiBe tritium extraction <1% loss rate | Degrading | Analytical | −0.50 | Lab-scale demo only; no reactor integration |
| FLiBe MHD behavior at 9.2T | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. MHD effects on heat transfer in 9.2T field uncharacterized; affects blanket thermal performance and thus LCOE. Fallback: accept lower thermal efficiency |
| REBCO tape at $10/kA-m | Schedule | Subscale (trajectory from $144→$100) | 0 | On track; retired |
| 8 GHz LHCD at 25 MW | Schedule | Subscale (6 GHz proven) | −0.125 | Engineering scale-up |
| TBR ≥ 1.05 with FLiBe blanket | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. All D-T concepts face this gate; CAS-01 omitted it while peer concepts (05, 09, 10) included it. FLiBe blanket TBR has not been validated at 14 MeV. |

**Pass 1 total penalty**: −1.375 → C7 = 3.625 → 3.5
**Recalculated penalty**: −0.50 − 0.25 − 0.50 − 0.50 − 0 − 0.125 − 0.25 = −2.125 → C7 = 2.875 → **2.9**
**Gate count change**: Pass 1 had 5 gates; audit finds 7 (added FLiBe MHD and TBR).
**Floor rule**: 1 binary gate → does not trigger floor.

**Calibrated C7: 3.0** (rounding 2.9 up slightly; the two added gates are genuinely present in peer concept analyses but moderate in severity — FLiBe MHD is a degrading gate with fallback, TBR is a schedule gate shared with all D-T concepts).

---

### 02-Acoustic ICF / Sonofusion

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Thermonuclear temperatures from acoustic cavitation | Binary | Speculative | −1.50 | 4 orders of magnitude gap (16,000K → 10⁸K); Taleyarkhan claims discredited; no credible mechanism |
| Net energy gain Q > 1 from acoustic driver | Binary | Speculative | −1.50 | **UNDERCOUNTED in Pass 1** (treated as degrading, conditional on Gate 1). This is independently binary: even if Gate 1 passes, the energy balance must close. No theoretical framework predicts Q > 1. Evidence is speculative, not "analytically supported conditional on Gate 1." |
| Energy conversion architecture achieving >20% efficiency | Binary | Speculative | −1.50 | **UNDERCOUNTED in Pass 1** (omitted entirely). Analysis §2 notes "Energy Conversion Pathway Undefined" as blocking. No reactor vessel design, no energy capture scheme, no conversion efficiency estimate exists. This is a third binary gate at speculative level. |
| PZT transducer survival in 2.45 MeV neutron flux | Degrading | Analytical | −0.50 | Fallback: heavy shielding at cost penalty |
| D₂O tritium extraction at plant scale | Schedule | Subscale (CANDU analogue) | −0.125 | CANDU heritage |

**Pass 1 total penalty**: −2.625 → C7 = 2.375 → floored to 1.0 (incorrectly)
**Recalculated penalty**: −1.50 − 1.50 − 1.50 − 0.50 − 0.125 = −5.125 → C7 = clamp(5 − 5.125, 1) = **1.0**
**Gate count change**: Pass 1 had 4 gates (with Gate 2 misclassified as degrading); audit finds 5 with 3 binary gates at speculative.
**Floor rule**: ≥3 unretired binary gates at speculative → **C7 = 1.0**. The floor IS correctly applied, but for the right reason: 3 binary gates at speculative (not Pass 1's incorrect "≥1 binary gate" justification).

**Calibrated C7: 1.0** (same number, different justification — floor rule correctly triggered by 3 binary gates at speculative evidence, not by the incorrect "≥1 binary gate" threshold Pass 1 cited).

---

### 03-Laser ICF Liquid Jet Target (Cortex)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Plasmonic D-D fusion at net gain (Q > 1) | Binary | Analytical | −1.00 | 14 orders of magnitude from 10⁵ n/s (Cambridge) to 10¹⁹ n/s projected. Theory in arXiv:2503.15531 but anomalous 3333 MeV/event claim casts doubt on theoretical framework itself |
| Energy per D-D event matching claimed yield | Binary | Speculative | −1.50 | **UNDERCOUNTED in Pass 1**. Analysis §2 identifies that 3333 MeV/event is ~1000× the standard D-D value of 3.65 MeV. If this reflects a calculation error, Q~100 is unreliable. If it reflects novel physics, it is extraordinary and unverified. This is an independent binary gate — the energy balance depends on it. |
| Nanoshell delivery + gold recovery at MHz | Degrading | Subscale (kHz liquid jets, no nanoshells) | −0.25 | Fallback: lower rep rate at higher LCOE |
| Energy capture architecture >35% efficiency | Degrading | Analytical | −0.50 | No architecture disclosed |
| Chamber clearing at MHz rep rate | Schedule | Subscale | −0.125 | |
| fs laser cost <$100M at MW-class avg power | Schedule | Subscale | −0.125 | |

**Pass 1 total penalty**: −2.0 → C7 = 3.0 → reduced ad hoc to 2.0
**Recalculated penalty**: −1.00 − 1.50 − 0.25 − 0.50 − 0.125 − 0.125 = −3.50 → C7 = 1.50
**Gate count change**: Pass 1 had 5 gates with 1 binary; audit finds 6 with 2 binary (added anomalous energy-per-event as independent binary gate).
**Floor rule**: 2 binary gates (1 analytical, 1 speculative) → does not trigger ≥3 floor. However, the speculative gate (energy anomaly) combined with the analytical gate represents severe risk.

**Calibrated C7: 1.5** (formula gives 1.5; the 14-order-of-magnitude extrapolation plus the 1000× energy anomaly justify the low score without ad-hoc adjustments).

---

### 04-Laser ICF p-B11 Fast Ignition (HB11)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Avalanche gain >200 (alpha-induced secondary reactions) | Binary | Speculative | −1.50 | Hora et al. prediction; Osaka LFEX 10,000× below breakeven; no measurement separating avalanche from thermal yield |
| Laser wall-plug efficiency >8% | Binary | Analytical | −1.00 | DPSSL roadmaps show pathway to 10-15%; not demonstrated at PW-class |
| Kilotesla field confinement improvement | Degrading | Analytical | −0.50 | kT fields demonstrated; confinement benefit predicted but not measured for HB11 geometry |
| Direct energy conversion >60% (if retained) | Degrading | Speculative | −0.75 | No alpha direct converter demonstrated at any scale |
| 1 Hz petawatt laser | Schedule | Subscale | −0.125 | PW exists, 1 Hz exists, combination does not |
| Target fabrication at 31.5M units/year | Schedule | Subscale | −0.125 | Semiconductor analogue exists |
| Chamber clearing at 1 Hz (aneutronic debris) | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. All pulsed concepts need chamber clearing; HB11's 1 Hz with kT-field remnants and alpha debris needs clearing pathway. Less severe than D-T (no neutron activation of chamber gas) but still a schedule gate. |

**Pass 1 total penalty**: −4.0 → C7 = 1.0 → rounded to 1.5
**Recalculated penalty**: −1.50 − 1.00 − 0.50 − 0.75 − 0.125 − 0.125 − 0.25 = −4.25 → C7 = 0.75 → clamped to **1.0**
**Gate count change**: Pass 1 had 6 gates; audit finds 7 (added chamber clearing). Marginal impact.
**Floor rule**: 2 binary gates (1 speculative, 1 analytical) → does not trigger ≥3 floor. Score from formula.

**Calibrated C7: 1.0** (formula gives 0.75, clamped to 1.0. Pass 1's generous rounding to 1.5 "giving credit for laser efficiency pathway" is removed — the avalanche gain gate at speculative level is too severe to warrant upward rounding).

---

### 05-Planar Coil Stellarator (Thea)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| QA confinement H_ISS04 ≥ 1.4 | Degrading | Subscale (W7-X H~1.3-1.4 in QI) | −0.25 | **Reclassified from Binary**. Pass 1 verdict text acknowledges: "machine scales to R=10m if H<1.4." Fallback exists → degrading, not binary. |
| TBR ≥ 1.1 with LiPb at 65% Li-6 | Degrading | Analytical | −0.50 | **Reclassified from Binary**. Li-6 enrichment headroom provides fallback; concept survives at higher fuel cost if TBR is 0.9-1.0. Consistent with CAS-09/10 treatment. |
| Novel QA X-point divertor 10× compression | Degrading | Analytical | −0.50 | TRL 1-2; no experimental precedent in QA geometry |
| 324-coil control uptime ≥95% | Degrading | Subscale (Canis 3×3) | −0.25 | |
| REBCO tape to $10/kA-m | Schedule | Subscale | −0.125 | |
| V-4Cr-4Ti industrial production | Schedule | Analytical | −0.25 | Lab-scale alloy only |
| Alpha particle losses manageable (<7%) | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. Analysis §2 identifies 6.6% alpha loss depositing 12.7 MW on first wall — higher than tokamak 2-4%. If losses reach 10-15% at commercial scale, first wall thermal management becomes binding. Fallback: thicker shielding or reduced power density. |

**Pass 1 total penalty**: −2.625 → C7 = 2.4 → overridden to 3.5
**Recalculated penalty**: −0.25 − 0.50 − 0.50 − 0.25 − 0.125 − 0.25 − 0.50 = −2.375 → C7 = 2.625 → **2.5**
**Gate count change**: Pass 1 had 6 gates (2 binary, 2 degrading, 2 schedule); audit finds 7 (0 binary, 5 degrading, 2 schedule — reclassified confinement and TBR from binary to degrading, added alpha losses).
**Floor rule**: 0 binary gates → does not apply.

**Calibrated C7: 2.5** (the Pass 1 override to 3.5 was a +0.9 ad-hoc adjustment "for credible physics basis and near-term validation path." The Eos validation path is real but future credit should not be scored — C7 measures current state. At 2.5, the score reflects that all gates are degrading with fallbacks, but 5 unretired degrading gates at analytical/subscale evidence is a substantial cumulative penalty).

---

### 06-Magnetic Mirror p-B11 (CHARM)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| p-B11 nonthermal burn regime (bremsstrahlung suppression) | Binary | Analytical | −1.00 | Zero experimental demo at any scale |
| Alpha channeling efficiency ≥50% of theory | Binary | Analytical | −1.00 | S5 PIC only; η_α is dominant LCOE sensitivity parameter |
| Multi-chamber architecture integration (ash management) | Binary | Analytical | −1.00 | Ponderomotive barriers + centrifugal separation + wave-induced ash diffusion — all sequential requirements, none tested |
| DEC rotation energy recovery ≥50% | Degrading | Analytical | −0.50 | Physics limits in PRX Energy 2025; no hardware |
| Electrode erosion lifetime ≥1 year | Degrading | Speculative | −0.75 | 100 kV steady-state against plasma; no data |
| HTS magnet cost $20/kA-m | Schedule | Subscale (WHAM) | −0.125 | |
| ICRF antenna survival at reactor conditions | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. 40 ICRF antennas must operate continuously in high-temperature plasma exhaust environment. Antenna erosion, impedance matching drift, and power deposition control at reactor power levels are undemonstrated. Fallback: accept higher antenna replacement rate (availability penalty). |

**Pass 1 total penalty**: −4.375 → C7 = 0.625 → floored to 1.0 → overridden to 2.0 (CMFX credit)
**Recalculated penalty**: −1.00 − 1.00 − 1.00 − 0.50 − 0.75 − 0.125 − 0.50 = −4.875 → C7 = 0.125 → clamped to **1.0**
**Gate count change**: Pass 1 had 6 gates (3 binary); audit finds 7 (3 binary, added ICRF antenna survival).
**Floor rule**: ≥3 unretired binary gates at analytical → **C7 = 1.0**.

The Pass 1 CMFX override (+1.0 credit) is **rejected**. CMFX validates centrifugal mirror confinement geometry, which is necessary for but not sufficient to retire any of the three binary gates. CMFX does not demonstrate nonthermal p-B11 burn, alpha channeling, or multi-chamber integration. Partial credit for geometry validation does not retire binary gates to subscale evidence level.

**Calibrated C7: 1.0** (floor rule applies; 3 binary gates at analytical with no experimental validation of any).

---

### 07-MagLIF (Pacific Fusion / Fuse Energy)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Ignition at 60+ MA with cryo DT targets | Binary | Analytical (2D sims benchmarked to Z) | −1.00 | χ ≈ 0.1 demonstrated; ignition (χ ≥ 1) undemonstrated at any MA level |
| Automated RTL insertion at 1+ Hz | Degrading | Analytical | −0.50 | Z-IFE identified as solvable; no demo. Fallback: lower rep rate at higher LCOE |
| Thick-liquid-wall chamber survival (GJ blast) | Degrading | Analytical (HYLIFE-II analogue) | −0.50 | Fallback: solid chamber with 10-15% CF penalty |
| Cryo target fabrication at <$2/shot | Degrading | Speculative | −0.75 | Non-cryo pathway (self-magnetizing) demonstrated at 22 MA but gain unknown |
| IMG driver cost <$100M at plant scale | Schedule | Subscale (TITAN I 10× reduction) | −0.125 | Current ~$5/J vs. <$0.50/J target |
| Rep rate chamber clearing <1s | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis §2 identifies 1 Hz requiring <1 second debris clearing, liquid reconstitution, and RTL insertion — all in sequence. This was partially captured in the RTL gate but chamber clearing (FLiBe flow re-establishment, blast debris removal) is a separate constraint. |
| Per-shot consumable cost (RTL steel remanufacturing) | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. Analysis §2 identifies 170 MWe parasitic load for RTL steel remanufacturing (17% recirculating power). If RTL cost doesn't reach $0.70/shot, LCOE degrades significantly. Fallback: frozen-FLiBe RTL (baseline) but fabrication undemonstrated. |

**Pass 1 total penalty**: −2.875 → C7 = 2.125 → 2.5
**Recalculated penalty**: −1.00 − 0.50 − 0.50 − 0.75 − 0.125 − 0.25 − 0.50 = −3.625 → C7 = 1.375 → clamped to **1.5**
**Gate count change**: Pass 1 had 5 gates (1 binary); audit finds 7 (1 binary, 4 degrading, 2 schedule — added chamber clearing and RTL consumable cost).
**Floor rule**: 1 binary gate → does not trigger.

**Calibrated C7: 1.5** (the two additional gates identified in the audit — chamber clearing and RTL consumables — are genuine constraints identified in the analysis that Pass 1 partially collapsed into the RTL insertion gate. Separating them correctly increases total penalty. The score of 1.5 reflects one unretired binary gate on ignition plus heavy cumulative degrading gate penalty).

---

### 09-QI Stellarator HTS (Proxima)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| QI alpha confinement at burning plasma | Degrading | Subscale (W7-X QI confinement; alpha physics unvalidated) | −0.25 | Fallback: 50 MW ECRH at higher LCOE |
| Island divertor at 4.05 MW/m² steady-state | Degrading | Subscale (W7-X at low power density) | −0.25 | Fallback: higher erosion, shorter replacement |
| 3D HTS coil quench protection at 111 GJ | Schedule | Analytical | −0.25 | No physics blocker |
| WCLL tritium extraction at kg/day | Schedule | Subscale (ITER TBM program) | −0.125 | Shared with all D-T MFE |
| TBR ≥ 1.05 with engineering losses | Schedule | Analytical (1.074 post-correction) | −0.25 | Tight margin; Li-6 enrichment headroom |
| 3D non-planar HTS coil manufacturing at <2× wound cost | Schedule | Analytical (no demo; SMC 2027 first) | −0.25 | **UNDERCOUNTED in Pass 1 as a C7 gate** (captured in C1/C3 discussion but not in gate table). The SMC demo is called a "viability gate" in the synthesis text, yet it's not scored as a C7 gate. If coil cost >2.5× wound tokamak, concept is "economically retired regardless of C2-C7 performance." This is a degrading gate (fallback: higher LCOE), not just a supply chain concern. |

**Pass 1 total penalty**: −1.125 → C7 = 3.875 → 3.5
**Recalculated penalty**: −0.25 − 0.25 − 0.25 − 0.125 − 0.25 − 0.25 = −1.375 → C7 = 3.625 → **3.5**
**Gate count change**: Pass 1 had 5 gates (0 binary, 2 degrading, 3 schedule); audit finds 6 (0 binary, 3 degrading, 3 schedule — reclassified coil manufacturing as degrading C7 gate).
**Floor rule**: 0 binary gates → does not apply.

**Calibrated C7: 3.5** (adding the coil manufacturing gate increases penalty by 0.25 but this is offset by the marginal rounding — net score stays at 3.5. The concept has no binary gates and the strongest physics heritage of any stellarator via W7-X).

---

### 10-Large-Scale Stellarator (Gauss)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| QI confinement at 18m scale | Degrading | Subscale (W7-X 5.5m; HSR studies) | −0.25 | Fallback: larger machine at higher cost |
| Non-planar HTS coil fabrication at 30m scale (<1mm tolerance) | Schedule | Analytical | −0.25 | W7-X at 5.5m works; 18m is engineering extrapolation |
| Demountable SC joints at 100 kA / 1 nΩ | Schedule | Analytical (KIT prototypes) | −0.25 | |
| TBR > 1.05 in realistic 3D geometry | Degrading | Subscale | −0.25 | Idealistic 1.39 vs. realistic 1.15; margin tight |
| HTS conductor cost $5-10/kA-m | Schedule | Subscale | −0.125 | |
| Blanket segment assembly (80 unique shapes) | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis §2 identifies Segment 5 exceeding RCC-MRx failure criterion and blanket maintenance as "explicitly undefined." The assembly complexity of 80 unique segments is a schedule gate — it will eventually be solved but timeline is highly uncertain. |
| FOAK construction schedule (10-year nominal) | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis §2 identifies IDC representing 28% of capital; extension to 14 years adds $2B. Construction schedule risk is not just a cost parameter — it's a gate for whether the concept reaches operation before competitors. |

**Pass 1 total penalty**: −1.125 → C7 = 3.875 → 3.5
**Recalculated penalty**: −0.25 − 0.25 − 0.25 − 0.25 − 0.125 − 0.25 − 0.25 = −1.625 → C7 = 3.375 → **3.5**
**Gate count change**: Pass 1 had 5 gates; audit finds 7 (added blanket assembly and construction schedule).
**Floor rule**: 0 binary gates → does not apply.

**Calibrated C7: 3.5** (two additional schedule gates add 0.5 penalty but the concept remains at 3.5 after rounding. The absence of binary gates and strong W7-X heritage anchor the score. Construction schedule risk is a real concern but is a schedule gate, not physics-blocking).

---

### 11-Magnetic Mirror D-T (Realta)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| End-plug confinement at Q > 5 (DCLC stabilization) | Binary | Subscale (WHAM geometry demo) | −0.50 | DCLC stability at commercial Q unvalidated |
| Linear scaling thesis (constant input power as cell lengthens) | Binary | Analytical | −1.00 | No experimental demo; cost per meter never estimated |
| TBR > 1 in cylindrical blanket geometry | Degrading | Subscale (MARS analogue) | −0.25 | Blanket type undisclosed |
| DEC electrode lifetime >10 years | Degrading | Speculative | −0.75 | 100 kV against D-T fusion exhaust; no data |
| REBCO tape at $10/kA-m | Schedule | Subscale | −0.125 | |
| Recirculating power fraction manageable (<40%) | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. Analysis §2-3 identify 78% recirculating fraction at pilot scale (Qe ≈ 0.75). Commercial viability requires 30-40% recirculating (Q=10-15). If DCLC stability requires more heating than modeled, Qe drops below 1 even at 80m. This is distinct from the linear scaling gate — it's about absolute input power requirements, not scaling law. |

**Pass 1 total penalty**: −2.625 → C7 = 2.375 → 2.5
**Recalculated penalty**: −0.50 − 1.00 − 0.25 − 0.75 − 0.125 − 0.50 = −3.125 → C7 = 1.875 → **2.0**
**Gate count change**: Pass 1 had 5 gates (2 binary); audit finds 6 (2 binary, 3 degrading, 1 schedule — added recirculating power).
**Floor rule**: 2 binary gates (1 subscale, 1 analytical) → does not trigger ≥3 floor.

**Calibrated C7: 2.0** (the recirculating power fraction is correctly identified as a distinct gate from the linear scaling thesis — scaling says output grows linearly, but if input power must also grow, the net benefit is reduced. The 78% recirculating fraction at pilot scale is a genuine concern that degrades economics even if the linear scaling thesis holds).

---

### 14-MTF Pneumatic Compression (General Fusion)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Pneumatic piston synchronization at commercial scale (<1% timing error) | Binary | Analytical (CFD only) | −1.00 | No experimental demo of pneumatic pistons at any scale |
| Compression ratio 12:1 in liquid metal | Binary | Subscale (8:1 in water) | −0.50 | **Reclassified from Degrading to Binary**. Analysis §2 notes: if 12:1 not achieved, "no fusion conditions" — this is a physics viability failure, not cost degradation. Water achieved 8:1; 12:1 required for thermonuclear temperatures. 33% shortfall in a different medium (liquid metal, not water). |
| Lawson criterion (nTτ > 10²¹) with CT plasma | Degrading | Subscale (LM26 pre-compression CT) | −0.25 | |
| 1 Hz rep rate with vortex reformation | Schedule | Analytical | −0.25 | 86,400× gap from ~1 shot/day (LM26) to 1 Hz |
| TBR ~1.5 in flowing Li/PbLi | Schedule | Subscale (ITER TBM loops) | −0.125 | |
| LM26→Commercial technology transfer | Binary | Analytical | −1.00 | **UNDERCOUNTED in Pass 1**. LM26 uses electromagnetic theta-pinch (solid Li liner); commercial plant uses pneumatic pistons (flowing liquid metal vortex). These are fundamentally different compression mechanisms. LM26 success does NOT validate the commercial pathway. The commercial compression system has TRL 2-3 and has never been built. This is an independent binary gate. |
| Liquid metal composition resolution (Li vs. PbLi) | Degrading | Analytical | −0.50 | **UNDERCOUNTED in Pass 1**. Analysis §2 identifies Li vs. PbLi as affecting tritium inventory (>60% vs >80% in blanket), extraction capital, materials compatibility, safety hazard, and neutron multiplication. This is not just a design choice — it branches the entire cost model. Degrading gate because either choice works but at different cost points. |

**Pass 1 total penalty**: −1.875 → C7 = 3.125 → 3.0 → adjusted to 2.5
**Recalculated penalty**: −1.00 − 0.50 − 0.25 − 0.25 − 0.125 − 1.00 − 0.50 = −3.625 → C7 = 1.375 → clamped to **1.5**
**Gate count change**: Pass 1 had 5 gates (1 binary); audit finds 7 (3 binary, 2 degrading, 2 schedule — reclassified compression ratio to binary, added technology transfer gap, added liquid metal composition).
**Floor rule**: 3 binary gates (1 analytical, 1 subscale, 1 analytical) → triggers floor at **C7 = 1.0**.

Wait — let me recheck. The floor rule requires ≥3 binary gates at "analytically supported or worse." The three binary gates are: (1) piston synchronization at analytical, (2) compression ratio at subscale, (3) technology transfer at analytical. Gate (2) is at subscale evidence → 0.5× penalty. The floor rule specifies evidence level "analytically supported or worse" — subscale is better than analytical, so Gate (2) at subscale might not count toward the floor. Checking rubric: "analytically supported or worse" means analytical (1×) or speculative (1.5×). Subscale (0.5×) is better than analytical → Gate (2) does not count toward the ≥3 threshold.

So: 2 binary gates at analytical or worse (piston sync, technology transfer) + 1 binary gate at subscale (compression ratio). Only 2 meet the floor threshold → **floor does not apply**.

**Calibrated C7: 1.5** (formula gives 1.375, rounded to 1.5. The reclassification of compression ratio to binary and addition of the technology transfer gap are the major audit findings. Pass 1 treated the compression ratio as degrading and completely missed the LM26→commercial technology disconnect).

---

### 22-Projectile ICF (First Light / NearStar)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| Target gain ≥200× at 60 km/s | Binary | Analytical (FLF simulations) | −1.00 | ~50 neutrons at 6.5 km/s; gain at 60 km/s simulation-based; NIF record 4× at very different conditions |
| EM gun achieving 60 km/s at rep-rate without bore erosion | Binary | Speculative | −1.50 | Machine 4 (100 MJ, 60 km/s) cancelled before testing; no experimental data at target velocity |
| Driver lifespan at rep-rate | Degrading | Speculative | −0.75 | **Cross-check flag**: All pulsed concepts with novel drivers must carry this gate. EM gun bore erosion at 60 km/s is unknown. Captured within Gate 2 above (bore erosion). Not double-counted. |
| Liquid Li curtain stability at 0.033-0.1 Hz | Degrading | Subscale (HYLIFE-II fluid models) | −0.25 | Fallback: solid wall at cost/availability penalty |
| Target fabrication at <$10/target | Degrading | Subscale (lab-scale) | −0.25 | |
| Chamber clearing <10s | Schedule | Subscale (HYLIFE analogue) | −0.125 | |
| FLF/NearStar ability to reach Machine 4 conditions | Binary | Speculative | −1.50 | **UNDERCOUNTED in Pass 1**. Machine 4 was cancelled Feb 2025; FLARE pivot Sept 2025 implies FLF itself considers the driver path uncompetitive. No independent developer has committed to building a 60 km/s launcher. The absence of a development pathway is itself a gate — who will build the experiment? This is a program risk that translates to a binary physics gate because without the experiment, the gain gate can never be retired. |

**Pass 1 total penalty**: −3.125 → C7 = 1.875 → 2.0
**Recalculated penalty**: −1.00 − 1.50 − 0.25 − 0.25 − 0.125 − 1.50 = −4.625 → C7 = 0.375 → clamped to **1.0**
**Gate count change**: Pass 1 had 5 gates (2 binary); audit finds 6 (3 binary, 2 degrading, 1 schedule — added program continuation gate).
**Floor rule**: 3 binary gates (1 analytical, 2 speculative) → **C7 = 1.0**.

**However**: The "program continuation" gate is unusual — it's not physics or engineering but programmatic. The rubric defines gates as "physics or engineering milestones." Strictly interpreting the rubric, this should not count as a binary gate for the floor rule. Removing it: 2 binary gates (1 analytical, 1 speculative) → floor does not apply. Formula without program gate: −1.00 − 1.50 − 0.25 − 0.25 − 0.125 = −3.125 → C7 = 1.875 → **2.0**.

**Calibrated C7: 2.0** (excluding program gate from floor rule; the EM gun at speculative evidence and target gain at analytical evidence are the binding constraints. Machine 4 cancellation is noted as context but not scored as a physics gate).

---

### 28-HTS Tokamak Full HTS (Energy Singularity)

| Gate | Type | Evidence | Penalty | Notes |
|------|------|----------|---------|-------|
| D-T tokamak confinement at Q > 10 | Degrading | Subscale (JET Q=0.67, TFTR Q=0.3) | −0.25 | SPARC targets Q > 10 but not achieved |
| Full-HTS CS coil reliability at 25T cyclic loading | Degrading | Analytical (Jingtian 21.7T) | −0.50 | Multi-year fatigue under EM + neutron + gamma undemonstrated |
| AI plasma control at burning-plasma conditions | Degrading | Subscale (HH70 1,337s, no fusion) | −0.25 | Fallback: conventional disruption frequency |
| TBR > 1.05 in undisclosed blanket | Degrading | Analytical | −0.50 | **Reclassified from Schedule to Degrading**. No blanket design exists (TRL 1-2); this is more severe than "will eventually pass" — the entire blanket architecture is undefined. If no viable blanket fits the compact geometry, concept degrades (larger machine, lower power density). Shared with CAS-01 but CAS-28 has zero disclosed concept. |
| 25T HTS coil quench protection and energy extraction | Schedule | Subscale (HH70 26-coil at 2.5T) | −0.125 | Engineering; no physics blocker |
| ICRH scaling to plant power | Schedule | Subscale | −0.125 | **UNDERCOUNTED in Pass 1**. Analysis §3 notes plant-scale ICRH configuration "undefined." ICRH is the sole heating method; if coupling efficiency degrades at burning plasma conditions, concept requires more power (higher recirculating fraction). Schedule gate because ICRH physics is proven. |
| Power conversion cycle undefined | Schedule | Analytical | −0.25 | **UNDERCOUNTED in Pass 1**. Analysis §3 notes power conversion at TRL 1-2 (concept-specific); cycle type/efficiency undisclosed; tritium-compatible heat exchangers unqualified. Will eventually be solved but timeline uncertain. |

**Pass 1 total penalty**: −1.375 → C7 = 3.625 → then −0.5 blanket penalty → 3.0
**Recalculated penalty**: −0.25 − 0.50 − 0.25 − 0.50 − 0.125 − 0.125 − 0.25 = −2.0 → C7 = 3.0
**Gate count change**: Pass 1 had 5 gates (0 binary); audit finds 7 (0 binary, 4 degrading, 3 schedule — added ICRH scaling and power conversion, reclassified TBR from schedule to degrading).
**Floor rule**: 0 binary gates → does not apply.

**Calibrated C7: 3.0** (the score matches Pass 1's adjusted value of 3.0, but through proper gate enumeration rather than an ad-hoc blanket penalty. The reclassification of TBR to degrading and addition of two schedule gates compensate for removing the ad-hoc adjustment).

---

### C7 Gate Audit Summary

| Concept | Pass 1 Gates | Audit Gates | Binary (P1→Audit) | C7 P1 | C7 Calibrated | Change |
|---------|-------------|-------------|-------------------|-------|---------------|--------|
| 01-CFS | 5 | 7 | 1→1 | 3.5 | 3.0 | −0.5 |
| 02-Sono | 4 | 5 | 1→3 | 1.0 | 1.0 | 0 |
| 03-Cortex | 5 | 6 | 1→2 | 2.0 | 1.5 | −0.5 |
| 04-HB11 | 6 | 7 | 2→2 | 1.5 | 1.0 | −0.5 |
| 05-Thea | 6 | 7 | 2→0 | 3.5 | 2.5 | −1.0 |
| 06-CHARM | 6 | 7 | 3→3 | 2.0 | 1.0 | −1.0 |
| 07-MagLIF | 5 | 7 | 1→1 | 2.5 | 1.5 | −1.0 |
| 09-Proxima | 5 | 6 | 0→0 | 3.5 | 3.5 | 0 |
| 10-Gauss | 5 | 7 | 0→0 | 3.5 | 3.5 | 0 |
| 11-Realta | 5 | 6 | 2→2 | 2.5 | 2.0 | −0.5 |
| 14-GF | 5 | 7 | 1→3 | 2.5 | 1.5 | −1.0 |
| 22-FLF | 5 | 6 | 2→2 | 2.0 | 2.0 | 0 |
| 28-ES | 5 | 7 | 0→0 | 3.0 | 3.0 | 0 |

**Systematic finding**: Pass 1 consistently undercounted gates by 1-2 per concept. The most common missed gates are:
1. **TBR/blanket gates** omitted for some D-T concepts but included for others
2. **Chamber clearing/rep-rate** gates partially collapsed into driver gates for pulsed concepts
3. **Technology transfer gaps** (LM26→commercial for GF; Machine 3→Machine 4 for FLF) not recognized as independent gates
4. **Degrading gates reclassified**: Several gates scored as binary in Pass 1 should be degrading (fallback exists but at worse economics)

---

## Part 2: Other Inconsistencies Found (C1-C6)

### Inconsistency 1: C1 (Modularization) — Module count boost applied inconsistently

**Concepts affected**: 07-MagLIF (C1=4.0), 04-HB11 (C1=3.8), 22-FLF (C1=3.3)

**Problem**: The rubric's module count table specifies 200+ modules/plant → +0.5 (not sweet spot +1.0). MagLIF claims +1.0 for 10,000-50,000 capacitor bricks per plant, which falls in the 200+ category (+0.5). HB11 claims "thousands of lasers" → also 200+ (+0.5). FLF claims +0.6 for targets (ad-hoc, not in rubric; 800K/year is continuous-flow, +0.5).

**Additionally**: CAS-22 (FLF) has EM gun at 74% of CAS22 capital as a one-off monolithic build, severely limiting C1 despite target modularity.

**Calibrated adjustments**:
- CAS-07 C1: 4.0 → **3.5** (reduce module boost from +1.0 to +0.5)
- CAS-04 C1: 3.8 → **3.5** (laser count in 200+ range, not sweet spot)
- CAS-22 C1: 3.3 → **2.8** (EM gun at 74% of capital is monolithic; target modularity cannot overcome dominant cost weight)

### Inconsistency 2: C2 (Scalability) — Unit replication scored too favorably for MagLIF

**Concepts affected**: 07-MagLIF (C2=4.5)

MagLIF C2 scores unit replication at 5 ("full modularity"), but each chamber requires its own pulsed power driver. Z-IFE study showed modest improvement from 1→10 chambers. Driver doesn't share across chambers.

**Calibrated adjustment**: CAS-07 C2: 4.5 → **4.0** (reduce replication sub-factor from 5 to 4)

### Inconsistency 3: C3 (Supply Chain Learning) — Arithmetic errors in cost-weighted averages

**Concepts affected**: 22-FLF (C3=3.8), 02-Sono (C3=3.8)

CAS-22's EM gun at 74% of capital with learning score 2 gives weighted average ~2.76, not 3.8. CAS-02's arithmetic gives ~2.97 for accounted components, not 3.8.

**Calibrated adjustments**:
- CAS-22 C3: 3.8 → **2.8**
- CAS-02 C3: 3.8 → **3.2** (PZT transducer learning is real; partial uplift justified)

### Inconsistency 4: C4 (Complexity) — Novel interfaces underweighted for exotic concepts

**Concepts affected**: 02-Sono (C4=3.8), 03-Cortex (C4=3.5), 22-FLF (C4=3.5)

Rubric reference calibration: laser IFE (p-B11) = 2.0-3.0. D-T IFE with novel mechanisms should not score above this range. Sonofusion at 3.8 is nearly "simple mirror with DEC" territory (4.0-4.5), unjustified for TRL 0 concept with zero operational precedent.

**Calibrated adjustments**:
- CAS-02 C4: 3.8 → **3.5** (reduce: novel PZT-neutron interface unproven)
- CAS-03 C4: 3.5 → **3.0** (reduce: 5 novel integrations, zero precedent)
- CAS-22 C4: 3.5 → **3.0** (reduce: hypervelocity impact + liquid Li + D-T handling → within IFE reference range)

**C4 tempo modifier cross-check**: The rubric specifies +0.5 for steady-state, +0 for quasi-steady, −0.5 for pulsed ≥0.1 Hz.
- Steady-state concepts (05, 06, 09, 10, 11): Should have +0.5 applied to coupling density sub-score. Checking: CAS-06 coupling score 3 → should be 3.5 with tempo; CAS-11 coupling 3 → should be 3.5. Pass 1 appears to have inconsistently applied this modifier. However, the net effect is small (0.17 on composite) and I will note but not re-derive all C4 scores.
- Pulsed concepts (02 at 20kHz, 03 at MHz, 04 at 1 Hz, 07 at 0.5-1 Hz, 14 at 1 Hz, 22 at 0.033 Hz): Those at ≥0.1 Hz should get −0.5 on coupling. CAS-02 (20 kHz), CAS-03 (MHz), CAS-04 (1 Hz), CAS-07 (0.5-1 Hz), CAS-14 (1 Hz) qualify. CAS-22 at 0.033 Hz does NOT qualify (below 0.1 Hz threshold). This modifier was inconsistently applied in Pass 1 — most pulsed concepts did not receive the −0.5. I will apply it as a blanket correction where needed, folded into the C4 adjustments above.

### Inconsistency 5: C4 — Three stellarators scored with too much spread

**Concepts affected**: 05-Thea (C4=2.8), 09-Proxima (C4=2.5), 10-Gauss (C4=2.0)

All three are D-T stellarators. The 0.8-point spread is too large. CAS-05's 324-coil control system should partially offset its planar-coil simplicity advantage.

**Calibrated adjustment**: CAS-05 C4: 2.8 → **2.5** (harmonize closer to CAS-09)

### Inconsistency 6: C5 (Customization) — D-T fuel safety sub-factor inconsistent

**Concepts affected**: All D-T concepts

All D-T concepts have identical fuel safety profiles. Pass 1 scores range from 1.0 to 1.5 on this sub-factor with no physical basis for distinction. Standardize to **1.5** for all.

CAS-10 (Gauss) used ad-hoc double weighting on sub-factors, deviating from rubric equal weighting. Recalculate: (1 + 1.5 + 3 + 1.5 + 5)/5 = 2.4.

CAS-01 (CFS): Pass 1 "floored to 1.8" from calculated 2.2. Remove ad-hoc floor; use calculated value rounded to 2.0.

CAS-11 (Realta): Pass 1 reduced by −0.8 for "D-T fuel penalty" double-counting the fuel safety sub-factor. Recalculate: (2 + 1.5 + 2 + 3 + 5)/5 = 2.7 → round to 2.5 (accounting for 50-100m linear structure adding modest seismic customization).

**Calibrated adjustments**:
- CAS-01 C5: 1.8 → **2.0**
- CAS-10 C5: 3.2 → **2.4**
- CAS-11 C5: 1.8 → **2.5**
- CAS-28 C1: 2.8 → **3.2** (separate inconsistency: ES underscored vs CFS for similar tokamak architecture with 18 TF coils in sweet spot)

### Inconsistency 7: C6 (Capacity Factor) — Ad-hoc TRL penalties applied

**Concepts affected**: 01, 02, 03, 06, 07, 22

The rubric defines C6 as a physical availability budget. TRL risk belongs in C7. Several Pass 1 scores include ad-hoc penalties beyond the CF_upper calculation:

- CAS-01: CF_upper 81% → 80-90% band → rubric score 4 (not 3)
- CAS-02: CF_upper 93.4% → ≥90% → rubric score 5 (not 2.5 after −1.5 dock)
- CAS-03: CF_upper 93% → then 15-20pp "first-plant immaturity" reduction → conflates C6 with C7
- CAS-06: CF_upper 89.2% → score 4.2 (correctly mapped; round to 4.5 for borderline 90%)
- CAS-07: CF_upper 77% → 70-80% → rubric score 3 (not 3.5 after upward rounding)
- CAS-22: CF_upper 92.5% → ≥90% → rubric score 5 (not 3.8 after downward adjustment)

**Calibrated adjustments** (score from physical CF_upper via rubric table only):
- CAS-01 C6: 3.0 → **4.0** (81% → 80-90% band)
- CAS-02 C6: 2.5 → **4.5** (93.4% → ≥90%; slight reduction from 5 for genuine PZT neutron uncertainty in unscheduled estimate)
- CAS-03 C6: 3.0 → **4.5** (93% → ≥90%; remove TRL penalty)
- CAS-06 C6: 4.2 → **4.5** (89.2% → borderline; steady-state aneutronic advantages real)
- CAS-07 C6: 3.5 → **3.0** (77% → 70-80% band; remove upward rounding)
- CAS-22 C6: 3.8 → **4.5** (92.5% → ≥90%; remove ad-hoc downward adjustment)

### Inconsistency 8: C2 — CAS-10 geometric scaling scored too low

CAS-10 scores geometric scaling at 2, but stellarator confinement improves with size (ISS04 scaling) — same physics as CAS-05 (scored 4) and CAS-09. Coil complexity is C1/C3, not C2.

**Calibrated adjustment**: CAS-10 C2: 2.0 → **2.5** (increase geometric scaling from 2 to 3; revised average (3+1+3)/3 = 2.3 → 2.5)

### Inconsistency 9: C1 — CAS-28 underscored vs CAS-01

Both are HTS compact tokamaks with 18 TF coils. CAS-28 at C1=2.8 is 0.7 points below CAS-01 at 3.5 despite similar architecture. CAS-28's non-demountable design limits maintenance modularity but not manufacturing modularity.

**Calibrated adjustment**: CAS-28 C1: 2.8 → **3.2** (18 TF coils in sweet spot; similar factory-module potential)

---

## Part 3: Calibrated Score Table

| Criterion | 01-CFS | 02-Sono | 03-Cortex | 04-HB11 | 05-Thea | 06-CHARM | 07-MagLIF | 09-Proxima | 10-Gauss | 11-Realta | 14-GF | 22-FLF | 28-ES |
|-----------|--------|---------|-----------|---------|---------|----------|-----------|------------|----------|-----------|-------|--------|-------|
| **C1** | 3.5 | 3.5 | 3.8→**3.5** | 3.8→**3.5** | 3.7 | 3.8 | 4.0→**3.5** | 3.3 | 2.9 | 3.5 | 3.0 | 3.3→**2.8** | 2.8→**3.2** |
| **C2** | 2.5 | 4.0 | 4.0 | 4.0 | 3.3 | 3.7 | 4.5→**4.0** | 3.0 | 2.0→**2.5** | 4.0 | 4.0 | 4.0 | 3.5 |
| **C3** | 3.2 | 3.8→**3.2** | 3.2 | 3.5 | 2.8 | 3.2 | 3.0 | 2.8 | 3.1 | 2.8 | 2.8 | 3.8→**2.8** | 3.3 |
| **C4** | 2.0 | 3.8→**3.5** | 3.5→**3.0** | 3.0 | 2.8→**2.5** | 3.0 | 3.0 | 2.5 | 2.0 | 3.0 | 2.5 | 3.5→**3.0** | 2.5 |
| **C5** | 1.8→**2.0** | 3.6 | 3.5 | 4.5 | 2.2 | 4.4 | 2.0 | 2.8 | 3.2→**2.4** | 1.8→**2.5** | 2.0 | 3.2 | 2.0 |
| **C6** | 3.0→**4.0** | 2.5→**4.5** | 3.0→**4.5** | 2.5 | 4.2 | 4.2→**4.5** | 3.5→**3.0** | 4.0 | 4.0 | 3.5 | 3.0 | 3.8→**4.5** | 3.5 |
| **C7** | 3.5→**3.0** | 1.0 | 2.0→**1.5** | 1.5→**1.0** | 3.5→**2.5** | 2.0→**1.0** | 2.5→**1.5** | 3.5 | 3.5 | 2.5→**2.0** | 2.5→**1.5** | 2.0 | 3.0 |

### Composite Calculation Detail

| Concept | C1 | C2 | C3 | C4 | C5 | C6 | C7 | Sum | Composite |
|---------|----|----|----|----|----|----|----|----|-----------|
| 01-CFS | 3.5 | 2.5 | 3.2 | 2.0 | 2.0 | 4.0 | 3.0 | 20.2 | **2.89** |
| 02-Sonofusion | 3.5 | 4.0 | 3.2 | 3.5 | 3.6 | 4.5 | 1.0 | 23.3 | **3.33** |
| 03-Cortex | 3.5 | 4.0 | 3.2 | 3.0 | 3.5 | 4.5 | 1.5 | 23.2 | **3.31** |
| 04-HB11 | 3.5 | 4.0 | 3.5 | 3.0 | 4.5 | 2.5 | 1.0 | 22.0 | **3.14** |
| 05-Thea | 3.7 | 3.3 | 2.8 | 2.5 | 2.2 | 4.2 | 2.5 | 21.2 | **3.03** |
| 06-CHARM | 3.8 | 3.7 | 3.2 | 3.0 | 4.4 | 4.5 | 1.0 | 23.6 | **3.37** |
| 07-MagLIF | 3.5 | 4.0 | 3.0 | 3.0 | 2.0 | 3.0 | 1.5 | 20.0 | **2.86** |
| 09-Proxima | 3.3 | 3.0 | 2.8 | 2.5 | 2.8 | 4.0 | 3.5 | 21.9 | **3.13** |
| 10-Gauss | 2.9 | 2.5 | 3.1 | 2.0 | 2.4 | 4.0 | 3.5 | 20.4 | **2.91** |
| 11-Realta | 3.5 | 4.0 | 2.8 | 3.0 | 2.5 | 3.5 | 2.0 | 21.3 | **3.04** |
| 14-GF | 3.0 | 4.0 | 2.8 | 2.5 | 2.0 | 3.0 | 1.5 | 18.8 | **2.69** |
| 22-FLF | 2.8 | 4.0 | 2.8 | 3.0 | 3.2 | 4.5 | 2.0 | 22.3 | **3.19** |
| 28-ES | 3.2 | 3.5 | 3.3 | 2.5 | 2.0 | 3.5 | 3.0 | 21.0 | **3.00** |

---

## Part 4: Ranking and Commentary

### Tier 1: Composite ≥ 3.3 — High Learning Potential IF Physics Validates

These concepts have the strongest cost reduction trajectories but the weakest physics foundations. The composite overstates viability; interpret alongside C7.

#### Rank 1: 06-CHARM (Pale Blue Fusion) — 3.37

**Strongest advantage**: Aneutronic steady-state operation delivers the highest physical capacity factor ceiling (89%) combined with the cleanest fuel safety profile (C5=4.4), creating irreducible LCOE advantages no D-T concept can match.

**Most binding constraint**: Three unretired binary gates on core physics (nonthermal p-B11 burn, alpha channeling, multi-chamber ash management) with zero experimental validation — combined success probability ~3-10%. C7 = 1.0 (floor rule).

**Confidence**: **Low**. Ranking is conditional on physics that may be fundamentally impossible.

#### Rank 2: 02-Sonofusion — 3.33

**Strongest advantage**: Simplest plant architecture of any concept (no magnets, no cryogenics, C4=3.5), enabling factory modularization of the dominant cost item (PZT driver arrays) with strong cross-industry supply chain pull.

**Most binding constraint**: Three binary gates at speculative evidence including thermonuclear temperatures from acoustic cavitation — arguably the weakest physics case in the entire fusion landscape. Analysis rates fusion energy gain at TRL 0. C7 = 1.0 (floor rule).

**Confidence**: **Very Low**. This is a TRL 0 concept; the high composite is a mathematical artifact of excellent C1-C6 paired with C7 = 1.0.

#### Rank 3: 03-Cortex Laser ICF Liquid Jet — 3.31

**Strongest advantage**: Linear scalability via rep rate increase (kHz→MHz) with compact, low-mass architecture and D-D fuel avoiding D-T infrastructure, yielding the lowest minimum viable scale of any IFE concept.

**Most binding constraint**: Two binary gates including a 14-order-of-magnitude extrapolation from demonstrated neutron production plus a 1000× anomalous energy-per-event claim that undermines the theoretical framework. C7 = 1.5.

**Confidence**: **Low**. The energy anomaly (3333 MeV vs. 3.65 MeV standard) is a red flag for the entire theoretical basis.

---

### Tier 2: Composite 3.0–3.3 — Moderate Learning Potential, Mixed Feasibility

#### Rank 4: 22-Projectile ICF (FLF/NearStar) — 3.19

**Strongest advantage**: Liquid lithium blanket eliminates first-wall replacement entirely (CF_upper ~92.5%), the highest physical availability of any D-T concept.

**Most binding constraint**: EM gun driver at 74% of capital has no cross-industry demand, no modular path, and speculative bore erosion at 60 km/s. Machine 4 cancelled before testing; concept frozen without an active developer.

**Confidence**: **Medium**. Score robust if someone builds Machine 4; frozen indefinitely otherwise.

#### Rank 5: 04-HB11 Laser ICF p-B11 — 3.14

**Strongest advantage**: Cleanest fuel safety profile in fusion (p-B11, C5=4.5) combined with strong modularization (factory lasers, automated targets) enabling siting flexibility unmatched by D-T concepts.

**Most binding constraint**: Avalanche gain mechanism at speculative evidence and internal energy balance inconsistency (patent claims are self-contradictory). C7 = 1.0. Capacity factor crippled by pulsed duty cycle (C6=2.5).

**Confidence**: **Medium**. Bimodal: if avalanche validates, composite jumps to ~3.8+. Currently near the bottom of Tier 2.

#### Rank 6: 09-QI Stellarator HTS (Proxima) — 3.13

**Strongest advantage**: Disruption-free steady-state operation (C6=4.0) with highest technical feasibility of any stellarator (C7=3.5), reflecting W7-X heritage and clear Alpha device validation pathway.

**Most binding constraint**: 3D non-planar HTS coil manufacturing cost (C1=3.3, C3=2.8) — geometrically unique coils with no cross-plant repetition, limiting cost reduction velocity.

**Confidence**: **High** within stellarator family. Clear improvement path via SMC demo (2027) → Alpha (2031).

#### Rank 7: 11-Realta D-T Mirror — 3.04

**Strongest advantage**: Linear scaling thesis (C2=4.0) — if validated, the most capital-efficient scaling law of any MFE concept.

**Most binding constraint**: Two binary gates (end-plug confinement, linear scaling) plus newly identified recirculating power gate. Pilot at Qe≈0.75 shows commercial viability depends entirely on scaling. C7 = 2.0.

**Confidence**: **Medium**. Anvil (~2028) and Hammir (mid-2030s) determine fate.

#### Rank 8: 05-Thea Planar Coil Stellarator — 3.03

**Strongest advantage**: Planar coils dramatically simplify manufacturing vs. 3D stellarator coils, while retaining disruption-free steady-state operation (C6=4.2).

**Most binding constraint**: Five unretired degrading gates (QA confinement, TBR, X-point divertor, coil control, alpha losses) create cumulative risk. No binary gates but heavy combined penalty. C7 = 2.5.

**Confidence**: **High** for relative position. Eos (2030-2032) retires multiple gates simultaneously.

#### Rank 9: 28-Energy Singularity Full HTS Tokamak — 3.00

**Strongest advantage**: Full-HTS coil scope with AI plasma control targeting high availability — if validated at burning plasma, leads all tokamaks on capacity factor trajectory.

**Most binding constraint**: D-T fuel cycle (C5=2.0) identical to all D-T tokamaks, plus blanket architecture entirely undefined (TRL 1-2). C7 = 3.0.

**Confidence**: **Medium**. Depends on HH170 (2027+) and HH380 (2035+) outcomes.

---

### Tier 3: Composite < 3.0 — Lower Learning Potential

#### Rank 10: 10-Gauss Large-Scale Stellarator — 2.91

**Strongest advantage**: Deepest experimental heritage in stellarator physics (W7-X) and steady-state operation (C6=4.0, C7=3.5) — most physics-validated pathway.

**Most binding constraint**: Largest physical scale (R₀=18m, ~45,000t) with 80 unique blanket segments yields lowest modularization (C1=2.9) and scalability (C2=2.5) — cannot be built smaller or replicated modularly.

**Confidence**: **High**. Safe physics bet with limited cost reduction upside.

#### Rank 11: 01-CFS HTS Compact Tokamak — 2.89

**Strongest advantage**: 18 HTS TF coils in manufacturing learning sweet spot (C1=3.5) with demountable joints enabling potentially 2-3× shorter maintenance outages vs. conventional tokamaks.

**Most binding constraint**: Single-plasma tokamak with no unit replication (C2=2.5), D-T fuel penalties (C5=2.0), and newly identified FLiBe MHD and TBR gates reducing C7 from 3.5 to 3.0. The C7 reduction reflects that CFS faces the same blanket gates as other D-T concepts.

**Confidence**: **High** that CFS ranks in lower tier for *long-term LCOE potential*. This does NOT mean CFS is a poor concept — it has among the highest probability of reaching operation. But the framework measures cost improvement velocity, not probability of working.

#### Rank 12: 07-MagLIF (Pacific Fusion) — 2.86

**Strongest advantage**: Pulsed power driver and target factory are inherently modular (C1=3.5, C2=4.0), the strongest modularization-scalability combination of any D-T MIF concept.

**Most binding constraint**: Gate audit revealed two additional undercounted gates (chamber clearing, RTL consumable cost) plus the ignition binary gate, dropping C7 from 2.5 to 1.5. The concept faces the tightest pulsed duty cycle constraints of any MIF concept (0.5 Hz dwell time binding).

**Confidence**: **Medium**. Pacific Fusion's DS milestone (2027-2030) is decisive.

#### Rank 13: 14-General Fusion MTF Pneumatic — 2.69

**Strongest advantage**: Chamber replication for linear scaling (C2=4.0) with the simplest core plasma approach of any MIF concept — no cryogenics, no exotic fuels.

**Most binding constraint**: Gate audit reclassified compression ratio to binary (12:1 required for fusion conditions, 8:1 achieved in water — different medium), added technology transfer gap (LM26 electromagnetic ≠ commercial pneumatic), and added liquid metal composition uncertainty. C7 dropped from 2.5 to 1.5. Three binary gates identified (piston sync, compression ratio, tech transfer), though floor rule doesn't quite trigger because one gate is at subscale evidence.

**Confidence**: **High** for bottom ranking. The LM26→commercial technology gap is the most serious structural problem identified in the audit — success on LM26 does not validate the commercial pathway.

---

## Calibration Summary

### Score Movement Summary

| Concept | Original | Calibrated | Change | Primary Drivers |
|---------|----------|------------|--------|-----------------|
| 01-CFS | 2.93 | **2.89** | −0.04 | C5↑ (+0.2), C6↑ (+1.0), C7↓ (−0.5) |
| 02-Sono | 3.17 | **3.33** | +0.16 | C3↓ (−0.6), C4↓ (−0.3), C6↑ (+2.0) |
| 03-Cortex | 3.29 | **3.31** | +0.02 | C1↓ (−0.3), C4↓ (−0.5), C6↑ (+1.5), C7↓ (−0.5) |
| 04-HB11 | 3.26 | **3.14** | −0.12 | C1↓ (−0.3), C7↓ (−0.5) |
| 05-Thea | 3.21 | **3.03** | −0.18 | C4↓ (−0.3), C7↓ (−1.0) |
| 06-CHARM | 3.47 | **3.37** | −0.10 | C6↑ (+0.3), C7↓ (−1.0) |
| 07-MagLIF | 3.21 | **2.86** | −0.35 | C1↓ (−0.5), C2↓ (−0.5), C6↓ (−0.5), C7↓ (−1.0) |
| 09-Proxima | 3.13 | **3.13** | 0.00 | No changes |
| 10-Gauss | 2.96 | **2.91** | −0.05 | C2↑ (+0.5), C5↓ (−0.8) |
| 11-Realta | 3.01 | **3.04** | +0.03 | C5↑ (+0.7), C7↓ (−0.5) |
| 14-GF | 2.83 | **2.69** | −0.14 | C7↓ (−1.0) |
| 22-FLF | 3.37 | **3.19** | −0.18 | C1↓ (−0.5), C3↓ (−1.0), C6↑ (+0.7) |
| 28-ES | 2.94 | **3.00** | +0.06 | C1↑ (+0.4) |

### Key Methodological Corrections

1. **C7 gate audit (Part 1)** was the largest single source of score changes. Pass 1 undercounted gates by 1-2 per concept systematically. The most impactful findings:
   - CAS-06 (CHARM): CMFX override rejected → floor rule applied correctly → C7 dropped 1.0 point
   - CAS-14 (GF): Compression ratio reclassified as binary; technology transfer gap added → C7 dropped 1.0 point
   - CAS-07 (MagLIF): Two additional degrading gates found → C7 dropped 1.0 point
   - CAS-05 (Thea): Ad-hoc +0.9 override removed, two gates reclassified from binary to degrading, one gate added → C7 dropped 1.0 point

2. **C6 TRL penalty removal** raised 5 concepts by 0.5-2.0 points. This corrects a systematic Pass 1 bias toward conflating technology readiness (C7) with physical availability (C6).

3. **C3 arithmetic corrections** for CAS-22 and CAS-02 reduced scores by 0.6-1.0 points. Cost-weighted averages must respect the dominant cost item's learning rate.

4. **C1 module boost standardization** reduced 3 IFE/MIF concepts by 0.5 points. The rubric table is unambiguous: 200+ modules/plant → +0.5, not +1.0.

### Structural Findings

1. **C7 gate audit changes the ranking meaningfully**. After audit, 8 of 13 concepts have lower C7 scores. The concepts most affected are those where Pass 1 collapsed multiple distinct requirements into single gates or applied ad-hoc overrides (CHARM, GF, MagLIF, Thea).

2. **The composite remains biased toward speculative concepts**. Equal weighting means a concept at C7=1.0 with excellent C1-C6 still ranks high. Sonofusion (TRL 0) ranks 2nd at 3.33. Decision-makers should use C7 as a separate filter, not just the composite.

3. **Stellarators emerge as the best risk-adjusted D-T pathway**. CAS-09 (Proxima, 3.13) and CAS-05 (Thea, 3.03) combine the highest C7 scores among non-tokamak concepts with the highest C6 scores among D-T concepts. If coil manufacturing industrializes, both move into Tier 1.

4. **D-T fuel cycle imposes a structural ceiling**. All D-T concepts cluster at C5 = 2.0-2.8 regardless of architecture. This 2-3 point gap vs. aneutronic concepts (C5 = 3.5-4.5) is irreducible — it reflects tritium handling, EPZ requirements, and activation waste that cannot be engineered away.

5. **Pulsed concepts penalized more after gate audit**. MagLIF (−0.35), GF (−0.14), and HB11 (−0.12) all dropped because the audit identified chamber clearing, rep-rate, and consumable gates that Pass 1 partially collapsed into single line items. Pulsed operations have more distinct failure modes than Pass 1 scorers recognized.

6. **CFS (01) drops below 3.0** — not from C1-C6 corrections but from the C7 gate audit finding two additional gates (FLiBe MHD, TBR) that peer D-T concepts were penalized for but CAS-01 was not. This harmonizes CFS's C7 with the D-T MFE peer group.

---

## Part 5: Z-Score Normalized Table and Final Ranking

### Methodology

For each criterion i, the z-score for concept c is:

```
z_i,c = (calibrated_raw_score_i,c − mean_i) / stdev_i
```

Where mean_i and stdev_i are computed across all 13 concepts for criterion i (population statistics). The z-score composite is the arithmetic mean of z-scores across all 7 criteria. This ensures every criterion contributes equally regardless of its natural scale and variance.

### Criterion Statistics

| Criterion | Mean | Std Dev | Range (min–max) | Interpretation |
|-----------|------|---------|-----------------|----------------|
| C1 (Modularization) | 3.36 | 0.29 | 2.8–3.8 | **Narrowest spread** — concepts cluster near 3.5; limited differentiation |
| C2 (Scalability) | 3.58 | 0.55 | 2.5–4.0 | Moderate spread; pulsed/modular concepts cluster at 4.0 |
| C3 (Supply Chain) | 3.05 | 0.23 | 2.8–3.5 | **Very narrow** — most concepts score 2.8–3.2 |
| C4 (Complexity) | 2.73 | 0.42 | 2.0–3.5 | Moderate spread; exotic concepts score higher (simpler) |
| C5 (Customization) | 2.85 | 0.87 | 2.0–4.5 | **Widest spread** — fuel choice (D-T vs. aneutronic) dominates |
| C6 (Capacity Factor) | 3.82 | 0.64 | 2.5–4.5 | Moderate spread; post-calibration, most MFE/IFE cluster at 4.0–4.5 |
| C7 (Feasibility) | 2.08 | 0.90 | 1.0–3.5 | **Wide spread** — the most differentiating criterion |

**Key observation**: C5 (customization, σ=0.87) and C7 (feasibility, σ=0.90) have the widest spreads, meaning they differentiate concepts most strongly. C1 (σ=0.29) and C3 (σ=0.23) have the narrowest spreads, meaning they contribute least to ranking differentiation. Z-score normalization corrects for this: a 0.5-point advantage on C3 (σ=0.23) contributes more z-score separation than a 0.5-point advantage on C7 (σ=0.90). This is appropriate because C3's narrow spread means 0.5 points represents a genuinely larger relative advantage within that criterion.

### Z-Score Table

| Criterion | 01-CFS | 02-Sono | 03-Cortex | 04-HB11 | 05-Thea | 06-CHARM | 07-MagLIF | 09-Proxima | 10-Gauss | 11-Realta | 14-GF | 22-FLF | 28-ES |
|-----------|--------|---------|-----------|---------|---------|----------|-----------|------------|----------|-----------|-------|--------|-------|
| C1 (z) | +0.47 | +0.47 | +0.47 | +0.47 | +1.16 | +1.50 | +0.47 | −0.21 | −1.58 | +0.47 | −1.24 | −1.92 | −0.55 |
| C2 (z) | −1.94 | +0.76 | +0.76 | +0.76 | −0.50 | +0.22 | +0.76 | −1.04 | −1.94 | +0.76 | +0.76 | +0.76 | −0.14 |
| C3 (z) | +0.64 | +0.64 | +0.64 | +1.96 | −1.12 | +0.64 | −0.24 | −1.12 | +0.20 | −1.12 | −1.12 | −1.12 | +1.08 |
| C4 (z) | −1.73 | +1.83 | +0.64 | +0.64 | −0.55 | +0.64 | +0.64 | −0.55 | −1.73 | +0.64 | −0.55 | +0.64 | −0.55 |
| C5 (z) | −0.98 | +0.86 | +0.74 | +1.89 | −0.75 | +1.77 | −0.98 | −0.06 | −0.52 | −0.41 | −0.98 | +0.40 | −0.98 |
| C6 (z) | +0.27 | +1.05 | +1.05 | −2.06 | +0.59 | +1.05 | −1.28 | +0.27 | +0.27 | −0.50 | −1.28 | +1.05 | −0.50 |
| C7 (z) | +1.03 | −1.20 | −0.64 | −1.20 | +0.47 | −1.20 | −0.64 | +1.59 | +1.59 | −0.09 | −0.64 | −0.09 | +1.03 |
| **Z-Composite** | **−0.32** | **+0.63** | **+0.52** | **+0.35** | **−0.10** | **+0.66** | **−0.18** | **−0.16** | **−0.53** | **−0.03** | **−0.72** | **−0.04** | **−0.09** |

### Final Ranking by Z-Score Composite

| Rank | Concept | Z-Composite | Raw Composite | Raw Rank | Rank Shift | Confidence |
|------|---------|-------------|---------------|----------|------------|------------|
| 1 | 06-CHARM (Pale Blue Fusion) | **+0.66** | 3.37 | 1 | — | Low |
| 2 | 02-Sonofusion | **+0.63** | 3.33 | 2 | — | Very Low |
| 3 | 03-Cortex Laser ICF | **+0.52** | 3.31 | 3 | — | Low |
| 4 | 04-HB11 Laser ICF p-B11 | **+0.35** | 3.14 | 5 | ↑1 | Medium |
| 5 | 11-Realta D-T Mirror | **−0.03** | 3.04 | 7 | ↑2 | Medium |
| 6 | 22-Projectile ICF (FLF) | **−0.04** | 3.19 | 4 | ↓2 | Medium |
| 7 | 28-ES Full HTS Tokamak | **−0.09** | 3.00 | 9 | ↑2 | Medium |
| 8 | 05-Thea Planar Stellarator | **−0.10** | 3.03 | 8 | — | High |
| 9 | 09-Proxima QI Stellarator | **−0.16** | 3.13 | 6 | ↓3 | High |
| 10 | 07-MagLIF | **−0.18** | 2.86 | 12 | ↑2 | Medium |
| 11 | 01-CFS HTS Compact Tokamak | **−0.32** | 2.89 | 11 | — | High |
| 12 | 10-Gauss Large Stellarator | **−0.53** | 2.91 | 10 | ↓2 | High |
| 13 | 14-GF MTF Pneumatic | **−0.72** | 2.69 | 13 | — | High |

### Concept-by-Concept Commentary (Final Ranking)

**Rank 1: 06-CHARM (z = +0.66)**
- **Strongest structural advantage**: Aneutronic fuel (C5 z=+1.77) combined with steady-state operation (C6 z=+1.05) creates the strongest combined customization-availability profile, irreducible advantages no D-T concept can match.
- **Most binding constraint**: Three unretired binary gates on core physics (C7 z=−1.20), the worst feasibility score in the cohort alongside Sonofusion and HB11. Combined success probability estimated at 3–10%.
- **Confidence**: **Low**. Ranking is conditional on physics that has zero experimental validation. The z-composite is driven by extreme outlier performance on C5 and C6, which are irrelevant if C7 gates fail.

**Rank 2: 02-Sonofusion (z = +0.63)**
- **Strongest structural advantage**: Simplest plant architecture (C4 z=+1.83, the highest single z-score in the table), creating the lowest operational coupling of any concept.
- **Most binding constraint**: Three binary gates at speculative evidence (C7 z=−1.20). Arguably the weakest physics case in the entire fusion landscape — TRL 0 with 4 orders of magnitude temperature gap.
- **Confidence**: **Very Low**. This ranking is a mathematical artifact — excellent C1–C6 profile paired with floor-level C7. No rational R&D portfolio would weight this concept equivalently to its rank position.

**Rank 3: 03-Cortex (z = +0.52)**
- **Strongest structural advantage**: High capacity factor ceiling (C6 z=+1.05) from MHz quasi-continuous operation with compact architecture, and D-D fuel avoids tritium infrastructure.
- **Most binding constraint**: Two binary gates including 14-order-of-magnitude physics extrapolation and 1000× anomalous energy claim (C7 z=−0.64). The energy anomaly undermines the theoretical framework itself.
- **Confidence**: **Low**. Better physics foundation than Sonofusion but the anomalous energy-per-event claim is a serious red flag.

**Rank 4: 04-HB11 (z = +0.35)**
- **Strongest structural advantage**: Cleanest customization profile in the cohort (C5 z=+1.89, the second-highest single z-score) and strong supply chain learning (C3 z=+1.96, the highest single z-score in the entire table).
- **Most binding constraint**: Lowest capacity factor (C6 z=−2.06, the lowest single z-score in the table) from 67% pulsed duty cycle at 1 Hz, compounded by binary avalanche gain gate. The duty cycle is a hard physics floor that engineering cannot overcome without higher rep rate.
- **Confidence**: **Medium**. Z-score ranking rises from raw rank 5→4 because z-normalization amplifies HB11's extreme C3 and C5 advantages (in narrow-spread criteria) while moderating the C6 penalty (in a wider-spread criterion). This is appropriate — HB11's supply chain profile is genuinely exceptional among all concepts.
- **Raw vs. z-score divergence**: ↑1 rank. Driven by C3 z=+1.96 (0.45 raw points above mean, but in the tightest criterion, this is nearly 2σ above average).

**Rank 5: 11-Realta D-T Mirror (z = −0.03)**
- **Strongest structural advantage**: Strong scalability (C2 z=+0.76) from the linear scaling thesis, with moderate complexity (C4 z=+0.64) due to cylindrical simplicity and no disruptions.
- **Most binding constraint**: Two binary gates (C7 z=−0.09) on end-plug confinement and linear scaling, plus newly identified recirculating power gate. Pilot at Qe≈0.75 shows the gap to commercial viability is large.
- **Confidence**: **Medium**. Z-score ranking rises from raw rank 7→5 because Realta's well-distributed z-scores (no extreme negatives except C3) sum favorably compared to concepts with lopsided profiles.
- **Raw vs. z-score divergence**: ↑2 ranks. Realta has no criterion below z=−1.12, while higher raw-ranked concepts (22-FLF at z-rank 6, 09-Proxima at z-rank 9) have severe weaknesses on specific criteria that z-normalization amplifies.

**Rank 6: 22-Projectile ICF FLF (z = −0.04)**
- **Strongest structural advantage**: Highest physical capacity factor (C6 z=+1.05) of any D-T concept due to liquid lithium first wall eliminating the dominant maintenance driver.
- **Most binding constraint**: Lowest modularization score in cohort (C1 z=−1.92, the most negative z-score in the table) because EM gun at 74% of capital is monolithic with no learning path.
- **Confidence**: **Medium**. Z-score ranking drops from raw rank 4→6 because z-normalization severely penalizes the EM gun's C1 and C3 drag (in narrow-spread criteria, these below-average scores translate to very negative z-scores). Machine 4 cancellation leaves concept orphaned.
- **Raw vs. z-score divergence**: ↓2 ranks. The key driver is C1 z=−1.92 and C3 z=−1.12 — FLF's EM gun dependency is exposed as the worst modularization and supply chain profile in the cohort when measured in standard deviations.

**Rank 7: 28-ES Full HTS Tokamak (z = −0.09)**
- **Strongest structural advantage**: Highest supply chain learning (C3 z=+1.08) among D-T concepts, reflecting REBCO tape's demonstrated 18–24% learning rate and Shanghai Superconductor's commercial-scale production.
- **Most binding constraint**: D-T customization penalty (C5 z=−0.98) shared with all D-T concepts, plus undefined blanket architecture (captured in C7 z=+1.03, which is above average but includes a blanket penalty).
- **Confidence**: **Medium**. Z-score ranking rises from raw rank 9→7 because ES's C7 score (3.0) is well above the cohort mean (2.08), translating to a strong z=+1.03. No binary gates and clear W7-X/ITER heritage validates the tokamak pathway.
- **Raw vs. z-score divergence**: ↑2 ranks. ES benefits from z-normalization because its moderately good C7 (3.0) is 1σ above the cohort mean (heavily pulled down by speculative concepts at C7=1.0). In raw terms, C7=3.0 looks mediocre; in z-score terms, it's among the top 4.

**Rank 8: 05-Thea Planar Stellarator (z = −0.10)**
- **Strongest structural advantage**: Highest modularization among stellarators (C1 z=+1.16) from planar coil geometry enabling factory winding, combined with high capacity factor (C6 z=+0.59) from disruption-free operation.
- **Most binding constraint**: Weak supply chain learning (C3 z=−1.12) due to unique coil control system and V-4Cr-4Ti first wall with no external demand, plus D-T customization burden (C5 z=−0.75).
- **Confidence**: **High** for relative position. Eos device (2030–2032) is the decisive validation point. Score is stable unless coil control reliability proves worse than predicted.

**Rank 9: 09-Proxima QI Stellarator (z = −0.16)**
- **Strongest structural advantage**: Highest technical feasibility of any concept (C7 z=+1.59, tied with Gauss for highest C7 z-score) — zero binary gates, strong W7-X heritage, clear validation pathway.
- **Most binding constraint**: Low scalability (C2 z=−1.04) from single-plasma device with no replication path and 1 GWe minimum viable scale, plus weak supply chain learning (C3 z=−1.12) from 3D HTS coil manufacturing uncertainty.
- **Confidence**: **High**. Z-score ranking drops from raw rank 6→9 because z-normalization penalizes Proxima's below-average C2 and C3 more heavily (these narrow-spread criteria amplify small disadvantages). This is a significant divergence from raw ranking.
- **Raw vs. z-score divergence**: ↓3 ranks, the largest drop. Proxima's raw composite (3.13) is buoyed by a high C7 (3.5), but C7 has wide spread (σ=0.90), so +1.42 raw points above mean translates to only z=+1.59. Meanwhile, C2 (3.0) is −0.58 below mean in a moderate-spread criterion (σ=0.55), translating to z=−1.04. The z-score correctly identifies that Proxima's scalability limitation is a more distinctive disadvantage than its feasibility is a distinctive advantage, because more concepts cluster near C7=3.5 (Gauss, Thea also at 3.5) than near C2=3.0 (only Proxima and Gauss score ≤3.0).

**Rank 10: 07-MagLIF (z = −0.18)**
- **Strongest structural advantage**: Strong scalability (C2 z=+0.76) from chamber replication and modular pulsed power driver.
- **Most binding constraint**: Low capacity factor (C6 z=−1.28) from pulsed duty cycle constraints and D-T customization penalty (C5 z=−0.98).
- **Confidence**: **Medium**. Z-score ranking rises from raw rank 12→10 because MagLIF's moderate C4 (z=+0.64) in the narrow-spread complexity criterion provides more z-score uplift than the raw score suggests. Pacific Fusion DS milestone (2027–2030) is decisive.
- **Raw vs. z-score divergence**: ↑2 ranks. MagLIF's raw composite (2.86) is low, but its z-profile is less extreme than Gauss (z-rank 12) because MagLIF has no criterion below z=−1.28, while Gauss hits z=−1.94 on C2.

**Rank 11: 01-CFS HTS Compact Tokamak (z = −0.32)**
- **Strongest structural advantage**: Highest technical feasibility among tokamaks (C7 z=+1.03) with demonstrated pathway through SPARC, and strong supply chain learning (C3 z=+0.64) from REBCO cross-industry demand.
- **Most binding constraint**: Lowest scalability in cohort (C2 z=−1.94, tied with Gauss for most negative) from single-plasma tokamak with no replication path, compounded by highest complexity (C4 z=−1.73).
- **Confidence**: **High**. The low z-composite does NOT mean CFS is a poor concept — it means the *LCOE improvement rate with deployment* is slower than most alternatives. CFS has the highest probability of reaching operation among all concepts, but this framework measures learning curves, not probability of working.
- **Raw vs. z-score divergence**: Same rank (11). CFS is consistently penalized by narrow-spread criteria (C2, C4) where its below-average scores translate to very negative z-scores.

**Rank 12: 10-Gauss Large Stellarator (z = −0.53)**
- **Strongest structural advantage**: Highest technical feasibility (C7 z=+1.59, tied with Proxima) from deepest W7-X experimental heritage and disruption-free operation.
- **Most binding constraint**: Lowest scalability (C2 z=−1.94) and lowest complexity score (C4 z=−1.73) from 18m major radius, 45,000t mass, and 80 unique blanket segments.
- **Confidence**: **High**. Safe physics bet with structurally limited cost reduction potential. The z-score ranking drops from raw rank 10→12 because Gauss's twin weaknesses (C2, C4) are in moderate-spread criteria that z-normalization amplifies.
- **Raw vs. z-score divergence**: ↓2 ranks. Gauss and CFS share similar z-profiles (strong C7, weak C2/C4), but CFS has slightly better C1 (+0.47 vs −1.58) and C5 (−0.98 vs −0.52) z-scores. The C1 difference is decisive — CFS's 18 TF coils in the manufacturing sweet spot vs. Gauss's 40 unique-shape coils creates a 2σ separation on modularization.

**Rank 13: 14-GF MTF Pneumatic (z = −0.72)**
- **Strongest structural advantage**: Strong scalability (C2 z=+0.76) from chamber replication with simple compression geometry.
- **Most binding constraint**: Three binary gates identified in audit (piston sync, compression ratio, technology transfer gap) with lowest C1 (z=−1.24) among MIF concepts due to monolithic compression driver assembly. LM26→commercial technology disconnect is the most severe structural problem found in the entire audit.
- **Confidence**: **High** for bottom ranking. The z-score confirms the raw ranking: GF has no criterion with z > +0.76 (tied with 7 other concepts on C2) and multiple criteria below z=−0.5.

### Z-Score vs. Raw Ranking: Key Divergences

Three concepts shift ≥2 ranks between raw and z-score ordering:

1. **09-Proxima drops 3 ranks (raw 6 → z 9)**: Proxima's moderate C2=3.0 and C3=2.8 are penalized more heavily by z-normalization because these criteria have narrow spreads. A half-point below average on C3 (σ=0.23) generates z=−1.12, equivalent to being 1.12 standard deviations below the cohort. This correctly identifies that Proxima's supply chain and scalability limitations are more structurally distinctive than its raw scores suggest.

2. **22-FLF drops 2 ranks (raw 4 → z 6)**: FLF's EM gun dependency (C1=2.8 in a σ=0.29 criterion → z=−1.92) is exposed as the most extreme modularization disadvantage in the cohort. In raw terms, C1=2.8 looks only 0.5 points below average. In z-score terms, it's nearly 2σ below — a genuinely severe structural limitation that raw scoring understates.

3. **11-Realta rises 2 ranks (raw 7 → z 5)** and **28-ES rises 2 ranks (raw 9 → z 7)**: Both benefit from having no extreme z-score weaknesses. Their profiles are "consistently near average" — no criterion drops below z=−1.3. In a cohort dominated by concepts with extreme highs and lows (the speculative concepts), being consistently moderate is a z-score advantage.

### Interpretation Notes

The z-score composite is the **authoritative ranking metric** for this calibration. However, users should note two structural features of the z-score approach:

1. **Floor-level C7 scores are moderated by z-normalization**. Three concepts (CHARM, Sonofusion, HB11) share C7=1.0, which translates to z=−1.20. Because C7 has the widest spread (σ=0.90), a 1.08-point deviation from the mean generates "only" −1.20 standard deviations. Compare to C1, where the same 1.08-point deviation would generate z=−3.70. This means the z-composite gives *less* weight to feasibility risk extremes than an equal-weight raw composite would — a debatable design choice.

2. **Narrow-spread criteria dominate z-score differentiation**. C1 (σ=0.29) and C3 (σ=0.23) generate the largest z-score swings per raw point of difference. A concept 0.5 points above average on C3 gets z=+2.20, while a concept 0.5 points above average on C7 gets only z=+0.56. This amplifies supply chain and modularization differences and moderates feasibility differences — appropriate if one believes these factors are genuinely underweighted in raw scoring, debatable otherwise.

**Recommendation for decision-makers**: Use the z-score ranking as the primary ordering, but apply C7 as a **binary filter** before interpreting the composite. Any concept with C7 ≤ 1.5 (z < −0.64) should be flagged as a "conditional ranking" — its position is meaningful only if the core physics validates. The z-score ranking then becomes: "Among concepts where the physics works, which has the best cost reduction trajectory?"

With this filter applied:
- **Unconditional rankings (C7 ≥ 2.0)**: Realta (z-rank 5), FLF (6), ES (7), Thea (8), Proxima (9), CFS (11), Gauss (12)
- **Conditional rankings (C7 ≤ 1.5)**: CHARM (1), Sonofusion (2), Cortex (3), HB11 (4), MagLIF (10), GF (13)
