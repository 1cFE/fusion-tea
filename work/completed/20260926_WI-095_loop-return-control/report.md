# WI-095 report: loop return control

**Status:** implemented and reviewed (fresh design review FINDINGS applied, fresh implementation review PASS with five notes, 2026-09-26); integration seam CANDIDATE on the new identity (executable `f3cfaa1e9b49daf6612bb6d7aed91128d7f3f7963ce3aab487a37d7b78208989`, semantic `a72fe5c4c825e47504e5941d1819344c3895b697d2674a61c853799218929203`, manifest pin `7fb8341cf1206ebf3f83a458f33b3c469089bf08e68f8fcad9f84b2739016028`). The item stays `active` until the goal's round-3 study has run and sealed on the package; closure is the owner's.

**Closed:** 2026-09-26 by the owner's direction (`work/orchestration/goals/design-study-parameters/evidence/owner-direction-close.md`) through `pm close-item`; archived here from `work/active/`. Citations inside the sealed model files, the generated package and the frozen study records keep the `work/active/` path and resolve to this directory.

## What was built

- `models/library/analyses/loop_return_control.sysml` (new, additive): `calc def 'Primary Bypass Control'` (eleven inputs, eleven outputs; the equations, the monotonicity argument and the bisection in its doc) and `constraint def 'Return Condition Held'`, `constraint def 'Bypass Within Limit'`.
- `exploration/costed_loop_brayton/bodies/loop_return_control/primary_bypass_control_impl.py` (new reviewed body, copied into the package prefix-only by the build).
- `models/designs/costed_loop_brayton/costed_loop_brayton.sysml` (additive): `primary_loop.T_comp_in` and `heat_exchangers.he_secondary_in` exposed; new `part return_control` bound to the loop's flow, delivery temperature, duty and required return, the exchanger's UA and cp, the cycle's flow and cp and the closure's secondary inlet; two asserts in `checks`.
- The package `costed_loop_brayton_tea` rebuilt to a fixed point (13 sources, 25 bodies, 0 adapted); `census.json` (165 entry points); snapshot; `studies/{interface_data.py (165 keys, 256 channels, 11 constraints), oracle_entry.py (extended by a fresh worker: 255 catalogued channels, eleven bindings), manifest.json (twelve declared classes: the six executed in round 1, the three ruled under G-001, three for the new root-solve channels declared before any study on this identity)}`; `verify.py` covers the two new checks; `verify_return_control.py` (the pre-change control and the new identities); `tests/model_families.py` lists the new library file.

Commits: `f766bbce` (part 1: definition, body, assembly, package, receipts), `1127c27e` (part 2: interface, oracle, manifest, verifiers, review).

## Acceptance against the spec

| Req | Evidence | Outcome |
|---|---|---|
| R1 explicit bypass control with the exchanger's reduced-flow performance computed | the body's effectiveness-NTU root (design review r3 Q1; implementation review Q1: nothing computed from the duty that the design assigns to the capability) | met |
| R2 checks enforce the relationship without a physical tolerance | `return_condition_ok` at 1e-6 K against a feasible residual of order 1e-11 K and a physical deficit when infeasible (+17.8 K at 2,500 / 1.35, +72.3 K at 1,400 kg/s); `bypass_within_limit` vacuous at the declared 1.0 until the owner sets a limit | met |
| R3 MR-7; pre-change control | flow, ratio, area, ratings chosen; `f` calculated; `max_bypass`, `tolerance` declared and graded; `evidence/return-control-verification.json`: 245 channels bit-exact on every evaluated WI-094 receipt, the 4,000 kg/s case refused in both (implementation review Q2, Q4) | met |
| R4 arrangement A representable as the f = 0 family | the study composer's boundary solve (`studies/study_support.py`, `boundary_designs`) executes the located ratio as a chosen input | met (exercised by the round-3 study) |
| R5 concept-agnostic, graded, no shared file edited | new library file; grades in the assembly doc lines; preservation checks `-t010-build`, `-t010-seam` pass (20,973 files) | met |
| R6 study tooling and CANDIDATE | `work/orchestration/goals/design-study-parameters/evidence/integration-t010/integration_return.json`: CANDIDATE, ten gates (45 handwritten files byte-identical, 165 entry points re-derived, six preflight gates, oracle parity with every verdict re-derived, lineage) | met |

## Development cases (the eight WI-094 cases on the new identity)

| Case | Net MW | Unmet MW | Bypass fraction | Feasible | Return residual K | New checks |
|---|---|---|---|---|---|---|
| `c1-aries-ratios-reselected-ratings` (starting point, I-R) | 426.579 | 0 | 0.3112 | 1 | −4.0e-11 | both satisfied |
| `c1-aries-ratios-aries-ratings` (I-A) | 426.579 | 0 | 0.3112 | 1 | −4.0e-11 | both satisfied (ratings still violated) |
| `best-screen-point-reselected` (2,500 / 1.45) | 575.617 | 0 | 0.1296 | 1 | ≈ 1e-11 | both satisfied |
| `best-screen-point-aries-ratings` | 575.617 | 0 | 0.1296 | 1 | ≈ 1e-11 | both satisfied |
| `starting-point-fuel-term-wired` | 424.789 | 0 | 0.3112 | 1 | −4.0e-11 | both satisfied |
| `c1-ratio1.35-reselected-ratings` | 575.227 | 278.149 | 0 | 0 | +17.796 | return condition violated |
| `c1-flow1400-aries-ratings` | 365.279 | (unmet) | 0 | 0 | +72.3 | return condition violated |
| `c1-flow4000-reselected-ratings` | refused (lifecycle body) | | | | | |

Every existing channel of every case equals its WI-094 value bit for bit. The receipts are `evidence/native_runs/<case>/result.json`; the identities and the control are `evidence/return-control-verification.json`; the identity verifier `evidence/verification-summary.json` passes (7 cases, eleven checks re-derived).

## Review notes and dispositions

Design review (`…/evidence/design-review-r3.md`, FINDINGS): the correct-before-implementation item (the return check was tautological when the exchanger outlet was computed from the duty) is corrected: the outlet is computed from the achieved capability in both branches and the residual is the root-solve closure; the monotonicity derivation, the cp-identity guard, the vacuous limit, the linear bypass equivalents not being acceptance values, the uncontrolled meaning of the closure's `he_hot`/`he_return`, and the bypass-loss disclosure are applied in the design and the definition's doc. Implementation review (`…/evidence/implementation-review-r3.md`, PASS): notes on a third raising guard (zero duty, unexercised), the loop flow's pre-existing calculated role, the vacuous limit's wording, and the receipt's `prefix_only` field placement; all accepted as disclosures.

## Replay

```
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/costed_loop_brayton/run.py --root /tmp/wi095-replay'
.codex-test/run python exploration/costed_loop_brayton/verify.py --runs /tmp/wi095-replay --out-dir /tmp/wi095-replay
.codex-test/run python exploration/costed_loop_brayton/verify_return_control.py --runs /tmp/wi095-replay --out /tmp/wi095-replay/return-control-verification.json
```
