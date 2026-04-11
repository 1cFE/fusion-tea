# D1+ Analysis: HTS Compact Tokamak (Commonwealth Fusion Systems)

**Concept**: HTS Compact Tokamak — D-T fuel
**Company**: Commonwealth Fusion Systems (Cambridge, MA)
**Devices**: SPARC (burning plasma experiment, under construction), ARC (conceptual power plant)
**Confinement Family**: MFE — Compact Tokamak

---

## Section 1: Availability of Data

**Rating: Rich**

The CFS HTS compact tokamak is among the most extensively documented private fusion concepts. CFS emerged from MIT's Plasma Science and Fusion Center, and the academic lineage shows: key design choices are published in peer-reviewed journals rather than press releases.

**Primary engineering references:**
The 2015 Sorbom et al. paper "ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets" (*Fusion Engineering and Design* 100, 378–405) remains the foundational ARC conceptual design document. It provides reactor dimensions, magnet specifications, blanket engineering, cost analysis at the component level, and a structured R&D gap inventory [arc-reactor-specifications.md §1–7]. A companion 2020 J. Plasma Physics special issue covers SPARC physics basis papers including the ICRF heating system [sparc-icrf-heating-paper.md] and plasma performance (Creely et al. 2020, not directly ingested but cited in dossier). The Phase 1a dossier achieved high confidence on all 12 differentiation columns; the single medium-confidence item (energy capture / thermal cycle choice) is confirmed as unpublished rather than unresolved.

**Power conversion analysis:**
An independent 2020 thermodynamic study (ingested as arc-power-conversion-studies.md) compared three power conversion cycles for ARC — supercritical Rankine steam, sCO₂ Brayton, and helium Brayton — using the full ARC heat load (645 MWth to PCS). Colliva et al. (2024, MDPI) independently reached the same conclusion that supercritical Rankine is the most promising option. Together these provide credible efficiency estimates.

**Technology milestone disclosures:**
CFS demonstrated a 20 T large-bore HTS magnet in September 2021, directly validating the core magnet bet. In November 2025, Tokamak Energy's Demo4 validated a complete 18-coil HTS system at 11.8 T in full tokamak configuration. As of January 2026, the first of SPARC's 18 D-shaped TF coils had been installed, with SPARC construction expected to complete by end of 2026 and first plasma in 2027 [cfs-2025-2026-updates.md].

**Independent techno-economic analyses:**
Araiinejad & Shirvan (2025), "Techno-economic Analysis of Deuterium-Tritium Magnetic Confinement Fusion Power Plants" (*Applied Energy* 401, 126567) applies directly to the concept family and quantifies the regulatory cost impact. The ARIES-AT and ARIES-CS studies provide plant-level CAS cost benchmarks against which ARC can be compared. Brown (2018, *IEEE Transactions on Plasma Science*) provides a three-way cost decomposition across spherical tokamak, standard tokamak, and stellarator for component-level cost structure. The PROCESS UKAEA system code includes tokamak models for self-consistent design point generation.

**Key data gaps limiting this analysis:**
1. No published commercial capital cost estimate for ARC. The 2015 paper provides fabricated component costs totaling $5.56B, but this covers only vacuum vessel, blanket, and magnet/structure — not balance of plant, land, indirect costs, or construction financing.
2. ARC's current design has evolved: the 2015 paper shows 190–261 MWe depending on operating phase, while 2025-2026 CFS communications describe a 400 MWe plant. The updated design parameters are not publicly documented.
3. Capacity factor is not stated anywhere in published CFS/ARC materials.
4. O&M cost breakdown (scheduled maintenance, unplanned outage, remote handling labor) is absent from all published sources.

---
[1] arc-reactor-specifications.md, §6 "Identification of Cost Feasibility": "The cost of ARC is approximately one-third the cost of the 8 T ARIES-RS (∼$14 B)"
[2] cfs-2025-2026-updates.md: "Just installed the first of 18 high-temperature, D-shaped superconducting magnets"
[3] sparc-icrf-heating-paper.md, §Introduction: "the only method that can penetrate the SPARC plasmas, heat fusion ions and can be built cost-effectively using existing technology"

---

## Section 2: Challenges in Capturing System Function

The following challenges are ranked by impact on LCOE uncertainty:

**1. Magnet system cost dominance — very high impact**
The magnet system (TF coils, PF coils, structure) accounts for approximately $5.1–5.2B of ARC's $5.56B total fabricated cost — roughly 92% of the total [arc-reactor-specifications.md §6]. The materials cost is only $160–260M (REBCO tape + structural steel); the remainder is fabrication labor and tooling. This means the magnet cost is simultaneously LCOE's largest driver and most uncertain line item. REBCO tape prices in 2014 ranged from $36 to $198/m — a 5.5× spread that, when applied to the 5,730 km required, spans $206M to $1.13B in materials alone. Reaching commercial viability likely requires tape prices to fall to ~$10/kA-m — a target that requires production scale-up of 1–2 orders of magnitude from current global capacity. The model must treat REBCO price as a sensitivity parameter with at least a 5× range.

**2. Capacity factor — high impact, structurally uncertain**
ARC's design targets 9 full-power years (FPY) of operation before the TF coils reach their REBCO neutron fluence limit [arc-reactor-specifications.md §5]. This establishes a hard upper bound on plant lifetime without magnet replacement, but annual capacity factor (the fraction of calendar time at full power) is nowhere stated in published materials. For a quasi-steady tokamak (pulse length tens of minutes, with brief interruptions), capacity factor depends on: (a) divertor and first-wall replacement frequency, (b) FLiBe blanket maintenance access, (c) remote handling system reliability, and (d) unplanned outage rate. The handwritten exemplar (01-hts-compact-tokamak.md) identifies remote handling and blanket maintenance as TRL 5–6 — not yet demonstrated at power-plant availability. A 2× swing in capacity factor (50% vs. 90%) translates to a 2× swing in LCOE for a CAPEX-heavy concept.

**3. FLiBe blanket behavior under fusion conditions — high impact**
The ARC paper explicitly calls out three unresolved FLiBe data gaps: tritium extraction timescales ("few experiments have been built to assess the turn-around time for tritium extraction from FLiBe"); MHD effects on heat transfer under ARC's 9.2 T field; and radiation-assisted corrosion of Inconel-718 in FLiBe [arc-reactor-specifications.md §7]. Any of these could force blanket redesign:
- Slow tritium extraction raises on-site inventory (regulatory implications) or constrains burns to shorter durations
- MHD flow disruption reduces heat transfer, potentially requiring higher flow rates and more pumping power
- Radiation-accelerated Inconel corrosion would require material substitution, affecting blanket fabrication cost

> "Few experiments have been built to assess the turn around time for tritium extraction from FLiBe; this must be experimentally demonstrated, as the on-site inventory limits will be set by regulatory requirements."
> — arc-reactor-specifications.md, §7 "Identification of R&D Requirements"

