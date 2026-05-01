---
ID: 30-laser-icf-nif-commercialization
Concept: Laser ICF - NIF Commercialization (D-T)
Company: Inertia Enterprises
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Most important risk**: Energy balance closure is unverified — model requires Q_sci ≈ 52.5 for stated 1.5 GW net from a single system, but company claims ">30×" commercial threshold would yield only ~440 MWe per system. Either modular architecture is required or gain targets are understated. This is a blocking feasibility gap.
- **Most important advantage**: Physics validation is complete — NIF ignition demonstrated with Q_sci = 4.13 achieved (April 2025), the only fusion concept with experimentally confirmed net target energy gain. No physics risk to burning plasma, only engineering scale-up from 2 MJ to 10 MJ drive.
- **LCOE ballpark**: $120/MWh at 1.5 GWe NOAK with aggressive assumptions (80% availability, $100/J DPSSL laser after 10× learning, $1/target achieved). FOAK: $189/MWh at $700/J laser. Diode replacement adds $3–7/MWh if current-generation diode lifetime persists. At 1 GWe scaled: $137/MWh.
- **Confidence verdict**: **Low** — NOAK model assumes 10× laser cost reduction, unverified $1/target manufacturing cost, 80% availability with no 10 Hz IFE operational experience, and a 45% thermal efficiency borrowed from LIFE heritage (2011 design). Four of the five largest cost drivers are speculative.

---

## 2. What Matters Most for LCOE

Ranked by model elasticity (sensitivity analysis from model output):

### 1. Plant Availability (elasticity: -0.97)
- **Assumed value**: 80% (model); LIFE heritage target was 92% (NOAK), 70% (FOAK)
- **Source**: No 10 Hz IFE plant has operated. LIFE targets from OSTI-1022881. Model uses 80% as optimistic-but-conservative midpoint given high-turnover components: laser diodes (4–9 year replacement at current lifetime), final optics (debris/X-ray exposure at 10 Hz), target injection mechanisms, first wall structural elements.
- **Sensitivity magnitude**: 10% improvement in availability (80% → 88%) reduces LCOE by ~9.7% (~$120 → $108/MWh). Degradation to 70% (LIFE FOAK) increases LCOE to ~$137/MWh.
- **What would flip the conclusion**: Availability below 65% makes the concept economically uncompetitive with fission (~$130–150/MWh new nuclear). Above 88%, LCOE reaches sub-$110/MWh, approaching natural gas combined cycle parity in high-carbon-price scenarios.

### 2. Target Material O&M Cost (elasticity: +0.46)
- **Assumed value**: $315M/year at $1/target × 315M targets/year (10 Hz × 3.15×10^7 s/yr)
- **Source**: Inertia's stated "<$1 per target" goal (inertia-website-technical.md). Heritage: Goodin et al. (2004) projects $0.41/target NOAK for indirect drive at 182M/year throughput; Inertia's 315M/year is 73% higher. Current experimental targets cost ~$2,500 each — 6,000× reduction required.
- **Sensitivity magnitude**: Halving target cost ($1 → $0.50) reduces LCOE by ~23% (~$120 → $93/MWh). Doubling ($1 → $2) increases LCOE by ~46% (~$120 → $175/MWh). Target cost contributes ~$27/MWh to LCOE at $1/target.
- **What would flip the conclusion**: Target cost above $2/target (~$630M/year) drives LCOE above $175/MWh, likely uneconomic. Below $0.50/target (~$158M/year) reaches competitive LCOE <$95/MWh. The $0.41 Goodin NOAK projection suggests $1/target is conservative, but no industrial-scale validation exists.

### 3. Laser Driver Capital Cost (elasticity: +0.09 via driver_laser_per_mw)
- **Assumed value**: $1,000M for 10 MJ at $100/J NOAK (model); FOAK: $7,000M at $700/J
- **Source**: Analysis §S5 cites $700–1,000/J FOAK from handwritten exemplar 26 (Xcimer whitepaper context); NOAK assumes 10× learning curve (analogous to solar PV). Haefner (2023) ILT workshop states diodes must reach $0.007/W (100× cost reduction from ~$0.7/W current) for IFE viability; diodes represent ~1/3 of total laser capital (~$333M of $1B).
- **Sensitivity magnitude**: Laser cost from $1B (NOAK) → $7B (FOAK) increases LCOE from $120 → $189/MWh (+57%). Each $1B laser capital adds ~$11/MWh to LCOE.
- **What would flip the conclusion**: Laser cost above $10B (>$1,000/J) drives LCOE above $210/MWh. Below $500M (<$50/J, further 2× learning from NOAK) reaches ~$109/MWh. The 10× FOAK-to-NOAK reduction is aggressive but follows semiconductor manufacturing precedent.

### 4. Q_eng / Target Gain (elasticity: -0.39)
- **Assumed value**: q_eng = 2.370 (model-derived to close 1.5 GWe at 10 MJ driver); Q_sci ≈ 52.5× required
- **Source**: Anchored to stated 10 MJ laser energy (Inertia website, GlobeNewsWire). Stated ">30×" commercial threshold yields only ~440 MWe per system (model); §S2 simplified formula gives ~350 MWe (omitting neutron multiplier). Tension with 1.5 GW claim unresolved. NIF peak Q_sci = 4.13 at 2 MJ (Wurzel & Hsu 2025); 52.5× at 10 MJ is 12.7× higher, requiring favorable scaling (physically expected but undemonstrated).
- **Sensitivity magnitude**: Q_sci from 52.5 → 60 reduces LCOE by ~3% ($120 → $116/MWh). Q_sci = 30 (stated threshold) at 10 MJ yields 440 MWe net → LCOE $255/MWh due to capacity underutilization. Once energy balance closes (Q_sci ≥ 50), further gain improvements have diminishing returns — O&M levers dominate.
- **What would flip the conclusion**: Q_sci below 45× at 10 MJ makes single-system 1.5 GW infeasible; modular architecture becomes mandatory. Q_sci above 60× provides limited additional LCOE benefit (<5% marginal gain). The key question is binary: does gain scale favorably from 2 MJ (demonstrated) to 10 MJ (extrapolated)?

### 5. Interest Rate (elasticity: +0.40)
- **Assumed value**: 7% real (model); construction time 6 years (model)
- **Source**: Standard fusion plant financing assumption. Extended construction time (6 yr vs. 4–5 yr for conventional plants) reflects first-of-kind IFE complexity.
- **Sensitivity magnitude**: 10% reduction in interest rate (7% → 6.3%) reduces LCOE by ~4% (~$120 → $115/MWh). Interest during construction (IDC) represents ~$1,326M of $8,223M total capital (16%).
- **What would flip the conclusion**: Primarily a financial lever, not a technical one. Low-interest government financing (3–4%) could reduce LCOE to ~$105–110/MWh. Commercial financing at 10%+ drives LCOE above $140/MWh.

**Summary hierarchy**: Availability > Target cost > Laser capital > Q_sci (above closure) > Interest rate. The first three are engineering challenges; the fourth is a physics extrapolation (low risk given NIF scaling trends); the fifth is a policy/financing lever. Improving availability from 80% → 90% yields more LCOE leverage than doubling Q_sci from 52 → 104.

---

## 3. Risk Verdicts

### Energy balance closure at stated design point (10 MJ, 1.5 GW net)
- **Verdict**: Genuinely uncertain (leans toward resolvable via modular architecture or higher gain)
- **Rationale**: Model requires Q_sci ≈ 52.5 for single-system closure; stated ">30×" threshold is insufficient. Either (a) modular architecture (multiple chambers) is intended, or (b) commercial gain target is understated. NIF Q_sci scaling from 2 MJ → 10 MJ is physically favorable (implosion energy scales superlinearly with drive energy above ignition threshold) but undemonstrated.
- **What would retire this risk**: Published energy flow diagram from Inertia showing power balance closure at stated parameters, OR NIF experiments at >5 MJ drive demonstrating favorable gain scaling, OR explicit confirmation of modular architecture (e.g., "four 375 MWe modules" totaling 1.5 GW).

### Target fabrication at 315M/year (<$1/target)
- **Verdict**: Unlikely resolvable at $1/target; likely resolvable at $0.41–0.50/target (Goodin NOAK projection)
- **Rationale**: Current targets cost ~$2,500 each (NIF campaign production). Reaching <$1 requires 2,500× cost reduction; Goodin (2004) projects $0.41/target NOAK for indirect drive at 182M/year (6,100× reduction from current experimental cost). Inertia's 315M/year is 73% higher throughput, implying target cost $0.50–0.75/target is more realistic than $1. The $1 goal has headroom against Goodin's $0.41 bottom-up projection, but no industrial-scale cryogenic D-T layering facility exists.
- **What would retire this risk**: Pilot target factory demonstration producing >1M targets/year at <$5/target (intermediate milestone) with credible pathway to $0.50 NOAK. Automated cryogenic D-T ice layering at >100 targets/hour throughput (vs. current ~1 target/day for NIF campaigns).

### Laser diode lifetime and replacement cost
- **Verdict**: Likely resolvable (7–10× gap closable with incremental R&D)
- **Rationale**: Current devices achieve ~1.4–2.9 GShots; target is 14–20 GShots (Haefner 2023). Gap is large (7–10×) but not fundamentally physics-limited — semiconductor diode degradation mechanisms (facet oxidation, thermal cycling, optical damage) are well-studied. Replacement at current-generation lifetime (every 4–9 years) adds $3–7/MWh to LCOE; target-met lifetime (44–63 years) reduces this to <$1/MWh. Missing this target does not block the concept but degrades LCOE by ~3–6%.
- **What would retire this risk**: Diode lifetime demonstration >10 GShots in accelerated lifetime testing (equivalent to ~30 years at 10 Hz). Commercial diode production at scale (100× current volume) with cost <$0.01/W (vs. $0.007/W target).

### 10 Hz chamber clearing and first wall survival
- **Verdict**: Genuinely uncertain (hardest materials problem in the concept)
- **Rationale**: No IFE chamber has operated at >1 Hz fusion-relevant fluence. Each shot deposits neutrons (14 MeV, ~450 MJ thermal per shot), X-rays (hohlraum radiation), and debris (vaporized lead hohlraum, ~1–5 g per shot). Chamber must clear debris and allow laser beam propagation within 100 ms (10 Hz = 0.1 s period). HAPL program (NRL/LANL) studied chamber clearing at kJ-scale shots, but no validation exists at 10 MJ yield × 10 Hz duty cycle. First wall material is unspecified by Inertia.
- **What would retire this risk**: Integrated chamber clearing + target injection demonstration at >5 Hz with simulated fusion yield (neutron fluence, X-ray pulse, debris mass) representative of ~10% of full commercial shot energy. First wall material qualification under 14 MeV neutron irradiation at 10 Hz pulse rate (requires dedicated test facility; does not currently exist).

### Liquid lithium tritium breeding and extraction
- **Verdict**: Likely resolvable (well-studied physics, engineering scale-up needed)
- **Rationale**: Tritium breeding from Li-6 under neutron irradiation is well-understood. Tritium extraction from liquid Li has been studied in fission breeder programs and MFE blanket R&D. LIFE heritage (OSTI-1028880) shows TBR = 1.59 for indirect-drive geometry with liquid Li first wall; tritium inventory ~40 g (Maroni process). Inertia claims "hundreds of grams" on-site inventory (website FAQ), consistent with LIFE. The company acknowledges tritium extraction is "still an area of active development." Scale-up risk is moderate (liquid-metal handling at GW thermal scale), not fundamental.
- **What would retire this risk**: Liquid Li loop demonstration at >100 MW thermal with tritium extraction at >10 g/day throughput. TBR validation with realistic chamber geometry including laser beam ports (beam ports subtract solid angle from breeding coverage; LIFE TBR may not be achievable with 1,000 beamline penetrations).

### Steam cycle thermal efficiency (45% assumption)
- **Verdict**: Likely resolvable (mature technology, integration risk only)
- **Rationale**: LIFE heritage assumes 44% thermal efficiency with 800°C Li exit temperature (OSTI-1022881). Modern supercritical CO2 cycles could reach ~50%. Inertia has not published a confirmed value. Steam Rankine cycle at GW scale is TRL 9; the only novelty is integration with a pulsed liquid-Li primary circuit. At 10 Hz (0.1 s period), thermal pulse frequency is well above steam system time constants (~seconds to minutes), so pulsed operation is unlikely to degrade cycle efficiency.
- **What would retire this risk**: Published heat balance for Inertia plant design confirming thermal efficiency ≥44%. Intermediate heat exchanger design for Li-water isolation (required to prevent tritium migration into steam system). No fundamental barrier; this is a low-risk assumption.

