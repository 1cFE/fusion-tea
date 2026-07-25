---
Status: implemented
Created: 2026-07-25
Updated: 2026-07-25
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
  Review: ./design-review.md
  Orchestration: ../../orchestration/handshake-lcoe-construction.md
  Protocol: ../../../knowledge/holdout/aries-cs/PROTOCOL.md
---

# WI-029 Plan — Handshake LCOE construction: CAS70/80 + IDC (STELLARATOR-DEMO Item 4)

**Required reading honored.** `knowledge/holdout/aries-cs/PROTOCOL.md` §3 barred paths were not read, cited, or opened while writing this plan, and stay barred through implement. Admissible surfaces only: the staged demo package under `exploration/stellarator_e2e/`, canonical `models/`, the 1costingFE editable dep at pin `0254385` (the ARIES-lineage exception already scoped in §3, C220107 excluded/footnoted at hold-out), and the sysml-codegen / teax / agentic-mbse deps at their pins.

## Source Documents

- **Design (primary input):** `./design.md` — approved rev 3 (commit `c2aad0b6`). All gates ruled. Load-bearing sections for implement: the **CAS72 codegen-envelope ruling** (rung table + "Guards are carried, not dropped"), the **CAS10 root-cause ruling**, the **IDC ruling — Option (ii)**, **D1** (three calc defs), **D2** (LCOE-side wiring + Option-(ii) channels), **D2b** (staged-twin propagation), **D3** (harness), **D4** (trap table, including traps 1b and 5), **D5** (CAS10 bounded fix), **D6** (verdict artifact), the **Cross-file bindings** table, and the **Validation plan**. Do not reopen the settled decisions.
- **Design review:** `./design-review.md` — must-fixes M1 (guards carried verbatim in impl *and* oracle mirror) and M2 (explicit `annual_om = 54.900` trap) are applied in rev 3 and are gated below.
- **Spec:** `./spec.md` — MR-WI029-1…11, Scope Boundaries, the criterion-3 verdict deliverable, Success Criteria, SV-035.
- **Orchestration brief:** `../../orchestration/handshake-lcoe-construction.md` — Align rulings 1–5, the **owner IDC gate ruling (Option ii, 2026-07-25)**, the CAS10 stop condition verbatim, the stage log, standing bars, toolchain quirks.
- **Upstream pattern:** `work/completed/20260720_WI-028_handshake-account-scope/plan.md` — the phase-gate/STOP pattern, the D2b two-tree rule, and the four codegen-mechanics adaptations precedent (that plan's Surfaced finding 1).
- **Epic (tracking home):** `.project/backlog/epic_stellarator_mbse_demo.md`, Item 4. **Governing frame:** `.project/concepts/stellarator-mbse-demo.md`, criterion 3, graded against the ratified anchor bars A-2/A-3/A-4/A-5/A-6 + G-8 in `.project/active/demo-anchor-acceptance-spec/spec.md`.

## Design Summary

Bring the annual-cost side of LCOE under the 1costingFE handshake: **CAS71** (levelized O&M) and **CAS80** (levelized DT fuel) as flat-Real codegen defs sharing one levelization wrapper; **CAS72** (levelized scheduled replacement, $82.23M) on the WI-022 handwritten rung because `ceil` breaks the codegen arithmetic envelope, with every 1cfe guard carried verbatim in both the impl and the oracle mirror; **CAS90/LCOE** reconciled under the ruled **Option (ii)** — the DCF headline stays untouched and 1cfe-form `cas90_1cfe` / `lcoe_1cfe` comparison channels are added, reusing the Item-3 CAS60 reported line; and the **CAS10** divergence closed as one clean error (`precon_fixed_base` 32M→16M). The deliverable is the **criterion-3 verdict in the A-4 form** with the reconciliation arithmetic shown. Rationale, the independent re-derivation, findings D1-a/D1-b, and the rejected alternatives are in the design — not repeated here.

## Prototype Baseline (design stage)

Per the design's Validation Report: the two flat-Real Rung-A defs parse clean; the 1cfe assembly is independently reproduced to float32 for all six outputs; the CAS10 reconstruction test lands residual 0.0. **Codegen capture was NOT run at design** (correctly, not fabricated) — it is this plan's Phase 5. The handwritten CAS72 impl and its oracle mirror do not exist yet — Phase 6.

| File | Role | State entering implement |
|---|---|---|
| `work/active/WI-029_handshake-lcoe-construction/prototype/wi029_lcoe_construction.sysml` | `'Levelized Annual Cost'` + `'DT Fuel Cost'` stencils | **parse-clean**; source-of-truth for Phase 1's two Rung-A defs |
| canonical `models/library/analyses/mfe_account_costs.sysml` | library, 20 calc defs post-WI-028 | append the 3 new defs (Phase 1) |
| staged `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` | **codegen input twin** (path drops `library/`) | region-identical append (Phase 1) |
| canonical `models/designs/generic_mfe/mfe_plant.sysml` | generic plant; `annual_om` bound unlevelized at `:571` | LCOE-side rewiring + Option-(ii) channels (Phase 2) |
| staged `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` | **codegen input twin** | same regions; carries the sanctioned Item-10 comment blocks (keep) |
| canonical `models/designs/stellarator_09/stellarator_plant.sysml` | Stellaris instance; `precon_fixed_base = 32000000.0` at `:631` | new bindings (Phase 3) + CAS10 fix (Phase 4) |
| staged `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` | **codegen input twin** | same, region-identical |
| canonical + staged `.../mfe_lcoe_dcf.sysml` | DCF headline, `idc_factor` at `:47-52` | **UNTOUCHED** (Option ii) — asserted by trap 5 |
| `exploration/stellarator_e2e/stellarator.snapshot.json` | codegen input, captured at WI-028 close | recapture from the staged tree (Phase 5) |
| `exploration/stellarator_e2e/generated/handwritten/**` | 20 `*_impl.py`; WI-022 `dt_fusion_power_impl.py` sha256 `8d2357…794a9f` | new `levelized_replacement_cost_impl.py` filled by hand (Phase 6) |
| `exploration/stellarator_e2e/{emit_1cfe_point.py, handshake_1costingfe.py, verify_stellaris.py, run_stellaris_single.py}` | harness + oracle + design-point runner | refs / channels / rows / traps / oracle mirror (Phases 6–7) |
| `exploration/stellarator_e2e/handshake_comparison.json` | handshake output @ `feb13ff3` | G-8 re-baseline as its own commit (Phase 8) |
| `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` | stale (Jul 18, pre-WI-028 numbers) | rewritten as the criterion-3 verdict artifact (Phase 7/8) |
| `modeling_project/VALIDATION_MATRIX.md` | SV registry | SV-035 registered `pending`, row filled at Phase 8 |

Level 4–6 issues to address by phase: **L5 documentation / traceability** (MR-4 citations on every new base and def) → Phases 1, 3, 4; **L6 architecture** (the new cross-calc producers and the handwritten-rung leaf) → the Phase-5 codegen-capture checkpoint; **library/designs separation** (MR-3 — defs concept-agnostic, all fuel/replacement constants are instance inputs) → Phases 1 and 3.

## Phasing Approach

Nine phases (0–8) following the WI-028 pattern: each ends at a **mechanically checkable state** with a hard gate and a named STOP condition. Four orderings bind:

1. **Pins first, as worktree checkouts (Phase 0).** Three of four upstream pins were already drifted at design time and five more days have passed — sysml-codegen has since moved again (design recorded HEAD `936315c`; it is now `fa9e0d0` on branch `nested-override-tripwire`), and **no worktree sits at `06d95f8`**. Codegen and exec run against a worktree checked out at the pin, never against a drifted HEAD (A-6). Adopting a newer HEAD is an owner-visible decision, never a side effect.
2. **Both trees, region-identical, every `.sysml` edit (D2b).** Codegen reads the staged twin; a canonical-only edit is a silent wrong result. This is a per-phase gate, not a final reconcile.
3. **The codegen-capture checkpoint (Phase 5) runs before every numeric phase.** Three things must capture cleanly: the two new flat-Real defs must lower, `'Levelized Replacement Cost'` must route to `MANUAL_REQUIRED` with a stub, and the Option-(ii) comparison channels must become producers. WI-028 hit **four** codegen-mechanics adaptations at exactly this checkpoint (aggregations must reference sibling attributes not calc `.cost`; no bare-alias attributes; calc inputs must read producers; an aggregation with no transitive part reference compiles at part-def scope). Expect the same class of issue on the new channels — apply value-preserving adaptations, region-identical in both trees, and record each.
4. **The handwritten rung (Phase 6) is filled and oracle-mirrored before any A-2 number is trusted (Phase 7).** A stub that silently returns a default would read as a formula error at measurement.

Bottom-up within that spine: library defs → generic plant → instance bindings → CAS10 fix → capture → handwritten rung → measurement → re-baseline/records.

## Validation Strategy

- **Per phase:** parse (`uv run python -m syside check`) after every `.sysml` phase (1–4); the staged-vs-canonical mirroring diff after every two-tree edit; codegen compile at Phase 5; the oracle rel-1e-9 agreement plus the guard-live spot-check at Phase 6; the A-2 numeric bar and the trap table at Phase 7; the full standing-bars sweep at Phase 8.
- **The load-bearing gates** are Phase 5 (does the CAS72 def route to `MANUAL_REQUIRED` and do the Option-(ii) channels become producers), Phase 6 (does the handwritten impl reproduce the closed form and agree with the mirror at rel 1e-9, guards live), and Phase 7 (A-2 |rel dev| ≤ 1e-6 per account plus the A-4 reconciliation — the SV-035 deliverable and the criterion-3 verdict).
- **The 6-level pyramid, scoped:** L1 runs at Phases 2–5 and again in the Phase-8 sweep. Per the WI-027/WI-028 precedent, compare the **offender list** (expected = the 6 pre-existing + WI-028's design-accepted rollup-key L6 set), not the level flags.
- **Final (Phase 8):** the full standing-bars set on one executed run.

## Rollback / Surface Posture (all phases)

Every edit is git-tracked; rollback is `git checkout -- <paths>` at any phase. **No bar is ever made to pass by moving the model or the design point** — MR-WI029-9 is a re-baseline, not a licence to tune. Named **surface-to-orchestrator** conditions — stop the phase, report, do not work around:

- **A pin is unreachable or a pin worktree cannot be created** at Phase 0, or the 1cfe drift-assert trips at run (A-6).
- **A staged↔canonical delta** at any mirroring gate beyond the intended WI-029 edits + the known Item-10 / DEMO-NOTE divergences (D2b: any other delta blocks recapture).
- **Codegen abort, or the CAS72 def does NOT route to `MANUAL_REQUIRED`**, or a comparison channel fails to become a producer after value-preserving adaptation (Phase 5).
- **The handwritten impl and the oracle mirror disagree beyond rel 1e-9**, or the guard-live spot-check shows a guard is not actually binding in one of the two (Phase 6) — this is the M1 must-fix made mechanical.
- **CAS10 does not reconstruct 18.5 with residual 0.0** at the handshake point (Phase 7). This is the **owner stop condition, verbatim: "please try (a) but stop if there is not a clear resolution."** If it does not reconstruct cleanly: revert `precon_fixed_base` to 32000000.0, restore CAS10 to explained-remainder treatment in the A-4 table, and park for owner. Do not force it.
- **An account cannot meet A-2 for a non-float32 reason** at Phase 7 (a real formula or mapping error) — surface. A legitimate float32-ceiling miss is itemized under A-4, not surfaced as a failure.
- **A standing bar breaks** at Phase 8 that this item did not intend to move — oracle rel 1e-9 fails, a new L1 offender appears, the WI-022 sha256 changes, IFE Run A/B moves, the pytest tally shifts for a model reason.

---

## Phase 0 — Pin verification, worktree checkouts, restore point

**Overview.** Establish the exec baseline before touching anything. All four pins must be reachable and checked out **in a worktree at the pin**, because three upstream HEADs are off-pin and none of the existing worktrees sits at a pin commit.

**Design Reference.** See design §"Toolchain pins (verified live this stage — DRIFT on three of four)". Key points:
- Pins: **sysml-codegen `06d95f8`**, **teax `07eb0ac`**, **agentic-mbse `4c18d61`**, **1costingFE `0254385`**.
- Lowering behaviour is unchanged pin↔HEAD (the whole `sysml-codegen/src/sysml_codegen/extraction/` directory diffs to nothing), but the pin discipline binds regardless — run against the pin object.

**Pin state re-verified 2026-07-25 (plan stage), for the implementing agent to re-check, not inherit:**

| Tool | Pin | Live HEAD now | Pin reachable | Pin ancestor of HEAD | Worktree at pin |
|---|---|---|---|---|---|
| 1costingFE | `0254385` | `0254385` (master, clean) | ✓ | ✓ (HEAD == pin) | main checkout on pin |
| sysml-codegen | `06d95f8` | `fa9e0d0` (branch `nested-override-tripwire`; moved again since design's `936315c`) | ✓ object | **NOT** | **none** |
| teax | `07eb0ac` | `fa0e06a` (main, clean) | ✓ object | **NOT** | **none** |
| agentic-mbse | `4c18d61` | `f4ebdce` (main) | ✓ object | **NOT** | **none** |

**Checklist.**
- [x] Record the fusion-tea restore point: `git rev-parse HEAD` (expected `c2aad0b6`, branch `feat/stellarator-mbse-demo`) and a clean tracked tree (only `.orchestrate-logs/` and the untracked status report).
- [x] Re-verify each pin is reachable as an object (`git cat-file -t <pin>`) and record whether HEAD has drifted further since this plan was written. **STOP if any pin is unreachable.**
- [x] Create/checkout a **worktree at the pin** for sysml-codegen `06d95f8` (per the worktree convention: `{repo}-{worktree-name}` parallel to the repo, e.g. `~/1cfe/sysml-codegen-wi029-pin`). Record the worktree path + `git -C <worktree> rev-parse HEAD`.
- [x] Same for teax `07eb0ac` and agentic-mbse `4c18d61`; record paths and commits. If a repo's main checkout can be safely put on the pin instead (clean tree, no other consumer), record which mechanism was used.
- [x] Confirm 1costingFE is on `0254385` with a clean tree; record.
- [x] Record the pre-existing dirty files in each upstream repo (sysml-codegen 1, agentic-mbse 1 at plan time) so nothing this item does is confused with them.
- [x] Confirm the license resolves: `set -a && source ~/1cfe/fusion-tea/.env && set +a` (`SYSIDE_LICENSE_KEY` non-empty).
- [x] Confirm the exec venv exists: `exploration/pipeline_spike/.venv-exec/bin/python --version`.

**Validation Checkpoint.**
- [x] All four pins reachable; worktrees created/recorded for the three drifted ones; every codegen/exec step downstream names the worktree path it ran from.
- [x] Baseline parse smoke: `uv run python -m syside check models/` → clean (only the pre-existing namespace-distinguishability warnings `f_shape`, `lt_shield_t`).

**Phase Completion Gate.** Four pins recorded, three pin worktrees live, license + exec venv resolved, restore point captured, baseline parse clean. **STOP-and-report** if any pin is unreachable, a worktree cannot be created at a pin, or the baseline parse shows an error the tree did not have at WI-028 close.

---

## Phase 1 — Library calc defs (both trees, D1)

**Overview.** Add the three concept-agnostic defs the plant will consume. Two are flat-Real (Rung A, codegen); one is the handwritten rung (Rung B). Leaf definitions land first.

**Design Reference.** See design **D1** (the calc-def → accounts table and the three bullet specs). Key points:
- `'Levelized Annual Cost'` is used **twice** — once with `annual_cost = om_cost.annual_om` (→ CAS71), once with `annual_cost = fuel_calc.annual_fuel` (→ CAS80). One def, two usages (MR-3).
- `'DT Fuel Cost'` takes the fuel constants as **inputs**, not library defaults (MR-3); the burn correction is `×(1 + (1−burn)/burn·(1−recovery))`.
- `'Levelized Replacement Cost'` **deliberately** carries the non-envelope invocations (`ceil`, `clip`, `max`) in its body so codegen routes it to `MANUAL_REQUIRED` — the WI-022 `'DT Fusion Power'` pattern. Do not "simplify" the guards out of the def to make it lower; routing to the manual rung is the ruled design.

**Files to Create/Modify.**
- REFINE `models/library/analyses/mfe_account_costs.sysml` (append after the WI-028 defs).
- REFINE `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` (**path drops `library/`**) — region-identical append.

**Checklist.**
- [x] Append `'Levelized Annual Cost'` (inputs: annual_cost, interest_rate, inflation_rate, operational_years, project_time; body per D1: `disc_pow_n`, `crf`, `a1`, `pv`, `levelized`) — canonical + staged. Transcribe the executable body byte-for-byte from the parse-clean prototype.
- [x] Append `'DT Fuel Cost'` (inputs: p_fus, n_mod, availability, cost_per_rxn, q_eff, mev_to_joules, burn_fraction, fuel_recovery) — both trees, body from the prototype.
- [x] Append `'Levelized Replacement Cost'` (inputs: cost_per_event, p_neutron, firstwall_area, fluence_limit, availability, interest_rate, operational_years) — both trees. Body declares the full guarded closed form: `q_n`, `core_lifetime_FPY = clip(fluence_limit/max(q_n,1e-6), 0.5, n·avail)`, `core_lifetime_cal`, `s`, `n_rep = max(0, ceil(n/t)−1)`, `pv`, `cost`.
- [x] Every defaulted input and every def carries an MR-4 `**Source**`/`**Ref**`/`**Basis**` doc comment citing 1cfe at pin `0254385` (`economics.py:13-50`, `economics.py:53-75`, `model.py:102-111`, `costs.py:476-544`), matching the WI-028 library house style.
- [x] Confirm no Stellaris-specific literal appears in any def (MR-3) — fuel constants, fluence limit, and the replaceable-account set are instance inputs.
- [x] Add the 3 defs to `data/traceability_matrix.csv` (library-scoped, source-cited).

**Test Requirements.** Structural parse only. Numeric correctness is graded end-to-end by the Phase-7 A-2 bar (the WI-025/WI-027/WI-028 pattern), and for CAS72 additionally by the Phase-6 oracle mirror.

**Validation Checkpoint.**
- [x] `uv run python -m syside check models/library/analyses/mfe_account_costs.sysml` → **Checks passed!**
- [x] `uv run python -m syside check exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml` → **Checks passed!**
- [x] Mirroring diff: the three appended defs are region-identical between the two files.

**Phase Completion Gate.** Both library files carry the three defs, parse-clean, region-identical, MR-4-cited, MR-3-clean. **STOP-and-report** on a parse failure the prototype did not exhibit (a botched transcription), or if `'Levelized Replacement Cost'` cannot be expressed with its guards at all in SysML — that would change the ruled rung assignment and is an owner-visible design question, not an implement workaround.

---

## Phase 2 — Generic-plant LCOE-side wiring + Option-(ii) channels (both trees, D2)

**Overview.** Wire the four calc usages and the CAS70 aggregate into `mfe_plant.sysml`, and add the two 1cfe-form comparison channels. The DCF headline is deliberately left alone — that is the ruled Option (ii), and trap 5 will assert it.

**Design Reference.** See design **D2** (the wiring block), the **IDC ruling — Option (ii)** section (what is added vs what stays untouched), and the **Cross-file bindings** table. Key decisions (do not re-derive):
- `cas71_calc`, `fuel_calc`, `cas80_calc`, `cas72_calc` usages; `cas70 = cas71 + cas72`.
- `cost_per_event` = the modeled C220101 (blanket) + C220108 (divertor) accounts × `n_mod` — both already modeled from WI-028's cas22 work.
- `cas90_1cfe = crf * (overnight_capital + idc.cost)` reusing the **Item-3 CAS60 reported line** — no new IDC arithmetic, and `crf` is the one the DCF core already computes (`mfe_lcoe_dcf.sysml:42-43`).
- `lcoe_1cfe = (cas90_1cfe + cas70 + cas80) * 1e6 / (8760 * p_net * n_mod * availability)`.
- **UNTOUCHED:** `'LCOE DCF'` usage, its `total_capital` input, and `mfe_lcoe_dcf.sysml`'s `idc_factor` at `:47-52`. `total_capital` stays `== overnight_capital` (Option C stands).
- Today's `mfe_plant.sysml:571` binds `annual_om = om_cost.annual_om` (unlevelized) into `'LCOE DCF'`. Per Option (ii) the DCF headline now takes the **levelized** CAS70 side; the design's D2 block is the specification — follow it exactly and record the exact binding you land as a checked item, since this is the one place the headline value legitimately moves.

**Prototype Baseline (this phase).** The staged twin carries the sanctioned Item-10 / DEMO-NOTE comment blocks — **keep them**, reconcile rather than blind-overwrite (the known staged↔canonical divergence, not a defect).

**Files to Create/Modify.**
- REFINE `models/designs/generic_mfe/mfe_plant.sysml`.
- REFINE `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` (reconcile Item-10 comment lines).

**Checklist.**
- [x] Canonical: add `cas71_calc` / `fuel_calc` / `cas80_calc` / `cas72_calc` usages per D2, with their sibling `_capital`-style exposure attributes following the WI-028 producer idiom (see Phase 5 note — expect codegen to require sibling-attribute aggregation).
- [x] Canonical: add `cas70` aggregate = `cas71 + cas72`.
- [x] Canonical: bind `cas72_calc.cost_per_event` from the modeled C220101 + C220108 accounts × `n_mod`.
- [x] Canonical: add `cas90_1cfe` and `lcoe_1cfe` comparison channels reusing `idc.cost` and the DCF `crf`.
- [x] Canonical: verify `mfe_lcoe_dcf.sysml` is **not** edited and `total_capital == overnight_capital` still holds by construction.
- [x] Staged twin: same regions, keeping the Item-10 comment blocks.
- [x] Confirm dataflow stays unidirectional (design "Cross-file bindings": physics/powers → fuel/replacement/O&M → levelization → cas70/80 → LCOE; the CAS72 rung is a leaf producer). No cycles.

**Test Requirements.** Parse both trees. Numeric correctness graded at Phase 7.

**Validation Checkpoint.**
- [x] `uv run python -m syside check` on both `mfe_plant.sysml` copies → **Checks passed!**
- [x] `uv run agentic-mbse validate --level 1 models` → L1 Errors 0; offender list = the 6 pre-existing + WI-028's design-accepted rollup-key L6 set. **Zero new offender kinds.**
- [x] `git diff` confirms `mfe_lcoe_dcf.sysml` (both trees) is untouched.
- [x] Mirroring diff: staged-vs-canonical shows only the intended WI-029 edits + the known Item-10 divergence.

**Phase Completion Gate.** Both `mfe_plant.sysml` copies carry the four usages, the `cas70` aggregate, and the two Option-(ii) channels; parse-clean; region-identical modulo Item-10 comments; `mfe_lcoe_dcf.sysml` untouched; L1 offender list unchanged. **STOP-and-report** on a new L1 offender kind or a mirroring delta beyond the intended edits.

---

## Phase 3 — Stellaris instance bindings (both trees, D1/D2 inputs)

**Overview.** Bind the new instance-scoped inputs the three defs need, as MR-4-cited conversions of the pinned 1cfe constants, next to the WI-025/WI-028 binding blocks.

**Design Reference.** See design **Cross-file bindings** table and **D1**'s per-def input lists. Key points: `inflation_rate` is a NEW instance input (0.02); the DT fuel constants and `fluence_limit_dt` are instance inputs, never library defaults (MR-3); availability is the instance's 0.85 at the design point and the injected 0.9 at the handshake point — the binding carries the difference, it is not frozen.

**Files to Create/Modify.**
- REFINE `models/designs/stellarator_09/stellarator_plant.sysml`.
- REFINE `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` (region-identical).

**Checklist.**
- [x] Bind `inflation_rate = 0.02` — canonical + staged, MR-4-cited to the 1cfe config at `0254385`.
- [x] Bind the DT fuel constants: `cost_per_rxn` (or its components `M_D_KG·u_deuterium` + `M_Li6_KG·u_li6`), `q_eff = Q_DT = 17.58`, `MEV_TO_JOULES`, `burn_fraction = 0.05`, `fuel_recovery = 0.99` — each MR-4-cited to `defaults.py` / `costs.py:476-544`.
- [x] Bind `fluence_limit_dt = 18.0` (`defaults.py:291`), MR-4-cited.
- [x] Confirm `p_neutron` and `firstwall_area` reach `cas72_calc` from the modeled physics chain (no new instance literal).
- [x] Confirm the replaceable set {C220101, C220108} is expressed as the modeled account references from Phase 2, not as a frozen dollar literal (`defaults.py:299`).
- [x] Every binding carries an inline `**Source**`/`**Ref**`/`**Basis**` doc comment (WI-028 style).
- [x] Add the new instance bindings to `data/traceability_matrix.csv` (designs-scoped).
- [x] Confirm no new library default was introduced (MR-3).

**Test Requirements.** Parse both trees. Numeric correctness graded at Phase 7.

**Validation Checkpoint.**
- [x] `uv run python -m syside check` on both `stellarator_plant.sysml` copies → **Checks passed!**
- [x] Mirroring diff: instance staged-vs-canonical shows only the intended WI-029 bindings.

**Phase Completion Gate.** Both instance files carry the new bindings, parse-clean, region-identical, MR-4-cited, MR-3-clean. **STOP-and-report** on a mirroring delta or a parse failure.

---

## Phase 4 — CAS10 bounded fix (both trees, D5)

**Overview.** Apply the ruled single-error correction. It is its own phase because it carries the **owner stop condition** and its own numeric gate, and because it moves the design-point headline by a known $16M — that must be attributable to this edit and nothing else.

**Design Reference.** See design **CAS10 root-cause ruling** ("Bounded fix (both trees, D2b)") and **D5**. Key points:
- **One** binding changes: `precon_fixed_base` 32000000.0 → 16000000.0 (`models/designs/stellarator_09/stellarator_plant.sysml:631` + staged twin). This is `plant_studies` FOAK 20 → NOAK 4.
- Doc amendments (FOAK → NOAK) at the binding and at `mfe_account_costs.sysml:364` + its twin — **documentation hygiene, changing no number**.
- The model applies no CAS10 contingency (deferred to CAS29 = 0 at NOAK) and that is already correct — do not add one.
- Expected consequence, recorded not asserted-away: `overnight_capital = total_capital` drops by exactly $16M at the design point too (≈$16,129.7M), because `precon_fixed_base` is power-independent.

**Files to Create/Modify.**
- REFINE `models/designs/stellarator_09/stellarator_plant.sysml` (`:631` value + doc).
- REFINE `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` (same region).
- REFINE `models/library/analyses/mfe_account_costs.sysml` (`:364` stale FOAK doc note → NOAK) + staged twin.

**Checklist.**
- [x] Canonical + staged: `precon_fixed_base` 32000000.0 → 16000000.0, one value, nothing else in the calc changed.
- [x] Amend the binding's doc comment: itemize the NOAK adders (site_permits 3 + licensing_dt 5 + plant_permits 2 + **studies_noak 4** + plant_reports 1 + other_precon 1 = 16.0), cited to `costs.py:52-80` / `defaults.py` at pin `0254385`.
- [x] Amend the stale "1cfe full CAS10 = subtotal × 1.10 exactly" FOAK note at `mfe_account_costs.sysml:364` + twin to the NOAK basis (contingency_rate_noak = 0.0); confirm no number changes.
- [x] Arithmetic pre-check (paper, before any run): land 0.25·√(1000·1·1000)·10000/1e6 = 2.5 + fixed 16.0 = **18.5**, residual 0.0 vs 1cfe c10.
- [x] Confirm nothing else in the CAS10 chain moved (`git diff` scoped to the two edited regions).

**Test Requirements.** Parse both trees. The **executed** reconstruction gate runs at Phase 7 (it needs the handshake); it is named here and carried forward.

**Validation Checkpoint.**
- [x] `uv run python -m syside check` on both instance + both library files → **Checks passed!**
- [x] Mirroring diff clean on all four files.
- [x] Arithmetic pre-check gives 18.5 exactly.

**Phase Completion Gate.** The single value is changed in both trees, the doc notes are NOAK-correct, the arithmetic pre-check reconstructs 18.5 with residual 0.0. The **executed gate — model CAS10 = 18.5 at the handshake point, residual 0.0 — is carried to Phase 7.** **STOP-and-report** under the verbatim owner stop condition ("please try (a) but stop if there is not a clear resolution") if the arithmetic does not reconstruct cleanly, or if landing the fix requires touching more than `precon_fixed_base` — either would mean it is not one clean error. Revert to 32000000.0, restore CAS10 to explained-remainder treatment, park for owner.

---

## Phase 5 — Mirroring diff gate + snapshot recapture + codegen-capture checkpoint

**Overview.** The load-bearing structural gate (design Validation Plan step 2). Confirm the whole Phase 1–4 edit set landed region-identical in the staged tree, recapture `stellarator.snapshot.json` **from the staged tree**, generate at the pin, and confirm three things: the two flat-Real defs lower, `'Levelized Replacement Cost'` routes to `MANUAL_REQUIRED` with a stub, and the Option-(ii) channels compile to instance-scoped producers.

**Design Reference.** See design **D2b**, the **CAS72 codegen-envelope ruling** (the `MANUAL_REQUIRED` routing at `expression_compiler.py:255-311`), and Validation plan step 2. Key points:
- Codegen's input is the **staged twin**, not canonical `models/` — recapture is mandatory.
- Run snapshot + generate via the sysml-codegen CLI **at the Phase-0 pin worktree** (`06d95f8`), from the exec context with `SYSIDE_LICENSE_KEY` set. No `--design-path-filter` (WI-024 gotcha).
- WI-028 precedent for regen: delete the `AUTO_IMPLEMENTED=True` auto-impls first so they regenerate fresh, and pass `--preserve-handwritten` so `AUTO_IMPLEMENTED=False` impls survive by signature match.

**Expect codegen-mechanics adaptations.** WI-028 needed four at this checkpoint (see its plan's Surfaced finding 1): aggregations must sum **sibling attributes**, not cross-namespace calc `.cost`; a bare 1-ref alias attribute produces no channel; a calc input reading a non-producer surfaces as a null entry point; an aggregation built only from calc-cost exposures with no transitive part reference compiles at part-def scope and dead-ends the instance leaves. The new `cas70`, `cas90_1cfe`, and `lcoe_1cfe` aggregates are exactly this shape. **Any adaptation must be value-preserving** (the ruled Option (ii), the 1cfe formulas, and the numeric intent unchanged), applied **region-identical to both trees**, and recorded in the Implementation Record as a surfaced finding.

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/stellarator.snapshot.json` (recaptured from the staged tree).
- REFINE `exploration/stellarator_e2e/generated/**` (machine-produced; no hand-edits in this phase).
- Possibly REFINE the Phase 1–3 `.sysml` files if a value-preserving adaptation is needed (both trees, then re-run this phase).

**Checklist.**
- [x] **Mirroring diff gate:** for all edited region sets (library defs + `:364` doc, `mfe_plant.sysml` wiring, `stellarator_plant.sysml` bindings + CAS10), staged-vs-canonical shows **only** the intended WI-029 edits + the known Item-10 / DEMO-NOTE divergences. Any other delta blocks recapture.
- [x] `set -a && source ~/1cfe/fusion-tea/.env && set +a`.
- [x] Re-verify the sysml-codegen pin worktree is still at `06d95f8` immediately before running (the WI-028 mid-run-drift precedent).
- [x] Recapture: `sysml-codegen snapshot` over `exploration/stellarator_e2e/models` (absolute staged path) → `stellarator.snapshot.json`, run from the pin worktree.
- [x] Confirm the recaptured snapshot carries the new structure (grep the new names: the three defs, `cas70`, `cas90_1cfe`, `lcoe_1cfe`, `inflation_rate`, the fuel constants) and still carries `constraint_lowering_mode: applied` + the 5 WI-027 constraint facts (`beta_ok`/`net_positive`/`recirc_ok`/`tbr_ok`/`wall_load_ok`).
- [x] Delete the `AUTO_IMPLEMENTED=True` auto-impls, then `generate --from-snapshot ... --package-name stellarator_tea --pipeline-name mfe_stellarator --overwrite --preserve-handwritten` at the pin.
- [x] **Capture check A:** `'Levelized Annual Cost'` and `'DT Fuel Cost'` **lower to generated arithmetic** (no `MANUAL_REQUIRED`).
- [x] **Capture check B:** `'Levelized Replacement Cost'` routes to **`MANUAL_REQUIRED`** and emits a stub impl (expected name `levelized_replacement_cost_impl.py`, `AUTO_IMPLEMENTED=False`). Record the exact codegen message.
- [x] **Capture check C:** `cas70`, `cas90_1cfe`, `lcoe_1cfe` compile to **instance-scoped producers**, and `cas90_1cfe` reads the Item-3 `idc` cost producer.
- [x] Confirm WI-022 `dt_fusion_power_impl.py` sha256 = `8d2357…794a9f` survives regen; generated constraint modules + aggregator still present.
- [x] Record every value-preserving adaptation applied (what, why, both trees), then re-run the mirroring diff and recapture.

**Test Requirements.** Structural verification of the generated package (the checks above). No new pytest — generated modules are proven-template.

**Validation Checkpoint.**
- [x] Mirroring diff clean; snapshot recaptured from the staged tree with the new structure + 5 constraint facts.
- [x] Generate succeeds; checks A, B, C all hold.
- [x] L1 Errors 0; offender list = 6 pre-existing + WI-028 rollup-key set; WI-022 hash intact.

**Phase Completion Gate.** The staged twin carries the full WI-029 edit set; the snapshot is recaptured from it; the two flat-Real defs lower; CAS72 routes to `MANUAL_REQUIRED` with a stub; the Option-(ii) channels are instance-scoped producers; WI-022 hash + L1 offenders unchanged. **STOP-and-report** on a codegen abort, on CAS72 **not** routing to `MANUAL_REQUIRED` (that would contradict the ruled envelope analysis and is owner-visible), or on a channel that cannot become a producer without a change that alters a value. Report the exact codegen error; do not work around by editing canonical only or diverging the twin.

**Rollback.** `git checkout -- exploration/stellarator_e2e/stellarator.snapshot.json` and discard regenerated `generated/**`; recapture from the committed staged tree is deterministic.

---

## Phase 6 — CAS72 handwritten rung fill + oracle mirror + guard-live spot-check

**Overview.** Fill the `MANUAL_REQUIRED` stub with the exact 1cfe closed form, give `verify_stellaris.py` an independent mirror of the same guarded chain, and prove the guards actually bind. This is review must-fix **M1** made mechanical.

**Design Reference.** See design **CAS72 codegen-envelope ruling** (the full numeric chain and the "Guards are carried, not dropped" section), **D1**'s `'Levelized Replacement Cost'` bullet, and Validation plan step 2. Key points:
- The impl is plain Python with **no envelope constraint** — every 1cfe guard is carried **verbatim**: `clip(fluence/max(q_n, 1e-6), 0.5, n·avail)`, and `n_rep = max(0, ceil(n/t) − 1)`. Dropping any of them because it is "inert at this point" is the failure mode the design explicitly forbids.
- `n_rep` is **never** frozen as a defaulted input — it is computed live every run.
- The oracle mirror recomputes the **identical guarded chain** a second way. A mirror that drops the guards is blind to exactly the divergence it exists to catch.
- Preservation across regen is `preserve_handwritten=True` (`cli/__init__.py:91,478`).
- Reference chain at the handshake point (design, for checking): q_n 3.12851, FPY 5.75354, cal 6.39282, s 0.64887, n/t 4.69277, ceil 5, **n_rep 4**, pv 1020.396, **cas72 82.230**.

**Files to Create/Modify.**
- CREATE `exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` (fill the Phase-5 stub; `AUTO_IMPLEMENTED=False`).
- REFINE `exploration/stellarator_e2e/verify_stellaris.py` (oracle mirror of the guarded chain + the cas72 return key).
- REFINE `exploration/stellarator_e2e/run_stellaris_single.py` and/or `run_stellaris.py` (assert impl vs mirror at rel 1e-9, following the existing oracle-assert pattern).

**Checklist.**
- [x] Fill the impl with the full chain: `q_n = p_neutron / firstwall_area`; `core_lifetime_FPY = clip(fluence_limit / max(q_n, 1e-6), 0.5, operational_years * availability)`; `core_lifetime_cal = FPY / availability`; `s = (1+i)**(−cal)`; `n_rep = max(0, ceil(operational_years/cal) − 1)`; `pv = cost_per_event * s * (1 − s**n_rep) / (1 − s)`; `cost = CRF(i,n) * pv`.
- [x] Confirm each guard is present as executable code, not a comment (grep the impl for `clip`/`max`/`ceil`; three guard sites: inner `max(q_n,1e-6)`, `clip(...)`, outer `max(0, ...)`).
- [x] Confirm `n_rep` is computed, not read from a defaulted input.
- [x] Add the mirror to `verify_stellaris.py` as an **independent** re-derivation carrying the identical guarded chain (not an import of the impl — that would make the assert vacuous).
- [x] Wire the runner assertion: impl vs mirror at **rel < 1e-9**.
- [x] **Guard-live spot-check:** run the impl and the mirror on a synthetic input where a guard actually binds — at minimum one case driving FPY to the `n·avail` cap (a low wall-loading / high fluence-limit input) and one driving `ceil(n/t) − 1 ≤ 0` so the outer `max` returns 0 (a replacement interval long relative to plant life). Confirm impl and mirror still agree at rel 1e-9 in each, and record the inputs and both outputs. This proves the guards are structural, not decorative.
- [x] Confirm `preserve_handwritten` keeps the new impl across a regen: re-run `generate --from-snapshot ... --preserve-handwritten` at the pin and check the impl's sha256 is unchanged; record the sha as the new standing hash alongside WI-022's.
- [x] Add the impl + mirror to `data/traceability_matrix.csv` with their 1cfe citations (`economics.py:53-75`, `model.py:102-111`).

**Test Requirements.** The impl-vs-mirror rel-1e-9 assert and the guard-live spot-check ARE the regression tests for the handwritten rung. The end-to-end A-2 bar at Phase 7 grades the number against 1cfe.

**Validation Checkpoint.**
- [x] Impl and mirror agree at rel < 1e-9 at the handshake point; the chain reproduces the design's intermediate values (n_rep = 4, cas72 ≈ 82.230).
- [x] Guard-live spot-check passes in both synthetic cases, inputs and outputs recorded.
- [x] Impl survives regen unchanged (sha recorded); WI-022 sha256 still intact.

**Phase Completion Gate.** The handwritten rung computes the full guarded chain live, the independent mirror agrees at rel 1e-9 both at the handshake point and where guards bind, and the impl survives regen. **STOP-and-report** if impl and mirror disagree beyond rel 1e-9, if a guard turns out to be unreachable in the spot-check (it would mean the synthetic input or the guard is wrong — investigate, do not delete the guard), or if `preserve_handwritten` does not preserve the impl.

---

## Phase 7 — Harness, A-2 measurement, traps, CAS10 closure gate, A-4 verdict

**Overview.** Add the emitter refs, handshake channels, injected inputs, comparison rows, and the full trap table; run the handshake; measure every new account under A-2; fire the CAS10 closure gate; and write the criterion-3 verdict in the A-4 form with the reconciliation arithmetic shown. This is the SV-035 core and this item's finish line.

**Design Reference.** See design **D3** (harness additions), **D4** (the trap table — all five classes including **1b** and **5**), **D6** (verdict artifact contents), and the **IDC ruling — Option (ii)** section for the convention line's exact magnitude. Key points:
- `annual_om_unlevelized_musd` = 54.900 is **already emitted** at `emit_1cfe_point.py:75` — trap 1b asserts against it directly, no new ref needed.
- Comparison **logic is untouched** — `rel(a,b)` and the row-loop machinery (`:410-516`) are generic; only new rows, channels, injected inputs, and traps.
- The trap helper is `trap(name, ok, detail)` at `handshake_1costingfe.py:577`.

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/emit_1cfe_point.py` (refs).
- REFINE `exploration/stellarator_e2e/handshake_1costingfe.py` (channels, injection, rows, traps).
- CREATE/REFINE the verdict artifact — `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` (currently stale, dated Jul 18 with pre-WI-028 numbers; rewrite it wholesale) or a named successor.

**Checklist — emitter refs (D3).**
- [x] Add `inflation_rate` (0.02, currently only in `target`) to `refs`.
- [x] Add the DT fuel constants to `refs`, each as `float(cc.<attr>)`: `cost_per_rxn` or its components (`M_D_KG`, `u_deuterium`, `M_Li6_KG`, `u_li6`), `q_eff`/`Q_DT`, `MEV_TO_JOULES`, `burn_fraction`, `fuel_recovery`.
- [x] Add the CAS72 replacement params to `refs`: `fluence_limit_dt` (18.0), the replaceable-account ids (`C220101`, `C220108`).
- [x] Confirm `annual_om_unlevelized_musd` (54.900) is present at `:75` and used by trap 1b (no duplicate ref added).

**Checklist — handshake channels, injection, rows (D3).**
- [x] Add `CH` channels: `cas71`, `cas72`, `cas70`, `cas80`, `cas90_1cfe`, `lcoe_1cfe`. The existing headline `lcoe` channel stays pointed at the DCF headline.
- [x] Add the new injected inputs (`inflation_rate`, fuel constants, `fluence_limit`) to the `set_1cfe_inputs` update blocks, same `f"{P}<module>__<input>"` pattern as availability at `:296`.
- [x] Add explicit A-2 comparison rows for `cas71`, `cas72`, `cas70`, `cas80`, `cas90_1cfe`, `lcoe_1cfe`.
- [x] Confirm the comparison logic (`rel`, the row loop) is **byte-unchanged**.

**Checklist — traps (D4, A-5, MR-WI029-8). Every new mapping asserted:**
- [x] **Trap 1 — levelization params:** g = inflation_rate = 0.02; Tc = construction_years = **8** (NOAK, not 10); i = 0.07; n = 30; and the **1.439** factor materializes (cas71 / annual_om at the handshake point).
- [x] **Trap 1b — handshake-point O&M base [HARD, M2]:** assert `annual_om = 54.900` at the handshake point (p_net = 1000 injected), **not** the design-point 52.517. This is separate from trap 1: the factor is mathematically constant in the base, so the factor trap alone is blind to a wrong base.
- [x] **Trap 2 — CAS72 replacement chain:** replaceable set = {C220101, C220108}; `fluence_limit_dt` = 18.0; q_n from the modeled p_neutron / firstwall_area; **n_rep = 4** (the handwritten rung's computed integer); clip inert here (assert FPY ∈ [0.5, n·avail]).
- [x] **Trap 3 — fuel constants:** `cost_per_rxn = M_D·u_D + M_Li6·u_Li6`; `q_eff = Q_DT = 17.58`; burn correction = ×1.19; each asserted against `cc`.
- [x] **Trap 4 — availability injection:** 0.9 (handshake) injected over the model's 0.85, into **both** CAS72's `core_lifetime_cal` and the LCOE denominator — the duty-7 trap made explicit.
- [x] **Trap 5 — IDC Option (ii):** assert `cas90_1cfe = CRF·(overnight_capital + CAS60)` and that it reads the **Item-3 CAS60 reported line**; assert the headline `idc_factor` is **unchanged** at `(1+d)^(Yc/2)`; assert `total_capital == overnight_capital` (CAS60 still excluded). Together these guard the double-count hazard across the two coexisting LCOE channels.
- [x] Every trap appears in the printed trap table with its detail line.

**Checklist — execute and measure.**
- [x] Re-verify the sysml-codegen pin worktree before running (A-6).
- [x] Execute: `exploration/pipeline_spike/.venv-exec/bin/python handshake_1costingfe.py` against the Phase-5 snapshot / generated package.
- [x] **A-2 measurement for every new channel (SV-035):** record `rel_dev` for `cas71` (target 79.00362), `cas72` (82.22999), `cas70` (161.23361), `cas80` (0.76907), `cas90_1cfe` (813.58728), `lcoe_1cfe` (123.74301) — each under |rel dev| ≤ 1e-6 vs 1cfe float32.
- [x] **CAS10 closure gate (Phase-4 carry-forward):** model CAS10 = **18.5** at the handshake point, residual **0.0**. If it does not, fire the owner stop condition (see Rollback / Surface Posture).
- [x] Confirm all traps assert-pass (no silent default).

**Checklist — the criterion-3 verdict artifact (D6, MR-WI029-5).** This item writes it. In the A-4 form:
- [x] **(1) Per-account A-2 pass table:** every modeled account — the WI-025 set, the WI-028 set, plus CAS71, CAS72 (forward-computed), CAS80, and the `cas90_1cfe` comparison channel — with |rel dev| vs 1cfe float32 and pass/fail at 1e-6.
- [x] **(2) FULL signed-magnitude remainder itemization:** every non-bar account with its 1cfe value, the model value (or "structurally absent"), the signed dollar gap, and a one-line reason. Expected standing set after this item: **C220106_pump $0.721M** (explained, shell-only vessel calc) and the **headline IDC convention line** — DCF multiplier 1.310796 vs 1cfe 1.282476, DCF-equivalent CAS90 831.553 vs 1cfe 813.587 = **+$17.966M (+2.208%)** on the annual capital charge, ≈+1.8% on LCOE, explained-and-kept under Option (ii). **CAS10 closes as error** (residual 0.0); **CAS72 leaves the remainder** (now forward-computed). Note that the 1cfe-form comparison channel itself comes under A-2, so the convention line is a headline-vs-comparison difference, not a handshake gap.
- [x] **(3) Reconciliation arithmetic, shown not asserted:** the residual end-to-end LCOE gap **equals** the itemized-remainder sum within ≤1e-6 relative to LCOE. Print the arithmetic term by term.
- [x] **(4) The criterion-3 verdict statement:** met, or honestly failed. No third state.
- [x] Note in the artifact that both LCOE channels coexist by design (headline DCF + 1cfe-form comparison) and which one is the design-point headline.

**Test Requirements.** The A-2 per-account bar, the six trap classes, and the A-4 reconciliation ARE the regression tests for this item.

**Validation Checkpoint.**
- [x] All six new channels under |rel dev| ≤ 1e-6, recorded per account (SV-035).
- [x] CAS10 = 18.5, residual 0.0.
- [x] All traps (1, 1b, 2, 3, 4, 5) assert-pass; trap table printed.
- [x] Verdict artifact carries all four A-4 parts with the reconciliation arithmetic shown.

**Phase Completion Gate.** Every newly-brought account is under A-2 (or a legitimate float32-ceiling account is itemized under A-4 with a signed magnitude); CAS10 reconstructs with residual 0.0; all traps pass; the A-4 table reconciles within tolerance; the criterion-3 verdict is written. **STOP-and-report** if an account misses A-2 for a real (non-float32) reason, if the reconciliation does not close, or if the CAS10 gate fails (owner stop condition).

**Rollback.** `git checkout -- exploration/stellarator_e2e/emit_1cfe_point.py handshake_1costingfe.py HANDSHAKE_REPORT.md`.

---

## Phase 8 — Re-baseline, standing-bars sweep, records (G-8, SV-035, MR-WI029-9/10/11)

**Overview.** Re-baseline `handshake_comparison.json` as its own commit, record the moved design-point headline, run the full standing-bars sweep on one executed run, fill SV-035, and reference the verdict artifact from the epic. No source mutation in this phase — it re-baselines, grades, and records.

**Design Reference.** See design **Validation plan** steps 5–7 and **D6**; spec MR-WI029-9/10/11 + Success Criteria; brief "Standing bars".

**Files to Create/Modify.**
- REFINE `exploration/stellarator_e2e/handshake_comparison.json` (re-baselined; **its own commit**).
- REFINE `modeling_project/VALIDATION_MATRIX.md` (SV-035 `pending` → executed record).
- REFINE `.project/backlog/epic_stellarator_mbse_demo.md` (Item 4 / criterion 3 references the verdict artifact).
- This plan's Implementation Record.

**Checklist — run once, grade all.**
- [x] **Execute the design point:** `exploration/pipeline_spike/.venv-exec/bin/python run_stellaris_single.py`; record the new headline (total_capital, LCOE, p_net, q_eng, magnet share, constraint verdicts).
- [x] **Design-point headline re-baseline recorded (MR-WI029-9)** with the movement attributed to exactly two causes and no third: **up** from CAS71 + CAS72 + CAS80 entering the LCOE numerator; **down $16M** on total_capital from the CAS10 fix (≈$16,129.7M, was $16,145,706,216.04). **No multiplier-swap component** — under Option (ii) the headline convention is unchanged (`idc_factor` untouched, `total_capital = overnight_capital`). Report the 1cfe-form comparison channel alongside, explicitly **not** as the headline. State plainly that this is a re-baseline, not a regression, and note the spec's MR-WI029-9 "total_capital unchanged" is corrected by the design's CAS10 finding.
- [x] **Oracle bit-exact (rel 1e-9):** every executed channel matches the pure-Python oracle at the new headline, including cas71 / cas72 / cas70 / cas80 / the comparison channels.
- [x] **G-8 re-baseline (MR-WI029-10):** re-run the handshake; `handshake_comparison.json` gains the new rows; commit it **alone**, as a standalone explicit commit, message listing each new row with its signed magnitude and noting the comparison logic is byte-unchanged (only rows + inputs).
- [x] **L1:** Errors 0; offender list = the 6 pre-existing + WI-028's design-accepted rollup-key L6 set. Compare the list, not the flags.
- [x] **WI-022 sha256** `8d2357…794a9f` intact; the new CAS72 impl sha recorded as a standing hash.
- [x] **IFE anchors:** Runs A/B byte-exact (252.29996307 / 68.69020165); **Run C out-of-scope** by [OWNER] ruling 2026-07-20 — record the supersession, do not count it as a failure.
- [x] **pytest:** `uv run pytest tests/models/ -q` → **11 failed / 18 passed / 14 skipped / 0 errors**.
- [x] **Regen stability:** recapture to `/tmp` and diff vs the committed snapshot — structure + the 5 constraint facts byte-identical (only `captured_at` / `document_path` differ).
- [x] **MR-3/MR-4** spot-check: no concept literal in any new library def; every new base carries a citation.
- [x] **PROTOCOL sealed** — record that no barred path was read at any stage of this item.
- [x] **Fill SV-035 by editing the matrix row directly** — the per-account A-2 table, the CAS10 closure, the verdict, the new headline, and each standing-bar result; set status `passing` only if all in-scope bars held. **Do NOT use `agentic-mbse pm update-validation`** — it corrupts rows containing `|` (the `|rel dev|` notation), a WI-028 finding.
- [x] Reference the verdict artifact from `.project/backlog/epic_stellarator_mbse_demo.md` Item 4 / criterion 3.
- [x] Record the pins + pin worktree paths (Phase 0) in the Implementation Record.

**Test Requirements.** This phase *is* the regression suite: oracle bit-exactness, L1 offender list, IFE anchors, pytest tally, regen stability, hash preservation.

**Validation Checkpoint (spec Success Criteria).**
- [x] `handshake_comparison.json` re-baselined as a standalone commit; move list documented; logic untouched.
- [x] New design-point headline recorded with the two-cause attribution; oracle rel 1e-9 holds at the new point.
- [x] All standing bars hold (Run C supersession recorded); SV-035 filled as an executed record.
- [x] The criterion-3 verdict artifact exists, is in the A-4 form, and is referenced from the epic.

**Phase Completion Gate.** The comparison JSON is re-baselined as its own commit; the new headline is recorded as a re-baseline with the oracle bar holding; every standing bar passes; SV-035 is an executed record; the criterion-3 verdict is written and referenced. This gate = the spec's Success Criteria for MR-WI029-1…11. Ready for `/audit-models` → owner close (Align ruling 2: owner holds close; orchestrator commits after close). **STOP-and-report** on any standing-bar break this item did not intend to move.

---

## Success Criteria Coverage (from spec)

| Spec Success Criterion | Covered by |
|---|---|
| CAS71 + CAS80 forward-computed, MR-4-sourced, each under A-2 (MR-WI029-1/3) | Phase 1 (defs) + Phase 2 (wiring) + Phase 3 (bindings) → Phase 7 (A-2) |
| CAS72 disposed explicitly — forward-computed under A-2 (MR-WI029-2) | Phase 1 (def) + Phase 5 (MANUAL_REQUIRED routing) + Phase 6 (impl + mirror) → Phase 7 (A-2) |
| IDC/LCOE reconciliation ruled; end-to-end LCOE compared in 1cfe-comparable form (MR-WI029-4) | Ruled Option (ii) in design; implemented Phase 2 (channels) + Phase 7 (rows, trap 5, A-4 convention line) |
| CAS10 error-to-close under the verbatim owner stop condition (MR-WI029-6) | Phase 4 (bounded fix + stop condition) → Phase 7 (executed reconstruction gate) |
| Criterion-3 verdict in the A-4 form with reconciliation arithmetic shown (MR-WI029-5) | Phase 7 (verdict artifact) + Phase 8 (epic reference) |
| Trap assertions for every new mapping (MR-WI029-8) | Phase 7 (traps 1, 1b, 2, 3, 4, 5) |
| Design-point headline re-baselined; oracle bit-exact at the new point (MR-WI029-9) | Phase 8 |
| `handshake_comparison.json` re-baselined as an explicit commit; logic untouched (MR-WI029-10) | Phase 8 |
| Every `.sysml` edit region-identical in both trees; mirroring diff clean; snapshot from the staged tree (MR-WI029-7) | Phases 1–4 (per-phase mirroring diff) + Phase 5 (gate + recapture) |
| Standing bars hold; SV-035 registered and passing (MR-WI029-11) | Phase 8 |

## Feasibility Concerns

Risks carried from the design (§Risks), restated as phase-located gates:

1. **CAS72 handwritten rung fill + oracle mirror (medium).** Gate: Phase 6 — impl vs independent mirror at rel 1e-9, plus the guard-live spot-check proving the guards bind. The full numeric chain is re-derived in the design to check against; WI-022 is the exact precedent.
2. **Double-count hazard from two coexisting LCOE channels (low, residual after the Option-(ii) ruling).** Gate: Phase 7 trap 5 — `idc_factor` unchanged and `total_capital == overnight_capital`, so CAS60 cannot enter the headline capital base.
3. **Staged-twin skip (high, inherited).** Gate: per-phase mirroring diff in Phases 1–4, then the Phase-5 gate + recapture from the staged tree. A canonical-only edit computes against a stale snapshot — silently wrong.
4. **Pin drift (medium, live).** Three pins are off-pin with no worktree at the pin, and sysml-codegen moved again since design. Gate: Phase 0 worktree checkouts, re-verified immediately before every codegen/exec step (Phases 5, 7).
5. **Codegen-mechanics adaptations on the new aggregates (medium, precedented).** WI-028 needed four at the same checkpoint. Gate: Phase 5 — adaptations must be value-preserving, both trees, and recorded as surfaced findings; a change that alters a value is a STOP.
6. **CAS10 fix moves total_capital by $16M** (a finding against MR-WI029-9's "unchanged"). Gate: Phase 8 records it with the two-cause attribution; the oracle bit-exact bar catches any arithmetic error at the new point.
7. **`n_rep` step-function (low).** Computed live in the handwritten rung, never frozen. Gate: Phase 6 (computed, not an input) + Phase 7 trap 2 (n_rep = 4 asserted).

**Assumptions about baseline state:** the two flat-Real prototype defs parse clean (verified at design); the staged twin is at its WI-028 close state; the four toolchain deps are reachable at their pins (re-verified at plan time — all four objects present, three HEADs drifted). If a pin is unreachable at Phase 0, that is a mismatch to surface (A-6), not silently accept.

---

## Implementation Record

*Filled by `/implement-model`, 2026-07-25. All nine phase gates PASS. No STOP condition fired.*

**Restore point.** fusion-tea `0ddf15b9f9638d2b3468e5385689b1952ceec266`, branch `feat/stellarator-mbse-demo`, tracked tree clean (untracked: `.orchestrate-logs/`, `.project/reports/2026-07-25-0835-status-report.md`). *(The plan expected `c2aad0b6`; `0ddf15b9` is the plan commit itself, one ahead — same tree plus the plan.)*

Pin worktrees created at Phase 0 and used for every codegen step:

| Tool | Pin | Worktree | HEAD at run |
|---|---|---|---|
| sysml-codegen | `06d95f8` | `~/1cfe/sysml-codegen-wi029-pin` | `06d95f854f30f77f1a7c93f9c0f13be878765165` |
| teax | `07eb0ac` | `~/1cfe/teax-wi029-pin` | `07eb0accd4852742a6da1820a05a4cae4fe707df` |
| agentic-mbse | `4c18d61` | `~/1cfe/agentic-mbse-wi029-pin` | `4c18d616f77e26932a8e158cefc2637db47f9b07` |
| 1costingFE | `0254385` | main checkout (already on pin, clean) | `02543850089be175ea7c28b92a8b2a4184e1637e` |

Pre-existing dirty files in the upstream repos, recorded so nothing here is confused with them: sysml-codegen `?? .project/diagrams/pipeline_explainer_v2.html`; agentic-mbse `?? .orchestrate-logs/`; teax and 1costingFE clean.

### Phase 0 — Pin verification, worktree checkouts, restore point — _(GATE: PASS)_
- **What ran.** `git cat-file -t` on all four pins; `git worktree add --detach` for the three drifted repos; license sourced; exec venv located; baseline parse smoke over `models/`.
- **Gate evidence.** All four pins reachable as commit objects. HEAD drift confirmed and unchanged from the plan's record: sysml-codegen `fa9e0d0` (branch `nested-override-tripwire`), teax `fa0e06a`, agentic-mbse `f4ebdce`, 1costingFE `0254385` (== pin). Three pin worktrees created and verified at their pin SHAs (table above). `SYSIDE_LICENSE_KEY` resolves (37 chars). Baseline parse: `uv run python -m syside check models/` → **Checks passed!**, 0 errors, 7 namespace-distinguishability warnings (`wall_area`, `f_shape`, `lt_shield_t`, `cas23_to_28`, `cas30`, `p_net`, `n_mod`) — the 6 pre-existing plus WI-028's design-accepted rollup-key set, unchanged.
- **Deviations.** The exec venv is **not** at `exploration/pipeline_spike/.venv-exec` inside this worktree — this repo is a git worktree of `~/1cfe/fusion-tea` and the venv is gitignored, so it exists only in the main checkout. Every exec step ran `~/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`, the same interpreter WI-028 used. No behavioural difference.

### Phase 1 — Library calc defs (both trees) — _(GATE: PASS)_
- **What ran.** Appended `'Levelized Annual Cost'`, `'DT Fuel Cost'`, `'Levelized Replacement Cost'` to `models/library/analyses/mfe_account_costs.sysml` and the staged twin `exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml`. Three rows added to `data/traceability_matrix.csv`.
- **Gate evidence.** Both files parse **Checks passed!**; `diff` between the two files is **empty** (region-identical, whole-file). Every def and defaulted input carries an MR-4 `**Source**`/`**Ref**`/`**Basis**` block citing 1cfe at pin `0254385` (`economics.py:13-50`, `economics.py:53-75`, `economics.py:6-10`, `costs.py:41-44`, `costs.py:476-544`, `model.py:102-111`, `physics.py:13-33`, `costing_constants.yaml:153,160,282-283`). MR-3 clean: no Stellaris literal in any def — the fuel chemistry, the fluence limit, the replaceable-account cost, and the escalation rate are all inputs.
- **Deviations (two, both recorded and value-preserving).**
  1. **`ceil` and `clip` are not in the KerML Real function library.** Verified by parse test: `RealFunctions::` has `max`, `min`, `floor`, `abs`, `sqrt`, `round` — no `ceiling`, no `clip`. Written as the exact identities `ceil(z) = -floor(-z)` and `clip(z, lo, hi) = min(max(z, lo), hi)` (jnp.clip's own order — floor first, then cap; it matters only when lo > hi, and matching it keeps the statement verbatim). Both are `InvocationNode`s, so the routing to `MANUAL_REQUIRED` is unaffected — which is the point of the rung assignment. The handwritten impl uses Python's `math.ceil` and the same guards directly.
  2. **`'DT Fuel Cost'` carries an explicit `1e6` the prototype did not.** 1cfe's `cas80_fuel` leaves the MW·s→J conversion implicit and therefore returns **M$**/yr; the plant rolls up in **$**. Transcribed byte-for-byte the def would have been off by 1e6 against every other account. The `* 1.0e6` makes the def unit-correct ($/rxn in → $/yr out) per the library's own unit-transparency rule, and is documented at the line. This is a unit correction inside the model, not a change to the 1cfe formula.

### Phase 2 — Generic-plant LCOE-side wiring + Option-(ii) channels — _(GATE: PASS)_
- **What ran.** Added `cas71_calc`, `fuel_calc`, `cas80_calc`, `cas72_calc`, the `cas70_calc` rollup, and the two Option-(ii) comparison-channel calcs to `models/designs/generic_mfe/mfe_plant.sysml` and its staged twin, with the new plant-level inputs (`inflation_rate`, the five fuel constants, `fluence_limit`, `ash_frac`).
- **Gate evidence.** Both trees parse **Checks passed!**. `uv run agentic-mbse validate --level 1 models` → **Errors 0, Warnings 0**; syside offender list unchanged at 7 — zero new offender kinds. `git status` confirms **`mfe_lcoe_dcf.sysml` is untouched in both trees**, and `total_capital == overnight_capital` still holds by construction (trap 5 asserts it at run: rel 0.00e+00). Mirroring diff between the two `mfe_plant.sysml` copies shows **only** the two known Item-10 comment blocks (lines 402-406, 564). Dataflow is unidirectional — physics/powers → fuel/replacement/O&M → levelization → cas70/80 → LCOE; the CAS72 rung is a leaf producer; no cycles.
- **The exact headline binding landed (the one place the headline legitimately moves).** `mfe_plant.sysml:571` was `attribute annual_om : Real = om_cost.annual_om;` (unlevelized). It is now `attribute annual_om : Real = cas70_calc.annual_total;` — the levelized CAS70 (= CAS71 + CAS72) plus CAS80. The DCF **convention** is untouched: `idc_factor` and `total_capital` are as they were; only the annual-cost numerator becomes complete.
- **Deviations.** See the Phase-5 surfaced findings — the wiring as first written did not survive the codegen checkpoint and was reshaped there (value-preserving), so the final shape in this file is the post-adaptation one.

### Phase 3 — Stellaris instance bindings — _(GATE: PASS)_
- **What ran.** Bound `inflation_rate` 0.02, `fuel_cost_per_rxn` 1.7260641119988767e-23 $/rxn, `fuel_q_eff` 17.58, `mev_to_joules` 1.6021766339999998e-13, `burn_fraction` 0.05, `fuel_recovery` 0.99, `fluence_limit` 18.0, `ash_frac` 0.2002275312855518 in `models/designs/stellarator_09/stellarator_plant.sysml` and the staged twin. Eight rows added to `data/traceability_matrix.csv`.
- **Gate evidence.** Both copies parse **Checks passed!**; the instance mirroring diff is **empty**. Every binding carries an inline `**Source**`/`**Ref**`/`**Basis**` doc comment in the WI-028 house style. `p_neutron` and `firstwall_area` reach `cas72_calc` from the modeled physics chain — `fusion.p_fus` and `rb.wall_area`, no new instance literal (the pipeline wiring confirms it: `p_fus: float ...fusion__p_fus.root`, `firstwall_area: float ...rb__wall_area`). The replaceable set is the modeled `blanket.capital_cost + divertor.capital_cost` accounts × `n_mod`, not a frozen dollar literal. No new library default introduced.
- **Deviations.** `ash_frac` is bound at the instance to the **exact** 1cfe constant `E_ALPHA_DT / Q_DT = 3.52 / 17.58 = 0.2002275312855518`, not the calc-def's rounded 0.2002 default. Checked and necessary: the rounded value shifts `q_n` by 3.4e-5 relative, which propagates through `core_lifetime_cal` into `s` and would have missed the A-2 1e-6 bar on CAS72. Cited to `physics.py:31-33`.

### Phase 4 — CAS10 bounded fix — _(GATE: PASS)_
- **What ran.** `precon_fixed_base` 32000000.0 → 16000000.0 in both instance copies, with the doc comment rewritten to itemize the NOAK adders (site_permits 3 + licensing_dt 5 + plant_permits 2 + **studies_noak 4** + plant_reports 1 + other_precon 1 = 16.0). The stale FOAK note in `'Preconstruction Cost'` (`mfe_account_costs.sysml`) amended to the NOAK basis in both library copies.
- **Gate evidence.** *Arithmetic pre-check (paper, before any run):* `0.25 · √(1000·1·1000) · 10000 / 1e6 = 2.5`, `+ fixed 16.0` = **18.5**, residual **0.0** — computed and confirmed exactly. All four edited files parse **Checks passed!**; all four mirroring diffs clean. `git diff` scoped to the two edited regions confirms nothing else in the CAS10 chain moved — one value changed, the rest is doc text. **The owner stop condition did NOT fire**: the divergence resolved to one clearly identified error under an unambiguous basis, and the fix reconstructs 1cfe cleanly. The doc amendment changes no number (contingency_rate_noak = 0.0 on both sides, so 1cfe's full CAS10 equals the subtotal exactly — the old "× 1.10" note was a stale FOAK reading contributing zero residual).
- **Deviations.** None. The executed reconstruction gate is carried to Phase 7 and passed there.

### Phase 5 — Mirroring diff gate + recapture + codegen-capture checkpoint — _(GATE: PASS)_
- **What ran.** Full mirroring diff over every edited region set; `sysml-codegen snapshot` over the absolute **staged** models path, run from the pin worktree at `06d95f8`; deleted the 36 `AUTO_IMPLEMENTED = True` auto-impls; `generate --from-snapshot ... --package-name stellarator_tea --pipeline-name mfe_stellarator --overwrite --preserve-handwritten` at the pin. Three snapshot/generate cycles were needed as the adaptations below landed.
- **Gate evidence.**
  - **Mirroring diff gate:** library and instance files byte-identical between trees; `mfe_plant.sysml` differs only by the two known Item-10 comment blocks. No other delta. (The staged tree also does not carry the IFE/HIF library files — pre-existing and by design.)
  - **Pin re-verified immediately before each run:** `git -C ~/1cfe/sysml-codegen-wi029-pin rev-parse HEAD` = `06d95f854f30f77f1a7c93f9c0f13be878765165`.
  - **Snapshot carries the new structure:** the three defs, `cas70_annual`, `cas90_1cfe`, `lcoe_1cfe`, `inflation_rate`, `fuel_cost_per_rxn`, `fluence_limit`, `ash_frac`, `p_neutron` all present; `constraint_lowering_mode: applied`; the 5 WI-027 constraint facts (`beta_ok`, `net_positive`, `recirc_ok`, `tbr_ok`, `wall_load_ok`) intact. `Step 6.5 complete: 34 compiled (32 fully_compilable, 2 manual_required)`.
  - **Capture check A — PASS.** `Levelized_Annual_Cost` → `fully_compilable`; `DT_Fuel_Cost` → `fully_compilable`. Both lower to generated arithmetic, no `MANUAL_REQUIRED`.
  - **Capture check B — PASS.** `Levelized_Replacement_Cost` → `manual_required`, with a stub emitted at `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py`. **Exact codegen message:** `unsupported node: invocation (['RealFunctions', 'max'])` on outputs `fpy_raw`, `core_lifetime_fpy`, `n_rep` — i.e. the guards and `ceil` are what push it off the rung, exactly as the design ruled.
  - **Capture check C — PASS.** `cas70_calc`, `cas90_1cfe_calc`, `lcoe_1cfe_calc` all compile to instance-scoped producers under `stellarator_09__stellaris__`, and `cas90_1cfe_calc` reads the Item-3 CAS60 producer directly: `idc_cost: float stellarator_09__stellaris__idc__cost.root`.
  - **WI-022 `dt_fusion_power_impl.py` sha256 `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` survives regen** (preserved by signature match). Generated constraint modules + aggregator present; 58 modules built. L1 Errors 0, offender list unchanged.
- **Deviations — SIX codegen-mechanics adaptations, all value-preserving, all applied region-identically to both trees.** Each is the WI-028 Phase-4 class: codegen wires a calc input only from a **producer** channel, and a plant attribute that merely restates or sums calc outputs does not mint one. See "Surfaced findings" below for the individual records. No adaptation altered a value, an operand, or an operand order; every one is graded by the Phase-6 oracle bar (rel 1e-9, achieved 0.0 on the affected channels) and the Phase-7 A-2 bar.

### Phase 6 — CAS72 handwritten rung + oracle mirror + guard-live spot-check — _(GATE: PASS)_
- **What ran.** Filled the stub with the full guarded closed form; added an independent mirror of the identical chain to `verify_stellaris.py` (written out, **not** imported from the impl, so the assert is not vacuous); wired the impl-vs-mirror assertion and the guard-live spot-check into `run_stellaris_single.py`; re-ran `generate --preserve-handwritten` to confirm preservation.
- **Gate evidence.**
  - **Impl vs mirror at the handshake and design points: rel `0.00e+00`** (bar 1e-9). The `cas72_annual` row of the bit-exact block reads `exec=95399746.500496805 oracle=95399746.500496805 reldev=0.00e+00`.
  - **Reference chain reproduced at the handshake point** (trap 2, executed): `q_n = 3.12851` MW/m², `FPY = 5.75353` ∈ [0.5, 27.0] (clip inert here), `cal = 6.39282`, **`n_rep = 4`**, `cost_per_event = 671.160` M$, **cas72 = 82.230031 M$/yr**.
  - **All three guards present as executable code, not comments.** Inner `max(q_n, 1e-6)`, `_clip(·, 0.5, operational_years * availability)` implemented as `min(max(value, lo), hi)` (jnp.clip's order), and outer `max(0.0, ceil(n/t) − 1.0)`. `n_rep` is **computed live** every call — it is not an input, defaulted or otherwise.
  - **Guard-live spot-check — PASS, 3 synthetic cases, each proving a different guard binds:**

    | case | inputs (the ones that matter) | guard proven live | impl | mirror | rel |
    |---|---|---|---:|---:|---:|
    | clip **cap** binds | p_fus 100 MW, fluence_limit 500 | raw FPY 4126.668 > cap 27.000 | 0.000000 | 0.000000 | 0.00e+00 |
    | clip **floor** binds | p_fus 200,000 MW, fluence_limit 18.0 | raw FPY 0.07428 < floor 0.500 → n_rep 53, cost nonzero | 1,219,445,700.972802 | 1,219,445,700.972802 | 0.00e+00 |
    | outer **max** binds | p_fus 50 MW, operational_years 5 | `ceil(n/t) − 1 ≤ 0` → n_rep floored to 0 → cost exactly 0.0 | 0.000000 | 0.000000 | 0.00e+00 |

    The floor case is the load-bearing one: it is the case where a guard binds **and** the result is non-zero, so the rel-1e-9 agreement is a real comparison rather than 0-vs-0. The cap and outer-max cases both return exactly 0 — which is itself the correct structural fact (when the core outlives the plant, nothing is replaced), and each is separately asserted to actually saturate rather than merely to agree.
  - **Preservation across regen:** re-ran `generate --from-snapshot ... --preserve-handwritten`; the impl's sha256 is unchanged. **New standing hash: `06fb1a6e37e46312ecab813241b810feea9cc56429a2cfeca6f16997d3af704c`** (`levelized_replacement_cost_impl.py`), alongside WI-022's `8d2357…794a9f`, which is also intact.
  - Impl + mirror added to `data/traceability_matrix.csv` via the `'Levelized Replacement Cost'` row (`economics.py:53-75`, `model.py:102-111`).
- **Deviations.** None.

### Phase 7 — Harness, A-2 measurement, traps, CAS10 closure, A-4 verdict — _(GATE: PASS)_
- **What ran.** Added the WI-029 refs to `emit_1cfe_point.py`; added six `CH` channels, the injected inputs, six A-2 comparison rows, the CAS10 closure gate, and the six D4 traps to `handshake_1costingfe.py`; executed the handshake at the pin; wrote the verdict artifact.
- **A-2 result (SV-035 core).** Bar |rel dev| ≤ 1e-6 vs 1cfe float32 at the handshake point:

  | channel | 1cfe | model | rel dev | A-2 |
  |---|---:|---:|---:|---|
  | `cas71` levelized O&M | 79,003,623.9624 | 79,003,632.4967 | **+1.08e-07** | PASS |
  | `cas72` levelized replacement | 82,229,988.0981 | 82,230,031.0496 | **+5.22e-07** | PASS |
  | `cas70` = 71 + 72 | 161,233,612.0605 | 161,233,663.5464 | **+3.19e-07** | PASS |
  | `cas80` levelized fuel | 769,069.7312 | 769,069.8108 | **+1.03e-07** | PASS |
  | `cas90_1cfe` (Option ii) | 813,587,280.2734 | 813,475,930.4152 | −1.37e-04 | MISS (inherited) |
  | `lcoe_1cfe` (Option ii) | 123.743011 | 123.728889 | −1.14e-04 | MISS (inherited) |

  All four forward-computed accounts pass. The two comparison channels miss **only** by the propagation of the single pre-existing itemized capital remainder `C220106_pump` ($0.7206M) — not a formula or mapping error, and therefore not a surfaced STOP: trap 5 shows `cas90_1cfe` reconstructs from the model's own overnight capital and CAS60 reported line at **rel 0.00e+00**, so the channel's own arithmetic is exact. Both are itemized under A-4 with signed magnitudes and reconcile.
- **CAS10 closure.** Model CAS10 at the handshake point = **18.500000 M$**, 1cfe = **18.500000 M$**, **residual 0.000000 M$** (rel +7.25e-09 — 1cfe's float32 emission plus the injected `p_net = 1000.0001`'s own residue through the sqrt land term; an order of magnitude inside the A-2 bar). **Gate PASS; the owner stop condition did not fire.**
- **Traps.** All twelve pass (six pre-existing WI-028 + six new WI-029), each printed with its detail line:
  - **WI-029/1 levelization params — PASS.** g = 0.02, Tc = **8.0** (NOAK, not 10), i = 0.07, n = 30; and the factor materializes: `cas71 / annual_om = 1.43905`.
  - **WI-029/1b handshake-point O&M base [HARD, review must-fix M2] — PASS.** 1cfe `annual_om = 54.900002` M$/yr at p_net = 1000 (**not** the design-point 52.517); model 54.900002 M$/yr, rel +0.00e+00. Asserted separately from trap 1 exactly because the factor is constant in the base and so blind to a wrong one.
  - **WI-029/2 CAS72 replacement chain — PASS.** Replaceable set == `['C220101', 'C220108']`; `fluence_limit_dt` = 18.0; q_n = 3.12851 from the modeled `p_neutron / firstwall_area`; FPY 5.75353 ∈ [0.5, 27.0] (clip inert asserted); **n_rep = 4**, the handwritten rung's computed integer.
  - **WI-029/3 fuel constants — PASS.** `cost_per_rxn = M_D·u_D + M_Li6·u_Li6 = 1.726064e-23` $/rxn (rel to 1cfe ≤ 1e-12); `q_eff = Q_DT = 17.58`; burn correction ×1.1900.
  - **WI-029/4 availability injection — PASS.** 0.9 injected over the model's 0.85 into **all three** consumers: `cas72_calc.availability` (→ `core_lifetime_cal`), `lcoe_calc.availability`, and `lcoe_1cfe_calc.availability`. The duty-7 trap made explicit.
  - **WI-029/5 IDC Option (ii) — PASS.** `cas90_1cfe = CRF·(overnight + CAS60)` reconstructs at rel +0.00e+00 reading the Item-3 CAS60 reported line; headline `idc_factor = 1.310796 = (1+d)^(Yc/2)` **unchanged** (1cfe's f_idc form is 1.282475); `total_capital == overnight_capital` at rel 0.00e+00, so CAS60 cannot enter the headline capital base. The double-count hazard is closed.
- **A-4 verdict.** Written to **`exploration/stellarator_e2e/HANDSHAKE_REPORT.md`**, generated from the executed run by `exploration/stellarator_e2e/build_verdict_report.py` (every number read from `handshake_comparison.json` / `onecfe_point.json`; none hand-transcribed). It carries all four A-4 parts:
  1. **Per-account A-2 pass table** — the WI-025 set, the WI-028 set, CAS71/CAS72/CAS80, and the `cas90_1cfe` comparison channel, each with |rel dev| and pass/fail at 1e-6.
  2. **Full signed-magnitude remainder itemization** — exactly two standing lines: **R1 `C220106_pump` −$0.7206M** (vessel shell-only, explained-and-kept) and **R2 the headline IDC convention +$17.9639M/yr (+2.208%)** on the annual capital charge (DCF multiplier 1.310796 vs 1cfe 1.282475), explained-and-kept under Option (ii). **CAS10 closes as error** (residual 0.0); **CAS72 leaves the remainder** (now forward-computed). R1's propagation factor through the WI-028 assembly is stated and checked: 1.14 × [1 + 0.20·(8/6) + 0.015 + 0.01 + 0.015·(1 + 0.20·(8/6))] = 1.494160, predicting an overnight gap of −1.0767 M$ against the executed −1.0770 M$.
  3. **Reconciliation arithmetic, shown term by term, for BOTH channels:**
     - *1cfe-form comparison channel:* gap −0.014122691 $/MWh; itemized sum (CAS90_1cfe −0.111349858 + CAS70 +0.000051486 + CAS80 +0.000000080) M$/yr × 1e6 / 7,884,000.481 MWh = −0.014116982 $/MWh; **residual −5.709e-06 $/MWh = 4.61e-08 relative to LCOE ≤ 1e-6 — CLOSES.**
     - *DCF headline:* gap +2.264397289 $/MWh (+1.830%); itemized sum (IDC convention +17.963853456 + the same three) M$/yr × 1e6 / 7,884,000.481 MWh = +2.264403104 $/MWh; **residual −5.815e-06 $/MWh = 4.70e-08 relative to LCOE ≤ 1e-6 — CLOSES.**
     - The leftover in each is the float32 A-2 residue of the accounts themselves, more than an order of magnitude inside the tolerance.
  4. **Verdict: MET.** Not partially met; there is no third state. Every modeled account is under A-2 or itemized with a signed magnitude; the remainder is two lines and reconciles in both channels; the one error found (CAS10) was closed. The artifact states plainly that both LCOE channels coexist by design and that the **DCF headline** is the design-point headline, the 1cfe-form channel a comparison.
- **Deviations.** The CAS10 closure gate was first coded with a **dollars-absolute** 1e-6 bar, which no spec requires and which is far stricter than A-2; it read FAIL on a 0.13-dollar residue of 1cfe's own float32 emission. Corrected to the project's A-2 **relative** 1e-6 bar (the residual in M$ is 0.000000 either way). This changed the gate's yardstick to the specified one, not the number.

### Phase 8 — Re-baseline, standing-bars sweep, records — _(GATE: PASS)_
- **What ran.** Executed the design point; re-baselined the recorded anchors with the two-cause attribution; re-ran the handshake and committed `handshake_comparison.json` alone; ran the full standing-bars sweep; filled SV-035; referenced the verdict artifact from the epic.
- **New design-point headline (MR-WI029-9 re-baseline).**

  | anchor | was (WI-028) | now | cause |
  |---|---:|---:|---|
  | total_capital $ | 16,145,706,216.04 | **16,129,706,216.04** | CAS10 fix, **exactly −$16,000,000.00** |
  | LCOE $/MWh | 258.013640 | **275.264220** | see attribution |
  | magnet share % | 39.165025 | **39.203876** | denominator only |
  | p_net MW | 915.081088 | 915.081088 | unchanged |
  | q_eng | 6.606662 | 6.606662 | unchanged |
  | rec_frac | 0.151362 | 0.151362 | unchanged |
  | CAS70 $/yr | — | 170,974,516.955938 | new |
  | CAS80 $/yr | — | 773,037.517724 | new |
  | `lcoe_1cfe` $/MWh | — | 269.861538 | comparison, **not** the headline |

  **Two causes and no third**, arithmetic shown: the annual-cost side entering the LCOE numerator (CAS71 + CAS72 + CAS80 replacing the unlevelized O&M line) = **+17.498627 $/MWh**; the CAS10 error fix taking $16M off total capital = **−0.248047 $/MWh**; sum **+17.250580**, which is exactly the observed 258.013640 → 275.264220. **No multiplier-swap component** — under Option (ii) the headline convention is unchanged (`idc_factor` untouched, `total_capital = overnight_capital`). The 1cfe-form comparison channel is reported alongside and is explicitly not the design-point headline. **This is a re-baseline, not a regression:** the physics spine is unmoved and all five constraint verdicts stay `satisfied`. The spec's MR-WI029-9 clause "total_capital unchanged ($16.146B)" is **corrected** by the design's CAS10 finding — the in-scope correction lowers it by $16M (0.1%).
- **Oracle bit-exact.** All **14** executed channels match the pure-Python oracle at the new headline, worst rel dev **4.13e-16** (bar 1e-9) — including `cas71_annual`, `cas72_annual`, `cas70_annual`, `cas80_annual`, `annual_fuel`, `cas90_1cfe`, `lcoe_1cfe`, all at **0.00e+00** except the two carrying the capital chain (2.86e-16, 2.11e-16).
- **G-8 re-baseline commit.** `31161dbe` — `handshake_comparison.json` **alone**, message beginning "WI-029 G-8 re-baseline:", listing each new row with its signed magnitude and noting the comparison logic is byte-unchanged. Verified: `rel(a, b)` and the row-loop machinery are untouched; the diff adds rows, injected inputs, traps, and one output key (`cas10_closure`). No row was removed.
- **Standing bars — all hold.**
  - **L1:** Errors 0, Warnings 0 (`agentic-mbse validate --level 1 models`); syside offender list = the same 7 names as the Phase-0 baseline. Zero new offender kinds.
  - **WI-022 sha256** `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` — intact. New standing hash recorded: CAS72 impl `06fb1a6e37e46312ecab813241b810feea9cc56429a2cfeca6f16997d3af704c`.
  - **IFE anchors:** Run A LCOE **252.29996307** and f_recirc 0.04166667, Run B LCOE **68.69020165** and f_recirc 0.08333333 — byte-exact. **Run C out-of-scope by [OWNER] ruling 2026-07-20** (teax-vs-HIF pipeline-validator skew; it raises `PipelineValidationError` on `hif_plant_pkg__hif_plant__meier_reactor_cost_calc.thermal_power_gw`). Supersession recorded; **not** counted as a failure. The whole `exploration/ife_e2e/` tree is byte-identical to its committed state — WI-029 touched nothing there.
  - **pytest:** `uv run pytest tests/models/ -q` → **11 failed / 18 passed / 14 skipped / 0 errors** — the recorded tally, unchanged.
  - **Regen stability:** recaptured to `/tmp/wi029_regen.snapshot.json` from the pin worktree and diffed against the committed snapshot — the **only** differing top-level key is `captured_at`; the 5 constraint facts are identical and `constraint_lowering_mode` is still `applied`.
  - **MR-3/MR-4 spot-check:** no concept literal in any new library def (fuel chemistry, fluence limit, replaceable cost, escalation rate are all inputs); every new base carries a `**Source**`/`**Ref**`/`**Basis**` citation to 1cfe at pin `0254385`.
  - **PROTOCOL sealed.** No barred path under `knowledge/holdout/aries-cs/PROTOCOL.md` §3 was read, cited, or opened at any stage of this item. The only §3-adjacent read was the PROTOCOL file itself (required reading). The C220107 power-supplies sub-account remains the footnoted ARIES-lineage exception.
- **SV-035.** Filled by **editing the matrix row directly** (`modeling_project/VALIDATION_MATRIX.md`) — `agentic-mbse pm update-validation` was **not** used, per the WI-028 `|`-corruption finding. Status `pending` → **`passing`**; column count verified unchanged at 9, matching SV-034.
- **Epic.** `.project/backlog/epic_stellarator_mbse_demo.md` Item 4 now references the verdict artifact, records the three success criteria as met, and the Anchor-A row reads "Items 1, 3, 4 done — criterion-3 verdict written: MET".
- **Deviations.** None.

### Surfaced findings (surface-to-orchestrator)

**Finding 1 — six codegen-mechanics adaptations at the Phase-5 checkpoint (the WI-028 Phase-4 class; value-preserving, both trees).** WI-028 hit four of these; this item hit six on the new channels, as the plan anticipated. The governing rule, read out of the pin's source (`extraction/computed_attribute_extractor.py:91-202`): codegen wires a calc input only from a **producer** channel. A plant attribute that mixes a calc output with a sibling classifies `EXPOSE_COMPUTED` and mints nothing; a bare `x.y` alias classifies `EXPOSE_PURE` and mints a `ChannelAlias`; a sibling-only sum classifies `FORMULA` and compiles at part-def scope, minting no instance-scoped key. Two of the six aborted codegen outright (`V11`) and one aborted the teax pipeline validator, so none could have passed silently.

| # | what codegen did | adaptation | why value-preserving |
|---|---|---|---|
| 1 | `cas72_calc.p_neutron` read the plant attribute `p_neutron = fusion.p_fus * (1 − ash_frac)`, which classifies `EXPOSE_COMPUTED` → **`V11` abort**: params key never minted | moved the multiply **inside** `'Levelized Replacement Cost'`: inputs are now `p_fus` (reads the `fusion` producer) + `ash_frac` (settable leaf), and the def computes `p_neutron` on its first line | identical expression, identical operand order, one fewer hop |
| 2 | `lcoe_calc.annual_om` read `annual_om = cas70_annual + cas80_annual`, a sibling-only sum with no part-rooted term → compiled at part-def scope, **`V11` abort** | added `'Annual Cost Rollup'` (library, ADR-002-compliant) with outputs `cas70 = cas71 + cas72` and `annual_total = cas71 + cas72 + cas80`; its inputs read the three calc outputs directly (the `in cas30 = indirect.cost` idiom) | pure addition, same terms, same order; it introduces no economics, only a producer channel |
| 3 | `cas90_1cfe = cas71_calc.crf * (overnight_capital + idc_capital)` classified `EXPOSE_COMPUTED` → dead channel | added `'1cfe-Form Capital Charge'` (library) with `cas90 = crf * (overnight_cost + idc_cost)`; inputs read `cas71_calc.crf`, the `overnight_capital` aggregation, and `idc.cost` | identical expression; trap 5 asserts it reconstructs at rel 0.00e+00 |
| 4 | `lcoe_1cfe = (…) / (8760 · p_net · n_mod · availability)` likewise `EXPOSE_COMPUTED` → dead channel | added `'1cfe-Form LCOE'` (library) with the identical expression; inputs read the `cas90_1cfe_calc`, `cas70_calc`, `cas80_calc` and `pb` producers | identical expression and denominator |
| 5 | `cas80_calc.annual_cost` read the bare alias `annual_fuel = fuel_calc.annual_fuel`, which resolved to the **part-def-scoped** key `mfe_plant__MFE_Power_Plant__annual_fuel` that no parameter group mints → **teax `PipelineValidationError`** | bound the input directly to the producer, `in annual_cost = fuel_calc.annual_fuel`, and dropped the alias (the `fuel_calc__annual_fuel` channel already exists for the A-2 row) | same source value, one indirection removed |
| 6 | the `replacement_cost_per_event` aggregation's `n_mod` LocalTerm resolved to nothing → surfaced as a **null** entry point (`I7`), which pydantic rejected at load | filled it from the harness in both runners with the plant's own declared value, `mfe_plant.sysml:328 attribute n_mod : Real default 1.0` — the same pattern the harness already uses for `special_materials_capital` and `cas28_capital` | restores the declared default rather than choosing one; 1cfe's point is also `n_mod = 1` |

None of the six altered a value, an operand, or an operand order. Every one is graded downstream by the oracle bit-exact bar (rel 1e-9; achieved 0.00e+00 on all six affected channels) and by the A-2 bar. To reuse the DCF core's CRF for adaptation 3 without editing `mfe_lcoe_dcf.sysml` (which the plan forbids and trap 5 asserts), `crf` in `'Levelized Annual Cost'` was promoted from a plain attribute to an `out` attribute — a visibility change only, computed from the same `discount_rate` / `operational_years` the DCF core uses. That keeps one CRF computation site rather than restating the formula, which is what the design asked for.

**Finding 2 — the exec venv lives in the main checkout, not this worktree.** `exploration/pipeline_spike/.venv-exec` is gitignored, so it exists only at `~/1cfe/fusion-tea/`. Any future item running from a fusion-tea worktree must use the absolute path. No behavioural difference; recorded so the next agent does not read the absence as a missing dependency.

**Finding 3 — the KerML Real function library has no `ceiling` and no `clip`.** `RealFunctions` provides `abs`, `arg`, `floor`, `im`, `max`, `min`, `product`, `re`, `round`, `sqrt`, `sum`, and the `To*` conversions. Both were written as exact identities (`ceil(z) = −floor(−z)`, `clip(z, lo, hi) = min(max(z, lo), hi)`). Worth knowing before another account is assigned a rung on the assumption that a guard is expressible.

**Finding 4 — 1cfe's `cas80_fuel` returns M$/yr through an implicit MW→W factor.** `annual_musd` is built from `p_fus [MW] · SECONDS_PER_YR` without the 1e6 to joules, so the missing factor is what makes the result M$ rather than $. A model rolling up in $ must carry the 1e6 explicitly. Filed as an observation about the source's unit convention, not a defect in it — and not a change to 1costingFE ([OWNER] non-goal).

**Nothing was surfaced as a STOP.** No pin was unreachable, no worktree failed, no mirroring delta appeared beyond the known Item-10 comments, codegen did not abort at the final state, CAS72 routed to `MANUAL_REQUIRED` as ruled, impl and mirror agree at rel 0.0, CAS10 reconstructed with residual 0.0, no account missed A-2 for a non-inherited reason, and no standing bar this item did not intend to move broke.

### Tree end state

**One commit made** — `31161dbe`, the plan-sanctioned Phase-8 G-8 re-baseline of `handshake_comparison.json` alone. Everything else is **uncommitted**, for the orchestrator:

- `models/library/analyses/mfe_account_costs.sysml` + staged twin — 6 new calc defs (3 designed + 3 producer-shaping), `crf` promoted to `out`, CAS10 doc note NOAK-corrected.
- `models/designs/generic_mfe/mfe_plant.sysml` + staged twin — the annual-cost wiring, the Option-(ii) comparison-channel calcs, the levelized headline binding.
- `models/designs/stellarator_09/stellarator_plant.sysml` + staged twin — 8 new instance bindings, `precon_fixed_base` 32M → 16M with the NOAK doc.
- `models/library/analyses/mfe_lcoe_dcf.sysml` + staged twin — **untouched, verified**.
- `exploration/stellarator_e2e/stellarator.snapshot.json` — recaptured from the staged tree at pin `06d95f8`.
- `exploration/stellarator_e2e/generated/**` — regenerated at the pin; `levelized_replacement_cost_impl.py` filled by hand (`AUTO_IMPLEMENTED = False`).
- `exploration/stellarator_e2e/{emit_1cfe_point,handshake_1costingfe,verify_stellaris,run_stellaris,run_stellaris_single}.py` — refs, channels, injection, rows, traps, oracle mirror, guard-live checks, re-baselined anchors.
- `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` — the criterion-3 verdict, rewritten wholesale; **new** `build_verdict_report.py` generates it from the executed run.
- `modeling_project/VALIDATION_MATRIX.md` — SV-035 filled, `passing`.
- `.project/backlog/epic_stellarator_mbse_demo.md` — Item 4 and the Anchor-A row updated.
- `data/traceability_matrix.csv` — 11 new rows.
- `work/active/WI-029_handshake-lcoe-construction/plan.md` — this record.

Pin worktrees left in place for the audit: `~/1cfe/sysml-codegen-wi029-pin`, `~/1cfe/teax-wi029-pin`, `~/1cfe/agentic-mbse-wi029-pin`.

**Ready for `/audit-models` → owner close** (Align ruling 2: owner holds close; orchestrator commits after close).

ARTIFACT: work/active/WI-029_handshake-lcoe-construction/plan.md
