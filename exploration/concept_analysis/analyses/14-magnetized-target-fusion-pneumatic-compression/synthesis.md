---
ID: 14-magnetized-target-fusion-pneumatic-compression
Concept: MTF Pneumatic Compression (General Fusion)
Company: General Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

## Executive Summary

- **Most important risk:** The 86,400× gap between demonstrated repetition rate (LM26: 1 pulse/day) and commercial requirement (1 pulse/second) compounds multiple unproven subsystems — vacuum re-establishment, liquid metal vortex reformation, piston recharge — each of which must complete in ~1 second. Failure in any one blocks the entire concept.
- **Most important advantage:** Zero per-shot consumables. Unlike all other pulsed fusion concepts (laser ICF, MagLIF, Z-pinch), the liquid metal liner is recycled, eliminating the target factory (C220108 = $0) and enabling true ~1 Hz pulsed operation without manufactured targets.
- **LCOE ballpark:** 47 $/MWh (1 GWe NOAK projection). Native-scale (150 MWe, single module) LCOE is 92 $/MWh. This is competitive with fission baseload if the engineering challenges are resolved.
- **Confidence verdict: Low.** Fusion power, Q, and recirculating power are all unpublished. The library's engineering gain default (q_eng = 3.0) drives the power balance, not company data. LM26 physics (electromagnetic compression of solid lithium) differs fundamentally from the commercial concept (pneumatic compression of liquid metal). The piston system cost override (15% of library default) is directionally grounded in General Fusion's claims but has no published dollar figure to anchor it.

## What Matters Most for LCOE

Ranked by LCOE sensitivity:

### 1. Engineering gain (q_eng) — library default = 3.0
- **Source:** Library default. General Fusion has not published fusion power (MWth), Q, or recirculating power for the commercial plant.
- **Sensitivity magnitude:** If q_eng drops from 3.0 to 2.0, net electric power falls by ~33% and LCOE rises proportionally. If q_eng < 1.5, the plant cannot sustain 150 MWe output at the stated 1 Hz repetition rate.
- **What would flip the conclusion:** q_eng < 2.0 would push LCOE above 100 $/MWh at NOAK. q_eng > 4.0 would bring LCOE below 40 $/MWh — potentially cost-competitive with natural gas peaking. The Krotez et al. 2023 SOFE paper likely contains Q or fusion power data but is not in the dossier.

### 2. Piston system capital cost (C220104) — override = 15% of library default ($7.2M at native scale)
- **Source:** Derived from General Fusion's claim that pneumatic pistons are "low-cost" relative to lasers and superconducting magnets. No published dollar figure.
- **Sensitivity magnitude:** If the piston system costs 50% of the library default (instead of 15%), C220104 rises from $7.2M to $24M at native scale, adding ~$15M to overnight capital and ~$7/MWh to LCOE. If pistons cost 100% of the library default, LCOE rises by ~$12/MWh.
- **What would flip the conclusion:** Piston system cost > 30% of library default would push native-scale LCOE above 100 $/MWh. The "major automaker" partnership suggests commodity-scale manufacturing; if pistons can be mass-produced at automotive precision, 15% may be conservative (i.e., actual cost could be lower).

### 3. Vacuum re-establishment and liquid metal vortex reformation — not explicitly modeled
- **Source:** Not quantified in available sources. The commercial plant requires vacuum re-establishment and vortex reformation within ~1 second. The Wikipedia article flags this as "a significant engineering obstacle that will need to be solved."
- **Sensitivity magnitude:** If vacuum re-establishment limits repetition rate to 0.5 Hz (instead of 1 Hz), thermal power is halved, electric output falls to ~75 MWe per module, and LCOE doubles. If the vortex spray problem (noted in 2013 experiments) persists, the concept is disqualified.
- **What would flip the conclusion:** Demonstrated 1 Hz operation with stable liquid metal reformation at GJ-scale blast loading would retire this risk. Failure to achieve >0.5 Hz at commercial scale would render the economics uncompetitive.

