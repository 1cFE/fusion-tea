# Diff: 38-particle-accelerator-driven-fusion

**Generated:** 2026-05-22T11:31:58-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 8 | 4 |
| important_count  | 4 | 5 | - |
| overall_rating   | Significant Gaps (for power-LCOE purposes) | Insufficient Data | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
75:- High-efficiency, high-current accelerator technology for power application — `not-yet-sourced` (accelerator R&D literature exists; `knowledge/sources/accelerators_for_inertial_fusion_energy_production/` may contain analogues for cost scaling, but applies to IFE driver-class machines, not low-energy electrostatic accelerators) — **important**
133:1. **Accelerator cost scaling analogues** — `knowledge/sources/accelerators_for_inertial_fusion_energy_production/` covers accelerator technologies for IFE drivers. May provide electrostatic/linac cost-per-Joule scaling that could be adapted, but applies to very different machine classes (high-energy induction linacs vs. low-energy electrostatic accelerators). Applicable as a rough order-of-magnitude baseline only; treat as `derivable` analogue, not direct data. (`not-yet-sourced` for SHINE-class machines specifically)
```

## Blocking-tier lines (baseline)

```
30:- No published beam current, electrical power, or production yield — `proprietary` — **blocking** (these define the cost-per-Ci denominator).
31:- No published facility capex — `proprietary` — **blocking**.
50:- **LCOE framework does not apply** — `truly-unknown` — **blocking** (for the power-generation comparison; the meaningful question is cost-per-Ci, which requires the proprietary economics).
51:- **Beam power consumption** — `proprietary` — **blocking** (the recirculating-power analog for an isotope plant; sets operating cost).
52:- **Mo-99 production yield** — `proprietary` — **blocking** (revenue driver; sets the economic case).
68:- **Path to net energy is non-existent** — `truly-unknown` — **blocking** (for the power-generation comparison; this concept's TRL maturity is irrelevant because the destination isn't power).
112:| Beam current (mA) | proprietary | blocking |
113:| Total facility electrical consumption | proprietary | blocking |
114:| Facility capital cost | proprietary | blocking |
115:| Mo-99 production yield | proprietary | blocking |
```

## Blocking-tier lines (new)

```
30:- No fusion power plant design or engineering basis exists in the public record — `truly-unknown` — **blocking**: the D1+ power analysis has no subject to analyze
31:- Phase 4 (fusion power) is a roadmap aspiration, not an engineered concept — `truly-unknown` — **blocking**: no public timeline, milestones, or technical targets disclosed
32:- NRC/NNSA regulatory documents cover the neutron-source/isotope facility only, not a power-generating configuration — `proprietary` (if studied internally) — **blocking**
51:- No energy conversion pathway described — `truly-unknown` — **blocking**: cannot model power output, efficiency, or LCOE without this
52:- Accelerator wall-plug efficiency at power-relevant beam currents — `not-yet-sourced` (accelerator physics literature exists; SHINE-specific data may be proprietary) — **blocking**: dominates recirculating power fraction
53:- No physics basis for net energy gain published — `truly-unknown` for this configuration — **blocking**: beam-target fusion is inherently below breakeven without an amplification mechanism; no public description of the amplification pathway for power
118:| Net electric power output | truly-unknown | blocking | No power plant design exists |
119:| Capital cost (any subsystem) for power configuration | truly-unknown | blocking | Only neutron-source facility costs exist; not public |
120:| Accelerator wall-plug efficiency at power scale | proprietary/not-yet-sourced | blocking | Dominates recirculating power fraction; SHINE-specific data not public |
121:| Energy conversion efficiency (thermal cycle) | truly-unknown | blocking | No thermal cycle described or designed |
122:| Capacity factor / availability | truly-unknown | blocking | No power plant to assess; neutron-source availability not public |
123:| Q-value / fusion energy gain | truly-unknown | blocking | Beam-target is below breakeven without amplification; no pathway described |
124:| O&M cost | truly-unknown | blocking | Neutron-source O&M not public; power application nonexistent |
125:| Fuel cost (tritium at power scale) | not-yet-sourced | blocking | General tritium economics exist in literature; SHINE-specific not public |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/38-particle-accelerator-driven-fusion.md	2026-05-22 09:21:13.890136980 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/38-particle-accelerator-driven-fusion/gap_report.md	2026-05-22 11:31:58.950078767 -0700
@@ -1,157 +1,170 @@
-# Gap Assessment: Particle Accelerator-Driven Fusion (SHINE Technologies)
+Now I have enough to write the full gap assessment.
+
+# Gap Assessment: Particle Accelerator-Driven Fusion (D-T)
 
 ## Overall Readiness
