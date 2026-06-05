## Design Point

- Name: First Light projectile pilot plant (2022 pre-pivot ~150 MWe target)
- Maturity: paper-concept
- P_native: 150 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/22-projectile-icf/iter-03/sources/prnewswire-news-releases-first-light-achieves-world-first.md
  - knowledge/concept_research/22-projectile-icf/iter-01/sources/first-light-fusion-technology.md

---

## Section 1: Availability of Data

**Rating: Limited**

The Projectile ICF concept as pursued by First Light Fusion has a narrow data base for techno-economic analysis. The key sources are:

1. **First Light Fusion press release (April 2022)** — confirms fusion demonstration at 6.5 km/s projectile speed, validated by UKAEA, and states a pilot plant target of "~150 MW of electricity" costing "less than $1 billion in the 2030s." This is the only source that names the design point's power and cost target.[^1]

2. **Hawker (2020), Phil. Trans. R. Soc. A** — "A simplified economic model for inertial fusion" provides a 14-parameter LCOE framework explicitly designed around First Light's high-gain, low-rep-rate approach. It supplies key economic parameters (driver cost $/J, yield cost $/GJ, target cost) and establishes gain > 500 + yield > 5 GJ as the regime where costs become competitive.[^2]

3. **IP Group press release (September 2025)** — describes the FLARE pivot, claims gain of up to 1000, FLARE demonstration facility cost of $100M–$200M ($2/J stored energy), and 400 MW commercial plant targets. Provides cost comparison data.[^3]

4. **The Engineer (February 2026)** — confirms tritium breeding ratio of 1.8 validated by TUV SUD UK at FLARE's 333 MWe design point, net surplus of 25 kg/year tritium.[^4]

> "First Light is working towards a pilot plant producing ~150 MW of electricity and costing less than $1 billion in the 2030s."
> — prnewswire-news-releases-first-light-achieves-world-first.md §Next Steps

No peer-reviewed power plant design study exists for the projectile ICF pilot. The 150 MWe target is a press-release figure with no published systems engineering backing. No independent cost analysis (analogous to ARIES/PROCESS for tokamaks) has been published for this concept. The company pivoted away from the projectile approach in September 2025, making further data unlikely.

**Key data gaps:**
- No published thermal-hydraulic design, chamber geometry, or energy balance
- No published driver energy or stored energy requirement for the pilot
- No breakdown of the "<$1B" cost target by subsystem
- Repetition rate is stated inconsistently (30 s, 10 s, 90 s between shots)
- No target manufacturing cost estimate at volume
- No published Q_eng or recirculating power fraction

[^1]: prnewswire-news-releases-first-light-achieves-world-first.md §Next Steps
[^2]: pmc-articles-pmc7658748.md §Abstract and §2. Model
[^3]: ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Cost comparisons estimates
[^4]: theengineer-content-news-first-light-fusion-claims-tritium/output.md

---

## Section 2: Challenges in Capturing System Function

### 2.1 Undefined Driver System (Critical)

The pilot plant design calls for an electromagnetic gun launching projectiles at ~60 km/s (Machine 4 target, cancelled February 2025). The only demonstrated speed is 6.5 km/s (Machine 3, gas gun). No electromagnetic launcher at the required speed exists. The stored energy requirement, pulse repetition capability, and cost of such a driver are entirely uncharacterized. The press release mentions "100 MJ stored energy" for Machine 4 but this refers to a cancelled single-shot experimental device, not a rep-rated power plant driver.

### 2.2 Target Gain Extrapolation (Critical)

The concept's economic case depends on target gains of 200–1000. The demonstrated result produced ~50 neutrons — a scientific proof-of-concept, not an engineering demonstration. The gain curve connecting these regimes is based on First Light's proprietary simulations, not on an established physics database. Hawker (2020) shows that LCOE is extremely sensitive to gain in this regime:

> "A combination of high gain (greater than 500) and high fusion energy yield per shot (greater than 5 GJ) together appear to unlock more cost competitive designs"
> — pmc-articles-pmc7658748.md §Abstract

### 2.3 Repetition Rate Ambiguity (High)

Multiple figures appear in sources: "once every 30 seconds" (0.033 Hz), "once every 10 seconds" (0.1 Hz for 500 MW plant), "once every 90 seconds." For a fixed fusion yield per shot, rep rate directly sets average thermal power. A factor-of-3 uncertainty in rep rate propagates directly into a factor-of-3 uncertainty in plant power output (or equivalently, in the yield per shot required to hit 150 MWe at a given rep rate).

### 2.4 Target Manufacturing at Scale (High)

The target is described as "very complex" as an object. No target cost estimate is published. Hawker's model treats target cost as a free parameter, noting that even $1/target at 0.033 Hz is only ~1M targets/year — far less demanding than laser IFE (10 Hz = 315M targets/year). However, complexity per target is higher.

### 2.5 Liquid Lithium Chamber Engineering (Moderate)

The "1-meter-thick curtains of liquid lithium metal flowing within the chamber" serve as blanket, shield, and heat transfer medium. This concept draws on HYLIFE heritage (1980s–1990s LLNL studies). The OSTI source on electromagnetic pumping of liquid lithium (UCRL-53356, 1983) gives design parameters for HYLIFE: 72 m³/s flow rate, 800 tonnes inventory, 50–60% pump efficiency. However, these were for a different chamber geometry and higher rep rate. No published adaptation to First Light's sub-Hz regime exists.

