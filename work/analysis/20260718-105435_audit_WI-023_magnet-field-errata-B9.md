# Audit Report — WI-023 magnet-field-errata-B9 (work item audit)

**Date**: 2026-07-18 | **Auditor**: independent audit session (did not implement the work)
**Scope**: work item WI-023 (`work/active/WI-023_magnet-field-errata-B9/`), uncommitted working-tree changes on `feat/stellarator-mbse-demo` at HEAD `cef74e8e`
**Verdict**: **POSITIVE** — all five MR-WI023 requirements satisfied, all five spec Success Criteria met, all plan completion gates re-verified. No blocking or material findings. Three note-level observations below.

## Executive Summary

WI-023 rebinds the concept-09 instance's magnet field from a phantom-sourced 5.86 T to the printed axis-averaged B₀ = 9.0 T and zeroes the phantom p_tf = 111 MW per the owner's option-b ruling. The auditor independently re-verified the source evidence (Table 2/5 images read directly; the published PDF text-searched), re-executed the pipeline, handshake, full validation ladder, and IFE regression, and re-derived the grep gates. Every executed number matches SV-030's recorded values bit-exact. The clean-room quarantine held: no barred path was opened by the implementation (per its record) or by this audit.

## Executed Evidence (re-run by the auditor, not taken from the implementation record)

| check | result |
|---|---|
| `run_stellaris.py` (exec venv) | ALL CHECKS PASSED, rel 1e-9 vs oracle, zero failures |
| magnet capital | $6,323,469,946 (50.2% share) — matches SV-030 |
| total overnight capital | $12,601,519,645.065952 — matches |
| p_net / q_eng / rec_frac | 915.145439 MW / 6.609268 / 0.1513 — matches |
| LCOE | $201.457898/MWh — matches |
| unchanged channels | V 425.000014, p_fus 2748.056877, p_th 3238.12, wall_load 3.131235 ≤ 4.05 — matches |
| `handshake_1costingfe.py` re-run | `git diff` empty on `handshake_comparison.json` and on the script (SV-025/026 byte-identical); working tree identical before and after audit re-runs |
| `agentic-mbse validate models --complete` | L1 = 0 (21 files); error set exactly the 6 pre-existing offenders (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`), zero new; L3/L4/L5 pass; the L2 ❌ is the known attribution of the hif:205 offender (all offenders live in files WI-023 did not touch) |
| IFE regression `run_anchors.py` (re-run) | 252.29996307 / 68.69020165 / 270.12117794 $/MWh; Meier 4.73540355 c/kWh — SV-023 anchors unchanged |
| handwritten reactivity impl | git-clean, sha256 `8d235747…794a9f` matches the plan's pre-regen record, `AUTO_IMPLEMENTED = False` intact, `preserve_handwritten=True` at `bridge_v11_generate.py:108` |

## Source Fidelity (re-derived)

- **Table 2 image** (`iter-01/sources/stellaris-design-details/images/page_002_table_0.png`, read directly): "Axis av. magnetic field strength [T] 9.0"; peak conductor 24.9 T; stored magnetic energy [GJ] 111; **no conduction-power row**.
- **Table 5 image** (`page_009_table_0.png`, read directly): "Axis averaged B₀ [T] 9.0" at Points A and B. Independent second witness.
- **Table 3 image** (`page_003_table_0.png`, read directly): 8 rows (aspect ratio … min radius of curvature), **no field row**; header right-truncated as the spec describes.
- **Published PDF** (`iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, pdftotext by the auditor): `5.86` — 0 occurrences; "conduction power to coils" — 0 occurrences; the deferral sentence "Economic aspects – including parasitic electricity consumption and availability – are outside the scope of this paper" present verbatim.
- All citation targets exist on disk (both images, raw.pdf, `page_020_table_0.png`); 1costingFE is at the pinned `0254385` and `steady_state_stellarator.yaml:19` prints `p_coils: 3.0` as cited.
- Handshake injection safety re-confirmed at source: `handshake_1costingfe.py:216` (`pb__p_tf` ← `pb["p_coils"]`) and `:271` (`magnet__B` ← `coil["b_center"]`).

## Grep Gate (re-derived)

No live model/pipeline artifact carries 5.86 as a value. Remaining hits in live surfaces are phantom-history/refutation mentions only (`stellarator_plant.sysml:63/93/111/113` both copies; `run_stellaris.py:234/237`; `verify_stellaris.py:72`; the two owner-ruled annotations). Old WI-019-era output JSONs match only as a digit coincidence inside `105226405.869…`. Generated artifacts carry `magnet__B: 9.0` and `pb__p_tf: 0.0` (JSON + schema defaults + snapshot literals: `111.0 → 0.0`, `5.86 → 9.0`). Phantom citation strings ("Table 3 line 289", "Table 2 line 235") are deleted from all live surfaces (grep-clean). Matches inside the PROTOCOL §3 barred `exploration/concept_analysis/analyses/09-qi-stellarator-hts/**` sit outside the demo model/pipeline surface; no barred file was opened.

