## Design Point

- Name: HESTIA Fusion Pilot Plant — reference operating case (Miyazawa & Goto, Phys. Plasmas 2023)
- Maturity: paper-concept
- P_native: 70.4 MWe
- Grounding: high
- Primary sources:
  - knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/aip-2023-paper-abstract.md
  - knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/helical-fusion-technology-overview.md

## 1. Availability of Data

**Rating: Moderate**

The helical-coil stellarator has moderate data availability across three distinct channels. At the reactor design level, the 2023 AIP Physics of Plasmas paper by Miyazawa & Goto provides a complete published reactor design (HESTIA) with quantitative geometry, physics parameters, and a direct construction cost estimate of USD 5 billion (late-1990s basis). The paper includes detailed subsystem specifications: HTS magnet configuration, liquid metal blanket design, ECRH heating system (60× 250 GHz gyrotrons), and a pellet fueling scheme. However, the cost model explicitly excludes inflation adjustment — the authors estimate a factor-of-2 multiplier to reach current-year costs, creating significant uncertainty in the absolute dollar figures.

At the technology development level, Helical Fusion (the Tokyo-based startup commercializing this concept) provides regular public updates on component milestones via press releases and their website. The October 2025 demonstration of a 40 kA HTS coil at 7 T external field (30-layer REBCO, uninsulated design, >4 m length) is well-documented. The GALOP liquid metal blanket test system is described qualitatively, as is the partnership with Sugino Machine for helical coil winding equipment. However, cost data for these components is absent — no unit costs, no build-of-materials, no supply chain pricing.

At the heritage physics level, HESTIA draws on 25+ years of Large Helical Device (LHD) operations at Japan's National Institute for Fusion Science (NIFS). LHD experimental results provide confinement scaling validation for the heliotron configuration, and the FFHR reactor study series (predating HESTIA) established liquid-metal-compatible structural materials and blanket designs. The Oroshhi-2 test platform at NIFS includes LiPb loops and a planned supercritical CO2 gas turbine demonstration at 20 kWe, supporting HESTIA's claimed >50% thermal efficiency.

**Key data gaps:**

1. **No independent cost validation** — the USD 5 billion direct cost is based on "actual performance of LHD and ITER at the end of the 1990s" without transparency into the underlying unit costs, and without adjustment for post-2000 inflation or supply chain changes.
2. **Component-level cost breakdowns absent** — the breakdown into CAS-level accounts is not provided; only a single lump sum exists.
3. **Thin operational cost data** — no staffing estimate, no maintenance schedule, no fuel processing costs, no component replacement intervals beyond the 6.4-year stated reactor lifetime.
4. **Prototype cost uncertainty** — the paper cites USD 480 million (1990s basis) for a HESTIA-Primary prototype to validate the optimized magnetic configuration, but its scope and deliverables are underspecified.
5. **Blanket material composition unconfirmed** — the specific liquid metal alloy (pure Li, LiPb, or tin-indium-lead-lithium as stated in the AIP paper) is inconsistently described across sources.

Independent peer-reviewed analysis of HESTIA's LCOE or capital cost does not exist in the available literature. The concept's TEA rests on a single-source design study from the developers themselves.

## 2. Challenges in Capturing System Function

The primary LCOE modeling challenges for the helical-coil stellarator, ranked by impact:

**1. Flexible HTS conductor scaling and cost (high impact, high uncertainty)**

The heliotron geometry requires two continuous helical HTS coils that wind through a complex 3D path with non-planar curvature. The WISE (Wound and Impregnated Stacked Elastic tapes) conductor approach — flexible REBCO tape stacking followed by low-melting-point alloy impregnation for structural rigidity — is proprietary and has no established supply chain or unit cost basis. The October 2025 demonstration achieved 40 kA at 7 T in a test coil, but the design field for HESTIA is 8 T at the coil center (9 T at plasma center), and the current density at 20 K in 20 T must reach 400 A/mm². The cost sensitivity is extreme: HTS conductor is the single largest capital cost item in any high-field fusion concept, and the 3D helical geometry requires significantly more conductor length than an equivalent-field tokamak. The AIP paper assumes a cryogenic efficiency of 2% (20 K helium gas cooling vs. 4 K liquid helium), reducing helium consumption by 75%, but this efficiency target is undemonstrated at reactor scale.

> "Flexible enough for complex helical coil winding. After winding, impregnated with low-melting point alloy"
> — helical-fusion-technology-overview.md §HTS Magnets

The lack of a reference unit cost for WISE conductor — or any continuous-helical HTS coil at this field strength and geometry complexity — makes C220103 (confinement magnets) cost estimation speculative. Standard REBCO tape pricing ($30–100/kA-m in 2025) assumes planar winding; the flexibility and impregnation steps add unknown markup.

**2. Liquid metal blanket system cost and corrosion management (high impact, medium uncertainty)**

HESTIA uses a modular liquid metal blanket with free-surface flow over the first wall, eliminating the need for a separate divertor system. This integrated blanket/divertor architecture is cited as a major cost advantage — the authors state that "by skipping the development of individual divertor systems, NBI, and ICH, which are widely recognized as the most difficult issues in fusion reactor development, a fast-track plan is possible" (aip-2023-paper-abstract.md, lines 81-84). However, the liquid metal free-surface flow must survive 14.1 MeV neutron fluence and heat fluxes without excessive evaporation, splashing, or MHD-driven flow disruption. The AIP paper specifies a tin-indium alloy with lead (neutron multiplication) and lithium (tritium breeding), but warns: "Tin is highly corrosive to steel and therefore careful consideration for corrosion protection is required" (aip-2023-paper-abstract.md, lines 227-228). The structural material is non-magnetic reduced-activation high-manganese steel (not conventional RAFM, which is ferromagnetic and incompatible with stellarator field purity requirements). The porous first wall material — pure titanium, titanium alloy, or high-manganese steel fabricated via 3D printing — must provide anti-corrosion oxide layers and high wettability for liquid metal adhesion.

The GALOP test system validates the gas-driven liquid metal pump concept (no rotating parts, developed with Sukegawa Electric), but pump power requirements are "quite unknown at this moment" (aip-2023-paper-abstract.md, lines 244-246). Liquid metal circulation power feeds directly into the recirculating power fraction and therefore Q_eng, but no estimate is provided. The blanket module replacement strategy — 90 modules accessible from an upper port via three-point suspension crane — is architecturally specified but carries no time estimate or cost projection for remote handling operations in an activated environment.

C220101 (blanket), C220102 (shield), and C220108 (divertor) costs are tightly coupled to the liquid metal system's performance and durability, yet no component-level cost breakdown exists.

**3. 250 GHz gyrotron array scaling and efficiency (medium impact, medium uncertainty)**

HESTIA requires 60× 250 GHz, 1 MW, CW gyrotrons distributed across 10 ports for ECRH heating. The AIP paper states: "At the moment, only the development of a 1 MW 170 GHz gyrotron can be found in the ITER program, and a 250 GHz-1 MW-CW gyrotron does not exist" (aip-2023-paper-abstract.md, line 261). The design assumes 50% wall-plug efficiency, matching the ITER 170 GHz gyrotron target. However, higher frequency typically degrades efficiency, and CW operation at 1 MW is undemonstrated at 250 GHz. The steady-state ECH power requirement (84 MW external, per the AIP paper's Q_eng = 2.0 calculation) drives a large auxiliary power system, and any shortfall in efficiency directly reduces net electric output. Helical Fusion lists R&D on "250 GHz, 1 MW, CW gyrotrons" and "integrated simulations targeting 24-hour operating conditions" among active development areas, but no prototype timeline or cost estimate is public.

C220104 (supplementary heating) cost depends on the per-gyrotron unit cost, which is unquoted. ITER's 170 GHz gyrotrons are estimated at several million dollars each; 60 units at comparable pricing would represent hundreds of millions of dollars, but the 250 GHz variant may carry a development premium or, conversely, benefit from future mass production.

**4. Confinement enhancement assumptions (high physics impact, unvalidated)**

The HESTIA physics design assumes a confinement improvement factor H = 1.3 relative to ISS04 scaling, plus a center-peaked heating effect γ_CEPI = 1.18, for a combined enhancement of ~1.5× over baseline stellarator scaling. The AIP paper states: "It should be noted that there is almost no experimental backup to support this optimized confinement" (aip-2023-paper-abstract.md, lines 206-209). The authors propose a HESTIA-Primary prototype (USD 480 million, 1990s basis) to validate the optimized magnetic configuration before committing to the full HESTIA build. If the confinement enhancement does not materialize, the plasma density must increase to maintain fusion power, risking exceedance of the Sudo density limit (already flagged as a concern in the baseline design, requiring off-axis ECH mitigation). Alpha particle confinement is assumed at ε_α = 85%, also without experimental validation. Turbulent transport is assumed negligible.

These assumptions directly affect the fusion power achievable at fixed geometry and field strength, which in turn determines whether 70.4 MWe net electric is feasible at Q_eng = 2.0. The stated Q ~ 13 (fusion power / external heating power) is contingent on these confinement factors; if H or γ_CEPI falls short, Q_eng collapses and the plant may not reach net electricity.

**5. Cost model inflation and currency basis (accounting challenge)**

The AIP paper's direct construction cost of USD 5 billion is based on "the actual performance of LHD and ITER at the end of the 1990s" and explicitly excludes inflation: "if this inflation is taken into account, Cdirect must be modified by a factor of 2 or more" (aip-2023-paper-abstract.md, lines 116-122). This creates a 2× to 2.5× range on the baseline capital cost (USD 10–12.5 billion in current-year dollars) before any concept-specific adjustments. The cost-per-kWh figure of $1.22/kWh (aip-2023-paper-abstract.md, line 169) is similarly stated in 1990s dollars and excludes O&M, financing, and decommissioning — it is a direct construction cost divided by total energy production over the 6.4-year reactor lifetime, not a levelized cost. Without a transparent unit-cost basis or a CAS-level breakdown, it is impossible to inflation-adjust selectively (e.g., labor vs. materials vs. R&D capitalization).

**Minor modeling challenges:**

- **Pellet injection system** — 30-barrel pipe-gun DT-ice pellet injectors (10 injectors = 300 barrels total) with direct fuel gas recycling; no cost or power requirement stated.
- **Supercritical CO2 gas turbine** — >50% thermal efficiency claimed but not yet demonstrated at fusion-relevant scale; the Oroshhi-2 platform targets 20 kWe at 20% efficiency, a 2.5× efficiency gap to commercial target.
- **Initial tritium inventory** — the paper proposes a DD startup phase over "a few months" to breed sufficient tritium for DT operation via DD side reactions, avoiding external tritium procurement. This strategy is unproven at the kg-scale required.
- **Enriched 6Li supply** — the design uses 80 at.% 6Li vs. natural ~8%; isotope enrichment infrastructure and cost are not addressed.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first):

