Now I have everything I need. Let me write the gap assessment.

---

# Gap Assessment: Orbital Levitated Dipole (D-He3)

## Overall Readiness
**Rating**: Insufficient Data

**Summary**: Zephyr Fusion is a pre-prototype, 2-person startup (founded 2025, YC F25) that has disclosed almost nothing beyond the existence of their concept. The academic heritage from LDX, Hasegawa 1987, and a 2026 D-T dipole reactor study (arxiv 2602.20564) provides a credible physics foundation, but Zephyr itself has not confirmed fuel type, heating method, energy conversion pathway, performance targets, or any cost-relevant engineering detail. Critically, the concept is an *orbital* power plant — a fundamentally different techno-economic system than any terrestrial fusion reactor — with no established LCOE methodology, no cost analogues, and launch cost dominating the capital structure in ways the standard fusion LCOE framework does not capture. A D1+ analysis can be written but must be heavily inference-based and clearly flagged as such.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Poor

**Available**:
- YC launch page (`yc-launch-page.md`): confinement principle, HTS magnet scale, Falcon 9 deployability, megawatt-class power target, $30M claimed cost for magnetized volume exceeding ITER, founder credentials
- NASASpaceFlight forum (`nasaspaceflight-forum-discussion.md`): community skepticism inventory — identifies every undisclosed element (energy conversion, shielding, power beaming path, tritium breeding)
- LDX/RT-1 heritage (`levitated-dipole-technical-background.md`): demonstrated physics of levitated dipole confinement, heating methods used in experiments, τₑ ~ R² scaling, high-beta properties
- arxiv 2602.20564 (OpenStar D-T dipole reactor study, via `dipole-reactor-heating-energy-conversion.md`): the only published modern dipole reactor design — 667 MW fusion power, 208 MW net electric, ICRH baseline, sacrificial shield lifetime (~1 year)
- Hasegawa & Chen 1987 (PPPL-2627, via `dipole-reactor-heating-energy-conversion.md`): original D-He3 dipole reactor concept with direct energy conversion at separatrix, space propulsion parameters (1 kW/kg specific power)
- ARIES-III D-He3 tokamak study (referenced via `dipole-reactor-heating-energy-conversion.md`): 47% net efficiency hybrid rectenna + thermal conversion, synchrotron radiation recovery concept
- Comprehensive web survey (`zephyr-fusion-web-sources-2026.md`): exhaustive confirmation that no ARPA-E/DOE funding, no patents, no conference papers, no additional technical disclosures exist as of March 2026

**Missing**:
- Any primary Zephyr technical disclosure beyond the YC launch page
- Confirmation of fuel type, heating method, or energy conversion approach from the company
- Any published plant study for a D-He3 *orbital* dipole
- Performance targets (Q, ion temperature, plasma density, power output)
- Timeline and milestones

**Gaps**:
- Company technical disclosure (fuel, heating, conversion) — `proprietary` — **blocking** (forces all key parameters to be inferred)
- No orbital fusion power plant study of any kind exists — `truly-unknown` — **blocking** (no cost methodology precedent)
- No Zephyr patents or conference presentations — `proprietary` — **important** (no mid-level technical detail available)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial (physics understood; engineering and economics not)

**Available**:
- The levitated dipole confinement physics is well-documented in LDX/RT-1 experiments and the arxiv 2602.20564 reactor study. The τₑ ~ R² scaling, high-beta advantage, and disruption-free steady-state operation are all experimentally grounded.
- The D-He3 fuel cycle rationale — aneutronic primary reaction, 85% energy in charged particles, no blanket requirement — is clearly established in Hasegawa 1987 and consistent with orbital operation.
- Direct charged particle conversion at the separatrix is physically well-motivated and the geometry is cited as "particularly suitable" for D-He3 in the academic literature.
- The core insight (space vacuum eliminates vacuum vessel as energy loss channel) is documented and acknowledged by the community as physically valid.

