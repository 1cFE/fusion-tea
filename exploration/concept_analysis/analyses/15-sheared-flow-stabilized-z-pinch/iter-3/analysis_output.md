# D1+ Analysis: Sheared-Flow Stabilized Z-Pinch (Zap Energy)

**Concept**: Sheared-Flow Stabilized Z-Pinch — D-T fuel
**Company**: Zap Energy (Seattle, WA; founded 2017; ~$330M raised as of 2026)
**Commercial Device Series**: FuZE → FuZE-Q → FuZE-3 → FuZE-A (in preparation) → Century (engineering platform) → pilot plant
**Confinement Family**: MFE — Z-pinch (sheared-flow)

---

## Section 1: Availability of Data

**Rating: Moderate**

Zap Energy occupies an unusual transparency position: it publishes detailed plasma physics results from its FuZE device series, a technically substantive reactor engineering paper (Thompson et al., *Fusion Science & Technology*, 2023 — the "Engineering Paradigms" paper), and regular press releases on Century milestones. The Engineering Paradigms paper is the single most analytically useful public document for any private fusion startup in the Z-pinch space — it provides plasma parameters, a power balance sketch, blanket design rationale, and subsystem engineering discussion. However, it stops short of LCOE, capital cost, or capacity factor estimates, leaving the economic analysis dependent on inference and analogue assumptions.

**Peer-reviewed publications:**
The Engineering Paradigms paper (Thompson, Levitt, Nelson, Shumlak, FST 2023) establishes the reactor concept with plasma parameters (1.2–1.5 MA, 30–35 keV, 200 µs, Q > 10), a LiPb blanket design with TBR ~ 1.1, and a pulsed-power driver discussion including wall-to-plasma efficiency of ~70% [engineering-paradigms-paper-summary.md, §Driver Efficiency]. The companion Physics of Plasmas overview paper (Shumlak et al., 2023) is paywalled; details accessed through third-party summaries. The FuZE-3 gigapascal results appear to be primarily from press materials and conference abstracts as of early 2026 [fuze-3-gigapascal-results-2025.md].

**Experimental results:**
FuZE device series: demonstrated thermonuclear neutron production, independent Ti and Te measurements consistent with 30+ keV, stable sheared-flow Z-pinches at 20–40 µs duration [engineering-paradigms-paper-summary.md, §Plasma Physics]. FuZE-3 achieved electron pressures of 830 MPa and total pressures of 1.6 GPa with three-electrode architecture at densities of 3–5 × 10²⁴ m⁻³ and Te > 1 keV [fuze-3-gigapascal-results-2025.md, §FuZE-3 Plasma Parameters]. Century completed 1,080 consecutive shots into a liquid-metal-lined chamber [century-demo-system.md, §Milestones].

**Company transparency:**
Zap Energy publishes roadmap milestones, device photos, press releases, and APS DPP abstracts. The Engineering Paradigms paper is unusually transparent for a commercial venture at TRL 3–4. What is NOT published: any cost estimate, capital expenditure projection, thermal efficiency target, Q value demonstration, or plant-scale system design beyond the conceptual sketch in the FST 2023 paper.

**Independent analyses:**
No independent techno-economic analysis of the SFS Z-pinch approach has been published. The concept is sufficiently novel that no ARIES-equivalent study exists. The closest analogy studies (pulsed power drivers, IFE economics) apply imperfectly.

**Phase 1a dossier completeness:**
High confidence on all 12 taxonomy columns per the dossier [dossier.md, §Remaining Gaps]. The dossier provides a complete and well-sourced classification baseline, including the MFE reclassification (from initial MIF), energy capture method (steam Rankine), and operational mode (pulsed at ~10 Hz).

**Key data gaps limiting this analysis:**
1. Q value not experimentally demonstrated; only calculated (Q > 10 at plant conditions)
2. No published thermal efficiency, net electric output, or recirculating power fraction
3. Capital cost entirely uncharacterized in the public literature
4. Capacity factor and maintenance interval data absent
5. Electrode erosion rates at commercial duty cycles not published
6. Commercial rep rate (10 Hz) not demonstrated — Century at 0.2 Hz

---

## Section 2: Challenges in Capturing System Function

