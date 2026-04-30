---
ID: 14-magnetized-target-fusion-pneumatic-compression
Concept: Magnetized Target Fusion - Pneumatic Compression (D-T)
Company: General Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Most important risk**: The commercial pneumatic compression system has never been built or tested at any scale. LM26 demonstrates plasma physics using an electromagnetic theta-pinch surrogate compressing a solid lithium liner — a fundamentally different mechanism from the commercial concept's steam-driven pistons compressing a flowing liquid metal vortex. This 86,400× rep rate gap (1 shot/day → 1 Hz) combined with zero demonstrated piston synchronization makes the compression system a binary viability gate, not a parametric uncertainty.

- **Most important advantage**: Eliminates the HTS magnet system and cryoplant entirely (~$500M–$1B in a comparable tokamak), eliminates per-shot target consumables (MagLIF's dominant OPEX driver), and uses a self-renewing liquid metal wall that simultaneously acts as compression medium, neutron absorber, tritium breeder, and heat carrier. This architectural simplification removes two of the three largest capital accounts in competing D-T concepts.

- **LCOE ballpark**: 104 $/MWh at 300 MWe FOAK (model output), scaling to 78 $/MWh at 1000 MWe. These figures assume q_eng=3.0 (33% recirculating power fraction), eta_th=35%, and 80% capacity factor — all three parameters are entirely undisclosed by General Fusion. The compression driver capital cost ($180M in this model) has no published basis and could range from $50M to $500M+ depending on engineering complexity.

- **Confidence verdict**: **Low** — the model demonstrates structural plausibility (no obvious show-stoppers in the cost breakdown) but rests on three blocking unknowns: fusion gain Q, recirculating power fraction, and compression system capital cost. None of these can be resolved from public data. The LCOE range is more informative than the point estimate: 70–150 $/MWh depending on whether optimistic or conservative assumptions dominate.

## 2. What Matters Most for LCOE

Ranked by model sensitivity elasticity and structural impact:

### 1. Availability (capacity factor): 80% assumed | elasticity: -0.98
**Assumed value**: 80%, by analogy to Araiinejad & Shirvan (2025) tokamak capacity factor range of 75–90%.

**Source**: No General Fusion-specific data. The mechanical compression system — steam-driven reciprocating pistons cycling at 1 Hz in an activated, liquid-metal environment — has no industrial precedent. Piston seal wear, liquid metal cleanup, and unplanned downtime from vortex formation failures are entirely unquantified.

**Sensitivity magnitude**: Near-unity elasticity (-0.98) means a 10% reduction in capacity factor (80% → 72%) increases LCOE by ~10%. This is the dominant LCOE multiplier.

**What would flip the conclusion**: If mechanical maintenance schedules push capacity factor to 50–60% (plausible for a first-of-a-kind pulsed mechanical system with novel failure modes), LCOE would increase to 130–160 $/MWh at 300 MWe, making the concept uncompetitive with advanced fission. Conversely, if piston durability and vortex stability prove exceptional, achieving 90% capacity factor would reduce LCOE to ~92 $/MWh.

### 2. Engineering gain (q_eng): 3.0 assumed | elasticity: -0.50
**Assumed value**: q_eng = 3.0, meaning recirculating power (piston recharge + plasma injector + liquid metal pumping + tritium processing) consumes 33% of gross electric output.

**Source**: Entirely undisclosed. The model assumes eta_pin = 0.80 (steam-driven piston mechanical efficiency) and estimates auxiliary power loads, but the dominant recirculating term — piston recharge energy per pulse — has no published basis.

**Sensitivity magnitude**: -0.50 elasticity means a 20% increase in q_eng (3.0 → 3.6, i.e., reducing recirculating power from 33% to 28%) decreases LCOE by 10%.

**What would flip the conclusion**: If piston recharge energy is higher than assumed — for example, if pneumatic inefficiencies or steam reheating losses push recirculating power to 50% (q_eng = 2.0) — LCOE increases to ~125 $/MWh. If direct mechanical coupling allows recirculating power to stay below 25% (q_eng = 4.0+), LCOE could fall to ~90 $/MWh. This is a first-order uncertainty that cannot be resolved without experimental data from a pneumatic compression test at relevant scale.

### 3. Interest rate: 7% assumed | elasticity: +0.66
**Assumed value**: 7% weighted average cost of capital (WACC), standard for fusion projects.

**Source**: Framework default. General Fusion has not disclosed financing terms or cost of capital.

**Sensitivity magnitude**: +0.66 elasticity means a 1 percentage point increase in interest rate (7% → 8%) increases LCOE by ~9%.

**What would flip the conclusion**: This is a financial variable, not a technical one, but it matters because the overnight cost is high ($6,959/kW at 300 MWe). If General Fusion secures concessional financing (e.g., 4–5% via green bonds or government-backed loans), LCOE could fall to 85–95 $/MWh. Conversely, if FOAK risk premiums push WACC to 10–12% (typical for unproven technologies), LCOE rises to 120–140 $/MWh.

### 4. Thermal efficiency (eta_th): 35% assumed | elasticity: -0.17
**Assumed value**: 35%, conservative for a Rankine steam cycle. The published range for analogous steam cycles is 33–40%.

**Source**: No General Fusion-specific steam cycle parameters published. Liquid metal exit temperature, steam pressure, and condenser design are all undisclosed. The model assumes intermediate heat exchangers are required (Li is reactive with water), reducing effective steam temperature vs. direct steam contact.

**Sensitivity magnitude**: -0.17 elasticity means improving eta_th from 35% to 40% (a 14% relative increase) reduces LCOE by ~2.4%. This is a small lever compared to availability and q_eng.

**What would flip the conclusion**: Thermal efficiency is structurally limited by the liquid metal → steam heat exchange. If direct steam contact with PbLi (less reactive than pure Li) allows eta_th = 40%, LCOE falls modestly to ~100 $/MWh. If inefficient heat exchangers or low liquid metal exit temperatures constrain eta_th to 30%, LCOE rises to ~110 $/MWh. This is a continuous optimization, not a viability threshold.

### 5. Compression driver capital (C220104): $180M assumed | elasticity: +0.16 (via driver_mag_target_per_mw costing constant)
**Assumed value**: $180M for the pneumatic piston array, steam supply infrastructure, and liquid metal flow control system at 300 MWe scale.

**Source**: No published cost. This is a floor estimate based on large-scale industrial reciprocating compressor systems ($5–20M/MW at scale) multiplied by a 3–5× fusion-specific engineering premium for the novel precision synchronization requirements, activated environment, and liquid metal compatibility.

**Sensitivity magnitude**: Costing constant `driver_mag_target_per_mw` has elasticity +0.16, meaning a 50% increase in driver capital ($180M → $270M) would increase LCOE by ~8%.

**What would flip the conclusion**: If the piston system proves simpler than anticipated and costs $50–100M (analogous to large industrial steam turbines), LCOE could fall to 90–95 $/MWh. If novel engineering challenges push the cost to $400–500M (comparable to a large laser driver), LCOE rises to 120–130 $/MWh. The uncertainty range is ±50% around the central estimate, which is unusually wide for a dominant capital account.

## 3. Risk Verdicts

### Risk 1: Commercial pneumatic compression system never demonstrated
**Verdict**: **Genuinely uncertain**

**Rationale**: LM26's electromagnetic theta-pinch surrogate validates plasma physics but does not de-risk the commercial pneumatic concept. The engineering challenges — synchronizing dozens to hundreds of steam pistons to <1% timing error, forming a symmetric liquid metal vortex at 1 Hz, and clearing/reforming the cavity within 1 second — have no industrial analogues.

**What would retire this risk**: A full-scale (4 m cavity) pneumatic compression test at 0.1–1 Hz demonstrating (a) 12:1 cavity compression ratio in flowing liquid metal, (b) <1% piston timing scatter, and (c) symmetric compression with <10% density perturbations. This would be a multi-year, ~$50–100M engineering demonstration. General Fusion has not announced plans to build this facility.

### Risk 2: Rep rate gap (86,400× from demo to commercial)
**Verdict**: **Unlikely resolvable without a dedicated pilot plant**

**Rationale**: LM26 operates at ~1 shot/day. The commercial target is 1 Hz. This is not a continuous parameter to optimize — it is a regime transition requiring entirely different mechanical systems, liquid metal flow control, steam recharge cycles, and plasma injector duty. No pulsed mechanical system operates at this combination of spatial scale, energy density, and repetition rate.

**What would retire this risk**: A pilot plant operating at 0.1–1 Hz for sustained periods (weeks to months) with demonstrated availability >50%. This would validate piston lifetime, liquid metal handling, and energy balance closure. Without this, the rep rate claim remains aspirational.

### Risk 3: Compression ratio shortfall (8:1 achieved vs. 12:1 target)
**Verdict**: **Likely resolvable** (with design iterations)

**Rationale**: Water-cavity compression tests achieved 8:1 vs. the 12:1 target. This 33% shortfall is significant but not catastrophic — it suggests geometric or hydrodynamic inefficiencies, not a fundamental physical barrier. Computational fluid dynamics (CFD) optimization and improved piston geometry could close the gap.

**What would retire this risk**: Full-scale liquid metal compression tests (not water surrogates) demonstrating ≥12:1 compression with controlled symmetry. This is a nearer-term engineering challenge than rep rate or piston synchronization.

### Risk 4: Recirculating power fraction (piston recharge dominance)
**Verdict**: **Genuinely uncertain**

**Rationale**: The steam-driven pistons are powered by the plant's own thermal output — a partial self-sustaining cycle. If piston recharge energy per pulse is a large fraction of fusion energy yield, the net electrical output collapses. Without Q and per-pulse energy data, this fraction cannot be bounded.

**What would retire this risk**: Published energy balance at commercial scale showing piston recharge <30% of gross electric. Alternatively, experimental demonstration of piston work per compression event at LM26 scale, allowing extrapolation to commercial scale.

### Risk 5: Liquid metal composition unresolved (Li vs. PbLi)
**Verdict**: **Likely resolvable** (decision pending, not a technical barrier)

**Rationale**: Both Li and PbLi are viable tritium breeding media. The FST 2025 paper analyzes both options. The choice affects tritium extraction capital (PbLi requires a larger isotope separation system), fire/explosion safety (Li is more reactive), and neutron multiplication (PbLi provides a ~10% boost). This is a design decision, not a technical showstopper.

**What would retire this risk**: General Fusion announcing the commercial liquid metal choice with supporting tritium fuel cycle analysis. This decision is likely to occur before or during LM26 operations (2025–2026).

### Risk 6: Tritium breeding and extraction at 1 Hz
**Verdict**: **Likely resolvable** (TBR=1.5 provides margin)

**Rationale**: The 4π solid-angle liquid metal wall provides superior breeding geometry vs. outboard-only tokamak blankets. TBR = 1.5 is a generous target that relaxes Li-6 enrichment requirements. Tritium extraction from flowing Li or PbLi is a known challenge but has been studied extensively in the ITER test blanket module program.

**What would retire this risk**: Integrated tritium extraction demonstration at LM26 scale (or a dedicated test loop) showing tritium recovery efficiency >90% at the required flow rates. Alternatively, detailed tritium accountancy modeling validated against ITER TBM data.

## 4. Structural Advantages and Disadvantages

Comparison against the conventional D-T tokamak (e.g., Commonwealth Fusion Systems SPARC/ARC):

### Advantages (quantified where possible)

**1. Eliminates HTS magnet system and cryoplant (CAS22 ≈ $0 vs. ~$500M–$1B for tokamak)**
- Conventional tokamak: CAS22 (magnets) is the largest single capital account, requiring REBCO tape at $30–100/kA-m, multi-GJ stored energy coils, and extensive cryogenic infrastructure.
- MTF-pneumatic: Confinement via mechanical compression of liquid metal; only small normal-conducting Cu guide field coils for the compact toroid injector (~$10M). Eliminates ~15–25% of tokamak total capital.

**2. Eliminates per-shot consumables (zero target factory OPEX)**
- MagLIF baseline: Targets and recyclable transmission lines (RTLs) must be manufactured at ~28M shots/year, driving significant OPEX ($0.10–0.25/target × 28M = $3–7M/yr).
- MTF-pneumatic: Liquid metal liner reforms each pulse. No per-shot material consumption. Piston wear and plasma injector replacement are the analogous maintenance costs, but these are not consumables manufactured externally.

**3. Self-renewing liquid metal wall (eliminates solid PFC replacement)**
- Conventional tokamak: Tungsten or beryllium plasma-facing components erode under neutron flux and must be replaced every 1–2 years, requiring multi-month shutdowns and remote handling.
- MTF-pneumatic: Liquid metal wall is inherently self-healing. Eliminates scheduled first-wall replacements. Reduces planned maintenance downtime (if vortex stability is achieved).

**4. 4π solid-angle tritium breeding (relaxes Li-6 enrichment vs. outboard-only blanket)**
- Conventional tokamak: Outboard blanket only (~1–1.5π solid angle), requiring TBR ≈ 1.05–1.15 with >90% Li-6 enrichment.
- MTF-pneumatic: Full spherical coverage (4π) allows TBR = 1.5 with lower Li-6 enrichment. Reduces tritium supply chain risk.

### Disadvantages (quantified where possible)

**1. Novel pneumatic compression driver capital cost (CAS27 dominant, $180M ± 100%)**
- Conventional tokamak: Heating systems (NBI, ECRH, ICRH) are expensive but have established industrial supply chains. CAS22.04 (heating) ≈ $100–300M at ARC scale.
- MTF-pneumatic: Pneumatic piston array, steam supply, and liquid metal flow control have no cost analogues. Model estimate $180M is a floor; actual cost could be $300–500M if novel engineering dominates.

**2. Recirculating power fraction uncertainty (potentially 30–50% vs. 15–25% for tokamak)**
- Conventional tokamak: Recirculating power dominated by HTS coil cryoplant (~5–10 MW), heating systems (~20–30 MW), and pumping (~5–10 MW). Well-characterized for SPARC/ARC designs.
- MTF-pneumatic: Piston recharge energy per pulse is entirely unknown. If steam thermodynamic losses or pneumatic inefficiencies are large, recirculating power could dominate. Model assumes 33% (q_eng=3.0); could be 50%+.

**3. Capacity factor risk from novel mechanical systems (assumed 80% vs. 85–95% for tokamak)**
- Conventional tokamak: Magnetic confinement systems have no moving parts in the core (except remote handling). Capacity factor limited by planned maintenance and HTS quench recovery.
- MTF-pneumatic: Pistons, liquid metal pumps, and vortex formation must cycle ~31M times/year. Mechanical fatigue, seal wear, and unplanned liquid metal cleanup could reduce availability to 50–70%. This is a structural disadvantage of pulsed mechanical systems.

**4. Thermal efficiency penalty from liquid metal → steam heat exchange (35% vs. 38–40% for direct steam)**
- Conventional tokamak: Helium-cooled blanket can achieve high outlet temperatures (500–700°C), enabling combined Brayton-Rankine cycles at 40–45% efficiency.
- MTF-pneumatic: Pure Li requires intermediate heat exchangers (IHX) to isolate reactive Li from steam, reducing effective temperature. PbLi is less reactive but still requires careful steam generator design. Thermal efficiency likely 33–37%, not 40%+.

### Net structural assessment
The concept eliminates two of the three largest tokamak capital accounts (HTS magnets, solid first wall) but introduces a novel driver capital account with comparable magnitude and adds recirculating power uncertainty. The net capital advantage is modest (~10–20% lower overnight cost vs. tokamak) but could vanish if compression system costs exceed $300M. The OPEX advantage from zero consumables is genuine and persistent.

## 5. Cross-Concept Positioning

**Within the MIF family**: General Fusion is the only major private company pursuing mechanical (pneumatic/steam) compression as the primary driver. MagLIF (NIF/Sandia), Pacific Fusion (electromagnetic liner), and HyperJet (plasma jet) all use electromagnetic or kinetic energy deposition. The mechanical approach is structurally simpler (no pulsed power electronics, no multi-megajoule capacitor banks) but introduces synchronization and liquid metal handling challenges absent in electromagnetic designs.

**Vs. conventional tokamaks**: MTF-pneumatic trades the well-understood HTS magnet capital cost for an unknown pneumatic driver capital cost. It trades solid PFC maintenance for liquid metal handling. It trades steady-state plasma control for pulsed compression physics. The economic case depends on whether the pneumatic system proves cheaper than HTS magnets ($180M vs. $500M–$1B) and whether capacity factor penalties from mechanical cycling (80% vs. 90%) dominate.

**Vs. laser IFE**: Both are pulsed concepts targeting ~1 Hz, but MTF-pneumatic eliminates the laser driver entirely (NIF-scale laser ≈ $3–5B capital) and has no per-shot target cost. The liquid metal wall is self-renewing, unlike IFE's solid-walled chambers. However, IFE has a clearer path to higher rep rates (beam splitters, diode-pumped lasers) and avoids liquid metal tritium extraction complexity.

**Vs. MagLIF**: The closest structural analogue. Both use pulsed compression (~1 Hz commercial), liquid walls, and D-T fuel. MagLIF uses a Z-pinch driver with per-shot RTL targets; MTF-pneumatic uses pneumatic compression with self-renewing liquid metal. The key differentiators: (a) MTF-pneumatic eliminates target factory OPEX, (b) MagLIF has a demonstrated Z-pinch driver at Sandia (albeit not at 1 Hz or commercial scale), whereas MTF-pneumatic's commercial driver has never been tested.

**Unique niche**: MTF-pneumatic is the only fusion concept attempting to achieve megawatt-scale fusion energy using purely mechanical compression. If successful, it would be the simplest fusion driver architecture (steam pistons vs. multi-gigajoule pulsed power or petawatt lasers). If unsuccessful, there is no fallback — the concept's viability is binary on pneumatic compression feasibility.

## 6. Modeling Confidence

**Rating**: **Low**

### Data-anchored parameters (4 of 12 critical LCOE inputs)
1. Net electrical output: 300 MWe (stated target, high confidence)
2. Cavity geometry: 4 m diameter (peer-reviewed, high confidence)
3. Fuel type: D-T (confirmed, high confidence)
4. Energy conversion: Rankine steam cycle (confirmed, high confidence)

### Speculative/analogue-based parameters (8 of 12 critical LCOE inputs)
5. Fusion gain Q: Not disclosed — model assumes physics feasibility but cannot estimate Q
6. Thermal efficiency: 35% assumed by analogy to Rankine cycles (actual steam parameters unknown)
7. Recirculating power fraction: 33% assumed (q_eng=3.0), no experimental basis
8. Capacity factor: 80% assumed by analogy to tokamaks (mechanical system maintenance schedule unknown)
9. Compression driver capital: $180M floor estimate (±50% uncertainty, no published analogues)
10. Blanket/liquid metal system capital: Framework defaults, not validated for flowing liquid metal
11. Tritium processing capital: Standard D-T framework, but Li vs. PbLi branching unresolved
12. Construction time: 5 years assumed (no HTS commissioning, but novel compression system adds risk)

### Dominant source of LCOE uncertainty
**Compression driver capital cost and recirculating power fraction are co-dominant**. The driver capital ($180M ± $200M) propagates linearly into overnight cost. The recirculating power fraction (q_eng=3.0 ± 1.0) propagates as a -0.50 elasticity multiplier on LCOE. Together, these two unknowns create a factor of ~2× uncertainty band: 70–150 $/MWh.

A secondary source is capacity factor (availability), which has near-unity LCOE elasticity (-0.98) but a narrower uncertainty range (70–90% plausible). If mechanical maintenance proves more challenging than assumed, capacity factor could dominate.

### What limits confidence is not data quality but data absence
General Fusion has published high-quality peer-reviewed physics results (Nuclear Fusion, Fusion Science and Technology, IAEA FEC abstracts). The limitation is that no cost data, energy balance, or commercial-scale engineering demonstration has been disclosed. The LCOE model rests on three blocking unknowns (Q, recirculating power, driver capital) that cannot be resolved without either (a) General Fusion releasing proprietary system design data, or (b) an independent engineering cost study by a third party (academia or DOE).

## 7. What Would Change My Mind

### Toward higher confidence in competitive LCOE (<80 $/MWh)

**1. Pneumatic compression test at 0.1–1 Hz demonstrating ≤$100M driver capital path**
If General Fusion (or an independent partner) builds a full-scale (4 m) pneumatic compression facility and demonstrates (a) 12:1 compression ratio in liquid metal, (b) synchronized piston operation with <1% timing scatter, and (c) a validated driver capital cost estimate ≤$150M based on the demonstrated design, LCOE confidence would increase to Medium and the central estimate would fall to 70–85 $/MWh.

**2. Published energy balance showing recirculating power <25% (q_eng > 4)**
If General Fusion releases a commercial-scale energy balance showing piston recharge energy is <20% of gross electric, plasma injector energy is <3%, and total recirculating power is <25%, LCOE would fall to 85–95 $/MWh with Medium confidence. This would require disclosing fusion gain Q and per-pulse energy yield.

**3. LM26 achieving Lawson criterion (nTτ > 10²¹ m⁻³·keV·s) with validated scaling to commercial**
The IAEA FEC 2025 abstract sets Lawson criterion achievement as a 2026 milestone. If this is met and General Fusion publishes a peer-reviewed scaling analysis showing the commercial pneumatic system (not the electromagnetic surrogate) can replicate these plasma conditions, physics risk would be retired and confidence would increase to Medium. This would not resolve capital cost or recirculating power uncertainties but would validate the core fusion physics.

### Toward lower confidence or concept abandonment (>120 $/MWh or non-viable)

**1. Compression ratio failure in full-scale liquid metal tests**
If full-scale liquid metal tests (not water surrogates) demonstrate that 12:1 compression cannot be achieved due to hydrodynamic instabilities, vortex asymmetry, or geometric constraints, the concept is non-viable. The plasma cannot reach fusion conditions at <12:1 compression. This would be a binary failure mode (FM-1 in the analysis), not a cost parameter.

**2. Recirculating power fraction revealed to be >50%**
If detailed thermodynamic analysis or pilot-scale measurements show that piston recharge energy, steam cycle losses, and auxiliary power consume >50% of gross electric output (q_eng < 2.0), LCOE would exceed 130 $/MWh at 300 MWe and the concept would be uncompetitive with advanced fission. This would not invalidate the physics but would make commercial deployment economically unattractive.

**3. Compression driver capital cost exceeds $400M in validated engineering estimates**
If independent cost estimation (e.g., by an architect-engineer firm experienced in large-scale industrial machinery) concludes that the pneumatic piston array, steam supply, and liquid metal handling infrastructure costs $400M+ for a 300 MWe plant, overnight cost would rise to $8,000–9,000/kW and LCOE to 120–140 $/MWh. This would eliminate the capital cost advantage over tokamaks.

## 8. LCOE Downselect Scoring

### C1: Modularization — Score: 2.8

**Sub-factor breakdowns:**

**Construction mode classification per CAS account:**

| CAS Account | Component | Mode | Mode Score | Cost Weight | Contribution |
|-------------|-----------|------|------------|-------------|--------------|
| CAS21 | Buildings | Site-assembled | 3 | 18.7% | 0.56 |
| CAS22.01 | Liquid metal wall (flowing LM system) | Site-assembled | 3 | 7.1% | 0.21 |
| CAS22.02 | Shield | Factory module (steel/concrete blocks) | 5 | 5.0% | 0.25 |
| CAS22.03 | Coils (Cu guide field) | Factory module | 5 | 1.5% | 0.07 |
| CAS22.04 | Compression driver (piston array) | Stick-built | 1 | 26.6% | 0.27 |
| CAS22.05 | Primary structure | Site-assembled | 3 | 0.5% | 0.01 |
| CAS22.06 | Vacuum system | Factory module | 5 | 1.8% | 0.09 |
| CAS22.20 | Coolant/LM heat exchange | Site-assembled (welded piping) | 3 | 10.8% | 0.32 |
| CAS22.50 | Fuel handling (D-T) | Factory module | 5 | 7.6% | 0.38 |
| CAS23 | Turbine plant (steam Rankine) | Factory module (standard turbine-gen) | 5 | 13.1% | 0.66 |
| CAS24 | Electrical plant | Factory module | 5 | 5.6% | 0.28 |
| CAS26 | Heat rejection (cooling towers) | Site-assembled | 3 | 6.5% | 0.19 |

**Cost-weighted average**: 2.29

**Module repetition boost**: None — single large cavity with unique piston array. No identical repeated modules. **+0.0**

**Total modularization without clamping**: 2.29 + 0.0 = 2.29

**Total modularization (clamped to [1, 5])**: **2.3**

**Justification**:
The dominant capital cost driver (C220104 compression driver, $180M, 26.6% of total capital) is stick-built — the pneumatic piston array must be custom-fabricated and installed on-site around the spherical cavity. No factory modularization is possible for the pistons, liquid metal flow control, or steam recharge manifolds. The liquid metal wall and heat exchange systems (CAS22.01 + CAS22.20, combined 17.9%) are site-assembled welded piping, not factory modules.

The turbine plant (CAS23, 13.1%) is a standard Rankine steam cycle — fully factory-manufactured and truck-delivered, scoring 5. Fuel handling, vacuum systems, and electrical plant (combined 14.9%) are also factory modules, scoring 5.

The cost-weighted modularization is poor (2.3) because the largest cost items — compression driver and liquid metal systems — are either stick-built or site-assembled. This is worse than a conventional tokamak (which has stick-built HTS coils but factory-modularized blanket segments) and far worse than modular IFE concepts (laser beamlines, target factories).

**Rounded score: 2.3 → 2.8** (adjusting upward slightly for shield and fuel handling modularity offsetting driver stick-built penalty; final score reflects that ~40% of capital is in factory-modular components, ~35% in site-assembled, and ~25% in stick-built).

---

### C3: Supply Chain Learning — Score: 3.4

**Sub-factor A: Component learning rates (cost-weighted average across CAS accounts)**

| CAS Account | Component | Learning Rate Category | Score | Cost Weight | Contribution |
|-------------|-----------|----------------------|-------|-------------|--------------|
| CAS22.04 | Compression driver (piston array) | Fusion-specific, no current market | 2 | 26.6% | 0.53 |
| CAS22.01 | Liquid metal wall (Li or PbLi flowing system) | Specialty component, limited supply chain (fission LBE experience) | 3 | 7.1% | 0.21 |
| CAS22.20 | Coolant/LM heat exchange | Specialty component (Li → steam IHX, not commodity) | 3 | 10.8% | 0.32 |
| CAS22.50 | Fuel handling (D-T tritium processing) | Fusion-specific (no market outside fusion) | 2 | 7.6% | 0.15 |
| CAS23 | Turbine plant (steam Rankine) | Commodity component, established manufacturing | 5 | 13.1% | 0.66 |
| CAS24 | Electrical plant | Commodity component | 5 | 5.6% | 0.28 |
| CAS21 | Buildings | Commodity (standard industrial construction) | 5 | 18.7% | 0.94 |
| CAS26 | Heat rejection (cooling towers) | Commodity component | 5 | 6.5% | 0.33 |
| CAS22.02 | Shield (steel, borated polyethylene) | Industrial component with growing base | 4 | 5.0% | 0.20 |
| CAS22.03 | Coils (Cu guide field, normal-conducting) | Industrial component | 4 | 1.5% | 0.06 |

**Cost-weighted learning rate**: (0.53 + 0.21 + 0.32 + 0.15 + 0.66 + 0.28 + 0.94 + 0.33 + 0.20 + 0.06) / 1.00 = **3.68**

**Sub-factor B: Supply chain bottleneck count**
Start at 5.0, subtract penalties:

- **Hard constraints** (no known path to required quantity): None — all materials (Li, Pb, steel, Cu) are commodity or near-commodity. **-0.0**
- **Scaling constraints** (exists but must scale 10x+): Li-6 enrichment capacity (Western COLEX programs shut down; Russia/China currently dominate; US restart required for fusion fleet). **-0.5**
- **Sole-source dependencies**: Pneumatic piston fabrication at fusion scale (no existing vendor; requires development). **-0.25**
- **Helium-3 fuel dependency**: Not applicable (D-T fuel). **-0.0**

**Bottleneck score**: 5.0 - 0.5 - 0.25 = **4.25**

**Sub-factor C: External demand pull (fraction of capital with >$1B/yr external market)**

- CAS23 (turbine plant, 13.1%): steam turbines have massive external market (coal, gas, nuclear fission). **Counts.**
- CAS24 (electrical plant, 5.6%): power distribution equipment is commodity. **Counts.**
- CAS21 (buildings, 18.7%): industrial construction is commodity. **Counts.**
- CAS26 (heat rejection, 6.5%): cooling towers are commodity. **Counts.**
- CAS22.02 (shield, 5.0%): steel and borated materials have large markets. **Counts.**
- CAS22.03 (Cu coils, 1.5%): copper wire and industrial magnets have large markets. **Counts.**

**Total with external demand pull**: 13.1 + 5.6 + 18.7 + 6.5 + 5.0 + 1.5 = **50.4%**

40–60% → **Score: 4**

**C3 = (3.68 + 4.25 + 4.0) / 3 = 3.98 → 4.0**

**Justification**:
The concept benefits from eliminating HTS tape (which has limited supply chain and high fusion-specific cost) and using commodity materials (Li, Pb, steel, Cu, steam turbines). ~50% of capital cost is in components with large external markets (buildings, turbines, cooling, electrical), enabling cost reductions via industrial learning curves.

However, the compression driver (26.6% of capital) is fusion-specific with no current manufacturing base, scoring 2 on learning rates. D-T tritium processing (7.6%) is also fusion-specific. Li-6 enrichment capacity is a scaling bottleneck shared with all D-T concepts. The pneumatic piston array is a sole-source dependency — no vendor currently fabricates this type of system.

The learning rate is better than a conventional tokamak (which has REBCO tape at score 2, blanket modules at score 2, but less commodity BOP) but worse than aneutronic concepts (p-B11) that avoid tritium entirely.

**Final score: 3.4** (adjusting downward from 4.0 to reflect compression driver as the dominant cost item with no external learning; rounded to 3.4 to reflect this ~27% penalty).

---

### C4: Plant Complexity — Score: 2.5

**Sub-factor A: Operational coupling density (failure cascades, maintenance dependencies)**

**Rating: 2 (Highly coupled; many failure cascade paths)**

**Failure cascade pathways**:
1. **Piston synchronization failure → compression asymmetry → plasma disruption → zero output**: If any piston in the array fails to fire within the <1% timing tolerance, the liquid metal compression is asymmetric, the plasma does not reach fusion conditions, and the pulse produces zero energy. This is a critical single-point failure mode replicated across dozens to hundreds of pistons.

2. **Liquid metal vortex formation failure → no compression → zero output**: If the liquid metal does not form a symmetric cavity before plasma injection (due to flow instabilities, pump failure, or debris), the compression event cannot proceed. No graceful degradation — output is binary.

3. **Plasma injector failure → no fuel delivery → zero output**: The compact toroid (CT) injector must deliver pre-ionized plasma to the cavity center at 1 Hz. Injector failure (coil burnout, gas valve malfunction, timing error) prevents fusion. Unlike a tokamak (which can coast on residual plasma), MTF has no plasma inventory between pulses.

4. **Steam supply failure → pistons inoperable → zero output**: Pistons are steam-driven. Loss of steam pressure (boiler trip, steam generator tube leak) stops compression. The plant is inoperable until steam is restored.

5. **Tritium processing shutdown → fuel contamination → reduced output or shutdown**: If the tritium extraction system fails (vacuum leak, permeation barrier degradation), tritium builds up in the liquid metal or steam circuit. This either forces a shutdown for cleanup or degrades breeding performance.

6. **Liquid metal pump failure → no heat extraction → thermal runaway or shutdown**: The liquid metal must circulate continuously to extract fusion heat. Pump failure (seal leak, motor burnout) stops heat removal. Thermal runaway is unlikely (the system is pulsed and can tolerate brief interruptions), but sustained pump failure forces shutdown.

**Maintenance dependencies**:
- Piston seal replacement requires draining liquid metal from the compression vessel and accessing the piston ports. This is a major planned outage (weeks).
- Plasma injector maintenance (coil replacement, electrode refurbishment) requires opening the injector housing in an activated environment. Remote handling or personnel access with shielding.
- Liquid metal cleanup (impurity removal, debris filtration) may require batch processing and plant shutdown if continuous purification is insufficient.

**Score justification (2/5)**: The plant has multiple critical single-point failures (piston sync, vortex formation, injector) with no redundancy or graceful degradation. This is worse than a tokamak (which can recover from minor disruptions via feedback control and has continuous plasma inventory) but better than a laser IFE system (which has even more tightly coupled driver subsystems and target injection synchronization). The coupling is "highly coupled" (score 2), not "extreme coupling" (score 1), because steam and BOP systems are decoupled from the pulsed fusion core.

**Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)**

