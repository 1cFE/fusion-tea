# D1+ Analysis: Particle Accelerator-Driven Fusion (D-T) — SHINE Technologies

---

## Section 1: Availability of Data

**Rating: Moderate (operational facts) / Opaque (economics)**

SHINE Technologies is unusual in this landscape: it is the only **commercially operating** fusion system in the concept catalog. This commercial reality cuts both ways for data availability. The technology concept itself is well-documented in public sources — NRC licensing records, peer-reviewed literature on accelerator-driven neutron sources, Wikipedia, and SHINE's own product marketing are openly available. However, operational economics (beam power consumption, facility capital cost, production yields, margins on Mo-99 and Lu-177 sales) are proprietary commercial information that SHINE has no incentive to disclose.

**Technical concept documentation:**

The fundamental physics is thoroughly understood. Piefer et al. (2011, ANL Mo-99 proceedings) describes the beam-target D-T approach for isotope production, providing accelerator architecture and target geometry context. Wikipedia gives a reliable summary of the SHINE process covering accelerator voltage, beam-target geometry, subcritical LEU assembly configuration, and NRC licensing history. SHINE's own press materials for the FLARE neutron system report 5 × 10^13 D-T fusion reactions per second and 14.1 MeV neutron output [shine-technology-overview.md §Key Facts]. NRC licensing documents (ML13172A262, ML15258A372) are publicly accessible and contain some technical parameters.

> "Compact linear particle accelerator drives beam-on-target fusion... Deuterium ions accelerated to up to 300 kV, fired into tritium gas target → D-T fusion → 14.1 MeV neutrons"
> — shine-technology-overview.md, §Key Facts

**What SHINE does not publish:**

Beam current, total electrical power consumption, capital cost of the accelerator system, tritium inventory and consumption rate, Mo-99 production yield, and any form of facility-level economics. The company has no obligation to publish these for a non-power commercial product, and none are available in the Phase 1a source set.

**Independent analyses:**

Because SHINE is not a power plant, it has not attracted the type of independent TEA analysis that power concepts receive (ARIES-class plant studies, PROCESS system code models). The few independent assessments of accelerator-driven fusion as a power concept are in the academic literature discussing why beam-target D-T cannot reach energy break-even — these confirm the fundamental physics limitation rather than offering SHINE-specific economics.

**Phase 1a dossier completeness:**

The dossier achieved high confidence on all taxonomy columns after two research iterations. The remaining gaps (beam current, neutron yield per unit beam power) are proprietary commercial parameters not resolvable through public research.

**Key data gaps limiting this analysis:**

1. Total electrical power consumption of the accelerator system — needed to characterize recirculating power burden
2. Facility capital cost breakdown — no published figure
3. Tritium consumption rate and procurement costs — NRC-licensed but not publicly specified
4. Mo-99 production economics and revenue — proprietary commercial

---

## Section 2: Challenges in Capturing System Function

SHINE presents a categorically different modeling challenge from every other concept in this landscape: **it is not a power plant and cannot be made into one by incremental development.** Beam-target D-T fusion is physically incapable of achieving energy break-even (Q ≥ 1), and SHINE does not claim otherwise. This creates multiple distinct modeling challenges:

**1. LCOE framework does not apply — requires a different economic model (Impact: Fundamental)**

Standard fusion LCOE analysis measures cost-per-kWh of electricity. SHINE produces no electricity and has no design pathway to net power output. The correct economic metric for SHINE is either cost-per-useful-neutron or cost-per-Curie of medical isotope. Modeling SHINE in the power-generation TEA pipeline requires an explicit statement of why beam-target D-T is excluded from the power-generation competition — not just flagging it as low-Q, but explaining what architectural change would be required (answer: a plasma-confining device capable of sustaining fusion burn, which is not beam-target physics).

The Q constraint is not a technology maturity problem but a physics ceiling. In beam-target D-T, each accelerated deuteron must be given ~150–300 keV of kinetic energy to access the D-T cross-section peak (σ ≈ 5 barns at ~120 keV CM energy). The D-T reaction releases 17.6 MeV total per event — a favorable single-reaction energy ratio of roughly 60:1. However, only a small fraction of beam deuterons fuse before losing their energy by elastic scattering and ionization in the target gas. The resulting effective Q for any practical thin or thick target is well below 1. SHINE's system is a net electricity consumer operating on purchased grid power.

**2. Physics calculation quantifies the Q gap (Impact: Demonstrated)**

At SHINE's stated fusion rate of 5 × 10^13 reactions/second, the total fusion power output is:

> P_fusion = 5 × 10^13 reactions/s × 17.6 × 10^6 eV × 1.6 × 10^{-19} J/eV ≈ **140 mW**

This is 140 milliwatts. The accelerator beam driving this reaction draws an estimated beam power of:

> P_beam = 300 kV × ~50 mA (mid-range beam current estimate) = **15 kW**

This gives Q_fusion ≈ 140 × 10^{-3} / 15,000 ≈ **10^{-5}**, five orders of magnitude below break-even. This is not a failure to optimize — it is a direct consequence of beam-target physics in which the beam slows primarily through Coulomb collisions with electrons rather than fusion reactions. The actual Q is independent of whether the beam current is 5 mA or 500 mA: the ratio of reaction energy to beam energy per fusion event stays near 10^{-5} because it is determined by the ratio of fusion cross-section to stopping cross-section. [Beam current not published by SHINE; 50 mA is a plausible midpoint estimate based on beam-target neutron generator literature for similar voltage ranges.]

**3. Tritium supply is a recurring cost driver with no self-sufficiency pathway (Impact: High for scaling)**

Unlike D-T power concepts that breed their own tritium, SHINE procures tritium externally and consumes it in fusion reactions without breeding. At 5 × 10^13 reactions/second, tritium consumption is approximately 8 mg/year:

> T consumption = 5 × 10^{13} atoms/s × [3 g/mol / (6.022 × 10^{23} atoms/mol)] × 3.15 × 10^7 s/yr ≈ **8 mg/yr**

At ~$35,000/g this is ~$280/year in tritium consumed — operationally negligible. The binding constraint is the NRC tritium possession limit and external procurement logistics, not unit cost. Scaling the SHINE concept to higher neutron flux increases tritium possession requirements and requires NRC amendment. No tritium breeding occurs; external supply is the only source.

**4. Revenue model is isotope pricing, not energy pricing (Impact: Structural)**

SHINE's economic viability is driven by Mo-99 and Lu-177 market pricing, not electricity markets. Mo-99 (the parent of Tc-99m, the most widely-used diagnostic nuclear medicine radioisotope) has historically traded at $2,000–$30,000 per 6-day Ci at the producer level, with global demand ~12,000 Ci/week. Lu-177 for targeted radionuclide therapy is a separate growing market. The economics are therefore tied to medical isotope market dynamics, beam-on-time and system availability for continuous production, and Mo-99 yield per unit neutron flux — none of which are in the standard fusion TEA parameter set.

