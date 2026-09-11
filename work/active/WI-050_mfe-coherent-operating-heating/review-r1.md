---
Verdict: pass
Created: 2026-09-11
Related Artifacts:
  Design: ./design.md
  Spec: ./spec.md
  Previous Review: ./review.md
  Dispositions: ./design-dispositions.md
---

# WI-050 independent design re-review

## Summary

The revised design is ready for planning. The actual indicator parser and verifier accept the four scalar efficiency assertions, and native boundary execution confirms their domain behavior. The revision preserves the operating-heating and installed-procurement contract; no unresolved design finding or new owner-held decision was identified.

Reviewed `spec.md@54a0725e`, original negative `review.md@d28ac7e3`, and revised design, dispositions and `prototype-r1/` at `60535433`. This is a fresh non-author review, focused on R1–R3 and coherence with the accepted specification under the parent's brief. Requirements, architecture, conventions and validation were checked locally; no supporting delegation was needed. Original review and prototype evidence remain unchanged.

## Findings and dispositions

### R1 — Resolved: scalar predicates work through actual consumers

**Original severity:** critical. **Status:** parent accepted correction; independently verified resolved.

The two dimensionless definitions use `efficiency > 0.0` and `efficiency <= 1.0`, asserted separately for source and coupling. Each generated predicate contains one feature and one literal. The actual indicator parser at `scripts/study/indicators.py:450` accepts every generated entry. The actual verifier at `scripts/study/verify.py:206` resolves exactly one input operand per new assertion and returns the expected result for both stages at 1.0, −0.5, 0.0 and 1.01. No shared-tool change is required.

The generated census is 18 individual assertions, 28 feature-reference occurrences and 247 public inputs. The aggregate `headline` response is separate. The generated operating-demand binding reads `sustain__p_aux_required`; there is no public stellarator operating-demand parameter. Baseline, negative-source and over-one-source native verdicts agree with the independent verifier. Evidence: `review-r1-evidence/consumer-results.json`, `checks.json` and `checks.log`.

### R2 — Resolved: consumer and boundary coverage is explicit

**Original severity:** concern. **Status:** parent accepted correction; independently verified resolved at design stage.

The design's “Affected live consumer inventory and implementation obligations” names the direct oracle, single runner, oracle binding map, route count, four study-test files, family tests and package/manifest dependency. Named implementation tests cover signed demand, generic defaults, scalar consumers, the public-input census, reserve invariance, direct/native parity and financial attribution. These remain implementation obligations, clearly distinguished from the working prototype.

This reviewer regenerated and executed only the small native boundary fixture in `/tmp`. Five signed-demand cases and eight efficiency cases passed. Positive, exact upper equality and exact zero satisfy both heating bounds; insufficient capacity violates the upper bound, and negative demand violates burn hold without clipping. Zero operating outputs are exactly zero. Both stages accept 1.0, reject negative/over-one values through the corresponding assertion, and fail native evaluation explicitly with `ZeroDivisionError` at zero efficiency. The actual verifier separately reports the violated positivity assertion at zero.

Native direct-only, mixed and all-zero defaults also pass. Direct-only retains 50 MW procurement, 30 MW coupled demand, 40 MW operating delivery and 80 MW electric draw. Mixed retains 100 MW procurement, 67.5 MW coupled demand, 90 MW operating delivery and 180 MW electric draw. All-zero outputs are zero. Every rerun output and response matches retained author evidence exactly; errors match in type and division-by-zero cause. Evidence: `review-r1-evidence/boundary-summary.json` and retained `prototype-r1/boundaries.py`.

### R3 — Bounded limitation remains accurately disclosed

**Original severity:** suggestion, nonblocking. **Status:** parent accepted bounded disposition; independently reconfirmed.

A fresh targeted differential reports Level 2 at 10 unchanged issues and Level 6 increasing from 227 to 229, with no removals. Its JSON matches the author's differential byte for byte. The two introduced diagnostics are:

- `ERROR: Unsupported operator '.' in attribute 'mfe_plant::'MFE Power Plant'::p_operating_coupled_heat'`
- `ERROR: Design attribute 'mfe_plant::'MFE Power Plant'::p_operating_coupled_heat' has expression but codegen cannot extract a numeric default: Feature reference 'p_coupled' found in static expression. This violates ADR-002 Rule 3. Run 'agentic-mbse validate' to identify and fix the violation.`

Successful native producer-default execution and the generated stellarator producer edge contradict their blocker implication on this tested route. The design correctly calls them introduced checker findings and keeps Level 6 failing. This is a bounded disposition, not a checker fix or a general waiver. Repeat the differential after production changes. Evidence: `review-r1-evidence/validation-diff.json`, `boundary-summary.json` and `checks.json`.

## Retained contract and standards

The revision changes predicate representation and verification coverage. The cost classification and financial propagation tables are unchanged. All 158 retained scalar outputs are exactly unchanged between original and revised prototypes in each of seven full-plant cases. Original `review.md` and `prototype/` bytes match `d28ac7e3`; preservation hashes are retained in `review-r1-evidence/repair-diff-checks.json`.

Independent conversion and thermal/electric/divertor conservation assertions pass over native outputs. The reserve pair preserves operation while procurement changes from $264145000 to $316974000. The physical demand control preserves heating procurement and explains its unchanged divertor heat through alpha compensation. Availability alone leaves online heat and power unchanged. The corrected baseline remains net 1013.931932554 MW and headline LCOE 224.269232884 $/MWh, with divertor heat violated. These are prototype results and do not establish a feasible plant.

MR-WI050-1 through -9 remain coherent with the design. The library/design separation, plain Real quantities, existing citation chain, CAS cost interfaces and retained financial conventions respect project MR-1–6 and relevant AD-001/003/004/005/006/007. The new fractions introduce no parameter-metadata requirement. No new source, technology/module scope, financial convention, residual acceptance, or historical reinterpretation is proposed. Routine planning approval remains with the parent.

## Verification and limits

All Python used `.codex-test/run`; no installation or holdout access occurred. Reran the retained `consumers.py`, `check_results.py` and `check_repair.py` with writes redirected to reviewer evidence using `review-r1-evidence/run_checks.py`. Separately copied `boundaries.py`, `scratch.txt` and `validation_diff.py` to `/tmp/wi050-rereview/` and ran those copies. The small fixture generated locally; full-family generation and broad regression were not repeated. All targeted checks passed with no skips. The targeted differential reports the failures described under R3.

Retained full-family validation reports Levels 1, 3, 4 and 5 passing, ten inherited Level 2 issues, and 229 Level 6 issues including the two introduced findings. Production model/twin changes, direct/native parity, explicit unchanged-finance-formula checks, package-dependent regressions and fresh implementation audit remain required. The financial bridge is attribution reconstructed from reported outputs; it does not independently validate the financial source relations. The design explicitly requires a declared current package/manifest for dependent study tests and disclosure if package preparation is deferred.

## Accepted changes and deferred items

R1 and R2 corrections satisfy the parent's recorded dispositions. No further design change is requested. R3 remains the recorded bounded checker limitation, with a production differential required. No new deferred item or owner gate is introduced.

Proceed to `$plan-model`, carrying the named implementation and verification obligations forward.