### 4. Liquid metal blanket material (LLE vs. Li) — undecided
- **Source:** FST 2025 paper evaluates both options without selecting one. LLE has lower tritium retention (favoring extraction) but risks plasma poisoning by high-Z lead during compression. Pure lithium has higher TBR (1.25–1.80 vs. 1.40 for LLE) but requires immature extraction technology.
- **Sensitivity magnitude:** If LLE plasma contamination is disqualifying, the concept must use pure lithium, which increases tritium startup inventory by 2.4× (0.747 kg vs. 0.317 kg) and requires 314 centrifugal contactors drawing 1.2 MW parasitic power. If pure lithium extraction technology proves infeasible, the concept is blocked. The LCOE impact is modest (~$2–5/MWh from parasitic power) but the risk is binary: either blanket material works, or the concept fails.
- **What would flip the conclusion:** LM26 compression experiments with both LLE and pure lithium would resolve the plasma contamination question. If lead contamination is minimal (<1% impurity at peak compression), LLE becomes the preferred option. If lead contamination is >10%, pure lithium is mandatory.

### 5. Thermal efficiency (η_th) — library default = 33% (assumed)
- **Source:** No published steam cycle parameters. Standard steam Rankine without reheat is ~30–35%. The Hatch/Kyoto Fusioneering partnerships may yield higher efficiency with advanced steam conditions.
- **Sensitivity magnitude:** If η_th = 38% (optimistic steam cycle with reheat), net electric power rises by ~15% and LCOE falls by ~$7/MWh. If η_th = 28% (pessimistic, limited by pulsed thermal buffering), LCOE rises by ~$9/MWh.
- **What would flip the conclusion:** η_th < 30% would push native-scale LCOE above 100 $/MWh. η_th > 40% would require supercritical CO2 or other advanced cycles, which are incompatible with the pulsed thermal source unless thermal buffering (molten salt or steam accumulator) is added at additional capital cost.

## Risk Verdicts

### 1. Vacuum re-establishment at ~1 Hz between pulses
- **Verdict:** Unlikely resolvable at 1 Hz, but 0.3–0.5 Hz may suffice.
- **Rationale:** The gap between LM26 (1 pulse/day) and commercial (1 pulse/second) is 86,400×. High-vacuum systems (10⁻⁵ Torr) typically require seconds to minutes to pump down after a GJ-scale blast that vaporizes liquid metal surface layers. Turbomolecular pumps at massive scale or cryogenic pumping could achieve <1 second pumpdown, but this is undemonstrated.
- **What would retire this risk:** Demonstrated vacuum re-establishment to <10⁻⁴ Torr within 3 seconds (enabling 0.3 Hz operation) on a subscale (~2 m diameter) system with liquid metal vaporization loads. 0.3 Hz would halve electric output but remain economically viable if capital cost reductions (pistons, blanket) hold.

### 2. Liquid metal vortex stability under repetitive GJ-scale fusion pulses
- **Verdict:** Genuinely uncertain.
- **Rationale:** Scaled water experiments (1:10 scale, 1,000+ shots) demonstrated controlled collapse. Mangione et al. 2024 (FED) showed shape-controlled compression of rotating liquid liners with pneumatic pistons. However, the 2013 proof-of-concept noted "the wall of the liquid metal vortex turned to a spray soon after the arrival of the pressure wave." Whether lithium or LLE can reform a stable vortex under neutron activation, tritium absorption, and thermal cycling is unknown. If the vortex degrades into spray or foam, vacuum cannot be re-established and the concept fails.
- **What would retire this risk:** LM26 integrated compression tests with fusion-relevant energy deposition (MJ-scale neutron + alpha heating) and vortex reformation within 5 seconds. If the vortex reforms cleanly at this timescale, 0.2 Hz operation becomes plausible and the economics remain viable.

