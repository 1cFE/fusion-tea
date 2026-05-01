---
ID: 19-orbital-levitated-dipole
Concept: Orbital Levitated Dipole (D-He3)
Company: Zephyr Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
---

# Synthesis: Orbital Levitated Dipole (D-He3)

## 1. Executive Summary

- **The single most important risk**: Helium-3 fuel cost at market price ($30M/kg) is LCOE-blocking—fuel alone delivers $6,000/MWh—unless self-breeding via D-D side reactions works. But self-breeding at equimolar D:He3 composition is insufficient by 13× based on reactivity arithmetic, requiring extreme D-rich fuel that destroys the aneutronic advantage. This is a binary economic fate: external He3 procurement (unviable) or a fundamentally different D-rich concept.

- **The single most important advantage**: Orbital deployment eliminates the vacuum vessel, blanket, tritium breeding infrastructure, and thermal cycle—removing CAS21-26 capital costs and tritium regulatory burden. In principle, this creates a radically simplified plant structure with no neutron wall loading, no first-wall replacement cycle, and steady-state operation with no day/night variation. The concept is structurally non-comparable to any terrestrial fusion reactor.

- **LCOE ballpark**: Baseline pessimistic (market He3 $30M/kg, Falcon 9 launch, phased-array beaming): **$11,800/MWh** (118× terrestrial fusion parity). Optimistic scenario (self-bred He3 ~$0, Starship launch $200/kg, improved beaming 50% transmitter efficiency): **$491/MWh** (within space solar power parity $200-500/MWh, but 3-8× terrestrial fusion parity). The optimistic case requires simultaneous success on three technology bets: (a) He3 self-breeding in a D-rich fuel mode, (b) non-phased-array beaming at 50% DC-RF efficiency, and (c) FOAK spacecraft hardware cost not exceeding ~2× baseline ($69M × 2 = $138M loses SPS parity).

- **Confidence verdict**: **Low**. Zephyr Fusion is a 2-person YC F25 startup (founded 2025) with no technical papers, no reactor design, and no disclosed plasma parameters, heating method, or energy conversion pathway. Every LCOE-critical parameter is either inferred from 1987-era academic heritage (Hasegawa PPPL-2627) or borrowed from a 2026 D-T terrestrial dipole study (OpenStar arxiv 2602.20564) that addresses a fundamentally different concept. The 4-stage efficiency chain (proton deceleration → DC-RF transmitter → beam → rectenna) compounds high uncertainty at each stage, yielding ~3% net efficiency in the baseline case. The model is a first-pass corridor map, not a defensible cost estimate.

---

## 2. What Matters Most for LCOE

### **Rank 1: He3 Fuel Cost**

- **Assumed value**: $30M/kg (market allocation price, 2011-2026 basis from CRS R41419)
  **Sensitivity magnitude**: At 30 MW fusion power, annual He3 consumption is 1.6 kg/yr → $48.5M/yr fuel cost. For a 1 MWe delivered plant, this alone contributes **$6,080/MWh** (51.5% of total LCOE in baseline). Sweeping He3 cost from $0 (self-bred) to $30M/kg changes LCOE from $4,293/MWh to $11,800/MWh—a 2.75× multiplier. This is the largest single-parameter LCOE lever in the entire model.
  **What would flip the economic conclusion**: Self-bred He3 at near-zero variable cost. But analysis Section 2 hypothesis (b) shows equimolar D:He3 self-breeding achieves only 7.5% of consumption via D-D side reactions (⟨σv⟩_DD / ⟨σv⟩_DHe3 ≈ 1/6.7 at 100 keV). Sufficiency requires 13:1 D:He3 ratio, which produces 2.45 MeV DD neutrons at levels comparable to D-D reactors, negating the aneutronic premise. The self-breeding pathway exists but is a qualitatively different concept than the aneutronic orbital dipole Zephyr describes.

### **Rank 2: End-to-End Power Beaming Efficiency**

- **Assumed value**: 3.4% net (p_net/p_fus) in baseline, decomposed as:
  - Stage 1 (DEC proton deceleration): 57% (Venetian blind upper bound, 14.7 MeV protons undemonstrated)
  - Stage 2 (DC-RF transmitter with phased-array steering): 15% (<20% per Shinohara 2005 due to 4-6 dB phase shifter losses)
  - Stage 3 (beam collection free-space): 89% (GEO SPS analogue, LEO comparable)
  - Stage 4 (RF-DC rectenna): 82% (mature technology)
  **Sensitivity magnitude**: Sweeping transmitter efficiency from 5% (extreme phased-array loss) to 75% (aspirational non-steering tube) changes LCOE from $35,237/MWh to $2,418/MWh—a 14.6× range. At baseline He3 cost ($30M/kg), transmitter efficiency dominates revenue-side sensitivity. In the optimistic scenario (He3 ~$0), beaming efficiency is the primary LCOE driver.
  **What would flip the economic conclusion**: Achieving 50% transmitter efficiency (non-steering microwave tubes or laser beaming) plus 65% DEC efficiency would yield 17.8% net end-to-end, bringing LCOE to $491/MWh (SPS parity window). Current technology (phased-array required for LEO tracking) delivers ~15% transmitter, implying <10% net beaming-only efficiency. The 4-stage chain including DEC yields 3.4% net, which cannot reach SPS parity even with $0 fuel cost unless beaming technology fundamentally improves.

### **Rank 3: Spacecraft Hardware Capital Cost**

- **Assumed value**: $69M baseline fabrication cost (HTS coil $15M + heating $15M + DEC $10M + phased-array transmitter $20M + bus $5M + electronics $4M). Total capital including launch ($27M Falcon 9) and ground infrastructure ($2M rectenna): $258M for 1 MWe delivered → **$255,100/kWe** specific capital (vs. $5,000-15,000/kWe for terrestrial fusion).
  **Sensitivity magnitude**: In the optimistic scenario (He3 $0, Starship $200/kg launch, 50% transmitter efficiency), LCOE = $491/MWh. Doubling spacecraft hardware cost to $138M (2× baseline) raises LCOE to $781/MWh, crossing above SPS parity ($500/MWh ceiling). The multiplier sweep (model output lines 233-240) shows SPS parity is lost between 1.0× and 2.0× baseline hardware cost. Analysis Section 7 notes FOAK spacecraft fabrication could be 10-100× higher than baseline, but the breakeven is at ~1.4× — a narrow viable corridor.
  **What would flip the economic conclusion**: NOAK serial production driving spacecraft hardware below $69M, combined with Starship-era launch ($200/kg → $2M launch cost per unit), yields specific capital ~$60,000/kWe. Still 4-12× terrestrial fusion, but within SPS cost structure. To reach terrestrial fusion parity ($5,000-15,000/kWe), delivered power per spacecraft must increase by ~5-10× (requiring beaming efficiency breakthrough) or unit capital must fall to $20M total (unachievable without radical manufacturing cost reduction or much smaller power scale).

### **Rank 4: Scientific Q**

- **Assumed value**: Q=10 (fusion power / heating power). D-He3 requires ~50-100 keV ion temperature (5-10× D-T) and ~10× higher triple product than D-T due to lower reactivity. OpenStar D-T dipole targets Q=15; Q=10 for D-He3 is optimistic.
  **Sensitivity magnitude**: Sweeping Q from 2 to 30 changes LCOE from infinite (Q=2 yields negative net power due to recirculating loads exceeding DEC output) to $9,032/MWh (Q=30). At baseline He3 cost, Q sensitivity is moderate—Q=30 vs. Q=10 is only a 1.3× LCOE improvement because fuel cost dominates. In the optimistic scenario (He3 $0), Q becomes more important but is still secondary to beaming efficiency.
  **What would flip the economic conclusion**: Achieving Q=30 in a D-He3 dipole (unprecedented—requires confirming τₑ ~ R² scaling at fusion-relevant conditions and demonstrating 10²⁰ keV·s·m⁻³ triple product) would lower recirculating power from 32% to ~10% of DEC output, improving net efficiency from 3.4% to ~5%. Significant but not transformative given the beaming efficiency bottleneck. Q is a necessary but insufficient condition for competitiveness.

### **Rank 5: Launch Cost ($/kg to LEO)**

- **Assumed value**: $2,700/kg (Falcon 9 rideshare current pricing). Starship target: $100-200/kg (not yet operational).
  **Sensitivity magnitude**: Sweeping launch cost from $100/kg to $5,000/kg changes LCOE from $11,176/MWh to $12,351/MWh—only a 1.1× range. Launch cost is 12.7% of overnight capital in baseline ($27M / $238.6M total overnight), so even order-of-magnitude launch cost reduction has limited LCOE impact. This is counterintuitive but correct: at 10,000 kg spacecraft mass and 1 MWe delivered, reducing launch from $27M to $2M (Starship) saves only ~$3,100/kWe, which is small relative to the $255,100/kWe baseline specific capital.
  **What would flip the economic conclusion**: Launch cost matters primarily in the optimistic scenario where He3 fuel cost is eliminated ($0 self-breeding). In that case, Starship launch ($200/kg) vs. Falcon 9 ($2,700/kg) is a $491/MWh vs. $515/MWh difference—meaningful for staying below SPS parity but not transformative. The real value of Starship is enabling larger spacecraft (100,000 kg to LEO) that could deliver 10-100× more power per unit, fundamentally changing the specific capital equation—but that requires resolving the beaming efficiency and He3 fuel bottlenecks first.

---

## 3. Risk Verdicts

### **Challenge 1: No Energy Conversion Pathway Disclosed**
**Verdict**: Genuinely uncertain (company has not disclosed mechanism)
**Rationale**: Hasegawa 1987 describes separatrix direct conversion of 14.7 MeV protons, and ARIES-III D-He3 tokamak study achieved 47% net efficiency with hybrid rectenna + thermal conversion. The physics pathway exists in the heritage literature, but Zephyr has not confirmed they are using direct conversion, power beaming, or any specific technology. Without this disclosure, the efficiency chain is entirely assumed.
**What would retire this risk**: Company disclosure of (a) direct conversion technology (electrostatic decelerator, magnetic divertor, or alternative), (b) power beaming method (microwave frequency, laser, or other), and (c) target end-to-end efficiency with component-level breakdown. A single technical paper describing the energy conversion architecture would convert this from "genuinely uncertain" to "quantifiable engineering challenge."

### **Challenge 2: Helium-3 Supply — Market Purchase vs. Self-Breeding**
**Verdict**: Likely resolvable IF the concept shifts to D-rich fuel mode, but this negates the aneutronic advantage
**Rationale**: Global He3 production is ~1.8-2.7 kg/yr (US Savannah River + CANDU), and market price is $28-34M/kg. At 1.6 kg/yr consumption per MW-class spacecraft, external procurement is economically unviable (fuel alone is $48.5M/yr → $6,080/MWh). Self-breeding via D-D side reactions is the only path to commercial supply, but equimolar D:He3 composition yields only 7.5% breeding fraction (analysis Section 2 hypothesis b). To approach sufficiency, fuel must shift to 13:1 D:He3 ratio, producing significant 2.45 MeV DD neutrons and effectively becoming a D-D reactor with trace He3. This is physically plausible but destroys the aneutronic premise.
**What would retire this risk**: Demonstration of D-D → T → He3 breeding loop closure in a dipole geometry at >90% self-sufficiency. This requires (a) operating at 13:1 D:He3 fuel ratio, (b) confirming tritium extraction and 12.3-year decay management, (c) accepting DD neutron production at ~10% energy fraction (requiring shielding the concept explicitly avoids), and (d) demonstrating the D-rich fuel ignites and confines stably in a dipole. None of this has been shown. If successful, the concept becomes a "D-D breeder with He3 burnup"—economically viable but not the aneutronic orbital reactor described on the YC launch page.

