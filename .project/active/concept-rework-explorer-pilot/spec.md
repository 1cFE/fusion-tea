# Spec: Explorer Adapter + Pilot Regeneration (Concept-Analysis Rework, Item 10)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-31
**Complexity:** MEDIUM
**Branch:** `concept-analysis-rework`
**Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 10

---

## Work Item Summary

Adapt `concept_explorer` to the new pipeline contract — read `Confinement-Family:` (and the other orchestrator-owned fields) from frontmatter, drop the `result_1gw → result` fallback path, and verify the two-knob fractional-`n_mod` mechanism end-to-end — then regenerate a small **pilot** of 3–5 concepts spanning the **fit_grade × grounding_confidence** grid so the new contract is validated under realistic concept variety before bulk regeneration (Item 11). Issues found by the pilot are folded back into Items 7–9 (helpers / validators / templates / critic) before the bulk roll-out is unlocked.

## Why This Matters Now

Items 4, 6, 7, 8 have landed; Item 9 (`model_critic`) artifacts exist alongside concept 01. Item 8's Phase-5 ARC pilot already exercised the *prompt* contract on one High-fit / high-grounding concept and passed. What Item 10 still has to clear before bulk regen is everything that *only shows up at variety*:

- the **explorer** has not been adapted yet — it still reads `Confinement Family` from body prose (regex on the body, line 89) and still silently falls back from `result_1gw` to `result` (line 261–262), so under the new contract a missing `result_1gw` would quietly degrade the comparison view instead of failing loudly
- the **`grounding_confidence` asterisk** path in the comparison view is new (folded into Item 5's surprise finding) and has never been exercised on a real low-grounding row
- the **Med / Low fit-grade** branches of the orchestrator (Item 6's four-state routing) have only been run on dry-runs — never end-to-end through analyze → model_setup → critic against a real Med- or Low-fit dossier
- the **two-knob fractional `n_mod`** call (Item 4's `_scale_overrides` fix; Item 7's `run_native_and_1gw` helper) has been unit-tested but has only one real-pipeline cross-check (ARC, `P_native = 233`, `n_mod = 4.29`); a pilot row with a very different `P_native` (e.g. Helion Orion ~50 MWe → `n_mod = 20`) is the first non-trivial fractional check at scale

This is the last opportunity to catch contract-level bugs cheaply. Bulk regen (Item 11) amplifies any defect by ~25×.

## Key Bets / Constraints

- **Bet:** Three to five concepts spanning the two-axes grid surface most cross-concept failure modes; the marginal value of a sixth pilot row is low relative to the cost of an extra regen + critic pass.
- **Bet:** The pilot's job is *finding* problems, not certifying success. A "clean" pilot that surfaces zero fold-backs is a weak signal, not a strong one — the report's first-class output is the issue list, not a green checkmark.
- **Constraint:** The explorer reads against the three-forward module-level contract (`model`, `generic`, `native`, `result_1gw`); Item 10's change is to *stop tolerating* a missing `result_1gw` and drop the `result_1gw → result` fallback, not to redefine the surface. (`result` is removed by the three-forward contract item; the explorer's primary number is still `result_1gw`.)
- **Constraint:** `Confinement-Family:` (and the other Item 6 frontmatter fields: `Archetype`, `Archetype-Fit`, `Comparison-Status`, `Design-Point-*`, `Grounding-Confidence`) are read from frontmatter only — never from body prose. The body-prose regex (`extract_explorer_data.py:89, 287, 579`) is removed.
- **Constraint:** Human-authored content under each pilot concept's directory (notably `review.md`, plus any other artifact known to carry hand-written content) is **snapshotted before regeneration** and not overwritten. The snapshot procedure documented here is what Item 11 will follow mechanically.
- **Constraint:** Asterisking of `grounding_confidence: low` rows reuses the existing asterisk pattern already used for `fit_grade=None` / archetype-bespoke concepts in the comparison view — it is not a new visual idiom.
- **Constraint:** Item 12 (native-scale projection) is **out of scope**. The pilot validates the *replication-floor* `result_1gw` only; the asterisked low-grounding rows are still presented as `result_1gw @ 1000 MWe`, not as a range.
- **Non-goal:** Bulk regeneration. That is Item 11, gated on this pilot's fold-backs landing.
- **Non-goal:** Regenerating freeform concepts — both `fit_grade=None` (no enum analog) and the `fit_grade != None`-but-no-`P_native` route. Both stay asterisked in the explorer and are not touched here.
- **Non-goal:** Reworking the comparison-view visual design beyond the asterisk reuse.

---

## Business Goals

### Why This Matters

Item 10 is the last gate where contract defects can be caught cheaply. Once Item 11 fans out across ~25 concepts, any prompt-level, validator-level, or explorer-level bug discovered downstream costs a full re-regen to fix. The whole "apples-to-apples cross-concept comparison" framing rests on `result_1gw` being reached the same way for every concept and the explorer reading the same fields from the same place for every concept. The pilot proves that holds across the two-axes grid before we commit to it at scale.

### Success Criteria

- [ ] Explorer reads every pilot concept's `Confinement-Family`, `Archetype`, `Archetype-Fit`, `Comparison-Status`, and `Grounding-Confidence` from frontmatter; the body-prose `**Confinement Family**:` regex is gone.
- [ ] Explorer raises (does not silently fall back) when a concept the orchestrator routed to `costingfe` or `costingfe-asterisked` has no `result_1gw` at module level.
- [ ] Every pilot `result_1gw` was reached by `forward(net_electric_mw=1000, n_mod=1000/P_native, override_reference_mw=P_native, …)` — verified by inspecting `result_1gw.params["n_mod"]` and `result_1gw.params["net_electric_mw"]`.
- [ ] Pilot rows with `Grounding-Confidence: low` render with an asterisk in the comparison view that matches the existing `fit_grade=None` asterisk styling — the user can tell at a glance which numbers are well-grounded vs poorly-grounded.
- [ ] The pilot set spans the **fit_grade × grounding_confidence** grid: minimum one High-fit/high-grounding row (e.g. ARC, concept 01), one Low-fit/medium-grounding row (e.g. Helion Orion, 08-frc-w-direct-conversion), one Low-fit/low-grounding row (a concept with a published-but-pathological `P_native`); a Med-fit row included if a clean candidate is available without inflating the pilot beyond five rows.
- [ ] Human-authored artifacts (`review.md` and any other artifact identified during the snapshot scan) for each pilot concept are preserved verbatim through regeneration. The snapshot lives under this work-item directory and is auditable after the fact.
- [ ] `pilot_report.md` enumerates every issue surfaced by the pilot with: which artifact / surface raised it, severity (blocker / fold-back / nit), the fold-back fix (which item — 7 / 8 / 9 — owns it), and disposition (landed before bulk / deferred to Item 11 / accepted as residual). A pilot with zero fold-backs is flagged as a weak signal, not a green light.

### Priority

P0 within the epic — gates Item 11. Inside the epic's phase plan this is the pacing gate for Phase 2.

---

## Problem Statement

### Current State

- `extract_explorer_data.py` reads `Confinement Family` from `analysis.md` body prose (regex at line 89, called at 287 and 579). Under Item 6's contract, that field is orchestrator-owned in frontmatter.
- `extract_explorer_data.py:261–262` silently falls back from `result_1gw` to `result` when `result_1gw` is missing. Under the new contract, every `costingfe` / `costingfe-asterisked` concept **must** expose `result_1gw`; absence is a contract violation and should fail loudly.
- The two-knob fractional-`n_mod` mechanism has been unit-tested in 1costingFE and helper-tested in fusion-tea, but its end-to-end behaviour in the real pipeline is verified against only one concept (ARC, Item 8 Phase 5).
- `grounding_confidence` is a new field. The asterisk path that surfaces it in the comparison view has never been exercised on a real low-grounding row.
- Med- and Low-fit branches of the orchestrator's four-state routing have only been dry-run.

### Desired Outcome

The explorer adapts cleanly to the orchestrator-owned frontmatter contract and refuses to silently degrade. A 3–5-concept pilot spanning the fit × grounding grid runs end-to-end (regenerate → critic → explorer ingest → comparison view), and every surfaced issue is either landed back into Items 7–9 or explicitly accepted as residual in `pilot_report.md`. Item 11 unlocks only after the fold-backs land.

---

## Scope

### In Scope

- `exploration/concept_explorer/extract_explorer_data.py`: frontmatter reads (Confinement-Family and the other Item 6 fields the explorer consumes); removal of the `result_1gw → result` fallback; verification of fractional-`n_mod` params on `result_1gw`; the narrative-extraction prompt path called out in the epic for explorer ingest.
- Pilot regeneration of 3–5 concepts spanning the fit × grounding grid (concrete selection deferred to design).
- A documented snapshot procedure for human-authored content (`review.md` and any other artifact identified during the snapshot scan), executed for each pilot concept and stored under `.project/active/concept-rework-explorer-pilot/pre_pilot_snapshot/`.
- `pilot_report.md` enumerating issues, fold-backs, and dispositions.
- Asterisk styling reuse in the comparison view for `Grounding-Confidence: low` rows.

### Out of Scope

- Bulk regeneration (Item 11).
- Freeform concepts — both `fit_grade=None` and `fit_grade != None`-but-no-`P_native` (`design_point_freeform_routes.md`). Both stay asterisked and are not regenerated.
- Item 12 (native-scale `result_1gw_native` projection).
- Visual redesign of the comparison view beyond reusing the existing asterisk idiom.
- Modifying Item 4's library fix, Item 7's helper / validator APIs, or Item 8's prompt contracts. Item 10 *exercises* these; fixes triggered by pilot findings land back in their owning items.

### Edge Cases & Considerations

- A pilot concept whose `P_native` produces a *non-fractional* `n_mod` (e.g. `P_native = 500`, `n_mod = 2`) does not exercise the fractional-scaling path; the pilot composition must include at least one row where `n_mod` is meaningfully fractional.
- A low-grounding row's costingfe answer may be confidently nonsense; the asterisk is what carries that honesty. The pilot must show this concretely (visual artifact in `pilot_report.md`) rather than asserting it abstractly.
- A "super-1GWe" pathological `P_native` (a published native plant > 1000 MWe, inverting the replication-floor framing — see epic Item 5 status note on rows #26 / #30 / #31) is a legitimate Low-fit/low-grounding pilot candidate but warrants an explicit note in `pilot_report.md` about what the asterisk means in that inverted regime.
- `model_critic` (Item 9) is exercised as part of the pilot; if its acuity drops on a Med- or Low-fit concept (Phase 0's strong-signal evidence was on ARC only), that's a fold-back into Item 9.

---

## Requirement Selection Notes

Most of the substantive decisions live in the epic Item 10 success-criteria block and Item 5's surprise finding (orthogonal axes, asterisk reuse). This spec captures only the requirements we have actually decided must hold: the explorer's frontmatter-only read, the fail-loud removal of the `result_1gw` fallback, the fractional-`n_mod` verification, the snapshot-before-regen rule, the two-axes pilot coverage, and the issue-list-shaped pilot report. Concrete pilot concept selection, the snapshot artifact list, and the exact location/shape of the narrative-extraction prompt are deferred to design.

---

## Requirements

### Functional Requirements

1. **FR-1**: `extract_explorer_data.py` MUST read `Confinement-Family` from `analysis.md` frontmatter; the body-prose regex (currently `extract_explorer_data.py:89`) MUST be removed.
2. **FR-2**: `extract_explorer_data.py` MUST read the other Item 6 orchestrator-owned fields the explorer consumes (at minimum: `Archetype`, `Archetype-Fit`, `Comparison-Status`, `Grounding-Confidence`) from frontmatter; the exact set is pinned in design.
3. **FR-3**: `extract_explorer_data.py` MUST raise a clear, sourced error when a concept whose orchestrator routing is `costingfe` or `costingfe-asterisked` does not expose `result_1gw` at module level. The current silent fallback at `extract_explorer_data.py:261–262` MUST be removed.
4. **FR-4**: `extract_explorer_data.py` MUST verify (and surface in its output sidecar) that each ingested `result_1gw` was reached by the two-knob call: `result_1gw.params["net_electric_mw"] == 1000` AND `result_1gw.params["n_mod"] == 1000 / P_native` (within float tolerance). A mismatch is a hard error, not a warning.
5. **FR-5**: Pilot concepts MUST span the fit_grade × grounding_confidence grid as: at minimum one High-fit/high-grounding row, one Low-fit/medium-grounding row, one Low-fit/low-grounding row; a Med-fit row included if a clean candidate exists without exceeding five total pilot rows.
6. **FR-6**: For each pilot concept, the snapshot procedure MUST capture every artifact known or discovered to carry human-authored content (`review.md` is the known case; the snapshot scan identifies any others) to `.project/active/concept-rework-explorer-pilot/pre_pilot_snapshot/{cid}/` **before** regeneration is run.
7. **FR-7**: Regeneration of a pilot concept MUST NOT overwrite the artifacts captured in FR-6; if the regeneration pipeline currently writes one of those paths, design specifies the preservation mechanism (skip / merge / sidecar) before regen runs.
8. **FR-8**: The comparison view MUST asterisk rows with `Grounding-Confidence: low` using the same visual idiom already used for `fit_grade=None` / archetype-bespoke rows.
9. **FR-9**: `pilot_report.md` MUST enumerate every surfaced issue with: surface (artifact / validator / explorer / critic), severity, fold-back item (7 / 8 / 9), and disposition (landed before bulk / deferred / accepted residual). A pilot that surfaces zero issues MUST be flagged as a weak-signal result, not a sign-off.

### Non-Functional Requirements

- None specified — pilot scale is small enough that runtime / cost is not a constraint (one critic pass and one regen pass per pilot concept; ≤5 concepts).

---

## Acceptance Criteria

### Core Functionality

- [ ] FR-1 / FR-2: `git grep` against `extract_explorer_data.py` finds no body-prose `**Confinement Family**:` regex; every orchestrator-owned field the explorer consumes is read from frontmatter.
- [ ] FR-3: Removing `result_1gw` from a regenerated pilot `model_setup.py` (test fixture) makes the explorer raise rather than silently degrading (under the three-forward contract there is no `result` to fall back to).
- [ ] FR-4: The explorer's per-concept output records the verified `n_mod` and `net_electric_mw` for each pilot row; injecting a mismatched value in a fixture makes ingestion fail.
- [ ] FR-5: Pilot composition documented in `pilot_report.md` lists each chosen concept with its `fit_grade` and `Grounding-Confidence` and confirms the grid coverage.
- [ ] FR-6 / FR-7: Snapshot directory exists for each pilot concept and contains the pre-regen artifacts; post-regen, those artifacts are present in the concept directory unchanged (byte-identical to the snapshot copy).
- [ ] FR-8: Comparison-view screenshot in `pilot_report.md` shows the asterisk on at least one low-grounding pilot row using the existing styling.
- [ ] FR-9: `pilot_report.md` matches the shape above; every fold-back issue is either linked to a landed change in Item 7 / 8 / 9 or explicitly carried into Item 11 as accepted residual.

### Quality & Integration

- [ ] Existing `exploration/concept_analysis/scripts/` tests continue to pass.
- [ ] Explorer ingestion runs cleanly on every pilot concept end-to-end (regenerate → critic → ingest → render).
- [ ] `model_critic` (Item 9) is run against every pilot concept; its reviews are linked from `pilot_report.md`.

---

## Next-Stage Handoff

**Settled in this spec:**
- The explorer adapter contract: frontmatter-only reads, no `result_1gw` fallback, fractional-`n_mod` verification.
- The pilot's two-axes grid coverage requirement and the "issue list, not green checkmark" report shape.
- The snapshot-before-regenerate rule and its location under this work-item directory.
- Item 12 (native-scale projection) is explicitly out — the pilot validates replication-floor `result_1gw` only.

**Design must figure out:**
- Concrete pilot concept selection (which 3–5 concepts, with `fit_grade` / `Grounding-Confidence` justification each), and whether a clean Med-fit candidate exists without pushing past five rows.
- The exact set of frontmatter fields the explorer consumes (currently: `Confinement-Family`, `Archetype`, `Archetype-Fit`, `Comparison-Status`, `Grounding-Confidence`; design confirms or amends from the Item 6 field block).
- The snapshot artifact list — start from `review.md` and any others surfaced by a scan of the pilot concepts' current directories; design produces the canonical list and the preservation mechanism (skip / merge / sidecar).
- The narrative-extraction prompt path called out by the epic: whether it lives in `extract_explorer_data.py` as today, moves to a template under `prompt_templates/`, or is replaced by a frontmatter read; design picks one and justifies.
- The fail-loud error shape in the explorer (exception class, message format, sidecar fields) for FR-3 and FR-4.
- The fractional-`n_mod` tolerance for FR-4 (exact equality vs ULP-level tolerance vs explicit tolerance constant).
- How `pilot_report.md` documents the "weak signal" case (FR-9) if the pilot surfaces zero fold-backs.

**Watch-outs for design:**
- A pilot row whose `P_native` is integer (`n_mod` exact) doesn't exercise the fractional path — composition must include at least one meaningfully-fractional row.
- A super-1GWe pathological `P_native` row (epic Item 5 status note: #26 / #30 / #31) is a legitimate Low-fit/low-grounding candidate but inverts the replication-floor framing — the report must call this out, not paper over it.
- `model_critic` acuity outside ARC is unmeasured; if it under-performs on Med / Low fit, the fold-back lands in Item 9, not Item 10.
- The asterisk idiom is shared across two distinct semantic conditions (`fit_grade=None` *or* `Grounding-Confidence: low`); design confirms whether the rendered tooltip / legend distinguishes them, or whether the shared mark is intentional.

---

## Related Artifacts

- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 10
- **Upstream items:** Item 4 (library), Item 6 (orchestrator / frontmatter), Item 7 (helpers / validators), Item 8 (prompt templates), Item 9 (model_critic)
- **Item 8 pilot precedent:** [`.project/active/concept-rework-prompt-templates/pilot_report.md`](../concept-rework-prompt-templates/pilot_report.md)
- **Snapshot location (to be created):** `.project/active/concept-rework-explorer-pilot/pre_pilot_snapshot/`
- **Design:** `.project/active/concept-rework-explorer-pilot/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