The SFS Z-pinch has a smaller parameter space than most MFE concepts — no magnets, no auxiliary heating, no divertor in the conventional sense — but its key LCOE drivers sit precisely in the whitespace between current experimental results and commercial requirements. Challenges are ranked by LCOE impact.

**1. Q > 10 not demonstrated — the model has no physics anchor (Impact: Critical)**

The Engineering Paradigms paper states:

> "At plant-relevant currents, the fusion Q (Pfusion / Pinput) is greater than 10"
> — engineering-paradigms-paper-summary.md, §Physics Assumptions

This is a calculated projection, not an experimental result. FuZE and FuZE-Q have demonstrated thermonuclear neutron production; FuZE-3 has achieved gigapascal pressures. However, the pinch lifetime required for Q > 10 is 200 µs [engineering-paradigms-paper-summary.md, §Table I], while the longest demonstrated lifetimes on FuZE are 20–40 µs. The paper explicitly acknowledges this:

> "The question remains if sheared flows will continue to be effective at stabilizing laboratory Z pinches with higher fusion performance and longer pulse durations"
> — engineering-paradigms-paper-summary.md, §Physics Uncertainties

A factor-of-5× to 10× extension in pinch lifetime is required before Q can be measured. Until demonstrated, the entire power balance (net electric, recirculating fraction, LCOE numerator) is anchored on a physics extrapolation. This is the single most constraining gap in the analysis.

**2. Rep rate scaling: 0.2 Hz → 10 Hz (Impact: Critical)**

Commercial operation requires 10 Hz. Century currently demonstrates 0.2 Hz [dossier.md, §Repetition Rate]. The 50× scaling gap affects:
- Average input power (from ~39 kW at 0.2 Hz to ~10 MWe per module)
- Electrode thermal loading and erosion rates (duty cycle × peak thermal flux)
- Liquid metal wall replenishment cycle between shots
- Pulsed power system heat rejection between shots
- Capacitor/switch component lifetimes under repetitive cycling

The path from 0.2 Hz to 10 Hz is not merely an electrical engineering problem — it requires that electrode durability, liquid metal dynamics, and gas injection timing all work reliably at the higher cadence simultaneously. No public data characterizes the failure modes expected in this regime.

**3. Electrode erosion under commercial duty cycles (Impact: High)**

The electrodes serve as both current-carrying conductors and plasma-facing components. The Engineering Paradigms paper draws analogy to commercial smelting furnace cathodes:

> "Delivering pinch currents of ~1 MA is well within the technical state of the art in the field of pulsed power"
> — engineering-paradigms-paper-summary.md, §Driver Scaling

However, commercial furnace cathodes operate in non-nuclear environments without 14 MeV neutron bombardment. At 10 Hz and microsecond-scale 1 MA discharges, electrode erosion accumulates rapidly. Replacement schedule and material cost directly enter operating costs. The Engineering Paradigms paper notes Zap Energy is "working on several damage-mitigation techniques" [§Electrode Engineering], but no erosion rate data, replacement interval, or material cost estimate appears in any public source.

**4. LiPb flowing first wall — no validated fusion analogue (Impact: High)**

The design requires liquid LiPb to cascade under gravity as the first wall, outer electrode, tritium breeder, neutron shield, and heat transfer medium simultaneously. This "quadruple-duty" design is conceptually elegant but has no equivalent in any operating fusion system. Challenges include:
- Establishing a stable, repeatable LiPb film on the inner wall surface between pulses at 10 Hz
- LiPb wettability and flow stability under pulsed electromagnetic forcing from the Z-pinch current
- In the absence of external magnets, MHD drag on flowing LiPb is absent (a major simplification vs. tokamak liquid-metal concepts), but electromagnetic induction from the pulsed current still couples to the liquid metal
- TBR of 1.1 is marginal [dossier.md, §Tritium Breeding]; a 10% reduction from design flow conditions could push TBR below 1.0 and make the plant tritium-negative

**5. Pulsed power driver cost and supply chain (Impact: Moderate–High)**