-**Rating**: Significant Gaps (for power-LCOE purposes)
+**Rating**: Insufficient Data
 
-**Summary**: SHINE is unique in the catalog: the only **commercially operating** fusion system, with a mature commercial product line (Mo-99, Lu-177, FLARE neutron services) and NRC licensing in place. Technical *concept* documentation is good (peer-reviewed Piefer 2011, NRC license documents, Wikipedia, company FLARE materials). However, this is a commercial radioisotope producer, not a power plant — and beam-target D-T fusion has a hard physics ceiling at Q ≈ 10⁻³, two-to-three orders of magnitude below break-even. The standard LCOE framework does not apply: SHINE produces no electricity and has no design pathway to net power output. The correct economic model is cost-per-Curie of medical isotope, not $/kWh. For the catalog's power-generation TEA comparison, the LCOE result is formally ∞ — SHINE is categorically outside the power-generation competition. For its actual isotope-production business model, operational economics (beam current, electrical power consumption, facility capex, Mo-99 yield) are entirely proprietary commercial information.
+**Summary**: SHINE Technologies operates a commercially-demonstrated beam-target D-T neutron source for medical isotope production and materials testing — it is explicitly not a power-generating system. Phase 4 (fusion power) is a stated long-horizon goal with no engineered plant design, no energy conversion pathway, and no public cost or performance parameters relevant to electricity generation. All five D1+ sections depend on a power-plant configuration that does not yet exist in the public record. The dossier is complete and high-confidence for what the concept *is*, but the subject of the analysis (a fusion power plant) has no engineering basis to assess.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Good (technical concept) / Poor (operational economics)
+
+**Coverage**: Poor
 
 **Available**:
-- Piefer et al. 2011 (ANL Mo-99 proceedings): peer-reviewed description of beam-target D-T architecture for isotope production.
-- SHINE technology overview: FLARE specifications — 5×10¹³ D-T reactions/s, ≤300 kV beam voltage, 14.1 MeV neutrons, continuous steady-state operation.
-- NRC licensing documents (ML13172A262, ML15258A372) publicly accessible.
-- Wikipedia entry covering accelerator architecture, subcritical LEU assembly, NRC licensing history.
-- LIBRTI commercial deployment with UKAEA (2024 press release).
+- Comprehensive characterization of SHINE's operational neutron-source system: beam-target geometry, 300 kV electrostatic acceleration, D-T fuel cycle, steady-state operation, ~5×10¹³ fusions/second, commercial deployment in Chrysalis for Mo-99/Lu-177 production (dossier; `shine-technology-overview.md`)
+- Company four-phase roadmap: Phase 1 (inspection) → Phase 2 (medical isotopes, operational) → Phase 3 (spent-fuel recycling, R&D) → Phase 4 (fusion power, long-horizon goal) (`shine-accelerator-driven-fusion-overview.md`)
+- NRC licensing documents (NRC ML13172A262, ML15258A372) covering the Chrysalis facility, subcritical LEU assembly, and neutron-source design
+- Piefer et al. (ANL Mo-99 proceedings, 2011) on beam-target subcritical isotope production
 
 **Missing**:
-- Beam current (mA) — SHINE has not publicly disclosed.
-- Total facility electrical power consumption.
-- Mo-99 production yield per beam-hour.
-- Facility capital cost.
-- OPEX breakdown.
+- Any public engineering study, design concept, or technical basis document for a beam-target D-T *power plant*
+- Stated power output targets, Q-value goals, or physics basis for net energy gain from this architecture
+- Company technical disclosures on accelerator efficiency, tritium consumption rate at power-relevant scale, or pathway to electricity generation
 
 **Gaps**:
-- No published beam current, electrical power, or production yield — `proprietary` — **blocking** (these define the cost-per-Ci denominator).
-- No published facility capex — `proprietary` — **blocking**.
-- No independent TEA of accelerator-driven fusion as a power concept (academic literature only confirms the Q ceiling) — `derivable` — nice-to-have.
+- No fusion power plant design or engineering basis exists in the public record — `truly-unknown` — **blocking**: the D1+ power analysis has no subject to analyze
+- Phase 4 (fusion power) is a roadmap aspiration, not an engineered concept — `truly-unknown` — **blocking**: no public timeline, milestones, or technical targets disclosed
+- NRC/NNSA regulatory documents cover the neutron-source/isotope facility only, not a power-generating configuration — `proprietary` (if studied internally) — **blocking**
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good (physics is well-understood) / Poor (economics)
+
+**Coverage**: Poor
 
 **Available**:
-- Beam-target D-T physics is thoroughly characterized: thick-target fusion probability per deuteron, Coulomb-scattering stopping range, D-T cross-section peak near 120 keV CM (~240 keV lab).
-- Physics-derived effective Q in the range 10⁻³–10⁻² is robust to beam-current optimization (Q is bounded by the integrated fusion-vs-scattering cross-section ratio, not by current).
-- Operational reality: SHINE is a net electricity *consumer* on grid power, by design.
+- System function as a neutron source is well-understood: ion acceleration → beam-on-gas target → D-T neutrons → fission-driven isotope production. This chain is commercially demonstrated.
+- Beam-target fusion physics is straightforward (no plasma confinement, no instability physics): fusion cross-section at 300 kV, neutron yield as function of beam power, target gas density. Well-established nuclear physics.
 
 **Missing**:
-- Annual electrical operating cost (depends on undisclosed beam power consumption).
-- Operating economics under the cost-per-Ci framework.
-- Mo-99 / Lu-177 revenue model details (proprietary commercial).
+- Energy conversion pathway for a power plant: no blanket design, no thermal cycle, no electricity generation mechanism described anywhere
+- Recirculating power fraction: accelerator wall-plug efficiency is the dominant cost/performance lever for beam-target power, and no data exists for a power-relevant system
+- Q-value or "fusion gain" concept for this architecture: unlike plasma-based concepts, "Q" for beam-target requires accounting for accelerator efficiency separately — no treatment of this found
+- Subcritical fission amplifier design (if retained for power): whether the LEU subcritical assembly would be adapted for power extraction is entirely unstated
 
 **Gaps**:
-- **LCOE framework does not apply** — `truly-unknown` — **blocking** (for the power-generation comparison; the meaningful question is cost-per-Ci, which requires the proprietary economics).
-- **Beam power consumption** — `proprietary` — **blocking** (the recirculating-power analog for an isotope plant; sets operating cost).
-- **Mo-99 production yield** — `proprietary` — **blocking** (revenue driver; sets the economic case).
-- **NRC tritium possession limit and procurement logistics** — `proprietary / NRC docket` — important (binds scalability more than tritium unit cost).
+- No energy conversion pathway described — `truly-unknown` — **blocking**: cannot model power output, efficiency, or LCOE without this
+- Accelerator wall-plug efficiency at power-relevant beam currents — `not-yet-sourced` (accelerator physics literature exists; SHINE-specific data may be proprietary) — **blocking**: dominates recirculating power fraction
+- No physics basis for net energy gain published — `truly-unknown` for this configuration — **blocking**: beam-target fusion is inherently below breakeven without an amplification mechanism; no public description of the amplification pathway for power
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Good
+
+**Coverage**: Partial (neutron-source application only)
 
 **Available**:
-- TRL assessments by subsystem: compact linear accelerator at ≤300 kV TRL 9 (commercially operating, industrial-class device); tritium gas target system TRL 9 (operating); subcritical LEU assembly TRL 8–9 (NRC-licensed); Mo-99 / Lu-177 extraction TRL 7–8 (operating since 2019, expanded with FLARE).
-- FLARE described as "world's most powerful continuous fusion neutron system" (SHINE press release, 2024).
+- **Particle accelerator (electrostatic, ~300 kV)**: commercially deployed and demonstrated at SHINE Chrysalis; TRL 8–9 for neutron-source application
+- **Beam-on-gas target assembly**: commercially demonstrated; TRL 8–9 for Mo-99 production context
+- **Subcritical LEU fission assembly**: NRC-licensed and operational; TRL 7–8
+- **Steady-state operation**: demonstrated in commercial facility
+- **Tritium handling**: operational at neutron-source scale (procurement-based, not bred)
 
 **Missing**:
