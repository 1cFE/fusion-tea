---
ID: 15-sheared-flow-stabilized-z-pinch
Concept: Sheared-Flow Z-Pinch (Zap Energy)
Company: Zap Energy
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Most important risk**: Repetition rate scaling — 50× gap between demonstrated (0.2 Hz on Century) and required (10 Hz commercial) operation. At demonstrated rep rate, the 50 MWe module produces only 3.8 MWth, making the economics unworkable. The entire cost thesis depends on high capital utilization through rep rate.
- **Most important advantage**: No superconducting magnets, no lasers, no cryogenics. Eliminates ~40% of tokamak direct capital (CAS22 magnet systems + cryoplant + power supplies) and removes REBCO/Nb₃Sn supply-chain constraints entirely. The 3 m diameter core and 25 m³ volume should deliver dramatically lower building costs than MCF or laser ICF.
- **LCOE ballpark**: 157.5 $/MWh at native scale (50 MWe single module, FOAK), falling to 49.7 $/MWh at 1 GWe NOAK with manufacturing learning and multi-module scale-up. This sits in the middle of the fusion portfolio — better than first-generation tokamaks, worse than mature modular concepts at scale.
- **Confidence verdict**: **Low.** The 50 MWe figure is from a press release with no published derivation. Thermal efficiency (assumed 33–38% for low-temperature LiPb Rankine), recirculating power fraction, and parasitic loads are all analyst inferences. The power balance is a black box. Rep rate extrapolation dominates all uncertainty.

## 2. What Matters Most for LCOE

### 1. Repetition Rate (10 Hz target vs. 0.2 Hz demonstrated)
- **Assumed value**: 10 Hz (19 MJ per pulse → 190 MWth fusion power)
- **Source**: Thompson et al. FST 2023 §III, "variable pulse rate...nominal maximum thermal power of 200 MW"
- **Sensitivity**: Linear with thermal power and revenue. A 5× shortfall (2 Hz instead of 10 Hz) cuts revenue 80%, raising LCOE from 157 $/MWh to ~785 $/MWh at native scale. Century has demonstrated 0.2 Hz — if that were the commercial ceiling, the concept is economically retired.
- **What would flip the conclusion**: Demonstration of sustained 5+ Hz operation with stable plasma parameters and cathode survival. Below 5 Hz, the economics likely fail even with optimistic cost assumptions.

### 2. Thermal Efficiency (assumed 33–38%, not published)
- **Assumed value**: 35% (midpoint for subcritical steam Rankine from ~600 K LiPb)
- **Source**: Analyst estimate based on standard thermodynamic cycles at this source temperature
- **Sensitivity**: Medium. A 10-point drop (35% → 25%) increases recirculating power fraction and cuts net output from 50 MWe to ~30 MWe, raising LCOE ~65%. A 10-point gain (35% → 45%) would require supercritical CO₂ or higher LiPb temperatures, neither of which are proposed.
- **What would flip the conclusion**: Published thermal-hydraulic analysis showing either (a) LiPb outlet temperatures enabling supercritical cycles (>45% efficiency), or (b) confirmation that steam Rankine at 600 K delivers <30% efficiency, which would make the 50 MWe claim implausible.