### **Challenge 3: D-He3 Confinement Physics — Enormous Parameter Extrapolation**
**Verdict**: Unlikely resolvable without intermediate-scale experimental validation (decade+ timeline)
**Rationale**: D-He3 requires 50-100 keV ion temperature (5-10× D-T) and ~10× higher triple product (~10²⁰ keV·s·m⁻³) due to lower reactivity. LDX/RT-1 demonstrated dipole confinement at few-hundred-eV electron temperature—2-3 orders of magnitude below D-He3 conditions. The arxiv 2602.20564 OpenStar study explicitly states "no such model exists for dipoles" regarding energy confinement scaling and requires demonstrating 10¹⁹ keV·s·m⁻³ triple product in intermediate devices to validate reactor-relevant models for D-T. For D-He3, the target is 10× harder. The τₑ ~ R² scaling claim is unverified at fusion temperatures and may weaken to τₑ ~ R^1.5 or τₑ ~ R in edge-turbulence regimes (analysis Section 2 hypothesis a).
**What would retire this risk**: Construction and operation of a D-He3 dipole experimental device achieving (a) 50 keV ion temperature, (b) triple product >10¹⁹ keV·s·m⁻³, (c) confirmation of τₑ ~ R² scaling at these conditions, and (d) Q>1 net fusion gain. This is a $500M-1B scale experiment (comparable to LDX cost inflation-adjusted) with 10-15 year timeline. No such device is funded or planned. Zephyr is a 2-person startup with no ARPA-E or DOE backing as of March 2026. The risk is not retired by subscale modeling or simulation—D-He3 dipole reactor physics is TRL 1-2.

### **Challenge 4: No Heating Method Specified — Q and Recirculating Power Unanchored**
**Verdict**: Likely resolvable (ICRH is the most plausible baseline)
**Rationale**: ECRH (30-40% wall-plug efficiency) was used on LDX; ICRH (70% wall-plug efficiency) is the OpenStar D-T dipole baseline and studied on RT-1 with "mixed results." NBI is also applicable. At Q=10 and 30 MW fusion power, ICRH heating requires 4.29 MW wall-plug (model output line 34), which is 32% of DEC output—manageable but significant. If ECRH is required instead, wall-plug heating rises to ~7.5 MW (55% of DEC output), making net power delivery marginal. The uncertainty is which heating method couples efficiently to a D-He3 dipole plasma at 50-100 keV ion temperature.
**What would retire this risk**: Experimental demonstration of ICRH or ECRH coupling efficiency in a dipole geometry at ≥20 keV ion temperature. RT-1 has begun ICRH studies; extending this to fusion-relevant temperatures would validate the 70% wall-plug efficiency assumption. Alternatively, company disclosure of heating method and coupling model (even if unvalidated) would provide a defensible basis for the recirculating power estimate. This is a lower-tier technical risk compared to confinement physics and He3 supply.

### **Challenge 5: Orbital Operations Cost Structure — No Precedent in Fusion LCOE Literature**
**Verdict**: Genuinely uncertain (no operational orbital fusion analogue exists)
**Rationale**: Operating a fusion reactor in LEO introduces cost categories with no terrestrial fusion parallel: orbital debris mitigation (10-50 m plasma radius creates large interaction cross-section), Van Allen radiation damage to HTS coil (orbital altitude selection trades off debris risk vs. radiation environment), replacement/servicing logistics (no crewed EVA at this scale), and orbital lifetime management. The model uses 3% of overnight capital per year as O&M (analysis Section 7 skeleton basis), but this is extrapolated from satellite operations, not fusion plants. Space solar power (SPS) feasibility studies (NASA NTRS 20140003205) concluded GEO SPS is "not practical" vs. ground CSP even with reduced launch cost—ground infrastructure scale and cost was the binding constraint, not launch.
**What would retire this risk**: A 5-year orbital technology demonstration mission—deploy a sub-scale HTS dipole coil to LEO, operate cryocoolers continuously, measure radiation damage to REBCO tape, characterize debris interaction events, and demonstrate remote coil management. Cost: ~$100-200M (comparable to a NASA Discovery-class mission). This would validate (a) HTS coil lifetime in LEO radiation, (b) thermal management via passive radiators + active cryocoolers, (c) debris risk at the relevant cross-section scale, and (d) orbital O&M cost structure. No such mission is planned. Until this is done, the O&M cost is a placeholder with ±5× uncertainty.

### **Challenge 6: Launch Cost Replaces Capital Plant Cost as Primary CAPEX Driver**
**Verdict**: Likely resolvable (Starship operational timeline is 2-5 years; cost reduction is credible)
**Rationale**: At Falcon 9 pricing ($2,700/kg) and 10,000 kg spacecraft mass, launch cost is $27M (10.5% of total capital, 12.7% of overnight capital). This is significant but not dominant—spacecraft hardware ($83M per-module) and He3 startup inventory ($48.5M) exceed launch cost. Starship target pricing ($100-200/kg) would reduce launch to $1-2M per spacecraft, making it negligible. The uncertainty is whether Starship achieves this pricing and whether the 10,000 kg mass estimate is realistic.
**What would retire this risk**: Starship enters operational service with demonstrated $/kg to LEO pricing. This is on a 2-5 year timeline (Starship test flights ongoing as of 2026). The 10,000 kg mass estimate uncertainty is harder to retire—requires detailed spacecraft design (HTS coil winding, heating hardware, DEC mass breakdown, phased-array transmitter mass, thermal radiator sizing) that Zephyr has not disclosed. A conceptual design report from the company would convert this from "likely resolvable pending Starship" to "quantified with bounded uncertainty."

---

## 4. Structural Advantages and Disadvantages

### **Advantages vs. D-T Tokamak Baseline**

1. **Eliminates ~40% of direct capital (CAS21-23 structures + blanket/shield)**: No vacuum vessel (space provides vacuum), no first wall / blanket (He3 aneutronic eliminates neutron wall loading), no shield (DD neutrons at 10% energy fraction radiate to space), no tritium breeding infrastructure (Li-6 enrichment, FLiBe/Li-metal handling, tritium processing), no thermal cycle / turbine plant (direct conversion replaces Rankine), no building (ground station only). OpenStar D-T dipole (arxiv 2602.20564) allocates 4,320 km REBCO tape + Li₂O blanket + W-B₄C shield as major cost drivers (CAS22 dominates). Zephyr's orbital concept has none of these. Quantified elimination: CAS21 (buildings) ~$10M → ~$2M; CAS22 (blanket/shield) ~$200M → $0; CAS23-26 (turbine/electric/thermal) ~$150M → $2M rectenna. **Net structural advantage: ~$350M capital avoided at GW scale**, scaling to ~$35M at 10 MWe baseline.

2. **No tritium regulatory burden**: D-T concepts face NRC tritium licensing ($50-100M), tritium confinement systems (negative pressure, detritiation), and public opposition to tritium inventory (5-10 kg on-site for GW-scale plant). D-He3 orbital avoids all of this—no NRC jurisdiction for orbital nuclear operations (IAEA Outer Space Nuclear Safety Guidelines apply, simpler framework), no tritium handling (unless D-D breeding mode, which produces T as intermediate). **Regulatory cost avoided: $50-100M at GW scale** (not directly quantified in model but embedded in CAS10 reduction).

3. **Steady-state operation with no day/night variation**: Orbital platform has no diurnal cycle, no weather downtime, no seasonal variation. Capacity factor ceiling is set only by planned maintenance and unplanned failures (debris strikes, radiation-induced component degradation). Model assumes 90% availability (analysis Section 5 parameter table); terrestrial fusion baselines are 85-90% for steady-state, 70-80% for pulsed. **Advantage: ~5-10 percentage points higher capacity factor ceiling** than pulsed concepts, comparable to other steady-state MFE.

4. **Levitated dipole: no disruptions, no ELMs, no RWM**: Dipole confinement is intrinsically stable—no sawteeth, no edge-localized modes (ELMs), no resistive wall modes (RWMs), no disruption damage to first wall. LDX and RT-1 demonstrated disruption-free operation. This eliminates a major ITER/SPARC operational complexity and reduces first-wall replacement frequency. **Operational simplification advantage** (not easily quantified in LCOE but reduces unplanned downtime risk).

### **Disadvantages vs. D-T Tokamak Baseline**

1. **He3 fuel cost: $30M/kg market price vs. D-T fuel near-zero variable cost**: D-T breeding concepts have fuel cost ~$0.1-1M/yr at GW scale (deuterium extraction + Li-6 for breeding). D-He3 at market price is $48.5M/yr for 1 MWe delivered (model output line 52)—fuel alone is **484× higher cost than D-T**. Self-breeding is required for viability, but equimolar D:He3 is insufficient by 13× (analysis Section 2 hypothesis b). The only resolution is D-rich fuel (13:1 D:He3), which destroys the aneutronic advantage and produces DD neutrons requiring shielding. **Net disadvantage: $48M/yr fuel cost unless concept shifts to D-rich mode** (at which point it is no longer the concept described).

2. **Power beaming losses: 3.4% net efficiency vs. 35-40% thermal cycle efficiency**: D-T tokamak with Rankine thermal cycle achieves 35-40% thermal-to-electric efficiency. Zephyr's 4-stage chain (DEC 57% × transmitter 15% × beam 89% × rectenna 82%) yields 3.4% net (p_net / p_fus). Even in the optimistic case (DEC 65% × transmitter 50% × beam 89% × rectenna 90%), net efficiency is 26%—still 30-40% lower than thermal. **Revenue-side penalty: 10-20× more fusion power required per MWe delivered** compared to terrestrial thermal cycle. This is the dominant revenue-side disadvantage.

3. **Spacecraft capital cost: $258M total for 1 MWe → $255,100/kWe vs. $5,000-15,000/kWe terrestrial**: Launch cost ($27M Falcon 9), spacecraft hardware ($95M), He3 startup inventory ($48M), and ground rectenna ($2M) yield specific capital **17-50× higher than terrestrial fusion**. Even with Starship ($200/kg) and NOAK hardware cost reduction, specific capital is ~$60,000/kWe (optimistic scenario model output line 232: $96M CAS22 ÷ 5.3 MWe = ~$18k/kWe, scaling to $60k/kWe with full capital stack). This is the binding CAPEX disadvantage.

