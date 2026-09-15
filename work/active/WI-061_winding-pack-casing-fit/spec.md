---
Status: active
Scale: standard
Epic: standalone
Owner: fit_model
Created: 2026-09-15
Updated: 2026-09-15
---
# WI-061 — Winding pack casing fit

## Intended use

[NEED] Add an independently based available-space screen to the current winding-pack calculation so enlarged packs cannot acquire geometric feasibility merely by growing without a cavity limit. Authority: ../../orchestration/goals/winding-pack-casing-fit/goal.md, Question, Answered when and Invariants. The supported answer may be conditional when device-specific cavity geometry is unavailable.

## Requirements

| ID | Requirement and authority | Acceptance evidence |
|---|---|---|
| R1 | [NEED] Distinguish bare pack, insulated pack, casing interior and exterior; define local axes, orientation, units and provenance. Available space must be independent of calculated pack demand. | Reviewed geometry basis, model ownership and dimension identities. |
| R2 | [NEED] Count insulation and assembly clearance exactly once; expose interpretable margins and a native fit predicate responsive to reference current density, current and purchased field envelope. | Positive, exact-boundary and oversized native cases; independent dimensional reconstruction. |
| R3 | [NEED] Preserve the eighteen existing predicates and report their feasibility separately from feasibility including fit. Attribute effects against the immediate entering package. | Expression-level catalog comparison and matched native outputs/verdicts. |
| R4 | [NEED] Reject invalid geometry deliberately and establish native/generated/oracle agreement. | Nonfinite, invalid sign, arithmetic overflow/underflow and native-route checks. |
| R5 | [NEED] Explain any reference failure without tuning the cavity to force acceptance; retain coherent procurement, thermal accounting and total-support pricing. | Independent review, fixed-input old-channel neutrality and declared approximation limits. |
| R6 | [NEED] Supply bounded-study inputs and outputs for reference/enlarged packs and earlier passes; support reporting feasibility loss and sampled cheapest feasible choice. | Coordinator-owned native study at one integrated candidate, compared to preserved entering package. |

## Scope and provenance

[INFERRED] Implement a local, aligned rectangular-envelope screen using current pack area and an explicit aspect ratio. This is a design proposal pending source review, not an owner-prescribed geometry. The existing square-equivalent side does not establish actual orientation. Neither aggregate electromagnetic support mass nor the thermal area allowance determines cavity space.

[NEED] Absolute conductor-current margin, detailed stress, three-dimensional interference and manufacturing-effort estimates remain separate follow-ups. Preserve source quarantine and do not merge or push. Source: goal Invariants.

## Preparation status

Native registration created WI-061 through `pm add-item`. The CLI leaves registry status at backlog; active metadata records actual preparation, following the WI-060 limitation without editing the registry manually. No production changes have been made. Research must determine the admissible source basis and the coordinator must release production after independent design review. The draft design supplies explicitly conditional dimensions for independent review, preserving the reference radial-allocation failure.
