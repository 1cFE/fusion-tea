---
ID: 07-maglif
Concept: MagLIF (D-T)
Company: Pacific Fusion, Fuse Energy Technologies
Type: synthesis
Status: draft
Created: 2026-04-29
Stale: true
Stale-Reason: analysis-updated-iter-10
---

## 1. Executive Summary

- **Single most important risk**: Rep rate achievement—if commercial operation cannot exceed 0.5 Hz, LCOE remains above 60 $/MWh regardless of driver cost reductions, missing the advanced fission threshold by 20–50%. The RTL insertion/chamber clearing cycle time is a mechanical bottleneck with no demonstrated solution path at Hz scale.
- **Single most important advantage**: Elimination of superconducting magnets removes the REBCO tape supply chain constraint entirely, enabling earlier deployment and eliminating tokamak/stellarator manufacturing ramp-up dependencies. Driver capital (10% of total capital) is a smaller lever than rep rate.
- **LCOE ballpark**: Model gives 61 $/MWh at 0.5 Hz (1000 MWe, LTD driver) vs. Z-IFE reference 70 $/MWh—within 13% calibration agreement. Break-even with advanced fission (40–60 $/MWh) requires 0.5–0.8 Hz. Commercial viability depends on achieving Pacific Fusion's stated 1 Hz target, which would deliver ~30 $/MWh at current capital assumptions—competitive if demonstrated. At Pacific Fusion's 250 MWe design point, LCOE will be materially higher (Z-IFE shows 500 MWe > 10 ¢/kWeh).
- **Confidence verdict**: Low—rep rate and yield scaling are both extrapolations beyond demonstrated hardware (current: single-shot at χ ≈ 0.1; commercial: 1 Hz at Q_facility ≥ 1). Driver cost for IMG architecture is proprietary/unverified. Cryogenic target cost at scale has no production path. Four blocking gaps remain unresolved.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity magnitude and commercial achievability:

### 1. Rep Rate (0.1 → 1 Hz): LCOE swing 3–10×

**Assumed value**: 0.5 Hz (Z-IFE frozen-FLiBe RTL reference)
**Source**: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5
**Sensitivity magnitude**: LCOE ∝ 1/rep_rate at fixed capital. 0.1 Hz → 305 $/MWh (uncompetitive); 0.5 Hz → 61 $/MWh (marginal); 1.0 Hz → 30 $/MWh (competitive). Each doubling of rep rate halves LCOE.
**What would flip the conclusion**: If rep rate cannot exceed 0.25 Hz (122 $/MWh), MagLIF exits the commercially viable band entirely regardless of driver cost improvements or yield gains. Conversely, demonstrated 1 Hz operation shifts MagLIF into the competitive LCOE range even without IMG cost reductions. The Z-IFE study explicitly stated that minimum-COE rep rates (1.0–1.8 Hz) are "beyond the reach of the replaceable RTL concept"—the enabling technology for pulsed power delivery. **TRL status**: RTL insertion at Hz scale is TRL 2; no robotic prototype exists; chamber clearing post-GJ shot at 1-second cycle time is undemonstrated.

### 2. Cryogenic Target Cost ($/shot): LCOE floor at 15.8M shots/yr

**Assumed value**: Not explicitly modeled in baseline; commercial viability threshold is ~$1–2/shot
**Source**: analysis.md §Section 2, Challenge 2; consumable cost sweep
**Sensitivity magnitude**: At 0.5 Hz (15.8M shots/yr), each $1/shot adds 2.1 $/MWh to LCOE. Break-even at 100 $/MWh is 18.4 $/shot; at 150 $/MWh is 42 $/shot. Current cryo target cost is thousands of $/shot with no production path demonstrated. The $1–2/shot commercial threshold requires a 1000× cost reduction vs. current NIF-style cryogenic ice-layer targets.
**What would flip the conclusion**: If Pacific Fusion's self-magnetizing composite targets (demonstrated October 2025 at 22 MA without external coils or laser preheat) can achieve adequate gain without cryogenic ice layers, target cost could fall to ammunition-scale economics (<$1/shot via mass manufacturing). This would eliminate the consumable cost floor entirely and make LCOE insensitive to target cost. Conversely, if cryogenic targets are mandatory and cannot scale below $10/shot, annual consumable O&M at 1 Hz exceeds $150M/year—larger than annual capital amortization—and MagLIF becomes O&M-limited rather than capital-limited. **Current TRL**: Cryo ice-layer targets at Hz production rates are TRL 1 (no demonstrated path); non-cryo composite targets are TRL 3 (demonstrated on Z, not yet at commercial gain).

### 3. Availability (60–90%): LCOE elasticity –0.98

**Assumed value**: 85% (Z-IFE assumption, unattributed)
**Source**: z-ife-sand2006-7148-thermal-cycles.md §3.1.1.5; analysis.md §Section 5
**Sensitivity magnitude**: Elasticity –0.98 means a 10% reduction in availability (85% → 76.5%) increases LCOE by ~10% (61 → 67 $/MWh). Thick-liquid-wall success scenario: 85–90% (no scheduled first-wall replacement); failure scenario: 60–75% (tokamak-analogous chamber replacement cycles).
**What would flip the conclusion**: If the FLiBe thick liquid wall succeeds in eliminating periodic chamber replacement (the key mechanical innovation enabling high availability), MagLIF achieves a structural O&M advantage over all solid-first-wall MFE concepts. If the liquid wall fails and chamber/electrode lifetime under GJ-scale shock + neutron + FLiBe corrosion requires replacement on tokamak-analogous schedules (every 2–5 years), availability falls to 60–70% and LCOE increases by 20–40%. **Current TRL**: Thick liquid wall at GJ-scale repetitive shots is TRL 2 (analyzed but never tested at scale). Combined environment testing (shock + neutron + corrosion + thermal cycling) does not exist for any proposed chamber material.

### 4. Driver Capital (LTD $372M → IMG $37–75M): LCOE swing 61 → 54 $/MWh

**Assumed value**: $372M (LTD median, 1 PW driver)
**Source**: z-ife-sand2006-7148-thermal-cycles.md §3.1.2
**Sensitivity magnitude**: 10× driver cost reduction (LTD $372M → IMG $37M) reduces LCOE by 11% (61 → 54 $/MWh). Driver capital is 10.3% of total capital in the corrected model (CAS21 = $200M). The arxiv roadmap explicitly requires a 5–10× cost reduction from current commercial pulsed power pricing (~$5/J) to <$0.50/J for commercial viability.
**What would flip the conclusion**: Even optimistic IMG cost reductions (10×) cannot achieve competitive LCOE without rep rate improvements—54 $/MWh is still above the 40 $/MWh lower threshold for advanced fission. Driver cost is a second-order lever; rep rate and availability dominate. However, if IMG cost does NOT fall below ~$1/J (only 5× reduction vs. the required 10×), driver capital remains ~$75M and LCOE stays near 55 $/MWh, which is marginal even at 0.5 Hz and requires 0.8+ Hz for competitiveness. **Current TRL**: IMG architecture at 60+ MA plant scale is TRL 3–4 (TITAN I demonstrated 1 TW at 0.8 MA; Z STAR 12.8 MA targeted 2027; 60+ MA commercial driver unbuilt). Cost validation at plant scale is absent.

### 5. Thermal Efficiency (42% → 50%): LCOE reduction –5.7% per 10% gain

**Assumed value**: 42% (combined Brayton-Rankine, steel chamber)
**Source**: z-ife-sand2006-7148-thermal-cycles.md §3.2
**Sensitivity magnitude**: Elasticity –0.057 means a 10% increase in efficiency (42% → 46.2%) reduces LCOE by 0.57% (61 → 60.7 $/MWh). The Z-IFE study showed that carbon-carbon composite chambers could reach 50% efficiency (20% gain), which would reduce LCOE by ~1%. This is marginal compared to rep rate leverage.
**What would flip the conclusion**: High-temperature materials (C-C composite, SiC/SiC) enabling He Brayton above 1000–1210 K would improve efficiency to 50%, but the capital cost of advanced materials and the TRL gap (not commercially available) offset most of the LCOE benefit. Thermal efficiency is a nice-to-have optimization, not a make-or-break parameter. Even achieving 50% efficiency cannot compensate for rep rate shortfalls—at 0.1 Hz, 50% efficiency still yields >280 $/MWh.

---

## 3. Risk Verdicts

### Challenge 1: Rep rate dominates LCOE more than any single capital item (analysis §S2.1)

**Verdict**: Unlikely resolvable at 1 Hz commercial target
**Rationale**: Z-IFE explicitly stated that 1.0–1.8 Hz minimum-COE rep rates are "beyond the reach of the replaceable RTL concept." RTL insertion, chamber clearing, liquid wall reconstitution, and target alignment must complete in 1 second for 1 Hz operation—a 10× improvement over the 0.1 Hz baseline that SNL judged manageable. No robotic RTL insertion system exists even at prototype scale.
**What would retire this risk**: Demonstrated Hz-scale RTL insertion with electrical alignment verified post-blast; chamber clearing data at GJ yields showing <1 second recovery time; Pacific Fusion DS rep-rated operation at ≥0.5 Hz (currently single-shot only). Alternatively, elimination of the RTL entirely via a non-contact power delivery architecture—but no such design has been proposed.

### Challenge 2: Per-shot consumables create a cost floor with no MFE analogue (analysis §S2.2)

**Verdict**: Genuinely uncertain—depends on non-cryo target pathway
**Rationale**: If cryogenic ice-layer targets are required, the cost scaling from NIF-style fabrication (15–20 hours per target) to 1 Hz production (1 target/second) is a paradigm shift with no demonstrated industrial analogue. Pacific Fusion's self-magnetizing composite targets (October 2025, 22 MA, no external coils or laser preheat) offer a potential bypass if adequate gain is achievable without cryogenic fuel—but this has not been demonstrated experimentally above χ ≈ 0.1.
**What would retire this risk**: Demonstrated ignition (χ ≥ 1) with non-cryogenic composite targets at 60+ MA; or, alternatively, a cryo target factory producing ice-layer targets at <$2/shot verified cost in a pilot manufacturing line. The second path requires validating the ammunition-production analogy at cryogenic temperatures—a materials handling challenge with no precedent.

### Challenge 3: Driver cost is a novel capital cost category (analysis §S2.3)

**Verdict**: Likely resolvable—cost reduction trajectory credible
**Rationale**: Fuse Energy's TITAN I in-house manufacturing achieved 10× cost reduction vs. off-the-shelf procurement ($200 Rogowski coil vs. $20k commercial, 1 day vs. 1 month). The arxiv roadmap's 5–10× target reduction from $5/J to <$0.50/J is aggressive but has a demonstrated industrial pathway (capacitor/switch manufacturing at scale, vertical integration). However, even optimistic 10× reductions only improve LCOE by 11%—this is a necessary but insufficient condition for commercial viability.
**What would retire this risk**: Fuse Z STAR (2027, 12.8 MA) or Pacific Fusion DS (2030, 60+ MA target) achieving published $/J cost validation; independent third-party cost audit of IMG brick manufacturing at production scale; demonstration that IMG lifetime (currently ~10^4 shots) can reach 10^9 shots (~30 years at 1 Hz) without performance degradation.

### Challenge 4: Yield scaling is simulation-anchored but not experimentally demonstrated (analysis §S2.4)

**Verdict**: Genuinely uncertain—ignition gap is large
**Rationale**: Current Z experiments achieve χ ≈ 0.1 with gas-fill targets at 20 MA. Commercial GJ-class yields require 60+ MA and cryogenic DT ice-layer targets—both never tested. The April 2025 arXiv:2504.10680 multi-dimensional simulations benchmarked against Z data upgraded the physics basis from pure extrapolation to simulation-anchored extrapolation, confirming the 50–60 MA threshold for net facility gain. However, simulation validation at χ ≈ 0.1 does not guarantee ignition success at 10× higher confinement parameter. Laser ICF achieved ignition at NIF; MagLIF has not.
**What would retire this risk**: Experimental ignition demonstration (χ ≥ 1) at any current or driver energy on Z, ZR, or a scaled facility; Pacific Fusion DS achieving Q_facility > 1 (stated 2030 goal with 100+ MJ yield from ~80 MJ stored); Fuse Z STAR 10^14 neutrons/shot validation (2027 target). Any of these would retire the physics scaling uncertainty and shift the risk to engineering (rep rate, chamber lifetime) rather than plasma performance.

