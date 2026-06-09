## Design Point

- Name: Orbitron commercial module — lower bound (Avalanche Energy product page / CWFest 2023)
- Maturity: paper-concept
- P_native: 0.005 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-orbitron-page.md
  - knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/avalanche-cwfest2023-blog.md

## Section 1: Availability of Data

**Rating: Opaque**

Avalanche Energy's public information consists primarily of press releases, blog posts, and marketing materials. The most substantial technical source is a 2023 CWFest presentation blog post (avalanche-cwfest2023-blog.md) which provides concept-level physics discussion and order-of-magnitude performance estimates for laboratory prototypes. Two peer-reviewed papers exist—"The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons" (AIP Advances, August 2024) and "Mode-enhanced ion loading in a 100 kV orbitron" (Physics of Plasmas, September 2025)—but only abstracts are available in the dossier. No plant-level system studies, detailed cost breakdowns, or engineering design documents are public.

> "capital costs to first commercial operations is less than a billion dollars... company is less than 200 people in headcount"
> — avalanche-cwfest2023-blog.md, §Robin Langtry section

The above quote represents the most specific cost target published. It refers to company-level development cost to first commercial operations, not to the capital cost of a single commercial plant.

The fixed design point specifies D-T fuel at 5 kWe net electric output. However, a critical discrepancy exists: the analyst-patch source (analyst-patch-pb11-fuel-critical.md) asserts that Avalanche's actual target fuel is p-B11, not D-T, and that using D-T assumptions produces a 10× LCOE error. The company's public materials mention both D-T (for near-term FusionWERX neutron source applications) and p-B11 (for longer-term commercial power). This analysis proceeds with the fixed design-point specification (D-T, 5 kWe) while noting the fuel ambiguity as a critical gap.

**Key data gaps:**
1. No published power plant design study for any scale
2. No reactor-level cost breakdown (magnets, vacuum vessel, power supplies, BOP, etc.)
3. No LCOE estimate or economic model from the company
4. No quantitative confinement performance data (density, temperature, confinement time, Q) for any D-T operation — published neutron rates are for D-D
5. No engineering drawings, material specifications, or supply-chain analysis
6. The full text of the two peer-reviewed papers would likely resolve physics questions but are not available

## Section 2: Challenges in Capturing System Function

The Orbitron presents five major LCOE modeling challenges, ranked by impact:

### Challenge 1: Sub-1 MWe Scale Outside Standard Power Plant Economics — **Critical**

The fixed design point is 5 kWe net electric. This is three orders of magnitude below the scale at which standard utility power plant economics apply. At this scale:
- No grid connection or power purchase agreement is realistic
- Traditional LCOE (levelized cost of electricity per MWh sold to grid) is not the relevant economic metric
- Thermal conversion via steam turbine (as stated on the Orbitron product page) is thermodynamically impractical at 5 kW output
- The economic value proposition is likely backup power, remote/mobile applications, or process heat, not bulk electricity generation

> "packaged as a single cell from 5kW to 100s of kW capacity, grouped together however needed to get to megawatt-scale"
> — avalanche-orbitron-page.md, §Main body

The company envisions modular stacking to MW-scale, but the 5 kWe design point in isolation cannot be costed using conventional LCOE frameworks. The 1costingFE library explicitly cannot model below ~1 MWe due to power balance convergence floors. Any LCOE estimate for this design point would require either extrapolation from a larger (1–10 MWe) model or abandonment of LCOE in favor of $/kW installed cost for distributed generation applications.

### Challenge 2: Electrostatic Confinement Physics Uncertainty — **Critical**

The fundamental physics viability of net-energy electrostatic fusion remains contested. Two critiques dominate the literature:

1. **Space charge limits**: Traditional IEC/Fusor devices cannot achieve fusion-relevant ion densities because positive ion space charge repels incoming ions, creating a density ceiling. Avalanche claims to overcome this via electron co-confinement in a magnetron geometry (E×B drift), which neutralizes space charge:

> "electrostatic approaches to Fusion cannot achieve high ion densities due to space charge effects"
> — avalanche-cwfest2023-blog.md, §Electrostatic controversy section