4. **On-orbit maintenance: impossible or prohibitively expensive**: Terrestrial fusion plants schedule first-wall replacement, blanket module swaps, and magnet maintenance during planned outages. Orbital platform has no crewed access—any component failure requires either (a) autonomous robotic repair (undemonstrated at this scale), (b) replacement spacecraft launch (cost = full unit CAPEX), or (c) deorbit and replacement (asset write-off). **Failure mode consequence: single HTS coil quench or DEC failure → total loss of $258M asset**. Terrestrial concepts can replace failed components for ~10-20% of total capital cost.

5. **Uncharacterized orbital risks: debris, radiation, thermal cycling**: LEO debris environment at 10-50 m plasma radius (large interaction cross-section) creates collision risk not present in terrestrial plants. Van Allen radiation damage to REBCO HTS tape over 10-15 year lifetime is uncharacterized (no space-qualified fusion HTS coil exists). Thermal cycling from Earth shadow passes (90-minute orbit → 45 min sun / 45 min shadow) stresses cryogenic systems. **Risk premium: model assumes 10-year plant lifetime; actual lifetime could be 3-5 years** if debris or radiation damage dominates, multiplying annualized capital by 2-3×.

### **Cost Structure Comparison (Baseline Case: 1 MWe Delivered)**

| CAS Account | D-T Tokamak (1 GWe) | Orbital Dipole (1 MWe) | Notes |
|-------------|---------------------|------------------------|-------|
| CAS21 Buildings | $50-100M | $2M (ground station only) | **Eliminated** |
| CAS22 Reactor Plant | $2,000-3,000M (blanket/shield/magnets/heating) | $95M (spacecraft hardware) | **Radically simplified** (no blanket/shield) |
| CAS23-26 BOP | $800-1,200M (turbine/electric/thermal) | $2M (ground rectenna) | **Eliminated** (direct conversion) |
| CAS50 Launch | $0 | $27M (Falcon 9) | **New cost category** |
| CAS80 Annual Fuel | $1-5M/yr (D-T breeding) | $48.5M/yr (He3 market) | **484× higher** unless self-breeding |
| Overnight Capital | $4,000-6,000M | $239M | **17× lower absolute $** but per-kWe is 17× higher due to power scale difference |
| Specific Capital | $5,000-8,000/kWe | $255,100/kWe | **32-51× higher** $/kWe |

**Key takeaway**: Orbital concept eliminates most conventional CAS accounts but introduces launch cost and catastrophic efficiency penalty (beaming losses). At MW scale, the concept has lower absolute capital ($239M vs. $4-6B for GW tokamak) but far higher specific capital ($/kWe). The crossover point where orbital becomes competitive is either (a) much higher power per spacecraft (10-100 MWe delivered requires beaming efficiency breakthrough), or (b) MW-scale is the target market and terrestrial fusion is not the competitor (SPS parity at $200-500/MWh is the relevant threshold).

---

## 5. Cross-Concept Positioning

**Where this concept sits in the landscape**: Zephyr Fusion occupies a unique position—it is the only orbital deployment fusion concept in the landscape and one of only two D-He3 aneutronic concepts (the other is Helion Energy FRC, 08-frc-w-direct-conversion). It shares levitated dipole confinement geometry with OpenStar Technologies (12-levitated-dipole, D-T terrestrial) but diverges completely on fuel, deployment environment, and energy conversion. The closest economic analogue is not fusion at all—it is **space-based solar power (SPS)**, which also delivers power from orbit via beaming to ground receivers and has the same cost structure (launch-dominated CAPEX + beaming infrastructure + ground rectenna).

**Concepts sharing similar economics**:

1. **Helion Energy (08-frc-w-direct-conversion)**: D-He3 fuel + direct energy conversion. Helion's handwritten analysis (analysis Section 7 cross-concept notes) shows He3 supply is the dominant cost risk and self-breeding via D-D → T → He3 decay is the mitigation strategy. Helion also found HTS magnets drive LCOE to ~20 ¢/kWh vs. ~4 ¢/kWh with copper coils—a 5× penalty. Zephyr uses HTS magnets (required for space mass constraints) and faces the same He3 cost sensitivity. **Shared challenge**: He3 fuel supply; **divergence**: Helion is terrestrial pulsed FRC (no launch cost, no beaming losses), Zephyr is orbital steady-state dipole (launch cost + beaming losses dominate).

2. **Space-Based Solar Power (SPS, not fusion)**: GEO SPS concepts (NASA NTRS 20140003205) have LCOE ~$200-500/MWh and are uncompetitive with ground CSP ($50-100/MWh) despite launch cost reductions. The binding constraint was ground infrastructure scale ($2B for GW-scale rectenna, 34 km² land area) and beaming efficiency (<30% end-to-end due to phased-array losses). Zephyr's optimistic scenario ($491/MWh, model output line 213) is within SPS parity but still 3-8× terrestrial fusion parity. **Shared challenge**: power beaming efficiency and ground infrastructure cost; **divergence**: SPS uses photovoltaics (TRL 8-9), Zephyr uses D-He3 fusion (TRL 1-2).

**What makes this concept fundamentally different**:

1. **Orbital deployment eliminates the vacuum vessel**: Every other MFE concept (tokamaks, stellarators, mirrors, FRCs, dipoles) has a vacuum vessel as a major cost and engineering challenge. Zephyr uses space vacuum, removing CAS22 (vacuum system) and CAS23 (first wall/blanket) entirely. This is a **categorical structural difference**, not a parametric variation.

2. **Launch cost replaces construction cost**: Terrestrial fusion capital is dominated by blanket/shield ($500M-1B), magnets ($300-800M), and building ($50-200M). Zephyr's capital is dominated by spacecraft hardware ($95M), launch ($27M Falcon 9 or $2M Starship), and He3 startup inventory ($48M if market-purchased). The cost structure has no overlap with terrestrial CAS frameworks.

3. **No grid connection—power is beamed**: Every terrestrial fusion concept delivers AC power to the grid at the plant site. Zephyr delivers power via microwave or laser beam to a ground rectenna field, which then feeds the grid. The efficiency chain includes beaming losses (model: 89% beam collection × 82% rectenna = 73% for stages 3-4 alone) that do not exist in terrestrial plants. The **revenue model is fundamentally different**: $/MWh must account for beaming losses and ground infrastructure cost, not just plant-gate electricity cost.

4. **Aneutronic fuel eliminates neutron shielding supply chain**: D-T concepts require tungsten (W), tungsten carbide cermet (WC), boron carbide (B₄C), and Li-6 enrichment for breeding blanket. D-He3 produces 2.45 MeV DD neutrons at ~10% energy fraction (radiated to space, no shielding needed) and no 14 MeV neutrons. This **eliminates ~$500M-1B in blanket/shield capital** at GW scale and removes tritium handling regulatory burden. Shared with p-B11 aneutronic concepts (18-p-b11-frc, 24-dense-plasma-focus), but orbital deployment is unique.

**Positioning summary**: Zephyr is economically closest to SPS (orbital power beaming) and technically closest to Helion (D-He3 fuel + direct conversion) but shares confinement heritage with OpenStar (levitated dipole). It is **not comparable** to conventional tokamaks or any terrestrial fusion concept—the cost structure, supply chain, and regulatory environment are categorically different. The relevant competitive threshold is SPS parity ($200-500/MWh), not terrestrial fusion parity ($50-150/MWh), because the concept must compete in the orbital-to-ground power market, not the terrestrial baseload market. If the concept achieves SPS parity, it unlocks a niche market (remote power delivery, military forward bases, disaster relief, lunar/Mars surface power via orbital relay); if it cannot reach SPS parity, it has no viable market.

---

## 6. Modeling Confidence

**Rating: Low**

**How many parameters are data-anchored vs. speculative?**

Of 32 key model parameters (power balance, efficiency chain, mass budget, costs), only **8 are data-anchored**:
- Fusion power split (80% charged, 10% neutron): nuclear data (Bosch & Hale 1992) — HIGH confidence
- ICRH wall-plug efficiency (70%): OpenStar D-T dipole baseline — MEDIUM confidence (different fuel)
- Beam collection efficiency (89%): SPS analogue (Shinohara 2005) — MEDIUM confidence (GEO not LEO)
- Rectenna efficiency (82%): mature technology — HIGH confidence
- Launch cost ($2,700/kg): Falcon 9 public pricing — HIGH confidence
- HTS coil mass (2,000 kg): LDX heritage + space qualification — MEDIUM confidence
- He3 market price ($30M/kg): CRS R41419 — MEDIUM confidence (2011 basis, may be outdated)
- Plant lifetime (10 years): satellite analogue — MEDIUM confidence (no fusion-specific data)

**24 parameters are speculative or inferred**:
- Fusion power per spacecraft (30 MW): back-calculated from "MW-class" YC claim — HIGH UNCERTAINTY
- Scientific Q (10): D-He3 reactivity analogy — HIGH UNCERTAINTY (undemonstrated in dipole)
- DEC efficiency (57%): Venetian blind upper bound for non-fusion ions, 14.7 MeV protons undemonstrated — HIGH UNCERTAINTY
- Transmitter efficiency (15%): phased-array phased-shifter loss estimate — HIGH UNCERTAINTY (MW scale undemonstrated)
- Heating system mass (1,500 kg): ITER ICRH scaling — HIGH UNCERTAINTY (space qualification adds unknown mass)
- DEC mass (1,000 kg): power density extrapolation — HIGH UNCERTAINTY (no DEC ever built at this scale)
- Transmitter mass (2,500 kg): SPS phased-array analogy — HIGH UNCERTAINTY
- Spacecraft hardware costs ($69M baseline): component-level buildup with no validation — HIGH UNCERTAINTY (could be 10-100× higher per analysis Section 7)
- Rectenna cost ($2M/MWe): SPS analogue — HIGH UNCERTAINTY (GW-scale SPS, not MW fusion)
- O&M cost (3% overnight capital): satellite analogy — HIGH UNCERTAINTY (no orbital fusion operations precedent)
- He3 consumption rate (1.6 kg/yr): derived from fusion power — MODERATE UNCERTAINTY (physics is certain, but fusion power assumption is uncertain)
- Capacity factor (90%): satellite uptime analogy — HIGH UNCERTAINTY (debris/radiation risk unquantified)
- All 13 CAS22 spacecraft hardware accounts: inferred from 1costingfe scaling laws or first-principles estimates — HIGH UNCERTAINTY

**What is the dominant source of LCOE uncertainty?**

The **4-stage efficiency chain** (DEC × transmitter × beam × rectenna) is the largest compound uncertainty. Each stage has 20-50% uncertainty, and they multiply:
- DEC: 57% baseline, could be 20% (proton range physics) to 80% (optimistic electrostatic decelerator) → 4× range
- Transmitter: 15% baseline (phased-array), could be 5% (extreme phase-shifter loss) to 75% (non-steering tube) → 15× range
- Combined: 3.4% baseline net efficiency (p_net/p_fus), plausible range 0.5% to 40% → **80× range on delivered power**

Because LCOE ~ 1/(delivered power) at fixed capital, this 80× efficiency range translates directly to an 80× LCOE range ($150/MWh to $12,000/MWh) holding all other parameters constant. No other uncertainty in the model has this magnitude.

