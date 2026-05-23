# Phase 3 diff: 05-planar-coil-stellarator

**Generated:** 2026-05-22T13:28:23-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 3 | 1 | -2 |
| important_count  | 8 | 6 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
(none — good)
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have all the material needed to write the full assessment. Here is the report:
```

## Blocking-tier lines (new)

```
114:| CAS-level capital cost estimates (any subsystem) | derivable | blocking | Zero cost data in concept-scoped sources; must build bottom-up from geometry + material costs using TEA/ARIES framework; wide uncertainty expected |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/05-planar-coil-stellarator.md	2026-05-22 12:59:21.059228928 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/05-planar-coil-stellarator/gap_report.md	2026-05-22 13:28:23.520402219 -0700
@@ -1,185 +1,163 @@
-I now have sufficient data to write the gap assessment. Let me compile the report.
-
----
+I now have all the material needed to write the full assessment. Here is the report:
 
 # Gap Assessment: Planar Coil Stellarator (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: The Helios preconceptual design paper (arXiv:2512.08027, ~200 pages, DOE Milestone-certified January 2026) provides exceptional technical depth for a private-sector fusion concept at this stage. Physics performance, engineering architecture, materials, maintenance scheme, and power flows are comprehensively documented with full confidence. The critical gap is cost: the public paper includes no CAS-level capital cost breakdown, no O&M dollar estimates, and no detailed LCOE derivation — only high-level targets ($150/MWh → $60/MWh at scale) that appear in the dossier without a traceable citation. Fleet-wide analogs (TEA D-T MFE, ARIES cost accounts) can partially fill this gap, but quantitative cost estimates for this concept will require either accessing the full DOE Milestone report or using scaled analogs from ARIES-CS.
-
----
+**Summary**: Thea Energy's Helios preconceptual design (arXiv:2512.08027, DOE Milestone-certified January 2026) is one of the most thoroughly documented private fusion concepts in the public domain. Physics, engineering, and system-level performance parameters are available at exceptional detail for a preconceptual design. The primary gap for a quantitative LCOE model is the complete absence of capital cost estimates from any concept-scoped source — subsystem costs must be derived from geometry, material specifications, and fleet-wide analogs. All qualitative sections (1–4) can be executed with high confidence; the quantitative LCOE model (§5) will require a full bottom-up construction from available data.
 
 ## Section Coverage
 
 ### 1. Availability of Data
 **Coverage**: Good
 
-**Available**:
-- Full preconceptual design report as arXiv preprint (arXiv:2512.08027), submitted to *Fusion Engineering and Design*, DOE Milestone-certified January 13, 2026. Covers all major subsystems with engineering-level detail.
-- 4 peer-reviewed companion papers in *Nuclear Fusion* (Jan 2025) covering coil optimization methods, Eos plasma physics, fast ion confinement, and the stellarator systems architecture.
-- Canis prototype paper (arXiv:2503.18960) confirming REBCO HTS manufacturing process and field-shaping control.
-- DOE Milestone program certification press release with independent expert review statement.
-- ANS news article and Thea press releases confirming design milestones and roadmap.
-
-**Missing**:
-- Full 200-page DOE Milestone report (referenced but not public; contains more system-level detail than the arXiv overview paper).
-- Detailed LCOE / TEA companion study (not published; Thea mentions discussions with "power offtakers and hyperscalers" suggesting internal cost models exist).
-- 4 Nuclear Fusion companion papers on specific components — not individually fetched in Phase 1a.
+**Available**: The Helios overview paper (arXiv:2512.08027, ~200 pages, submitted to Fusion Engineering and Design) provides a complete preconceptual design reviewed and certified by a DOE expert panel in January 2026. This is backed by 14 companion papers submitted concurrently to the same journal covering each subsystem in detail. Four earlier Nuclear Fusion papers (January 2025) document the planar coil stellarator architecture foundation. The Canis prototype paper (arXiv:2503.18960) provides direct experimental demonstration of HTS planar shaping coil arrays. Company website and press releases fill context on the development roadmap. All core physics and engineering parameters are stated explicitly, with high-fidelity simulation results (ASCOT5, GENE/T3D, M3D-C1, OpenMC) substantiating the design assumptions.
 