### 3. Piston seal technology and wear under repetitive high-speed impacts
- **Verdict:** Likely resolvable.
- **Rationale:** General Fusion ran a $20,000 crowdsourced innovation challenge specifically for robust seal technology, indicating this was a recognized bottleneck. The "major automaker" partnership suggests automotive-scale precision and wear-resistant materials (ceramic composites, elastomeric seals) can be adapted. Automotive pistons routinely survive millions of cycles at comparable speeds (50 m/s piston velocity). The unique challenge is isolating pistons from hot (300–500°C) liquid metal under repetitive impacts.
- **What would retire this risk:** Demonstrated piston seal survival for >10,000 cycles at commercial impact energy (100 kg hammer at 50 m/s) with liquid metal contact. If seals require replacement every 1,000 cycles (i.e., daily at 1 Hz), O&M costs rise by ~$5–10M/year (100 pistons × $50k/seal replacement), adding ~$3–5/MWh to LCOE — non-trivial but not disqualifying.

### 4. LM26-to-commercial extrapolation (electromagnetic compression of solid lithium → pneumatic compression of liquid metal)
- **Verdict:** Unlikely resolvable via LM26 alone; requires intermediate-scale pneumatic compression demonstration.
- **Rationale:** LM26 compression mechanism, liner state, and driver technology all differ from the commercial concept. Electromagnetic theta-pinch compression of a solid lithium liner has fundamentally different implosion dynamics (MHD instabilities, skin-depth effects) than pneumatic piston compression of a liquid metal liner (hydrodynamic instabilities, vortex shear). LM26 can demonstrate that a magnetized compact toroid survives compression and reaches 10 keV, but it cannot validate the pneumatic-on-liquid-metal compression physics that underpins the commercial plant.
- **What would retire this risk:** A pneumatic compression test at 50–70% commercial scale (~2 m cavity diameter) with liquid metal and fusion-relevant compression ratios (100–200×). This would validate piston synchronization, vortex stability, and achievable compression symmetry. If LM26 reaches 10 keV and the pneumatic test achieves >50× compression with <10% asymmetry, the commercial plant becomes credible.

### 5. Tritium extraction at 2 m³/s lithium throughput
- **Verdict:** Likely resolvable, but TRL is low for pure lithium.
- **Rationale:** For LLE blanket, tritium extraction is mature (palladium diffusers, CECE, gas-liquid contactors). For pure lithium, the FST 2025 paper notes that Direct LiT Electrolysis "is in its infancy and will require more research to determine to what level of throughput it can handle." The alternative (Maroni centrifugal contactors) requires 314 units drawing 1.2 MW parasitic power — a ~1% hit to net electric output, adding ~$0.5/MWh to LCOE. This is non-trivial but not a showstopper.
- **What would retire this risk:** Lab-scale demonstration of Direct LiT Electrolysis at >1 kg/day tritium extraction rate with <0.1% lithium loss. If successful, the centrifugal contactor array can be avoided. If Direct LiT proves infeasible, the Maroni process is the fallback at modest parasitic power cost.

## Structural Advantages and Disadvantages

### vs. D-T tokamak baseline (ITER-scale, HTS magnets, solid blanket):

**Eliminated costs:**
- **C220103 (confinement magnets): $0.** No HTS tape, no REBCO superconducting magnets, no cryogenic refrigeration, no quench protection. The tokamak baseline has C220103 ~ $50–100M at 150 MWe scale; GF MTF eliminates this entirely. This is a structural ~$30–50/kWe capital savings (~7–10% of overnight capital at native scale).
- **C220108 (target factory): $0.** Tokamaks don't have target factories either, but all other pulsed concepts (laser ICF, MagLIF, Z-pinch) do. Relative to MagLIF (which has C220108 ~ $100–200M for liner fabrication at GW-scale), GF MTF saves ~$10–15/MWh in consumables OPEX.
- **C220101 (blanket): 40% of library default.** The liquid metal blanket eliminates solid blanket module fabrication (tungsten tiles, beryllium first wall, HCPB structured breeder). Tokamak baseline has C220101 ~ $50M at 150 MWe scale; GF MTF reduces this to ~$20M. Savings: ~$20/kWe.

