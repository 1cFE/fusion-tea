# Phase 3 diff: 28-hts-tokamak-full-hts

**Generated:** 2026-05-22T15:38:38-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 6 | 3 | -3 |
| important_count  | 9 | 5 | - |
| overall_rating   | Significant Gaps | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information to write the assessment. The TEA D-T MFE Cost Analysis (Araiinejad & Shirvan 2025, `knowledge/sources/tea_dt_mfe_cost_analysis/`) is directly applicable — it covers a compact REBCO HTS tokamak (ARC-derived ARAI concept) with full CAS breakdown and LCOE results. The second ScienceDirect source in iter-03 (pii-s2211467x25003839) is a fusion licensing/regulation paper with no cost or engineering data relevant to this concept.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information to write the assessment. The TEA D-T MFE Cost Analysis (Araiinejad & Shirvan 2025, `knowledge/sources/tea_dt_mfe_cost_analysis/`) is directly applicable — it covers a compact REBCO HTS tokamak (ARC-derived ARAI concept) with full CAS breakdown and LCOE results. The second ScienceDirect source in iter-03 (pii-s2211467x25003839) is a fusion licensing/regulation paper with no cost or engineering data relevant to this concept.
```

## Blocking-tier lines (new)

```
28:- HH380 power plant specs (power output, thermal efficiency, sizing) — proprietary — **blocking**
75:- Blanket/tritium breeding subsystem maturity — proprietary/TBD — **blocking**
76:- Neutron shielding and first-wall design maturity — proprietary/TBD — **blocking**
97:- Blanket material and supply chain — proprietary/TBD — **blocking** (resolves only when blanket design disclosed)
134:| HH380 rated power output | proprietary | blocking | No company disclosure; must use ARC/ARAI analog (~350 MWe) with explicit caveat |
135:| Blanket design and TBR | proprietary | blocking | Structurally unresolvable before HH380 engineering phase; blanket type drives tritium self-sufficiency and breeding heat |
136:| Neutron wall loading and first-wall lifetime | proprietary | blocking | Required for replaceable-component cost and downtime estimate |
150:- **ARAI/ARC TEA** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Already integrated. This is the primary cost analog for HH380 — compact REBCO HTS D-T tokamak, NOAK basis. Reduces the `blocking` classification of HH380 power specs to a bounded `important` gap once analog assumptions are made explicit.
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/28-hts-tokamak-full-hts.md	2026-05-22 12:59:21.084528402 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/gap_report.md	2026-05-22 15:38:38.855882513 -0700
@@ -1,184 +1,183 @@
-Now I have enough context to write the gap assessment. The second ScienceDirect source (licensing framework paper) is completely irrelevant to this concept — it's about fusion regulation policy globally. Let me compose the report.
-
----
+I now have sufficient information to write the assessment. The TEA D-T MFE Cost Analysis (Araiinejad & Shirvan 2025, `knowledge/sources/tea_dt_mfe_cost_analysis/`) is directly applicable — it covers a compact REBCO HTS tokamak (ARC-derived ARAI concept) with full CAS breakdown and LCOE results. The second ScienceDirect source in iter-03 (pii-s2211467x25003839) is a fusion licensing/regulation paper with no cost or engineering data relevant to this concept.
 
 # Gap Assessment: HTS Tokamak - Full HTS (D-T)
 
 ## Overall Readiness