The pulsed power driver (capacitor bank + pulse-forming networks) is the primary capital cost driver for this concept — it replaces the magnet system cost that dominates tokamak economics. No public cost estimate exists for the commercial driver. Relevant data points:
- Wall-to-plasma efficiency ~70% (from Engineering Paradigms paper, combining AC-DC rectification at ~90% and modulator at ~80%)
- FuZE-Q uses ~1 MJ capacitor bank; commercial requires ~1.9 MJ/pulse electrical at Q = 10 and 19 MJ fusion/pulse
- Capacitor costs scale approximately as $/J of stored energy; industrial pulsed power systems run ~$1–10/J depending on repetition rating and pulse shape requirements [analogue from general pulsed power literature — no Zap-specific data]
- **Supply chain constraint (program-level risk):** The OSTI 2025 pulsed power challenges report quantifies the Western manufacturing gap: a single commercial plant requires 10,000–216,000 capacitors with 4–6 year delivery lead times; building 150 plants at current Western production capacity would take 125–250 years [osti-servlets-purl-2588719.md §Energy Storage]. This places supply chain maturation on a 10–20 year development timeline — comparable in commercial-schedule severity to Q demonstration and rep-rate scaling.

**6. No O&M baseline for pulsed Z-pinch operation (Impact: Moderate)**

Operating costs for a pulsed Z-pinch power plant have no industry precedent. Key cost items without data: electrode replacement, LiPb processing and resupply, pulsed power component cycling lifetimes (capacitors, switches, pulse-forming networks), gas injection and vacuum handling at 10 Hz, and tritium extraction from circulating LiPb. The modular architecture means O&M costs may scale differently than large single-unit plants — favorable for learning and parallel maintenance, unfavorable if multiple modules fail simultaneously.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk) to most mature.

---

**Physics Basis at Commercial Scale (Q > 10, 200 µs lifetime) — TRL 2**

- **Demonstrated**: Thermonuclear neutron production from FuZE at 20–40 µs; Ti = Te independently measured; FuZE-3 electron pressures of 830 MPa and total pressures of 1.6 GPa at densities 3–5 × 10²⁴ m⁻³ [fuze-3-gigapascal-results-2025.md, §Results]. Sheared-flow stabilization experimentally validated at these conditions.
- **On paper only**: Q > 10 at 200 µs and 1.2–1.5 MA — calculated but not measured [engineering-paradigms-paper-summary.md, §Q Value]. Pinch lifetime of 200 µs — a 5–10× extrapolation from demonstrated FuZE durations.
- **Missing at scale**: Experimental demonstration of stable sheared-flow Z-pinch at commercial current (1.2–1.5 MA) and commercial pinch lifetime (200 µs) simultaneously. Thermonuclear yield measurement at Q ≥ 1.

---

**LiPb Flowing First Wall / Blanket System — TRL 2–3**

- **Demonstrated**: Liquid metal (bismuth, not LiPb) circulating in Century's chamber at 0.2 Hz; 1,080 consecutive shots with flowing liquid metal demonstrated [century-demo-system.md, §Milestones]. LiPb selected as commercial design fluid; TBR ~ 1.1 calculated via Monte Carlo neutronics.
- **On paper only**: LiPb (vs. bismuth) compatibility with the commercial chamber design. Gravity-cascade flow dynamics providing stable, repeatable first-wall film between 10 Hz shots. Full integration of heat extraction, tritium breeding, neutron shielding, and electrode functions in a single flowing medium. TBR validation under realistic neutron spectrum with blanket penetrations.
- **Missing at scale**: Tritium extraction from circulating LiPb at commercial throughput. LiPb electromagnetic coupling behavior under repeated 1 MA Z-pinch pulses. First-wall erosion and LiPb contamination rates under high-Z neutron bombardment. In-situ LiPb chemistry control for tritium inventory management.

---

**High-Rep-Rate Pulsed Power Driver — TRL 3**

