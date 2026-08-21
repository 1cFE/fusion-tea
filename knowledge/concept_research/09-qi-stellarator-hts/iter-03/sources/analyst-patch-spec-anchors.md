---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T07:50:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea glossary refactor + spec-key whitelist (F7/F9 validators)"
patch_class: "spec_anchor"
---

# Analyst-Verified Spec Anchors: QI Stellarator HTS (Proxima Fusion Stellaris)

**Why this source exists.** Documents the verified spec values currently in
`exploration/concept_analysis/analyses/09-qi-stellarator-hts/model_setup.py`
and the critical do-not-set rules. A prior regen mis-set `p_input` to the
fusion power value (2700 MW), which would have back-solved to p_fus ≈ 13 GW
for a 1000 MWe plant and inflated LCOE to ~$303/MWh. The F9 validator
(p_input/P_native ≤ 0.5) now blocks this regression, but the patch source
also documents the correct value for cold-start regen.

## Verified spec values (transcribe verbatim)

| Parameter | Value | Primary source |
|-----------|-------|----------------|
| `R0` (major radius) | 12.0 m | stellaris-design-details.md §Table 1 |
| `B` (on-axis magnetic field) | 5.86 T | stellaris-design-details.md §Table 3 |
| `plasma_volume` | 448.0 m³ | stellaris-design-details.md §Table 1 |
| `plasma_t` (minor radius) | 1.38 m | Derived: V = 2π²·R₀·a² with R₀=12m, V=448 m³ → a≈1.38m. Drives `r_coil = vessel_or` in the bilinear coil cost (1costingfe master 52d95b9+) |
| `elon` (elongation) | 1.0 | Stellarators typically ~1 (analysis §5 parameter table) |
| `p_input` | 50.0 MW | stellaris-design-details.md §2.6, Table 1 (50 MW ECRH at 230-240 GHz) |
| `P_native` | 1000.0 MWe | Copied from the analysis Design Point block |
| `ConfinementConcept` | `STELLARATOR` | Class membership |
| `Fuel` | `DT` | Confirmed |

> **Errata (WI-023, 2026-07-18 — phantom-lineage / superseded rows):** the `B` = 5.86 T row cites a Table 3 text row that does not exist — the Table 3 image (`.../stellaris-design-details/images/page_003_table_0.png`) has no field row, and the published paper (iter-02 publikationen raw.pdf) contains no "5.86"; the Table 2/5 images print axis-averaged B₀ = **9.0 T**. The `plasma_volume` = 448 m³ and derived `plasma_t` ≈ 1.38 m rows are stale extraction artifacts: the images print V = **425 m³**, a = **1.3 m** (WI-022 errata record). See `work/active/WI-023_magnet-field-errata-B9/spec.md` §Evidence.

## Critical do-not-set parameters

- **`p_input` MUST be 50 MW** (auxiliary heating wallplug), NOT fusion power.
  Fusion power is library back-solved via the inverse power balance. Prior
  regen set p_input = 2700 (fusion power) which back-solved to p_fus ≈ 13 GW
  for a 1000 MWe plant — physically impossible and inflated LCOE to ~$303/MWh.
  F9 ratio check now blocks `p_input/P_native > 0.5`.
- **`p_fus`** must not be in spec — library computes from inverse power balance.
- **`eta_p=0.0276`** must NOT be set. This was previously mis-applied: 0.0276
  is the plasma β value from stellaris-design-details.md §2.3 (informational only),
  not a power-conversion efficiency. Power-conversion efficiencies are never
  spec keys (they're ENUM-owned by PowerCycle).
- **No `eta_*` overrides** unless the design point's physics genuinely differs
  from the STELLARATOR + RANKINE archetype default.

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    R0: 12.0
    B: 5.86
    plasma_volume: 448.0
    plasma_t: 1.38
    elon: 1.0
    p_input: 50.0
  P_native: 1000.0
  ConfinementConcept: STELLARATOR
  Fuel: DT
  do_not_set:
    - p_fus
    - eta_p
  rationale: "Stellaris design point from Proxima Fusion technical materials."
  provenance: "direct"
  notes:
    - "p_input is 50 MW ECRH wallplug power — NOT fusion power. F9 ratio check enforces p_input/P_native ≤ 0.5."
    - "Plasma β=0.0276 is informational only; do not pass as eta_p."
```

## Sources cited (already in research corpus)

- `stellaris-design-details.md` §Table 1, §Table 3, §2.3, §2.6 — primary
- Additional Proxima Fusion technical materials per concept dossier

## Maintenance

If Proxima publishes updated Stellaris design parameters, supersede with
a new source citing the disclosure. Keep this file for backward-traceability.