### Semiconductor diode supply chain scale-up (100× required)
- **Verdict**: Likely resolvable (precedent in consumer electronics, but fusion-specific wavelengths may limit leverage)
- **Rationale**: Inertia explicitly states ~100× supply chain expansion needed (website FAQ). Current high-power diode market serves industrial cutting, materials processing, and consumer electronics (FaceID lidar). Fusion requires diodes at specific wavelengths (~890 nm for Nd:glass pump) with high duty cycles and potentially radiation-hardened for near-chamber environments. The smartphone lidar analogy (Inertia's own comparison) suggests rapid scale-up is feasible, but fusion wavelengths may not fully overlap with consumer demand. Cost target $0.007/W (Haefner 2023) requires ~100× cost reduction from current ~$0.7/W.
- **What would retire this risk**: Diode production capacity demonstration >1M units/year at target wavelength (890 nm) with cost trajectory toward $0.01/W. Multi-GW fusion diode production commitment from major semiconductor manufacturers (analogous to solar PV supply chain development 2010–2020).

---

## 4. Structural Advantages and Disadvantages

Comparison against conventional D-T tokamak cost structure (CAS breakdown baseline):

### Advantages (Cost Eliminated or Reduced):

**1. No superconducting magnets or cryogenics (CAS220103 = $0; eliminates ~15–25% of tokamak direct capital)**
- Tokamak: REBCO tape, magnet structures, cryogenic systems (He refrigeration, thermal shields) represent largest single capital cost — ~$1.5–3B for 1 GWe plant.
- Inertia: Zero magnet capital. Cryogenic infrastructure limited to target D-T fuel layering (factory-scale, not plant-scale).
- Quantified benefit: Eliminates ~$1.5–3B from CAS22 vs. HTS tokamak baseline; partially offset by $1–7B laser driver capital (net neutral to unfavorable at FOAK; favorable at NOAK if laser learning curve holds).

**2. No plasma-facing components with multi-year replacement cycles (reduces CAS70 O&M complexity)**
- Tokamak: First wall, divertor tiles, breeding blanket modules require periodic replacement (2–6 year cycles); remote handling in activated environment; large replacement capital events.
- Inertia: Liquid Li first wall is continuously refreshed (no solid replacement). Chamber structural components may require replacement every 3–5 years (Inertia website), but liquid wall reduces neutron damage to structure.
- Quantified benefit: Eliminates solid blanket module replacement (~$200–400M periodic capital for tokamak). Partially offset by laser diode replacement ($333M every 4–9 years at current lifetime) and final optics replacement (unquantified, frequency unknown).

**3. Modular factory-manufactured driver (potential for learning curve cost reduction)**
- Tokamak: Custom on-site magnet winding, assembly, and integration; limited learning across units (each plant is effectively FOAK for magnets).
- Inertia: 1,000 identical beamline modules factory-manufactured with semiconductor processes. Diode production follows semiconductor learning curves (15–20% cost reduction per doubling of cumulative production, analogous to solar PV).
- Quantified benefit: Laser cost $7B FOAK → $1B NOAK (10× reduction assumed in model) is plausible if diode costs follow solar precedent. Tokamak magnets show much slower learning (5–10% per doubling, dominated by custom engineering rather than mass production).

### Disadvantages (Cost Added or Increased):

**1. Massive consumable O&M cost (target materials at $315M/year baseline)**
- Tokamak: Fuel cycle cost ~$2–10M/year (D-T fuel, tritium processing, minimal consumables).
- Inertia: Target material cost ~$315M/year at $1/target (10 Hz × 3.15×10^7 s/yr). Adds ~$27/MWh to LCOE vs. ~$0.2–1/MWh for tokamak fuel. This is a structural disadvantage — IFE requires consumable precision-manufactured targets; MFE does not.
- Quantified disadvantage: +$300M/year O&M vs. tokamak; equivalent to ~25% of LCOE at baseline. If target cost reaches $2/target (miss on manufacturing learning curve), O&M cost doubles (+$315M/year additional), driving LCOE to $175/MWh.

**2. Novel chamber engineering with no operational heritage (increases technical risk and FOAK cost)**
- Tokamak: Vacuum vessel, blanket, divertor are high-TRL subsystems (ITER validates these at scale).
- Inertia: 10 Hz chamber clearing, first wall survival under pulsed neutron/X-ray/debris loading, and laser beam propagation path cleanliness are unprecedented. No cost heritage; LIFE studies (2011) predate ignition and assumed different driver. First wall material unspecified.
- Quantified disadvantage: Chamber capital cost is uncertain (modeled at ~$281M for CAS220101 blanket + first wall, scaled from LIFE analogue). True FOAK cost could be 2–3× higher (~$500–800M) given lack of heritage. This adds ~$5–10/MWh to LCOE vs. baseline.

**3. Lower availability ceiling due to high-turnover components (structural LCOE penalty)**
- Tokamak: Target availability 85–92% (ITER-era baseline; limited by planned maintenance, not component failures).
- Inertia: High-turnover components (laser diodes every 4–9 years, final optics unknown replacement rate, target injection mechanisms) impose availability ceiling. Model assumes 80%; LIFE FOAK was 70%. Sensitivity analysis shows -0.97 elasticity — availability is the dominant LCOE driver.
- Quantified disadvantage: 80% vs. 90% availability (tokamak baseline) adds ~$13/MWh to LCOE. If availability degrades to 70% (LIFE FOAK), penalty is ~$17/MWh. Structural: 10 Hz pulsed operation stresses components more than tokamak steady-state.

**4. Periodic large-capex diode replacement not in baseline O&M (hidden LCOE adder)**
- Tokamak: Periodic magnet refurbishment every 15–30 years (limited scope; magnets are long-lived).
- Inertia: Diode capital ~$333M NOAK (1/3 of $1B laser); replacement every 4–9 years at current lifetime. Over 30-year plant life: ~$1.0–2.3B cumulative periodic capital NOT included in baseline O&M model (framework has no account for this). Adds $3–7/MWh to LCOE.
- Quantified disadvantage: +$3–7/MWh vs. tokamak baseline (which has no equivalent high-frequency large-capex replacement). If diode lifetime target (44–63 years) is met, this penalty reduces to <$1/MWh.

### Net Structural Assessment:

At **NOAK** with optimistic assumptions (laser $1B, availability 80%, target $1/each, diode lifetime target met):
- Advantages (no magnets, modular factory production) offset disadvantages (consumable targets, periodic diode replacement) → **roughly neutral vs. tokamak capital structure**.
- O&M disadvantage (~$27/MWh target cost + $3/MWh diode replacement) is **structural and cannot be eliminated** — IFE requires consumables; MFE does not.
- LCOE: $120/MWh (Inertia NOAK) vs. ~$110–130/MWh (spherical tokamak HTS baseline from analysis 21). Comparable, not advantaged.

At **FOAK** (laser $7B, availability 70%, target $2–5/each, diode lifetime current-gen):
- Laser capital disadvantage (~$7B vs. ~$2–3B tokamak magnets) + consumable O&M penalty (~$630M–1.6B/year at $2–5/target) → **substantially worse than tokamak**.
- LCOE: $189/MWh (laser FOAK only) → $250–350/MWh if target cost and availability degrade → **uncompetitive with any baseload generation**.

**Key insight**: Inertia's economic viability depends on NOAK learning curves holding for both laser hardware (10× cost reduction) and target manufacturing (2,500–6,000× cost reduction). If either fails, the concept is structurally disadvantaged vs. MFE. If both succeed, it is competitive but not superior.

---

## 5. Cross-Concept Positioning

### Landscape Position:

**Within IFE family**:
- **Inertia (concept 30)** vs. **Xcimer (concept 17a, hybrid direct drive)**: Opposite design space extremes. Inertia chooses high rep rate (10 Hz), low yield per shot (~450 MJ fusion), indirect drive (12% coupling efficiency), and DPSSL laser ($700–1,000/J FOAK). Xcimer chooses low rep rate (0.25–1 Hz), high yield per shot (~1.6 GJ fusion), hybrid drive (>50% coupling efficiency), and excimer laser ($100–120/J FOAK). Xcimer's lower rep rate drastically reduces chamber clearing and target injection stress; Inertia's higher rep rate makes the thermal plant more continuous (10 Hz ≈ quasi-steady-state vs. 0.25 Hz pulsed). Inertia's physics validation is stronger (NIF ignition); Xcimer's engineering challenges are fewer (lower duty cycle). Economic outcome depends on whether laser diode costs reach $0.007/W (Inertia wins) or excimer gas handling at 1 Hz is manageable (Xcimer wins).
- **Inertia vs. Marvel Fusion (concept 31, nanostructured targets)**: Marvel uses similar laser IFE chamber architecture but pursues advanced targets (nanostructured, potentially p-B11 fuel). If Marvel achieves higher gain or aneutronic fuel, it inherits Inertia's chamber/driver engineering challenges but avoids D-T tritium breeding complexity. Inertia has physics validation; Marvel does not (nanostructured target gain is undemonstrated). Inertia is the conservative path within laser IFE; Marvel is the high-risk, high-reward variant.

**Within broader fusion landscape**:
- **Inertia vs. Spherical Tokamak HTS (concept 21, Tokamak Energy)**: Both are D-T concepts commercializing proven physics (NIF ignition vs. MAST/NFRI spherical tokamak experiments). Tokamak Energy bets on HTS magnets enabling compact geometry (R = 1.5–2 m); Inertia bets on DPSSL lasers enabling high rep rate. Capital cost structure: Inertia's $1B NOAK laser vs. Tokamak Energy's ~$1.5–2B NOAK magnets → comparable. O&M: Inertia's $315M/year target cost vs. Tokamak Energy's ~$5–10M/year fuel → Inertia structurally disadvantaged. Availability: Inertia 80% (high-turnover components) vs. Tokamak Energy 85–90% (steady-state operation) → Inertia disadvantaged. LCOE: Inertia $120/MWh (NOAK optimistic) vs. Tokamak Energy ~$110–130/MWh (similar range). **Key differentiator**: Inertia has demonstrated net energy gain (NIF); Tokamak Energy has not (no burning plasma in spherical tokamak). Inertia's physics de-risking advantage is offset by IFE's structural O&M penalty.
- **Inertia vs. conventional tokamak (ITER-class D-T)**: Inertia eliminates magnets but adds consumable targets and high-frequency pulsed stress. At NOAK, roughly cost-neutral on capital; O&M disadvantaged by ~$300M/year. ITER-class LCOE projections ~$120–150/MWh → Inertia is competitive only if NOAK assumptions hold. Inertia's advantage: modular factory production enables faster learning than custom ITER-scale construction. Inertia's disadvantage: IFE has zero operational heritage; tokamaks have 70+ years of experimental validation (JET, TFTR, JT-60, etc.).

### What Makes This Concept Fundamentally Different:

**1. Only fusion concept with experimentally demonstrated net energy gain (Q > 1)**
- NIF achieved Q_sci = 4.13 (April 2025, shot N250406). Every MFE concept (tokamak, stellarator, mirror, FRC) and every other IFE concept (Xcimer, Marvel, First Light) has not demonstrated burning plasma. This is Inertia's unique value proposition: physics validation is complete; only engineering scale-up remains. The gap from Q_sci = 4.13 (at 2 MJ) to Q_sci = 52.5 (required for 1.5 GW at 10 MJ) is large but follows favorable scaling (implosion physics above ignition threshold scales superlinearly with drive energy).

**2. Cost structure dominated by consumables, not capital (inverts MFE economics)**
- MFE: ~70–80% of LCOE is capital (magnets, blanket, vessel, BOP); ~10–20% is O&M (staffing, maintenance); <5% is fuel.
- Inertia (IFE): ~50% of LCOE is capital (laser, chamber, BOP); ~40% is O&M (target materials); ~10% is financial/other. O&M fraction is 2–4× higher than MFE. This means Inertia's LCOE is more sensitive to manufacturing learning curves (target cost $1 → $0.50 = -23% LCOE) than to capital cost reductions (laser $1B → $0.5B = -11% LCOE). **Implication**: Inertia's economic outcome hinges on industrial automation (target factory) more than on materials science (magnet performance). This favors concepts with credible mass-manufacturing analogs (semiconductor diodes, lead hohlraums) over custom one-off components (HTS magnets, breeding blankets).

**3. Pulsed 10 Hz operation creates unique availability challenge (structural LCOE penalty vs. MFE)**
- MFE steady-state operation stresses components via cumulative fluence over years (divertor, first wall). IFE 10 Hz operation stresses components via pulsed thermal/mechanical loading every 0.1 seconds (chamber structure, final optics, target injection). Component lifetimes are measured in months to years (diodes: 4–9 years; chamber: 3–5 years; final optics: unknown), not decades. This creates a high-turnover maintenance model more analogous to a semiconductor fab or chemical plant than a nuclear reactor. Availability ceiling is structurally lower (80% optimistic; 70% LIFE FOAK) than MFE (85–92%). **Implication**: Even if all other costs reach NOAK targets, Inertia's LCOE will be ~10–15% higher than MFE due to availability penalty alone (elasticity -0.97). This is a fundamental disadvantage of high-rep-rate IFE, not a solvable engineering challenge.

---

## 6. Modeling Confidence

**Rating: Low**

### Parameter-by-Parameter Confidence Assessment:

| Parameter | Data Quality | Confidence Level |
|-----------|--------------|------------------|
| Laser wallplug efficiency (10%) | Explicitly stated by Inertia; single-beamline prototype demonstrated | High |
| Laser energy (10 MJ) | Explicitly stated; consistent across all sources | High |
| Repetition rate (10 Hz) | Explicitly stated | High |
| Net power (1.5 GW) | Explicitly stated | High |
| Q_sci required (~52.5) | Model-derived from above; tension with stated ">30" threshold unresolved | **Low** (blocking gap) |
| Thermal efficiency (45%) | LIFE heritage analogue (OSTI-1022881: 44%); not confirmed by Inertia | Medium |
| Availability (80%) | No operational data; LIFE targets 70% FOAK / 92% NOAK; model uses midpoint | **Low** (dominant LCOE lever) |
| Laser capital cost ($1B NOAK) | 10× learning curve from $7–10B FOAK; FOAK is handwritten estimate, NOAK is speculative | **Low** (second-largest capital item) |
| Target cost ($1/each) | Inertia goal; Goodin (2004) projects $0.41 NOAK; 6,000× reduction from current $2,500 experimental | **Low** (dominant O&M lever) |
| Chamber capital cost (~$281M) | LIFE analogue scaled; chamber is novel, unbuilt component | **Low** |
| Diode lifetime (4–9 yr current) | Haefner (2023) ILT workshop; 7–10× short of target | Medium (sourced but extrapolated) |
| Diode replacement cost ($333M) | 1/3 of $1B laser capital per Haefner (2023) | Medium |
| Construction time (6 yr) | Analyst judgment (first-of-kind IFE complexity); no Inertia guidance | Low |

**Data-anchored parameters (high confidence)**: 4 of 13 (laser specs, rep rate, net power)
**Speculative parameters (low confidence)**: 6 of 13 (Q_sci, availability, laser capital, target cost, chamber cost, construction time)
**Analogues/heritage (medium confidence)**: 3 of 13 (thermal efficiency, diode lifetime, diode replacement cost)

### Dominant Source of LCOE Uncertainty:

**Availability (80% assumption) is the dominant source of LCOE uncertainty** — elasticity -0.97 means 10% error in availability propagates to ~10% error in LCOE. Availability is entirely speculative (no 10 Hz IFE operational data). The plausible range is 65–92% (LIFE FOAK 70%, LIFE NOAK 92%, model uses 80%). This translates to LCOE range $110–160/MWh at baseline, even holding all other parameters fixed. Secondary source: target cost ($0.41–$2/target plausible range → LCOE $93–175/MWh). Tertiary: laser capital ($1–7B → LCOE $120–189/MWh).

**Combined uncertainty**: If availability, target cost, and laser capital all hit pessimistic ends of their ranges simultaneously (70% avail, $2/target, $5B laser), LCOE could exceed $280/MWh. If all hit optimistic ends (90% avail, $0.41/target, $0.5B laser), LCOE could reach ~$85/MWh. The 95% confidence interval is approximately **$85–280/MWh** — a 3.3× range. Median estimate $120/MWh should be interpreted as "central scenario assuming all learning curves hold," not "expected outcome."

### Model Validation Against Heritage:

LIFE heritage (OSTI-1022881, Anklam 2011): ~$69/MWh (2011$) at ~900 MWe NOAK with 92% availability. Scaled to 1,500 MWe and 80% availability: ~$85–95/MWh (rough adjustment). Model gives $120/MWh at 1,500 MWe / 80% avail (2026$). Gap is ~25–40% higher than LIFE.

**Drivers of model-vs-LIFE gap**:
1. LIFE assumed 92% availability; model uses 80% → +$17/MWh (availability penalty)
2. LIFE laser was 30% of COE (~$21/MWh); model laser is ~$11/MWh at $1B NOAK → model is MORE optimistic on laser cost (LIFE used flashlamp, which is cheaper than DPSSL)
3. LIFE target cost was $110M/year at 900 MWe → $183M/year scaled to 1,500 MWe; model uses $315M/year → +$12/MWh (target cost penalty vs. LIFE basis)
4. Model O&M (CAS70: $600M/yr annualized) includes inflated om_cost_dt to capture target materials; LIFE non-fuel O&M was 19% of COE (~$13/MWh) → model is higher

**Interpretation**: Model is pessimistic on availability and target cost vs. LIFE NOAK targets, but LIFE's 92% availability was a design goal, not validated. Model's $120/MWh is consistent with LIFE heritage if LIFE's NOAK assumptions (92% avail, $183M/yr targets) are replaced with more conservative estimates (80% avail, $315M/yr targets). The model is plausible as a "NOAK with execution risk priced in" scenario.

---

## 7. What Would Change My Mind

### In the optimistic direction (LCOE could reach <$100/MWh):

**1. Target factory pilot demonstration producing >10M targets/year at <$2/target by 2028**
- **Why it matters**: Target cost is the second-highest LCOE sensitivity (elasticity +0.46). If a pilot factory achieves $2/target at 10M/year scale (1% of commercial throughput), it validates the manufacturing automation pathway and suggests $0.50–1.00/target is achievable at full scale. Current experimental targets cost $2,500 → pilot target $2 is 1,250× reduction → validates half the required learning curve.
- **What I'd need to see**: Published target factory design, automated cryogenic D-T ice layering at >100 targets/hour throughput, quality control inspection at line speed, and cost breakdown showing $2/target includes hohlraum materials, capsule assembly, cryo layering, and QC.
- **Impact**: If target cost reaches $0.50/target (Goodin projection with headroom), LCOE drops from $120 → $93/MWh. Combined with 85% availability (modest improvement from 80%), LCOE reaches ~$83/MWh → competitive with new nuclear and approaching natural gas CCGT parity in high-carbon-price regimes.

**2. NIF experiments at 5–10 MJ drive demonstrating Q_sci > 30 by 2027**
- **Why it matters**: Retires the energy balance uncertainty. If NIF or a similar facility (LMJ, Omega EP upgraded) demonstrates favorable gain scaling from 2 MJ (Q_sci = 4.13) to 5–10 MJ (Q_sci > 30), it confirms that Inertia's commercial gain targets are conservative rather than optimistic. Current Q_sci = 4.13 at 2 MJ → 30 at 10 MJ is 7.3× gain improvement for 5× energy increase → favorable but unproven scaling.
- **What I'd need to see**: Peer-reviewed publication showing Q_sci > 30 at >5 MJ drive energy with Hybrid-E or similar indirect-drive target design. Bonus: demonstration of gain scaling law (Q_sci ∝ E_drive^α with α > 1).
- **Impact**: Eliminates energy balance as a blocking gap. If Q_sci = 60 is demonstrated (2× margin above 1.5 GW closure), LCOE drops from $120 → $108/MWh (small direct effect via Q_eng elasticity -0.39, but large indirect effect by reducing modular architecture uncertainty).

**3. Diode lifetime demonstration >10 GShots in accelerated testing by 2029**
- **Why it matters**: Current diodes are 7–10× short of the 14–20 GShot target; replacement every 4–9 years adds $3–7/MWh to LCOE. If diode lifetime reaches target (44–63 year replacement interval), periodic replacement cost drops to <$1/MWh, and availability ceiling rises (fewer forced outages for diode replacement). This would also validate the broader laser NOAK cost trajectory ($1B assumption).
- **What I'd need to see**: Accelerated lifetime testing protocol (high-power cycling at 10–50 Hz, elevated temperature, radiation exposure) demonstrating >10 GShot MTTF with <10% performance degradation. Commercial diode production commitment from major semiconductor manufacturers (TRUMPF, Coherent, II-VI) at >100× current volume with cost roadmap to $0.01/W.
- **Impact**: Reduces LCOE from $127 (with diode replacement penalty) → $120/MWh (base case). Indirectly enables higher availability (80% → 85%) by reducing unplanned outage frequency → combined effect ~$120 → $107/MWh.

### In the pessimistic direction (LCOE could exceed $200/MWh, concept uneconomic):

**1. Inertia publishes energy flow diagram confirming modular architecture (e.g., "four 375 MWe chambers") required for 1.5 GW**
- **Why it matters**: If single-system closure at 10 MJ / 10 Hz is infeasible (Q_sci = 30 at stated threshold → only 440 MWe/system), and modular architecture is mandatory, it implies higher capital cost (four chambers instead of one), higher O&M complexity (four target factories, four laser systems), and lower availability (N-module system availability = single-module availability^N; four 80% modules → 41% system availability). This would destroy the economic case.
- **What I'd need to see**: Inertia design documentation showing 1.5 GW plant consists of multiple independent fusion chambers (e.g., four 375 MWe modules), each with its own laser driver and target factory. Or published Q-accounting showing Q_sci = 30 is sufficient for 1.5 GW only if thermal efficiency >60% or other unstated assumptions.
- **Impact**: If four-chamber architecture is required, capital cost scales ~3× (not quite 4× due to shared BOP) → overnight cost $5,482/kW × 3 ≈ $16,000/kW → LCOE >$300/MWh. Concept becomes uneconomic vs. any baseload alternative.

**2. Final optics replacement frequency revealed as <1 year (annual or sub-annual replacement required)**
- **Why it matters**: Final focusing optics (unspecified by Inertia) must survive X-ray, neutron, and debris environment at 10 Hz. If protective scheme (grazing-incidence mirrors, disposable thin films, magnetic debris deflection) fails to extend optics lifetime beyond 1 year, annual replacement of ~1,000 beamline final optics becomes a massive O&M cost driver (comparable to target material cost). This is the "hidden" O&M risk not captured in current model.
- **What I'd need to see**: HAPL program reports or Inertia design documents showing final optics must be replaced annually due to debris coating, surface damage, or radiation-induced absorption. Cost per beamline final optics assembly >$100K × 1,000 beamlines = $100M/year additional O&M.
- **Impact**: Adds ~$9/MWh to LCOE if optics replacement is $100M/year. If replacement is quarterly (<1 year interval), could add $20–40/MWh → LCOE $140–160/MWh. Combined with pessimistic target cost ($2/target), LCOE exceeds $200/MWh.

**3. 10 Hz chamber clearing demonstrated infeasible at fusion-relevant fluence (clearing time >1 second required)**
- **Why it matters**: If chamber clearing cannot complete within 100 ms (10 Hz period), rep rate must decrease (1 Hz or lower), eliminating Inertia's quasi-steady-state thermal advantage. At 1 Hz, the concept becomes similar to Xcimer (low-rep-rate IFE) but with DPSSL laser cost penalty ($700–1,000/J vs. Xcimer's $100–120/J excimer). This would make Inertia structurally dominated by Xcimer within the IFE design space.
- **What I'd need to see**: HAPL chamber clearing experiments or simulation showing debris removal, vapor condensation, and laser beam propagation path recovery requires >1 second at 10 MJ yield scale with vaporized lead hohlraum debris. Or Inertia design documentation downgrading rep rate from 10 Hz to 1 Hz.
- **Impact**: At 1 Hz (10× lower rep rate), net power from a single 10 MJ system drops from 1,500 MWe → 150 MWe (10× fewer shots/year). To reach 1.5 GW requires 10 chambers instead of 1 → capital cost scales ~8× (shared BOP reduces scaling factor below 10×) → overnight cost ~$40,000/kW → LCOE >$500/MWh. Concept becomes economically infeasible.

