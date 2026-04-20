# D1+ Analysis: Helical Coil Stellarator (Helical Fusion)

**Concept**: Heliotron-type Stellarator — continuous helical HTS coils (HESTIA design)
**Company**: Helical Fusion (Tokyo, Japan; NIFS spinout)
**Pilot Device**: Helix HARUKA (integrated demonstration, assembly 2026); Helix KANATA (pilot plant, 50 MWe, 2030s target)
**Confinement Family**: MFE — Stellarator (Heliotron)

---

## Section 1: Availability of Data

**Rating: Moderate**

The primary technical reference is Miyazawa & Goto (2023), *Physics of Plasmas* 30, 050601 — a peer-reviewed conceptual design paper for HESTIA (Helical Stellarator Torus with Integrated Alloy-blanket) that is unusually complete for a private startup. The paper provides explicit reactor geometry, a full parameter table including cost estimates, subsystem descriptions, engineering gain, and identified risk areas. However, the paper is behind a paywall (only the extended abstract is in the Phase 1a sources), and its cost figures are self-declared as based on late-1990s LHD/ITER construction pricing, with the authors explicitly requiring a ×2 or greater inflation correction before use [1].

> "if inflation during these 20 years is taken into account, the construction cost must be modified by a factor of 2 or more"
> — aip-2023-paper-abstract.md, §I

**Published design documentation:**
The 2023 AIP paper provides the most comprehensive public baseline, including: HESTIA reactor geometry (R₀ = 7.8 m, 8 T at coil center), a cost table estimating ~$5B direct construction cost, net electric output (~70 MWe), Q (plasma) ~13, Q_eng = 2.0, availability target >80–85%, and design rationale for all six major subsystems (HTS magnets, LM blanket, ECH system, fueling, sCO₂ power conversion, solar H₂ startup) [1]. A SOARHER variant (more conservative, lower-performance FPP) is discussed but not costed in detail.

**Milestone publications and press releases:**
ANS Nuclear Newswire (October 2025) and BusinessWire (October 2026) document a critical manufacturing milestone: the world's first demonstration of an uninsulated large-scale HTS coil using WISE REBCO conductor — 40 kA at 7 T external field, 15 K, 30 layers of REBCO, >4 m conductor length. A dedicated coil manufacturing machine was completed in collaboration with Sugino Machine [dossier.md, §Magnet Type].

**Company disclosures:**
The Helical Fusion technology overview (helical-fusion-technology-overview.md) provides a summary of 14 collaborative R&D areas including sCO₂ gas turbines, maintenance robotics, GALOP (GAs-driven Liquid metal OPeration) blanket testing, and WISE coil manufacturing. Total funding is modest at ~$35.3M through late 2025 [helical-fusion-2025-2026-updates.md], which is low relative to peers (CFS ~$2.9B, Tokamak Energy ~$335M).

**Independent and heritage documentation:**
NIFS — the parent institution — has extensive stellarator physics and blanket engineering heritage from LHD and the FFHR design study series. The Oroshhi-2 blanket test platform at NIFS studies liquid blanket materials and sCO₂ power conversion [nifs-ffhr-blanket-heritage.md; Ishiyama & Tanaka 2019, *Fusion Science and Technology* 75:8]. Brown (2018, *IEEE Transactions on Plasma Science*) provides a cross-concept cost decomposition comparing stellarators, standard tokamaks, and spherical tokamaks.

**Phase 1a dossier completeness:**
The dossier achieves high confidence on confinement family, confinement concept, fuel, heating method, plasma state, magnet type, tritium breeding approach, neutron management, and operation mode. One medium-confidence item remains: energy capture (sCO₂ Brayton cycle is strongly suggested by three independent data points but not explicitly confirmed as the HESTIA baseline).

**Key data gaps limiting this analysis:**
1. Full AIP paper content beyond the extended abstract (potentially more detail on TBR, alpha confinement, and cost breakdown)
2. Cost model not inflation-corrected by the authors — applying ×2+ multiplier introduces significant uncertainty
3. O&M cost breakdown entirely absent
4. LM pump power explicitly flagged as unknown in the paper
5. No independent techno-economic assessment of HESTIA or any heliotron FPP design exists in the public literature

---

## Section 2: Challenges in Capturing System Function

Ranked by LCOE impact.

**1. Cost model anchored to 1990s prices — first-order correction required (Impact: Critical)**

The only published cost estimate for HESTIA is Table I in Miyazawa & Goto (2023), with a direct construction cost of ~$5B. The authors explicitly state this is calibrated to late-1990s LHD and ITER construction prices and requires a factor-of-2-or-more inflation correction [1]. Applying a ×2 correction yields ~$10B for a 70 MWe plant — an extraordinary specific capital cost of ~$143B/GWe, compared to ~$6–15B/GWe for large tokamak estimates. Even the FOAK follow-on plant at ~103 MWe with a published ~$3B cost estimate (1990s prices) implies ~$6B inflation-adjusted, or ~$58B/GWe. These figures imply LCOE in the dollar-per-kWh range, and the primary path to competitiveness is fleet scaling, series production, and technology learning — none of which have a quantitative basis yet.

> "The cost is preliminary and based on the LHD construction and ITER cost data in the 1990s"
> — aip-2023-paper-abstract.md, §II

**Anchored LCOE range — lower and upper bounds:**
The TEA model, calibrated to the ARIES stellarator framework rather than the published HESTIA cost table, produces a lower-bound LCOE of approximately $1,160/MWh (at ARIES-framework capital cost structure, P_net = 70 MWe, CF = 80%). This is a structural lower bound because the ARIES framework cannot reproduce the published $10B inflation-adjusted overnight cost. To bound the range from above, applying the published cost directly: at $10B overnight cost, 70 MWe net output, 80% capacity factor, an 8.6% fixed charge rate (8% discount, 40-year life), and a nominal O&M of $60/kWe-yr (ARIES-CS analogue), the LCOE resolves to approximately **$1,750–1,850/MWh** (~$1.75–1.85/kWh). This upper-bound figure is driven almost entirely by the inflation-adjusted capital cost. For cross-concept comparison, both bounds must be reported: the framework lower bound (~$1,160/MWh) and the published-cost-anchor upper bound (~$1,800/MWh), with the caveat that the FOAK design point improves to approximately $700–1,000/MWh if the $6B inflation-adjusted cost and 103 MWe output are used. Any single LCOE figure for HESTIA without this range stated is misleading.

**2. Stellarator confinement improvement factor — geometry-transfer risk, not overoptimism (Impact: High)**

The HESTIA plasma design assumes H = 1.3 above the ISS04 empirical stellarator scaling law. Contrary to the initial framing of this as an overoptimistic claim, this assumption is *conservative relative to recent stellarator experimental performance*: the Helios preconceptual stellarator FPP design (2024) reports that W7-X has achieved H_ISS04 = 1.4 experimentally, citing this explicitly as justification for Helios's own H_ISS04 = 1.4 baseline — "this value has been achieved in the W7-X stellarator" [arxiv-2512-08027.md §3.1]. HESTIA's H = 1.3 is 0.1 below the demonstrated W7-X figure. The residual risk is not that H = 1.3 is overoptimistic but that HESTIA's heliotron geometry differs from W7-X (a quasi-isodynamic design): center-peaked ECH density profiles, alpha confinement properties, and turbulent transport characteristics may not transfer directly from the W7-X database to a heliotron configuration. The downside scenario remains relevant — if H = 1.0 (LHD-era performance without optimization), machine volume increases and capital cost inflates — but the central assumption should be treated as plausibly achievable in an optimized stellarator rather than an unjustified optimistic claim. A ±30% sensitivity range in H remains appropriate given the geometry difference, but the direction of risk is primarily in the heliotron-vs-QI transferability question rather than in whether H > 1 is achievable at all.