### 2.6 Post-Pivot Status (Context)

First Light pivoted to FLARE (pulsed-power liner implosion with fast ignition) in September 2025 and abandoned plans for building a projectile fusion power plant, instead pursuing a technology-licensing model. No active commercial pursuer of the pure projectile ICF design point remains. This makes the 150 MWe pilot plant a historical design point that will not be further developed.

---

## Section 3: Maturity of Key Subsystems and Components

Subsystems ranked in ascending order of maturity:

### Electromagnetic Gun Driver — TRL 1–2 (Missing at scale)

First Light achieved 6.5 km/s with a two-stage gas gun (Machine 3). The electromagnetic launcher needed for a power plant (~60 km/s, rep-rated, 100 MJ stored energy) was never built. Machine 4 was cancelled in February 2025. No electromagnetic gun at any scale has demonstrated the required projectile velocities for high-gain fusion targets.

### Target Design for High Gain — TRL 2 (On paper only)

The 2022 experiment produced ~50 neutrons. The target amplified impact pressure by ~20×. Designs achieving gain 200–1000 exist only in simulation. The FLARE pivot explicitly acknowledges that high gain requires a different approach (fast ignition) rather than pure projectile compression.

> "The design used to achieve this result is already months out of date. As soon as we reach the maximum with one idea, we invent the next"
> — prnewswire-news-releases-first-light-achieves-world-first.md §Dr Nick Hawker quote

### Liquid Lithium Chamber with Flowing Curtains — TRL 2–3 (On paper only)

The chamber concept (flowing lithium curtains absorbing blast energy, breeding tritium, shielding walls) draws on HYLIFE heritage but has never been demonstrated at any scale for projectile ICF geometry. The HYLIFE program studied FLiBe jets rather than pure lithium curtains at the geometry First Light describes. First Light claims "lifetime-of-plant vessel" because neutrons never reach the vessel wall.

### Tritium Breeding Blanket — TRL 3 (On paper only, independently validated)

TBR of 1.8 validated by TUV SUD UK (February 2026) for the FLARE geometry. The liquid lithium approach (natural lithium, no enrichment needed) is simpler than FLiBe/Li-6 alternatives. However, this validation is a neutronics calculation, not a physical demonstration. No tritium extraction or processing system has been designed.

### Energy Conversion (Steam Rankine) — TRL 7–8 (Demonstrated)

> "After the lithium heat exchanger, the plant is identical to many other already working facilities"
> — first-light-fusion-technology.md §FLARE

Steam Rankine cycle from a lithium-to-water heat exchanger is entirely conventional. The thermal conversion efficiency can be bounded at 33–40% based on lithium outlet temperatures typical of IFE designs.

### Balance of Plant (Turbine, Generator, Grid Connection) — TRL 9 (Mature)

Standard power plant equipment. No novel engineering required downstream of the heat exchanger.

---

## Section 4: Key Materials and Supply Chain Considerations

### Liquid Lithium Inventory

The HYLIFE reference design used 800 tonnes of lithium. First Light's chamber at 150 MWe would likely require less (lower rep rate → less flow → smaller inventory) but no published figure exists. High-purity lithium metal costs ~$100/kg (Hawker 2020). At 400–800 tonnes, the lithium inventory alone represents $40M–$80M — a significant fraction of the plant capital. Global lithium production is ~130,000 tonnes/year (2024), primarily for batteries. A single fusion plant would require <1% of global supply but the high-purity metal form is a smaller market than battery-grade lithium carbonate.

### Projectile Materials

The projectile must survive electromagnetic acceleration to ~60 km/s. Material requirements are not publicly specified. At one shot every 30 seconds, consumption is ~1M projectiles/year. If projectiles are metal (aluminum, copper, or tungsten), material cost is likely modest (<$1/projectile for a few-gram projectile). Manufacturing precision requirements are unknown.

### Target Materials

Targets contain deuterium-tritium fuel in a "few mm" capsule surrounded by a complex amplifier structure. No materials specification is published. The per-target cost at volume is the key unknown. Hawker's model explores target costs from $0.10 to $100; at 0.033 Hz the annual target count is ~1.04M, making total target cost $0.1M–$104M/year depending on unit cost.

### Tritium

Standard D-T concern. Startup inventory required (order 1–5 kg at ~$30,000/g). First Light claims TBR 1.8 and self-sufficiency "in as little as one week" at the 333 MWe design point. At 150 MWe, tritium consumption scales roughly proportionally. The high TBR (if achievable) would make this concept a net tritium producer and potential supplier to other D-T concepts.

### Electromagnetic Gun Components

The driver would require large capacitor banks, high-current switches, and electromagnetic acceleration coils. These are industrial components (similar to railgun technology developed for defense applications) but have never been built for the energy levels and repetition rates required. No supply chain assessment exists.

---

