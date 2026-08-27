---
date: 2026-08-21
researcher: Claude
topic: "WI-031 — second-arm values for the Item 6 A/B studies"
tags: [research, WI-031, run-study, item-6, stellarator, sco2, cryoplant, nb3sn, holdout]
research_type: domain
status: pending
---

# Research: WI-031 — second-arm values for the Item 6 A/B studies

**Work item**: `work/active/WI-031_research-round-item6-values/spec.md`
**Consumer**: RUN-STUDY Item 6, `.project/active/run-study-first-consumer/design.md` (Appendix A arm tables)
**Rules honored**: `knowledge/holdout/aries-cs/PROTOCOL.md` (sealed; nothing under `knowledge/holdout/` opened; see § Holdout disclosures). No fallbacks `[OWNER 2026-08-21]`: every value below ends as a citation, a derived number with its inputs cited, or an explicit "no source".

## Research Question

For the four second-arm values Item 6 cannot source from the model, find an admissible citation or report "no source": (1) sCO2 `p_pump` for the helium-cooled Stellaris blanket; (2) provenance of arm-A `eta_th` = 1/3; (3) fraction-of-Carnot at 4.5 K for the Nb3Sn arm; (4) Nb3Sn winding-pack current density or volume for a comparable coil set.

## Summary

- **`p_pump` (study 2, arm-sco2): hold it equal across the three arms; no separate sCO2 value exists or is expected.** The power cycle is the secondary side. Stellaris's primary coolant is helium at 8 MPa regardless of cycle, and 1costingFE's cycle presets change only `eta_th`, the turbine rate, and the heat-rejection rate; `p_pump` is a concept-level engineering default. The sCO2 compressor work is inside `eta_th`. Status: **resolved by construction** (in-repo citations). Surfaced separately: the held value 1.0 MW is two orders of magnitude below admissible helium-primary circulator figures (2–6 % of blanket thermal power).
- **`eta_th` (study 2, arm-rankine-paper): confirmed as a bare assumption, with a citation correction.** The paper says "assuming a *simple* electrical conversion efficiency of 1/3" (raw PDF p. 3). Both extractions paraphrase this as "single-element". The paper names no cycle anywhere; its only balance-of-plant reference is Warmer & Bubelis 2019 (HELIAS). Status: **resolved** (PDF witness); the design table's citation should move from `stellaris-design-details.md:251` to the PDF.
- **`f_carnot_cryo` at 4.5 K (study 1, arm-nb3sn): no admissible in-repo value; three open web sources give 0.22–0.30.** In-repo W7-X material gives capacity (7 kW at 4.5 K) but no electrical power. ITER (75 kW at 4.5 K + 1300 kW at 80 K, 35 MW electrical) → 0.24 plant-level; LHC (18 kW at 4.5 K per 4 MW) → 0.30; W7-X (5 kW design capacity, 1.5 MW compressor rating) → ≥ 0.22. Status: **citation pending ingestion** via `/manage-sources`; until then a disclosed hold. Recommendation: hold `f_carnot_cryo` equal in both arms so the A/B isolates `T_cold`; the evidence says the fraction is roughly temperature-independent at plant scale (a 20 K HTS plant assumption in an un-ingested Helical Fusion paper also lands at 0.28).
- **Nb3Sn winding pack (study 1, `vol_cold_cryo`): no in-repo number; one open-access EU DEMO TF paper gives enough to derive 15–28 A/mm².** EU DEMO reference TF: 14.9 MA-turns over an ~821 × 1240 mm winding pack → 14.6 A/mm²; the SPC react-and-wind proposal at 12.04 T → 28 A/mm². Stellaris's REBCO winding packs run 112–124 A/mm² (Table 8). At equal Amp-turns an Nb3Sn pack is 4–8× the cold volume: `vol_cold_cryo` ≈ 575–1100 m³ vs 136.56. Status: **citation pending ingestion**; disclosed hold until then.

