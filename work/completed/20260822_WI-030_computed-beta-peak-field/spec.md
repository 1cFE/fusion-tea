---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-08-21
Updated: '2026-08-22'
---

# WI-030: Computed Beta and Conductor Peak-Field Limit (Stellaris)

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — this is a stellarator-demo model-development item. The ARIES-CS hold-out is sealed; the § 3 barred paths must not be read, cited, or opened. ARIES-CS is the one public LTS stellarator design with costing and is exactly what a second-magnet-arm search would reach for. Admissible sources: the Stellaris sources under `knowledge/concept_research/09-qi-stellarator-hts/iter-01..03/sources/**` minus the barred entries, with the published paper's PDF and page images as the authority for table values (`knowledge/SOURCE_INDEX.md:179-189`); 1costingFE (`/home/reid/1cfe/1costingfe`, pinned `0254385`) for engineering ceilings and costs.

**Why this item exists.** RUN-STUDY Item 6 (`.project/active/run-study-first-consumer/`) runs a magnet-technology A/B (HTS REBCO at 20 K vs LTS Nb3Sn at 4.5 K). In the model today that comparison is dishonest: on-axis field `B` enters only the magnet cost (`mfe_magnet_cost.sysml:246-249`) and beta is a bound input (`stellarator_plant.sysml:828`), so a lower-field LTS arm costs less and loses nothing, and nothing objects to a conductor carrying a field it cannot hold. Research (`.project/research/20260821-141439_item6-ab-candidates.md` § 2–3) found the smallest honest repair: compute beta from the profiles the model already has and `B`, and add a peak-field-on-conductor constraint. **[OWNER 2026-08-21]** Item 6 pauses; this change runs here, through the modeling PM; Item 6 resumes on the regenerated package.

## Overview

Add two library elements and wire them into the generic MFE plant and the Stellaris instance: a `'Volume-Averaged Beta'` calc that derives `<beta>_V` from the peak densities, peak temperatures, profile exponents, and on-axis field; and a `'Conductor Peak Field Limit'` constraint asserting `B_axis × peak_ratio ≤ B_max`. The bound `beta = 0.0276` is retired as an input and kept as a doc cross-check. Regenerate the package, re-pin the study manifest and fixtures, extend the oracle, and leave both test suites green.

## Goals & Context

