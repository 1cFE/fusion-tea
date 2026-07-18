---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
---

> Process note: per the owner-ratified item process, the single owner checkpoint sits after
> `/spec-model`. That checkpoint ran 2026-07-18 and ratified the full scope, including
> MR-WI023-3 (p_tf = 0.0, option b), Q2 (annotate the analyst patch), Q3 (dated note below
> HANDSHAKE_REPORT.md:30), and Q1's future-work capture (WI-024, registered in the backlog).
> Design → plan → implement → close proceed without a further stop.

# WI-023 Design: Magnet-Field Errata — B = 9.0 T, p_tf = 0.0

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. Physics evidence from the admissible Stellaris sources (Table 2/5/3 images + the iter-02 raw.pdf); engineering/cost from 1costingFE @ `0254385`.

## Overview

No structure changes. This item is two literal rebinds in the concept-09 instance (`models/designs/stellarator_09/stellarator_plant.sysml`) plus the doc rewrites, mirroring, oracle/runner re-baseline, regen, and two annotation edits the spec directs — the WI-020 shape (bindings + doc rewrite + oracle/runner re-baseline), smaller.

1. **`magnet.B` 5.86 → 9.0** (line 118). The phantom "Table 3 line 289" citation is deleted; the new citation resolves to the Table 2 and Table 5 images (two independent printed witnesses of axis-averaged B₀ = 9.0 T), with the raw.pdf refutation noted. Magnet cost is linear in B (`total_kAm = G·B·R0·r_coil/(mu0·1000)`), so magnet capital scales exactly ×9.0/5.86 to **$6.3235B** and the rollup carries it to **total $12.6015B**, share **50.2%**.
2. **`pb.p_tf` 111.0 → 0.0** (line 425, [OWNER] option b). The phantom "conduction power to coils" citation is deleted; the doc states the honest deferral (the paper prints 111 only as stored magnetic energy [GJ] and defers parasitic electricity consumption) and points forward to WI-024. Moves **p_net 804.1 → 915.1 MW, q_eng 3.93 → 6.61, LCOE $176.07 → $201.46/MWh**.

Both corrections are handshake-safe by construction: `handshake_1costingfe.py` injects `magnet__B` from `coil["b_center"]` (line 271) and `pb__p_tf` from `pb["p_coils"]` (line 216), so the Anchor A comparison never sees the instance values. Zero handshake edits; SV-025/026 byte-identical is the gate.

## Research Findings

**Expected headline is oracle-exact, computed this session** (scratch copy of `verify_stellaris.py` with `magnet_B = 9.0`, `p_tf = 0.0`; the unmodified oracle first reproduced the WI-022 baseline to the cent — total $9,586,395,493.62, LCOE 176.0743, magnet $4,117,281,542.84 / 42.95%):

| quantity | WI-022 baseline | WI-023 expected | moved by |
|---|---|---|---|
| magnet capital | $4,117,281,542.84 | **$6,323,469,946.33** ($6.3235B) | B (exactly ×9.0/5.86 = 1.535836177) |
| magnet share | 42.95% | **50.18%** | B |
| total capital | $9,586,395,493.62 | **$12,601,519,645.07** ($12.6015B) | B only (p_tf touches no capital account) |
| p_net | 804.145 MW | **915.145 MW** | p_tf (recirc drops 111 MW) |
| rec_frac | 0.2542 | **0.1513** | p_tf |
| q_eng | 3.933 | **6.609** | p_tf |
| LCOE | $176.07/MWh | **$201.458/MWh** | both (capital ↑, denominator energy ↑) |
| V, p_fus, p_th, p_et, wall_load | 425.0 / 2748.06 / 3238.1 / 1078.3 / 3.131 | unchanged | — (nothing upstream reads B or p_tf) |

These match the spec's Success Criteria numbers exactly. The intermediate case (B = 9.0, p_tf = 111) also reproduced the spec's $12.6015B / $229.27 — confirming total capital is p_tf-invariant.

**Carrier inventory** (grep `5\.86` + `p_tf`, current at `cef74e8e`):

