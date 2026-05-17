---
ID: 28-polywell
Concept: Polywell (D-T)
Company: EMC2
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: Polywell (D-T)

## 1. Executive Summary

- **The single most important risk**: The entire reactor concept rests on an unvalidated free parameter (γ = 0.1, the electron loss reduction factor). Park et al. 2025 explicitly acknowledges "currently, we lack a quantitative model for the reduction in the loss rate." If γ = 0.2 instead of 0.1, the concept produces negative net power. The University of Sydney (2019) found "little or no trace of virtual cathode formation" at higher densities — contested by EMC2 but never refuted with published experimental data.

- **The single most important advantage**: If the physics holds, the magnet system is tiny. Unlike tokamaks that must confine 20 keV ions directly (requiring massive 5–20 T magnets), Polywell only confines electrons magnetically at far lower energy density. Park 2025: "the magnetic energy density required to confine electrons is far smaller than that required to directly confine ions." The 1.6 m cube device with 4.5 T boundary field is orders of magnitude smaller than ITER-scale hardware for comparable fusion power.

- **LCOE ballpark**: Baseline model yields 11.1 ¢/kWh (111 $/MWh) at 248 MWe net, scaled to 6.4 ¢/kWh (64 $/MWh) at 1000 MWe reference. Conservative scenario (γ=0.2, FOAK) produces negative net power. These numbers are corridor indicators, not projections — the model is ~90% analogue-based.

- **Confidence verdict**: **Low**. No plant engineering study exists. The thermal cycle, blanket design, and tritium breeding ratio are all unspecified. Capital cost estimates rest on analogues from MFE/accelerator hardware with ×2–5 uncertainty. The single published reactor-scale study (Park 2025) is a physics scaling paper with explicit caveats about free parameters, not an engineering design. The LCOE model serves to bound the range if γ=0.1 holds, not to project likely outcomes.

---

## 2. What Matters Most for LCOE

The Polywell has an unusual LCOE structure: three parameters dominate, but two of them (γ and thermal efficiency) are either unvalidated or completely unspecified.

### Rank 1: Loss reduction factor γ / Q_plasma (blocking)

- **Assumed value**: γ = 0.1 (Park et al. 2025, arXiv:2508.06761, free parameter from 2D PIC simulation extrapolated to 3D)
- **Sensitivity**: The coupled γ sweep shows that γ = 0.05 yields 6.4 ¢/kWh (664 MWe net); γ = 0.10 yields 11.1 ¢/kWh (248 MWe net); γ = 0.15 yields 26.6 ¢/kWh (78 MWe net); γ = 0.20 produces negative net power (-29 MWe). This is a **factor of 4× LCOE swing** across the plausible γ range. No other parameter in the model has comparable leverage.
- **What would flip the economic conclusion**: Any experimental result showing γ > 0.15 at commercial plasma densities (~10²¹ m⁻³) would eliminate the Polywell as a power concept. The concept cannot sustain net electricity production above γ ≈ 0.18 given the fixed recirculating power structure (78+ MW e-beam injection). Conversely, experimental confirmation of γ ≤ 0.08 would halve LCOE and make the concept economically competitive with advanced fission.

### Rank 2: Thermal-to-electric efficiency (blocking)

- **Assumed value**: 35% (standardized per scoring framework for "Thermal (unspecified)")
- **Source**: ANALOGUE from MFE D-T steam Rankine baseline. No thermal cycle has been specified for the Polywell. Park 2025 mentions "neutrons will be captured in a blanket" but provides no coolant, cycle type, or thermodynamic parameters.
- **Sensitivity**: The thermal efficiency sweep shows 11.8 ¢/kWh at 33% efficiency vs. 8.2 ¢/kWh at 50% efficiency — a **±3 ¢/kWh range** around the 35% baseline. Net electric output varies from 227 MWe to 406 MWe across this range.
- **What would flip the economic conclusion**: If the polyhedral coil geometry forces a low-temperature thermal cycle (saturated steam at 32% efficiency rather than superheated steam at 40%), LCOE rises to ~12 ¢/kWh. If an advanced sCO₂ Brayton cycle at 48% efficiency is feasible, LCOE falls to ~8.6 ¢/kWh. The absence of any thermal design specification means this ±30% LCOE range is genuinely uncertain, not just sensitivity analysis.

### Rank 3: Capital cost of SC coil + e-beam systems (high uncertainty, moderate leverage)

- **Assumed values**: $150M for 6-coil superconducting magnet system (C220103); $100M for electron beam injection system (C220104)
- **Source**: ASSUMED. SC coil: scaled from SPARC-class HTS tokamak costs ($100–300M for full TF set) adjusted downward for 80 cm coil scale and non-interlocking geometry. E-beam: $5–15M per MW-class commercial beam × 10–20 beams for 78 MW total, plus integration.
- **Sensitivity**: Coil cost sweep shows 10.5 ¢/kWh at $75M vs. 12.4 ¢/kWh at $300M (±1.3 ¢/kWh around baseline). E-beam cost sweep shows 10.7 ¢/kWh at $50M vs. 12.0 ¢/kWh at $200M (±0.9 ¢/kWh). Combined, these two CAS22 overrides represent ~$250M of the $461M per-module reactor equipment cost — a major fraction, but with lower LCOE elasticity than γ or thermal efficiency.
- **What would flip the economic conclusion**: If the polyhedral SC coil geometry proves manufacturable at the low end of the range ($75M coils, $50M e-beam), LCOE falls to ~9.7 ¢/kWh. If engineering study reveals the non-interlocking geometry requires custom coil forms that double costs ($300M coils, $200M e-beam), LCOE rises to ~13.5 ¢/kWh. This is a ±2 ¢/kWh swing — significant, but an order of magnitude less leverage than the γ uncertainty.

### Rank 4: Blanket/first wall cost (high uncertainty, moderate leverage)

- **Assumed value**: $75M (C220101 override)
- **Source**: ARIES-class MFE D-T blanket studies estimate $50–150M for comparable neutron power levels in standard toroidal geometry. The standard 1costingfe analogue formula (0.60 M$/m³ × blanket volume) yields ~$7.3M but is derived from toroidal MFE geometry and is inapplicable to the 6-faced polyhedral cusp. Park 2025 acknowledges "neutron shadowing caused by internal coil structures" as a challenge requiring "innovative breeding solutions" — no design exists (TRL 1).
- **Sensitivity**: Blanket cost sweep shows 10.7 ¢/kWh at $50M vs. 13.1 ¢/kWh at $200M (±2.0 ¢/kWh around the $75M baseline). The replacement schedule (6 replacements over 40-year plant life at 5 FPY core lifetime) amplifies capital cost impact through CAS72.
- **What would flip the economic conclusion**: If a polyhedral-geometry blanket proves manufacturable at tokamak-analogue costs ($50M), LCOE falls to ~10.7 ¢/kWh. If the coil-shadowing problem forces a thicker or higher-enrichment blanket that costs $150–200M, LCOE rises to 12.3–13.1 ¢/kWh. The geometry-specific engineering challenge means the $7.3M generic analogue is a red herring — the true range is $50–200M with no central tendency.

### Rank 5: Capacity factor (moderate leverage)

- **Assumed value**: 80%
- **Source**: ANALOGUE from MFE D-T aspirational targets. No Polywell maintenance strategy, unplanned outage model, or operational data exists. Park 2025 claims "easily assembled and disassembled in a modular manner" due to non-interlocking coils, but this is a design claim, not a demonstrated maintenance advantage.
- **Sensitivity**: Capacity factor sweep shows 14.6 ¢/kWh at 60% vs. 10.0 ¢/kWh at 90% (±3.5 ¢/kWh around the 80% baseline). This is purely a utilization penalty — capital cost is fixed regardless.
- **What would flip the economic conclusion**: If modular coil replacement enables 90% capacity factor (tokamak-beating), LCOE falls to 10.0 ¢/kWh. If steady-state operation at high beta proves unstable and forced outages push capacity factor to 60–70%, LCOE rises to 12.6–14.6 ¢/kWh. The lack of operational data means this is genuinely uncertain.

**Summary ranking by LCOE sensitivity (baseline to extreme)**:
1. γ (0.1 → 0.15): 11.1 → 26.6 ¢/kWh (+140%)
2. Thermal efficiency (35% → 33%): 11.1 → 11.8 ¢/kWh (+6%)
3. Capacity factor (80% → 60%): 11.1 → 14.6 ¢/kWh (+31%)
4. Blanket cost ($75M → $200M): 11.1 → 13.1 ¢/kWh (+18%)
5. Coil + e-beam ($250M → $500M combined): 11.1 → 13.5 ¢/kWh (+22%)

The γ parameter dwarfs all others because it couples both the physics gain (fusion power output) and the recirculating power requirement (beam injection power) simultaneously. It is the master lever.

---

## 3. Risk Verdicts

### Major Challenge 1: γ / virtual cathode formation (γ=0.1 unvalidated)

- **Verdict**: Unlikely resolvable without multi-year experimental program; genuinely uncertain whether γ ≤ 0.1 is achievable at reactor densities.
- **Rationale**: WB-X (2013, Phys. Rev. X 2015) demonstrated high-beta electron confinement enhancement at 13.8 cm coil scale with sub-microsecond pulses. The University of Sydney (2019) calculated that 200,000 A electron supply would be required to sustain a virtual cathode at commercial plasma densities and found "little or no trace of virtual electrode formation" in their experiments. EMC2 disputes this but has published no counter-experimental evidence. Park 2025 extrapolates γ=0.1 from 2D PIC simulations with explicit caveats: "currently, we lack a quantitative model for the reduction in the loss rate." The FPNS program (350 kW fusion, 2–3 T field, $20M/24 months) is the next validation milestone, but FPNS is not at reactor-relevant plasma density or steady-state duration.
- **What would retire this risk**: FPNS experimental data showing sustained high-beta electron confinement at ~10²⁰–10²¹ m⁻³ with measured loss rates consistent with γ ≤ 0.1. A peer-reviewed experimental paper refuting the University of Sydney calculation with direct measurements of virtual cathode stability. Timeline: FPNS Phase 1 is ~2 years from program start; scaling to reactor-relevant parameters would require an additional device (cost unknown, likely $100M+ for a steady-state reactor-scale prototype).

### Major Challenge 2: No energy conversion architecture (blocking for LCOE)

