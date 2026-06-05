# Design Point Reasoning Trace — 33-state-backed-tokamak-best

## 1. Sources walked

- `knowledge/concept_research/33-state-backed-tokamak-best/dossier.md` — concept summary; identifies BEST (Burning Plasma Experimental Superconducting Tokamak) as the device anchoring the concept and CFEDR/PFPP as the downstream Chinese program lineage; confirms BEST has no electrical output and CFEDR has no published MWe figure
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-01/sources/best-research-plan-v1.1-summary.md` — EUROfusion/ASIPP BEST Research Plan v1.1 (Nov 2025); defines BEST as an experimental burning-plasma facility (R0=3.6 m, B0=6.15 T, Pfus up to 200 MW, Q~5 target), positions CFEDR as the next-step demonstration reactor (Pfus = 1.5–3.0 GW per Table 1.1) and PFPP as the eventual prototype power plant; explicitly states CFEDR's mission is "net electrical power generation" but never quotes an MWe number
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-01/sources/neo-fusion-company-profile.md` — Neo Fusion (Fusion Energy Technology Co. / 聚变新能) company profile; confirms ownership (CNPC, CAS), funding history, and ASIPP relationship; no commercial design specs
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/arxiv-1907-11919.md` — Liu et al., integrated-modeling study of CFETR Phase I (R0=6.6 m, a=1.8 m, B0=6 T, Ip=7.6 MA, Pfus=171 MW, Qfus=3.2) and Phase II (Ip=11 MA, Pfus=1083.5 MW, Qfus=23.5) baseline and high-performance scenarios; reports fusion power and gain but no net electric figure
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-pages-servlets-purl-1465662.md` — Liu et al., time-dependent CFETR baseline scenario; targets Pfus up to 200 MW for Phase I FNSF mission; no MWe
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md` — Kessel et al., ARIES-ACT (Advanced and Conservative Tokamak) power plant study; four design points (ACT1, ACT2, ACT3, ACT4) all explicitly designed to **1000 MW net electric power**, with full engineering basis including geometry (ACT1: R=6.25 m, B=6.0 T, Ip=11 MA, SiC SCLL blanket, η_th=58%; ACT2: R=9.75 m, B=8.75 T, Ip=14 MA, RAFM DCLL, η_th=45%), Q_engr, blanket, divertor, safety analysis, and tritium breeding. State-backed (US DOE national labs: PPPL, UCSD, INL, LLNL, ORNL, U. Wisconsin) tokamak commercial-plant design
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1305833.md` — Meier 2014 LLNL report on tritium breeding blanket system engineering for a generic commercial fusion power plant; no design-point Pnet
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/cfetr-power-conversion-studies.md` — sCO2 Brayton PCS studies for CFETR and EU-DEMO; reports cycle efficiencies (water-Rankine 26.4%, He-Brayton+ORC 23.7%, sCO2 34.7%, with literature ranges 42.8–53.7%); no plant-level MWe for any specific Chinese reactor
- `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/scientific-publications-wp-content-uploads-extrapolating.md` — Foster et al. (UKAEA STEP) parametric LCOE-vs-Pnet scan for spherical tokamaks; not a tokamak commercial-plant design point — used only to confirm that no other state-backed tokamak design with a stated Pnet appears in this concept's corpus

## 2. Candidates surfaced

**BEST (ASIPP / Neo Fusion, under construction at Hefei)**
Mid-size superconducting tokamak, R0=3.6 m, B0=6.15 T, Ip up to 7 MA, Pfus up to 200 MW, Q≥1 target by 2030 and Q~5 burning-plasma studies 2032–2035. LTS+HTS hybrid magnets, 50 MW multi-method H&CD, 110 g tritium inventory, full-W PFCs. Pilot-demonstrator scale but **experimental device with no power conversion system and no design electrical output** — directly analogous to SPARC. P_native: none. Disqualifies as design point per the selection rule.

**CFEDR — China Fusion Engineering Demonstration Reactor (ASIPP roadmap, next-step after BEST)**
Pfus = 1.5–3.0 GW (BEST Research Plan v1.1 Table 1.1), Q = 10–30 target, mission includes "net electrical power generation" and tritium self-sufficiency. **No published net electric power figure, no published geometry, no engineering parameter set.** The named successor in China's roadmap but currently a mission statement, not a design. P_native: unknown (no figure of any kind published). Cannot be adopted as design point.

**PFPP — Prototype Fusion Power Plant (Chinese roadmap, post-CFEDR)**
Named only as the eventual commercial step after CFEDR. No specifications of any kind published. P_native: unknown. Cannot be adopted.

**CFETR Phase I baseline scenario (Liu et al. arXiv:1907.11919)**
Integrated-modeling design point for CFETR, an earlier-generation Chinese ITER–DEMO bridge reactor (predecessor to CFEDR). R0=6.6 m, a=1.8 m, B0=6 T, Ip=7.6 MA, Pfus=171 MW with 33.6 MW NBI + 20 MW ECH, Qfus=3.2, f_bs=64%. Steady-state, fully non-inductive baseline. **Fusion power only; no published net electric output.** P_native: unknown (no MWe reported). Maturity tier: paper-concept.

**CFETR Phase II high-performance scenario (Liu et al. arXiv:1907.11919)**
Same machine as Phase I (no hardware upgrade required), driven harder: Ip=11 MA, Pfus=1083.5 MW, Qfus=23.5, f_bs=89%, alpha-dominated self-heating. **Fusion power only; no published net electric output.** P_native: unknown. Maturity tier: paper-concept (high-performance operating scenario).

**ARIES-ACT1 — Advanced Physics / Advanced Technology (Kessel et al., Fusion Sci. Tech. 67 (2015))**
State-backed (US DOE: PPPL / UCSD / INL / LLNL / ORNL / U. Wisconsin / KIT) conceptual tokamak power plant; advanced-physics, advanced-technology corner of the ARIES-ACT four-corners study. **Designed explicitly to 1000 MW net electric power**, with R=6.25 m, Ip=11 MA, B0=6.0 T, β_N=5.75, H98=1.65, SiC composite structure SCLL blanket at η_th=58%, He-cooled W-alloy divertor, Q_engr=6.6, full self-consistent core-edge-divertor analysis, complete 3-D engineering CAD model, neutronics with TBR=1.05, full safety analysis (LTSBO/LOFA/LOCA). The most-complete published state-backed tokamak commercial-plant design in this corpus. Maturity tier: paper-concept. P_native = 1000 MWe.

**ARIES-ACT2 — Conservative Physics / Advanced Technology (same study)**
Same 1000 MWe target, conservative-physics corner. R=9.75 m, Ip=14 MA, B0=8.75 T, β_N<2.60, H98=1.25, RAFM steel DCLL blanket at η_th=45%, Q_engr=3.1. Larger and lower-efficiency than ACT1; designed to the same net electric output but illustrates the sensitivity of plant size to physics assumptions. P_native = 1000 MWe. Maturity tier: paper-concept.

**ARIES-ACT3 and ARIES-ACT4 (same study, advanced-physics/conservative-tech and conservative-physics/conservative-tech corners)**
Mentioned in the four-corners study framework with the same 1000 MWe target; ARIES-ACT4 parameters partially tabled, ARIES-ACT3 sparsely reported. Both treated by the paper as scoping corners rather than primary engineering design points. P_native = 1000 MWe. Maturity tier: paper-concept.

**EU-DEMO, JA-DEMO, K-DEMO**
Referenced as international peer DEMO programs in arxiv-1907-11919 and cfetr-power-conversion-studies. Discussed only by name and program affiliation in this concept's corpus; no DEMO-specific Pnet, geometry, or engineering parameters extracted in any source file walked. Cannot serve as the design point for this concept without dedicated source ingestion.

## 3. Selection

**ARIES-ACT1** is selected as the design point at **P_native = 1000 MWe**.

Among the state-backed tokamak candidates in this concept's corpus, ARIES-ACT1 is the only one with a published net electric power figure attached to a fully specified engineering design point. The Chinese roadmap that anchors this concept's identity (BEST → CFEDR → PFPP) has no published MWe at any maturity tier: BEST is an experimental device with no power conversion system; CFEDR's published mission includes net electric power but no figure has been quoted in the source corpus; CFETR Phase I and Phase II report fusion power and gain but stop short of a net-electric design point; PFPP is named only. ARIES-ACT1, by contrast, is designed to 1000 MWe with detailed geometry (R=6.25 m, B0=6.0 T, Ip=11 MA), full thermal cycle (SiC SCLL blanket at 58% efficiency), DT fuel, complete 3-D engineering analysis, and Q_engr=6.6 — exactly the kind of "best published" state-backed tokamak the selection rule asks for. ACT1 beat ACT2/3/4 because it is the four-corners study's headline advanced-physics, advanced-technology design with the most-elaborated engineering analysis and the highest engineering Q; ACT2 (the conservative-physics counterpart at the same 1000 MWe) is the natural sensitivity case.

The concept's nominal identity is Chinese (BEST / Neo Fusion / ASIPP), but the published-data anchor in the corpus is American (ARIES-ACT). This mismatch is acceptable under the selection rule (ARIES-ACT is itself a state-backed tokamak with the best published quantitative data in this concept's portfolio) and is called out as the dominant open question — if CFEDR or a future ASIPP-program plant publishes engineering parameters with a stated MWe, the design point should be revisited.

```yaml
proposal:
  concept_id: 33-state-backed-tokamak-best
  design_name: "ARIES-ACT1 advanced-physics / advanced-technology design (Kessel et al., Fusion Sci. Tech. 67 (2015))"
  maturity_tier: paper-concept
  grounding_confidence: high
  p_native_mwe: 1000
  primary_sources:
    - knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md
    - knowledge/concept_research/33-state-backed-tokamak-best/iter-01/sources/best-research-plan-v1.1-summary.md
  selection_rationale: |
    ARIES-ACT1 is the only design in this concept's corpus with a published net electric
    power figure (1000 MWe) attached to a fully specified engineering design point —
    geometry (R=6.25 m, B0=6.0 T, Ip=11 MA), SiC SCLL blanket at 58% thermal efficiency,
    He-cooled W-alloy divertor, Q_engr=6.6, complete 3-D engineering CAD model,
    neutronics with TBR=1.05, and full safety analysis. The Chinese roadmap that anchors
    this concept's nominal identity (BEST -> CFEDR -> PFPP per BEST Research Plan v1.1)
    has no published MWe at any maturity tier: BEST is experimental, CFEDR's mission
    statement cites "net electrical power generation" without a figure, and PFPP is
    named only. Among the four ARIES-ACT corners (all targeting 1000 MWe), ACT1 is the
    headline advanced-physics / advanced-technology design point with the most-elaborated
    engineering analysis and highest engineering Q. ARIES-ACT is a US national-lab
    state-backed conceptual tokamak power plant and therefore fits the
    state-backed-tokamak archetype.
  alternatives_considered:
    - design: "ARIES-ACT2 conservative-physics / advanced-technology design (Kessel et al.)"
      reason_rejected: same 1000 MWe target but larger and lower-efficiency than ACT1; the four-corners study's conservative-physics counterpart, not the headline design
      sensitivity_implication: >
        If picked instead, P_native is unchanged (still 1000 MWe by construction) but
        device size and capital intensity rise substantially (R=9.75 m vs 6.25 m,
        B0=8.75 T vs 6.0 T, eta_th=45% vs 58%, Q_engr=3.1 vs 6.6) -> per-module
        reactor-island cost and recirculating power rise -> 1 GWe LCOE shifts up
        materially. Worth probing whenever the physics-assumption sensitivity is in
        question (beta_N, H98 attainment).
    - design: "ARIES-ACT3 and ARIES-ACT4 corner designs (Kessel et al.)"
      reason_rejected: scoping corners of the same four-corners study rather than primary engineering design points; sparser published parameter set
      sensitivity_implication: >
        If picked instead, P_native unchanged (1000 MWe) but device size and recirculating
        power shift between the ACT1 and ACT2 envelopes depending on which physics/tech
        corner is chosen -> 1 GWe LCOE shifts in the same direction as ACT2 but to a
        lesser degree. Worth probing if the cost analysis wants to bound the four-corners
        physics-vs-technology trade.
    - design: "CFEDR (China Fusion Engineering Demonstration Reactor)"
      reason_rejected: no published net electric power, no published geometry, no engineering parameters - mission statement only
      sensitivity_implication: >
        If CFEDR publishes a design point with a stated MWe, that becomes the natural
        design point for this Chinese-program-anchored concept. Direction unknown until
        the figure is published; CFEDR's Pfus = 1.5-3.0 GW range suggests P_native could
        land anywhere from ~500 MWe (low-efficiency) to >1 GWe (sCO2 Brayton at 40%) -
        the 1 GWe LCOE direction depends entirely on where it lands. This is the primary
        watch item for design-point revision.
    - design: "CFETR Phase I baseline scenario (Liu et al. arXiv:1907.11919)"
      reason_rejected: fusion-power design point only; no published net electric output
      sensitivity_implication: >
        If a published net electric figure for CFETR Phase I emerges (Pfus=171 MW x ~40%
        sCO2 efficiency would imply ~70 MWe gross, lower net), P_native would be much
        lower than ARIES-ACT1 -> many more modules at 1 GWe -> 1 GWe LCOE shifts up
        substantially. Worth probing if the cost analysis is scoped to a CFETR-class
        bridge facility rather than a commercial plant.
    - design: "CFETR Phase II high-performance scenario (Liu et al. arXiv:1907.11919)"
      reason_rejected: fusion-power design point only; no published net electric output (Pfus=1083.5 MW is fusion power, not electric)
      sensitivity_implication: >
        If a published net electric figure for CFETR Phase II emerges (Pfus=1083.5 MW x
        ~40% sCO2 ~= 430 MWe gross before recirculating losses), P_native would be lower
        than ARIES-ACT1 -> more modules at 1 GWe -> 1 GWe LCOE shifts up. Worth probing
        once a Chinese-roadmap plant publishes a full electric design point.
    - design: "BEST (Burning Plasma Experimental Superconducting Tokamak, ASIPP)"
      reason_rejected: no electrical output by design; experimental burning-plasma facility analogous to SPARC
      sensitivity_implication: "n/a - BEST has no P_native and cannot be used as a design point."
    - design: "PFPP (Prototype Fusion Power Plant, China)"
      reason_rejected: named only in the BEST Research Plan as the eventual commercial step after CFEDR; no specifications published
      sensitivity_implication: >
        If PFPP publishes a commercial design point with a stated MWe, that would be the
        natural design point for this concept and would supersede ARIES-ACT1. Direction
        unknown until specifications are published.
    - design: "EU-DEMO, JA-DEMO, K-DEMO (peer state-backed DEMO programs)"
      reason_rejected: referenced as peer state-backed DEMO programs but no DEMO-specific Pnet or engineering parameters extracted in this concept's corpus
      sensitivity_implication: >
        If a dedicated EU-DEMO or JA-DEMO source is ingested, those programs publish
        targets in the ~300-500 MWe range (well below ARIES-ACT1's 1000 MWe) -> many
        more modules at 1 GWe -> 1 GWe LCOE shifts up. Worth probing as a parallel
        state-backed-tokamak sensitivity. Currently out of scope of the source corpus.
```

## 4. Open questions

- **CFEDR engineering basis with a stated MWe**: The BEST Research Plan v1.1 (2025) commits ASIPP to a CFEDR mission of "net electrical power generation" with Pfus = 1.5–3.0 GW, but no source in the corpus quotes a CFEDR net electric figure. If/when CFEDR publishes a commercial-grade design with a stated MWe, the design point for this concept should be re-selected away from ARIES-ACT1 to the Chinese-roadmap plant; direction of P_native shift is unknown until published. This is the dominant open question.
- **PFPP design release**: If the eventual Chinese Prototype Fusion Power Plant publishes a design point, it would supersede both CFEDR and ARIES-ACT1 as the natural design point for this concept.
- **CFETR Phase I/II thermal-to-electric coupling**: The cfetr-power-conversion-studies corpus recommends sCO2 Brayton for the Chinese fusion lineage at 34–47% efficiency, but no source actually couples that efficiency to a CFETR fusion-power scenario to produce a CFETR net-electric figure. If a Chinese-program PCS study completes that coupling, CFETR Phase II × 40% sCO2 ≈ 430 MWe gross becomes citable as a design point (currently this projection is not published).
- **EU-DEMO / JA-DEMO ingestion**: Both programs are state-backed-tokamak peers with published Pnet targets in the literature but no dedicated source for either was ingested for this concept. Adding one would substantially expand the candidate pool and likely shift the design point downward from ARIES-ACT1's 1000 MWe.
- **Concept identity alignment**: The concept is nominally anchored on Neo Fusion / ASIPP's BEST → CFEDR roadmap, but the chosen design point is a US-DOE conceptual study. The mismatch is acceptable under the selection rule (ARIES-ACT is a state-backed tokamak with the best published data in the corpus) but would force a re-selection the moment a Chinese-program plant publishes an electric design point.