**4. I-mode operating regime extrapolation — medium impact**
ARC's physics baseline relies on I-mode confinement — an operating regime demonstrated on C-Mod at parameters up to 0.2–0.5 MW/m²/n₂₀ and fields up to 6 T. ARC's operating point is 0.55 MW/m²/n₂₀ at 9.2 T, exceeding published I-mode range [arc-reactor-specifications.md §7]. If I-mode is not accessible at ARC parameters, the required heating power would increase substantially, raising recirculating power fraction and reducing Qe.

**5. LHCD system development — medium impact**
ARC requires a 25 MW 8 GHz lower-hybrid current drive system. The paper notes that only 6 GHz klystrons have proven reliable; 8 GHz at the required power level has not been demonstrated [arc-reactor-specifications.md §7]. LHCD is needed for non-inductive sustainment — without it, ARC would need to rely entirely on bootstrap current (currently modeled at 63%), which may be insufficient for the required current profile.

**6. Regulatory framework — medium impact, shared with all D-T concepts**
Araiinejad & Shirvan (2025) demonstrate that fission-style nuclear regulation produces a 2.2× markup on building costs, increases indirect cost percentages, and reduces capacity factor — effects that together can nearly double overnight capital cost and quadruple LCOE spread relative to the base estimate. The NRC's 2023 decision to regulate fusion under 10 CFR Part 30 (byproduct material rules) rather than Part 50 (reactor rules) is favorable, but detailed rulemaking is incomplete. This is a shared uncertainty across all D-T fusion concepts.

**7. O&M costs — low-to-medium impact, data absent**
No published estimate exists for ARC's annual O&M cost breakdown. For a CAPEX-dominated concept, O&M is not the primary LCOE driver, but remote handling labor, tritium handling infrastructure, and component replacement (first wall, divertor, possibly blanket) are non-trivial. Per cross-concept analysis guidance, a placeholder O&M subsection is included in Section 5 with analogue estimates.

---

**Key Testable Hypotheses**

The following propositions organize the model's primary questions as testable conditional claims rather than open uncertainties:

**Hypothesis 1 — REBCO cost trajectory (necessary condition for cost competitiveness):**
ARC's magnet system becomes cost-competitive with ARIES-RS–class LTS designs if and only if REBCO tape cost falls to ≤$10/kA-m AND fabricated magnet cost per tonne scales to ARIES-class levels (~$1.06M/tonne). As of 2025, PLD-REBCO manufacturers sell tape at ~$20/m (~$100/kA-m at >200 A/4mm, 20 K, 20 T) [sciencedirect-science-article-pii-s2772830725000390.md §Introduction] — below the entire 2014 range ($36–198/m, equivalent to ~$144–792/kA-m), but still ~10× above the commercial target. The implied trajectory — from $144–792/kA-m in 2014 to ~$100/kA-m in 2025 — reduces but does not eliminate the REBCO cost risk; the gap to $10/kA-m is ~1.5–8× smaller than the 2014 range implied. At 2025 prices, magnet materials cost remains substantially above the commercial target [arc-reactor-specifications.md §4.1, §6.2]. This hypothesis drives the most important sensitivity in the cost model; the REBCO price axis should span at least 10× the commercial target.

**Hypothesis 2 — Capacity factor dominance (primary LCOE lever):**
For ARC's cost structure (>90% of known fabricated cost in capital, O&M not yet quantified), LCOE scales approximately inversely with capacity factor. The concept achieves sub-$100/MWh LCOE only if capacity factor exceeds approximately 70–80% on a sustained, multi-year basis — a level not yet demonstrated for any fusion device. A 2× swing in capacity factor (50% → ~85%) dominates LCOE more than any other parameter at near-target REBCO prices. The model should treat capacity factor as the primary output sensitivity, not a fixed assumption.

**Hypothesis 3 — I-mode economic threshold (not just physics threshold):**
The ARC paper shows that if I-mode is not achieved and the plasma falls back to standard H-mode (H₈₉ = 2.2), fusion power drops from 525 MW to ~200 MW while still meeting the FNSF neutron flux mission [arc-reactor-specifications.md §3.5]. For a power plant, this reduces net electric output from ~261 MWe to approximately 80–100 MWe — pushing $/kWe up by 2.5–3× with identical capital cost. Physics success does not imply economic success: I-mode at the ARC design point is a necessary condition for economic viability, not just a performance target.

**Hypothesis 4 — FOAK-to-NOAK cost trajectory (step-function risk, not continuous sensitivity):**
ARC's $5.56B fabricated component cost uses NOAK assumptions — mass-proportional scaling ($1.06M/tonne) benchmarked against prior conceptual designs with implicit manufacturing learning. The first commercial ARC plant faces First-of-a-Kind (FOAK) premiums that are not continuous sensitivity parameters but step-function risks concentrated in plants 1–3 of the deployment sequence. The CATF International Working Group methodology framework (arxiv-2602-19389 §2.1.5) explicitly cites FOAK commercial fusion plants in the 150–200 $/MWh LCOE range, versus 60–100 $/MWh for NOAK plants — a 2–3× gap driven by manufacturing complexity, quality assurance rework, and supply chain immaturity for novel components. This gap is well-established in advanced nuclear analogues (NCSX program experienced severe underestimation of manufacturing complexity; arxiv-2602-19389 §2.1.3). The cost model must treat FOAK/NOAK as a discrete scenario branch alongside the regulatory multiplier: both are step-function uncertainties tied to specific positions in the deployment sequence and do not average out over the sensitivity range. The $/kWe figure inferred from the $5.56B nuclear island cost (~$21,300–29,200/kWe) therefore represents the NOAK floor, not the first-plant expectation.

---

## Section 3: Maturity of Key Subsystems and Components

Presented in ascending order of maturity (least mature first).

---

**Integrated FLiBe Blanket (breeder / coolant / shield) — TRL 3–4**

- **Demonstrated**: Small-scale tritium breeding in lithium-bearing materials; FLiBe thermophysics characterized at lab scale; neutron irradiation tests in fission reactors up to ~30–50 dpa. ITER Test Blanket Module designs are in detailed engineering (PDR expected 2026, but ITER TBMs use different blanket chemistries). ARC's specific FLiBe configuration (liquid immersion, magnetic field-exposed flow) has no prototype.
- **On paper only**: Full-scale integrated FLiBe blanket module operating under simultaneous neutron flux, magnetic field, FLiBe flow, and tritium extraction load. MHD behavior of FLiBe under 9.2 T field — the Sorbom 2015 paper notes that initial computational work suggests MHD effects can be neglected, but "detailed investigation is needed" [arc-reactor-specifications.md §7].
- **Missing at scale**: 14 MeV neutron qualification of FLiBe tritium extraction system at kg/day rates; demonstration of Inconel-718 compatibility with FLiBe under combined heat flux + radiation; FLiBe purification and redox control at industrial scale; integrated test at relevant flow velocity (≤0.2 m/s design limit).

> "The effect of the strong background magnetic field on the magnetohydrodynamics of FLiBe flow, turbulence, and heat transfer... can be neglected based on initial computational work, but requires detailed investigation."
> — arc-reactor-specifications.md, §7

---

