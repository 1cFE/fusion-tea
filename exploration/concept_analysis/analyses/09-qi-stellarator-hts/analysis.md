---
ID: 09-qi-stellarator-hts
Concept: QI Stellarator - HTS
Company: Proxima Fusion
Status: draft
Created: 2026-03-28
Approved-Date:
Reuses: [01-hts-compact-tokamak]
---

# D1+ Analysis: QI Stellarator - HTS (Proxima Fusion)

**Concept**: Quasi-isodynamic (QI) stellarator with HTS magnets — D-T fuel
**Company**: Proxima Fusion (Munich, Germany; spin-off from Max Planck IPP)
**Commercial Plant**: Stellaris (published in *Fusion Engineering and Design*, Vol. 214, May 2025)
**Demo Device**: Alpha (~EUR 2B, Q>1, ~2031, Garching)
**Confinement Family**: MFE — Stellarator (QI)

---

## Section 1: Availability of Data

**Rating: Moderate**

Proxima Fusion has published more detailed technical information than most private fusion companies at equivalent maturity — most notably the peer-reviewed Stellaris power plant concept paper in *Fusion Engineering and Design* (2025, DOI: 10.1016/j.fusengdes.2025.114868). However, the Stellaris paper is paywalled on ScienceDirect, and the publicly accessible abstract and associated press materials disclose only a partial parameter set: peak fusion power (2.7 GW), thermal power (~3.1 GW), net electrical output (~1 GW), blanket TBR (1.07), and structural material choices. Key LCOE-relevant parameters — Q value, heating power, detailed thermal efficiency, and capital cost — do not appear in any publicly available source.

**Peer-reviewed publications and plant studies:**
The Stellaris paper is a full power plant concept study covering first wall cooling, divertor considerations, WCLL blanket design (TBR 1.07), magnet quench safety, support structures, remote maintenance solutions, and trade-offs between physics and engineering constraints [stellaris-paper-details.md §Paper Scope]. This is a meaningful disclosure — Proxima has done more than most private companies in publishing a reactor study before demonstrating Q>1. The physics basis rests on Wendelstein 7-X (W7-X) results from Max Planck IPP, which Proxima founders helped develop. W7-X has achieved the highest triple-product for any stellarator and 8-minute plasma duration, validating the QI optimization approach and island divertor concept:

> "QI optimization approach validated, island divertor concept proven at W7-X and W7-AS"
> — proxima-fusion-2026-updates.md, §W7-X Heritage

**Comparison benchmarks:**
The Helios stellarator design (Thea Energy, arXiv:2512.08027v1) is an independently published QI stellarator power plant study using a similar approach — QI optimization, ECRH heating, PbLi blanket, steady-state operation. It provides detailed parameters that serve as direct analogues where Proxima has not published specifics [helios-stellarator-comparison.md]. Brown (2018, *IEEE Transactions on Plasma Science*, DOI: 10.1109/TPS.2018.2831148) provides a comparative cost decomposition across spherical tokamak, standard tokamak, and stellarator geometries — the only published multi-concept cost comparison that includes stellarators, and a structural reference for the CAPEX premium discussion in Section 2.

**Company transparency:**
Proxima publishes substantially more than comparable early-stage companies: the Stellaris plant study, subsystem disclosures (WCLL blanket, HTS magnets, island divertor), supplier agreements (Faraday Factory Japan for REBCO tape), and institutional partnerships [dossier.md §Key Sources]. The February 2026 MoU with RWE, the Free State of Bavaria, and Max Planck IPP provides a credible governance and funding structure for the Alpha → Stellaris roadmap [proxima-fusion-2026-updates.md §RWE/Bavaria/IPP MoU]:

> "Proxima Fusion, RWE, the Free State of Bavaria and Max Planck Institute for Plasma Physics sign agreement to build the world's first commercial fusion power plant in Europe"
> — proxima-fusion-2026-updates.md, §Headline

Key proprietary items include: full Stellaris parameter set (in the paywalled paper), the innovative liquid-metal breeding blanket patent, and specific coil geometry details [stellaris-design-details.md §Blanket Note].

**Phase 1a dossier completeness:**
The Phase 1a dossier achieved high confidence on 8 of 12 columns after two research iterations. Four medium-confidence values remain: primary heating (ECRH strongly inferred but not confirmed), energy capture (steam Rankine strongly inferred from WCLL + EUROFER97 constraints), plasma state (burning inferred from 2.7 GW fusion target), and neutron management (integrated blanket/shield inferred). Iter-02 conducted 13 targeted queries without resolving these; they are confirmed as not in public sources [dossier.md §Remaining Gaps].

**Key data gaps limiting this analysis:**
1. Full Stellaris paper parameters: Q value, heating power, thermal efficiency, capital cost breakdown — paywalled
2. Machine geometry (dimensions, plasma volume) — required for conductor demand and structural cost estimation
3. No published NOAK cost estimate for Stellaris or any modern HTS QI stellarator
4. No capacity factor target or maintenance schedule
5. Final blanket technology: WCLL demonstrated as viable, but Proxima holds a patent for an "innovative liquid-metal breeding blanket" suggesting WCLL may not be the final choice [stellaris-design-details.md §Blanket Note]

---

## Section 2: Challenges in Capturing System Function

The QI stellarator presents LCOE modeling challenges that diverge substantially from the HTS compact tokamak. The steady-state D-T thermal physics fits conventional power plant cost structures, and the disruption-free operation simplifies some structural design questions. But the dominant cost driver — 3D HTS coil manufacturing — has no commercial precedent. Ranked by LCOE impact:

**1. 3D HTS stellarator coil manufacturing cost — dominant unknown CAPEX driver**

Stellarator coils are geometrically complex 3D non-planar structures. Unlike tokamak D-shaped coils (wound on a 2D mandrel), stellarator coils require precision winding of REBCO tape through compound curves with tight tolerances on field-shaping accuracy. Wendelstein 7-X used 50 non-planar and 10 planar LTS (NbTi) coils — the non-planar coils alone accounted for a large fraction of the device's ~EUR 1B total cost and took approximately 8 years to manufacture [analogue from W7-X heritage, cited in proxima-fusion-technology-page.md §Key Details].

