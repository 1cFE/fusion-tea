# Exact 48 kA capture verification

[INHERITED: accepted WI-098 design/configuration 81423599] The selected offer uses 48 kA, a 0.54 m winding-pack side, aspect ratio 0.19, 1.30 m cavity height and a 40/60 kW cold/intercept cryoplant. Independent arithmetic passes 93 relevant numerical channels at relative tolerance 1e-9. The executable check is `check_capture.py`; `capture-check.json` contains every expected value and exact input/capture hashes. No production numerical implementation is imported.

- Peak field is 23.904 T, within the conductor relation's retained 20–24 T domain. Current allowance is 54,687.355927 A, leaving 6,687.355927 A. Minimum local winding-fit margin is 0.004619457 m. Stress is 399.36 MPa and conductor strain is 0.0013312.
- The repriced magnet purchase is USD2025 2,614,323,601.574602. This independently sums tape, non-tape material, fabrication, support and insulation purchases. Winding escalation is 321.9/130.7; helium is repriced by 321.9/334.4. Other selected material rates are explicit USD2025 requotes, not inferred historical inflation corrections.
- At the declared 35.5 W/m³ winding heating and zero structure nuclear heating, cold duty is 27,730.308885 W and intercept duty is 41,189.504335 W. Their selected margins are 12,269.691115 W and 18,810.495665 W. Refrigeration electricity is 2.537567042 MW; direct lead/joint electricity is 0.048556634 MW. The cryoplant quote is USD2025 62,957,384.242174.

## Nuclear-heating authority

[INHERITED] The original Stellaris source describes neutron transport in its source geometry near 2700 MW fusion and reports average winding-pack nuclear heating of 35.5 W/m³. See `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md:1652–1716`. Its local-temperature analysis remains deferred. The retained model treats this heating as an independent supplied value; it has no fusion-to-heating scaling equation.

[AGENT] A chosen fusion ceiling of 2652.5632625175904 MW does not prove that 35.5 W/m³ bounds the enlarged magnet/casing. The old WI-059 cryogenic basis also explicitly leaves case/support nuclear heating unbounded by its sources (`work/orchestration/goals/magnet-coil-realism/evidence/T-005_cryo_basis.md:66`). This check certifies arithmetic and local capacity under the stated heat assumption. It does not certify transport, global manufactured fit, the recalculated plasma operating point or a conservative nuclear envelope. Source and transport qualification remain zero. The coordinator is reviewing an amendment to expose uncertain heating and propagate it through cryogenic, auxiliary-rejection and electrical checks.

## Execution

`.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/check_capture.py` returns `pass 93 []`. The full capture and its failed full-plasma predicates remain at the sibling `magnet-capture/` evidence directory; those results have not been altered.
