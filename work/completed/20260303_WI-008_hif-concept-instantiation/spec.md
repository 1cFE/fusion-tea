---
Status: completed
Scale: standard
Epic: IFE Cost Modeling
Owner: reid
Created: 2026-03-02
Updated: '2026-03-03'
---

# WI-008: HIF Concept Instantiation

## Overview

Instantiate the generic IFE power plant (WI-007) with Heavy Ion Fusion parameters from Meier 1986, Bangerter 2013, and Hogan/EIF 1992. This produces the first concrete concept model in the project — an HIF plant with LCOE output, validated against both Hawker's parametric model and Meier's engineering-economic model.

## Goals & Context

**Goals served**:
- RQ-1: HIF cost drivers — the instantiation shows where money goes in an HIF plant (driver dominates)
- RQ-2: Credible LCOE/COE — dual model validation provides two independent cost estimates
- RQ-3: Shared vs. divergent — HIF concretely demonstrates what changes vs. what stays the same when specializing the generic IFE model
- RQ-5: High-sensitivity parameters — HIF's specific sensitivity profile (driver cost dominance) differs from generic IFE

**Domain insights applied**:
- DI-001: Fusion cycle gain viability → HIF with eta=0.25-0.35 and G=60-80 comfortably exceeds eta*G>10
- DI-002: CAS22 divergence → HIF driver (induction linac) fills the CAS22.1.3 slot
- DI-003: Target cost as operating cost → HIF target costs from source literature
- DI-004: Driver cost reference points → HIF induction linacs fall between pulsed-power ($1.7-6/J) and NIF ($9.5/J); Meier formula provides parametric relationship
- DI-005: Hawker 14 parameters → bound to HIF-specific values from sources

**Epic context**: Third and final item in the IFE Cost Modeling epic (WI-006 → WI-007 → **WI-008**). Depends on WI-007's generic IFE plant model. Completes the IFE half of the V1 cross-concept comparison.

**Baseline operating point**: EIF-1992 Osiris HIF plant design — the best-documented HIF plant with a liquid-wall chamber, 1.0 GWe net output, and published COE.

> Source: knowledge/sources/energy_from_inertial_fusion/output.md
> Ref: Power plant operating parameters table (lines 644-658)
> Basis: Osiris is the most complete HIF plant design with operating parameters, COE, and chamber details

## Current State

**Generic IFE model exists** (WI-007 output — 2 files in `models/designs/generic_ife/`):
- `ife_subsystems.sysml` — `IFE Driver` (abstract, 4 params), `Target Factory`, `Reaction Chamber`, CAS22 sub-accounts, `Wall Type` enum
- `ife_plant.sysml` — `IFE Power Plant` assembly with 14-param LCOE binding, power balance, viability constraint

**Library exists** (WI-006 output — 6 files in `models/library/`):
- `IFE Cost Parameters` with all 14 Hawker parameters and metadata
- `IFE LCOE` calc def (14 inputs → LCOE)
- `Recirculating Power Fraction` calc and `Viability Threshold` constraint
- CAS hierarchy, costed component, economic parameter foundations

**WI-007 status**: Active — model files are production-quality and pass Level 1 validation. Phase 2 (SV verification and close) is pending but does not affect the model structures WI-008 builds on.

**No HIF models exist** — `models/designs/hif_ife/` does not exist yet.

## Modeling Requirements

### Functional

#### MR-WI008-1: HIF Driver Definition

The model SHALL define a concrete `'HIF Driver'` part def specializing `'IFE Driver'` with the four interface parameters set to HIF-specific values from the Osiris baseline:

| Parameter | Symbol | Osiris Value | Source |
|-----------|--------|-------------|--------|
| efficiency | eta | 0.35 | EIF-1992 Osiris table |
| cost_per_joule | gamma | Derived from Meier formula (MR-WI008-2) | Meier 1986 Eq. 5 |
| energy | E_d | See A2 (definition mapping) | EIF-1992 / Meier 1986 |
| lifetime_shots | N_d | See A3 | Bangerter 2013 |

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Epic Item 3, MR-WI007-2 (abstract driver interface)
- **Validation**: HIF Driver is concrete (not abstract), specializes IFE Driver, all 4 params set with citations (SV-011)

> Source: knowledge/sources/energy_from_inertial_fusion/output.md
> Ref: Power plant operating parameters table — Osiris column
> Basis: Osiris is the best-documented HIF plant design

#### MR-WI008-2: Meier Driver Cost Formula

The model SHALL include Meier's HIF driver cost formula as a calc def:

```
C_dd = (0.32 + 0.088 * E_d) * (1.25 + 0.05 * N_c) * (1 + 0.0088 * (v - 5))   [$B]
```

Where E_d is driver energy (MJ), N_c is number of chambers, v is pulse rate (Hz). The calc SHALL be used to derive the HIF Driver's `cost_per_joule` (gamma) parameter, establishing the bridge between Meier's engineering cost model and Hawker's parametric LCOE.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Epic Item 3 key requirement
- **Validation**: Calc def produces expected output for known inputs (SV-012)

> Source: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
> Ref: Eq. 5 (lines 173-192)
> Basis: Meier 1986 parametric driver cost formula, fit to induction linac design studies

#### MR-WI008-3: Meier COE Model

The model SHALL include Meier's COE calculation as calc defs, covering:

1. **Reactor cost**: `C_rd = C_r * (P_t / 1.67)^b * (0.72 * N_u + 0.28)` [$B]
2. **Total capital cost**: `C_T = 1.83 * (C_rd + C_dd + C_tfd)` [$B]
3. **COE**: `COE = (0.113 * C_T) / (0.0876 * a * P_n)` [cents/kWh]

Constants: C_r = $0.66B, b = 0.49, C_tfd = $0.1B, factor 1.83 (total/direct ratio), 0.113 = R + M rate (8.3% + 3%), 0.0876 = conversion factor.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Dual validation approach, Epic COE validation target
- **Validation**: COE at Meier reference case ≈ 5.0 cents/kWh (SV-014)

> Source: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
> Ref: Eqs. 1-4 (lines 76-171)
> Basis: Meier 1986 complete engineering-economic COE model

#### MR-WI008-4: HIF Plant Instantiation

The model SHALL define an HIF plant as an instance of `'IFE Power Plant'` with all 14 Hawker parameters bound to HIF-appropriate values:

**Driver parameters** (from HIF-specific sources):

| Parameter | Hawker Symbol | HIF Value | Source |
|-----------|--------------|-----------|--------|
| driver.efficiency | mu_d | 0.35 | EIF-1992 Osiris |
| driver.cost_per_joule | gamma | From Meier formula | Meier 1986 Eq. 5 |
| driver.energy | E_d | Mapped from Osiris (see A2) | EIF-1992 Osiris |
| driver.lifetime_shots | N_d | See A3 | Bangerter 2013 |

**Chamber parameters**:

| Parameter | Hawker Symbol | HIF Value | Source |
|-----------|--------------|-----------|--------|
| chamber.wall_type | — | liquid_wall | EIF-1992 Osiris/Cascade |
| chamber.blanket_energy_multiple | E_b | 1.1-1.3 | Bangerter 2013 |
| chamber.yield_cost_constant | beta | From Hawker range | Hawker 2020 Table 1 |

**Plant-level parameters**:

| Parameter | Hawker Symbol | HIF Value | Source |
|-----------|--------------|-----------|--------|
| availability | mu_a | 0.90 | Bangerter 2013 (5 Hz, 40 yr, 90%) |
| frequency | f | 3.5 | EIF-1992 Osiris |
| gain | G | 80 | EIF-1992 Osiris |
| thermal_efficiency | mu_th | 0.43 | EIF-1992 Osiris |
| discount_rate | d | 0.08 | Hawker default (financial, not concept-specific) |
| plant_cost_constant | alpha | Derived or from Hawker range | See A4 |
| om_cost_constant | epsilon | Derived or from Hawker range | See A4 |
| target_cost_constant | delta | Source-derived | HIF target literature |

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Epic Item 3, RQ-1, RQ-2
- **Validation**: All 14 parameters set with citations; no unattributed values (SV-013)

#### MR-WI008-5: Dual LCOE/COE Validation

The HIF plant model SHALL produce two independent cost outputs:

1. **Hawker LCOE** (via library `'IFE LCOE'` calc, inherited from `'IFE Power Plant'`) — the cross-concept comparable output
2. **Meier COE** (via MR-WI008-3 calc defs, HIF-specific) — the engineering-economic validation output

Both outputs must be present and evaluable for the same plant parameters.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: Epic success criteria, user-selected dual validation approach
- **Validation**: Both LCOE and COE values computed; Meier COE cross-checked against published values (SV-013, SV-014)

#### MR-WI008-6: Viability Constraint Satisfaction

The HIF plant parameters SHALL satisfy the viability constraint (eta * G >= 10). With Osiris baseline values (eta=0.35, G=80), eta*G = 28, well above threshold.

