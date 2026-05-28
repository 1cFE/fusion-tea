# Diff: 10-large-scale-stellarator

**Generated:** 2026-05-22T09:59:25-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 0 | 2 | 2 |
| important_count  | 2 | 6 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
136:| CAS-level capital cost breakdown | proprietary | blocking | CDR contains this but not public; HELIAS analog or PyFECONS scaling can substitute with high uncertainty |
153:2. **ARIES-CS cost study (El-Guebaly et al., 2008)** — the ARIES compact stellarator study included CAS-level costing directly applicable as an analog. Part of the ARIES series in `knowledge/sources/aries_cost_account_documentation/` — check whether ARIES-CS specifically is covered, or ingest the primary Fusion Sci. Technol. 54 (2008) special issue. `not-yet-sourced`.
155:3. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — already ingested; should be read for CAS structure directly applicable to GIGA as a D-T MFE concept. Useful for BOP, O&M, indirect cost fractions.
161:6. **PyFECONS stellarator modules** (`/home/reid/PyFECONS`) — already available; the code has stellarator-specific modules. Running PyFECONS with GIGA parameters (18 m major radius, 3 GW, 40 coils, LTS+HTS) would generate a CAS-level cost estimate as a `derivable` baseline for all missing cost parameters.
169:The primary weakness is LCOE: the only GIGA-specific economic data point is a $15–18B FOAK cost estimate, with no CAS breakdown and no published efficiency or capacity factor. This is typical for pre-commercial fusion concepts. The recommended approach for section 5 is to (a) read `knowledge/sources/tea_dt_mfe_cost_analysis/` to apply CAS-level methodology, (b) run PyFECONS with GIGA parameters to generate a `derivable` baseline, and (c) use the Helios (Thea Energy) design as a capacity-factor and efficiency analog. All cost estimates should carry explicit uncertainty flags as `derivable from HELIAS/ARIES-CS analogs, not from GIGA-specific data`.
```

## Blocking-tier lines (baseline)

```
(none)
```

## Blocking-tier lines (new)

```
136:| CAS-level capital cost breakdown | proprietary | blocking | CDR contains this but not public; HELIAS analog or PyFECONS scaling can substitute with high uncertainty |
137:| O&M cost estimate ($/MWe/yr) | proprietary | blocking | No fusion stellarator O&M study specific to GIGA scale exists; ARIES-CS or TEA D-T MFE analogs needed |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/10-large-scale-stellarator.md	2026-05-22 09:21:13.844645357 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/10-large-scale-stellarator/gap_report.md	2026-05-22 09:59:25.273374522 -0700
@@ -1,45 +1,188 @@
-# Gap Assessment: Large-Scale Stellarator
+I have read all the key sources. Now I'll write the comprehensive gap assessment.
 
