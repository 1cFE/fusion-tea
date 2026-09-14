# WI-038 source and interpretation basis

## Verified source facts

[SOURCE] Molodyk et al., Scientific Reports 11:2084 (2021), reports a critical-current field dependence proportional to field raised to approximately −0.6 at 20 K and −0.7 at 4.2 K. The original PDF's printed page 5 was image-checked by coordinator and author (`/tmp/wi038-molodyk-page5.png` is a convenience rendering, not the durable source). The page also reports pinning-force saturation near 15 T at 20 K. Durable authority: `knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf`, printed p. 5; extracted discussion in `output.md`. The registered source record and its original PDF take precedence over transcription or a mistyped DOI.

[SOURCE] The paper's measurements describe tape performance under perpendicular applied field, with 20 K results through 20 T; they are not winding-pack current densities. Its abstract/result values exceeding 1000 A/mm² do not replace the installed pack's roughly 119 A/mm². See the same source's Fig. 1 and `output.md:51`. No absolute 80% operating-current fraction is established by the selected exponent.

[SOURCE] Stellaris Table 8 provides the existing coil-current/cross-section anchors; the current baseline has `j_wp = 118.8271604938272 A/mm²` from 15.4 MA and 0.36 m. The chosen field envelope is 24.9 T from Table 2. Sources: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_022_table_0.png` and `images/page_002_table_0.png` in that directory. Preserve the existing calibrated current-density value.

[SOURCE] WI-040 corrected Table 7's material fractions to 35% copper, 12% solder, 36% steel, 8% helium and residual 9% composite tape. Use its audited basis and `images/page_021_table_0.png`, not the historical priced-levers research's incorrect insulation-heavy transcription.

## Agent-derived model and price interpretation

[AGENT] At fixed temperature, tape construction, angle and operating fraction, usable current per equal tape area follows the selected relative field law. Maintaining current at a higher selected envelope therefore requires the inverse current-density ratio: `q = (B_design / B_reference)^field_exponent`. This is a relative conductor-quantity multiplier, not evidence that a manufacturer sells a distinct grade at that price.

[AGENT] Holding the pack's tape volume fraction fixed makes total pack area and volume increase by q at fixed coil current and length. The effective pack current density becomes `j_reference/q`; multiplying the reference tape procurement rate by q then prices the increased tape amount once. This assumes unchanged tape thickness and per-unit-tape procurement economics. Increasing non-tape material volume by q is a packaging/support assumption, not a result from Molodyk's tape experiment.

[INHERITED] The existing `coil.cost_per_kAm` is an economic reference input, not a newly qualified vendor quote with documented temperature/field rating. [AGENT] Interpret it operationally as the reference rate at the inherited 24.9 T design anchor. The relative multiplier adds no evidence to that absolute cost basis. The source-graded model and the old ungraded comparison coincide at q = 1 by construction; their equality is not independent validation of absolute conductor price or field capability.

[AGENT] The 24.9 T anchor extrapolates above 20 T measurements. A 20–30 T sensitivity window limits the extrapolation being explored and remains conditional throughout because its reference is already extrapolated. Do not describe it as a source-validated operating range. Exponent changes are scenario assumptions, not a probability distribution or a fit uncertainty interval. Keep temperature fixed at 20 K in the conductor transfer study; arithmetic at another cryoplant temperature does not qualify that conductor.

## Alternatives considered

[AGENT] Selected-envelope sizing is preferred over sizing directly from actual peak field because it represents an installed design capability with a separately tested operating demand and avoids a geometry/pack feedback redesign. The existing peak-field verdict checks whether actual demand exceeds that envelope. A geometry point below its envelope retains its purchased inventory; it does not automatically buy fewer tapes.

[AGENT] A full `Ic(B,T,angle,strain)` surface and computed absolute field ceiling would require reference performance, operating fraction, angular treatment and mechanical coupling absent from this bounded evidence. A vendor-grade premium would need distinct procurement evidence. Neither is substituted for the relative quantity model.
