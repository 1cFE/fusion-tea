---
ID: 24-dense-plasma-focus
Concept: Dense Plasma Focus (LPP Fusion)
Company: LPPFusion
Status: draft
Created: 2026-06-06
Approved-Date:
Confinement-Family: MFE
Archetype: DENSE_PLASMA_FOCUS
Archetype-Fit: Low
Comparison-Status: costingfe-asterisked
Comparables: []
Design-Point-Name: Focus Fusion commercial generator (Lerner et al. 2023)
Design-Point-Maturity: paper-concept
P-Native: 5.0
Grounding-Confidence: low
---

## Design Point

- Name: Focus Fusion commercial generator (Lerner et al. 2023)
- Maturity: paper-concept
- P_native: 5.0 MWe
- Grounding: low
- Primary sources:
  - knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2023-jfe-paper.md
  - knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-our-plan-to-net-energy/output.md

---

## Section 1: Availability of Data

**Rating: Limited**

LPPFusion publishes more than most pre-net-energy fusion startups, but the available material is almost entirely authored by the company itself. Two peer-reviewed papers form the quantitative backbone: Lerner et al. (2023) in *J. Fusion Energy* provides the most comprehensive overview of experimental results and the commercial generator concept, and Lerner et al. (2024) in *Frontiers in Physics* describes preparations for p-B11 testing on FF-2B. Both papers are authored solely by LPPFusion personnel with no independent co-investigators, which limits their value as external validation.

> "This paper reviews progress toward pB11 fusion with the dense plasma focus (DPF) device, known as FF-1 and FF-2B, at LPPFusion Inc., Middlesex, NJ."
> — lerner-2023-jfe-paper.md, §Introduction

The company's investor-facing documents (executive summary, "plan to net energy," technology pages) provide design targets and cost projections but are promotional in intent and do not disaggregate costs by subsystem.

No independent power plant study exists for the Focus Fusion commercial generator concept. There is no equivalent of the ARIES or Z-IFE studies for this device — no published system-code analysis, no independent cost estimate, no independent physics assessment of the commercial design point. The dossier notes no university or national laboratory co-publications on the commercial concept, only on laboratory-scale DPF physics more broadly.

**Key data gaps:**
- No published breakdown of the $1M device cost across subsystems (capacitor bank, electrodes, vacuum vessel, DEC, cooling, controls)
- No demonstrated conversion efficiency for the ion beam decelerator or x-ray photovoltaic converter at fusion-relevant energies
- No demonstrated p-B11 fusion yield — all experimental results are with deuterium fuel
- No published stored energy or voltage specification for the commercial generator's capacitor bank
- No independent validation of the QMFE bremsstrahlung suppression at commercial operating conditions
- Repetition rate demonstrations do not exist at fusion-relevant conditions; the 200 Hz target is extrapolated from engineering judgment, not experiment

---

## Section 2: Challenges in Capturing System Function

Five challenges dominate LCOE modeling of the Focus Fusion concept, ranked by impact on cost uncertainty.

**1. The QMFE assumption is the existential physics bet (blocking).** The entire economic case for p-B11 DPF fusion rests on the quantum magnetic field effect (QMFE) suppressing bremsstrahlung radiation by approximately a factor of five. Without QMFE, a p-B11 plasma radiates more bremsstrahlung power than it generates in fusion power regardless of confinement quality, because boron's Z=5 increases radiative losses. The QMFE requires extreme magnetic fields in the plasmoid (the plasmoid self-generates fields in the GG range, orders of magnitude beyond external magnets). LPPFusion's 0-D simulations show that fusion power can exceed bremsstrahlung by a factor of two under QMFE, but these simulations assume a uniform sphere and are acknowledged as "not fully realistic."

> "In addition, the high magnetic fields associated with such high densities make possible the use of the quantum magnetic field effect to reduce bremsstrahlung radiation. This is particularly important with pB11 fuel, where the relatively higher Z of boron nuclei tends to increase bremsstrahlung."
> — lerner-2024-frontiers-pB11-prep.md, §Introduction

No experiment has confirmed QMFE-suppressed bremsstrahlung. The entire thermal physics of the commercial design point is contingent on this unvalidated effect.

**2. The yield gap is enormous (blocking for near-term modeling).** The commercial generator requires ~60 kJ of fusion yield per shot to produce 25 kJ net electricity after direct energy conversion (~83% efficiency) minus bank recharge losses. Current FF-2B results with deuterium fuel achieve on the order of millijoules of fusion output — approximately eight orders of magnitude below the commercial target. LPPFusion's published path to closing this gap (doubling current to 2.4 MA, switching to p-B11 fuel, achieving improved compression to 50 µm plasmoid radius) must proceed in sequence, and each step rests on earlier undemonstrated steps.