-Written to: `analyses/10-large-scale-stellarator/gap_report.md`
+---
+
+# Gap Assessment: Large-Scale Stellarator (D-T)
+
+## Overall Readiness
+**Rating**: Mostly Ready
+
+**Summary**: The Gauss Fusion GIGA concept has unusually strong public documentation relative to other private fusion companies: a 1,000-page CDR was completed in 2025 and independently reviewed, the HELIAS/HSR4/18 reactor heritage provides a decades-deep engineering baseline, and active industrial partnerships have generated specific technical disclosures on magnets and blanket development. Physics and engineering sections can be written to high quality. The main gap is economic: no CAS-level cost breakdown exists in the public domain, and the thermal conversion cycle/blanket type (which sets thermal efficiency) remains undisclosed. LCOE estimation requires significant reliance on HELIAS analogs and fleet-wide references rather than GIGA-specific data.
+
+---
+
+## Section Coverage
+
+### 1. Availability of Data
+**Coverage**: Good
+
+**Available**:
+- Gauss Fusion company disclosures across multiple sources: key plant parameters (3 GW thermal → 1 GW electric, 18 m major radius, 6 T on-axis, 12–13 T peak on coils, 1,500 m³ plasma volume, 1.7 m minor radius), roadmap to grid 2040–2045, and supply chain quantities (dossier, `gauss-fusion-technical-summary.md`)
+- HELIAS/HSR4/18 reactor study (IAEA, IPP, ~2001): predecessor design with nearly identical plasma parameters, quantified coil weights (~4,100 t SC coils), blanket options (HCPB 7,080 t; WCLL 14,450 t), 35% steam cycle efficiency, first wall area 2,500 m², cryostat volume 21,500 m³ (`helias-reactor-context.md`)
+- MT29 abstract on magnet system: 40 non-planar modular coils, conductor-in-plate design, demountable joints, dual LTS/HTS development strategy (`gauss-fusion-technical-summary.md`)
+- Tritium blanket partnerships: KIT/FZJ/IDOM finalizing TBB industrial design; Alsymex fabricating prototype sub-assemblies (`gauss-fusion-partnerships-2025.md`)
+- CDR completion and expert review by 13-person panel chaired by Zohm, January 2026 (`gauss-fusion-cdr-review-2026.md`)
+- HELIAS 5-B HCPB blanket structural study (Bongiovi et al. 2022): detailed mechanical design of bean-shaped blanket ring, TBR 1.3863, material specs (EUROFER 97, 8 MPa He coolant, W armour, Li₄SiO₄ breeder) (`helias-blanket-studies.md`)
+- Helios (Thea Energy) planar coil stellarator: compact analog with detailed power balance — 1.1 GW thermal, 390 MWe net, 40% thermal efficiency, 88% capacity factor — useful engineering analog (`arxiv-2512-08027v1.md`)
+
+**Missing**:
+- Full CDR content (behind download gate at gauss-fusion.com; covers detailed systems specs, fuel cycle, power conversion, waste)
+- Any published economic analysis of GIGA specifically
+
+**Gaps**:
+- CDR full content — `proprietary` — **important**: CDR would resolve blanket type, power conversion cycle, and many engineering uncertainties. The publicly available CDR executive summary is likely sufficient for the analysis but has not been captured.
+- Lack of independent academic or OSTI publications specifically on GIGA economics — `not-yet-sourced` — **nice-to-have**
+
+---
+
+### 2. Challenges in Capturing System Function
+**Coverage**: Partial
+
+**Available**:
+- Steady-state operation: explicitly confirmed as inherent stellarator advantage; no disruption risk, no current drive required (`dossier.md`, `gauss-fusion-technical-summary.md`)
+- Burning plasma regime: 3 GW fusion power implies deeply ignited operation; alpha particle heating dominates (~600 MW alphas vs. ~50–100 MW ECRH for startup/control) — well documented via HELIAS heritage
+- ECRH heating: not Gauss-confirmed but effectively certain from stellarator physics precedent and HELIAS heritage; startup only at reactor scale
+- Non-planar modular coil geometry: acknowledged as the primary engineering complexity driver — 3D coil shapes require tight tolerances; demountable joints at ~1 nΩ per joint are a novel innovation requiring prototype validation
+- Blanket accessibility: porthole-based maintenance (portholes ~2×6 m² between coils) identified in HSR4/18 studies as the baseline concept — more complex than tokamak sector maintenance
+- Divertor concept: island divertor concept (same as W7-X) documented in HELIAS studies; preliminary divertor heat load >10 MW/m² noted as critical issue in HSR4/18 (`helias-reactor-context.md`)
+
+**Missing**:
+- Power conversion cycle details (He/steam for HCPB, or higher-efficiency options for DCLL) — not disclosed publicly
+- Thermal-hydraulic system design for GIGA specifically
+- Plasma facing component material qualification under 3 GW neutron environment (first wall material choice unspecified beyond tungsten armour)
+
+**Gaps**:
+- Power conversion cycle type — `proprietary` — **important**: affects thermal efficiency (35% steam Rankine vs. 40%+ He-Brayton or DCLL-enabled cycles), which directly enters LCOE
+- Divertor heat load management strategy — `not-yet-sourced` — **important**: >10 MW/m² divertor load in HELIAS geometry is a known challenge with no published Gauss-specific solution
+- Plasma-facing component material specification — `derivable` from ITER/DEMO analogues — **nice-to-have**
+
+---
+
+### 3. Maturity of Key Subsystems and Components
+**Coverage**: Partial
+
+**Available**:
+- **Plasma physics**: W7-X experimental results directly validate QI stellarator confinement scaling. LGS empirical scaling predicts ignition in HSR4/18 without enhancement factor. Neoclassical transport <1% effective helical ripple confirmed. Alpha particle losses ~2.5% tolerable. TRL: 4–5 for plasma physics basis.
+- **Magnet system**: Conceptual design complete (CDR). Dual LTS/HTS conductor development underway with ENEA (HTS cables/joints) and ICAS (LTS cables), €9M + €10M BMBF grants. Demountable joint prototyping at KIT. Conductor-in-plate concept (novel). Tokamak Energy HTS collaboration signed Oct 2025. TRL: 3–4 (conductor level), lower for full coil assembly.
+- **Tritium breeding blanket**: KIT/FZJ industrial design ongoing; Alsymex prototype sub-assemblies contracted; HELIAS 5-B HCPB structural concept analyzed to heterogeneous detail. TBR 1.3863 demonstrated analytically for HELIAS 5-B HCPB. TRL: 2–3.
+- **Divertor**: Island divertor concept (W7-X heritage). W7-X has operated with island divertor. TRL: 4 for concept, 2 for reactor-scale implementation.
+- **Vacuum vessel**: 10,000 t steel VV identified in supply chain; 3D geometry well-documented. No specific VV manufacturing study found.
+- **CDR milestone**: Completed and independently reviewed (expert panel, Jan 2026) — equivalent to pre-Phase-B gate, significantly higher than most private fusion companies.
+
+**Missing**:
+- Formal TRL assessment per subsystem (not published)
+- Cryogenic system engineering (21,500 m³ cryostat)
+- ECRH system specifications and sourcing
+
+**Gaps**:
+- Published TRL matrix — `not-yet-sourced` — **nice-to-have**: subsystem TRLs can be inferred from engineering readiness but no structured assessment is public
+- Cryogenic system TRL — `derivable` from ITER/W7-X heritage — **nice-to-have**
+
+---
+
+### 4. Key Materials and Supply Chain Considerations
+**Coverage**: Partial
+
+**Available**:
+- Quantified supply chain requirements (from binding.energy commercial roadmap, confirmed in dossier):
+  - ~10,000 t vacuum vessel steel
+  - ~35,000 t superconducting coil assemblies
+  - ~75 t lithium inventory
+  - ~800 t LTS conductor + ~26 million meters HTS conductor
+  - Beryllium, tungsten, RAFM steel, cryostats, breeder blankets
+- EUROFER 97 RAFM steel confirmed as structural material for TBB (Bongiovi et al. 2022) — EU fusion supply chain baseline
+- Nb3Sn strongly inferred for LTS track from 12–13 T field requirement (NbTi limited to ~10 T) — established ITER supply chain analog
+- REBCO confirmed for HTS track (Tokamak Energy, ENEA partnerships)
+- Partnership with ASG Superconductors (founding industrial partner) — Italy's leading SC magnet manufacturer
+- Tungsten first wall armour (2 mm per blanket segment): standard fusion industry material
+
+**Missing**:
+- REBCO availability at 26 million meters scale — current global production is orders of magnitude below GIGA requirements and represents a market-creation challenge
+- 6Li enrichment requirements for lithium breeding (HCPB uses natural Li; DCLL studies cited 90% enriched ⁶Li)
+- Beryllium supply chain (neutron multiplier for HCPB concept) — limited global production, geopolitically concentrated
+- RAFM steel industrial production scale-up timeline
+
+**Gaps**:
+- REBCO supply chain bottleneck at scale — `not-yet-sourced` — **important**: global HTS production insufficient for GIGA at current volumes; supply chain roadmap not published
+- Beryllium availability (if HCPB selected) — `not-yet-sourced` — **important**: limited global production, high cost, geopolitical concentration (Kazakhstan/US)
+- Lithium enrichment strategy — `derivable` — **nice-to-have**: ⁶Li enrichment level determines cost and supply chain complexity
+
+---
+
+### 5. LCOE Parameter Extraction
+**Available Parameters**:
+| Parameter | Value/Range | Source | Confidence |
+|-----------|-------------|--------|------------|
+| Fusion power | 3,000 MW | Dossier, HELIAS heritage | high |
+| Gross thermal output | ~3,000 MW (neutron + alpha heat) | Dossier, CDR summary | high |
+| Net electric output | ~1,000 MWe | Dossier, CDR summary | high |
+| Gross thermal-to-electric efficiency | ~33% (implied: 3 GW → 1 GW) | Derived | medium |
+| First wall neutron load | 1 MW/m² | Dossier | high |
+| FW/blanket design life | 5 years | Dossier | high |
+| Magnet/VV design life | 40 years | Dossier | high |
+| Plant design life | 40 years (magnet-limited) | Dossier | medium |
+| FOAK estimated total cost | $15–18B | binding.energy commercial roadmap | low |
+| Plasma volume | 1,500 m³ | Dossier | high |
+| Coil mass | ~35,000 t total | Dossier supply chain | medium |
+| VV mass | ~10,000 t | Dossier supply chain | medium |
+| Operation mode | Steady-state (no pulsing) | Dossier | high |
+| Blanket lifetime analog (HELIAS) | 4.6–9 years (100–140 dpa limit) | helias-reactor-context.md | medium |
+| Thermal efficiency analog (Helios) | 40% (DCLL/higher-efficiency cycle) | arxiv-2512-08027v1.md | low (different architecture) |
+| Capacity factor analog (Helios) | 88% (biennial 84-day outage) | arxiv-2512-08027v1.md | low (different architecture) |
+
+**Missing Parameters**:
+| Parameter | Gap Type | Criticality | Notes |
+|-----------|----------|-------------|-------|
+| CAS-level capital cost breakdown | proprietary | blocking | CDR contains this but not public; HELIAS analog or PyFECONS scaling can substitute with high uncertainty |
+| O&M cost estimate ($/MWe/yr) | proprietary | blocking | No fusion stellarator O&M study specific to GIGA scale exists; ARIES-CS or TEA D-T MFE analogs needed |
+| Thermal conversion efficiency (specific cycle) | proprietary | important | 33% inferred from output ratio; actual depends on HCPB (≤35%) vs. DCLL (≥40%) blanket choice |
+| Capacity factor / planned outage schedule | proprietary | important | Steady-state favors high CF; no GIGA-specific availability study; Helios 88% is a reasonable analog |
+| Blanket replacement unit cost | not-yet-sourced | important | Mass quantities known (7,080–14,450 t); per-module replacement cost not quantified |
+| Tritium startup inventory cost | derivable | important | 1–2 kg T₂ startup (from Helios analog); market price ~$100–150M per kg; calculable |
+| ECRH system cost | not-yet-sourced | nice-to-have | Startup heating only (~10–50 MW at reactor scale); ITER ECRH cost analogs available |
+| Balance of plant cost (turbines, heat exchangers) | derivable | important | Standard plant engineering; depends on cycle type |
+| Cryogenic system cost | not-yet-sourced | important | 21,500 m³ cryostat at ~4 K; ITER cryoplant cost analog ($0.5–1B) applicable |
+| Decommissioning cost | derivable | nice-to-have | Similar activated waste inventory to equivalent tokamak (noted in helias-reactor-context.md) |
 
 ---
 
