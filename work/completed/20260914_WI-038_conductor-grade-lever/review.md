---
Verdict: pass
Created: 2026-09-13
Related Artifacts:
  Design: ./design.md
  Spec: ./spec.md
---

# WI-038 independent design critique

The proposed relative field multiplier passes design review for a conditional, fixed-reference engineering estimate. Both material corrections below were incorporated and independently rechecked. It does not establish a qualified conductor capability or a source-validated geometry/field transfer range. The coordinator's separate entering-consumer repair remains an implementation prerequisite.

## Evidence boundary

Fresh non-author review under `review-model`, dispatched by `evidence/design-review-prompt.md@ee10b495`. Reviewed spec, design, plan and basis at entering commit `22f851e3c77362bea737bd327bd6e06b3d337d61`; goal and T-004 scope; project MR-1–4 and AD-007/008; current magnet assembly, physical inputs and winding procurement/material equations; audited WI-040. No implementation or generated-package execution was performed. This is design readiness evidence, not the independent implementation audit.

Independently inspected the admitted Molodyk printed-page-5 rendering and extracted discussion, and Stellaris original Table 2, 7 and 8 images. No barred accounting document, sealed paper or comparison study was opened. Molodyk PDF SHA256 is `2925a09fba687fbcf37d86bada14da7a0925e63a207b932650311de475f97f9b`, matching the registered raw source. The inspected `/tmp/wi038-molodyk-page5.png` has SHA256 `31e1ba24dbc5fa0a65199f87f3cbe855231466fb4d61b99187f009b560302d2c`; it is a convenience rendering. Source-image SHA256 values are Table 2 `a54b61528687bb4554d2c6ff9d02bb6b8486ece711004faf5de182da54d9d102`, Table 7 `12b5ef816b3da1f8d744cf0136108f6ff7c46180523bbf2455792e04e034efdd`, Table 8 `560427a71a6af9027d9f6c158a143ffb8dd2e1eb6c7f0fe95fa0ffbaed46d51e`. Their paths are recorded in `basis.md`.

## Material findings

### R1 — Pair the reference density and economic basis

**Concerns; correct before implementation.** The design equations at `design.md:28` price envelope changes coherently only while the reference density is held fixed. Existing `j_wp` remains independently settable (`models/designs/stellarator_09/stellarator_plant.sysml:379`), but the supported-use list does not hold it fixed (`spec.md:34`). With the source composition held, tape volume is proportional to `q / j_wp`, whereas tape procurement is proportional to `q`. Halving `j_wp` at fixed current, geometry and envelope therefore doubles tape volume without changing tape procurement. This changes the implied price per volume of the same composite tape and cannot be represented as a fully priced same-technology transfer.

The mismatch follows directly from sizing and inventory bindings in `models/library/cost_structure/mfe_power_core.sysml:190` and `:238`, and the independent inventory/procurement equations in `models/library/analyses/mfe_winding_pack_cost.sysml:4` and `:42`. It is not cured by checking only envelope perturbations or preserving the baseline.

**Recommended correction:** hold `j_wp = 118.8271604938272 A/mm²` fixed for the supported priced-transfer claim. Keep its existing calibration interface and arithmetic behavior, but state that independent changes require a separately justified reference price/inventory basis. Hold the economic reference field, composition and coil-set distribution factors fixed as well. Propagate this condition into the spec, design, basis, plan and eventual study protocol. Add an explicit verification obligation that the priced study does not vary this reference density; optionally characterize an independent density perturbation to demonstrate why it is outside the claim.

**Alternative assessed:** the coordinator proposed an additional fixed `j_grade_ref`, with total quantity `q * j_grade_ref / j_wp` and effective price proportional to that total. This restores constant implied price per tape volume algebraically. It is defensible as an explicit constant-unit-tape-price inventory assumption, not as a sourced density/performance relationship. Independent `j_wp` then changes tape loading and operating fraction at a fixed envelope; it cannot simultaneously retain a fixed operating-fraction interpretation. The bounded fixed-density route is sufficient for this item's geometry/current/envelope comparison and avoids introducing that additional engineering premise.

### R2 — Correct the 15 T interpretation and retain the high-field uncertainty

**Concerns; correct before implementation.** `spec.md:32` says that below approximately 15 T the source's high-field interpretation is unsupported. The inspected Molodyk p. 5 instead states pinning-force saturation near 15 T at 20 K and gives an approximate current-density exponent of 0.6 without identifying its fit interval in that paragraph. Saturation is not evidence for a lower validity boundary. Since pinning force is proportional to current density times field, exact saturation would imply a different local high-field slope from a continued exponent of 0.6. These are approximate source observations; the design must not silently resolve their relationship into a validated extrapolation.