2. **Coulomb collision losses**: Even if space charge is neutralized, non-Maxwellian electrostatic systems lose energy to ion-ion coulomb scattering faster than fusion occurs. Todd Ryder's 1995 MIT thesis concluded that for non-thermal plasmas, "recirculating power will always substantially exceed the fusion power." For D-T, the coulomb collision rate through 90° scattering is 25× faster than fusion (Labee & Mannheimer critique cited in avalanche-cwfest2023-blog.md).

Avalanche's counter-argument rests on achieving a specific operating regime: 300 keV ions (from 300 kV cathode potential) co-confined with 15 keV electrons at sufficient density that electron-mediated collisions thermalize ion velocities faster than ion-ion scattering removes energy. This regime is predicted by their simulations but not yet experimentally validated at fusion-relevant densities. Current prototypes operate at 200 kV (Marty) and 100 kV (Neo), not the target 300 kV.

> "we can't possibly simulate that at the densities we're talking about. So what we do is we actually run the simulation at much, much higher densities, and then we density scale the results back down"
> — avalanche-cwfest2023-blog.md, §Simulation section

The simulation validation gap is significant: the code cannot run at actual device densities, so results are extrapolated from higher-density runs. This introduces physics uncertainty that propagates directly into Q estimates. Without experimental demonstration of Q>1 at any scale, the LCOE model rests on unvalidated physics assumptions.

### Challenge 3: D-T vs p-B11 Fuel Ambiguity — **High**

The fixed design point specifies D-T fuel. The dossier (dossier.md) classifies the concept as D-T. However, the analyst-patch source (analyst-patch-pb11-fuel-critical.md) asserts that Avalanche's actual commercial target fuel is p-B11, and that modeling D-T introduces costs (tritium breeding, 14.1 MeV neutron shielding, tritium handling plant, T-licensing premium) that "an actual Orbitron at any scale doesn't need." The patch claims the D-T-forced LCOE is ~$890/MWh vs. ~$92/MWh for p-B11, a 10× difference.

Avalanche's public materials are contradictory:
- The Orbitron product page states: "heat generated from neutron bombardment will be converted to electrical energy with a thermal cycle, utilizing turbines" — this describes D-T thermal conversion.
- The same page also states: "p-B11 fuel... practically eliminates internal neutron radiation, resulting in longer life and lower shielding requirements" — this acknowledges p-B11 as a fuel option.
- The FusionWERX neutron source facility uses D-T (and D-D) for neutron production applications.
- The CWFest 2023 blog discusses both D-T and p-B11, with performance estimates given for D-T (1 kW fusion power at Q~1).

The most plausible interpretation is that Avalanche targets D-T for near-term applications (neutron production, materials testing) and p-B11 for longer-term commercial power (where neutron shielding and tritium infrastructure dominate cost). For the fixed 5 kWe D-T design point, this analysis proceeds with D-T assumptions, but the LCOE result carries large uncertainty due to this fuel ambiguity.

### Challenge 4: Lack of Engineering Design for 5 kWe Thermal Conversion — **High**

The Orbitron product page states that D-T energy will be converted via "thermal cycle, utilizing turbines." At 5 kWe net electric output and assuming ~30% thermal efficiency, the thermal input is ~17 kWt. No steam turbine exists at this scale — the smallest industrial steam turbines are ~100 kWe. Possible interpretations:

1. The 5 kWe figure refers to fusion power, not net electric, and the actual device is larger
2. The thermal cycle description is aspirational for scaled-up versions, and the 5 kWe device uses a different conversion method (thermoelectric, direct conversion, or simply exhausts heat)
3. The device is intended for heat applications, not electricity generation

The CWFest 2023 blog gives per-device recirculating power as 1 kW (600 W cathode + 400 W ion guns) for a device producing ~1 kW fusion power, implying Q~1. If this scales linearly, a 5 kW fusion power device would require ~5 kW recirculating power, producing zero net electric output. To achieve 5 kWe net, the device must either operate at Q>>1 (undemonstrated) or the recirculating power must scale sublinearly with fusion power (no evidence provided).

Without a credible 5 kWe thermal cycle design, the power balance and LCOE cannot be modeled with any confidence.

### Challenge 5: No Cost Data for Unique Subsystems — **Moderate**