**3. Liquid metal pump power — explicitly unknown (Impact: High)**

The AIP paper acknowledges that the LM blanket circulation pump power is "quite unknown at this moment" [1]. This is a primary recirculating power component: with Q_eng = 2.0 (net electric / recirculating = 1.0 by definition), even modest LM pump power affects the achievable net output. The GALOP (gas-driven) pump eliminates rotating components for reliability, but its power consumption at plant-scale LM circulation rates through 90 modules has not been calculated. This directly affects Q_eng, gross electric sizing, and BOP design.

**4. Novel power conversion (sCO₂ at >50% efficiency) — undemonstrated at scale (Impact: High)**

The HESTIA design targets >50% thermal-to-electric conversion efficiency via an sCO₂ Brayton cycle at 800–1200 K working temperature. This efficiency is central to achieving Q_eng = 2.0 at Q (plasma) = 13 — a modest plasma gain. If conventional steam Rankine (~33–38% efficiency) is substituted, Q_eng drops below 2.0, and net output decreases significantly from the 70 MWe target. In the fusion-specific engineering literature, a CO₂ recompression Brayton cycle combined with a Rankine bottoming cycle achieves 47% gross efficiency in a fusion design study [Kovari et al. 2014, arxiv-1401-4232.md §Section 4] — the highest published figure in a fusion engineering context and already at the lower edge of HESTIA's target range. The NIFS Oroshhi-2 platform has a proposed sCO₂ demonstration targeting >50% efficiency, but a 20 kWe laboratory demonstration at 20% efficiency is the current state [helical-fusion-2025-2026-updates.md]. No fusion-coupled sCO₂ demonstration exists. The Kovari review — the most comprehensive fusion-specific energy conversion survey in the available sources — concludes that "there is as yet not a fully consistent solution for engineering design, coolants and working cycle" [arxiv-1401-4232.md §Summary]. HESTIA's >50% sCO₂ target is therefore not merely a company-specific execution risk but an instance of a field-wide unsolved design problem. Furthermore, the efficiency-to-LCOE relationship has a hard failure mode: below a threshold thermal efficiency where recirculating loads exceed gross electric output, net electric approaches zero and the design cannot close — the current 20% laboratory demonstration is far below this threshold, making the risk structural rather than a continuous cost sensitivity. Furthermore, the contemporary Helios preconceptual stellarator FPP study (2024, R₀ = 8 m, 390 MWe net) demonstrates how the broader stellarator design community handles this uncertainty: the Helios authors explicitly selected a 40% steam Rankine cycle as their power conversion baseline and do not consider sCO₂ at all — treating 40% Rankine as the appropriate conservative assumption at the current state of knowledge [arxiv-2512-08027.md §2, §4.4]. HESTIA's >50% sCO₂ target therefore diverges by 10+ percentage points from the contemporary stellarator design consensus on achievable power conversion efficiency. **A 40% Rankine fallback is not merely a downside sensitivity — it represents the peer-endorsed design-conservative assumption and must be modeled as an explicit scenario branch.** At 40% thermal efficiency with Q~13 plasma, HESTIA's Q_eng = 2.0 target cannot be maintained and net output falls below the 70 MWe design point.

**5. Tritium breeding ratio — 3D neutron transport calculation not yet complete (Impact: High)**

The paper acknowledges that the 3D neutron transport calculation required to confirm the TBR target has not been completed as of the 2023 publication date [1]. The LM blanket uses 80 at.% Li-6 enrichment, which is extremely high (natural Li is ~7.5% Li-6; ITER TBM designs use 60–90% enrichment but at smaller coverage fractions). Whether the heliotron geometry — with its complex coil geometry, maintenance ports, and coil-occupied volume — can achieve TBR > 1.0 with the proposed LM module arrangement remains unconfirmed.

**6. Unconfirmed liquid metal composition (Impact: Moderate)**

The AIP paper describes the LM first wall alloy as a tin-indium-lead-lithium mixture, with tin chosen for low vapor pressure and low hydrogen retention, and lithium providing the tritium breeding function. However, the exact composition (at.% fractions) is not publicly confirmed, and the NIFS FFHR heritage source notes the blanket material is distinct from the FLiBe used in the older FFHR line [nifs-ffhr-blanket-heritage.md]. The alloy chemistry affects tritium solubility, extraction process, MHD behavior, corrosion of structural materials, and supply chain (indium is a scarce element). This is an unresolved engineering parameter with material cost implications.

**7. Small plant scale drives high specific cost (Impact: Moderate)**

At 70–103 MWe, HESTIA is the smallest reactor design in the concept portfolio (along with compact experiments). High specific capital cost ($/kWe) at small scale is an inherent economic challenge. The concept's economic theory of value relies on steady-state operation (~80–90% availability) and fleet-manufacturing cost reductions achieving NOAK economics — a learning-curve argument that cannot be validated with current data.

**O&M placeholder:**
No O&M cost breakdown is available in the public record. A nominal O&M estimate can be drawn from analogue stellarator plant studies (ARIES-CS: ~$50–70/kWe-yr for fixed O&M) but is not anchored to HESTIA-specific design features. Steady-state operation (no plasma restarts) should reduce unplanned outage costs relative to pulsed concepts; the integrated LM first-wall/divertor eliminates one major replacement category. However, the novel HTS coil geometry and LM blanket system introduce new O&M uncertainties with no operational precedent.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**250 GHz / 1 MW Continuous-Wave Gyrotrons — TRL 1–2**

- **Demonstrated**: The highest-frequency, highest-power CW gyrotrons currently available for stellarator heating are ~154 GHz at <0.5 MW CW, developed for LHD at NIFS. ITER uses 170 GHz, 1 MW CW gyrotrons — but these operate at lower frequency and in a different power regime. No 250 GHz / 1 MW CW gyrotron has been demonstrated anywhere [1].
- **On paper only**: The HESTIA ECH system requires 60 such gyrotrons delivering a total of ~20 MW absorbed power (implying ~40 MW wall-plug assuming ~50% efficiency). The frequency (250 GHz) is required by the higher toroidal field and plasma density of HESTIA relative to LHD; it cannot be substituted with available technology.
- **Missing at scale**: The gyrotron technology itself must be invented at the required frequency-power-continuous-wave combination. Joint R&D with QST (Japan Atomic Energy Agency) is ongoing but has not achieved 250 GHz / 1 MW CW. This is the highest-TRL-risk single subsystem in the concept.

---

**Liquid Metal Blanket (Tin-Indium-Lead-Lithium Alloy) — TRL 2–3**

- **Demonstrated**: Lab-scale liquid metal loop experiments at NIFS using FLiNaK and LiPb (Oroshhi-2 platform). The GALOP gas-driven pump has been tested at NIFS as a proof-of-concept for the pumping mechanism [helical-fusion-technology-overview.md]. Liquid lithium and LiPb blanket concepts have been studied extensively in fission breeder reactor programs. The ITER Pb-17Li WCCB TBM provides a partial analogy for liquid metal blanket module design.
- **On paper only**: 90 modular tin-indium-lead-lithium LM blanket modules covering the complete plasma-facing first wall including divertor strike zones in a heliotron geometry. Tritium breeding from the alloy's lithium fraction at 80 at.% Li-6 enrichment. Simultaneous first-wall cooling, tritium breeding, and neutron shielding in a single flowing circuit. The specific alloy chemistry's tritium solubility, extraction kinetics, and corrosion behavior with the novel non-magnetic structural steel is at laboratory study stage.
- **Missing at scale**: 14 MeV neutron irradiation of the tin-indium alloy at fusion-relevant fluences (tin and indium activation behavior under fusion neutron spectrum is not well characterized). Industrial-scale LM circulation pump at plant-scale flow rates. Tritium extraction from a multi-component low-melting-point alloy (distinct from the LiPb or FLiBe extraction literature). Indium supply at the scale required for 90 large modules (indium is a byproduct of zinc smelting with ~900 tonnes/year global production — plant-scale demand could be material relative to supply).