## Section 5: Design Point Parameters

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| net_electric_MWe | 150 MWe | prnewswire-news-releases-first-light-achieves-world-first.md §Next Steps | medium | spec key: drives `P_native` |
| target_gain | 200–1000 | ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Technical background | low | Gain 200 is minimum for commercial viability per FLF economic modeling; 1000 is aspirational upper bound |
| rep_rate_Hz | 0.033 (baseline) | prnewswire-news-releases-first-light-achieves-world-first.md §Fusion Facts: "every 30 seconds" | medium | Conflicting values: 0.011–0.1 Hz range in sources |
| fusion_energy_per_shot_GJ | ~7.5 GJ | [inferred: at 150 MWe, 0.033 Hz, 35% thermal efficiency, blanket multiple 1.15 → P_th = 150/0.35 = 429 MW → E_f = 429/(0.033 × 1.15) = ~11.3 GJ fusion; adjusted for recirculating power → ~7.5 GJ at gain 250] | low | Sensitive to gain, rep rate, and efficiency assumptions; not published |
| driver_energy_MJ | ~100 MJ (stored) | first-light-fusion-technology.md §Machine 4 description (cancelled) | low | Machine 4 target; never built; actual pilot driver energy unknown |
| projectile_speed_km_s | ~60 | prnewswire-news-releases-first-light-achieves-world-first.md §Fusion Facts: "fuel accelerated to over 70 km per second as it implodes" | low | 60 km/s is Machine 4 target; fuel implodes at >70 km/s due to amplification |
| projectile_speed_demonstrated_km_s | 6.5 | prnewswire-news-releases-first-light-achieves-world-first.md §body: "6.5 km per second" | high | Gas gun demonstration, not electromagnetic |
| target_pressure_amplification | >20× | prnewswire-news-releases-first-light-achieves-world-first.md §Fusion Facts | high | Demonstrated in 2022 experiment |
| fuel_compression_TPa | 10 | prnewswire-news-releases-first-light-achieves-world-first.md §Fusion Facts: "10 Terapascals" | high | Demonstrated condition |
| TBR | 1.8 | theengineer-content-news-first-light-fusion-claims-tritium/output.md §body | high | Validated by TUV SUD UK; note: this is for FLARE geometry, assumed same for projectile plant |
| lithium_blanket_thickness_m | 1.0 | dossier.md §Tritium Breeding: "1-meter-thick curtains" | medium | |
| eta_th | 0.33–0.40 | [analogue: steam Rankine from liquid lithium heat exchanger; HYLIFE-II design used similar cycle] | medium | Not published for this design point |
| p_input_MW | ~30–50 | [estimated: driver 100 MJ at 0.033 Hz = 3.3 MW driver power; with EM gun wall-plug efficiency ~10–20% → 17–33 MW electrical; plus auxiliaries → ~30–50 MW total recirculating] | low | spec key: `p_input` — highly uncertain |
| LCOE_target_USD_MWh | <50 | prnewswire-news-releases-first-light-achieves-world-first.md §A consumables business model: "under $50/MWh" | medium | Company claim; Hawker (2020) peer-reviewed analysis |
| total_plant_cost_USD | <$1B | prnewswire-news-releases-first-light-achieves-world-first.md §Next Steps | low | No breakdown provided |
| driver_cost_USD_per_J | 1.7 (Machine 3 reference) | pmc-articles-pmc7658748.md §2. Model: "First Light's Machine Three… $1.7/J" | medium | Not rep-rated; pilot driver cost unspecified |
| energy_per_target_home_years | 2+ | prnewswire-news-releases-first-light-achieves-world-first.md §Fusion Facts: "enough energy to power the average UK home for over 2 years" | medium | ~5.6 GJ thermal per UK home per year → >11 GJ per shot implied |

---

## Section 5b: Override Candidates

### Per-Account Walkthrough

**C220101 — First wall, blanket & neutron multiplier**: The liquid lithium curtain design is distinctive — 1-meter-thick flowing lithium serving simultaneously as blanket, shield, and first wall. No dollar figure is published for this subsystem. The concept eliminates solid first-wall replacement (claimed "lifetime-of-plant vessel") which would reduce this account relative to solid-wall IFE designs. The HEAVY_ION archetype default ($64.8M at P_native) prices a solid blanket with neutron multiplier structures — structurally inapplicable to a flowing liquid-metal curtain. However, no company-grounded quantity or unit cost justifies a specific override value.

```yaml
  - account: C220101
    value: 64.8
    enabled: false
    provenance: derived
    source: "dossier.md §Neutron Management; prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
    rationale: |
      The library default ($64.8M) prices a solid blanket with neutron multiplier.
      First Light's design uses flowing liquid lithium curtains that serve as blanket,
      shield, and first wall simultaneously — a structurally different system. The curtain
      cost is better captured by the lithium inventory (CAS27 = $70M) plus the EM pump
      system (C220200, not overridable). No company-published dollar figure exists for the
      blanket subsystem alone. Disabled because the structural mismatch is acknowledged
      but no quantitative correction is derivable without double-counting CAS27.
```

**C220102 — Radiation shield**: The lithium curtain itself performs the shielding function; no separate radiation shield structure is described. The HEAVY_ION archetype default ($45.2M at P_native) prices a dedicated radiation shield structure behind the blanket. First Light's 1-meter-thick flowing lithium curtain absorbs all neutrons before they reach the vessel wall — "Neutrons do not reach vessel wall → lifetime-of-plant vessel" (dossier.md §Neutron Management). With no neutrons reaching the structural wall, a separate shield is structurally unnecessary. The shielding function is fully integrated into the lithium curtain (captured in CAS27 inventory cost).