**Tritium Fuel Cycle & Extraction — TRL 4–5**

- **Demonstrated**: Lab-scale tritium handling loops, permeation barriers; JET and TFTR handled gram-scale D-T. FLiBe tritium solubility and release chemistry characterized at small scale.
- **On paper only**: Closed-loop tritium extraction from FLiBe at kg/day rates with <1% losses; on-site tritium processing plant integrated with molten-salt chemistry.
- **Missing at scale**: Demonstrated tritium extraction turn-around time from FLiBe sufficient to meet ARC's tritium breeding cycle requirements; tritium accountability system meeting regulatory inventory limits without excessive storage; kg/year scale operations.

---

**Remote Maintenance System — TRL 5–6**

- **Demonstrated**: ITER remote handling prototypes and full-scale mock-ups for blanket/divertor exchange; industrial robotics for highly activated environments developed at ITER scale. ARC's demountable TF coil joints are designed to permit coil extraction — a feature specifically enabling maintenance access that LTS-based tokamaks lack.
- **On paper only**: Reliable high-availability remote maintenance at power-plant operating tempo (>80% capacity factor requires maintenance windows on the order of hours to days, not weeks).
- **Missing at scale**: Radiation-hardened robotics with multi-year service life in ARC's neutron environment; remote demountable coil joint operations under ARC's 23 T peak field conditions.

---

**Divertor — TRL 5–7**

- **Demonstrated**: ITER-style tungsten monoblock divertors tested at >10–20 MW/m² in WEST, GLADIS, and DTT; detached/radiative divertor operation on DIII-D, JET, AUG; ARC's compact geometry increases heat flux per unit divertor area relative to larger machines.
- **On paper only**: Advanced ARC-compatible divertor concepts (potentially liquid metal or advanced tungsten alloys) at ARC's neutron flux and compact geometry.
- **Missing at scale**: Long-term (multi-year) tungsten divertor survival at ARC's heat flux with simultaneous 14 MeV neutron damage; remote divertor replacement system at ARC's replacement frequency.

---

**HTS Magnets (REBCO, 20–23 T) — TRL 6–8**

CFS is further advanced on this subsystem than the generic class.

- **Demonstrated**: 20 T large-bore HTS test coil validated by CFS (September 2021) — directly matching ARC's operating point. SPARC TF coil No. 1 (of 18) installed January 2026 [cfs-2025-2026-updates.md]. Two magnet architectures: NINT (stacked steel-plate HTS) for TF coils; PIT VIPER cable for pulsed PF/CS coils (announced 2024). Critical current density: "one to two orders of magnitude higher than Nb₃Sn at 23 T" [arc-reactor-specifications.md §4.1].
- **On paper only**: REBCO joint performance at reactor-level field + stress + neutron flux simultaneously. The 2015 paper notes joints were only bench-top tested at 77 K without background field [arc-reactor-specifications.md §7]. Quench detection and protection at 20 K operating temperature.
- **Missing at scale**: Radiation-hardened insulation for REBCO coils; km-scale REBCO production with consistent Jc (>150 MA/cm² at 20 K, 20 T); structural delamination behavior under cyclic high-field load over 9 FPY lifetime; supply chain for thousands of km/year per plant.

> "REBCO has never been tested to failure in a fusion-relevant environment. Fluence experiments only establish conservative limits."
> — arc-reactor-specifications.md, §7

---

**ICRF Heating System — TRL 6–8**

- **Demonstrated**: 120 MHz ICRF systems validated on Alcator C-Mod (MIT predecessor to SPARC/CFS). Single-pass absorption 60–97% for D-T(³He) heating across ARC parameter space [sparc-icrf-heating-paper.md §2]. Multiple-pass absorption >80% over broad parameter range. ICRF selected specifically for "cost-effectiveness using existing technology" — no new high-power tube development required [sparc-icrf-heating-paper.md §Introduction].
- **On paper only**: Full 25 MW coupled power from 12 four-strap in-vessel antennae in the SPARC geometry; performance under D-T neutron flux.
- **Missing at scale**: Remote maintenance of in-vessel antennae after D-T activation (paper notes this is "significantly more challenging" than insertable designs); real-time impedance matching during ELM bursts; tetrode tubes qualifying at ≥2 MW at 120 MHz with VSWR ≤1.3.

---

**Vacuum Vessel & In-Vessel Structures — TRL 7–8**

- **Demonstrated**: ITER vacuum vessel sectors manufactured and welded at full scale. ARC's double-walled design using Inconel-718 is conventional engineering scaled to compact geometry.
- **Missing at scale**: Long-term Inconel-718 behavior under combined neutron irradiation and FLiBe exposure; integration with demountable TF coil joints at power-plant scale.

---

**Cryogenics & Thermal Management — TRL 7–8**

- **Demonstrated**: Large-scale helium refrigeration at ITER scale. ARC operates REBCO at ~20 K (subcooled liquid hydrogen temperature) rather than 77 K — simpler than LHe but still requires industrial cryoplant.
- **Missing at scale**: Optimization of 20 K cryogenic efficiency; integration with ARC's compact geometry and the thermal load from plasma-facing components.

---

**Balance of Plant (Power Conversion) — TRL 8–9**

- **Demonstrated**: Supercritical steam Rankine cycles at GW scale in fission and fossil plants. The recommended cycle for ARC (supercritical Rankine at 250 bar, 540°C inlet) operates within existing commercial plant parameters [arc-power-conversion-studies.md §3.2].
- **Missing at scale**: Integration with fusion-specific heat sources — tritium-compatible primary heat exchangers, pulsed thermal load from quasi-steady plasma, FLiBe-to-steam HX materials compatibility. The 645 MWth input and 46% net efficiency (297 MWe) are within the range of existing commercial Rankine plants, but the primary side (FLiBe) is novel.

---

## Section 4: Key Materials and Supply Chain Considerations

**REBCO Superconducting Tape — Critical bottleneck**

A single ARC-class reactor requires ~5,730 km of REBCO tape [arc-reactor-specifications.md §4.1, §6]. Global REBCO production capacity is estimated at thousands of km per year (the handwritten exemplar cites thousands of km/year across all manufacturers — Shanghai Superconductor Technology, Faraday Factory Japan, CFS). This implies current global capacity could supply at most 1–2 ARC-class magnets per year, with no margin for other applications (MRI, industrial magnets, power cables). Scaling to a fleet of reactors requires production scale-up of 1–2 orders of magnitude.

REBCO tape pricing in 2014 ranged from $36 to $198/m (per ARC paper), reflecting early-stage manufacturing. By 2025, leading PLD-REBCO manufacturers sell tape at ~$20/m, with top producers collectively supplying >3,000 km-12mm annually — accounting for over half of global HTS wire production [sciencedirect-science-article-pii-s2772830725000390.md §Introduction]. At >200 A per 4 mm tape width at 20 K, 20 T, this corresponds to ~$100/kA-m — below the entire 2014 range ($144–792/kA-m) but still roughly 10× above the commercial viability target of ~$10/kA-m. CFS is vertically integrating tape manufacturing. This cost trajectory is encouraging but the $10/kA-m commercial target represents a further ~10× reduction from 2025 market prices; tape cost uncertainty is the single largest input uncertainty in the ARC cost model.

