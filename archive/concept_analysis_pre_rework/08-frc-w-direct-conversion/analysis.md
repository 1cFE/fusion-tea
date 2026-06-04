---
ID: 08-frc-w-direct-conversion
Concept: FRC w/ Direct Conversion
Company: Helion Energy
Status: draft
Created: 2026-03-29
Approved-Date:
Reuses: []
---

# D1+ Analysis: FRC w/ Direct Conversion (Helion Energy)

---

## Section 1: Availability of Data

**Rating: Limited**

Helion Energy is the world's best-funded private fusion company (~$2.2B raised as of 2025) and has operated seven prototype generations over more than a decade. This history produces a recognizable public record but not a deep one. The available sources cluster into three tiers:

**Company-produced materials** (primary): Helion's website publishes conceptual explanations, milestone press releases, and a FAQ covering FRC physics, the D-He3 fuel choice, and the direct energy recovery mechanism. The February 2026 milestone announcement confirmed D-T fusion at 150M°C and 13 keV on Polaris. These are marketing and communications materials, not engineering documents — they state performance claims without uncertainty ranges, diagnostic details, or falsifiable data.

**Third-party analyses**: Contrary Research published a company profile that includes direct CEO quotes on magnet materials and energy recovery constraints [contrary-research-helion.md]. An ARPA-E presentation slide (archived on DocsLib) provides the most quantitative public design-point data available: 50 MW at 2 Hz, η·Q = 0.2×1.2, and a magnetic recovery efficiency η=0.7 [docslib-helion-arpa-e-presentation.md]. This presentation is undated but appears to correspond to Helion's ARPA-E grant period (pre-2020 based on prototype generation context).

**Peer-reviewed literature**: An FRC experimental database spanning six decades and over 600 published papers exists for the FRC concept generally (LANL FRX series, UW LSX, AFRL experiments). Kirtley & Milroy (J. Fusion Energy, 2023) published an FRC scaling paper from Helion's principals. Slough et al. (Nuclear Fusion, 51(5), 2011) covers merging and compression of FRC plasmoids. These cover the underlying physics but not Helion's commercial device.

> "We've built and operated seven prototypes, setting and exceeding more ambitious technical and engineering goals each time. The historic results from our deuterium-tritium testing campaign on Polaris validate our approach to developing high power fusion and the excellence of our engineering."
> — helion-milestones-feb2026.md, §Polaris D-T Milestone

**Critical absence of an independent plant study.** No public equivalent of ARIES, ARC, or PROCESS outputs exists for Helion. Orion (the first commercial plant, under construction in Malaga, WA as of July 2025 with a 2028 Microsoft grid delivery target) has not had its engineering specifications published. The dossier confirms that "no peer-reviewed reactor engineering design document has been published — Orion's detailed specifications are proprietary."

**Key data gaps that limit this analysis:**
- No published Q (gain) values for any Helion prototype
- No fusion energy yield per pulse (joules/shot) disclosed for Trenta or Polaris
- No achieved rep rate data for Polaris
- No Orion capital cost or subsystem breakdown
- No D-He3 plasma operation data (all public experiments are D-D or D-T)
- No He3 self-breeding demonstration at any scale

---
[1] helion-milestones-feb2026.md, §Polaris: "first privately developed fusion energy machine to demonstrate measurable deuterium-tritium (D-T) fusion and achieve plasma temperatures of 150 million degrees Celsius"
[2] docslib-helion-arpa-e-presentation.md, §Energy Efficiency: "η (=Ed/Eplasma) · Gain = 0.2 · 1.2 with magnetic energy recovery; Magnetic energy recovery efficiency: η=0.7"
[3] helion-prototype-generations.md, §Technology: six decades of FRC experimental database, over 600 published papers from primary U.S. and Japanese programs

---

## Section 2: Challenges in Capturing System Function

Helion's FRC + direct conversion approach is structurally unlike any other fusion concept in this study. The system operates as a pulsed RLC circuit — capacitor banks discharge through aluminum coils to form, accelerate, collide, and compress FRC plasmoids, then recover energy from the expanding magnetized plasma via Faraday induction. This architecture creates distinctive LCOE modeling challenges that have no ready analogues in tokamak TEA literature.

### 1. No Published Q Values: The Central Modeling Blocker

The most fundamental LCOE parameter for any fusion concept is the gain Q (fusion energy out / input energy). Helion has never disclosed a measured Q value for any prototype. The ARPA-E presentation states an η·Q product of 0.2×1.2=0.24 at a design point, where η=0.2 is the coupling efficiency (fraction of stored capacitor energy deposited into the plasma) and Q=1.2 is the implied plasma gain [1]. This is the only published Q-adjacent figure in the public record. Without verified Q values, all LCOE calculations based on fusion yield are speculative.

### 2. The Pulsed RLC Economics: Energy Recovery is the Master Lever

Unlike all other fusion concepts, Helion does not require ignition (Q >> 1) to achieve net electricity. The architecture allows net output when:

> (η_coupling × Q_plasma × η_direct_conversion) + (η_magnetic_recovery × (1 - η_coupling)) > 1

At the ARPA-E design point (η_coupling=0.2, Q=1.2, η_magnetic_recovery=0.7), the first term contributes ~0.20 (fusion) and the second term ~0.56 (recovered magnetic energy), for a total round-trip recovery of ~0.76 before direct conversion losses. The implication is that the economics are dominated not by fusion yield but by magnetic energy recovery efficiency. Helion demonstrated >95% round-trip energy recovery at subscale in 2015 [2]. Whether this holds at commercial rep rates and field strengths is entirely uncharacterized publicly.

> "95% of input energy after each pulse must be recovered for net electricity"
> — contrary-research-helion.md, §Energy Recovery

This 95% figure from Contrary Research appears inconsistent with the η=0.7 from ARPA-E. The discrepancy likely reflects different definitions: the 95% may refer to the RLC circuit's charge/discharge efficiency alone (the passive energy recovery), while η=0.7 captures the full magnetic-to-electrical conversion including losses in the plasma interaction. This unresolved ambiguity is a modeling risk: a 10 percentage-point drop in recovery efficiency from 95% to 85% would materially change the economics.

