# Taxonomy Schema Revision Proposals

**Status**: proposal — not yet scheduled as work
**Author**: Mallory Snowden
**Date**: 2026-05-07
**Source**: dossier audit against [schema.md](schema.md) + per-concept review

## Context

This document captures proposed revisions to the Phase 1a differentiation table schema, motivated by:

1. Several columns appear to encode information already implied by other columns (Neutron Management ≈ Fuel; Plasma State ≈ Confinement Concept + Operation Mode).
2. The blanket/breeder vocabulary is more granular than the cost model can use, while losing important architectural detail (Renaissance: Li-LiH + Pb pebbles).
3. The magnet vocabulary creates distinctions (`Pulsed EM`, `Self-confined`) that fragment what could be cleaner top-level categories.
4. Specific concepts are misclassified (Pacific Fusion as `Pulsed EM`; Renaissance forced into a value that loses the multiplier architecture).

LCOE impact is assessed against [1costingFE](https://github.com/1cFE/1costingfe) — the cost engine consumed by Stage 2 concept analysis.

**Important framing**: today's taxonomy fields are largely decorative for LCOE — only `Fuel` actually drives 1costingFE cost calculations ([cas22.py:128-152](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L128-L152)). Schema-side changes are therefore safe with respect to existing cost outputs but also low-leverage until paired with cost-model wiring (covered in the second half of this document).

---

## Summary of proposals

| # | Proposal | Rationale |
|---|---|---|
| P1 | Eliminate `Neutron Management` column | Information is already implied by `Fuel` |
| P2 | Eliminate `Plasma State` column | Derivable from `Confinement Concept` + `Operation Mode` |
| P3 | Rename `Tritium Breeding` → `Blanket Config`; reduce to 4 buckets | Current 10-value vocab is over-granular and conflates chemistry with architecture |
| P4 | Restructure `Magnet Type`: fold `Pulsed EM` into `Resistive`, fold `Self-confined` into `None` | Cleaner top-level categories; Pulsed EM is a duty-cycle distinction, not a magnet-type distinction |
| P5 | Correct Pacific Fusion: `Pulsed EM` → `None` | Their published design has no external confinement magnets |
| P6 | Correct Renaissance: `Liquid metal wall` → `other/hybrid` (under P3 vocabulary) | Current value loses the Li-LiH wall + Pb pebble multiplier architecture |
| P7 | Update Helion magnet notes; reclassify as `Resistive` (under P4 vocabulary) | Schema note hardcodes "aluminum"; reality is copper + aluminum + custom alloys |
| P8 | Rename `Primary Heating` → `Heating Type`; reduce to 4 MFE-relevant values (ICRH/ECRH/NBI/Ohmic) + combinations + 2 N/A flavors | Old vocab conflated physical heating with driver subsystems; non-MFE concepts had values that were really *drivers*, not heating |
| P9 | Add `Driver Type` column (8 values + TBD) | Separate the engineering driver subsystem from heating physics; enables structured cost-model wiring of CAS22 c220104 |
| P10 | Add `Laser Drive Architecture` column (Direct / Indirect / Hybrid / N/A) — laser/beam IFE only | Direct vs indirect vs hybrid drive is a primary cost differentiator within laser ICF; pulling it out of Confinement Concept makes comparison cleaner |

---

## P1 — Eliminate the `Neutron Management` column

### Current state

`Neutron Management` (Column 9) has 5 values: `Heavy shielding (14 MeV)`, `Heavy shielding (D-D)`, `Integrated blanket/shield`, `Reduced (D-He3)`, `Minimal (aneutronic)`. Definition at [schema.md:238-255](schema.md#L238).

### Why eliminate

Four of the five values restate `Fuel`:

| Neutron Management value | Fuel that implies it |
|---|---|
| Heavy shielding (14 MeV) | DT |
| Heavy shielding (D-D) | DD |
| Reduced (D-He3) | DHE3 |
| Minimal (aneutronic) | PB11 |

The only value carrying *new* information is `Integrated blanket/shield` — but that's an architectural integration choice that does not have its own clean axis. Concepts using FLiBe (CFS), liquid metal walls (Renaissance, General Fusion), or pulsed power inertial integration all get lumped into the same value despite very different engineering.

The column appears to give physics shielding info (already known from Fuel) plus an architecture flag (only one value, not a real distinction). Both better captured elsewhere.

### What replaces it

Nothing. Shielding requirements remain inferable from `Fuel`. The "integrated vs separate" architectural distinction, if needed for cost modeling, should be wired in differently — see Cost Model Wiring §W2 below.

### Affected files

- [schema.md](schema.md) — remove Column 9; update column count and summary
- [table.csv](table.csv) — remove `Neutron Management` column
- [citations.csv](citations.csv) — remove `Neutron Management` citation rows
- [taxonomy_models.py](../concept_explorer/taxonomy_models.py) — remove `NeutronManagement` enum and `neutron_management` field on `ConceptTaxonomy`
- [seed_registry.py](../concept_explorer/seed_registry.py#L127-L130) — remove `neutron_management` parsing
- [similarity.py:26](../concept_explorer/similarity.py#L26) — remove from `fuel_cycle` similarity group
- [view_categorical.js](../concept_explorer/static/js/view_categorical.js), [taxonomy_card.js](../concept_explorer/static/js/taxonomy_card.js) — remove the column/card row
- All per-concept dossiers in `knowledge/concept_research/*/dossier.md` — remove the `### Neutron Management` section (or leave as historical record)

### LCOE impact

**Zero.** 1costingFE's `c220102` shield cost is keyed off `Fuel` directly via `shield_scale[fuel]` ([cas22.py:144-152](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L144)) — DT=1.0, DD=0.7, DHE3=0.3, PB11=0.1. The `Neutron Management` taxonomy field is not consumed.

---

## P2 — Eliminate the `Plasma State` column

### Current state

`Plasma State` (Column 6) has 8 values: `Burning`, `Sustained`, `Transient`, `Compressed`, `Pinch`, `Confined`, `Non-burning`, `Solid-state`. Definition at [schema.md:167-184](schema.md#L167).

### Why eliminate

For the vast majority of concepts the value is determined by other columns:

- MFE Tokamak + Steady-state → `Burning` or `Sustained` (boundary fuzzy per schema:183)
- MFE Z-pinch → `Pinch`
- MFE Mirror + Steady-state → `Confined` or `Sustained`
- MIF + Pulsed → `Compressed` or `Transient`
- IFE + Pulsed → `Compressed`

The only places it disambiguates are:
- The fuzzy `Burning` vs `Sustained` boundary (already noted in schema as Q-target dependent)
- `Pinch` vs `Compressed` for self-confined plasmas (better captured under Confinement Concept: Z-pinch vs MagLIF)

The column adds noise without independent signal.

### What replaces it

Nothing. Where downstream consumers (similarity grouping, explorer cards) need a "what state is the plasma in" view, derive it from `Confinement Concept` + `Operation Mode`.

### Affected files

Same set as P1, plus:
- [similarity.py:24](../concept_explorer/similarity.py#L24) — `plasma_physics` group currently `[fuel, primary_heating, plasma_state]`. Decide whether to drop the field or replace with `confinement_concept` for similarity computation.
- 1costingFE has its own `plasma_state` object ([model.py:289](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/model.py#L289), [types.py:188](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/types.py#L188)) which is a numeric 0D plasma physics record (`n_e`, `T_e`, `V_plasma`). Unrelated to the taxonomy column. **Removing the taxonomy column does not touch 1costingFE.**

### LCOE impact

**Zero.** The taxonomy `Plasma State` is not read by 1costingFE.

### Side note: Zap classification

I noticed Zap appearing as "Cmp" in the explorer — this looks like a render or reading error. Verified:

- [table.csv:16](table.csv#L16): Zap Energy → Plasma State = `Pinch` (correct)
- [knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/dossier.md:44-48](../../knowledge/concept_research/15-sheared-flow-stabilized-z-pinch/dossier.md#L44) confirms `Pinch`
- The `Compressed` value (likely abbreviated "Cmp" in compact card UI) belongs to MagLIF/Pacific Fusion at [table.csv:19](table.csv#L19)

If "Cmp" is showing up next to Zap somewhere, that's a UI bug separate from this proposal — flag for review.

---

## P3 — Rename `Tritium Breeding` → `Blanket Config`; reduce to 4 buckets

### Current state

`Tritium Breeding` (Column 8) has 10 values: `FLiBe blanket`, `LiPb blanket`, `Liquid Li blanket`, `Li blanket (unspecified)`, `Solid ceramic breeder (HCPB)`, `Liquid metal wall`, `Self-bred (DD side)`, `N/A (no tritium in fuel cycle)`, `N/A (non-power)`, `TBD`. Definition at [schema.md:214-234](schema.md#L214).

### Proposed vocabulary (4 buckets)

| New value | Concrete examples |
|---|---|
| `Liquid metal` | LiPb eutectic, pure liquid Li, Li-LiH, flowing wall designs |
| `Molten salt` | FLiBe, FLiNaBe |
| `Solid breeder` | HCPB (Li₄SiO₄, Li₂TiO₃ pebbles + Be multiplier) |
| `Other/hybrid` | Architecturally hybrid blankets (e.g., Renaissance Li-LiH + Pb pebble), self-bred D-He3 (Helion), or any concept that does not fit the three primary buckets |

`N/A` (aneutronic, non-power) and `TBD` remain as separate values per existing convention.

### Why this mapping

- The current vocabulary mixes **chemistry** (FLiBe, LiPb, HCPB) with **architecture** (`Liquid metal wall` is geometry/integration, not a material). Consolidating to chemistry buckets makes the column orthogonal.
- 10-way granularity is more than the cost model uses (1costingFE doesn't read this field at all today; it uses Fuel and per-concept overrides).
- The `Other/hybrid` bucket is intentional. It captures concepts whose blanket cannot be costed by a default unit-cost lookup and **flags them for per-concept override**. See Cost Model Wiring §W4.

### Mapping table for migration

| Current value | Proposed value | Notes |
|---|---|---|
| FLiBe blanket | Molten salt | |
| LiPb blanket | Liquid metal | |
| Liquid Li blanket | Liquid metal | |
| Li blanket (unspecified) | Liquid metal | (with `subtype: TBD` in dossier note if unresolved) |
| Solid ceramic breeder (HCPB) | Solid breeder | |
| Liquid metal wall | depends — most cases `Liquid metal`; Renaissance-class (with multiplier integration) → `Other/hybrid` | |
| Self-bred (DD side) | Other/hybrid | Helion case — D-He3 with DD bootstrap |
| N/A (no tritium in fuel cycle) | unchanged | |
| N/A (non-power) | unchanged | |
| TBD | unchanged | |

### Architectural detail preservation

Renaming the column from `Tritium Breeding` to `Blanket Config` introduces a chemistry axis. Architecture detail (integrated wall vs contained, with/without multiplier, geometry) is NOT a top-level field — it lives in:
- The per-concept dossier `Notes` field (already the case for Renaissance: "liquid Li-LiH + Pb pebbles … 15 cm Pb + 18 cm Li-LiH; fm=1.24")
- Optional structured sub-fields if/when a future cost-model wiring requires them (see §W1)

### Affected files

- [schema.md](schema.md) — rewrite Column 8 vocabulary and notes
- [table.csv](table.csv) — rename column header; remap all 35+ concept values per migration table
- [taxonomy_models.py:136-145](../concept_explorer/taxonomy_models.py#L136) — replace `TritiumBreeding` enum with new 4-bucket enum (rename or new class)
- [seed_registry.py:127](../concept_explorer/seed_registry.py#L127) — update parsing to new column name + enum
- [similarity.py:26](../concept_explorer/similarity.py#L26) — update `fuel_cycle` group field name
- [view_categorical.js:66](../concept_explorer/static/js/view_categorical.js#L66), [taxonomy_card.js](../concept_explorer/static/js/taxonomy_card.js) — relabel
- All per-concept dossiers — section heading and values update; preserve dossier `Notes` text (it carries the architectural detail)

### LCOE impact

**Zero today.** 1costingFE's blanket cost (`c220101`) is `blanket_unit_cost[fuel] * volume * scaling`. The taxonomy field is not read.

**Future leverage**: a richer `Blanket Config` enum is a prerequisite for differentiating blanket unit costs by chemistry. See §W1.

---

## P4 — Restructure `Magnet Type`

### Current state

`Magnet Type` (Column 7) has 12 values: `HTS (wound)`, `HTS (3D stellarator)`, `HTS (planar array)`, `HTS (levitated dipole)`, `LTS`, `LTS+HTS`, `Resistive`, `Pulsed EM`, `Self-confined`, `None (IFE)`, `Electrostatic`, `N/A`. Definition at [schema.md:188-211](schema.md#L188).

### Proposed changes

1. **Fold `Pulsed EM` into `Resistive`**.
   `Pulsed EM` is defined as "pulsed resistive electromagnets driven by capacitor banks". The conductor is resistive; the duty cycle is the only difference. Duty cycle is captured by `Operation Mode` and (for capacitor bank capital) is better tracked under the driver/heating account.

2. **Fold `Self-confined` into `None`**.
   `Self-confined` currently covers Z-pinch (self-generated B-field), DPF (same), and MTF (mechanical compression — no magnetic confinement at all). The grouping is awkward: Z-pinch and DPF have plasma magnetic fields, MTF doesn't. The relevant engineering distinction (whether external confinement coils exist) is captured by `None`. The physics distinction (self-generated B-field vs purely mechanical) is preserved in `Confinement Concept` (Z-pinch / DPF / MTF).

3. **`None (IFE)` becomes `None`** — extend it to also cover MIF concepts that do not use external confinement magnets (Pacific Fusion's self-magnetized targets, MTF's mechanical compression). Drop the parenthetical scope qualifier.

4. **Other values unchanged** — HTS family, LTS, LTS+HTS, Electrostatic, N/A.

### Resulting vocabulary (10 values)

`HTS (wound)`, `HTS (3D stellarator)`, `HTS (planar array)`, `HTS (levitated dipole)`, `LTS`, `LTS+HTS`, `Resistive`, `None`, `Electrostatic`, `N/A`.

### Concept reclassifications under new vocabulary

| Concept | Current | New |
|---|---|---|
| Helion (08) | Pulsed EM | Resistive |
| Zap (15) | Self-confined | None |
| MagLIF / Pacific Fusion (19) | Pulsed EM | None — see P5 |
| General Fusion (14) | Self-confined | None |
| Dense Plasma Focus (24) | Self-confined | None |

### Affected files

- [schema.md:188-211](schema.md#L188) — rewrite Column 7 vocabulary and notes (especially the Helion/General Fusion/Zap parentheticals at L208-L210)
- [table.csv](table.csv) — remap affected rows
- [taxonomy_models.py:122-133](../concept_explorer/taxonomy_models.py#L122) — update `MagnetType` enum
- [seed_registry.py](../concept_explorer/seed_registry.py) — update parsing
- [similarity.py:25](../concept_explorer/similarity.py#L25) — `engineering` group field unchanged
- Affected dossiers: 08-frc-w-direct-conversion (Helion), 15-sheared-flow-stabilized-z-pinch (Zap), 07-maglif (MagLIF/Pacific Fusion), 14-magnetized-target-fusion-pneumatic-compression (GF), 24-dense-plasma-focus (DPF)

### LCOE impact

**Zero.** 1costingFE's coil cost (`c220103`) keys off `CoilMaterial` (4 values: REBCO_HTS / Nb3Sn / NbTi / Copper) and `_COIL_DEFAULTS`. If `_COIL_DEFAULTS.get(concept) is None`, `c220103 = 0`. The schema's Magnet Type taxonomy is not consumed directly. Concepts moving from `Pulsed EM` to `Resistive` map to `CoilMaterial.COPPER` (no change). Concepts moving from `Self-confined` to `None` map to "no entry in `_COIL_DEFAULTS`" → `c220103 = 0` (no change).

### Open question — capacitor bank capital cost

If we fold `Pulsed EM` into `Resistive`, the capacitor bank capital cost (a real and substantial item for Helion-class concepts: >50 MJ banks) loses its explicit signal in the taxonomy. 1costingFE today bundles this under `c220104` (Driver/Heating) for pulsed-family concepts via `_DRIVER_COST_PER_MW`, so it's not lost in costing. But if anyone is reading the taxonomy looking for a pulsed-driver flag, they'll now have to look at `Operation Mode` instead. Worth noting in the schema rewrite.

---

## P5 — Correct Pacific Fusion classification

### Current state

[table.csv:19](table.csv#L19): `MagLIF (D-T) | Pacific Fusion, Fuse Energy Technologies | … | Pulsed EM | …`

The single row lumps Pacific Fusion together with MagLIF heritage (Sandia Z-machine class) which uses a 10-30 T premagnetization coil.

### Proposed correction

Pacific Fusion's published design has **no external confinement magnets** — their self-magnetizing targets generate the axial seed field from the drive current itself. After P4 magnet vocabulary collapse: classify Pacific Fusion as `None`.

### Source

- Existing dossier already captures this: [knowledge/concept_research/07-maglif/dossier.md:57-58](../../knowledge/concept_research/07-maglif/dossier.md#L57): "Pacific Fusion's self-magnetizing targets generate the axial field from the drive current itself. No superconducting magnets involved."
- Confirming source not yet ingested into citations: <https://www.pacificfusion.com/updates/experimental-breakthrough-by-pacific-fusion-clears-major-obstacle-to-affordable-commercial-fusion> — explicitly states no external magnets needed.
- Add this URL to the iter-NN/sources directory and to citations.csv when implementing.

### Implementation choice

Two ways:
- **Row split**: keep MagLIF row for Sandia/Fuse Energy heritage, create new row for Pacific Fusion
- **Override existing row**: change row 19 magnet value to `None`, note Pacific Fusion's self-magnetization as the canonical case

Row split is cleaner if we expect more Pacific Fusion-specific values to diverge (driver tech is different too — they're building proprietary linear transformer driver hardware, not Z-machine). Decide at implementation time.

### LCOE impact

**Zero.** MagLIF concepts already get `c220103 = 0` via the `_COIL_DEFAULTS` lookup miss (their entry, if any, is excluded from the coil cost path). Reclassifying to `None` does not change the cost.

---

## P6 — Correct Renaissance Fusion classification

### Current state

[knowledge/concept_research/20b-renaissance-stellarator/dossier.md:56-60](../../knowledge/concept_research/20b-renaissance-stellarator/dossier.md#L56): blanket value = `Liquid metal wall`. This loses the architectural detail that the wall is **liquid Li-LiH with embedded Pb pebble neutron multiplier** (15 cm Pb + 18 cm Li-LiH; fm=1.24 from J. Nuclear Materials 599 (2024) 155239).

### Proposed correction

Under P3 vocabulary, Renaissance gets `Blanket Config = Other/hybrid`.
Dossier `Notes` field continues to carry the chemistry/architecture detail (already does).

### Why "Other/hybrid"

The Pb-pebble multiplier is not a small detail — it is a TBR-defining design choice. The architecture (flowing liquid wall + solid multiplier pebbles) does not match any of the three primary buckets:
- Not pure liquid metal (the multiplier is solid)
- Not molten salt (no salt)
- Not solid breeder (the breeder is liquid)

Forcing it into `Liquid metal` would erase the multiplier; forcing it into `Solid breeder` would erase the wall chemistry. `Other/hybrid` is the honest answer and signals "needs per-concept handling" downstream.

### LCOE impact

**Zero today.** 1costingFE's blanket cost is fuel-driven, with per-concept overrides. Renaissance's blanket cost would have to be set via override regardless of taxonomy value.

**Future leverage**: under §W4 below, `Other/hybrid` would carry the semantic of "default unit cost is invalid for this concept; explicit override required". This is more useful than the current `Liquid metal wall` value, which silently allows fallback to a default that doesn't represent the architecture.

---

## P7 — Update Helion magnet documentation

### Current state

[schema.md:209](schema.md#L209) (in the Magnet Type column notes):
> Helion uses `Pulsed EM` — their aluminum coils are pulsed with capacitor banks, not steady-state superconducting.

This hardcodes "aluminum" as the coil material.

### Reality (per Helion's own statements)

Helion uses a multi-material approach: copper, aluminum, and custom alloys. From [knowledge/concept_research/08-frc-w-direct-conversion/dossier.md:54](../../knowledge/concept_research/08-frc-w-direct-conversion/dossier.md#L54):
> Aluminum coils pulsed with capacitor banks (>50 MJ, tens of kV). Not superconducting, no cryogenics. … Cables use copper, aluminum, and custom alloys.

CEO Kirtley quote (Contrary Research): "regular aluminum magnets" — but the dossier itself acknowledges the broader material set.

### Proposed change

After P4 (fold Pulsed EM into Resistive):
- Helion's Magnet Type value: `Resistive`
- Schema notes section for Magnet Type: remove the "aluminum coils" hardcode; replace with a more general note acknowledging multi-material conductor stack
- Helion dossier `### Magnet Type` Notes: keep multi-material description; update parenthetical citation if a more current Helion source is available

### LCOE impact

**Zero.** Helion's coil cost in 1costingFE keys off `CoilMaterial.COPPER` (cheapest of the four conductor classes). Material distinction within "Resistive" is not a cost lever in the current model.

---

## P8 — Rename `Primary Heating` → `Heating Type`; reduce vocabulary

### Current state

`Primary Heating` (Column 4) has 19 controlled values mixing physical heating mechanisms with driver subsystems (laser variants, projectile impact, electromagnetic pinch, muon catalysis, acoustic implosion, etc.). The conflation makes it hard to reason about heating physics separately from the engineering driver.

### Proposed vocabulary (Heating Type — 4 MFE-relevant values + 2 N/A flavors + combinations + TBD)

| Value | Description |
|---|---|
| `ICRH` | Ion cyclotron resonance heating — RF at ~40-55 MHz. Tokamak heritage. |
| `ECRH` | Electron cyclotron resonance heating — gyrotrons at ~100-170 GHz. Stellarator default. |
| `NBI` | Neutral beam injection — primary or co-heating with RF. |
| `Ohmic` | Resistive dissipation of plasma current — primary in Z-pinch, present at startup in tokamaks. |
| `<combination>` | Combinations of the above, alphabetical with `+` separator: `ECRH + NBI`, `ICRH + NBI`, `ICRH + ECRH + NBI`, etc. |
| `N/A (compression-driven)` | Concept heats via driver compression (magnetic, mechanical, pulsed power, laser, projectile). The "heating" is the driver subsystem; see Driver Type. |
| `N/A (non-thermal)` | Concept does not reach thermal-equilibrium plasma temperatures (muon catalysis, sonoluminescence, electrostatic IEC). |
| `TBD` | Heating method not disclosed. |

### Why

The 4 controlled values (ICRH/ECRH/NBI/Ohmic) cover all MFE auxiliary heating in the concept list. Other "heating" entries in the old vocabulary (`Laser (variants)`, `Magnetic compression`, `Mechanical compression`, `Pulsed power implosion`, `Projectile impact`, `Heavy ion beam`, `Electrostatic acceleration`, `Electromagnetic pinch (DPF)`, `Muon catalysis`, `Acoustic implosion`) are really *drivers*, not heating mechanisms — they move to a new `Driver Type` column (P9). The two N/A flavors preserve the distinction between "compression-driven" and "non-thermal" concepts that would otherwise collapse to a single ambiguous N/A.

### Concept mapping under new vocab

| Concept | Old `Primary Heating` | New `Heating Type` |
|---|---|---|
| CFS (HTS Compact Tokamak) | RF (ICRH) | `ICRH` |
| Tokamak Energy | RF (ECRH) | `ECRH` |
| Energy Singularity | RF (ICRH) | `ICRH` |
| Firefly (Negative Triangularity) | RF (ECRH) | `ECRH` |
| Neo Fusion (BEST) | RF + NBI | `ICRH + ECRH + NBI` (per published heating plan) |
| Thea Energy | RF (ECRH) | `ECRH` |
| Proxima | RF (ECRH) | `ECRH` |
| Gauss | RF (ECRH) | `ECRH` |
| Type One Energy | RF (ECRH) | `ECRH` |
| Renaissance | NBI | `NBI` |
| Helical Fusion | RF (ECRH) | `ECRH` |
| OpenStar (Levitated Dipole) | RF (ICRH) | `ICRH` |
| Zephyr (Orbital Dipole) | RF (ECRH) | `ECRH` |
| Pale Blue (Mirror p-B11) | RF (ICRH) | `ICRH` |
| Realta (Mirror D-T) | RF + NBI | `ICRH + NBI` (verify against dossier — may also include ECRH) |
| TAE | NBI | `NBI` |
| ENN | RF (ECRH) | `ECRH` |
| Zap Energy | Ohmic (self-pinch) | `Ohmic` |
| Helion | Magnetic compression | `N/A (compression-driven)` |
| GF | Mechanical compression | `N/A (compression-driven)` |
| Pacific Fusion (MagLIF) | Pulsed power implosion | `N/A (compression-driven)` |
| All laser ICF (Focused Energy, Xcimer, Inertia, Blue Laser, GenF, HB11, Marvel, Cortex) | Laser (variants) | `N/A (compression-driven)` |
| FLF (Projectile ICF) | Projectile impact | `N/A (compression-driven)` |
| NearStar (MTIF) | Mechanical/magnetized impact | `N/A (compression-driven)` |
| Intensity (Heavy Ion Beam) | Heavy ion beam | `N/A (compression-driven)` |
| Avalanche, EMC2 (Polywell) | Electrostatic acceleration | `N/A (non-thermal)` |
| SHINE | Electrostatic acceleration (beam-target) | `N/A (non-thermal)` |
| LPPFusion (DPF) | Electromagnetic pinch (DPF) | `N/A (compression-driven)` (or `Ohmic` — DPF pinch self-heats ohmically; depends on interpretation) |
| Acceleron (Muon) | Muon catalysis | `N/A (non-thermal)` |
| Sonofusion | Acoustic implosion | `N/A (non-thermal)` |
| Deutelio (PoloMac) | Unknown | `TBD` |

### Affected files

- [schema.md](schema.md) Column 4: rewrite vocabulary
- [table.csv](table.csv): remap all 39 rows' Primary Heating values to new vocabulary
- [taxonomy_models.py:78-98](../concept_explorer/taxonomy_models.py#L78-L98): rename `PrimaryHeating` → `HeatingType`; reduce to 4 base values + N/A flavors + combinations + TBD
- [seed_registry.py](../concept_explorer/seed_registry.py): column name change
- [similarity.py:24](../concept_explorer/similarity.py#L24): `plasma_physics` group keeps `heating_type` (renamed)
- [view_categorical.js:62](../concept_explorer/static/js/view_categorical.js#L62), [taxonomy_card.js:24](../concept_explorer/static/js/taxonomy_card.js#L24): rename `primary_heating` → `heating_type`, update label

### LCOE impact

1costingFE's `c220104` for steady-state concepts already sums per-modality heating contributions (`p_nbi`, `p_icrf`, `p_ecrh`, `p_lhcd`) from concept YAML defaults. The schema renaming doesn't change this. The combination-encoding (e.g., `ECRH + NBI`) makes it cleaner to validate that YAML heating splits match the taxonomy. Zero direct LCOE impact; small validation/clarity gain.

---

## P9 — Add `Driver Type` category

### Motivation

`Primary Heating` (now `Heating Type` per P8) used to conflate heating physics with driver engineering. Splitting out `Driver Type` gives each concept a clean high-level engineering category for cross-concept comparison.

### Proposed vocabulary (8 values + TBD)

| Value | Description | Concept examples |
|---|---|---|
| `Magnetic` | External or self-generated magnetic system is the dominant driver subsystem. Covers both steady-state confinement (tokamaks, stellarators, mirrors) and pulsed magnetic compression (Helion FRC). Specific magnet technology captured in `Magnet Type`. | CFS, Tokamak Energy, Helion, all stellarators, all mirrors, TAE (NBI is heating, magnets are driver subsystem), ENN |
| `Magnetic pinch` | Pulsed current generates magnetic field that pinches or implodes the plasma. Covers Z-pinch, MagLIF (pulsed-power liner implosion), and DPF. | Zap Energy, Pacific Fusion, LPPFusion |
| `DPSSL Laser` | Diode-pumped solid-state laser. Includes Nd:glass and Yb:YAG architectures, femtosecond-to-nanosecond pulses. | Focused Energy, Inertia, Blue Laser, GenF, Marvel, HB11, Cortex |
| `Gas Laser` | Gas-lasing-medium laser. Includes excimer (KrF, ArF) and CO₂ lasers. | Xcimer |
| `Ion/particle beam` | Accelerator-driven ion or particle beams used as the primary driver. | Intensity Energy (heavy ion beam ICF), SHINE (beam-target accelerator) |
| `Mechanical/kinetic` | Driver delivers kinetic energy via mechanical or electromagnetic acceleration of a physical projectile or piston. | GF (pneumatic pistons), FLF (EM gun), NearStar (railgun) |
| `Electrostatic` | High-voltage electric fields accelerate ions toward convergence. | Polywell (EMC2), Avalanche |
| `Other` | Driver mechanism doesn't fit the above (sonic, muonic, etc.). | Sonofusion, Acceleron |
| `TBD` | Driver subsystem not disclosed. | Deutelio (PoloMac) |

### Why "Magnetic" is inclusive

The unifying physics is: a magnetic system is the work-doing element. This covers both steady-state magnetic confinement (tokamaks/stellarators) and pulsed magnetic compression (Helion FRC). The specific technology (HTS / Resistive / etc.) is captured in `Magnet Type`. The temporal profile (continuous / pulsed) is captured in `Operation Mode`.

### Why "Magnetic pinch" is separate

Z-pinch, MagLIF, and DPF share a distinctive physics: a pulsed high-current discharge generates a magnetic field that pinches or implodes the plasma (in Z-pinch the plasma current self-pinches; in MagLIF the current implodes a liner around pre-magnetized fuel; in DPF the current creates a dense plasma focus). The engineering subsystem is fundamentally pulsed power (Marx generators or simpler capacitor banks); the work-doing mechanism is current-driven pinch. Combining these three under one value reflects the shared engineering and cost-modeling concerns (capacitor bank capital, fast switches, high-current transmission lines).

### Concept mapping

(See P8 mapping table above for the inverse view: each concept's old `Primary Heating` value plus its new `Driver Type`.) Compact summary:

| Driver Type | Concepts |
|---|---|
| `Magnetic` | All MFE concepts (CFS, Tokamak Energy, Energy Singularity, Firefly, Neo Fusion, Thea, Proxima, Gauss, Type One, Renaissance, Helical, OpenStar, Zephyr, Pale Blue, Realta, TAE, ENN) + Helion |
| `Magnetic pinch` | Zap Energy, Pacific Fusion, LPPFusion |
| `DPSSL Laser` | Focused Energy, Inertia, Blue Laser, GenF, Marvel, HB11, Cortex |
| `Gas Laser` | Xcimer |
| `Ion/particle beam` | Intensity Energy, SHINE |
| `Mechanical/kinetic` | GF, FLF, NearStar |
| `Electrostatic` | Avalanche, EMC2 (Polywell) |
| `Other` | Sonofusion, Acceleron |
| `TBD` | Deutelio |

### Affected files

- [schema.md](schema.md): add Column for Driver Type
- [table.csv](table.csv): add `Driver Type` column; populate all 39 rows
- [taxonomy_models.py](../concept_explorer/taxonomy_models.py): add `DriverType` enum
- [seed_registry.py](../concept_explorer/seed_registry.py): parse new column
- [similarity.py](../concept_explorer/similarity.py): add `driver_type` to `engineering` group (currently `magnet_type`, `energy_capture`)
- [view_categorical.js](../concept_explorer/static/js/view_categorical.js), [taxonomy_card.js](../concept_explorer/static/js/taxonomy_card.js): add Driver Type column/row

### LCOE impact

This is the **biggest cost-model wiring opportunity** of the schema revisions. 1costingFE's `c220104` (CAS22 Driver/Heating) currently keys off `ConfinementFamily` (steady-state vs pulsed) and a per-concept `_DRIVER_COST_PER_MW` map. A direct mapping from `Driver Type` to driver-cost-per-MW lookup tables would replace the ad-hoc per-concept dictionary with a structured, taxonomy-driven cost model. See §W5 below.

---

## P10 — Add `Laser Drive Architecture` (laser/beam-IFE only)

### Motivation

Within laser/beam IFE, the distinction between direct drive, indirect drive (hohlraum), and hybrid architectures is a primary differentiator in cost and physics. The current schema captures this in `Confinement Concept` (`Laser ICF (indirect drive)`, `Laser ICF (direct drive)`, `Laser ICF (hybrid drive)`, etc.) — but conflating it with the confinement concept makes it harder to reason about. A dedicated column makes the architecture explicit.

### Proposed vocabulary

| Value | Description |
|---|---|
| `Direct drive` | Laser/beam directly ablates capsule surface (no hohlraum). |
| `Indirect drive` | Laser/beam → hohlraum → X-rays → capsule ablation. Canonical NIF approach. |
| `Hybrid drive` | First pulse heats a hohlraum to form a thick plasma atmosphere; subsequent pulses drive the capsule directly through it. Xcimer HDD approach. |
| `N/A` | Concept is not laser/beam IFE. Applies to all MFE, MIF, projectile ICF, acoustic ICF, DPF, electrostatic, muon — i.e., any concept whose driver isn't a laser or particle beam aimed at a compressible target. |

### Concept mapping

| Concept | Laser Drive Architecture |
|---|---|
| Inertia Enterprises | `Indirect drive` |
| Xcimer Energy | `Hybrid drive` |
| Focused Energy (Fast Ignition) | `Direct drive` (fast ignition is a direct-drive variant) |
| Blue Laser Fusion (OEC) | `Direct drive` |
| GenF Systems (French National) | `Direct drive` |
| HB11 Energy | `Direct drive` (ultrashort pulse on solid targets — no hohlraum) |
| Marvel Fusion | `Direct drive` (nanostructured targets, ultrashort pulse) |
| Cortex Fusion (Liquid Jet) | `Direct drive` (femtosecond on liquid D2O jet) |
| Intensity Energy (Heavy Ion Beam) | `Direct drive` (canonical HIF approach) |
| All MFE concepts | `N/A` |
| All MIF concepts (Helion, GF, Pacific Fusion, Zap, NearStar) | `N/A` |
| FLF (Projectile ICF) | `N/A` (projectile is the driver, not a laser/beam at a target) |
| LPPFusion (DPF) | `N/A` |
| Sonofusion | `N/A` |
| Polywell, Avalanche, SHINE | `N/A` |
| Acceleron (Muon) | `N/A` |
| Deutelio (PoloMac) | `N/A` |

### Why scoped to laser/beam IFE

The direct/indirect/hybrid distinction is meaningful only when a laser or particle beam is aimed at a compressible target. For all other concepts, the question doesn't apply. Forcing every concept to have a non-N/A value would dilute the column's meaning.

### Affected files

Same files as P9 — add a column to schema.md and table.csv, add `DriveArchitecture` enum to taxonomy_models.py, etc.

### LCOE impact

Direct/indirect/hybrid have meaningfully different cost structures:
- **Indirect drive**: hohlraum target fabrication adds significant target-factory CAPEX/OPEX
- **Direct drive**: target is just a fuel capsule, simpler factory
- **Hybrid drive**: hohlraum + atmosphere physics complicate target design and laser pulse shaping; intermediate cost profile

Currently 1costingFE's target fabrication costs are concept-specific. A direct-drive vs indirect-drive multiplier on target factory cost would be a natural wiring point. See §W6 below.

---

# Cost Model Wiring (Follow-up Work)

This section is forward-looking: it captures the natural follow-ups to feed the (revised) taxonomy into 1costingFE so cost outputs reflect concept-specific architectural choices rather than relying solely on Fuel + per-concept YAML overrides.

These are NOT prerequisites for the schema revisions above. The schema revisions are safe with respect to current LCOE outputs (because the taxonomy is currently decorative for cost purposes). The wiring proposals below describe how the revised taxonomy could *become* cost-relevant in a follow-up effort.

## Today's cost model integration (baseline)

- **C220101 First Wall + Blanket** ([cas22.py:128-137](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L128)): `blanket_unit_cost[fuel] × blanket_vol × (p_th/P_TH_REF)^0.6`. Fuel-keyed only.
- **C220102 Shield** ([cas22.py:144-152](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L144)): `shield_unit_cost × shield_vol × shield_scale[fuel] × (p_th/P_TH_REF)^0.6`. Fuel-keyed only.
- **C220103 Coils** ([cas22.py:161-171](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L161)): `total_kAm × CoilMaterial.cost_per_kAm × markup`. `_COIL_DEFAULTS.get(concept) is None` → `c220103 = 0`. Concept-keyed.
- **C220104 Driver/Heating** ([cas22.py:180-196](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L180)): for steady-state, sums `heating_<modality>_per_mw × p_<modality>` (NBI, ICRF, ECRH, LHCD); for pulsed, `_DRIVER_COST_PER_MW[concept] × p_driver`. Heating modality is concept-keyed (each YAML default sets `p_nbi`, `p_icrf`, etc.) — not directly tied to schema's `Primary Heating` taxonomy.
- **Per-concept YAML defaults** in [`costingfe/data/defaults/`](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/data/defaults/): 16 archetype YAMLs (`steady_state_tokamak.yaml`, `pulsed_maglif.yaml`, etc.) supply numeric design parameters. There is no Renaissance-specific YAML — Renaissance presumably inherits from `steady_state_stellarator.yaml` plus dossier-driven overrides (`overridden: true` flags in [exploration/concept_explorer/data/20b.json](../concept_explorer/data/20b.json)).

## W1 — `Blanket Config` → C220101 unit cost differentiation

**Goal**: blanket capital cost should distinguish FLiBe vs LiPb vs HCPB vs hybrid, not just by Fuel.

**Mechanism**:
- Replace `blanket_unit_cost[fuel]` with `blanket_unit_cost[fuel, blanket_config]` — a 2D table.
- Default values per (Fuel × Blanket Config) cell, calibrated against literature (CFS FLiBe ARC studies, EU-DEMO HCPB cost studies, Renaissance liquid-Li wall paper, etc.)
- For `blanket_config == Other/hybrid`, raise an error or warning if no per-concept override is supplied (see §W4).

**Affected files**:
- [costingfe/data/defaults/costing_constants.yaml](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml) — extend the `blanket_unit_cost_<fuel>` constants to a (fuel, config) lookup
- [costingfe/layers/cas22.py:128-137](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L128) — update lookup
- 1costingFE adapter — read `Blanket Config` from concept taxonomy
- Per-concept overrides for hybrid blankets (Renaissance, Helion DD-side bootstrap)

**Expected LCOE movement**: meaningful for concepts where the blanket dominates CAS22. Liquid metal walls (Renaissance, GF) and HCPB (Type One, Pranos, etc.) currently use the same DT unit cost — wiring this would create real differentiation.

## W2 — Integrated vs separate shielding (P1 follow-up)

**Goal**: capture the integration architecture that motivated the original `Integrated blanket/shield` value, even though we've eliminated the column.

**Mechanism options**:
- Add a boolean field `blanket_integrated_shield` to the concept-specific YAML / taxonomy
- When `True`, apply a multiplier (>1 to blanket account, <1 to shield account) reflecting the consolidated structural cost
- When `False`, keep current Fuel-only shield scaling

**Affected files**:
- [costingfe/data/defaults/*.yaml](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/data/defaults/) — add the field per archetype
- [costingfe/layers/cas22.py:140-152](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L140) — apply multiplier
- 1costingFE adapter — read flag

**Expected LCOE movement**: small but architecturally meaningful. Consolidates the C220101+C220102 structural redundancy that integrated designs avoid.

**Decide first**: is this distinction actually material enough to warrant a wiring effort? If not, leave shield cost fuel-driven and accept the small inaccuracy.

## W3 — `Magnet Type` → `CoilMaterial` mapping

**Goal**: stop hand-maintaining a separate `_COIL_DEFAULTS` map keyed off concept-specific shorthands. Derive `CoilMaterial` from the schema's revised Magnet Type vocabulary.

**Mechanism**:
- Mapping function: `magnet_type → CoilMaterial`:
  - HTS family → `REBCO_HTS`
  - LTS / LTS+HTS → `NB3SN` (or `NBTI` for older designs — needs concept-by-concept review)
  - Resistive → `COPPER`
  - None / Electrostatic / N/A → no entry → `c220103 = 0`
- Per-concept `_COIL_DEFAULTS` continues to supply geometry parameters (path_factor, markup) but conductor cost is taxonomy-driven.

**Affected files**:
- [costingfe/layers/cas22.py:161-171](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L161)
- 1costingFE adapter — read Magnet Type
- [costingfe/types.py:82-99](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/types.py#L82) — keep `CoilMaterial` enum; potentially expand if HTS/LTS subdistinctions matter

**Expected LCOE movement**: zero if mapping is faithful to current `_COIL_DEFAULTS`. Benefit is reduced surface area for hand-maintenance.

## W4 — `Other/hybrid` blanket → required per-concept override

**Goal**: make the `Other/hybrid` Blanket Config bucket carry semantic weight: "default unit cost is invalid; explicit override required."

**Mechanism**:
- 1costingFE blanket cost lookup raises if `blanket_config == Other/hybrid` and no per-concept `c220101_override` is supplied.
- Per-concept YAML / explorer JSON `overridden: true` flag at C220101 level becomes the override path.
- Renaissance gets an override based on the J. Nuclear Materials 599 (2024) 155239 cost decomposition; Helion gets an override reflecting their integrated FRC chamber + DEC architecture.

**Affected files**:
- [costingfe/layers/cas22.py:128-137](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L128)
- [exploration/concept_explorer/data/20b.json](../concept_explorer/data/20b.json) — set Renaissance C220101 override
- [exploration/concept_explorer/data/08.json](../concept_explorer/data/08.json) — set Helion C220101 override (already partially overridden)

**Expected LCOE movement**: corrects the silent fallback to a default that doesn't apply.

## W5 — `Primary Heating` taxonomy → C220104 modality split

**Goal**: align the steady-state heating cost calculation with the schema's `Primary Heating` vocabulary.

**Current state**: 1costingFE's `c220104` for steady-state sums per-modality contributions (`p_nbi`, `p_icrf`, `p_ecrh`, `p_lhcd`), but the modality power split comes from per-concept YAML defaults, not from the dossier's `Primary Heating` value. There's no enforced consistency.

**Mechanism**:
- For steady-state concepts, validate that the YAML's heating power split matches the schema's `Primary Heating` value. If `Primary Heating == RF (ECRH)`, expect `p_ecrh > p_nbi` etc.
- Optionally, derive a default power split from `Primary Heating` if YAML is silent.

**Affected files**:
- 1costingFE adapter — validation step
- Possibly [costingfe/layers/cas22.py:180-196](file:///c:/Users/mallo/1cfe/1costingfe/src/costingfe/layers/cas22.py#L180) — derive default split if YAML missing

**Expected LCOE movement**: small, mostly catches inconsistencies between the dossier and the cost-model defaults.

---

## Open questions

1. **Similarity grouping**: dropping `Plasma State` and `Neutron Management` removes fields from `similarity.py`'s `plasma_physics` and `fuel_cycle` groups. What replaces them? Options: (a) drop those groups, (b) substitute `Confinement Concept` and Fuel respectively, (c) augment with new derived fields. Decide before the schema change ships.

2. **Pulsed EM → Resistive consequences for capacitor bank visibility**: after the fold, is there sufficient downstream signal to identify "pulsed copper coils with capacitor bank" concepts? Options: (a) accept that it's now derivable from `Resistive` + `Operation Mode == Pulsed`, (b) add an explicit `driver_includes_capacitor_bank` flag at the concept level.

3. **Schema versioning**: this revision should bump schema to v0.3 and add a changelog entry at the bottom of [schema.md](schema.md#L334). Decide whether to back-fill existing dossiers' schema-version metadata or only enforce going forward.

4. **Re-running concept analyses**: dossiers that change classification under P4/P5/P6 (Helion, Pacific Fusion, Renaissance, Zap, GF, DPF) should be re-validated after the change. The Stage 2 cost analyses for the corresponding concepts may need regeneration if any wiring (W1-W5) is implemented at the same time.

5. **Pacific Fusion row split vs override**: see P5 — decide at implementation time.

6. **Renaissance multiplier preservation**: `Other/hybrid` is the right bucket for Renaissance, but how do we preserve the `15 cm Pb + 18 cm Li-LiH` numbers in a structured way that 1costingFE could read for §W4? Free-text in dossier Notes is the lowest-effort answer; structured sub-fields are the better-quality answer. Decide based on whether other `Other/hybrid` concepts will need similar structured detail.