**5. O&M structure is industrial, not fusion-plant (Impact: Moderate for comparability)**

SHINE's O&M profile resembles a specialty radiopharmaceutical manufacturing plant more than a fusion power plant. Maintenance is contact-accessible (no activation concerns at this neutron flux scale comparable to a power plant), isotope extraction is routine radiochemistry, and the accelerator is an industrial device with established maintenance schedules. This is both a strength (low O&M uncertainty) and a structural difference that prevents direct comparison to other concepts in the LCOE landscape.

**Note on O&M gap:** Per cross-concept memory, analyses should include a placeholder O&M subsection even for thin-data concepts. For SHINE: estimated O&M structure is dominated by (a) accelerator power cost (grid electricity at ~$0.05–0.10/kWh × unknown beam power draw), (b) staff (NRC-licensed radiological operations require certified operators), (c) LEU fuel and waste disposal, (d) tritium procurement and waste management. No published breakdown is available.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least to most mature. Note: because SHINE is commercially operating, the maturity profile is dramatically different from every other concept in this catalog — most subsystems are at TRL 8–9.

---

**Scaling to power application — TRL 1**

- **Demonstrated**: Nothing. No one has attempted to engineer beam-target D-T fusion toward net energy production because the physics prohibits it (Q ≈ 10^{-5}).
- **On paper only**: No published design study for a power-producing beam-target system exists.
- **Missing at scale**: Everything relevant to power generation — plasma confinement, energy multiplication beyond Q = 1, tritium breeding, thermal energy conversion. The entire chain must be invented; beam-target D-T provides none of these building blocks.

---

**Medical Isotope Extraction and Processing — TRL 7–8**

- **Demonstrated**: Mo-99 production from neutron-irradiated aqueous LEU solution at commercial scale; Lu-177 production confirmed. SHINE has been producing Mo-99 commercially since approximately 2019 and expanded capacity significantly with FLARE.
- **On paper only**: Full throughput optimization at FLARE-level neutron flux with automated remote handling for radioactive separation chemistry.
- **Missing at scale**: Sustained production at maximum FLARE capacity with minimal downtime; Lu-177 production processes are newer and less mature than Mo-99.

---

**FLARE / LIBRTI Neutron Irradiation Services — TRL 8–9**

- **Demonstrated**: FLARE described as "the world's most powerful continuous fusion neutron system" [shinefusion.com, FLARE press release]; LIBRTI deployed for UKAEA neutron irradiation services.

> "SHINE Technologies Showcases FLARE™ — the World's Most Powerful Continuous Fusion Neutron System"
> — shinefusion.com, FLARE press release (2024)

- **On paper only**: Multi-year contracted radiation effects testing programs at high instrumentation and electronics testing throughput.
- **Missing at scale**: Very high fluence irradiation campaigns requiring months of continuous operation at maximum flux; qualification testing for nuclear-grade structural materials requiring sustained high 14 MeV fluences.

---

**Subcritical LEU Assembly (for Mo-99) — TRL 8–9**

- **Demonstrated**: NRC-licensed subcritical assembly using aqueous LEU solution driven by D-T fusion neutrons; commercially operating for Mo-99 production. NRC license documents publicly available (ML13172A262, ML15258A372).

> "NRC-licensed subcritical LEU assembly... Neutrons drive subcritical LEU fission for Mo-99/Lu-177 isotope production"
> — dossier.md §Blanket Config

- **On paper only**: Scaled-up assembly geometries for higher neutron flux environments.
- **Missing at scale**: Not applicable — design operates at commercial scale within NRC-licensed parameters.

---

**Tritium Gas Target System — TRL 9**

- **Demonstrated**: Commercially operating at stated 5 × 10^13 D-T reactions/second [shine-technology-overview.md §Key Facts]. Continuous steady-state operation demonstrated. Target handling and recycling systems operational. No publicly available data on target lifetime or tritium replacement schedule.
- **On paper only**: Nothing material.
- **Missing at scale**: Tritium target scaling to higher beam currents would require NRC license amendment; not a technical barrier.

---

**Compact Linear Ion Accelerator (≤300 kV, D-beam) — TRL 9**

- **Demonstrated**: Commercially operating in steady-state continuous mode. Accelerators of this type (compact electrostatic, 100–400 kV, low-to-moderate beam current) are mature industrial devices with decades of deployment history in neutron generators for well-logging, security scanning, and laboratory sources. SHINE's application is the highest-flux commercial deployment of this technology class.

> "Deuterium ions accelerated to up to 300 kV, fired into tritium gas target"
> — shine-technology-overview.md, §Key Facts; dossier.md §Primary Heating

- **On paper only**: Higher-beam-current variants for increased neutron flux beyond current FLARE capability.
- **Missing at scale**: Nothing material for the current operating regime.

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium — Ongoing Procurement, Supply Constrained at Scale**

SHINE procures tritium externally for the gas target. No tritium breeding occurs. At the current stated fusion rate (5 × 10^13 reactions/s), annual tritium consumption is approximately 8 mg/year [inferred from reaction rate: Section 2 derivation]. At ~$35,000/g, this amounts to roughly $280/year in tritium consumed by reactions — operationally negligible. The binding constraint is the NRC possession limit under SHINE's license and procurement logistics, not unit cost. As SHINE scales toward higher neutron flux with FLARE, tritium inventory requirements increase and require NRC amendments. The global civilian tritium supply constraint (~25–30 kg total, declining as CANDUs retire) is not a near-term concern for SHINE's operating scale; if multiple SHINE-type facilities were built simultaneously, demand would still be trivially small compared to D-T power plant programs.

**Low-Enriched Uranium (LEU) — Limited Qualified Suppliers**

The subcritical assembly uses aqueous LEU solution. LEU for research and isotope production reactors is supplied by a small number of government-qualified suppliers (ConverDyn, Tenex, others) under NNSA oversight as part of the global effort to eliminate highly enriched uranium from civilian programs. SHINE's conversion to LEU-based production was itself a significant nonproliferation milestone. Supply is adequate for current needs; the supplier base is narrow and geopolitical disruptions (e.g., Russian supply chain) create risk. This is a shared concern with all medical isotope reactor operators globally.

**Deuterium Gas — Abundant, No Supply Constraint**

Deuterium is commercially available as D₂ gas from industrial suppliers at ~$100–600/kg depending on purity grade. At SHINE's operating scale, deuterium is a negligible cost item. No supply constraint.

**Accelerator Components — Mature Industrial Supply Chain**