**Required correction:** remove the unsupported lower-bound statement. Describe 20–30 T as an agent-selected sensitivity window, with the 24.9 T normalization already beyond the inspected 20 K measurements. State that the approximate exponent does not establish its own validity over that window. The source-register caveat at `knowledge/SOURCE_INDEX.md:257` carries the same lower-bound premise and needs a narrowly scoped correction by its owner.

The proposed calculation may still be used for conditional sensitivity. No alternate exponent or missing critical-current relationship should be invented to make it a qualified capability model. If the later goal requires an affirmative engineering claim beyond that conditional estimate, the source limitation remains evidence for an inconclusive answer or further admitted research.

## Assessment of the remaining design

- **Ownership and accounting: pass for the proposed scope.** A magnet-owned calculation combines coil economics and pack facts without a cycle. Live sizing receives effective density and live procurement receives the effective tape rate. Non-tape procurement already receives the enlarged volume and must not receive a second quantity multiplier. Existing CAS rollup and comparison channels remain distinct. This fits MR-3 and AD-007/008.
- **Physical consequences: pass as conditional identities.** At fixed reference density, composition, current, length and temperature, the proposed equations give volume and tape/material procurement proportional to `q`, side proportional to its square root, and the inherited stress/strain operands inversely proportional to that square root. Casing mass and field demand remain unchanged because their present formulas do not consume pack side. This exposes an inherited fit/configuration limitation; it does not validate casing clearance or structural adequacy. Cryogenic cost must be checked through its existing nonlinear chain, with extra cold volume distinguished from pack volume.
- **Reference economics: concerns already disclosed, not a new blocker.** The inherited $50/kA-m input has no demonstrated 24.9 T vendor rating. The proposed normalization is an explicit economic calibration assumption. Equal tape construction and unit procurement economics support a relative quantity estimate; baseline equality cannot validate absolute price. Original Table 7 confirms 9% tape, 35% copper, 12% solder, 36% steel and 8% helium. Original Table 8 contains its own operating-fraction and graded-tape results, but importing those into this relative model would require a separate reconciliation and is not warranted by the selected exponent.
- **Verification: adequate after R1/R2 are carried.** Exact 174-channel/18-verdict neutrality, independent wrapper/domain checks, crossed operating-field/envelope cases, live/legacy separation and fresh generation address implementation risks. Expected ratios must freeze all relevant references. A change in actual peak field at fixed envelope verifies demand/capacity separation; it is not an assertion that current or geometry changes leave other quantities fixed. Numerical success must remain separate from conductor qualification in public study findings.

## Dispositions and next step

[REVIEWER CORRECTION, 2026-09-13] Retracted the DOI locator finding after independently verifying the [publisher record](https://www.nature.com/articles/s41598-021-81559-z): the registered `81559-z` identifies this title, authors and Scientific Reports 11:2084; the original finding misread the rendered character.

[AGENT, coordinator decision communicated 2026-09-13] Choose fixed reference `j_wp` for the priced-transfer claim; keep it as a calibration/arithmetic input outside that claim. Vary geometry, current and selected envelope; any exponent sensitivity is an explicit scenario assumption. Remove the unsupported 15 T lower validity boundary and retain 20–30 T solely as a sensitivity window. This is delegated coordinator judgment, not an owner-originated settled requirement.

**Targeted recheck, 2026-09-13: PASS.** R1 is resolved in the spec's supported-use boundary, design's interface and verification sections, basis derivation and plan's explicit protocol assertion. All freeze the reference density, economic reference field, composition and shape/distribution factors for priced transfer. R2 is resolved across the four native artifacts and the narrowed source-register caveat. The 15 T lower-bound assertion is removed; the unreported fit interval and conditional 20–30 T sensitivity remain explicit. The equations and two-input/three-output ABI are unchanged. No wider review restart or model execution was needed for these documentation repairs; scoped diff whitespace checks passed.

The rechecked artifacts were uncommitted working-tree revisions over the entering baseline. SHA256: spec `24a81ad0203325e7dfd375f5de28d254e38f00d0dbcc8bcd58364c71e82e2da2`; design `e314aeaecdc027e1baa1961123fe2c4d36bf2f0a03d6ad592cf45cad95417cbf`; plan `38d15873a6a3c0034ee6f39b39e17cdd2852ea06909b396d5826a50017f0eae9`; basis `d8b5f58cd73992d35ee6bd7f714bb102c7af21c6627e2431e4dddeb2a8dfa665`; source register `9c30d0bb4d8d507908a7f935e9344e3b6985c87fea48fd3f8049cb7183bc2562`.

Proceed to implementation after the coordinator's separate baseline-consumer prerequisite is cleared. The listed implementation checks and independent audit remain required. No model or implementation-file changes were made by this reviewer.