- **Verdict**: Likely resolvable by engineering design study; not a fundamental physics risk.
- **Rationale**: 80% of D-T fusion energy (14.1 MeV neutrons) flows into an unspecified blanket with unspecified coolant and unspecified thermal cycle. This is an engineering gap, not a physics gap. Standard steam Rankine or sCO₂ Brayton cycles are mature; the question is which one EMC2 selects and how the polyhedral coil geometry constrains blanket cooling. Park 2025 mentions "naturally diverging magnetic fields at plasma-facing surfaces" for thermal management but provides no cycle parameters.
- **What would retire this risk**: EMC2 engineering design study specifying blanket coolant (water, LiPb, FLiBe, etc.), thermal cycle type (Rankine, Brayton, or other), and gross/net electric power balance. This is a ~1-year, ~$5M conceptual design study, not a multi-decade research program. If EMC2 has prioritized physics validation (FPNS) over plant engineering, this gap may persist for years.

### Major Challenge 3: Tritium breeding blanket geometry (coil neutron shadowing)

- **Verdict**: Genuinely uncertain; novel engineering required, but not obviously impossible.
- **Rationale**: The six coil faces subtend a large solid angle from the plasma center, shadowing neutrons from the blanket in those directions. Park 2025 acknowledges this explicitly: "tritium breeding blankets can operate in regions of low magnetic field strength, providing opportunities for innovative breeding solutions to address neutron shadowing caused by internal coil structures." No TBR calculation, no blanket geometry, and no material selection has been published. Standard liquid-Li or LiPb blanket designs from MFE tokamaks cannot be adapted without a neutronics study specific to the polyhedral geometry.
- **What would retire this risk**: MCNP or Serpent neutronics analysis showing TBR > 1.1 achievable in the polyhedral cusp geometry with specified blanket material and thickness. If the analysis reveals TBR < 1.0 without impractically thick blankets or extreme Li-6 enrichment, the D-T variant is nonviable and the concept pivots to D-D or external tritium purchase (cost prohibitive). Timeline: neutronics study is ~6–12 months once blanket material is selected; material selection requires the thermal cycle specification first (Challenge 2).

### Major Challenge 4: Scaling extrapolation from WB-X to reactor (10⁶× power, 12× linear scale)

- **Verdict**: Genuinely uncertain; scaling laws derived from sub-microsecond pulsed experiments to steady-state reactor operation carry enormous uncertainty.
- **Rationale**: WB-X (coil diameter ~13.8 cm, sub-microsecond pulses) → reactor (coil diameter ~160 cm, 980 MW steady-state). Park 2025 derives scaling laws from PIC simulations and WB-X/WB-8 data but acknowledges the gyroradius scaling exponent is "preliminary" and requires "future experiments and/or simulations." The mass ratio extrapolation from hydrogen to deuterium-tritium (mass ratio 3672) is flagged as needing validation. No intermediate-scale device has bridged the gap between WB-8 (0.8 T, ~100 ms pulses) and the reactor design.
- **What would retire this risk**: FPNS data at 2–3 T and ~1-second pulses, followed by a reactor-scale demonstration device at 4.5 T steady-state. If FPNS reveals unfavorable scaling (confinement degrades faster than predicted, or instabilities emerge at higher density), the reactor design collapses. Timeline: FPNS Phase 1 ~2 years; reactor-scale prototype ~10+ years and $500M+ if FPNS succeeds.

### Major Challenge 5: Bremsstrahlung radiation balance (thermalized plasma assumption)

- **Verdict**: Likely resolvable by first-principles calculation; medium priority given other uncertainties.
- **Rationale**: Rider (1995) calculated that bremsstrahlung X-ray losses exceed fusion power for non-Maxwellian plasmas. Bussard argued this doesn't apply to Polywell's non-equilibrium ion distribution. Park 2025 assumes "sufficiently fast thermalization time scale for a high-density cusp plasma equilibrium" — i.e., the plasma thermalizes, which changes the Rider calculation but also means the ion distribution is Maxwellian at 20 keV, not the monoenergetic beams Bussard envisioned. This theoretical tension (thermalized plasma loses any direct-conversion advantage; non-thermal plasma faces Rider radiation losses) is not resolved in any public source.
- **What would retire this risk**: First-principles bremsstrahlung calculation for 20 keV Maxwellian D-T plasma at reactor density using Park 2025's thermalization assumption. If bremsstrahlung losses are <5% of fusion power, this is a non-issue. If losses are 10–20%, gross thermal output is reduced correspondingly but the concept remains viable. If losses exceed 30%, the thermalized-plasma model is untenable. This is a ~3-month theoretical/computational study, not an experimental program.

### Major Challenge 6: Superconducting coil design for 6-sided cusp geometry

- **Verdict**: Likely resolvable by engineering design study; cost uncertainty is the primary concern, not feasibility.
- **Rationale**: All WB-series devices used resistive copper coils. EMC2 reportedly began SC Polywell development in 2012 but no results were published. The 4.5 T boundary field in Park 2025 implies steady-state superconducting coils — resistive coils would require impractical continuous cooling. The non-interlocking cubic geometry has been described as a manufacturing advantage, but no SC coil design with specified wire type (REBCO, Nb₃Sn), operating temperature, or mechanical support structure has been published. Standard HTS tokamak coil knowledge does not transfer directly to the polyhedral geometry.
- **What would retire this risk**: SC coil design study specifying conductor type, operating temperature (4.2 K LTS or 20–77 K HTS), coil form geometry, and structural support under high-beta plasma pressure. If the non-interlocking geometry enables factory-manufactured coil modules at lower cost than tokamak TF coils, the capital cost advantage is real. If custom coil forms double costs, the advantage evaporates. Timeline: ~1-year engineering study; prototype coil fabrication ~2–3 years.

---

## 4. Structural Advantages and Disadvantages

Compare against the conventional D-T tokamak cost structure baseline (ITER-lineage, ~$5000–7000/kWe overnight capital).

### Eliminated or reduced cost items (advantages):

1. **Magnet system size (potential 40–60% CAS22 reduction)**:
   - Polywell confines electrons at far lower magnetic energy density than ion-confining MFE. Park 2025: "the magnetic energy density required to confine electrons is far smaller than that required to directly confine ions." The baseline model allocates $150M for the 6-coil SC system at 4.5 T boundary field (C220103) vs. $400–600M for ITER-scale tokamak TF coils. The 1.6 m cube device is physically tiny compared to ITER's 6.2 m plasma radius. If the SC coil cost estimate holds, this eliminates ~$250–450M relative to a tokamak of comparable fusion power.
   - Caveat: no SC Polywell coil has been built. The $150M is an analogue, not a quote.

2. **No divertor (eliminates CAS22 sub-account, ~$50–100M)**:
   - The Polywell's cusp geometry naturally provides plasma exhaust outlets at the cusp points. Unlike tokamaks, which require a complex plasma-exhaust handling system (divertor) with remote maintenance and regular replacement, the Polywell has no divertor. This eliminates a major MFE cost item and maintenance headache.
   - Caveat: plasma-facing component (PFC) heat flux management in the cusp regions is unaddressed. If the cusps require active cooling or shielding that adds cost comparable to a divertor, the advantage is illusory.

3. **Modular coil assembly (potential 20–40% reduction in remote handling and installation labor, CAS22 C220110 + C220111)**:
   - Park 2025 claims the six non-interlocking coils are "easily assembled and disassembled in a modular manner." Unlike tokamak TF coils that interlock and require fully remote maintenance, Polywell coils each face one side of the cube and can (in principle) be replaced independently. The baseline model applies a 0.4× scale factor to remote handling costs ($60M vs. $150M for standard MFE) and sees proportional installation labor savings.
   - Caveat: this is a design claim, not a demonstrated maintenance advantage. No Polywell has operated long enough to validate the modular replacement advantage. If neutron activation or blanket integration prevents independent coil removal, the advantage disappears.

4. **Compact device size (reduces CAS21 buildings cost by ~20–30%)**:
   - A 1.6 m cube reactor core fits in a far smaller reactor building than ITER-scale hardware. The baseline model uses the standard D-T building cost formula (502 $/kWe) but the compact geometry should reduce building volume. Quantifying this requires a plant layout study that doesn't exist.

### Added or increased cost items (disadvantages):

1. **High recirculating power fraction (structural penalty, -15 to -25 percentage points capacity vs. burning-plasma MFE)**:
   - The Polywell is not a burning plasma. The electrostatic well requires continuous 78 MW electron beam injection to maintain ion acceleration. Baseline recirculating fraction is 33% (122.8 MW total recirculating / 370 MWe gross electric). A burning-plasma tokamak recirculates 10–20% for heating and housekeeping once ignited. This 13–23 percentage point penalty is structural and permanent — it's built into the physics, not the engineering. Every MWe of output costs proportionally more capital because a larger fraction of gross electric is consumed internally.
   - At γ=0.2, recirculating fraction rises to 50%+ and the concept produces negative net power. This is the γ coupling penalty described in Section 2.

2. **Tritium breeding blanket geometry challenge (potential +$50–150M vs. standard MFE blanket)**:
   - The standard 1costingfe blanket cost analogue (0.60 M$/m³ × blanket volume) yields ~$7.3M for the Polywell's compact geometry. This is misleading. The polyhedral cusp geometry creates neutron shadowing with no proposed engineering solution (Park 2025 acknowledges this). ARIES-class MFE D-T blanket studies estimate $50–150M for comparable neutron power levels in standard toroidal geometry. The baseline model overrides C220101 to $75M (conservative ARIES lower bound) with a stated range of $50–200M. If the "innovative breeding solutions" Park 2025 mentions prove expensive or infeasible (TBR < 1.0), this wipes out the magnet cost savings.

3. **Electron beam injection system (new CAS22 line item, ~$100M)**:
   - MFE concepts use neutral beam injection or RF heating (CAS22 C220104, ~$40–80M for comparable injected power). The Polywell requires 78 MW of 60 keV electron beams ($100M baseline estimate). Commercial electron beam systems exist, but 78 MW total injection into a magnetic cusp geometry is unprecedented. Integration engineering and power supply efficiency losses add cost.
   - Park 2025 notes "off-the-shelf availability" but provides no cost data. The $100M estimate is an analogue with ×2 uncertainty.

4. **Unspecified thermal cycle efficiency penalty (potential -5 to -10 percentage points vs. advanced MFE)**:
   - Advanced tokamaks assume superheated steam at 40% or sCO₂ Brayton at 45–48% thermal efficiency. The Polywell has no specified thermal cycle. If the polyhedral coil geometry constrains blanket cooling to saturated steam at 32% efficiency (lower temperature limit), net electric output falls by ~20% and LCOE rises proportionally. The baseline assumes 35% (standardized per framework), but this is a placeholder, not an engineering assessment.