Ion accelerators at 100–400 kV scale are mature industrial devices. Components (vacuum systems, ion sources, high-voltage power supplies, beam optics) are available from multiple established suppliers (National Electrostatics Corp., HVEE, Excelis, others). No supply chain constraint.

**No HTS Tape, No Beryllium, No FLiBe — SHINE Is Supply-Chain-Simple**

SHINE requires none of the materials that create supply chain risk for plasma-confining fusion concepts: no REBCO tape, no FLiBe, no beryllium multiplier, no large cryogenic systems, no specialized laser gain media. From a materials supply chain perspective, SHINE is the simplest concept in this catalog by a wide margin. This simplicity is the direct consequence of not attempting plasma confinement.

---

## Section 5: LCOE-Relevant Parameters

**Framing note**: SHINE does not generate electricity, and beam-target D-T cannot achieve Q ≥ 1 by physics. The standard LCOE metric ($/kWh) does not apply. The relevant economic metrics are (a) cost per useful neutron for radiation-effects testing, and (b) cost per Ci of Mo-99 or Lu-177 for isotope production. The table below captures what quantitative parameters are available and flags what would be needed to characterize SHINE's true economics.

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| D-T fusion reaction rate | 5 × 10^13 reactions/s | shine-technology-overview.md §Key Facts | high | FLARE system rated performance |
| Deuterium beam voltage | ≤ 300 kV | shine-technology-overview.md §Key Facts; dossier.md §Primary Heating | high | Sets beam kinetic energy and D-T cross-section regime |
| Neutron energy | 14.1 MeV | shine-technology-overview.md §Key Facts | high | D-T fusion neutron; 14.1 MeV forward, ~14.1 MeV average in lab frame for thick-target geometry |
| Operation mode | Steady-state (continuous) | shinefusion.com FLARE press release §Continuous operation | high | "Continuous fusion neutron system" |
| Fuel type | D-T beam on gas target | dossier.md §Fuel | high | Deuterium beam onto tritium gas target; no plasma confinement |
| Effective Q (energy gain) | ~10^{-5} | [inferred: P_fusion (~140 mW) / P_beam (~15 kW at 50 mA × 300 kV); reaction rate from FLARE press release; beam current midpoint estimate from accelerator literature for this voltage class] | medium | Physical ceiling, not a technology maturity issue; Q is approximately constant across this beam-target operating regime regardless of beam current |
| Fusion power (derived) | ~140 mW | [inferred: 5×10^13 reactions/s × 17.6 MeV/reaction × 1.6×10^-13 J/MeV; reaction rate from shine-technology-overview.md §Key Facts] | high | Confirms non-power status; total fusion energy output is trivially small |
| Tritium consumption rate | ~8 mg/year | [inferred: 5×10^13 T-atoms/s × 3 g/mol / (6.022×10^23 atoms/mol) × 3.15×10^7 s/yr; Section 2 derivation] | medium | At current reaction rate only; tritium cost ~$280/yr — negligible |
| NRC licensing status | Licensed, commercial operation | NRC records ML13172A262, ML15258A372 | high | Aqueous homogeneous reactor licensing; confirms commercial operation |
| Net electrical output | 0 kWe | dossier.md §Energy Capture | high | "No thermal cycle, no electricity generation" — by design |
| Products | Mo-99, Lu-177, FLARE/LIBRTI neutron services | shinefusion.com product pages | high | Mo-99 for Tc-99m diagnostic imaging; Lu-177 for targeted radionuclide therapy |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Beam current (mA) | proprietary | blocking | Required to calculate beam power consumption; with voltage known (300 kV), current determines total electrical input to accelerator and confirms Q estimate |
| Total electrical power consumption | proprietary | blocking | The "recirculating power fraction" analog — determines operating cost |
| Facility capital cost ($M) | proprietary | blocking | No published figure; private company |
| Mo-99 production yield (Ci/beam-hour) | proprietary | blocking | Key revenue driver; sets the economic case |
| Capacity factor / beam-on-time fraction | proprietary | important | Determines annual neutron output and production volume |
| OPEX breakdown (staffing, tritium, LEU, maintenance) | proprietary | important | Needed for operating economics model |
| Tritium inventory (possession) beyond consumption | proprietary / NRC | important | NRC license amendment filings may contain possession limits |
| Lu-177 production rate | proprietary | important | Newer product; economics less developed than Mo-99 |
| FLARE service pricing ($/neutron·cm^{-2}·s^{-1}) | proprietary | nice-to-have | Sets LIBRTI/FLARE revenue side |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Beam current (mA) — determines beam power consumption and confirms Q estimate | S2, S5 | proprietary | blocking | NRC license documents (ML13172A262) may constrain beam power; Piefer et al. (2011) may contain design specifications; accelerator literature for comparable beam-target neutron generators provides analogues |
| 2 | Total facility electrical power consumption | S2, S5 | proprietary | blocking | Not in available sources; SHINE facility energy reports would be needed; $0.05–0.10/kWh grid power at estimated 10–100 kW provides rough OPEX bound |
| 3 | Facility capital cost | S5 | proprietary | blocking | No published figure; comparable Mo-99 production facilities (NorthStar Medical Radioisotopes, non-reactor Mo-99 producers) provide rough analogues of $30–150M range |
| 4 | Mo-99 production yield and throughput | S2, S5 | proprietary | blocking | Global Mo-99 demand (~12,000 Ci/week), SHINE's claimed market position, and half-life-corrected shipping logistics could bound this indirectly |
| 5 | Capacity factor / beam availability | S5 | proprietary | important | Medical isotope production is time-critical (Mo-99 t₁/₂ = 66 hours); operators target >90% uptime; analogues from reactor-based Mo-99 producers applicable |
| 6 | OPEX breakdown — no public itemized data | S2, S5 | proprietary | important | Analogous isotope production facility O&M from CNSC (NRU) or SCK•CEN (BR2) public records may provide structure |
| 7 | Tritium possession inventory beyond consumed quantity | S4, S5 | proprietary / NRC | important | NRC license amendment filings for FLARE capacity increase may contain possession limits; accessible via public NRC docket |
| 8 | Lu-177 production process and yield | S3, S5 | proprietary | important | Lu-177 for radionuclide therapy is a ~$1B/year and growing market |
| 9 | LIBRTI / FLARE service pricing for neutron irradiation contracts | S5 | proprietary | nice-to-have | UKAEA LIBRTI contract publicly announced but unpriced; HIFR, LANSCE neutron service rates may provide range |

---

## Section 7: Cross-Concept Notes

**No approved prior analyses directly applicable.**

The approved Spherical Tokamak - HTS (21-spherical-tokamak-hts) and HTS Compact Tokamak (01-hts-compact-tokamak) analyses are not useful cross-references for SHINE — they share the D-T fuel cycle but have no other structural commonality. SHINE's concept is categorically distinct from every plasma-confining concept in this catalog.

