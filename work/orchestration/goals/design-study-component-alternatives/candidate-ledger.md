# Candidate ledger

[AGENT] Updated during round 1. A candidate here is a comparison strategy, not a successful engineering design. Native diagnostic case identities and every failure are in `evidence/readiness-screen.json`; the executed 498-case blocked study retains complete case identities in `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/results/cases.json`. No verified ranking is released.

| Candidate | Evidence and disposition | Status |
|---|---|---|
| Complete published Stellaris vs complete ARIES | Owner excludes attribution-confounded whole-plant comparison | Declined by owner scope |
| Full three-stream ARIES source into either cycle | PbLi-to-salt and merged source interface missing from existing steam path; compatibility map H4/H5 | Declined for this bounded comparison |
| ARIES blanket helium at 456 °C into existing salt/steam path | Native S3 refuses nonpositive IHX terminal approach; S1 cannot repair it by changing salt temperature alone | Unsupported unchanged interface |
| ARIES divertor source C-3 | Assemblable in principle; hot limit is not a complete source state, retained model and source duty/flow differ, fixed return absent | Deferred in favor of the better-defined Stellaris boundary |
| Original C-1 versus original whole-plant steam outputs | Diagnostic controls execute; C-1 needs 31% modeled bypass and has different auxiliary/cost boundaries | Retained controls; not a matched economic comparison |
| Fixed supplied source at 80/90/100% duty | Steam temperature checks remain applicable at fixed temperatures, but a fixed active IHX may not achieve all duties and required returns without a modeled control | Replaced as primary design proposal by offered exchanger circuit counts; no main points executed |
| Offered steam IHX circuit counts with externally matched source duty | Original diagnostic matches the unchanged primary loop and selected 10/11/12 IHXs at delivered heat 2819.514/3024.031/3214.740 MW. Submission 3 rejected external physical-closure solves as the main-study route. | Historical diagnostic retained; superseded production design |
| Chosen source heat/ratio with model-owned primary bypass control | Source offers 2500/2800/3000 MW and independently chosen 10/11/12/14 IHXs; controllers calculate bypass or retain deficient transfer. Five substantive bodies include one new finite-water-cooler closure family. Submission 4 passed independent review without a policy waiver. | Implemented and integrated; 498-case native study completed, but six numerical verification failures block release |
| Two circulator cost correlations (C-5) | Changes price equation for the same equipment | Declined; does not answer the categorical component question |
| Recuperator present/absent | Genuine physical alternative but shares omitted equipment/cooling issues and does not improve the present scope | Deferred; no unrelated study opened |

## Native readiness cases

S0–S5 and B0–B2 are all retained in `evidence/readiness-screen.md`. S1 and S3 are expected native refusals. S2/S4/S5 execute with unsupported or insufficient unchanged equipment. B2 fails source heat/return checks. No failed case is promoted to an economic winner. S0 includes seven whole-plant failures outside the proposed isolated comparison, all kept in the raw record.

## Changed and reused inventory

The isolated assembly is `models/designs/component_alternatives/plant.sysml`, with its own generated package at `exploration/component_alternatives/component_alternatives_tea`. Original Stellaris/ARIES models, packages and studies remain unchanged. The final preservation receipt checks all 13,215 protected files.

| Scope | Final behavior and evidence |
|---|---|
| Primary loop, bypass algorithms and gas network | Existing definitions/bodies reused; chosen source and ratios remain public inputs. |
| Steam cycle and original ratings | Reused at the held 445/445/42 °C offer; broader temperature/head variation declined. |
| Selected salt pump count | Additive variant permits independently chosen pump count; k=2 control matches the original implementation. |
| Controlled boundary | New bounded accounting/algebra connects actual transfer, returned temperature, controller loads and ratings. |
| Recuperator capability | New algebra derives effectiveness from selected UA and operating flow. |
| Finite water cooler | One new iterative definition used for three coolers, including pump heat and property limits; main-study numerical accuracy remains unresolved. |
| Conversion ledger | New subsystem energy and present-value cost accounting, with explicit replacement/service assumptions. |
| Native constraint representation | Boolean guards use supported numeric screens; two labels and residual-magnitude views align stock identities without changing physical predicate meanings. |

WI-096's report, implementation census and independent integration review distinguish these extensions from unchanged reuse. No required coupled physical solve runs in a study harness.

## Executed catalog and disposition

| Candidate family | Declared / distinct native points | Native engineering result | Disposition |
|---|---:|---|---|
| Gas flow × stage ratio × service offer at three source duties | 375 | 14 pass; 322 have a cooler no-root validity failure; 39 other failed combinations | Retained finite catalog; no continuous optimum or envelope claim |
| Steam connecting-equipment offers at selected passing gas anchors | 72 / 69 additional | 21 pass including three aliases | Retained; turbine offer remains fixed |
| Efficiency, price, recurring allowance and common upstream PV sensitivities | 48 | All native predicates pass; two cases fail numerical verification | Unreleased sensitivity evidence |
| Smaller controller offers | 6 | Three steam offers pass; three gas offers fail bypass capacity | Retained; no assumption that every smaller offer must fail |
| All distinct native cases | 498 | 83 pass all checks, 415 fail; six numerical mismatches in total | Verification blocked; no economic release |

The nominal selected steam connectors are 10 circuits × 4 pumps at 225 kg/s design flow, 11 × 4 at 225 kg/s, and 14 × 3 at 250 kg/s for reactor heat 2500, 2800 and 3000 MW. Gas selections are 2000 kg/s with stage ratio 1.5, 1750 kg/s with ratio 1.8, and 2000 kg/s with ratio 1.65. All use the tested 25/25/25 MW/K cooler offer and 60 MW/K recuperator. These are selected discrete offers, not automatically sized equipment or equally optimized technologies.

Full choice provenance and duplicate aliases are retained in the study's proposal files, anchor selections and `window.json`. Every native failed case and all earlier diagnostic refusals remain available. Numerical verification failures are separately joined in `results/verification-diagnostics.json`; passing predicates do not override them.