**Added costs:**
- **C220104 (piston driver): 15% of library default = $7.2M at native scale.** This is lower than the tokamak heating systems (NBI + ECRH ~ $30–50M at 150 MWe scale), but the uncertainty is high. If pistons cost 50% of library default, the advantage evaporates.
- **Vacuum re-establishment and liquid metal loop maintenance (CAS70 O&M):** No published breakdown, but piston seal replacement, liquid metal pumping (2 m³/s at hundreds of kW), and vortex control systems are unique OPEX items. If O&M is 50% higher than tokamak baseline, this adds ~$5–8/MWh. The library default for CAS70 at MIF concepts may underestimate this.

**Net effect:** GF MTF saves ~$50–70/kWe in overnight capital (magnets + blanket) and ~$10/MWh in consumables OPEX, but faces uncertain piston capital cost and likely higher O&M. If all assumptions hold, the concept is 20–30% cheaper than a tokamak at the same net electric output. If the piston system costs 2× the override assumption and O&M is 2× library default, the advantage shrinks to <10%.

### vs. laser ICF (NIF-scale indirect drive):

**Structural advantage:** Target factory elimination. NIF-style laser ICF requires precision-fabricated hohlraums and cryogenic D-T capsules at ~10–20 Hz for power production. Target fabrication cost is $10–30 per shot (optimistic NOAK), implying $100M–$600M/year consumables OPEX for a 1 GWe plant. GF MTF has zero per-shot consumables. This is a ~$10–20/MWh OPEX advantage.

**Structural disadvantage:** Liquid metal vortex management is harder than simply injecting a fresh target. Laser ICF starts each shot with a clean chamber; GF MTF must reform the vortex, pump out vaporized lithium, and re-establish vacuum — all while maintaining dimensional tolerance for piston compression symmetry.

## Cross-Concept Positioning

GF MTF occupies a unique position in the fusion landscape:

- **Within MIF:** The only concept with recycled compression medium. MagLIF (Sandia/Pacific Fusion), NearStar (railgun MIF), and FuZE (sheared-flow stabilized Z-pinch) all destroy their liner/target per shot. GF MTF's liquid metal recycling is a genuine innovation — if it works.

- **Within pulsed fusion:** The only pulsed concept without manufactured consumables. Laser ICF (hohlraums/capsules), MagLIF (liners + return transmission lines), and Z-pinch (wire arrays) all have per-shot hardware costs. GF MTF's claim of "a pulsed system without manufactured consumables" is structurally true but operationally unproven at rate.

- **Within liquid-metal-first-wall concepts:** Similar to Solase (laser ICF with liquid Flibe vortex) and some tokamak liquid metal divertor proposals, but GF MTF is the only concept where the liquid metal is also the compression medium. This triple function (blanket/shield/compressor) is architecturally elegant but creates the vacuum/vortex/reformation trilemma.

**Closest comparable:** Helion (pulsed FRC compression), which also uses pulsed operation without per-shot consumables and mechanical/magnetic compression. Helion targets D-He3 fuel (avoiding tritium) and direct inductive energy recovery (avoiding steam cycle losses). GF MTF uses D-T fuel (easier physics, harder fuel cycle) and conventional thermal conversion. Helion's approach is higher risk (D-He3 requires 5× higher temperature) but higher reward (no tritium breeding, no neutron activation). GF MTF is lower risk (D-T is proven fuel) but accepts the tritium fuel cycle and neutron damage.

## Modeling Confidence

**Rating: Low**

### Data-anchored parameters (5 of 12):
1. Net electric output (150 MWe per module) — high confidence, from Krotez 2023 SOFE via Wikipedia + FST 2025
2. Repetition rate (1 Hz) — high confidence, stated in multiple sources
3. Chamber radius and blanket thickness — high confidence, from FST 2025
4. Tritium fuel cycle parameters (burn fraction, TBR, startup inventory) — high confidence, peer-reviewed FST 2025 paper
5. Demonstrated plasma parameters (pre-compression T_e, n_e, τ_E) — high confidence, from company press releases and IAEA abstract