-- Scaling pathway to power-generation TRL: nothing. No published design study; this isn't a TRL gap, it's a categorical mismatch (beam-target D-T cannot reach Q ≥ 1 by physics).
+- TRL for any power-generation-relevant subsystem: breeding blanket, thermal conversion cycle, tritium breeding/fuel cycle at power scale, high-efficiency driver at power-relevant beam currents
+- Accelerator scaling: current SHINE system is a relatively small machine; a power-producing version would require dramatically higher beam current or a fundamentally different amplification scheme — no data
+- Materials performance under sustained high-flux 14 MeV neutron irradiation (relevant for accelerator components and any surrounding structure at power scale)
 
 **Gaps**:
-- **Path to net energy is non-existent** — `truly-unknown` — **blocking** (for the power-generation comparison; this concept's TRL maturity is irrelevant because the destination isn't power).
-- Lu-177 production yield and process maturity — `proprietary` — important.
+- Power-generation subsystems are at TRL 1–2 at best (concept only, no design) — `truly-unknown` — **important**: TRL assessment is possible but only at the lowest levels
+- High-efficiency, high-current accelerator technology for power application — `not-yet-sourced` (accelerator R&D literature exists; `knowledge/sources/accelerators_for_inertial_fusion_energy_production/` may contain analogues for cost scaling, but applies to IFE driver-class machines, not low-energy electrostatic accelerators) — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Good
+
+**Coverage**: Partial
 
 **Available**:
-- Tritium consumption: ~8 mg/year (derived from 5×10¹³ reactions/s rate) — operationally negligible (~$280/yr at $35,000/g). NRC possession limit is the binding constraint, not unit cost.
-- Low-enriched uranium (LEU) supply: narrow but adequate qualified-supplier base (ConverDyn, Tenex) under NNSA oversight.
-- Deuterium gas: commercial industrial supply, no constraint.
-- Accelerator components (vacuum, ion sources, HV power supplies, beam optics): mature industrial supply (NEC, HVEE, Excelis).
-- No HTS / beryllium / FLiBe required — SHINE is supply-chain-simple by virtue of not attempting plasma confinement.
+- **Tritium supply**: SHINE procures tritium externally (no breeding); this is documented as the current operational model. Tritium is produced at CANDU reactors (primarily Darlington/Pickering in Canada via SRB Technologies, and US DOE/Savannah River).
+- **Deuterium supply**: abundant; no supply constraint
+- **LEU supply**: commercially available for the subcritical assembly
+- **Accelerator components**: mature industrial supply chain for electrostatic accelerators at SHINE's operating scale
 
 **Missing**:
-- Tritium possession limit at FLARE-scale operation (under NRC license amendments).
+- Tritium supply chain at power-plant scale: a fusion power plant would require orders-of-magnitude more tritium than the current neutron-source operation; no analysis of supply feasibility at that scale
+- Breeding blanket materials: no blanket design exists, so no material specification is possible
+- High-current accelerator components at power scale: potential supply chain constraints for high-power ion sources, beam optics, and target assemblies are unstudied
+- First-wall/structural materials for sustained 14 MeV neutron flux: relevant to any power-extracting configuration but entirely unaddressed
 
 **Gaps**:
-- LEU supply chain geopolitical risk (Russian supply chain) — `derivable` from NNSA reports — nice-to-have.
-- Tritium possession limit at FLARE scale — `proprietary / NRC docket` — important.
+- Tritium supply and breeding strategy for power scale — `not-yet-sourced` (general tritium supply literature exists; SHINE-specific analysis does not) — **important**
+- Materials selection for power-extracting configuration — `truly-unknown` (no design exists) — **important**
+- Supply chain for high-current accelerator technology at power scale — `not-yet-sourced` — **nice-to-have** (premature until a design exists)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Framing note**: Standard LCOE doesn't apply (SHINE is non-power). The available table below is what would be extractable *if* the catalog framework were adapted to cost-per-Ci for medical isotope production.
 
-**Available Parameters**:
+**Coverage**: Poor
 
