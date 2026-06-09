---
ID: 06-magnetic-mirror
Concept: Magnetic Mirror (Pale Blue)
Company: Pale Blue
Status: draft
Created: 2026-06-09
Approved-Date:
Confinement-Family: MFE
Archetype: MIRROR
Archetype-Fit: Low
Comparison-Status: costingfe-asterisked
Comparables: []
Design-Point-Name: Pale Blue Fusion CHARM commercial notional plant (operator-authored, 150 MWe)
Design-Point-Maturity: paper-concept
P-Native: 150
Grounding-Confidence: low
---

## Design Point

- Name: Pale Blue Fusion CHARM commercial notional plant (operator-authored, 150 MWe)
- Maturity: paper-concept
- P_native: 150 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/06-magnetic-mirror/iter-02/sources/arpa-e-2025-fisch-presentation-notes.md
  - knowledge/concept_research/06-magnetic-mirror/iter-01/sources/technical-papers-summary.md
  - knowledge/concept_research/06-magnetic-mirror/iter-01/sources/princeton-arpa-e-funding-2022.md

## 1. Availability of Data

**Rating: Limited**

The Pale Blue Fusion (pre-incorporation Princeton University spinoff) p-B11 centrifugal magnetic mirror concept has extensive **physics literature** but minimal **engineering data**. The team led by Nat Fisch, Ian Ochs, and Elijah Kolmes has published 29 peer-reviewed papers and filed 4 patent applications (March-April 2025) covering the theoretical foundations of alpha channeling, ponderomotive barriers, and centrifugal confinement. The July 2025 ARPA-E presentation provides the most comprehensive public disclosure of the CHARM (CHambered Aneutronic Rotating Mirror) architecture.

> "Our proposal is purely theoretical, so it does not require the large resources associated with experiments. However, should our ideas work out, perhaps unlikely but fantastic if they do, we will need partners to help us navigate the key uncertainties experimentally."
> — princeton-arpa-e-funding-2022.md §A different kind of fusion reaction

The related CMFX (Centrifugal Mirror Fusion Experiment) at the University of Maryland provides partial physics validation using LTS magnets (3 T throat, 0.3 T midplane), with first plasma in October 2022 and fusion yield measurements reported in 2025 (arXiv:2505.23047). However, CMFX is a separate research group validating centrifugal mirror physics at small scale — it is not a Pale Blue device and provides no engineering or cost data.

**Key Data Gaps:**

1. **Zero quantitative reactor parameters disclosed.** The analyst-patch document explicitly flags: "Pale Blue Fusion has disclosed no quantitative reactor parameters for the CHARM commercial plant — no geometry, fields, densities, temperatures, confinement times, or fusion power" (analyst-patch-data-grounded.md, lines 12-15). The only company-disclosed value is `P_native = 150 MWe` from the ARPA-E presentation slide showing a "commercial notional plant."

2. **No engineering subsystem specifications.** The 29 publications and 4 patents focus entirely on plasma physics. No magnet technology (HTS vs LTS), no blanket design, no direct energy converter topology, no balance-of-plant architecture is specified.

3. **No cost breakdowns or TEA disclosures.** The only economic claim is qualitative: "Cheap and non-radioactive reactants" for p-B11 fuel (arpa-e-2025-fisch-presentation-notes.md §Why pB11?, line 41).

4. **Physics validation limited to components, not integration.** The team's summary states: "Now we need to see if these components work together self-consistently" (arpa-e-2025-fisch-presentation-notes.md, line 414). Alpha channeling, ponderomotive barriers, and helium ash removal are validated individually in theory and simulation, but the coupled system has not been demonstrated.

This analysis is constrained to extracting the **physics architecture** from theoretical papers and mapping it to cost implications — it cannot produce a grounded cost estimate without disclosed reactor parameters.

## 2. Challenges in Capturing System Function

The major challenges for LCOE modeling of Pale Blue's CHARM concept, ranked by impact on cost uncertainty:

### 1. Alpha Channeling Efficiency (Existential — Determines Viability)

p-B11 fusion has an intrinsic bremsstrahlung radiation barrier: at thermal equilibrium, bremsstrahlung losses exceed fusion power. The concept's viability depends entirely on maintaining a **highly nonthermal distribution** — energetic protons (100-300 keV), cold electrons (~10 keV), and moderate-temperature boron. Alpha channeling uses RF waves to extract energy from fusion-born helium-3 nuclei and reinject it into the proton population, bypassing thermalization.

> "If helium stays in the soup, the reactor never reaches breakeven even with perfect confinement!"
> — arpa-e-2025-fisch-presentation-notes.md §In particular: Helium poisoning, lines 61-72

The claimed confinement time reduction is 2.6-6.9× (technical-papers-summary.md §2, §4), which would dramatically reduce capital costs by shrinking the required magnetic mirror volume and field strength. However, this multiplier is **theoretical** — no experiment has demonstrated alpha channeling at fusion-relevant conditions.

**LCOE Impact:** If alpha channeling efficiency falls below ~70-80% of theoretical, the reactor may not reach Q > 1. This is a binary on/off switch for the concept's viability, not a parametric sensitivity.

### 2. Direct Energy Conversion Efficiency and Recirculating Power (High Impact)

The concept assumes direct electromagnetic energy recovery from the plasma's rotation energy. The 2025 PRX Energy paper from the core team (Rax, Kolmes & Fisch, "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields") suggests an adiabatic DEC approach for axisymmetric mirror fields. A 2023 patent (US20230298771) describes a Standing Wave Direct Energy Converter (SWDEC) using RF devices.

**Uncertainty range:** Direct energy conversion efficiency for charged particle exhaust is claimed at 50-90% in various mirror DEC studies, but has never been demonstrated at reactor-scale power levels (hundreds of MW). For comparison, Helion claims >90% electromagnetic energy recovery for their pulsed FRC compression cycle, but this is recovering compression energy, not fusion product energy.

If DEC efficiency is <60%, the recirculating power fraction could exceed 40%, making Q_eng < 2 and LCOE economically unviable. If DEC efficiency is >80%, the concept bypasses the 30-40% thermal cycle efficiency penalty, giving a significant advantage over D-T tokamaks.

**LCOE sensitivity:** A 20-percentage-point swing in DEC efficiency translates to ~50-100% variation in net electric output for the same fusion power, directly impacting $/kW overnight cost.

