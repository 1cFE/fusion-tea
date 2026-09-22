---
Status: active
Scale: standard
Owner: transfer_physics_inventory
Created: 2026-09-21
Updated: 2026-09-21
---

# WI-081: Explicit-amplitude radial density profile

[INHERITED: coordinator assignment, 2026-09-21] Implement the local density relationship in Lyon Eq. (3), preserving amplitude as a supplied quantity and keeping generic logic separate from the comparison case. The new models and native execution package are isolated from the existing plant. Original owner authority is recorded in `work/orchestration/aries-transfer-experiment/`; this is a post-reveal subsystem experiment.

## Contract

- **R1 [INHERITED]:** Represent `n(rho)=(A-E)*(1-rho^p)^q*(h+(1-h)*rho²)+E` with supplied amplitude `A`, edge density `E`, normalized coordinate `rho`, radial exponent `p`, profile exponent `q`, and hollowness `h`. Amplitude and edge/output densities use `m^-3`; other quantities are dimensionless. Do not interpret `A` as axis, maximum or average density.
- **R2 [INHERITED]:** Generic library logic contains no ARIES-selected parameter values. A comparison case selects `p=12`, `q=1`, `h=0.66`, and `E/A=0.1`, citing the primary equation image. An arbitrary demonstration amplitude is labeled as such and remains a public choice.
- **R3 [INFERRED]:** Enforce a declared mathematical domain: all inputs finite, `A>0`, `0<=E<=A`, `0<=rho<=1`, `p>0`, `q>0`, `0<=h<=1`; refuse nonfinite intermediate/output arithmetic. This is a supported mathematical subset, not empirical plasma qualification.
- **R4 [INHERITED]:** Parse, generate, and execute the actual new model through the pinned SysML/codegen/TEAx route. Preserve chosen values. Verify center/edge identities, an interior point, parameter changes, amplitude scaling, and invalid-input refusal in native execution.
- **R5 [INHERITED]:** Keep existing plasma definitions and plant bindings unchanged. Report local density only; moments, normalization from observed densities, full fusion power and LCOE are outside this work item.

## Source and acceptance

[INHERITED: Lyon 2008, printed p701 Eq. (3)] Primary source: `knowledge/holdout/aries-cs/08-FST-Lyon.pdf`; retained image: `.project/active/aries-comparison-preparation/post-reveal-preparation/mapping/evidence/lyon-p701.png`. Authorization applies only to this comparison-specific use. No shared domain fact is registered.

[AGENT] The page states `n_edge/n_e0=0.1` below Eq. (3), but later says `n_edge/n_e,axis=0.1`. The equation with `h=0.66` makes `n(0)=0.694*A`; amplitude identification with axis density is unresolved and is not assumed. This work implements the explicit equation, rather than inferring amplitude from the later absolute edge value or any published average/maximum.

[AGENT] Acceptance needs focused independent source/design review before implementation, successful generated/native checks, and independent review of consequential final behavior. MR-7 acceptance concerns preservation of supplied profile choices and validity; insufficient/sufficient hardware tests do not apply because this calculation selects no equipment or capacity.