**Research questions served:** RQ-1 (magnet cost is the dominant CAS22 driver; this item makes the field a physics lever, not only a cost term), RQ-5 (the B–beta–fusion-power coupling is high-sensitivity and its omission is the current model's largest silent assumption for any field-dependent study).

**Epic context.** Epic Item 4 ("Codegen + Viability Sweep", `work/backlog/epic-mfe-cost-modeling.md:128`) is half done: constraint predicates now execute (WI-027, SV-033), but the viability set compares two bound inputs. This item converts one of them (`beta_ok`) into a verdict that responds to design levers and adds the first conductor-technology constraint. It is the policy's "internalize and retire the axis" move (`modeling_project/STUDY_POLICY.md` § 2.3, § 3 row 3) and the R1 rung of its cycle ladder (§ 4: conductor feasibility "enters as an inequality, not as a solve").

**Insights.** No DI-XXX in `knowledge/KNOWLEDGE.md` covers MFE beta or conductor limits; DI-002 (CAS22 is the divergence point) is the structural frame. A DI for "B enters physics through beta, not only cost" is a candidate insight at close.

**Decisions carried in (do not reopen):**
- **[OWNER 2026-08-21]** REBCO arm `B_max` is bound at **24.9 T**, the field Stellaris designs to (Table 2 image), not 1costingFE's 23.0 T engineering ceiling (`defaults.py:611`). The disagreement is disclosed in the binding's doc.
- **[OWNER 2026-08-21]** No fallbacks: every new bound value is sourced from the Table 5 / Table 2 images or 1costingFE at the pin, or it is not bound.
- **[OWNER 2026-08-21]** No coil nuclear-heating budget constraint and no shield re-sizing in this item (research § 3: satisfied in both arms at this build; no discriminating power).

## Current State

- `models/library/analyses/mfe_plasma_scaling.sysml:132-219` — `'DT Fusion Power'` integrates Bosch-Hale over `n(ρ) = n0(1−ρ²)^α_n`, `T(ρ) = T0(1−ρ²)^α_T` (handwritten rung). B is absent. The `u = 1−ρ²` substitution documented at `:142-143` is what makes the volume average of `n·T` closed-form: `<n T> = n0 T0 / (1 + α_n + α_T)`.
- `models/library/analyses/mfe_viability.sysml:40-58` — `'Beta Limit'` compares `beta_in ≤ beta_limit_in`, both bound at the instance.
- `models/library/analyses/mfe_magnet_cost.sysml` — the only consumer of `B`.
- `models/designs/generic_mfe/mfe_plant.sysml:282-289` — `magnet_cost` reads `magnet.B`, the idiom a beta calc reuses; `:792-799` the two plant-level asserts.
- `models/designs/stellarator_09/stellarator_plant.sysml:90-148` — magnet bindings and the B-vs-peak mapping trap (24.9 T peak on the winding, 9.0 T on axis); `:385-446` profile referents (`n_e` vol-avg 3.17e20 reference-only in profile mode, `n_D0 = n_T0 = 1.96e20`, `T_i0 = 14.63`, `α_n = 0.33`, `α_T = 1.19`); `:826-834` bound `beta = 0.0276`, `beta_limit = 0.05`; `:874-877` `assert constraint beta_ok`.
- `exploration/stellarator_e2e/models/` — byte-identical twin of the 14 MFE files (`tests/models/test_model_family_spines.py` enforces); both homes change together.
- Generated package: `exploration/stellarator_e2e/generated/`, runtime contract 2.0.0, sealed `bf480f68…`; `studies/manifest.json` pinned to it; `tests/study/data/*` known answers bound to its semantic fingerprint; `oracle_entry.py` maps 52 oracle outputs and the five constraints' operand bindings.
- Codegen envelope (stellarator-model-migration, `models/stellarator_migration_ledger.md` header): executable expressions use `+ − × ÷ **` only; no function invocation; defaulted formals declared after bound formals. Constraint predicates admit arithmetic operands (research cites `sysml-codegen predicate_compiler.py:52,160-174`) — to be confirmed in this item's first hour (risk R1).

**Known issue this item fixes:** `beta_ok` is an input check, not a verdict; `B` has no physics role.

## Modeling Requirements

#### MR-WI030-1: Beta is computed, not bound
**Type:** Functional | **Priority:** P0 | **Source:** policy § 2.3 / § 3 (owner-ratified 2026-08-21), research § 2a
The model SHALL compute the volume-averaged beta as `beta = 2 μ0 Σ_s [n_s0 T_s0 e_keV / (1 + α_n,s + α_T)] / B²` over the species {electrons, D, T, He} with the model's own peak densities, peak temperatures, and profile exponents, and `beta_ok` SHALL read the computed value. The bound `beta = 0.0276` SHALL no longer be an entry point; it remains in the instance doc as the printed cross-check.
**Rationale:** the only way a field or density lever reaches the beta verdict.
**Validation:** the computed beta at Point A reproduces the Table 5 image's printed 2.76 % within ±3.5 % (research: 0.0283 or 0.0267 depending on the helium exponent; the design picks one and records the other as the tolerance); Point B (Table 5: 2.81 %) within the same band; `beta` absent from `contracts/model_contract.json` parameters; a `beta_calc__beta` output channel present.

#### MR-WI030-2: Conductor peak-field limit is an executing constraint
**Type:** Functional | **Priority:** P0 | **Source:** policy § 4 R1; research § 2b
The model SHALL assert `B_peak ≤ B_max` as a viability constraint (`'Conductor Peak Field Limit'`, local identity `peak_field_ok`) beside the existing five, where `B_peak = B_axis × peak_ratio` is forward-computed by a library calc (`'Conductor Peak Field'`), `peak_ratio` is a bound geometry fact (Stellaris 24.9/9.0, bound as its float64 value `2.7666666666666666`, Table 2 image) and `B_max` a bound conductor ceiling. *Amended 2026-08-21 (design, ratified by owner via `/_my_ask_me`): the spec's original single predicate `B_axis × peak_ratio ≤ B_max` compiles on the pinned codegen but `scripts/study/indicators.py:469` and `verify.py:193` cannot parse an arithmetic operand, so the calc-then-compare shape is required; `2.7667` would read `24.9003 > 24.9` (violated) at the design point.*
**Rationale:** an LTS arm at the Stellaris field must be rejected by the model's own verdict, not by a hand rule in the study.
**Validation:** six constraints in the catalog; at the Stellaris point `peak_field_ok` is `satisfied` with margin 0.0 (24.9 ≤ 24.9 by the owner's binding) and at `B_max = 13.0` it is `violated`; `B_peak` is a calc output channel (`peak_field_calc__B_peak`) and the six constraints parse in `scripts/study/indicators.py` and `verify.py` (amended 2026-08-21; see MR text).

#### MR-WI030-3: Library stays concept-agnostic; values live in the instance
**Type:** Constraint | **Priority:** P0 | **Source:** MR-3
The calc def and constraint def SHALL carry no concept values; `μ0` and `e_keV` are defaulted inputs declared last with citations; all species peaks, exponents, `peak_ratio`, and `B_max` SHALL be bound in `stellarator_plant.sysml`. `generic_mfe/mfe_plant.sysml` SHALL wire the calc from `magnet.B` and the plant's profile attributes so a second MFE instance binds values only.
**Validation:** grep: no numeric literal other than the two defaulted constants in the new library defs; `mfe_plant.sysml` carries no Stellaris value.

#### MR-WI030-4: Every new value sourced (no fallbacks)
**Type:** Traceability | **Priority:** P0 | **Source:** MR-4; **[OWNER 2026-08-21]** no-fallbacks
Every new bound value SHALL carry `Source / Ref / Basis`: `n_e0 = 5.06e20`, `T_e0 = 15.40`, `n_He0 = 0.56e20` (Table 5 image Point A); `α_n,e` derived from the printed vol-av/peak pair 3.17/5.06 = 0.596 (derivation in the doc) or the fuel exponent 0.33, per the design's choice; `peak_ratio = 2.7666666666666666` (= 24.9/9.0 in float64, Table 2 image; amended 2026-08-21); `B_max = 24.9` (**[OWNER]**, Table 2 image; doc states the 1costingFE ceiling 23.0 T at `defaults.py:611` and that the design value was chosen). Nothing is bound from a typical-literature value.
**Validation:** citation-by-citation read at audit; every Ref resolves to an image or a pinned upstream line.

#### MR-WI030-5: Regenerate, re-pin, and keep the study capability green
**Type:** Constraint | **Priority:** P0 | **Source:** Item 6 design Architecture table (the interface Item 6 resumes on)
After the model change the item SHALL: regenerate the package on the pinned codegen (`8a758e92`) with zero readiness diagnostics at runtime contract 2.0.0; re-pin `exploration/stellarator_e2e/studies/manifest.json` (fingerprints, baseline point and headline, verdicts now six) and add `beta_calc__beta` to its objective catalog; re-derive `tests/study/data/*` known answers; extend `verify_stellaris.py` with the beta recompute and `oracle_entry.py` with the beta channel and `peak_field_ok` operand bindings; recapture `stellarator.snapshot.json` and `tests/models/data/mfe_census.json`; and leave `tests/study` and `tests/models` green with the IFE family untouched.
**Validation:** `preflight.py gates` 6/6 and `verify.py` `outcome: pass` on the regenerated package; the six names `n_e0`, `T_e0`, `n_He0`, `alpha_n_e`, `peak_ratio`, `B_max` resolve as entry points and `peak_field_ok` as a constraint id in `model_contract.json`; `uv run pytest tests/study tests/models` green.

#### MR-WI030-6: Headline moves only where physics says it should
**Type:** Quality | **Priority:** P1 | **Source:** SV-033 standing bars
At the Stellaris design point, LCOE, total capital, `p_net`, `q_eng`, `rec_frac`, and magnet capital SHALL be unchanged to the cent (beta is not in the cost chain; the new constraint is satisfied); the only headline change is the sixth verdict. The oracle bit-exact bar (rel 1e-9) holds on every executed channel including the new beta channel.
**Validation:** `AFTER_MIGRATION_RECORD.md` § 2 headline reproduced; verdict list = five satisfied + `peak_field_ok` satisfied.

**Promotion candidate (flag):** MR-WI030-3's "a viability limit on a technology-dependent quantity is bound in the instance and asserted through a library constraint def" is a durable pattern worth a PR-XXX after the tokamak instantiation exercises it a second time. Not promoted here.

## Scope Boundaries

**In scope:**
- `models/library/analyses/mfe_plasma_scaling.sysml` — new `calc def 'Volume-Averaged Beta'` after `'Neutron Wall Load'`
- `models/library/analyses/mfe_viability.sysml` — new `constraint def 'Conductor Peak Field Limit'`
- `models/designs/generic_mfe/mfe_plant.sysml` — plant attributes for the electron/He peaks and exponent; `calc beta_calc`; the assert moved to or declared at plant level if the pattern requires (design decides)
- `models/designs/stellarator_09/stellarator_plant.sysml` — bindings, `beta_ok` rewired, `beta` demoted to doc, `peak_ratio`, `B_max`, `assert constraint peak_field_ok`
- `exploration/stellarator_e2e/models/` twin (byte-identical), `generated/`, `stellarator.snapshot.json`, `studies/manifest.json`, `studies/oracle_entry.py`, `verify_stellaris.py`, `tests/study/data/*`, `tests/models/data/mfe_census.json`, `tests/models/test_model_family_spines.py` mutation rows if the new channel warrants one
- `modeling_project/VALIDATION_MATRIX.md` — SV-036 (created pending)

**Out of scope:**
- A confinement solve (ISS04) or any closure that makes T or n computed (policy § 4 R3; a later round)
- Coil nuclear-heating budget, shield re-sizing, Nb3Sn winding-pack volume (**[OWNER]**; research § 3)
- The A/B study itself, its arms, windows, and record (Item 6)
- `handshake_1costingfe.py` (P3 backlog row; it cannot run on the 2.0.0 package regardless)
- The IFE models and package

## Success Criteria

**Functional**
- [x] `'Volume-Averaged Beta'` and `'Conductor Peak Field Limit'` exist in the library with MR-4 docs; wired in `mfe_plant.sysml`; bound in `stellarator_plant.sysml`
- [x] `beta` is no longer an entry point; `beta_calc__beta` is a channel; `peak_field_ok` is the sixth constraint

**Quality**
- [x] `uv run agentic-mbse validate models --level 1` passes; Levels 2 and 6 offender list unchanged from the migration's (zero introduced)
- [x] Generation: exit 0, zero readiness diagnostics, `runtime_contract_version 2.0.0`
- [x] `tests/models` and `tests/study` green; IFE census and anchors unchanged

**Verification (SV-036, pending)**
- [x] Computed beta at Point A within ±3.5 % of 0.0276 and at Point B within ±3.5 % of 0.0281 (Table 5 image), oracle bit-exact rel 1e-9
- [x] Design-point headline unchanged to the cent; six verdicts, all satisfied, `peak_field_ok` margin 0.0
- [x] With `B_max = 13.0` and `B = 9.0`: `peak_field_ok` violated; with `B = 4.69`: satisfied (margin +0.024) and `beta_ok` violated (β = 0.0988) — the two verdicts that make Item 6's LTS arm honest. *Amended 2026-08-21: 4.70 T gives `B_peak = 13.0033 > 13.0` (violated); the exact Nb3Sn ceiling on axis is 13.0 × 9.0/24.9 = 4.6988 T.*
- [x] `preflight.py gates` 6/6 and `verify.py` pass on the regenerated package with the re-pinned manifest

*All criteria verified 2026-08-21 at commit `ba5c9945`; evidence in `./verification_record.md` (SV-036).*

## Assumptions & Risks

1. **R1 — arithmetic in a constraint predicate.** *Resolved 2026-08-21 (design research, spike on the pinned codegen):* the predicate compiler admits it, but the study tools (`indicators.py`, `verify.py`) do not parse it. Resolution: `'Conductor Peak Field'` calc + plain comparison (design D1); the plant-attribute fallback was rejected because it would add a Level 6 offender.
2. **R2 — helium exponent choice.** The two defensible choices bracket the printed beta at −3.3 % / +2.5 %. Design picks one, records the other as the tolerance; neither is a fallback (both derive from the image).
3. **R3 — entry-point shape.** Plant-level attributes project one entry point each (post-migration convention); the twin and census must be recaptured together or the spine test fails. Mechanical.
4. **R4 — regeneration drift.** Every known-answer fixture is bound to the semantic fingerprint and fails first by design; re-derivation is a known procedure (migration Phase 3).
5. **A1** — `T_e0` and `T_i0` are separate peaks with one shared `α_T = 1.19` (Stellaris Fig. 16 fit applies to both per WI-022); if the design finds a separate electron exponent in the image it binds it, else shared.

## Traceability

**Source requirements:** Stellaris Table 5 image (`09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_009_table_0.png`): peaks, vol-av beta 2.76 % / 2.81 %; Table 2 image (`images/page_002_table_0.png`): 9.0 T axis, 24.9 T peak; `1costingfe defaults.py:596-619` `MAGNET_TABLE` ceilings (REBCO 23.0, Nb3Sn 13.0) — disclosed, not bound for REBCO; `mfe_plasma_scaling.sysml:141-146` profile forms.
**Downstream impacts:** Item 6 study 1 (resumes on the six names); `studies/manifest.json`, `tests/study/data/*`, `oracle_entry.py`, `verify_stellaris.py`, `mfe_census.json`; the demo epic's criterion-2 evidence (SV-033) gains a sixth verdict.
**Applicable PR-XXX:** PR-3 (pattern before production: the beta calc reuses the WI-022 profile pattern and the `magnet.B` read idiom), PR-5 (committed artifacts per phase). MR-3, MR-4 throughout.

## Related Artifacts

- Epic: `work/backlog/epic-mfe-cost-modeling.md` (Item 4 lineage)
- Item 6: `.project/active/run-study-first-consumer/{spec,design,align}.md`
- Research: `.project/research/20260821-141439_item6-ab-candidates.md`
- Sibling: WI-031 (research round; independent, runs in parallel)
- Design: `work/active/WI-030_computed-beta-peak-field/design.md` (to be created, `/design-model`)
- Plan: `work/active/WI-030_computed-beta-peak-field/plan.md` (to be created)