```yaml
  - account: C220102
    value: 0.15 * generic.costs.C220102
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
    rationale: |
      The library default ($45.2M) prices a dedicated solid radiation shield behind
      the blanket. First Light claims neutrons never reach the vessel wall due to
      1-meter-thick lithium curtains. No separate shield structure is described.
      A small residual (15% of generic) is retained for biological shielding of
      penetrations (projectile entry port, target injection, diagnostics) and any
      secondary radiation paths not covered by the lithium curtain. Zero would
      under-price penetration shielding; the full default is structurally inapplicable.
```

**C220104 — Primary pulsed driver ($/J of driver energy)**: The electromagnetic gun is the primary driver. The only published cost metric is Machine 3 at $1.7/J stored energy (Hawker 2020). The IP Group release states FLARE demonstration facility at "$2 per Joule stored energy" ($100M–$200M for a 50–100 MJ system). For a 100 MJ pilot driver at $1.7–$2.0/J, the implied cost is $170M–$200M.

```yaml
  - account: C220104
    value: 200.0
    enabled: true
    provenance: derived
    source: "pmc-articles-pmc7658748.md §2. Model; ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Cost comparisons estimates"
    rationale: |
      Hawker (2020) published Machine 3 driver cost at $1.7/J stored.
      IP Group (2025) published FLARE demo at $2/J stored.
      Pilot design specifies 100 MJ stored energy (Machine 4 target).
      100 MJ × $2/J = $200M. Used $2/J as the more conservative (later, rep-rated)
      estimate. This is the electromagnetic gun + capacitor bank + power supply cost.
      Library IFE driver default (laser-based at $60–$700/J) is inapplicable to EM gun.
```

**C220105 — Primary structure**: No published cost data for the reactor vessel/structure. First Light claims the vessel is a simple steel container since lithium absorbs all neutrons before reaching the wall. This suggests lower cost than laser IFE chambers with final optics, but no dollar figure is available. **No override.**

**C220106 — Vacuum system**: The reaction chamber likely requires vacuum for projectile flight and target integrity. No published cost or specification. **No override.**

**C220107 — Pulsed-power capacitor bank ($/J stored)**: The 100 MJ stored energy for the EM gun is delivered from a capacitor bank. The $2/J figure from IP Group encompasses the entire driver (gun + bank + power supply). Since C220104 already captures the driver cost, and the EM gun architecture merges the capacitor bank with the launcher (unlike laser IFE where the bank powers the laser separately), this account should be zeroed to avoid double-counting with C220104.

```yaml
  - account: C220107
    value: 0.0
    enabled: true
    provenance: derived
    source: "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Cost comparisons estimates"
    rationale: |
      The EM gun driver cost ($2/J for 100 MJ = $200M) already includes the capacitor
      bank as an integral part of the electromagnetic launcher system. Unlike laser IFE
      where the bank charges the laser and the laser is a separate cost item, here
      the bank IS the driver's energy store. Setting to zero avoids double-counting.
```

**C220108 — Target factory (IFE/MIF target manufacturing)**: Targets are the core consumable. At 0.033 Hz, annual production is ~1.04M targets. No published target cost exists. Hawker's model treats it parametrically. However, the IP Group release states that the FLARE approach has "core components such as the energy delivery system costing 1/10th of the capital cost of previous fast ignition schemes" and that the sub-Hz rep rate "could also lower the operating costs." The company's business model centers on targets as a "high value-added consumables" — implying targets are not trivially cheap.

**Important caveat**: The override value below is a *viability-required ceiling* — the maximum target cost at which the concept remains economically viable — not an estimate of actual target manufacturing cost. No published $/target figure exists. The library default ($79.1M for a high-rep-rate IFE target factory producing 30M–300M targets/year) is structurally inapplicable to a sub-Hz concept producing ~1M targets/year. The override replaces a clearly wrong default with a viability-constrained placeholder. Actual target cost could be higher (making the concept uneconomic) or lower. The model carries a target-cost sensitivity sweep ($1–$20/target annualized) to bound this uncertainty.

```yaml
  - account: C220108
    value: 5.6
    enabled: true
    provenance: derived
    source: "pmc-articles-pmc7658748.md §2. Model (target cost framework); prnewswire-news-releases-first-light-achieves-world-first.md §A consumables business model"
    rationale: |
      VIABILITY CEILING, not a cost estimate. No published target cost exists.
      Hawker (2020) establishes that target cost must be <10% of electricity revenue
      for economic viability. At 150 MWe, 85% CF, $50/MWh LCOE target:
      Annual revenue = 150,000 × 8760 × 0.85 × $50/1000 = $55.8M.
      10% ceiling = $5.58M/year.
      At 0.033 Hz × 8760 × 3600 × 0.85 = 0.99M shots/year.
      Max target cost = $5.58M / 0.99M = ~$5.6/target.
      Value represents the annualized target-factory viability ceiling in $M/year.
      Library default ($79.1M for high-rep-rate IFE target factory) is structurally
      inapplicable at 1M/year volume. Actual cost is unknown — sensitivity sweep
      spans $1–$20/target to bound the range.
```

**C220110 — Remote handling & maintenance**: First Light claims the vessel never needs internal replacement due to lithium shielding — "Neutrons do not reach vessel wall → lifetime-of-plant vessel" (dossier.md §Neutron Management). If true, there is no first-wall or blanket module change-out, which eliminates the dominant remote-handling scope in conventional fusion designs. However, target injection, projectile gun maintenance, and lithium system access still require handling equipment. The HEAVY_ION archetype default ($33.5M at P_native) prices remote handling for periodic blanket and first-wall replacement — structurally inapplicable if no solid in-vessel components require replacement.

