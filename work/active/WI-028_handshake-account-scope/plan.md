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
- [ ] Confirm a clean tracked working tree (only `.orchestrate-logs/` untracked) as the restore point; record `git` HEAD of the fusion-tea repo.
- [ ] `~/1cfe/sysml-codegen`: check out `06d95f8`; record the exact commit + `git status` (worktree state) for SV-034.
- [ ] `~/1cfe/teax` (teax dep): check out `07eb0ac`; record commit.
- [ ] agentic-mbse `4c18d61`, 1costingFE `0254385`: confirm checked out; record.
- [ ] Confirm `SYSIDE_LICENSE_KEY` resolves: `set -a && source ~/1cfe/fusion-tea/.env && set +a`.

**Validation Checkpoint.**
- [ ] All four pins checked out and recorded (commit + worktree state for the two that moved).
- [ ] Parse smoke: `uv run python -m syside check models/` (baseline clean before any edit).

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
- [ ] Append `'Plant Power-Law Cost'` (inputs: base, power, n_mod, ref_power, alpha) — canonical + staged.
- [ ] Append `'Remote Handling Cost'` (base, concept_scale, p_et per-module, ref 1100, α 0.5) — both trees.
- [ ] Append `'Installation Labor Cost'` (installation_frac 0.14, reactor_subtotal) — both trees.
- [ ] Append `'Coolant Cost'` (primary_base, intermediate_base, p_net, p_th, n_mod, refs 1000/3500, α 0.55) — both trees.
- [ ] Append `'Aux Cooling Cost'` (aux_per_mw, p_th, cryo_base, p_cryo per-module, n_mod, ref 30, α 0.7) — both trees.
- [ ] Append `'Supplementary Cost'` (six fracs/bases + cas20, cas23_to_28, cas30, p_net, n_mod; input named `cas23_to_28` per F-1) — both trees.
- [ ] Append `'IDC Closed-Form Cost'` (interest_rate, construction_years, overnight_cost) — both trees.
- [ ] Each defaulted input (ref powers, exponents, `installation_frac`) carries an MR-4 doc-comment citation to the 1cfe source at pin `0254385` (`cas22.py:631-731`, `costs.py:239-297`).
- [ ] Confirm no Stellaris-specific literal appears in any def (MR-3); `concept_scale` is an input, not a default.
- [ ] Add the 7 defs to `data/traceability_matrix.csv` (library defs, source-cited).

**Test Requirements.** Structural parse test only (leaf defs). Their numeric correctness is graded by the Phase-5 A-2 bar end-to-end, not unit-tested here (the WI-025/WI-027 pattern).

**Validation Checkpoint.**
- [ ] `uv run python -m syside check models/library/analyses/mfe_account_costs.sysml` → **Checks passed!**
- [ ] `uv run python -m syside check exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` → **Checks passed!**
- [ ] Mirroring diff: the 7 appended defs are **region-identical** between the two files (only file-path context differs).

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
- [ ] Canonical: add the 8 tail account calc usages; add `cas22_tail_capital` / `cas22_capital` / `cas28_capital` / `cas2x_pre_contingency` / `cas20_capital` / `cas30_capital` / `cas23_to_28_capital` / `overnight_capital` per the D2 block.
- [ ] Canonical: rebind `contingency.in direct_subtotal` → `cas2x_pre_contingency`; rebind `indirect.in direct_cost` → `cas20_capital`.
- [ ] Canonical: add `owner` (CAS40) + `supplementary` (CAS50) usages at the overnight level; add `idc` (CAS60) usage reading `overnight_capital`, `cost` exposed as a reported line.
- [ ] Canonical: `total_capital = overnight_capital` (CAS60 `idc.cost` NOT summed in); `lcoe_calc` + `idc_factor` untouched.
- [ ] Staged twin: apply the **same regions**, keeping the Item-10 comment lines at `:400-403`/`:427`; no blind overwrite.
- [ ] Confirm dataflow stays unidirectional (design "Cross-file bindings": powers → accounts → cas2x → contingency → cas20 → indirect → cas30 → overnight → total_capital → LCOE; no cycle).

