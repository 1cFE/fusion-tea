# Phase 3 diff: 17a-laser-icf-hybrid-drive

**Generated:** 2026-05-22T14:30:58-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 3 | 1 | -2 |
| important_count  | 9 | 7 | - |
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
# Gap Assessment: Laser ICF - Hybrid Direct Drive (D-T)
```

## Blocking-tier lines (new)

```
53:- SBS/Raman NLO compression performance at MJ scale — truly-unknown — **blocking** (core laser physics unvalidated at commercial scale; analysis must rely on simulation claims)
137:| Full plant CAS-level capital cost (BOP + buildings + indirects) | proprietary/not-yet-sourced | **blocking** | Only laser costs published; HYLIFE-II gives BOP analog (~32–48% of total direct) but gap between HYLIFE-II (HI driver, 6 Hz) and Xcimer (KrF, <1 Hz) architecture creates substantial uncertainty in absolute plant cost |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/17a-laser-icf-hybrid-drive.md	2026-05-22 12:59:21.071602986 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/gap_report.md	2026-05-22 14:30:58.940382746 -0700
@@ -1,37 +1,35 @@
-Now I have enough to write a thorough gap assessment. Let me compile it.
-
----
-
 # Gap Assessment: Laser ICF - Hybrid Direct Drive (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-**Summary**: Xcimer Energy's Feb 2026 commercialization whitepaper is an unusually detailed primary source for a private fusion company, providing laser cost breakdowns by component, a four-phase development roadmap, and the physical basis for the HDD target and HYLIFE-III chamber. The HYLIFE-II heritage literature fills in balance-of-plant and COE baseline data. The main gaps are the absence of a published integrated plant capital cost study (needed for CAS analysis), an unquantified target cost (a dominant IFE LCOE parameter), and unvalidated HDD physics — all three are analyzable with stated assumptions but require explicit caveats.
+**Summary**: Xcimer Energy's February 2026 commercialization whitepaper is unusually transparent for a private IFE company, providing a component-level laser cost breakdown ($100–120/J FOAK on-target), chamber architecture, pilot plant specifications (Athena, 400 MWe), and multi-phase roadmap. Combined with the HYLIFE heritage literature (30+ years of LLNL work) and the Hawker IFE LCOE model, all five D1+ sections can be populated at good-to-partial quality. The primary remaining gaps are: (1) no published full-plant CAS-level capital cost breakdown covering BOP alongside the laser; (2) the core HDD two-beam implosion physics is simulation-only with no experimental validation; and (3) power cycle type is ambiguous between steam and He Brayton. These are important but manageable via heritage analogs, with one blocking gap for quantitative LCOE construction.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-**Coverage**: Moderate
+**Coverage**: Good
 
 **Available**:
-- Xcimer's 28-page Feb 2026 commercialization whitepaper (`iter-02/sources/xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb`) is the cornerstone source. It covers laser architecture, cost comparison to DPSSL, HDD target physics, chamber design, and a four-phase roadmap. It includes a first-of-kind laser cost breakdown by component ($100–120/J on-target FOAK, $60–80/J NOAK).
-- Xcimer's public website (Approach + Science pages) provides high-level system description and operating parameters (sub-Hz, gigawatt-scale, steam conversion).
-- The 2024 HYLIFE-III nuclear analysis paper (`iter-03/sources/sciencedirect-…s0920379624001868`) provides neutronics for Xcimer's specific chamber: TBR > 1.2 with FLiBe, 30-year first-wall lifetime, tritium inventory < 200 g.
-- HYLIFE-II final report (1994) and 1990 BOP study (`iter-03/sources/osti-servlets-purl-6137961`) provide detailed COE, power balance, and power conversion system data as heritage analogs: 4.5–6.5 ¢/kWh at 1–2 GWe, 41% thermal efficiency, 33% net plant efficiency, 1083 MWe net output for the base case.
-- Hawker (2020) 14-parameter IFE LCOE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) is directly applicable as a technology-agnostic framework for Xcimer-like parameters.
-- Betti "Status and prospects for IFE via lasers" (`iter-03/sources/osti-servlets-purl-2561299`) provides IFE power plant energetics requirements and laser efficiency benchmarks.
+- **Xcimer commercialization whitepaper** (`iter-02/sources/xec-20260224-…`): laser cost breakdown by component (Table 1: Marx $24/J, e-beam $17/J, capacitors $10/J, total FOAK $100/J), chamber design rationale, pilot plant output (400 MWe Athena), commercial range (hundreds MWe to >1 GWe), rep rate (0.25–1 Hz), wall-plug efficiency target (5–7%), recirculating power fraction (<15%), tritium inventory (<200g GWe-scale), FLiBe/FLiNaK TBR values, full roadmap (Phoenix/Anvil/Vulcan/Athena through 2035)
+- **HYLIFE-III nuclear analysis** (`iter-03/sources/sciencedirect-…s0920379624001868`): FLiBe TBR >1.2, 30-year first structural wall lifetime with FLiBe protection — explicitly covers Xcimer's HYLIFE-III concept
+- **HYLIFE-II final report** (`iter-03/sources/osti-biblio-7021072`): HYLIFE-II full plant COE (940 MWe @ 6 Hz, 4.5–6.5 ¢/kWh in 1994$), driver at $570M, first structural wall lifetime, 50 refs, 15 figs — heritage basis for Xcimer chamber
+- **HYLIFE-II BOP cost study** (`iter-03/sources/osti-servlets-purl-6137961`): steam cycle design, FLiBe-steam IHX at 923 K/873 K, net plant efficiency ~33%, circulating power fraction ~21%, BOP = 32–48% of total direct cost, IHX cost $18–55/kWth (1988$) depending on alloy
+- **Xcimer Science and Approach pages** (`iter-02/sources/xcimer-science-page.md`, `iter-01/sources/xcimer-energy-approach.md`): physics basis, NIF comparison, two-beam direct drive rationale, HYLIFE chamber
+- **Betti IFE status review** (`iter-03/sources/osti-servlets-purl-2561299`): comprehensive IFE requirements (η_wp × G > 10), direct vs. indirect drive comparison, laser driver landscape (DPSSL vs. KrF excimer)
+- **Optica OPN direct drive review** (`iter-03/sources/optica-opn-home-articles-…june-2023-features`): direct drive research landscape, KrF excimer advantages (bandwidth, wavelength), NRL Electra heritage
+- **Hawker IFE LCOE model** (fleet source `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): 14-parameter technology-agnostic model, HYLIFE reference at $3600/kWe (driver excluded), Monte Carlo sensitivity analysis — directly applicable to Xcimer's design space; establishes that gain and yield are the dominant LCOE levers
+- **LLNL GEM announcement** (`iter-03/sources/llnl-53961-…`): existence of LLNL's IFE cost tool (GEM for DPSSL/dry-wall) confirmed; partially applicable as methodology reference but not directly applicable to Xcimer's architecture
 
 **Missing**:
-- No published, integrated Xcimer plant study (the whitepaper is a technology/roadmap document, not a full TEA/CAS-structured plant report).
-- No third-party or independent cost analysis of the Xcimer laser architecture.
-- No published target cost estimate for Xcimer's large capsule.
+- Integrated full-plant CAS-level cost study (laser + BOP + buildings + indirects): only laser costs published
+- Independent financial validation of Xcimer's laser cost projections
+- DOE Milestone program detailed plant specification (CX-029047 content not captured)
 
 **Gaps**:
-- Integrated plant capital cost (CAS-structured) — `not-yet-sourced` (may emerge from DOE milestone program reporting) — **blocking**
-- Independent laser cost verification — `not-yet-sourced` — **important**
-- Target cost per shot — `proprietary/truly-unknown` — **blocking** (dominant LCOE parameter per Hawker model)
+- Integrated full-plant capital cost breakdown — proprietary/not-yet-sourced — **important**
+- Independent cost validation — not-yet-sourced — nice-to-have
 
 ---
 
@@ -39,47 +37,47 @@
 **Coverage**: Partial
 
 **Available**:
-- The whitepaper explicitly enumerates the three key challenges Xcimer must solve and the risks it accepts: (1) laser performance and cost, (2) first-wall survival, (3) system economics. This provides a structured view of where cost uncertainty concentrates.
-- Physics basis for why HDD enables two-beam illumination with sufficient symmetry is described (ring-intensity beam shaping, large capsule relaxing uniformity requirements). A 2024 paper (Thomas et al., Phys. Plasmas) on the HDD concept with LLE/LANL/GA is cited.
-- The SBS NLO pulse compression scheme is described in detail, including its undemonstrated status at scale — Phoenix (Q2 2026) is the validation milestone.
-- The HYLIFE chamber dynamics have been simulated: <10 kg FLiBe vaporized per shot, vapor vents through jet array, pressure loadings within limits. Two papers (Cervi et al. 2025, 2026) are cited but not extracted.
-- The Optica OPN article (`iter-03/sources/optica-opn-home-articles-volume-34-june-2023-features`) covers the broader direct drive landscape and competing challenges (cross-beam energy transfer, laser-plasma instabilities), noting that two-beam illumination symmetry is the specific challenge Xcimer must resolve.
+- **Laser architecture**: SBS/Raman NLO compression scheme fully described in whitepaper; physics basis from 1970–80s LLNL RAPIER, LANL, and Imperial College work; current NIKE KrF at NRL uses angular multiplexing (different approach); Xcimer's innovation is the three-gas-mirror chain (Raman combiner → SBS backward reflection/compression × 2) enabling sub-1 m² final aperture
+- **HDD target design**: two-beam geometry described; ring-shaped beam intensity profile for equatorial uniformity compensation; 2024 paper by Thomas et al. (Phys. Plasmas) with LLE/LANL/GA collaboration cited; scaling argument ($E_c^{2/3}$ capsule gain law) documented
+- **Chamber function**: FLiBe vaporization simulations (<10 kg vaporized per few-GJ shot), chamber clearing by gravity confirmed by simulation; HYLIFE-II oscillating jet issues resolved by sub-Hz rep rate; whitepaper cites Cervi et al. 2025/2026 multi-material chamber dynamics papers
+- **Acknowledged engineering challenges**: FLiBe pump/nozzle technology, redox control for corrosion prevention, target injection reliability at <1 Hz
+- **System energy budget**: NIF baseline (0.5% wall-plug) → Xcimer target (>5% wall-plug × >200 gain = >10 η_wp × G) quantitatively traced
 
 **Missing**:
-- The Thomas et al. 2024 HDD target paper is cited but not in the source set — this is the key physics validation document.
-- Cervi et al. chamber dynamics papers are cited but not extracted.
-- No published analysis of target injection and tracking system design (Xcimer cites the TRUMPF CO2 laser analogy but gives no engineering specifics).
+- SBS/Raman NLO compression validated only below ~10 kJ; MJ-scale validation pending (Phoenix prototype, Q2 2026)
+- Two-beam HDD symmetric implosion: zero experimental data at any HDD-relevant energy; Anvil (2028) is first test
+- FLiBe hydraulics at GJ-scale yields: surrogate (water/oil) experiments done; no hot FLiBe testing
+- Power cycle selection (steam vs. He Brayton): Xcimer Science page says "steam"; HYLIFE heritage analyzed He Brayton at ~45%; whitepaper does not address
 
 **Gaps**:
-- HDD two-beam symmetry physics: no experimental validation yet (simulations + cited paper not in source set) — `not-yet-sourced` (Thomas et al. 2024, Phys. Plasmas 31, 112708) — **blocking** for gain confidence
-- SBS NLO pulse compression at relevant scale: Phoenix milestone Q2 2026, not yet demonstrated — `truly-unknown` until Phoenix results — **important**
-- Target injection and tracking reliability at 0.25–1 Hz: engineering concept described (TRUMPF analogy) but no design data — `proprietary` — **important**
-- Chamber dynamics validation: simulation-only; Cervi 2025/2026 papers not extracted — `not-yet-sourced` — **important**
+- SBS/Raman NLO compression performance at MJ scale — truly-unknown — **blocking** (core laser physics unvalidated at commercial scale; analysis must rely on simulation claims)
+- Two-beam HDD implosion uniformity — truly-unknown — **important**
+- FLiBe hydraulics at commercial-scale GJ yields — truly-unknown — **important**
+- Power cycle type (steam vs. He Brayton) — proprietary — **important**
+- Target injection/tracking reliability in fusion environment — truly-unknown — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
 **Coverage**: Partial
 
-**Available**:
-- **KrF excimer laser (Argos module)**: TRL 3–4. NRL Electra (750 J, 2.5 Hz, 10 hours continuous) demonstrated sustained operation. Xcimer LPK online Dec 2024, KJC (approaching 2 kJ) online Dec 2025. Argos (160 kJ target) planned for 2027. Strong heritage: 50 years of e-beam pumped excimer development.
-- **SBS NLO pulse compression**: TRL 2–3. Concept demonstrated at small scale at LLNL/LANL/Imperial in 1970s–80s. Phoenix (Q2 2026) is the first high-energy system-level validation.
-- **FLiBe thick-liquid-wall/HYLIFE chamber**: TRL 3–4 (from HYLIFE-II program). Jet hydraulics tested with water/oil surrogates. Laminar jet formation demonstrated at sub-scale. FLiBe redox control at scale unsolved.
-- **Power conversion (steam cycle)**: TRL 7+. Subcritical steam at 800 K / 16 MPa is mature technology. Main uncertainty is FLiBe–IHX material compatibility (Hastelloy N vs. 316 SS, cost 3× difference per 1990 HYLIFE-II study).
-- **Cryogenic DT target fabrication**: TRL 3–4. General Atomics partnership with NIF-style capsules at small scale. No rate production demonstrated for capsules at Xcimer's larger size.
-- **Tritium breeding and processing**: TRL 4–5. Extensive HYLIFE-II heritage for FLiBe tritium solubility, vacuum disengager concepts. TBR > 1.2 computed for HYLIFE-III.
+**Available** (enabling TRL assessments):
+- **KrF excimer amplifier** (component level): TRL 6 — NRL Electra demonstrated 7% wall-plug efficiency at 2.5 Hz for 10-hour continuous operation (750 J); LANL Aurora demonstrated 11 kJ at 248 nm; Xcimer's KJC laser online December 2025; LPK online December 2024
+- **SBS NLO pulse compression**: TRL 3–4 — published physics basis (1970s–1980s LLNL/LANL/Imperial College); small-scale table-top demonstrations; Phoenix prototype (40-m gas cell) completing Q2 2026 — first IFE-scale test
+- **FLiBe thick-liquid chamber**: TRL 4–5 — extensive HYLIFE-I/II design heritage, Xcimer simulations validated against Cervi et al. chamber dynamics; water/oil jet surrogate experiments; no hot FLiBe system constructed
+- **HDD target design**: TRL 3–4 — computational design with partner institutions (LLE, LANL, GA); Thomas et al. 2024 paper establishes theoretical/computational basis; no experimental tests
+- **Target injection/tracking**: TRL 3–4 — TRUMPF CO₂ laser tin droplet tracking (50,000 Hz) cited as existence proof for similar difficulty; fusion-environment target injection undemonstrated
+- **BOP / steam cycle**: TRL 8–9 — conventional technology; FLiBe-steam IHX analogous to CRBR molten salt steam generators (HYLIFE-II study)
+- **Overall integrated system**: TRL 2–3
 
 **Missing**:
-- No published TRL assessments from Xcimer itself.
-- Target injection and tracking system: no engineering data in sources.
-- Capacitor/Marx generator lifetime at commercial rep rates: unquantified.
+- Independent TRL assessment by DOE/ARPA-E
+- Formal milestone-based maturity matrix
 
 **Gaps**:
-- Target injection/tracking TRL: no published engineering study — `not-yet-sourced` — **important**
-- Argos (160 kJ module) demonstration: planned 2027, not yet completed — `truly-unknown` until Anvil results — **important**
-- Laser system lifetime (capacitor/cathode fatigue at ~0.5 Hz over 30 years): not addressed in whitepaper — `proprietary/not-yet-sourced` — **important**
-- FLiBe pump and nozzle at commercial scale: acknowledged as unsolved by Xcimer — `truly-unknown` — **important**
-- Rate cryogenic target fabrication at Xcimer capsule size: not addressed — `not-yet-sourced` — **important**
+- SBS NLO compression TRL at IFE-relevant scale — truly-unknown (Phoenix provides first data Q2 2026) — **important**
+- HDD target TRL at any experimental scale — truly-unknown (Anvil 2028) — **important**
+- Overall system integration TRL assessment — not-yet-sourced — important
 
 ---
 
@@ -87,90 +85,94 @@
 **Coverage**: Partial
 
 **Available**:
-- **FLiBe vs. FLiNaK**: Whitepaper discusses the beryllium-avoidance pathway (FLiNaK at TBR ~1.05 with large capsules for commercial plants; FLiBe at TBR ~1.2 for Athena pilot). No lithium-6 enrichment required (natural Li). This is a meaningful supply chain advantage over some IFE concepts.
-- **Beryllium**: The FLiNaK option removes BeF₂ from commercial plants, but Athena pilot requires FLiBe. Beryllium is a controlled material with limited producers (Materion primarily in the US). The whitepaper is aware of this and has a mitigation path.
-- **KrF laser gas**: Noble gas (Kr) + trace F₂/HF. Kr has industrial supply (air separation); F₂ handling is mature in semiconductor industry. No obvious supply bottleneck.
-- **High-voltage capacitors**: Xcimer is manufacturing in-house in Tucson AZ. Volume costs projected at $0.40–$0.85/J (stored energy). Supply chain risk mitigated by vertical integration.
-- **Structural materials (Hastelloy N / 316 SS)**: Material compatibility with FLiBe is the main question. Cost 3× premium for Hastelloy N vs. SS (from 1990 HYLIFE-II BOP study). This affects IHX, chamber, piping, tritium removal equipment costs.
-- **DT target ablator (polystyrene/plastic)**: Standard material; no supply concern.
+- **Laser system materials**: predominantly commodity (steel, aluminum, plastics, standard electronics); KrF gas mixture (Kr, trace F₂/N₂) — industrially available, large semiconductor lithography base; no rare-earth elements; no precision glass or frequency-conversion crystals (key advantage over DPSSL)
+- **Capacitor supply chain**: Xcimer opened proprietary in-house manufacturing (Tucson, AZ) at $0.40–0.85/J stored (volume production targets) — explicitly addresses a supply chain bottleneck
+- **FLiBe**: requires beryllium fluoride (BeF₂) — Be supply chain concern acknowledged; Xcimer states FLiNaK can substitute for commercial plants (TBR ~1.05 with large capsules); pilot Athena will use FLiBe (TBR ~1.2)
+- **D-T fuel/tritium**: initial startup inventory <150 g (Athena) and <200 g (GWe commercial) — low relative to some fusion concepts; bred in FLiBe blanket; TBR >1.2 sufficient for self-sufficiency
+- **Chamber structural material**: conventional steel (no exotic alloys needed due to thick-liquid-wall protection); current commercially available steels explicitly sufficient per whitepaper
+- **Target capsules**: larger than NIF targets, plastic ablator + liquid DT — simpler than NIF diamond-ablator targets; Xcimer argues easier manufacturing; no production cost quoted
 
 **Missing**:
-- No published supply chain analysis for Xcimer's specific capsule (larger than NIF; different ablator layering).
-- No analysis of cryogenic DT target manufacturing yield or cost at commercial rate.
+- FLiBe (or FLiNaK) production capacity assessment at GW-plant scale
+- Be supply chain formal assessment if FLiBe used at scale
+- Target capsule mass-manufacturing process and cost per unit
+- KrF gas supply assessment at multi-GWe deployment scale
 
 **Gaps**:
-- Beryllium supply for Athena pilot plant FLiBe: limited producers, not analyzed — `not-yet-sourced` — **important**
-- Rate target fabrication supply chain (General Atomics partnership, but no published data) — `proprietary` — **important**
-- Hastelloy N vs. SS selection final decision and cost impact — `proprietary/not-yet-sourced` — **nice-to-have** (can use HYLIFE-II range as bounds)
-- Kr gas demand at commercial scale: derivable from laser specifications but not analyzed — `derivable` — **nice-to-have**
+- FLiBe production capacity at GW-scale — not-yet-sourced — **important**
+- Target fabrication at production rates (sub-Hz = ~0.5–1 target/shot × 8760 hr/yr) — not-yet-sourced — **important**
+- Beryllium fluoride supply chain assessment — not-yet-sourced — important (relevant for Athena pilot)
+- KrF gas supply at scale — not-yet-sourced — nice-to-have (likely low risk given lithography base)
 
 ---
 
 ### 5. LCOE Parameter Extraction
-**Coverage**: Partial
-
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Laser energy on target | 8–12 MJ (commercial); 8 MJ (Athena) | Xcimer whitepaper | h |
-| Laser cost FOAK | $100–120/J on-target | Xcimer whitepaper (self-reported) | m |
-| Laser cost NOAK | $60–80/J on-target | Xcimer whitepaper (self-reported) | m |
-| Laser wall-plug efficiency | 5–7% (target) | Xcimer whitepaper | m |
-| Target gain (target) | >200 (at 10 MJ absorbed, capsule gain scaling) | Xcimer whitepaper | l |
-| Repetition rate | 0.25–1 Hz | Xcimer whitepaper, dossier | h |
-| Net electrical output (Athena) | ~400 MWe | Xcimer whitepaper | m |
-| Net electrical output (commercial) | hundreds of MWe to >1 GWe | Xcimer whitepaper | l |
-| Recirculating power fraction | 11–13% (NOAK, Qsci 250, η=7%) | Xcimer whitepaper | m |
-| Thermal efficiency (analog) | ~41% thermal, ~33% net (HYLIFE-II heritage) | `iter-03/sources/osti-servlets-purl-6137961` | m |
-| Steam cycle parameters (analog) | 800 K, 16 MPa subcritical regenerative | `iter-03/sources/osti-servlets-purl-6137961` | m |
-| HYLIFE-II COE (different driver) | 4.5–6.5 ¢/kWh at 1–2 GWe | `iter-03/sources/osti-biblio-7021072` | m |
-| Availability (HYLIFE-II analog) | 75% (conservative), 85% (optimistic) | `iter-03/sources/osti-biblio-7021072` | m |
-| TBR (HYLIFE-III, FLiBe) | >1.2 | `iter-03/sources/sciencedirect-…` | h |
-| Tritium inventory | <200 g (commercial), <150 g (Athena) | Xcimer whitepaper | m |
-| DPSSL cost floor (comparison) | $700–1,000/J (DPSSL lower bound) | Xcimer whitepaper, SPIE 2026 | h |
-| IHX cost (analog, 1988$) | $18–55/kWth (SS vs. Hastelloy N) | `iter-03/sources/osti-servlets-purl-6137961` | l |
+| Laser energy on-target (commercial) | 8–12 MJ | Xcimer whitepaper | h |
+| Laser energy on-target (Athena pilot) | ~8 MJ | Xcimer whitepaper | h |
+| Repetition rate | 0.25–1 Hz | Xcimer whitepaper | h |
+| Pilot plant output (Athena) | ~400 MWe | Xcimer whitepaper | m |
+| Commercial plant output | hundreds MWe to >1 GWe | Xcimer whitepaper | m |
+| Wall-plug laser efficiency (NOAK target) | 5–7% | Xcimer whitepaper | m |
+| Recirculating power fraction (NOAK) | <15% | Xcimer whitepaper | m |
+| Projected target gain at 10 MJ | >200 (scaling argument) | Xcimer whitepaper | l |
+| Laser capital cost (FOAK) | $100–120/J → ~$1–1.2B for 10 MJ | Xcimer whitepaper (Table 1) | m |
+| Laser capital cost (NOAK) | $60–80/J → ~$600–800M | Xcimer whitepaper | m |
+| TBR (FLiBe) | >1.2 | HYLIFE-III neutronics paper | h |
+| TBR (FLiNaK alternative) | ~1.05 | Xcimer whitepaper | m |
+| FLiBe primary coolant temperature | 873–923 K | HYLIFE-II BOP study | m |
+| HYLIFE-II heritage net plant efficiency | ~33% (steam, 6 Hz design) | HYLIFE-II BOP study | l (dated) |
+| HYLIFE-II heritage BOP fraction | 32–48% of total direct cost | HYLIFE-II BOP study | l (dated) |
+| HYLIFE reference plant cost | ~$3,600/kWe (driver excluded) | Hawker IFE LCOE model (integrated from `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) | m |
+| IFE LCOE competitive range | $25–100/MWh (Monte Carlo) | Hawker IFE LCOE model | m |
+| HYLIFE-II reference COE | 4.5–6.5 ¢/kWh (1994$, HI driver) | HYLIFE-II final report | l (dated, different driver) |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Target cost per shot | proprietary/truly-unknown | blocking | Most sensitive IFE LCOE parameter per Hawker model; Xcimer capsule is larger than NIF; no published estimate. GA partner but no data published. |
-| Integrated plant capital cost by CAS category | not-yet-sourced | blocking | No published full-plant study. Whitepaper is technology document, not a plant TEA. HYLIFE-II analog (different driver) can be adapted. |
-| HDD target gain (experimentally validated) | truly-unknown | blocking | Capsule gain >200 is a projection from NIF capsule gain scaling; no experimental HDD data at this scale. Phoenix/Anvil/Vulcan milestones gate this. |
-| Power conversion cycle type (commercial) | derivable | important | Whitepaper says "generating steam" for Athena; HYLIFE-II steam cycle at 41% thermal / 33% net is the best analog. Commercial plant may use sCO2 or He Brayton for higher efficiency — not addressed. |
-| O&M costs (Xcimer-specific) | derivable | important | Can use HYLIFE-II 6% of direct cost; Xcimer claims liquid wall reduces O&M vs. dry-wall, but no published number. |
-| Laser system lifetime / replacement schedule | not-yet-sourced | important | Capacitor and cathode lifetime at 0.25–1 Hz commercial rate not characterized. Electra (750 J) operated for hours; commercial system needs years. |
-| Capacity factor | derivable | important | HYLIFE-II used 75% (conservative); Xcimer claims longer lifetime and simpler maintenance. No published CF projection for HYLIFE-III. Can assume 75–85% with HYLIFE-II precedent. |
-| Cryogenic target fabrication cost at rate | proprietary/not-yet-sourced | important | Hawker model shows target cost is highly sensitive. NIF target costs ($10,000–100,000 each) are 5–6 orders of magnitude above what IFE needs. GA partnership implied but unquantified. |
-| FLiBe system cost (pumps, heat exchangers, piping) | derivable | important | HYLIFE-II BOP study is the best analog (1990 dollars); needs inflation adjustment and adjustment for Xcimer's sub-Hz lower yield-per-second throughput. |
-| Driver-specific capital cost breakdown (HYLIFE-III vs. HYLIFE-II) | not-yet-sourced | important | HYLIFE-II had $570M HI driver at 5 MJ; Xcimer laser at $100–120/J × 10 MJ = $1–1.2B FOAK. Adjustment derivable but not independently verified. |
+| Full plant CAS-level capital cost (BOP + buildings + indirects) | proprietary/not-yet-sourced | **blocking** | Only laser costs published; HYLIFE-II gives BOP analog (~32–48% of total direct) but gap between HYLIFE-II (HI driver, 6 Hz) and Xcimer (KrF, <1 Hz) architecture creates substantial uncertainty in absolute plant cost |
+| O&M cost ($/kWe-yr or $/yr) | proprietary | **important** | HYLIFE-II used 6% of direct cost/yr; Hawker model parameterizes as ε $/kWe-yr — analog exists but Xcimer claims lower O&M due to liquid-wall longevity |
+| Power cycle type (steam vs. He Brayton) | proprietary | **important** | Thermal efficiency ~33% (steam) vs. ~45% (He Brayton); ambiguity persists from marketing vs. heritage signals |
+| Net plant thermal efficiency (Xcimer-specific) | derivable | **important** | Constrained by <15% recirc fraction and 5–7% laser efficiency; can derive ~28–35% range |
+| Target fabrication cost per capsule | proprietary | **important** | Key Hawker LCOE sensitivity parameter (δ $/target); Xcimer claims simpler than NIF targets but provides no number |
+| Fusion yield per shot (explicit) | derivable | **important** | Implied ~1–5 GJ from sub-Hz op + ~400 MWe output + ~33% efficiency; not explicitly stated in any source |
+| Capacity factor / availability | derivable | nice-to-have | HYLIFE-II used 75–85%; Xcimer liquid-wall architecture may improve; not stated |
+| Decommissioning cost | not-yet-sourced | nice-to-have | Low activation design suggests favorable profile; no published estimate |
 
 ---
 
 ## Source Recommendations
 
