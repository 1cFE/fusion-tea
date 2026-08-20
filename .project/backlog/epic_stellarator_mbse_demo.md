# Epic: Stellarator MBSE Full Demo

**Epic ID**: STELLARATOR-DEMO
**Status**: Ready
**Priority**: High
**Created**: 2026-07-18
**Estimated Effort**: ~10–14 days remaining (excluding the stretch item)

---

## Governing frame

**The governing artifact is `.project/concepts/stellarator-mbse-demo.md`.** Every done-ness assessment for demo work runs against that concept's 8 success criteria and five-stage arc — not against any other epic's items. This epic is the concept's tracking home; it exists because tracking was lost for six days (2026-07-12 → 07-18): the demo's work items were registered under the differently-scoped MFE Cost Modeling epic, and three sessions assessed "what's next" from that borrowed frame before the owner caught it. Every demo handoff and stage brief must name the concept as the governing frame.

**Every item in this epic lists `knowledge/holdout/aries-cs/PROTOCOL.md` as Required Reading.** The ARIES-CS hold-out is sealed; the barred-artifact lists in PROTOCOL §3 are absolute for demo sessions until the owner-triggered reveal.

### Epic home — [OWNER] ratified 2026-07-18

Coding PM is the home base: **one tracking home here in `.project/backlog/`, whose items delegate execution to the right PM system** — modeling items are created in `work/` (via `pm add-item`) at pick-up; tooling/spec/write-up items run as coding-PM items in `.project/active/`. The epic tracks stage and criterion status; each item's execution records live in its own system. This satisfies the concept's decomposition guidance (the work "spans both PM systems") without a mega-epic in either.

---

## Executive Summary

Prove the agentic-mbse / sysml-codegen / teax methodology on a real fusion deep dive: a QI stellarator (concept 09) physics+costing model built and refined with the full toolchain, validated two independent ways — a machinery handshake against 1costingFE (Anchor A) and a clean-room hold-out comparison against ARIES-CS (Anchor B) — exercised through the teax study layer, and written up for a public audience. The demo is 80% methodology validation, 20% proof-by-example ([OWNER], concept).

**Critical Success Factor**: The two anchors hold under honest reporting — the handshake passes a written tolerance spec, and the hold-out comparison is reported against pre-committed expectations, pass or fail.

---

## Source Documents