-**Gaps**:
-- Full DOE Milestone report content — `proprietary` — **nice-to-have** (the arXiv paper captures the key engineering parameters; additional detail would improve fidelity)
-- Quantitative cost model or LCOE derivation — `proprietary` — **blocking** (LCOE section requires this)
+**Missing**: Thea Energy has not published any capital cost estimates, construction cost projections, or detailed LCOE calculations. The 200-page DOE report is not publicly available; only the overview arxiv paper has been released. Eos design details are covered in the four Nuclear Fusion papers (referenced, not individually fetched). No supply chain analysis has been published.
 
----
+**Gaps**:
+- No capital cost estimates published for any Helios subsystem — derivable — blocking (for §5 quantitative model)
+- Eos design details (Nuclear Fusion, Jan 2025) not individually fetched — not-yet-sourced — nice-to-have
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Good
 
-**Available**:
-- Novel planar coil stellarator architecture well-documented: 12 encircling + 324 shaping coils, software-controlled with 450+ independent variables. The "hardware-to-software complexity transfer" is the primary architectural innovation.
-- QA stellarator equilibrium physics: ISS04 transport scaling with H_ISS04 = 1.4 (verified by GENE/Trinity gyrokinetic simulations), MHD stability via TERPSICHORE and M3D-C1, energetic particle confinement via ASCOT5 (6.6% alpha loss to wall).
-- Novel X-point divertor for a stellarator: first-of-kind tokamak-like X-point in a stellarator power plant design; physics basis documented.
-- Bootstrap current management: 2/3 of rotational transform from bootstrap current — controlled via individually-addressable shaping coils.
-- Startup scenario: POPCON analysis, 2-hour startup, 10 MW ECRH → ignition at <1 MW.
-- Power balance: 958 MW fusion → 1,094 MW thermal → 438 MWe gross → 390 MWe net; recirculating power <3%.
-
-**Missing**:
-- Experimental validation of the X-point divertor in a stellarator plasma (Eos must demonstrate this first).
-- Experimental validation of closed-loop control at Eos scale with dozens of coils (Canis only demonstrated 9 coils).
-- Bootstrap current steady-state control over operational timescales (hours to days).
+**Available**: The Helios paper is unusually self-aware about its own limitations. Key modeling challenges are directly discussed: (1) the software-defined field control system (450+ independent coil variables) is explicitly noted to have 450+ control variables with no precedent in prior stellarators; (2) the novel X-point divertor is flagged explicitly as requiring "additional consideration" for heat flux management at power scale (§3.7: "some combination of radiative impurity seeding, or detachment... [is required]"); (3) alpha particle loss at 6.6% to the first wall is noted as higher than academic literature and is an area of ongoing optimization; (4) the ISS04 confinement enhancement factor H=1.4 (based on W7-X QI data) is used for a QA equilibrium, acknowledged as an extrapolation — the paper validates this with gyrokinetic calculations and finds H=1.33 self-consistently; (5) V-4Cr-4Ti is used as first wall material for its 15 full-power year lifetime, but with "significant uncertainties with respect to suitability of materials for fusion environments" (§4.2); (6) D-T ice pellet fueling with mixed isotopes is noted as demonstrated only for single-isotope species in limited-duration discharges.
 
-**Gaps**:
-- X-point divertor in stellarator — no experimental precedent — `truly-unknown` at Helios scale — **important** (the design is modeled but undemonstrated; adds uncertainty to plasma-wall interaction modeling and heat load estimates)
-- Confinement enhancement H_ISS04 = 1.4 in QA configuration — `not-yet-sourced` (W7-X is QI, not QA; QA at this parameter is extrapolated) — **important** (affects fusion power and thus LCOE sensitively)
-- Software-defined stellarator field control at scale — `truly-unknown` (Canis proved principle; Eos-scale has 50+ coils; Helios has 324) — **nice-to-have** (risk flag for cost estimation uncertainty)
+**Missing**: The cost modeling implications of the software control stack (450+ variables, GPU/FPGA control architecture) are not assessed — this is a novel O&M complexity driver with no analog. Heat management of 4 MW/m² peak alpha-particle heat flux is flagged but not resolved.
 
