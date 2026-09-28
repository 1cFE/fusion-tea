# Independent accounting-convention review

Reviewer: `equipment_review`, 2026-09-18. Inspected `models/designs/generic_mfe/mfe_subsystems.sysml:280` and `/home/reid/1cfe/1costingfe/src/costingfe/defaults.py:327`. Both describe CAS23 as steam turbine-generator, condenser and feedwater; neither explicitly identifies a steam generator. This review does not certify the inherited coefficient's empirical scope or read its external calibration documentation.

**Both proposed conventions can define honest conceptual ownership, but the narrower interface is preferable for the exact R7.S3 task.** Source-boundary uncertainty does not automatically prevent S3. It must remain separate from proof of accounting disjointness and complete plant-price accuracy.

## Recommended smallest scope

End Row 7's intermediate circuit at the salt supply/return interface to power conversion. Row 7 owns its primary circulators, primary piping, helium-to-salt IHX, intermediate salt pumps/piping and appropriate circuit lifecycle. Explicitly assign the salt-to-steam generator to Row 8/power conversion. Keep its decomposition and inclusion in the inherited CAS23 coefficient **unverified**, rather than asserting that the coefficient demonstrably prices it. Do not add a steam-generator charge in Row 7 as well.

This can meet the exact Row 7 requirement for separately sized pumps, piping and heat exchangers without inventing steam-side conditions or expanding into a conversion redesign. It does not waive the one-owner rule: the generator has one declared owner, with its price coverage unresolved. Primary-to-salt exchanger ownership still needs reconciliation when replacing the old C220200 allowance; shifting the downstream interface does not resolve that separate overlap by itself.

Report the resulting estimate as decomposed heat-transport accounts through the declared interface. Do not call it a complete costed heat-to-electricity chain or assert the steam generator is free, absent or proved included in CAS23. Retain this Row 8 coverage gap in whole-plant economic conclusions. The unchanged rubric permits a subsystem to reach S3 while another subsystem retains a named decomposition/estimate-quality gap; it does not require all plant accounts to reach the same depth simultaneously.

## Additive steam-generator alternative

Alternatively, explicitly assign the steam generator to C220202 and retain CAS23 for turbine-generator/condenser/feedwater. That is consistent with the current textual descriptions and can be an agent-defined accounting convention. It needs a separate quantity/cost method and a declared treatment of possible historical overlap. Do not fabricate a subtraction from CAS23 or claim its empirical coefficient has been rederived. A matched alternative-scope sensitivity can show the economic effect of the uncertain incremental generator charge; it is not a calibrated error bound or evidence that both accounting interpretations are correct.

This option adds thermodynamic and cost-method work without being necessary to satisfy the exact R7.S3 anchor. Choose it if the authorized goal explicitly requires a separately priced downstream generator or evidence makes that broader boundary valuable. Neither convention should be used to declare the total plant free of omissions/duplicates.

## Disposition

Recommend the narrow interface for the forthcoming ledger, with the Row 8 generator-price uncertainty explicit and one-owner accounting enforced. This is scope guidance, not a production implementation release or a new R7.S grade. The concrete primary/intermediate equipment and lifecycle ledger still requires review.
