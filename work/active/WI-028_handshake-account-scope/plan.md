---
Status: draft
Created: 2026-07-20
Updated: 2026-07-20
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
  Orchestration: ../../orchestration/handshake-account-scope.md
  Protocol: ../../../knowledge/holdout/aries-cs/PROTOCOL.md
---

# WI-028 Plan — Handshake account scope: CAS22 tail + CAS40/50/60 (STELLARATOR-DEMO Item 3)

**Required reading honored.** `knowledge/holdout/aries-cs/PROTOCOL.md` §3 barred paths were not read, cited, or opened while writing this plan. This is a stellarator-demo model-development item; the barred artifacts stay barred through implement. Admissible surfaces only: the staged demo package under `exploration/stellarator_e2e/`, canonical `models/`, the 1costingFE editable dep at pin `0254385` (the ARIES-lineage exception already scoped in PROTOCOL §3, with C220107 excluded/footnoted at hold-out), and the sysml-codegen / teax / agentic-mbse deps at the WI-027 pins.

## Source Documents

- **Design (primary input):** `./design.md` — the approved rev-3 design. Both owner gates ruled: **D1 full rebuild** and **D2 CAS60 Option C** (reported line excluded from `total_capital`). Do not reopen the settled decisions. Load-bearing sections for implement: **D1** (the 7 calc defs), **D2** (the overnight rebuild block), **D2b** (staged-twin propagation — the M1 must-fix), **D3** (the 4-deep CAS50 chain), **D4** (CAS60 Option C), **D5** (harness + instance bindings table), **D6** (trap table), **D7** (A-4 remainders), the **Validation Plan**, and the **Implementation Checklist**.
- **Spec:** `./spec.md` — MR-WI028-1…10, Success Criteria, SV-034, Standing bars.
- **Orchestration brief:** `../../orchestration/handshake-account-scope.md` — Align rulings, the two owner gate rulings (post-design), the stage log, standing bars.
- **Epic (tracking home):** `.project/backlog/epic_stellarator_mbse_demo.md`, Item 3. **Governing frame:** `.project/concepts/stellarator-mbse-demo.md`, criterion 3 — done-ness runs against this criterion and the ratified anchor bars (A-2/A-3/A-4/A-5/A-6 + G-8) in `.project/active/demo-anchor-acceptance-spec/spec.md`.

## Design Summary

Forward-compute the reactor-plant cost tail and the owner/supplementary/IDC accounts that are structurally absent today, so they come under the A-2 per-account bar (|rel dev| ≤ 1e-6 vs 1cfe float32). Add **7 concept-agnostic library calc defs serving 11 accounts** (design D1), **rebuild the overnight-capital assembly to mirror 1cfe exactly** (design D2 — cas2x → contingency → cas20 → indirect → cas30 → overnight; CAS10 at overnight; cas28 added), and bind the new unit-cost bases at the Stellaris instance as dollar conversions of the pinned 1cfe constants (design D5). CAS60 is a **reported, A-2-checked line excluded from `total_capital`** (Option C, D4); the DCF `idc_factor` is untouched. Rationale, the independent formula re-derivation, findings F-1…F-4, and the rejected narrow-shadow alternative are in the design — not repeated here.

## Prototype Baseline (design stage)

Per the design's Validation Report, the design stage produced parse-clean stencils and an independent assembly reproduction — but **no codegen capture** (deferred to this plan, step 2 of the Validation Plan). Levels 1–3 pass on the stencils; the load-bearing de-risks that remain are the **codegen compile of the 4-deep cross-calc chain** (Phase 4) and the **A-2 numeric measurement** (Phase 5).

| File | Role | State entering implement |
|---|---|---|
| `work/active/WI-028_handshake-account-scope/prototype/mfe_tail_supplementary_costs.sysml` | 7 calc-def stencils (`'Plant Power-Law Cost'`, `'Remote Handling Cost'`, `'Installation Labor Cost'`, `'Coolant Cost'`, `'Aux Cooling Cost'`, `'Supplementary Cost'`, `'IDC Closed-Form Cost'`) | **parse-clean** (design Validation Report); source-of-truth for Phase 1 |
| `work/active/WI-028_handshake-account-scope/prototype/plant_chain_probe.sysml` | full cas2x→contingency→cas20→indirect→cas30→supplementary probe | **parse-clean** against real `mfe_account_costs.sysml` deps; shape reference for Phase 2 |
| canonical `models/library/analyses/mfe_account_costs.sysml` | library, 13 existing calc defs | append the 7 new defs (Phase 1) |
| canonical `models/designs/generic_mfe/mfe_plant.sysml` | generic plant | overnight rollup at `:388-424` (flat chain — to rebuild, Phase 2) |
| staged `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` | **codegen input twin** | rollup at `:388-429`; carries Item-10 explanatory comment lines at `:400-403`/`:427` (staged-only, keep) |
| canonical `models/designs/stellarator_09/stellarator_plant.sysml` | Stellaris instance (758 lines) | bind new bases next to WI-025 bindings (Phase 3) |
| staged `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` | **codegen input twin** (758 lines) | same bindings, region-identical (Phase 3) |
| `exploration/stellarator_e2e/stellarator.snapshot.json` | codegen input | captured from the **stale flat rollup** — must be recaptured from the staged tree (Phase 4) |
| `exploration/stellarator_e2e/{emit_1cfe_point.py, handshake_1costingfe.py}` | harness | add refs / channels / rows / injection / traps (Phase 5, D5/D6) |
| `exploration/stellarator_e2e/handshake_comparison.json` | handshake output | re-baselined as an explicit commit, G-8 (Phase 6) |
| `modeling_project/VALIDATION_MATRIX.md` | SV registry | SV-034 registered `pending` |

Level 4–6 issues from the design to address by phase: **L5 documentation / traceability** (MR-4 citations on every new base) → Phases 1 & 3; **L6 architecture** (the 4-deep cross-calc DAG, D3) → codegen-capture checkpoint Phase 4; **library/designs separation** (MR-3: defs concept-agnostic, `concept_scale` is an instance input) → Phases 1 & 3.

## Phasing Approach

Seven phases (0–6), each ending at a **mechanically checkable state**, following the design's Implementation Checklist. The hard orderings, both honored:

1. **Both trees, region-identical, every `.sysml` edit (D2b).** The 7 defs, the D2 restructure, and the D5 bindings each land in BOTH the canonical `models/` tree and the staged `exploration/stellarator_e2e/models/` twin — the library twin path is `models/analyses/` (not `models/library/analyses/`). Codegen reads the staged twin; a canonical-only edit produces a silent wrong result against the stale flat rollup (design Risk 2 / M1). This is a first-class per-phase gate, not a final reconcile.
2. **The codegen-capture checkpoint (Phase 4) runs before the instance-binding-dependent numeric work (Phase 5).** The restructure and the instance bindings must both be in the staged tree for the generate to emit instance-scoped aggregation producers — so Phases 1→2→3 land first; then Phase 4 recaptures from the staged tree and confirms the 4-deep chain **compiles** in correct topological order (the D3 de-risk); only after that structural gate passes does Phase 5 trust any A-2 number computed off the restructure. This is the design's Validation Plan step 2 ordered ahead of steps 3–7.

Bottom-up within that spine: library defs (Phase 1) before the plant that uses them (Phase 2) before the instance that binds them (Phase 3) before capture (Phase 4) before measurement (Phase 5) before re-baseline/records (Phase 6). Phase 0 pins the toolchain first.

## Validation Strategy

