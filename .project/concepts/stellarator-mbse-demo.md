# Concept: Stellarator MBSE Full Demo

**Created:** 2026-07-12
**Status:** Draft

---

## Problem Statement

The 1cFE investigation has moved from casting a wide net (38 concepts through `concept-analysis` and `concept-explorer`) to downselect deep dives, where the core question is "what would need to be true to get to 1c per kWh?" The team is splitting that work; this track's job is to prove that the agentic-mbse / sysml-codegen / teax methodology is a valid way to do such a deep dive, using a tokamak or stellarator as the vehicle.

The toolchain has one end-to-end proof so far: the IFE demo (WI-015, 2026-07-05) took SysML v2 models through codegen to teax execution with bit-exact LCOE anchors and an 11,505-point sweep. But that demo predates the constraint-execution epic: its viability rule was hand-coded in the sweep harness, there was no study layer, and no validation that the methodology can reproduce independently known results. There is also no public-facing account of the methodology at all.

This concept defines the first fusion-focused full demo: a QI stellarator physics+costing model built and refined with the full toolchain, validated two independent ways (a machinery handshake against 1costingFE, and a hold-out comparison against the ARIES-CS study), exercised through the new teax study layer, and written up for a public audience.

## Owner's Words

- **[OWNER-VERBATIM]** "I want to think through our first fusion-focused full demo."
- **[OWNER-VERBATIM]** "Essentially drilling into the concept further to probe at the core question 'what would need to be true to get to 1c per kWh?'"
- **[OWNER-VERBATIM]** "we should actually choose a concept that has a lot of design data available. The rationale is that we can start by *holding out* some of this information -- see if we can come to similar conclusions."
- **[OWNER-VERBATIM]** "This is mainly a validation of the sysmlv2 modeling capabilities and the codegen methodology."
- **[OWNER-VERBATIM]** "I would say this is 80% methodology demo. ... The other 20% is proof-by-example, but we don't NEED to have exhaustive contributions yet. If this succeeds, then yes we will focus on the deep-dive contribution."
- **[OWNER-VERBATIM]** (hold-out target) "Similarity in the structural models; Similarity in the 'optimized' sizing; Rough costing by component" — and "But this is a risk."
- **[OWNER-VERBATIM]** "The visualization of outputs will be really critical for this stage. I am imagining a full animation for showing a 'search' process."
- **[OWNER-VERBATIM]** "Whereas most custom TEA tools like 1costingFE need to decide 'what are the inputs' and 'what gets derived' (which can then be painful to change later), this is totally generalized to forward-pass and assess only. Not necessarily 'better', just has its own pros and cons."
- **[OWNER-VERBATIM]** (concept choice) "Let's pencil in `09`" — a provisional selection, not final.

## Success Criteria

When this work is complete:

1. **Initial model runs end-to-end** — A SysML v2 stellarator physics+costing model (bootstrapped from in-repo sources: the Stellaris design paper, W7-X material, generic MFE costing) generates through sysml-codegen and executes under teax, producing LCOE and a full CAS-account breakdown at the Stellaris design point.
2. **Viability checks execute as modeled constraints** — Physics viability limits (candidates: confinement-scaling consistency, beta/density limits, wall load, TBR floor) are modeled as `assert constraint`s and execute via the constraint-execution machinery, with verdicts (satisfied / violated / indeterminate) appearing as data in run reports — no hand-coded viability rules anywhere in the demo.
3. **1costingFE handshake** — The SysML forward model, fed the plant point 1costingFE solved for (its solved fusion power plus its merged parameter set), reproduces 1costingFE's per-account costs and LCOE within a tolerance the spec defines. Discrepancies are itemized and explained.
4. **ARIES-CS hold-out comparison** — With ARIES-CS sources ingested but quarantined throughout model development, the finished model is evaluated at the ARIES-CS design point (their geometry and magnet technology) and a comparison report covers: structural similarity of the models, derived-quantity agreement given their geometry (radial-build consequences, coil mass, power flows), and rough per-component costs versus their published values. The spec defines quantitative expectations per axis, and those expectations are pass/fail for this criterion — a miss beyond them fails the anchor and is reported as a demo finding, not narrated away. Note on the owner's three axes: "optimized sizing" cannot be tested at a fixed design point (sizing is an input there); that axis is covered only by the stretch criterion 8. **[SURFACED to owner]** — this reallocation needs owner confirmation.
5. **Studies run through the teax study layer** — At least one parameter sweep and one A/B instance-swap study (e.g., magnet technology or blanket material) run via `teax` study definitions using the study layer's delivered execution semantics, with constraint verdicts classifying points — no hand-rolled sweep loops or harness code. (Resume/crash-safety is the epic's acceptance criterion, not this demo's.)
6. **Study outputs are visualized** — Sweep and A/B results render as figures that ship embedded in the criterion-7 blog draft, including an animated visualization of the design-space exploration. Since studies are prepared lists/grids (no optimizer), the animation depicts the stage 3⇄4 refinement arc — successive study rounds narrowing on the critical subsystems — rendered over study results, not a live search trajectory.
7. **Public write-up exists** — A blog-post draft plus supporting GitHub-hosted interactive HTML explain how the system works, what the fusion implementation looks like, and the forward-pass-and-assess versus inverse-solver framing (using the 1costingFE handshake as the concrete illustration), with the hold-out protocol and its results reported honestly.
8. **(Stretch) Optimum rediscovery** — A constrained search study over sizing variables, run with ARIES-CS-era technology and cost assumptions, is compared against ARIES-CS's published optimized sizing. Because sourcing the vintage assumptions requires reading ARIES-CS, this runs after the reveal: the model is frozen as of comparison time, and only vintage input values change post-reveal — the search itself stays mechanical (grid). This is a showcase if it works; a miss is ambiguous (model error vs vintage-assumption error) and does not fail the demo.