---

**Non-Magnetic Structural Steel (High-Mn Austenitic) — TRL 2–3**

- **Demonstrated**: High-manganese alumina-forming austenitic steel with silicon addition has been developed as a collaboration between Helical Fusion and Tohoku University's Institute for Materials Research, with characterization published in 2024 [nifs-ffhr-blanket-heritage.md; dossier.md]. Material properties (non-magnetic, low activation, high-temperature corrosion resistance) have been assessed at small-scale coupon level.
- **On paper only**: Standard reduced-activation ferritic-martensitic (RAFM) steels used in ITER, EU-DEMO, and most MFE design studies are ferromagnetic, which would generate unacceptable error fields in the precision magnetic geometry of helical coils. HESTIA's blanket structural material must be non-magnetic — a requirement that eliminates the most mature structural materials database in fusion. The high-Mn steel is a new material with no nuclear qualification history.
- **Missing at scale**: Neutron irradiation database for high-Mn austenitic steel under fusion-relevant 14 MeV neutrons. The paper acknowledges known issues with high-Mn steels in neutron environments (elevated decay heat, potential swelling) and assesses these as manageable at HESTIA's low fusion power density (~tens of MW) — but this is an assumption, not a demonstration [1]. Industrial-grade production at nuclear-material purity, welding procedures, and long-term creep data are absent.

---

**sCO₂ Brayton Power Conversion at Fusion Outlet Temperature — TRL 3–4**

- **Demonstrated**: sCO₂ Brayton cycles are commercial at MW-to-GW scale in fossil power and CSP plants, with demonstrated efficiencies of ~40–47% at temperatures accessible to those systems. The most recent large-scale milestone is GTI Energy's STEP Demo (October 2024): a 10 MWe facility achieved grid-synchronized power at 500°C (773 K) in Phase 1, described as confirming "operability, efficiency, and commercial readiness" of the sCO₂ power cycle; Phase 2 targets 715°C (988 K) in a Recompression Closed Brayton Cycle configuration [gti-step-demo-achieves-phase-1-testing-milestone.md]. Phase 2's 988 K target falls within HESTIA's lower 800–1200 K operating range, making this trajectory materially relevant to the TRL assessment. In the fusion-specific literature, a CO₂ recompression Brayton cycle with a Rankine bottoming cycle achieves 47% gross efficiency in a fusion design study [Kovari et al. 2014, arxiv-1401-4232.md §Section 4] — the authoritative upper bound from a fusion engineering context. The NIFS Oroshhi-2 platform includes a proposed sCO₂ demonstration plan targeting >50% efficiency at 800–1200 K (Ishiyama & Tanaka 2019). A 20 kWe demonstration at 20% efficiency has been assessed as feasible [helical-fusion-2025-2026-updates.md]. This efficiency gap (20% demonstrated vs. >50% target) reflects the challenge of reaching high turbine inlet temperatures with fusion-compatible heat exchanger materials. Notably, the Helios stellarator FPP design (2024, arxiv-2512-08027.md) — the most comparable public stellarator FPP study — did not adopt sCO₂, instead selecting a 40% steam Rankine cycle as its baseline [§4.4], treating this as the achievable conservative choice at the current state of development.
- **On paper only**: >50% sCO₂ Brayton cycle integrated with a LM primary blanket circuit at 800–1200 K inlet temperature. The interface between the flowing LM (tin-indium alloy with tritium inventory) and sCO₂ secondary loop requires tritium-impermeable heat exchanger materials — an unsolved materials integration problem.
- **Missing at scale**: Tritium permeation suppression in LM-to-sCO₂ heat exchangers (tritium permeates readily through steel; sCO₂ at these temperatures increases permeation rate). Integration with the LM primary circuit chemistry (tin-indium alloy corrosiveness to heat exchanger alloys at 800–1200 K). Long-duration sCO₂ turbine reliability with fusion-relevant thermal cycling profile. The sCO₂ efficiency target is an aspiration; if only ~40% is achievable, Q_eng drops below the published 2.0 figure.

---

**WISE HTS Helical Coil System at Reactor Scale — TRL 3–5**

- **Demonstrated**: October 2025 milestone: 40 kA at 7 T external field, 15 K, in an uninsulated large-scale (>4 m length, ~3 cm cross-section) WISE REBCO coil — the world's first demonstration of this coil type [dossier.md]. The WISE (Wound and Impregnated Stacked Elastic tapes) conductor concept: REBCO tapes stacked for flexibility, wound into the helical geometry while pliable, then impregnated with a low-melting-point alloy for structural rigidity. A dedicated coil manufacturing machine was completed with Sugino Machine [dossier.md].

> "Helical Fusion has demonstrated the world's first successful demonstration of uninsulated large-scale HTS conductor-based coil achieving 40 kA at 7T"
> — helical-fusion-2025-2026-updates.md, §HTS Coil Milestone

- **On paper only**: Full-scale reactor helical coils at the HESTIA geometry (R₀ = 7.8 m, 8 T at coil center). The October 2025 test coil is a prototype element; a complete reactor coil set would require winding REBCO tapes in continuous helical paths at a scale orders of magnitude larger. Quench protection for uninsulated HTS coils at reactor scale and in a neutron environment. Coil alignment tolerances required for the precise magnetic field geometry of a heliotron.
- **Missing at scale**: REBCO tape performance under combined 14 MeV neutron irradiation + cyclic thermal loads at 20 K. The WISE impregnation alloy (low-melting-point alloy) behavior under fast neutron flux. Industrial production of kilometer-length continuous helical coils for two reactor coils per machine. Validated manufacturing tolerances for the complex 3D coil geometry at HESTIA scale.

---

**ECRH Heating at Pilot Plant Scale (existing frequency/power) — TRL 5–6**

- **Demonstrated**: MW-class gyrotrons at 170 GHz (ITER) and 154 GHz (LHD) are operational. The physics of ECH plasma heating and startup is mature and well-demonstrated on LHD and other stellarators. The 250 GHz frequency requirement is the gap (see TRL 1–2 subsystem above); if operating at a reduced plasma density or field that permits lower-frequency ECRH, the heating subsystem maturity would increase to TRL 7–8 — but this would change the operating point from the HESTIA design.
- **On paper only**: 20 MW continuous-wave ECRH at 250 GHz on a burning plasma.
- **Missing at scale**: 250 GHz CW gyrotrons (the blocking item); long-duration ECRH antenna/launcher surviving neutron and gamma background in a burning plasma heliotron.

---

**Remote Maintenance (Heliotron Geometry) — TRL 4–5**