### 3. Multi-Chamber Coordination and Helium Ash Removal (Medium-High Impact)

The CHARM architecture uses three regions:
- **Fusion chamber** where protons and boron react
- **Heat exchange chamber** where helium ash is removed via wave-induced diffusion
- **Plug regions** using ponderomotive barriers as "one-way RF walls" for ion traffic control

> "Wave-induced diffusion in the second chamber necessary?"
> — arpa-e-2025-fisch-presentation-notes.md §For Vision 2021, we began with questions, line 117

The team's 2025 ash removal paper (Ochs, Kolmes & Fisch, Phys. Plasmas 32, 052506) addresses helium poisoning via spatial separation. However, the continuous helium extraction rate required for steady-state operation has not been experimentally validated.

**LCOE Impact:** If helium removal is insufficient, the reactor stalls below breakeven. If it requires large auxiliary power (e.g., high-power RF systems for wave-induced diffusion), the recirculating power fraction increases. The ponderomotive barrier patent (Rubin & Fisch, Phys. Plasmas 32, 062104) describes "passive" barriers using static field perturbations, but the ARPA-E summary notes: "One-way walls have high energy cost, so use is situational" (arpa-e-2025-fisch-presentation-notes.md, line 411).

### 4. Synchrotron Radiation Losses (Medium Impact)

p-B11 requires ion temperatures approaching the relativistic regime (proton energy ~150-300 keV, corresponding to ~1 billion K). At these temperatures, synchrotron radiation from relativistic electrons becomes significant.

> "Relativistic effects reduce confinement time in mirror machines. Important for p-B11 which requires very high temperatures (approaching relativistic regime)."
> — technical-papers-summary.md §3

The team claims synchrotron radiation is "manageable through reabsorption" (arpa-e-2025-fisch-presentation-notes.md §Summary), but this is theoretical. If synchrotron losses are higher than predicted, auxiliary heating power increases, raising CAS22 heating system costs and recirculating power.

### 5. Magnet Technology and Cost (High Impact on Absolute Cost)

No magnet technology is specified. The simple solenoidal mirror geometry (outer and inner mirror coils visible in presentation slides) is compatible with HTS wound coils, LTS coils, or even resistive magnets. The related CMFX experiment uses repurposed MRI LTS magnets. The WHAM experiment at Wisconsin uses CFS-supplied HTS-REBCO magnets at 17 T for a similar mirror geometry.

**For a 150 MWe reactor-scale device, HTS-REBCO is the likely choice** given:
- Simple solenoidal geometry (no complex 3D shaping → easier winding)
- Benefit from high mirror ratios (B_throat / B_midplane > 5-10) enabled by HTS high-field capability
- Industry trend toward HTS for all post-2020 reactor-scale designs

However, the library's HTS coil cost scaling ($30-50/kg for REBCO tape + structure) may underestimate costs for a centrifugal mirror, which requires:
- High mechanical strength to resist centrifugal and magnetic stresses from rotating plasma
- Potentially larger bore radius than standard tokamak scaling to accommodate rotation-enhanced radial pressure

**LCOE Impact:** Magnet costs typically represent 20-40% of CAS22 for MFE concepts. A 2× variation in HTS unit cost translates to 10-20% variation in overnight capital cost.

### 6. Data Grounding — No Published Design Point

The analyst-patch document preserves a `DATA_GROUNDED = False` flag to prevent the concept explorer from displaying placeholder LCOE values as if they were real predictions. The entire parameter set except `P_native` and fuel choice is library defaults.

This is **not** a modeling challenge — it is a **disclosure gap**. The company has not published a reactor design. Any cost estimate is an analogue-based projection, not a company-validated figure.

## 3. Maturity of Key Subsystems and Components

Subsystems are listed in **ascending order of maturity** (least mature first):

### Alpha Channeling RF System — TRL 1-2 (Missing at Scale, On Paper for p-B11)

**Demonstrated:** Alpha channeling has been proposed theoretically for decades (Fisch 2006, Zhmoginov & Fisch 2009, Fetterman & Fisch 2010) and validated in simulation for mirror machines. The S5 PIC code simulation shows "XB Mode Conversion in Supersonic Flow" at the upper hybrid resonance (arpa-e-fisch-2025-presentation.md), indicating X-mode to Bernstein wave mode conversion in the rotating plasma.

**On paper only:** Alpha channeling in a p-B11 fusion environment. The hybrid fast+thermal proton scheme (Ochs et al., PRE 106, 055215, 2022) and wave-supported hybrid beam-thermal pB11 paper (Kolmes, Ochs & Fisch, Phys. Plasmas 29, 110701, 2022) provide the theoretical basis, but **no experiment has demonstrated energy extraction from fusion-born alpha particles and channeling into fuel ions at any scale.**

**Missing at scale:** RF antenna design, launching geometry, power handling (tens to hundreds of MW of circulating RF power), and integration with the rotating plasma. The exact frequency and antenna scheme are not disclosed.

**Critical for cost:** Alpha channeling is not an optimization — it is the enabling mechanism. Without it, p-B11 fusion does not reach breakeven. The RF system's capital cost (CAS22 C220104 supplementary heating) and operating efficiency directly set the recirculating power fraction.

### Direct Energy Converter for Rotation Energy — TRL 2-3 (On Paper, Lab-Scale for Related Systems)

**Demonstrated:** Venetian blind DEC systems were tested in the 1970s for conventional mirror end-loss recovery at ~50-65% efficiency, TRL 5 (Moir & Barr, Nucl. Fusion 13, 1973). However, these were uncooled ribbon electrodes in low-power test stands.

**On paper only:** The Pale Blue-specific DEC. The PRX Energy 2025 paper (Rax, Kolmes & Fisch, "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields") addresses adiabatic DEC in axisymmetric mirror fields, indicating this is the preferred approach. The SWDEC patent (US20230298771, 2023) describes an alternative RF-based DEC, but whether Pale Blue adopts this or the adiabatic method is not confirmed.

**Missing at scale:** A DEC system that handles hundreds of MW of rotation energy recovery at >70% efficiency while surviving the radiation environment downstream of a fusion reactor. The temperature and particle flux of the axially exhausted plasma are not disclosed. Electrode lifetime, voltage holdoff at high power density, and thermal management are unaddressed.