Proxima has explicitly identified 3D HTS coil manufacturing as a critical risk, scheduling a Stellarator Model Coil (SMC) demo for 2027 specifically to de-risk this step:

> "2027: Stellarator Model Coil (SMC) demo magnet — de-risk HTS coil manufacturing"
> — proxima-fusion-2026-updates.md, §Development Milestones

The 2027 SMC demo is still future work: no HTS non-planar stellarator coil of any scale has been completed. Brown (2018) estimated that stellarator coil costs exceeded comparable tokamak coil costs by 15–30% even with conventional LTS technology; the premium for 3D REBCO HTS winding is entirely unknown. The uncertainty range on coil CAPEX is wider for the QI stellarator than for any other MFE concept with a published plant study.

**2. Machine scale and beta: power density vs. CAPEX**

The Stellaris design targets 2.7 GW peak fusion power and ~1 GW net electrical [stellaris-paper-details.md §Key Parameters]. The volume-averaged plasma beta is ~2.76% [stellaris-paper-details.md §Key Parameters]. Stellarators typically operate at lower beta than optimized tokamaks — low beta means more magnetic field energy per unit plasma pressure, driving up the machine's stored energy and physical size. A larger machine with expensive 3D coils is a double penalty: higher CAPEX per coil and more coils. LCOE scales with capital cost per kWe, and without published machine dimensions, the implied physical scale must be estimated from the Helios analogue or W7-X scaling.

The net electrical-to-fusion power ratio (~37%: 1 GW / 2.7 GW) is lower than the Helios analogue (~41%: 390 MW / 958 MW), suggesting Stellaris has larger recirculating loads — consistent with a larger machine requiring more heating and auxiliary power at startup.

**3. WCLL blanket geometry compatibility — stellarator-specific challenge**

The WCLL blanket is a well-developed EUROfusion/DEMO technology, but it must be adapted to the complex non-axisymmetric geometry of a QI stellarator. Fitting modular blanket segments around 3D coil geometry produces more geometric dead zones where tritium breeding coverage is reduced compared to the tokamak case. Proxima's TBR of 1.07 is adequate but provides thin margin — 7% above self-sufficiency before engineering losses and simulation uncertainties [dossier.md §Tritium Breeding]:

> "Proxima notes this is a 'concept, not a complete engineering design' demonstrated as viable 'without suggesting this is the optimal choice.'"
> — stellaris-design-details.md, §Blanket

For comparison, the Helios analogue reports TBR 1.1 practical (idealized 1.3), with the gap between idealized and practical representing exactly these geometric and engineering losses [helios-stellarator-comparison.md §Blanket].

**4. ECRH recirculating power and gyrotron cost**

ECRH heating via gyrotrons is the universal stellarator heating method [dossier.md §Primary Heating]. Gyrotron wall-plug efficiency is ~50–60% at the device level. The Helios QI stellarator analogue uses ECRH at 170 GHz (ITER-spec gyrotrons), requiring 10 MW for startup and only ~1 MW once ignited:

> "Heating system: ECRH at 170 GHz using ITER-spec gyrotrons; requires 10 MW for startup, 1 MW in ignited phase"
> — helios-stellarator-comparison.md, §Key Parameters

