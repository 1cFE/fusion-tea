# Round 2 frozen preparation acceptance

Date: 2026-09-27. [AGENT] Independent reviewer. **PASS for main native execution of the frozen replacement point list.** Final economic release still requires full native verification and results review.

Reviewed replacement study: `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b`. Proposed-point SHA256: `5ca2398ee367b5438e667c3ee9c74f0e8c90919f2bb0416f31015c7a315b1992`. Candidate-freeze SHA256: `d317a0e3d01bb09fc6a619433d6115298bddaa3992d92b54e88dbf763cafc525`.

- Ran the independent [preparation checker](check_preparation.py) successfully against the new freeze. Its [receipt](preparation-checks.json) verifies all frozen artifact/code hashes, 2,496 complete 637-input points, 2,651 aliases, 3,956 evaluated oracle planning points with zero refusals, full nominal/performance catalog counts, predicate ownership, admission proofs and common-input equality across 121 ranking scenario/source groups.
- Independently compared both complete proposal maps and every noncryogenic membership. Exactly 2,492 complete points are unchanged. Only the supplied nuclear-heating input changes in the four approved cryogenic cases. All 2,651 aliases remain; noncryogenic membership metadata is exact.
- Inspected `retain_reporting_locations.py` and `check_selection.py`. The helper preserves the recomputed diagnostic files, restores the original quote maps, and evaluates them with the corrected oracle. It does not substitute old oracle outputs. Independently checked the preserved recomputed-file hashes.
- Independently checked retained reporting coordinates and corrected-oracle signs. The +5 bracket gives approximately `5.000663982332071` and `4.999336017668497 USD2025/MWh`; the −5 bracket gives `−4.999336017668156` and `−5.00066398233173`. Original coordinates are exact and both boundaries remain bracketed.
- The selection receipt maps the four changed point identities to the independently stock-verified native cryogenic cases accepted in [correction-acceptance.md](correction-acceptance.md). Anchors and economic-zero brackets remain unchanged.

This closes the preparation conditions in [reporting-location-disposition.md](reporting-location-disposition.md). Existing source, accounting, variable-role and MR-7 reviews remain applicable to the unchanged native executable. Every frozen point, including engineering failures, must remain in the main native record and its all-case stock verification.
