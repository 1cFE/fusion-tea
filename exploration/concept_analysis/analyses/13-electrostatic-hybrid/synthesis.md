---
ID: 13-electrostatic-hybrid
Concept: Electrostatic Hybrid (D-T)
Company: Avalanche Energy
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Most critical risk**: Coulomb collision thermalization has not been experimentally disproven. The Lampe-Mannheimer critique (1998) claims loss rates 25–37× fusion rates at required densities. Avalanche's counter-argument is simulation-only. If this barrier is real, the concept cannot achieve Q>1 regardless of engineering optimizations.

- **Most important advantage**: Eliminates ~70% of D-T tokamak direct capital by avoiding large superconducting magnets, breeding blankets, and plasma heating infrastructure. The cost structure is fundamentally different—dominant accounts shift to HV power supplies and per-module shielding, both potentially mass-manufacturable at scale.

- **LCOE ballpark**: At the baseline model parameters (Q=10, η=12%, 1000 modules, FOAK), LCOE is **$302k/MWh** with specific capital of **$8.8M/kWe**—six orders of magnitude above commercial viability. The turbine-array scenario (Q=10, η=30%) yields **$13k/MWh** at **$380k/kWe**—still 100× too expensive. Even the most optimistic NOAK case (Q=20, η=30%, 10,000 modules, mass-manufactured) reaches only **$4.8k/MWh** at **$107k/kWe**. The model finds no parameter combination yielding LCOE ≤ $100/MWh within physically plausible Q ranges (Q ≤ 30).

- **Confidence verdict**: **Low**. The concept has not demonstrated Q>1, the space-charge mitigation physics is unverified experimentally, no plant architecture exists, and the energy conversion pathway at kWe scale is undefined. LCOE estimates rest on four sequential unproven steps: (1) experimental validation of Q>1, (2) thermal conversion pathway at <1 MWe scale, (3) modular plant architecture with practical neutron shielding, and (4) cost reduction through mass manufacturing. Any single step failing eliminates commercial viability.

## 2. What Matters Most for LCOE

The model output reveals three parameters that determine whether the Orbitron can ever achieve commercial LCOE. Unlike mature concepts where cost uncertainty dominates, here **physics feasibility** gates the entire economic case.

### **1. Q_engineering (assumed: 10; required: >30 for viability)**
**Sensitivity magnitude**: At Q=10, LCOE = $302k/MWh. At Q=12, LCOE = $78k/MWh (4× reduction). At Q=20, LCOE = $23k/MWh. At Q=30, LCOE = $14k/MWh. The LCOE surface shows that even at Q=30 with optimistic NOAK capital ($30k/module cathode cost), the concept barely approaches **$11k/MWh**—still 100× too expensive.

**Source**: No Q value has been measured. The CWFest 2023 target of 1 kW fusion from 1 kW input corresponds to Q≈1 at *best*. The model's baseline Q=10 is aspirational—it represents the minimum thermoelectric break-even (Q≈8.3 for η=12%) plus a small margin. The concept has never operated above Q=0.

**What would flip the conclusion**: If experimental results demonstrate Q>30 with the space-charge-mitigated density regime that simulations predict, *and* if a turbine-array architecture at >1 MWe aggregate scale proves feasible (η=30%), the LCOE surface shows potential descent toward $3–5k/MWh in the NOAK limit. This is still 30–50× too expensive, but it moves from "physically impossible" to "economically implausible." Conversely, if Coulomb collision physics limits achievable Q to <5—consistent with the 1998 critique—net power generation becomes impossible regardless of capital cost reductions.

---

### **2. Thermal efficiency (assumed: 12%; turbine scenario: 30%)**
**Sensitivity magnitude**: Thermal efficiency determines the break-even Q threshold. At η=12% (thermoelectric), break-even is Q≈8.3; at η=30% (turbine array), break-even is Q≈3.3. The difference compounds exponentially with capital cost per kWe: at Q=10, moving from η=12% to η=30% reduces LCOE from $302k/MWh to $13k/MWh—a **23× improvement**. This is the single largest LCOE lever in the model.

**Source**: The company states "thermal cycle with turbines" (Orbitron product page), but this is thermodynamically implausible at 1–100 kWe per module. Commercial steam turbines operate at hundreds of MWe minimum; sCO₂ cycles reach ~30% efficiency only above ~10 MWe. At 1 kWe module scale, thermoelectric conversion (η=5–15%) is the only practical option. The baseline η=12% reflects optimistic thermoelectric performance. The η=30% scenario requires a megawatt-aggregate plant architecture stacking thousands of modules with shared turbine infrastructure—a design that has never been disclosed.

**What would flip the conclusion**: Development of a practical thermal conversion pathway at kWe scale with η>20% would fundamentally change the economics. Alternatively, a validated plant architecture demonstrating >1 MWe aggregate thermal output with conventional turbine conversion (η≈30%) would enable the more favorable LCOE surface shown in the model's turbine-array scenarios. Without this, the concept remains trapped in the thermoelectric regime where even Q=30 yields LCOE in the $10–20k/MWh range.

---

### **3. Cathode/module capital cost (baseline: $100k/module; range: $30k–250k)**
**Sensitivity magnitude**: The back-solve LCOE surface shows that at Q=20, η=12%, varying cathode cost from $30k (optimistic NOAK) to $250k (pessimistic FOAK) shifts LCOE from $17k/MWh to $34k/MWh—a **2× swing**. At lower Q values near break-even, the capital cost sensitivity is weaker because recirculating power and tritium fuel costs dominate. The model uses $100k/module as the FOAK baseline (primary accounts: $100k cathode assembly + $50k HV supply + $50k HTS magnets + $80k vacuum system + $5.7k shielding).

**Source**: No cost data exists. The $100k baseline is analogized from industrial HV equipment: sustained 300 kV power supplies for particle accelerators cost ~$200–500/kW_input, but at 1 kWe input scale, a minimum $50k floor applies (you cannot buy a 300 kV sustained supply for less than ~$50k regardless of power rating). The cathode/vacuum assembly ($100k) reflects precision HV vacuum hardware with the proprietary feedthrough Avalanche describes as their "key innovation." The optimistic $30k scenario assumes mass manufacturing learning curves analogous to consumer-electronic HV systems; the pessimistic $250k scenario reflects conservative FOAK estimates for novel neutron-exposed HV components.

**What would flip the conclusion**: Capital cost becomes decisive only if Q and η are simultaneously favorable. If the concept achieves Q=20 and validates a turbine-array architecture (η=30%), the specific capital at $100k/module cathode cost is **$149k/kWe** yielding LCOE = $6k/MWh. Reducing cathode cost to $30k (NOAK learning) brings this down to $4.6k/MWh at the same Q and η. This is still **46× too expensive** for commercial electricity, but it demonstrates that capital cost is a second-order effect compared to Q and η. The model reveals the harsh truth: even with heroic cost reduction (10× learning from FOAK to NOAK), the concept remains structurally non-viable unless Q and η both exceed their current best-case projections.

---

**LCOE elasticity summary** (from baseline Q=10, η=12%, $100k/module):
- **Q: +20% → LCOE –36%** (Q=10→12 reduces LCOE from $302k to $78k/MWh)
- **η: +150% → LCOE –96%** (η=12%→30% reduces LCOE from $302k to $13k/MWh)
- **Cathode cost: –70% → LCOE –28%** ($100k→$30k reduces LCOE from $302k to $217k/MWh at Q=10, η=12%)

Thermal efficiency is the dominant lever, but it is gated by plant architecture (undefined). Q is the second-most sensitive parameter and is gated by unresolved Coulomb collision physics. Capital cost is tertiary—it matters only after the physics and architecture barriers are resolved.

## 3. Risk Verdicts

### **Coulomb collision thermalization dominates fusion rate → Q<1 ceiling**
**Verdict**: **Genuinely uncertain** — but evidence leans toward "unlikely resolvable."

**Rationale**: The 1998 Lampe-Mannheimer analysis claims Coulomb collision rates exceed fusion rates by 25–37× at densities required for net energy gain. Avalanche's counter-argument (CWFest 2023 blog) states that PIC simulations use ion density scaling that makes thermalization "appear worse than it is," but this is a claim about simulation methodology—not experimental disproof. The AIP Advances (2024) paper confirms that space-charge-mitigated ion densities above 10¹⁰ cm⁻³ are "the focus of initial experiments"—meaning they have *not yet been demonstrated*. The physics claim is simulation-only.

**What would retire this risk**: Experimental measurement of Coulomb collision loss rates in an operating Orbitron at fusion-relevant ion densities (>10¹⁰ cm⁻³) with simultaneous neutron yield characterization. If the measured loss rate is ≤ fusion rate, the barrier is retired. If the measured loss rate confirms the 25–37× ratio, the concept is definitively non-viable for D-T power generation. Publication of full experimental data from the two paywalled peer-reviewed papers (AIP Advances 2024, Physics of Plasmas 2025) would partially address this—but only if those papers report measured collision rates, not just simulated ones.

---

### **Energy conversion at 1–100 kWe scale with reasonable efficiency**
**Verdict**: **Unlikely resolvable** at claimed module scale; **likely resolvable** at megawatt-aggregate plant scale.

**Rationale**: The company's statement that energy will be "converted with a thermal cycle, utilizing turbines" is thermodynamically implausible at 1–100 kWe per module. Steam turbines achieve ~30% efficiency only at scales >10 MWe; Stirling engines and ORCs can operate at kWe scale but with η=10–20% at best. Thermoelectric conversion at 1 kWe yields η≈5–12%. At η=12% (optimistic thermoelectric), the baseline Q=10 scenario produces LCOE = $302k/MWh—six orders of magnitude above commercial viability. At η=30% (turbine array), the *same* Q=10 yields LCOE = $13k/MWh—a 23× improvement. The company likely envisions stacking thousands of modules to reach megawatt aggregate thermal output feeding conventional turbines, but no such plant architecture has been disclosed.

**What would retire this risk**: Publication of a multi-module plant architecture showing how >1 MWe aggregate thermal output is collected from a distributed array of kWe-scale modules, integrated with turbine-based conversion. The engineering challenges are significant (thermal coupling between modules, neutron shielding geometry for dense arrays, per-module reliability vs. plant availability) but not fundamental. If this architecture is validated, η=30% becomes plausible and the LCOE surface shifts from $300k/MWh to $13k/MWh at Q=10—still economically non-viable, but *physically* coherent. Alternatively, a breakthrough in small-scale thermoelectric or thermionic conversion achieving η>20% at <1 MWe would retire the risk without requiring plant architecture changes, but this seems less likely given mature state-of-art performance.

---

### **Tritium breeding at compact device scale**
**Verdict**: **Unlikely resolvable** without major geometric redesign—but **not blocking** for near-term neutron source application.