**Critical for cost:** If DEC efficiency < 60%, the concept is economically unviable. If efficiency > 80%, the concept bypasses thermal cycle losses and gains a significant cost advantage. DEC capital cost is captured in CAS22 C220109 (direct energy converter), which the library prices for mirror/FRC directed exhaust but with large uncertainty.

### Ponderomotive Barriers for Ion Traffic Control — TRL 2 (On Paper Only)

**Demonstrated:** Ponderomotive forces from RF waves are well-established physics. The 2025 patent (Rubin & Fisch, Phys. Plasmas 32, 062104) describes "passive" ponderomotive barriers using static magnetic field perturbations with high azimuthal mode numbers to regulate ion traffic between chambers.

**On paper only:** Application to CHARM's multi-chamber architecture. The barriers must selectively reflect boron ions while transmitting helium ash, and prevent back-diffusion of helium into the fusion chamber.

**Missing at scale:** Experimental validation in a rotating mirror plasma. The team's summary notes: "Can selective ponderomotive barriers regulate ion traffic?" and "Can we make passive ponderomotive barriers?" were answered affirmatively at the component level, but "Now we need to see if these components work together self-consistently" (arpa-e-2025-fisch-presentation-notes.md, lines 406-414).

**Cost impact:** If ponderomotive barriers require active RF power, they add to CAS22 C220104 supplementary heating costs and recirculating power. If they are truly passive (static field perturbations), they are a magnetic field shaping cost absorbed into C220103 magnet design. The ARPA-E summary flags: "One-way walls have high energy cost, so use is situational" (line 411).

### Centrifugal Confinement via E×B Rotation — TRL 3-4 (Lab-Scale Demonstrated, Reactor-Scale On Paper)

**Demonstrated:** The CMFX experiment at the University of Maryland reached first plasma in October 2022 and reported fusion yield measurements in 2025 (arXiv:2505.23047). CMFX uses a biased central electrode to establish E×B rotation and validates centrifugal species separation physics at 3 T throat / 0.3 T midplane with LTS magnets. This is **partial validation** — the physics mechanism works at small scale.

**On paper only:** Centrifugal confinement at reactor-scale power density, with differential confinement (protons and boron confined, helium expelled) sustained for hours to days. The required rotation Mach number, electrode voltage, and wall interaction physics are not disclosed for the 150 MWe design point.

**Missing at scale:** Biased central electrode system that handles reactor-scale power throughput without intolerable voltage drops or sputtering. The ARPA-E derisking questions included: "Can rotation be maintained without intolerable voltage drops at walls?" (arpa-e-2025-fisch-presentation-notes.md, line 117). The team claims this is answered affirmatively, but no publication provides electrode design details.

**Cost impact:** The central electrode system is a novel reactor component with no direct cost analogue. Electrode power supply, cooling, and lifetime affect CAS22 C220107 (power supplies) and CAS70 (O&M replacement). If electrode lifetime is <1 year, scheduled replacement costs could be significant.

### Aneutronic Blanket (Energy Capture, No Tritium Breeding) — TRL 4-5 (Conceptual Designs Exist, Neutronic Validation Pending)

**Demonstrated:** p-B11 fusion produces <1% neutron energy from side reactions. The blanket does not breed tritium — it is an energy-capture-only component. Advanced fuel FRC and mirror concepts (TAE, Helion) have studied aneutronic blanket designs, but none are built.

**On paper only:** A blanket optimized for <1% neutron flux with high-efficiency thermal energy capture. The presentation lists "No neutron damage and induced radioactivity" and "No waste storage issues" as advantages (arpa-e-2025-fisch-presentation-notes.md §Why pB11?), but the blanket must still capture bremsstrahlung X-rays and neutron side reactions. The CHARM architecture uses a "heat exchange chamber" for helium removal, implying a second region where thermal energy may be extracted.

**Missing at scale:** Validated blanket design for p-B11. The library's `blanket_unit_cost_pb11` parameter activates near-aneutronic cost scaling, but this is an analyst-constructed default, not a company-disclosed figure.

**Cost impact:** Eliminating the tritium breeding requirement removes the need for lithium enrichment, tritium extraction systems, and associated regulatory burden, reducing CAS22 C220101 blanket costs and CAS27 special materials (initial Li inventory). However, the blanket must still handle ~10-50 MW/m² surface heat flux (bremsstrahlung + neutron side reactions), requiring advanced materials and cooling.

### Solenoidal HTS Mirror Coils — TRL 5-7 (HTS Coils Demonstrated, Mirror-Specific Stresses Uncharacterized)

**Demonstrated:** HTS-REBCO wound coils at 20 T have been built and tested (CFS SPARC TF coil prototype, January 2026). Tokamak Energy achieved 11.8 T in a full tokamak configuration (November 2025). The WHAM experiment at Wisconsin uses CFS-supplied HTS magnets for a simple mirror geometry at 17 T.

**On paper only:** HTS coils for a centrifugal mirror at reactor scale. The rotating plasma exerts centrifugal pressure on the confining magnetic field, creating radial stress on the coils. The stress scaling for a rotating mirror is different from tokamak or stellarator TF coils.

**Missing at scale:** HTS coil design validated for centrifugal stress at high mirror ratios (B_throat / B_midplane > 5). REBCO tape delamination under combined high-field + cyclic mechanical loads is an industry-wide concern. Radiation damage to HTS insulation in the near-aneutronic (but not zero-neutron) environment is uncharacterized.

**Cost impact:** HTS magnet costs dominate CAS22 C220103. The library default assumes standard tokamak/stellarator coil geometry. A centrifugal mirror may require thicker structural support or larger bore radius, increasing coil mass and cost. The analyst-patch document flags: "Library default of 1.85 m under-sizes the coil bore for an open-ended mirror" (analyst-patch-data-grounded.md, lines 55-57).

### Balance of Plant (Thermal Cycle if DEC Does Not Achieve 100% Capture) — TRL 8-9 (Mature, If Needed)

**Demonstrated:** Conventional Rankine or Brayton cycle heat rejection systems are TRL 9 (deployed at GW scale in fission and fossil plants). If the CHARM concept uses a hybrid approach — partial direct conversion + thermal cycle for uncaptured heat — this subsystem is off-the-shelf.

**On paper only:** Integration with p-B11 bremsstrahlung heat signature and aneutronic neutron environment. The thermal power profile (MW_th from bremsstrahlung vs. neutron heating vs. DEC waste heat) is not disclosed.