**Second-tier uncertainty**: He3 fuel cost ($0 to $30M/kg) is a 2.75× LCOE multiplier (sensitivity sweep line 154-160) and is binary—either self-breeding works (concept shifts to D-rich fuel, sacrificing aneutronic premise) or it doesn't (market purchase is economically unviable). This is a discrete scenario branch, not a continuous uncertainty.

**Third-tier uncertainty**: Spacecraft hardware fabrication cost ($69M baseline, could be $690M at 10× FOAK multiplier per analysis Section 7) is a 6× LCOE multiplier in the optimistic scenario (model output line 240: 10× hardware → $3,106/MWh vs. baseline $491/MWh). But the breakeven for SPS parity is only 1.4× baseline ($96M hardware cost), so the viable corridor is narrow: **$69M to $96M spacecraft hardware cost** to stay below $500/MWh (SPS ceiling) in the optimistic case. Above $96M, the concept loses to SPS even with $0 He3 fuel and Starship launch.

**Confidence summary**: The LCOE estimate is a **first-pass corridor map**, not a defensible cost target. The model demonstrates that (a) baseline pessimistic case ($11,800/MWh) is 118× terrestrial fusion parity and uncompetitive with any energy source, (b) optimistic case ($491/MWh) reaches SPS parity but not terrestrial fusion parity, and (c) the viable corridor requires simultaneous success on three uncorrelated technology bets (He3 self-breeding, non-phased-array beaming, FOAK hardware cost <$100M). If any one bet fails, the concept falls outside the SPS parity window. The model is structurally sound (CAS framework adapted for orbital deployment, 4-stage efficiency chain correctly represented, He3 self-breeding arithmetic cross-checked against reactivity data) but parametrically fragile—changing any single high-uncertainty input by 2× shifts LCOE by 2-10×.

---

## 7. What Would Change My Mind

### **In the pessimistic direction (concept becomes less viable than baseline estimate):**

1. **Phased-array transmitter efficiency demonstrates <10% DC-RF at MW scale**: Baseline assumes 15% (per Shinohara 2005 phased-array loss analysis). If MW-scale demonstrations (JAXA, US Naval Research Lab follow-on experiments) show phase-shifter losses compound to 6-8 dB per element at high power, transmitter efficiency falls to 5-8%, cutting delivered power by 2× and raising LCOE from $11,800/MWh to $20,000-35,000/MWh. At that point, even the optimistic scenario (He3 $0, Starship launch) cannot reach SPS parity. **Specific milestone**: JAXA or DoD space solar power demonstration transmitting >1 MW continuous at >1 GHz with <10% measured DC-RF efficiency.

2. **HTS coil radiation lifetime in LEO <3 years**: Model assumes 10-year plant lifetime. If Van Allen proton/electron irradiation degrades REBCO critical current density by >50% within 3 years (no space-qualified fusion HTS coil data exists), replacement cadence is 3× faster than baseline, annualizing capital charge from $38.5M/yr to $115M/yr and raising LCOE from $11,800/MWh to $21,000/MWh. Concept becomes unviable even in optimistic scenario. **Specific milestone**: NASA or AFRL space-qualification test of REBCO tape in Van Allen belt analogue radiation environment (proton fluence >10^15 /cm² at 1-10 MeV) showing >50% Ic degradation in <1000 days.

3. **D-He3 dipole confinement scaling demonstrates τₑ ~ R^1.5 or weaker at fusion temperatures**: Baseline assumes τₑ ~ R² (favorable scaling). If intermediate-scale D-He3 dipole experiment (hypothetical ~$500M device, 10-year timeline) shows energy confinement time scales as τₑ ~ R^1.5 due to edge turbulence at 50 keV ion temperature, achieving Q=10 requires 2× larger coil radius or 4× higher magnetic field → 2-8× higher spacecraft mass → 2-8× higher launch cost + hardware cost → LCOE increases by 2-4×. At that point, optimistic scenario ($491/MWh) rises to $1,000-2,000/MWh, well above SPS parity. **Specific milestone**: RT-1 or LDX follow-on experiment reaches 20 keV ion temperature (still 2.5× below D-He3 requirement) and measures τₑ vs. R scaling exponent <1.8.

### **In the optimistic direction (concept becomes more viable than baseline estimate):**

1. **Direct demonstration of >60% DC-RF transmitter efficiency at MW scale using non-phased-array aperture (laser or fixed-beam microwave)**: Baseline phased-array is <20% efficient due to phase-shifter losses. If a laser power beaming system (demonstrated at kW scale) achieves >60% wall-plug-to-beam efficiency at MW scale, or if orbital tracking is solved via mechanical gimbals (not phase-shifting), transmitter efficiency jumps from 15% baseline to 60-75%, improving net beaming-only efficiency from 10.9% to 44-55% and full 4-stage efficiency from 3.4% to 14-20%. LCOE in baseline case falls from $11,800/MWh to $3,000-4,000/MWh; optimistic case falls from $491/MWh to $150-200/MWh (terrestrial fusion parity threshold). **Specific milestone**: Orbital laser power beaming demonstration (e.g., JAXA follow-on to SPRITZ, or DoD High Energy Laser program) transmitting >1 MW continuous over >100 km with >60% measured wall-plug-to-received-DC efficiency.

2. **Confirmation of D-D → He3 self-breeding closure in FRC or dipole geometry at >90% fuel self-sufficiency**: Helion Energy (08-frc-w-direct-conversion) is pursuing D-D breeding for He3 supply. If Helion or another group demonstrates (a) D-D fusion at sufficient rate to breed He3 via T decay (12.3 year half-life), (b) tritium extraction efficiency >95%, (c) He3 burnup in subsequent cycles achieving >90% fuel self-sufficiency, then He3 fuel cost drops from $48.5M/yr to near-zero, and baseline LCOE falls from $11,800/MWh to $4,293/MWh (sensitivity sweep line 154). Optimistic scenario becomes viable ($491/MWh, within SPS parity). **Specific milestone**: Helion Energy announces net electricity generation from D-He3 fuel with disclosed He3 breeding fraction >0.9× consumption rate, validated by third-party measurement of fuel throughput and tritium inventory.

3. **Starship achieves $100/kg to LEO pricing and Zephyr discloses spacecraft mass <5,000 kg**: Baseline spacecraft mass is 10,000 kg → $27M Falcon 9 launch. If Starship reaches operational $100/kg pricing (SpaceX target for mature reuse cadence) and Zephyr engineering design demonstrates 5,000 kg total spacecraft mass (2× lighter than baseline via aggressive mass optimization), launch cost falls to $500k per unit. Combined with NOAK spacecraft hardware cost reduction (serial production drives $69M baseline to $20M per model assumptions), total capital per spacecraft falls from $258M to ~$40M. At 1 MWe delivered, specific capital is $40,000/kWe (still 3-8× terrestrial fusion but within SPS range). LCOE in optimistic scenario falls from $491/MWh to $200/MWh (SPS floor, entering terrestrial fusion competitive zone). **Specific milestone**: SpaceX Starship completes 50+ operational flights with published per-kg pricing <$200/kg AND Zephyr publishes conceptual design review with component-level mass budget totaling <6,000 kg.

**Summary**: The concept's viability is **extremely sensitive to beaming efficiency** (1st optimistic lever) and **He3 self-breeding demonstration** (2nd optimistic lever). If either lever fails, the concept cannot reach SPS parity ($200-500/MWh) even with Starship-era launch costs. If both levers succeed, the concept reaches the low end of SPS parity and becomes viable for niche markets (orbital power relay, remote bases, space-to-space power transfer) but still does not compete with terrestrial fusion or renewables for grid baseload. The concept's fate hinges on two technology demonstrations that are (a) outside Zephyr's direct control (beaming efficiency depends on DoD/JAXA SPS programs; He3 breeding depends on Helion or other D-D fusion efforts) and (b) on decade-scale timelines (SPS at MW scale is 2030-2035; Helion D-He3 net electricity is 2028-2030 target per public statements).

---

## 8. LCOE Downselect Scoring

### C1: Modularization

**Score: 2.1**

| CAS Account | Construction Mode | Score | Cost Weight (%) | Weighted |
|-------------|-------------------|-------|-----------------|----------|
| **Spacecraft hardware (per-module accounts)** |
| C220103 (HTS coil) | Site-assembled from factory sub-assemblies | 3 | 18.1% ($15M / $83M) | 0.54 |
| C220104 (ICRH heating) | Site-assembled from factory sub-assemblies | 3 | 18.1% | 0.54 |
| C220105 (Spacecraft bus) | Factory-manufactured module | 5 | 6.0% | 0.30 |
| C220107 (Power electronics) | Factory-manufactured module | 5 | 4.8% | 0.24 |
| C220109 (DEC) | Stick-built / field-erected | 1 | 12.1% | 0.12 |
| C220110 (Remote handling) | Factory sub-assemblies | 3 | 2.4% | 0.07 |
| C220111 (Integration labor) | N/A (labor account) | 3 | 11.9% | 0.36 |
| C220112 (Fuel system) | Factory-manufactured module | 5 | 2.4% | 0.12 |
| C220113 (Phased-array transmitter) | Site-assembled from factory sub-assemblies | 3 | 24.1% | 0.72 |

**Sub-factor 1 (cost-weighted mode average)**: 3.01
**Sub-factor 2 (module repetition boost)**: No repetition boost within a single spacecraft (each subsystem is unique). Fleet scaling (10-100 units) would enable NOAK learning but does not apply to per-module construction mode. **+0.0**
**Module repetition note**: If a 100-unit fleet is built, HTS coil and transmitter become mass-produced modules (10-49 identical units per account → +1.0 boost per framework), but this is not the baseline scenario (single spacecraft).

**C1 = 3.01 + 0.0 = 3.0** (rounded to 1 decimal)

**Justification**: Spacecraft integration is fundamentally "site-assembled" (launch site clean room, TVAC chamber, final integration at launch pad) but benefits from factory-manufactured bus and electronics modules. The HTS coil is wound in a factory but requires on-site cryostat integration and space qualification testing (analogous to tokamak TF coil assembly). The DEC and phased-array transmitter are first-of-a-kind hardware with no manufacturing precedent—scored as stick-built. Integration labor (14% of hardware subtotal, model line 78) reflects high touch-time for FOAK spacecraft assembly. The 3.0 score reflects **moderate modularization advantage over stick-built terrestrial reactors** (which score 1.5-2.5) but **no advantage over factory-modular concepts** (laser IFE target factories, compact FRCs score 4-5). The orbital concept eliminates the reactor building (score +1 vs. terrestrial) but introduces spacecraft integration complexity (score -0.5 vs. pure factory modules).

---

### C3: Supply Chain Learning

**Score: 2.7**

#### Sub-factor A: Component learning rates (cost-weighted average)

