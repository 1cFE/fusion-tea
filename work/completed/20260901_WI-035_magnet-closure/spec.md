---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-08-30
Updated: '2026-09-01'
---

# WI-035: Magnet Closure — Derived Field, Structural Limit, Decomposed Cost Accounts

**⛔ This item stops at spec until the owner rules at the checkpoint.** It is task T-001 of goal `magnet-closure`, round 1 (`work/orchestration/goals/magnet-closure/goal.md@11fa3e3d`; trail § Round 1). The requirements below are outcome-level: what the model must do afterward, with mechanisms left to design. § Open decisions for the owner names the two calls only the owner can make. No design, no plan, and no edit under `models/` until the checkpoint passes.

**Required reading: `knowledge/holdout/aries-cs/PROTOCOL.md`.** This is stellarator-demo model-facing work; §2/§3 apply in full and the four sealed PDFs stay unread. Admissible sources: the Stellaris sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` minus barred entries, with **every table value re-verified against the iter-02 raw PDF or page images** (`knowledge/SOURCE_INDEX.md` — the iter-01 text tables are corrupted LLM reconstructions); the EU-DEMO conductor source (`knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/`); 1costingFE at pin `0254385`; the ITER cryoplant pages. No new ingestion inside this item — a missing input is surfaced with honest options, never defaulted (goal reserved gate 2).

## Why this item exists

The goal question (`goal.md@11fa3e3d` § Question): can the magnet system's field, feasibility, and cost be derived from its own engineering design instead of cited constants? The operative meaning is rubric v1 Row 3 (`​.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`), target P3/S3.

- **The fresh grade**: R3.P = 1, R3.S = 2 (`grading.md@fc80e5b2`). P1 because B = 9.0 T is a cited constant and nothing derives field from coil geometry or current — the ampere-meter quantity in the cost model is derived *from* B, never the reverse. S2 because cost follows one engineered quantity (conductor kA·m) but the winding pack, quench protection, cryostat, and testing are all swallowed by the single 5.87 markup.
- **The stakes** (`gap-report.md@fc80e5b2` Band A entry 2): the coil channel is $6.323B — 39.3% of overnight capital, over half of power-core capital — and moved $4.39B → $6.32B on a single field errata. `peak_field_ok` is held×held against held with margin 0.0 by construction: zero design response.
- **The study evidence** (`exploration/stellarator_e2e/studies/20260823-magnet-technology-ab/synthesis.md@00bc1928`, findings #3/#4): no coil-thickness/radial-build/stress coupling anywhere — `B_max` enters only as a verdict bound; and B is never rewarded, so the optimum is always the lowest field the beta limit allows. Discovery rows `20260823-magnet-technology-ab#3` and `#4` are open and `unrouted`; #3 routes here on the owner's checkpoint ruling (#4 is confinement closure, owner-gated out of this goal).

## Current state

- **Field**: `B = 9.0` held in the instance (`models/designs/stellarator_09/stellarator_plant.sysml:133`), `peak_ratio = 2.7666…` held (`:153`), `B_max = 24.9` held (`:161`). `B_peak = B_axis × peak_ratio` (`models/library/analyses/mfe_plasma_scaling.sysml:328`) multiplies held by held; `peak_field_ok` (`models/designs/generic_mfe/mfe_plant.sysml:836-841`) checks that product against the held ceiling. Changing coil geometry or current re-derives nothing.
- **No structural feedback**: no stress, current-density, quench, or winding-pack calculation exists anywhere in `models/` (verified by absence in the grading pass, `grading.md` R3.P).
- **Cost**: 'Magnet Coil Cost' (`models/library/analyses/mfe_magnet_cost.sysml:4-49`) = total_kAm × $/kA·m × `coil_markup = 5.87`, the markup explicitly swallowing winding, quench protection, cryostat, and testing. Siblings already separately homed: power supplies (`mfe_account_costs.sysml:140`, wired `mfe_plant.sysml:356`), primary structure C220105 (`:81`/`:342`), cryoplant capital C220302 inside 'Aux Cooling Cost' (`:559`/`:513`, driven by the computed `p_cryo`).
- **Already computed** (kept, not re-derived): the cryo chain — winding-pack heat inventory → COP → cryoplant electrical (`mfe_cryo_plant.sysml`, WI-024; grader note G5 credits it as the second P2 conjunct already met).
- **The known physics trap** (WI-032, closed `BOUNDED_NEGATIVE`): for this modular QI coil set, Ampère's law on the magnetic axis is a *lower bound* on coil current, not an estimate — Table 8's 48 coils carry ≈644.8 MA-turns against the 571.5 MA-turns that link the axis (≈+13%), because shaping currents largely do not link the axis. Any field↔current relation for Stellaris carries a coil-set linkage factor. Design must treat that factor the way WI-030 treated `peak_ratio`: a held, sourced coil-set geometry fact — never a silent calibration.