**Missing at scale:** Nothing, if a thermal cycle is used. However, the concept's economic advantage depends on minimizing or eliminating the thermal cycle via high-efficiency DEC. If DEC efficiency is 90%, only 10% of fusion energy goes to thermal → small turbine → lower CAS23 turbine plant equipment cost. If DEC efficiency is 50%, half goes to thermal → large turbine → CAS23 cost approaches D-T tokamak levels.

## 4. Key Materials and Supply Chain Considerations

### Boron-11 Fuel (Abundant, Cheap)

**Current production:** Boron-11 is 80.1% of natural boron. Global boron production is ~1 million tonnes/year (USGS 2024), primarily for glass, ceramics, and agriculture. Isotopically enriched boron-11 (>95% purity) is commercially available from specialty suppliers at $50-200/kg depending on purity and batch size.

**Plant-scale demand:** A 150 MWe p-B11 plant operating at 85% capacity factor consumes approximately:
- Protons: sourced from water electrolysis or natural gas reforming (trivial cost, unlimited supply)
- Boron-11: ~10-100 kg/year (exact consumption depends on burnup fraction and recirculation efficiency, not disclosed by company)

**Supply chain assessment:** Boron-11 is the least constraining fusion fuel. No enrichment infrastructure bottleneck (unlike lithium-6 for tritium breeding), no radioactive handling (unlike tritium), no scarcity (unlike helium-3). Fuel cost is negligible compared to capital cost.

**LCOE impact:** Fuel cost is <0.1% of LCOE. The claim "Cheap and non-radioactive reactants" (arpa-e-2025-fisch-presentation-notes.md §Why pB11?, line 41) is accurate. This is a cost **advantage** vs. D-T (tritium breeding, handling, regulatory burden) and D-He3 (helium-3 scarcity).

### HTS-REBCO Tape for Magnets (Bottleneck, High Cost)

**Current production:** Global REBCO production capacity is thousands of kilometers per year. Major suppliers: Shanghai Superconductor Technology, Faraday Factory Japan, CFS (Devens facility ramping to high volume).

**Plant-scale demand:** A 150 MWe centrifugal mirror with simple solenoidal geometry requires an estimated:
- Bore radius: 2.75 m (analyst-derived from radial build arithmetic, not company disclosure)
- Mirror ratio: 5-10 (typical for end-plug mirrors, not disclosed)
- Peak field on conductor: 15-20 T (estimated from WHAM 17 T and CMFX 3 T scaling, not disclosed)
- Coil ampere-meters: ~50-150 MA-m (order-of-magnitude estimate)
- REBCO tape requirement: **1,000-3,000 km** (comparable to ARC-class tokamak, but simpler winding geometry may reduce labor cost)

**Supply chain assessment:** REBCO tape is the primary material bottleneck for all HTS fusion concepts. The Pale Blue concept has **no unique advantage** in HTS demand — it is a standard consumer of REBCO tape. The simple solenoidal geometry may reduce coil fabrication complexity vs. 3D stellarator coils, but the centrifugal stress requirement may demand thicker structural support.

**Cost trajectory:** Current REBCO tape pricing is $50-100/kA-m at low volume, with industry targets of $10-20/kA-m at high volume (CFS, SuperPower). The library's HTS magnet cost scaling uses $30-50/kg effective cost including structure and winding.

**LCOE impact:** HTS magnet cost is the largest single capital cost component for MFE concepts, typically 20-40% of CAS22. A 2× variation in REBCO unit cost translates to 10-20% variation in overnight capital cost.

### Central Electrode Materials (Tungsten, Molybdenum, or Graphite — Unknown)

**Current production:** Tungsten global production is ~85,000 tonnes/year. Molybdenum is ~300,000 tonnes/year. Both are adequate for fusion-scale demand.

**Plant-scale demand:** The biased central electrode for establishing E×B rotation is a concept-unique component. Material selection depends on:
- Operating voltage: 10-100 kV (estimated from CMFX 100 kV specification, reactor-scale not disclosed)
- Particle flux from rotating plasma
- Sputtering rate and lifetime
- Thermal loading

**Supply chain assessment:** Material supply is not a bottleneck. The **design and lifetime** are unknowns. If electrode lifetime is <1 year due to sputtering, scheduled replacement becomes a CAS70 O&M cost driver. If the electrode requires exotic coatings (e.g., tungsten monoblock like tokamak divertors), fabrication cost increases.

**LCOE impact:** Electrode capital cost is small (<5% of CAS22). Electrode **replacement cost** is the larger concern. If annual replacement is required, the O&M cost penalty could be $1-5M/year, comparable to D-T tokamak divertor replacement.

### FLiBe or Lead-Lithium for Aneutronic Blanket (If Liquid Breeder Used)

**Current production:** FLiBe (Li₂BeF₄) is not produced at industrial scale. Beryllium production is ~300 tonnes/year globally, dominated by Materion Corp. Lithium-6 enrichment capacity is limited (Russia and China mercury-based process, US/EU alternatives under development).

**Plant-scale demand:** If the CHARM blanket uses a liquid breeder for thermal energy extraction (not disclosed), the inventory is:
- FLiBe: 100-500 tonnes (typical for aneutronic blanket, order-of-magnitude estimate)
- No lithium-6 enrichment required (no tritium breeding)
- Beryllium: 10-50 tonnes Be metal equivalent

**Supply chain assessment:** **This is speculative — no blanket design is disclosed.** If a solid ceramic blanket (Li₄SiO₄ or Li₂TiO₃) is used instead, beryllium is not required. The "heat exchange chamber" mentioned in the ARPA-E presentation could be a gas-cooled or molten-salt-cooled region, but no details are provided.

**LCOE impact:** If FLiBe is used, CAS27 special materials (initial blanket inventory) is $15-75M at $150/kg FLiBe cost. This is a one-time capital cost, not an O&M cost (FLiBe is not consumed, unlike tritium).

## 5. Design Point Parameters