-## Overall Readiness: **Mostly Ready**
+## Source Recommendations
 
-The data is sufficient to write all five D1+ qualitative sections and build a credible first-pass LCOE model. Nothing is blocking. Here's the summary by section:
+1. **HELIAS reactor engineering studies (EUROfusion/KIT)** — multiple KIT publications exist on HELIAS 5-B systems engineering, costs, and neutronics. Search OSTI/FusionDB for "HELIAS reactor cost" or "HELIAS 5-B engineering". `not-yet-sourced` — likely to yield analog cost data at CAS level. *Unverified — confirm existence before searching.*
 
-### Section-by-Section
+2. **ARIES-CS cost study (El-Guebaly et al., 2008)** — the ARIES compact stellarator study included CAS-level costing directly applicable as an analog. Part of the ARIES series in `knowledge/sources/aries_cost_account_documentation/` — check whether ARIES-CS specifically is covered, or ingest the primary Fusion Sci. Technol. 54 (2008) special issue. `not-yet-sourced`.
 
-| Section | Coverage | Key Gap | Gap Type |
-|---|---|---|---|
-| 1. Availability of Data | Moderate | CDR content is gated; HSR4/18 cost study not captured | not-yet-sourced / proprietary |
-| 2. System Function Challenges | Partial | Power cycle type unknown; remote maintenance architecture not public | proprietary |
-| 3. Subsystem Maturity | Partial | TRL data is inferrable but no Gauss self-assessment exists | proprietary |
-| 4. Materials / Supply Chain | Good | HTS tape (26M m = 13–26× global annual production) is a clear bottleneck; He supply not analyzed | not-yet-sourced |
-| 5. LCOE Parameters | Partial | No CAS cost breakdown; €15–18B FOAK total is the only published figure | proprietary |
+3. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — already ingested; should be read for CAS structure directly applicable to GIGA as a D-T MFE concept. Useful for BOP, O&M, indirect cost fractions.
 