---

## 8. LCOE Downselect Scoring

### C1: Modularization

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Construction Mode | Mode Score | Cost Weight | Justification |
|-------------|------------------|------------|-------------|---------------|
| CAS21 (Buildings) | Site-assembled from factory sub-assemblies | 3 | 13.4% | Standard power plant buildings; prefabricated steel structures but site-erected (analysis §model_output: CAS21 = $1,102M of $8,223M total = 13.4%) |
| CAS22 (Reactor Plant) | Mixed: laser factory (5), chamber stick-built (1) | 3.5 weighted | 37.4% | DPSSL laser: 1,000 factory-manufactured beamline modules (score 5; C220104 = $1,000M). Chamber/blanket: stick-built first wall, liquid Li piping (score 1; C220101+C220108 = $756M). Target factory: factory module (score 5; C220107 = $50M). Weighted: (1000×5 + 756×1 + 50×5) / 1806 = 3.56 |
| CAS23 (Turbine) | Factory-manufactured module | 5 | 6.2% | Standard steam turbines; mature commercial product (GE, Siemens supply); fully factory-built (CAS23 = $513M) |
| CAS24 (Electrical) | Factory-manufactured module | 5 | 2.7% | Standard electrical equipment; transformers, switchgear commercially available (CAS24 = $218M) |
| CAS26 (Heat Rejection) | Site-assembled from factory sub-assemblies | 3 | 2.4% | Cooling towers; prefabricated cells but site-erected (CAS26 = $197M) |
| CAS27 (Special Materials) | Factory-manufactured (tritium, targets) | 5 | 0.3% | D-T fuel capsules factory-manufactured (target factory); lithium commercially supplied (CAS27 = $23M) |