- **Demonstrated**: 10 Hz thyristor-based modulators demonstrated at laboratory scale [engineering-paradigms-paper-summary.md, §Driver Efficiency]. AC-DC rectification at ~90% efficiency documented. FuZE-Q operational with ~1 MJ capacitor bank at up to 1.5 MA. Wall-to-plasma efficiency of ~70% established.
- **On paper only**: Commercial-scale driver delivering 2–3 MJ/pulse electrical at 10 Hz continuously. Passive pulse-forming networks scaled to ~1.9 MJ at 10 Hz with > 10⁸ shot lifetime. Heat rejection design for driver components at 10 MW average throughput.
- **Missing at scale**: Two distinct gaps require separation:
  - *Capability gap (switching):* Current commercial Si MOSFETs and SiC devices top out at 6.5–10 kV; 4H-SiC custom devices reach 15–20 kV. Commercial Z-pinch switching requires 100–200 kV at 100–200 kA — no existing commercial switch meets this specification. The Z-pinch's 50–200 kV operating range is a relative advantage over other pulsed-fusion approaches (Marx bank drivers at 5–10 MV), but still requires a new switch technology class before lifetime durability can even be evaluated [osti-servlets-purl-2588719.md §High Voltage Switching].
  - *Lifetime gap (capacitors):* Current Z Marx bank capacitors achieve 10⁴–10⁵ shots before failure. Commercial fusion requires 10⁸–10⁹ shots — a 4–6 order-of-magnitude shortfall. This is not a modest engineering extrapolation; it is a decades-long materials development challenge for dielectric and switch components [osti-servlets-purl-2588719.md §Energy Storage]. Full driver system cost at commercial scale remains entirely uncharacterized.

---

**Electrode System (High-Duty-Cycle Cathodes) — TRL 3–4**

- **Demonstrated**: Industrial arc furnace cathodes up to 60 MW continuous operation provide engineering analogue [engineering-paradigms-paper-summary.md, §Electrode Analogy]. Century integrates "high-duty-cycle cathodes" as a test platform [century-and-fuze-a-updates-2025.md, §Abstract]. Electrode materials and damage-mitigation techniques under active development.
- **On paper only**: Electrode erosion rate and replacement interval at 10 Hz, 1 MA, D-T plasma conditions. Neutron damage to electrodes under commercial fluence. Electrode material choice for nuclear environment (typical industrial cathode materials — copper, graphite, tungsten — behave differently under 14 MeV bombardment).
- **Missing at scale**: Quantified erosion data from Century at duty cycles approaching commercial rep rates. Electrode material cost per shot and annual replacement cost estimate. Activated electrode disposal pathway (first wall components become activated waste).

---

**Tritium Breeding and Extraction — TRL 2**

- **Demonstrated**: TBR ~ 1.1 calculated from Monte Carlo neutronics for 3 m LiPb blanket; enriched Li-6 not required at this blanket thickness [dossier.md, §Tritium Breeding]. LiPb chosen over pure lithium — avoids water-reactivity of liquid Li metal and enables Pb neutron multiplication.
- **On paper only**: Engineering design that achieves TBR = 1.1 in a real flowing-blanket geometry with penetrations and supports. Tritium extraction via vacuum permeation or cold trapping from LiPb at commercial flow rates. Tritium inventory accounting in the LiPb circuit.
- **Missing at scale**: Tritium permeation rates through LiPb circuit structural materials under irradiation. Tritium extraction capacity to prevent unacceptable tritium inventory in the liquid metal. LiPb activation product management (Pb and Li activation under 14 MeV neutrons generates radioactive isotopes that complicate processing).

---

**Steam Rankine Power Conversion — TRL 7–8**

- **Demonstrated**: Conventional steam Rankine cycles are commercial technology. LiPb heat extraction via steam cycle is the established design choice per the Engineering Paradigms paper and independent summaries [engineering-paradigms-paper-summary.md, §Heat Extraction; dossier.md, §Energy Capture].
- **On paper only**: Heat exchanger coupling LiPb to steam cycle at the specific temperature and flow rates of the Zap commercial design. Thermal efficiency for LiPb outlet temperatures (LiPb solidification point ~235°C sets a floor on blanket temperature, which limits steam cycle efficiency).
- **Missing at scale**: Detailed power conversion loop design. Tritium permeation from LiPb through heat exchanger walls into steam cycle — requires tritium barrier or secondary loop.

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium (D-T fuel)**

The D-T fuel cycle is the shared supply chain challenge across all D-T fusion concepts. Commercial reactors require on-site tritium breeding with TBR > 1.0 from the blanket and external startup inventory (~1–3 kg per GWe reactor). Tritium supply from CANDU reactors (the dominant commercial source) is limited to ~1–2 kg/year globally. A fleet of SFS Z-pinch plants would face the same startup inventory constraint as any D-T fleet. TBR = 1.1 provides a ~10% margin over self-sufficiency — marginally positive, which may be insufficient if blanket availability falls below design. This challenge is identical in structure to the spherical tokamak analysis [21-spherical-tokamak-hts analysis, §Section 4].

