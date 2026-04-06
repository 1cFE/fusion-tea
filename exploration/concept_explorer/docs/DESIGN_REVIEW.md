# Design Review

## Dimensional Assessment

### 1. Concept Compliance
**Assessment:** Concerns

**Coverage mapping:**

| Success Criterion / User Story | Design Coverage | Gap? |
|---|---|---|
| SC-1: Identity at a glance | `concept.html.j2` layout covers this well | No |
| SC-2: Sensitivity with context | Tornado chart + parameter detail cards | No |
| SC-3: Comparisons that teach | `compare.html.j2` + comparison.js | No |
| SC-4: Trust through traceability | Color/opacity encoding in §6.2 | No |
| SC-5: Fluid navigation | No page reload needed — API-driven | No |
| US-1: First encounter (illustration slot) | Mentioned in layout but **no mechanism for providing/serving illustrations** | **Yes** |
| US-3: Economic thesis (key bets, eliminated/novel costs) | `NarrativeData` + layout section "Key Bets & Differentiators" | No |
| US-7: Interactive what-if (sliders) | `/api/compute` + slider JS | No |
| US-12: Agent integration | `GET /api/state` + filesystem access | No |
| US-14: Following threads (parameter across concepts) | **No design element addresses this** | **Yes** |

**Findings:**

1. **US-14 ("Following threads") is unaddressed.** The concept says "I can quickly see which other concepts also have sensitivity to that parameter." The design has no cross-concept parameter index, no parameter search, and no way to navigate from a parameter in one concept to the same parameter in others. The comparison view lets you compare *selected* concepts, but there's no discovery mechanism for "which concepts share sensitivity to HTS magnet cost?"

2. **US-1 illustration slot is architecturally hollow.** The concept layout shows `[illustration slot]` but the design provides no mechanism for associating images with concepts — no `illustration` field in `ConceptData`, no path in `SourcePaths`, no image serving route. The concept's Open Question 2 acknowledges this, but the design should at minimum define the data model field even if the content strategy is deferred.

3. **"Compare by default" principle (§6.1) has no single-concept-view implementation.** The principle says "showing where a value sits relative to the population of analyzed concepts, even in single-concept view." The single concept profile shows only its own data — no population context marks on the tornado chart or CAS breakdown showing where this concept sits relative to others.

**Recommendations:**
- Add a `GET /api/parameters/{param_name}` endpoint that returns which concepts have sensitivity to a given parameter, with elasticity values. Wire into tornado chart click handler.
- Add `illustration: str | None = None` to `ConceptData` and a corresponding directory in static/images/concepts/.
- For "compare by default": on the tornado chart, show small tick marks or a whisker range indicating the population distribution of each parameter's elasticity.

---

### 2. Abstraction Quality
**Assessment:** Pass

The abstraction hierarchy is clean: `ConceptData` → `CostModelData` / `NarrativeData` / `ParameterMetadata`. The split between pipeline (extraction) → server (serving + computation) → frontend (visualization) is clear. Component responsibilities are well-separated (each JS module owns one chart type).

**One concern:** The `ExplorerState` model (referenced in the `/api/state` endpoint) is **never defined**. The server claims to return it, but there's no Pydantic model showing what fields it contains. This is a gap, not an abstraction problem, but it means the agent integration surface is undefined.

**Recommendation:** Define `ExplorerState` in models.py with fields like `current_concept_id`, `slider_overrides`, `comparison_set`.

---

### 3. Duplication Avoidance
**Assessment:** Concerns

**Findings:**

1. **Dual data delivery: inlined JSON vs. API fetch.** The design contradicts itself. §3.6 (`concept.html.j2`) shows `const CONCEPT_DATA = {{ concept_json | tojson }};` — data inlined into HTML by Jinja2. But the sentence immediately after says "data is loaded via `fetch('/api/concepts/{id}')` rather than embedded in `<script>` tags." The comparison page similarly shows both `CONCEPT_DATA_STORE` embedded and lazy fetch. **Which is it?** This ambiguity will create confusion during implementation.

2. **`build_explorer.py` vs. `server.py` as data sources.** The build script generates `data/*.json` files AND renders HTML. The server serves the same data via API. The build script's HTML embeds data; the server's API serves it dynamically. This is two delivery mechanisms for the same data. If the server is primary, the build step for HTML is only needed for CI/archival — but the design treats both as first-class without clarifying when to use which.

3. **Manifest vs. concept list endpoint.** `GET /api/manifest` returns `ConceptManifest` and `GET /api/concepts` returns `list[ConceptManifestEntry]`. These serve nearly identical purposes with slightly different shapes. The manifest has `generated_at` and a `concepts` list; the concepts endpoint returns the list directly.

**Recommendations:**
- **Resolve the data delivery question definitively.** If the server is primary: HTML pages are shells that fetch data via API. If build-only mode needs to work offline: inline the JSON. Don't do both — pick one and document the other as a fallback mode.
- Remove `GET /api/concepts` (the list endpoint) — the manifest already serves that purpose.

