# Diff: 01-hts-compact-tokamak

**Generated:** 2026-05-22T09:26:34-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 1 | 4 | 3 |
| important_count  | 10 | 6 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
172:6. **tea_dt_mfe_cost_analysis** (already in source index): This D-T MFE cost analysis at `knowledge/sources/tea_dt_mfe_cost_analysis/` has not been read but is directly applicable to ARC costing methodology and CAS breakdowns. Should be read before constructing the quantitative LCOE model.
180:**Proceed to full analysis**: Yes, with caveats. The concept has sufficient technical depth for a rigorous qualitative D1+ write-up and a parameterized first-pass LCOE model. The primary actions needed before building the quantitative model are: (1) read `knowledge/sources/tea_dt_mfe_cost_analysis/` for D-T MFE CAS methodology; (2) decide how to handle the missing BOP — either use a pyFECONS MFE run with ARC parameters or scale from ARIES-AT as an analog; (3) assume 80% capacity factor as a point estimate (justified by Schwartz et al. 2024 and generic fusion planning) with a 65–90% sensitivity range; (4) note the confinement assumption (H₉₈ = 2.8) as the dominant physics risk in the qualitative write-up.
```

## Blocking-tier lines (baseline)

```
58:- Divertor design, materials selection, replacement schedule — `not-yet-sourced` / `proprietary` — **blocking** for LCOE (divertor replacement is a major OPEX driver in tokamaks)
88:- Divertor material and lifetime at ARC-scale heat flux — `not-yet-sourced` — **blocking** for LCOE
177:| Divertor design, materials, replacement schedule | not-yet-sourced | **blocking** | Explicitly left open in ARC 2015; required for first-wall OPEX estimate. Araiinejad & Shirvan 2025 gives only a crude cost share (~10% of reactor plant equipment, "18 tungsten tiles") — no design, materials, or replacement schedule. Sole remaining blocking LCOE gap. |
```

## Blocking-tier lines (new)

```
148:| Full plant capital cost (BOP included) | not-yet-sourced | **blocking** | ARC 2015 stops at reactor island. BOP cost (turbines, buildings, electrical, balance of plant) unquantified for ARC specifically. ARIES-AT (~1 GWe, ~$3B full plant 2003$) or pyFECONS applied to ARC parameters is the best analog |
149:| Capacity factor / plant availability | not-yet-sourced | **blocking** | ARC quasi-steady operation, burns tens of minutes. No explicit capacity factor stated. Generic fusion 75–85% often assumed; ARC modular VV replacement enables potentially shorter outages. Schwartz et al. 2024 provides framework but not ARC-specific values |
150:| Scheduled maintenance costs (blanket/VV replacement schedule) | not-yet-sourced | **blocking** | ARC replaceable VV concept is unique; no commercial operation cost model. VV fabricated cost ~$92M + divertor ~$17.5M; replacement cycle unknown |
152:| Tritium startup inventory cost | proprietary/not-yet-sourced | **blocking** | ARC paper flags FLiBe tritium extraction time as unknown. Startup inventory cost is a one-time capital add-on. Tritium at ~$84,000/g; estimated 1–2 kg needed. Need FLiBe T extraction efficiency data |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/01-hts-compact-tokamak.md	2026-05-22 09:21:13.829049462 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/gap_report.md	2026-05-22 09:26:34.682877177 -0700
@@ -1,11 +1,10 @@
-# Gap Assessment: HTS Compact Tokamak
+I now have enough information from all sources to write the comprehensive gap assessment.
 
-> **Revision 2026-05-20 — surgical regeneration.** Integrated Araiinejad & Shirvan 2025 (`knowledge/sources/tea_dt_mfe_cost_analysis/`), an independent bottom-up techno-economic analysis of "ARAI" — a modified-ARC D-T tokamak — treated here as an ARC-class cost analog per analyst decision (ARAI ≈ ARC, shared MIT/ARC origin). The source was already ingested repo-wide but never entered concept 01's Phase-1a research tree, so the original gap-check — which only sees concept-scoped sources — could not see it. Net effect: balance-of-plant cost, capacity factor, and vacuum-vessel replacement reclassified from blocking to important; `blocking_count` 4 → 1 (divertor only). This supersedes the original gap-check output.
+# Gap Assessment: HTS Compact Tokamak (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: The HTS Compact Tokamak (CFS/ARC) is one of the best-documented private fusion concepts, with a published conceptual reactor design (Sorbom et al. 2015), a detailed plasma physics basis (Creely et al. 2020), a specific heating system study (Lin et al. 2020), an independent power conversion analysis (Colliva et al. 2024), and — for plant-level economics — an independent ARC-class techno-economic analysis (Araiinejad & Shirvan 2025). A first-pass LCOE model is buildable from available data, with caveats: the ARC-paper capital estimate excludes balance of plant and is denominated in 2014 dollars for a 200 MWe design since evolved to 400 MWe. Araiinejad & Shirvan 2025 now supplies an ARC-class balance-of-plant, O&M, and LCOE envelope (NOAK lower/upper bounds at 350 MWe), which removes balance-of-plant cost, capacity factor, and vacuum-vessel replacement as blocking gaps — they remain important accuracy gaps pending CFS-specific data. The divertor — explicitly deferred in the 2015 ARC paper — is now the sole blocking LCOE gap.
+**Summary**: The CFS ARC/SPARC concept has exceptionally rich public literature for a private fusion company — a detailed 2015 ARC conceptual design paper with plasma physics, magnetics, blanket engineering, neutronics, and rough economics; multiple independent power conversion studies; an ICRF physics basis paper; and current construction/commercial updates. A first-pass qualitative and quantitative LCOE analysis is supportable now. The main gaps are a missing full-plant capital cost (the ARC 2015 paper covers reactor island only, not BOP), no explicit capacity factor target, and significant uncertainty on the Q/confinement assumption that underlies the entire plant concept.
 
 ---
 
