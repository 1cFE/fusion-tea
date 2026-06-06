---
date: 2026-06-05T15:03:29-0700
researcher: Claude
topic: "Concept Explorer UX — user journeys and improvement ideas"
tags: [research, concept-explorer, ux, concept-analysis, lcoe]
status: complete
last_updated: 2026-06-05
---

# Research: Concept Explorer UX — User Journeys & Improvement Ideas

**Date**: 2026-06-05T15:03:29-0700
**Researcher**: Claude
**Research Type**: UX / Architecture / Data-coverage

## Research Question

Take a fresh, user-centric look at the `concept_explorer`. Two threads:

1. **Qualitative data** — what have we collected and synthesized in `concept_analysis`? What questions could a fusion researcher or enthusiast answer with it, and what UX would let them answer those questions interactively?
2. **Quantitative (LCOE) data** — the numbers are heavily asterisked (suspected issues in `model_setup.py` generation and/or underlying 1costingFE). Even so, value exists in: viewing the LCOE landscape with caveats; focusing on a family and understanding *why* values differ by tracing LCOE to input parameters and cost overrides; and using that tracing as a physics-based sanity-check / debugging surface (cf. `explorer-slider-override-semantics/spec.md`).

Write up the user journeys and UX improvement ideas. (Data staleness is explicitly out of scope — this is about UX, not numbers.)

## Summary

- **The explorer surfaces a thin slice of a deep dataset.** The `concept_analysis` pipeline produces a rich, multi-layered qualitative corpus per concept — rated data-availability, impact-ranked modeling challenges, per-subsystem TRL, supply-chain bottlenecks, a design-point block (named plant + maturity + `P_native`), an override registry with full provenance/source/rationale, archetype-fit grades, comparables, and an adversarial critic review. The explorer's extracted JSON ingests only **four** of these: `cost_model` (CAS accounts + headline + sensitivities), `parameter_metadata`, a thin `narrative` (key bets / eliminated costs / novel costs / risks), and file-path `sources`. The single richest artifact the rework produced — **the override registry with its `provenance`/`source`/`rationale` fields** — reaches the UI only as a boolean `overridden: true` star. This is the largest UX opportunity in the system, and the slider-semantics spec (FR-SO7) already independently asks for it.
- **The landing page under-sells the dataset.** ~40 concepts are presented as a flat two-bucket card grid (Approved / In Progress) with no sort, no filter, no search, and no family grouping. The one spatial/family view (the taxonomy constellation) is buried on a separate page and not discoverable from the entry point. A researcher's *first* question — "what's the landscape, and where does my concept of interest sit in it?" — has no good answer on the page built to answer it.
- **The "why is this number what it is?" journey is the explorer's real value proposition under stale data, and it's currently broken at the seam.** Sliders, tornado, and the headline number describe *three different LCOE functions* (the slider-semantics spec documents a −17.8% discontinuity on first slider touch on concept 01). For LCOE-as-debugging to work, the user must be able to trust that the curve they're dragging is the curve the hero number sits on. Fixing that seam (the spec's option (c)) is a precondition for the entire quantitative-investigation journey.
- **Family-level comparison — the user's stated highest-value quantitative journey — is under-served.** Comparison is concept-centric (pick 1–6 by hand) rather than family-centric ("show me all stellarators, ranked, with their LCOE driver decomposition side by side"). There is no "why is this one higher than its neighbors?" view that puts a concept's per-account breakdown against its *comparables* (a field we compute but the explorer never reads).
- **Maturity/confidence is expressed in ~7 different vocabularies** across the corpus (TRL, Rich/Moderate/Limited/Opaque, grounding confidence, per-parameter confidence, gap criticality, archetype-fit grade, overall readiness). The explorer collapses all of this to a single per-concept confidence badge. A researcher assessing "how much should I trust this?" needs the distinct layers, not the average.

## Detailed Findings

### The data we have vs. the data we show

**What `concept_analysis` collects** (per the qualitative inventory and `concept_analysis_brief.md`):

