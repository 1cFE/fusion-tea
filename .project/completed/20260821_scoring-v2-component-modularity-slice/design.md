# Design: Scoring V2 — `component_modularity` Embedding Group (Slice 2)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-17
**Branch:** concept-downselect

---

## The whole thing

For each concept, modularity is one number:

```
component_modularity(concept) = sum over 7 subsystems of [ rating × weight ]
```

- **7 subsystems**: vessel, coils, blanket, bop, fuel_cycle, aux, civil.
- **rating** (1–5) per subsystem, per concept: a deterministic if/elif over a few taxonomy columns from `table.csv`. Same function applied to every concept.
- **weight** (fraction) per subsystem, per concept: that subsystem's share of total capex, computed by summing `model_output.txt` line items via one static `CAS → subsystem` dict.

The 7 weights for one concept sum to 1. The rating × weight sum stays in 1–5.

No LLM. No new extraction infrastructure. No fallbacks.

## Features per concept

`features/{cid}.yaml` gains exactly these fields. Nothing else.

**Taxonomy (from `table.csv` columns, populated by `lib/extractors/taxonomy.py`):**

Already in slice 1: `confinement_family`, `mfe_topology`, `ife_driver`, `mif_method`, `tokamak_shape`, `stellarator_type`, `magnet_type`, `fuel`, `tritium_breeding`, `neutron_management`, `operation_mode`, `driver_technology`.

Added by slice 2: `primary_heating`, `energy_capture`.

**Cost shares (from `model_output.txt`, populated by new `lib/extractors/cost_model.py`):**

`w_vessel`, `w_coils`, `w_blanket`, `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil`.

## The 7 rating functions

All live in `embeddings/rulebook.py` under the `component_modularity` group. Each is a tiny if/elif over taxonomy. Bands are transcribed from the xlsx "Driver Lookups" tab.

```python
@embedding("vessel_rating",
           inputs=["confinement_family", "mfe_topology", "tokamak_shape"])
def vessel_rating(confinement_family, mfe_topology, tokamak_shape):
    if confinement_family == "MIF":                                return 5
    if mfe_topology == "Tokamak" and tokamak_shape in ("Compact","Spherical"):
                                                                   return 4
    if mfe_topology == "Tokamak":                                  return 2
    if mfe_topology == "Stellarator":                              return 2
    if confinement_family == "IFE":                                return 3
    return 3
```

```python
@embedding("coils_rating",
           inputs=["magnet_type", "mfe_topology", "ife_driver",
                   "tokamak_shape", "stellarator_type"])
def coils_rating(magnet_type, mfe_topology, ife_driver, tokamak_shape, stellarator_type):
    if "DPSSL" in (ife_driver or ""):                              return 5
    if "Pulsed EM" in (magnet_type or ""):                         return 5
    if "Flashlamp" in (ife_driver or "") or "KrF" in (ife_driver or ""):
                                                                   return 2
    if mfe_topology == "Tokamak" and "HTS" in (magnet_type or "") and tokamak_shape in ("Compact","Spherical"):
                                                                   return 4
    if mfe_topology == "Stellarator" and "HTS" in (magnet_type or ""):
                                                                   return 3
    if mfe_topology == "Stellarator":                              return 2
    if mfe_topology == "Tokamak" and "LTS" in (magnet_type or ""): return 2
    return 3
```

```python
@embedding("blanket_rating",
           inputs=["fuel", "tritium_breeding", "mfe_topology"])
def blanket_rating(fuel, tritium_breeding, mfe_topology):
    if fuel in ("p-B11", "D-He3", "D-D"):                          return 5
    if "FLiBe"  in (tritium_breeding or ""):                       return 5
    if "HCPB"   in (tritium_breeding or "") or "pebble" in (tritium_breeding or "").lower():
                                                                   return 4
    if mfe_topology == "Stellarator":                              return 2
    if "Heavy"  in (tritium_breeding or ""):                       return 2
    return 3
```

```python
@embedding("bop_rating",
           inputs=["energy_capture", "operation_mode"])
def bop_rating(energy_capture, operation_mode):
    if "Direct" in (energy_capture or ""):                         return 4   # modular pulsed-power capture (Helion-class)
    if "sCO2"   in (energy_capture or ""):                         return 5
    if "Thermal" in (energy_capture or "") and operation_mode in ("Steady-state","Quasi-steady"):
                                                                   return 4
    if "Thermal" in (energy_capture or "") and operation_mode == "Pulsed":
                                                                   return 3
    return 3
```