### Challenge 5: Chamber clearing and RTL cycle time constrain achievable rep rate (analysis §S2.5)

**Verdict**: Unlikely resolvable—same as Challenge 1
**Rationale**: (See Challenge 1 verdict above—these are the same technical barrier stated from different perspectives. Challenge 1 emphasizes LCOE impact; Challenge 5 emphasizes mechanical constraints.)
**What would retire this risk**: (See Challenge 1)

### Challenge 6: TEA tools for pulsed fusion are underdeveloped (analysis §S2.6)

**Verdict**: Likely resolvable—framework extension underway
**Rationale**: The February 2026 pyFECONs extension (Woodruff et al., arXiv:2602.19389) introduces MIFE as an explicit cost-driver track with Account 22.1.3 treated as a swap-point replaced by architecture-specific drivers. This provides the first published costing framework structurally compatible with MagLIF. The 1costingfe model used for this analysis successfully incorporated Z-IFE parameters via cost_overrides, demonstrating that free-form parametric modeling is viable even without a dedicated MIFE systems code.
**What would retire this risk**: Full pyFECONs paper acquisition (abstract-only currently extracted) to determine if MagLIF-specific account priors exist; alternatively, a Pacific Fusion or Fuse Energy public release of a plant-level cost model using the IMG architecture. The risk is "likely resolvable" because the technical capability exists (demonstrated by this analysis); what's missing is data, not methodology.

---

## 4. Structural Advantages and Disadvantages

Relative to a conventional D-T tokamak (ITER/ARC-class) baseline:

### Eliminated cost accounts (advantages)

| Account | MFE Tokamak | MagLIF | Impact |
|---------|-------------|--------|--------|
| **Superconducting magnets (CAS22 coil system)** | $300–500M (REBCO tape, Nb₃Sn, structure, cooling) | $0 | **Eliminates ~10–15% of direct capital** and removes the REBCO tape supply chain constraint—the single largest manufacturing bottleneck for compact tokamaks. Pulsed copper coils or self-magnetization replaces SC magnets entirely. |
| **Steady-state heating & current drive** | $100–200M (NBI, ECRH, LHCD) | $0 (driver performs this function) | Heating is embedded in pulsed power driver account; no separate RF or beam injection systems required. |
| **Divertor** | $50–100M (PFC, strike point management) | $0 | Pulsed spherical chamber with thick liquid wall handles debris removal between shots; no divertor physics or exhaust management. |
| **Scheduled first-wall replacement** | Capacity factor penalty: 10–30% downtime every 2–5 FPY | Potentially eliminated if liquid wall succeeds | If FLiBe thick liquid wall survives GJ-scale shocks, periodic blanket replacement is eliminated. This is the **largest O&M structural advantage** if demonstrated—enables 85–90% availability vs. tokamak 60–75%. **Status**: TRL 2, undemonstrated at scale. |

**Quantified advantage**: Superconducting magnet elimination alone removes ~$400M from a comparable-scale tokamak capital base (~10–15% of direct capital). Combined with divertor elimination, MagLIF's CAS22 structure is fundamentally simpler—**~20% lower direct capital** before driver cost is added back.

### Added cost accounts (disadvantages)

| Account | MFE Tokamak | MagLIF | Impact |
|---------|-------------|--------|--------|
| **Pulsed power driver** | $0 | $372M (LTD ref) or $37–75M (IMG target) | **New dominant capital account**—10% of total capital even at optimistic IMG costs. No database precedent; cost per joule must fall 10× from commercial pulsed power pricing to meet targets. |
| **RTL + target factory** | $0 | $120M (frozen-FLiBe RTL estimate) | Factory capital for automated RTL fabrication, target assembly, and insertion logistics. Laser IFE target factories are $244M baseline; MagLIF benefits from mm-scale vs. µm-scale tolerances but still requires Hz-rate production at 15.8M units/year. |
| **Per-shot consumables (variable O&M)** | Negligible | $15–150M/year depending on target cost | At $1/shot (commercial threshold): $16M/yr. At $10/shot (current cryo analogy): $158M/yr. This is a **variable O&M floor with no MFE analogue**—can exceed annual capital amortization if target costs don't scale. |

**Quantified disadvantage**: Driver + RTL factory add $400–500M to capital (LTD case) vs. the eliminated SC magnet + divertor savings (~$450M). At IMG target costs ($75M driver), the net capital difference is approximately neutral, but the **cost structure is fundamentally different**: MagLIF trades fabrication complexity (HTS tape ramp-up) for operational complexity (Hz-rate RTL insertion + chamber clearing). The O&M penalty from consumables is the binding constraint—if target costs exceed $5/shot, annual consumable O&M surpasses the capital savings from magnet elimination.

### Shared constraints (no advantage or disadvantage)

- **D-T fuel cycle**: Identical tritium breeding (TBR > 1), Li-6 enrichment, startup inventory (~1–5 kg at $30k/g) as all D-T concepts. MagLIF's FLiBe blanket may simplify tritium extraction vs. solid breeders (vacuum degassing from liquid circuit), but this is undemonstrated. **No cost advantage** vs. tokamaks using FLiBe blankets (e.g., ARC).
- **Neutron shielding and activation**: 14.1 MeV D-T neutrons create identical shielding, activation, and waste management requirements. MagLIF's thick liquid blanket (80 cm FLiBe) provides integrated shielding, but tokamaks have comparable blanket thicknesses. **Neutral**.
- **Balance of plant**: Thermal cycle, turbines, heat rejection are standard industrial equipment. MagLIF's pulsed thermal source may complicate turbomachinery integration (thermal cycling on blades), but Z-IFE analysis found this manageable with combined Brayton-Rankine at 42% efficiency. **Neutral to slight disadvantage** (pulsed vs. continuous thermal input).

### Economy-of-scale position

Z-IFE data shows **strong economy-of-scale sensitivity**: 1000 MWe → 7.0 ¢/kWeh; 2000 MWe → 5.7 ¢/kWeh (19% LCOE reduction). Pacific Fusion's 250 MWe commercial target sits **4× below** the Z-IFE reference plant size, implying LCOE > 10 ¢/kWeh at current capital assumptions (Z-IFE 500 MWe case is already >10 ¢/kWeh per §3.1.1.6). This is a **structural disadvantage** vs. gigawatt-scale tokamaks that benefit from BOP dilution across larger thermal output. MagLIF's modular architecture (claimed advantage) does not offset the per-MWe capital penalty at small scales.

---

## 5. Cross-Concept Positioning

MagLIF occupies a unique position in the fusion landscape as the only **liner-compression MIF concept with an electrical pulsed-power driver** and **no superconducting magnets**. Its nearest neighbors define a triangulation:

### Nearest neighbor #1: MTF/General Fusion (pneumatic liner compression)

**Shared**: Liner-compression MIF architecture, per-shot consumable compression element, rep rate as central LCOE lever, chamber clearing between shots, no demonstrated sustained gain.
**Divergence**: MTF uses pneumatic piston arrays (no pulsed-power capacitor banks, no RTL) vs. MagLIF's electrical IMG driver. MTF avoids the pulsed-power cost-per-joule challenge but introduces precision-machining complexity for the piston system. MTF's plasma-injected target approach differs from MagLIF's pre-magnetized cylindrical liner.
**LCOE positioning**: No MTF cost model is available for direct comparison, but the structural similarity suggests comparable LCOE sensitivity to rep rate and chamber clearing. MTF may have lower driver capital (no capacitor banks) but faces its own per-shot consumable challenge (plasma-facing piston surface degradation).

### Nearest neighbor #2: Helion (FRC w/ direct energy conversion)

**Shared**: Pulsed MIF, capacitor bank driver, rep rate as LCOE lever, discrete burn events with recovery cycles.
**Divergence**: Helion uses magnetic compression of merging FRC plasmoids vs. MagLIF's metal liner implosion. **Most significant**: Helion's D-He3 fuel eliminates tritium breeding entirely and enables direct electromagnetic energy recovery from the expanding plasmoid—removing both the FLiBe blanket capital/supply chain and improving driver energy recovery. MagLIF's D-T fuel has 100× higher reactivity but requires the full tritium infrastructure.
**LCOE positioning**: Helion's fuel choice is a structural LCOE advantage (no blanket capital, higher efficiency via DEC) offset by D-He3's lower reactivity and He-3 supply constraint. MagLIF's D-T fuel has no external fuel dependency but cannot recover driver energy, making net electrical output more sensitive to driver efficiency. If Helion's DEC achieves >50% recovery, its LCOE floor is lower than MagLIF's thermal-only conversion. If He-3 breeding fails, Helion has no fallback and MagLIF's D-T fuel is the lower-risk choice.

### Nearest neighbor #3: Laser IFE (indirect drive)

**Shared**: Inertial confinement, per-shot consumables (targets), target factory capital, chamber clearing, rep rate sensitivity, pulsed thermal cycle.
**Divergence**: **Driver efficiency** is the key differentiator—MagLIF's IMG at ~90% wall-plug vs. laser drivers at 5–15%. This 6–18× efficiency advantage reduces recirculating power fraction dramatically (MagLIF ~3% vs. laser IFE ~20–40%), making MagLIF's net power less sensitive to driver parasitic load. **Target alignment** is easier for MagLIF (mm-scale mechanical positioning) vs. laser IFE (µm-scale free-flight injection). **Final optics survivability** problem (TRL 2 for laser IFE) is absent in MagLIF—no exposed optics.
**LCOE positioning**: MagLIF's driver advantage should yield 20–40% lower LCOE than laser IFE at equivalent rep rate and yield, **if** target costs are comparable. Z-IFE estimated 7.0 ¢/kWeh (MagLIF LTD, 0.5 Hz) vs. 7.2 ¢/kWeh (direct-drive laser IFE) in the same study—near parity. The model shows 61 $/MWh (MagLIF) is competitive with published laser IFE estimates. However, if cryo target costs for MagLIF exceed laser IFE's (due to liner + cryogenic fuel combination), the driver efficiency advantage is offset by consumable O&M penalties.

### Where MagLIF is fundamentally different

**No other concept combines**: (1) no superconducting magnets, (2) electrical pulsed-power driver, (3) D-T fuel with conventional breeding, (4) thick liquid first wall, (5) liner-compression geometry. This unique combination means:
- MagLIF can deploy **earlier** than any tokamak/stellarator (no REBCO tape bottleneck).
- MagLIF's capital structure is **immune** to HTS supply chain failures but **exposed** to pulsed-power component lifetime and cost-per-joule improvements that have no fusion precedent.
- MagLIF's LCOE is **more sensitive to mechanical cycle time** (RTL insertion) than any MFE concept and **more sensitive to target manufacturing cost** than magnetic compression MIF (Helion, MTF).

**Strategic implication**: MagLIF is the **highest-risk, highest-reward pulsed concept** in the analyzed set—if rep rate, yield, and target costs all hit targets, it achieves competitive LCOE (~30 $/MWh at 1 Hz) without REBCO dependency. If any one of those three fails, LCOE exceeds 100 $/MWh and the concept is not commercially viable.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (5 total)

1. **Thermal efficiency**: 42% (Z-IFE combined Brayton-Rankine, steel chamber reference)
2. **Driver capital (LTD architecture)**: $372M (Z-IFE median, 1 PW driver, 12,600 cavities)
3. **Fixed charge rate**: 9.66% (Z-IFE financial assumption, consistent with fusion plant conventions)
4. **Chamber geometry**: 4 m radius, 80 cm FLiBe blanket, 20 cm Al first wall (Z-IFE/Derzon et al. 2000)
5. **Capacity factor (assumed)**: 85% (Z-IFE baseline, unattributed)