## What must be true afterward (requirements)

#### MR-WI035-1: Peak field is computed from coil geometry and coil current
**Type:** Functional | **Priority:** P0 | **Source:** rubric Row 3 P2 anchor; discovery row `20260823-magnet-technology-ab#3`
The model SHALL compute the axis field and the peak winding field from coil geometry and coil current, such that changing coil current or coil-set geometry re-derives the field. Held coil-set geometry facts (e.g. `peak_ratio`, a linkage factor) are permitted as sourced constants; a held *field* is not. At the Stellaris design point the computed fields SHALL reproduce 9.0 T axis / 24.9 T peak within a tolerance design states with its basis.
**Validation:** SV-038.

#### MR-WI035-2: One structural or current-density limit pushes back, with a computed operand
**Type:** Functional | **Priority:** P0 | **Source:** rubric Row 3 P3 anchor; grader note G6 (computed-vs-held is the ladder working)
The model SHALL assert at least one executable viability constraint whose operand (winding-pack stress, or an operational-to-critical current-density margin) is computed from the derived field/current and winding-pack sizing, against a sourced held limit. The constraint SHALL respond to coil sizing and field choice — margin at the design point must not be zero by construction. Sourced limit bases available in-repo: the Stellaris 800 MPa design stress limit (§2.10, peak winding stress ≈600 MPa) and the J_op/J_crit ≤ 80% quench criterion with per-coil J_op 112–124 A/mm² (Table 8 — image-verify). Which limit (or both) is design's choice.
**Validation:** SV-039. **PR-promotion candidate:** "a viability constraint's operand must be computed, not held-vs-held" — the failure mode now recorded three times (`tbr_ok`, `peak_field_ok`, heating).

#### MR-WI035-3: Magnet cost decomposes into separately sized sub-accounts
**Type:** Functional | **Priority:** P0 | **Source:** rubric Row 3 S3 anchor; R3.S why_not_next
The model SHALL cost the magnet as separately sized sub-accounts — at minimum winding pack, magnet structure, and cryoplant, alongside the existing power-supplies account — each following its own engineered quantity with its own source basis, replacing the single 5.87 markup as the sole carrier. The CAS22.1.3 rollup SHALL equal the sum of its sub-accounts. The design-point total is recorded and explained against the current $6.3235B lump — **not fitted to it** (goal invariant: headline moves are expected and honest). Decomposition bases available at the 1costingFE pin: fab markups by material (`costing_constants.yaml:50,53`), `structure_unit_cost` (C220105 pattern), the documented "conductor ~10–15% of finished magnet cost"; plus Stellaris per-coil masses and casing/structure content (Tables 7/8, §2.10 — image-verify).
**Validation:** SV-040.

