# Findings and failed attempts

| ID | Evidence | Finding or attempt | Disposition |
|---|---|---|---|
| F-001 | thermal-audit.md and thermal-screen-result.json | Supplied 85% PbLi split starves the network divertor at the prior high-load case. | Main comparison includes a bounded split range and fair common cycle-flow choices. |
| F-002 | thermal-audit.md; original ARIES plasma model | Imposed plasma computes fusion but no sustainment requirement. | Supplied-load downstream comparison; 20 MW deposited heating/40 MW electric held explicit; no plasma feasibility claim. |
| F-003 | cost-audit.md; selected purchase bindings | Native costs and primary pump law contain no topology/split differential. | Annual-extra-cost/unrecovered-extra-power break-even chart plus native pressure-loss uncertainty; no invented engineering estimate. |
| F-004 | thermal-screen-result.json | Tiny terminal differences and no supplied primary-return requirement. | Retain full states; source-specific 30 K approach sensitivity and explicit missing qualification. |
| F-005 | screen.py first scratch attempt | Oracle does not export primary-return channels; first extraction raised KeyError after successful numerical evaluations. | Corrected extraction to retain oracle's actual outputs; native screen independently retains returns. Scratch invocation failure, no main study was run or overwritten. |
| F-006 | comparison reviewer | Capture errors: .05 written for baseline .045 pressure loss; audit reversed source selector labels. | Correct contract to .045; audit corrected to 0 supplied/1 calculated; original records unaffected. |
| F-007 | thermal-audit.md; original B3 branch outputs; native main results | Prior B3 prose attributed the series failure generally to helium; the relevant series failure is PbLi, while the prior fixed-split network failure is divertor. | Use stored per-branch duties for the new explanation; append a disposition to original finding #4 without editing its frozen record. |
| F-008 | Coordinator independent selection versus reporting worker draft summary | Missing paired economics at 2600 MW was briefly misread as neither layout passing; the network has passing cases there while series has none. | Correct before final report/seal; retain unpaired network range extension and no fabricated paired LCOE. |

These are goal findings, not minted native discovery IDs. Native study findings will be registered in its own record and discovery log before sealing.