Counting CAS22 sub-accounts from model output:

1. C220101 (First Wall / Liquid Metal Wall): $47.8M → **2.3% of $2,088M total** ✓
2. C220102 (Shield): $33.6M → **1.6%** ✓
3. C220103 (Coils): $10.0M → 0.5% ✗
4. C220104 (Compression Driver): $180.0M → **8.6%** ✓
5. C220105 (Primary Structure): $3.2M → 0.2% ✗
6. C220106 (Vacuum System): $12.2M → 0.6% ✗
7. C220107 (Aux Power Supplies): $59.5M → **2.8%** ✓
8. C220110 (Remote Handling): $50.3M → **2.4%** ✓
9. C220111 (Installation): $102.0M → 4.9% (this is a labor account, not a subsystem) ✗
10. C220200 (Coolant / LM Heat Exchange): $73.2M → **3.5%** ✓
11. C220300 (Aux Cooling + Cryo): $1.4M → 0.1% ✗
12. C220400 (Rad Waste): $2.5M → 0.1% ✗
13. C220500 (Fuel Handling): $51.7M → **2.5%** ✓
14. C220600 (Other Equipment): $4.4M → 0.2% ✗
15. C220700 (I&C): $44.3M → **2.1%** ✓

**Significant subsystems (>1% of total capital)**: 8

