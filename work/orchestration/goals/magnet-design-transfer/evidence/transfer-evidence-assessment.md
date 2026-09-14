# Transfer evidence assessment

Coordinator assessment under T-006, 2026-09-13. This separates source support from the numerical study. The study result and fresh review will determine the final transfer claim; neither is credited here before completion.

## What the sources establish

- The reference material inventory is traceable to the corrected Stellaris Table 7 image: tape, external copper jacket, solder, steel and coolant occupy distinct fractions. The independent WI-040 audit accepts the correction and the explicit procurement account. Authority: `work/active/WI-040_winding-pack-mass-cost/design.md@a4d740d1` and `work/analysis/20260914-045431_audit_WI-040.md@0d077258`.
- The conductor paper supplies a relative field/current trend for measured tape at fixed temperature and orientation. It does not supply an installed winding-pack operating margin. Its visible 20 K measurements extend to approximately 24 T, below the inherited 24.9 T normalization point. Authority: `work/active/WI-038_conductor-grade-lever/basis.md@48417c9e` and `work/analysis/20260914-054500_audit_WI-038.md@aa3e1f3d`.
- The winding-operation term has an explicit historical source and dimensional basis. Its transfer to a nonplanar REBCO assembly remains an estimating assumption. A separately additive material term is defensible as a declared replacement estimate; it does not prove the old multiplier omitted those materials. Authority: WI-040 design and `evidence/accounting-research.md` in that item.
- The inherited tape price is an aggressive nth-of-a-kind target, not a qualified vendor quote at the normalization field. Its relative multiplier therefore estimates additional quantity at held unit economics, not a measured technology-price curve. Authority: the independent WI-038 audit's checked clean constants-file citation, `work/analysis/20260914-054500_audit_WI-038.md@aa3e1f3d`, Evidence limits and handoff.
- Prior geometry research identified specific missing inputs, not merely an absent numerical range. The source forms need configuration coefficients and a coil–plasma spacing factor that are unprinted for this machine; the implemented shapes absorb coefficients into reference anchors. The sister-code studies held configuration/aspect ratio fixed. This supports conditional anchored scaling, not arbitrary independent major/minor-radius qualification. Authority: `work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/spec.md`, Problem statement, MR-WI044-6 and Source basis; inherited by this goal's grounding references. No new geometry capability or source-derived bound is inferred here.

## What the numerical study can establish

[AGENT] At the fixed reference density, composition, temperature, shape factors and price assumptions, the study can check whether geometry, current and selected conductor envelope propagate consistently into sizing, field demand, mechanical screens and costs. Native execution and independent arithmetic checks can expose implementation errors or unexpected accounting responses. Agreement cannot validate the shared physical assumptions.

[AGENT] The selected field envelope is purchased capacity. Actual peak field is operating demand, tested against that capacity. Increasing the envelope need not increase the actual field. It increases estimated conductor quantity and pack size; this must not be described as a verified manufacturer-grade premium.

[AGENT] A field-envelope-only increase is expected to increase tape and external-material procurement while leaving composite-conductor length and the length-based winding-operation charge unchanged. That is coherent with the chosen estimating equation. It leaves the additional effort of winding a larger cross-section unpriced. The final claim must disclose that omission rather than call the unchanged fabrication charge a validated manufacturing response.

[AGENT] The tape account buys composite tape, while the four inventory accounts buy the external jacket, solder, steel and coolant fractions. That explicit boundary prevents deliberately re-pricing the tape's own substrate/stabilizer as external material. It does not establish that every inherited unit price is a pure raw-material quote: the steel price's upstream fabricated-steel wording remains ambiguous. The audited estimate discloses that uncertainty rather than certifying zero manufacturing overlap. See WI-040 `evidence/accounting-research.md` and `evidence/material-research.md`.

## Evidence still needed for an engineering-qualified transfer

| Missing evidence | Why the current study cannot supply it | Evidence that would resolve it |
|---|---|---|
| Configuration-specific geometry range | The live radius and coil-bore relations preserve anchored shape factors; a numerically valid radius is not an optimized or buildable coil set. | Coil configurations or independently validated geometry scaling over the proposed range, including coil–plasma spacing. |
| Absolute conductor operating margin | The exponent supplies relative tape performance, not the installed operating fraction, angular distribution, strain dependence or reference critical current. | Qualified conductor/cable data and an explicit operating-margin calculation at the relevant field, temperature, angle and mechanical state. |
| Pack/casing fit and structural adequacy | The pack-size response and casing estimate are not a geometric fit or detailed structural analysis. | Cross-section/layout and structural checks that couple the enlarged pack to its casing and supports. |
| Complete manufactured component cost | Insulation inventory, fixed cable additions and cross-section-dependent winding effort are not quantified; reference tape pricing is not a qualified high-field quote. | Consistent procurement and manufacturing evidence for the selected construction, without overlapping material or operation charges. |

These are [AGENT] sufficiency judgments derived from the audited scopes, not newly imposed owner requirements. The goal permits an inconclusive engineering answer with identified missing evidence. Implementing separate configuration or qualification capabilities is not part of the two-item scope.

## Historical findings touched

The current goal already touched `20260903-priced-levers#2`, `20260903-wall-and-heating#7`, `20260901-sustainment-fence#1` and `20260907-minor-radius#2`. Their latest pre-study rows still describe the initial specification/gate state. After the study reading, joined disposition updates must credit the audited work while retaining the remaining geometry, absolute margin and cost limits. Do not close these whole historical findings merely because the two implementations pass audit.

The current independent-comparison coverage also touches `20260911-model-owned-radius#3`: the package now has sixteen numeric outputs outside the oracle map, not the previously recorded seventeen. The 147 unsupported override keys remain explicitly unsupported. Update that declared seam with current evidence, without treating exact native checks as independent physical validation.