- **Demonstrated**: ITER-class remote handling systems for tokamak blanket modules and divertor replacement are at TRL 6. Helical Fusion explicitly lists "maintenance robots" as one of 14 collaborative R&D priorities [helical-fusion-technology-overview.md]. The heliotron coil geometry constrains access differently than a tokamak — the two continuous helical coils form a complex 3D envelope around the plasma, requiring bespoke access paths. The 90 modular LM blanket modules are designed for crane access from upper ports without robotic in-vessel entry [1].
- **On paper only**: Complete remote handling scheme for a heliotron at HESTIA scale, including coil maintenance, blanket module extraction through upper ports, and diagnostics/instrumentation access through the helical coil geometry.
- **Missing at scale**: Validated maintenance cycle time consistent with >80% availability target. Radiation-hardened robotics customized for heliotron access geometry. Activated blanket module handling and storage system.

---

**Balance of Plant (Conventional Components) — TRL 7–9 (BOP), TRL 4–5 (LM–sCO₂ Integration)**

- **Demonstrated**: Conventional turbomachinery, cooling towers, electrical switchgear, and grid connection infrastructure are TRL 9 — commercially mature. The BOP challenge is specific to the LM primary loop interface with the sCO₂ secondary loop (see sCO₂ section above).
- **Missing at scale**: Tritium-impermeable primary-to-secondary heat exchangers for a tin-indium LM primary circuit. BOP integration with the solar H₂ production system used for startup power and HTS magnet cooling (a unique feature of the HESTIA design).

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO HTS Tape (WISE format) — Critical Bottleneck, Shared with HTS Concept Family**

The WISE conductor requires REBCO tapes wound into complex continuous helical geometry while flexible, then impregnated. REBCO global production capacity is on the order of a few thousand km/year across all manufacturers [21-spherical-tokamak-hts.md, Section 4]. Unlike tokamak coils, which can use shorter sections joined at demountable joints, the HESTIA concept uses two continuous helical coils — requiring much longer unbroken conductor runs. The tape demand for HESTIA's two reactor coils at R₀ = 7.8 m has not been published, but the helical path length scales roughly as 2π × R₀ × turns per helical period × number of periods × conductor cross-section layers. For a device of this scale, tens of thousands of km of tape may be required for a single machine. At current tape costs of ~$30–100/kA-m, even modest tape demands create multi-hundred-million-dollar cost items. The NOAK cost target for commercial viability (~$10/kA-m) has not been reached by any supplier.

**Liquid Metal Alloy (Tin-Indium-Lead-Lithium) — Novel, Supply-Constrained on Indium**

The LM blanket alloy is not a standard industrial material. The key supply concern is **indium**: global production is ~900 tonnes/year, dominated by refining as a byproduct of zinc ore smelting. Primary applications include ITO (indium tin oxide) for flat-panel displays and photovoltaics. Fusion-scale demand for 90 large LM blanket modules could be material relative to global supply, depending on the indium fraction of the alloy. No supply chain exists for fusion-grade indium-containing alloy production. Lead in the alloy creates low-level radioactive waste from neutron activation (Pb-208 → Pb-207 via (n,2n)); this does not affect supply but affects blanket module disposal.

**Li-6 Enrichment (80 at.% Target) — Globally Limited, Highest Enrichment in Portfolio**

The HESTIA TBR design requires 80 at.% Li-6 enrichment [1], which is at the high end of any fusion blanket design (most designs target 40–90% but at larger coverage fractions or thicker blanket geometries). Natural lithium is ~7.5% Li-6. Global Li-6 enrichment capacity is constrained: Russia and China operate legacy mercury-amalgam separation processes (banned elsewhere for environmental reasons); Western alternatives are in development but not at industrial scale. An 80 at.% target for 90 large blanket modules represents a significant enrichment demand, and the complex heliotron geometry (with coil intrusions) that necessitates high enrichment also suggests the TBR sensitivity to Li-6 fraction will be high — a shortfall in enrichment quality directly threatens tritium self-sufficiency.

**Non-Magnetic Structural Steel (High-Mn Austenitic) — New Industrial Material**

High-Mn austenitic steel with alumina-forming additions is being developed specifically for HESTIA [dossier.md; Tohoku University collaboration, 2024]. No industrial production process, nuclear qualification, or procurement baseline exists. The material must be produced at purity suitable for primary circuit service at 800–1200 K, with demonstrated weldability and long-term microstructural stability under neutron irradiation. This is a material that must be invented and qualified in parallel with the reactor development — a supply chain that does not yet exist.

**Helium Supply (Reduced vs. LTS) — Advantage Relative to LTS Designs**

Unlike LTS magnets requiring liquid helium at 4 K, HESTIA's WISE HTS coils operate at 20 K cooled by helium gas — dramatically reducing helium consumption per unit of cryogenic cooling. The AIP paper cites global helium scarcity as a motivation for the HTS-at-20K design choice [1]. This is a genuine supply chain advantage over older stellarator designs (W7-X uses LTS at 4 K), though helium supply uncertainty (concentrated in US, Qatar, Russia) remains a background risk for all cryogenic fusion systems.

**Tritium (D-T Startup Inventory) — Standard D-T Constraint**

The global tritium inventory is approximately 25–30 kg, produced primarily as CANDU byproduct, decaying at 5.5%/year [21-spherical-tokamak-hts.md, Section 4]. A startup inventory of ~1 kg at >$35,000/g is required for a 70 MWe plant. The HESTIA TBR target (>1.0, achieved with 80 at.% Li-6) provides self-sufficiency margin if the blanket performs as designed. At 50–70 MWe scale, tritium consumption per unit time is modest relative to large tokamaks, reducing the sequencing constraint. However, the TBR calculation has not been completed (see Section 2, Challenge 5).

**Indium Note — Potential Sole-Source Risk**