### Net capital cost comparison (baseline scenario):

- Polywell overnight capital: $1429M at 248 MWe → $5764/kWe
- Scaled to 1000 MWe (α=0.6 economy-of-scale): $3302/kWe
- Conventional D-T tokamak (ITER-lineage): ~$5000–7000/kWe

If the physics holds (γ=0.1) and the SC coil cost estimate is accurate, the Polywell has a **30–50% capital cost advantage** vs. ITER-scale tokamaks at comparable electric output. The recirculating power penalty (~33% vs. ~15% for burning plasma) and thermal efficiency uncertainty offset this advantage in LCOE terms, yielding 6.4 ¢/kWh (64 $/MWh) at 1000 MWe vs. 5–7 ¢/kWh for advanced tokamaks.

The advantage is real but fragile: if γ > 0.12, the recirculating power penalty dominates and LCOE exceeds tokamak baselines. If blanket cost reaches the upper end of the ARIES range ($150–200M), the capital advantage shrinks to <20%.

---

## 5. Cross-Concept Positioning

The Polywell occupies a unique position in the fusion landscape: it is the only electrostatic confinement concept with a published reactor-scale design study (Park 2025) and the only D-T concept that confines electrons magnetically but ions electrostatically.

### Nearest conceptual neighbors:

1. **13-electrostatic-hybrid (Avalanche Energy)**: E×B electron confinement with electrostatic ion acceleration — shares the principle of using electron trapping to build an electrostatic well for ions. Avalanche uses resistive wall + electrostatic cathode rather than magnetic cusp; similar Q-prediction uncertainty. Not yet analyzed.

2. **IEC/Fusor concepts (Farnsworth-Hirsch lineage)**: The Polywell's direct ancestor. Distinguished by replacing the physical grid cathode with a magnetic cusp, eliminating grid losses. The same fundamental question applies: can electron confinement time be long enough for net energy?

3. **06-magnetic-mirror, 11-magnetic-mirror**: Both use open-field-line magnetic confinement with cusp-like field topology. The Polywell's magnetic cusp is structurally similar to mirror cusps, but the physics is inverted — mirrors confine ions magnetically and lose electrons; Polywell confines electrons magnetically and accelerates ions electrostatically.

### Divergence from MFE mainstream (tokamaks, stellarators):

The Polywell is conceptually distant from all closed-field-line MFE in four ways:

1. **Magnet sizing**: MFE magnets must confine 20 keV ions at billion-particle densities, requiring >5–20 T fields over large plasma volumes. Polywell magnets only confine electrons at much lower energy densities — in principle, a far smaller and cheaper magnet system. The 1.6 m cube vs. ITER's 6.2 m radius plasma exemplifies this.

2. **No divertor**: Tokamaks require complex plasma-exhaust handling (divertor). The Polywell's cusp geometry naturally provides plasma exhaust outlets at the cusp points, eliminating a major MFE cost and maintenance item.

3. **No burning plasma**: The Polywell is not designed around self-sustaining burn. The electrostatic well continuously injects energy (78 MW e-beam) to maintain ion acceleration. Alpha heating is incidental. This changes the self-Q calculation: the e-beam must run continuously at full power, creating a structural recirculating power fraction (~33% at γ=0.1, ~50%+ at γ=0.2). A burning-plasma MFE recirculates 10–20% once ignited. This 13–23 percentage point penalty is permanent.

4. **Modular assembly**: The six non-interlocking coils each face one side of the cube. Park 2025 claims this enables straightforward manufacturing and maintenance — a contrast to interlocked TF coils that require fully remote maintenance. If true, this reduces CAS22 C220110 (remote handling) and C220111 (installation labor) by 40–60%. If false (neutron activation or blanket integration prevents independent coil removal), the advantage is illusory.

### Economic positioning (if γ=0.1 holds):

- **Best-case (γ=0.05–0.08, optimistic scenario)**: 4.4–6.4 ¢/kWh (44–64 $/MWh) at 1000 MWe. Competitive with advanced fission and wind+storage. Magnet cost advantage dominates; recirculating power penalty is manageable.
- **Central case (γ=0.10, moderate scenario)**: 6.4 ¢/kWh (64 $/MWh) at 1000 MWe. Comparable to advanced tokamaks (5–7 ¢/kWh). Capital advantage offsets recirculating power penalty.
- **Pessimistic case (γ=0.12–0.15)**: 10–20 ¢/kWh. Recirculating power penalty dominates; magnet cost advantage is insufficient. Noncompetitive.
- **Failure case (γ > 0.18)**: Negative net power. Concept is nonviable for electricity generation.

The Polywell's LCOE corridor overlaps with advanced tokamaks only if γ ≤ 0.10. It has no overlap with low-cost renewables (2–4 ¢/kWh wind/solar) under any scenario. The recirculating power penalty floor is structural — even at γ=0.05, recirculating fraction is ~20%, which limits LCOE downside to ~4 ¢/kWh at 1000 MWe with aggressive capital cost assumptions.

### What makes this concept fundamentally different:

The Polywell is the only D-T concept where **a single unvalidated free parameter (γ) determines viability**. For tokamaks, Q is constrained by decades of transport scaling law benchmarks (ITER-98, ITERH-98y2, etc.). For IFE, gain is constrained by radiation-hydrodynamic simulation validated against NIF/OMEGA experiments. For the Polywell, Q = f(γ), and γ is a free parameter from 2D PIC extrapolated to 3D with no experimental validation above WB-X's sub-microsecond pulses at 13.8 cm scale.

If γ ≤ 0.10 is real, the Polywell is a genuine dark horse — small, cheap magnets and no divertor offset the recirculating power penalty. If γ > 0.15, the concept is dead on arrival. There is no middle ground. This binary risk profile makes the Polywell fundamentally unlike any MFE or IFE concept in the portfolio.

---

## 6. Modeling Confidence

**Rating: Low**

The baseline LCOE model (11.1 ¢/kWh at 248 MWe, 6.4 ¢/kWh scaled to 1000 MWe) is ~90% analogue-based. Of the 12 blocking gaps identified in the gap report, only 2 are resolved with concept-specific data (fusion power and input power from Park 2025). The remaining 10 are derived by analogy:

### Data-anchored parameters (2):

1. **Fusion power** (980 MW): Park 2025, Table II. Confidence: medium (depends on γ=0.1 assumption).
2. **Electron beam input power** (78 MW): Park 2025, Table II. Confidence: medium (60 keV × 1.3 kA is explicit).

### Analogue or assumed parameters (10):

3. **Thermal efficiency** (35%): Standardized from "Thermal (unspecified)" per framework. No Polywell thermal cycle exists. Range: 32–50%. Confidence: very low.
4. **Recirculating power fraction** (33%): Derived from power balance (e-beam wall-plug + cryogenic + housekeeping + tritium + vacuum). Beam supply efficiency (85%) is industrial analogue. Confidence: low.
5. **SC coil cost** ($150M): Analogue from SPARC-class HTS tokamak TF coils scaled to 80 cm coil diameter. No SC Polywell coil design exists. Range: $75–300M. Confidence: very low.
6. **E-beam system cost** ($100M): Analogue from commercial e-beam systems ($5–15M per MW-class unit) × 10–20 beams. No 78 MW integrated system exists. Range: $50–200M. Confidence: very low.
7. **Blanket/FW cost** ($75M): Override using ARIES-class MFE blanket cost range ($50–150M) as proxy. Standard formula ($7.3M) inapplicable due to polyhedral geometry. Range: $50–200M. Confidence: very low.
8. **Buildings cost** ($186M): Standard D-T formula (502 $/kWe). Should be lower for compact device but no plant layout exists. Range: $150–220M. Confidence: low.
9. **O&M cost** ($46.2M/yr): Analogue from MFE D-T (52 M$/yr at 1 GWe, scaled to 248 MWe). No Polywell operational model exists. Confidence: low.
10. **Capacity factor** (80%): Analogue from MFE D-T aspirational. Modular coil advantage claimed but not demonstrated. Range: 60–90%. Confidence: low.
11. **Blanket lifetime** (5 FPY): Standard D-T assumption at 14.1 MeV neutron flux. No Polywell-specific PFC lifetime data. Confidence: medium (generic D-T analogue is defensible).
12. **Tritium breeding ratio** (assumed ≥1.0): Required for D-T self-sufficiency, but no blanket design or neutronics study exists. Polyhedral coil shadowing acknowledged as challenge. Confidence: very low (could be <1.0, invalidating D-T operation).

### Dominant source of LCOE uncertainty:

The γ parameter dwarfs all others. The coupled γ sweep (Section 2, model output lines 172–182) shows:

- γ=0.05: LCOE = 6.4 ¢/kWh, net = 664 MWe
- γ=0.10: LCOE = 11.1 ¢/kWh, net = 248 MWe (baseline)
- γ=0.15: LCOE = 26.6 ¢/kWh, net = 78 MWe
- γ=0.20: net power negative (-29 MWe)

This is a **factor of 4× LCOE swing** across the plausible γ range (0.05–0.15). By comparison:

- Thermal efficiency (33–50%): ±30% LCOE swing
- Capital cost uncertainty (all CAS22 overrides ±50%): ±20% LCOE swing
- Capacity factor (60–90%): ±30% LCOE swing

The γ uncertainty dominates by an order of magnitude. Until γ is experimentally validated, all LCOE projections are speculative corridors, not estimates.

### Secondary source of LCOE uncertainty:

Energy conversion architecture. The model assumes 35% thermal efficiency by standardization, but no thermal cycle, coolant, or BOP design exists. The thermal efficiency sweep shows 11.8 ¢/kWh at 33% vs. 8.2 ¢/kWh at 50% — a ±26% LCOE range. This is an engineering gap (resolvable by design study), not a physics gap, but it's currently blocking.

### What would improve modeling confidence to Medium:

1. FPNS experimental data validating γ ≤ 0.1 at ~10²⁰ m⁻³ (not yet reactor-relevant, but a bridge).
2. EMC2 engineering design study specifying thermal cycle, blanket coolant, and gross/net electric power balance.
3. Neutronics analysis confirming TBR > 1.1 achievable in polyhedral geometry.
4. SC coil design study with conductor type, operating temperature, and cost estimate from a supplier.

Even with all four, confidence would remain Medium (not High) because the reactor-scale extrapolation (WB-X → 980 MW, 10⁶× power) is unprecedented. High confidence requires a reactor-scale prototype, which is >10 years and $500M+ away even if FPNS succeeds.

---