- **Per phase:** each phase ends with the specific checks in its Validation Checkpoint. Parse (`uv run python -m syside check`) after every `.sysml` phase (1–3); the staged-vs-canonical mirroring diff after every two-tree edit; the codegen compile at Phase 4; the A-2 numeric bar at Phase 5; the full standing-bars sweep at Phase 6.
- **The load-bearing gates** are Phase 4 (codegen compile of the 4-deep chain — the D3 risk) and Phase 5 (A-2 |rel dev| ≤ 1e-6 per account — the SV-034 deliverable). Parse cannot settle codegen topological order (design D3); the A-2 bar catches any formula misreading at percent scale.
- **The 6-level pyramid applies in a scoped way:** L1 (parse / offender list) runs at Phases 2–4 and again in the Phase-6 sweep; L2–L6 level *flags* may shift with the added defs/modules — per the WI-027 precedent, compare the **offender list** (expected = the 6 pre-existing), not the flags.
- **Final (Phase 6):** the full standing-bars set on one executed run — oracle rel 1e-9 bit-exact at the new headline; WI-022 sha256; IFE Runs A/B byte-exact (Run C out-of-scope, owner ruling); pytest 11/18/14/0; L1 offender list = 6; regen stability. This is the spec's Success Criteria and SV-034 in one place.

## Rollback / Surface Posture (all phases)

Every edit is git-tracked; rollback is `git checkout -- <paths>` at any phase. **No bar is ever made to pass by moving the model or the design point** (MR-WI028-9 is a re-baseline, not a licence to tune). The named **surface-to-orchestrator** conditions — stop the phase, report, do not work around (the WI-027 Phase-2 STOP is the precedent):

- **Codegen abort or wrong topological order** on the 4-deep cas2x→…→supplementary chain at Phase 4 (the D3 risk; the WI-027 Phase-2 INV-2 abort is the precedent for how this surfaces).
- **An account cannot meet A-2** for a non-float32 reason at Phase 5 (a real formula/mapping error) — surface; a *legitimate* float32-ceiling miss is itemized under A-4 (D7), not surfaced as a failure.
- **A standing bar breaks** at Phase 6 that this item did not intend to move — oracle rel 1e-9 fails on a channel, a new L1 offender appears, WI-022 hash changes, IFE Run A/B moves, pytest tally shifts for a model reason.
- **A pin is unreachable** at Phase 0, or the 1cfe drift-assert trips at run (A-6).
- **A staged↔canonical delta** at any mirroring gate beyond the intended WI-028 edits + the known Item-10 / DEMO-NOTE divergences (design D2b: any other delta is a defect that blocks recapture).

---

## Phase 0 — Toolchain pins + restore point

**Overview.** Check out and record the WI-027 pins explicitly. sysml-codegen and teax HEADs have advanced past the WI-027 pins (design "Toolchain pins"); this item stays on the WI-027 commits — movement is adopted deliberately, never implicitly (spec Standing bars, A-6). Establish the clean-tree restore point.

**Design Reference.** See design §"Toolchain pins (verified live this stage)". Key points:
- Pins: **sysml-codegen `06d95f8`** (Item 10 certified `1c85042`), **teax `07eb0ac`**, **agentic-mbse `4c18d61`**, **1costingFE `0254385`** (drift-asserted at run, A-6).
- sysml-codegen live HEAD was `baf455d`, teax live HEAD `c342b10` — both **moved**; both WI-027 pins remain **reachable**. Check out the pins; do not adopt the newer HEADs.

**Checklist.**
- [x] Confirm a clean tracked working tree (only `.orchestrate-logs/` untracked) as the restore point; record `git` HEAD of the fusion-tea repo.
- [x] `~/1cfe/sysml-codegen`: check out `06d95f8`; record the exact commit + `git status` (worktree state) for SV-034.
- [x] `~/1cfe/teax` (teax dep): check out `07eb0ac`; record commit.
- [x] agentic-mbse `4c18d61`, 1costingFE `0254385`: confirm checked out; record.
- [x] Confirm `SYSIDE_LICENSE_KEY` resolves: `set -a && source ~/1cfe/fusion-tea/.env && set +a`.

**Validation Checkpoint.**
- [x] All four pins checked out and recorded (commit + worktree state for the two that moved).
- [x] Parse smoke: `uv run python -m syside check models/` (baseline clean before any edit).

**Phase Completion Gate.** The four pins are checked out and recorded; the restore point (clean tree + HEAD) is captured. **STOP-and-report** if any pin is unreachable or a checkout fails — a pin mismatch is surfaced, never silently accepted (A-6).

---

## Phase 1 — Library calc defs (both trees)

**Overview.** Add the 7 new concept-agnostic calc defs to the library, in BOTH trees. These are the leaf definitions the plant (Phase 2) consumes; they land first (bottom-up). Source from the parse-clean prototype `mfe_tail_supplementary_costs.sysml`.

**Design Reference.** See design **D1** (the calc-def → accounts table and the reuse rationale). Key points:
- `'Plant Power-Law Cost'` serves **five** accounts (C220400 waste α=1.0, C220500, C220600, C220700, **CAS40**) as `base*(n_mod*power/ref)**alpha`; the other six defs are one-per-account.
- Codegen-envelope-clean: flat Real arithmetic (`+ - * / **`), no `if`/lookup/`sum`/nested-calc. Reference powers and exponents are **defaulted inputs** carrying their 1cfe citation (MR-4); bases and fuel/concept factors are **un-defaulted inputs**, bound at the instance (MR-3). `concept_scale` stays an instance input, never a library default.
- `'IDC Closed-Form Cost'` uses a variable real exponent (`construction_years`); the existing `mfe_lcoe_dcf.sysml:47` proves codegen handles variable exponents.

**Files to Create/Modify.**
- REFINE `models/library/analyses/mfe_account_costs.sysml` (append 7 defs after the 13 existing, last is `'Annual OM Cost'` at `:387`).
- REFINE `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` (**note path: `models/analyses/`, not `models/library/analyses/`**) — region-identical append.

**Checklist.**
- [x] Append `'Plant Power-Law Cost'` (inputs: base, power, n_mod, ref_power, alpha) — canonical + staged.
- [x] Append `'Remote Handling Cost'` (base, concept_scale, p_et per-module, ref 1100, α 0.5) — both trees.
- [x] Append `'Installation Labor Cost'` (installation_frac 0.14, reactor_subtotal) — both trees.
- [x] Append `'Coolant Cost'` (primary_base, intermediate_base, p_net, p_th, n_mod, refs 1000/3500, α 0.55) — both trees.
- [x] Append `'Aux Cooling Cost'` (aux_per_mw, p_th, cryo_base, p_cryo per-module, n_mod, ref 30, α 0.7) — both trees.
- [x] Append `'Supplementary Cost'` (six fracs/bases + cas20, cas23_to_28, cas30, p_net, n_mod; input named `cas23_to_28` per F-1) — both trees.
- [x] Append `'IDC Closed-Form Cost'` (interest_rate, construction_years, overnight_cost) — both trees.
- [x] Each defaulted input (ref powers, exponents, `installation_frac`) carries an MR-4 doc-comment citation to the 1cfe source at pin `0254385` (`cas22.py:631-731`, `costs.py:239-297`).
- [x] Confirm no Stellaris-specific literal appears in any def (MR-3); `concept_scale` is an input, not a default.
- [x] Add the 7 defs to `data/traceability_matrix.csv` (library defs, source-cited).

**Test Requirements.** Structural parse test only (leaf defs). Their numeric correctness is graded by the Phase-5 A-2 bar end-to-end, not unit-tested here (the WI-025/WI-027 pattern).

**Validation Checkpoint.**
- [x] `uv run python -m syside check models/library/analyses/mfe_account_costs.sysml` → **Checks passed!**
- [x] `uv run python -m syside check exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` → **Checks passed!**
- [x] Mirroring diff: the 7 appended defs are **region-identical** between the two files (only file-path context differs).

**Phase Completion Gate.** Both library files carry the 7 defs, parse-clean, region-identical, MR-4-cited, MR-3-clean (no concept literals). **STOP-and-report** on a parse failure that the prototype did not exhibit (a botched transcription).

---

## Phase 2 — Generic-plant overnight rebuild (both trees, D2 + CAS60 Option C wiring)