If indium constitutes even 5–10 at.% of the LM alloy and 90 modules contain several tonnes of alloy each, the indium demand for a single HESTIA could represent a few percent of annual global production. Unlike REBCO or FLiBe, indium demand for fusion has not been assessed in any published supply chain study. This is a potentially blocking gap if the alloy composition requires significant indium content.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Major radius (R₀) | 7.8 m | aip-2023-paper-abstract.md §Table I | high | HESTIA FPP design point |
| Magnetic field at coil center | 8 T | aip-2023-paper-abstract.md §II-B | high | Target coil field; ~9 T at plasma center |
| Plasma gain Q (FPP) | ~13 | aip-2023-paper-abstract.md §Abstract, §V | high | Design target; enables steady-state without large current-drive recirculation |
| Engineering gain Q_eng (FPP) | 2.0 | aip-2023-paper-abstract.md §Table I | medium | Gross electric 139 MW, net 70 MWe; sensitive to sCO₂ efficiency assumption |
| Fusion power (FPP) | ~260 MW | aip-2023-paper-abstract.md §Table I | medium | Derived from Q~13 and heating power; paper does not separately tabulate heating power |
| Gross electrical output (FPP) | ~139 MWe | aip-2023-paper-abstract.md §F | medium | Required to achieve 70 MWe net at Q_eng = 2.0 |
| Net electrical output (FPP) | 70.4 MWe | aip-2023-paper-abstract.md §Table I | high | Direct Table I value |
| Net electrical output (FOAK plant) | ~103 MWe | aip-2023-paper-abstract.md §Table I | medium | Same reactor size as HESTIA; improved Q_eng = 2.3 via technology maturation |
| Engineering gain Q_eng (FOAK) | 2.3 | aip-2023-paper-abstract.md §Table I | medium | Improved over HESTIA via technology improvements; not detailed |
| Thermal conversion efficiency | >50% (target) | aip-2023-paper-abstract.md §II-F; helical-fusion-2025-2026-updates.md §sCO₂ | medium | sCO₂ Brayton cycle target at 800–1200 K; only 20% demonstrated in kW-scale demo |
| Continuous operation duration | ~1 year | aip-2023-paper-abstract.md §Abstract; helical-fusion-technology-overview.md | high | Steady-state operation before maintenance; key commercial advantage |
| Maintenance cycle | ~3 months | dossier.md §Operation Mode; helical-fusion-technology-overview.md | high | After ~1-year burn period; yields >80% availability by cycle |
| Availability target (FPP) | >80–85% | aip-2023-paper-abstract.md §Table I | high | Target >85% FPP, >90% FOAK; comparable to best steady-state projections |
| Availability target (FOAK) | >90% | aip-2023-paper-abstract.md §Table I | medium | Commercial plant target; undemonstrated |
| Direct construction cost (HESTIA FPP) | ~$5B | aip-2023-paper-abstract.md §Table I | low | 1990s LHD/ITER pricing; ×2+ inflation correction required → ~$10B in 2023 USD |
| Direct construction cost (FOAK) | ~$3B | aip-2023-paper-abstract.md §I | low | Same 1990s price basis; inflation-adjusted ~$6B in 2023 USD |
| Prototype (HESTIA-Primary) cost | ~$480M | aip-2023-paper-abstract.md §Table I | low | 1990s prices; inflation-adjusted ~$960M |
| Simplified lifetime energy cost | $1.22/kWh (FPP); $1.19/kWh (FOAK) | aip-2023-paper-abstract.md §Table I | low | C_direct / (P_net × T_net); not a full LCOE — excludes O&M, fuel, financing, and inflation correction |
| ECRH total power (wall-plug) | ~40 MW | [inferred: 20 MW absorbed × 2 for ~50% gyrotron efficiency; 60 gyrotrons at 1 MW each = 60 MW heating power, 20 MW absorbed = 3× more beam than needed unless some gyrotrons share beams] | low | The paper states "60 gyrotrons × 1 MW / 3 = 20 MW to plasma" — three gyrotrons per ECH beam [1]; wall-plug = 60 MW, absorbed = 20 MW |
| Gyrotron count and specifications | 60 × 250 GHz / 1 MW CW | aip-2023-paper-abstract.md §II-D | high | Target spec; no 250 GHz / 1 MW CW gyrotron currently exists |
| LM blanket modules | 90 modular units | aip-2023-paper-abstract.md §II-C | high | Upper-port crane access; no in-vessel robotics required for module extraction |
| Li-6 enrichment required | 80 at.% | aip-2023-paper-abstract.md §IV | high | Required for adequate TBR per design assumption; TBR not yet confirmed by 3D transport |
| WISE coil demonstrated performance | 40 kA at 7 T, 15 K | helical-fusion-2025-2026-updates.md §HTS Coil; dossier.md §Magnet Type | high | World-first uninsulated large-scale REBCO coil; October 2025 milestone |
| HTS coil operating temperature | 20 K (gas He cooling) | aip-2023-paper-abstract.md §II-B | high | Gas He vs. LTS liquid He at 4 K; reduces He consumption |
| H confinement improvement factor | 1.3 above ISS04 | aip-2023-paper-abstract.md §II-A | medium | Conservative relative to W7-X demonstrated H_ISS04 = 1.4 (arxiv-2512-08027.md §3.1); residual risk is heliotron-vs-QI geometry transfer, not whether H > 1 is achievable |
| Alpha particle confinement | ~85% | aip-2023-paper-abstract.md §II-A | low | Assumed based on prior FFHR analysis; "marginal" at ρ > 0.7 per paper |
| Sudo density limit | Plasma center exceeds limit | aip-2023-paper-abstract.md §II-A | medium | Off-axis ECH mitigation proposed; acknowledged risk |
| Company funding (total) | ~$35.3M | helical-fusion-2025-2026-updates.md | high | Series A + extension through late 2025 |
| LM pump power | unknown | aip-2023-paper-abstract.md §II-C | N/A | "Quite unknown at this moment" — direct quote from the paper; affects Q_eng calculation |
| Recirculating power fraction | [inferred] ~50% | [inferred: Q_eng = 2.0 → P_recirc = P_net; if gross = 139 MWe and net = 70 MWe, recirculating = 69 MWe ≈ 50% of gross; ECRH wall-plug ~43 MW + cryogenics + LM pumps + misc account for bulk of this] | low | Tight margin; >50% sCO₂ efficiency is essential to maintain Q_eng ≥ 2.0 |
| REBCO tape cost (market) | $30–100/kA-m | 21-spherical-tokamak-hts.md §Section 4 | medium | Current market range; commercial viability target ~$10/kA-m |
| Regulatory cost multiplier (fission-style) | 2.2× building cost | Stewart & Shirvan 2022 [cited in 21-spherical-tokamak-hts.md] | medium | Upper-bound scenario; Japan regulatory path uncertain but likely more favorable |