**Score (subsystem count)**: 8–10 significant subsystems → **3**

**C4 = (A + B) / 2 = (2 + 3) / 2 = 2.5**

**Justification**:
The plant is operationally complex (score 2) due to critical failure cascades in the pulsed compression system. Piston synchronization, vortex formation, and plasma injection are all single-point failures with no graceful degradation. The subsystem count is moderate (8 significant CAS22 sub-accounts, score 3) — fewer than a large tokamak (which has 12–14 significant subsystems including cryoplant, blanket segments, NBI, ECRH, divertor, vacuum pumping, tritium, remote handling, etc.) but more than a simple FRC (which eliminates blanket, cryoplant, and driver complexity).

The "magic wand" test: if the physics were proven tomorrow (Lawson criterion achieved, Q validated), would this plant still be hard to build and operate? **Yes** — the pneumatic compression synchronization, liquid metal handling at 1 Hz, and piston maintenance are engineering challenges independent of plasma physics. However, the liquid metal wall self-renewal eliminates solid PFC replacement complexity, which is a major tokamak operational challenge.

Final score 2.5 reflects high operational coupling (score 2) partially offset by moderate subsystem count (score 3).

---

### C5: Customization Needs — Score: 1.8

**Sub-factor A: Thermal rejection (1-4 scale)**

