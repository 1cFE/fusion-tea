# Spec: Anchor Acceptance Bars — Anchor A handshake tolerances + Anchor B hold-out expectations

**Status:** Ratified — [OWNER] 2026-07-19: all proposals ratified as proposed; G-8 successor-bar amendment in force
**Owner:** Reid W
**Created:** 2026-07-18
**Complexity:** MEDIUM
**Branch:** feat/stellarator-mbse-demo

---

## Problem

The stellarator demo validates its model two independent ways, and the concept required a written pass/fail bar for each before either comparison runs (concept Open Questions 1–2). Neither bar was ever written.

- **Anchor A** (the 1costingFE handshake) has a byte-stable, bit-exact machinery record but no tolerance spec. Its per-account agreement is measured; what counts as *pass* is not written down. Worse, the current handshake reproduces only 12 formula-computed accounts and *injects* 1costingFE's own values for the rest — a −31% structural LCOE gap that later items (3, 4) must close or explain. Without a written boundary, "handshake passes" has no defined meaning.
- **Anchor B** (the ARIES-CS hold-out) is a sealed blind. The model's output at the ARIES-CS design point does not exist yet, and the reference is quarantined until the owner-triggered reveal. Expectations must be committed *pre-reveal* so a miss cannot be narrated away after the fact — which means they must be band widths set from model-side evidence only, never point targets and never reasoned backward from what ARIES-CS "probably" is.

This spec writes both bars. The spec document is the deliverable; there is no design/plan/implement after it. A spec review follows, then owner ratification of the consolidated proposal list at the end. Items 3, 4, and 7 are judged against what this spec sets.

**This spec proposes every number; the owner ratifies.** ([OWNER] reserved gate, 2026-07-18.) The ratification section was marked **2026-07-19: all proposals ratified as proposed, G-8 amended as proposed** — everything in this spec is in force.

## Success Criteria