### 3. Pulsed Power Driver Cost (capacitor bank, not quantified)
- **Assumed value**: Library default for pulsed-electrical-drive archetype (no override)
- **Source**: None. Curry et al. LLNL-JRNL-2001600 (2025) reports 125–250 years to build 150 plants' worth of capacitors at current manufacturing capacity, and 4–6 year delivery per order, but no Zap-specific unit cost.
- **Sensitivity**: Likely high. The pulsed power system is analogous to the magnet system in a tokamak — a capital-intensive, long-lead-time subsystem. If capacitor costs at 10⁹-shot lifetimes are 2× the library assumption, overnight capital rises ~20–30% (estimate based on typical pulsed-driver share in MIF concepts).
- **What would flip the conclusion**: Published bill of materials showing either (a) capacitor count <10,000 per 50 MWe module due to voltage efficiency (50–200 kV is much lower than Z-machine's 5–10 MV), or (b) capacitor costs >$500/unit at volume with 10⁹-shot specs, which would materially raise capital cost.

### 4. Cathode Lifetime (not published, high-duty-cycle erosion + neutron damage)
- **Assumed value**: No lifetime estimate exists. Remote replacement is described as "straightforward" due to "simple geometry."
- **Source**: Thompson et al. FST 2023 §V (qualitative claim only)
- **Sensitivity**: High for O&M costs. If cathode replacement is required every 10⁶ shots (28 hours at 10 Hz), annual replacement cost could dominate CAS70. If cathodes last 10⁹ shots (3+ years), replacement becomes infrequent capital refresh.
- **What would flip the conclusion**: Demonstration of >10⁸-shot cathode survival under neutron flux and megaampere currents, or published cathode material specification with neutronics-validated damage model showing multi-year lifetimes.

### 5. TBR Margin (1.1 from "initial calculations")
- **Assumed value**: TBR ≈ 1.1 (Forbes et al. FST 2019, cited in Thompson 2023)
- **Source**: "Initial calculations" — no Monte Carlo neutronics or detailed geometry published
- **Sensitivity**: Medium for fuel cost and tritium availability. A TBR of 1.1 is marginal — most D-T designs target ≥1.15 to account for processing losses and inventory buildup. If detailed neutronics shows TBR <1.05, the concept requires external tritium supply, adding fuel cost and supply-chain risk.
- **What would flip the conclusion**: Monte Carlo neutronics showing TBR <1.05 would force reliance on external tritium (uneconomic at scale). TBR >1.2 would provide comfortable margin and possible tritium export revenue.

## 3. Risk Verdicts

### Rep Rate Scaling from 0.2 Hz to 10 Hz (50× gap)
- **Verdict**: Genuinely uncertain (45% likely resolvable, 55% unlikely)
- **Rationale**: Century's 1,000+ consecutive shots at 0.2 Hz show pulsed stability, but the gap to 10 Hz involves cathode erosion rates, capacitor recharge time, LiPb flow stability, and thermal transient management — none of which are characterized at >1 Hz. No analogue system operates at this combination of parameters (megaampere plasma currents, 10 Hz, neutron environment).
- **What would retire this risk**: FuZE-A or a follow-on device demonstrating sustained (>1 hour) operation at ≥5 Hz with stable neutron yield and cathode survival, plus publication of capacitor recharge architecture proving 10 Hz is physically achievable with the solid-state thyristor stack design.

### Cathode Survival Under Reactor Conditions
- **Verdict**: Unlikely resolvable without major R&D (35% likely resolvable)
- **Rationale**: The cathode is unprotected by the LiPb blanket and sees full neutron flux at the plasma boundary. Arc smelting furnace analogy (60 MW, no neutrons) is weak. No cathode material candidate is named. Graphite (standard for arc furnaces) has poor neutron damage resistance; refractory metals (tungsten, molybdenum) have high sputtering under plasma bombardment. Remote replacement may be "straightforward" but if required every 10⁵–10⁶ shots, it becomes a chronic availability and cost burden.
- **What would retire this risk**: Publication of cathode material specification with neutronics damage modeling showing >10⁸-shot lifetime, plus Century demonstration of cathode replacement in <8 hours with remote tooling (to meet 85%+ availability target).

### Confinement Scaling to 1.2–1.5 MA at 200 μs (from FuZE's 0.25–0.3 MA at ~1 μs)
- **Verdict**: Likely resolvable (65% likely)
- **Rationale**: The APS DPP 2025 abstract explicitly states Zap is "seeking to complete the physics basis" and "determine the scaling laws" — this is still open research. However, FuZE-3's gigapascal pressures and the three-electrode architecture for independent acceleration/compression control are encouraging. The pinch current requirement (1.2–1.5 MA) is not exotic by pulsed-power standards (Z machine operates at 20+ MA). The question is whether sheared-flow stabilization holds at these currents with fusion-relevant temperatures and confinement times.
- **What would retire this risk**: FuZE-A achieving pinch currents ≥0.8 MA with confinement times >50 μs and thermonuclear neutron yield >10¹³ n/pulse, plus peer-reviewed publication of scaling law validation showing linear or better-than-linear confinement time scaling with current.

### Pulsed Thermal Coupling to Steam Rankine Cycle
- **Verdict**: Likely resolvable (75% likely)
- **Rationale**: This is an engineering challenge, not a physics risk. LiPb blanket has high thermal mass (~235 tonnes at 9,400 kg/m³ × 25 m³), smoothing 19 MJ pulses at 10 Hz into quasi-steady heat flux. The individual pulse energy (19 MJ) is orders of magnitude lower than laser ICF (hundreds of MJ to GJ), making thermal smoothing easier. Steam Rankine cycles tolerate some load variation.
- **What would retire this risk**: Thermal-hydraulic simulation of LiPb temperature transients showing outlet temperature variation <10 K peak-to-trough at 10 Hz, or Century demonstration of stable heat extraction from pulsed source (even at 0.2 Hz with surrogate liquid metal).

### TBR Achieving ≥1.1 with LiPb Weir-Wall Geometry
- **Verdict**: Likely resolvable (70% likely)
- **Rationale**: LiPb is a proven breeder material with excellent neutron multiplication from lead. The thick blanket (~1 m+) provides ample breeding volume. The weir-wall flow geometry introduces uncertainty (neutron streaming through gaps, flow voids reducing effective density), but these are addressable with detailed design. "Initial calculations" showing TBR ≈ 1.1 are credible as a first estimate.
- **What would retire this risk**: Monte Carlo neutronics (MCNP/Serpent) with realistic 3D weir-wall flow geometry showing TBR ≥1.05 with 95% confidence, accounting for structural penetrations, flow voids, and cathode penetration.

## 4. Structural Advantages and Disadvantages

### Advantages vs. D-T Tokamak Baseline

**Eliminates ~40% of direct capital (CAS22 magnet systems)**
- No superconducting magnets → no REBCO tape at $40–100/m, no Nb₃Sn, no NbTi
- No cryoplant → no 4 K helium systems, no nitrogen pre-cooling, no compressor infrastructure
- No magnet power supplies → no AC/DC converters for coil current control
- Estimated capital savings: tokamak CAS22 magnets typically represent 30–40% of direct capital; SFS Z-pinch CAS22 (blanket + pulsed power) is 17.6% of overnight capital at native scale (93.4 M$ of 532.3 M$ total CAS10-90)

**Compact core reduces building costs (CAS21)**
- 3 m diameter, 25 m³ core volume vs. tokamak reactor buildings sized for 10–15 m diameter vacuum vessels
- Model output: CAS21 = 199.9 M$ at native scale (37.6% of capital) — this is still high due to single-module inefficiency. At 1 GWe NOAK, CAS21 rises to 760.8 M$ (18.2% of capital), showing building costs scale favorably with multi-module plants.

**No precision optics or laser infrastructure**
- Eliminates laser ICF's CAS22 driver complexity (frequency conversion, beam transport, final optics, target positioning)

**No manufactured targets**
- Plasma forms from gas injection (no target factory, no cryogenic D-T shells, no ablator material supply chain)

### Disadvantages vs. D-T Tokamak Baseline

**Pulsed power driver is capital-intensive with long lead times**
- Capacitor supply-chain constraint: 125–250 years to build 150 plants' worth at current manufacturing capacity (Curry et al. 2025)
- 4–6 year delivery per capacitor order
- Component lifetime requirements: 10⁶–10⁹ shots (current state of art is ~10⁴ shots) — 2–6 orders of magnitude improvement needed
- This partially offsets the magnet cost savings. The net capital advantage depends on whether capacitor costs at 10⁹-shot specs are lower than superconducting magnet costs — not yet quantified.

**Low thermal efficiency limits revenue per unit fusion power**
- LiPb outlet temperature ~600 K → subcritical steam Rankine at 33–38% efficiency
- Tokamaks with helium-cooled blankets at 800–900 K can achieve 40–45% efficiency with supercritical CO₂ or advanced steam cycles
- Revenue penalty: at 35% vs. 42% thermal efficiency, a tokamak generates 20% more revenue from the same fusion power, improving LCOE proportionally

**Cathode replacement is a recurring availability and cost burden**
- No tokamak analogue — tokamak first walls are protected by divertors and replaced on multi-year schedules
- If cathode replacement is required every 10⁶ shots (28 hours at 10 Hz), availability could fall to 70–80% unless replacement time is <4 hours
- Remote handling costs (CAS22 C220110 = 20.5 M$ at native scale) may reflect this, but without published replacement schedules, O&M risk is unquantified

**Rep rate extrapolation is a unique engineering risk**
- Tokamaks operate quasi-steady (no rep rate scaling risk)
- The 50× gap from demonstrated (0.2 Hz) to required (10 Hz) is a concept-specific risk with no mature analogue

### Net Structural Position

At demonstrated rep rate (0.2 Hz): **Worse than tokamak.** Capital savings from no magnets are overwhelmed by thermal power shortfall.

At commercial rep rate (10 Hz): **Potentially better than tokamak at NOAK scale, worse at FOAK scale.** The model projects 49.7 $/MWh at 1 GWe NOAK — competitive with advanced tokamaks if rep rate and cathode lifetime risks are resolved. But at native scale (157.5 $/MWh), the small module size and single-unit learning curve leave it uncompetitive with FOAK tokamaks (~80–120 $/MWh for mature designs).

## 5. Cross-Concept Positioning

**Nearest neighbors by architecture:**
- **MagLIF (Pacific Fusion)**: Shares pulsed-power driver and liquid-wall concept, but operates at opposite end of the pulse-energy / rep-rate tradeoff. MagLIF uses GJ-class pulses at ~1 Hz from Z-machine-class drivers (60+ MA); SFS Z-pinch uses 19 MJ pulses at 10 Hz from much smaller drivers (1.2–1.5 MA). MagLIF bets on high energy gain per shot to amortize driver cost; Z-pinch bets on high capital utilization through rep rate.
- **General Fusion (MTF Pneumatic Compression)**: Shares liquid-metal wall and pulsed operation, but uses mechanical compression of a magnetized plasma rather than electrical current. SFS Z-pinch eliminates the mechanical compression system entirely (no pistons, no pneumatic actuators).

**Nearest neighbors by scale:**
- **Small modular concepts (50–200 MWe native scale)**: HB11 (p-¹¹B aneutronic, no published LCOE), Type One Energy (planar-coil stellarator, 50 MWe modules). These share the multi-module plant architecture thesis — FOAK economics are poor due to learning-curve and fixed-cost allocation, but NOAK economics at GWe scale benefit from manufacturing learning and infrastructure sharing.

**Differentiation:**
- **Only self-confined pulsed MFE concept in the portfolio.** No external magnets, no laser, no mechanical compression.
- **Lowest voltage pulsed-power system (50–200 kV).** Simpler switch and capacitor specs than Z-machine-class (5–10 MV) or laser drivers (kilojoule-scale capacitor banks at 20–30 kV but with complex laser chains).
- **Rep rate dominates economics more than any other pulsed concept.** MagLIF and laser ICF amortize driver cost over high yield per pulse; Z-pinch amortizes small driver cost over high rep rate. If rep rate fails to scale, the concept is economically retired. No other concept has this binary dependency.

**Where it sits in the LCOE landscape (model projection):**
- **At native scale (50 MWe FOAK)**: 157.5 $/MWh — middle of the pack, worse than mature tokamak designs (80–120 $/MWh), better than exotic concepts without cost data.
- **At 1 GWe NOAK**: 49.7 $/MWh — competitive with advanced tokamaks and modular concepts at scale, assuming rep rate and cathode lifetime risks are resolved.

The concept's economic viability depends on (a) whether 10 Hz is achievable, and (b) whether multi-module plants can share pulsed-power infrastructure or if each module requires a dedicated capacitor bank. The model assumes favorable scaling; if modules cannot share infrastructure, NOAK LCOE could rise 30–50%.

## 6. Modeling Confidence

**Rating: Low**

**Data-anchored parameters (high confidence):**
- Pinch current: 1.2–1.5 MA (simulation-based but within pulsed-power state of art)
- Pinch geometry: 0.15 mm radius × 0.5 m length (published in peer-reviewed paper)
- Fusion energy per pulse: 19 MJ (simulation-based, consistent with Q > 10 at stated parameters)
- Repetition rate target: 10 Hz (published, though not demonstrated)
- Core volume: 25 m³ (published)
- Blanket material: LiPb eutectic (published)

**Speculative or analyst-inferred parameters (low confidence):**
- **Net electric output (50 MWe)**: From press release, no published derivation. Implied thermal efficiency of ~25% (50 MWe / 200 MWth) is plausible but unverified.
- **Thermal efficiency (33–38%)**: Analyst estimate based on standard Rankine cycles at assumed LiPb temperature (~600 K). No published LiPb inlet/outlet temperatures or cycle specification.
- **Recirculating power fraction**: Derived from published drive efficiency (~70%) but no published breakdown of pulsed-power recharge vs. parasitic loads (pumping, vacuum, tritium processing).
- **Cathode lifetime**: No data. Replacement frequency is unknown.
- **Pulsed power system cost**: Library default (no company-grounded figure). Capacitor count, stored energy, and unit cost at 10⁹-shot specs are unquantified.
- **TBR (1.1)**: From "initial calculations" (Forbes et al. 2019), not detailed neutronics. Geometry of weir-wall flow is idealized.

**Dominant source of LCOE uncertainty:**
Repetition rate achievability. The model assumes 10 Hz is feasible. If commercial operation is limited to 2–5 Hz due to cathode erosion, capacitor recharge, or plasma stability limits, LCOE rises by a factor of 2–5×. This is a binary risk — the concept either achieves high rep rate and becomes economically competitive, or it doesn't and is retired.

Secondary uncertainties (thermal efficiency, cathode lifetime, pulsed-power cost) are important but do not individually determine economic viability. Rep rate is the single make-or-break parameter.

## 7. What Would Change My Mind

### Evidence that would improve LCOE estimate (make me more optimistic):

**Demonstration of sustained 5+ Hz operation with stable plasma parameters**
- If FuZE-A or Century achieves ≥5 Hz for >1 hour continuous operation with neutron yield variance <20% pulse-to-pulse, it proves the concept is not fundamentally limited by cathode erosion or capacitor recharge. LCOE confidence would rise from Low to Medium, and the 10 Hz target becomes credible.
- Impact: Would validate the central cost thesis (high capital utilization through rep rate). LCOE estimate would hold or improve.

**Published thermal-hydraulic analysis showing thermal efficiency ≥40%**
- If LiPb outlet temperatures are higher than assumed (~800 K instead of 600 K) or a supercritical CO₂ cycle is feasible with the weir-wall blanket, thermal efficiency could reach 40–45%. This would raise net electric output from 50 MWe to ~60–65 MWe at the same fusion power, dropping LCOE ~20%.
- Impact: Would close the efficiency gap with tokamaks and strengthen revenue per unit capital.

**Capacitor supply-chain investment demonstrating 10⁹-shot components at <$200/unit**
- If pulsed-power manufacturers achieve 10⁹-shot lifetimes (currently ~10⁴) and volume production drives unit costs below $200 (vs. current ~$500–1,000 for high-reliability units), pulsed-power capital cost could fall 50–70%. This would drop overnight capital ~15–20%, improving LCOE proportionally.
- Impact: Would confirm the "no magnets = lower capital" thesis holds even accounting for pulsed-power costs.

### Evidence that would worsen LCOE estimate (make me more pessimistic):

**Experimental data showing rep rate ceiling at <5 Hz due to cathode erosion**
- If Century or FuZE-A testing shows cathode damage rates require replacement every 10⁵ shots (2.8 hours at 10 Hz), sustained operation above 2–3 Hz becomes uneconomic due to availability loss. LCOE at 3 Hz would rise to ~525 $/MWh (10/3 × 157.5 $/MWh).
- Impact: Would retire the concept economically unless a breakthrough cathode material is found.

**Monte Carlo neutronics showing TBR <1.05 with realistic weir-wall geometry**
- If detailed neutronics accounting for flow voids, structural penetrations, and cathode gap shows TBR <1.05, the concept requires external tritium supply. At 50 MWe native scale, tritium availability becomes a bottleneck. LCOE impact is moderate (+10–15% due to fuel cost) but supply-chain risk becomes severe.
- Impact: Would force redesign of blanket geometry or acceptance of tritium dependency, adding cost and risk.

**Published power balance showing net electric output <35 MWe at 200 MWth**
- If the actual recirculating power fraction is higher than modeled (e.g., due to underestimated parasitic loads for vacuum, tritium processing, or LiPb pumping), net output could fall from 50 MWe to 30–35 MWe. This would raise native-scale LCOE from 157.5 $/MWh to ~225–260 $/MWh.
- Impact: Would confirm the low thermal efficiency penalty is more severe than assumed, making the concept uncompetitive at native scale even if rep rate is achieved.
