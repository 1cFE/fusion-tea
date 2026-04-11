# Concept: Fusion Concept Explorer

**Created:** 2026-03-28
**Status:** Draft
**Related Epic:** ANALYSIS-V2, Item 2 (Build-Visuals Stage) — this concept describes the full vision; Item 2 is a first slice

---

## Problem Statement

Today, the output of the concept analysis pipeline is a collection of markdown files: `analysis.md`, `model_output.txt`, `synthesis.md`. A reviewer who wants to understand a concept must read thousands of lines of text, mentally cross-reference parameter tables against sensitivity sweeps, and remember numbers from one concept while reading another. There is no way to quickly grasp what a concept IS, what DRIVES its economics, or how it COMPARES to alternatives.

The reference project (`Dipole_Tokamak_LaserIFE_Comparison`) demonstrates how powerful even basic cross-concept sensitivity comparison is — grid searches across shared parameter axes immediately reveal which concepts are robust and which are fragile. But that project required bespoke Python scripts per concept. The concept analysis pipeline has standardized cost models for 8 concepts (and growing), each with 40+ sensitivity parameters, CAS-level cost breakdowns, and rich narrative context about risks, innovations, and assumptions. This data is ready to be made visual and interactive.

The deeper problem isn't just "we need charts." It's that the most important information — *why* a parameter matters, *how* it's modeled, *what* the concept bets on — is buried in prose. A reviewer can't efficiently build the intuition needed to evaluate whether a concept's economics are credible without toggling between analysis text, model code, and output tables. The tool should surface this narrative context *at the point of need*, attached directly to the numbers.

**Why now:** Once ~10 concepts are finalized, the comparison problem becomes acute. And when concept 11 arrives — less familiar, freshly analyzed — being able to compare it against the established 10 will: highlight key differences, raise questions about "why" and "how" this concept looks the way it does, identify potential analysis failures, and build intuition. The explorer isn't just a reporting tool — it's a review instrument.

## Success Criteria

When this work is complete:

1. **Concept identity at a glance** — The profile view displays concept name, confinement family, company, key differentiators, operating parameters (P_fus, P_net, Q_eng), headline LCOE, total capital cost, and confidence rating without requiring the reviewer to scroll or read analysis.md.

2. **Sensitivity with context** — Every sensitivity bar in the tornado chart shows its LCOE elasticity. On hover/click, a detail card appears with: baseline value and source, assumed range, confidence level, modeling mechanism, and parameter category (shared baseline / key innovation / concept-unique / high-risk). No toggling to model_setup.py or analysis.md required.

3. **Comparisons that teach** — The comparison view aligns shared parameters horizontally across concepts, surfaces concept-unique parameters separately, and shows CAS-level cost breakdowns side by side. Structural explanations of WHY key sensitivities differ are accessible via the companion `/manage-concept` agent (the tool provides the numerical context; the agent provides causal interpretation).

4. **Trust through traceability** — Confidence levels are encoded visually on every parameter (color, badge, or opacity). Overridden CAS accounts are flagged. A reviewer can never mistake a speculative estimate for a well-grounded one.

5. **Fluid navigation** — Adding or removing a concept from comparison requires one interaction per concept, with no page reload. The entry view shows approved and in-progress concepts; clicking one opens its profile.

---

## User Stories

### Understanding a New Concept

**US-1: First encounter**
As a researcher encountering a concept for the first time, I can see its identity — name, company, confinement approach, one-line thesis ("Single floating HTS coil — simplest possible MFE magnet system") — plus a slot showing what makes it physically distinctive (schematic, diagram, or photograph), so that I have a mental model before diving into economics.

**US-2: Economic snapshot**
As a researcher, I can see headline LCOE, total capital, net power, Q_eng, and confidence rating in a compact summary card, so that I immediately know the concept's economic ballpark and how much to trust the estimate.

**US-3: Economic thesis**
As a researcher, I can see — prominently, not buried — what this concept bets on (key innovations), what cost categories it eliminates (e.g., "no tritium handling" or "no divertor"), and what novel cost categories it introduces (e.g., "annual sacrificial coil replacement"), so that I understand where its economic argument lives before looking at numbers.

### Exploring Sensitivities

**US-4: What drives LCOE?**
As a reviewer, I can see a ranked tornado chart of parameters by LCOE elasticity, so that I know where to focus my scrutiny. The top 3-5 sensitivities are visually emphasized.

**US-5: Understanding a specific sensitivity**
As a reviewer, when I interact with a sensitivity bar, I see a detail card showing: (a) the baseline value and its source citation, (b) the assumed range and why that range was chosen, (c) the confidence level, (d) one sentence on how this parameter flows through the cost model, and (e) a category label — so that I can judge whether this sensitivity is well-grounded or speculative.

**US-6: Spotting where the argument lives**
As a reviewer trying to assess credibility, I can visually distinguish shared baselines (same for all concepts — discount rate, construction time), well-established concept parameters, key innovation claims, concept-unique novelties, and high-risk assumptions — so that I can focus my skepticism on the parameters that actually differentiate the concept's economics.

