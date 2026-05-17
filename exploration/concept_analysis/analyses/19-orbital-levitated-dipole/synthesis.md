---
ID: 19-orbital-levitated-dipole
Concept: Orbital Levitated Dipole (D-He3)
Company: Zephyr Fusion
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Editorial Synthesis: Orbital Levitated Dipole (D-He3) — Zephyr Fusion

## 1. Executive Summary

- **Most important risk**: He3 fuel cost at market-purchase pricing ($30M/kg) drives LCOE to $8,863/MWh—59× terrestrial fusion parity—overwhelming all other factors. Self-breeding from D-D side reactions is categorically insufficient by 13× at equimolar D:He3 composition.
- **Most important advantage**: Eliminates CAS21–23 accounts entirely (no blanket, no shielding, no vacuum vessel)—$200–500M capital cost reduction at terrestrial scale—but this is replaced by three genuinely novel cost drivers with no LCOE precedent: launch cost, orbital spacecraft hardware, and ground rectenna infrastructure.
- **LCOE ballpark**: Baseline pessimistic (market He3, Falcon 9 launch, phased-array beaming): $8,863/MWh delivered. Optimistic-A (self-bred He3, Starship era, no-steering beaming): $491/MWh—within SPS parity ($200–500/MWh) but 3–8× terrestrial fusion parity. Native output 1.35 MWe scales to $631/MWh at 1000 MWe reference (α=0.6).
- **Confidence verdict**: Low. The concept rests on three sequential binary bets (He3 self-breeding × beaming efficiency >40% × spacecraft CAPEX <2× baseline), any one of which blocks economic viability. No element of the power chain beyond plasma confinement has been demonstrated at fusion-relevant scale. LCOE model is first-of-kind orbital-fusion-to-grid framework with no validation precedent.

---

## 2. What Matters Most for LCOE

### Rank 1: He3 fuel cost — Dominant lever, two-order-of-magnitude swing

**Assumed value**: $30M/kg (market allocation price), OR $0/kg (self-bred via D-D → T → He3 decay)
**Source**: CRS R41419 (2011) DOE He3 supply analysis; current allocation market $5–6k/std L ≈ $28–34M/kg

**Sensitivity magnitude**: At baseline 30 MW fusion (1.35 MWe delivered), He3 consumption is 1.62 kg/yr. Market purchase at $30M/kg adds $48.5M/yr to annual costs—51% of total LCOE ($8,863/MWh). Reducing He3 cost to $0 (self-bred) drops LCOE to $3,251/MWh—a 63% reduction—and shifts the economic constraint entirely to beaming efficiency and spacecraft hardware cost.

**What would flip the conclusion**: He3 self-breeding *at sufficiency* (breeding rate ≥ consumption rate) would eliminate the fuel cost barrier. Analysis §2 hypothesis (b) establishes that equimolar D:He3 self-breeding achieves only 7.5% of consumption—13× below sufficiency—based on Maxwellian-averaged cross-section arithmetic (⟨σv⟩_DD / ⟨σv⟩_DHe3 ≈ 1/6.7 at 100 keV). Closing the gap requires a D-rich fuel mix (D:He3 ≈ 13:1) that produces significant 2.45 MeV neutrons (D-D → He3+n branch), negating the aneutronic advantage and requiring shielding infrastructure the concept explicitly avoids. The binary outcome: market purchase (LCOE-blocking) or D-rich breeding mode (fundamentally different concept).

---

### Rank 2: End-to-end beaming efficiency — Revenue-side threshold

**Assumed value**: 4.5% net (baseline 4-stage chain: 70% DEC × 15% transmitter × 89% beam × 82% rectenna)
**Source**: Proton deceleration 50–65% (Venetian blind DEC, 1970s), transmitter <20% with phased-array steering (NSS SPS workshop, Shinohara 2005), beam 89% (GEO SPS reference geometry), rectenna >80% (world record 90%)

**Sensitivity magnitude**: Elasticity ≈ -1.0 (LCOE scales inversely with beaming efficiency). At 5% transmitter efficiency (phased-array worst case), LCOE rises to $26,432/MWh; at 75% (non-steering tube efficiency, aspirational), LCOE drops to $1,830/MWh. The beaming sub-chain (stages 2–4) contributes 10.9% efficiency before recirculating power losses.

**What would flip the conclusion**: SPS parity ($200–500/MWh) requires full-chain efficiency >40%. This demands either (a) 80% DEC + 50% transmitter + 90% beam/rectenna (no combination demonstrated), or (b) eliminating phased-array steering entirely and accepting fixed ground target (loses LEO orbital flexibility). The phased-array transmitter is the dominant bottleneck: 4–6 dB phase shifter losses per element drop DC-RF conversion from 70–80% (high-efficiency tubes) to <20%. No MW-scale space power beaming system has operated continuously; historical demonstrations (26.5% MSFC 1970, 54% Raytheon 1975) covered beaming-only sub-chain without the fusion DEC stage.

---

### Rank 3: Spacecraft hardware CAPEX multiplier — FOAK uncertainty corridor

**Assumed value**: $69M (baseline hardware accounts: HTS coil $15M, heating $15M, DEC $11M, transmitter $20M, bus/electronics/cryo/fuel $8M)
**Source**: Model costing file, line-item estimates from 1costingfe scaling laws + spacecraft analogy + FOAK premia

**Sensitivity magnitude**: Optimistic-A scenario (self-bred He3 $0, Starship $200/kg launch, eta_tx 50%) holds SPS parity ($491/MWh) at 1.0× baseline. Doubling hardware cost to 2.0× ($138M) pushes LCOE to $781/MWh—above SPS ceiling. At 10× ($690M spacecraft hardware), LCOE reaches $3,106/MWh. Hardware CAPEX multiplier sweep (Finding F-1) establishes breakeven between 1.0× and 2.0× baseline.

**What would flip the conclusion**: Analysis §7 flags that FOAK orbital fusion spacecraft cost "could be 10–100× higher per analysis" than the $69M baseline. If spacecraft fabrication exceeds 2× ($138M), the optimistic scenario crosses above SPS parity even with zero He3 cost and Starship-era launch. This is independent of the fuel and beaming bets—spacecraft CAPEX uncertainty is a third binary risk. NOAK serial production could reduce this, but the concept requires He3 self-breeding *and* beaming >40% *and* spacecraft <2× FOAK baseline simultaneously.

---

### Rank 4: Launch cost — Scenario-dependent; low impact in pessimistic, moderate in optimistic

**Assumed value**: $2,700/kg (Falcon 9 rideshare) OR $200/kg (Starship target)
**Source**: Public SpaceX pricing; Starship target from industry projections

**Sensitivity magnitude**: In the pessimistic scenario (market He3), reducing launch cost from $2,700/kg to $100/kg changes LCOE by only $466/MWh (5%)—He3 fuel cost dominates. In the optimistic scenario (self-bred He3 $0), launch cost becomes a meaningful lever: Falcon 9 ($2,700/kg) contributes $27M to $260M total capital; Starship ($200/kg) reduces this to $2M, lowering LCOE from ~$550/MWh to $491/MWh. Elasticity ≈ +0.05 in pessimistic, ≈ +0.15 in optimistic.

**What would flip the conclusion**: Launch cost alone cannot flip the economic outcome. Even at $0/kg launch (free orbital deployment), the pessimistic scenario (market He3) still yields $8,397/MWh. Launch cost matters only in the optimistic corridor where He3 is self-bred and beaming efficiency is high.

---

### Rank 5: Scientific Q — Recirculating power fraction driver

**Assumed value**: Q = 10 (optimistic for D-He3; D-T analogue OpenStar targets Q=15)
**Source**: Model baseline; D-He3 requires ~10× higher triple product than D-T (analysis §2 Challenge 4)

**Sensitivity magnitude**: At Q=5, recirculating power rises to 6 MW (36% of DEC output), dropping net delivered power from 1.35 MWe to 0.88 MWe—LCOE rises to $13,524/MWh (+53%). At Q=20, recirculating fraction drops to 22%, LCOE falls to $7,565/MWh (-15%). Elasticity ≈ -0.3 (LCOE moderately sensitive to Q).

**What would flip the conclusion**: Q<5 makes net power delivery marginal—at Q=2, recirculating power exceeds DEC output and net power goes to zero. Q alone does not determine economic viability (He3 cost and beaming efficiency dominate), but Q<10 compounds the revenue-side losses.

---

## 3. Risk Verdicts

### Challenge 1: Energy conversion pathway undefined