Conductor performance is also improving rapidly: increasing REBCO film thickness from 1 μm to 4 μm increases critical current by ~200% [arc-reactor-specifications.md §4.1], meaning cost per amp-meter continues to fall even at constant $/m prices. This is an important model consideration: the $/kA-m metric, not $/m, is the relevant one.

**Tritium — Existential constraint for first-of-kind deployment**

Global civilian tritium inventory is approximately 25–30 kg, produced primarily as a byproduct of CANDU heavy-water reactors, and decays at 5.5%/year. The start-up tritium requirement for a D-T reactor is ~1 kg; maintaining breeding self-sufficiency requires TBR > 1.0 from first plasma [dossier, §Tritium Breeding]. ARC targets TBR ≥ 1.1 (optimizable to ~1.22) from FLiBe with Li-6 enrichment [arc-reactor-specifications.md §5.4]. The market price exceeds $35,000/kg.

The sequencing problem: early ARC plants must operate partly on external tritium while demonstrating breeding self-sufficiency. CANDU reactor retirements are reducing the external supply. The first few commercial D-T plants must demonstrate adequate TBR before the fleet can scale — there is no margin for breeding shortfalls in the early commercial phase. ARC's choice of FLiBe (rather than a solid ceramic breeder) provides flexibility: TBR is tunable by adjusting Li-6 enrichment fraction and blanket geometry.

**FLiBe (LiF-BeF₂) — Not at industrial scale**

ARC requires approximately 950 tonnes of FLiBe across the blanket tank, cooling channels, and heat exchanger [arc-reactor-specifications.md §5.4]. FLiBe is not currently produced at industrial scale. The Araiinejad 2025 study estimates NOAK FLiBe cost at ~$154/kg — giving a blanket material cost of ~$146M per reactor. This estimate assumes a 20% learning rate; actual NOAK costs are uncertain.

Beryllium (a component of FLiBe) is toxic and globally produced in limited quantities (~300 tonnes/year, dominated by Materion Corp. in the US). At ARC's demand, a fleet of 10 reactors would require ~9,500 tonnes/year of FLiBe, implying ~300 tonnes/year of Be per plant or ~3,000 tonnes/year for a 10-plant fleet — exceeding current global production by an order of magnitude. Beryllium supply chain development is a gating constraint for fleet-scale deployment.

Lithium-6 enrichment is needed for efficient tritium breeding. Natural lithium is ~7.6% Li-6; optimal TBR requires 40–90% enrichment. Only a few global suppliers produce enriched Li-6; Russia and China still use mercury-based enrichment processes that are banned in the EU and US. Western supply of Li-6 at scale requires new enrichment facilities.

FLiBe is a shared supply chain with certain fission MSR concepts (Kairos Power) and with IFE concepts using FLiBe liquid walls (see cross-concept Section 7). Shared demand could accelerate economies of scale, but could also create competition.

**Inconel 718 — Adequate at known scale, radiation behavior uncertain**

Vacuum vessel and blanket tank use Inconel-718 for its strength and FLiBe corrosion resistance. Inconel-718 is a mature industrial alloy with qualified global supply. The concern is specific to ARC's environment: high nickel content makes it "prone to nuclear activation" [arc-reactor-specifications.md §4.3], and radiation-assisted chromium transport in FLiBe exposure is an uncharacterized degradation mechanism. The paper designates Inconel-718 as a "first-round material" pending materials research. A material substitution in later design phases could affect fabrication cost.

**Tungsten (first wall) — Supply adequate, fabrication challenging**

