# WI-077 implementation plan

[AGENT] Binding proposal and acceptance contract are in spec.md; independent pre-implementation approval is goal evidence/architecture-review-r2.md. Root owns this processor repair and integrated acceptance.

- [x] Replace demand-multiplier capacity binding with independently supplied kg D+T/s per-module rating in native source and twin.
- [x] Separate capacity adequacy and source-price applicability; expose margin/defined values and add the active-instance constraint.
- [x] Implement normative seed and independent current oracle; preserve historical seeds and packages.
- [x] Validate component units, invalid inputs, zero demand, module scaling and source conditions (172 tests in evidence/component-tests.log).
- [x] Regenerate and execute native insufficient/sufficient, fixed-rating demand changes and unsupported-price conditions (WI-075 integration/native-magnet-processor.log).
- [x] Complete affected regression migration and independently review final integrated evidence.

The explicit selected rating is 0.00015 kg D+T/s per module. Entering price was demand-matched; current price differs because it uses this independent engineering assumption. Capacity adequacy and source validity remain separate. No price or constraint result was tuned against comparison data.

## Final technical acceptance

[AGENT] Technical acceptance passed fresh non-author [final integrated review](../../orchestration/goals/preserve-model-design-choices/evidence/final-review.md). Native integration returned CANDIDATE at implementation commit `b11567eb693a4fd6f45a487f75dc5244fb433774`, with all ten gates passing. The broad regression sweep and complete reruns of its two corrected test files are accepted composite evidence; see WI-075 `integration/regression-accounting.json`. Scientific limits and the existing unexecuted read-set coverage check remain disclosed in the goal answer. This active record is retained for provenance; formal goal closure and archival remain owner-held.