**Missing**:
- This concept doesn't fit the standard LCOE framework at all. The "plant" is an orbiting spacecraft with no grid connection — LCOE in $/kWh is only meaningful if power beaming losses and beaming infrastructure costs are included. No methodology exists for this.
- D-He3 requires ~60 keV ion temperatures (vs. ~20 keV for D-T), implying a challenging heating power requirement. Without target plasma parameters, heating power cannot be estimated.
- The relationship between orbital altitude, drag makeup, plasma confinement geometry, and power output is completely uncharacterized.
- No description of how synchrotron radiation is managed (tolerable power load? recovered? radiated?)
- The power beaming pathway (fusion energy → direct conversion → microwave/laser → ground/customer) has multiple efficiency stages, each unspecified.

**Gaps**:
- No applicable LCOE framework for orbital power delivery — `truly-unknown` — **blocking** (requires methodological invention before the model can be scoped)
- D-He3 plasma ignition/sustainment conditions not characterized for dipole geometry at orbital scale — `not-yet-sourced` (search: Hasegawa 1987 PPPL-2627 full text, arxiv dipole D-He3 reactor studies) — **important**
- Power beaming losses and infrastructure cost — `truly-unknown` for this application — **blocking** (determines whether the concept can ever produce cheap electricity at the customer)
- Heating power requirement and recirculating power fraction — `derivable` from D-He3 reactivity data + target plasma parameters, but no targets disclosed — **important**

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial (heritage physics demonstrated; most engineering subsystems at TRL 1-2)

**Available**:
- **Dipole confinement physics**: TRL 4-5. LDX (MIT/Columbia, 2004-2012) and RT-1 (U. Tokyo) demonstrated stable levitated dipole confinement with ECRH heating, density/pressure profiles consistent with theory, and high-beta operation.
- **HTS magnet technology**: TRL 6-7 for terrestrial magnets. REBCO tape technology is commercially available; tokamak projects (SPARC, Commonwealth Fusion) have demonstrated high-field HTS magnets at meter scale. Space qualification of HTS magnets is lower (TRL 3-4).
- **ECRH heating (ground-based)**: TRL 7-8 for terrestrial application. Demonstrated on LDX. Gyrotrons at industrial scale exist.
- **NBI**: TRL 8-9 for terrestrial application. Mature technology.

**Missing** (no data available for any of these):
- **Orbital HTS magnet deployment**: No demonstration of superconducting magnets sustained in LEO. Passive cooling in LEO thermal environment is uncharacterized for this application.
- **Direct energy conversion at dipole separatrix**: TRL 1-2. Described theoretically in Hasegawa 1987 and ARIES-III but never built or tested at any scale.
- **Microwave/laser power beaming from orbit**: Contested TRL (various demos exist for small-scale terrestrial and near-orbit). MW-class continuous power beaming is undemonstrated.
- **Heating systems in space vacuum**: ECRH/ICRH/NBI in space environment — no heritage. RF systems in vacuum would need different engineering.
- **Plasma fueling/refueling at orbital platform**: Unaddressed.
- **Cryogenic maintenance in LEO**: Sustained HTS magnet operation over years requires thermal management strategy not described.

**Gaps**:
- Direct energy conversion technology at reactor scale — `truly-unknown` for orbital application — **blocking**
- Space-qualified superconducting magnet (sustained multi-year operation) — `not-yet-sourced` (search: NASA/ESA superconducting magnet space qualification efforts, CERN for space, etc.) — **important**
- Heating subsystem in space environment — `truly-unknown` — **important**
- Fuel delivery / refueling logistics — `truly-unknown` — **important**

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial (He-3 supply well-documented elsewhere; orbital supply chain is unique)

**Available**:
- **HTS tape (REBCO)**: Supply chain is constrained but exists. The broader fusion industry (SPARC, many startups) is building this supply chain. Meter-scale coil for a single satellite is a small quantity relative to terrestrial reactor magnets.
- **He-3 supply**: The D-He3 fuel choice has a well-documented supply gap in the literature. Terrestrial He-3 comes primarily from tritium decay (~15 kg/year from US/Russia weapons programs). Lunar He-3 mining remains speculative. This supply constraint is a fundamental challenge for any D-He3 concept, not unique to Zephyr.
- **D (deuterium)**: Abundant, electrochemically separable from seawater. Not a supply concern.

