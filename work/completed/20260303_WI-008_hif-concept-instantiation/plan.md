---
Status: complete
Created: 2026-03-03
Updated: '2026-03-03'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-008: HIF Concept Instantiation — Implementation Plan

## Source Documents

- **Design**: `./design.md` — primary; 7 design decisions, validated prototype, full parameter tables
- **Spec**: `./spec.md` — 11 modeling requirements (MR-WI008-1 through MR-WI008-11), 5 SV entries
- **Epic**: `work/backlog/epic-ife-cost-modeling.md` — Item 3 (final item)

## Design Summary

Three new files implementing the first concrete concept model: Meier's HIF cost formulas in library (`hif_economics.sysml`), an HIF Driver type definition (`hif_driver.sysml`), and an HIF plant instance with dual cost outputs — Hawker LCOE (inherited) + Meier COE (added). The design resolves the "driver energy" definition ambiguity (beam vs bank) and establishes the Meier→Hawker gamma bridge.

## Prototype Baseline

The design phase produced working prototypes that pass Level 1 validation:

| File | Location | Current State | Level 1 |
|------|----------|---------------|---------|
| `hif_economics.sysml` | `models/library/analyses/` | 4 calc defs with doc comments, Source/Ref/Basis citations, year-dollar basis | PASS |
| `hif_driver.sysml` | `models/designs/hif_ife/` | HIF Driver part def with 3 HIF-specific attrs, meier_cost calc, 4 inherited params set, EXPOSE pattern | PASS |
| `hif_plant.sysml` | `models/designs/hif_ife/` | hif_plant instance with all 14 Hawker params, Meier COE chain (3 calc usages), dual outputs | PASS |

```
$ uv run python -m syside check -Werror [all 11 files]
Checks passed!
```

**Assessment**: Prototypes are production-quality in SysML code. Doc comments are comprehensive with structured citations on every value. The remaining work is verification, formula cross-checking, and project artifact updates — not model code refinement.

### Level 4-6 Issues from Design

The design validation report did not identify specific Level 4-6 failures. The prototype was high-confidence from the start because all SysML patterns were validated during design. The work below therefore focuses on systematic verification rather than code repair.

## Phasing Approach

Two phases (review + verify), reflecting the prototype maturity. Phase 1 does a systematic code review and fixes any gaps. Phase 2 writes verification scripts, updates project artifacts, and closes the work item. Both phases are compact because the prototype is already production-grade.

## Validation Strategy

- **Per-phase**: Level 1 (`syside check -Werror`) after any file modifications
- **Final**: Levels 1-3 comprehensive, plus SV-011 through SV-015 formal verification
- **User review**: After Phase 2 (before closing), user reviews verification script output and VALIDATION_MATRIX updates

---

## Phase 1: Model Review & Refinement

### Overview

Systematic code review of all three prototype files against the design's element details, parameter tables, and cross-file binding specifications. Fix any doc comment gaps, verify formula constants against source documents, and confirm the import map matches the design.

### Design Reference

- See design doc "Element Details" for the four calc def specifications and verification targets
- See design doc "HIF Parameter Values (Osiris Baseline)" for all numeric values and sources
- See design doc "Cross-File Bindings → Import Map" for expected imports
- See design doc "Parameter Binding Table" for the 14 Hawker parameter mappings

### Prototype Baseline

- `models/library/analyses/hif_economics.sysml` — has 4 calc defs with doc comments. Review: verify formula constants match design doc Eq. references, verify year-dollar basis on all 4 calc defs.
- `models/designs/hif_ife/hif_driver.sysml` — has HIF Driver with 3 attrs, meier_cost, 4 inherited params. Review: verify all attribute values match design parameter table, verify EXPOSE patterns.
- `models/designs/hif_ife/hif_plant.sysml` — has hif_plant with all 14 params and Meier COE chain. Review: verify all 14 values match design "Parameter Binding Table", verify calc input bindings, verify target_factory_cost literal (0.1) has citation.

### Files to Modify

- `models/library/analyses/hif_economics.sysml` — REFINE (doc comments only if gaps found)
- `models/designs/hif_ife/hif_driver.sysml` — REFINE (doc comments only if gaps found)
- `models/designs/hif_ife/hif_plant.sysml` — REFINE (doc comments only if gaps found)

