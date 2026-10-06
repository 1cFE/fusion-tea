# Probe P2 — two sub-part retypes in one copied instance, and the instance count

Design § 7 P2 (K7), extended by what it found about K21. Run 2026-09-30 on scratch copies.

## What was run

The P1 probe tree (`sources/probe_variants.sysml`, `sources/make_probe_design.py`) in three shapes, each generated with `sysml-codegen generate`:

| Shape | Instances of `'MFE Power Plant'` | Result | Log |
|---|---|---|---|
| staged Stellaris file plus two copies `probe_a`, `probe_b` (the design's three-instance package) | 3 (813-module graph) | **refused**: `REGISTRY_CLASS_NAME_COLLISION` | `evidence/generation-three-instances.log` |
| staged Stellaris file plus `probe_a` | 2 (540-module graph) | **refused**: `REGISTRY_CLASS_NAME_COLLISION` | `evidence/generation-two-instances.log` |
| `probe_a` alone (the Stellaris file left out of the tree) | 1 | generated and sealed (274-module graph; the hunked reference alone is 267) | `evidence/generation-one-material-instance.log` |

The collision is in module class names, before any file is written. Two families collide:

- the plant-definition aggregation modules, which codegen names by the definition rather than the instance: `MfePowerPlant_bop_capitalModule`, `…cas20_capitalModule`, `…cas22_capitalModule`, `…cas23_to_28_capitalModule`, `…cas2x_pre_contingencyModule`, `…overnight_capitalModule`, `…powercore_capitalModule`, `…reactor_equipment_subtotalModule`, `…replacement_cost_per_eventModule`, `…total_capitalModule` — each `<- ['mfe_plant.mfe_power_plant.<name>Module']` once per instance, identical strings;
- four `buildings` modules whose grandparent alias (`Buildings_…`) cannot separate `stellarator_09.stellaris.buildings` from `stellarator_09_probe.probe_a.buildings`.

The first family cannot be fixed by renaming a scope in the model: the colliding names do not contain the instance. So no package can hold two instances of `'MFE Power Plant'` on this codegen.

## Result

- **The two retypes: PASS.** In the single-instance package, `part :>> magnet : 'Probe Magnet System'` and `part :>> cryoplant : 'Probe Cryoplant'` in one copied instance parse (`syside check` passed), generate, and route every consumer to the variants (P1 table).
- **The three-instance package: refused by the toolchain.** This is a generation refusal, not a cost.

## Fallback taken

Design K21's stated fallback: "split into per-instance packages from the same staged tree, which changes only the build and route, not the model." The build generates three packages from one staged source set:

- `reference`: the 42 staged twin files with the 15 hunks (the Stellaris design file byte-identical);
- `rebco` and `nb3sn`: the same staged files without the Stellaris design file, plus Round 1's library, the variants library, and that material's design file.

Because a generation unit may hold only one instance, the materials design file is written as two files, `rebco_material.sysml` and `nb3sn_material.sysml`, both in package `stellarator_09_materials`, so the entry-key prefixes stay exactly as design § 5.1 names them. They are never staged together. The SysML definitions, bindings and edit list are unchanged.

What the split removes: the coupling that D4 guarded against (a case now evaluates only its own material package, so the unselected material instance does not run and cannot refuse a case), and the per-case reference witness of § 1.5 (the reference package is a separate package; its parity is proven by the build regression, the reference manifest baseline and test 1). What it adds: three packages, three manifests and three seam pins instead of one.
