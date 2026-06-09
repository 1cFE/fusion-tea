---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T07:55:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #b5a1a00 (fusion-power-into-p_house transcription error fix)"
patch_class: "spec_anchor"
---

# Analyst-Verified Spec Anchors: Type One Stellarator

**Why this source exists.** Documents the verified spec values for Type One
Energy's Stellarator design point, and specifically documents the
fusion-power-into-`p_house` transcription error fixed in PR `b5a1a00`. A
prior regen mis-set `p_house = 800 MW` with comment "fusion power" — a
transcription error of fusion power into the housekeeping slot, same class
of bug as the `p_input` errors caught on concepts 05/09. Drove every
p_th-scaled CAS22 account upward and inflated LCOE to ~$285.

## Verified spec values (transcribe verbatim)

| Parameter | Value | Primary source |
|-----------|-------|----------------|
| `R0` (major radius) | 12.5 m | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 |
| `plasma_t` (minor radius) | 1.25 m | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 |
| `B` (on-axis magnetic field) | 9.0 T | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 |
| `p_input` (auxiliary ECRH) | 20.0 MW | cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 |
| `elon` | 1.0 | Stellarators typically ~1 (not specified in sources) |
| `P_native` | 350.0 MWe | Copied from the analysis Design Point block |
| `ConfinementConcept` | `STELLARATOR` | Class membership |
| `Fuel` | `DT` | Confirmed |

## Critical do-not-set parameters

- **`p_house`** must NOT be in spec. It's library-default
  (~4 MW housekeeping for a stellarator). Setting `p_house = 800` (mistakenly
  copying the fusion power value into the housekeeping slot) drives every
  p_th-scaled CAS22 account upward, inflating LCOE to ~$285. This is the same
  class of transcription error as the `p_input = fusion_power` bug seen on
  concepts 05 and 09 — fusion power belongs to neither slot; it's library
  back-solved via the inverse power balance.
- **`p_fus`** must not be in spec — library back-solves via inverse power balance.
- **No `eta_*` overrides** unless the design point's physics genuinely differs
  from the STELLARATOR + RANKINE archetype default.

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    R0: 12.5
    plasma_t: 1.25
    B: 9.0
    p_input: 20.0
    elon: 1.0
  P_native: 350.0
  ConfinementConcept: STELLARATOR
  Fuel: DT
  do_not_set:
    - p_house        # library default ~4 MW for stellarator; prior regen mis-set to 800 MW (fusion power) — see PR b5a1a00
    - p_fus
    - eta_p
  rationale: "Type One Energy Stellarator design point from Cambridge published parameters."
  provenance: "direct"
  notes:
    - "p_input = 20 MW is auxiliary ECRH — NOT fusion power, NOT housekeeping."
    - "F9 ratio validator extension for p_house tracked — prevent regression of the fusion-power-into-p_house error class."
```

## Sources cited (already in research corpus)

- `cambridge-core-services-aop-cambridge-core-content-view.md` §2.4 Table 1 — primary

## Maintenance

If Type One Energy publishes an updated Infinity One stellarator design or
the underlying Cambridge paper is revised, supersede with a new source.
