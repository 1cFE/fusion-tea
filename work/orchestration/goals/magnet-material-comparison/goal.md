# Goal: REBCO versus Nb₃Sn magnet subsystem at matched duty

## Status

`grounded` — 2026-09-29. The owner requested this goal and its execution through the initiating brief, preserved verbatim at [evidence/owner-brief.md](evidence/owner-brief.md) (SHA-256 `eb5536f2…7cb6`). The slug was supplied in the brief; no further naming confirmation was requested.

## Question

[AGENT] (ratified by owner, 2026-09-29) For the same specified magnetic duty in a supported operating range, how do explicit REBCO and Nb₃Sn winding alternatives compare in current margin, conductor inventory, winding fit, refrigeration demand, and subsystem cost, and which assumptions determine the preference?

## Consumer

[AGENT] (ratified by owner, 2026-09-29) The owner, evaluating whether the model can support a credible component/material-choice study. A useful result may later support the write-up, but editorial corrections proceed independently and this goal must earn its conclusions through evidence.

## Answered when

[AGENT] (ratified by owner, 2026-09-29) An executed, independently checked comparison of genuinely different supported conductor alternatives quantifies the requested subsystem consequences (current margin, conductor inventory, winding fit, cold load, electrical refrigeration demand, subsystem cost) at matched duty, uses consistent accounting, and tests at least two consequential uncertainties that could change the conclusion. Where a dimension is only bounded, the answer says so and shows whether the bound still supports a decision. If missing physics or costs prevent the conclusion, the goal reports partial/unmet completion and the exact next evidence needed.

Deliverables (brief § Deliverables and answer contract): native goal/trail/learnings with linked research, model and study records; a source evidence matrix and data-sufficiency finding; a reviewed comparison contract and supported alternative definitions; a sealed, verified native study with explicit choices, failed/unsupported statuses and replay instructions; `answer.md`; a compact results table and SVG/PNG figures traced to recorded cases, with data and renderer; a short proposed narrative with an assessment of whether it qualifies as a defensible component/material-choice example. A data-sufficiency report alone is partial completion. Scientific qualification of a complete stellarator magnet is outside the contract.

## Invariants

- **Package:** [AGENT] (ratified by owner) Existing reference behavior, historical packages and sealed studies are preserved. Conductor alternatives are additive, isolated variants with regression evidence that the existing REBCO/Stellaris reference is unchanged. Each round's study runs against one promoted pin.
- **Comparison:** [AGENT] (ratified by owner) The alternatives are genuinely different conductor definitions with their own properties and equations; changing price, temperature or field-limit inputs in the same conductor law does not count. Both alternatives meet the same specified magnetic duty (ampere-turns, field magnitude/orientation basis, conductor length basis, spatial allocation) inside a common range supported for both. Any REBCO-only high-field extension is reported separately from the matched comparison. The existing 24.9 T Stellaris reference is not forced onto Nb₃Sn, and no field value in the brief is treated as a universal material limit. Economics stay inside the declared magnet/refrigeration subsystem; full-plant LCOE is out of scope. Unsupported cost categories are reported as partial accounting, not filled in. A fixed-duty calculation is not a reactor redesign, and lowering field is not claimed to preserve Stellaris plasma performance. If geometry changes feed back into field in a claimed result, the deficient geometry relationship is repaired or replaced with supported evidence first.
- **Modeling requirements:** [INHERITED: modeling_project/REQUIREMENTS.md] MR-1 to MR-6 apply to all model additions; MR-4 citations on every new quantity. MR-7 governs: turns, parallel conductor count, winding-pack dimensions, conductor construction and installed refrigeration capacity remain supplied design choices. Requirements (required current, required pack area, required cold capacity) are calculated and compared with the supplied design; nothing is automatically resized to pass. A separately declared search may propose candidate hardware, but each selected design must be evaluable without that policy, and inventory and cost follow the supplied design. Unsupported conductor field/temperature/strain domains are reported as unsupported, never as pass or fail. Each capacity/fit relation introduced or repaired is exercised with insufficient and sufficient supplied designs plus an unsupported-domain case.
- **Source discipline:** [INHERITED: CLAUDE.md; knowledge/holdout/aries-cs/PROTOCOL.md] The clean-room screen applies before every fetch; quarantined material is never read or cited; no earlier source exception is assumed to extend to this goal. Consequential numbers are checked against original figures/tables, and new source interpretations or equations are independently checked before dependent modeling.

## Grounding evidence

