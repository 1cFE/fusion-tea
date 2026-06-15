---
date: 2026-06-15T11:56:24-07:00
researcher: Claude
topic: "Model rerun after costingfe adapter migration + 1costingfe upgrade"
tags: [report, costingfe, model-rerun, lcoe, adapter-migration]
status: complete
last_updated: 2026-06-15
---

# Report: Model Rerun After Adapter Migration + Library Upgrade

**Date**: 2026-06-15
**Trigger**: `refactor(concept-analysis): route model_setup forwards through costingfe.adapter`
**Command**: `uv run python exploration/concept_analysis/scripts/rerun_all_models.py`

## What this rerun captures

Two things changed since the committed `model_output.txt` files were last generated:

1. **The helper migration** (this branch) — the three-forward helper now invokes
   the library via `costingfe.adapter.run_costing` instead of `CostModel.forward`.
   This was verified **numerically identical** old-vs-new on the same library, so
   it contributes **zero** to the deltas below.
2. **The 1costingfe upgrade** — `1costingfe@master` was pulled to commit `b9b0a4c`
   (21 commits ahead). The committed outputs were generated against the *old*
   library, so every delta here is attributable to the library upgrade.

## Result

**41 concepts ran, 0 failed.** 15 `model_output.txt` files changed; 13 had a
changed headline LCOE (2 — `21-spherical-tokamak-hts`, `22-projectile-icf` —
shifted only in CAS sub-accounts that round to the same LCOE).

### LCOE changes

| Concept | Old | New | Δ | Family |
|---|---|---|---|---|
| 11-magnetic-mirror | 289.4 | 398.1 | **+37.6%** | Mirror |
| 32-laser-icf-french-national | 76.7 | 89.5 | +16.7% | IFE |
| 04-laser-icf | 80.4 | 92.8 | +15.4% | IFE |
| 30-laser-icf-nif-commercialization | 89.8 | 102.4 | +14.0% | IFE |
| 25-heavy-ion-beam-icf | 87.8 | 96.1 | +9.5% | IFE |
| 17b-laser-icf-fast-ignition | 119.5 | 127.9 | +7.0% | IFE |
| 26-laser-icf-indirect-drive | 105.4 | 112.7 | +6.9% | IFE |
| 18-p-b11-frc | 358.8 | 381.2 | +6.2% | Pulsed/aneutronic |
| 17a-laser-icf-hybrid-drive | 83.5 | 88.4 | +5.9% | IFE |
| 31-laser-icf-oec-architecture | 192.7 | 198.7 | +3.1% | IFE |
| 23-laser-icf-nanostructured-target | 381.9 | 393.0 | +2.9% | IFE |
| 07-maglif | 125.0 | 127.5 | +2.0% | MIF |
| 37-magnetized-target-inertial-fusion-mtif | 302.0 | 284.0 | **−6.0%** | MIF |

### Unchanged

All **magnetic-confinement (MFE)** concepts — tokamaks (01, 21\*, 28, 29, 33, 34,
39), stellarators (05, 09, 10, 20a, 20b, 36), FRC-DEC (08), levitated dipole (12),
spherical tokamaks (21\*) — and all **freeform** concepts (02, 16; and the
no-numeric-LCOE concepts 03, 06, 19, 35, 38) are unchanged.
(\* 21 changed in sub-accounts but not headline LCOE.)

## Why the changes land where they do

The shift is confined to **IFE / pulsed / mirror** concepts. The 21-commit
upgrade's costing-relevant changes are exactly in those domains:

- **IFE / pulsed (most of the table)** — the reactor-plant-equipment and
  lifecycle-replacement cost models changed (notably the commit *"Replace
  CAS220119 flat replacement fraction with lifecycle CAS72"*). On `04-laser-icf`,
  the **generic** (library-bare) CAS22 rose 795 → 1360 M$, driven by C220108
  (target factory / divertor, 184 → 680) and C220111 (installation, 75 → 145),
  cascading into CAS30/50/60/80/90 and the total. The net effect on the
  override-on 1 GWe LCOE is the +3–17% seen above.
- **Magnetic mirror (11, +37.6%)** — the upgrade added a mirror 0D model with
  central-cell length sizing (*"central cell beyond 50 m per Realta Hammir; coil
  cost scales with length"*). Mirror coil cost now scales with the longer central
  cell, raising LCOE. (Concept 06, the ungrounded Pale Blue mirror, emits no
  numeric LCOE and is unaffected.)
- **MFE (tokamak/stellarator/dipole)** — untouched by these commits, hence flat.

The lone decrease (`37-MTIF`, −6.0%) reflects the same CAS72 lifecycle-replacement
change netting favorably for that concept's accounting.

## Bottom line

The reruns are healthy (0 failures) and the deltas are explained: **the adapter
migration is cost-neutral; all movement is the deliberate 1costingfe upgrade**,
concentrated in IFE/pulsed/mirror cost models exactly as those commits intend.
The committed `model_output.txt` files are now consistent with `1costingfe@b9b0a4c`.

> Note: the concept-explorer's cost-landscape / ontology pages read these
> outputs; they will reflect the new numbers once rebuilt from this branch.
</content>