**Overview.** Replace the flat `direct_capital → contingency/indirect → total` chain (canonical `mfe_plant.sysml:388-424`; staged `:388-429`) with the 1cfe-mirroring overnight assembly. This is the risky cross-calc construct (parse-validated in `plant_chain_probe.sysml`) and the highest-scope change. Land it region-identical in both `mfe_plant.sysml` copies, reconciling the staged copy's Item-10 comment lines rather than blind-overwriting.

**Design Reference.** See design **D2** (the overnight assembly block, verbatim), **D3** (the 4-deep CAS50 chain), **D4** (CAS60 Option C wiring), and the **Cross-file bindings** table. Key decisions (do not re-derive):
- New tail account calc usages (7 defs → 8 tail accounts: `'Plant Power-Law Cost'` instantiated for waste/fuel/other/I&C, plus remote_handling/installation/coolant/aux_cooling) feed `cas22_tail_capital`.
- New aggregate attributes: `cas22_capital`, `cas28_capital` (fed 5.0e6, F-2), `cas2x_pre_contingency` (**NO CAS10**), `cas20_capital`, `cas30_capital`, `cas23_to_28_capital`, `overnight_capital`.
- **Rebind** `contingency` input from `direct_capital` → `cas2x_pre_contingency` (was `:408`); **rebind** `indirect` input from `direct_capital` → `cas20_capital`, post-contingency (was `:417`).
- CAS40 (`owner`) + CAS50 (`supplementary`) usages added **at the overnight level**, NOT into cas2x.
- **CAS60 Option C:** add the `idc` calc usage reading `overnight_capital`; expose its `cost` as a **reported line**; `total_capital = overnight_capital` — the idc line is **NOT** summed into `total_capital`. Leave `lcoe_calc` (`:435`) and its `total_capital` input untouched; `mfe_lcoe_dcf.sysml` `idc_factor` untouched.

**Prototype Baseline (this phase).** Canonical `mfe_plant.sysml:388-424` and staged `:388-429` carry the flat WI-025 rollup. The staged copy carries Item-10 explanatory comment lines at `:400-403` and `:427` (the DEMO-NOTE plain-input conversions were removed at Item 10; the rollup formulas are byte-identical to canonical, only the comments differ). **Keep those staged-only comment lines** — they are the known staged↔canonical divergence, not a defect.

**Files to Create/Modify.**
- REFINE `models/designs/generic_mfe/mfe_plant.sysml` (rebuild `:388-424`).
- REFINE `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` (rebuild `:388-429`; reconcile Item-10 comment lines).

**Checklist.**
- [x] Canonical: add the 8 tail account calc usages; add `cas22_tail_capital` / `cas22_capital` / `cas28_capital` / `cas2x_pre_contingency` / `cas20_capital` / `cas30_capital` / `cas23_to_28_capital` / `overnight_capital` per the D2 block.
- [x] Canonical: rebind `contingency.in direct_subtotal` → `cas2x_pre_contingency`; rebind `indirect.in direct_cost` → `cas20_capital`.
- [x] Canonical: add `owner` (CAS40) + `supplementary` (CAS50) usages at the overnight level; add `idc` (CAS60) usage reading `overnight_capital`, `cost` exposed as a reported line.
- [x] Canonical: `total_capital = overnight_capital` (CAS60 `idc.cost` NOT summed in); `lcoe_calc` + `idc_factor` untouched.
- [x] Staged twin: apply the **same regions**, keeping the Item-10 comment lines at `:400-403`/`:427`; no blind overwrite.
- [x] Confirm dataflow stays unidirectional (design "Cross-file bindings": powers → accounts → cas2x → contingency → cas20 → indirect → cas30 → overnight → total_capital → LCOE; no cycle).

**Test Requirements.** Parse test both trees. The rebuild's numeric correctness is graded by Phase-4 compile + Phase-5 A-2 rollup match (`cas20→5710.95`, `cas30→1522.92`, `overnight→7872.15`).

**Validation Checkpoint.**
- [x] `uv run python -m syside check` on both `mfe_plant.sysml` copies → **Checks passed!**
- [x] `uv run agentic-mbse validate --level 1 models` → L1 offender list = the 6 pre-existing (the 3 canonical `mfe_plant.sysml` capital-rollup cross-part derived expressions may line-shift; `ife_plant.sysml:33/41`, `hif_plant.sysml:205`). **Zero new offenders** beyond the known rollup keys.
- [x] Mirroring diff: staged-vs-canonical `mfe_plant.sysml` shows **only** the intended WI-028 rebuild + the known Item-10 comment divergence — nothing else.

**Phase Completion Gate.** Both `mfe_plant.sysml` copies carry the rebuilt overnight assembly, parse-clean, region-identical modulo the Item-10 comments; contingency/indirect rebased; CAS60 wired Option-C (`total_capital == overnight_capital`, idc reported-not-summed); LCOE untouched; L1 offender list unchanged. **STOP-and-report** on a new L1 offender or a mirroring delta beyond the intended edits.

---

## Phase 3 — Stellaris instance bindings (both trees, D5)

**Overview.** Bind the new unit-cost bases at the Stellaris instance as dollar conversions of the pinned 1cfe constants, in BOTH `stellarator_plant.sysml` copies, next to the WI-025 building/precon bindings. These provide the instance-scoped values the codegen generate (Phase 4) resolves per instance.

**Design Reference.** See design **D5** (the instance bindings table) and the **Cross-file bindings** table. Key points:
- Every base is a dollar conversion (×1e6 where the 1cfe constant is in M$) with an MR-4 citation to `0254385`.
- `p_cryo` binds from `cryo_elec.p_elec` (`mfe_plant.sysml:238` proves it is available cross-calc); `p_th`/`p_net`/`p_et` from the `pb.*` aliases.
- `concept_scale = 1.0` (stellarator, toroidal) is bound **here** (instance), not in the library (MR-3).
- The full base list (canonical binding values): C220110 base 150.0e6 / concept_scale 1.0 / ref 1100 / α 0.5; C220111 frac 0.14; C220200 166.0e6 + 40.6e6 / refs 1000,3500 / α 0.55; C220300 aux 1100.0 per-MW + 200.0e6 / ref 30 / α 0.7; C220400 1.96e6 / ref 1000 / α 1.0; C220500 120.0e6 / ref 1000 / α 0.7; C220600 11.5e6 / ref 1000 / α 0.8; C220700 85.0e6 / ref 3500 / α 0.65; CAS40 41.2e6 / ref 1000 / α 0.5; CAS50 fracs 0.015/0.01/0.015/0.03 + 40.0e6/272.0e6 / ref 1000; cas28 5.0e6.

**Files to Create/Modify.**
- REFINE `models/designs/stellarator_09/stellarator_plant.sysml` (bind next to WI-025 bindings, ~`:262+`).
- REFINE `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` (region-identical).

**Checklist.**
- [x] Bind all 11 base rows from the D5 table (8 tail + CAS40 + CAS50 + cas28) — canonical + staged, region-identical.
- [x] Bind `concept_scale = 1.0`; bind `p_cryo` from `cryo_elec.p_elec`.
- [x] Each binding carries an MR-4 `Source`/`Ref`/`Basis` citation to the 1cfe constant at `0254385` (mirror the WI-025 binding doc-comment style at `:271-308`).
- [x] Add the 11 instance bindings to `data/traceability_matrix.csv` (designs-scoped, source-cited).
- [x] Confirm no new base is a library default (MR-3: all Stellaris-specific values live here).

**Test Requirements.** Parse test both trees. Numeric correctness graded at Phase 5 (A-2).

**Validation Checkpoint.**
- [x] `uv run python -m syside check` on both `stellarator_plant.sysml` copies → **Checks passed!**
- [x] Mirroring diff: staged-vs-canonical `stellarator_plant.sysml` shows **only** the intended WI-028 bindings — nothing else.

**Phase Completion Gate.** Both instance files carry the 11 bindings, parse-clean, region-identical, MR-4-cited, MR-3-clean. **STOP-and-report** on a mirroring delta or a parse failure.