**Test Requirements.** Parse test both trees. The rebuild's numeric correctness is graded by Phase-4 compile + Phase-5 A-2 rollup match (`cas20→5710.95`, `cas30→1522.92`, `overnight→7872.15`).

**Validation Checkpoint.**
- [ ] `uv run python -m syside check` on both `mfe_plant.sysml` copies → **Checks passed!**
- [ ] `uv run agentic-mbse validate --level 1 models` → L1 offender list = the 6 pre-existing (the 3 canonical `mfe_plant.sysml` capital-rollup cross-part derived expressions may line-shift; `ife_plant.sysml:33/41`, `hif_plant.sysml:205`). **Zero new offenders** beyond the known rollup keys.
- [ ] Mirroring diff: staged-vs-canonical `mfe_plant.sysml` shows **only** the intended WI-028 rebuild + the known Item-10 comment divergence — nothing else.

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
- [ ] Bind all 11 base rows from the D5 table (8 tail + CAS40 + CAS50 + cas28) — canonical + staged, region-identical.
- [ ] Bind `concept_scale = 1.0`; bind `p_cryo` from `cryo_elec.p_elec`.
- [ ] Each binding carries an MR-4 `Source`/`Ref`/`Basis` citation to the 1cfe constant at `0254385` (mirror the WI-025 binding doc-comment style at `:271-308`).
- [ ] Add the 11 instance bindings to `data/traceability_matrix.csv` (designs-scoped, source-cited).
- [ ] Confirm no new base is a library default (MR-3: all Stellaris-specific values live here).

**Test Requirements.** Parse test both trees. Numeric correctness graded at Phase 5 (A-2).

**Validation Checkpoint.**
- [ ] `uv run python -m syside check` on both `stellarator_plant.sysml` copies → **Checks passed!**
- [ ] Mirroring diff: staged-vs-canonical `stellarator_plant.sysml` shows **only** the intended WI-028 bindings — nothing else.

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
- [ ] **Mirroring diff gate:** for all three edited `.sysml` region sets (library defs, `mfe_plant.sysml` rebuild, `stellarator_plant.sysml` bindings), staged-vs-canonical diff shows **only** the intended WI-028 edits + the known Item-10 comment lines (`mfe_plant.sysml:400-403/427`). Any other delta blocks recapture (design D2b).
- [ ] `set -a && source ~/1cfe/fusion-tea/.env && set +a` (license).
- [ ] Recapture: run the sysml-codegen `snapshot` CLI over `exploration/stellarator_e2e/models` → `exploration/stellarator_e2e/stellarator.snapshot.json`, from the **staged tree** (mirror the WI-027 Item-10 bridge-free recipe; no `--design-path-filter` per the WI-024 gotcha).
- [ ] Confirm the recaptured snapshot carries the new account/rollup structure (grep for the new attribute names: `cas2x_pre_contingency`, `cas20_capital`, `cas30_capital`, `overnight_capital`, the tail account usages) and still carries the 5 WI-027 constraint facts (`beta_ok`/`net_positive`/`recirc_ok`/`tbr_ok`/`wall_load_ok`, `constraint_lowering_mode: applied`).
- [ ] Generate: `sysml-codegen generate --from-snapshot` at `06d95f8`; confirm the 4-deep chain compiles — the `supplementary` producer reads instance-scoped `cas20_capital` and `cas30_capital`; `cas30`←`cas20`←`contingency`←`cas2x` resolve in correct topological order (design D3).
- [ ] Confirm generated constraint modules + aggregator still present (WI-027 carry-through); WI-022 `dt_fusion_power_impl.py` sha256 = `8d2357…794a9f` survives regen.

**Test Requirements.** Structural verification of the generated package (the checks above). No new pytest — generated modules are proven-template; correctness graded by the Phase-5 A-2 run.