**Rationale**: The Orbitron's desktop form factor (10 cm radius × 20 cm length per module) provides negligible space for a breeding blanket. A lithium-bearing blanket thick enough to achieve TBR≥1.0 requires ~40 cm of FLiBe or Li-Pb—larger than the entire device. The April 2025 MoU with Fusion Fuel Cycles (FFC) covering "tritium breeding blankets and D-T fuel cycle systems" is a disclosed collaboration direction, but no blanket design, timeline, or technical specification has been published. For the near-term FusionWERX neutron source application, purchased tritium at $35k/g is acceptable—neutron production is the revenue product, not electricity. For a power reactor, purchased tritium at Q=10 contributes **$57k/MWh** (19% of total $302k/MWh LCOE), scaling inversely with Q. At Q approaching break-even, tritium cost per MWh diverges to infinity regardless of capital cost.

**What would retire this risk**: A disclosed breeding blanket design with credible TBR≥1.0 geometry integrated with the Orbitron module. The compact scale makes this geometrically challenging—likely requiring either (a) a shift to larger device geometry (contradicting the modular mass-manufacturing advantage), or (b) an external blanket surrounding a dense module array (introducing neutron shielding complexity and thermal coupling challenges), or (c) operation with D-D fuel (eliminating tritium breeding requirement but reducing fusion cross-section by 100×, making Q>1 even harder). Absent a breeding solution, the concept remains dependent on purchased tritium, capping commercial viability at Q values where tritium cost is <10% of LCOE—roughly Q>15 at η=30%.

---

### **Neutron shielding for stacked multi-module plants does not dominate cost/volume**
**Verdict**: **Likely resolvable**—but current "concrete castle" approach is economically self-defeating.

**Rationale**: The CWFest 2023 blog describes a "concrete castle" surrounding the Marty prototype. If each 1–100 kWe module requires a dedicated concrete shield at $15k/m³ (baseline model assumption), the shield volume per module (~0.37 m³) adds $5.7k/module—small compared to $100k cathode cost, but the *volume* penalty is severe. At 1000 modules with individual shielding, the plant footprint becomes dominated by concrete rather than fusion cores, negating the modular compactness advantage. The model's shielding sensitivity sweep shows that varying shielding cost from $2k/m³ to $500k/m³ changes baseline LCOE from $299k/MWh to $385k/MWh—a ±15% swing, significant but not dominant.

**What would retire this risk**: A disclosed multi-module plant architecture demonstrating shared neutron shielding (e.g., modules grouped in a common shielded vault with distributed cooling/power extraction). This would reduce shielding volume per module by 5–10× and shift shielding from a per-module CAPEX to a plant-level account (CAS22 plant-wide), improving LCOE by ~10–15%. The engineering is mature (fission reactor shielding, neutron source facilities), so this risk is "likely resolvable" given competent plant design—but that design does not yet exist.

---

### **Cathode and HV feedthrough lifetime under 14 MeV neutron bombardment**
**Verdict**: **Genuinely uncertain**—no experimental data exists, but analogues suggest short lifetimes.

**Rationale**: The cathode operates at 300 kV sustained in direct line-of-sight to a D-T fusion plasma producing 14 MeV neutrons. Neutron-induced displacement damage to tungsten cathodes is well-characterized in fission (where 1 MeV neutrons dominate) but poorly understood at 14 MeV. The HV feedthrough's ceramic insulator will experience cumulative radiation damage, reducing dielectric strength over time. The model assumes 2 FPY cathode lifetime (conservative vs. tokamak first-wall but aggressive given direct particle bombardment geometry). At 2 FPY, the baseline scenario requires **12 cathode replacements** over 30 years, contributing $39M/yr annualized cost (22% of total O&M). Halving cathode lifetime to 1 FPY raises LCOE from $302k/MWh to $377k/MWh (+25%). Extending to 5 FPY reduces LCOE to $258k/MWh (–15%).

**What would retire this risk**: Dedicated irradiation testing of Orbitron cathode and HV feedthrough materials under 14 MeV neutron fluence at operating voltage. This is not expensive—neutron source facilities (e.g., FusionWERX itself once operational) can provide the test environment. If measured lifetimes are ≥5 FPY, the O&M cost contribution is manageable. If measured lifetimes are <1 FPY, frequent cathode replacement becomes an LCOE-dominant cost driver, potentially adding $100–200/MWh even in the optimistic Q=20, η=30% scenario. The gap report flags this as a "truly-unknown" gap with no fission analog—correct, and this warrants high-priority experimental characterization before commercial projections are credible.

## 4. Structural Advantages and Disadvantages

The Orbitron's cost structure diverges categorically from the D-T tokamak baseline. It does not shift costs—it **eliminates entire CAS accounts** and introduces novel ones. Quantifying these deltas against a reference tokamak (e.g., 01-HTS-Compact-Tokamak) reveals where the concept's economic case lives or dies.

### **Eliminated accounts (savings vs. tokamak baseline)**

| CAS Account | Tokamak Reference | Orbitron | Delta | Notes |
|-------------|-------------------|----------|-------|-------|
| **C220103: Magnets** | ~$400M (30% of CAS22) | $50M (0.5 T HTS pair, 1000 modules) | **–88%** | Dominant tokamak cost eliminated; 0.5 T HTS at $50k/module vs. 5–20 T large-bore REBCO at $200–500M |
| **C220101: Breeding Blanket** | ~$300M (20% of CAS22) | $20M (chamber wall only, no blanket) | **–93%** | No FLiBe, no beryllium, no breeding infrastructure; tritium purchased as OPEX instead |
| **C220104: Plasma Heating** | ~$150M (10% of CAS22) | $0 (replaced by HV supply in C220107) | **–100%** | No RF, no NBI; electrostatic acceleration via cathode voltage |
| **CAS27: Special Materials** | ~$100M (FLiBe, beryllium, REBCO tape) | $0.04M (minimal) | **–100%** | No scarce materials; tungsten cathodes and stainless vacuum components are commodity |

**Aggregate saving**: ~$850M eliminated from a $1.2B tokamak CAS22 baseline → **~70% direct capital reduction** in reactor plant equipment. This is the concept's *single largest structural advantage*. If the Orbitron achieves Q>1, it does so with a fundamentally cheaper device architecture than any mainstream MFE concept.

---

### **Novel accounts (costs added vs. tokamak baseline)**

| CAS Account | Tokamak Reference | Orbitron | Delta | Notes |
|-------------|-------------------|----------|-------|-------|
| **C220107: HV Power Supply** | $0 (no HV in tokamak) | $50M ($50k/module × 1000, FOAK floor) | **+$50M** | Novel dominant account; 300 kV sustained supply + ion gun array replaces plasma heating |
| **C220102: Neutron Shield** | $80M (shared toroidal shield) | $5.7M (per-module at $15k/m³) | **–93%** at 1000 modules | BUT: scales linearly with module count; 10,000 modules → $57M, eliminating the savings |
| **C220105: Cathode Assembly** | $150M (vacuum vessel + first wall) | $100M ($100k/module × 1000) | **–33%** | Smaller device but higher $/kWe; novel neutron-exposed HV geometry may drive FOAK cost up |
| **CAS80: Tritium Fuel (OPEX)** | ~$5M/yr (self-breeding, makeup only) | $33M/yr (purchased, no breeding) | **+$28M/yr** | Permanent OPEX penalty; at Q=10, tritium cost contributes $57k/MWh (19% of LCOE) |

**Aggregate addition**: +$50M novel CAPEX (HV supply) + $28M/yr OPEX penalty (purchased tritium). The HV supply cost is manageable at $50M (6% of total capital in the baseline model). The tritium OPEX is LCOE-impacting at low Q but scales favorably (∝1/Q); at Q=20, tritium cost drops to ~$20M/yr (~$15k/MWh contribution).

---

### **Net structural position**

At Q=10, η=12%, 1000 modules, FOAK:
- **Overnight capital**: $610M (vs. ~$2B tokamak reference) → **–70% total capital**
- **Specific capital**: $8.8M/kWe (vs. ~$5k/kWe tokamak) → **+1760× per-kWe cost**

The paradox: the Orbitron is *cheaper in absolute dollars* but *catastrophically more expensive per kWe* because net power is only 80 kWe (0.08 MW) at the baseline operating point. The recirculating power fraction is **93%**—nearly all gross electric output is consumed by input power and auxiliaries. This is the fundamental economic barrier: even with 70% capital cost reduction vs. tokamaks, the Orbitron at Q=10, η=12% produces so little net power that $/kWe explodes to $8.8M—commercially meaningless.

The structural advantage is *real* but *latent*. It materializes only if:
1. Q increases to ≥20 (reducing recirculating fraction from 93% to ~70%)
2. η increases to ≥30% (requiring turbine-array plant architecture)
3. Module count scales to 10,000+ (amortizing plant-wide BOP over larger output)

Under those conditions, the model shows overnight capital of ~$1.1B for 48.8 MWe net → **$23k/kWe**—still 5× too expensive, but within the range where NOAK learning curves and supply chain optimization could conceivably reach $5k/kWe. This is the "conditional viability" the model reveals: the Orbitron's structural cost advantage is buried under four layers of unproven physics and engineering. Remove those layers, and a $3–5k/MWh NOAK LCOE becomes *geometrically possible*—though still economically unattractive vs. $50/MWh renewables.

## 5. Cross-Concept Positioning

The Orbitron occupies a unique position in the fusion landscape: it shares D-T fuel and steady-state operation with tokamaks but diverges completely in confinement physics, scale, and cost structure. No other concept in the analysis pipeline offers a useful quantitative comparison.

### **Nearest neighbors (qualitative only)**

**Polywell (27-polywell, gap-checked)**: Both are non-standard electrostatic approaches to D-T fusion using combined electric and magnetic fields. The Polywell has a longer experimental history (U.S. Navy WB-series devices) and a more developed physics critique, but it also has not demonstrated Q>1. The Coulomb collision barrier applies to both concepts—neither has experimentally disproven the thermalization critique. The Polywell uses magnetically-confined virtual electrodes rather than the Orbitron's physical cathode, but the core challenge (achieving fusion-relevant densities without collisional loss dominance) is shared.

**Dense Plasma Focus (24, gap-checked)**: Another "exotic" non-standard D-T concept. Shares the property of extreme physics uncertainty and thin public data, but uses a fundamentally different confinement mechanism (Z-pinch compression vs. electrostatic orbiting). No approved analysis exists for parameter reuse.

