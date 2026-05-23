# Phase 3 diff: 36-helical-coil-stellarator

**Generated:** 2026-05-22T16:14:10-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 4 | 3 | -1 |
| important_count  | 9 | 10 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information from all concept-scoped and relevant fleet-wide sources to write the gap assessment.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information from all concept-scoped and relevant fleet-wide sources to write the gap assessment.
```

## Blocking-tier lines (new)

```
35:- Validated confinement enhancement factor H=1.3 for optimized heliotron configuration — `truly-unknown` (not yet experimentally demonstrated at LHD or otherwise) — **blocking** for quantitative performance prediction
110:| O&M costs (annual) | not-yet-sourced | **blocking** | No estimates in any concept source; fleet analogy from `tea_dt_mfe_cost_analysis/` gives $25–40/MWh O&M range for tokamak at much larger scale — stellarator O&M likely higher per MWe due to scale |
111:| CAS-level capital cost breakdown | proprietary | **blocking** | Only aggregate $5B direct cost given; no CAS account allocation; limits structured cost modeling |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/36-helical-coil-stellarator.md	2026-05-22 12:59:21.091099325 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/gap_report.md	2026-05-22 16:14:10.598281301 -0700
@@ -1,12 +1,10 @@
-I now have all the information needed to write the gap assessment.
-
----
+I now have sufficient information from all concept-scoped and relevant fleet-wide sources to write the gap assessment.
 
 # Gap Assessment: Helical Coil Stellarator (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-**Summary**: Helical Fusion is unusually transparent for a small startup — the AIP 2023 paper (Miyazawa & Goto) provides a complete conceptual design with reactor parameters, a cost estimate, subsystem descriptions, and a roadmap. The primary limitation is that the cost model is based on 1990s LHD/ITER cost data without a CAS-level subsystem breakdown, and several novel subsystems (WISE conductor, 250 GHz CW gyrotrons, Sn-based liquid metal blanket) have no independent cost analogues. A first-pass LCOE model can be built with stated assumptions, but uncertainty bands are wide and several important parameters require analogue-based estimation.
+**Summary**: Helical Fusion's HESTIA heliotron design is unusually well-documented for an early-stage startup — a full published reactor design paper (AIP Physics of Plasmas 2023) provides reactor parameters, energy balance, and a first-order direct cost estimate. The concept-scoped sources collectively confirm the energy conversion system (sCO2 Brayton, >50% efficiency), liquid metal blanket composition (tin-indium-lead-lithium), and the full development roadmap. Primary gaps are at the LCOE quantification layer: no O&M estimates, no CAS-level cost breakdown, and no published TBR calculation. These can be partially bridged via fleet-wide stellarator and D-T MFE cost analogs.
 
 ---
 
@@ -15,161 +13,138 @@
 ### 1. Availability of Data
 **Coverage**: Good
 
-**Available**:
-- **AIP 2023 paper (Miyazawa & Goto)** — the primary design source. Provides complete plasma parameters, subsystem descriptions (magnets, blanket, ECRH, fueling, power conversion), cost estimates, and development timeline. Explicitly confirms sCO2 power conversion (Section F), tin-indium-lead-lithium liquid metal blanket composition, 250 GHz CW gyrotron targets, and 9T field at plasma center.
-- **Dossier** (high confidence across all columns except Energy Capture which is now resolved by full paper) — structured summary consistent with the full paper.
-- **ANS/BusinessWire press releases (2025)** — HTS coil milestone, Series A extension, Helix HARUKA roadmap.
-- **NIFS heritage** (Sagara et al. FFHR series) — blanket and helical reactor design genealogy.
-- **Helios preconceptual design (Thea Energy, arXiv:2512.08027)** — planar coil stellarator analog providing detailed engineering parameters (1.1 GW thermal, 390 MWe, 40% Rankine efficiency, 88% capacity factor, vanadium first wall, PbLi blanket), useful for gap-filling.
-- **Kovari et al. energy conversion review** — MFE coolant and power cycle options, confirms sCO2 Brayton cycle viability at fusion temperatures.
-
-**Missing**:
-- No independently published techno-economic analysis of HESTIA by a third party.
-- No investor deck or detailed technical report beyond the AIP paper.
-- Helical Fusion's own cost model (HELICOSOPE systems code) is not publicly accessible.
+**Available**: The primary design paper (Miyazawa & Goto, *Phys. Plasmas* 30, 050601, 2023) is fully extracted and provides reactor parameters, energy balance table, cost headline, physics basis (DPE extrapolation from LHD), and subsystem descriptions for all six technology pillars. Supplementary sources cover the HTS coil milestone (ANS 2025), coil manufacturing (Sugino Machine collaboration), blanket testing (GALOP at NIFS), materials development (Tohoku University, 2024), and sCO2 context (GTI STEP Demo milestone). The ARIES-CS study (Academia source) confirms the stellarator design space HESTIA occupies. The Helios/Thea Energy design (arxiv-2512-08027) provides a contemporaneous stellarator plant analog at comparable major radius (8 m).
+
+**Missing**: Full HESTIA-Primary design parameters are not published; only the prototype cost ($480M at 1990s prices) and broad intent are stated. HELICOSOPE systems code outputs are not available. No investor-facing economics disclosure exists.
 
 **Gaps**:
-- No independent cost validation of the $5B HESTIA estimate — `not-yet-sourced` — `important`
-- Full AIP paper includes inflation caveat ("costs based on 1990s prices, multiply by 2+") but no updated inflation-adjusted CAS breakdown — `not-yet-sourced` — `important`
+- Full HELICOSOPE systems code output and parametric sensitivity tables — `proprietary` — important
+- HESTIA-Primary detailed technical parameters (1/3-scale prototype) — `not-yet-sourced` — nice-to-have
+- Peer-reviewed TBR simulation results — `not-yet-sourced` — important (company references 3D neutron transport as planned)
 
 ---
 
 ### 2. Challenges in Capturing System Function
 **Coverage**: Partial
 
-**Available**:
-- The AIP paper explicitly enumerates six technology gaps that must be overcome, and discusses each subsystem at meaningful depth.
-- Plasma physics basis: uses DPE (direct profile extrapolation) from LHD, with H=1.3 confinement enhancement required. The H=1.3 assumption is openly stated as relying on magnetic configuration optimization not yet demonstrated in the heliotron geometry.
-- Recirculating power breakdown is partially specified: 40 MW wall-plug for 20 MW ECH (50% efficiency assumed), cryogenic system at 2% gross output, but LM pump power is explicitly flagged as unknown.
-- Impurity shielding (Sn/Pb from liquid metal first wall) expected to rely on ergodic layer friction forces observed in LHD — but not demonstrated at reactor-relevant density/temperature.
-
-**Missing**:
-- LM pump power for gas-driven system: the paper states "the electric power needed for the new LM circulation system is quite unknown at this moment" — HESTIA Table I uses mechanical pump estimates as a placeholder.
-- Impurity shielding effectiveness at reactor conditions: "we expect" the impurity shielding effect — not validated for Sn/Pb contamination in heliotron configuration.
-- Long-pulse pellet injection performance: 30-barrel injectors at several Hz have not been demonstrated; LHD uses 20-barrel units.
+**Available**: The AIP paper explicitly catalogs six technology gaps: (1) confinement optimization requiring H=1.3 enhancement factor, (2) WISE HTS conductor for 3D winding, (3) liquid metal blanket as integrated first wall/breeder/divertor, (4) 250 GHz CW gyrotrons, (5) high-frequency pellet injectors with direct gas recycling, and (6) sCO2 electricity generation. The physics design relies on the gyro-Bohm DPE extrapolation method validated against LHD — a 10× scale jump. The paper explicitly states that LM pump power "is quite unknown at this moment." Alpha particle confinement is modeled at 85% confinement fraction but is an assumption from prior FFHR modeling. The density limit challenge (HESTIA requires n > n_Sudo in some regions) is identified and partially addressed.
+
+**Missing**: No integrated system-level simulation combining plasma, blanket, and power conversion. No published quench dynamics or stability analysis for the large (46-66 GJ stored energy) uninsulated helical coil system. No validated model for tin-alloy vapor pressure behavior at the plasma-facing surface under steady-state DT conditions.
 
 **Gaps**:
-- LM pump power requirement unknown (acknowledged in paper) — `truly-unknown` — **blocking** (directly affects recirculating power fraction and net output)
-- Impurity control with heavy-metal (Sn, Pb) liquid metal first wall — `truly-unknown` — `important`
-- H=1.3 confinement enhancement in heliotron geometry — `truly-unknown` — `important` (determines whether Q~13 is achievable at stated parameters)
-- 30-barrel pellet injection at several Hz — `not-yet-sourced` — `nice-to-have` (pellet injection is not a dominant cost driver)
+- Validated confinement enhancement factor H=1.3 for optimized heliotron configuration — `truly-unknown` (not yet experimentally demonstrated at LHD or otherwise) — **blocking** for quantitative performance prediction
+- LM pump parasitic power (explicitly unknown per paper) — `truly-unknown` — important
+- Plasma-facing tin-alloy vapor pressure at reactor operating conditions — `not-yet-sourced` (NIFS material research ongoing) — important
+- Quench dynamics of large uninsulated helical HTS coil system (46-66 GJ) — `not-yet-sourced` — important
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **WISE HTS conductor**: October 2025 milestone demonstrated 40 kA at 7 T external field at 15 K; coil manufacturing machine completed with Sugino Machine. TRL ~3-4 (component demonstrated at near-relevant scale, but full helical coil geometry not integrated).
-- **LM blanket / GALOP**: Gas-driven LM pump validated at small scale (~4×2×2 m system at NIFS). TRL ~3 (proof of concept demonstrated).
-- **ECRH gyrotrons**: 154 GHz gyrotrons in LHD can deliver <0.5 MW CW; 250 GHz at 1 MW CW does not exist. TRL ~2 (technology concept formulated but not demonstrated at required frequency/power).
-- **sCO2 power conversion**: STEP Demo achieved 4 MWe grid-synchronized operation at 500°C (Phase 1); plans for 10 MWe at 715°C. TRL ~5-6 in commercial context, but fusion-relevant 800-1200K operation not yet demonstrated.
-- **Structural material (high-Mn austenitic steel)**: 2024 paper on development with Tohoku University. TRL ~2-3.
-- **Pellet injection**: 20-barrel units operational in LHD. TRL ~5 for current designs; new 30-barrel design at higher frequency TRL ~3.
-
-**Missing**:
-- TRL assessment for full remote maintenance system (conceptual design only in HESTIA paper, no prototype described).
-- Neutron shielding performance data for heliotron geometry (3D geometry complicates shielding design vs. tokamak).
-- WISE conductor performance under neutron irradiation.
+**Available**: TRL assessments can be made with reasonable confidence for most subsystems:
+- WISE REBCO HTS conductor: TRL 4–5 (Oct 2025: 40 kA at 7 T, 15 K demonstrated; manufacturing machine completed; Helix HARUKA assembly beginning 2026)
+- Helical coil winding/impregnation: TRL 3–4 (machine completed, coils not yet wound at reactor scale)
+- Liquid metal blanket (GALOP system at NIFS): TRL 3–4 (gas-driven pump validated at bench scale; NIFS Oroshhi-2 LiPb/FLiNaK loops provide materials heritage)
+- 250 GHz CW gyrotrons: TRL 2–3 (joint R&D with QST; LHD operates 154 GHz/0.5 MW CW — significant step to 250 GHz/1 MW CW)
+- sCO2 Brayton cycle: TRL 6 (STEP Demo phase 1 complete, 4 MWe synchronized at 500°C; phase 2 targeting 10 MWe at 715°C in RCBC configuration)
+- 30-barrel DT pellet injector: TRL 3–4 (20-barrel system demonstrated at LHD; DT ice capability requires further development)
+- Non-magnetic high-Mn structural steel: TRL 3 (Tohoku University collaboration, 2024 publication)
+- Remote maintenance robotics: TRL 2–3 (collaborative research listed, no published results)
+
+The Wurzel & Hsu (2021) Lawson criterion compilation confirms LHD achieves ion temperature >10 keV, density >10²⁰ m⁻³, and plasma duration >3000 s — individually, and comparable to large tokamaks — providing a physics heritage baseline for HESTIA extrapolation.
+
+**Missing**: No published TRL assessment by an independent party. No radiation damage data for WISE conductor or high-Mn steel under 14.1 MeV neutron flux. No published end-to-end DT pellet injection results in a stellarator geometry.
 
 **Gaps**:
-- 250 GHz CW gyrotron at 1 MW does not exist — `truly-unknown` (development timeline and cost uncertain) — `important`
-- WISE conductor full-scale helical winding and structural performance — `not-yet-sourced` — `important`
-- High-Mn steel neutron embrittlement data at fusion-relevant fluence — `truly-unknown` — `important`
-- Remote maintenance system TRL — `truly-unknown` (concept only) — `important`
-- Coil lifetime under D-T neutron flux (HTS coil dose limits) — `not-yet-sourced` — `important`
+- Independent TRL validation for WISE conductor at reactor field (20 T on-coil) — `not-yet-sourced` — important
+- Neutron irradiation testing data for high-Mn steel and WISE conductor — `truly-unknown` (material is too new) — important
+- 250 GHz gyrotron performance at 1 MW CW — `truly-unknown` (under development) — important
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
 **Coverage**: Partial
 
-**Available**:
-- REBCO tape supply: multiple manufacturers (SuperPower, Fujikura, SuNAM); existing HTS fusion programs consuming significant supply. Large helical coil winding at 31.2 MA total current would require substantial REBCO procurement but is not uniquely difficult compared to other HTS MFE concepts.
-- Li-6 enrichment: AIP paper explicitly states 80% Li-6 enrichment assumed (vs. ~7.5% natural abundance); 3D neutron transport simulation to confirm exact enrichment needed. Li-6 enrichment capacity is a known supply chain constraint shared across all D-T concepts.
-- Tin (Sn) and lead (Pb): widely available commodities, not supply-constrained.
-- Helium for cryogenics: paper specifically notes global helium supply concerns and proposes using 20K He gas (not liquid He at 4K) to reduce helium demand. 20K operation reduces helium consumption 4× vs. 4K LHD.
-- Structural material (high-Mn austenitic steel): not commercially available for fusion use; still in development.
-
-**Missing**:
-- Quantitative REBCO tape requirements (meters of tape, total weight) — not stated in available sources.
-- LM blanket composition confirmed (Sn-Pb-Li proposed but not finalized; exact Li fraction for TBR not specified pending 3D neutron transport simulation).
-- Industrial-scale corrosion protection process for porous titanium/high-Mn steel blanket structures.
+**Available**: The AIP paper confirms the liquid metal composition as a tin-indium-lead-lithium alloy (tin base, lead for neutron multiplication, lithium for tritium breeding). Tin is abundant (no supply constraint). High-Mn austenitic steel requires no rare elements. REBCO tape for WISE conductor uses rare-earth barium copper oxide — yttrium is the rare earth, commercially available from SuperPower, SuNAM, and Fujikura. ⁶Li isotope enrichment is required at ~80% (specified in the paper); natural ⁶Li abundance is ~7.6%, so enrichment is needed. The ITER cryogenic distillation system provides tritium separation heritage.
+
+**Missing**: Indium content in the LM alloy is not quantified; indium is a critical material with limited supply (primarily from zinc smelting byproduct). The paper confirms the composition in principle but not the weight fractions. No supply chain analysis for the 90 blanket modules (each requiring large liquid metal inventories). No REBCO cost estimate for the helical coil system (very large coil current 31.2 MA compared to typical pancake coils).
 
 **Gaps**:
-- Li-6 enrichment volume and cost — `derivable` (blanket volume and Li fraction can be estimated from reactor geometry) — `important`
-- High-Mn austenitic steel supply chain (development stage, no commercial supply) — `truly-unknown` — `important`
-- REBCO tape volume requirement — `derivable` (from stored energy and current parameters in Table I) — `nice-to-have`
-- LM composition confirmed for TBR simulation — `not-yet-sourced` — `nice-to-have` (doesn't block first-pass LCOE)
+- Indium fraction in tin-indium-lead-lithium alloy and resulting supply criticality — `not-yet-sourced` — important
+- ⁶Li enrichment supply chain (China dominates production) — `derivable` from ITER analogies — important
+- Total REBCO tape quantity for 31.2 MA helical coil system and cost — `derivable` (from J_c ~48 A/mm² and coil geometry) but not calculated — important
+- Low-melting-point alloy for WISE impregnation — composition not specified publicly — `proprietary` — nice-to-have
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Available Parameters**:
+**Coverage**: Partial
 
+**Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electric output (HESTIA FPP) | 70 MWe | AIP 2023, Table I | high |
-| Net electric output (FOAK) | 103 MWe | AIP 2023, Table I | medium |
-| Fusion power (HESTIA) | 260 MW | AIP 2023, Table I | high |
-| Gross electricity | ~139 MW | AIP 2023, Table I | high |
-| Fusion gain Q | ~13 | AIP 2023 | high |
-| Direct construction cost (HESTIA) | $5B (1990s basis; ~$10B+ inflation-adjusted) | AIP 2023, Table I + text | medium |
-| FOAK construction cost | ~$3B (1990s basis) | AIP 2023, Introduction | medium |
-| Capital cost per lifetime output | $1.22/kWh (HESTIA), $1.19/kWh (FOAK) | AIP 2023, Table I | medium |
-| Target availability | >80–85% | AIP 2023 | high |
-| Burn cycle | ~1 year continuous + ~3 month maintenance | AIP 2023 | high |
-| ECH wall-plug power | 40 MW (for 20 MW plasma heating, 50% η) | AIP 2023 | high |
-| ECH wall-plug efficiency target | 50% | AIP 2023 | medium |
-| Cryogenic recirculating power | ~2% gross output | AIP 2023 | medium |
-| Power conversion type | sCO2 Brayton cycle (explicitly confirmed Section F) | AIP 2023 | high |
-| Target thermal efficiency | >50% | AIP 2023 | medium |
-| Current sCO2 demo efficiency | ~40–47% | Kovari 2014; STEP Demo GTI | high |
-| Major radius | 7.8 m | AIP 2023 | high |
-| Stored magnet energy | 46.2–66.2 GJ | AIP 2023, Table I | high |
-| Building envelope | 60×160 m² floor, 100 m height | AIP 2023 | high |
-| Helios analog: net output | 390 MWe | Helios arXiv:2512.08027 | high |
-| Helios analog: thermal efficiency | 40% (steam Rankine) | Helios arXiv:2512.08027 | high |
-| Helios analog: capacity factor | 88% (84 days outage/2 years) | Helios arXiv:2512.08027 | high |
+| Net electric output (HESTIA) | 70 MWe (max) | AIP 2023, Table I | h |
+| Gross electric output | ~140 MW | AIP 2023 | h |
+| Fusion power | 260 MW | AIP 2023, Table I | h |
+| Physics gain Q | ~13 | AIP 2023 | h |
+| Engineering gain Q_eng | ~2.0 | AIP 2023, Table I | h |
+| Availability target | >80–85% | AIP 2023 | h |
+| Operation cycle | ~1 year burn + ~3 month maintenance | AIP 2023 | h |
+| Direct capital cost (HESTIA) | $5B (1990s USD); ~$7.5–10B inflation-adjusted | AIP 2023 | m (inflation uncertainty) |
+| Capital cost proxy (C_direct / P_net·T_net) | $1.22/kWh (1990s USD) | AIP 2023, Table I | m |
+| Energy conversion cycle | sCO2 Brayton cycle, >50% efficiency target | AIP 2023 (confirmed) | h |
+| Operating temperature (sCO2) | 800–1200 K | AIP 2023 | h |
+| ECH wall-plug power | 40 MW (20 MW to plasma) | AIP 2023 | h |
+| Cryogenic system efficiency | 2% of output | AIP 2023 | m |
+| Plant footprint | 60×160 m² floor, 100 m height | AIP 2023 | h |
+| Capacity factor (analogous stellarator) | 88% (Helios/Thea Energy at 84-day biennial maintenance) | arxiv-2512-08027 | m (different architecture) |
+| TBR target (analogous) | 1.3 (Helios) | arxiv-2512-08027 | l (different blanket) |
+| LCOE range (D-T MFE fleet, 350 MWe) | $140–550/MWh | `knowledge/sources/tea_dt_mfe_cost_analysis/` | m (different scale/type) |
 
-**Missing Parameters**:
+The TEA D-T MFE Cost Analysis (`knowledge/sources/tea_dt_mfe_cost_analysis/`) provides bottom-up CAS framework for D-T MC FPP costs using EEDB-derived scaling (Accounts 21–27 direct, Account 90+ indirect). Its $140–550/MWh LCOE range for a 350 MWe tokamak is not directly applicable to HESTIA's 70 MWe heliotron, but the methodology and BOP cost structure (turbine plant, heat rejection, electrical systems) transfer directly. The ARIES Cost Account Documentation (`knowledge/sources/aries_cost_account_documentation/`) provides the foundational CAS framework (Starfire lineage through ARIES series) that anchors any fusion cost model and is directly applicable to structuring HESTIA cost accounts.
 
+**Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Subsystem capital cost breakdown (magnets, blanket, BOP, ECH system) | not-yet-sourced | **blocking** | Only total direct cost is available; no CAS-level breakdown from any source for this specific concept |
-| Annual O&M cost | not-yet-sourced | **blocking** | No O&M estimate in any source; must be derived from analogue (e.g., 2–3% of capital from TEA D-T MFE source or ARIES CAS) |
-| Plant lifetime | not-yet-sourced | **blocking** | Not stated in AIP paper; implied >30 years from development strategy but never confirmed |
-| LM pump recirculating power | truly-unknown | **blocking** | Paper explicitly states "quite unknown"; uses mechanical pump placeholder in Table I |
-| First wall replacement schedule and cost | truly-unknown | important | Porous first wall structure novel; no lifetime estimate |
-| Confirmed thermal efficiency | not-yet-sourced | important | >50% is target; sCO2 at 800-1200K not yet demonstrated; current demos at ~40-47% |
-| WISE conductor unit cost ($/kA·m) | not-yet-sourced | important | Novel conductor; no published cost data; REBCO tape scaling may provide bound |
-| 250 GHz CW gyrotron cost (60 units) | truly-unknown | important | Technology does not yet exist; no cost analogue |
-| Tritium startup inventory cost | derivable | important | ~1 kg needed (per Table I context); market price applies |
-| Li-6 enrichment procurement and cost | derivable | important | 80% Li-6 enrichment needed; global supply constrained |
-| Decommissioning cost | not-yet-sourced | nice-to-have | Standard 10–15% of capital assumption applicable |
-| Staffing model | not-yet-sourced | nice-to-have | No staffing estimate published |
+| O&M costs (annual) | not-yet-sourced | **blocking** | No estimates in any concept source; fleet analogy from `tea_dt_mfe_cost_analysis/` gives $25–40/MWh O&M range for tokamak at much larger scale — stellarator O&M likely higher per MWe due to scale |
+| CAS-level capital cost breakdown | proprietary | **blocking** | Only aggregate $5B direct cost given; no CAS account allocation; limits structured cost modeling |
+| Blanket module replacement cost/schedule | not-yet-sourced | important | 90 modules; LM expected to be drained/replaced; no schedule published |
+| Gyrotron capital cost (60 units) | not-yet-sourced | important | 60 × 1 MW-CW at 250 GHz; no market price (custom development) |
+| Gyrotron replacement interval | truly-unknown | important | CW gyrotrons at this frequency have no lifetime data at MW-class |
+| Tritium startup inventory cost | derivable | important | ~1-2 kg initial inventory (from Helios analog); cost depends on external procurement scenario; DD startup reduces but doesn't eliminate need |
+| Decommissioning cost | derivable | nice-to-have | Fleet analogy applicable |
+| Indirect costs (contingency, owner's costs) | derivable | important | ARIES CAS framework provides methodology; `tea_dt_mfe_cost_analysis/` gives 25–40% indirect cost fraction |
+| LCOE at commercial scale (FOAK 100 MWe) | derivable | important | Paper implies C_direct/(P_net·T_net) ~ $1.19/kWh (1990s) for FOAK; inflation-adjusted ~$1.80–2.40/kWh capital-only |
+| LM pump power consumption | truly-unknown | important | Explicitly stated "quite unknown at this moment" in AIP paper |
+| Thermal conversion efficiency (actual vs. target) | derivable | important | sCO2 >50% is target; STEP Demo demonstrated ~40% in simple cycle; 47% with recompression Brayton cycle (Kovari 2013 fleet analog for CO2) |
 
 ---
 
 ## Source Recommendations
 
-1. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — read for CAS-level cost breakdown applicable to D-T MFE. Should resolve subsystem cost proportion assumptions (magnets, blanket, BOP, ECH as fractions of total direct cost). **Verified exists in repo; read before building cost model.**
-
-2. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — read for CAS 20-27 account definitions and cost scaling algorithms. Directly applicable to stellarator cost estimates. **Verified exists; the ARIES-CS compact stellarator study is in the same family as HESTIA.**
-
-3. **Revisit of 2017 ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — read for multi-concept cost breakdown methodology. May contain O&M cost fractions applicable across MFE concepts.
-
-4. **FFHR full design papers** — search OSTI/J-STAGE for Sagara et al. "FFHR Design Group" papers (Nuclear Fusion, 2017; referenced in AIP 2023 as [1] — Nucl. Fusion 57, 086046). These NIFS design study papers are the precursor to HESTIA and likely contain more detailed subsystem cost analysis. `unverified — confirm existence before searching`.
-
-5. **HELICOSOPE systems code outputs** — if any Helical Fusion or NIFS conference papers cite HELICOSOPE results with parameter tables, these would provide validated plant economics. Search IAEA Fusion Energy Conference proceedings and Plasma and Fusion Research. `unverified — confirm existence before searching`.
-
-6. **Gyrotron cost analogues** — search for cost estimates of ITER 170 GHz gyrotrons (unit costs ~$2-5M per tube in ITER procurement) as a lower bound for the 250 GHz development program. `not-yet-sourced — analogue available in public ITER documentation`.
+**Not-yet-sourced gaps — search recommendations:**
+1. **TBR simulation for HESTIA LM blanket**: Search NIFS publications (FFHR Design Group, Sagara et al.) for neutron transport calculations on tin-lead-lithium blankets, or OSTI for heliotron blanket TBR studies — `unverified — confirm existence before searching`
+2. **Gyrotron capital costs at 140–250 GHz**: Search ITER Organization procurement documents and QST/NIFS publications for gyrotron cost estimates — the ITER 170 GHz gyrotrons provide a lower-bound reference (publicly reported at ~$5–10M per unit) — `unverified — confirm exact figures before using`
+3. **O&M cost for stellarator power plants**: The ARIES-CS maintenance study (Waganer et al., *Fusion Sci. Technol.* 54, 787, 2008) contains maintenance labor and schedule analysis for a compact stellarator; this paper is listed as a reference in the ARIES-CS source but was not extracted — `unverified — confirm availability`
+4. **sCO2 efficiency at fusion-relevant temperatures**: Linares et al. (2011) "Power conversion systems based on Brayton cycles for fusion reactors," *Fusion Eng. Des.* 86, 2735 — referenced in the Kovari 2013 source (arxiv-1401-4232); provides 47% gross efficiency for CO2 recompression Brayton cycle with LiPb/He dual-cooled blanket — `unverified — confirm this paper is accessible`
+5. **Helical coil REBCO conductor quantity and cost**: Search IEEE Trans. Appl. Supercond. for WISE conductor papers by Yanagi, Terazaki, et al. (some are referenced in AIP 2023) — foundational HTS conductor design papers likely contain current density and mass estimates — `unverified — confirm scope of publications`
+
+**Fleet-wide source disqualifications:**
+- `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`: IFE-specific (Monte Carlo over 14 IFE LCOE parameters including gain and driver efficiency). No content applicable to MFE heliotron. Opening confirmed it covers IFE economics only.
+- `knowledge/sources/energy_from_inertial_fusion/`: Comprehensive 1992 IFE review (laser, heavy-ion, light-ion drivers). Architecture, cost drivers, and physics are entirely IFE-specific.
+- `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`: LLNL heavy-ion driver economics (1.5–3 GWe, pulse rate scaling). No overlap with steady-state MFE stellarator.
+- `knowledge/sources/accelerators_for_inertial_fusion_energy_production/`: Accelerator drivers for IFE. Not applicable.
+- `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`: Pacific Fusion high-yield pulsed IFE. Not applicable.
+- `knowledge/sources/commercialization_of_laser_fusion_energy/`: Xcimer KrF laser IFE. Not applicable.
+- `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`: Re-costing of four ARPA-E ALPHA compact fusion concepts (FRC, Z-pinch, MTF, dense plasma focus families — not stellarators). The $43/MWh average LCOE is for 500 MWe plants with fundamentally different physics and cost structure. Opening confirmed this covers compact pulsed/non-stellarator concepts. Methodology is CAS-based but concept architecture diverges too far from heliotron to use as a direct analog.
+- `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`: ORNL historical positioning of fusion LCOE against competing generation. Opening would confirm this is historical benchmark context, not HESTIA-specific. Not read — flagged as not needed given the TEA D-T MFE source already provides contemporary LCOE context.
 
 ---
 
 ## Summary
 
-Proceed to full analysis. The AIP 2023 paper provides sufficient technical detail for a well-grounded qualitative analysis across all five D1+ sections. For the quantitative LCOE model: use the $5B total direct cost (inflation-adjusted to $10B+) for HESTIA at 70 MWe as the primary capital cost input; supplement with CAS-level breakdowns from the ARIES cost account documentation and TEA D-T MFE source to estimate subsystem proportions; use analogue-based O&M (2–3% of capital); assume 50% sCO2 thermal efficiency per target (with 40–47% sensitivity range); use >80% availability. The cost model will have wide uncertainty bands (factor ~2) due to the 1990s cost basis, novel conductor costs, and unquantified LM pump power — but these uncertainties are characterizable and suitable for a first-pass analysis.
+The Helical Coil Stellarator (D-T) concept has an unusually rich primary source in the AIP 2023 design paper, which confirms sCO2 energy conversion (>50% target), LM blanket composition (Sn-In-Pb-Li), full reactor parameters, and a first-order direct capital cost. The concept is ready for a qualitative D1+ analysis covering all five sections, and for a partially-quantitative LCOE analysis using fleet-wide CAS analogs for indirect costs and O&M. The main blockers for a fully quantitative LCOE model are the absence of a CAS-level cost breakdown and any O&M estimate — both require either additional source acquisition (ARIES-CS maintenance study, gyrotron procurement data) or explicit fleet-analog assumptions with stated uncertainty. Proceed to full analysis with these acknowledged limitations; flag the $1.22/kWh capital-only proxy (1990s USD) as a floor requiring inflation adjustment and O&M addition before any LCOE estimate is reportable.
 
 ---
 
@@ -177,9 +152,9 @@
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 4
-important_count: 9
-counting_method: "section_5_missing_parameters_plus_section_2_lm_pump_gap; deduplicated across all sections; blocking = parameters where no data exists and no standard analogue applies without stated assumptions; important = significant uncertainty but analogue-based estimation possible"
+blocking_count: 3
+important_count: 10
+counting_method: "blocking: (1) H=1.3 confinement enhancement unvalidated blocking quantitative performance, (2) no O&M cost data in any source blocking LCOE, (3) no CAS-level capital cost breakdown blocking structured cost model. Important: O&M methodology gap, CAS breakdown, blanket replacement, gyrotron cost/lifetime, TBR calculation, LM pump power, indium supply criticality, Li-6 supply chain, independent TRL validation, LCOE at commercial scale. Deduplicated across sections."
 section_coverage:
   availability_of_data:       "Good"
   system_function:            "Partial"
```