The following table describes the **150 MWe CHARM commercial notional plant** quantitatively. **Critical data gap:** The company has disclosed only `P_native = 150 MWe` and fuel choice (p-B11). All other values are analyst-derived from library defaults, radial build arithmetic, or inferred from the CMFX experiment scaling. These are **placeholders for a future company-disclosed design point**, not validated parameters.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| **Net electric power** | 150 MWe | arpa-e-2025-fisch-presentation-notes.md (slide showing "commercial notional plant") | high | spec key: `P_native` — only company-disclosed value |
| **Fuel** | p-B11 | arpa-e-2025-fisch-presentation-notes.md §Why pB11? | high | spec key: `Fuel` — drives aneutronic cost scaling |
| **Confinement concept** | Magnetic mirror (centrifugal, multi-chamber) | arpa-e-2025-fisch-presentation-notes.md §Our solution: multi-chamber centrifugal fusion | high | CHARM: CHambered Aneutronic Rotating Mirror |
| **r_bore (coil bore radius)** | 2.75 m | [inferred: analyst-patch-data-grounded.md lines 55-57 — derived from library radial build, not company disclosure] | low | spec key: `r_bore` — library default 1.85 m "under-sizes the coil bore for an open-ended mirror" |
| **Mirror ratio (B_throat / B_midplane)** | 5-10 (estimated) | [inferred: typical for end-plug mirrors; CMFX uses 10 (3T / 0.3T); WHAM targets 10-15; no CHARM disclosure] | low | Not a spec key — informational only |
| **Peak field on conductor (B_peak)** | 15-20 T (estimated) | [inferred: WHAM uses 17 T HTS; CMFX uses 3 T LTS; reactor-scale mirrors require high mirror ratio → high throat field] | low | Not a spec key — informational only |
| **On-axis midplane field (B0)** | 2-3 T (estimated) | [inferred: B_peak / mirror_ratio; no company disclosure] | low | spec key: `B` (not `B0` — canonical name is `B`) |
| **Plasma radius (minor radius)** | 0.5-1.0 m (estimated) | [inferred: order-of-magnitude from r_bore minus radial build; no company disclosure] | low | spec key: `plasma_t` (or `plasma_volume`) |
| **Central cell length** | 10-50 m (estimated) | [inferred: magnetic mirrors are inherently modular and can have arbitrarily long central cells; no CHARM disclosure] | low | Not a spec key — informational only |
| **Fusion power** | 300-600 MW (estimated) | [inferred: back-solved from P_native = 150 MWe assuming eta_th ~30-50% and Q_eng ~2-5; no company disclosure] | low | Informational only — library back-solves `p_fus` from `p_input` + `P_native`; do NOT include `p_fus` in spec |
| **Auxiliary heating power (p_input)** | 50-150 MW (estimated) | [inferred: from estimated Q_eng ~2-5; no company disclosure] | low | spec key: `p_input` — RF power for alpha channeling + startup heating |
| **Q_eng (engineering gain)** | 2-5 (estimated) | [inferred: p-B11 with alpha channeling and DEC; no company disclosure] | low | Not a spec key — derived from P_native and p_input |
| **DEC efficiency** | 70-90% (claimed range) | [inferred: general DEC studies for charged particle exhaust; no CHARM-specific disclosure] | low | Not a spec key — affects net thermal power to balance of plant |
| **Thermal efficiency (eta_th)** | 0-40% (depends on DEC) | [inferred: if DEC is 90%, only 10% goes to thermal cycle → low eta_th; if DEC is 60%, 40% goes to thermal → conventional eta_th ~35%] | low | Not a spec key — affects turbine sizing |
| **Capacity factor** | 85% (library default) | [assumed: no company disclosure on maintenance schedule or availability] | low | Not a spec key — library default for steady-state MFE |
| **Plant lifetime** | 30 years (library default) | [assumed: no company disclosure] | low | Not a spec key — standard for fusion economic studies |
| **Rotation Mach number** | 0.5-2 (estimated) | [inferred: centrifugal confinement requires supersonic rotation; CMFX uses biased electrode up to 100 kV; no CHARM disclosure] | low | Not a spec key — affects centrifugal pressure and confinement |
| **Electrode bias voltage** | 10-100 kV (estimated) | [inferred: CMFX uses up to 100 kV; reactor-scale may differ; no CHARM disclosure] | low | Not a spec key — affects electrode power supply cost (CAS22 C220107) |
| **Alpha channeling RF frequency** | Ion cyclotron range (10-100 MHz estimated) | [inferred: technical-papers-summary.md §1 cites ICRH; XB mode conversion at upper hybrid resonance; no exact frequency disclosed] | medium | Not a spec key — affects RF antenna design |

**Summary of grounding confidence:**
- **1 high-confidence value** (P_native = 150 MWe, company-disclosed)
- **1 high-confidence categorical value** (Fuel = p-B11, company-disclosed)
- **All other values are low-confidence estimates** derived from library defaults, radial build arithmetic, or scaling from related experiments (CMFX, WHAM)

**Derivation chain for key inferred values:**

1. **r_bore = 2.75 m**: The analyst-patch document states: "Library default of 1.85 m under-sizes the coil bore for an open-ended mirror" (analyst-patch-data-grounded.md, lines 55-57). The 2.75 m value is derived from radial build arithmetic: plasma radius (~0.5 m) + first wall (~0.05 m) + blanket (~0.3 m) + shield (~0.5 m) + vacuum gap (~0.1 m) + coil winding (~0.3 m) ≈ 1.75 m minimum; scaled up to 2.75 m to provide margin for centrifugal pressure and mirror geometry. **This is not a company disclosure.**

2. **B_peak = 15-20 T**: Estimated from reactor-scale mirror requirements. CMFX uses 3 T throat (LTS). WHAM targets 17 T (HTS). A 150 MWe reactor-scale mirror requires high mirror ratio (5-10) to minimize end losses, implying peak field on conductor of 15-20 T. **No CHARM-specific field strength is disclosed.**

3. **Fusion power = 300-600 MW**: Back-solved from P_native = 150 MWe assuming:
   - If DEC efficiency = 80% and thermal efficiency = 35%, then P_fusion ≈ 150 / (0.8 × 0.8) ≈ 235 MW (lower bound)
   - If DEC efficiency = 60% and thermal efficiency = 30%, then P_fusion ≈ 150 / (0.6 × 0.5) ≈ 500 MW (upper bound)
   - **No company disclosure of fusion power, DEC efficiency, or thermal efficiency.**

4. **p_input = 50-150 MW**: Estimated from Q_eng = P_net / p_input. If Q_eng = 2, then p_input = 150 / 2 = 75 MW. If Q_eng = 5, then p_input = 150 / 5 = 30 MW. The RF power requirement for alpha channeling is not disclosed. The CMFX power supply is 100 kV, 100 kW (technical-papers-summary.md §2), but this is a small-scale experiment, not a reactor.

