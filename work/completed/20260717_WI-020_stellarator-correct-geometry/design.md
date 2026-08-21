---
Status: complete
Created: 2026-07-17
Updated: '2026-07-17'
Related Artifacts:
  Spec: ./spec.md
---

> Process note: per the owner-ratified item process (handoff 2026-07-17), the single owner
> checkpoint sits after `/spec-model`; design → plan → implement → validate → handshake → close
> proceed without a further stop. Spec approved at checkpoint 2026-07-17: Decision B = B1 (agreed);
> Decision A = **do not re-solve sigma_v** — "make sure the model is accurate. We can test various
> inputs at the codegen phase."

# WI-020 Design: Stellarator-Correct Plasma Geometry

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read. Geometry/physics sourcing is the admissible Stellaris sources; engineering formulas are 1costingFE @ `0254385`.

## Overview

One calc def changes: `'Plasma Geometry'` gains a multiplicative shape/packing factor `f_shape` (default 1.0), so `V = 2π²Ra²κ·f_shape`. The generic plant threads `f_shape` through its `geom` block, and the Stellaris instance binds `f_shape = 0.794259` to reproduce the tabulated plasma volume 448 m³. Per the owner's Decision A, `sigma_v` is **not** re-solved — its doc comment is rewritten to remove the (now false) back-solve justification, and fusion power drops to a computed ≈ 2145 MW, re-baselining the downstream headline. The e2e artifacts (staged copies, generated pipeline, oracle, runner) follow; the Anchor A handshake is untouched because `f_shape` defaults to 1.0 on 1costingFE's torus point. No new files, no new SysML constructs — one added multiply and one defaulted input, both inside the proven codegen envelope.

## Research Findings

**The torus formula over-predicts the QI plasma volume.** At the Stellaris bindings (R=12.7, a=1.5, κ=1.0, pi=3.14159265358979):

```
V_torus = 2·pi²·R·a²·κ = 564.048 m³
```

The Stellaris source tabulates 448 m³ (`stellaris-design-details.md` Table 2, line 230). The QI plasma is a shaped, twisted column (bean cross-section varying around the torus), not a smooth elongated torus, so the torus formula runs ~26% high. The correction is a single multiplicative factor:

```
f_shape = 448 / 564.048 = 0.794259   →   V = 448.00 m³
```

**The prior cross-check note is arithmetically wrong** (spec Current State). `stellarator_plant.sysml:252-254` blames the gap on "R/a rounding, consistent with R=12.0, a=1.38." Torus at R=12, a=1.5 = 533 m³, not 448; a=1.38 only reaches 451 by shrinking a below the source's own 1.5 m. No source (R,a) reproduces 448 via the torus. Cause is shaping, not rounding — this design deletes the note and replaces it (MR-WI020-4).

