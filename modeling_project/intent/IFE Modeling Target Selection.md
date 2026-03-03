# IFE Modeling Target Selection

**Date**: 2026-03-02
**Context**: Emerged from IFE domain research (Item 4 of DEMO epic)
**Research basis**: `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`
**Domain insights**: DI-001 through DI-005

---

## Decision

Start with a **generic, driver-agnostic IFE model** built around Hawker's 14-parameter LCOE framework, then instantiate it with **Heavy Ion Beam (HIF) parameters** as the first concrete concept.

## Why Not Driver-Specific First?

The research revealed that no single driver type has sufficient CAS-level cost data for a bottom-up model:

- **Laser IFE**: Xcimer costs only the laser subsystem. AMPS defers technoeconomics entirely. Neither provides a complete LCOE.
- **Heavy Ion Beam IFE**: The 1986 Meier paper has a complete COE model, but uses a simplified 3-item decomposition with 1988$ values. Driver cost formula is detailed; everything else is sparse.
- **Pulsed-power IFE**: One data point ($6/J stored energy) and no plant-level economics.

## Why Hawker's Framework as First Pass?

1. **Parameter completeness**: All 14 parameters have defined ranges, defaults, and sensitivity rankings (DI-005). The model can be fully populated from day one.
2. **Structure maps to CAS**: Hawker's 5 cost categories (plant, yield, driver, target, O&M) map to CAS groupings (DI-002). Gives a CAS-structured model that can later be disaggregated.
3. **Driver-agnostic = reusable**: Captures shared IFE economics (fusion cycle gain, recirculating power, target cost as operating expense) without committing to a driver. Driver-specific parameters (eta, gamma, driver lifetime) become the variation axis.
4. **Validation target exists**: Hawker's Monte Carlo results ($25–120/MWh range) provide a direct validation benchmark.
5. **Natural extension path**: Instantiating with HIF or laser parameters is a parameter-setting exercise, not a structural redesign.

## Why HIF as First Instantiation?

The 1986 HIF paper + Accel-2013 together provide the richest concrete numbers:
- Driver efficiency: 20–30%
- Driver cost formula: C_d = (0.32 + 0.088·E_d) × (1.25 + 0.05·N_c) × (1 + 0.0088·(v−5)) [$B]
- Target gain curves for multiple target types
- Rep rate ranges (5–10 Hz)
- Complete COE model for cross-validation

Two dedicated papers beats any other driver type's data coverage.

## Implied Model Structure

From the research (Section 7 — Architecture Insights):

- **Library**: Hawker's 14-parameter framework + shared CAS elements (CAS21, 23–27, 91–99) + fusion cycle gain relationship (DI-001)
- **Design**: Generic IFE concept with abstract driver interface, target factory as operating cost (DI-003), chamber as structural element
- **First instantiation**: HIF-specific driver parameters from Meier/Bangerter sources

## Implied Work Items for Modeling Epic

1. **Library patterns for IFE cost structure** — Hawker's 14 parameters as model attributes, CAS mapping, LCOE calculation framework, fusion cycle gain constraint
2. **Generic IFE concept model** — driver-agnostic plant with abstract driver interface, target factory, chamber, BOP
3. **HIF instantiation** — populate driver parameters from 1986/2013 sources, validate COE against Meier's projections