---

### 4. Data Structure Clarity
**Assessment:** Pass

The Pydantic models are well-defined with explicit types. The mapping from `ForwardResult` → `CostModelData` is clearly documented. The `ParameterMetadata` schema is concrete.

**Minor issues:**

1. **`SensitivityEntry` only has `elasticity` and `baseline`** but the tornado chart JS API (§5.4) expects `{ elasticity, baseline, unit }`. The `unit` field is in `ParameterMetadata`, not `SensitivityEntry` — this works but means the frontend must join two data structures. This is fine but should be noted.

2. **`CostModelData.params` is `dict[str, float]`** — an untyped bag. This is acknowledged and justified (1costingfe returns it this way), but it means slider bounds, display names, and units all come from `ParameterMetadata`, which must be complete for every key in `params`. There's no validation that `parameter_metadata.keys() ⊇ sensitivities.engineering.keys() ∪ sensitivities.financial.keys()`.

**Recommendation:** Add a `model_validator` on `ConceptData` that checks parameter_metadata covers all sensitivity keys when `has_cost_model` is True.

---

### 5. Interface Completeness
**Assessment:** Concerns

**Findings:**

1. **`POST /api/compute` request/response for sensitivity recomputation is ambiguous.** The endpoint returns `CostModelData`, which includes `sensitivities: SensitivityAnalysis`. But the caching TODO asks "consider only recomputing LCOE on slider change and leaving the sensitivity ranking from pre-computed data." If the response always includes full sensitivities, clients assume re-ranking. If not, the response type is wrong. **The contract is unclear.**

2. **`GET /api/state` endpoint body is undefined.** No `ExplorerState` model. The design says "Server maintains in-memory state" and "frontend POST calls on navigation and slider changes" but there's no `POST /api/state` endpoint defined, and no mechanism for the frontend to report its state to the server.

3. **No `GET /api/health` endpoint defined**, yet the frontend JS (§5.2) calls `fetch('/api/health')` to detect server availability.

4. **HTML page routing is unspecified.** The server mounts `/static` for assets, but how does `http://localhost:8421/concept/01-hts-compact-tokamak` serve `dist/concept/01-hts-compact-tokamak.html`? The "catch-all route" is mentioned in a comment but not defined.

5. **Error responses not specified.** What does the API return when a concept_id doesn't exist? When a standalone concept gets a `/api/compute` request (422 is mentioned but not formalized)?

**Recommendations:**
- Define `ExplorerState` model and add `POST /api/state/update` for frontend to push navigation state.
- Add `GET /api/health` to the endpoint list.
- Specify the HTML serving strategy (e.g., `@app.get("/{path:path}")` catch-all serving from dist/).
- Add error response models to the API spec.

---

### 6. Implementability
**Assessment:** Concerns

**Findings:**

1. **The `from_forward_result()` classmethod is critical-path and unimplemented.** Listed as TODO T1. Every costingfe concept depends on it. The design describes what it should do but doesn't address edge cases: What happens when `ForwardResult.plasma_state` is not None? Does it need to be serialized? What about `cas22_detail` keys — are they always strings like `"C220101"` or sometimes bare integers?

2. **Standalone concept refactoring is underspecified.** The design says standalone scripts "need refactoring to implement `to_explorer_dict()`" and "this is acceptable: we own these scripts and there are only 2." But the sonofusion script is ~800-1000 lines with a custom `SonofusionPlantParams` dataclass. Implementing `to_explorer_dict()` means mapping every CAS calculation back to a `CASAccount` dict, computing headline economics, and producing sensitivity data. This is a significant refactoring effort — not a trivial wrapper. **The design undersells this.**

3. **Sensitivity data for standalone concepts doesn't exist.** Costingfe concepts get `model.sensitivity()` via JAX autodiff. Standalone concepts compute CAS costs via hand-coded math — there's no autodiff, no sensitivity method. The design doesn't address how standalone concepts get `SensitivityAnalysis` data. Either:
   - Standalone concepts ship without sensitivity data (tornado chart empty — bad UX)
   - Standalone concepts implement finite-difference sensitivity (significant new code)
   - Standalone concepts are migrated to costingfe (the real solution, but out of scope)

   **This is a blocking gap for 2 of 8 concepts.**

4. **LLM narrative extraction depends on prompt design (TODO T2) which is on the critical path for C1.** Without the prompt, you can't extract narrative data, and without narrative data the concept profile is incomplete (no thesis, no key bets, no risks). The design defers this but it gates E1.

5. **The `model_metadata.yaml` authoring pipeline (C2) is a substantial content effort.** 8 concepts × ~30 parameters each = ~240 parameter metadata entries. Each needs display_name, category, confidence, range, source, and modeling_note. The design says "LLM-generated draft, human reviews" but doesn't estimate the human review effort or define the LLM prompt for draft generation.