### Flexible 3D HTS Coils for Heliotron Geometry — TRL ~3–4

**Demonstrated**: October 2025 test coil achieved 40 kA at 7 T external field, 15 K, using 30-layer REBCO tape in an uninsulated configuration. Coil length >4 m, conductor cross-section ~3 cm. This is the "world's first demonstration of large-scale HTS coil designed for commercial reactor" using uninsulated design (helical-fusion-2025-2026-updates.md). A custom coil winding machine developed with Sugino Machine is completed and will be transported to the demonstration site in 2026 for on-site assembly of Helix HARUKA (the integrated demonstration device). REBCO tape stacking, helical winding, and low-melting-point alloy impregnation have been validated at subscale.

**On paper only**: Full-scale continuous helical coils at 8 T coil center field (9 T at plasma center) over ~8 m major radius, operating at 20 K with 400 A/mm² current density in 20 T background. Structural delamination resistance and quench protection for uninsulated HTS coils under combined high-field + neutron irradiation + cyclic thermal loads remain undemonstrated. The two helical coils are each ~100+ meters of complex 3D conductor path; no coil of this length and geometry complexity has been built.

**Missing at scale**: Radiation-hardened REBCO insulation and adhesive layers for 14.1 MeV neutron environment. Long-term mechanical fatigue data for impregnated REBCO tape under stellarator-specific stress profiles. Supply chain capacity for km-scale continuous REBCO tape at consistent critical current density (current global production is thousands of km/year; a single HESTIA-class reactor requires an unspecified but likely multi-km length for the two helical coils plus auxiliary coils). Manufacturing throughput for multi-hundred-meter continuous helical windings without joints (joints in HTS coils are high-resistance failure points; the heliotron design minimizes them by using continuous coils, but this shifts risk to the winding process).

### 250 GHz, 1 MW, CW Gyrotrons — TRL ~2–3

