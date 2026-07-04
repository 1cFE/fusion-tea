---
Status: draft
Priority: P0
Goal: null
Created: 2026-07-04
Updated: 2026-07-04
---

# Epic: Pipeline De-Risk & Demonstration

## Executive Summary

Close the pipeline's riskiest open loop — SysML → codegen → executable Python → constraint-checked sweep has **never run end-to-end on any model** — and produce the documentation that shows what the program has actually demonstrated. Two-week timebox. Every item ships a written record as a first-class deliverable, feeding a hypothesis-evidence dossier that maps each of the four program hypotheses (H1 agentic modeling, H2 agentic research loop, H3 SysML methodology, H4 executable exploration) to concrete evidence.

This epic runs on **existing assets** (the validated IFE models, the catf_mfe/solar_battery codegen fixtures, the ingested source corpus). It does not touch the MFE epic's scope; it de-risks WI-010 and WI-012 so they land on proven ground.

## Context

**Motivating analysis**: `.project/research/20260704-120000_pipeline-hypothesis-meta-review.md`. Key findings this epic answers:

- **R1 (top risk)**: no generated pipeline has ever been executed. `sysml-codegen` generation is proven (baselines for solar_battery, chain_spike, catf_mfe), and expression translation exists, but the assembled path — generate → AI implementation pass fills calc bodies → teax executor → numbers — has never been closed. Constraint predicate emission is an open TODO (codegen Phase 6). WI-012 currently carries all of this risk at the end of a sequential epic.
- **R2**: the two SysML constructs that join structure to behavior (usage-level calc chaining `in x = calc.ret`, part-level `assert constraint`) are exercised nowhere in the corpus; WI-009's design defers them to WI-010.
- **R3**: H2 — agents deriving models from first-class research — is not tested by any scheduled work. The MFE epic sources its formulas from 1costingfe (transcription, not derivation). The one existing H2 data point (Hawker paper → IFE model, WI-006–008) is uncaptured.
- **R5**: the correctness oracle for generated code is weak (single-point "credible range" checks).

**Correction to the meta-review**, from the user: the codegen step includes an **AI pass** — calc bodies and functions outside the mechanical translation envelope (e.g. `exp()`) get written into Python by an agent, not left as stubs. So the wrapper-delegates-to-handwritten structure is the design, not a gap. What remains unproven is the *assembled* loop with that AI pass included — which is exactly what Items 1 and 3 close.

**What exists to build on**:
- IFE models, validated: `models/library/` + `models/designs/generic_ife/` + `models/designs/hif_ife/`, with a known-good anchor — SV-008, HIF realistic design point → LCOE 8.69 $/MWh — and a viability constraint pattern (DI-001, ηG > 10, `fusion_cycle.sysml`).
- Codegen fixtures with captured generation baselines: `~/1cfe/sysml-codegen/tests/fixtures/` (solar_battery, chain_spike, catf_mfe — 42 fusion calc defs).
- teax executor proven on the battery demo (`~/1cfe/teax/packages/battery-tea-demo/`).
- 13 ingested sources + 39 concept dossiers (`knowledge/SOURCE_INDEX.md`, `knowledge/concept_research/`).

**Relationship to the MFE epic (WI-009–012)**: WI-009 continues unchanged — its library work is needed on every branch. This epic pulls WI-012's integration risk forward onto IFE (which exists today) and validates the constructs WI-010's architecture assumes. When WI-012 arrives, it should be a *repeat* of a proven loop on new models, not a first attempt.

## Authority Source Dependencies

