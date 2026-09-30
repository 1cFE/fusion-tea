# T-004 independent comparison-contract and design review

You are a fresh, independent reviewer in `/home/reid/1cfe/fusion-tea`. You did not author the contract. Review `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` (draft r1) before any model is built. Write your review to `work/orchestration/goals/magnet-material-comparison/evidence/contract-review.md` (the only file you write). Budget about 25 tool calls; return at most 500 words. Do not read goal trails or delegate. Two separate checkers are verifying the source numbers against originals in parallel; you judge the comparison's design, not transcription.

## Read

- The initiating brief: `work/orchestration/goals/magnet-material-comparison/evidence/owner-brief.md` (§ Engineering question, § Comparison contract, § Model and study requirements).
- MR-7: `modeling_project/REQUIREMENTS.md` § MR-7.
- The contract, and as needed `evidence/evidence-matrix.md`, `evidence/binding-audit.md` (sections 2, 4, 6), and the coordinator's unchecked magnitude screen `evidence/screen/contract-screen.json`.
- Clean room: do not open `knowledge/holdout/**` or any ARIES-CS material.

## Questions

1. **Duty coherence.** Is holding the Stellaris coil geometry fixed and scaling turn current with peak field (I = 50 kA × B/24.9 T) a physically consistent matched duty? Does it genuinely keep the omitted winding-size field term out of claimed results? Is the Stellaris anchor a reasonable choice, and are its limits stated?
2. **Genuinely different definitions.** Do the two conductor definitions satisfy the brief's requirement for different properties and equations rather than changed inputs to one law?
3. **Fairness of construction.** Is the common-P / native / common-C pairing a fair way to separate material effects from construction effects? Is anything load-bearing missing or double-counted in the required-area formula (for example protection copper counting element copper, steel scaling, CICC void applied to REBCO)?
4. **Margins.** Is it fair to use different acceptance rules per material (Nb₃Sn temperature margin, REBCO current fraction), with the symmetric alternative as a sensitivity? Is reporting both operating fraction and temperature margin for both enough for a like-for-like reading?
5. **MR-7.** Check the role table and offer policy: are n, construction, refrigerator rating and temperatures supplied; are requirements calculated and compared rather than bound; does inventory and cost follow the supplied design; is the separately declared offer policy identifiable and its selected designs evaluable without it? Are the planned insufficient/sufficient/unsupported tests adequate?
6. **Cryogenics and accounting.** Are the staged loads, efficiency basis and capital basis consistent between the two temperatures? Is the subsystem boundary consistent, and are exclusions honestly labelled as partial accounting? Is the break-even price computable from recorded cases as claimed?
7. **Outputs and claims.** Do the statuses, tolerances, materiality criteria and uncertainty set meet the brief's answer contract? Is anything claimed that the evaluated effects cannot support?

## Return

`contract-review.md`: per question, `OK` or a concrete finding with the change needed. Overall verdict `PASS`, `FINDINGS` (list required changes before implementation, distinguishing blocking from advisory), or `OWNER_GATE` (only for an unresolved scientific choice that changes the comparison's meaning and that the brief does not delegate).
