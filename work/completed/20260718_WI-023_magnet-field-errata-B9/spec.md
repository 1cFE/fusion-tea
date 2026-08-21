---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-18
Updated: '2026-07-18'
---

# WI-023: Magnet-Field Errata — Rebind B = 9.0 T, Resolve the Coil-Power Phantom

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the §3 barred paths must not be read, cited, or opened. Admissible sources for this item: the Stellaris sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` (minus the barred entries) for physics, and 1costingFE (pinned `0254385`) for engineering and cost.

**Alignment brief: `work/orchestration/magnet-field-errata-B9.md`** — objective, provenance grades, owner decisions, parked questions. This spec executes that brief; the evidence authority record is the WI-022 spec §"Surfaced extraction errata" (`work/completed/20260718_WI-022_predictive-confinement/spec.md`).

## Overview

Two committed bindings rest on rows that exist only in the corrupted text extraction of the Stellaris design paper — not in the paper itself:

1. **Magnet-cost field.** `models/designs/stellarator_09/stellarator_plant.sysml:118` binds `B = 5.86` citing "Table 3 line 289 (B_0 = 5.86 T)". That row is a phantom. The real axis-averaged field is **B₀ = 9.0 T**, printed independently in the Table 2 and Table 5 images and confirmed against the published PDF (Evidence, below). Magnet cost is linear in B, and magnet is the largest capital account (42.9% at the WI-022 baseline), so this is the single largest known error in the model.
2. **Coil recirculating power.** `stellarator_plant.sysml:425` binds `p_tf = 111.0` citing "Table 2 line 235 (conduction power to coils = 111 MW)". Also a phantom: the paper prints 111 only as **stored magnetic energy [GJ]**, and contains no coil-conduction-power row at all. The owner folded this into WI-023 scope this Align, with the disposition decided by the spec-stage source sweep (Sweep Findings, below). 111 MW sits in the recirculating-power sum, so it moves p_net and q_eng directly.

The item rebinds B, rewrites every doc that names 5.86, resolves p_tf per the owner's checkpoint decision, re-baselines the headline, and holds the standing validation/regen/handshake bars.

**Baseline moved from (WI-022 executed record, `work/completed/20260718_WI-022_predictive-confinement/plan.md` Implementation Record):** p_fus 2748.1 MW, p_th 3238.1, gross 1078.3, net 804.1 MW, rec_frac 0.254, q_eng 3.93, total $9.586B, LCOE $176.07/MWh, magnet $4.117B (42.9%).

## Goals & Context

**Research questions served**:
- RQ-1 (MFE cost drivers): magnet is the dominant capital account; correcting its field input from a hallucinated 5.86 to the printed 9.0 changes the headline cost story (magnet share moves from ~43% to ~50%).
- RQ-2 (credible LCOE range): the LCOE moves by tens of $/MWh; a value resting on a phantom citation is not credible, whichever way it moves.

**Owner decisions carried in (graded in the alignment brief)**:
- [OWNER] 2026-07-18 (WI-022 errata record): the magnet-field correction is this separate follow-up item, WI-023.
- [OWNER] 2026-07-18 (Align, verbatim): *"yes do the sweep during spec stage, and include in scope all findings"* — the coil/cryo source sweep ran during this spec; all findings, the p_tf fold-in included, are in WI-023 scope.
- [OWNER] 2026-07-18 (Align): hard stop for the owner checkpoint after this spec; nothing past spec runs until scope approval.
- [OWNER] 2026-07-18 (Align): SV-016 (Q_eng ~10–40 band, `pending`) is re-flagged at close if p_tf changes.
- [OWNER] standing: no-fallbacks rule — never invent a value for a missing input; if no admissible source value exists, surface the honest options and the owner decides.

**Epic context**: instance-level correction in the WI-018 concept-09 instance; no library or generic-plant formula changes. The magnet cost formula itself (ampere-meter model, `total_kAm = G·B·R0·r_coil/(mu0·1000)`; `magnet = total_kAm · cost_per_kAm · coil_markup`) is untouched — only the B input and its documentation change.

## Current State

**The B binding and its doc carriers** (canonical `models/designs/stellarator_09/stellarator_plant.sysml`; staged twin `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` mirrors the same lines):

- Line 118: `:>> B = 5.86;` with comment (lines 116–117) citing "Table 3 line 289 (B_0 = 5.86 T)".
- Lines 82–110: the magnet-block doc — carries the phantom Table 3 citation in its **Ref** line (line 108) and the "loop-center field 5.86 T, NOT the 24.9 T peak" mapping-trap sentence (line 87). This block's r_coil arithmetic (lines 94–102) is also stale: it still shows the a = 1.5 radial-build sum (vessel_or = 3.20 m), but WI-022 rebound a = 1.3, so the actual forward-computed r_coil is 3.00 m. Found in passing at this spec; the block is rewritten wholesale anyway.
- Lines 64–70: the instance headline "THREE MAPPING TRAPS" note — names 5.86 with the WI-022-era caveat "under review as WI-023 — the Table 2/5 images print axis-averaged B_0 = 9.0 T".
- `exploration/stellarator_e2e/verify_stellaris.py:69`: oracle `magnet_B=5.86`.
- `exploration/stellarator_e2e/run_stellaris.py:244-251`: WI-022 headline asserts (total 9.59, LCOE 176, magnet 4.12) — all move.
- Generated artifacts (`generated/inputs/mfe_plant_params.json`, `generated/schemas/mfe_plant_params.py`, `stellarator.snapshot.json`) carry 5.86 as the extracted default — regenerated, not hand-edited.

**The p_tf binding**: `stellarator_plant.sysml:425-434` — `p_tf = 111.0` with a doc mapping "conduction power to coils (111 MW)" onto the coil-power slot, citing "Table 2 line 235". The oracle mirrors it (`verify_stellaris.py:66`).

**Other 5.86 carriers found (repo-wide grep)**, dispositions in Scope Boundaries: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md:30` (describes "the Stellaris SysML defaults" with b_center=5.86); `knowledge/concept_research/09-qi-stellarator-hts/iter-03/sources/analyst-patch-spec-anchors.md:25` (asserts B = 5.86 T citing "§Table 3" — same phantom lineage, plus stale a≈1.38/V=448 rows); historical work-item and report artifacts (WI-018 spec, `.project/` reports); `exploration/concept_explorer/data/09.json` (the separate 38-concept analysis track).