The Orbitron's distinguishing subsystems have no published cost estimates:

1. **300 kV feed-through and high-voltage generator**: Maintains 300 kV at 6 MV/m gradient with 3 W standby power. This is a proprietary technology achievement with no commercial analogue.
2. **Superconducting magnets**: Required for 0.3 T field (current prototypes use 0.05 T permanent magnets). The magnets are for electron confinement (E×B drift), not ion confinement, so standard tokamak/stellarator magnet cost models do not apply. Avalanche lists these as "long-lead equipment," suggesting high cost or supply-chain constraint.
3. **Ion guns**: 400 W recirculating power per the CWFest blog. No unit cost or lifetime data.
4. **Desktop-scale vacuum system**: Very high vacuum required for a 12 cm diameter device. Standard large-bore vacuum cost models are inapplicable.

The only cost anchor is Avalanche's statement that company-level capital to first commercial operations is "less than a billion dollars" — this is a development program cost, not a per-plant capital cost, and provides no basis for LCOE estimation.

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in order of ascending maturity (least mature first).

### D-T Fusion at Q>1 in Electrostatic Confinement — TRL ~2 (On Paper Only)

**Demonstrated:** Laboratory electrostatic confinement devices (fusors, IEC, Polywell) have produced D-D and D-T fusion reactions at low rates. Avalanche's Marty prototype achieved 200 kV steady-state operation; Neo operates at 100 kV. Neutron production has been demonstrated but not quantified in available sources beyond "mid to high 10^11 neutrons per second" projections for 300 kV operation.

**On paper only:** Q>1 operation. The CWFest 2023 blog estimates Q~1 for a 300 kV, 0.4 T device producing ~1 kW fusion power with ~1 kW recirculating power. This is a simulation-based projection, not experimental data. The simulation cannot run at actual device densities, so the Q~1 estimate is extrapolated.

**Missing at scale:** Experimental validation of coulomb collision regime assumptions. The claim that 15 keV electrons thermalize ion velocities faster than ion-ion scattering removes energy is central to the concept but not validated at fusion-relevant densities. Without this, Q>1 remains speculative.

### 5 kWe Thermal Energy Conversion — TRL ~1 (Conceptual Only)

**Demonstrated:** Nothing. No steam turbine exists at 5 kWe scale. Thermoelectric generators at this scale (RTGs for spacecraft) achieve ~6–8% efficiency, not the ~30% implied for a "thermal cycle with turbines."

**On paper only:** The Orbitron product page mentions thermal conversion but provides no engineering design, efficiency estimate, or technology selection.

**Missing at scale:** Credible energy conversion pathway for 5 kWe output. This is a fundamental gap — without net electric output, LCOE is undefined.

### Tritium Breeding and Handling (if D-T fuel) — TRL ~2 (Concept Only)

**Demonstrated:** Nothing. Avalanche has a tritium-licensed facility (FusionWERX) but this is for neutron source applications, not tritium breeding. At 5 kWe scale, a breeding blanket is impractical — the device geometry (12 cm diameter) leaves no space for a blanket of sufficient thickness to achieve TBR>1.

**On paper only:** No tritium breeding concept has been disclosed. The analyst-patch source argues tritium breeding is not needed because the actual fuel is p-B11, not D-T. If the design point is truly D-T, tritium must be purchased, not bred, introducing a recurring fuel cost and supply constraint.

**Missing at scale:** Any tritium breeding design for a compact electrostatic device. This is likely infeasible at 5 kWe scale.

### Superconducting Magnets for 0.3 T Electron Confinement — TRL ~4 (Component-Level Demonstration)

**Demonstrated:** Superconducting magnets at 0.3 T are commercially available for MRI and particle physics applications. Current Orbitron prototypes use 0.05 T permanent magnets. The upgrade to superconducting is listed as planned but not yet implemented.

**On paper only:** Integration of superconducting magnets into the Orbitron coaxial vacuum geometry. The magnets must produce 0.3 T axial field in a ~12 cm diameter bore while maintaining very high vacuum and not interfering with the high-voltage cathode (300 kV at 6 MV/m gradient). Magnetic field line geometry must support E×B electron confinement without creating loss channels.