| Component | Learning Rate Category | Score | Cost Weight | Weighted |
|-----------|------------------------|-------|-------------|----------|
| HTS coil (REBCO tape) | Industrial component with growing production base | 4 | 18.1% | 0.72 |
| ICRH heating | Specialty component with limited but existing supply chain | 3 | 18.1% | 0.54 |
| Spacecraft bus | Commodity component with established manufacturing | 5 | 6.0% | 0.30 |
| Power electronics | Industrial component with growing production base | 4 | 4.8% | 0.19 |
| DEC | Novel component never manufactured at scale | 1 | 12.1% | 0.12 |
| Phased-array transmitter | Specialty component with limited but existing supply chain | 3 | 24.1% | 0.72 |
| Fuel system (He3/D tanks) | Specialty component | 3 | 2.4% | 0.07 |
| Integration labor | N/A (learning curve applies but not a material) | 3 | 11.9% | 0.36 |
| Ground rectenna | Specialty component (SPS analogue, no fusion supply chain) | 2 | 2.5% | 0.05 |

**Sub-factor A = 3.07**

**Justification**: REBCO tape supply is scaling rapidly (SPARC, Commonwealth Fusion, multiple HTS startups driving demand from 1,000s km/yr to 10,000s km/yr globally). ICRH systems exist for ITER/tokamaks but space-qualified RF at MW scale is bespoke. Spacecraft bus is mature (SSL, Lockheed Martin produce 10-20 GEO buses/yr). DEC has no supply chain—Venetian blind concept was never productized. Phased-array transmitters exist for radar (Raytheon, Northrop Grumman) but MW-class space power beaming is TRL 3-4. Ground rectenna is undemonstrated at MW fusion scale (SPS analogue at kW scale).

#### Sub-factor B: Supply chain bottleneck count

**Hard constraints** (no known path to required quantity):
- **He3 fuel supply at commercial scale**: Global production ~2 kg/yr, concept requires 1.6 kg/yr per spacecraft. A 10-spacecraft fleet consumes 16 kg/yr (8× global production). No commercial He3 production infrastructure exists; self-breeding is undemonstrated. **-1.0 penalty**

**Scaling constraints** (exists but must scale 10x+):
- **REBCO tape**: Global production ~5,000 km/yr (estimate), small orbital coil requires ~100 km. Constraint for fleet scaling (100 spacecraft = 10,000 km demand), not single unit. **-0.5 penalty for fleet scaling bottleneck**

**Sole-source dependencies**:
- **Falcon 9 / Starship launch**: SpaceX is the only provider at <$3,000/kg to LEO. Blue Origin New Glenn (2025 target) is 2nd source but unproven. **-0.25 penalty**

**Helium-3 fuel dependency penalty**: **-1.5 penalty** (framework-specified)

**Sub-factor B = 5.0 - 1.0 - 0.5 - 0.25 - 1.5 = 1.75** (clamped to [1,5])

**Justification**: He3 supply is the dominant bottleneck—market price is $30M/kg and global production is insufficient for a commercial fleet. Self-breeding requires undemonstrated D-D fusion closure (analysis Section 2 hypothesis b). REBCO tape is a scaling constraint (not binding for single unit but blocks fleet deployment). Launch is sole-sourced to SpaceX until New Glenn proves operational. The -1.5 He3 penalty is framework-mandated and reflects the unique criticality of He3 scarcity.

#### Sub-factor C: External demand pull

**Components with >$1B/yr external market**:
- Spacecraft bus: $5M (satellite industry ~$15B/yr globally, addressable for fusion bus design) → 6.0% of capital
- Power electronics: $4M (space power electronics ~$2B/yr market) → 4.8% of capital
- Launch services: $27M (SpaceX revenue ~$8B/yr in 2025, orbital launch market ~$10B/yr) → 32.3% of capital
- **Total: 43.1% of capital has >$1B/yr external market**

**Score: 4** (framework: 40-60% → score 4)

**Justification**: Launch services and spacecraft bus benefit from strong external demand (satellite constellations, DoD, NASA). HTS coil (18.1% of capital) has growing fusion industry pull but <$1B/yr market (SPARC + CFS + startups ~$500M/yr combined REBCO demand estimate). DEC (12.1% of capital) and phased-array transmitter (24.1% of capital) have zero external demand—first-of-a-kind fusion hardware. Ground rectenna (2.5% of capital) has SPS research interest but no commercial market.

**C3 = (3.07 + 1.75 + 4.00) / 3 = 2.94 → 2.9**

---

### C4: Plant Complexity

**Score: 3.5**

#### Sub-factor A: Operational coupling density (1-5)

**Score: 4 (mostly decoupled; few critical interdependencies)**

**Justification**: The orbital concept has **lower operational coupling than terrestrial fusion** due to elimination of blanket/shield/thermal cycle integration. Key subsystem dependencies:
- HTS coil → cryocooler (if cryocooler fails, coil quenches → total plant shutdown). **Critical coupling path.**
- ICRH heating → plasma sustainment (if heating fails, plasma extinguishes → zero fusion power). **Critical coupling path.**
- DEC → power output (if DEC fails, no electricity generation but heating can continue from solar panels if installed). **Degrading, not binary.**
- Phased-array transmitter → power delivery (if transmitter fails, power cannot be beamed but can be stored in batteries or used for onboard loads). **Degrading, not binary.**

**Failure cascade assessment**: Cryocooler failure → coil quench → plasma loss → zero output (single-point failure cascade). Heating failure → plasma loss → zero fusion output but plant remains safe (no disruption damage in dipole). DEC or transmitter failure → power delivery lost but plant can be mothballed without asset loss. **Score 4: few failure cascades (only cryocooler is single-point), subsystems can be maintained independently if component failures are non-destructive.**

**Comparison to tokamak**: Terrestrial tokamak has blanket/shield/first-wall/divertor/coolant loop tightly coupled (coolant failure → blanket overheat → shutdown; divertor failure → impurity contamination → density control loss). Orbital dipole eliminates these loops. **+1 point vs. tokamak baseline (score 3).**

**Comparison to laser IFE**: Laser IFE has driver/target factory/chamber as decoupled subsystems (driver maintenance does not require chamber shutdown). **-0.5 points vs. laser IFE (score 4.5-5).**

#### Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)

**CAS22 sub-accounts >1% of capital** (from model output lines 68-80):
1. C220103 (HTS coil): $15M (18.1%)
2. C220104 (ICRH heating): $15M (18.1%)
3. C220105 (Spacecraft bus): $5M (6.0%)
4. C220107 (Power electronics): $4M (4.8%)
5. C220109 (DEC): $10M (12.1%)
6. C220111 (Integration labor): $9.9M (11.9%)
7. C220113 (Phased-array transmitter): $20M (24.1%)

**Count: 7 significant subsystems**

**Score: 4** (framework: 5-7 subsystems → score 4)

**Justification**: Seven major subsystems is at the high end of "moderate complexity." Terrestrial tokamak has 12-15 significant CAS22 accounts (blanket, shield, divertor, first wall, vacuum vessel, TF coils, PF coils, central solenoid, heating, fueling, tritium processing, coolant loops, remote handling). Laser IFE has 4-6 (driver, target factory, chamber, final optics, coolant). Orbital dipole is intermediate—simpler than tokamak (no blanket/shield/divertor), more complex than laser IFE (additional spacecraft bus/cryocooler/transmitter).

**C4 = (4 + 4) / 2 = 4.0**

**Revision after "magic wand" test**: If D-He3 fusion physics were proven tomorrow (τₑ ~ R² scaling confirmed, Q=10 achieved in subscale device), would this plant still be hard to build and operate? **Answer: Partially.** The spacecraft integration (7 major subsystems, TVAC testing, launch integration, orbital deployment, cryocooler operation in LEO thermal environment) is inherently complex regardless of fusion physics maturity. But the **dominant operational challenge is physics, not engineering**: maintaining 50 keV ion temperature with ICRH coupling in a dipole geometry, managing He3 fuel resupply logistics, and achieving 10-year HTS coil lifetime under Van Allen radiation. Much of the "complexity" is actually **technical risk (C7), not operational complexity (C4)**. Revising:

- **Sub-factor A: 3.5** (reducing from 4.0). Failure cascades are few, but the cryocooler single-point failure + He3 fuel delivery logistics + orbital maintenance constraints make operations harder than the subsystem count suggests. Still better than tokamak (score 2-3) due to no blanket/coolant loops, but not as decoupled as pure factory-modular concepts.
- **Sub-factor B: 4** (unchanged).

**C4 = (3.5 + 4) / 2 = 3.75 → 3.8**

**Final revision**: Operational coupling density is being inflated by physics risks (fuel delivery, radiation lifetime). Applying "magic wand" strictly: **if fusion physics worked, is the built plant operationally complex?** Yes—cryocooler failure still cascades to total loss, and orbital maintenance is impossible. But this is **asset risk (binary failure = $258M loss), not operational coupling (cascading subsystem failures)**. Asset risk belongs in C7 (hardware risk for power conversion function). Returning to **Sub-factor A = 4** as initially scored. **C4 = 4.0.**

**Compromise**: Splitting the difference—orbital maintenance impossibility is an **operational constraint** (cannot swap components mid-life), which increases coupling density indirectly (any failure requires full asset replacement). **Final Sub-factor A = 3.5.**

**C4 = 3.5 + 4 = 7.5 / 2 = 3.75 → 3.8 (rounded to 1 decimal) → 3.8**

**Final answer: C4 = 3.8**, acknowledging moderate complexity (7 subsystems, few cascades but binary asset-loss failure mode for cryocooler/coil).

---

### C5: Customization Needs

**Score: 3.6**

#### Sub-factor A: Thermal rejection (1-4)

**Score: 4** (no thermal cycle; passive radiation cooling only)

**Justification**: Orbital platform has no thermal cycle (direct conversion eliminates Rankine/Brayton). Waste heat from recirculating power (4.44 MW heating + cryocooler + housekeeping) is rejected via **thermal radiators** (passive radiation to space at ~300 K). No cooling towers, no condenser, no water source required. This is the maximum thermal simplification score. **Comparison**: D-T tokamak with Rankine cycle (score 2); hybrid DEC+thermal (score 3); p-B11 aneutronic with full DEC (score 4, same as this concept).

#### Sub-factor B: Fuel safety profile (1-4)

**Score: 3** (D-He3: low neutron fraction, no tritium handling)

**Justification**: D-He3 produces 2.45 MeV DD neutrons at ~10% energy fraction (analysis Section 5 parameter table, f_neutron=0.10) but no tritium breeding or handling infrastructure. Framework assigns:
- p-B11 (aneutronic, no tritium) → score 4
- D-He3 (low neutron fraction, no tritium) → score 3
- D-D (neutrons but no tritium handling) → score 2
- D-T (full tritium handling and breeding) → score 1

D-He3 is score 3 per framework. **Note**: If the concept shifts to D-rich fuel (13:1 D:He3 for self-breeding per analysis Section 2 hypothesis b), DD neutron fraction rises from 10% to ~30%, and shielding becomes necessary—downgrading fuel safety profile. But baseline concept (equimolar D:He3) remains score 3.

**C5 raw = (4 + 3) / 2 = 3.5**

**Scale to [1,5]**: C5 = 1 + (3.5 - 1) × (4/3) = 1 + 2.5 × 1.333 = 1 + 3.33 = 4.33