**Handshake safety (verified at this spec)**: `handshake_1costingfe.py` injects both affected inputs from 1costingFE's own refs — `pb__p_tf` from `pb["p_coils"]` (line 216) and `magnet__B` from `coil["b_center"]` (line 271) — so neither instance rebind can leak into the Anchor A handshake. The standing byte-identical check re-proves this at implement.

## Evidence — image-verified, now PDF-confirmed

The text extraction's Tables 2/3/4/5 are corrupted reconstructions (WI-022 finding): no quantitative table value from the text may be trusted without the page image. For B, the image evidence (verified again at this spec):

- **Table 2 image** (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_002_table_0.png`): "Axis av. magnetic field strength [T] **9.0**"; also peak conductor field 24.9 T, peak coil current 15.4 MA, 48 TF coils, stored magnetic energy **111 GJ**, peak neutron wall load 4.05 MW/m². No conduction-power row.
- **Table 5 image** (`.../images/page_009_table_0.png`): "Axis averaged B₀ [T] **9.0**" (both operating points). Independent second printed witness.
- **Table 3 image** (`.../images/page_003_table_0.png`): 8 rows, none of them a field row. The crop is right-truncated ("Valu[e]" header cut).

**Premise upgrade found during this spec's sweep.** The alignment brief recorded "5.86 is a hallucinated row" as near-certain, not absolute, because the Table 3 crop is truncated and "the original Stellaris PDF is not in the repo." The sweep found that a raw PDF of the published paper (Lion et al., FED 2025, doi 10.1016/j.fusengdes.2025.114868) **is** in the repo, inside an admissible iter-02 companion dir: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf` (KIT publikationen mirror; its own page images reproduce the Table 2 and Table 3 crops identically). Text-extracting that PDF (`pdftotext`, this spec session) settles the premise:

- The string "5.86" appears **nowhere** in the published paper.
- Table 3 has exactly the 8 rows of the image (aspect ratio 9.8 … minimum radius of curvature 0.64) — **no B row**. The caption reads "Main configuration parameters of Stellaris scaled to a minor radius of a = 1.3 m."
- "Conduction" appears twice, both as *thermal* conduction in quench contexts — **no "conduction power to coils" exists in the paper**. 111 appears in the parameter tables only as stored magnetic energy [GJ].

Both phantoms are therefore confirmed against the published paper itself, not just against truncated crops. The brief's re-check directive ("if a higher-fidelity crop or the original PDF ever surfaces, re-check") is discharged.

The existing mapping-trap distinction survives with the corrected value: the cost formula takes the **axis-averaged (loop-center) field 9.0 T**, not the 24.9 T peak-on-winding-pack (a conductor-grade concern, not a cost-quantity term).

## Sweep Findings — coil conduction / cryogenic power (owner-directed, spec stage)

**Question**: does any admissible source print a real total coil-conduction or cryo-plant power that could replace the phantom 111 MW?

**Answer: no.** No admissible source prints a total coil/cryo power in MW. What the sources actually contain:

- **Stellaris design paper** (iter-01 `stellaris-design-details.md` + images + the iter-02 raw.pdf): the paper *explicitly defers the question* — "Economic aspects — including parasitic electricity consumption and availability — are outside the scope of this paper" (conclusion/outlook; text line ~2799, PDF-confirmed). Its only quantified coil-thermal figures are densities and negligible losses, none a plant-level power:
  - Mean cryogenic nuclear heating at the winding pack **35.5 W/m³** — Table 6 image (`.../stellaris-design-details/images/page_020_table_0.png`, bottom row) and body text (§2.8, text line ~1701), with the EU DEMO ~50 W/m³ peak as the viability reference and magnets at 20 K. A heat *density*: converting it to a total electrical power needs a winding-pack volume (not printed) and a 20 K cryo-plant COP (not given) — a derivation on invented inputs, barred by the no-fallbacks rule.
  - Steady-state resistive-joint losses **~7.5 kW** for the whole coil set (§2.9, text line ~2119; PDF-confirmed) — "negligible compared to other electricity consumption and within the cooling capacity of existing cryocooler designs"; the paper adds that total nuclear heating of coils/cases/structure "will be examined in future studies."
- **iter-02 `stellaris-paper-details.md`**: same extraction lineage — it repeats the identical phantom "Conduction power to coils [MW] | 111" row at its line 235. Not a witness; contains nothing new.
- **iter-02 W7-X sources** (`en-wiki-wendelstein-7-x.md`; `pure-rest-...-content.md`, the SOFE-2009 W7-X construction paper): W7-X experiment cryo figures (~7 kW at 4.5 K equivalent capacity, 425 t cold mass). A different machine (4 K NbTi experiment vs 20 K HTS power plant); borrowing would violate the no-fallbacks rule.
- **All other admissible sources** (iter-01 Proxima technology page; iter-02 arXiv QI papers ×5, NEI magazine item, Proxima 2026 updates, the paywalled ScienceDirect power-conversion abstract; iter-03 analyst patch): no coil/cryo power content (keyword sweep over every extraction: cryo/conduction/cold mass/refrigeration/recirculating/parasitic).
- **1costingFE (engineering/cost authority, pinned `0254385`)** — a sweep find: its stellarator defaults file carries **`p_coils: 3.0` [MW] ("Coil power — complex 3D coils") at `src/costingfe/data/defaults/steady_state_stellarator.yaml:19`** — the same file the instance already takes p_cool (15.0, line 20), p_pump (21), p_trit (22), p_house (23), p_cryo (0.8, line 24), and f_sub (17) from. It is an engineering-authority default, not a Stellaris-specific value (the yaml's reference machine is R0 = 5.5 m; Stellaris is 12.7 m with 111 GJ stored).

Per the no-fallbacks rule the choice among the honest options is the **owner's, at the checkpoint** — Open Question 1 below. Every option is quantified in Success Criteria so the choice is made on stated numbers.

## Modeling Requirements

### Functional

#### MR-WI023-1: Rebind the magnet-cost field to the printed B₀ = 9.0 T

The concept-09 instance SHALL bind `magnet.B = 9.0` (axis-averaged, loop-center field), with an MR-4 citation resolving to the Table 2 and Table 5 images (and noting the raw-PDF confirmation), replacing the phantom Table 3 text-row citation. The doc SHALL retain the mapping-trap distinction: the cost formula takes the axis-averaged 9.0 T, NOT the 24.9 T peak-conductor field printed beside it in Table 2.

- **Type**: Functional / correction | **Priority**: Must | **Derives from**: [OWNER] WI-023 registration; RQ-1/RQ-2; capture-fidelity correction rule
- **Validation**: SV-030; run_stellaris bit-exact vs oracle (rel 1e-9)

> **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
> **Ref**: Table 2 image (images/page_002_table_0.png: "Axis av. magnetic field strength [T] 9.0"); Table 5 image (images/page_009_table_0.png: "Axis averaged B₀ [T] 9.0", Points A and B); phantom refuted against knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf (published FED 2025 paper: no "5.86" anywhere; Table 3 has no field row)
> **Basis**: Stellaris axis-averaged on-axis field; the ampere-meter magnet cost model takes the loop-center field

#### MR-WI023-2: Rewrite every 5.86-naming doc; delete the phantom citation everywhere

The change SHALL rewrite, in the same change, every live artifact that names 5.86 or the phantom Table 3 row: the instance "THREE MAPPING TRAPS" headline note (`stellarator_plant.sysml:64-70` — the "under review as WI-023" caveat resolves to the corrected statement), the magnet-block doc (lines 82–110 — phantom **Ref** line replaced; the stale a = 1.5 / vessel_or = 3.20 m arithmetic refreshed to the actual a = 1.3 / 3.00 m build), the B binding comment (lines 116–117), the staged twin (same lines), the oracle (`verify_stellaris.py:69` `magnet_B=9.0`), and the runner headline asserts (`run_stellaris.py:244-251` — retargeted to the re-baselined values). Generated artifacts pick up 9.0 through regen, never hand-edits. Per the capture-fidelity correction rule, the phantom citation is deleted, not annotated around; the WI-022-era "under review" framing is removed.

- **Type**: Traceability / correction | **Priority**: Must | **Derives from**: capture-fidelity correction rule; alignment brief objective
- **Validation**: doc inspection at review; repo grep for "5.86" finds no live model/pipeline carrier

#### MR-WI023-3: Rescope p_tf to 0 — the source defers the value ([OWNER] checkpoint ruling, 2026-07-18)

**Owner ruling at the spec checkpoint: option (b).** The instance SHALL rebind `p_tf = 0.0`, deleting the phantom "Table 2 line 235" citation. The binding's doc SHALL state plainly: the Stellaris paper explicitly defers parasitic electricity consumption ("outside the scope of this paper", conclusion, raw.pdf-confirmed); its only coil-thermal figures (35.5 W/m³ winding-pack heat density, ~7.5 kW joint losses) are not convertible to a plant-level MW without invented inputs; the model carries no invented value (no-fallbacks rule). The doc SHALL NOT cite the Stellaris paper for any MW value and SHALL point forward to the backlog item that will derive these power values properly (see Open Question 1 ruling). The oracle (`verify_stellaris.py:66`) and runner asserts move with it (p_net 915.2, q_eng 6.61, LCOE $201.46 expected).

- **Type**: Functional / correction | **Priority**: Must | **Derives from**: [OWNER] checkpoint ruling 2026-07-18 (option b); [OWNER] standing no-fallbacks rule
- **Validation**: SV-030 (headline recorded per disposition); citation inspection at review; SV-016 re-flag at close if the value changed

### Constraint

#### MR-WI023-4: Standing bars hold — validation, regen, execute, handshake, mirroring

The change SHALL hold the inherited bars: L1 = 0 and L2–L5 pass with L6 exactly the 6 pre-existing offenders (3 MFE cross-part rollups, 2 IFE unbound attrs, 1 hif_plant binding — zero new); regen via the `~/1cfe/sysml-codegen` snapshot + `bridge_v11_generate.py` with `preserve_handwritten=True` surviving (the WI-022 handwritten reactivity impl must survive this regen); `run_stellaris.py` bit-exact vs the updated oracle at rel 1e-9; the Anchor A handshake byte-identical (`handshake_1costingfe.py` unedited, empty `git diff` on `handshake_comparison.json` — the injections at lines 216 (`pb__p_tf`) and 271 (`magnet__B`) keep both corrections out of the anchor); canonical↔staged mirroring discipline (shared regions byte-identical).

- **Type**: Constraint | **Priority**: Must | **Derives from**: [INHERITED: handoff] working bars; WI-022 MR-WI022-4/5/6 pattern
- **Validation**: SV-030; SV-025/026 byte-identical; L1–L6 vs baseline; IFE regression SV-023 unchanged

### Traceability

#### MR-WI023-5: Citations, clean-room

Every changed value and doc SHALL carry an MR-4 `Source / Ref / Basis` citation resolving to an admissible Stellaris source **image** (never an extracted-text table row) or to 1costingFE at `0254385`. No ARIES-CS-informed source may be cited or read (PROTOCOL.md §3).

- **Type**: Traceability | **Priority**: Must | **Derives from**: MR-4; PROTOCOL.md §3; WI-022 errata lesson (text tables untrustworthy)
- **Validation**: citation inspection at review

## Scope Boundaries

**In scope**
- `models/designs/stellarator_09/stellarator_plant.sysml` — B rebind + all doc rewrites (MR-WI023-1/2); p_tf resolution (MR-WI023-3).
- `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` — staged twin, same edits.
- `exploration/stellarator_e2e/verify_stellaris.py` (oracle `magnet_B`, `p_tf`), `run_stellaris.py` (headline asserts), regenerated pipeline artifacts.
- `modeling_project/VALIDATION_MATRIX.md` — SV-030 (created by this spec, status pending).
- `exploration/stellarator_e2e/HANDSHAKE_REPORT.md:30` — dated update note appended below the b_center = 5.86 sentence ([OWNER] Q3 ruling: annotate below, don't rewrite the original).
- `knowledge/concept_research/09-qi-stellarator-hts/iter-03/sources/analyst-patch-spec-anchors.md` — phantom-lineage annotation ([OWNER] Q2 ruling).

**Out of scope**
- The magnet cost formula, library files, and the generic plant — no formula changes anywhere.
- Historical records that name 5.86 as the then-current state (WI-018 spec, `.project/` reports, WI-022 artifacts): records of past state, not live instructions; left as history.
- `exploration/concept_explorer/data/09.json` — the separate 38-concept analysis track; not the demo model.
- Deriving the recirculating power values (coil conduction, cryo-electrical from heat loads + COP) — captured as its own backlog item per the [OWNER] Q1 ruling; WI-023 binds p_tf = 0 with the deferral documented.
- Recomputing the STALE-BASIS pass-throughs (buildings/preconstruction/O&M) — annotations move with the new headline; recomputation stays the Stage-3 account-scope item.

## Success Criteria

Expected numbers below were computed at this spec by running the WI-022 oracle (`verify_stellaris.py`) with `magnet_B = 9.0` — exact under the current formulas, since magnet cost is linear in B and nothing else reads it.

1. **SV-030 (corrected-B headline)**: magnet capital = **$6.3235B** (= $4.1173B × 9.0/5.86), bit-exact vs oracle at rel 1e-9, magnet share ≈ **50.2%**. With p_tf unchanged (111 MW): total **$12.6015B**, LCOE **$229.27/MWh**, p_net 804.1 / q_eng 3.93 unchanged. If the owner changes p_tf: p_tf = 0 → p_net 915.2, q_eng 6.61, LCOE $201.46; p_tf = 3.0 → p_net 912.2, q_eng 6.49, LCOE $202.12 (total capital is unchanged by p_tf). Implement records the executed values for the ratified disposition.
2. **SV-025 / SV-026 byte-identical** — `handshake_comparison.json` empty `git diff`; zero edits to `handshake_1costingfe.py`.
3. **Validation L1–L6** vs the WI-022 baseline: L1 = 0, L2–L5 pass, L6 = the same 6 pre-existing offenders, zero new; IFE regression SV-023 unchanged; viability (beta / wall load / TBR) unchanged — none reads magnet B (verified: beta binds the printed 0.0276; no power-balance channel reads B).
4. **The WI-022 handwritten reactivity impl survives the regen** (`preserve_handwritten=True`) and the pipeline stays bit-exact vs oracle at rel 1e-9.
5. **No live 5.86 carrier remains** in model/pipeline files (grep-clean outside historical records and the separate analysis track); the re-baselined headline is recorded in the work item and `.project/CURRENT_WORK.md`.

**Note on the brief's hand estimate (surfaced, not silently corrected):** the alignment brief's expected movement (≈$11.8B total, ≈$215/MWh, ≈53% share — [AGENT] hand estimate) under-counted the rollup: the +$2.206B magnet delta also carries contingency (10%) and time-scaled indirect (26.67%), so the oracle-computed movement is **total $12.60B, LCOE $229.27/MWh at p_tf = 111, share 50.2%**. Magnet $6.32B matches the estimate. The brief itself marks the estimate agent-grade with "implement produces exact numbers"; these are the exact numbers under the current formulas.

## Open Questions — resolved at the owner checkpoint ([OWNER] 2026-07-18)

1. **p_tf disposition — ruled: option (b), rescope to 0.** The sweep found no sourced Stellaris value (the paper defers parasitic electricity consumption; its only coil-thermal numbers are the 35.5 W/m³ winding-pack heat density and ~7.5 kW joint losses). Ruling recorded in MR-WI023-3. Expected movement: q_eng 6.61, LCOE $201.46; optimistic until a real derivation lands (p_tfcool 15 MW and p_cryo 0.8 MW, both 1costingFE-sourced, still carry some coil-adjacent load). *Rejected alternatives, recorded: (a) keep 111 MW as a phantom-sourced placeholder; (c) bind the 1costingFE 5.5 m-reference default `p_coils = 3.0 MW` — unrepresentative of a 12.7 m / 111 GJ coil set.* **The owner additionally directed a future-work capture: derive/decompose and model how these power values are actually derived** (coil conduction, cryo-plant electrical from heat loads and COP, parasitic loads) rather than binding constants — registered as a backlog item in the MFE epic (see Related Artifacts).
2. **Analyst patch — ruled: annotate.** WI-023 SHALL annotate `knowledge/concept_research/09-qi-stellarator-hts/iter-03/sources/analyst-patch-spec-anchors.md` (its line 25 B = 5.86 assertion, plus its stale a≈1.38 / V=448 rows) as phantom-lineage / superseded, pointing to the image evidence and this item. Moved into In Scope.
3. **`HANDSHAKE_REPORT.md:30` — ruled: add an update note below the sentence for traceability** (do not rewrite the original WI-019-era sentence; append a dated correction note). Moved into In Scope.
4. **Publikationen PDF registration — ruled: register.** The owner initiated a `/manage-sources` registration of the publikationen extraction in `SOURCE_INDEX.md` (runs alongside this item, not part of WI-023's model change).

## Assumptions & Risks

1. **This re-baselines the headline upward** (certain, accepted): magnet +$2.21B → total +$3.02B after rollup; LCOE +$53/MWh at p_tf = 111 (partly offset to +$25–26 if p_tf drops per Open Question 1). The demo's honest-correction story is the point: the model moves to what the source actually prints.
2. **Table 3 premise** — settled. Was "near-certain" (truncated crop); now confirmed against the published PDF text (no "5.86", no B row, no conduction-power row anywhere in the paper). Residual risk effectively zero.
3. **SV-016 (Q_eng ~10–40 band, `pending`)**: options (b)/(c) move q_eng 3.93 → ~6.5–6.6, still below the band; option (a) leaves it at 3.93. Per the owner's Align decision, re-flag SV-016 at close if p_tf changes; do not self-resolve.
4. **Viability decoupling** (verified): beta binds the printed 0.0276 and no power-balance or viability channel reads magnet B — correction 1's blast radius is exactly magnet capital → powercore → direct/contingency/indirect/total → LCOE, plus the 5.86-naming docs. Correction 2 adds recirc → p_net → q_eng → LCOE denominator.
5. **Stale-doc drift** (low): the magnet-block doc carried stale a = 1.5 arithmetic from before WI-022; MR-WI023-2 rewrites the block wholesale. If other stale doc arithmetic surfaces during implement, surface it at close rather than silently expanding scope.

## Traceability

**Sources**
- `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` + `stellaris-design-details/images/`: Table 2 image `page_002_table_0.png` (axis-av. 9.0 T; peak conductor 24.9 T; 48 coils; 111 GJ stored; wall load 4.05); Table 5 image `page_009_table_0.png` (axis-averaged B₀ 9.0, Points A/B); Table 3 image `page_003_table_0.png` (8 rows, no field row); Table 6 image `page_020_table_0.png` (mean cryogenic nuclear heating 35.5 W/m³); §2.8 text ~line 1701 (35.5 W/m³, 20 K, EU DEMO reference), §2.9 text ~line 2119 (7.5 kW joint losses), conclusion ~line 2799 (parasitic electricity out of the paper's scope).
- `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf` — the published paper (FED 2025, doi 10.1016/j.fusengdes.2025.114868); confirms both phantoms absent; its images reproduce the Table 2/3 crops.
- `/home/reid/1cfe/1costingfe` @ `0254385`: `src/costingfe/data/defaults/steady_state_stellarator.yaml:19` (`p_coils = 3.0`, Open Question 1c); the magnet cost formula lineage (cas22 ampere-meter model) unchanged.

**Downstream impacts**: WI-018 instance (B binding + docs), staged twin, oracle + runner, regenerated pipeline artifacts, VALIDATION_MATRIX SV-030 (+ SV-016 re-flag at close if p_tf changes), headline in `.project/CURRENT_WORK.md`, `HANDSHAKE_REPORT.md:30` (Open Question 3).

**Applicable project rules**: MR-4 (citations), PROTOCOL.md §3 (clean-room; this spec's sweep read only admissible sources), no-fallbacks (p_tf options surfaced, not chosen), capture-fidelity correction (phantom citations deleted, not annotated around) and surfacing (hand-estimate deviation, PDF premise upgrade, and p_tf choice all surfaced above).

## Related Artifacts

- Alignment brief: `work/orchestration/magnet-field-errata-B9.md`
- Evidence authority record: `work/completed/20260718_WI-022_predictive-confinement/spec.md` §"Surfaced extraction errata"
- Executed baseline: `work/completed/20260718_WI-022_predictive-confinement/plan.md` Implementation Record
- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Handshake: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`
- Design: `work/active/WI-023_magnet-field-errata-B9/design.md` (to be created after the owner checkpoint)
- Plan: `work/active/WI-023_magnet-field-errata-B9/plan.md` (to be created)
