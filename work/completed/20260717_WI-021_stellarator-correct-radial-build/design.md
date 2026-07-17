---
Status: complete
Created: 2026-07-17
Updated: '2026-07-17'
Related Artifacts:
  Spec: ./spec.md
---

> Process note: per the owner-ratified item process, the single owner checkpoint sits after
> `/spec-model`; design → plan → implement → validate → handshake → close proceed without a
> further stop. Spec approved at checkpoint 2026-07-17: **Option 1** (torus shells, no material
> shape factor); yes to all three sub-decisions (wall_area, r_coil, special_materials rebind);
> Option 2 deferred to the epic; proceed on top of the uncommitted WI-020 state.

# WI-021 Design: Stellarator-Correct Radial-Build Volumes

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. Radial-build formulas are 1costingFE @ `0254385` (ARIES/Starfire-lineage exception, admissible per §3); R/a/kappa are the admissible Stellaris sources.

## Overview

Add one calc def — `'MFE Radial Build'` — to the library, thread it through the generic plant, and wire its outputs into the six consumers that today carry injected constants. The calc computes cumulative radii (flat sums of thicknesses), per-layer torus-shell volumes, the four CAS22 aggregate volumes, the first-wall area, and the coil-bore radius, reproducing `costingfe.layers.geometry.compute_geometry`'s torus branch and the `model.py:1205-1208` aggregation. Under the owner's Option 1 (torus shells, no material shape factor) the six computed values equal the current constants, so **cost and LCOE are unchanged** — this is a fidelity/traceability win, not a re-baseline. No new SysML constructs: the multi-output, intermediate-attribute calc pattern is already codegen-proven by the WI-019 `'MFE Power Balance Calc'`.

## Research Findings

### The multi-output / intermediate-attribute pattern is codegen-proven

`'MFE Power Balance Calc'` (`models/library/analyses/mfe_power_balance.sysml`, WI-019 — flows through the pipeline and passes SV-025/026) uses exactly the constructs the radial build needs:
- intermediate `attribute p_alpha : Real = (3.52/17.58) * p_nrl;` locals (7 of them), some referencing earlier intermediates (`p_neutron = p_nrl - p_alpha`);
- multiple `out attribute`s (p_th, p_the, p_et, q_eng, rec_frac, p_net), some referencing intermediates.

So the radial build's cumulative radii (flat `+` sums), torus coefficient, per-layer volumes (`C * (r_out**2 - r_in**2)`), and six outputs are all inside the proven envelope. This retires the epic's codegen-envelope risk for this item.

### The formulas (1costingFE, admissible)

`src/costingfe/layers/geometry.py`, torus branch. Cumulative radii from the minor radius `a` (= `plasma_t`) outward:
```
vacuum_or   = a + vacuum_t          ht_shield_or = reflector_or + ht_shield_t
firstwall_or= vacuum_or + firstwall_t  structure_or = ht_shield_or + structure_t
blanket_or  = firstwall_or + blanket_t gap1_or      = structure_or + gap1_t
reflector_or= blanket_or + reflector_t vessel_or    = gap1_or + vessel_t
                                       coil_or      = vessel_or + coil_t
                                       gap2_or      = coil_or + gap2_t
                                       lt_shield_or = gap2_or + lt_shield_t
```
Torus-shell volume `V = kappa · 2π²·R · (r_out² − r_in²)` (geometry.py:67-73); surface area `SA = kappa · 4π²·R·a_ref` (geometry.py:76-81). CAS22 aggregates (model.py:1205-1208):
```
blanket_vol   = firstwall_vol + blanket_layer_vol + reflector_vol
shield_vol    = ht_shield_vol + lt_shield_vol
structure_vol = vol(ht_shield_or, structure_or)
vessel_vol    = vol(gap1_or, vessel_or)
wall_area     = SA(R, vacuum_or, kappa)        # first-wall standoff radius, NOT a
r_coil        = vessel_or
```
Verified at the Stellaris build (R=12.7, a=1.5, κ=1.0; blanket_t=0.80 from `steady_state_stellarator.yaml:39`, the rest `RadialBuild` defaults): reproduces 1118.695 / 552.140 / 219.979 / 157.933 / 802.201 / 3.20 exactly. Note `wall_area` uses `vacuum_or = a + vacuum_t = 1.60` (the first-wall standoff), not the plasma minor radius `a` — getting this wrong mismatches 802.201 (spec Risk 5).