-| Parameter | Value | Source | Confidence |
-|---|---|---|---|
-| D-T reaction rate | 5 × 10¹³ /s | SHINE FLARE materials | high |
-| Beam voltage | ≤ 300 kV | SHINE / dossier | high |
-| Neutron energy | 14.1 MeV | physics | high |
-| Operation mode | Steady-state continuous | SHINE | high |
-| Effective Q | ~10⁻³–10⁻² | thick-target physics | medium |
-| Fusion power (derived) | ~141 W | derived from reaction rate | high |
-| Tritium consumption | ~8 mg/yr | derived | medium |
-| Net electrical output | 0 kWe | dossier (by design) | high |
+**Available Parameters**:
+| Parameter | Value/Range | Source | Confidence |
+|-----------|-------------|--------|------------|
+| Operation mode | Steady-state (continuous) | dossier; SHINE press releases | high |
+| Fuel type | D-T (deuterium beam on tritium gas) | dossier | high |
+| Neutron output | ~5×10¹³ fusions/sec (current system) | `shine-technology-overview.md` | medium |
+| Accelerator voltage | ~300 kV | dossier; `shine-technology-overview.md` | high |
+| Energy product | Neutrons (not electricity) | dossier | high |
 
 **Missing Parameters**:
-
-| Parameter | Gap Type | Criticality |
-|---|---|---|
-| Beam current (mA) | proprietary | blocking |
-| Total facility electrical consumption | proprietary | blocking |
-| Facility capital cost | proprietary | blocking |
-| Mo-99 production yield | proprietary | blocking |
-| Capacity factor / beam-on-time | proprietary | important |
-| OPEX breakdown | proprietary | important |
-| Lu-177 production rate | proprietary | important |
-| Tritium NRC possession limit | proprietary / NRC | important |
-| FLARE service pricing | proprietary | nice-to-have |
+| Parameter | Gap Type | Criticality | Notes |
+|-----------|----------|-------------|-------|
+| Net electric power output | truly-unknown | blocking | No power plant design exists |
+| Capital cost (any subsystem) for power configuration | truly-unknown | blocking | Only neutron-source facility costs exist; not public |
+| Accelerator wall-plug efficiency at power scale | proprietary/not-yet-sourced | blocking | Dominates recirculating power fraction; SHINE-specific data not public |
+| Energy conversion efficiency (thermal cycle) | truly-unknown | blocking | No thermal cycle described or designed |
+| Capacity factor / availability | truly-unknown | blocking | No power plant to assess; neutron-source availability not public |
+| Q-value / fusion energy gain | truly-unknown | blocking | Beam-target is below breakeven without amplification; no pathway described |
+| O&M cost | truly-unknown | blocking | Neutron-source O&M not public; power application nonexistent |
+| Fuel cost (tritium at power scale) | not-yet-sourced | blocking | General tritium economics exist in literature; SHINE-specific not public |
+| Plant footprint / unit size | truly-unknown | important | No power plant design |
+| Decommissioning cost | truly-unknown | nice-to-have | — |
 
 ---
 
 ## Source Recommendations
 