### Checklist

#### hif_economics.sysml Review
- [x] Verify `'Meier HIF Driver Cost'` formula constants: 0.32, 0.088, 1.25, 0.05, 1.0, 0.0088, 5.0 match Meier Eq. 5
- [x] Verify `'Meier Reactor Cost'` constants: 0.66, 1.67, 0.49, 0.72, 0.28 match Meier Eq. 3
- [x] Verify `'Meier Total Capital Cost'` constant: 1.83 matches Meier Eq. 2
- [x] Verify `'Meier COE'` constants: 0.113, 0.0876 match Meier Eq. 1
- [x] Confirm all 4 calc defs have Source/Ref/Basis citations
- [x] Confirm all 4 calc defs state year-dollar basis (1988$)
- [x] Verify design verification target: `'Meier HIF Driver Cost'` at E_d=5, eta=0.35, N_c=1, v=3.5 → C_dd≈$0.975B, gamma≈$68.25/J

#### hif_driver.sysml Review
- [x] Verify `beam_energy_mj` has doc comment with EIF-1992 source
- [x] Verify `num_chambers` has doc comment with Meier Eq. 5 source
- [x] Verify `pulse_rate_ref` has doc comment with Meier Eq. 5 source
- [x] Verify `meier_cost` calc bindings: `in beam_energy_mj = beam_energy_mj`, `in driver_efficiency = efficiency`, `in num_chambers = num_chambers`, `in rep_rate = pulse_rate_ref`
- [x] Verify `:>> efficiency = 0.35` (EIF-1992 Osiris)
- [x] Verify `:>> cost_per_joule = meier_cost.gamma` (EXPOSE pattern)
- [x] Verify `:>> energy = 14.286e6` (derived: 5.0 MJ / 0.35 = 14.286e6 J)
- [x] Verify `:>> lifetime_shots = 6.0e9` (Bangerter 2013)
- [x] Verify `driver_cost_billions` EXPOSE: `= meier_cost.cost_billions`
- [x] Verify import map: `ScalarValues::*`, `ife_subsystems::*`, `hif_economics::*`

#### hif_plant.sysml Review
- [x] Verify driver type narrowing: `part :>> driver : 'HIF Driver'`
- [x] Verify driver HIF params: `beam_energy_mj=5.0`, `num_chambers=1.0`, `pulse_rate_ref=3.5`
- [x] Verify target_factory: `cost_per_target = 10.0` with citation
- [x] Verify chamber: `wall_type = 'Wall Type'::liquid_wall`, `blanket_energy_multiple=1.15`, `yield_cost_constant=5.0e6`
- [x] Verify plant operations: `availability=0.90`, `frequency=3.5`, `gain=80.0`, `thermal_efficiency=0.43`
- [x] Verify plant financial: `discount_rate=0.08`, `plant_cost_constant=2000.0`, `om_cost_constant=65.0`
- [x] Verify `[ESTIMATED]` parameters (alpha, epsilon) have explicit `[ESTIMATED]` in doc comments
- [x] Verify Meier COE chain bindings:
  - `meier_reactor_cost_calc`: `in thermal_power_gw = thermal_power_gw`, `in num_units = 1.0`
  - `meier_capital_calc`: `in reactor_cost = meier_reactor_cost_calc.reactor_cost_billions`, `in driver_cost = driver.driver_cost_billions`, `in target_factory_cost = 0.1`
  - `meier_coe_calc`: `in total_capital_billions = meier_capital_calc.total_capital_billions`, `in availability = availability`, `in net_electric_power_gw = net_electric_power_gw`
- [x] Verify `meier_coe` EXPOSE: `= meier_coe_calc.coe_cents_kwh`
- [x] Verify `target_factory_cost = 0.1` literal has doc comment explaining C_tfd = $0.1B — added inline comment
- [x] Verify import map: `ScalarValues::*`, `ife_plant::*`, `ife_subsystems::*`, `hif_driver::*`, `hif_economics::*`
- [x] Count: all 14 Hawker parameters bound (4 driver + 1 target + 2 chamber + 7 plant-level)