**Verdict**: Genuinely uncertain (technology exists in principle; efficiency unknown at fusion scale)

**Rationale**: The 4-stage chain (DEC → transmitter → beam → rectenna) has been demonstrated at subscale for each individual stage, but the *combined* efficiency at MW-class fusion output is uncharacterized. Venetian blind DEC achieved 50–65% for non-fusion ions (TRL 3–4 for 14.7 MeV protons); phased-array transmitters exist but phase-shifter losses are fundamental; MW-scale space power beaming is undemonstrated. The full chain could achieve 40–50% (SPS-competitive) or remain at 5–10% (LCOE-blocking); no operating system resolves this.

**What would retire this risk**: A demonstration of MW-class continuous power beaming from LEO to ground rectenna—even without fusion (i.e., solar or fission power source + beaming transmitter + ground receiver)—would validate the beaming sub-chain efficiency. For the DEC stage, a 14.7 MeV proton deceleration experiment at kW-scale would bound the efficiency range for reactor extrapolation.

---

### Challenge 2: He3 fuel supply — Market purchase vs. self-breeding

**Verdict**: Unlikely resolvable at equimolar D:He3 composition; resolvable only via D-rich breeding mode that negates aneutronic premise

**Rationale**: Cross-section arithmetic (Bosch & Hale 1992) establishes that D-D/D-He3 rate ratio at 100 keV is ~7.5%, yielding 7.5% self-breeding at equimolar fuel mix—13× below sufficiency (analysis §2 hypothesis b). This is not an engineering uncertainty; it is nuclear data. Self-breeding sufficiency requires D:He3 ≈ 13:1, at which point D-D reactions dominate fusion output and produce significant 2.45 MeV neutrons. The "aneutronic" advantage disappears, and the concept becomes a D-D reactor with trace He3.

**What would retire this risk**: (a) Demonstration of He3 production at multi-kg/year scale via alternative pathways (lunar mining, large-scale tritium → He3 decay infrastructure, or reactor breeding), reducing market price from $30M/kg to <$1M/kg—makes market purchase economically tolerable. OR (b) Acceptance that the concept must operate in D-rich breeding mode, with commensurate shielding infrastructure and loss of aneutronic cost/regulatory advantages.

---

### Challenge 3: Confinement scaling (τₑ ~ R²) unvalidated at fusion-relevant temperatures

**Verdict**: Genuinely uncertain (favorable scaling observed at LDX/RT-1 laboratory conditions; extrapolation to 50–100 keV unvalidated)

**Rationale**: LDX and RT-1 demonstrated τₑ ~ R² scaling at electron temperatures ~few hundred eV. Dipole geometry suppresses MHD instabilities and supports high-beta steady-state operation—this is well-established physics. However, D-He3 requires ion temperatures 50–100 keV (5–10× higher than D-T requirement), and no dipole experiment has approached these conditions. If edge turbulence or other transport mechanisms scale less favorably (τₑ ~ R or R^1.5), net fusion power becomes unachievable at commercially viable device mass.

**What would retire this risk**: A burning-plasma dipole experiment at intermediate scale (~10 MW thermal, D-T fuel) validating τₑ scaling in the fusion-relevant temperature regime. The OpenStar arxiv 2602.20564 study explicitly calls for such a demonstration to validate reactor-scale confinement models. Alternative: high-fidelity gyrokinetic simulations benchmarked against LDX/RT-1 and extended to reactor parameters—less definitive but could narrow uncertainty.

---

### Challenge 4: Orbital operations cost structure — No precedent in fusion LCOE literature

**Verdict**: Genuinely uncertain (satellite lifetime/maintenance analogies exist; fusion-specific orbital O&M is truly novel)

**Rationale**: The model uses 3% of overnight capital as annual O&M (analysis §7 LCOE skeleton), but this is a placeholder. Orbital fusion adds debris mitigation (plasma extends 10–50 m radius—large cross-section), Van Allen radiation damage to HTS coil, on-orbit replacement logistics (no crewed EVA analogue at this scale), and fuel resupply via launch. Space Solar Power (SPS) analogy provides partial guidance (rectenna O&M, ground station operations), but the fusion plasma + HTS coil + direct converter stack is unique.

**What would retire this risk**: A detailed orbital operations study for a fusion spacecraft—covering lifetime radiation damage to REBCO tape under Van Allen proton/electron flux, cryocooler replacement cadence, fuel resupply logistics, and anomaly recovery—would bound the O&M cost corridor. Alternatively, long-duration HTS magnet operation in LEO (non-fusion test article) would validate coil lifetime assumptions.

---

### Challenge 5: Spacecraft CAPEX — FOAK manufacturing cost unknown

**Verdict**: Likely resolvable (orbital spacecraft manufacturing is established industry; fusion-specific premia are the uncertainty)

**Rationale**: The model baseline ($69M spacecraft hardware) aggregates HTS coil ($15M), heating ($15M), DEC ($11M), transmitter ($20M), and bus/cryo/electronics ($8M). Each component has terrestrial analogy (HTS coils for fusion exist; phased-array transmitters for radar exist; satellite buses are commodity). The fusion-specific FOAK premium—space qualification of the HTS coil under fusion plasma loads, integration of the DEC with the transmitter, thermal management at MW-class—is genuinely unknown and "could be 10–100× higher" (analysis §7). The hardware multiplier sweep establishes that 2× baseline ($138M) is the SPS-parity ceiling in the optimistic scenario.

**What would retire this risk**: A preliminary design review (PDR) for an orbital fusion spacecraft—even at conceptual level—would provide bottom-up cost estimates for each subsystem. NOAK learning curves from terrestrial fusion (SPARC, Commonwealth Fusion HTS magnet costs) and satellite manufacturing (Starlink bus production costs) could inform the FOAK → NOAK transition.

---

## 4. Structural Advantages and Disadvantages

**Reference baseline**: Conventional D-T spherical tokamak (21-spherical-tokamak-hts analogue—Tokamak Energy) with steam Rankine cycle, breeding blanket, and terrestrial siting.

### Advantages (quantified where possible)

1. **Eliminates CAS21–23 accounts entirely** (blanket, shielding, vacuum vessel)
   At terrestrial scale, these accounts total $200–500M for a GW-class tokamak (analysis cross-concept notes). The orbital concept radiates D-D neutrons into space and uses LEO vacuum inherently—no vacuum vessel, no tritium breeding blanket, no W/WC/B₄C shielding infrastructure. This removes the dominant TRL-risk category for D-T concepts (tritium breeding TBR<1.0 is a binary failure mode).

2. **No tritium handling or regulatory burden**
   D-He3 eliminates: Li-6 enrichment supply chain, FLiBe/Li-metal coolant handling, tritium extraction/purification, NRC Part 50 licensing for tritium inventory, and dual-use export controls on tritium. CAS10 pre-construction costs drop from $100M+ (D-T tokamak) to ~$18M (model baseline—orbital nuclear licensing + spectrum permits).

3. **Steady-state operation with no disruption risk**
   Levitated dipole geometry is intrinsically disruption-free (no current-driven instabilities). Capacity factor ceiling is higher than pulsed concepts: baseline 90% vs. 70–80% for pulsed IFE. However, orbital debris events and radiation damage introduce unplanned downtime not present in terrestrial concepts.

4. **Compact magnet geometry reduces REBCO tape demand**
   A meter-scale HTS dipole coil requires ~500–2,000 km REBCO tape (estimated from OpenStar D-T terrestrial dipole 4,320 km at 208 MWe, scaled down to MW-class). This is 5–10× less than a spherical tokamak pilot plant at equivalent fusion power, partially offsetting the space-qualification premium.

### Disadvantages (quantified where possible)

1. **Launch cost replaces construction cost as CAPEX driver**
   At Falcon 9 pricing ($2,700/kg), a 10,000 kg spacecraft costs $27M launch alone—comparable to CAS21 (buildings) for a small terrestrial plant. Starship ($200/kg) reduces this to $2M, but then spacecraft hardware ($69M baseline) dominates. Terrestrial fusion scales capital cost with fusion power via economy-of-scale (α=0.6); orbital fusion scales capital with *spacecraft mass*, which scales poorly with fusion power at MW-class (specific power 135 W/kg baseline—far below the 1 kW/kg Hasegawa 1987 target).

2. **Power beaming adds 80–95% conversion loss**
   The 4-stage efficiency chain (4.5% baseline; 17.8% optimistic-A) is structurally worse than any terrestrial thermal cycle (32–48% steam/sCO₂). Every MW of fusion power delivers only 0.045–0.18 MWe to the customer. A terrestrial D-T tokamak at 35% thermal efficiency delivers 7.8× more revenue per unit fusion power than the orbital baseline, and 2× more than the optimistic case.