- **Type**: Functional
- **Priority**: Must
- **Derives from**: DI-001, MR-WI007-6
- **Validation**: `assert constraint viability` passes for HIF parameters

### Quality

#### MR-WI008-7: Traceable Citations

All quantitative values SHALL carry structured citations per MR-4 (Source/Ref/Basis in doc comments). Every parameter value must trace to a specific source document and location. Values derived from formulas must cite the formula source plus the input values used.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: MR-4, PR-5
- **Validation**: Every numeric literal and structural choice has a citation; no unattributed values

#### MR-WI008-8: Year-Dollar Documentation

All cost parameters SHALL document their year-dollar basis in doc comments. No inflation adjustments are applied (out of scope) — but the year basis must be stated so a reader knows what they're comparing.

- **Type**: Quality
- **Priority**: Must
- **Derives from**: Epic risk (HIF 1986 data in 1988$ requires inflation adjustment)
- **Validation**: Every cost parameter's doc comment states the year-dollar basis

### Constraint

#### MR-WI008-9: Design Location

All files SHALL reside in `models/designs/hif_ife/`.

- **Type**: Constraint
- **Derives from**: MR-3, epic deliverables

#### MR-WI008-10: No Upstream Modification

The model SHALL NOT modify any files in `models/library/` or `models/designs/generic_ife/`. HIF specialization is downstream only.

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: MR-3, MR-WI007-12

#### MR-WI008-11: Parse Validation

All model files SHALL pass syside validation (Level 1 — zero parse errors).

- **Type**: Constraint
- **Priority**: Must
- **Derives from**: Epic success criteria
- **Validation**: `uv run syside check models/designs/hif_ife/*.sysml` — zero errors (SV-015)

## Scope Boundaries

### In Scope

- `models/designs/hif_ife/` — all HIF concept model files
- Concrete `'HIF Driver'` part def specializing `'IFE Driver'`
- HIF plant instantiation with all 14 Hawker parameters bound to HIF values
- Meier driver cost formula as SysML calc def
- Meier COE model (reactor cost, total capital, COE) as SysML calc defs
- Chamber wall type set to `liquid_wall`
- Dual output: Hawker LCOE + Meier COE
- SV-011 through SV-015 entries in VALIDATION_MATRIX.md
- Osiris as baseline operating point

### Out of Scope