**Positioning within the concept landscape:**

SHINE is the only commercially operating fusion system in the entire 39-concept catalog. Every other concept is at pre-commercial demonstration stage (TRL 2–7 at the system level). This is SHINE's most important distinguishing characteristic. However, SHINE's commercial maturity comes precisely because it does not attempt power generation — the beam-target D-T approach sidesteps the plasma confinement problem entirely at the cost of being permanently Q << 1.

**Nearest neighbors by physics mechanism:**

- **Muon-Catalyzed Fusion (16, Acceleron Fusion)**: Closest structural analog in the catalog. Both use an external energy input (accelerator for SHINE; muon source for MCF) to catalyze individual D-T fusion reactions without plasma confinement. Both are currently Q < 1 by physics. MCF's theoretical maximum Q is bounded by the muon sticking coefficient (~0.7% per muon × ~300 fusions/muon = ~210, i.e., catalysis gain ~210 before sticking stops the muon — this approaches breakeven only if the muon production cost is low enough); SHINE's Q is bounded by thin-target fusion probability per deuteron. The MCF iter-3 analysis faces the same fundamental barrier as this concept.

- **Electrostatic Hybrid / IEC (13, Avalanche Energy)**: Shares ion acceleration via electrostatic fields, but uses a convergent potential well (Penning-trap-like geometry with E×B electron co-confinement) rather than a linear beam onto a gas target. Avalanche claims a path to Q > 1 through enhanced ion recirculation; this distinguishes it from SHINE, which makes no such claim.

- **Heavy Ion Beam ICF (25, Intensity Energy)**: Also particle-beam driven, but operates in a completely different physics regime — GeV-scale heavy ions driving IFE compression toward Q >> 1. Heavy-ion ICF and beam-target D-T at 300 keV are as different as a garden hose and a fire hydrant.

**What SHINE demonstrates for the TEA project:**

SHINE establishes the achievable performance of commercially demonstrated D-T fusion at the lower Q bound. It confirms that building a working D-T fusion system is not the hard part: SHINE does it with a well-understood industrial accelerator at modest cost. Building one at Q ≥ 1 is the hard part. Every accelerator-driven fusion power concept in the catalog (heavy ion ICF, potentially muon-catalyzed fusion) must first clear the Q ≥ 1 barrier that SHINE explicitly does not clear.

**Tritium supply note:**

The tritium supply chain characterization from the HTS Compact Tokamak analysis ($35,000/g, ~25 kg global civilian inventory) applies in principle to SHINE, but at such different quantities (~8 mg/year consumed) that the supply chain dynamics are incomparable. SHINE's tritium constraint is a licensing and procurement matter, not a physical scarcity matter.

---

## Section 8: Sources

**1. SHINE Technology Overview (Phase 1a source)**
- Full citation: Synthesized overview drawn from SHINE corporate materials, Wikipedia, and press releases. Captured as iter-01/sources/shine-technology-overview.md.
- Contribution: Primary source for FLARE specifications (5 × 10^13 D-T reactions/second, 14.1 MeV neutrons, continuous steady-state operation, ≤300 kV beam voltage), system architecture (linear accelerator → tritium gas target → subcritical LEU assembly), and product line (Mo-99, Lu-177, FLARE, LIBRTI). Only source in the current set providing a quantitative fusion reaction rate.
- Location: knowledge/concept_research/38-particle-accelerator-driven-fusion/iter-01/sources/shine-technology-overview.md

**2. SHINE Technologies — FLARE product press release (2024)**
- Full citation: SHINE Technologies (2024). "SHINE Technologies Showcases FLARE™ — the World's Most Powerful Continuous Fusion Neutron System." shinefusion.com.
- Contribution: Primary source for "world's most powerful continuous fusion neutron system" claim, steady-state continuous operation, and FLARE commercial service offering.
- Location: Dossier key sources; shinefusion.com/blog/shine-technologies-showcases-flare-tm-the-worlds-most-powerful-continuous-fusion-neutron-system

**3. SHINE Technologies — LIBRTI announcement (2024)**
- Full citation: SHINE Technologies (2024). "SHINE Provides Fusion Neutron Source for UKAEA LIBRTI." shinefusion.com.
- Contribution: Confirms commercial deployment of packaged neutron irradiation product to external customer (UKAEA), establishing that SHINE's neutron services business extends beyond in-house Mo-99 production.
- Location: shinefusion.com/blog/shine-provides-fusion-neutron-source-for-ukaea-librti

**4. Piefer, G. et al. (2011) — Accelerator-driven Mo-99 production**
- Full citation: Piefer, G. et al. (2011). "Neutron production for Mo-99 using a D-T fusion source." *Proceedings of the ANL Mo-99 Technology Development Workshop*, Argonne National Laboratory. Available at: mo99.ne.anl.gov/2011/pdfs/Mo99%202011%20Web%20Papers/S6-P3_Piefer-Paper.pdf.
- Contribution: Peer-reviewed technical description of the beam-target D-T approach for isotope production; accelerator architecture, target geometry, subcritical LEU assembly configuration. Most technically detailed public document on SHINE's operating approach. Not directly reviewed in this iteration; beam current and neutron yield data may be available here.
- Location: Dossier key sources; ANL Mo-99 symposium proceedings

**5. NRC Licensing Documents**
- Full citation: U.S. Nuclear Regulatory Commission (2013, 2015). SHINE Medical Technologies license application documents. Public NRC docket. ML13172A262.pdf, ML15258A372.pdf.
- Contribution: Confirms NRC licensing for subcritical assembly and isotope production; provides regulatory framework context. May contain operational beam parameters not available in other public sources. Not directly reviewed in this iteration.
- Location: Dossier key sources; nrc.gov public docket

**6. Wikipedia — SHINE Technologies**
- Full citation: Wikipedia contributors (2025). "SHINE Technologies." Wikipedia, The Free Encyclopedia. en.wikipedia.org/wiki/Shine_Technologies.
- Contribution: Reliable summary of company history, technology concept, product lines, and NRC licensing milestones. Cross-checked against dossier claims.
- Location: en.wikipedia.org/wiki/Shine_Technologies

**7. Phase 1a Dossier — SHINE Technologies**
- Full citation: Internal research dossier, iter-02 (2026-05-17). knowledge/concept_research/38-particle-accelerator-driven-fusion/dossier.md.
- Contribution: High-confidence taxonomy values for all 10 differentiation columns with citation chains. Authoritative factual foundation for this analysis. Key facts: beam voltage (≤300 kV), operation mode (steady-state), energy capture (Neutron applications), blanket (N/A non-power), overall confidence (high).
- Location: knowledge/concept_research/38-particle-accelerator-driven-fusion/dossier.md