3. **Ground rectenna infrastructure is a new CAS account**
   At ~$2M/MWe (SPS GW-class analogue), a 1.35 MWe plant requires $2.7M rectenna + grid tie (model CAS24). This is small in absolute terms but scales *per delivered MWe*—not per fusion MWe—making it 5–10× more expensive per delivered power than a terrestrial grid connection ($0.08–0.2M/MWe). At GW-delivered scale, rectenna cost becomes a major capital driver.

4. **He3 fuel cost at market purchase is 10–100× D-T fuel cost**
   D-T fuel (with breeding) costs ~$10–50/kg tritium (steady-state inventory replacement). He3 at $30M/kg is 600,000× more expensive per kg. Even though D-He3 fusion releases more energy per reaction (18.3 MeV vs. 17.6 MeV), the fuel cost per MWh is ~1,000× higher than D-T at current He3 allocation pricing. This is the dominant LCOE penalty in the pessimistic scenario.

5. **Orbital O&M has no servicing pathway**
   A terrestrial tokamak can replace the blanket, repair coils, and upgrade power electronics. An orbital spacecraft has two options: (a) design for zero maintenance over 10–20 year lifetime (high FOAK cost), or (b) plan for on-orbit replacement via robotic servicing or de-orbit + relaunch (high NOAK cost). The model assumes option (a); coil replacement cycle is set to 10 years (= plant lifetime), meaning the first HTS coil failure ends the mission.

### Net structural impact

The concept's cost structure is better than a terrestrial D-T tokamak *only if* three conditions hold simultaneously: (1) He3 is self-bred at sufficiency (eliminating fuel cost), (2) beaming efficiency >40% (approaching thermal-cycle parity), and (3) spacecraft CAPEX <2× baseline (preserving SPS parity). If any one fails, the structural disadvantages (beaming loss, launch cost, no servicing) dominate. The blanket/shielding/vacuum-vessel elimination provides a capital cost advantage at terrestrial scale ($200–500M) but is offset by spacecraft hardware + launch + rectenna in the orbital context.

---

## 5. Cross-Concept Positioning

### Location in the fusion landscape

The Orbital Levitated Dipole sits at the intersection of **three concept families**, each with distinct economic reference points:

1. **MFE aneutronic concepts** (D-He3 fuel)
   Peers: Helion FRC (08-frc-w-direct-conversion), TAE FRC (18-p-b11-frc), Realta Fusion mirror (11-magnetic-mirror, p-B11). All share the He3 or p-B11 fuel supply challenge and direct energy conversion pathway. Helion explicitly pursues He3 self-breeding via D-D → T → He3 decay; Zephyr has not disclosed a breeding strategy. The orbital concept is *unique* in combining aneutronic fuel with space deployment—no other aneutronic concept uses this approach.

2. **Levitated dipole confinement**
   Peers: OpenStar levitated dipole (12-levitated-dipole, D-T terrestrial), PoloMac (35-polomac, D-D terrestrial with internal coil). OpenStar provides the closest physics analogy (same confinement geometry, same τₑ ~ R² scaling, same steady-state operation) but uses D-T fuel + blanket + thermal cycle. PoloMac uses an internal non-levitated coil. Zephyr is the only orbital dipole concept in the current fusion industry.

3. **Orbital/space power concepts** (competitive reference)
   The economic peer group is **Space Solar Power (SPS)**, not terrestrial fusion. SPS LCOE benchmarks at $200–500/MWh (NASA/DOE 2012 study) for GEO photovoltaic + microwave beaming to ground. Zephyr's optimistic-A scenario ($491/MWh) sits at the upper edge of SPS parity. The competitive question is: can fusion offer higher specific power (W/kg) than photovoltaics to justify the TRL gap? Baseline 135 W/kg (Zephyr model) is 3–5× lower than modern PV arrays (~400–700 W/kg for deployable space arrays), and far below the 1 kW/kg Hasegawa 1987 target.

### What makes this concept fundamentally different

**Launch cost as the dominant CAPEX driver** — Every other fusion concept scales capital cost with fusion power (larger reactor → higher cost, but economy-of-scale α=0.6 reduces $/kWe). Orbital fusion scales capital cost with *spacecraft mass*. This inverts the usual LCOE optimization: maximizing fusion power per unit mass (W/kg) becomes the primary design goal, not minimizing capital cost per unit power ($/kWe). The concept must achieve >1 kW/kg to compete with SPS on specific-power grounds, and >10 kW/kg to approach terrestrial fusion on $/kWe grounds—neither demonstrated.

**Revenue-side loss chain dominates LCOE** — Terrestrial fusion optimizes capital cost (CAS 20–50 accounts) because thermal efficiency is fixed by Carnot limits (~35–50%). Orbital fusion must optimize *beaming efficiency* (stages 2–4) because this 10–fold variation (5% baseline to 50% aspirational) swamps capital cost sensitivity. The phased-array transmitter is the single highest-impact component—more important than plasma Q, more important than launch cost—because phase-shifter losses (4–6 dB/element) are fundamental to LEO tracking and no technology bypasses them.

**Three-way failure mode** — Most fusion concepts have a single dominant risk (e.g., tokamaks: TBR<1.0; IFE: target fabrication cost; mirrors: end-loss power density). Orbital D-He3 has three *independent* binary risks: (1) He3 self-breeding sufficiency, (2) beaming efficiency >40%, (3) spacecraft CAPEX <2× baseline. The probability of simultaneous success is the product of three uncertain terms—each <<1—making the overall risk-adjusted LCOE expectation value very high.

---

## 6. Modeling Confidence

**Rating**: Low

### Data-anchored parameters (7 of 22 LCOE-critical parameters)

- Falcon 9 launch cost ($2,700/kg): publicly known, medium confidence
- He3 market price ($30M/kg): well-documented in CRS R41419, medium confidence
- D-He3 charged particle fraction (80%): nuclear data, high confidence
- ICRH wall-plug efficiency (70%): OpenStar baseline, medium confidence
- Rectenna efficiency (82%): SPS demonstration, medium confidence
- Beam collection efficiency (89%): SPS reference geometry, medium confidence
- Plant availability (90%): satellite analogy, low confidence (no fusion precedent)

### Speculative parameters (15 of 22)

- **Q = 10**: Optimistic for D-He3. OpenStar D-T dipole targets Q=15; D-He3 requires ~10× higher triple product. Q=5 is more conservative. (HIGH UNCERTAINTY)
- **DEC efficiency 70%**: Venetian blind 50–65% for non-fusion ions; 14.7 MeV proton deceleration physics differs qualitatively (proton range 1.4 mm exceeds original electrode gaps). Actual efficiency truly unknown. (HIGH UNCERTAINTY)
- **Transmitter efficiency 15%**: Phased-array with 4–6 dB phase-shifter loss per element. No MW-scale demonstration. Non-steering tubes achieve 70–80% but lose LEO tracking flexibility. (HIGH UNCERTAINTY)
- **Spacecraft hardware costs ($69M)**: Line-item estimates from 1costingfe scaling + spacecraft analogy. FOAK fusion spacecraft has no precedent; analysis flags "10–100× higher" uncertainty. (HIGH UNCERTAINTY)
- **He3 self-breeding at $0/kg**: Cross-section arithmetic establishes equimolar breeding is 13× insufficient. Assumes a future D-rich breeding mode that negates aneutronic premise. (HIGH UNCERTAINTY)
- **Fusion power 30 MW**: Back-calculated to yield ~1 MWe delivered. Zephyr states "megawatt-class"—could be 5–100 MW. (HIGH UNCERTAINTY)
- **Orbital O&M 3% of overnight capital**: Placeholder from analysis LCOE skeleton. No orbital fusion precedent. (HIGH UNCERTAINTY)

### Dominant source of LCOE uncertainty

**He3 fuel supply pathway** is the dominant uncertainty because it spans two orders of magnitude ($0 to $30M/kg) and contributes 0–51% of LCOE depending on the scenario. This is not a precision uncertainty (e.g., ±20% around a central value); it is a *scenario branch* where the two outcomes lead to qualitatively different concepts. Market purchase makes the concept non-viable under any other parameter assumption; self-breeding makes it SPS-competitive *if* beaming efficiency and spacecraft CAPEX are favorable. No intermediate state exists.

### Model validation constraints

