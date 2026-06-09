---
source: "analyst-derived"
source_type: "analyst-patch"
extracted_at: "2026-06-09T08:00:00+00:00"
author: "Mallory Snowden"
provenance_pr: "fusion-tea PR #302c1bf (drop B0 from spec; document plasma_volume omission)"
patch_class: "spec_anchor_with_architectural_constraint"
---

# Analyst-Verified Spec + Architectural Workarounds: OpenStar Levitated Dipole

**Why this source exists.** Documents two deliberate architectural choices for
the OpenStar levitated dipole model that a cold-start regen will likely get
wrong without explicit guidance:

1. **`B` (= B0) field must NOT be in spec.** The arxiv reference cites Simpson's
   B_max = 23 T peak field at the coil, but this is **not** in
   `CostingInput.model_fields` and `forward()` would silently drop it. The
   coil center field used for cost (`b_center`) is the library default
   6.26 T (= B_max/3.67 via Simpson's peak_to_center_ratio), so no override
   is needed. F7 (spec-key whitelist) now rejects `B` for DIPOLE concepts.

2. **`plasma_volume` is intentionally OMITTED.** Simpson's geometric volume
   of 13,600 m³ would drive the MFE radiation calc out of its calibrated
   range (formulas assume uniform profile; dipole is highly peaked, with
   the radiating core < 10% of the geometric volume per Hasegawa-Mauel
   scaling). The library default `plasma_volume = 200 m³` in
   `steady_state_dipole.yaml` is NOT the geometric volume — it's a
   calibrated effective value that produces the right p_fus (~700 MW)
   against Simpson Reactor A. A proper `radiation_peaking_factor` field is
   filed as a 1costingfe issue; until then, the library default produces
   the physically correct answer.

## Verified spec values (transcribe verbatim)

| Parameter | Value | Primary source |
|-----------|-------|----------------|
| `R0` (Core magnet outer radius) | 5.3 m | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5, §Table 7 |
| `p_input` (Auxiliary ICRH) | 44.5 MW | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5, §Table 9 |
| `P_native` | 208.0 MWe | arxiv-2602-20564-dt-dipole-power-plants.md §Table 5 |
| `ConfinementConcept` | `DIPOLE` | Class membership |
| `Fuel` | `DT` | Confirmed |

## Critical do-not-set parameters

- **`elon` / `plasma_t`** — dipole geometry doesn't use tokamak-style elongation
  or minor radius. OMIT.
- **`B` (or `B0`)** — NOT in `CostingInput.model_fields`. Coil center field for
  cost is the library's `b_center = 6.26 T` (= B_max/3.67). Setting B=23
  (Simpson's B_max) would be silently dropped by `forward()`; F7 now rejects.
- **`plasma_volume`** — INTENTIONALLY OMITTED. Passing Simpson's geometric
  13,600 m³ drives MFE radiation calc out of calibrated range. Library default
  (200 m³ in `steady_state_dipole.yaml`) is a calibrated effective value, not
  geometric — produces correct p_fus (~700 MW) against Simpson Reactor A.
- **`eta_th`** — 0.40 from §4.4 matches library default RANKINE cycle.
  ENUM-owned, not spec-authorable. No override needed.
- **`p_fus`** — library back-solves via inverse power balance.

## Model directive (machine-parseable)

```yaml
model_directives:
  spec:
    R0: 5.3
    p_input: 44.5
  P_native: 208.0
  ConfinementConcept: DIPOLE
  Fuel: DT
  do_not_set:
    - elon              # dipole geometry doesn't use tokamak-style elongation
    - plasma_t          # dipole geometry doesn't use tokamak-style minor radius
    - B                 # F7 rejects; coil cost uses library b_center=6.26T
    - B0                # alias of B
    - plasma_volume     # intentionally omitted — see Hasegawa-Mauel peaking discussion
    - eta_th            # matches library RANKINE default; ENUM-owned
    - p_fus             # library back-solves
  rationale: "OpenStar dipole reactor design point from Simpson 2026 arxiv reactor study."
  provenance: "direct"
  architectural_notes:
    - "B_max = 23 T is Simpson's peak field; coil cost anchors to b_center = B_max/3.67 = 6.26 T (library default)."
    - "plasma_volume omission is a calibration choice; library's 200 m³ default is effective (calibrated against Simpson p_fus), not geometric."
```

## Sources cited (already in research corpus)

- `arxiv-2602-20564-dt-dipole-power-plants.md` §Table 5, §Table 7, §Table 9, §4.4 — primary

## Maintenance

If OpenStar publishes its own reactor parameters (currently using the arxiv
Simpson Reactor A as the design-point anchor), supersede with a company source.
