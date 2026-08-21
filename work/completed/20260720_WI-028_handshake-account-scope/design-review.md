---
Verdict: fail
Created: 2026-07-20
Related Artifacts:
  Design: ./design.md
  Spec: ./spec.md
  Brief: ../../orchestration/handshake-account-scope.md
---

# WI-028 Design Review — Handshake account scope (CAS22 tail + CAS40/50/60)

**Verdict: Revise.** One genuine must-fix. The design's technical substance is verified-sound — every 1cfe formula and assembly fact was independently re-derived at the pin and matches source, the four findings (F-1..F-4) are all confirmed against the actual code and the comparison JSON, both prototypes parse clean, the library defs are MR-3-clean and codegen-envelope-clean, and the A-4/A-5/CAS60-gate treatment covers what the spec requires. The single blocker is an omission, not an error in the approach: the design edits only the canonical model tree, but the codegen snapshot is captured from a separate **staged twin**, and the checklist never syncs it. Implemented as written, the generated pipeline would never see the D2 restructure. That is a bounded fix — mirror the WI-025/WI-027 pattern — after which this is ready to plan.

---

## What I verified independently (not trusted from the design)

- **1cfe formulas at pin `0254385`** — re-read from source (`~/1cfe/1costingfe`, HEAD confirmed `0254385`). All eight CAS22-tail formulas (C220110/111/200/300/400/500/600/700), CAS40, CAS50 (all six terms + bases), CAS60 `f_idc`, and every assembly fact (M1–M7: CAS10 outside cas2x; c29 on pre-contingency; c30 on post-contingency c20 with the 8/6 factor; overnight = c10+c20+c30+c40+c50; c28 = 5.0; total = overnight+c60) **CONFIRMED**. The per-module vs plant-total split (p_et, p_cryo per-module; the rest ×n_mod), the `installation_frac` 0.14 on the C220101‥110 subtotal, and the F-1 spares-parameter misnaming (`cas22_to_28` in the signature, fed c23‥28 at `model.py:1492`) all check out against source. The numeric assembly reproduces (c30 1522.919, f_idc 0.282476, total 10095.837).
- **F-2/F-3/F-4 against the current model** — `mfe_plant.sysml:400-424` confirms `direct_capital` folds in CAS10 (`preconstruction_capital`, :402) and omits c28; contingency (:408) and indirect (:417) are both on `direct_capital` (pre-contingency, CAS10-inclusive). `handshake_comparison.json` confirms the cited rows (cas20 5710.95/4646.41 = −18.64%; indirect 1522.92/1239.04; CAS10 18.50/34.50). All **CONFIRMED**.
- **Prototype parses** — re-ran `syside check`. `mfe_tail_supplementary_costs.sysml` passes standalone. `plant_chain_probe.sysml` passes when checked with its real deps (`mfe_account_costs.sysml` + the tail file); the residual output is namespace-shadowing *warnings* from the `in x = x` probe idiom, which the design correctly attributes to the probe. **CONFIRMED clean.**
- **Codegen envelope + precedent** — all 7 defs are flat Real arithmetic (`+ - * / **`, no if/lookup/sum). The variable-exponent claim is real: `mfe_lcoe_dcf.sysml:47` has `(1.0 + discount_rate) ** (construction_years / 2.0)`, and that same working def already uses intermediate (non-in/out) attributes, so the IDC def's `f_idc` intermediate is a proven pattern. **CONFIRMED.**
- **MR-3 cleanliness** — no Stellaris-specific literal in the library defs; bases/fuel factors are `in` attributes bound at the instance; `concept_scale` is an `in` with no default (correctly instance-bound). **CONFIRMED.**
- **Snapshot source** — `stellarator.snapshot.json` carries 59 path references to `exploration/stellarator_e2e/models/…` and zero to canonical `models/designs/…`; `snapshot()` in `handshake_1costingfe.py:128` reads the staged-tree files. **CONFIRMED — codegen's input is the staged twin.**

---

## Must-fix

**M1 — The D2 restructure and D5 instance bindings must be propagated to the staged model twin, and the snapshot recaptured from it. As written, the pipeline never sees the restructure.**