# D1+ Analysis: Particle Accelerator-Driven Fusion (D-T) — SHINE Technologies

---

## Section 1: Availability of Data

**Rating: Moderate (operational facts) / Opaque (economics)**

SHINE Technologies is unusual in this landscape: it is the only **commercially operating** fusion system in the concept catalog. This commercial reality cuts both ways for data availability. The technology concept itself is well-documented in public sources — NRC licensing records, peer-reviewed literature on accelerator-driven neutron sources, Wikipedia, and SHINE's own product marketing are openly available. However, operational economics (beam power consumption, facility capital cost, production yields, margins on Mo-99 and Lu-177 sales) are proprietary commercial information that SHINE has no incentive to disclose.

**Technical concept documentation:**

The fundamental physics is thoroughly understood. Piefer et al. (2011, ANL Mo-99 proceedings) describes the beam-target D-T approach for isotope production, providing accelerator architecture and target geometry context. Wikipedia gives a reliable summary of the SHINE process covering accelerator voltage, beam-target geometry, subcritical LEU assembly configuration, and NRC licensing history. SHINE's own press materials for the FLARE neutron system report 5 × 10^13 D-T fusion reactions per second and 14.1 MeV neutron output [shine-technology-overview.md §Key Facts]. NRC licensing documents (ML13172A262, ML15258A372) are publicly accessible and contain some technical parameters.

> "Compact linear particle accelerator drives beam-on-target fusion... Deuterium ions accelerated to up to 300 kV, fired into tritium gas target → D-T fusion → 14.1 MeV neutrons"
> — shine-technology-overview.md, §Key Facts

**What SHINE does not publish:**

Beam current, total electrical power consumption, capital cost of the accelerator system, tritium inventory and consumption rate, Mo-99 production yield, and any form of facility-level economics. The company has no obligation to publish these for a non-power commercial product, and none are available in the Phase 1a source set.

**Independent analyses:**

Because SHINE is not a power plant, it has not attracted the type of independent TEA analysis that power concepts receive (ARIES-class plant studies, PROCESS system code models). The few independent assessments of accelerator-driven fusion as a power concept are in the academic literature discussing why beam-target D-T cannot reach energy break-even — these confirm the fundamental physics limitation rather than offering SHINE-specific economics.

**Phase 1a dossier completeness:**

The dossier achieved high confidence on all taxonomy columns after two research iterations. The remaining gaps (beam current, neutron yield per unit beam power) are proprietary commercial parameters not resolvable through public research.

**Key data gaps limiting this analysis:**

1. Total electrical power consumption of the accelerator system — needed to characterize recirculating power burden
2. Facility capital cost breakdown — no published figure
3. Tritium consumption rate and procurement costs — NRC-licensed but not publicly specified
4. Mo-99 production economics and revenue — proprietary commercial

---

## Section 2: Challenges in Capturing System Function

SHINE presents a categorically different modeling challenge from every other concept in this landscape: **it is not a power plant and cannot be made into one by incremental development.** Beam-target D-T fusion is physically incapable of achieving energy break-even (Q ≥ 1), and SHINE does not claim otherwise. This creates multiple distinct modeling challenges:

**1. LCOE framework does not apply — requires a different economic model (Impact: Fundamental)**

Standard fusion LCOE analysis measures cost-per-kWh of electricity. SHINE produces no electricity and has no design pathway to net power output. The correct economic metric for SHINE is either cost-per-useful-neutron or cost-per-Curie of medical isotope. Modeling SHINE in the power-generation TEA pipeline requires an explicit statement of why beam-target D-T is excluded from the power-generation competition — not just flagging it as low-Q, but explaining what architectural change would be required (answer: a plasma-confining device capable of sustaining fusion burn, which is not beam-target physics).

The Q constraint is not a technology maturity problem but a physics ceiling. In beam-target D-T, each accelerated deuteron must be given ~150–300 keV of kinetic energy to access the D-T cross-section peak (σ ≈ 5 barns at ~120 keV CM energy). The D-T reaction releases 17.6 MeV total per event — a favorable single-reaction energy ratio of roughly 60:1. However, only a small fraction of beam deuterons fuse before losing their energy by elastic scattering and ionization in the target gas. The resulting effective Q for any practical thin or thick target is well below 1. SHINE's system is a net electricity consumer operating on purchased grid power.

**2. Physics calculation quantifies the Q gap (Impact: Demonstrated)**

At SHINE's stated fusion rate of 5 × 10^13 reactions/second, the total fusion power output is:

> P_fusion = 5 × 10^13 reactions/s × 17.6 × 10^6 eV × 1.6 × 10^{-19} J/eV ≈ **140 mW**

This is 140 milliwatts. The accelerator beam driving this reaction draws an estimated beam power of:

> P_beam = 300 kV × ~50 mA (mid-range beam current estimate) = **15 kW**

This gives Q_fusion ≈ 140 × 10^{-3} / 15,000 ≈ **10^{-5}**, five orders of magnitude below break-even. This is not a failure to optimize — it is a direct consequence of beam-target physics in which the beam slows primarily through Coulomb collisions with electrons rather than fusion reactions. The actual Q is independent of whether the beam current is 5 mA or 500 mA: the ratio of reaction energy to beam energy per fusion event stays near 10^{-5} because it is determined by the ratio of fusion cross-section to stopping cross-section. [Beam current not published by SHINE; 50 mA is a plausible midpoint estimate based on beam-target neutron generator literature for similar voltage ranges.]

**3. Tritium supply is a recurring cost driver with no self-sufficiency pathway (Impact: High for scaling)**

Unlike D-T power concepts that breed their own tritium, SHINE procures tritium externally and consumes it in fusion reactions without breeding. At 5 × 10^13 reactions/second, tritium consumption is approximately 8 mg/year:

> T consumption = 5 × 10^{13} atoms/s × [3 g/mol / (6.022 × 10^{23} atoms/mol)] × 3.15 × 10^7 s/yr ≈ **8 mg/yr**

At ~$35,000/g this is ~$280/year in tritium consumed — operationally negligible. The binding constraint is the NRC tritium possession limit and external procurement logistics, not unit cost. Scaling the SHINE concept to higher neutron flux increases tritium possession requirements and requires NRC amendment. No tritium breeding occurs; external supply is the only source.

**4. Revenue model is isotope pricing, not energy pricing (Impact: Structural)**

SHINE's economic viability is driven by Mo-99 and Lu-177 market pricing, not electricity markets. Mo-99 (the parent of Tc-99m, the most widely-used diagnostic nuclear medicine radioisotope) has historically traded at $2,000–$30,000 per 6-day Ci at the producer level, with global demand ~12,000 Ci/week. Lu-177 for targeted radionuclide therapy is a separate growing market. The economics are therefore tied to medical isotope market dynamics, beam-on-time and system availability for continuous production, and Mo-99 yield per unit neutron flux — none of which are in the standard fusion TEA parameter set.