- [x] Anchor A has a per-account pass bar and an end-state LCOE acceptance form, with the three test tiers kept distinct.
- [x] The Anchor A gap boundary is drawn account-by-account: which accounts Items 3–4 must bring under the per-account bar, and what may remain as itemized-and-explained remainder.
- [x] The mapping-trap inventory is a spec requirement: every trap asserted in the handshake, not assumed; new traps added as Items 3–4 introduce them.
- [x] The 1costingFE commit pin is a recorded requirement, and a pin-bump procedure exists.
- [x] Anchor B has a per-axis, band-shaped, pre-reveal expectation for structural similarity, derived quantities, and rough per-component costs — each pass/fail.
- [x] The C220107 exclusion (Anchor B) and the sizing-axis exclusion (criterion 8, not 4) are stated.
- [x] The prior-leak bar is written into the spec as a constraint on how Item 7 argues.
- [x] The G-8 premise conflict is surfaced with a proposed amendment, marked pending — not resolved silently (ruled by owner 2026-07-19: amended as proposed).
- [x] Owner sign-off on the consolidated proposal list (this is the concept's "owner sign-off on both specs") — marked 2026-07-19.

## Known Requirements

**Provenance tags used here** (per `capture-fidelity`, spec + shaping registers blended because this spec both absorbs owner rulings and proposes numbers):
- **[OWNER]** — the owner said it; settled, challengeable only by asking the owner.
- **[AGENT-PROPOSED — owner ratifies]** — a number or rule this spec proposes; not in force until ratified. Every one is repeated in the final section.
- **[HARD]** — forced by an interface, physics, or a measured floor; not negotiable.
- **[INHERITED: src]** — absorbed from an upstream artifact (research §X, concept criterion N, PROTOCOL §N); authority is that document, carried with the citation.

Evidence for every Anchor-A number lives in `.project/research/20260718-205525_anchor-acceptance-evidence-stellarator-demo.md` (cited by section, e.g. "research §B"). This spec carries the bars and their one-line bases; it does not restate the evidence.

---

### Anchor A — 1costingFE handshake tolerances

**A-1. The three test tiers are distinct and must not be conflated.** [HARD] [INHERITED: research §A, §B]

Three comparisons exist. They test different things and carry different bars. The spec names all three and keeps them separate.

| Tier | What it proves | Bar | Status |
|---|---|---|---|
| **Pipeline vs pure-Python oracle** (float64) | codegen + teax execution is faithful to the reproduced formulas | rel **1e-9** (bit-exact) | already standing and met; **not** the handshake bar |
| **Formula isolation** (SysML cost formula fed 1cfe's own powers) | the reproduced formula equals 1cfe's formula | ~1e-8 diagnostic (worst −7.63e-8, structure) | diagnostic sub-check, not the pass gate |
| **End-to-end handshake** (SysML computes powers, then costs, vs 1cfe's float32 runtime) | the whole chain reproduces 1cfe at 1cfe's point | **A-2 below** | the handshake pass gate |

The pipeline-vs-oracle 1e-9 bar (float64) is a different test from the pipeline-vs-1cfe bar (against 1cfe's float32 runtime). Asking the handshake to meet 1e-9 would test float32 noise, not the machinery. Keep them apart in every report.

**A-2. Per-account handshake pass bar: |relative deviation| ≤ 1e-6.** [AGENT-PROPOSED — owner ratifies]

- **Applies to:** each formula-reproduced account, comparing the SysML pipeline's end-to-end value against 1costingFE's float32 runtime value (the 12 accounts in research §A, and any account Items 3–4 bring under the bar). The deviation is the handshake's `rel_dev` sense — (model − reference) / reference — and the bar is on its **magnitude**, so a −20.6% miss (`rel_dev = −0.206`) fails, not passes.
- **Ceiling, not a shared floor:** 1e-6 is a ceiling. The 12 formula-reproduced accounts have a measured float32 floor of ~1e-7; accounts Items 3–4 newly bring under the bar are measured against the **same 1e-6 bar** at first measurement (no grandfathering), and most have less float32 noise, not more (research §B notes CAS70 O&M has "no jnp in line" — no float32 rounding at all), so they pass more easily. Any account that legitimately cannot meet 1e-6 becomes explained remainder under A-4, not a loosened bar.
- **Basis:** 1costingFE runs jax at float32 at runtime, so per-account agreement has a hard floor of **~1e-7 relative** (worst measured −4.8e-8 at CAS21; power table +6.23e-8; heat_rejection end-to-end +1.0e-7) — research §B. A bar tighter than ~1e-7 is physically unachievable and would test float32 rounding, not the model. Real modeling or mapping errors show up at **percent scale** (research §E; the f_shape trap produced −20.6%). A bar of **1e-6** sits ~10× above the float32 floor with headroom and ~10⁴× below where real errors appear, so it passes clean machinery and fails any real error loudly.
- **The ~1e-7 float32 floor is [HARD]** — the bar may be loosened above 1e-6 but not tightened below the floor.

**A-3. Gap boundary — account-by-account.** [INHERITED: research §D] [OWNER criterion-3 ruling]

The handshake currently reproduces 12 accounts under tolerance and fills the rest by injecting 1cfe's own values or leaving them structurally absent — the −31% LCOE gap (1cfe LCOE $123.74 vs SysML $85.55; total capital $10.096B vs $5.865B). The boundary this spec draws:

- **Must come under the A-2 per-account bar after Items 3–4** (forward-computed and sourced):
  - **Item 3** — CAS22 tail (~$1.094B at the 1 GWe point: C220110 remote handling, C220111 installation, C220200 coolant, C220300 aux cooling + cryoplant, C220400 waste, C220500 fuel handling, C220600 other, C220700 I&C), plus CAS40 owner ($41.2M), CAS50 supplementary ($578.6M), CAS60 IDC line ($2224M).
  - **Item 4** — CAS70 levelization into LCOE, CAS80 fuel, and IDC treatment reconciled with the model's DCF convention.
- **May remain as itemized-and-explained remainder** (per the [OWNER] criterion-3 ruling, 2026-07-18): whatever 1costingFE legitimately carries that the model does not — documented simplifications (e.g. the C220106 vessel gas-load pump sub-term, $0.72M), or 1cfe quirks filed as findings ([OWNER] non-goal: no changes to 1costingFE).

**[OWNER] criterion-3 ruling, as ruled 2026-07-18** (an [OWNER] paraphrase from the epic, carried at full force): remaining discrepancies after Items 3–4 are **itemized and explained**; anything shown to be an **error** (model, mapping, or sourcing mistake) is **closed**; full structural-gap closure is **not** required.

**Nuance to record (research §D):** CAS21 buildings, CAS10 preconstruction, and CAS70 O&M are *injected* in the handshake but already *forward-computed in the instance* (WI-025). "Injected in the handshake" therefore does not mean "unmodeled" for these three — the handshake injection is a handshake-point tautology, not a modeling gap.

**A-4. End-state LCOE acceptance form.** [AGENT-PROPOSED — owner ratifies]

After Items 3–4, the end-to-end LCOE comparison passes when **both** hold — not a blanket LCOE percentage:

1. **Every modeled account** (the 12 formula-reproduced plus each account Items 3–4 bring in) is under the A-2 per-account bar (|relative deviation| ≤ 1e-6).
2. **The remainder is fully itemized with signed magnitudes**: every account that is not under the bar is listed with its 1cfe value, the model's value (or "structurally absent"), the signed dollar gap, and a one-line reason — closed-as-error, or explained-and-kept per the criterion-3 ruling. **Reconciliation:** the residual LCOE gap equals the itemized-remainder sum to within an aggregate tolerance — the accumulated per-account 1e-6 tolerances of the modeled accounts (equivalently, ≤ 1e-6 relative to LCOE) — distinct from the per-account bar itself.

**Basis:** a single "LCOE within X%" bar would let a large error in one account hide under a small net percentage, or fail the whole comparison over an explained structural simplification. The itemized form makes every dollar of the gap accountable, which is exactly what the criterion-3 ruling asks for (explain the remainder; close errors). The signed-magnitude itemization *is* the pass artifact.

**A-5. Mapping-trap discipline — every trap asserted, not assumed.** [HARD] [INHERITED: research §C]

The 1costingFE→SysML mapping has 14 documented traps plus the `rb__*` vs `geom__*` separation (research §C, full table). The spec requires: **each trap in that table is asserted in the handshake** (as most already are in `handshake_1costingfe.py` / `emit_1cfe_point.py`), never left to a "the default handles it" assumption. New traps introduced by Items 3–4 (new accounts bring new field mappings) are **added to the table with an assertion** as part of that item's acceptance.

**Cautionary precedent:** the `f_shape` trap (research §C-g) — a "default is automatic" assumption was wrong and the first re-run **failed −20.6%** until `geom__f_shape := 1.0` was made an explicit injection. A silent mapping is a latent handshake failure.

**A-6. Version discipline — pin recorded, bump procedure defined.** [INHERITED: concept + research §G-6]

- **Recorded, every run:** the 1costingFE commit pin (currently `0254385`, hardcoded at `emit_1cfe_point.py:22`, asserted equal to the live repo HEAD at `handshake_1costingfe.py:115` — the run aborts on "commit drift"). Every handshake report records the commit it ran against. This half already exists in code; the spec makes the *recording* a requirement.
- **Pin-bump procedure** [AGENT-PROPOSED — owner ratifies] (research §G-6: currently undocumented). A bump is:
  1. **Who decides:** the owner. 1costingFE is an [OWNER] non-goal anchor, pinned deliberately; an agent does not advance the pin on its own.
  2. **What a bump triggers, before it is accepted:**
     - Re-run the full handshake against the new pin.
     - Re-assert every mapping trap (A-5) — an upstream change can move the injection map or a field's meaning.
     - Confirm every formula-reproduced account still passes the A-2 bar. **Any account that moves beyond the bar is a finding to investigate before the bump is accepted**, not an auto-rebaseline.
     - Re-baseline `handshake_comparison.json` as a deliberate committed step (see A-7).
     - Record in the handshake report: old→new commit, date, who approved, and a summary of what moved and why.

---

### Anchor B — ARIES-CS hold-out expectations (pre-committed, pre-reveal)

**B-0. Expectations are band widths, committed before reveal.** [HARD] [INHERITED: research §G-1, concept criterion 4]

The model's output at the ARIES-CS design point does not exist yet (it is Item 7, post-reveal), and the reference is sealed (PROTOCOL, `status: sealed`). So every Anchor-B expectation is a **band width set now**, from model-side evidence only — never a point target, never tightened after seeing the reference. A miss beyond a band **fails the anchor and is reported as a demo finding**, not narrated away (concept criterion 4; [OWNER-VERBATIM] "But this is a risk.").

**B-1. Basis discipline — the prior-leak bar.** [HARD] [INHERITED: research §E–F, PROTOCOL §3]

Every band's written rationale draws **only** from: (a) model-side evidence — how far our own headline moved under corrections (research §E); (b) the concept's axes; (c) general estimating-accuracy knowledge that is not ARIES-CS-specific (research §F). **No reasoning of the form "ARIES-CS is probably around X" is admissible** — not in this spec, and not in Item 7's comparison argument. This bar binds how Item 7 writes its verdict, not just how this spec sets the bands: a pass/fail may cite the band and the observed model value, never a smuggled expectation about the reference.

**B-2. Structural similarity — qualitative checklist (pass = all items present).** [AGENT-PROPOSED — owner ratifies]

Structural similarity is qualitative, not a number. It passes when the model, evaluated at the ARIES-CS point, exhibits all of:

- [ ] **Subsystem decomposition correspondence** — the model's major subsystems (plasma/physics, magnets, blanket/shield, vessel, heating, power conversion, BOP, buildings) map onto recognizable ARIES-CS subsystems, with no whole subsystem the model omits that ARIES-CS treats as first-order.
- [ ] **Radial-build ordering** — the model's radial build orders the same layers in the same sequence (plasma → SOL → first wall → blanket → shield → vessel → coil bore), even where thicknesses differ.
- [ ] **Cost-account coverage** — the model's CAS-account tree covers the standard CAS20 reactor plant (its 22x subsystems) plus CAS10/40/50/60/70/80, so that whatever ARIES-CS reports can be matched account-to-account, not apples-to-oranges.

A missing correspondence is recorded as a structural finding with its reason; the axis fails if a first-order correspondence is absent.

**B-3. Derived quantities — same order of magnitude.** [AGENT-PROPOSED — owner ratifies]

- **Applies to:** the model's derived quantities at the ARIES-CS geometry — radial-build consequences (build thicknesses/dimensions), coil mass, power flows (p_th, p_net, recirculating power, etc.).
- **Pass band:** the ratio **model / reference ∈ [1/3, 3]** (equivalently |log10(model/reference)| ≤ 0.5) — plainly, "same order of magnitude." This is the one operational test; Item 7 reports the ratio, not a signed percentage (convention pinned in B-8).
- **Basis:** our own headline moved ±25–30% and p_net re-staled across 575→786→578→804→915 MW under legitimate modeling corrections *before any ARIES-CS contact* (research §E) — direct evidence that even our own derived quantities are stable only to tens of percent under corrections. A blind evaluation at a geometry the model never saw cannot honestly be held tighter than a factor of ~3.
- **Expectation nuance (recorded, not a tighter pass gate):** geometry-direct quantities (radial-build dimensions, coil mass — computed straight from geometry and current density) are *expected* to land inside a factor of 2. This is a stronger-signal note for Item 7's report, not a separate pass bar; the pass bar for all derived quantities is same-order-of-magnitude.

**B-4. Rough per-component costs — factor-of-2, asymmetric high (AACE Class 5).** [AGENT-PROPOSED — owner ratifies]

- **Applies to:** rough per-component cost agreement versus ARIES-CS's published component costs.
- **Pass band:** **−50% to +100%** (a factor of ~2, asymmetric high) — the ratio **model / reference ∈ [0.5, 2.0]** (convention pinned in B-8) — i.e. AACE Class 5 concept-screening accuracy. This band is reciprocal (0.5 and 2.0 invert to each other), so the pass/fail verdict is the same whichever way the ratio is taken; the convention fixes only the reported sign and any future non-reciprocal adjustment.
- **Basis:** the stellarator model is a conceptual-stage estimate (AACE Class 5, optimistically Class 4). AACE Class 5 accuracy is −30%/−50% low to +30%/+100% high at 80% confidence (research §F, arXiv 2602.19389 Table 3, confirmed admissible). Combined with our own ±25–30% headline swings and the magnet cost/share jump ($4.39B/43.5% → $6.32B/50%) on a single field errata (research §E), a factor-of-2 asymmetric-high band is the defensible pre-committed expectation. Tighter would claim an accuracy a concept-stage estimate does not have.

**B-5. C220107 exclusion — mandatory.** [HARD] [INHERITED: research §G-2, PROTOCOL §3]

C220107 power_supplies is **excluded or footnoted in Anchor B.** It is the one known ARIES-CS-derived 1cfe value; leaving it in the blind would make the comparison self-referential. It **stays included in Anchor A** (the handshake is not the blind). This is forced, not a proposal.

**B-5a. Sizing-axis reallocation — owner confirmation pending.** [INHERITED: concept criterion 4 note — reallocation pending owner confirmation] [AGENT-PROPOSED — owner ratifies]

The concept marks the "optimized sizing" axis's move out of criterion 4 as **[SURFACED to owner] — this reallocation needs owner confirmation**. The proposal: "optimized sizing" cannot be tested at a fixed design point (sizing is an input there), so it is excluded from criterion 4 and covered only by the stretch (criterion 8 / Item 9). **Confirmed [OWNER] 2026-07-19** — this spec writes no criterion-4 sizing expectation; the axis lives in Item 9's scope.

**B-6. Pass/fail semantics and the comparison report.** [AGENT-PROPOSED — owner ratifies]

Item 7's comparison report records, **per axis**: the pre-committed band (from B-2/B-3/B-4), the observed model value, a verdict (pass / fail), and an explanation drawn only from admissible bases (B-1). A miss beyond a band is a **demo finding**, reported honestly — the honesty is the credibility (concept, risk table). Criterion 4's verdict is the conjunction: it passes when structural similarity passes and the derived-quantity and cost axes are within band (excluding C220107 and the sizing axis).

**B-7. AACE provenance cross-check.** [AGENT-PROPOSED — owner ratifies] [INHERITED: research §F caveat]

The AACE Class-5 table (B-4's basis) is an in-repo *dossier extraction* (pandoc from arXiv HTML at `knowledge/concept_research/01-hts-compact-tokamak/iter-04/sources/arxiv-2602-19389/output.md:1318-1328`), not a `SOURCE_INDEX.md`-registered primary source. Because it is load-bearing, **Item 7 (or an earlier convenient moment) cross-checks the extracted table against the raw arXiv PDF** and cites **AACE 18R-97** as the standard, with this file recorded as where it is written down in-repo.

**B-8. Ratio convention.** [AGENT-PROPOSED — owner ratifies]

Every Anchor-B band (B-3, B-4) is on the ratio **model / reference**, matching the handshake's `rel_dev` sense (model over reference). Item 7 reports the **ratio**, not a signed percentage. The −50%/+100% cost band (B-4) is reciprocal so the verdict is convention-independent at its endpoints; fixing the convention still matters because Item 7 must print a consistent sign, and any owner adjustment to a **non-reciprocal** band (e.g. −30%/+100% → [0.7, 2.0]) breaks the invariance and would otherwise be ambiguous.

---

## Non-Goals

- **Running either comparison.** This spec writes bars only; the handshake account-scope work is Items 3–4, the hold-out comparison is Item 7.
- **Item 2's constraint-execution acceptance.** The Anchor-A handshake and the constraint-verdict machinery are separate; this spec does not assume verdicts exist in the run report (research §G-7).
- **Anything about criterion 8 beyond the sizing-axis exclusion note (B-5).**
- **Changes to 1costingFE.** [OWNER] non-goal — gaps found there are filed, not fixed.

## Open Questions / Deferred

- **The G-8 premise conflict — surfaced, ruled by the owner 2026-07-19 (below): amended as proposed, in force.**
- The exact accounts Items 3–4 can bring fully under the A-2 bar vs. must itemize as remainder is not knowable until those items run — the boundary in A-3 is the target, and each item records its actual result against A-4.

### The G-8 premise conflict — [OWNER ruled 2026-07-19: amended as proposed, in force]

**The conflict** (research §G-8). A standing [OWNER] rule (the WI-024 successor bar, `work/orchestration/stale-basis-recompute.md:24`) says the handshake may be edited **only within `set_1cfe_inputs`'s injection map**, and `git diff exploration/stellarator_e2e/handshake_comparison.json` must be **empty** after a run. Items 3–4 add real modeled accounts — they **replace injected values with computed ones**, which **moves the comparison JSON** and **shrinks the injection map** by construction. Both clauses of the standing bar are violated by design. This is a premise conflict between a standing owner rule and this spec's own acceptance; per `capture-fidelity` §4 it is **surfaced, not resolved**.

**Proposed amendment** (marked pending — the owner amends the successor bar, an agent does not):
- The bar **as written continues to govern refinement items** (the WI-019–025 kind) that must *not* move the handshake — there, a moved comparison JSON signals a regression and the empty-diff check stays the guardrail.
- For **account-scope items** (3, 4, and any future account-adding item), the bar is **superseded by this spec's acceptance (A-3, A-4)**: comparison JSON moves are **expected** and re-baselined per item as a deliberate committed step; injection-map shrinkage is **documented** (each newly-modeled account named as it leaves the injection map); the item still may **not touch comparison *logic*** (the comparison machinery is fixed — only what feeds it changes).
- Each account-scope item records: which accounts moved injected→computed, the signed magnitude of each move, and the re-baseline as an explicit commit (never a silent diff).

**Ruled [OWNER] 2026-07-19: amended as proposed.** The amendment is in force and is recorded at the bar's home (`work/orchestration/stale-basis-recompute.md`, the ruling-3 bullet). Items 3–4 are unblocked.

---

## Ratification package — [OWNER: ratify or adjust each line]

Success criterion "owner sign-off on both specs" is met by marking this list. **Marked [OWNER] 2026-07-19: "ratify all, G-8 amend as proposed" — every line below is in force.**

**Anchor A**

| # | Proposal | Basis (one line) | Owner |
|---|---|---|---|
| A-2 | Per-account handshake pass bar: **\|relative deviation\| ≤ 1e-6** | ~10× above the ~1e-7 float32 floor, ~10⁴× below percent-scale real errors (research §B, §E) | ☑ **ratified 2026-07-19** |
| A-4 | End-state LCOE acceptance = **all modeled accounts under A-2 + remainder itemized with signed magnitudes** (no blanket LCOE %) | makes every dollar of the −31% gap accountable per the criterion-3 ruling | ☑ **ratified 2026-07-19** |
| A-6 | **Pin-bump procedure**: owner decides; a bump re-runs the handshake, re-asserts traps, re-checks every account against A-2, re-baselines JSON, records old→new commit | research §G-6, currently undocumented | ☑ **ratified 2026-07-19** |

*(All [HARD] and [INHERITED] items — A-1 (pipeline-vs-oracle rel 1e-9 + the ~1e-7 float32 floor), A-3 (the [OWNER] criterion-3 ruling), A-5 (mapping-trap discipline), B-0, B-1, and the B-5 C220107 exclusion — are excluded from this table: their authority is physics, an interface, or an existing owner ruling, not a fresh proposal. The table carries only the [AGENT-PROPOSED] items. They are listed here for visibility, no ratification needed.)*

**Anchor B**

| # | Proposal | Basis (one line) | Owner |
|---|---|---|---|
| B-2 | Structural similarity: **qualitative checklist, pass = all three correspondences present** (subsystem decomposition, radial-build ordering, cost-account coverage) | concept criterion 4 axes | ☑ **ratified 2026-07-19** |
| B-3 | Derived quantities: **model/reference ratio ∈ [1/3, 3]** ("same order of magnitude"); geometry-direct quantities *expected* inside 2× as a note | our own headline moved ±25–30%, p_net re-staled 575→915 MW (research §E) | ☑ **ratified 2026-07-19** |
| B-4 | Rough per-component costs: **model/reference ratio ∈ [0.5, 2.0]** (−50%/+100%, factor-of-2 asymmetric high) | AACE Class 5 concept-stage accuracy (research §F) | ☑ **ratified 2026-07-19** |
| B-5a | **Sizing-axis reallocation**: confirm criterion-4 sizing exclusion → covered only by criterion 8 / Item 9 (concept marks this [SURFACED to owner], unconfirmed) | sizing is an input at a fixed design point; concept criterion 4 note | ☑ **confirmed 2026-07-19** |
| B-6 | Report records **per axis**: band, observed value, verdict, admissible-only explanation; a miss is a demo finding | concept criterion 4 honesty bar | ☑ **ratified 2026-07-19** |
| B-7 | **AACE cross-check**: Item 7 verifies the extracted Class-5 table against the raw arXiv PDF; cites AACE 18R-97 | table is a dossier extraction, not a registered primary source (research §F caveat) | ☑ **ratified 2026-07-19** |
| B-8 | **Ratio convention**: bands are on model/reference; Item 7 reports the ratio; convention fixes reported sign and any non-reciprocal adjustment | matches the handshake `rel_dev` sense | ☑ **ratified 2026-07-19** |

**Standing-rule amendment**

| # | Proposal | Owner |
|---|---|---|
| G-8 | Amend the WI-024 successor bar: empty-diff/injection-map-only governs **refinement** items; **account-scope** items (3, 4) may move the comparison JSON and shrink the injection map, re-baselined and documented per item, comparison *logic* untouched. | ☑ **amended as proposed 2026-07-19** — recorded at the bar's home (`work/orchestration/stale-basis-recompute.md`) |

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_stellarator_mbse_demo.md` (Item 1)
- **Governing concept:** `.project/concepts/stellarator-mbse-demo.md` (criteria 3, 4, 8)
- **Required Reading:** `knowledge/holdout/aries-cs/PROTOCOL.md` (§3 barred paths — honored, none read)
- **Research (evidence base):** `.project/research/20260718-205525_anchor-acceptance-evidence-stellarator-demo.md`

---

**Next Steps:** Done — reviewed (spec-review.md, all must-fixes applied) and ratified [OWNER] 2026-07-19. Items 3, 4, and 7 are judged against these bars; Items 3–4 are unblocked by the G-8 amendment.
