# T-012 brief — fresh review of the plant comparison contract (r1)

You are a fresh reviewer for goal `magnet-material-comparison`, Round 2, in `/home/reid/1cfe/fusion-tea`. You did none of the work. The owner's question is: “Across explicit assumptions about confinement and coil geometry, when does each material give lower LCOE—and are those conditions supported by evidence?” The coordinator wrote `evidence/plant-contract.md` (r1) to make that question executable on the Stellaris plant model. Your job is to find where the contract would produce a misleading, unsupported or MR-7-violating result, and where it mislabels evidence.

## Read

1. `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` (the artifact under review).
2. The owner's brief and ruling: `evidence/owner-brief-round2.md`; `goal.md` §§ Invariants and Amendments 1–2; `trail.md` § Round 2 (strategy revision, T-009/T-011 returns, the owner ruling).
3. The evidence the contract cites: `evidence/plant-chain-audit.md` (all sections), `evidence/sources/field-term.md`, `evidence/sources/plasma-validity.md`, `evidence/sources/nb3sn-stellarator.md`, Round 1's `evidence/comparison-contract.md` §§ 2–8 and `answer.md`.
4. `modeling_project/REQUIREMENTS.md` MR-7 and `modeling_project/STUDY_POLICY.md` §§ 2, 9, 11.
5. Where you need to check a model fact the contract asserts (an attribute is an entry point; a held constant; an equation), open the cited file:line in `models/` or `exploration/stellarator_e2e/`. Clean room: never open `knowledge/holdout/**` beyond PROTOCOL.md or the barred paths listed in `evidence/briefs/t009-plant-chain-audit.md`.

## Check, and write a finding for each defect

A. **Evidence labels (§ 3).** For every value on the two axes, is the label ([S]/[A]/[D]/[U]) the one the cited source note supports? Is anything labelled [A] that is really [U] at this plant, or [S] that is [U] away from the anchor? Is the pack-size arm's formula the re-anchoring the field-term note actually supports, and is its floor check stated correctly?

B. **The confinement axis.** Does applying `f_ren` as a uniform multiplier for both materials at every design of a cell reflect the sources' meaning of the renormalization factor? Is holding `beta_limit` 0.05 defensible, and is the 0.045 variant placed where it matters?

C. **The coil-geometry axis.** Is setting `B_max` per material (13 T / 25 T) instead of the Stellaris 24.9 T envelope consistent with the goal invariants ("no field value in the brief is treated as a universal material limit") and MR-7? Is the HELIAS-class ratio applied to the Stellaris plant an assumption the owner's question allows, and is it labelled honestly? Does the arm's sign (bigger pack → lower ratio) follow from eq. 39 as printed?

D. **The materials (§ 4).** Is the REBCO `extrapolated 20–25 T` band justified by Round 1's definition and the Molodyk data extent, and is treating the Stellaris reference as extrapolated a fair reading? Are the Nb₃Sn bands, strain allowable and `B_max` 13 T (edge admitted) consistent with Round 1?

E. **Supplied designs and MR-7 (§ 5).** Is every quantity the policy proposes supplied to the model and then checked, with nothing resized inside the model? Is the "matched fusion power" rule for `n_e0` a defensible design choice, and does the `power_short` fallback keep MR-7 (a supplied design evaluated as given)? Are the structure-mass rule and the heating rule labelled as the assumptions they are, and are their variants placed where they can change the map? Is the grid bounded and justified, and is anything in it physically incoherent (e.g. a Nb₃Sn 12 T peak design at (12.7, 1.3) with `f_ren` 1.0)? Is the case count credible?

F. **Accounting (§ 6).** Does the single-basis rule remove every double count named in the audit's § 4 map? Is anything from Round 1's annualization still entering? Is replacing the plant's cryo chain by the Green laws for both materials in the material instances, while the reference instance keeps the plant chain, coherent, and does it bias either material? Is the USD2021-inside-mixed-year statement honest?

G. **Statuses (§ 7).** Rule on the treatment of the four reference-common screens: is "supported except those four, with margins reported and a downgrade if worse than the reference" defensible, or must they be held common in another way, or must they be disqualifying? Are `unsupported` / `failed` / `supported` mutually exclusive and complete?

H. **Reporting (§ 8).** Does the reporting deliver the owner's four shown items (Round 2 brief) and the map with evidence labels? Is the break-even derivation (LCOE linear in tape price at fixed design, with re-selection per price) correct for this model's DCF?

I. **Package and verification (§ 9).** Is the derived-package route and the three-oracle verification plan adequate for "focused independent review of the new physical relationships, comparison assumptions, and integrated accounting"?

J. **Anything the contract omits** that the owner's brief or ruling requires, or any claim that would infer a plant benefit from a conductor field limit alone.

## Return

Write `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract-review.md`: verdict (RELEASE / REVISE / BLOCK), numbered findings with severity (blocking / must-fix / note), the quoted contract text, the evidence or rule it conflicts with (path and location), and the fix you propose; then what you did not check. Run Python only as `.codex-test/run python ...` if you compute anything; modify nothing except your review file; do not commit. Return at most 300 words: the verdict and the blocking and must-fix findings.
