# Numerical evidence and lineage reuse

[AGENT] Preparation at `c1b853ad80d3aefa2fc98ce45288582b3482eddb` reuses current-lineage evidence. The September 14 draft's numerical baseline, eighteen-predicate inventory and proposed extra checks are superseded by the current records; those proposals add no requirements.

| Evidence | What is established | Scope retained |
|---|---|---|
| `work/orchestration/goals/divertor-peak-heat-load/evidence/T-003_integration/integration_return.json`, published at `686bc67b`, implementation `48b65159` | Ten native gates returned CANDIDATE; source, generated package, baseline and oracle were checked | Original integration omitted reader read-set coverage; it is supplemented below, not rewritten |
| `work/orchestration/goals/bounded-feasibility-transfer/evidence/round2-review.md@c1b853ad80d3aefa2fc98ce45288582b3482eddb` and referenced Round 1 check receipt | Independent review of 71 native cases, 16,046 mapped scalar checks and 1,420 predicates; corrected bounded search counts | Declared-window/control: 191 unique coordinates, 185 evaluated and six refused; nine below-bound oracle-only diagnostics remain outside protocol; zero combined passes |
| `work/orchestration/goals/bounded-feasibility-transfer/evidence/transfer-checks.json@a16e7256` | Three joint anchors, six isolated contrasts, three transverse contrasts and four loop contrasts | Conditional response under source-shaped geometry/material assumptions; anchors use study-specific allocations, loop counts and inventory reserve, not automatic forward-run defaults |
| `work/orchestration/goals/magnet-manufacturing-cost-completeness/account-ledger.md` | Explicit priced procurement, winding and support boundaries, conditional insulation stock and unpriced remainder | Mixed price years and processing boundaries remain; added coolant assemblies are not priced by the power-scaled coolant account |

## Fresh preparation checks

[AGENT] `check_lineage.py --out lineage-check.json` passes against the current checkout. It verifies unchanged tracked production models, generation inputs, executable package and independent oracle versus the reviewed WI-065 checkpoint; rejects new untracked SysML inputs; verifies all 296 sealed package artifacts; checks recorded semantic/executable identities; resolves the pipeline's actual input references; and calls the native `assert_read_set_covered` on all twelve read paths. Negative probes reject an unpinned internal path and a path outside the package.

[AGENT] `.codex-test/run python -m pytest tests/test_dependency_provenance.py -q`: **3 passed**. This checks the immutable dependency references and actual sealed wheels/runtime APIs. `.codex-test/run python -m pytest tests/study/test_read_set_coverage.py -q`: **6 passed**. These exercise actual altered pipeline references, including outside-root and unpinned paths, guard order, current coverage and permitted input renaming. No physical model evaluation was performed by these checks.

[AGENT] The native integration driver still omits the direct coverage call at its gate 6. This comparison package supplies the concrete current-package check; it does not claim to have repaired that general driver or re-executed all ten integration gates. Source continuity and fresh seal verification justify reusing the existing integration evidence.

## Limits that survive preparation

[INHERITED] Sixteen numeric channels were retained but not independently mapped by the prior oracle. Static L2/L6 limitations and the recorded exact-current-boundary sign difference remain. A missing independent check is not a successful verification. The manifest names evidence and unresolved applicability by quantity.

[OWNER] Constraint violations and failed execution remain reportable outcomes. Finite bounded search found no combined pass; it is neither a global infeasibility proof nor a reason to forbid a valid constraint-violating fixed-point prediction. No numerical comparison establishes conductor, coolant, equilibrium, neutronics, hardware or whole-plant reliability qualification.