### The handshake bypasses SysML geometry — surfaced (capture-fidelity §4)

Non-obvious and load-bearing: `handshake_1costingfe.py` does **not** use the SysML geometry. It injects 1costingFE's own pre-computed material volumes directly as leaf params (lines 232/238/242/248/261: `blanket__blanket_vol = geo["blanket_vol"]`, etc.), and its plasma-volume path (line 174, `a=1.8, kappa=1.6`) is an arbitrary self-consistent `(V, sigma_v)` pair chosen only to inject 1cfe's *given* p_fus — unrelated to the real geometry. This isolates the cost formulas from geometry.

Consequence for item 1: once the six volumes become computed outputs of `rb`, they stop being settable leaf params (confirmed: they are leaf params in `mfe_plant_params.json` today *because* they are injected redefinitions; binding them to `rb.*` makes them derived, exactly like `wall_area = 802.201` today is already a non-param computed attribute). So the handshake's 5 direct injections must be removed, and closure must come from `rb` computing 1cfe's values. That closure holds under Option 1 because the baked-in instance radial-build inputs equal 1cfe's — see D5. This is a genuine tightening of the handshake (it now exercises `rb`), with numbers unchanged; recorded, not resolved silently.

### Codegen emits per-calc-input params (closure-critical)

Confirmed from `system_design.json`: params are per-calc-input (`geom__a`, `geom__kappa`, `geom__R` are distinct keys). So `rb__a`, `rb__kappa`, `rb__R` and the 11 `rb__*_t` will be their own params, each baked from the plant/instance bindings. The handshake overrides `geom__a=1.8`/`geom__kappa=1.6`/`geom__R` for the plasma path; it does **not** touch `rb__*`, so `rb` keeps the instance's real geometry (a=1.5, κ=1.0, R=12.7) and reproduces 1cfe's material volumes. This is the mechanism that keeps SV-025/026 byte-identical.

### Consumer map (grep over `models/` + `exploration/`)

| consumer | file | change |
|---|---|---|
| `'MFE Radial Build'` calc def (new) | `models/library/analyses/mfe_plasma_scaling.sysml` | add the calc def (D1) |
| `rb` calc block + 11 thickness attrs (new) | `models/designs/generic_mfe/mfe_plant.sysml` | add block + thickness attributes (D2) |
| `part blanket/shield/structure/vessel` | `mfe_plant.sysml:59-69` | add `:>> <vol> = rb.<vol>;` (D3, sibling-calc pattern) |
| `part magnet` r_coil | `mfe_plant.sysml:48` + instance | bind `r_coil = rb.r_coil` (D3) |
| instance thickness bindings (new) | `stellarator_09/stellarator_plant.sysml` (~277) | bind 11 thicknesses, cited (D4) |
| instance injected constants (remove) | `stellarator_plant.sysml:145,158,169,180,117,507` | drop the six constants; docs → forward-computation (D4) |
| `special_materials_capital` | `stellarator_plant.sysml:445` | rebind to `blanket.blanket_vol × 0.50 × 9400 × 5.0` (D6) |
| staged copies | `exploration/stellarator_e2e/models/**` | mirror canonical edits (check byte-identity of the analyses file first) |
| oracle | `exploration/stellarator_e2e/verify_stellaris.py` | mirror the rb formulas (D7) |
| handshake | `exploration/stellarator_e2e/handshake_1costingfe.py` | remove 5 direct volume/r_coil injections; verify rb reproduces geo (D5) |
| runner | `exploration/stellarator_e2e/run_stellaris.py` | headline unchanged under Option 1; re-confirm asserts pass |

## Design Decisions

**D1 — `'MFE Radial Build'` calc def, multi-output with intermediate radii.** In `mfe_plasma_scaling.sysml` (alongside `'Plasma Geometry'`). Inputs: `R, a, kappa`, `pi` (default 3.14159265358979, existing pattern), and 11 thicknesses (`vacuum_t, firstwall_t, blanket_t, reflector_t, ht_shield_t, structure_t, gap1_t, vessel_t, coil_t, gap2_t, lt_shield_t`). Intermediate `attribute`s: the cumulative radii, the torus coefficient `C = kappa*2*(pi**2)*R`, and the per-layer volumes. Outputs: `blanket_vol, shield_vol, structure_vol, vessel_vol, wall_area, r_coil`. `bioshield_t` is omitted (bioshield_vol is unconsumed); the coil has no shell volume (magnet cost is separate). All flat arithmetic (D1 envelope, proven by WI-019).