-### For the LCOE Model
-- **What you have**: Total FOAK cost (€15–18B), power output (3 GW → 1 GW), machine geometry, supply chain quantities (35,000T SC coils, 26M m HTS), 5-year blanket replacement cycle, 40-year magnet life, steady-state operation
-- **What you'll need to assume**: Blanket type (HCPB/DCLL bracket), power cycle efficiency (~33%), capacity factor (~85–90%), annual O&M from first-principles
+4. **Gauss Fusion CDR executive summary** — reportedly accessible at gauss-fusion.com/cdr-executive-summary (behind a download gate per dossier). If accessible: `proprietary` but gated, not classified — worth attempting download. Would resolve blanket type, power cycle, and key cost assumptions.
 
-### Two High-Value Quick Wins
-1. **Read the Bongiovì 2022 HCPB paper** (confirmed URL in dossier) — power cycle efficiency and blanket thermal-hydraulics
-2. **Read the CIEMAT DCLL paper** (confirmed URL in dossier) — alternative blanket TBR and thermal parameters
+5. **KIT/FZJ TBB publications 2025–2026** — Gauss Fusion's TBB partnerships are recent (announced 2025). Watch for KIT/FZJ conference papers (SOFT 2026, ISFNT 2025) on the GIGA-specific TBB design. `not-yet-sourced`.
 
