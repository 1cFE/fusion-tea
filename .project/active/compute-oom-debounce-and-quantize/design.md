# Design: Compute OOM — Client Debounce + Server Cache Quantization

**Status**: Draft
**Owner**: Reid W
**Created**: 2026-06-29
**Updated**: 2026-06-29
**Branch**: `feat/explorer-web-hosting`
**Commit**: 6be4095e

## Overview

Cut the volume and cost of `/api/compute` calls that OOM-kill the Railway-deployed explorer, via two independent levers: fewer client requests (longer debounce + abort the superseded fetch) and more server cache hits (quantize override floats to 4 sig figs before the LRU lookup).

## Related Artifacts

- Spec: `.project/active/compute-oom-debounce-and-quantize/spec.md`
- Deployment track: `.project/active/explorer-web-hosting/` (RUNBOOK, parity gate)
- Parity gate: `scripts/parity_explorer.py` (FR-SO1 post-deploy validation)

## Research Findings

Three integration points, all confirmed in the current tree:

- **`static/js/tornado.js:55`** — `const SLIDER_DEBOUNCE_MS = 200;`. The only consumer is `_scheduleFire()` (`tornado.js:198`), which `clearTimeout`/`setTimeout`s `onSliderChange({ ...overrides })`. Changing the constant is the whole of L1-1. Note `overrides` here is the **full** param map (every slider's current value, baseline for unmoved ones), not a delta — so every fire carries ~15 floats.
- **`static/js/concept_page.js:583` `onSliderChange(overrides)`** — `async` fetch to `/api/compute`, then updates sticky headline + CAS. Two UI elements matter: `headlineLoadingEl` (`#headline-loading`, the "Recomputing…" indicator, shown at entry) and `computeErrorEl` (`#compute-error`). **Critical finding:** the `finally` block at `concept_page.js:619` *unconditionally* hides `headlineLoadingEl`. A naive abort would make the superseded request's `finally` hide the indicator while the replacement request is still in flight — violating L1-2 ("indicator stays visible until the final response arrives"). The design must guard the hide. The same function's `catch` (`:613`) shows a compute error on any throw — an `AbortError` must be excluded so aborts fail silently (L1-2).
- **`server.py:1084` `compute()`** — thin wrapper: 404/422 guards, then `_compute_cached(concept_id, frozenset(body.overrides.items()), apply_analyst_overrides)`. `_compute_cached` is `@lru_cache(maxsize=128)` (`server.py:990`). Quantization belongs between unpacking `body.overrides` and building the frozenset, so the cache key is the rounded map. `ComputeRequest` (`models.py:617`) stays untouched (L2-3).

Supporting facts:

- **`onModeSwitch()` (`concept_page.js:669`)** also POSTs `/api/compute`, but with `overrides: {}` and only on a discrete toggle click — low frequency, not a drag burst. Out of scope for the abort logic; see Non-Goals.
- **Parity gate sends `overrides={}`** (`parity_explorer.py:100`). An empty map has nothing to quantize, so the FR-SO1 no-op path is byte-for-byte unchanged by L2 — AC #4 holds by construction, not by luck. (Quantization only ever touches *non-empty* override maps from real drags.)
- **Override values are `dict[str, float]`** (`models.py:621`). Quantization applies uniformly; the rounding helper must still handle `0.0` and negatives defensively (sig-fig math takes `log10`).
- **Existing test `test_compute_cache_hit_module_not_reloaded`** uses `availability: 0.85`, which rounds to itself at 4 sig figs — the test stays green. No test currently asserts the cache *misses* on near-but-distinct floats, so AC #2 needs a new test.

## Core Concept

Two unrelated bottlenecks sit on the same request path, so we attack both with the smallest possible change at each and let them compound. **Client side:** raise the debounce to 400 ms (halves the steady-state drag rate) and wrap each compute fetch in an `AbortController` so a new fire cancels the previous one — together these cap each client at one in-flight compute at a time. **Server side:** the LRU cache misses because full-precision IEEE-754 floats are almost never equal; round every override to 4 significant figures *at the cache boundary* so slider positions that are indistinguishable at display precision collapse onto one key and one `forward()`. Neither lever changes any contract: the slider UX, the `ComputeRequest` schema, and the `forward()` call are all identical. The key insight is that quantization is a property of the *cache key*, not the model — it lives in the four lines of `compute()` between the request and `_compute_cached`, invisible to everything else.

## Key Bets

- **B1.** Reducing concurrent `forward()` calls (fewer requests + higher cache-hit rate) lowers peak RSS enough to stay under Railway's limit at realistic multi-user load. *If false → the explorer still OOMs and we need the out-of-scope `forward()` semaphore / memory-tier bump anyway.*
- **B2.** 4-sig-fig input rounding is below the noise floor of the displayed LCOE (`$XXX.XX/MWh`), so no user-visible number changes. *If false → headline/CAS values shift visibly between adjacent slider positions and the quantization is too aggressive.*
- **B3.** Real drag traffic clusters into a small set of distinct quantized positions, so 128 cache slots are enough to serve hits across concurrent users. *If false → the cache thrashes anyway and the hit-rate gain doesn't materialize.*

## Key Decisions

- **D1.** Quantize to **4 significant figures**, not N decimal places. *Rejected: fixed decimals (`round(x, 4)`) — parameters span many orders of magnitude (availability ~0.85 vs cost ~5000), so a fixed decimal count is either too coarse for small params or a no-op for large ones. Sig figs give a uniform relative error (<0.01%).*
- **D2.** Quantize **inside `compute()`**, before `_compute_cached`. *Rejected: quantizing inside `_compute_cached` or `_forward_with_overrides` — would bury a behavioral change deeper in the call stack and couple it to the model path; the cache boundary is the natural seam (D2 keeps the rounded value as both the key and the computed input, so a hit and its miss agree).*
- **D3.** Guard the "Recomputing…" hide with a **current-controller identity check**, not a flag toggled in `catch`. *Rejected: a boolean `aborted` flag — racy across overlapping closures; comparing `this request's controller === the latest controller` is the standard stale-closure guard and reads cleanly.*
- **D4.** Scope the `AbortController` to **`onSliderChange` only**. *Rejected: also wrapping `onModeSwitch` — it's a discrete toggle, not a burst; adding abort there is unrequested scope and risks cross-cancelling a slider fetch with a mode switch.*

## Architecture

Three files, each touched independently; no new modules, no shared state between the client and server changes.

```
 drag ──▶ tornado.js                concept_page.js                 server.py
          _scheduleFire()           onSliderChange(overrides)       compute(body)
          debounce 200→400ms  ─────▶ abort prev controller          quantize overrides
                                     fetch(signal) ────/api/compute─▶ → frozenset → _compute_cached
                                     guard hide on stale                (LRU maxsize=128)
```

- **Client request reduction** is entirely within the browser: the debounce constant and the abort wiring don't talk to each other beyond both living on the slider-fire path. The `AbortController` is created per `onSliderChange` call and stored in an enclosing-scope `let inflightController`; entry aborts the prior one and installs itself as current.
- **Server quantization** is a pure transform at the endpoint boundary. A module-level helper `_quantize_sig(x, sig=4)` rounds one float; `compute()` maps it over `body.overrides` before constructing the frozenset cache key. `_compute_cached` and everything downstream are unchanged — they simply receive already-rounded values.

## Required Invariants

- **INV-A (one in-flight per client).** After any `onSliderChange` fire, at most one `/api/compute` fetch issued by the slider path is outstanding; a new fire aborts the previous.
- **INV-B (indicator liveness).** The "Recomputing…" indicator is visible from the first fire until the *final, non-aborted* response settles — never hidden by a superseded request, never left stuck on after the final response.
- **INV-C (FR-SO1 preserved).** A no-op recompute (`overrides={}`) produces the stored headline. Trivially held: empty map → no quantization → identical to today. `parity_explorer.py` passes at `REL_TIGHT=1e-5`.
- **INV-D (schema stability).** `ComputeRequest` accepts the same full-precision floats; quantization is server-internal and invisible to callers.
- **INV-E (key/value agreement).** The value used to compute a result equals the value in its cache key (both rounded) — no cache entry keyed on a rounded float but computed from a raw one.

## Component Overview

- **`tornado.js` `SLIDER_DEBOUNCE_MS`** (`:55`) — single constant, 200 → 400. Sole behavioral knob for L1-1.
- **`concept_page.js` `onSliderChange`** (`:583`) — gains an `AbortController`: declare `inflightController` in the enclosing scope, abort-and-replace at entry, pass `controller.signal` to `fetch`, swallow `AbortError` in `catch`, and gate the `finally` hide on `controller === inflightController`.
- **`server.py` `_quantize_sig` + `compute`** — new private helper (4-sig-fig rounding, 0/negative-safe) plus a one-line map over `body.overrides` inside `compute()` (`:1084`) before the frozenset.

## Non-Goals

- Server-side concurrency limiting (a semaphore around `forward()`) — explicitly out of scope per spec; B1 bets we don't need it.
- Abort/dedup on `onModeSwitch` or any non-slider compute call (D4).
- Railway memory-tier changes or `maxsize` tuning (L2-4 keeps 128).
- Any change to `CostModelData`, `forward()`, or the `/api/compute` contract.

## Implementation Notes

- **Sig-fig helper, edge cases.** `x == 0.0 → 0.0`; use `abs(x)` for the `log10` exponent; preserve sign. Sketch (the whole helper, not a fragment to expand):

  ```python
  def _quantize_sig(x: float, sig: int = 4) -> float:
      if x == 0.0 or not math.isfinite(x):
          return x
      exp = math.floor(math.log10(abs(x)))
      return round(x, -(exp - (sig - 1)))
  ```

- **Abort guard shape** (pseudo, in `onSliderChange`): at entry `inflightController?.abort(); const controller = inflightController = new AbortController();` → `fetch(..., { signal: controller.signal })` → in `catch`, `if (err.name === 'AbortError') return;` (before showing `computeErrorEl`) → in `finally`, `if (controller === inflightController && headlineLoadingEl) headlineLoadingEl.style.display = 'none';`. The `return` in `catch` still runs `finally`, but the identity check makes the hide a no-op for a superseded request, satisfying INV-B.
- **`math` is NOT currently imported in `server.py`** (verified) — add `import math` to the stdlib import block. The helper can alternatively avoid `math` with `f"{x:.4g}"`/`float()`, but `log10` rounding is clearer and exact; prefer adding the import.
- Keep `_quantize_sig` module-level (not a closure inside `create_app`) so it's unit-testable in isolation.
- Do not round inside `_compute_cached` — INV-E requires the rounded value to be both key and computed input, which D2's placement guarantees.

## Potential Risks

- **400 ms feels laggy.** Mitigated: the indicator shows immediately on input; spec allows tuning to 300 ms without a spec revisit. Low risk.
- **Quantization shifts a visible digit** (B2 false). Mitigated by 4 sig figs (<0.01%) vs 2-decimal display; the new AC #2 test plus `parity_explorer.py` bound the regression. If a param's display is unusually precise, revisit `sig`.
- **Abort guard race** leaving the indicator stuck on. Mitigated by INV-B's identity check: the final (current) request always owns the hide. Covered by manual UI verification (spec AC #5).
- **B1 insufficient** — OOM persists. Then the out-of-scope semaphore becomes the next work item; this design is still a strict improvement and a prerequisite (fewer concurrent calls is necessary either way).

## Integration Strategy

Drops into the live `feat/explorer-web-hosting` branch alongside the existing deployment work. No data regeneration, no migration, no API version bump. Complements (does not replace) the parity gate, which continues to validate FR-SO1 post-deploy. The three edits are independent and could land in separate commits, but ship together since they jointly target the one OOM symptom.

## Validation Approach

- **Unit (server).** New `test_compute_quantizes_near_floats_to_one_forward_call`: POST `availability=0.6902` then `0.6903`, assert `_load_model_module`/`forward` ran once (mirror the existing cache-hit test's counting pattern) → AC #2. Add a direct `_quantize_sig` table test (0, negative, 0.85→0.85, 5000.4→5000, 0.69017…→0.6902).
- **Regression (server).** Existing `test_state_and_compute.py` stays green (0.85 rounds to itself). Run the file.
- **Parity (deploy).** `python scripts/parity_explorer.py http://127.0.0.1:8421` passes at default tolerance → AC #4 / INV-C.
- **Manual UI (`browser-inspect` skill).** Drag a slider fast: indicator appears immediately, headline updates after the final settle, no error flash, fewer intermediate updates than before → AC #1/#5. Read the JSON sidecar for console errors (AbortError must *not* surface as a page error).
- **Client request count.** In the browser Network panel (or a `--eval` counter), confirm a sustained 1 s drag yields ≤ ~3 compute requests → AC #1.

## Next-Stage Handoff

- **Fixed:** the three integration points and their line anchors; 4 sig figs; abort scoped to `onSliderChange`; `maxsize=128`; `ComputeRequest` unchanged.
- **Open (plan may choose):** exact new-test file placement (extend `test_state_and_compute.py` vs new file); whether to also add a `_quantize_sig` micro-test module; the precise debounce value if 400 ms is later tuned.
- **De-risk first:** the `finally`-hide guard (INV-B) — it's the one place a wrong edit produces a stuck or flickering indicator. Implement and eyeball it with `browser-inspect` before the rest.

## Implementation Notes (2026-06-29)

**Completed** directly from this design (no separate plan.md — change was small).

**Changes made:**
- `tornado.js:55` — `SLIDER_DEBOUNCE_MS` 200 → 400 (L1-1), with rationale comment.
- `concept_page.js` — `inflightController` declared in the cost-model scope; `onSliderChange` aborts the prior controller, installs itself as current, passes `signal` to `fetch`, returns silently on abort, and gates the `finally` indicator-hide on `controller === inflightController` (L1-2 / INV-B).
- `server.py` — added `import math`; module-level `_quantize_sig(x, sig=4)` (0/inf/negative-safe); `compute()` maps it over `body.overrides` before the frozenset cache key (L2-1/L2-2/L2-3). `maxsize=128` unchanged (L2-4). `ComputeRequest` untouched (L2-3 / INV-D).
- `test_state_and_compute.py` — `test_quantize_sig_rounds_to_four_significant_figures` (table) + `test_compute_quantizes_near_floats_to_one_forward_call` (AC #2, counting-load pattern).

**Deviations from design:**
1. **Abort detection uses `controller.signal.aborted`, not `err.name === "AbortError"`.** The repo's `test_no_raw_name_label_render` (test_identity_frontend.py) globs every JS file for raw `.name` reads to catch concept-name render divergence; `err.name` is a false positive there. `signal.aborted` answers "was *this* fetch aborted" directly, is more robust, and sidesteps the guard rather than blinding it by whitelisting the file. (The comment was also reworded — the lint is line-based and matched the token inside the comment too.)
2. **Spec's L2-1 quantization example was imprecise.** `0.6902` and `0.6903` already have 4 sig figs and stay *distinct*; the test instead uses `0.69021`/`0.69018`, which both round to `0.6902` (verified empirically). The collapse acts on floats differing *below* the 4th sig fig — the real slider-drift case (`0.6901750000000001 → 0.6902`).

**Verification:**
- `test_state_and_compute.py` — 15/15 pass.
- Full explorer suite — exact parity with base (32 pre-existing failures, all unrelated: data/fixture/browser-manual; `test_views_manual.py`/`test_integration_manual.py` errors; the FR-SO1 `>5%` stale-assertion already documented in CURRENT_WORK.md). My change adds 2 passing tests and **zero** new failures (confirmed by stash-diffing base vs branch).
- Parity gate (`scripts/parity_explorer.py` vs running server) — 33/33 within 1e-5, worst-dev 0.0000% (FR-SO1 / AC #4).
- Browser (`browser-inspect`) — 6 rapid input events → 1 compute request (AC #1); single drag → headline 107.6 → 103.0 with ▼4.2% delta, indicator cleared, no error flash, 0 console/page errors (AC #3/#5).

**Not done (out of scope / pre-existing):** server `forward()` semaphore (spec out-of-scope); the pre-existing FR-SO1 `>5%` stale test assertion (separate loose end, not touched per "no unsolicited fixes").

---
Next Step: After approval → `/_my_plan` (or `/_my_implement` — the change is small enough to implement directly).
