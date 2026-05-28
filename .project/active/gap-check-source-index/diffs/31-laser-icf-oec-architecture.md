# Diff: 31-laser-icf-oec-architecture

**Generated:** 2026-05-22T11:17:55-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 8 | 4 |
| important_count  | 2 | 5 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
165:1. **For laser system capital cost**: Search OSTI for "diode-pumped solid-state laser inertial fusion energy cost" and the Xcimer whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — has $/J breakdown for KrF vs DPSSL. BLF's OEC claims to undercut both, but the Xcimer numbers give a useful upper bound. Use as analog with explicit downward adjustment. `not-yet-sourced — verify content before citing`
167:2. **For IFE LCOE methodology and parameter sensitivity**: Read the Hawker simplified IFE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — Monte Carlo over 14 technology-agnostic parameters including gain, driver efficiency, rep rate. Directly applicable to BLF parameterization.
169:3. **For IFE reactor chamber and blanket cost analogs**: `knowledge/sources/energy_from_inertial_fusion/` (1992 comprehensive IFE review covering HYLIFE, SOMBRERO, other plant designs with cost breakdowns). Also relevant: LIFE engine design reports (search OSTI for "LIFE engine laser inertial fusion energy LLNL" — not currently ingested). `not-yet-sourced — unverified; confirm existence before searching`
173:5. **For capacity factor and availability modeling**: PyFECONS (`/home/reid/PyFECONS`) includes IFE modules; check for rep-rate pulsed operation availability assumptions.
```

## Blocking-tier lines (baseline)

```
(none)
```

## Blocking-tier lines (new)

```
35:- No experimental target gain data from any direct-drive shock ignition campaign at BLF's specified parameters — `truly-unknown` for BLF specifically, `not-yet-sourced` for community experiments — **blocking** (G=160 is the pivotal parameter for all power balance conclusions)
57:- Target gain G=160 unvalidated at any laser energy — `truly-unknown` (no shock ignition experiment demonstrates this) — **blocking**
58:- DEC efficiency at η_DEC = 0.44 unvalidated — `not-yet-sourced` (some experimental IFE DEC programs exist but not for this geometry) — **blocking**
59:- First wall lifetime / rep-rate survival data — `truly-unknown` — **blocking**
92:- OEC at reactor scale (150m, pulsed, nanosecond) — no experimental data — `truly-unknown` for this configuration — **blocking** (the central technology innovation)
93:- Cryogenic DT target fabrication at 1–10 Hz — `truly-unknown` — **blocking**
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/31-laser-icf-oec-architecture.md	2026-05-22 09:21:13.881455289 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/gap_report.md	2026-05-22 11:17:55.682989096 -0700
@@ -1,49 +1,204 @@
-Gap report written to `analyses/31-laser-icf-oec-architecture/gap_report.md`. Here's the summary:
+I now have sufficient information to write the gap assessment. Let me compile it.
 
 ---
 
-## Assessment Summary
+# Gap Assessment: Laser ICF - OEC Architecture (D-T)
 
-**Rating: Mostly Ready (qualitative) / Significant Gaps (quantitative LCOE)**
+## Overall Readiness
+**Rating**: Mostly Ready
 
-### What's unusually strong for an early-stage startup
+**Summary**: Blue Laser Fusion's Optics Express 2025 paper (Sunahara et al.) provides a single comprehensive primary source with a complete, internally-consistent power balance (Table 2), reactor configuration description, and laser system roadmap. The physics/engineering design layer is well-documented for a concept at this stage. The dominant gaps are on the cost side: no capital cost estimates exist for any subsystem (laser, chamber, blanket, DEC), and several performance parameters critical to power balance (target gain G=160, DEC efficiency) remain unvalidated assumptions rather than experimental results. Fleet-wide IFE economic sources can partially fill LCOE methodology gaps.
 
