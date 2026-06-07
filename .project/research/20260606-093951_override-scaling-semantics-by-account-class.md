---
date: 2026-06-06T09:39:51-07:00
researcher: Claude
topic: "What a relative cost override actually does — step-by-step trace"
tags: [research, costingfe, cost-overrides, scaling, generic_reference, run_native_and_1gw]
status: complete
last_updated: 2026-06-06
supersedes_conclusion_of: 20260605-145424_relative-override-double-discount.md
---

# What a relative cost override actually does — walked through step by step

**Date**: 2026-06-06 · **Type**: Codebase / library semantics

Concept 24 (Dense Plasma Focus, `P_native = 5 MWe`). The analyst overrides
buildings: `CAS21 = 0.05 * generic.costs.cas21`. Here is exactly what the code
does, step by step, with the real number at each step (all computed live, not
asserted).

---

## The trace

```
STEP 1 - generic_reference(model, spec, P_native=5)
   runs: forward(net_electric_mw=5, n_mod=1, NO overrides)
   per-module power = 5 / 1 = 5 MWe
   library computes buildings for a 5 MWe reactor:
   >>> generic.costs.cas21 = 138.4 M$

STEP 2 - analyst writes the override
   value = 0.05 * generic.costs.cas21 = 0.05 * 138.4
   >>> override = {"CAS21": 6.92}

STEP 3 - run_native_and_1gw runs the 1 GWe projection
   calls: forward(net_electric_mw=1000, n_mod=200,
                  cost_overrides={"CAS21": 6.92},
                  override_reference_mw=5)

   STEP 3a - forward sees override_reference_mw=5, so FIRST it rescales the override.
      It runs two throwaway forwards with NO overrides:
        reference forward: forward(net=5,    n_mod=1)   -> CAS21 = 138.4   (REF)
        target    forward: forward(net=1000, n_mod=200) -> CAS21 = 138.4   (TGT)
            (1000/200 = 5 MWe per module; buildings computed per module and
             NOT multiplied by 200, so TGT = REF)
      ratio = TGT / REF = 138.4 / 138.4 = 1.000
      rescaled override = 6.92 * 1.000 = 6.92
      >>> override is now {"CAS21": 6.92}  (unchanged)

   STEP 3b - forward computes the plant at (net=1000, n_mod=200) using the override.
      at the buildings line:  CAS21 = override = 6.92 M$  (replaces default 138.4)
      >>> the entire 1 GWe / 200-module plant has buildings = 6.92 M$

   STEP 3c - forward finishes: sums all accounts, computes LCOE
      >>> headline LCOE = 19.02 $/MWh

WHAT WENT WRONG
   The override is 5% of 138.4 (REF) = ONE 5 MWe module's buildings.
   A real 1 GWe plant = one 1000 MWe reactor, whose buildings = 456.3 M$.
   The analyst's words were "5% of a conventional plant" = 0.05 * 456.3 = 22.8 M$.
   The framework delivered 6.92 M$  ->  3.3x too cheap.
   Root cause is STEP 3a: TGT came out 138.4 (one module) instead of 456.3,
   because buildings are NOT multiplied by the 200 modules.
```

---

## The two things to take away from the trace

1. **The override is real, it doesn't "cancel."** At STEP 3b buildings go from the
   default 138.4 to 6.92 M$, and the headline LCOE moves (20.98 with no override →
   19.02 with it). The only thing that "cancels" is the arithmetic at STEP 3a:
   `6.92 × (138.4 / 138.4)` — the two 138.4s cancel, so the override passes through
   the rescaling unchanged. That is *how* it lands, not proof it has no effect.

2. **The bug is at STEP 3a: `TGT = 138.4`, not 456.3.** The rescaler asks "how much
   bigger is this line at 1 GWe?" For buildings the answer comes back `×1.0`,
   because the 1 GWe projection is 200 little 5 MWe modules and the model never
   multiplies buildings by the 200. So the override stays anchored to *one small
   module's* buildings. The analyst meant "5% of a conventional plant" (5% of
   456.3 = 22.8 M$); the framework delivered 5% of 138.4 = 6.92 M$, which is 3.3×
   too cheap.

   (For concept 24 this only moves the headline LCOE ~1%, because buildings are a
   small slice of total capital — but the bias is real and it is in the headline,
   not just a display column.)

---

## Why STEP 3a behaves differently for different accounts

STEP 3a's `ratio = TGT / REF` is the whole game. It depends on what the library
does to that line when it goes from 1 module to 200:

| account class | examples | TGT vs REF | ratio at STEP 3a | net effect of an `M ×` override |
|---|---|---|---|---|
| **A — buildings-like (counted once)** | CAS21, CAS40, CAS70, most C2201xx | TGT = REF (not replicated) | **1.0** | stays 5% of **one small module** → too cheap by `mono/REF` (CAS21: 3.3×; deeper-scaling lines worse) |
| **B — per-module gear (×200)** | CAS23/24/25/26, CAS80 | TGT = 200 × REF | **= n_mod** | becomes 5% of the **full plant** → correct, matches "fraction of a conventional plant" |
| **C — blend** | CAS22 rollup, CAS30/50/60 | partly replicated | between 1 and n_mod | partway between |

Run the same trace for a **Class B** account (say CAS24) and STEP 3a comes back
`ratio = 200`, so `0.10 × 0.63 → 0.10 × 126.3 = 12.6 M$` — i.e. 10% of the full
1 GWe plant's electrical. No error. **Same syntax, opposite behavior**, and
nothing in `M * generic.costs.X` tells the author which case they are in. That is
the actual hazard for the authoring rules.

---

## Corrections to earlier conclusions

- **Prior research doc** (`20260605-...`) said the headline was "correct for the
  author's intent." Its number (6.92) was right; its interpretation was wrong —
  6.92 is 5% of a per-module figure, not 5% of a conventional plant. Headline is
  biased low for Class A, not "fine."
- **An earlier draft of *this* report** claimed Class A overrides are "off by
  ~200×". That was wrong — I confused the bug factor with `n_mod`. The real factor
  is `mono / REF` (the gap between one module's line and a conventional plant's
  line): CAS21 = 3.3×, and it varies a lot by account.

## Reproduce / verify

- Trace script behind this report: re-run the snippet that produced the STEP block
  (computes every number live).
- **Spike:** `exploration/concept_analysis/scripts/spike_override_semantics.py`
  (`--concept 24 --sweep --probe-edge-cases`) — per-account REF / TGT / ratio.
- **Test:** `1costingfe/tests/test_override_scaling_semantics.py` — pins Class A
  ratio = 1, Class B ratio = n_mod, CAS70/80 no-op.

## Open questions

1. **Library:** should Class A accounts (esp. CAS21) be multiplied by module count
   in the plant total? Today they are not — that is the STEP 3a root cause.
2. **Authoring rules:** must state each account's class and what `M` means, so the
   value and the rationale can't silently disagree.