**Weighted average (by cost fraction):**
= (13.4%×3 + 37.4%×3.5 + 6.2%×5 + 2.7%×5 + 2.4%×3 + 0.3%×5) / (13.4%+37.4%+6.2%+2.7%+2.4%+0.3%)
= (0.402 + 1.309 + 0.310 + 0.135 + 0.072 + 0.015) / 0.623
= 2.243 / 0.623 = **3.60**

**Sub-factor 2: Module repetition boost**
- 1,000 identical laser beamlines per plant → **+1.0 boost** (10–49 identical modules per plant triggers +1.0; >49 modules provides no further benefit per framework, but 1,000 beamlines clearly satisfy "high repetition" intent)

**C1 = 3.60 + 1.0 = 4.60, clamped to [1, 5] → C1 = 4.6**

**Justification (2-3 sentences):**
The DPSSL laser driver is the dominant capital cost (37.4% of direct capital excluding financials) and consists of 1,000 factory-manufactured beamline modules — each a standardized 10 kJ, 10 Hz semiconductor-diode-pumped unit. This is the highest-repetition component in any fusion concept analyzed (analysis §model_setup: "1,000 beamlines built in factories"). The fusion chamber and blanket are stick-built (no modular analog for a 10 Hz IFE chamber exists), but turbine, electrical, and target factory are fully modular. The weighted score of 3.60 + repetition boost of 1.0 reflects Inertia's structural advantage: the largest cost item (laser) is factory-produced at semiconductor-fab scale, enabling learning curves unavailable to custom MFE magnets.

---

### C3: Supply Chain Learning

**Sub-factor A: Component learning rates (cost-weighted average across CAS accounts)**

| CAS Account | Learning Rate Category | Category Score | Cost Weight | Justification |
|-------------|----------------------|----------------|-------------|---------------|
| CAS21 (Buildings) | 5 (commodity) | 5 | 13.4% | Steel structures, concrete; established construction supply chain |
| Laser optics & structure (C220104 excl. diodes: ~$667M of $1,000M) | 3 (specialty) | 3 | 8.1% | Nd:glass gain medium, precision optics; limited fusion-IFE market but laser industry exists |
| Laser diodes (C220104 fraction: ~$333M) | 4 (industrial, growing) | 4 | 4.1% | Semiconductor diodes; consumer electronics + industrial cutting markets exist (FaceID lidar analogy per Inertia website FAQ); fusion-specific wavelengths (890 nm) are specialty but leverage broader high-power diode supply chain. 100× scale-up required (analysis §S4) but precedent in solar PV (2010–2020 scaling) |
| Chamber/blanket (C220101, C220108: ~$756M) | 2 (fusion-specific) | 2 | 9.2% | Liquid Li first wall, chamber structure for 10 Hz operation; no current market (analysis §S3: TRL 1–2) |
| Target factory (C220107: $50M) | 2 (fusion-specific) | 2 | 0.6% | Cryogenic D-T layering, hohlraum assembly at 315M/year; no analog (analysis §S2 Challenge 3: "no manufacturing analogue") |
| Tritium/fuel handling (C220106, C220110: ~$170M) | 3 (specialty) | 3 | 2.1% | Tritium processing, D-T fuel; limited market (CANDU, MFE R&D) but established technology |
| Turbine/BOP (CAS23+CAS24+CAS26: ~$928M) | 5 (commodity) | 5 | 11.3% | Steam turbines, electrical equipment, cooling towers; mature commercial markets |
| Other reactor plant (C220102, C220105, C220111, C220200-700: ~$1,100M) | 4 (industrial) | 4 | 13.4% | Vacuum systems, radiation shielding, remote handling, auxiliary systems; established nuclear/aerospace supply chains |

**Weighted average:**
= (13.4%×5 + 8.1%×3 + 4.1%×4 + 9.2%×2 + 0.6%×2 + 2.1%×3 + 11.3%×5 + 13.4%×4) / (13.4%+8.1%+4.1%+9.2%+0.6%+2.1%+11.3%+13.4%)
= (0.670 + 0.243 + 0.164 + 0.184 + 0.012 + 0.063 + 0.565 + 0.536) / 0.622
= 2.437 / 0.622 = **3.92**

**Sub-factor B: Supply chain bottleneck count**
Start at 5.0, subtract penalties:

| Bottleneck | Type | Penalty | Justification |
|------------|------|---------|---------------|
| Semiconductor laser diodes (890 nm, 100× scale-up) | Scaling constraint (10–50× scale-up) | -0.5 | Inertia explicitly states "~100× supply chain expansion" needed (analysis §S4; inertia-website-technical.md §Laser FAQ). Current high-power diode market serves industrial cutting + consumer electronics; fusion-specific wavelengths are subset. Not a hard constraint (production capacity exists) but requires 100× volume growth → -0.5 scaling penalty |
| Li-6 enrichment (if required; level unspecified) | Scaling constraint (existing but limited) | -0.5 | Natural Li is 7.5% Li-6; TBR may require enrichment (analysis §S4: "Li-6 enrichment level required" is a gap). Global enrichment capacity limited (Russian/Chinese mercury amalgam processes; Western alternatives in development per SHINE Technologies). Not a hard constraint but supply at GW-fleet scale uncertain → -0.5 scaling penalty |
| Cryogenic D-T target layering equipment | Sole-source dependency | -0.25 | Target manufacturing equipment (cryogenic layering, hohlraum assembly) has no commercial market; General Atomics + Schafer Corp are only vendors at NIF-campaign scale (analysis §S3). Industrial-scale target factory (315M/year) would require custom tooling development → -0.25 sole-source |
| Lead hohlraum materials | None | 0 | Lead is abundant (~$2/kg, millions of tonnes/year global production; analysis §S4). No bottleneck |
| Tritium startup inventory | None | 0 | Shared D-T constraint (all D-T concepts face this); not a concept-specific bottleneck. Inertia claims hundreds of grams on-site (vs. kg-scale for tokamaks) → modest advantage, no penalty |

**Bottleneck score = 5.0 - 0.5 - 0.5 - 0.25 = 3.75**

**Sub-factor C: External demand pull (% of capital in components with >$1B/yr external market)**

| Component Category | Capital Cost (M$) | External Market? | Notes |
|--------------------|------------------|------------------|-------|
| Buildings (CAS21) | 1,102 | Yes (>$1B/yr) | Power plant construction: global market >$100B/yr |
| Laser diodes (1/3 of C220104) | 333 | Yes (>$1B/yr) | High-power diode lasers: industrial cutting ($5B/yr), consumer electronics (FaceID lidar, $2B/yr), medical ($1B/yr). Fusion-specific wavelengths are subset but market exists |
| Laser optics/structure (2/3 of C220104) | 667 | Marginal (<$1B/yr) | Precision optics for high-energy lasers: industrial/defense markets exist but <$1B/yr at fusion-relevant specs (large aperture, high damage threshold). Count as NO |
| Turbines + BOP (CAS23+24+26) | 928 | Yes (>$1B/yr) | Steam turbines ($20B/yr global), electrical equipment ($50B/yr), cooling towers ($5B/yr) |
| Chamber/blanket/fuel handling (C220101, 106, 108, 110) | 1,096 | No | Fusion-specific; no external market |
| Target factory (C220107) | 50 | No | Cryogenic D-T layering; no external market |
| Other reactor plant | 1,100 | Partial (~30% yes) | Vacuum systems (semiconductor fab market, yes), radiation shielding (nuclear/medical, yes), remote handling (nuclear/aerospace, marginal). Estimate ~30% overlap → 0.3 × 1,100 = 330 |
| Preconstruction, indirects, contingency (CAS10+29+30+40+50+60) | 2,956 | Yes (>$1B/yr) | Engineering services, construction management, financing: global markets >$100B/yr |

**Total capital with external demand pull:**
= 1,102 (buildings) + 333 (diodes) + 928 (BOP) + 330 (partial reactor plant) + 2,956 (indirects) = **5,649 M$**

**Total capital (CAS10–60):** 8,223 M$ (from model_output)

**Fraction = 5,649 / 8,223 = 68.7%**

**Score (>60% → score 5):** **5**

**C3 = (3.92 + 3.75 + 5.00) / 3 = 12.67 / 3 = 4.2**

**Justification:**
Laser diodes (4.1% of capital) leverage consumer electronics and industrial laser markets ($7B/yr combined), enabling learning rates comparable to solar PV (15–20% per doubling). Turbine and BOP components (11.3% of capital) are fully commercial with mature supply chains. However, chamber/blanket (9.2%), target factory (0.6%), and specialized laser optics (8.1%) are fusion-specific with limited learning potential. Two scaling constraints exist: 100× diode volume expansion (Inertia explicitly states this is required; analysis §S4) and Li-6 enrichment capacity (limited globally, though enrichment may not be required if natural Li suffices). External demand pull is strong (68.7% of capital) due to diodes, BOP, and engineering services. Score reflects balance: modular laser benefits from external markets, but chamber and target manufacturing do not.

---

### C4: Plant Complexity

**Sub-factor A: Operational coupling density (failure cascades and maintenance dependencies)**

**Score: 2 (Highly coupled; many failure cascade paths)**

**Failure cascade analysis:**

| Subsystem | Failure Mode | Cascade Effect | Coupling Assessment |
|-----------|--------------|----------------|---------------------|
| **Laser driver (any beamline)** | Single beamline failure | If one beamline of 1,000 fails, target illumination symmetry breaks → hohlraum implosion asymmetry → failed shot → chamber contamination with unburned D-T + vaporized hohlraum debris → requires cleanup before next shot → forced outage. **Cascade: laser → target → chamber → full plant shutdown** | High coupling (single-point failure cascades to plant shutdown unless N-1 redundancy designed in; not described by Inertia) |
| **Target injection system** | Target positioning error (>±10 μm) | Laser beams miss target → no fusion → chamber exposed to full laser energy (10 MJ) with no yield → potential optics damage from reflected laser light → forced outage for optics inspection/replacement. **Cascade: target injection → optics damage → plant shutdown** | High coupling (target injection failure cascades to optics damage risk) |
| **Chamber clearing system** | Debris clearing incomplete (<100 ms) | Next target injected into debris-contaminated chamber → laser beam scattering/absorption by residual vapor → reduced laser-target coupling → low/no yield → repeat debris accumulation → forced outage to vent chamber. **Cascade: chamber clearing → target failure → multi-shot outage** | High coupling (chamber clearing failure prevents next shot) |
| **Final optics** | Optics coating/damage | Laser beam quality degrades → reduced target illumination uniformity → low yield or failed shot → same cascade as beamline failure above. **Cascade: optics → target → chamber → plant shutdown** | High coupling (optics degradation cascades to shot failure) |
| **Liquid Li tritium breeding circuit** | Li flow interruption | Loss of tritium breeding + loss of neutron energy capture → fusion yield thermal energy not recovered → gross electric drops → net electric may go negative (recirculating power 1,017 MW exceeds gross output if blanket thermal contribution lost). Plant must shut down to restore Li flow. **Cascade: Li circuit → thermal conversion → net power loss → shutdown** | High coupling (Li circuit failure cascades to net power loss) |
| **Steam turbine** | Turbine trip | Loss of electrical generation → cannot supply recirculating power (1,017 MW driver + aux) → plant shutdown. However, laser can be shut down quickly (turn off diodes) → no thermal transient damage. **Cascade: turbine → grid → controlled shutdown (low consequence)** | Moderate coupling (turbine failure requires shutdown but does not damage other subsystems) |

**Operational maintenance dependencies:**

- **Target factory outage**: If target production line fails, no targets available → plant cannot operate. Target factory is off-site (analysis §S3 implies separate facility) → maintenance independence is moderate (plant can continue if spare target inventory exists).
- **Laser diode replacement**: Requires individual beamline shutdown. If modular design allows N-1 operation (999 of 1,000 beamlines), maintenance can be performed online. If not, full plant shutdown required for diode replacement → every 4–9 years at current diode lifetime.
- **Chamber first wall maintenance**: Requires plant shutdown (must open chamber to access liquid Li piping). Inertia states "structural replacements every 3–5 years" (website FAQ) → planned outages every 3–5 years.