**CRITICAL ERROR**: Framework formula is **C5 = 1 + (raw - 1) × (4/3)**, which maps raw [1,4] to [1,5.67]. But the framework specifies "scale to [1,5] range" and provides the formula. Let me recompute:

If raw = 3.5 (average of two 1-4 sub-factors), then:
C5 = 1 + (3.5 - 1) × (4/3) = 1 + 2.5 × 1.333 = 1 + 3.333 = 4.33

But this exceeds 5.0 if raw = 4.0 (max): C5 = 1 + (4 - 1) × (4/3) = 1 + 4 = 5.0. **Framework formula is correct.**

**C5 = 1 + (3.5 - 1) × (4/3) = 4.33 → 4.3**

**Justification**: Orbital deployment eliminates site-specific thermal rejection needs (no cooling tower site survey, no water permits, no once-through cooling environmental impact). D-He3 fuel eliminates tritium handling licenses and breeding infrastructure. The concept has minimal site customization needs—ground station is a rectenna field + grid tie, which is commodity infrastructure (SPS analogue). The 4.3 score reflects **high favorability on customization** (only p-B11 aneutronic concepts score higher at ~4.5-5.0).

---

### C8: Data Adequacy

**Score: 1.5**

#### Sub-factor A: Source diversity & independence (1-5)

**Score: 2** (almost exclusively academic/heritage sources, no company publications)

**Justification**: Zephyr Fusion has published zero technical papers, zero patents, zero conference presentations as of March 2026 (analysis Section 1). The analysis relies entirely on:
- **Academic heritage**: LDX/RT-1 experiments (MIT/U.Tokyo, 2004-2012), Hasegawa & Chen 1987 (PPPL-2627), arxiv 2602.20564 OpenStar D-T dipole (2026 preprint)
- **Company disclosure**: YC launch page only (~500 words, no quantitative parameters)
- **SPS analogue literature**: Shinohara 2005 (power beaming), NASA NTRS 20140003205 (rectenna cost)
- **He3 supply**: CRS R41419 (2011 Congressional Research Service report)

**No independent validation** of Zephyr's concept exists—NASASpaceFlight forum discussion (analysis Section 1) is community skepticism, not validation. All technical parameters are inferred from heritage literature for **different concepts** (D-T terrestrial dipole, D-He3 tokamak, GEO solar power satellites). **Score 2 per framework: "Almost exclusively company publications" → but in this case, almost NO publications at all.** Academic sources are independent but do not describe Zephyr's specific concept (orbital D-He3 dipole). Revising to **score 1-2 boundary: ~1.5 rounded to 2** for having *some* independent academic sources, even if not directly applicable.

**Final Sub-factor A: 2**

#### Sub-factor B: Reactor design specification (1-5)

**Score: 1** (no reactor design beyond basic concept description)

**Justification**: Zephyr has disclosed **zero reactor design parameters**—no plasma density, no temperature target, no Q target, no heating power, no spacecraft mass breakdown, no DEC design, no power beaming architecture. The YC launch page states "meter-scale HTS magnets" (no dimensions), "megawatt-class power" (no MWe number), "Falcon 9 deployable" (no payload mass), "magnetized volume exceeding ITER" (no volume number). The analysis gap report (Section 5) lists 16 missing parameters rated "blocking" or "important," including target net electrical output, plasma design point, energy conversion pathway, and capital cost structure. **Framework score 1: "No reactor design beyond basic concept description."** The concept exists as a physical principle (levitated dipole in space, D-He3 aneutronic) with no engineering specification.

#### Sub-factor C: LCOE parameter coverage (1-5)

**Blocking gap count** from gap_report.md (read in context):

Let me count blocking gaps explicitly from the gap report text (lines 33-148):

1. Company technical disclosure (fuel, heating, conversion) — blocking
2. No orbital fusion power plant study of any kind exists — blocking
3. No applicable LCOE framework for orbital power delivery — blocking
4. Power beaming losses and infrastructure cost — blocking
5. Capital cost breakdown (launch, conversion, beaming) — blocking
6. Falcon 9 launch cost (now sourced, not blocking) — RESOLVED in analysis
7. System mass — blocking
8. Target fusion power — blocking
9. Target Q — blocking
10. Direct conversion efficiency — blocking
11. Power beaming efficiency — blocking
12. He3 fuel supply strategy — blocking
13. Operating cost (fuel resupply, orbital maintenance) — blocking
14. Direct energy conversion technology at reactor scale — blocking
15. He3 supply path to orbital platform — blocking

**Blocking gap count: 13-14** (some overlap between "no LCOE framework" and "capital cost breakdown"). Framework scoring:
- 5 = 0 blocking gaps
- 4 = 1-2 blocking gaps
- 3 = 3-4 blocking gaps
- 2 = 5-7 blocking gaps
- 1 = 8+ blocking gaps

**Score: 1** (8+ blocking gaps → score 1 per framework)

**Justification**: Every LCOE-critical parameter is either missing (company has not disclosed) or truly-unknown (no published study of orbital fusion power delivery exists). The model in model_setup.py is a **parametric corridor map**, not a data-driven estimate—it back-calculates fusion power from an assumed 1 MWe delivered output, infers DEC efficiency from 1970s Venetian blind experiments on non-fusion ions, borrows beaming efficiency from GEO SPS studies, and uses He3 market price from a 2011 government report. None of these are Zephyr-specific data. The gap report explicitly states "insufficient data" overall readiness rating.

#### Sub-factor D: Commercialization pathway clarity (1-5)

**Score: 1** (no commercialization pathway articulated)

**Justification**: Zephyr has disclosed no timeline, no milestones, no funding beyond YC F25 seed, no experimental device plans, no partnerships, no customer LOIs, and no technical development roadmap. The YC launch page states only "we're building fusion power in space" with no staged development plan. For context:
- **Score 5 example**: Tokamak Energy (detailed STEP program, £200M Series E, 2030s grid delivery target)
- **Score 3 example**: Helion Energy (Polaris demonstration target 2028, Microsoft PPA signed, subscale Trenta device operational)
- **Score 1 example**: Zephyr Fusion (no disclosed milestones, no device timeline, no commercialization pathway beyond "space makes fusion easier")

**C8 = (2 + 1 + 1 + 1) / 4 = 1.25 → 1.3**

**Justification**: Data adequacy is extremely poor. The analysis is possible only by leveraging academic heritage literature (LDX, OpenStar, Hasegawa 1987) and space power analogues (SPS studies), none of which directly describe Zephyr's concept. The company has provided no technical data, no reactor design, and no commercialization plan beyond a vision statement. The 1.3 score reflects **near-minimum data adequacy**—slightly above 1.0 only because *some* academic analogues exist, preventing complete inability to analyze. This is the lowest C8 score in the concept landscape (tied with other pre-prototype, no-publication startups).

---

### C7: Technical Risk Evidence (Risk Matrix)

I will now score the 7-function × 2-subcategory = 14-cell risk matrix.

#### Function 1: Plasma Performance

**Subcategory: Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | D-He3 dipole at 50-100 keV ion temperature achieving triple product ≥10²⁰ keV·s·m⁻³ (10× higher than D-T requirement) for Q≥10 net fusion gain |
| Best demonstrated | LDX achieved few-hundred-eV electron temperature, ~10¹⁷ m⁻³ density, <10 ms confinement (estimated triple product ~10¹³-10¹⁴ keV·s·m⁻³). RT-1 achieved similar parameters. No D-He3 operation at any temperature in any confinement geometry at fusion-relevant triple product. |
| Gap ratio | 10⁶-10⁷× (requirement 10²⁰ / demonstrated 10¹³-10¹⁴) |
| Closure mechanism | Proponents claim τₑ ~ R² scaling enables favorable extrapolation from LDX/RT-1 (few-hundred-eV, sub-meter scale) to reactor (50-100 keV, meter-scale). OpenStar arxiv 2602.20564 notes "no such model exists for dipoles" for energy confinement scaling law and requires intermediate-scale experimental validation at 10¹⁹ keV·s·m⁻³ before reactor commitment. |
| Classification | **Binary** (zero net electricity if D-He3 ignition cannot be sustained) |
| Evidence tier | **2** (simulation only, no experimental validation at fusion-relevant temperature or density) |

**Subcategory: Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | HTS dipole coil providing ≥5 T field at 1-meter radius, operating continuously for 10 years in LEO Van Allen radiation environment (proton fluence >10¹⁵ /cm² at 1-10 MeV), with cryocooler maintaining <30 K and passive radiators rejecting ~100 kW thermal load in LEO thermal cycling (45 min sun / 45 min shadow per 90-min orbit). |
| Best demonstrated | LDX levitated superconducting coil operated in terrestrial environment at 1 T peak field (not HTS, used NbTi). RT-1 used permanent magnets. No HTS fusion magnet has operated in space. REBCO tape radiation testing (ground-based) shows <10% critical current degradation at 10¹⁴ /cm² fluence (1× lower than LEO 10-year exposure). No space cryocooler has operated continuously at <30 K for >1 year. |
| Gap ratio | Radiation fluence: 10× beyond demonstrated HTS damage threshold. Cryocooler lifetime: >10× beyond demonstrated space cryocooler continuous operation (JWST cryocooler is <5 years design life). |
| Closure mechanism | REBCO tape space qualification testing (NASA/AFRL), active cryocooler arrays (Stirling or pulse-tube) with redundancy, thermal radiator panel sizing via analysis (no demonstration required). |
| Classification | **Binary** (if HTS coil quenches due to radiation damage or cryocooler fails, plasma is lost and plant cannot restart without coil replacement—impossible on orbit) |
| Evidence tier | **2** (simulation + subscale ground testing; no orbital HTS fusion magnet demonstration) |

**Function-level mean F1**: (2 + 2) / 2 = **2.0**

---

#### Function 2: Driver / Energy Input (Heating)

**Subcategory: Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | ICRH or ECRH delivering 3-5 MW (at Q=10) to sustain 50-100 keV D-He3 plasma in dipole geometry with coupling efficiency ≥50% (input power → plasma heating). |
| Best demonstrated | ECRH demonstrated on LDX at few-hundred-eV electron temperature, coupling efficiency not disclosed. ICRH studied on RT-1 with "mixed results" per OpenStar arxiv 2602.20564. No ICRH or ECRH demonstrated at >20 keV ion temperature in dipole geometry. Tokamak ICRH achieves 50-70% coupling efficiency at 10-20 keV; extrapolation to 50-100 keV in dipole is unvalidated. |
| Gap ratio | Temperature: 50-100× (requirement 50-100 keV / demonstrated few-hundred-eV). Power scale: 100-1000× (requirement 3-5 MW / LDX ~10 kW ECRH). |
| Closure mechanism | Proponents assume ICRH (70% wall-plug efficiency) couples efficiently at D-He3 temperature by analogy to tokamak scaling. RT-1 follow-on experiments targeting ICRH coupling at 5-10 keV would partially close gap. |
| Classification | **Degrading** (if coupling efficiency falls below 50%, recirculating power fraction rises and Q_eng falls, worsening LCOE but not preventing net electricity) |
| Evidence tier | **3** (partial demonstration—ECRH works on LDX at low temperature, ICRH demonstrated in tokamaks but not dipoles at D-He3 conditions) |