**Lithium-6 (for tritium breeding)**

Natural lithium is ~7.6% Li-6. LiPb blankets may require enrichment to boost TBR — however, the Engineering Paradigms paper calculates TBR ~ 1.1 with natural LiPb in a 3 m thick blanket, implying enrichment is not required at this blanket depth [engineering-paradigms-paper-summary.md, §Blanket Design]. Global Li-6 enrichment capacity is limited (primarily former Soviet facilities); enrichment adds cost but may not be necessary for this design. Demand is shared with deuterium-tritium weapons programs and other fusion concepts.

**Lead (for LiPb blanket)**

Lead (Pb) is a commodity industrial metal with robust global supply. LiPb eutectic (83% Pb, 17% Li by mass) requires large volumes — a 3 m thick blanket around a ~25 m³ core implies several hundred tonnes of LiPb per module. Lead supply is not a constraint. Lead activation under 14 MeV neutrons produces Pb-204/205 and bismuth isotopes; radioactive waste management for LiPb circuit components is a long-term liability but not a supply constraint.

**Electrode materials (tungsten or refractory metals)**

Industrial arc furnace cathodes use copper, graphite, or refractory metals. Commercial Z-pinch electrodes require neutron-hard materials suitable for a nuclear environment. Tungsten is the leading candidate (high melting point, low sputtering yield, prior art in fusion first-wall applications). Global tungsten production is ~90,000 t/year, dominated by China (~80%). A multi-module plant requires modest tungsten mass, but geopolitical supply concentration is a moderate risk — shared with tokamak tungsten divertor programs.

**Capacitors and high-voltage switches (pulsed power driver) — Program-Level Supply Chain Risk**

The pulsed power driver is the unique supply chain item for this concept, and published data from the OSTI 2025 pulsed power challenges report (LLNL-JRNL-2001600) establishes the constraint at a severity comparable to Q demonstration or tritium supply:

- **Capacitors per plant**: A single commercial Z-pinch plant requires 10,000–216,000 high-voltage capacitors [osti-servlets-purl-2588719.md §Energy Storage].
- **Delivery lead times**: 4–6 years per order at current production capacity.
- **Fleet buildout**: Building 150 plants to serve the United States would require 125–250 years at current Western manufacturing capacity. Labor remains "a major fraction of capacitor cost at the present time" [osti-servlets-purl-2588719.md §Energy Storage].
- **Lifetime gap**: Current Z Marx bank capacitors achieve 10⁴–10⁵ shots; commercial fusion requires 10⁸–10⁹ shots — a 4–6 order-of-magnitude shortfall requiring sustained materials R&D.
- **Switch capability gap**: Current commercial SiC devices reach 6.5–15 kV. Z-pinch switches must operate at 50–200 kV, 100–200 kA — a specification no commercially available switch meets. This is a capability problem (wrong technology class), not merely a durability problem. Note that the Z-pinch's 50–200 kV range is a relative advantage over Marx-bank-driven approaches (5–10 MV), but the gap to commercial availability remains large.
- **OSTI roadmap timeline**: A new material or component class developed today takes 10–15 years to reach manufacturing scale. The pulsed power supply chain is on a 10–20 year maturation trajectory before commercial Z-pinch deployment is credible [osti-servlets-purl-2588719.md §Workshop Outcomes].

The absence of HTS tape eliminates the most costly material in compact tokamak designs, but capacitor and switch supply chain development is the structural supply chain challenge this concept substitutes in its place. This is not a "specialty market" scaling problem — it is a program-level constraint requiring coordinated government and industry investment over decades.

**Materials not required (vs. conventional tokamak):**
- REBCO HTS tape — entirely absent; eliminates the most costly and supply-constrained material in compact tokamak designs
- Cryogenic systems (no superconducting magnets)
- Beryllium (no Be first wall; LiPb is the first wall)
- NBI beam dumps, gyrotrons, or RF launchers