**Validation Checkpoint.**
- [ ] Mirroring diff clean (only intended edits + Item-10 comments).
- [ ] Snapshot recaptured from the staged tree; carries the new structure + the 5 constraint facts.
- [ ] Generate succeeds; the 4-deep cross-calc chain compiles to instance-scoped producers in correct order.
- [ ] L1 offender list = the 6 pre-existing, zero new; WI-022 hash intact.

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
- [ ] `emit_1cfe_point.py`: add the 12 refs (11 bases + concept_scale), each read from the 1cfe config at `0254385` (drift-asserted, A-6).
- [ ] `handshake_1costingfe.py`: add the 11 channels (8 tail + CAS40 + CAS50 + CAS60) to `CH`; feed the new bases into the injection map (×1e6); add the 11 explicit comparison rows.
- [ ] Add all six D6 trap classes as assertions and to the trap table (MR-WI028-6 / A-5).
- [ ] **Execute** the handshake: `exploration/pipeline_spike/.venv-exec/bin/python handshake_1costingfe.py` (against the Phase-4 recaptured snapshot / generated package).
- [ ] **A-2 per-account (SV-034):** record each of the 8 tail accounts + CAS40 + CAS50 + CAS60 line's `rel_dev`; each under |rel dev| ≤ 1e-6 vs 1cfe float32 at the handshake point.
- [ ] **Rollup match:** confirm `cas20_capital → 5710.95`, `cas30_capital → 1522.92`, `overnight → 7872.15` (the direct/indirect rows move from −18.64% to ~0).
- [ ] **A-4 remainder table** (D7): itemize C220106_pump ($0.721M, standing), CAS10 (+16.0M / +86.5%, isolated at overnight, explained-and-kept), and the CAS60/`total_capital` convention difference (1cfe folds CAS60 into `total_capital` = 10095.84M; model keeps `total_capital = overnight = 7872.15M`, folds IDC into the LCOE `idc_factor`) — signed magnitudes; residual reconciles to the itemized sum.
- [ ] Confirm the six traps all assert-pass (no silent default).

**Test Requirements.** The A-2 per-account bar and the trap assertions ARE the regression tests for the new accounts. The rollup-match check is the regression guard for the D2 rebuild.

**Validation Checkpoint.**
- [ ] All 8 tail + CAS40 + CAS50 (+ CAS60 line) under |rel dev| ≤ 1e-6, recorded per account (SV-034).
- [ ] Rollup values reproduce 1cfe (cas20/cas30/overnight).
- [ ] Six D6 traps assert-pass; trap table updated.
- [ ] A-4 remainder table itemized with signed magnitudes; residual reconciles.

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
- [ ] **Execute the design point:** `exploration/pipeline_spike/.venv-exec/bin/python run_stellaris_single.py`; record the new headline (total_capital, LCOE, p_net, q_eng, magnet share).
- [ ] **Oracle bit-exact (MR-WI028-9):** every executed channel matches the pure-Python oracle at rel dev < 1e-9 **at the new headline**.
- [ ] **G-8 re-baseline (MR-WI028-8):** re-run the handshake; `handshake_comparison.json` gains the new rows; re-baseline as an **explicit standalone commit**; the diff matches the documented move list (each account absent→computed, signed magnitude); comparison logic byte-unchanged; note the injection map does not shrink for these accounts.
- [ ] **Design-point headline re-baseline recorded** (MR-WI028-9) — the new total_capital/LCOE, explicitly a re-baseline like WI-025, not a regression.
- [ ] **L1 offender list = 6 pre-existing, zero new** (compare the list, not level flags).
- [ ] **WI-022 sha256** `8d2357…794a9f` survives (re-confirm post-run).
- [ ] **IFE anchors:** Runs A/B byte-exact (252.29996307 / 68.69020165 / 270.12 as applicable; Meier 4.735); **Run C out-of-scope** — record the supersession (owner ruling 2026-07-20), do not treat as a failure.
- [ ] **pytest:** `uv run pytest tests/models/ -q` → **11 failed / 18 passed / 14 skipped / 0 errors**.
- [ ] **Regen stability:** re-capture to `/tmp` and diff vs committed snapshot — constraint facts + structure byte-identical (only `captured_at` / `document_path` metadata differ).
- [ ] **Fill SV-034:** the per-account A-2 table (Phase 5), the rollup match, the new design-point headline, and each standing-bar result; set status `passing` **only if** all in-scope bars held (IFE Run C supersession recorded, not counted as a fail) via `uv run agentic-mbse pm update-validation SV-034 --status passing`.
- [ ] Record the pins (Phase 0) and the PROTOCOL-honored note in the item record.