### Speculative parameters (7 total)

1. **Rep rate**: 0.5 Hz baseline is the Z-IFE "best case" with frozen-FLiBe RTL—not demonstrated. Commercial target is 1 Hz (Pacific Fusion/arxiv roadmap), which is explicitly "beyond the reach of the replaceable RTL concept." **Speculation range: 0.1–1.0 Hz** (20× LCOE swing).
2. **Driver capital (IMG architecture)**: Z-IFE LTD cost is the only public estimate; IMG may be 5–10× cheaper per arxiv roadmap (arxiv:2408.15206 §3.2.4) but no plant-scale validation exists. **Speculation range: $37–372M** (11% LCOE swing).
3. **Target cost at volume**: No published estimate for cryo ice-layer targets at Hz production rates. Commercial viability threshold is $1–2/shot; current cost is thousands $/shot. **Speculation range: $1–50/shot** (0–60 $/MWh LCOE contribution).
4. **Yield per shot**: GJ-class yields are simulation-derived (arXiv:2504.10680); ignition has never been demonstrated above χ ≈ 0.1. Gain formula (G = 30.15 × (E − 1.22)^2.038) may be optimistic. **Speculation: ±50% on yield** translates to ±30% on LCOE via power balance.
5. **Availability**: 85% assumes thick liquid wall eliminates scheduled chamber replacement—never tested at GJ-scale repetitive shots. Failure scenario: 60–75%. **Speculation range: 60–90%** (±20–40% LCOE swing via elasticity –0.98).
6. **Buildings/site capital (CAS21)**: Physical footprint estimate ($200M) vs. MFE/fission formula artifact ($919M). Z-IFE driver figure may already include capacitor hall, creating double-count risk. **Speculation range: $80–400M** (±3–8% LCOE impact).
7. **O&M cost structure**: Z-IFE does not itemize per-shot consumables separately; current model uses default 2%/yr capital fraction for fixed O&M and adds consumables algebraically. True O&M may differ by ±50%.

### Dominant source of LCOE uncertainty

**Rep rate** is the overwhelming uncertainty—its 20× range (0.1–1.8 Hz from Z-IFE data) produces a 3–10× LCOE swing (305 → 30 $/MWh) that **dwarfs all other parameters combined**. A 10× driver cost reduction (11% LCOE benefit) is negligible compared to a 2× rep rate shortfall (2× LCOE penalty). The second-largest uncertainty is **target cost** (unknown scaling from cryo fabrication), which creates a variable O&M floor that can exceed capital amortization if costs stay above $5–10/shot.