```python
@embedding("fuel_cycle_rating",
           inputs=["fuel", "tokamak_shape", "mfe_topology"])
def fuel_cycle_rating(fuel, tokamak_shape, mfe_topology):
    if fuel in ("p-B11", "D-He3", "D-D"):                          return 5
    if fuel == "D-T" and mfe_topology == "Tokamak" and tokamak_shape in ("Compact","Spherical"):
                                                                   return 3
    if fuel == "D-T" and mfe_topology == "Tokamak":                return 2
    if fuel == "D-T" and mfe_topology == "Stellarator":            return 3
    if fuel == "D-T":                                              return 3
    return 3
```

```python
@embedding("aux_rating",
           inputs=["magnet_type", "confinement_family", "tokamak_shape"])
def aux_rating(magnet_type, confinement_family, tokamak_shape):
    if confinement_family == "MIF" and "HTS" in (magnet_type or ""):
                                                                   return 5
    if "HTS" in (magnet_type or "") and tokamak_shape in ("Compact","Spherical"):
                                                                   return 3
    if "HTS" in (magnet_type or ""):                               return 4
    if "LTS" in (magnet_type or ""):                               return 2
    return 3
```

```python
@embedding("civil_rating",
           inputs=["fuel", "neutron_management", "mfe_topology", "tokamak_shape"])
def civil_rating(fuel, neutron_management, mfe_topology, tokamak_shape):
    if fuel in ("p-B11", "D-He3"):                                 return 5
    if "Heavy" in (neutron_management or ""):                      return 2
    if mfe_topology == "Stellarator":                              return 2
    if mfe_topology == "Tokamak" and tokamak_shape in ("Compact","Spherical"):
                                                                   return 4
    if mfe_topology == "Tokamak":                                  return 2
    return 3
```

## The CAS → subsystem dict

The whole content of `lib/extractors/cost_model.py`'s classification, transcribed from `01-hts-compact-tokamak/model_output.txt`. Codes not listed are ignored (financial, indirect, O&M, fuel, IDC, contingency).

```python
CAS_TO_SUBSYSTEM = {
    # vessel
    "C220105": "vessel", "C220106": "vessel", "C220108": "vessel",
    # coils / driver
    "C220103": "coils",  "C220107": "coils",
    # blanket & first wall
    "C220101": "blanket", "CAS27":  "blanket",
    # power conversion / BOP
    "C220109": "bop", "C220200": "bop",
    "CAS23":   "bop", "CAS24":   "bop", "CAS26": "bop",
    # fuel cycle
    "C220112": "fuel_cycle", "C220400": "fuel_cycle", "C220500": "fuel_cycle",
    # auxiliaries
    "C220104": "aux", "C220300": "aux", "C220600": "aux", "C220700": "aux",
    "CAS25":   "aux", "CAS28":   "aux",
    # civil / shielding
    "C220102": "civil", "C220111": "civil",
    "CAS10":   "civil", "CAS21":   "civil",
}
```

**`cost_model` extractor behavior:** parse `analyses/{cid}/model_output.txt`, sum `$` per bucket, divide each by total bucket $. Write the 7 `w_*` features into `features/{cid}.yaml`. Codes seen in the file that aren't in `CAS_TO_SUBSYSTEM` are ignored. Codes in the dict that don't appear in the file contribute 0 to that bucket.

**If `analyses/{cid}/model_output.txt` does not exist:** the extractor writes nothing. The 7 `w_*` features stay absent from `features/{cid}.yaml`. No fallback.

## The aggregate embedding and the M&SO blend

```python
@embedding("component_modularity_aggregate",
           inputs=["vessel_rating","coils_rating","blanket_rating",
                   "bop_rating","fuel_cycle_rating","aux_rating","civil_rating",
                   "w_vessel","w_coils","w_blanket","w_bop",
                   "w_fuel_cycle","w_aux","w_civil"])
def component_modularity_aggregate(...):
    ratings = [vessel_rating, coils_rating, blanket_rating, bop_rating,
               fuel_cycle_rating, aux_rating, civil_rating]
    weights = [w_vessel, w_coils, w_blanket, w_bop, w_fuel_cycle, w_aux, w_civil]
    if any(w is None for w in weights):
        return None
    return sum(r * w for r, w in zip(ratings, weights))
```

Returning `None` means "no contribution" — the concept's row in the score table records 0 for this embedding's contribution and the `mso_evidence` column flags it. No score is fabricated.