**US-7: Interactive "what-if"**
As a reviewer, I can adjust parameter values and see LCOE update, so that I can test "what happens if this assumption is wrong?" When I move a slider, the tornado chart re-ranks (some parameters become more important), the CAS breakdown updates, and the summary card reflects the new LCOE. I can reset to baseline at any time.

### Comparing Concepts

**US-8: Flexible comparison**
As a researcher studying a concept, I can pull in any other modeled concept for comparison — not restricted to "same family" — so that I can compare based on whatever dimension matters right now: similar physics, similar cost structure, shared vulnerability, or contrasting approach.

**US-9: Aligned sensitivity profiles**
As a reviewer comparing two concepts, I can see their tornado charts aligned so that shared parameters (availability, eta_th, construction_time_yr, interest_rate, etc.) line up horizontally and concept-unique parameters (e.g., dipole's annual coil replacement, IFE's target factory cost) stand out in separate sections — so that I immediately see where the concepts face the same challenges and where they diverge.

**US-10: CAS structure comparison**
As a reviewer, I can see each concept's cost breakdown by CAS category side by side (stacked bars or waterfall), so that I can see which are capital-dominated vs. operations-dominated, which CAS accounts dominate each concept, and where the money flows differently.

**US-11: Range and confidence comparison**
As a reviewer, I can see each concept's LCOE range (optimistic to conservative scenarios from model_output.txt) and confidence level side by side, so that I can assess not just "which is cheaper" but "which estimate do I trust more."

**US-12: Getting causal explanations**
As a reviewer who sees that concept A is 3× more sensitive to magnet cost than concept B, I can take that observation to the `/manage-concept` interactive agent — which can access the explorer's current state (which concepts are compared, what parameter values are set) — to get a structural explanation of WHY. The tool shows me WHAT differs; the agent helps me understand WHY.

### Navigation and Discovery

**US-13: Entry view**
As a researcher opening the explorer, I see all concepts organized as "approved" (finalized analyses) and "in progress" (still being analyzed), with enough information per concept (name, family, LCOE range, confidence badge) to decide where to start. Clicking a concept opens its profile. A supported subset of concepts are available for comparison views.

**US-14: Following threads**
As a researcher who noticed that "HTS magnet cost" is critical for the dipole, I can quickly see which other concepts also have sensitivity to that parameter, so that I can follow a technical thread across the investigation without manually opening each concept.

---

## Key Concepts

### 1. The 1costingfe Standardization Advantage

All 8 modeled concepts use the `1costingfe` framework, which guarantees identical output structure: same 17 CAS codes (CAS10-CAS90), same 15 CAS22 sub-accounts, same LCOE formula, same sensitivity computation (JAX autodiff elasticities on the same dimensionless scale). This means CAS-level comparison is structurally sound — apples to apples. Sensitivity elasticities are directly comparable across concepts: when the dipole has availability elasticity of -0.91 and laser IFE has -0.45, that's a real, meaningful difference driven by structural economics, not measurement artifacts.

Concept differences are isolated to: engineering defaults (YAML per concept type), physics equations (MFE/IFE/MIF power balance), geometry (toroidal/cylindrical/spherical), and concept-specific cost overrides. The CAS hierarchy, scaling laws, and financial formulas are identical.

If a future concept can't use 1costingfe, a minimum output interface would be needed. But today, all modeled concepts share this foundation.

### 2. Parameter Categories

Every sensitivity parameter belongs to one of these categories, which drive the visual treatment:

- **Shared baseline**: Same value across all concepts (discount rate, inflation, construction time). Moving these affects all concepts equally — not where the economic argument lives.
- **Well-established concept parameter**: Concept-specific but grounded in published data or mature analogues (e.g., REBCO tape cost for HTS concepts).
- **Key innovation**: What the concept claims as its breakthrough — the parameter whose favorable value makes the economics work (e.g., direct energy conversion efficiency for FRC, single-coil simplicity for dipole).
- **Concept-unique novelty**: A cost category or parameter that exists only for this approach, with no precedent to calibrate against (e.g., annual sacrificial coil replacement for dipole, avalanche gain for p-B11 laser ICF).
- **High-risk assumption**: Poorly constrained AND high LCOE impact. The intersection of uncertainty and sensitivity — where the estimate is most fragile.

These categories are authoring metadata, not computed properties. They must be authored as part of the analysis pipeline (likely in a structured metadata file alongside model_setup.py).

### 3. Tool + Agent Complementarity

The explorer and the `/manage-concept` interactive agent are complementary instruments:

- **Explorer**: Shows WHAT — sensitivity rankings, CAS breakdowns, parameter values, comparison alignments. Visual, interactive, self-service.
- **Agent**: Explains WHY — structural reasons for sensitivity differences, causal chains, traceability to sources, judgment about credibility. Conversational, interpretive.

The agent needs to be able to access or reconstruct the explorer's numerical state: which concept is being viewed, what parameter values are set (if sliders have been moved), which concepts are in the comparison set. This allows a workflow where the reviewer plays with the explorer, notices something interesting, and takes the question to the agent without having to re-describe what they're looking at.

---

## Design Aesthetic

### Design Principles