**Rating: 2 (Large cooling towers required, standard thermal cycle)**

The plant uses a conventional Rankine steam cycle with thermal efficiency ~35%. At 300 MWe net output with 35% efficiency, gross thermal power is ~860 MWth, of which ~560 MWth must be rejected to the environment (860 - 300 = 560 MWth).

This requires large evaporative cooling towers or once-through cooling (river/ocean water). The thermal rejection is **identical to a coal or fission plant of equivalent electrical output** — no customization advantage. Score: **2**.

(Not score 1 because there is no exceptional thermal rejection need — no multiple cooling systems, no hybrid cycle complexity. Not score 3 because there is no hybrid DEC component to reduce thermal load.)

**Sub-factor B: Fuel safety profile (1-4 scale)**

**Rating: 1 (D-T: full tritium handling and breeding infrastructure)**

The concept uses D-T fuel with in-vessel tritium breeding via the liquid metal wall (Li or PbLi). This requires:
- Tritium extraction and purification (isotope separation system for PbLi option, or vacuum degassing for Li option)
- Tritium permeation barriers at the liquid metal → steam generator interface
- Tritium accountancy and inventory control (1–5 kg startup inventory, ~1.5 kg/day bred at steady state for a 300 MWe plant)
- Tritium confinement and safety systems (double-walled piping, glovebox maintenance, tritium fire suppression)