**Subcategory: Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Space-qualified ICRH system (3-5 MW RF power, 20-100 MHz, gyrotrons or solid-state RF, mass <2,000 kg) operating in LEO thermal/vacuum environment with wall-plug efficiency ≥70% for 10 years. |
| Best demonstrated | Terrestrial ICRH systems (ITER 20 MW, tokamak heritage) operate at 70% wall-plug efficiency but are not space-qualified. Gyrotrons for ECRH are 1-2 MW units at >5,000 kg each (ITER baseline). No MW-scale RF heating system has operated in space. Mass estimate (1,500 kg per model) assumes 3× reduction from terrestrial ITER-scale ICRH via solid-state RF and space integration—undemonstrated. |
| Gap ratio | Space qualification: never demonstrated. Mass: 3-5× reduction required from terrestrial analogue. Lifetime: 10 years continuous (terrestrial systems have <5 year replacement cycles for RF tubes). |
| Closure mechanism | Space-qualified solid-state RF amplifiers (DoD satellite comms heritage at kW scale, extrapolated to MW scale), thermal radiators for RF tube cooling, redundancy for 10-year lifetime without servicing. |
| Classification | **Degrading** (if heating system fails mid-life, net output drops to zero until restart, but replacement is impossible on orbit → permanent output loss. This is effectively binary asset loss but not a "no net electricity if unmitigated" design flaw—the technology works, it just cannot be serviced.) |
| Evidence tier | **2** (simulation + component-level terrestrial analogy; no space-qualified MW-scale RF heating system demonstrated) |

**Function-level mean F2**: (3 + 2) / 2 = **2.5**

---

#### Function 3: Instability Control

**Subcategory: Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Dipole confinement maintaining MHD stability (no disruptions, no sawteeth, no edge-localized modes) at D-He3 reactor conditions (50-100 keV ion temp, β~0.5-0.8) for continuous operation over years. |
| Best demonstrated | LDX and RT-1 demonstrated disruption-free, sawtooth-free operation at all plasma conditions tested (few-hundred-eV, β~0.1-0.3). Levitated dipole is intrinsically stable—no kink modes, no tearing modes in closed-field-line region. This is the core physics advantage of dipole confinement. |
| Gap ratio | N/A (no gap—instability-free operation is demonstrated at subscale and extrapolates favorably) |
| Closure mechanism | No closure mechanism needed—instability suppression is intrinsic to dipole topology, not a control challenge. |
| Classification | **Degrading** (if unexpected high-beta instabilities emerge at D-He3 conditions, β must be reduced → lower fusion power density → larger/heavier coil for same net output, but not a binary failure) |
| Evidence tier | **4** (near-regime demonstrated—disruption-free operation confirmed in LDX/RT-1 across all accessible parameter space, within 2× of β requirement but 100× below temperature requirement; high confidence in extrapolation for MHD stability, low confidence for kinetic instabilities at 50 keV) |

**Subcategory: Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | No active instability control hardware required (no feedback coils, no disruption mitigation system). Passive structure only: dipole coil mechanical support, quench detection, emergency shutdown (coil deenergization). |
| Best demonstrated | LDX passive levitation and quench detection operated successfully. No hardware failures caused by plasma instabilities (because none occurred). |
| Gap ratio | 1× (no gap—hardware requirement is minimal and demonstrated) |
| Closure mechanism | N/A (no gap) |
| Classification | **Degrading** (quench detection failure → coil damage, but this is a sensor/electronics reliability issue not specific to instability control) |
| Evidence tier | **5** (operating-regime demonstrated—passive instability tolerance is validated at LDX/RT-1 scale; no extrapolation risk for hardware since no active control hardware is needed) |

**Function-level mean F3**: (4 + 5) / 2 = **4.5**

---

#### Function 4: Plasma-Wall Interaction

**Subcategory: Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | Plasma loss-cone flux to spacecraft surfaces (antennae, heating ports, DEC electrodes) must remain below material erosion limits (<10 MW/m² peak heat flux) and impurity contamination must not quench D-He3 fusion (Z_eff <2). No material walls inside dipole separatrix (loss-cone flux exits to space, not to walls). |
| Best demonstrated | LDX and RT-1 operated with loss-cone flux to chamber walls at few-hundred-kW/m² peak. No erosion issues observed at these conditions. At D-He3 reactor conditions (50-100 keV ions), loss-cone flux rises by ~100× due to higher temperature and power density. Impurity contamination in dipoles is self-limiting (impurities are expelled to separatrix by centrifugal force in rotating plasma)—demonstrated in RT-1. |
| Gap ratio | Heat flux: 100× (requirement <10 MW/m² / demonstrated ~0.1 MW/m²). Temperature: 100× (requirement 50-100 keV / demonstrated few-hundred-eV). |
| Closure mechanism | Orbital geometry eliminates chamber walls—loss-cone flux exits to space, not to material surfaces. Only DEC electrodes and heating antennae intercept flux, and these can be designed with refractory materials (tungsten, molybdenum, graphite) to tolerate 10 MW/m². Impurity self-expulsion is intrinsic to dipole rotation (demonstrated in RT-1). |
| Classification | **Degrading** (if DEC electrodes erode faster than 10-year lifetime, efficiency falls and replacement is required—impossible on orbit, leading to permanent output degradation. But this is a lifetime issue, not a "no net electricity" physics failure.) |
| Evidence tier | **3** (subscale demonstration—RT-1 showed impurity self-cleaning, but D-He3 heat flux to DEC electrodes at 50-100 keV is undemonstrated) |

**Subcategory: Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | DEC electrodes (tungsten or molybdenum, electrostatic or magnetic separatrix extraction) withstanding 10 MW/m² peak heat flux from 14.7 MeV protons and 3.6 MeV alpha particles for 10 years without erosion >10% thickness loss. Heating antennae (ICRH or ECRH) tolerating ~1 MW/m² backscattered power. |
| Best demonstrated | Venetian blind DEC (1970s) used copper electrodes with water cooling for non-fusion ions at <1 MW/m² heat flux. No DEC has been tested with 14.7 MeV protons. ITER divertor targets (tungsten) are designed for 10-20 MW/m² heat flux in tokamak edge plasma (1-5 keV ions), not 14.7 MeV protons. Proton range in tungsten at 14.7 MeV is ~0.6 mm (NIST PSTAR)—electrode must be >6 mm thick to stop protons, creating material activation and thermal stress challenges. |
| Gap ratio | Particle energy: 1000× (14.7 MeV protons / 10-20 keV tokamak divertor ions). Lifetime: >10× (10 years continuous / <1 year ITER divertor target replacement cycle). Cooling: passive radiation only (no active cooling in space) vs. active water cooling in terrestrial DEC/divertor. |
| Closure mechanism | Refractory metal electrodes (tungsten, TZM molybdenum) with passive radiation cooling via backside thermal radiators. Materials qualification testing (proton accelerator beam testing at 10-20 MeV, simulating DEC environment). Alternative: magnetic divertor DEC (no electrodes, charged particles spiral along field lines to collection region) eliminates direct material interaction—TRL 2-3. |
| Classification | **Degrading** (electrode erosion → DEC efficiency falls over time → LCOE rises, but not a binary failure unless erosion is catastrophic <1 year) |
| Evidence tier | **2** (simulation only—no 14.7 MeV proton DEC hardware tested; ITER divertor analogy is for different particle energy and cooling mechanism) |

**Function-level mean F4**: (3 + 2) / 2 = **2.5**

---

#### Function 5: Neutron/Particle Handling

**Subcategory: Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | D-D side reactions produce 2.45 MeV neutrons at ~10% of fusion energy (3 MW neutron power at 30 MW fusion baseline). These neutrons radiate to space with no spacecraft activation concern (flux to HTS coil and DEC is negligible due to large standoff distance ~10-50 m separatrix radius). |
| Best demonstrated | D-D neutron production is well-understood nuclear physics. LDX operated with deuterium plasmas at sub-fusion conditions (no measurable neutron yield). OpenStar D-T dipole study (arxiv 2602.20564) analyzed 14 MeV neutron transport in terrestrial geometry with W-B₄C shielding. Orbital geometry has no shielding—neutrons exit to space, no activation. |
| Gap ratio | 1× (no gap—neutron physics is well-understood, and orbital geometry eliminates the activation challenge by design) |
| Closure mechanism | N/A (no closure needed—neutrons radiate to space, no material interaction) |
| Classification | **Degrading** (if neutron flux to HTS coil is higher than estimated due to scattering from spacecraft structure, coil radiation damage accelerates → shorter lifetime, but this is a hardware lifetime issue not a physics failure) |
| Evidence tier | **5** (operating-regime demonstrated—D-D neutron production is standard nuclear physics, and neutron transport in vacuum is trivial; no extrapolation uncertainty) |

**Subcategory: Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | HTS coil and DEC/transmitter electronics tolerating background neutron flux from D-D reactions (~10¹⁰ n/cm²/s at 10 m standoff, 2.45 MeV neutrons) plus Van Allen proton/electron flux for 10 years without >20% performance degradation. REBCO tape displacement damage threshold >10¹⁵ n/cm² (fast neutron equivalent). Electronics radiation-hardened to ≥100 krad total ionizing dose. |
| Best demonstrated | REBCO tape ground-based radiation testing: <10% critical current degradation at 10¹⁴ n/cm² fast neutron fluence (1 order of magnitude below 10-year orbital requirement). Space electronics (satellite avionics) routinely hardened to 100-300 krad TID and operate in Van Allen environment for 10-15 years. No HTS fusion magnet has operated in combined neutron + Van Allen radiation environment. |
| Gap ratio | REBCO neutron fluence: 10× beyond demonstrated threshold (10¹⁵ requirement / 10¹⁴ demonstrated). Combined radiation (neutron + proton + electron): never tested. |
| Closure mechanism | REBCO tape irradiation testing in mixed neutron + proton beams (simulating combined fusion + Van Allen environment). Radiation-hardened electronics (space-grade ASICs, FPGA with triple-module redundancy). Shielding (if needed) via polyethylene or borated plastic around sensitive electronics—adds mass but tractable. |
| Classification | **Degrading** (radiation-induced degradation → coil performance loss → lower field → lower fusion power, but not a binary failure unless degradation is catastrophic) |
| Evidence tier | **3** (subscale demonstration—REBCO radiation tolerance tested at 10¹⁴ n/cm² but not in combined environment or at 10¹⁵ requirement; space electronics heritage validates rad-hard approach but not for fusion neutron spectrum) |

**Function-level mean F5**: (5 + 3) / 2 = **4.0**

---

#### Function 6: Fuel Cycle Closure

