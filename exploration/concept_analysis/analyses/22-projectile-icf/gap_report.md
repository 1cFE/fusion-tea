Now I have everything I need. Let me write the assessment.

---

# Gap Assessment: Projectile ICF (D-T)

## Overall Readiness
**Rating**: Mostly Ready (with important caveats)
**Summary**: First Light Fusion's extensive public disclosures provide enough architecture, performance targets, and cost anchors for a credible qualitative analysis and first-pass LCOE model. However, this concept has a fundamental structural problem: it has no active commercial pursuer (First Light pivoted to FLARE in Sept 2025; NearStar is properly MIF, not projectile ICF). The qualitative write-up must lead with this context. Quantitative modeling is feasible but will be heavily assumption-driven — subsystem cost breakdown data is absent, driver efficiency is unpublished, and the claimed gain (200–1000×) has never been demonstrated, creating compounding physics-to-cost uncertainty.

---

## Section Coverage

### 1. Availability of Data
**Coverage**: Moderate

**Available**:
- First Light Fusion published a substantial body of technical and commercial detail between 2011–2025, captured across all four source documents. This includes power plant architecture, TBR data (independently validated), cost targets, rep rate ranges, plant size targets, and the strategic pivot narrative.
- First Light stated LCOE target (<$50/MWh), pilot plant cost target (<$1B for 150 MWe), and commercial plant cost (<$5B for ~500 MWe) — rare top-line cost disclosures for a fusion startup (`first-light-fusion-technology.md`).
- TBR 1.8 was independently verified by TÜV SÜD UK (Feb 2026), giving the tritium breeding claim unusual credibility.
- NearStar's public disclosures are thinner but captured (`nearstar-fusion-technology.md`, `nearstar-fusion-2025-update.md`): driver specs, fuel preference, modularity pitch, and funding stage.

**Missing**:
- Peer-reviewed publications on projectile ICF gain physics (First Light published some target physics work; these are not captured in Phase 1a sources)
- Any independent plant study or system code output for the projectile ICF concept
- Published techno-economic analysis from any third party

**Gaps**:
- Peer-reviewed target physics papers — `not-yet-sourced` — important (would constrain gain credibility)
- Independent TEA or LCOE study — `truly-unknown` — nice-to-have (unlikely to exist; concept is abandoned)
- Active commercial development data post-pivot — `truly-unknown` — blocking for near-term commercial projections (concept is orphaned)

---

### 2. Challenges in Capturing System Function
**Coverage**: Partial

**Available**:
- The system architecture is well described: EM gun driver → hypervelocity projectile → proprietary amplifier target → D-T implosion → liquid Li neutron absorption/tritium breeding → steam Rankine BOP. This chain is sufficient to structure an LCOE model.
- The gain requirement (200–1000×) is stated and its commercial significance explained.
- The "decoupled" nature of driver and BOP is clearly articulated: "after the lithium heat exchanger, the plant is identical to many other already working facilities."
- The abandonment of Machine 4 (which would have been the gain-demonstration machine at 60 km/s / 100 MJ) is documented — this is the key physics gap that killed the concept.

**Missing**:
- Driver wall-plug efficiency: how much grid electricity is consumed per shot to accelerate the projectile? Not disclosed anywhere in the sources.
- Recirculating power fraction: closely related to driver efficiency; absent.
- Fusion-energy-to-driver-energy coupling path: what fraction of fusion yield is captured vs. lost?
- Target physics credibility: the "amplifier" that converts 6.5 km/s projectile to >70 km/s internal fuel velocity is entirely proprietary. The physics of this gain mechanism is the central uncertainty and not described in enough detail to evaluate.
- Demonstrated Q: First Light achieved fusion (neutrons detected) but never Q>1. The gap between Q<0.001 (demonstrated) and Q=200–1000 (commercial claim) is enormous and unvalidated.

**Gaps**:
- Driver wall-plug efficiency — `proprietary` — **blocking** for LCOE model (determines recirculating power; must be assumed)
- Target amplifier physics detail — `proprietary` — **blocking** for gain credibility assessment (must use stated range with large uncertainty)
- Demonstrated Q or credible Q roadmap — `not-yet-sourced` / `truly-unknown` — **blocking** (search for any First Light arxiv papers on target compression physics; `unverified — confirm existence before searching`)
- Recirculating power fraction — `derivable` — important (can be estimated from gain × driver efficiency with stated assumptions)

---

### 3. Maturity of Key Subsystems and Components
**Coverage**: Partial