Global tungsten supply is adequate for a fleet of reactors. The challenge is fabricating the precisely shaped, large-area tungsten first wall components that must withstand extreme heat loads and thermal cycling. This is a shared challenge with ITER-class tokamaks and is being addressed through the ITER program.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| **Performance** | | | | |
| Fusion power | 500–525 MW | arc-reactor-specifications.md §2 | high | ARC design point |
| Plasma gain (Qp) | 13.6 | arc-reactor-specifications.md §2 | high | Fully non-inductive design point |
| SPARC plasma gain | >2 (target ~11) | dossier §Plasma State; sparc-icrf-heating-paper.md §Introduction | high | SPARC is experiment, not power plant |
| Net electric output | 190–261 MWe | arc-power-conversion-studies.md §Results | high | Phase-dependent: 190 MWe (FNSF, 900K FLiBe) to 261 MWe (aggressive pilot, 1200K); 2025 target = 400 MWe |
| Thermal power to PCS | 645 MWth | arc-power-conversion-studies.md §2 | high | Per ARC design |
| Thermal efficiency (Rankine) | 46% net | arc-power-conversion-studies.md §3.2, Table 15 | high | Supercritical Rankine; recommended cycle |
| Thermal efficiency (sCO₂) | 40.3% net | arc-power-conversion-studies.md §3.3, Table 15 | high | Brayton cycle alternative |
| Auxiliary heating power | 38.6 MW | arc-reactor-specifications.md §5.1 | high | 25 MW LHCD + 13.6 MW ICRF (ARC) |
| ICRF coupled power (SPARC) | 25 MW | sparc-icrf-heating-paper.md §Introduction | high | 120 MHz, 12 four-strap antennae |
| Bootstrap fraction | 63% | arc-reactor-specifications.md §Introduction | high | Non-inductive profile |
| Major radius (ARC) | 3.3 m | arc-reactor-specifications.md §2 | high | Aspect ratio 3 |
| Minor radius (ARC) | 1.13 m | arc-reactor-specifications.md §2 | high | |
| On-axis field (ARC) | 9.2 T | arc-reactor-specifications.md §2 | high | |
| Peak on-coil field (ARC) | ~23 T | arc-reactor-specifications.md §4.1 | high | REBCO critical current margin maintained |
| Plasma current (SPARC) | 8.7 MA | sparc-icrf-heating-paper.md §Introduction | high | |
| TF coil fluence lifetime | 9 full-power years | arc-reactor-specifications.md §5 | high | REBCO fluence limit before replacement |
| TBR (FLiBe blanket) | ≥1.1 (optimizable to ~1.22) | arc-reactor-specifications.md §5.4 | high | Li-6 enriched FLiBe |
| REBCO tape per reactor | 5,730 km | arc-reactor-specifications.md §4.1 | high | Total TF + PF coil length |
| **Capital Cost** | | | | |
| Total fabricated component cost | $5.56B (2014 USD) | arc-reactor-specifications.md §6 | medium | Covers VV + blanket + magnets only; excludes BoP, land, indirect costs, construction interest. **NOAK/learning-assumed basis**: mass-proportional scaling at $1.06M/tonne benchmarked against ARIES/FIRE conceptual designs implicitly assumes mature manufacturing. First-of-a-kind (FOAK) costs would be substantially higher — see Hypothesis 4. |
| Magnet/structure cost (fabricated) | $5.1–5.2B (2014 USD) | arc-reactor-specifications.md §6 | medium | Dominates total: ~92% of component cost |
| Blanket cost (fabricated) | $260M (2014 USD) | arc-reactor-specifications.md §6 | medium | $160M materials, remainder fabrication |
| Vacuum vessel cost (fabricated) | $92M (2014 USD) | arc-reactor-specifications.md §6 | medium | $5.5M materials |
| REBCO tape materials cost | $103–206M (2014 USD) | arc-reactor-specifications.md §6 | medium | Depends on $/m price ($36–198/m); 5,730 km |
| FLiBe materials cost | ~$146M (NOAK) | arc-reactor-specifications.md §6; dossier §Energy Capture | medium | 950 t × $154/kg (2014 USD); includes HX inventory |
| Total plant cost (NOAK estimate) | Not published | proprietary | — | See gap inventory |
| $/kWe (FNSF phase) | ~$29,200/kWe | [inferred: $5.56B fabricated ÷ 190 MWe; excludes BoP, indirect, financing] | low | Component cost only; full plant cost would be substantially higher |
| $/kWe (aggressive pilot) | ~$21,300/kWe | [inferred: $5.56B fabricated ÷ 261 MWe; same caveats] | low | |
| Cost vs. ARIES-RS | 1/3 of ~$14B ARIES-RS at 1/4 the electrical output | arc-reactor-specifications.md §6 | high | ARIES-RS: 8 T, ~1 GWe. ARC: 9.2 T, 190–261 MWe |
| **Operating Cost** | | | | |
| REBCO tape price (2014) | $36–198/m | arc-reactor-specifications.md §4.1 | medium | Wide range = manufacturing uncertainty |
| REBCO tape price (current, ~2025) | ~$20/m (~$100/kA-m at >200 A/4mm, 20 K, 20 T) | sciencedirect-science-article-pii-s2772830725000390.md §Introduction | medium | PLD-REBCO from leading manufacturers; top producers supply >3,000 km-12mm/yr (>50% of global HTS wire production); still ~10× above $10/kA-m commercial target |
| REBCO target price (commercial) | ~$10/kA-m | [analogue: industry target; basis from handwritten exemplar] | low | Current conductor: ~250 A/m at 20K, 20T → ~$25–40/m |
| FLiBe unit cost (NOAK) | ~$154/kg | arc-reactor-specifications.md §6; Araiinejad 2025 [cited in handwritten exemplar] | medium | 20% learning rate assumed |
| Tritium market price | >$35,000/kg | dossier §Tritium Breeding [citing handwritten exemplar] | high | Current CANDU byproduct price |
| TiH₂ neutron shielding | 380 t at $26.4/kg | arc-reactor-specifications.md §6 | high | ~$10M; small fraction of total |
| Annual O&M cost (FECONS anchor) | ~$16M/yr at 261 MWe; ~$24M/yr at 400 MWe | arxiv-2601-21724.md §6.5 | low | $60/kWe-yr fusion-specific rate: "O&M is computed using a lookup-based factor of 60 USD/(kW_e-yr)"; framework reference, not ARC-specific; 2–4× below fission BoP analogue at ARC scale |
| Annual O&M cost (fission BoP analogue) | $50–100M/yr | [estimated from fission BoP analogue] | low | Upper bound; FECONS anchor suggests this overestimates O&M at ARC's output level |
| **Availability** | | | | |
| Capacity factor | Not published | proprietary/not-yet-sourced | — | See gap inventory |
| Quasi-steady pulse duration | Tens of minutes | dossier §Operation Mode | high | Long burns with brief interruptions |
| SPARC flat-top duration | 10 seconds | dossier §Operation Mode | high | Experiment, not power plant |
| **ARIES-AT Analogue Benchmark** | | | | |
| COE | 5 ¢/kWh (year unspecified, ~2000–2003 USD) | osti-etdeweb-servlets-purl-20261446.md §Abstract, Table 1 | medium | Dollar-year not stated in source; order-of-magnitude reference only |
| Net electric output | ~1,000 MWe | osti-etdeweb-servlets-purl-20261446.md §Abstract | high | 5.3× larger than ARC 2015 design (190–261 MWe); CAS fractions may not scale linearly with plant size |
| Net plant efficiency | 51% | osti-etdeweb-servlets-purl-20261446.md Table 1 | high | After recirculating power deduction |
| Thermal cycle efficiency (gross) | 59% | osti-etdeweb-servlets-purl-20261446.md Table 1, §3 | high | Advanced Brayton, SiC/PbLi blanket at ~1,100°C coolant outlet — 13 pp above ARC's 46% Rankine |
| Recirculating power fraction | 14% | osti-etdeweb-servlets-purl-20261446.md Table 1 | high | Net plant efficiency = cycle efficiency × (1 − recirculating fraction) |
| On-axis toroidal field | 6.0 T | osti-etdeweb-servlets-purl-20261446.md Table 1 | high | Abstract states 5.6 T; Table 1 value used as reference |
| Bootstrap current fraction | 0.94 | osti-etdeweb-servlets-purl-20261446.md §2 | high | Reference equilibrium at β_N = 6.0; 90% of theoretical limit |
| **FECONS Framework Reference** | | | | |
| LCOE (FECONS illustrative, not ARC-specific) | 55.1 $/MWh (5.5 ¢/kWh) | arxiv-2601-21724.md §8.3 Table 3 | low | 636.75 MWe, 0.9 availability, 30-year plant life; $60/kWe-yr O&M + $195.6M/yr capital + $1M/yr fuel; fusion-specific contemporary benchmark (complements ARIES-AT 5 ¢/kWh in 2000–2003 USD) |

---

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capacity factor | proprietary | blocking | No CFS publication states this; depends on blanket/divertor maintenance schedule |
| Full plant capital cost (with BoP, indirect, financing) | not-yet-sourced | blocking | ARC paper covers only VV + blanket + magnets; BoP, construction cost, and indirect costs are unaccounted. FECONS reference design (arxiv-2601-21724 §8.2): direct costs ~71% of TCC, indirect/owner/supplementary/financial ~29% of TCC — implies total plant cost is ~1.41× the direct (nuclear island + BOP) cost, not 2–3× the nuclear island alone. |
| Annual O&M cost breakdown | not-yet-sourced | important | ARC-specific breakdown not published; FECONS framework ($60/kWe-yr, arxiv-2601-21724 §6.5) provides fusion-specific anchor (~$16–24M/yr at ARC scale) — reduces uncertainty from truly-unknown to framework-bounded |
| ARC commercial design parameters (400 MWe update) | proprietary | important | 2025-2026 communications describe a 400 MWe plant, up from 190–261 MWe in 2015. Updated dimensions, field, and Q not published. |
| Blanket replacement schedule | not-yet-sourced | important | FLiBe liquid blanket does not face hard fluence limit like solid modules, but vacuum vessel/heat exchanger service life under FLiBe corrosion + radiation needs quantification |
| LHCD system cost | not-yet-sourced | important | 25 MW 8 GHz LHCD system is a novel high-risk subsystem; no cost estimate found |
| Tritium start-up inventory requirement | derivable | important | [inferred: ~1 kg at startup per D-T plant; basis: tritium decay rate × startup time × reserve margin] |
| REBCO coil lifetime (radiation + fatigue) | truly-unknown | important | 9 FPY is the shielding-based TF coil lifetime; actual coil degradation vs. time under combined mechanical + radiation load not characterized |
| Learning rate for REBCO tape | not-yet-sourced | nice-to-have | Araiinejad 2025 uses 20% for FLiBe; REBCO learning rate for $/kA-m reduction not found |

