---
Status: technical work complete; formal close/archive owner-held
Created: 2026-09-18
Updated: 2026-09-18
Related Artifacts: spec.md; combined-design.md
---

# Cooling equipment implementation plan

[AGENT] Execute the combined design after its required independent preimplementation review. Owner approval of the intermediate scenario and continued work is recorded in the goal. This checklist carries the implementation sequence across sessions; the append-only goal trail records task outcomes.

- [x] Confirm retained input cases, historical versus current checks, existing accounts and source boundaries. Evidence: goal Round1/2 records and entering replay.
- [x] Obtain owner decision on intermediate technology. Evidence: goal Round3 owner ruling, HITEC270–465°C with primary helium retained.
- [x] Finish T-008 source capture/report and exact secondary price/quantity interfaces; amend draft combined design with any review corrections.
- [x] Obtain independent combined-design release, retaining accepted limitations separately from must-fix findings.
- [x] Implement reusable canonical equipment/lifecycle calculations, physical child accounts, cost/energy selectors and stellarator scenario inputs. Preserve dormant generic behavior. Coordinator owns canonical model and plant bindings unless a bounded worker brief assigns a subset.
- [x] Implement generated manual bodies where native expression lowering requires them; register analysis family and mirror canonical models. Native generation must be fresh, hash-seeded and repeatable. Update the independent oracle and explicit output maps, census, manifests and appropriate consumer contracts.
- [x] Verify physical quantities, source examples, energy/accounting identities, lifecycle timing/rate limits, mode parity and count/demand response. Run affected regressions and separate new failures from the retained six consumer failures.
- [x] Obtain implementation assurance and prepare one native integration pin. Commit only task-owned files; preserve unrelated work. No merge or push.
- [x] Run the focused native study at that pin, retaining all failed cases and clear matched comparisons. Write the study reading and obtain required independent disposition review before follow-up semantic work.
- [x] Obtain fresh exact R7.S assessment from implemented and executed evidence, update goal answer/account map/findings and project context. Formal native goal closure remains owner-held.

## Acceptance evidence

| Requirement | Check and expected result | Basis | Status |
|---|---|---|---|
| CE-01 boundaries | Every new child owns one equipment class; old primary/intermediate allowance disabled in equipment mode; explicit residual conversion scope | Account map and combined design | Independent release; executable identity tests pass |
| CE-02 machines | Flow split, pressure/head and electrical/fluid work independently reconstructed; exported counts respond to circuits | Primary loop and source equations | Source reconstruction and retained-case native checks pass |
| CE-03 exchangers | Both tube passes counted; installed geometry fixed; required area and positive approaches independently checked | Image-checked source Table2 and Round2 diagnostics | Original source reviewed; native/oracle checks pass |
| CE-04 piping | Annular mass, branches, fitting ratio and layout scaling; secondary head screen | Stated quantity schedule/source fabrication | Explicit geometry and native formula checks pass; assumptions retained |
| CE-05 prices | Raw-year source examples, source inclusion and applicability; CPI proxy explicit | Registered originals and independent reviews | Primary and secondary independent reviews pass as conceptual transfers |
| CE-06 lifecycle | Initial spare count, dated events strictly inside horizon, stable discount/annualization, CAS71/72 ownership | Declared service scenarios and existing finance convention | Dated replacement and actual CAS71/72 consumer tests pass |
| CE-07 integration | Legacy mode preserves entering equations; generated values and independent oracle agree; account deltas propagate to capital/LCOE | Native package and CAS hierarchy | All ten native integration gates pass at retry1 |
| CE-08 verification | Relevant model/parser, executable, domain and affected consumer tests; failures classified against baseline | Entering131passes/6failures | Targeted98passes; later25passes; expanded71passes and same6failures; static L2/L6 fail as documented |
| CE-09 study | Saved controls, selected designs, cost-only/full-energy comparisons and declared sensitivity grid; failures retained | Combined-design study contract | All34 native candidates plus baseline retained; generic and all-point verification pass; frozen study5b956a82 |
| CE-10 independent review | Concrete design release and fresh exact R7.S grade after implementation | Pinned unchanged rubric | Independent final PASS, R7.S=3; final-review-and-grade.md |
| CE-11 preservation | Frozen archive hash and historical paths unchanged; no barred reads, target changes, merge or push | Goal constraints | Archive hash, historical study paths and exact rubric revision unchanged; evidence/round3/preservation.json |