`weights/default.yaml`:

```yaml
manufacturability_scale_out:
  # plant-level modularity group (slice 1) — halved for the 50/50 blend
  min_viable_device_scale:      0.15
  hardware_topology_complexity: 0.15
  unit_multiplicity:            0.10
  subsystem_stack_burden:       0.10
  # component modularity group (slice 2) — single aggregate
  component_modularity_aggregate: 0.50
```

Slice-1 preservation: set `component_modularity_aggregate: 0.0`, restore slice-1 weights to 0.30 / 0.30 / 0.20 / 0.20, and the slice-1 acceptance numbers (Helion 4.80, CFS 2.90, Stellarator 1.50) come back.

## The reference concepts (ITER, NIF, Inertia/LIFE)

The xlsx Worked Examples include three concepts not in `table.csv`. They are added the **same way as any other taxonomy concept**: three new rows in `table.csv` with taxonomy columns filled in from the xlsx Concept Multipliers row + public info, and a `model_output.txt` written for each. Concept IDs: `00a-iter`, `00b-nif`, `00c-inertia-life`. This is user work (per the no-fallbacks rule). Once added, the same extractors and same embeddings produce their scores.

## Acceptance test

One test, in `tests/scoring_v2/test_component_modularity.py`:

For each of the six xlsx worked examples (`01-hts-compact-tokamak`, `08-frc-w-direct-conversion`, `10-large-scale-stellarator`, `00a-iter`, `00b-nif`, `00c-inertia-life`), assert that the value of `component_modularity_aggregate` is within ±0.4 of the xlsx Final Modularity Score (5.0, 4.65, 2.18, 1.4, 1.83, 4.15 respectively — re-read from the xlsx for the exact numbers).

A second test asserts slice-1 preservation: zero the aggregate weight, restore plant-level weights, M&SO matches slice-1 within ±0.01.

## Required invariants

- `score.py`, `embeddings/rulebook.py`, `lib/schema.py`, `lib/feature_io.py`, `lib/extractors/cost_model.py` import no LLM client.
- Every rating function returns an integer 1..5.
- The 7 `w_*` features for a concept either all exist and sum to 1.0 ± 1e-6, or all are absent.
- No defaults, no family fallbacks, no Concept-Multipliers-tab values anywhere in code or data.

## Versioning policy (FR-7)

**Decision (slice 2): deferred to slice 3.** No `version:` field on `@embedding`,
no bump rule. Rationale:

- This slice grows the embedding count from 4 to 12 and adds the new
  `component_modularity_aggregate` blend, but the schema-vs-feature-file
  contract has not yet exhibited version skew. Every `features/*.yaml` is
  regenerated by `extract.py` on demand; there are no long-lived feature
  files written by one schema version and read by a later one.
- The first real version-skew pressure will land in slice 3, when an
  embedding's band logic gets revised in response to a documented
  xlsx-collapse gap (e.g., tightening `coils_rating` for HTS+compact tokamaks
  — see `implementation_notes.md`). Revising an embedding without a version
  marker leaves no audit trail of which scoring rules produced a given
  `scores/table.csv`.
- Bound to: slice 3 (next `component_modularity` revision). If slice 3 lands
  without versioning, this deferral note is the bug.

Shape sketched for future reference (not implemented):

```python
@embedding("coils_rating", inputs=[...], version="2025-05-17")
def coils_rating(...): ...
```

Bump rule: any change to band logic or input set requires a new `version`
string (ISO date is fine). `score.py` writes the active version per embedding
into a sidecar `scores/embeddings.lock`. Diffing the lock identifies which
rules changed between runs.

## Risks

- **xlsx-collapse may fail on stellarator (Type One).** Stellarator's xlsx Final is 2.18 with a 0.75 family multiplier. Without that multiplier, our ratings would have to land ~2.9 raw to match — and the rules above probably overshoot. If so, the diagnosis points at coils and blanket ratings under-discriminating non-planar geometry. Fix: tighten those two rules. Documented negative result is acceptable per FR-5.
- **CAS dict drift.** Cost models written outside `01-hts-compact-tokamak`'s shape may use codes not in the dict. Those codes are silently ignored. The extractor should log unrecognized codes; new codes get added to the dict explicitly.
- **`primary_heating` not consumed.** Added to the feature set "just in case" but no rating uses it. If true after writing the rules, drop it.

---

**Next Step:** After approval → `/_my_plan`.