6. **Phase dependency: P2 requires pipeline changes.** Adding `model_output.json` to the pipeline means modifying `run_analysis.py` to add a new stage or modify the model-setup stage. The design references this but the pipeline modification isn't scoped — it's treated as a prerequisite but the effort to implement it is unaddressed.

**Recommendations:**
- Explicitly scope the standalone concept problem: either (a) declare standalone concepts get reduced tornado charts (no sensitivity), or (b) add a finite-difference sensitivity utility, or (c) put standalone migration on the critical path.
- Write the `from_forward_result()` implementation in the design (it's the bridge between systems and deserves pseudocode, not just a TODO).
- Acknowledge that C2 (metadata authoring) is the largest content effort and estimate scope.

---

## Issues by Severity

### Critical (Must address before implementation)

1. **Standalone concept sensitivity data gap**: 2 of 8 concepts have no mechanism to produce `SensitivityAnalysis`. The design promises tornado charts for all cost-model concepts but doesn't address how standalone concepts get elasticity data. — Dimension 6

2. **Data delivery contradiction**: The design simultaneously specifies Jinja2-inlined JSON and API-fetched data for the same pages. Implementers will make inconsistent choices. — Dimension 3

### Major (Should address)

3. **US-14 (parameter thread following) unaddressed**: A named user story in the concept has no corresponding design element. — Dimension 1

4. **`ExplorerState` model undefined**: The agent integration endpoint (`GET /api/state`) returns an undefined type, and there's no mechanism for the frontend to report state to the server. — Dimension 5

5. **`from_forward_result()` needs design, not just a TODO**: This classmethod is the bridge between 1costingfe and the explorer. It deserves pseudocode covering CAS mapping, overridden flags, cas22_detail handling, and PowerTable → HeadlineEconomics mapping. — Dimension 6

6. **Standalone `to_explorer_dict()` effort undersold**: The sonofusion and dipole scripts are 600-1000 lines of custom physics. Refactoring them to produce a standardized dict is a non-trivial work item, not a parenthetical. — Dimension 6

### Minor (Consider addressing)

7. **No illustration data model field**: `ConceptData` has no `illustration` field despite the concept layout showing an illustration slot. — Dimension 1

8. **"Compare by default" principle not implemented in single-concept view**: The design principle says values should show population context even in solo view, but no design element implements this. — Dimension 1

9. **`GET /api/concepts` duplicates manifest data**: Two endpoints serving near-identical data. — Dimension 3

10. **No `GET /api/health` in API spec**: Frontend code references it but it's not in the endpoint list. — Dimension 5

11. **Missing parameter_metadata coverage validation**: No check that metadata keys cover all sensitivity keys. — Dimension 4

12. **HTML routing unspecified**: How the server maps URL paths to dist/ HTML files. — Dimension 5

---

## Specific Recommendations

1. **Resolve standalone sensitivity immediately.** Add a section to §4 that either (a) defines a `finite_difference_sensitivity(params_dataclass, cost_fn)` utility that standalone scripts can use, or (b) explicitly states standalone concepts ship with `sensitivities=None` and the tornado chart shows a "no sensitivity data" placeholder. Option (b) is honest and ships faster.

2. **Pick one data delivery model.** Recommendation: server-primary. HTML pages are shells; all data comes via `fetch()`. The build script produces `data/*.json` and static HTML shells. The `--serve` flag on `build_explorer.py` is redundant with `server.py` — remove it or make it a convenience wrapper.

3. **Define `ExplorerState` and the state-reporting protocol.** Add to models.py:
   ```python
   class ExplorerState(BaseModel):
       current_concept_id: str | None = None
       slider_overrides: dict[str, float] = {}
       comparison_set: list[str] = []
       timestamp: str  # ISO 8601
   ```
   Add `POST /api/state` for frontend to push state on navigation and slider changes.

4. **Add a cross-concept parameter index for US-14.** Either a `GET /api/parameters/{name}` endpoint or a static `parameter_index.json` built during extraction that maps parameter names → list of (concept_id, elasticity) tuples.

5. **Write `from_forward_result()` pseudocode in the design.** The CAS field mapping (e.g., `result.costs.cas10` → `CASAccount(name="Preconstruction", cost_m_usd=result.costs.cas10, overridden="cas10" in result.overridden)`) is straightforward but there are ~20 fields to map. Making this explicit prevents implementation mistakes.

6. **Scope the metadata authoring effort (C2) honestly.** Consider: for Layer 1, only 1-2 concepts need metadata. Defer the full 8-concept sweep to Layer 2. This de-risks the critical path.

---

**Overall:** **Revise**

The data model and component architecture are solid. The main issues are: (1) a blocking gap for standalone concept sensitivity data, (2) a self-contradiction in data delivery strategy, and (3) several undefined interfaces that will cause implementation friction. None of these require a rethink of the architecture — they're gaps and ambiguities that can be resolved with targeted additions to the existing design.