Each concept (`analyses/NN-name/`) carries up to four layers:

- **`analysis.md`** — frontmatter (confinement family, archetype, **archetype-fit grade** High/Med/Low/None, comparison-status, **comparables**, design-point name/maturity/`P_native`, **grounding-confidence**, review-status) plus an 8-section body: (1) Data Availability *rated* Rich/Moderate/Limited/Opaque; (2) Challenges in Capturing System Function, *impact-ranked* Critical/High/Moderate — the richest "what's weird/hard about this concept" narrative; (3) per-subsystem **TRL** with Demonstrated / On-paper / Missing-at-scale; (4) Materials & Supply Chain bottlenecks; (5) Design-Point Parameters with per-row confidence + citations; (5b) **Override Candidates** with provenance/rationale; (6) Data Gap Inventory (gap type × criticality); (7) **Family-Delta vs Comparables** — directional cost deltas vs named peers; (8) annotated sources.
- **`synthesis.md`** (9 concepts) — "What Matters Most for LCOE," **Risk Verdicts**, structural advantages/disadvantages, cross-concept positioning, "**What Would Change My Mind**," and a YAML downselect-scoring block (C1/C3/C4/C5/C8 + F1–F7 + `binary_risks` deal-breakers).
- **`critic_review_*.md`** — adversarial editorial critique (headline issues, override-discipline judgment).
- **`model_setup.py`** — the three-forward model (`generic`/`native`/`result_1gw`) and the **override registry**: each entry has `account`, `value`, `enabled`, `cost_basis`, `provenance` (direct/derived), `source` (citation), `rationale` (often a multi-paragraph derivation), and sometimes `blocked_by` (an upstream issue link). Concept 01's `C220103` magnet override carries a full FOAK→NOAK learning-curve derivation with a CFS-SPARC sanity check — `model_setup.py:53-100`.

Cross-concept tables (`tables/*.csv`): **ontology** (family/subfamily/fuel/driver-class/conversion-path), **archetype_fit** (enum + fit grade + rationale), **comparables** (derived peer sets), **design_point** (name/maturity/`P_native`/selection rationale).

**What the explorer's JSON ingests** (`models.py:344-362`, verified against `data/*.json`):

`ConceptData` = `cost_model` (17 CAS accounts + CAS22 sub-detail + headline + sensitivities) · `parameter_metadata` (display name, category, confidence, baseline, range, source, modeling_note) · `narrative` (key_bets / eliminated_costs / novel_costs / risks — populated for 37/38 concepts; only concept 01 is null) · `sources` (two file paths). Plus a separate taxonomy data layer (`taxonomy_models.py`, `seed_registry.py`, `similarity.py`) feeding `/taxonomy`.

**The gap.** Everything in `analysis.md` Sections 1, 2, 3, 4, 6, 7, the synthesis layer, the critic review, the design-point block, the archetype-fit grade, and the entire override registry *narrative* (provenance/source/rationale) is collected, version-controlled, and source-cited — and **none of it reaches the explorer UI**. The override registry reaches the front-end as exactly one bit per account: `overridden: bool` → a ★ glyph (`models.py:254`, `cas_breakdown.js:277`). The "why" is thrown away at the extractor boundary.

### Current UX surfaces (what exists today)

Four pages, three nav links (Taxonomy / All Concepts / Compare). No global search or filter.