## Detailed Findings

### 1. sCO2 primary-coolant pumping power (`p_pump`)

**What the upstream model says.** 1costingFE's cycle selection carries exactly three fields per cycle: `eta_th`, `turbine_per_mw`, `heat_rej_per_mw` (`/home/reid/1cfe/1costingfe/src/costingfe/defaults.py:578-593`, pinned `0254385`). The justification doc states it plainly: "The cycle determines `eta_th`, CAS23 (`turbine_per_mw`), and CAS26 (`heat_rej_per_mw`). CAS24 and CAS25 are cycle-independent" (`docs/account_justification/CAS23_26_balance_of_plant.md:163-166`). `p_pump` lives in the concept engineering defaults as "Pumping power [MW]" = 1.0 (`src/costingfe/data/defaults/steady_state_stellarator.yaml:21`) with no justification document; it enters the thermal balance as `eta_p * p_pump` (`src/costingfe/layers/physics.py:303`) and the recirculating sum. The sCO2 section of the doc discusses recuperators and turbomachinery size, never primary pumping (`CAS23_26_balance_of_plant.md:188-213`).

**What Stellaris says.** The blanket is helium-cooled: "gas as the primary coolant. We simulate helium at 8 MPa" (`knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/output.md:1336`); the blanket is HCLL (`:1349`). Pumping is explicitly future work: "thermal stress analysis and estimation of pumping requirements" in the open-items list (`:2831`). The PDF text contains no occurrence of "Rankine", "Brayton", "steam", or "turbine" (checked with `pdftotext` on `raw.pdf`).

**Physics.** With a helium primary loop, the power-conversion working fluid (steam or sCO2) sits on the secondary side of the intermediate heat exchanger. The primary circulator power is set by the helium mass flow and loop pressure drop, not by the secondary cycle. The sCO2 recompression cycle's own compressor work is internal to its cycle efficiency, i.e. already inside `eta_th` = 0.47. So the honest arm-sco2 value for `p_pump` is the same as the Rankine arms', by construction. The only way the cycle would touch the primary loop is through IHX temperature constraints, which 1costingFE does not model.

**Disposition.** `p_pump` = 1.0 in all three arms, cited to `steady_state_stellarator.yaml:21` and to the cycle-independence statement above. The record's § 17 should say the cycle does not reach `p_pump`, not that an sCO2 value is missing.

**Premise conflict, surfaced (not acted on).** The held value is far below admissible helium-primary figures:

| source | admissibility | figure | fraction of thermal |
|---|---|---|---|
| Moscato et al., "Progress in the design development of EU DEMO HCPB PHTS", SOFT 2018 preprint (EUROfusion WPBOP-CPR(18) 20276) — open PDF, 0 ARIES-CS mentions, **not ingested** | ingestible | 2101.7 MWth blanket; 9 loops, 2 compressors each; 6.8 MW (IB) / 7.5 MW (OB) per compressor → ≈131 MW total; "near-term" 8-loop design 5.9 / 5.2 MW per compressor → 83–94 MW; target 5 MW per compressor | 6.2 % (2017), ~4 % (near-term) |
| Cismondi et al., EUROfusion WPPMI-CPR(17) 17709 — **ingested** at `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/scipub-wp-content-uploads-eurofusion-wppmicpr17-17709.md:176` (0 ARIES-CS mentions) | admissible | "In case of helium the pumping power is ~150MW, one order of magnitude higher than in case of water (~15MW)" for 2389 MW HCPB | 6.3 % |
| Kessel et al., ARIES-ACT overview — **ingested** at `knowledge/concept_research/33-state-backed-tokamak-best/iter-02/sources/osti-servlets-purl-1178069.md:175,290` (0 ARIES-CS mentions) | admissible | "pumping power requirement of ~1% of the total thermal power" (DCLL, He + LiPb); "12 MW for He in the divertor and Ppump/Pthermal ≈ 2% for ACT2" | 1–2 % |

