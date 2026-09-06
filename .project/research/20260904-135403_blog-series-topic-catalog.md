---
date: 2026-09-04T13:54:03-07:00
researcher: Claude
topic: "Marquee blog series: catalog of concepts, topics, results, and where to read more"
tags: [research, blog, communication, pipeline, harness, 1cfe-context]
status: complete
last_updated: 2026-09-04
---

# Research: Marquee Blog Series Topic Catalog

**Date**: 2026-09-04 (PDT)
**Researcher**: Claude
**Research Type**: Information collection across five repos, the live blog, and sibling 1cFE work

## Research Question

The owner wants to plan marquee blog posts that capture the last year of work for an external audience: original hypotheses, concepts, progress, contributions, code and explainers, and results. The posts must cover the whole pipeline (agentic-mbse, sysml-codegen, teax), call out the key tools, frame the whole thing as a harness of agents plus a coordination system, and place the work in the 1cFE context (concept exploration, relation to 1costingFE, and the stellarator deep dive relative to colleagues' corridor pursuits). The most important thing is showing how it is working.

This document does not draft posts. It organizes every distinct topic worth considering, gives each a short summary, and points to where to read more.

## Summary

- **The public story has a hole exactly where this series belongs.** The March post promised "the next post will cover the TEA pipeline: how we go from formal system models to cost estimates," and the February roadmap promised a "physics constraints" post where "constraints propagate through the cost model rather than sitting as buried assumptions." Neither has been written. The June posts covered the concept-analysis pipeline and 1costingFE, not the SysML to codegen to teax route, and not the goal harness.
- **There is a large body of near-ready prose.** Three goal narratives dated 2026-09-04, four HTML explainers under `docs/demo/`, a teax explainer, a near-finished pipeline draft at `docs/concept-pipeline/pipeline.md`, the hypothesis dossier, and the CHANGELOG. Section 5.9 lists every reusable asset.
- **The strongest editorial throughline is honesty under measurement, not capability.** Pre-committed pass bars, an unfired blind hold-out, "disclosed, never tuned," a negative result kept as the finding, and a ledger of process failures the harness caught. Section 5.8 collects these.
- **The 1cFE frame is clear from the sources.** 1costingFE is the forward, differentiable costing engine with 17 archetypes. fusion-tea is the model-based route where engineering logic lives in the model and design parameters vary freely. Colleagues' corridor deep dives (Helion-class, Borealis-class) are floor hunts built directly on 1costingFE with evidence ladders. The stellarator work is the same kind of deep dive done through the MBSE route, with the harness running the rounds.
- **Headline numbers exist for every claim.** Section 5.10 tables them with source paths so a writer never quotes from memory.

## How to read this catalog

Paths without a prefix are relative to `~/1cfe/fusion-tea/`. Sibling repos are written `agentic-mbse/...`, `sysml-codegen/...`, `teax/...`, `1costingfe/...` and live under `~/1cfe/`. The m-scout precursor lives at `~/m-scout/`.

Each entry carries a type tag: HYPOTHESIS, METHOD/TOOL, PROCESS/HARNESS, RESULT, DECISION, DEMO/EXPLAINER, or NARRATIVE (writer-ready prose).

Scratchpad copies of the six sub-agent catalogs that fed this document are at `/tmp/claude-1000/-home-reid-1cfe-fusion-tea/625f5cd2-e691-43b2-8b6a-81ee1b1ba469/scratchpad/agent*_*.md` for this session only. Everything load-bearing is repeated here with a repo path.

## Detailed Findings

### 1. Where the public story stands today

**The live blog** (`https://1cf.energy/updates/`, eight posts, all 2026):

| Date | Title | Author | What it covers |
|---|---|---|---|
| Feb 24 | Introducing 1cFE | Damien Scott | The backcasting question, the three things being built (formal modeling layer, TEA engine, concept taxonomy), the team, and the roadmap: methodology and tooling, then the spanning set, then physics constraints, then corridor maps, then synthesis |
| Mar 10 | Searching the Fusion Design Space Systematically | Reid | Why SysML v2 (definition vs usage, textual notation, git, AI coding tools), the six-level verification stack, the agentic workflow (spec, design, plan, implement), the IFE demo, relationship to PyFECONS and PROCESS. Ends: "The next post in this series will cover the technoeconomic analysis pipeline" |
| Mar 27 | The Unsolved Engineering Behind Fusion Power | (team) | Tritium breeding, tritium extraction, remote maintenance as first-class cost drivers |
| Apr 8 | Fusion's cost floor: what if the core were free? | (team) | D-T floor $29/MWh even with a free core; fuel choice reshapes buildings and staffing. Source draft: `1costingfe/docs/blog/1 Floor/` |
| May 12 | Direct Energy Conversion for Fusion | (team) | Venetian blind and pulsed inductive DEC; efficiency, not BOP, is where DEC pays. Source draft: `1costingfe/docs/blog/2 DEC/` |
| May 27 | Space Sector vs. Fusion Sector | Mallory Snowden | Analogy essay |
| Jun 10 | From Papers to Plant Economics: Costing 38 Fusion Concepts in One Pipeline | Mallory Snowden | The concept-analysis pipeline (stages 0 to 3, filesystem as state machine, `run_analysis.py` flags), the ST-E1 walkthrough, the Concept Explorer, three observations, validation spot checks, known limitations. Promises a down-select post |
| Jun 29 | Introducing 1costingFE | Tal Rubin | The open-source costing engine, three override levels, JAX elasticities (availability −0.91, interest rate +0.69), landscape, "what is shaky": geometry and power are separate inputs, "the fusion-tea pipeline ingests them." Source draft: `1costingfe/docs/blog/3 Intro/` |

Fetched copies of the four pages the owner named plus the Feb 24 post are in the session scratchpad as `blog_*.txt`.

**What was promised and not yet written** (all DECISION-grade facts from the posts themselves):

- The TEA pipeline post: SysML model to cost estimate via sysml-codegen and teax. Promised Mar 10. Not written.
- The physics-constraints post: constraints propagating through the cost model. Promised Feb 24 as roadmap step 3. Not written. This is exactly constraint execution, fences, and the goal harness.
- The spanning-set post. Drafted by Mallory as "Six Candidate Corridors" / "The Spanning Set" at `~/1cfe/Candidate corridors.md` (target June 1, status Drafting). It has a placeholder "How We Ingest a New Concept" section that says "reference the methodology post for details on the verification stack and agentic workflow."
- The down-select post promised Jun 10. The material exists at `docs/demo/down-select.html` and the score explorer.

**Other live public surfaces** (all returned HTTP 200 on 2026-09-04):

| URL | What it is | Source |
|---|---|---|
| `https://1cfe.github.io/fusion-tea/demo/index.html` | The interactive workflow explainer (IFE) linked from the Mar 10 post | `docs/demo/index.html` |
| `https://1cfe.github.io/fusion-tea/` | The public Score Explorer | `docs/index.html`, `docs/data/concepts.json` |
| `https://1cfe.github.io/fusion-tea/concept-pipeline/dependency-graph.html` | Seven-part dependency map of the concept pipeline | `docs/concept-pipeline/` |
| `https://1cfe.github.io/fusion-tea-walkthrough-visualization/` | The ST-E1 pipeline walkthrough linked from the Jun 10 post | separate public repo |
| `https://1costingfe.1cf.energy/` | The 1costingFE explorer | private repo `1costingfe-explorer` |
| `https://concepts.1cf.energy/` | The hosted Concept Explorer (HEAD returned 405, so GET-only) | `exploration/concept_explorer/`, runbook `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md` |
| `https://files.1cf.energy/1costingfe_paper.pdf` | The methodology paper | `1costingfe/docs/papers/1costingfe_paper/` |

**The GitHub org `1cFE`** (from `gh repo list`, 2026-09-04): public repos `fusion-tea`, `agentic-mbse`, `sysml-codegen`, `1costingfe`, `fusion-tea-walkthrough-visualization`, `levers` (LCOE lever-stack reference), `Tokamak-TEA-Tool`, `fusion-backcasting`, `Magnetic-Confinement-Comparison-DWhyte-Methodology`. Private: `helion_pulsed_frc_tea`, `borealis_mirror_tea`, `1costingfe-explorer`, `1costingfe_fusion_tea_interaction`, `nttau`, `Dipole_Tokamak_LaserIFE_Comparison`, `1costingfe_dashboard`, `tea-models`. Note teax is at `rwestwood89/teax`, not under the org (`README.md` clone instructions).

### 2. The 1cFE frame: where fusion-tea sits

**The question.** What must be true for fusion to reach $0.01/kWh. Frontier backcasting: start from the target and work backward. Every architectural choice in the pipeline follows from that (Feb 24 and Mar 10 posts). DECISION.

**1costingFE versus fusion-tea.** Two routes to a cost number, and the sources say plainly that this is a trade, not a win:

- 1costingFE commits at design time to what is input and what is derived. It takes power and geometry as separate inputs and, in its own words, "nothing enforces that the geometry you specify can actually deliver the power you ask for." It is JAX end-to-end, so it can back-solve and give exact elasticities. It covers 17 archetypes and four fuels. (`1costingfe/docs/blog/3 Intro/1costingfe-intro-post.md` § What is shaky; paper `1costingfe/docs/papers/1costingfe_paper/1costingfe_paper.tex`.)
- fusion-tea's model route puts the engineering chains in the SysML model, so any quantity can become a study variable, but the model must be fed a solved point. The owner-verbatim product promise: "engineering design parameters can be freely varied, and viability and outcomes (like LCOE) can be assessed... we differentiate from 1costingFE in that we do not embed the engineering logic." (`sysml-codegen/.project/product/0001-design-search-free-variation.md`; the forward-pass versus inverse-solver framing in `.project/concepts/stellarator-mbse-demo.md` § Key Concepts.)
- The bridge is the handshake: the SysML model reproduced 1costingFE account by account to 1e-6 with a two-line itemized remainder (`exploration/stellarator_e2e/HANDSHAKE_REPORT.md`), and then the owner retired the reproduction duty: "we showed we could do it. pin it, or archive those models" (`work/orchestration/stale-basis-recompute.md` § Addendum 2026-08-30). The adapter seam is `1costingfe/src/costingfe/adapter.py`.
- The unresolved tension is recorded honestly: codegen emits forward-only plain Python, so every formula transcribed into SysML moves capability off the substrate that can invert it (`work/backlog/epic-inverse-solving.md`, a framing epic with no work items). HYPOTHESIS.

**Concept exploration and analysis.** The breadth layer: 38 concepts (39 to 41 with splits), an ontology, a per-concept automated analysis pipeline built on 1costingFE, a Concept Explorer, a scoring framework, and a down-select map. This is the Jun 10 post's subject, and Section 5.1 and 5.2 catalog it. RESULT.

**The deep dive relative to colleagues' corridor pursuits.** `~/1cfe/Candidate corridors.md` links six corridor pages: Pulsed Power, Alternate Revenue Streams, "How cheap could p-B11 fusion get, if it works?", the Borealis p-B11 mirror record ledger, the Helion-class pulsed inductive floor, and the Mature Magnetic D-T corridor. Two have repos, and their READMEs describe the method:

- `helion_pulsed_frc_tea` (private): "the down-select's deep dive into the subject of the second 1cFE blog post." A floor hunt built on costingfe, four devices on one architecture differing only in the evidence tier granted (citable records, vendor claims at face value, labelled extrapolations, labelled speculation), six physics-coherence constraints enforced on every quoted point, and costingfe itself extended to support it.
- `borealis_mirror_tea` (private): same shape for a rotating-mirror p-B11 plant. Baseline, tornado, plant-scale scan, best-case waterfall, evidence-tier ladder, recirculating-power scan, and a first-wall wall-load cap closed at every operating point. Ledger at `docs/ledger.md`, narrative at `docs/writeup.md` in that repo.

The stellarator work is the same species of deep dive by a different route. The corridor studies hold the physics in hand-set constraints and evidence tiers inside a costingfe script. The stellarator work puts the physics chains and the constraints in the model, generates the executable, and lets the goal harness run rounds that replace held constants with computed chains and report where the model then refuses. Both end with a fence map and a "what must be true" list. This contrast is the natural framing for the series. [AGENT] reading of the two READMEs and the goal trails.

**Other sibling tools worth one line each** (for a "landscape" paragraph): `fusion-backcasting` (target LCOE as the binding constraint, web tool, Feb 2026, bridged via `1costingfe/src/costingfe/backcasting_bridge.py`); `Tokamak-TEA-Tool` (D-T tokamak sizing from MHD limits to LCOE bounds); `levers` (archetype LCOE lever-stack reference); `tea-models` (first-pass MagLIF and muon-catalyzed models, Mar 2026); `Dipole_Tokamak_LaserIFE_Comparison` (three-concept grid search, Mar 2026); `1costingfe/tex/path_to_1cent.tex` and `1costingfe/docs/analysis/path_to_1cent_fusion_energy.md` (the $42.9/MWh p-B11 mirror baseline and the 4.3× gap).

### 3. Original hypotheses and what happened to them

**Prehistory: m-scout (Sep 2025).** The AI-MBSE vision that became 1cFE's tooling: "models that drive work, not trail behind it," SysML v2 definition versus usage for search-driven optimization, validation functions as gates, and four technical hypotheses (LLM extraction produces reviewable SysML seeds; a dual store beats embeddings-only; MCP-exposed validations make agents predictable; auto-generated TEA code is accurate enough for concept selection). Useful as the origin story and for the "two modes of innovation" framing (accelerate human ideation; search-driven optimization). `~/m-scout/docs/01-vision-overview-ai-mbse-v1.0.md`, `01-vision-overview-product-v1.0.md`, `03-impl-roadmap-product-v0.1.md` § 5. HYPOTHESIS.

**The reframing (Mar 1 to 6, 2026).** From a CATF-lineage MFE model to a broad comparative investigation across all confinement families. `.project/completed/20260306_project-reframing/spec.md`; the resulting scope doc `modeling_project/OVERVIEW.md` with RQ-1 to RQ-5, seven comparison axes, the two-stage process, and V1 done criteria. DECISION.

**The four pipeline hypotheses H1 to H4**, scored twice. The July meta-review found H2 "NOT tested and drifting" because a work item had made 1costingFE the formula source, turning the MFE epic into transcription rather than derivation, and H4 "most important, least validated, scheduled last." A two-week de-risk epic then produced evidence for each. The dossier is the single best source document for a hypotheses-and-evidence post because it states limits as loudly as wins.

| Hypothesis | Status (July 2026) | Evidence |
|---|---|---|
| H1 agents write good SysML through agentic-mbse | Partially validated: bit-exact against an execution oracle, but no independent correctness standard; the validation stack catches none of the "unworkable SysML" traps | `modeling_project/HYPOTHESIS_DOSSIER.md` |
| H2 agents derive behavior from research, not transcribe it | Substantially validated, one family, one probe: blind firewalled derivation matched or beat the answer key on every functional form, found two answer-key bugs, caught two extraction errors | dossier; `work/completed/20260705_WI-016_h2-blind-derivation/comparison.md` |
| H3 SysML v2 captures the relationships a TEA needs | Validated for the arithmetic envelope; the constraint half did not execute at the time (it does now, see 5.5) | dossier |
| H4 codegen plus teax make models executable for exploration | Demonstrated: 11,505-point IFE sweep in 0.1 s | dossier; `docs/demo/closed-loop.html` |

Also: `.project/research/20260704-120000_pipeline-hypothesis-meta-review.md` (the critical review), `.project/reports/epic-pipeline-derisk-demo-progress.md` (the fix epic), and the dossier's 12-row register of findings filed upstream against teax, sysml-codegen, syside, and 1costingFE. HYPOTHESIS and RESULT.

**The two-anchor bet for the stellarator demo.** "A methodology demo is only credible if the model is checked against results it could not have copied." Anchor A (1costingFE handshake) passed 2026-07-25. Anchor B (blind ARIES-CS hold-out with pre-committed pass bands) is still unfired as of 2026-09-04, deliberately, because the owner judged the model not yet worth spending the one irreversible piece of evidence on. Any post must be scoped to this. `.project/concepts/stellarator-mbse-demo.md`, `.project/backlog/epic_stellarator_mbse_demo.md`, `.project/research/20260718-205525_anchor-acceptance-evidence-stellarator-demo.md`. HYPOTHESIS.

**The lean-first hardening bet (ADR-0003).** "Begin with prose files and native facts; harden only on an observed failure." Measured three times in the goal-harness proofs; verdict every time "nothing promoted," with all prose failures caught by cold sessions or fresh reviewers. `.project/adr/0003-lean-first-persistence.md` with its two amendments. DECISION and RESULT.

**The negative result kept as the finding.** The bet that "a bounded task would discover a prerequisite blind" measured false because a need selected for being documented carries its own answer. Retired by owner ruling; the measurement kept. `.project/completed/20260828_goal-research-model-proof/verification_record.md`. RESULT.

### 4. Timeline of the year

fusion-tea: 917 commits from 2026-01-05 to 2026-09-04, with 442 in August alone. The chronological spine for a writer is `.project/completed/CHANGELOG.md` (481 lines).

| When | What | Read |
|---|---|---|
| Dec 2025 to Jan 2026 | agentic-mbse and sysml-codegen bootstrapped; SysML docs corpus and the `NumericalFunctions::sum` discoverability failure; visualization POC | `agentic-mbse/.project/research/20260112-064217_sysmlv2-agent-discoverability-failure.md`; `.project/completed/20260306_epic_visualization-poc.md` |
| Jan to Feb | Cost patterns de-risking; solar plus battery end-to-end LCOE $288.68; Zotero ingestion; expression-aware codegen; first e2e bug wave (19 bugs, 42% naming) | `.project/completed/20260306_epic-end-to-end-pipeline-derisking.md`; `sysml-codegen/.project/research/20260217-030000_mistakes-and-learnings-since-a6310a4b.md` |
| Feb | agentic-mbse architecture redesign (four epics, PM engine); PDF extraction v2, v3, v4 in three weeks | `agentic-mbse/.project/concepts/toolkit-redesign.md`; `agentic-mbse/docs/extraction-internals.md` |
| Mar 1 to 6 | Project reframing; full-workflow demo epic (taxonomy, IFE model, explainer) | `.project/completed/20260306_project-reframing/spec.md` |
| Mar 10 | Methodology blog post published | live |
| Mar to Apr | Phases 1a to 2a on the concept table; taxonomy and explorer; automated concept analysis; source-acquisition provenance investigation | `exploration/phase_1d/report.md`; `.project/concepts/source-acquisition-investigation.md` |
| May | Scoring v2/v3, down-select, ontology v3, score explorer reviews | `.project/research/20260517_ontology_v3_delta.md`; `docs/demo/down-select.html` |
| May 30 to June | Concept-analysis rework (one named plant, then 1 GWe NOAK projection); explorer UX v3; explorer web hosting; 1costingFE v0.1.0 release (Jun 26) | `.project/concepts/concept-analysis-rework.md`; `1costingfe/docs/blog/3 Intro/` |
| Jul 4 to 5 | Pipeline de-risk: H1 to H4 probes, first generated pipeline run through teax, IFE closed loop, DI-006 corruption found | `.project/reports/epic-pipeline-derisk-demo-progress.md` |
| Jul 10 to 20 | Constraint execution ratified across three repos; teax evaluator and crash-safe study layer; stellarator demo grounded; ARIES-CS sealed | `sysml-codegen/.project/concepts/constraint-execution-authoritative-lifecycle-contract.md`; `teax/.project/CONSTRAINT_EXEC_PR_BODY.md`; `knowledge/holdout/aries-cs/PROTOCOL.md` |
| Jul 18 to Aug 2 | Six orchestration briefs: magnet field erratum, recirc power, stale basis, constraint execution demo, two handshake items; Anchor A met | `work/orchestration/*.md`; `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` |
| Aug 7 to 19 | sysml-codegen elaborate-first rebuild ("we are solving the wrong problem"); stop-reinventing-the-parser | `sysml-codegen/.project/research/20260807-145336_elaborate-first-instance-graph-architecture.md` |
| Aug 16 to 23 | Proof-of-life design search; run-study skill; two A/B studies; stellarator migration to a sealed stock package; bulk archival | `exploration/stellarator_e2e/study/synthesis.md`; `.project/concepts/run-study-skill.md` |
| Aug 20 | Stop-parser shipment: three-repo merge-commit wave, immutable tags, sealed wheels, provenance test | `sysml-codegen/.project/CURRENT_WORK.md`; `tests/test_dependency_provenance.py` |
| Aug 23 to 30 | Goal Strategy and Task Harness epic: contract, research seam, integration seam, cold-pickup proof, research-to-model proof, route equivalence; product ledger entry 0001; REPO-CLEANUP in sysml-codegen | `.project/completed/20260830_epic_goal_strategy_task_harness.md`; `sysml-codegen/.project/backlog/epic_repo_cleanup.md` |
| Aug 26 to Sep 4 | Seven goals run: cryo volume, p-pump basis, p-pump fence, magnet closure, operating-point closure, priced levers, wall and heating; depth rubric re-grades; narratives | `work/orchestration/goals/*/`; `work/narratives/` |

Status snapshots that read as state-of-the-project essays: `.project/reports/2026-07-03-1114-status-report.md`, `2026-07-25-0835-status-report.md`, `2026-08-21-1339-status-report.md`, `2026-08-30-0900-status-report.md`, and `.project/CURRENT_WORK.md`.

### 5. Catalog by theme

#### 5.1 Concept space: taxonomy, ontology, reasoning tree, scoring, down-select

| Topic | Summary | Read | Type |
|---|---|---|---|
| Context-dependent design spaces | The founding claim: fusion's design space is not a grid; each choice reshapes which downstream questions exist. Tested empirically by N/A density and generative coherence | `exploration/context/context_dependent_design_spaces.md`; `exploration/sprint_plan.md` | HYPOTHESIS |
| Phase 1a differentiation table | 38 concepts by 12 cited columns, every cell filled, N/A, or TBD with a reason | `exploration/phase_1a/` (`CONCEPT_ONTOLOGY.md`, `table.csv`, `schema.md`) | METHOD |
| Phase 1b: two columns identify 37 of 38 | Brute-force over all column subsets showed "Confinement Concept" was a disguised ID column | `exploration/phase_1b/report.md` | RESULT |
| Phase 1b v2: the hierarchy | Replacing it with an 8-column tree moved N/A density 9.6% to 36.7% monotonically, the empirical signature of a context-dependent space | `exploration/phase_1b_v2/report.md` | RESULT |
| Phase 1d: classification scheme, not design space | 0 of 30 random rows physically coherent; about 2 effective degrees of freedom from 18 columns | `exploration/phase_1d/report.md` | RESULT |
| Phase 2 concept and its self-review | Three framings (subsystems, seven primitive requirements P1 to P7, force-resolution cascades), then a review that kills its own proposal | `exploration/phase_2_concept.md`; `exploration/phase_2_concept_review.md` | METHOD |
| Constraint propagation with ATMS | Variables, domains, constraints, minimal justification sets; a working spike and an interactive demo; honest review that constraint authoring, not computation, is the wall | `exploration/algorithm_ideation.md`; `exploration/spike_constraint_atms.py`; `exploration/spike_review.md`; `docs/demo/constraint-propagation.html` | METHOD |
| Reasoning tree (Phase 2a) | Derive concepts from six universal requirements instead of classifying known ones; L0 five options, 22 constraints, all unmappable to table columns | `.project/concepts/reasoning-tree-formal-model.md`; `exploration/phase_2a/report.md`; `.project/concepts/framework-agent-prompt.md` (the prompt that produced the formal model) | HYPOTHESIS |
| Ontology v3 | Flat columns to a three-level tree with nine descriptor bands; the renumbering silently miscategorized eight concepts, which produced the "classify from architecture, never ID prefixes" rule | `.project/research/20260517_ontology_v3_delta.md`; the figure `concept_ontology_v3.png` in the Jun 10 post | DECISION |
| Scoring v2 and v3 | Features, deterministic embeddings, weight-driven scores as three inspectable layers so a dispute localizes; seven axes in v3 | `.project/concepts/scoring-framework-v2.md`; `.project/completed/20260821_scoring-v3-rewrite/design.md`; `exploration/scoring_v2/weights/default.yaml` | METHOD |
| Triple-product technology-risk framework | Uniform physics-risk comparison across MCF, ICF, MIF via the generalized Lawson parameter with three disputable gaps | `.project/research/20260515-143425_triple-product-technology-risk-framework.md` | METHOD |
| Down-select map | Four-stage technology journey; cohort effects (about eight concepts need REBCO, eight need cryo target fab, four need pulsed-power capacitors); "we don't gate on physics" | `docs/demo/down-select.html`; `.project/concepts/concept-trace.md` | DEMO |
| Score explorer and its adversarial reviews | The public ranking tool, plus two large critical reviews including a pairwise-inconsistency sweep | `docs/index.html`; `.project/reports/2026-05-29-score-explorer-critical-review.md`, `-pairwise-inconsistencies.md` | RESULT |
| The spanning-set draft | Mallory's draft of the concept-selection post, with the corridor links | `~/1cfe/Candidate corridors.md` | NARRATIVE |

#### 5.2 The concept-analysis pipeline (38 concepts on 1costingFE)

| Topic | Summary | Read | Type |
|---|---|---|---|
| The filesystem is the state machine | No orchestrator, no database; a concept's state is the files in its directory; every feedback producer emits the same verdict schema so humans and agents are interchangeable | `docs/concept-pipeline/pipeline.md` (75 lines, near blog-ready); `outline.md`; `actual-mechanics.md` (reference) | METHOD |
| The five-case dispatch | What drives the next pass: cold start, reviewer kick-back, new sources, autonomous research, prior assessment; two one-shot rules stop re-integration | `docs/concept-pipeline/actual-mechanics.md`; `docs/concept-pipeline/diagrams/dispatch.svg` | METHOD |
| The 2306-line monolith refactor | Fourteen subcommands that were really three kinds of command | `.project/research/20260405-concept-analysis-refactor.md` | RESULT |
| `/manage-concept` operator console | Adapts to the stage the concept is in and never edits artifacts directly | `.claude/commands/manage-concept.md`; `docs/concept-pipeline/outline.md` | TOOL |
| Autonomous source acquisition | Budgeted research agent with an audit log and per-run cost caps | `.project/concepts/autonomous-source-acquisition.md` | TOOL |
| The Haiku-paraphrase provenance scandal | Every "exact quote" in early sources was a summarizer's version, because the fetch tool never showed the agent the raw page; 21 files re-sourced | `.project/concepts/source-acquisition-investigation.md` | RESULT |
| Concept-analysis rework: "what plant are we specifying?" | Per-concept LCOEs were stitched from disagreeing sources; the rework specifies one named plant at native scale, then projects to 1 GWe NOAK with a two-knob call; overrides become a six-field registry | `.project/concepts/concept-analysis-rework.md` (Key Concept 6 on the replication floor); `.project/reports/2026-05-30-1gw-scaling-and-override-interpretation.md`; `2026-06-06-1gw-estimate-policy.md` | DECISION |
| Explorer UX v3: three different LCOE functions | The slider, tornado, and headline described different functions; a half-percent nudge dropped concept 01 from 155.17 to 127.53 $/MWh; fix is one override toggle; thesis "traceability is the product" | `.project/backlog/epic_explorer_ux_v3.md`; `.project/research/20260605-150329_concept-explorer-ux-user-journeys.md` | RESULT |
| Staleness propagation | A stale stamp that carried zero information, fixed by making set and clear conditional | `.project/concepts/staleness-propagation.md` | METHOD |
| Validation spot checks | Expert deep-dive comparisons against pipeline output (PacFusion MagLIF, Realta mirror, OpenStar dipole, Xcimer) | `exploration/concept_analysis/validation_reviews/` | RESULT |
| Known limitations on record | Modularity scaling penalty, non-standard freeform concepts, limited physical consistency checks | Jun 10 post § Known Limitations; `.project/concepts/concept-analysis-rework.md` | DECISION |
| Explorer architecture and bake-off | Nine approaches, three rounds of critique; the real decision was the computation layer | `.project/concepts/concept-analysis-ux-tool.md` (boxed summary at top); `.project/designs/concept-explorer-architecture.md` | DECISION |
| Open CLI bugs | `analyze` and `model-setup` presented as peers when one runs the other; dry-run writes two of three prompts | `.project/active/run-analysis-cli-step-semantics/spec.md`; `.project/active/loop-dry-run-symmetry/spec.md` | RESULT |

#### 5.3 Knowledge and sources (the indexing and extraction tools)

| Topic | Summary | Read | Type |
|---|---|---|---|
| PDF extraction v1 to v4 | v1: an autonomous agent loop grew a pipeline from 57 to 797 lines with no quality gain and 170 lines of regex in one function, then 97 commits abandoned. v2: 2.68/5 to shippable in three days, then 0 of 5 usable on unseen documents. v3: Claude as the structural backbone. v4: per-page quality-gated routing, 8% table error at $0.12/doc, 12× cheaper than full-Claude, built by a four-stage tool-deep-dive method | `agentic-mbse/.project/research/20260213-180000_bart-loop-process-learnings.md`; `agentic-mbse/.project/concepts/pdf-extraction-v2.md`, `pdf-extraction-v3-strategy.md`, `doc-extraction-development-strategy.md`; `agentic-mbse/docs/extraction-internals.md` (the shipped machine and its named design decisions) | RESULT and METHOD |
| The extraction corpus | 14 PDFs, ground truth for seven, about 60 named experiment runs | `agentic-mbse/tests/corpus/` | METHOD |
| Where the quality gate is blind | Six of twelve pages mis-routed with only $0.45 of $2.00 spent: "the gate was never designed to catch these" | `agentic-mbse/.project/research/20260227-210000_extraction-quality-failures.md`; `agentic-mbse/.project/backlog/epic_pdf-extraction-improvements.md` | RESULT |
| Web and arXiv capture | Sanitized HTML via trafilatura with a Pandoc path for arXiv; raw-bytes SHA-256 in frontmatter | `agentic-mbse/src/agentic_mbse/extraction/web_backend.py`; `agentic-mbse/.project/research/20260328-web-source-capture-integration.md` | TOOL |
| Zotero ingestion | Batch ingestion from a Zotero group library (166 items, 130 PDFs at the time) through the extractor | `scripts/zotero_ingest.py`, `zotero_lib.py`; `.project/research/20260302-zotero-library-capabilities-and-demo-strategy.md` | TOOL |
| The source registry as the one write door | Staging, provenance verification, dedupe, a commit ladder under a lock, receipts; the hold-out guard fails closed and has no waiver flag | `scripts/source_registry.py`; `scripts/holdout_guard.py`; `docs/research_seam_operator_guide.md`; `.project/research/20260822-120756_research-extraction-harness.md` | TOOL |
| The research seam | A bounded request with search and capture limits, receipts on disk, four return classes computed from receipts rather than agent claims | `scripts/research_seam.py`; `knowledge/research/requests/REQ-*.json` and `runs/` | PROCESS |
| SOURCE_INDEX | 33 registered sources with Type, Location, Use for, Validation, Caveat, raw and extract SHA-256; the pattern everything else copied ("design for 0, 1, or N") | `knowledge/SOURCE_INDEX.md`; `agentic-mbse/docs/source-index.md`; `agentic-mbse/.project/research/20260130-235423_information-role-taxonomy.md` | TOOL |
| Domain insights DI-XXX and the approval pipeline | Research is staged in `pending/`, approved by a human, and only then yields insights; DI-008 was later amended in place by a goal with the reasoning retained | `knowledge/KNOWLEDGE.md`; `knowledge/research/approved/`; `agentic-mbse pm approve-research` | PROCESS |
| The durable traceability chain | DI to PR to model element to authority source, each a durable artifact | `.claude/skills/source-traceability/SKILL.md`; `modeling_project/REQUIREMENTS.md` MR-4 | METHOD |
| Traceability audit still unbuilt | The spec cites `scripts/trace_audit.py` as the enforcement mechanism and the script does not exist; a clean essay about aspirational versus scriptable requirements | `.project/active/traceability-system/spec.md` | DECISION |
| The DI-006 dropped digit | A leading "2" lost from every figure in an insight, propagated for four months into the meta-review | `.project/reports/epic-pipeline-derisk-demo-progress.md`; dossier H1 | RESULT |
| The concept-research corpus and image protocol | 38 dossiers, git for markdown and R2 for binaries, three quality tiers with an authority order, and the rule that tables and equations must be read from page images because text extraction is lossy | `knowledge/concept_research/README.md`; `.claude/skills/concept-research-navigation/SKILL.md`; `scripts/sync_research.sh` | METHOD |
| The ARIES-CS hold-out protocol | Four papers sealed by checksum and page count only; a clean room that bars ARIES-informed artifacts too; a contamination inventory that discloses training-data priors as irreducible; the 2026-08-30 clean-room split | `knowledge/holdout/aries-cs/PROTOCOL.md` §§ 3, 5, 6, 8; `.project/research/20260712-aries-cs-quarantine-leak-surfaces.md`; `tests/research/test_holdout.py` | PROCESS |
| Meta-analysis corpus | 18 non-fusion economics and deployment documents (FOAK financing, learning rates, megaprojects) with section indexes | `knowledge/meta_analysis/` | TOOL |
| Document indexing over chunking | For grep-based retrieval with a large context window, structured section indexes beat chunking | `agentic-mbse/src/agentic_mbse/extraction/index.py`; `agentic-mbse/.project/completed/epic_documentation-discoverability.md` | DECISION |
| Source identity is raw-bytes SHA-256 | | `.project/adr/0008-source-identity-raw-bytes-sha256.md` | DECISION |

#### 5.4 The modeling layer (agentic-mbse and the SysML models)

| Topic | Summary | Read | Type |
|---|---|---|---|
| Why SysML v2 | Definition versus usage; textual notation unlocks git and coding agents; SysIDE as the parser | Mar 10 post; `~/m-scout/docs/01-vision-overview-ai-mbse-v1.0.md` | DECISION |
| Library versus designs | Concept-agnostic definitions in `models/library/`, concept-specific instances in `models/designs/`; 25 files today, catalog with per-file purpose | `models/README.md`; `modeling_project/REQUIREMENTS.md` MR-3 | METHOD |
| Architecture decisions AD-001 to AD-007 | Plain `Real` with units in doc comments; the Economic Parameter attribute; closed-form DCF because calc defs cannot loop; CAS accounts as typed part defs | `modeling_project/ARCHITECTURE.md` | DECISION |
| The 6-level validation stack, and the audit of it | Syntax, structure, dataflow, constraint coverage, traceability, architecture. The self-audit found L4 and L5 were stubs and the blog "overpromised on three of six levels," which drove the 8-to-6 restructuring | `agentic-mbse/src/agentic_mbse/validation/`; `agentic-mbse/.project/research/20260227-195415_validation-stack-audit.md`; `.claude/skills/model-validation/SKILL.md` | RESULT |
| The subtype-enumeration bug | The dependency graph was always empty, so the circular-import check always passed | `agentic-mbse/docs/subtype-enumeration-decision-table.md` | RESULT |
| The verification registry SV-001 to SV-052 | 52 criteria with type, mechanism, expected value, tolerance, and status; several rows are narrative records of a criterion being flagged, source-checked, and parked | `modeling_project/VALIDATION_MATRIX.md` | PROCESS |
| The agentic modeling workflow | spec, design, plan, implement, audit; a specification agent with the full language spec; review agents at the end of design and implement | `agentic-mbse/claude/commands/`; the 15 commands, 10 skills, and 5 agents listed in `agentic-mbse/CLAUDE.md` | PROCESS |
| The architecture redesign | Commands of 1,345 lines embedding shared knowledge, PM state living in agent memory; rebuilt as commands under 300 lines that reference skills, plus a deterministic PM engine | `agentic-mbse/.project/concepts/toolkit-redesign.md`; `agentic-mbse/.project/research/20260130-234525_agentic-mbse-pipeline-critical-analysis.md` | DECISION |
| Frontmatter as the database | Work-item state is derived from the filesystem and YAML frontmatter, never declared by an agent; mutations run through scripts | `agentic-mbse/src/agentic_mbse/pm/`; `agentic-mbse/.project/completed/epic_architecture-pm-engine.md` | METHOD |
| The SysML pattern library and expert agents | 13 pattern docs; the `NumericalFunctions::sum` discoverability failure that produced the specialist agents | `agentic-mbse/docs/patterns/`; `agentic-mbse/.project/research/20260112-064217_sysmlv2-agent-discoverability-failure.md` | METHOD |
| The IFE model and its target selection | Why a generic driver-agnostic IFE model on Hawker's 14-parameter framework came first | `modeling_project/intent/IFE Modeling Target Selection.md`; `models/designs/generic_ife/`, `hif_ife/` | DECISION |
| The stellarator model | Stellaris (concept 09) plant model plus the MFE library; the exploration twin with an anti-drift test | `models/designs/stellarator_09/stellarator_plant.sysml`; `models/library/analyses/mfe_*.sysml`; `exploration/stellarator_e2e/STAGED_MODELS.md` | METHOD |
| Study policy for model authors | Inequality constraints cut a region; equalities asserted over swept inputs drop a dimension and produce a manifold a grid never lands on. The axis rule, a four-rung resolution ladder for cycles, six anti-patterns | `modeling_project/STUDY_POLICY.md` | DECISION |

#### 5.5 Execution: sysml-codegen, teax, and the handshake

| Topic | Summary | Read | Type |
|---|---|---|---|
| What sysml-codegen is | SysML v2 text to a runnable Python package for teax: parse, elaborate, seal, project, render, seal the package. One public entry point | `sysml-codegen/README.md`; `sysml-codegen/CLAUDE.md`; `sysml-codegen/docs/architecture/overview.md` (ASCII pipeline diagram at lines 11 to 43) | METHOD |
| Expression-aware codegen | "100 lines of scaffolding for one line of math" ended by compiling SysML expressions to Python; 15 of 15 and 19 of 21 calc defs auto-implemented | `sysml-codegen/.project/concepts/expression-aware-codegen.md`; `sysml-codegen/.project/research/20260202-180000_expression-compilation-and-inline-math-strategy.md` | RESULT |
| The first bug wave | 19 bugs across seven root-cause reports, 42% naming failures | `sysml-codegen/.project/research/20260217-030000_mistakes-and-learnings-since-a6310a4b.md` | RESULT |
| Elaborate-first ("we are solving the wrong problem") | The library had never performed SysML elaboration; it simulated it after the fact in about 3,400 lines of string-identity guessing. Rebuilt as elaborate-then-project with no compatibility layer. The pivot document of the year for this repo | `sysml-codegen/.project/research/20260807-145336_elaborate-first-instance-graph-architecture.md`; `sysml-codegen/.project/adr/0005-exact-identity-elaboration-replaces-string-resolution.md` | DECISION |
| Source identity | One modelled value occurrence resolves to exactly one runtime source; an arrayed child is enumerated, not multiplied; an unresolvable reference is a typed refusal | `sysml-codegen/.project/product/0002-exact-owner-anchoring.md`; `sysml-codegen/.project/adr/0004-...` | METHOD |
| Snapshots and sealing | A v6 instance-graph snapshot lets generation run without the parser license; a semantic contract and a physical package contract with an emitted verifier | `sysml-codegen/docs/architecture/reference/27-snapshot-generation.md`, `29-contracts-and-sealing.md` | METHOD |
| Constraint execution | `assert constraint` used to be recognized, classified, and reported as dropped; now each becomes a module emitting satisfied, violated, or indeterminate, rolled into one report. A false predicate is data, not an exception. Layer split: agentic-mbse owns meaning, codegen owns lowering, teax owns execution, the study owns policy | `sysml-codegen/.project/concepts/constraint-execution-authoritative-lifecycle-contract.md` (ratified 2026-07-19, the authority across three repos); `sysml-codegen/.project/research/20260710-095634_...`; `teax/.project/reference/constraint-execution-concept.md` ("silence must stop being a possible outcome") | DECISION |
| Coverage truth | "Full satisfaction is a coverage claim": a package never reports all-satisfied while authored gates went unassessed; teax retired `all_satisfied` and refuses older packages at load; `partial_coverage` is kept for the boundary but not fed to the search | `sysml-codegen/.project/product/0005-...`; `teax/docs/evaluation-and-study.md` | DECISION |
| Constraint facts, ExpressionIR, executable profile | The neutral seam between the two repos: facts not decisions; references carried unclassified; four outcomes admit, block, non-numerical, unassessed, and "silence is never an outcome" | `agentic-mbse/docs/constraint-facts-and-expression-ir.md` | METHOD |
| Stop reinventing the parser | Use SysIDE as the authority; refuse rather than re-derive; a closed failure vocabulary; the three-repo merge-commit shipment with four immutable tags, a sealed evidence child that never merges, byte-identical wheels, and a provenance test | `sysml-codegen/.project/CURRENT_WORK.md` lines 30 to 110; `git show da15f14:.project/completed/20260820_stop-parser-pr-shipment/plan.md` in sysml-codegen; `tests/test_dependency_provenance.py`; `~/1cfe/stop-parser-sealed-wheels/` | RESULT |
| REPO-CLEANUP: keep the decisions, delete the exhaust | `.project/` was 78% of the repo and one lint log was committed ten times; production code was well-factored (2% duplication). Close now means record, then delete; git history is the archive | `sysml-codegen/.project/backlog/epic_repo_cleanup.md`; `sysml-codegen/.project/research/20260820-201945_line-count-anatomy-and-salvageability.md` | DECISION |
| The repo boundary | agentic-mbse owns neutral facts, codegen owns rendering, one-way dependency; "a boundary move is byte-faithful or it is a behavior change" | `sysml-codegen/.project/adr/0007-...`; `sysml-codegen/.project/concepts/agentic-mbse-push-down-design.md` | DECISION |
| What teax is | A typed, YAML-declared pipeline runtime: Pydantic modules, channels, graph validated before running; the RootModel asymmetry; entry and exit points | `teax/README.md`; `teax/docs/rootmodel-and-primitives.md`; `teax/.project/concepts/exitpoint-persistence-contract.md` | METHOD |
| The evaluator and the study layer | Loads a sealed package by path, never imports a generated class name, one case per call, evidence projected off duck-typed attributes; studies with strategy, bridge, and policy; SQLite with WAL, content-addressed evidence, a fenced single-writer lease, crash tests with real process kills; explicit non-claims (no sandbox) | `teax/docs/evaluation-and-study.md`; `teax/.project/CONSTRAINT_EXEC_PR_BODY.md` | METHOD |
| teax explainer | "How TEAx works: from typed modules to durable studies," with three SVG diagrams and inline limits | `teax/docs/teax-study-explainer.html` | DEMO |
| The solar plus battery first run | 36 modules through teax, 11 of 11 assertions at 1e-12, the first generated pipeline ever executed end to end | `exploration/pipeline_spike/`; `.project/reports/epic-pipeline-derisk-demo-progress.md` | RESULT |
| The IFE closed loop | Three anchors reproduced bit-exactly; 11,505 points in 0.1 s; the viability knee at driver efficiency times gain of 10 | `docs/demo/closed-loop.html`; `docs/demo/closed-loop-story.md`; `exploration/ife_e2e/` | RESULT |
| The 1costingFE handshake | 30-plus accounts under 1e-6 with a two-line itemized remainder; float32 as the binding floor; the IDC convention kept as a mapped channel by owner ruling | `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`; `work/orchestration/handshake-account-scope.md`, `handshake-lcoe-construction.md`; `1costingfe/src/costingfe/adapter.py` | RESULT |
| Codegen findings from the stellarator | A second independent round of upstream findings | `exploration/stellarator_e2e/CODEGEN_FINDINGS.md`; `.project/reports/2026-07-05-upstream-findings-register.md` | RESULT |
| The migration to a sealed stock package | Regenerated at runtime contract 2.0.0 with numerical identity preserved across a 948-point grid; the merge plan with three conflicts and three new refusal classes | `.project/research/20260820-221835_stellarator-demo-reconciliation-plan.md` | RESULT |

#### 5.6 Studies: turning a package into evidence

| Topic | Summary | Read | Type |
|---|---|---|---|
| Study-driven model development | A model can be point-faithful (bit-exact at its design point) and not space-faithful; "a naive sweep produces smooth, plausible, silently wrong maps"; adaptivity lives between studies | `.project/concepts/study-driven-model-development.md` | HYPOTHESIS |
| Failure classes A, A', B and input fan-out | Code faithful at the anchor but wrong elsewhere; one SysML attribute reaching two entry keys so a sweep manufactures an inconsistent point | `.project/research/20260725-110828_study-failure-classes-and-mechanisms.md` | METHOD |
| The run-study skill | Fifteen execute obligations; indicators for every proposed axis before any point runs; "an unresisted axis is a model-underdevelopment finding, not a study"; a fresh administrator reads only the record | `.claude/skills/run-study/{SKILL.md,runbook.md,record-template.md}`; `.project/concepts/run-study-skill.md` | PROCESS |
| The record contract | Born from the proof-of-life synthesis listing 20 facts the study directory could not support; "an unrecoverable fact is a defect in the contract" | `exploration/stellarator_e2e/study/synthesis.md` § 6; `tests/study/test_records.py` | PROCESS |
| The discovery log | Append-only, one row per sighting, joined by id, every touched row dispositioned, never mint an id | `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`; `.project/adr/0004-finding-disposition.md` | PROCESS |
| The study tools | identity, indicators, manifest, preflight, verify | `scripts/study/` | TOOL |
| Proof-of-life design search | 948-point (R, a) grid, 59% feasible, wall load the active fence, best feasible 209.00 | `exploration/stellarator_e2e/study/report.html`, `synthesis.md` | RESULT |
| Power-cycle A/B | sCO2 versus Rankine: efficiency worth −14.4%, equipment rates −0.8%, ordering never reverses | `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md` | RESULT |
| Magnet-technology A/B | Nb3Sn cheaper at all 4,144 points and feasible at none; the pathology that nothing rewarded field, which drove the next month | `.../20260823-magnet-technology-ab/record.md`; `.project/active/run-study-first-consumer/briefs/` | RESULT |
| p-pump fence | +21.0% LCOE; the fence grows from a corner to a band; the CAS10 square-root crash | `.../20260829-p-pump-fence/record.md` | RESULT |
| Stress fence | Winding-pack stress binds for R above 16.5 m once field is derived | `.../20260830-stress-fence/record.md` | RESULT |
| Sustainment fence | At the printed 50 MW heating nothing is feasible; at 110 MW a region appears whose best point beats the baseline despite buying 2.2× the heating, off the beta floor | `.../20260901-sustainment-fence/record.md` | RESULT |
| Priced levers | Pack current density moves cold volume and cryoplant but magnet capital by exactly zero; freeing temperature overturns the previous round | `.../20260903-priced-levers/record.md` | RESULT |
| Wall and heating | Two efficiency experiments with opposite signs; the apparent optimum survives only under a wall check known to be wrong | `.../20260903-wall-and-heating/record.md` | RESULT |

#### 5.7 The goal harness (agents plus coordination)

| Topic | Summary | Read | Type |
|---|---|---|---|
| The problem it solves | Three working entry points forming a loop that "had run exactly once, by hand"; owner expectation that 95% of study-shaped goals return "we need to revisit the model" | `.project/concepts/goal-driven-model-development-harness.md` | HYPOTHESIS |
| The runbook | One procedure for humans and agents; states obligations, never decisions; not a plan, not a control plane, not an automation of owner judgment | `work/orchestration/GOAL_RUNBOOK.md` (281 lines, read whole) | PROCESS |
| The five surfaces | goal.md written once; trail.md append-only; learnings.md proposed by the result and accepted by the review; the runbook; the ADRs | runbook § The five surfaces; `work/orchestration/goal-templates/` | PROCESS |
| The roles | Operator, round agent, fresh reviewer, study executor, study administrator, grader | `.claude/skills/run-goal/SKILL.md` | PROCESS |
| Grounding and the five field classes | A goal hollow in any of five classes authorizes no task; promoted after a cold-session probe measured agents running full tasks on hollow goals | runbook § Grounding; `.project/completed/20260827_goal-cold-pickup-proof/gate-probe-record.md` | DECISION |
| One task, six outcomes | Six-line scope before work, a start line before the first side effect, outcomes COMPLETE, BOUNDED_NEGATIVE, PREREQUISITE, STRATEGY_BLOCKER, OWNER_GATE, MECHANICAL_FAILURE; "a scope that lists its own prerequisites is a plan" | runbook § One task | PROCESS |
| Fresh means a session boundary | "The critic is never the author's session"; an agent cannot spawn a session, so it stops and hands back | runbook; `work/orchestration/goals/priced-levers/evidence/round1_handoff_20260903.md` | DECISION |
| The pre-execution disposition checkpoint | PASS or REVISE, cap two revisions, "the cap stops the work; it does not release it" | `.project/adr/0005-review-topology.md` | PROCESS |
| The fresh round review | Checks every citation, scope drift, retry classification, every touched discovery row, and the learning delta; never resumes the round; writes the next strategy | runbook § Review | PROCESS |
| Disclosed, never tuned | "'Made honest' is not 'made looser.' The limit is not moved to open a region." Live instance: 4.087 against a 4.05 limit | `work/orchestration/goals/wall-and-heating/goal.md` § Answered when | DECISION |
| Fences | Vocabulary for the boundary where a modeled constraint stops being satisfied; the held-axis pitfall | `work/orchestration/goals/priced-levers/learnings.md` L-003 | METHOD |
| The ten ADRs | One authority unit per round; fresh review authors the next strategy; lean-first persistence; finding disposition; review topology; the evidence seam between PMs; supersession; source identity; integration as a fixed-point proof; the oracle mirrors audited bindings | `.project/adr/INDEX.md` | DECISION |
| The native seams | research, model, integrate, study.execute, study.read; two were repaired mid-project and their runbook rows flipped only on live evidence | runbook § The native seams; `docs/integration_seam_operator_guide.md` | PROCESS |
| The integration seam | Ten ordered gates, one CANDIDATE or one BLOCKER, never both, refused distinguished from could-not-run | `scripts/integrate.py`; `.project/adr/0009-integration-is-a-fixed-point-proof.md` | TOOL |
| The five GSTH proofs | Cold pickup (13 sessions, 12 fresh agents, a real mid-task kill and resume, "not exercised as designed, not as a pass"); research-to-model (the critic bound on a live round for the first time); route equivalence (the seam refused four times before one CANDIDATE; hand and agent routes byte-identical; the product lens blocked on one over-claim) | `.project/completed/20260830_epic_goal_strategy_task_harness.md`; `.project/completed/2026082{7,8}_goal-*-proof/verification_record.md`; `.project/completed/20260830_goal-integration-study-proof/route_equivalence.md` | RESULT |
| The product promise | Exactly one: "A non-builder runs a goal round from the runbook and native records alone," with three declared limits | `.project/product/0001-goal-round-native-operability.md` | DECISION |
| The goal-contract tests | Thirteen tests that make the runbook enforce itself | `tests/orchestration/test_goal_contract.py` | TOOL |
| The seven goals as one story | Cryo volume (bounded negative), p-pump basis (100× understatement), p-pump fence (+21%), magnet closure (field computed to 1 ulp; rubric rows move), operating-point closure (no feasible point at 50 MW; field finally rewarded), priced levers (magnet capital moves by exactly zero; closed by redirect), wall and heating (opposite signs; the wall check exposed) | `work/orchestration/goals/*/{goal,trail,learnings}.md`; summaries in `work/narratives/` | RESULT |
| The depth rubric | Two 0 to 4 ladders per subsystem (physics self-consistency; structural and costing depth), never averaged, targets per row, written blind; the re-grade series is the measured trajectory | `.project/active/demo-depth-rubric/{rubric,gap-report,grading*}.md`; `.project/research/20260830-141348_demo-depth-rubric-design-evidence.md` | METHOD |
| Demo maturation | The owner declined to fire the blind comparison on a one-deep model and operationalized "ARIES-level quality" against the class of study without reading the sealed instance | `.project/concepts/stellarator-demo-maturation.md` | DECISION |
| Two agent notes hardened into fake owner rulings | A scope note in a doc comment became a "reserved gate" that blocked two rounds; "nothing is sacred here" | `.project/concepts/stellarator-demo-maturation.md` § Corrections 2026-09-01 | RESULT |
| The orchestration briefs (pre-goal-layer) | Six immutable briefs with graded decision inputs, the earlier generation of the harness | `work/orchestration/{magnet-field-errata-B9,recirc-power-derivation,stale-basis-recompute,demo-constraint-execution,handshake-account-scope,handshake-lcoe-construction}.md` | DECISION |
| Narrative snapshots | Eight fixed sections, an authority disclaimer, a cutoff SHA, a review-status line, and an evidence-and-visual index that reads as a figure brief | `.project/concepts/goal-narrative-snapshots.md`; `.claude/skills/narrate-goal/SKILL.md`; `work/narratives/20260904-184254Z-*.md` | NARRATIVE |
| Two PMs, one evidence seam | Coding PM and modeling PM each mutated only through their own operations; citing by path and digest is not mirroring | `CLAUDE.md` § Two Systems; `.project/adr/0006-goal-evidence-seam.md` | DECISION |

#### 5.8 How it is working: process failures caught and corrected

This is the strongest external material because in every case the mechanism that caught the error is nameable and the correction is on the record.

| Failure | What caught it, and the fix | Read |
|---|---|---|
| A bot-check page registered as a paper | The research return named it; the registry has no unregister, so it was left in place with a caveat and a backlog item | `knowledge/SOURCE_INDEX.md` (both entries); `work/orchestration/goals/wall-and-heating/evidence/T-001_research_return.md`; `.project/backlog/BACKLOG.md` § Flagged |
| A study ran with no scope or start line | Reconstructed after the fact and marked; a fresh administrator's recount found five prose misstatements; learning L-006 | `work/orchestration/goals/priced-levers/learnings.md` L-006; `work/orchestration/goals/priced-levers/trail.md` lines 183 to 198 |
| A held axis silently decided a fence conclusion | The pre-execution critique caught it before a point ran; sweeping temperature improved the optimum by 16.645 $/MWh | `work/orchestration/goals/priced-levers/evidence/T-007_precritique.md`; `learnings.md` L-003 |
| Extraction artifacts in the machine's own source, three generations | A phantom Table 3 row (5.86 T) in July; a phantom 4.95 peak and an r = 1.5 m torus in September. Rule: table values are verified against page images | `work/orchestration/magnet-field-errata-B9.md`; `work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md` |
| The hold-out screen fired after the fetch | A research subagent had already read an ARIES-CS result; fix moved the screen into the instruction; next run refused a Helios versus HELIAS homograph without fetching | `work/orchestration/goals/priced-levers/learnings.md` L-005; `work/orchestration/goals/wall-and-heating/learnings.md` L-008; `knowledge/research/requests/runs/REQ-WALL-02/` |
| Five stale expectations, four mechanisms | The fifth was found by a person reading the annex for another reason | `work/orchestration/goals/p-pump-fence/learnings.md` L-001 |
| The silent blank column, four sightings | Four recorded repeats bought one guard, exactly as the hardening rule requires; root cause spans teax and the exporters | `work/orchestration/goals/wall-and-heating/learnings.md` L-005; `.project/backlog/BACKLOG.md` § Flagged |
| "New" claims that were not new | Three of a work item's claimed novelties cut back at the checkpoint | `work/orchestration/goals/wall-and-heating/learnings.md` L-004 |
| The false R-independence claim | Caught by the fresh checkpoint before it reached the next goal | `.project/CURRENT_WORK.md` (2026-09-03 entry) |
| The Haiku-paraphrase sources | Every early "exact quote" was a summarizer's version; 21 files re-sourced | `.project/concepts/source-acquisition-investigation.md` |
| Three different LCOE functions in one UI | A phantom −17.8% drop on a nudge the user never made | `.project/backlog/epic_explorer_ux_v3.md` |
| The dropped digit in DI-006 | Propagated for four months into the hypothesis review | `.project/reports/epic-pipeline-derisk-demo-progress.md` |
| The blog overpromised on three of six validation levels | Found by the tool's own audit; stack restructured | `agentic-mbse/.project/research/20260227-195415_validation-stack-audit.md` |
| The agent optimized the metric, not the problem | 97 commits of regex abandoned | `agentic-mbse/.project/research/20260213-180000_bart-loop-process-learnings.md` |
| Two agent notes hardened into owner rulings | Corrected on the record; "no agent may cite a Rung C gate as authority" | `.project/concepts/stellarator-demo-maturation.md` § Corrections |
| An unscoped one-line change | Recorded as a review finding and ratified by the owner rather than hidden | `work/orchestration/goals/p-pump-fence/trail.md` § Round 1 review |

#### 5.9 Explainers and visual assets already built

| Asset | Story it tells | Path | Date |
|---|---|---|---|
| Workflow explainer (IFE) | Nine sections from the question through source ingestion, research, modeling, visualization, and the closed loop, with real artifacts embedded | `docs/demo/index.html` (live) | Jul 5 |
| Closed-loop story | "A model that has never run is a diagram"; bit-exact anchors; the 11,505-point viability map | `docs/demo/closed-loop.html`, `closed-loop-story.md` | Jul 5 |
| Down-select | Four-stage technology journey; cohort effects | `docs/demo/down-select.html` | May 19 |
| Constraint propagation | Interactive ATMS walkthrough | `docs/demo/constraint-propagation.html` | Apr 11 |
| Score explorer | Public rankings with adjustable axis weights | `docs/index.html` (live) | Jun 26 |
| Pipeline dependency graph | Seven-part map including cross-cutting fragility | `docs/concept-pipeline/dependency-graph.html` (live); d2 sources in `docs/concept-pipeline/diagrams/` | Aug 20 |
| Pipeline prose draft | Filesystem state machine, near blog-ready | `docs/concept-pipeline/pipeline.md` | Aug |
| Pipeline walkthrough | Older standalone | `pipeline-walkthrough.html` | Aug 21 |
| Proof-of-life study report | Feasible band, wall-load fence, availability sweep, "what this does not prove" | `exploration/stellarator_e2e/study/report.html` | Aug 16 |
| Workflow diagram | Six phases as d2 | `docs/workflow.d2`, `docs/workflow.png` | |
| teax explainer | Typed modules to durable studies; three SVG diagrams | `teax/docs/teax-study-explainer.html` | Jul 20 |
| Goal narratives | Three plain-language goal stories with Mermaid figures and a visual index | `work/narratives/20260904-184254Z-*.md` | Sep 4 |
| 1costingFE figures | Tornado, sankeys, floor scenarios, all regenerable from scripts | `1costingfe/docs/blog/{1 Floor,2 DEC,3 Intro}/` | Mar to Jun |
| Blog-post images already published | Ontology v3, the stage diagrams, validation pyramid, calc-flow | in the live posts; `docs/demo/images/` |
| Run-study end-to-end explainer spec | Reader profile, honesty floor, fresh-subagent verification method; the outline file is missing from history | `.project/active/run-study-e2e-explainer/spec.md` | Aug 23 |
| The title rule and adversarial review pattern | "Titles should have MEANING"; FAIR, UNFAIR-BUT-EXPECTED, DEFUSED | `.project/mental-alignment/feedback-synthesis.md` | Aug 23 |

Note: sysml-codegen has no HTML, d2, or dot assets; its diagrams are ASCII in `sysml-codegen/docs/architecture/overview.md` and Mermaid in the constraint concept docs.

#### 5.10 Headline numbers with source paths

| Number | Claim | Source |
|---|---|---|
| 38 (39 to 41) | Concepts in the analysis pipeline | `docs/data/concepts.json`; `.project/research/20260517_ontology_v3_delta.md` |
| 0 of 30; 36.7%; about 2 | Random column combinations coherent; N/A density; effective degrees of freedom | `exploration/phase_1d/report.md`; `phase_1b_v2/report.md` |
| $288.68/MWh; 11 of 11 at 1e-12 | Solar plus battery, first generated pipeline run | `.project/reports/epic-pipeline-derisk-demo-progress.md` |
| $252.30 / $68.69 / $270.12 | IFE anchors reproduced bit-exactly | `modeling_project/VALIDATION_MATRIX.md` SV-023 |
| 11,505 points, 0.1 s; 75.8% viable | IFE viability map | `docs/demo/closed-loop.html` |
| 4 / 6 / 2 / 4 | Blind-derivation adjudication (equivalent, both defensible, answer key wrong, capture gaps) | `modeling_project/HYPOTHESIS_DOSSIER.md` H2 |
| 250.95 → 247.34 → 201.46 → 203.65 → 275.26 → 333.07 → 307.09 → 313.51 $/MWh | Stellarator LCOE by milestone (first pass, geometry, field erratum, stale accounts, handshake, p_pump, sustainment, wall fence) | `modeling_project/VALIDATION_MATRIX.md` SV-027 to SV-052; `.project/CURRENT_WORK.md` |
| 30-plus accounts under 1e-6; two-line remainder; float32 floor −4.8e-08 | The handshake | `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` |
| $6.32B; 50% of $12.60B; 39.3% of overnight | Magnet capital after the field erratum | SV-030; `.project/active/demo-depth-rubric/gap-report.md` |
| 948 points, 59% feasible, best 209.00 | Proof of life | `exploration/stellarator_e2e/study/synthesis.md` |
| 0 of 4,144 feasible; $7.27B vs $16.13B | Nb3Sn arm | `.../studies/20260823-magnet-technology-ab/record.md` |
| −14.4% vs −0.8% | Efficiency versus equipment rates, sCO2 | `.../20260821-power-cycle-ab/record.md` |
| 1.0 → 195 MW; +21.0%; 32 → 184 points | p_pump | `.../20260829-p-pump-fence/record.md`; `work/orchestration/goals/p-pump-basis/trail.md` |
| 0 feasible at 50 MW; 293.468 at 110 MW; beta 0.0311 | Sustainment fence | `.../20260901-sustainment-fence/record.md` |
| 0 of 240 at 50 MW; 27 wall-alone vs 6 ceiling-alone; magnet capital delta exactly zero; 16.645 $/MWh | Priced levers | `.../20260903-priced-levers/record.md` |
| 0 of 240 at 100 MW; 269.8 → 273.7 up vs 317.2 → 256.0 down; 4.087 vs 4.05 | Wall and heating | `.../20260903-wall-and-heating/record.md`; `work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md` |
| R1.P 2 → 3; R3.P 1 → 3; R3.S 2 → 3; R4.P at target | Rubric rows moved | `.project/active/demo-depth-rubric/grading-r*-regrade.md` |
| 13 sessions, 12 agents; 2 of 5 field classes | Cold-pickup proof | `.project/completed/20260827_goal-cold-pickup-proof/verification_record.md` |
| 574 / 14 / 0 | Battery at the harness epic close | `.project/product/0001-goal-round-native-operability.md` |
| 2.68 → 3.71; 8% table error at $0.12/doc; 12× cheaper; 46% → 86% recall | PDF extraction | `agentic-mbse/docs/extraction-internals.md` |
| 57 → 797 lines; 97 commits abandoned | The agent loop that optimized the metric | `agentic-mbse/.project/research/20260213-180000_bart-loop-process-learnings.md` |
| 19 bugs, 42% naming | First codegen e2e wave | `sysml-codegen/.project/research/20260217-030000_...` |
| about 3,400 lines deleted; 676k → 62k lines | Elaborate-first; REPO-CLEANUP | `sysml-codegen/.project/research/20260807-145336_...`; `20260820-201945_...` |
| 2,140 / 9 / 94; 1,506 / 1 / 5; 346 | Test suites: sysml-codegen, agentic-mbse, teax | each repo's `.project/CURRENT_WORK.md` |
| $108.7/MWh, $8,262/kW; −0.91, +0.69 | 1costingFE fresh install; top elasticities | `1costingfe/docs/blog/3 Intro/freeze_outputs/` |
| $29 → $9.5; $17 → $5.0 | Free-core floors D-T and p-B11 | `1costingfe/docs/papers/cost_floor_dec/cost_floor_dec.tex` |
| 917 / 354 / 139 / 40 / 438 | Commits: fusion-tea, sysml-codegen, agentic-mbse, teax, 1costingfe | `git log` in each |

## Code References

- `modeling_project/OVERVIEW.md` lines 22 to 101: research questions, axes, done criteria
- `modeling_project/HYPOTHESIS_DOSSIER.md`: H1 to H4 with evidence and the upstream findings register
- `.project/completed/CHANGELOG.md`: the chronological spine
- `work/orchestration/GOAL_RUNBOOK.md`: the harness contract
- `work/narratives/20260904-184254Z-*.md`: three plain-language goal stories
- `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`: the 1costingFE reconciliation
- `exploration/stellarator_e2e/studies/*/record.md`: every study of record
- `docs/demo/*.html`, `docs/concept-pipeline/pipeline.md`: existing explainers and drafts
- `agentic-mbse/docs/extraction-internals.md`, `agentic-mbse/docs/constraint-facts-and-expression-ir.md`
- `sysml-codegen/docs/architecture/overview.md`, `sysml-codegen/.project/concepts/constraint-execution-authoritative-lifecycle-contract.md`
- `teax/docs/evaluation-and-study.md`, `teax/docs/teax-study-explainer.html`
- `1costingfe/docs/blog/3 Intro/1costingfe-intro-post.md`, `1costingfe/src/costingfe/adapter.py`
- `~/1cfe/Candidate corridors.md`: the spanning-set draft and corridor links

## Architecture Insights

Three patterns recur across every repo and are worth naming once in the series rather than per tool:

- **The filesystem is the state, and scripts mutate it.** The concept pipeline's iteration directories, the PM engine's frontmatter, the goal layer's five surfaces, and the study record contract all follow the same rule: state is what is on disk, agents decide what to change, deterministic code makes the change. (`docs/concept-pipeline/pipeline.md`; `agentic-mbse/.project/completed/epic_architecture-pm-engine.md`; `work/orchestration/GOAL_RUNBOOK.md`.)
- **Fail closed and name the refusal.** Codegen refuses unclean models by typed code; teax refuses a pre-coverage package at load; the integration seam returns one blocker; the hold-out guard fails closed on a bad parse; the research seam computes its return from receipts. "Silence is never an outcome" appears nearly verbatim in three repos.
- **Fresh eyes are a session, not a role.** The study administrator sees only the record, the round reviewer is a different session, the grader is a non-author, and the explainer spec verifies with a subagent that has the page and no repo. The harness's mechanism for catching its own errors is the same everywhere.

## Feasibility Assessment

The series can be written from existing material. Every headline claim has a path, most figures exist or regenerate from a script, and three narratives already read as drafts. Two constraints shape what can be said:

- **Anchor B is unfired.** The stellarator model has not been compared against ARIES-CS. Any post must say Anchor A passed, the depth rubric is the measured maturation loop, and the blind comparison is deferred by choice. The hold-out protocol's contamination inventory should be quoted, not paraphrased.
- **Some promised artifacts are missing.** The run-study end-to-end explainer's story outline is in no branch's history. The traceability audit script cited by MR-4 does not exist. The dependency-graph page lists cross-cutting fragilities. Honest posts can use these as content; they cannot be glossed.

Risks: quoting numbers from memory (use 5.10), and describing tools by their current state when the story is about how they got there (use the timeline in section 4 and the pivot documents).

## Recommendations

A candidate post map, [AGENT], for the owner to accept, reorder, or cut. It fills the two promised-but-unwritten slots first and puts "how it is working" last, where the evidence is strongest.

1. **The pipeline post the March post promised.** From a SysML model to an LCOE: parse, elaborate, generate, evaluate, cost. Three repos, one boundary each, and the handshake as proof. Sources: 5.5, `docs/demo/closed-loop.html`, `HANDSHAKE_REPORT.md`. Assets: the codegen ASCII pipeline redrawn, the teax evaluation-boundary SVG, the handshake remainder table.
2. **Reading the literature is the hard part.** PDF extraction v1 to v4, the corpus, the quality gate and its blind spots, the source registry, the image-inspection rule, and the three generations of extraction phantoms in the machine's own source. Sources: 5.3, 5.8. This is the "key tools" post.
3. **The physics-constraints post the February roadmap promised.** Constraints as verdicts, coverage truth, fences, "disclosed, never tuned," and the seven-goal chain read as one story from a held cold volume to an honest wall fence. Sources: 5.6, 5.7, the three narratives.
4. **The harness.** Goals, rounds, tasks, fresh reviewers, checkpoints, seams, and the five proofs, framed by the owner's own expectation that most rounds return "revisit the model." Sources: 5.7, the runbook, the GSTH epic close.
5. **How it is working.** The failure ledger in 5.8, told as a sequence of catches, each naming the mechanism. End on what is still open: Anchor B, the missing audit script, the blank column.
6. **Where this sits.** 1costingFE as the forward engine, the concept pipeline as breadth, the corridor deep dives as costingfe-direct floor hunts, and the stellarator as the model-route deep dive. Sources: section 2, `~/1cfe/Candidate corridors.md`, the two corridor READMEs. This could open the series instead of closing it.

Alternatives to consider: a hypotheses post built directly on the dossier (section 3), which is the most honest single document in the repo, and a short "designing for 0, 1, or N" post on the information architecture (`agentic-mbse/.project/research/20260130-235423_information-role-taxonomy.md`).

Next step: the owner picks the map and the audience, then `/_my_concept` per post, or one concept for the series with per-post success criteria, feeding `html-explainer` for assets.

## Open Questions

- Which repos are the series allowed to name and link, given teax lives under a personal account and two corridor repos are private?
- Should the series wait for Anchor B, or publish with the blind comparison explicitly deferred?
- Is the spanning-set draft at `~/1cfe/Candidate corridors.md` still planned, and does it precede or follow this series?
- Who is the audience for the harness posts: systems engineers, fusion TEA people, or the agentic-coding community? The tone and the level of tool detail change with the answer.
- The run-study end-to-end explainer spec is approved and its outline is lost. Recover from the mental-alignment run, or re-draft as part of post 1?