The absence of HTS tape is a material simplification that substantially de-risks the supply chain relative to spherical tokamak and compact tokamak concepts.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Fusion thermal power per core | ~200 MWt | engineering-paradigms-paper-summary.md §Design Parameters/Table I | medium | "Nominal maximum thermal power: 200 MW"; 19 MJ/pulse × 10 Hz = 190 MWt consistent |
| Fusion energy per pulse | 19 MJ | engineering-paradigms-paper-summary.md §Design Parameters | medium | Plant design point; not experimentally demonstrated |
| Target Q (fusion gain) | > 10 | engineering-paradigms-paper-summary.md §Physics Assumptions | low | Calculated; never demonstrated at any scale |
| Rep rate (target) | 10 Hz | zap-energy-website-how-it-works.md §Commercial Design; dossier.md §Repetition Rate | high | Commercial target; Century at 0.2 Hz |
| Wall-to-plasma efficiency | ~70% | engineering-paradigms-paper-summary.md §Driver Efficiency | medium | 90% (AC-DC) × 80% (modulator); demonstrated at subscale |
| Pinch current (commercial) | 1.2–1.5 MA | engineering-paradigms-paper-summary.md §Table I | medium | Design point; highest demonstrated on FuZE-Q |
| Pinch radius | 0.15 mm | engineering-paradigms-paper-summary.md §Table I | medium | Design point only |
| Pinch length | 0.5 m | engineering-paradigms-paper-summary.md §Table I | medium | Constant across development stages per paper |
| Plasma lifetime (commercial) | 200 µs | engineering-paradigms-paper-summary.md §Table I | low | Design requirement; FuZE demonstrated 20–40 µs |
| Electron density (commercial) | 1.5 × 10²⁶ m⁻³ | engineering-paradigms-paper-summary.md §Table I | low | Design point; extrapolated from FuZE |
| Plasma temperature | 30–35 keV | engineering-paradigms-paper-summary.md §Design Parameters | medium | Consistent with FuZE measurements; required for DT yield |
| Core volume | 25 m³ | engineering-paradigms-paper-summary.md §Design Parameters | medium | Much smaller than comparable pulsed concepts |
| Core diameter (approx.) | ~3 m | engineering-paradigms-paper-summary.md §Design Parameters | medium | Implies compact geometry |
| Module net electric output | ~50 MWe | century-demo-system.md §Commercial Scale | low | Century described as "close to eventual size of single module producing 50 MWe"; [inferred] |
| Blanket TBR | ~1.1 | engineering-paradigms-paper-summary.md §Blanket Design; dossier.md §Tritium Breeding | medium | Calculated for 3 m LiPb blanket; marginal positive |
| LiPb blanket thickness | ~3 m | dossier.md §Tritium Breeding | medium | For TBR ~ 1.1 and biological shielding |
| Driver input power (inferred) | ~27–30 MWe/module | [inferred: 200 MWt / Q(10) = 20 MWt plasma input; ÷ 0.70 efficiency = 28.6 MWe; at 10 Hz continuous] | low | Derivation: fusion power from §Table I, Q from §Physics, efficiency from §Driver |
| Gross electric per module (inferred) | ~60–70 MWe | [inferred: 200 MWt × η_thermal (~33% steam Rankine)] | low | Steam Rankine efficiency assumed 30–35%; cycle design unpublished |
| Net electric per module (inferred) | ~35–50 MWe | [inferred: gross electric minus driver recirculating power ~28–30 MWe] | low | Consistent with Century "50 MWe module" claim if efficiency is ~37% |
| Recirculating power fraction (inferred) | ~40–55% | [inferred: driver power / gross electric; Q = 10 assumption] | low | High recirculating fraction is a key LCOE risk; depends strongly on Q |