**TEA failure consequence:** If η_recovery falls below ~90% (from the 95% target), the round-trip energy balance becomes negative at the ARPA-E design point (η_coupling=0.2, Q=1.2) — the plant consumes more input energy than it recovers and LCOE is undefined as a power producer. Recovery efficiency is therefore a threshold parameter, not a gradual cost penalty; the model must treat it as a go/no-go sensitivity, not a continuous sensitivity.

### 3. Rep Rate Scaling: 1200× from Trenta to Commercial Design Point

The economics of a pulsed system depend directly on rep rate × fusion energy per shot. Trenta operated at approximately one pulse every ten minutes [3]. The ARPA-E 50 MW design point requires 2 Hz [4]. Commercial targets range from 2 Hz to "every few seconds" (Contrary Research) to speculative 10-60 Hz (website). The gap from Trenta to the 2 Hz design point is a factor of ~1200 in pulse frequency.

This gap is not a physics challenge but an engineering one: capacitor bank recharge time, thermal management of the coils between pulses, diagnostic latency between shots, and mechanical stability of the accelerator structure. None of these have been characterized publicly at anything approaching 1 Hz.

> "Trenta: pulse every 10 minutes; Commercial: pulses every few seconds"
> — contrary-research-helion.md, §Repetition Rate

**TEA failure consequence:** Rep rate failure is a proportional cost penalty, not a binary cliff: if Polaris achieves 0.5 Hz rather than 2 Hz, the capital cost per MWe quadruples (same plant infrastructure, one-quarter the annual output). Unlike the η_recovery threshold, this failure mode degrades LCOE continuously and remains a power plant — just an expensive one. The model should treat rep rate as a primary sensitivity variable with floor, mid, and high scenarios.

### 4. D-He3 Fuel: The Performance-Cost Duality

D-He3 is both Helion's primary cost advantage and its primary technical risk. The advantages are structural: D-He3 produces only ~5% of its energy as fast neutrons [5], eliminating the need for a tritium breeding blanket, reducing activation, and enabling lighter shielding. The RLC direct conversion architecture captures the 95% charged-particle energy directly. Helion self-breeds He3 from D-D side reactions without external fuel input.

The risks are equally structural: D-He3 requires ~200M°C (~17 keV) for commercial operation, versus the 100M°C threshold crossed by Trenta and the 150M°C milestone on Polaris. No D-He3 fusion has been demonstrated in any Helion prototype. The temperature gap from current capability (13 keV at 150M°C) to D-He3 ignition threshold (~17 keV) is approximately 30%, but achieving it reliably at rep rate with sufficient yield is qualitatively harder than the temperature number suggests.

**TEA failure consequence:** If D-He3 operation cannot be achieved, Helion reverts to D-T fuel — this is not a minor adjustment. D-T requires a tritium breeding blanket (eliminating the primary structural cost advantage), restores 80% neutron loading (heavy shielding, activation management, wall replacement), and makes He3 self-breeding irrelevant. The LCOE model for a D-T FRC is architecturally closer to a pulsed MIF device than to Helion's commercial concept and would need to be rebuilt from different foundations.

### 5. Magnetic Field Scaling: 8 T → 40 T

Trenta demonstrated >8 T compressed field. Polaris targets 15 T+. The reactor design point requires 40 T. The progression from 8 T to 40 T represents a 5× increase in field, a 25× increase in magnetic pressure (B²/2μ₀), and corresponding increases in mechanical stress on the coil structure. Pulsed aluminum coils at 40 T is outside demonstrated experience. The ARPA-E presentation specifies 20 T for its experiment and 40 T for the reactor [4], with no intermediate demonstration at commercial scale.

**TEA failure consequence — two-regime structure.** Compression field failure has a different character depending on which regime Helion is in:

- **Below the D-He3 ignition threshold (binary cliff):** Final compressed plasma temperature scales approximately as a power of compression field. Polaris demonstrated 13 keV at ~15 T; the D-He3 commercial threshold is ~17 keV (~200M°C). Below the ignition threshold, D-He3 fusion is kinematically inaccessible regardless of other system parameters — this is a cliff, not a penalty. At the current 15 T achieved field, Helion is approximately at the boundary of this regime: the ~30% temperature gap from 13 keV to 17 keV corresponds to the remaining compression field headroom Polaris has not yet demonstrated. If the 40 T target cannot be reached and the achievable field does not clear the D-He3 ignition threshold, the entire commercial fuel strategy fails — no gradual degradation, the concept forces a D-T fallback.

- **Above the D-He3 ignition threshold but below 40 T (proportional penalty):** Once the plasma temperature clears ~17 keV, D-He3 fusion is achievable. But the 40 T commercial target is a design-point choice, not the ignition minimum — it provides margin for sufficient yield (Q) and sustainable pulsed operation. In this regime, undershoot in compression field produces proportionally lower Q per pulse, proportionally less fusion energy per shot, and a corresponding LCOE penalty that scales inversely with the reduction in yield. Unlike the η_recovery threshold and the D-He3 ignition cliff, this proportional regime does not produce a no-go condition: Helion remains a power plant with a worse LCOE.

The modeling consequence is that the model should carry a field-undershoot scenario distinct from the D-T fallback: a "low-field D-He3" scenario (field clears ignition threshold at 17 keV but falls short of 40 T) captures the proportional penalty regime, while the D-T fallback scenario captures the binary cliff below ignition.

### 6. He3 Fuel Cost and Breeding Economics

Commercial He3 is extremely scarce. Helion's stated plan is self-breeding via D-D side reactions (50% of D-D reactions produce He3 directly; 50% produce tritium which decays to He3 at 5.5%/year). The economics of this breeding cycle at commercial scale — the breeding chamber, the tritium handling and storage system needed during the 12.3-year decay waiting period, the isotopic separation — are not modeled or published anywhere. He3 costs at commercial scale are a genuine unknown that could materially impact LCOE if the breeding system is costlier than the D-He3 fuel savings from reduced neutron management.

**TEA failure consequence:** If He3 self-breeding fails, commercial D-He3 operation has no viable fuel path — natural He3 supply cannot support even a single 50 MWe plant. This makes self-breeding a binary prerequisite for the entire commercial concept: LCOE is undefined for D-He3 operation if breeding fails, regardless of how favorable Q, η_recovery, or rep rate may be. The model should include a D-T fallback scenario rather than treating D-He3 as the single modeling path.

### 7. O&M Cost: No Analogues at Pulsed EM Scale