- **`/` Landing** — card grid split into two status buckets (Approved / In Progress). Each card: thumbnail, name, family badge, ⚠ low-grounding marker, company, LCOE, confidence badge, Σ sensitivity glyph. **Only interaction is click-through.** No sort/filter/search/family-group. (`index_page.js:63-227`)
- **`/concept/{id}`** — the richest page. Sticky headline (4 stat pills with deltas + Reset), hero, collapsible Narrative / Risks / **CAS Cost Breakdown** (table + treemap, CAS22 drill-down, ★ on overrides) / **Sensitivity & What-If** (one-sided elasticity-bar grid with population whiskers + top-15 sliders + parameter-card popovers). Slider → `POST /api/compute` re-forwards the model. (`concept_page.js`, `tornado.js`, `cas_breakdown.js`, `parameter_card.js`)
- **`/compare`** — URL-driven, 1–6 concepts, Integrated (≤3, two panels) or Landscape (≤6, grid). Four views: Categorical (taxonomy attrs), Summary (5-metric bars), CapEx (17-account grouped bars), Sensitivity (grouped tornado). Inline picker; no pre-population from elsewhere. (`comparison.js` + `view_*.js`)
- **`/taxonomy`** — decision-tree sidebar · constellation scatter (MDS of similarity, the only spatial full-set view) / neighborhood graph (Cytoscape) · taxonomy-card detail. Selection tray is the one well-formed bridge into `/compare`. Dense single/double/Ctrl-click interaction model. (`taxonomy.js`, `constellation.js`, `neighborhood_graph.js`)

**Known structural awkwardness** (from the UI map):
- "Add to Comparison" on the concept page is a dead `<a href="/compare">` with no concept id — lands on an empty compare page (`concept.html.j2:119`).
- Selection state lives in three disconnected places (taxonomy tray `?selected=`, compare `?concepts=`, server `/api/state` which nothing reads back).
- Two divergent tornado implementations (concept page DOM grid top-15 w/ whiskers+sliders vs. compare Plotly top-8 no sliders).
- Compare picker shows no LCOE/confidence/⚠ — users add concepts blind to whether they even have a cost model.
- Silent degradation everywhere (missing slider range → "—" with no explanation; missing param index → whiskers vanish with a console.warn).

### The slider/tornado/headline incoherence (quantitative journey blocker)

Per `explorer-slider-override-semantics/spec.md`, three different LCOE functions are presented as one:

1. **Headline** = overrides-applied (`result_1gw.costs.lcoe`, concept 01 = 155.17 $/MWh).
2. **First slider compute** = overrides-*off* — re-forwards without the registry, collapsing concept 01 to 127.53 $/MWh (−17.8%) on a half-percent availability nudge the user didn't make.
3. **Tornado** = also overrides-off (`model.sensitivity(result.params, cost_overrides=None)`, `extract_explorer_data.py:183`).

So the slider and tornado happen to agree with each other and *both disagree with the hero number*. For the user's stated goal — "understand *why* some values look higher than others" and "use the explorer for physics-based sanity checks" — this is disqualifying: you cannot debug a number by perturbing a *different* number. The spec's recommended option (c) (a single `apply_analyst_overrides` toggle driving slider + tornado + headline in lockstep, plus a precomputed `sensitivities_applied`, plus an override-inspection affordance) is the precondition for the entire quantitative-investigation journey below — not an independent nicety.

## User Journeys

Framed from the two personas the request names: a **fusion researcher** (wants defensible, traceable comparison and to interrogate assumptions) and an **enthusiast** (wants to understand the landscape and "why is X expensive?"). Journeys are ordered roughly by how well the current tool serves them — worst-served first, since those are where the leverage is.

### J1 — "What's the landscape, and where does my concept sit?" (entry / orientation)

*Researcher or enthusiast, first visit.* They want to see the field: how many concepts, grouped how, with what spread of LCOE and maturity, and to spot their concept of interest.

**Today:** A flat two-bucket (Approved / In Progress) card grid. No sense of families, no LCOE distribution, no maturity spread, no way to find "the stellarators" or "the aneutronic ones." The constellation that *would* answer this is on `/taxonomy`, undiscoverable from here. The split that *is* shown (extraction status) is an internal pipeline-state distinction the user doesn't care about.

**Friction:** The landing page answers "which concepts has the pipeline finished?" when the user is asking "what is the space of fusion approaches and how do they compare?"

### J2 — "Why is this concept's LCOE higher than its neighbors?" (the core quantitative journey)