**Missing at scale:** Demonstration that the electron confinement regime predicted by simulations (space charge neutralization, coulomb collision suppression) actually occurs when superconducting magnets replace permanent magnets. The field strength increase from 0.05 T to 0.3 T is a 6× jump; nonlinear physics effects may emerge.

### 300 kV High-Voltage System — TRL ~5 (Integrated Prototype Demonstrated)

**Demonstrated:** Avalanche achieved 300 kV steady-state operation in a compact geometry (2.5 inch gap, 6 MV/m gradient) with 3 W standby power. This is a real accomplishment — most high-voltage systems of this class are either pulsed or require much larger gaps. The 300 kV press release (avalanche-300kv-press-release.md) presents this as a de-risked subsystem.

**On paper only:** Long-term reliability and lifetime. The 300 kV achievement was demonstrated but no data on hours of operation, failure modes, or component degradation is public. High-voltage systems in other industries (electron microscopes, X-ray tubes, particle accelerators) exhibit insulator degradation, vacuum breakdown, and cathode sputtering over time. The Orbitron's cathode is directly exposed to fusion plasma (or at least energetic ions), which will erode it.

**Missing at scale:** Production-scale manufacturing cost. The 300 kV feed-through is proprietary and has no commercial analogue, so no unit cost estimate is possible. Avalanche states the design "lends itself to high-speed production line manufacturing," but this claim is unsubstantiated.

### Desktop-Scale Vacuum System — TRL ~6 (Fully Demonstrated)

**Demonstrated:** Very high vacuum systems at 12 cm diameter scale are standard in laboratory and industrial applications (electron microscopes, deposition chambers, surface analysis tools). Avalanche's prototypes operate in this regime.

**On paper only:** Nothing significant. Vacuum technology at this scale is mature.

**Missing at scale:** Integration with 300 kV high-voltage, superconducting magnets, and fusion neutron environment. The vacuum vessel must maintain vacuum while supporting electrical feedthroughs, magnetic field penetration, and (if D-T) neutron shielding. This is an integration challenge but not a fundamental technology gap.

### Ion Injection and Heating System — TRL ~5 (Integrated Prototype Demonstrated)

**Demonstrated:** Ion guns delivering 400 W wallplug for ionization, acceleration, and beam focusing are operational in current prototypes. The CWFest 2023 blog describes these as functioning subsystems.

**On paper only:** Efficiency optimization and long-term reliability. The 400 W recirculating power for 1 kW fusion power (Q~1) implies 40% of gross fusion power is consumed by ion injection. This is a high recirculating fraction, comparable to D-T mirrors with end losses. Cost and lifetime of ion gun components (filaments, grids, focusing electrodes) at high duty cycle are unknown.

**Missing at scale:** Nothing critical. Ion sources are mature technology.

### Balance of Plant (Power Supplies, Vacuum Pumps, Cooling) — TRL ~7-8 (Commercial Technology)

**Demonstrated:** High-voltage power supplies, vacuum pumps, and cooling systems for 5 kW-scale devices are off-the-shelf industrial products. No fusion-specific innovation required.

**On paper only:** System integration for a modular power product. Avalanche envisions packaging the Orbitron as a "single cell" that can be "grouped together" to reach MW-scale. This requires standardized interfaces, control systems, and power management — routine engineering but not yet demonstrated.

**Missing at scale:** Nothing.

## Section 4: Key Materials and Supply Chain Considerations

### Superconducting Magnets — **Critical for Concept Performance**

The upgrade from 0.05 T permanent magnets (current prototypes) to 0.3 T superconducting magnets is necessary to achieve the electron density required for space charge neutralization. Superconducting wire at 0.3 T is commercially available (NbTi or MgB2), but Avalanche lists these as "long-lead equipment" in the $29M raise press release, suggesting supply-chain constraints or high cost. For a 12 cm bore diameter coil at 0.3 T, the required conductor quantity is modest (likely <100 kg), so the supply chain bottleneck is more likely specialized fabrication and cryogenic integration than raw material availability.

**Current supply:** NbTi superconducting wire production is ~1000 tons/year globally, adequate for demand. MgB2 is less mature but scalable.