Unlike tokamaks (well-characterized O&M from ITER and plant studies) or laser IFE (consumable targets at scale), Helion's pulsed aluminum-coil system has no published maintenance literature. Coil fatigue, dielectric aging in capacitors, and quartz tube replacement schedules at 2 Hz × 50 MW are not characterized publicly. A prior handwritten assessment noted this as a key modeling gap [6].

---
[1] docslib-helion-arpa-e-presentation.md, §Energy Efficiency: "η (=Ed/Eplasma) · Gain = 0.2 · 1.2 with magnetic energy recovery"
[2] helion-prototype-generations.md, §Technology: "Demonstrated the first direct magnetic energy recovery from a subscale pulsed magnetic system with over 95% round-trip efficiency for over 1 million pulses"
[3] contrary-research-helion.md, §Repetition Rate
[4] docslib-helion-arpa-e-presentation.md, §Power and Repetition: "50 MW at 2 Hz repetition rate (Fusion Engine design point)"
[5] helion-website-technology.md, §Fuel: D-He3 "releases only 5% of its energy in the form of fast neutrons"
[6] handwritten/08-frc-w-direct-conversion.md, §Deliverable 2

---

### 8. Modeling Approach

**Free-form modeling is required.** This concept has no thermal conversion cycle, no steam generator, and no breeding blanket — the entire CAS20/CAS22 cost structure of a conventional fusion plant applies differently or not at all. A standard 1costingfe template (built around thermal-cycle fusion plants) cannot capture Helion's architecture without substantial modification. A free-form LCOE model treating the capacitor bank + pulsed coil system as the primary capital item, and the direct energy recovery efficiency as the primary performance parameter, is the appropriate starting point.

**Top 2 LCOE sensitivity parameters** (in order of impact):

1. **η_recovery (magnetic energy recovery efficiency)**: As shown in Section 2.2, this is a threshold parameter. At the ARPA-E design point (η_coupling=0.2, Q=1.2), net electricity requires η_recovery ≥ ~90%. The publicly cited range of 70–95% spans the go/no-go boundary. Sensitivity runs should cover η_recovery = 0.70, 0.85, 0.90, and 0.95; the latter two are the meaningful commercial range.

2. **Rep rate (pulses per second)**: Capital cost per MWe scales inversely with rep rate — halving rep rate doubles all capital cost on a per-MWe basis. The gap between Trenta (~0.002 Hz) and the commercial design point (2 Hz) is three orders of magnitude. Sensitivity runs should cover 0.5 Hz, 1 Hz, and 2 Hz.

**Testable hypotheses for the cost model:**

- **H1 (η threshold):** Net electricity output requires η_recovery ≥ 0.90 at the ARPA-E design point. A 5 percentage-point drop from 0.95 to 0.90 reduces net output by approximately 50% [inferred from the RLC balance in Section 2.2]; a drop to 0.85 eliminates net output entirely. The model should confirm this numerically as the first validation.

- **H2 (rep rate × capital cost):** At 2 Hz with 25 MJ/pulse and a 50 MWe net output, the capacitor bank capital cost per MWe is determined by ($/J × 25 MJ × N_units) / 50 MWe. For LCOE < 50 c/kWh, the effective bank cost must fall below approximately $0.50/J (analogous to the MagLIF viability threshold in 07-maglif analysis). If the current pulse power industry baseline of ~$5/J holds, LCOE exceeds 500 c/kWh at this design point — requiring either dramatic cost reduction or a substantially different architectural parameter.

- **Scenario branch condition (D-T fallback):** If D-He3 operation is not achieved — either because the compression field cannot clear the ~17 keV ignition threshold or because He3 self-breeding fails — the D-T fallback requires a structurally separate model. The D-T branch adds a tritium breeding blanket (~$200–500M capital, from 01-hts-compact-tokamak analysis §CAS22 Breeding), eliminates the direct conversion advantage for ~80% of fusion energy (only the ~20% charged-particle fraction remains directly recoverable), and reinstates commercial tritium supply costs. These are architectural substitutions, not parameter perturbations — they cannot be tested as a sensitivity run on the D-He3 base model. Build the D-T branch as a parallel free-form model with its own parameter table, using the D-He3 model as structural contrast rather than a base case. This reframes what was labeled H3: it is a branch precondition, not a testable hypothesis within the D-He3 model.

**D-T fallback model structure.** The D-T branch requires a structurally different model from the D-He3 base case. Four parameters change at the architecture level: (1) **Neutron energy fraction** rises from ~5% to ~80% — the direct inductive recovery system captures only the ~20% charged-particle fraction, not the ~95% it captures in D-He3 mode; (2) **Breeding blanket (CAS22)** is reinstated — lithium blanket required for tritium production, estimated $200–500M capital [from 01-hts-compact-tokamak analysis §CAS22 Breeding]; (3) **Tritium supply** transitions from interim (Polaris testing) to full commercial supply at ~0.1–0.3 kg/year per 50 MWe plant, at ~$35,000/g [from 01-hts-compact-tokamak analysis §Tritium]; (4) **He3 breeding economics drop out entirely** — the D-D side reaction cycle and isotopic separation plant are not needed. The result is a pulsed FRC architecture with D-T fuel and partial direct conversion — structurally closer to a pulsed MIF device (compare MagLIF §07-maglif) than to Helion's commercial concept, and requiring a separate LCOE model rather than a parameter swap on the D-He3 model.

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

---

**D-He3 Fusion in the Colliding FRC — TRL 2–3**

- **Demonstrated**: D-D fusion (indirect, via neutron diagnostics across prototype generations). D-T fusion at 150M°C / 13 keV on Polaris (Jan-Feb 2026) — the first D-T fusion by a private fusion company [helion-milestones-feb2026.md §Polaris]. Earlier achievement: 100M°C on Trenta with 8 keV ion temperature.
- **On paper only**: D-He3 operation at 200M°C / ~17 keV. No D-He3 plasma data exists in any Helion prototype. The ~30% ion temperature increase from Polaris' current 150M°C to the D-He3 threshold is not trivial.
- **Missing at scale**: Demonstrated fusion gain (Q) at any level in D-He3 fuel. Reliable, rep-rated D-He3 ignition and yield per pulse. Validation that the collision/compression dynamics scale to 40 T and 200M°C.

---

**He3 Self-Breeding Cycle — TRL 2–3**