The LCOE model is a **first-of-kind orbital-fusion-to-grid framework** with no validation precedent. The CAS 10-60 accounts are adapted from 1costingfe but heavily overridden (CAS21–26 accounts do not apply as terrestrial-fusion-defined). The closest validation analogy is Space Solar Power LCOE studies (NASA/DOE 2012, JAXA SPS), but these use photovoltaic + beaming, not fusion + DEC + beaming. The model's structural choices—treating launch cost as CAS50, rectenna as CAS24, spacecraft hardware as CAS22—are defensible but unverified.

---

## 7. What Would Change My Mind

### In the optimistic direction (toward commercial viability):

1. **Demonstration of 50%+ end-to-end beaming efficiency at MW-scale**
   A continuous 1–10 MW power beaming test from LEO to ground rectenna—even with solar or fission power source (no fusion required)—validating transmitter + beam + rectenna at 50%+ combined efficiency would retire the dominant revenue-side uncertainty. This would establish that SPS parity ($200–500/MWh) is achievable with self-bred He3 and Starship-era launch, shifting the economic question from "can this ever work?" to "how fast can spacecraft CAPEX be reduced via NOAK learning?"

2. **He3 production at <$1M/kg from non-market source**
   Either (a) lunar He3 mining demonstration at multi-kg/year scale, or (b) large-scale terrestrial He3 production via dedicated tritium → He3 decay infrastructure, achieving <$1M/kg long-run marginal cost. This would make market-purchase He3 economically tolerable ($1M/kg → $1.62M/yr fuel cost → LCOE drops from $8,863 to ~$3,400/MWh). Not competitive with terrestrial fusion but removes the LCOE-blocking fuel barrier.

3. **10 kW/kg specific power demonstration in a subscale orbital dipole test**
   A small-scale orbital fusion experiment (1–10 kW output, 1–10 kg coil) achieving >10 kW/kg specific power would validate that the physics-limited scaling is far more favorable than the baseline model (135 W/kg). This would shift the $/kWe capital cost from $192,562/kWe (baseline) toward terrestrial fusion parity ($5,000–15,000/kWe), making the concept competitive even without breakthrough beaming efficiency.

### In the pessimistic direction (away from commercial viability):

1. **Phased-array transmitter efficiency confirmed <10% at MW-scale**
   A detailed engineering study or prototype test establishing that phase-shifter losses at MW-class drive DC-RF conversion below 10%—worse than the 15% baseline—would push the optimistic-A scenario above $700/MWh and eliminate SPS parity even with self-bred He3 and Starship launch. This would confine the concept to niche non-terrestrial markets (lunar base power, deep-space propulsion) where LCOE is not the primary figure of merit.

2. **FOAK spacecraft CAPEX confirmed >5× baseline ($345M)**
   A preliminary design review for an orbital fusion spacecraft—including space-qualified HTS coil, DEC, phased-array transmitter, and cryocooler—establishing that first-unit cost exceeds $345M (5× the $69M baseline) would push optimistic-A LCOE to $1,653/MWh, eliminating SPS parity. This would make the concept economically non-viable under any fuel or beaming assumption until NOAK learning drives costs down by 5–10×.

3. **D-He3 confinement scaling in dipole geometry confirmed weaker than τₑ ~ R²**
   High-fidelity gyrokinetic simulations or intermediate-scale burning-plasma dipole experiments establishing that D-He3 transport scales as τₑ ~ R^1.5 or τₑ ~ R (rather than R²) would require impractically large orbital devices to achieve net power. If the R² scaling does not hold at fusion-relevant temperatures, the orbital advantage (no vacuum vessel energy loss) is overwhelmed by poor confinement, and the concept becomes non-viable at any achievable spacecraft mass.

---

## 8. LCOE Downselect Scoring

I score C1, C3, C4, C5, and C8. I fill the complete C7 risk matrix (7 functions × 2 subcategories). C2, C6, and C7 are computed by Python.

---

### C1: Modularization — 3.2

**Sub-factor breakdown**:

| CAS Account | Construction Mode | Mode Score | Cost Weight | Weighted |
|-------------|------------------|------------|-------------|----------|
| CAS21 (Ground station) | Site-assembled from factory sub-assemblies | 3 | 0.02 | 0.06 |
| CAS22 (Spacecraft hardware) | Factory-manufactured modules (spacecraft bus, HTS coil, heating, DEC, transmitter all fab'd off-site) | 5 | 0.96 | 4.80 |
| CAS23 (Beaming management) | Factory-manufactured | 5 | 0.02 | 0.10 |
| CAS24 (Rectenna + grid) | Site-assembled from factory sub-assemblies | 3 | 0.03 | 0.09 |
| CAS25 (Misc ground) | Site-assembled | 3 | 0.01 | 0.03 |
| CAS26 (Thermal ground) | Factory-manufactured | 5 | 0.01 | 0.05 |
| **Cost-weighted average** | | | | **5.13** |

**Module repetition boost**: 0 (single spacecraft per plant; no identical module repetition within spacecraft)

**C1 = min(5.13 + 0, 5.0) = 5.0** (clamped)

**However**, the scoring framework defines repetition boost as applying when "10–49 identical modules per plant" exist. The orbital concept has a single spacecraft with unique subsystems—no module is repeated 10+ times. The high factory-fab mode score (5.0) reflects that the spacecraft is entirely built off-site, but there is no repetition *within* the plant. The cost-weighted average exceeds 5.0 due to CAS22 dominance (96% of direct cost), but C1 is clamped at 5.0 per framework.

Re-computing without the repetition assumption (which does not apply): **C1 = 5.0** (cost-weighted mode score alone, clamped). The spacecraft is a single factory-manufactured unit; ground infrastructure is minor (<5% cost).

**Correction**: The framework states "clamped to [1, 5]" after applying repetition boost. Without repetition, the cost-weighted average is 5.13, which clamps to **C1 = 5.0**.

**But** let me reconsider the CAS22 classification. The spacecraft is factory-manufactured as a *single unit*—it is not modular in the sense of repeated identical subassemblies. However, the framework's "factory-manufactured module" definition (score 5) applies to components that are "standardized, repeatable" in a broader industry context. The HTS coil, heating system, DEC, and transmitter are each *custom* first-of-kind (FOAK) designs for this application—not standardized industrial modules. A more conservative classification:

| CAS Account | Construction Mode | Mode Score |
|-------------|------------------|------------|
| CAS22 | Site-assembled from factory sub-assemblies (spacecraft is integrated from FOAK subsystems, not off-the-shelf modules) | 3 |

Revising: cost-weighted average = 3.0 × 0.96 + (other accounts) ≈ 3.0. No repetition boost. **C1 = 3.0**.

**Final C1 = 3.0**: The spacecraft hardware (CAS22, 96% of cost) is site-assembled (launch site integration) from factory-fabricated FOAK subsystems. No module repetition within the plant.

**Justification**: The orbital concept eliminates field-erected construction (no stick-built blanket, no on-site shield assembly), but the spacecraft is a FOAK integrated system, not a standardized module. Ground infrastructure (<5% cost) is conventional site assembly. The high factory-fab fraction is offset by lack of module repetition.

---

### C3: Supply Chain Learning — 2.3

**Sub-factor A: Component learning rates (cost-weighted)** = 2.7

| CAS Account | Learning Rate Category | Category Score | Cost Weight | Weighted |
|-------------|----------------------|----------------|-------------|----------|
| CAS22 (Spacecraft hardware) | Fusion-specific HTS coil (2), FOAK DEC (1), FOAK transmitter (1), heating (2), bus (4), electronics (4) — weighted avg ~2.0 | 2 | 0.96 | 1.92 |
| CAS24 (Rectenna) | Specialty component with limited supply chain (SPS analogy, not at fusion scale) | 3 | 0.03 | 0.09 |
| CAS27 (He3 startup inventory) | Novel material never manufactured at scale (He3 at kg/yr) | 1 | 0.01 | 0.01 |
| Other accounts | Industrial components (ground station, grid tie) | 4 | 0.00 | 0.00 |
| **Cost-weighted average** | | | | **2.02** |

Rounding to nearest 0.5: **A = 2.0**

**Sub-factor B: Supply chain bottleneck count** = 2.5

Starting at 5.0, subtract penalties:
- **He3 fuel supply** (no path to kg/yr scale at market price): -1.5 (He3 dependency per framework)
- **Space-qualified HTS coil** (scaling constraint—REBCO tape supply exists but space-qual is limited): -0.5
- **MW-class phased-array transmitter** (no known supplier; FOAK development): -0.5
- **14.7 MeV DEC hardware** (no commercial supply; never manufactured at scale): -0.5

**B = 5.0 - 1.5 - 0.5 - 0.5 - 0.5 = 2.0**

**Sub-factor C: External demand pull** = 2.0

Fraction of capital cost in components with >$1B/yr external market:
- **REBCO tape**: External market ~$500M/yr (fusion + MRI + other), but Zephyr's small coil is <1% of this. Not a demand pull for this concept.
- **Spacecraft bus, power electronics**: External market >$10B/yr (satellite industry). Applies to ~$10M of $260M total capital (4%).
- **Rectenna, grid tie**: External market (utility grid equipment) >$100B/yr. Applies to ~$3M of capital (1%).
- **He3, HTS coil, DEC, transmitter**: No external market at fusion scale.

Total: ~5% of capital cost has >$1B/yr external market. Per framework: <10% → **C = 1.0**.

Correction: The spacecraft bus + electronics ($9M) + rectenna/grid ($3M) = $12M / $261M ≈ 5%. This is <10%, so **C = 1.0**. However, let me reconsider whether the HTS coil benefits from external demand. REBCO tape has a >$1B/yr projected market (fusion industry alone: SPARC, Commonwealth Fusion, Tokamak Energy, multiple tokamak projects), and Zephyr's coil uses the same tape. The coil *fabrication* is custom, but the tape *material* has external demand pull.

Revising: REBCO tape cost ~$5M (of $15M coil cost); spacecraft bus/electronics $9M; rectenna/grid $3M. Total: $17M / $261M ≈ 6.5%. Still <10% → **C = 1.0** per framework threshold.

But the framework asks "what fraction of capital cost is in components with >$1B/yr external market?"—not materials. The *components* are spacecraft bus (external market exists) and grid tie (external market exists). REBCO tape is a material input, not a component. The DEC, transmitter, and HTS coil are FOAK components with no external market. Sticking with **C = 1.0**.

**C3 = (A + B + C) / 3 = (2.0 + 2.0 + 1.0) / 3 = 1.7**

**Justification**: He3 fuel dependency is the dominant bottleneck (-1.5); FOAK spacecraft hardware (DEC, transmitter, space-qualified HTS) has minimal supply chain maturity (learning rate 1–2); external demand pull is limited to satellite bus + grid equipment (~5% of capital). The concept depends on a supply chain that does not yet exist.

---

### C4: Plant Complexity — 2.5

**Sub-factor A: Operational coupling density** = 2.0

The orbital concept has **moderate operational coupling** (score 3 → but see below for adjustment).

**Failure cascade paths identified**:
1. **HTS coil quench → loss of confinement → plasma termination → zero output**: Single-point failure. No redundancy in coil design (single levitated coil). Quench protection must dump energy safely, but coil failure ends the mission.
2. **Cryocooler failure → coil warming → quench → mission loss**: Cryocooler is a critical path component. Redundancy possible (multiple cryocoolers) but not specified.
3. **DEC failure → no DC power → no beaming → zero revenue**: DEC is a single-point bottleneck in the power chain. No bypass pathway.
4. **Phased-array transmitter failure → no beaming → zero revenue**: Partial degradation possible (lose some array elements → reduced beam coherence) but full failure is mission-loss.
5. **Heating system (ICRH) failure → plasma cooling → loss of Q → zero net power**: Heating is critical path to sustain D-He3 conditions.

**Decoupled systems**:
- Ground rectenna failure does not affect spacecraft (spacecraft can beam to alternate ground station if available)
- Fuel system failure (He3 injection) is single-point but has possible manual override / backup tanks

The spacecraft has **5 major single-point failures** (HTS coil, cryocooler, DEC, transmitter, heating). This is higher coupling than a terrestrial plant with redundant cooling loops, spare breeder modules, and on-site maintenance. However, it is lower coupling than a pulsed IFE concept where target factory → injector → laser → chamber is a serial failure chain with no bypass.

**Comparison**: A terrestrial tokamak has ~8–10 critical interdependencies (vacuum vessel integrity, blanket cooling, tritium loop, magnet cooling, heating, fueling, divertor, power conversion, grid tie). The orbital concept has fewer *total* subsystems but higher criticality per subsystem (no redundancy, no servicing).

Scoring: **A = 2.0** (highly coupled; several failure cascade paths; single-point failures dominate; no on-orbit servicing to recover).

**Sub-factor B: Subsystem count** = 3.0

CAS22 sub-accounts representing >1% of total capital ($261M × 0.01 = $2.6M threshold):

1. C220103 HTS coil: $15M (5.7%)
2. C220104 Heating: $15M (5.7%)
3. C220105 Bus: $5M (1.9%)
4. C220107 Electronics: $4M (1.5%)
5. C220109 DEC: $10.9M (4.2%)
6. C220111 Integration labor: $10.1M (3.9%)
7. C220113 Transmitter: $20M (7.7%)
8. C220300 Cryocooler/radiator: $3.7M (1.4%)
9. C220600 Ground control: $5M (1.9%)
10. C220700 I&C: $3.3M (1.3%)
11. CAS24 Rectenna: $2.8M (1.1%)
12. CAS27 He3 inventory: $48.5M (18.6%)

**Total: 12 significant subsystems** → per framework: 11–14 subsystems = score 2.

But let me re-read the framework: "Count CAS22 sub-accounts that represent >1% of total capital." CAS27 (He3 inventory) is not a CAS22 sub-account—it's CAS20-level. Excluding CAS27 and accounts outside CAS22:

CAS22 sub-accounts >1%:
1. C220103 HTS coil: $15M
2. C220104 Heating: $15M
3. C220105 Bus: $5M
4. C220107 Electronics: $4M
5. C220109 DEC: $10.9M
6. C220111 Integration labor: $10.1M
7. C220113 Transmitter: $20M

That's 7 CAS22 sub-accounts. But the framework asks for "CAS22 sub-accounts that represent >1% of total capital"—not just CAS22 cost. Total capital is $261M; 1% = $2.61M. All 7 above exceed this.

Add plant-wide CAS22 sub-accounts:
8. C220300 Cryocooler: $3.7M
9. C220600 Ground control: $5M
10. C220700 I&C: $3.3M

**Total: 10 CAS22 sub-accounts >1% of total capital** → per framework: 8–10 subsystems = score 3.

**B = 3.0**

**C4 = (A + B) / 2 = (2.0 + 3.0) / 2 = 2.5**

**Justification**: The orbital spacecraft has 5 major single-point failures (HTS coil, cryocooler, DEC, transmitter, heating) with no on-orbit servicing capability—higher operational criticality than a terrestrial plant with redundancy and maintenance access. Subsystem count is moderate (10 significant CAS22 accounts), but operational coupling is high due to serial power chain (fusion → DEC → transmitter → beam → rectenna) with no bypass pathways.

---

### C5: Customization Needs — 3.5

**Sub-factor A: Thermal rejection** = 4.0

The concept uses **direct energy conversion (DEC) for charged particles + passive radiation to space for neutrons**. The DEC stage produces DC electricity (no thermal cycle for the charged particle fraction, 80% of fusion energy). The D-D neutron fraction (10% of fusion energy, 3 MW at baseline) radiates into space—no cooling infrastructure. The spacecraft does require thermal management for the cryocooler heat rejection (maintaining HTS coil at ~20 K), but this is accomplished via passive radiator panels—no active cooling towers or water intake.

Per framework: "4 = No thermal cycle or air-cooled (e.g., direct energy conversion only)". The concept is not *pure* DEC (some bremsstrahlung heat is radiated and not recovered), but it has no steam cycle, no cooling towers, no heat exchanger to ground. The cryocooler radiator is air-cooled-equivalent (passive radiation to space).

**A = 4.0**

**Sub-factor B: Fuel safety profile** = 3.0

D-He3 fuel: low neutron fraction (~10% from D-D side reactions, 2.45 MeV), no tritium breeding required.

Per framework: "3 = D-He3 (low neutron fraction, no tritium)".

**B = 3.0**

**Raw C5 = (A + B) / 2 = (4.0 + 3.0) / 2 = 3.5**

**Scaled to [1, 5] range: C5 = 1 + (3.5 - 1) × (4/3) = 1 + 2.5 × 1.333 = 1 + 3.33 = 4.33**

Wait, let me re-read the framework formula: "C5 = (A + B) / 2, then scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)".

So: raw = 3.5. scaled = 1 + (3.5 - 1) × (4/3) = 1 + 2.5 × 1.333 = 1 + 3.33 = **4.33**.

Rounding to nearest 0.5: **C5 = 4.5**

But the framework says "scale to [1, 5] range"—does this mean the scaled value can exceed 5? Let me check: A ranges [1, 4], B ranges [1, 4], so raw C5 ranges [1, 4]. Scaling: 1 + (4 - 1) × (4/3) = 1 + 4 = 5.0. So the formula maps [1, 4] → [1, 5]. At raw = 3.5, scaled = 4.33.

**C5 = 4.5** (rounded to nearest 0.5)

**Justification**: D-He3 fuel eliminates tritium handling and requires no thermal rejection infrastructure (DEC + passive radiators). The D-D neutron fraction (10%) is radiated into space. Site-specific thermal rejection advantages (water access, cooling towers) do not apply—the concept is intrinsically site-independent (can beam to any ground station with line-of-sight). Minor customization needed for rectenna ground station (land area ~1 ha per MWe at LEO geometry).

---

### C8: Data Adequacy — 1.5

**Sub-factor A: Source diversity & independence** = 1.0

Available public-domain sources:
- **Academic heritage**: LDX/RT-1 experiments (MIT, U. Tokyo), Hasegawa 1987 (PPPL), OpenStar arxiv 2602.20564 (2026 preprint, D-T terrestrial dipole)
- **Company sources**: YC launch page only (1 page, ~500 words technical content)
- **Independent validation**: NASASpaceFlight forum discussion (community critique)

The academic heritage is *not specific to Zephyr's concept*—it covers dipole confinement in general (LDX/RT-1) or D-T terrestrial application (OpenStar). The only Zephyr-specific source is the YC launch page, which discloses almost nothing (no plasma parameters, no heating method, no conversion pathway). There are no independent peer-reviewed studies of the orbital D-He3 dipole concept.

Per framework: "1 = No public-domain architecture literature available" — this is too harsh (LDX/OpenStar heritage exists). "2 = Almost exclusively company publications" — this fits better, but Zephyr has only 1 company publication (YC page).

**A = 1.0**: No independent public-domain literature specific to the orbital D-He3 concept; all specific claims are company-only (YC page).

**Sub-factor B: Reactor design specification** = 1.0

The YC launch page provides: confinement concept (levitated dipole), scale (meter-scale HTS coil, >ITER magnetized volume), deployment (Falcon 9), and power class (MW-class). It does *not* provide: plasma parameters (n, T, τ), heating method, energy conversion pathway, Q target, fuel cycle, or any subsystem specifications.

Per framework: "1 = No reactor design beyond basic concept description".

**B = 1.0**

**Sub-factor C: LCOE parameter coverage** = 1.0

Blocking gaps from gap_report.md (F-2 summary):
1. Energy conversion pathway undefined (no DEC or beaming spec)
2. He3 fuel supply strategy (purchase vs. self-breed)
3. Plasma design point (T, n, Q, heating power)
4. Capital cost structure (no analogue for orbital fusion plant)
5. Plant capacity factor (orbital operations undefined)
6. Heating method and efficiency
7. Target net electrical output (specific MWe)

**Total: 7 blocking gaps identified**.

Per framework: "2 = 5–7 blocking gaps".

**C = 2.0**

**Sub-factor D: Commercialization pathway clarity** = 2.0

Zephyr's YC launch page states: "targeting our first orbital fusion demonstration in ~10 years" (implied timeline). Funding: YC F25 seed (Pioneer Fund backing). Team: 2 founders (Galen Burke, Edward Hinson). No milestones, no intermediate demonstration program, no cost-to-first-power estimate, no scale-up pathway described.

Per framework: "2 = Vague or aspirational commercialization narrative".

**D = 2.0**

**C8 = (A + B + C + D) / 4 = (1.0 + 1.0 + 2.0 + 2.0) / 4 = 1.5**

**Justification**: Zephyr has disclosed almost nothing beyond the existence of their concept. The YC launch page (March 2025) is the sole company publication. Academic heritage (LDX, OpenStar) provides physics foundation but not Zephyr-specific design parameters. Seven LCOE-blocking gaps remain unresolved; commercialization pathway is aspirational ("~10 years" with no intermediate milestones). Data adequacy is among the lowest in the concept landscape.

---

### C7: Technical Risk Evidence — Risk Matrix

I fill the complete 7-function × 2-subcategory risk matrix. For each cell, I provide: plant requirement, best demonstrated, gap ratio, closure mechanism, classification (Binary/Degrading), and evidence tier (1–5).

#### Function 1: Plasma Performance

**F1.1 — Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | D-He3 triple product ≥ 10²⁰ keV·s·m⁻³ (estimated from D-T requirement 10¹⁹ keV·s·m⁻³ × reactivity ratio ~10×) at ion temperature 50–100 keV |
| Best demonstrated | LDX: electron temperature ~few hundred eV, density ~10¹⁷ m⁻³, confinement time ~1 ms → triple product ~10¹⁴ keV·s·m⁻³ (D plasma, not fusion-relevant). RT-1: similar parameters. |
| Gap ratio | 10⁶× (requirement / demonstrated) |
| Closure mechanism | Extrapolation via τₑ ~ R² scaling law from LDX/RT-1 (laboratory scale, few hundred eV) to reactor scale (meter-scale separatrix, 50–100 keV). OpenStar arxiv 2602.20564 explicitly states "no such model exists for dipoles" for confinement scaling. Intermediate-scale burning-plasma dipole experiment required to validate. |
| Classification | Binary (if confinement scaling is weaker than R², net fusion power unachievable at commercially viable spacecraft mass) |
| Evidence tier | 2 (simulation + scaling law extrapolation; no demonstrated regime) |

**F1.2 — Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | HTS levitated dipole coil operating at >10 T field in LEO radiation environment (Van Allen belts) for 10+ years without quench or degradation |
| Best demonstrated | LDX: superconducting coil levitated and operated in terrestrial lab (not space-qualified). REBCO tape tested in simulated space radiation (ground-based). No HTS coil operated in LEO under fusion plasma loads. |
| Gap ratio | N/A (never demonstrated in combined environment) |
| Closure mechanism | Space qualification of HTS coil via (1) radiation damage testing under Van Allen proton/electron flux, (2) thermal cycling + vacuum testing, (3) quench protection for free-floating coil. Cryocooler + passive radiator system for sustained ~20 K operation. No on-orbit servicing—coil must survive full mission lifetime. |
| Classification | Binary (coil quench or radiation-induced degradation → loss of confinement → zero output; no repair pathway) |
| Evidence tier | 2 (HTS coils exist for terrestrial fusion; space qualification is design study + simulation, not operated) |

**Function-level F1 mean = (2 + 2) / 2 = 2.0**

---

#### Function 2: Driver / Energy Input

**F2.1 — Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | ICRH or ECRH coupling efficiency ≥70% to sustain D-He3 plasma at 50–100 keV ion temperature in dipole geometry; heating power ~3 MW at Q=10 |
| Best demonstrated | ICRH demonstrated on RT-1 (dipole, sub-keV regime) with "mixed results" per OpenStar study. ECRH demonstrated on LDX (dipole, sub-keV). Both at heating power <1 MW, electron heating only (not ion heating to fusion-relevant temperatures). |
| Gap ratio | ~100× on temperature (few hundred eV → 50–100 keV); ~3× on power (1 MW → 3 MW) |
| Closure mechanism | RF wave propagation and absorption modeling for D-He3 plasma in dipole geometry at fusion-relevant density/temperature. ICRH ion heating validated at intermediate scale. OpenStar identifies ICRH as baseline (70% wall-plug) for D-T dipole; D-He3 requires higher temperature but same heating physics. |
| Classification | Degrading (inefficient heating → higher Q required → larger spacecraft → worse $/kWe; does not block net power if Q is achieved) |
| Evidence tier | 3 (subscale ICRH demonstrated on RT-1 at <50% of temperature requirement, same geometry, different fuel) |

**F2.2 — Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | ICRH antenna + power supply delivering 3 MW RF power in LEO environment (vacuum, thermal management, radiation hardening) with 70% DC-RF conversion efficiency |
| Best demonstrated | ITER ICRH system (terrestrial): 20 MW capacity, 70% efficiency at component level. No ICRH system operated in space environment. RF systems in LEO face thermal management challenges (no convective cooling). |
| Gap ratio | 7× scale-down (20 MW ITER → 3 MW Zephyr) is favorable, but space qualification is undemonstrated |
| Closure mechanism | Adapt terrestrial ICRH technology (gyrotrons, antennas) for space environment. Thermal rejection via passive radiators. Radiation hardening of power electronics. Space-grade RF components exist (satellite communications) but not at MW-class fusion power. |
| Classification | Degrading (heating hardware failure → loss of plasma sustainment → zero output, but backup heating methods exist in principle—ECRH, NBI) |
| Evidence tier | 3 (terrestrial ICRH at full power demonstrated; space environment is adjacent—different thermal/vacuum but same RF physics) |

**Function-level F2 mean = (3 + 3) / 2 = 3.0**

---

#### Function 3: Instability Control

**F3.1 — Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Stable plasma confinement at high beta (β > 0.2) in dipole geometry under D-He3 fusion conditions (50–100 keV, density ~10²⁰ m⁻³) with no disruptive instabilities |
| Best demonstrated | LDX: high-beta (β ~ 0.25) stable plasma demonstrated at sub-keV electron temperature. RT-1: similar. Dipole geometry is intrinsically MHD-stable (no current-driven kink/tearing modes). Interchange instability suppressed by compressibility in dipole field. |
| Gap ratio | ~100× on temperature extrapolation (few hundred eV → 50–100 keV), but stability physics is favorable—dipole stability improves with beta |
| Closure mechanism | Dipole confinement is intrinsically disruption-free per LDX/RT-1 validation. Edge turbulence (not MHD) may limit confinement, but this affects τₑ scaling (Function 1), not catastrophic instability. D-He3 high-Z impurity radiation could be a loss channel but does not destabilize the plasma. |
| Classification | Degrading (if edge turbulence dominates, confinement time is reduced, but plasma remains stable—this is a performance degradation, not a binary failure) |
| Evidence tier | 4 (LDX/RT-1 demonstrated high-beta stability at subscale in same geometry; extrapolation to fusion temperature is favorable—higher temperature stabilizes via pressure profile) |

**F3.2 — Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Coil positioning and levitation control to maintain dipole geometry under plasma pressure and thermal loads in LEO microgravity environment |
| Best demonstrated | LDX: levitated coil maintained via magnetic levitation in terrestrial lab (1g environment). LEO microgravity simplifies levitation (no gravity load) but introduces orbital perturbations (drag, solar wind, magnetic field gradients). |
| Gap ratio | Microgravity levitation is easier than 1g, but long-term position control (10+ years) in LEO is undemonstrated for fusion coil |
| Closure mechanism | Active position control via trim coils or thrusters. Passive magnetic levitation + feedback control (heritage from LDX). Orbital debris avoidance (plasma extends 10–50 m—large cross-section for debris interaction). |
| Classification | Degrading (position control failure → loss of confinement geometry → reduced fusion output, but plasma does not quench—this is a gradual performance loss) |
| Evidence tier | 4 (LDX demonstrated levitation at subscale; LEO microgravity is adjacent environment—easier on some axes, harder on others—debris, radiation, long duration) |

**Function-level F3 mean = (4 + 4) / 2 = 4.0**

---

#### Function 4: Plasma-Wall Interaction

**F4.1 — Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Plasma-wall heat flux managed at dipole separatrix (10–50 m radius) with impurity influx below tolerable limit for D-He3 burn; wall loading ~0.01–0.1 MW/m² (very low compared to tokamak divertor ~10 MW/m²) |
| Best demonstrated | LDX/RT-1: plasma-wall interaction observed at sub-keV conditions with no material damage issues (sub-eV particle energy at wall). D-He3 in dipole radiates bremsstrahlung but wall loading is intrinsically low due to large surface area (4πR² ~ thousands of m² at R=20 m). |
| Gap ratio | ~100× temperature extrapolation, but favorable geometry—wall loading scales as P_fusion / (4πR²), which is ~1000× lower than tokamak divertor per unit fusion power |
| Closure mechanism | Large separatrix radius distributes heat load over vast area. Impurity influx managed via gas puffing (He3, D). No divertor required—particles drift to separatrix and escape. Bremsstrahlung radiation (high-Z impurities) is a performance loss (Function 1) but not a wall damage issue. |
| Classification | Degrading (excessive impurity influx reduces fusion power via radiation loss, but does not damage structure—this degrades performance, not a binary failure) |
| Evidence tier | 4 (LDX/RT-1 validated low wall flux in dipole geometry at subscale; extrapolation to fusion power is favorable—heat load per unit area decreases with scale) |

**F4.2 — Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Materials for plasma-facing surfaces (if any) at separatrix must survive 10+ years exposure to D-He3 plasma, 2.45 MeV neutrons (low flux), and LEO radiation environment (Van Allen belts, solar wind) |
| Best demonstrated | Tungsten plasma-facing components: WEST, JET, ITER divertor mock-ups at >10 MW/m² heat flux (tokamak regime). Orbital concept has ~0.01–0.1 MW/m² heat flux—far lower. However, no plasma-facing material tested in combined LEO radiation + fusion plasma environment. |
| Gap ratio | Heat flux requirement is 100× lower than demonstrated ITER/WEST regime, but combined environment (LEO + fusion) is undemonstrated |
| Closure mechanism | Use standard tokamak PFC materials (tungsten, carbon composites) at far lower heat flux than demonstrated capability. Dominant concern is LEO radiation damage (proton/electron belts) to structural materials over 10+ years, not plasma erosion. No first wall / blanket (orbital concept), so no neutron displacement damage to structure. |
| Classification | Degrading (PFC degradation increases impurity influx → reduces performance, but structure remains intact—no catastrophic failure mode) |
| Evidence tier | 4 (tungsten PFCs demonstrated at 100× higher heat flux than this concept requires; LEO environment is adjacent—different radiation spectrum but lower thermal load) |

**Function-level F4 mean = (4 + 4) / 2 = 4.0**

---

#### Function 5: Neutron/Particle Handling

**F5.1 — Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | 2.45 MeV neutrons from D-D side reactions (~10% of fusion energy, 3 MW at baseline) radiated into space without shielding; no activation of spacecraft structure |
| Best demonstrated | D-D neutrons well-characterized; 2.45 MeV cross-sections and transport physics are standard nuclear data. Spacecraft structure (aluminum, titanium, composite) has low activation under 2.45 MeV neutron flux (no long-lived isotopes produced). |
| Gap ratio | 1× (physics is well-understood; no gap) |
| Closure mechanism | No closure needed—D-D neutron radiation into space is inherent to orbital operation. 2.45 MeV neutrons do not require shielding (unlike 14 MeV D-T neutrons). Spacecraft structure experiences ~10¹⁵–10¹⁶ n/cm² over 10 years (low fluence—no displacement damage or transmutation concerns). |
| Classification | Degrading (long-term low-flux neutron exposure could induce minor activation of structure, but this is regulatory/decommissioning issue, not operational failure) |
| Evidence tier | 5 (D-D neutron production is well-understood; spacecraft materials under 2.45 MeV flux are characterized; no extrapolation required) |

**F5.2 — Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Neutron-induced activation of spacecraft materials (aluminum, titanium, REBCO tape superconductor) remains below regulatory limits for space debris disposal |
| Best demonstrated | REBCO tape under neutron irradiation: tested at fission reactor neutron flux (HFIR, ORNL) for tokamak magnet programs. Aluminum + titanium spacecraft structure: well-characterized activation cross-sections. No long-lived isotopes produced at 10¹⁵ n/cm² fluence (2.45 MeV neutrons). |
| Gap ratio | 1× (activation cross-sections known; fluence is low; no gap) |
| Closure mechanism | Neutron fluence calculation + activation analysis per standard methods (MCNP, FISPACT). Spacecraft disposal via controlled de-orbit after mission end (burn-up in atmosphere). Regulatory precedent: nuclear-powered satellites (RTGs) have orbital disposal protocols. |
| Classification | Degrading (activation affects end-of-life disposal cost, not operational function) |
| Evidence tier | 5 (activation of aluminum/titanium under 2.45 MeV neutrons is well-characterized; REBCO under neutron flux is demonstrated at higher fluence than this concept experiences) |

**Function-level F5 mean = (5 + 5) / 2 = 5.0**

---

#### Function 6: Fuel Cycle Closure

**F6.1 — Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | He3 breeding from D-D side reactions at rate ≥ consumption (1.62 kg/yr at baseline 30 MW fusion) to enable self-sufficient fuel cycle |
| Best demonstrated | D-D fusion produces He3 via two branches: (1) D+D → He3+n (direct, 50% of D-D reactions), (2) D+D → T+p followed by T → He3 + β⁻ (tritium decay, t₁/₂=12.3 yr, other 50% of D-D). However, at equimolar D:He3 fuel mix (optimal for D-He3 fusion), D-D reaction rate is only 7.5% of D-He3 rate (cross-section arithmetic, Bosch & Hale 1992). Self-breeding rate is 7.5% of consumption—13× below sufficiency. |
| Gap ratio | 13× (sufficiency requires D:He3 ~ 13:1, which negates aneutronic advantage and produces significant 2.45 MeV neutrons) |
| Closure mechanism | Company has not disclosed breeding strategy. Self-breeding at equimolar composition is categorically insufficient per nuclear data. Pathways: (1) Market purchase He3 at $30M/kg (LCOE-blocking), (2) D-rich fuel mix (D:He3 ~ 13:1) to achieve breeding sufficiency, which transforms the concept into a D-D reactor with trace He3 and requires shielding, (3) External He3 supply (lunar mining, terrestrial production scale-up). |
| Classification | Binary (without He3 self-breeding, market-purchase fuel cost ($48.5M/yr at baseline) drives LCOE to $8,863/MWh—59× terrestrial fusion parity; concept is non-viable without resolution of He3 supply) |
| Evidence tier | 1 (breeding sufficiency at equimolar D:He3 is asserted by analogy to Helion but contradicted by cross-section arithmetic; no He3 breeding demonstrated in dipole geometry at any scale) |

**F6.2 — Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | He3 + D fuel injection, on-orbit storage, and recycling system delivering fuel to plasma for 10+ years; fuel resupply via periodic launch if self-breeding is insufficient |
| Best demonstrated | He3 handling: terrestrial lab-scale (few kg total inventory in US DOE stockpile, grams in experimental systems). D fueling: well-established for terrestrial fusion (tokamaks, stellarators). On-orbit cryogenic storage: demonstrated for satellite propellant (N2O, hydrazine) but not for He3 at kg-scale. |
| Gap ratio | 1000× scale-up (grams in lab → kg/yr throughput), plus on-orbit operation undemonstrated |
| Closure mechanism | Pressurized tanks for He3 + D storage (gaseous or cryogenic). Fuel injection via gas puffing or pellet injection (tokamak heritage). Unburned fuel recovery via pumping + reprocessing (terrestrial heritage). Launch resupply: periodic Falcon 9 / Starship missions with He3 cargo (assumes market supply or terrestrial production scale-up). |
| Classification | Binary (if He3 fuel cannot be delivered to orbit at kg/yr scale—either via self-breeding or launch resupply—the concept cannot operate; no substitute fuel exists for D-He3 fusion) |
| Evidence tier | 2 (terrestrial He3 handling is lab-scale; on-orbit storage + injection is design study; no combined system demonstrated) |

**Function-level F6 mean = (1 + 2) / 2 = 1.5**

---

#### Function 7: Power Conversion & BOP

**F7.1 — Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Direct energy conversion of 14.7 MeV protons from D-He3 fusion at ≥70% efficiency (DEC stage); 3.6 MeV alpha particles also contribute to charged particle power |
| Best demonstrated | Venetian blind DEC: 50–65% efficiency demonstrated for non-fusion ions in 1970s experiments (Post & Moir, LLNL). However, 14.7 MeV proton range in condensed matter is ~1.4 mm—exceeds original DEC electrode gaps and requires qualitatively different hardware design. Efficiency for 14.7 MeV protons is truly unknown. |
| Gap ratio | N/A (efficiency at 14.7 MeV is uncharacterized; original DEC used lower-energy ions <100 keV) |
| Closure mechanism | Electrostatic deceleration of 14.7 MeV protons via multi-stage DEC with large electrode gaps (mm-scale) or alternative media (liquid metal, plasma). Proton stopping power is well-understood physics (Bethe-Bloch formula), but conversion efficiency at this energy in practical hardware is undemonstrated. ARIES-III D-He3 tokamak study claimed 60–70% DEC efficiency (design estimate, not built). |
| Classification | Degrading (DEC efficiency <70% reduces revenue-side power output, but fusion energy is still captured—efficiency could range 20–70%, not binary failure) |
| Evidence tier | 2 (DEC concept demonstrated at subscale for lower-energy ions; 14.7 MeV proton deceleration is simulation + scaling, not operated) |

**F7.2 — Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Phased-array microwave transmitter converting DC power to RF at ≥15% efficiency (baseline) or ≥50% (optimistic, non-steering tubes); beam collection ≥89%; rectenna RF-DC ≥82%; all stages operating continuously at MW-scale in LEO → ground path |
| Best demonstrated | Individual stages: (1) High-efficiency microwave tubes: 70–80% DC-RF without steering (terrestrial); phased-array with steering: <20% due to 4–6 dB phase-shifter losses per element (Shinohara 2005, NSS SPS workshop). (2) Beam collection: 89% demonstrated in SPS reference geometry (GEO 36,000 km; LEO 500 km is shorter—comparable or better). (3) Rectenna: >80% RF-DC world record 90% (terrestrial). Historical combined DC-DC beaming demos: 26.5% (1970 MSFC), 54% (1975 Raytheon, 495 W magnetron)—neither included fusion DEC stage. |
| Gap ratio | MW-scale space power beaming is undemonstrated (historical demos <1 kW); phased-array steering at MW-class is undemonstrated; full 4-stage chain (DEC + beaming) never operated |
| Closure mechanism | Scale up terrestrial microwave beaming technology (magnetrons, klystrons, phased arrays) to MW-class for space. Thermal management via passive radiators. Ground rectenna at ~1 ha per MWe (LEO geometry, shorter range than GEO). Phase-shifter loss is fundamental (ferrite or semiconductor phase shifters introduce 4–6 dB attenuation)—no bypass exists while maintaining LEO tracking. Alternative: fixed ground target (no phased-array) achieves 70–80% transmitter efficiency but loses orbital flexibility. |
| Classification | Degrading (beaming efficiency <40% makes LCOE non-competitive with SPS/terrestrial fusion, but net power is still delivered—efficiency range 5–50%, not binary failure) |
| Evidence tier | 2 (individual beaming sub-components demonstrated at subscale; MW-class combined system is design study + component testing, not operated; phased-array phase-shifter losses are fundamental physics, not engineering uncertainty) |

**Function-level F7 mean = (2 + 2) / 2 = 2.0**

---

### Heritage credit: DOES NOT APPLY (D-He3 fuel)

The framework states: "Heritage credit only applies to D-T fuel." This concept uses D-He3, so no heritage floor is applied to F1–F7.

---

### Binary risks identified

From the risk matrix above, risks classified as **Binary**:

1. **F1.1 Physics**: If τₑ scaling is weaker than R², net fusion power is unachievable at commercially viable spacecraft mass (confinement physics extrapolation failure)
2. **F1.2 Hardware**: HTS coil quench or radiation-induced degradation in LEO → loss of confinement → zero output (no on-orbit servicing)
3. **F6.1 Physics**: He3 self-breeding at equimolar composition is 13× insufficient; market-purchase fuel cost ($30M/kg) drives LCOE to $8,863/MWh—59× terrestrial parity (fuel supply failure)
4. **F6.2 Hardware**: If He3 cannot be delivered to orbit at kg/yr scale (via self-breeding or launch resupply), concept cannot operate (fuel delivery failure)

---

### Function-level means (after heritage, if applicable)

Heritage credit does not apply (D-He3 fuel). Function-level means are computed directly from the 2-subcategory symmetric averages:

- F1 = 2.0
- F2 = 3.0
- F3 = 4.0
- F4 = 4.0
- F5 = 5.0
- F6 = 1.5
- F7 = 2.0

---

## YAML Scores Block

```yaml
---
scores:
  C1: 3.0
  C3: 1.7
  C4: 2.5
  C5: 4.5
  C8: 1.5
  F1: 2.0
  F2: 3.0
  F3: 4.0
  F4: 4.0
  F5: 5.0
  F6: 1.5
  F7: 2.0
  binary_risks:
    - "F1.1: Confinement scaling weaker than R² → net fusion power unachievable at viable spacecraft mass"
    - "F1.2: HTS coil quench or radiation degradation in LEO → loss of confinement, no on-orbit repair"
    - "F6.1: He3 self-breeding at equimolar D:He3 is 13× insufficient per cross-section arithmetic; market purchase at $30M/kg drives LCOE to $8,863/MWh (59× terrestrial parity)"
    - "F6.2: He3 delivery failure (via self-breeding or launch resupply) → concept cannot operate, no substitute fuel exists"
---
```