**Subcategory: Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | He3 self-breeding via D-D side reactions (D+D → T+p, then T → He3+β⁻ over 12.3 year half-life) at ≥100% breeding fraction (bred He3 per year ≥ consumed He3 per year) to eliminate external He3 procurement. Equimolar D:He3 fuel composition (50:50) assumed for aneutronic operation. |
| Best demonstrated | D-D fusion produces T at 50% branching ratio (D+D → T+p) and He3 at 50% branching ratio (D+D → He3+n) per nuclear data. Helion Energy claims D-D → T → He3 breeding in FRC geometry but has not disclosed breeding fraction or demonstrated >1 year of continuous closed-loop fuel operation. No dipole experiment has demonstrated D-D breeding. Analysis Section 2 hypothesis (b) arithmetic: equimolar D:He3 self-breeding fraction = 7.5% of consumption (⟨σv⟩_DD / ⟨σv⟩_DHe3 ≈ 1/6.7 at 100 keV), requiring 13:1 D:He3 ratio to approach sufficiency—this negates the aneutronic advantage (DD neutron fraction rises from 10% to ~30%). |
| Gap ratio | 13× (self-sufficiency requires 13:1 D:He3 / equimolar 1:1 operation) |
| Closure mechanism | Proponents claim D-rich fuel mode (13:1 D:He3) enables self-breeding, accepting DD neutron production (2.45 MeV at ~30% energy fraction) as trade-off. Tritium extraction and decay management over 12.3 years required. No demonstration exists in any geometry. |
| Classification | **Binary** (if He3 self-breeding at ≥100% is not achieved, external He3 procurement at $30M/kg is required → fuel cost $48.5M/yr for 1 MWe → LCOE $11,800/MWh → economically unviable. This is a mandatory binary classification per framework: "He-3 self-breeding at scale" is always binary.) |
| Evidence tier | **1** (asserted/absent—no experimental validation of D-D → He3 breeding closure in any fusion device; Helion has claimed but not demonstrated breeding fraction; dipole breeding is entirely uncharacterized) |

**Subcategory: Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | He3 extraction from D-D fusion ash (T + He3 mixture), isotopic separation (T from He3), tritium decay storage (12.3 year mean lifetime → 17 years for 90% decay to He3), and He3 recycling/reinjection. All systems must operate on orbital platform with <5% fuel loss per cycle for 10 years. |
| Best demonstrated | Terrestrial tritium handling (JET, TFTR) demonstrates T extraction and storage but not for He3 breeding purpose. CANDU reactor He3 recovery from tritium-contaminated heavy water is batch process (decades of T accumulation → single extraction), not continuous breeding loop. Isotopic separation of He3/He4 has been demonstrated (DOE Savannah River Site) but not He3/T separation at fusion relevant purity (99%+ He3). No orbital fuel handling system exists for any fusion concept. |
| Gap ratio | Orbital fuel handling: never demonstrated. He3 extraction from fusion ash: never demonstrated (D-T concepts extract T from Li breeding blanket, not from ash). T→He3 decay loop closure: never demonstrated at >90% efficiency over 10-year plant lifetime. |
| Closure mechanism | Cryogenic distillation for He3/T separation (isotopic mass difference 3:1 enables separation), tritium storage tanks with decay monitoring, He3 purification and reinjection. All systems must be space-qualified (no gravity-driven liquid handling). |
| Classification | **Binary** (mandatory per framework—He3 extraction/purification failure → external He3 purchase required → LCOE-blocking) |
| Evidence tier | **1** (asserted/absent—no He3 breeding loop has been closed in any fusion device; no orbital fuel handling system exists; He3/T separation at fusion scale is undemonstrated) |

**Function-level mean F6**: (1 + 1) / 2 = **1.0**

---

#### Function 7: Power Conversion & BOP

**Subcategory: Physics risk**

| Field | Content |
|-------|---------|
| Plant requirement | 14.7 MeV protons (80% of fusion energy) decelerated to <100 eV kinetic energy via direct energy converter (electrostatic or magnetic), delivering DC electrical power at ≥50% efficiency (proton kinetic energy → DC electricity). |
| Best demonstrated | Venetian blind DEC (1970s experiments) achieved 50-65% efficiency for non-fusion ions at <1 MeV energy. Direct conversion physics is well-understood (Coulomb deceleration in electrostatic potential well). 14.7 MeV protons have ~1.4 mm range in condensed matter (NIST PSTAR), requiring electrostatic potential gradients over ~meter scale for gradual deceleration—geometrically larger than 1970s Venetian blind design (cm-scale electrode gaps). No DEC has been tested with >1 MeV ions. |
| Gap ratio | Particle energy: 15-100× (14.7 MeV requirement / 0.1-1 MeV Venetian blind demonstration). Geometry scaling: 10-100× (meter-scale electrodes required / cm-scale Venetian blind). |
| Closure mechanism | Proponents assume electrostatic deceleration scales to 14.7 MeV with larger electrode spacing and higher voltage gradients (few-MV potentials). Physics is in principle sound (Coulomb force integration), but space-charge effects, secondary electron emission, and plasma breakdown at MV potentials are uncharacterized. Alternative: magnetic divertor DEC (charged particles follow field lines to expansion region, slowing via adiabatic magnetic mirror) eliminates high-voltage electrodes—TRL 2. |
| Classification | **Degrading** (if DEC efficiency falls below 50%, net beaming efficiency drops (already 3.4% baseline) → LCOE rises, but not a binary "zero electricity" failure) |
| Evidence tier | **2** (simulation only—Coulomb deceleration physics is understood, but 14.7 MeV proton DEC has never been demonstrated even at laboratory scale; Venetian blind analogy is extrapolation across 15-100× energy range) |

**Subcategory: Hardware risk**

| Field | Content |
|-------|---------|
| Plant requirement | Phased-array microwave transmitter (2,500 kg, 10 MW RF output, 15% DC-RF efficiency baseline / 50% aspirational non-phased-array) beaming power from LEO to ground rectenna (10×13 km at GEO analogue, scaled to ~1 km² at LEO for 1 MWe). Rectenna (RF-DC conversion at 82% efficiency) feeding AC grid. Full 4-stage chain: DEC → transmitter → beam → rectenna achieving ≥3% net efficiency (baseline) or ≥20% (optimistic). |
| Best demonstrated | Microwave power beaming: 54% DC-DC efficiency demonstrated at 495 W scale (1975 Raytheon Lab, magnetron). MW-scale beaming undemonstrated. Phased-array transmitters for radar (military) achieve 70-80% DC-RF without beam steering, <20% with phased-array steering due to 4-6 dB phase-shifter losses per element (Shinohara 2005). Rectenna: 90% RF-DC efficiency achieved at kW scale (JAXA). Full MW-scale space-to-ground beaming chain: never demonstrated. GEO SPS analogue (NASA NTRS 20140003205) studied but not built. |
| Gap ratio | Power scale: 2,000-20,000× (10 MW requirement / 0.5-5 kW demonstrations). Distance: 10-100× (LEO 500 km / ground demonstrations <10 km). Phased-array at MW scale: never demonstrated. |
| Closure mechanism | Proponents assume phased-array transmitter technology from radar scales to MW power (currently demonstrated at kW scale for space applications). Alternative: laser power beaming (demonstrated at kW scale, claimed 30-50% wall-plug efficiency for high-power lasers) eliminates phased-array phase-shifter losses but introduces atmospheric absorption losses (20-40% depending on weather). Ground rectenna infrastructure ($2M/MWe per SPS analogue) is civil construction (antenna farm + grid tie), not novel technology. |
| Classification | **Degrading** (if transmitter efficiency falls below 10%, net delivered power drops to <0.5 MWe → LCOE rises to $20,000-40,000/MWh, but not a binary "zero electricity" outcome—some power is still delivered) |
| Evidence tier | **2** (simulation + kW-scale demonstrations; no MW-scale space power beaming demonstrated; phased-array at MW scale is unproven; SPS feasibility studies conclude technology is not currently economical) |

**Function-level mean F7**: (2 + 2) / 2 = **2.0**

---

### Heritage Credit Assessment

**Fuel type**: D-He3 (not D-T) → **No heritage credit applies** per framework.

**Heritage lineage check**: Levitated dipole heritage (LDX, RT-1) is experimental physics validation, not reactor-scale demonstration. The framework heritage credit table specifies:
- Tokamak (ITER, JET, EAST) → floor 4.0 for F1-F3 (D-T fuel only)
- Stellarator (W7X, LHD) → floor 4.0 (D-T fuel only)
- Laser IFE (NIF, HYLIFE) → floor 3.5 (D-T fuel only)
- Mirror (MFTF, TMX) → floor 2.5 (D-T fuel only)
- FRC → floor 2.5 (D-T fuel only)

**D-He3 fuel explicitly excludes heritage credit.** The framework states: "Heritage credit only applies to D-T fuel. Alternate fuels get no heritage credit."

**No heritage credit is applied.** F1-F3 scores stand as computed: F1=2.0, F2=2.5, F3=4.5.

---

### Summary of Function-Level Means

| Function | Physics Tier | Hardware Tier | Mean |
|----------|--------------|---------------|------|
| F1: Plasma Performance | 2 | 2 | **2.0** |
| F2: Driver / Energy Input | 3 | 2 | **2.5** |
| F3: Instability Control | 4 | 5 | **4.5** |
| F4: Plasma-Wall Interaction | 3 | 2 | **2.5** |
| F5: Neutron/Particle Handling | 5 | 3 | **4.0** |
| F6: Fuel Cycle Closure | 1 | 1 | **1.0** |
| F7: Power Conversion & BOP | 2 | 2 | **2.0** |

**Binary risks** (from Classification fields):
1. D-He3 plasma ignition failure (F1 physics): zero net electricity if triple product <10²⁰ keV·s·m⁻³ cannot be sustained
2. HTS coil radiation damage or cryocooler failure (F1 hardware): irreversible plant loss (no on-orbit repair capability)
3. He3 self-breeding <100% (F6 physics): external procurement at $30M/kg → LCOE-blocking
4. He3 extraction/purification failure (F6 hardware): external procurement required → LCOE-blocking

**C7 computation (done by Python, not Claude)**: The framework specifies C7 = mean(F1-F7) after heritage credit (none applies here), rounded to nearest 0.5, with function-level cap if any function mean ≤1.5.

C7 = (2.0 + 2.5 + 4.5 + 2.5 + 4.0 + 1.0 + 2.0) / 7 = 18.5 / 7 = **2.64 → rounds to 2.5**

**Function-level cap check**: F6=1.0 is ≤1.5, so C7 is **capped at F6's actual value = 1.0** per framework rule ("if any function mean <= 1.5, C7 is capped at that function's actual value").

**C7 = 1.0** (capped by F6 fuel cycle closure)

---

## YAML Scores Block

```yaml
---
scores:
  C1: 3.0
  C3: 2.9
  C4: 4.0
  C5: 4.3
  C8: 1.3
  F1: 2.0
  F2: 2.5
  F3: 4.5
  F4: 2.5
  F5: 4.0
  F6: 1.0
  F7: 2.0
  binary_risks:
    - "D-He3 triple product <10^20 keV·s·m^-3 prevents ignition (F1 physics)"
    - "HTS coil radiation damage or cryocooler failure causes irreversible plant loss (F1 hardware)"
    - "He3 self-breeding <100% requires external procurement at $30M/kg (F6 physics)"
    - "He3 extraction/purification system failure requires external procurement (F6 hardware)"
---
```
