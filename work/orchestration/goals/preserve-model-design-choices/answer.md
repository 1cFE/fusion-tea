# Preserve model design choices — current technical answer

[AGENT] **The expanded technical goal is met.** Round 2 repairs the equipment-price and capability gaps the owner made mandatory after accepting Round 1. Independent [final review](evidence/round2/final-review.md) is PASS. [OWNER] Accepted and formally closed on 2026-09-20: “ok accepted, please close”. All stated modeling limits and adverse engineering results remain attached to the accepted result.

## What changed

- **Equipment prices follow the chosen purchase.** Turbine, heat-rejection, cryoplant, power-supply and divertor costs now use supplied package amounts. Other affected allowances use independent procurement classes. Electrical-plant cost uses its selected gross-power rating. Operating demand no longer silently selects these purchase amounts.
- **Thermal requirements are checked against supplied ratings.** Primary and intermediate loops, steam equipment, cooling-water equipment, refrigeration and represented electrical loads have explicit capacity comparisons. The existing intermediate-exchanger area margin is now a native assertion. The repair adds 33 asserted predicates, for 67 total.
- **Calculated loads reach downstream equipment.** Six native perturbation cases demonstrate plasma heat reaching the cooling/steam/rejection chain, cryogenic loads reaching refrigeration/electrical checks, and heating, breeding and divertor verdicts remaining connected. Equipment ratings and purchase amounts remain fixed during those demand changes.
- **Round 1 choices remain preserved.** Supplied magnet geometry/inventory/masses, facility geometry/allocations, processor throughput and cooling purchase points/stocks survive evaluation. Accepted Round 1 evidence remains at its original checkpoint and under [the prior review](evidence/final-review.md).

A capacity pass means the represented requirement is no greater than the supplied rating at supported conditions. A changed or unsupported operating state gets no affirmative capacity credit. Raw capacity margins remain strict; the small floating-point allowance for identifying an otherwise identical state never relaxes capacity.

## Evidence and interface

The current interface has 704 public inputs, 1,352 numeric outputs, 68 structured outputs and 67 predicates. Round 2 adds 118 inputs and retires 11; all current inputs have actual consumers across 1,121 direct edges. The [migration and coverage receipts](../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/interface-migration.md) preserve exact identities. Historical packages and old study axes are unchanged.

- All ten native integration gates pass and return CANDIDATE at implementation checkpoint `fce788412fa53384688642dbc7deee9ee66431f2`. [Retained integration evidence](../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/seam-retention.json) maps original scratch paths to hashed durable copies.
- Current model regression evidence reconciles to **2,738 passed, 13 existing skips and one existing expected historical CLI failure**, with no unresolved failure/error. The initial broad run had 83 failures and 47 setup errors; all 130 exact nodes are accounted for by corrections and reruns. This is composite evidence, not one clean initial sweep. [Validation accounting](../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/validation-summary.json).
- Stock-route evidence reconciles to 704 passing checks. Native and independent calculations agree for all 1,352 baseline numeric channels and all 67 predicates. All 1,095 prior non-cost numeric channels are exactly unchanged. Focused tests cover insufficient/sufficient offers, unsupported conditions, fixed hardware under changing loads and all forty administrative flags.
- Fresh native generation with 52 normative manual bodies reproduces exactly on a second generation. Source/package identities are bound to the committed integration return. The seam checks its declared 112 scalar channels and all 67 predicates; the 1,352-channel numeric comparison is separate development evidence.

## What remains assumed

The supplied package amounts and ratings describe hypothetical offers. Their captured defaults are assumptions, not vendor quotations. Increasing a rating while retaining its price describes a different assumed offer; the model does not predict the price of that upgrade.

Capability checks cover declared operating points. Full pump/compressor/refrigerator maps, complete heat-sink allocation, tower/site qualification, pressure design and detailed electrical qualification remain absent. Equipment qualification flags do not claim those omissions are resolved. Plasma transport, bounded breeding interpolation and divertor heat descriptions retain their existing physical approximations. Vacuum pumping hardware and offered active fuel/tank inventories remain unmodeled. The complete current interpretation is in [residual dispositions](../../../active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/residual-dispositions.md).

The baseline still fails six engineering screens: facility occupancy, divertor heat, breeding, conductor current, winding fit and the new cooling-water electrical rating comparison. The last margin is `-3.552713678800501e-15`; native and independent arithmetic both retain that strict failure. Passing verification means the calculations and verdicts agree, not that the plant is adequate. Existing conductor validity limits remain unchanged.

Existing integration tooling does not execute `assert_read_set_covered`; the ten-gate result does not prove read-set completeness. Generated float-as-Boolean warnings remain visible. The historical CLI expected failure is disclosed separately from current equipment acceptance.

## Exact identity and disposition

- Pre-reveal code baseline: `86712a0d080d745802c1bcc57a30d3eca00458c3`.
- Accepted Round 1 implementation: `b11567eb693a4fd6f45a487f75dc5244fb433774`.
- Round 2 implementation/integration checkpoint: `fce788412fa53384688642dbc7deee9ee66431f2`.
- Candidate pin: `b60bcb940398d1df39bf779394ebab46ea309e31e8c00034d3dedee39832c9d3`.
- Semantic fingerprint: `6f51a9963348754694563855957d9bf9bfdfb90c61bd9228c9bd8868286fac90`.
- Executable fingerprint: `1ba8c423983518416d4320155f465f88a37f37456d73b0b6e4cf73b5050900c9`.
- Checked TEAx revision: `8d877460ac4f6f264561d916e40c1708adb13397`.

The delivery-record commit retains final reviews, evidence and status without changing the integrated model/package bytes. The pre-checkpoint review's final PASS text was written after its earlier draft had been staged; it is retained in the delivery record, with final checkpoint review separately binding the committed implementation. This is post-reveal repair from pre-reveal code. No reference comparison, reference-derived tuning, replacement freeze, push or merge was performed.