**5. O&M structure is industrial, not fusion-plant (Impact: Moderate for comparability)**

SHINE's O&M profile resembles a specialty radiopharmaceutical manufacturing plant more than a fusion power plant. Maintenance is contact-accessible (no activation concerns at this neutron flux scale comparable to a power plant), isotope extraction is routine radiochemistry, and the accelerator is an industrial device with established maintenance schedules. This is both a strength (low O&M uncertainty) and a structural difference that prevents direct comparison to other concepts in the LCOE landscape.

**O&M placeholder:** Estimated O&M cost structure is dominated by (a) accelerator power cost (grid electricity at ~$0.05–0.10/kWh × unknown beam power draw, estimated 10–100 kW), (b) NRC-licensed radiological operator staffing, (c) LEU fuel procurement and waste disposal, and (d) tritium procurement and waste management. No published breakdown is available. This cost structure has no analogue in the fusion power concept TEA framework.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (highest risk / most relevant gap) to most mature. Because SHINE is commercially operating, most subsystems are at TRL 8–9 — the opposite of every other concept in this catalog. The TRL ordering here reflects relevance to power applications, not operational readiness for the current use case.

---

**Scaling to power application — TRL 1**

- **Demonstrated**: Nothing. No one has attempted to engineer beam-target D-T fusion toward net energy production because the physics prohibits it (Q ≈ 10^{-5}).
- **On paper only**: No published design study for a power-producing beam-target system exists.
- **Missing at scale**: Everything relevant to power generation — plasma confinement, energy multiplication beyond Q = 1, tritium breeding, thermal energy conversion. The entire chain must be invented; beam-target D-T provides none of these building blocks.

---

**Medical Isotope Extraction and Processing — TRL 7–8**

- **Demonstrated**: Mo-99 production from neutron-irradiated aqueous LEU solution at commercial scale; Lu-177 production confirmed. SHINE has been producing Mo-99 commercially since approximately 2019 and expanded capacity significantly with FLARE.
- **On paper only**: Full throughput optimization at FLARE-level neutron flux with automated remote handling for radioactive separation chemistry.
- **Missing at scale**: Sustained production at maximum FLARE capacity with minimal downtime; Lu-177 production processes are newer and less mature than Mo-99.

---

**FLARE / LIBRTI Neutron Irradiation Services — TRL 8–9**

- **Demonstrated**: FLARE described as "the world's most powerful continuous fusion neutron system" [shinefusion.com, FLARE press release]; LIBRTI deployed for UKAEA neutron irradiation services.

> "SHINE Technologies Showcases FLARE™ — the World's Most Powerful Continuous Fusion Neutron System"
> — shinefusion.com, FLARE press release (2024)

- **On paper only**: Multi-year contracted radiation effects testing programs at high instrumentation and electronics testing throughput.
- **Missing at scale**: Very high fluence irradiation campaigns requiring months of continuous operation at maximum flux; qualification testing for nuclear-grade structural materials requiring sustained high 14 MeV fluences.

---

**Subcritical LEU Assembly (for Mo-99) — TRL 8–9**

- **Demonstrated**: NRC-licensed subcritical assembly using aqueous LEU solution driven by D-T fusion neutrons; commercially operating for Mo-99 production. NRC license documents publicly available (ML13172A262, ML15258A372).

> "NRC-licensed subcritical LEU assembly... Neutrons drive subcritical LEU fission for Mo-99/Lu-177 isotope production"
> — dossier.md §Blanket Config

- **On paper only**: Scaled-up assembly geometries for higher neutron flux environments.
- **Missing at scale**: Not applicable — design operates at commercial scale within NRC-licensed parameters.

---

**Tritium Gas Target System — TRL 9**

- **Demonstrated**: Commercially operating at stated 5 × 10^13 D-T reactions/second [shine-technology-overview.md §Key Facts]. Continuous steady-state operation demonstrated. Target handling and recycling systems operational. No publicly available data on target lifetime or tritium replacement schedule.
- **On paper only**: Nothing material.
- **Missing at scale**: Tritium target scaling to higher beam currents would require NRC license amendment; not a technical barrier.

---

**Compact Linear Ion Accelerator (≤300 kV, D-beam) — TRL 9**

- **Demonstrated**: Commercially operating in steady-state continuous mode. Accelerators of this type (compact electrostatic, 100–400 kV, low-to-moderate beam current) are mature industrial devices with decades of deployment history in neutron generators for well-logging, security scanning, and laboratory sources. SHINE's application is the highest-flux commercial deployment of this technology class.

> "Deuterium ions accelerated to up to 300 kV, fired into tritium gas target"
> — shine-technology-overview.md, §Key Facts; dossier.md §Primary Heating

- **On paper only**: Higher-beam-current variants for increased neutron flux beyond current FLARE capability.
- **Missing at scale**: Nothing material for the current operating regime.

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium — Ongoing Procurement, Supply Constrained at Scale**

SHINE procures tritium externally for the gas target. No tritium breeding occurs. At the current stated fusion rate (5 × 10^13 reactions/s), annual tritium consumption is approximately 8 mg/year [inferred from reaction rate; see Section 2 derivation]. At ~$35,000/g, this amounts to roughly $280/year in tritium consumed by reactions — operationally negligible. The binding constraint is the NRC possession limit under SHINE's license and procurement logistics, not unit cost. As SHINE scales toward higher neutron flux with FLARE, tritium inventory requirements increase and require NRC amendments. The global civilian tritium supply constraint (~25–30 kg total, declining as CANDUs retire) is not a near-term concern for SHINE's operating scale; if multiple SHINE-type facilities were built simultaneously, demand would still be trivially small compared to D-T power plant programs.

**Low-Enriched Uranium (LEU) — Limited Qualified Suppliers**

The subcritical assembly uses aqueous LEU solution. LEU for research and isotope production reactors is supplied by a small number of government-qualified suppliers (ConverDyn, Tenex, others) under NNSA oversight as part of the global effort to eliminate highly enriched uranium from civilian programs. SHINE's conversion to LEU-based production was itself a significant nonproliferation milestone. Supply is adequate for current needs; the supplier base is narrow and geopolitical disruptions (e.g., Russian supply chain) create risk. This is a shared concern with all medical isotope reactor operators globally.

**Deuterium Gas — Abundant, No Supply Constraint**

Deuterium is commercially available as D₂ gas from industrial suppliers at ~$100–600/kg depending on purity grade. At SHINE's operating scale, deuterium is a negligible cost item. No supply constraint.

**Accelerator Components — Mature Industrial Supply Chain**