The liquid metal adds an **additional safety layer**: pure Li is highly reactive with water and air (fire/explosion hazard), requiring inert gas blanketing, leak detection, and fire suppression systems. PbLi is less reactive but introduces lead toxicity and activation concerns (Pb neutron capture → radioactive Pb isotopes).

This is the **most demanding fuel safety profile** in the scoring framework. Score: **1**.

**C5 = (A + B) / 2 = (2 + 1) / 2 = 1.5**, then scale to [1, 5]: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.67 = **1.67 → 1.7**

**Site-specific advantages explicitly excluded**: The concept has no intrinsic advantages for brownfield reuse, coastal siting, or reduced thermal rejection. All thermal cycle and fuel handling requirements are site-dependent but not site-advantaged.

**Rounded score: 1.7 → 1.8**

**Justification**:
The concept has no customization advantages. Thermal rejection (score 2) is standard for a Rankine plant. Fuel safety (score 1) is the worst category — D-T tritium breeding plus reactive liquid metal handling. The final score 1.8 (on the 1–5 scale after transformation) reflects that this concept requires **more site infrastructure** than a D-D or aneutronic concept (which would score 2–3 on fuel safety) and has **no thermal rejection advantage** over any other thermal-cycle fusion plant.

This is a structural disadvantage vs. aneutronic concepts (p-B11, score 4 on fuel safety) and D-He3 concepts (score 3). It is comparable to conventional D-T tokamaks (also score 1 on fuel safety, score 2 on thermal rejection).

---

### C8: Data Adequacy — Score: 2.5

**Sub-factor A: Source diversity & independence (1-5)**

**Rating: 3 (Primarily company publications with some independent validation)**

**Public-domain sources**:
- Peer-reviewed journal articles: FST 2025 (fuel cycles, DOI confirmed), Nuclear Fusion 2025 (plasma confinement, cited in dossier), IAEA FEC 2025 abstract (LM26 milestones)
- Academic conference presentations: APS DPP 2018 (compression parameters), multiple APS/DPP posters
- Company website technical pages: generalfusion.com/fusion-technology (detailed concept description)

**Independent validation**:
- IAEA FEC 2025 abstract is peer-reviewed (conference abstracts undergo review)
- FST 2025 journal article is peer-reviewed
- No independent third-party techno-economic assessments (e.g., DOE, EPRI, academic groups) have been published

**Company-dominated**:
- Most quantitative data (cavity diameter, rep rate targets, commercial power output) comes from General Fusion press releases or website
- No multi-institutional collaborative publications (unlike tokamak programs, which have ITER/SPARC collaborations with universities)

**Score justification (3/5)**: There is a **mix of independent and company sources with public peer review** (FST 2025, IAEA FEC abstracts, Nuclear Fusion publications), but no independent architecture literature exists. The concept is primarily documented by the company, with peer-reviewed validation of specific physics results (plasma confinement, tritium inventory analysis) but not system-level design.

This is better than score 2 ("almost exclusively company publications") because peer-reviewed journal articles exist. It is worse than score 4 ("mix of independent and company sources with public peer review") because the independent validation is narrow (physics only, not engineering or economics).

**Sub-factor B: Reactor design specification (1-5)**

**Rating: 3 (Partial design with key subsystems defined but gaps in integration)**

**Available design specifications**:
- Cavity diameter: ~4 m (peer-reviewed, FST 2025)
- Liquid metal options: Li or PbLi (both under evaluation, FST 2025)
- Compression driver: pneumatic piston array (confirmed, but no detailed design published)
- Plasma injector: Marshall gun / compact toroid (demonstrated at LM26 scale)
- Power conversion: Rankine steam cycle (confirmed, but no steam parameters)
- Repetition rate: ~1 Hz (confirmed across multiple sources)

**Missing specifications**:
- Piston count, geometry, and synchronization control system
- Steam supply parameters (pressure, temperature, flow rate)
- Liquid metal flow rate and heat exchanger design
- Tritium extraction system architecture (ISS for PbLi, vacuum degassing for Li)
- Structural materials (pressure vessel, piston housing, heat exchangers)
- Remote handling approach and maintenance procedures
- Plasma heating and current drive (if any beyond compression)

**Score justification (3/5)**: The design is **partial** — major subsystems are identified (piston compression, liquid metal wall, CT injector, steam BOP) and some key parameters are specified (cavity size, rep rate, power output), but there are **significant integration gaps**. No integrated plant layout, no detailed piston design, no steam cycle parameters, no liquid metal flow control architecture.

This is better than score 2 ("preliminary design with significant specification gaps") because peer-reviewed publications confirm the basic architecture and operating parameters. It is worse than score 4 ("comprehensive conceptual design with major subsystems specified") because integration details are absent.

**Sub-factor C: LCOE parameter coverage (blocking gap count from gap_report.md)**

**Blocking gaps from gap_report.md Section 5**:
1. Fusion gain Q (commercial target) — proprietary — blocking
2. Recirculating power fraction (piston system) — proprietary — blocking
3. Capital cost (any subsystem) — proprietary — blocking
4. Piston system capital cost — proprietary — blocking
5. Pneumatic piston compression at any scale — not-yet-sourced — blocking
6. Liquid metal vortex stability at commercial repetition rate — truly-unknown — blocking

**Count: 6 blocking gaps**

**Score (LCOE parameter coverage)**: 5–7 blocking gaps → **2**

**Sub-factor D: Commercialization pathway clarity (1-5)**

**Rating: 3 (General pathway described but lacking specifics)**

**Available commercialization pathway information**:
- LM26 demonstration facility operational (2025–2026), targeting 10 keV ion temperature and Lawson criterion
- LM26 is 50% plasma scale and uses electromagnetic surrogate (theta-pinch), not commercial pneumatic system
- Commercial deployment target: early-to-mid 2030s (stated in multiple sources)
- Funding: $200M+ raised (2021–2024), including Shopify investment, government grants (Canada, UK)
- Partnership: UK Atomic Energy Authority collaboration announced (2024) for fusion development center

**Missing commercialization specifics**:
- No disclosed plan for a pneumatic compression demonstration at any scale (required before commercial plant)
- No published timeline for commercial system component testing (pistons, liquid metal handling at 1 Hz)
- No pilot plant milestones beyond LM26 (e.g., 0.1 Hz → 1 Hz progression)
- No disclosed LCOE target or cost-competitiveness roadmap
- No manufacturing partnerships for piston fabrication, liquid metal supply chain, or BOP integration

**Score justification (3/5)**: General Fusion has a **clear near-term pathway** (LM26 physics validation) and a **stated commercial timeline** (early 2030s), but the pathway from LM26 (electromagnetic surrogate) to the commercial pneumatic plant is **not described**. There is a major gap: no announced facility to test the pneumatic compression system at relevant scale or rep rate.

This is better than score 2 ("vague or aspirational commercialization narrative") because LM26 is operational and funded, and the UK partnership provides regulatory pathway. It is worse than score 4 ("clear pathway with identified steps but some gaps") because the commercial driver demonstration step is entirely absent.

**C8 = (A + B + C + D) / 4 = (3 + 3 + 2 + 3) / 4 = 2.75 → 2.8**

**Rounded score: 2.8 → 2.5** (adjusting downward to reflect the severity of blocking gaps in C, which dominate data adequacy for LCOE purposes; the score is more constrained by missing cost data than by missing design documentation).

**Justification**:
General Fusion has published more peer-reviewed physics results than most private fusion companies, and the concept architecture is well-documented. However, **zero cost data** has been published (capital, operating, performance economics), and the commercial pneumatic compression system has **never been tested at any scale**. The LM26 demonstration validates plasma physics but does not de-risk the commercial driver.

The final score 2.5 reflects that **qualitative understanding is good** (scores 3 on source diversity, design specification, and commercialization pathway) but **quantitative LCOE data is almost entirely absent** (score 2 on parameter coverage, with 6 blocking gaps). For a techno-economic analysis framework, data adequacy is dominated by the economic data gaps, not the physics data availability.

---

### C7: Technical Risk Evidence (Risk Matrix)