| Source | Use For | Items | Status |
|--------|---------|-------|--------|
| Hawker 2020 (`knowledge/sources/a_simplified_economic_model_for_inertial_fusion/`) | IFE LCOE anchor values, H2 retroactive capture | 3, 4 | Ingested |
| IFE epic artifacts (WI-006/007/008, `work/completed/`) | Derivation chain record, SV-008 anchor | 3, 4 | In repo |
| `sysml-codegen` fixtures + baselines | Execution spike ground truth | 1 | Available (external repo, editable dep) |
| teax battery demo | Executor reference pattern | 1, 3 | Available (external repo) |
| Concept research corpus (`knowledge/concept_research/`, 39 dossiers) + ingested sources (`knowledge/sources/`) | Blind physics derivation — the full corpus is the input, not one pre-selected source | 4 | In repo |
| 1costingfe (`~/1cfe/1costingfe`) | **Comparison step only** — held-out answer key, firewalled from derivation | 4 | Available (external repo) |

**Constraint-emission dependency (external)**: codegen Phase 6 (constraint predicate generation) is in flight in `sysml-codegen`. Items 1 and 3 must not block on it — if predicates aren't emitted by execution time, the sweep evaluates constraints harness-side from the extracted constraint expressions, and the gap is filed as a codegen finding. Either way the finding is a deliverable.

## Success Criteria

- [ ] A generated pipeline (codegen + AI implementation pass) executes end-to-end through the teax executor and produces asserted numeric output — first time ever (Item 1)
- [ ] Calc-chaining and part-level `assert constraint` validated through syside **and** codegen extraction, with the working idiom recorded for WI-010 (Item 2)
- [ ] The IFE/HIF model runs SysML → Python → sweep → viability map: generated LCOE reproduces the verified anchors ($252.30/MWh at Hawker defaults, $68.69/MWh at the realistic HIF point, per `scripts/verify_ife_lcoe.py` — the widely-quoted "8.69" was a digit corruption, see WI-016 retro capture) within a stated tolerance, and a parameter sweep partitions the input grid by the ηG > 10 constraint with the feasible region visualized (Item 3)
- [ ] H2 has written evidence: the tokamak physics/costing chain derived blind from the research corpus (firewalled from 1costingfe), compared against 1costingfe at real design points with every divergence adjudicated, and the agent research loop instrumented; plus the Hawker→IFE derivation captured retroactively (Item 4)
- [ ] A hypothesis-evidence dossier maps H1–H4 → items → evidence → honest status, and a public-facing explainer section shows the closed loop (Item 5)
- [ ] Every item ships its findings/process document — documentation is a deliverable, not a byproduct
- [ ] All gaps discovered in `sysml-codegen`/`teax` filed as findings in those repos, not worked around silently
- [ ] Completed within the 2-week timebox (by 2026-07-18)

## Items

### Item 1: Pipeline Execution Spike

**Scale**: standard
**Dependencies**: none — start day 1

**Scope**: Close the never-executed gap on the cheapest possible model. Take a fixture with captured generation baselines (solar_battery first; catf_mfe if time allows, as the fusion-shaped stress case) through the full assembled path: `sysml-codegen` generate → AI implementation pass fills the module bodies → teax `execute_pipeline()` → numeric outputs asserted against hand-computed expectations. This is deliberately *not* on fusion-tea's models — the point is to debug the plumbing where generation is already known-good, so Item 3 debugs only what's new.

**Key requirements**:
- [ ] At least one generated pipeline executes end-to-end under the teax executor with asserted numeric output
- [ ] The AI implementation pass is exercised and its outputs checked against the SysML expressions (spot-check translation fidelity)
- [ ] Constraint-predicate status established: emitted and evaluable, or gap confirmed and filed (Phase 6 finding)
- [ ] Findings document: every gap, workaround, and friction point, filed to the owning repo (`sysml-codegen` or `teax`)

**Deliverables**: executed pipeline artifacts (in `sysml-codegen` or `exploration/`), findings document (`work/learnings/` + issues filed in the owning repos)

---

### Item 2: SysML Wiring Construct Validation

**Scale**: standard (small — bounded to ~1 day)
**Dependencies**: none — parallel with Item 1