**Available from sources**:
- **EM launcher (driver)**: TRL 4–5. Machine 3 demonstrated 6.5 km/s. Machine 4 (targeting 60 km/s, commercially relevant) was cancelled before construction. The 10× velocity gap is the unresolved engineering challenge.
- **Target / amplifier**: TRL 3–4. Fusion demonstrated (UKAEA validated, 2022). Gain demonstrated at what NIF calls record is ~4×; First Light needs 200–1000×. This is the biggest TRL gap in the entire concept.
- **Liquid lithium blanket/breeding**: TRL 3–4. Design is detailed, TBR independently validated, but not built at any scale. Liquid metal handling at this scale is a known engineering challenge shared with other IFE/MFE concepts.
- **Tritium handling systems**: TRL 5–6 (via ITER and fission industry experience, applicable here).
- **Steam Rankine BOP**: TRL 9. Mature commercial technology; sources confirm "identical to many other already working facilities."

**Missing**:
- TRL breakdown explicitly stated for any subsystem (these are inferred from source descriptions)
- Any Materials and Components Readiness Level (McRL) assessment
- Target fabrication at repetition rate (even sub-Hz): how are the ~1 cm cubic targets with multi-cavity proprietary amplifier structure manufactured at commercial scale? Not addressed in any source.

**Gaps**:
- Target fabrication at commercial rep rate — `proprietary` — **blocking** (no information on target manufacturing process, cost, or scalability)
- EM driver scaling pathway (6.5 → 60 km/s) — `not-yet-sourced` / `truly-unknown` — **blocking** (Machine 4 was cancelled; this problem is unresolved)
- Liquid Li system engineering challenges at scale — `not-yet-sourced` — important (search MHD pump literature, fission Li-cooled reactor experience; `unverified — confirm existence before searching`)

---

### 4. Key Materials and Supply Chain Considerations
**Coverage**: Partial

**Available**:
- **Lithium**: Liquid lithium is the primary blanket/breeding material. Large volumetric quantity needed (1-meter-thick flowing curtains). Li-6 enrichment needed for TBR optimization (though TBR 1.8 may allow natural lithium; not specified in sources).
- **Tritium startup inventory**: D-T fuel requires initial tritium purchase before plant achieves self-sufficiency. At 333 MWe with 25 kg/yr net surplus, startup inventory requirements are non-trivial. Sources state self-sufficiency achievable "in as little as one week" which seems physically unrealistic and may reflect a misstatement.
- **Target materials**: The "amplifier" target is cubic, ~1 cm, proprietary multi-cavity design. Materials not specified. Standard IFE targets use beryllium, diamond, or plastic ablators — none of these are explicitly mentioned.
- **Conventional BOP**: No exotic materials in the steam Rankine cycle.

**Missing**:
- Target material composition (entirely proprietary)
- Li-6 enrichment fraction required
- Annual target production volume (shots/year at 0.033 Hz ≈ ~1M shots/year for 333 MWe — this is the scale question)
- Tritium startup inventory quantification

**Gaps**:
- Target material composition — `proprietary` — **important** (could affect cost significantly; must use analogue from NIF/hohlraum targets)
- Target production volume and manufacturing process — `proprietary` — **blocking** for operating cost model (target cost/shot is often the dominant IFE operating cost)
- Li-6 enrichment requirements and supply chain — `not-yet-sourced` — important (search ORNL or DOE Li isotope separation literature)
- Tritium startup inventory — `derivable` — important (can be estimated from D-T burn rate at target Q and rep rate)

---

### 5. LCOE Parameter Extraction
**Coverage**: Partial

**Available Parameters**:

| Parameter | Value/Range | Source | Confidence |
|---|---|---|---|
| Plant electrical output (pilot) | ~150 MWe | first-light-fusion-technology.md | m |
| Plant electrical output (commercial) | ~333–500 MWe | first-light-fusion-technology.md | m |
| Total capital cost (pilot) | <$1B | first-light-fusion-technology.md | l (company target) |
| Total capital cost (commercial) | <$5B | first-light-fusion-technology.md | l (company target) |
| LCOE target | <$50/MWh | first-light-fusion-technology.md | l (company target) |
| Claimed fusion gain | 200–1000× | first-light-fusion-technology.md | l (undemonstrated) |
| Rep rate | 0.011–0.1 Hz (sub-Hz) | dossier.md | m |
| Energy conversion pathway | Steam Rankine cycle | first-light-fusion-technology.md | h |
| Thermal efficiency (steam Rankine) | ~33–38% | derivable from standard steam cycle | m (analogue) |
| TBR | 1.8 | first-light-flare-pivot-update.md | h (independently validated) |
| Net tritium surplus | 25 kg/yr at 333 MWe | first-light-fusion-technology.md | m |
| Vessel replacement schedule | Lifetime-of-plant | first-light-fusion-technology.md | m (unvalidated claim) |
| Driver cost per joule (FLARE, not projectile) | $2/J | first-light-flare-pivot-update.md | l (FLARE, not applicable directly) |
| Demonstrator cost (FLARE) | $100–200M | first-light-flare-pivot-update.md | l (FLARE, not projectile) |

