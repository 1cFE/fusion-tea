# Spec: Cost Landscape Page (Theme F)

**Status:** Implementation Complete (all 5 phases; cas71/72 re-extract held per user — see plan Phase 1/FR-F11)
**Owner:** Reid W
**Created:** 2026-06-07 13:28 PDT
**Complexity:** MEDIUM
**Branch:** `feat/explorer-cost-landscape` (off `feat/explorer-ontology-matrix` / PR #59, per the epic's branching convention)

---

## Work Item Summary

A new dedicated explorer page — **Cost landscape** — that presents every costed concept's LCOE as a stacked bar chart, with each bar broken into the cost components that *make up* that LCOE: Capital, Fixed-O&M, Replacement, and Fuel. Concepts can be re-grouped live by ontology facet (family, fuel, driver, energy capture, operation mode) and are always sorted cheapest-first within each group. Hovering a segment reveals its $/MWh contribution, its share of the total, and the analyst's source/override notes; clicking a bar opens that concept's page. This is the J2 journey ("why is this concept's LCOE higher than its neighbors?") made into a single, honest, comparison-first surface — the place a user goes *on purpose* to ask the cost question.

## Why This Matters Now

The explorer has a per-concept cost story (the concept page's CAS breakdown + the Phase-1 override spine) but **no cross-concept cost comparison** — to compare LCOE you must hand-pick concepts into `/compare`, and even then nothing shows *what drives the differences*. The data to do better already exists: the annualized cost components that sum to LCOE are in (or one small extractor change away from) the served JSON. The landing reframe (Theme B1) deliberately demoted economics on the *home* page; this page is its complement — the destination where leading with cost is correct, because the user arrived asking the cost question. It also turns the continuous-vs-pulsed difference (which lives in the Replacement + Fuel components, not in capacity factor) into something you can actually see.

## Key Bets / Constraints

- **Bet:** The single most useful cost view is the **LCOE numerator breakout** — the annualized buckets (Capital/Fixed-O&M/Replacement/Fuel) that are exactly additive to the headline LCOE. One honest chart beats a metric switcher for v1.
- **Bet:** Because the explorer standardizes every concept to a 1 GWe plant at ~0.85 availability (`result_1gw`), the LCOE *denominator* is nearly constant across concepts — so LCOE differences are a **cost-composition story**, and a stacked bar of the cost numerator tells essentially the whole story. (See Appendix B for the data check that killed the availability-scatter idea.)
- **Constraint:** Segments MUST be the *annualized* components in $/MWh that sum to the headline LCOE. The CapEx-by-CAS-account breakdown is a different unit (M$, capital-only) and MUST NOT be stacked on this axis — it is a deferred separate view, not part of this bar.
- **Constraint:** Reuse Theme A's identity/caveat authorities (`conceptLabel()`, `caveatMarker()`) and Theme A2's facet/color vocabulary (`ontologyPalette`, `facetModel`) and the matrix's grouping-control idiom — this is UI wiring over existing authorities, not a new vocabulary.
- **Non-goal:** No metric toggle (CapEx / OpEx / Production as separate views), no scatter, no registry editing, no comparables pre-population (that is C2). Those are explicitly deferred.

---

## Business Goals

### Why This Matters

A fusion researcher's stated highest-value quantitative journey is "focus on a family, see how LCOE varies across its members, and trace each difference to its drivers." Today that journey is assembled by hand and breaks at every seam. This page answers it directly: pick a grouping, read the field cheapest-to-most-expensive, and see at a glance whether a concept is expensive because of capital, O&M, replacement, or fuel — with the analyst's reasoning one hover away. Under known-stale LCOE numbers, this kind of *traceable, caveat-forward* comparison is the product.

### Success Criteria

- [ ] A user can open one page and see all costed concepts' LCOE side by side, decomposed into Capital / Fixed-O&M / Replacement / Fuel, without hand-picking anything.
- [ ] A user can re-group the field by family/fuel/driver/energy-capture/operation-mode and, within each group, immediately read concepts cheapest-first.
- [ ] For any segment, a user can see its $/MWh contribution, its % of that concept's LCOE, and the analyst's source/override note — and jump to the concept page for the full story.
- [ ] The continuous-vs-pulsed difference is legible: pulsed (IFE/MIF) concepts visibly carry Replacement and Fuel (target) segments that steady-state concepts do not.
- [ ] Missing/stale/not-recorded data is marked honestly, never silently dropped.

### Priority

P1. The agreed next build in the Explorer UX v3 epic (Theme F). Branches off the unmerged B1 matrix (#59) per the epic's branching convention.

---

## Problem Statement

### Current State

- The explorer has no cross-concept cost-comparison surface. `/compare` requires hand-picking and shows CapEx bars without the *why*; the concept page shows one concept at a time.
- The top nav is the legacy three-link set (Taxonomy / All Concepts / Compare); "Taxonomy" no longer has a unique job now that the matrix (All Concepts) is the better raw taxonomy view.
- The served concept JSON already carries the LCOE headline and the `cas90`, `cas70`, `cas80` annualized components — but **only the combined `cas70`**, not the `cas71`/`cas72` split needed for the Fixed-O&M-vs-Replacement breakout.

### Desired Outcome

A dedicated Cost landscape page, 4th in a reordered top nav, presenting the LCOE-numerator stacked-bar comparison described above, fed by an extractor that emits the CAS71/72 split.

---

## Scope

### In Scope

- **New page + route** "Cost landscape", registered as the 4th top-nav destination, after Compare.
- **Nav reorder + rename** (rides with this item): All Concepts (far-left) · Design Space Viz (renamed from Taxonomy) · Compare · Cost landscape.
- **The stacked-bar chart (Plot 1)**: one bar per costed concept; height = headline LCOE ($/MWh); segments = Capital (CAS90) / Fixed-O&M (CAS71) / Replacement (CAS72) / Fuel (CAS80), each as its $/MWh contribution, summing to the headline LCOE.
- **X-axis identity**: concept # code (A1) with the A3 caveat marker adjacent; hover → canonical `Name (Fuel)`.
- **Grouping control**: `[no grouping]`, Family (tree), Fuel, Driver, Energy Capture, Operation Mode; re-group live with no refetch; reuse the matrix control idiom + Theme A2 facets/colors.
- **Sort**: always LCOE ascending within each group (fixed, not user-configurable).
- **Segment hover**: $/MWh contribution, % of the bar's LCOE, and source/override notes (from the Item 2 override records already in the payload).
- **Bar → concept page** link.
- **Extractor change**: emit `cas71` and `cas72` into the concept cost-model JSON; re-extract the served concepts.
- **Honest degradation** throughout: only costed concepts appear; missing/not-recorded fields say so.

### Out of Scope

- Metric toggle / alternate views: **CapEx-by-CAS-account** (different unit), **OpEx-only**, **Production/utilization** — deferred. (CapEx-by-account is a plausible *future* metric view; not this item.)
- The **availability scatter** (Plot 2) — dropped; the dataset's denominator is standardized, so its axes don't vary (Appendix B).
- A page-level **bare/applied (`apply_analyst_overrides`) toggle** — v1 uses the served headline (applied) values; respecting the Phase-1 toggle here is a design question, leaning out for v1.
- **C2** comparables pre-population, **registry editing**, and any change to how LCOE itself is computed in costingFE.
- Changing `default_availability` to differentiate pulsed vs continuous — a costingFE modeling decision, noted but out of scope.

### Edge Cases & Considerations

- **Concepts that break the 1 GWe normalization**: e.g. 35 is a genuine 84 MW plant; 02/03 show data inconsistencies (Appendix B). Decide per-concept: show with a caveat marker or omit. The page must not silently misrepresent them.
- **Extreme-LCOE concepts** (16 ≈ 2068, 03 ≈ 37,452 $/MWh) dominate a linear axis and crush everyone else. Axis treatment (clip/flag/log/exclude-freeform) is a design question.
- **Override-note granularity**: the Capital segment aggregates many CAS-account overrides; the per-segment tooltip must summarize/roll these up honestly rather than imply a single override.
- **Concepts missing the 71/72 split** after extraction (37 & 39 are blocked by concept-side bugs — Item 2-FU): show the combined O&M honestly rather than fabricating a split.
- **Stale headline values** (e.g. the FU2 `data/24.json` issue): the page reads stored headlines; it inherits whatever the extractor wrote. Not this item's job to fix, but worth a caveat-marker tie-in.

---

## Requirement Selection Notes

The normative requirements below fix what we settled in discussion: the chart's identity (LCOE numerator breakout), the axis/identity/grouping/sort behavior, the why-affordances, the one extractor change, and honest degradation. Deliberately left to design: the exact decomposition computation and where it runs, axis scaling for outliers, segment color tokens, tooltip roll-up mechanics, whether the grouping control is physically shared with the matrix, and the bare/applied question. Those are mechanism, not contract.

---

## Requirements

### Functional Requirements

> From the user's request and our settled discussion unless marked [INFERRED].

1. **FR-F1**: The explorer SHALL provide a new dedicated page, "Cost landscape", reachable from the top nav as the **4th destination, after Compare**.
2. **FR-F2**: The top nav SHALL be ordered, left → right: **All Concepts · Design Space Viz · Compare · Cost landscape**, with the former "Taxonomy" link relabeled **"Design Space Viz"**. (Label/order only; the constellation page's deeper refocus is Theme C1.)
3. **FR-F3**: The page SHALL render **one stacked bar per costed concept**, where bar height equals that concept's headline LCOE in $/MWh.
4. **FR-F4**: Each bar SHALL be segmented into the LCOE **numerator breakout** — **Capital (CAS90), Fixed-O&M (CAS71), Replacement (CAS72), Fuel (CAS80)** — each segment expressed as its $/MWh contribution, and the segments SHALL sum to the headline LCOE. The bar MUST NOT mix in capital-cost-by-account (M$) values.
5. **FR-F5**: The x-axis SHALL identify each concept by its **# code** (Theme A1) with the **A3 caveat marker** rendered adjacent; hovering the axis label SHALL reveal the canonical `Name (Fuel)`.
6. **FR-F6**: The page SHALL let the user **re-group** concepts among `[no grouping]`, **Family (tree)**, **Fuel**, **Driver**, **Energy Capture**, **Operation Mode**, applied live without refetching, rendered through Theme A2's facet/color vocabulary.
7. **FR-F7**: Within every group, bars SHALL **always be sorted by LCOE ascending** (cheapest first). Sort SHALL NOT be user-configurable; grouping is the only variable.
8. **FR-F8**: Hovering a segment SHALL show its **$/MWh contribution**, its **% of the bar's LCOE**, and the **source/override notes** for that cost component, drawn from the override records already in the concept payload.
9. **FR-F9**: Each bar SHALL **link to its concept page**.
10. **FR-F10**: Only concepts with a cost model SHALL appear; any concept or segment with missing/not-recorded data SHALL **say so** (caveat marker or explicit "not recorded") and SHALL NOT silently vanish.
11. **FR-F11**: The extractor SHALL emit the **`cas71` and `cas72` split** into each concept's cost-model JSON (today only combined `cas70` is served), and the served concepts SHALL be re-extracted so the breakout is available.

### Non-Functional Requirements

- **NFR-1**: The page SHALL preload all data it needs with the concept payloads (as B1 does) and SHALL NOT fetch per render or per re-group.
- **NFR-2**: No measurable latency regression versus existing explorer pages.

---

## Acceptance Criteria

### Core Functionality

- [ ] The Cost landscape page exists, is the 4th nav item after Compare, and the nav reads All Concepts · Design Space Viz · Compare · Cost landscape (FR-F1, FR-F2).
- [ ] Every costed concept appears as a stacked bar whose height = its headline LCOE and whose Capital/Fixed-O&M/Replacement/Fuel segments sum to that LCOE (verify against ≥3 concepts spanning tiers, e.g. 01, 24, 23) (FR-F3, FR-F4).
- [ ] Re-grouping by each of the 6 options re-lays the bars live with no network refetch; within each group bars run cheapest-first (FR-F6, FR-F7, NFR-1).
- [ ] x-axis shows # code + caveat marker; hover yields the canonical name; a pulsed IFE concept (e.g. 17a/17b) visibly shows Replacement + Fuel segments a tokamak (01) lacks (FR-F5, FR-F4 narrative).
- [ ] Segment hover shows contribution + % + source/override note; clicking a bar lands on the right concept page (FR-F8, FR-F9).
- [ ] A concept missing the 71/72 split (e.g. 37) or with not-recorded notes degrades honestly (FR-F10).
- [ ] `cas71`/`cas72` present in the re-extracted served JSON (FR-F11).

### Quality & Integration

- [ ] Existing tests continue to pass.
- [ ] New coverage that the emitted Capital/Fixed-O&M/Replacement/Fuel components sum to the stored headline LCOE for a sample concept (the decomposition is exact, not approximate).

---

## Next-Stage Handoff

**Settled in this spec:**
- The chart is the LCOE numerator breakout (Capital/Fixed-O&M/Replacement/Fuel, $/MWh, additive to headline). No metric toggle, no scatter, no CapEx-by-account on this axis.
- Nav order + Taxonomy→Design Space Viz rename are in scope here.
- Grouping = the 6 facets, live; sort = fixed LCOE-ascending within group.
- Why-affordances = per-segment notes + concept-page link.
- One extractor change: emit cas71/cas72 + re-extract.

**Design must figure out:**
- The exact decomposition computation (component $/MWh = component-share-of-annualized × LCOE) and **where it runs** — extractor emits per-component $/MWh, or front-end derives from cas71/72/80/90 + headline. (Appendix A has the math.)
- Axis scaling for extreme-LCOE outliers (clip / flag / log / exclude freeform).
- Segment color tokens (reuse the CAS-breakdown palette or define 4 cost-bucket tokens traceable to a single authority).
- Tooltip override-note roll-up for aggregate segments (Capital spans many CAS accounts).
- Whether the grouping control is physically shared with the matrix (extract a reusable component) or re-implemented from the same facet model.
- Whether to honor the Phase-1 `apply_analyst_overrides` state on this page (v1 leans: no, use applied headline).
- Edge-case policy for off-normalization concepts (35, 02) and freeform/broken (03).

**Watch-outs for design:**
- Do not let CapEx-by-account (M$) leak onto the LCOE ($/MWh) axis — different units; keep deferred.
- 37 & 39 lack records (Item 2-FU, concept-side bugs); 24's stored headline had an FU2 staleness issue — the page inherits stored values, so tie missing/suspect data to the caveat marker rather than papering over it.
- Active 1 GWe override-policy churn is re-rolling underlying concept data; this page is UI-over-schema so it's insulated, but coordinate the re-extract (FR-F11) with that work to avoid stacking stale outputs.

---

## Related Artifacts

- **Research:** `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md` (J2/J3, Tier-1/Tier-2 ideas)
- **Epic:** `.project/backlog/epic_explorer_ux_v3.md` (Theme F; Navigation & page taxonomy; branching convention)
- **Upstream spine:** `.project/active/explorer-identity-spine/` (A1/A2/A3 authorities), `.project/active/explorer-override-inspection/` (Item 2 override records), `.project/active/explorer-ontology-matrix/` (B1 grouping idiom)
- **Design:** `.project/active/explorer-cost-landscape/design.md` (to be created)

---

## Appendix A — The LCOE decomposition (for design)

LCOE as implemented (`1costingfe/src/costingfe/layers/economics.py:78`):

```
LCOE ($/MWh) = (CAS90 + CAS70 + CAS80) × 1e6  ÷  (8760 × p_net × n_mod × availability)
                  │       │       │
                  │       │       └─ Fuel
                  │       └───────── O&M  =  CAS71 (Fixed O&M) + CAS72 (Replacement)
                  └───────────────── Capital (= CRF × total_capital)
```

Each component's $/MWh contribution is its share of the annualized-cost sum times the LCOE — exact, no separate energy term needed:

```
capital   $/MWh = CAS90 / (CAS70+CAS80+CAS90) × LCOE
fixed-O&M $/MWh = CAS71 / (…)                 × LCOE
replace   $/MWh = CAS72 / (…)                 × LCOE
fuel      $/MWh = CAS80 / (…)                 × LCOE
```

Worked check (concept 01): annualized sum = 1006.5 + 147.99 + 0.93 = 1155.4 M$ → capital 135.2 + O&M 19.9 + fuel 0.1 = **155.2 $/MWh** = headline ✓.

**Data availability today** (served `data/01.json`): `headline.lcoe_per_mwh`, `cas90`, `cas80`, **combined** `cas70` are present; `cas71`/`cas72` are **not** (the only gap — FR-F11). `params.n_mod`, `headline.p_net_mw`, `headline.capacity_factor` are present if an energy-based derivation is preferred over the share form. Override records are present (Theme A / Item 2).

## Appendix B — Why the availability scatter was dropped

The explorer headline is the `result_1gw` forward, which standardizes every concept to a ~1 GWe plant. And `default_availability` (`1costingfe/src/costingfe/validation.py:25`) is concept-blind: **0.87 for mirrors, 0.85 for everything else** — it does not encode pulsed vs continuous. Across the 39 served concepts, availability is 0.85 for 28, with a few analyst-set 0.75/0.80/0.87 — range 1.16×, while LCOE spans 130×. So the LCOE *denominator* is nearly constant and **LCOE ≈ 0.134 × annual cost** for the standardized cluster (verified: 01, 05, 24). A scatter on availability would be a vertical stripe with color tracking the y-axis — it would restate the bar, not add a dimension.

The continuous-vs-pulsed difference the scatter was meant to reveal is real but lives in the **cost numerator**: pulse cadence is folded into time-averaged power (`p_driver = e_driver_mj × f_rep`, `physics.py:576`), and the pulsed economic penalty surfaces in **CAS72 replacement** (laser optics, target chamber, electrodes, scheduled off `n_shots_per_year`) and **CAS80 fuel** (manufactured targets, zero for MFE). That is exactly why the numerator breakout (Replacement + Fuel segments) is the right place to see it — and why the 71/72 split (FR-F11) is load-bearing, not cosmetic.

---

**Next Steps:** After approval, proceed to `/_my_design`.