-1. **NRC public docket** (ML13172A262, ML15258A372 plus subsequent amendments) — may contain operational beam parameters, possession limits, and updated facility descriptions.
-2. **Piefer et al. 2011 full text** (ANL Mo-99 symposium proceedings, not yet directly extracted) — may contain beam current and neutron yield specifications.
-3. **NorthStar Medical Radioisotopes / SHINE public filings** — comparable non-reactor Mo-99 producer; facility capital cost benchmark of ~$30–150M is the publicly stated range.
-4. **CNSC (Canadian NRC) NRU operational records** for analog isotope-plant OPEX structure.
-5. **SHINE SEC filings or commercial disclosures** if/when the company IPOs or issues public financial statements.
+1. **Accelerator cost scaling analogues** — `knowledge/sources/accelerators_for_inertial_fusion_energy_production/` covers accelerator technologies for IFE drivers. May provide electrostatic/linac cost-per-Joule scaling that could be adapted, but applies to very different machine classes (high-energy induction linacs vs. low-energy electrostatic accelerators). Applicable as a rough order-of-magnitude baseline only; treat as `derivable` analogue, not direct data. (`not-yet-sourced` for SHINE-class machines specifically)
+
+2. **IEC/fusor power economics literature** — search OSTI and Google Scholar for "accelerator-driven fusion power economics," "beam-target fusion power plant," "electrostatic accelerator fusion economics." These searches are likely to return sparse results; beam-target power is essentially unstudied. Flag as `unverified — confirm existence before searching`.
+
+3. **SHINE investor/regulatory filings** — NRC license application documents (already partially sourced: ML13172A262, ML15258A372) may contain facility cost data for the Chrysalis neutron-source plant. Would not cover a future power plant but could establish cost analogues for the accelerator subsystem. Likely to be heavily redacted. (`proprietary` for power configuration; `not-yet-sourced` for facility costs)
+
+4. **Phoenix Nuclear Labs technical papers** — SHINE spun out of Phoenix Nuclear Labs; PNL has published on compact neutron generator physics and efficiency. Search OSTI/Google Scholar for Piefer et al. and related Phoenix/SHINE publications. May yield beam current, target efficiency, and component cost data. `unverified — confirm existence before searching`.
+
+5. **Tritium supply economics at scale** — general fusion tritium supply literature (e.g., Kovari et al. tritium breeding studies, ITER Organization tritium assessments) can provide supply-chain cost analogues. Not SHINE-specific but addresses a blocking gap for any D-T power concept. `not-yet-sourced` — likely findable in fusion fuel cycle literature.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis**: No — but for a categorical reason, not a data-availability one.
+**Do not proceed to full LCOE/power analysis without additional sourcing — and note that the fundamental barrier is not a sourcing gap but a design-existence gap.**
+
+SHINE Technologies has built a real, commercially-operational beam-target D-T neutron source, and that system is well-characterized. However, the concept as a *fusion power plant* does not exist in any engineered form. Phase 4 (fusion power) is a long-horizon roadmap item with no public design, no performance targets, no cost estimates, and no energy conversion pathway. The concept cannot be given a meaningful LCOE analysis in its current state.
 
-SHINE is the only catalog concept that does not aim for power generation. Beam-target D-T fusion has a hard physics ceiling at Q ~ 10⁻²; no engineering optimization changes the fundamental ratio. The correct framework for SHINE is cost-per-Ci of medical isotope, not $/kWh. The catalog should disposition SHINE as the "validated lower bound on D-T fusion economics at Q < 1" — useful as a calibration point but not a power-generation competitor. For the standard LCOE comparison, the disposition is LCOE = ∞ (categorical disqualification), and the framework's CrossAxisSanity tests already exclude it correctly via the Technical Feasibility floor (1.0, no-data) and the absence of any net-power architecture.
+The most useful analysis available is a qualitative assessment documenting: (a) what SHINE has demonstrated and at what TRL, (b) the fundamental physics barrier (beam-target fusion is inherently sub-breakeven without an amplification mechanism), (c) SHINE's stated pathway and what would be required to overcome it, and (d) a comparison to analogous accelerator-based concepts. A quantitative D1+ analysis with LCOE parameter extraction is not supported by available data.
 
-Were the catalog ever expanded to include "useful neutron flux" or "medical isotope production" as additional evaluation axes, SHINE would likely rank highly. That work is out of scope for the current power-LCOE focus.
+**Recommendation**: Flag this concept as "neutron source / pre-power-plant" in the taxonomy and defer LCOE modeling until a power-plant design is published. If a qualitative section is still desired, it can be written against the neutron-source system with explicit caveats on the power-generation extrapolation.
 
 ---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps (for power-LCOE purposes)"
-blocking_count: 4
-important_count: 4
-counting_method: "section_5_missing_parameters"
+overall_rating: "Insufficient Data"
+blocking_count: 8
+important_count: 5
+counting_method: "section_5_missing_parameters_blocking_rows_plus_unique_blocking_gaps_from_sections_1_2_not_duplicated_in_section_5"
 section_coverage:
-  availability_of_data:       "Good (technical concept) / Poor (operational economics)"
-  system_function:            "Good (physics is well-understood) / Poor (economics)"
-  subsystem_maturity:         "Good"
-  materials_supply_chain:     "Good"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  availability_of_data:       "Poor"
+  system_function:            "Poor"
+  subsystem_maturity:         "Partial"
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Poor"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