---

**Modeling Approach**

**Recommended architecture: Free-form parametric scaling with analogue cost fractions — not a structured CAS framework**

The ARC cost database provides fabricated component costs for three subsystems only (VV, blanket, magnets), explicitly excluding balance of plant. The 2015 paper states: "While a full costing of the ARC reactor is beyond the scope of this paper, a rough scaling based on volumes and materials prices has been performed" [arc-reactor-specifications.md §6]. The costing methodology is mass-proportional: $1.06M/tonne (2014 USD) for fabricated components, benchmarked against four prior devices (FIRE, BPX, PCASTS, ARIES-RS) [arc-reactor-specifications.md §6.2]. BOP capital cost, indirect costs, and construction financing are entirely absent from all available sources.

Given this structure, the appropriate approach is:

**(a) Free-form scaling with analogue cost fractions for BOP and indirect costs.** A structured costing framework (pyFECONS / 1costingfe) requires a complete CAS breakdown — which does not exist for ARC. Instead: use ARC's $5.56B as the direct nuclear island cost basis; estimate conventional BOP accounts (power conversion turbomachinery, buildings, electrical systems, water systems, site infrastructure) using ARIES-AT or ARIES-RS CAS fractions (BOP is typically 30–50% of nuclear island cost in MFE designs); apply indirect cost fractions from the FECONS framework (arxiv-2601-21724 §8.2): direct costs (nuclear island + BOP) constitute ~71% of Total Capital Cost, with the remaining ~29% comprising Capitalized Indirect Service Costs (~1%), Owner's Costs (~8%), Supplementary Costs (~10%), and Financial Costs (~8%). This implies a total plant cost of roughly 1.41× the direct cost sum — not 2–3× the nuclear island alone. The FECONS fraction is a framework reference, not ARC-specific; apply as a first-order bound while flagging ARC-specific indirect cost deviations. The regulatory cost multiplier from Araiinejad & Shirvan (2025) (1.0× under NRC Part-30 vs. 2.2× under Part-50-equivalent) is a discrete scenario branch that scales on top of this indirect cost structure, not a continuous variable.

**ARIES-AT benchmark values now available:** The ARIES-AT source (osti-etdeweb-servlets-purl-20261446.md) provides the anchor values for BOP analogue use: net plant efficiency 51%, recirculating power fraction 14%, on-axis field 6.0 T, bootstrap fraction 0.94, COE ~5 ¢/kWh at 1,000 MWe (~2000–2003 USD). Gap #1 is partially addressable from this source for CAS-independent BOP accounts. However, the ARIES-AT BOP cost fractions cannot be applied uniformly to ARC — the power conversion architectures are structurally different (see caveat below).

**ARIES-AT BOP CAS transfer caveat:** ARIES-AT's power conversion architecture uses an SiC/PbLi blanket at ~1,100°C coolant outlet driving an advanced Brayton cycle at 59% gross thermal efficiency. ARC's recommended cycle is supercritical Rankine at 46% net efficiency, driven by FLiBe at ~565°C PCS inlet. The 13-percentage-point efficiency gap reflects a fundamentally different hardware configuration — different coolant chemistry, different outlet temperature regime, different turbomachinery class. ARIES-AT CAS fractions therefore split into two distinct classes:

- **Transfer cleanly to ARC (cycle-independent accounts):** CAS-20 (site improvements), CAS-21 (structures and site facilities — buildings, civil works, waste management), CAS-24 (electric plant equipment — switchyard, grid connection, transformers, emergency diesel). These accounts depend on plant footprint, regulatory requirements, and utility interface, not on the thermal cycle design.
- **Require independent treatment (architecture-specific accounts):** CAS-22 (turbine plant equipment — turbomachinery, heat exchangers, hot-side piping, condenser systems). ARIES-AT's CAS-22 is calibrated to high-temperature Brayton hardware; ARC's CAS-22 requires supercritical Rankine equipment at lower temperatures. Applying ARIES-AT CAS-22 fractions to ARC embeds a systematic cost mismatch. Estimate ARC's CAS-22 independently using supercritical Rankine cost data from commercial steam plant literature or analogous fission plant data at comparable MWth throughput.

Do not apply ARIES-AT CAS fractions as a uniform BOP multiplier; apply selectively by account type.

**ARC-specific BOP additions not covered by ARIES analogues**: ARIES-AT and ARIES-RS use solid ceramic tritium breeders with conventional steam BOPs — neither design includes a FLiBe chemistry plant or molten-salt tritium extraction system. Applying ARIES CAS fractions directly to ARC's BOP would omit a real cost line with no analogue in those studies. The FLiBe chemistry and tritium extraction plant must be treated as an additive ARC-specific BOP cost, estimated independently from the ARIES fraction approach. No published cost estimate exists for this subsystem (see Section 6, gap #15). Scope the ARIES fraction guidance strictly to conventional BOP accounts; flag the FLiBe plant as a truly-unknown additive line.

**(b) Primary scaling axes — three parameters dominate model output:**
1. **REBCO tape cost [$/kA-m]** — drives 80–90% of the nuclear island cost uncertainty. Span at least 10× the $10/kA-m commercial target in sensitivity analysis.
2. **Capacity factor [%]** — ARC is CAPEX-heavy; a 2× swing in capacity factor (50% → 90%) produces a near-2× LCOE swing. Treat as the primary output sensitivity lever.
3. **Regulatory cost multiplier [1.0×–2.2×]** — scenario-level uncertainty, not a parameter range; model as two discrete cases.

