---
ID: 14-magnetized-target-fusion-pneumatic-compression
Concept: Magnetized Target Fusion - Pneumatic Compression (D-T)
Company: General Fusion
Status: draft
Created: 2026-03-28
Approved-Date:
Reuses: [07-maglif, 01-hts-compact-tokamak, 21-spherical-tokamak-hts, 08-frc-w-direct-conversion]
---

# D1+ Analysis: Magnetized Target Fusion - Pneumatic Compression (D-T)
**Company: General Fusion**

---

## Section 1: Availability of Data

**Rating: Moderate**

General Fusion occupies an unusual position: it is one of the most technically distinctive private fusion companies, with an unconventional mechanical compression approach that is genuinely novel in the literature, yet has published selectively — enough to understand the concept and current milestones, not enough to construct a bottom-up LCOE model without significant inference.

**Peer-reviewed literature.** The FST 2025 paper (Dossier Key Source #1; DOI: 10.1080/15361055.2025.2526266) is the most substantial public technical document, covering tritium fuel cycle analysis for both lead-lithium eutectic (PbLi) and pure lithium (Li) liquid metal wall options. It confirms the commercial cavity diameter (~4 m), the pneumatic piston driver concept, and tritium inventory distributions — but does not disclose fusion gain, thermal efficiency, or capital cost. General Fusion has also published peer-reviewed results on plasma confinement time (>10 ms) and neutron yield during compression, demonstrating scientific progress without disclosing plant-level economics [general-fusion-technology-overview.md §Peer-reviewed Publications].

**Technical documentation.** The APS 2018 overview (Dossier Key Source #5) provides the most detailed public compression parameters: density 10²² → 10²⁵ ions/m³, temperature 0.1 → 10 keV, magnetic field 2 → 200 T, and a volume reduction of three orders of magnitude [dossier §Primary Heating]. This is the primary public anchor for the plasma physics parameters.

**IAEA FEC 2025 abstract** (Hildebrand et al.) documents LM26 milestone targets — 10 keV ion temperature by end-2025, Lawson criterion (nTτ > 10²¹ m⁻³·keV·s) by 2026 — and confirms the 50% plasma scale of LM26 relative to the commercial machine [general-fusion-iaea-fec-2025-abstract.md §LM26 Targets].

**Company communications.** Multiple press releases, LinkedIn posts, and journalistic coverage (TechCrunch, Hackaday, Interesting Engineering, 2025) document LM26 milestones — first plasma compression, neutron yield, lithium liner compression — but provide no quantitative cost data [general-fusion-lm26-milestones-2025.md §Timeline].

**Independent analyses.** No published independent techno-economic study exists for General Fusion's commercial concept. No equivalent of the ARIES or Z-IFE system code studies exists for this architecture. The concept's novelty means there is no directly analogous industrial technology to benchmark against.

**Data completeness.** The Phase 1a dossier achieves 100% coverage of the 12 schema differentiation columns, all at high confidence. However, the schema columns capture confinement family, driver type, and fuel cycle topology — not the LCOE-relevant plant parameters (gain, efficiency, capital cost breakdown). Those remain almost entirely proprietary or undisclosed.

**Key data gaps limiting analysis:**
- No published fusion gain (Q) or fusion power target
- No published thermal efficiency or Rankine cycle parameters
- No published capital cost estimate or subsystem cost breakdown
- Liquid metal composition (Li vs. PbLi) not finalized as of 2025
- Commercial compression system (pneumatic) never demonstrated — only the electromagnetic surrogate (LM26)

---

## Section 2: Challenges in Capturing System Function

The MTF-pneumatic approach presents a distinct challenge set compared to both MFE and IFE concepts. The compression mechanism, liquid metal wall, and pulsed-but-not-inertial operating regime all introduce modeling challenges without established analogues.

**1. The commercial compression system has never been built or tested (highest impact)**

LM26 demonstrates plasma physics at 50% scale using electromagnetic theta-pinch compression of a solid lithium liner — a deliberate surrogate that does not replicate the commercial concept. The commercial plant requires pneumatic steam-driven pistons to compress a flowing liquid metal vortex. These are fundamentally different mechanisms: the surrogate is electromagnetic, the commercial system is mechanical; the surrogate uses a solid liner, the commercial system uses a flowing liquid. The physics of plasma compression may be transferable, but the engineering of the liquid metal system — synchronization of dozens to hundreds of pistons to <1% timing error, formation and stability of a symmetric liquid metal vortex, clearing and reforming the cavity within 1 second — has not been demonstrated at any scale [dossier §Driver Technology, §Plasma State; general-fusion-fst-2025-fuel-cycles.md §Commercial Design].

> "Array of pneumatic piston drivers" — general-fusion-fst-2025-fuel-cycles.md, §Compression System Description

This creates a fundamental LCOE modeling challenge: the capital cost of the compression system — which is likely the dominant non-blanket cost driver — cannot be estimated from the LM26 demonstration. **Failure consequence: if synchronized piston operation in the flowing liquid metal environment proves infeasible at commercial scale, there is no fallback compression mechanism in the current design — the no-magnet cost advantage that distinguishes this concept from all MFE approaches would be lost, requiring a fundamental architecture change.**

**2. Rep rate gap: ~86,400× between demo and commercial target**

LM26 currently operates at approximately one compression event per day. The commercial target is ~1 Hz [general-fusion-lm26-milestones-2025.md §Repetition Rate]. This is not an engineering refinement — it is an entirely different regime. Pistons must cycle, liquid metal must flow and reform, plasma must be injected and conditioned, steam must be recharged, and the entire mechanical system must reset within ~1 second. No analogous pulsed mechanical system operates at this combination of spatial scale (~4 m), energy density, and repetition rate. The LCOE is proportional to (net energy per pulse × rep rate × capacity factor), making rep rate the single most leveraged parameter [dossier §Repetition Rate; analogy to 07-maglif §Pulsed Operation].

**3. Compression ratio shortfall**

Water-cavity compression tests (surrogate for liquid metal dynamics) achieved a compression ratio of ~8:1 against a commercial target of 12:1 — a 33% shortfall [general-fusion-technical-details.md §Compression System]. Whether this gap is closeable with design changes or reflects a fundamental geometric constraint is unknown. A 12:1 cavity volume compression is required to achieve the target plasma conditions (10⁻³ to 1 relative volume = 10³× density and temperature scaling). Under-compression propagates directly into failure to achieve fusion conditions, not a cost parameter — making this a binary risk rather than a continuous uncertainty. **Failure consequence: if 12:1 compression cannot be achieved in a flowing liquid metal environment, the plasma cannot reach fusion temperatures and densities — this is a physics viability failure, not a cost uncertainty that can be parameterized in an LCOE model.**

**4. Liquid metal composition unresolved, with cost implications**

Both pure lithium (Li) and lead-lithium eutectic (Pb-83Li-17, or PbLi) remain under evaluation for the commercial wall [general-fusion-fst-2025-fuel-cycles.md §Liquid Metal Options]. The choice affects:
- Tritium inventory distribution: Li design has >60% in blanket; PbLi design has >80% in isotope separation system (ISS)
- Tritium extraction technology and capital cost of the ISS
- Thermal hydraulics and heat transfer to the steam cycle
- Materials compatibility with structural components
- Fire and explosion hazard (pure Li is highly reactive with water/air; PbLi is more benign)
- Neutron multiplication (PbLi provides additional neutrons from Pb; pure Li does not)

> "The tritium inventory distributions differ significantly between PbLi and Li designs: the LLE design has >80% of in-process inventory in the isotope separation system, while the Li design has >60% in the blanket material" — general-fusion-fst-2025-fuel-cycles.md, §Tritium Inventory Analysis

This is a cost model branching decision that must be treated as a scenario parameter, not a fixed value.

**5. No published gain or energy balance**

Unlike most fusion concepts at this stage, General Fusion has not published a design-point Q value, fusion power, or energy balance. The 300 MWe commercial target implies a thermal power of roughly 750–900 MWth at 33–40% thermal efficiency — but neither efficiency target nor fusion power has been disclosed. The recirculating power fraction (driven primarily by plasma injector energy, piston recharge, and pumping power for the liquid metal circuit) is entirely unknown. This makes the LCOE model structurally underdetermined: net electrical output cannot be derived from first principles without Q and η.

**6. Thermal cycle integration with liquid metal wall**

The liquid metal is the primary heat carrier (collecting both neutron energy and direct plasma energy from the compression event), which means the Rankine steam cycle is directly coupled to the liquid metal temperature and flow rate. The heat exchange between flowing Li or PbLi and the steam generator is non-trivial — Li reacts violently with water, requiring intermediate heat exchangers. The specific steam cycle parameters (temperature, pressure, thermal efficiency) have not been disclosed, preventing direct modeling of this cost component.

---

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

---

**Commercial Pneumatic Compression System (Piston Array + Liquid Metal Vortex) — TRL 2–3**

- **Demonstrated**: Water-cavity compression tests at surrogate scale; compression ratio ~8:1 (vs. 12:1 target); radial velocity >300 m/s [general-fusion-technical-details.md §Compression System]. No plasma in these tests.
- **On paper only**: Commercial-scale (4 m cavity) liquid metal vortex formation, stability, and uniformity; timing synchronization of dozens-to-hundreds of pistons to <1% error; liquid metal jetting and debris control after each pulse.
- **Missing at scale**: Repetitive operation at 1 Hz over plant lifetime; piston seal and wear performance under combined steam pressure + shock loading + activated environment; liquid metal vortex reformation within 1 second; full-scale validation that acoustic symmetry is achievable with the commercial piston geometry.

---

**Tritium Breeding and Extraction from Flowing Liquid Metal — TRL 2–3**

- **Demonstrated**: Analytical/computational analysis of tritium inventory for both Li and PbLi (FST 2025); generic liquid metal tritium extraction has been studied for ITER test blanket modules (Pb-17Li). TBR target of ~1.5 identified [dossier §Tritium Breeding; general-fusion-fst-2025-fuel-cycles.md §TBR Analysis].
- **On paper only**: Full tritium fuel cycle for either Li or PbLi design at GF's commercial scale; isotope separation system capital cost and tritium extraction efficiency for the specific flow rates and temperatures involved.
- **Missing at scale**: Integrated continuous tritium extraction at 1 Hz pulse rate; management of tritium permeation into steam circuit (Li/PbLi → steam generator interface is a major tritium containment challenge); tritium accounting at the ~1.5 kg/day production rate a 300 MWe plant would require [inferred: ~300 MW × 3.5 eV/reaction × unit conversion; analogue from 01-hts-compact-tokamak §Tritium Breeding].

---

**Compact Toroid (Spherical Torus) Plasma Injector — TRL 5–6**

- **Demonstrated**: PI3 injector demonstrated pre-compression parameters: ion temperature ~400 eV, density ~6×10¹⁹ m⁻³, energy confinement time >10 ms [general-fusion-iaea-fec-2025-abstract.md §Pre-Compression Baseline]. First plasma injection experiments ongoing at LM26 scale.
- **On paper only**: Compact toroid survival into the liquid metal cavity at commercial scale; CT formation reliability at 1 Hz injection rate; CT trajectory control into the compression zone.
- **Missing at scale**: Consistent shot-to-shot CT quality at 1 Hz with <X% variation (variation budget not published); CT injector lifetime under 10⁸ pulse cycling; plasma injector cost at production volume.

---

**Electromagnetic Compression Surrogate (LM26 Demo Only) — TRL 6**

Note: This is the *demonstration* subsystem, not the commercial one. Its maturity is relevant to validating the physics, not the engineering.

- **Demonstrated**: Theta-pinch electromagnetic compression of solid lithium liner achieves ion temperature and density increases during compression at 50% plasma scale (April 2025). 18 MJ electrical input per compression event. Neutron yield >600 million neutrons/second [general-fusion-lm26-milestones-2025.md §Milestones; general-fusion-technical-details.md §Compression Results]. Ion temperature approaching 10 keV target for 2025.
- **On paper only**: Achievement of Lawson criterion nTτ > 10²¹ m⁻³·keV·s (2026 target per IAEA FEC 2025 abstract).
- **Missing at scale**: This subsystem is a *scientific surrogate* and will not be used in the commercial plant. Its TRL is not transferable to the commercial pneumatic system.

---

**Liquid Metal Heat Transfer and Steam Rankine Cycle — TRL 4–5 (integrated)**

- **Demonstrated**: Steam Rankine cycle is TRL 9 as a commercial technology. Li and PbLi heat transfer loops have been operated in fission research (ITER TBM program uses Pb-17Li). Steam generators with intermediate heat exchangers (to isolate Li from water) have been built for sodium-cooled fast reactors (analogous but not identical) [analogue from 01-hts-compact-tokamak §Power Conversion].
- **On paper only**: Integration of liquid metal heat extraction with pulsed 1 Hz energy deposition from fusion; thermal management of pulsed heat loads in the liquid metal circuit; steam cycle thermal efficiency for this specific operating point.
- **Missing at scale**: Steam generation from a pulsed heat source at 1 Hz with liquid Li or PbLi primary; dynamic control of the steam-piston feedback loop (pistons are steam-driven, steam is generated from fusion heat — partial self-sustaining cycle); plant-level thermal efficiency measurement.

---

**Plasma-Facing Components / First Wall — TRL 5–6 (liquid metal provides self-replacing wall)**

- **Demonstrated**: The liquid metal liner is inherently self-renewing — it reforms each pulse, eliminating solid first-wall erosion as a traditional concern. This is a genuine advantage over solid-wall MFE concepts. Pure Li or PbLi flowing walls have been studied in NSTX-U and other MFE experiments.
- **On paper only**: Long-term compatibility of liquid metal with structural materials under combined fusion neutron flux + thermal cycling; activation of the Li or PbLi inventory over plant lifetime.
- **Missing at scale**: Liquid metal activation management (¹⁴ MeV neutrons activate Li → ³H production, confirmed feature; activate Pb → Pb isotopes, some long-lived); liquid metal purification and impurity management at scale.

---

## Section 4: Key Materials and Supply Chain Considerations

**Lithium (as liquid metal wall and tritium breeder)**

Lithium is the central material for this concept. The commercial design requires a large inventory of liquid Li or PbLi in continuous circulation. For a ~4 m spherical cavity with a ~1 m thick liquid metal shell, the liquid metal inventory is on the order of tens of tonnes per plant [inferred: 4/3π(2)³ − 4/3π(1)³ ≈ 29 m³ void; liquid Li density 0.51 g/cm³ → ~15 tonnes minimum; actual volume larger accounting for piping and heat exchangers; rough estimate ~50–100 tonnes Li equivalent].

Global lithium production is ~180,000 tonnes/year (2024, dominated by the battery industry). A fleet of 100 GW of MTF-pneumatic plants at 300 MWe each = ~330 plants; at ~100 tonnes Li per plant = ~33,000 tonnes Li inventory. This is a minor fraction of annual production, but the quality and isotopic requirements matter:

- **Li-6 enrichment**: Natural Li is 7.6% Li-6. For TBR = 1.5, significant Li-6 enrichment is required [dossier §Tritium Breeding; general-fusion-fst-2025-fuel-cycles.md §TBR Analysis]. Current Western Li-6 enrichment capacity is negligible — historically performed by Russia (Lesnoy plant) and China; US COLEX program was shut down in the 1960s. No large-scale Western enrichment capacity exists for fusion-fleet quantities. This is a supply chain risk shared with all D-T fusion concepts [analogue from 21-spherical-tokamak-hts §Li-6 Supply Chain].
- **Pure Li vs. PbLi trade-off**: Pure Li is more reactive (water, air → fire/explosion hazard) but offers higher tritium breeding and no Pb neutron capture complications. PbLi is safer to handle and has established supply chains (both Pb and Li are commodity materials) but requires the ISS to process the >80% tritium fraction in the separation system. The cost differential between these two options is a first-order LCOE branching decision [general-fusion-fst-2025-fuel-cycles.md §Material Selection].

**Lead (for PbLi option)**

If PbLi is selected, lead is required in large quantities (Pb-83Li-17 by atomic fraction → roughly 97% by mass = mostly lead). Lead is a commodity metal at ~$2/kg, produced at ~5 million tonnes/year globally. No supply chain bottleneck, but neutron activation of Pb produces hazardous and long-lived isotopes (²⁰⁶Pb, ²⁰⁷Pb → ²⁰⁴Tl, ²⁰³Hg pathways), creating radioactive waste management considerations not present in pure Li designs.

**Tritium (startup inventory)**

Standard D-T requirement: 1–5 kg startup inventory at ~$30,000/g. Current global tritium supply (~22 kg total, from CANDU reactors, declining). Startup tritium for a fleet requires either early plants to operate with tritium deficit (burning DD initially) or purchasing from the declining CANDU supply. Shared constraint with all D-T fusion concepts [analogue from 01-hts-compact-tokamak §Tritium Supply].

**Structural alloys (piston materials, vessel walls)**

Steam pistons at commercial scale are mature industrial technology. The challenge is the combined environment: pistons must withstand neutron activation, thermal shock from compression events, potential liquid metal splash, and the mechanical fatigue of ~3×10⁷ cycles per year at commercial rep rate [inferred: 1 Hz × 3×10⁷ s/year]. No standard materials qualification exists for this combined loading. Tungsten or tungsten alloys may be required near the plasma zone; standard steel for outer structures. No supply chain bottleneck anticipated for quantities at this scale, but qualification time and cost are non-trivial.

**No HTS tape, no cryoplant, no exotic driver materials**

Unlike tokamak/stellarator concepts, General Fusion's commercial design uses no superconducting magnets — the confinement is provided by the mechanical pressure of the liquid metal, not external magnetic coils. The LM26 electromagnetic surrogate uses conventional copper coils. This eliminates REBCO tape supply constraints (~$30–100/kA-m, limited production) as a concern [dossier §Magnet Type; contrast with 01-hts-compact-tokamak §REBCO Supply Chain]. No laser components, no cryogenic gas inventories, no beryllium (unlike FLiBe-based designs) required. This is a notable supply chain simplification relative to MFE and FLiBe-using MIF concepts.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output (commercial target) | 300 MWe | general-fusion-lm26-milestones-2025.md §Commercial Target; dossier §Power Output | high | "~150,000 Canadian homes"; single plant target |
| Repetition rate (commercial) | ~1 Hz | dossier §Repetition Rate; general-fusion-lm26-milestones-2025.md §Rep Rate | high | All recent sources converge; original "1–10 Hz" range has narrowed |
| Cavity diameter (commercial) | ~4 m | general-fusion-fst-2025-fuel-cycles.md §Cavity Geometry | high | Stated in peer-reviewed FST 2025 paper |
| Pre-compression plasma temperature | ~0.1 keV | dossier §Primary Heating; APS 2018 overview cited therein | high | CT injection conditions |
| Post-compression target temperature | ~10 keV | general-fusion-iaea-fec-2025-abstract.md §2025 Target; dossier §Primary Heating | high | LM26 2025 target; commercial design requirement |
| Pre-compression ion density | ~10²² ions/m³ | dossier §Primary Heating (APS 2018) | high | Pre-compression CT density |
| Post-compression ion density (target) | ~10²⁵ ions/m³ | dossier §Primary Heating (APS 2018) | high | Required for D-T fusion rate |
| Magnetic field: pre-compression | ~2 T | dossier §Primary Heating (APS 2018) | high | CT magnetic field at injection |
| Magnetic field: post-compression (target) | ~200 T | dossier §Primary Heating (APS 2018) | high | Field amplified by volume compression |
| Volume compression ratio (target) | ~1000× (3 orders of magnitude) | dossier §Primary Heating (APS 2018) | high | Density increase from 10²² to 10²⁵ |
| Compression timescale | ~0.7–1 ms | general-fusion-technical-details.md §Compression System | high | Radial velocity >300 m/s |
| Compression ratio achieved (water tests) | ~8:1 | general-fusion-technical-details.md §Compression System | high | Target is 12:1; 33% shortfall in surrogate tests |
| Liquid metal options under evaluation | Li, PbLi (both) | general-fusion-fst-2025-fuel-cycles.md §Material Options | high | Not finalized; affects fuel cycle cost |
| Tritium breeding ratio (target) | ~1.5 | dossier §Tritium Breeding (fusionconclusion.com) | medium | From third-party technical analysis |
| Energy confinement time (pre-compression, LM26) | >10 ms | general-fusion-technology-overview.md §Confinement Time; general-fusion-iaea-fec-2025-abstract.md | high | Peer-reviewed milestone; baseline before compression |
| LM26 compression energy input | 18 MJ electrical | general-fusion-technical-details.md §Compression System | high | LM26 coils; demo system only |
| LM26 neutron yield achieved | >600 million n/s | general-fusion-technical-details.md §Compression Results | high | Experimental result; not commercial yield |
| LM26 plasma scale | 50% of commercial | general-fusion-iaea-fec-2025-abstract.md §LM26 Description | high | Explicitly stated in IAEA FEC 2025 abstract |
| Fusion thermal power | ~750–900 MWth | [inferred: 300 MWe ÷ 0.33–0.40 thermal efficiency; efficiency range from analogue thermal cycles] | low | Depends entirely on undisclosed thermal efficiency |
| Energy per pulse | ~250–900 MJ | [inferred: Fusion thermal power ÷ 1 Hz rep rate; 750–900 MWth ÷ 1 pulse/s = 750–900 MJ/pulse; minus recirculating power] | low | Wide range reflects undisclosed efficiency and gain |
| Capacity factor | 75–90% | [analogue: 07-maglif analysis; 01-hts-compact-tokamak analysis citing Araiinejad & Shirvan 2025 §Capacity Factor Sensitivity] | low | Dominant LCOE sensitivity; mechanical system maintenance unknown |
| Thermal efficiency (Rankine) | ~33–40% | [analogue: steam Rankine baseline; 07-maglif §Power Conversion cites ~40% for combined Brayton-Rankine; pure steam typically 33–36%] | low | Not published; depends on liquid metal exit temperature |
| Fusion gain Q | Unknown | — | — | Not disclosed by General Fusion; required for energy balance |
| HTS magnet system + cryoplant capital (CAS22) | $0 — eliminated by design | Section 7 TEA Implications; contrast with 07-maglif §No External Magnets; dossier §Magnet Type | high | No superconducting coils or cryoplant in commercial design; liquid metal pressure provides confinement. Direct zeroing of a cost account that dominates tokamak/stellarator LCOE (~$500–1000M in HTS compact tokamak, per 01-hts-compact-tokamak §Capital Cost Structure) |
| Consumable cost per pulse (target/liner) | $0 — liquid metal recycles; no destroyed targets | Section 7 TEA Implications; contrast with 07-maglif §Target Factory where $0.10–0.25/target is a key cost driver | high | Liquid metal liner reforms each pulse; no target consumed per shot. Eliminates the target factory cost structure that defines IFE/MagLIF LCOE models |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion gain Q (plasma physics) | proprietary | blocking | Cannot close energy balance without this; not published by GF at any stage |
| Fusion power (thermal, commercial design) | proprietary | blocking | Follows from Q; 300 MWe target published but thermal basis undisclosed |
| Thermal efficiency (steam Rankine at operating point) | proprietary | blocking | Liquid metal exit temperature and cycle parameters not disclosed |
| Recirculating power fraction | proprietary | blocking | Piston recharge energy, plasma injector energy, pumping — no basis for estimate |
| Capital cost (total or by subsystem) | proprietary | blocking | No published estimate; no analogous industrial system |
| Compression system capital cost (pistons, vessel) | truly-unknown | blocking | No cost study for this novel architecture; no surrogate technology at this scale |
| Liquid metal composition (commercial selection) | proprietary | important | Li vs. PbLi affects fuel cycle cost, materials cost, and safety classification |
| Capacity factor (maintenance-driven) | truly-unknown | important | Mechanical compression system maintenance schedule completely unpublished |
| Li-6 enrichment level (commercial) | not-yet-sourced | important | Required for TBR calculation; FST 2025 discusses inventory but not enrichment fraction |
| Steam Rankine cycle parameters (T, P, efficiency) | proprietary | important | Operating temperatures and steam conditions not disclosed |
| Plasma injector unit cost and lifetime | truly-unknown | important | CT injector at 1 Hz cycling: cost, reliability, replacement schedule unknown |
| Piston wear rate and replacement schedule | truly-unknown | important | Major O&M cost driver; no experimental data at relevant conditions |
| Tritium permeation rate (Li/PbLi → steam circuit) | not-yet-sourced | important | Tritium barrier design and cost not disclosed; literature values exist for Pb-17Li |
| Commercial plant capital cost ($/kWe) | truly-unknown | nice-to-have | Would require a complete bottom-up cost study |

### Modeling Approach and Key Hypotheses

**Top LCOE sensitivity parameters for this concept:**

1. **Repetition rate** (commercial target: 1 Hz). The single highest-leverage parameter. Annual net energy = energy per pulse × rep rate × capacity factor × thermal efficiency. A 2× shortfall in rep rate (0.5 Hz vs. 1 Hz) doubles the capital cost per delivered kWh from identical plant capital. The 86,400× gap between LM26's current ~1 shot/day and the commercial 1 Hz target is not a continuous parameter to optimize — it is a binary regime transition requiring entirely new mechanical engineering.

2. **Capacity factor** (analogue: 75–90% from 01-hts-compact-tokamak §Capacity Factor Sensitivity). The second multiplicative term in the LCOE denominator, and the one most sensitive to the mechanical compression system's unknown maintenance schedule. For a novel piston-and-vortex architecture operating at 1 Hz with no industrial precedent, unplanned downtime scenarios could easily push capacity factor to 50–60%, which would be the dominant LCOE penalty relative to MFE concepts.

3. **Fusion gain Q** (entirely undisclosed). The unlock parameter for the energy balance. Without Q, net electrical output cannot be derived even if rep rate and thermal efficiency are assumed. Q determines whether the recirculating power fraction (piston recharge + plasma injector + liquid metal pumping) allows net positive generation at all. A minimum Q ≳ 1/η_thermal is required for breakeven; commercial viability likely requires Q ≳ 5–10 [inferred from ARPA-E Q × η_recovery > 1 formulation; analogue from 08-frc-w-direct-conversion §Energy Balance].

**Key testable hypotheses:**

- *H1 — Compression driver dominance*: The pneumatic compression system (vessel, piston array, steam recharge infrastructure) will constitute the dominant non-blanket capital account — analogous to the laser driver in IFE or the magnet system in tokamaks. This makes CAS27 (compression/driver system) the critical cost sensitivity, unlike tokamaks where CAS22 (magnet) and CAS26 (blanket) are the primary drivers. This hypothesis can be tested by parametric cost bounding: even at $200M for the compression system (well below large industrial machinery projects), it would dominate the plant at 300 MWe scale.

- *H2 — Liquid metal material choice as first-order LCOE branch*: The Li vs. PbLi selection creates bifurcating cost implications in (a) isotope separation system capital (ISS-dominant in PbLi, blanket-extraction-dominant in Li), (b) safety infrastructure capital (Li fire/explosion mitigation significantly more expensive than PbLi), and (c) tritium permeation control cost. These must be modeled as separate scenario branches, not a single parametric uncertainty.

- *H3 — Rep rate as viability threshold*: At 1 Hz with 300 MWe output and 80% capacity factor, the concept's LCOE is plausibly competitive with advanced fission if capital cost is moderate. At 0.1 Hz — a factor of 10 below commercial target — capital cost per delivered kWh increases 10× from identical plant capital investment, making the concept uncompetitive regardless of fuel cycle advantages. This is a qualitative threshold, not a continuous optimization.

**Explicit failure modes (pre-commercial physics/engineering gates — not TEA parameters):**

- *FM-1 — Compression ratio failure (Challenge #3)*: If 12:1 cavity compression cannot be achieved with flowing liquid metal at commercial cavity diameter (~4 m), the plasma cannot reach fusion conditions. This is a concept-level physics failure — it eliminates the concept from the TEA comparison regardless of cost assumptions, and cannot be represented as a sensitivity range in the LCOE model.

- *FM-2 — Commercial pneumatic system infeasibility (Challenge #1)*: If synchronized piston operation in the liquid metal environment proves mechanically infeasible (e.g., due to vortex instability, piston timing scatter, or acoustic asymmetry at scale), there is no demonstrated fallback compression mechanism for the commercial design. Loss of this bet eliminates the concept's primary differentiator — no-magnet, no-driver mechanical compression — and would require reverting to an electromagnetic driver architecture.

Both FM-1 and FM-2 represent binary gates that precede LCOE modeling. They should be tracked as explicit go/no-go flags in the TEA framework, not as uncertainty ranges.

**Recommendation — free-form parametric modeling:**

The 1costing framework (deriving costs by scaling from a reference plant with known subsystem breakdown) cannot be applied without first resolving the blocking unknowns (Q, thermal efficiency, compression system capital cost). No analogous industrial system exists. The appropriate modeling structure is:
- Anchor on the 300 MWe commercial output target
- Parameterize rep rate (0.1–2 Hz), capacity factor (50–90%), and thermal efficiency (33–40%) as the three primary LCOE sensitivity dimensions
- Treat Q as a threshold parameter: define minimum Q for net energy breakeven at each assumed η_thermal
- Develop bounding capital cost estimates using analogous industrial components (steam-driven compressor systems for very rough piston-array order-of-magnitude; industrial pressure vessel fabrication for cavity vessel) as floor estimates, acknowledging the novel engineering premium cannot be quantified from public data

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Fusion gain Q at commercial design point | S2, S5 | proprietary | blocking | General Fusion technical publications; IAEA FEC proceedings when available |
| 2 | Thermal efficiency and steam cycle parameters | S2, S5 | proprietary | blocking | GF technical publications; FST 2025 follow-on papers |
| 3 | Recirculating power fraction (piston recharge + injector + pumping) | S2, S5 | proprietary | blocking | Requires system design disclosure or independent engineering estimate |
| 4 | Capital cost structure for pneumatic compression system | S2, S3, S5 | truly-unknown | blocking | No published analogue; requires original engineering cost estimate |
| 5 | Compression ratio achievable in liquid metal (vs. 8 in water, target 12) | S2, S3 | proprietary | blocking | GF R&D publications; surrogate test reports |
| 6 | Liquid metal composition selection (Li vs. PbLi) | S2, S4, S5 | proprietary | important | GF commercial design announcement expected before LM26 completion |
| 7 | Capacity factor and maintenance schedule for mechanical compression system | S2, S5 | truly-unknown | important | No mechanical system at comparable scale/duty; requires original engineering study |
| 8 | Li-6 enrichment level and tritium breeding performance by composition | S4, S5 | not-yet-sourced | important | FST 2025 follow-on; ITER TBM program Pb-17Li data for PbLi case |
| 9 | Piston seal, wear, and replacement schedule in activated liquid metal environment | S3, S5 | truly-unknown | important | No data; requires dedicated R&D program |
| 10 | Plasma injector (CT) reliability and cost at 1 Hz duty cycle | S3, S5 | truly-unknown | important | No equivalent injector at this duty cycle; General Fusion internal R&D |
| 11 | Tritium permeation rate through liquid metal → steam generator interface | S3, S4 | not-yet-sourced | important | ITER TBM program (Pb-17Li permeation data); pure Li literature |
| 12 | Steam cycle thermal efficiency at specific liquid metal outlet temperature | S5 | derivable | important | Can be derived once Li/PbLi choice and operating temperature are known |
| 13 | Commercial plant capital cost ($/kWe, bottom-up) | S5 | truly-unknown | nice-to-have | No basis for estimate without items 1–6 above |
| 14 | Plasma injector energy per shot and electrical efficiency | S5 | proprietary | nice-to-have | Needed for recirculating power; current LM26 data is surrogate-only |

---

## Section 7: Cross-Concept Notes

Four approved prior analyses were available for cross-referencing.

### Differentiators vs. Conventional Tokamak (Reference Concept)

The table below consolidates key structural differences between General Fusion's MTF-pneumatic concept and a conventional D-T tokamak (e.g., CFS ARC). Classification: **Novel** = no precedent in commercial fusion; **Borrowed** = adapted from established technology in another domain; **Shared** = essentially identical to the tokamak reference.

| Differentiator | MTF-Pneumatic | Conventional Tokamak | Classification |
|---|---|---|---|
| Drive mechanism | Pneumatic/steam pistons compressing a liquid metal vortex | Inductive + auxiliary heating (NBI, ECRH, ICRH) | Novel |
| Confinement regime | Compression-driven pulsed magnetized target; magnetic field amplified by mechanical work | Steady-state toroidal magnetic confinement | Novel |
| Plasma-facing material | Self-renewing liquid metal liner (Li or PbLi); no solid first wall | Solid tungsten or beryllium PFCs; scheduled replacement every 1–2 years | Novel |
| Magnet type | None in commercial plant (confinement via mechanical compression; CT carries its own field) | HTS superconducting toroidal + poloidal coils; cryoplant required | Novel |
| Power delivery mode | Pulsed: ~1 pulse/second, energy deposited in ~1 ms; output smoothed by thermal mass | Quasi-continuous: plasma heating continuous, power output near-steady | Novel (borrowed from pulsed ICF concept) |
| Fuel cycle geometry | 4π solid-angle liquid metal wall acts as both breeder and heat carrier | Outboard blanket only (~1–1.5π solid angle); separate first wall structure | Novel |
| D-T fuel and tritium self-sufficiency | D-T, tritium bred in Li/PbLi liquid metal wall; TBR target ~1.5 | D-T, tritium bred in outboard Li blanket; TBR target ~1.05–1.15 | Shared (fuel); Novel (breeding geometry) |
| Energy conversion | Rankine steam cycle; conventional turbine-generator | Rankine steam cycle; conventional turbine-generator | Shared |

The most consequential differentiators for TEA are: (1) elimination of the magnet system and cryoplant, which removes the largest single capital account from a tokamak; (2) the liquid metal wall as combined breeding/heat-extraction element, which eliminates a separate blanket structure but introduces novel cost and engineering complexity; and (3) pulsed mechanical compression, for which no capital cost analogue exists. These are developed further in the TEA implications subsection below.

### Reused Frameworks

**From 07-maglif (MagLIF, D-T)**
The MagLIF analysis is the most structurally relevant prior work. Both concepts are pulsed MIF at ~1 Hz commercial target, with per-shot energy deposition and liquid-wall heat extraction. Several frameworks transfer directly:

- *Pulsed LCOE structure*: Annual energy output = yield/pulse × rep rate × capacity factor. Rep rate is the single largest LCOE lever — a 2× improvement in rep rate doubles annual energy output from identical capital. This multiplier structure applies identically here [07-maglif §Challenges].
- *Capacity factor as dominant sensitivity*: In MagLIF, no published plant-level availability data exists; the same is true here. The Araiinejad & Shirvan (2025) finding that capacity factor (75–90%) is the primary LCOE sensitivity for D-T fusion [01-hts-compact-tokamak §Capacity Factor Sensitivity] should be assumed to hold here as well.
- *No HTS/cryoplant advantage*: Both MagLIF and MTF-pneumatic avoid superconducting magnets, eliminating REBCO and cryoplant costs. This is a structural cost advantage over MFE concepts.

The key *divergence* from MagLIF: General Fusion uses no per-shot consumables in the commercial design (the liquid metal liner reforms each pulse; it is not destroyed). This is a structural OPEX advantage — MagLIF must address target and RTL destruction at 28M shots/year, while General Fusion's liquid metal is continuously recycled. The piston and plasma injector wear are the analog maintenance costs, but these are not per-shot disposables.

### TEA Implications by Differentiator

The table below maps each major differentiator (from the tokamak comparison above) to its cost direction, the affected CAS account(s), and the available quantitative basis.

| Differentiator | Cost Direction | Reasoning | CAS Account | Basis |
|---|---|---|---|---|
| No HTS magnet system or cryoplant | Capital **advantage** vs. tokamak | Eliminates CAS22 (magnet system) and associated CAS23 (cryoplant) entirely. REBCO tape at $30–100/kA-m and multi-GJ stored energy magnets are among the largest capital items in ARC-class tokamaks. | CAS22 ≈ $0 (vs. estimated $1–3B for ARC-class HTS plant) | 01-hts-compact-tokamak §HTS Cost; dossier §Magnet Type |
| No per-shot consumables | OPEX **advantage** vs. MagLIF | Liquid metal liner reforms each pulse; no destroyed targets or RTLs. MagLIF must fabricate ~28M targets/year at commercial rep rate. GF's per-shot materials OPEX is effectively zero for the plasma fuel; piston wear is the analogous recurring maintenance cost. | CAS60 (fuel cycle OPEX): minimal | 07-maglif §Consumables; analogue from 07-maglif §RTL Cost |
| Pneumatic compression driver | Capital **penalty** (unknown magnitude) | Novel architecture — no industrial analogue for synchronized piston array at 4 m scale, 1 Hz, in activated liquid metal environment. Likely the dominant non-blanket capital account. Cannot be estimated from public data; must be bounded via analogous industrial machinery. | CAS27 (compression/driver system): dominant unknown | Section 2 Challenge #1; no published estimate |
| Liquid metal wall as combined breeder + heat carrier | TEA impact: **mixed** | Advantage: eliminates separate blanket fabrication; 4π breeding geometry relaxes Li-6 enrichment vs. outboard blanket. Penalty: tritium permeation risk at Li/PbLi → steam interface requires costly double-walled intermediate heat exchangers (analogous to sodium-cooled fast reactor IHX). Thermal efficiency coupled to liquid metal outlet temperature — cannot be designed independently. | CAS26 (blanket): partially eliminated, merged into compression vessel; CAS22 heat exchange: IHX cost added | general-fusion-fst-2025-fuel-cycles.md §Blanket Integration; 21-spherical-tokamak-hts §Liquid Lithium Blanket |
| Pulsed operation (1 Hz) | LCOE **leverage factor** | Not a single line item but a multiplier on all capital costs via the energy denominator: LCOE ∝ capital / (annual energy) = capital / (E_pulse × rep_rate × CF). Any shortfall from 1 Hz propagates linearly into LCOE. At 0.5 Hz, capital cost per kWh doubles from identical plant capital. | Affects all accounts via capacity factor denominator | See H3 (modeling hypotheses above); 07-maglif §Rep Rate Sensitivity |
| Conventional Rankine steam cycle | **Cost-neutral** vs. tokamak | Steam turbine-generator is TRL 9, commodity pricing (~$400/kWe); identical cost structure to conventional D-T MFE plants. No cost advantage or penalty from this subsystem alone. | CAS24 (power conversion): conventional baseline | 07-maglif §Power Conversion; 01-hts-compact-tokamak §Power Conversion |

**From 08-frc-w-direct-conversion (FRC/Helion, D-He3)**
The FRC analysis highlights the rep rate scaling challenge — Helion's Trenta operates at ~0.002 Hz and must reach 1–2 Hz commercially. General Fusion faces an identical scaling factor (~86,400×). The ARPA-E energy balance formulation (Q × η_recovery must exceed 1 for net energy output) applies analogously here with thermal efficiency replacing direct conversion efficiency.

*Divergence*: Helion pursues direct electromagnetic energy recovery, avoiding the steam cycle. General Fusion's thermal cycle is more conventional but introduces steam generator tritium management concerns absent in Helion's design.

**From 01-hts-compact-tokamak (CFS ARC, D-T) and 21-spherical-tokamak-hts (Tokamak Energy ST-E1)**
The D-T tritium fuel cycle framework from Araiinejad & Shirvan (2025) is directly applicable: startup inventory requirements (1–5 kg at ~$30k/g), declining CANDU supply, TBR > 1.05 threshold for self-sufficiency. Applied to the MTF-pneumatic concept with TBR target ~1.5 — this is a generous margin that provides confidence in tritium self-sufficiency if the liquid metal breeding performance matches design analysis.

The spherical tokamak analysis covers liquid lithium blanket design (outboard-only, TBR = 1.2 with >90% Li-6 enrichment). General Fusion's design uses Li or PbLi as the *entire* wall (not just a blanket), providing ~4π solid angle coverage — superior breeding geometry that likely relaxes the Li-6 enrichment requirement compared to the tokamak case [21-spherical-tokamak-hts §Tritium Breeding; contrast with dossier §Tritium Breeding].

*Divergence*: HTS tokamak concepts use FLiBe (Li₂BeF₄), which has both Li and Be. General Fusion avoids beryllium entirely — eliminating FLiBe's supply chain constraints and toxicity concerns but forgoing Be's neutron multiplication benefit.

### Concept Family Context

General Fusion occupies a unique niche: it is the only major private fusion company pursuing *mechanical* (pneumatic/steam) compression as the primary energy delivery mechanism. Other MIF/MTF companies use pulsed electromagnetic systems (MagLIF/Pacific Fusion), laser-driven (various IFE approaches), or rail-gun plasma-jets (HyperJet/PJMIF). The mechanical approach has potential advantages in driver simplicity and cost but introduces engineering challenges — timing synchronization, liquid metal dynamics, piston lifetime — with no direct technology analogues.

---

## Section 8: Sources

1. **FST 2025: Fuel Cycles for Li and PbLi Walls in MTF Power Plant** (Hildebrand et al., Fusion Science and Technology, DOI: 10.1080/15361055.2025.2526266) — Primary peer-reviewed source. Confirms pneumatic piston array, ~4 m cavity, Li and PbLi options, tritium inventory distributions (>60% in blanket for Li, >80% in ISS for PbLi), TBR requirements. Found at: `exploration/phase_1a/research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-fst-2025-fuel-cycles.md`

2. **IAEA FEC 2025 Abstract: LM26 Results** (Hildebrand et al., IAEA Fusion Energy Conference 2025) — Peer-reviewed conference abstract. Confirms LM26 at 50% commercial plasma scale; 2025 target 10 keV; 2026 target Lawson criterion; electromagnetic theta-pinch surrogate for commercial pneumatic system. Found at: `exploration/phase_1a/research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-iaea-fec-2025-abstract.md`

3. **General Fusion Technology Overview** (General Fusion website, generalfusion.com/fusion-technology/) — Primary company source for concept description, liquid metal wall multifunctionality (compression medium, neutron absorber, tritium breeder, heat transfer), Marshall gun plasma injector. Found at: `exploration/phase_1a/research/14-magnetized-target-fusion-pneumatic-compression/iter-01/sources/general-fusion-technology-overview.md`

4. **General Fusion Technical Details** (aggregated from generalfusion.com and related sources) — Compression parameters: 0.7–1 ms timescale, >300 m/s radial velocity, 8:1 achieved vs. 12:1 target compression ratio in water tests; LM26 18 MJ coil energy; neutron yield >6×10⁸ n/s. Found at: `exploration/phase_1a/research/14-magnetized-target-fusion-pneumatic-compression/iter-01/sources/general-fusion-technical-details.md`

5. **General Fusion LM26 Milestones 2025** (aggregated company communications, 2025) — 300 MWe commercial target, ~1 Hz rep rate, ~150,000 home equivalent, 18-month assembly timeline. Found at: `exploration/phase_1a/research/14-magnetized-target-fusion-pneumatic-compression/iter-02/sources/general-fusion-lm26-milestones-2025.md`

6. **Phase 1a Dossier: MTF - Pneumatic Compression** (internal research synthesis, 2026-03-07) — Consolidates all schema column values with citations and confidence ratings; primary reference for compression parameters from APS 2018 overview. Found at: `exploration/phase_1a/research/14-magnetized-target-fusion-pneumatic-compression/dossier.md`

7. **APS 2018: Magnetized Target Fusion Overview at General Fusion** (General Fusion, APS DPP 2018, published PDF at generalfusion.com) — Key compression parameter table: density 10²² → 10²⁵ ions/m³, temperature 0.1 → 10 keV, magnetic field 2 → 200 T, 3 orders of magnitude volume compression. Cited via dossier §Primary Heating.

8. **07-maglif prior analysis** (internal D1+ analysis, this project) — Pulsed MIF LCOE framework, rep rate as dominant cost lever, per-shot consumable cost structure, FLiBe thick-liquid-wall concept, driver capital cost considerations, ~40% combined thermal efficiency baseline.

9. **01-hts-compact-tokamak prior analysis** (internal D1+ analysis, this project) — D-T tritium fuel cycle costing framework (Araiinejad & Shirvan 2025); capacity factor sensitivity finding; tritium startup inventory requirements; regulatory cost multiplier (Stewart & Shirvan 2.2×).

10. **21-spherical-tokamak-hts prior analysis** (internal D1+ analysis, this project) — Liquid lithium blanket design; Li-6 enrichment requirements; tritium extraction from liquid metal; vacuum degassing and permeation approaches; comparison of outboard-only vs. 4π solid angle tritium breeding geometry.

11. **COMSOL: Compressing the Timeline to a Fusion Future** (COMSOL News, 2023) — Commercial rep rate confirmation ("once per second in a commercial plant"); liquid metal wall heat capture pathway description (liquid metal → heat exchanger → steam → turbine). Cited via dossier §Repetition Rate, §Energy Capture.

12. **Fusion Conclusion: How General Fusion's Reactor Will Work** (fusionconclusion.com, independent technical analysis) — TBR target ~1.5 (only published TBR target for this concept). Cited via dossier §Tritium Breeding.

---

*Footnotes:*

[1] dossier §Primary Heating, citing APS 2018 overview: compression from 0.1 keV / 10²² m⁻³ to 10 keV / 10²⁵ m⁻³ represents 3 orders of magnitude density increase and 100× temperature increase — consistent with adiabatic heating scaling (T ∝ V^(−2/3(γ−1)) with γ~5/3 gives T ∝ n^(2/3), so 1000× density → ~100× temperature).

[2] general-fusion-fst-2025-fuel-cycles.md, §Tritium Inventory: ">80% of in-process tritium inventory in the isotope separation system" for PbLi design vs. ">60% in the blanket material" for Li design — this distinction has major implications for tritium handling capital cost and safety classification.

[3] general-fusion-technical-details.md, §Compression System: "Target compression ratio needed: 12 (achieved ~8 in water tests with <10% perturbation)" — the 33% shortfall between achieved and required compression ratio in the surrogate medium is the most specific quantitative risk indicator in the public record.

[4] general-fusion-iaea-fec-2025-abstract.md, §LM26 Surrogate: "Electromagnetic theta-pinch compresses solid lithium liner" — the demo uses electromagnetic compression of a solid liner, while the commercial plant uses pneumatic compression of a liquid metal vortex. These are different physics and engineering challenges.