```yaml
  - account: C220110
    value: 0.30 * generic.costs.C220110
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
    rationale: |
      The library default ($33.5M) prices remote handling for periodic blanket/first-wall
      replacement. First Light's liquid lithium curtain eliminates solid in-vessel component
      replacement ("lifetime-of-plant vessel"). Remaining RH scope covers projectile gun
      access, target injection systems, lithium loop maintenance, and diagnostic equipment.
      30% of generic is an analogue estimate: ~70% of conventional RH cost is driven by
      blanket/first-wall change-out (based on tokamak cost studies where blanket RH is the
      dominant scope item), leaving ~30% for other in-vessel and ex-vessel handling needs.
```

**C220111 — Reactor-equipment installation & assembly**: The library computes C220111 as `installation_frac` × the reactor equipment subtotal. Because C220111 is computed from the *pre-override* subtotal in the library's CAS22 rollup, cost overrides that dramatically reduce the equipment accounts (C220104: $12,591M → $200M; C220107: $420M → $0; C220108: $79M → $5.6M) do not automatically reduce C220111. This is corrected in the model via the `installation_frac` spec parameter, not as a cost override — `installation_frac` is adjusted so that 14% of the *post-override* equipment subtotal (~$301M) is produced by the library's computation, yielding C220111 ≈ $42.2M. This is a spec-level correction for a library computation artifact, not an accountable cost departure. **Not an override** — handled as a spec parameter in model_setup.py.

**CAS21 — Buildings & site structures**: The IP Group release notes the plant is "compact enough to integrate seamlessly into existing power grids" and that the technology "leverag[es] existing supply chains." The <$1B total plant cost constrains CAS21 implicitly, but no breakdown is available. Given the simple chamber design (steel vessel, no superconducting magnets, no complex optics), buildings costs should be lower than laser IFE or tokamak concepts. An analogue from Hawker's $3,600/kWe total for HYLIFE (which includes all accounts) suggests buildings at ~15% of total = $540/kWe × 150 MW = $81M. This is too speculative for an override. **No override.**

**CAS23 — Turbine plant equipment**: Steam Rankine cycle is standard. No reason to override the library default for a thermal-cycle plant at 150 MWe. **No override.**

**CAS24 — Electric plant equipment**: No specific data. **No override.**

**CAS26 — Heat rejection system**: Standard cooling for a 150 MWe thermal plant. **No override.**