**Tokamaks (01-HTS-Compact-Tokamak, 21-Spherical-Tokamak-HTS)**: Share D-T fuel and tritium supply constraints (global inventory ~25–30 kg, CANDU production, $35k/g market price), but diverge completely in cost structure. The Orbitron eliminates the three largest tokamak CAS accounts (magnets, blanket, heating) but introduces novel HV and per-module shielding accounts. The tritium sequencing constraint (early plants must demonstrate self-sufficiency before fleet scaling) applies equally—but the Orbitron is *further behind* because it has no breeding blanket design at all, while tokamaks have detailed blanket engineering from ITER/DEMO programs.

### **Landscape positioning**

The Orbitron is the **most structurally divergent D-T concept** in the portfolio:
- **Smallest device scale**: Desktop/pickup-truck form factor vs. building-scale MFE/IFE plants
- **Lowest magnetic field**: 0.5 T vs. 5–20 T (tokamak/stellarator) or 10–30 T (mirror/FRC)
- **Most capital-efficient at Q>20**: Eliminates ~$850M in tokamak CAS accounts, but this advantage is negated by low net power at Q<15
- **Most OPEX-intensive at low Q**: Purchased tritium at Q=10 contributes 19% of LCOE vs. ~2% for self-breeding tokamaks

If the Orbitron achieves Q=20+ and validates a turbine-array architecture, it could offer the **lowest $/kWe in the D-T landscape**—but only in a NOAK scenario with mass-manufactured modules. If Q remains <10 or Coulomb collision physics proves limiting, it becomes the **most economically disadvantaged D-T concept** due to catastrophic recirculating power fractions and permanent tritium OPEX.

### **TEA implications**

The Orbitron cannot be evaluated with conventional LCOE methods because its physics feasibility is unresolved. The analysis correctly uses a **back-solve conditional viability map**: parameterize Q and $/kWe, compute LCOE surface, identify which (Q, cost) combinations yield LCOE ≤ $100/MWh, then state what experimental results would place the concept in or out of that region.

**Key finding from the model**: At FOAK capital ($100k/module cathode cost), even Q=30 with η=30% yields LCOE = $4.3k/MWh. The $100/MWh threshold is **not reached at any Q value the model explores** (Q ≤ 30). Only in the most optimistic NOAK scenario (Q=20, η=30%, 10,000 modules, $30k/module cathode cost, 7% interest rate) does LCOE approach $3.4k/MWh—still **34× too expensive**.

The model output is *not* an LCOE estimate. It is a **falsifiable physics requirement**: if Coulomb collision physics constrains achievable Q to <20, the concept is structurally non-viable for electricity generation under any capital cost assumption. This is the appropriate analytical framing for pre-Q=1 concepts, and the Orbitron analysis executes it correctly.

## 6. Modeling Confidence

**Rating: Low**

**Data-anchored parameters**: 6 of 28 model inputs
- Cathode voltage: 300 kV (demonstrated, press release)
- Magnetic field target: 0.5 T (AIP Advances 2024 specification)
- Operation mode: steady-state (300 kV sustained for hours, press release)
- Fuel type: D-T (multiple sources)
- Tritium price: $35k/g (market data)
- Plant availability: 85% (steady-state analogue, weakly anchored)

**Speculative parameters**: 22 of 28 model inputs
- **Q_engineering = 10**: No Q value has been measured. Target is Q≈1. The model's Q=10 is aspirational minimum for net power at η=12%.
- **Thermal efficiency = 12%**: Thermoelectric analogue; no conversion system designed.
- **Cathode cost = $100k/module**: No cost data exists; industrial HV analogy with FOAK factor.
- **HV supply cost = $50k/module floor**: Minimum 300 kV sustained supply cost; no Orbitron data.
- **Shielding cost = $15k/m³**: Concrete + structure + integration; "concrete castle" analogy.
- **Cathode lifetime = 2 FPY**: No neutron irradiation data; aggressive assumption vs. tokamak first-wall.
- **O&M fraction = 4%**: Placeholder; no component lifetime or maintenance data.
- **Module count = 1000**: Plant architecture does not exist; assumed for sizing only.
- **All CAS20-50 plant-wide accounts**: Scaled from 1costingfe tokamak formulas with concept-specific overrides; none validated for kWe-scale modular D-T plants.

### **Dominant uncertainty source**

The LCOE uncertainty is not cost uncertainty—it is **physics feasibility uncertainty**. The model can compute LCOE to arbitrary precision for any (Q, η, $/kWe) input triple, but the *choice* of Q is unconstrained by data. At Q=5, net power is negative. At Q=10, LCOE = $302k/MWh. At Q=20, LCOE = $23k/MWh. At Q=30, LCOE = $14k/MWh. The 20× swing from Q=10 to Q=30 dwarfs all cost uncertainty.

**Until Coulomb collision loss rates are measured experimentally, the LCOE range is [–∞, +∞]** because Q itself is undefined. The model assumes Q>1 is achievable—a binary assumption that determines whether the concept produces net power or not. If this assumption is false (i.e., Coulomb collision physics prevents Q>1), the LCOE is undefined regardless of how precisely capital costs are estimated.

### **Cost account confidence breakdown**

| CAS Account | Confidence | Grounding |
|-------------|-----------|-----------|
| C220103 (Magnets) | Medium | HTS at 0.5 T is low-field; small coil geometry; analogy to industrial SC magnets reasonable |
| C220107 (HV Supply) | Low | No Orbitron cost data; industrial 300 kV supply analogy ($50k floor) is order-of-magnitude only |
| C220105 (Cathode) | Very Low | Proprietary HV feedthrough is "key innovation" per company; no disclosed cost or design |
| C220102 (Shield) | Low | "Concrete castle" geometry known but per-module integration cost is unknown |
| CAS80 (Tritium) | High | Fuel consumption calculable from Q and fusion power; tritium price is market data |
| CAS71 (O&M) | Very Low | 4% of CAPEX is placeholder; no component lifetime data under neutron bombardment |
| CAS72 (Cathode replacement) | Very Low | 2 FPY lifetime is assumed; neutron damage to HV cathodes is "truly-unknown" per gap report |

**Overall**: 1 high-confidence account (tritium fuel), 1 medium-confidence account (magnets), 5 low/very-low accounts covering 85% of direct capital. This is the weakest cost basis of any D-T concept in the portfolio.

## 7. What Would Change My Mind

Three specific developments would materially shift the LCOE estimate in either direction:

### **1. Experimental measurement of Q>5 with published Coulomb collision loss rates**
**Direction**: Favorable (if Q>5 demonstrated) or Fatal (if collision losses confirm Q<1 ceiling)

If Avalanche publishes peer-reviewed experimental results showing:
- Sustained fusion operation at ion densities >10¹⁰ cm⁻³ (the space-charge-mitigated regime)
- Measured fusion Q ≥ 5 in a D-T plasma (not beam-into-gas)
- Coulomb collision loss rates ≤ fusion energy production rate

...then the central physics barrier is retired. The LCOE surface shifts from speculative to exploratory: Q=5 at η=30% yields $57k/MWh at baseline capital, still 570× too expensive, but it places the concept in the "difficult but not impossible" regime where engineering cost reduction could conceivably reach commercial LCOE in a NOAK limit.

Conversely, if the measured collision rate confirms the 25–37× fusion rate ratio from Lampe-Mannheimer (1998), the concept is definitively non-viable for D-T power generation. No capital cost reduction, module scaling, or thermal efficiency improvement can overcome a physics barrier that prevents net energy gain.

**Likelihood**: The full-text AIP Advances (2024) and Physics of Plasmas (2025) papers likely contain the first experimental constraints on collision rates, but the gap report notes these were inaccessible (paywalled). The APS DPP 2023 abstract reports ">100 keV deuterium ions confined"—a necessary but insufficient condition for Q>1 (density and confinement time are also required). Avalanche's FusionWERX facility is designed for D-T testing; results are expected within 2–3 years if the program proceeds as announced.

---

### **2. Disclosure of a multi-module turbine-array plant architecture with η>25% at <1 MWe aggregate**
**Direction**: Strongly favorable

If Avalanche or an independent engineering firm publishes a credible plant design showing:
- Stacking of ≥1000 modules with integrated thermal coupling to a shared turbine system
- Demonstrated thermal-to-electric conversion efficiency ≥25% at aggregate thermal power <1 MWe
- Neutron shielding geometry compatible with dense module packing (not individual "concrete castles")

...then the turbine-array scenario (η=30% in the model) becomes physically realizable rather than aspirational. This shifts the baseline LCOE surface from $302k/MWh (thermoelectric, η=12%) to $13k/MWh (turbine, η=30%) at the same Q=10—a **23× improvement**. At Q=20 with this architecture, LCOE drops to $6k/MWh, approaching the range where NOAK learning curves could conceivably yield sub-$1k/MWh in a mature supply chain.

**Likelihood**: Low in the near term. The company's public roadmap emphasizes Q>1 demonstration, not plant architecture development. The modular concept is described qualitatively ("stacked for near-endless power") without engineering detail. Small-scale turbine technology exists (sCO₂, ORC) but achieving 25–30% efficiency below 1 MWe requires custom engineering that has not been demonstrated for fusion applications.

---

### **3. Validated tritium breeding blanket design with TBR≥1.0 integrated with the Orbitron geometry**
**Direction**: Favorable (moderate impact)

If the Fusion Fuel Cycles (FFC) MoU yields a disclosed breeding blanket design with:
- TBR ≥ 1.0 validated by neutronics simulation
- Physical integration with the Orbitron's compact cylindrical geometry (10 cm radius × 20 cm length module)
- Cost estimate ≤ $50k/module additional CAPEX

...then the permanent tritium OPEX penalty is eliminated. At Q=10, baseline LCOE drops from $302k/MWh to ~$246k/MWh (–18%) by removing the $33M/yr tritium purchase cost. At Q=20 with η=30%, LCOE drops from $6k/MWh to ~$4k/MWh (–33%). This is significant but not transformative—tritium cost is a second-order effect compared to Q and η.

**Likelihood**: Low. The compact module geometry provides insufficient space for a conventional lithium blanket (~40 cm thickness required for TBR≥1.0 with FLiBe). Alternative approaches (external blanket surrounding module array, advanced breeding concepts with thin lithium layers) are geometrically possible but add thermal coupling and neutron shielding complexity. The FFC MoU (April 2025) is a disclosed collaboration direction, not a design or timeline. Expect 3–5 years minimum before a conceptual blanket design is published, if at all.

## 8. LCOE Downselect Scoring

### C1: Modularization — Score: **3.8**

**Sub-factor 1: Construction mode classification per CAS account**

The Orbitron's desktop-scale modules are inherently factory-manufacturable, but the plant-level integration introduces site-assembly for BOP and shielding.

