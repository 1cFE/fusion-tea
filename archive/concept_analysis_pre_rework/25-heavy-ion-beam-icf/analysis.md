---
ID: 25-heavy-ion-beam-icf
Concept: Heavy Ion Beam ICF (D-T)
Company: Intensity Energy
Status: draft
Created: 2026-04-20
Approved-Date:
Reuses: [21-spherical-tokamak-hts]
---

# D1+ Analysis: Heavy Ion Beam ICF (D-T) — Intensity Energy

**Concept**: Heavy Ion Beam Inertial Confinement Fusion — D-T fuel
**Company**: Intensity Energy (unverified — almost certainly a placeholder; not found in FIA 2025 survey of 53 fusion companies or any public database)
**Driver**: Linear induction accelerator (US reference); RF linac (European/GSI alternative)
**Confinement Family**: IFE — Heavy Ion Beam

---

## Section 1: Availability of Data

**Rating: Moderate (physics and plant studies) / Opaque (commercial)**

Heavy ion beam ICF is one of the most extensively analyzed IFE concepts at the power plant design level, owing to sustained national laboratory programs in the US (LBNL, LLNL) and Europe (GSI Darmstadt). However, all detailed design studies are from the 1980s and 1990s, no private company currently pursues the concept commercially, and "Intensity Energy" cannot be verified as an existing entity.

**Published power plant design studies:**

Two complete conceptual power plant designs exist in the public literature. HIBALL (KfK-3202, 1985) was a joint German-US study using a 10 GeV Bi²⁺ induction linac to drive direct-drive DT targets at 3.8 GWe net output with a LiPb blanket [hif-technology-overview.md §Power Plant Designs]. HYLIFE-II (OSTI 7021072, LLNL, early 1990s) proposed a 5 MJ recirculating induction accelerator with thick FLiBe liquid-jet walls, producing 940 MWe at a baseline LCOE of 6.5 cents/kWh (early-1990s dollars), scaling to 4.5 cents/kWh at 2 GW [hif-technology-overview.md §HYLIFE-II]. The "Improved HYLIFE-II heat transport system and steam power plant" companion report provides the energy conversion design. These are the most complete fusion power plant economic analyses of any IFE concept in the public domain.

**Peer-reviewed physics literature:**

A 2020 arXiv review paper (arxiv 2005.07520) provides a current overview of HIF technology status, driver efficiency comparisons, target physics, and the ~10–15 Hz repetition rate target for commercial plants [dossier.md §Key Sources]. The LBNL HIF program produced decades of peer-reviewed literature on ion beam physics, beam transport, and target coupling. The GSI/HIDIF program produced complementary European studies with RF linac architectures.

**Experimental platforms:**

NDCX-II (Neutralized Drift Compression Experiment, LBNL) has been operational since approximately 2012, providing a platform for heavy ion beam compression and target heating experiments [dossier.md §Key Sources]. FAIR/SIS100 (GSI Darmstadt, heavy ion synchrotron) was commissioning in 2025 and produces high-intensity ion pulses relevant to HIF [hif-recent-research-compilation.md §No New Private Companies Found]. The LBNL HIF program itself ended; no successor US program exists.

**Company transparency:**

Nonexistent. "Intensity Energy" cannot be found in the FIA 2025 survey of 53 fusion companies, Crunchbase, LinkedIn, ARPA-E awards, DOE databases, Wikipedia, conference proceedings, or news sources [intensity-energy-search-results.md §Assessment]. Heavy ion beam ICF is pursued exclusively by national laboratories and academic groups, not private commercial entities as of 2026. The concept name in this analysis reflects the archetype, not a specific company's design.

**Phase 1a dossier completeness:**

High-confidence values achieved for confinement family, driver technology, fuel, plasma state, magnet type (none for plasma), operation mode, and repetition rate. Medium confidence on energy capture (steam confirmed from historical designs but modern concepts might use sCO₂), tritium breeding choice (HIBALL used LiPb, HYLIFE-II used FLiBe — no company has selected), and neutron management (integrated blanket/shield confirmed but design details depend on blanket choice). After two research iterations, the medium-confidence items cannot reach high confidence without a commercial developer making design choices [dossier.md §Remaining Gaps].

**Key data gaps limiting this analysis:**

1. All cost data is 30–40 years old (1985 HIBALL, early-1990s HYLIFE-II), with no modern reanalysis in current dollars
2. No private company exists to provide design choices or proprietary performance targets
3. Driver component lifecycle costs (induction cell replacement, beam transport magnet maintenance) are not characterized for commercial operation
4. Ion source performance at commercial duty cycle is unstated
5. Final focus opnet design for 10+ Hz rep rates is an active research gap

---

## Section 2: Challenges in Capturing System Function

Heavy ion beam ICF has a distinctive LCOE challenge profile relative to both laser ICF and MFE concepts. The core structural advantage — high driver wall-plug efficiency — is well-established. The core challenge is translating 30-year-old national laboratory designs into a contemporary commercial cost model without a living commercial program to provide updated numbers.

**1. Driver capital cost dominates LCOE, and estimates are ancient (Impact: Critical)**

The HYLIFE-II study estimated $570M direct cost for the recirculating induction accelerator driver [hif-technology-overview.md §HYLIFE-II]. This is the only published bottom-up cost estimate for an HIF driver and is stated in early-1990s dollars. Inflated to 2026 dollars (CPI ~2.5×), this becomes approximately $1.4B — a figure that must be regarded as highly uncertain because (a) induction linac costs have not been re-estimated with modern construction and component costs, (b) the "recirculating" architecture (where beam pulses are compressed and recirculated in a storage ring) was not the US reference architecture but a specific HYLIFE-II choice, and (c) HIBALL used a different ~3 km single-pass linac design. The driver cost is plausibly 40–60% of total plant capital cost, making its uncertainty the single largest LCOE uncertainty.

> "HYLIFE-II estimated $570M direct cost for recirculating induction accelerator driver"
> — hif-technology-overview.md, §HYLIFE-II

The driver's modular architecture (hundreds of identical induction cells) is frequently cited as a manufacturing scaling advantage: mass-production of identical cells could substantially reduce per-cell cost below what scientific-instrument procurement achieves. But no learning-curve analysis exists to quantify how far this reduction could extend.