**1. Trustworthy density.** Bloomberg terminal, not marketing dashboard. Information-dense but navigable. The user is a domain expert who wants to see the data, not be protected from it. Every number earns its space; every visualization serves a decision.

**2. Uncertainty is visual, not footnoted.** Confidence levels are as visually prominent as the values themselves. A reviewer should never mistake a speculative estimate for a well-grounded one. Color, opacity, hatching, badges — uncertainty is impossible to ignore.

**3. Narrative at the point of need.** Context (why this value, how it's modeled, what would change it) appears exactly where the reviewer needs it — attached to the parameter via hover/click, not in a separate document.

**4. Compare by default.** A number in isolation is almost meaningless for TEA. The tool nudges toward "compared to what?" — showing where a value sits relative to the population of analyzed concepts, even in single-concept view.

**5. The overview invites exploration.** The entry point shows enough to make you curious. Like a museum map — you should want to explore rooms, not need a guide to find them.

### Visual Directions (to be validated during design)

**Sensitivity tornado chart:** Horizontal bars extending left (LCOE decrease) and right (LCOE increase) from baseline. Parameter category encoded via color/treatment. Top sensitivities visually emphasized. Detail card appears on interaction.

**CAS composition:** Stacked bar or waterfall chart. In comparison mode, bars sit side by side. Hovering a CAS segment shows cost, scaling law, and any overrides. Overridden accounts are flagged (these are where the concept-specific engineering judgment lives).

**Concept identity hero:** Name, company, one-line thesis, key stats card, slot for illustration. The layout accommodates a schematic, photograph, or stylized representation equally well.

**Comparison alignment:** Shared parameters aligned horizontally across concepts. Concept-unique parameters in separate sections below. In the CAS view, side-by-side stacked bars with shared x-axis scale so magnitude differences are immediately visible.

**Entry view:** Two groups — approved and in-progress. Each concept shows a compact card (name, family badge, LCOE range, confidence indicator). Clicking opens the profile. Cards for modeled concepts are richer than those with analysis-only data.

---

## Out of Scope

- **Authoring or editing artifacts** — the explorer is read-only; changes flow through the pipeline
- **Full grid search / Monte Carlo** — sliders do single-parameter "what-if," not combinatorial sweeps
- **Automated diagram generation** — illustration slots are manual; the explorer doesn't generate concept art
- **Causal explanations of differences** — the agent handles interpretation; the explorer surfaces the numbers
- **Custom-costed concept support** — all current concepts use 1costingfe; a custom output interface is deferred until needed
- **Export / sharing** — saving comparisons or generating static snapshots for reports is future work

## Assumptions & Prerequisites

- Concepts with `model_setup.py` + `model_output.txt` (1costingfe-backed) get the full experience: sensitivities, sliders, CAS breakdown, comparison views
- Concepts with only `analysis.md` get a reduced profile: identity, challenges, TRL — no interactive cost model, not available for comparison views
- Parameter categories must be authored as structured metadata alongside the cost model — the explorer displays them but doesn't infer them
- The `/manage-concept` agent (or similar) can read/reconstruct the explorer's numerical state for causal interpretation

## Open Questions

1. **Parameter category metadata format.** Where do the "key innovation" / "high-risk" / "shared baseline" labels live? Options: structured comments in model_setup.py, a separate `model_metadata.yaml`, or fields in synthesis.md. Needs to be maintainable as analyses iterate.

2. **Concept illustration strategy.** The identity section benefits hugely from a visual. Options: curated from papers (copyright?), simplified diagrams (manual authoring cost?), AI-generated schematics (quality?), or photographs of prototypes where available.

3. **Explorer state for agent access.** How does `/manage-concept` access what the reviewer is looking at? Options: the explorer writes a state file, the agent reads the HTML and extracts state, or the reviewer copy-pastes a URL/parameter string.

4. **Reduced profile design.** What does an analysis-only concept (no cost model) look like in the explorer? It needs enough presence to be useful for context but shouldn't imply economic analysis exists.

---

## Decomposition Guidance

This concept splits into progressive layers, each independently useful:

**Layer 1 — Single-concept profile** (maps to epic Item 2)
Concept identity + sensitivity tornado chart + CAS breakdown for one concept. Proves the information architecture. No comparison, no metadata popups, no sliders.

**Layer 2 — Parameter detail cards**
Hover/click detail on each sensitivity bar. Requires resolving Open Question 1 (metadata format). This is where "narrative at point of need" comes alive.

**Layer 3 — Comparison view**
Side-by-side profiles with aligned parameters and CAS breakdowns. Entry view with approved/in-progress grouping. This is the highest-value layer after the basic profile.

**Layer 4 — Interactive sliders**
JS reimplementation of the cost model for live "what-if." Most technically complex. The 1costingfe standardization helps — the cost model structure is regular enough to transpile, though concept-specific overrides add complexity.

**Layer 5 — Agent integration**
Explorer exposes state for `/manage-concept` to consume. Enables the tool + agent workflow described in US-12.

Layers 1-3 deliver the core value. Layer 4 is powerful but deferrable. Layer 5 ties it all together.