- **Demonstrated**: D-D reactions are understood physics. Tritium decay to He3 is well-characterized. Helion received regulatory approval to possess and use tritium for Polaris testing (first company to do so) [helion-milestones-feb2026.md §Polaris].
- **On paper only**: He3 capture and separation from the D-D exhaust at scale. Tritium storage for the 12.3-year decay period at commercially meaningful inventory levels. He3 separation from the D-He3/D-D plasma exhaust.
- **Missing at scale**: An operational He3 breeding cycle at any significant throughput. The economics of tritium storage and He3 separation at GW-scale fuel demand. Regulatory framework for tritium inventory at commercial plant scale.

---

**Rep-Rated Pulsed Operation at Commercial Duty Cycle — TRL 2–3**

- **Demonstrated**: Trenta ran 10,000 pulses over 16 months continuous operation at ~1 pulse/10 minutes [helion-website-technology.md §Prototypes]. This demonstrates long-term system reliability but not commercial rep rate.
- **On paper only**: Polaris targets ~1 Hz (one pulse per second). The 2 Hz ARPA-E design point [docslib-helion-arpa-e-presentation.md §Power]. Long-term commercial targets of 10-60 Hz.
- **Missing at scale**: Capacitor bank recharge systems capable of sustained 1+ Hz operation. Coil thermal management between pulses. FRC formation and injection at 1 Hz. No public data on achieved rep rate for Polaris, which became operational at end of 2024 [helion-milestones-feb2026.md §Polaris]. The 150M°C milestone press release made no mention of rep rate achieved.

---

**Commercial-Scale Magnetic Compression (40 T) — TRL 3**

- **Demonstrated**: >8 T on Trenta [helion-website-technology.md §Plasma Parameters]. >10 T implied by Trenta's successor progression. 15 T+ targeted for Polaris. 20 T for the ARPA-E experiment [docslib-helion-arpa-e-presentation.md §Magnetic Fields].
- **On paper only**: 40 T reactor compression field. This field strength in pulsed aluminum coils is not established technology.
- **Missing at scale**: Demonstrated 40 T pulsed compression coil system with adequate lifetime at commercial rep rate. Mechanical design to withstand the ~25× increase in magnetic pressure compared to Trenta.

> "20 Tesla: ARPA-E experiment compression capability; 40 Tesla: Target reactor compression field"
> — docslib-helion-arpa-e-presentation.md, §Magnetic Fields

---

**Direct Inductive Energy Recovery System — TRL 4–5**

- **Demonstrated**: >95% round-trip energy recovery from a subscale pulsed magnetic system at over 1 million pulses (2015, Grande prototype) [helion-prototype-generations.md §Technology]. The underlying mechanism (Faraday induction in aluminum coils driven by expanding magnetized plasma) is established physics. Modern high-voltage IGBTs enable this recovery.
- **On paper only**: Recovery efficiency at 15–40 T field strengths and at D-He3 plasma conditions. Recovery efficiency at 1+ Hz sustained operation.
- **Missing at scale**: Full-plant direct conversion system operating continuously at 50 MWe output level. Confirmed recovery efficiency at commercial conditions (not subscale 2015 demo).

---

**Pulsed Electromagnetic Coil and Capacitor Bank System — TRL 5–6**

- **Demonstrated**: Seven prototype generations of increasingly capable pulsed EM systems, from Grande (4 T, 2013) through Polaris (15 T+ target, 2024–). >50 MJ capacitor bank on Polaris, charged to tens of thousands of volts, driving ~720 miles of coaxial cables [helion-website-technology.md §Capacitor Bank, §Magnets/Coils]. In-house manufacturing of quartz tubes and high-voltage capacitors [contrary-research-helion.md §In-House Manufacturing].
- **On paper only**: Long-duration, rep-rated performance of capacitors and coils at commercial duty cycle. Coil replacement schedule and fatigue lifetime.
- **Missing at scale**: Cost and supply chain for commercial-scale capacitor bank at 2+ Hz sustained operation. Component lifetime data at 10^7–10^9 pulses (comparable to the lifetime requirement in MagLIF literature for pulsed power systems).

---

**FRC Formation, Acceleration, and Merging Physics — TRL 6**

- **Demonstrated**: Two FRC plasmoids formed, accelerated to >300 km/s from opposite ends, colliding and merging in the center — demonstrated across six prototype generations [helion-website-technology.md §Confinement]. FRC plasma density of 3×10^22 ions/m³ and confinement time of 0.5 ms demonstrated on Trenta [helion-prototype-generations.md §Trenta].
- **On paper only**: FRC stability at 40 T compression and 200M°C with D-He3 fuel.
- **Missing at scale**: Collision efficiency and stability maintenance at 40 T. Scaling to commercial ion densities and temperatures while maintaining adequate confinement.

---

**Plasma-Facing Structures and Shielding — TRL 5–6**

- **Demonstrated**: Polaris is 25% larger than Trenta specifically to ensure "ions do not damage the vessel walls" [helion-prototype-generations.md §Polaris], indicating awareness and management of plasma-wall interaction. Borated polyethylene and borated concrete shielding demonstrated at Polaris scale.
- **On paper only**: First-wall material selection and lifetime for commercial D-He3 operation with 2.45 MeV neutrons at commercial rep rate.
- **Missing at scale**: Wall loading and replacement schedule at 50–500 MWe power levels and 2+ Hz rep rate. Materials certification for the regulatory environment.

---

**Balance of Plant (No Steam Cycle) — TRL 8–9 (as a design simplification)**

The absence of a steam/thermal cycle is architecturally significant. Conventional Rankine or Brayton cycles for power conversion are TRL 9 technology. Helion's direct conversion eliminates this subsystem entirely for the ~95% charged-particle fusion energy fraction, reducing plant complexity by removing the steam generator, turbines, condensers, and heat exchangers. The remaining ~5% neutron energy fraction from D-He3 requires some thermal capture, but this is minor. This design choice is a genuine TRL advantage relative to all thermal-conversion fusion concepts.

---

## Section 4: Key Materials and Supply Chain Considerations

### High-Voltage Pulsed Capacitors

The capacitor bank is the heart of the Helion system — the energy storage and delivery mechanism. Polaris uses >50 MJ in thousands of capacitors charged to tens of thousands of volts [helion-website-technology.md §Capacitor Bank]. Helion manufactures quartz tubes and some capacitors in-house and sources others externally. Contrary Research explicitly identifies the supply chain as "Helion's main potential risk" [contrary-research-helion.md §In-House Manufacturing].