- **What.** Codegen's actual input is the staged twin at `exploration/stellarator_e2e/models/`, not canonical `models/`. The snapshot (`stellarator.snapshot.json`) is captured from the staged tree — its internal file paths reference `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` (38×) and never canonical. The handshake and runner then execute the pre-built `generated/` package produced from that snapshot; the `.sysml` files matter only at capture time, and capture reads the staged tree.
- **Where.** Design Implementation Checklist (design.md:255-261) and Traceability "Model" list (design.md:292) name only canonical paths (`models/designs/generic_mfe/mfe_plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml`). The spec and design never mention "staged", "twin", "snapshot", or "recapture". Step 3 ("Codegen capture checkpoint") says only "confirm the chain compiles" — it does not say to apply D2 to the twin or to recapture from the staged tree.
- **Why it's a must-fix.** Implemented literally, D2/D5 land only on canonical `models/`; the recapture reads the stale staged twin (old flat `direct_capital` rollup, no CAS22 tail, no CAS40/50/60); the generated handshake pipeline produces the *old* structure. Every A-2/A-4 result and the design-point re-baseline would be computed against a model that does not contain the restructure — a silent wrong result, not a loud failure.
- **Precedent this omits.** Both prior items handled this explicitly. WI-025 plan: "the staged tree is what the Phase 4 snapshot reads," and its Files entries listed *both* trees with a per-phase mirroring `diff` check. WI-027 plan: "the snapshot, not the `.sysml`, is codegen's input"; it edited the staged twins and recaptured from the staged tree.
- **Fix.** Mirror WI-025:
  1. Add the staged twins to the Files/Traceability list — `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml`, `.../designs/stellarator_09/stellarator_plant.sysml`, and the library twin `.../models/analyses/mfe_account_costs.sysml` (the 10 new defs must land in the staged library file too).
  2. In checklist step 2 (generic plant) and step 4 (instance), apply the same D2 restructure and D5 bindings to the staged twins, region-identical.
  3. Add a per-phase mirroring `diff` gate (staged vs canonical shows only the intended edits plus the known WI-015 DEMO-NOTE divergences; any other delta is a defect). Note the caveat: the staged `mfe_plant.sysml` currently carries extra "Item 10" comment lines — reconcile, don't blind-overwrite.
  4. Make checklist step 3 explicit: recapture the snapshot from `exploration/stellarator_e2e/models/` after the twin carries the restructure; that snapshot is what `sysml-codegen generate --from-snapshot` consumes.

---

## Should-fix

- **S1 — "Forces the rebuild" over-claims; name the narrower alternative as a rejected-alternative record.** CAS50 under A-2 needs only faithful `cas20`/`cas23_to_28`/`cas30` aggregates as its inputs; those can be built as dedicated attributes feeding only the CAS40/CAS50 calcs, leaving `direct_capital`/contingency/indirect/`total_capital`/LCOE untouched (those names are new — no conflict). By the design's own CAS60 logic (the account *value* is what A-2 tests, wiring is separate, design.md:169), the headline rollup is not on the A-2 critical path. The rebuild is the better *engineering* answer (it avoids a divergent shadow `cas20`/`cas30` and it fixes the knowingly-wrong headline LCOE), but it is a *separately-motivated* correctness+coherence change bundled into an account-scope item — not something the A-2 bar strictly compels. The design already surfaces the scope tension to the owner (good, per capture-fidelity §4); it should also, per capture-fidelity §3, record the narrow isolated-aggregate option and its one-line rejection reason so the owner's gate is a choice between two named options rather than a single "rebuild required" framing. (Substance of the recommendation stands.)
- **S2 — "Ten library calc defs" / "(10 calc defs)" is a miscount.** The prototype file defines **7** calc defs (`'Plant Power-Law Cost'` is reused for 5 accounts). "10" is the account count, not the def count. Fix the Overview (design.md:16), D1 heading (:103), and the Validation Report line "mfe_tail_supplementary_costs.sysml (10 calc defs)" (:245), which is literally false about the artifact it validated.
- **S3 — The written LCOE denominator drops `n_mod`.** design.md:62 writes `(8760*p_net*avail)`; source (`economics.py:90`, fed at `model.py:1604`) is `8760 * p_net * n_mod * availability`. Inert at n_mod=1, but in a design whose whole theme is "carry n_mod explicitly so it generalizes," the re-derivation should show it. (The model's actual LCOE calc uses plant-total `net_electric_mw`, so executed results are unaffected — documentation only.)
- **S4 — CAS10 percentage uses an inconsistent denominator.** design.md:89 labels CAS10 "+46.4%" (model as denominator); the −18.64% rows use the 1cfe value as denominator, against which CAS10 is +86.5%. Pick one convention. The A-4 remainder line (:209) uses signed dollars (+16.0 M$), which is fine.
- **S5 — Prototype warning count understated.** The design says "two namespace-shadowing warnings"; the real deps check emits more (alpha ×5, cas20/cas23_to_28/cas30/p_net). They are all benign `in x = x` probe artifacts as claimed — just make the count accurate.

---

## Checks that passed (no action)

- Formula re-derivation, assembly facts, F-1..F-4, JSON rows — all confirmed against source (above).
- A-3 completeness: comparison rows (design D5) and traps (D6) cover all 11 target accounts (8 tail + CAS40/50/60). A-3-over-epic-prose honored (C220600 and aux-cooling included).
- CAS60 reserved-gate treatment is consistent with MR-WI028-3: the IDC line is computed as a value for the A-2 check; only its wiring into `total_capital` is gated; double-count hazard correctly identified; design built CAS60-independent.
- Toolchain pins: 1cfe HEAD confirmed at `0254385`. sysml-codegen/teax movement handled deliberately (pinned to WI-027 commits), consistent with A-6 and the spec's standing bars.
- MR-4: bases carry 1cfe citations; concept-agnostic defs in `models/library/`, instance bindings in `models/designs/stellarator_09/` (MR-3).

---

## Recommendation

Address **M1** (add the staged-twin sync + recapture to the checklist and traceability). Fold in S1–S5 while there. Then proceed to `/plan-model` — the codegen-capture checkpoint (Validation Plan step 2) remains the right first de-risk for the 4-deep cross-calc chain, and it must run against the *recaptured* snapshot per M1.

ARTIFACT: work/active/WI-028_handshake-account-scope/design-review.md