-The Sunahara et al. *Optics Express* 2025 paper is a genuine asset — it provides a complete power balance table (Table 2) with 14+ quantitative parameters including net output (102–2,820 MW_e across the rep rate range), recirculating power fractions, efficiencies, and reactor geometry. This is more than most IFE startups disclose. The qualitative write-up can proceed directly.
+---
+
+## Section Coverage
+
+### 1. Availability of Data
+**Coverage**: Partial
+
+**Available**:
+- One peer-reviewed, open-access paper (Sunahara et al., *Optics Express* 33(22), 2025) authored by BLF staff, covering laser physics, reactor configuration, and complete power balance. This is the authoritative source for all quantitative design parameters.
+- Company website confirming D-T fuel, dual energy conversion, 1 GW target output.
+- Finance news confirming $37.5M seed round (SoftBank, Maezawa, Itochu), giving company scale context.
+- DOE INFUSE award reports (2024, 2025) confirming R&D collaboration with Caltech (OEC scaling) and CSU (mirror coatings).
+- Moonshot Program selection (Japan) confirming University of Osaka collaboration.
+- Supporting fleet-wide sources on TBB physics (`osti-servlets-purl-1305833`, `osti-servlets-purl-1165762`) and He-Brayton cycle design (`osti-servlets-purl-1323907`), which are MFE-focused but provide analogical data for the helium-cooled blanket.
+- INL paper on PbLi tritium extraction (`lasers-sites-lasers-files-2023-11-fuerst-idaho-ife-workshop`) is directly applicable to BLF's LiPb blanket.
+
+**Missing**:
+- No independent costing study or plant-level TEA by any national laboratory or third party.
+- No published capital cost estimates for any BLF subsystem.
+- No conference proceedings from BLF team on target fabrication, chamber design, or O&M planning.
+
+**Gaps**:
+- No independent plant study or cost estimate — `proprietary` / `not-yet-sourced` — **important** (blocks LCOE derivation but concept description is complete enough to proceed with analog-based estimates)
+- No experimental target gain data from any direct-drive shock ignition campaign at BLF's specified parameters — `truly-unknown` for BLF specifically, `not-yet-sourced` for community experiments — **blocking** (G=160 is the pivotal parameter for all power balance conclusions)
+
+---
+
+### 2. Challenges in Capturing System Function
+**Coverage**: Partial
+
+**Available**:
+- The OEC laser architecture is described in detail. The paper gives cascade efficiency breakdown (ηw = 0.16 at 1 µm, η3ω = 0.6, overall ηw* = 0.10), enabling full laser recirculating-power calculation.
+- The dual-channel energy conversion (70% thermal via He-Brayton, 30% direct via DEC) is described with efficiency values (ηth* = 0.44, η_DEC = 0.44).
+- LPI mitigation strategy (multicolor, SRP, RPP, 500-beam uniformity) is described with physics rationale and ties to FLUX experiments at OMEGA.
+- Power balance equations and the full parameterization are given (Table 2 in paper).
+- Chamber configuration (8–10 m radius, magnetized dry-wall, W/RAFM layered first wall) described.
+
+**Missing / hard to model**:
+- **Target gain G=160 is unvalidated**: The paper acknowledges the design operates "beyond the CBET-mitigated curve" of Froula et al. — an extrapolation, not experiment. No shock ignition experiment has demonstrated G > ~10. This propagates a multiplicative 1σ uncertainty of likely ±50–100% into gross power output.
+- **DEC system**: η_DEC = 0.44 is described as "conservative" but references Rax et al. (2025) theoretical work, not demonstrated hardware. DEC for IFE has no cost analogue.
+- **First wall survival at 10 Hz**: The paper explicitly notes that "comprehensive MHD and PIC simulations will be performed" — not yet done. No replacement interval data exists.
+- **Cryogenic target injection at 1–10 Hz**: Paper explicitly acknowledges this is "still major issues" without a solution.
+- **OEC at 150m scale**: Only 1.5m demonstrated with CW signal. 15m system under construction. The 150m reactor-scale is a 100× extension from the demonstrated prototype.
+
+**Gaps**:
+- Target gain G=160 unvalidated at any laser energy — `truly-unknown` (no shock ignition experiment demonstrates this) — **blocking**
+- DEC efficiency at η_DEC = 0.44 unvalidated — `not-yet-sourced` (some experimental IFE DEC programs exist but not for this geometry) — **blocking**
+- First wall lifetime / rep-rate survival data — `truly-unknown` — **blocking**
+- Cryogenic target injection at 1–10 Hz — `truly-unknown` in the industry — **important**
+
+---
+
+### 3. Maturity of Key Subsystems and Components
+**Coverage**: Partial
+
+**Available**:
+- OEC prototype results: 1.5m cavity, finesse 419,000, enhancement factor 59,000 (CW, not pulsed). 15m system under construction at Goleta and Osaka University.
+- THG frequency conversion (1060 nm → 350 nm via KDP/DKDP): TRL 7–8; established technology used at NIF and other facilities.
+- LiPb blanket concept: Described as under collaborative development with universities and national labs; SiC ceramic investigation ongoing; HTGR integration being explored.
+- He-gas cooling: Mature technology with fission reactor heritage (HTGR).
+- RAFM/W first wall: Established materials for fusion, TRL 4–5 for IFE application.
+- DEC concept: TRL 2 (theoretical).
+
+**TRL assessment by subsystem** (estimated from available data):
+
+| Subsystem | Estimated TRL | Basis |
+|-----------|-------------|-------|
+| CBC fiber laser arrays | 4–5 | Multi-channel CBC demonstrated in lab |
+| OEC (1.5m, CW) | 4 | Finesse/enhancement demonstrated |
+| OEC (15m, pulsed) | 2–3 | Under construction 2025 |
+| OEC (150m, reactor-scale) | 1–2 | Design phase only |
+| THG frequency conversion | 7–8 | NIF-heritage technology |
+| Shock ignition target physics | 3–4 | Simulations; some omega-scale experiments but not at BLF parameters |
+| LiPb He-cooled blanket | 2–3 | Conceptual; investigating HTGR integration |
+| W/RAFM first wall | 4–5 | Established materials, IFE-specific geometry TRL lower |
+| Direct Energy Conversion | 2 | Theoretical; Rax et al. 2025 is a preprint |
+| Cryogenic DT target fabrication at 1–10 Hz | 1–2 | Not demonstrated anywhere |
+| Tritium extraction from LiPb (vacuum permeator) | 4 | INL TEX experiment underway |
+
+**Gaps**:
+- OEC at reactor scale (150m, pulsed, nanosecond) — no experimental data — `truly-unknown` for this configuration — **blocking** (the central technology innovation)
+- Cryogenic DT target fabrication at 1–10 Hz — `truly-unknown` — **blocking**
+- DEC hardware at any IFE-relevant scale — `not-yet-sourced` (some IFE DEC programs; worth searching OSTI) — **important**
+
+---
+
+### 4. Key Materials and Supply Chain Considerations
+**Coverage**: Partial
 