---

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Inflation-adjusted construction cost | derivable | blocking | Authors explicitly flag need for ×2+ correction but do not apply it; ×2 applied here as working estimate but true NOAK cost trajectory is unknown |
| O&M cost breakdown (fixed + variable) | truly-unknown | blocking | No O&M data anywhere in public record; no analogue stellarator plant study exists; placeholder needed for any LCOE model |
| LM blanket pump power | truly-unknown | blocking | Explicitly flagged as unknown in primary source paper; determines true Q_eng |
| Full LCOE (vs. simplified C_direct metric) | derivable | blocking | $1.22/kWh metric excludes O&M, fuel, financing, and inflation correction; not comparable to LCOE figures from other concepts without full build-up |
| Tritium breeding ratio (confirmed by 3D neutron transport) | truly-unknown | blocking | 3D transport calculation not yet completed per paper; 80 at.% Li-6 assumption may not achieve TBR > 1.0 in complex heliotron geometry |
| H confinement factor at HESTIA scale | truly-unknown | blocking | H = 1.3 is an assumption; unvalidated; drives machine size and hence all cost estimates |
| sCO₂ thermal efficiency at plant scale | not-yet-sourced | blocking | Current demo at 20% (kW-scale); target is >50%; intermediate scale validation absent |
| Liquid metal alloy exact composition | proprietary/not-yet-sourced | important | Sn-In-Pb-Li alloy fractions not published; affects indium supply risk, tritium chemistry, and structural material corrosion data |
| REBCO tape total demand for HESTIA coil set | derivable | important | Not published; derivable from coil geometry (continuous helical path length × turns × layers); likely tens of thousands of km |
| Capacity factor target | derivable | important | >80% availability implied by ~1-year burn + 3-month maintenance cycle; formal CF target not stated |
| Alpha particle confinement at HESTIA scale | not-yet-sourced | important | 85% assumption from prior FFHR analysis; ρ > 0.7 marginality noted; required for accurate alpha heating in Q calculation |
| Component replacement schedule (coil, blanket modules) | truly-unknown | important | LM blanket modules replaceable via crane; no replacement interval given; affects availability and maintenance OPEX |
| Power conversion cycle (confirmed baseline) | proprietary/not-yet-sourced | important | sCO₂ Brayton is directional evidence from 3 independent indicators; no source explicitly confirms this as HESTIA baseline |
| Gyrotron wall-plug efficiency at 250 GHz | truly-unknown | important | 250 GHz gyrotrons do not exist; efficiency cannot be measured; ~50% is an analogue from lower-frequency gyrotrons |
| Startup power (solar H₂ system) cost | not-yet-sourced | nice-to-have | Unique to HESTIA design; solar H₂ used for both HTS cooling (liquid H₂ at 20 K) and startup power generation; capital cost not estimated |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Construction cost uses 1990s price basis; ×2+ inflation correction required but not applied in published table | S1, S5 | derivable | blocking | Apply US GDP deflator or construction cost index from 1998–2023; obtain current-dollar estimate from Helical Fusion or independent engineering study |
| 2 | O&M cost breakdown entirely absent from all public sources | S2, S5 | truly-unknown | blocking | Use ARIES-CS O&M analogue (~$50–70/kWe-yr fixed O&M) as placeholder; flag as unanchored |
| 3 | LM blanket pump power flagged as "quite unknown" in the primary source — directly affects Q_eng | S2, S3, S5 | truly-unknown | blocking | Engineering analysis of GALOP pump at 90-module LM circulation rate; consult Helical Fusion or NIFS Oroshhi-2 pump performance data |
| 4 | 3D neutron transport calculation for TBR not completed; 80 at.% Li-6 assumption unvalidated | S2, S3, S5 | truly-unknown | blocking | Monte Carlo neutron transport (MCNP or OpenMC) with HESTIA coil geometry; Helical Fusion and NIFS are likely performing this work |
| 5 | H confinement factor H = 1.3 assumed above ISS04; unverified at HESTIA scale | S2, S5 | truly-unknown | blocking | Validate with stellarator confinement database scaling; Helix HARUKA integrated demo may provide first data point by end of 2020s |
| 6 | sCO₂ power cycle efficiency at fusion-coupled plant scale — only kW-scale at 20% demonstrated by NIFS; GTI STEP Phase 2 (715°C / 988 K target) is the closest industrial milestone | S3, S5 | not-yet-sourced | blocking | GTI STEP Demo Phase 2 completion (gti-step-demo-achieves-phase-1-testing-milestone.md) will close temperature gap to HESTIA lower bound; monitor Phase 2 results. Review NIFS Oroshhi-2 sCO₂ program status. Note: peer stellarator FPP study (Helios, 2024) chose 40% Rankine, not sCO₂ — model this as the design-conservative scenario branch |
| 7 | Liquid metal alloy composition (at.% fractions of Sn, In, Pb, Li) not publicly confirmed | S2, S4, S5 | proprietary/not-yet-sourced | important | Full AIP paper may specify; Helical Fusion patent filings may disclose; determine indium content for supply chain analysis |
| 8 | REBCO tape total demand for two continuous helical reactor coils | S4, S5 | derivable | important | Calculate from helical coil path length at R₀ = 7.8 m × conductor cross-section dimensions; scale from October 2025 test coil geometry |
| 9 | Indium supply chain impact — demand relative to global production of ~900 tonnes/year | S4 | truly-unknown | important | Determine alloy In fraction; estimate mass per module × 90 modules; compare to annual production |
| 10 | Alpha particle confinement at ρ > 0.7 — flagged as marginal in paper | S2, S5 | truly-unknown | important | Neoclassical and gyrokinetic transport calculations for HESTIA heliotron geometry; W7-X alpha confinement studies provide partial analogy |
| 11 | Component replacement intervals (LM blanket modules, HTS coils) not stated | S3, S5 | proprietary/not-yet-sourced | important | Engineering estimate based on neutron fluence rate at blanket wall and material damage thresholds for high-Mn steel |
| 12 | Capacity factor target not formally stated | S5 | derivable | important | 1-year burn + 3-month maintenance → ~80% upper bound; derate for unplanned outages; sensitivity study covers range 70–90% |
| 13 | Non-magnetic structural steel irradiation behavior under fusion neutrons | S3, S4 | truly-unknown | important | No 14 MeV irradiation data for high-Mn austenitic steel; ITER TBM fission-spectrum irradiation analogue only partial |
| 14 | Full LCOE build-up (vs. C_direct / P_net × T_net surrogate) | S5 | derivable | important | Full LCOE requires: inflation-corrected CAPEX + O&M analogue + financing assumptions + CF estimate + fuel cost (tritium startup) |
| 15 | 250 GHz / 1 MW CW gyrotron performance and cost — technology does not exist | S3, S5 | truly-unknown | important | Monitor QST gyrotron R&D program; use cost scaling from existing 170 GHz ITER gyrotrons as lower-bound analogue |
| 16 | Independent stellarator FPP cost study for heliotron geometry | S1 | not-yet-sourced | nice-to-have | Brown (2018) provides stellarator cost decomposition relative to tokamak; ARIES-CS provides modular stellarator plant study; no heliotron-specific analog exists |

---

## Section 7: Cross-Concept Notes

**Prior approved analysis referenced: 21-spherical-tokamak-hts (Tokamak Energy ST-E1)**

The spherical tokamak HTS analysis is the most relevant approved prior due to shared REBCO HTS supply chain and shared D-T tritium constraints. However, the HESTIA concept diverges from the ST-E1 in nearly every structural respect — confinement topology, coil geometry, blanket chemistry, scale, and operating philosophy. Cross-referencing is primarily useful for shared infrastructure costs and supply chain constraints.

**Reused assumptions and data:**
- **REBCO supply chain**: Global production bottleneck (~thousands km/year), current pricing ($30–100/kA-m), commercial viability target (~$10/kA-m) [21-spherical-tokamak-hts.md, Section 4]. Applied here with the caveat that HESTIA's continuous helical coils may require longer unbroken runs than tokamak coil sets, amplifying the bottleneck.
- **Tritium supply**: Global inventory ~25–30 kg, startup cost >$35,000/g, CANDU production decline [21-spherical-tokamak-hts.md, Section 4]. Identical D-T constraint applies. HESTIA's smaller scale reduces per-machine startup demand relative to GWe-class tokamaks.
- **Regulatory cost uncertainty**: Stewart & Shirvan (2022) 2.2× building cost factor applies to all D-T fusion concepts as an upper-bound scenario [21-spherical-tokamak-hts.md, Section 4]. Japan's regulatory trajectory may differ from US/EU; the NRC's 10 CFR Part 30 decision is US-specific and does not apply to HESTIA.
- **Capacity factor sensitivity**: The Araiinejad & Shirvan (2025) finding that capacity factor is a primary LCOE lever for D-T MCF plants applies here. HESTIA's steady-state operation provides structural advantage over pulsed concepts (no plasma restart losses), but novel subsystems (LM blanket, 250 GHz gyrotrons) introduce unplanned outage risk not present in more mature concepts.

**Key divergences from the ST-E1 and broader tokamak family:**

- **Confinement geometry — continuous helical coils vs. modular coils**: HESTIA is a heliotron using two long continuous helical coils, not the planar or modular coil topologies used by other stellarator entries in this portfolio (QI Stellarator - HTS, QI Modular HTS Stellarator, Planar Coil Stellarator, Large-Scale Stellarator). The continuous coil winding is the core manufacturing challenge but also enables a simpler coil system with fewer joints. No other concept in this portfolio uses this approach.

- **Scale — smallest MFE power plant in the portfolio**: At 70–103 MWe, HESTIA is significantly smaller than any tokamak concept (CFS ~200 MWe, ST-E1 450–750 MWe, Gauss 1+ GWe). The implied specific capital cost ($143B/GWe inflation-adjusted for the FPP; ~$58B/GWe for the FOAK) is the highest in the portfolio. The economic thesis depends on mass production of modular units rather than large-scale plant economics.

- **Liquid metal blanket chemistry — closest neighbor is Renaissance Fusion (20b)**: The Renaissance Fusion Compact Liquid-Wall Stellarator (20b) also uses a liquid metal wall, the only other concept in the portfolio with this approach. Key differences: Renaissance uses laser-patterned HTS film coils (not WISE REBCO); its liquid metal composition has not been identified in public sources. HESTIA's tin-indium-lead-lithium alloy represents a different chemistry from the liquid lithium used in ITER TBM experiments. The two liquid-metal stellarators share the non-magnetic structural material requirement; high-Mn steel is HESTIA-specific but the underlying need is shared.