@@ -15,79 +14,76 @@
 **Coverage**: Good
 
 **Available**:
-- Sorbom et al. 2015 (ARC paper): Full conceptual design with physics basis, costing estimate ($5.5–5.6B fabricated, 2014$, excluding BoP), neutronics, materials analysis, and R&D gaps (Section 7). This is an unusually complete public document for a private venture.
-- Creely et al. 2020 (SPARC overview): SPARC physics parameters (Bt=12.2T, Ip=8.7MA, R=1.85m, targeting Q~11)
-- Lin et al. 2020 (ICRF physics): Detailed heating system physics, antenna design rationale, power absorption calculations
-- Colliva et al. 2024 (power conversion): Three-cycle comparison (Rankine 46%, sCO₂ 40%, He Brayton 32% net efficiency for ARC FNSF phase at 645 MWth input)
-- Araiinejad & Shirvan 2025 (TEA of D-T MC fusion power plants, `knowledge/sources/tea_dt_mfe_cost_analysis/`): independent bottom-up techno-economic analysis of "ARAI", a modified-ARC reactor (2015 ARC design with vanadium-alloy VV/plasma-facing components), scaled to a 350 MWe ARC-class plant. Provides a full plant-level cost breakdown — direct + indirect + balance of plant + O&M + decommissioning — at NOAK lower/upper bounds. Used as an ARC-class cost analog per analyst decision (ARAI ≈ ARC); an independent academic estimate, not CFS data.
-- CFS public communications (2025–2026): SPARC construction status, ARC site announcement (Virginia), 400 MWe target, investor disclosures
-- Dossier: All 12 differentiation columns filled at high/medium confidence
+- **Sorbom et al. 2015 (ARC paper)** (`arc-reactor-specifications.md`): Full conceptual design — plasma physics, radial build, magnet engineering, FLiBe blanket neutronics (MCNP), disruption analysis, and Section 6 rough materials/fabrication cost estimate for the reactor island. This is the primary reference.
+- **SPARC ICRF heating paper** (`sparc-icrf-heating-paper.md`): Physics basis for the 25 MW ICRF system at 120 MHz; establishes heating system design.
+- **ARC power conversion study** (`arc-power-conversion-studies.md`, Colliva et al. 2024): Three-cycle GateCycle analysis — Rankine (46% net), sCO₂ Brayton (40.3%), He Brayton (32%). Concludes supercritical steam Rankine is the "most promising solution" for the FNSF phase.
+- **CFS 2025–2026 updates** (`cfs-2025-2026-updates.md`): SPARC assembly started January 2026, first TF magnet installed, first plasma targeting 2027; ARC commercial target confirmed at 400 MWe at Virginia site with Google and Eni PPAs.
+- **REBCO tape supply and cost** (`arxiv-2503-23048.md`, `sciencedirect-s2772830725000390.md`): Current PLD-REBCO production prices ~$20/m; declining costs driven by compact fusion demand; CERN procurement data showing HTS approaching Nb₃Sn normalized costs at 16+ T.
+- **Li-6 supply chain** (`sciencedirect-s092037961930835x.md`): Documents that enriched Li-6 is not commercially available at fleet-deployment scale; ICOMAX process proposed for DEMO.
+- **Schwartz et al. 2024** (`arxiv-2405-01514.md`): Generic D-T tokamak maintenance value study — capacity factor, blanket durability, optimal replacement scheduling.
+- **ARPA-E ALPHA costing revisit** (`osti-servlets-purl-1820946.md`): CAS-structured cost breakdown for ~500 MWe compact modular fusion ($1.2B TCC, 43 $/MWh LCOE range 34–54) — non-tokamak but useful as cross-check on BOP and indirect cost structure.
+- **pyFECONS methodology papers** (`arxiv-2601-21724.md`, `arxiv-2602-19389.md`): ARPA-E/CATF costing framework directly applicable to compact tokamak costing, with explicit MFE magnet account (22.1.3) and probabilistic extensions.
 
 **Missing**:
-- Updated ARC commercial design documentation (the public ARC design is 2015 vintage; the 400 MWe commercial plant remains undocumented publicly)
-- SPARC results (device is under construction; first plasma ~2027)
-- CFS-specific BoP cost breakdown (an ARC-class analog is now available — Araiinejad & Shirvan 2025 — but CFS's own BoP figures remain unpublished)
-- CFS-specific site-level operational parameters (staffing, O&M); analog O&M estimates now available from Araiinejad & Shirvan 2025
+- No published full-plant ARC capital cost (ARC 2015 Section 6 is reactor island only; BOP, buildings, indirects not addressed).
+- No ARC-specific LCOE estimate in any source.
+- Creely et al. 2020 (SPARC overview) cited in dossier but not ingested; would provide updated plasma performance parameters.
 
 **Gaps**:
-- Updated ARC commercial design parameters — `proprietary` — important (changes plant output from 200→400 MWe, affects all cost scaling)
-- SPARC experimental results validating burning plasma physics — `not-yet-available` (SPARC not yet operating) — important but not blocking (ARC paper physics basis is well-documented)
-- CFS internal cost modeling for ARC at 400 MWe — `proprietary` — important
+- No ingested ARC-specific capital cost study beyond the reactor island rough estimate — `not-yet-sourced` — **important**. PROCESS runs for ARC-like compact tokamaks exist in the academic literature (e.g., Franza et al. 2022 PROCESS runs for compact high-field tokamaks). Search OSTI/arXiv for "ARC compact tokamak PROCESS LCOE" or "CFS ARC capital cost."
+- Creely et al. 2020 (J. Plasma Phys.) overview of SPARC physics basis not ingested — `not-yet-sourced` — **nice-to-have**. Contains updated design parameters that supersede some ARC 2015 values.
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Good
+**Coverage**: Partial
 
 **Available**:
-The ARC paper (Section 7) is explicit about its engineering uncertainties. Key challenges are documented:
-
-- **Plasma regime (I-mode)**: ARC is designed around I-mode confinement (energy barrier without particle barrier), which avoids damaging ELMs. The paper flags that I-mode has been demonstrated at ≤6T; ARC operates at 9.2T, so confinement extrapolation carries physics uncertainty. SPARC will validate this.
-- **LHCD at 8 GHz**: The ARC paper identifies that klystron sources exist at 6 GHz but not 8 GHz. The heating system uses 25 MW LHCD (current drive) + 13.6 MW ICRF (heating). Lin et al. 2020 establishes ICRF physics clearly; LHCD is the less mature component.
-- **FLiBe behavior under radiation**: The paper explicitly flags unknown MHD effects on FLiBe flow at relevant magnetic fields, unknown radiation-assisted corrosion of Inconel 718 in FLiBe, and radiation effects on FLiBe resistivity.
-- **Tritium extraction from FLiBe**: Described as an active R&D area; the turnaround time for tritium extraction determines the tritium inventory requirement. The paper notes "few experiments have been built to assess the turnaround time."
-- **Quasi-steady operation**: ARC pulses for "tens of minutes" rather than continuous. The power conversion system requires an energy storage system (ESS) between the FLiBe intermediate circuit and the turbine. Colliva et al. 2024 notes this ESS and analyzes pulse-phase power (645 MWth), but dwell-phase dynamics are not quantified.
-- **Divertor design**: Explicitly left as "an open question" in the ARC 2015 paper. This is a significant cost and engineering uncertainty.
+The ARC 2015 paper explicitly enumerates R&D needs and uncertainties, providing a clear roadmap of modeling difficulties:
+- **I-mode confinement regime**: ARC targets H₉₈ = 2.8 (40% above standard H-mode). The paper acknowledges "significantly less information" on I-mode energy transport scaling with device size and relies on C-Mod scalings that may not hold in a burning plasma. This is the primary physics uncertainty affecting Q and Pf.
+- **HTS demountable coil joints**: The REBCO joint resistance dissipates power and must be accounted in the plant electrical balance. At commercial scale the joint resistance has not been demonstrated; the 2015 paper estimates ~27 MW loss but flagged this as needing validation.
+- **FLiBe magnetohydrodynamic effects**: MHD flow in a high-field environment affects heat transfer; computational results suggest it is negligible but experimental validation is needed.
+- **Radiation-assisted corrosion of Inconel 718 in FLiBe**: Static corrosion rate from experiment (1.1 µm/yr) does not include radiation effects; the paper flags this as a key unknown for vacuum vessel lifetime.
+- **Tritium extraction from FLiBe**: Turnaround time for tritium extraction from the FLiBe loop directly determines startup inventory and regulatory compliance; limited experimental data exists.
+- **Quasi-steady operation + energy storage**: ARC pulsed for "tens of minutes" requires FLiBe thermal storage to provide steady grid power. The cost of this storage system and its effect on availability are not modeled.
+- **Divertor design left for future work**: Section 6 of ARC 2015 explicitly omits divertor cost; its design and cost are unknown at this stage.
 
 **Missing**:
-- Divertor technology selection and cost estimate
-- Quantitative ESS sizing and cost
-- FLiBe radiation chemistry data at ARC-relevant neutron flux
+- No cost propagation model mapping physics uncertainties (especially confinement factor H₉₈) to capital cost uncertainty bands.
+- No explicit LCOE sensitivity to the Q uncertainty.
 
 **Gaps**:
-- Divertor design, materials selection, replacement schedule — `not-yet-sourced` / `proprietary` — **blocking** for LCOE (divertor replacement is a major OPEX driver in tokamaks)
-- ESS sizing and cost — `not-yet-sourced` — important
-- LHCD wall-plug efficiency at 8 GHz — `derivable` from klystron analogs (medium confidence)
+- Quantified sensitivity of LCOE to H₉₈ uncertainty — `derivable` from ARC 0-D scoping model (Fig. 15 in ARC paper provides Pf vs. H₉₈ scan) — **important**. Can be built from available data.
+- Cost impact of demountable joint power loss on plant Qe — `derivable` from ARC electrical balance — **nice-to-have**.
+- Thermal storage system cost for quasi-steady output smoothing — `not-yet-sourced` — **important**. Analogues exist in molten salt fission CSP literature.
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial
+**Coverage**: Good
 
 **Available**:
-The ARC paper and CFS public materials provide enough to make TRL assessments for most subsystems:
+The ARC paper, CFS updates, and magnet supply chain sources provide a clear TRL picture:
 
-| Subsystem | TRL Estimate | Basis |
-|-----------|-------------|-------|
-| HTS magnets (REBCO TF coils) | TRL 6–7 | 20T large-bore magnet demonstrated September 2021; SPARC magnet installation underway 2025–2026 |
-| ICRF heating system (~120 MHz, 25 MW) | TRL 5–6 | Physics validated on JET and TFTR (Lin 2020); SPARC-specific antenna requires engineering demonstration |
-| FLiBe blanket (tritium breeding + cooling) | TRL 3–4 | Concept well-understood from molten salt fission (MSRE); tritium extraction at power scale undemonstrated |
-| Tritium extraction from FLiBe | TRL 2–3 | Identified as R&D gap in ARC paper; no power-relevant experiments |
-| LHCD at 8 GHz | TRL 3–4 | 6 GHz klystrons demonstrated; 8 GHz is a technology stretch (per ARC paper Section 7.1) |
-| Power conversion (supercritical steam Rankine) | TRL 7–8 | Mature commercial technology; ARC-specific integration at 645 MWth TRL 5 |
-| Vacuum vessel (Inconel 718 + FLiBe) | TRL 3–4 | Corrosion data at 873K in FLiBe exists; radiation-assisted corrosion unknown |
-| TiH₂ neutron shielding | TRL 4–5 | Material properties established; large-scale structural application in reactor context novel |
-| Demountable HTS joints (REBCO) | TRL 4–5 | Bench-top demonstrations exist; reactor-scale validation pending SPARC |
+| Subsystem | TRL (approx.) | Basis |
+|---|---|---|
+| REBCO HTS magnets (TF coils, demountable) | 5–6 | 20T large-bore magnet demonstrated (Sept 2021); SPARC TF magnets being manufactured and installed (2026). No demountable joint at full ARC scale validated. |
+| PIT VIPER pulsed superconducting magnets (CS/PF) | 4–5 | Demonstrated by CFS in 2024; novel cable-in-conduit concept, not yet at ARC operating currents |
+| ICRF heating system | 6–7 | Mature technology; SPARC ICRF design based on C-Mod heritage at 120 MHz. Physics basis paper (Lin et al. 2020) establishes design. |
+| LHCD system (HFS launch) | 4–5 | High-field-side launch not demonstrated in a burning plasma; physics basis established in ARC paper using ACCOME code |
+| FLiBe liquid immersion blanket | 3–4 | Conceptual design with MCNP neutronics. No full-scale demonstration at fusion-relevant temperatures. Tritium extraction from FLiBe loop not demonstrated at needed flow rates. |
+| First wall / divertor | 3 | Explicitly left for future work in ARC paper; Inconel 718 for VV chosen as "first-round" material pending materials R&D |
+| Power conversion (supercritical Rankine) | 8–9 | Mature industrial technology; Colliva 2024 confirms it's the preferred option; no fusion-specific qualification needed |
+| Remote handling / maintenance | 3–4 | Demountable coil concept enables new maintenance paradigm; no system-level demonstration at fusion scale |
+| Tritium processing | 5–6 | Generic D-T tritium handling well-developed; FLiBe-specific extraction loop challenging; KIT/ORNL experience is fission MSR not fusion D-T |
+| Plasma facing components (Be first wall, W divertor) | 4–5 | Materials selected; radiation performance in D-T spectrum not validated for 9 FPY lifetime |
 
 **Missing**:
-- TRL assessment for plasma-facing components at ARC heat flux levels (first wall: W, divertor material TBD)
-- Cryogenic system TRL for 20K HTS operation at ARC scale
-- Digital twin / AI control system TRL (CFS + Siemens + NVIDIA partnership — mentioned in 2026 update, no technical specifics)
+- No published TRL assessment for CFS subsystems exists in the source set; TRL estimates above are inferred from technical content.
 
 **Gaps**:
-- Divertor material and lifetime at ARC-scale heat flux — `not-yet-sourced` — **blocking** for LCOE
-- REBCO irradiation limits in fusion-relevant spectrum — `not-yet-sourced` (ARC paper notes no failure testing done) — important for lifetime calculation
-- Cryogenic system sizing and cost — `derivable` from ITER analogues — important
+- Formal TRL assessment for any ARC/SPARC subsystem — `proprietary` (CFS likely has internal TRL data from DOE reporting but hasn't published it) — **important**. STEP/DEMO literature contains analogous assessments for conventional tokamak subsystems; use as partial analog.
+- Divertor design and cost: ARC 2015 rough estimate is $17.5M fabricated for a W divertor; full design basis absent — `not-yet-sourced` — **important for cost model**.
 
 ---
 
@@ -95,139 +91,109 @@
 **Coverage**: Partial
 
 **Available**:
-The ARC paper provides 2014 material cost figures and quantities (Table 10 and Table 11):
-
-| Material | Quantity (ARC) | 2014 Price | Notes |
-|----------|---------------|------------|-------|
-| REBCO tape | 5,730 km | $36–$198/m | Bulk quote range; dominant cost driver |
-| FLiBe | ~950 tonnes (blanket + HX) | $154/kg | Beryllium component is toxic and supply-limited |
-| Beryllium (multiplier) | ~3.82 tonnes | $257/kg | US production from Materion; export controls |
-| TiH₂ (shield) | ~380 tonnes | $26.4/kg | Limited commercial scale |
-| Inconel 718 | ~170 tonnes (VV + blanket tank) | $56/kg | Commercially available but neutron activation concerns |
-| Tungsten (first wall) | ~3.72 tonnes | $29/kg | Commercially available |
-
-**Key supply chain concerns (from ARC paper and general knowledge)**:
-- **REBCO tape**: Few commercial manufacturers (AMSC, SuperPower/Furukawa, Bruker, SuNAM, Theva). CFS has publicly disclosed manufacturing agreements. Price has declined since 2014 (~$36/m in bulk was the low end in 2015; current spot prices are in this range or lower). Supply for a commercial fleet of ARC reactors would require significant expansion.
-- **Beryllium**: Used as neutron multiplier in the vacuum vessel (FLiBe contains Be naturally). Primary US supplier is Materion. Beryllium is toxic to process and subject to export restrictions. Global supply is limited.
-- **Tritium**: Initial startup inventory needed (~0.5–1 kg/reactor). Global civilian tritium inventory is ~25 kg (primarily from CANDU reactors). At ARC scale (400 MWe), daily tritium consumption is ~150–200 g/day, requiring TBR > 1 from day one. FLiBe TBR ≥ 1.1 is the design target but undemonstrated.
-- **FLiBe at scale**: No large-scale commercial FLiBe production exists. BeF₂ production capacity is the bottleneck. Toxicity and cost make this a supply chain risk.
+- **REBCO tape**: ARC 2015 requires 5,730 km tape at $36–198/m (2014$); current pricing ~$20/m (PLD manufacturers, s2772830725000390). Cost is declining; production capacity is expanding. For a fleet of ARC plants at $20/m this is ~$114M per reactor — manageable. The arxiv-2503-23048 paper confirms the fusion demand is currently the main driver of REBCO production scale-up. Supply is technically available but constrained at any given production ramp rate.
+- **FLiBe (LiF-BeF₂ molten salt)**: ARC requires ~950 tonnes of FLiBe (475 tonnes blanket tank + 475 tonnes heat exchanger per ARC 2015 Table 11) at $154/kg = ~$146M per unit. FLiBe availability depends on beryllium supply; Be is strategically sensitive (primarily sourced from US/Kazakhstan). No specific supply chain analysis found in sources.
+- **Beryllium**: ~3.82 tonnes used as neutron multiplier in ARC vacuum vessel. Beryllium has limited global production capacity (US near-monopoly for aerospace/defense). Critical material for ARC fleet.
+- **Li-6 enrichment**: ARC uses FLiBe with natural Li (7.6% ⁶Li). The source on Li-6 supply (s092037961930835x) documents that enriched Li-6 at fleet scale is a supply chain risk for DEMO and future power plants; if ARC FLiBe uses natural lithium, this risk is lower but TBR optimization may require enrichment.
+- **Inconel 718**: Vacuum vessel and blanket tank material (97+ tonnes per unit). Industrial commodity, no supply constraint.
 
 **Missing**:
-- Current (2025/2026) REBCO tape pricing and CFS supply agreements
-- Quantitative FLiBe production capacity analysis
-- Tritium startup inventory plan for ARC commercial plant
+- No ARC-specific supply chain or criticality analysis.
+- No beryllium supply chain analysis despite it being a strategic material in significant quantities.
 
 **Gaps**:
-- Current REBCO tape cost and supply commitment status — `proprietary`/`not-yet-sourced` — important (cost driver)
-- FLiBe production capacity at ARC-fleet scale — `not-yet-sourced` — important
-- Beryllium supply chain risk quantification — `derivable` from open US DOE beryllium supply data — nice-to-have
+- Beryllium supply chain analysis — `not-yet-sourced` — **important**. USGS/DoD beryllium criticality assessments exist; search "beryllium supply chain fusion reactor" and US Geological Survey mineral commodity summaries.
+- REBCO ramp-rate analysis for fleet deployment — `derivable` from current production data + ARC tape requirements — **nice-to-have**.
+- Tritium startup inventory cost — `not-yet-sourced` — **blocking for LCOE**. Startup tritium costs ($84M/kg market price assumed; ARC needs a minimum initial inventory that depends on FLiBe tritium extraction efficiency) are a known gap in ARC 2015. Search for "tritium startup inventory tokamak" or "tritium doubling time ARC" in DOE/NRC literature.
 
 ---
 
 ### 5. LCOE Parameter Extraction
+**Coverage**: Partial
+
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
-|-----------|-------------|--------|------------|
-| Fusion power (ARC 2015) | 525 MW | Sorbom 2015 | h |
-| Net electric power (ARC 2015, FNSF) | ~190 MW | Sorbom 2015 | m |
-| Net electric power (ARC 2015, conservative pilot) | ~233 MW | Sorbom 2015 | m |
-| Net electric power (current ARC target) | 400 MWe | CFS 2025-2026 | m |
-| On-axis B field | 9.2 T | Sorbom 2015 | h |
-| Major radius | 3.3 m | Sorbom 2015 | h |
-| Plasma gain Qp | ~13.6 | Sorbom 2015 | h |
-| Electrical gain Qe | 3.0–3.8 | Sorbom 2015 | m |
-| Thermal efficiency (Rankine, FNSF) | 46% net | Colliva 2024 | m |
-| Thermal efficiency (ARC 2015 He Brayton, FNSF) | ~40% | Sorbom 2015 | m |
-| Blanket outlet temperature (FNSF) | 900 K | Sorbom 2015 | h |
-| ICRF heating power (SPARC) | 25 MW | Lin 2020 | h |
-| LHCD power (ARC) | 25 MW | Sorbom 2015 | h |
-| Bootstrap fraction | ~63% | Sorbom 2015 | h |
-| TBR (FLiBe blanket) | ≥1.1 (up to 1.22) | Sorbom 2015 | m |
-| TF coil lifetime (neutron fluence limit) | ≥9 FPY | Sorbom 2015 | l–m |
-| Inner vacuum vessel lifetime | ~6–12 months | Sorbom 2015 | l |
-| Total fabricated cost (2014$, excl. BoP) | $5.5–5.6B | Sorbom 2015 | l |
-| REBCO tape cost | $36–$198/m (2014$) | Sorbom 2015 | l |
-| FLiBe cost | $154/kg (2014$) | Sorbom 2015 | l |
-| Magnet/structure fabricated cost | $5.1–5.2B (2014$) | Sorbom 2015 | l |
-| Blanket fabricated cost | ~$260M (2014$) | Sorbom 2015 | l |
-| Vacuum vessel fabricated cost | ~$92M (2014$) | Sorbom 2015 | l |
-| Operation mode | Quasi-steady (tens of minutes) | CFS communications | h |
-| SPARC parameters (B, R, Ip, ne, Te) | 12.2T, 1.85m, 8.7MA, 4×10²⁰m⁻³, 20 keV | Lin 2020 | h |
-| Overnight capital cost (ARC-class analog, NOAK) | 8,800–22,200 $/kW | Araiinejad & Shirvan 2025 | l |
-| BoP — turbine generator equipment | 535–550 $/kW | Araiinejad & Shirvan 2025 | m |
-| BoP — electric plant equipment | 274–402 $/kW | Araiinejad & Shirvan 2025 | m |
-| BoP — heat rejection system | 70–88 $/kW | Araiinejad & Shirvan 2025 | m |
-| Structures & site facilities | 819–1,317 $/kW | Araiinejad & Shirvan 2025 | l–m |
-| Indirect cost | 1,146–2,644 $/kW | Araiinejad & Shirvan 2025 | l–m |
-| Capacity factor (NOAK analog, not ARC-derived) | 0.5–0.7 | Araiinejad & Shirvan 2025 | l |
-| Annual O&M | 35–182 $/MWh | Araiinejad & Shirvan 2025 | l |
-| Replaceable-component O&M (VV + PFC) | 11–107 $/MWh | Araiinejad & Shirvan 2025 | l |
-| Fabricated VV + first wall cost | 109 $/kW (conventional fab) | Araiinejad & Shirvan 2025 | l |
-| Power-core fabrication cost assumption | $1,000/kg FOAK → $150/kg NOAK → $15/kg advanced mfg | Araiinejad & Shirvan 2025 | l |
-| LCOE (ARC-class analog, NOAK) | 140–550 $/MWh | Araiinejad & Shirvan 2025 | l |
+|---|---|---|---|
+| Fusion power (Pf) | 525 MW | ARC paper (Sorbom 2015) | h |
+| Plasma gain (Qp) | ~13.6 | ARC paper | h |
+| External heating power | 38.6 MW (25 MW LHCD + 13.6 MW ICRF) | ARC paper | h |
+| On-axis B₀ | 9.2 T | ARC paper | h |
+| Major radius R₀ | 3.3 m | ARC paper | h |
+| Net electrical output | 190–261 MWe (Brayton) | ARC paper | m |
+| Net electrical output | ~297 MWe (Rankine, FNSF) | Colliva 2024 | m |
+| Commercial plant target output | 400 MWe | CFS 2026 updates | m |
+| Thermal efficiency (Brayton, 900K) | ~40% | ARC paper | m |
+| Thermal efficiency (Rankine, optimal) | 46% net | Colliva 2024 | m |
+| Thermal power to PCS | 645 MWth | Colliva 2024 (power balance) | h |
+| TF coil lifetime | ≥9 full-power years | ARC paper (MCNP) | m |
+| Vacuum vessel replacement cost (fabricated) | ~$92M (2014$) | ARC paper Section 6 | l |
+| Blanket (FLiBe + Inconel) fabricated cost | ~$260M (2014$) | ARC paper Section 6 | l |
+| Magnet/structure fabricated cost | $5.1–5.2B (2014$) | ARC paper Section 6 | l |
+| Reactor island total (materials+fabrication, no BOP) | $5.5–5.6B (2014$) | ARC paper Section 6 | l |
+| REBCO tape cost (current) | ~$20/m | s2772830725000390 | h |
+| REBCO tape cost (2014 quote, bulk) | $36–198/m | ARC paper | l |
+| FLiBe cost | $154/kg (2014$) | ARC paper | l |
+| REBCO tape length required | 5,730 km | ARC paper | m |
+| Materials-only total | $330–430M (2014$) | ARC paper | l |
+| TBR | ≥1.1 (optimizable to 1.22) | ARC paper (MCNP) | h |
+| D-T fuel cost | Near-zero (bred on-site) | ARC paper, standard | h |
+| Analog LCOE (ALPHA modular fusion ~500 MWe) | 34–54 $/MWh | ARPA-E ALPHA revisit | l |
+| Analog CapEx (ALPHA modular fusion) | 2.4 $/W, $1.2B | ARPA-E ALPHA revisit | l |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
-|-----------|----------|-------------|-------|
-| Balance of plant capital cost | derivable (analog) | important | CFS-specific BoP unpublished, but an ARC-class analog is now available (Araiinejad & Shirvan 2025: turbine generator, electric plant, heat rejection, structures, indirect — NOAK LB/UB). No longer blocking — build LCOE with stated-assumption BoP. |
-| Capacity factor / availability | derivable | important | Analog range 0.5–0.7 now available (Araiinejad & Shirvan 2025), enough to bound an LCOE model. Generic NPP/fossil-derived — does not reflect ARC's 6–12-month VV-replacement downtime; derive ARC-specific availability for accuracy. |
-| Vacuum vessel replacement cost and schedule | derivable | important | Costing methodology + figures now available (Araiinejad & Shirvan 2025: fabricated VV+FW 109 $/kW, replaceable-component O&M 11–107 $/MWh). Thesis assumes a 24-month vanadium VV; ARC's Inconel 718 inner VV is ~6–12 months — apply ARC's schedule with the analog costing. |
-| Divertor design, materials, replacement schedule | not-yet-sourced | **blocking** | Explicitly left open in ARC 2015; required for first-wall OPEX estimate. Araiinejad & Shirvan 2025 gives only a crude cost share (~10% of reactor plant equipment, "18 tungsten tiles") — no design, materials, or replacement schedule. Sole remaining blocking LCOE gap. |
-| Staffing / O&M cost rates | not-yet-sourced | important | No published estimates; ITER/tokamak analogues can inform |
-| Electricity for recirculating power (grid draw) | derivable | important | Qe is given (3–3.8); recirculating fraction derivable (~1/Qe ≈ 26–33%) |
-| ESS (energy storage system) cost | not-yet-sourced | important | Required to buffer pulsed operation; Colliva 2024 mentions but doesn't size or cost |
-| REBCO tape current market price | not-yet-sourced | important | 2014 price range in source; market has evolved significantly |
-| Tritium startup inventory cost | derivable | important | ~0.5–1 kg at ~$30,000/g ≈ $15–30M; derivable from published tritium price estimates |
-| Cooling system and cryostat capital cost | derivable | important | 20K cooling for HTS coils; can estimate from ITER/W7-X analogs |
-| ARC at 400 MWe: updated capital cost | proprietary | important | 2015 paper designed 200–250 MWe; updated design is unpublished |
+|---|---|---|---|
+| Full plant capital cost (BOP included) | not-yet-sourced | **blocking** | ARC 2015 stops at reactor island. BOP cost (turbines, buildings, electrical, balance of plant) unquantified for ARC specifically. ARIES-AT (~1 GWe, ~$3B full plant 2003$) or pyFECONS applied to ARC parameters is the best analog |
+| Capacity factor / plant availability | not-yet-sourced | **blocking** | ARC quasi-steady operation, burns tens of minutes. No explicit capacity factor stated. Generic fusion 75–85% often assumed; ARC modular VV replacement enables potentially shorter outages. Schwartz et al. 2024 provides framework but not ARC-specific values |
+| Scheduled maintenance costs (blanket/VV replacement schedule) | not-yet-sourced | **blocking** | ARC replaceable VV concept is unique; no commercial operation cost model. VV fabricated cost ~$92M + divertor ~$17.5M; replacement cycle unknown |
+| Operating costs (O&M, staffing) | not-yet-sourced | **important** | No ARC-specific O&M data. ARPA-E ALPHA analog: $48M/year O&M for ~500 MWe; use as rough cross-check |
+| Tritium startup inventory cost | proprietary/not-yet-sourced | **blocking** | ARC paper flags FLiBe tritium extraction time as unknown. Startup inventory cost is a one-time capital add-on. Tritium at ~$84,000/g; estimated 1–2 kg needed. Need FLiBe T extraction efficiency data |
+| Interest during construction / construction time | derivable | **important** | CFS plans "early 2030s" for ARC commercial; SPARC 2027 first plasma → ARC ~2033? ~5-7 year construction assumed. Standard 7% WACC, 3-year construction would produce ~$300-400M IDC at $1.2B total capital |
+| Decommissioning cost | derivable | nice-to-have | ARC's reduced activation inventory (85 tonnes solid vs. ITER's 2000 tonnes) should significantly reduce decommissioning cost. Can scale from ITER/fission analogues |
+| REBCO supply cost trajectory for NOAK/fleet | derivable | important | 2014 ARC paper uses $36–198/m; current ~$20/m. Learning curve for fleet deployment derivable from arxiv-2503-23048 data |
+| Recirculating power (cryogenics + controls during operation) | derivable | important | Schwartz et al. use 5% active + 10% passive parasitic; ARC demountable joint losses (~27 MW) are an additional load. Total recirculating power affects Qe and capacity factor |
 
 ---
 
 ## Source Recommendations
 
-1. **BoP capital cost** — *resolved (analog).* Araiinejad & Shirvan 2025 (`knowledge/sources/tea_dt_mfe_cost_analysis/`) provides a full bottom-up plant-level cost breakdown for an ARC-class D-T MC plant — direct, indirect, and BoP at NOAK lower/upper bounds. Use as the primary BoP analog, flagged as an independent academic estimate. The ARIES-AT study (Najmabadi et al.) remains a useful secondary cross-check.
+1. **Full ARC plant capital cost study**: Search OSTI/arXiv for PROCESS-based analyses of compact high-field tokamaks (ARC-like). Franza et al. or similar systems code outputs for ARC parameters would provide BOP and full plant cost. Search: "ARC compact tokamak systems code PROCESS cost" — `not-yet-sourced`, unverified — confirm before searching.
 
-2. **Capacity factor / availability** — *partially addressed.* Araiinejad & Shirvan 2025 supplies a usable analog range (CF 0.5–0.7). No CFS-specific publication exists; for ARC accuracy still derive from first principles: (a) VV replacement frequency [6–12 months], (b) time per replacement, (c) unplanned outage rate by analogy to JET/C-Mod. The ARC paper assumes modular replacement as a key availability improvement — model this explicitly.
+2. **Creely et al. 2020, "Overview of the SPARC tokamak," J. Plasma Phys.**: Published SPARC physics basis covering updated design parameters vs. ARC 2015. Should be ingested to update performance parameters for any Q/power sensitivity analysis. DOI: 10.1017/S0022377820001257.
 
-3. **Divertor design and lifetime**: Search for CFS technical presentations at IAEA Fusion Energy Conference or ANS Fusion Engineering conference. May have updated ARC divertor design since 2015. Also applicable: ITER divertor experience as conservative analog. `unverified — search IAEA FEC 2023 proceedings for "ARC" or "CFS divertor"`
+3. **ARC-specific LCOE study**: Roddy & Whyte or similar MIT PSFC economic analysis of ARC. A 2022 paper by Lindley et al. or Pearson et al. may provide LCOE estimates; unverified — search PSFC publications or CFS technical reports.
 
-4. **REBCO tape current pricing and supply**: Contact manufacturer pricing sheets or look for recent supply chain publications. SuperPower, AMSC, Bruker all publish pricing in some contexts. DOE HTS roadmap documents may have current cost targets. `not-yet-sourced — search DOE 2023 superconductor roadmap documents`
+4. **Tritium startup inventory for FLiBe breeder**: ORNL FLiBe tritium extraction literature (e.g., Dolan, Forsberg work on FLiBe T extraction). The ARC paper cites Dolan 1992 (HYLIFE-II T extraction) and Fukada (FFHR-2) — these would provide T extraction efficiency data needed to size startup inventory.
 
-5. **FLiBe production scale and cost**: MSR fission community is a close proxy. Search for FLiBe supply chain analysis in DOE Molten Salt Reactor R&D literature or Kairos Power publications (Kairos uses FLiBe as coolant for pebble bed fission). `not-yet-sourced — search "FLiBe production capacity Kairos" or "BeF2 supply chain fusion"`
+5. **Beryllium supply chain**: USGS Mineral Commodity Summaries for Beryllium; US DoD strategic minerals assessments. ARC uses beryllium as neutron multiplier — supply and cost at fleet scale unassessed in current sources. `not-yet-sourced`.
 
-6. **O&M cost analogs** — *addressed (analog).* Araiinejad & Shirvan 2025 provides FTE-based fixed O&M (50–95 staff) and variable O&M (total 35–182 $/MWh, replaceable-component share 11–107 $/MWh). DEMO and ARIES plant studies remain a useful cross-check. `unverified — search "DEMO O&M cost tokamak" in Fusion Engineering and Design`
+6. **tea_dt_mfe_cost_analysis** (already in source index): This D-T MFE cost analysis at `knowledge/sources/tea_dt_mfe_cost_analysis/` has not been read but is directly applicable to ARC costing methodology and CAS breakdowns. Should be read before constructing the quantitative LCOE model.
 
-7. **Tritium startup and handling costs**: Reyes et al. 2021 or similar tritium fuel cycle analyses in NF or FED. Search for "tritium startup inventory fusion economics." `not-yet-sourced`
+7. **ARC cost drivers / compact pilot plant paper**: Sorbom, Ball et al. separately published a "cost drivers for compact pilot plant" paper after the 2015 ARC paper. Search OSTI for "Sorbom ARC cost drivers." `unverified — confirm existence before searching`.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis**: Yes, with caveats.
+**Proceed to full analysis**: Yes, with caveats. The concept has sufficient technical depth for a rigorous qualitative D1+ write-up and a parameterized first-pass LCOE model. The primary actions needed before building the quantitative model are: (1) read `knowledge/sources/tea_dt_mfe_cost_analysis/` for D-T MFE CAS methodology; (2) decide how to handle the missing BOP — either use a pyFECONS MFE run with ARC parameters or scale from ARIES-AT as an analog; (3) assume 80% capacity factor as a point estimate (justified by Schwartz et al. 2024 and generic fusion planning) with a 65–90% sensitivity range; (4) note the confinement assumption (H₉₈ = 2.8) as the dominant physics risk in the qualitative write-up.
 
-The HTS Compact Tokamak has unusually rich publicly available technical data for a private fusion venture. The Sorbom 2015 ARC paper provides the physics, engineering rationale, a materials costing table, and an explicit R&D gap list — all in one document. The ICRF and power conversion papers add detail on two specific subsystems. This is enough to build a parameterized LCOE model with clearly stated assumptions.
+The ARC 2015 reactor island cost ($5.5–5.6B, 2014$) is a low-confidence rough estimate dominated by the magnet structure and uses a simple volumetric scaling — do not use as a capital cost input without adjustment. The ARPA-E ALPHA costing structure (~$1.2B, $2.4/W, 43 $/MWh for ~500 MWe compact modular fusion) is a better-structured analog, though the magnet cost account (22.1.3) for those non-superconducting concepts is much lower than ARC's HTS-dominated magnet system. The pyFECONS MFE magnet account with ARC geometry and REBCO cost inputs is the recommended path for a defensible capital cost estimate.
 
-The main modeling challenges are:
-1. **Balance of plant** — uncosted in the primary source, but an ARC-class analog is now available (Araiinejad & Shirvan 2025: turbine generator 535–550 $/kW, electric plant 274–402 $/kW, heat rejection 70–88 $/kW, structures 819–1,317 $/kW, indirect 1,146–2,644 $/kW). Use these NOAK bounds, flagged as an independent academic analog; cross-check against ARIES-AT.
-2. **Capacity factor** — Araiinejad & Shirvan 2025 supplies an analog range (CF 0.5–0.7), enough to bound an LCOE model. But that range is generic NPP/fossil-derived; it does not reflect ARC's 6–12-month vacuum-vessel replacement cadence, so model availability parametrically from VV replacement frequency for ARC-specific accuracy.
-3. **The 2015 ARC design (200 MWe) ≠ the 2025 ARC commercial design (400 MWe)** — all capital cost numbers need rescaling, inflation adjustment (2014→2026), and ideally current REBCO pricing. Araiinejad & Shirvan 2025 models a 350 MWe ARC-class plant — a closer size match to the current 400 MWe target than the 2015 paper.
-4. **Divertor is the remaining blocking gap** — the ARC paper explicitly deferred it, and Araiinejad & Shirvan 2025 gives only a crude cost share (~10% of reactor plant equipment, "18 tungsten tiles"). Use a tungsten divertor cost and replacement schedule from ITER analogs and flag it as a high-uncertainty line item, or source an updated CFS/IAEA-FEC divertor design.
-
-Despite these gaps, the available data supports a D1+ analysis that covers all five required sections with honest uncertainty quantification. With the Araiinejad & Shirvan 2025 analog integrated, only the divertor remains a blocking LCOE gap; the rest are accuracy refinements estimable from analogs — they do not indicate fundamental unknowns about the concept's technical viability or cost structure.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 1
-important_count: 10
-counting_method: "section_5_missing_parameters"
+blocking_count: 4
+important_count: 6
+counting_method: "section_5_missing_parameters_and_section_gaps_deduplicated: blocking = {full plant capital cost, capacity factor, scheduled maintenance costs, tritium startup inventory}; important = {BOP cost analog, confinement H98 sensitivity to LCOE, beryllium supply chain, formal TRL assessment, divertor design and cost, recirculating power}"
 section_coverage:
   availability_of_data:       "Good"
-  system_function:            "Good"
-  subsystem_maturity:         "Partial"
+  system_function:            "Partial"
+  subsystem_maturity:         "Good"
   materials_supply_chain:     "Partial"
-  lcoe_parameter_extraction:  "Unknown"
-```
+  lcoe_parameter_extraction:  "Partial"
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