**Demonstrated**: 170 GHz, 1 MW gyrotrons for ITER are under development and tested at subscale. ECRH at lower frequencies (110–140 GHz) and lower power (0.5–1 MW, pulsed or short-pulse CW) is routine on existing stellarators (LHD, W7-X). Joint research between Helical Fusion and QST (Japan's National Institutes for Quantum Science and Technology) on 250 GHz, 1 MW, CW gyrotrons is ongoing, with "integrated simulations targeting 24-hour operating conditions" (helical-fusion-2025-2026-updates.md).

**On paper only**: 250 GHz frequency at 1 MW CW power. The AIP paper explicitly states: "a 250 GHz-1 MW-CW gyrotron does not exist" (line 261). The efficiency target of 50% wall-plug is borrowed from the ITER 170 GHz gyrotron program but is unvalidated at 250 GHz. Higher frequency typically increases cavity losses and requires tighter beam quality, both of which can degrade efficiency.

**Missing at scale**: Continuous-wave operation at 1 MW and 250 GHz in a compact, manufacturable package suitable for 60-unit deployment. Long-term reliability under neutron/gamma background from the reactor (gyrotrons in HESTIA are distributed across 10 ports; shielding effectiveness determines whether electronics survive). Manufacturing supply chain for 250 GHz gyrotrons at scale (current suppliers: CPI Canada, Thales, Toshiba, Gycom Russia; none has produced a 250 GHz, 1 MW CW unit).

### Liquid Metal Free-Surface First Wall and Integrated Blanket — TRL ~3–4

**Demonstrated**: GALOP (Gas-driven Liquid metal blanket test system) at Helical Fusion validates a gas-driven pump with no rotating components, developed with Sukegawa Electric. Test system dimensions ~4m × 2m × 2m (helical-fusion-2025-2026-updates.md). NIFS Oroshhi-2 test platform includes LiPb twin-loop systems operational since 2013–2014 and FLiNaK (another molten salt) loops, providing liquid-metal handling infrastructure heritage. High-manganese alumina-formed austenitic steel with silicon addition (developed with Tohoku University, 2024) is characterized as "non-magnetic, low-activation, corrosion-resistant at high temperatures" (helical-fusion-2025-2026-updates.md).

**On paper only**: Free-surface liquid metal flow over the entire first wall (including divertor strike zones) at steady-state under 14.1 MeV neutron wall loading and MW/m² heat flux, without excessive evaporation, MHD instabilities, or splashing. The AIP paper specifies a tin-indium alloy with lead and lithium, but warns of tin's high corrosivity to steel and acknowledges that "hydrogen retention in tin-lead-lithium alloy will be investigated in future studies" (line 228). The porous titanium or high-manganese steel first wall fabricated via 3D printing with anti-corrosion oxide layers and controlled wettability is a design concept but not a demonstrated component.

**Missing at scale**: Integrated blanket module tested under prototypical fusion neutron fluence (no facility yet provides 14 MeV neutrons at fusion-relevant flux over m²-scale areas for extended durations). Liquid metal circulation pump power consumption at reactor scale ("quite unknown at this moment," per the AIP paper, line 245). Remote handling and replacement of 90 activated blanket modules via upper-port access — demonstrated at ITER mock-up scale for tokamak blankets but not validated for stellarator geometry or liquid-metal-wetted components. Tritium extraction from liquid metal at kg/day rates with <1% losses. Corrosion-resistant coating longevity under combined neutron damage + liquid metal attack over multi-year campaigns.

### Tritium Fuel Cycle with DD Bootstrap Startup — TRL ~3–4

**Demonstrated**: Lab-scale tritium handling, permeation barriers, and extraction from liquid breeders. LHD and historical D-T tokamaks (JET, TFTR) have handled gram quantities of tritium. The AIP paper proposes a DD startup operation to self-produce tritium inventory via DD side reactions (D+D → T+p, followed by T decay to He3 over months), avoiding the need for external tritium procurement beyond startup fuel.

**On paper only**: DD operation at sufficient density and confinement time to breed 1+ kg of tritium via DD side reactions within "a few months," then transition to DT operation once the inventory is sufficient. The DD-to-DT transition itself — managing the shift in plasma parameters (reactivity, ash, heating requirements) — is operationally untested.

**Missing at scale**: Closed-loop, kg/day tritium processing at >99% retention efficiency. Real-time tritium accountancy in a liquid metal blanket system (tritium permeates through metals; tracking inventory vs. loss requires continuous monitoring and control). Industrial-scale lithium isotope enrichment for 80 at.% 6Li (current global capacity for >90% 6Li is limited to Russia and China using mercury-based processes banned in the West; the AIP paper does not address this supply chain bottleneck).

### Supercritical CO2 Gas Turbine for Fusion Primary Heat — TRL ~4–5

**Demonstrated**: Supercritical CO2 Brayton cycles exist at pilot scale in non-nuclear applications (waste heat recovery, concentrating solar thermal). The NIFS Oroshhi-2 test platform includes a planned sCO2 turbine demonstration at 20 kWe and 20% efficiency (nifs-ffhr-blanket-heritage.md, line 50). sCO2 turbine technology for fission applications is at TRL 5–6 (DOE funding for demonstrations, but no commercial deployment).

**On paper only**: >50% thermal efficiency at 800–1200 K working temperature (helical-fusion-2025-2026-updates.md, line 51) for a fusion primary heat source, operating continuously in a tritium-contaminated environment. The 2.5× efficiency gap between the Oroshhi-2 demonstration target (20%) and the HESTIA commercial target (>50%) is large. High-temperature heat exchangers compatible with liquid metal coolant and sCO2 working fluid, with tritium containment, are in the design phase but not built.

**Missing at scale**: MW-to-GW scale sCO2 turbines with integrated tritium barrier coatings, long-term reliability under neutron activation of working fluid and structural components, and maintenance protocols for contaminated turbomachinery. Standard Rankine steam cycles are TRL 8–9 for fusion applications (ITER will use one); sCO2 carries a 20–30% efficiency advantage but adds development risk.

### Reactor Core Plasma Optimization and Steady-State Control — TRL ~5–6

**Demonstrated**: LHD has operated since 1998, demonstrating heliotron confinement scaling, steady-state capability (multi-hour discharges), and beta limits. The heliotron magnetic configuration is validated at ~4 m major radius, ~0.6 m minor radius, 3 T on-axis field, with H ~ 1 (no enhancement). ECRH heating and pellet fueling are routine. Stellarator disruption immunity is proven (stellarators have no plasma current, therefore no current-driven instabilities or disruptions).

**On paper only**: Confinement enhancement factor H = 1.3 × γ_CEPI = 1.18 ≈ 1.5× improvement over ISS04 scaling in an optimized heliotron configuration. Alpha particle confinement ε_α = 85%. Turbulent transport suppression. The AIP paper states: "there is almost no experimental backup to support this optimized confinement" (line 207). Density operation near or above the Sudo density limit n_Sudo (baseline design exceeds it; mitigation via off-axis ECH is proposed but untested). Steady-state burn at fusion-relevant density and temperature in a heliotron (LHD has not run DT and has not demonstrated burning plasma).

**Missing at scale**: Year-long continuous DT burn campaigns with ~3-month maintenance intervals as claimed for HESTIA (lines 315, 363). Integrated control of heliotron plasma at Q ~ 13 with ECRH-only heating (no NBI for profile control, no ICRH for ion heating). The HESTIA-Primary prototype (USD 480 million, 1990s basis) is proposed specifically to validate the optimized confinement before full HESTIA construction; without it, the physics case rests on simulation.

### Remote Handling for Modular Liquid-Metal-Wetted Blanket — TRL ~4–5

**Demonstrated**: ITER remote handling prototypes and full-scale mock-ups for tokamak blanket/divertor exchange under activation. The HESTIA design specifies 90 blanket modules accessible via upper port with three-point suspension crane (aip-2023-paper-abstract.md, lines 199-202). The stellarator geometry simplifies access relative to tokamaks (no tight inboard clearance), but liquid-metal-wetted components introduce drying, decontamination, and handling challenges not present in solid-breeder or water-cooled designs.

**On paper only**: Remote handling of liquid-metal-contaminated blanket modules in a stellarator geometry at >80% plant availability. The 3-month maintenance interval claim requires that 90 modules can be inspected, removed if needed, replaced, and re-commissioned within ~10–12 weeks. No time-motion study or operational simulation is provided.

**Missing at scale**: Radiation-hardened robotics and tooling for liquid-metal systems (liquid metal residue on module surfaces complicates handling; tin and lead are particularly difficult to clean). Long-term reliability of remote handling equipment under stellarator-specific neutron/gamma fields (different activation spectrum than tokamaks due to different shielding geometry).

### Cryogenics and Thermal Management (20 K Helium Gas Cooling) — TRL ~6–7

**Demonstrated**: Large-scale helium refrigeration plants exist (ITER-scale at 4 K for LTS magnets). Helium gas cooling at 20 K for HTS is less common but has been demonstrated at subscale (CFS SPARC magnets target similar temperatures). The AIP paper claims 20 K gas cooling reduces helium consumption by 75% relative to 4 K liquid helium, with cryogenic efficiency of 2% (line 217).

**On paper only**: Multi-hundred-meter continuous helical HTS coils cooled to 20 K uniformly, with thermal load from 14.1 MeV neutron heating in the coil structure despite shielding. The AIP paper flags neutron shielding for HTS coils as a concern: "requires blanket expansion or new shield materials for FOAK plant lifetime" (line 325). If neutron heating degrades cryogenic efficiency below 2%, the refrigeration power scales unfavorably.

**Missing at scale**: Integrated cryogenic system for a stellarator with HTS magnets, liquid metal blanket (hot side ~800–1200 K), and sCO2 power cycle — three distinct thermal zones requiring isolation and load management. Experience base exists for fission (LWRs) and LTS tokamaks, but the HTS + liquid metal + sCO2 combination is novel.

### Vacuum Vessel and In-Vessel Structures — TRL ~6–7

**Demonstrated**: LHD vacuum vessel and support structure are operational at full scale. ITER vacuum vessel sectors are under construction (double-wall stainless steel). Stellarator vacuum vessel fabrication is more complex than tokamak (3D shaping) but is a known process.

**On paper only**: Vacuum vessel integrating ports for 60 gyrotrons (distributed across 10 ports), 10 pellet injectors (30-barrel arrays), upper-port blanket module access, and liquid metal blanket attachment points. The AIP paper does not provide a vessel mass estimate or structural analysis.

**Missing at scale**: Manufacturing a heliotron vacuum vessel at ~8 m major radius with port penetrations that maintain field accuracy and minimize neutron streaming. Activation and remote maintenance of vessel internals. These are incremental challenges, not fundamental gaps.

## 4. Key Materials and Supply Chain Considerations

### REBCO Superconducting Tape (critical, supply-constrained)

Global REBCO production capacity is currently thousands of kilometers per year, dominated by Shanghai Superconductor Technology, Faraday Factory Japan, and Commonwealth Fusion Systems. A single HESTIA-class reactor requires an estimated multi-km length for two continuous helical coils plus auxiliary coils (exact length not stated in sources, but a heliotron at ~8 m major radius with two helical windings implies >>1 km per coil when accounting for 3D path length). Current REBCO tape pricing ranges from $30–100/kA-m, but this assumes planar winding; the WISE conductor's flexibility and impregnation process add unknown markup. Critical current density must reach 400 A/mm² at 20 K in 20 T (aip-2023-paper-abstract.md, line 219) — significantly higher than commercially-available tape performance in 2025. Scaling production by one to two orders of magnitude while maintaining Jc uniformity and reducing cost to enable commercial viability is a shared challenge with all HTS fusion concepts.

**Supply chain pinch point**: Only a few global suppliers exist, and REBCO tape production requires rare-earth elements (yttrium, sometimes gadolinium or other lanthanides as substitutes). China controls most rare-earth refining capacity. A single HESTIA reactor competes with tokamak and mirror concepts for the same tape supply; fleet deployment (multiple plants) would require gigawatt-scale tape production infrastructure that does not exist in 2025.

### Tritium (critical, supply-constrained)

The global civilian tritium inventory is approximately 25–30 kg, produced primarily as a byproduct of CANDU heavy-water reactors. A single HESTIA startup under the proposed DD-bootstrap scheme would still require D-D fuel (deuterium is abundant) and ~months of DD operation to breed 1+ kg of tritium via DD → T + p side reactions, followed by T → He3 decay over additional months. Once DT operation begins, tritium self-sufficiency via liquid metal blanket breeding (TBR > 1) is mandatory — external tritium supply is insufficient to support even a single plant's steady-state consumption (~kg/year burn rate at Q ~ 13). The AIP paper assumes 80 at.% 6Li enrichment for the blanket; global enriched 6Li production capacity is small and concentrated in Russia and China (mercury-based enrichment processes banned in the West). Lithium supply itself is abundant (battery industry scale), but isotope enrichment is a bottleneck. Tritium handling, permeation control, and inventory accountancy in a liquid metal blanket system are complex — tritium permeates through metals and escapes unless barriers are effective. Current market rate for tritium exceeds $35,000/kg, but this is irrelevant for fusion (no external market can supply kg-scale continuous burn; self-breeding is existential).

**Sequencing constraint**: The first few DT fusion plants worldwide must demonstrate tritium self-sufficiency (TBR > 1.0 validated in operation) before fleet deployment can proceed. If HESTIA or any other DT plant fails to breed sufficient tritium, the concept is economically and physically non-viable.

### Liquid Metal Blanket Inventory (tin, lead, lithium, indium)

The AIP paper specifies a tin-indium alloy with lead (neutron multiplication) and lithium (tritium breeding). Tin global production is ~300 kt/year (dominated by China, Indonesia); a single reactor's blanket inventory is estimated at multi-hundred tonnes (exact figure not stated, but liquid-metal-cooled reactors typically carry 100–1000 t of coolant depending on geometry and flow rate). Indium is a minor metal produced at ~1 kt/year globally; pricing is volatile (~$200–500/kg historically). Lead is abundant (~5 Mt/year global production, <$2/kg). Lithium metal production for batteries is ~100 kt/year and growing; fusion-scale blanket demand is a small fraction of this. The supply constraint is isotope enrichment (80 at.% 6Li) as discussed above, not lithium availability.

**Corrosion concern**: "Tin is highly corrosive to steel and therefore careful consideration for corrosion protection is required" (aip-2023-paper-abstract.md, line 227). The blanket structural material is high-manganese austenitic steel developed with Tohoku University, but long-term corrosion resistance under neutron damage + liquid metal attack is unproven. If corrosion rates are high, blanket module lifetime shortens, increasing replacement frequency and O&M costs. The first wall uses a 3D-printed porous titanium or high-manganese steel layer with anti-corrosion oxide coating (aip-2023-paper-abstract.md, lines 233-234); titanium is corrosion-resistant but expensive ($20–40/kg for Ti-6Al-4V alloy, higher for nuclear-grade). Fabrication via additive manufacturing adds cost but enables complex geometries for liquid metal flow channels.

### High-Manganese Austenitic Steel (emerging, supply-developing)

The non-magnetic requirement for stellarator blanket structures (to avoid perturbing the external magnetic field) disqualifies conventional RAFM (reduced-activation ferritic-martensitic) steels, which are ferromagnetic. High-manganese austenitic steel with silicon addition (developed by Helical Fusion + Tohoku University, 2024) is non-magnetic, low-activation, and corrosion-resistant, but has never been produced at the multi-hundred-tonne scale required for a reactor blanket and vacuum vessel (helical-fusion-2025-2026-updates.md, line 43). Manganese is abundant (~20 Mt/year global production, <$2/kg); silicon is commodity-scale. The supply chain challenge is not raw material but the production of nuclear-grade alloy plates, forgings, and welded structures with controlled impurities and qualified mechanical properties under neutron irradiation. This is a shared challenge with fission advanced reactor programs (sodium-cooled fast reactors also use austenitic steels), so supply chain development is underway but not fusion-specific.

### 250 GHz Gyrotron Components (niche, supplier-limited)

Gyrotrons for fusion ECRH are produced by a handful of specialized suppliers: CPI Canada, Thales (France), Toshiba (Japan), Gycom (Russia). HESTIA requires 60× 250 GHz, 1 MW, CW units — a quantity that exceeds the current global installed base of fusion gyrotrons by an order of magnitude. The 250 GHz frequency does not yet exist at 1 MW CW; development requires scaling from ITER's 170 GHz units. Key components — electron guns, cavity resonators, output windows (diamond or sapphire for high-power microwave transmission) — are niche items with long lead times. Diamond windows, in particular, are grown via CVD (chemical vapor deposition) and are expensive (~$10–50k per window depending on size and quality); 60 gyrotrons imply 60 windows plus spares. This is not a fundamental bottleneck (diamond CVD is a mature process) but a manufacturing-scale question.

### Deuterium (commodity, abundant)

Deuterium is extracted from water via electrolysis or Girdler-sulfide process. Global production capacity exceeds fusion demand by orders of magnitude (~1000 t/year from heavy water production for CANDU reactors and industrial applications; a single HESTIA burns <100 kg/year at steady state). Current market price ~$1000/kg; fusion fuel cost is negligible relative to capital and O&M.

### Helium (cryogenic coolant — supply concerns for 4K, less critical at 20K)

The AIP paper claims 20 K gas cooling reduces helium consumption by 75% relative to 4 K liquid helium (line 217). Global helium supply has tightened due to CANDU reactor retirements and geopolitical supply concentration (Qatar, U.S., Russia dominate production). However, 20 K operation uses significantly less helium than 4 K (no liquid reservoir, lower refrigeration power), and HTS concepts overall are less helium-intensive than LTS tokamaks. This is a minor advantage relative to ITER-heritage LTS designs but not a major differentiator within the HTS concept set.

### Beryllium and Ceramic Breeder Materials (N/A for liquid metal blanket)

Unlike solid breeder blanket designs (ITER TBM, EU-DEMO HCPB), HESTIA's liquid metal blanket does not require beryllium neutron multiplier or lithium ceramic pebbles (Li4SiO4, Li2TiO3). This eliminates a major supply chain bottleneck: beryllium global production is ~300 t/year (Materion Corp. is dominant U.S. supplier; toxicity and limited mining infrastructure constrain expansion). Liquid metal blankets are therefore simpler from a materials sourcing perspective, though they introduce corrosion and MHD challenges instead.

## 5. Design Point Parameters

The following table describes the HESTIA Fusion Pilot Plant reference operating case from Miyazawa & Goto, Physics of Plasmas 30, 050601 (2023). All parameters are at the native 70.4 MWe scale.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Major radius R0 | 7.8 m | aip-2023-paper-abstract.md Table I, R_c row, HESTIA column (lines 124-134); also line 88 | high | spec key: `R0` |
| Minor radius a | 1.87 m | aip-2023-paper-abstract.md Table I, a_0 row, HESTIA column (lines 124-134) | high | spec key: `plasma_t` (helical coil minor radius ac in source) |
| Aspect ratio A | 4.17 | [inferred: R0/a = 7.8/1.87 ≈ 4.17] | high | informational only |
| Elongation κ | 1.0 | [assumed for heliotron — no elongation stated; heliotrons are typically circular cross-section] | medium | spec key: `elon` |
| On-axis magnetic field B0 | 9 T | aip-2023-paper-abstract.md §II, lines 81, 214 — "approximately 9 T at the plasma center" | high | spec key: `B` (NOT `B0` — canonical name is `B`) |
| Peak field on conductor B_peak | 8 T (at coil center) | aip-2023-paper-abstract.md §II.B, line 214 | high | informational only — library uses on-axis B for coil sizing |
| Plasma volume | ~287 m³ | [inferred: 2π²Raκ ≈ 2π² × 7.8 × 1.87 × 1 ≈ 287 m³] | medium | informational — library back-solves from R0, a, elon |
| Fusion power P_fus | 250 MW | aip-2023-paper-abstract.md §II, Table I line 156 | high | informational only — `p_fus` is back-solved by library from `p_input` + `P_native`; do NOT put in spec |
| Gross electric power P_gross | 139 MWe | aip-2023-paper-abstract.md §II, Table I line 164 | high | informational |
| Net electric power P_net | 70.4 MWe | aip-2023-paper-abstract.md §II, Table I line 163 (must match P_native from design point block) | high | drives `P_native` spec kwarg |
| External heating power (ECH) | 20 MW (delivered to plasma) | aip-2023-paper-abstract.md §II.D, lines 268-272 — "40 MW of the wall-plug electricity is required to inject 20 MW of ECH power into HESTIA" (60 gyrotrons at 1 MW each, alternately operated, 50% wall-plug efficiency); Table I line 155 P_VCM = 20 MW | high | spec key: `p_input` — auxiliary heating delivered to plasma. The 60 gyrotrons require 40 MW wall-plug electricity at 50% efficiency to deliver 20 MW continuously. |
| Engineering gain Q_eng | 2.0 | aip-2023-paper-abstract.md §II, Table I line 165 | high | informational — library computes Q_eng internally from P_fus / (P_input + other recirculating loads) |
| Plasma gain Q | ~13 | aip-2023-paper-abstract.md §II, lines 102, 362 — "fusion gain of about 13" | high | informational — Q = P_fus / P_external_heating_absorbed |
| Thermal conversion efficiency η_th | >50% (target) | helical-fusion-2025-2026-updates.md §Energy Capture, line 51 — "sCO2 commercial system target >50% efficiency at 800-1200 K" | medium | spec key: `eta_th` — the 50% is aspirational; Oroshhi-2 demo targets 20% |
| Availability / Capacity factor | >80% | aip-2023-paper-abstract.md §I and §III, lines 78, 365 — "target availability of >80%, with ~1 year continuous operation + ~3 month maintenance cycles" | medium | spec key: `availability` — steady-state stellarator advantage; no disruptions |
| Reactor lifetime T_net | 6.4 years | aip-2023-paper-abstract.md §II, Table I line 167 | high | informational — drives total energy production calculation in AIP paper; not a standard 1costingFE input |
| Gyrotron count and power | 60× 250 GHz, 1 MW CW gyrotrons across 10 ports | aip-2023-paper-abstract.md §II.D, lines 262-265 | high | concept-specific ECRH architecture; 60 gyrotrons operated alternately to inject 20 MW ECH continuously; 40 MW wall-plug at 50% gyrotron efficiency |
| Pellet injector count | 10 injectors × 30-barrel pipe-gun = 300 barrels total | aip-2023-paper-abstract.md §II.E, lines 276-294 | high | concept-specific fueling; no cost or power stated |
| Blanket module count | 90 modules, accessible via upper port | aip-2023-paper-abstract.md §II.C, lines 199-202 | high | remote handling architecture |
| Tritium breeding ratio (TBR) | >1.0 (required for self-sufficiency) | aip-2023-paper-abstract.md §II.C, line 226 — liquid metal blanket with lithium for tritium breeding | high | spec key: `tbr` — library default TBR for liquid metal blankets is ~1.05–1.1; HESTIA paper does not state exact TBR but it must be >1.0 for DT steady-state |
| 6Li enrichment | 80 at.% | aip-2023-paper-abstract.md §IV, lines 349-355 | high | informational — impacts blanket cost and tritium breeding performance |
| Confinement enhancement H | 1.3 (optimized) | aip-2023-paper-abstract.md §II.A, line 147 | medium | physics assumption with "almost no experimental backup" per line 207 |
| Center-peaked heating factor γ_CEPI | 1.18 | aip-2023-paper-abstract.md §II.A, lines 197-206 | medium | physics assumption; combined with H gives ~1.5× confinement improvement |
| Alpha particle confinement ε_α | 85% | aip-2023-paper-abstract.md §II.A, line 209 | low | physics assumption; impacts effective Q |
| Cryogenic cooling temperature | 20 K (helium gas) | aip-2023-paper-abstract.md §II.B, lines 214-217 | high | HTS coil cooling; 75% helium reduction vs. 4 K LTS |
| Cryogenic system efficiency | 2% | aip-2023-paper-abstract.md §II.B, line 217 | medium | informational — efficiency of converting electrical power to cooling power |

**Note on p_input and Q_eng**: The AIP paper explicitly states (lines 268-272) that 40 MW wall-plug electricity is required to inject 20 MW of ECH power into HESTIA via 60 gyrotrons operated alternately at 50% wall-plug efficiency. For the `p_input` spec kwarg, we use 40 MW as the auxiliary heating wall-plug power. The Q_eng = 2.0 stated in Table I implies P_recirculating = P_fus / Q_eng = 250 MW / 2.0 = 125 MW total recirculating power, which includes the 40 MW ECH wall-plug plus ~85 MW of other house loads (cryogenic refrigeration, liquid metal circulation pumps, controls, etc.). The library will compute these additional recirculating loads internally based on the plasma physics and engineering systems.

**Note on P_native**: The design point block at the top of this analysis states P_native = 70.4 MWe, matching Table I line 163 from the AIP paper. This is the authoritative value for all model instantiations.

**Note on thermal efficiency**: The sCO2 Brayton cycle target is >50% at 800–1200 K (helical-fusion-2025-2026-updates.md, line 51), but the NIFS Oroshhi-2 demonstration targets 20 kWe at 20% efficiency (line 50). The 2.5× efficiency gap creates significant uncertainty. For baseline modeling, we use η_th = 0.50 (the commercial target stated by Helical Fusion's collaborative research program) but flag this as a sensitivity parameter. If actual η_th = 0.40 (closer to conventional Rankine), P_gross = P_fus × 0.40 = 100 MWe, and P_net = 100 - 125 = -25 MWe (the plant does not reach net electricity). This sensitivity is critical.

**Note on missing parameters**: The AIP paper does not provide plasma density n_e, ion/electron temperatures T_i / T_e, or energy confinement time τ_E. These can be back-calculated from P_fus, plasma volume, and confinement scaling laws, but doing so requires assuming the ISS04 stellarator scaling law plus the H = 1.3 enhancement factor. Since the library's stellarator physics module will perform this calculation internally, we do not forward-propagate inferred n_e or T_e into the spec.

## 5b. Override Candidates

The following candidates emerged from the per-account walkthrough of the canonical 1costingFE schema for this archetype. Six accounts justify potential overrides; all others default to library pricing.

```yaml
overrides:
  - account: C220103
    value: null  # no company-grounded HTS unit cost; WISE conductor pricing is proprietary and undisclosed
    enabled: false
    provenance: N/A
    source: "aip-2023-paper-abstract.md §II.B, helical-fusion-2025-2026-updates.md §HTS Magnets"
    rationale: |
      The AIP paper and company updates describe WISE conductor (REBCO tape + impregnation)
      but provide no unit cost ($/kg, $/kA-m, or $/coil). The October 2025 demonstration
      validates 40 kA at 7 T in a test coil, but scaling to 8 T at plasma center over
      7.8 m major radius with two continuous helical coils yields no cost anchor. The
      library's default HTS coil pricing (derived from CFS ARC REBCO cost assumptions)
      applies to planar wound tokamak coils; 3D helical winding likely carries a
      manufacturing premium, but without a published WISE conductor price, no override
      is justified. Leave this account at library default and flag as a major cost
      uncertainty.

  - account: C220104
    value: null  # no per-gyrotron unit cost published
    enabled: false
    provenance: N/A
    source: "aip-2023-paper-abstract.md §II.D, lines 261-264"
    rationale: |
      HESTIA specifies 60× 250 GHz, 1 MW CW gyrotrons. The AIP paper states "a 250 GHz-1 MW-CW
      gyrotron does not exist" (line 261), indicating this is a development item. No unit cost
      is provided. ITER's 170 GHz, 1 MW gyrotrons are estimated at several million dollars
      each in published ITER cost breakdowns, but scaling to 250 GHz may increase or decrease
      cost depending on production volume and technical maturity. The library default for
      ECRH systems (based on ITER gyrotron costs) is the best available estimate. No override.

  - account: C220101
    value: null  # no blanket unit cost ($/kg LM, $/module) provided
    enabled: false
    provenance: N/A
    source: "aip-2023-paper-abstract.md §II.C, lines 226-236"
    rationale: |
      The AIP paper describes a modular liquid metal blanket (90 modules, tin-indium-lead-lithium
      alloy, 3D-printed porous first wall, high-manganese austenitic steel structure) but
      provides no cost breakdown. The only cost figure in the paper is the lump-sum direct
      construction cost of USD 5 billion (1990s basis, lines 116-122), which is not decomposed
      by account. The blanket's integration of first wall + breeding + shielding functions
      "eliminates the need for separate divertor systems" (line 234), suggesting cost savings
      relative to tokamak blanket + divertor, but this is qualitative. Without a published
      $/module or $/kg LM figure, no override is justified. The library's default liquid metal
      blanket cost (derived from ARIES-AT FLiBe blanket estimates) is the best proxy.

  - account: C220108
    value: 0.0
    enabled: true
    provenance: direct
    source: "aip-2023-paper-abstract.md §II.C, lines 81-84, 234-236"
    rationale: |
      "Individual divertor systems are not required in HESTIA. By skipping the development
      of individual divertor systems, NBI, and ICH, which are widely recognized as the most
      difficult issues in fusion reactor development, a fast-track plan is possible."
      The liquid metal free-surface first wall serves the divertor function by flowing over
      the plasma-facing surfaces and absorbing heat/particle fluxes. No separate tungsten
      monoblock divertor cassettes are installed. C220108 (divertor) cost = 0. The divertor
      functionality is embedded in C220101 (blanket).

  - account: CAS23
    value: null  # sCO2 turbine cost not stated; use library thermal-cycle default
    enabled: false
    provenance: N/A
    source: "helical-fusion-2025-2026-updates.md §Energy Capture, lines 46-51"
    rationale: |
      The design uses a supercritical CO2 Brayton cycle targeting >50% efficiency at
      800-1200 K. The library's CAS23 (turbine plant equipment) account prices thermal
      cycles generically; sCO2 is higher efficiency than Rankine but costs are comparable
      at scale (both are turbomachinery + heat exchangers + condensers/coolers). Without
      a HESTIA-specific sCO2 turbine cost estimate, the library default for thermal
      conversion applies. The efficiency delta (50% vs. ~33% Rankine) is captured in the
      `eta_th` spec kwarg, not in CAS23 cost.

  - account: CAS27
    value: null  # liquid metal inventory cost not stated
    enabled: false
    provenance: N/A
    source: "aip-2023-paper-abstract.md §II.C, lines 226-228"
    rationale: |
      The blanket uses tin-indium alloy + lead + lithium. Tin (~$20-30/kg), indium
      (~$200-500/kg), lead (~$2/kg), lithium (~$80-100/kg for battery-grade, higher for
      nuclear isotope-enriched). The AIP paper does not state total blanket inventory mass.
      For a liquid-metal-cooled reactor, typical inventory is 100-1000 tonnes depending on
      flow rate and geometry. If we assume 500 t and a 50/25/15/10 mass split
      (Sn/Pb/In/Li), rough cost = (250 t Sn × $25/kg) + (125 t Pb × $2/kg) + (75 t In × $300/kg)
      + (50 t Li × $100/kg) ≈ $6.25M + $0.25M + $22.5M + $5M = $34M. However, this is
      speculative (the alloy composition is stated as "tin-indium alloy with lead and lithium"
      with no percentages, and total mass is not given). The library's CAS27 default for
      initial blanket inventory is based on FLiBe or LiPb; those costs are comparable to
      the above rough estimate. Without a company-grounded figure, no override is justified.
```

**Override count: 1 enabled override** (C220108 = 0 for integrated blanket/divertor). The archetype-fit rubric expects 0–4 enabled overrides for a High archetype-fit concept. The count of 1 falls within the expected band. The single override is well-grounded (the AIP paper explicitly states no separate divertor system) and has direct provenance.

**Key cost uncertainties not overridden**: The two largest capital cost drivers — C220103 (HTS magnets) and C220101 (blanket) — lack company-grounded unit costs and therefore remain at library defaults. The library's HTS coil pricing is derived from CFS ARC assumptions (REBCO tape at $40–50/kA-m, planar winding); HESTIA's continuous helical winding is architecturally different and likely more expensive per meter due to 3D complexity, but without a WISE conductor price quote, no defensible override exists. Similarly, the liquid metal blanket cost depends on module fabrication (3D-printed porous first wall, high-manganese steel structure, liquid metal inventory) and corrosion-protection engineering, but no $/module figure is published. The AIP paper's lump-sum $5 billion (1990s) direct cost provides no per-account resolution.

**Why C220104 (ECRH) is not overridden despite 250 GHz novelty**: The 250 GHz gyrotrons are in R&D and do not exist as of the AIP paper's writing ("a 250 GHz-1 MW-CW gyrotron does not exist," line 261). Without a prototype cost or vendor quote, any cost estimate would be speculative. The library's ECRH pricing is based on ITER 170 GHz gyrotron costs (~$2–3M per gyrotron); scaling to 250 GHz may add 20–50% development premium, or may decrease cost if production volume rises. The uncertainty range is too wide and the data too thin to justify a derived override. Default library pricing stands.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | WISE HTS conductor unit cost ($/kA-m or $/kg) for continuous helical winding at 8 T, 20 K | S2, S5b | proprietary | blocking | Helical Fusion investor deck or vendor partnership announcement; alternatively, analogous quotes from CFS or Tokamak Energy for non-planar REBCO coils |
| 2 | Liquid metal blanket module fabrication cost ($/module or $/kg) including 3D-printed porous first wall, high-manganese steel structure, and corrosion protection | S2, S5b | not-yet-sourced | blocking | NIFS Oroshhi-2 blanket test campaign results; FFHR-d1 / FFHR-c1 blanket cost estimates (heritage designs); or Helical Fusion detailed engineering report |
| 3 | Liquid metal circulation pump power consumption at reactor scale (MW wall-plug per pump, number of pumps) | S2 | truly-unknown | important | GALOP test results extrapolated to full scale; or computational fluid dynamics simulation validated against test data |
| 4 | 250 GHz, 1 MW CW gyrotron unit cost and development timeline | S2, S5b | not-yet-sourced | important | Joint research program between Helical Fusion and QST; or analogous cost data from ITER 170 GHz gyrotron procurement adjusted for frequency scaling |
| 5 | Confinement enhancement factor H experimental validation in optimized heliotron configuration | S2, S3, S5 | truly-unknown | blocking | HESTIA-Primary prototype experimental results (USD 480M prototype, per AIP paper line 318); or scaled LHD experiments with magnetic field optimization |
| 6 | Supercritical CO2 turbine cost and efficiency at fusion-relevant scale (MW-to-GW thermal input, tritium-compatible heat exchangers) | S2, S5 | not-yet-sourced | important | NIFS Oroshhi-2 sCO2 demonstration results scaled to commercial plant; or DOE-funded sCO2 pilot projects (Sandia National Labs, Southwest Research Institute); or fission-focused sCO2 vendors (Echogen, Kairos Power) |
| 7 | Blanket module replacement time and remote handling equipment cost | S2, S3 | truly-unknown | important | ITER remote handling mock-up results adapted to stellarator geometry; or time-motion simulation for liquid-metal-wetted module handling |
| 8 | CAS-level cost breakdown of the USD 5 billion direct construction cost (late-1990s basis) | S1, S5b | proprietary | blocking | HESTIA detailed engineering report or Helical Fusion Series A pitch deck; or FFHR cost studies as a heliotron heritage proxy |
| 9 | Inflation adjustment methodology and reference year for USD 5 billion figure | S1, S2 | derivable | important | Apply U.S. CPI-U or construction cost index (e.g., Handy-Whitman) from late 1990s to 2025; AIP paper suggests 2× multiplier but does not specify the index or base year |
| 10 | Tritium breeding ratio (TBR) for tin-indium-lead-lithium blanket at 80 at.% 6Li enrichment | S5 | not-yet-sourced | blocking | Neutronics simulation results from HESTIA design (likely in full AIP paper behind paywall); or FFHR blanket TBR calculations as a lithium-bearing liquid metal proxy |
| 11 | Tin-lead-lithium alloy composition (mass percentages) and total blanket inventory mass | S4, S5b | not-yet-sourced | important | Full AIP Physics of Plasmas paper (not just abstract); or GALOP test campaign material specifications |
| 12 | High-manganese austenitic steel unit cost ($/kg) and production capacity at nuclear-grade quality | S4 | not-yet-sourced | important | Tohoku University materials collaboration publication; or advanced fission reactor vendors (sodium-cooled fast reactors use austenitic steel) |
| 13 | DD startup operational timeline and tritium breeding rate via DD → T side reactions | S3, S5 | truly-unknown | important | Plasma physics simulation of DD operation in heliotron geometry; or analogy to tokamak DD experiments (but stellarator confinement scaling differs) |
| 14 | Enriched 6Li supply chain capacity and cost at 80 at.% (kg/year global production, $/kg) | S4 | not-yet-sourced | important | U.S. DOE or IAEA isotope program reports; or China National Nuclear Corporation / Rosatom disclosures (they control most 6Li enrichment capacity) |
| 15 | Final optics and beamline configuration for 60 gyrotrons across 10 ports (number of beamlines, window materials, neutron shielding for transmission lines) | S3, S5 | not-yet-sourced | nice-to-have | HESTIA engineering drawings (proprietary); or W7-X / LHD ECRH beamline designs as heritage (but those use 140–170 GHz, not 250 GHz) |
| 16 | Pellet injector cost and fueling efficiency ($/injector, fueling rate per barrel, DT ice production capacity) | S5 | not-yet-sourced | nice-to-have | ITER pellet injector procurement cost as analogue; or direct quote from pellet injector vendors (PELIN in Russia, ORNL in U.S.) |
| 17 | Cryogenic system capital cost and operating power for 20 K helium gas cooling of multi-km HTS coils under neutron heating | S3, S5 | not-yet-sourced | important | CFS SPARC cryogenic system design (similar HTS cooling requirements); or large-scale helium refrigerator vendors (Linde, Air Liquide) for 20 K capacity quotes |
| 18 | Vacuum vessel mass, structural analysis, and cost for heliotron geometry at 7.8 m major radius | S3, S5b | not-yet-sourced | nice-to-have | LHD vacuum vessel as-built cost inflated to current year; or ITER vessel cost adjusted for size and geometry differences |
| 19 | Operating & maintenance cost breakdown (staffing, scheduled maintenance frequency, unplanned outage costs) | S1 | not-yet-sourced | blocking | ARIES-CS stellarator O&M model (closest publicly-available analogue); or ITER operational plan extrapolated to smaller steady-state plant |
| 20 | Component replacement schedule and costs beyond 6.4-year reactor lifetime (blanket module lifetime under neutron fluence, gyrotron lifetime, first wall lifetime) | S1, S3 | truly-unknown | blocking | Neutron damage simulations for high-manganese steel under 14.1 MeV fluence; gyrotron vendor MTBF data; or ITER component lifetime projections |

**Criticality definitions**: **Blocking** — LCOE model cannot produce a defensible estimate without this data; **Important** — model can proceed with analogues or conservative assumptions, but uncertainty is large; **Nice-to-have** — fills out the picture but does not drive LCOE sensitivity.

**Gap type definitions**: **Truly-unknown** — no existing data or validated model can answer this; requires prototype testing or new experimental campaign. **Proprietary** — company or consortium likely has the data but has not released it publicly. **Not-yet-sourced** — data likely exists in published literature (conference papers, vendor quotes, heritage reactor studies) but has not been located in the current dossier. **Derivable** — can be computed from available data using standard engineering methods (e.g., inflation adjustment, scaling laws).

## 7. Family-Delta vs Comparables

The fixed comparables for HESTIA are: 05-planar-coil-stellarator (Thea Energy), 09-qi-stellarator-hts (Proxima Fusion), 10-large-scale-stellarator (Gauss Fusion), 20a-type-one-stellarator (Type One Energy), and 20b-renaissance-stellarator (Renaissance Fusion). All are stellarators within the MFE family, enabling direct subsystem-level cost comparison.

### vs. 05 Planar-Coil Stellarator (Thea Energy)

**Divergence: Coil geometry and winding complexity**

Thea Energy's planar-coil stellarator uses an array of simple flat HTS coils arranged in a toroidal configuration, with field shaping achieved by current distribution rather than coil geometry. HESTIA uses two continuous helical HTS coils that wind through a complex 3D path (double-helix configuration) at 7.8 m major radius. The planar-coil approach trades physics optimization (less confinement quality per unit field strength) for manufacturing simplicity (each coil is a flat pancake, easy to wind and stack). The helical-coil approach achieves better plasma confinement (heliotron physics is well-validated by LHD) but requires flexible REBCO conductor (WISE technology) and specialized winding machinery.

**Cost implication**: HESTIA's C220103 (HTS magnets) likely carries a **manufacturing premium** per meter of conductor due to 3D winding complexity, but may require **less total conductor length** if the heliotron's superior confinement permits smaller major radius for the same plasma performance. The net cost effect is ambiguous without per-meter WISE conductor pricing vs. Thea's planar coil costs. Thea's approach is likely cheaper per coil but may require more coils or larger machine size.

**Divergence: Blanket and divertor architecture**

Thea Energy has not publicly specified a blanket design. HESTIA uses an integrated liquid metal blanket with free-surface first wall, eliminating the need for a separate divertor system. If Thea adopts a conventional solid breeder blanket + divertor (ITER TBM heritage), HESTIA gains a **cost advantage** by eliminating C220108 (divertor) entirely (override in Section 5b sets this to zero). However, HESTIA's liquid metal system introduces corrosion management and MHD flow control challenges that may offset the divertor savings via higher C220101 (blanket) complexity.

**Net cost delta**: Likely **neutral to slight advantage for HESTIA** if liquid metal blanket proves durable; **penalty** if corrosion or flow control requires frequent module replacement.

### vs. 09 QI-Stellarator-HTS (Proxima Fusion) and 10 Large-Scale Stellarator (Gauss Fusion)

**Divergence: Modular vs. continuous coil design**

Proxima Fusion (QI stellarator, W7-X lineage) and Gauss Fusion (large-scale stellarator) use modular non-planar HTS coils — each coil is a complex 3D shape, but coils are manufactured individually and assembled into a torus. HESTIA uses **two continuous helical coils** that wrap the entire torus without joints. Modular coils enable parallel manufacturing and easier replacement (remove and replace a single failed coil), but each coil has high-resistance joints where modules connect. Continuous coils eliminate joints (lower resistance, fewer failure points) but cannot be disassembled — the entire coil is a single monolithic structure.

**Cost implication**: Modular coils spread manufacturing risk (if one coil fails QA, scrap only that module, not the entire set) and enable factory production at scale. Continuous coils concentrate risk (a defect anywhere along a multi-hundred-meter winding scraps the entire coil) and require on-site or large-facility winding. HESTIA's approach with Sugino Machine's custom winding machine (to be transported to the demonstration site, per helical-fusion-2025-2026-updates.md line 15) suggests on-site fabrication, which may reduce transport risk but increases site construction complexity. The cost delta depends on REBCO tape yield and winding QA — if yield is high, continuous coils save on joints and assembly labor; if yield is low, modular coils reduce scrap cost.

**Net cost delta**: **Ambiguous**. HESTIA's continuous-coil approach is novel and has no cost precedent; Proxima/Gauss benefit from W7-X and Helias heritage for modular coil cost estimation.

**Divergence: Physics optimization vs. engineering simplicity**

The QI (quasi-isodynamic) stellarator (Proxima) and Helias (Gauss) are optimized for low neoclassical transport and good fast-ion confinement, requiring precise 3D coil shaping. The heliotron (HESTIA) is optimized for manufacturing simplicity via continuous helical coils, accepting somewhat higher neoclassical transport. The AIP paper states that HESTIA's confinement depends on assumed H = 1.3 enhancement over baseline heliotron scaling, whereas QI stellarators target H ~ 1.0 with intrinsically better transport. If HESTIA's confinement enhancement does not materialize, the plasma must run at higher density or field strength to achieve the same fusion power, increasing cost. If it does materialize, HESTIA matches QI performance with simpler coils.

**Net cost delta**: **Conditional**. If HESTIA-Primary prototype validates H = 1.3, HESTIA gains a **cost advantage** via simpler coil manufacturing. If H = 1.0 (baseline heliotron), HESTIA requires larger machine or higher field to match Proxima/Gauss performance, erasing the coil simplicity advantage.

### vs. 20a Type One Stellarator and 20b Renaissance Stellarator

**Divergence: Manufacturing approach**

Type One Energy (20a) uses a planar-coil variant with emphasis on modular assembly and supply chain localization (U.S. manufacturing). Renaissance Fusion (20b) uses laser-patterned HTS film on cylindrical substrates (a radically different coil fabrication method: deposit REBCO film via PVD, then laser-etch current paths to create 3D field patterns). HESTIA uses stacked REBCO tape + impregnation (WISE). Each approach targets cost reduction via different manufacturing innovations: Type One via modularity, Renaissance via additive/subtractive film patterning, HESTIA via continuous winding + impregnation.

**Cost implication**: Renaissance's laser-patterned film approach, if successful, could achieve very low $/kA-m by eliminating tape winding labor and enabling large-area deposition, but it is unproven at high field and carries thin-film delamination risk. Type One's modular planar coils benefit from supply chain maturity (planar coils are simpler to manufacture than 3D shapes). HESTIA's WISE conductor is intermediate complexity — more complex than planar, simpler than fully-3D modular coils, but relies on low-melting-point alloy impregnation (a novel step with uncertain cost and yield).

**Net cost delta**: **Ambiguous**. All three concepts are betting on different HTS manufacturing cost curves. HESTIA's WISE approach is furthest along in hardware demonstration (40 kA test coil in Oct 2025), but Type One and Renaissance have raised more capital and may achieve faster scale-up.

**Divergence: Blanket architecture**

Renaissance Fusion uses a flowing Li-LiH wall + lead pebble neutron multiplier — a hybrid solid/liquid architecture (flagged as `Other/hybrid` in the schema). HESTIA uses a pure liquid metal blanket (tin-indium-lead-lithium free-surface flow). Type One has not publicly specified a blanket design. Renaissance's hybrid approach aims to combine liquid metal's first-wall simplicity with solid breeder's TBR margin, but introduces two-phase flow complexity. HESTIA's single-phase liquid metal flow is simpler fluidically but carries higher corrosion risk (tin is "highly corrosive to steel," per AIP paper).

**Net cost delta**: **Slight advantage to HESTIA** if single-phase liquid metal proves manageable; **penalty** if corrosion forces frequent blanket replacement. Renaissance's dual-phase system is architecturally more complex but may achieve higher TBR (lead pebbles boost neutron multiplication).

### Shared advantages across all stellarator comparables

All stellarator concepts, including HESTIA, share the following cost advantages relative to tokamaks:

1. **No disruption risk** — stellarators have no plasma current, therefore no current-driven MHD instabilities or disruptions. This eliminates disruption mitigation systems (massive gas injection, vertical stability control, runaway electron suppression) and reduces structural design margins (no need to design for 10–100 MA disruption electromagnetic loads). Cost savings in C220105 (primary structure) and C220110 (remote handling — fewer unplanned failures).

2. **True steady-state operation** — no current drive power required (tokamaks need NBI, ECRH, or LHCD to sustain plasma current in steady-state; stellarators are intrinsically steady-state). HESTIA's claimed ~1 year continuous operation is physically plausible (stellarators are limited only by tritium inventory and maintenance needs, not by physics). Higher capacity factor (>80% target) vs. pulsed or quasi-steady tokamaks improves LCOE denominator.

3. **No central solenoid** — tokamaks (except spherical tokamaks with external current drive) require a central solenoid for inductive startup and current ramp. Stellarators have no solenoid, freeing the central bore and reducing C220103 (magnets) and C220105 (structure). This advantage is shared with spherical tokamaks and mirrors.

### Shared challenges across all stellarator comparables

1. **3D coil complexity and cost** — all stellarators (except planar-coil variants, which trade physics performance for simplicity) require complex 3D coil shapes, whether modular (Proxima, Gauss), continuous helical (HESTIA), or laser-patterned film (Renaissance). This increases C220103 (magnet) cost relative to tokamaks' simple toroidal + poloidal coil sets. The magnitude of the premium depends on the manufacturing approach; no consensus cost basis exists yet.

2. **Lower power density than compact tokamaks** — stellarators are generally larger than high-field compact tokamaks for the same fusion power, due to lower beta limits and more conservative field strength (W7-X operates at ~3 T; HESTIA targets 9 T, which is high for a stellarator but still below the 12–20 T of compact tokamaks). Larger size increases C220105 (structure), C220106 (vacuum), CAS21 (buildings), and site footprint. HESTIA's 8 m major radius for 70.4 MWe net is large compared to CFS SPARC's ~1.85 m major radius for ~140 MWe (though SPARC is a technology demonstrator, not optimized for economy).

3. **Unvalidated high-performance scenarios** — all advanced stellarator concepts (QI, Helias, heliotron-optimized) assume confinement and stability performance beyond current experimental validation. W7-X is the only modern superconducting stellarator, and it operates at low density and low beta relative to power-plant targets. HESTIA's H = 1.3 assumption is in the same category as Proxima's QI transport optimization or Gauss's Helias stability claims — all require prototype validation before commercial deployment.

## 8. Sources

Listed in order of importance for LCOE modeling:

1. **Miyazawa, J. and Goto, T. (2023)** "Design of a heliotron-type DEMO reactor HESTIA." *Physics of Plasmas* 30, 050601. DOI: 10.1063/5.0146228. Abstract available at https://ui.adsabs.harvard.edu/abs/2023PhPl...30e0601M/abstract. **Contribution**: Complete reactor design specification for HESTIA — geometry, physics parameters, subsystem architecture (HTS magnets, liquid metal blanket, ECRH heating, pellet fueling, sCO2 power conversion), direct construction cost estimate (USD 5 billion, late-1990s basis), and reactor lifetime energy production. This is the primary quantitative anchor for the analysis. The full text (behind paywall) likely contains additional CAS-level cost breakdowns, blanket neutronics (TBR), and engineering drawings not visible in the abstract. **Source**: knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/aip-2023-paper-abstract.md (extracted abstract, 58 KB).

2. **Helical Fusion Technology Overview** (company website summary, 2025). Overview of HESTIA design basis, HTS coil development, liquid metal blanket approach, ECRH heating strategy, and energy conversion pathway. Confirms 50 MWe-class power target, Q ~ 13, >80% availability, and modular liquid metal blanket with no separate divertor. **Contribution**: Design philosophy and technology pillars — useful for understanding cost-reduction strategy (integrated blanket/divertor, continuous helical coils, DD startup to avoid tritium procurement). **Source**: knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/helical-fusion-technology-overview.md (3 KB).

3. **ANS Nuclear Newswire (2025-10-29)** "Helical Fusion marks milestone in progress toward fusion power." Report on the October 2025 HTS coil demonstration: 40 kA at 7 T external field, 15 K, using 30-layer REBCO uninsulated design in a >4 m coil. Described as "world's first demonstration of large-scale HTS coil designed for commercial reactor." **Contribution**: Hardware validation of WISE conductor approach at subscale; confirms HTS coil development timeline. **Source**: Cited in dossier; URL: https://www.ans.org/news/2025-10-29/article-7500/helical-fusion-marks-milestone-in-progress-toward-fusion-power/ (not directly extracted but summarized in helical-fusion-2025-2026-updates.md).

4. **BusinessWire (2025-10-26)** Helical Fusion press release on HTS coil milestone. Confirms Helix HARUKA integrated demonstration device assembly beginning 2026, with custom coil manufacturing machine developed with Sugino Machine. **Contribution**: Manufacturing timeline and partnership details (Sugino Machine for winding equipment, Sukegawa Electric for GALOP pump system). **Source**: https://www.businesswire.com/news/home/20251026597002/en/ (cited in dossier).

5. **Helical Fusion 2025-2026 Updates** (aggregated press releases and company announcements). Covers Series A extension ($5.5M, Dec 2025), GALOP liquid metal blanket test system unveiling, Tohoku University materials collaboration (high-manganese austenitic steel), Sugino Machine coil winding machine completion, and roadmap to Helix KANATA pilot plant. **Contribution**: Near-term milestones and partnerships; confirms sCO2 power conversion as baseline (listed among collaborative research areas). **Source**: knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/helical-fusion-2025-2026-updates.md (2 KB).

6. **NIFS FFHR Blanket Heritage** (summary of FFHR design evolution and Oroshhi-2 test platform). Describes the shift from FFHR's FLiBe molten salt blanket to HESTIA's liquid metal blanket, and the Oroshhi-2 platform's LiPb twin-loop system and planned sCO2 turbine demonstration (20 kWe at 20% efficiency). **Contribution**: Heritage context for blanket technology and sCO2 power conversion; explains why HESTIA diverged from FFHR (liquid metal vs. molten salt). **Source**: knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/nifs-ffhr-blanket-heritage.md (2 KB).

7. **Ishiyama, S. and Tanaka, T. (2019)** "Demonstration Plan of Nuclear Fusion Power Generation by CO2 Gas Turbine in Oroshhi-2." *Fusion Science and Technology* 75:8. DOI: 10.1080/15361055.2019.1610315. Describes NIFS Oroshhi-2 test platform's sCO2 Brayton cycle demonstration plan targeting >50% efficiency at 800-1200 K for commercial systems, with a 20 kWe / 20% efficiency proof-of-concept. **Contribution**: sCO2 power conversion efficiency targets and test platform infrastructure supporting Helical Fusion's claimed >50% η_th. **Source**: https://www.semanticscholar.org/paper/Demonstration-Plan-of-Nuclear-Fusion-Power-by-CO2-Ishiyama-Tanaka/c65a8bee89527829427288e4fe2a278409abad6e (cited in dossier).

8. **Tanaka, T. and Sagara, A.** "Liquid Blanket Collaboration Platform Oroshhi-2 at NIFS." Describes the FLiNaK/LiPb twin-loop system at Oroshhi-2 (operational since 2013-2014) for liquid blanket R&D. **Contribution**: Test infrastructure heritage for liquid metal handling; supports HESTIA's liquid metal blanket feasibility claim. **Source**: https://www.semanticscholar.org/paper/Liquid-Blanket-Collaboration-Platform-Oroshhi-2-at-Tanaka-Sagara/6aa3a1a42420da041a9d98e1bb46169e57112b79 (cited in dossier).

9. **Helical Fusion — Tohoku University Materials Collaboration** (company announcement, 2024). High-manganese alumina-formed austenitic steel with silicon addition developed for blanket structural material: non-magnetic, low-activation, corrosion-resistant at high temperatures. **Contribution**: Material selection for liquid metal blanket structure; addresses corrosion challenge flagged in AIP paper. **Source**: https://www.helicalfusion.com/en/post/helical-fusion-inc-and-tohoku-university-s-institute-for-materials-research-pioneer-revolutionary-m (cited in dossier).

10. **ARIES-CS Stellarator Power Plant Study** (Fusion Science and Technology, 2008). Comprehensive stellarator power plant design study (QI stellarator, ~1 GWe) with CAS-level cost breakdowns, O&M estimates, and stellarator-specific engineering challenges. **Contribution**: Nearest publicly-available analogue for stellarator LCOE modeling; provides default unit costs for accounts where HESTIA data is absent (C220101 blanket, C220103 magnets if WISE conductor cost remains proprietary, CAS70 O&M). The ARIES-CS design uses modular coils + helium-cooled pebble bed blanket, so direct cost transfer to HESTIA (continuous coils + liquid metal blanket) is imperfect, but it is the best available stellarator reference. **Source**: Not in current dossier; available at https://www.sciencedirect.com/science/article/pii/S092037960800085X or via ARIES project bibliography https://qedfusion.org/DOCS/bib.shtml.

11. **LHD (Large Helical Device) experimental database** (NIFS publications, 1998–present). 25+ years of heliotron physics data: confinement scaling, beta limits, steady-state operation demonstrations, ECRH heating efficiency. **Contribution**: Physics validation for heliotron configuration; provides baseline for HESTIA's H = 1.3 enhancement assumption (LHD operates near H ~ 1.0). **Source**: Diffuse — no single publication, but referenced in AIP paper as heritage. Representative papers available via NIFS publication database or LHD project overview at https://www-lhd.nifs.ac.jp/en/.

12. **ITER cost and schedule data** (ITER Organization annual reports). Not directly applicable to HESTIA (ITER is a tokamak, not a stellarator, and is FOAK not NOAK), but provides order-of-magnitude unit costs for gyrotrons (170 GHz, ~$2–3M each), remote handling equipment, and vacuum vessel fabrication that can be scaled to HESTIA's requirements in the absence of concept-specific data. **Contribution**: Fallback cost analogues for C220104 (ECRH), C220110 (remote handling), C220106 (vacuum vessel). **Source**: https://www.iter.org/sites/default/files/media/2025-11/rapport-financier-iter-2024-web.pdf (cited in 01-hts-compact-tokamak handwritten exemplar).

**Note on source quality**: The single authoritative design study (AIP 2023 paper) provides geometry and physics but lacks CAS-level cost transparency and inflation adjustment. Company announcements confirm technology development progress (HTS coil demo, GALOP test system, materials R&D) but provide no cost data. ARIES-CS is the best publicly-available stellarator cost reference, but its architecture (modular QI coils + solid breeder blanket) differs significantly from HESTIA's (continuous helical coils + liquid metal blanket). The resulting cost model will be highly uncertain in absolute dollars, though the relative cost structure (magnets + blanket dominate CAPEX, capacity factor drives LCOE) is defensible.