> **Modeling limitation (F-1)**: The 1costingfe framework's `eta_pin` parameter produces *positive* LCOE elasticity (+0.148) for this HIF model — higher driver efficiency raises modeled LCOE rather than reducing it. This is a framework wiring issue: `eta_pin` is designed for tokamak plasma heating efficiency and enters a cost sub-model that does not correctly represent IFE driver recirculating power. As a result, the quantitative driver efficiency advantage over laser ICF cannot be demonstrated through the sensitivity sweeps in the current model. The manual workaround is the driver capital scenario sweep: reducing C220104 from $1.4B to $0.7B (NOAK modular manufacturing) drops LCOE from $92.3/MWh to $78.8/MWh, proxying the manufacturing-learning pathway. The correct recirculating-power framing (Section 2, H3 under Modeling Approach below) shows a ~13% generation requirement penalty for a laser ICF plant at 25% recirculation vs. HIF at 15% — this comparison must be made manually until the framework wiring is corrected.

**2. Target fabrication at commercial rep rate is uncharacterized (Impact: High)**

HIF targets are simpler than NIF hohlraums — direct-drive spherical capsules with a lead or gold tamper, aluminum pusher, and thin DT ice layer [hif-technology-overview.md §Target Design] — but must be produced at ~10 Hz for one chamber or multiple Hz per chamber in multi-chamber configurations. At 10 Hz for 30 years, a single chamber requires approximately 9.5 billion targets. No cost estimate exists for mass-produced HIF targets. The target fabrication cost must satisfy the Goodin et al. (2004) criterion used for laser IFE economics: target cost must be less than ~10% of the electricity value per target. At HYLIFE-II's baseline power output and historical LCOE, this implies roughly a few dollars per target in 1990s dollars. Whether DT ice-layer targets with external tamper shells can be produced at this cost in commercial volumes is unknown — it is likely achievable in principle given simpler geometry than laser ICF hohlraums, but it has never been demonstrated.

**3. Rep-rated chamber operation at 5–15 Hz has no demonstrated analog (Impact: High)**

A key selling point of HIF over laser ICF is that the accelerator is physically separated from the chamber, so final focus optics do not need to survive the neutron and X-ray environment of each shot. However, the chamber itself must clear ejecta, reform liquid wall protection (if HYLIFE-II-style FLiBe jets), and accept the next target within ~100–200 ms (at 5–10 Hz) or ~67 ms (at 15 Hz). HYLIFE-II analyzed chamber clearing in detail and concluded that the FLiBe jet system could reform within the cycle time, but this was an analytical conclusion, not an experimental demonstration. The NDCX-II and FAIR platforms are single-shot or low-rep-rate devices; no high-rep-rate chamber exists. The chamber clearing problem is architecturally simpler for HIF than for laser ICF (no optical delivery, so the chamber can be filled with gas or liquid), but it remains undemonstrated at commercial rates.

**4. Cost data currency: all figures are 30–40 years old (Impact: High)**