Commercial high-voltage pulse capacitors for repetitive use exist but are a specialty item with limited suppliers. At 2 Hz × 50 MW, the total pulse energy is 100 MJ/s = 100 MW of cycling through the bank per second. Capacitor lifetime at this duty cycle, and the supply volume needed for Orion and subsequent plants, is not published. Unlike tokamak economics where the dominant capital item (REBCO tape) has a visible market, there is no publicly available $/J curve for Helion-specification pulse capacitors at the required lifetime and rep rate.

### Aluminum Coils and Custom Alloy Cables

Helion uses "regular aluminum magnets" (CEO quote, [contrary-research-helion.md §Magnet Materials]), not superconductors. This is a deliberate and cost-advantageous choice: no cryogenic plant, no REBCO tape, no quench protection system. The ~720 miles of coaxial cables per plant use copper, aluminum, and custom-metal alloys [helion-website-technology.md §Magnets/Coils]. The "custom-metal alloys" formulation is unexplained — this may refer to high-conductivity alloys needed for pulse performance at low resistive loss. Supply chain concentration risk depends on the specifics of these alloys, which are not disclosed.

Unlike MagLIF capacitors (where $/J cost learning curves exist from commercial pulsed power literature) or tokamak REBCO (where supply ramp-up trajectories are tracked), there is no published learning rate or market trajectory for Helion's specific coil-and-cable configuration.

### He3 Supply and Tritium Handling

He3 is the most consequential supply chain issue for this concept. Natural He3 is produced primarily as a byproduct of nuclear warhead tritium maintenance (US DOE) and is available in limited quantities at high cost. Commercial D-He3 fusion at 50-500 MWe scale cannot be supported by natural He3 supply — Helion's entire commercial viability depends on self-breeding.

The breeding pathway: D-D reactions produce He3 (50% directly) and tritium (50%). Tritium decays to He3 with a 12.3-year half-life (5.5%/year). This creates a long-cycle inventory management problem: tritium produced today becomes He3 12+ years from now. During fleet scale-up, there is a lag period where tritium inventory must be accumulated and stored before He3 breeding supports fuel demand.

Helion is currently using externally-sourced tritium for Polaris D-T experiments (the first company to receive regulatory approval for this) [helion-milestones-feb2026.md §Polaris]. This tritium testing pathway is a prudent stepping stone but does not demonstrate D-He3 self-sufficiency.

A prior analysis estimated that "He3 costs are enormous. If Helion consumes significant portion of the inventory before setting up breeding, the costs would go through the roof." [handwritten/08-frc-w-direct-conversion.md §LCOE Model]. This framing understates the structural nature of the problem: at commercial scale with no alternative He3 source, the breeding cycle must be operational and self-sustaining before significant power production can occur.

### Neutron Shielding Materials

Borated polyethylene and borated concrete, similar to hospital particle beam shielding [helion-website-technology.md §Neutron Management]. These are commodity materials with no supply chain constraints. The ~1 meter solid barrier requirement is far lighter than D-T shielding requirements, confirming the D-He3 neutron penalty reduction. This is a genuine cost advantage with no supply risk.

### No REBCO or HTS Materials Required

In contrast to all tokamak and stellarator concepts in this study, Helion requires no REBCO tape, no Nb₃Sn, no LHe cryogenics, and no superconducting magnet infrastructure. This eliminates the most capital-intensive supply chain challenge in conventional fusion (current REBCO prices of $30-100/kA-m, capacity measured in hundreds of km/year) and removes the cryogenic plant entirely. This is a significant structural supply chain advantage.

### Quartz Tubes

