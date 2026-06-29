# Spec: Compute OOM — Client Debounce + Server Cache Quantization

**Status**: Implementation Complete (2026-06-29)
**Scale**: standard
**Owner**: reid
**Created**: 2026-06-29
**Branch**: `feat/compute-oom-debounce-quantize` (off `feat/explorer-web-hosting`)

## Problem

The Railway-deployed concept explorer is being OOM-killed under multi-user slider load. The Linux OOM-killer fires SIGKILL (no traceback, just `Killed`), uvicorn restarts, and users see HTTP 502 during the ~10-30s restart window.

**Root cause chain:**

1. Slider `input` events fire every drag increment. The existing 200ms debounce in `tornado.js:55` collapses sub-200ms bursts but still produces ~5 requests/second per user during a sustained drag.
2. Each request carries raw IEEE 754 floats (e.g. `availability: 0.6901750000000001`). The server LRU cache key is `(concept_id, frozenset(overrides.items()), apply_analyst_overrides)` — full float precision means nearly every request is a cache miss.
3. Each cache miss runs `model.forward()` through JAX, allocating transient arrays. With multiple concurrent users, multiple `forward()` calls run simultaneously with no concurrency bound.
4. Cumulative transient JAX allocations push RSS past Railway's memory limit. OOM-killer fires SIGKILL.

**Additionally**, `concept_page.js:onSliderChange` (line 583) does not cancel in-flight requests. If a debounce fires request A, then 200ms later fires request B, both run `forward()` to completion on the server — request A's response is silently discarded by the client but the server already spent the memory computing it.

## Scope

This spec covers two coordinated fixes ("Layer 1" and "Layer 2" from the initial diagnosis):

1. **Client-side request reduction** — reduce the volume of `/api/compute` requests reaching the server.
2. **Server-side cache quantization** — increase LRU cache hit rate by rounding override values so nearby slider positions share a cache key.

Out of scope: server-side concurrency limiting (a semaphore around `forward()`), Railway memory tier changes, and any changes to the `CostModelData` response shape or the `forward()` call itself.

## Requirements

### Layer 1: Client-side request reduction

**L1-1. Increase debounce interval.** Change `SLIDER_DEBOUNCE_MS` in `tornado.js` from 200ms to 400ms. This halves request rate during sustained drags (~5 req/s → ~2.5 req/s) while remaining responsive enough that users see the headline update before they finish dragging.

**L1-2. Cancel in-flight requests.** In `concept_page.js:onSliderChange`, use an `AbortController` to abort the previous `/api/compute` fetch when a new debounced fire occurs. This ensures at most one in-flight compute request per client at any time. The aborted fetch should fail silently (not show a compute error), and the "Recomputing..." indicator should stay visible until the final (non-aborted) response arrives.

**L1-3. No visual behavior change.** The slider UX must feel the same: drag → brief "Recomputing..." → headline + CAS update. The only observable difference is that very fast drags produce fewer intermediate updates. Reset behavior is unchanged (it does not call `/api/compute`).

### Layer 2: Server-side cache quantization

**L2-1. Quantize override values before cache lookup.** In the `compute()` endpoint function (`server.py`, line 1084), round each override value to 4 significant figures before passing to `_compute_cached`. This collapses nearby slider positions into the same cache key. Example: `availability=0.6902` and `availability=0.6903` both round to `0.6902` at 4 sig figs, producing one `forward()` call instead of two.

**L2-2. Quantization precision: 4 significant figures.** This gives <0.01% rounding error on the input, which is well below the display precision of LCOE results (displayed as `$XXX.XX/MWh`). The slider has 200 discrete positions per parameter; at 4 sig figs, adjacent positions typically differ by enough to remain distinct when the parameter range is wide, while collapsing positions that are indistinguishable at display precision. 4 sig figs also preserves FR-SO1 (no-op recompute matches stored headline) because the baseline values round to themselves at this precision.

**L2-3. Quantize in the endpoint, not the model.** The `ComputeRequest` Pydantic model and the `/api/compute` API contract are unchanged — clients still send full-precision floats. Quantization happens inside `compute()` before calling `_compute_cached`, so it's invisible to callers and tests that check the API schema.

**L2-4. Cache size unchanged.** Keep `maxsize=128` on `_compute_cached`. With quantized keys, 128 slots now cover ~128 distinct slider positions across all concepts instead of being thrashed by unique floats. This is adequate.

## Acceptance criteria

1. A single user dragging a slider produces at most ~3 `/api/compute` requests per second (down from ~5).
2. Two sequential slider drags to the same quantized position produce exactly one `forward()` call (cache hit on the second).
3. The 502 error under multi-user slider load is eliminated or substantially reduced (the OOM chain is broken by reducing concurrent `forward()` calls).
4. FR-SO1 is preserved: a no-op recompute (sliders at baseline) still reproduces the stored headline LCOE. The existing `parity_explorer.py` gate passes.
5. No visual regression: slider drag → "Recomputing..." → headline update still works. Aborted fetches do not flash error messages.
6. The `ComputeRequest` API schema is unchanged (no breaking change for external callers or tests).

## Files touched

| File | Change |
|---|---|
| `exploration/concept_explorer/static/js/tornado.js` | L1-1: `SLIDER_DEBOUNCE_MS` 200 → 400 |
| `exploration/concept_explorer/static/js/concept_page.js` | L1-2: `AbortController` in `onSliderChange` |
| `exploration/concept_explorer/server.py` | L2-1/L2-3: quantize overrides in `compute()` before `_compute_cached` |

## Risks and mitigations

**Risk: 400ms debounce feels laggy.** Mitigation: the "Recomputing..." indicator appears immediately on slider input (before the debounce fires), so the user knows the system is responding. 400ms is a common debounce interval for search-as-you-type UIs. If it feels slow in practice, it can be tuned down to 300ms without revisiting this spec.

**Risk: 4 sig fig quantization changes LCOE output.** Mitigation: at 4 sig figs, input rounding error is <0.01%. LCOE is displayed at 2 decimal places (`$XXX.XX`). The quantization error is orders of magnitude below display precision. The parity gate (`parity_explorer.py`) validates this post-deploy.

**Risk: AbortController aborts the fetch but the server still runs `forward()`.** This is expected and acceptable. The abort prevents the client from issuing a *new* request while the old one is in flight (the debounce + abort together ensure at most one in-flight request per client). Server-side concurrency limiting is out of scope for this spec.
