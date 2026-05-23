# Diff: 17a-laser-icf-hybrid-drive

**Generated:** 2026-05-22T10:23:35-07:00

## Counts

| field | baseline | new | Δ |
|-------|----------|-----|---|
| blocking_count   | 4 | 3 | -1 |
| important_count  | 8 | 9 | - |
| overall_rating   | Mostly Ready (with important sourcing gaps for quantitative LCOE work) | Mostly Ready | - |

## Fleet-source citations (new only — grep `knowledge/sources/` or `PyFECONS`)

```
23:- Hawker (2020) 14-parameter IFE LCOE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) is directly applicable as a technology-agnostic framework for Xcimer-like parameters.
161:5. **Hawker IFE LCOE model (in-repo source)** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` — directly applicable. Apply Xcimer parameters (gain >200, yield 1–2 GJ, driver efficiency 7%, rep rate 0.5 Hz) to bound LCOE. Hawker's sensitivity analysis shows target cost and gain are the highest-leverage parameters — use to quantify the target-cost uncertainty impact.
```

## Blocking-tier lines (baseline)

```
157:| Net electrical output (MWe, Xcimer plant) | proprietary / not-yet-sourced | blocking | No plant-scale design published; HYLIFE-II 940 MWe analog is at different rep rate and yield |
161:| Capital cost breakdown by subsystem | not-yet-sourced / proprietary | blocking | HYLIFE-II Final Report has heritage BOP costs; laser cost requires ASPEN data. No integrated plant cost estimate published. |
164:| Operating cost (annual) | not-yet-sourced / proprietary | blocking | No source. Analogies from NIF O&M costs and fission BOP costs needed |
165:| Capacity factor / planned availability | not-yet-sourced / proprietary | blocking | No source. Sub-Hz pulsed operation simplifies some constraints but laser maintenance is key unknown |
```

## Blocking-tier lines (new)

```
32:- Integrated plant capital cost (CAS-structured) — `not-yet-sourced` (may emerge from DOE milestone program reporting) — **blocking**
34:- Target cost per shot — `proprietary/truly-unknown` — **blocking** (dominant LCOE parameter per Hawker model)
54:- HDD two-beam symmetry physics: no experimental validation yet (simulations + cited paper not in source set) — `not-yet-sourced` (Thomas et al. 2024, Phys. Plasmas 31, 112708) — **blocking** for gain confidence
138:| Target cost per shot | proprietary/truly-unknown | blocking | Most sensitive IFE LCOE parameter per Hawker model; Xcimer capsule is larger than NIF; no published estimate. GA partner but no data published. |
139:| Integrated plant capital cost by CAS category | not-yet-sourced | blocking | No published full-plant study. Whitepaper is technology document, not a plant TEA. HYLIFE-II analog (different driver) can be adapted. |
140:| HDD target gain (experimentally validated) | truly-unknown | blocking | Capsule gain >200 is a projection from NIF capsule gain scaling; no experimental HDD data at this scale. Phoenix/Anvil/Vulcan milestones gate this. |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_baselines_2026-05-22/17a-laser-icf-hybrid-drive.md	2026-05-22 09:21:13.856656599 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/gap_report.md	2026-05-22 10:23:35.907740864 -0700
@@ -1,213 +1,190 @@
-I have all the source material I need. Let me now write the gap assessment.
+Now I have enough to write a thorough gap assessment. Let me compile it.
 
 ---
 
 # Gap Assessment: Laser ICF - Hybrid Direct Drive (D-T)
 
-**Concept**: Xcimer Energy — KrF excimer laser, HYLIFE-III FLiBe chamber, sub-Hz HDD
-**Note**: Phase 1a dossier (concept 17) covers both Xcimer and Focused Energy combined. This assessment focuses on the Xcimer HDD concept as the primary subject; Focused Energy data is noted separately where it bleeds through.
-
----
-
 ## Overall Readiness
-
-**Rating**: Mostly Ready (with important sourcing gaps for quantitative LCOE work)
-
-**Summary**: Xcimer is unusually transparent for a private fusion company — their website, DOE program filings, and public presentations together provide a coherent physical picture of the concept. The qualitative analysis sections (Availability, System Function, Maturity) can be written to a good standard from current sources. However, the LCOE quantitative model is hampered by three gaps: (1) no extracted full text of the HYLIFE-III 2024 nuclear analysis paper (which likely contains TBR, neutron flux, and chamber engineering numbers), (2) no extracted full text of the HYLIFE-II final report (which contains the BOP cost breakdown and thermal efficiency basis), and (3) no primary-source numbers for net electrical output or capital cost at the Xcimer-scale plant. These gaps are workable with targeted sourcing and well-documented analogues but should not be ignored.
+**Rating**: Mostly Ready
+**Summary**: Xcimer Energy's Feb 2026 commercialization whitepaper is an unusually detailed primary source for a private fusion company, providing laser cost breakdowns by component, a four-phase development roadmap, and the physical basis for the HDD target and HYLIFE-III chamber. The HYLIFE-II heritage literature fills in balance-of-plant and COE baseline data. The main gaps are the absence of a published integrated plant capital cost study (needed for CAS analysis), an unquantified target cost (a dominant IFE LCOE parameter), and unvalidated HDD physics — all three are analyzable with stated assumptions but require explicit caveats.
 
 ---
 
 ## Section Coverage
 
 ### 1. Availability of Data
