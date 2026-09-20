# WI-077 implementation plan

[AGENT] Binding proposal and acceptance contract are in spec.md; independent pre-implementation approval is goal evidence/architecture-review-r2.md. Root owns this processor repair and integrated acceptance.

- [x] Replace demand-multiplier capacity binding with independently supplied kg D+T/s per-module rating in native source and twin.
- [x] Separate capacity adequacy and source-price applicability; expose margin/defined values and add the active-instance constraint.
- [x] Implement normative seed and independent current oracle; preserve historical seeds and packages.
- [x] Validate component units, invalid inputs, zero demand, module scaling and source conditions (172 tests in evidence/component-tests.log).
- [x] Regenerate and execute native insufficient/sufficient, fixed-rating demand changes and unsupported-price conditions (WI-075 integration/native-magnet-processor.log).
- [ ] Complete affected regression migration and independently review final integrated evidence.

The explicit selected rating is 0.00015 kg D+T/s per module. Entering price was demand-matched; current price differs because it uses this independent engineering assumption. Capacity adequacy and source validity remain separate. No price or constraint result was tuned against comparison data.