### Validation Checkpoint

```bash
# Only if files were modified during review
uv run python -m syside check -Werror \
    models/library/analyses/hif_economics.sysml \
    models/designs/hif_ife/hif_driver.sysml \
    models/designs/hif_ife/hif_plant.sysml
```

Expected: `Checks passed!` (0 errors, 0 warnings)

### Phase Completion Gate

- All checklist items verified or fixed
- If any file was modified: Level 1 re-confirmed
- No unattributed numeric literals
- No missing Source/Ref/Basis citations

---

## Phase 2: Verification, Artifacts & Close

### Overview

Write the Python verification script for SV-012/013/014, run the full 11-file Level 1 check, update project artifacts (VALIDATION_MATRIX, README, traceability matrix), and confirm no upstream modifications. This phase completes the work item.

### Design Reference

- See design doc "Validation Plan" for the three validation levels and expected values
- See design doc "HIF Parameter Values (Osiris Baseline)" for verification inputs
- See spec "Success Criteria → Verification" for SV-011 through SV-015 definitions

### Files to Create/Modify

- `scripts/verify_hif_costs.py` — NEW: Python verification script for SV-012, SV-013, SV-014
- `modeling_project/VALIDATION_MATRIX.md` — REFINE: update SV-011 through SV-015 statuses
- `models/README.md` — REFINE: add HIF catalog entries
- `data/traceability_matrix.csv` — REFINE: add HIF element entries

### Checklist

#### Verification Script (`scripts/verify_hif_costs.py`)
- [x] Create verification script following `scripts/verify_ife_lcoe.py` pattern
- [x] Implement `compute_meier_driver_cost(beam_energy_mj, driver_efficiency, num_chambers, rep_rate)` returning `(cost_billions, gamma)`
- [x] Implement `compute_meier_reactor_cost(thermal_power_gw, num_units)` returning `reactor_cost_billions`
- [x] Implement `compute_meier_capital_cost(reactor_cost, driver_cost, target_factory_cost)` returning `total_capital_billions`
- [x] Implement `compute_meier_coe(total_capital_billions, availability, net_electric_power_gw)` returning `coe_cents_kwh`
- [x] Implement Hawker LCOE at HIF params (reuse `compute_ife_lcoe` from `verify_ife_lcoe.py`)
- [x] SV-012 check: Meier driver cost at E_d=5, eta=0.35, N_c=1, v=5.0 Hz → C_dd=$0.988B (PASS ±10%)
- [x] SV-012 check: Meier driver cost at E_d=5, eta=0.35, N_c=1, v=3.5 Hz → C_dd=$0.975B, gamma=$68.25/J (PASS)
- [x] SV-013 check: Hawker LCOE with HIF Osiris params → $270/MWh (positive, finite — PASS per VALIDATION_MATRIX tolerance "finite positive"). NOTE: exceeds Hawker's $25-120 range due to target cost dominance at 3.5 Hz ($213/MWh of $270/MWh from targets alone). Design doc estimate of ~$66/MWh was incorrect.
- [x] SV-014 check: Meier COE at Osiris params → 4.74 cents/kWh (5.3% from 5.0 — PASS ±15%)
- [x] Print clear PASS/FAIL for each SV entry
- [x] Run script and confirm all checks pass

#### Full Level 1 Validation (SV-015)
- [x] Run full 11-file syside check:
  ```bash
  uv run python -m syside check -Werror \
      models/library/foundation/economic_parameter.sysml \
      models/library/foundation/costed_component.sysml \
      models/library/cost_structure/cas_hierarchy.sysml \
      models/library/cost_structure/ife_cost_parameters.sysml \
      models/library/analyses/ife_lcoe.sysml \
      models/library/analyses/fusion_cycle.sysml \
      models/library/analyses/hif_economics.sysml \
      models/designs/generic_ife/ife_subsystems.sysml \
      models/designs/generic_ife/ife_plant.sysml \
      models/designs/hif_ife/hif_driver.sysml \
      models/designs/hif_ife/hif_plant.sysml
  ```
- [x] Confirm: `Checks passed!` (0 errors, 0 warnings)