**Notes on recirculating power:**
The recirculating fraction is highly sensitive to Q. At Q = 10 and 70% driver efficiency, recirculating power is ~14% of fusion power; as a fraction of gross electric (~33% thermal efficiency), recirculating fraction ≈ 43%. If Q = 5, recirculating fraction climbs to ~85% of gross electric, making net output negligible. This is the key lever — every doubling of Q halves the recirculating fraction.

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Q value (experimental) | truly-unknown | blocking | Must reach FuZE-Q; no published result |
| Thermal conversion efficiency | proprietary | blocking | Steam Rankine assumed; exact cycle design unpublished |
| Capital cost (total plant $/kWe) | proprietary | blocking | No estimate in any public source |
| Capacity factor | truly-unknown | blocking | No operational plant; maintenance intervals uncharacterized |
| Electrode erosion rate and replacement cost | truly-unknown | important | No nuclear-environment erosion data |
| Driver cost ($/J stored) at commercial scale | not-yet-sourced | important | Industrial pulsed power cost data exists but not specific to this application |
| LiPb pumping power | derivable | important | Can estimate from flow velocity and hydraulic resistance |
| Annual LiPb replacement volume | derivable | important | Activation buildup sets a circuit turnover requirement |
| Fixed O&M ($/MWh) | truly-unknown | important | No analogue for pulsed Z-pinch at commercial scale |
| Plant lifetime | truly-unknown | nice-to-have | Electrode, blanket, and driver component lifetimes unknown |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Q > 10 not demonstrated; commercial power balance anchored on calculation | S2, S5 | truly-unknown | blocking | FuZE-Q results when published; FuZE-A commissioning results |
| 2 | Pinch lifetime of 200 µs not demonstrated (5–10× extrapolation from FuZE) | S2, S3 | truly-unknown | blocking | FuZE-Q / FuZE-A experimental results |
| 3 | Capital cost estimate entirely absent | S5 | proprietary | blocking | No public source; requires Zap Energy disclosure or independent study |
| 4 | Capacity factor and maintenance interval data | S5 | truly-unknown | blocking | Century long-run testing; no published target |
| 5 | Rep rate scaling from 0.2 Hz (Century) to 10 Hz (commercial) | S2, S3 | truly-unknown | blocking | Century program milestones; no timeline published |
| 6 | Electrode erosion rate under nuclear duty — replacement interval and cost | S3, S5 | truly-unknown | important | Century electrode data; no nuclear-environment data exists |
| 7 | Thermal conversion efficiency (steam Rankine cycle design) | S5 | proprietary | important | Engineering Paradigms paper implies Rankine; no efficiency stated |
| 8 | LiPb flowing first-wall stability at 10 Hz — validated analogue absent | S2, S3 | truly-unknown | important | Century liquid metal data (bismuth to date; LiPb next) |
| 9 | Tritium extraction from LiPb at commercial throughput | S3, S4 | truly-unknown | important | No Z-pinch-specific TBR validation experiment; EU-DEMO analogue partial |
| 10 | Driver cost at commercial scale ($/J, $/MWe) | S4, S5 | not-yet-sourced | important | Industrial pulsed power cost studies; NIF/Z machine cost analogy |
| 11 | LiPb activation and processing requirements | S4 | truly-unknown | important | Requires neutronics + chemistry modeling; no Zap publication |
| 12 | Recirculating power fraction (depends on Q) | S5 | derivable | important | Derives directly once Q is measured |
| 13 | Fixed vs. variable O&M breakdown | S2 | truly-unknown | important | No fusion Z-pinch precedent; pulsed machine analogy (ICF) partial |
| 14 | Pulsed power component lifetime and switch capability: capacitors at 10⁴–10⁵ shots vs. 10⁸–10⁹ required (4–6 OOM); no commercial switch meets 50–200 kV, 100–200 kA specs | S3, S4 | truly-unknown | blocking | New switch technology class required before lifetime can be tested; OSTI 2025 roadmap projects 10–15 year materials maturation timeline |
| 15 | LiPb pumping power requirements | S5 | derivable | nice-to-have | Estimable from blanket geometry and flow velocity |

---

## Section 7: Cross-Concept Notes

**Reused from 21-spherical-tokamak-hts:**
- Tritium supply chain analysis (D-T startup inventory, CANDU production constraint, global Li-6 enrichment capacity) applies without modification to the SFS Z-pinch. Both are D-T concepts targeting TBR just above 1.0.
- Recirculating power framework (definition, impact on LCOE denominator, sensitivity to Q) is structurally identical. For the ST-HTS, recirculating power is dominated by ECRH; here it is dominated by pulsed power driver.
- Steam Rankine as baseline thermal cycle, with tritium permeation through heat exchanger walls as a design concern, is shared.