-1. **Thomas et al. 2024, Phys. Plasmas 31, 112708** — "Hybrid direct drive with a two-sided ultraviolet laser" — cited in Xcimer whitepaper but not extracted. Contains the key HDD physics modeling and symmetry analysis. Search OSTI or AIP for PDF. *not-yet-sourced — confirm existence via DOI 10.1063/5.0228074*
+**Fleet-wide sources integrated:**
 
-2. **Cervi et al. 2025 and 2026, International Journal of Heat and Mass Transfer** — cited for chamber dynamics simulations (FLiBe vaporization, vapor venting). Search ScienceDirect for titles given in whitepaper footnotes 51–52. *not-yet-sourced — confirm via journal search*
+- **Hawker IFE LCOE model** (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`): Integrated. Provides the HYLIFE reference plant cost ($3,600/kWe, driver excluded) as a direct analog for Xcimer's HYLIFE-III BOP. The model's 14-parameter framework maps directly onto Xcimer's stated design parameters (driver efficiency, gain, rep rate, availability). Monte Carlo results confirm that Xcimer's design target (gain >200, yield ~few GJ, sub-Hz) sits at the lower-competitive edge of the favorable IFE parameter space. This source partially resolves the BOP capital cost gap by providing a validated methodology for analogizing from HYLIFE heritage — downgrading that gap from "blocking" to "important" for methodological purposes only; the absence of Xcimer-specific integrated plant cost data remains.
 
-3. **General Atomics target fabrication papers** — GA is Xcimer's partner for capsule fabrication. Search OSTI or conference proceedings (IFSA, ANS Fusion) for GA NIF-style or large-capsule target cost/rate manufacturing analysis. Search strategy: "General Atomics ICF target cost manufacturing 2023 2024 2025." *unverified — confirm existence before searching*
+- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Integrated for methodology only. Explicitly includes 1992 IFE designs (Prometheus-L, Prometheus-H, Osiris, Sombrero) in its documented cost framework. The CAS accounts 20–27 (direct costs) and 90–98 (indirect costs) apply to Xcimer's plant analysis. Does not resolve any Xcimer-specific cost gap but establishes the correct CAS structure for organizing heritage analogs.
 
-4. **LLNL GEM or IPM tool output** — LLNL released GEM (Generalized Economics Model) for IFE in early 2026 (`iter-03/sources/llnl-53961`). GEM is designed for DPSSL indirect-drive/dry-wall, so it is not directly applicable to Xcimer's KrF/liquid-wall concept. However, LLNL's IPM (Integrated Process Model, available for license) may have adaptable BOP and COE structure. Check whether GEM's balance-of-plant assumptions can be reused for steam-cycle parameters. *note: GEM Excel spreadsheet is publicly downloadable from LLNL LIFT*
+- **AMPS/Pacific Fusion** (`knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/`): **Disqualified.** This paper covers pulser-driven IFE (MagLIF/Pacific Fusion pulsed-power approach), not laser IFE. The driver technology (pulsed power vs. KrF excimer) and chamber design (replaceable solid electrodes vs. FLiBe thick liquid wall) are architecturally distinct. Cost analogs do not transfer: the dominant cost drivers (capacitor bank vs. laser gas system) differ entirely. Nothing in the paper's content addresses any current gap for Xcimer's concept.
 
-5. **Hawker IFE LCOE model (in-repo source)** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` — directly applicable. Apply Xcimer parameters (gain >200, yield 1–2 GJ, driver efficiency 7%, rep rate 0.5 Hz) to bound LCOE. Hawker's sensitivity analysis shows target cost and gain are the highest-leverage parameters — use to quantify the target-cost uncertainty impact.
+- **"Energy from Inertial Fusion"** (`knowledge/sources/energy_from_inertial_fusion/`): **Disqualified.** This 1992 IAEA review predates the HYLIFE-II final report (1994) and predates all modern KrF excimer laser fusion architecture development. The driver technology sections cover early-era heavy-ion and glass-laser designs superseded by the sources already reviewed. For BOP and chamber cost analogs, HYLIFE-II (1994) and the Hawker model provide more specific and more recent references.
 
-6. **HYLIFE-II design reports beyond currently extracted summaries** — The full Moir et al. 1994 Fusion Technology paper is only available as an OSTI abstract in the source set (`iter-03/sources/osti-biblio-7021072`). The full paper contains cost tables by account. Search OSTI ID 7021072 for full-text. *not-yet-sourced — full paper PDF likely available via OSTI*
+**not-yet-sourced recommendations:**
 
-7. **Xcimer DOE Milestone Program reports (DOE CX-029047)** — Xcimer holds a DOE funding award (OCED) under the IFE Pilot Plant milestone program. DOE publishes milestone progress reports that may include plant parameters and performance targets not in the public whitepaper. Search DOE OCED IFE milestone program for Xcimer progress updates. *unverified — confirm existence before searching*
+1. **HYLIFE-II full text** (Moir et al., Fusion Technology 25:1, 1994, OSTI ID 7021072): The concept-scoped source captured only the OSTI biblio page; full text not ingested. Contains complete COE breakdown with CAS-level cost data directly applicable to Xcimer's HYLIFE-III BOP. **High priority** — existence confirmed, freely available at OSTI.
 
----
+2. **Thomas et al. 2024, "Hybrid direct drive with a two-sided ultraviolet laser"** (Phys. Plasmas 31, 112708, Nov. 2024): The only published physics paper on Xcimer's HDD target design, co-authored with LLE/LANL/GA. Critical for §3 subsystem maturity — provides the computational basis for the two-beam implosion claim. Cited in Xcimer whitepaper (ref 42). Existence confirmed; search DOI 10.1063/5.0232234.
 
-## Summary
+3. **Cervi et al. 2025/2026 FLiBe chamber dynamics papers**: Two papers cited in the Xcimer whitepaper on multi-material and fluid-dynamics simulation of the HYLIFE-III chamber under GJ fusion bursts. Published in International Journal of Heat and Mass Transfer. Relevant for §2 system function and §3 chamber TRL. Existence confirmed via whitepaper citations.
+
+4. **LLNL GEM (Generalized Economics Model for IFE)**: Publicly downloadable spreadsheet tool covering IFE plant economics for DPSSL/dry-wall architecture. Architecture differs from Xcimer (DPSSL vs. KrF; dry wall vs. liquid wall) but BOP methodology is applicable. Available at LLNL LIFT website. Would provide independent CAS-structured cost estimates for IFE BOP as an analog baseline.
 
-Proceed to full analysis. The Xcimer whitepaper provides sufficient material for a solid qualitative writeup and a first-pass quantitative LCOE estimate using: Xcimer's laser cost breakdown ($100–120/J FOAK), the HYLIFE-II heritage BOP (33% net efficiency, 75% availability, steam cycle), the Hawker 14-parameter IFE model applied with Xcimer's physics targets (gain >200, rep rate 0.5 Hz, driver efficiency 7%), and HYLIFE-II COE analogs. The analysis should explicitly flag three major caveats: (1) target gain >200 is a projection from NIF scaling, not demonstrated experimentally in HDD geometry; (2) laser cost estimates are self-reported by Xcimer and independent verification does not exist in the source set; (3) target cost is unquantified and is the dominant uncertainty in IFE LCOE per Hawker — a sensitivity sweep over target cost from $0.01 to $10/MJ-yield should be the central quantitative result.
+5. **Xcimer DOE Milestone Program submission (CX-029047, "IFE Pilot Plant with HYLIFE Concept")**: DOE categorical exclusion document; may contain additional plant specification data supporting Athena design. Search DOE NEPA database — existence inferred from dossier reference; verify before searching.
 
-The two sources most worth acquiring before finalizing Section D2 (quantitative model) are the Thomas et al. 2024 HDD physics paper and the full HYLIFE-II 1994 final report.
+---
+
+## Summary
+Proceed to full D1+ analysis. The Xcimer concept is among the better-documented private fusion concepts at this stage — the 2026 whitepaper's laser cost breakdown and HYLIFE heritage literature together support good coverage of §1 (data availability), §3 (TRL), and §4 (materials). Section §2 (system function challenges) is well served precisely because the gaps (SBS NLO compression at MJ scale, two-beam HDD implosion) constitute the core narrative of the challenges section. The one blocking gap (no integrated CAS-level plant cost study) affects §5 quantitative LCOE precision but is partially bridged by HYLIFE-II BOP heritage and the Hawker IFE LCOE model; LCOE can be estimated as a range with explicit analog assumptions. Ingest the full HYLIFE-II Moir 1994 paper and Thomas et al. 2024 HDD target paper before constructing the quantitative LCOE section.
 
 ---
 
@@ -178,11 +180,11 @@
 
 ```yaml
 overall_rating: "Mostly Ready"
-blocking_count: 3
-important_count: 9
-counting_method: "section-by-section deduplicated: 3 blocking gaps (integrated plant capital cost by CAS, target cost per shot, HDD gain not experimentally validated); 9 important gaps (independent laser cost, SBS/NLO scale demonstration, target injection engineering, chamber dynamics validation, Argos module completion, laser lifetime, FLiBe pump/nozzle, rate target fabrication supply chain, beryllium/Be-avoidance supply chain for Athena)"
+blocking_count: 1
+important_count: 7
+counting_method: "all_sections_deduplicated: §5 BOP capital cost (blocking); §2 SBS NLO MJ-scale + HDD experimental validation + FLiBe hydraulics + power cycle type + target injection (important); §5 O&M cost + target fabrication cost (important)"
 section_coverage:
-  availability_of_data:       "Partial"
+  availability_of_data:       "Good"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
   materials_supply_chain:     "Partial"
```
