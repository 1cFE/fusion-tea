# Computed breeding: a usable research model, an unresolved plant model

## Result

[AGENT] **The breeding gap is not closed.** Research recovered and executed a published model that calculates tritium breeding from helium-cooled lead-lithium blanket choices. Its validated configuration does not cover the retained stellarator. No model equation, generated plant package, physical limit, frozen r2 result or historical study was changed. Formal goal closure remains the owner's decision.

Tritium breeding ratio (TBR) is the number of tritium atoms produced in the blanket per tritium atom consumed by fusion. A value above one is necessary, but losses, extraction and stock requirements can demand more than one.

## What is now calculated?

A **research executable**, recovered from Martínez Arroyo's published HCLL surrogate, calculates TBR from 26 inputs. HCLL means helium-cooled lithium-lead. Its inputs include lithium-6 enrichment, material fractions, first-wall thickness, separate inboard/outboard breeding layers, surrounding layers and tokamak geometry. Its underlying physics comes from neutron-transport calculations; it is not a geometry multiplier applied to a single published TBR.

The retained stellarator still takes achieved TBR as the supplied value 1.074. The research executable has not been connected to it because doing so would exceed the source's domain. [Source assessment](evidence/hcll-surrogate-assessment.md), [executable](evidence/hcll_surrogate_probe.py), [retained results](evidence/hcll-surrogate-probe-results.txt).

## Which choices affect the research calculation?

All rows below retain the thesis reference configuration except the named change. They are **not stellarator predictions**.

| Source-domain case | Calculated TBR |
|---|---:|
| Published reference inputs | 1.135285 |
| Lithium-6 fraction 0.70 | 1.082858 |
| Lithium-6 fraction 0.80 | 1.111386 |
| Inboard breeder 35 cm | 1.105302 |
| Inboard breeder 55 cm | 1.158301 |
| Inboard breeder 80 cm | Rejected: outside domain |

The published final module prints 1.13509 at its reference, a difference of 0.000195 from the recovered example. The appendix example and selected final network may differ; that explanation remains unproven. No coefficient was adjusted to remove the discrepancy.

## How was it checked?

- **Software:** The researcher recovered all 253 weights and normalization arrays. A fresh reviewer checked them against the original PDF and compiled the original C++ function. Python and C++ agree within 2.3e-16 over five cases. This verifies transcription and evaluation.
- **Physical basis:** The thesis separately compares its reduced two-dimensional geometry with three-dimensional neutron transport over ten DEMO cases, reporting TBR deviations from −1.29% to +1.42%. Those cases support that specific reduction; they do not bound transfer to a stellarator. The network's own interpolation errors are another uncertainty.
- **Applicability:** The source's first-wall domain is approximately 2–4 cm and inboard breeder domain 30–60 cm. The current model uses 5 cm and 80 cm. Its geometry and material definitions also differ. Input clipping or unrestricted extrapolation would conceal this gap.

The example-network error statistics and final-module discrepancy remain unresolved. Applying the source's published correction produces a diagnostic value, not a validated uncertainty bound for this example or the stellarator. [Independent method and probe review](evidence/method-review.md).

## Does the model meet P3?

**No.** The plant still assumes achieved breeding. P2 requires TBR calculated from its blanket configuration; P3 additionally requires that result, compared with a justified floor, to constrain blanket/build choices. A working research surrogate for a different assembly satisfies neither condition for the current plant. The rubric remains unchanged at `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`.

## What does it predict about breeding adequacy?

The current model does not yet predict achieved breeding for its actual blanket. Its two existing comparisons disagree under a particular recovery interpretation:

| Existing calculation | Result |
|---|---:|
| Supplied production | 1.074 |
| Existing fixed floor | 1.05 |
| Margin against that floor | +0.024 |
| Required production with 5% burn and 99% exhaust recovery | 1.190 |
| Margin against that conditional requirement | −0.116 |

At 5% burn, twenty atoms must be injected for each one burned; nineteen leave unburned. Losing 1% of those nineteen consumes another 0.19 atoms per atom burned. This calculation assumes complete extraction from the breeder and no inventory decay or stock growth. Those terms have separate meanings and must not disappear into an unexplained margin.

The 99% value originated in a costing assumption, not established physical tritium-recovery evidence. Therefore the negative margin is a **conditional deficit**, not proof that the real blanket is inadequate. Passing the old floor is likewise not proof of fuel self-sufficiency. [Balance diagnostic](evidence/threshold-check.json), [current implementation trace](evidence/current-trace.md).

## What remains and what comes next?

[AGENT] I recommend retaining the current helium/PbLi target and developing evidence for that actual build. Before integration, specify the breeder, coolant and structural fractions; enrichment; temperatures/densities; layer materials; and geometry/port treatment. Then reproduce independent benchmark cases, extend or replace the reduced model over the actual domain, and quantify transfer uncertainty. Source results used for fitting must not also count as independent validation.

A separately identified HCLL redesign is an alternative, but it changes build choices and still requires stellarator-transfer evidence. Reverting to the source Stellaris water/PbLi design is another material change with cooling consequences. The owner has been asked which physical target should govern the next round. The present source-backed research does not establish that any of these paths is impossible.

After that scientific boundary is resolved, the remaining deliverables are a native model work item, generated executable and verified integration pin, a focused plant study preserving failures and coupled plant quantities, and a fresh grade demonstrating both P2 and P3. None is claimed complete here. No reveal, replacement, merge or push occurred.

[Native research report](../../../../knowledge/research/pending/20260918-130310_computed-tritium-breeding-methods.md), [goal](goal.md), [trail](trail.md).

## Independent assessment

The fresh reviewer assigns **R2c.P1**, with P2 and P3 both unmet, against the unchanged rubric. The research round passes review as an accurately bounded result; that verdict does not certify breeding adequacy or goal completion. [Grade and round review](evidence/round1-review-and-grade.md).