## MR Verification

| requirement | status | evidence |
|---|---|---|
| MR-WI023-1 (B = 9.0, image citations, mapping trap retained) | PASS | `stellarator_plant.sysml:123-127` binding + comment; magnet-block Ref `:108-116`; trap restated `:88-92` and `:67-72` |
| MR-WI023-2 (all 5.86 docs rewritten, phantom citations deleted, stale a=1.5/3.20 → 1.3/3.00) | PASS | headline `:49-65`; traps note `:67-72` (caveat gone); magnet doc `:96-101` (3.00 m sum); r_coil comment `:131-134`; oracle/runner diffs; grep gates above |
| MR-WI023-3 (p_tf = 0.0 per [OWNER] option b; honest deferral; no Stellaris MW cited; WI-024 pointer) | PASS | `stellarator_plant.sysml:434-453`; Basis line "cites no MW value"; WI-024 named `:446` |
| MR-WI023-4 (standing bars) | PASS | auditor re-ran validation, pipeline, handshake, IFE anchors (table above); mirror diff shows only the known staged viability-assert divergence |
| MR-WI023-5 (citations resolve; clean-room) | PASS | all cited files verified on disk; sources are admissible per PROTOCOL §3 (iter-01 images, iter-02 publikationen mirror, 1costingFE) |

## Spec Success Criteria

1. SV-030 headline — PASS (executed by auditor, values above, bit-exact).
2. SV-025/026 byte-identical — PASS (auditor re-ran handshake; empty diffs).
3. L1–L6 baseline + SV-023 + viability — PASS (re-run; 6 pre-existing offenders exactly; anchors exact; beta 0.0276 / wall 3.131 / TBR static bindings untouched).
4. Handwritten impl survives regen, pipeline bit-exact — PASS (hash + AUTO_IMPLEMENTED=False + rel-1e-9 run).
5. No live 5.86 carrier; headline recorded — PASS (grep gates; `.project/CURRENT_WORK.md` new WI-023 section matches executed numbers; plan Implementation Record present, all checkboxes checked).

## Owner-Ruling Fidelity

- `HANDSHAKE_REPORT.md:30` — original WI-019-era sentence untouched; dated WI-023 update note appended directly below (diff is pure addition). PASS.
- `analyst-patch-spec-anchors.md` — table rows untouched; dated errata blockquote appended below the table (pure addition). PASS.
- SV-016 — status still `pending`; dated re-flag appended to the Description cell (q_eng 3.93 → 6.609, still below the ~10–40 band); band and status not touched; not self-resolved. PASS.
- SV-030 — flipped to `passing` with the executed values recorded; values match the auditor's run. PASS.
- WI-024 — registered in `work/BACKLOG.md` (frontmatter + table) and in the epic file with the owner-stated intent; the p_tf doc's forward pointer resolves. PASS.

## SV-XXX Status

SV-030 `passing` and SV-016 `pending` (re-flagged) already reflect the audited reality — no status mutations made by this audit (item close is owner-held).

## Findings

No blocking findings. No material findings. No minor findings.

**Notes (no action required for WI-023):**

1. **[note] Table 2 image prints plasma volume 428 m³** while Table 5 prints 425 (the bound value, WI-022's choice of the Point-A operating table). The analyst-patch errata sentence "the images print V = 425 m³" is loose — true of Table 5, not Table 2. WI-022 legacy, outside WI-023 scope; flagged for any future errata sweep.
2. **[note] BACKLOG status field** for WI-023 reads `backlog` while the spec is `active` — the same pre-existing convention as WI-009/010/018; the dashboard resolves via spec override ("active:implementing") and `pm close-item` will settle it. Not a WI-023 defect.
3. **[note] Traceability matrix** not extended — consistent with the recorded WI-020→022 convention (instance-literal rebinds cite in model doc comments); noted for completeness against the audit command's matrix obligation.

## Quarantine

No PROTOCOL §3 barred path was opened in this audit. The audit's repo-wide 5.86 grep excluded the barred trees from its output; a filename-only check confirmed no `knowledge/sources/` barred extraction matches 5.86 at all. The implementation record's own quarantine disclosure (match lines from the barred analyses track seen in a grep, no file opened) is consistent with what the auditor observed.

## Audit Metadata

- Models audited: `models/designs/stellarator_09/stellarator_plant.sysml` + staged twin; oracle/runner/generated artifacts under `exploration/stellarator_e2e/`
- Baseline sources: Stellaris Table 2/3/5 images (iter-01), publikationen raw.pdf (iter-02), 1costingFE @ `0254385`
- Thresholds: rel 1e-9 (pipeline vs oracle), byte-identity (handshake), exact offender-set match (L1–L6)
- Everything in "Executed Evidence" was re-run by the auditor; nothing in this report relies solely on the implementing agent's self-report.