---

## Phase 4 — Mirroring diff gate + snapshot recapture + codegen-capture checkpoint (the D3 de-risk)

**Overview.** This is the load-bearing structural gate and the design's Validation Plan step 2. Confirm the whole D1/D2/D5 edit set landed region-identical in the staged tree, recapture `stellarator.snapshot.json` **from the staged tree**, then generate and confirm the 4-deep cas2x→…→supplementary chain **compiles to instance-scoped aggregation producers in correct topological order**. It runs before any Phase-5 numeric work builds on the restructure — parse cannot settle codegen topological order (design D3); this checkpoint does.

**Design Reference.** See design **D2b** (staged-twin propagation + mirroring diff gate + recapture), **D3** (the 4-deep DAG and the WI-010/WI-025 precedent), and Validation Plan step 2. Key points:
- **Codegen's input is the staged twin, not canonical `models/`** — the snapshot has 59 path refs into `exploration/stellarator_e2e/models/`; a stale twin yields a silent wrong result (design Risk 2 / M1). Recapture is mandatory.
- The mirroring diff gate: staged-vs-canonical region diff must show **only** the intended WI-028 edits + the known Item-10 / DEMO-NOTE divergences before recapture.
- Recapture + generate via the sysml-codegen CLI (`snapshot` then `generate --from-snapshot`) at pin `06d95f8`, from the staged tree. Run from the exec context with `SYSIDE_LICENSE_KEY` set.

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/stellarator.snapshot.json` (recaptured from the staged tree).
- REFINE `generated/**` under the e2e package (machine-produced; no hand-edits) — new instance-scoped producers for the cas2x→…→overnight chain and the account/idc calcs.

**Checklist.**
- [x] **Mirroring diff gate:** for all three edited `.sysml` region sets (library defs, `mfe_plant.sysml` rebuild, `stellarator_plant.sysml` bindings), staged-vs-canonical diff shows **only** the intended WI-028 edits + the known Item-10 comment lines (`mfe_plant.sysml:400-403/427`). Any other delta blocks recapture (design D2b).
- [x] `set -a && source ~/1cfe/fusion-tea/.env && set +a` (license).
- [x] Recapture: run the sysml-codegen `snapshot` CLI over `exploration/stellarator_e2e/models` → `exploration/stellarator_e2e/stellarator.snapshot.json`, from the **staged tree** (mirror the WI-027 Item-10 bridge-free recipe; no `--design-path-filter` per the WI-024 gotcha).
- [x] Confirm the recaptured snapshot carries the new account/rollup structure (grep for the new attribute names: `cas2x_pre_contingency`, `cas20_capital`, `cas30_capital`, `overnight_capital`, the tail account usages) and still carries the 5 WI-027 constraint facts (`beta_ok`/`net_positive`/`recirc_ok`/`tbr_ok`/`wall_load_ok`, `constraint_lowering_mode: applied`).
- [x] Generate: `sysml-codegen generate --from-snapshot` at `06d95f8`; confirm the 4-deep chain compiles — the `supplementary` producer reads instance-scoped `cas20_capital` and `cas30_capital`; `cas30`←`cas20`←`contingency`←`cas2x` resolve in correct topological order (design D3).
- [x] Confirm generated constraint modules + aggregator still present (WI-027 carry-through); WI-022 `dt_fusion_power_impl.py` sha256 = `8d2357…794a9f` survives regen.

**Test Requirements.** Structural verification of the generated package (the checks above). No new pytest — generated modules are proven-template; correctness graded by the Phase-5 A-2 run.

**Validation Checkpoint.**
- [x] Mirroring diff clean (only intended edits + Item-10 comments).
- [x] Snapshot recaptured from the staged tree; carries the new structure + the 5 constraint facts.
- [x] Generate succeeds; the 4-deep cross-calc chain compiles to instance-scoped producers in correct order.
- [x] L1 offender list = the 6 pre-existing, zero new; WI-022 hash intact.

**Phase Completion Gate.** The staged twin carries the full WI-028 restructure; the snapshot is recaptured from it; the 4-deep chain compiles in correct topological order; WI-022 hash + L1 offenders unchanged. **STOP-and-report** on a codegen abort or wrong-order compile (the D3 risk — the WI-027 Phase-2 INV-2 abort is the precedent; report the exact codegen error, do not work around by editing canonical or diverging the twin), or a mirroring delta the gate rejects.

**Rollback.** `git checkout -- exploration/stellarator_e2e/stellarator.snapshot.json` and discard regenerated `generated/**`; re-running the recapture from the committed staged tree is deterministic.

---

## Phase 5 — Harness + A-2 per-account measurement (D5/D6, SV-034 core)

**Overview.** Add the harness refs, channels, comparison rows, injection entries, and traps (D5/D6), then run the handshake and measure each account under A-2. This is the SV-034 deliverable. The comparison *logic* is unchanged — only new rows and inputs (G-8, MR-WI028-8).

**Design Reference.** See design **D5** (harness additions — emitter refs, handshake channels/rows/injection), **D6** (the trap table, all six trap classes), **D4** (CAS60 A-2 row), and **D7** (A-4 remainders). Key points:
- **`emit_1cfe_point.py`:** add the new CONST bases to `refs` (remote_handling 150.0, fuel_handling 120.0, installation_frac 0.14, owner 41.2, shipping 0.015, spares 0.03, tax 0.01, insurance 0.015, startup 40.0, decom 272.0, cas28, concept_scale 1.0) so the handshake feeds them (×1e6) and asserts them against 1cfe config (A-5).
- **`handshake_1costingfe.py`:** add SysML channels for the 8 tail accounts + CAS40/CAS50/CAS60 line to `CH`; feed the new bases into the injection map (×1e6); add explicit comparison rows for C220110/111/200/300/400/500/600/700, CAS40, CAS50, CAS60. Logic unchanged.
- **D6 traps** (assert every new mapping, add to the trap table): (1) plant-total vs per-module split; (2) reference-power split; (3) installation base = Σ(C220101..C220110); (4) fuel-keyed bases match `cc` for DT; (5) F-2/F-3 structural asserts (cas28 present, CAS10 at overnight/absent from cas2x, indirect on post-contingency cas20); (6) **CAS60 Option C: `total_capital == overnight_capital`, idc line reported-not-summed, `idc_factor` unchanged**.

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/emit_1cfe_point.py` (refs additions).
- REFINE `exploration/stellarator_e2e/handshake_1costingfe.py` (channels + rows + injection + traps; comparison logic untouched).

**Checklist.**
- [x] `emit_1cfe_point.py`: add the 12 refs (11 bases + concept_scale), each read from the 1cfe config at `0254385` (drift-asserted, A-6).
- [x] `handshake_1costingfe.py`: add the 11 channels (8 tail + CAS40 + CAS50 + CAS60) to `CH`; feed the new bases into the injection map (×1e6); add the 11 explicit comparison rows.
- [x] Add all six D6 trap classes as assertions and to the trap table (MR-WI028-6 / A-5).
- [x] **Execute** the handshake: `exploration/pipeline_spike/.venv-exec/bin/python handshake_1costingfe.py` (against the Phase-4 recaptured snapshot / generated package).
- [x] **A-2 per-account (SV-034):** record each of the 8 tail accounts + CAS40 + CAS50 + CAS60 line's `rel_dev`; each under |rel dev| ≤ 1e-6 vs 1cfe float32 at the handshake point.
- [x] **Rollup match:** confirm `cas20_capital → 5710.95`, `cas30_capital → 1522.92`, `overnight → 7872.15` (the direct/indirect rows move from −18.64% to ~0).
- [x] **A-4 remainder table** (D7): itemize C220106_pump ($0.721M, standing), CAS10 (+16.0M / +86.5%, isolated at overnight, explained-and-kept), and the CAS60/`total_capital` convention difference (1cfe folds CAS60 into `total_capital` = 10095.84M; model keeps `total_capital = overnight = 7872.15M`, folds IDC into the LCOE `idc_factor`) — signed magnitudes; residual reconciles to the itemized sum.
- [x] Confirm the six traps all assert-pass (no silent default).

**Test Requirements.** The A-2 per-account bar and the trap assertions ARE the regression tests for the new accounts. The rollup-match check is the regression guard for the D2 rebuild.

**Validation Checkpoint.**
- [x] All 8 tail + CAS40 + CAS50 (+ CAS60 line) under |rel dev| ≤ 1e-6, recorded per account (SV-034).
- [x] Rollup values reproduce 1cfe (cas20/cas30/overnight).
- [x] Six D6 traps assert-pass; trap table updated.
- [x] A-4 remainder table itemized with signed magnitudes; residual reconciles.

**Phase Completion Gate.** Every newly-brought account is under A-2 (or a legitimate float32-ceiling account is itemized under A-4 with a signed magnitude); the rollup matches 1cfe; the traps pass; the A-4 table reconciles. **STOP-and-report** if an account misses A-2 for a real (non-float32) reason — a formula/mapping error surfaces, it is not worked around (the f_shape −20.6% precedent is why traps exist).

**Rollback.** `git checkout -- exploration/stellarator_e2e/emit_1cfe_point.py handshake_1costingfe.py`.

---

## Phase 6 — Re-baseline, standing-bars sweep, records (G-8, SV-034, MR-WI028-9/10)

**Overview.** Re-baseline `handshake_comparison.json` as its own explicit commit (G-8), record the moved design-point headline, run the full standing-bars sweep on one executed run, and fill SV-034. No source mutation in this phase — it re-baselines, grades, and records.

**Design Reference.** See design Validation Plan steps 5–7, **D7** (A-4), and spec MR-WI028-8/9/10 + Standing bars. Key points:
- G-8 amendment (in force): `handshake_comparison.json` moves are **expected** and re-baselined as an explicit commit; comparison *logic* untouched; the commit records which accounts moved absent→computed and each signed magnitude, and notes the injection map does not shrink for these accounts (they were absent, not injected).
- MR-WI028-9: the design-point headline **moves** (re-baseline, not regression); the oracle rel-1e-9 bit-exact bar holds at the new point.
- Standing bars (MR-WI028-10): pytest 11/18/14/0; L1 = 0 / offenders = the 6 pre-existing; WI-022 sha256; IFE Runs A/B byte-exact (**Run C out-of-scope by owner ruling** — record the supersession, do not treat as failure); regen stability; PROTOCOL honored.

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/handshake_comparison.json` (re-baselined; its own commit).
- REFINE `modeling_project/VALIDATION_MATRIX.md` (SV-034 `pending` → executed record).
- Item record (this plan's Implementation Record) — headline re-baseline, pins, bar results.

**Checklist — run once, grade all:**
- [x] **Execute the design point:** `exploration/pipeline_spike/.venv-exec/bin/python run_stellaris_single.py`; record the new headline (total_capital, LCOE, p_net, q_eng, magnet share).
- [x] **Oracle bit-exact (MR-WI028-9):** every executed channel matches the pure-Python oracle at rel dev < 1e-9 **at the new headline**.
- [x] **G-8 re-baseline (MR-WI028-8):** re-run the handshake; `handshake_comparison.json` gains the new rows; re-baseline as an **explicit standalone commit**; the diff matches the documented move list (each account absent→computed, signed magnitude); comparison logic byte-unchanged; note the injection map does not shrink for these accounts.
- [x] **Design-point headline re-baseline recorded** (MR-WI028-9) — the new total_capital/LCOE, explicitly a re-baseline like WI-025, not a regression.
- [x] **L1 offender list = 6 pre-existing, zero new** (compare the list, not level flags).
- [x] **WI-022 sha256** `8d2357…794a9f` survives (re-confirm post-run).
- [x] **IFE anchors:** Runs A/B byte-exact (252.29996307 / 68.69020165 / 270.12 as applicable; Meier 4.735); **Run C out-of-scope** — record the supersession (owner ruling 2026-07-20), do not treat as a failure.
- [x] **pytest:** `uv run pytest tests/models/ -q` → **11 failed / 18 passed / 14 skipped / 0 errors**.
- [x] **Regen stability:** re-capture to `/tmp` and diff vs committed snapshot — constraint facts + structure byte-identical (only `captured_at` / `document_path` metadata differ).
- [x] **Fill SV-034:** the per-account A-2 table (Phase 5), the rollup match, the new design-point headline, and each standing-bar result; set status `passing` **only if** all in-scope bars held (IFE Run C supersession recorded, not counted as a fail) via `uv run agentic-mbse pm update-validation SV-034 --status passing`.
- [x] Record the pins (Phase 0) and the PROTOCOL-honored note in the item record.

**Test Requirements.** This phase *is* the regression suite: oracle bit-exactness, L1 offender list, IFE anchors, pytest tally, regen stability. All must hold (Run C excepted by owner ruling).

**Validation Checkpoint (Levels 1–6 / spec Success Criteria).**
- [x] `handshake_comparison.json` re-baselined as a standalone commit; move list documented; logic untouched.
- [x] New headline recorded; oracle rel 1e-9 at the new point.
- [x] All standing bars hold (Run C supersession recorded); SV-034 filled.

**Phase Completion Gate.** The comparison JSON is re-baselined as its own commit; the new headline is recorded as a re-baseline with the oracle bar holding; every standing bar passes (IFE Run C out-of-scope, supersession recorded); SV-034 is an executed record. This gate = the spec's Success Criteria for MR-WI028-1…10. Ready for `/audit-models` → owner close (Align ruling 2: owner holds close; orchestrator commits after close). **STOP-and-report** on any standing-bar break this item did not intend to move (oracle fail, new L1 offender, WI-022 hash change, IFE Run A/B move, pytest shift for a model reason).

---

## Success Criteria Coverage (from spec)

| Spec Success Criterion | Covered by |
|---|---|
| 8 tail + CAS40 + CAS50 forward-computed as library defs, bound at Stellaris, MR-4-sourced (MR-WI028-1/2/7) | Phase 1 (defs) + Phase 3 (bindings) |
| Each newly-brought account under A-2 (1e-6), recorded per account; misses itemized (MR-WI028-4/5) | Phase 5 (A-2 + A-4) → SV-034 |
| CAS60/IDC mapping documented; Option C disposition recorded (MR-WI028-3) | Phase 2 (Option-C wiring) + Phase 5 (A-2 row + A-4 convention itemization) |
| Handshake re-run; comparison JSON gains rows, re-baselined as explicit commit; logic untouched; traps asserted (MR-WI028-6/8) | Phase 5 (rows + traps) + Phase 6 (re-baseline commit) |
| Design-point headline moves, recorded as re-baseline; oracle bit-exact at new point (MR-WI028-9) | Phase 6 |
| All standing bars hold; supersessions recorded (MR-WI028-10) | Phase 6 |

## Feasibility Concerns

Risks are carried from the design (§Risks); the plan restates the mitigations as phase-located gates:

1. **Staged-twin skip (high — M1).** Codegen reads the staged twin. Gate: every `.sysml` phase (1–3) ends with a mirroring diff; Phase 4 recaptures from the staged tree behind the mirroring diff gate. A canonical-only edit would silently compute against the stale flat rollup.
2. **Codegen binding order on the 4-deep chain (medium — D3).** Gate: Phase 4 codegen-capture checkpoint confirms the chain compiles to instance-scoped producers in correct topological order, before any A-2 number is trusted. Parse-validated; WI-010/WI-025 precedent. A wrong-order compile surfaces (WI-027 Phase-2 precedent).
3. **CAS60 double-count if Option C is mis-implemented (low).** Gate: `total_capital == overnight_capital` (idc reported-not-summed); `idc_factor` untouched; D6 trap 6 asserts it (Phase 5).
4. **The overnight rebuild touches WI-025 contingency/indirect wiring (medium — scope).** Ruled in-bounds by the owner (closes F-2/F-3/F-4). Gate: the headline moves as an expected re-baseline (MR-WI028-9), verified by the oracle bit-exact bar at the new point (Phase 6).
5. **Float32 near the A-2 ceiling (low).** Gate: Phase 5 measures; a legitimate ceiling miss is itemized under A-4, not surfaced as a failure.
6. **n_mod=1 hides per-module vs plant-total (low).** Gate: n_mod explicit in every def (Phase 1); D6 trap 1 asserts the split (Phase 5).

**Assumptions about baseline state:** the prototypes parse-clean (verified design stage); the staged twin is at its WI-027 Item-10 state (rollup byte-identical to canonical modulo the Item-10 comments); the four toolchain deps are reachable at the WI-027 pins. If a pin is unreachable at Phase 0, that is a mismatch to surface (A-6), not silently accept.

---

## Implementation Record

*(Filled by `/implement-model`. Skeleton below — one block per phase: what ran, gate evidence recorded, deviations; then a surfaced-finding block if any STOP fired, and the tree end state. Model on the WI-027 record.)*

**Restore point.** fusion-tea HEAD `5127efa4` (branch `feat/stellarator-mbse-demo`); tree clean, only `.orchestrate-logs/` untracked. Pins checked out: sysml-codegen `06d95f854f30f77f1a7c93f9c0f13be878765165` (was `d7ad714`; detached HEAD — worktree carries 2 docs-only uncommitted files under `.project/active/constraint-lifecycle-*`, no codegen code touched), teax `07eb0accd4852742a6da1820a05a4cae4fe707df` (was `c342b10`; clean worktree), agentic-mbse `4c18d616` (on pin), 1costingfe `02543850` (on pin, `../1costingfe` editable dep).

### Phase 0 — Toolchain pins + restore point — _(GATE PASSED)_
- **What ran.** Recorded fusion-tea HEAD + clean tree; confirmed all four pins reachable; checked out sysml-codegen `06d95f8` and teax `07eb0ac` (the two that had moved); confirmed agentic-mbse `4c18d61` / 1costingfe `0254385` already on pin; resolved `SYSIDE_LICENSE_KEY` (len 37); baseline parse smoke `uv run python -m syside check models/`.
- **Gate evidence.** All four pins checked out + recorded (commit + worktree state for the two that moved: sysml-codegen 2 docs-only files, teax clean). Restore point captured (HEAD `5127efa4`, clean tree). Baseline parse: **Checks passed!** (only pre-existing namespace-distinguishability warnings — `f_shape`, `lt_shield_t` — no errors). No pin unreachable; no STOP.
- **Deviations.** None.

### Phase 1 — Library calc defs (both trees) — _(GATE PASSED)_
- **What ran.** Appended the 7 defs (`'Plant Power-Law Cost'`, `'Remote Handling Cost'`, `'Installation Labor Cost'`, `'Coolant Cost'`, `'Aux Cooling Cost'`, `'Supplementary Cost'`, `'IDC Closed-Form Cost'`) after `'Annual OM Cost'` in canonical `models/library/analyses/mfe_account_costs.sysml`; copied the identical result to the staged twin `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` (the two files were byte-identical pre-edit, verified via `git show HEAD:`). Executable bodies transcribed byte-for-byte from the parse-clean prototype; doc comments enriched with `**Source**`/pin `0254385` footers to match library house style + MR-4. Added 7 rows to `data/traceability_matrix.csv`.
- **Gate evidence.** Parse: both files → **Checks passed!** Mirroring diff: `diff` of the two files → empty (region-identical). MR-4: every def carries a `**Source**`/`**Ref**` block citing the 1cfe source at pin `0254385` (`cas22.py:631-731`, `costs.py:256/259-297`), defaulted inputs (refs/exponents/`installation_frac`) carry inline citations. MR-3: no Stellaris literal in any def; `concept_scale` is an un-defaulted input. Traceability: 7 library-def rows added (12→19). No STOP.
- **Deviations.** None. (Doc-comment style enriched vs prototype's terser form; executable lines identical — no parse or semantic change.)

### Phase 2 — Generic-plant overnight rebuild (both trees) — _(GATE PASSED)_
- **What ran.** Replaced the flat `direct_capital → contingency/indirect → total` chain in canonical `models/designs/generic_mfe/mfe_plant.sysml` with the D2 overnight assembly: 8 tail-account calc usages (`remote_handling`, `installation`, `coolant`, `aux_cooling`, `waste`, `fuel_handling`, `other_rpe`, `inc_cost`) + `owner` (CAS40) + `supplementary` (CAS50) + `idc` (CAS60); new aggregates `cas22_tail_capital`/`cas22_capital`/`cas28_capital`/`cas2x_pre_contingency`/`cas20_capital`/`cas30_capital`/`cas23_to_28_capital`/`overnight_capital`/`idc_capital`. Rebased `contingency.direct_subtotal` → `cas2x_pre_contingency` and `indirect.direct_cost` → `cas20_capital`. `total_capital = overnight_capital` (Option C: `idc.cost` reported via `idc_capital`, NOT summed in). `idc` reads existing `discount_rate`+`construction_years` (=0.07/8, matching 1cfe CAS60). Staged twin rebuilt region-identical, re-anchoring the two Item-10 comment blocks.
- **Gate evidence.** Parse: both trees → **Checks passed!** `validate --level 1 models` → Errors 0 / Warnings 0 (PASS). Mirroring diff: staged-vs-canonical = ONLY the two sanctioned Item-10 comment blocks, nothing else. `git status`: only the 4 intended `.sysml`/csv files + plan changed — `ife_plant.sysml`/`hif_plant.sysml` untouched (their 3 pre-existing offenders ife:33/41 + hif:205 definitionally unchanged). `total_capital == overnight_capital` by construction; `lcoe_calc` + `mfe_lcoe_dcf.idc_factor` untouched. No STOP.
- **Deviations / offender-list note (surfaced, not a STOP).** (1) The design/probe bound `installation.reactor_subtotal = powercore_capital + remote_handling.cost` directly; Level-2 flagged this mixed-expression calc-input as a *new-kind* error ("bound to undefined attribute remote_handling"). Fixed idiomatically with an intermediate attribute `reactor_equipment_subtotal` (the WI-025 rollup pattern: calc inputs bind to a single attribute), which clears the error and reclassifies it into the accepted rollup-derived-expression category. (2) Per the design's explicit rule ("L2–L6 level flags may shift with the added defs/modules — compare the offender list, not the flags"): the mfe_plant Level-6 "Derived expression references design attributes" offenders grew (baseline 3 → ≥5 printed) — all are capital-rollup cross-part derived expressions (the "known rollup keys": `reactor_equipment_subtotal`, `cas22_tail_capital`, `cas2x_pre_contingency`, `cas30_capital`, `overnight_capital`, `idc_capital`…), the exact construct Phase-4 codegen exists to settle (D3). `L6_DESIGN_ATTR_INCOMPLETE` grew 75→91 (+16 = the new instance-bound generic attributes, bound at Phase 3 — the `divertor_base` split). Five Level-2 WARNs (ref_power/alpha literals on the shared `'Plant Power-Law Cost'` usages) are the accepted per-usage-constant style (same category as pre-existing hif_plant literal WARNs). No new NON-rollup offender; no new offender kind survives.

### Phase 3 — Stellaris instance bindings (both trees) — _(GATE PASSED)_
- **What ran.** Bound the 16 attribute bindings (11 accounts) in canonical `models/designs/stellarator_09/stellarator_plant.sysml`, placed just before the WI-025 "Rollup rates" block: `remote_handling_base` 150e6 + `concept_scale` 1.0; `installation_frac` 0.14; `coolant_primary_base` 166e6 + `coolant_intermediate_base` 40.6e6; `aux_per_mw` 1100.0 + `aux_cryo_base` 200e6; `waste_base` 1.96e6; `fuel_handling_base` 120e6; `other_rpe_base` 11.5e6; `inc_base` 85e6; `owner_base` 41.2e6; `supplementary_spares_frac` 0.03 + `supplementary_startup_base` 40e6 + `supplementary_decom_base` 272e6; `cas28_capital` 5e6. Each value re-verified against 1cfe at `0254385` (costing_constants.yaml + cas22.py/costs.py literals). Copied identical to the staged twin (byte-identical pre-edit, verified via `git show HEAD:`). Added 16 designs-scoped rows to `data/traceability_matrix.csv`.
- **Gate evidence.** Parse: both trees → **Checks passed!** Mirroring diff: instance staged-vs-canonical = empty (region-identical). MR-4: every binding carries an inline `**Source**`/`**Ref**`/`**Basis**` doc-comment to the pinned 1cfe constant (yaml line or cas22/costs.py line). MR-3: all 16 are instance bindings; `concept_scale` = 1.0 bound HERE (not a library default); no new library default introduced. `p_cryo` needs no instance binding — it is wired in the generic plant (`in p_cryo = cryo_elec.p_elec`, Phase 2), a plant-internal source, not a Stellaris literal. No STOP.
- **Deviations.** Traceability rows added to the CSV even though WI-025 kept instance-binding citations inline-only (the CSV previously had no `stellarator_plant.sysml` rows) — done to satisfy the Phase-3 checklist; the primary MR-4 chain remains the inline doc comments.

### Phase 4 — Mirroring diff gate + recapture + codegen-capture checkpoint — _(GATE PASSED, with design-mechanics fixes surfaced below)_
- **What ran.** Mirroring diff gate clean (only the 2 Item-10 comment blocks). Recaptured `stellarator.snapshot.json` from the staged tree via `sysml-codegen snapshot --models <abs staged models> ...` at pin `06d95f8`. Regenerated `generated/**` via `generate --from-snapshot ... --package-name stellarator_tea --pipeline-name mfe_stellarator --overwrite --preserve-handwritten`, after **deleting the AUTO_IMPLEMENTED=True auto-impls** first (so they regenerate fresh against the new structure while the one normative hand-written impl, `dt_fusion_power_impl.py` AUTO_IMPLEMENTED=False, is preserved by signature match).
- **Gate evidence.** Mirroring diff clean. Snapshot carries the new structure (`cas2x_pre_contingency`/`cas20_capital`/`cas30_capital`/`overnight_capital`/`total_capital`/`supplementary`/…) + `constraint_lowering_mode: applied` + the 5 constraint facts (`beta_ok`/`net_positive`/`recirc_ok`/`tbr_ok`/`wall_load_ok`). Generate **succeeds** — the 4-deep chain compiles to instance-scoped producers in correct topological order: `supplementary` reads `cas20_capital.root` + `cas23_to_28_capital.root` + `indirect__cost.root`; `overnight`/`total` read `cas30_capital ← indirect__cost.root`; `cas30←cas20←contingency←cas2x` resolve in order (no V11 abort). WI-022 `dt_fusion_power_impl.py` sha256 = `8d2357…794a9f` intact. L1 Errors 0; no orphan modules/impls; `total_capital_impl` regenerated to the overnight sum (Option C, idc excluded).
- **Deviations (design-mechanics fixes; faithful to intent, applied region-identical to both trees; SURFACED).** The design's D2 block is pseudocode; making it compile through sysml-codegen `06d95f8` required three mechanical adjustments, all value-preserving (Option C, 1cfe formulas, and the numeric intent unchanged):
  1. **Aggregates must reference sibling attributes, not calc `.cost` directly.** codegen classifies an attribute that mixes sibling attrs with cross-namespace calc `.cost` refs as `expose_computed` (no producer channel); `lcoe_calc.total_capital` (untouched) then dead-ends at V11. Fix: expose each consumed calc cost as a sibling `_capital` attribute (`owner_capital`, `supplementary_capital`, `remote_handling_capital` = the respective `.cost`), and write `overnight_capital`/`total_capital`/`reactor_equipment_subtotal` as sums of siblings → they become aggregation producers. This mirrors the existing model idiom (`contingency_capital = contingency.cost`, then aggregate).
  2. **`total_capital` written as the overnight aggregation, not a bare alias.** `total_capital = overnight_capital` (bare 1-ref alias) produces no channel; written as the 5-sibling overnight sum so codegen emits a `total_capital` producer. Still `== overnight_capital`, idc excluded (Option C); `idc_capital` reported-only; `mfe_lcoe_dcf.idc_factor` untouched.
  3. **Two calc inputs rebased onto producers.** `installation.reactor_subtotal` → `reactor_equipment_subtotal` (now a 2-sibling producer); `supplementary.cas30` → `indirect.cost` (the CAS30 producer) since `cas30_capital` is `expose_pure`. A calc reading a non-producer attribute surfaces the input as a null entry-point (would NaN the run); reading the producer wires it forward.
- **SURFACED to Phase 5 (harness), not a STOP.** A premature design-point smoke test (`run_stellaris_single.py`) then failed on 5 null SystemDesign inputs: `special_materials_capital`/`cas28_capital` are now surfaced as per-module entry points (`cas2x_pre_contingency__*`, `cas23_to_28_capital__*`) because each is consumed by two aggregations, whereas `run_stellaris_single.py:26` still injects only the retired `direct_capital__special_materials_capital` key. This is a harness-fill mismatch (the codegen structure is correct); the runner's injection glue must be updated for the new keys in Phase 5. Not a codegen/structural failure — generate and the chain compile are clean.

### Phase 5 — Harness + A-2 per-account measurement — _(GATE PASSED — resumed on fresh budget)_
- **What ran.** Re-checked-out the sysml-codegen pin (`06d95f8` — it had drifted to `d03defb` during the pause; A-6 restored). **Oracle** (`verify_stellaris.py`): rewrote the rollup to the D2 overnight assembly (all 8 tail accounts + CAS40 + CAS50 + CAS28 + Option-C total + the CAS60 idc line), added the account constants + return keys — an independent pure-Python re-derivation. **Emitter** (`emit_1cfe_point.py`): added the 12 CONST bases to `refs` (remote_handling/fuel_handling/owner/spares/startup/decom via `cc` accessors + shipping/tax/insurance/installation fracs + concept_scale). **Handshake** (`handshake_1costingfe.py`): 11 new CH channels; injection-map entries feeding every base ×1e6 at the 1cfe values (+ updated the `special_materials`/`cas28` per-module keys); 11 explicit A-2 comparison rows; the six D6 trap classes. **Runner** (`run_stellaris_single.py`): injection-glue fill-key update. Ran the handshake.
- **A-2 result (SV-034 core).** 11 newly-scoped accounts measured at the handshake point. **8 under A-2 (|rel dev| ≤ 1e-6):** remote_handling −3.23e-08, coolant +1.62e-08, aux_cooling −2.92e-08, waste +7.60e-08, fuel_handling −5.21e-08, other_rpe +2.86e-09, inc +7.95e-08, owner/CAS40 +3.51e-08. **3 A-4 remainders (fully diagnosed, not formula errors):** installation −1.98e-04 = 0.14·C220106_pump; supplementary/CAS50 −6.24e-05 = pump propagating via cas20/cas30; idc/CAS60 +1.89e-03 = the CAS10 +16M remainder (F-4) via overnight (Option C: reported, excluded from total_capital). Each miss reconstructs to 1cfe **exactly** when the documented remainder is added back (D6 traps: installation −3.12e-08, cas20 −2.01e-08, cas30 −1.38e-07).
- **Rollup:** at the handshake point cas20 = 5,710.12 M$ (target 5,710.946, short by 1.14·pump = 0.822 M$), cas30 = 1,522.70 M$ (target 1,522.919, short by the pump propagation), overnight = 7,887.07 M$ (target 7,872.149; +14.9 M$ = the CAS10 +16 M$ remainder net of the pump). All three deltas are the two A-4 remainders — no third source.
- **Six D6 traps all PASS:** fuel-keyed bases (DT); plant-total/per-module + ref-power split (8 clean accounts @ 1e-6); installation base = 0.14·Σ(C220101..110) [reconstructs +pump]; F-2/F-3 structural (cas28=5.0; cas20/cas30 reconstruct); CAS60 Option C (total==overnight, rel 0.0, idc reported-only). (Traps 1 and 2 are jointly asserted by the clean-account pass.)
- **A-4 remainder table** (reconciles the residual): (1) **C220106_pump** $0.721 M — vessel shell-only, standing WI-025 remainder; propagates into installation (0.14·pump), cas20/cas30 (via cas22_capital), supplementary. (2) **CAS10** model 34.5 vs 1cfe 18.5 M$ (+16.0 M$, F-4) — pre-existing WI-025 remainder, now isolated at overnight; propagates into overnight + the CAS60 idc line. (3) **CAS60/total_capital convention** (Option C, ruled) — the CAS60 account line is A-2-checked (reported); 1cfe folds CAS60 into `total_capital` (10,095.84 M$), the model keeps `total_capital = overnight` (7,872.15 M$) and folds IDC into the LCOE `idc_factor`. Residual reconciles to this itemized sum.
- **Deviations.** `run_stellaris_single.py` (design-point runner) was not pre-listed under Phase 5 but its injection glue required the new-key update. The D6 traps assert the CLEAN accounts at 1e-6 and prove the A-4 accounts reconstruct (rather than asserting all 11 at 1e-6), which is the A-4 path, not a loosened bar.

### Phase 6 — Re-baseline, standing-bars sweep, records — _(GATE PASSED)_
- **What ran.** Executed the design point + the full standing-bars sweep; re-baselined the comparison JSON as its own commit; filled SV-034.
- **New design-point headline (MR-WI028-9 re-baseline):** `total_capital = $16,145,706,216.04` (was 12,638,857,665.74); `LCOE = $258.013640/MWh` (was 203.647152); `p_net = 915.081088 MW`, `q_eng = 6.606662`, `rec_frac = 0.151362` **UNCHANGED** (physics spine); `magnet_capital = $6,323,469,946.33` unchanged, share 39.17%. All 5 constraint verdicts satisfied. Explicitly a re-baseline (new real accounts enter the rollup), NOT a regression.
- **Oracle bit-exact (MR-WI028-9):** every executed channel matches the independent pure-Python oracle at rel < 1e-9 at the new headline — total_capital 3.54e-16, lcoe 4.41e-16, p_net/q_eng/rec_frac 0.0, cas20_capital 3.17e-16, overnight_capital 3.54e-16. **PASS.**
- **G-8 re-baseline commit** `feb13ff3` (the only commit this item): `handshake_comparison.json` alone, message "WI-028 G-8 re-baseline:", body lists all 11 accounts absent→computed with signed magnitude and notes the injection map did not shrink (accounts were structurally absent, not previously injected). Comparison logic byte-unchanged (only rows + inputs).
- **Standing bars — all hold:** WI-022 `dt_fusion_power_impl.py` sha256 `8d2357…794a9f` intact (preserved via `--preserve-handwritten`); IFE **Run A 252.29996307 / Run B 68.69020165 byte-exact**, **Run C out-of-scope** (teax-vs-HIF validator skew, owner ruling 2026-07-20 — supersession recorded, not a fail); **pytest 11 failed / 18 passed / 14 skipped / 0 errors**; **L1 Errors = 0**, offender list = the 6 pre-existing (ife:33/41, hif:205, + the 3 mfe_plant rollup keys) + the design-accepted expanded rollup-key L6 set (Phase 2/4); **regen stability** — recapture byte-identical to the committed snapshot (only `captured_at` differs; 5 constraint facts intact); PROTOCOL honored (barred paths never read).
- **SV-034:** status `passing` (real status column set directly — the `pm update-validation` CLI mis-parsed the embedded `|rel dev|` pipes and corrupted the criteria field; reverted and edited the status column cleanly).

### Surfaced findings (surface-to-orchestrator)
1. **[RESOLVED in-item, faithful] The D2 rollup pseudocode does not compile as written through sysml-codegen `06d95f8`.** Making `total_capital`/`overnight_capital`/`cas22_capital` into instance-scoped aggregation producers that a runnable teax-simkit pipeline validates required, iteratively: (a) exposing every consumed calc `.cost` as a sibling `_capital` attribute and aggregating siblings (not calc `.cost`) — else `expose_computed`, no channel; (b) writing `total_capital` as the overnight sum, not a bare alias; (c) rebasing `installation.reactor_subtotal` → `reactor_equipment_subtotal` producer and `supplementary.cas30` → `indirect.cost` producer; (d) **inlining the CAS22 tail directly into `cas22_capital`** (which references `powercore_capital` → parts → instance scope) and **removing the intermediate `cas22_tail_capital`**, because an aggregation built only from calc-cost exposures with no transitive part reference compiles at part-def scope (`mfe_plant__MFE_Power_Plant__*`) and dead-ends the instance-level leaves. All four are value-preserving mechanical fixes (Option C, 1cfe formulas, numeric intent unchanged), applied region-identical to both trees. **Codegen aggregation-scoping heuristic (part-def vs instance) is the load-bearing subtlety here — worth an upstream note.**
2. **[RESOLVED on the continuation] Phases 5–6 completed.** The A-2 measurement, oracle re-baseline, G-8 commit, standing-bars sweep, and SV-034 are all done (see the Phase 5/6 records). 8 accounts under A-2; the 3 misses are the two pre-existing documented A-4 remainders (C220106_pump, CAS10 +16M) propagating, each reconstructing to 1cfe exactly. Nothing was tuned to pass. **Toolchain note:** the sysml-codegen pin drifted to `d03defb` during the pause and was restored to `06d95f8` before any codegen work (A-6). **CLI note:** `agentic-mbse pm update-validation` corrupts rows whose text contains `|` (the `|rel dev|` notation) — worked around by editing the status column directly; worth an upstream fix.

### Tree end state
- **Edited this item (both `.sysml` trees region-identical modulo the 2 sanctioned Item-10 comment blocks):** library `mfe_account_costs.sysml` (+7 defs), generic `mfe_plant.sysml` (D2 rebuild + producer-scoping fixes), instance `stellarator_plant.sysml` (+16 bindings). Recaptured `stellarator.snapshot.json` (staged tree) + regenerated `generated/**`. Harness: `verify_stellaris.py` (oracle → new rollup), `emit_1cfe_point.py` (refs), `handshake_1costingfe.py` (channels/rows/injection/traps), `run_stellaris_single.py` (fill keys + re-baselined anchors + oracle map). `handshake_comparison.json` (G-8 re-baselined — **committed** `feb13ff3`). `data/traceability_matrix.csv` (+23 rows). `modeling_project/VALIDATION_MATRIX.md` (SV-034 passing). This plan.
- **Untouched (verified):** `mfe_lcoe_dcf.sysml` `idc_factor`; `lcoe_calc`'s `total_capital` input; `ife_plant.sysml`/`hif_plant.sysml` (offenders unchanged); handshake comparison LOGIC (only rows/inputs added). WI-022 `dt_fusion_power_impl.py` sha256 `8d2357…794a9f` intact. sysml-codegen used read-only at pin `06d95f8`. **Only commit made: the G-8 re-baseline `feb13ff3`** (handshake_comparison.json alone); all other WI-028 edits remain staged-clean/uncommitted for the orchestrator to commit after owner close. Pins left checked out (sysml-codegen `06d95f8`, teax `07eb0ac`, agentic-mbse `4c18d61`, 1costingfe `0254385`).

ARTIFACT: work/active/WI-028_handshake-account-scope/plan.md