- **sCO₂ power conversion target — highest efficiency in portfolio**: The >50% sCO₂ Brayton cycle target is more aggressive than any power conversion approach in other analyzed concepts (steam Rankine at 33–38%; sCO₂ at ~40–47% in CSP applications). This efficiency is essential to achieving Q_eng = 2.0 at Q~13 — without it, the concept cannot achieve net electricity at this plasma gain. No other concept in the portfolio has this dependency; the sCO₂ assumption is a structural load-bearing element of HESTIA's economic case.

- **Solar H₂ for startup and cooling — unique integration**: The use of solar-generated liquid H₂ for both HTS magnet cooling (20 K) and startup power generation is a unique feature with no parallel in other concepts. This integration reduces operating costs for magnet cooling (no helium refrigerator at full cryogenic scale) but adds a solar-plus-electrolyzer capital cost not represented in any other concept model.

- **Recirculating power structure — zero current-drive overhead vs. tokamaks**: The Kovari (2014) fusion energy conversion review explicitly distinguishes stellarators from tokamaks on internal power demand: "A stellarator does not have this issue" — referring to the power required to drive circulating plasma current [arxiv-1401-4232.md §Section 2]. HESTIA's recirculating power fraction (~50% of gross output at Q_eng = 2.0) is composed entirely of ECRH heating (~40 MW wall-plug for 60 gyrotrons), cryogenic cooling, LM pumping, and BOP auxiliary loads — with zero current-drive component. By contrast, a steady-state tokamak at equivalent Q_eng = 2.0 must absorb all of those same loads plus a current-drive power demand (typically 10–30% of gross electric output), meaning a tokamak achieving Q_eng = 2.0 requires substantially higher plasma Q to compensate. HESTIA's Q_eng = 2.0 at Q~13 is therefore not equivalent to a tokamak's Q_eng = 2.0 in terms of physics challenge — the stellarator reaches the same net output fraction from a less demanding plasma operating point. When comparing Q_eng figures across concepts in the portfolio, the absence of current-drive overhead is a structural TEA differentiator: equal Q_eng implies harder physics for any tokamak that achieves it.

- **Heliotron vs. QI modular stellarators — coil cost structure and scale thesis**: Within the stellarator family, the nearest TEA comparators are 09-qi-stellarator-hts (Proxima Fusion Stellaris, ~1 GWe, non-planar modular HTS) and 10-large-scale-stellarator (Gauss Fusion GIGA, 1 GWe, 18 m major radius, 40 non-planar modular coils), both of which use quasi-isodynamic (QI) coil architectures. On coil cost structure, HESTIA's continuous helical coils carry a structural joint-count advantage: the helical winding requires no internal superconducting joints, compared to ~10,000 demountable joints across GIGA's 40 coils at a critical resistance target of ~1 nΩ each [10-large-scale-stellarator analysis]. However, this advantage is offset by a more severe tape-continuity constraint: continuous helical coils cannot be assembled from joined segments, so HESTIA requires unbroken REBCO conductor at lengths orders of magnitude beyond the 4 m October 2025 prototype — with no fallback option if a long-run tape fails during winding. GIGA's ~26,000 km REBCO tape demand already exceeds current global production by >10× [10-large-scale-stellarator analysis]; HESTIA's two helical coils at R₀ = 7.8 m require an unpublished but likely comparable tape length with the additional constraint of full continuity. Proxima Fusion's non-planar modular design carries a 1.5–5× manufacturing cost premium per unit fusion power over wound tokamaks due to 3D freeform geometry [09-qi-stellarator-hts analysis]; HESTIA's continuous helical geometry is no simpler and loses the modular quality-control advantage. On balance, the heliotron coil topology is expected to be a **cost penalty relative to QI modular designs at FOAK**: the joint-count advantage is real but does not offset the manufacturing difficulty of continuous kilometer-scale HTS winding in helical geometry — an industrial capability that does not yet exist. On scale thesis, HESTIA's economic case depends on fleet replication of 70 MWe units achieving NOAK learning (small-modular logic), while Gauss and Proxima target 1 GWe single-plant scale with FOAK capital of €15–18B/GWe (Gauss) before NOAK reduction. Neither path has a published NOAK cost trajectory, but the mechanisms are fundamentally different: HESTIA's path requires high-volume identical-unit manufacturing, while the QI stellarator path requires learning from progressively larger single plants. For the TEA model, this determines the C220103 (coil cost) structure: HESTIA's coil cost should be parameterized on tape demand per continuous helical run and manufacturing yield, while QI modular costs are dominated by 3D winding mandrel and joint qualification — distinct cost driver architectures within the same HTS stellarator family.

**Cross-concept modeling note for the TEA pipeline:**
HESTIA's "simplified lifetime energy cost" metric (C_direct / (P_net × T_net) = $1.22/kWh) must not be compared directly to LCOE figures from other concepts. This metric excludes O&M, fuel, discount rate, and inflation — all of which are first-order LCOE contributors. A proper LCOE comparison requires rebuilding the HESTIA cost structure from first principles using: inflation-adjusted CAPEX, analogue O&M, tritium startup cost, and a capacity factor assumption.

**Modeling priority — coil cost upper-bound sweep:**
The continuous helical coil cost (C220103) is the dominant capital item in the ARIES-framework model, at approximately 71% of reactor plant equipment cost with an LCOE elasticity of ~1.36. The current framework parameterization is a lower bound — it uses ARIES modular coil cost factors and does not capture the manufacturing premium for continuous kilometer-scale REBCO winding in helical geometry. The comparison to QI modular stellarator designs (which carry 1.5–5× manufacturing cost premiums per unit fusion power over wound tokamaks) provides the basis for an upper-bound range. The model should include a coil cost multiplier sweep: 1× (ARIES framework lower bound), 2×, and 3× C220103. At 3×, the LCOE would approximately triple the C220103 contribution relative to other cost components, shifting total LCOE substantially above the current framework value and approaching (though not reaching) the published-cost upper bound. This sweep is the highest-priority modeling action: it converts the current single-point lower-bound LCOE into a bounded range useful for cross-concept comparison.

**Modeling priority — operating point consistency:**
The framework model back-solves to P_net = 70.4 MWe, which requires Q_sci > 13 (higher than the published HESTIA design assumption). The physics-forward result at fixed Q = 13 and η_th = 50% gives P_net ≈ 52 MWe with Q_eng ≈ 1.53. The 52 MWe figure is the correct design-point result for the published Q~13 assumption; its LCOE is higher than the headline figure due to the lower net output. For cross-concept comparison, the 52 MWe physics-forward result should be the primary reported figure, with the 70.4 MWe back-solved case clearly labeled as requiring Q_sci > 13 with the implied Q stated explicitly. The sCO₂ scenario sweep in the model already computes this operating point and should be promoted to the primary output.

---

## Section 8: Sources

**1. Miyazawa, J. and Goto, T. (2023) — HESTIA reactor design paper (primary reference)**
- Full citation: Miyazawa, J. and Goto, T. (2023) "A conceptual design of a commercial reactor based on a helical-type plasma confinement," *Physics of Plasmas*, 30, 050601. doi:10.1063/5.0143612.
- Contribution: Primary engineering reference for all HESTIA design parameters — geometry, performance (Q~13, 70 MWe, Q_eng=2.0), subsystem descriptions, cost estimates (1990s price basis requiring ×2+ inflation correction), identified risks (H factor assumption, LM pump power unknown, TBR calculation incomplete, Sudo limit concern, alpha confinement marginality). Most technically complete public document for this concept.
- Location: Phase 1a source [iter-01/sources/aip-2023-paper-abstract.md]