**(c) Do not compute from first principles:**
- **BOP capital cost**: No ARC-specific data exists; use ARIES-AT CAS2X/CAS9X fractions as analogues with explicit uncertainty range.
- **Annual O&M**: Use D-T tokamak O&M structure from Araiinejad & Shirvan (2025); a maintenance schedule model does not exist for ARC.
- **Updated 400 MWe design parameters**: The 2025 CFS target is not publicly documented. Do not extrapolate from the 2015 paper without an explicit assumption flag.
- **REBCO learning curve**: Avoid single-point learning rate projections; treat the price trajectory as a scenario parameter.

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Full plant capital cost including BoP, indirect costs, construction financing | S5 | not-yet-sourced | blocking | ARIES-AT source now ingested (osti-etdeweb-servlets-purl-20261446.md): provides analogue benchmark values (COE, net plant efficiency, recirculating power fraction) for cycle-independent CAS accounts (CAS-20, CAS-21, CAS-24). CAS-22 power conversion turbomachinery cannot be transferred directly — ARIES-AT's SiC/Brayton cycle at 59% differs structurally from ARC's FLiBe/Rankine at 46%. FECONS/pyFECONS (arxiv-2601-21724 §8.2) partially addresses indirect cost fraction: direct costs ~71% of TCC, indirect/owner/supplementary/financial ~29% of TCC — bounds the indirect multiplier without ARC-specific BOP data. ARC-specific BoP direct cost structure still absent. |
| 2 | Capacity factor — not stated anywhere in CFS/ARC publications | S1, S5 | proprietary | blocking | ITER-analogues (PROCESS code) for maintenance schedule estimates; Stewart & Shirvan 2022 for regulatory impact |
| 3 | ARC updated commercial design parameters (400 MWe; evolved from 2015 paper) | S1, S5 | proprietary | important | CFS investor presentations or patent filings; Araiinejad & Shirvan 2025 may reference updated parameters |
| 4 | Tritium extraction timescales from FLiBe | S2, S3 | truly-unknown | important | ORNL FLiBe experimental program; US DOE fusion tritium cycle publications |
| 5 | REBCO neutron irradiation data at fusion-relevant fluence | S3, S4 | truly-unknown | important | ITER/SPARC irradiation test campaigns (underway but not yet reported); REBCO manufacturers' neutron test data |
| 6 | I-mode confinement validation at ARC operating point (0.55 MW/m²/n₂₀, 9 T+) | S2 | truly-unknown | important | SPARC experimental results (2027+); DIII-D high-field campaigns |
| 7 | Annual O&M cost breakdown | S2, S5 | not-yet-sourced | important | Araiinejad 2025 for D-T tokamak O&M structure; PROCESS output for staffing model; arxiv-2601-21724 (FECONS/pyFECONS) provides $60/kWe-yr fusion-specific anchor (§6.5) — not ARC-specific but reduces gap from truly-unknown to framework-bounded (~$16–24M/yr at ARC's 261–400 MWe range) |
| 8 | REBCO tape learning rate ($/kA-m trajectory to commercial target) | S4 | not-yet-sourced | important | REBCO manufacturers' public roadmaps; Rocky Mountain Institute superconductor market analysis |
| 9 | FLiBe-Inconel corrosion under combined radiation + flow | S3, S4 | truly-unknown | important | ORNL FLiBe corrosion database; MSR materials test programs (Kairos Power, TerraPower) |
| 10 | Blanket replacement schedule / FLiBe system service life | S2, S5 | not-yet-sourced | important | ITER TBM results; ARC detailed design update (if published) |
| 11 | LHCD system (8 GHz, 25 MW) cost and technology readiness | S3, S5 | not-yet-sourced | important | ITER LHCD program data; EC/LH system cost benchmarks from larger tokamaks |
| 12 | Li-6 enrichment supply chain and cost at fleet scale | S4 | not-yet-sourced | important | US DOE Li-6 enrichment program; ORNL isotope production data |
| 13 | Regulatory cost impact specific to NRC Part 30 framework | S2 | not-yet-sourced | nice-to-have | Stewart & Shirvan 2022 (quantifies Part 50 impact); NRC fusion rulemaking docket |
| 14 | Divertor replacement cost and frequency for compact tokamak geometry | S3, S5 | not-yet-sourced | nice-to-have | ITER divertor cost data; DEMO/EU-DEMO studies |
| 15 | FLiBe chemistry plant and tritium extraction system capital cost — ARC-specific BOP addition with no ARIES analogue | S5 | truly-unknown | important | ARC paper explicitly excludes BOP from cost scope; tritium extraction from FLiBe is identified only as an R&D requirement with no design or cost basis [arc-reactor-specifications.md §7]. Cannot be estimated from ARIES CAS fractions. Estimate by analogy to chemical plant cost databases (e.g., IChemE) scaled to blanket flow rate and tritium throughput, or defer to a detailed ARC BOP engineering study. |

---

## Section 7: Cross-Concept Notes

**ARC vs. Conventional Large-Bore LTS Tokamak (ITER/ARIES-RS class)**

The table below identifies the key structural differentiators between ARC and the reference class — a conventional large-bore LTS tokamak (ITER-scale or ARIES-RS-scale, Nb₃Sn/Nb₃Ti conductor). Each is labeled **novel** (new to ARC/CFS approach) or **borrowed** (standard tokamak practice), with a single-sentence cost implication.

| Differentiator | ARC | Conventional (ITER/ARIES-RS) | Status | Cost Implication |
|---|---|---|---|---|
| Superconductor: REBCO HTS, 20–23 T on-coil | REBCO at 20 K, ~23 T peak | Nb₃Sn/Nb₃Ti, 11–13 T peak | **Novel** | REBCO currently ~3–5× more expensive per kA-m than Nb₃Sn; commercial viability requires tape cost to fall to ~$10/kA-m — the primary cost uncertainty. |
| High-field compact geometry (R=3.3 m, B=9.2 T on-axis) | R=3.3 m, ~500 MW fusion | R=6.2–8.1 m, 500–2000 MW fusion | **Novel realization** | Claimed 1/3 the cost of ARIES-RS at ~1/4 the output [arc-reactor-specifications.md §6]; net $/kWe advantage requires high capacity factor to amortize reduced output. |
| Demountable TF coil joints | Yes — all 18 TF coils removable | No (welded/permanent) | **Novel** | Higher joint fabrication cost; but enables in-situ blanket/vessel maintenance without full reactor disassembly, reducing lifecycle maintenance downtime. |
| Liquid FLiBe blanket (breeder + coolant + shield combined) | FLiBe liquid immersion | Solid ceramic modules + He/water cooling | **Novel** | Eliminates complex solid module handling cost; TBR tunable via Li-6 enrichment. Adds chemical processing plant and introduces uncharacterized MHD/corrosion risk not present in solid breeders. |
| I-mode confinement basis (no ELMs) | I-mode | H-mode ELMy or ELM-suppressed | **Novel** | Eliminates ELM-driven first-wall erosion cost; reduces divertor replacement frequency. Risk: regime not yet validated at ARC parameters (0.55 MW/m²/n₂₀, 9.2 T). |

**Borrowed from conventional tokamak practice** (not sources of cost differentiation): D-T fuel cycle, tritium breeding blanket requirement, supercritical steam Rankine BOP, tungsten first wall and divertor, remote maintenance requirement, regulatory framework. The hybrid energy conversion approach (FLiBe carries both breeding and thermal duties) is a structural efficiency relative to separate solid-breeder and coolant systems, but does not eliminate the steam Rankine BOP.

---

Three approved analyses are available: MagLIF (07), FRC with Direct Conversion / Helion (08), and Spherical Tokamak HTS / Tokamak Energy (21). The analysis of concept 21 already reuses concept 01 as a prior; the analysis of concept 08 also references concept 01.

**vs. Spherical Tokamak HTS (21 — Tokamak Energy ST-E1)**

The most direct comparator. Both concepts use HTS REBCO magnets in a D-T tokamak. The key divergence is aspect ratio and field strategy: CFS ARC uses A=3, B=9.2 T on-axis, R=3.3 m; Tokamak Energy ST-E1 uses A=2.3, B=5.25 T on-axis, R=5.0 m. CFS achieves higher fusion power density (∝ B⁴/R²) via higher field; TE compensates with larger volume. The cost implication is important: ARC's $5.56B is dominated by magnet structure, while ST-E1 with lower field requires proportionally less magnet cost per unit volume but more volume. Both share the REBCO supply chain bottleneck; competition for limited REBCO production is a shared risk.

The data availability contrast is striking: CFS has published detailed component-level cost data (2015 paper); Tokamak Energy has published no cost data whatsoever. The ST-E1 analysis (21) uses ARC as an analogue for magnet cost structure assumptions.

The energy capture choice is also shared: both are D-T with thermal (steam) energy capture pending engineering commitment. The 46% Rankine efficiency from arc-power-conversion-studies.md applies as an analogue baseline for the ST-E1 analysis.

**vs. FRC with Direct Conversion / Helion (08)**

Near-zero overlap in cost structure. Helion uses a pulsed FRC with D-He3 fuel and direct inductive energy recovery — eliminating the entire thermal cycle, breeding blanket, and tritium management infrastructure. ARC's ~$400M blanket cost and tritium fuel cycle have no analogue in Helion's architecture. The contrast illustrates the maximum divergence within the private fusion landscape: ARC is the CAPEX-intensive, well-documented steady-state end, while Helion is the OPEX-light, low-data pulsed end. The concept 08 analysis already references concept 01 for REBCO tape supply chain context, since both use HTS magnets.

**vs. MagLIF / Pacific Fusion (07)**

Minimal overlap. MagLIF is pulsed-power magnetized target fusion — 14.1 MeV D-T neutrons are shared, but the engineering systems (pulsed power driver, cylindrical liner compression, no external breeding blanket) are entirely different from ARC. The shared characteristics are: D-T fuel cycle (tritium supply constraints are identical), 14 MeV neutron management (both require substantial shielding), and ultimately the same BoP (steam Rankine). The FLiBe liquid wall studied for MagLIF chamber concepts shares design challenges with ARC's FLiBe blanket (MHD effects, tritium extraction, radiation compatibility) — this is a rare point of cross-concept leverage for shared research.

**Shared cost structure patterns across tokamak concepts:**

From the cross-concept perspective, the handwritten exemplar and the Araiinejad & Shirvan 2025 analysis establish that D-T tokamak LCOE is consistently dominated by: (1) reactor CAPEX (magnets + blanket + structure), (2) capacity factor, (3) regulatory cost adder. These three factors appear in every tokamak cost study regardless of geometry. ARC's compact HTS approach reduces (1) via volume reduction, but (2) and (3) remain shared challenges. This pattern holds for both ARC and ST-E1, confirming that the high-field compactness strategy is primarily a CAPEX mitigation strategy, not an O&M or regulatory mitigation.

---

## Section 8: Sources

1. **Sorbom et al. (2015), "ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets"**, *Fusion Engineering and Design* 100, 378–405 — Primary ARC design reference. Provides reactor dimensions, magnet specifications, FLiBe blanket design, component-level cost analysis, and structured R&D gap inventory. Found at: `/exploration/phase_1a/research/01-hts-compact-tokamak/iter-03/sources/arc-reactor-specifications.md`

2. **Lin, Wright et al. (2020), "Physics basis for the ICRF system of the SPARC tokamak"**, *Journal of Plasma Physics* 86 — ICRF system design, antenna concepts, power absorption analysis, SPARC machine parameters (Bt, Ip, R, a). Found at: `/exploration/phase_1a/research/01-hts-compact-tokamak/iter-03/sources/sparc-icrf-heating-paper.md`

3. **Power Conversion Study (2020), "Exploration of power conversion thermodynamic cycles for ARC fusion reactor"**, *Fusion Engineering and Design* — Three-cycle comparison (Rankine, sCO₂, He Brayton) for ARC. Provides net efficiency and net electric output for each cycle against 645 MWth input. Found at: `/exploration/phase_1a/research/01-hts-compact-tokamak/iter-04/sources/arc-power-conversion-studies.md`

4. **CFS 2025–2026 Updates** — Construction status (first TF coil installed Jan 2026), SPARC timeline (first plasma 2027), ARC commercial target (400 MWe, early 2030s). Found at: `/exploration/phase_1a/research/01-hts-compact-tokamak/iter-04/sources/cfs-2025-2026-updates.md`

5. **Phase 1a Dossier, HTS Compact Tokamak** (2026-03-06) — Per-column values with confidence ratings and citations for all 12 differentiation schema columns. Covers confinement family, fuel, heating, energy capture, plasma state, magnets, blanket, neutron management, operation mode, and key metadata. Found at: `/exploration/phase_1a/research/01-hts-compact-tokamak/dossier.md`

6. **Araiinejad & Shirvan (2025), "Techno-economic Analysis of Deuterium-Tritium Magnetic Confinement Fusion Power Plants"**, *Applied Energy* 401, 126567 — Quantifies regulatory cost impact (2.2× building cost under Part 50), O&M structure, FLiBe NOAK cost ($154/kg at 20% learning rate). Cited via handwritten exemplar 01-hts-compact-tokamak.md.

7. **Colliva et al. (2024), "Power conversion thermodynamic cycles for ARC"**, MDPI — Independent conclusion that supercritical Rankine steam is "the most promising solution" for ARC power conversion. Cited via Phase 1a dossier.

8. **Creely et al. (2020), "Overview of the SPARC tokamak"**, *Journal of Plasma Physics* — SPARC machine parameters, Q~11 burning plasma target. Cited via Phase 1a dossier.

9. **Brown (2018), "Three confinement systems — spherical tokamak, standard tokamak, and stellarator: a comparison of key component cost elements"**, *IEEE Transactions on Plasma Science* 46(6) — Component cost decomposition across tokamak geometries. Cited via handwritten exemplar for cross-concept cost structure context.

10. **Handwritten Exemplar: 01-hts-compact-tokamak.md** (Fusion TEA internal) — Calibration reference for LCOE challenge ranking, TRL assessments, and supply chain constraints (REBCO, FLiBe, tritium, vanadium, tungsten). Contains citations to Araiinejad 2025, ARIES studies, Foster 2024, and Whyte 2024 that are not directly ingested as source documents.

11. **ARIES-AT Study** (Najmabadi et al., *Fusion Engineering and Design*, ~2006) — ARIES-AT plant-level parameters: net electric ~1,000 MWe, fusion power 1,755 MW, thermal cycle efficiency 59% (advanced Brayton, SiC/PbLi at ~1,100°C), net plant efficiency 51%, recirculating power fraction 14%, on-axis field 6.0 T, bootstrap fraction 0.94, COE 5 ¢/kWh (~2000–2003 USD). Used as BOP cost analogue for cycle-independent CAS accounts (CAS-20, -21, -24); CAS-22 requires independent treatment due to structural cycle mismatch with ARC. Found at: `/knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/osti-etdeweb-servlets-purl-20261446.md`