**3. Filament disruption blocks progress at >1 MA (blocking for experimental validation).** Current experiments show a yield plateau above 1 MA: the current sheath filaments that drive the compression are being disrupted before completing their convergence. LPPFusion identifies two candidate mechanisms — a backward-propagating shock wave and high-frequency oscillations in the discharge current — but has not resolved the cause or demonstrated a fix.

> "We now have firm observational evidence that filaments are now forming but are being disrupted and disorganized during the run down."
> — lerner-2023-jfe-paper.md, §Experimental Challenges

**4. 200 Hz repetition rate is undemonstrated at any scale for fusion-class DPF (important).** The design requires 200 pulses per second to achieve 5 MWe net output from 25 kJ per shot. The fastest DPF repetition rate demonstrated in any application (the NX2 neutron source in Singapore) is 16 Hz — a small device used as an X-ray source, not a fusion generator. Going from single-shot to 200 Hz requires electrode cooling (up to 10 kW/cm²), fast-recovery capacitor banks, switch replacement compatible with high-rep-rate cycling, and debris clearing between shots. Each of these is an unsolved engineering problem.

**5. Direct energy conversion efficiency is undemonstrated at commercial scale (important for LCOE floor).** LPPFusion calculates ~85% for the ion beam decelerator and ~80% for the x-ray photovoltaic converter, giving a blended DEC efficiency of ~83%. These are theoretical calculations, not demonstrated results. If actual efficiency falls to 60%, the net energy per shot drops to near zero and the LCOE diverges. The DEC efficiency is thus both the key commercial advantage over thermal-cycle concepts and the largest single unverified claim in the commercial design.

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first).

