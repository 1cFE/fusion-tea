# Learnings: Installed cooling equipment costs

## L-001 — Replacing cooling aggregates requires explicit installation and lifecycle boundaries

- **Evidence:** `evidence/account-boundary-map.md`, `evidence/accounting-preimplementation-review.md`, `evidence/final-review-and-grade.md` (new artifacts unpinned; no native digest until checkpoint).
- **Scope:** Current helium heat-transport and plant CAS/DCF implementation. Reactor installation and initial spares do not automatically cover cooling; equipment replacements are absent. Broader indirect/service allowances can overlap inclusive estimates.
- **Implication:** WI-067 must replace overlapping allowance scope and reconcile dedicated equipment with shared services and operating costs before adding prices.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-18.

## L-002 — Verified physical anchors do not establish installed equipment prices

- **Evidence:** `evidence/sizing-source-review.md`, `evidence/source-methods.md`, native REQ-COOL-INSTALL-01-CONT return and pending research (new artifacts unpinned; no native digest until checkpoint).
- **Scope:** Existing DEMO source geometry and the bounded acquisition performed here. Four relevant cost originals remain inaccessible; an acquired low-temperature method lacks demonstrated helium applicability. This is not literature exhaustion.
- **Implication:** Obtain original cost evidence and justify conceptual transfer across equipment, pressure, temperature, material and installation scope. A vendor quotation is one route, not the only route.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-18.

## L-003 — Current replay preserves selected cooling costs but changes the full-plant verdict

- **Evidence:** `evidence/starting-cases.json`, `evidence/entering-replay.json`, `evidence/final-review-and-grade.md` (new artifacts unpinned; no native digest until checkpoint).
- **Scope:** Four exact retained input scenarios, 23 selected historical/current cooling/economic comparisons each. Selected18/14 cases now fail breeding; r2 cases retain prior failures plus breeding. Not a claim of full historical output parity.
- **Implication:** Future matched equipment-cost studies must label the executable version and retain current breeding failures independently of cooling performance.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-18.

## L-004 — Original component methods now support a conceptual cooling estimate

- **Evidence:** Round2 `circulator-transfer.md`, `hx-method-check.md`, `new-source-review.md`, `candidate-review.md`; native registered source receipts. Reports unpinned; no native digest until checkpoint.
- **Scope:** Historical helium-machine references and finished nuclear stainless fabrication/installation methods support declared conceptual transfers. Pressure/scale/material and package uncertainties remain explicit, without a calibrated confidence band.
- **Implication:** Proceed through a concrete quantity/accounting/lifecycle design; recovery of the original four queued reports is no longer the only route forward.
- **Supersedes:** L-002's source-access-only next step, not its distinction between physical requirements and complete installed prices.
- **Accepted by:** Round2 review,2026-09-18.

## L-005 — Preserve source rating, price year and installation denominators

- **Evidence:** Round2 `circulator-transfer.md`, `new-source-review.md` and `candidate-review.md`.
- **Scope:** BNL50hp nominal pumping duty differs from140hp motor rating; its quote is December1978 despite the1979 report. ORNL installation is27%of hardware including procurement, while35%is engineering. Seider's descriptive compressor ratio statement is not its explicit equation bound.
- **Implication:** Use original images and component definitions; none of these quantities or factors may be silently interchanged in implementation. Preserve raw source amounts alongside any declared CPI comparison.
- **Supersedes:** Corrected provisional readings within Round2, as recorded in its reviews; no production parameter was adopted from them.
- **Accepted by:** Round2 review,2026-09-18.

## L-006 — Intermediate technology and allowance scope need an explicit decision

- **Evidence:** WI-067 `primary-candidate.md`, Round2 `candidate-review.md`, goal trail material-decision entry.
- **Scope:** Current primary helium is selected; the existing intermediate aggregate has no selected coolant or equipment bill. Reference HITEC terminals were a conditional thermal calculation, not an owner-selected plant architecture.
- **Implication:** Ask the reserved material technology question and then reconcile equipment ownership. Relabeling C220202 cannot establish that its cost excludes the newly priced exchanger. Keep total cooling and lifecycle amounts unresolved until that work is complete.
- **Supersedes:** none.
- **Accepted by:** Round2 review,2026-09-18.

## L-007 — Separate cooling equipment and lifecycle accounts meet the structural target

- **Evidence:** Independent `evidence/round3/final-review-and-grade.md`; reviewed modelc6906cbe; frozen study5b956a82; exact rubricdc0f0b6dc6512b29e1307da647f3a508a1f5356d.
- **Scope:** R7.S=3 for independently sized principal pumps/circulators, pipes and exchangers with declared installation, initial spares, replacement and routine-maintenance coverage. Both old aggregate cooling terms are replaced. This does not establish complete equipment scope, pressure qualification, S4 or another row's grade.
- **Implication:** The specific cooling structure/cost gap is closed technically. Carry residual scope and source-transfer uncertainty into downstream comparisons.
- **Supersedes:** Earlier S2 status as the current implementation assessment; earlier evidence remains historical.
- **Accepted by:** Round3 non-author review and final frozen-artifact assurance,2026-09-18.

## L-008 — Missing equipment cost dominates the matched economic change

- **Evidence:** Study5b956a82 retained-case mode comparisons and `evidence/round3/study-reading.md`.
- **Scope:** Selected18 LCOE150.429542→309.554789$/MWh from costing/lifecycle alone at unchanged net power; salt electricity and recovered shaft heat then give310.632663. Fixed per-circuit fabrication can outweigh reduced machine pumping duty when circuit count increases. Fourteen circuits is numerically cheaper but fails salt-machine price ranges; no optimum follows.
- **Implication:** Separate added scope from changed design or performance in any comparison. Lower estimated price does not establish equipment applicability or physical feasibility.
- **Supersedes:** None.
- **Accepted by:** Round3 non-author review and final frozen-artifact assurance,2026-09-18.

## L-009 — Layout and conversion interfaces remain material limits

- **Evidence:** Study5b956a82 layout/construction sensitivities and equipment flags; combined design; final independent review.
- **Scope:** Half/twice pipe length gives271.612338/388.673313$/MWh for the selected full scenario; walls and service lives are assumed. Primary inventory geometry exceeds the reference envelope. The retained480°C efficiency-fit argument exceeds465°C salt supply, so full-mode electricity uses a declared conversion surrogate. Auxiliary inventories/equipment and steam-generator price inclusion remain incomplete.
- **Implication:** A justified layout, design-pressure/material construction, auxiliary bill and physically consistent Row8 interface are concrete next steps for a more mature estimate. They are not silently commissioned or treated as negligible by S3 acceptance.
- **Supersedes:** None.
- **Accepted by:** Round3 non-author review and final frozen-artifact assurance,2026-09-18.
