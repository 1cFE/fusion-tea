# Phase 3 diff: 10-large-scale-stellarator

**Generated:** 2026-05-22T13:59:15-07:00

## Counts (Phase 2 -> Phase 3 strict-read regen)

| field | phase2 | phase3 | Δ |
|-------|--------|--------|---|
| blocking_count   | 2 | 2 | 0 |
| important_count  | 6 | 8 | - |
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
# Gap Assessment: Large-Scale Stellarator (D-T)
```

## Blocking-tier lines (new)

```
129:| Power conversion cycle type and efficiency | proprietary | blocking | HCPB → He/steam ~33–35%; DCLL → advanced Rankine ~40%; 7 pp spread is meaningful for LCOE. CDR specifies this. Thea Helios achieves 40.2% with Pb-Li + Rankine — usable as upper-bound analog. |
130:| Capital cost by CAS account (CAS 21–27) | proprietary | blocking | No public CAS breakdown for GIGA; must use ARIES-CS as analog (ARIES cost account framework from knowledge/sources/aries_cost_account_documentation/ provides the CAS structure but not GIGA-specific values) |
```

## Full unified diff (truncated to 400 lines)

```diff
--- /tmp/gap_phase2_state/10-large-scale-stellarator.md	2026-05-22 12:59:21.064279526 -0700
+++ /home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/10-large-scale-stellarator/gap_report.md	2026-05-22 13:59:15.914017639 -0700
@@ -1,13 +1,8 @@
-I have read all the key sources. Now I'll write the comprehensive gap assessment.
-
----
-
 # Gap Assessment: Large-Scale Stellarator (D-T)
 
 ## Overall Readiness
 **Rating**: Mostly Ready
-
-**Summary**: The Gauss Fusion GIGA concept has unusually strong public documentation relative to other private fusion companies: a 1,000-page CDR was completed in 2025 and independently reviewed, the HELIAS/HSR4/18 reactor heritage provides a decades-deep engineering baseline, and active industrial partnerships have generated specific technical disclosures on magnets and blanket development. Physics and engineering sections can be written to high quality. The main gap is economic: no CAS-level cost breakdown exists in the public domain, and the thermal conversion cycle/blanket type (which sets thermal efficiency) remains undisclosed. LCOE estimation requires significant reliance on HELIAS analogs and fleet-wide references rather than GIGA-specific data.
+**Summary**: Gauss Fusion's GIGA concept is unusually well-documented for a fusion startup: a 1,000+ page CDR was validated by an independent 13-person expert panel in January 2026, and the HELIAS heritage provides decades of plasma physics and blanket engineering literature. Plant-level parameters (geometry, power output, magnet system, supply chain mass budget) are publicly established. The primary gaps are proprietary CDR content — specifically the blanket type, power conversion cycle, and itemized capital cost breakdown — which must be substituted with HELIAS/ARIES-CS analogs for LCOE estimation. Qualitative analysis and TRL assessment can proceed now; quantitative LCOE modeling requires explicit analog assumptions for 2 key parameters.
 
 ---
 
@@ -17,21 +12,22 @@
 **Coverage**: Good
 
 **Available**:
-- Gauss Fusion company disclosures across multiple sources: key plant parameters (3 GW thermal → 1 GW electric, 18 m major radius, 6 T on-axis, 12–13 T peak on coils, 1,500 m³ plasma volume, 1.7 m minor radius), roadmap to grid 2040–2045, and supply chain quantities (dossier, `gauss-fusion-technical-summary.md`)
-- HELIAS/HSR4/18 reactor study (IAEA, IPP, ~2001): predecessor design with nearly identical plasma parameters, quantified coil weights (~4,100 t SC coils), blanket options (HCPB 7,080 t; WCLL 14,450 t), 35% steam cycle efficiency, first wall area 2,500 m², cryostat volume 21,500 m³ (`helias-reactor-context.md`)
-- MT29 abstract on magnet system: 40 non-planar modular coils, conductor-in-plate design, demountable joints, dual LTS/HTS development strategy (`gauss-fusion-technical-summary.md`)
-- Tritium blanket partnerships: KIT/FZJ/IDOM finalizing TBB industrial design; Alsymex fabricating prototype sub-assemblies (`gauss-fusion-partnerships-2025.md`)
-- CDR completion and expert review by 13-person panel chaired by Zohm, January 2026 (`gauss-fusion-cdr-review-2026.md`)
-- HELIAS 5-B HCPB blanket structural study (Bongiovi et al. 2022): detailed mechanical design of bean-shaped blanket ring, TBR 1.3863, material specs (EUROFER 97, 8 MPa He coolant, W armour, Li₄SiO₄ breeder) (`helias-blanket-studies.md`)
-- Helios (Thea Energy) planar coil stellarator: compact analog with detailed power balance — 1.1 GW thermal, 390 MWe net, 40% thermal efficiency, 88% capacity factor — useful engineering analog (`arxiv-2512-08027v1.md`)
+- Plant-level parameters are publicly documented across multiple sources: 3 GW thermal / 1 GW electric, 18 m major radius, 1.7 m minor radius, 1500 m³ plasma volume, 40 non-planar modular coils (5 shapes × 8), 6 T on-axis / 12–13 T on-coil, 1 MW/m² first-wall neutron load, 5-year blanket life, 40-year magnet life (`iter-01/sources/gauss-fusion-technical-summary.md`).
+- HELIAS heritage (HSR4/18, HSR5/22) provides deep plasma physics literature: transport scaling (LGS and ISS95), MHD stability up to β=4.3%, alpha-particle loss rate (~2.5%), coil mass and geometry estimates, blanket weight estimates for HCPB (~7,080 t) and WCLL (~14,450 t) concepts, and ~35% thermal efficiency for Rankine cycle (`iter-01/sources/helias-reactor-context.md`).
+- Supply chain bill of materials published: ~10,000 t vacuum vessel steel, ~35,000 t SC coils, ~800 t LTS + 26M m HTS, ~75 t lithium, RAFM steel, tungsten, beryllium (`iter-01/sources/gauss-fusion-technical-summary.md`).
+- Partnership structure confirms active blanket (KIT/FZJ/IDOM/Alsymex), magnet (ENEA/ICAS/Tokamak Energy), and tritium cycle (F4E) work is in progress (`iter-02/sources/gauss-fusion-partnerships-2025.md`).
+- Expert panel confirmation of CDR: overall architecture, system interfaces, central technical solutions reviewed and approved (`iter-02/sources/gauss-fusion-cdr-review-2026.md`).
+- HELIAS 5-B HCPB blanket study provides detailed mechanical design and TBR analysis (~1.39 in idealistic model) for HCPB concept applicable to GIGA geometry (`iter-02/sources/helias-blanket-studies.md`).
+- FOAK total cost estimate of €15–18B published (`iter-01/sources/gauss-fusion-technical-summary.md`).
 
 **Missing**:
-- Full CDR content (behind download gate at gauss-fusion.com; covers detailed systems specs, fuel cycle, power conversion, waste)
-- Any published economic analysis of GIGA specifically
+- CDR full technical content is behind a download gate; blanket type, power conversion cycle, tritium extraction scheme, and CAS-level cost breakdown are proprietary.
+- No published LCOE or itemized capital cost analysis for GIGA.
+- Gauss Fusion has made limited technical disclosures at conferences (MT29 magnet abstract is the most detailed public technical document).
 
 **Gaps**:
-- CDR full content — `proprietary` — **important**: CDR would resolve blanket type, power conversion cycle, and many engineering uncertainties. The publicly available CDR executive summary is likely sufficient for the analysis but has not been captured.
-- Lack of independent academic or OSTI publications specifically on GIGA economics — `not-yet-sourced` — **nice-to-have**
+- CDR blanket type and power conversion specifics — proprietary — important (affects thermal efficiency and capital cost structure)
+- GIGA-specific LCOE / capital cost breakdown — proprietary — blocking (no public analog within Gauss publications)
 
 ---
 
@@ -39,22 +35,22 @@
 **Coverage**: Partial
 
 **Available**:
-- Steady-state operation: explicitly confirmed as inherent stellarator advantage; no disruption risk, no current drive required (`dossier.md`, `gauss-fusion-technical-summary.md`)
-- Burning plasma regime: 3 GW fusion power implies deeply ignited operation; alpha particle heating dominates (~600 MW alphas vs. ~50–100 MW ECRH for startup/control) — well documented via HELIAS heritage
-- ECRH heating: not Gauss-confirmed but effectively certain from stellarator physics precedent and HELIAS heritage; startup only at reactor scale
-- Non-planar modular coil geometry: acknowledged as the primary engineering complexity driver — 3D coil shapes require tight tolerances; demountable joints at ~1 nΩ per joint are a novel innovation requiring prototype validation
-- Blanket accessibility: porthole-based maintenance (portholes ~2×6 m² between coils) identified in HSR4/18 studies as the baseline concept — more complex than tokamak sector maintenance
-- Divertor concept: island divertor concept (same as W7-X) documented in HELIAS studies; preliminary divertor heat load >10 MW/m² noted as critical issue in HSR4/18 (`helias-reactor-context.md`)
+- Steady-state plasma physics well understood via W7-X and HELIAS heritage: no disruptions, no current drive required, neoclassical transport minimized in QI configuration. Alpha particle losses ~2.5% tolerable for ignition balance (`iter-01/sources/helias-reactor-context.md`).
+- Stellarator-specific operational advantages vs. tokamak are well documented: inherent steady-state, no Greenwald density limit, no disruption risk (`iter-02/sources/arxiv-2512-08027v1.md`, Thea Helios).
+- Power balance structure: 3 GW fusion power with alpha-dominated heating; ECRH required only for startup/profile control (~50–100 MW estimated); this is confirmed by analogy with Thea Helios (10 MW ECRH startup, <1 MW ignited).
+- Divertor concept: HELIAS uses island divertor concept (4/4-island topology, W7-X-derived); porthole maintenance with 8 portholes per period identified (`iter-01/sources/helias-reactor-context.md`). ARIES-CS maintenance analysis confirms porthole approach with ~85% plant availability (`iter-02/sources/core-outputs-100308302.md`).
+- 3D geometry challenges for blanket design documented: many different blanket segment shapes required vs. only 2 for tokamak; complex non-planar access geometry requires ParaStell-type tools (`iter-02/sources/frontiersin-journals-nuclear-engineering-articles-10-3389.md`).
+- Demountable joints: ~250 per coil at ~1 nΩ target resistance; allows sector-based maintenance (`iter-01/sources/gauss-fusion-technical-summary.md`).
 
 **Missing**:
-- Power conversion cycle details (He/steam for HCPB, or higher-efficiency options for DCLL) — not disclosed publicly
-- Thermal-hydraulic system design for GIGA specifically
-- Plasma facing component material qualification under 3 GW neutron environment (first wall material choice unspecified beyond tungsten armour)
+- Gauss Fusion's specific divertor design is not publicly disclosed. The W7-X island divertor does not scale to a power plant without major redesign — this is an acknowledged open problem in stellarator physics. Thea Helios solved this with a novel QA X-point divertor, but GIGA's QI geometry requires a different solution.
+- Recirculating power breakdown not available: cryogenic load, auxiliary heating, tritium processing, vacuum pumping power are all unknown.
+- Power conversion cycle architecture unknown (He/steam Rankine for HCPB vs. higher-efficiency options for DCLL).
 
 **Gaps**:
-- Power conversion cycle type — `proprietary` — **important**: affects thermal efficiency (35% steam Rankine vs. 40%+ He-Brayton or DCLL-enabled cycles), which directly enters LCOE
-- Divertor heat load management strategy — `not-yet-sourced` — **important**: >10 MW/m² divertor load in HELIAS geometry is a known challenge with no published Gauss-specific solution
-- Plasma-facing component material specification — `derivable` from ITER/DEMO analogues — **nice-to-have**
+- Divertor architecture and heat exhaust solution at power plant scale — proprietary/not-yet-sourced — important (open physics problem for stellarators; GIGA's solution is CDR-only)
+- Recirculating power breakdown — derivable/proprietary — important (needed for gross-to-net efficiency and LCOE numerics)
+- Power conversion cycle type — proprietary — important (determines thermal efficiency: 33% HCPB → steam vs. ~40% DCLL advanced cycle)
 
 ---
 
@@ -62,21 +58,23 @@
 **Coverage**: Partial
 
 **Available**:
-- **Plasma physics**: W7-X experimental results directly validate QI stellarator confinement scaling. LGS empirical scaling predicts ignition in HSR4/18 without enhancement factor. Neoclassical transport <1% effective helical ripple confirmed. Alpha particle losses ~2.5% tolerable. TRL: 4–5 for plasma physics basis.
-- **Magnet system**: Conceptual design complete (CDR). Dual LTS/HTS conductor development underway with ENEA (HTS cables/joints) and ICAS (LTS cables), €9M + €10M BMBF grants. Demountable joint prototyping at KIT. Conductor-in-plate concept (novel). Tokamak Energy HTS collaboration signed Oct 2025. TRL: 3–4 (conductor level), lower for full coil assembly.
-- **Tritium breeding blanket**: KIT/FZJ industrial design ongoing; Alsymex prototype sub-assemblies contracted; HELIAS 5-B HCPB structural concept analyzed to heterogeneous detail. TBR 1.3863 demonstrated analytically for HELIAS 5-B HCPB. TRL: 2–3.
-- **Divertor**: Island divertor concept (W7-X heritage). W7-X has operated with island divertor. TRL: 4 for concept, 2 for reactor-scale implementation.
-- **Vacuum vessel**: 10,000 t steel VV identified in supply chain; 3D geometry well-documented. No specific VV manufacturing study found.
-- **CDR milestone**: Completed and independently reviewed (expert panel, Jan 2026) — equivalent to pre-Phase-B gate, significantly higher than most private fusion companies.
+- **Plasma physics (TRL 4–5)**: W7-X has achieved ISS04 enhancement factor H=1.4 at reactor-relevant conditions; alpha-particle confinement analytically validated in HSR4/18; MHD stability limit established at <β>=4.2–4.3%. Physics basis is the most mature subsystem.
+- **LTS coil technology (TRL 4–5)**: ITER TF coils (Nb3Sn, ~300 t each, ~30–35 m perimeter) directly analogous in scale and field to GIGA coils. ICAS partnership for LTS cable manufacturing is active. Modular non-planar geometry is more complex than ITER.
+- **HTS coil development (TRL 3–4)**: REBCO HTS cable/joint development in active collaboration with Tokamak Energy and ENEA. Demountable joints at ~1 nΩ are the critical innovation; this resistance target has been demonstrated in laboratory conditions but not at GIGA coil scale (~100 kA current).
+- **HCPB blanket for HELIAS geometry (TRL 2–3)**: Homogeneous and heterogeneous mechanical models developed for HELIAS 5-B (`iter-02/sources/helias-blanket-studies.md`); TBR ~1.39 in idealized model. Critical: HELIAS 5-B is 5-period while GIGA is 4-period; direct transferability is partial. Prototype sub-assemblies being fabricated by Alsymex.
+- **Tritium handling (TRL 2–3)**: F4E collaboration ongoing; no stellarator has ever handled tritium at power plant scale.
+- **First wall/armor (TRL 4–5)**: EUROFER97 RAFM steel and W armor well-studied from DEMO program. 5-year replacement cycle feasible.
+- **ECRH heating (TRL 5–6)**: W7-X uses 140 GHz ECRH; ITER-spec gyrotrons at 170 GHz are production-ready.
 
 **Missing**:
-- Formal TRL assessment per subsystem (not published)
-- Cryogenic system engineering (21,500 m³ cryostat)
-- ECRH system specifications and sourcing
+- No published TRL-by-subsystem assessment from Gauss Fusion or an independent reviewer.
+- Divertor concept for GIGA not disclosed; W7-X island divertor TRL is high (5–6) but it doesn't scale to power plant.
+- Demountable SC joint performance at 100 kA / 12–13 T has not been demonstrated; prototype status unknown.
 
 **Gaps**:
-- Published TRL matrix — `not-yet-sourced` — **nice-to-have**: subsystem TRLs can be inferred from engineering readiness but no structured assessment is public
-- Cryogenic system TRL — `derivable` from ITER/W7-X heritage — **nice-to-have**
+- Demountable joint validation at power plant scale — proprietary — important (de-risks the maintenance approach; CDR likely has test plan)
+- Stellarator divertor at power plant scale — truly-unknown/not-yet-sourced — important (active research problem; GIGA's solution hidden in CDR)
+- Per-subsystem TRL matrix (Gauss-specific) — proprietary — nice-to-have (can be estimated from heritage and published analogs)
 
 ---
 
@@ -84,28 +82,23 @@
 **Coverage**: Partial
 
 **Available**:
-- Quantified supply chain requirements (from binding.energy commercial roadmap, confirmed in dossier):
-  - ~10,000 t vacuum vessel steel
-  - ~35,000 t superconducting coil assemblies
-  - ~75 t lithium inventory
-  - ~800 t LTS conductor + ~26 million meters HTS conductor
-  - Beryllium, tungsten, RAFM steel, cryostats, breeder blankets
-- EUROFER 97 RAFM steel confirmed as structural material for TBB (Bongiovi et al. 2022) — EU fusion supply chain baseline
-- Nb3Sn strongly inferred for LTS track from 12–13 T field requirement (NbTi limited to ~10 T) — established ITER supply chain analog
-- REBCO confirmed for HTS track (Tokamak Energy, ENEA partnerships)
-- Partnership with ASG Superconductors (founding industrial partner) — Italy's leading SC magnet manufacturer
-- Tungsten first wall armour (2 mm per blanket segment): standard fusion industry material
+- Mass budget is publicly documented: ~35,000 t SC coils, ~10,000 t VV steel, ~800 t LTS + 26M m HTS tape, ~75 t Li (for breeding), tungsten, RAFM steel, beryllium (`iter-01/sources/gauss-fusion-technical-summary.md`).
+- HTS supply chain: 26M meters of REBCO tape is a massive procurement (~10× ITER's HTS content). Current global HTS production is ~5–10M m/year. Significant scale-up required. Partnerships with ENEA/ICAS/Tokamak Energy directly target this (`iter-02/sources/gauss-fusion-partnerships-2025.md`).
+- LTS supply chain: Nb3Sn is industrially available via ITER supply chain. ICAS (ENEA/Criotec/Tratos consortium) is manufacturing LTS cables for GIGA.
+- Beryllium: Critical material for neutron multiplication in HCPB blanket concept; European supply limited, strategic concern.
+- Li-6 enrichment: ~75 t total Li inventory; commercial enrichment feasible but requires coordination. Only a few global facilities enrich Li-6 to >90%.
+- RAFM steel (EUROFER97): Active European supply chain from DEMO program; ITER-scale manufacturing base established.
+- Tungsten: Standard industrial material; no supply chain risk at planned quantities.
 
 **Missing**:
-- REBCO availability at 26 million meters scale — current global production is orders of magnitude below GIGA requirements and represents a market-creation challenge
-- 6Li enrichment requirements for lithium breeding (HCPB uses natural Li; DCLL studies cited 90% enriched ⁶Li)
-- Beryllium supply chain (neutron multiplier for HCPB concept) — limited global production, geopolitically concentrated
-- RAFM steel industrial production scale-up timeline
+- No published cost-per-unit estimates for critical materials in GIGA context.
+- HTS supply chain ramp-up timeline and cost structure not public.
+- Beryllium supply chain analysis (if HCPB blanket is selected) not published.
 
 **Gaps**:
-- REBCO supply chain bottleneck at scale — `not-yet-sourced` — **important**: global HTS production insufficient for GIGA at current volumes; supply chain roadmap not published
-- Beryllium availability (if HCPB selected) — `not-yet-sourced` — **important**: limited global production, high cost, geopolitical concentration (Kazakhstan/US)
-- Lithium enrichment strategy — `derivable` — **nice-to-have**: ⁶Li enrichment level determines cost and supply chain complexity
+- HTS tape supply chain cost and ramp-up timeline — not-yet-sourced — important (26M m is a market-defining quantity; cost per unit drives CAS 22 magnet cost)
+- RAFM steel fabrication cost at GIGA scale (stellarator-specific complex shapes) — not-yet-sourced — important
+- Beryllium cost and supply chain risk (if HCPB) — not-yet-sourced — nice-to-have (conditional on blanket type)
 
 ---
 
@@ -113,62 +106,57 @@
 **Available Parameters**:
 | Parameter | Value/Range | Source | Confidence |
 |-----------|-------------|--------|------------|
-| Fusion power | 3,000 MW | Dossier, HELIAS heritage | high |
-| Gross thermal output | ~3,000 MW (neutron + alpha heat) | Dossier, CDR summary | high |
-| Net electric output | ~1,000 MWe | Dossier, CDR summary | high |
-| Gross thermal-to-electric efficiency | ~33% (implied: 3 GW → 1 GW) | Derived | medium |
-| First wall neutron load | 1 MW/m² | Dossier | high |
-| FW/blanket design life | 5 years | Dossier | high |
-| Magnet/VV design life | 40 years | Dossier | high |
-| Plant design life | 40 years (magnet-limited) | Dossier | medium |
-| FOAK estimated total cost | $15–18B | binding.energy commercial roadmap | low |
-| Plasma volume | 1,500 m³ | Dossier | high |
-| Coil mass | ~35,000 t total | Dossier supply chain | medium |
-| VV mass | ~10,000 t | Dossier supply chain | medium |
-| Operation mode | Steady-state (no pulsing) | Dossier | high |
-| Blanket lifetime analog (HELIAS) | 4.6–9 years (100–140 dpa limit) | helias-reactor-context.md | medium |
-| Thermal efficiency analog (Helios) | 40% (DCLL/higher-efficiency cycle) | arxiv-2512-08027v1.md | low (different architecture) |
-| Capacity factor analog (Helios) | 88% (biennial 84-day outage) | arxiv-2512-08027v1.md | low (different architecture) |
+| Net electric output | ~1 GWe | gauss-fusion-technical-summary.md | H |
+| Thermal output | 3 GW | gauss-fusion-technical-summary.md | H |
+| Major radius | 18 m | gauss-fusion-technical-summary.md | H |
+| Plasma volume | 1,500 m³ | gauss-fusion-technical-summary.md | H |
+| First wall neutron load | 1 MW/m² | gauss-fusion-technical-summary.md | H |
+| Blanket/FW replacement interval | 5 years | gauss-fusion-technical-summary.md | H |
+| Magnet/VV design lifetime | 40 years | gauss-fusion-technical-summary.md | H |
+| SC coil mass | ~35,000 t | gauss-fusion-technical-summary.md | M |
+| VV steel mass | ~10,000 t | gauss-fusion-technical-summary.md | M |
+| LTS conductor mass | ~800 t | gauss-fusion-technical-summary.md | M |
+| HTS tape length | ~26M m | gauss-fusion-technical-summary.md | M |
+| Lithium inventory | ~75 t | gauss-fusion-technical-summary.md | M |
+| FOAK total cost estimate | €15–18B | gauss-fusion-technical-summary.md | L |
+| Thermal efficiency (Rankine analog) | 33–40% | helias-reactor-context.md (35%), Thea Helios (40.2%) [knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/] | M |
+| Capacity factor (analog) | 85–88% | ARIES-CS (core-outputs-100308302.md, 85%), Thea Helios (88%) | M |
+| LCOE range (D-T MFE analog) | $140–$550/MWh | tea_dt_mfe_cost_analysis (Araiinejad & Shirvan, 2025): $8,800–$22,200/kW OCC for 350 MWe ARC | L |
 
 **Missing Parameters**:
 | Parameter | Gap Type | Criticality | Notes |
 |-----------|----------|-------------|-------|
-| CAS-level capital cost breakdown | proprietary | blocking | CDR contains this but not public; HELIAS analog or PyFECONS scaling can substitute with high uncertainty |
-| O&M cost estimate ($/MWe/yr) | proprietary | blocking | No fusion stellarator O&M study specific to GIGA scale exists; ARIES-CS or TEA D-T MFE analogs needed |
-| Thermal conversion efficiency (specific cycle) | proprietary | important | 33% inferred from output ratio; actual depends on HCPB (≤35%) vs. DCLL (≥40%) blanket choice |
-| Capacity factor / planned outage schedule | proprietary | important | Steady-state favors high CF; no GIGA-specific availability study; Helios 88% is a reasonable analog |
-| Blanket replacement unit cost | not-yet-sourced | important | Mass quantities known (7,080–14,450 t); per-module replacement cost not quantified |
-| Tritium startup inventory cost | derivable | important | 1–2 kg T₂ startup (from Helios analog); market price ~$100–150M per kg; calculable |
-| ECRH system cost | not-yet-sourced | nice-to-have | Startup heating only (~10–50 MW at reactor scale); ITER ECRH cost analogs available |
-| Balance of plant cost (turbines, heat exchangers) | derivable | important | Standard plant engineering; depends on cycle type |
-| Cryogenic system cost | not-yet-sourced | important | 21,500 m³ cryostat at ~4 K; ITER cryoplant cost analog ($0.5–1B) applicable |
-| Decommissioning cost | derivable | nice-to-have | Similar activated waste inventory to equivalent tokamak (noted in helias-reactor-context.md) |
+| Power conversion cycle type and efficiency | proprietary | blocking | HCPB → He/steam ~33–35%; DCLL → advanced Rankine ~40%; 7 pp spread is meaningful for LCOE. CDR specifies this. Thea Helios achieves 40.2% with Pb-Li + Rankine — usable as upper-bound analog. |
+| Capital cost by CAS account (CAS 21–27) | proprietary | blocking | No public CAS breakdown for GIGA; must use ARIES-CS as analog (ARIES cost account framework from knowledge/sources/aries_cost_account_documentation/ provides the CAS structure but not GIGA-specific values) |
+| Blanket type (HCPB vs. DCLL) | proprietary | important | Determines efficiency, material costs, and TBR; active partnerships but not disclosed. Thea Helios uses DCLL as direct stellarator analog. |
+| Recirculating power breakdown | derivable | important | Cryogenic + auxiliary heating + pumping; can be estimated from analogs (~10–15% of gross electric) |
+| O&M annual cost | not-yet-sourced | important | ARIES-CS has published O&M estimates; no GIGA-specific values |
+| Tritium breeding and fuel cost | derivable | important | Standard D-T assumptions applicable; Li-6 cost and tritium processing cost not specified |
+| Capacity factor (GIGA-specific) | derivable | important | Demountable joints may enable higher availability than ARIES-CS (85%); Thea Helios achieves 88% with biennial maintenance; bracket at 85–90% |
+| NOAK cost scaling from FOAK | derivable | important | €15–18B is FOAK; standard learning curve methodology applicable but no Gauss-specific data |
+| Decommissioning cost | derivable | nice-to-have | Standard ARIES CAS 93 methodology applicable |
 
 ---
 
 ## Source Recommendations
 
-1. **HELIAS reactor engineering studies (EUROfusion/KIT)** — multiple KIT publications exist on HELIAS 5-B systems engineering, costs, and neutronics. Search OSTI/FusionDB for "HELIAS reactor cost" or "HELIAS 5-B engineering". `not-yet-sourced` — likely to yield analog cost data at CAS level. *Unverified — confirm existence before searching.*
+1. **CDR Executive Summary** (Gauss Fusion, gauss-fusion.com/cdr-executive-summary): Most critical source. Would resolve blanket type, power conversion cycle, heating system specifics, and possibly a high-level cost estimate. Listed as publicly downloadable after registration; not captured in Phase 1a. Suggested action: access CDR executive summary directly. *Existence confirmed — Gauss Fusion CDR was submitted to German government in October 2025 and reviewed January 2026.*
 
-2. **ARIES-CS cost study (El-Guebaly et al., 2008)** — the ARIES compact stellarator study included CAS-level costing directly applicable as an analog. Part of the ARIES series in `knowledge/sources/aries_cost_account_documentation/` — check whether ARIES-CS specifically is covered, or ingest the primary Fusion Sci. Technol. 54 (2008) special issue. `not-yet-sourced`.
+2. **ARIES-CS Power Plant Study** (Najmabadi et al., Fusion Engineering and Design, 2008): Definitive stellarator power plant cost study in the ARIES CAS framework. Provides capital cost breakdown for a QA compact stellarator (R=7.75 m, P_net~1 GW) using the same CAS 20-27 structure as the ARIES Cost Account Documentation. Search OSTI for "ARIES-CS" — confirmed exists as peer-reviewed publication. *Not-yet-sourced.*
 
-3. **TEA D-T MFE cost analysis** (`knowledge/sources/tea_dt_mfe_cost_analysis/`) — already ingested; should be read for CAS structure directly applicable to GIGA as a D-T MFE concept. Useful for BOP, O&M, indirect cost fractions.
+3. **HSR4/18 Costing Studies** (IPP Garching, various 1999–2005): HELIAS predecessor design studies may include parametric cost estimates for the coil system and blanket. Search IPP report series (IPP-Report III/xxx) and SOFT conference proceedings. *Existence unverified — confirm before searching.* `unverified — confirm existence before searching`
 
-4. **Gauss Fusion CDR executive summary** — reportedly accessible at gauss-fusion.com/cdr-executive-summary (behind a download gate per dossier). If accessible: `proprietary` but gated, not classified — worth attempting download. Would resolve blanket type, power cycle, and key cost assumptions.
+4. **PROCESS Stellarator Module Documentation** (UKAEA): The PROCESS systems code has a stellarator module that outputs cost estimates for HELIAS-type configurations. UKAEA GitHub and associated publications may contain cost outputs for HSR-like parameterizations. *Not-yet-sourced.*
 
-5. **KIT/FZJ TBB publications 2025–2026** — Gauss Fusion's TBB partnerships are recent (announced 2025). Watch for KIT/FZJ conference papers (SOFT 2026, ISFNT 2025) on the GIGA-specific TBB design. `not-yet-sourced`.
+5. **KIT/FZJ HCPB and DCLL Blanket Studies for HELIAS geometry**: More recent publications beyond the HELIAS 5-B HCPB paper already captured. KIT has ongoing HELIAS blanket work under EUROfusion. Search OSTI or KIT repository for "HELIAS blanket 2022–2026." *Not-yet-sourced.*
 
-6. **PyFECONS stellarator modules** (`/home/reid/PyFECONS`) — already available; the code has stellarator-specific modules. Running PyFECONS with GIGA parameters (18 m major radius, 3 GW, 40 coils, LTS+HTS) would generate a CAS-level cost estimate as a `derivable` baseline for all missing cost parameters.
+6. **Disqualified fleet sources**: All IFE-focused sources (laser ICF, heavy-ion, AMPS, Xcimer, accelerators) do not apply to stellarator MFE economics and are disqualified. The ARPA-E ALPHA revisit (`knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/`) covers non-stellarator MIF/MTF concepts (mirror, Z-pinch, FRC, MTF variants) and provides no stellarator-specific cost data — disqualified. The Wurzel & Hsu progress-toward-breakeven meta-analysis (`knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/`) provides physics performance benchmarks but the concept-scoped sources already establish the W7-X / HELIAS physics basis adequately — disqualified for this assessment. The historical ORNL economics assessment (`knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/`) is a historical benchmarking document; the TEA D-T MFE analysis (Araiinejad & Shirvan 2025, read above) is more current and directly applicable — ORNL source disqualified.
 
 ---
 
 ## Summary
 
-The available data is sufficient to write a high-quality D1+ analysis covering physics basis, engineering architecture, subsystem maturity, and supply chain considerations — these are well documented by the HELIAS lineage plus Gauss Fusion's own disclosures. The analysis can proceed without additional sources for sections 1–4.
-
-The primary weakness is LCOE: the only GIGA-specific economic data point is a $15–18B FOAK cost estimate, with no CAS breakdown and no published efficiency or capacity factor. This is typical for pre-commercial fusion concepts. The recommended approach for section 5 is to (a) read `knowledge/sources/tea_dt_mfe_cost_analysis/` to apply CAS-level methodology, (b) run PyFECONS with GIGA parameters to generate a `derivable` baseline, and (c) use the Helios (Thea Energy) design as a capacity-factor and efficiency analog. All cost estimates should carry explicit uncertainty flags as `derivable from HELIAS/ARIES-CS analogs, not from GIGA-specific data`.
-
-**Recommendation: Proceed to full analysis.** The physics, engineering, and maturity sections have sufficient source coverage for a D1+ quality write-up. The LCOE section requires explicit use of analog references and stated assumptions, but this is appropriate given the pre-commercial status of the concept.
+Proceed to full analysis with explicit analog assumptions for two blocking parameters. For power conversion efficiency: bracket at 33–40% using HCPB (helias-reactor-context.md, ~35%) and DCLL analogs (Thea Helios: 40.2% in `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/`). For capital cost structure: use ARIES-CS as the primary cost analog within the ARIES CAS framework (`knowledge/sources/aries_cost_account_documentation/`), noting that GIGA's larger scale (R=18 m vs R=7.75 m), non-planar modular coil geometry, and demountable joints will diverge from ARIES-CS. The qualitative sections (system function, subsystem maturity, materials/supply chain) can be written at high quality from available sources. Attempting to acquire the CDR executive summary before LCOE modeling would reduce the two blocking gaps to important or resolved.
 
 ---
 
@@ -177,8 +165,8 @@
 ```yaml
 overall_rating: "Mostly Ready"
 blocking_count: 2
-important_count: 6
-counting_method: "section_5_missing_parameters (CAS-level cost breakdown, O&M cost) as blocking; thermal efficiency, capacity factor, blanket replacement cost, TBB unit cost, cryogenic system cost, BOP cost as important; plus power conversion cycle type from section 2 merged with thermal efficiency"
+important_count: 8
+counting_method: "all_sections_deduplicated: §1 CDR cost breakdown (blocking), §5 power conversion cycle (blocking); §2 divertor/recirculating power/blanket type (3 important); §3 demountable joint validation/divertor TRL (2 important, blanket type already counted); §4 HTS supply chain/RAFM fabrication cost (2 important); §5 capacity factor/O&M/NOAK scaling/tritium cost (4 important, blanket type and divertor already counted); net deduplicated: 8 important"
 section_coverage:
   availability_of_data:       "Good"
   system_function:            "Partial"
```