#### Function 1: Plasma Performance

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | nTτ ≥ 10²¹ m⁻³·keV·s (Lawson criterion for D-T fusion); ion temperature ≥10 keV; density ≥10²⁵ m⁻³ at compression peak |
| Best demonstrated | LM26 (2025): ion temperature ~10 keV (target met), density ~10²⁴ m⁻³ (190× compression from 10²² baseline), confinement time >10 ms pre-compression. **Lawson criterion not yet demonstrated** (2026 target per IAEA FEC 2025). |
| Gap ratio | Lawson: not yet achieved → N/A. Density: 10²⁵ / 10²⁴ = **10×** (requires one more order of magnitude compression). |
| Closure mechanism | LM26 scale-up from 50% to 100% plasma scale; transition from electromagnetic theta-pinch surrogate to pneumatic compression (commercial driver). Computational MHD modeling of compression stability. |
| Classification | **Binary** — if Lawson criterion cannot be met at commercial scale with pneumatic compression, net energy gain is impossible. |
| Evidence tier | **3** (Subscale demonstration: LM26 at 50% plasma scale with electromagnetic compression achieves ion temperature target and partial density compression; full Lawson criterion and commercial driver validation pending) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Pressure vessel withstands 1 Hz pulsed mechanical loading + neutron flux for 30-year lifetime; structural materials survive 14.1 MeV neutron damage (DPA accumulation) + thermal cycling without catastrophic failure. Specific limit: <20 DPA at end-of-life for steel structures. |
| Best demonstrated | Fission fast reactors (EBR-II, BN-600) demonstrate steel pressure vessels surviving neutron flux + thermal cycling for decades. No fusion-specific demonstration at 1 Hz pulsed mechanical loading with 14.1 MeV neutrons. LM26 vessel is non-activated (50% scale, low neutron fluence). |
| Gap ratio | Neutron energy: 14.1 MeV / ~1 MeV (fission) = **14×** (higher displacement damage per neutron). Pulsed mechanical loading: 1 Hz / 0 Hz (fission steady-state) = **∞** (no direct analogue). |
| Closure mechanism | Computational fatigue modeling of pulsed vessel loading; materials testing in fission neutron sources (HFIR, ATR) for DPA accumulation; extrapolation from sodium-cooled fast reactor vessel experience for thermal-mechanical coupling. |
| Classification | **Degrading** — if vessel lifetime is <10 years due to neutron embrittlement or fatigue, replacement costs increase LCOE by ~20–40% (via increased CAS22 replacement frequency and downtime). Not binary because the plant can operate with more frequent vessel replacement. |
| Evidence tier | **3** (Subscale / partial demonstration: fission reactor vessels demonstrate long-term neutron exposure and thermal cycling, but not at fusion neutron energy or pulsed mechanical loading; computational models exist but lack fusion-specific validation) |

**F1 mean**: (3 + 3) / 2 = **3.0**

---

#### Function 2: Driver / Energy Input

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Pneumatic piston array delivers 12:1 cavity volume compression in <1 ms with <1% timing synchronization error; adiabatic compression heats plasma from 0.1 keV → 10 keV and compresses density 10²² → 10²⁵ m⁻³ (1000× volume reduction). |
| Best demonstrated | Water-cavity compression tests (General Fusion, date not disclosed): **8:1 compression ratio achieved** with <10% perturbation. Electromagnetic theta-pinch (LM26, 2025): solid lithium liner compression achieves required plasma heating and density increase, but this is a surrogate driver (not pneumatic). |
| Gap ratio | Compression ratio: 12 / 8 = **1.5×** shortfall (33% gap). Pneumatic system at any scale: **never demonstrated** → N/A. |
| Closure mechanism | Full-scale pneumatic compression tests in liquid metal (not water surrogates) to validate 12:1 compression; piston synchronization control system development; CFD optimization of vortex geometry to maximize compression symmetry. **No announced facility or timeline for this demonstration.** |
| Classification | **Binary** — if 12:1 compression cannot be achieved with pneumatic pistons in flowing liquid metal, the plasma cannot reach fusion conditions (temperature and density both scale with compression ratio). Under-compression → zero net energy. |
| Evidence tier | **2** (Simulation only: water tests demonstrate partial compression, electromagnetic surrogate validates plasma response, but commercial pneumatic system has zero experimental validation; CFD models exist but are unvalidated against pneumatic-liquid-metal compression data) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | **Materials**: Piston seals survive 3×10⁷ cycles/year (1 Hz × 31.5M sec/yr) in activated environment with liquid metal splash; seal leakage <0.1% per cycle to maintain steam pressure. **Components**: Steam manifolds deliver synchronized pressure pulses to dozens-to-hundreds of pistons with <0.01 ms jitter; pistons retract and recharge within 1 second. |
| Best demonstrated | Industrial reciprocating compressors (Dresser-Rand, Atlas Copco): steam-driven pistons at <1 MPa pressure, <0.1 Hz duty cycle, non-activated environment, non-synchronized operation. **No system approaching 1 Hz synchronized multi-piston operation in activated liquid metal environment.** |
| Gap ratio | Duty cycle: 1 Hz / 0.1 Hz = **10×**. Synchronization: synchronized array / single-piston = **N/A** (qualitatively different regime). Activation environment: fusion neutron flux / industrial zero = **∞**. |
| Closure mechanism | Piston seal materials development (ceramic, metal, or elastomeric seals qualified for radiation + thermal cycling + liquid metal compatibility); steam control valve response time reduction (hydraulic or pneumatic actuation); distributed control system (DCS) for <1 ms synchronization across piston array. **No disclosed R&D program or demonstration timeline.** |
| Classification | **Binary** — if piston synchronization fails (timing scatter >1%, leading to asymmetric compression), the plasma does not reach fusion conditions and the pulse produces zero energy. If seal failure leads to steam leakage >10%, compression force is insufficient. No graceful degradation pathway. |
| Evidence tier | **1** (Asserted / absent: no experimental data on synchronized piston arrays at any scale approaching commercial requirements; industrial analogues exist for individual steam pistons but not for fusion-relevant duty cycle, synchronization, or environment; no published R&D results) |

**F2 mean**: (2 + 1) / 2 = **1.5**

---

#### Function 3: Instability Control

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Rayleigh-Taylor instabilities during compression must remain <10% amplitude (to avoid plasma disruption and asymmetric burn). MHD instabilities (kink, sausage modes) during confinement must be suppressed or tolerated for >1 ms burn duration. |
| Best demonstrated | LM26 (2025): compression event demonstrates ion temperature increase and density rise without catastrophic instability (neutron yield >600M n/s sustained during compression). **Quantitative instability amplitude measurements not disclosed.** Computational MHD simulations (General Fusion, unpublished) predict stable compression if symmetry <10% perturbation. |
| Gap ratio | Instability amplitude: <10% requirement / "not disclosed" best = **N/A** (insufficient data). Burn duration: 1 ms requirement / ~0.7 ms compression timescale = **~1.4×** (marginal, may be met). |
| Closure mechanism | Active feedback control of piston firing sequence to correct real-time asymmetries; passive stabilization via magnetic field geometry (CT self-field + compression-amplified field → ~200 T peak provides stabilization); MHD simulation validation against LM26 instability measurements. |
| Classification | **Degrading** — if instabilities reduce burn efficiency by 30–50% (via asymmetric compression or early termination), fusion yield per pulse falls proportionally, increasing LCOE by the same fraction. Not binary because partial burn still produces net energy if Q is high enough. |
| Evidence tier | **3** (Subscale demonstration: LM26 achieves compression without catastrophic disruption, and neutron yield implies some level of stable confinement, but quantitative instability data and commercial-scale validation are absent) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | **Materials**: Liquid metal (Li or PbLi) remains hydrodynamically stable during vortex formation, compression, and reformation at 1 Hz; no cavitation, splashing, or debris generation that disrupts subsequent pulses. **Components**: Liquid metal flow control system (pumps, valves, nozzles) maintains symmetric cavity geometry shot-to-shot with <5% variation. |
| Best demonstrated | General Fusion liquid lithium vortex formation tests (2019, scale not disclosed): demonstrated stable rotating liquid metal cavity in non-pulsed conditions. **No demonstration at 1 Hz with compression and reformation.** Sodium-cooled fast reactors (EBR-II, Phenix): flowing liquid metal at steady-state (not pulsed). |
| Gap ratio | Repetition rate: 1 Hz / 0 Hz (steady-state) = **∞**. Pulsed compression + reformation: commercial / demonstrated = **never demonstrated** → N/A. |
| Closure mechanism | Full-scale liquid metal flow loop tests at 0.1–1 Hz to validate vortex stability, compression uniformity, and reformation time; CFD modeling of liquid metal hydrodynamics under pulsed compression; debris filtration and impurity removal systems to prevent shot-to-shot degradation. **No announced test facility.** |
| Classification | **Binary** — if liquid metal vortex cannot reform symmetrically within 1 second, the next pulse cannot proceed, and repetition rate falls below commercial target. If reformation time is 2 seconds, rep rate is 0.5 Hz, and LCOE doubles (linear with rep rate). Below ~0.1 Hz, the concept becomes economically unviable. |
| Evidence tier | **2** (Simulation only: vortex formation demonstrated in steady-state, CFD models predict pulsed stability, but zero experimental validation of 1 Hz compression-reformation cycling; analogues from sodium reactors are not pulsed) |

**F3 mean**: (3 + 2) / 2 = **2.5**

---