**D2 — `rb` calc block + thickness attributes in the generic plant (MR-3).** `'MFE Power Plant'` gets 11 `attribute <layer>_t : Real default <RadialBuild default>;` (generic machinery, concept-agnostic — the radial-build *pattern* is shared; the *values* are concept-specific) and a `calc rb : 'MFE Radial Build' { in R = R; in a = a; in kappa = kappa; in <each>_t = <each>_t; }` block, mirroring the existing `geom` block. `rb` reuses the plant's existing `R`/`a`/`kappa` attributes (same real geometry as `geom`).

**D3 — outputs wired at each consumer's home, via the proven sibling-calc reference.** The subsystem parts already redefine `capital_cost` by referencing a sibling plant calc from inside the part body (`part magnet { :>> capital_cost = magnet_cost.capital_cost; }`). Same pattern for volumes: in the generic plant, `part blanket { :>> capital_cost = blanket_cost.cost; :>> blanket_vol = rb.blanket_vol; }` and likewise shield/structure/vessel; `part magnet { … :>> r_coil = rb.r_coil; }`. `wall_area` is instance-only (WI-018 viability), so it binds in the instance: `attribute wall_area : Real = rb.wall_area;`.

**D4 — instance binds all 11 thicknesses explicitly; the six constants are removed.** Rather than relying on generic-plant defaults for the 7 non-overridden layers, the Stellaris instance binds every thickness explicitly, each with an MR-4 citation (blanket_t/ht_shield_t/structure_t/vessel_t → `steady_state_stellarator.yaml:39-42`; vacuum_t/firstwall_t/reflector_t/gap1_t/coil_t/gap2_t/lt_shield_t → `RadialBuild` defaults `geometry.py:19-40`). Rationale: (a) robust against the WI-020 gotcha — an explicit instance binding guarantees the snapshot bakes the correct value into `rb__*_t`, no reliance on default propagation; (b) fully traceable — every thickness names its source. The six injected constants (`blanket_vol`, `shield_vol`, `structure_vol`, `vessel_vol`, `wall_area`, `r_coil`) are deleted; their doc comments are rewritten to describe the forward computation. Under Option 1 the computed values equal the deleted constants.

**D5 — handshake: remove the 5 direct volume/r_coil injections; closure comes from `rb`.** After D3/D4 the volumes are derived (non-param), so `blanket__blanket_vol` etc. leave `mfe_plant_params.json`. Delete the 5 `mp.update` lines (232/238/242/248/261). The generated `forward()` then computes the volumes via `rb` from the baked-in instance inputs. Closure holds because: (i) `rb__a/kappa/R/*_t` are per-calc params baked to the instance's real geometry (a=1.5, κ=1.0, R=12.7, yaml thicknesses); (ii) the handshake overrides only `geom__*`, never `rb__*`; (iii) the instance's radial-build inputs equal 1cfe's stellarator build, so `rb` reproduces `geo["blanket_vol"]` etc. **Implement MUST verify** `rb`'s six outputs equal the 1cfe `geo` values (and the pre-item-1 constants) before trusting closure; if any differs, that is a real geometry inconsistency to surface, not absorb. *Fallback if closure proves fragile* (e.g. `geo` was computed at an R ≠ 12.7): inject `rb__*` inputs in the handshake set to 1cfe's radial build so `rb` reproduces `geo` — a stronger test, numbers still identical.

**D6 — `special_materials_capital` rebound to the computed blanket volume.** Instance: `:>> special_materials_capital = blanket.blanket_vol * 0.50 * 9400.0 * 5.0;` (the CAS27 PbLi inventory, keyed to the aggregate blanket_vol per its current basis). This slightly refines the value — the exact computed blanket_vol gives ≈ 26,289,332 vs the rounded constant 26,289,000, a ~$332 shift, ~3e-6 of total capital, invisible at headline precision. CAS27 is a pass-through, not in the handshake's per-account comparison (ACCOUNTS = POWERCORE + BOP), so it does not perturb SV-025/026. *Codegen check at implement:* this makes `special_materials_capital` an attribute bound to an expression referencing a part attribute; if that proves outside the envelope, fall back to the instance literal with the derivation kept in the doc (the number is unchanged either way).