| CAS Account | Component | Construction Mode | Score | Cost Weight (%) | Notes |
|-------------|-----------|-------------------|-------|-----------------|-------|
| C220101 | Chamber wall | Factory module | 5 | 5% | Stainless vacuum envelope, precision-welded; ships as sealed unit |
| C220102 | Neutron shield | Site-assembled | 3 | 1% | Concrete + steel enclosure; poured/erected on-site around module array |
| C220103 | HTS magnets | Factory module | 5 | 12% | Two compact HTS coil pairs per module; wound and tested at factory |
| C220105 | Cathode assembly | Factory module | 5 | 24% | Tungsten cathode + HV feedthrough is proprietary; precision assembly at factory |
| C220106 | Vacuum system | Factory module | 5 | 19% | Ion pumps + turbo pumps integrated into module at factory |
| C220107 | HV power supply | Factory module | 5 | 12% | 300 kV sustained supply is industrial product; factory-built and tested |
| C220110 | Remote handling | Factory sub-assemblies | 3 | 1% | Robotic tooling for module swap; assembled on-site from factory components |
| C220200 | Coolant system | Site-assembled | 3 | 0.4% | Thermal coupling between modules; piping erected on-site |
| C220300 | Aux cooling + cryo | Site-assembled | 3 | 14% | Cryoplant for HTS coils is plant-level equipment; installed on-site |
| C220700 | I&C | Factory sub-assemblies | 3 | 1% | Distributed sensors/controls per module shipped as components; integrated on-site |

**Cost-weighted average (CAS22 only)**:
- Factory module (score 5): 72% of CAS22 cost
- Site-assembled (score 3): 17% of CAS22 cost
- Factory sub-assemblies (score 3): 2% of CAS22 cost
- **Weighted average: (0.72×5) + (0.17×3) + (0.02×3) = 4.17**

**Sub-factor 2: Module repetition boost**

1000 modules per plant at baseline; each module is identical. Per framework: 10–49 modules → +0.5 boost; ≥50 modules → +1.0 boost (diminishing returns above 49, but 1000 is well into saturation).

**Module repetition boost: +1.0**

**Total C1 score**: 4.17 (weighted mode) + 1.0 (repetition) = **5.17**, clamped to [1, 5] → **5.0**

Wait—I need to re-check the calculation. Let me recalculate more carefully, as the framework says the boost applies to the cost-weighted average, and the result should be clamped to 5.

Actually, re-reading: "C1 = cost-weighted average of mode scores + module repetition boost, clamped to [1, 5]."

So: 4.17 + 1.0 = 5.17, clamped → **5.0**. But this seems too generous. Let me verify the cost weights are correct by checking the model output.

From model output (baseline, 1000 modules):
- C220101: $20M fleet (5%)
- C220102: $5.65M fleet (1%)
- C220103: $50M fleet (12%)
- C220105: $100M fleet (24%)
- C220106: $80M fleet (19%)
- C220107: $50M fleet (12%)
- C220110: $5M fleet (1%)
- C220200: $1.63M (0.4%)
- C220300: $57M (14%)
- C220700: $2.83M (1%)
- CAS22 total: $416M

Cost-weighted average calculation:
- Factory module accounts (5): 20+50+100+80+50 = $300M → 72% of $416M
- Site-assembled accounts (3): 5.65+1.63+57+2.83 = $67M → 16% of $416M
- Factory sub-assemblies (3): 5 = $5M → 1% of $416M
- Unaccounted: $416M - $372M = $44M (missing from this breakdown—likely other CAS22 accounts like C220111 installation, C220400, C220500, C220600 which are plant-wide)

Hmm, I need to include all CAS22 accounts for the cost weight. Let me use only the major per-module accounts for the mode classification and note that plant-wide accounts (C220200, C220300, C220400, C220500, C220600, C220700) are site-assembled or site-erected by definition.

Let me recalculate using CAS22 per-module subtotal ($354M fleet) + plant-wide subtotal ($62M):
- Factory module (score 5): $300M / $416M = 72%
- Site-assembled (score 3): ($5.65M shield + $62M plant-wide) / $416M = 16%
- Factory sub-assemblies (score 3): $5M / $416M = 1%
- Other (installation C220111 = $43M): site labor, score 1 → 10%

Revised cost-weighted average:
(0.72×5) + (0.16×3) + (0.01×3) + (0.10×1) = 3.6 + 0.48 + 0.03 + 0.10 = **4.21**

Add module repetition boost (+1.0 for 1000 modules): 4.21 + 1.0 = 5.21, clamped to [1, 5] → **5.0**

Actually, I realize installation labor (C220111) should not be "site-erected" (score 1) but rather "site-assembled from factory sub-assemblies" (score 3)—it's the labor to install factory-built modules. Let me re-score:

- Factory module (score 5): $300M / $416M = 72%
- Site-assembled (score 3): ($5.65M shield + $62M plant-wide + $43M installation) / $416M = 27%
- Factory sub-assemblies (score 3): $5M / $416M = 1%

Weighted: (0.72×5) + (0.27×3) + (0.01×3) = 3.6 + 0.81 + 0.03 = **4.44**

Add boost: 4.44 + 1.0 = 5.44, clamped → **5.0**

This still clamps to 5.0. But intuitively, the Orbitron should score very high on modularization (desktop-scale factory-built modules), so C1=5.0 seems correct. However, I should be more conservative given that the plant-wide BOP (27% of cost) is site-assembled. Let me check if the "module repetition boost" should actually be smaller.

Re-reading framework: "10–49 identical modules: +1.0 to the cost-weighted average. Diminishing returns above 49 units."

The text says "+1.0" for 10-49 modules, with diminishing returns above 49. It does *not* specify the exact boost value for 1000 modules, but implies it's still +1.0 (just with diminishing marginal benefit beyond 49). So +1.0 is correct.

Given that 72% of CAS22 cost is factory-manufactured modules (score 5) and 27% is site-assembled (score 3), the weighted average before boost is 4.44. Adding +1.0 boost → 5.44, clamped to 5.0.

**Final C1 score: 5.0**

But let me double-check the mode classifications for a few key accounts:
- **C220102 (shield)**: I scored this as "site-assembled" (score 3). But if shielding is poured concrete around a dense module array, this is "stick-built / field-erected" (score 1). Let me revise to score 1.
- **C220200 (coolant)**: Site-assembled piping → score 3 is correct.
- **C220300 (cryo)**: Industrial cryoplant installed on-site → score 3 is correct.
- **C220111 (installation)**: Labor to install factory modules → score 3 is reasonable.

Revised with shield = 1:
- Factory module (score 5): $300M / $416M = 72%
- Site-assembled (score 3): ($62M plant-wide + $43M installation + $5M RH) / $416M = 26%
- Stick-built (score 1): $5.65M shield / $416M = 1%

Weighted: (0.72×5) + (0.26×3) + (0.01×1) = 3.6 + 0.78 + 0.01 = **4.39**
Add boost: 4.39 + 1.0 = 5.39, clamped → **5.0**

OK so C1 = 5.0 is robust to these variations. The Orbitron genuinely scores very high on modularization.

**Justification (2-3 sentences)**: The Orbitron's desktop-scale modules (cathode, HTS magnets, HV supply, vacuum system) are entirely factory-manufacturable with 1000 identical units per plant, scoring 5 (factory module) for 72% of CAS22 direct capital. Plant-wide BOP (coolant, cryoplant, I&C) is site-assembled (score 3) for 26% of cost. The module repetition boost (+1.0 for 1000 units) pushes the cost-weighted score from 4.4 to 5.4, clamped at the maximum 5.0. Modularization is the concept's strongest structural advantage.

---

### C3: Supply Chain Learning — Score: **3.5**

**Sub-factor A: Component learning rates (1-5, cost-weighted)**

| Component | Learning Rate Category | Score | Cost Weight (%) | Rationale |
|-----------|------------------------|-------|-----------------|-----------|
| HTS magnets (0.5 T) | Growing production base | 4 | 12% | REBCO tape supply chain is expanding; 0.5 T compact coils are orders of magnitude smaller than tokamak magnets; existing industrial SC magnet vendors can supply |
| HV power supply | Specialty, limited supply | 3 | 12% | Industrial 300 kV sustained supplies exist for accelerators/e-beam systems, but production volume is low; Avalanche's proprietary HV feedthrough is novel (no existing market) |
| Cathode assembly | Fusion-specific, no market | 2 | 24% | Tungsten cathode geometry optimized for orbitrap confinement is novel; neutron-tolerant HV electrode at 300 kV has no current analog |
| Vacuum system | Industrial, established | 4 | 19% | Ion pumps, turbo pumps, HV feedthroughs (non-neutron) are mature industrial products with large supply base |
| Neutron shielding | Commodity | 5 | 1% | Concrete and structural steel are globally abundant commodities |
| Coolant/thermal | Industrial, established | 4 | 0.4% | Small-scale heat exchangers and coolant loops are mature industrial products |
| Cryoplant | Specialty, limited supply | 3 | 14% | Industrial cryocoolers for HTS exist but production is limited; low cryo load (5 W/module) uses existing technology |
| I&C | Industrial, established | 4 | 1% | Distributed sensors, HV monitoring, control systems are mature with large markets |

**Cost-weighted average**:
(0.12×4) + (0.12×3) + (0.24×2) + (0.19×4) + (0.01×5) + (0.004×4) + (0.14×3) + (0.01×4)
= 0.48 + 0.36 + 0.48 + 0.76 + 0.05 + 0.02 + 0.42 + 0.04 = **2.61**

Hmm, this seems low. Let me recalculate with attention to the cost weights summing to 100%:

From CAS22 breakdown ($416M total):
- C220103 HTS: $50M → 12%
- C220107 HV supply: $50M → 12%
- C220105 Cathode: $100M → 24%
- C220106 Vacuum: $80M → 19%
- C220102 Shield: $5.65M → 1.4%
- C220200 Coolant: $1.63M → 0.4%
- C220300 Cryo: $57M → 14%
- C220700 I&C: $2.83M → 0.7%
- Other (C220101, 111, 400, 500, 600): $69M → 16.5%

I need to classify "Other" accounts:
- C220101 chamber wall ($20M, 5%): Stainless steel vacuum envelope → industrial, established → score 4
- C220111 installation ($43M, 10%): Labor, not a component → exclude from learning rate assessment (or score as 3 for construction labor learning)
- C220400 rad waste ($0.02M, ~0%): negligible
- C220500 fuel handling ($0.16M, ~0%): negligible
- C220600 other equipment ($0M reported): negligible

Revised cost weights (excluding installation labor):
Total cost excluding installation = $416M - $43M = $373M

