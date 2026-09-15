# Winding-pack/casing fit study protocol

Status: executed under coordinator release ac1d675a. The prepared sample retained 117 report rows and 116 unique native cases after the candidate scan. Exact-boundary semantics reuse the independently reviewed component tests; no additional native boundary witnesses were needed. Resolved outcomes and evidence are in record.md and results/.

## Authority and scope

[INHERITED: goal.md and evidence/study-brief.md] Preserve existing predicates and distinguish old-predicate feasibility from feasibility including fit. Compare shared channels with captured entering-oracle evidence, explicitly identified as such. Execute at most 150 unique native cases. Keep the entire native store and content-addressed evidence. The coordinator owns commits and candidate release.

[OWNER] Intake is captured verbatim in record.md §2. The study answers a conditional geometric-screen question; geometric passage alone does not establish structural or device-specific qualification.

## Proposed bounded sample

[AGENT] Start with the 60 entering density/envelope/minor-radius/current/major-radius proposal rows in preparation/proposals-entering.json. Add the exact manifest baseline and deduplicate using fully resolved inputs. The historical three eighteen-predicate passes are covered by the density/envelope/current block. Hold existing physical and economic inputs unchanged in the matched entering comparison.

[INHERITED: WI-061 design.md@677d6d31] Radial interior is the existing coil-layer allocation less two mechanical wall thicknesses. The 0.30 m nominal allocation is smaller than the 0.36 m reference area-equivalent pack side even before the wall and insulation allowances. Nominal radial fit failure is expected. Allocation sensitivities change the complete existing coil_t entry group, including all radial-build consequences.

[AGENT] Add the twelve retained entering allocation comparisons: 0.40/0.50/0.60 m at the reference and each of the three historically passing density/envelope/current anchors. Their old scalar values and predicates must match the entering oracle at the same allocation. Differences between allocations are legitimate existing geometry effects and are reported separately from the added fit predicate.

[AGENT] At the 0.50 m allocation, add one-at-a-time geometry sensitivities at those four anchors: aspect ratio 0.8/1.25, transverse interior 0.35/0.45 m, mechanical wall 0.015/0.035 m per face, external insulation 0/0.005 m per face, clearance 0/0.004 m per face, and transverse internal-build fraction 0. These eleven alternatives per anchor add at most 44 points. Baseline geometry uses aspect ratio 1, transverse interior 0.40 m, wall 0.025 m, external insulation 0.003 m, clearance 0.002 m, radial internal-build fraction 0 and transverse internal-build fraction 0.025. Radial internal build stays fixed. These choices are explicit engineering scenarios from the reviewed design, not measured cavity dimensions.

[AGENT] The proposed list is at most 117 points before deduplication: sixty original proposals, one exact baseline, twelve allocation points and 44 geometry alternatives. Reserve up to twelve additional direct equality and just-inside/just-outside witnesses where represented geometry and floating-point behavior make them defensible. Final choices follow the candidate oracle scan; a failed nominal radial allocation must not make all sensitivity cases uninformative.

[AGENT] All axes are proposed as sensitivities. Report sampled cheapest cases with and without the fit predicate over the same sample, separately for the original nominal family, the allocation alternatives with nominal remaining geometry, and the shape/insulation/clearance alternatives at 0.50 m. Keep the nominal 0.30 m screen's result explicit. No continuous optimum is claimed.

## Release and execution

Execution requires an explicit coordinator release, copied CANDIDATE integration return, passing independent review, and unchanged released package identity. Qualified entry groups and candidate defaults are resolved only after that release. A prepared script is not execution authorization.

Prepared tooling: execution/build_proposals.py builds 117 unevaluated coordinate rows and twelve axis declarations using the author-supplied interface. preparation/expected-fit-interface.json records eight held nominal inputs, seventeen expected fit outputs, predicate identity, and expected input/output/predicate counts. The predicate compares the minimum of the two axis margins with zero; both margins remain published. execution/prepare.py requires preparation/execution-release.json and preparation/integration-return.json before importing the route, validates the interface and pins against the candidate, captures the package/oracle inputs, and deduplicates by fully resolved coordinates. Native generation must confirm every input fan-out before the axis declarations are accepted. study.py retains the same explicit release gate before native execution.

Run all-axis indicators, retain their limitations and rulings, execute the pinned baseline, and record every preflight gate. Scan the candidate and edge behavior independently before fixing the prepared native list. If no all-predicate feasible anchor exists, state that fact and use separate old-predicate and geometric-fit diagnostics; do not silently claim a feasible-anchor edge scan.

Every native case uses the stock StudyRunner/PreparedListStrategy route through study_route.run_points. Retain every numeric output and exact qualified predicate identity. Verify by verdict-stratified generic verification and by all-case independent mapped scalar and predicate comparisons. Compare the retained entering predicate definitions exactly with their candidate counterparts and require unchanged shared numerical channels and old verdicts at matched inputs.

Freeze snapshot values and hashes only after execution, verification, native-store/artifact joins and record checks pass. Record unresolved coverage plainly. The executor writes first-sighting findings and an honestly labeled executor synthesis; independent assurance is coordinator-owned.
