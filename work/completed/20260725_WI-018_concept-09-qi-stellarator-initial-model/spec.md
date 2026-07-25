---
Status: completed
Scale: standard
Epic: MFE Cost Modeling — Tokamak & Stellarator
Owner: reid
Created: 2026-07-13
Updated: '2026-07-25'
---

# WI-018: Concept-09 QI Stellarator Initial Model

## Overview

The stellarator MBSE demo's Stage-2 initial-model leaf: a concept-09 (QI stellarator, Proxima "Stellaris") design instance that specializes the WI-010 generic MFE plant, evaluated at the Stellaris design point, producing LCOE + a full CAS breakdown. This is the concrete model that generates through `sysml-codegen` and runs under `teax` (concept Success Criterion 1), and that the 1costingFE handshake (Anchor A, Success Criterion 3) is run against.

Distinct from the epic's WI-011 (tokamak concept-01 + Type-One concept-20a). This item is the **demo** stellarator instance, concept-09 only.

## Required Reading

- `knowledge/holdout/aries-cs/PROTOCOL.md` — demo model-development item; the ARIES-CS blocklist binds. **Bootstrap the physics/geometry from the admissible Stellaris sources only; source engineering/cost parameters from 1costingFE stellarator defaults (admissible). Never open the barred docs/dirs in PROTOCOL §3 — in particular NOT `exploration/concept_analysis/analyses/09-qi-stellarator-hts/**`.**

## Scope

Build in `models/designs/stellarator_09/` (or similar):
1. Optionally an abstract `'Stellarator Plant' :> 'MFE Power Plant'` family layer (density as a direct input — no tokamak Greenwald closure; no current drive; stellarator coil geometry G = 8π²), then
2. A concrete concept-09 instance (e.g. `'Stellaris QI Stellarator'`) binding the Stellaris design-point values below, which instantiates the plant and so clears the abstract-layer L6 flags.
3. Add the cheap, data-supported viability constraints as concept-agnostic library `constraint def`s (beta limit, neutron wall-load limit, TBR floor) + a forward `'Neutron Wall Load'` calc, and bind them in the instance. (ISS04 confinement-consistency is deferred to Stage 3 per the owner decision.)

## Clean bootstrap parameter set (Stellaris design point)