----
+**Gaps**:
+- Software control system O&M complexity — truly-unknown — important (no analog for 324-coil independent control system at commercial scale)
+- Mixed D-T pellet fueling system at steady-state power scale — not-yet-sourced — important
+- Novel X-point divertor power handling validation — truly-unknown — important (first stellarator to claim this topology; no experimental validation at power plant scale)
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **HTS coil system (encircling)**: TRL 4–5. REBCO at 20 T, 20 K demonstrated in large-bore magnets (MIT SPARC TFMC). Planar encircling coil design documented with FEA stress analysis. 40-year lifetime modeled.
-- **HTS shaping coils**: TRL 3–4. Canis (2025) demonstrated 9-coil REBCO array with closed-loop field control to <1% RMS error at 20 K. Manufacturing process (soldered metal insulation, ≤1 day/DP takt time) validated.
-- **Tritium breeding blanket (LiPb)**: TRL 4. LiPb blanket design well-documented: 50 cm thick, Pb-17Li, 65% Li-6 enrichment, EUROFER97 structure, SiC MHD inserts, He-cooled. TBR = 1.3 (idealized). No full-scale LiPb blanket module tested yet; HCLL designs from EU DEMO program are comparable.
-- **Vanadium first wall (V-4Cr-4Ti)**: TRL 4. Choice justified by 15-year neutron survival time. Referenced against prior fusion materials research. Not used in current operating devices.
-- **Thermal cycle (steam Rankine)**: TRL 9. 635°C superheated steam, three-stage turbines, 40.2% efficiency. Fully mature industrial technology.
-- **ECRH (startup heating)**: TRL 7. ITER-spec 170 GHz gyrotrons at 10 MW for startup; mature technology.
-- **Sector-based maintenance**: TRL 2–3. Architecture is designed and analyzed (84 days per 2-year cycle), but no stellarator has implemented this maintenance scheme. Novelty is a key cost and schedule uncertainty.
-- **X-point divertor for stellarator**: TRL 2–3. Documented in design, modeled in simulation, but no experimental precedent.
-
-**Missing**:
-- TRL assessments are inferred from context; Helios paper doesn't present a formal TRL matrix.
-- No published test data for V-4Cr-4Ti under D-T neutron fluence at scale.
-- No demonstrated sector-based maintenance at any prototype.
+**Available**: The Helios paper provides explicit TRL-relevant descriptions for each subsystem:
+- **REBCO HTS magnets (encircling)**: TRL 4–5 — comparable to SPARC TFMC/CSMC demonstrated in large-bore coils at 20 T (cited in Canis paper §I). The planar winding approach is simpler than NoT cable architectures.
+- **REBCO HTS planar shaping coils**: TRL 4 — the Canis 3×3 array (9 coils) was successfully operated at 20 K with closed-loop field control to <1% RMS error at 20 K (arXiv:2503.18960). Manufacturing at ≤1 day per double-pancake takt time demonstrated. Scaling to 324 coils is not demonstrated.
+- **QA stellarator plasma physics**: TRL 5 — W7-X has demonstrated H_ISS04=1.4 and the physics basis is mature for QI configurations. QA specific to Thea/Eos architecture remains to be plasma-tested; physics is analyzed at high fidelity computationally.
+- **Novel X-point divertor**: TRL 2 — "first time to our knowledge that a stellarator equilibrium has explicitly been designed to include such a divertor" (§3.7). Modeled with FLARE code; no experimental validation.
+- **LiPb tritium breeding blanket**: TRL 4 — ARIES-CS, EU-DEMO, Stellaris heritage. Helios design uses 50 cm thick Pb-17Li with 65% Li-6 enrichment, EUROFER97 structure, SiC/SiC inserts, He gas coolant.
+- **V-4Cr-4Ti first wall**: TRL 3–4 — irradiation data exist from fission sources; 15 full-power year lifetime is extrapolated. Paper explicitly cites "immature supply chain."
+- **ECRH / 170 GHz gyrotrons**: TRL 8 — ITER-specification gyrotrons. Standard technology.
+- **Steam Rankine cycle (635°C, 3 turbines)**: TRL 9 — conventional thermal plant technology.
+- **Tritium fuel cycle**: TRL 4 — modeled with TMAP8 using ITER-based assumptions; "estimates are likely of the correct order of magnitude for present technology."
+- **Sector-based remote maintenance**: TRL 3 — conceptual design with hardware-informed constraints; no full-scale demonstration.
+- **Field-shaping units (FSUs)**: TRL 3 — grouping of shaping coils with integrated services; Canis demonstrates coil but not FSU assembly.
+- **Cryogenic system**: TRL 7 — expander cycle at 10 MW electrical, 40 kW cold mass load; based on established industrial equipment.
 