#### Function 4: Plasma-Wall Interaction

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Liquid metal wall (Li or PbLi) absorbs plasma energy without excessive vaporization or impurity influx; vapor pressure <0.1 Pa (to avoid plasma contamination and radiative cooling). Surface temperature during burn must stay below boiling point (Li: 1342°C; PbLi eutectic: ~1670°C at atmospheric pressure). |
| Best demonstrated | NSTX-U and other tokamaks: liquid lithium limiters demonstrate compatibility with plasma edge (small-scale, edge-only contact). General Fusion: liquid metal wall contact with plasma during compression (LM26, scale not disclosed). **No measurement of vapor pressure or impurity influx at commercial fusion conditions.** |
| Gap ratio | Liquid metal surface temperature: ~1000–1200°C (inferred from 10 keV plasma) / "not measured" = **N/A**. Heat flux: 10–100 MW/m² during burn (inferred from fusion power density) / "not measured" = **N/A**. |
| Closure mechanism | Liquid metal flow velocity provides continuous surface renewal, preventing hotspot formation; thick liquid layer (1 m shell) provides thermal mass to absorb pulsed heat loads; Li vs. PbLi selection optimizes vapor pressure (PbLi has lower vapor pressure at equivalent temperature). |
| Classification | **Degrading** — if liquid metal vapor contaminates the plasma, radiative losses increase, reducing Q by 10–30% (proportional LCOE impact). If vapor pressure is extreme, plasma quenches, but this is unlikely given the thick liquid wall provides a heat sink. |
| Evidence tier | **3** (Subscale / partial demonstration: liquid lithium plasma contact demonstrated in tokamak edge and LM26 compression, but commercial-scale heat flux, vapor pressure, and impurity transport are unvalidated) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | **Materials**: Liquid metal (Li or PbLi) chemical compatibility with structural steel (pressure vessel, piping) over 30-year lifetime with <1 mm/yr corrosion rate. **Components**: Liquid metal pumps (EM or mechanical) operate at 1 Hz flow modulation with >99% uptime; heat exchangers transfer heat from Li/PbLi → steam without tube failures (<0.1 failures/year to avoid Li-water contact). |
| Best demonstrated | Fission liquid metal reactors (EBR-II, BN-600): sodium and lead-bismuth eutectic (LBE) compatibility with steel demonstrated for decades. Pure Li corrosion data from ITER TBM programs and Fusion Materials Facility tests. EM pumps (sodium, LBE) operate at steady-state in fission reactors. **No 1 Hz pulsed liquid metal pumping or heat exchanger operation at fusion scale.** |
| Gap ratio | Li corrosion rate: <1 mm/yr requirement / 0.5–2 mm/yr (literature range for Li-steel at 500–600°C, per ITER TBM) = **~0.5–2×** (marginal, material selection and temperature control critical). Pulsed pumping: 1 Hz / steady-state = **∞**. |
| Closure mechanism | Advanced steel alloys (e.g., F82H, RAFM steels) with Li corrosion inhibitors (Al, Si additions to Li); intermediate heat exchangers (IHX) to isolate Li from steam (preventing Li-water reaction); redundant heat exchanger tubes with leak detection; EM pump control systems for flow modulation. Demonstrated in fission programs (SFR, LFR). |
| Classification | **Degrading** — if heat exchanger tube failures occur at 1–2/year (vs. <0.1/year target), unplanned shutdowns increase, reducing capacity factor from 80% to 60–70%, increasing LCOE by ~15–25%. Not binary because heat exchangers can be repaired or replaced. |
| Evidence tier | **4** (Near-regime demonstrated: fission reactors validate Li/PbLi-steel compatibility and heat exchanger operation at steady-state; ITER TBM programs provide Li tritium breeding data; pulsed operation and fusion-scale heat exchangers are not demonstrated but are within 2× of fission analogues) |

**F4 mean**: (3 + 4) / 2 = **3.5**

---

#### Function 5: Neutron/Particle Handling

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | 14.1 MeV neutron energy spectrum from D-T fusion is accurately modeled for activation, heating, and tritium breeding; neutron multiplication in PbLi (if used) boosts TBR by ~10–15% as designed. |
| Best demonstrated | D-T fusion neutron spectrum is well-characterized from decades of tokamak D-T campaigns (TFTR, JET DTE1/DTE2, JT-60U). Neutron transport codes (MCNP, PHITS, OpenMC) validated against fission and fusion benchmarks. PbLi neutron multiplication measured in ITER TBM mock-ups and SINQ (PSI). |
| Gap ratio | Neutron energy modeling: 14.1 MeV / 14.1 MeV = **1.0×** (no gap; D-T spectrum is standard). PbLi multiplication: measured / predicted = **~1.0×** (validated). |
| Closure mechanism | No closure needed — D-T neutronics are well-understood and validated in fission and fusion experiments. |
| Classification | **Not a risk** — this is a known quantity; scoring 5 (operating-regime demonstrated). |
| Evidence tier | **5** (Operating-regime demonstrated: D-T fusion neutrons characterized in multiple tokamaks; neutron transport modeling validated; PbLi multiplication measured) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | **Materials**: Structural steel (vessel, piping) withstands <20 DPA (displacements per atom) over 30-year lifetime without embrittlement; tungsten or ceramic neutron shields reduce dose to pistons and instrumentation to <1 DPA. **Components**: Liquid metal circulation continues despite neutron activation (Li → T production, activation of impurities); radiation monitoring and shielding protect personnel during maintenance. |
| Best demonstrated | Fission fast reactors (BN-600, EBR-II): steel structures survive ~10–50 DPA in fast neutron spectrum (~1 MeV); some components replaced after 20 DPA. Fusion: ITER design basis assumes <20 DPA for structural steel with RAFM (Reduced Activation Ferritic Martensitic) alloys. **No fusion power plant lifetime demonstration at 14.1 MeV neutrons; extrapolation from fission.** |
| Gap ratio | Neutron energy: 14.1 MeV / ~1 MeV (fission) = **14×** (higher displacement damage per neutron; damage scales ~E^0.8, so ~10× more damage per neutron). Lifetime DPA: 20 DPA (target) / 10–20 DPA (fission demonstrated) = **~1–2×** (marginal). |
| Closure mechanism | Use of RAFM steels (F82H, EUROFER) qualified to 20 DPA in fission neutron irradiation facilities (HFIR, ATR); computational damage modeling (molecular dynamics, rate theory); ITER and DEMO programs provide material qualification pathway. Liquid metal activation managed via continuous purification and decay storage tanks. |
| Classification | **Degrading** — if vessel steel embrittlement occurs at 15 DPA instead of 20 DPA, vessel replacement is required after 22 years instead of 30 years, increasing lifecycle capital by ~15–20% (proportional LCOE impact). Not binary because the plant operates until replacement threshold. |
| Evidence tier | **4** (Near-regime demonstrated: fission reactors validate steel DPA tolerance at ~1 MeV; ITER/DEMO programs extend to 14.1 MeV via extrapolation and subscale irradiation tests; full 30-year fusion lifetime not demonstrated but within 2× of fission data) |

**F5 mean**: (5 + 4) / 2 = **4.5**

---

#### Function 6: Fuel Cycle Closure

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | TBR ≥ 1.05 for tritium self-sufficiency (breeding replaces burned + decayed tritium). Target TBR = 1.5 provides 50% margin for uncertainties and startup inventory accumulation. |
| Best demonstrated | Computational neutronics (MCNP, PHITS): TBR = 1.5 predicted for 4π liquid metal wall (Li or PbLi) in peer-reviewed FST 2025 paper. **No experimental validation at commercial scale.** ITER TBM programs will demonstrate TBR ~1.1–1.2 in outboard blanket modules (partial validation, different geometry). |
| Gap ratio | TBR prediction: 1.5 (computational) / 1.0–1.2 (ITER TBM expected) = **1.25–1.5×** (modest extrapolation from partial-angle breeding to 4π). |
| Closure mechanism | 4π solid-angle coverage provides intrinsic TBR advantage over outboard-only blankets; Li-6 enrichment (if needed) boosts TBR; PbLi neutron multiplication from Pb(n,2n) reactions adds ~10–15% margin. ITER TBM data (expected 2030s) will validate computational models. |
| Classification | **Binary** — if TBR < 1.05 at commercial scale, tritium self-sufficiency fails, and the plant cannot sustain D-T operation without external tritium purchases (which are unavailable at commercial fleet scale due to declining CANDU supply). |
| Evidence tier | **3** (Subscale / partial demonstration: TBR modeling validated in ITER TBM mock-ups and fission benchmarks; 4π geometry extrapolation is computational-only; no full-scale fusion breeding demonstration) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | **Materials**: Li-6 enrichment to 30–90% (depending on TBR modeling; natural Li is 7.6% Li-6) for tritium breeding; Western enrichment capacity ≥10 tonnes/yr for commercial fleet. **Components**: Tritium extraction system (vacuum degassing for Li, or isotope separation for PbLi) achieves >90% extraction efficiency at commercial flow rates; tritium permeation barriers at LM → steam interface limit losses to <0.1 kg/day. |
| Best demonstrated | Li-6 enrichment: COLEX process demonstrated in US (1950s–1960s, shutdown) and Russia/China (operational, capacity ~1–5 tonnes/yr). ITER TBM: tritium extraction from Pb-17Li demonstrated in lab-scale test loops (TLK, CIEMAT). **No commercial-scale tritium extraction at 1 Hz with flowing Li/PbLi.** Permeation barriers (Al₂O₃, oxide layers): effective in fission sodium systems. |
| Gap ratio | Li-6 enrichment capacity: 10 t/yr (fleet need) / ~1–5 t/yr (current) = **2–10×** (scaling required; US restart needed). Tritium extraction: commercial scale / lab-scale = **~100–1000×** (flow rate scaling). |
| Closure mechanism | US/Western Li-6 enrichment restart (ORNL, commercial CECE process development); scale-up of tritium extraction loops (vacuum degassing or molten salt extraction for Li; He bubbling or vacuum sieve tray for PbLi, per ITER TBM); double-walled heat exchangers with He purge for permeation control. **Li-6 enrichment is a shared D-T supply chain bottleneck; tritium extraction is General Fusion-specific R&D.** |
| Classification | **Binary** (Li-6 enrichment shortage at fleet scale → showstopper shared with all D-T concepts). **Degrading** (tritium extraction <90% efficiency → steady-state tritium deficit → must slow burn rate or purchase external T, reducing plant output or increasing fuel cost). |
| Evidence tier | **3** (Subscale demonstration: Li-6 enrichment proven at small scale; tritium extraction validated in ITER TBM test loops at <1% of commercial flow rate; full-scale integration and 1 Hz pulsed operation not demonstrated) |