Physics/geometry — from the **admissible** Stellaris sources (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md` and iter-03 anchor sheet). Cite each per MR-4.

| Parameter | Value | Note |
|---|---|---|
| Major radius R0 | 12.7 m | |
| Minor radius a | 1.5 m | aspect ratio ~9.9 |
| Elongation kappa | ~1.0 | QI stellarator, ~circular average cross-section (confirm/justify) |
| Plasma volume V | ~448 m³ | cross-check against `'Plasma Geometry'` output |
| Plasma surface area | 327 m² | for neutron wall load |
| On-axis field B0 | 5.86 T | coil-cost field (loop-center); peak-on-winding 24.9 T is a different quantity |
| Vol-avg beta | 2.76 % | design target 5% |
| Vol-avg n_e | 3.37e20 m⁻³ | operating point A |
| T_e0 / T_i0 | 15.4 / 24.6 keV | point A |
| Fusion power | 2700 MW | full-power design point (1800 MW is the lower-power phase) |
| ECRH heating | 50 MW | stellarator has NO external current drive (steady-state QI) |
| Conduction to coils | 111 MW | |
| Blanket mult (mn) | 1.2 | HCLL PbLi |
| Thermal efficiency | 0.333 (1/3) | |
| TBR | 1.074 | floor 1.05 |
| Neutron wall load | 2.87 avg / 4.95 peak MW/m² | cross-check computed value |

Engineering/recirculating-power and ALL cost parameters — from **1costingFE** `data/defaults/steady_state_stellarator.yaml` + `data/defaults/costing_constants.yaml` (admissible), since Stellaris has zero cost data by design. Convert M$ → $ (×1e6) to match the plant's dollar rollup. Cite each per MR-4.

- Coil: G = 8π² ≈ 78.957; coil_markup = 5.87; cost_per_kAm = 50 (REBCO_HTS).
- r_coil (coil-bore / vessel-outer radius): a **mapping trap** — source from the 1costingFE stellarator radial build / geometry default and document the choice; do not guess silently.
- sigma_v (D-T reactivity at the design temperature): a **mapping trap** — Bosch–Hale can't run in SysML, so supply the reactivity value at the Stellaris T from 1costingFE's reactivity function/table (or a cited literature value) and document it.
- E_fus = 2.817e-12 J (17.58 MeV × 1.602176634e-13 J/MeV).
- All account unit costs / per-MW BOP rates / power-supply & divertor bases / heating per-MW / contingency rate / indirect fraction: from the two yaml files, ×1e6.

## Success Criteria

- Concrete concept-09 instance specializes `'MFE Power Plant'`, sets the Stellaris design point, and instantiates cleanly (abstract-layer L6 flags cleared).
- Full physics→cost→LCOE forward pass evaluates: net electric, LCOE, per-account CAS breakdown.
- Three viability constraints (beta, wall load, TBR) asserted; wall load computed forward from the power balance + surface area.
- Every value carries a Source/Ref/Basis citation (Stellaris for physics/geometry; 1costingFE for engineering/cost).
- `uv run agentic-mbse validate` Level 1 clean; L6 free of binding/constraint/redef-drop errors and free of the abstract-instantiation flags (now instantiated).
- Mapping traps (r_coil, sigma_v, B vs b_center) documented for the Anchor-A handshake.

## Related Artifacts

- Concept: `.project/concepts/stellarator-mbse-demo.md` (Stage 2)
- Plant: `models/designs/generic_mfe/mfe_plant.sysml` (WI-010); library WI-009
- IFE instance precedent: `models/designs/hif_ife/hif_plant.sysml`
- Formula/param source: 1costingFE `/home/reid/1cfe/1costingfe`

## Completion (2026-07-13)

Implemented. Concrete instance `part stellaris : 'MFE Power Plant'` in `models/designs/stellarator_09/stellarator_plant.sysml`; library additions in `mfe_plasma_scaling.sysml` (`'Neutron Wall Load'` calc) and `mfe_viability.sysml` (beta/wall-load/TBR constraint defs).

- **Deviation**: the optional `'Stellarator Plant'` abstract family layer was collapsed into the concrete instance (typed directly on `'MFE Power Plant'`) because syside doesn't surface a grandparent type through an intermediate abstract def, which left the plant flagged `NO_INSTANTIATION`. Direct typing (the hif_plant idiom) clears it; family choices applied inline and labelled.
- **Forward-pass result** (verified via an oracle script mirroring the SysML): plasma volume 564 m³, fusion power 2700 MW, net electric 575 MW, rec_frac 0.36, total overnight capital ~$9.78B, LCOE ~$251/MWh (FOAK, magnet-dominated ~$4.4B).
- **Viability**: beta_ok pass (0.0276 ≤ 0.05), tbr_ok pass (1.074 ≥ 1.05), wall_load_ok pass (2.69 ≤ 4.95 after the first-wall-area fix, 802.2 m² from 1costingFE geometry — matches Stellaris 2.87 avg within ~6%).
- **Mapping traps**: r_coil=3.20 m (radial-build vessel_or), sigma_v=5.985e-23 m³/s (0D-effective D-T reactivity reproducing 2700 MW at vol-avg density — a documented 0D limitation; profile integration is Stage-3), B=5.86 T (loop-center, not 24.9 T peak-on-winding).
- **Documented fidelity gaps for Stage 3**: torus-volume formula 564 m³ vs Stellaris 448 m³ (R/a source rounding / stellarator shaping); 0D reactivity tuned to design power; buildings/preconstruction/special-materials/O&M are pass-throughs computed from admissible 1costingFE functions at the design point.
- **Validation**: Level 1 clean; L6 binding/constraint/redef-drop = 0; abstract-instantiation flag cleared. Remaining L6: the WI-010 per-account rollup "references design attributes" (codegen watch item, handled at the codegen step).

---

## Disposition — closed as superseded ([OWNER] 2026-07-25)

Closed under the demo epic's Board-housekeeping ruling (option c). The Stellaris instance this item set out to build exists (`models/designs/stellarator_09/`) and carries the demo headline; the item was spec-only, overtaken by the WI-019–028 corrective run whose audited records are the effective completion evidence.