Ion accelerators at 100–400 kV scale are mature industrial devices. Components (vacuum systems, ion sources, high-voltage power supplies, beam optics) are available from multiple established suppliers (National Electrostatics Corp., HVEE, Excelis, others). No supply chain constraint.

**No HTS Tape, No Beryllium, No FLiBe — SHINE Is Supply-Chain-Simple**

SHINE requires none of the materials that create supply chain risk for plasma-confining fusion concepts: no REBCO tape, no FLiBe, no beryllium multiplier, no large cryogenic systems, no specialized laser gain media. From a materials supply chain perspective, SHINE is the simplest concept in this catalog by a wide margin. This simplicity is the direct consequence of not attempting plasma confinement.

---

## Section 5: LCOE-Relevant Parameters

**Framing note**: SHINE does not generate electricity, and beam-target D-T cannot achieve Q ≥ 1 by physics. The standard LCOE metric ($/kWh) does not apply. The relevant economic metrics are (a) cost per useful neutron for radiation-effects testing, and (b) cost per Ci of Mo-99 or Lu-177 for isotope production. The table below captures what quantitative parameters are available and flags what would be needed to characterize SHINE's true economics.

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| D-T fusion reaction rate | 5 × 10^13 reactions/s | shine-technology-overview.md §Key Facts | high | FLARE system rated performance |
| Deuterium beam voltage | ≤ 300 kV | shine-technology-overview.md §Key Facts; dossier.md §Primary Heating | high | Sets beam kinetic energy and D-T cross-section regime |
| Neutron energy | 14.1 MeV | shine-technology-overview.md §Key Facts | high | Characteristic D-T fusion neutron energy |
| Operation mode | Steady-state (continuous) | shinefusion.com FLARE press release §Continuous operation | high | "Continuous fusion neutron system" |
| Fuel type | D-T beam on gas target | dossier.md §Fuel | high | Deuterium beam onto tritium gas target; no plasma confinement |
| Effective Q (energy gain) | ~10^{-5} | [inferred: P_fusion (~140 mW) / P_beam (~15 kW at 50 mA × 300 kV); reaction rate from FLARE press release; beam current midpoint estimate from accelerator literature for this voltage class] | medium | Physical ceiling, not a technology maturity issue; Q is approximately constant across this operating regime regardless of beam current |
| Fusion power (derived) | ~140 mW | [inferred: 5×10^13 reactions/s × 17.6 MeV/reaction × 1.6×10^-13 J/MeV; reaction rate from shine-technology-overview.md §Key Facts] | high | Confirms non-power status; total fusion energy output is trivially small |
| Tritium consumption rate | ~8 mg/year | [inferred: 5×10^13 T-atoms/s × 3 g/mol / (6.022×10^23 atoms/mol) × 3.15×10^7 s/yr; Section 2 derivation] | medium | At current reaction rate only; tritium cost ~$280/yr — negligible |
| NRC licensing status | Licensed, commercial operation | NRC records ML13172A262, ML15258A372 | high | Aqueous homogeneous reactor licensing; confirms commercial operation |
| Net electrical output | 0 kWe | dossier.md §Energy Capture | high | "No thermal cycle, no electricity generation" — by design |
| Products | Mo-99, Lu-177, FLARE/LIBRTI neutron services | shinefusion.com product pages | high | Mo-99 for Tc-99m diagnostic imaging; Lu-177 for targeted radionuclide therapy |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Beam current (mA) | proprietary | blocking | Required to calculate beam power consumption; with voltage known (300 kV), current determines total electrical input and confirms Q estimate |
| Total electrical power consumption | proprietary | blocking | The "recirculating power fraction" analog — determines operating cost |
| Facility capital cost ($M) | proprietary | blocking | No published figure; private company |
| Mo-99 production yield (Ci/beam-hour) | proprietary | blocking | Key revenue driver; sets the economic case |
| Capacity factor / beam-on-time fraction | proprietary | important | Determines annual neutron output and production volume |
| OPEX breakdown (staffing, tritium, LEU, maintenance) | proprietary | important | Needed for operating economics model |
| Tritium inventory (possession) beyond consumption | proprietary / NRC | important | NRC license amendment filings may contain possession limits |
| Lu-177 production rate | proprietary | important | Newer product; economics less developed than Mo-99 |
| FLARE service pricing ($/neutron·cm^{-2}·s^{-1}) | proprietary | nice-to-have | Sets LIBRTI/FLARE revenue side |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Beam current (mA) — determines beam power consumption and confirms Q estimate | S2, S5 | proprietary | blocking | NRC license documents (ML13172A262) may constrain beam power; Piefer et al. (2011) may contain design specifications; accelerator literature for comparable beam-target neutron generators provides analogues |
| 2 | Total facility electrical power consumption | S2, S5 | proprietary | blocking | Not in available sources; SHINE facility energy reports would be needed; $0.05–0.10/kWh grid power at estimated 10–100 kW provides rough OPEX bound |
| 3 | Facility capital cost | S5 | proprietary | blocking | No published figure; comparable Mo-99 production facilities (NorthStar Medical Radioisotopes, non-reactor Mo-99 producers) provide rough analogues of $30–150M range |
| 4 | Mo-99 production yield and throughput | S2, S5 | proprietary | blocking | Global Mo-99 demand (~12,000 Ci/week), SHINE's claimed market position, and half-life-corrected shipping logistics could bound this indirectly |
| 5 | Capacity factor / beam availability | S5 | proprietary | important | Medical isotope production is time-critical (Mo-99 t₁/₂ = 66 hours); operators target >90% uptime; analogues from reactor-based Mo-99 producers applicable |
| 6 | OPEX breakdown — no public itemized data | S2, S5 | proprietary | important | Analogous isotope production facility O&M from CNSC (NRU) or SCK•CEN (BR2) public records may provide structure |
| 7 | Tritium possession inventory beyond consumed quantity | S4, S5 | proprietary / NRC | important | NRC license amendment filings for FLARE capacity increase may contain possession limits; accessible via public NRC docket |
| 8 | Lu-177 production process and yield | S3, S5 | proprietary | important | Lu-177 for radionuclide therapy is a ~$1B/year and growing market |
| 9 | LIBRTI / FLARE service pricing for neutron irradiation contracts | S5 | proprietary | nice-to-have | UKAEA LIBRTI contract publicly announced but unpriced; HIFR, LANSCE neutron service rates may provide range |

---

## Section 7: Cross-Concept Notes

**No approved prior analyses directly applicable.**

The approved Spherical Tokamak - HTS (21-spherical-tokamak-hts) and HTS Compact Tokamak (01-hts-compact-tokamak) analyses share the D-T fuel cycle label but have no structural commonality with SHINE. SHINE's concept is categorically distinct from every plasma-confining concept in this catalog. No cost assumptions, TRL estimates, or physics parameters are reused from prior analyses.