**Overall coupling assessment:**
Multiple single-point failures cascade to full plant shutdown (laser beamline, target injection, chamber clearing, final optics, Li circuit). No redundancy or N-1 operation capability described by Inertia. 10 Hz operation means failures propagate quickly (missed shot every 0.1 s if clearing/injection fails) rather than being recoverable within a pulse cycle. Operational coupling is higher than steady-state MFE (tokamak divertor failure does not cascade to immediate shutdown; IFE chamber clearing failure does). **Score 2: Highly coupled.**

**Sub-factor B: Subsystem count (CAS22 sub-accounts representing >1% of total capital)**

From model_output CAS22 detail, total capital = $8,223M; 1% threshold = $82M.

| CAS22 Sub-Account | Cost (M$) | >1% of Total? | Subsystem Description |
|-------------------|----------|---------------|----------------------|
| C220101 (Blanket) | 281 | Yes | Liquid Li first wall, breeding blanket |
| C220102 (Shield) | 196 | Yes | Radiation shielding |
| C220103 (Magnets) | 0 | No | N/A (IFE has no magnets) |
| C220104 (Driver) | 1,000 | Yes | DPSSL laser (1,000 beamlines) |
| C220105 (Supplemental Heating) | 13 | No | Minimal auxiliary heating |
| C220106 (Primary Coolant) | 49 | No | Below 1% threshold |
| C220107 (Target Factory) | 50 | No | Below 1% threshold |
| C220108 (Vacuum/First Wall) | 476 | Yes | Vacuum vessel, first wall structure, chamber |
| C220109 (Cryogenic) | 0 | No | N/A (no superconducting magnets) |
| C220110 (Fuel Handling) | 121 | Yes | Tritium processing, D-T fuel systems |
| C220111 (Maintenance) | 278 | Yes | Remote handling, maintenance equipment |
| C220112 (Instrumentation) | 0 | No | Minimal (included in other accounts) |
| C220200 (Heat Transport) | 302 | Yes | Intermediate heat exchangers, Li-steam interface |
| C220300 (Radioactive Waste) | 6 | No | Below 1% threshold |
| C220400 (Turbine) | 11 | No | Below 1% threshold (bulk turbine cost is CAS23) |
| C220500 (Other Reactor Plant) | 159 | Yes | Auxiliary systems, structures |
| C220600 (Instrumentation & Control) | 16 | No | Below 1% threshold |
| C220700 (Distributed Systems) | 118 | Yes | Electrical distribution, control systems |

**Count of subsystems >1% of total capital: 9**
(Blanket, Shield, Driver, Vacuum/First Wall, Fuel Handling, Maintenance, Heat Transport, Other Reactor Plant, Distributed Systems)

**Score (8–10 subsystems → score 3):** **3**

**C4 = (2 + 3) / 2 = 2.5**

**Justification:**
Operational coupling is high — failure of any of five critical subsystems (laser beamline, target injection, chamber clearing, final optics, Li circuit) cascades to full plant shutdown within one shot cycle (0.1 s). No N-1 redundancy or graceful degradation described. Subsystem count is 9 CAS22 accounts >1% of capital (moderate complexity comparable to tokamaks). However, the 10 Hz pulsed operation amplifies coupling consequences: a tokamak can tolerate brief subsystem faults within a multi-second plasma discharge, but IFE must execute target injection → laser firing → fusion → chamber clearing → repeat every 100 ms, creating many tight interdependencies. The "magic wand" test confirms this is operational complexity, not physics complexity: if fusion physics were proven (it is — NIF ignition), the plant would still be hard to operate due to high-frequency pulsed coordination requirements.

---

### C5: Customization Needs

**Sub-factor A: Thermal rejection**

**Score: 2 (Large cooling towers required, standard thermal cycle)**

**Justification:**
Inertia uses liquid Li → steam Rankine cycle → standard thermal rejection (analysis §model_setup: "Liquid Li → steam turbine"; §S3: "Steam Rankine cycle at GW scale is a fully mature commercial technology"). No direct energy conversion (DEC) — all fusion energy (neutrons + charged particles) is thermalized in the Li blanket and converted via steam turbine at ~45% efficiency (analysis §S5: LIFE analogue 44%; model uses 45%). Heat rejection load = (1 - 0.45) × 5,246 MW fusion thermal ≈ 2,885 MW thermal rejected to cooling towers (model_output: p_fus = 5,246 MW; CAS26 heat rejection = $197M). This is a standard large thermal plant (comparable to 1 GWe nuclear fission plant rejecting ~2,000 MW thermal). **Score 2: standard thermal cycle, large cooling towers.**

**Sub-factor B: Fuel safety profile**

**Score: 1 (D-T: full tritium handling and breeding infrastructure)**

**Justification:**
D-T fuel requires: (1) tritium breeding (liquid Li blanket with Li-6 neutron absorption; TBR must exceed 1.0 for fuel self-sufficiency); (2) tritium extraction from flowing Li (Maroni process or equivalent; "still an area of active development" per Inertia FAQ); (3) tritium processing (purification, storage, fueling); (4) tritium inventory management (hundreds of grams on-site per Inertia claim, unverified; analysis §S4). D-T also produces 14 MeV neutrons (80% of fusion energy) → neutron activation of chamber structure, shielding, and coolant → activated waste. No aneutronic advantage (p-B11 would score 4; D-He3 would score 3; D-D would score 2). **Score 1: D-T, full tritium infrastructure.**

**C5 (raw) = (2 + 1) / 2 = 1.5**

**C5 (scaled to [1,5]) = 1 + (1.5 - 1) × (4/3) = 1 + 0.667 = 1.67 → round to 1.7**

**Justification:**
Standard thermal cycle with large cooling towers (no DEC) and D-T fuel with full tritium breeding/extraction infrastructure (no aneutronic advantage). Thermal rejection is plant-specific (requires access to large water source or dry cooling with LCOE penalty in arid regions) but not exceptional vs. other D-T fusion or fission plants. Tritium breeding ratio (TBR = 1.59 per LIFE heritage, OSTI-1028880) is adequate but unverified for Inertia's specific chamber geometry (1,000 laser beamports subtract solid angle from breeding coverage). No site-specific advantages to inflate the score; this is an intrinsic concept characteristic.

---

### C8: Data Adequacy

**Sub-factor A: Source diversity & independence**

**Score: 2 (Almost exclusively company publications)**

**Justification:**
Three sources captured: Inertia website FAQ, ENR interview with CTO Mike Dunne, Series A press release (GlobeNewsWire). All are company-controlled or company-sourced. No peer-reviewed technical papers from Inertia (company founded 2024, 2 years old at time of analysis). No independent third-party engineering assessments. NIF ignition experiments (Kritcher et al., Nature 2022–2024) validate the Hybrid-E target physics but are LLNL publications, not Inertia publications — these establish physics heritage but do not describe Inertia's commercial plant design. LLNL LIFE program studies (Latkowski, Anklam, Moir, 2010–2013) are independent public-domain sources for IFE chamber/blanket architecture, and three LIFE reports were sourced (OSTI-1028880, OSTI-1022881, OSTI-828518 Goodin target study), providing critical heritage. However, LIFE predates ignition (2008–2013 program) and uses flashlamp driver, not DPSSL — analogy is strong for chamber/blanket but weak for laser economics. Gap report states: "Inertia Enterprises was founded in February 2024 and raised a $450M Series A in February 2026. At the time of this analysis, the company has published no engineering white papers, no formal plant study, and no peer-reviewed technical papers of its own." **Score 2: almost exclusively company publications,** with LIFE heritage providing limited independent validation for chamber/blanket subsystems only.

**Sub-factor B: Reactor design specification**

**Score: 2 (Preliminary design with significant specification gaps)**

**Justification:**
Available design specifications: laser architecture (10 MJ DPSSL, 1,000 beamlines, 10 Hz, 10% wallplug efficiency), target specs (Hybrid-E lead hohlraum, 4.5 mm diameter, <$1 cost goal), net power (50 MWe pilot, 1.5 GW commercial), energy conversion pathway (liquid Li → steam turbine), tritium breeding (liquid Li blanket, TBR unspecified by Inertia). Missing specifications: chamber geometry (radius, standoff distance, beamport configuration), first wall material, thermal efficiency (LIFE analogue 45% used in model, not confirmed by Inertia), Li-6 enrichment level, final optics approach (grazing-incidence mirrors, sacrificial lens, magnetic debris deflection — unspecified), target injection mechanism, chamber clearing approach (gas jets, xenon fill gas, other — unspecified), number of chambers for 1.5 GW (single system vs. modular unclear), Q-accounting energy flow diagram (absent; energy balance tension between stated >30× threshold and model-derived ~52.5× requirement is unresolved). Analysis gap report: "The available sources are sufficient to write a credible qualitative narrative and establish the system architecture... However, the LCOE model will be almost entirely driven by assumptions rather than data." **Score 2: preliminary design** with high-level architecture defined but significant gaps in subsystem integration and component specifications.

**Sub-factor C: LCOE parameter coverage (based on blocking gap count from gap_report.md)**

Gap report identifies the following **blocking** gaps (criticality = blocking):