In-house manufacture [contrary-research-helion.md §In-House Manufacturing]. Quartz tubes are used in the FRC formation chambers. Industrial quartz manufacturing is mature (optical fiber, semiconductor, specialty glass industries), but Helion's specific geometry and purity requirements are not published. The self-manufacturing of these components suggests specialized requirements not met by standard commercial supply.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Plasma temperature (D-T, achieved) | 150M°C (13 keV) | helion-milestones-feb2026.md §Polaris D-T Milestone | high | Polaris, Jan-Feb 2026; peer-reviewed diagnostic confirmed |
| Plasma temperature (D-He3 target) | ~200M°C (~17 keV) | helion-website-technology.md §Fuel | high | Commercial operating target; ~30% above current |
| Plasma temperature (Trenta, achieved) | 100M°C (8-9 keV) | helion-prototype-generations.md §Trenta | high | Set the commercial fusion temp record prior to Polaris |
| Compression field (Polaris target) | 15 T+ | helion-website-technology.md §Magnets/Coils | high | Design target; achievement not yet confirmed publicly |
| Compression field (reactor target) | 40 T | docslib-helion-arpa-e-presentation.md §Magnetic Fields | high | ARPA-E presentation design point |
| Compression field (Trenta, demonstrated) | >8 T | helion-website-technology.md §Plasma Parameters | high | Demonstrated, highest confirmed public value |
| Capacitor bank energy (Polaris) | >50 MJ | helion-website-technology.md §Capacitor Bank | high | Plant size; drives capital cost |
| FRC plasmoid velocity | >300 km/s | helion-website-technology.md §Confinement | high | Acceleration target; consistent across sources |
| Plasma confinement time | >1 ms | helion-website-technology.md §Plasma Parameters | high | Trenta; sufficient for pulsed compression |
| Ion temperature (Trenta, peak) | 8 keV | helion-website-technology.md §Plasma Parameters | high | Electron temperature 1 keV — large ion/electron gap |
| FRC beta | ~100% | contrary-research-helion.md §Plasma Parameters | medium | Company claim; high-beta is a feature of FRC topology |
| Rep rate (Polaris design target) | ~1 Hz | helion-website-technology.md §Repetition Rate | medium | Stated target; achieved rate undisclosed |
| Rep rate (ARPA-E 50 MW design point) | 2 Hz | docslib-helion-arpa-e-presentation.md §Power and Repetition | medium | Design point at 50 MW net electric |
| Rep rate (commercial target) | "every few seconds" | contrary-research-helion.md §Repetition Rate | low | Vague; implies 0.5–5 Hz |
| Rep rate (Trenta, achieved) | ~0.0017 Hz (1/10 min) | contrary-research-helion.md §Repetition Rate | high | ~1 pulse per 10 minutes |
| Net electric output (Orion, first plant) | 50 MWe+ | helion-website-technology.md §Power Output | medium | 2028 target under Microsoft PPA |
| Net electric output (future modular) | 500 MWe | helion-prototype-generations.md §Technology | low | Nucor partnership; aspirational |
| η_coupling × Q_plasma (ARPA-E) | 0.2 × 1.2 = 0.24 | docslib-helion-arpa-e-presentation.md §Energy Efficiency | medium | Q_plasma = 1.2 implied; only public Q-adjacent figure |
| Magnetic energy recovery efficiency (η) | 0.7 | docslib-helion-arpa-e-presentation.md §Energy Efficiency | medium | Partial recovery efficiency; appears inconsistent with 95% claim below |
| Direct energy recovery (subscale, 2015) | >95% round-trip | helion-prototype-generations.md §Technology | medium | Grande prototype, >1 million pulses; not at commercial fields |
| Direct energy recovery (commercial claim) | 85-95% | contrary-research-helion.md §Energy Recovery | low | Company marketing range; no independent verification |
| Neutron energy fraction (D-He3) | ~5% | helion-website-technology.md §Fuel | medium | vs. ~80% for D-T; source of structural cost advantage |
| D-He3 reaction yield | 18.3 MeV | helion-website-technology.md §Fuel | high | 3.6 MeV alpha + 14.7 MeV proton; physics |
| Charged particle fraction (D-He3) | ~95% | helion-website-technology.md §Fuel | high | Directly capturable by inductive recovery |
| Prototype size (Polaris) | 19 m long | helion-prototype-generations.md §Polaris | high | 25% larger than Trenta; ion wall damage driver |
| Plasma density (Trenta, compressed) | 3×10²² ions/m³ | helion-prototype-generations.md §Trenta | medium | Achieved; target compressed density 10²³/m³ per ARPA-E |
| Compressed density target (reactor) | 10²³ m⁻³ | docslib-helion-arpa-e-presentation.md §Plasma Parameters | medium | ARPA-E design point |
| Cost target (input energy) | <$0.03/MJ | docslib-helion-arpa-e-presentation.md §Energy Efficiency | low | ARPA-E-era design target; no current equivalent |
| LCOE estimate (first-pass) | ~4 c/kWh | [inferred: handwritten/08-frc-w-direct-conversion.md §LCOE Model; copper coils, no turbines, proprietary model] | low | Prior analyst first-pass; rises to ~20 c/kWh if HTS coils required |
| Capacitor bank cost — pulse power industry baseline | ~$5/J | [inferred: H2 derivation from pulsed power literature; basis from 07-maglif analysis §Capacitor Bank Cost] | low | Current commercial pulsed power baseline; not Helion-specific — represents cost floor without learning curve investment |
| Capacitor bank cost — LCOE viability threshold | ~$0.50/J | [inferred: H2 RLC balance; 50 MW net / 2 Hz / 25 MJ/pulse — see Section 2 H2] | low | At ~$5/J baseline, LCOE exceeds 500 c/kWh at this design point; viability requires 10× cost reduction to ~$0.50/J; neither figure is published by Helion |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q_plasma (measured gain per pulse, any prototype) | proprietary | blocking | No published gain figure; ARPA-E implies Q~1.2 but undated, unconfirmed |
| Fusion energy yield per pulse (J/shot) | proprietary | blocking | No J/shot disclosed for Trenta or Polaris; needed to size capital cost per MWe |
| Achieved rep rate on Polaris | proprietary | blocking | 150M°C milestone made no mention of rep rate |
| Plant capital cost (Orion or any Helion plant) | proprietary | blocking | No published cost estimate from Helion or independent source |
| He3 breeding cycle cost and efficiency | truly-unknown | blocking | No demonstration; cost curve does not exist |
| Capacitor bank capital cost ($/J or $/MWe) | not-yet-sourced | blocking | In-house manufacturing; no published cost per unit energy |
| Component lifetime at 1+ Hz (capacitors, coils, quartz) | truly-unknown | important | No endurance data at commercial rep rates published |
| O&M cost breakdown (fixed + variable, maintenance schedule) | truly-unknown | important | No analogue plant; no Helion operations data published |
| Compression field achieved on Polaris (vs. 15 T+ target) | proprietary | important | Target stated but no achieved field disclosed |
| Tritium storage cost for He3 breeding inventory | derivable | important | [inferred: ~1-5 kg tritium inventory at ~$35,000/g = $35-175M; basis from 01-hts-compact-tokamak analysis §Tritium; scales with plant size and lag time] |
| First-wall / coil replacement schedule | truly-unknown | important | No published maintenance interval for pulsed FRC components |
| Fusion energy per pulse at reactor design point | derivable | important | [inferred: at 2 Hz and 50 MWe, each pulse delivers ~25 MJ fusion energy net, assuming 100% recirculating efficiency; basis: 50 MW / 2 Hz = 25 MJ/pulse] |
| Neutron energy per pulse (2.45 MeV DD neutrons) | derivable | nice-to-have | At 5% neutron fraction and 25 MJ fusion, ~1.25 MJ/pulse neutron load; requires thermal capture |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q_plasma (gain per pulse) — no published value for any prototype | S1, S2, S5 | proprietary | blocking | Kirtley & Milroy (J. Fusion Energy, 2023) may contain indirect data; DOE progress reports if available |
| 2 | Fusion energy yield per pulse (J/shot) — Trenta and Polaris | S1, S5 | proprietary | blocking | Helion technical publications, peer-reviewed diagnostics data |
| 3 | Achieved rep rate on Polaris — milestone press release silent | S1, S3, S5 | proprietary | blocking | Future Helion announcements; GeekWire prototype tour reporting |
| 4 | Orion plant capital cost — no specification published | S1, S5 | proprietary | blocking | Helion investor materials, future SEC/utility regulatory filings if applicable |
| 5 | He3 self-breeding economics — never demonstrated at any scale | S2, S4, S5 | truly-unknown | blocking | No published source; requires Helion experimental data or DOE breeding studies |
| 6 | Capacitor bank capital cost ($/J or $/kWe) | S4, S5 | not-yet-sourced | blocking | Pulsed power literature (Z-IFE study analog), commercial capacitor pricing surveys |
| 7 | 40 T pulsed coil feasibility and cost | S3, S5 | truly-unknown | blocking | IEEE pulsed power literature; Sandia/LANL high-field pulsed magnet work |
| 8 | Component lifetime at 1+ Hz (capacitors, coils, quartz tubes) | S3, S5 | truly-unknown | important | No source exists; Helion internal data required |
| 9 | O&M cost breakdown — fixed vs. variable, maintenance schedule | S2, S5 | truly-unknown | important | No analogue; pulsed power plant literature (NIF operations) for partial analogy |
| 10 | Direct conversion efficiency at commercial conditions (vs. subscale 2015) | S2, S3, S5 | proprietary | important | Helion experimental data; future peer-reviewed publication |
| 11 | D-He3 fusion operation — any experimental data | S1, S3 | proprietary | important | Polaris test program (future); no current public data |
| 12 | Compression field actually achieved on Polaris | S3 | proprietary | important | Helion technical disclosures; GeekWire/press tour data |
| 13 | Tritium storage cost and inventory for He3 breeding lag period | S4, S5 | derivable | important | Extrapolate from D-T tritium cost ($35k/g) and required inventory sizing |
| 14 | First-wall material and replacement schedule for D-He3 neutrons | S3 | truly-unknown | important | No FRC wall loading literature at commercial conditions |
| 15 | Neutron shielding design and cost for commercial D-He3 operation | S4 | not-yet-sourced | nice-to-have | Hospital particle accelerator shielding literature; Helion FAQ analogy |
| 16 | Consistency between η=0.7 and >95% recovery efficiency claims | S2, S5 | not-yet-sourced | important | ARPA-E presentation vs. website/Contrary Research; definitions differ |