**Test Requirements.** This phase *is* the regression suite: oracle bit-exactness, L1 offender list, IFE anchors, pytest tally, regen stability. All must hold (Run C excepted by owner ruling).

**Validation Checkpoint (Levels 1–6 / spec Success Criteria).**
- [ ] `handshake_comparison.json` re-baselined as a standalone commit; move list documented; logic untouched.
- [ ] New headline recorded; oracle rel 1e-9 at the new point.
- [ ] All standing bars hold (Run C supersession recorded); SV-034 filled.

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

**Restore point.** _(fusion-tea HEAD + clean-tree confirmation; the four pins checked out, commit + worktree state for sysml-codegen `06d95f8` and teax `07eb0ac`.)_

### Phase 0 — Toolchain pins + restore point — _(GATE PASSED / BLOCKED)_
- **What ran.** _(pin checkouts; license resolve; baseline parse.)_
- **Gate evidence.** _(commits recorded; restore point captured; STOP if any pin unreachable.)_
- **Deviations.** _(…)_

### Phase 1 — Library calc defs (both trees) — _(GATE …)_
- **What ran.** _(7 defs appended to both `mfe_account_costs.sysml` files.)_
- **Gate evidence.** _(parse clean both trees; mirroring diff region-identical; MR-4 citations; MR-3 clean; traceability rows.)_
- **Deviations.** _(…)_

### Phase 2 — Generic-plant overnight rebuild (both trees) — _(GATE …)_
- **What ran.** _(D2 restructure in both `mfe_plant.sysml`; contingency/indirect rebased; CAS60 Option-C wired; Item-10 comments reconciled.)_
- **Gate evidence.** _(parse clean; L1 offenders = 6; mirroring diff = intended edits + Item-10 comments only; `total_capital == overnight_capital`; LCOE untouched.)_
- **Deviations.** _(…)_

### Phase 3 — Stellaris instance bindings (both trees) — _(GATE …)_
- **What ran.** _(11 bindings in both `stellarator_plant.sysml`; concept_scale; p_cryo.)_
- **Gate evidence.** _(parse clean; mirroring diff intended-only; MR-4 citations; MR-3 clean; traceability rows.)_
- **Deviations.** _(…)_

### Phase 4 — Mirroring diff gate + recapture + codegen-capture checkpoint — _(GATE …)_
- **What ran.** _(mirroring diff gate; snapshot recaptured from staged tree; generate at `06d95f8`.)_
- **Gate evidence.** _(mirroring diff clean; snapshot carries new structure + 5 constraint facts; 4-deep chain compiles to instance-scoped producers in correct order; L1 offenders = 6; WI-022 hash intact.)_
- **Deviations.** _(…)_

### Phase 5 — Harness + A-2 per-account measurement — _(GATE …)_
- **What ran.** _(emit refs; handshake channels/rows/injection/traps; handshake executed.)_
- **Gate evidence.** _(per-account A-2 table, each ≤ 1e-6; rollup match cas20/cas30/overnight; six traps pass; A-4 remainder table reconciles.)_
- **Deviations.** _(…)_

### Phase 6 — Re-baseline, standing-bars sweep, records — _(GATE …)_
- **What ran.** _(design point executed; comparison JSON re-baselined as standalone commit; SV-034 filled.)_
- **Gate evidence.** _(new headline; oracle rel 1e-9; G-8 move list; L1 offenders = 6; WI-022 hash; IFE A/B byte-exact + Run C supersession; pytest 11/18/14/0; regen stable.)_
- **Deviations.** _(…)_

### Surfaced findings (surface-to-orchestrator, not fixed)
- _(any STOP condition that fired: the exact error, why surfaced not fixed, the decision needed. Empty if none.)_

### Tree end state
- _(files edited this item; what stayed untouched — canonical vs staged, LCOE/idc_factor, sysml-codegen read-only; WI-022 hash; nothing committed beyond the noted G-8 re-baseline commit; orchestrator commits after owner close.)_

ARTIFACT: work/active/WI-028_handshake-account-scope/plan.md
