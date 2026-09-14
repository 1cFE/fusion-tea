# WI-038 implementation evidence

The chosen field envelope now changes effective pack current density and tape procurement through the reviewed relative quantity relation. Existing sizing, material inventory and cryogenic equations consume the resulting pack geometry. Actual peak-field demand stays separate from the selected envelope; the existing peak-field verdict compares them. Both legacy ungraded cost paths remain intact.

Priced transfer holds reference density at 118.8271604938272 A/mm², reference field at 24.9 T, temperature at 20 K, composition and coil-set reference factors fixed. The approximate tape exponent does not qualify the engineering range. Independent changes to reference density remain outside the same-technology priced claim. The design/review explain why the 20–30 T sensitivity window is an agent-selected extrapolation, not a source validity interval.

## Verification to date

- `evidence/baseline-reconciliation.json`: all 174 entering outputs and eighteen verdicts preserved exactly, with three new outputs and 161 independent oracle comparisons at relative/absolute tolerance 1e-9. The reference still violates the divertor limit and still reports 142.50725862880648 dollars/MWh.
- `evidence/conductor-grade-tests.xml`: 41 component and public checks pass. Named wrapper outputs, deliberate input/result domains, envelope changes at fixed demand, demand changes at fixed envelope, procurement/volume identities and stress/strain/cryo consequences are exercised. A test initially confused emitted verdict IDs with short names; its lookup was corrected without changing numerical assertions or production behavior.
- Current oracle/consumer author reports 332 passes including 38 native consumer cases, plus exact preservation of old oracle values at reference and R14. Broader recorded model/study regressions are pending.
- Fresh stock generation is byte-identical using fifteen preserved and one new normative body. The public contract has 265 inputs and 177 outputs. Receipts, hashes and reproduction scripts are in evidence/.
- All six validation levels assessed: L1/L3/L4/L5 pass; L2 retains exactly ten diagnostic identities and L6 retains 249 occurrences/238 distinct identities. No diagnostic is added or removed (`evidence/validation-delta.json`). Failed inherited levels remain failed, not certified.

The first full model battery passed 886 tests with thirteen inherited skips and three failures. Two failures were old input counts; one was an incomplete cumulative source-hash receipt that omitted WI-040's unchanged predecessor files. Those guards and counts were corrected without changing model arithmetic. The failed XML is retained as `evidence/model-tests-before-consumer-fixes.xml`; the final battery and independent audit remain pending.