-### Most Impactful `not-yet-sourced` Item
-**HSR4/18 cost study (Beidler et al. ~2001, *Nuclear Fusion* 41)** — almost certainly contains subsystem cost fractions for the direct GIGA predecessor. This is the difference between a single-number LCOE model and a decomposed parametric one.
+6. **PyFECONS stellarator modules** (`/home/reid/PyFECONS`) — already available; the code has stellarator-specific modules. Running PyFECONS with GIGA parameters (18 m major radius, 3 GW, 40 coils, LTS+HTS) would generate a CAS-level cost estimate as a `derivable` baseline for all missing cost parameters.
+
+---
+
+## Summary
+
+The available data is sufficient to write a high-quality D1+ analysis covering physics basis, engineering architecture, subsystem maturity, and supply chain considerations — these are well documented by the HELIAS lineage plus Gauss Fusion's own disclosures. The analysis can proceed without additional sources for sections 1–4.
+
+The primary weakness is LCOE: the only GIGA-specific economic data point is a $15–18B FOAK cost estimate, with no CAS breakdown and no published efficiency or capacity factor. This is typical for pre-commercial fusion concepts. The recommended approach for section 5 is to (a) read `knowledge/sources/tea_dt_mfe_cost_analysis/` to apply CAS-level methodology, (b) run PyFECONS with GIGA parameters to generate a `derivable` baseline, and (c) use the Helios (Thea Energy) design as a capacity-factor and efficiency analog. All cost estimates should carry explicit uncertainty flags as `derivable from HELIAS/ARIES-CS analogs, not from GIGA-specific data`.
+
+**Recommendation: Proceed to full analysis.** The physics, engineering, and maturity sections have sufficient source coverage for a D1+ quality write-up. The LCOE section requires explicit use of analog references and stated assumptions, but this is appropriate given the pre-commercial status of the concept.
+
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 0
-important_count: 2
-counting_method: "manual_prose_count"
+blocking_count: 2
+important_count: 6
+counting_method: "section_5_missing_parameters (CAS-level cost breakdown, O&M cost) as blocking; thermal efficiency, capacity factor, blanket replacement cost, TBB unit cost, cryogenic system cost, BOP cost as important; plus power conversion cycle type from section 2 merged with thermal efficiency"
 section_coverage:
-  availability_of_data:       "Unknown"
-  system_function:            "Unknown"
-  subsystem_maturity:         "Unknown"
-  materials_supply_chain:     "Unknown"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  availability_of_data:       "Good"
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
