# Report: How 1costingFE Power Scaling Works, and the Actual Issues in Current Pipeline Usage

**Date:** 2026-05-30 (rewritten — an earlier draft mis-framed the library's two-knob scaling as a defect; corrected here)
**Author:** Claude
**Scope:** `costingfe` scaling mechanics + intended usage, then the real issues in how the live `model_setup.py` files invoke it
**Related:** `.project/research/20260530-072832_1costingfe-and-pipeline-redesign-context.md`, `.project/concepts/concept-analysis-rework.md`

---

## Summary

`costingfe` separates three things by design: the **geometry of one module** (an exogenous input — the library costs the design you give it; it does not size a machine), the **per-module output power**, and the **number of modules** (`n_mod`). Reaching a target plant power uses **two scaling knobs together**: `net_electric_mw` scales the shared plant and sets per-module power; `n_mod` replicates the reactor island. The coil account being invariant under `net_electric_mw` is **correct and intended** — the reactor island scales by module count, not by cranking one module's output.

The actual issues are not in the library. They are in how the current pipeline invokes it: it never uses `n_mod`, invokes `forward()` three inconsistent ways across the 41 concepts, and lets the explorer silently compare some concepts off the 1 GWe basis.

---

## Part A — How `costingfe` scales (intended design)

### A.1 Three independent quantities

`forward()` is given:

- **Module geometry** — the radial build (`R0`, `plasma_t`, `elon`, thicknesses). This is a fixed input. `compute_geometry(rb, concept)` (`geometry.py:94`) takes **no power argument**; component volumes are a function of geometry alone. The library costs the design you hand it — it does not derive a machine size from a power target. To model a physically larger machine, you give it larger geometry.
- **`net_electric_mw`** — total plant net electric output.
- **`n_mod`** — number of identical reactor modules on the site (default 1).

Per-module power is `net_electric_mw / n_mod` (`model.py:105`). The power balance solves **each module** at that power on the given geometry.

### A.2 Two scaling knobs, by design

| Knob | What it scales | Mechanism |
|---|---|---|
| **`net_electric_mw`** | The **shared plant** — BOP (CAS23–26) and plant-wide reactor auxiliaries (coolant, cryoplant, rad-waste, fuel handling, I&C; C220200–C220700), all sized once at total plant power (`cas22.py:380–381`, `p_*_total = n_mod * p_*`). Also sets per-module power, which drives the per-module power-law cost terms. | Power balance + per-account power laws |
| **`n_mod`** | The **reactor island** — per-module equipment (C220101–C220112) multiplied by `n_mod` copies; installation labor (C220111) gets a multi-unit discount (`×(1 + (n_mod−1)·0.92)`); land scales `√n_mod`; CAS72 replacement and the LCOE denominator scale with `n_mod`. | `per_module_equipment * n_mod + labor + plant_wide` (`cas22.py:451–453`) |

### A.3 Per-account behavior (verified against `cas22.py`)

For a reactor-island account with per-module power exponent **α**, total cost over `n_mod` copies of a fixed-geometry module is **`∝ net^α · n_mod^(1−α)`** (per-module cost `∝ (net/n_mod)^α`, times `n_mod` copies). This single relation explains the whole spectrum:

| Account | Formula | α | Scales with `net` | Scales with `n_mod` |
|---|---|---|---|---|
| **C220103 coils** | `G·b_max·r_coil² · $/kAm · markup` (`:201–203`) | **0** | **no** (net⁰) | **yes, linearly** (n_mod¹) |
| C220101 blanket | `unit · form · blanket_vol · (p_th/REF)^0.6` (`:160`) | 0.6 | net⁰·⁶ | n_mod⁰·⁴ |
| C220102 shield | `unit · shield_vol · scale · (p_th/REF)^0.6` (`:178`) | 0.6 | net⁰·⁶ | n_mod⁰·⁴ |
| C220105 structure | `unit · structure_vol · (p_et/REF)^0.5` (`:261`) | 0.5 | net⁰·⁵ | n_mod⁰·⁵ |
| C220106 vessel | `unit · vessel_vol · (p_et/REF)^0.6` (`:268`) | 0.6 | net⁰·⁶ | n_mod⁰·⁴ |
| Plant-wide C220200–700 | functions of `p_*_total` (`:380–381`) | 1 (on total) | net¹ | none (sized once) |
| BOP CAS23–26 | linear in total `p_th`/`p_et` | 1 (on total) | net¹ | none (sized once) |

So the coil account having **no power term is by design**: the reactor island is meant to scale by **replication** (`n_mod`), and the magnets are a per-module manufactured object. `net_electric_mw` deliberately does not multiply them — that is `n_mod`'s job.

### A.4 Intended usage patterns

- **Single machine of power P:** give that machine's geometry, `net_electric_mw=P`, `n_mod=1`.
- **Modular plant:** give one module's geometry, set `n_mod` and `net_electric_mw` so per-module power (`net/n_mod`) matches the module's design point; the reactor island replicates and the shared plant is sized for the total.
- **Caveat — what one knob alone means:** raising `net_electric_mw` on a single fixed module (`n_mod=1`) models *"the same machine running at higher power density,"* not *"a bigger machine."* That is a valid query but is rarely the right way to reach utility scale from a sub-scale module — `n_mod` is.

---

## Part B — Cost-override mechanism (intended)

### B.1 `cost_overrides`

A dict of per-account M$ values that **replace** the computed value (`model.py:557–713`). Overridable: top-level CAS10–28 and the CAS22 sub-accounts (`C220101…C220700`). Reactor-island sub-account overrides are treated as **per-module** costs — they are summed into `per_module_equipment` and multiplied by `n_mod` (`model.py:664–676`), exactly like the computed accounts. Plant-wide and BOP overrides replace plant-total values.

### B.2 `override_reference_mw` (optional)

When an override **value comes from a design at a different power than the one being modeled**, `override_reference_mw` rescales it. `_scale_overrides` (`model.py:849–896`) runs the bare model at the reference and target powers and multiplies the override by that account's own computed ratio:

```python
# model.py:888–889
if ref_val > 0:
    scaled[key] = value * (tgt_val / ref_val)
```

It has no independent scaling model — it borrows each account's library power-law, so an override scales the same way the account does. Intended use: *"I have an empirical cost from a 400 MWe study but I'm modeling 1000 MWe."* It only engages when **both** `override_reference_mw` and a non-empty `cost_overrides` are present (`model.py:418`).

Note the interaction with the `n_mod` approach: if each module runs at its native power, overrides are already per-module facts at that power and need **no** reference scaling — they ride `×n_mod` automatically. `override_reference_mw` is the tool for the single-machine output-power-scaling workflow, not the modular workflow.

### B.3 One genuine library footgun

`override_reference_mw` is **silently ignored** when `cost_overrides` is empty (it is gated by `... and cost_overrides`, `model.py:418`). Passing it without overrides is a no-op, not an error. Defensible (there is nothing to scale), but it gives no warning — and the current pipeline relies on it in exactly that dead-end way (see Part C).

---

## Part C — Actual existing issues (current pipeline usage)

These are real, verified against the 41 live `model_setup.py` files and the explorer. None is a library defect; all are usage.

### C.1 The pipeline never uses `n_mod` (> 1)

Every `model_setup.py` runs a single module. So for any concept whose design point is **below 1 GWe**, nothing replicates the reactor island to 1 GWe. The magnets and the rest of the island are costed for one sub-scale module and then either not scaled at all, or "scaled" only via output power on that one frozen module — which, by A.3, does not move the coils. The library's intended mechanism for reaching scale (replication) is simply not invoked anywhere.

### C.2 Three inconsistent invocation patterns → "1 GWe NOAK" is not a uniform basis

Classifying each file by (has `result_1gw`?) × (passes `cost_overrides`?) × (passes `override_reference_mw`?), with native design-point power:

**Pattern 1 — no `result_1gw`:** the explorer falls back to native `result` (`extract_explorer_data.py:262`: `effective_result = result_1gw if result_1gw is not None else result`), so the concept enters the comparison **at its native power**:

| Concept | Native MWe compared | Note |
|---|---|---|
| 01-hts-compact-tokamak | **261** | magnet-dominated; overrides applied directly at native |
| 17a-laser-icf-hybrid-drive | **400** | overrides at native |
| 28-hts-tokamak-full-hts | **500** | 8 overrides at native |

(03, 04, 07, 08, 09, 10 are native-only too but native = 1000, so no distortion. Concepts 02, 12, 13, 15, 16, 18, 19, 22, 24, 27, 35, 38 are freeform/unmodeled — no `forward()`.)

**Pattern 2 — `override_reference_mw` set, no `cost_overrides` (no-op, B.3):** `result_1gw` is just `forward(net_electric_mw=1000)` on a single frozen module; the reactor island does not replicate:

| Concept | Native MWe | Single-module output-power scale |
|---|---|---|
| 34-compact-spherical-tokamak-india | **50** | 20× |
| 05-planar-coil-stellarator | 390 | 2.6× |
| 39-spherical-tokamak-cs-free-p-b11 | 500 | 2× |
| 21-spherical-tokamak-hts | 600 | 1.67× |

(23, 36, 37 here too but native = 1000.) Several of these carry comments claiming the framework is scaling overrides — there are none to scale.

**Pattern 3 — `override_reference_mw` + `cost_overrides` (scaling engaged):** overridden accounts scale by their power-law, but the single module's non-overridden island still does not replicate:

| Concept | Native MWe |
|---|---|
| 29-negative-triangularity-tokamak | **90** |
| 14-magnetized-target-pneumatic | 300 |
| 20a-type-one-stellarator | 350 |

(06, 11, 25, 26, 30, 31 here too but native = 1000.)

### C.3 Net effect

The explorer places side by side, all labeled "1 GWe NOAK":

- native-power machines at 261 / 400 / 500 MWe (never scaled),
- single frozen modules repriced to 1000 MWe via output power (reactor island, including coils, never replicated),
- genuine 1000 MWe single-machine designs.

The worst-affected are the sub-scale magnetic concepts — **34 (50), 29 (90), 01 (261)** — whose reactor-island cost never reaches 1 GWe scale because `n_mod` is unused. This is the concrete, localized source of the cross-concept "not comparable" symptom.

---

## Part D — What correct usage is (pointer)

The intended way to put every concept on one 1 GWe basis is to use **both** knobs: `forward(net_electric_mw=1000, n_mod=1000/P_native)` — each module held at its native operating point, the reactor island replicated to 1 GWe, the shared plant sized at 1 GWe. This is using the library as designed, not fixing it. The one library change it needs is to accept a non-integer `n_mod` (a `validation.py:90` relaxation). See `concept-analysis-rework.md`, Key Concept 6, for the full mechanism.

---

## Key code references

- `model.py:105` — per-module power `= net_electric_mw / n_mod`
- `model.py:418` — `override_reference_mw and cost_overrides` gate (silent no-op when no overrides)
- `model.py:530–544` — power balance then geometry; `net_electric_mw` never enters the radial build
- `model.py:642–676` — per-module equipment keys × `n_mod`; per-module overrides replicated
- `model.py:849–896` — `_scale_overrides` (override rescaling by per-account ratio)
- `layers/geometry.py:94` — `compute_geometry`, no power argument
- `layers/cas22.py:160/178/201–203/261/268` — blanket/shield/**coils (no power term)**/structure/vessel
- `layers/cas22.py:380–381, 451–453` — plant-wide accounts on total power; reactor-island × `n_mod` + labor discount
- `concept_explorer/extract_explorer_data.py:262` — `result_1gw` else native `result`
- Live examples: `analyses/21-spherical-tokamak-hts/model_setup.py:187–197` (Pattern 2 no-op), `analyses/01-hts-compact-tokamak/model_setup.py` (Pattern 1, native 261 MWe)