---

## Section 7: Cross-Concept Notes

### Concept Family Classification

Helion's approach is **MIF (Magneto-Inertial Fusion)**, not MFE or IFE. The classification is non-obvious because the company's marketing uses "magneto-inertial fusion" [helion-website-technology.md §Confinement] — the same language — but the physical reason matters: two FRC plasmoids are formed by magnetic means but then collide and compress inertially, after which pulsed EM coils apply a second magnetic compression stage. This two-stage sequence (magnetic formation → inertial collision → magnetic compression) places the concept in the hybrid MIF category, not the steady-state MFE category and not the purely inertial IFE category. The dossier schema explicitly records this classification as "pulsed FRC compression (Helion) → MIF."

**Nearest neighbors by confinement family and energy conversion approach:**

| Concept | Family | Key Differentiator from Helion |
|---------|--------|-------------------------------|
| **TAE Technologies (C-2W/Norman)** | MFE — beam-driven steady-state FRC | TAE sustains a steady-state FRC using neutral beam injection, not pulsed compression; no capacitor bank economics; no direct energy recovery — TEA structure is closer to a tokamak (steady-state thermal cycle) than to Helion |
| **General Fusion (MTF)** | MIF — liquid-metal vortex piston compression | Shares pulsed compression concept; uses D-T (not D-He3), mechanical piston drivers (not capacitor banks), and thermal liquid-metal energy extraction (not direct inductive recovery); consumable cost category absent from Helion |
| **MagLIF (Sandia/Z-IFE lineage)** | MIF — pulsed liner Z-pinch | Shares pulsed capacitor-bank driver and rep-rate economics challenge; uses recyclable transmission line targets as per-shot consumables (Helion has none); D-T fuel with thermal conversion; single-shot yield ~GJ vs. Helion's ~MJ/pulse approach |

The ST-HTS comparison below provides architectural contrast, not family similarity. Helion's closest structural analogue within this study is MagLIF — both are pulsed MIF concepts with capacitor-bank drivers, rep-rate economics, and no steady-state plasma.

---

The approved 21-spherical-tokamak-hts analysis is the most relevant prior analysis in this project (steady-state fusion with net electricity target). However, direct parameter transfer from that analysis to Helion is not appropriate — the two concepts share almost no subsystem architecture.

**Key divergences from the ST-HTS baseline (21-spherical-tokamak-hts analysis):**

| Dimension | Spherical Tokamak (HTS) | Helion FRC (Direct Conversion) |
|-----------|------------------------|-------------------------------|
| Confinement | Steady-state toroidal | Pulsed linear compression |
| Magnet technology | REBCO HTS superconductors (20 K cryogenics) | Pulsed aluminum electromagnets (room temperature) |
| Energy conversion | Thermal Rankine/Brayton steam cycle | Direct Faraday inductive recovery |
| Fuel | D-T | D-He3 (self-bred) |
| Neutron load | ~80% energy as 14.1 MeV neutrons | ~5% energy as 2.45 MeV neutrons |
| Breeding blanket | Required (FLiBe or WCCB) | Not required for D-He3 commercial operation |
| Tritium | External supply + blanket breeding | Intermediate only (Polaris testing) |
| LCOE dominant cost driver | Magnet capex + capacity factor | Capacitor bank + rep rate + He3 breeding |

**CAS Account Mapping:**

| CAS Category | Tokamak Treatment | Helion FRC Treatment |
|---|---|---|
| CAS21 (Site/Facility) | Standard | Retained approximately; no heavy civil works for magnet halls |
| CAS22 Magnet systems | REBCO HTS, cryogenic plant (dominant capex) | **Eliminated** — pulsed aluminum coils at room temperature |
| CAS22 Breeding blanket | Required (FLiBe/WCCB, ~$200–500M) | **Eliminated** for D-He3 commercial operation |
| CAS22 Steam generator + turbines | Standard thermal cycle | **Eliminated** — no steam cycle; direct inductive recovery |
| CAS22 Capacitor bank + pulsed coils | Not applicable | **Novel (no CAS analogue)** — primary energy storage and conversion hardware; requires free-form treatment; dominant capex uncertainty |
| CAS22 Direct energy recovery system | Not applicable | **Novel** — Faraday induction recovery replaces power conversion island; TRL 4–5 at commercial conditions |
| CAS22 He3 breeding and isotope separation | Not applicable | **Novel** — tritium storage + separation plant; cost unknown; no commercial analogue |
| CAS23 Thermal balance of plant | Full thermal cycle | Retained for ~5% neutron energy thermal capture only; substantially smaller than D-T equivalent |
| CAS25 Fuel handling | Tritium supply + blanket breeding | Retained for D-D fuel; reduced complexity (no tritium recirculation at commercial scale) |
| CAS26 Instrumentation/control | Standard | Retained; pulsed system may require additional shot-timing control |
| CAS27 Electrical plant | Standard | Modified — capacitor bank recharge infrastructure replaces conventional grid interface |
| CAS91–93 (Financial/O&M) | Well-characterized from ITER/fission | Retained structurally; specific rates unknown (see Section 2.7) |

