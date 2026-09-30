# T-005 independent oracle and offer-policy brief

You are an independent author in `/home/reid/1cfe/fusion-tea` (branch `goal/magnet-material-comparison`). A separate implementer is building the SysML model and handwritten bodies for WI-099 in parallel. **Do not read** `exploration/magnet_materials/bodies/`, `exploration/magnet_materials/magnet_materials_tea/`, `models/library/analyses/magnet_conductor_alternatives.sysml` or `models/designs/magnet_materials/`. Your oracle's value is that it is written from the contract and design alone.

## Inputs

- Released contract: `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` (r3).
- Reviewed design: `work/active/WI-099_magnet-conductor-alternatives/design.md` (§ 2 equations, § 6 case-input names).
- Checked source values: `work/orchestration/goals/magnet-material-comparison/evidence/check-nb3sn.md`, `check-rebco-cryo-cost.md` and the evidence notes in `evidence/sources/`. Where a value is needed (NIST 316 fit coefficients, Stellaris thermal inventory values, CPI factors, Green and Strobridge laws), read it from the cited source file and cite it in your code comments.
- Clean room: never open `knowledge/holdout/**` or ARIES-CS material.

## Deliverables (you own exactly these new paths)

1. `exploration/magnet_materials/oracle.py` — pure Python (standard library only) implementing every calc of design § 2 as functions of a dict keyed by the design § 6 names, returning every output named in design § 2 (same names). Include the NIST 316 conductivity integral (your own numerical integration) and the Tcs root (your own method; the implementer uses bisection, so use a different method such as Brent or Newton with bracketing).
2. `exploration/magnet_materials/studies/offer_policy.py` — the declared offer policy of contract § 5, using the oracle: for each anchor, field, material, pairing, rule family and variant, the smallest integer element count meeting the acceptance rule under that case's assumptions; construction areas from the construction rule at that duty (contract § 4: construction P and C, with the variants); insufficient ⌊0.9 n⌋ and generous ⌈1.2 n⌉ offers; refrigerator ratings from the fixed list (reference offer's demand, next lower as insufficient).
3. `exploration/magnet_materials/studies/declare_cases.py` and its output `exploration/magnet_materials/studies/cases.json` — every case with all design § 6 inputs plus labels (`anchor`, `B_peak`, `pairing`, `rule_family`, `variant`, `offer_kind`: reference / insufficient / generous / variant-offer, `refrigerator_kind`). Cover: anchors D and S; fields 8, 9, 10, 11, 12, 13 T (both anchors) and REBCO-only 14, 16, 18, 20 T (anchor D; Nb₃Sn still evaluated there so its status is recorded); pairings common-P, native, common-C; rule families reference, both-temperature, both-fraction; and the one-at-a-time variants listed in contract §§ 3–8 (including strand grade, strain, Tcs 6.5 K, REBCO shape/anchor/T*/degradation, steel base and scaling, copper-density variants, η and capital bases and the combined unfavourable case, cold-load multiplier, electricity price, capital recovery, anchor D turn length, manufacturing allowance, and price levels). Reference offers are re-evaluated unchanged under each variant; variant offers are separately labelled. Keep the case count below about 3000 by applying variants at the reference rule family and common-P and native pairings only; state what you chose.
4. `tests/models/test_magnet_oracle.py` — pure-oracle tests against the source points and tolerances listed in contract § 5 (not against the package).
5. `exploration/magnet_materials/studies/oracle-notes.md` — equations as you implemented them, every constant with its source, and any contract or design ambiguity you had to resolve (flag it; do not guess silently).

## Rules

Run Python only as `.codex-test/run python ...` from the repository root. Do not modify existing files. Do not commit. Return at most 400 words: what exists, the case count by label, test results, and any ambiguity found in the contract or design.