**Missing**:
- No estimate of He-3 consumption rate for a MW-class D-He3 dipole (requires plasma parameters)
- No consideration of D-He3 fuel delivery logistics to orbital platform
- Orbital logistics supply chain (launch cadence for fuel resupply) — novel problem with no precedent
- Space-rated power electronics for direct conversion at MW scale — no supply chain exists

**Gaps**:
- He-3 supply path to orbital platform — `truly-unknown` — **blocking** (if the fuel can't be delivered to orbit at scale, the concept can't operate)
- He-3 fuel consumption rate — `derivable` from D-He3 reactivity + plasma parameters once targets are known — **important**
- Space-rated MW-class direct conversion hardware — `truly-unknown` — **important**
- REBCO tape quantity for meter-scale coil — `derivable` (small relative to terrestrial projects, manageable supply risk) — **nice-to-have**

---

### 5. LCOE Parameter Extraction
**Coverage**: Poor — almost no LCOE-relevant parameters available; standard LCOE framework may not apply

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|-----------|-------------|--------|------------|
| Magnetized plasma volume | ">ITER" (>840 m³ implied) | YC launch page | medium |
| Capital cost (magnet/coil only) | <$30M | YC launch page | low (unverified claim) |
| Net electrical output | "MW-class" | YC launch page | low (no number given) |
| Confinement scaling | τₑ ~ R² | LDX heritage | high (physics) |
| Launch vehicle | Falcon 9 (rideshare) | YC launch page | medium |
| D-He3 charged particle fraction | ~85% | Hasegawa 1987 heritage | high (physics) |
| ARIES-III D-He3 net efficiency (tokamak analogue) | 47% | ARIES-III via `dipole-reactor-heating-energy-conversion.md` | medium (different geometry) |
| D-T dipole reactor analogue: net electric | 208 MW from 667 MW fusion | arxiv 2602.20564 | medium (different fuel) |
| D-T dipole analogue: sacrificial shield replacement | ~1 year cycle | arxiv 2602.20564 | medium (different fuel/geometry) |
| Hasegawa 1987 space parameter | 1 kW/kg specific power | `levitated-dipole-technical-background.md` | low (1987 design estimate) |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Capital cost breakdown (magnet, launch, direct conversion, power beaming) | proprietary + truly-unknown | blocking | $30M claim likely magnet-only; launch + power beaming system dominate |
| Falcon 9 launch cost (rideshare) | not-yet-sourced | blocking | SpaceX pricing; $2-5k/kg to LEO is public — mass of system needed |
| System mass (coil + support structure + heating + power electronics) | proprietary | blocking | Determines launch cost, which may dominate |
| Target fusion power (MW) | proprietary | blocking | "MW-class" is all that's stated |
| Target Q (fusion gain) | proprietary | blocking | Required to compute recirculating power and net output |
| Heating power requirement | derivable (once Q and fusion power known) | blocking | ECRH at 30-40% efficiency is a major recirculating power cost |
| Direct conversion efficiency (orbital separatrix) | truly-unknown | blocking | Never been built; 60-80% claimed in theory |
| Power beaming efficiency (fusion → delivered electricity) | truly-unknown | blocking | Each step (conversion → beaming → receipt) has large loss; likely 20-40% end-to-end |
| Power beaming infrastructure cost (ground/orbit receiver) | truly-unknown | blocking | May dominate system LCOE |
| Capacity factor / on-orbit lifetime | proprietary | important | No satellite lifetime assumptions stated; degradation of HTS coil in LEO radiation environment unknown |
| Operating cost (fuel resupply, orbital maintenance) | truly-unknown | blocking | On-orbit maintenance is either impossible or extremely expensive |
| He-3 fuel consumption rate | derivable | important | Requires plasma parameters |
| Replacement schedule (if any components fail) | truly-unknown | important | On-orbit replacement logistics are unique problem |

---

## Source Recommendations

1. **Hasegawa & Chen 1987 (PPPL-2627) full text** — cited in dossier, may contain quantitative D-He3 dipole reactor parameters (plasma density, temperature, power, direct conversion design). Priority: high. *Verify availability at INIS/IAEA: https://inis.iaea.org/records/05wfd-4pb29 — confirm before citing.*