**p-B11 net energy and QMFE-suppressed bremsstrahlung — On paper only.** No experimental confirmation of QMFE in any fusion device. No p-B11 fusion yield measured in any DPF device (LPPFusion's best experiments have produced no measurable p-B11 reactions; they are still optimizing the device with deuterium). The Frontiers 2024 paper describes "preparations for pB11 tests" — pB11 shots have not yet been attempted. This is the core physics TRL gap.

**200 Hz repetition rate — Missing at scale.** No DPF device has operated at 200 Hz under fusion-relevant conditions. The current FF-2B is single-shot. The engineering challenges (electrode cooling at 10 kW/cm², bank recharge in 5 ms, switch longevity over billions of cycles) have been analyzed but not built or demonstrated.

**Ion beam decelerator (commercial scale) — On paper only.** LPPFusion holds patents on an ion beam decelerator and has modeled ~85% efficiency, but no prototype has been built and tested with fusion ion energies. The concept (a particle accelerator in reverse) is physically sound, but scaling to megawatt average power levels and achieving the projected efficiency is undemonstrated.

**X-ray photovoltaic converter — On paper only.** Dimensions (40–50 cm inner radius, ~50 cm length per module) and efficiency (~80%) are calculated by Lerner et al. (2023) but no prototype exists. The photoelectric conversion of x-rays from a pulsed fusion source at commercial flux levels is novel technology with no demonstrated analogue at this scale.

**Beryllium electrode system (laboratory scale) — Demonstrated.** Beryllium electrodes have operated successfully on FF-2B since 2019, replacing earlier copper and tungsten variants. The beryllium choice resolved problems with arcing (eliminated by monolithic tungsten) and x-ray opacity (beryllium is nearly transparent to the 10s-keV x-rays from the plasma, reducing anode heating). However, demonstrated operation is at single-shot, laboratory-scale; monthly electrode replacement at 200 Hz commercial rep rate is a design target, not a demonstrated capability.

**Dense plasma focus pinch physics — Demonstrated (laboratory scale).** DPF pinch formation, filament development, and plasmoid creation are well-established physics demonstrated in hundreds of devices worldwide over six decades. Ion temperatures >200 keV have been demonstrated in FF-2B.

> "FF-1 [predecessor to FF-2B] achieved a record mean ion energy >200 keV in 2016 and a ten-shot mean ion-energy of 125 keV."
> — lerner-2023-jfe-paper.md, §Experimental Results

The high ion temperature is one of three conditions LPPFusion claims are necessary for net p-B11 energy; the other two (sufficient confinement time and QMFE-suppressed bremsstrahlung) remain undemonstrated.

**Balance of plant / power electronics — Demonstrated (conventional technology).** No thermal turbine is needed. Electrical BOP (switchyard, transformers, power distribution) is conventional and mature. The direct energy conversion approach eliminates the main TRL risk in the BOP by replacing the steam turbine with power electronics. Power conversion electronics for megawatt-class power conditioning are mature industrial technology.

---

## Section 4: Key Materials and Supply Chain Considerations

**Beryllium (electrodes) — critical constraint for fleet scale.** Beryllium is the electrode material for both anode and cathode in the current device. The commercial generator is assumed to use the same material.

> "Currently, world production of beryllium is about 400 tons per year. To power all the world's electricity needs with Focus Fusion generators would require approximately a 10-fold increase in beryllium production."
> — lerner-2023-jfe-paper.md, §Materials and Supply

A 1 GWe fleet of 200 modules requires monthly electrode replacement. The anode geometry (2.8 cm radius) implies a relatively small mass per electrode, but at 200 Hz operation over 30 years, the cumulative consumption is substantial. Beryllium toxicity (fine beryllium dust is a serious respiratory hazard) creates occupational health constraints on electrode fabrication and replacement operations. Current production is concentrated in the US (Materion) with secondary suppliers in Russia and Kazakhstan — a moderate concentration risk. Scale-up to 10× production is not impossible (beryllium abundance in the Earth's crust is comparable to lead) but requires opening lower-grade ore deposits and building new processing capacity over a decade-plus timeline.

**Isotopically pure decaborane (B₁₀H₁₄, B-11 enriched) — specialty fuel, manageable scale.** The commercial generator uses decaborane as the boron source, requiring isotopic purity: reactions with B-10 produce radioactive Be-7, while p-B11 reactions produce only stable He-4 and short-lived C-11 (20 min half-life). LPPFusion has acquired 93 grams of isotopically pure decaborane.

> "We have now received a limited but adequate quantity of isotopically-pure decaborane."
> — lerner-2024-frontiers-pB11-prep.md, §Fuel Preparations

Unlike beryllium, the fuel consumption per shot is tiny (microscopic quantities), and boron is abundant. A world fleet of Focus Fusion generators would require only ~10% increase in global boron production. The isotopic enrichment process (separating B-11 from natural boron, which is 80% B-11 and 20% B-10) is commercially available but at limited scale. This is a manageable supply constraint assuming adequate lead time for industrial scale-up.

**Diamond switches (proposed for DEC) — unproven at scale, limited supply chain.** Lerner (2023) proposes diamond-film photoconductive switches as the fast switching mechanism for the ion beam decelerator circuit. Diamond photoconductive switches (PCSS) exist in research-scale form (efficiencies ~20% in early TRL-3 demonstrations). Industrial synthetic diamond production for semiconductor applications is growing but expensive. The compound semiconductor article in the dossier describes diamond PCSS achieving record 44 A/cm² under 60V bias with rise/fall times of ~2 ns — appropriate switching characteristics — but at research scale. A commercial fleet would require millions of such switches. No supply chain for this application exists at scale.

**No HTS tape, no tritium, no REBCO, no NbSn — supply chain advantages.** DPF requires none of the materials that constrain most fusion concepts: no REBCO tape, no NbTi or Nb₃Sn, no tritium (startup or operating inventory), no Li-6 enriched breeding material, no beryllium or lead neutron multiplier blanket. These absences are genuine supply chain advantages. The electrode beryllium is the only fusion-specific material supply concern, and it is a far smaller constraint than REBCO or tritium supply chains would be.

---

## Section 5: Design Point Parameters

All parameters describe the Focus Fusion commercial generator (Lerner et al. 2023) at its native 5.0 MWe scale. This design point is entirely theoretical — no prototype of the commercial generator has been built. Parameters flagged `[inferred]` or `[estimated]` are derived from published device physics or scaling arguments.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| net_electric_MWe | 5.0 MWe | Design Point (fixed) | high | Drives module count at 1 GWe: n_mod = 200 |
| rep_rate_hz | ~200 Hz | lerner-2023-jfe-paper.md §5 MW Design Point | low | Design target; thermally limited; not demonstrated |
| energy_per_pulse_kj (net electric) | 25 kJ | lerner-2023-jfe-paper.md §5 MW Design Point | medium | 5 MW / 200 Hz = 25 kJ/pulse net; derives from stated P_native and rep rate |
| fusion_yield_per_pulse_kj | ~60 kJ | lerner-2023-jfe-paper.md §Net Energy Path | low | Needed to produce 25 kJ net after DEC + bank recharge losses; stated as ~60 kJ threshold in source |
| capacitor_stored_energy_kj | ~115 kJ | lerner-2023-jfe-paper.md §Experimental Device | medium | Measured on FF-1/FF-2B (12 caps × 113 µF, 45 kV); commercial bank may differ |
| capacitor_bank_voltage_kv | 40–45 kV | lerner-2023-jfe-paper.md §Experimental Device | medium | Operating range in current device |
| p_input_MW | ~0 (self-sustaining) | [inferred: bank recharged from DEC output at net-energy operation; grid draw limited to ancillary loads ~0.2 MW] | low | spec key: `p_input`; during Phase 2 testing, grid-fed charging dominates |
| anode_radius_cm | 2.8 cm | lerner-2023-jfe-paper.md §Experimental Device | high | spec key: analogous to plasma minor radius for DPF geometry |
| anode_length_cm | 6.6–10.6 cm | lerner-2023-jfe-paper.md §Experimental Device | high | Range explored experimentally |
| peak_current_ma | 2.4–2.7 MA | lerner-2023-jfe-paper.md §Experimental Device; lerner-2024-frontiers-pB11-prep.md §Device | medium | FF-2B target; 2.7 MA with upgraded switches; not yet demonstrated stably |
| peak_plasmoid_density_cm3 | ~10²¹ cm⁻³ | lerner-2023-jfe-paper.md §Plasma Parameters | medium | Approaches solid density; required for QMFE activation |
| ion_temperature_keV | >200 keV (demonstrated) | lerner-2023-jfe-paper.md §Experimental Results | high | Demonstrated with D fuel in FF-1; required for p-B11 ignition |
| nτT_product | 3.4 × 10²⁰ keV·s/m³ | lerner-2023-jfe-paper.md §Experimental Results | high | Best D result in FF-1; needs ~15× improvement for p-B11 net energy |
| ion_dec_efficiency | ~85% | lerner-2023-jfe-paper.md §Energy Capture | low | Calculated; not demonstrated at commercial energies |
| xray_photovoltaic_efficiency | ~80% | lerner-2023-jfe-paper.md §Energy Capture | low | Calculated; no prototype |
| xray_converter_inner_radius_cm | 40–50 cm | lerner-2023-jfe-paper.md §Energy Capture | medium | Per-module geometry |
| xray_converter_length_cm | ~50 cm | lerner-2023-jfe-paper.md §Energy Capture | medium | Per-module geometry |
| blended_dec_efficiency | ~83% | [inferred: 2/3 × 85% (ion) + 1/3 × 80% (x-ray) per energy split fraction] | low | No published energy split ratio; 2/3 ion, 1/3 x-ray estimated from device geometry |
| anode_tip_heat_flux_kw_cm2 | up to 10 kW/cm² | lerner-2023-jfe-paper.md §Engineering Constraints | medium | Drives helium cooling requirement |
| electrode_material | Beryllium | lerner-2023-jfe-paper.md §Electrode Materials | high | Since 2019; chosen for transparency to 10s-keV x-rays and oxide passivation |
| electrode_replacement_interval | ~monthly | lerner-2023-jfe-paper.md §Maintenance | low | Design target; erosion-limited; not demonstrated at rep rate |
| device_mass_tons | ~3 | lerner-2023-jfe-paper.md §Commercial Generator | medium | Per module |
| device_volume_m3 | ~30 | lerner-2023-jfe-paper.md §Commercial Generator | medium | Per module |
| device_capital_cost_per_module | <$1M ($0.10/W) | lerner-2023-jfe-paper.md §Commercialization | low | Mass-production projection; no prototype cost demonstrated |
| fuel | p-B11 (decaborane + H) | lerner-2023-jfe-paper.md | high | Commercial target; current experiments use deuterium |
| neutron_fraction | <1% of fusion energy | lerner-2023-jfe-paper.md §Introduction | high | Side reactions only; primary p-B11 → 3α is fully aneutronic |
| n_mod (1 GWe fleet) | 200 | [inferred: 1000 MWe / 5 MWe per module] | high | Drives fleet capital and NOAK learning curve |

**Note on `p_input` ambiguity for pulsed self-sustaining concepts.** In the commercial design, the capacitor bank is recharged from the DEC output at net-energy operation (no grid draw except ancillaries). The `p_input` spec key in 1costingFE represents auxiliary heating wallplug power for the library's physics solver; for DPF the relevant engineering quantities are `capacitor_stored_energy_kj` and `rep_rate_hz`, from which average driver power can be computed. The model-setup agent should treat `p_input` as the ancillary load (~0.2 MW estimated), not as the recirculating bank recharge power, to avoid double-counting fusion-driven recirculation.

---

## Section 5b: Override Candidates

Per-account walkthrough against the canonical 1costingFE schema for this archetype. Each account examined; overrides proposed only where company-grounded data or unambiguous architectural facts justify departing from the library default.

```yaml
overrides:

  # C220101 — First wall, blanket & neutron multiplier
  # No override. The DENSE_PLASMA_FOCUS library archetype already carries $0 for this
  # account, correctly reflecting that DPF with p-B11 has no neutron-breeding blanket
  # or heavy energy-capture blanket. The library default is already consistent with
  # the aneutronic architecture; a relative multiplier of any value evaluates to $0
  # and adds no information. Library default stands.

  # C220102 — Radiation shield
  # No override. The DENSE_PLASMA_FOCUS library archetype already carries $0 for this
  # account. Side reactions produce <1% of fusion energy as neutrons, but the library
  # correctly zeros this account for the DPF archetype. A relative multiplier evaluates
  # to $0 identically. Library default stands.

  # C220104 — Supplementary plasma heating / primary pulsed driver (laser/accelerator/gun)
  # Per schema note: "electrical-drive concepts cost it in C220107." DPF is driven by
  # pulsed coaxial electrodes powered by a capacitor bank. The driver is the capacitor
  # bank, costed under C220107. C220104 is not applicable.
  # Class U (per-unit).
  - account: C220104
    value: 0.0
    enabled: true
    provenance: direct
    source: "lerner-2023-jfe-paper.md §Experimental Device"
    rationale: |
      DPF driver is electrically driven (pulsed coaxial electrodes from capacitor bank).
      Per the canonical account schema, electrically-driven pulsed concepts cost the
      primary driver in C220107 (pulsed-power capacitor bank), not C220104 (which covers
      laser/accelerator/gun drivers). Setting C220104 to zero prevents double-counting.

  # C220107 — Pulsed-power capacitor bank ($/J stored)
  # The entire commercial generator (including capacitor bank, electrodes, vacuum vessel,
  # DEC, cooling, and controls) is claimed at <$1M for 5 MWe at mass production.
  # Capacitor bank is the dominant CAS22 sub-cost, estimated at ~40% of device cost.
  # Per-module cap bank cost implied: ~$400K = $0.40M absolute.
  # NOTE: the DENSE_PLASMA_FOCUS library archetype carries $0 for C220107 in its
  # default (bank cost may be routed through C220200 power conditioning). A relative
  # multiplier against a $0 base evaluates to $0 and loses the cost signal. This
  # override is therefore expressed as an absolute per-module value (Class U,
  # $0.40M/module), following the same approach as C220109.
  # Class U (per-unit).
  - account: C220107
    value: 0.40
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Commercialization; lerner-2023-jfe-paper.md §Experimental Device"
    rationale: |
      Lerner 2023 states the commercial generator "could be mass-produced and sold for
      less than $1 million" ($0.10/W capital, §Commercialization), covering all reactor
      island subsystems including the capacitor bank. The experimental device (FF-1) was
      built for ~$500K including a 115 kJ bank (§Experimental Device). Engineering judgment
      allocates ~40% of the $1M device cost to the capacitor bank = $0.40M per module
      (absolute). The DENSE_PLASMA_FOCUS archetype carries $0 for C220107 in the library
      default (driver cost may route through C220200), so a relative multiplier would
      evaluate to $0 and omit this cost entirely. Absolute value $0.40M/module ensures the
      capacitor bank is priced in the fleet model (200 modules × $0.40M = $80M fleet
      reactor-island contribution). Low confidence: the company's $1M figure is a
      paper-concept mass-production projection, not a demonstrated cost. Anchored to the
      library's 1 GWe modular-fleet default context (200 modules).

  # C220109 — Direct energy converter (electrostatic exhaust / inductive DEC)
  # DPF uses a two-channel DEC: (1) ion beam decelerator (~85% efficiency, ion beam
  # represents ~2/3 of fusion energy) and (2) x-ray photovoltaic converter (~80%
  # efficiency, x-rays ~1/3 of fusion energy). Both are integral to the device and
  # subsumed within the <$1M total device cost. Library default for this archetype
  # may not include DEC (thermal-cycle is the standard pulsed concept default).
  # Class U (per-unit).
  - account: C220109
    value: 0.15
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Energy Capture, Conversion to Electricity"
    rationale: |
      Ion beam decelerator (particle accelerator in reverse, ~85% efficiency for ~2/3
      of fusion energy) and x-ray photoelectric converter (multilayer metal foil,
      dimensions 40–50 cm inner radius × ~50 cm length, ~80% efficiency for ~1/3 of
      fusion energy) are both integral to the Focus Fusion generator. Lerner 2023
      includes both within the total device cost of <$1M per module. DEC is estimated at
      ~15% of total device cost = $150K per module ($0.15 M$). This is an absolute
      per-module value in M$. A 200-module 1 GWe fleet implies $30M total DEC capital
      — a modest cost consistent with the compact x-ray converter geometry. Anchored to
      the library's 1 GWe modular-fleet default for this account.

  # C220110 — Remote handling & maintenance equipment
  # Aneutronic fuel cycle means very low neutron activation of structural components.
  # Monthly electrode replacement is required (erosion-limited), but this is manual
  # contact maintenance, not remote handling. No hot cell needed. Remote handling
  # requirements are greatly reduced vs. D-T concepts.
  # Class U (per-unit).
  - account: C220110
    value: 0.10 * generic.cas22_detail["C220110"]
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Introduction; lppfusion-technology-focus-fusion-energy-dpf-device.md"
    rationale: |
      p-B11 primary reactions are aneutronic; secondary neutrons <1% of fusion energy.
      Structural components accumulate negligible neutron activation, requiring no hot
      cell and no high-rad-hardened remote handling equipment. Electrode replacement
      (design target: monthly) involves direct contact maintenance of small beryllium
      components (~kg scale) — standard industrial glove-box or light-booth procedures
      cover Be toxicity controls. Library's per-module remote handling default is sized
      for D-T neutron activation levels; 10% of that default covers the reduced
      requirements here. Anchored to the library's 1 GWe modular-fleet default.

  # CAS23 — Turbine plant equipment
  # Direct energy conversion (no thermal cycle). Zero turbine capital.
  # Class P (power-proportional).
  - account: CAS23
    value: 0.0
    enabled: true
    provenance: direct
    source: "lerner-2023-jfe-paper.md §Energy Capture; lppfusion-investing-in-lppfusion-executive-summary.md §Energy Conversion"
    rationale: |
      All fusion energy is captured via direct energy conversion: ion beam decelerator
      (charged particles) and x-ray photovoltaic converter (x-rays). No thermal blanket,
      no steam generator, no turbine, no condenser. LPPFusion explicitly states the device
      converts energy "without going through heat and steam." Turbine plant capital is
      zero for the Focus Fusion design point. This is an architectural certainty, not a
      modeling assumption.

  # CAS26 — Heat rejection system
  # Direct conversion at ~83% blended efficiency means ~17% of fusion energy becomes
  # waste heat. At 5 MWe net output and ~6 MW total fusion power per module, waste
  # heat ≈ 1 MW per module vs. ~16 MW for a 33%-efficient thermal plant of similar
  # gross power. Heat rejection capacity needed is roughly 15–20% of a thermal-cycle
  # plant of equivalent net output.
  # Class P (power-proportional).
  - account: CAS26
    value: 0.18 * generic.costs.cas26
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Energy Capture"
    rationale: |
      Ion beam DEC efficiency ~85% (§Energy Capture) and x-ray photovoltaic efficiency
      ~80%, blending to ~83% overall DEC efficiency ([inferred: 2/3 × 85% + 1/3 × 80%]).
      Total waste heat fraction ≈ 17% of fusion output plus electrode cooling (~1 MW per
      module for anode tip cooling at 10 kW/cm²). Total heat rejection per module at
      commercial scale ≈ 2 MW, compared to ~14 MW for a 33%-efficient thermal plant at
      equivalent gross output (Q_thermal ≈ 6 MW fusion). Ratio ≈ 14% + margin → override
      at 0.18× the library's fleet default, reflecting the large heat rejection reduction
      from direct conversion. Anchored to the library's 1 GWe modular-fleet default.

  # CAS27 — Special materials (initial reactor material inventory / blanket fill)
  # No tritium startup inventory. No breeding material (FLiBe, Li-6 ceramics). The only
  # first-fill special material is the decaborane fuel charge (93 g scale; cost negligible)
  # and the initial beryllium electrode set for 200 modules.
  # Class P (power-proportional).
  - account: CAS27
    value: 0.02 * generic.costs.cas27
    enabled: true
    provenance: derived
    source: "lerner-2023-jfe-paper.md §Fuel; lerner-2024-frontiers-pB11-prep.md §Fuel Preparations"
    rationale: |
      D-T concepts must acquire kg-scale tritium at ~$30k/g for startup inventory —
      the dominant CAS27 cost. DPF with p-B11 fuel has no tritium and no breeding
      blanket fill material. Initial decaborane inventory is gram-scale (LPPFusion
      received 93 g of isotopically pure decaborane, §Fuel Preparations), cost
      negligible. Initial beryllium electrode set for 200 modules: ~200 × small Be
      cylinder, rough cost <$1M at $800/kg. Override at 2% of library fleet default
      accounts for initial electrode material inventory only. Anchored to the library's
      1 GWe fleet default.
```

**Override count: 7 enabled overrides.** Target band for Low archetype-fit is 6–12. Count is within band. (Reduced from 9: C220101 and C220102 removed because the DENSE_PLASMA_FOCUS library archetype already carries $0 for both accounts — relative multipliers against a $0 base add no cost signal. C220107 changed from relative to absolute $0.40M/module to prevent the same vacuousness, since the library also carries $0 there.)

**LCOE interpretation note.** The overrides-on run produces a very low LCOE (~13 $/MWh) driven entirely by the company's unverified $1M/module mass-production claim. This is an optimistic lower bound, contingent on: (a) the $1M figure being realised at NOAK scale, (b) QMFE-suppressed bremsstrahlung holding at commercial conditions (unvalidated), and (c) p-B11 net energy being demonstrated (not yet attempted). The library-default run (overrides off) prints the upper bracket (~557 $/MWh). Both numbers should be presented together in any cross-concept comparison — the 13 $/MWh headline in isolation is not credible given the concept's technology status.

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | QMFE bremsstrahlung suppression unvalidated — the entire p-B11 commercial physics basis rests on this unconfirmed effect | S2, S3 | truly-unknown | blocking | Independent theoretical review; direct experimental measurement of bremsstrahlung vs. fusion power in DPF plasmas with strong self-fields |
| 2 | No demonstrated p-B11 fusion yield — all experimental results are with deuterium; FF-2B pB11 shots not yet attempted | S2, S3 | truly-unknown | blocking | LPPFusion's Phase 1 experimental results when published |
| 3 | Filament disruption mechanism above 1 MA unresolved — blocks yield improvement since 2016 | S2, S3 | truly-unknown | blocking | LPPFusion switch redesign results; independent DPF physics analysis |
| 4 | Device cost breakdown by subsystem unpublished — $1M claim covers all components; cannot allocate to CAS22 sub-accounts independently | S1, S5b | proprietary | blocking | Company cost model disclosure; analogous industrial capacitor bank pricing surveys |
| 5 | 200 Hz rep rate undemonstrated at fusion-class energies — electrode cooling, switch recovery, bank cycling all need experimental validation | S2, S3 | truly-unknown | blocking | Rep-rate demonstrations on FF-2B or successor device |
| 6 | Ion beam decelerator efficiency undemonstrated — ~85% calculated but no prototype at fusion-relevant ion energies | S3, S5 | truly-unknown | important | DEC prototype test results; analogue: FRC/mirror direct-energy-converter literature |
| 7 | X-ray photovoltaic efficiency undemonstrated — ~80% calculated; multi-layer foil concept has no known prototype | S3, S5 | truly-unknown | important | Photoelectric x-ray converter prototype experiments; solar-cell/photodiode analogue data |
| 8 | Fusion yield per shot for commercial design — 60 kJ target is a design requirement, not experimentally grounded | S5 | truly-unknown | blocking | Experimental fusion yield scaling data; validated simulation results |
| 9 | Capacitor bank stored energy for commercial generator — 115 kJ measured on FF-1/FF-2B; commercial design may use different bank to achieve 200 Hz cycling | S5 | not-yet-sourced | important | LPPFusion commercial generator design documents |
| 10 | Energy split between ion beam and x-rays — the 2/3 ion / 1/3 x-ray assumption used in Section 5 is estimated; actual split affects blended DEC efficiency | S5, S5b | derivable | important | Full energy accounting from FF-2B shot diagnostics |
| 11 | Beryllium electrode erosion rate at 200 Hz — determines replacement frequency and annual beryllium consumption for supply chain sizing | S4 | not-yet-sourced | important | High-rep-rate electrode erosion experiments |
| 12 | Diamond switch supply chain and cost at scale — proposed for DEC ion beam circuit; no commercial supply for this application exists | S4 | truly-unknown | nice-to-have | Industrial diamond PCSS production capacity surveys |

---

## Section 7: Family-Delta vs Comparables

No comparable concept in the corpus for this design point.

The DPF falls outside the standard fusion concept families. For context, the structural differences from the nearest analogues in the corpus are noted below; these are not formal comparables and are offered as orientation only.

**Vs. pulsed electrically-driven concepts (MagLIF / Pacific Fusion):** DPF and MagLIF share a capacitor-bank driver and a pulsed electromagnetic compression mechanism, but differ fundamentally in scale, fuel, and energy conversion. MagLIF operates at 20–60 MA with GJ-class yields in a large chamber; DPF operates at ~2.7 MA with ~60 kJ target yields in a device that fits in a small room. MagLIF uses D-T fuel with a tritium-breeding blanket and thermal energy conversion; DPF uses p-B11 with no blanket and direct energy conversion. MagLIF's dominant cost is the pulsed power driver at GJ stored energy; DPF's capacitor bank stores ~115 kJ — six orders of magnitude less energy. The economics are structurally different: MagLIF's LCOE challenge is driver cost and rep rate at very large scale; DPF's challenge is demonstrating net fusion energy at all.

**Vs. other direct-conversion concepts (Helion FRC):** Both DPF and Helion use direct energy conversion and claim high electrical efficiency. Helion's inductive DEC recovers ~90% of stored magnetic energy. DPF's ion beam decelerator claims ~85% at full chain. DPF avoids Helion's He-3 supply challenge (uses abundant protons and boron) but faces a deeper physics proof gap: Helion has demonstrated >100 million degree plasma temperatures and D-T fusion; DPF has not yet demonstrated p-B11 fusion conditions with QMFE suppression active.

**Vs. laser IFE concepts (HB11, Xcimer):** HB11 and Xcimer also target p-B11 with laser drivers. HB11 achieved p-B11 fusion with laser acceleration but at efficiencies far below what is commercially needed. LPPFusion's DPF claims higher fusion yield per input joule than laser approaches for p-B11 (Lerner 2023 cites ~300× better efficiency than HB11's laser results). The capital cost structures differ radically: laser facilities require $100M+ optical systems, while DPF's capacitor bank costs ~$1M total for the entire device. But both face the same fundamental p-B11 net-energy physics challenge.

---

## Section 8: Sources

1. **Lerner, E. J. et al. (2023).** "Focus Fusion: Overview of Progress Towards p-B11 Fusion with the Dense Plasma Focus." *Journal of Fusion Energy* 42:7. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2023-jfe-paper.md` (77 KB). **Primary source** for experimental results, device specifications, commercial generator design point, and cost projections. Authored by LPPFusion personnel.

2. **Lerner, E. J. et al. (2024).** "Preparations for pB11 tests in the FF-2B dense plasma focus." *Frontiers in Physics*. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2024-frontiers-pB11-prep.md` (25 KB). Most recent peer-reviewed paper; describes FF-2B device parameters (anode 2.8 cm radius, 2.7 MA target), experimental status, and planned p-B11 test sequence. Authored by LPPFusion personnel.

3. **LPPFusion, "Investing in LPPFusion: Our Plan to Net Energy."** Company investor document. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md` (6 KB). Commercial roadmap; 5 MW generator target, $100M Phase 2 budget, 3–4 year timeline. Promotional in nature.

4. **LPPFusion, "Investing in LPPFusion: Executive Summary."** Company investor document. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-executive-summary.md` (6 KB). Top-level claims for aneutronic advantage, device simplicity, and energy conversion approach.

5. **LPPFusion, "Technology: Focus Fusion Energy / DPF Device."** Company website pages. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lppfusion-website-technology.md` and `iter-02/sources/lppfusion-technology-focus-fusion-energy-dpf-device.md`. Company description of device operation, direct energy conversion, and economic claims. No quantitative data beyond what appears in the peer-reviewed papers.

6. **LPPFusion, "Proton-Boron (pB11) Fuel Arrives."** Company news post. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-proton-boron-p11b-fuel-arrives.md` (1 KB). Confirms receipt of 93 g of isotopically pure decaborane for pB11 experiments.

7. **Compound Semiconductor / IPO articles on diamond PCSS.** Saved: `iter-02/sources/compoundsemiconductor-119149-us-team-reinvents-the.md` and `iter-02/sources/ipo-ipo-technologies-instruments-sensors-and-electronics.md`. These articles cover diamond photoconductive semiconductor switches (PCSS) used in power grid protection — the underlying switching technology proposed for DPF's ion beam DEC circuit. They do not reference LPPFusion directly but characterize the TRL and performance (TRL 3, ~20% efficiency, 44 A/cm² demonstrated) of diamond PCSS switches relevant to DEC feasibility.