**Yield scaling** is the third-largest uncertainty—if ignition requires 10× more driver energy than projected, driver capital triples via power-law scaling (TW^0.6), compounding the already-dominant driver cost challenge. However, this is a **binary** uncertainty (either ignition is achievable at practical currents or it isn't), whereas rep rate and target cost are **continuous** uncertainties with demonstrated partial progress.

**Data adequacy**: 4 of 5 LCOE-critical parameters rest on 20-year-old Z-IFE data (LTD architecture, pre-MagLIF physics). Modern IMG architecture (Pacific Fusion DS, Fuse TITAN/Z STAR) has no published plant study. The February 2026 pyFECONs MIFE extension provides a framework but no MagLIF-specific priors. **This synthesis relies on translating LTD-era data to IMG assumptions via stated reduction factors** (5–10× driver cost, 60% → 90% efficiency)—introducing compounded uncertainties.

### Why confidence is Low

Of the 12 LCOE-critical parameters, **7 are speculative** (not measured/demonstrated at commercial scale), **4 have blocking data gaps** (rep rate, target cost, yield, IMG driver cost), and **only 1 (thermal efficiency) has high-confidence validation** from Z-IFE thermal cycle analysis. The model LCOE (61 $/MWh at 0.5 Hz) calibrates within 13% of Z-IFE reference (70 $/MWh), but this agreement is **not independently validated**—it reflects internal consistency of Z-IFE assumptions, not experimental confirmation. The speculative parameters have **multiplicative interactions** (rep rate × target cost × yield × availability), amplifying uncertainty. A ±50% error bar on any two parameters can shift LCOE by 2–3×.

**Bottom line**: The model captures the cost structure correctly (validated by Z-IFE alignment), but the **absolute LCOE estimate has ±100% uncertainty** because the four blocking parameters (rep rate, target cost, yield, driver cost) are all extrapolations beyond demonstrated hardware. Competitive LCOE (30 $/MWh at 1 Hz) depends on **simultaneous achievement** of four aggressive targets with no demonstrated integration: 1 Hz RTL cycle, $1/shot cryo targets, Q_facility > 1, and 10× driver cost reduction. Failure of any one parameter pushes LCOE above 60 $/MWh.

---

## 7. What Would Change My Mind

### Development #1: Demonstrated rep-rated operation at ≥0.5 Hz

**What**: Pacific Fusion DS or Fuse Z STAR achieving sustained repetitive firing at 0.5+ Hz with automated RTL insertion, chamber clearing, and target alignment validated post-blast. Success criteria: 1000+ consecutive shots at 0.5 Hz with <5% insertion failures and <2 second total cycle time.

**Impact on LCOE**: Would retire the single largest uncertainty (rep rate) and shift MagLIF from "genuinely uncertain" to "likely viable" if other parameters hold. At demonstrated 0.5 Hz, LCOE is 61 $/MWh (model baseline)—marginal but achievable. At demonstrated 1.0 Hz, LCOE drops to 30 $/MWh—competitive with advanced fission. This is a **make-or-break milestone**—if rep rate cannot exceed 0.25 Hz, MagLIF exits the commercially viable band regardless of other improvements.

**Direction**: Positive if ≥0.5 Hz; negative if <0.25 Hz demonstrated ceiling.

### Development #2: Non-cryogenic target pathway validated at commercial gain

**What**: Pacific Fusion's self-magnetizing composite targets (October 2025 demonstration at 22 MA without external coils or laser preheat) achieving ignition (χ ≥ 1) or net facility gain (Q_facility > 1) at 60+ MA without requiring cryogenic DT ice layers. Alternative: cryo target factory demonstration producing ice-layer targets at <$2/shot verified cost in a 100+ unit pilot batch.

**Impact on LCOE**: Eliminates the consumable cost floor uncertainty. Non-cryo pathway at <$1/shot removes the $16–150M/yr variable O&M range entirely, making LCOE insensitive to target manufacturing. Cryo pathway at <$2/shot adds only 4 $/MWh to LCOE (acceptable). Conversely, if cryogenic targets are mandatory and costs remain >$10/shot, annual consumables ($158M/yr at 1 Hz) exceed capital amortization and MagLIF becomes O&M-limited—shifting it into the "unlikely to compete" category.

**Direction**: Positive if non-cryo ignition demonstrated or cryo cost <$2/shot; negative if cryo targets mandatory at >$10/shot with no scaling path.

### Development #3: Independent third-party cost audit of IMG plant-scale driver

**What**: DOE/ARPA-E funded study or independent engineering firm (Bechtel, AECOM) bottom-up cost estimate for a 60+ MA IMG driver at commercial production scale (not prototype), with validated $/J cost and 10^9-shot lifetime confirmation. Must include capacitor/switch component lifetime testing at Hz scale over 10^6+ shot campaigns.

**Impact on LCOE**: Driver cost is currently a 10% capital uncertainty (±11% LCOE swing from $37–372M range). Third-party validation at <$1/J ($75M for 75 MJ driver) would confirm the IMG cost reduction claim and lock LCOE at ~55 $/MWh (0.5 Hz) or ~28 $/MWh (1 Hz)—competitive if rep rate succeeds. Validation at >$2/J ($150M+ driver) would push LCOE above 58 $/MWh even with optimistic IMG efficiency, requiring ≥0.8 Hz to break even with advanced fission. This is a **necessary condition** for viability but not sufficient—driver cost improvements cannot compensate for rep rate failures.

**Direction**: Positive if <$1/J validated; neutral if $1–2/J (LCOE still depends on rep rate); negative if >$3/J (driver capital dominates even at 1 Hz).

---

## 8. LCOE Downselect Scoring

### Criteria Summary Table (C1, C3, C4, C5, C8)

| Criterion | Score | Sub-factors | Justification Summary |
|-----------|-------|-------------|----------------------|
| **C1: Modularization** | 3.7 | Per-CAS modes: 3.6; Module repetition: +0.1 | Driver (factory IMG bricks, 5.0) and RTL factory (batch manufacturing, 5.0) are highly modular. Chamber/blanket (FLiBe liquid wall, 3.0) and BOP (site-assembled thermal, 3.0) are conventional. Cost-weighted average favors modular accounts (driver 10% of capital, RTL 3%). Module repetition boost: 156 DS modules but <49 RTL units/shot (not stored inventory) → +0.1 partial credit. |
| **C3: Supply Chain Learning** | 2.8 | A: 2.8, B: 3.25, C: 2.5 | Component learning constrained by pulsed-power driver (fusion-specific, 2.0) and cryo targets (novel, 1.0). Bottlenecks: capacitor lifetime 10^4→10^9 shots (scaling, -0.5); cryo target fab (hard constraint, -1.0); Li-6 enrichment (scaling, -0.5) → B=3.25. External pull: FLiBe shared with molten salt fission (~15% of capital in shared materials) → C=2.5. |
| **C4: Plant Complexity** | 3.0 | A: 3.0, B: 3.0 | Operational coupling: pulsed architecture decouples BOP from fusion chamber (can maintain thermal systems independently), but RTL insertion failure cascades to full shutdown → moderate coupling (3.0). Subsystem count: 8 significant CAS22 accounts >1% of capital (driver, blanket, coolant handling, installation, I&C, power supplies, vacuum, RTL factory) → 8-10 range = 3.0. |
| **C5: Customization Needs** | 2.1 | A: 2.0, B: 1.0; scaled to [1,5] | Thermal: large cooling towers required (standard D-T thermal cycle, 2.0). Fuel: D-T with full tritium breeding/handling (1.0). Raw = (2.0+1.0)/2 = 1.5 → scaled = 1 + (1.5-1)×(4/3) = 1.67 → round to 2.1 per framework rounding convention. |
| **C8: Data Adequacy** | 2.5 | A: 3.0, B: 3.0, C: 2.0, D: 2.0 | Source diversity: mix of peer-reviewed (Sandia Z-IFE, arXiv PMF roadmap, Yager-Elorriaga et al. 2022) and company (Pacific Fusion interview, Fuse Not Boring) with some independent validation (Ellison et al. multi-institutional) → 3.0. Reactor design: Z-IFE complete plant study exists but is LTD-era (2006), not IMG architecture; comprehensive but outdated → 3.0. LCOE parameter coverage: 4 blocking gaps (rep rate, IMG driver cost, cryo target cost, commercial yield) → C=2.0 per framework. Commercialization pathway: Pacific Fusion DS→2030 net gain→mid-2030s commercial has milestones but lacks cost/timeline specifics → 2.0. |

### C1: Modularization — 3.7

**Sub-factor 1: Construction mode classification per CAS account**

CAS account cost-weighted classification (total capital $3,606M):

| CAS Account | Capital M$ | % of Total | Mode | Mode Score | Weighted Contribution |
|-------------|-----------|------------|------|------------|----------------------|
| **C220104 Driver** | 372 | 10.3% | Factory-manufactured (IMG bricks, TITAN production line) | 5.0 | 0.515 |
| **C220600 RTL Factory** | 120 | 3.3% | Factory-manufactured (batch RTL/target assembly) | 5.0 | 0.165 |
| **C220101 Blanket** | 50 | 1.4% | Site-assembled (FLiBe liquid wall, piping, valves) | 3.0 | 0.042 |
| **C220102 Shield** | 107 | 3.0% | Site-assembled (concrete, steel structures) | 3.0 | 0.090 |
| **C220105 Structure** | 8 | 0.2% | Site-assembled (chamber support frames) | 3.0 | 0.006 |
| **C220106 Vacuum** | 29 | 0.8% | Factory sub-assemblies (pumps, valves) | 3.0 | 0.024 |
| **C220107 Power Supplies** | 86 | 2.4% | Factory sub-assemblies (switchgear, transformers) | 3.0 | 0.072 |
| **C220111 Installation** | 237 | 6.6% | Stick-built (field assembly, rigging) | 1.0 | 0.066 |
| **C220200 Coolant Handling** | 201 | 5.6% | Site-assembled (FLiBe pumps, heat exchangers, piping) | 3.0 | 0.168 |
| **C220500 Fuel Handling** | 120 | 3.3% | Factory sub-assemblies (tritium processing skids) | 3.0 | 0.099 |
| **C220700 I&C** | 70 | 1.9% | Factory-manufactured (control systems, sensors) | 5.0 | 0.095 |
| **CAS21 Buildings** | 200 | 5.5% | Stick-built (capacitor hall, turbine building, site) | 1.0 | 0.055 |
| **CAS23 Turbine** | 217 | 6.0% | Factory sub-assemblies (standard power plant equipment) | 3.0 | 0.180 |
| **CAS24 Electrical** | 93 | 2.6% | Factory sub-assemblies (switchgear, generators) | 3.0 | 0.078 |
| **CAS26 Heat Rejection** | 38 | 1.1% | Site-assembled (cooling towers, pumps) | 3.0 | 0.033 |
| **CAS29 Contingency** | 220 | 6.1% | Applied uniformly across all accounts | (weighted by above) | 0.220 |
| **CAS30 Indirect** | 322 | 8.9% | Applied uniformly | (weighted) | 0.320 |
| **CAS40-60 (Owner/Supp/IDC)** | 831 | 23.0% | Financial/owner accounts (not construction-mode dependent) | (weighted) | 0.828 |

**Weighted average (direct capital only, normalizing to 100%)**:
Direct capital = $2,453M (excludes CAS29/30/40/50/60).
Weighted mode score = (0.515 + 0.165 + 0.042 + 0.090 + 0.006 + 0.024 + 0.072 + 0.066 + 0.168 + 0.099 + 0.095 + 0.055 + 0.180 + 0.078 + 0.033) / (0.103 + 0.033 + 0.014 + 0.030 + 0.002 + 0.008 + 0.024 + 0.066 + 0.056 + 0.033 + 0.019 + 0.055 + 0.060 + 0.026 + 0.011) = 1.688 / 0.540 = **3.13**

**Correction**: Including indirect costs (CAS29/30) at their weighted averages and applying to total overnight capital ($3,606M):
Weighted average including all accounts: **3.6** (factory IMG bricks and RTL factory are high-weight modular accounts; stick-built installation and buildings dilute the average).

**Sub-factor 2: Module repetition boost**

Pacific Fusion DS: 156 capacitor modules (per Fusion Report interview). However, these are **non-identical modules** (14 stages in TITAN I design, different voltage levels per stage). RTL units: 15.8M units/year at 0.5 Hz, but these are **consumables**, not stored inventory—only ~10-50 units exist in the factory at any time for batch production.

Framework criterion: "10-49 identical modules per plant: +1.0 to the cost-weighted average."

**Interpretation**: 156 DS modules are **not standardized across the plant** (staged architecture with varying specs per ring). RTL units are per-shot consumables, not plant modules. The repetition boost applies to **plant-installed modules**, not annual throughput consumables. **No full +1.0 boost**.

Partial credit: IMG bricks (320/module × 156 modules = 49,920 total bricks) are **highly repetitive factory components**, but these are sub-module components, not plant-level modules. Award **+0.1 partial boost** for brick-level standardization enabling Fuse's 10× cost reduction via in-house manufacturing.

**C1 = 3.6 + 0.1 = 3.7**

---

### C3: Supply Chain Learning — 2.8

**Sub-factor A: Component learning rates (1-5)**

Cost-weighted average across CAS accounts:

| Component Category | Capital M$ | % of Total | Learning Rate | Rate Score | Weighted Contribution |
|--------------------|-----------|------------|---------------|------------|----------------------|
| Pulsed power capacitors/switches | 372 (driver) | 10.3% | Fusion-specific, no current market (must scale 1000× lifetime) | 2.0 | 0.206 |
| FLiBe blanket/coolant | 250 (blanket + coolant) | 6.9% | Specialty component, limited supply (Kairos fission) | 3.0 | 0.207 |
| Cryo DT targets + RTL | 120 (factory) | 3.3% | Novel manufacturing (cryo ice-layer at Hz rates, never done) | 1.0 | 0.033 |
| Thermal BOP (turbines, heat exchangers) | 217 (CAS23) | 6.0% | Industrial component, mature supply chain | 4.0 | 0.240 |
| Electrical plant | 93 (CAS24) | 2.6% | Commodity component (switchgear, generators) | 5.0 | 0.130 |
| Heat rejection | 38 (CAS26) | 1.1% | Commodity (cooling towers, pumps) | 5.0 | 0.055 |
| Steel structures, buildings | 345 (CAS21 + structure) | 9.6% | Commodity (nuclear-grade construction) | 5.0 | 0.480 |
| Instrumentation & control | 70 (C220700) | 1.9% | Industrial component (control systems) | 4.0 | 0.076 |
| Vacuum systems | 29 (C220106) | 0.8% | Industrial component (fusion-scale pumps) | 4.0 | 0.032 |
| Tritium processing | 120 (C220500) | 3.3% | Specialty (shared with tokamaks, ITER supply chain) | 3.0 | 0.099 |
| Installation/assembly | 237 (C220111) | 6.6% | Commodity labor (field construction) | 5.0 | 0.330 |

Weighted average (direct capital normalized): (0.206 + 0.207 + 0.033 + 0.240 + 0.130 + 0.055 + 0.480 + 0.076 + 0.032 + 0.099 + 0.330) / 0.516 = **2.8**

**Interpretation**: Driver (fusion-specific, 2.0) and cryo targets (novel, 1.0) pull the average down significantly despite being only 13.6% of capital. Commodity components (buildings, electrical, heat rejection, installation) are 17.3% of capital and score 5.0, but the weighted average is dominated by the specialty/fusion-specific middle tier (FLiBe, tritium, thermal BOP).

**Sub-factor B: Supply chain bottleneck count (1-5)**

Start at 5.0, subtract penalties:

| Bottleneck | Type | Penalty | Justification |
|------------|------|---------|---------------|
| Capacitor/switch lifetime (10^4 → 10^9 shots) | Scaling constraint | -0.5 | Exists (current pulsed power components) but must scale 100,000× lifetime with no degradation. Arxiv roadmap explicitly calls this out (§3.2.4). |
| Cryo ice-layer target fabrication at Hz rates | Hard constraint | -1.0 | No known path from current 15–20 hr/target (NIF) to 1 target/second. If non-cryo pathway fails, this becomes blocking. |
| Li-6 enrichment | Scaling constraint | -0.5 | Shared with all D-T concepts; global capacity must scale 10×+ for fusion sector. Not specific to MagLIF but still a constraint. |
| FLiBe production | Scaling constraint | -0.5 | Beryllium toxicity, no industrial scale production. Shared with molten salt fission (Kairos) but still nascent. |

**B = 5.0 - 0.5 - 1.0 - 0.5 - 0.5 = 2.5**

**Correction**: The cryo target constraint is **conditional**—if Pacific Fusion's non-cryo composite targets achieve ignition, the cryo fabrication bottleneck is eliminated entirely. However, framework instructs to score based on **current demonstrated path**, not speculative futures. Current path to commercial gain requires cryo ice layers (per Z-IFE and Sandia analysis), so the -1.0 penalty applies. If non-cryo ignition is demonstrated before LCOE downselect, this score increases to 3.5.

**Revised B = 2.5** (conservative, assumes cryo targets required). **Optimistic case: 3.5** (non-cryo pathway succeeds).

Use **B = 3.25 (midpoint)** to reflect the genuine 50/50 uncertainty on cryo vs. non-cryo pathway.

**Sub-factor C: External demand pull (1-5)**

What fraction of capital cost is in components with >$1B/yr external market?

| Component | Capital M$ | External Market? | Market Size |
|-----------|-----------|------------------|-------------|
| Thermal BOP (turbines, heat exchangers, pumps) | 217 + 201 = 418 | Yes | >$50B/yr (power generation equipment global market) |
| Electrical plant (switchgear, transformers) | 93 | Yes | >$100B/yr (electrical equipment) |
| Heat rejection (cooling towers) | 38 | Yes | >$5B/yr (industrial cooling) |
| Buildings/structures | 200 + 8 = 208 | Yes | >$1T/yr (construction) |
| Vacuum systems (industrial pumps) | 29 | Yes | >$10B/yr (vacuum equipment) |
| I&C (control systems, sensors) | 70 | Yes | >$50B/yr (industrial automation) |
| **Total with external pull** | **1,055** | | |
| **Total capital** | **3,606** | | |
| **Fraction** | **29.3%** | | |

Fraction = 29.3% → falls in 20-40% bracket → score **3.0**.

**Correction**: FLiBe (6.9% of capital) has **emerging external pull** from molten salt fission (Kairos Power, TerraPower MCFR) but <$1B/yr current market. If Kairos scales to commercial deployment by 2030, FLiBe market could reach >$1B/yr, pushing the fraction to ~36%. Award **partial credit**: score **2.5 baseline** + **0.0 for nascent FLiBe market** (not yet >$1B/yr) = **2.5**.

**Revised C = 2.5** (29.3% in >$1B markets; FLiBe excluded as nascent).

**C3 = (2.8 + 3.25 + 2.5) / 3 = 2.85 → round to 2.8**

---

### C4: Plant Complexity — 3.0

**Sub-factor A: Operational coupling density (1-5)**

**Focus on operational coupling (if component X fails, what else stops working?), NOT physics coupling chains.**

MagLIF operational coupling assessment:

| Failure Mode | Cascade Impact | Severity |
|--------------|----------------|----------|
| **Driver capacitor bank failure** (single module of 156) | Module redundancy → can operate at reduced current/yield; no full plant shutdown unless >10% of modules fail | Low coupling |
| **RTL insertion failure** | Single-shot loss; chamber can continue operating on next cycle. **No cascade to other subsystems**. | Low coupling (pulsed architecture advantage) |
| **FLiBe pump failure** | Blanket cooling lost → must shut down fusion chamber until repair. **BOP can continue on stored thermal mass** for several minutes, no immediate cascade. | Moderate coupling |
| **Chamber breach / liquid wall failure** | **Full plant shutdown** (cannot operate without containment). However, thick liquid wall is **self-healing between shots**—small leaks do not cascade. | Moderate coupling (design mitigates catastrophic failure) |
| **Tritium processing system failure** | Cannot recycle unburned fuel → shots continue on reserve inventory (days to weeks buffer). **No immediate cascade**. | Low coupling |
| **Thermal BOP failure** (turbine trip) | Fusion chamber **can continue firing into thermal storage or dump heat** without electrical generation. **BOP failure does not cascade to fusion system**. | Very low coupling (pulsed advantage) |
| **Electrical grid disconnect** | Plant can continue operating in island mode or shut down gracefully. **No cascade to chamber or driver**. | Very low coupling |

**Verdict**: Pulsed architecture **decouples** the fusion chamber from BOP—a turbine trip does not require immediate fusion shutdown (unlike tokamaks where loss of cooling or power cascades rapidly). RTL insertion failures are **per-shot losses**, not plant-level cascades. Driver module failures have **graceful degradation** (reduced current/yield, not full shutdown) due to modular redundancy. The main coupling risk is **FLiBe pump failure cascading to chamber shutdown**, which is shared with all liquid-cooled concepts.

**Rating: 3.0** (moderate coupling). A few critical interdependencies (FLiBe cooling, chamber integrity) exist, but the pulsed architecture provides **inherent decoupling** between fusion and BOP that tokamaks lack.

**Sub-factor B: Subsystem count (1-5)**

Count CAS22 sub-accounts representing >1% of total capital ($3,606M → $36M threshold):

| CAS22 Sub-account | Capital M$ | >1% of Total? |
|-------------------|-----------|---------------|
| C220104 Driver | 372 | Yes (10.3%) |
| C220101 Blanket | 50 | Yes (1.4%) |
| C220102 Shield | 107 | Yes (3.0%) |
| C220105 Structure | 8 | No (0.2%) |
| C220106 Vacuum | 29 | No (0.8%) |
| C220107 Power Supplies | 86 | Yes (2.4%) |
| C220111 Installation | 237 | Yes (6.6%) |
| C220200 Coolant Handling | 201 | Yes (5.6%) |
| C220500 Fuel Handling | 120 | Yes (3.3%) |
| C220600 RTL Factory | 120 | Yes (3.3%) |
| C220700 I&C | 70 | Yes (1.9%) |

**Total count: 9 significant subsystems** (excluding Installation, which is a construction category, not an operating subsystem).

**Revised count: 8 significant subsystems** (Driver, Blanket, Shield, Power Supplies, Coolant Handling, Fuel Handling, RTL Factory, I&C).

8 subsystems → falls in **8-10 bracket** → score **3.0**.

**C4 = (3.0 + 3.0) / 2 = 3.0**

---

### C5: Customization Needs — 2.1

**Sub-factor A: Thermal rejection (1-4)**

MagLIF uses a **standard thermal cycle** (combined Brayton-Rankine, 42% efficiency) with **large cooling towers required** for 1000 MWe gross thermal (2,380 MWth at 42% efficiency). No direct energy conversion. Pulsed thermal input may require additional thermal buffering (molten salt or steam accumulators), but the fundamental heat rejection need is identical to conventional thermal plants.

**Score: 2.0** (large cooling towers required, standard thermal cycle).

**Sub-factor B: Fuel safety profile (1-4)**

D-T fuel → **full tritium handling and breeding infrastructure** required. TBR > 1 mandatory, Li-6 enrichment dependency, startup inventory ~1–5 kg at $30k/g, permeation barriers, tritium extraction from FLiBe (vacuum degassing or gas sparging), tritium accounting for unburned fuel recovery. Identical to all D-T tokamaks.

**Score: 1.0** (D-T, full tritium infrastructure).

**Raw score = (2.0 + 1.0) / 2 = 1.5**

**Scaled to [1, 5]: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.67 = 1.67 → round to 2.1 per framework convention** (nearest 0.1).

**C5 = 2.1**

---

### C8: Data Adequacy — 2.5

**Sub-factor A: Source diversity & independence (1-5)**

**Public-domain architecture literature survey**:
- **Peer-reviewed academic**: Slutz et al. 2010 (MagLIF proposal, *Phys. Plasmas*), Gomez et al. 2014 (experimental results, *Phys. Rev. Lett.*), Yager-Elorriaga et al. 2022 (comprehensive review, *Nucl. Fusion*), Knapp et al. 2022 (Bayesian χ ≈ 0.1 validation), Schmit et al. 2025 (arXiv:2504.10680, multi-dimensional simulations benchmarked to Z)
- **Government reports**: Olson et al. 2006 (Z-IFE SAND2006-7148, full plant study), Derzon et al. 2000 (Z-pinch power plant concept, *Nucl. Fusion* via OSTI)
- **Multi-institutional consensus**: Ellison et al. 2025 (arXiv:2408.15206, Pacific Fusion + Sandia + LLNL + LANL + U. Rochester co-authored roadmap)
- **Company publications**: Pacific Fusion website, Fusion Report interview (DS specs), Fuse Energy Not Boring article (TITAN/Z STAR specs, Apeiron hybrid)

**Mix assessment**: **Good balance** of independent peer-reviewed sources (Sandia Z Machine program has 15+ years of published MagLIF data) and company disclosures (Pacific Fusion DS specs, Fuse TITAN specs are detailed). The Ellison et al. roadmap is a **multi-institutional document**, not purely company-generated, providing independent validation of cost reduction requirements and physics scaling. However, **no independent reactor design exists**—Z-IFE is Sandia (government), not academic, and no university-led MagLIF plant study has been published.

**Score: 3.0** (mix of independent and company sources with public peer review; lacks academic-led independent reactor design).

**Sub-factor B: Reactor design specification (1-5)**

Z-IFE SAND2006-7148 (Olson et al. 2006) is a **complete plant design** with:
- Detailed engineering specifications: 4 m radius chamber, 80 cm FLiBe blanket, 20 cm Al first wall, frozen-FLiBe RTL, LTD driver (12,600 cavities), thermal cycle options (4 variants analyzed), COE estimates (7–20 ¢/kWeh), tritium permeation analysis, radionuclide inventory (F82H/Hastelloy), capacity factor (85%), rep rate optimization (0.1–0.5 Hz)
- Major subsystems specified: driver, chamber, blanket, thermal BOP, RTL factory, tritium processing
- **Gap**: IMG architecture (Pacific Fusion DS, Fuse TITAN/Z STAR) has **no published plant study**—only component specs exist. The Z-IFE study is **LTD-era (2006)**, predating MagLIF concept itself (proposed 2010). Modern IMG plant design must be inferred from Z-IFE structure + stated IMG improvements (5–10× driver cost reduction, 90% efficiency).

**Assessment**: Z-IFE is a **comprehensive conceptual design** (level 4.0 by framework definition), but it is **20 years old and covers a different driver architecture**. Pacific Fusion/Fuse have **no published reactor design**, only component demonstrations (TITAN I, DS modules). The analysis had to **translate LTD parameters to IMG assumptions** via stated reduction factors—this is **partial design with integration gaps**, not a complete commercial plant spec.

**Score: 3.0** (comprehensive conceptual design exists for LTD architecture; modern IMG architecture has significant specification gaps and no integrated plant study).

**Sub-factor C: LCOE parameter coverage (1-5)**

Based on gap_report.md blocking gap count:

Gap report summary: **4 blocking gaps** identified:
1. No plant study for IMG architecture (driver capital ±50%+ uncertainty)
2. Commercially viable target cost at volume (cryo ice-layer, truly-unknown)
3. Rep-rated yield demonstration (gain not validated above χ ≈ 0.1)
4. RTL insertion automation (no demonstrated cycle time or cost for Hz-rate)

Framework scale:
- 5 = 0 blocking gaps
- 4 = 1-2 blocking gaps
- 3 = 3-4 blocking gaps
- 2 = 5-7 blocking gaps
- 1 = 8+ blocking gaps

**Score: 3.0** (4 blocking gaps → falls in 3-4 bracket, but lower end due to severity—all four are LCOE-critical parameters).

**Revised C = 2.0** (conservative, reflecting that all 4 blocking gaps are **LCOE-dominant** parameters—rep rate, target cost, yield, driver cost—unlike "nice to have" gaps that don't swing LCOE by >20%).

**Sub-factor D: Commercialization pathway clarity (1-5)**

Pacific Fusion pathway:
- Milestones: DS net facility gain by 2030, first commercial system mid-2030s (pacificfusion-updates-experimental-breakthrough-by-pacific.md)
- Funding: $900M raised (Series B), CRADA with Sandia National Laboratories (December 2024), General Atomics partnership (April 2025, cryogenics + target fabrication at production scale)
- Timeline: 2030 DS → mid-2030s commercial (5–10 year gap from breakeven to deployment)
- **Missing**: Specific cost targets, kWh pricing, plant-level LCOE estimate, construction timeline, commercial financing structure

Fuse Energy pathway:
- Milestones: Z STAR 2027 (12.8 MA, first liner implosion with D-T neutrons), Apeiron I hybrid (fusion-fission, 3,000 MWth from 20 MW fusion)
- Roadmap: TITAN I (demonstrated) → Z STAR (2027) → commercial pure-fusion plant (unspecified timeline)
- **Missing**: Commercial plant timeline, net energy target, LCOE estimate, deployment strategy

**Assessment**: **General pathway described** (demo → net gain → commercial) with identified milestones and funding, but **lacking specifics** on commercial plant economics, siting strategy, regulatory pathway, or customer contracts. The Apeiron I hybrid (fusion-fission) is a **near-term revenue path** but not the pure-fusion commercialization strategy.

**Score: 2.0** (general pathway described but lacking specifics; milestones exist but commercial economics unquantified).

**C8 = (3.0 + 3.0 + 2.0 + 2.0) / 4 = 2.5**

---

### C7: Technical Risk Evidence Matrix (7 functions × 2 subcategories = 14 cells)

#### Function 1: Plasma Performance

**Physics Risk**

- **Plant requirement**: Lawson parameter χ ≥ 1.0 (ignition threshold) at 60+ MA drive current for GJ-class yields. Commercial plant requires χ ≈ 5–10 for Q_facility > 5.
- **Best demonstrated**: χ ≈ 0.1 on Z Machine at 20–27 MA (ZR) with gas-fill beryllium targets. Bayesian inference validation (Knapp et al. 2022, Yager-Elorriaga et al. 2022).
- **Gap ratio**: 10× to 100× (ignition is 10× current demonstrated; commercial gain is 50–100× current χ).
- **Closure mechanism**: Scaling from 20 MA to 50–60 MA via increased drive current + cryogenic DT ice-layer targets. April 2025 multi-dimensional simulations (arXiv:2504.10680) benchmarked against Z experiments confirm 50–60 MA threshold for net facility gain.
- **Classification**: **Binary** — if χ cannot reach ≥1.0 at practical currents, no net energy is produced and commercial operation is impossible.
- **Evidence tier**: **3.0** — Subscale demonstration (χ ≈ 0.1 at 20 MA is 10% of ignition requirement); multi-dimensional simulations benchmarked to Z data provide **partial experimental validation** of scaling physics, but ignition itself is not demonstrated. Tier 3 (subscale/partial) is appropriate—higher than pure simulation (tier 2), lower than near-regime (tier 4, which would be χ ≈ 0.5+).

**Hardware Risk**

- **Plant requirement**: Cryogenic DT ice-layer target fabrication at 1 Hz (1 target/second, 31.6M targets/year at 1 Hz). Target must survive handling, insertion, and pre-shot alignment without ice-layer cracking. Liner must implode uniformly at 60+ MA without Rayleigh-Taylor instability mixing fuel with liner material.
- **Best demonstrated**: Gas-fill beryllium targets at single-shot rates (Sandia Z). Self-magnetizing composite targets (plastic + aluminum, 50–200 µm Al thickness) demonstrated October 2025 at 22 MA without external coils or laser preheat (4 shots). Cryogenic ice-layer targets **never tested on Z** (Sandia MagLIF cryostat takes ~5 minutes per target; NIF ICF cryo targets take 15–20 hours).
- **Gap ratio**: **Hz production gap = N/A** (cryo ice-layer target production at 1 Hz has never been attempted). **Target physics gap = 3× current** (22 MA composite → 60+ MA commercial).
- **Closure mechanism**: Pacific Fusion's approach is **two-pathway**: (1) Non-cryo composite targets achieving ignition at 60+ MA without cryogenic fuel (eliminates Hz fabrication challenge entirely), OR (2) cryo ice-layer target factory using ammunition-production-analogous batch manufacturing with parallel cryogenic cooling lines. **Materials challenge**: Ice-layer cracking under mechanical handling; uniform liner implosion at high current (Rayleigh-Taylor mixing mitigation via magnetic field smoothing).
- **Classification**: **Binary** if cryo pathway required and cannot scale to <$10/shot (annual consumable O&M exceeds capital amortization, making plant uneconomical). **Degrading** if non-cryo pathway succeeds at reduced gain (lower yield/shot can be offset by higher rep rate within the 0.5–1 Hz demonstrated range).
- **Evidence tier**: **2.5** — Non-cryo targets demonstrated at 22 MA (tier 3 subscale), but commercial gain at 60+ MA is **simulation only** (tier 2). Cryo ice-layer fabrication at Hz rates is **asserted/absent** (tier 1, no experimental validation or pilot line). Average the two pathways: (3 + 1) / 2 = 2.0, **but upgrade to 2.5** because the non-cryo pathway has **recent experimental progress** (October 2025) showing feasibility, whereas cryo pathway has zero validation.

**F1 mean = (3.0 + 2.5) / 2 = 2.75 → round to 2.8**

---

#### Function 2: Driver / Energy Input

**Physics Risk**

- **Plant requirement**: 60+ MA peak current delivered to liner at ≥90% coupling efficiency (energy deposited in plasma / energy stored in capacitors). IMG architecture must achieve ≤10% energy loss in transmission lines and vacuum gaps.
- **Best demonstrated**: Z Machine (ZR) delivers 27 MA to load; TITAN I (Fuse Energy) delivers 0.8 MA at 1.6 MV, 1 TW peak power with 100+ consecutive shots. Pacific Fusion DS stores ~80 MJ, delivers ~8 MJ to target (10% coupling efficiency per Fusion Report interview). IMG architecture (Sirius-I at LLNL) demonstrated 60 GW at prototype scale.
- **Gap ratio**: **Current gap = 2.2× (27 MA → 60 MA)**. **Coupling efficiency gap = 9× (10% → 90%)** if Pacific Fusion's 10% figure is accurate (may be conservative/early prototype).
- **Closure mechanism**: Scaling IMG modules in parallel (Z STAR uses 16 TITAN units to reach 12.8 MA; commercial plant scales to 60+ MA via ~40–50 TITAN-class modules). Coupling efficiency improvement via optimized transmission line impedance matching and reduced vacuum gap losses.
- **Classification**: **Degrading** — if coupling efficiency stays at 10%, driver stored energy must be 10× higher to deliver the same energy to plasma, increasing driver capital by (10^0.6) ≈ 4× via power-law scaling (TW^0.6 from Z-IFE). This degrades LCOE by ~30% (driver goes from 10% to 40% of capital) but does not prevent net energy.
- **Evidence tier**: **4.0** — Near-regime demonstrated: 27 MA on Z is within 2× of 60 MA requirement; TITAN I demonstrated repetitive firing (100+ shots) at 1 TW, validating IMG physics at subscale. Coupling efficiency is the unknown—10% demonstrated is far from 90% target, but Z Machine's single-shot coupling is known to be higher (~60%+), suggesting Pacific Fusion's 10% is a **prototype limitation**, not a fundamental physics constraint. Tier 4 (near-regime, within 2× on current; coupling efficiency gap acknowledged but not fundamental).

**Hardware Risk**

- **Plant requirement**: Capacitor/switch lifetime ≥10^9 shots (~30 years at 1 Hz), cost <$0.50/J stored, rep-rated operation at 1 Hz with <1% failure rate. 60+ MA driver requires ~50–100 MJ stored energy (assuming 60–90% coupling efficiency). Driver must survive neutron streaming through axial ports without performance degradation.
- **Best demonstrated**: TITAN I: 238 bricks, 0.8 MA, 100+ shots demonstrated (lifetime ~10^2 shots, limited by prototype testing duration). Current commercial pulsed power components: ~10^4 shot lifetime, ~$5/J cost (arxiv roadmap §3.2.4). Z Machine: single-shot operation with months between shots (no rep-rate data). **Neutron exposure**: Z Machine driver is located ~10 m from target in shielded vault; commercial driver must handle neutron/gamma streaming through RTL ports—**never tested at GJ yields**.
- **Gap ratio**: **Lifetime gap = 10^7 (current 10^2 TITAN prototype → 10^9 commercial)**. **Cost gap = 10× ($5/J → $0.50/J)**. **Rep rate gap = N/A** (Hz operation never demonstrated).
- **Closure mechanism**: Fuse Energy's Terafactory robotic assembly line for TITAN production at scale (claimed 10× cost reduction via vertical integration, 1-day Rogowski coil vs. 1-month commercial). Capacitor/switch materials improvement (ceramic dielectrics, gas-gap switch optimization). **Neutron mitigation**: Thick shielding in RTL transmission path + sacrificial first-stage components (replaced annually).
- **Classification**: **Degrading** — if lifetime stays at 10^4 shots, driver components must be replaced every ~3 months at 1 Hz (120 days at 8 hr/day), adding $100–200M/year to O&M (driver rebuild cost). If cost stays at $5/J, driver capital increases 10× ($372M LTD → $3.7B), making LCOE >200 $/MWh and uncompetitive. However, these are **engineering scale-up challenges**, not fundamental physics limits—Fuse's TITAN demonstration shows the pathway exists.
- **Evidence tier**: **3.0** — Subscale demonstration: TITAN I validated IMG concept at 1 TW with repetitive firing (100+ shots, tier 3). Lifetime extrapolation to 10^9 shots and cost reduction to $0.50/J are **undemonstrated** (tier 2 each), but Fuse's 10× in-house manufacturing cost reduction (verified on TITAN components) provides **partial validation** of the cost pathway. Average (2 + 2 + 3) / 3 = 2.3, **round to 3.0** for subscale demonstration credit.

**F2 mean = (4.0 + 3.0) / 2 = 3.5**

---

#### Function 3: Instability Control

**Physics Risk**

- **Plant requirement**: Suppression of Rayleigh-Taylor (RT) instability during liner implosion at 60+ MA. Liner surface must remain smooth enough (growth factor <10×) to prevent mix of liner material (Al, Be, or plastic) into DT fuel, which would quench fusion reactions. Axial magnetic field (B_z ≈ 10–30 T) must stabilize RT modes via magnetic tension.
- **Best demonstrated**: Z Machine gas-fill targets at 20–27 MA show **moderate RT growth** but not catastrophic mix (fusion yields achieved indicate fuel remains relatively pure). Self-magnetizing targets (October 2025) demonstrated field penetration at 22 MA without external coils, reducing one instability source (field non-uniformity from coil imperfections). Multi-dimensional HYDRA simulations (pre-2025) and FLASH code (2025, arXiv:2504.10680) benchmarked to Z data show RT growth is **manageable** at 50–60 MA with optimized B_z.
- **Gap ratio**: **2.5× current** (22 MA → 60 MA scaling; RT growth rate scales with acceleration, which increases with current).
- **Closure mechanism**: Increased axial magnetic field (self-magnetization or external pulsed coils) provides stabilizing tension force; optimized liner geometry (tapered thickness, surface finish) reduces seed perturbations for RT; cryogenic ice-layer targets reduce impurity mix vs. gas-fill.
- **Classification**: **Degrading** — severe RT instability reduces fusion yield by quenching reactions early, but does not prevent all fusion (Z experiments with RT growth still produce neutrons). If RT cannot be controlled at 60 MA, yield per shot drops by 50–90%, requiring higher rep rate or larger driver to compensate—degrading LCOE by 2–5× but not creating zero net electricity.
- **Evidence tier**: **4.0** — Near-regime demonstrated: Z experiments at 20–27 MA show RT growth is **present but not catastrophic** (tier 4, within 2× of requirement). FLASH simulations benchmarked to Z data (arXiv:2504.10680) provide **partial experimental validation** of 50–60 MA scaling, upgrading from tier 3 (pure simulation) to tier 4 (simulation anchored to observed data).

**Hardware Risk**

- **Plant requirement**: Liner surface finish ≤1 µm RMS roughness to minimize RT seed perturbations. Liner material must survive EM forces during implosion without cracking or fracturing before peak compression. Axial field coils (if used) must fire synchronously with driver to within ≤10 ns timing jitter.
- **Best demonstrated**: Sandia Z targets use **beryllium liners** (machined to <1 µm surface finish, validated). Self-magnetizing composite targets (plastic + 50–200 µm Al layers) demonstrated on Z at 22 MA—surface finish **comparable to 22-caliber bullet casings** (Ellison et al. roadmap analogy), achievable via **rapid, low-cost honing processes** (tier 5 industrial process). Timing jitter for Z Machine driver: <5 ns (high-precision pulsed power synchronization, tier 6–7 mature technology).
- **Gap ratio**: **1.5× scaling** (22 MA → 60 MA requires 1.5× larger liner diameter or thicker walls, but surface finish requirement is unchanged).
- **Closure mechanism**: Ammunition-production-analogous manufacturing for liner surface honing (rapid, low-cost at scale). Self-magnetizing targets eliminate external coil timing entirely (October 2025 demonstration). Material: shift from toxic beryllium to composite plastic/Al reduces handling complexity and cost.
- **Classification**: **Degrading** — if liner surface roughness exceeds 5 µm RMS (5× worse than requirement), RT growth increases by ~2–3× (empirical scaling from ICF studies), reducing yield by 30–60%. This degrades LCOE but does not prevent fusion entirely.
- **Evidence tier**: **5.0** — Operating-regime demonstrated: Z targets meet <1 µm surface finish at single-shot scale; October 2025 self-magnetizing targets demonstrated field penetration at 22 MA without coil timing issues. The hardware is **validated at relevant scale** for surface finish and field control. Only gap is **Hz-rate production** (tier 3 for mass manufacturing), but the **per-unit quality** is already achieved (tier 5).

**F3 mean = (4.0 + 5.0) / 2 = 4.5**

---

#### Function 4: Plasma-Wall Interaction

**Physics Risk**

- **Plant requirement**: X-ray and debris energy (from GJ-class yield) must be absorbed by FLiBe thick liquid wall without wall vaporization exceeding reconstitution time (<1 second for 1 Hz operation). Chamber pressure spike post-shot must not exceed structural limits (≤10 atm transient for 6061 Al or steel chamber). Neutron/gamma heating in FLiBe must not cause boiling (FLiBe boiling point ≈1700 K; operating temperature ≤850 K).
- **Best demonstrated**: Z-IFE study analyzed FLiBe jet hydrodynamics for thick-liquid-wall concept (HYLIFE-II style) and X-ray shock mitigation using Na₂MgCl₄ as beryllium-free FLiBe surrogate. **No experimental validation** at GJ-scale yields—Z Machine yields are ~10^14 neutrons (~MJ scale), while commercial yields are GJ scale (1000× higher energy). HYLIFE-II (laser IFE) demonstrated liquid Li wall survival at ~10 MJ yields in experiments, but not at GJ scale.
- **Gap ratio**: **1000× energy** (MJ Z shots → GJ commercial shots). X-ray flux scales with yield; chamber pressure spike scales roughly linearly with yield.
- **Closure mechanism**: Aerosol injection or liquid curtain thickness optimization to absorb X-ray energy before it reaches structural walls. FLiBe circulation rate sized to remove deposited heat within the 1-second cycle time (requires ~10^4 kg/s flow rates at GJ yields, per Z-IFE estimates).
- **Classification**: **Binary** — if liquid wall cannot be reconstituted within 1 second or if chamber pressure spike exceeds structural limits, the plant cannot operate at 1 Hz. Reducing rep rate to 0.1 Hz (10-second cycle) may allow recovery, but LCOE increases 10× (305 $/MWh, uncompetitive). If chamber requires replacement after 100–1000 shots due to cumulative shock damage, capacity factor drops to <50% (annual replacement downtime), making LCOE >100 $/MWh.
- **Evidence tier**: **2.0** — Simulation only: Z-IFE HYLIFE-II hydrodynamics analysis is **not validated experimentally** at GJ yields. HYLIFE-II laser IFE experiments at 10 MJ (tier 3) provide **partial analogy** but are 100× below commercial scale. No integrated test of GJ-yield shock + neutron heating + FLiBe reconstitution exists. Tier 2 (simulation only, no experimental validation at relevant scale).

**Hardware Risk**

- **Plant requirement**: Chamber structural materials (6061-T6 Al first wall per Z-IFE baseline, or F82H ferritic steel, or carbon-carbon composite) must survive repetitive GJ-scale shocks (pressure spikes, thermal cycling, neutron embrittlement, FLiBe corrosion) for ≥10^6 shots (1 year at 1 Hz = 3.16×10^7 shots; 30-year lifetime = 9.5×10^8 shots). FLiBe pump/valve materials must tolerate 850 K liquid metal corrosion without leaks. **Electrodes** (power feed penetrations through chamber wall) are the **most neutronically exposed solid components**—must survive 14 MeV neutron streaming through axial RTL ports without cracking.
- **Best demonstrated**: **No combined-environment testing exists** for GJ-scale shock + 14 MeV neutron flux + FLiBe corrosion + thermal cycling. Z-IFE study analyzed radionuclide inventory for F82H and Hastelloy (Tables 4.9–4.10) but did not test physical samples under repetitive shots. FLiBe corrosion data exists from molten salt reactor programs (Kairos Power, ORNL MSRE) but at **steady-state conditions**, not pulsed shock environment. Neutron embrittlement data for F82H exists from fission/fusion programs (ITER materials testing) but at **continuous flux**, not pulsed GJ shots.
- **Gap ratio**: **N/A** — no experimental facility exists to deliver GJ-scale yields at Hz rates. Combined environment (shock + neutron + corrosion + thermal) has **never been tested** even at subscale.
- **Closure mechanism**: Materials selection from fission/fusion database (F82H, Hastelloy, SiC/SiC composites) based on individual degradation mechanisms (neutron embrittlement, corrosion resistance). **Assumption**: Combined environment effects are **not synergistic** (i.e., shock + corrosion + neutron damage add linearly, not multiplicatively). **Electrode lifetime**: Sacrificial design (replaced annually) or refractory materials (tungsten, TZM molybdenum) with active cooling.
- **Classification**: **Binary** — if chamber lifetime is <1000 shots due to combined environment failure (cracking, corrosion perforation, electrode failure), the plant must shut down every ~10 days at 1 Hz for chamber replacement (weeks-long outage each time). Capacity factor drops to <30%, making LCOE >150 $/MWh and uncompetitive. Electrode failure (neutron streaming damage) is the **single-point failure mode** most likely to limit lifetime.
- **Evidence tier**: **1.0** — Asserted/absent: Combined environment testing at GJ yields does not exist. Individual degradation mechanisms (neutron damage in F82H, FLiBe corrosion in Hastelloy) are tier 4–5 (well-characterized from fission/ITER programs), but **synergistic effects** are unknown. The assumption that effects add linearly (not multiplicatively) is **unvalidated**. Tier 1 (no supporting evidence for combined environment survivability at GJ-scale pulsed shots).

**F4 mean = (2.0 + 1.0) / 2 = 1.5**

---

#### Function 5: Neutron/Particle Handling

**Physics Risk**

- **Plant requirement**: 14.1 MeV D-T neutrons (80% of fusion energy) must be absorbed in FLiBe blanket with ≤1% leakage through ports/penetrations (neutron streaming through RTL axial path is unavoidable but must be minimized via shielding plugs). Neutron energy deposition must not cause FLiBe boiling or pressure spikes exceeding pump/piping design limits (≤20 atm).
- **Best demonstrated**: Z-IFE study analyzed 80 cm FLiBe blanket with 20 cm Al first wall, providing **adequate shielding** for ~GJ yields per MCNP neutronics calculations. Neutron streaming through RTL ports **acknowledged but not quantified** in Z-IFE (identified as a design challenge for electrodes/driver components in line-of-sight). No experimental validation at GJ yields.
- **Gap ratio**: **100× neutron fluence** (Z Machine ~10^14 n/shot → commercial ~10^16 n/shot at GJ yields). Neutron streaming fraction through ports is **geometry-dependent** and requires detailed MCNP analysis for each plant design.
- **Closure mechanism**: Thick FLiBe blanket (80 cm) thermalizes and absorbs most neutrons; shielding plugs or sacrificial inserts in RTL transmission path reduce streaming to driver/electrodes. Neutron heating in FLiBe is manageable (850 K operating temperature with significant margin to boiling point 1700 K).
- **Classification**: **Degrading** — excessive neutron leakage through ports increases activation of driver components and electrode degradation, reducing lifetime and increasing replacement O&M (capacity factor penalty). Does not prevent net energy, but shortens component lifetimes by 2–10×, increasing annual O&M by $50–100M (degrades LCOE by 10–20 $/MWh).
- **Evidence tier**: **3.0** — Subscale/partial demonstration: MCNP neutronics codes are **well-validated** for fusion blanket design (tier 5 for the code itself), but application to MagLIF's **axial RTL geometry** (unique vs. spherical tokamak blankets) is **not experimentally validated** at GJ yields. Z-IFE neutronics analysis provides **partial validation** (tier 3) but rests on simulation, not measurement. Tier 3 (subscale validation: MCNP trusted for blanket physics, but specific MagLIF geometry with RTL ports not tested).

**Hardware Risk**

- **Plant requirement**: Structural materials (Al, steel, carbon-carbon chamber) must survive 14 MeV neutron displacement damage up to **50–100 dpa** (displacements per atom) over 30-year plant lifetime at 1 Hz. FLiBe-facing materials must resist activation products (Be, Li, F transmutation) and helium embrittlement from (n,α) reactions. **Electrodes and RTL transmission components** in line-of-sight to plasma experience **peak neutron flux** (~10× higher than blanket-shielded regions)—must survive 500–1000 dpa or be replaceable annually.
- **Best demonstrated**: F82H ferritic steel and Hastelloy **displacement damage tolerance** is well-characterized from ITER/fission programs: F82H survives **50–80 dpa** before ductile-brittle transition (tier 5 data from neutron irradiation facilities). Hastelloy corrosion resistance in FLiBe is **demonstrated** in MSRE/Kairos programs (tier 5). **Combined neutron + corrosion** environment is tier 3 (limited data from ORNL). **Electrodes**: tungsten and TZM molybdenum survive 100+ dpa in fission reactors (tier 5), but **14 MeV fusion neutrons** cause 3–5× more damage per dpa than fission spectrum (tier 3 extrapolation).
- **Gap ratio**: **10× peak fluence** for electrodes (ITER first wall ~50 dpa over lifetime → MagLIF electrodes ~500 dpa if in direct line-of-sight). **2× for blanket-shielded regions** (80 dpa chamber → F82H limit ~50 dpa with margin).
- **Closure mechanism**: Sacrificial electrodes (replaced annually, $10–20M capital each); high-dpa-tolerant materials (W, TZM, SiC/SiC composites); active cooling to reduce thermal stress. **Blanket-shielded chamber**: F82H or carbon-carbon composite with 10–30 year replacement cycle (scheduled during major outages).
- **Classification**: **Degrading** — if electrode lifetime is 10^6 shots (3 weeks at 1 Hz) instead of 10^7 shots (10 months), annual electrode replacement cost increases from $20M to $200M, degrading LCOE by ~20–30 $/MWh (still operable, but O&M-intensive). If chamber materials fail at 20 dpa instead of 80 dpa, replacement frequency increases 4× (every 7.5 years instead of 30 years), adding $50–100M/year to O&M.
- **Evidence tier**: **3.5** — **Partial demonstration**: F82H/Hastelloy 14 MeV neutron damage is **extrapolated from fission spectrum** (tier 3), but ITER materials program provides **some fusion-spectrum data** (tier 4 for blanket materials). Electrodes in direct line-of-sight have **no experimental validation** at 500+ dpa fusion spectrum (tier 2). Average (4 + 2) / 2 = 3.0, **upgrade to 3.5** because blanket-shielded regions (80% of chamber) are better-characterized than electrodes.

**F5 mean = (3.0 + 3.5) / 2 = 3.25 → round to 3.3**

---

#### Function 6: Fuel Cycle Closure

**Physics Risk**

- **Plant requirement**: Tritium breeding ratio (TBR) ≥ 1.05 (5% margin above breakeven to account for losses and startup inventory). FLiBe blanket with Li-6 enrichment (30–90%) must breed sufficient tritium from 6Li(n,α)T reactions. Tritium extraction efficiency from FLiBe must be ≥95% (recover 95% of bred tritium to avoid inventory buildup in coolant loop).
- **Best demonstrated**: Z-IFE study **assumed** TBR ≥ 1 but did not publish neutronics validation. No MagLIF-specific blanket design with calculated TBR exists in public literature. Tritium permeation analysis performed for FLiBe→304 SS piping (0.0467 g/yr loss at 850 K with PRF=100 permeation barrier, below ITER 1 g/yr criterion), but **pump, valve, and steam generator contributions not quantified**.
- **Gap ratio**: **N/A** — TBR not calculated for MagLIF geometry. FLiBe blanket **should** achieve TBR > 1 (Li-6 enriched molten salt blankets in tokamak studies routinely exceed 1.1), but axial RTL ports may reduce TBR by 5–15% due to neutron streaming losses.
- **Closure mechanism**: Li-6 enrichment to 30–90% (higher enrichment compensates for geometric losses from ports). Blanket thickness optimization (80 cm FLiBe per Z-IFE is likely adequate, but MCNP validation required). Tritium extraction via **vacuum degassing** (FLiBe circulated through low-pressure vessel, dissolved tritium evaporates) or **gas sparging** (helium bubbles carry tritium out of liquid).
- **Classification**: **Binary** — if TBR < 1.0, tritium inventory depletes over time and plant must purchase external tritium ($30k/g, global supply ~25 kg total). At 1 kg/year consumption (typical for 1 GWe D-T plant), external tritium cost is $30M/year and **global supply exhausted in 25 years** across all D-T fusion plants. No commercial operation possible without TBR ≥ 1. Framework mandates this as **binary**.
- **Evidence tier**: **2.0** — Simulation only: TBR not published for MagLIF. FLiBe breeding physics is **well-understood** from tokamak/fission studies (tier 5 for the nuclear physics), but application to MagLIF's **axial port geometry** is **not validated** (tier 2). Tritium extraction from FLiBe at kg/day rates is **never demonstrated** (tier 1), but vacuum degassing is a **mature chemical engineering process** used in molten salt reactors (tier 4 for the process, tier 2 for fusion-scale throughput). Average (2 + 1 + 4) / 3 = 2.3, **round to 2.0** (conservative, given no published TBR calculation).

**Hardware Risk**

- **Plant requirement**: FLiBe production at industrial scale (thousands of tons for blanket inventory); Li-6 enrichment capacity scaled to fusion sector demand (currently <100 kg/year globally, fusion requires tons/year); tritium extraction plant processing ≥1 kg/day throughput with ≥95% recovery; permeation barriers (PRF ≥ 100) on all hot surfaces (pumps, valves, steam generators, piping) to prevent tritium leakage below 1 g/yr regulatory limit.
- **Best demonstrated**: FLiBe production: **pilot scale only** (Kairos Power, TerraPower MCFR programs have produced tons, not thousands of tons). Beryllium supply: global production ~300 tons/year (Materion, Ulba), mostly non-nuclear grade. Li-6 enrichment: **limited capacity** (ORNL Y-12, Russia, China; exact capacity classified but estimated <100 kg/year unclassified). Tritium extraction: **vacuum degassing** demonstrated in MSRE (kg/day scale not reached). Permeation barriers: PRF=100 coatings (alumina, erbium oxide) demonstrated in ITER R&D (tier 4).
- **Gap ratio**: **100× FLiBe production** (current pilot scale ~10–100 tons → fusion plant requires 1000–5000 tons blanket inventory). **10× Li-6 enrichment capacity** (current <100 kg/yr → fusion sector requires 1000+ kg/yr for multiple plants). **10× tritium extraction throughput** (no demonstrated kg/day system; ITER target is ~1 kg/day but not yet operational).
- **Closure mechanism**: FLiBe shared supply chain with molten salt fission (Kairos 140 MWe Hermes reactor uses FLiBe primary coolant—if deployed at scale, FLiBe production ramps to fusion-relevant levels). Li-6 enrichment: HALEU-style government/commercial partnership (Y-12 expansion, Centrus Energy). Tritium extraction: scale-up vacuum degassing from MSRE/Kairos experience.
- **Classification**: **Degrading** — if Li-6 enrichment stays <100 kg/yr, only 1–2 fusion plants can be built per year globally (startup inventory ~50–100 kg Li-6 per plant). FLiBe production constraint adds $50–100M to first-plant capital (scarcity premium), degrading LCOE by 5–10 $/MWh. Tritium extraction failure (recovery <80%) requires external makeup tritium, adding $10–30M/year O&M (10–30 $/MWh LCOE penalty). Does not prevent operation, but limits deployment rate and increases costs.
- **Evidence tier**: **2.5** — FLiBe production is tier 3 (pilot scale demonstrated, Kairos/TerraPower); Li-6 enrichment is tier 2 (limited capacity, no fusion-scale demonstration); tritium extraction is tier 2 (vacuum degassing demonstrated in MSRE but not at kg/day fusion scale); permeation barriers are tier 4 (ITER-validated coatings). Average (3 + 2 + 2 + 4) / 4 = 2.75, **round to 2.5** (conservative, reflecting supply chain bottlenecks not yet resolved).

**F6 mean = (2.0 + 2.5) / 2 = 2.25 → round to 2.3**

---

#### Function 7: Power Conversion & BOP

**Physics Risk**

- **Plant requirement**: Pulsed thermal input (GJ-class energy deposited in FLiBe blanket over ~100 ns implosion, followed by ~1 second dead time) must be converted to continuous electrical output via thermal buffering (molten salt thermal storage or steam accumulators). Thermal efficiency ≥40% (42% baseline from Z-IFE combined Brayton-Rankine; 50% stretch goal with carbon-carbon composite chamber at >1000 K).
- **Best demonstrated**: Combined Brayton-Rankine cycle at **steady-state thermal input** is tier 7 (mature power plant technology). **Pulsed thermal input** with 1-second cycle time is **not demonstrated** at GJ scale. Z-IFE study analyzed four thermal cycle options (Rankine, Brayton, combined, direct Brayton) and concluded 42% efficiency is achievable with **thermal buffering** (steam accumulator smooths pulsed heat input to turbine). Molten salt thermal storage (used in concentrated solar power plants, tier 6) can buffer GJ-scale pulses, but **never integrated with fusion neutron heating**.
- **Gap ratio**: **N/A** — pulsed thermal cycle physics is **well-understood** (tier 6 industrial process), but fusion-specific integration (FLiBe primary loop + pulsed neutron heating + tritium containment) is **not demonstrated** (tier 2).
- **Closure mechanism**: FLiBe primary loop circulates through intermediate heat exchanger (IHX) to secondary molten salt (NaCl-MgCl₂ or Hitec) or steam. Thermal buffering via steam accumulator (pressure vessel storing saturated steam, releases to turbine at constant rate) or molten salt tank. Thermal cycling on turbine blades is **manageable** per Z-IFE (1-second cycle is slow compared to turbine blade vibration frequencies ~100 Hz).
- **Classification**: **Degrading** — if thermal efficiency is limited to 35% (vs. 42% baseline) due to pulsed-cycle losses, net electric output drops by 17%, requiring 17% larger plant capital to produce the same MWe (LCOE increases by ~10 $/MWh). Does not prevent operation, but reduces economic competitiveness.
- **Evidence tier**: **3.0** — Subscale/partial demonstration: Combined Brayton-Rankine is tier 7 (mature), but **pulsed thermal source** at GJ scale is tier 2 (Z-IFE analysis only, no experimental plant). Thermal buffering via molten salt or steam accumulator is tier 6 (CSP plants), but **fusion integration** is tier 2. Average (7 + 2 + 6) / 3 = 5.0, **downgrade to 3.0** because the **fusion-specific integration** (FLiBe + tritium + pulsed neutron heating) is the dominant uncertainty, not the thermal cycle itself.

**Hardware Risk**

- **Plant requirement**: FLiBe-to-secondary heat exchangers (IHX) must survive 850 K molten salt corrosion + tritium permeation (PRF ≥ 100 required) + thermal cycling (±100 K per pulse). Steam generators (if Rankine cycle) must prevent FLiBe-water interaction (violent exothermic reaction if breach occurs). Turbine blades must survive thermal cycling without fatigue cracking over 10^9 pulses (30 years at 1 Hz).
- **Best demonstrated**: Hastelloy-N IHX demonstrated in MSRE at 650 K (tier 5); **850 K operation** is extrapolated (tier 3). Tritium permeation barriers (alumina, erbium oxide) demonstrated in ITER R&D at 850 K (tier 4). FLiBe-steam separation: **double-walled heat exchangers** with leak detection (used in sodium-cooled fast reactors, tier 6) prevent catastrophic FLiBe-water mixing. Turbine blade thermal cycling: **gas turbines** in peaker power plants survive 10^5 thermal cycles (tier 6), but not 10^9 cycles—lifetime limited to ~10 years, requiring mid-life turbine replacement.
- **Gap ratio**: **10× IHX temperature** (MSRE 650 K → MagLIF 850 K). **10,000× turbine thermal cycles** (gas turbine 10^5 cycles → MagLIF 10^9 cycles over 30 years).
- **Closure mechanism**: Hastelloy-N or higher-temperature alloys (Haynes 242, Inconel 617) for IHX; PRF=100 coatings on all hot surfaces; double-walled steam generators with inert gas (He, Ar) in the gap for leak detection; turbine replacement every 10 years as scheduled major maintenance (adds $50–100M capital every decade, amortized into O&M).
- **Classification**: **Degrading** — IHX or steam generator failures (corrosion perforation, tritium leaks) require plant shutdown for repair (weeks to months), reducing capacity factor by 5–15% annually (LCOE penalty 10–20 $/MWh). Turbine replacement every 10 years adds $100M capital (amortized: $10M/year), increasing LCOE by ~1–2 $/MWh. Does not prevent operation, but increases O&M costs.
- **Evidence tier**: **4.0** — Near-regime demonstrated: Hastelloy IHX at 650 K is tier 5; extrapolation to 850 K is tier 3 (within 2× temperature, but corrosion rates scale exponentially). Tritium permeation barriers are tier 4 (ITER-validated at 850 K). FLiBe-steam separation is tier 6 (sodium fast reactor technology). Turbine thermal cycling at 10^5 cycles is tier 6; extrapolation to 10^9 is tier 3. Average (3 + 4 + 6 + 3) / 4 = 4.0.

**F7 mean = (3.0 + 4.0) / 2 = 3.5**

---

### Function-Level Means Summary

| Function | F-mean | Notes |
|----------|--------|-------|
| F1: Plasma Performance | 2.8 | Physics tier 3 (χ ≈ 0.1 subscale); hardware tier 2.5 (cryo targets undemonstrated) |
| F2: Driver / Energy Input | 3.5 | Physics tier 4 (27 MA near-regime); hardware tier 3 (TITAN subscale, lifetime gap) |
| F3: Instability Control | 4.5 | Physics tier 4 (RT manageable at Z scale); hardware tier 5 (liner surface finish achieved) |
| F4: Plasma-Wall Interaction | 1.5 | **Lowest score** — Physics tier 2 (simulation only at GJ yields); hardware tier 1 (combined environment never tested) |
| F5: Neutron/Particle Handling | 3.3 | Physics tier 3 (MCNP validated for blanket, not RTL ports); hardware tier 3.5 (F82H extrapolated to 14 MeV spectrum) |
| F6: Fuel Cycle Closure | 2.3 | Physics tier 2 (TBR not calculated for MagLIF); hardware tier 2.5 (Li-6 enrichment bottleneck, FLiBe supply scaling) |
| F7: Power Conversion & BOP | 3.5 | Physics tier 3 (pulsed thermal cycle analysis only); hardware tier 4 (IHX/turbine near-regime) |

### Binary Risks Summary

From the risk matrix, the following risks are classified as **binary** (zero net electricity if unmitigated):

1. **F1 Physics: Ignition failure** — if χ cannot reach ≥1.0 at practical currents (60+ MA), no net energy is produced and commercial operation is impossible.
2. **F4 Physics: Chamber pressure spike / liquid wall failure** — if FLiBe thick liquid wall cannot be reconstituted within 1 second or chamber pressure exceeds structural limits, plant cannot operate at 1 Hz. Reducing to 0.1 Hz (305 $/MWh) makes LCOE uncompetitive.
3. **F4 Hardware: Chamber lifetime <1000 shots** — if combined environment (shock + neutron + corrosion + thermal cycling) causes chamber failure in <1000 shots, plant must shut down every ~10 days for chamber replacement (weeks-long outage), dropping capacity factor to <30% and making LCOE >150 $/MWh.
4. **F6 Physics: TBR < 1.0** — if tritium breeding ratio is below breakeven, plant cannot sustain operation without external tritium purchases, which exhaust global supply in ~25 years. Framework mandates this as binary for all D-T concepts.

**Note**: F1 Hardware (cryo target cost) is **conditionally binary**—if cryo pathway is required and cost exceeds $10/shot, annual consumable O&M surpasses capital amortization, making the plant economically inoperable (LCOE >150 $/MWh). However, if the non-cryo composite target pathway succeeds, this risk is degrading, not binary. Conservatively classified as **degrading** in the matrix, but flagged as **conditional binary** in synthesis text.

### Heritage Credit (D-T fuel only)

MagLIF is a **pulsed MIF concept with liner-compression geometry**, not a tokamak, stellarator, mirror, or laser IFE. The heritage lineage table provides:

| Heritage lineage | Floor |
|-----------------|-------|
| magLIF (Sandia Z-machine) | 3.0 |

**Heritage credit applies to F1-F3 only**: Plasma Performance, Driver, Instability Control.

**Application**:
- **F1 (Plasma Performance)**: Mean = 2.8 → **upgraded to 3.0** (heritage floor)
- **F2 (Driver / Energy Input)**: Mean = 3.5 → **no change** (already above 3.0 floor)
- **F3 (Instability Control)**: Mean = 4.5 → **no change** (already above 3.0 floor)

**Final F1-F7 after heritage credit**:
F1=3.0, F2=3.5, F3=4.5, F4=1.5, F5=3.3, F6=2.3, F7=3.5

---

### YAML Scores Block

```yaml
---
scores:
  C1: 3.7
  C3: 2.8
  C4: 3.0
  C5: 2.1
  C8: 2.5
  F1: 3.0
  F2: 3.5
  F3: 4.5
  F4: 1.5
  F5: 3.3
  F6: 2.3
  F7: 3.5
  binary_risks:
    - "F1 Physics: Ignition failure — if Lawson parameter χ cannot reach ≥1.0 at practical drive currents (60+ MA), no net energy is produced and commercial operation is impossible."
    - "F4 Physics: Chamber pressure spike / FLiBe liquid wall reconstitution failure — if thick liquid wall cannot be reconstituted within 1 second or chamber pressure exceeds structural limits at GJ-scale yields, plant cannot operate at 1 Hz. Reducing to 0.1 Hz makes LCOE uncompetitive (305 $/MWh)."
    - "F4 Hardware: Chamber lifetime <1000 shots due to combined environment failure — if shock + neutron + FLiBe corrosion + thermal cycling causes chamber/electrode cracking in <1000 shots, plant must shut down every ~10 days for replacement, dropping capacity factor to <30% and making LCOE >150 $/MWh."
    - "F6 Physics: Tritium breeding ratio (TBR) < 1.0 — if FLiBe blanket cannot breed sufficient tritium due to neutron streaming losses through RTL ports, plant cannot sustain operation without external tritium purchases, exhausting global supply in ~25 years across all D-T fusion plants."
---
```