*Researcher, the request's headline use-case.* Pick a family (say stellarators), see how LCOE varies across its members, and trace each difference to input parameters and cost overrides — using divergence from physically-similar peers as a sanity/debugging signal.

**Today, this journey is assembled by hand and breaks at two seams:**
- There is no family-scoped landing — the user must already know which concept ids are stellarators and add them one at a time in `/compare`.
- The CapEx compare view shows per-account bars side by side (good!) but the ★-overridden accounts carry no explanation, so "this one's CAS22 is 2× its neighbor's" terminates at "…because it's overridden" with no visible *why* (the rationale is in `model_setup.py`, not the UI).
- The slider/tornado/headline incoherence (above) means the per-concept "what drives this?" decomposition is computed against the library-bare LCOE, not the headline the user is comparing.

**This is the journey the user most wants and the one with the widest gap.** The raw materials exist — comparables table, per-account `generic`/`native`/`result_1gw` decomposition (the override-effect isolation the three-forward contract was built for), override rationale — but none are wired into a "concept vs. its comparables, with the override deltas explained" view.

### J3 — "Is this number trustworthy? What's the analyst's reasoning?" (provenance / audit)

*Researcher doing due diligence.* For any LCOE, they want: what plant is this (design point)? what's the archetype fit? which accounts did the analyst override, by how much, on what evidence? what's the data-availability and TRL backdrop?

**Today:** Almost none of this is reachable in the UI. The ★ tells you an account was overridden but not to what, from what, or why. Design point, archetype-fit grade, data-availability rating, per-subsystem TRL, and the gap inventory aren't extracted. A researcher who wants to audit a number has to leave the tool and read `model_setup.py` and `analysis.md` directly — at which point the explorer added nothing to the journey.

**This is the journey the rework's whole philosophy is built to serve** ("every override is one accountable, toggleable claim") and the one the explorer most conspicuously drops.

### J4 — "How do I develop intuition for what moves LCOE?" (what-if / sensitivity)

*Enthusiast or researcher.* Drag a slider, watch LCOE respond, learn which assumptions matter.

**Today:** The mechanic exists (sliders + tornado + sticky-headline deltas) and is genuinely the explorer's most-built surface. But the first drag produces a discontinuity unrelated to the drag (J2/slider-spec), which teaches the wrong intuition and undermines trust in every subsequent drag. Once the override-semantics fix lands, this becomes the explorer's strongest journey.

### J5 — "Compare these specific concepts head-to-head" (curated comparison)

*Researcher who already knows what they want to compare.* Select N concepts, see attributes / economics / CapEx / sensitivity side by side.

**Today:** This is the best-served journey — `/compare` is capable and thoughtfully built (4 views, two layout modes, URL-shareable). The frictions are at the edges: getting concepts *into* compare (dead "Add to Comparison" button, picker shows no economics, no pre-population from concept or landing pages), and the same overridden-without-explanation gap in CapEx.

### J6 — "Explore the design space / find similar concepts" (taxonomy browsing)

*Researcher mapping the field.* Navigate families, find nearest neighbors, see what attributes concepts share/diverge on.

**Today:** `/taxonomy` serves this well in isolation (constellation, neighborhood graph, similarity, bridge nodes) but is siloed: it's the only place families and the full-set spatial view live, yet it's a separate top-nav destination disconnected from the cost story. A user exploring the taxonomy can jump to one concept's cost model but can't pull "this whole family" into a cost comparison without the manual tray dance.

## UX Improvement Ideas

Grouped by leverage. Each is annotated with the journey it serves and whether it's primarily a **data-layer** change (extractor must emit more), a **UI** change, or both. None of these depend on the LCOE numbers being correct — they improve the *scaffolding for investigating* the numbers, which is exactly what's valuable while the numbers are asterisked.

### Tier 1 — Highest leverage (unlock the journeys that are currently broken)