-### The central gap
+**Available**:
+- Tritium supply: General IFE community concern acknowledged; INL paper notes ~0.37 kg/day for a 2.2 GWth IFE reactor; BLF design claims limited chamber tritium inventory (few mg) as an advantage.
+- LiPb blanket: Natural lithium (no Li-6 enrichment required in the paper's description, though TBR would benefit from enrichment); Pb neutron multiplier.
+- First wall: W facing + RAFM steel — well-characterized materials with fission supply chains.
+- OEC mirrors: Ultra-high reflectivity (>99.9995%) coatings are a critical supply chain item; DOE INFUSE award with CSU specifically targets this.
+- SiC ceramics: Under investigation as blanket structural material; low industrial maturity for fusion-relevant conditions.
+- KDP/DKDP crystals: Required at 500-module scale for THG; supply chain for large KDP crystals is established (NIF heritage) but scaling to 500 modules is an open question.
+
+**Missing**:
+- No supply chain analysis published for OEC mirror coating production at 500-module scale.
+- No fiber amplifier supply chain estimate (how many individual fibers per module, cost per fiber, manufacturing ramp).
+- No TBR calculation stated in paper — unclear if natural Li achieves TBR > 1.05 without enrichment.
+- No tritium startup inventory analysis.
+- No SiC structural component manufacturing roadmap.
+
+**Gaps**:
+- OEC mirror coatings at 500-module scale: manufacturing throughput and cost — `not-yet-sourced` / `proprietary` — **important** (cost could be significant; DOE INFUSE suggests it is a known challenge)
+- Li-6 enrichment requirement (TBR not calculated) — `not-yet-sourced` — **important**
+- KDP/DKDP crystal supply at 500-module scale — `not-yet-sourced` — **important**
+- SiC ceramic supply chain for blanket — `not-yet-sourced` — **nice-to-have** at this stage
 
-**Zero published cost estimates for any subsystem.** The paper is a physics/engineering study, not a techno-economic one. The entire LCOE model must be built from analogues (ARIES-IFE, LIFE, HAPL program reports).
+---
+
+### 5. LCOE Parameter Extraction
+**Available Parameters**:
+
+| Parameter | Value/Range | Source | Confidence |
+|-----------|-------------|--------|------------|
+| Net electrical output | 102–2820 MW_e | OE-2025, Table 2 | H (design target; G and η assumed) |
+| Laser energy per shot | 5 MJ UV | OE-2025, Table 2 | H |
+| Repetition rate | 1–10 Hz | OE-2025, Table 2 | H |
+| Wall-plug-to-UV efficiency | 10% | OE-2025, Table 2 | M (not demonstrated at scale) |
+| Target gain | G = 160 | OE-2025, Table 2 | L (unvalidated extrapolation) |
+| Thermal conversion efficiency | 44% | OE-2025, Table 2 | M (He-Brayton analog exists) |
+| DEC efficiency | 44% | OE-2025, Table 2 | L (theoretical) |
+| Total conversion efficiency | 44% | OE-2025 | M (combines two L-confidence terms) |
+| Recirculating power fraction | 17–43% | OE-2025, Table 2 | M |
+| Auxiliary (non-laser) power | 100 MW | OE-2025, Table 2 | L (assumed constant) |
+| Chamber radius | 8–10 m | OE-2025 text | M |
+| Blanket coolant | He gas (LiPb breeder) | OE-2025 | H |
+| First wall material | W facing, RAFM steel | OE-2025 | H |
+| D-T fuel | Cryogenic DT, natural Li | OE-2025 | H |
+| Tritium extraction | Vacuum permeator from LiPb | OE-2025 + INL paper | M |
+
+**Missing Parameters**:
+
+| Parameter | Gap Type | Criticality | Notes |
+|-----------|----------|-------------|-------|
+| Capital cost of OEC laser system ($/J or total) | proprietary | Blocking | BLF claims cost advantage over DPSSL but no $/J number published; Xcimer paper has DPSSL baseline |
+| Capital cost of reactor chamber | not-yet-sourced | Blocking | Use LIFE/HiPER/SOMBRERO analogs with caveats |
+| Capital cost of blanket system | not-yet-sourced | Blocking | He-LiPb blanket has no published IFE cost estimate; MFE analogs exist |
+| Capital cost of DEC system | truly-unknown | Blocking | Novel subsystem; no cost data anywhere |
+| Target fabrication cost ($/target at 10 Hz) | not-yet-sourced | Blocking | Community estimates exist (FIRE collab) but not for this target type |
+| First wall lifetime / replacement interval | truly-unknown | Blocking | No materials lifetime data under BLF operating conditions |
+| Capacity factor / availability | truly-unknown | Blocking | Pulsed IFE rep-rate availability not modeled |
+| Balance of plant capital cost | not-yet-sourced | Important | Fleet-wide analog (ARIES, LIFE) can fill with caveat |
+| O&M annual cost estimate | not-yet-sourced | Important | No concept-specific estimate; IFE analogs exist |
+| Decommissioning cost | not-yet-sourced | Nice-to-have | RAFM/W activation levels — derivable from material inventory |
+| Tritium breeding ratio | not-yet-sourced | Important | Not calculated in paper; natural Li + Pb multiplier probably achieves TBR ~1.05–1.1 but unconfirmed |
+
+---
+
+## Source Recommendations
+
+1. **For laser system capital cost**: Search OSTI for "diode-pumped solid-state laser inertial fusion energy cost" and the Xcimer whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/`) — has $/J breakdown for KrF vs DPSSL. BLF's OEC claims to undercut both, but the Xcimer numbers give a useful upper bound. Use as analog with explicit downward adjustment. `not-yet-sourced — verify content before citing`
+
+2. **For IFE LCOE methodology and parameter sensitivity**: Read the Hawker simplified IFE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — Monte Carlo over 14 technology-agnostic parameters including gain, driver efficiency, rep rate. Directly applicable to BLF parameterization.
 
-### Key blocking gaps for the quantitative model
+3. **For IFE reactor chamber and blanket cost analogs**: `knowledge/sources/energy_from_inertial_fusion/` (1992 comprehensive IFE review covering HYLIFE, SOMBRERO, other plant designs with cost breakdowns). Also relevant: LIFE engine design reports (search OSTI for "LIFE engine laser inertial fusion energy LLNL" — not currently ingested). `not-yet-sourced — unverified; confirm existence before searching`
 
-| Gap | Type | Criticality |
-|-----|------|-------------|
-| Laser system (CBC-OEC) capital cost | proprietary + not-yet-sourced | **Blocking** |
-| OEC mirror cost/lifetime | truly-unknown | **Blocking** |
-| Target fabrication cost at Hz rep rates | not-yet-sourced | **Blocking** |
-| Chamber/first wall capital cost | not-yet-sourced | **Blocking** |
-| DEC capital cost | truly-unknown | Important |
-| Capacity factor / availability | derivable | Important |
+4. **For target fabrication cost at rep rate**: BLF is on the industrial council for DOE FIRE Collaborative (led by General Atomics on fusion targets per Semiconductor Today source). Published outputs from this collaborative would be the best source. Search OSTI and DOE FES for "inertial fusion energy target fabrication cost repetition rate." `not-yet-sourced — unverified`
 
-### Physics uncertainty that propagates hardest into LCOE
+5. **For capacity factor and availability modeling**: PyFECONS (`/home/reid/PyFECONS`) includes IFE modules; check for rep-rate pulsed operation availability assumptions.
 
-Target gain G=160 is simulation-based (Froula et al.), not experimentally validated. This is the single largest physics uncertainty — it directly drives the net output and recirculating power fraction.
+6. **For DEC cost and efficiency**: Search for "direct energy conversion inertial fusion energy" and the Rax et al. 2025 paper cited by BLF (citation [73] in OE-2025: "designs based on recent theoretical work"). `not-yet-sourced — the paper may not have been published yet as of Phase 1a extraction`
 
-### Source recommendations
+7. **For first wall/chamber survival at 10 Hz**: HiPER and LIFE design reports contain first wall lifetime analyses under repetitive IFE conditions. Not currently ingested but OSTI-available. `not-yet-sourced — unverified; search "HiPER first wall repetitive inertial fusion energy"`
 
-The ARIES-IFE plant study and HAPL program target cost reports are the highest-priority acquisitions before finalizing the quantitative model. The Rax et al. (2025) DEC paper cited in Sunahara et al. should also be retrieved to validate the η_DEC = 0.44 assumption.
+---
+
+## Summary
+
+The concept is well-documented at the physics and systems configuration level — the Sunahara 2025 Optics Express paper provides a complete, internally-consistent power balance and is more detailed than typical pre-demonstration IFE company publications. Proceed to full qualitative analysis immediately.
+
+The LCOE quantitative model will require substantial analog-filling: all capital cost line items are absent from published sources. The Hawker simplified IFE model and the Xcimer commercialization paper (both already ingested) are the most directly applicable fleet-wide sources. The laser $/J is the critical unknown that will dominate sensitivity analysis.
+
+Two technical uncertainties are deep enough to flag as model-level risks rather than data gaps: (1) target gain G=160 is an unvalidated extrapolation that could halve the power output if the actual gain tracks the CBET-mitigated rather than the BLF-claimed curve, and (2) the DEC system contributing 30% of electricity output has no hardware demonstration. Both uncertainties should be treated as sensitivity axes in the LCOE model rather than fixed parameters.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 4
-important_count: 2
-counting_method: "manual_prose_count"
+blocking_count: 8
+important_count: 5
+counting_method: "all_sections_deduplicated — 8 unique blocking gaps: target_gain_unvalidated, oec_laser_capital_cost, reactor_chamber_capital_cost, blanket_capital_cost, dec_capital_cost_and_efficiency, target_fabrication_cost, first_wall_lifetime, capacity_factor. 5 important: tbr_not_calculated, oec_mirror_supply_chain, kdp_crystal_supply_chain, bop_capital_cost, om_cost"
 section_coverage:
-  availability_of_data:       "Unknown"
-  system_function:            "Unknown"
-  subsystem_maturity:         "Unknown"
-  materials_supply_chain:     "Unknown"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  availability_of_data:       "Partial"
+  system_function:            "Partial"
+  subsystem_maturity:         "Partial"
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