**Key divergences from ST-HTS:**
- **No HTS magnets**: The dominant capital cost driver for the ST-HTS (and all compact tokamak variants) is entirely absent in the Z-pinch. This is the single largest structural difference in cost architecture. The Z-pinch substitutes pulsed power driver (capacitors, switches, PFNs) as the dominant capital item.
- **No cryogenic plant**: No liquid helium, no cold mass, no quench protection systems. Simplifies plant design and eliminates a low-TRL-in-fusion subsystem.
- **LiPb as first wall (not separate blanket)**: In the ST-HTS, a separate outboard-only liquid Li blanket sits behind a plasma-facing first wall material. In the Z-pinch, LiPb is simultaneously the electrode, first wall, blanket, and shield. This is more elegant but means any blanket failure mode (flow interruption, LiPb contamination) directly disrupts plasma operation.
- **Pulsed operation regime**: Both concepts are pulsed, but the regimes are completely different. ST-HTS pulses are 15+ minutes with inductive current drive. Z-pinch pulses are 200 µs at 10 Hz. The thermal energy storage and grid integration challenge for the Z-pinch is far more aggressive — 100 ms between pulses rather than minutes.
- **Modularity**: The Z-pinch commercial plant is explicitly multi-module (50 MWe/module, multiple modules per plant). The ST-HTS is a single-unit design at 450–750 MWe net. Multi-module architecture improves O&M flexibility but introduces coordination complexity and common-mode failure risk.
- **Regulatory pathway**: SFS Z-pinch geometry and pulsed power driver have no licensed precedents. The novel first-wall design (LiPb flowing electrode) and the absence of external containment magnets may require new licensing frameworks. This is a shared challenge with all private fusion ventures but is more acute for a design that deviates more from the ITER reference pathway.

---

## Section 8: Sources

1. **Thompson, Levitt, Nelson, Shumlak — "Engineering Paradigms for SFS Z-Pinch Fusion Energy" (FST, 2023)**
   - Primary engineering reference for reactor concept, plasma parameters, blanket design, driver efficiency, and Q projections
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/engineering-paradigms-paper-summary.md`

2. **Zap Energy — Century Demo System (FST, 2025 / press release)**
   - Commercial architecture (modular 50 MWe, double-decker bus scale), Century engineering milestones, liquid metal integration, electrode durability program
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/century-demo-system.md`

3. **Zap Energy — FuZE-3 Gigapascal Results (Nov 2025)**
   - Latest plasma performance data: 830 MPa electron, 1.6 GPa total; 3–5 × 10²⁴ m⁻³ density; Te > 1 keV; three-electrode architecture
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-02/sources/fuze-3-gigapascal-results-2025.md`

4. **FuZE-Q and FuZE-3 Overview**
   - FuZE device series specs and neutron yield context; FuZE-3 design rationale (three electrodes for independent compression/acceleration)
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/fuze-q-and-fuze-3.md`

5. **Zap Energy — How It Works (website)**
   - Commercial parameters (D-T fuel, 10 Hz, no-magnet cost claims, LiPb wall description)
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-01/sources/zap-energy-website-how-it-works.md`

6. **Century and FuZE-A Updates (2025)**
   - Parallel physics/engineering strategy; Century integrates repetitive pulsed power, high-duty-cycle cathodes, and liquid metal walls; FuZE-A as next device
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-02/sources/century-and-fuze-a-updates-2025.md`

7. **Phase 1a Dossier — Sheared-Flow Stabilized Z-Pinch**
   - High-confidence taxonomy classification; MFE re-classification rationale; energy capture and operational mode cross-checking
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/dossier.md`

8. **D1+ Analysis: Spherical Tokamak - HTS (prior approved analysis)**
   - Cross-concept reference for tritium supply chain, recirculating power framework, steam Rankine assumption, and pulsed operation LCOE challenges
   - `/exploration/concept_analysis/analyses/21-spherical-tokamak-hts/analysis.md`

9. **OSTI — "Challenges and Gaps in Pulsed Power for Fusion" (LLNL-JRNL-2001600, 2025)**
   - Quantitative supply chain constraints: 10k–216k capacitors/plant, 4–6 year lead times, 125–250 year fleet buildout timeline; component lifetime gap (10⁴–10⁵ demonstrated vs. 10⁸–10⁹ required); switching technology capability gap (SiC at 6.5–15 kV vs. 50–200 kV Z-pinch requirement); 10–20 year maturation roadmap
   - `/knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/iter-03/sources/osti-servlets-purl-2588719.md`