| carrier | lines | change |
|---|---|---|
| `stellarator_plant.sysml` (canonical) | 49–62 headline block; 64–70 mapping-traps note; 82–110 magnet doc; 116–118 B comment+binding; 122–125 r_coil comment (stale 3.20 — see D3); 425–434 p_tf | rebinds + doc rewrites (below) |
| staged twin `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` | same line numbers | identical edits (D4) |
| `stellarator_plant.sysml` 498, 542 | two P_net STALE BASIS blocks (804.1) | append the WI-023 move to 915.1 (annotation only; buildings block at 259 keys on p_et/p_th, which don't move — untouched) |
| `verify_stellaris.py` | 66 (`p_tf=111.0`), 69 (`magnet_B=5.86`) | oracle inputs → 0.0 / 9.0 |
| `run_stellaris.py` | 232–251 headline comment + asserts | retarget (below) |
| generated: `mfe_plant_params.json:17` + `mfe_plant_params.py:24` (`magnet__B` 5.86); `system_design.json:42` + `system_design.py:52` + `pipelines/mfe_stellarator.yaml` (`pb__p_tf` 111.0); `stellarator.snapshot.json` literals | — | **regen only, never hand-edited** |
| `HANDSHAKE_REPORT.md:30` (`b_center=5.86`) | — | dated note appended below ([OWNER] Q3) |
| `analyst-patch-spec-anchors.md` | 25 (B 5.86), 26 (V 448), 27 (a≈1.38 derived) | phantom-lineage/superseded annotation ([OWNER] Q2) |
| `.project/CURRENT_WORK.md:15` | history/queue record | updated at close (headline record), not a model carrier |
| `work/completed/**`, WI-018 spec, `.project/` reports, `exploration/concept_explorer/data/09.json` | — | out of scope (historical records / separate analysis track, per spec) |

**Mirroring is trivial here**: a full-file diff of canonical vs staged shows exactly one divergence — the staged copy's commented-out viability-assert block (canonical 609–621 vs staged 609–614, a known staged-only codegen adaptation). Every WI-023 edit region is shared and byte-identical today, at the same line numbers. Simple Edit-per-region on both files; post-edit diff must again show only the assert block.

**Baseline validation state re-confirmed this session**: `uv run agentic-mbse validate models --level 1` → 21 files, 0 errors, 0 warnings.

**WI-024 is registered** (`work/BACKLOG.md`: "Recirculating-power derivation model (coil/cryo parasitic loads)", standard, backlog) — the p_tf doc's forward pointer resolves.

## Design Decisions

**D1 — pure rebind; no formula, library, or generic-plant change.** The ampere-meter magnet model and the power-balance recirc sum are untouched; only two instance literals and their docs move. This is the spec's epic-context constraint, and it keeps the blast radius exactly the spec's verified map: B → magnet → powercore → direct/contingency/indirect → total → LCOE; p_tf → recirc → p_net/q_eng → LCOE denominator.

**D2 — p_tf = 0.0 documented as a deferral, cited to the deferral.** The binding's doc states what the source actually supports: the paper defers parasitic electricity consumption ("outside the scope of this paper", conclusion, raw.pdf-confirmed); its only coil-thermal figures (35.5 W/m³ winding-pack heat density, ~7.5 kW joint losses) are not convertible to a plant-level MW without invented inputs; the model binds 0.0 rather than an invented value (no-fallbacks rule, [OWNER] option b). The MR-4 citation resolves to the raw.pdf (deferral sentence) and the Table 2 image (111 = stored magnetic energy [GJ], no conduction-power row) — evidence of absence, never a MW value, satisfying MR-WI023-3's "SHALL NOT cite the Stellaris paper for any MW value". The doc names the known-optimistic direction and points to WI-024. Rejected (owner-recorded in the spec): keeping 111 as a phantom placeholder; binding the 1costingFE 5.5 m-reference `p_coils = 3.0`.

**D3 — the magnet-block rewrite also refreshes the stale `r_coil = 3.20 m` comment (lines 122–125).** MR-WI023-2 directs refreshing "the stale a = 1.5 / vessel_or = 3.20 m arithmetic" in the magnet doc (lines 94–102); the same stale 3.20 appears once more in the r_coil binding comment three lines below (found at design — it names 3.20, not 5.86, so the spec's grep missed it). Refreshing both to the actual a = 1.3 / vessel_or = 3.00 m build is the same directed correction, not new scope; surfaced in the design report per spec Risk 5.

**D4 — headline doc block (lines 49–62) re-baselines in the same rewrite.** The mapping-traps note (64–70) is the spec's named target, but it sits inside the same instance doc comment as the HEADLINE FORWARD-PASS RESULT block, which states the WI-022 numbers ($9.59B / $176.07 / magnet 42.9%) that this item moves. WI-022 precedent (its plan Phase 3) refreshes the headline block with the executed values and appends one history line; spec Success Criterion 5 requires the re-baselined headline recorded. Final numbers land at implement from the executed run.

**D5 — regen only for generated artifacts; oracle is the reference implementation.** Sequence at implement: edit models (both copies) → validate → snapshot + `bridge_v11_generate.py` (confirm `preserve_handwritten=True` still set and the WI-022 `dt_fusion_power_impl.py` survives — the WI-022 record's gotcha: preservation is by file existence, so verify the impl content, not just presence) → update oracle inputs → retarget runner asserts → run bit-exact. No hand-edit of anything under `generated/` or the snapshot.

**D6 — annotations append; originals stay.** Both annotation targets are records, not live docs, so the correction rule's "delete the phantom" applies only to the model/pipeline files. `HANDSHAKE_REPORT.md:30` keeps its WI-019-era sentence and gains a dated update note directly below ([OWNER] Q3, verbatim ruling). `analyst-patch-spec-anchors.md` keeps its table and gains a clearly-dated errata section flagging the B row as phantom-lineage and the V/a rows as stale, pointing to the image evidence and WI-023 ([OWNER] Q2).

## Proposed Design

### 1. Instance edits (`stellarator_plant.sysml`, canonical + staged identical)

**B binding + comment (116–118):**

```sysml
// Axis-averaged (loop-center) field [T]. Source: Table 2 image
//   (page_002_table_0.png: "Axis av. magnetic field strength [T] 9.0") and
//   Table 5 image (page_009_table_0.png: "Axis averaged B_0 [T] 9.0", Points
//   A and B). NOT the 24.9 T peak-on-winding printed beside it in Table 2.
:>> B = 9.0;
```

**Magnet-block doc (82–110), rewritten wholesale.** Contents: (a) the B mapping trap restated at 9.0 — cost formula takes the axis-averaged loop-center field, not the 24.9 T peak-conductor field; (b) the phantom history compressed to one line (the prior 5.86 cited a Table 3 text row absent from the table image and from the published paper — raw.pdf-confirmed, WI-023); (c) the r_coil trap with refreshed arithmetic:

```
vessel_or = a + vacuum_t + firstwall_t + blanket_t + reflector_t
            + ht_shield_t + structure_t + gap1_t + vessel_t
          = 1.3 + 0.10 + 0.05 + 0.80 + 0.20 + 0.20 + 0.15 + 0.10 + 0.10
          = 3.00 m
```

with a = 1.3 m cited to the Table 2 image (WI-022 errata rebind) and the layer-sum formula verified against `costingfe.layers.geometry` (geometry.py:106-114); (d) the **Ref** line's phantom entry replaced by the Table 2 + Table 5 image refs and the raw.pdf refutation note. The r_coil binding comment (122–125) updates 3.20 → 3.00 (D3). MR-4 stencil for the block:

```
**Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
**Ref**: Table 2 image (images/page_002_table_0.png: axis av. field 9.0 T; peak
    conductor 24.9 T); Table 5 image (images/page_009_table_0.png: axis-averaged
    B_0 9.0 T, Points A/B); phantom 5.86 refuted vs knowledge/concept_research/
    09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/
    tmpissrtbos/raw.pdf (no "5.86" in the published paper; Table 3 has no field
    row); geometry.py:106-114 (vessel_or layer sum);
    steady_state_stellarator.yaml:39-42 (thicknesses)
**Basis**: coil bore = radial-build vessel_or; axis-averaged on-axis field for cost
```

**p_tf binding + doc (425–434):**

```sysml
:>> p_tf = 0.0 {      // coil recirculating power [MW] — source defers; no invented value (WI-023).
    doc /*
    Coil-system recirculating power: bound 0.0 because no admissible source
    prints one. The prior 111.0 mapped a "conduction power to coils" text row
    that does not exist in the paper — the published Stellaris paper prints
    111 only as stored magnetic energy [GJ] (Table 2 image) and explicitly
    defers parasitic electricity consumption ("outside the scope of this
    paper", conclusion; raw.pdf-confirmed). Its only coil-thermal figures —
    35.5 W/m^3 winding-pack nuclear-heating density (Table 6 image) and
    ~7.5 kW resistive-joint losses (sec. 2.9) — are not convertible to a
    plant-level MW without invented inputs (winding-pack volume, 20 K cryo
    COP), so per the no-fallbacks rule the slot carries no invented value
    ([OWNER] ruling 2026-07-18). Known-optimistic until WI-024 (backlog:
    recirculating-power derivation from heat loads + COP) lands; p_tfcool
    (15 MW) and p_cryo (0.8 MW), both 1costingFE-sourced, still carry some
    coil-adjacent load.
    **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
    **Ref**: conclusion (parasitic electricity consumption outside the paper's scope); Table 2 image (iter-01 .../stellaris-design-details/images/page_002_table_0.png: 111 = stored magnetic energy [GJ]; no conduction-power row)
    **Basis**: deferred by the source; 0.0 pending the WI-024 derivation — cites no MW value
    */
}
```

**Headline doc (49–62)**: re-baselined to the executed WI-023 numbers (expected: net 915.1 MW, rec_frac 0.151, q_eng 6.61, total $12.60B, LCOE $201.46, magnet $6.32B / 50.2%; p_fus/p_th/V unchanged), history line appended: WI-022 values moved to history; WI-023 rebound the magnet field to the printed 9.0 T (5.86 was a phantom row) and zeroed the phantom p_tf = 111 (stored energy in GJ, not a power).

**Mapping-traps note (64–70)**: the B trap resolves to its corrected statement — coil-cost field is the axis-averaged 9.0 T (Table 2/5 images), NOT the 24.9 T peak-on-winding; the "under review as WI-023" caveat is deleted (the review is this item, done). r_coil and sigma_v traps unchanged.

**STALE BASIS blocks (498, 542)**: append the WI-023 move (P_net now 915.1) in the established "updated WI-0xx" style; recomputation stays Stage-3. Buildings block (259) untouched — its basis is p_et/p_th, which this item does not move.

### 2. Oracle + runner (`exploration/stellarator_e2e/`)

- `verify_stellaris.py:66` → `p_tf=0.0` (comment: source defers, WI-023 / WI-024); line 69 → `magnet_B=9.0` (comment: Table 2/5 images).
- `run_stellaris.py:232–241` comment block rewritten for WI-023 (what moved and why, with the WI-022 values as the "was" line); asserts (243–251) retargeted:

```python
heads = [
    ("plasma volume V [m3]", b[CH["V"]], 425, 2),
    ("fusion power [MW]", b[CH["p_fus"]], 2748.1, 2),
    ("net electric [MW]", b[CH["p_net"]], 915.1, 3),
    ("rec_frac", b[CH["rec_frac"]], 0.151, 0.01),
    ("q_eng", b[CH["q_eng"]], 6.61, 0.05),
    ("total capital [$B]", total / 1e9, 12.60, 0.05),
    ("LCOE [$/MWh]", b[CH["lcoe"]], 201.5, 2),
    ("magnet capital [$B]", b[CH["magnet"]] / 1e9, 6.32, 0.05),
]
```

(Loose sanity band, same style as WI-022; the real gate stays the per-channel rel-1e-9 bit-exact compare vs the oracle.)

### 3. Regen

Snapshot from the staged models via the `~/1cfe/sysml-codegen` flow + `bridge_v11_generate.py` (verify `preserve_handwritten=True` still in `GenerationConfig`). Post-regen checks: `mfe_plant_params.json` carries `magnet__B: 9.0`; `system_design.json` carries `pb__p_tf: 0.0`; `dt_fusion_power_impl.py` content unchanged (`AUTO_IMPLEMENTED = False` intact); V11 offenders unchanged.

### 4. Annotations

**`HANDSHAKE_REPORT.md`** — appended directly below line 30:

> **Update (WI-023, 2026-07-18):** the b_center = 5.86 T above was an extraction phantom (text-only Table 3 row; the Table 2/5 images and the published paper print axis-averaged B₀ = 9.0 T) — the instance now binds 9.0. Likewise p_tf = 111 MW mapped a nonexistent "conduction power to coils" row (111 is the stored magnetic energy in GJ); the instance now binds 0.0 (source defers the value; WI-024). The handshake is unaffected by construction: `magnet__B` and `pb__p_tf` are injected from 1costingFE's own refs, and the comparison below stands unchanged.

**`analyst-patch-spec-anchors.md`** — dated errata section appended below the "Verified spec values" table (rows untouched):

> **Errata (WI-023, 2026-07-18 — phantom-lineage / superseded rows):** the `B` = 5.86 T row cites a Table 3 text row that does not exist — the Table 3 image (`.../stellaris-design-details/images/page_003_table_0.png`) has no field row, and the published paper (iter-02 publikationen raw.pdf) contains no "5.86"; the Table 2/5 images print axis-averaged B₀ = **9.0 T**. The `plasma_volume` = 448 m³ and derived `plasma_t` ≈ 1.38 m rows are stale extraction artifacts: the images print V = **425 m³**, a = **1.3 m** (WI-022 errata record). See `work/active/WI-023_magnet-field-errata-B9/spec.md` §Evidence.

## Cross-File Bindings

No binding graph changes — the generic plant's `magnet.B` and `pb.p_tf` wiring is untouched; only the instance literals move. Dataflow stays unidirectional. Handshake injections (unchanged, the safety proof): `magnet__B` ← `coil["b_center"]` (`handshake_1costingfe.py:271`), `pb__p_tf` ← `pb["p_coils"]` (line 216).

## Validation Plan

1. **L1** after each model edit (baseline re-confirmed this session: 21 files, 0 errors). Full **L1–L6** after the instance edits: L1 = 0, L2–L5 pass, L6 = exactly the 6 pre-existing offenders (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`), zero new. (`uv run agentic-mbse validate models --level N`; syside has no CLI in this venv. `SYSIDE_LICENSE_KEY` via `set -a && source ~/1cfe/fusion-tea/.env && set +a`.)
2. **Mirroring**: full-file diff canonical vs staged after edits — only the known viability-assert divergence remains.
3. **Regen**: params carry 9.0 / 0.0; WI-022 handwritten impl survives (content-verified); V11 offenders unchanged.
4. **Execute**: `run_stellaris.py` (executor `/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`) bit-exact vs the updated oracle at rel 1e-9 on every channel/account/LCOE; headline asserts green at the Research Findings table's values; magnet exactly ×9.0/5.86 vs the WI-022 record.
5. **Handshake**: `handshake_1costingfe.py` unedited; `handshake_comparison.json` empty `git diff` (SV-025/026 byte-identical).
6. **Regressions**: IFE SV-023 unchanged (no IFE files touched); viability unchanged (beta 0.0276, wall load 3.131 < 4.05, TBR — none reads B or p_tf).
7. **SV-030** (`modeling_project/VALIDATION_MATRIX.md:56`, pending) → passing at close with executed values; **SV-016 re-flagged at close** (q_eng 3.93 → 6.61, still below the ~10–40 band; owner adjust/annotate, not self-resolved).
8. Grep gate: no live `5.86` carrier in model/pipeline files (historical records and the concept-explorer track exempt, per spec).

## Validation Report (design-stage)

- **Oracle prototype: PASS.** Scratch harness (`scratchpad/wi023/headline.py`, session scratch — no repo file touched) reproduced the WI-022 baseline exactly, then computed the WI-023 point: magnet $6,323,469,946.33 (ratio vs baseline = 1.5358361774744025 = 9.0/5.86 to the last ulp), total $12,601,519,645.07, p_net 915.1454 MW, q_eng 6.6093, rec_frac 0.15130, LCOE $201.4579/MWh, share 50.18%, V/p_fus/p_th/wall_load unchanged. Matches the spec's Success Criteria and SV-030's expected values exactly.
- **Baseline L1: PASS** (21 files, 0 errors, 0 warnings — read-only check, this session).
- **Mirroring precondition: PASS** — canonical vs staged diff shows only the known staged-only assert block; all edit regions byte-identical at identical line numbers.
- No new SysML constructs are introduced (literal rebinds inside existing `:>>` redefinitions), so no parse-risk stencil beyond the existing forms was needed.

## Implementation Checklist

1. **Instance edits (canonical)** — B binding + comment; magnet-block doc (incl. r_coil 3.00 refresh, D3); p_tf binding + doc; headline block + mapping-traps note; two STALE BASIS appends. L1.
2. **Mirror to staged twin** — same regions; diff-verify only the assert-block divergence remains. L1–L6 full compare vs baseline.
3. **Regen** — snapshot + V11 bridge; verify params (9.0 / 0.0), handwritten-impl survival, offender count.
4. **Oracle + runner** — `verify_stellaris.py` inputs; `run_stellaris.py` comment + asserts; execute bit-exact.
5. **Handshake + regressions** — re-run handshake (zero edits, empty diff on `handshake_comparison.json`); SV-023; viability.
6. **Annotations** — HANDSHAKE_REPORT dated note; analyst-patch errata section.
7. **Close-out** — SV-030 passing with executed values; SV-016 re-flag; headline recorded in the work item and `.project/CURRENT_WORK.md`; `/status` close.

## Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| Executed numbers differ from the design-stage oracle run | very low | low | the same oracle is the implement-stage gate; runner asserts carry tolerance bands and the record takes executed values |
| Regen clobbers the WI-022 handwritten impl | low | high | `preserve_handwritten=True` verified pre-regen; impl **content** (not just existence) checked post-regen — the WI-022 record's stale-auto-impl gotcha |
| Handshake accidentally changes | very low | high | zero handshake edits; empty-git-diff gate on `handshake_comparison.json` |
| Stale-doc drift beyond the mapped carriers | low | low | one instance found and folded at design (r_coil 3.20, D3); anything further surfaces at close per spec Risk 5, no silent scope growth |
| SV-016 interpretation creep (q_eng still below band) | — | — | re-flagged at close for the owner, per the Align ruling; not self-resolved |