**Source internal conflict (surfaced, owner ruled B1).** Table 2: R=12, V=448. Prose §2.1: R≈12.7. Fig. 2 text: V=425. The model keeps R=12.7 (prose + magnet R0 consistency) and targets the Table-2 volume 448; f_shape=0.794259 is therefore an empirical packing factor bundling the ~16% physical QI shaping (448/533 at the source's own R=12) with the source's R=12-vs-12.7 inconsistency. Documented as empirical, not first-principles (MR-WI020-2/4).

**V's only consumer is fusion power.** Verified by grep over `models/`: the sole reader of `geom.V` is `mfe_plant.sysml:120` (`in V = geom.V` into `'DT Fusion Power'`). p_fus is linear in V, so at the unchanged sigma_v:

```
p_fus_new = p_fus_old · (448/564.048) = 2700.5 · 0.794259 ≈ 2145 MW
```

This cascades (Decision A — no re-solve): p_alpha/p_neutron ∝ p_fus → p_th, p_the, p_et, p_net all fall → all power-scaled cost accounts and LCOE recompute. Hand-estimate at the WI-018 bindings (implement records executed values):

| channel | WI-019 (V=564) | WI-020 est. (V=448) |
|---|---|---|
| p_fus [MW] | 2700 | ~2145 |
| p_th [MW] | 3182.4 | ~2538 |
| p_the = p_et [MW] | 1059.7 | ~845 |
| p_net [MW] | 786.1 | ~575–590 |
| wall_load [MW/m²] | 2.69 | ~2.14 |
| q_eng | 3.87 | ~3.1 |

Net electric lands near the pre-WI-019 range: WI-019's power-balance gain (recovering alpha power) and this volume correction partly offset. All three viability constraints still pass (wall load gains margin; net electric stays clearly positive; q_eng > 1). Implement confirms with the executed numbers.

**Consumer map (complete, grep over `models/` + `exploration/`).**

| consumer | what it touches | change |
|---|---|---|
| `models/library/analyses/mfe_plasma_scaling.sysml:19-28` | `'Plasma Geometry'` calc def | add `in attribute f_shape : Real default 1.0;`; `V = 2·pi²·R·a²·κ·f_shape`; update doc |
| `models/designs/generic_mfe/mfe_plant.sysml:100-108` | plant geometry attrs + `geom` calc block | add `attribute f_shape : Real default 1.0;` and `in f_shape = f_shape;` |
| `models/designs/stellarator_09/stellarator_plant.sysml:256-264` | instance geometry bindings + cross-check note | add `:>> f_shape = 0.794259` (cited); rewrite the note (MR-WI020-4) |
| `models/designs/stellarator_09/stellarator_plant.sysml:270-296` | `:>> sigma_v` binding + doc | value **unchanged** (5.985e-23); doc rewritten (no back-solve claim) |
| `exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml` | staged copy (check byte-identity first) | same edit as canonical |
| `exploration/stellarator_e2e/models/designs/...` staged plant/instance | same bindings | same edits |
| `exploration/stellarator_e2e/verify_stellaris.py:15,56` | oracle params + formula mirror | add `f_shape=0.794259` to `IN`; `V = ... * p["f_shape"]` |
| `exploration/stellarator_e2e/run_stellaris.py:230` | headline V assertion | `564` → `448` (tol 2); other asserted headline values updated to executed |
| `exploration/stellarator_e2e/handshake_1costingfe.py:174` | 1cfe torus injection + sigma_v solve | **no change** — injects geom R/a/κ directly, f_shape falls to default 1.0; SV-025/026 unchanged |

Nothing else in `models/` or the IFE side references `geom.V` or plasma volume.

**Pipeline regeneration (from CODEGEN_FINDINGS.md, unchanged):** `sysml-codegen snapshot` over `exploration/stellarator_e2e/models/` → `bridge_v11_generate.py` (V11's params-coverage gate aborts on cross-part rollups, so the direct emit path is bypassed). Needs `SYSIDE_LICENSE_KEY` from `/home/reid/1cfe/fusion-tea/.env`. teax execution uses `exploration/pipeline_spike/.venv-exec`. The added `geom__f_shape` field flows through the regenerated sys_design JSON automatically; the harness glue keys off unchanged output names.

## Design Decisions

**D1 — multiplicative shape factor, not a direct V binding or an R change.** `V = 2π²Ra²κ·f_shape` keeps volume forward-computable from R/a/κ, so the geometry→fusion-power chain and SV-017 monotonicity (d(p_fus)/dR > 0) survive, and a single literal multiply stays in the codegen envelope. Rejected: (a) binding V directly — breaks the R→V→p_fus chain items 1/2 depend on; (b) changing R to 12.0 (Decision B3) — larger blast radius, contradicts prose, owner chose B1.

**D2 — `f_shape` default 1.0 (pure torus).** The default makes tokamak instances and the 1costingFE torus geometry unchanged, and — critically — guarantees the Anchor A handshake stays closed: the handshake injects `geom__R/a/κ` directly and never sets `geom__f_shape`, so the generated calc falls back to 1.0 and reproduces 1cfe's torus point bit-for-bit (SV-025/026 unchanged). This mirrors the proven defaulted-input pattern (`pi` in the same calc, `ash_frac` in `'Neutron Wall Load'`).

**D3 — sigma_v unchanged; fusion power computed (owner Decision A).** No re-solve. `sigma_v` stays 5.985e-23 (a genuine Bosch-Hale point at T_eff ≈ 7.9 keV). Fusion power becomes ≈ 2145 MW, an honest 0D output. The doc comment is rewritten to delete the back-solve justification (capture-fidelity correction rule — remove the false claim, don't annotate around it) and to state the 2145-vs-2700 gap as the visible 0D single-temperature limitation, target of item 2. This re-baselines the headline; that is the accepted, accurate outcome.

**D4 — factor threaded as a plant attribute defaulting to 1.0.** `'MFE Power Plant'` gets `attribute f_shape : Real default 1.0;` bound `in f_shape = f_shape;` in the `geom` block, and the Stellaris instance overrides `:>> f_shape = 0.794259`. The plant-level default 1.0 keeps the library concept-agnostic (MR-3): a tokamak instance need not bind it. *Codegen-envelope check at implement:* if a plant-attribute default proves outside the envelope (plant attrs R/a/κ currently carry no defaults), fall back to a plain `attribute f_shape : Real;` and rely on the instance binding (the only executing instance, stellarator_09, binds it) — the calc-def default 1.0 still covers the handshake path either way.

**D5 — output contract unchanged.** `geom.V` stays the single output; `'DT Fusion Power'` and everything downstream are untouched structurally. Only V's *value* changes (and, via it, p_fus and the cascade).

## Proposed Design

`'Plasma Geometry'` (`models/library/analyses/mfe_plasma_scaling.sysml`; staged copy identical):

```sysml
calc def 'Plasma Geometry' {
    doc /*
    Plasma volume [m^3].

      V = 2 * pi^2 * R * a^2 * kappa * f_shape

    The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus volume.
    f_shape is a dimensionless shape/packing factor: 1.0 for a pure torus
    (tokamak / the 1costingFE torus geometry), < 1 for a shaped stellarator
    plasma whose twisted, non-circular cross-section encloses less volume than
    the torus of the same R, a, kappa. Concept-agnostic; the concept sets
    f_shape.

    **Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
    **Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
    **Basis**: elongated-torus volume with a concept shape factor; MFE-generic
    */

    in attribute R : Real;
    in attribute a : Real;
    in attribute kappa : Real;
    in attribute pi : Real default 3.14159265358979;

    // Shape/packing factor. Default 1.0 = pure elongated torus (tokamak;
    // 1costingFE torus geometry). A shaped stellarator sets f_shape < 1.
    in attribute f_shape : Real default 1.0;

    out attribute V : Real =
        2.0 * (pi ** 2) * R * (a ** 2) * kappa * f_shape;
}
```

**Instance geometry** (`stellarator_plant.sysml`, replacing the cross-check note at 250-255 and adding the binding near 262):

```sysml
// PLASMA SHAPING (WI-020): the QI stellarator plasma is a shaped, twisted
// column, not a smooth elongated torus. The torus formula 2*pi^2*R*a^2*kappa
// over-predicts its volume: at R=12.7, a=1.5, kappa=1.0 it gives 564 m^3, but
// the Stellaris source tabulates 448 m^3 (Table 2). f_shape = 448/564 = 0.7943
// is an empirical packing factor reconciling the model's geometry inputs to the
// tabulated volume; it bundles the ~16% physical QI shaping (448/533 at the
// source's own R=12) with the source's internal R inconsistency (Table 2 R=12
// vs prose R=12.7; a second tabulated volume 425 m^3 appears in the Fig. 2
// text). Owner ruled (2026-07-17) to target the Table-2 headline 448 m^3 at the
// model's R=12.7. NOT a first-principles shaping coefficient.
:>> f_shape = 0.794259 {
    doc /* **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md **Ref**: Table 2 line 230 (plasma volume = 448 m^3) **Basis**: shape factor = tabulated V (448) / elongated-torus V (564.05) at R=12.7, a=1.5, kappa=1.0 */
}
```

**sigma_v doc rewrite** (`stellarator_plant.sysml`, value stays `5.985e-23`): delete the "reproduces the Stellaris 2700 MW design fusion power ... geometry volume (564 m³)" back-solve paragraph; replace with: sigma_v is a 0D-effective D-T reactivity at T_eff ≈ 7.9 keV (a real point on the Bosch-Hale `sigv_dt` curve, `reactivity.py:54-70`); at the corrected volume 448 m³ and the volume-averaged density it yields ≈ 2145 MW, **below** the Stellaris 2700 MW design point (Table 5 line 742); the gap is the 0D single-temperature limitation (real n, T profiles peak fusion in the hot core) and is the target of item 2 (predictive confinement), left visible here rather than closed by a back-solve.

**Oracle mirror** (`verify_stellaris.py`): add `f_shape=0.794259` to `IN`; `V = 2.0 * (p["pi"]**2) * p["R"] * (p["a"]**2) * p["kappa"] * p["f_shape"]`. sigma_v unchanged.

**Runner** (`run_stellaris.py:230`): headline V assertion `564` → `448` (tol 2); refresh the other asserted headline values to the executed numbers.

## Cross-File Bindings

| binding | file | change |
|---|---|---|
| `in f_shape = f_shape` (new) | `mfe_plant.sysml` `geom` block | add binding + plant attribute `f_shape : Real default 1.0` |
| `:>> f_shape = 0.794259` (new) | `stellarator_plant.sysml` | new binding + citation + shaping note |
| `:>> sigma_v = 5.985e-23` | `stellarator_plant.sysml` | value unchanged; doc rewritten |
| `in V = geom.V` | `mfe_plant.sysml:120` | unchanged (V value moves, wiring stable) |
| `net_electric_mw = pb.p_net` | `mfe_plant.sysml:320` | unchanged — LCOE denominator moves automatically |
| handshake `geom__R/a/κ` inject | `handshake_1costingfe.py:186` | unchanged; `geom__f_shape` not injected → default 1.0 |

Dataflow stays unidirectional: geometry → fusion power → power balance → cost spine → LCOE. Nothing new in the graph; one input added to the head node.

## Validation Plan

1. **L1–L3** on canonical `models/` after each edit; L1 must be 0 errors.
2. **L6** extraction check — flat defaulted attribute + one multiply; SV-024 wiring patterns unchanged; binding/constraint/redef-drop counters stay 0. Compare L2/L6 counts to the WI-019 baseline (L1=0, L2=3 pre-existing IFE, L6=105 pre-existing) — expect zero new issues.
3. **At implementation**: regenerate snapshot → V11 bridge → `run_stellaris.py` (oracle bit-exactness at the Stellaris point, V=448, computed p_fus) → `handshake_1costingfe.py` (SV-025 channels and SV-026 account gap **unchanged** — the closure proof for D2) → IFE regression SV-023 (no IFE files touched; re-run as standing regression) → record the re-baselined Stellaris headline → sigma_v sensitivity sweep for the owner.
4. **Viability**: confirm beta_ok, wall_load_ok, tbr_ok all still assert true at the lower power.

## Implementation Checklist

1. **Library edit** — add `f_shape` to `'Plasma Geometry'` (canonical + staged copy, identical). Validate L1–L3.
2. **Plant thread** — `mfe_plant.sysml` plant attribute + `geom` binding; staged copy likewise. Validate L1.
3. **Instance** — `stellarator_plant.sysml`: add `:>> f_shape = 0.794259` + shaping note; rewrite the sigma_v doc (value unchanged); clarify the wall_area "564" note (no value change). Staged copy likewise. Validate L1–L6 across `models/`.
4. **Oracle + regen** — update `verify_stellaris.py`; regenerate snapshot + pipeline via V11 bridge; `run_stellaris.py` green (bit-exact vs oracle, V=448); update runner headline asserts.
5. **Handshake** — re-run `handshake_1costingfe.py`; confirm SV-025/026 **unchanged** (D2 closure proof); no report edits beyond noting f_shape defaults to 1.0 on the torus point.
6. **Close-out** — flip SV-027 status; record the re-baselined Stellaris headline + sigma_v sensitivity in the work item and `.project/CURRENT_WORK.md`; update the STALE-BASIS annotations to the new p_net; note the volume gap closed and the 2145-vs-2700 design-point gap handed to item 2.

## Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| Plant-attribute default 1.0 outside codegen envelope | low | low | D4 fallback: plain `attribute f_shape : Real;` + instance binding; calc-def default still covers the handshake |
| Regenerated pipeline breaks harness glue | low | medium | glue keys off unchanged pb output names; `run_stellaris.py` oracle check gates before the handshake |
| Lower power pushes a viability constraint to fail | low | high if it happened | estimates keep all three comfortably passing (wall load gains margin; p_net ≈ 580; q_eng ≈ 3.1); implement confirms with executed values before close |
| SV-016 band (Q_eng 10–40) reads low at q_eng ≈ 3.1 | certain to surface | low | already open from WI-019 (pre-fix order-of-magnitude band); owner adjusts/annotates, not silently edited |
| STALE-BASIS pass-throughs drift further at new p_net | certain | low | annotations updated to new p_net; recomputation stays the Stage-3 account item (out of scope) |
| Handshake accidentally changes | very low | high | D2: f_shape never injected in the handshake; verify SV-025/026 byte-identical at re-run |