- HTS: $50M / $373M = 13.4%
- HV supply: $50M / $373M = 13.4%
- Cathode: $100M / $373M = 26.8%
- Vacuum: $80M / $373M = 21.4%
- Chamber wall: $20M / $373M = 5.4%
- Shield: $5.65M / $373M = 1.5%
- Coolant: $1.63M / $373M = 0.4%
- Cryo: $57M / $373M = 15.3%
- I&C: $2.83M / $373M = 0.8%

Weighted average:
(0.134×4) + (0.134×3) + (0.268×2) + (0.214×4) + (0.054×4) + (0.015×5) + (0.004×4) + (0.153×3) + (0.008×4)
= 0.536 + 0.402 + 0.536 + 0.856 + 0.216 + 0.075 + 0.016 + 0.459 + 0.032
= **3.13**

Round to one decimal: **3.1**

**Sub-factor B: Supply chain bottleneck count (1-5)**

Start at 5.0, subtract penalties:

**Hard constraints (no known path to required quantity)**: 0
- None identified. All components have existing industrial supply chains or are manufacturable with current technology.

**Scaling constraints (exists but must scale 10×+)**: 2
- **HTS tape for compact 0.5 T coils**: Existing REBCO production can supply small coils, but scaling to 1000 modules (1000 coil pairs) requires increased tape production. However, the total tape quantity is ~50–200 m per module × 1000 modules = 50–200 km total—well within current global REBCO production capacity (~500–1000 km/yr). This is NOT a hard constraint (no 10× scaling needed), so no penalty. *Actually, on second thought, 1000 modules is relatively modest scale, so no scaling penalty applies.*
- **300 kV sustained HV supplies**: Industrial production exists for accelerator/e-beam markets, but scaling to 1000+ units/yr for a commercial Orbitron fleet would require 10× expansion of current specialized HV supply vendors. **–0.5 penalty**.
- **Proprietary HV feedthrough**: Avalanche's "key innovation" has no current market. Scaling to mass production (1000+ units/yr) requires establishing a new supply chain. **–0.5 penalty**.

**Sole-source dependency**: 1
- **Avalanche HV feedthrough**: Proprietary design with no alternative suppliers disclosed. **–0.25 penalty**.

**Helium-3 fuel dependency**: 0
- Concept uses D-T, not D-He3.

**Total penalties**: –0.5 (HV supply scaling) – 0.5 (HV feedthrough scaling) – 0.25 (sole-source) = **–1.25**

**Sub-factor B score**: 5.0 – 1.25 = **3.75**, rounded to **3.8**

**Sub-factor C: External demand pull (1-5)**

What fraction of capital cost is in components with >$1B/yr external market?

- **Vacuum systems** (ion pumps, turbo pumps): $80M (19%) → >$1B/yr global market (semiconductor, research, industrial vacuum)
- **Cryoplant** (cryocoolers): $57M (14%) → >$1B/yr global market (medical MRI, industrial gas liquefaction, superconducting magnet applications)
- **Coolant/heat exchangers**: $1.63M (0.4%) → >$1B/yr global market
- **I&C** (sensors, controls): $2.83M (0.7%) → >$10B/yr global market
- **Neutron shielding** (concrete, steel): $5.65M (1.4%) → >$100B/yr global construction market
- **Chamber wall** (stainless steel): $20M (5%) → >$10B/yr global stainless steel market

**Total with >$1B/yr external market**: $80M + $57M + $1.63M + $2.83M + $5.65M + $20M = **$167M**
**Fraction of CAS22**: $167M / $416M = **40%**

Per framework:
- >60%: score 5
- 40–60%: score 4
- 20–40%: score 3
- 10–20%: score 2
- <10%: score 1

**Sub-factor C score: 4**

**C3 total**: (A + B + C) / 3 = (3.1 + 3.8 + 4.0) / 3 = **3.63**, rounded to **3.6**

Hmm, let me recalculate C more carefully. I should check if "HTS magnets" count as external demand pull. REBCO tape has a growing market for fusion magnets, but the market is currently <$1B/yr globally. However, *cryocoolers* for HTS are part of a >$1B/yr market (medical MRI cryogenics, industrial SC applications). Let me not double-count cryo in the >$1B category if I already counted it.

Actually, re-reading my list: I counted cryoplant ($57M, 14%) separately, which is correct. HTS magnets ($50M, 12%) are NOT in the >$1B/yr category (global REBCO market is ~$100–500M/yr currently, growing). So my C=4 calculation is correct: 40% of cost is in >$1B/yr markets.

**Final C3 score: 3.6**

**Justification**: Component learning rates average **3.1/5** (cost-weighted): vacuum systems, chamber wall, and cryoplant (47% of cost) score 4 (industrial, established supply), but the cathode assembly (26% of cost) scores only 2 (fusion-specific, no current market) and the proprietary HV feedthrough (13% of cost) scores 3 (specialty, limited supply). Supply chain bottlenecks are moderate (**3.8/5**): scaling 300 kV HV supplies and the proprietary feedthrough to 1000+ units/yr requires 10× vendor expansion (–1.0 penalty), and the HV feedthrough is sole-source (–0.25). External demand pull is **4/5**: 40% of capital cost (vacuum systems, cryo, shielding, chamber steel) taps >$1B/yr industrial markets. The cathode and HV supply novelty limit learning potential.

---

### C4: Plant Complexity — Score: **3.0**

**Sub-factor A: Operational coupling density (1-5)**

Rate failure cascades and maintenance dependencies focusing on OPERATIONAL coupling (if component X fails, what else stops working).

**Module-level coupling (within a single Orbitron module)**:
- **Cathode failure** → immediate module shutdown (no fusion without 300 kV cathode potential). Other modules unaffected. **Low inter-module coupling**.
- **HV supply failure** → immediate module shutdown. Other modules unaffected. **Low inter-module coupling**.
- **Vacuum breach** → module shutdown (plasma extinguished). Other modules unaffected unless breach is catastrophic (neutron shielding breach → radiation hazard affects adjacent modules). **Low-to-moderate coupling**.
- **HTS magnet quench** → E×B electron confinement lost → module shutdown. Other modules unaffected unless quench damages cryo supply (affects all modules sharing cryoplant). **Moderate coupling via shared cryo**.
- **Ion gun failure** → reduced fusion rate but not immediate shutdown (cathode still accelerates residual ions). **Low coupling**.

**Plant-level coupling**:
- **Cryoplant failure** → all 1000 HTS magnets lose cooling → plant-wide shutdown within hours as magnets quench sequentially. **High coupling** (single-point failure cascades to full plant).
- **Coolant system failure** → thermal runaway in operating modules → emergency shutdown required. **Moderate-to-high coupling** (shared coolant loop creates cascade potential).
- **Tritium supply interruption** → gradual fusion rate decline as fuel depletes, but not immediate shutdown (can run on D-D or residual D-T inventory). **Low coupling**.
- **Module replacement** → one module can be swapped without shutting down others (assuming modular design intent). **Low coupling** (if design is competent).

**Operational coupling verdict**: The plant has **one critical single-point failure** (cryoplant for 1000 HTS coils), but otherwise module-level failures are mostly isolated. Maintenance dependencies are moderate: cathode replacement requires module shutdown but not plant shutdown. HV feedthrough failure is a module-level event. Neutron shielding integrity is module-specific (or array-specific if shared shielding design is used, which is TBD).

Comparison to tokamak baseline:
- **Tokamak**: Magnet quench → plant shutdown; first-wall breach → plant shutdown; blanket failure → plant shutdown; RF system failure → plasma loss → shutdown. **Highly coupled** (score 2–3).
- **Orbitron**: Module failures are isolated except for shared cryoplant. **Moderately decoupled** (score 3–4).

**Sub-factor A score: 3.5**

Reasoning: The cryoplant single-point failure drops the score from 4 (mostly decoupled) to 3.5 (moderate coupling). If the design evolves to per-module cryo (eliminating the shared cryoplant), this could rise to 4.

**Sub-factor B: Subsystem count (1-5)**

Count CAS22 sub-accounts representing >1% of total capital ($416M × 0.01 = $4.2M threshold):

From model output:
1. C220103: HTS magnets — $50M (12%) ✓
2. C220107: HV supply — $50M (12%) ✓
3. C220105: Cathode assembly — $100M (24%) ✓
4. C220106: Vacuum system — $80M (19%) ✓
5. C220102: Neutron shield — $5.65M (1.4%) ✓
6. C220300: Cryo + aux cooling — $57M (14%) ✓
7. C220111: Installation — $43M (10%) ✓
8. C220101: Chamber wall — $20M (5%) ✓
9. C220700: I&C — $2.83M (0.7%) — below threshold
10. C220200: Coolant — $1.63M (0.4%) — below threshold

**Subsystem count >1% of capital: 8**

Per framework:
- Fewer than 5: score 5
- 5–7: score 4
- 8–10: score 3
- 11–14: score 2
- 15+: score 1

**Sub-factor B score: 3**

**C4 total**: (A + B) / 2 = (3.5 + 3.0) / 2 = **3.25**, rounded to **3.3**

Hmm, but I should reconsider whether "Installation" (C220111) counts as an operational subsystem. Installation is a cost account for labor during construction, not an operating subsystem. Let me exclude it:

Subsystems >1% (excluding installation):
1. HTS magnets — $50M ✓
2. HV supply — $50M ✓
3. Cathode assembly — $100M ✓
4. Vacuum system — $80M ✓
5. Neutron shield — $5.65M ✓
6. Cryo + aux cooling — $57M ✓
7. Chamber wall — $20M ✓

**Subsystem count: 7** → score **4** per framework (5–7 subsystems)

**Revised C4 total**: (3.5 + 4.0) / 2 = **3.75**, rounded to **3.8**

**Justification**: Operational coupling is **moderate** (score 3.5): module-level failures (cathode, HV supply, vacuum) are isolated and do not cascade to other modules, but the shared cryoplant for 1000 HTS magnets is a single-point failure that would shut down the entire plant. Subsystem count is **7** (score 4): major subsystems include HTS magnets, HV supply, cathode, vacuum, shield, cryo, and chamber wall—all >1% of capital. The modular architecture limits failure propagation compared to highly-coupled tokamak systems, but the cryoplant dependency and lack of in-vessel complexity (no breeding blanket, no plasma-facing components beyond cathode) keep complexity moderate rather than low.

---

### C5: Customization Needs — Score: **1.75 → scaled to 2.3**

**Sub-factor A: Thermal rejection (1-4)**

The baseline model uses thermoelectric conversion (η=12%, no large heat rejection) but the turbine-array scenario (η=30%) requires conventional thermal cycle with cooling towers.

- If thermoelectric-only (baseline): **score 4** (air-cooled or minimal cooling)
- If turbine array (optimistic scenario): **score 2** (large cooling towers required)