The ignited-phase heating load is small and gyrotron CAPEX is lower than for NBI or ICRF systems — a cost advantage relative to beam-heated concepts. Startup gyrotron power (scaled up for Stellaris' larger plasma) is the primary uncertainty, but it does not represent a blocking challenge.

**5. Island divertor scaling to burning plasma conditions**

The island divertor was validated on W7-AS and W7-X at sub-fusion power densities. Scaling to 2.7 GW fusion power (significantly higher power density than W7-X's maximum ~14 MW heating) has not been demonstrated. At fusion-relevant power densities, island divertor target heat loads and erosion rates are uncertain. The geometry of the island divertor is set by the magnetic configuration, which gives it limited design flexibility compared to a poloidal divertor — the exhaust power must be handled where the islands naturally form. This is not necessarily a cost penalty, but it is a validated-physics-at-scale gap.

**6. Alpha demo cost and commercial timeline risk**

The Alpha demo is costed at ~EUR 2B [proxima-fusion-2026-updates.md], comparable to SPARC's cost profile but for a significantly less mature technology basis — no Q>1 stellarator has ever been built. The gap between Alpha (Q>1, ~2031) and Stellaris (commercial, late 2030s) must bridge from a first-ever Q>1 demonstration to a 1 GW commercial power plant in under a decade. Regulatory frameworks for commercial stellarator power plants in Germany have not been defined. The Gundremmingen site selection (former nuclear fission plant) provides regulatory infrastructure but introduces nuclear licensing complexity [proxima-fusion-2026-updates.md §RWE/Bavaria Note].

---

### Recommended Modeling Approach

**Framework applicability:** The 1costingfe framework (tokamak ConfinementConcept) provides a valid structural starting point for Stellaris but requires targeted overrides for the two cost accounts that diverge most from the tokamak reference: the magnet system and the current drive / heating system. The power balance structure, CAS21 (buildings), CAS23 (turbine plant), CAS26 (heat rejection), and the indirect cost and economics layers are directly applicable. The concept fits the MFE D-T power plant archetype well enough that free-form modeling is not required — 1costingfe with documented overrides is the right approach. The primary advantage of keeping the framework is that it enables direct LCOE comparison to the HTS compact tokamak on a consistent cost accounting basis, which is the central analytical question.

**Dominant unknown — coil cost premium:** The 3D HTS coil manufacturing cost premium over a wound-coil tokamak is the most consequential unknown and should be modeled as a multiplicative factor applied to the 1costingfe CAS22 magnet sub-account. The appropriate range is: floor set by Brown (2018) — a 15–30% premium over tokamak coil costs in the LTS era — and the ceiling determined by the 2027 SMC demo results and eventual W7-X HTS coil analogue data. Until the SMC demo is complete, the premium is unconstrained from above; modeling it as a free parameter over the range 1.0×–3.0× the wound-coil tokamak cost is the most defensible approach. This is the primary sensitivity axis for any Stellaris LCOE model: the LCOE result is a direct function of where this multiplier falls.

**Secondary modeling note:** The 1costingfe current drive and auxiliary heating sub-account should be zeroed out (no CS coil, no NBI/ICRF system) and replaced with a gyrotron-only CAPEX estimate scaled from ITER-spec gyrotron unit costs. This is a negative delta from the tokamak reference and should not be left at the tokamak default.

**Tertiary sensitivity — plasma volume and machine scale:** The low-beta penalty (~2.76% vs. ~5–8% for compact tokamaks) should be modeled as a named sensitivity axis. Plasma volume scales inversely with beta at fixed fusion power, implying Stellaris requires roughly 2–3× the plasma volume of a comparable-power compact tokamak — a direct CAPEX multiplier for structural, blanket, and coil costs. In the absence of published Stellaris machine dimensions, the Helios analogue (958 MW fusion, planar coils) scaled to 2.7 GW provides a bounding estimate of major radius: scaling fusion power by ~2.8× at similar beta and field strength implies major radius scaling by ~1.4× (since P_fusion ∝ R³ at fixed β and B). This gives a rough machine-scale envelope for the cost model. Major radius (or equivalently plasma volume) should be a free parameter over the plausible range until the full Stellaris paper dimensions are available.

### Key Hypotheses

The following propositions define what the cost model should test. Each is falsifiable against model outputs and can be revisited once SMC demo data or the full Stellaris paper are available.

- **H1 (Coil cost competitiveness):** The 3D HTS stellarator coil manufacturing cost premium over a wound tokamak coil of equivalent peak field strength is less than ~1.5× the tokamak reference. If false (premium exceeds ~1.5×), stellarator CAPEX per kWe is uncompetitive against HTS compact tokamaks even after accounting for the disruption-free availability advantage. This threshold is approximate and should be tested via sensitivity sweep.

- **H2 (Scale penalty cancellation):** The capacity factor benefit from disruption-free, steady-state operation is sufficient to offset the LCOE penalty from Stellaris' lower plasma beta (~2.76% vs. ~5–8% for compact tokamaks), which implies a larger plasma volume and higher structural CAPEX per unit fusion power. This hypothesis is testable with a specific threshold: a stellarator capacity factor advantage of **≥3–5 percentage points** over the HTS compact tokamak reference (e.g., ~88–92% vs. ~85% for a disruption-prone device) is needed to offset a ~10–15% CAPEX-per-kWe penalty at the low end of the coil cost multiplier range; this margin is insufficient to overcome a 2×+ coil premium. The ≥3–5 pp advantage estimate is grounded in the mechanism — no unplanned disruption-induced downtime in steady-state operation — but no published stellarator capacity factor target or long-run W7-X availability figure appears in the available sources, so the specific range is a modeling assumption to be validated rather than a sourced datum. If both the low-beta scale penalty and the coil cost premium compound without a capacity factor offset materializing, the stellarator is uncompetitive at any coil cost.

- **H3 (TBR adequacy):** The Stellaris TBR of 1.07 is sufficient for tritium self-sufficiency in steady-state commercial operation. If false — i.e., if the simulation-to-reality gap for WCLL in 3D stellarator geometry reduces effective TBR below 1.0 (as the Helios idealized-to-practical gap of 1.3→1.1 suggests is plausible) — the tritium fuel cycle becomes a blocking constraint independent of cost, requiring either blanket redesign or an external tritium supply that does not exist at commercial scale.

- **H4 (Ignition assumption):** Stellaris achieves alpha self-heating such that steady-state ECRH power requirement is ≤~5 MW in operation (burning plasma regime). If false — i.e., if Stellaris requires sustained external heating at tens of MW rather than ~1 MW post-ignition — the H&CD cost advantage in Section 7 (CAS22 H&CD: −50% to −80% delta) largely disappears and may reverse to a cost penalty. No Q>1 stellarator has been demonstrated; the ignition assumption is inferred from the 2.7 GW fusion power target (high fusion gain strongly implied) and from the Helios analogue's 1 MW ignited-phase ECRH [helios-stellarator-comparison.md §Key Parameters], but it is explicitly unconfirmed in public sources [dossier.md §Remaining Gaps]. The cost model should branch on this assumption: (a) ignited branch — ECRH ~1–5 MW steady-state → large H&CD saving preserved; (b) non-ignited branch — ECRH ~20–50 MW sustained → H&CD account reverts to a modest cost penalty and the net directional assessment in Section 7 changes sign on the H&CD row, strengthening the case that LCOE is uncompetitive against HTS tokamaks unless the coil cost multiplier is near unity.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature to most mature.

---

**3D HTS Stellarator Coil System — TRL 3–4**

- **Demonstrated**: Wendelstein 7-X (Max Planck IPP, 2015) demonstrated a complete 50 non-planar + 10 planar LTS (NbTi) coil set for a QI stellarator, validating the physics design approach and coil manufacturing concept at sub-commercial scale with legacy superconductor. Proxima has secured REBCO tape supply (agreement with Faraday Factory Japan [dossier.md §Driver Technology]) and is developing coil winding technology with PSI and BNET. AI-driven coil optimization has been used to design the winding geometry [proxima-fusion-technology-page.md §Key Details].
- **On paper only**: HTS non-planar stellarator coil at REBCO tape current densities and 20 T field — the SMC demo (2027) is specifically the first proof-of-concept [proxima-fusion-2026-updates.md §Milestones]. Full commercial magnet set at Stellaris scale. Quench protection scheme for complex 3D HTS coil geometry.
- **Missing at scale**: Whether REBCO tape can be wound into the required compound curves without degrading Jc has not been demonstrated. Manufacturing yield and reproducibility for precision stellarator coils at commercial quantities. Long-term fatigue under combined high-field + neutron irradiation for non-planar coil structures. The 2027 SMC demo is the key de-risking milestone: until it succeeds, TRL remains at the low end of this range.

This is the highest-risk subsystem for the Proxima concept and the primary differentiator in TRL from HTS tokamak programs, where 20 T wound coil demonstrations are already complete (CFS, September 2021; Tokamak Energy Demo4, November 2025).

---

**WCLL Tritium Breeding Blanket — TRL 3–5 (tokamak geometry: ~5; stellarator geometry: ~3)**

- **Demonstrated**: WCLL is the EUROfusion DEMO baseline blanket concept. Small-scale mockups and neutronic simulations have been validated in tokamak geometry. Proxima validated WCLL feasibility in Stellaris geometry via neutronic simulations, achieving TBR 1.07 [stellaris-design-details.md §Technical Specifications]. Tritium breeding in lead-lithium has been demonstrated at bench scale.
- **On paper only**: Full-scale WCLL module integration in complex 3D stellarator geometry. Tritium extraction from liquid lead-lithium at power-plant throughput rates. EUROFER97 behavior under combined 14 MeV neutron damage + temperature + PbLi corrosion over multi-year plant lifetime. The "innovative liquid-metal breeding blanket" for which Proxima has filed a patent may represent a substantially different approach [dossier.md §Tritium Breeding].
- **Missing at scale**: 14 MeV neutron testing of WCLL at relevant fluences. Tritium extraction at kg/day scale from a PbLi circuit. EUROFER97 at >100–150 dpa lifetime — this reduced-activation ferritic-martensitic steel has less long-term irradiation data than austenitic steels. Remote maintenance of blanket modules in 3D stellarator geometry is geometrically more complex than in a tokamak and has not been demonstrated.

---

**Tritium Fuel Cycle (common with all D-T concepts) — TRL 4–5**

The TRL assessment follows the cross-concept framework established in the HTS compact tokamak analysis [01-hts-compact-tokamak, Section 3]. The QI stellarator adds no unique tritium fuel cycle challenges beyond those shared with all D-T concepts, but the Stellaris TBR of 1.07 provides thinner self-sufficiency margin than the ARC FLiBe target (≥1.1).

- **Demonstrated**: Lab-scale tritium handling; JET and TFTR handled gram-level D-T tritium quantities. Tritium extraction from liquid metal breeders demonstrated at bench scale. ITER will be the first device to operate a proto-tritium-cycle at sub-commercial scale.
- **On paper only**: Closed-loop kg/day-scale self-sufficient fuel cycle for a commercial plant. Near-zero tritium loss across blanket + plasma exhaust + gas processing.
- **Missing at scale**: Industrial tritium processing plant for ~55 kg/year throughput [analogue: D-T at 1 GW thermal scale]. Tritium accountability in the PbLi circuit. Permeation barriers for water-cooled heat exchangers in a tritium environment. Demonstrated TBR > 1.0 in operating conditions — all current TBR data are from simulation or fission-neutron experiments, not 14 MeV fusion neutrons.

The 1.07 TBR margin (7% above self-sufficiency) should be compared to the idealized vs. practical TBR gap seen in the Helios analogue: 1.3 idealized vs. 1.1 practical [helios-stellarator-comparison.md §Blanket]. If the same gap applied to Stellaris, the practical TBR might fall below self-sufficiency. This is a model risk that should be captured as a sensitivity parameter.

---

**Island Divertor — TRL 4–6 (physics: ~6; power-plant scale: ~4)**

- **Demonstrated**: Island divertor concept validated on W7-AS (first demonstration) and W7-X in extended plasma operation with up to ~10 MW heating [proxima-fusion-2026-updates.md §W7-X Heritage]. W7-X validated the island divertor as the working exhaust solution for QI stellarators — this is more physics maturity than most stellarator-specific subsystems.
- **On paper only**: Island divertor performance at Stellaris fusion power density (2.7 GW, orders of magnitude higher power density than W7-X). Island divertor target design and heat load management at 10+ MW/m² steady state. Compatibility between island divertor geometry and WCLL blanket coverage in the same helical structure.
- **Missing at scale**: Long-term tungsten plasma-facing components at fusion-relevant 14 MeV neutron fluences and heat loads combined. Power exhaust solutions for the 3D island divertor in a reactor-scale QI stellarator.

---

**ECRH Heating System (gyrotrons) — TRL 6–8**

- **Demonstrated**: ECRH is the universal stellarator heating method. W7-X operates with up to 10 MW absorbed ECRH power via gyrotrons [inferred from W7-X heritage; dossier.md §Primary Heating]. ITER-specification gyrotrons at 170 GHz exist and are referenced in the Helios analogue as the planned heating technology [helios-stellarator-comparison.md §Key Parameters]. Gyrotron technology is mature for its heating role at the power levels needed.
- **On paper only**: ECRH system scaled to Stellaris plasma volume and density. High-efficiency transmission lines and launcher systems in a reactor geometry with neutron activation constraints.
- **Missing at scale**: Gyrotrons optimized for >60% wall-plug efficiency at Stellaris-relevant power levels. Long-term gyrotron reliability in a fusion plant environment (years of continuous operation with radiation exposure). The startup phase heating requirement for a 2.7 GW fusion plant is not confirmed; scaling from the Helios 10 MW startup [helios-stellarator-comparison.md §Key Parameters] to Stellaris scale may require 20–50 MW, but this is unconfirmed.

The ECRH power requirement at steady-state ignited operation is estimated at ~1 MW [analogue from helios-stellarator-comparison.md §Key Parameters], making gyrotrons a small fraction of total CAPEX and a negligible recirculating power contributor in steady operation.

---

**Vacuum Vessel and In-Vessel Structures — TRL 6–7**

- **Demonstrated**: W7-X demonstrated that complex 3D non-axisymmetric stellarator vacuum vessels can be designed and manufactured to tight tolerances — a direct proof-of-concept for the manufacturing challenge. ITER vacuum vessel manufacturing is validating large-scale fusion vessel construction at tokamak scale.
- **On paper only**: Stellaris-scale vacuum vessel at 3D non-axisymmetric geometry with 14 MeV neutron activation levels, blanket module attachment, coil support structure integration, and provision for remote maintenance access.
- **Missing at scale**: Remote maintenance in a 3D non-axisymmetric geometry is substantially more complex than in a tokamak. W7-X used only electron heating and had no activated in-vessel components, so W7-X maintenance experience does not transfer to a D-T burning plasma scenario. Radiation-hardened remote handling tooling for complex 3D geometries has no demonstrated precedent.

---

**Cryogenics and Thermal Management — TRL 7–8**

The assessment is the same as for the HTS compact tokamak [01-hts-compact-tokamak, Section 3]. Large-scale helium refrigeration plants are demonstrated at ITER scale. REBCO coils operate at ~20 K — warmer than LTS designs, reducing cryoplant size and cost. Stellarator-specific considerations: cryogenic penetrations for a 3D vacuum vessel are geometrically more complex than for an axisymmetric design, adding custom engineering cost, but this is a design-detail challenge rather than a technology readiness gap.

---

**Balance of Plant (Power Conversion) — TRL 8–9**

The same TRL assessment as HTS compact tokamak [01-hts-compact-tokamak, Section 3] applies. Steam Rankine at GW scale is mature commercial technology. The WCLL blanket outlet temperature (<500°C with EUROFER97) constrains the steam cycle to conventional Rankine operating conditions — similar to modern fission plants — rather than the higher-efficiency advanced cycles possible with ARC's higher-temperature FLiBe outlet. This limits gross thermal efficiency to approximately 35–40% but eliminates the exotic material compatibility challenges associated with ARC's FLiBe primary loop. The water-cooled secondary loop and standard steam turbine represent lower engineering risk than FLiBe-based systems.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical Bottleneck with Stellarator Premium**

The REBCO supply chain challenge described for the HTS compact tokamak [01-hts-compact-tokamak, Section 4] applies here with an additional penalty: stellarator coils require more conductor per unit field volume than wound tokamak coils, due to geometrically inefficient 3D winding paths. W7-X used ~600 km of NbTi superconductor for its modular coils — a proxy for conductor demand in an LTS stellarator. Stellaris operates at 20 T (vs. ~3 T for W7-X), and scaling field strength while maintaining stellarator geometry will require substantially more REBCO per unit plasma volume than a wound-coil tokamak design.

Proxima has signed an agreement with Faraday Factory Japan for REBCO tape supply [dossier.md §Magnet Type] and is planning a magnet factory with up to 1,000 jobs [proxima-fusion-2026-updates.md §Jobs], indicating in-house manufacturing is part of the supply plan rather than pure external procurement. This is a sound strategy given the specialized winding requirements, but it adds CAPEX to the magnet factory itself.

Global REBCO production capacity is ~few thousand km/year across all manufacturers, with current cost ~$30–100/kA-m and a commercial target of ~$10/kA-m [01-hts-compact-tokamak, Section 4]. For stellarator coils, winding losses and off-specification tape rejection during compound-curve winding may exceed the rates achievable with simpler toroidal geometries, effectively increasing cost per installed meter beyond the tape purchase price.

**Lithium-6 Enrichment**

The WCLL blanket requires lithium enriched in Li-6 for effective tritium breeding (natural abundance: ~7.5%). The Helios stellarator analogue uses 65% Li-6 enrichment [helios-stellarator-comparison.md §Blanket]. Proxima's Stellaris TBR of 1.07 does not specify enrichment level in public sources. Global Li-6 enrichment capacity is limited: the mercury-amalgam separation process used historically is now restricted in most Western countries; current producers are primarily Russia and China, with limited Western capacity under development. For a commercial fleet, Li-6 enrichment represents a supply chain concentration risk and adds cost above natural lithium pricing.

**Tritium — Declining External Supply (common with all D-T concepts)**

The global tritium supply constraint is identical to the assessment for all D-T concepts [01-hts-compact-tokamak, Section 4]. Startup inventory: ~1 kg at >$35,000/g ≈ $35M per plant [analogue]. Fleet scaling requires demonstrated TBR > 1.0 in operating conditions. Stellaris TBR of 1.07 provides 7% margin, lower than the ARC FLiBe target (≥1.1) but similar to the Helios PbLi practical value (1.1). Tritium extraction from WCLL PbLi circuit is technically distinct from FLiBe extraction — PbLi extraction technology (using permeation membranes or vacuum permeation) is considered more mature than FLiBe extraction and shares development with EUROfusion DEMO work, a potential supply chain benefit.

**EUROFER97 Structural Steel**

EUROFER97 is a reduced-activation ferritic-martensitic (RAFM) steel developed specifically for fusion applications by EUROfusion. It is produced at small scale (research quantities) by SIDENOR in Spain; a commercial plant would require hundreds of tonnes. The material is not currently produced at industrial scale, and its irradiation behavior at >100–150 dpa lifetime doses under combined neutron + temperature + PbLi chemistry is not fully characterized. EUROFER97 shares supply chain development with EUROfusion DEMO — if both Proxima and DEMO advance on similar timescales, there may be economies of scale in material qualification and production capacity.

The EUROFER97 operating temperature limit (<500°C) caps thermal cycle efficiency. This is a design constraint, not a supply chain risk per se, but it affects economic performance: higher-temperature structural materials (ODS steels, SiC composites) could enable more efficient steam cycles but are substantially less mature.

**Tungsten (First Wall and Island Divertor Targets)**

Island divertor targets and first wall components will use tungsten, consistent with all high-heat-flux D-T fusion concepts. Tungsten supply at commodity level is adequate. The unique challenge for a QI stellarator: the first wall and divertor targets follow the 3D helical plasma boundary, requiring curved/custom tungsten tiles rather than the standard flat or cylindrical tiles used in tokamak designs. Fabricating large, precisely shaped tungsten components with complex 3D geometry — including the potential for cracking during thermal cycling — is a cost and manufacturing challenge beyond the tokamak case.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Peak fusion power | 2.7 GW | stellaris-paper-details.md §Key Parameters | high | Explicitly stated; "peak," not average |
| Thermal power | ~3.1 GW | stellaris-paper-details.md §Key Parameters | high | Explicitly stated |
| Net electrical output | ~1 GW | stellaris-paper-details.md §Key Parameters | high | Explicitly stated; net after all loads |
| Net plant efficiency (fusion → net electric) | ~37% | [inferred: 1 GW net / 2.7 GW fusion] | medium | Gross thermal efficiency higher; recirculating power reduces net output |
| Overall plant efficiency (thermal → net) | ~32% | [inferred: 1 GW net / ~3.1 GW thermal] | medium | Consistent with WCLL + steam Rankine at <500°C with typical recirculating fraction |
| Volume-averaged plasma beta | ~2.76% | stellaris-paper-details.md §Key Parameters | high | Explicitly stated; lower than typical advanced tokamak |
| Magnetic field (peak at coil) | up to 20 T | proxima-fusion-technology-page.md §Technology | high | HTS REBCO coils |
| Tritium Breeding Ratio | 1.07 | dossier.md §Tritium Breeding; stellaris-design-details.md §Technical Specifications | high | WCLL blanket, neutronic simulation; 7% margin above self-sufficiency |
| Blanket structural temperature limit | <500°C | stellaris-design-details.md §Technical Specifications | high | EUROFER97 constraint; caps thermodynamic efficiency |
| Blanket type | WCLL (Water-Cooled Lithium-Lead) | stellaris-design-details.md §Technical Specifications | high | EUROFER97 structure; Proxima notes this is a concept demonstration, not the final choice |
| Fuel | D-T | dossier.md §Fuel | high | Confirmed |
| Operation mode | Steady-state, 24/7, disruption-free | proxima-fusion-technology-page.md §Technology | high | Inherent to stellarator: no plasma current |
| Alpha demo cost | ~EUR 2B | proxima-fusion-2026-updates.md §RWE/Bavaria MoU | medium | For Alpha (Q>1 demo, ~2031), not Stellaris commercial plant |
| ECRH startup power | ~10 MW [analogue] | [analogue: helios-stellarator-comparison.md §Key Parameters — Helios is smaller, 958 MW fusion; Stellaris scaled power may be ~20–40 MW] | low | Stellaris not stated; QI stellarator analogue only |
| ECRH ignited-phase power | ~1 MW [analogue] | [analogue: helios-stellarator-comparison.md §Key Parameters — "1 MW in ignited phase"] | low | Stellaris specific value not published; driven by physics, not machine size |
| Gross thermal efficiency | ~35–40% [inferred] | [inferred: EUROFER97 <500°C limit → steam Rankine at ~35–38% gross; Helios at 635°C achieves ~40%] | low | Temperature limit is the constraining factor |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value (Stellaris design point) | proprietary / not-yet-sourced | blocking | Fundamental to recirculating power fraction; not stated in any public source |
| Capital cost (Stellaris) | proprietary | blocking | No cost estimate published; Alpha EUR 2B is a demo cost |
| Capacity factor / availability target | proprietary | blocking | No maintenance schedule or target published |
| Machine geometry (major radius, plasma volume, coil dimensions) | not-yet-sourced | blocking | Required to estimate conductor demand, structural costs, and confinement time |
| Total REBCO conductor length | derivable | important | Estimable from machine dimensions and coil geometry if dimensions are known |
| ECRH power (confirmed for Stellaris) | not-yet-sourced | important | Strong analogue from Helios and W7-X but not confirmed for Stellaris scale |
| Thermal cycle type and steam temperature | not-yet-sourced | important | Strongly implied by WCLL + EUROFER97; full Stellaris paper likely specifies |
| Total recirculating power fraction | derivable | important | Estimable if gross electrical and net electrical are both known |
| LCOE estimate / bottom-up plant cost study | truly-unknown | blocking | No stellarator-specific NOAK cost study for a modern HTS QI stellarator exists |
| Li-6 enrichment level in WCLL blanket | not-yet-sourced | important | Not stated; Helios analogue uses 65% |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Full Stellaris paper parameters: Q, heating power, capital cost, efficiency, machine dimensions | S1, S5 | proprietary | blocking | Access DOI 10.1016/j.fusengdes.2025.114868; KIT repository may have an open-access preprint |
| 2 | NOAK capital cost estimate for Stellaris or any modern HTS QI stellarator | S2, S5 | truly-unknown | blocking | No published study exists; Brown (2018) IEEE TPS is the best structural analogue for cost decomposition |
| 3 | 3D HTS stellarator coil unit cost: $/module, total REBCO demand, manufacturing cost | S2, S4, S5 | truly-unknown | blocking | No HTS stellarator coil has been manufactured; 2027 SMC demo will provide first data |
| 4 | Q value (plasma energy gain) for Stellaris design point | S2, S5 | proprietary | blocking | Likely in full Stellaris paper; no public source |
| 5 | Capacity factor / maintenance schedule / blanket replacement interval | S2, S5 | proprietary | blocking | No published data; will likely appear in Alpha design documentation |
| 6 | Machine geometry: major radius, plasma volume, coil dimensions | S2, S4, S5 | not-yet-sourced | blocking | Full Stellaris paper; beta and field strength alone cannot bound CAPEX |
| 7 | Confirmed heating system: ECRH power, gyrotron count and specs for Stellaris | S2, S3, S5 | not-yet-sourced | important | Full Stellaris paper; Proxima APS-DPP or IAEA FEC conference presentations |
| 8 | Confirmed power conversion cycle: Rankine temperature, gross efficiency, cycle type | S2, S3, S5 | not-yet-sourced | important | Full Stellaris paper likely specifies; strongly implied by WCLL + EUROFER97 constraint |
| 9 | WCLL blanket adaptation specifics: TBR distribution across 3D geometry, dead-zone quantification | S3, S5 | not-yet-sourced | important | Full Stellaris paper; EUROfusion DEMO WCLL reports provide tokamak baseline for comparison |
| 10 | Final tritium breeding technology: WCLL confirmed vs. patent-protected alternative | S3, S4 | proprietary | important | Patent applications; Proxima has filed for "innovative liquid-metal breeding blanket" |
| 11 | Li-6 enrichment level in WCLL blanket | S4, S5 | not-yet-sourced | important | Not in public sources; Helios analogue (65% enrichment) is best current proxy |
| 12 | Stellarator-vs-tokamak CAPEX comparison with HTS technology | S2, S5 | truly-unknown | blocking | Brown (2018) is the only structural reference; it used LTS and does not reflect HTS geometry premiums |

---

## Section 7: Cross-Concept Notes

**Nearest-neighbor positioning:**

Stellaris sits within a small cluster of private-sector QI stellarator commercial plant concepts. Helios (Thea Energy, arXiv:2512.08027v1) is the nearest within-family neighbor — another private-sector QI-optimized stellarator power plant study using ECRH heating and a PbLi blanket; the key similarity is the shared QI physics approach and ECRH heating method, and the key difference is coil architecture: Helios uses planar coils while Stellaris uses 3D non-planar HTS coils, making Helios a useful parameter analogue but not a direct cost comparator [helios-stellarator-comparison.md §Relevance to Stellaris]. The EUROfusion HELIAS concept (W7-X → DEMO public-sector pathway) is the large-device public-sector comparator: it shares the same QI physics lineage (Max Planck IPP, W7-X heritage) and island divertor approach, but targets a device roughly 4–5× larger in fusion power, uses conventional LTS superconductor, and operates on a research timeline without commercial cost pressure — it anchors the public-sector performance baseline against which Proxima's private-sector cost case (HTS-enabled size reduction) is being made. The 01-HTS Compact Tokamak (CFS/ARC) is the cross-family economic benchmark used throughout this analysis because it is the nearest HTS MFE commercial competitor and shares the REBCO supply chain.

**Reference concepts used: 01-hts-compact-tokamak (CFS/ARC)**

The QI stellarator shares its most important supply chain with the HTS compact tokamak: REBCO tape from Faraday Factory Japan (Proxima has an agreement with them; CFS manufactures its own tape). The REBCO supply chain quantification, tritium fuel cycle assessment, BoP TRL assessment, and regulatory framework discussion from the HTS compact tokamak analysis [01-hts-compact-tokamak] are directly applicable and reused with attribution.

**Shared assumptions from 01-hts-compact-tokamak:**
- REBCO supply chain: global production ~few thousand km/year; current cost ~$30–100/kA-m; commercial target ~$10/kA-m [01-hts-compact-tokamak, Section 4]
- Tritium startup cost: ~1 kg required; >$35,000/g; global inventory ~25–30 kg and declining as CANDU reactors retire [01-hts-compact-tokamak, Section 4]
- Tritium fuel cycle TRL (4–5): same assessment applies [01-hts-compact-tokamak, Section 3]
- Balance of Plant TRL (8–9): steam Rankine at GW scale is mature; applies directly to WCLL-based steam cycle [01-hts-compact-tokamak, Section 3]
- Regulatory uncertainty: NRC Part 30 for US deployments; Stellaris adds EU/German regulatory uncertainty for the Gundremmingen site

**Key divergences from 01-hts-compact-tokamak:**

| Dimension | HTS Compact Tokamak (CFS/ARC) | QI Stellarator (Proxima/Stellaris) | LCOE Implication |
|-----------|-------------------------------|-----------------------------------|-----------------|
| Magnet geometry | Wound D-shaped TF/PF/CS coils | 3D non-planar coils | Stellarator coils: higher cost per installed conductor meter; no HTS precedent |
| Plasma current | ~21 MA (SPARC-class) | Zero | No disruptions; no PF/CS current-drive system; simpler vessel structural loads |
| Current drive requirement | LHCD + ICRF (~39 MW for ARC) | Not needed (stellarator is steady-state without current drive) | CAPEX and recirculating power saving for stellarator |
| Primary blanket | FLiBe molten salt (~900–1200 K outlet) | WCLL LiPb (<500°C, water-cooled) | ARC achieves higher thermodynamic efficiency; Stellaris uses simpler, lower-temp steam cycle |
| Volume-averaged plasma beta | ~5–8% (compact tokamak range) | ~2.76% | Lower stellarator beta → larger plasma volume per unit fusion power |
| Disruption risk | Significant; disruption protection required | Zero (no plasma current) | Stellarator vessel design: more benign structural loads; better availability potential |
| HTS coil demonstration status | 20 T wound coil demonstrated (CFS, September 2021) | 3D HTS coil NOT yet built; SMC demo planned 2027 | CFS is ~5–6 years ahead in coil TRL |
| TBR margin | ≥1.1 target (FLiBe) | 1.07 (WCLL) | Thinner stellarator margin; higher risk of breeding shortfall if simulation-to-reality gap exists |
| Physics basis | SPARC (MIT lineage) + decades of tokamak data | W7-X (Max Planck IPP) + QI stellarator experiments | Both credible physics bases; different risk profiles |

The most significant divergence for LCOE modeling is coil geometry. ARC's wound REBCO coil cost is at least partially bounded by SPARC manufacturing experience; the Stellaris 3D HTS coil cost has no commercial precedent and is the dominant cost uncertainty for this concept. The stellarator earns its complexity premium by eliminating disruptions and plasma current — a trade that may favor stellarators at scale if 3D HTS coil manufacturing costs fall along a sufficiently steep learning curve.

**CAS-Level Cost Delta Summary (Stellaris vs. HTS Compact Tokamak / ARC):**

| CAS Account | Subsystem | Direction | Rough Magnitude | Basis |
|-------------|-----------|-----------|-----------------|-------|
| CAS22 — Magnet system | 3D non-planar HTS coils (REBCO) | **Large positive delta** (Stellaris more expensive) | 1.15×–3.0× tokamak magnet cost | No HTS stellarator coil built; Brown (2018) gives 15–30% LTS premium; upper bound unconstrained until 2027 SMC demo |
| CAS22 — Heating and current drive | ECRH gyrotrons only; no CS, no NBI, no ICRF | **Negative delta** (Stellaris cheaper) | −50% to −80% vs. tokamak H&CD account | No central solenoid; no beam injectors; gyrotron cost << NBI/ICRF + CS combined. Helios startup: 10 MW ECRH only [helios-stellarator-comparison.md §Key Parameters] |
| CAS22 — Blanket and tritium | WCLL LiPb + EUROFER97; adapted to 3D geometry | **Small positive delta** (Stellaris moderately more expensive) | ~10–20% premium over tokamak WCLL baseline | 3D blanket geometry creates dead zones and more complex module segmentation; EUROfusion DEMO WCLL is the shared baseline |
| CAS22 — Remote maintenance | 3D non-axisymmetric in-vessel access | **Moderate positive delta** (Stellaris more expensive) | Uncertain; 1.2×–2× tokamak estimate | No precedent for D-T remote maintenance in 3D stellarator geometry; tokamak sector maintenance is itself immature |
| CAS23 — Turbine plant | Steam Rankine at WCLL outlet temperature (<500°C) | **Small negative delta** (Stellaris slightly less efficient) | ~2–5% lower gross thermal efficiency vs. ARC FLiBe | EUROFER97 caps steam temperature; conventional Rankine vs. ARC's potential supercritical cycle [inferred: WCLL + EUROFER97 constraint] |
| CAS26 — Heat rejection | Water-cooled secondary; lower-temperature heat rejection | **Neutral to slightly negative delta** | Negligible | Lower primary loop temperature simplifies materials; water-cooled is standard |
| CAS21 — Buildings | 3D machine geometry drives larger building footprint | **Small positive delta** | Scales with plasma volume; beta penalty | Larger machine at lower beta implies larger building; no specific data |
| Tritium fuel cycle (CAS22 sub) | WCLL PbLi extraction; TBR 1.07 | **Neutral** | Similar to tokamak baseline | PbLi extraction more mature than FLiBe; TBR margin thinner (1.07 vs. ≥1.1 ARC target) |
| BoP structure (CAS24–25) | Electrical systems, controls | **Neutral** | No significant delta | Steady-state simplifies some control systems; no pulsed power supply for CS |

**Net directional assessment:** The Stellaris CAPEX is almost certainly higher per kWe than an HTS compact tokamak if the 3D coil premium exceeds ~1.5×; it may be competitive if the coil premium is modest (~1.2×) and the capacity factor advantage materializes. The H&CD account saving (large negative delta) partially offsets the magnet premium, but the magnitude of the offset depends on how large the gyrotron-only system is relative to the NBI/ICRF/CS package it replaces — a quantitative comparison that no published source directly provides.

The QI stellarator's steady-state, disruption-free operation is a genuine long-term availability advantage that the tokamak does not share. Capacity factor, which the Araiinejad & Shirvan (2025) study identifies as the second-largest LCOE lever for D-T tokamaks (after CAPEX), could be substantially higher for a stellarator — if blanket replacement intervals and remote maintenance requirements are similar, the elimination of disruption-induced downtime is a direct LCOE benefit. This advantage has not been quantified in any published stellarator cost study.

---

## Section 8: Sources

**Primary sources accessed for this analysis:**

1. **Proxima Fusion Technology Page** (https://www.proximafusion.com/technology)
   — Company technology overview; HTS magnets (20 T, REBCO), island divertor, steady-state operation, disruption-free design, AI-driven coil optimization
   — Phase 1a source: `iter-01/sources/proxima-fusion-technology-page.md`

2. **Stellaris Power Plant Concept — Design Details** (*Fusion Engineering and Design*, Vol. 214, May 2025; DOI: 10.1016/j.fusengdes.2025.114868)
   — Primary engineering reference: fusion power (2.7 GW), thermal power (~3.1 GW), net electrical (~1 GW), WCLL blanket (TBR 1.07, EUROFER97, <500°C), magnetic field (20 T), paper scope (first wall, divertor, blanket, quench safety, remote maintenance)
   — Phase 1a sources: `iter-01/sources/stellaris-design-details.md`; `iter-02/sources/stellaris-paper-details.md`

3. **Proxima Fusion 2026 Updates** (multiple press releases, February–March 2026)
   — Alpha demo cost (~EUR 2B), RWE/Bavaria/Max Planck IPP MoU, SMC demo timeline (2027), magnet factory (up to 1,000 jobs), W7-X heritage milestones (highest triple-product for any stellarator, 8-minute plasma)
   — Phase 1a source: `iter-02/sources/proxima-fusion-2026-updates.md`

4. **Helios Stellarator Design — Comparison Analysis** (Thea Energy; arXiv:2512.08027v1)
   — Primary QI stellarator power plant analogue for this analysis: fusion power (958 MW), thermal power (1.1 GW), net electrical (390 MW net / 438 MW gross - 48 MW facility loads), ECRH heating (170 GHz, ITER-spec gyrotrons, 10 MW startup / 1 MW ignited), steam Rankine (~40% efficiency, 635°C), PbLi blanket (TBR 1.1 practical / 1.3 idealized), Li-6 enrichment 65%, multi-layer shielding, minimum 1.2 m plasma-coil distance
   — Phase 1a source: `iter-02/sources/helios-stellarator-comparison.md`

5. **Phase 1a Dossier** (QI Stellarator - HTS, 2 iterations, completed 2026-03-06)
   — Compiled per-column values with confidence ratings and citations; overall confidence: medium
   — Source: `exploration/phase_1a/research/09-qi-stellarator-hts/dossier.md`

**Cross-referenced prior analyses:**

6. **01-hts-compact-tokamak Analysis** (CFS/ARC; approved 2026-03-20)
   — Provides REBCO supply chain quantification, tritium fuel cycle TRL assessment, BoP TRL assessment, and regulatory framework discussion reused in Sections 3, 4, and 7 of this analysis
   — Source: `analyses/01-hts-compact-tokamak/analysis.md`

**Background references cited via dossier and prior analyses:**

7. **Brown (2018)**: "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements," *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230. DOI: 10.1109/TPS.2018.2831148
   — The only published multi-concept cost comparison that includes stellarators; provides the LTS-era cost decomposition that is the closest available structural analogue for Stellaris CAPEX

8. **Wendelstein 7-X publications** (multiple; Max Planck IPP): Physics basis for QI stellarator physics, island divertor demonstration (also W7-AS), QI optimization validation — cited via dossier and proxima-fusion-2026-updates.md