#### SV-011 Verification (Model Inspection)
- [x] Confirm HIF Driver specializes IFE Driver: `part def 'HIF Driver' :> 'IFE Driver'`
- [x] Confirm 4 interface params set: efficiency=0.35, cost_per_joule=meier_cost.gamma, energy=14.286e6, lifetime_shots=6.0e9
- [x] Confirm all 4 params have Source/Ref/Basis citations
- [x] Mark SV-011 as passing

#### No-Upstream-Modification Check (MR-WI008-10)
- [x] Run `git diff HEAD -- models/library/ models/designs/generic_ife/` to confirm no modifications to existing files
- [x] Confirm only additions in `models/library/analyses/hif_economics.sysml` (new file) and `models/designs/hif_ife/` (new directory)

#### Viability Constraint (MR-WI008-6)
- [x] Confirm eta*G = 0.35 × 80 = 28 ≥ 10 (pass by inspection)

#### Update VALIDATION_MATRIX.md
- [x] Update SV-011 status: pending → passing
- [x] Update SV-012 status: pending → passing (after script confirms)
- [x] Update SV-013 status: pending → passing (after script confirms)
- [x] Update SV-014 status: pending → passing (after script confirms)
- [x] Update SV-015 status: pending → passing (after syside check confirms)

#### Update models/README.md
- [x] Add `### library/analyses/` entry for `hif_economics.sysml`
- [x] Add `## Design Catalog` section with generic_ife and hif_ife entries
- [x] Add `### designs/hif_ife/` entry for `hif_driver.sysml`
- [x] Add `### designs/hif_ife/` entry for `hif_plant.sysml`

#### Update Traceability Matrix (`data/traceability_matrix.csv`)
- [x] Add row: `'Meier HIF Driver Cost'`
- [x] Add row: `'Meier Reactor Cost'`
- [x] Add row: `'Meier Total Capital Cost'`
- [x] Add row: `'Meier COE'`
- [x] Add row: `'HIF Driver'`
- [x] Add row: `hif_plant`

### Validation Checkpoint

All verification activities are the validation checkpoint for this phase:
- Level 1: Full 11-file syside check → 0 errors, 0 warnings
- SV-012: Meier driver cost within ±10% of reference
- SV-013: Hawker LCOE positive and finite (formal tolerance; actual $270/MWh — see note in script)
- SV-014: Meier COE within ±15% of 5.0 cents/kWh
- SV-015: Same as Level 1 (HIF files specifically)

### Phase Completion Gate

- All SV-011 through SV-015 marked as passing in VALIDATION_MATRIX.md
- Verification script runs cleanly with all PASS results
- models/README.md updated with HIF entries
- Traceability matrix has all HIF element rows
- No upstream files modified (git diff clean)
- All spec success criteria verified:
  - [Functional] HIF Driver exists as concrete part def specializing IFE Driver, with 4 params set from sources
  - [Functional] HIF plant instantiation with all 14 Hawker params bound to HIF values
  - [Functional] Meier driver cost formula implemented as evaluable calc def
  - [Functional] Meier COE model implemented as evaluable calc def
  - [Functional] Both Hawker LCOE and Meier COE computed for the same HIF plant
  - [Functional] Viability constraint (eta*G >= 10) satisfied
  - [Quality] Every quantitative value carries Source/Ref/Basis citation
  - [Quality] Every cost parameter documents year-dollar basis
  - [Quality] No files in library or generic_ife modified
  - [Quality] All files parse cleanly with syside check

---

## Feasibility Concerns

| Concern | Assessment | Mitigation |
|---------|-----------|------------|
| Prototype already passes Level 1; minimal code changes expected | Low risk — this is the ideal outcome from design-phase prototyping | Phase 1 is a review phase; if no gaps found, it completes quickly |
| Verification script may reveal parameter errors | Low risk — design already hand-computed all verification targets | Cross-reference script inputs against design parameter table |
| `target_factory_cost = 0.1` literal in `meier_capital_calc` binding may lack citation context | Medium — this is C_tfd from Meier, should have a doc comment | Add citation if missing during Phase 1 review |
| Traceability matrix has no existing entries (empty CSV) — format conventions untested | Low — CSV format is defined in the header row | Follow header schema exactly; first entries establish the convention |