---

## Why This Shape

- **Key bet:** A methodology demo is only credible if the model is checked against results it could not have copied. Two independent anchors do this: the 1costingFE handshake validates the *machinery* (same point in, same costs out), and the ARIES-CS hold-out validates *generality* (a model built from Stellaris/W7-X sources, evaluated at a design point it never saw). **[AGENT]** The anchors are genuinely independent: 1costingFE's stellarator dollars are calibrated to NCSX fabrication experience on a SPARC-anchored baseline, not ARIES-CS (single known exception: the C220107 power-supplies sub-account is ARIES-CS-derived and must be excluded or footnoted in the hold-out comparison).
- **Why 09 (QI stellarator):** The Stellaris design paper is fully extracted in-repo with complete geometry/field/power/blanket tables and **zero cost data** (economics explicitly deferred) — so the costing side cannot crib from the design source. ARIES-CS provides the one complete public stellarator conceptual design *with* costing to hold out. The existing 09 pipeline model proves the bootstrap is sufficient.
- **Why evaluate at the ARIES-CS point rather than compare plants:** **[AGENT] (ratified by owner, 2026-07-12)** ARIES-CS (quasi-axisymmetric, Nb3Sn LTS, R = 7.75 m) and Stellaris (quasi-isodynamic, HTS, R = 12 m) are different machines; head-to-head comparison validates nothing. Re-running the bootstrapped model at their design point tests whether the modeling method generalizes — which is the 80% goal.
- **Constraint to preserve downstream:** The hold-out must stay a real blind. ARIES-CS ingestion is quarantined from day one, and all agentic research/model-development prompts blocklist ARIES-CS entirely until the comparison stage (owner's choice of the strict variant). The write-up claim is scoped as "no ARIES-CS-specific stellarator data used" — not "no ARIES lineage at all," since 1costingFE's account structure descends from the ARIES/Starfire cost-account family and one superseded 09 analysis iteration once cited ARIES-CS.

---

## User Stories

### Methodology validation

**US-1: Reproduce a known design's economics blind**
As the methodology owner, I can point to a comparison report showing the model — built without seeing ARIES-CS — lands near ARIES-CS's published derived quantities and component costs when evaluated at their design point, so that I (then others) trust the methodology for deep dives on concepts with *no* published answer.

**US-2: Cross-check the machinery against the team's tool**
As a team member using 1costingFE, I can see the SysML forward model reproduce 1costingFE's costs when fed the same plant point, so that I trust the generated pipeline computes the same economics our existing tool does.

### Model development

**US-3: Refine the model where it matters**
As the modeler, I can run studies, see which subsystems dominate cost or bind viability, direct agentic research at those subsystems, and fold findings back into the model, so that model depth grows where leverage is highest rather than uniformly.

**US-4: Ask design questions as studies**
As the modeler, I can define a parameter sweep or an A/B component swap as a `teax` study and get back classified (viable/violated/indeterminate) costed points with resume-safety, so that design-space questions don't require bespoke harness code.

### Communication

**US-5: Show the process publicly**
As a public reader of the blog post, I can follow how a SysML model becomes a running cost pipeline, watch a search of the design space, and understand the forward-pass vs inverse-solver trade, so that the methodology's value is legible without fusion-TEA background.

---

## Key Concepts

### 1. The five-stage demo arc

Owner-defined stages; 3 and 4 deliberately interleave ("run studies, sanity check, find issues, research and refine, then set up new studies" — order between them may switch).

1. **Concept choice** — 09 penciled in (see Owner's Words).
2. **Initial model** — physics+costing model from in-repo basic sources: forward physics calculations, viability checks as assert constraints, the CostedComponent pattern, comparison against 1costingFE. Mainly validates SysML v2 modeling + codegen.
3. **Agentic research and model development** — AI-driven source research on materials/physics for the subsystems that studies reveal as critical; recursive refinement. Least-specified stage by design.
4. **Studies** — `teax` study definitions: parameter sweeps, A/B model-instance comparison; visualization including the search animation.
5. **Write-up** — public blog post + interactive HTML; includes the "how it fits a larger development process" framing and the forward-pass vs inverse-solver illustration.

### 2. Hold-out validation protocol

ARIES-CS full papers (systems-optimization and overview papers; OSTI IDs already captured in-repo) are ingested into a quarantined location before modeling starts. Every model-development and research prompt blocklists ARIES-CS until stages 2–3 conclude. At comparison time, the model is evaluated at the ARIES-CS design point and compared per criterion 4. The protocol, including the pre-existing contamination inventory (superseded iter-1 calibration, one narrative LCOE quote in the 09 synthesis, ARIES-lineage library defaults), is documented so the public claim is defensible. One limit is inherent and stated up front: the blocklist controls prompts and sources, not model priors — the agents' training data includes ARIES-CS publications. The public claim is therefore scoped to "no ARIES-CS material in context or sources during model development," and the write-up says so explicitly.

### 3. Two-anchor validation

Anchor A (machinery): 1costingFE `forward()` solves fusion power from a net-electric target; its result carries the full merged parameter set. Handing that point to the SysML forward model and comparing per-account costs isolates the codegen/execution machinery from modeling judgment. Anchor B (generality): the ARIES-CS hold-out. A must pass tightly; B is expected to be rough and is reported with discrepancies explained.

### 4. Forward-pass-and-assess as the story

The write-up's central contrast: 1costingFE commits at design time to what is input and what is derived (its forward call inverse-solves fusion power from net electric; backcasting solves parameters from target LCOE). The SysML approach is forward-pass and assess only — any quantity can become a study variable, and viability is asserted, not solved for. The demo shows this is a trade, not a win: the handshake requires *feeding* the SysML model a solved point, which is exactly the capability forward-pass gives up.

---

## Scope of Behavior Changes

### New artifacts to create

- SysML v2 stellarator model set: concept-agnostic library additions (`models/library/`) and the 09 design instance (`models/designs/`), including viability `assert constraint`s
- Generated + sealed teax package(s) for the stellarator model; study definitions (sweep, A/B)
- ARIES-CS source ingestion in a quarantined location + registration
- 1costingFE handshake script/report; ARIES-CS comparison report; hold-out protocol record
- Visualization assets (sweep figures, search animation); blog-post draft; interactive HTML page
- Demo work items/records in the modeling PM (`work/`), following the WI-015 pattern

### Existing artifacts to modify

- `knowledge/` source indexes (ARIES-CS registration with quarantine marking)
- MFE cost-structure library elements (WI-009) as needed for stellarator specifics

### Behavior changes by workflow stage

- Model development: viability judgment moves from prose/harness into modeled constraints
- Studies: design-space questions move from bespoke scripts into `teax` study definitions

---

## Non-Goals / Out of Scope

- **[OWNER]** An exhaustive deep-dive contribution — this is 80% methodology demo; the full "what must be true for 1c/kWh" investigation follows only if the demo succeeds.
- **[AGENT]** Changes to 1costingFE itself — it is a comparison anchor, pinned at a fixed version; gaps found in it are filed, not fixed here.
- **[AGENT]** Head-to-head Stellaris-vs-ARIES-CS plant comparison — different topology/magnet-tech/era; the demo evaluates its own model at the ARIES-CS point instead.
- **[AGENT]** Validating Proxima's Stellaris design — the paper is a data source for bootstrapping, not a claim under test.
- **[AGENT]** New study-layer capability beyond what the constraint-execution epic delivers (prepared lists/grids); adaptive/optimizer strategies are not assumed even for the stretch goal, which can run as a grid.
- **[AGENT]** Modeling a tokamak in parallel — 09 is penciled in; a switch is a concept-level revisit, not a second track.

---

## Assumptions & Prerequisites

- **Constraint-execution epic lands first** (owner decision): constraint execution, sealed packages, and the teax study layer (`~/1cfe/sysml-codegen/.project/backlog/epic_constraint_execution.md`, through Item 12) are available before stage 4; stages 1–2 need only today's toolchain.
- ARIES-CS full papers are obtainable and ingestible (freely available; OSTI 1014258, 20849901 already captured as abstracts in-repo).
- SysIDE license available for live extraction (snapshot path exists as fallback).
- 1costingFE version discipline is to-be-established, not assumed: fusion-tea consumes it as an editable local path dependency (`pyproject.toml`), so nothing pins it today. The handshake report must record the exact 1costingFE commit it ran against — a spec item.
- In-repo 09 sources (Stellaris paper extraction, W7-X material) are sufficient bootstrap — evidenced by the existing 09 pipeline model.

## Open Questions

1. Handshake tolerance: what per-account and LCOE agreement counts as pass for Anchor A? (Parameter-mapping traps exist, e.g. 1costingFE's radiation-model `B` = 5 T vs coil-cost `b_center` = 6 T must both transfer.)
2. Hold-out expectations: what counts as "similar" per axis (structure / sizing / component costs) for Anchor B? Order-of-magnitude? Factor-of-2? Per-axis?
3. Which viability constraints are in the initial model vs added in stage 3? (Candidates: confinement scaling à la ISS04, beta limit, density limit, wall load, TBR floor, coil stress/standoff.)
4. Quarantine mechanics: how is the blocklist enforced in agentic research prompts, where does the quarantined ingestion live, and what triggers/records the reveal?
5. ARIES-CS-era assumption set for the stretch study: which technology/cost assumptions must be swapped to their vintage, and where do those values come from?
6. Write-up split: what lives in the blog post vs the interactive HTML vs a possible live tool?
7. PM split: which pieces run as modeling PM work items (`work/`) vs coding PM (`.project/`) — WI-015 precedent suggests modeling PM owns the model/demo items.

---

## Next-Stage Handoff

**Settled here:**

- **[OWNER]** Concept 09 (QI stellarator) is penciled in — proceed on it; revisiting the choice reopens this concept, not the spec.
- **[OWNER]** 80% methodology demo / 20% proof-by-example; exhaustive contribution deferred to follow-on work.
- **[OWNER]** Write-up is public-facing: primary blog post + supporting GitHub-hosted interactive HTML (possibly a live tool).
- **[OWNER]** The demo assumes the constraint-execution epic completes first.
- **[OWNER]** Quarantine strictness: full ARIES-CS blocklist until the comparison stage ("first try" the strict variant — may be relaxed by the owner if it proves unworkable).
- **[OWNER]** The 1costingFE comparison works by feeding the SysML forward model the parameter set 1costingFE solved for.
- **[AGENT] (ratified by owner, 2026-07-12)** Hold-out test = evaluate at the ARIES-CS design point (committed) + optimum-rediscovery (stretch only).
- **[AGENT] (ratified by owner, 2026-07-12)** Initial model includes viability physics as assert constraints (one notch deeper than 1costingFE's fixed-operating-point power balance).

**Needs spec next:**

- Tolerances and pass criteria for both anchors (open questions 1–2)
- The initial constraint set and its physics sources (open question 3)
- The quarantine/reveal protocol as concrete procedure (open question 4)
- Stage 3 ⇄ 4 interleaving: what the first study round is, and what triggers a research round
- Owner's noted risk stands: the bootstrap → refine → compare-to-hold-out loop is unproven; spec should define the earliest cheap checkpoint that tests it (e.g., a stage-2 mini-comparison on one subsystem)

**Decomposition guidance:**

- Natural work-item seams: (a) ARIES-CS ingestion + quarantine setup, (b) initial SysML model + codegen + Stellaris-point run, (c) 1costingFE handshake, (d) research/refinement rounds, (e) study definitions + runs, (f) visualization, (g) ARIES-CS comparison, (h) write-up. (a) is independent and can start immediately; (b–c) need only today's toolchain; (e) waits on the epic.
- The demo spans both PM systems: modeling items in `work/`, tooling/write-up items in `.project/` — decompose accordingly rather than as one mega-epic in either.