**2. ANS Nuclear Newswire / BusinessWire (October 2025) — HTS coil milestone**
- Contribution: Documents the October 2025 WISE HTS coil demonstration (40 kA at 7 T, 15 K, 30 layers REBCO, >4 m length) — "world's first uninsulated large-scale HTS conductor-based coil." Primary evidence for current manufacturing readiness.
- Location: Referenced in dossier.md §Magnet Type; helical-fusion-2025-2026-updates.md

**3. Helical Fusion technology overview (helical-fusion-technology-overview.md)**
- Contribution: 14 collaborative R&D areas including sCO₂ gas turbines (energy conversion), maintenance robots, GALOP liquid metal pump. Confirms 50 MWe first-plant and 100 MWe commercial targets. Primary source for technology roadmap and subsystem identification.
- Location: Phase 1a source [iter-01/sources/helical-fusion-technology-overview.md]

**4. Helical Fusion 2025–2026 updates (helical-fusion-2025-2026-updates.md)**
- Contribution: HTS coil milestone details; Helix HARUKA assembly schedule (2026); Helix KANATA pilot plant 2030s target; funding (~$35.3M); sCO₂ demonstration feasibility assessment (20 kWe at 20% efficiency); Sugino Machine manufacturing collaboration.
- Location: Phase 1a source [iter-02/sources/helical-fusion-2025-2026-updates.md]

**5. NIFS FFHR blanket heritage documentation (nifs-ffhr-blanket-heritage.md)**
- Contribution: Clarifies design evolution from FFHR FLiBe blanket heritage to HESTIA liquid metal blanket; Oroshhi-2 twin-loop platform (LiPb and FLiNaK); high-Mn alumina-forming austenitic steel development by Helical Fusion + Tohoku University. Establishes that the specific LM composition for HESTIA remains unconfirmed in public sources.
- Location: Phase 1a source [iter-02/sources/nifs-ffhr-blanket-heritage.md]

**6. Ishiyama, S. and Tanaka, T. (2019) — NIFS sCO₂ demonstration plan**
- Full citation: Ishiyama, S. and Tanaka, T. (2019) "Demonstration Plan of Nuclear Fusion Power by CO2 Gas Turbine System," *Fusion Science and Technology*, 75(8), pp. 698–708.
- Contribution: NIFS Oroshhi-2 sCO₂ power conversion demonstration plan targeting >50% efficiency at 800–1200 K. Primary evidence for sCO₂ as the HESTIA power cycle. Provides the specific efficiency target and temperature range.
- Location: Referenced in dossier.md §Energy Capture; Semanticscholar.

**7. Brown, T.G. (2018) — Stellarator, ST, and tokamak cost comparison**
- Full citation: Brown, T.G. (2018) "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements," *IEEE Transactions on Plasma Science*, 46(6), pp. 2216–2230. doi:10.1109/TPS.2018.2831148.
- Contribution: Framework for comparing stellarator capital costs vs. tokamak and ST configurations by component category. Only published cross-concept cost decomposition covering the stellarator family directly. Not specific to heliotron topology but provides reference anchor for major cost elements.
- Location: Referenced in handwritten exemplar [01-hts-compact-tokamak.md]

**8. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-concept reference for REBCO tape supply chain characterization (tape costs $30–100/kA-m, production bottleneck), D-T tritium startup constraints (~1 kg at >$35,000/g, global inventory ~25–30 kg), and regulatory cost uncertainty (Stewart & Shirvan 2.2× factor). Provides consistent assumptions across HTS D-T concepts in the portfolio.
- Location: `analyses/21-spherical-tokamak-hts/analysis.md`

**9. ARIES-CS (ARIES Team, ~2004–2008) — modular stellarator plant study**
- Contribution: ARIES Compact Stellarator power plant study provides the most complete published stellarator FPP engineering baseline (1000 MWe, modular coils). Not directly applicable to heliotron topology but provides a reference cost structure for stellarator BOP, maintenance, and blanket systems when HESTIA-specific data is absent.
- Location: Referenced at https://qedfusion.org/DOCS/bib.shtml (ARIES archive)

**10. Kovari, M., Harrington, C., Jenkins, I., and Kiely, C. (2014) — fusion energy conversion review**
- Full citation: Kovari, M., Harrington, C., Jenkins, I., and Kiely, C. (2014) "Converting energy from fusion into useful forms," *Proceedings of the Institution of Mechanical Engineers, Part A: Journal of Power and Energy*. doi:10.1177/0957650913514230.
- Contribution: Comprehensive fusion-specific review of energy conversion systems covering coolants, thermodynamic cycles (Rankine, Brayton, combined), and parasitic internal power demands. Explicitly states that stellarators carry zero internal current-drive power demand ("A stellarator does not have this issue" — §Section 2). Establishes 47% gross efficiency for a CO₂ recompression Brayton cycle with Rankine bottoming in a fusion design study (§Section 4) as the fusion-engineering upper bound. Concludes "there is as yet not a fully consistent solution for engineering design, coolants and working cycle" (§Summary) — framing the sCO₂ challenge as field-wide rather than HESTIA-specific. Used in Sections 2, 3, and 7.
- Location: Phase 2a source [iter-02/sources/arxiv-1401-4232.md]

**11. GTI Energy STEP Demo (October 2024) — sCO₂ MW-scale demonstration**
- Full citation: GTI Energy press release, "STEP Demo Pilot Achieves Phase 1 Testing Milestone, Paving the Way for Next-Generation Supercritical CO2 Power Production," October 7, 2024.
- Contribution: Documents Phase 1 completion of the 10 MWe STEP sCO₂ demonstration facility in San Antonio (500°C, grid-synchronized, 4 MWe achieved) and Phase 2 target (715°C / 988 K, 10 MWe, RCBC configuration). Confirms "commercial readiness" language for the sCO₂ cycle and establishes that MW-scale demonstration at temperatures approaching HESTIA's lower operating range was achieved in 2024. Phase 2 at 988 K would fall within HESTIA's 800–1200 K target range.
- Location: Phase 2a source [iter-02/sources/gti-step-demo-achieves-phase-1-testing-milestone.md]

**12. Goodman, S. et al. (2024) — Helios preconceptual stellarator design study**
- Full citation: Goodman, S. et al. (2024) "Helios: A Preconceptual Design of a Compact Stellarator Power Plant," arXiv:2512.08027.
- Contribution: Contemporary peer stellarator FPP study (R₀ = 8 m, 958 MW fusion power, 390 MWe net) providing two critical data points: (1) W7-X has achieved H_ISS04 = 1.4 experimentally (cited in §3.1 with Nuclear Fusion references), used by Helios as its own baseline — establishing that HESTIA's H = 1.3 is conservative relative to the current stellarator confinement database; (2) Helios explicitly selected a 40% steam Rankine cycle as its power conversion baseline (§2 Table 1, §4.4), not sCO₂, treating this as the achievable conservative design choice at the current state of knowledge. Used in Sections 2, 3, and 7.
- Location: Phase 2a source [iter-02/sources/arxiv-2512-08027.md]

---

[1] aip-2023-paper-abstract.md, §I–§V: Primary HESTIA design reference; cost figures based on 1990s LHD/ITER construction prices; explicit ×2+ inflation correction required; LM pump power "quite unknown at this moment"; H confinement factor H = 1.3 assumed but unverified; TBR 3D neutron transport calculation not yet completed.