The company states "thermal cycle with turbines" (Orbitron page), suggesting intent to use conventional thermal rejection. However, at 1–100 kWe per module, turbines are implausible. The *realistic* near-term path is thermoelectric or small-scale ORC with minimal cooling. The *aspirational* commercial path is turbine array with cooling towers.

**Conservative scoring (assume turbine scenario intent)**: **score 2**

**Sub-factor B: Fuel safety profile (1-4)**

- D-T fuel with full tritium handling, no breeding blanket (tritium purchased) → **score 1** per framework

**Raw C5**: (A + B) / 2 = (2 + 1) / 2 = **1.5**

**Scaled to [1, 5]**: C5 = 1 + (1.5 – 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = **1.67**, rounded to **1.7**

Wait, I need to recompute the scaling formula. The framework states:

> **C5 = (A + B) / 2**, then scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)

The raw score range for (A + B)/2 is [1, 4] (since A and B each range [1, 4]).
- Minimum raw: (1+1)/2 = 1
- Maximum raw: (4+4)/2 = 4

Scaling formula maps [1, 4] → [1, 5]:
- At raw=1: C5 = 1 + (1–1)×(4/3) = 1 + 0 = 1 ✓
- At raw=4: C5 = 1 + (4–1)×(4/3) = 1 + 3×1.333 = 1 + 4 = 5 ✓

For raw=1.5:
C5 = 1 + (1.5–1)×(4/3) = 1 + 0.5×1.333 = 1 + 0.667 = **1.67**, rounded to **1.7**

Hmm, but this seems very low. Let me reconsider the thermal rejection score. The framework says:

> 4 = No thermal cycle or air-cooled (e.g., direct energy conversion only)

The baseline Orbitron scenario uses thermoelectric conversion (a solid-state heat-to-electricity process) with heat rejection to air or a small coolant loop. This is closer to "air-cooled" than "large cooling towers," so I should score A=4 for the baseline case, not A=2.

However, the company *states* they will use turbines (implying conventional thermal cycle with cooling towers). The ambiguity here is that the stated intent (turbines) conflicts with the physical reality (1–100 kWe scale makes turbines implausible).

**Conservative approach**: Score based on stated intent (turbines) → A=2
**Optimistic approach**: Score based on physically realistic path (thermoelectric) → A=4

I'll use the conservative scoring (A=2) because the framework instructs to avoid inflating C5 with "site-specific advantages" and to score "intrinsic concept characteristics." The *concept* as described by the company uses turbines (A=2), even if this is implausible at the claimed scale.

**Final C5 raw**: (2 + 1) / 2 = **1.5**
**Scaled**: 1 + (1.5–1)×(4/3) = **1.67**, rounded to **1.7**

Actually, wait. Let me reconsider the fuel safety score. The framework says:

> 1 = D-T (full tritium handling and breeding infrastructure)

But the Orbitron has **no breeding infrastructure**—tritium is purchased. Does this make the fuel profile *worse* (no breeding = permanent hazmat dependency) or *better* (no breeding blanket complexity)? The framework's intent with "score 1" for D-T is to penalize the site-level tritium handling, activation, and regulatory burden—not the *cost* of tritium (that's handled in LCOE).

The Orbitron's fuel safety profile is:
- D-T fuel: neutron radiation, tritium inventory on-site (albeit smaller than tokamak due to no breeding blanket inventory)
- No breeding blanket: eliminates FLiBe/LiPb chemical hazards, reduces activation inventory per module
- Compact scale: smaller absolute tritium inventory per module, but 1000 modules → plant-wide inventory is comparable to large tokamak

**Fuel safety verdict**: The elimination of breeding blanket reduces some hazards (no molten salt, no beryllium), but the core D-T neutron and tritium burden remains. This is still "score 1" per the framework definition.

**Final C5**: **1.7**, but let me reconsider the thermal rejection score one more time.

Actually, I realize the framework's thermal rejection scale is about the *site* burden, not the technology pathway:
- Score 4 = no thermal cycle or air-cooled (minimal site infrastructure)
- Score 2 = large cooling towers required (significant site infrastructure)

If the Orbitron uses thermoelectric conversion at kWe scale, the heat rejection per module is tiny (~8–9 kWe thermal per module at Q=10, η=12%). For 1000 modules, total heat rejection is ~8–9 MWe thermal—this can be air-cooled with forced-air heat exchangers (like data center cooling), not requiring cooling towers.

If the Orbitron uses turbine-array at megawatt aggregate (e.g., 10,000 modules, ~100 MWe thermal), cooling towers are required.

The baseline scenario (1000 modules, thermoelectric) is **air-cooled** → A=4.
The aspirational scenario (10,000 modules, turbines) requires **cooling towers** → A=2.

Since the scoring framework asks for the "intrinsic concept characteristics" and the company's *stated* commercial pathway is turbines, I'll score the aspirational case: **A=2**.

**Final C5 raw**: (2 + 1) / 2 = **1.5**
**Scaled**: 1 + (1.5–1)×(4/3) = **1.67**, rounded to **1.7**

Hmm, but 1.7 seems very low and I worry I'm under-scoring. Let me check if I'm applying the scaling formula correctly by testing edge cases again:

- Minimum: A=1, B=1 → raw = 1 → scaled = 1 + (1–1)×(4/3) = 1 ✓
- Maximum: A=4, B=4 → raw = 4 → scaled = 1 + (4–1)×(4/3) = 1 + 4 = 5 ✓
- My case: A=2, B=1 → raw = 1.5 → scaled = 1 + 0.5×1.333 = 1.667 ✓

The math is correct. The low score reflects the D-T fuel burden (B=1, no avoiding this) and the thermal cycle requirement (A=2, assuming turbines per company statement).

Actually, I realize I should reconsider whether the Orbitron should get credit for "hybrid power conversion" (A=3). The framework says:

> 3 = Hybrid power conversion (partial DEC + partial thermal)

If the Orbitron eventually combines thermoelectric conversion (capturing cathode heat directly) + turbine cycle (capturing blanket neutron heat), this would be hybrid (A=3). But there's no blanket, so this doesn't apply. The concept is either:
- Pure thermoelectric (A=4) if kWe-scale
- Pure thermal cycle (A=2) if MW-scale

There's no hybrid pathway for the Orbitron. So A=2 (conservative, assumes turbines) or A=4 (optimistic, assumes thermoelectric) are the only options.

I'll stick with **A=2** (conservative, matches company's stated intent) → **C5 = 1.7**

But actually, let me reconsider one more time whether I should score the *baseline feasible* scenario (thermoelectric, A=4) or the *stated aspirational* scenario (turbines, A=2). The framework says to score "intrinsic concept characteristics," not aspirations.

The *intrinsic* thermal rejection characteristic of a 1 kWe module is that it produces ~8–9 kWe thermal waste heat. This is air-coolable. The *plant-level* thermal rejection depends on module count: 1000 modules (baseline) → 8–9 MWe thermal → air-cooled; 10,000 modules → 80–90 MWe thermal → likely requires cooling towers.

Since the framework is scoring the *concept* (not a specific plant size), I should score the intrinsic module-level characteristic: **A=4** (air-cooled at module scale).

**Revised C5 raw**: (4 + 1) / 2 = **2.5**
**Scaled**: 1 + (2.5–1)×(4/3) = 1 + 1.5×1.333 = 1 + 2 = **3.0**

This feels more reasonable. The Orbitron's intrinsic thermal rejection is modest (air-coolable at module scale), but the D-T fuel burden is unavoidable (B=1).

**Final C5: 3.0**

**Justification**: Thermal rejection at module scale is **air-cooled** (score 4): each 1 kWe module produces ~8–9 kWe thermal waste heat, manageable with forced-air heat exchangers without requiring cooling towers (though a large plant with 10,000+ modules would eventually require wet cooling). Fuel safety profile is **D-T with full tritium handling** (score 1): neutron radiation, tritium inventory, and activation hazards are intrinsic to D-T fuel regardless of device scale; the lack of a breeding blanket eliminates FLiBe/beryllium chemical hazards but does not reduce the core tritium regulatory burden. Raw score (4+1)/2 = 2.5 scales to **3.0/5**.

---

### C8: Data Adequacy — Score: **2.3**

**Sub-factor A: Source diversity & independence (1-5)**

Available sources:
- **Peer-reviewed**: 2 papers (AIP Advances 2024, Physics of Plasmas 2025) — abstracts only; full text paywalled
- **Company publications**: CWFest 2023 blog (most substantive technical source), press releases (300 kV milestone, $29M raise, FusionWERX grant), product page
- **Independent**: None (no university/lab analyses, no fusion TEA frameworks have published Orbitron assessments)
- **Public-domain architecture literature**: None (no plant studies, no independent reactor designs)

The two peer-reviewed papers confirm the experimental program is real, but only abstracts were accessible. All technical detail derives from company sources. No independent validation or critique exists in the public domain.

**Sub-factor A score: 2** (almost exclusively company publications; 2 peer-reviewed abstracts provide minimal independent validation)

**Sub-factor B: Reactor design specification (1-5)**

- **Device-level**: Confinement geometry described qualitatively (E×B crossed-field, 300 kV cathode, 0.5 T HTS target). Operating point targets stated (1 kW input, Q≈1 target, 10^11 n/s). Form factor (desktop scale, "tens of cm"). **Preliminary design**.
- **Subsystem-level**: HV feedthrough described as proprietary innovation (4.7 MV/m sustained). Ion gun array mentioned but not specified. Diagnostics listed (scintillators, He-3 counters, X-ray/neutron spectroscopy). Energy conversion stated ("thermal cycle with turbines") but not designed. **Partial subsystem definition**.
- **Plant-level**: No architecture. Modular stacking described qualitatively ("near-endless power applications") with no module count, BOP layout, or integration design. **No plant design**.

**Sub-factor B score: 2** (preliminary device design with key subsystems defined but significant gaps in integration; no plant-level design)

**Sub-factor C: LCOE parameter coverage (1-5)**

From gap_report.md, blocking gaps:
1. Q>1 not demonstrated — blocking
2. Coulomb collision loss rate not measured — blocking
3. Ion density, confinement time, triple product unpublished — blocking
4. Commercial plant architecture undefined — blocking
5. Energy conversion system at kWe scale undefined — blocking
6. Overnight capital cost per kWe — blocking
7. Achieved Q value (not target) — blocking (proprietary)
8. Component replacement schedule (cathode, HV, ion gun) — blocking (proprietary)
9. Capacity factor / availability — blocking
10. Thermal conversion efficiency — blocking

**Blocking gap count: 10** (8+ blocking gaps)

Per framework:
- 0 blocking gaps: score 5
- 1–2: score 4
- 3–4: score 3
- 5–7: score 2
- 8+: score 1

**Sub-factor C score: 1**

**Sub-factor D: Commercialization pathway clarity (1-5)**