**Missing Parameters**:

| Parameter | Gap Type | Criticality | Notes |
|---|---|---|---|
| Capital cost by subsystem (CAS breakdown) | proprietary | blocking | Only total cost targets stated; no subsystem breakdown |
| Driver (EM gun) capital cost | proprietary | blocking | No figure for the projectile driver specifically |
| Target cost per shot | proprietary | blocking | Most sensitive IFE operating cost; entirely unknown |
| Annual target production volume | derivable | blocking | Derivable from rep rate × hours/year |
| Driver wall-plug efficiency | proprietary | blocking | Determines recirculating power fraction |
| Recirculating power (gross→net) | derivable | blocking | Need driver efficiency first; else must assume |
| Capacity factor / availability | not-yet-sourced | important | Not stated; pulsed IFE analogues could inform |
| Q (target fusion gain, demonstrated) | truly-unknown | blocking | Machine 3 achieved Q<<1; commercial needs 200–1000× |
| D-T fuel cost (pre-self-sufficiency) | derivable | important | Tritium spot market ~$30k/g; derivable from burn rate |
| O&M cost (non-fuel) | not-yet-sourced | important | No data; could use IFE plant study analogues |
| Blanket/Li loop capital cost | not-yet-sourced | important | Analogues available from other liquid-metal blanket designs |
| Thermal conversion efficiency (actual) | derivable | important | Steam Rankine ~33–38%; can be assumed with note |
| First wall replacement cost | not applicable | — | Liquid Li blanket eliminates this cost item |
| EM driver maintenance/replacement | truly-unknown | important | No data on EM launcher maintenance at commercial scale |

---

## Source Recommendations

1. **First Light Fusion arxiv/journal publications** on target physics and compression gain — `not-yet-sourced` — search arxiv for "First Light Fusion" or "projectile inertial confinement"; may include peer-reviewed work on amplifier target physics. `unverified — confirm existence before searching`

2. **IFE plant studies (laser ICF analogues)** for capital cost structure and target cost — `not-yet-sourced` — the SOMBRERO, HYLIFE-II, or Prometheus-L plant studies from the 1990s contain CAS-level cost breakdowns for IFE concepts that can serve as structural analogues. These are in OSTI. Available via OSTI/DOE.

3. **Electrothermal / electromagnetic launcher literature** for driver cost and efficiency — `not-yet-sourced` — railgun and coilgun cost-per-joule literature from DoD/DARPA programs could inform EM driver capital and wall-plug efficiency. Search DTIC or IEEE for "electromagnetic launcher efficiency commercial."  `unverified — confirm existence before searching`

4. **Liquid lithium loop engineering literature** for blanket capital cost — `not-yet-sourced` — ITER liquid metal blanket module cost estimates, or fission Li-cooled reactor (MSRE, FFTF) O&M analogues. Search IAEA or ORNL reports.

5. **IFE target cost studies** — `not-yet-sourced` — DOE has funded IFE target fabrication cost studies (especially for NIF/laser ICF); these could anchor target cost/shot estimates even if the amplifier geometry differs. Search OSTI for "IFE target fabrication cost." `unverified — confirm existence before searching`

6. **NearStar Fusion 2025 concept paper** — `not-yet-sourced` — sources indicate NearStar planned to publish experimental results and a detailed concept paper in 2025. If published, it may contain driver specs and power plant economics. Search for NearStar Fusion publications or SBIR final report.

---

## Summary

**Proceed to full analysis with stated limitations.** The available data from First Light Fusion's public disclosures is sufficient to produce a credible qualitative write-up and a first-pass LCOE model — but both require explicit acknowledgment of the concept's unusual status: it is analytically interesting but commercially orphaned. The qualitative write-up should open with this context prominently.

For the quantitative model, the following assumptions will need to be stated explicitly due to data gaps:
- **Driver efficiency**: assume 10–30% (electromagnetic gun wall-plug efficiency range from analogues) — this is a high-leverage uncertain parameter
- **Target cost/shot**: assume $10–$1,000 (spanning laser IFE target analogues to speculative amplifier manufacturing) — this is likely the dominant operating cost uncertainty
- **Capital cost structure**: use SOMBRERO/HYLIFE-II IFE plant study ratios as structural analogues, scaled to First Light's total cost targets
- **Fusion gain**: use First Light's claimed 200–1000× range as a parameter sweep input; note no gain has been demonstrated

The back-solve to $0.01/kWh will need to clearly flag that the binding constraint (target gain ≥200×) has never been demonstrated at any scale, and that even the $50/MWh company target appears optimistic given the absence of a credible path to Machine 4's velocity requirement.