#### MR-WI035-4: Library stays concept-agnostic; values live in the instance
**Type:** Constraint | **Priority:** P0 | **Source:** project MR-3
New calc/constraint defs SHALL carry no concept values; Stellaris values (coil count, currents, winding-pack dimensions, limits) bind in `stellarator_plant.sysml`; `generic_mfe/mfe_plant.sysml` wires structure only.
**Validation:** grep at audit — no numeric literal beyond defaulted physical constants in library defs.

#### MR-WI035-5: Every value sourced; table values image-verified; no fallbacks
**Type:** Traceability | **Priority:** P0 | **Source:** project MR-4; `SOURCE_INDEX.md` iter-01 caveat
Every new bound value SHALL carry `Source / Ref / Basis` resolving to admissible material, with any Stellaris table value verified against the iter-02 raw PDF or page images (the iter-01 text tables are corrupted). If a needed value has no admissible source, the item SHALL surface the gap with options rather than default it.
**Validation:** citation-by-citation read at audit.

#### MR-WI035-6: Standing owner rulings are preserved
**Type:** Constraint | **Priority:** P0 | **Source:** goal invariants and reserved gates (`goal.md@11fa3e3d`)
The item SHALL NOT: couple field to confinement (Rung C, owner-gated); alter the held `p_pump` (WI-033); retire `vol_cold_cryo` as a settable input (WI-032 R3 ruling `[OWNER 2026-08-27]`); edit the rubric; or fit toward SV-016's pending Q_eng band. The cryo *capital* sub-account (MR-WI035-3) reads the already-computed `p_cryo`; the cold-volume input feeding it stays held.
**Validation:** audit greps + rulings cross-read.

#### MR-WI035-7: Entry-point and committed-study consequences are restated, never silently broken
**Type:** Constraint | **Priority:** P0 | **Source:** `modeling_project/STUDY_POLICY.md` § 2; MR-WI032-5 precedent
If the field derivation retires `B` (or any swept/arm key) as a settable entry point, the item SHALL record the replacement lever set and declare which committed studies are no longer reproducible as written, before any regeneration. Regeneration/verification/pinning itself is the `integrate` seam, invoked separately per the goal runbook — not part of this item's implement stage.
**Validation:** the restatement exists in the item record before regeneration.

## Scope boundaries

**In scope (post-checkpoint):** field-from-current calc def(s) and stress/J-margin calc def in `models/library/analyses/`; constraint def in `mfe_viability.sysml` (or sibling); decomposed magnet cost accounts in the library; wiring in `models/designs/generic_mfe/mfe_plant.sysml`; bindings in `models/designs/stellarator_09/stellarator_plant.sysml` and the byte-identical `exploration/stellarator_e2e/models/` twin; one new instance-asserted constraint.