- **Timeline**: "Less than six years" to commercial operation (CWFest 2023) — aspirational, no milestone-based plan
- **Funding**: $29M Series A + $10M state grant = $39M total — modest by fusion standards
- **Facility**: FusionWERX (Richland, WA) confirmed for Q>1 D-T testing, tritium-licensed, operational 2027 — this is concrete near-term infrastructure
- **Technical milestones**: 300 kV sustained achieved (2025 press release); Q>1 D-T test program intent (2026 press release); no published roadmap linking milestones to commercial scale
- **Commercial pathway**: Modular stacking + mass manufacturing cited as cost reduction mechanism, but no plant design, cost model, or scaling validation exists

**Sub-factor D score: 3** (general pathway described with identified near-term steps but lacking specifics for commercial scale)

**C8 total**: (A + B + C + D) / 4 = (2 + 2 + 1 + 3) / 4 = **2.0**

Wait, this seems too low. Let me reconsider D. The FusionWERX facility (tritium-licensed, Q>1 D-T testing capability, operational 2027) is a *concrete* near-term milestone, not vague aspiration. The funding ($39M) is real. The 300 kV milestone is demonstrated hardware. This should score higher than 3.

Re-reading the framework for D:
- 5 = Detailed commercialization plan with milestones, funding, and timeline
- 4 = Clear pathway with identified steps but some gaps
- 3 = General pathway described but lacking specifics
- 2 = Vague or aspirational commercialization narrative
- 1 = No commercialization pathway articulated

The Orbitron has:
- **Identified steps**: 300 kV achieved → FusionWERX Q>1 tests (2027–2029) → commercial modular plant (no timeline)
- **Funding**: $39M raised (sufficient for Phase 1 D-T testing, insufficient for commercial plant)
- **Gaps**: No commercial plant design, no cost model, no scaling validation, no supply chain plan

This is "clear pathway with identified steps but some gaps" → **score 4** is more accurate than 3.

**Revised C8 total**: (2 + 2 + 1 + 4) / 4 = **2.25**, rounded to **2.3** (keeping one decimal as specified)

**Justification**: Source diversity is **limited** (score 2): all substantive technical data derives from company sources (CWFest 2023 blog, press releases); two peer-reviewed papers exist but only abstracts were accessible, providing minimal independent validation. Reactor design specification is **preliminary** (score 2): device-level confinement geometry and operating point targets are described, key subsystems (HV feedthrough, cathode, HTS magnets) are identified, but energy conversion and plant architecture are undefined. LCOE parameter coverage is **very poor** (score 1): **10 blocking gaps** including Q value, Coulomb collision rates, plant architecture, capital cost, conversion efficiency, and availability—no LCOE-critical parameter is experimentally anchored. Commercialization pathway is **moderately clear** (score 4): FusionWERX facility (tritium-licensed, operational 2027) provides concrete near-term D-T testing capability; $39M funding secured; 300 kV milestone achieved; but commercial-scale pathway lacks design, cost model, or scaling validation.

---

### C7: Technical Risk Evidence Matrix

I'll now fill the 7-function × 2-subcategory = 14-cell risk matrix.

#### **Function 1: Plasma Performance**

**Physics risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Ion density >10¹⁰ cm⁻³ at >100 keV energy with confinement time sufficient for Q>10 |
| Best demonstrated | >100 keV deuterium ions confined (APS DPP 2023 abstract); density not published; Q not measured |
| Gap ratio | N/A (density and confinement time unpublished) |
| Closure mechanism | Space-charge mitigation via electron co-confinement; PIC simulations show 5.4×10¹⁰ cm⁻³ achievable (AIP Advances 2024) |
| Classification | Binary (no net fusion without achieving required density-temperature-confinement triple product) |
| Evidence tier | 3 (subscale: >100 keV ion energies demonstrated, but density regime and confinement time uncharacterized experimentally; simulation-only for space-charge mitigation) |

**Hardware risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Cathode maintains 300 kV potential under 14 MeV neutron flux (>10²⁰ n/m²) for >2 FPY without arc/breakdown |
| Best demonstrated | 300 kV sustained for hours in vacuum at 3 W power draw (2025 press release); no neutron exposure testing published |
| Gap ratio | N/A (neutron fluence tolerance unpublished) |
| Closure mechanism | Proprietary HV feedthrough design achieving 4.7 MV/m field gradient (Avalanche innovation); neutron damage mitigation TBD |
| Classification | Degrading (cathode failure shortens replacement cycle, increasing O&M cost; does not prevent net electricity if cathode is replaced) |
| Evidence tier | 3 (partial demonstration: 300 kV sustained in vacuum validated, but neutron-exposed operation is untested) |

---

#### **Function 2: Driver / Energy Input**

**Physics risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Ion gun array delivers >10¹⁷ ions/s at >100 keV without excessive beam loss or divergence |
| Best demonstrated | "Mode-enhanced ion loading in a 100 kV orbitrap" (Physics of Plasmas 2025 title); ion energies >100 keV achieved (APS abstract); loading efficiency not published |
| Gap ratio | N/A (ion loading rate unpublished) |
| Closure mechanism | Mode-enhanced ion loading technique (per Physics of Plasmas 2025 paper title); scaling from 100 kV to 300 kV operating point |
| Classification | Degrading (insufficient ion loading reduces fusion rate, lowering Q; does not prevent net electricity if loading is improved) |
| Evidence tier | 3 (partial demonstration: 100 kV operation with ion loading validated; 300 kV operation and high-density loading uncharacterized) |

**Hardware risk:**

| Field | Value |
|-------|-------|
| Plant requirement | HV power supply delivers 300 kV sustained at 1 kWe per module with >95% efficiency and <1% voltage ripple under plasma load |
| Best demonstrated | 300 kV sustained for hours at 3 W draw (feedthrough power, not plasma load); commercial accelerator/e-beam supplies at 300 kV exist industrially |
| Gap ratio | N/A (efficiency under plasma load unpublished) |
| Closure mechanism | Avalanche proprietary HV feedthrough + industrial 300 kV supply technology (particle accelerator analogue) |
| Classification | Degrading (HV supply inefficiency increases recirculating power, reducing net electricity; does not prevent operation if efficiency is <95%) |
| Evidence tier | 4 (near-regime: 300 kV sustained operation demonstrated in vacuum; plasma load operation within 2× of requirement for industrial HV supplies) |

---

#### **Function 3: Instability Control**

**Physics risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Diocotron and electron cyclotron drift instabilities (ECDI) suppressed or tolerated at commercial density >10¹⁰ cm⁻³ without disrupting ion confinement |
| Best demonstrated | Instabilities "have not been directly observed in simulations of this device" (AIP Advances 2024), but flagged as concerns for higher-density operation |
| Gap ratio | N/A (instabilities uncharacterized experimentally) |
| Closure mechanism | E×B electron confinement geometry intrinsically stabilizes diocotron mode (per PIC simulations); ECDI mitigation at high density TBD |
| Classification | Binary (if ECDI disrupts ion confinement at required density, Q>1 is unachievable) |
| Evidence tier | 2 (simulation only: PIC simulations show stability in current parameter range, but experimental validation at fusion-relevant density is absent) |

**Hardware risk:**

| Field | Value |
|-------|-------|
| Plant requirement | HTS magnet coils (0.5 T) maintain field stability within ±1% under neutron irradiation (>10²⁰ n/m²) and plasma thermal transients for >5 FPY |
| Best demonstrated | Permanent magnets (0.05 T) operational in current prototypes (CWFest blog); HTS coil pair (0.5 T) is "long-lead equipment" (2026 press release); no HTS coil fabrication or testing reported |
| Gap ratio | 10× (current 0.05 T → target 0.5 T); neutron exposure untested |
| Closure mechanism | Industrial HTS coil technology at 0.5 T (low field by fusion standards); compact geometry simplifies coil design; neutron shielding reduces flux to coils |
| Classification | Degrading (HTS quench reduces E×B confinement, lowering fusion rate and Q; does not prevent restart if coil is replaced) |
| Evidence tier | 3 (subscale: 0.05 T operation demonstrated; 0.5 T HTS technology exists industrially but not fabricated/tested for Orbitron geometry) |

---

#### **Function 4: Plasma-Wall Interaction**

**Physics risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Cathode surface erosion from ion bombardment <1 mm/FPY to maintain 300 kV geometry within tolerances for >2 FPY |
| Best demonstrated | Cathode operation demonstrated at laboratory scale (AIP Advances 2024 device experiments); erosion rate under fusion-relevant ion flux unpublished |
| Gap ratio | N/A (erosion rate unpublished) |
| Closure mechanism | Tungsten cathode (refractory metal, high sputtering threshold); ion energies tuned to minimize sputtering yield via voltage control |
| Classification | Degrading (excessive erosion shortens cathode replacement cycle, increasing O&M; does not prevent net electricity if cathode is replaced more frequently) |
| Evidence tier | 3 (partial demonstration: cathode operation at kW-scale input validated; fusion-relevant ion flux erosion is uncharacterized) |

**Hardware risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Cathode material (tungsten or refractory alloy) withstands 14 MeV neutron displacement damage (>10 dpa) and maintains electrical integrity (no cracking, embrittlement, arc initiation) for >2 FPY |
| Best demonstrated | Tungsten cathodes in vacuum tube applications (TRL 9 for non-neutron environments); 14 MeV neutron damage to tungsten characterized in fission studies but not at 300 kV HV stress |
| Gap ratio | N/A (no Orbitron-specific neutron irradiation testing published) |
| Closure mechanism | Tungsten's high damage tolerance (used in tokamak divertors) + periodic cathode replacement as consumable (modeled as 2 FPY lifetime in baseline) |
| Classification | Degrading (neutron damage shortens cathode life, increasing replacement frequency and O&M cost; does not prevent operation with more frequent replacement) |
| Evidence tier | 3 (partial demonstration: tungsten neutron tolerance known from fission/tokamak data; HV+neutron combined stress is untested) |

---

#### **Function 5: Neutron/Particle Handling**

**Physics risk:**

| Field | Value |
|-------|-------|
| Plant requirement | 14 MeV neutron flux <10¹⁴ n/cm²/s at HTS coil locations (via shielding geometry) to limit radiation damage and activation |
| Best demonstrated | Neutron production confirmed (10¹¹ n/s target at Q≈1 operating point per CWFest blog; >10¹³ n/s capability per APS abstract); flux distribution uncharacterized |
| Gap ratio | N/A (neutron flux spatial distribution unpublished) |
| Closure mechanism | Compact shielding geometry (concrete + steel) surrounding each module or module array; neutronics modeling TBD |
| Classification | Degrading (excessive neutron flux to coils accelerates damage and activation, increasing maintenance cost; does not prevent operation with more shielding or faster coil replacement) |
| Evidence tier | 2 (simulation only: neutron production confirmed but spatial flux distribution and shielding effectiveness are unmodeled in public sources) |

