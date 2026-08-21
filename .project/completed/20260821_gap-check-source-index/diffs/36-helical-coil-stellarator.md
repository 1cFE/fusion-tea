# Diff: 36-helical-coil-stellarator

**Generated:** 2026-05-22T11:27:39-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 1 | 4 | 3 |
| important_count  | 8 | 9 | - |
| overall_rating   | Mostly Ready | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
156:1. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — read for CAS-level cost breakdown applicable to D-T MFE. Should resolve subsystem cost proportion assumptions (magnets, blanket, BOP, ECH as fractions of total direct cost). **Verified exists in repo; read before building cost model.**
158:2. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — read for CAS 20-27 account definitions and cost scaling algorithms. Directly applicable to stellarator cost estimates. **Verified exists; the ARIES-CS compact stellarator study is in the same family as HESTIA.**
160:3. **Revisit of 2017 ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — read for multi-concept cost breakdown methodology. May contain O&M cost fractions applicable across MFE concepts.
```

## Blocking-tier lines (baseline)

```
58:- Plasma confinement scaling validation (LHD → HESTIA) — `proprietary` / `not-yet-sourced` — **blocking** (the central physics claim; no published scaling confirmation found)
```

## Blocking-tier lines (new)

```
52:- LM pump power requirement unknown (acknowledged in paper) — `truly-unknown` — **blocking** (directly affects recirculating power fraction and net output)
139:| Subsystem capital cost breakdown (magnets, blanket, BOP, ECH system) | not-yet-sourced | **blocking** | Only total direct cost is available; no CAS-level breakdown from any source for this specific concept |
140:| Annual O&M cost | not-yet-sourced | **blocking** | No O&M estimate in any source; must be derived from analogue (e.g., 2–3% of capital from TEA D-T MFE source or ARIES CAS) |
141:| Plant lifetime | not-yet-sourced | **blocking** | Not stated in AIP paper; implied >30 years from development strategy but never confirmed |
142:| LM pump recirculating power | truly-unknown | **blocking** | Paper explicitly states "quite unknown"; uses mechanical pump placeholder in Table I |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/36-helical-coil-stellarator.md	2026-05-22 09:21:13.887224893 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/gap_report.md	2026-05-22 11:27:39.510951025 -0700
@@ -1,39 +1,36 @@
-Now I have everything I need. Let me write the gap assessment.
+I now have all the information needed to write the gap assessment.
 
 ---
 
-# Gap Assessment: Helical Coil Stellarator
+# Gap Assessment: Helical Coil Stellarator (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: Helical Fusion is unusually transparent for an early-stage startup, having published a primary reactor design paper (HESTIA, AIP 2023) with construction cost and performance targets. The qualitative sections are well-supported across five sources. The main gap for LCOE is the absence of any subsystem-level cost breakdown — only the total $5B construction figure is published — and unconfirmed power conversion efficiency. These gaps are real but workable: the total cost enables a top-down LCOE estimate, and key parameters (thermal power, efficiency) are derivable with stated assumptions.
+**Summary**: Helical Fusion is unusually transparent for a small startup — the AIP 2023 paper (Miyazawa & Goto) provides a complete conceptual design with reactor parameters, a cost estimate, subsystem descriptions, and a roadmap. The primary limitation is that the cost model is based on 1990s LHD/ITER cost data without a CAS-level subsystem breakdown, and several novel subsystems (WISE conductor, 250 GHz CW gyrotrons, Sn-based liquid metal blanket) have no independent cost analogues. A first-pass LCOE model can be built with stated assumptions, but uncertainty bands are wide and several important parameters require analogue-based estimation.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Good
 
 **Available**:
-- Primary reactor design paper published in a peer-reviewed journal (AIP Physics of Plasmas 30, 050601 (2023)) with top-level performance parameters, construction cost estimate, and key technology choices
-- Company website with collaborative research structure (14 named areas), technology roadmap (HARUKA → KANATA → HESTIA), and milestone press releases
-- 2025 milestone: HTS coil demonstrated at 40 kA / 7 T / 15 K (ANS Newswire, BusinessWire)
-- NIFS heritage documentation: Oroshhi-2 platform, FFHR blanket program, sCO2 demo plan (Ishiyama & Tanaka 2019)
-- Tohoku University materials paper (Nuclear Materials and Energy, March 2024) on blanket structural material
-- GALOP blanket test system announcement (public press release)
+- **AIP 2023 paper (Miyazawa & Goto)** — the primary design source. Provides complete plasma parameters, subsystem descriptions (magnets, blanket, ECRH, fueling, power conversion), cost estimates, and development timeline. Explicitly confirms sCO2 power conversion (Section F), tin-indium-lead-lithium liquid metal blanket composition, 250 GHz CW gyrotron targets, and 9T field at plasma center.
+- **Dossier** (high confidence across all columns except Energy Capture which is now resolved by full paper) — structured summary consistent with the full paper.
+- **ANS/BusinessWire press releases (2025)** — HTS coil milestone, Series A extension, Helix HARUKA roadmap.
+- **NIFS heritage** (Sagara et al. FFHR series) — blanket and helical reactor design genealogy.
+- **Helios preconceptual design (Thea Energy, arXiv:2512.08027)** — planar coil stellarator analog providing detailed engineering parameters (1.1 GW thermal, 390 MWe, 40% Rankine efficiency, 88% capacity factor, vanadium first wall, PbLi blanket), useful for gap-filling.
+- **Kovari et al. energy conversion review** — MFE coolant and power cycle options, confirms sCO2 Brayton cycle viability at fusion temperatures.
 
 **Missing**:
-- Full text of AIP 2023 paper (paywalled) — abstract covers the key parameters but the body likely contains plasma parameter tables, subsystem sizing, and power balance details
-- Any conference proceedings from FPA, IAEA, or SOFT that may cover HESTIA in more depth
-- Investor materials or technical pitch decks (if any have been shared)
-- Any system code study from NIFS applying to the HESTIA geometry (the FFHR line used the HELIOS system code)
+- No independently published techno-economic analysis of HESTIA by a third party.
+- No investor deck or detailed technical report beyond the AIP paper.
+- Helical Fusion's own cost model (HELICOSOPE systems code) is not publicly accessible.
 
 **Gaps**:
-- Full AIP 2023 paper body — `not-yet-sourced` — **important** (may contain power balance, subsystem masses, full plasma parameter set)
-- Conference proceedings (FPA, IAEA Fusion Energy, SOFT) — `not-yet-sourced` — **important** (Helical Fusion/NIFS regularly present at these)
-- HELIOS/PROCESS system code runs for HESTIA geometry — `not-yet-sourced` — **nice-to-have**
+- No independent cost validation of the $5B HESTIA estimate — `not-yet-sourced` — `important`
+- Full AIP paper includes inflation caveat ("costs based on 1990s prices, multiply by 2+") but no updated inflation-adjusted CAS breakdown — `not-yet-sourced` — `important`
 
 ---
 
@@ -41,24 +38,21 @@
 **Coverage**: Partial
 
 **Available**:
-- Core physics advantages are documented: no disruption risk, no current drive power, steady-state operation rationale
-- Two technology "pillars" for Helix HARUKA identified: HTS magnets and integrated blanket/divertor system
-- ECRH identified as sole heating mechanism (250 GHz, 1 MW CW gyrotrons, joint R&D with QST)
-- Liquid metal blanket multi-function role documented: tritium breeding + first wall + neutron shield + heat removal (no separate divertor)
-- Q~13 and 50 MWe target give enough to frame recirculating power fraction
+- The AIP paper explicitly enumerates six technology gaps that must be overcome, and discusses each subsystem at meaningful depth.
+- Plasma physics basis: uses DPE (direct profile extrapolation) from LHD, with H=1.3 confinement enhancement required. The H=1.3 assumption is openly stated as relying on magnetic configuration optimization not yet demonstrated in the heliotron geometry.
+- Recirculating power breakdown is partially specified: 40 MW wall-plug for 20 MW ECH (50% efficiency assumed), cryogenic system at 2% gross output, but LM pump power is explicitly flagged as unknown.
+- Impurity shielding (Sn/Pb from liquid metal first wall) expected to rely on ergodic layer friction forces observed in LHD — but not demonstrated at reactor-relevant density/temperature.
 
 **Missing**:
-- Plasma confinement physics validation: confinement scaling from LHD to reactor scale is not publicly confirmed (the "factor of N" extrapolation from LHD parameters to HESTIA)
-- Neoclassical transport losses in heliotron geometry at reactor scale (a well-known challenge for stellarators; Helical Fusion claims mitigation but no published data)
-- Power balance table: how much ECRH power input is required at Q~13? What fraction of gross electricity is recirculated?
-- Divertor heat flux handling via liquid metal flow: quantitative heat load and flow rate data
-- MHD pressure drop in liquid metal loops under magnetic field (classic LM blanket challenge)
+- LM pump power for gas-driven system: the paper states "the electric power needed for the new LM circulation system is quite unknown at this moment" — HESTIA Table I uses mechanical pump estimates as a placeholder.
+- Impurity shielding effectiveness at reactor conditions: "we expect" the impurity shielding effect — not validated for Sn/Pb contamination in heliotron configuration.
+- Long-pulse pellet injection performance: 30-barrel injectors at several Hz have not been demonstrated; LHD uses 20-barrel units.
 
 **Gaps**:
-- Plasma confinement scaling validation (LHD → HESTIA) — `proprietary` / `not-yet-sourced` — **blocking** (the central physics claim; no published scaling confirmation found)
-- ECRH power budget at full Q~13 operating point — `not-yet-sourced` — **important** (needed for net efficiency calculation; derivable to first order if Q is trusted)
-- Liquid metal MHD and heat removal quantitative data — `not-yet-sourced` — **important** (conference papers from NIFS/GALOP team likely exist)
-- Neoclassical transport loss fraction at HESTIA scale — `proprietary` / `truly-unknown` — **important** (fundamental stellarator engineering challenge)
+- LM pump power requirement unknown (acknowledged in paper) — `truly-unknown` — **blocking** (directly affects recirculating power fraction and net output)
+- Impurity control with heavy-metal (Sn, Pb) liquid metal first wall — `truly-unknown` — `important`
+- H=1.3 confinement enhancement in heliotron geometry — `truly-unknown` — `important` (determines whether Q~13 is achievable at stated parameters)
+- 30-barrel pellet injection at several Hz — `not-yet-sourced` — `nice-to-have` (pellet injection is not a dominant cost driver)
 
 ---
 
@@ -66,25 +60,24 @@
 **Coverage**: Partial
 
 **Available**:
-- **HTS magnets (WISE REBCO)**: Demonstrated at 40 kA / 7 T / 15 K at conductor scale (>4 m length, 30 REBCO layers, ~3 cm cross-section) — Oct 2025 milestone. Coil manufacturing machine completed with Sugino Machine. TRL ~3-4 at conductor/coil level; full helical coil winding at HESTIA scale undemonstrated.
-- **ECRH gyrotrons**: R&D stage at 250 GHz / 1 MW CW. Joint program with QST. 250 GHz is significantly above demonstrated continuous-wave high-power gyrotron frequencies (170 GHz for ITER); TRL ~2-3.
-- **Liquid metal blanket**: GALOP test system validates gas-driven pump mechanism at lab scale (~4m×2m×2m). TRL ~2-3.
-- **Structural material**: Tohoku University collaboration on high-Mn alumina-forming austenitic steel published (2024); material characterized but not fabricated at blanket module scale.
-- **Solid pellet fueling**: Listed as collaborative research area; off-the-shelf technology from existing fusion programs.
-- **Roadmap context**: Helix HARUKA (integrated demo) is at assembly-initiation stage in 2026. KANATA (pilot) targeted for 2030s.
+- **WISE HTS conductor**: October 2025 milestone demonstrated 40 kA at 7 T external field at 15 K; coil manufacturing machine completed with Sugino Machine. TRL ~3-4 (component demonstrated at near-relevant scale, but full helical coil geometry not integrated).
+- **LM blanket / GALOP**: Gas-driven LM pump validated at small scale (~4×2×2 m system at NIFS). TRL ~3 (proof of concept demonstrated).
+- **ECRH gyrotrons**: 154 GHz gyrotrons in LHD can deliver <0.5 MW CW; 250 GHz at 1 MW CW does not exist. TRL ~2 (technology concept formulated but not demonstrated at required frequency/power).
+- **sCO2 power conversion**: STEP Demo achieved 4 MWe grid-synchronized operation at 500°C (Phase 1); plans for 10 MWe at 715°C. TRL ~5-6 in commercial context, but fusion-relevant 800-1200K operation not yet demonstrated.
+- **Structural material (high-Mn austenitic steel)**: 2024 paper on development with Tohoku University. TRL ~2-3.
+- **Pellet injection**: 20-barrel units operational in LHD. TRL ~5 for current designs; new 30-barrel design at higher frequency TRL ~3.
 
 **Missing**:
-- Integrated coil winding demonstration at helical scale (a full helical coil segment, not just double-pancake test piece)
-- Blanket module design with full tritium breeding ratio calculation
-- Gyrotron performance data at 250 GHz (output power, efficiency, CW operation duration)
-- Remote maintenance robot system (listed as collaborative research area, no milestone data)
-- Vacuum vessel design and scale
+- TRL assessment for full remote maintenance system (conceptual design only in HESTIA paper, no prototype described).
+- Neutron shielding performance data for heliotron geometry (3D geometry complicates shielding design vs. tokamak).
+- WISE conductor performance under neutron irradiation.
 
 **Gaps**:
-- Full-scale helical coil demonstration — `proprietary` (in progress, HARUKA) — **blocking for pilot, important for analysis** (currently the single biggest engineering unknown)
-- 250 GHz CW gyrotron performance data — `proprietary` / `not-yet-sourced` — **important** (needed for heating efficiency and recirculating power)
-- TBR calculation for HESTIA blanket geometry — `not-yet-sourced` — **important** (NIFS has published TBR studies for FFHR; HESTIA TBR likely in full AIP paper)
-- Remote maintenance system TRL — `not-yet-sourced` — **nice-to-have**
+- 250 GHz CW gyrotron at 1 MW does not exist — `truly-unknown` (development timeline and cost uncertain) — `important`
+- WISE conductor full-scale helical winding and structural performance — `not-yet-sourced` — `important`
+- High-Mn steel neutron embrittlement data at fusion-relevant fluence — `truly-unknown` — `important`
+- Remote maintenance system TRL — `truly-unknown` (concept only) — `important`
+- Coil lifetime under D-T neutron flux (HTS coil dose limits) — `not-yet-sourced` — `important`
 
 ---
 
@@ -92,114 +85,105 @@
 **Coverage**: Partial
 
 **Available**:
-- **REBCO tape**: Identified as primary superconductor. Proprietary WISE conductor uses stacked REBCO tapes. REBCO is commercially produced (Fujikura, SuNAM, AMSC) but at limited volumes; scale-up for two continuous multi-kilometer helical coils is a supply chain challenge.
-- **Liquid metal**: Lithium-bearing metal required for tritium breeding. Specific composition unconfirmed (Li, LiPb, or other). Li-6 enrichment requirement unknown.
-- **Structural steel**: High-Mn austenitic steel (non-magnetic, low-activation) — novel alloy under development; not yet commercially available.
-- **Gyrotrons**: 250 GHz CW devices require specialized manufacturing; no commercial supplier currently produces at this frequency/power.
-- **Funding context**: $38M raised total (including $13M Japan SBIR); modest for the scope, suggesting supply chain development is still upstream.
+- REBCO tape supply: multiple manufacturers (SuperPower, Fujikura, SuNAM); existing HTS fusion programs consuming significant supply. Large helical coil winding at 31.2 MA total current would require substantial REBCO procurement but is not uniquely difficult compared to other HTS MFE concepts.
+- Li-6 enrichment: AIP paper explicitly states 80% Li-6 enrichment assumed (vs. ~7.5% natural abundance); 3D neutron transport simulation to confirm exact enrichment needed. Li-6 enrichment capacity is a known supply chain constraint shared across all D-T concepts.
+- Tin (Sn) and lead (Pb): widely available commodities, not supply-constrained.
+- Helium for cryogenics: paper specifically notes global helium supply concerns and proposes using 20K He gas (not liquid He at 4K) to reduce helium demand. 20K operation reduces helium consumption 4× vs. 4K LHD.
+- Structural material (high-Mn austenitic steel): not commercially available for fusion use; still in development.
 
 **Missing**:
-- REBCO tape quantity estimate for HESTIA's two helical coils (length × cross-section gives tape volume; not published)
-- Li-6 enrichment requirement and global supply capacity
-- Low-melting-point alloy specification for WISE impregnation (determines availability and properties)
-- Magnet cooling system design (cryostat, cryocoolers for 15 K operation at reactor scale)
+- Quantitative REBCO tape requirements (meters of tape, total weight) — not stated in available sources.
+- LM blanket composition confirmed (Sn-Pb-Li proposed but not finalized; exact Li fraction for TBR not specified pending 3D neutron transport simulation).
+- Industrial-scale corrosion protection process for porous titanium/high-Mn steel blanket structures.
 
 **Gaps**:
-- REBCO tape quantity for full HESTIA coil set — `derivable` (from coil geometry + conductor specs) — **important** (cost driver)
-- Li-6 enrichment level and annual tritium inventory — `not-yet-sourced` — **important** (fuel cost and supply risk)
-- WISE impregnation alloy identity — `proprietary` — **nice-to-have** (affects conductor performance/cost)
-- Cryostat system design and scale — `not-yet-sourced` — **nice-to-have**
+- Li-6 enrichment volume and cost — `derivable` (blanket volume and Li fraction can be estimated from reactor geometry) — `important`
+- High-Mn austenitic steel supply chain (development stage, no commercial supply) — `truly-unknown` — `important`
+- REBCO tape volume requirement — `derivable` (from stored energy and current parameters in Table I) — `nice-to-have`
+- LM composition confirmed for TBR simulation — `not-yet-sourced` — `nice-to-have` (doesn't block first-pass LCOE)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Total construction cost (HESTIA) | USD 5 billion | AIP 2023 abstract | medium — company estimate, no breakdown |
-| Net electrical output | 50 MWe | AIP 2023 | high |
-| Follow-on plant output | 100 MWe-class | AIP 2023 | high |
+| Net electric output (HESTIA FPP) | 70 MWe | AIP 2023, Table I | high |
+| Net electric output (FOAK) | 103 MWe | AIP 2023, Table I | medium |
+| Fusion power (HESTIA) | 260 MW | AIP 2023, Table I | high |
+| Gross electricity | ~139 MW | AIP 2023, Table I | high |
 | Fusion gain Q | ~13 | AIP 2023 | high |
-| Availability target | >80% | AIP 2023 | high |
-| Maintenance cycle | ~3 months per year | AIP 2023 | high |
-| Continuous burn duration | ~1 year | AIP 2023 | high |
-| Magnetic field at coil center | 8 T | AIP 2023 | high |
-| Major radius | ~8 m (helical coils) | Tech overview | medium |
-| Heating method | ECRH, no current drive | AIP 2023 | high |
-| Power conversion | sCO2 Brayton (likely) | Indirect: website + Oroshhi-2 | medium |
-| sCO2 efficiency target | >50% at 800–1200 K | Ishiyama & Tanaka 2019 | medium — NIFS research target, not HESTIA-specific |
-| Capacity factor (derived) | ~80% | AIP 2023 | medium |
-| Fuel type | D-T, self-bred tritium | AIP 2023 | high |
-| Funding raised | ~USD 38M (Dec 2025) | BusinessWire | high |
-
-**Derived / Estimable Parameters** (not directly stated but calculable):
-
-| Parameter | Derivation | Notes |
-|-----------|-----------|-------|
-| Thermal power | If η=50%, P_thermal ≈ 100 MWth; if η=40%, P_thermal ≈ 125 MWth | Depends on sCO2 efficiency assumption |
-| Specific capital cost | $5B / 50 MWe = $100,000/kWe ($100/W) | Extremely high by power plant standards; driven by small scale |
-| ECRH recirculating power | At Q~13: P_fusion ≈ 13×P_ECRH; if P_net=50 MWe and η=50%, rough estimate P_ECRH ≈ 10–15 MW, recirculating fraction ~20–30% | Assumes simple Q definition; actual power balance needs full paper |
-| Back-of-envelope LCOE | At 8% FCR: ~$400M/yr capital + $50M/yr O&M over 350 GWh/yr → ~$130/MWh (13 c/kWh) at 50 MWe | Very high; improves sharply at 100 MWe scale |
+| Direct construction cost (HESTIA) | $5B (1990s basis; ~$10B+ inflation-adjusted) | AIP 2023, Table I + text | medium |
+| FOAK construction cost | ~$3B (1990s basis) | AIP 2023, Introduction | medium |
+| Capital cost per lifetime output | $1.22/kWh (HESTIA), $1.19/kWh (FOAK) | AIP 2023, Table I | medium |
+| Target availability | >80–85% | AIP 2023 | high |
+| Burn cycle | ~1 year continuous + ~3 month maintenance | AIP 2023 | high |
+| ECH wall-plug power | 40 MW (for 20 MW plasma heating, 50% η) | AIP 2023 | high |
+| ECH wall-plug efficiency target | 50% | AIP 2023 | medium |
+| Cryogenic recirculating power | ~2% gross output | AIP 2023 | medium |
+| Power conversion type | sCO2 Brayton cycle (explicitly confirmed Section F) | AIP 2023 | high |
+| Target thermal efficiency | >50% | AIP 2023 | medium |
+| Current sCO2 demo efficiency | ~40–47% | Kovari 2014; STEP Demo GTI | high |
+| Major radius | 7.8 m | AIP 2023 | high |
+| Stored magnet energy | 46.2–66.2 GJ | AIP 2023, Table I | high |
+| Building envelope | 60×160 m² floor, 100 m height | AIP 2023 | high |
+| Helios analog: net output | 390 MWe | Helios arXiv:2512.08027 | high |
+| Helios analog: thermal efficiency | 40% (steam Rankine) | Helios arXiv:2512.08027 | high |
+| Helios analog: capacity factor | 88% (84 days outage/2 years) | Helios arXiv:2512.08027 | high |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost by subsystem (magnet, blanket, BOP, building) | proprietary | blocking for detailed model | Only total cost published |
-| Thermal power output | derivable | important | Back-calculable once efficiency assumed |
-| Power conversion cycle efficiency (confirmed) | not-yet-sourced | important | sCO2 strongly implied; value unconfirmed |
-| ECRH total power input (MW) | not-yet-sourced | important | Determines recirculating power; may be in full AIP paper |
-| O&M cost estimate | proprietary / not-yet-sourced | important | No public estimate; need analogue from FFHR studies or tokamak O&M |
-| Blanket module lifetime / replacement schedule | not-yet-sourced | important | Affects O&M cost; neutron wall loading unknown |
-| REBCO tape cost at production volume | not-yet-sourced | important | Major capital cost driver |
-| 250 GHz gyrotron cost and efficiency | not-yet-sourced | important | Determines ECRH capital and recirculating power |
-| Li-6 enrichment and annual fuel cost | not-yet-sourced | nice-to-have | Fuel cost likely small vs. capital |
-| Neutron wall loading (MW/m²) | not-yet-sourced | important | Drives blanket lifetime and replacement cost |
+| Subsystem capital cost breakdown (magnets, blanket, BOP, ECH system) | not-yet-sourced | **blocking** | Only total direct cost is available; no CAS-level breakdown from any source for this specific concept |
+| Annual O&M cost | not-yet-sourced | **blocking** | No O&M estimate in any source; must be derived from analogue (e.g., 2–3% of capital from TEA D-T MFE source or ARIES CAS) |
+| Plant lifetime | not-yet-sourced | **blocking** | Not stated in AIP paper; implied >30 years from development strategy but never confirmed |
+| LM pump recirculating power | truly-unknown | **blocking** | Paper explicitly states "quite unknown"; uses mechanical pump placeholder in Table I |
+| First wall replacement schedule and cost | truly-unknown | important | Porous first wall structure novel; no lifetime estimate |
+| Confirmed thermal efficiency | not-yet-sourced | important | >50% is target; sCO2 at 800-1200K not yet demonstrated; current demos at ~40-47% |
+| WISE conductor unit cost ($/kA·m) | not-yet-sourced | important | Novel conductor; no published cost data; REBCO tape scaling may provide bound |
+| 250 GHz CW gyrotron cost (60 units) | truly-unknown | important | Technology does not yet exist; no cost analogue |
+| Tritium startup inventory cost | derivable | important | ~1 kg needed (per Table I context); market price applies |
+| Li-6 enrichment procurement and cost | derivable | important | 80% Li-6 enrichment needed; global supply constrained |
+| Decommissioning cost | not-yet-sourced | nice-to-have | Standard 10–15% of capital assumption applicable |
+| Staffing model | not-yet-sourced | nice-to-have | No staffing estimate published |
 
 ---
 
 ## Source Recommendations
 
-1. **Full AIP 2023 paper (Physics of Plasmas 30, 050601)** — paywalled, but likely accessible via institutional access or Sci-Hub equivalent. Expected content: plasma parameter table, power balance, subsystem sizing, TBR estimates, possibly cost breakdown detail. `not-yet-sourced` — **highest priority**.
-
-2. **NIFS FFHR system studies** — search NIFS publications or OSTI for "FFHR-c1" or "FFHR-d1" system code studies by Sagara, Takahashi, or Goto. These form the heritage basis for HESTIA and may contain cost modeling methodology applicable by analogy. `not-yet-sourced` — `unverified — confirm existence before searching`.
+1. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — read for CAS-level cost breakdown applicable to D-T MFE. Should resolve subsystem cost proportion assumptions (magnets, blanket, BOP, ECH as fractions of total direct cost). **Verified exists in repo; read before building cost model.**
 
-3. **FPA or IAEA conference proceedings** — Helical Fusion/NIFS team likely presented at Fusion Power Associates Annual Meeting (2024, 2025) or IAEA Fusion Energy Conference. Search FPA proceedings or IAEA INIS for "Helical Fusion" or "HESTIA." `not-yet-sourced` — `unverified — confirm existence before searching`.
+2. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — read for CAS 20-27 account definitions and cost scaling algorithms. Directly applicable to stellarator cost estimates. **Verified exists; the ARIES-CS compact stellarator study is in the same family as HESTIA.**
 
-4. **SOFT (Symposium on Fusion Technology) proceedings** — NIFS blanket team regularly presents liquid metal blanket progress at SOFT. Relevant for GALOP quantitative data, MHD analysis, TBR calculations. `not-yet-sourced` — `unverified — confirm existence before searching`.
+3. **Revisit of 2017 ARPA-E ALPHA costing** (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) — read for multi-concept cost breakdown methodology. May contain O&M cost fractions applicable across MFE concepts.
 
-5. **Springer book chapter** — Source listed in dossier: "Helical Fusion Reactor Concepts" chapter from a Springer volume. May contain reactor parameter tables and cost discussion. `not-yet-sourced` — obtain via DOI `10.1007/978-3-031-17711-8_9`.
+4. **FFHR full design papers** — search OSTI/J-STAGE for Sagara et al. "FFHR Design Group" papers (Nuclear Fusion, 2017; referenced in AIP 2023 as [1] — Nucl. Fusion 57, 086046). These NIFS design study papers are the precursor to HESTIA and likely contain more detailed subsystem cost analysis. `unverified — confirm existence before searching`.
 
-6. **HTS coil cost analogues** — For REBCO magnet cost estimation, use published HTS magnet cost studies from SPARC (Commonwealth Fusion), STEP (UKAEA), or ARPA-E GAMOW program reports. These provide $/kA-m or $/kg cost data applicable to WISE-type conductors. `derivable by analogy`.
+5. **HELICOSOPE systems code outputs** — if any Helical Fusion or NIFS conference papers cite HELICOSOPE results with parameter tables, these would provide validated plant economics. Search IAEA Fusion Energy Conference proceedings and Plasma and Fusion Research. `unverified — confirm existence before searching`.
 
-7. **sCO2 Brayton cycle cost data** — NREL, Sandia, or DOE sCO2 pilot program reports (e.g., the NET Power plant, Echogen) provide BOP cost estimates at relevant scales. `not-yet-sourced` — applicable as analogue for energy conversion cost.
+6. **Gyrotron cost analogues** — search for cost estimates of ITER 170 GHz gyrotrons (unit costs ~$2-5M per tube in ITER procurement) as a lower bound for the 250 GHz development program. `not-yet-sourced — analogue available in public ITER documentation`.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with current sources, supplemented by targeted retrieval.**
+Proceed to full analysis. The AIP 2023 paper provides sufficient technical detail for a well-grounded qualitative analysis across all five D1+ sections. For the quantitative LCOE model: use the $5B total direct cost (inflation-adjusted to $10B+) for HESTIA at 70 MWe as the primary capital cost input; supplement with CAS-level breakdowns from the ARIES cost account documentation and TEA D-T MFE source to estimate subsystem proportions; use analogue-based O&M (2–3% of capital); assume 50% sCO2 thermal efficiency per target (with 40–47% sensitivity range); use >80% availability. The cost model will have wide uncertainty bands (factor ~2) due to the 1990s cost basis, novel conductor costs, and unquantified LM pump power — but these uncertainties are characterizable and suitable for a first-pass analysis.
 
-The data state is sufficient to write a well-grounded qualitative write-up and a parameterized first-pass LCOE model. The $5B construction cost figure and >80% availability target provide anchors for top-down LCOE estimation. The Q~13 performance target and sCO2 efficiency range support a reasonable power balance derivation.
-
-The most important gap is the absence of any subsystem-level cost breakdown — the $5B is a single number with no decomposition. A bottom-up cost model is not feasible without this, but a top-down model with sensitivity analysis is tractable. The second-priority gap is confirmed power conversion efficiency; using a range of 40–55% for sCO2 covers the uncertainty reasonably.
-
-The Springer book chapter (DOI available) and the full AIP 2023 paper body should be attempted before finalizing the analysis, as they are the most likely sources to contain plasma parameter tables, power balance details, and possibly cost structure. All other gaps can be addressed through analogues, derivations, and explicitly stated assumptions.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 1
-important_count: 8
-counting_method: "section_5_missing_parameters"
+blocking_count: 4
+important_count: 9
+counting_method: "section_5_missing_parameters_plus_section_2_lm_pump_gap; deduplicated across all sections; blocking = parameters where no data exists and no standard analogue applies without stated assumptions; important = significant uncertainty but analogue-based estimation possible"
 section_coverage:
-  availability_of_data:       "Moderate"
+  availability_of_data:       "Good"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
   lcoe_parameter_extraction:  "Partial"
-```
+```
\ No newline at end of file
```

## Acceptance notes (fill during Phase 3)

- Deviation class (1-6 per plan.md): 
- Justified by fleet source? 
- Notes: 