**Out of scope:** confinement closure (discovery row #4 — owner-gated); `p_pump`, `vol_cold_cryo` re-basing; divertor/heating/vessel rows; rubric edits; new source ingestion; the 1costingFE handshake (Anchor A is closed evidence at `f22bd288` — this item neither re-runs nor preserves it, `[OWNER 2026-08-30]` pin addendum); package regeneration and pinning (separate `integrate` invocation); re-running committed studies.

## Success criteria

- Field: SV-038 — computed axis/peak field reproduces the design point within the stated tolerance and responds to coil current (pending).
- Limit: SV-039 — the new constraint executes with a computed operand, nonzero design-point margin, and real design response (pending).
- Cost: SV-040 — sub-accounts separately sized with source bases; CAS22.1.3 rollup = sum; single-markup path retired (pending).
- Validation Levels 1–3 pass; L1 = 0 with the offender list unchanged (6 pre-existing).
- The affected-studies restatement (MR-WI035-7) exists before any regeneration.

## Assumptions & risks

1. **Winding-pack data sufficiency** (confidence: high): coil currents, turns, J_op, dimensions, masses, the 800 MPa limit, and the 80% J_op/J_crit criterion are all in the admissible Stellaris §2.9/2.10 material. Risk: the text tables are corrupted; every value must be image-verified (MR-WI035-5), and a value that fails verification is a surfaced gap, possibly a `PREREQUISITE` return.
2. **The linkage factor** (confidence: high it exists, medium on treatment): the ≈13% axis-linking shortfall (WI-032) means the field↔current relation needs one held coil-set fact. If design cannot source it as a geometry fact of the printed coil set (Table 8 currents + Table 2 field, the `peak_ratio` move), the P2 claim weakens and the checkpoint reading of "computed from geometry and current" goes back to the owner — a rubric-anchor contest, reserved gate 4.
3. **Decomposition basis** (confidence: medium): 1costingFE's ingredients plus Stellaris masses suffice for separately *sized* sub-accounts without new ingestion. If a sub-account cannot be sized from admissible material, it is surfaced (options: coarser split, or a research-seam request), never defaulted.
4. **P3 without confinement** (strategy assumption, recorded in the round's strategy revision): the Row-3 P3 anchor asks the limit to push on coil sizing and field choice, not on the operating point — reachable while Rung C stays closed.

## Traceability

- **Upstream**: rubric `rubric.md@dc0f0b6d` Row 3; grading `grading.md@fc80e5b2` R3.P/R3.S + G5/G6; gap report `gap-report.md@fc80e5b2` Band A 2; study `20260823-magnet-technology-ab` synthesis findings #3/#4; `DISCOVERY_LOG.md` rows `#3`/`#4`; DI-009 (Carnot fraction), DI-010 (J_eng bands), DI-011 (field↔beta↔ceiling pattern); WI-030 (computed-value precedent), WI-032 (linkage-factor physics, closed R3 ruling).
- **Downstream impacts**: `exploration/stellarator_e2e/generated/` contract entry points (new inputs, possible retirement of `B`); oracle/runner re-baseline; committed studies' reproducibility (MR-WI035-7); the eventual fresh re-grade of Row 3 (`goal.md` § Answered when).
- **Applicable project rules**: MR-3 (library/designs split), MR-4 (citations), PROTOCOL §2/§3.

## Open decisions for the owner (the checkpoint)

**Ruled 2026-08-30.** Decision 1 `[OWNER 2026-08-30]`: **inversion** — coil current becomes the design input and B_axis/B_peak become computed outputs; `B` retires as a settable entry point, with the MR-WI035-7 restatement of affected committed studies. Decision 2: delegated to the round agent by the owner ("I am deferring to you here"); the agent approves the requirement set as scoped `[AGENT] (delegated by owner 2026-08-30)` — the cryo capital sub-account reads the computed `p_cryo` while `vol_cold_cryo` stays a held settable input, keeping this item clear of the WI-032 R3 ruling. The checkpoint is passed; the item proceeds to design.

1. **The lever direction.** The round strategy proposes inverting the field path: coil current (sourced, Table 8) becomes the design input and B_axis/B_peak become computed outputs. That is the straight reading of the P2 anchor ("peak field computed from geometry and coil current"), and it retires `B = 9.0` as a settable entry point — committed studies that swept `B` become non-reproducible as written (restated per MR-WI035-7, the WI-032/MR-WI032-5 shape). The alternative keeps `B` as the lever and derives the *required* coil current from it, feeding the new limit — weaker against the P2 anchor's letter, but no entry-point retirement. The spec is written to work under either; the strategy's stated intent is inversion.
2. **Approve the requirement set as scoped** — in particular MR-WI035-6's reading that the cryo cost sub-account reads computed `p_cryo` while `vol_cold_cryo` stays held, which keeps this item clear of the WI-032 ruling.

## Related artifacts

- Goal: `work/orchestration/goals/magnet-closure/` (question, invariants, reserved gates, limits)
- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Precedents: `work/completed/20260822_WI-030_computed-beta-peak-field/spec.md`; `work/completed/20260827_WI-032_cold-volume-basis/spec.md`
- Design and plan: not created — the item is at spec pending the checkpoint.