-**Gaps**:
-- Formal TRL matrix for all subsystems — `not-yet-sourced` (Thea's DOE Milestone report may contain this) — **important**
-- V-4Cr-4Ti neutron irradiation qualification at target fluence — `truly-unknown` — **important** (could force first-wall lifetime revision; 15-year lifetime is a key assumption)
-- Sector maintenance at any scale — `truly-unknown` — **nice-to-have** (risk factor, not cost-blocking)
+**Missing**: TRL assessments for the field-control software stack (650+ coil current channels with GPU/FPGA real-time control) and the 51,000-tile He-cooled tungsten divertor target system are not discussed in terms of technology readiness in the paper.
 
----
+**Gaps**:
+- Novel X-point stellarator divertor: no experimental data — truly-unknown — important
+- V-4Cr-4Ti at FPP-scale neutron fluence: limited irradiation database — not-yet-sourced — important
+- FSU assembly and integration at 324-coil scale — not-yet-sourced — important (derivable from Canis data but not demonstrated)
+- 51,000-piece He-cooled W tile divertor manufacturing at scale — not-yet-sourced — nice-to-have
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
 **Available**:
-- REBCO HTS tape: commercially available from multiple suppliers (Canis paper tested tapes from 3 suppliers including YBCO and GdBCO variants). Current supply adequate for experiments; scaling to 336 full-scale coils requires HTS production ramp-up. Referenced cost projection study (Grant & Sheahen, arXiv:cond-mat/0202386) cited in Helios paper.
-- V-4Cr-4Ti vanadium alloy: 15-year first-wall lifetime documented; material referenced against Smith et al. (2000) and Sparks et al. (2022). Supply chain not discussed in published sources.
-- Pb-17Li breeder with 65% Li-6 enrichment: Li-6 enrichment is the key bottleneck — current global Li-6 enrichment capacity is limited (primarily Russia/China historical capability, with new US program underway via ORNL). Paper specifies 65% enrichment and 1.3 TBR but doesn't quantify enrichment cost.
-- Tungsten divertor targets: mature material, commercially available, standard in fusion devices.
-- EUROFER97 structural steel: EU-developed reduced-activation ferritic-martensitic steel, produced in limited quantities for fusion R&D.
-- SiC MHD inserts for blanket: specialty ceramic, limited production scale.
-
-**Missing**:
-- REBCO tape cost projections specific to Helios scale (336 coils × hundreds of km of tape).
-- Li-6 enrichment cost and supply chain analysis.
-- V-4Cr-4Ti production capacity and cost.
-- EUROFER97 production scaling.
+- **REBCO tape**: The Canis paper confirmed manufacturing from three separate REBCO suppliers (including YBCO and GdBCO variants), demonstrating multi-supplier independence. Commercial availability is confirmed. Large-bore HTS coils at 20 T have been achieved (cited in §3.6). The Canis team demonstrated ≤1 day DP takt time.
+- **Structural steel (SS316L)**: Standard, well-characterized supply chain.
+- **EUROFER97**: Well-developed material for European fusion programs; blanket structure in Helios.
+- **Tungsten**: 51,000 hex tiles at 2.5 cm width for divertor; standard supply chain for tungsten but fusion-scale manufacturing not demonstrated at this tile count.
+- **Lead-lithium (Pb-17Li)**: Lead supply chain established. Lithium enrichment to 65% Li-6 is a gap explicitly flagged in the ARIES cost account documentation: "there is no effective large production capability of enriched lithium in the U.S." as of 2013; only small government production in the 1950s–1960s using COLEX process (which was environmentally damaging). Knowledge/sources/aries_cost_account_documentation/ confirms this remains an open supply chain challenge.
+- **V-4Cr-4Ti**: The Helios paper (§4.2) explicitly states "immature supply chain" as a contraindicating consideration. Used for first wall and vacuum vessel; no large-scale industrial production exists.
 
-**Gaps**:
-- REBCO tape cost at scale — `not-yet-sourced` — **blocking** (coil cost is a primary capital cost driver; fleet-wide sources may have per-kA·m pricing estimates)
-- Li-6 enrichment cost and supply security — `not-yet-sourced` — **important** (tritium breeding depends on enriched Li; cost is non-trivial)
-- V-4Cr-4Ti supply chain — `not-yet-sourced` — **important** (alternative vanadium alloy sourcing not discussed; US production capacity is limited)
-- EUROFER97 scaling — `not-yet-sourced` — **nice-to-have** (DEMO program producing it; likely not a blocking gap for cost estimation)
+**Missing**: No quantitative supply chain analysis has been published by Thea Energy. The scale of REBCO production needed for 336 coils (total tape length not stated) has not been compared against current commercial production capacity. Tritium supply chain (1-2 kg startup, then self-sufficient) is not analyzed for startup cost.
 
----
+**Gaps**:
+- V-4Cr-4Ti at FPP scale: no commercial production exists — truly-unknown — important (blocking cost driver if not resolved)
+- Li-6 enrichment at 65% for multi-tonne LiPb inventory: no large-scale US production capability confirmed — truly-unknown — important (knowledge/sources/aries_cost_account_documentation/ confirms this gap; enrichment cost described as "completely unknown")
+- REBCO tape production capacity vs. demand for 336 Helios coils — not-yet-sourced — important (search: REBCO production capacity surveys, CFS scaling analyses)
+- SiC/SiC MHD inserts (blanket flow channels) at fusion-relevant scale: low TRL in neutron environment — not-yet-sourced — nice-to-have
+- Tritium startup procurement cost (1-2 kg): not quantified — not-yet-sourced — nice-to-have
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electric power | 390 MWe | arXiv:2512.08027 Table 1 | high |
-| Fusion power | 958 MW | arXiv:2512.08027 Table 1 | high |
-| Thermal power | 1,094 MW | arXiv:2512.08027 Table 1 | high |
-| Thermal efficiency (gross) | 40.2% | arXiv:2512.08027 §4.4 | high |
-| Net efficiency (net/thermal) | ~35.6% | Derived: 390/1094 | high |
-| Capacity factor | 88% | arXiv:2512.08027 Abstract, §2 | high |
-| Maintenance cycle | 84 days / 2 years | arXiv:2512.08027 §4.5 | high |
-| Plant design lifetime | 40 years | arXiv:2512.08027 §2 | high |
-| First wall lifetime | 15 full-power years | arXiv:2512.08027 §2 | high |
-| Coil lifetime | 40 years (plant lifetime) | arXiv:2512.08027 §2 | high |
-| ECRH recirculating power (ignited) | ~1 MW | arXiv:2512.08027 §3.1 | high |
-| ECRH recirculating power (startup) | 10 MW | arXiv:2512.08027 §3.1 | high |
-| Cryogenic cooling load | Not explicitly stated | — | low |
-| Tritium startup inventory | 1–2 kg | arXiv:2512.08027 Table 1 | high |
-| LCOE target (first plant) | ~$150/MWh | Dossier metadata (source uncertain) | low |
-| LCOE target (at scale) | ~$60/MWh | Dossier metadata (source uncertain) | low |
+| Net electric power | 390 MWe | arXiv:2512.08027 Table 1 | h |
+| Gross electric power | 438 MWe | arXiv:2512.08027 §4.4 | h |
+| Total thermal power | 1,094 MW | arXiv:2512.08027 §4.4 | h |
+| Fusion power | 958 MW | arXiv:2512.08027 Table 1 | h |
+| Thermal efficiency (Rankine) | ~40.2% | arXiv:2512.08027 §4.4 | h |
+| Capacity factor | 88% | arXiv:2512.08027 §4.5, abstract | m |
+| Planned maintenance cycle | 84 days every 2 years | arXiv:2512.08027 §4.5 | m |
+| Recirculating auxiliary power | ~70 MW (~18% of gross) | arXiv:2512.08027 §4.6 | m |
+| Cryogenic system electric power | ~10 MW at 25% Carnot efficiency | arXiv:2512.08027 §4.5 | m |
+| ECRH power (ignited operation) | 2.5 MW (1 MW plasma + overhead) | arXiv:2512.08027 §4.6 | h |
+| Magnet operating temperature | 20 K | arXiv:2512.08027 Table 1 | h |
+| First wall lifetime | 15 full-power years | arXiv:2512.08027 §4.2 | m |
+| HTS coil lifetime | 40+ years (full plant life) | arXiv:2512.08027 §2 | m |
+| Tritium startup inventory | 1–2 kg | arXiv:2512.08027 Table 1 | m |
+| Steam cycle temperature | 635°C superheated | arXiv:2512.08027 §4.4 | h |
+| Plant electrical output (Q effectively ∞) | Ignited, recirculating power fraction <3% | arXiv:2512.08027 §1 | h |
+| LCOE company target (FOAK → NOAK) | $150 → $60/MWh | Dossier (thea.energy) | l |
+| LCOE analog (D-T MFE NOAK tokamak) | $140–$550/MWh | knowledge/sources/tea_dt_mfe_cost_analysis/ | l |
+| ARIES-CS LiPb blanket cost | ~$171M (2009$) | knowledge/sources/aries_cost_account_documentation/ | l |
+| Material cost: V-4Cr-4Ti | $37/kg | knowledge/sources/tea_dt_mfe_cost_analysis/ Table 4 | l |
+| Material cost: SS316 LN | $10/kg | knowledge/sources/tea_dt_mfe_cost_analysis/ Table 4 | l |
+| Material cost: Tungsten | $29/kg | knowledge/sources/tea_dt_mfe_cost_analysis/ Table 4 | l |
+| Supplemental heating system cost | ~$2.5/W | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.2.2 | l |
+| Cryosystem unit cost | ~$300/kW at 20K | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.2.2 | l |
+| O&M staffing (analog) | 50–95 FTE | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.4 | l |
+| O&M annual maintenance fraction | 9% of reactor plant equipment cost | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.4 | l |
+| Decommissioning cost (analog) | 5% of total capital | knowledge/sources/tea_dt_mfe_cost_analysis/ §2.5 | l |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost (total, by CAS) | proprietary | blocking | No CAS-level breakdown in arXiv paper; DOE Milestone report may contain it; ARIES-CS analog available as fleet-wide proxy |
-| HTS coil cost (total) | not-yet-sourced | blocking | Dominant capital cost driver; depends on REBCO $/kA·m × tape length; Grant & Sheahen (2002) cited in paper but not extracted |
-| Balance of plant cost (turbine island, heat exchangers) | derivable | important | Standard steam Rankine at 390 MWe; TEA D-T MFE source and ARIES cost accounts can provide analogs |
-| O&M cost (annual, staffing + consumables) | not-yet-sourced | blocking | No estimate in public sources; comparable to a ~400 MWe nuclear plant baseline is the likely analog |
-| First wall replacement cost (per 15-year cycle) | derivable | important | V-4Cr-4Ti blanket modules; sector maintenance scheme enables cost estimation if component costs known |
-| Cryogenic system operating cost | not-yet-sourced | important | 20 K operation for 336 REBCO coils; non-trivial parasitic load; not quantified |
-| Control system capital cost (software + hardware) | truly-unknown | important | 450+ independent variables, novel software stack; no published cost estimate |
-| Li-6 enrichment cost | not-yet-sourced | important | 65% enrichment for LiPb blanket; DOE/ORNL enrichment program data needed |
-| LCOE derivation / methodology | proprietary | blocking | $150/$60 targets cited in dossier without traceable citation; presumed from internal Thea analysis |
-| Fuel cost (D-T annual) | derivable | nice-to-have | Low relative to capital; standard D-T fuel cost methodology applies |
-| Decommissioning cost estimate | derivable | nice-to-have | CAS 90s approach from ARIES cost account documentation applicable |
-
----
+| CAS-level capital cost estimates (any subsystem) | derivable | blocking | Zero cost data in concept-scoped sources; must build bottom-up from geometry + material costs using TEA/ARIES framework; wide uncertainty expected |
+| Total REBCO tape length for 336 Helios coils | derivable | important | Primary capital cost driver; Canis coil specs (4mm tape, 1500 turns per coil, 190×163×47mm winding pack) available as scaling basis but full Helios coil dimensions not stated numerically for encircling coils |
+| Steel/structural mass for coil support structure | derivable | important | ARIES-CS structure was 3,000 tons; Helios is different architecture; mass estimate requires geometric reconstruction from figures |
+| Blanket capital cost (Helios-specific) | derivable | important | 50cm LiPb geometry + EUROFER97 structure defined; ARIES-CS $171M (2009$) provides lower bound analog; requires scaling to Helios geometry |
+| V-4Cr-4Ti first wall/VV fabrication cost | not-yet-sourced | important | Immature supply chain; $37/kg raw material cost available from TEA source but fabrication premium unknown |
+| Li-6 enrichment cost for LiPb startup charge | truly-unknown | important | No large-scale commercial process; ARIES doc confirms no pricing data exists |
+| REBCO tape unit cost at commercial production scale | not-yet-sourced | important | No public CFS/Thea quotes; literature suggests $5–50/m range; search: OSTI, CFS papers |
+| Annual O&M cost (Helios-specific) | derivable | important | TEA source provides methodology (9% RPE cost + 50-95 FTE); applicable as first-pass |
+| Power supply system capital cost | derivable | nice-to-have | 12 encircling coil PSUs (50 kA) + 324 shaping PSUs + ECRH; TEA $1.5/W power supply and $2.5/W heating analogs available |
+| FSU (field shaping unit) assembly and installation cost | truly-unknown | nice-to-have | Novel manufacturing process for grouped 324-coil assembly; no analog |
+| Back-solve to $0.01/kWh: specific binding constraints | derivable | nice-to-have | Can be computed once baseline LCOE is established |
 
 ## Source Recommendations
 
-1. **Access the 4 Nuclear Fusion companion papers** (Jan 2025, Nuclear Fusion vol. 65 issue 2) — `not-yet-sourced` — the companion papers on Eos scoping and fast ion confinement likely contain more quantitative detail on transport assumptions that affect LCOE sensitivity. Publicly available via IOP Science.
+- **REBCO tape production capacity and unit cost at scale**: Search OSTI for "REBCO HTS tape cost projection" or "HTS cost roadmap." CFS SPARC papers may include REBCO cost assumptions. The 2022 Fusion Industry Association Supply Chain report is worth checking. Flag as `not-yet-sourced — confirm existence before searching`.
 
-2. **Read `knowledge/sources/tea_dt_mfe_cost_analysis/`** — this fleet-wide source covers TEA methodology for D-T MFE with detailed CAS cost breakdowns. It is directly applicable to Helios as a D-T MFE steady-state plant. Use for BOP cost analogs, O&M estimates, and LCOE methodology. The ARIES-CS stellarator costing in that study (if present) is the closest analog.
+- **V-4Cr-4Ti supply chain analysis**: Published analyses exist from ARIES-AT and US materials program. Search OSTI for "V-4Cr-4Ti fusion supply chain" or "vanadium alloy fusion cost." Flag as `not-yet-sourced — likely exists in DOE fusion materials program literature`.
 
-3. **Read `knowledge/sources/aries_cost_account_documentation/`** — essential for assigning CAS numbers and applying standard fusion costing algorithms to Helios. ARIES-CS (compact stellarator, similar scale to Helios) is the most directly applicable prior stellarator plant study and likely contains cost estimates usable as analogs.
+- **Li-6 enrichment cost**: No large-scale commercial production exists as of 2013 per knowledge/sources/aries_cost_account_documentation/. Search for recent IAEA or DOE reports on lithium isotope separation for fusion. This is likely still an open research gap. Flag as `not-yet-sourced, low probability of finding commercial pricing — may remain truly-unknown`.
 
-4. **Search for ARIES-CS cost data** — ARIES-CS was a compact stellarator plant study at similar scale (R~7.7 m, 1 GW thermal). It has a detailed cost breakdown. Thea explicitly compares Helios to ARIES-CS in the paper. Search OSTI for "ARIES-CS cost" or "compact stellarator power plant economics." `unverified — confirm existence before searching`.
+- **ARIES-CS total capital cost and COE**: The ARIES-CS final report (Najmabadi et al., 2008, Fusion Engineering and Design) contains the full cost breakdown not covered by the ARIES cost account methodology document. This would provide the best available stellarator analog for a complete cost estimate. Available via ARIES project website. Flag as `not-yet-sourced — high probability of existence`.
 
-5. **Check `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`** — multi-concept costing in a common CAS framework. While none of the four concepts is a stellarator, the O&M methodology and indirect cost fractions are applicable.
+- **Helios coil structural mass**: Thea Energy has not published structural masses. The ARIES-CS coil structure was 3,000 tons (Helios paper §1 reference). The Helios encircling coil structure uses SS316L cases + central support + inter-coil trusses. A rough estimate using major radius (8m) and 12 planar coils + truss geometry can serve as a first-pass proxy. `derivable`.
 
-6. **REBCO tape cost projection** — Grant & Sheahen (2002) is already cited in the Helios paper (ref [49]). More current REBCO cost projections exist through Commonwealth Fusion Systems and SuperPower Inc. announcements. Search OSTI or Google Scholar for "REBCO cost projection fusion" for 2020–2025 estimates. `unverified — confirm existence before searching`.
+- **Divertor X-point heat flux management**: No external sources currently address this gap — it is a Thea Energy research-in-progress item. Any ITER detachment or impurity seeding literature (search: "detachment stellarator X-point") could bound assumptions. Flag as `not-yet-sourced — search ITER science program publications`.
 
-7. **Li-6 enrichment cost** — ORNL's Li-6 Enrichment Program (Milestone-program adjacent) likely has public cost-per-gram estimates. Search DOE/ORNL NNSA publications. `unverified — confirm existence before searching`.
+**Fleet-wide source disqualifications** (per assessment protocol):
 
----
+- `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/` — Opened and read (v3 of arXiv:2512.08027). This is a later version of the same paper already captured as a concept-scoped source (v1). The content is identical in all substantively relevant sections; no additional information was found.
 
-## Summary
+- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/` — Not plausibly applicable: per the source index, this covers four ARPA-E ALPHA concepts (FRC, IEC, MIF, compact tokamak variants), none of which are stellarators. The CAS methodology it uses is already covered by the tea_dt_mfe_cost_analysis and aries_cost_account_documentation sources already read; no marginal value for this concept.
 
-**Proceed to full analysis with the fleet-wide TEA source as cost scaffold.** The Helios preconceptual design provides the most detailed technical foundation available for any private fusion concept at this stage — physics is well-characterized with high-fidelity simulations, engineering architecture is documented at a level sufficient for subsystem-level cost estimation, and key performance parameters (390 MWe, 88% CF, 40.2% thermal efficiency, 40-year plant life) are firm. 
+- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/` — Not plausibly applicable: the source index describes it as an ORNL historical LCOE benchmarking study for fusion vs. other electricity sources. It addresses none of the identified gaps (which are internal capital cost components and supply chain costs), and the LCOE benchmarking context needed here is already supplied by the tea_dt_mfe_cost_analysis ($140–550/MWh NOAK range).
 
-The capital cost and O&M gaps are significant but **bridgeable**: Thea explicitly compares Helios to ARIES-CS, making ARIES-CS cost data the natural analog for the magnet system and structural costs. The TEA D-T MFE fleet-wide source covers BOP and O&M methodology directly applicable to a 400 MWe D-T MFE plant. The two main technical uncertainties that affect LCOE sensitivity — REBCO tape cost at scale and HTS coil lifetime under neutron flux — are real but have published partial data. The analysis should proceed with cost estimates derived from ARIES-CS and ARIES cost account analogs, with explicit uncertainty bounds on REBCO cost and V-4Cr-4Ti replacement frequency.
+- All IFE-focused sources (laser IFE, heavy-ion, inertial fusion) — Clearly not applicable to a magnetic confinement stellarator concept.
+
+## Summary
 
----
+Proceed to full analysis. The qualitative sections (§1–4) of the D1+ analysis can be executed with high confidence — the Helios preconceptual design is the most complete publicly available documentation of a private fusion concept, with DOE external validation adding credibility. For the quantitative LCOE model (§5), a defensible first-pass estimate can be constructed by combining: (a) the excellent performance parameters from Helios, (b) material unit costs from `knowledge/sources/tea_dt_mfe_cost_analysis/`, (c) the ARIES-CS blanket cost analog from `knowledge/sources/aries_cost_account_documentation/`, and (d) geometric reasoning from the Helios engineering sections to estimate component masses. Key uncertainties that will dominate the LCOE sensitivity analysis are: REBCO tape length and unit cost (magnet system ~40–60% of direct cost for HTS MFE designs), V-4Cr-4Ti fabrication cost, and Li-6 enrichment cost. The $150 → $60/MWh company LCOE target provides a sanity check but is not independently validated.
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 3
-important_count: 8
-counting_method: "deduplicated across all sections; blocking = capital cost breakdown, O&M cost quantification, LCOE derivation/methodology; important = H_ISS04 in QA stellarator, TRL formal matrix, V-4Cr-4Ti qualification, REBCO cost at scale, Li-6 enrichment cost, V-4Cr-4Ti supply chain, HTS coil cost, cryogenic operating cost, balance of plant cost, first wall replacement cost, control system cost (collapsed to 8 distinct items)"
+blocking_count: 1
+important_count: 6
+counting_method: "section_5_lcoe_blocking_plus_important_across_all_sections_deduplicated"
 section_coverage:
   availability_of_data:       "Good"
   system_function:            "Good"
```