1. **Extract the override registry's narrative, and build an override-inspection surface.** *(J2, J3; data-layer + UI; aligns exactly with slider-spec FR-SO7.)* Emit `account`, `value`, `provenance`, `source`, `rationale`, `cost_basis`, `enabled`, `blocked_by` per override into the concept JSON. Surface it as a click/hover affordance on (a) ★-overridden CAS rows and treemap tiles, (b) ★-overridden CapEx compare bars, and (c) an "N analyst adjustments" chip on the concept page. This single change converts every ★ in the system from a dead-end marker into the entry point of the provenance journey — and it's the one piece of the dataset whose entire reason for existing (the rework's "accountable, toggleable claim") is invisible today.

2. **Resolve the slider/tornado/headline incoherence (slider-spec option (c)).** *(J2, J4; data-layer + UI.)* A single `apply_analyst_overrides` toggle (default on) that drives slider recompute, tornado source, and headline in lockstep; emit both `sensitivities_bare` and `sensitivities_applied`. This is the precondition for trusting any "why is it this number?" exploration. It also turns the toggle itself into a *teaching* surface — flip it and watch the override registry's contribution to LCOE appear/disappear, which is the cleanest possible illustration of "what is the analyst's judgment worth here?"

3. **Add a family/comparables-scoped comparison entry point.** *(J2, J6; data-layer + UI.)* Extract the ontology family/subfamily and the `comparables` set into the manifest. Then: (a) on the concept page, a "Compare with its N comparables" button that pre-populates `/compare` with the computed peer set; (b) on the landing page, family grouping/filter (below) with a "compare this whole family" action. This directly serves the request's "focus in on a particular family, look at how LCOE values vary." The comparables field is already computed deterministically — the explorer just never reads it.

### Tier 2 — Reframe the entry experience around the dataset, not the pipeline

4. **Rebuild the landing page around families and the LCOE landscape.** *(J1; UI, modest data.)* Replace the Approved/In-Progress split (pipeline-internal, user-irrelevant) with: a family-grouped or family-filterable grid, plus an at-a-glance **LCOE landscape** strip (a sorted bar or beeswarm of all concepts' headline LCOE, colored by family, with the asterisk/low-grounding markers honest and prominent). Promote the taxonomy constellation (or a simplified version) to be reachable — or embedded — from the entry page. The user's first question (J1) deserves an answer on the first page.

5. **Add sort / filter / search to the landing grid.** *(J1; UI.)* Sort by LCOE / confidence / family; filter by family, fuel (aneutronic vs DT), archetype-fit grade, has-cost-model; free-text search by name/company. The data to filter on is mostly already in the manifest or trivially addable (fuel, fit grade). ~40 cards with no find-affordance is the single most common "I can't use this" moment.

6. **Surface the "landscape with caveats" honestly and everywhere.** *(J1, J3; UI.)* The request explicitly wants "the LCOE landscape with the appropriate caveats." Make the asterisk/low-grounding/archetype-fit-None status a first-class, consistent visual treatment (not a quiet ⚠), with a one-line plain explanation on hover ("company-stated single-source number" / "archetype fit Low — costed against an imperfect library analogue"). This lets the tool show the landscape *and* be trustworthy about its own uncertainty — which, under known-stale data, is the difference between "misleading" and "useful with eyes open."

### Tier 3 — Deepen the provenance/maturity story

7. **Extract and surface the design-point block.** *(J3; data-layer + UI.)* "What plant did we model?" should have a one-sentence answer on the concept page: design name, maturity tier, `P_native`, primary source. The rework makes this a first-class concept; the explorer should make it the first thing you read under the hero. (It also frames every parameter on the page — the three-forward contract guarantees they all describe this one named unit.)

8. **Replace the single confidence badge with a layered maturity panel.** *(J3; data-layer + UI.)* The corpus expresses maturity in ~7 vocabularies; collapsing them to one badge destroys the signal a researcher needs. A compact panel: data-availability rating, grounding confidence, archetype-fit grade, and (if extracted) the least-mature key subsystem TRL. Each is a distinct question ("is the data there?" vs "does the cost model's archetype fit?" vs "is the physics demonstrated?") and a researcher assessing trust needs them separated.

9. **Wire the per-account override decomposition into the CAS breakdown.** *(J2, J3; data-layer + UI.)* The three-forward contract gives `generic` (library-bare), `native` (overrides on), and `result_1gw` per account. For any overridden account, show the user the *delta*: "library says X, analyst says Y, because [rationale]." This is the literal mechanism the request asks for — "trace/correlate [LCOE] with input parameters and/or cost overrides… understand *why* some values look higher." The data exists in the module; only `result_1gw` is currently extracted.

### Tier 4 — Connective tissue (fix the disconnected-state friction)

10. **Make selection continuous across pages.** *(J5, J6; UI.)* Fix the dead "Add to Comparison" button (carry the concept id); let landing cards and concept pages add to a shared selection that flows into `/compare`; either read `/api/state` back into the UI or drop it. Today a user assembles a comparison by re-finding concepts they were just looking at.

11. **Enrich the compare picker with economics.** *(J5; UI.)* Show LCOE / confidence / has-cost-model / ⚠ in the picker so users don't add cost-model-less concepts blind (the Taxonomy tray already warns; the compare picker doesn't).

12. **Unify the two tornado implementations** *(J4, J5; UI, lower priority.)* so a parameter's sensitivity looks and behaves the same whether viewed on one concept or across several.

## Code References

- `exploration/concept_explorer/models.py:344-362` — `ConceptData` payload: the exact (thin) set of fields the explorer ingests.
- `exploration/concept_explorer/models.py:82-187` — `CostModelData` / CAS account structure; `overridden: bool` is the only override signal (`models.py:254`).
- `exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py:43-130` — override registry with full `provenance`/`source`/`rationale`/`cost_basis`/`blocked_by` — the rich data discarded at extraction.
- `exploration/concept_explorer/extract_explorer_data.py:183` — tornado built `cost_overrides=None` (library-bare), the root of the tornado↔headline mismatch.
- `exploration/concept_explorer/server.py:561-612` — `/api/compute`; `_forward_with_overrides` drops the registry on recompute.
- `exploration/concept_explorer/static/js/index_page.js:215-227` — landing page two-bucket status split (the pipeline-internal framing to replace).
- `exploration/concept_explorer/static/js/cas_breakdown.js:277` — where ★ overridden is rendered with no "why."
- `exploration/concept_explorer/templates/concept.html.j2:118-120` — dead "Add to Comparison" button.
- `exploration/concept_analysis/tables/{ontology,archetype_fit,comparables,design_point}.csv` — cross-concept fields computed but never read by the explorer.
- `.project/active/explorer-slider-override-semantics/spec.md` — the data-layer fix (option (c)) that Tier-1 items 1–2 build on.
- `.project/concepts/concept-analysis-rework-design.md:160-188` — the preserved `concept_explorer` contract (`model`/`generic`/`native`/`result_1gw` at module level) the per-account decomposition (idea 9) would consume.

## Architecture Insights

- **The extractor is the bottleneck, not the UI.** Most of the high-leverage ideas (override narrative, design point, archetype-fit, comparables, per-account decomposition, layered maturity) are gated on `extract_explorer_data.py` emitting fields it currently drops, not on front-end capability. The front-end is, if anything, *over*-built relative to the data it's fed (two tornado implementations, a whole taxonomy sub-app) — the imbalance is collected-but-unsurfaced data, not missing widgets.
- **The three-forward contract was designed for exactly this.** `generic`/`native`/`result_1gw` being module-level importable (`concept-analysis-rework-design.md:160`) exists *specifically* to let the explorer show the override-effect decomposition (idea 9). The contract is already paid for; the explorer just hasn't drawn on it.
- **The rework's philosophy and the explorer's current behavior are in direct tension.** The rework's thesis is "make analyst judgment auditable per-entry instead of buried in code." The explorer currently re-buries it: it throws away the registry narrative and (via the slider seam) silently discards the overrides on first interaction. Tier-1 items 1–2 are not feature additions so much as *making the explorer honor the contract the rest of the pipeline was rebuilt to provide.*
- **"Stale data" is not a blocker for any of this** — and is arguably an argument *for* it. Under known-wrong numbers, a landscape view that's honest about caveats (idea 6), a provenance trail that shows the analyst's reasoning (idea 1), and a per-account "library vs analyst, here's why" decomposition (idea 9) are precisely the surfaces that turn the explorer into the physics-sanity-check / debugging instrument the request envisions. The numbers being suspect makes *traceability* the product, and traceability is exactly the layer the explorer currently omits.

## Feasibility Assessment

- **Tier-1 item 2** (slider semantics) is already spec'd in `explorer-slider-override-semantics/spec.md` with options analyzed and option (c) recommended; LOW–MEDIUM lift, mostly settled. It should land first because items 1 and 9 share its data-layer plumbing (reading the registry at extract/compute time).
- **Tier-1 item 1** (override narrative surface) is a data-layer addition (extend the extracted schema with the registry fields — they're already evaluated in `model_setup.py` and partially read via `_load_model_module`) plus a UI affordance. MEDIUM. Highest value-to-effort ratio in the system.
- **Tier-1 item 3 & Tier-2/3 extraction items** are mostly "read a CSV column / a markdown frontmatter field into the JSON" — LOW each, though there are several. The work is breadth (many small fields) not depth.
- **Tier-2 landing redesign** is the largest pure-UI lift but needs no new data beyond family/fuel/fit-grade in the manifest.
- **Risk:** the corpus coverage is uneven (32 full `analysis.md`, 9 synthesis, several review-only). Any surface that promises a field must degrade honestly when it's absent for a given concept — the explorer's existing "silent degradation" habit (whiskers vanish, sliders show "—") is the *wrong* pattern to copy here; missing provenance/maturity should say so, not disappear.

## Recommendations

1. **Sequence:** land slider-semantics option (c) (item 2) → override-narrative extraction + inspection surface (item 1) → per-account decomposition (item 9) → family/comparables entry (item 3). These four, in order, build the J2+J3 "why is this number what it is, and can I trust it?" spine that is the explorer's real value under stale data. They share plumbing, so doing them as one arc is cheaper than scattered.
2. **In parallel**, the landing-page reframe (items 4–6) is independent and serves J1 — the orientation journey that every user hits first. It needs only manifest enrichment, no per-concept extraction.
3. **Treat "honest about uncertainty" as a cross-cutting requirement**, not a feature: every surface that shows a number or a field should make its caveat/coverage status visible (idea 6 generalized). This is the single design principle that makes a known-stale dataset *useful* rather than *misleading*, and it's the through-line connecting the request's "appropriate caveats," "physics-based sanity checks," and "debugging" framings.
4. **Resist adding more widgets to the front-end** until the extractor is feeding the ones that exist. The diagnosis is an under-fed UI, not an under-built one.

## Open Questions

- **Scope of provenance surfacing:** does the override-inspection view show *disabled* overrides too (the rework's `enabled: false` entries with `blocked_by` links)? They're arguably the most interesting for debugging ("here's a departure we *would* make but an upstream bug blocks") but the slider-spec scopes them out of v1. Worth a decision.
- **Landing-page family taxonomy source:** the explorer has two family notions — `ConfinementFamily` enum on `ConceptData` (MFE/IFE/MIF/NONSTANDARD; note concept 01 ARC is `NONSTANDARD`) and the richer ontology subfamily/archetype in `tables/`. Which drives landing-page grouping? They don't fully agree.
- **How much synthesis-layer content to surface:** the `synthesis.md` "What Would Change My Mind" and risk-verdict content is high-value for J3 but exists for only 9 concepts. Surface it where present (degrading honestly), or defer until coverage is broader?
- **Per-concept vs session-global toggle/selection state:** the slider-spec recommends per-concept override toggle state; the cross-page selection continuity (item 10) implies session-global selection. Confirm these two don't collide in `ExplorerState`.