**CAS27 — Special materials (initial reactor material inventory)**: The lithium inventory is a major cost item. Hawker (2020) provides the key data: lithium at ~$100/kg, with HYLIFE requiring 800 tonnes ($80M). For a 150 MWe sub-Hz plant, inventory requirements are driven by blast absorption (yield per shot) and flow architecture. Using Hawker's lower-bound estimate (heat capacity sizing: cost = $70k/GJ of fusion energy per shot), at ~7.5 GJ/shot: $70k × 7.5 = $525k minimum. The HYLIFE upper bound ($44M/GJ) clearly applies to a different (multi-GJ, high-rep) design. A reasonable estimate for a ~7.5 GJ, sub-Hz system is 200–400 tonnes of lithium ($20M–$40M) based on scaling from HYLIFE's 800 tonnes at 8 Hz to sub-Hz with proportional flow reduction. Using $70M (IP Group's "natural lithium per reactor" figure from their cost comparison):

```yaml
  - account: CAS27
    value: 70.0
    enabled: true
    provenance: direct
    source: "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Cost comparisons estimates"
    rationale: |
      IP Group press release directly states "Natural lithium per reactor: $70M"
      in the cost comparison table. This represents the initial lithium inventory
      for the reactor chamber. Compares to "$143M-$451M for enriched lithium
      alternatives" — First Light uses natural lithium (no enrichment needed due
      to TBR 1.8 with natural Li). Library default for special materials does not
      account for the large liquid-metal inventory unique to this architecture.
```

**CAS70 — Annualized O&M + scheduled component replacement**: First Light claims no first-wall or vessel replacement is needed ("lifetime-of-plant vessel"). The primary maintenance items would be the EM gun components and target injection system. At sub-Hz rep rate, component wear is orders of magnitude lower than high-rep IFE. However, no published O&M cost exists. Hawker's model uses $10–$100/kWe-yr as the nuclear analogue range. At $50/kWe-yr (midpoint), O&M = $7.5M/year for 150 MWe. This is within normal analogue bounds and does not justify an override. **No override.**

**CAS80 — Annualized fuel cost**: Deuterium is negligible. Tritium is self-bred with TBR 1.8 (net producer). Target cost is captured in C220108. No separate fuel procurement cost beyond startup tritium inventory. The startup tritium is a capital item (CAS27), not an annual cost. **No override** (targets already captured, tritium self-sufficient).

### Override Count Check

Total override entries: 7 (C220101, C220102, C220104, C220107, C220108, C220110, CAS27).
Enabled overrides: 6 (C220102, C220104, C220107, C220108, C220110, CAS27).
Disabled overrides: 1 (C220101 — structural mismatch acknowledged but no quantitative correction derivable without double-counting CAS27).

Expected band for Low archetype-fit: 6–12 enabled overrides.

The count of 6 enabled overrides falls within the expected band. Four overrides (C220104, C220107, C220108, CAS27) are grounded in company-published cost data or peer-reviewed parametric analysis. Two overrides (C220102, C220110) are derived corrections for structural mismatches between the HEAVY_ION archetype defaults and the liquid-lithium-curtain, sub-Hz, EM-gun architecture. C220111 (installation labor) is corrected via the `installation_frac` spec parameter rather than as a cost override — this is a spec-level correction for a library computation artifact, not an accountable cost departure (see C220111 walkthrough entry above).

```yaml
overrides:
  - account: C220101
    value: 64.8
    enabled: false
    provenance: derived
    source: "dossier.md §Neutron Management; prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
    rationale: |
      The library default ($64.8M) prices a solid blanket with neutron multiplier.
      First Light's design uses flowing liquid lithium curtains that serve as blanket,
      shield, and first wall simultaneously — a structurally different system. The curtain
      cost is better captured by the lithium inventory (CAS27 = $70M) plus the EM pump
      system (C220200, not overridable). No company-published dollar figure exists for the
      blanket subsystem alone. Disabled because the structural mismatch is acknowledged
      but no quantitative correction is derivable without double-counting CAS27.

  - account: C220102
    value: 0.15 * generic.costs.C220102
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
    rationale: |
      The library default ($45.2M) prices a dedicated solid radiation shield behind
      the blanket. First Light claims neutrons never reach the vessel wall due to
      1-meter-thick lithium curtains. No separate shield structure is described.
      A small residual (15% of generic) is retained for biological shielding of
      penetrations (projectile entry port, target injection, diagnostics) and any
      secondary radiation paths not covered by the lithium curtain. Zero would
      under-price penetration shielding; the full default is structurally inapplicable.

  - account: C220104
    value: 200.0
    enabled: true
    provenance: derived
    source: "pmc-articles-pmc7658748.md §2. Model; ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Cost comparisons estimates"
    rationale: |
      Hawker (2020) published Machine 3 driver cost at $1.7/J stored.
      IP Group (2025) published FLARE demo at $2/J stored.
      Pilot design specifies 100 MJ stored energy (Machine 4 target).
      100 MJ × $2/J = $200M. Used $2/J as the more conservative (later, rep-rated)
      estimate. This is the electromagnetic gun + capacitor bank + power supply cost.
      Library IFE driver default (laser-based at $60–$700/J) is inapplicable to EM gun.

  - account: C220107
    value: 0.0
    enabled: true
    provenance: derived
    source: "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Cost comparisons estimates"
    rationale: |
      The EM gun driver cost ($2/J for 100 MJ = $200M) already includes the capacitor
      bank as an integral part of the electromagnetic launcher system. Unlike laser IFE
      where the bank charges the laser and the laser is a separate cost item, here
      the bank IS the driver's energy store. Setting to zero avoids double-counting.

  - account: C220108
    value: 5.6
    enabled: true
    provenance: derived
    source: "pmc-articles-pmc7658748.md §2. Model; prnewswire-news-releases-first-light-achieves-world-first.md §A consumables business model"
    rationale: |
      VIABILITY CEILING, not a cost estimate. No published target cost exists.
      Hawker (2020) establishes that target cost must be <10% of electricity revenue
      for economic viability. At 150 MWe, 85% CF, $50/MWh LCOE target:
      Annual revenue = 150,000 × 8760 × 0.85 × $50/1000 = $55.8M.
      10% ceiling = $5.58M/year annualized target factory + consumables cost.
      At 0.033 Hz × 8760 × 3600 × 0.85 = 0.99M shots/year.
      Max target cost = $5.58M / 0.99M = ~$5.6/target.
      Value represents the annualized target-factory viability ceiling in $M/year.
      Library default ($79.1M for high-rep-rate IFE target factory) is structurally
      inapplicable at 1M/year volume. Actual cost is unknown — sensitivity sweep
      spans $1–$20/target to bound the range.

  - account: C220110
    value: 0.30 * generic.costs.C220110
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
    rationale: |
      The library default ($33.5M) prices remote handling for periodic blanket/first-wall
      replacement. First Light's liquid lithium curtain eliminates solid in-vessel component
      replacement ("lifetime-of-plant vessel"). Remaining RH scope covers projectile gun
      access, target injection systems, lithium loop maintenance, and diagnostic equipment.
      30% of generic is an analogue estimate: ~70% of conventional RH cost is driven by
      blanket/first-wall change-out (based on tokamak cost studies where blanket RH is the
      dominant scope item), leaving ~30% for other in-vessel and ex-vessel handling needs.

  # C220111 (installation labor) is NOT an override — it is corrected via the
  # installation_frac spec parameter. See the per-account walkthrough for details.

  - account: CAS27
    value: 70.0
    enabled: true
    provenance: direct
    source: "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md §Cost comparisons estimates"
    rationale: |
      IP Group press release directly states "Natural lithium per reactor: $70M"
      in the cost comparison table. This represents the initial lithium inventory
      for the reactor chamber. Compares to "$143M-$451M for enriched lithium
      alternatives." First Light uses natural lithium (no enrichment needed due
      to TBR 1.8 with natural Li). Library default for special materials does not
      account for the large liquid-metal inventory unique to this architecture.
```

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No published driver energy requirement or EM gun design for the pilot plant | S2, S5 | truly-unknown | blocking | None available — concept abandoned; original Machine 4 specs (100 MJ) are the only reference |
| 2 | No target gain curve or physics basis for gain 200–1000 from projectile compression alone | S2, S5 | proprietary | blocking | First Light's proprietary simulation database; FLARE white paper may contain partial data |
| 3 | No thermal-hydraulic design or chamber geometry for the 150 MWe plant | S2, S3 | truly-unknown | blocking | HYLIFE/HYLIFE-II studies (UCRL-53356, Hoffman 1990) provide analogues but not direct data |
| 4 | Repetition rate for 150 MWe (0.011–0.1 Hz range) | S2, S5 | proprietary | important | Company sources give conflicting values; 0.033 Hz (30 s) is most frequently cited |
| 5 | Target manufacturing cost at volume — C220108 override is a viability ceiling ($5.6/target), not an estimate; actual cost unknown | S4, S5b | truly-unknown | important | No published estimate; Hawker (2020) provides parametric framework; model carries $1–$20/target sensitivity sweep |
| 6 | EM gun wall-plug efficiency at required velocities | S2, S5 | truly-unknown | important | Defense railgun literature may provide analogues (typically 20–40% for military railguns at lower velocities) |
| 7 | Capital cost breakdown of the <$1B plant target | S5, S5b | proprietary | important | Only the total figure is published; no subsystem allocation |
| 8 | Lithium inventory sizing for sub-Hz projectile ICF chamber | S4, S5 | derivable | nice-to-have | Could be derived from HYLIFE scaling with appropriate adjustments for yield/rep-rate |
| 9 | O&M cost structure (fixed vs. variable, staffing, scheduled maintenance) | S3 | not-yet-sourced | nice-to-have | No fusion-specific O&M data; nuclear analogue ($50–100/kWe-yr) is typical assumption |
| 10 | Tritium startup inventory requirement for 150 MWe plant | S4 | derivable | nice-to-have | Derivable from TBR 1.8, burn rate at P_native, and doubling time claim ("one week") |

---

## Section 7: Family-Delta vs Comparables

No comparable concept in the corpus for this design point. The upstream pipeline assigns an empty comparables list because no other concept in the corpus shares the defining characteristics of sub-Hz electromagnetic-gun-driven projectile ICF: (a) the driver is a hypervelocity electromagnetic launcher, not a laser, accelerator, or pulsed-power liner driver; (b) the operating regime is uniquely low-frequency (0.033 Hz vs. 1–10 Hz for laser IFE or 5–10 Hz for heavy-ion beam IFE); and (c) the liquid lithium curtain chamber replaces solid blanket/shield structures entirely. NearStar Fusion pursues a related projectile concept but uses a railgun variant with magneto-inertial target compression (MTIF approach) — a different enough architecture that the upstream pipeline does not assign it as a comparable. The HEAVY_ION archetype is therefore the only structured reference frame, and all cost deltas below are articulated against its defaults.

### Delta Against the HEAVY_ION Archetype

The library's HEAVY_ION archetype (the generic forward that governs all default costs for this concept) is calibrated to a heavy-ion beam IFE plant: a multi-GeV particle accelerator driver at 5–10 Hz rep rate, FLiBe molten-salt coolant with jet arrays, and conventional solid blanket/shield structures. Projectile ICF diverges from this archetype in nearly every major subsystem. The following table articulates each structural delta and its cost direction:

| Subsystem | HEAVY_ION Archetype | Projectile ICF (First Light) | Cost Direction |
|-----------|--------------------|-----------------------------|----------------|
| **Driver (C220104)** | Multi-GeV heavy-ion accelerator ($60–$700/J typical for particle accelerators/lasers) | Electromagnetic gun ($1.7–$2/J stored energy) | **Strong advantage** — >30× reduction in driver cost per joule; override $200M vs. generic $12,591M |
| **Capacitor bank (C220107)** | Separate pulsed-power bank charging the accelerator | Integrated into the EM gun system (captured in C220104) | **Advantage** — zeroed to avoid double-counting; generic $420M eliminated |
| **Rep rate** | 5–10 Hz (high-frequency IFE baseline) | 0.033 Hz (one shot every 30 seconds) | **Mixed** — reduces target factory throughput (advantage) but demands very high yield per shot and gain >200 to reach economic power output |
| **Target factory (C220108)** | High-rep-rate factory producing 30M–300M targets/year | ~1M targets/year at 0.033 Hz | **Advantage** — two orders of magnitude fewer targets; override $5.6M/yr vs. generic $79.1M |
| **Blanket/first wall (C220101)** | Solid blanket with neutron multiplier structures | Flowing liquid lithium curtains (no solid first wall) | **Structural mismatch** — cost captured in lithium inventory (CAS27) rather than fabricated blanket hardware |
| **Radiation shield (C220102)** | Dedicated solid shield behind blanket | Eliminated; 1 m lithium curtain absorbs all neutrons | **Advantage** — override to 15% of generic for penetration shielding only |
| **Coolant system (C220200)** | FLiBe molten-salt loop with mechanical pumps | Liquid lithium with electromagnetic pumps (72 m³/s HYLIFE reference) | **Structural mismatch** — EM pumps for liquid metal vs. mechanical pumps for molten salt; C220200 not in override schema |
| **Remote handling (C220110)** | Periodic blanket/first-wall replacement | No solid in-vessel replacement ("lifetime-of-plant vessel") | **Advantage** — override to 30% of generic; only gun/target-injection RH remains |
| **Installation (C220111)** | Scaled from reactor equipment subtotal | Must scale from post-override subtotal (~$301M, not $13,247M) | **Correction** — spec-level `installation_frac` adjustment yields $42.2M vs. generic $1,855M (library artifact); not a cost override |
| **Special materials (CAS27)** | Standard initial inventory | 200–800 tonnes natural lithium at $70M (company-published) | **Penalty** — $70M override vs. generic $2.2M; liquid-metal inventory is a major cost unique to this architecture |
| **Beam transport magnets** | Large superconducting quadrupole array for beam focusing | None — projectile is mechanically guided | **Advantage** — eliminates SC magnet supply chain entirely |

**Net assessment**: The archetype mismatch is pervasive. The projectile ICF concept trades the accelerator-physics complexity of heavy-ion beam IFE for mechanical-engineering complexity (hypervelocity EM guns, liquid-metal hydrodynamics) at fundamentally different cost scales. The dominant cost advantage is the >30× reduction in driver cost per joule. The dominant cost penalty is the large liquid lithium inventory ($70M). The dominant uncertainty is whether the sub-Hz, high-gain operating regime (gain >200, yield >5 GJ per shot) is physically achievable — this has no experimental demonstration beyond ~50 neutrons.

### Supplementary Cross-Concept Context (outside the formal comparables framework)

The following comparisons are informal positioning against other IFE/MIF concepts in the corpus. They are not structured cost-delta analyses against assigned comparables (which are empty for this concept) but provide useful context for the reader.

- **vs. Laser ICF concepts (Xcimer, Inertia, Focused Energy)**: Projectile ICF replaces the laser driver (at $60–$700/J) with an electromagnetic gun ($1.7–$2/J). The tradeoff is that the projectile approach requires extremely high target gain (>200) to compensate for the low repetition rate, whereas laser IFE can achieve economic power output at gain 30–100 with 1–10 Hz rep rates.

- **vs. MagLIF/Pulsed power (Pacific Fusion)**: Both use pulsed electrical energy stores at comparable $/J ($1.7–$5/J). MagLIF uses the electrical energy directly to implode a liner, while projectile ICF converts it to kinetic energy in a projectile. MagLIF has a more extensive physics database (>70 experiments on Z) but faces similar rep-rate and per-shot consumable challenges.

- **Unique features**:
  - Sub-Hz operation (0.033 Hz) — drastically reduces target factory requirements but demands very high yield per shot
  - Natural lithium blanket with TBR 1.8 — avoids Li-6 enrichment costs ($143M–$451M per IP Group) and creates a tritium-surplus revenue stream
  - No magnets, no lasers, no superconductors — radically simplified supply chain

---

## Section 8: Sources

1. **First Light Fusion press release (April 2022)** — "First Light achieves world first fusion result, proving unique new target technology." Provides the design point (150 MWe, <$1B), demonstrated performance (6.5 km/s, ~50 neutrons, 10 TPa), and power plant architecture description. Path: `iter-03/sources/prnewswire-news-releases-first-light-achieves-world-first/output.md`

2. **Hawker, N. (2020). "A simplified economic model for inertial fusion." Phil. Trans. R. Soc. A 378: 20200053** — Peer-reviewed 14-parameter LCOE model designed around First Light's approach. Establishes gain/yield requirements, driver cost benchmarks ($1.7/J for Machine 3), and yield cost framework. The most rigorous published economics source for this concept. Path: `iter-03/sources/pmc-articles-pmc7658748/output.md`

3. **IP Group press release (September 2025)** — "First Light Fusion Publishes First Plausible Path to High Gain, Unlocking Cheap Fusion Energy." FLARE pivot details, cost comparisons ($2/J FLARE demo, $70M natural lithium per reactor), 400 MW commercial targets. Path: `iter-03/sources/ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md`

4. **The Engineer (February 2026)** — "First Light Fusion validates tritium breeding concept." TBR 1.8 validated by TUV SUD UK, 333 MWe design point, 25 kg/year net tritium surplus. Path: `iter-03/sources/theengineer-content-news-first-light-fusion-claims-tritium/output.md`

5. **World Nuclear News (September 2025)** — "First Light Fusion presents novel approach to fusion." FLARE white paper details, gain 1000 pathway, cost comparisons with NIF. Path: `iter-02/sources/first-light-flare-pivot-update.md`

6. **First Light Fusion website** — Technology overview, power plant description, liquid lithium architecture. Path: `iter-01/sources/first-light-fusion-technology.md`

7. **NearStar Fusion website and VIPC investment announcement** — Contextual comparison for railgun-based projectile ICF variant (MTIF approach). Not used for the First Light design point but informative for the broader concept space. Paths: `iter-01/sources/nearstar-fusion-technology.md`, `iter-02/sources/nearstar-fusion-2025-update.md`

8. **Baker, Blink & Tessier (1983). "Electromagnetic Pumping of Liquid Lithium in Inertial Confinement Fusion Reactors." UCRL-53356, LLNL** — HYLIFE reactor EM pump design (72 m³/s flow, 50–60% efficiency). Provides engineering context for liquid lithium circulation systems. Path: `iter-03/sources/osti-servlets-purl-6360934/output.md`

9. **Hoffman (1990). "The Heat Transport System and Plant Design for the HYLIFE-II Fusion Reactor."** — HYLIFE-II FLiBe design, heat exchanger optimization, BOP design. Provides analogue for IFE thermal plant architecture. Path: `iter-03/sources/osti-servlets-purl-6780071/output.md`
