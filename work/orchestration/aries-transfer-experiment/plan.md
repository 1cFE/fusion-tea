# Test model reuse by transferring to ARIES-CS

[OWNER-VERBATIM] “I think it would be illustrative to see if our overall modeling had reusable components and such. As long as we keep a good log, this is an interesting test.” [OWNER] Requested a written plan, step-by-step execution, substantial subagent modeling work and a continuing log. [INHERITED] Prior instruction requests regular checkpoint commits. [AGENT] Treat this as an explicitly post-reveal transfer experiment. Target the original 1 GWe ARIES-CS reference first; do not select an easier point merely to obtain agreement.

## Questions and milestones

1. Which existing physical relationships, components, interfaces and cost calculations can be reused unchanged or by supplying a different configuration?
2. Which need source-definition mapping, supported-domain extension, replacement physics or added plant architecture?
3. What is the minimum evidence-backed change set to evaluate the design and its engineering checks? A violated check is a valid result; unsupported physics is not.
4. What additional work is required for comparable LCOE, including cost scope and financial conventions?

[AGENT] Count independent engineering changes, not edited files. For each, record the original capability, source requirement, reused definitions, changed bindings/equations/structure, supplied versus predicted quantities, validation, and remaining limits. Report a lower bound where source gaps prevent a complete count. A conditioned subsystem exercise can demonstrate component reuse, but not independent prediction of the supplied boundary values.

## Execution plan

- [x] Record authority, freeze original evidence and assign parallel inventory work; commit plan.
- [ ] Inspect existing physical and economic components; build a non-overlapping minimum-change register with dependencies and evidence gaps.
- [ ] Select source-supported, independently useful modeling increments; register native work items and record their requirements before implementation.
- [ ] Implement and validate ready increments through native SysML/executable consumers, using continuing subagent authors and separate independent review. Update the register/log and commit each completed group.
- [ ] Integrate demonstrated reuse and remaining changes into an assessment of the two milestones. Do not replace missing physics with reference outputs under an independent-prediction label.
- [ ] Review the combined claims, verify preserved original evidence, and publish a concrete status with completed work, remaining implementation and external data needs.

## Boundaries and decisions

[INHERITED: MR-7] Preserve supplied design choices and separate demand, installed capability and any design-selection policy. [AGENT] Existing ARIES evidence is authorized within comparison-specific artifacts and new explicitly post-reveal case models; do not silently calibrate shared generic behavior to match ARIES. Original frozen packages, results and comparisons are immutable. Shared changes require proportional regression checks; prefer a separate case assembly where semantically appropriate.

[AGENT] Reuse existing source/domain findings rather than redoing the archive search. Missing coil data and new neutronics evidence are external/scientific dependencies, not ordinary code fixes. Continue independently useful work while blocked components remain recorded. A static count alone is insufficient evidence of reuse where a native execution probe is possible. No push, merge, external author message or formal goal closure is included.

## Coordination

Physics inventory agent owns physics-inventory.md and physics-* evidence. Thermal/cost agent owns thermal-cost-inventory.md and thermal-* evidence. Coordinator owns this plan, the change register, log and native tracking/integration. Implementation ownership is assigned per item after inventory. Fresh reviewers assess relevant source, design or integrated claims without author history.