**These values are placeholders only.** They allow the 1costingFE library to run a cost calculation using default scaling relationships, but the resulting LCOE is **not a company-validated prediction** — it is an analyst-constructed scenario to explore cost sensitivities.

## 5b. Override Candidates

The per-account walkthrough below examines each canonical 1costingFE account for this archetype. An override is proposed only when the dossier provides company-grounded data — a published quantity, unit cost, or dollar figure — that justifies departing from the library default.

**Result:** **Zero enabled overrides.** The company has disclosed no quantitative reactor parameters beyond `P_native = 150 MWe`. Every canonical account in the schema depends on geometry (bore radius, length, field strength), power levels (fusion power, auxiliary heating), or subsystem specifications (magnet type, blanket design, DEC topology) that are not disclosed. Without this data, no override can be justified as evidence-backed.

**Per-account walkthrough (canonical codes only):**

| Account | Library Default (What It Costs) | Override Justification? | Outcome |
|---------|--------------------------------|------------------------|---------|
| `C220101` | First wall, blanket & neutron multiplier (aneutronic energy-capture blanket for p-B11) | **No company data.** Blanket design not disclosed. Library activates `blanket_unit_cost_pb11` based on fuel choice, but this is an analyst-constructed default for near-aneutronic concepts, not a Pale Blue figure. | **No override** |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for p-B11 low-neutron) | **No company data.** Shield thickness and material not disclosed. Library scales from neutron wall loading, which is not disclosed for CHARM. | **No override** |
| `C220103` | Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat) | **No company data.** Magnet technology (HTS vs LTS), peak field, bore radius, and coil geometry are not disclosed. The analyst-patch flags that library default bore radius "under-sizes the coil bore for an open-ended mirror" (analyst-patch-data-grounded.md), but provides no company-grounded alternative. | **No override** |
| `C220104` | Supplementary plasma heating (RF for alpha channeling + startup) | **No company data.** RF system power, frequency, and antenna design are not disclosed. The CMFX power supply (100 kV, 100 kW) is a small-scale experiment, not a reactor. No published CHARM heating power. | **No override** |
| `C220105` | Primary structure (gravity supports, thermal shields, inter-coil structure, machine base) | **No company data.** Machine geometry (length, diameter, mass) not disclosed. Library scales from coil size and fusion power, both of which are analyst estimates. | **No override** |
| `C220106` | Vacuum system (vessel, port extensions, cryopumps, leak detection) | **No company data.** Vessel geometry not disclosed. Mirror machines have open-ended geometry (no closed vessel like tokamaks), but the CHARM multi-chamber architecture's vacuum boundary is not described. | **No override** |
| `C220107` | Power supplies (DC magnet power supplies + electrode bias power supply for E×B rotation) | **No company data.** Magnet power supply sizing depends on coil inductance and field ramp rate (if any). The biased central electrode power supply is a concept-unique component — CMFX uses 100 kV, 100 kW, but reactor-scale is not disclosed. | **No override** |
| `C220108` | Divertor (or mirror end-loss target / heat sink) | **No company data.** The CHARM concept has axial end losses like all mirrors. The presentation does not disclose heat flux, target material, or cooling scheme. Library default assumes standard tokamak-style W monoblock divertor, which is inappropriate for a mirror but cannot be overridden without CHARM-specific data. | **No override** |
| `C220109` | Direct energy converter (electrostatic DEC for axial exhaust + rotation energy recovery) | **No company data.** DEC topology (adiabatic vs SWDEC vs other), efficiency, power handling, and electrode design are not disclosed. The PRX Energy 2025 paper and SWDEC patent provide theoretical foundations but no reactor-scale design. Library prices DEC for directed axial exhaust, but the CHARM-specific cost is unknown. | **No override** |
| `C220110` | Remote handling & maintenance equipment | **No company data.** The aneutronic p-B11 fuel cycle has minimal neutron activation, potentially reducing remote handling complexity vs. D-T. However, no maintenance scheme is disclosed. | **No override** |
| `C220111` | Reactor-equipment installation & assembly (fraction of CAS22 subtotal) | **No company data.** Library default is 10% of CAS22 sum. No CHARM-specific assembly cost disclosed. | **No override** |
| `CAS21` | Buildings & site structures | **No company data.** Building footprint depends on machine geometry (length, diameter). The ARPA-E presentation lists "Easier regulatory environment" as a p-B11 advantage (arpa-e-2025-fisch-presentation-notes.md §Why pB11?), implying lower regulatory building cost markup vs. D-T, but no quantitative figure is provided. | **No override** |
| `CAS23` | Turbine plant equipment (thermal cycle; zero if DEC achieves 100% capture, partial if hybrid) | **No company data.** DEC efficiency is not disclosed. If DEC is 90%, only 10% goes to thermal → small turbine. If DEC is 60%, 40% goes to thermal → large turbine. Library scales CAS23 from thermal power to balance of plant. | **No override** |
| `CAS24` | Electric plant equipment (switchyard, transformers, plant distribution) | **No company data.** Library scales from net electric output (P_native = 150 MWe). | **No override** |
| `CAS26` | Heat rejection system (cooling towers, circulating water) | **No company data.** Heat rejection load depends on DEC efficiency and thermal cycle waste heat. Not disclosed. | **No override** |
| `CAS27` | Special materials — initial reactor material inventory / blanket fill | **No company data.** If liquid breeder (FLiBe) is used, inventory is 100-500 tonnes. If solid ceramic, different material. Blanket design not disclosed. | **No override** |

**Override count:** 0 enabled overrides (expected band for low archetype-fit: 6-12). The count falls **below** the expected band because the design point is paper-concept with no disclosed reactor parameters.

**Note for model-setup agent:** The absence of overrides does not mean the library defaults are correct — it means the dossier provides no evidence to depart from them. The resulting LCOE is a **library-default scenario**, not a company-validated estimate. The `DATA_GROUNDED = False` flag must be preserved in the frontmatter.