**Hardware risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Neutron shielding (concrete + steel, ~30 cm thickness) attenuates 14 MeV neutron flux by >10³× without exceeding module volume/mass constraints for modular deployment |
| Best demonstrated | "Concrete castle" shielding for Marty prototype (CWFest blog); commercial neutron shielding technology is TRL 9 (fission reactors, neutron sources) |
| Gap ratio | N/A (per-module shielding geometry undefined) |
| Closure mechanism | Conventional neutron shielding materials (concrete, borated polyethylene, steel) scaled to compact module geometry |
| Classification | Degrading (insufficient shielding increases activation of BOP components, raising O&M and waste disposal cost; does not prevent operation) |
| Evidence tier | 4 (near-regime: fission-scale neutron shielding is mature; compact module geometry introduces integration challenges but no fundamental barrier) |

---

#### **Function 6: Fuel Cycle Closure**

**Physics risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Tritium breeding ratio TBR ≥ 1.05 (self-sufficient with 5% margin) for sustainable D-T operation without external tritium purchase |
| Best demonstrated | Never demonstrated (no breeding blanket exists); MoU with Fusion Fuel Cycles (FFC) covering breeding blanket R&D announced April 2025 |
| Gap ratio | N/A (no blanket design published) |
| Closure mechanism | Future breeding blanket design via FFC collaboration; geometry TBD (compact module scale is geometrically challenging for conventional lithium blanket) |
| Classification | Binary for long-term commercial operation (without TBR≥1.0, tritium cost scales inversely with Q and becomes prohibitive at low Q; purchased tritium at $35k/g contributes $57k/MWh at Q=10 baseline, scaling to infinity as Q→break-even) |
| Evidence tier | 1 (asserted: FFC MoU is a disclosed collaboration direction with no design, timeline, or technical specification) |

**Hardware risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Tritium extraction, purification, and recycling system achieves >95% fuel recovery and maintains <1 g inventory loss per FPY |
| Best demonstrated | FusionWERX facility (operational 2027) includes "integrated tritium management systems capable of extracting, purifying, and recycling tritium" (PRNewswire 2025); system design and performance unpublished |
| Gap ratio | N/A (tritium system performance unpublished) |
| Closure mechanism | FusionWERX tritium handling infrastructure (licensed facility with extraction/purification capability) provides near-term operational capability for research-scale D-T testing |
| Classification | Degrading (tritium loss increases fuel cost; >95% recovery is achievable with competent engineering per tokamak experience) |
| Evidence tier | 3 (subscale: tritium handling infrastructure confirmed at FusionWERX facility, but commercial-scale tritium system performance is uncharacterized) |

---

#### **Function 7: Power Conversion & BOP**

**Physics risk:**

| Field | Value |
|-------|-------|
| Plant requirement | N/A (no physics coupling to power conversion; this function is purely engineering) |
| Best demonstrated | N/A |
| Gap ratio | N/A |
| Closure mechanism | N/A |
| Classification | N/A |
| Evidence tier | 5 (no physics risk for this function; hardware risk dominates) |

**Hardware risk:**

| Field | Value |
|-------|-------|
| Plant requirement | Thermal-to-electric conversion achieves η≥25% at <1 MWe aggregate thermal power (multi-module plant) to reach LCOE ≤ $10k/MWh per model sensitivity |
| Best demonstrated | Thermoelectric conversion at kWe scale: η=5–15% (mature technology, TRL 7–8); small-scale ORC/Stirling: η=10–20% (TRL 6–7); steam turbines at >10 MWe: η=30–40% (TRL 9) |
| Gap ratio | ~2× (demonstrated η=10–15% at kWe scale → required η=25–30% at <1 MWe aggregate) |
| Closure mechanism | Multi-module thermal coupling to aggregate >1 MWe thermal output feeding conventional turbine cycle (plant architecture undefined); alternatively, advanced thermoelectric or thermionic conversion achieving η>20% at kWe scale (speculative) |
| Classification | Degrading (lower thermal efficiency reduces net power and increases LCOE; η=12% baseline yields $302k/MWh vs. η=30% yielding $13k/MWh at Q=10; does not prevent net electricity, only makes it more expensive) |
| Evidence tier | 3 (partial demonstration: thermoelectric and small ORC technology exist at kWe scale with η=10–15%; turbine arrays at MW scale exist with η=30%; the *integration* of modular kWe thermal sources into a turbine-fed plant is undemonstrated) |

---

### Function-level means (F1-F7)

| Function | Physics tier | Hardware tier | Mean |
|----------|--------------|---------------|------|
| F1: Plasma Performance | 3 | 3 | **3.0** |
| F2: Driver / Energy Input | 3 | 4 | **3.5** |
| F3: Instability Control | 2 | 3 | **2.5** |
| F4: Plasma-Wall Interaction | 3 | 3 | **3.0** |
| F5: Neutron/Particle Handling | 2 | 4 | **3.0** |
| F6: Fuel Cycle Closure | 1 | 3 | **2.0** |
| F7: Power Conversion & BOP | 5 (N/A) | 3 | **3.0** (using hardware only since physics N/A) |

Wait, for F7, since there's no physics risk, should I average (5 + 3)/2 = 4.0, or just use the hardware tier (3) as the function mean? Let me re-read the framework:

> After filling all 14 cells, compute the mean evidence tier for each function (average of physics and hardware subcategory tiers). Report as F1 through F7.

The instruction says "average of physics and hardware subcategory tiers." For F7, physics tier = 5 (N/A, no physics coupling), hardware tier = 3 → mean = (5+3)/2 = **4.0**.

Revised F7: **4.0**

---

### Binary risks

From the risk matrix, risks classified as "binary":

1. **Plasma Performance (physics)**: No net fusion without achieving required density-temperature-confinement triple product
2. **Instability Control (physics)**: If ECDI disrupts ion confinement at required density, Q>1 is unachievable
3. **Fuel Cycle Closure (physics)**: Without TBR≥1.0, tritium cost becomes prohibitive at low Q for long-term commercial operation

Note: I classified "Fuel Cycle Closure (physics)" as binary with the caveat "for long-term commercial operation." The framework's mandatory binary classifications include "TBR < 1.0 for any D-T concept," so this is correctly classified as binary.

---

### Heritage credit (D-T fuel)

The Orbitron uses D-T fuel but does **not** have good traceability to previous public fusion experiments:
- **Not a tokamak** (no ITER/JET heritage)
- **Not a stellarator** (no W7X/LHD heritage)
- **Not laser IFE** (no NIF/HYLIFE heritage)
- **Not a mirror** (no MFTF/TMX heritage; the magnetic field is auxiliary E×B confinement, not mirror confinement)
- **Not an FRC** (different confinement mechanism)
- **Not Z-pinch** (electrostatic, not pinch)

The Orbitron is an **electrostatic confinement** device. The closest heritage lineage is IEC fusors (Farnsworth-Hirsch), but these are generally regarded as non-viable for net power (dominated by Coulomb collisions, same critique leveled at Orbitron). There is no heritage credit lineage in the framework table for "electrostatic confinement."

**Heritage credit: NONE** (no applicable lineage)

**F1-F3 floors do not apply.**

---

### C7 Computation

Per framework:
> C7 = mean of F1-F7 (after heritage), rounded to nearest 0.5

F1-F7 means (no heritage credit applied):
- F1 = 3.0
- F2 = 3.5
- F3 = 2.5
- F4 = 3.0
- F5 = 3.0
- F6 = 2.0
- F7 = 4.0

Mean = (3.0 + 3.5 + 2.5 + 3.0 + 3.0 + 2.0 + 4.0) / 7 = 21.0 / 7 = **3.0**

**Function-level cap check**: Is any function mean ≤ 1.5? No (minimum is F6 = 2.0).

**C7 = 3.0** (no cap applied, no heritage credit)

---

### YAML scores block

```yaml
---
scores:
  C1: 5.0
  C3: 3.6
  C4: 3.8
  C5: 3.0
  C8: 2.3
  F1: 3.0
  F2: 3.5
  F3: 2.5
  F4: 3.0
  F5: 3.0
  F6: 2.0
  F7: 4.0
  binary_risks:
    - "Coulomb collision thermalization prevents Q>1: If experimental measurement confirms Lampe-Mannheimer (1998) critique that collision rates exceed fusion rates by 25-37× at required densities, net energy gain is unachievable regardless of engineering optimizations"
    - "Electron cyclotron drift instability (ECDI) disrupts ion confinement at commercial density >10¹⁰ cm⁻³: If ECDI cannot be suppressed at fusion-relevant density, required triple product for Q>1 is unattainable"
    - "Tritium breeding ratio <1.0: Without a breeding blanket achieving TBR≥1.05, purchased tritium cost at $35k/g scales inversely with Q and becomes LCOE-prohibitive at low Q (contributes $57k/MWh at Q=10, diverging to infinity as Q approaches break-even)"
---
```

---

### Scoring summary table

| Criterion | Score | Key Drivers |
|-----------|-------|-------------|
| **C1: Modularization** | 5.0 | 72% factory-manufactured modules; 1000 identical units; +1.0 repetition boost |
| **C3: Supply Chain Learning** | 3.6 | Cathode (26% cost) is fusion-specific (score 2); HV feedthrough sole-source; 40% of cost taps >$1B markets |
| **C4: Plant Complexity** | 3.8 | Moderate coupling (cryoplant single-point failure); 7 major subsystems >1% of capital |
| **C5: Customization Needs** | 3.0 | Air-cooled at module scale (score 4 thermal); D-T fuel burden (score 1 safety); scaled (4+1)/2 = 2.5 → 3.0 |
| **C8: Data Adequacy** | 2.3 | Almost exclusively company sources (score 2 diversity); 10 blocking LCOE gaps (score 1 coverage); FusionWERX provides near-term pathway (score 4 commercialization) |

---

### C7 Risk Matrix Summary

**Highest-risk functions:**
- **F6: Fuel Cycle Closure (2.0)** — No breeding blanket design exists; tritium cost is binary risk for long-term commercial operation
- **F3: Instability Control (2.5)** — ECDI flagged as concern for high-density operation; simulation-only stability assessment

**Lowest-risk function:**
- **F7: Power Conversion & BOP (4.0)** — Thermal conversion technology exists (thermoelectric, small turbines); integration challenge is engineering, not physics

**Binary risks** gate commercial viability: If Coulomb collision physics prevents Q>1, or if ECDI disrupts confinement at required density, or if no breeding blanket is developed, the concept cannot achieve commercial LCOE regardless of capital cost reductions.