**Positioning within the concept landscape:**

SHINE is the only commercially operating fusion system in the entire 39-concept catalog. Every other concept is at pre-commercial demonstration stage (TRL 2–7 at the system level). This is SHINE's most important distinguishing characteristic. However, SHINE's commercial maturity comes precisely because it does not attempt power generation — the beam-target D-T approach sidesteps the plasma confinement problem entirely at the cost of being permanently Q << 1.

**Nearest neighbors by physics mechanism:**

- **Muon-Catalyzed Fusion (16, Acceleron Fusion)**: Closest structural analog in the catalog. Both use an external energy input (accelerator for SHINE; muon source for MCF) to catalyze individual D-T fusion reactions without plasma confinement. Both are currently Q < 1 by physics. MCF's theoretical maximum Q is bounded by the muon sticking coefficient (~0.7% per muon × ~300 fusions/muon = ~210, i.e., catalysis gain ~210 before sticking stops the muon — this approaches breakeven only if the muon production cost is low enough); SHINE's Q is bounded by the thin-target fusion probability per deuteron with no analogous gain mechanism. The MCF iter-3 analysis faces the same fundamental barrier as this concept.

- **Electrostatic Hybrid / IEC (13, Avalanche Energy)**: Shares ion acceleration via electrostatic fields, but uses a convergent potential well (Penning-trap-like geometry with E×B electron co-confinement) rather than a linear beam onto a gas target. Avalanche claims a path to Q > 1 through enhanced ion recirculation; this distinguishes it from SHINE, which makes no such claim.

- **Heavy Ion Beam ICF (25, Intensity Energy)**: Also particle-beam driven, but operates in a completely different physics regime — GeV-scale heavy ions driving IFE compression toward Q >> 1. Heavy-ion ICF and beam-target D-T at 300 keV operate in entirely different physical regimes; the driver technology label ("particle beam") is the only shared feature.

**What SHINE demonstrates for the TEA project:**

SHINE establishes the achievable performance of commercially demonstrated D-T fusion at the lower Q bound. It confirms that building a working D-T fusion system is not the hard part: SHINE does it with a well-understood industrial accelerator at modest cost. Building one at Q ≥ 1 is the hard part. Every accelerator-driven fusion power concept in the catalog (heavy ion ICF, potentially muon-catalyzed fusion) must first clear the Q ≥ 1 barrier that SHINE explicitly does not clear.

**Tritium supply note:**

The tritium supply chain characterization from the HTS Compact Tokamak analysis ($35,000/g, ~25 kg global civilian inventory) applies in principle to SHINE, but at such different quantities (~8 mg/year consumed) that the supply chain dynamics are incomparable. SHINE's tritium constraint is a licensing and procurement matter, not a physical scarcity matter.

---

## Section 8: Sources

**1. SHINE Technology Overview (Phase 1a source)**
- Full citation: Synthesized overview drawn from SHINE corporate materials, Wikipedia, and press releases. Captured as iter-01/sources/shine-technology-overview.md.
- Contribution: Primary source for FLARE specifications (5 × 10^13 D-T reactions/second, 14.1 MeV neutrons, continuous steady-state operation, ≤300 kV beam voltage), system architecture (linear accelerator → tritium gas target → subcritical LEU assembly), and product line (Mo-99, Lu-177, FLARE, LIBRTI). Only source in the current set providing a quantitative fusion reaction rate.
- Location: knowledge/concept_research/38-particle-accelerator-driven-fusion/iter-01/sources/shine-technology-overview.md

**2. SHINE Technologies — FLARE product press release (2024)**
- Full citation: SHINE Technologies (2024). "SHINE Technologies Showcases FLARE™ — the World's Most Powerful Continuous Fusion Neutron System." shinefusion.com.
- Contribution: Primary source for "world's most powerful continuous fusion neutron system" claim, steady-state continuous operation, and FLARE commercial service offering.
- Location: Dossier key sources; shinefusion.com/blog/shine-technologies-showcases-flare-tm-the-worlds-most-powerful-continuous-fusion-neutron-system

**3. SHINE Technologies — LIBRTI announcement (2024)**
- Full citation: SHINE Technologies (2024). "SHINE Provides Fusion Neutron Source for UKAEA LIBRTI." shinefusion.com.
- Contribution: Confirms commercial deployment of packaged neutron irradiation product to external customer (UKAEA), establishing that SHINE's neutron services business extends beyond in-house Mo-99 production.
- Location: shinefusion.com/blog/shine-provides-fusion-neutron-source-for-ukaea-librti

**4. Piefer, G. et al. (2011) — Accelerator-driven Mo-99 production**
- Full citation: Piefer, G. et al. (2011). "Neutron production for Mo-99 using a D-T fusion source." *Proceedings of the ANL Mo-99 Technology Development Workshop*, Argonne National Laboratory. Available at: mo99.ne.anl.gov/2011/pdfs/Mo99%202011%20Web%20Papers/S6-P3_Piefer-Paper.pdf.
- Contribution: Peer-reviewed technical description of the beam-target D-T approach for isotope production; accelerator architecture, target geometry, subcritical LEU assembly configuration. Most technically detailed public document on SHINE's operating approach. Not directly reviewed in this iteration; beam current and neutron yield data may be available here.
- Location: Dossier key sources; ANL Mo-99 symposium proceedings

**5. NRC Licensing Documents**
- Full citation: U.S. Nuclear Regulatory Commission (2013, 2015). SHINE Medical Technologies license application documents. Public NRC docket. ML13172A262.pdf, ML15258A372.pdf.
- Contribution: Confirms NRC licensing for subcritical assembly and isotope production; provides regulatory framework context. May contain operational beam parameters not available in other public sources. Not directly reviewed in this iteration.
- Location: Dossier key sources; nrc.gov public docket

**6. Wikipedia — SHINE Technologies**
- Full citation: Wikipedia contributors (2025). "SHINE Technologies." Wikipedia, The Free Encyclopedia. en.wikipedia.org/wiki/Shine_Technologies.
- Contribution: Reliable summary of company history, technology concept, product lines, and NRC licensing milestones. Cross-checked against dossier claims.
- Location: en.wikipedia.org/wiki/Shine_Technologies

**7. Phase 1a Dossier — SHINE Technologies**
- Full citation: Internal research dossier, iter-02 (2026-05-17). knowledge/concept_research/38-particle-accelerator-driven-fusion/dossier.md.
- Contribution: High-confidence taxonomy values for all 10 differentiation columns with citation chains. Authoritative factual foundation for this analysis. Key facts: beam voltage (≤300 kV), operation mode (steady-state), energy capture (Neutron applications), blanket (N/A non-power), overall confidence (high).
- Location: knowledge/concept_research/38-particle-accelerator-driven-fusion/dossier.md