## 7. What Would Change My Mind

### 1. FPNS experimental results showing γ > 0.12 at high beta

**Direction**: Invalidates the concept for power generation.

If the FPNS program (2–3 T, 350 kW fusion, $20M/24 months) measures electron loss rates corresponding to γ > 0.12 at high beta (β ~1) and plasma densities approaching 10²⁰ m⁻³, the reactor design collapses. At γ=0.15, the baseline model yields 26.6 ¢/kWh with only 78 MWe net; at γ=0.20, net power is negative. The coupled γ sweep (model output line 178) shows the concept crosses the net-power threshold at γ ≈ 0.18.

EMC2 could respond by redesigning for higher beam power or lower fusion power, but both paths worsen LCOE. The recirculating power penalty is structural — there is no engineering fix if the physics doesn't cooperate.

**Likelihood**: Medium. The University of Sydney (2019) found "little or no trace of virtual electrode formation" at higher densities and calculated 200,000 A electron supply required. EMC2 disputes this but has not published counter-data. FPNS will resolve the dispute one way or the other.

### 2. Neutronics analysis showing TBR < 1.0 in polyhedral geometry

**Direction**: Forces pivot to D-D or external tritium purchase (cost prohibitive).

If an MCNP/Serpent study reveals that the polyhedral coil geometry creates sufficient neutron shadowing that TBR < 1.0 even with Li-6 enrichment and thick blankets, the D-T variant is nonviable. External tritium purchase at current CANDU market rates (~$30M/kg) would add ~$1.6B/year fuel cost for a 980 MW fusion plant (55 kg/yr tritium consumption at 55% burnup) — utterly prohibitive.

EMC2 could pivot to D-D (no tritium breeding required, but cross-section is 100× lower and Q drops by similar factor) or p-B11 (aneutronic, but Rogers 2018 analysis shows p-B11 Polywell requires >100 T fields or >1 MeV ion energies). Neither pivot is economically viable.