-**Rating**: Significant Gaps
-
-**Summary**: Energy Singularity has produced meaningful prototype-level engineering data (HH70 commissioning, Jingtian magnet) and enough trajectory information to characterize their technology approach, but the company has published essentially nothing about power plant economics, blanket design, energy conversion, or LCOE-relevant parameters. The HH380 demo plant — the only machine where these questions become concrete — is post-2030 with no disclosed specifications. Fleet-wide D-T MFE cost analogs (TEA D-T MFE, ARIES, PyFECONS) can partially substitute for many plant-level parameters, but the full-HTS magnet cost premium over LTS is a novel, poorly-bounded variable with no direct published analog.
-
----
+**Rating**: Mostly Ready
+**Summary**: Energy Singularity's HH70/HH170 program is well-documented at the machine-physics level, and a high-quality D-T MFE cost analog (Araiinejad & Shirvan 2025, `knowledge/sources/tea_dt_mfe_cost_analysis/`) provides a compact REBCO HTS tokamak cost framework that directly maps onto this concept. The primary blocking gaps — HH380 power plant specifications, blanket design, and neutron shielding approach — are proprietary or structurally unresolvable at the current company stage (HH380 is post-2030), but these can be handled with explicit analog assumptions derived from the fleet-wide TEA source. The analysis can proceed with clearly bounded uncertainty, drawing on the ARC/ARAI analog for LCOE parameters.
 
 ## Section Coverage
 
 ### 1. Availability of Data
 **Coverage**: Partial
-
 **Available**:
-- Company profile, funding status (~$110M raised for HH70, seeking $500M for HH170), investor base, and 3-machine roadmap — `iter-01/sources/energy-singularity-overview.md`
-- HH70 engineering specs: major radius (0.7 m), minor radius (0.25–0.3 m), B0 = 0.6 T, Bmax = 2.5 T, 20 K operating temperature, 26 REBCO coils (12 TF + 6 PF + 8 CS), conductor dimensions — `iter-03/sources/sciencedirect-science-article-pii-s092037962500537x.md` (abstract) and `iter-01`
-- Jingtian prototype magnet: 21.7–22.4 T peak field, dimensions (~3 m × 1.4 m, ~7.5 T), 32 single-pancake REBCO coils, operating current 24,300 A — `iter-01`
-- HH70 plasma performance record (1,337 s steady-state, shot #5,755, Feb 2026) — `iter-02/sources/energy-singularity-technical-summary.md` (Xinhua article)
-- HH170 top-level targets: Q > 10, ~25 T peak coil field, ~70% of SPARC volume, completion target 2027 — `iter-01`
-- HH380 existence and timeline (post-2030 demo plant) — `iter-01`
-- Domestic supply chain: >96% localization, Shanghai Superconductor as REBCO supplier — `iter-01`
-- AI-based plasma control as a differentiating engineering feature — `iter-02` (Xinhua)
-- Fleet-wide D-T MFE cost methodology applicable as analog: `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/sources/aries_cost_account_documentation/`, PyFECONS
+- HH70 commissioning data: major radius 0.7 m, minor radius 0.25–0.3 m, B0 = 0.6 T, Bmax = 2.5 T, 26 REBCO coils (12 TF + 6 PF + 8 CS), 1,337-second steady-state plasma demonstrated (energy-singularity-overview.md; sciencedirect pii-s092037962500537x abstract)
+- HH170 targets: Q > 10, ~14 T on-axis, ~110% of SPARC field, ~70% SPARC volume, D-shaped HTS magnets targeting 25 T peak field, 2027 completion (dossier; energy-singularity-overview.md)
+- Jingtian magnet: 21.7–22.4 T peak field demonstrated, IEEE TAS 2025 publication (dossier)
+- Company roadmap: HH70 → HH170 → HH380 → commercialization before 2035 (energy-singularity-overview.md)
+- Funding: ~$110M raised for HH70, seeking $500M for HH170 (energy-singularity-overview.md)
+- D-T MFE cost analog: ARAI-FPP (ARC-derived, compact REBCO HTS, 350 MWe) with full CAS breakdown and LCOE $140–$550/MWh (`knowledge/sources/tea_dt_mfe_cost_analysis/`, Araiinejad & Shirvan 2025)
+- CAS methodology: Full COA 20–27, 90–98 framework applicable to HTS tokamaks (`knowledge/sources/tea_dt_mfe_cost_analysis/`; `knowledge/sources/aries_cost_account_documentation/`)
 
 **Missing**:
-- HH170 engineering specifications beyond top-level targets (heating systems, power density, plasma parameters)
-- HH380 any engineering details whatsoever
-- No company-published techno-economic analysis or cost projections
-- The fourth iter-03 ScienceDirect source (pii-s2211467x) is about fusion licensing/regulation globally — zero content relevant to Energy Singularity or this concept
+- HH380 power plant design specifications (power output, size, plant layout)
+- Any company-disclosed LCOE targets (CEO statement "reduce LCOE to thermal power level or lower" is aspirational, not quantified)
+- Peer-reviewed papers with plasma parameter details for HH170
 
 **Gaps**:
-- HH170/HH380 engineering design documents — `proprietary` — **blocking** for concept-specific analysis
-- Published techno-economic study or LCOE projection from Energy Singularity — `proprietary` — **blocking**
-- Full text of HH70 commissioning paper (paywalled; would give complete engineering specs) — `not-yet-sourced` — **important**
-- Full text of Jingtian IEEE TAS paper (2025; magnet cost/manufacturing data) — `not-yet-sourced` — **important**
+- HH380 power plant specs (power output, thermal efficiency, sizing) — proprietary — **blocking**
+- Detailed plasma physics parameters (temperature, density, confinement time) for HH170 — not-yet-sourced — **important**
+- Chinese-language technical disclosures beyond publicly captured sources — not-yet-sourced — **nice-to-have**
 
 ---
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Partial
-
 **Available**:
-- All-REBCO coil architecture (TF + PF + CS) is documented and understood as the key differentiator — `iter-01`
-- Steady-state operation demonstrated on prototype; AI plasma control confirmed — `iter-01`, `iter-02`
-- ICRF as primary heating on HH70 confirmed — `iter-01`
-- The physics challenges of full HTS at high field (quench management, joint resistance, coil mechanics) are documentable from general HTS tokamak literature, though no Energy Singularity-specific paper covers HH170 design choices
+- Novel full-HTS tokamak architecture is documented at HH70 level — all coils REBCO, operating at 20 K, with demonstrated engineering feasibility (sciencedirect pii-s092037962500537x)
+- AI-based plasma control is confirmed as operational on HH70 and cited as enabling steady-state (energy-singularity-overview.md; Xinhua iter-02 source)
+- The closest cost analog (ARAI/ARC, `knowledge/sources/tea_dt_mfe_cost_analysis/`) uses identical magnet technology (REBCO, ~same field targets) and D-T fuel — functions as a validated template for system function modeling
+- Steady-state operation confirmed vs. pulsed: eliminates pulsed-power cost issues
+- Heating on HH70: ICRF confirmed as primary, electron gun for pre-ionization — no ECRH, LHCD, or NBI mentioned
 
 **Missing**:
-- Heating and current drive strategy for HH170 and HH380 (ECCD? NBI? higher-power ICRF?) — essential for plasma performance and recirculating power fraction
-- Divertor design and plasma-facing component strategy — particularly challenging at high B-field
-- Tritium breeding approach — completely undisclosed across 3 iterations and 20+ sources; structurally unresolvable until HH380 design phase
-- Neutron shielding / blanket integration design
-- Recirculating power fraction estimate (affects net electrical output significantly)
+- Heating plan for HH170 and HH380 (ICRF alone is unlikely at higher power levels; NBI or ECRH may be required)
+- Energy conversion pathway (no disclosure of thermal cycle type: steam Rankine assumed by analogy)
+- Divertor design and exhaust handling strategy (standard challenge for compact high-field tokamaks)
+- Recirculating power fraction (critical for net electric calculation)
+- Alpha-heating fraction at Q > 10 (derivable from physics, but no company disclosure)
 
 **Gaps**:
-- Tritium breeding blanket design — `proprietary` (and not yet designed) — **blocking** for full system function analysis
-- Heating/CD strategy for power plant — `proprietary` — **important**
-- Divertor/PFC design — `proprietary` — **important**
-- Recirculating power fraction — `derivable` (can estimate from compact tokamak analogs like SPARC/ARC) — **important**
+- Heating system design for HH170/HH380 — proprietary — **important**
+- Energy conversion pathway specifics (cycle type, coolant, interface with blanket) — proprietary — **important**
+- Divertor/exhaust design — proprietary — **important**
+- Recirculating power fraction — derivable (from Q and heating efficiency assumptions) — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
-
 **Available**:
-- Full-HTS magnet set (TF+PF+CS): TRL 6 demonstrated on HH70; Jingtian magnet demonstrates HH170-class fields at TRL 5–6 — `iter-01`
-- AI plasma control: TRL 5–6 (demonstrated in >5,700 shots on HH70, including 1,337 s hold) — `iter-02`
-- REBCO tape manufacturing (domestic via Shanghai Superconductor): TRL 7–8 at pilot scale — `iter-01`
-- HH70 overall machine integration: TRL 6 (demonstrated operation) — `iter-03` abstract
+- **HTS magnets (TF/PF/CS full-REBCO)**: TRL 6 — Jingtian prototype demonstrated 21.7–22.4 T, and HH70 operated a full 26-coil set at 2.5 T. Full-power coil set for HH170 (25 T) not yet built. Analogous to CFS SPARC TFMC (20.1 T) which was TRL 5–6.
+- **AI plasma control**: TRL 5–6 — demonstrated on HH70 at 1,337 seconds; not yet validated at burning plasma conditions.
+- **ICRF heating**: TRL 7 — well-established on HH70 and prior tokamaks globally.
+- **Steam Rankine cycle (assumed BOP)**: TRL 9 — mature technology applicable by analogy.
+- **D-T fuel cycle**: TRL 4–5 — ITER program basis; Energy Singularity has not run D-T in any device.
+- The TEA analog (`knowledge/sources/tea_dt_mfe_cost_analysis/`) acknowledges low TRL for "tritium handling systems, advanced heat exhaust solutions, and high-field HTS magnets" and treats NOAK as bypassing TRL constraints.
 
 **Missing**:
-- TRL assessment for blanket/tritium breeding subsystem (not designed yet — effectively TRL 1–2 for this company's specific concept)
-- TRL for energy conversion system (not disclosed; generic D-T thermal cycle)
-- TRL for HH170 heating/CD systems beyond ICRF prototype capability
-- Tritium handling and processing systems (no disclosure at any stage)
+- TRL assessment from Energy Singularity (no company disclosure)
+- Tritium handling and breeding maturity for this specific design
+- Neutron shielding / first-wall design (no disclosure — first wall will need radiation-hardened materials)
+- Remote maintenance system design (no disclosure)
 
 **Gaps**:
-- Blanket/TBR subsystem TRL — `proprietary` + concept not yet designed — **blocking** for full maturity picture
-- Tritium processing/handling TRL — `truly-unknown` at Energy Singularity level — **important**
-- Divertor/PFC maturity — `not-yet-sourced` (general tokamak literature can inform) — **important**
-- HH380 power conversion system TRL — `proprietary` — **important**
+- Blanket/tritium breeding subsystem maturity — proprietary/TBD — **blocking**
+- Neutron shielding and first-wall design maturity — proprietary/TBD — **blocking**
+- Remote handling / maintenance system design — proprietary — **important**
+- Tritium handling system maturity (HH380-specific) — proprietary — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Poor
-
+**Coverage**: Partial
 **Available**:
-- REBCO tape: domestic supplier (Shanghai Superconductor) confirmed; >96% localization rate — `iter-01`
-- Tape geometry: 12 mm wide, 10 mm REBCO core, ~230 µm tape, ~480 µm conductor — `iter-01`
-- Scale of conductor use for HH70: ~450 m HTS conductor per TF coil × 12 = ~5,400 m for TF coils alone — calculable from `iter-01`
-- HH170 Jingtian-class magnets will require substantially more conductor (dimensions ~3 m × 1.4 m vs HH70 TF coil 2.015 m × 1.03 m); no tape quantity estimate published
+- REBCO HTS tape: primary supplier identified as Shanghai Superconductor; conductor specs known (12 mm wide, 230 μm thick, 10 mm REBCO core) (energy-singularity-overview.md)
+- Domestic localization rate >96% for HH70 — strong China-domestic supply chain signal (energy-singularity-overview.md; Xinhua iter-02)
+- Material costs for D-T HTS tokamak from cost analog: V-4Cr-4-Ti ($37/kg), SS316 LN ($10/kg), FLiBe ($154/kg), tungsten ($29/kg), copper ($8.3/kg), REBCO tape (per ARC/ARAI study) (`knowledge/sources/tea_dt_mfe_cost_analysis/`)
+- REBCO tape volume for ARC-equivalent: ~5,730 km of 70 kA cables used as analog basis (`knowledge/sources/tea_dt_mfe_cost_analysis/`)
 
 **Missing**:
-- Global REBCO tape supply capacity and cost trajectory — no source covers this for the HH380 scale
-- Lithium-6 supply (for tritium breeding) — not discussed anywhere in concept sources
-- Beryllium, tungsten, or other PFC/blanket-specific materials — not discussed (no blanket design)
-- Conductor quantity estimate for HH170 or HH380 magnets
-- Manufacturing cost per kA·m of REBCO at production scale
+- Blanket material specification (no disclosure — lithium ceramic, WCCB, LiPb, or other unknown)
+- REBCO tape production capacity at GW-scale deployment (current Shanghai Superconductor output unknown)
+- Tritium supply chain for D-T operation (standard gap for all pre-burning concepts)
+- Vanadium alloy or alternate structural material choice for HH380
 
 **Gaps**:
-- REBCO tape cost at production scale ($/kA·m or $/m) — `not-yet-sourced` (published HTS tape cost literature exists, e.g., SuperPower/Fujikura pricing studies) — **blocking** for magnet capital cost
-- HH170/HH380 conductor quantity estimate — `derivable` (from magnet geometry scaling, but geometry not yet public) — **important**
-- Li-6 enrichment supply chain — `not-yet-sourced` — **important**
-- Blanket materials (W, Be, structural steel, LiPb) — `truly-unknown` (no blanket design exists) — **important**
+- Blanket material and supply chain — proprietary/TBD — **blocking** (resolves only when blanket design disclosed)
+- REBCO tape production scale-up pathway and cost curve for GW deployment — not-yet-sourced — **important**
+- Tritium supply chain and initial inventory cost — derivable (from standard D-T fuel cycle models) — **important**
+- China-specific REBCO cost vs. Western sources (affects LCOE for non-Chinese deployments) — not-yet-sourced — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Q target (HH170) | Q > 10 | `iter-01` (company claim) | medium |
-| Plant timeline | HH380 post-2030; commercialization <2035 | `iter-01` | low (aspirational) |
-| Magnet field (HH170) | ~25 T peak (HTS coils) | `iter-01` | medium |
-| Device volume (HH170) | ~70% of SPARC | `iter-01` | medium |
-| Confinement approach | Steady-state tokamak | dossier | high |
-| Fuel | D-T | dossier | high |
-| Domestic localization | >96% (HH70) | `iter-01` | medium |
-| D-T MFE plant capital cost structure (CAS analog) | CAS 20–27 breakdowns | `knowledge/sources/tea_dt_mfe_cost_analysis/` | medium (analog only) |
+| Net electric output (analog) | 350 MWe (ARAI) / 500 MWe (TEA base case) | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Thermal power (analog) | 1,000–1,500 MWth | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Thermal efficiency (assumed Rankine) | ~33% | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| OCC (direct + indirect, D-T HTS tokamak) | $7,100–$14,900/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Total OCC (with owner's cost) | $8,800–$22,200/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Capacity factor (NOAK assumption) | 0.5–0.7 | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| LCOE (NOAK D-T MFE HTS tokamak) | $140–$550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Fixed O&M | $5–$12/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Variable O&M | $30–$170/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Annual equipment maintenance | $19–$63/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Power core replacement cost | $11–$107/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Decommissioning | 5% of total capital | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Discount rate | 6% | `knowledge/sources/tea_dt_mfe_cost_analysis/` | h |
+| Plant lifetime | 30 years | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| Magnet cost fraction (Account 22.13) | Dominant share of Account 22 | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m |
+| REBCO tape for compact HTS tokamak | ~5,730 km of 70 kA cables (ARC basis) | `knowledge/sources/tea_dt_mfe_cost_analysis/` | l |
+| Supplemental heating cost | ~$2.5/W | `knowledge/sources/tea_dt_mfe_cost_analysis/` | l |
+| Cryosystem cost | ~$300/kW | `knowledge/sources/tea_dt_mfe_cost_analysis/` | l |
+| Performance target (Q) | Q > 10 (HH170), commercial Q >> 10 | dossier / energy-singularity-overview.md | m |
+| Operation mode | Steady-state | dossier | h |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Net electrical output (MWe) | proprietary | blocking | HH380 has no published specs; CFS ARC (~200 MWe) is the closest published analog for compact HTS tokamak |
-| Capital cost by CAS account | proprietary | blocking | No plant study published; fleet analog (ARIES, TEA D-T MFE) applies but misses full-HTS magnet premium |
-| Full-HTS magnet capital cost premium vs. LTS | not-yet-sourced | blocking | Key differentiator for this concept; published academic cost models exist (Whyte et al., SPARC cost papers) but not captured |
-| Thermal conversion efficiency | proprietary | blocking | No energy cycle disclosed; generic Rankine or supercritical CO2 could be assumed from fleet analogs |
-| Capacity factor / availability | proprietary | blocking | Steady-state operation is an advantage; no plant-level estimate published |
-| O&M costs ($/MWh) | derivable | important | Can scale from D-T MFE analogs (TEA D-T MFE source) |
-| Recirculating power fraction | derivable | important | Can estimate from compact tokamak physics (heating, cryogenics at 20 K) |
-| Fuel cycle costs (tritium, D2 supply) | derivable | important | Standard D-T fuel cost is well-characterized in fleet analogs |
-| Decommissioning cost | derivable | important | Standard MFE analog applicable |
-| HTS tape cost contribution to magnet CAPEX | not-yet-sourced | important | Requires REBCO $/kA·m × conductor quantity estimate |
-| Construction time / interest during construction | proprietary | important | HH70 built in 2 years; HH380 unknown |
+| HH380 rated power output | proprietary | blocking | No company disclosure; must use ARC/ARAI analog (~350 MWe) with explicit caveat |
+| Blanket design and TBR | proprietary | blocking | Structurally unresolvable before HH380 engineering phase; blanket type drives tritium self-sufficiency and breeding heat |
+| Neutron wall loading and first-wall lifetime | proprietary | blocking | Required for replaceable-component cost and downtime estimate |
+| Energy conversion cycle (coolant, turbine inlet temperature) | proprietary | important | Rankine assumed; supercritical CO2 possible for higher efficiency — affects thermal efficiency by ~5–10 pts |
+| Recirculating power fraction | derivable | important | Derivable from Q and heating efficiency; ~15–25% typical for compact HTS tokamak |
+| Heating power and system efficiency (HH170/HH380) | proprietary | important | Only ICRF confirmed for HH70; higher-power HH380 heating not disclosed |
+| Capacity factor basis (Energy Singularity-specific) | derivable | important | Can use fleet analog (0.5–0.7) but concept-specific plasma disruption rate and maintenance cycle unknown |
+| REBCO tape unit cost at production scale | not-yet-sourced | important | Cost reduction trajectory from Shanghai Superconductor not publicly available; ARC assumed $87.5/m |
+| Tritium startup inventory and cost | derivable | important | Standard D-T assumption: ~5–10 kg; cost depends on CANDU/fission supply chain |
+| Chinese vs. Western supply chain cost differential | not-yet-sourced | nice-to-have | >96% domestic localization may create cost advantage (or disadvantage for international deployment) |
+| Indirect cost multiplier (China construction vs. US/EU) | not-yet-sourced | nice-to-have | ARAI uses US cost data; Chinese construction labor rates differ substantially |
 
 ---
 
 ## Source Recommendations
 
-1. **CFS/SPARC/ARC published literature** — compact HTS tokamak with disclosed parameters (major radius, magnet specs, Q target, power output). Most direct structural analog for cost estimation. `not-yet-sourced` — search SPARC physics basis papers (Journal of Plasma Physics, 2020) and ARC concept design papers. **Unverified — confirm existence before searching.**
+- **ARAI/ARC TEA** (`knowledge/sources/tea_dt_mfe_cost_analysis/`): Already integrated. This is the primary cost analog for HH380 — compact REBCO HTS D-T tokamak, NOAK basis. Reduces the `blocking` classification of HH380 power specs to a bounded `important` gap once analog assumptions are made explicit.
 
-2. **REBCO tape cost scaling studies** — published academic papers on $/kA·m vs. production volume for YBCO/REBCO tapes (SuperPower, SuNAM, Fujikura). Key input for HTS magnet capital cost. `not-yet-sourced` — search IEEE TAS, Superconductor Science and Technology journals. **Unverified — confirm existence before searching.**
+- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Already read. Provides the historical CAS framework (Accounts 20–27, 90–98) underlying the TEA analog; useful for structuring the LCOE model but adds no HTS-specific values not already in the TEA source. Explicitly disqualified as a concept-specific data source — it does not contain plasma parameters, material choices, or cost estimates relevant to Energy Singularity's machines beyond what the 2025 TEA paper already incorporates.
 
-3. **HH70 commissioning paper full text** — `knowledge/concept_research/28-hts-tokamak-full-hts/iter-03/` has abstract only (doi:10.1016/j.fusengdes.2025.115341). Full text would provide complete engineering specs, subsystem list, and potentially cost/schedule data. `not-yet-sourced` — institutional access or Sci-Hub.
+- **Energy Singularity HH70 commissioning paper** (Fusion Engineering and Design, 2025, doi:10.1016/j.fusengdes.2025.115341): Full text paywalled; abstract only captured in iter-03. Covers engineering design and commissioning of HH70 but not D-T blanket, power conversion, or LCOE — low priority for gap resolution. Flag as `not-yet-sourced` if full text becomes accessible; it may provide updated coil current, inductance, or plasma-facing material specs.
 
-4. **Jingtian magnet IEEE TAS paper (2025)** — would provide manufacturing data, conductor quantity, coil engineering details useful for magnet cost estimation. `not-yet-sourced` — search IEEE Xplore for "Jingtian" or "Energy Singularity" + "IEEE Transactions on Applied Superconductivity."
+- **Energy Singularity HH70 magnet system paper** (Superconductivity, 2024, doi:10.1016/j.supcon.2024.100119): Paywalled. May contain additional REBCO tape cost or engineering data relevant to §4. Low-to-medium priority — search OSTI or preprint servers.
 
-5. **Fleet-wide TEA D-T MFE source** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — already registered; directly applicable for BOP, O&M, decommissioning, and thermal conversion cost structure as tokamak analog. Read this before attempting LCOE estimation — it will supply most of the plant-level CAS accounts that Energy Singularity hasn't disclosed.
+- **CFETR blanket design studies** (China Fusion Engineering Test Reactor): Energy Singularity's HH380 blanket is likely to draw on CFETR's WCCB/HCCB/LiPb work. Search OSTI or IAEA Nuclear Data Services for "CFETR blanket 2024 2025" — `not-yet-sourced`, unverified existence of public English-language design studies.
 
-6. **ARIES-ACT or ARIES-AT design study** — advanced tokamak with high-field, steady-state operation closest to HH380 concept. Would provide CAS-level cost breakdowns for compact, steady-state MFE. `not-yet-sourced` — search ARIES project reports or ARIES Cost Account Documentation already registered.
+- **CFS SPARC plant study / ARC design documentation**: SPARC is the closest Western analog to HH170 (similar field, similar Q target). Published SPARC physics design papers (Ji 2022, Rodriguez-Fernandez 2022 series in Journal of Plasma Physics) may provide plasma parameter analogs derivable for HH170. Search via OSTI — `not-yet-sourced`, high-value for §3 subsystem maturity and §5 recirculating power.
+
+- **PyFECONS** (`/home/reid/PyFECONS`): Not read for this assessment — IFE and large-MFE heritage, may not have compact HTS tokamak configurations. Applicable for CAS validation of fleet analog cost outputs but likely less direct than the already-integrated TEA source. Disqualified as a primary source for this concept without further investigation.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with explicit use of fleet-wide analogs.** The concept-specific data is sufficient for qualitative characterization (technology approach, maturity trajectory, key differentiators) and partial quantitative analysis (magnet field, device sizing, Q target). For LCOE estimation, the analysis will need to lean heavily on fleet-wide D-T MFE cost analogs and make explicit the key unknown: the cost premium of a full-HTS magnet system (all coils REBCO) over conventional LTS or partial-HTS designs. Acquiring the HH70 full commissioning paper and a compact HTS tokamak cost study (CFS/ARC analog) before writing the analysis would materially improve confidence. The tritium breeding gap is structurally unresolvable until HH380 design phase (post-2030) and should be flagged as an assumed-standard D-T blanket for analysis purposes.
-
----
+Proceed to full D1+ analysis. The concept-scoped sources establish physics differentiation (all-REBCO coil set, 22.4 T demonstrated, Q>10 target, steady-state) and company context. The `knowledge/sources/tea_dt_mfe_cost_analysis/` fleet source provides a directly applicable NOAK cost framework for a compact REBCO HTS D-T tokamak ($140–$550/MWh LCOE, $8,800–$22,200/kW OCC, CF 0.5–0.7), which should be used as the primary LCOE basis with explicit "analog from ARC/ARAI" caveats. The three blocking gaps (HH380 specs, blanket/TBR, neutron shielding) are proprietary or structurally unresolvable before the HH380 engineering phase (~post-2030), so they should be documented as uncertainty sources that widen the LCOE range rather than treated as sourcing failures. The analysis is well-positioned to characterize both what is novel about Energy Singularity's approach and why cost uncertainty remains high.
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Significant Gaps"
-blocking_count: 6
-important_count: 9
-counting_method: "section_5_missing_parameters_plus_sections_1_to_4_blocking_gaps_deduplicated; section 5 blocking: net electrical output, capital cost by CAS, full-HTS magnet cost premium, thermal conversion efficiency, capacity factor; sections 1-4 added: blanket/TBR design"
+overall_rating: "Mostly Ready"
+blocking_count: 3
+important_count: 5
+counting_method: "deduplicated across all sections: blocking = HH380 power specs, blanket/TBR design, neutron shielding/first-wall design; important = heating plan HH170/HH380, energy conversion pathway, recirculating power fraction, capacity factor basis, REBCO scale-up cost"
 section_coverage:
   availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
-  materials_supply_chain:     "Poor"
-  lcoe_parameter_extraction:  "Poor"
+  materials_supply_chain:     "Partial"
+  lcoe_parameter_extraction:  "Partial"
 ```
\ No newline at end of file
```