**D7 — oracle mirrors the rb formulas.** `verify_stellaris.py` gains the cumulative-radii + torus-shell computation (replacing the six constants in `IN`), so `run_stellaris.py` stays bit-exact against the generated pipeline. The oracle is the independent check that the SysML rb arithmetic is transcribed correctly.

**D8 — output contract otherwise unchanged.** The cost calcs still read `blanket.blanket_vol` etc.; only the *source* of those values changes (constant → `rb` output). The magnet cost still reads `magnet.r_coil`; `wall_load_calc` still reads `wall_area`. Dataflow stays unidirectional: radial build → volumes → costs; radial build → wall_area → wall_load. Under Option 1 every downstream number is unchanged.

## Proposed Design — `'MFE Radial Build'` calc def

```sysml
calc def 'MFE Radial Build' {
    doc /*
    Forward radial build [m, m^2, m^3] for an MFE torus: cumulative layer radii
    from the plasma minor radius outward, then torus-shell volumes and the
    first-wall surface area.

      or_i        = or_{i-1} + t_i            (cumulative radii)
      layer_vol   = kappa * 2*pi^2 * R * (or_out^2 - or_in^2)   (torus shell)
      wall_area   = kappa * 4*pi^2 * R * vacuum_or              (first-wall SA)

    Aggregates match 1costingFE's CAS22 grouping (model.py:1205-1208):
    blanket = firstwall+blanket+reflector; shield = ht+lt; structure; vessel.
    Concept-agnostic: R major radius, a minor radius (= plasma_t), kappa
    elongation, and per-layer thicknesses. Pure torus shells, no shape factor
    (owner Option 1, WI-021) — engineered annuli are sized by the radial build,
    not the plasma cross-section. ARIES/Starfire-lineage geometry, admissible
    per PROTOCOL.md §3.

    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py
    **Ref**: geometry.py:67-81 (torus shell + surface area), 106-118 (cumulative
        radii), 156-170 (per-layer volumes); model.py:1205-1208 (CAS22 aggregation)
    **Basis**: forward radial build; torus branch; MFE-generic
    */

    in attribute R : Real;
    in attribute a : Real;           // minor radius = plasma_t
    in attribute kappa : Real;
    in attribute pi : Real default 3.14159265358979;

    in attribute vacuum_t : Real;
    in attribute firstwall_t : Real;
    in attribute blanket_t : Real;
    in attribute reflector_t : Real;
    in attribute ht_shield_t : Real;
    in attribute structure_t : Real;
    in attribute gap1_t : Real;
    in attribute vessel_t : Real;
    in attribute coil_t : Real;
    in attribute gap2_t : Real;
    in attribute lt_shield_t : Real;

    // Cumulative radii from the plasma minor radius outward.
    attribute vacuum_or : Real = a + vacuum_t;
    attribute firstwall_or : Real = vacuum_or + firstwall_t;
    attribute blanket_or : Real = firstwall_or + blanket_t;
    attribute reflector_or : Real = blanket_or + reflector_t;
    attribute ht_shield_or : Real = reflector_or + ht_shield_t;
    attribute structure_or : Real = ht_shield_or + structure_t;
    attribute gap1_or : Real = structure_or + gap1_t;
    attribute vessel_or : Real = gap1_or + vessel_t;
    attribute coil_or : Real = vessel_or + coil_t;
    attribute gap2_or : Real = coil_or + gap2_t;
    attribute lt_shield_or : Real = gap2_or + lt_shield_t;

    // Torus-shell coefficient C = kappa * 2*pi^2 * R.
    attribute C : Real = kappa * 2.0 * (pi ** 2) * R;

    // Per-layer torus-shell volumes.
    attribute firstwall_vol : Real = C * ((firstwall_or ** 2) - (vacuum_or ** 2));
    attribute blanket_layer_vol : Real = C * ((blanket_or ** 2) - (firstwall_or ** 2));
    attribute reflector_vol : Real = C * ((reflector_or ** 2) - (blanket_or ** 2));
    attribute ht_shield_vol : Real = C * ((ht_shield_or ** 2) - (reflector_or ** 2));
    attribute lt_shield_vol : Real = C * ((lt_shield_or ** 2) - (gap2_or ** 2));

    // CAS22 aggregate outputs.
    out attribute blanket_vol : Real = firstwall_vol + blanket_layer_vol + reflector_vol;
    out attribute shield_vol : Real = ht_shield_vol + lt_shield_vol;
    out attribute structure_vol : Real = C * ((structure_or ** 2) - (ht_shield_or ** 2));
    out attribute vessel_vol : Real = C * ((vessel_or ** 2) - (gap1_or ** 2));

    // First-wall area (standoff radius vacuum_or, not a) and coil-bore radius.
    out attribute wall_area : Real = kappa * 4.0 * (pi ** 2) * R * vacuum_or;
    out attribute r_coil : Real = vessel_or;
}
```

