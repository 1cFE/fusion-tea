# Independent final review and R7.S grade

Reviewer: `equipment_review`, 2026-09-18; non-author of models, rubric, account map, research and goal answer. Earlier independent physical/accounting reviews remain applicable. No model or source edited; no full suite rerun.

## Cell record

| Field | Assessment |
|---|---|
| cell_id | R7.S |
| rubric_version | `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d` |
| model_version | `af226462c8f72ee1425eae4239c8617b25e1432e`; current HEAD verified; no working-tree diff in models or generated package |
| score | **2** |
| anchor_satisfied | “Costs follow loop thermal power or flow quantities with source basis” |
| model_evidence | `models/library/analyses/mfe_account_costs.sysml:532` and `:559`; `models/library/structure/mfe_plant_systems.sysml:62`; `models/designs/generic_mfe/mfe_plant.sysml:465` |
| runtime_evidence | `exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/coolant_cost_impl.py:80`; `evidence/entering-replay.json`; replay database compatibility row |
| study_evidence | Four-case diagnostic replay under `evidence/entering-replay/`; historical/current selected channels agree, but no new equipment-cost study exists |
| why_not_next | Pumps, piping and exchangers lack independently sized/priced child accounts and appropriate installation/spares/replacement/maintenance logic. |
| grader | Independent reviewer `equipment_review` |

The coolant equation retains a sourced primary net-power term and intermediate thermal-power term, with explicit CAS rollup. This meets S2, not the exact S3 anchor, “Pumps, piping, heat exchangers as separately sized subaccounts,” or the general decomposed-lifecycle test. Source basis here means the inherited model attribution; this review does not newly certify its price year or completeness. R7.P is not regraded.

Current package contract executable fingerprint `5cbec23bcb96913ccacfb3ea30e8a94bdabf37a03899c9c88997e9cf4f064e41` exactly matches the replay database. Contract SHA256 is `60f5dba4d0a7b7f7330d7a828850d82f7429d23fdd916b3eb2178a9a3b9442f7`.

## Final gate and bounded outcome

**Substantial implementation remains held; R7.S3 remains unmet.** The completed continuation return is OPERATOR_QUEUE, with four original candidates queued, no registration and no bounded negative. This legitimately records unsuccessful retrieval within this investigation. It does not prove literature exhaustion or that supplier quotations are necessary.

The inaccessible NGNP/HTGR originals are retrieval gaps. The acquired low-temperature INL method has an applicability gap: its equipment-based installation workflow does not establish high-pressure helium prices. The screened 2024 follow-up supplies no equipment-specific bridge. Separately, target topology, secondary conditions, pressure/material construction, pipe layout and lifecycle/account boundaries remain incomplete. Acquiring a PDF alone would not resolve these design gaps.

Release requires checked original equipment prices/equations, actual price year/currency, scaling/domain and installation inclusions; explicit target specifications and justified conceptual transfer; nonoverlapping replacement of the inherited allowance; and lifecycle treatment plus the concrete verification/study contract in the accounting review. Published reference estimates can suffice. Vendor quotations are an alternative. Physical qualification may remain separately unresolved in a clearly bounded conceptual estimate.

## Answer and evidence-integrity checks

The answer's numerical table agrees with replay outputs. Its WI-067 relative link resolves correctly. No model price change means no newly calculated equipment-cost delta, not zero missing cost. Both selected designs now fail breeding; r2 controls retain their three prior failures plus breeding. The 131-pass/six-failure baseline does not certify assertions skipped after schema failures.

Before publication, update the answer's stale “final assessment pending” and “reports are being pursued” wording to this completed assessment and operator queue. Replace “source establishes two active machines” with “source lists two machines per loop; the energy balance supports both operating,” because activity is inferred. Otherwise its central conclusions agree with this review. Goal and WI-067 remain open; no installed-cost estimate or equipment-cost study was completed.

## Corrective-diff and round-record assurance

Independent follow-up, 2026-09-18: the answer corrects all three requested wording points, names the four queued originals and identifies original-table acquisition followed by applicability review as the next action. Its unchanged-cost, historical/current feasibility and test-limit claims remain accurate. Descriptions of prospective source tables are retrieval leads, not certified cost evidence.

The trail explicitly returns T-001 as STRATEGY_BLOCKER and T-002 as completed specification only. It records the initial research-bound overrun and prospectively bounded continuation rather than disguising them as a compliant first attempt. The import-path correction is accurately distinguished from a changed scientific case. Closing this strategy round leaves the goal and WI-067 open and does not release implementation or assert literature exhaustion.

The six proposed dispositions preserve existing finding IDs and distinguish retained hydraulic requirements, source/qualification seams, current breeding failures and unresolved cost research. Their responsibility and next-evidence statements agree with the reviewed evidence; none claims an implemented remedy or a new study result. They are suitable for append-only acceptance under the existing findings. The learning delta accurately captures account/lifecycle gaps, verified physical anchors without prices, unchanged selected cooling/economic channels and changed full-plant verdicts. No broad rerun or round reopening is warranted by these corrective edits. R7.S2 and the implementation hold remain unchanged.