**Scope**: The two constructs the whole plant idiom depends on, exercised nowhere in the corpus: usage-level calc chaining (`in x = calc.ret`) and part-level `assert constraint`. Build a minimal toy model using both; validate with syside/`sysmlv2-validator`; run it through codegen extraction to confirm the constructs survive into the graph. Record the working syntax as the reference idiom for WI-010 (and register an AD if the answer forces an architectural choice).

**Key requirements**:
- [ ] Toy model with a two-calc chain and an asserted constraint parses clean (Level 1) and evaluates correctly under syside
- [ ] Codegen extraction handles both constructs, or the gap is characterized precisely and filed
- [ ] The working idiom written up as a learning record WI-010 can copy verbatim

**Deliverables**: toy `.sysml` (under `exploration/` or codegen fixtures), learning record in `work/learnings/`, AD if warranted

---

### Item 3: IFE End-to-End Demonstration — Codegen, Sweep, Viability Map

**Scale**: standard
**Dependencies**: Item 1 (plumbing proven); Item 2 informs but does not block

**Scope**: The demonstration centerpiece. Run the validated IFE/HIF models through the full pipeline: codegen + AI implementation pass over `ife_lcoe.sysml`, `fusion_cycle.sysml`, and the HIF plant bindings → executable Python → (a) **anchor check**: generated pipeline reproduces SV-008's 8.69 $/MWh at the Hawker realistic design point within a stated tolerance — this is the correctness oracle the pipeline has lacked; (b) **viability sweep**: grid over Hawker parameters (candidate axes: rep rate, driver efficiency, target gain, availability — pinned at spec), each point classified against the ηG > 10 constraint (DI-001) and an LCOE threshold, feasible region visualized. This delivers everything WI-012 promises, one epic early, on models that already exist — so WI-012 becomes a repeat on MFE, not a first attempt.