- `.project/concepts/stellarator-mbse-demo.md` — **concept** (governing; owner-verbatim decisions, non-goals, 8 criteria, five-stage arc)
- `knowledge/holdout/aries-cs/PROTOCOL.md` — **protocol** (quarantine rules, barred lists, reveal procedure, contamination inventory)
- `.project/active/aries-cs-holdout/spec.md` — **spec** (clean-room barred/admissible lists; the demo's first item, complete)
- `work/backlog/epic-mfe-cost-modeling.md` — **epic (adjacent)** (per-item status assessment of WI-009–025; holds the tokamak and sweep as its own non-demo goals)
- `.project/CURRENT_WORK.md` — **status narrative** (Stage 2/3 build history, WI-019–025 records)
- `~/1cfe/sysml-codegen/.project/completed/20260713_epic_constraint_execution.md` — **external epic** (constraint execution + study layer: completed 2026-07-13, IFE acceptance 2294/2301 in this repo)

---

## Why This Epic?

**Current State**:
- The five-stage arc and 8 criteria exist only in the concept; no artifact tracks their execution. Work landed under the MFE epic's frame, which mis-prioritized "what's next" three sessions running.
- Stages 1–2 are done and Stage 3 has run seven audited refinement items (WI-019–025), but the refinements were errata-driven (extraction phantom rows, stale bases), not study-driven as the concept intended — studies have never run.
- Criterion statuses were never mapped: done-ness questions get answered from a borrowed epic's items.

**Future State**:
- One place answers "where is the demo?": stages and criteria mapped to items with honest status.
- The remaining arc — constraint execution, handshake completion, studies, visualization, reveal, write-up — is decomposed into right-sized items with owners' decision points marked.

---

## Success Criteria

These are the concept's 8 criteria, status as verified 2026-07-18. The checkbox is the concept's bar, not a restatement.

- [x] **1. Initial model runs end-to-end** — met. Stage 2 built and committed (`c3f3089e`), refined through WI-025 (`7ba3cd70`). Executed headline at that point (bit-exact vs oracle, rel 1e-9): total $12,638,857,665.74, LCOE $203.647/MWh, p_net 915.081 MW, q_eng 6.607, magnet $6.3235B (50.03%). Every account sourced or forward-computed; zero STALE BASIS annotations. *(Headline re-baselined by Items 3–4: total $16,129,706,216.04, LCOE $275.264220/MWh — the full annual-cost side (levelized O&M, replacement, fuel) now in the numerator and the CAS10 error closed; p_net/q_eng/rec_frac unchanged; oracle bit-exact at the new point — see criterion 3.)*
- [x] **2. Viability checks execute as modeled constraints** — met 2026-07-20 (WI-027, audit POSITIVE, owner-closed). All five asserts (`net_positive`, `recirc_ok`, `beta_ok`, `wall_load_ok`, `tbr_ok`) execute as generated constraint modules; verdicts are data in the run report (`all_satisfied`, 5 assessed, all off-boundary); zero hand-coded viability (grep-proven); headline unchanged to the cent. Route is fully public post-lifecycle-Item-10 (bridge-free, no D7 passthroughs). Records: `work/completed/20260720_WI-027_demo-constraint-execution/`, SV-033, audit `work/analysis/20260720-163628_audit_WI-027_demo-constraint-execution.md`.
- [x] **3. 1costingFE handshake (Anchor A)** — **MET 2026-07-25, verdict confirmed by independent audit; WI-029 owner-closed 2026-08-02.** Item 3 (WI-028, closed 2026-07-20) brought the CAS22 tail + CAS40/50/60 under the ratified bars; Item 4 (WI-029) finished the LCOE construction: CAS70 = CAS71 levelized O&M + CAS72 levelized blanket/divertor replacement (a $82.2M/yr stream the spec discovered — forward-computed on the handwritten rung, 1cfe guards verbatim) + CAS80 fuel, all under A-2 (≤ 5.3e-07); CAS10 closed as one error (residual 0.0, [OWNER] stop condition never fired); IDC ruled Option (ii) — DCF headline untouched, 1cfe-form comparison channels exact (rel 0.0 by trap). **The A-4 reconciliation closes in both channels (~5e-08 rel): the once −31% gap is now fully accounted — every account computed under the bar or one of exactly two itemized lines (C220106_pump −$0.72M; IDC convention +$17.96M/yr, kept by ruling).** A-4 condition-(1) reading ratified at close ([OWNER] 2026-07-25, audit F1). Verdict artifact: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` (generated from the executed run; auditor reproduced byte-identical). Records: `work/completed/20260802_WI-029_handshake-lcoe-construction/`, SV-035 passing, audit `work/analysis/20260725-091831_audit_WI-029_handshake-lcoe-construction.md`, trail `work/orchestration/handshake-lcoe-construction.md`.
- [ ] **4. ARIES-CS hold-out comparison (Anchor B)** — not started, but the per-axis expectations are now pre-committed and ratified (Item 1, 2026-07-19). Quarantine live and sealed since 2026-07-12; reveal is owner-triggered (PROTOCOL §6). → Item 7.
- [ ] **5. Studies run through the teax study layer** — not started, now unblocked: the demo package executes constraints (criterion 2 met 2026-07-20), so verdicts can classify study points. → Item 5.
- [ ] **6. Study outputs visualized** (figures + search-process animation) — not started. → Item 6.
- [ ] **7. Public write-up exists** (blog draft + interactive HTML) — not started. → Item 8.
- [ ] **8. (Stretch) Optimum rediscovery** — not started; post-reveal by design; a miss is ambiguous and does not fail the demo. → Item 9.

### Stage map

| Concept stage | Status | Items |
|---|---|---|
| 1. Concept choice | Done — 09 penciled in ([OWNER]) | — |
| 2. Initial model | Done — WI-009/010/018 substance + codegen chain + handshake machinery | — |
| 3. Agentic research / refinement | Partial — WI-019–025 ran as errata-driven refinement; study-driven rounds have not happened (studies never ran) | interleaves with Item 5 |
| 4. Studies | Constraint execution done (Item 2, 2026-07-20); studies + viz not started | Items 5, 6 |
| 5. Write-up | Not started | Item 8 |
| Anchor A (cross-stage) | **Done — criterion 3 MET** (verdict audit-confirmed; WI-029 closed 2026-08-02) | — |
| Anchor B (cross-stage) | Quarantine done (seam a); comparison not started | Items 1, 7 |

A plain statement, per the concept's honesty bar: WI-019–025 refined the Stage-2 model because execution surfaced defects (phantom table rows, stale bases, unfaithful power balance) — not because studies revealed critical subsystems. The concept's stage-3⇄4 interleave (studies drive refinement) starts with Item 5; further refinement rounds get registered at pick-up when studies surface them.

---

## Backlog Items

Registration convention: modeling items (2, 3, 4, 5, 7, 9) register in the modeling PM (`uv run agentic-mbse pm add-item`, records in `work/active/WI-XXX_*/`) at pick-up — not pre-registered, matching the WI-019–025 precedent. Coding-PM items (1, 6, 8) get `.project/active/{name}/` directories at pick-up. Every item lists the concept and PROTOCOL.md as Required Reading.

### Item 1: Anchor acceptance spec (tolerances + hold-out expectations)

**Status**: **COMPLETE 2026-07-19** — spec written, independently reviewed (3 must-fixes applied), ratified [OWNER] 2026-07-19 ("ratify all, G-8 amend as proposed"). Bars in force: Anchor A |rel dev| ≤ 1e-6 per account + itemized-signed-remainder LCOE form; Anchor B ratios [1/3,3] derived / [0.5,2.0] costs + structural checklist; sizing reallocation to criterion 8 confirmed; successor-bar amendment recorded at `work/orchestration/stale-basis-recompute.md`. Deliverable: `.project/active/demo-anchor-acceptance-spec/spec.md`.

**Type**: Research/Spec (coding PM)
**Effort**: 0.5–1 day
**Dependencies**: None — do this first; Items 3, 4, 7 are judged against it.

**Objective**: Write the pass/fail bars for both anchors that the concept required and no one ever wrote (concept Open Questions 1–2).

**Scope**:
1. **Anchor A tolerance spec**: per-account and LCOE agreement thresholds for the 1costingFE handshake; parameter-mapping traps enumerated (e.g. radiation-model `B` = 5 T vs coil-cost `b_center` = 6 T); the 1costingFE commit pin recorded as a spec requirement; float32-at-runtime in 1cfe cost layers (WI-025 finding) accounted for in the tolerance basis.
2. **Anchor B expectations**: quantitative per-axis expectations (structural similarity, derived-quantity agreement at their design point, rough per-component costs) that are pass/fail for criterion 4 — committed *before* reveal so a miss cannot be narrated away. Include the C220107 exclusion/footnote rule (the one known ARIES-CS-derived 1cfe value).
3. **Apply the criterion-3 ruling** — **[OWNER] 2026-07-18: the bar is *explaining*, and closing any errors.** Remaining discrepancies after Items 3–4 must be itemized and explained; any discrepancy shown to be an error (model, mapping, or sourcing mistake) is closed. Closing the full structural gap is not required. The spec words Items 3–4's acceptance in these terms.

**Out of Scope**:
- Running either comparison — this item only writes the bars.
- Reading any barred artifact (expectations are written blind, from the model side).

**Success Criteria**:
- [x] Anchor A tolerance spec exists with per-account + LCOE thresholds and the commit-pin requirement
- [x] Anchor B per-axis expectations exist, marked pass/fail, written pre-reveal
- [x] Items 3–4 acceptance worded per the [OWNER] criterion-3 ruling (explain discrepancies; close errors)
- [x] Owner sign-off on both specs — ratified 2026-07-19

**Deliverables**: `.project/active/demo-anchor-acceptance-spec/spec.md` (both anchors' bars + owner rulings)

---

### Item 2: Constraint execution in the demo pipeline

**Status**: **COMPLETE 2026-07-20** — executed as WI-027 (registered 2026-07-19, owner-closed 2026-07-20, independent audit POSITIVE with all eight bars reproduced). The run surfaced two toolchain gates (Gate A: INV-2 literal actuals; Gate B: capture-time coverage check), both root-caused here and fixed upstream by the sysml-codegen constraint-execution-lifecycle-remediation epic (Items 2, 3, 10) — the demo now generates on the fully public single-pass route, no bridge, no passthroughs. One out-of-scope finding routed to that epic ([OWNER] ratified): teax-vs-HIF-package validator skew in the IFE Run C regression leg. Orchestration trail: `work/orchestration/demo-constraint-execution.md`.

**Type**: Modeling (modeling PM, register at pick-up)
**Effort**: 1–2 days
**Dependencies**: None internally. External: constraint-execution toolchain — **delivered** (epic completed 2026-07-13; acceptance ran in this repo: `exploration/ife_e2e/study/`, 2294/2301 with the divergence being the hand rule's fault). Caveat: the upstream PR wave is under a P0 remediation epic (`~/1cfe/sysml-codegen/.project/backlog/epic_constraint_pr_wave_remediation.md`, 2026-07-18) and consumer-side follow-ons CE-F1 (standalone catalog emission) / CE-F2 (multi-channel CandidateBridge) are open — pin the local editable-dep commit for the demo and record it.

**Objective**: Criterion 2 — the demo's viability constraints execute as generated modules with verdicts as data in run reports; no hand-coded viability anywhere in the demo.

**Scope**:
1. Regenerate the stellarator package with constraint lowering: the canonical asserts (`net_positive`, `recirc_ok`; instance-level beta / wall-load / TBR) flow through codegen instead of being stripped in the staged copy (the strip comment at the staged `stellarator_plant.sysml:741` retires).
2. Verdicts (`satisfied | violated | indeterminate`) appear in run reports at the Stellaris design point; add the SV validation entry (next free: SV-033).
3. Decide-and-document which constraints are in the executing set now vs deferred to study-driven refinement (concept Open Question 3 — most candidates already exist in the model).
4. Standing bars hold: handshake byte-identity under the successor bar, IFE anchors unchanged, regen stability, WI-022 handwritten-impl hash survives.

**Out of Scope**:
- New physics constraints not already modeled (ISS04 confinement-consistency stays a refinement candidate).
- Study definitions (Item 5).

**Success Criteria**:
- [x] Constraint verdicts appear as data in the demo run report at the design point
- [x] No hand-coded viability rule anywhere in the demo pipeline
- [x] Toolchain commit pinned and recorded; all standing validation bars pass (bar 5's literal IFE Run C leg out-of-scope by [OWNER] ruling — regression intent met, skew routed upstream)
- [x] Modeling-PM item record complete (spec → close per scale)

**Deliverables**: regenerated demo package with executing constraints; run report with verdicts; `work/` item record

---

### Item 3: Handshake account scope — CAS22 tail + CAS40/50/60

**Status**: **COMPLETE 2026-07-20** — executed as WI-028 (registered 2026-07-20, orchestrator-driven, owner-closed 2026-07-20 after a POSITIVE independent audit with all nine bars reproduced). All 11 target accounts forward-computed per the A-3 list; 8/11 under A-2 outright, 3 misses fully explained by the two documented A-4 remainders (audit-recomputed, no third source). Two owner gates ruled mid-run: **full overnight rebuild** (closed rollup errors F-2/F-3 — CAS10 wrongly inside direct capital, missing cas28, indirect on the wrong base) and **CAS60 Option C** (A-2-checked reported line excluded from total_capital; DCF idc_factor untouched; LCOE-side reconciliation stays Item 4). Design-point headline re-baselined: total $16.146B, LCOE $258.01/MWh (physics spine unchanged, all standing bars hold). Premise correction recorded: the target accounts were structurally absent, not injected. Upstream findings filed in the trail (sysml-codegen aggregation scoping; `pm update-validation` `|`-corruption; mid-run pin drift restored per A-6). Records: `work/completed/20260720_WI-028_handshake-account-scope/`, SV-034 passing, audit `work/analysis/20260720-195640_audit_WI-028_handshake-account-scope.md`, trail `work/orchestration/handshake-account-scope.md`.

**Type**: Modeling (modeling PM, register at pick-up)
**Effort**: 1–2 days
**Dependencies**: Item 1 (acceptance judged against the tolerance spec). Parallel with Items 2 and 4.

**Objective**: Model the reactor-plant cost tail and owner/supplementary/IDC accounts the handshake currently fills by injecting 1cfe's own values — the larger share of the −31% structural gap.

**Scope**:
1. CAS22 tail accounts (~$1.09B at the 1 GWe point, per the Stage-2 handshake report): remote handling, installation, coolant, cryoplant balance, waste, fuel handling, I&C — forward-computed from the model's powers/geometry where 1costingFE's formulas allow, sourced per MR-4, pinned to the 1cfe commit.
2. CAS40 (owner) / CAS50 (supplementary) / CAS60 (IDC line) treatment reconciled with the model's DCF convention — a documented mapping, not a fudge.
3. Handshake re-run; injected-value list shrinks correspondingly; remaining injections itemized.

**Out of Scope**:
- LCOE construction accounts (CAS70/80) — Item 4.
- Closing the gap to zero regardless of cost — the bar is the recorded [OWNER] ruling: explain what remains; close what is an error.

**Success Criteria**:
- [x] Named account scopes forward-computed and sourced (all 11 per the A-3 list; MR-4-cited at pin `0254385`). *Premise correction: nothing left an injection map — the accounts were structurally absent, and the documented remainder is the A-4 table (pump, CAS10, CAS60/total_capital convention).*
- [x] Handshake re-run against the Item 1 tolerance spec; result recorded pass/fail per account (8/11 pass A-2; 3 recorded as explained A-4 remainders reconstructing 1cfe exactly; comparison JSON re-baselined as its own commit `feb13ff3` per G-8)
- [x] Standing validation bars pass (empty-diff bar superseded by G-8 for this item as ratified; oracle rel 1e-9 at the new headline; IFE Runs A/B byte-exact, Run C out-of-scope by [OWNER] ruling; regen stability; WI-022 hash intact; pytest 11/18/14/0)

**Deliverables**: library/instance model additions; updated handshake report; `work/` item record — all delivered (see Status).

---

### Item 4: Handshake account scope — LCOE construction (CAS70/80)

**Status**: **COMPLETE — owner-closed 2026-08-02** (executed as WI-029, registered 2026-07-20, audit POSITIVE 9/9 on 2026-07-25 with the verdict arithmetic independently recomputed). Delivered criterion 3's MET verdict — see the criterion-3 entry above for the full result. Both mid-run owner gates ruled: CAS10 option (a) (clean single error, closed residual 0.0; stop condition never fired) and IDC Option (ii) (mapped comparison channel; headline convention itemized +$17.96M/yr). Post-audit rulings recorded 2026-07-25: F1 A-4 reading ratified; CAS71 guard-branch follow-up accepted as an Item-5 pick-up note. New headline: total $16,129,706,216.04 / LCOE $275.264220/MWh. Records: `work/completed/20260802_WI-029_handshake-lcoe-construction/`, SV-035 passing, trail `work/orchestration/handshake-lcoe-construction.md`.

**Type**: Modeling (modeling PM, register at pick-up)
**Effort**: 1–1.5 days
**Dependencies**: Item 1. Item 3 delivered its inputs (2026-07-20): the CAS60 mapping is ruled **Option C** ([OWNER] — CAS60 is an A-2-checked reported line excluded from total_capital; the model's DCF `idc_factor` untouched), so this item's IDC reconciliation starts from that mapping, not from scratch. Pick-up notes: brief against the post-WI-028 harness (rebuilt overnight assembly, new comparison rows, re-baselined `handshake_comparison.json` @ `feb13ff3`); the CAS10 remainder disposition (below) is an owner ruling to collect at pick-up.

**Objective**: Close the LCOE-construction share of the structural gap: levelized O&M and fuel enter the LCOE the way 1costingFE constructs it.

**Scope**:
1. CAS70 levelized O&M (WI-025 delivered unlevelized CAS70; the levelization step into LCOE remains) and CAS80 fuel costs, forward-computed and sourced.
2. IDC treatment reconciled (SysML folds into DCF vs 1costingFE's CAS60 line) — coordinate with Item 3's CAS60 mapping.
3. Handshake re-run; end-to-end LCOE gap re-measured and itemized against the Item 1 ruling.

**Out of Scope**:
- Changes to 1costingFE itself ([OWNER] non-goal: gaps found there are filed, not fixed here).

**Success Criteria**:
- [x] CAS70 levelization + CAS80 in the model's LCOE, sourced per MR-4 — CAS71 (+1.08e-07), CAS72 (+5.22e-07), CAS70 (+3.19e-07), CAS80 (+1.03e-07), all under the A-2 1e-6 bar
- [x] End-to-end LCOE handshake result recorded pass/fail against the Item 1 spec; **criterion-3 verdict written: MET** — `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`
- [x] Standing validation bars pass

**Deliverables**: model additions; final Anchor-A handshake report (criterion-3 evidence); `work/` item record

**Status**: implemented 2026-07-25 as WI-029 (`work/active/WI-029_handshake-lcoe-construction/`), pending audit + owner close.

**The criterion-3 verdict artifact is `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`** — written in the A-4 form and generated from an executed run by `build_verdict_report.py`. It carries (1) the per-account A-2 pass table, (2) the full signed-magnitude remainder itemization, (3) the reconciliation arithmetic shown term by term, and (4) the verdict: **MET**.

Headline results: the residual end-to-end LCOE gap reconciles to the itemized remainder sum in **both** LCOE channels — the 1cfe-form comparison channel at 4.61e-08 and the DCF headline at 4.70e-08 relative to LCOE, both far inside the 1e-6 aggregate tolerance. The remainder is two lines: **C220106_pump −$0.7206M** (the vessel shell-only simplification, explained-and-kept) and the **headline IDC convention +$17.9639M/yr (+2.208%)** on the annual capital charge, kept deliberately under the [OWNER] Option-(ii) ruling of 2026-07-25 (the DCF headline convention stays; a 1cfe-form comparison channel is added alongside). **CAS10 closed as an error** — one mis-set FOAK constant (`precon_fixed_base` 32M → 16M, `plant_studies` 20 → NOAK 4) now reconstructs 1cfe's 18.500000 M$ with residual 0.000000 M$; the owner stop condition did not fire. **CAS72 left the remainder**: $82.230M/yr, previously structurally absent, is now forward-computed on the WI-022 handwritten rung with every 1cfe guard carried verbatim and proven live.

Design-point headline **re-baselined** (not a regression): total capital $16,145,706,216.04 → **$16,129,706,216.04** (down exactly $16,000,000.00 from the CAS10 fix) and LCOE $258.013640 → **$275.264220/MWh**, for exactly two causes and no third — the annual-cost side entering the numerator (+$17.498627/MWh) and the CAS10 capital correction (−$0.248047/MWh), summing to the observed +$17.250580 exactly. No multiplier-swap component: the headline convention is unchanged. The physics spine (p_net 915.081088, q_eng 6.606662, rec_frac 0.151362) is unmoved and all five constraint verdicts stay satisfied.

---

### Item 5: Studies — parameter sweep + A/B swap via the teax study layer

**Type**: Modeling/Execution (modeling PM, register at pick-up)
**Effort**: 1–2 days
**Dependencies**: Item 2 (verdicts must classify points). Items 3–4 improve cost fidelity but do not block starting.

**Objective**: Criterion 5 — at least one parameter sweep and one A/B instance-swap study run as `teax` study definitions, constraint verdicts classifying points, no hand-rolled sweep loops.

**Pick-up notes** (2026-07-25): (1) WI-026 (pytest baseline re-record) is slotted before this item per the [OWNER] board ruling. (2) WI-029 audit follow-up, [OWNER]-accepted: the CAS71 `'Levelized Annual Cost'` calc omits 1cfe's `i ≈ g` guard branch — inert at pinned points, but a discount-rate sweep exercises it; if this item sweeps discount rate, address it first (small bounded fix in the library def + oracle mirror). (3) *(added 2026-08-02)* **Required reading for the Align: `.project/active/demo-study-parameterization-policy/policy.md`** (Draft — owner ratifies at the Align). It carries the axis rule ([OWNER]: sweep causal design levers only, declared at the SysML-attribute level), the constraint-triage rule (inequalities accumulate; discovered couplings internalize, never stand as equality asserts over swept axes), the distributed-cycle resolution ladder, the barred anti-patterns, the in-scope teax construct list, and the three hypotheses (H1–H3) the first study round tests.

**Scope**:
1. Define the first study round (this absorbs the concept's "stage 3⇄4 interleave" spec need): which variables sweep, what the A/B swap is (magnet technology or blanket material are the concept's examples), and what result pattern triggers a research/refinement round.
2. Run both studies through the study layer's delivered execution semantics (prepared lists/grids; resume/crash-safety is the upstream epic's acceptance, not re-proven here).
3. Classified results (viable / violated / indeterminate) land as committed study artifacts; findings ranked by leverage feed the refinement queue (new refinement items register at pick-up, in this epic's frame).

**Out of Scope**:
- Optimizer/adaptive strategies ([AGENT] non-goal in the concept — grids suffice, even for the stretch).
- Visualization (Item 6).

**Success Criteria**:
- [ ] One sweep + one A/B study defined as teax studies and run to completion
- [ ] Constraint verdicts classify every point; zero hand-rolled harness code
- [ ] Research-trigger rule written; refinement candidates (if any) recorded
- [ ] Study artifacts committed; `work/` item record complete

**Deliverables**: study definitions + result stores; first-study-round findings note; `work/` item record

---

### Item 6: Study visualization + search-process animation

**Type**: Code/Implementation (coding PM)
**Effort**: 1–2 days
**Dependencies**: Item 5 (needs real study results).

**Objective**: Criterion 6 — sweep and A/B figures ready to embed in the blog draft, plus the animated design-space visualization the owner called critical ([OWNER-VERBATIM]: "The visualization of outputs will be really critical for this stage. I am imagining a full animation for showing a 'search' process.").

**Scope**:
1. Static figures: sweep feasible-region / classification plots, A/B comparison — publication quality, embeddable.
2. The animation: since studies are prepared lists/grids (no optimizer), it depicts the stage-3⇄4 refinement arc — successive study rounds narrowing on critical subsystems — rendered over study results, not a live search trajectory (concept criterion 6's framing).
3. Reusable enough to re-render when later study rounds land.

**Out of Scope**:
- The interactive HTML explainer page itself (Item 8) — this item produces assets it consumes.

**Success Criteria**:
- [ ] Sweep + A/B figures render from committed study artifacts
- [ ] Animation exists and depicts the refinement arc over real results
- [ ] Assets committed with a regeneration path (script, not hand-edited images)

**Deliverables**: `.project/active/demo-study-viz/` records; figure/animation assets + generation scripts

---

### Item 7: ARIES-CS reveal + hold-out comparison (Anchor B)

**Type**: Modeling (modeling PM, register at pick-up); **owner-triggered** — the reveal is the owner's call, per PROTOCOL §6
**Effort**: 1.5–2 days
**Dependencies**: Item 1 (expectations pre-committed); model frozen at comparison state — sensible after Items 3–4 and at least one Item 5 study round. [OWNER] sequencing call on when to trigger.

**Objective**: Criterion 4 — evaluate the finished model at the ARIES-CS design point and report against the pre-committed expectations, pass or fail.

**Scope**:
1. Reveal per PROTOCOL §6: owner flips status, logs the unseal; extraction lands only in `knowledge/holdout/aries-cs/extracted/`; extraction-quality remediation happens now (deferred from ingestion by owner decision).
2. Freeze and record the model state under comparison (commit hash + package fingerprint).
3. Evaluate at the ARIES-CS design point (their geometry and magnet technology); compare per the Item 1 axes: structural similarity, derived quantities (radial-build consequences, coil mass, power flows), rough per-component costs; C220107 excluded/footnoted.
4. Comparison report states pass/fail per axis against the pre-committed expectations; a miss is a demo finding, not narrated away. Derived-artifact rule (PROTOCOL §4) binds: ARIES-CS material lands only in the designated locations.

**Out of Scope**:
- Vintage-assumption sourcing and the rediscovery search (Item 9).
- Any model change motivated by ARIES-CS content — the model is frozen; post-reveal refinements would contaminate the claim.

**Success Criteria**:
- [ ] Reveal executed and logged per PROTOCOL §6; extraction remediated in the quarantine-designated location
- [ ] Model state frozen and recorded before any comparison
- [ ] Comparison report with per-axis pass/fail vs pre-committed expectations; contamination inventory referenced
- [ ] Criterion 4 verdict recorded in this epic, honest either way

**Deliverables**: reveal log entry; `knowledge/holdout/aries-cs/extracted/`; hold-out comparison report; `work/` item record

---

### Item 8: Public write-up — blog draft + interactive HTML

**Type**: Code/Documentation (coding PM)
**Effort**: 1.5–2 days
**Dependencies**: Items 4, 5, 6, 7 for content (the criterion-6 figures ship embedded in this draft). Structure/outline can start earlier; final draft needs the anchors' outcomes.

**Objective**: Criterion 7 — a blog-post draft plus supporting GitHub-hosted interactive HTML that make the methodology legible without fusion-TEA background.

**Scope**:
1. Blog draft: how a SysML model becomes a running cost pipeline; the forward-pass-and-assess vs inverse-solver framing with the 1costingFE handshake as the concrete illustration (concept Key Concept 4); the hold-out protocol and its results reported honestly, including the scoped claim ("no ARIES-CS material in context or sources during model development") and the training-data-priors disclosure.
2. Interactive HTML (follow the `html-explainer` skill): the demo arc, embedded figures and animation from Item 6.
3. Write-up split (blog vs HTML vs possible live tool — concept Open Question 6): propose at spec, owner decides.

**Out of Scope**:
- Publishing/hosting mechanics beyond a GitHub-hosted page; a live tool is a possible follow-on, not this item.

**Success Criteria**:
- [ ] Blog draft complete with embedded criterion-6 figures and honest anchor reporting
- [ ] Interactive HTML page renders the demo arc (verify with browser-inspect)
- [ ] Owner has ruled on the write-up split
- [ ] Draft reviewed against the concept's US-5 ("legible without fusion-TEA background")

**Deliverables**: `.project/active/demo-writeup/` records; blog draft; HTML page

---

### Item 9 (stretch): Optimum rediscovery at ARIES-CS-era assumptions

**Type**: Modeling/Execution (modeling PM, register at pick-up); post-reveal only
**Effort**: 1–2 days
**Dependencies**: Item 7 (requires reading ARIES-CS for vintage assumptions). Explicitly optional.

**Objective**: Criterion 8 (stretch) — a constrained grid search over sizing variables with ARIES-CS-era technology and cost assumptions, compared against their published optimized sizing.

**Scope**:
1. Source the vintage assumption set from the revealed papers (concept Open Question 5); model frozen as of comparison time — only input values change.
2. Run as a mechanical grid via the study layer; compare against published sizing.
3. Report as showcase-if-it-works: a miss is ambiguous (model vs vintage-assumption error) and does not fail the demo — say so in the report.

**Out of Scope**:
- Adaptive/optimizer search; model changes of any kind.

**Success Criteria**:
- [ ] Vintage assumption set documented with sources
- [ ] Grid search run through the study layer; comparison reported with the ambiguity caveat
- [ ] Criterion 8 status recorded (met / attempted-miss / skipped)

**Deliverables**: study definition + results; comparison note; `work/` item record

---

## Board housekeeping (recorded here, ruled by owner)

Not epic items — decisions the owner makes, recorded in this epic when ruled so the board stops carrying ambiguity:

- **WI-009 / WI-010 / WI-018 disposition — RULED [OWNER] 2026-07-25: close as superseded (option c).** Substance built and refined through the WI-019–028 corrective run, whose audited records are the effective completion evidence; each item closed with a disposition note in its record — no close-out audit vs own spec, no spec re-scope. Noted in the notes: WI-010's "LCOE within a credible MFE range at defaults" bar was never formally assessed (decision record, not an open action).
- **SV-016 (Q_eng ~10–40 band) — RULED [OWNER] 2026-07-25: option (i), re-derive the band from source. EXECUTED same day; outcome: source silent, finding recorded.** The Stellaris paper prints gross electric ~1000 MW but never net electric, recirculating power, or Q_eng, and explicitly defers parasitic electricity ("outside the scope of this paper"). Recorded as a finding in the SV-016 row per the ruling; band not fitted. The check also surfaced that the ~10–40 band has no external source (it is internal to the WI-009 spec), while the only sourced admissible convention is 1costingFE's recirc knee (rec_frac ≤ 0.5, Q_eng ≥ 2 — `mfe_viability.sysml:21-38`) and 1cfe's own reference point runs q_eng 8.835, also below the band. **One follow-on parked for owner**: replace the band with the sourced knee (SV-016 becomes assessable and passes on sourced, measurement-independent grounds) vs keep the band and mark the row failed-explained.
- **WI-026 (pytest baseline re-record) — RULED [OWNER] 2026-07-25: slot immediately after WI-029, before Item 5 (studies). EXECUTED same day (fix, not retire).** All 11 stale tests rewritten intent-preserving against the current layout; suite now **30 passed / 13 skipped / 0 failed** (one skip un-skipped by the shared path fix). Standing per-item pytest bar becomes **green (0 failed / 0 errors)**, replacing "tally unchanged vs 11/18/14/0". Record: `work/completed/20260725_WI-026_pytest-baseline-re-record/`.
- **CAS10 remainder disposition — RESOLVED.** Ruled error-to-close at the WI-029 Align ([OWNER] 2026-07-20, ruling 4, with stop condition); design found one clean error (FOAK plant_studies 20.0 vs NOAK 4.0; fix reconstructs 1cfe's 18.5 with residual 0.0) — stop condition did not fire; the fix ships inside WI-029. Owner confirmed 2026-07-25; no separate action.
- **Adjacent, not demo work** ([OWNER] non-goal): the tokamak instantiation and the self-contained viability sweep remain the MFE epic's own deferred goals; they do not gate or count toward any demo criterion.

---

## Dependencies

**External**:
- Constraint-execution toolchain (sysml-codegen / agentic-mbse / teax): delivered 2026-07-13, proven in-repo on IFE. Risk: P0 PR-wave remediation epic in flight upstream; CE-F1/CE-F2 open. Mitigation: pin the local editable-dep commit per item.
- 1costingFE: comparison anchor, pinned commit recorded per handshake run ([OWNER] non-goal: no changes to it).
- SysIDE license (`.env`), snapshot path as fallback.

**Internal**:
- The sealed quarantine (`knowledge/holdout/aries-cs/`) — intact until Item 7's owner-triggered reveal.

**Item Dependency Graph**:
```
Item 1 (anchor acceptance spec)            Item 2 (constraint execution)
  ├─> Item 3 (CAS22 tail + 40/50/60) ──┐     └─> Item 5 (studies) ──> Item 6 (visualization)
  ├─> Item 4 (LCOE construction) ──────┤            │
  └───────────────┐                    ├────────────┴──> Item 7 (reveal + comparison, owner-triggered)
                  └────────────────────┘                       ├─> Item 8 (write-up; also needs 5, 6)
                                                               └─> Item 9 (stretch, optional)
```
Items 1 and 2 start independently (parallel). Items 3 and 4 parallel after 1. Critical path: 1 → 3/4 → 7 → 8 on the anchor side; 2 → 5 → 6 → 8 on the study side.

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hold-out comparison misses the pre-committed expectations ([OWNER-VERBATIM]: "But this is a risk.") | High | Expectations written pre-reveal (Item 1); a miss is reported as a demo finding per the concept — the honesty is the credibility. |
| Upstream constraint-exec churn (P0 remediation wave; CE-F1/F2 open) shifts behavior under the demo | Medium | Pin the toolchain commit per item; re-verify standing bars on any bump; adopt wave output deliberately, not implicitly. |
| The −31% structural gap resists the account-scope items within tolerance | Medium | Bounded by the [OWNER] ruling (2026-07-18): remaining gap is itemized and explained, errors are closed; full closure is not required. |
| 1costingFE float32 runtime layers complicate tolerance definition | Low | Item 1 sets tolerances with the float32 floor in evidence (WI-025 design finding, f64 comparison path exists). |
| Frame loss recurs — future sessions assess progress from item records instead of the concept | Medium | This epic + the standing rule: every demo handoff/brief names the concept as governing frame; done-ness runs against the 8 criteria. |
| Quarantine violated before reveal | High | PROTOCOL required reading on every item; §6 violation log + pre-decided deny-hook escalation. |

---

## Timeline

**Total remaining**: ~10–14 days (excluding Item 9)

| Item | Effort | Dependencies |
|------|--------|--------------|
| 1. Anchor acceptance spec | 0.5–1 d | None |
| 2. Constraint execution | 1–2 d | None (external pin) |
| 3. CAS22 tail + 40/50/60 | 1–2 d | Item 1 |
| 4. LCOE construction | 1–1.5 d | Item 1 |
| 5. Studies | 1–2 d | Item 2 |
| 6. Visualization | 1–2 d | Item 5 |
| 7. Reveal + comparison | 1.5–2 d | Items 1, 3, 4; owner-triggered |
| 8. Write-up | 1.5–2 d | Items 4, 5, 6, 7 |
| 9. Stretch: rediscovery | 1–2 d | Item 7; optional |

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete. One is pre-registered from the recovery itself:*

**Surprises**:
- Item-level rolling handoffs carried bars, numbers, and procedures faithfully but dropped the governing concept — three sessions assessed "what's next" from a borrowed epic's frame before the owner caught it. The fix is structural (this epic + the governing-frame rule), not vigilance.

---

**Last Updated**: 2026-08-02
**Next Action**: Item 5 (studies — pick-up notes in its section: WI-026 done, CAS71 guard-branch follow-up if sweeping discount rate). Anchor A is finished (criterion 3 MET); Item 7 (owner-triggered reveal) is now sequenced behind at least one Item-5 study round per its dependency note — the reveal timing is the owner's call. Items 1–4 complete.