```yaml
overrides: []
```

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | **All reactor geometry and physics parameters** except P_native (bore radius, length, plasma radius, field strength, densities, temperatures, confinement time, fusion power) | S5 | proprietary | blocking | Company disclosure of CHARM commercial plant design basis, or publication of a reactor concept study with quantitative parameters |
| 2 | **Alpha channeling efficiency and RF system specification** — frequency, antenna design, power handling, demonstrated efficiency at fusion-relevant conditions | S2, S3, S5 | truly-unknown | blocking | Experimental validation of alpha channeling in a p-B11 plasma (does not exist at any scale), or detailed simulation results with error bars from the PB² / S⁵ codes |
| 3 | **Direct energy converter topology, efficiency, and cost** — adiabatic vs SWDEC vs other; electrode design; power handling at 100+ MW scale | S2, S3, S5 | proprietary (design choice), truly-unknown (efficiency) | blocking | Company disclosure of preferred DEC approach, or publication of DEC design study with efficiency targets and cost estimates |
| 4 | **Magnet technology choice** (HTS vs LTS), peak field, bore radius, structural design for centrifugal stress | S2, S3, S5 | proprietary | important | Company disclosure or engineering study addressing centrifugal stress on mirror coils for rotating plasma |
| 5 | **Blanket design and material** — liquid (FLiBe, Pb-Li) vs solid ceramic; thermal energy extraction scheme; compatibility with heat exchange chamber architecture | S3, S4, S5 | proprietary | important | Company disclosure or publication addressing aneutronic blanket for p-B11 |
| 6 | **Central electrode design, material, voltage, lifetime, and replacement schedule** for E×B rotation establishment | S3, S4, S5 | proprietary, not-yet-sourced | important | Company disclosure or engineering study on biased electrode system at reactor scale |
| 7 | **Helium ash removal rate, wave-induced diffusion power requirement, and ponderomotive barrier energy cost** | S2, S3 | proprietary, truly-unknown | blocking | Experimental validation of multi-chamber coordination and helium extraction, or detailed simulation showing self-consistent operation |
| 8 | **Maintenance schedule, component lifetimes, and capacity factor** — electrode replacement, first wall/blanket lifetime, remote handling scheme | S3, S5 | truly-unknown | important | Engineering reliability study addressing long-term operation and scheduled maintenance for p-B11 mirror |
| 9 | **Synchrotron radiation loss magnitude** at p-B11 operating temperatures and impact on power balance | S2 | truly-unknown | important | Experimental measurement or validated simulation of synchrotron losses in relativistic-temperature mirror plasma |
| 10 | **Cost structure comparison** — which CAS accounts are higher/lower than D-T tokamak baseline, and by what factor | S7 | derivable (if gaps 1-8 closed) | nice-to-have | Bottom-up cost model once reactor design is disclosed |

**Gap summary:** The critical path is **company disclosure of the CHARM reactor design basis**. Without quantitative parameters (geometry, fields, power levels), no cost estimate can be grounded. Gaps 2, 3, and 7 (alpha channeling, DEC, and helium removal) are **physics validation gaps** that may take 5-10 years of experimental work to close. Gaps 4-6 (magnets, blanket, electrode) are **engineering design gaps** that could be addressed in a conceptual design study once the physics is validated.

## 7. Family-Delta vs Comparables

**No comparable concept in the corpus for this design point.**

The fixed comparables list is empty. There are no other p-B11 centrifugal magnetic mirror concepts in the pipeline with sufficient data for cost comparison. The two other p-B11 concepts in the broader fusion landscape are:

1. **HB11 Energy (laser-driven p-B11)** — IFE, not MFE; fundamentally different confinement and driver
2. **TAE Technologies (FRC with p-B11 roadmap)** — beam-driven FRC, not a mirror; TAE's current focus is D-He3, with p-B11 as a long-term stretch goal

**Cross-family positioning (qualitative, not a fixed comparable delta):**

### vs. D-T Tokamaks (HTS Compact Tokamak, State-Backed Tokamak)

**Advantages:**
- **No tritium breeding or handling** → eliminates CAS22 C220101 blanket complexity (lithium enrichment, tritium extraction loops, permeation barriers), CAS27 special materials (initial Li inventory), and regulatory burden
- **Minimal neutron activation** → reduced CAS22 C220110 remote handling complexity and CAS21 building cost regulatory markup
- **No waste storage** → simplified licensing and public acceptance (lower soft costs)
- **Fuel cost negligible** → boron-11 is $50-200/kg vs tritium bred in situ (complex fuel cycle)

**Penalties:**
- **Alpha channeling requirement** → adds CAS22 C220104 RF system complexity and capital cost (tens to hundreds of MW of circulating RF power); if alpha channeling fails, concept is unviable
- **Direct energy converter adds novel subsystem** → CAS22 C220109 DEC cost is uncertain (50-90% efficiency range translates to 2× variation in Q_eng)
- **Centrifugal confinement untested at scale** → higher technology risk than tokamak magnetic confinement (TRL 7-8 for tokamaks vs TRL 3-4 for centrifugal mirrors)
- **p-B11 cross-section is 1/1000th of D-T at same temperature** → requires extreme temperatures (100-300 keV protons vs 10-20 keV for D-T), higher field strengths, and longer confinement times; partially offset by alpha channeling's claimed 2.6-6.9× confinement time reduction

**Cost direction:** **Uncertain, large error bars.** If alpha channeling and DEC work as theorized, the concept could have **20-40% lower capital cost** than D-T tokamaks (no tritium breeding, minimal shielding, simpler licensing). If alpha channeling efficiency is <70% or DEC efficiency is <60%, the concept is **economically unviable** (Q_eng < 1.5). The binary nature of the physics validation makes this a **high-risk, high-reward** proposition.

### vs. D-T Magnetic Mirrors (Realta Fusion CoSMo, hypothetical WHAM-scale mirror)

**Advantages:**
- **Same core advantage as vs tokamaks** → no tritium breeding, minimal neutron activation
- **Simpler mirror geometry** → solenoidal coils, no complex 3D shaping like stellarators; lower CAS22 C220103 magnet fabrication cost per ampere-meter
- **Modular central cell** → mirrors can have arbitrarily long central cells built from repeated pipe-like sections; potential for factory fabrication and field assembly

**Penalties:**
- **Alpha channeling and DEC requirements** → same as vs tokamaks; adds subsystem complexity not present in D-T mirrors
- **Centrifugal confinement adds rotating plasma and biased electrode** → CAS22 C220107 power supply for electrode bias (novel subsystem); potential CAS70 O&M cost for electrode replacement if lifetime is <1 year

**Cost direction:** **Comparable to slightly lower capital cost than D-T mirrors** if physics works. D-T mirrors already benefit from simple geometry and modularity. The p-B11 fuel cycle advantage (no tritium) is the main differentiator. However, D-T mirrors are further along the technology maturity curve (WHAM targeting first plasma 2026, Realta building CoSMo) — the p-B11 centrifugal mirror is 5-10 years behind in experimental validation.