- [evidence/owner-brief.md](evidence/owner-brief.md) — initiating brief, unpinned; no native digest until committed with this goal.
- `.project/active/write-up/magnet-study-evaluation/evaluation.md`, `narrative-proposal.md`, `data/claim-evidence.csv`, `replay/` — category-fit investigation, source limitations and supplied-winding replay; untracked, unpinned; no native digest. Investigation evidence only, not a sealed study.
- `.project/active/write-up/feedback-resolution.md` — editorial context separating this study from write-up corrections; untracked, unpinned; no native digest.
- work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md@55cc001c2 — September sizing study: one REBCO conductor with historical automatic sizing.
- work/orchestration/goals/magnet-closure/trail.md@55cc001c2 — magnet closure history, including the non-reproducible August REBCO/Nb₃Sn input swap (`:403`).
- work/orchestration/goals/preserve-model-design-choices/evidence/magnet-binding-plan.md@55cc001c2 — the MR-7 repair that made windings supplied (WI-075).
- work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-capture/report.md@55cc001c2 — 48 kA supplied magnet capture.
- knowledge/SOURCE_INDEX.md@55cc001c2 — registered Molodyk et al. REBCO tape source (`development_and_large_volume_production_of_extremely_high/`), Demattè/Bruzzone EU DEMO Nb₃Sn winding pack, ITER cryoplant pages, REBCO strain/angle sources, PROCESS cost accounting form.
- knowledge/KNOWLEDGE.md@55cc001c2 — DI-009 (cryoplant fraction of Carnot, 4.5 K vs 20 K), DI-010 (Nb₃Sn vs REBCO winding-pack current density).
- models/library/analyses/mfe_conductor_current.sysml, mfe_conductor_grade.sysml, mfe_magnet_field.sysml, mfe_winding_pack_fit.sysml, mfe_winding_pack_cost.sysml, mfe_magnet_cost.sysml, mfe_cryo_plant.sysml, mfe_cryo_inventory.sysml; models/library/structure/mfe_magnet_parts.sysml; models/designs/stellarator_09/stellarator_plant.sysml — all @55cc001c2. Current conductor, field, fit, cryogenic and cost definitions; bindings are to be established in round 1, not assumed.
- docs/research_seam_operator_guide.md@55cc001c2 — research seam protocol.

## Limits

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) with task, inputs, scope and meaning identical |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 4 rounds `[AGENT]` (brief § Execution bounds); at the limit, deliver the best supported answer and name unmet criteria |
| Time or iteration limit | One promoted pin and one committed study per round; study domains declared before execution |

## Reserved gates

[AGENT] (ratified by owner, 2026-09-29) The owner keeps: formal goal closure and work-item closure; material scope changes (including full reactor redesign/optimization or a new detailed electromagnetic/mechanical solver); unresolved scientific choices that change the comparison's meaning; source-access exceptions and any purchase. No publish, push, merge, or contact with vendors/authors. The owner's article and supporting HTML are not edited. Routine implementation choices, source acquisition within existing permissions, bounded model additions/repairs, native studies and required independent reviews are authorized without repeated confirmation.

## Close rule

[AGENT] (ratified by owner, 2026-09-29) Owner-held. The owner closes the goal after reviewing the answer and any unmet criteria. The coordinator may close rounds and recommend goal closure.

## Amendments

### Amendment 1 — 2026-09-30 — Round 2 question and scope (owner-originated)

[OWNER-VERBATIM] Round 2 question: “Can REBCO’s additional field or winding-space capability improve the plant enough to offset its higher magnet cost, measured in LCOE?” Full brief preserved at [evidence/owner-brief-round2.md](evidence/owner-brief-round2.md) (SHA-256 `2dfaa54d69ee8192…`).

What this amends, each traced to the brief:

- **Question and answer contract.** Round 1's matched-duty subsystem answer stands. Round 2 answers the LCOE question above: “Investigate the chain conductor choice → achievable field and winding geometry → plant performance and equipment → LCOE.” Answered when the brief's four shown items exist (a matched-duty comparison connected to Round 1; the best supported plant design points per material; an LCOE breakdown; the REBCO price at which the whole-plant preference changes, where a supported crossing exists), with interaction results, figures, replay evidence and a short narrative; or when a credible LCOE comparison cannot be established and the missing relationship is named as partial completion (“subsystem savings alone do not answer this round”).
- **Invariant “Comparison”, superseded in part.** “Economics stay inside the declared magnet/refrigeration subsystem; full-plant LCOE is out of scope” no longer applies: “All accounting must return to LCOE … Use consistent whole-plant accounting for both alternatives.” The sentence “A fixed-duty calculation is not a reactor redesign” is replaced for Round 2 by the brief's “Let each material have explicit design choices suited to it” within “a bounded search with justified ranges.” The invariant's last sentence is strengthened: “Resolve the known field/geometry limitations wherever the result depends on them. Do not infer plant benefits from a conductor field limit alone.” All other Round 1 invariants stand, including MR-7: “Preserve the distinction between a supplied design and calculated requirements; no silent resizing to make constraints pass.”
- **Reserved gates, narrowed.** “Model updates and source acquisition are authorized where needed”, and “Select one coherent plant model and explain why it supports this comparison.” A bounded per-material design search is authorized; full reactor optimization and a new detailed electromagnetic/mechanical solver remain reserved. Cleanup is authorized: “Fix the missing package oracle_entry and retire the bogus source registration.” Unchanged: “Keep the article unchanged”; “Formal closure remains with me”; no publish, push, merge, purchase or vendor/author contact.
- **Review.** “obtain focused independent review of the new physical relationships, comparison assumptions, and integrated accounting.”
- **Limits.** Unchanged (round limit 4; one pin and one study per round).

### Amendment 2 — 2026-09-30 — Round 2 question refined to an assumption map (owner-originated)

[OWNER-VERBATIM] “we need to focus on getting some insight. Across explicit assumptions about confinement and coil geometry, when does each material give lower LCOE—and are those conditions supported by evidence?”

[AGENT] Effect on the answer contract: Round 2 is answered when a map over explicit confinement assumptions (renormalization factor, beta limit) and coil-geometry assumptions (peak/axis field ratio, pack-size term) shows, per cell, which material gives the lower whole-plant LCOE at its best supported design point, at which REBCO price the preference changes, and what evidence supports that cell's assumptions; with the LCOE decomposition, failed/unsupported cases retained, figures and replay evidence, and the narrative the Round 2 brief asks for. The brief's other terms stand (Amendment 1).
