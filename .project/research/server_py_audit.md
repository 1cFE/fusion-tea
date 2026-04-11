# Audit: `exploration/concept_explorer/server.py`

**Date**: 2026-03-29
**Scope**: Architecture, correctness, design quality
**Verdict**: Functional but architecturally sloppy. Reads like an AI wrote it with good intentions and poor judgment.

---

## Critical Issues

### 1. `assert` used as runtime error handling (lines 344, 414, 416)

Three `assert` statements guard runtime conditions that can actually occur:

```python
# line 344 — _s()
assert s is not None, "App state not initialised — lifespan must run first"

# line 414 — _compute_cached
assert concept is not None, f"Concept {concept_id!r} not found in loaded data"

# line 416
assert model_setup is not None, "compute called for a concept with no model_setup"
```

`assert` is **stripped by `python -O`**. If uvicorn or any deployment wrapper ever passes `-O`, these guards silently disappear: `_s()` returns `None`, every route handler gets `AttributeError`. The two in `_compute_cached` are doubly wrong — the calling `compute()` endpoint (line 435-444) already does proper `HTTPException` checks for the same conditions, making these asserts redundant guards using the wrong mechanism.

**Fix**: Replace all three with `raise RuntimeError(...)` or `raise HTTPException(...)`.

---

## Major Issues

### 2. `importlib` executes arbitrary Python from disk on every compute cache miss (lines 94-101, 418)

`_load_model_module` calls `spec.loader.exec_module(module)` — this **runs the entire model_setup.py file** including all top-level code. The path comes from a string in JSON data files.

Problems:
- **No path validation.** If data JSON is tampered, `model_setup` could point to any `.py` file on disk.
- **Module re-executed on every cache miss.** The LRU cache is on `_compute_cached` (keyed on concept_id + overrides), not on the module load. Same concept with different slider values = re-import from disk every time. This is the common case for interactive use.
- **Side effects accumulate.** `exec_module` runs all top-level statements. If a model file mutates global state, registers atexit handlers, or touches `sys.modules`, those effects pile up.
- **No error handling.** File not found? Syntax error? Runtime error in module? All become unhandled 500s with confusing stack traces.
- **Module name collision.** Every load uses `module_name="_concept_module"`. If import machinery registers these in `sys.modules`, later loads could get stale modules.

The module load should be cached independently (by path), not as a side effect of the compute result cache.

### 3. `getattr(module, "model")` / `getattr(module, "result")` with no fallback (lines 419-420)

```python
model = getattr(module, "model")
result = getattr(module, "result")
```

If the loaded module doesn't define `model` or `result`, this raises `AttributeError` — an opaque 500 with no useful error message. There's no validation that the dynamically-loaded module conforms to any expected interface.

### 4. Hardcoded parameter names coupled to external library (lines 72-83, 118-128)

`_FORWARD_NAMED` is a hand-maintained mirror of `costingfe`'s `CostModel.forward()` signature. `_forward_with_overrides` then manually extracts these as keyword arguments:

```python
model.forward(
    net_electric_mw=float(params["net_electric_mw"]),
    availability=float(params["availability"]),
    ...
    **extra,
)
```

If `costingfe` adds, removes, or renames a parameter:
- New required param: `TypeError` (missing argument)
- Removed param still in `_FORWARD_NAMED`: `TypeError` (unexpected keyword)
- Renamed param: old name flows into `**extra`, new name missing

There is no test or runtime check that `_FORWARD_NAMED` matches the actual signature. This coupling **will** silently break during library upgrades.

### 5. Mutable list as state container instead of `app.state` (lines 313, 328, 339)

```python
_state: list[_State | None] = [None]
```

This is the classic "mutable container as nonlocal workaround" trick. FastAPI has a first-class mechanism for this: `app.state`. The idiomatic approach is `app.state.data = _State(...)` in the lifespan, accessed via `request.app.state.data` in handlers or a `Depends()` callable.

The current approach forces **every route handler to be a closure** (see issue 7), which is the root cause of several downstream problems.

### 6. All routes defined as closures inside `create_app()` (lines 357-545)

Every single route handler is a nested function closing over `_s`, `_compute_cached`, `dist_dir`, etc. This is not standard FastAPI practice and has real consequences:

- **Routes are untestable in isolation.** You cannot import `get_concept` and call it. Every test requires `TestClient(create_app(...))` — all tests are integration tests.
- **No route composition.** Cannot factor taxonomy routes into a separate `APIRouter` module because they close over `_s()`.
- **IDE support degraded.** Nested functions don't appear in module-level symbols. Navigation and refactoring are harder.
- **Maintenance friction.** The file is a 575-line monolith because nothing can be extracted.

The standard patterns (dependency injection, `app.state`, `APIRouter`) exist specifically to avoid this.

### 7. In-memory `ExplorerState` — no persistence, no auth, single-user, race-prone (lines 387-396)