- Multiple HIF plant configurations (only one baseline instantiation)
- Multiple target designs (Bangerter Table 1 gains documented as reference, not modeled)
- Meier driver efficiency formula as calc def (Osiris eta=35% used directly; Meier's parametric formula is a reference, not a model element)
- Multi-unit plant economics (Meier's N_u > 1 scenarios)
- Inflation adjustment between year-dollars (documented, not applied)
- Sensitivity analysis or Monte Carlo sweeps (analysis phase)
- Modifications to library or generic IFE files
- MFE concept models

## Success Criteria

### Functional

- HIF Driver exists as concrete part def specializing IFE Driver, with 4 params set from sources
- HIF plant instantiation with all 14 Hawker params bound to HIF values
- Meier driver cost formula implemented as evaluable calc def
- Meier COE model implemented as evaluable calc def
- Both Hawker LCOE and Meier COE computed for the same HIF plant
- Viability constraint (eta*G >= 10) satisfied

### Quality

- Every quantitative value carries Source/Ref/Basis citation
- Every cost parameter documents year-dollar basis
- No files in library or generic_ife modified
- All files parse cleanly with `uv run syside check`

### Verification

- SV-011: HIF Driver concrete with 4 params set from sources
- SV-012: Meier driver cost formula produces expected output (e.g., ~$1B at E_d=5 MJ, N_c=1, v=5 Hz)
- SV-013: Hawker LCOE with HIF params produces a finite, positive value in a reasonable range
- SV-014: Meier COE at reference case ≈ 5.0 cents/kWh (Meier 1986, 1988$, 1.0 GWe)
- SV-015: All HIF files pass syside check (0 errors)

## Assumptions & Risks

| # | Assumption/Risk | Type | Confidence/Likelihood | Impact | Mitigation |
|---|----------------|------|----------------------|--------|------------|
| A1 | WI-007 generic IFE model is stable and sufficient for HIF specialization | Assumption | High — model files exist and pass validation | Low if wrong — can extend during implementation | |
| A2 | "Driver energy" definition differs between sources: EIF-1992/Meier use beam energy on target (MJ), Hawker uses bank/stored energy (J). Mapping: E_d_Hawker = E_d_beam / eta | Assumption | Medium — inferred from cross-checking Osiris yield vs gain | High — incorrect mapping produces wrong LCOE | Design phase must verify by reproducing Osiris power balance |
| A3 | Driver lifetime (N_d) is not explicitly stated for Osiris. Bangerter gives 6×10^9 pulses for "5 Hz, 40 years, 90% availability". This is a reliability target, not a demonstrated lifetime. | Assumption | Medium | Low — N_d has moderate LCOE sensitivity (-0.134) | Document as engineering target; sensitivity analysis can explore range |
| A4 | Hawker aggregate parameters (alpha, beta, epsilon) may not map cleanly to Meier's cost decomposition. Alpha (plant cost $/kWe) aggregates reactor + BOP; Meier disaggregates these. | Assumption | Medium | Medium — may need approximate mapping | Design phase resolves by computing alpha from Meier's reactor cost, or uses Hawker defaults with documentation |
| R1 | `part redefines driver : 'HIF Driver'` pattern (from WI-007 design doc) may not work as expected in syside | Risk | Medium | Medium — may need alternative specialization pattern | Design phase prototypes the specialization pattern before committing to it |
| R2 | Meier COE and Hawker LCOE may produce significantly different results for the same plant, making "dual validation" more of a "dual computation" | Risk | High | Low — the models have different structures and assumptions; documenting both is valuable regardless | Frame validation as: each model must match its own published reference, not match each other |
| R3 | Gain definition ambiguity (yield/beam-energy vs yield/bank-energy) may propagate errors through LCOE calculation | Risk | Medium | High — wrong G by factor of eta (2-3x) would invalidate LCOE | Cross-check: compute Osiris net power and yield using both conventions; the one that matches published values is correct |

## Traceability

### Source Requirements

| Source | What it provides | Requirements served |
|--------|-----------------|-------------------|
| `knowledge/sources/energy_from_inertial_fusion/output.md` | Osiris baseline: E_d, G, eta, f, P_n, mu_th, COE; chamber type (liquid wall); gain curves | MR-WI008-1, MR-WI008-4, MR-WI008-6 |
| `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md` | Meier driver cost formula, reactor cost formula, COE model, sensitivity analysis, validation targets | MR-WI008-2, MR-WI008-3, MR-WI008-4 |
| `knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md` | Bangerter Table 1 (target gains by type), driver efficiency range (20-30%), eta*G>10 criterion, availability target (90%), rep rate ranges | MR-WI008-1, MR-WI008-4, MR-WI008-6 |
| `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` | Hawker's 14 parameters, ranges, sensitivities | MR-WI008-4 (non-driver parameter defaults) |
| `models/designs/generic_ife/ife_subsystems.sysml` | IFE Driver (abstract), Target Factory, Reaction Chamber, CAS22 sub-accounts | MR-WI008-1 (specialization target) |
| `models/designs/generic_ife/ife_plant.sysml` | IFE Power Plant assembly with LCOE wiring | MR-WI008-4 (instantiation target) |

### Downstream Impacts

- Cross-concept comparison (OVERVIEW.md comparison axes) consumes HIF LCOE and CAS cost outputs — this is the IFE representative for V1
- Future IFE concept instantiations (laser, pulser) follow the same specialization pattern established here
- Demo/workflow explainer (`demo/index.html`) shows HIF as the concrete concept example

### Applicable Project Requirements

- MR-1: CAS hierarchy as primary cost decomposition (inherited via generic IFE)
- MR-2: Standard costed component interface (inherited via library)
- MR-3: Library concept-agnostic, designs concept-specific (HIF values only in `designs/hif_ife/`)
- MR-4: Traceable citations on all quantitative values
- MR-5: Standard output schema — HIF produces LCOE along comparison axes
- MR-6: Modeling patterns — HIF validates the specialization pattern from WI-007

### Requirements Flagged for Promotion

- **MR-WI008-8 (year-dollar documentation)** may warrant promotion to a project-wide PR-XXX rule. All concept models will need year-dollar basis documentation for meaningful cross-concept comparison. Defer decision until MFE modeling begins and the pattern is validated.

## Related Artifacts

- **Epic**: `work/backlog/epic-ife-cost-modeling.md` — Item 3
- **Predecessor**: `work/active/WI-007_generic-ife-concept-model/` — generic IFE model (consumed)
- **Completed dependency**: `work/completed/20260302_WI-006_ife-cost-structure-library/` — library definitions (consumed)
- **Research**: `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`
- **Design**: `work/active/WI-008_hif-concept-instantiation/design.md` (to be created)
- **Plan**: `work/active/WI-008_hif-concept-instantiation/plan.md` (to be created)
