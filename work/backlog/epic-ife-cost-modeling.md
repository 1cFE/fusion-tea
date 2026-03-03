---
Status: draft
Priority: P0
Created: 2026-03-02
Updated: 2026-03-02
---

# Epic: IFE Cost Modeling

## Executive Summary

Build the economic modeling infrastructure for Inertial Fusion Energy — a driver-agnostic cost framework based on Hawker's 14-parameter LCOE model, a generic IFE plant design, and a first concrete instantiation with Heavy Ion Beam parameters. This delivers the IFE half of the V1 cross-concept comparison.

**Critical Success Factor**: A validated IFE LCOE model that produces cost breakdowns traceable to source literature and comparable to MFE models along the project's comparison axes.

---

## Context

The IFE domain research (approved 2026-03-02, DI-001 through DI-005) established that:

- No single IFE driver type has sufficient CAS-level data for a bottom-up model
- Hawker's 14-parameter framework provides a complete, technology-agnostic LCOE model with defined ranges, sensitivity rankings, and Monte Carlo validation targets
- The CAS framework is universal across MFE and IFE; divergence concentrates in CAS22 sub-accounts (DI-002)
- Heavy Ion Beam has the richest concrete data across two dedicated papers (Meier 1986, Bangerter 2013)

The modeling target selection decision (`modeling_project/intent/IFE Modeling Target Selection.md`) chose a top-down approach: build the driver-agnostic framework first, then instantiate with HIF parameters.

**Current state**: No IFE models exist. Library has no IFE-relevant definitions. Research basis is complete (7 IFE sources ingested, 5 domain insights captured).

**After this epic**: A working IFE LCOE model producing cost breakdowns by CAS category, with HIF as the first concrete concept, validated against Hawker's Monte Carlo range and Meier's COE projections.

---

## Authority Source Dependencies

| Source | Use For | Items Depending On | Status |
|--------|---------|-------------------|--------|
| Hawker 2020 | 14 parameters, LCOE formula, sensitivity rankings, MC validation targets | Items 1, 2 | Ingested |
| ARIES Cost Account Doc 2013 | CAS hierarchy, IFE/MFE account mapping | Item 1 | Ingested |
| Meier et al. 1986 (HIF Economics) | HIF driver cost formula, COE model, cost decomposition | Items 1, 3 | Ingested |
| Bangerter et al. 2013 (Accelerators) | HIF driver efficiency, target gain curves, rep rates | Item 3 | Ingested |
| EIF-1992 (Energy from Inertial Fusion) | IFE process chain, structural components, chamber concepts | Item 2 | Ingested |
| PyFECONS | IFE CAS22 implementation, power balance model, target factory costing | Items 1, 2 | Available (external codebase) |

---

## Success Criteria

- [ ] All 14 Hawker parameters exist as typed model attributes with ranges and sensitivity metadata
- [ ] CAS mapping covers shared (CAS20-21, 23-27, 91-99) and IFE-specific (CAS22 sub-accounts) structure
- [ ] LCOE calculation produces results within Hawker's $25-120/MWh Monte Carlo range for valid parameter combinations
- [ ] HIF instantiation produces COE values cross-checkable against Meier 1986 projections (3.9-5.8 cents/kWh at 1.0 GWe)
- [ ] Every quantitative value carries MR-4 compliant citations
- [ ] Models pass validation Levels 1-3

---

## Items

### Item 1: IFE Cost Structure Library

**Scale**: standard
**Dependencies**: None

**Scope**:
Define the reusable library elements for IFE economic modeling. This includes Hawker's 14 parameters as typed model attributes with ranges, CAS mapping that identifies shared vs. IFE-specific accounts (DI-002), the LCOE calculation framework, and the fusion cycle gain constraint (eta * G * M * epsilon, DI-001). All definitions are driver-agnostic per MR-3.

**Key requirements**:
- [ ] 14 Hawker parameters as attributes with units, ranges, defaults, and sensitivity rankings (DI-005)
- [ ] CAS account hierarchy covering IFE-relevant accounts with shared/divergent classification
- [ ] LCOE calculation implementing Hawker's DCF formula
- [ ] Fusion cycle gain constraint with eta*G > 10 viability threshold (DI-001)
- [ ] Costed component interface per MR-2

**Deliverables**:
- `models/library/ife_cost_parameters.sysml` (or similar)
- `models/library/cas_ife.sysml` (IFE CAS mapping)
- `models/library/lcoe_calculation.sysml`

---

### Item 2: Generic IFE Concept Model

**Scale**: standard
**Dependencies**: Item 1 (library patterns must exist before design uses them)

**Scope**:
Build a driver-agnostic IFE plant model that uses the library definitions from Item 1. The model has an abstract driver interface (parameterized by efficiency, cost/J, energy, lifetime), target factory as operating cost (DI-003), reaction chamber, and BOP from shared library. This is the "template" that driver-specific instantiations (Item 3 and future) will specialize.

**Key requirements**:
- [ ] Abstract driver interface with parameterized eta, gamma, E_d, N_d
- [ ] Target factory modeled as operating cost with per-target cost parameter (DI-003)
- [ ] Chamber with abstract wall type (dry/wet/liquid)
- [ ] Power balance: fusion cycle gain, recirculating power fraction
- [ ] Cost rollup through CAS hierarchy to LCOE

**Deliverables**:
- `models/designs/generic_ife/` — concept model files
- Validation: LCOE output within Hawker range for default parameters

---

### Item 3: HIF Concept Instantiation

**Scale**: standard
**Dependencies**: Item 2 (generic IFE model must exist to instantiate)

**Scope**:
Instantiate the generic IFE model with Heavy Ion Beam parameters from Meier 1986 and Bangerter 2013. Implement the HIF driver cost formula (C_d = f(E_d, N_c, v)), set driver efficiency (20-30%), target gain curves, and rep rate ranges. Validate COE output against Meier's projections.

**Key requirements**:
- [ ] HIF driver cost formula: C_d = (0.32 + 0.088·E_d) × (1.25 + 0.05·N_c) × (1 + 0.0088·(v−5))
- [ ] Driver efficiency 20-30% (DI-004)
- [ ] Target gain from Bangerter Table 1 (distributed radiator, close-coupled, x-target)
- [ ] COE validation: 3.9-5.8 cents/kWh at 1.0 GWe (Meier 1986, 1988$)
- [ ] All parameters cite source with MR-4 format

**Deliverables**:
- `models/designs/hif_ife/` — HIF-specific model files
- Validation report comparing model output to Meier COE projections

---

## Sequencing

```
Item 1: IFE Cost Structure Library (no dependencies)
  └─> Item 2: Generic IFE Concept Model (depends on Item 1)
       └─> Item 3: HIF Concept Instantiation (depends on Item 2)
```

Strictly sequential — each item builds on the previous. No parallelism within this epic.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hawker's aggregate cost categories don't map cleanly to CAS sub-accounts | Medium | Medium | Start with Hawker's 5 categories, disaggregate incrementally using ARIES doc |
| HIF 1986 data in 1988$ requires inflation adjustment for cross-comparison | High | Low | Document year-dollar basis; defer normalization to analysis phase |
| Modeling patterns (MR-6, PR-3) not yet defined — risk of rework | Medium | Medium | Treat Items 1-2 as pattern-defining work; validate patterns before Item 3 |
| PyFECONS IFE implementation may reveal structural constraints not in papers | Low | Medium | Reference PyFECONS as validation, not as prescriptive architecture |

---

**Last Updated**: 2026-03-02
**Next Action**: `/spec-model` on Item 1 (IFE Cost Structure Library)