-
-**Coverage**: Good (qualitative), Partial (quantitative)
+**Coverage**: Moderate
 
 **Available**:
-- Xcimer website (approach + science pages): detailed physics rationale, gain targets, laser architecture, chamber concept, NIF comparison — extracted and readable (`xcimer-energy-approach.md`, `xcimer-science-page.md`)
-- DOE program filing (CX-029047): confirms government-funded IFE pilot plant program with HYLIFE concept — cited in dossier, not extracted
-- Focused Energy interview (`focused-energy-callahan-interview.md`): confirms Focused Energy's steam cycle, 10 Hz rep rate, gain >50 target, lithium blankets — useful for contrast/comparison but is a different concept
-- HYLIFE-II BOP study (OSTI 6137961): extracted as abstract only — confirms FLiBe primary coolant, IHX, steam generators were studied at UC Davis/LLNL. Full text not available.
-- Dossier contains citations to 20 sources including key papers with access notes (paywalled ScienceDirect, paywalled Springer)
-- ASPEN architecture presentation (LLNL IFE Workshop 2022, PDF): cited in dossier, not extractable via web fetch — contains $20-30/J laser cost target
+- Xcimer's 28-page Feb 2026 commercialization whitepaper (`iter-02/sources/xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb`) is the cornerstone source. It covers laser architecture, cost comparison to DPSSL, HDD target physics, chamber design, and a four-phase roadmap. It includes a first-of-kind laser cost breakdown by component ($100–120/J on-target FOAK, $60–80/J NOAK).
+- Xcimer's public website (Approach + Science pages) provides high-level system description and operating parameters (sub-Hz, gigawatt-scale, steam conversion).
+- The 2024 HYLIFE-III nuclear analysis paper (`iter-03/sources/sciencedirect-…s0920379624001868`) provides neutronics for Xcimer's specific chamber: TBR > 1.2 with FLiBe, 30-year first-wall lifetime, tritium inventory < 200 g.
+- HYLIFE-II final report (1994) and 1990 BOP study (`iter-03/sources/osti-servlets-purl-6137961`) provide detailed COE, power balance, and power conversion system data as heritage analogs: 4.5–6.5 ¢/kWh at 1–2 GWe, 41% thermal efficiency, 33% net plant efficiency, 1083 MWe net output for the base case.
+- Hawker (2020) 14-parameter IFE LCOE model (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) is directly applicable as a technology-agnostic framework for Xcimer-like parameters.
+- Betti "Status and prospects for IFE via lasers" (`iter-03/sources/osti-servlets-purl-2561299`) provides IFE power plant energetics requirements and laser efficiency benchmarks.
 
 **Missing**:
-- Full text of HYLIFE-III 2024 (Fusion Eng. Des., S0920379624001868) — contains FLiBe TBR analysis, neutron flux data, first-wall activation. Currently behind ScienceDirect paywall.
-- Full text of HYLIFE-II Final Report 1994 (Fusion Technology) — contains 940 MWe plant design, BOP cost breakdown, thermal efficiency basis
-- Full text of HDD Physics of Plasmas 2024 paper — contains target physics details for Xcimer's specific HDD geometry
-- Full text of Mehlhorn 2024 (Physics of Plasmas) — KrF heritage history, may contain cost/efficiency context
-- Full ASPEN presentation PDF content
+- No published, integrated Xcimer plant study (the whitepaper is a technology/roadmap document, not a full TEA/CAS-structured plant report).
+- No third-party or independent cost analysis of the Xcimer laser architecture.
+- No published target cost estimate for Xcimer's large capsule.
 
 **Gaps**:
-- HYLIFE-III 2024 full text — `not-yet-sourced` — **important** (TBR numbers, neutron shielding thickness needed for LCOE)
-- HYLIFE-II Final Report full text — `not-yet-sourced` — **important** (baseline BOP cost/thermal efficiency for HYLIFE lineage)
-- ASPEN presentation full content — `not-yet-sourced` — **important** (primary source for laser cost target of $20-30/J)
-- HDD Physics of Plasmas 2024 — `not-yet-sourced` — **nice-to-have** (confirms target coupling physics at Xcimer scale)
+- Integrated plant capital cost (CAS-structured) — `not-yet-sourced` (may emerge from DOE milestone program reporting) — **blocking**
+- Independent laser cost verification — `not-yet-sourced` — **important**
+- Target cost per shot — `proprietary/truly-unknown` — **blocking** (dominant LCOE parameter per Hawker model)
 
 ---
 
 ### 2. Challenges in Capturing System Function
-
 **Coverage**: Partial
 
 **Available**:
-- Physics rationale for HDD vs indirect drive: NIF coupling efficiency (12% via hohlraum) vs Xcimer >90% direct coupling (`xcimer-science-page.md`)
-- Wall-plug gain pathway: fuel capsule gain ~10x NIF (=~200), laser efficiency ~10x NIF (KrF vs Nd:glass), coupling efficiency ~7.5x NIF — together achieving ~1000x wall-plug gain improvement (`xcimer-science-page.md`)
-- Rep rate simplification rationale: high yield per shot allows <1 Hz, reduces target fabrication and chamber shock recovery demands (`xcimer-energy-approach.md`)
-- FLiBe liquid-wall self-healing chamber concept: protects structural wall from ions, debris, 14 MeV neutrons; uses flowing jets (`xcimer-energy-approach.md`)
-- KrF laser architecture: Raman beam combining + SBS pulse compression (cited in dossier, not in extracted sources)
-- Safety/activation analysis: low activation structural materials enabled by liquid wall (`xcimer-science-page.md`)
+- The whitepaper explicitly enumerates the three key challenges Xcimer must solve and the risks it accepts: (1) laser performance and cost, (2) first-wall survival, (3) system economics. This provides a structured view of where cost uncertainty concentrates.
+- Physics basis for why HDD enables two-beam illumination with sufficient symmetry is described (ring-intensity beam shaping, large capsule relaxing uniformity requirements). A 2024 paper (Thomas et al., Phys. Plasmas) on the HDD concept with LLE/LANL/GA is cited.
+- The SBS NLO pulse compression scheme is described in detail, including its undemonstrated status at scale — Phoenix (Q2 2026) is the validation milestone.
+- The HYLIFE chamber dynamics have been simulated: <10 kg FLiBe vaporized per shot, vapor vents through jet array, pressure loadings within limits. Two papers (Cervi et al. 2025, 2026) are cited but not extracted.
+- The Optica OPN article (`iter-03/sources/optica-opn-home-articles-volume-34-june-2023-features`) covers the broader direct drive landscape and competing challenges (cross-beam energy transfer, laser-plasma instabilities), noting that two-beam illumination symmetry is the specific challenge Xcimer must resolve.
 
 **Missing**:
-- Target injection system at sub-Hz: how capsules are tracked, injected, positioned at chamber center — no source addresses this
-- Chamber shock recovery: FLiBe jet re-establishment after each fusion pulse — not addressed in extracted sources (HYLIFE-II literature would cover this)
-- KrF laser rep-rate limits: Electra laser at NRL demonstrated 5 Hz (cited in dossier/science page), but 10 MJ KrF at sub-Hz involves different engineering challenges not quantified in available sources
-- Energy cycle details: steam vs. Brayton ambiguity unresolved (science page says steam; HYLIFE heritage says helium Brayton at ~45%). This directly affects thermal efficiency assumptions.
-- FLiBe tritium extraction: vacuum disengager concept cited in OSTI related records but not extracted
-- Chamber vacuum maintenance: how chamber vacuum is maintained between shots — not addressed
+- The Thomas et al. 2024 HDD target paper is cited but not in the source set — this is the key physics validation document.
+- Cervi et al. chamber dynamics papers are cited but not extracted.
+- No published analysis of target injection and tracking system design (Xcimer cites the TRUMPF CO2 laser analogy but gives no engineering specifics).
 
 **Gaps**:
-- Thermal cycle type (steam vs. He Brayton) — `proprietary` (design may have changed from heritage) / `not-yet-sourced` (HYLIFE-III 2024 paper likely resolves this) — **important** (affects thermal efficiency and BOP cost assumptions)
-- Target injection and tracking at sub-Hz — `not-yet-sourced` — **important** (affects rep-rate reliability and capacity factor modeling)
-- FLiBe chamber shot dynamics (jet recovery timing, vacuum recovery) — `not-yet-sourced` — **nice-to-have** (HYLIFE-II literature covers this but text not extracted)
-- KrF 10 MJ system efficiency (actual, vs. claimed ~10%) — `not-yet-sourced` — **important** (fundamental to wall-plug gain and recirculating power)
+- HDD two-beam symmetry physics: no experimental validation yet (simulations + cited paper not in source set) — `not-yet-sourced` (Thomas et al. 2024, Phys. Plasmas 31, 112708) — **blocking** for gain confidence
+- SBS NLO pulse compression at relevant scale: Phoenix milestone Q2 2026, not yet demonstrated — `truly-unknown` until Phoenix results — **important**
+- Target injection and tracking reliability at 0.25–1 Hz: engineering concept described (TRUMPF analogy) but no design data — `proprietary` — **important**
+- Chamber dynamics validation: simulation-only; Cervi 2025/2026 papers not extracted — `not-yet-sourced` — **important**
 
 ---
 
 ### 3. Maturity of Key Subsystems and Components
-
 **Coverage**: Partial
 
 **Available**:
-- KrF excimer laser (driver): Phoenix prototype milestone — first private-sector electron-beam excimer laser completed June 2025 (cited in dossier). NRL Electra laser demonstrated 5 Hz, ~kJ scale (`xcimer-science-page.md`). TRL assessment: ~4-5 for the laser module; full 10 MJ ASPEN architecture is earlier.
-- HDD target physics: NIF ignition demonstrated (indirect drive); direct-drive implosions at OMEGA (cited in dossier). HDD with two-sided UV: Physics of Plasmas 2024 paper exists (cited in dossier, not extracted). TRL: ~3-4 for HDD specifically.
-- FLiBe chamber (HYLIFE): Concept from 1984, developed through HYLIFE-II (1994), HYLIFE-III (2024 nuclear analysis). Heritage is extensive but no flow loop at scale has been built. TRL: ~2-3.
-- Target fabrication: NIF fabricates ~400 targets/year at >$1M each. Xcimer requires larger capsules at much lower frequency (<1 Hz ≈ <1/day vs 400/year for NIF). Mass production pathway not established but simpler than 10 Hz concepts. TRL: ~2.
-- Tritium breeding (FLiBe blanket): FLiBe TBR analysis in HYLIFE-III 2024. Tritium extraction from FLiBe: studied at LLNL (OSTI related records) but not at scale. TRL: ~2-3.
-- Balance of plant: Conventional steam or Brayton cycle — these are mature technologies. TRL for BOP: ~8-9 (heritage from fission/concentrated solar). Interface with FLiBe primary coolant requires IHX development.
+- **KrF excimer laser (Argos module)**: TRL 3–4. NRL Electra (750 J, 2.5 Hz, 10 hours continuous) demonstrated sustained operation. Xcimer LPK online Dec 2024, KJC (approaching 2 kJ) online Dec 2025. Argos (160 kJ target) planned for 2027. Strong heritage: 50 years of e-beam pumped excimer development.
+- **SBS NLO pulse compression**: TRL 2–3. Concept demonstrated at small scale at LLNL/LANL/Imperial in 1970s–80s. Phoenix (Q2 2026) is the first high-energy system-level validation.
+- **FLiBe thick-liquid-wall/HYLIFE chamber**: TRL 3–4 (from HYLIFE-II program). Jet hydraulics tested with water/oil surrogates. Laminar jet formation demonstrated at sub-scale. FLiBe redox control at scale unsolved.
+- **Power conversion (steam cycle)**: TRL 7+. Subcritical steam at 800 K / 16 MPa is mature technology. Main uncertainty is FLiBe–IHX material compatibility (Hastelloy N vs. 316 SS, cost 3× difference per 1990 HYLIFE-II study).
+- **Cryogenic DT target fabrication**: TRL 3–4. General Atomics partnership with NIF-style capsules at small scale. No rate production demonstrated for capsules at Xcimer's larger size.
+- **Tritium breeding and processing**: TRL 4–5. Extensive HYLIFE-II heritage for FLiBe tritium solubility, vacuum disengager concepts. TBR > 1.2 computed for HYLIFE-III.
 
 **Missing**:
-- Quantitative TRL assessments with justification for each subsystem — no published TRL ladder for Xcimer's specific architecture
-- Status of target injection / tritium injection system — not addressed in any extracted source
-- FLiBe loop engineering status (pumps, IHX prototype, tritium extraction) — not in extracted sources
+- No published TRL assessments from Xcimer itself.
+- Target injection and tracking system: no engineering data in sources.
+- Capacitor/Marx generator lifetime at commercial rep rates: unquantified.
 
 **Gaps**:
-- Formal TRL table for Xcimer subsystems — `not-yet-sourced` / `proprietary` — **important** (IFES roadmap reports or DOE program status reports may contain this; `unverified — confirm existence before searching`)
-- Target injection demonstrator status — `proprietary` — **nice-to-have**
-- FLiBe loop engineering prototype status — `not-yet-sourced` — **important** (HYLIFE-III 2024 may address; also search OSTI for HYLIFE FLiBe loop)
+- Target injection/tracking TRL: no published engineering study — `not-yet-sourced` — **important**
+- Argos (160 kJ module) demonstration: planned 2027, not yet completed — `truly-unknown` until Anvil results — **important**
+- Laser system lifetime (capacitor/cathode fatigue at ~0.5 Hz over 30 years): not addressed in whitepaper — `proprietary/not-yet-sourced` — **important**
+- FLiBe pump and nozzle at commercial scale: acknowledged as unsolved by Xcimer — `truly-unknown` — **important**
+- Rate cryogenic target fabrication at Xcimer capsule size: not addressed — `not-yet-sourced` — **important**
 
 ---
 
 ### 4. Key Materials and Supply Chain Considerations
-
 **Coverage**: Partial
 
 **Available**:
-- FLiBe: lithium fluoride + beryllium fluoride molten salt. Used as both primary coolant and tritium breeder. Li-6 enrichment required for breeding (natural Li is ~7.5% Li-6). FLiBe is well-characterized in molten salt reactor literature. Beryllium is a controlled material with limited production base. (`xcimer-energy-approach.md`, `xcimer-science-page.md` — implicitly)
-- Structural materials: Xcimer claims commercial/readily available structural materials enabled by liquid first wall (`xcimer-science-page.md`). No specifics given.
-- KrF gas: krypton (from air separation, limited but industrial-scale supply) + fluorine handling — industrial chemistry
-- D-T fuel: deuterium from seawater (abundant); tritium from Li-6 breeding (covered by FLiBe blanket). Startup tritium inventory supply chain not addressed.
-- Target capsule materials: presumably plastic/CH ablator + cryogenic D-T ice + foam layers. Xcimer targets are larger than NIF (to achieve 10x capsule gain) — mass production of precision cryogenic spheres at scale not demonstrated.
+- **FLiBe vs. FLiNaK**: Whitepaper discusses the beryllium-avoidance pathway (FLiNaK at TBR ~1.05 with large capsules for commercial plants; FLiBe at TBR ~1.2 for Athena pilot). No lithium-6 enrichment required (natural Li). This is a meaningful supply chain advantage over some IFE concepts.
+- **Beryllium**: The FLiNaK option removes BeF₂ from commercial plants, but Athena pilot requires FLiBe. Beryllium is a controlled material with limited producers (Materion primarily in the US). The whitepaper is aware of this and has a mitigation path.
+- **KrF laser gas**: Noble gas (Kr) + trace F₂/HF. Kr has industrial supply (air separation); F₂ handling is mature in semiconductor industry. No obvious supply bottleneck.
+- **High-voltage capacitors**: Xcimer is manufacturing in-house in Tucson AZ. Volume costs projected at $0.40–$0.85/J (stored energy). Supply chain risk mitigated by vertical integration.
+- **Structural materials (Hastelloy N / 316 SS)**: Material compatibility with FLiBe is the main question. Cost 3× premium for Hastelloy N vs. SS (from 1990 HYLIFE-II BOP study). This affects IHX, chamber, piping, tritium removal equipment costs.
+- **DT target ablator (polystyrene/plastic)**: Standard material; no supply concern.
 
 **Missing**:
-- Beryllium supply chain: BeF₂ in FLiBe requires significant beryllium. Global beryllium production is dominated by one major US producer (Materion). No source quantifies FLiBe inventory requirements for a Xcimer-scale plant.
-- Li-6 enrichment: enrichment capacity is limited globally (DOE stopped enrichment; commercial enrichment capacity is small). Needed fraction for adequate TBR not specified in available sources.
-- Startup tritium inventory: initial tritium needed before breeding comes online. Not addressed in any extracted source.
-- Excimer gas (KrF): fluorine handling at MJ scale, krypton inventory and consumption rate — not addressed.
-- Chamber structural materials specification (type, quantity) — not in extracted sources.
+- No published supply chain analysis for Xcimer's specific capsule (larger than NIF; different ablator layering).
+- No analysis of cryogenic DT target manufacturing yield or cost at commercial rate.
 
 **Gaps**:
-- Beryllium supply chain assessment for FLiBe inventory — `not-yet-sourced` — **important** (HYLIFE-II literature likely addresses this; search OSTI for HYLIFE beryllium)
-- Li-6 enrichment requirement and global capacity — `not-yet-sourced` — **important** (relevant to schedule and cost risk; general fusion literature covers this)
-- Startup tritium inventory — `not-yet-sourced` — **important** (generic to all D-T IFE; existing fusion economics literature covers this)
-- Cryogenic target fabrication at scale — `not-yet-sourced` / `proprietary` — **important** (IFE target factory studies exist in DOE literature; search OSTI for "IFE target factory")
+- Beryllium supply for Athena pilot plant FLiBe: limited producers, not analyzed — `not-yet-sourced` — **important**
+- Rate target fabrication supply chain (General Atomics partnership, but no published data) — `proprietary` — **important**
+- Hastelloy N vs. SS selection final decision and cost impact — `proprietary/not-yet-sourced` — **nice-to-have** (can use HYLIFE-II range as bounds)
+- Kr gas demand at commercial scale: derivable from laser specifications but not analyzed — `derivable` — **nice-to-have**
 
 ---
 
 ### 5. LCOE Parameter Extraction