Summary: Roughly half the standard CAS22 line items are eliminated; two large novel cost categories (capacitor bank and He3 breeding) have no published $/kWe figures and require free-form treatment. The eliminated accounts (magnets, steam cycle, breeding blanket) represent the highest-cost items in conventional fusion TEA, suggesting Helion's capital structure could be materially lower than D-T fusion — if the novel items prove tractable.

**What transfers from 01-hts-compact-tokamak (upstream of 21-spherical-tokamak-hts):**
- Tritium unit cost reference (~$35,000/g) is relevant for sizing He3 breeding lag inventory
- Regulatory cost framework (10 CFR Part 30) applies to Helion as well; regulatory markup uncertainty is shared
- Balance of plant cost benchmarks for the 5% neutron energy thermal capture are potentially applicable

**Shared supply chain non-issues**: Helion requires no REBCO, no LHe, no tungsten divertor, no FLiBe — the four major supply chain challenges in tokamak analyses. This structural advantage is unambiguous from a comparative standpoint.

**Cross-concept family comparison**: The closest structural analogue in this study's concept set is MagLIF (07-maglif analysis), which is also pulsed, also uses a capacitor-bank/pulsed-EM driver, and shares the challenge of rep rate scaling and per-pulse cost structure. Key differences: MagLIF uses D-T (requiring a breeding blanket and conventional thermal conversion), uses recyclable transmission line targets (per-shot consumable cost), and targets much higher single-shot gain (GJ yields). The Helion approach trades per-shot yield for high recovery efficiency, eliminating the consumable cost category entirely. The MagLIF analysis's treatment of capacitor bank cost amortization ($/J cost needing to drop from ~$5/J to <$0.50/J for viability) is the most relevant analogue for Helion's capacitor economics.

No parameters were numerically borrowed from any prior analysis.

---

## Section 8: Sources

1. **helion-milestones-feb2026.md** — Helion's Feb 2026 press release announcing D-T fusion at 150M°C / 13 keV on Polaris, first private company to use tritium for fusion. Primary source for milestone temperature and regulatory timeline.
   - Path: `exploration/phase_1a/research/08-frc-w-direct-conversion/iter-02/sources/helion-milestones-feb2026.md`
   - Origin: https://www.helionenergy.com/articles/helion-achieves-new-fusion-energy-milestones/

2. **helion-prototype-generations.md** — Wikipedia article covering all seven Helion prototype generations, key performance milestones (Trenta density/temperature/confinement time), and the Polaris size/design decisions. Also covers MITRE/JASON 2018 criticism (8 T achieved vs. 40 T needed). Primary source for prototype-level parameter history.
   - Path: `exploration/phase_1a/research/08-frc-w-direct-conversion/iter-02/sources/helion-prototype-generations.md`
   - Origin: Wikipedia (extracted 2026-03-29)

3. **helion-website-technology.md** — Consolidated extraction from multiple Helion website pages covering confinement, fuel cycle, energy capture, magnet design, capacitor bank, plasma parameters, rep rate targets, and neutron management. Most comprehensive single source for technical architecture details.
   - Path: `exploration/phase_1a/research/08-frc-w-direct-conversion/iter-01/sources/helion-website-technology.md`
   - Origin: https://www.helionenergy.com/technology/ and linked articles

4. **docslib-helion-arpa-e-presentation.md** — Archived ARPA-E presentation slide by David Kirtley (CEO). Most quantitative public source: 20 T/40 T field targets, 50 MW @ 2 Hz design point, η·Q = 0.2×1.2, η_recovery = 0.7, and compressed density targets.
   - Path: `exploration/phase_1a/research/08-frc-w-direct-conversion/iter-01/sources/docslib-helion-arpa-e-presentation.md`
   - Origin: https://docslib.org/doc/9103852/helion-energy-david-kirtley-ceo-project-lead-20-tesla-arpa-e-experiment-40-tesla-reactor

5. **contrary-research-helion.md** — Contrary Research company profile with direct CEO quotes ("regular aluminum magnets"), explicit energy recovery constraint (95% recovery required), Trenta rep rate (1/10 min), and supply chain risk identification (quartz tubes + capacitors as "main potential risk").
   - Path: `exploration/phase_1a/research/08-frc-w-direct-conversion/iter-01/sources/contrary-research-helion.md`
   - Origin: https://research.contrary.com/company/helion

6. **Phase 1a Dossier: 08-frc-w-direct-conversion** — Structured research summary with high-confidence values for all 12 schema columns. Primary synthesis document for dossier-level facts (confinement family, fuel, magnet type, energy capture, tritium breeding, neutron management).
   - Path: `exploration/phase_1a/research/08-frc-w-direct-conversion/dossier.md`

7. **Kirtley & Milroy, J. Fusion Energy (2023)** — Peer-reviewed FRC scaling paper by Helion principals. Contains "two supersonic field-reversed configurations (FRCs) merge and the resulting plasmoid is adiabatically compressed to fusion conditions" and provides scaling analysis. Cited in dossier but not directly extracted.
   - https://link.springer.com/article/10.1007/s10894-023-00367-7

8. **Slough et al., Nuclear Fusion 51(5), 2011** — "Creation of a high-temperature plasma through merging and compression of supersonic field reversed configuration plasmoids." The foundational experimental paper from the MSNW/UW lineage. Covers the IPA (Inductive Plasmoid Accelerator) heritage directly preceding Helion.
   - https://doi.org/10.1088/0029-5515/51/5/053008

9. **handwritten/08-frc-w-direct-conversion.md** — Prior analyst first-pass assessment. Contains the only published LCOE model estimate (~4 c/kWh copper coils, ~20 c/kWh with HTS) and the key observation that He3 costs "could go through the roof" if self-breeding is delayed.
   - Path: `exploration/concept_analysis/handwritten/08-frc-w-direct-conversion.md`