### Speculative parameters (7 of 12):
1. **Fusion power (MWth) — library back-solves from net electric + q_eng default.** Not published anywhere in the dossier. The Krotez 2023 SOFE paper likely contains this but is unavailable.
2. **Energy gain Q — unknown.** Library default q_eng = 3.0 is assumed, not derived from company data.
3. **Recirculating power (p_input) — unknown.** Piston drive energy, plasma injector power, and liquid metal pumping are all unpublished. Library derives from q_eng.
4. **Thermal efficiency (η_th) — library default ~33%.** No published steam cycle parameters. Hatch/Kyoto Fusioneering partnerships suggest advanced BOP but no specifics.
5. **Piston system capital cost (C220104) — 15% of library default.** Directionally grounded in GF's "low-cost" claim but no dollar figure published. Could be 10–50% of library default.
6. **Blanket material (LLE vs. Li) — undecided.** FST 2025 evaluates both without selecting one. TBR, tritium inventory, and extraction system all depend on this choice.
7. **O&M cost breakdown — library default.** No published maintenance schedule. Piston seal replacement, liquid metal loop upkeep, and tritium processing are concept-specific OPEX items with no analogues in other fusion concepts.

### Dominant source of LCOE uncertainty:

**q_eng (engineering gain).** If q_eng = 2.0 instead of 3.0, LCOE rises by ~30%. If q_eng = 4.0, LCOE falls by ~20%. The library's q_eng default is the single largest assumption driving the LCOE projection. Without published fusion power, Q, or recirculating power, the model output should be interpreted as "what the economics would be IF the library's q_eng assumption is correct" — not as a validated estimate of GF MTF's actual LCOE.

Second-order uncertainty: piston system cost. If pistons cost 50% of library default (instead of 15%), LCOE rises by ~15%. If pistons cost 5% (i.e., truly commodity-scale manufacturing), LCOE falls by ~10%.

Tertiary uncertainty: O&M. Piston wear, seal replacement, liquid metal loop maintenance, and tritium processing are all concept-specific OPEX items. If actual O&M is 2× library default, LCOE rises by ~$8/MWh.

## What Would Change My Mind

### 1. Published fusion power, Q, and recirculating power from the Krotez 2023 SOFE paper or a follow-on publication
**Direction:** Either direction.

If Q > 5 and recirculating power is <30% of gross electric (i.e., q_eng > 4), the LCOE projection of 47 $/MWh is conservative and actual cost could be 35–40 $/MWh — competitive with fission baseload. If Q < 3 and recirculating power is >50% of gross electric (i.e., q_eng < 2), LCOE rises above 70 $/MWh and the concept becomes uncompetitive even at NOAK.

**Likelihood:** Medium. General Fusion has strong incentives to publish Q if it's favorable (investor signaling, talent recruitment). The absence of Q in public materials suggests either (a) it's proprietary and being held for competitive reasons, or (b) it's unfavorable. The Krotez 2023 SOFE paper is the most likely source.

### 2. Demonstrated vacuum re-establishment and vortex reformation at >0.3 Hz on a subscale (~2 m diameter) system with fusion-relevant energy deposition
**Direction:** Higher confidence in viability.

If LM26 or a follow-on experiment demonstrates stable liquid metal vortex reformation within 3 seconds after a MJ-scale pulse (enabling 0.3 Hz operation), the 1 Hz commercial target becomes plausible with incremental engineering improvements (larger pumps, faster valves). 0.3 Hz would reduce electric output by 70% but the capital cost structure (eliminated magnets, eliminated target factory) still yields competitive LCOE if overnight capital reductions hold.

**Likelihood:** Medium-high. General Fusion is actively running LM26 compression tests. The April 2025 first plasma compression milestone was announced; vacuum reformation data at <10 second timescales would be the next logical disclosure.

### 3. Published piston system capital cost or a detailed costing breakdown from the FDP (Fusion Demonstration Plant) program
**Direction:** Either direction.

If the piston system costs <$10M for a 150 MWe module (i.e., <10% of library default C220104), the 15% override is conservative and LCOE could be 5–10% lower. If the piston system costs >$25M (i.e., >50% of library default), LCOE rises by 10–15% and the structural capital advantage over tokamaks shrinks materially.

**Likelihood:** Low. The FDP is currently on hold (UK plant construction paused) and costing details are likely proprietary. The "major automaker" partnership may yield manufacturing cost data but this would be commercially sensitive.