**Likelihood**: Low-medium. The polyhedral geometry is a genuine challenge (Park 2025 acknowledges it), but breeding blanket engineers have solved harder problems (e.g., ITER's complex 3D blanket geometry). If TBR ≈ 1.0–1.05 is achievable with thicker blankets, the concept survives with a cost penalty ($150–200M blanket instead of $75M). TBR < 1.0 seems unlikely unless the coil-shadowing solid angle exceeds ~30%.

### 3. EMC2 publishes engineering design study with sCO₂ Brayton at 48% efficiency + modular blanket at $50M

**Direction**: Validates the magnet cost advantage; LCOE falls to ~8 ¢/kWh (optimistic scenario).

If EMC2 (or an independent group) publishes a plant engineering study showing:
- sCO₂ Brayton thermal cycle at 48% efficiency (vs. 35% baseline)
- Polyhedral blanket manufacturable at tokamak-analogue cost ($50M vs. $75M baseline)
- SC coil system at low end of range ($100M vs. $150M baseline)
- Modular coil replacement validated (90% capacity factor vs. 80% baseline)

...then the optimistic scenario LCOE (7.7 ¢/kWh at 253 MWe, 4.4 ¢/kWh scaled to 1000 MWe) becomes credible. This would position the Polywell as cost-competitive with advanced fission if γ=0.1 holds.

**Likelihood**: Low. EMC2 has published two peer-reviewed papers since 2015 (WB-X results, Park 2025 scaling) and minimal website content. Current focus is FPNS (neutron source for isotope production, not power plant). A full plant engineering study is a ~$5–10M, 1–2 year effort that EMC2 has shown no indication of pursuing. If a national lab or ARPA-E funds such a study (contingent on positive FPNS results), timeline is 2027–2029.

---

## 8. LCOE Downselect Scoring

### C1: Modularization (5 sub-factors, cost-weighted)

**Score: 3.4**

The Polywell has genuine modularization advantages in the reactor core (non-interlocking coils, compact geometry) but shares the same stick-built BOP as any thermal-cycle fusion plant.

**Per-CAS mode classification**:

| CAS Account | Mode | Score | Cost Weight | Notes |
|-------------|------|-------|-------------|-------|
| CAS21 Buildings | Stick-built | 1 | 13% ($186M / $1429M OCC) | Reactor building, turbine hall, hot cell — conventional construction |
| C220101 Blanket/FW | Site-assembled | 3 | 5% ($75M / $1429M) | Polyhedral geometry requires on-site assembly; modules may be factory-fabricated but integration is site-specific |
| C220102 Shield | Site-assembled | 3 | 1% ($12M) | Shield modules factory-cast, site-installed around blanket |
| C220103 SC Coils | Factory module | 5 | 10% ($150M) | **Key advantage**: Six independent non-interlocking coil assemblies, each factory-wound and tested. Park 2025: "compact, non-interlocking coils that can be easily assembled and disassembled in a modular manner." |
| C220104 E-beam | Factory module | 5 | 7% ($100M) | Commercial e-beam injectors are factory-manufactured units. Multiple beams installed on-site but each is a discrete module. |
| C220105 Structure | Site-assembled | 3 | 0.1% ($2M) | Minimal; compact device |
| C220106 Vacuum | Factory module | 5 | 0.2% ($3M) | Vacuum vessel for 1.6 m cube is small enough to be factory-fabricated and shipped whole |
| C220107 Power Supplies | Factory module | 5 | 3% ($40M) | Standard electrical equipment |
| C220110 Remote Handling | Factory module | 5 | 2% ($23M) | Modular RH tools, not custom-built on-site |
| C220200 Coolant Systems | Site-assembled | 3 | 4% ($62M) | Piping and HX partially modular, but site-integrated |
| C220300 Cryoplant | Factory module | 5 | 9% ($124M) | Large cryoplant is modular (standard industrial equipment) |
| C220500 Fuel Handling | Site-assembled | 3 | 3% ($45M) | Tritium systems are complex, site-integrated |
| CAS23 Turbine | Factory module | 5 | 5% ($73M) | Standard turbine-generator set |
| CAS24 Electric | Factory module | 5 | 2% ($31M) | Standard switchgear |
| CAS25 Misc | Factory module | 5 | 1% ($19M) | Cranes, HVAC, etc. |
| CAS26 Heat Rejection | Site-assembled | 3 | 1% ($13M) | Cooling towers partially modular |

**Cost-weighted average**:
- Stick-built (score 1): 13% weight → 0.13
- Site-assembled (score 3): 18% weight → 0.54
- Factory module (score 5): 69% weight → 3.45
- **Raw average**: 0.13 + 0.54 + 3.45 = 4.12

**Module repetition boost**: The six independent SC coils are identical modules within a single plant (6 units). This is below the 10-unit threshold for the +1.0 boost. No boost applied.

**C1 = 4.12 (no boost), clamped to [1, 5] → 4.1**

**Justification**: The Polywell scores well on modularization because the reactor core (coils, e-beam, vacuum vessel, cryoplant) is compact and non-interlocking, enabling factory manufacture of the most expensive components. The 69% factory-module fraction (by capital cost) is higher than most MFE concepts, which have interlocked TF coils requiring on-site assembly. However, the BOP (buildings, coolant systems, fuel handling, heat rejection) is conventional stick-built or site-assembled, pulling the score down from 5.0. The six-coil modular advantage is real but doesn't qualify for the repetition boost (below 10 units).

---

### C3: Supply Chain Learning (3 sub-factors, equal weight)

**Score: 3.3**

**Sub-factor A: Component learning rates (cost-weighted across CAS accounts)**

| Component | Learning Rate Category | Score | Cost Weight | Notes |
|-----------|----------------------|-------|-------------|-------|
| Buildings (CAS21) | Commodity construction | 5 | 13% | Steel, concrete — mature |
| Blanket/FW (C220101) | Fusion-specific novel | 2 | 5% | Polyhedral geometry breeding blanket never manufactured; TRL 1 |
| Shield (C220102) | Specialty component | 3 | 1% | Borated steel/concrete; limited supply but existing |
| SC Coils (C220103) | Industrial growing | 4 | 10% | REBCO/Nb₃Sn for fusion ramping but limited production base |
| E-beam (C220104) | Industrial growing | 4 | 7% | Commercial e-beam systems exist but 78 MW integrated is novel |
| Structure (C220105) | Commodity | 5 | 0.1% | Steel structures |
| Vacuum (C220106) | Commodity | 5 | 0.2% | Standard vacuum tech |
| Power Supplies (C220107) | Commodity | 5 | 3% | Standard HV electrical |
| Remote Handling (C220110) | Specialty | 3 | 2% | Fusion-specific but analogues exist |
| Coolant (C220200) | Industrial growing | 4 | 4% | Heat exchangers mature; fusion-specific coolants (LiPb?) limited |
| Cryoplant (C220300) | Industrial growing | 4 | 9% | Large cryoplants exist but fusion-scale SC is growing |
| Fuel Handling (C220500) | Fusion-specific | 2 | 3% | Tritium handling limited to CANDU, fusion labs |
| Turbine (CAS23) | Commodity | 5 | 5% | Steam turbines mature |
| Electric (CAS24) | Commodity | 5 | 2% | Switchgear mature |
| Misc (CAS25) | Commodity | 5 | 1% | HVAC, cranes mature |
| Heat Rejection (CAS26) | Commodity | 5 | 1% | Cooling towers mature |

**Weighted average**: (5×13% + 2×5% + 3×1% + 4×10% + 4×7% + 5×0.1% + 5×0.2% + 5×3% + 3×2% + 4×4% + 4×9% + 2×3% + 5×5% + 5×2% + 5×1% + 5×1%) = 0.65 + 0.10 + 0.03 + 0.40 + 0.28 + 0.005 + 0.01 + 0.15 + 0.06 + 0.16 + 0.36 + 0.06 + 0.25 + 0.10 + 0.05 + 0.05 = **3.7**

**Sub-factor B: Supply chain bottleneck count**

Start at 5.0 and subtract penalties:

- **Tritium self-sufficiency (blanket design unresolved)**: Hard constraint (no known path to TBR > 1.0 in polyhedral geometry). Penalty: **-1.0**.
- **Superconductor scaling**: REBCO or Nb₃Sn production must scale 10× for global fusion buildout. Scaling constraint. Penalty: **-0.5**.
- **Li-6 enrichment (if required)**: Polyhedral blanket may need higher enrichment to compensate for coil shadowing. Scaling constraint (Li-6 enrichment capacity limited). Penalty: **-0.5**.
- **Sole-source dependency**: E-beam systems and cryoplants have multiple vendors (Leybold, Sciaky, Linde, Air Liquide). No sole-source penalty. Penalty: **0**.

**Sub-factor B = 5.0 - 1.0 - 0.5 - 0.5 = 3.0**

**Sub-factor C: External demand pull (fraction of capital with >$1B/yr external market)**

| Component | External Market? | Cost ($M) | Fraction |
|-----------|------------------|-----------|----------|
| Buildings (CAS21) | Yes (construction) | $186M | 13% |
| Turbine (CAS23) | Yes (power gen equipment) | $73M | 5% |
| Electric (CAS24) | Yes (switchgear) | $31M | 2% |
| Misc (CAS25) | Yes (industrial HVAC, cranes) | $19M | 1% |
| Heat Rejection (CAS26) | Yes (cooling towers) | $13M | 1% |
| Cryoplant (C220300) | Yes (industrial cryogenics) | $124M | 9% |
| Power Supplies (C220107) | Yes (HV electrical) | $40M | 3% |
| Vacuum (C220106) | Yes (vacuum tech) | $3M | 0.2% |
| **Total with external demand** | | **$489M** | **34%** |

Fraction = 34% → **Sub-factor C = 3** (20–40% bracket per framework)

**C3 = (3.7 + 3.0 + 3.0) / 3 = 3.2 → 3.2**

**Justification**: The Polywell scores moderately on supply chain learning because ~65% of capital cost is in fusion-specific or limited-supply-chain components (SC coils, e-beam, blanket, tritium fuel handling). The polyhedral breeding blanket is a hard constraint (no demonstrated path to TBR > 1.0, TRL 1). SC conductor and Li-6 enrichment are scaling constraints. External demand pull is limited to 34% (buildings, turbine, electrical, cryoplant) — most of the reactor core has no external market. Learning rates are better than ITER-scale tokamaks (no divertor, smaller magnets) but worse than concepts with higher commodity content.

---

### C4: Plant Complexity (2 sub-factors, equal weight)

**Score: 3.5**

**Sub-factor A: Operational coupling density**

Rate failure cascades and maintenance dependencies focusing on OPERATIONAL coupling (if component X fails, what else stops working?), not physics coupling.

The Polywell has **moderate coupling**. Major failure cascade paths:

1. **Cryoplant failure → SC coil quench → plasma loss → full shutdown**: The six SC coils require continuous cryogenic cooling. Cryoplant trip cascades to immediate plasma termination. Magnet quench may require days-to-weeks warm-up/cool-down cycle. **High coupling**.

2. **E-beam injector failure → plasma loss → full shutdown**: The 78 MW e-beam injection is required to sustain the electrostatic well. Loss of one beam (out of 10–20 beams) may be tolerable with redundancy, but loss of multiple beams or power supply failure cascades to plasma loss. **Moderate coupling** (depends on redundancy design).

3. **Blanket coolant loop failure → overheating → forced shutdown**: 784 MW of neutron power deposits in the blanket. Loss of coolant forces immediate shutdown to prevent first-wall damage. **Standard MFE coupling** (shared with all D-T concepts).

4. **Tritium processing failure → fuel starvation → shutdown within hours**: D-T fuel cycle requires continuous tritium extraction and purification. Processing failure doesn't cascade immediately (fuel inventory provides buffer) but forces shutdown within hours to days. **Moderate coupling** (shared with all D-T concepts).

5. **Vacuum failure → plasma contamination → shutdown**: 1.6 m cube vacuum vessel is compact; leak detection and isolation should be faster than ITER-scale systems. **Low coupling** (small vessel advantage).

**Relative to tokamaks**: The Polywell has **fewer critical interdependencies** than ITER-scale MFE:
- No divertor (eliminates divertor-PFC-coolant cascade failure path)
- No plasma position control system (no disruption-induced component damage cascade)
- Smaller vacuum vessel (faster leak isolation)

**Relative to simple concepts (IFE, some pulsed concepts)**: The Polywell has **more coupling** due to steady-state operation requiring continuous cryogenic, e-beam, and coolant systems.

**Verdict**: Moderate coupling (score 3). The cryoplant and e-beam are single-point failures with full-plant cascade, but the compact geometry and lack of divertor reduce complexity vs. large tokamaks.

**Sub-factor A = 3.0**

**Sub-factor B: Subsystem count (CAS22 sub-accounts representing >1% of total capital)**

Count from baseline cost model (total capital $1748M, threshold $17.5M):

| CAS Account | Cost ($M) | >1% threshold? |
|-------------|-----------|----------------|
| C220101 Blanket | $75M | Yes (4.3%) |
| C220102 Shield | $12M | No (0.7%) |
| C220103 SC Coils | $150M | Yes (8.6%) |
| C220104 E-beam | $100M | Yes (5.7%) |
| C220105 Structure | $2M | No |
| C220106 Vacuum | $3M | No |
| C220107 Power Supplies | $40M | Yes (2.3%) |
| C220110 Remote Handling | $23M | Yes (1.3%) |
| C220111 Installation Labor | $57M | Yes (3.3%) |
| C220200 Coolant Systems | $62M | Yes (3.5%) |
| C220300 Cryoplant | $124M | Yes (7.1%) |
| C220400 Rad Waste | $2M | No |
| C220500 Fuel Handling | $45M | Yes (2.6%) |
| C220600 Other Equipment | $4M | No |
| C220700 I&C | $39M | Yes (2.2%) |

**Significant subsystems**: 10 (Blanket, SC Coils, E-beam, Power Supplies, Remote Handling, Installation, Coolant, Cryoplant, Fuel Handling, I&C)

Per framework: 8–10 subsystems → **score 3**

**Sub-factor B = 3.0**

**C4 = (3.0 + 3.0) / 2 = 3.0**

**Justification**: The Polywell has moderate plant complexity. Operationally, the cryoplant and e-beam injection systems are critical single-point failures with full-plant shutdown cascades, but the lack of divertor and compact geometry reduce coupling vs. ITER-scale tokamaks. The subsystem count (10 significant CAS22 accounts) is typical for a D-T thermal-cycle fusion plant — fewer than ITER (which has divertor, plasma control, etc.) but more than simple pulsed concepts. The "magic wand" test: if the physics were proven tomorrow (γ=0.1 validated), the plant would still require steady-state cryogenic, e-beam, and coolant systems with nontrivial operational coupling. The polyhedral geometry is novel but not inherently more complex than toroidal geometry for operations.

---

### C5: Customization Needs (2 sub-factors)

**Score: 1.8 → scaled to 3.4**

**Sub-factor A: Thermal rejection (1-4 scale)**

The Polywell is a **thermal-cycle concept** with ~1058 MW thermal power (baseline model) rejected through a conventional steam or sCO₂ cycle. No thermal rejection advantage vs. standard MFE.

- Not air-cooled or direct-conversion-only (score 4)
- Not hybrid (score 3)
- Standard thermal cycle with large cooling towers required (score 2)

**Sub-factor A = 2**

**Sub-factor B: Fuel safety profile (1-4 scale)**

The Polywell uses **D-T fuel** with full tritium handling and breeding infrastructure.

- Not p-B11 (score 4)
- Not D-He3 (score 3)
- Not D-D (score 2)
- D-T with tritium breeding (score 1)

**Sub-factor B = 1**

**Raw C5 = (2 + 1) / 2 = 1.5**

**Scaled to [1, 5] range**: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = **1.7 → 1.7**

Wait, let me recalculate per the framework formula:

Raw = (A + B) / 2 = (2 + 1) / 2 = 1.5
Scaled: C5 = 1 + (raw - 1) × (4/3) = 1 + (1.5 - 1) × 1.333 = 1 + 0.5 × 1.333 = 1 + 0.667 = **1.67 → 1.7**

Hmm, the framework says "scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)". Let me verify the calculation:

- Raw = 1.5 (range is [1, 4] for the raw sub-factor average)
- Scaled = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = 1.667

Round to one decimal: **C5 = 1.7**

**Justification**: The Polywell has high customization needs due to D-T fuel (full tritium infrastructure required) and standard thermal cycle (large cooling towers and site water access required). There is no site-specific advantage — the compact 1.6 m device still requires the same tritium handling, biological shielding, and thermal rejection infrastructure as any D-T fusion plant. The only potential site flexibility is the small reactor building footprint, but this doesn't offset the D-T fuel penalty.

---

### C8: Data Adequacy (4 sub-factors, equal weight)

**Score: 2.4**

**Sub-factor A: Source diversity & independence (1-5)**

- **Available**: Park et al. 2025 (arXiv preprint, EMC2-authored); Park et al. 2015 (Phys. Rev. X, peer-reviewed); EMC2 website (minimal); Wikipedia (comprehensive history, secondary source); FPNS proposal (EMC2/SHINE, DOE-submitted).
- **Independent validation**: None. No independent group has reproduced WB-X results or validated Park 2025 scaling. University of Sydney (2019) contradicts EMC2 claims (no virtual cathode formation at high density) — contested but not refuted.
- **Public-domain architecture literature**: Rogers 2018 (J. Fusion Energy, p-B11 variant, not extracted) may contain architecture but is company-affiliated. No independent academic reactor study exists.

**Verdict**: Almost exclusively company publications with contested external critique. No independent peer-reviewed reactor study. **Score: 2** (between "almost exclusively company" and "mix with some validation").

**Sub-factor B: Reactor design specification (1-5)**

- **Available**: Park 2025 provides physics scaling to reactor power levels (980 MW fusion, 78 MW beam, 4.5 T field, 1.6 m cube). This is a **preliminary design** with major subsystems defined (coils, e-beam, plasma parameters) but gaps in integration (no blanket, no thermal cycle, no BOP).
- **Missing**: Blanket design, thermal cycle, neutronics, tritium breeding, PFC heat flux management, maintenance strategy, capital cost.

**Verdict**: Partial design with key subsystems defined but significant specification gaps. **Score: 3** (matches framework: "partial design with key subsystems defined but gaps in integration").

**Sub-factor C: LCOE parameter coverage (1-5, based on blocking gap count)**

From gap_report.md summary (lines 159–171), blocking gaps identified:

1. Loss reduction factor γ — no experimental validation
2. Virtual cathode formation at commercial densities — contested, no EMC2 counter-data
3. Energy conversion architecture — no thermal cycle
4. Net electrical output and recirculating power — derivable once (3) resolved
5. Tritium breeding blanket design — polyhedral geometry, no neutronics study
6. Capital cost breakdown by CAS — no plant study
7. (Bremsstrahlung is listed as "important", not blocking)
8. (SC coil design is listed as "important", not blocking)

**Count: 6 blocking gaps** (items 1-6 above)

Per framework: 5–7 blocking gaps → **score 2**

**Sub-factor D: Commercialization pathway clarity (1-5)**

- **Available**: FPNS program (350 kW fusion neutron source, $20M/24 months, partnership with SHINE Technologies for medical isotope production) is the stated near-term milestone. Park 2025 acknowledges FPNS as a "stepping stone" to power reactors but provides no commercialization timeline, funding plan, or reactor demonstration roadmap beyond FPNS.
- **Missing**: No power reactor demonstration plan. No identified funding beyond FPNS. No timeline for reactor-scale prototype. No commercialization partners beyond SHINE (neutron source only).

**Verdict**: General pathway (FPNS → larger device → reactor) described but lacking specifics on timeline, funding, or steps beyond FPNS. **Score: 3** (matches framework: "general pathway described but lacking specifics").

**C8 = (2 + 3 + 2 + 3) / 4 = 2.5 → 2.5**

**Justification**: Data adequacy is poor. The single reactor-scale study (Park 2025) is an EMC2-authored arXiv preprint with no independent validation. Six blocking gaps exist for LCOE modeling (γ validation, thermal cycle, blanket design, capital cost, virtual cathode, net electric output). The commercialization pathway is vague beyond FPNS (which is a neutron source, not a power reactor). Source diversity is limited to EMC2 publications and secondary sources. The concept has published more than many exotic concepts (2 peer-reviewed papers vs. 0 for some) but far less than mainstream MFE (decades of tokamak data).

---

### C7: Technical Risk Evidence (7 functions × 2 subcategories = 14 cells)

I will now fill the full risk matrix with all required fields for each cell.

---

#### F1: Plasma Performance

**F1 Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Plasma density n ~10²¹ m⁻³, ion temperature Ti = 20 keV, electron confinement time sufficient to sustain virtual cathode potential well depth ~60 kV for D-T fusion at Q_sci ≥ 10 |
| Best demonstrated | WB-X (2013, Phys. Rev. X 2015): high-beta electron confinement at β ~1, hard X-ray emission increased by order of magnitude at 13.8 cm coil scale, sub-microsecond pulses. No sustained fusion; no reactor-relevant density or temperature demonstrated. |
| Gap ratio | Density: 10²¹ / ~10¹⁸ (WB-X estimated) = 1000×. Duration: steady-state / <1 μs = ∞ (transient vs. steady). Temperature: 20 keV / ~keV-scale (WB-X, not specified) ≈ 10–20×. |
| Closure mechanism | Park 2025 scaling laws extrapolate WB-X results to reactor scale using 2D PIC simulations. Authors acknowledge: "currently, we lack a quantitative model for the reduction in the loss rate. Therefore, we will use a parametric expression to represent the reduction in the energy loss rate with γ=0.1." FPNS program at 2–3 T, 350 kW fusion is the next experimental step. |
| Classification | **Binary** — if virtual cathode does not form at reactor density or if γ > 0.18, net electric output is negative and the concept cannot generate power. |
| Evidence tier | **Tier 2** — subscale demonstration (WB-X) at <0.1% of reactor density, transient only. Park 2025 scaling is simulation-based extrapolation with unvalidated free parameter (γ). University of Sydney (2019) contradicts feasibility ("little or no trace of virtual electrode formation" at higher densities); EMC2 disputes but has not published counter-experimental evidence. FPNS is a design, not operating hardware. |

**F1 Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Polyhedral magnetic cusp geometry with 4.5 T superconducting coils at 1.6 m cube scale, steady-state operation, plasma-facing surfaces survive 14.1 MeV neutron flux at ~0.5 MW/m² wall loading for 5 FPY. |
| Best demonstrated | WB-8 (2010–2012): 0.8 T resistive copper coils, ~10 cm coil scale, 500+ plasma shots with pulse lengths ~100 ms. No superconducting coils. No steady-state operation. No neutron wall loading (no fusion). EMC2 reportedly began SC Polywell work in 2012; no published results. |
| Gap ratio | Field: 4.5 T / 0.8 T = 5.6×. Scale: 1.6 m / ~0.2 m (WB-8 coil diameter) = 8×. Neutron fluence: 5 FPY at 0.5 MW/m² / 0 (no fusion in WB-8) = ∞. Duration: steady-state / 100 ms = 10⁴× extrapolation. |
| Closure mechanism | SC coil design study (not published). FPNS will use SC coils at 2–3 T, 8.5–10 cm plasma radius, but not at reactor neutron flux. Park 2025 notes "commercial-grade MW-class electron beam injectors are available" and claims "compact, non-interlocking coils that can be easily assembled and disassembled in a modular manner." |
| Classification | **Degrading** — SC coil failure or PFC damage forces shutdown and replacement (cost/schedule penalty), but does not invalidate the physics. Coil quench or neutron damage reduces availability, not fundamental viability. |
| Evidence tier | **Tier 2** — WB-8 resistive coils are not analogous to 4.5 T SC at steady-state. FPNS SC coil design exists but is not yet operating. No demonstrated SC Polywell at any scale. Neutron wall loading is unaddressed (no reactor-scale PFC or first-wall design). |

**F1 Mean: (2 + 2) / 2 = 2.0**

---

#### F2: Driver / Energy Input

**F2 Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | 60 keV electron beam at 1.3 kA per injector, ~78 MW total beam power, injected into polyhedral magnetic cusp with beam-plasma coupling efficiency sufficient to sustain virtual cathode. Beam must thermalize at plasma center to form potential well depth ~60 kV. |
| Best demonstrated | WB-series devices used plasma guns and thermionic emitters at kV-scale, not MW-class beams. No published data on beam-plasma coupling efficiency in a Polywell cusp. Park 2025 cites "off-the-shelf availability" of 60 keV electron beams but provides no experimental validation of coupling into the magnetic cusp geometry. |
| Gap ratio | Beam power: 78 MW / ~kW-scale (WB-series, not specified) ≈ 10⁴–10⁵×. Coupling efficiency unknown (never measured at MW scale). |
| Closure mechanism | Commercial electron beam systems exist at MW-class for industrial applications (materials processing). Park 2025 assumes beam-plasma coupling is efficient based on 2D PIC simulations. FPNS will use 5–6 MW ion beams (not e-beams) for a different operational mode. |
| Classification | **Degrading** — if beam-plasma coupling is poor (e.g., 50% instead of assumed 80–90%), more beam power is required, raising recirculating power fraction and worsening LCOE. This does not invalidate the concept, only degrades economics. |
| Evidence tier | **Tier 2** — Commercial e-beam systems exist at MW-class in non-fusion applications (adjacent analogue). No demonstrated MW-class e-beam injection into a magnetized cusp. FPNS will use ion beams, not e-beams, so provides no direct validation. Beam-plasma coupling is simulated, not measured. |

**F2 Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | 10–20 independent 60 keV, ~4–8 MW electron beam injectors, total 78 MW, continuous operation (CW), injected into magnetic cusp with neutron and X-ray environment. Beam injector lifetime ≥5 FPY under neutron fluence ~10²³ n/m² (14.1 MeV). Power supply efficiency ≥85%. |
| Best demonstrated | Commercial electron beam systems: Leybold, Sciaky, Ferrotec manufacture MW-class CW e-beams at 60 keV for materials processing (vacuum metallurgy, welding). Operating in non-neutron environment. No fusion-specific e-beam injection system demonstrated. |
| Gap ratio | Neutron environment: 10²³ n/m² / 0 (commercial beams) = ∞. Integrated system: 78 MW / ~MW-class single units = 78× (if no commercial multi-MW single unit exists). Reliability: 5 FPY CW / industrial duty cycle (not specified) ≈ 10× (fusion requires higher reliability). |
| Closure mechanism | Park 2025 states "off-the-shelf availability of steady-state electron beam injectors with power levels of tens of megawatts." Multiple commercial vendors exist. Integration engineering and neutron shielding of injectors required but not fundamentally novel. |
| Classification | **Degrading** — beam injector failure or power supply inefficiency raises recirculating power and LCOE, but does not invalidate the concept. Neutron damage to injectors shortens replacement cycle (cost penalty), not a fundamental blocker. |
| Evidence tier | **Tier 3** — subscale demonstrated at MW-class in non-fusion (adjacent) environment. Commercial vendors provide reliability data for industrial e-beams. Fusion-specific integration (neutron shielding, multiple beams into cusp geometry) is undemonstrated but analogous to NBI systems in tokamaks. |

**F2 Mean: (2 + 3) / 2 = 2.5**

---

#### F3: Instability Control

**F3 Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Suppression or tolerance of electrostatic and magnetohydrodynamic instabilities in a high-beta (β ~1) non-Maxwellian plasma with electrostatic ion confinement and magnetic electron confinement. Plasma must remain stable for steady-state operation (years, not seconds). |
| Best demonstrated | WB-X (2015): demonstrated high-beta (β ~1) electron confinement for sub-microsecond pulses with hard X-ray emission order-of-magnitude increase. No long-pulse stability data. Park 2025 notes "experiments conducted at varying cusp magnetic field strengths showed that both too low and too high magnetic fields reduce confinement, indicating the existence of an optimal β value, β ~1." |
| Gap ratio | Duration: steady-state / <1 μs = ∞. Beta regime: β ~1 at reactor density 10²¹ m⁻³ / β ~1 at WB-X density ~10¹⁸ m⁻³ = 1000× density extrapolation at same beta (different stability regime). |
| Closure mechanism | Park 2025 scaling assumes high-beta confinement observed in WB-X generalizes to reactor conditions. Authors acknowledge: "the gyroradius scaling exponent is preliminary and needs to be validated by future experiments and/or simulations." FPNS will provide longer-pulse high-beta data at intermediate scale. |
| Classification | **Binary** — if high-beta plasma is unstable at reactor density or if instabilities cause loss of virtual cathode, the concept cannot achieve net fusion power. MHD or electrostatic instabilities that disrupt the potential well collapse the confinement mechanism. |
| Evidence tier | **Tier 2** — WB-X demonstrated β ~1 stability transiently at low density. Steady-state stability at reactor density is undemonstrated and predicted by PIC simulations only. No theoretical proof or experimental validation that cusp-confined high-beta plasma is MHD-stable at 10²¹ m⁻³ for extended duration. |

**F3 Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Magnetic field coils maintain 4.5 T boundary field with sufficient ripple control and field uniformity to prevent electron loss. Coil quench protection system handles stored magnetic energy ~GJ-scale (6 coils × 4.5 T × ~m³-scale volume). Electromagnetic forces from plasma pressure at β ~1 do not deform coil structure beyond tolerance. |
| Best demonstrated | WB-8: 0.8 T resistive coils with field ripple tolerance demonstrated for 100 ms pulses. No quench protection system (resistive coils). No structural loading from high-beta plasma at reactor scale. Tokamak analogue: ITER TF coils handle quench protection and structural loading at 11.8 T but in interlocked geometry (not applicable). |
| Gap ratio | Field: 4.5 T / 0.8 T = 5.6×. Stored energy: GJ-scale / kJ-scale (WB-8, estimated) ≈ 10⁶×. Structural loading: plasma pressure at β ~1, 10²¹ m⁻³ / WB-8 pressure ~0 (no fusion) = ∞. Duration: steady-state / 100 ms = 10⁴×. |
| Closure mechanism | SC coil design study with quench protection and structural analysis (not published). Park 2025 claims non-interlocking geometry enables modular coil assembly, implying independent structural support per coil. ITER and tokamak experience provides quench protection analogues (different geometry). |
| Classification | **Degrading** — coil structural failure or quench damage forces shutdown and replacement (cost/schedule penalty). Does not invalidate physics if coils are repaired/replaced. |
| Evidence tier | **Tier 2** — WB-8 resistive coils are not analogous to SC at 4.5 T. ITER SC coil quench protection is analogous in principle but different geometry (toroidal interlocked vs. polyhedral independent). No polyhedral SC cusp coil demonstrated at any field strength. Structural loading from high-beta plasma is unaddressed (no design). |

**F3 Mean: (2 + 2) / 2 = 2.0**

---

#### F4: Plasma-Wall Interaction

**F4 Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Heat flux at plasma-facing cusp regions <10 MW/m² (within material limits for tungsten or carbon-based PFCs). Plasma exhaust through cusp points must not cause excessive erosion or impurity influx that contaminates core plasma. Helium ash removal sufficient to prevent dilution. |
| Best demonstrated | WB-X: sub-microsecond pulses, no steady-state heat flux data. FPNS target: 350 kW fusion power → ~280 kW neutron power + ~70 kW alpha power. Heat flux at cusp regions not specified in FPNS proposal. No PFC erosion measurements in any WB-series device. |
| Gap ratio | Heat flux: reactor ~MW/m² / FPNS <kW/m² (estimated) ≈ 1000×. Duration: steady-state / transient = ∞. Erosion: 5 FPY cumulative / 0 (no WB-series erosion data) = ∞. |
| Closure mechanism | Park 2025 mentions "naturally diverging magnetic fields at plasma-facing surfaces" for heat spreading, but provides no heat flux calculation or PFC design. Analogy to tokamak divertor physics (particle flux, heat flux) is weak because cusp geometry is fundamentally different (open-field-line exhaust vs. closed-field divertor). |
| Classification | **Degrading** — excessive heat flux shortens PFC lifetime and increases replacement frequency (cost penalty). If heat flux exceeds material limits (>20 MW/m² for tungsten), PFC damage forces frequent shutdowns, worsening capacity factor. Does not invalidate concept, only degrades economics. |
| Evidence tier | **Tier 1** — no heat flux measurements or PFC erosion data exist for any Polywell device. Park 2025 mentions heat management qualitatively but provides no quantitative analysis. FPNS will provide first data at 350 kW scale (far below reactor). Analogues (tokamak divertor) are in different geometry and not directly applicable. |

**F4 Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Plasma-facing components (PFCs) at cusp regions survive 5 FPY under combined heat flux (~MW/m²), 14.1 MeV neutron flux (~0.5 MW/m² wall loading, ~2 dpa/FPY), and plasma erosion. PFC material: tungsten or carbon-based armor with active cooling. Replacement schedule: 5–10 FPY per PFC module. |
| Best demonstrated | No Polywell-specific PFC. Tokamak analogue: ITER tungsten divertor qualified for 10 MW/m² steady-state heat flux and 0.7 dpa/FPY in ITER neutron spectrum (different from Polywell 14.1 MeV D-T neutrons). WEST tokamak: 1000+ tungsten-divertor pulses at 5 MW/m². FPY lifetime not yet demonstrated in any tokamak divertor. |
| Gap ratio | Neutron spectrum: 14.1 MeV D-T / ITER mixed spectrum (not directly comparable, but ITER is fission-like, not 14 MeV). Geometry: polyhedral cusp PFC / toroidal divertor = different erosion pattern. FPY lifetime: 5 FPY target / 0 FPY demonstrated (ITER will be first) = ∞. |
| Closure mechanism | PFC design study (not published). Tungsten armor with water or helium cooling (standard tokamak technology). Park 2025 assumes cusp geometry spreads heat flux, reducing peak loads, but provides no engineering design or thermal analysis. |
| Classification | **Degrading** — PFC failure forces shutdown and replacement. If replacement frequency is higher than assumed (e.g., 2 FPY instead of 5 FPY), O&M costs increase and capacity factor degrades. Does not invalidate concept. |
| Evidence tier | **Tier 3** — tokamak tungsten PFC qualified at heat flux and partial neutron dose in adjacent environment (fission-like spectrum, not 14 MeV). Polyhedral cusp PFC is undemonstrated. FPNS will provide first Polywell-specific PFC data at 350 kW scale (subscale). 5 FPY lifetime in 14 MeV neutron environment is undemonstrated for any PFC (ITER will be first data, not yet operating). |

**F4 Mean: (1 + 3) / 2 = 2.0**

---

#### F5: Neutron/Particle Handling

**F5 Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | 14.1 MeV neutron production at ~980 MW fusion power → 784 MW neutron power (80% of fusion). Neutron activation and damage to coils, structure, and blanket within design limits for 5 FPY core lifetime. Helium production in structural materials and coils <material embrittlement limits. |
| Best demonstrated | No D-T fusion in any Polywell device (WB-6 achieved ~10⁹ D-D neutrons/s at 12.5 kV, reported by Bussard 2006 but not peer-reviewed). 14.1 MeV neutron activation is identical to all D-T fusion concepts — no Polywell-specific physics risk, only geometry-specific activation patterns. |
| Gap ratio | Neutron power: 784 MW / 0 (no D-T in WB-series) = ∞. D-D neutrons in WB-6 at ~10⁹ n/s are ~10¹⁰× lower flux than reactor (D-T at 980 MW → ~10²⁰ n/s). |
| Closure mechanism | D-T neutron physics is well-understood (ENDF/B cross-section libraries, fission reactor experience, tokamak D-T campaigns at JET/TFTR). Polyhedral geometry activation and shielding require MCNP analysis (not published). Park 2025 acknowledges neutron shadowing by coils as a breeding challenge but does not address activation or He production. |
| Classification | **Degrading** — excessive neutron activation or He production shortens coil and structure lifetime (replacement cost penalty) but does not prevent fusion. Shielding adds cost but is solvable. |
| Evidence tier | **Tier 2** — 14.1 MeV D-T neutron production physics is well-understood from fission and tokamak analogues (JET 1997 D-T at 16 MW peak fusion power, TFTR). Polyhedral geometry-specific activation is unanalyzed (MCNP/Serpent study required). No operating Polywell neutron source yet (FPNS is design). |

**F5 Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Superconducting coils, blanket structure, and vacuum vessel survive neutron fluence ~10²³ n/m² over 5 FPY (at 80% capacity factor, 0.5 MW/m² wall loading). Displacement damage: <200 dpa in first wall; <10 dpa in coils (shielded). Helium production: <1000 appm in steel structures. Tritium permeation through steel <loss rate limits. |
| Best demonstrated | Fission fast reactors: stainless steel survives 50–80 dpa in fast neutron spectrum over decades. ITER design basis: tungsten first wall at ~0.7 dpa/FPY ITER spectrum (mixed fission-like), 316 stainless steel blanket structure at ~20 dpa over 6 FPY (design target, not demonstrated). HTS coils: no neutron irradiation data at fusion-relevant fluence (REBCO degrades above ~10¹⁹ n/cm² per lab studies). |
| Gap ratio | First wall dpa: 200 dpa (5 FPY × 40 dpa/FPY at 2 MW/m² 14 MeV) / 20 dpa (ITER 6 FPY target, not demonstrated) = 10×. Coil neutron fluence: depends on shield thickness (undesigned). HTS degradation: 10²³ n/m² (coil location, shielded) / 10¹⁹ n/cm² (lab REBCO limit) = 10⁴× if poorly shielded. |
| Closure mechanism | Neutronics analysis (MCNP/Serpent) to determine shielding thickness required to keep coil fluence below HTS degradation limit. Fission reactor steel and ITER blanket provide material database for 14 MeV neutrons (FENDL-3.2 library). Park 2025 assumes shielding is sufficient but provides no design. |
| Classification | **Degrading** — neutron damage shortens blanket/coil lifetime (replacement cost penalty). If shielding proves inadequate and coils must be replaced every 5 FPY instead of 20 FPY, capital and O&M costs increase. Does not invalidate concept. |
| Evidence tier | **Tier 3** — fission fast reactor steel at 50–80 dpa provides partial analogue (different neutron spectrum). ITER steel blanket at 20 dpa is design basis (not demonstrated). HTS coil neutron tolerance is lab-scale only; no fusion-relevant fluence demonstrated. Polyhedral geometry shielding is undesigned; MCNP analysis required (Tier 2 without shield design). |

**F5 Mean: (2 + 3) / 2 = 2.5**

---

#### F6: Fuel Cycle Closure

**F6 Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tritium breeding ratio (TBR) ≥1.10 to account for decay, processing losses, and startup inventory. Tritium extraction from blanket (Li or LiPb) at ≥90% efficiency. Fuel burnup fraction ≥5% per pass. Tritium recycling and purification sufficient to close fuel cycle with <10% external tritium purchase. |
| Best demonstrated | No tritium breeding in any Polywell device. D-T fuel cycle closure demonstrated in tokamaks: TFTR and JET achieved tritium injection and D-D/D-T operation with tritium recycling (not breeding). ITER design targets TBR = 1.15 with test blanket modules (not demonstrated). No tokamak has closed the fuel cycle without external tritium supply. |
| Gap ratio | TBR: ≥1.10 required / 0 (no Polywell blanket) = ∞. Polyhedral coil geometry creates neutron shadowing challenge acknowledged by Park 2025: "tritium breeding blankets can operate in regions of low magnetic field strength, providing opportunities for innovative breeding solutions to address neutron shadowing caused by internal coil structures." No TBR calculation exists. |
| Closure mechanism | Liquid lithium or LiPb blanket with Li-6 enrichment (if natural Li is insufficient). Neutronics analysis (MCNP/Serpent) required to determine achievable TBR in polyhedral geometry. If TBR < 1.0, concept must pivot to D-D (100× lower cross-section, nonviable Q) or external tritium purchase (cost prohibitive at ~$30M/kg, ~$1.6B/yr for 55 kg/yr consumption). |
| Classification | **Binary** — if TBR < 1.0 and cannot be resolved by blanket design, the D-T concept is nonviable. External tritium purchase at scale is economically prohibitive and supply-limited. Tritium self-sufficiency is mandatory for D-T power reactors. |
| Evidence tier | **Tier 2** — ITER TBR = 1.15 is design target based on MCNP neutronics with FENDL-3.2 cross-sections (not demonstrated). Polyhedral cusp geometry TBR is unanalyzed (no neutronics study). Coil shadowing is acknowledged challenge. Tokamak breeding blanket designs (HCPB, WCLL) are adjacent analogues but not directly applicable to polyhedral geometry. |

**F6 Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tritium breeding blanket with TBR ≥1.10, operating temperature 300–900°C (depending on coolant: water, LiPb, FLiBe, or helium), tritium extraction efficiency ≥90%, blanket lifetime ≥5 FPY under 14.1 MeV neutron flux (~40 dpa). Tritium processing plant handles ~55 kg/yr throughput with <1% loss rate. Tritium permeation barriers on all steel surfaces. |
| Best demonstrated | Fission breeder blanket analogue: MSRE (Molten Salt Reactor Experiment) operated FLiBe at 650°C with tritium extraction (fission neutrons, not 14 MeV fusion). ITER blanket modules (HCPB, WCLL) designed for TBR ~1.15 in toroidal geometry (not demonstrated). Tritium processing: ITER tritium plant designed for ~1 kg/day throughput (not operated). CANDU reactors process tritium from heavy water at kg/yr scale (operating regime demonstrated). |
| Gap ratio | Blanket geometry: polyhedral cusp / toroidal (ITER) = fundamentally different (neutron shadowing). Neutron spectrum: 14 MeV D-T / mixed fission (MSRE) = different He production rate. Tritium throughput: 55 kg/yr / CANDU kg/yr-scale = ~50× (ITER plant design is bridge). Blanket lifetime: 5 FPY at 40 dpa / MSRE ~0 dpa (fission, not fusion-relevant) = ∞. |
| Closure mechanism | Blanket design study with neutronics (MCNP), thermal-hydraulics (RELAP), and tritium extraction modeling. No Polywell-specific study exists. Park 2025 defers: "opportunities for innovative breeding solutions." ITER and ARIES studies provide design analogues but toroidal geometry is not transferable to polyhedral cusp without custom analysis. |
| Classification | **Binary** (for blanket TBR) + **Degrading** (for tritium processing). If blanket design cannot achieve TBR ≥1.0, concept is nonviable (binary). Tritium processing inefficiency or permeation losses increase operating cost but are solvable (degrading). |
| Evidence tier | **Tier 2** — ITER blanket and tritium plant are design-basis (not operating). MSRE FLiBe and CANDU tritium processing are partial analogues in different environments (fission neutrons, not 14 MeV). Polyhedral blanket is undesigned (no study). TBR < 1.0 is possible (coil shadowing), making this a binary risk. |

**F6 Mean: (2 + 2) / 2 = 2.0**

---

#### F7: Power Conversion & BOP

**F7 Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Thermal power from blanket (neutron capture + alpha thermalization) converts to electricity at ≥35% efficiency. Gross electric ≥370 MWe; net electric ≥240 MWe after recirculating power (e-beam, cryogenic, tritium processing, housekeeping). Power balance closes (net positive). |
| Best demonstrated | No power conversion demonstrated in any Polywell device (no net fusion). Park 2025 mentions "neutrons will be captured in a blanket" but specifies no thermal cycle, coolant, or BOP. Thermal efficiency of 35% (baseline model) is analogy to MFE D-T steam Rankine. |
| Gap ratio | Thermal power: 1058 MW (baseline) / 0 (no Polywell power conversion) = ∞. Net electric: 248 MWe / 0 = ∞. |
| Closure mechanism | Standard steam Rankine (35–42% efficiency) or sCO₂ Brayton (45–48% efficiency) thermal cycle, well-understood from fission and fossil plants. No novel physics; purely engineering design choice. Park 2025 defers BOP design entirely. |
| Classification | **Degrading** — poor thermal efficiency (e.g., 32% saturated steam instead of 40% superheated) reduces net electric and worsens LCOE by ~20%. Power balance failure (negative net electric if γ > 0.18) invalidates concept, but this is F1 physics risk (γ parameter), not F7. |
| Evidence tier | **Tier 5** — commercial steam Rankine cycle at 35–42% efficiency is operating-regime demonstrated at 100+ MWe scale in coal/fission plants. sCO₂ Brayton at 45–48% efficiency is demonstrated at 10 MWe pilots (Tier 3 for sCO₂). Coupling to Polywell-specific blanket (undesigned) is Tier 2 (design study required). Score F7 physics at Tier 5 for Rankine baseline. |

**F7 Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Heat exchangers transfer thermal power from blanket coolant (water, LiPb, FLiBe, or helium) to steam or sCO₂ working fluid. Turbine-generator operates at 370 MWe gross electric (baseline). Coolant chemistry control prevents corrosion and tritium contamination. BOP components survive fusion-specific environment (high tritium permeation, neutron activation of coolant). |
| Best demonstrated | Steam Rankine BOP: commercial operation at GWe scale in fission (PWR, BWR at 33–36% efficiency). sCO₂ Brayton: 10 MWe pilots at Sandia, SwRI (45–48% efficiency demonstrated transiently). Fusion-specific: no BOP operated downstream of a fusion blanket. ITER design includes primary cooling loop (water-cooled blanket modules) but no operating data. |
| Gap ratio | Scale: 370 MWe Polywell / 1000+ MWe commercial PWR = 0.37× (subscale, favorable). Fusion-specific: tritium permeation through HX, neutron-activated coolant (LiPb?), no commercial analogue (ITER will be first). sCO₂: 370 MWe / 10 MWe pilots = 37× scale-up. |
| Closure mechanism | Engineering design study specifying coolant, thermal cycle, and HX design. No Polywell-specific study exists. Steam Rankine at 35–40% efficiency is low-risk (mature technology). sCO₂ Brayton at 45–48% requires scale-up from 10 MWe pilots but is advancing rapidly (DOE STEP program, Kairos Power). |
| Classification | **Degrading** — BOP inefficiency or HX fouling reduces thermal efficiency and net output (cost penalty). Tritium permeation or coolant activation increases O&M cost (chemistry control, cleanup) but does not invalidate concept. |
| Evidence tier | **Tier 5** (for steam Rankine) — PWR/BWR steam cycles operate at 33–36% efficiency in commercial regime at 100+ MWe with 40+ year operating history. Coupling to fusion blanket is Tier 4 (ITER design, not operated). **Tier 3** (for sCO₂ Brayton) — 10 MWe pilots demonstrated transiently; 370 MWe scale-up is ~37× (subscale). Score F7 hardware at Tier 5 for Rankine baseline (most conservative thermal cycle assumption). |

**F7 Mean: (5 + 5) / 2 = 5.0**

---

### Function-Level Means (Before Heritage Credit)

| Function | Physics | Hardware | Mean (unrounded) | Mean (rounded to 0.5) |
|----------|---------|----------|------------------|-----------------------|
| F1 Plasma Performance | 2 | 2 | 2.0 | 2.0 |
| F2 Driver / Energy Input | 2 | 3 | 2.5 | 2.5 |
| F3 Instability Control | 2 | 2 | 2.0 | 2.0 |
| F4 Plasma-Wall Interaction | 1 | 3 | 2.0 | 2.0 |
| F5 Neutron/Particle Handling | 2 | 3 | 2.5 | 2.5 |
| F6 Fuel Cycle Closure | 2 | 2 | 2.0 | 2.0 |
| F7 Power Conversion & BOP | 5 | 5 | 5.0 | 5.0 |

### Heritage Credit Application

The Polywell is **not eligible for heritage credit**. Heritage credit applies only to concepts with good traceability to previous public fusion experiments (tokamak, stellarator, laser IFE, mirror, FRC, etc.). The Polywell has no lineage from publicly-funded large-scale fusion programs:

- Not a tokamak derivative (ITER, JET, etc.)
- Not a stellarator derivative (W7-X, LHD, etc.)
- Not a laser IFE derivative (NIF, HYLIFE)
- Not a mirror derivative (MFTF, TMX)
- Not an FRC derivative

The Polywell's lineage is IEC/Fusor (Farnsworth-Hirsch), which are tabletop-scale devices with no reactor-relevant operating history. WB-series experiments (1989–2013) were small-scale, privately funded (Navy SBIR, EMC2), and none produced net fusion or sustained plasmas. Heritage credit does not apply.

**Function-level means (final, after heritage floor)**: F1=2.0, F2=2.5, F3=2.0, F4=2.0, F5=2.5, F6=2.0, F7=5.0

### Binary Risks

From the risk matrix, the following risks are classified as **Binary**:

1. **F1 Physics: Virtual cathode formation and γ ≤ 0.18 required for net power** — If virtual cathode does not form at reactor density or if γ > 0.18, net electric output is negative and the concept cannot generate power.

2. **F6 Physics: Tritium breeding ratio TBR ≥ 1.0 required for fuel cycle closure** — If TBR < 1.0 in polyhedral geometry and cannot be resolved by blanket design, the D-T concept is nonviable. External tritium purchase at scale is economically prohibitive.

---

### YAML Scores Block

```yaml
---
scores:
  C1: 4.1
  C3: 3.2
  C4: 3.0
  C5: 1.7
  C8: 2.5
  F1: 2.0
  F2: 2.5
  F3: 2.0
  F4: 2.0
  F5: 2.5
  F6: 2.0
  F7: 5.0
  binary_risks:
    - "F1 Physics: Virtual cathode formation and electron confinement (γ ≤ 0.18) required for net power — if virtual cathode does not form at reactor density ~10²¹ m⁻³ or if loss reduction factor γ > 0.18, net electric output is negative"
    - "F6 Physics: Tritium breeding ratio TBR ≥ 1.0 in polyhedral coil geometry — neutron shadowing by six coil faces may prevent TBR ≥ 1.0; no neutronics study exists; external tritium purchase is cost-prohibitive"
---
```