1. Energy balance inconsistency (gap #1): Q_target >30× insufficient for 1.5 GW net from single system
2. DPSSL laser capital cost (gap #2): largest single capital item, no published data
3. Fusion chamber capital cost (gap #3): novel unbuilt component
4. First wall replacement schedule and cost (gap #5): no 10 Hz IFE operational data
5. O&M cost breakdown (gap #6): target material, laser diode replacement, chamber maintenance
6. Capacity factor / availability model (gap #7): no 10 Hz IFE plant has operated

**Blocking gap count: 6**

Gap #4 (target fabrication) is listed as "partially sourced" (Goodin et al. 2004 provides $0.41/target NOAK indirect-drive analogue, but Inertia's 315M/year throughput requires upward adjustment; gap report criticality = "important" not "blocking"). Gap #12 (LIFE engineering cost reports) is "partially filled" (OSTI-1022881 provides COE fraction breakdown, but full bottom-up capital cost by CAS sub-account still missing; criticality = "important").

**Score (5–7 blocking gaps → score 2):** **2**

**Sub-factor D: Commercialization pathway clarity**

**Score: 3 (General pathway described but lacking specifics)**

**Justification:**
Commercialization pathway elements identified: (1) Thunderwall DPSSL single-beamline prototype (10 kJ, 10 Hz, 10% wallplug — demonstrated per Series A press release); (2) 50 MWe pilot plant ("initially operate at 50 MWe net" per ENR interview; construction start ~2030 per press release "within the next decade"); (3) 1.5 GW commercial plant (long-term goal per website FAQ). Three development pillars named: "Thunderwall prototype, target factory prototype, plant design" (ENR interview). Funding: $450M Series A (Feb 2026) for pilot plant development. Timeline: pilot plant 2030s, commercial plant 2040s (implied, not explicit). Missing specifics: no published technical milestones (e.g., "demonstrate 10 Hz chamber clearing by 2028," "pilot target factory 10M targets/year by 2029"), no go/no-go decision criteria, no cost or schedule estimates for commercial plant, no fleet deployment plan, no utility partnership or offtake agreement announcements. NIF ignition heritage (Dec 2022, Q_sci = 1.51 → April 2025, Q_sci = 4.13) provides physics validation milestone but is LLNL work, not Inertia work. **Score 3: general pathway described** (prototype → pilot → commercial) with identified development pillars, but lacking quantitative milestones, cost/schedule estimates, and utility engagement specifics.

**C8 = (2 + 2 + 2 + 3) / 4 = 9 / 4 = 2.2 (round to nearest 0.1) → 2.2**

**Justification:**
Data adequacy is low across all dimensions. Source diversity is limited (company-only publications; LIFE heritage provides chamber/blanket validation but not laser or target manufacturing data). Reactor design is preliminary (high-level architecture clear; subsystem integration and component specs missing). LCOE parameter coverage has 6 blocking gaps (energy balance, laser capital, chamber capital, first wall replacement, O&M breakdown, availability — all speculative or absent). Commercialization pathway is outlined at high level (Thunderwall prototype → 50 MWe pilot → 1.5 GW commercial) but lacks quantitative milestones and cost/schedule detail. The company is 2 years old; absence of detailed engineering publications is expected at this stage, but it creates high LCOE modeling uncertainty. Score of 2.2 reflects "minimal public-domain data; LCOE model is assumption-driven."

---

### C7: Technical Risk Evidence (7-function × 2-subcategory risk matrix)

**Function 1: Plasma Performance (Density, temperature, confinement sufficient for net energy gain)**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier | Justification |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|---------------|
| **Physics** | Q_sci ≥ 52.5 at 10 MJ drive (required for 1.5 GW net from single system per model; stated threshold >30×) | Q_sci = 4.13 at 2.1 MJ drive (NIF shot N250406, Apr 2025; Wurzel & Hsu 2025, arxiv-2505-03834v5) | 12.7× (52.5 / 4.13) | Favorable gain scaling from 2 MJ → 10 MJ: implosion physics above ignition threshold scales superlinearly with drive energy (power-law Q ∝ E^α, α > 1 observed in NIF progression from Q=1.51 to 4.13 over 2.5 years). NIF experiments at 5–10 MJ would validate scaling law. | Degrading (if Q_sci = 30 at 10 MJ per stated threshold, net power drops to ~440 MWe → capacity underutilization → LCOE $255/MWh; modular architecture required to reach 1.5 GW) | **4** (Near-regime demonstrated: 4.13 at 2 MJ is within 3× of interim milestone Q~15 at 5 MJ; extrapolation to 52.5 at 10 MJ is 2.5× further) | NIF ignition demonstrated with 8 shots Q_sci > 1 (Dec 2022 → Apr 2025); peak Q = 4.13. Hybrid-E target design (Kritcher et al., Nature 2022) validated. Gap from 4.13 → 52.5 is large but scaling is physically favorable (higher drive energy → higher compression → higher temperature → superlinear gain increase). Conservative tier 4 (near-regime) because 10 MJ drive is 5× energy increase from demonstrated 2 MJ, and commercial Q_sci requirement (52.5) is 12.7× higher than demonstrated (4.13). |
| **Hardware** | Target fabrication: Hybrid-E lead hohlraum with cryogenic D-T ice layer, sub-mm surface roughness tolerance, delivered at 10 Hz (315M/year) with ±10 μm positioning accuracy | NIF-campaign targets: ~100 hohlraums/year at $2,500 each with manual cryogenic layering (General Atomics); positioning accuracy ±10 μm validated at ~1 shot/hour (NIF operations) | 3.15M× throughput gap (315M/year ÷ 100/year); 6,000× cost gap ($2,500 → $0.41 NOAK per Goodin 2004) | Mass production automation: Goodin et al. (2004) projects $0.41/target NOAK for indirect drive at 182M/year with $97M factory capital. Inertia's 315M/year is 73% higher throughput → factory capital $150–200M. Cryogenic layering automation at >100 targets/hour (vs. current ~1/day). Lead hohlraum assembly simpler than gold (material cost $2/kg vs. $90,000/kg). | Degrading (if target cost reaches $2/target vs. $1 goal, O&M cost doubles → LCOE $175/MWh; at $5/target, LCOE >$250/MWh → uneconomic) | **3** (Subscale demonstration: NIF campaign targets validate physics and cryogenic D-T layering at low throughput; Goodin (2004) provides manufacturing cost model but no industrial-scale validation) | NIF targets demonstrate required quality (surface roughness <1% for Rayleigh-Taylor suppression, cryogenic D-T ice uniformity). Gap is throughput automation (100/year → 315M/year) and cost reduction ($2,500 → <$1). Goodin (2004) bottom-up projection of $0.41 NOAK is credible (6,100× reduction from experimental cost) but unvalidated. Tier 3 (subscale) because manufacturing process is demonstrated at small scale but industrial automation at 315M/year has no precedent. |

**F1 (mean) = (4 + 3) / 2 = 3.5**

---

**Function 2: Driver / Energy Input (Heating, compression, or catalytic species delivery)**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier | Justification |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|---------------|
| **Physics** | 10 MJ laser energy delivered to hohlraum with pulse shaping (temporal profile, spectral bandwidth) adequate for uniform capsule implosion; 1,000-beamline synchronization to single target within ±10 μm pointing tolerance | NIF: 1.8–2.1 MJ delivered to target with 192 beamlines; pointing tolerance ±10 μm demonstrated; pulse shaping validated for Hybrid-E target (Kritcher et al. 2022) | 4.8× energy gap (10 MJ / 2.1 MJ); 5.2× beamline count gap (1,000 / 192) | Thunderwall DPSSL beamline: 10 kJ per beamline at 10 Hz with 10% wallplug efficiency demonstrated (GlobeNewsWire Series A press release, Feb 2026). Array scaling: 1,000 beamlines → 10 MJ total. Pulse shaping and synchronization at array scale is engineering challenge (not physics). NIF demonstrates 192-beamline synchronization; 1,000-beamline is 5× larger but same technology (fiber optics, timing electronics). | Degrading (if laser energy falls short of 10 MJ or pulse shaping degrades at scale, Q_sci drops → net power shortfall; can compensate with higher Q_sci or modular architecture) | **4** (Near-regime demonstrated: single Thunderwall beamline validated at 10 kJ, 10 Hz; NIF validates 192-beamline synchronization; gap is array integration at 1,000 beamlines — incremental engineering, not fundamental physics) | Thunderwall prototype demonstrated at 10 kJ, 10 Hz, 10% wallplug (analysis §S3: "world's first grid-scale fusion laser beamline"). NIF validates laser-target coupling physics at 2 MJ with 192 beamlines. Gap from 192 → 1,000 beamlines is engineering (fiber distribution, timing synchronization, beam pointing control) with no fundamental physics barrier. Tier 4 (near-regime) because single beamline is proven, and NIF shows multi-beamline synchronization is achievable; 1,000-beamline integration is incremental scale-up. |
| **Hardware** | DPSSL laser: 1,000 beamlines × 10 kJ each, 10 Hz rep rate, 10% wallplug efficiency, 30-year operational lifetime with modular beamline replacement. Laser diodes: 14–20 GShot MTTF (44–63 year lifetime at 10 Hz). Final optics: survive X-ray, neutron, debris environment at 10 Hz for ≥1 year before replacement. | Thunderwall: 10 kJ, 10 Hz, 10% wallplug demonstrated (single beamline). Laser diodes: 1.4–2.9 GShot MTTF (4.4–9.2 year lifetime at 10 Hz, per Haefner 2023 ILT workshop). Final optics: no 10 Hz fusion-relevant validation (HAPL program tested kJ-scale shots at <1 Hz; NRL/LANL grazing-incidence mirrors at laboratory scale). | Diode lifetime: 7–10× gap (14–20 GShot ÷ 1.4–2.9 GShot). Final optics: no demonstrated solution at 10 Hz IFE fluence (gap ratio N/A). | Diode lifetime: incremental semiconductor R&D (facet passivation, thermal management, optical coatings) to extend MTTF from ~2 GShot → 14 GShot. Precedent in LED lifetime improvements (2000s: 10,000 hr → 2020s: 50,000 hr = 5× improvement via packaging + materials). Final optics: protective schemes under study (grazing-incidence metal mirrors, sacrificial thin films, magnetic debris deflection); no validated solution at 10 Hz + 10 MJ yield. Inertia has not disclosed approach. | Binary (if diode lifetime remains at current 4–9 year replacement, periodic capital $333M every 4–9 years is manageable but adds $3–7/MWh to LCOE — degrading not binary. If final optics have <1 year lifetime, annual replacement cost could exceed $100M/year → $9/MWh penalty — degrading. If final optics fail catastrophically with no replacement scheme, plant cannot operate → binary.) | **3** (Subscale demonstration: Thunderwall single beamline validated; diode lifetime gap is incremental R&D with precedent; final optics have no IFE-relevant validation but HAPL program provides laboratory-scale data) | Thunderwall demonstration (10 kJ, 10 Hz, 10%) proves DPSSL beamline concept. Diode lifetime is 7–10× short of target but improving (Haefner 2023 identifies this as solvable via semiconductor process development, not fundamental physics limit). Final optics are unvalidated at 10 Hz IFE conditions — this is the highest hardware risk. HAPL (NRL/LANL) studied grazing-incidence mirrors and xenon gas protection but did not validate at 10 MJ yield × 10 Hz duty cycle. Tier 3 (subscale) because single beamline is validated and diode lifetime gap is incremental, but final optics have no fusion-relevant demonstration at commercial rep rate. |

**F2 (mean) = (4 + 3) / 2 = 3.5**

---

**Function 3: Instability Control (Suppression or tolerance of intrinsic plasma instabilities)**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier | Justification |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|---------------|
| **Physics** | Rayleigh-Taylor instability suppression during capsule implosion: surface roughness <1%, X-ray drive uniformity ±1%, implosion symmetry adequate for central hot spot formation at 10 MJ drive | NIF Hybrid-E: Rayleigh-Taylor suppression validated at 2.1 MJ drive with Q_sci = 4.13 (Apr 2025). Surface roughness <1% achieved via precision capsule fabrication. Indirect drive provides X-ray bath uniformity superior to direct drive (12% coupling efficiency penalty is trade-off for RT stability). | 1.0× (no gap; RT physics validated at ignition-regime; scaling to 10 MJ is favorable — higher drive energy → faster implosion → less RT growth time) | Indirect drive architecture inherently provides RT stability via hohlraum X-ray bath uniformity (NIF design choice). Hybrid-E target (Kritcher design) optimized for RT suppression. Commercial targets use same physics (lead hohlraum, cryogenic D-T ice, precision surface finish). | Degrading (if RT instability grows at 10 MJ scale due to unforeseen scaling effects, capsule fails to compress → low/no yield → net power shortfall; can compensate with improved target design or higher drive energy) | **5** (Operating-regime demonstrated: NIF Hybrid-E achieved ignition (Q > 1) with 8 shots, demonstrating RT suppression is sufficient for net gain at ignition-relevant conditions. Scaling to 10 MJ is favorable for RT (faster implosion → less growth time).) | RT instability is the dominant physics challenge for ICF; NIF ignition (Dec 2022 → Apr 2025, Q_sci = 1.51 → 4.13) proves RT is controlled at ignition conditions. Indirect drive (hohlraum X-ray bath) provides superior uniformity vs. direct drive, at cost of 12% coupling efficiency. Commercial targets at 10 MJ use same Hybrid-E design physics; RT growth rate decreases with faster implosion (higher drive energy), so scaling is favorable. Tier 5 (operating-regime) because RT suppression is demonstrated at ignition-relevant conditions and scaling to higher energy is physically favorable. |
| **Hardware** | Target capsule: cryogenic D-T ice layer uniformity <1% variation, surface roughness <1 μm RMS, hohlraum X-ray emission uniformity ±1%. Target must survive injection at 10 Hz (ballistic or sabot delivery) and arrive at chamber center with ±10 μm positioning accuracy. | NIF targets: D-T ice uniformity <1% and surface roughness <1 μm achieved via Beta-layering technique (slow rotation + thermal gradient). Hohlraum X-ray uniformity validated with Hybrid-E lead hohlraum (Kritcher et al. 2022). Positioning: ±10 μm demonstrated at ~1 shot/hour (NIF target insertion). 10 Hz injection: not demonstrated (HAPL studied gas-gun injection at laboratory scale; no fusion-relevant validation). | Ice uniformity: 1.0× (no gap). Target injection at 10 Hz: gap ratio N/A (never demonstrated at IFE scale). | Cryogenic ice layering: Beta-layering or equivalent at high throughput (Goodin 2004 assumes automated layering at 182M/year; Inertia's 315M/year requires faster cycle time but same physics). Target injection: gas-gun, electromagnetic rail, or sabot delivery at 10 Hz with ±10 μm accuracy. HAPL program (NRL) studied injection; no IFE demonstration at fusion yield + 10 Hz. | Binary (if target injection fails to achieve ±10 μm accuracy, laser beams miss target → no fusion → full laser energy (10 MJ) deposited in chamber with no yield → potential optics damage + chamber contamination → plant shutdown until injection is fixed) | **3** (Subscale demonstration: NIF validates target quality (ice uniformity, surface finish, hohlraum performance) at low throughput. Target injection at 10 Hz with ±10 μm accuracy has no IFE demonstration; HAPL laboratory-scale studies provide partial validation.) | NIF demonstrates that target quality (ice uniformity, surface roughness, hohlraum X-ray uniformity) can meet RT suppression requirements. Gap is high-throughput automated target production (315M/year) and 10 Hz injection with ±10 μm positioning accuracy. Target injection is critical: if accuracy degrades, laser-target coupling fails → shot failure → binary risk (no fusion). HAPL (NRL/LANL) studied gas-gun injection and tracking at <1 Hz; no validation at 10 Hz + fusion yield. Tier 3 (subscale) because target quality is validated at NIF but injection at commercial rep rate is undemonstrated. |

**F3 (mean) = (5 + 3) / 2 = 4.0**

---

**Function 4: Plasma-Wall Interaction (Erosion, heat flux management, surface damage)**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier | Justification |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|---------------|
| **Physics** | Chamber clearing within 100 ms (10 Hz period): remove vaporized hohlraum debris (~1–5 g Pb per shot), D-T ash, ablator material, residual vapor from chamber atmosphere to allow next target injection and clean laser beam propagation. X-ray and debris energy deposition in liquid Li first wall and gas fill (if present) must not prevent shot-to-shot recovery. | HAPL program (NRL/LANL): chamber clearing studied at <1 Hz with kJ-scale shots. Gas jets and xenon fill gas (6 g/cc per LIFE design, OSTI-1028880) demonstrated for ion debris stopping at laboratory scale. No validation at 10 MJ yield × 10 Hz duty cycle. First Light Fusion (projectile ICF): liquid Li first wall at low rep rate (~0.1 Hz). | 100× rep rate gap (10 Hz vs. 0.1 Hz demonstrated). Energy gap: 10 MJ vs. kJ-scale HAPL experiments = 10,000× energy/shot. | Xenon fill gas (LIFE design): 6 g/cc Xe stops ions from hohlraum vaporization within ~1 m radius, protecting first wall from direct ion damage. Debris falls to liquid Li pool or is swept by gas jets. Laser beam propagation path maintained via beam ports with differential pressure or magnetic deflection. Chamber clearing time scales with gas flow rate and debris settling time — 100 ms is engineering target, not fundamental limit. | Degrading (if clearing requires >100 ms, rep rate drops from 10 Hz → lower frequency → net power drops proportionally → capacity underutilization → LCOE penalty. If clearing >1 s required, rep rate drops to <1 Hz → concept converges to Xcimer-style low-rep-rate IFE → DPSSL laser cost penalty vs. excimer makes concept uncompetitive) | **2** (Simulation only: HAPL program modeled chamber clearing with gas dynamics codes; xenon fill gas approach is analyzed but not validated at 10 MJ yield × 10 Hz. Laboratory-scale experiments at kJ-level provide partial validation but 10,000× energy gap is huge.) | HAPL (NRL/LANL) studied chamber clearing with computational fluid dynamics (gas jet flow, debris transport, vapor condensation). LIFE design (OSTI-1028880) specifies xenon fill gas at 6 g/cc for ion stopping. No experimental validation at 10 MJ yield and 10 Hz rep rate. First Light Fusion operates liquid Li chamber at ~0.1 Hz (100× slower than Inertia's 10 Hz). Chamber clearing at 10 Hz is the hardest unvalidated engineering challenge in the concept. Tier 2 (simulation only) because HAPL modeling exists but no IFE experiment has validated clearing at fusion-relevant yield and commercial rep rate. |
| **Hardware** | Liquid Li first wall: survive repeated impulsive loading (X-rays + neutrons + debris, ~450 MJ fusion energy per shot at 10 Hz). Structural integrity of Li-carrying pipes under pulsed pressure/thermal shock. First wall material (unspecified) must tolerate 14 MeV neutron fluence + erosion from debris impact. Laser beam ports must remain optically clean (no Li vapor, debris coating, or condensation on beam path). | Liquid Li loops: laboratory-scale experiments in fission/fusion programs (TFTR, JET, FLiBe test stands). First Light Fusion: liquid Li first wall at low rep rate + low yield. No 14 MeV neutron fluent, high-rep-rate IFE chamber has been built. First wall materials for IFE: tungsten, SiC, ODS steel studied analytically; no 10 Hz validation. | Rep rate gap: 10 Hz vs. 0.1 Hz (100×). Fluence gap: 10 Hz × 450 MJ/shot × 30 years = 4.3×10^11 J neutron fluence integrated over plant life vs. zero for any demonstrated IFE chamber. | LIFE first wall design: liquid Li flowing through pipes lining chamber inner surface, with xenon gas fill for debris/ion stopping. Structural materials (ferritic steel or ODS steel per LIFE studies) must survive pulsed thermal/mechanical loading. Chamber geometry: spherical radius ~4–5 m (LIFE.1 = 3.4 m, LIFE.2 = 5.7 m per OSTI-1028880) provides standoff distance from target. First wall replacement every 3–5 years per Inertia website FAQ (unverified; no data basis). | Binary (if first wall fails structurally due to pulsed fatigue or neutron embrittlement, chamber loses vacuum integrity or Li coolant leaks → plant shutdown for chamber replacement. If Li vapor or debris contaminates laser beam ports, beam propagation fails → shot failure → operational binary failure until ports cleaned.) | **1** (Asserted/absent: Inertia states "structural replacements every 3–5 years" but provides no engineering basis. LIFE chamber design exists (OSTI-1028880) but assumes flashlamp driver (not DPSSL), and LIFE was never built. No IFE chamber has operated at 10 Hz with 14 MeV neutron fluence.) | LIFE studies (OSTI-1028880) provide chamber design concept (liquid Li, xenon fill, spherical geometry) but this is pre-conceptual (2010–2013, before NIF ignition). No material or structural validation at 10 Hz pulsed loading + 14 MeV neutron fluence. First wall material is unspecified by Inertia. Chamber clearing (100 ms shot-to-shot recovery) and beam port cleanliness are unvalidated. This is the highest-risk hardware item in the plant. Tier 1 (asserted) because Inertia claims 3–5 year first wall life with no supporting data, and no IFE chamber exists at any rep rate to validate. |

**F4 (mean) = (2 + 1) / 2 = 1.5**

---

**Function 5: Neutron/Particle Handling (Activation, shielding, displacement damage)**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier | Justification |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|---------------|
| **Physics** | 14 MeV neutron transport from point-source fusion target (isotropic emission) to liquid Li first wall (~4–5 m radius). Neutron energy deposition in Li (80% of fusion energy = 360 MJ thermal per shot). Activation of chamber structure, shielding, and Pb hohlraum debris under 14 MeV neutron irradiation. | NIF: 14 MeV neutron yield up to ~10^19 neutrons per shot (Q_sci = 4.13 → 8.6 MJ fusion yield → ~1.5×10^19 n/shot). Neutron transport validated via Monte Carlo (MCNP) for NIF target chamber (~5 m radius aluminum chamber). Activation of NIF chamber documented (Al-26, Na-24 from Al structure). No data on lead activation under 14 MeV neutrons at high rep rate. | 1.0× (neutron transport physics fully validated at NIF; commercial plant uses same 14 MeV neutron spectrum). Fluence gap: NIF fires ~50 shots/year → 5×10^20 n/year; Inertia 10 Hz × 1.5×10^19 n/shot → 4.7×10^27 n/year = 10^7× higher integrated fluence. | Neutron transport: well-understood physics (Monte Carlo codes MCNP, TRIPOLI validated against NIF, OMEGA, fission reactors). Liquid Li neutron energy capture: exothermic Li-6(n,T)He-4 reaction well-characterized. Chamber energy gain mn = 1.10 (LIFE baseline, OSTI-1028880) from neutron multiplication in Li. Activation: lead activation products (Pb-204 → Bi-205, etc.) are known; manage as activated waste. | Degrading (neutron shielding must protect personnel and electronics; if inadequate, occupational dose limits exceeded → restricted access → maintenance complexity ↑ → availability ↓. Activated Pb debris must be managed as radioactive waste — if waste volume exceeds Class C limits, disposal cost ↑ → O&M penalty.) | **4** (Near-regime demonstrated: NIF validates 14 MeV neutron transport and activation physics at ignition-relevant yield per shot. Fluence scaling to commercial plant (10^7× higher integrated fluence) is linear extrapolation — no new physics, but materials performance under cumulative damage is engineering challenge (covered in hardware subcategory).) | 14 MeV neutron transport is well-understood; NIF provides experimental validation at fusion-relevant yield (~10^19 neutrons/shot). Commercial plant has 10^7× higher integrated fluence over 30 years, but neutron physics does not change — only cumulative materials damage (addressed in hardware). Liquid Li energy capture (mn = 1.10) is validated via LIFE neutronics studies (OSTI-1028880). Activation of Pb hohlraum debris is calculable (nuclear data libraries for Pb isotopes well-characterized). Tier 4 (near-regime) because neutron physics is demonstrated at NIF, and commercial fluence is extrapolation, not new regime. |
| **Hardware** | Radiation shielding: protect personnel (dose <0.5 mSv/hr at plant boundary) and electronics (dose <10^4 Gy total over 30 years for control systems). First wall and chamber structure: survive displacement damage (dpa) from 14 MeV neutrons. Activated materials: manage as Class C or lower radioactive waste (disposal pathway exists; cost acceptable). | NIF: biological shielding (concrete, borated polyethylene) adequate for ~50 shots/year at 10^19 n/shot. No high-rep-rate IFE shielding validation. Displacement damage: fission reactor materials (ferritic steel, ODS steel) characterized to ~100 dpa; 14 MeV neutrons cause ~2× higher dpa per fluence vs. fission spectrum. IFE chamber at 10 Hz × 450 MJ/shot × 30 yr: ~50–200 dpa at first wall (order-of-magnitude estimate; depends on geometry). | Shielding: 10^7× fluence gap (NIF 50 shots/yr vs. Inertia 3.15×10^8 shots/yr). Displacement damage: 14 MeV dpa data exists from fission experiments (FFTF, HFIR with D-T neutron source) but not at IFE-relevant fluence + pulsed loading. | Shielding: scale up NIF shielding thickness (concrete + borated poly) to handle 10^7× higher fluence — primarily a matter of cost (thicker shield → higher CAS220102 shield capital). Displacement damage: first wall replacement every 3–5 years (Inertia claim) limits cumulative dpa to ~10–30 dpa per component life (well within ferritic steel tolerance if true). Activated waste: lead hohlraum debris + chamber structure activation managed as Class C waste (similar to fission reactor decommissioning waste). | Degrading (if shielding inadequate, occupational dose → access restrictions → lower availability. If first wall dpa exceeds material limits, replacement frequency ↑ from claimed 3–5 years → O&M cost ↑. If activated waste exceeds Class C, disposal cost ↑.) | **3** (Subscale demonstration: Fission reactors and NIF provide 14 MeV neutron damage data at low/moderate fluence. IFE-specific pulsed loading + high fluence (50–200 dpa at 10 Hz duty) is unvalidated. Shielding design is straightforward scaling from NIF but not demonstrated at commercial rep rate.) | Radiation shielding is mature technology (concrete, borated polyethylene, steel); NIF demonstrates shielding at low rep rate. Scaling to 10 Hz × 30 years requires thicker shielding (higher cost) but no new materials. Displacement damage: ferritic steel and ODS steel characterized to ~100 dpa in fission reactors; IFE first wall at 10 Hz × 30 yr with 3–5 year replacement reaches ~10–30 dpa/component (within material limits if replacement schedule holds). Uncertainty: pulsed 14 MeV neutron damage (10 Hz thermal/mechanical cycling) may accelerate fatigue vs. steady-state fission irradiation — no data. Tier 3 (subscale) because fission and NIF provide neutron damage data but IFE-specific pulsed high-fluence regime is unvalidated. |

**F5 (mean) = (4 + 3) / 2 = 3.5**

---

**Function 6: Fuel Cycle Closure (Breeding, extraction, purification, recycling)**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier | Justification |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|---------------|
| **Physics** | Tritium breeding ratio (TBR) ≥ 1.05 (accounting for decay, processing losses, inventory). Liquid Li blanket with Li-6(n,T)He-4 exothermic reaction provides tritium + energy gain mn = 1.10. Chamber geometry (spherical with laser beam ports for 1,000 beamlines) must provide adequate solid angle coverage for breeding. | LIFE design: TBR = 1.59 with liquid Li blanket, spherical chamber, 192 beamlines (NIF-scale beamport geometry per OSTI-1028880). Li-6(n,T)He-4 cross-section well-characterized. Inertia has 1,000 beamlines → more solid angle subtracted from breeding coverage vs. LIFE 192 beamlines → TBR likely lower than 1.59 but still >1.05 (derivable via neutronics). | 1.0× (breeding physics validated; TBR scaling from 192 → 1,000 beamports is calculable via Monte Carlo neutronics) | Monte Carlo neutronics (MCNP, TRIPOLI): calculate TBR for Inertia's 1,000-beamline geometry. LIFE achieved TBR = 1.59 with 192 beamports; Inertia's 1,000 beamports subtract more solid angle but spherical geometry + Li-6 enrichment (if used) can compensate. Li-6 enrichment from natural 7.5% → 30–60% increases TBR (trade-off: enrichment cost vs. breeding margin). | Binary (TBR < 1.0 → cannot breed sufficient tritium → external tritium purchase required → fuel cost ↑ 100× (~$30k/g tritium from CANDU) → economically infeasible. TBR 1.0–1.05 → marginal (decay + losses barely compensated) → plant cannot start up successor plants (tritium doubling time >30 years) → fleet deployment blocked.) | **4** (Near-regime demonstrated: LIFE neutronics (OSTI-1028880) validates TBR > 1.5 for liquid Li blanket with similar indirect-drive geometry. Inertia's 1,000 beamlines reduce TBR but >1.05 is achievable with Li-6 enrichment or optimized blanket thickness. Neutronics codes well-validated.) | LIFE achieved TBR = 1.59 with liquid Li first wall and 192 laser beamports (OSTI-1028880 §V.A). Inertia has 1,000 beamports → more solid angle subtracted → TBR will be lower but >1.05 is achievable (Li-6 enrichment or thicker blanket compensates). Breeding physics (Li-6 cross-section, neutron multiplication) is well-characterized. Gap: Inertia has not published TBR calculation for 1,000-beamline geometry, but this is derivable via MCNP. Tier 4 (near-regime) because LIFE validates breeding in similar geometry and Inertia's TBR is calculable (not a new physics regime). |
| **Hardware** | Tritium extraction from flowing liquid Li: recover >90% of bred tritium at throughput sufficient for 10 Hz operation (~100–200 g T/day production to maintain steady-state inventory + losses). Tritium processing: purification, isotope separation (D-T), storage, fueling. On-site inventory: Inertia claims "hundreds of grams" vs. "20× more" for tokamaks (→ tokamak ~kg-scale, Inertia ~300–500 g). | LIFE design: Maroni process (vacuum permeation extraction from Li) achieves ~40 g tritium inventory within Li loops at 100 wppb concentration (OSTI-1028880 §IV). Tritium extraction validated in fission breeder programs (FFTF, EBR-II) at laboratory scale (~g/day). JET/TFTR operated with D-T fuel at ~10 g/shot tritium fueling; tritium processing (ISS, WDS) demonstrated at fusion-relevant purity. No IFE-specific tritium extraction at 10 Hz + 100–200 g/day throughput. | Throughput gap: 100–200 g T/day (Inertia commercial plant) vs. ~1 g/day (JET/TFTR campaigns). Extraction rate gap: 100× higher than laboratory-scale fission breeder experiments. | Maroni process scaling: vacuum permeation modules in parallel to handle Inertia's Li flow rate (~10^4 kg/s for GW thermal scale). Tritium permeability through Li-contacting heat exchanger walls must be minimized (double-wall with He purge gas or cold trap). Inertia FAQ states tritium extraction "is still an area of active development" — acknowledges this is unresolved but claims it is solvable. | Binary (if tritium extraction fails to achieve ≥90% recovery, bred tritium is lost to waste → TBR_effective < 1.0 → must purchase makeup tritium externally → economically infeasible. If extraction works but inventory is >kg-scale (not hundreds of grams), regulatory/safety classification worsens → licensing penalty.) | **3** (Subscale demonstration: Maroni process demonstrated in LIFE design studies (40 g inventory, 100 wppb in Li loops) and fission breeder experiments at ~g/day scale. Scaling to 100–200 g/day is engineering (larger permeation area, higher Li flow rate) but no IFE validation at commercial throughput.) | LIFE tritium system design (OSTI-1028880 §IV) provides detailed engineering basis: Maroni vacuum permeation extraction achieves 40 g inventory in Li loops at 100 wppb. Tritium recovery from Li is well-studied in fission breeder programs (EBR-II, FFTF). Gap: Inertia's 10 Hz operation at GW scale requires 100–200 g T/day throughput (10× higher than LIFE 900 MWe). Inertia FAQ explicitly states extraction "is still an area of active development" — company acknowledges gap. Tier 3 (subscale) because tritium extraction physics and Maroni process are demonstrated at laboratory scale, but commercial IFE throughput (100–200 g/day) is unvalidated. |

**F6 (mean) = (4 + 3) / 2 = 3.5**

---

**Function 7: Power Conversion & BOP (Energy conversion, heat rejection, auxiliaries)**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier | Justification |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|---------------|
| **Physics** | Thermal energy transport from pulsed fusion source (10 Hz, 450 MJ/shot → 4.5 GW thermal average power) via liquid Li coolant to steam cycle. Thermal buffering to smooth 10 Hz pulses into continuous steam supply. Heat rejection of ~2.9 GW thermal (55% of fusion power at 45% thermal efficiency) via cooling towers or water source. | Pulsed thermal systems: coal/gas peaker plants handle load-following (minutes to hours timescale). 10 Hz thermal pulse (0.1 s period) is well above steam system thermal time constants (seconds to minutes for steam drums, heat exchangers) → effectively continuous thermal load from steam cycle perspective. LIFE design (OSTI-1028880): liquid Li primary loop → intermediate heat exchanger → steam cycle at 800°C Li exit temp, 44% thermal efficiency. | 1.0× (thermal physics validated; pulsed operation at 10 Hz does not create new thermal challenges vs. steady-state) | Standard steam Rankine cycle (GE, Siemens turbines): TRL 9. Liquid-Li-to-steam heat exchanger: fission reactor and MFE blanket R&D provides precedent (LIFE design, FLiBe loops). Thermal buffering: large Li inventory + intermediate heat exchanger provide thermal mass to smooth pulses. Heat rejection: cooling towers at GW scale are standard power plant equipment. | Degrading (if thermal efficiency falls short of 45%, gross electric drops → net power shortfall → capacity underutilization. If heat rejection requires excessive water (arid site) or dry cooling (LCOE penalty ~$5–10/MWh), site customization penalty.) | **5** (Operating-regime demonstrated: Steam Rankine cycle at GW scale is fully commercial (every coal, gas, nuclear fission plant worldwide). Liquid metal coolant integration validated in fission reactors (sodium, lead-bismuth) and MFE blanket experiments (ORNL FLiBe loops). LIFE design (OSTI-1028880) provides detailed IFE integration study.) | Steam turbines at GW scale: TRL 9 (GE, Siemens, Mitsubishi supply global fleet). LIFE program (OSTI-1028880 §IV) designed liquid-Li-to-steam heat exchanger with 800°C Li exit temp → 44% thermal efficiency (model uses 45%; conservative). Pulsed operation at 10 Hz (0.1 s period) is effectively continuous for steam cycle (thermal time constants ~seconds for heat exchangers, ~minutes for steam drums → 10 Hz pulses are high-frequency compared to thermal response). Heat rejection: cooling towers or water source at ~2.9 GW thermal (model: 5,246 MW fusion - 1,500 MW net - recirculating = ~2,900 MW rejected). Tier 5 (operating-regime) because steam cycle is fully commercial and LIFE provides IFE-specific integration design. |
| **Hardware** | Steam turbine: 2,595 MW gross electric output (model_output: p_et = 2,595 MW at q_eng = 2.37) at ~45% thermal efficiency. Intermediate heat exchanger: liquid Li (primary) to steam (secondary) with tritium permeation barrier (double-wall or cold trap). Cooling towers: ~2.9 GW thermal rejection. Electrical distribution: 1,500 MW net to grid; 1,017 MW recirculating power (laser driver 1,000 MW + aux 17 MW). | GE/Siemens steam turbines: 1–2 GW gross output commercially available (standard nuclear/coal plant equipment). Liquid metal heat exchangers: sodium-water IHX in fission fast reactors (BN-600, SuperPhenix); no Li-water IHX at GW scale (LIFE design is pre-conceptual). Cooling towers: 3+ GW thermal rejection at large nuclear plants (Vogtle, Barakah). Electrical distribution: standard power plant substation equipment. | 1.0× (turbine and cooling towers are direct commercial analogs). Li-water IHX: no GW-scale demonstration (LIFE is paper design); laboratory-scale Li loops exist (ORNL, INL). | Steam turbine: procure from GE, Siemens, Mitsubishi (off-the-shelf). Li-water IHX: scale up LIFE design (OSTI-1028880 §IV) or use intermediate loop (Li → molten salt → water to isolate tritium). Tritium permeation: double-wall IHX with He purge gas or cold trap on steam side (fission reactor precedent). Cooling towers: standard design (Hamon, SPX Cooling). | Degrading (if IHX fails (tritium leaks into steam → environmental release), plant shuts down for IHX replacement → O&M cost + availability penalty. If cooling tower capacity undersized, turbine backpressure ↑ → thermal efficiency ↓ → net power ↓.) | **4** (Near-regime demonstrated: Steam turbine, cooling towers, electrical distribution are fully commercial (TRL 9). Li-water IHX is undemonstrated at GW scale but LIFE provides detailed design (OSTI-1028880) and fission reactors validate liquid-metal-to-water heat exchange at 100s of MW thermal scale. Scaling from 100 MW to GW is incremental engineering.) | Steam turbine (2.6 GW gross electric) is standard equipment (GE supplies 1–2 GW turbines for nuclear/coal plants; Inertia's 2.6 GW is large but not unprecedented). Li-water intermediate heat exchanger: LIFE design (OSTI-1028880 §IV) specifies double-wall IHX with He purge to prevent tritium migration; no GW-scale demonstration but fission fast reactors (BN-600, SuperPhenix) validate sodium-water IHX at 100s of MW scale. Cooling towers at 2.9 GW thermal: standard for large nuclear plants (Vogtle units 3&4: ~6 GW thermal total = 3 GW per unit). Electrical distribution (1,500 MW net to grid, 1,017 MW recirculating): standard substation equipment. Tier 4 (near-regime) because turbine/cooling are fully commercial and IHX is demonstrated at subscale with clear scaling path. |

**F7 (mean) = (5 + 4) / 2 = 4.5**

---

### Binary Risks Summary

From the 14-cell risk matrix above, risks classified as **binary** (zero net electricity if unmitigated):

1. **F2 (Driver/Energy Input) - Hardware**: Final optics failure with no replacement scheme → plant cannot operate (laser beams cannot reach target).
2. **F3 (Instability Control) - Hardware**: Target injection positioning failure (±10 μm accuracy not achieved) → laser beams miss target → no fusion → full laser energy deposited in chamber with no yield → catastrophic optics damage + chamber contamination → plant shutdown.
3. **F4 (Plasma-Wall Interaction) - Hardware**: First wall structural failure (pulsed fatigue or neutron embrittlement) → chamber loses vacuum integrity or Li coolant leaks → plant shutdown for chamber replacement. Alternatively, Li vapor or debris contamination of laser beam ports → beam propagation fails → shot failure → operational binary failure until ports cleaned.
4. **F6 (Fuel Cycle Closure) - Physics**: TBR < 1.0 → cannot breed sufficient tritium → external tritium purchase required → fuel cost ↑ 100× (~$30k/g tritium) → economically infeasible.
5. **F6 (Fuel Cycle Closure) - Hardware**: Tritium extraction failure (<90% recovery) → bred tritium lost to waste → TBR_effective < 1.0 → must purchase makeup tritium externally → economically infeasible.

Note: F2 and F4 hardware binary risks are conditional — if protective/replacement schemes exist (final optics annual replacement, first wall 3–5 year replacement per Inertia claim), they become degrading (O&M cost penalty) rather than binary. However, since Inertia has not disclosed final optics approach and first wall replacement is unverified, these remain classified as binary pending demonstration of viable mitigation.

---

### Function-Level Means and Heritage Credit

| Function | F1 | F2 | F3 | F4 | F5 | F6 | F7 |
|----------|-----|-----|-----|-----|-----|-----|-----|
| **Mean (physics + hardware)** | 3.5 | 3.5 | 4.0 | 1.5 | 3.5 | 3.5 | 4.5 |

**Heritage credit application (D-T fuel only):**

Inertia is a **Laser IFE (indirect drive)** concept with **D-T fuel** → heritage lineage: **Laser IFE (NIF, LIFE, etc.)** → floor **3.5** applies to F1, F2, F3 (per scoring framework).

**Heritage credit floors:**
- F1 (Plasma Performance): Mean = 3.5 → floor 3.5 → **F1 = 3.5** (no change)
- F2 (Driver/Energy Input): Mean = 3.5 → floor 3.5 → **F2 = 3.5** (no change)
- F3 (Instability Control): Mean = 4.0 → floor 3.5 → **F3 = 4.0** (mean exceeds floor; no change)

**Final function-level means (after heritage):**
- F1: 3.5
- F2: 3.5
- F3: 4.0
- F4: 1.5
- F5: 3.5
- F6: 3.5
- F7: 4.5

---

### LCOE Downselect Scoring YAML Block

```yaml
---
scores:
  C1: 4.6
  C3: 4.2
  C4: 2.5
  C5: 1.7
  C8: 2.2
  F1: 3.5
  F2: 3.5
  F3: 4.0
  F4: 1.5
  F5: 3.5
  F6: 3.5
  F7: 4.5
  binary_risks:
    - "F2-Hardware: Final optics failure with no replacement scheme → plant cannot operate (laser beams cannot reach target)"
    - "F3-Hardware: Target injection positioning failure (>±10 μm error) → laser beams miss target → no fusion → catastrophic optics damage + chamber contamination"
    - "F4-Hardware: First wall structural failure (pulsed fatigue or neutron embrittlement) → vacuum/coolant breach → plant shutdown; or beam port contamination → shot failure"
    - "F6-Physics: TBR < 1.0 → insufficient tritium breeding → external purchase required → economically infeasible"
    - "F6-Hardware: Tritium extraction failure (<90% recovery) → TBR_effective < 1.0 → external tritium purchase → economically infeasible"
---
```