+**Coverage**: Partial
 
 **Available Parameters**:
 
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Laser type | KrF excimer, 248 nm | xcimer-energy-approach.md | high |
-| Laser energy per pulse | ~10+ MJ | xcimer-energy-approach.md, xcimer-science-page.md | high |
-| Rep rate | <1 Hz | xcimer-energy-approach.md | high |
-| Fuel | D-T | dossier | high |
-| Wall-plug gain required (commercial) | ~10 | xcimer-science-page.md | high |
-| Fuel capsule gain target | ~200 (10× NIF's ~20) | xcimer-science-page.md (derived) | medium |
-| Laser-to-capsule coupling efficiency | >90% (vs NIF 12%) | xcimer-science-page.md | medium |
-| Laser cost target (on-target) | ~$20–30/J | dossier (from ASPEN PDF, unextracted) | medium |
-| Laser cost reduction vs NIF | >30× per joule | xcimer-energy-approach.md | medium (claimed) |
-| Final optical area | <1 m² | xcimer-energy-approach.md | high |
-| Energy conversion pathway | Thermal → steam (claimed) | xcimer-science-page.md | medium (ambiguous vs Brayton) |
-| Primary coolant | FLiBe (molten salt) | xcimer-energy-approach.md | high |
-| Tritium breeding material | FLiBe blanket | xcimer-energy-approach.md, dossier | high |
-| First-wall concept | Liquid FLiBe wet wall, lifetime | xcimer-energy-approach.md | high |
-| Chamber lifetime claim | 30 years without first-wall replacement | dossier (HYLIFE-III 2024, not extracted) | medium |
-| Heritage reference plant output | 940 MWe at 6 Hz (HYLIFE-II, 1994) | dossier (HYLIFE-II Final Report, not extracted) | high (analog, different rep rate) |
-| Heritage BOP | FLiBe → IHX → steam generators | hylife-energy-conversion-notes.md (abstract only) | medium |
-| NIF total cost (reference) | $3.5B for 2 MJ, 192 beams | xcimer-science-page.md | high |
-| NIF annual optics cost (reference) | ~$40M/yr at current low rep-rate | xcimer-science-page.md | high |
+| Laser energy on target | 8–12 MJ (commercial); 8 MJ (Athena) | Xcimer whitepaper | h |
+| Laser cost FOAK | $100–120/J on-target | Xcimer whitepaper (self-reported) | m |
+| Laser cost NOAK | $60–80/J on-target | Xcimer whitepaper (self-reported) | m |
+| Laser wall-plug efficiency | 5–7% (target) | Xcimer whitepaper | m |
+| Target gain (target) | >200 (at 10 MJ absorbed, capsule gain scaling) | Xcimer whitepaper | l |
+| Repetition rate | 0.25–1 Hz | Xcimer whitepaper, dossier | h |
+| Net electrical output (Athena) | ~400 MWe | Xcimer whitepaper | m |
+| Net electrical output (commercial) | hundreds of MWe to >1 GWe | Xcimer whitepaper | l |
+| Recirculating power fraction | 11–13% (NOAK, Qsci 250, η=7%) | Xcimer whitepaper | m |
+| Thermal efficiency (analog) | ~41% thermal, ~33% net (HYLIFE-II heritage) | `iter-03/sources/osti-servlets-purl-6137961` | m |
+| Steam cycle parameters (analog) | 800 K, 16 MPa subcritical regenerative | `iter-03/sources/osti-servlets-purl-6137961` | m |
+| HYLIFE-II COE (different driver) | 4.5–6.5 ¢/kWh at 1–2 GWe | `iter-03/sources/osti-biblio-7021072` | m |
+| Availability (HYLIFE-II analog) | 75% (conservative), 85% (optimistic) | `iter-03/sources/osti-biblio-7021072` | m |
+| TBR (HYLIFE-III, FLiBe) | >1.2 | `iter-03/sources/sciencedirect-…` | h |
+| Tritium inventory | <200 g (commercial), <150 g (Athena) | Xcimer whitepaper | m |
+| DPSSL cost floor (comparison) | $700–1,000/J (DPSSL lower bound) | Xcimer whitepaper, SPIE 2026 | h |
+| IHX cost (analog, 1988$) | $18–55/kWth (SS vs. Hastelloy N) | `iter-03/sources/osti-servlets-purl-6137961` | l |
 
 **Missing Parameters**:
 
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| Net electrical output (MWe, Xcimer plant) | proprietary / not-yet-sourced | blocking | No plant-scale design published; HYLIFE-II 940 MWe analog is at different rep rate and yield |
-| Fusion yield per shot (MJ) | derivable | important | Can be estimated: ~10 MJ laser × 10 wall-plug gain × laser efficiency = ~100 MJ fusion; needs stated assumptions |
-| Thermal efficiency (%) | not-yet-sourced | important | Steam: ~33%; He Brayton: ~45%. Ambiguity directly affects LCOE. HYLIFE-III 2024 or HYLIFE-II Final Report would resolve |
-| Recirculating power fraction | derivable | important | Dominated by laser (wall-plug gain ~10 means 10% recirculation from laser alone) |
-| Capital cost breakdown by subsystem | not-yet-sourced / proprietary | blocking | HYLIFE-II Final Report has heritage BOP costs; laser cost requires ASPEN data. No integrated plant cost estimate published. |
-| Target fabrication cost ($/target) | not-yet-sourced / proprietary | important | IFE target factory studies exist in DOE literature (Goodin et al.); search OSTI for "IFE direct drive target factory cost" — `unverified — confirm existence before searching` |
-| FLiBe inventory cost | not-yet-sourced | important | HYLIFE-II BOP study covers this; BeF₂ is expensive (~$900/kg Be metal equivalent) |
-| Operating cost (annual) | not-yet-sourced / proprietary | blocking | No source. Analogies from NIF O&M costs and fission BOP costs needed |
-| Capacity factor / planned availability | not-yet-sourced / proprietary | blocking | No source. Sub-Hz pulsed operation simplifies some constraints but laser maintenance is key unknown |
-| TBR (numerical) | not-yet-sourced | important | HYLIFE-III 2024 contains this; paper not extracted |
-| KrF wall-plug efficiency (current demonstrated) | not-yet-sourced | important | NRL Electra demonstrated ~2-5% wall-plug efficiency. 10% is target. HAPL program reports exist on OSTI. |
-| Target gain vs laser energy (gain curve) | not-yet-sourced | important | Physics of Plasmas 2024 HDD paper likely contains this. Needed for sensitivity analysis. |
+| Target cost per shot | proprietary/truly-unknown | blocking | Most sensitive IFE LCOE parameter per Hawker model; Xcimer capsule is larger than NIF; no published estimate. GA partner but no data published. |
+| Integrated plant capital cost by CAS category | not-yet-sourced | blocking | No published full-plant study. Whitepaper is technology document, not a plant TEA. HYLIFE-II analog (different driver) can be adapted. |
+| HDD target gain (experimentally validated) | truly-unknown | blocking | Capsule gain >200 is a projection from NIF capsule gain scaling; no experimental HDD data at this scale. Phoenix/Anvil/Vulcan milestones gate this. |
+| Power conversion cycle type (commercial) | derivable | important | Whitepaper says "generating steam" for Athena; HYLIFE-II steam cycle at 41% thermal / 33% net is the best analog. Commercial plant may use sCO2 or He Brayton for higher efficiency — not addressed. |
+| O&M costs (Xcimer-specific) | derivable | important | Can use HYLIFE-II 6% of direct cost; Xcimer claims liquid wall reduces O&M vs. dry-wall, but no published number. |
+| Laser system lifetime / replacement schedule | not-yet-sourced | important | Capacitor and cathode lifetime at 0.25–1 Hz commercial rate not characterized. Electra (750 J) operated for hours; commercial system needs years. |
+| Capacity factor | derivable | important | HYLIFE-II used 75% (conservative); Xcimer claims longer lifetime and simpler maintenance. No published CF projection for HYLIFE-III. Can assume 75–85% with HYLIFE-II precedent. |
+| Cryogenic target fabrication cost at rate | proprietary/not-yet-sourced | important | Hawker model shows target cost is highly sensitive. NIF target costs ($10,000–100,000 each) are 5–6 orders of magnitude above what IFE needs. GA partnership implied but unquantified. |
+| FLiBe system cost (pumps, heat exchangers, piping) | derivable | important | HYLIFE-II BOP study is the best analog (1990 dollars); needs inflation adjustment and adjustment for Xcimer's sub-Hz lower yield-per-second throughput. |
+| Driver-specific capital cost breakdown (HYLIFE-III vs. HYLIFE-II) | not-yet-sourced | important | HYLIFE-II had $570M HI driver at 5 MJ; Xcimer laser at $100–120/J × 10 MJ = $1–1.2B FOAK. Adjustment derivable but not independently verified. |
 
 ---
 
 ## Source Recommendations
 
-1. **HYLIFE-III 2024 nuclear analysis paper** (Fusion Eng. Des., S0920379624001868) — `not-yet-sourced` — Resolves: TBR, neutron flux, first-wall activation, chamber dimensions, and possibly thermal cycle clarification. Access via ScienceDirect institutional login or interlibrary loan. Already in dossier citations — **high priority**.
+1. **Thomas et al. 2024, Phys. Plasmas 31, 112708** — "Hybrid direct drive with a two-sided ultraviolet laser" — cited in Xcimer whitepaper but not extracted. Contains the key HDD physics modeling and symmetry analysis. Search OSTI or AIP for PDF. *not-yet-sourced — confirm existence via DOI 10.1063/5.0228074*
 
-2. **HYLIFE-II Final Report 1994** (Fusion Technology 15:25–70) — `not-yet-sourced` — Resolves: 940 MWe plant parameters, BOP cost breakdown (including FLiBe costs), thermal cycle efficiency, chamber engineering. Tandfonline paywall or possibly available via OSTI. Already in dossier citations — **high priority**.
+2. **Cervi et al. 2025 and 2026, International Journal of Heat and Mass Transfer** — cited for chamber dynamics simulations (FLiBe vaporization, vapor venting). Search ScienceDirect for titles given in whitepaper footnotes 51–52. *not-yet-sourced — confirm via journal search*
 
-3. **ASPEN architecture presentation PDF** (Galloway, LLNL IFE Workshop 2022) — `not-yet-sourced` — Resolves: $20-30/J laser cost target (currently unverified in extracted text), ASPEN architecture specifics. URL in dossier: `lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf`. Not extractable via web fetch due to PDF format — needs direct download.
+3. **General Atomics target fabrication papers** — GA is Xcimer's partner for capsule fabrication. Search OSTI or conference proceedings (IFSA, ANS Fusion) for GA NIF-style or large-capsule target cost/rate manufacturing analysis. Search strategy: "General Atomics ICF target cost manufacturing 2023 2024 2025." *unverified — confirm existence before searching*
 
-4. **NRL Electra / HAPL program KrF efficiency reports** — `not-yet-sourced` — Resolves: current demonstrated KrF wall-plug efficiency baseline. Search OSTI for "Electra KrF laser efficiency HAPL" or "high average power laser program efficiency" — `unverified — confirm existence before searching`.
+4. **LLNL GEM or IPM tool output** — LLNL released GEM (Generalized Economics Model) for IFE in early 2026 (`iter-03/sources/llnl-53961`). GEM is designed for DPSSL indirect-drive/dry-wall, so it is not directly applicable to Xcimer's KrF/liquid-wall concept. However, LLNL's IPM (Integrated Process Model, available for license) may have adaptable BOP and COE structure. Check whether GEM's balance-of-plant assumptions can be reused for steam-cycle parameters. *note: GEM Excel spreadsheet is publicly downloadable from LLNL LIFT*
 
-5. **IFE target factory cost studies** (e.g., Goodin/GA studies from HAPL era) — `not-yet-sourced` — Resolves: target fabrication cost per shot for direct-drive IFE. Search OSTI for "IFE target factory cost direct drive" — `unverified — confirm existence before searching`. These were produced during the HAPL program (~2000–2009) and may be publicly available.
+5. **Hawker IFE LCOE model (in-repo source)** — `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` — directly applicable. Apply Xcimer parameters (gain >200, yield 1–2 GJ, driver efficiency 7%, rep rate 0.5 Hz) to bound LCOE. Hawker's sensitivity analysis shows target cost and gain are the highest-leverage parameters — use to quantify the target-cost uncertainty impact.
 
-6. **Focused Energy J. Fusion Energy 2023** (Springer) — `not-yet-sourced` — Resolves: Focused Energy blanket and chamber details (relevant only if analysis includes Focused Energy as a comparison). Lower priority if focusing on Xcimer HDD exclusively.
+6. **HYLIFE-II design reports beyond currently extracted summaries** — The full Moir et al. 1994 Fusion Technology paper is only available as an OSTI abstract in the source set (`iter-03/sources/osti-biblio-7021072`). The full paper contains cost tables by account. Search OSTI ID 7021072 for full-text. *not-yet-sourced — full paper PDF likely available via OSTI*
 
-7. **DOE CX-029047 documentation** — `not-yet-sourced` — Resolves: any program-level parameters filed with DOE NEPA. URL in dossier: `energy.gov/nepa/articles/cx-029047-ife-pilot-plant-low-cost-high-energy-excimer-driver-and-hylife-concept`. The dossier has the link; the page may have program description text worth extracting.
+7. **Xcimer DOE Milestone Program reports (DOE CX-029047)** — Xcimer holds a DOE funding award (OCED) under the IFE Pilot Plant milestone program. DOE publishes milestone progress reports that may include plant parameters and performance targets not in the public whitepaper. Search DOE OCED IFE milestone program for Xcimer progress updates. *unverified — confirm existence before searching*
 
 ---
 
 ## Summary
 
-**Proceed to full analysis, with targeted sourcing for 3 key documents before quantitative modeling.**
-
-The qualitative sections (Availability, Challenges, Maturity, Materials) can be written now to a good D1 standard using current sources. Xcimer's public communications provide a consistent and detailed physical picture that supports coherent narrative analysis.
+Proceed to full analysis. The Xcimer whitepaper provides sufficient material for a solid qualitative writeup and a first-pass quantitative LCOE estimate using: Xcimer's laser cost breakdown ($100–120/J FOAK), the HYLIFE-II heritage BOP (33% net efficiency, 75% availability, steam cycle), the Hawker 14-parameter IFE model applied with Xcimer's physics targets (gain >200, rep rate 0.5 Hz, driver efficiency 7%), and HYLIFE-II COE analogs. The analysis should explicitly flag three major caveats: (1) target gain >200 is a projection from NIF scaling, not demonstrated experimentally in HDD geometry; (2) laser cost estimates are self-reported by Xcimer and independent verification does not exist in the source set; (3) target cost is unquantified and is the dominant uncertainty in IFE LCOE per Hawker — a sensitivity sweep over target cost from $0.01 to $10/MJ-yield should be the central quantitative result.
 
-The quantitative LCOE model faces blocking gaps in two areas: (a) net plant output and capital cost — currently only addressable via HYLIFE-II heritage analogs, which requires the HYLIFE-II Final Report full text; and (b) thermal efficiency — unresolved steam vs. Brayton ambiguity that directly multiplies into LCOE. Before building the model, retrieving the HYLIFE-III 2024 paper and the HYLIFE-II Final Report would substantially reduce the assumptions that must be stated and defended. The ASPEN PDF is also worth acquiring since the $20-30/J laser cost target is the single most important driver in the capital cost and is currently unverified in extracted text.
+The two sources most worth acquiring before finalizing Section D2 (quantitative model) are the Thomas et al. 2024 HDD physics paper and the full HYLIFE-II 1994 final report.
 
-The back-solve to $0.01/kWh can be performed with current data using stated assumptions, and it will be genuinely informative — the binding constraints (laser cost, target gain, thermal efficiency, capacity factor) are all identifiable from existing sources. The analysis should be explicit that LCOE central estimates are provisional pending these three documents.
+---
 
 ## Structured summary (machine-readable)
 
 ```yaml
-overall_rating: "Mostly Ready (with important sourcing gaps for quantitative LCOE work)"
-blocking_count: 4
-important_count: 8
-counting_method: "section_5_missing_parameters"
+overall_rating: "Mostly Ready"
+blocking_count: 3
+important_count: 9
+counting_method: "section-by-section deduplicated: 3 blocking gaps (integrated plant capital cost by CAS, target cost per shot, HDD gain not experimentally validated); 9 important gaps (independent laser cost, SBS/NLO scale demonstration, target injection engineering, chamber dynamics validation, Argos module completion, laser lifetime, FLiBe pump/nozzle, rate target fabrication supply chain, beryllium/Be-avoidance supply chain for Athena)"
 section_coverage:
-  availability_of_data:       "Good (qualitative), Partial (quantitative)"
+  availability_of_data:       "Partial"
   system_function:            "Partial"
   subsystem_maturity:         "Partial"
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