`POST /api/state` overwrites a single `ExplorerState` instance:
- **No persistence.** Server restart = state gone.
- **No authentication.** Bound to `0.0.0.0` (line 571), any network peer can overwrite state.
- **Single-user assumption.** One `ExplorerState` for the entire server. Two browser tabs clobber each other.
- **Race condition.** Sync handlers run in a thread pool. Two concurrent POSTs have a last-write-wins race with no locking.

### 8. Thread safety across sync handlers (lines 313, 392-396)

FastAPI runs sync route handlers in `asyncio.to_thread()` by default. This means:
- `_state[0]` reads/writes are not atomic
- `explorer_state` assignment races with concurrent reads
- `_compute_cached`'s LRU cache is thread-safe (CPython GIL), but the module loading inside it is not (`redirect_stdout` modifies `sys.stdout` globally)

The `redirect_stdout` hack (lines 98-100) is particularly bad here — it temporarily replaces `sys.stdout` for the entire process. Concurrent module loads in different threads can capture each other's output or lose output from other parts of the application.

### 9. `lru_cache` on `_compute_cached` — no eviction, no invalidation, memory leak (lines 402-405)

The cache:
- Has **no eviction tied to server lifecycle.** When `_state[0]` is set to `None` on shutdown (line 339), cached `CostModelData` objects and loaded modules persist.
- Has **no invalidation.** If data files change, cached results are stale until server restart.
- Has **no visibility.** No metrics, no logging, no way to know hit rate or memory usage.

---

## Minor Issues

### 10. `lru_cache` wrapping `dict.get()` — zero performance benefit (lines 324-326)

```python
@lru_cache(maxsize=256)
def _get_concept_cached(concept_id: str) -> ConceptData | None:
    return concepts.get(concept_id)
```

`dict.get()` is O(1) with a tiny constant. The LRU cache adds overhead (hash key, check cache dict, manage LRU linked list) that is comparable to or greater than the operation it "optimizes." With ~36 concepts, the dict lookup is already essentially free. The cache saves nothing measurable and adds a `Callable` field to `_State` instead of just using the dict directly.

The comment "skip the dict lookup after the first hit" reveals a misunderstanding — the LRU cache **is** a dict lookup.

### 11. Float precision in `frozenset` cache key (line 444)

```python
frozenset(body.overrides.items())
```

IEEE 754 floats: `0.1 + 0.2 != 0.3`. If two slider interactions produce "the same" value via different arithmetic paths, they get different cache entries. In practice, JSON parsing is deterministic, so the same slider value sent twice yields the same float. But the cache could fill with near-identical entries.

### 12. `redirect_stdout` is the wrong fix (lines 98-100)

```python
buf = StringIO()
with redirect_stdout(buf):
    spec.loader.exec_module(module)
```

- Only captures stdout, not stderr or warnings
- Not thread-safe (modifies `sys.stdout` globally)
- Silently discards output — if a module prints a diagnostic, it vanishes
- Treats the symptom (noisy output) not the cause (model files with print statements at module scope)

### 13. `0.0.0.0` bind with no security (line 571)

Default bind to all interfaces. Combined with no auth on any endpoint — including `POST /api/compute` which executes arbitrary Python via `importlib` — this exposes the full attack surface to the local network. For a dev tool this is common but worth noting.

### 14. `import json` inside function body (line 226)

`_load_taxonomy` does `import json` inside the function rather than at module top. This is a stdlib module that's already imported by Pydantic et al., so there's no laziness benefit. Just looks sloppy.

### 15. Template rendering at startup is wasteful (lines 257-293)

`_render_templates` runs on every server start, regenerating static HTML that only changes when templates change. For 4 concepts this is trivial; for 36 concepts it's unnecessary I/O on every restart. Should be a separate build step, not part of server startup.

---

## Design Smell Summary

| Pattern | What's wrong |
|---------|-------------|
| Everything-in-closures | Forces monolithic file, prevents route extraction, blocks unit testing |
| `assert` as error handling | Correctness bug waiting to happen |
| Dynamic module loading with `exec_module` | Arbitrary code execution from data-controlled path, no caching, not thread-safe |
| Hand-maintained parameter lists | Brittle coupling to external library signature |
| Single-process in-memory state | No persistence, no multi-user, no thread safety |
| LRU cache on dict lookup | Cargo-cult optimization that adds complexity for zero benefit |

## Root Cause

Most of these issues stem from a single architectural mistake: **using closures instead of FastAPI's dependency injection system.** If state lived on `app.state` and routes used `Depends()`, the file could be decomposed into modules, routes would be independently testable, and the mutable-list hack and closure gymnastics would disappear. The closure approach then cascaded into the other issues: everything had to live in one function, so the module-loading hack, the redirect_stdout hack, and the lru_cache-on-dict-get all got stuffed in there too.

The compute endpoint is the most concerning area. It loads and executes arbitrary Python files from disk, uses `assert` for error handling, hardcodes external library signatures, and wraps it all in a thread-unsafe `redirect_stdout`. This is the kind of code that works on the developer's laptop and breaks in any other context.
