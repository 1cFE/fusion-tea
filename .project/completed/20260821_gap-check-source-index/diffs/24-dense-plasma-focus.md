# Diff: 24-dense-plasma-focus

**Generated:** 2026-05-22T10:54:57-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 6 | 7 | 1 |
| important_count  | 5 | 6 | - |
| overall_rating   | Insufficient Data | Significant Gaps | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
154:4. **ARPA-E ALPHA program documentation** — The ALPHA program (2015–2020) funded low-cost pulsed fusion concepts. If LPPFusion participated, ARPA-E published milestone reports and a revisit costing exercise (already in repo: `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`). Check whether DPF was one of the four costed concepts. `unverified — confirm existence before searching`. If DPF was included, this would be the single most valuable fleet-wide source for this concept.
156:5. **IFE simplified economics model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — The 14-parameter Monte Carlo LCOE model for pulsed fusion is methodologically applicable to DPF given its pulsed operation and yield-per-shot economics, even though DPF uses direct conversion rather than a thermal cycle. The rep rate, gain, and driver efficiency parameters map directly. Useful for parameterizing a DPF LCOE model in the absence of concept-specific cost data.
158:6. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — The CAS 20–27 framework is the right structure for any LCOE model regardless of concept. Should be used to structure whatever cost estimates can be made for DPF.
```

## Blocking-tier lines (baseline)

```
34:- No independent technical literature — `proprietary/not-yet-sourced` — **blocking** for credibility assessment; all data comes from the company's principals
59:- Ion beam decelerator efficiency: `truly-unknown` (no published data anywhere) — **blocking** for LCOE
60:- X-ray converter efficiency: `not-yet-sourced` (patent may contain data) — **blocking** for LCOE
61:- QMFE validity: `not-yet-sourced` (independent literature exists) — **blocking** for viability assessment
63:- Electrode erosion solution: `truly-unknown` — **blocking** for capacity factor
83:- Ion beam decelerator TRL: `truly-unknown` (no published experiments) — **blocking**
86:- p-B11 ignition physics (independent): `not-yet-sourced` (QMFE critiques in plasma physics literature) — **blocking** for viability
```

## Blocking-tier lines (new)

```
53:- QMF effect enabling p-B11 gain >1: theoretically predicted, never experimentally confirmed at required field strengths — `truly-unknown` at this point — **blocking** (the entire concept's viability hinges on this)
54:- Ion beam decelerator and x-ray photovoltaic converter: conceptual only, no prototype, no efficiency measurement — `truly-unknown` — **blocking** for quantitative cost modeling
55:- High-rep-rate operation: no demonstration at fusion-relevant conditions — `truly-unknown` — **blocking** for capacity factor and O&M modeling
77:- Ion beam decelerator: TRL 1–2, no prototype — `truly-unknown` (fusion-specific; accelerator analogy is imperfect) — **blocking**
78:- X-ray photovoltaic converter: TRL 1–2, never built — `truly-unknown` — **blocking**
79:- Electrode durability at 200 Hz: no data — `truly-unknown` — **blocking** (monthly replacement is target, not validated)
133:| CAS-level cost breakdown (20–27) | truly-unknown | blocking | No subsystem-level cost estimates; only total unit cost |
134:| Direct energy conversion capital cost | truly-unknown | blocking | Novel technology; no analogues; dominates BOP cost |
135:| Operating cost (electrode replacement $/yr) | derivable | blocking | Monthly Be electrodes; need Be unit cost + machining |
136:| Capacity factor / availability | truly-unknown | blocking | No rep-rate demonstration; electrode wear unquantified |
137:| Recirculating power fraction | derivable | blocking | Needed for net electric output; not stated |
142:| Fusion gain Q (at net energy conditions) | truly-unknown | blocking | p-B11 net energy not yet demonstrated; Q=1 target only |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/24-dense-plasma-focus.md	2026-05-22 09:21:13.871101209 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/24-dense-plasma-focus/gap_report.md	2026-05-22 10:54:57.685935388 -0700
@@ -1,197 +1,183 @@
-I have everything I need. Here is the assessment:
+I now have sufficient information to write the gap assessment. Let me compile the report.
 
 ---
 
 # Gap Assessment: Dense Plasma Focus (p-B11)
 
 ## Overall Readiness
-**Rating**: Insufficient Data
-
-**Summary**: The available source material is extremely thin — three brief extraction files totaling ~5 KB, all ultimately sourced from LPPFusion's own publications and website. The concept is at TRL 3–4 (physics experiments, far from net energy), and virtually all engineering subsystems (ion beam decelerator, x-ray converter, high-rep-rate driver) exist only at the conceptual/patent stage with no published prototype results, efficiency data, or engineering studies. A credible LCOE model cannot be built from these sources; only an illustrative bounding analysis using company-stated targets is possible. A qualitative narrative analysis is feasible but must be heavily caveated.
+**Rating**: Significant Gaps
+**Summary**: Public physics literature (Lerner 2023 JFE, Lerner 2024 Frontiers) provides good qualitative coverage of the DPF device, confinement mechanism, and experimental results, supporting a solid narrative write-up. However, quantitative LCOE analysis faces severe structural problems: all cost projections originate from company promotional materials, assume undemonstrated physics (QMF effect enabling p-B11 net energy), and rely on mass-production cost models for hardware that does not yet exist as a prototype. The two most capital-cost-relevant subsystems — the direct energy conversion systems (ion beam decelerator and x-ray photovoltaic converter) — have no prototypes, no measured efficiencies, and no cost analogues anywhere in the public literature.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Poor
+**Coverage**: Partial
 
 **Available**:
-- LPPFusion website technology pages (retrieved 2026-03-08): device description, power plant targets, development roadmap
-- Lerner et al. (2024) *Frontiers in Physics*: FF-2B device specs, fuel preparation details, plasma conditions, nτ targets
-- Lerner et al. (2023) *J. Fusion Energy* 42:7: summary of experimental achievements, nτT product, qualitative claims
-- Company executive summary (website): 5 MW target, <$1M construction cost claim, LCOE claim of <0.2 c/kWh
-- All available sources are either from LPPFusion itself (company website, Lerner as principal author) or secondary summaries
+- Two recent peer-reviewed papers by Lerner et al.: the 2023 JFE comprehensive review and 2024 Frontiers preparations paper. Both are open access and contain substantial technical detail on plasma physics, experimental results, and the path to net energy.
+- Company website (lppfusion.com) provides technology descriptions, investor materials, and high-level cost claims.
+- Broad DPF literature base from 60 years of international DPF research (referenced in Lerner 2023), though not directly ingested.
+- Patent US #7,482,607 covers the key design innovations (small anode radius, angular momentum control, direct conversion concept) but the full text was not captured.
 
 **Missing**:
-- Independent third-party technical review of DPF physics claims
-- Any published plant study or system code analysis
-- Peer-reviewed critique or validation of the quantum magnetic field effect (QMFE) mechanism
-- Independent assessment of energy conversion subsystem viability
-- Financial disclosures or detailed cost models
+- Independent peer-reviewed cost analysis or plant study. All cost figures come from the company itself.
+- Full text of Lerner (2011) J. Fusion Energy 30:367 — the earliest quantitative power plant conceptual design paper, referenced in the dossier as the likely source of engineering specs (input energy per shot, capacitor bank sizing for the commercial device).
+- Third-party assessment of the QMF effect claim and whether bremsstrahlung suppression is sufficient for p-B11 gain >1.
+- DPF experiment results at fusion-relevant conditions from other international groups for benchmarking.
 
 **Gaps**:
-- No independent technical literature — `proprietary/not-yet-sourced` — **blocking** for credibility assessment; all data comes from the company's principals
-- No published plant study (Lerner (2011) *J. Fusion Energy* 30:367 referenced in the dossier as possibly containing a conceptual power plant design, but not extracted) — `not-yet-sourced` — **important**
-- U.S. Patent #7,482,607 (x-ray conversion technology) not extracted — `not-yet-sourced` — **important**
+- No independent techno-economic analysis of DPF/Focus Fusion — `truly-unknown` (no external group has published one) — **important**
+- Lerner (2011) commercial design paper not captured — `not-yet-sourced` — **important** (likely contains device engineering specs for the commercial-scale unit)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-**Coverage**: Partial (qualitatively describable, quantitatively unresolvable)
+**Coverage**: Good (qualitative); Poor (quantitative)
 
 **Available**:
-- QMFE mechanism described qualitatively (simulations show fusion power can exceed bremsstrahlung by ~2×)
-- Two-channel energy conversion pathway described: ion beam decelerator + x-ray photoelectric (Frontiers 2024, website)
-- Pulsed operation mode, ~10 ns pulse, plasmoid physics
-- Known challenge flagged in dossier: electrode erosion at 200 Hz rep rate (no solutions cited)
-- nτ gap quantified: current best 2.4 × 10¹² s/cm³ vs. target 2 × 10¹³ s/cm³ (10× improvement needed); fusion yield gap: 0.26 J achieved vs. 30 kJ needed (~115,000×)
+- The Lerner 2023 JFE paper provides an unusually candid account of current experimental failures: yield plateau at >1 MA peak current (unresolved for 20+ years), filament disruption by high-frequency oscillations, switch reliability problems. The factor-of-120,000 gap between current yield (0.25 J) and net-energy target (30 kJ) is explicitly stated.
+- The QMF effect mechanism (bremsstrahlung suppression via ultra-strong magnetic fields) is described in detail; its validity is the central physics bet. Only 0-D simulations exist; no 2-D validated model (Lerner 2023 notes a 2-D model is in progress).
+- The energy capture architecture is described qualitatively: ion beam enters a coil-based "decelerator" (analogous to linear accelerator in reverse), x-rays hit a multilayer photoelectric converter.
+- The cooling challenge at the anode tip (up to 10 kW/cm²) is explicitly flagged as a primary engineering challenge.
+- Repetition rate target (200 Hz) is derived from a thermal-cooling-limited argument, not from operational demonstration.
 
 **Missing**:
-- Any prototype test data for ion beam decelerator (efficiency, engineering design)
-- Any prototype test data for x-ray photoelectric converter (efficiency, material requirements)
-- Recirculating power fraction at 200 Hz (capacitor bank recharge, cooling loads)
-- Electrode wear rate and replacement interval at target rep rate
-- Analysis of plasmoid-to-beam coupling efficiency (what fraction of plasmoid energy enters the decelerator)
-- Whether QMFE has been independently verified or is disputed in the literature
+- Validated efficiency for either direct conversion pathway. The claimed 85% (ion beam) and >80% (x-ray) are derived from principles, not measurements.
+- Any demonstration of repetitive pulsed operation at kA-scale plasma conditions (all experiments are single-shot).
+- Validated 2-D or MHD simulation of plasmoid dynamics with p-B11 fuel.
+- Quantified shot-to-shot variability and its effect on net energy economics.
 
 **Gaps**:
-- Ion beam decelerator efficiency: `truly-unknown` (no published data anywhere) — **blocking** for LCOE
-- X-ray converter efficiency: `not-yet-sourced` (patent may contain data) — **blocking** for LCOE
-- QMFE validity: `not-yet-sourced` (independent literature exists) — **blocking** for viability assessment
-- Recirculating power / wall-plug Q: `derivable` only with assumed efficiencies — **important**
-- Electrode erosion solution: `truly-unknown` — **blocking** for capacity factor
+- QMF effect enabling p-B11 gain >1: theoretically predicted, never experimentally confirmed at required field strengths — `truly-unknown` at this point — **blocking** (the entire concept's viability hinges on this)
+- Ion beam decelerator and x-ray photovoltaic converter: conceptual only, no prototype, no efficiency measurement — `truly-unknown` — **blocking** for quantitative cost modeling
+- High-rep-rate operation: no demonstration at fusion-relevant conditions — `truly-unknown` — **blocking** for capacity factor and O&M modeling
+- Shot-to-shot variability impact on plant economics: unquantified — `derivable` (from known shot variance if yield data were available) — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial (qualitative TRL estimates possible, no quantitative data)
+**Coverage**: Partial
 
 **Available**:
-- DPF device (FF-2B): operational, achieving 2.7 MA, >200 keV ion energies, record nτT — TRL ~4
-- Decaborane fuel preparation: described in Frontiers 2024, planned tests — TRL ~4 for fuel handling
-- Beryllium electrode fabrication: demonstrated in FF-2B — TRL ~5 for fabrication, TRL ~3 for wear management
+- **DPF plasma device (physics)**: TRL 3–4. Ion energies >200 keV demonstrated (world record); nτT = 3.4×10²⁰ keV·s/m³ achieved with D fuel. Beryllium electrodes demonstrated with zeff ~1.004. Yield plateau at >1 MA remains unresolved; new switches installed (2023).
+- **Fuel handling (decaborane)**: TRL 3. Isotopically pure decaborane procured; safe handling equipment installed; first p-B11 shots described as imminent in 2024 Frontiers paper.
+- **Diamond photoconductive switches**: Two external sources (compoundsemiconductor.net, LLNL IPO) confirm diamond PCSS development at TRL 3, with record current densities demonstrated. These would be needed for fast switching in the direct conversion circuit.
+- **Capacitor bank / pulsed power driver**: TRL 6–7 (well-established commercial technology; FF-2B uses a 12-capacitor bank at up to 45 kV). Not a technical risk.
 
 **Missing**:
-- TRL of ion beam decelerator: no prototype, no test data — TRL ~1–2
-- TRL of x-ray photoelectric converter: patent exists but no experimental efficiency data — TRL ~1–2
-- TRL of high-rep-rate capacitor driver (200 Hz at MW scale): DPF at 16 Hz demonstrated elsewhere (NX2, Singapore), but at much lower energy and different application — TRL ~2–3
-- TRL of p-B11 ignition: not yet achieved in any device anywhere — TRL ~2–3 (relevant physics partially demonstrated, ignition not demonstrated)
-- TRL of thermal management at 200 Hz: undefined
+- **Ion beam decelerator**: No prototype at any scale. The concept is described by analogy with particle accelerator beam dumps; efficiencies >85% are claimed from that literature. No fusion-beam-scale hardware exists.
+- **X-ray multilayer photoelectric converter**: Never built. Design is described in the patent (US #7,482,607) but no prototype or test data exists.
+- **Electrode durability at 200 Hz / fusion yield conditions**: Electrode replacement is targeted at "once per month" but no data on erosion rates at fusion-relevant conditions exists. Current experiments run single-shot.
+- **High-rep-rate pulsed power system**: The electrical circuit (180 kHz natural frequency) has never been run repetitively near fusion conditions.
+- **Anode tip cooling system**: Compressed helium cooling conceptualized; not designed or tested.
 
 **Gaps**:
-- Ion beam decelerator TRL: `truly-unknown` (no published experiments) — **blocking**
-- X-ray converter TRL: `not-yet-sourced` (patent, possibly internal LPPFusion work) — **important**
-- 200 Hz driver TRL at relevant scale: `not-yet-sourced` (NX2 reports, pulsed power literature) — **important**
-- p-B11 ignition physics (independent): `not-yet-sourced` (QMFE critiques in plasma physics literature) — **blocking** for viability
+- Ion beam decelerator: TRL 1–2, no prototype — `truly-unknown` (fusion-specific; accelerator analogy is imperfect) — **blocking**
+- X-ray photovoltaic converter: TRL 1–2, never built — `truly-unknown` — **blocking**
+- Electrode durability at 200 Hz: no data — `truly-unknown` — **blocking** (monthly replacement is target, not validated)
+- Anode tip cooling at 10 kW/cm²: conceptual only — `derivable` from helium cooling literature — **important**
+- Diamond switch integration with DPF pulse power: TRL 3 in general, not validated for DPF application — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-**Coverage**: Partial (identifiable from physics; no sourced supply chain analysis)
+**Coverage**: Partial
 
 **Available**:
-- Fuel: proton (hydrogen) + boron-11. Isotopically pure B-10 decaborane used in FF-2B (B-10 enrichment specified at 0.07% B-10 content — wait, this means nearly pure B-11, since natural boron is ~20% B-10). Standard decaborane commercially available.
-- Electrode material: beryllium (FF-2B). Be identified as critical for impurity reduction.
-- No tritium, no helium-3, no superconducting magnets, no lithium-6 — key simplifying factors
+- **Beryllium**: Lerner 2023 JFE explicitly flags the supply chain issue. Current global production ~400 t/year; commercial DPF fleet would require ~10x scale-up. The paper notes that "somewhat less-concentrated ores will have to be exploited" but does not quantify cost impact. Beryllium toxicity requires specialized manufacturing controls.
+- **Boron-11 (isotopically pure)**: Decaborane with 0.07% B-10 has been procured (350× enrichment over natural boron). Cost and supply scalability for commercial deployment are not discussed.
+- **p-B11 fuel abundance**: Both boron and hydrogen are abundant; LPPFusion claims a fully commercial global fleet would need only ~10% increase in total boron production. This is credible given the aneutronic, non-tritium fuel cycle.
+- **No tritium**: Eliminates the most severe supply chain constraint of D-T fusion.
+- **No neutron damage**: Eliminates the first-wall material replacement cycle and radioactive waste stream that drive operating costs in D-T concepts.
 
 **Missing**:
-- Beryllium supply chain assessment (beryllium is a strategic/critical material; U.S. primary producer is Materion; limited global supply; toxic manufacturing)
-- Electrode replacement rate at 200 Hz and its impact on Be consumption
-- Cost and availability of isotopically pure decaborane at commercial scale
-- Whether electrodes require other exotic materials (coatings, composites)
-- Manufacturing scalability for mass-produced 5 MW units (claimed path to mass production)
+- Cost and scalability data for isotopically pure decaborane at commercial volumes.
+- Beryllium manufacturing cost (machined electrodes, monthly replacement cycle).
+- Diamond availability for photoconductive switches (natural diamond is rare; synthetic CVD diamond supply is limited but growing).
+- Any supply chain analysis from an independent source.
 
 **Gaps**:
-- Be electrode consumption rate and supply chain: `not-yet-sourced` — **important** (Be is a known supply chain concern for fusion)
-- Decaborane enrichment cost at scale: `not-yet-sourced` — **important** for fuel cost LCOE inputs
-- Mass production pathway for DPF units: `proprietary` — **nice-to-have** (company claims but no engineering basis)
+- Isotopically pure decaborane supply at commercial scale: no published data — `not-yet-sourced` (industrial chemistry literature may have analogs) — **important**
+- Monthly beryllium electrode replacement cost at scale: no data — `derivable` (from Be pricing and machining cost analogues) — **important**
+- Diamond supply for PCSS switches: no published data for this application — `not-yet-sourced` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Poor — company targets only, no engineering basis
+**Coverage**: Poor
+
+All cost figures below originate from LPPFusion company materials (investor documents, peer-reviewed papers authored by company staff). No independent cost analysis exists.
 
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Net electric output per unit | 5 MW | LPPFusion website | l — design target |
-| Repetition rate target | ~200 Hz | LPPFusion website | l — undemonstrated |
-| Net energy per pulse | ~25 kJ | LPPFusion website | l — design target |
-| Device construction cost | <$1M per unit | Lerner 2024 / website | l — single data point, no breakdown |
-| LCOE claim | <0.2 c/kWh | LPPFusion website | l — no derivation provided |
-| Device mass | ~3 tons | LPPFusion website | m — plausible for described geometry |
-| Device volume | ~30 m³ | LPPFusion website | m — plausible |
-| Cap→x-ray conversion efficiency | >10% | Lerner 2024 Frontiers | l — stated without derivation |
-| Current fusion yield | 0.26 J/shot | LPPFusion website | h — experimental result |
-| Target fusion yield | 30 kJ/shot | LPPFusion website | l — design target |
-| nτ current best | 2.4 × 10¹² s/cm³ | Lerner 2024 Frontiers | h — experimental |
-| nτ target for ignition | >2 × 10¹³ s/cm³ | Lerner 2024 Frontiers | m — derived from physics |
-| Phase 2 development cost | ~$100M | LPPFusion website | l — company estimate |
+| Plant electric output (per unit) | 5 MW | Lerner 2023 JFE (p. 14) | medium — derived from 200 Hz × 25 kJ/pulse |
+| Capital cost (mass production) | ~$500K/unit ($0.10/W) | Lerner 2023 JFE (p. 14) | low — assumes mass production; no BOM |
+| LCOE (claimed) | ~0.3 ¢/kWh | Lerner 2023 JFE (p. 14) | low — unvalidated, company estimate |
+| Repetition rate target | 200 Hz | Lerner 2023 JFE | low — undemonstrated; thermal limit argument |
+| Device mass | ~3 tons | Lerner 2023 JFE | medium |
+| Device volume | ~30 m³ | Lerner 2023 JFE | medium |
+| Annual fuel consumption (per unit) | 5 kg p-B11 | Lerner 2023 JFE | medium — physics consistent |
+| Direct conversion claimed efficiency (ion beam) | ≤85% | Lerner 2023 JFE | low — from accelerator analogy, not DPF test |
+| Direct conversion claimed efficiency (x-ray) | >80% | Lerner 2023 JFE | low — theoretical, never prototyped |
+| Phase 2 engineering budget | ~$100M | Lerner 2023 JFE / net energy plan | medium — company estimate |
+| Electrode replacement target | ~monthly | Lerner 2023 JFE | low — target, no erosion data |
+| Input energy per shot | ~115 kJ stored (FF-1 bank) | Lerner 2023 JFE (p. 9) | high (for current experimental device) |
+| Net energy per pulse (commercial target) | ~25 kJ | Lerner 2023 JFE | low — requires unproven 30 kJ gross yield |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Ion beam decelerator efficiency | truly-unknown | Blocking | No published prototype; core to direct conversion LCOE |
-| X-ray converter efficiency | not-yet-sourced | Blocking | Patent #7,482,607 may have design claims |
-| Overall wall-plug efficiency (electrical out / electrical in) | derivable | Blocking | Requires conversion efficiencies + cap bank round-trip |
-| Capacitor bank round-trip efficiency | not-yet-sourced | Blocking | Pulsed power literature; determines recirculating power |
-| Capacity factor / availability | truly-unknown | Blocking | Depends on electrode life, undemonstrated rep rate |
-| Electrode replacement interval and cost | truly-unknown | Blocking | Determines major OPEX driver |
-| O&M cost | truly-unknown | Important | No analogues published for this class of device |
-| Fuel cost (decaborane at scale) | not-yet-sourced | Important | Likely low but unquantified |
-| Balance of plant cost | derivable | Important | Can borrow from small-scale industrial power; but direct conversion BOP has no analogues |
-| FOAK vs NOAK capital cost | truly-unknown | Important | Company claims mass production pathway, no basis |
-| R&D amortization basis | truly-unknown | Nice-to-have | Company-financed; unclear what is included in <$1M claim |
-| Scaling law (Q vs device size/current) | not-yet-sourced | Important | DPF scaling literature exists; Lerner 2011 may contain this |
-
-**Internal consistency check on the company's LCOE claim**:
-The <0.2 c/kWh LCOE claim fails a simple sanity check. At $1M capex for a 5 MW unit, 90% capacity factor, and a generous 30-year life with no discount rate:
-- Annual energy = 5 MW × 8,760 hr × 0.9 = 39,420 MWh/yr
-- Capex annualized (undiscounted) = $1M / 30 = $33,333/yr
-- Capex LCOE component alone = $33,333 / 39,420 MWh = $0.85/MWh = 0.085 c/kWh
-
-So the capex-only LCOE is ~0.085 c/kWh undiscounted — marginally consistent with their claim only if operating costs are near-zero, electrode replacement is negligible, and no R&D amortization is included. This is implausible for any real device. The claim appears to exclude all development costs and assumes near-zero OPEX. This should be flagged explicitly in any analysis.
+| CAS-level cost breakdown (20–27) | truly-unknown | blocking | No subsystem-level cost estimates; only total unit cost |
+| Direct energy conversion capital cost | truly-unknown | blocking | Novel technology; no analogues; dominates BOP cost |
+| Operating cost (electrode replacement $/yr) | derivable | blocking | Monthly Be electrodes; need Be unit cost + machining |
+| Capacity factor / availability | truly-unknown | blocking | No rep-rate demonstration; electrode wear unquantified |
+| Recirculating power fraction | derivable | blocking | Needed for net electric output; not stated |
+| Balance of plant cost | derivable | important | Could use scaled-down BOP analogues from small DG sets |
+| Cooling system cost (helium at 10 kW/cm²) | not-yet-sourced | important | He cooling engineering literature may have analogues |
+| D&D cost | derivable | nice-to-have | Small, low-activation device; likely minor |
+| Indirect costs (contingency, owner's cost) | derivable | important | ARIES CAS accounts apply; no concept-specific data |
+| Fusion gain Q (at net energy conditions) | truly-unknown | blocking | p-B11 net energy not yet demonstrated; Q=1 target only |
 
 ---
 
 ## Source Recommendations
 
-1. **Lerner, E.J. (2011) "Theory and Experimental Program for p-B11 Fusion with the Dense Plasma Focus"** *J. Fusion Energy* 30:367 — `not-yet-sourced, unverified — confirm existence before searching`. Cited in dossier as potentially containing conceptual power plant design. May contain early LCOE estimates and scaling assumptions. Search: Springer link `doi:10.1007/s10894-010-9354-5` or similar.
+1. **Lerner (2011) J. Fusion Energy 30:367** — Contains the quantitative commercial device conceptual design (full capacitor bank specs, power plant geometry, scaling arguments). High probability of containing the most detailed engineering data available in the public literature. `not-yet-sourced` — search Springer via DOI 10.1007/s10894-010-9342-2.
 
-2. **U.S. Patent #7,482,607** (LPPFusion x-ray conversion technology) — `not-yet-sourced`. May contain efficiency claims for photoelectric x-ray converter. Search: USPTO or Google Patents by number.
+2. **US Patent #7,482,607** (LPPFusion, "Method and apparatus for producing x-rays, ion beams and nuclear fusion energy") — Contains the original direct energy conversion architecture designs. `not-yet-sourced` — free from USPTO.
 
-3. **Independent QMFE literature** — `not-yet-sourced`. Search for peer-reviewed responses to or citations of Lerner's QMFE papers in plasma physics / nuclear fusion journals. Look for Rider (1995), Nevins critiques of advanced fuels, and any direct responses to Lerner's bremsstrahlung suppression claims. This is essential for viability framing.
+3. **Abolhasani et al. (2013) J. Fusion Energy 32:189** — Independent simulation of QMF effect in DPF with p-B11, finding gain ~6×. The only independent cross-check of the QMF physics claim in the available sources. `not-yet-sourced`.
 
-4. **NX2 device technical reports (Nanyang Technological University, Singapore)** — `not-yet-sourced, unverified`. Dossier cites 16 Hz DPF rep rate; NX2 is the referenced device. Engineering details on rep-rate limits, electrode wear, and capacitor bank design would directly inform capacity factor and OPEX gaps.
+4. **ARPA-E ALPHA program documentation** — The ALPHA program (2015–2020) funded low-cost pulsed fusion concepts. If LPPFusion participated, ARPA-E published milestone reports and a revisit costing exercise (already in repo: `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`). Check whether DPF was one of the four costed concepts. `unverified — confirm existence before searching`. If DPF was included, this would be the single most valuable fleet-wide source for this concept.
 
-5. **Pulsed power / capacitor bank efficiency literature** — `not-yet-sourced`. General pulsed power engineering literature covers capacitor bank round-trip efficiency at MA-class currents. Search IEEE Transactions on Plasma Science, Pulsed Power Conference proceedings.
+5. **IFE simplified economics model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — The 14-parameter Monte Carlo LCOE model for pulsed fusion is methodologically applicable to DPF given its pulsed operation and yield-per-shot economics, even though DPF uses direct conversion rather than a thermal cycle. The rep rate, gain, and driver efficiency parameters map directly. Useful for parameterizing a DPF LCOE model in the absence of concept-specific cost data.
 
-6. **Advanced fuel fusion viability reviews** — `not-yet-sourced`. Review papers on p-B11 viability (e.g., Putvinski et al. 2019 *Nuclear Fusion* "Fusion reactivity of the pB11 plasma revisited") provide independent basis for Q achievability. Essential for system function framing.
+6. **ARIES cost account documentation** (`knowledge/sources/aries_cost_account_documentation/`) — The CAS 20–27 framework is the right structure for any LCOE model regardless of concept. Should be used to structure whatever cost estimates can be made for DPF.
+
+7. **International DPF database / Lee model** — S. Lee's DPF scaling code (Lee model) is widely published and used by the international DPF community. It produces quantitative yield predictions vs. capacitor bank parameters. `not-yet-sourced` — search OSTI or Google Scholar for "Lee model dense plasma focus". Could constrain yield-per-shot and rep-rate parameters.
 
 ---
 
 ## Summary
 
-**Proceed to full analysis with significant caveats.** The available data is sufficient for a qualitative narrative analysis, but not for a credible bottom-up LCOE model. The recommended approach is:
-
-1. **Qualitative narrative**: Write-up is feasible. Flag that: (a) all sources are company-originated; (b) the key enabling physics (QMFE, p-B11 ignition) is undemonstrated and independently disputed; (c) the concept is at TRL 3–4 globally; (d) the LCOE claim fails basic sanity-check arithmetic if any realistic OPEX is included.
+Proceed to full analysis, but with significant caveats clearly stated. The qualitative sections (1–4) can be written substantively using the available physics literature. The quantitative LCOE model will be highly speculative: the device is single-shot today, net energy has not been demonstrated (either with D or p-B11), the two novel direct conversion systems exist only on paper, and all cost projections come from company investor materials assuming mass production of a working prototype that does not yet exist. The model should be parameterized to make all assumptions explicit and the back-solve analysis ($0.01/kWh target) is actually where this concept shines analytically — the concept's cost structure is plausibly ultra-low if its physics and engineering claims hold, making the binding constraints (Q, rep rate, electrode life, conversion efficiency) the interesting story.
 
-2. **Quantitative model**: Build an illustrative/bounding model only, using company-stated targets as the optimistic scenario. The model should make explicit that: device cost, conversion efficiency, electrode lifetime, and capacity factor are all assumed from unvalidated company claims. Back-solve to $0.01/kWh can be performed but the base case should be flagged as almost certainly optimistic by ≥10×.
-
-3. **Before a serious second-pass analysis**: acquire Lerner (2011) for any conceptual plant design; extract QMFE critiques from independent literature; and confirm whether the x-ray patent contains efficiency data. These three sources would substantially improve the analysis quality.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Insufficient Data"
-blocking_count: 6
-important_count: 5
-counting_method: "section_5_missing_parameters"
+overall_rating: "Significant Gaps"
+blocking_count: 7
+important_count: 6
+counting_method: "deduplicated across all sections: blocking = (QMF physics undemonstrated, ion beam decelerator no prototype, x-ray photovoltaic no prototype, rep-rate operation undemonstrated, electrode durability unknown, no CAS-level cost breakdown, no capacity factor data); important = (no independent TEA, Lerner 2011 not captured, shot-to-shot variability unquantified, anode cooling conceptual, Be electrode replacement cost unquantified, isotopic decaborane supply unknown)"
 section_coverage:
-  availability_of_data:       "Poor"
-  system_function:            "Partial (qualitatively describable, quantitatively unresolvable)"
-  subsystem_maturity:         "Partial (qualitative TRL estimates possible, no quantitative data)"
-  materials_supply_chain:     "Partial (identifiable from physics; no sourced supply chain analysis)"
-  lcoe_parameter_extraction:  "Poor — company targets only, no engineering basis"
-```
+  availability_of_data:       "Partial"
+  system_function:            "Partial"
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
