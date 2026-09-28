# Focused density-profile source and proposed-contract review

[AGENT] Independent reviewer, 2026-09-21. Scope: the bounded implementation proposal in `../physics-inventory.md`, the initial `spec.md`, `design.md` and `plan.md` in `work/active/WI-081_aries-hollow-finite-edge-density-profile/`, and visually inspected primary `lyon-p701.png` at `.project/active/aries-comparison-preparation/post-reveal-preparation/mapping/evidence/`. This applies the focused source/design provisions of `audit-models`. Source and design are accepted for implementation; execution acceptance remains pending.

## Finding

[AGENT] The proposed generic local-density relationship is supported: `n(rho)=(A-e)*(1-rho^p)^q*(x+(1-x)*rho^2)+e`. The primary image prints `p=12`, `q=1`, `x=0.66`, and `e/A=0.1` immediately below Eq. (3). Its later `edge/axis=0.1` statement conflicts with interpreting the same A as axis density. Preserve that conflict and use only the explicit equation-shape ratio for the comparison case. No source amplitude is established by this review.

[AGENT] A supplied amplitude remains an independent coefficient. At the axis, `n(0)=(A-e)*x+e`; at the edge, `n(1)=e`. Thus the reference shape gives `n(0)=0.694*A`, excluding axis or peak labels for A. A clearly synthetic unit amplitude is permissible for equation verification.

[AGENT] The proposed finite domain, `rho` in `[0,1]`, `A>0`, `0<=e<=A`, `p>0`, `q>0`, and `x` in `[0,1]`, supports a finite nonnegative profile. It is a chosen mathematical subset, not an ARIES engineering validity envelope. Domain refusal must survive the actual generated/native evaluation path, including nonfinite inputs.

[AGENT] An independent reference oracle can use the expanded polynomial `n/A=0.694+0.306*rho^2-0.594*rho^12-0.306*rho^14`; this follows exact decimal arithmetic and differs structurally from directly transcribing Eq. (3). Include center, edge, an interior point, changed supplied amplitude and off-reference shapes. Check the constant case `e=A` and the `x=1` nonhollow limit if those advertised boundaries remain included.

[AGENT] Allowed bounded implementation: a concept-agnostic calc, a comparison-specific component owning its supplied profile inputs, and calculated local density. Moments, temperature, fusion closure and plant claims require separate evidence. No material source or design blocker remains within that scope.

## Native design disposition

[AGENT] Accepted for implementation. R1–R5 retain the bounded outcome and explicit units. The generic calc owns the equation; the comparison component owns its amplitude, source shape choices and edge-ratio binding. Distinct formal names and density EXPOSE make the intended binding path reviewable without altering existing plant producers. MR-7 is satisfied by the proposed supplied-choice roles, subject to verifying their actual generated bindings and amplitude/shape propagation.

[AGENT] The typed manual completion is acceptable as the proposed route to enforcing the declared domain. Acceptance must still demonstrate generated/native execution, seal identity, finite-input/intermediate/output refusal, and unsupported cases failing through TEAx. Review of these documents is not evidence that those runtime behaviors already exist. The plan correctly keeps that verification and independent final review open. The expanded polynomial and advertised-domain boundary checks above remain focused verification guidance.