**Key requirements**:
- [ ] Generated IFE pipeline executes; LCOE at the SV-008 design point matches 8.69 $/MWh within tolerance (tolerance stated and justified in the spec)
- [ ] Sweep harness varies ≥3 physical/economic axes over a grid; every point classified viable/non-viable via the ηG constraint (harness-side evaluation acceptable if Phase 6 predicates aren't ready — documented)
- [ ] Feasible region and the viability knee visualized; artifacts committed
- [ ] Deviations between generated-code results and the SysML-model values investigated and explained, not tolerated silently
- [ ] Demonstration write-up: what ran, what the map shows, what broke along the way

**Deliverables**: `generated/ife/` (codegen output), sweep script + visualization under `exploration/` or `data/`, demonstration write-up, new SV entry for the anchor check

---

### Item 4: H2 Probe — Blind Physics Derivation + 1costingfe Differential

**Scale**: standard
**Dependencies**: none — parallel track throughout

**Scope**: The direct test of H2, designed so 1costingfe is the **held-out answer key**, not the formula source. Agents derive the core MFE physics/costing relations from the research corpus alone — the 39 concept dossiers (`knowledge/concept_research/`), the ingested sources (`knowledge/sources/`), and pretraining — with a **contamination firewall**: the deriving agents may not read 1costingfe, the WI-009 design doc, or the meta-review (all three quote 1costingfe formulas). Then a separate comparison step evaluates the derived models against 1costingfe at real design points and diagnoses every divergence.

**Minimum derivation set** (tokamak chain — richest source coverage, richest comparison target):
1. Fusion power from machine parameters (R, a, κ, B, plus whatever closure the sources support)
2. Power balance → net electric, engineering Q, recirculating fraction
3. Magnet/coil cost scaling from geometry and field

**Stretch**: the stellarator variant of the coil relation.

**Comparison protocol**: evaluate both the derived relations and 1costingfe at the concept 01 (ARC-class tokamak) and 20a (Type One stellarator) design points, plus a small grid around them. Convergence is evidence the loop works; divergence is a *finding to adjudicate against sources*, not an automatic failure — the derived model may have chosen a different-but-defensible relation, or exposed a 1costingfe limitation (the structure-dominated magnet undercount is a known candidate). Nuance to hold onto: 1costingfe is a sanity check, not ground truth.

**Contamination note for spec**: the dossiers' `model_setup.py` files reference 1costingfe spec keys and contain 1costingfe-computed values. Protocol distinction to pin at spec time: dossier *source citations and source-quoted values* are usable inputs to derivation; 1costingfe-*computed* numbers are excluded from derivation and reserved for the comparison step.

**Also in this item (small)**: retroactive capture of the one derivation that already happened — Hawker paper → 14 parameters → IFE calc defs → SV-008 — as an H2 process record with pointers into the WI-006–008 artifacts.

**Key requirements**:
- [ ] Firewall protocol defined at spec time and observed — derivation context excludes 1costingfe code, WI-009 design.md, and the meta-review; exclusion list recorded in the process record
- [ ] The three tokamak-chain relations derived as cited calc defs (Levels 1–3 pass, MR-4 citations, reasonableness SV entries); every relation traces to dossier/source material or an explicit pretraining-knowledge declaration
- [ ] Comparison report: derived vs 1costingfe at concept 01 and 20a design points + small grid; every divergence diagnosed (different relation? different constant? error on which side?) and adjudicated against sources
- [ ] Instrumented process record: what agents searched, what they found, dead ends, human interventions — honest about where the loop needed steering
- [ ] Hawker→IFE retroactive capture written

**Deliverables**: derived calc defs in `models/library/` (or `exploration/` if they don't meet library quality — the spec decides the bar), comparison report + H2 process records (`.project/research/` or `work/learnings/`), SV entries

---

### Item 5: Demonstration Dossier & Explainer

**Scale**: standard
**Dependencies**: Items 1–4 (rolling — seeded day 1, finalized last)

**Scope**: The documentation capstone. **(a) Hypothesis-evidence dossier**: one document mapping H1–H4 → the work that tests each → the evidence produced → an honest status (validated / partially / untested), including the explicit statement of what the MFE epic does and does not validate (the relabel recommended by the meta-review). Seeded at epic start, updated as items land. **(b) Explainer section**: extend the public workflow explainer (`docs/demo/index.html`, per the `html-explainer` skill) with the closed loop — model → codegen → executable → viability map — using the Item 3 artifacts. This is the material the next blog post ("how we go from formal system models to cost estimates") draws from. **(c) Backlog seeds**: one-page framings for the two unowned vision claims (uncertainty propagation, inverse solving) so they become schedulable epics rather than unbacked public claims.

**Key requirements**:
- [ ] Dossier covers all four hypotheses with evidence pointers and honest status; MFE-epic relabel paragraph included
- [ ] Explainer section renders the IFE demonstration (verified with the `browser-inspect` skill)
- [ ] Uncertainty and inverse-solve framings written and added to the backlog as draft epics/items
- [ ] Everything committed; no results living only in chat history

**Deliverables**: hypothesis-evidence dossier (`modeling_project/` or `.project/`), explainer section in `docs/demo/`, two one-page epic framings in `work/backlog/`

---

## Sequencing

```
Day 1        Day 3        Day 5        Day 8        Day 10
│ Item 1 ━━━━━━━┓
│ Item 2 ━━┛    ┃ (idiom → WI-010)
│               ┗━▶ Item 3 ━━━━━━━━━━━━━┓
│ Item 4 ━━━━━━━━━━━━━━━━━━━━━━━━┛      ┃
│ Item 5 (dossier seeded) ┄┄┄┄┄┄┄┄┄┄┄┄━━┻━━ finalize
```

- **Items 1, 2, 4 start in parallel on day 1.** Item 2 is ~1 day; Item 1 targets ~2–3 days; Item 4 targets ~3–4 days (derivation ~2–3, comparison ~1).
- **Item 3 starts when Item 1's plumbing is proven** (~day 3–4); it shares the critical path with Item 4.
- **Item 4 runs as an independent parallel track** — it shares no code path with 1–3. Its derivation phase should run *before* much MFE-epic implementation lands, to keep the firewall easy to maintain.
- **Item 5 is rolling**: dossier skeleton on day 1, each item feeds it on completion, finalized days 9–10.
- Critical paths: Item 1 → Item 3 → Item 5, and Item 4 → Item 5. Buffer: ~1–2 days, held for Items 3 and 4 (highest unknown-count).
- **Timebox rule**: if day 7 arrives and Item 3's anchor check hasn't passed, cut the sweep to 2 axes and a coarse grid — a small honest map beats a large late one. Item 4's cut line is the stretch (stellarator variant) first, then grid breadth on the comparison (design points only); the derivation minimum set and the comparison itself are not cuttable — they are the H2 test.

## Out of Scope

- **Generated-code parity harness vs 1costingfe** — Item 4 compares *derived model relations* to 1costingfe; the separate check that *codegen-generated Python* reproduces 1costingfe over the WI-012 sweep grid needs MFE generated code and stays in WI-012, where it should be added as a requirement (the meta-review's R4/R5 fix)
- **The two-track end-state decision** (SysML vs 1costingfe relationship) — a user decision, prompted by the dossier, not an engineering item
- **Codegen Phase 6 completion** — owned by `sysml-codegen`; this epic consumes it if ready, files findings if not
- **Uncertainty propagation / inverse solving implementation** — Item 5 seeds the framings only
- **Any MFE model authoring** — WI-009–011 continue in their own epic

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| The assembled execution path fails in a deep way (executor/registry/schema mismatch between codegen output and teax) | Medium | High | That discovery is the epic's purpose — surfacing it on day 2 on solar_battery instead of at WI-012 on MFE. Item 1's findings doc is a success outcome even if execution doesn't close; timebox the debugging, escalate to a codegen/teax fix decision |
| AI implementation pass introduces silent translation errors (body ≠ SysML expression) | Medium | High | Item 3's SV-008 anchor is the oracle; Item 1 spot-checks bodies against expressions; any mismatch investigated, not tolerated |
| IFE models use constructs codegen extraction hasn't seen (they were authored pre-codegen, unlike catf_mfe) | Medium | Medium | Item 1 proves the path on known-good fixtures first, isolating Item 3 failures to IFE-specific constructs; gaps filed as findings |
| Constraint predicates (Phase 6) not ready in time | High | Low | Planned for: harness-side constraint evaluation from extracted expressions; documented gap, not a blocker |
| Item 4 firewall leaks — 1costingfe formulas reach the deriving agents (they're quoted in WI-009 design.md, the meta-review, and referenced in dossier `model_setup.py` files) | Medium | High | Exclusion list pinned at spec time and recorded; derivation runs in fresh agent contexts fed only whitelisted paths; comparison done by a separate agent/step. A leak invalidates the H2 claim, not the models — disclose it if it happens |
| Item 4 corpus too thin for a defensible relation (e.g. no source gives a coil-cost scaling) | Low | Medium | That finding is itself H2 evidence — the loop must detect data insufficiency rather than confabulate; write it up, and note pretraining-derived relations explicitly as such |
| Derived models diverge from 1costingfe and adjudication is ambiguous (both defensible) | Medium | Low | Expected and valuable — record both relations with their bases; divergences feed the MFE epic's sourcing decisions rather than blocking this item |
| Two weeks is tight for 5 items | Medium | Medium | Cut lines pre-declared (sweep breadth, then Item 4 probe); Items 1/2/4 genuinely parallel; Item 5 rolling so documentation never bunches at the end |

---

**Last Updated**: 2026-07-04
**Next Action**: register items in BACKLOG.md, then `/spec-model` on Item 1 (Pipeline Execution Spike)