## Validation Plan

1. **L1–L3** on canonical `models/` after each edit; L1 must be 0 errors. The calc def is bigger than WI-020's (15 inputs, ~13 intermediates, 6 outputs) — watch for `**`/precedence and name-resolution parse errors.
2. **L6** extraction check — flat intermediates + outputs, same construct family as `'MFE Power Balance Calc'`; binding/constraint/redef-drop counters stay 0. Compare L2/L6 counts to the WI-020 baseline (L1=0, L2=3 pre-existing IFE, L6=105 pre-existing) — expect zero new issues.
3. **At implementation**: regenerate snapshot → V11 bridge → `run_stellaris.py` (oracle bit-exactness; the six geometry outputs = the pre-item-1 constants) → **verify `rb` outputs == 1cfe `geo` values** (D5 closure precondition) → `handshake_1costingfe.py` after removing the 5 injections (SV-025/026 **unchanged** — the closure proof) → IFE regression SV-023 (no IFE files touched) → confirm the Stellaris headline is unchanged (Option 1).
4. **Viability**: beta_ok, wall_load_ok, tbr_ok all still assert true (wall_area = 802.201 unchanged → wall_load unchanged).

## Implementation Checklist

1. **Library** — add `'MFE Radial Build'` to `mfe_plasma_scaling.sysml` (canonical + staged copy; confirm byte-identity of the analyses file first, then apply identically). Validate L1–L3.
2. **Generic plant** — add 11 thickness attributes (RadialBuild defaults) + `calc rb` block; add `:>> <vol> = rb.<vol>` to blanket/shield/structure/vessel parts and `:>> r_coil = rb.r_coil` to magnet. Staged copy likewise. Validate L1.
3. **Instance** — bind 11 thicknesses (cited); `wall_area = rb.wall_area`; rebind `special_materials_capital`; delete the six injected constants; rewrite the six doc comments to the forward computation. Staged copy likewise. Validate L1–L6 across `models/`.
4. **Oracle + regen** — mirror the rb formulas in `verify_stellaris.py`; regenerate snapshot + pipeline via V11 bridge; `run_stellaris.py` green (bit-exact; six outputs = constants).
5. **Handshake** — remove the 5 direct volume/r_coil injections; verify `rb` reproduces `geo` and SV-025/026 unchanged (D5). If closure is fragile, apply the D5 fallback (inject `rb__*`).
6. **Close-out** — flip SV-028 status; confirm the unchanged Stellaris headline in the work item and `.project/CURRENT_WORK.md`; note the six-constants fidelity gap closed; note Option 2 deferred in the epic.

## Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| Handshake closure breaks (volumes no longer injectable) | medium | high | D5: remove the 5 injections; `rb` reproduces `geo` from baked-in instance inputs; per-calc params keep `geom__a` override off `rb`; verify rb==geo before trusting; D5 fallback injects `rb__*` |
| `geo` computed at R ≠ 12.7, so `rb` ≠ `geo` | low | high if real | the pre-item-1 constants (=geo) verify at R=12.7; if implement finds a mismatch, surface it (real geometry inconsistency), don't absorb |
| Larger calc def hits a parse/precedence issue | low-med | low | explicit parens on every `**` and shell term; oracle + SV-028 catch a transcription slip |
| `special_materials_capital` expression outside codegen envelope | low | low | D6 fallback: instance literal with derivation in the doc; number unchanged |
| Defaulted thickness doesn't propagate to `rb__*_t` | low | medium | D4: instance binds all 11 explicitly, so the snapshot bakes real values — no reliance on default propagation |
| Staged/canonical drift on the analyses file | low | medium | confirm byte-identity before editing; apply identical edits to both |