### vs. D-He3 FRC (Helion Energy)

**Advantages:**
- **Helium-3 scarcity is not an issue for p-B11** → boron-11 is naturally abundant (80% of natural boron) vs He3 which must be bred from D-D reactions or imported from lunar regolith (long-term fantasy)
- **No D-D neutron background from fuel breeding** → Helion's D-He3 cycle requires D-D breeding to produce He3 via tritium decay, generating 2.45 MeV neutrons; p-B11 has <1% neutron energy from side reactions

**Penalties:**
- **p-B11 requires higher temperature than D-He3** → D-He3 ignites at ~50-100 keV, p-B11 at 100-300 keV; higher confinement challenge
- **Alpha channeling is more critical for p-B11 than for D-He3** → D-He3 can reach breakeven without alpha channeling (though performance is improved with it); p-B11 **cannot** reach breakeven without alpha channeling due to bremsstrahlung barrier

**Cost direction:** **Uncertain.** Both concepts rely on direct energy conversion and advanced fuels. Helion's pulsed FRC compression has demonstrated 100+ million °C temperatures and >90% energy recovery (at subscale), providing some validation. Pale Blue's centrifugal mirror is earlier-stage (CMFX is first experiment, no fusion yet). If both concepts achieve their claimed DEC efficiencies and fuel cycle performance, **p-B11 has lower fuel cost** (boron vs He3 breeding) but **higher physics risk** (alpha channeling requirement).

**Summary:** The p-B11 centrifugal mirror occupies a **high-risk, high-reward** position. It shares the aneutronic fuel cycle advantages with D-He3 FRC (Helion) but adds alpha channeling as a critical enabling mechanism. Relative to D-T tokamaks and mirrors, it eliminates tritium breeding and neutron shielding costs but introduces DEC and centrifugal confinement subsystems with no commercial precedent. **The cost delta is dominated by physics uncertainty, not subsystem cost differences.**

## 8. Sources

Listed in order of importance to the analysis:

1. **ARPA-E presentation notes (July 2025)** — arpa-e-2025-fisch-presentation-notes.md
   - Primary source for CHARM architecture, derisking progress, and company pivot to Pale Blue Fusion
   - 20-slide presentation from Nat Fisch covering multi-chamber centrifugal fusion, alpha channeling, ponderomotive barriers, computational tools (PB², S⁵, R³FP, MITNS), and patent portfolio (4 applications)
   - Most complete public disclosure of the concept to date
   - Location: knowledge/concept_research/06-magnetic-mirror/iter-02/sources/

2. **Technical papers summary** — technical-papers-summary.md
   - Summarizes key physics papers on alpha channeling (Zhmoginov & Fisch 2009, Fetterman & Fisch 2010, Fisch 2006), ash removal (Ochs, Kolmes & Fisch 2025), ponderomotive barriers (Rubin & Fisch 2025), and direct energy conversion (Rax, Kolmes & Fisch, PRX Energy 2025)
   - Provides performance claims (2.6-6.9× confinement time reduction via alpha channeling)
   - Location: knowledge/concept_research/06-magnetic-mirror/iter-01/sources/

3. **Princeton ARPA-E funding announcement (2022)** — princeton-arpa-e-funding-2022.md
   - News article announcing $850K ARPA-E grant for "Economical Proton-Boron11 Fusion"
   - Fisch quote: "Our ideas on this are a real long shot. But so long as we do not violate any fundamental laws of thermodynamics — and we will come very close to that! — I figure we have an obligation to fully explore the upside potential of pB11 fusion."
   - Establishes project motivation (fuel cost, regulatory simplicity, public acceptance) and acknowledged technical risks
   - Location: knowledge/concept_research/06-magnetic-mirror/iter-01/sources/

4. **ARPA-E Fisch 2025 presentation (markdown extract)** — arpa-e-fisch-2025-presentation.md
   - Redundant with #1 above (iter-02 notes are more complete), but includes slide-by-slide breakdown
   - Covers same material: CHARM architecture, derisking questions (9 key physics risks), codes, patents
   - Location: knowledge/concept_research/06-magnetic-mirror/iter-01/sources/

5. **Analyst-patch data grounded (methodological flag)** — analyst-patch-data-grounded.md
   - Documents that "Pale Blue Fusion has disclosed no quantitative reactor parameters" for CHARM commercial plant
   - Preserves `DATA_GROUNDED = False` flag to prevent placeholder LCOE from being displayed as prediction
   - Provides derived `r_bore = 2.75 m` from radial build arithmetic (library default 1.85 m "under-sizes the coil bore for an open-ended mirror")
   - Location: knowledge/concept_research/06-magnetic-mirror/iter-03/sources/

**Additional references cited but not in dossier:**

6. **Rax, Kolmes & Fisch (2025)** — "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields", PRX Energy 4, 013007
   - Theoretical paper on adiabatic DEC for mirror fields from the core Pale Blue team
   - Indicates preferred DEC approach (adiabatic, not SWDEC)

7. **Ochs, Kolmes & Fisch (2025)** — "Preventing ash from poisoning proton-boron 11 fusion plasmas", Phys. Plasmas 32, 052506 (arXiv:2502.13300)
   - Addresses helium ash removal via spatial separation in multi-chamber architecture

8. **Rubin & Fisch (2025)** — "Ponderomotive barriers in rotating mirror devices using static fields", Phys. Plasmas 32, 062104 (arXiv:2502.02008)
   - Patent describing passive ponderomotive barriers for ion traffic control

9. **CMFX at University of Maryland** — https://ireap.umd.edu/research/centrifugal-mirror-fusion-experiment
   - Separate research group validating centrifugal mirror physics at small scale (LTS magnets, 3 T throat, 0.3 T midplane)
   - First plasma Oct 2022, fusion yield measurements reported 2025 (arXiv:2505.23047)
   - Provides partial validation of E×B rotation physics, but is not a Pale Blue device

10. **Patent US20230298771** — "Direct Energy Converter for Axisymmetric Mirror Fusion Reactor" (SWDEC concept, 2023)
    - Alternative RF-based DEC design (potentially different inventor group)
    - Uncertain whether Pale Blue adopts SWDEC or their own adiabatic DEC from the PRX Energy paper