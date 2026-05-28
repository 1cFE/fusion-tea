# Phase 3 diff: 03-laser-icf-liquid-jet-target

**Generated:** 2026-05-22T13:13:51-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 8 | 7 | -1 |
| important_count  | 5 | 7 | - |
| overall_rating   | Insufficient Data | Insufficient Data | - |

## Fleet-source dispositions in new report

```
```

## Forbidden-phrase check (should be empty)

```
1:I now have sufficient information from all relevant sources to write the gap assessment report.
```

## First line of new report (should start with `# Gap Assessment`)

```
I now have sufficient information from all relevant sources to write the gap assessment report.
```

## Blocking-tier lines (new)

```
27:- No experimental validation from Cortex — `truly-unknown` — **blocking**
28:- Anomalous energy claim (3333 MeV per D-D event stated in paper vs. known 3–4 MeV; likely calculation error) — `truly-unknown` — **blocking**
29:- No published reactor design or plant study of any kind — `proprietary` — **blocking**
52:- Energy capture architecture completely unspecified — `proprietary` / `truly-unknown` — **blocking**
53:- Plasmonic ionization damping effect on fusion rate unquantified; potentially undermines the entire mechanism — `truly-unknown` — **blocking**
54:- 3-orders-of-magnitude gap between demonstrated kHz neutron yield (10⁵ n/s Cambridge) and claimed reactor neutron flux (10¹⁹ n/s Cortex) — `truly-unknown` — **blocking**
78:- Plasmonic D-D fusion mechanism entirely undemonstrated — `truly-unknown` — **blocking**
79:- Energy extraction subsystem: no concept disclosed — `truly-unknown` / `proprietary` — **blocking**
99:- Gold mass balance and recycling strategy for nanoshells: unaddressed — `truly-unknown` — **blocking** (cost viability depends entirely on this)
130:| Net fusion energy output (validated) | truly-unknown | blocking | Q~100 is a theoretical claim with anomalous intermediate result (3333 MeV/event); no experimental basis |
131:| Driver cost at MHz rate, mJ-class fs laser | not-yet-sourced | blocking | Industrial fs laser pricing exists but $/J at MHz rep rate for reactor scale not calculated |
132:| Capital cost of chamber/reactor vessel | truly-unknown | blocking | No chamber design disclosed; cannot estimate |
133:| Nanoshell target cost at reactor scale | not-yet-sourced | blocking | Gold nanoshell production cost at scale not established anywhere; plasmonics fabrication literature would bound this |
134:| O&M cost structure | truly-unknown | blocking | No plant design; no component replacement data |
135:| Capacity factor / availability | truly-unknown | blocking | No engineering basis; no analogous system |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/03-laser-icf-liquid-jet-target.md	2026-05-22 12:59:21.057230366 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/03-laser-icf-liquid-jet-target/gap_report.md	2026-05-22 13:13:51.496531754 -0700
@@ -1,15 +1,10 @@
-I now have sufficient information to write the gap assessment. Let me compose it.
-
----
+I now have sufficient information from all relevant sources to write the gap assessment report.
 
 # Gap Assessment: Laser ICF - Liquid Jet Target (D-D)
 
 ## Overall Readiness
 **Rating**: Insufficient Data
-
-**Summary**: Cortex Fusion Systems operates with extreme opacity — the only physics source is a single theoretical preprint (arXiv:2503.15531) whose Q~100 claim rests on a back-of-envelope calculation that ignores multiple known loss channels. There are zero experimental results from Cortex, no energy capture architecture, no plant design, and no cost data of any kind. The independent Cambridge kHz liquid-sheet D-D fusion paper confirms the enabling physics at tiny scale (~10^5 n/s) but falls nine orders of magnitude short of the claimed reactor scenario. A qualitative write-up can be structured around this extreme pre-conceptual state; a quantitative LCOE model requires inventing nearly every input from scratch.
-
----
+**Summary**: Cortex Fusion Systems is at a pre-experimental stage with a single theoretical preprint (arXiv:2503.15531, 2025) as its primary technical basis. The physics mechanism — plasmonic field enhancement in D₂O-filled gold nanoshells — is unvalidated by any experiment, and the performance claims (Q~100, 10¹⁹ n/s) contain an anomalous result (3333 MeV per D-D event vs. the known 3–4 MeV) that suggests calculation error. No plant design, energy capture architecture, chamber concept, or cost data has been disclosed. The data available is insufficient to produce a D1+ analysis beyond a brief technology assessment noting extraordinary unvalidated claims.
 
 ## Section Coverage
 
@@ -17,21 +12,22 @@
 **Coverage**: Poor
 
 **Available**:
-- `iter-01/sources/arxiv-2503-nanoshell-paper.md` — The primary physics paper. Provides: plasmonic field enhancement model (Mie theory), deuteron momentum estimate (~10 MeV → ~25 keV equivalent temperature), per-nanoshell fusion rate (~10^7 s^-1, ~1 µW), and a back-of-envelope reactor projection (1 MHz rep rate × 10^6 nanoshells/pulse → ~1 MW fusion, Q~100 at 3 kW laser input). Explicitly acknowledges open questions: ionization damping of plasmon, escaping deuteron fraction, thermalization kinetics. No engineering details, no cost data.
-- `iter-01/sources/arxiv-2308-levitt-quantum-control.md` — Older Levitt paper describing a completely different mechanism (quantum tunneling control of the ¹⁶O(2p,γ)¹⁸Ne reaction in water). Provides laser architecture details (Ti:sapphire 1 kHz, 15 mJ, bichromatic VUV+DUV control). Mentions scintillator/semiconductor energy extraction with <6% round-trip efficiency. This mechanism is not what the nanoshell paper describes — it is unclear which (if either) reflects Cortex's actual current direction.
-- `iter-01/sources/cortex-fusion-website.md` — Patent list only. 11 patent applications covering nanoshell approaches, quantum tunneling control, chiral catalysis, OAM beams, and a D2O-moderated fusion-fission hybrid. No technical or economic content.
-- `iter-01/sources/kHz-liquid-sheet-fusion-paper.md` — Independent Cambridge/AFRL paper demonstrating 1 kHz D-D fusion on a ~500 nm D2O liquid sheet. Confirms the enabling physics: ~10^5 n/s with 8 mJ, 40 fs, 780 nm laser at 5×10^18 W/cm². No connection to Cortex. Outcome is a neutron source, not an energy source (Q ≪ 1).
+- One theoretical preprint by company co-founders (arXiv:2503.15531) proposing the plasmonic D-D fusion mechanism; provides quantum mechanical estimates of deuteron momentum (~10 MeV) and projected fusion rate (~10⁷ s⁻¹ per nanoshell)
+- One earlier Cortex preprint (arXiv:2308.07417) on quantum control of nuclear fusion via laser-driven tunneling; covers a different reaction (¹⁶O(2p,γ)¹⁸Ne) but demonstrates the company's broader approach
+- Cortex Fusion Systems website: patent list only (11 applications covering nanoshell, quantum Zeno/anti-Zeno, chiral catalysis, and hybrid fusion-fission approaches); no technical specifications or cost data
+- Independent validation source (Cambridge HPLSE 2024, `iter-01/sources/kHz-liquid-sheet-fusion-paper.md`): demonstrates kHz-rate D-D fusion from sub-μm D₂O liquid sheets at 10⁵ neutrons/second using 8 mJ, 40 fs laser at ~5×10¹⁸ W/cm²; confirms technical feasibility of liquid D₂O jet targets at kHz rate but at yield 14 orders of magnitude below Cortex's reactor claim
 
 **Missing**:
-- Company-disclosed plant design or engineering roadmap
-- Any experimental validation of the nanoshell plasmonic enhancement mechanism at the claimed field strengths
-- Energy capture architecture (not specified in any source)
-- Economic or cost data of any kind
+- Any experimental results from Cortex itself
+- Engineering design for any subsystem (chamber, energy capture, target delivery system)
+- Company-disclosed performance data
+- Any independent review of the theoretical claims
 
 **Gaps**:
-- No plant-level or system-level design documents exist — `proprietary` (or simply not developed yet) — **blocking**
-- Only one company-affiliated physics paper, which is a preprint with unverified extraordinary claims — `truly-unknown` whether the mechanism produces net energy — **blocking**
-- Company's transparency is essentially zero — the website contains only patent numbers — `proprietary` — **blocking**
+- No experimental validation from Cortex — `truly-unknown` — **blocking**
+- Anomalous energy claim (3333 MeV per D-D event stated in paper vs. known 3–4 MeV; likely calculation error) — `truly-unknown` — **blocking**
+- No published reactor design or plant study of any kind — `proprietary` — **blocking**
+- Company funding ($2.6M) indicates pre-experimental stage with no near-term likelihood of published experimental results — `truly-unknown` — **important**
 
 ---
 
@@ -39,47 +35,50 @@
 **Coverage**: Poor
 
 **Available**:
-- The nanoshell paper provides enough to identify the fundamental system function challenge: the Q~100 estimate uses P_laser ≈ 3 kW as a given (equation 16), but does not explain how 10^6 nanoshells are ignited per pulse at 1 MHz, what laser energy per pulse this requires, or what efficiency assumptions are built into the 30% conversion factor. The actual laser energy budget is not closed.
-- The Cambridge paper confirms that liquid D2O jet targets are mechanically feasible at kHz rates with ~1 mL/min flow, ~$2/minute D2O consumption, and ~1 Torr vacuum. This is directly applicable to the Cortex liquid jet concept.
-- The Levitt 2023 quantum control paper (a different mechanism) explicitly states that ~10^12 fusion events per pulse are needed for net power production with 1 mJ pulses at 1–3% laser wall-plug efficiency — suggesting the energy balance problem is well-recognized even internally.
+- Plasmonic enhancement mechanism described in detail: gold nanoshell inner radius produces electric field ~10¹¹ V/cm from modest external laser (~10⁹ V/cm), accelerating deuterons to ~25 keV equivalent energy; quantum mechanical derivation of momentum gain (~10 MeV) provided with Mie theory foundation
+- D-D fuel cycle well-characterized (50% branch to ³He + n at 2.45 MeV, 50% to T + p at 3.02 MeV); D-D cross-section at 25 keV is ~0.1 mb — well-known but ~100× lower than D-T at equivalent temperature
+- Liquid D₂O jet delivery at kHz rate: Cambridge paper demonstrates stable sub-μm-thick sheet operation at 1 kHz using intersecting 25 μm D₂O cylindrical jets; target material cost demonstrated at ~$2/minute of runtime
+- OAM beam / inverse Faraday effect for self-generated magnetic confinement: mentioned in patent portfolio but not detailed in preprints
 
 **Missing**:
-- How deuteron confinement time inside the nanoshell is sustained for fusion to occur before ionization destroys the plasmon
-- How escaping deuterons (acknowledged in the paper) are handled in the energy balance
-- Whether plasmonic field enhancement inside a nanoshell has ever been measured internally (not just externally confirmed)
-- What the actual laser parameters (energy per pulse, pulse number, total power) would be for the MW-scale reactor scenario
+- Energy conversion pathway: entirely absent. The nanoshell paper assumes κ~30% for the Q~100 calculation without any engineering basis — no chamber, no heat extraction, no power cycle described
+- Mechanism for how fusion energy (D-D neutrons at 2.45 MeV + charged particles) is captured from a distributed nanoshell colloid is not addressed anywhere
+- Whether the plasmonic enhancement persists after partial ionization of the nanoshell (the paper acknowledges ionization "dampens plasmon oscillation" and flags this as requiring further investigation)
+- How escaping deuterons from each nanoshell contribute to net fusion rate (noted in paper as requiring "detailed kinetics study")
+- Rep rate path to 1 MHz: Cambridge paper demonstrates 1 kHz; Cortex claims 1 MHz but provides no engineering pathway
+- Charged particle and neutron containment/breeding (D-D does not need tritium breeding, but 2.45 MeV neutron management is unaddressed)
 
 **Gaps**:
-- Energy balance is not closed in any source: the 3 kW laser input figure appears unsupported — `truly-unknown` given current disclosure — **blocking**
-- Two different physical mechanisms appear in Cortex's own literature (plasmonic acceleration vs. quantum tunneling control); it is unclear which is being pursued and whether either can produce net energy — `proprietary` (or conceptually unresolved) — **blocking**
-- No system model, power flow diagram, or reactor architecture exists in the public record — `proprietary` — **important**
+- Energy capture architecture completely unspecified — `proprietary` / `truly-unknown` — **blocking**
+- Plasmonic ionization damping effect on fusion rate unquantified; potentially undermines the entire mechanism — `truly-unknown` — **blocking**
+- 3-orders-of-magnitude gap between demonstrated kHz neutron yield (10⁵ n/s Cambridge) and claimed reactor neutron flux (10¹⁹ n/s Cortex) — `truly-unknown` — **blocking**
+- D-D cross-section at 25 keV is ~100× lower than D-T at optimum temperature; the neutron paper does not address whether non-thermal acceleration actually reaches the claimed fusion rates — `truly-unknown` — **important**
+- Nanoshell destruction per pulse: each pulse destroys the nanoshell; recovery/recycling of gold not addressed — `truly-unknown` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-**Coverage**: Partial (physics-layer only; engineering layer absent)
+**Coverage**: Poor
 
 **Available**:
-
-| Subsystem | TRL Estimate | Basis |
-|-----------|-------------|-------|
-| Femtosecond laser (kHz class) | TRL 7–8 | Commercial availability confirmed by nanoshell paper; Cambridge paper demonstrates 1 kHz operation |
-| D2O liquid jet delivery | TRL 6–7 | Cambridge paper demonstrated stable sub-µm sheet at 1 kHz for >30 min, 1 mL/min, 1 Torr |
-| Gold nanoshell synthesis | TRL 4–5 | Hollow gold nanoshells are commercially available at research scale; mass production undemonstrated |
-| Plasmonic field enhancement (external, near-field) | TRL 5–6 | Externally measured >1000× field enhancement near gold nanoshells confirmed in published literature (Ref. [5] in nanoshell paper) |
-| Plasmonic field enhancement (internal, for D-D fusion) | TRL 1–2 | Theoretical proposal only; internal field has not been directly measured; ionization damping uncharacterized |
-| Energy capture / conversion | TRL 1 | Not specified by Cortex; Levitt 2023 mentions scintillator + semiconductor but with ~6% net efficiency, which is incompatible with commercial power |
-| Neutron shielding and management | TRL 1–2 | Not addressed by any source; D-D neutron physics is well-understood but Cortex-specific chamber design is absent |
+- **Femtosecond laser systems**: TRL 8–9 commercially. The Levitt paper and Cambridge paper both use commercial Ti:sapphire or Yb-based systems. The nanoshell paper cites commercial Yb-based lasers capable of kHz–hundreds of kHz repetition at relevant intensities. Commercial systems are available but capital cost at 1 MHz repetition rate at reactor power level is not quantified.
+- **D₂O liquid jet delivery**: TRL 5–6. Cambridge paper demonstrates stable sub-μm sheet at 1 kHz using simple pump-fed intersecting jet nozzles; target system operated continuously for 30+ minutes.
+- **D₂O as fuel**: TRL 9. Heavy water is commercially produced at industrial scale (~$600–700/kg). Liquid room-temperature fuel eliminates cryogenic target challenges.
+- **Gold nanoshell fabrication (lab scale)**: TRL 3–4. Well-established in nanophotonics/plasmonics research; Halas-group methods for ~100 nm Au nanoshells are mature at small scale.
 
 **Missing**:
-- Any TRL assessment from Cortex itself
-- Demonstration of plasmonic fusion enhancement (even at single-nanoshell scale)
-- Engineering design for nanoshell delivery at MW-scale rep rates
+- **Plasmonic D-D fusion**: TRL 1. No experimental demonstration by any group. The plasmonic enhancement for nuclear reactions is a theoretical extrapolation from known plasmonic physics for atom-scale phenomena.
+- **Nanoshell mass production**: TRL 1–2. No industrial-scale process exists; recovery of gold from spent colloidal suspension is unaddressed.
+- **Energy extraction subsystem**: TRL 0. Not even conceptually disclosed.
+- **Reactor chamber**: TRL 0. Not disclosed.
+- **Neutron management / shielding**: TRL 0. Not disclosed.
+- **Integrated system operation at reactor conditions**: TRL 0.
 
 **Gaps**:
-- Energy capture subsystem does not exist even as a concept in the relevant sources — `truly-unknown` from public record — **blocking**
-- Plasmonic internal field has never been directly measured; ionization damping (acknowledged in the paper) may prevent the mechanism from working — `truly-unknown` — **blocking**
-- No engineering design at any scale — `proprietary` (if it exists) — **important**
+- Plasmonic D-D fusion mechanism entirely undemonstrated — `truly-unknown` — **blocking**
+- Energy extraction subsystem: no concept disclosed — `truly-unknown` / `proprietary` — **blocking**
+- Gold nanoshell mass production readiness: no process exists — `not-yet-sourced` (plasmonics manufacturing literature exists but not applied to this use case) — **important**
+- TRL gap from current state (TRL 1 for core mechanism) to reactor-level integration is the largest of any concept in this portfolio — `truly-unknown` — **important**
 
 ---
 
@@ -87,20 +86,20 @@
 **Coverage**: Poor
 
 **Available**:
-- D2O (heavy water): abundant, room-temperature liquid, no cryogenic handling. The Cambridge paper cites ~$2/minute consumption at 1 mL/min for a research device. No supply chain concern.
-- Femtosecond lasers (commercial Ti:sapphire or Yb-based): commercially available at kHz rep rates; cost and lifetime data exist in commercial markets. The nanoshell paper references Yb-based lasers capable of 100s of kHz operation.
-- Gold nanoshells: ~100 nm radius hollow gold shells. Research-grade nanoshells are commercially available (Sigma-Aldrich, nanoComposix). Mass production at the scale needed for a MW reactor (10^6 nanoshells per pulse × 10^6 pulses/s = 10^12 nanoshells/s consumed) is entirely uncharacterized.
+- **D₂O (heavy water)**: Global production ~200 tonnes/year (Canada, India, China); price ~$600–700/kg. Cambridge paper demonstrates D₂O consumption of ~tens of nanoliters per shot at 1 kHz with 1 mL/minute flow; recycling demonstrated. At 1 MHz reactor scale, D₂O consumption and makeup rate is unquantified but manageable in principle given room-temperature operation.
+- **Femtosecond laser materials (Ti:sapphire, Yb:YAG)**: commercial supply chains exist for kW-class ultrafast lasers from vendors (Coherent, TRUMPF, IPG Photonics); no supply constraint for research/industrial scale.
 
 **Missing**:
-- Nanoshell consumption rate in a continuous liquid jet: do the shells survive multiple laser pulses, or are they destroyed each shot?
-- Gold supply chain at commercial scale: 10^12 nanoshells/s would represent an extraordinary gold demand if shells are single-use
-- Whether nanoshells can be recovered and recycled from the jet
-- Laser replacement intervals and component lifetime at high rep-rate operation
+- **Gold**: Gold nanoshells (~100 nm radius, ~10 nm wall thickness) contain ~10⁻¹⁷ g gold each. At 10⁶ nanoshells/pulse × 10⁶ Hz = 10¹² nanoshells/second, gold consumption rate is enormous without recycling. No gold recovery process described.
+- **Gold nanoshell synthesis at scale**: only lab-scale protocols exist (Halas group, seed-mediated growth); industrial production facility does not exist.
+- **Laser optics replacement cycle at 1 MHz**: high-intensity femtosecond laser optics have finite damage thresholds; no data on replacement cycle at reactor power levels.
+- **Activation and waste streams**: D-D produces ³He and T as byproducts; T accumulation, ³He capture strategy, and activation of structural materials from 2.45 MeV neutrons not addressed.
 
 **Gaps**:
-- Nanoshell consumption/recycling at reactor scale is completely unaddressed — `truly-unknown` — **blocking** (could make operating costs prohibitive)
-- Gold supply and cost at MW-scale are uncharacterized — `not-yet-sourced` — **important**
-- Laser capital and O&M costs at commercial scale: rough analogues exist in industrial ultrafast laser markets but no source applies this to the Cortex scenario — `derivable` with assumptions — **important**
+- Gold mass balance and recycling strategy for nanoshells: unaddressed — `truly-unknown` — **blocking** (cost viability depends entirely on this)
+- Nanoshell industrial fabrication process: does not exist — `not-yet-sourced` — **important**
+- T and ³He byproduct management: no disclosure — `not-yet-sourced` (general D-D byproduct literature exists) — **important**
+- Laser optic lifetime at reactor rep rates: `derivable` from ultrafast laser community data — **nice-to-have**
 
 ---
 
@@ -109,51 +108,67 @@
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fuel cycle | D-D (D2O liquid) | arXiv:2503.15531 | h |
-| Claimed fusion Q | ~100 (theoretical) | arXiv:2503.15531 (eq. 16) | l |
-| Claimed fusion power | ~1 MW (theoretical) | arXiv:2503.15531 (eq. 14) | l |
-| Laser input power assumed | 3 kW | arXiv:2503.15531 (eq. 16) | l |
-| Assumed thermal conversion efficiency | 30% | arXiv:2503.15531 (eq. 16, stated assumption) | l |
-| Target rep rate (aspirational) | 1 MHz | arXiv:2503.15531 | l |
-| D2O consumption rate (research scale) | ~1 mL/min (~$2/min) | Cambridge kHz paper | m |
-| Laser system: pulse duration | ~3–40 fs | arXiv:2503.15531, Cambridge paper | m |
-| Laser system: wavelength | ~780 nm–1 µm | Both papers | m |
-| Neutron energy | 2.45 MeV (D-D branch) | Cambridge paper | h |
+| Fuel type | D-D (D₂O liquid) | arXiv:2503.15531; kHz paper | high |
+| Driver energy per pulse | ~mJ class | Cambridge kHz paper (8 mJ/pulse demonstrated) | medium |
+| Rep rate (current) | 1 kHz demonstrated | Cambridge HPLSE 2024 | high |
+| Rep rate (claimed reactor) | 1 MHz | arXiv:2503.15531 | low |
+| D-D fusion energy per reaction | 3.27 MeV (n branch) / 4.03 MeV (p branch) | Standard nuclear physics | high |
+| D₂O target cost | ~$2/min at 1 kHz | Cambridge HPLSE 2024 | high |
+| Claimed thermal conversion efficiency | ~30% | arXiv:2503.15531 (assumed, no basis) | low |
+| Claimed Q factor | ~100 | arXiv:2503.15531 (theoretical, unvalidated) | low |
+| Claimed fusion power | ~1 MW | arXiv:2503.15531 (theoretical) | low |
+| Laser wall-plug power (claimed) | ~3 kW | arXiv:2503.15531 | low |
+| IFE LCOE framework (technology-agnostic) | ~$25–$100/MWh range | Hawker 2020 (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) | medium (framework only) |
+| Driver cost analog (large laser IFE) | $700–1000/J (DPSSL); <$100/J (KrF excimer target) | Xcimer whitepaper (`knowledge/sources/commercialization_of_laser_fusion_energy/`) | low (different regime) |
+
+**Hawker IFE model integration note**: The Hawker 14-parameter technology-agnostic LCOE framework (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) provides the correct structural approach for Cortex LCOE estimation: gain (G), driver cost (γ in $/J), driver energy (Ed), frequency (f), target cost (δ $/target), plant cost (α $/kWe), and thermal efficiency (μth) are all relevant parameters. However, every physics-side input from Cortex (gain, yield, fusion power) rests on unvalidated claims. The framework identifies that driver cost per joule is critical — Cortex operates in a mJ/pulse × MHz regime, a completely different scaling from the MJ-class conventional IFE that the Hawker model was calibrated against. The Xcimer whitepaper provides $700–1000/J for DPSSL and <$100/J target for KrF excimer lasers — both irrelevant to Cortex's ultrashort-pulse mJ regime, where industrial femtosecond laser pricing (e.g., TRUMPF TruMicro, Coherent Monaco) is ~$0.1–1M per system for kW-average-power units, translating to very different $/J values that have not been calculated for this concept.
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Capital cost — laser system | derivable | blocking | No Cortex-specific estimate; Xcimer source gives KrF laser costs, not applicable; commercial fs laser market rates (~$1–10M/kW avg power) could be used as rough proxy |
-| Capital cost — nanoshell production | truly-unknown | blocking | No production-scale cost model; no analogous industry |
-| Capital cost — reaction chamber / BOP | not-yet-sourced | blocking | Could use IFE chamber analogues (e.g., Hawker IFE model, ARIES IFE) as rough proxy, but geometry is completely different |
-| Capital cost — energy capture system | truly-unknown | blocking | No system designed; Levitt 2023 suggests scintillator+semiconductor but at ~6% efficiency — economically unviable |
-| Operating cost — nanoshell consumption / recycling | truly-unknown | blocking | Single-use vs. recycle not addressed; if single-use, gold cost could dominate OPEX |
-| Operating cost — laser maintenance / component replacement | not-yet-sourced | important | Commercial ultrafast laser lifetime data exists but not applied here |
-| Energy conversion pathway and efficiency | truly-unknown | blocking | No mechanism specified by Cortex; 30% assumption in paper has no engineering basis |
-| Capacity factor / availability | truly-unknown | important | No maintenance model; liquid jet continuous operation could be favorable |
-| Plant electrical output | truly-unknown | blocking | MW-scale claim is back-of-envelope; no plant study |
-| Laser wall-plug efficiency | not-yet-sourced | important | Commercial Yb:YAG ~10–30% wall-plug; Ti:sapphire ~0.1–1%; critical for energy balance |
+| Net fusion energy output (validated) | truly-unknown | blocking | Q~100 is a theoretical claim with anomalous intermediate result (3333 MeV/event); no experimental basis |
+| Driver cost at MHz rate, mJ-class fs laser | not-yet-sourced | blocking | Industrial fs laser pricing exists but $/J at MHz rep rate for reactor scale not calculated |
+| Capital cost of chamber/reactor vessel | truly-unknown | blocking | No chamber design disclosed; cannot estimate |
+| Nanoshell target cost at reactor scale | not-yet-sourced | blocking | Gold nanoshell production cost at scale not established anywhere; plasmonics fabrication literature would bound this |
+| O&M cost structure | truly-unknown | blocking | No plant design; no component replacement data |
+| Capacity factor / availability | truly-unknown | blocking | No engineering basis; no analogous system |
+| Energy conversion pathway details | truly-unknown | blocking | No cycle type specified (the 30% efficiency in the paper is a bare assumption) |
+| Gold recycling cost from colloidal system | truly-unknown | important | Determines target cost viability |
+| Blanket/shielding capital cost | truly-unknown | important | D-D produces 2.45 MeV neutrons; no shielding design disclosed |
+| T and ³He byproduct management cost | not-yet-sourced | important | Well-characterized physics; no Cortex-specific disclosure |
 
 ---
 
 ## Source Recommendations
 
-1. **Cortex patent applications** (US 19/316,087, US 63/802,958, US 63/792,117, etc.) — `not-yet-sourced`. Patent text often contains engineering details absent from papers. Search USPTO PAIR for the listed applications. May reveal nanoshell delivery mechanism, energy capture approach, chamber design. *Unverified — confirm availability before searching.*
+1. **Cortex patent full texts** (not-yet-sourced): The patent list on the Cortex website includes specific application numbers (US 63/802,958 for "D2O-Moderated, Fluid-Cooled, Hybrid Fusion-Fission Reactor System Utilizing Unenriched Uranium Fuel and Direct Brayton Cycle"; US 19/316,087 for "Bichromatic Femtosecond Direct Acceleration in Renewing Liquid Jets Using Nanoparticle-Gap Near-Fields for High-Gain Fusion"). Patent applications contain engineering details not in preprints. Search USPTO PAIR/PatentsView for these numbers. `unverified — confirm existence before searching` (some are provisional applications and may not be publicly available yet)
 
-2. **Hawker IFE simplified economic model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) — directly applicable as a fleet-wide IFE cost framework. The 14-parameter Monte Carlo LCOE model provides sensitivity structure (gain, rep rate, driver efficiency, target cost) that maps onto the Cortex concept's equivalent unknowns, even if the specific values are very different. **Read this source** to borrow the parameter sensitivity structure for the quantitative model.
+2. **Industrial femtosecond laser pricing at kHz–MHz** (not-yet-sourced): Manufacturers (TRUMPF TruMicro series, Coherent Monaco/Paladin, IPG Photonics YLPN) publish specifications for industrial kW-average-power ultrafast laser systems. This would bound the driver cost ($/J) for a credible LCOE parameter extraction. Search vendor product pages and Photonics Spectra laser market surveys.
 
-3. **PyFECONS** (`/home/reid/PyFECONS`) — contains IFE LCOE calculation code including driver cost models. The IFE modules may provide balance-of-plant cost structure analogues applicable to any laser-driven IFE concept. Use for BOP cost estimation with stated assumptions.
+3. **Gold nanoshell synthesis at scale** (not-yet-sourced): The Halas group at Rice University pioneered gold nanoshell synthesis; search their publications for cost, yield, and scalability characterizations. Also check OSTI for any DOE-funded nanomaterials production scaling studies. `unverified — confirm existence before searching`
 
-4. **Commercial femtosecond laser market data** — search industrial ultrafast laser vendor specs (Coherent, Trumpf, Light Conversion) for kHz Ti:sapphire or Yb:YAG system costs and lifetimes at the relevant power levels. *Unverified — confirm existence before searching.* Would enable a rough laser CAPEX estimate.
+4. **D-D fusion cross-section at 25 keV** (derivable): Nuclear data tables (ENDF/B-VIII, NACRE) give σ_DD at 25 keV. The paper's claimed fusion rate per nanoshell (~10⁷/s) should be checked against known cross-sections and the stated deuteron density; this may reveal the source of the anomalous 3333 MeV energy claim. All data needed is publicly available.
 
-5. **Gold nanoparticle/nanoshell manufacturing literature** — search for production-scale cost studies on hollow gold nanoshells from materials science or drug delivery literature, where large-scale nanoshell production has been explored. *Unverified — suggest search terms: "gold nanoshell manufacturing scale-up cost" on OSTI, ACS Publications.*
+5. **Physics review of the nanoshell paper claims** (not-yet-sourced): The anomalous 3333 MeV per D-D event claim and the Q~100 projection deserve independent expert review. Search for citing papers or commentary on arXiv:2503.15531 in PRL, Nuclear Fusion, or Physical Review C. As of March 2026, the paper appears to lack peer review citations.
+
+6. **Fleet source disqualifications**:
+   - `knowledge/sources/commercialization_of_laser_fusion_energy/` (Xcimer): Disqualified as cost analog. Xcimer covers 10 MJ-class KrF excimer IFE with large implosion capsules; Cortex's mJ-class ultrashort pulse regime is 10 orders of magnitude different in driver energy and uses a completely different physics mechanism (no implosion). Xcimer's $700–1000/J DPSSL vs. <$100/J KrF cost comparison does not transfer.
+   - `knowledge/sources/tea_dt_mfe_cost_analysis/`: Disqualified — D-T MFE focus with no IFE analog content applicable to this concept.
+   - `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`: Disqualified — stellarator MFE; no relevance to laser IFE.
+   - `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`: Disqualified — historical ORNL benchmarking study; the LCOE competitive landscape it establishes is at too high a level to address any Cortex-specific gap.
+   - `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`: Disqualified — four ARPA-E ALPHA concepts (none laser ICF liquid jet); CAS framework applies structurally but no direct cost analog exists for Cortex's non-implosion IFE approach.
+   - `knowledge/sources/aries_cost_account_documentation/`: Disqualified — provides the CAS 20–27/90–98 cost account structure, but Cortex's concept is so far from a defined plant design that applying CAS decomposition is premature.
+   - `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/`: Disqualified — heavy-ion driver; no relevance to femtosecond laser + nanoshell approach.
+   - `knowledge/sources/energy_from_inertial_fusion/`: Disqualified as direct analog. This 1992 review covers conventional laser/heavy-ion/light-ion IFE; Cortex's plasmonic confinement mechanism and mJ per pulse operating point are outside the scope of all architectures reviewed. No cost or design data transfers.
+   - `knowledge/sources/accelerators_for_inertial_fusion_energy_production/`: Disqualified — covers particle accelerator IFE drivers; irrelevant to laser-driven nanoshell approach.
+   - `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`: Disqualified — Pacific Fusion pulser-driven high-yield IFE (>1 GJ yield per shot, pulsed power driver); operating point and driver type have no overlap with Cortex.
 
 ---
 
 ## Summary
 
-This concept should proceed to a qualitative write-up, but the quantitative LCOE model will be almost entirely assumption-driven. The data is insufficient to produce a D1+ LCOE model grounded in company or engineering data — every input beyond basic D-D physics must be fabricated from analogs. The write-up should prominently characterize this as an extraordinary-claim pre-conceptual concept with a single theoretical paper as its entire physics basis, no experimental validation by Cortex, and zero disclosed engineering. The Cambridge kHz paper confirms the physics mechanism exists at ~10^5 n/s scale, which is nine orders of magnitude below the 10^19 n/s claimed for the reactor scenario. The quantitative model should use the Hawker IFE parameter sensitivity framework as scaffolding, with Cortex-specific inputs noted as near-total unknowns.
+This concept presents a single theoretical preprint with extraordinary unvalidated claims as its entire technical basis, no experimental results, no plant design, no energy conversion architecture, and a possible calculation error in its central Q-factor derivation. The gap count is high and almost entirely in the `blocking` category. A full D1+ analysis can proceed as a **physics critique and technology feasibility assessment** — noting what the claims are, why they are inconsistent or unvalidated, what the closest validated analog is (Cambridge kHz D-D neutron source), and what would need to be true for the concept to be viable — but it cannot produce a credible LCOE model or CAS cost decomposition. Acquiring additional sources (patent texts, independent physics review of arXiv:2503.15531) may yield engineering details from patents, but will not resolve the fundamental experimental validation gap. Recommend proceeding to analysis with a clear disclaimer that this assessment is a feasibility critique, not a techno-economic model.
 
 ---
 
@@ -161,13 +176,13 @@
 
 ```yaml
 overall_rating: "Insufficient Data"
-blocking_count: 8
-important_count: 5
-counting_method: "deduplicated across all sections: (1) energy capture mechanism unspecified, (2) physics unvalidated by Cortex, (3) energy balance not closed, (4) two conflicting mechanisms in Cortex literature, (5) capital costs entirely absent, (6) plant electrical output unspecified, (7) nanoshell consumption/recycling at scale unknown, (8) energy conversion efficiency has no engineering basis — plus 5 important gaps: neutron management, nanoshell mass production, laser OPEX, capacity factor model, wall-plug laser efficiency"
+blocking_count: 7
+important_count: 7
+counting_method: "deduplicated across all five sections — each unique gap counted once regardless of how many sections it affects; blocking = prevents any credible LCOE or plant-level analysis; important = limits depth/confidence of qualitative sections"
 section_coverage:
   availability_of_data:       "Poor"
   system_function:            "Poor"
-  subsystem_maturity:         "Partial"
+  subsystem_maturity:         "Poor"
   materials_supply_chain:     "Poor"
   lcoe_parameter_extraction:  "Poor"
 ```
\ No newline at end of file
```
