---
Verdict: pass
Created: 2026-09-27
Related Artifacts:
  Design: ../../../../active/WI-098_whole-plant-conversion-comparison/design.md
  Spec: ../../../../active/WI-098_whole-plant-conversion-comparison/spec.md
  Previous Review: boundary-review.md
---

# Independent complete-boundary review — submission 2

**PASS for the pre-implementation design gate. MR-7 compliant at the reviewed design level; implemented behavior remains unverified.** The coordinator may execute the exact48 kA capture and implement this isolated model. This does not release the main study, certify the unexecuted offer or qualify an operating reactor.

[AGENT] Continuing independent non-author reviewer. The r1 design/configuration are preserved at commit276cfe48; the previous review was not edited. R2 was reviewed as the diff against that revision and then pinned at81423599. Exact reviewed hashes: design.md `f4a879df60eb41bb3f3e6da50a48ce23419cf5ca43c6b6396dd0f561bd694973`; configuration.md `42e615e2aa788bd120fa3a51f91285ee8c651363d75ccf47b11c8c50492533af`. Scope is the three corrections and their source, account, finance, lifecycle and variable-role interactions. Valid original-evidence and conversion coverage in [r1](boundary-review.md) is reused.

## Finding dispositions

| R1 finding | R2 evidence and disposition |
|---|---|
| F1: missing major overhead scopes | **Resolved.** Configuration lines65–110 define exact purchase-membership sets and separate contingency, indirect services, freight, general spares, tax, construction insurance and nonfuel commissioning. CAS50 startup/decommissioning/supplementary contingency have explicit replacement or zero dispositions. Initial equipment is summed once; old aggregate totals remain excluded. CAS30 buys services and the separate midpoint factor finances initial spending. |
| F2: competing source inputs | **Resolved.** Design§3 directly binds both source inversion and primary evaluation to `source_basis.q_source_MW`; the old source becomes a calculated exposure. Configuration§Exact legacy-input migration retires the old input, rejects unequal duplicate values before stripping keys and requires the final generated input census to contain one source authority. The existing current key is now exactly `stellarator_09__stellaris__magnet__coil__turn_current`. |
| F3: undefined D/Li6 purchases | **Resolved.** Design§4 defines D consumption plus unrecovered exhaust, separate gross-breeding-based Li6 consumption, atomic masses and isotope/recovery assumptions. Annual Li6 feed maintains composition; full PbLi event refill buys the replacement maintained stock without crediting consumed atoms twice. Separate T supply/decay and the ban on the old blended fuel cost remain explicit. Native D/T/Li6 atom residuals and parameter variations are required. |

## Independent checks and interactions

The retained [probe](boundary-review/check_r2.py) and [receipt](boundary-review/r2-checks.json) evaluate the proposed equations without importing implementation code. They use deliberately distinct synthetic purchases for membership checks, not predicted plant costs. A gas slot3 purchase increase of USD1 million raises initial total by USD1,464,233.333 under the declared overheads. The same increase in delivered slot9 raises it by USD1,449,233.333; the USD15,000 difference is exactly the excluded freight. Direct capital equals the sum of all selected initial leaves once. Held branch purchases do not change. Contingency produces the expected affine response at fixed equipment.

Sixteen fuel scenarios cover2500/2800 MW, mean/lower TBR, extraction1/.9 and exhaust recovery.99/.98. Their D/T/Li6 atom identities close. Lower extraction changes external T rather than neutron-driven lithium consumption. The explicit Li7-as-Li6 treatment is a conservative price proxy, not a claim about the actual breeder isotope reaction distribution. These probes establish design arithmetic only; native generated output and predicate verification remains required.

I inspected the exact inherited steam slot1 composition and both branch-account scopes. Steam stock and the explicit salt spare must be removed by their named leaves, without also adding the aggregate salt subtotal. General spares are calculated on the declared eligible installed-cost proxy; they do not silently purchase demanded machinery. Source replacement/overhaul bases remain separate from initial overhead. The r2 assumption that replacement quotes include their own delivery, tax and execution overhead prevents a second project-overhead charge on every event. Initial T stock and the dated terminal event replace their old provisions individually.

The shared finance migration remains correct. Operational years must now be a positive integer both at preparation and in native domain enforcement, so the written end-year annual sums are defined. Construction duration and replacement dates may remain real. Initial finance is applied once before adding discounted future events. Terminal cost responds to the new initial total; salvage uses its explicit equipment-proxy membership. Recurring reserves are not added beside event cashflows.

One nonblocking wording limitation remains in configuration line77: “excludes … stocks/spares” is exact for separately identified stock/spare leaves. The explicit gas membership at line76 includes the whole transport slot9, whose inherited aggregate also owns cycle-helium stock. Its split is not known. Therefore the defined gas overhead/salvage calculation is an aggregate installed-cost proxy that includes that inseparable stock; it cannot be reported as a verified equipment-only or stock-free base. The exact listed membership supplies an unambiguous implementation, and no additional stock cost should be added to it. Clarifying that sentence is an objectively verifiable documentation correction, not a new physical or purchasing decision.

## Release boundaries

The unchanged source interpretation remains within the owner's authority: a supplied thermal source for a conditional comparison, with `source_qualified=0` and no reconstructed plasma or global manufactured-fit claim. The48 kA inventory is independently chosen and priced. Its current, fit, field-domain, cryogenic and other applicable component checks must be evaluated; a capture identity or installation allowance cannot substitute for them. The failed50 kA offer and the unchanged3000 MW pressure/divertor failures remain preserved and excluded.

The design now supports a complete declared major-account inventory and meaningful whole-plant reranking. It does not establish market coverage for hypothetical aggregate quotes, detailed service-installation scope, site water availability or global reactor construction. The required study must quantify consequential unknowns through justified ranges or native-checked reversal thresholds. The new overhead sensitivity method is valid at fixed hardware and operation; technology/catalog minima still require reranking each scenario, since a fixed-offer affine threshold is not automatically the optimized-catalog threshold.

Before main-study execution, retain the design's exact48 kA native capture and conservative nuclear-envelope evidence; generated source/finance migration and capture-map checks; sufficient/insufficient hardware and fixed-inventory load tests; conversion replay; independent verification of every new account, electrical term, fuel quantity, event and predicate; and substantive integration review establishing at least one supported common source condition for both branches. A new material capture or implementation failure requires disposition before changing the supplied offer or admitting cases. Final MR-7 behavioral assurance belongs to that integration evidence.

No production model or package was changed by this reviewer. No previous review, baseline or sealed study was changed, and no owner gate is newly required by these corrections.