2. **ARIES-III D-He3 fusion reactor study** — cited in dossier (`fti.neep.wisc.edu/pdf/fdm815.pdf`). Full study likely contains capital cost breakdown, direct conversion efficiency, LCOE estimate. The most relevant analogue for D-He3 energy conversion economics, even though it's a tokamak. Priority: high. *Link appears in source documents — confirm file exists before using.*

3. **arxiv 2602.20564 (OpenStar D-T dipole reactor, 2026)** — already cited, partially extracted. Contains cost estimates for D-T terrestrial dipole. Can be used as lower bound / structural analogue for magnet and plasma-facing component costs, with heavy caveats. Priority: medium. *Exists — referenced in multiple source files.*

4. **MIT LDX program publications** — `https://www-internal.psfc.mit.edu/ldx/pubs/` cited in sources. May contain performance scaling analyses useful for extrapolating to reactor scale. Search for LDX design reports and FESAC presentations. Priority: medium. *Internal MIT URL — may not be publicly accessible; unverified — confirm existence before searching.*

5. **Space-based power systems LCOE literature** — No specific paper cited. Search: "space-based solar power LCOE", "SBSP techno-economic analysis", "orbital power plant economics". These are the closest cost-methodology analogues for Zephyr's business model (orbital source + power beaming to ground). This literature provides the only credible framework for estimating launch-cost-dominated capital structure. Priority: high for methodology. *Unverified — confirm existence before searching.*

6. **Zephyr Fusion new disclosures** — Monitor for: conference papers (FPA, IAEA FEC, APS-DPP), DOE/ARPA-E grant announcements, patent filings (USPTO search: "levitated dipole" + "orbital" + "fusion"), investor updates. As of March 2026, none exist. *No specific paper to cite — ongoing monitoring recommended.*

---

## Summary

**Proceed to full analysis with heavy caveats — but restructure the LCOE model scope first.**

The physics section (Section 2) can be written with moderate confidence, drawing on LDX/RT-1 heritage and the arxiv 2602.20564 reactor study. The maturity section (Section 3) can clearly delineate demonstrated physics (TRL 4-5) from unbuilt engineering subsystems (TRL 1-2). The materials section (Section 4) has enough to discuss He-3 supply and REBCO.

The LCOE model (Deliverable 2) requires a methodological decision before coding: **standard fusion LCOE ($/kWh assuming grid connection) does not apply to an orbital power plant.** The analysis must either (a) frame LCOE in terms of delivered power at the customer endpoint — including power beaming losses and ground/orbit receiver infrastructure — or (b) analyze specific power (W/kg) as the more natural figure of merit for this concept, with LCOE back-derivation for a hypothetical customer. The Hasegawa 1987 "1 kW/kg" figure is the only existing target.

The $30M claim from the YC launch page is for the confinement volume (likely the magnet alone), not a system cost. The actual capital cost is dominated by unknowns: system mass × launch cost/kg + direct conversion hardware + power beaming transmitter. Without these, the quantitative model must be explicit that it is computing a lower bound on system capital cost and parametrically sweeping the unknown fractions.

**Recommend**: Acquire the ARIES-III and Hasegawa 1987 full texts before writing the analysis — both are cited in the dossier and likely contain quantitative parameters (plasma conditions, direct conversion efficiency, reactor-scale cost estimates) that would substantially improve the analysis quality. Without them, every LCOE-relevant number will be first-principles inference.

## Structured summary (machine-readable)

```yaml
overall_rating: "Insufficient Data"
blocking_count: 10
important_count: 3
counting_method: "section_5_missing_parameters"
section_coverage:
  availability_of_data:       "Poor"
  system_function:            "Partial (physics understood; engineering and economics not)"
  subsystem_maturity:         "Partial (heritage physics demonstrated; most engineering subsystems at TRL 1-2)"
  materials_supply_chain:     "Partial (He-3 supply well-documented elsewhere; orbital supply chain is unique)"
  lcoe_parameter_extraction:  "Poor — almost no LCOE-relevant parameters available; standard LCOE framework may not apply"
```