For Stellaris at ~3150 MWth with helium at 8 MPa, these bracket 30–190 MW against the held 1.0 MW. Every arm of study 2 holds the same value, so the A/B delta is unaffected, but the absolute LCOE and `recirc_ok` verdicts carry a known optimism. This is a modeling-item question, not a WI-031 deliverable; see Recommendations.

Side note: the spec's "~1 GWth" for the Stellaris blanket reads as a slip for ~1 GWe; the paper's thermal power is ~3150 MW (`output.md:256`).

### 2. Arm-A `eta_th` provenance

**PDF witness (authority per `knowledge/SOURCE_INDEX.md`, Stellaris entry).** `pdftotext -f 3 -l 3 raw.pdf` of `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, § 2.1, second column:

> "Stellaris is predicted to produce approximately 3150 MW of thermal power and (assuming a simple electrical conversion efficiency of 1/3) nearly 1 GW of electrical power."

**Extraction discrepancy.** Both text extractions render this as "single-element conversion efficiency of 1/3" (`iter-01/sources/stellaris-design-details.md:251`; `iter-02/sources/stellaris-paper-details.md:251`; `publikationen-…/tmpissrtbos/output.md:256`). "Simple" is what the paper says; "single-element" is a paraphrase artifact of the shared extraction lineage (the SOURCE_INDEX caveat already warns that the two extractions are not independent witnesses). The meaning is unchanged — a bare 1/3 assumption — but the design table's citation (`design.md` Appendix A, `stellaris-design-details.md:251`) should point at the PDF page.

**Does the paper state a cycle?** No. Zero hits for cycle vocabulary in the PDF text. The only balance-of-plant pointer is reference [242], Warmer & Bubelis, "First considerations on the balance of plant for a HELIAS fusion power plant", Fusion Eng. Des. 146 (2019) 2259–2263 (`output.md:4520-4522`), cited in a literature survey sentence (`:1469`), not for Stellaris's own design.

**Consequence for D5.** The "Rankine" in `arm-rankine-paper` is Item 6's label (the cost rates are the upstream Rankine preset); the paper itself commits to no cycle. The record should say so. A second extraction discrepancy noticed in passing: the winding-pack copper-fraction current density reads 353 A/mm² in both derived extractions (`stellaris-design-details.md:1900`) and 560 A/mm² in the authoritative extraction (`output.md:1903`); not used by Item 6, logged for the SOURCE_INDEX caveat.

### 3. Fraction-of-Carnot at 4.5 K (`f_carnot_cryo`)

**Model context.** The chain is `cop = f_carnot × T_cold / (T_amb − T_cold)` (`models/library/analyses/mfe_cryo_plant.sysml:48-49`); Stellaris binds `f_carnot_cryo` = 0.20 as an explicit assumption at 20 K (`models/designs/stellarator_09/stellarator_plant.sysml:573-584`, WI-024 D4) with no 80 K shield load modeled. So the apples-to-apples number for the Nb3Sn arm is a *plant-level* fraction of Carnot for a 4.5 K helium plant, with `T_amb` = 300 K.

**In-repo, admissible: capacity only, no electrical power.**

- W7-X refrigerator: "a cooling capacity equivalent to about 7 kW at 4.5 K", boostable to 10 kW for hours from the LHe tank (`knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/pure-rest-items-item-2140562-component-file-2140561-content.md:222-226, 304-310`; Bosch et al., SOFE 2009). No electrical figure. Its refs [13] (Schauer et al., KI Luft- und Kältetechnik 2005) and [14] (Kuendig et al., ICEC 22, 2008) are the cryoplant papers and are not in the repo (`:799-803`).
- 1costingFE's cryoplant cost calibration: "ITER's cryoplant provides 75 kW at 4.5K … At 30 MW electrical cryo power, our model gives $200M — consistent with ITER" (`docs/account_justification/CAS22_plant_systems.md:222-226`). The 30 MW is the cost model's reference point, not a sourced ITER electrical figure; it happens to sit near ITER's published 35 MW.

**Open web sources (clean of ARIES-CS; ingestible; not yet citable).**

| plant | capacity | electrical | source (fetched 2026-08-21) | derived fraction of Carnot, T_amb = 300 K |
|---|---|---|---|---|
| ITER cryoplant | "installed cooling power of 75 kW at 4.5 K (helium) and 1300 kW at 80 K (nitrogen)" | "Operating the cryoplant will require 35 MW of electrical power" | https://www.iter.org/machine/supporting-systems/cryogenics ; https://www.iter.org/node/20687/cold-it-gets | ideal work 75 × 295.5/4.5 = 4.93 MW (4.5 K) + 1300 × 220/80 = 3.58 MW (80 K) = 8.5 MW → **0.24** plant-level; **0.14** if all 35 MW is charged to the 4.5 K load. (One secondary page quotes 600 kW at 80 K; that gives 0.19.) |
| LHC 4.5 K refrigerators | "each with a capacity of 18 kW at 4.5 K" (entropic equivalent) | "An electrical input power of 32 MW (4 MW per refrigerator)" | https://cerncourier.com/a/cerns-giant-fridge/ | (18/4000) / (4.5/295.5) = **0.30**; the specification paper (Claudet, Gayet, Wagner, LHC Project Report 331) states "28 % of the Carnot cycle" per a search snippet — the CDS PDF sits behind a bot gate and was not read |
| W7-X refrigerator | "designed for 5 kW continuous power at 4.5 K equivalent" | "corresponding to 1.5 MW compressor connected rating" | Dhard et al., "Final Acceptance Tests of Helium Refrigerator for Wendelstein 7-X", Physics Procedia 67 (2015) — search snippet only; ScienceDirect returned 403 | (5/1500) / 0.01523 = **0.22** at the rating; a connected rating bounds the draw from above, so the true fraction is ≥ 0.22 |

**20 K corroboration (local PDF, not ingested, 0 ARIES-CS mentions).** Miyazawa & Goto, "Development of steady-state fusion reactor by Helical Fusion", Phys. Plasmas 30, 050601 (2023), at `/home/reid/1cfe/development-of-steady-state-fusion-reactor-by-helical.pdf`: "A cooling efficiency of 2% is assumed for the cryogenic system for HTS magnets in HESTIA. The cooling efficiency is supposed to be increased from 1.5% to 2%" for 20 K helium-gas cooling. Carnot COP at 20 K / 300 K is 0.0714, so 2 % ↔ 0.28 of Carnot (1.5 % ↔ 0.21). This is a design assumption, not a measurement, but it lands in the same band as the 4.5 K plants.

**Reading.** Large helium plants sit at 0.22–0.30 of Carnot at 4.5 K and a 20 K design assumption sits at 0.21–0.28. The fraction is roughly temperature-independent at plant scale; the temperature effect belongs in the Carnot term, which the chain already has. Stellaris's 0.20 is at the conservative edge of this band at both temperatures.

**Barred-by-principle datum, seen via grep, not used.** A 25 %-of-Carnot statement for the Helios cryoplant surfaced from an unlisted duplicate of the barred Helios design paper (see Holdout disclosures). It is Helios's own assumption, not ARIES-CS data, but the artifact is barred and the value is not used here.

**Disposition.** No admissible in-repo citation. Three open sources, each ingestible via `/manage-sources`. Until one is ingested, `f_carnot_cryo` for arm-nb3sn is a disclosed hold. Recommended shape (Recommendations R2): hold the fraction equal across both arms.

### 4. Nb3Sn winding-pack current density / volume (`vol_cold_cryo`)

**Stellaris side (in-repo, authoritative extraction).** Table 8, `j_WP` per coil type: 119, 112, 120, 112, 122, 124 A/mm²; turn current 44.7–49.8 kA; coil Amp-turns 11.2–15.4 MA; winding-pack side length 300–360 mm; peak field 19.5–24.6 T (`publikationen-…/tmpissrtbos/output.md:1912-1935`; page image `tmpissrtbos/images/page_021_table_0.png` or `page_022_table_0.png` for the cross-check owed by the SOURCE_INDEX caveat). Text: "the current density per turn is about 112 A/mm²" (`:1903`). WI-024 computed `vol_cold_cryo` = 136.56 m³ from these cross-sections × 8-fold symmetry × 25 m circumference (`work/completed/20260718_WI-024_recirc-power-derivation/design.md:27`).

**In-repo candidates (admissible) — none carries a Nb3Sn number.**

- HSR4/18 and HSR5/22 (Beidler et al., IAEA; open PDF fetched, 0 ARIES-CS mentions; an extraction is not in the repo): NbTi, 10 T on coils, Ic = 37 kA, coil mass 94 t, 10 km of cable per coil, 2 × 18-turn double pancakes — NbTi, so not the comparable asked for.
- ARIES-ACT overview (`osti-servlets-purl-1178069.md:74, 344`): "peak field at the toroidal field (TF) coil of 16 T for Nb3Sn"; "overall current density exceed those projected for ITER TF and central solenoid coils, 11.8 and 13 T" — no number.
- PROCESS stellarator module (`20b-renaissance-stellarator/iter-01/sources/ukaea-process-fusion-devices-stellarator.md`): `i_tf_sc_mat = 8`, winding-pack thickness as iteration variable — a code knob, no design value.
- HELIAS module paper for systems codes (Warmer et al., MPG pure; open PDF fetched, 0 ARIES-CS mentions): scales the Helias 5-B winding pack with an ITER Nb3Sn scaling `fq = 10.9 · sqrt(fI) · (Bmax/(33 − Bmax))^{1/4}` (Eq. 6) and keeps the 5-B WP aspect ratio; the 5-B base dimensions are in Schauer, Egorov, Bykov, "HELIAS 5-B magnet system structure and maintenance concept", FED 2013 (ScienceDirect 403; a search snippet says Nb3Sn at ~12 T with a winding-pack cross-section ≈ 0.5 m² and ITER-like cable current density — unverified).

**Open source with enough to derive a number.** Demattè & Bruzzone, "Preliminary Design of a High Current R&W TF Coil Conductor for the EU DEMO" (EPFL infoscience, open PDF; 0 ARIES-CS mentions; **not ingested**), https://infoscience.epfl.ch/server/api/core/bitstreams/72370f60-ba0d-4700-a09a-56813d0eb052/content :

- Reference EU DEMO TF: "16 coils with a total current ITF = 14.9 MA, which corresponds to 142 turns for an operating current Iop = 104.95 kA (compared to 226 turns for Iop = 66 kA)"; the proposed WP is 1296 mm toroidal × 411 mm radial, "just 56 mm larger" toroidally and "∼410 mm less" radially than the reference design. Conductor sized for 12.04 T at 6.5 K.
- Derived: proposed R&W design 14.9 MA / (1296 × 411 mm²) = **28.0 A/mm²**; reference design 14.9 MA / (1240 × ~821 mm²) ≈ **14.6 A/mm²**. Both are overall winding-pack engineering densities including jacket, insulation, and fillers — the same basis as Stellaris's `j_WP`.
- Dated cross-check: the 1990 ITER CDA coil paper (OSTI 6729950, open PDF, 0 ARIES-CS mentions) says "A winding current density of 4000 A/cm² is desirable" at 12 T — i.e. 40 A/mm², the optimistic end.

**Derived Nb3Sn-arm volume.** Holding Amp-turns fixed (the study sweeps `magnet__B`, and Amp-turns scale with B in both arms alike), `vol_cold ∝ 1/j_WP`. With Stellaris's Amp-turn-weighted `j_WP` ≈ 118 A/mm²: at 28 A/mm² → 136.56 × 118/28 ≈ **575 m³** (4.2×); at 14.6 → ≈ **1100 m³** (8.1×). The nuclear heat load `q_nuc × vol_cold` and the cryoplant electrical scale with it. Caveat: a thicker winding pack also moves the coil-plasma distance and the peak/axis field ratio, which the study holds at 2.7667; the record should disclose that the Nb3Sn volume scaling is first-order only.

**Disposition.** No in-repo citation. One open-access paper gives a derivable 15–28 A/mm² band; ingestible via `/manage-sources`. Until then `vol_cold_cryo` for arm-nb3sn is a disclosed hold at 136.56 with the scaling above stated in § 17.

## Holdout disclosures

No file under `knowledge/holdout/` was opened. Every grep over `knowledge/` excluded the barred paths by pattern; two things still surfaced and must be recorded (PROTOCOL § 6):

1. **Unlisted duplicates of the barred Helios design paper.** The Helios paper (arXiv 2512.08027, "Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant") is barred at `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/**` (PROTOCOL § 3). Three further extractions of the same paper exist and are not on the list, each with 17 "ARIES-CS" mentions (counted, not read): `knowledge/concept_research/05-planar-coil-stellarator/iter-01/sources/thea-energy-helios-arxiv-2512-08027.md` (+ `/output.md`), `knowledge/concept_research/10-large-scale-stellarator/iter-02/sources/arxiv-2512-08027v1/output.md`, `knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/arxiv-2512-08027/output.md`. A corpus grep for cryoplant power returned one identical line from each (Helios's own cryoplant: 10 MW electrical at "a plausible 25% of the Carnot" efficiency). That line is Helios data, not ARIES-CS data; it is not used. Recommend the owner add the three paths to PROTOCOL § 3. The WI-031 spec's "concept dossiers 05, 10" pointer was therefore not followed into those sources.
2. **Unlisted copy of the Waganer ARIES cost-account doc.** `knowledge/concept_research/29-negative-triangularity-tokamak/iter-04/sources/qedfusion-lib-report-aries-act-ucsd-cer-13-01/output.md` is UCSD-CER-13-01, the document barred by default at `knowledge/sources/aries_cost_account_documentation/**` (7 ARIES-CS mentions, counted). The same grep returned one line from it (the Starfire helium refrigerator, 20 kW at 4.2–4.5 K). Not ARIES-CS data; not used. Recommend listing the copy under the documented-exception path.
3. The ARIES-ACT study documents used above (`osti-servlets-purl-1178069`, `osti-servlets-purl-1127358`) contain zero "ARIES-CS" strings and were treated as admissible under the bibliographic-citation rule.

## Domain References

In-repo: `defaults.py:578-593`, `CAS23_26_balance_of_plant.md:163-213`, `CAS22_plant_systems.md:222-226`, `steady_state_stellarator.yaml:21`, `physics.py:303` (all under `/home/reid/1cfe/1costingfe/`, pinned `0254385`); Stellaris `raw.pdf` p. 3 and `output.md:256, 1336, 1349, 1903, 1912-1935, 2831, 4520-4522`; W7-X Bosch 2009 `:222-226, 304-310, 799-803`; Cismondi 2017 `:176`; Kessel ARIES-ACT `:74, 175, 290, 344`; `mfe_cryo_plant.sysml:48-49`; `stellarator_plant.sysml:466-467, 573-584`; WI-024 `design.md:27, 83`.

Open web (fetched 2026-08-21, not ingested): iter.org cryogenics page and "As cold as it gets"; CERN Courier "CERN's giant fridge"; Moscato et al. SOFT 2018 preprint (scipub.euro-fusion.org WPBOP-CPR(18) 20276); Demattè & Bruzzone EU DEMO TF conductor (EPFL infoscience); Warmer et al. HELIAS module (pure.mpg.de item 2056719); Beidler et al. HSR (IAEA csp_008c ft_4); OSTI 6729950. Search-snippet only (not fetched): Dhard et al. 2015 (W7-X acceptance tests); Claudet et al. LHC Project Report 331; Schauer et al. 2013 HELIAS 5-B. Local un-ingested PDF: Miyazawa & Goto 2023 (`~/1cfe/development-of-steady-state-fusion-reactor-by-helical.pdf`).

## Modeling Insights

- The cycle preset is a three-field object upstream; anything else the study wants to vary by cycle is the study's own invention and must say so.
- The cryo chain's shape (Carnot × fraction) is validated by the evidence: the fraction clusters at 0.22–0.30 across 4.5 K and 20 K plants, so the chain can carry an A/B on `T_cold` with one shared fraction.
- Nb3Sn vs REBCO at a stellarator's 20–25 T peak fields is not a like-for-like conductor swap: the Nb3Sn arm's `B_max` = 13 T binds first, and at the fields it can reach its winding pack is 4–8× larger. The study's verdicts (`peak_field_ok`) already encode the first; the second belongs in `vol_cold_cryo` once sourced.
- The `p_pump` default is the weakest link in the stellarator power balance: every admissible helium-primary figure is 30–190× larger.

## Recommendations

- **R1 (study 2).** Hold `p_pump` = 1.0 in all three arms with the cycle-independence citation; relabel the § 17 entry from "no sCO2 source" to "cycle does not reach this value". Repoint the `eta_th` citation to the PDF page and note the paper names no cycle.
- **R2 (study 1).** Hold `f_carnot_cryo` equal in both arms (0.20 as today) and disclose; the A/B then isolates `T_cold`. If the owner wants a sourced 4.5 K value instead, ingest the iter.org cryogenics pages (or the ITER cryoplant Physics Procedia paper) and use the plant-level 0.24 — in *both* arms, to avoid a provenance mismatch inside the delta.
- **R3 (study 1).** Ingest Demattè & Bruzzone; bind arm-nb3sn `vol_cold_cryo` from the 28 A/mm² derivation (575 m³) with the 14.6 A/mm² reference (1100 m³) as the tolerance, or hold 136.56 with the scaling disclosed. The owner picks; both are honest.
- **R4 (new modeling item, not Item 6).** Re-source the stellarator `p_pump` from a helium-primary circulator basis (Moscato 2018 or Cismondi 2017) — a 2–6 % of blanket thermal power term, on the order of 60–190 MW for Stellaris. This moves `recirc_ok` and LCOE in every arm and should not be folded into the A/B.
- **R5 (holdout).** Owner to ratify adding the three Helios duplicates and the Waganer copy to PROTOCOL § 3, and log this session's two one-line grep contacts in § 6.
- **R6 (source hygiene).** Add the "simple" vs "single-element" and 560 vs 353 A/mm² discrepancies to the SOURCE_INDEX Stellaris caveat.

## Open Questions

- Which ITER 80 K figure is current (1300 kW on iter.org vs 600 kW in a secondary page)? Affects the plant-level fraction 0.19–0.24.
- W7-X actual compressor draw at 5–7 kW operation (Dhard 2015 gives a rating only).
- HELIAS 5-B winding-pack cross-section and coil Amp-turns (Schauer 2013) would give a stellarator-specific Nb3Sn `j_WP` rather than a tokamak TF one.
- Whether the Stellaris Table 8 `j_WP` row matches the page image (SOURCE_INDEX caveat; image not opened in this session).

---

**Post-approval note (2026-08-21).** The two web sources flagged "not ingested" above were ingested via `/manage-sources` the same day: `knowledge/sources/iter_cryoplant_iter_org/` (ITER cryoplant pages; DI-009) and `knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/` (Demattè & Bruzzone; DI-010). DI-009/DI-010 source fields in `knowledge/KNOWLEDGE.md` point at those paths. The W7-X acceptance-test paper, the LHC specification report, and the Moscato 2018 HCPB PHTS preprint remain un-ingested.
