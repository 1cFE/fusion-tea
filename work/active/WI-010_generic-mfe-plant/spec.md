---
Status: active
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-13
Updated: 2026-07-13
---

# WI-010: Generic MFE Plant Model

## Overview

A confinement-agnostic MFE plant `part def` that composes the WI-009 subsystems, wires the physics→cost→LCOE calc pipeline, and asserts the viability constraints — the MFE analogue of `models/designs/generic_ife/ife_plant.sysml`, one level richer. This is Layer 2 assembly from the WI-009 design (the plant idiom sketch); WI-011 specializes it with concept values and family closures.

**Demo context**: this plant is the spine of the stellarator MBSE demo's initial model (Stage 2). It must be codegen-clean so WI-011's concept-09 instance generates through `sysml-codegen` and runs under `teax`, and so the 1costingFE handshake (Anchor A) can compare per-account costs and LCOE.

## Required Reading

- `knowledge/holdout/aries-cs/PROTOCOL.md` — this is a demo model-development item; the ARIES-CS blocklist binds. Source only from 1costingFE (admissible) and the WI-009 library; never open the barred docs/dirs listed in PROTOCOL §3.

## Scope (demo-scoped)

Per the initial-model scoping decision (2026-07-13): model the spine bottom-up and grow depth in Stage 3 where leverage is highest (concept US-3), rather than reproducing all ~30 CAS accounts uniformly now.

**In scope:**
- Abstract `'MFE Power Plant'` part def composing: `'Magnet System'`, `'Heating and CD'`, `'Divertor'` (from WI-009), plus representations of the shared power-core and balance-of-plant accounts (blanket, shield, structure, BOP, buildings, indirect, contingency) sufficient for a credible full-enough CAS breakdown and LCOE.
- Bind the physics spine: `'Plasma Geometry'` → `'DT Fusion Power'` → `'MFE Power Balance Calc'` → net electric; bind `'Magnet Coil Cost'` → magnet `capital_cost`; roll up total capital; bind `'LCOE DCF'` → LCOE.
- Assert the two WI-009 viability constraints (`'Net Power Positive'`, `'Economic Recirculating Threshold'`).
- Reproduce 1costingFE's steady-state per-account cost scalings for the non-magnet accounts **that fit the codegen envelope** (flat Real arithmetic, no exp/if/lookup). Where an account's 1costingFE formula needs out-of-envelope constructs, take that account cost as a plant input (pass-through) and record it as a documented initial-model limitation for Stage-3 deepening.
- Expose derived attributes: net electric, LCOE, and the per-account CAS breakdown.

**Out of scope:**
- Concept-specific values, geometry, coil topology, family density closure (WI-011).
- The tokamak Greenwald closure and any tokamak specifics (demo needs stellarator; tokamak is the separate epic track).
- Running codegen / the viability sweep (later).

## Key Risk — validate the two untested wiring constructs FIRST

Cross-calc usage binding (`in x = calc.ret;`) and part-level `assert constraint` are **not exercised anywhere in the existing corpus** (flagged in the WI-009 design). Before replicating them across the plant: write ONE cross-calc binding and ONE `assert constraint`, validate that it parses and resolves (`uv run agentic-mbse validate` / syside), and only then build out the rest. Any gap is a `sysml-codegen`/syside finding, recorded — not worked around in the model.

## Success Criteria

- `'MFE Power Plant'` composes the WI-009 subsystems and binds the full physics→cost→LCOE pipeline.
- Cross-calc binding and part-level assert constraint validated on first use, then replicated.
- Net electric, LCOE, and a per-account CAS breakdown exposed as derived attributes.
- All files parse clean (`uv run agentic-mbse validate` Level 1, 0 errors); IFE + WI-009 files still parse.
- Every quantitative value carries a Source/Ref/Basis citation to 1costingFE (MR-4); no concept-specific values (MR-3).
- Account coverage + any pass-throughs documented for Stage-3 follow-up.

## Related Artifacts

- Epic: `work/backlog/epic-mfe-cost-modeling.md` (Item 2)
- Architecture: WI-009 design Layers 2–3 (the plant idiom + variation mechanism); AD-005, AD-006, AD-007
- IFE precedent: `models/designs/generic_ife/ife_plant.sysml`
- Formula source: 1costingFE `/home/reid/1cfe/1costingfe` (steady-state layers)

## Completion (2026-07-13)

Implemented. Files: `models/designs/generic_mfe/mfe_plant.sysml` (abstract `'MFE Power Plant'`), `generic_mfe/mfe_subsystems.sysml` (shared + BOP costed components), `models/library/analyses/mfe_account_costs.sysml` (9 concept-agnostic account cost calcs).

- **Wiring de-risk PASSED**: cross-calc binding, part-level `assert constraint`, and `capital_cost`-from-calc redefinition all validate and survive extraction (L6 binding/constraint/redef-drop = 0). Corpus gap flagged in the WI-009 design is closed.
- **Forward-pass fix**: WI-009's power balance now exposes `p_th`/`p_the`/`p_et` as outputs; the plant aliases them from `pb`, so the cost accounts scale with forward-computed powers (no injected power values).
- **CAS coverage**: bottom-up/scaled — magnet, blanket, shield, structure, vessel (shell only), power supplies, divertor, heating, BOP (CAS23-26), contingency (CAS29), indirect (CAS30). Pass-through (Stage-3 deepening): buildings (CAS21), preconstruction (CAS10/20), special materials (CAS27), O&M (CAS70). IDC handled inside LCOE DCF.
- **Money unit**: dollars ($) throughout; WI-011 supplies unit costs in $ (1costingFE M$ × 1e6).
- **Validation**: Level 1 clean across all files; L3/4/5 pass; L6 shows only expected abstract-layer flags (rollup "references design attributes" + "never instantiated") that clear when WI-011 instantiates the plant.
- **Watch item for codegen**: confirm the per-account rollup attributes extract/compute correctly once the plant is instantiated (WI-011).