HIBALL (1985) and HYLIFE-II (early 1990s) predate modern fusion cost methodologies, advanced manufacturing for linac components, and any private fusion LCOE analysis. The CAS cost structure used in contemporary fusion TEA (CAS10-LCOE, from which this project's analysis framework derives) did not exist. No independent cost review of HIF power plants has been published since the 1990s. Comparing HIF LCOE to modern laser ICF or MFE estimates requires not just inflation adjustment but conceptual re-baselining, which has not been done. This is an analytical gap that is theoretically resolvable (by re-running HYLIFE-II or HIBALL economics through a modern cost framework) but has not been performed in the accessible literature.

**5. Final focus optics/magnets for high-rep-rate operation (Impact: Moderate)**

Ion beams must be focused onto millimeter-scale targets through superconducting or permanent quadrupole magnet arrays. The final focus system must survive proximity to each fusion event without degrading. Unlike laser optics (which are damaged by X-rays and neutrons), magnetic focusing elements do not absorb light — they are shielded by the large stand-off distance achievable with ion beams. But at 10–15 Hz over 30 years, the final focus magnets accumulate substantial radiation damage from neutrons and activated ejecta. The lifetime and replacement schedule of these elements is not addressed in either HIBALL or HYLIFE-II.

**6. Regulatory and commercial pathway are undefined (Impact: Moderate, Structural)**

With no private company pursuing HIF commercially, there is no regulatory engagement, no licensing pathway being scoped, and no cost estimate for regulatory compliance. As with all D-T IFE concepts, a first commercial plant would require a regulatory framework that does not yet exist. The cross-concept precedent (from D-T tokamak analysis) suggests regulatory cost could multiply facility construction cost by ~2.2× under a conservative fission-analog framework [21-spherical-tokamak-hts analysis, §Section 2, citing Stewart & Shirvan 2022].

**7. Plant availability is the primary LCOE lever — uncharacterized for rep-rated HIF (Impact: Critical)**

Sensitivity analysis identifies availability as the dominant LCOE parameter for this HIF archetype: elasticity ≈ −0.96, meaning each 1-percentage-point drop in availability raises LCOE by approximately 1%. The central-case availability is set to **0.75** per the project's scoring framework canonical value for Pulsed IFE D-T concepts (scoring_framework.md §"Plant availability") — this is a policy-driven choice rather than a concept-specific citation, enabling apples-to-apples cross-concept comparisons within the pulsed IFE family. A swing from 90% to 70% availability changes LCOE by approximately +27% (~$83.9/MWh to ~$106.5/MWh at the base case). This magnitude — roughly 3× the next-largest engineering lever (Q_eng at −0.32) — makes availability the central commercial viability question.

For a rep-rated plant at 6 Hz (~1.9 × 10⁸ shots/year), availability is determined by three independent subsystem chains:

- **Induction linac uptime**: Hundreds of identical induction cells operate at 6 Hz continuous duty. Modular architecture means individual cell failures do not require full shutdown and can in principle be hot-swapped, but cumulative failure rates across the whole driver at commercial rep rate and duty cycle are uncharacterized. High-energy physics accelerators provide the best analogue (~85–95% scheduled availability), but those machines run at lower rep rates and duty cycles with far more engineering margin than an optimized commercial power plant.
- **Liquid wall cycling reliability**: FLiBe jet nozzles and manifolds cycle thermally and mechanically at 6 Hz over 30 years. Nozzle erosion, jet formation degradation, and molten salt corrosion of piping are uncharacterized failure modes at this duty cycle. A nozzle bank failure disrupts chamber clearing and forces shutdown.
- **Target injection system**: Automated cryogenic DT target delivery at 6 Hz requires sub-mm accuracy for beam-on-target focusing. Any systematic drift in injection accuracy or cryogenic supply interruption propagates directly to lost pulses and, at sustained rates, to unplanned outage.

No published HYLIFE-II or HIBALL availability analysis exists. The plausible range for a first-of-kind HIF plant spans 70–90%, with 0.75 as the canonical base case per project policy. At 0.75, the model LCOE is $99.7/MWh. The LCOE consequence of a 5-percentage-point availability shortfall from base is approximately +$6/MWh (70% → $106.5/MWh); a 10-point shortfall adds ~$13/MWh. Bounding this range is the most important model parameter to resolve for HIF commercial assessment.

---

### Modeling Approach and Key Hypotheses

**Framework**: The 1costingfe tokamak-centric cost accounting framework has been adapted for this HIF analysis. Key structural gaps relative to HIF's actual cost shape:

- *No native IFE driver cost sub-account*: The induction linac driver ($1.4B, C220104) is manually assigned as the dominant reactor plant equipment item; the framework default for this account assumes plasma-facing components, not an accelerator.
- *Target factory OPEX underrepresented*: The `target_factory_base` constant captures staffing-based fixed overhead but does not represent variable consumable cost for ~189 million cryogenic DT targets per year. If target cost reaches $1–3/target, this becomes a significant OPEX term above current defaults.
- *No blanket replacement CAPEX*: HYLIFE-II's FLiBe liquid wall claims 30-year chamber lifetime with no first wall replacement, eliminating a large scheduled CAPEX item present in solid-blanket MFE and IFE designs — this is a structural cost advantage correctly not costed in the model.
- *eta_pin wiring limitation*: See modeling limitation note under Challenge 1. The driver efficiency advantage over laser ICF must be evaluated through manual scenarios (H3 below) rather than parametric sweeps.
- *plasma_t is a framework artifact with no HIF meaning*: The sensitivity table shows `plasma_t` at +0.245 elasticity (third-ranked lever). For an IFE concept, plasma temperature is not a design variable — the IFE performance analogs are target gain (q_sci) and driver energy. This elasticity is a framework artifact with no HIF design interpretation, analogous to the eta_pin wiring issue.
- *CAS21 (Buildings) likely undercosted; model LCOE is a lower bound*: CAS21 ($622M) uses per-MW civil works scaling derived from tokamak building geometry. An HIF plant requires a ~3 km accelerator tunnel — a qualitatively different civil works scope. This may partly explain the 43% gap between model LCOE ($92/MWh) and inflation-adjusted HYLIFE-II historical reference ($162/MWh; 6.5 c/kWh × 2.5 CPI). The model LCOE should be read as a probable lower bound; the inflation-adjusted historical figure as a probable upper bound. This gap is tracked separately from driver capital uncertainty in the gap table.

**Key hypotheses**:

- **H1 — Driver CAPEX reduction is the path to competitive LCOE**: If modular induction linac manufacturing reduces driver capital from $1.4B (scientific-instrument procurement) to $0.7B (NOAK factory production), LCOE falls from $92/MWh to $79/MWh. Tested in the driver capital scenario sweep.

- **H2 — Availability floor determines whether HIF crosses $100/MWh**: At the canonical availability (0.75, per scoring_framework.md §"Plant availability" for Pulsed IFE D-T), LCOE is $99.7/MWh — essentially at the $100/MWh threshold (elasticity −0.96). Above 75%, LCOE falls below this threshold (80% → $93.7/MWh; 90% → $83.9/MWh); below 75%, it rises above it (70% → $106.5/MWh). A 5-point shortfall from base adds ~$6/MWh; a 10-point shortfall adds ~$13/MWh. This is the most critical operational uncertainty to bound. Tested via availability scenario sweep (70%/75%/80%/85%/90%) in the model output.

- **H3 — HIF driver efficiency reduces recirculating power requirement vs. laser ICF**: At 15% recirculating power (HIBALL), gross generation must be 940/0.85 = 1,106 MWe. At 25% recirculation (laser ICF analogue), gross must be 940/0.75 = 1,253 MWe — a 13% penalty in gross generation with direct LCOE impact. This comparison must be made manually because the current model's eta_pin wiring is inverted (see Challenge 1 modeling limitation note).

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**Ion Source and Injector System at Commercial Duty Cycle — TRL 2–3**

- **Demonstrated**: Small-scale ion sources at NDCX-II (LBNL) and FAIR (GSI) produce heavy ion beams relevant to HIF physics research. NDCX-II produces ns-duration, ~1 MeV Li⁺ beams for target heating experiments [dossier.md §Key Sources]. FAIR/SIS100 produces high-intensity pulses from a synchrotron, not a linac architecture, and is for nuclear physics, not HIF power.
- **On paper only**: A commercial HIF injector producing Bi²⁺ or equivalent heavy ions at the current levels (160 mA in HIBALL), pulse durations, and repetition rates (5–15 Hz) needed for a power plant. The LBNL HIF program ended without building a driver-scale injector. The transition from single-shot or low-rep-rate research sources to commercial duty-cycle operation with >99% availability is entirely a paper extrapolation.
- **Missing at scale**: Commercial-rep-rate ion source with demonstrated availability target. Bi²⁺ or Cs⁺ ion source at 160 mA and 10+ Hz for >10⁸ shots. Beam emittance preservation through the full linac length at high rep rate.

---

**Target Fabrication at Commercial Scale — TRL 2–3**

- **Demonstrated**: Single-shot D-T targets for laser ICF experiments (NIF, OMEGA) have been produced in small quantities. HIF direct-drive targets are geometrically simpler (spherical, no hohlraum) but require cryogenic DT ice layers and an outer tamper. No HIF target production facility exists.
- **On paper only**: Mass-production process for DT ice-layer targets at the HYLIFE-II spec (~5 MJ coupling, ~100 mg DT fill). Cost target of <~$3/target (1990s dollars, rough estimate from HYLIFE-II economics) has not been validated against a manufacturing process. The simpler geometry of HIF direct-drive targets compared to laser ICF hohlraums is a plausible cost advantage, but no bottom-up fabrication cost analysis has been published.
- **Missing at scale**: Continuous batch production of cryogenic DT targets at 5–15 Hz throughput (9+ billion per 30-year plant life per chamber). Quality control at production rate. Automated fill-and-freeze processes. On-site DT handling and target loading infrastructure.

---

**Rep-Rated Fusion Chamber and Liquid Wall System — TRL 3–4**

- **Demonstrated**: The HYLIFE-II thick-liquid-wall concept analyzed the hydrodynamics of FLiBe jet reformation after each fusion pulse in detail, concluding that the jets could reform within the 6 Hz cycle time [hif-technology-overview.md §HYLIFE-II; hif-recent-research-compilation.md §Key Technical Parameters - Blanket Designs]. Water-surrogate experiments have validated jet dynamics at lower intensities. The HIBALL LiPb blanket concept is less experimentally advanced but has simpler geometry.
- **On paper only**: FLiBe jet system behavior under fusion-relevant yield and debris environments (350 MJ yield per shot in HYLIFE-II [hif-technology-overview.md §HYLIFE-II]). Chamber clearing and vacuum re-establishment at 5–15 Hz. First wall survival under combined neutron loading, blast loading, and thermal cycling over 30-year plant life. Integration of target injection and beam delivery with the liquid wall cycle.

> "HYLIFE-II designed for 30-year chamber lifetime with no first wall replacement due to thick flowing FLiBe jets"
> — hif-technology-overview.md, §HYLIFE-II

- **Missing at scale**: High-rep-rate liquid wall test facility with prototypical fusion yields. Demonstrated chamber clearing at 10+ Hz with activation debris. Complete liquid metal/molten salt loop at power-plant scale for either LiPb or FLiBe. Tritium extraction from FLiBe or LiPb at continuous commercial throughput.

---

**Linear Induction Accelerator Driver — TRL 4–5**

- **Demonstrated**: Linear induction accelerator technology is mature in the context of scientific instruments (electron LIAs at LLNL for flash radiography, heavy-ion LIAs at LBNL for HIF research). The HEDP program at LBNL operated multi-stage heavy-ion induction linacs. Individual induction cells and pulsed power components are commercially available. The modularity principle — hundreds of identical cells enabling factory manufacturing — is established in the induction linac literature [hif-technology-overview.md §Driver Technology].
- **On paper only**: A complete HIF driver at the power plant specification: HIBALL requires ~3 km linac delivering 10 GeV Bi²⁺ at 160 mA [dossier.md §Primary Heating]; HYLIFE-II uses a recirculating architecture with 5 MJ delivery at 6 Hz. Neither scale has been built. The transition from current (μA-scale) LIA demonstrations to mA-scale commercial drivers involves major beam quality and emittance control challenges.
- **Missing at scale**: Driver-scale induction linac demonstration at mA-class current and 5–15 Hz. Demonstrated beam transport through superconducting quadrupole arrays from source to final focus. Induction cell component lifetime at commercial rep rates. Cost validation of modular cell manufacturing at commercial quantities.

---

**Tritium Breeding Blanket and Fuel Cycle — TRL 3–4**

- **Demonstrated**: The two competing blanket concepts from HIF power plant studies — LiPb (HIBALL, TBR ~1.195 [hif-recent-research-compilation.md §Key Technical Parameters - Blanket Designs]) and FLiBe thick liquid jets (HYLIFE-II, tritium inventory 0.5 g in molten salt, 140 g in tube wall metal [hif-technology-overview.md §HYLIFE-II]) — are well-analyzed in neutronics studies. Li-6 breeding from thermal neutrons is well-understood physics. EU-DEMO Pb-17Li blanket program and the Molten Salt Reactor Experiment (MSRE at ORNL for FLiBe) provide partial experimental foundations.
- **On paper only**: Complete tritium breeding blanket integrated with IFE chamber clearing at 5–15 Hz. Tritium extraction from FLiBe at commercial throughput (the MSRE extracted 99.7% of bred tritium, but at far lower throughput than a power plant). Tritium extraction from LiPb at commercial plant rates. Validated TBR > 1 under realistic chamber geometry with penetrations for beam injection ports.

> "Tritium inventory in HYLIFE-II: 0.5 g in molten salt, 140 g in tube wall metal"
> — hif-technology-overview.md, §HYLIFE-II

- **Missing at scale**: Industrial-scale tritium extraction from LiPb or FLiBe at power plant throughput. Permeation barriers for FLiBe-facing heat exchangers. Validated tritium balance for IFE chamber with beam ports. Startup tritium procurement path (identical constraint shared with all D-T concepts).

---

**Superconducting Final Focus Magnet Arrays — TRL 5–6**

- **Demonstrated**: Superconducting quadrupole magnets are mature technology in high-energy physics (CERN, FermiLab, SNS). HIF beam transport requires arrays of LTS (NbTi/Nb₃Sn) quadrupoles historically; modern designs could use HTS [hif-technology-overview.md §Magnet Technology in Accelerator]. The LBNL and GSI programs have operated superconducting beam transport systems. Final focus quadrupoles for HIF are designed to handle emittance growth and space-charge effects of high-current ion beams, which adds complexity over collider-style focusing.
- **On paper only**: Final focus design for a commercial HIF plant providing beam-on-target focusing at mA currents with 10+ Hz rep rates. Radiation shielding for final focus elements near the fusion chamber. Component lifetime under combined neutron flux and rep-rate thermal cycling.
- **Missing at scale**: Validated radiation tolerance of final focus magnet insulation and superconductor under cumulative neutron exposure at rep-rate. Maintenance access and replacement scheme for final focus elements in a rep-rated plant.

---

**Balance of Plant (Steam Rankine Power Conversion) — TRL 7–9**

- **Demonstrated**: Conventional steam Rankine cycle is a mature commercial technology deployed in nuclear and fossil power plants. HYLIFE-II baselined on steam Rankine. Companion HYLIFE-II studies evaluated MHD + steam hybrid as an alternative [dossier.md §Energy Capture]. The thermal coupling from FLiBe or LiPb primary coolant to a steam secondary is analogous to molten salt reactor thermal coupling.
- **On paper only**: Integration with pulsed HIF thermal source at 5–15 Hz — thermal inertia of the primary loop must smooth shot-to-shot power pulses. At 6–15 Hz, pulse smoothing is more tractable than at 0.1–1 Hz (laser ICF and pulsed MIF), and the HYLIFE-II analysis considered this manageable with the FLiBe thermal mass. sCO₂ Brayton cycle has not been evaluated for HIF (no published HIF study specifies it [hif-recent-research-compilation.md §Key Technical Parameters - Energy Conversion]).
- **Missing at scale**: FLiBe-to-steam heat exchanger at full plant scale with tritium permeation barriers. Validated thermal buffering at 350 MJ/shot at 6 Hz. Integration with activated FLiBe primary loop requiring remote maintenance.

---

## Section 4: Key Materials and Supply Chain Considerations

**Heavy Ion Species (Bismuth) — Niche Supply Chain, Limited Quantities Required**

HIBALL selected Bi²⁺ at 10 GeV based on its high mass/charge ratio (~200 u/e), single natural isotope (Bi-209), and ease of ionization [hif-technology-overview.md §Driver Technology]. Lead, cesium, xenon, and mercury were also considered. Unlike structural materials consumed in bulk, the ion beam itself is recirculated in multi-pass architectures or produced continuously in single-pass linacs — the bismuth inventory in the accelerator is on the order of grams, not tons. Bismuth is a minor metal produced primarily as a byproduct of lead smelting; global production is approximately 15,000–20,000 tonnes/year, dominated by China. At the scale required for the accelerator inventory (grams to kilograms), supply is not a constraint. However, target tamper materials (lead or gold outer tamper [hif-technology-overview.md §Target Design]) and aluminum pushers require production at billions-per-year quantities — here, supply is abundant but manufacturing infrastructure to produce cryogenic spherical targets at that scale does not exist.

**FLiBe (Li₂BeF₄) — Shared Constraint with Laser IFE, But Larger Inventory**

HYLIFE-II uses FLiBe as the primary coolant, tritium breeder, and neutron shield in thick liquid jets. The FLiBe inventory in a commercial HYLIFE-II-class plant is large — sufficient to form thick (30–50 cm) flowing curtains around the entire chamber. FLiBe requires both beryllium (scarce: global production ~300 tonnes/year, dominated by Materion Corp. USA) and lithium-6 enrichment. The memory note for this analysis pipeline flags FLiBe cost data as consistently sparse across IFE concepts: "The HYLIFE-II report (Moir 1994) is the only source with FLiBe cost estimates but uses 1994 dollars." The FLiBe inventory cost for a full-scale HYLIFE-II plant is uncharacterized in modern dollars. This is a significant capital cost uncertainty shared with laser IFE concepts using FLiBe. If HIBALL's LiPb blanket is selected instead, beryllium is not required — LiPb (natural Li-Pb eutectic with Li-6 enrichment) is a more straightforward supply chain, though still requiring Li-6 enrichment capacity.

**Li-6 Enrichment — Structural Gating Constraint, No Active Production Facility Exists**

Both LiPb (HIBALL) and FLiBe (HYLIFE-II) require Li-6 enrichment for adequate TBR. Natural lithium is ~7.5% Li-6; both designs likely require moderate-to-high enrichment (50–90% Li-6) depending on blanket geometry.

No facility worldwide currently produces fusion-grade enriched Li-6 at the several-tons-per-year scale required for a power plant [transat-h2020-wp-content-uploads-2019-11-giegerich.md §Chapter 1: "As far as we know, no facility is available world-wide that could satisfy this demand"]. The entire current global commercial supply derives from Cold War stockpiles produced at the Y-12 National Security Complex (Oak Ridge, TN) between 1952–1963 using the COLEX process — 442 tonnes were produced and depleting stockpiles remain at Oak Ridge and Portsmouth. No COLEX-equivalent or successor process is in active production.

The consequence is a 53× price premium above historical production costs: the 2019 market price is **53 k€/kg** (95%-enriched Li-6) versus the 1982 COLEX production-cost estimate of ~1 k€/kg [transat-h2020-wp-content-uploads-2019-11-giegerich.md §Chapter 3]. Applied to the inventory requirement for a DEMO-class plant — approximately **52 tonnes of 90%-enriched Li-6 per 2 GW_fus device** (EU DEMO WCLL reference, from Giegerich §Chapter 2) — the Li-6 inventory cost at current market prices is on the order of **€2.5–3B per 2 GW plant**. Even at a future production-cost price of 1 k€/kg, the inventory cost would be ~€52M — still a significant LCOE input. This inventory cost is not captured in HIBALL or HYLIFE-II economics.

Establishing a new Li-6 production facility requires an estimated **~20 years of development from a 2019 baseline** (experimental work, pilot plant design and construction, process scale-up, then operational ramp-up), targeting readiness by the late 2030s to support 2040s blanket manufacturing [transat-h2020-wp-content-uploads-2019-11-giegerich.md §Chapter 7]. The ICOMAX process (Hg-amalgam column exchange, a successor to COLEX) is the leading candidate but remains at laboratory scale. This is a structural gating constraint shared with all D-T breeding concepts — not unique to HIF — but it is more severe than current analysis of any HIF concept acknowledges.

**Superconducting Magnet Materials (LTS/HTS for Accelerator) — No Critical Bottleneck**

The accelerator uses superconducting quadrupoles for beam transport. Historical designs specified NbTi or Nb₃Sn (LTS) magnets. Modern designs could substitute HTS (REBCO), though this has not been studied for HIF linac applications [hif-technology-overview.md §Magnet Technology in Accelerator]. Unlike tokamak/stellarator concepts where HTS magnet costs can be hundreds of millions of dollars per machine, the accelerator quadrupoles are individually modest magnets — the cost driver is quantity (hundreds to thousands along a km-scale linac) rather than any single large magnet. The REBCO supply chain bottleneck that affects tokamak concepts (thousands of km of tape per machine) does not apply in the same way to HIF linac quadrupoles. LTS magnets (NbTi/Nb₃Sn) for high-energy physics accelerators are commercially produced and not supply-constrained at HIF plant scale.

**Tritium — Standard D-T Startup and Self-Sufficiency Constraints**

Startup tritium requirements (~1 kg at >$35,000/g [21-spherical-tokamak-hts analysis, §Section 4]) apply identically to HIF as to all D-T concepts. HYLIFE-II's low in-system tritium inventory (0.5 g in circulating FLiBe plus 140 g in tube wall metal [hif-technology-overview.md §HYLIFE-II]) is noteworthy — the thick-liquid-wall architecture that self-renews every shot also minimizes tritium holdup in structural components. This is a modest tritium inventory management advantage relative to solid-first-wall IFE designs. Breeding self-sufficiency with HIBALL's TBR ~1.195 or HYLIFE-II's FLiBe provides adequate margin [hif-recent-research-compilation.md §Key Technical Parameters - Blanket Designs].

**No REBCO Tape Required (Unlike All HTS Tokamak/Stellarator Concepts)**

HIF has no plasma-confining magnets. The accelerator quadrupoles use conventional LTS or modest HTS, not the multi-thousand-km REBCO tape lengths required by compact tokamaks or HTS stellarators. This removes the most acute supply chain bottleneck affecting much of the fusion industry. It is a genuine supply chain advantage of the IFE approach.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Baseline LCOE (HYLIFE-II) | 6.5 cents/kWh (early-1990s dollars) | hif-technology-overview.md §HYLIFE-II | medium | ~16 cents/kWh in 2026 dollars (×2.5 CPI adjustment); single study, not independently validated |
| Scaled LCOE (HYLIFE-II at 2 GW) | 4.5 cents/kWh (early-1990s dollars) | hif-technology-overview.md §HYLIFE-II | low | ~11 cents/kWh in 2026 dollars; scaling projection within same study |
| Net electrical output — HYLIFE-II baseline | 940 MWe | hif-technology-overview.md §HYLIFE-II | medium | From early-1990s design study; no modern reconfirmation |
| Net electrical output — HYLIFE-II scaled | 1,934 MWe | hif-technology-overview.md §HYLIFE-II | low | Scaling projection within HYLIFE-II study |
| Net electrical output — HIBALL | 3.8 GWe | hif-technology-overview.md §Power Plant Designs | medium | 1985 design; large-scale multi-chamber plant |
| Recirculating power fraction — HIBALL | 15% | hif-technology-overview.md §HIBALL | medium | From 1985 HIBALL design; not updated |
| Driver wall-plug efficiency | 30–40% | hif-technology-overview.md §Driver Technology; hif-recent-research-compilation.md §Key Technical Parameters - Driver Efficiency | high | Confirmed across multiple sources; key structural advantage over laser ICF (1–15%) |
| Target gain required (1 GWe plant) | ~50–70 | hif-technology-overview.md §Target Design; hif-recent-research-compilation.md §Key Technical Parameters - Target Gain | high | Directly stated in both sources; lower than laser ICF requirement due to higher driver efficiency |
| Target gain (advanced design projection) | 130+ at 3.3 MJ driver | hif-technology-overview.md §Target Design | low | Simulation projection, not experimentally validated |
| Beam energy per shot | 3–8 MJ (HYLIFE-II: 5 MJ) | hif-technology-overview.md §HYLIFE-II; dossier.md §Primary Heating | high | Cross-confirmed; HYLIFE-II nominal 5 MJ, HIBALL up to 8 MJ |
| Yield per shot (HYLIFE-II) | 350 MJ | hif-technology-overview.md §HYLIFE-II | medium | At 5 MJ driver input, gain = 70; from 1990s design study |
| HYLIFE-II target gain (nominal) | 70 at 5 MJ | hif-recent-research-compilation.md §Key Technical Parameters - Target Gain | medium | Historical design point; modern target simulations project higher gains |
| Single-chamber repetition rate | 5–6 Hz (HIBALL: 5 Hz/chamber; HYLIFE-II: 6 Hz) | dossier.md §Repetition Rate | high | Historical designs; 2020 review targets 10–15 Hz for future reactors |
| Future target rep rate | 10–15 Hz | hif-recent-research-compilation.md §Key Technical Parameters - Repetition Rate | medium | Per 2020 arXiv review paper; not demonstrated |
| Driver direct cost (HYLIFE-II) | $570M (early-1990s dollars) | hif-technology-overview.md §HYLIFE-II | medium | ~$1.4B in 2026 dollars; only published HIF driver bottom-up estimate |
| Chamber lifetime (HYLIFE-II) | 30 years, no first wall replacement | hif-technology-overview.md §HYLIFE-II | medium | Enabled by FLiBe thick liquid wall; analytical result, not demonstrated |
| Tritium inventory in system | 0.5 g (molten salt) + 140 g (tube wall metal) | hif-technology-overview.md §HYLIFE-II | medium | Low inventory is a design feature of HYLIFE-II's FLiBe architecture |
| Tritium breeding ratio — HIBALL | ~1.195 (LiPb blanket) | hif-recent-research-compilation.md §Key Technical Parameters - Blanket Designs | medium | Analytical; no experimental validation |
| Ion species — HIBALL | Bi²⁺ at 10 GeV, 160 mA | dossier.md §Primary Heating | high | Confirmed HIBALL design specification |
| Linac length — HIBALL | ~3 km | dossier.md §Driver Technology | medium | Approximate from HIBALL design; single-pass linac |
| Fusion power per chamber — HIBALL | 2,000 MW | hif-technology-overview.md §Power Plant Designs | medium | From 1985 HIBALL design |
| Thermal conversion efficiency | [analogue] ~33–38% | [analogue — HYLIFE-II baselined on steam Rankine; comparable to historical nuclear steam plants] | low | No modern HIF design has committed to sCO₂; steam Rankine assumed |
| Total plant CAPEX | [estimated] $2–5B per GWe | [estimated from HYLIFE-II economics inflated to 2026 + analogy to comparable IFE plant studies] | low | Wide range; dominated by driver cost uncertainty; no modern cost study exists |
| Plant availability / capacity factor | 0.75 canonical (sweep: 70–90%) | scoring_framework.md §Plant availability (Pulsed IFE, D-T); analogue basis: HEP accelerator ~85–95%; IFE chamber systems more conservative ~70–80%; no HYLIFE-II published target | medium | Canonical per project policy (previously 0.80); top LCOE lever (elasticity −0.96); at 0.75, LCOE = $99.7/MWh; 5-pt swing ≈ $6/MWh; 10-pt swing ≈ $13/MWh; see Section 2 Challenge 7 and H2 |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Modern CAPEX estimate in current dollars | not-yet-sourced | blocking | All cost data from 1985–1994; no updated economic analysis exists; requires full re-baselining |
| Target fabrication cost at commercial volume | truly-unknown | blocking | No cost estimate for HIF direct-drive targets at 5–15 Hz throughput; required for OPEX model |
| Driver component replacement schedule and cost | truly-unknown | blocking | Induction cell and beam transport magnet lifetime at commercial rep rate unknown |
| Ion source lifetime and replacement at commercial duty cycle | truly-unknown | blocking | Commercial-grade ion sources for HIF do not exist; no published lifetime data |
| Regulatory cost (NRC or equivalent) | truly-unknown | important | No HIF plant has entered regulatory process; 2.2× construction cost multiplier from fission-analog scenario [21-spherical-tokamak-hts §Section 2] applies as upper bound |
| Final focus magnet lifetime under neutron exposure | truly-unknown | important | No irradiation database for final focus elements in HIF proximity |
| sCO₂ Brayton cycle applicability to HIF | not-yet-sourced | important | No published HIF study evaluates modern power conversion alternatives |
| Capacity factor target | truly-unknown | important | No HYLIFE-II or HIBALL capacity factor estimate published |
| FLiBe inventory cost for HYLIFE-II-scale plant | not-yet-sourced | important | Memory note: FLiBe cost data is consistently sparse across IFE analyses; HYLIFE-II has only 1994-dollar estimates |
| Li-6 enrichment level required | derivable | important | Can be estimated from neutronics if blanket geometry is known; sets supply chain requirements |
| O&M cost breakdown (fixed vs. variable, scheduled vs. unplanned) | truly-unknown | important | Placeholder O&M subsection — no O&M cost decomposition exists in historical HIF studies |

**O&M Placeholder Note:** Neither HIBALL nor HYLIFE-II published a detailed operations and maintenance cost breakdown separating fixed O&M, variable O&M, scheduled outages, and unplanned outage costs. The only economic output is LCOE. This is a guaranteed analysis gap. For a modern LCOE model, O&M should be estimated as: driver component maintenance (~1–2%/year of driver CAPEX), chamber/liquid wall maintenance (~0.5–1%/year), tritium processing system maintenance, and target factory operating costs. These must be treated as estimates with high uncertainty.

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | All cost data 30–40 years old; no modern CAPEX analysis in current dollars | S1, S5 | not-yet-sourced | blocking | Commission a modern reanalysis using HYLIFE-II/HIBALL as starting points; apply ARIES/PROCESS methodology; no published modern study exists |
| 2 | Target fabrication cost at 5–15 Hz commercial volume | S2, S3, S5 | truly-unknown | blocking | No HIF-specific target production cost study exists; analogize from NIF target production literature with geometry simplification adjustment |
| 3 | Driver component replacement schedule and cost at commercial rep rates | S2, S3, S5 | truly-unknown | blocking | Requires industry consultation or design study; induction linac accelerator physics literature does not address commercial rep-rated lifecycle |
| 4 | Capacity factor target and maintenance model | S2, S5 | truly-unknown | blocking | No published HIF availability analysis; apply IFE analogies with caveat; high rep rate may enable higher availability than low-rep-rate IFE |
| 5 | FLiBe coolant inventory cost at HYLIFE-II scale | S4, S5 | not-yet-sourced | important | HYLIFE-II 1994 data is the only source; requires material cost update and inventory sizing from design geometry |
| 6 | Ion source performance and lifetime at commercial duty cycle | S3, S5 | truly-unknown | important | No commercial-duty-cycle HIF ion source demonstrated; gap inherent to program hiatus |
| 7 | Final focus magnet lifetime under cumulative neutron exposure | S3 | truly-unknown | important | No irradiation database; neutron transport modeling of final focus shielding geometry needed |
| 8 | Modern target gain calculations with updated simulation codes | S2, S5 | not-yet-sourced | important | 1985–1994 target simulations; modern radiation-hydrodynamics codes (LASNEX, HYDRA) may significantly update gain projections |
| 9 | Li-6 supply chain: no active production facility at fusion scale; 53 k€/kg (2019) vs. 1 k€/kg historical; ~52 t inventory per 2 GW plant implies €2.5–3B inventory cost at current prices; ~20-year lead time to establish capacity | S4 | not-yet-sourced | important | No current production facility exists; Cold War COLEX stockpiles are the only source; inventory cost is a real LCOE input (uncaptured in HIBALL/HYLIFE-II); timeline blocks near-term commercial plants |
| 10 | sCO₂ or advanced power conversion cycle evaluation for HIF | S3 | not-yet-sourced | important | No published study; relevant given modern fusion TEA preference for sCO₂; tractable desk study |
| 11 | O&M cost decomposition (fixed/variable, scheduled/unplanned) | S2, S5 | truly-unknown | important | Historical studies report only LCOE; O&M decomposition needed for modern TEA pipeline |
| 12 | Regulatory pathway and cost for HIF commercial plant | S2 | truly-unknown | important | No HIF regulatory engagement exists; apply Stewart & Shirvan 2.2× scenario as conservative upper bound |
| 13 | Commercial company identity ("Intensity Energy") | S1 | truly-unknown | nice-to-have | Exhaustive search failed; may be a placeholder name or pre-announcement entity; cannot resolve without company disclosure |
| 14 | HIBALL or HYLIFE-II updated with modern Li-6 enrichment and beryllium supply chain constraints | S4 | not-yet-sourced | nice-to-have | Supply chain landscape has changed significantly since 1985/1994; dedicated analysis needed |
| 15 | CAS21 civil works cost for km-scale accelerator tunnel geometry | S2 | not-yet-sourced | important | Framework per-MW buildings scaling is tokamak-derived; 3 km linac tunnel is qualitatively different; likely undercosted and partly explains $92/MWh vs $162/MWh model/historical gap |

---

## Section 7: Cross-Concept Notes

**Available approved prior analysis: 21-spherical-tokamak-hts (Tokamak Energy)**

The Spherical Tokamak - HTS analysis is the only approved prior analysis available for cross-referencing. As an MFE tokamak concept, the overlap with HIF is limited primarily to D-T fuel cycle constraints and regulatory cost scenarios. No HIF accelerator, target, or chamber cost structures are shared with a tokamak design.

**Reused from 21-spherical-tokamak-hts:**

- **D-T tritium constraints**: The global tritium inventory (~25–30 kg), startup inventory requirement (~1 kg at >$35,000/g), CANDU production decline, and self-sufficiency sequencing constraint are identical for all D-T concepts [21-spherical-tokamak-hts §Section 4]. HIF's low in-system tritium inventory (0.5 g in FLiBe, 140 g in tube wall metal for HYLIFE-II) is a relative advantage in inventory management during operation, but startup procurement requirements are unchanged.
- **Regulatory cost uncertainty**: The Stewart & Shirvan 2.2× construction cost multiplier under a fission-analog regulatory framework applies to HIF as a D-T IFE facility [21-spherical-tokamak-hts §Section 2]. This is an industry-wide constraint, not concept-specific.

**Key divergences from tokamak/MFE concepts:**

HIF is structurally different from all MFE concepts in ways that materially restructure the cost model:

- **No plasma-confining magnets**: The largest single capital cost item in tokamak and stellarator designs — HTS magnet systems, costing hundreds of millions of dollars and requiring thousands of km of REBCO tape — is entirely absent from HIF. The accelerator quadrupoles are individually modest and use conventional LTS or HTS in small quantities. This represents a genuine capital cost structural advantage.
- **Driver replaces magnets as dominant cost item**: Instead of magnet capital cost, HIF LCOE is dominated by the induction linac driver ($570M in 1990s dollars for HYLIFE-II) and by per-shot consumables (targets). This creates a fundamentally different OPEX structure: there is a large per-shot operating cost (target + any consumable hardware) with no analog in steady-state MFE.
- **No superconducting magnet cryogenics**: Tokamaks and stellarators require large cryogenic systems for HTS/LTS magnets. HIF accelerators also require cryogenics for superconducting quadrupoles, but the scale is smaller (individual focusing elements, not km-scale coil systems). This eliminates a significant recurring maintenance and capital cost category.
- **IFE chamber vs. MFE plasma-facing components**: The LCOE challenge of periodic blanket module replacement (which dominates tokamak availability planning) is potentially eliminated by HYLIFE-II's liquid wall architecture, which claims 30-year chamber lifetime with no structural replacement. If validated, this would be a significant availability advantage over tokamak designs.

**Relationship to other IFE concepts in the landscape:**

Heavy ion beam ICF occupies a distinct driver technology position within IFE:

- *Laser ICF concepts* (concepts 17a, 17b, 23, 30, etc.): Laser drivers have 1–15% wall-plug efficiency vs. HIF's 30–40%. This is the foundational HIF economic argument. However, laser ICF has advanced experimentally far beyond HIF (NIF achieved ignition; no HIF driver-scale experiment exists). Target gain requirements are inversely related to driver efficiency — HIF needs only gain ~50–70 to close the energy balance where laser ICF needs gain 100–200 [hif-technology-overview.md §Target Design; hif-recent-research-compilation.md §Key Technical Parameters]. **Model limitation**: The current framework cannot quantify this advantage through parametric sweeps (eta_pin wiring inverted, +0.148 elasticity). Manual recirculating-power comparison (H3, Section 2): 15% recirc (HIF) vs. 25% recirc (laser ICF) imposes a ~13% gross generation penalty on the laser ICF plant. For a direct driver-cost-per-joule comparison, the driver capital scenario sweep should be run against the laser ICF concept (concept 30) with HIF parameters — this is the correct analytical axis until the eta_pin framework issue is resolved.
- *Projectile ICF* (concept 22, First Light Fusion): Another driver alternative with potentially high efficiency. The electromagnetic gun driver has different scaling characteristics. Both projectile ICF and HIF share the "no optics in the chamber" advantage over laser ICF.
- *MagLIF* (concept 07): MagLIF uses pulsed magnetic compression. Like HIF, it eliminates laser optics and achieves higher driver efficiency. Unlike HIF, MagLIF operates at sub-Hz to ~1 Hz (not 5–15 Hz), requires per-shot RTL consumables, and has active private-sector development.

The HIF economic model should be parameterized to enable direct comparison against laser IFE concepts at the driver cost-per-joule level — this is the primary axis on which HIF claims economic advantage.

---

## Section 8: Sources

**1. HIBALL Study (KfK-3202, Badger et al., 1985)**
- Contribution: German-US heavy ion beam power plant design study. Establishes HIBALL concept: 10 GeV Bi²⁺ at 160 mA, ~3 km linac, LiPb blanket with TBR ~1.195, 3.8 GWe net, 15% recirculating power, 2,000 MW fusion power per chamber. Primary source for large-scale HIF plant parameters.
- Location: Referenced in dossier.md §Key Sources; cited in hif-technology-overview.md

**2. HYLIFE-II Final Report (OSTI 7021072, LLNL, early 1990s)**
- Contribution: Most complete HIF power plant economic study. FLiBe thick-liquid-wall architecture, 940 MWe baseline, 6.5 cents/kWh LCOE (1990s dollars), $570M driver cost, 6 Hz single chamber, 350 MJ/shot at gain = 70, 30-year chamber lifetime, low tritium inventory (0.5 g molten salt + 140 g tube wall). Primary source for all LCOE and cost parameters.
- Location: Referenced in dossier.md §Key Sources; cited throughout hif-technology-overview.md

**3. HIF Technology Overview (iter-01/sources/hif-technology-overview.md)**
- Contribution: Compiled technical overview synthesizing HIBALL, HYLIFE-II, LBNL HIF program literature, and driver technology details. Source for cost estimates, driver efficiency, target design, magnet technology, and power plant parameters used in Section 5 parameter table.
- Location: Phase 1a source [iter-01/sources/hif-technology-overview.md]

**4. HIF Recent Research Compilation (iter-02/sources/hif-recent-research-compilation.md)**
- Contribution: Compilation covering 2020 arXiv review paper (arxiv 2005.07520) findings. Confirms 30–40% driver efficiency, 10–15 Hz rep rate target for future reactors, target gain 50–70 requirement, HYLIFE-II nominal gain of 70, FAIR status. No new private companies found.
- Location: Phase 1a source [iter-02/sources/hif-recent-research-compilation.md]

**5. arXiv 2005.07520 (2020 HIF Technology Review)**
- Contribution: Most recent peer-reviewed overview of HIF technology status. Establishes ~10–15 Hz rep rate target for commercial plants, confirms driver efficiency advantage, summarizes experimental program status.
- Location: Referenced via dossier.md §Key Sources and hif-recent-research-compilation.md

**6. Intensity Energy Search Results (iter-01/sources/intensity-energy-search-results.md)**
- Contribution: Documents exhaustive and failed attempt to verify "Intensity Energy" as an existing company. Confirms that no private company is currently pursuing heavy ion beam ICF commercially as of 2026. Establishes that the concept is analyzed here as a technology archetype, not a specific commercial entity.
- Location: Phase 1a source [iter-01/sources/intensity-energy-search-results.md]

**7. Dossier (knowledge/concept_research/25-heavy-ion-beam-icf/dossier.md)**
- Contribution: Phase 1a research summary with per-column confidence ratings, citations, and notes. Primary source for high-confidence taxonomy values (driver technology, fuel, ion species, rep rate, magnet type schema interpretation, HIBALL/HYLIFE-II design specifications).
- Location: Phase 1a dossier [knowledge/concept_research/25-heavy-ion-beam-icf/dossier.md]

**8. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-concept reference for D-T fuel cycle constraints (tritium global inventory, startup cost, CANDU production decline) and regulatory cost scenario (Stewart & Shirvan 2.2× multiplier). Not applicable for cost structure, magnet supply chain, or plasma physics parameters.
- Location: analyses/21-spherical-tokamak-hts/analysis.md

**9. Goodin et al. (2004) — IFE Target Fabrication Economics**
- Contribution: Establishes the criterion that target cost must be <10% of electricity value per target for IFE economic viability. Applied in Section 2 to frame the HIF target fabrication challenge.
- Location: Referenced in handwritten exemplar 26-laser-icf-indirect-drive.md

**10. Stewart, J. and Shirvan, K. (2022) — Regulatory Cost Framework**
- Contribution: Provides the 2.2× construction cost multiplier for fission-style regulation of fusion plants. Applied as conservative upper bound in regulatory cost discussion.
- Location: Referenced in approved analysis 21-spherical-tokamak-hts, §Section 2