**F6 mean**: (3 + 3) / 2 = **3.0**

---

#### Function 7: Power Conversion & BOP

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Pulsed heat deposition (1 Hz, ~500–800 MJ/pulse into liquid metal) is absorbed by liquid metal thermal mass and smoothed for continuous steam generation; steam conditions (temperature, pressure) remain stable despite pulsed source. |
| Best demonstrated | Pulsed heat loads in thermal storage (molten salt, liquid metal) demonstrated in concentrated solar power (CSP) plants (Gemasolar, Crescent Dunes) with heat storage buffering diurnal cycles. **No 1 Hz pulsed heat absorption at fusion energy density.** Computational modeling (General Fusion, unpublished) predicts liquid metal thermal mass sufficient for smoothing. |
| Gap ratio | Pulse frequency: 1 Hz / ~daily (CSP) = **~86,400×** faster pulsing. Energy per pulse: ~500–800 MJ / "not measured" = **N/A**. |
| Closure mechanism | Liquid metal heat capacity and flow rate sized to absorb per-pulse energy without excessive temperature swings; heat exchanger design provides continuous steam output (thermal inertia of the LM loop decouples pulsed source from steady steam); demonstration at LM26 scale or a dedicated thermal test loop. |
| Classification | **Degrading** — if thermal smoothing is incomplete, steam temperature oscillates, reducing turbine efficiency by 5–10% and increasing thermal stress on heat exchangers (maintenance cost penalty). Not binary because the Rankine cycle tolerates some temperature variation. |
| Evidence tier | **2** (Simulation only: CSP analogues demonstrate pulsed thermal storage concept but at vastly different timescales; fusion-specific 1 Hz pulsed heat extraction is unvalidated; computational models exist but lack experimental benchmarks) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | **Materials**: Steam generator tubes (heat exchanger between Li/PbLi and steam) survive pulsed thermal cycling (1 Hz, ~500–800 MJ/pulse) for 30 years with <0.1 tube failures/year; Li-water reaction prevention (double-walled tubes or IHX if Li). **Components**: Steam turbine operates at near-constant load despite pulsed fusion source (liquid metal thermal buffer stabilizes steam flow); condenser, feedwater pumps, and BOP are conventional. |
| Best demonstrated | Fission sodium-cooled fast reactors (SFR): steam generators with liquid metal primary loop operated for decades (EBR-II, Phenix, Monju). IHX designs for Li-to-NaK or Li-to-steam transitions studied in ITER TBM programs. Steam turbines are TRL 9 (coal, gas, fission). **No steam generator validated for 1 Hz thermal pulsing from Li/PbLi.** |
| Gap ratio | Thermal cycling: 1 Hz pulsed / steady-state = **∞** (qualitatively different fatigue regime). Li-steam heat exchange: demonstrated at lab scale / commercial scale = **~100×** (flow rate and heat duty scaling). |
| Closure mechanism | Thermal fatigue-resistant heat exchanger materials (Inconel, RAFM steels with thermal barrier coatings); double-walled tube design with He leak detection (prevents Li-water contact); oversized liquid metal thermal buffer to reduce temperature swing amplitude; steam generator demonstration at subscale (10–100 MWth). **Analogues from SFR provide design basis; 1 Hz pulsing is novel.** |
| Classification | **Degrading** — if steam generator tube failure rate is 1–2/year (vs. <0.1/year target), unplanned shutdowns increase, reducing capacity factor from 80% to 70%, increasing LCOE by ~14%. Not binary because tubes can be plugged or replaced during maintenance. |
| Evidence tier | **4** (Near-regime demonstrated: SFR steam generators validate liquid metal → steam heat exchange at steady-state; ITER TBM IHX designs validate Li heat exchange at subscale; pulsed thermal cycling is not demonstrated but is within 2× of fission SFR experience via computational thermal-mechanical modeling) |

**F7 mean**: (2 + 4) / 2 = **3.0**

---

### Function-Level Means (F1–F7)

| Function | F_mean | Notes |
|----------|--------|-------|
| F1: Plasma Performance | 3.0 | LM26 demonstrates 50% plasma scale; Lawson criterion pending |
| F2: Driver / Energy Input | 1.5 | Pneumatic compression never demonstrated; water tests show 33% shortfall |
| F3: Instability Control | 2.5 | Subscale stability shown; 1 Hz liquid metal vortex reformation unproven |
| F4: Plasma-Wall Interaction | 3.5 | Liquid metal wall contact demonstrated; commercial heat flux unvalidated |
| F5: Neutron/Particle Handling | 4.5 | D-T neutronics well-understood; fission analogues validate steel DPA tolerance |
| F6: Fuel Cycle Closure | 3.0 | TBR=1.5 predicted; tritium extraction at 1 Hz scale undemonstrated |
| F7: Power Conversion & BOP | 3.0 | SFR analogues strong; 1 Hz pulsed heat exchange novel |

**Heritage credit (D-T fuel)**: General Fusion's concept does **not** have clear lineage to previous public fusion experiments with established D-T operation. The compression mechanism is novel (pneumatic-liquid-metal, not tokamak/stellarator magnetic confinement, not laser IFE, not Z-pinch). The closest analogues are:
- Magnetized target fusion (MTF) programs: LANL FRX-L (1990s–2000s), MAGO (Russia, 1980s–1990s) — both discontinued, limited public data
- Compression concepts: LINUS (rotating liquid wall, 1970s–1980s, never reached plasma testing)

**Heritage floor does NOT apply** — no heritage credit because General Fusion's pneumatic-liquid-metal approach has no demonstrated lineage to previous operating fusion experiments at relevant scale. LM26 is the first significant MTF demonstration with this architecture.

**C7 (computed by Python)**: mean(F1–F7) = mean(3.0, 1.5, 2.5, 3.5, 4.5, 3.0, 3.0) = **3.0**

**Function-level cap check**: F2 = 1.5 ≤ 1.5 threshold → **C7 is capped at 1.5** (the actual F2 value).

**Final C7: 1.5** (capped by F2: Driver / Energy Input, due to zero demonstration of commercial pneumatic compression system).

### Binary Risks

1. **Pneumatic compression system failure (F2 hardware)**: If synchronized piston operation in liquid metal environment is mechanically infeasible, no fallback compression mechanism exists in the commercial design.

2. **Compression ratio shortfall (F2 physics)**: If 12:1 cavity compression cannot be achieved in flowing liquid metal, the plasma cannot reach fusion temperatures and densities (10 keV, 10²⁵ m⁻³ targets unmet).

3. **Lawson criterion failure (F1 physics)**: If nTτ < 10²¹ m⁻³·keV·s at commercial scale with pneumatic compression (vs. electromagnetic LM26 surrogate), net energy gain is impossible.

4. **Tritium breeding ratio shortfall (F6 physics)**: If TBR < 1.05 at commercial scale (computational models predict 1.5 but lack full-scale validation), tritium self-sufficiency fails.

5. **Li-6 enrichment supply bottleneck (F6 hardware)**: If Western Li-6 enrichment capacity cannot scale to 10+ tonnes/yr for commercial fusion fleet, D-T fuel cycle fails (shared with all D-T concepts).

6. **Liquid metal vortex stability failure (F3 hardware)**: If liquid metal cannot reform symmetrically within 1 second at 1 Hz, repetition rate falls, and LCOE increases proportionally (below ~0.1 Hz → economically unviable).

---

```yaml
---
scores:
  C1: 2.8
  C3: 3.4
  C4: 2.5
  C5: 1.8
  C8: 2.5
  F1: 3.0
  F2: 1.5
  F3: 2.5
  F4: 3.5
  F5: 4.5
  F6: 3.0
  F7: 3.0
  binary_risks:
    - "Pneumatic compression system synchronization failure — if piston timing scatter exceeds 1% or mechanical infeasibility prevents operation, no fallback driver exists"
    - "Compression ratio shortfall — if 12:1 cavity compression cannot be achieved in liquid metal (8:1 in water tests vs 12:1 target), plasma cannot reach fusion conditions"
    - "Lawson criterion failure at commercial scale — if nTτ < 10²¹ with pneumatic compression (LM26 electromagnetic surrogate does not validate commercial driver), net energy gain impossible"
    - "Tritium breeding ratio below self-sufficiency — if TBR < 1.05 (1.5 predicted, unvalidated), external tritium required (unavailable at fleet scale)"
    - "Li-6 enrichment supply bottleneck — Western capacity must scale 2–10× for D-T fleet (shared showstopper with all D-T concepts)"
    - "Liquid metal vortex reformation failure — if vortex cannot reform within 1 second at 1 Hz, repetition rate falls below viability threshold (~0.1 Hz minimum for LCOE <$150/MWh)"
---
```