**Cost trajectory:** NbTi wire costs ~$50-100/kg in bulk. For a 12 cm coil, material cost is $5k-10k, but fabrication and cryostat integration could add 10-100× multiplier. No vendor quote or cost estimate is available.

### High-Voltage Insulators and Feed-Throughs — **Critical for Concept Performance**

The 300 kV, 6 MV/m gradient achievement depends on proprietary vacuum insulator design. Standard insulators at this voltage use >10 cm gap distances; Avalanche's 2.5 inch (6.35 cm) gap is a significant improvement. The insulator material (likely alumina ceramic or similar) must withstand vacuum, high field gradients, and (if D-T) neutron and X-ray bombardment without breakdown or tracking.

**Current supply:** High-voltage ceramics are produced by specialty manufacturers (CoorsTek, Kyocera, CeramTec) for power transmission, particle accelerators, and industrial X-ray systems. Lead times are 6-12 months for custom geometries.

**Cost trajectory:** Custom vacuum insulators at 300 kV scale cost $10k-50k per unit in low-volume production. At "high-speed production line" scale (Avalanche's goal), costs could drop 10×, but no vendor has produced these at volume, so the learning curve is unknown.

### Tritium (if D-T fuel is confirmed) — **Moderate Supply Constraint**

Global civilian tritium inventory is ~25 kg, produced as byproduct from CANDU reactors (which are retiring). Market price is ~$30,000/g. A 5 kWe D-T device requires negligible tritium inventory (<1 g) for startup, but must either breed tritium (impractical at 5 kW scale) or purchase it as consumable fuel. At 5 kWe net and assuming 1% D-T burnup per pass, annual tritium consumption is ~0.1 g/year, costing ~$3,000/year. This is economically insignificant but depends on tritium remaining available — if CANDU retirements proceed and fusion plants consume the supply, small D-T devices like this would be priced out.

**Supply risk:** High if D-T fuel is confirmed. Low if p-B11 (no tritium needed).

### Vacuum Vessel and Structural Materials — **Low Constraint**

For a 12 cm diameter device, stainless steel or aluminum vacuum chambers are standard catalog items. Neutron activation (if D-T) at 5 kW fusion power is negligible — the device produces ~10^12 n/s, comparable to a small neutron generator used in oil well logging. Shielding requirements are minimal (the CWFest blog mentions a "concrete castle" for X-ray and neutron shielding, but this is for laboratory safety, not structural protection).

**Supply risk:** None.

## Section 5: Design Point Parameters

The fixed design point is a 5 kWe net electric output D-T Orbitron. Quantitative parameters below are extracted from the CWFest 2023 blog, which describes a ~1 kW fusion power prototype, and extrapolated to 5 kWe net assuming the company's stated "5 kW to 100s of kW" modular packaging applies. **Critical caveat**: The CWFest blog parameters are for a device producing 1 kW fusion power at Q~1, not 5 kWe net electric. The scaling assumptions are speculative.

| Parameter | Value | Source | Confidence | Note |
|---|---|---|---|---|
| Net electric power | 5.0 MWe | fixed by design-point selection | high | spec key: `P_native` — but see Challenge 1 (below LCOE scale) |
| Plasma radius | 0.06 m (6 cm) | avalanche-cwfest2023-blog.md §Fusion rate scaling section | high | spec key: `plasma_t`. Device is 12 cm diameter per blog. |
| Cathode voltage | 300 kV | avalanche-300kv-press-release.md §Main body | high | Not a spec key but critical for fusion rate. Achieved in prototype. |
| Magnetic field (on-axis) | 0.3 T | avalanche-cwfest2023-blog.md §Fusion rate scaling section | medium | spec key: `B`. Target for superconducting upgrade; current prototypes at 0.05 T permanent magnets. |
| Field gradient | 6.0 MV/m | avalanche-fusionwerx-grant.md §Voltage Breakthrough section | high | Not a spec key but characterizes high-voltage achievement. |
| Fusion power (scaled estimate) | [inferred: ~25 kWt] | [extrapolated from CWFest 1 kW @ Q~1, scaled to 5 kWe net assuming eta_th~0.2] | low | spec key: library back-solves from `P_native` + recirculating fraction. CWFest gives 1 kW fusion at 1 kW recirc (Q~1). For 5 kWe net at Q~1 and 20% gross thermal efficiency, need ~25 kW fusion. |
| Neutron rate (scaled estimate) | [inferred: ~10^12 n/s] | [extrapolated from CWFest "mid to high 10^11 n/s" for 1 kW fusion, scaled linearly] | low | Not a spec key. Informational only. |
| Auxiliary heating wallplug | [estimated: ~5-10 kW] | [extrapolated from CWFest 1 kW recirc (600 W cathode + 400 W ion guns) scaled to 5-10 kW for 5 kWe net] | low | spec key: `p_input`. CWFest gives 600 W cathode + 400 W ion guns = 1 kW for ~1 kW fusion. If Q~1 holds, ~5-10 kW recirculating for 5 kWe net (but this produces zero net electric unless Q>>1). |
| Q_plasma (estimated) | [inferred: ~2-5] | [must be >1 to produce net power; CWFest blog targets Q~1 for 1 kW device] | very low | Not a spec key. For 5 kWe net with ~5-10 kW recirculating, Q must be >2-5 depending on thermal efficiency assumptions. No experimental data at this Q. |
| Thermal conversion efficiency | [assumed: ~20-30%] | [standard for small-scale thermal systems; no source data] | low | spec key: `eta_th`. No steam turbine exists at 5 kWe scale. Thermoelectric would be ~6-8%. The Orbitron page says "thermal cycle, utilizing turbines" but this is physically implausible at 5 kW. |
| Device chamber length | [assumed: ~0.2-0.5 m] | [estimated from "desktop-scale" and 12 cm diameter; aspect ratio ~2-4 typical for coaxial devices] | low | spec key: `chamber_length`. No explicit length stated. CWFest blog describes "small enough to sit on a desk." |
| Blanket thickness | N/A | No breeding blanket at 5 kW scale | high | At 12 cm plasma diameter, no space for a breeding blanket of sufficient thickness to achieve TBR>1. Tritium must be supplied externally if D-T fuel. |

**Critical gap**: The 1 kW fusion power device described in the CWFest blog operates at Q~1, meaning it consumes as much power as it produces. To achieve 5 kWe **net** electric output, the device must either:
1. Operate at Q>>1 (factor of 5-10 higher than described), OR
2. Have much lower recirculating power than the linear scaling from the CWFest data implies, OR
3. Not use thermal conversion (use direct conversion instead, but the Orbitron page says thermal cycle for D-T).

None of these is substantiated. The 5 kWe design point is not credibly costed without resolving this gap.

### Inference Chain for `p_input`

The CWFest 2023 blog states that for a 300 kV, 0.4 T device producing ~1 kW fusion power:
- Cathode consumes 600 W
- Ion guns consume 400 W
- Total recirculating power: 1 kW

This is Q_device ~1 (fusion power equals recirculating power). If this scales linearly, a device producing 5 kW fusion power would require 5 kW recirculating power, producing zero net electric output at any thermal efficiency.

For the device to produce 5 kWe net electric, we must assume one of:
- **Option A**: Q scales favorably with size, so a larger device operates at Q_device ~5-10 instead of Q~1.
- **Option B**: Recirculating power does not scale linearly — the cathode and ion gun power requirements are fixed or scale sublinearly with fusion power.
- **Option C**: The device uses direct energy conversion (charged particle deceleration) instead of thermal conversion, improving net efficiency.

No evidence for any of these assumptions exists in the sources. The analyst-patch source (analyst-patch-pb11-fuel-critical.md) gives `p_input = 0.040 MW` (40 kW) for an 80 kWe device, implying Q_device ~2-3 at 80 kWe scale and ~30% efficiency. Scaling this to 5 kWe: 5 kWe / 80 kWe = 6.25% of the power, so p_input ~2.5 kW. But this assumes the same Q and efficiency at 5 kWe, which is uncertain.

**Adopted value for modeling**: `p_input = 5 MW` (assumes Q_device ~5-10 and eta_th ~20-30%, allowing 5 kWe net). Confidence: **very low**. This parameter dominates LCOE via the recirculating fraction and is essentially a guess.

## Section 5b: Override Candidates

**Critical blocker**: The 1costingFE library cannot model below ~1 MWe due to power balance convergence floors. Any `P_native < 1 MWe` is rejected with `rec_frac > 1` errors regardless of parameter choices. Per the analyst-patch source, the library must be run at `P_native = 1.0 MWe` as a workaround, even though the actual design point is 5 kWe (0.005 MWe). This makes override discovery impossible — the model does not represent the actual device scale, so cost accounts cannot be meaningfully overridden for a 5 kWe machine.

**Fuel ambiguity**: The analyst-patch source asserts the correct fuel is p-B11, not D-T, and that D-T assumptions introduce $700M+ in inapplicable costs (tritium breeding, 14 MeV shielding, T-handling). If p-B11 is confirmed, the override list would be:
- CAS27 (Special Materials — tritium inventory): $0 (no tritium needed)
- C220101 (Blanket): $0 or minimal (no breeding blanket; may still need neutron shield for <1% side-reaction neutrons)
- Decommissioning provision: reduced (low activation)
- Licensing cost: reduced (no tritium handling)
- CAS70 (O&M): reduced (no tritium processing)

But the fixed design point specifies D-T fuel, so these overrides cannot be applied without contradicting the design-point specification.

Given these blockers, **no overrides are proposed**. The concept cannot be meaningfully costed at the specified scale and fuel with current library capabilities.

```yaml
overrides: []
```

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q_plasma and confinement time at fusion-relevant densities for D-T operation | S5 | truly-unknown | blocking | Full text of AIP Advances (2024) and Physics of Plasmas (2025) papers; peer-reviewed experimental validation of coulomb collision regime assumptions |
| 2 | Thermal energy conversion pathway for 5 kWe net electric output | S2-Ch4, S3, S5 | truly-unknown | blocking | Engineering design study for thermal or direct energy conversion at 5-10 kW scale |
| 3 | Recirculating power scaling from 1 kW (CWFest prototype) to 5 kWe commercial module | S5 | truly-unknown | blocking | Company-published performance data for scaled devices, or physics-based scaling model |
| 4 | Capital cost breakdown by subsystem (magnets, vacuum, high-voltage, BOP) | S1, S2-Ch5 | proprietary | blocking | Vendor quotes for superconducting magnets, high-voltage feed-throughs, ion guns; company cost model |
| 5 | Tritium breeding approach (or confirmation of purchase-based fuel supply if D-T) | S2-Ch3, S3, S4 | proprietary | blocking | Company statement on tritium supply strategy; if breeding, blanket design; if purchase, supply contract terms |
| 6 | Confirmed fuel choice (D-T vs p-B11) for commercial power applications | S2-Ch3, S5 | proprietary | blocking | Company roadmap document or technical presentation clarifying fuel strategy |
| 7 | Superconducting magnet cost and lead time for 0.3 T, 12 cm bore | S4 | not-yet-sourced | important | Vendor quote from Cryomagnetics, Oxford Instruments, or similar for custom coil; timeline for delivery |
| 8 | High-voltage feed-through unit cost and manufacturing scalability | S2-Ch5, S4 | proprietary | important | Company manufacturing cost model; comparison to commercial high-voltage insulators at lower gradient |
| 9 | LCOE or $/kW installed cost estimate from company | S1, S2-Ch1 | proprietary | important | Avalanche investor deck, technical white paper, or public presentation with economic projections |
| 10 | Simulation code validation against experimental data at 300 kV, 0.3 T | S2-Ch2, S3 | truly-unknown | important | Peer-reviewed comparison of predicted vs measured neutron rates, density, temperature; parameter sensitivity analysis |
| 11 | Long-term reliability data for 300 kV steady-state operation | S3 | truly-unknown | nice-to-have | Extended run-time data (100s-1000s hours) from Marty or Neo prototypes; failure mode analysis |
| 12 | FusionWERX facility cost and neutron production economics | S1, S4 | proprietary | nice-to-have | Detailed cost breakdown for FusionWERX; revenue model for neutron source applications to contextualize near-term business case |

**Gap type definitions:**
- **truly-unknown**: Information does not exist (physics not validated, technology not demonstrated)
- **proprietary**: Information exists within company but not published
- **not-yet-sourced**: Information likely exists in open literature or vendor catalogs but not yet obtained

**Criticality definitions:**
- **blocking**: Cannot produce credible LCOE estimate without this data
- **important**: Estimate possible but with large uncertainty without this data
- **nice-to-have**: Would reduce uncertainty but not critical for order-of-magnitude LCOE

## Section 7: Family-Delta vs Comparables

No comparable concept in the corpus for this design point.

## Section 8: Sources

### Primary Company Sources (in order of technical depth)

1. **avalanche-cwfest2023-blog.md** — CWFest 2023 presentation blog post (2023)
   - Most detailed technical source available. Describes device physics, confinement concept (E×B electron co-confinement to overcome space charge), performance targets (300 kV, 0.4 T, ~1 kW fusion at Q~1), simulation methodology, and experimental status (Marty at 200 kV, Neo at 100 kV). Discusses space charge and coulomb collision critiques and Avalanche's proposed solutions.
   - Found: knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/

2. **avalanche-orbitron-page.md** — Orbitron product page (date unknown, likely 2023-2024)
   - Marketing-level description of Orbitron concept. Key claims: "1-100 kWe compact fusion machine," "small enough to sit on a desk," "No Giant Magnets or Lasers," modular packaging "from 5kW to 100s of kW," thermal energy conversion "utilizing turbines" for D-T, p-B11 capability mentioned. Lists applications (space, maritime, micro-grids).
   - Found: knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/

3. **avalanche-300kv-press-release.md** — 300 kV voltage achievement press release (2026)
   - Announces achievement of 300 kV steady-state operation at 4.7-6 MV/m gradient with 3 W standby power. Describes this as "steady-state; significantly more challenging than pulsed" and "the ideal energy for fusing Deuterium and Tritium in our compact machine."
   - Found: knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/

4. **avalanche-29m-raise-2026.md** — $29M Series A final close announcement (2026)
   - Announces $29M raise, total Series A of $40M. Plans to "order long-lead equipment (including superconducting magnets)" and conduct "Deuterium-Tritium Q>1 test program." Mentions FusionWERX facility for "licensing for commercial-scale fusion operations." Applications listed: defense, space, commercial (remote power, propulsion).
   - Found: knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/

5. **avalanche-fusionwerx-grant.md** — FusionWERX $10M Washington State grant announcement (date unknown, likely 2025-2026)
   - Describes FusionWERX facility in Richland, WA (former Kurion detritiation site). Tritium-licensed, targeting "continuous high-flux fusion neutrons" for "medical and power radioisotopes" and "radiation-tolerant alloys" testing. Grant funds "first-generation neutron-handling equipment" and ~12 jobs. Expected full operation 2027.
   - Found: knowledge/concept_research/13-electrostatic-hybrid/iter-01/sources/

### Analyst-Generated Patch Source

6. **analyst-patch-pb11-fuel-critical.md** — Analyst patch asserting p-B11 fuel for Orbitron (2026, iteration 03)
   - **Critical discrepancy source.** Asserts Avalanche's commercial target fuel is p-B11, not D-T, and that modeling D-T introduces ~$700M in inapplicable costs (tritium breeding, 14 MeV shielding, T-handling), producing LCOE ~$890/MWh (D-T) vs ~$92/MWh (p-B11), a 10× error. Provides model parameters for 80 kWe p-B11 device: plasma radius 0.06 m, B=0.3 T, p_input=0.040 MW, Q_sci~7. Also documents 1costingFE convergence floor at ~1 MWe as blocker for modeling sub-1 MWe devices.
   - Found: knowledge/concept_research/13-electrostatic-hybrid/iter-03/sources/

### Peer-Reviewed Papers (abstracts only)

7. **AIP Advances 14(8), 085025 (August 2024)** — "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons"
   - Abstract confirms crossed-field E×B confinement concept. Full text not available in dossier.

8. **Physics of Plasmas 32(9), 092105 (September 2025)** — "Mode-enhanced ion loading in a 100 kV orbitron"
   - Abstract describes ion loading dynamics at 100 kV. Full text not available in dossier.
