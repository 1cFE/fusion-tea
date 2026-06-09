---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T08:15:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #f881a24 (DATA_GROUNDED flag for placeholder/undisclosed-design-point concepts)"
patch_class: "methodological_flag + spec_anchor"
---

# Analyst Methodological Flag: DATA_GROUNDED = False (Pale Blue Fusion CHARM)

**Why this source exists.** Pale Blue Fusion has disclosed **no quantitative
reactor parameters** for the CHARM commercial plant — no geometry, fields,
densities, temperatures, confinement times, or fusion power. The current
model_setup.py is an honest placeholder: it carries the `MIRROR`+`PB11`
class membership and a single `r_bore` value (derived from radial-build
arithmetic, not company disclosure), and runs against pure library defaults
for everything else.

The `DATA_GROUNDED = False` constant is a deliberate methodological flag
read by the explorer extractor to **suppress the headline LCOE** in
cross-concept views (cost landscape, comparison summary), so the concept
doesn't appear with fake-precise economics. The CAS breakdown still renders
so reviewers can see the library-default structure, but the LCOE number is
intentionally hidden.

**This flag must survive cold-start regen.** Without it, the explorer will
silently start displaying the placeholder LCOE as if it were a real
prediction.

## The directive — module-level Python constant

`model_setup.py` MUST contain, at module level (above the spec dict):

```python
DATA_GROUNDED = False
```

A leading comment block should explain why:

```python
# Mirror of the data_grounded=False flag passed to print_cas_breakdown
# below — read by the explorer extractor to suppress headline LCOE in
# cross-concept views (cost landscape, comparison summary). The CAS
# breakdown still renders so reviewers can see library-default structure.
# (analysis.md §5: "no quantitative reactor parameters... are disclosed").
DATA_GROUNDED = False
```

The `data_grounded=False` flag must also appear in the `print_cas_breakdown()`
call at the bottom of model_setup.py, matching the module-level constant.

## Verified spec values

| Parameter | Value | Justification |
|-----------|-------|---------------|
| `r_bore` | 2.75 m | Derived from radial build: plasma_t (1.5 m library default) + blanket_t (0.6) + ht_shield_t (0.25) + structure_t (0.15) + vessel_t (0.1) = 2.6 m + plasma_t = 2.75 m. Library defaults `r_bore` to 1.85 m, which under-sizes the coil bore for an open-ended mirror. |
| `P_native` | 150.0 MWe | Design Point specification (operator-authored, no public source) |
| `ConfinementConcept` | `MIRROR` | Open-ended mirror geometry |
| `Fuel` | `PB11` | Pale Blue's published fuel choice (aneutronic). `Fuel.PB11` activates the correct near-aneutronic cost scaling: `blanket_unit_cost_pb11` |

## Critical do-not-set parameters

- **Most spec keys** — the analysis explicitly states "no quantitative reactor
  parameters... are disclosed." Do NOT populate the spec dict with invented
  values to make the cold-start "feel complete." Empty / minimal spec is the
  honest representation of "we don't know what Pale Blue is doing."
- **`Fuel = DT`** must NOT be set. Pale Blue's published fuel is PB11; using
  DT would silently activate D-T cost scaling (tritium breeding, neutron
  shielding) that doesn't apply.
- **Any non-PB11-derived `eta_*` overrides** — no design-point physics is
  disclosed to justify deviating from library archetype defaults.

## Model directive (machine-parseable)

```yaml
model_directives:
  module_constants:
    DATA_GROUNDED: false      # critical methodological flag — read by explorer
  spec:
    r_bore: 2.75              # radial-build-derived; library default 1.85m under-sizes coil bore
  P_native: 150.0
  ConfinementConcept: MIRROR
  Fuel: PB11
  do_not_set: "all spec keys not listed above — design point not disclosed"
  rationale: "Pale Blue Fusion CHARM placeholder: no public quantitative parameters. DATA_GROUNDED=False flags this in the explorer."
  provenance: "operator-authored placeholder + methodological flag"
  cross_reference:
    explorer_filter: "DATA_GROUNDED=False suppresses headline LCOE in cost landscape and comparison views"
    similar_concepts: "Also DATA_GROUNDED=False: 02-acoustic-icf-sonofusion, 03-laser-icf-liquid-jet-target, 16-muon-catalyzed-fusion, 19-orbital-levitated-dipole, 28-hts-tokamak-full-hts, 35-polomac-magnetic-confinement"
```

## Sources cited (already in research corpus)

- analysis.md §5 statement of undisclosed parameters (the analysis itself
  documents the gap honestly)
- Existing iter-01/iter-02 Pale Blue Fusion sources for class-membership
  context

## Maintenance

If Pale Blue Fusion publishes a quantitative design point, **remove the
`DATA_GROUNDED = False` flag** and replace the placeholder spec with sourced
values. This source becomes historical.
