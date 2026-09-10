---
question: "What I want is a full explainer which: gives context into WHY we are doing this; provides a strong mental model for HOW it all works. Most importantly, the end artifact should be really accessible to a general audience: technical, familiar with hardware engineering, and aware of the 1cFE project; but not much else. The challenge is how to balance that with having enough specifics to make this real. The coverage of the explainer must INCLUDE: main objectives and requirements: why this? The framing should follow .project/concepts/physical-innovation-narrative.md; putting this into the context of the 1cfe project; what makes this different from 1costingFE; map of the capabilities developed across agentic-mbse, fusion-tea, sysml-codegen, and teax: the problems they address, the parts that implement them, and the ways agents and programs combine those parts to investigate a physical system; an acknowledgement of the assumptions/limitations behind using DAG; the framework for managing model updates; defining a study, and how a study works; what 'run-goal' is and does; structural views: how to navigate the codebase and the generated artifacts; behavioral views: how pieces flow together; worked examples: showcase real instances to make the explanations real. This must be INTERESTING to read. It should be really clear why someone would be interested: why this exists, why it is non-trivial, and how we delivered it."
date: 2026-09-07 10:20
policy: discovered
shape: plain_document
evidence:
  - .project/concepts/physical-innovation-narrative.md (the required framing; owner-graded items)
  - .project/concepts/stellarator-mbse-demo.md, stellarator-demo-maturation.md, goal-driven-model-development-harness.md, study-driven-model-development.md
  - .project/CURRENT_WORK.md; .project/adr/INDEX.md and ADR-0001..0010; .project/backlog/epic_stellarator_mbse_demo.md
  - modeling_project/OVERVIEW.md, ARCHITECTURE.md, STUDY_POLICY.md
  - work/orchestration/GOAL_RUNBOOK.md; .claude/skills/run-goal/SKILL.md; .claude/skills/run-study/{SKILL.md,runbook.md,record-template.md}
  - work/orchestration/goals/burn-control/{goal.md,trail.md,evidence/T-003_precritique.md}; work/orchestration/goals/stored-energy-basis/learnings.md (L-004, L-005)
  - work/active/WI-043_two-sided-sustainment-condition/plan.md (phase records; the eight literal-count sites)
  - work/narratives/20260904-234255Z-goal-overview.md and 20260906-204832Z-stored-energy-basis.md
  - exploration/stellarator_e2e/studies/20260905-stored-energy-basis/{record.md,synthesis.md,snapshot.json}; 20260907-burn-control/record.md; DISCOVERY_LOG.md; STAGED_MODELS.md; HANDSHAKE_REPORT.md
  - models/library/analyses/mfe_viability.sysml ('Burn Hold'); models/designs/stellarator_09/stellarator_plant.sysml (assert sites)
  - docs/integration_seam_operator_guide.md; scripts/integrate.py; scripts/study/{identity,manifest,indicators,preflight,verify}.py (via explorer)
  - .project/active/demo-depth-rubric/grading-r1-regrade.md; work/orchestration/stale-basis-recompute.md (Addendum 2026-08-30)
  - ~/1cfe/sysml-codegen (README, docs/architecture/*, elaboration/project.py, generation/{stencils,preservation}.py, contracts/*, cli) — via explorer
  - ~/1cfe/teax/packages/teax-simkit (README, docs/evaluation-and-study.md, simkit/{core,evaluation,study}) — via explorer
  - ~/1cfe/1costingfe (README, src/costingfe/*, docs/blog/3 Intro, docs/plans/1todofe.md) — via explorer
  - ~/1cfe/agentic-mbse (src/agentic_mbse/{extraction,validation,pm,sysml,cli}, claude/) — via explorer
  - git log feat/demo-maturation (ed40db86..28e0f7dd); the fresh review of the first draft (20260907-085751_platform-explainer.review.md)
code_inspected: "fusion-tea: the goal/study runbooks and skills, the burn-control goal, trail and pre-execution critique, two study records and one synthesis, the WI-043 plan's phase records, the SysML constraint def and assert sites, test names, the discovery log, the staged-twin note. Sibling repos and scripts/study/*, scripts/integrate.py: inspected by three explorer subagents whose reports I relied on; I did not open those files myself."
limits: "The published post 'Searching the Fusion Design Space Systematically' is not in any local repo; I used the catalog summary in .project/research/20260904-135403_blog-series-topic-catalog.md via the explorer, not the post. The 20260907-burn-control study is staged but not executed at this writing, so its results are unknown. knowledge/holdout/ was not read. I did not run any code; every number is read from committed records. Sibling-repo internals are second-hand from explorer reports."
---

# TLDR

This project tests one idea: **how much useful feedback about a physical machine can you get before you build it, and can AI agents produce that feedback at scale without lying to you?** Fusion is the test case because it is the hardest version of the question (`physical-innovation-narrative.md` § 1–2, owner-graded).

The answer is a chain of five roles (§ 0 gives them as one picture). You write the plant down in a modeling language (a SysML v2 model). A compiler (`sysml-codegen`) turns that into a sealed Python program that computes every quantity forward from the design choices and refuses to solve anything implicitly. A runner (`teax`) evaluates that program at thousands of design points and keeps the results crash-safe. An executor writes each sweep up under a fixed lab-notebook discipline (a *study*, with a record a stranger can audit), so one run becomes evidence. An operator and a round agent, working a lab-director loop (a *goal*, operated with `run-goal`), decide what to ask next and hand the answer to a fresh agent to check.

What makes this different from 1costingFE, the 1cFE costing engine: 1costingFE inverse-solves for the plant that delivers a requested power and does not check that the geometry you typed can deliver it (its own intro post says so). This model computes forward from design levers and then **pushes back** through ten asserted limits, each returning a *verdict* (`satisfied | violated | indeterminate`) at every point. The two were reconciled once, LCOE 123.7430 vs 123.7289 $/MWh with the remaining gap itemized to the cent (`HANDSHAKE_REPORT.md`), then the owner pinned that result at commit `f22bd288` and released the model from matching it (2026-08-30).

The program is a directed acyclic graph (a DAG: every value computed once, in order, no cycles, no solvers). That is a real limitation, and the owner ratified a policy that names it as one: a ladder of four ways the modelers keep physics loops out of the graph, and a tripwire record they write if the ladder runs out (`STUDY_POLICY.md` § 4).

Model updates are managed by **digests everywhere and edits nowhere**. Every package carries three content fingerprints; a study runs against one exact package version (a *pin*); a checking program (`scripts/integrate.py`, the *integration seam*) proves a regeneration changed zero bytes before any study may run; committed study records are never edited (corrections are appended addenda; a changed value is a new study); and a stale reading is restated by re-running at the new pin and joining point by point.

The worked proof is the last two weeks on the stellarator model (§ 10): a typed-in pump power 150× too low; seven goals closed, after which the model contradicts its source paper in more places and hides less (the narrative's own phrase: "more honest, not drifting"); the ninth limit (helium ash on the paper's own rule) moved the design point from "needs 90.6 MW against 50 installed" to "needs 49.08, satisfied by 0.92 MW"; the tenth limit (`burn_hold_ok`, landed 2026-09-07) regenerated with 102 channels compared and 0 differing, passed ten integration gates first run, and is now being measured over 7,712 points.

---

# 0. The whole system in one frame

**Visual cue:** five boxes in a row with a return arrow from the last to the first. Label each box with its plain role and its real name.

Hold these five roles; everything later is one of them.

1. **The description you write** — a SysML v2 model. Text files under `models/` that say what parts the plant has, which values are chosen (the *levers*: major radius, minor radius, density, temperature, coil current, installed heating) and how every other value follows (a calc network: field from coil current, confinement from field and density, required heating from losses, cost from size). Every held number carries the page it came from.
2. **The compiler that turns the description into a program** — `sysml-codegen`, producing a *sealed package*: Python that computes forward through that network and asserts each modeled limit as a verdict. It refuses cycles and implicit solves, and it fingerprints what it produced.
3. **The runner** — `teax`. Loads the sealed package, checks its seal, evaluates it at as many design points as you ask, and stores each point's inputs, outputs and verdicts in a crash-safe database, never mixing results from different package versions.
4. **The lab-notebook discipline** — a *study*. An executor runs one sweep and writes it up in one directory with seventeen fixed sections, immutable once committed, so that a second agent with no memory of the run can say what was asked, what was assumed, what came out, and what none of it supports.
5. **The lab-director loop** — a *goal*, operated through `run-goal`. An operator grounds a question; a round agent pursues it in bounded rounds, one task at a time (change the model, find a source, prove a pin, run a study, read a study), writes a result, and hands it to a fresh agent who did not do the work.

They hand off like this: **a goal round asks for one model change through the modeling workflow; the change is compiled into a new sealed package; the integration seam proves the package is a fixed point and names its pin; a study runs at that pin and commits its record; a fresh reader says what the record supports; the round records what that means for the question and a fresh reviewer checks the round.**

Words this document uses that are the project's own, each defined where it first matters: *verdict* (§ 2), *lever, entry point, channel* (§ 2), *fence* (§ 4), *pin, fingerprint, seam* (§ 5), *restatement, addendum* (§ 5), *oracle* (§ 5), *fresh* (§ 7). The appendix repeats them as a glossary.

---

# 1. Why this exists: feedback before building

**Visual cue:** a two-column strip — left "AI for software" (text, git, tests, agents), right "AI for systems" (the same, plus: executing a model reveals the consequences of its assumptions; only engineering evidence says whether the assumptions describe reality).

The owner's umbrella question, verbatim: *"What would it take for us (humanity) to rapidly accelerate real innovation and progress in the world of physical technology?"* (`physical-innovation-narrative.md` § 1, `[OWNER-VERBATIM]`). Fusion embodies both the promise and the difficulty.

The owner's own constraint on the answer: hardware still has to be built; AI in bits will not deliver a reactor by itself. The leverage is in **where we invest and what we learn from each investment**: invest in the concepts with the most promise, and understand *"exactly what needs to be demonstrated for some larger concept to be viable"* (`[OWNER-VERBATIM]`).

The recurring question the narrative hangs on (agent-proposed, owner-ratified 2026-09-04): **"How much useful feedback can we obtain before building, and how can that feedback make the building count for more?"** The callback form the owner wants used is *"If we can do [X], we can achieve leverage by getting useful [feedback/data/inform]"* — an example of the shape, not fixed wording (`[EXAMPLE]`).

The technical motif is a transfer: patterns from AI-assisted software development (textual models, version control, automated checks, agent workflows) carried into systems engineering, with the differences named. The central difference, as the narrative captures it: *executing a physical-system model reveals consequences of its assumptions; determining whether those assumptions describe reality requires engineering evidence* (`[AGENT]` candidate connecting idea).

Concretely, the project's requirement set (`modeling_project/OVERVIEW.md`) is a cross-concept techno-economic comparison of ~36 fusion concepts along seven axes (LCOE, capital cost by CAS account, capacity factor, fuel cycle, technology readiness, estimation confidence, sensitivity-risk), with one non-negotiable: **every number traces to a source, and assumptions are labelled, because LLM agents do much of the work and hallucinate**. The first big demonstration is one concept, the QI stellarator (concept 09, the "Stellaris" design paper), modeled deep enough to be worth comparing against a sealed hold-out (ARIES-CS) that no model-facing session may read (`stellarator-mbse-demo.md` criteria 3–4; `knowledge/holdout/`).

**Why it is non-trivial.** Three reasons the record makes plain:

- A model that only computes forward will happily print a smooth, plausible LCOE map that is silently wrong. The study-driven concept says it in one line: *"the naive path's observed failure mode is no observed failure"* (`study-driven-model-development.md`). So the model has to be made to push back.
- Agents drift. The goal harness exists because the loop (study → model change → research → regenerate → re-study) had run exactly once, by hand, with the owner carrying "I need X" between stages in a different shape each time (`goal-driven-model-development-harness.md` § Problem).
- Being wrong must stay visible, not be tuned away. Load-bearing values were demonstrably wrong: pumping power was ~150× low until WI-033 (2026-08-28); stored energy sat 9.2 % above the paper's printed value and was left visible rather than fitted (`goal-overview` narrative).

# 2. Where it sits in 1cFE, and what makes it different from 1costingFE

**Visual cue:** side-by-side boxes "1costingFE" and "fusion-tea stellarator model", with arrows for direction of computation (inverse-solve vs forward-and-assess), and a bar underneath showing the handshake: 28 of 32 accounts at 1e-7, LCOE gap −1.14e-04 fully itemized.

**1costingFE** (`~/1cfe/1costingfe`, package `costingfe`) is a JAX-native fusion costing library: hand-written cost formulas over per-concept YAML defaults, CAS10–CAS90 with 18 CAS22 sub-accounts, 17 concepts and four fuels, autodiff sensitivities, and an inverse power balance that solves for the plant that meets a requested net electric power. It is the engine behind 1cFE's published numbers. Its own intro post states its structural hole: *geometry and power are two separate inputs, and nothing enforces that the specified geometry can deliver the requested power* (`docs/blog/3 Intro/1costingfe-intro-post.md`, via explorer). It has no SysML, no constraint verdicts, no study record layer, and its traceability is prose per account, not machine-checked.

The owner's framing of the difference, verbatim: *"Whereas most custom TEA tools like 1costingFE need to decide 'what are the inputs' and 'what gets derived' (which can then be painful to change later), this is totally generalized to forward-pass and assess only. Not necessarily 'better', just has its own pros and cons."* (`stellarator-mbse-demo.md` § Owner's Words.)

What "forward-pass and assess" means in code that exists today:

- **Levers in, everything else derived.** A *lever* is a value an engineer chooses; in the package each lever is an *entry point* with a qualified key like `stellarator_09__stellaris__T_i0`. A *channel* is a computed output, like `stellarator_09__stellaris__lcoe_calc__lcoe`. The stellarator package has 205 entry points and 113 channels. Density and temperature are levers; the field, coil current, stored energy, confinement time, required heating, wall load, every cost account and LCOE are computed (`model_contract.json`, explorer count).
- **Ten asserted limits, each a verdict per point.** A *verdict* is the program's three-valued answer to one asserted limit at one design point: `satisfied | violated | indeterminate`. The ten: `beta_ok`, `burn_hold_ok`, `cond_strain_ok`, `net_positive`, `peak_field_ok`, `recirc_ok`, `sustainment_ok`, `tbr_ok`, `wall_load_ok`, `wp_stress_ok`. In 1costingFE the equivalent question is answered by the analyst eyeballing the LCOE.
- **The model contradicts its source and says so.** Under the model's confinement chain the paper's own operating point needed 90.6 MW of heating against 50 installed; the modeler disclosed that at the assert site and tuned nothing (`grading-r1-regrade.md` EI-2). After the ash fix it reads 49.08 MW. Either way the model's number is the model's, with its basis stated.

## 2.1 The handshake proved the machinery reproduces 1costingFE's arithmetic, and then the owner released it

**The bar.** Demo criterion 3: feed the SysML forward model the plant point 1costingFE solved for and reproduce its per-account costs and LCOE within a written tolerance. The point: stellarator, D-T, 1000 MW net electric, availability 0.9, 30-year life, 8-year build, 7 % interest, NOAK. Per-account bar A-2: |relative deviation| ≤ 1e-6.

**The result** (`exploration/stellarator_e2e/HANDSHAKE_REPORT.md`, generated from an executed run against 1costingFE commit `0254385`): 28 of 32 accounts pass. The magnet account is 2,129.9527 M$ on both sides, deviation −5.4e-10. LCOE: 123.7430 (1costingFE) vs 123.7289 $/MWh (model), a −1.14e-04 miss against the bar.

**Why the miss was accepted.** The −0.0141 $/MWh decomposes exactly into two named remainders: a 0.72 M$ vacuum-pump sub-account the model omits by documented simplification (propagating to −1.08 M$ overnight), and an interest-during-construction convention (uniform-spend vs even-spend midpoint, +2.2 %) the owner ruled on rather than matched. The other four misses are the first remainder propagating downstream.

**The release.** *"I'm done caring about the 1costingFE reproduction. we showed we could do it. pin it, or archive those models. but let's move on — I do not want to be anchored to 1costingFE."* `[OWNER-VERBATIM 2026-08-30]`. Mechanism ruled: pin. The verdict stands at commit `f22bd288`; the reproduction is no longer a live gate; the model may get smarter even where that changes what the old handshake would print (`stale-basis-recompute.md` Addendum). 1costingFE remains the *validation reference* where a comparison applies and is *never a limit* on what the model may contain (`STUDY_POLICY.md` § 10, owner 2026-08-21).

**The published post this builds on.** "Searching the Fusion Design Space Systematically" (1cf.energy, March 2026) covers why SysML v2 (definitions vs usages, text, git, AI coding tools), the six-level verification stack, the spec/design/plan/implement agent workflow, and the IFE demo. I could not read the post itself (not in any local repo); this is from the catalog entry.

# 3. The capability map: four repos, one chain

*Where this sits in the frame:* roles 1–3 (description, compiler, runner) each live in one repo; roles 4 and 5 (study, goal) are layers written inside `fusion-tea`.

**Visual cue:** a horizontal pipeline of four boxes (agentic-mbse → sysml-codegen → teax → fusion-tea layers) with, under each, three rows: *problem*, *parts*, *a normal day*. A second lane below shows the two PM systems and the goal layer sitting above them.

## 3.1 agentic-mbse gets knowledge in and checks the description before anyone runs it

This one toolkit solves two problems that sit at the front of the pipeline. Research papers arrive as PDFs, and you cannot cite a number you cannot trust the extraction of. A SysML v2 model can be wrong in ways that only show when it is compiled, so it needs checking first. Given a PDF, `agentic-mbse` produces extracted text with quality metrics; given a model tree, a six-level validation report; and it keeps the bookkeeping (work items, insights, traceability rows) that the modeling workflow runs on.

On a normal day here: a research subagent runs `agentic-mbse extract` on a paper and then reads the *page image* for any table, because the project learned the extracted tables of the Stellaris paper are corrupted in every row research checked (`burn-control/goal.md` § Invariants). A modeling agent runs `uv run agentic-mbse validate models --complete` after every edit; a green battery is the first gate of every goal task.

**Parts** (`~/1cfe/agentic-mbse`, `src/agentic_mbse/`):

- `extraction/` — a multi-pass, budgeted, quality-gated PDF pipeline (`extract_pdf`; gates assess math garbling, equation fragments, table anomaly and text density, and route bad pages to Claude re-extraction under a dollar budget; three table passes: native, Img2Table, Docling).
- `validation/` — the six levels, exact names: 1 Syntax, 2 Structural Completeness, 3 Dependency Integrity, 4 Constraint Coverage, 5 Traceability & Documentation, 6 Architecture & Pipeline Readiness (level 6 absorbed the former "codegen readiness" checks: qualified names, calc-def structure, anonymous returns, supported operators).
- `pm/` — the modeling project-management state: `work/BACKLOG.md` (YAML frontmatter, tool-owned), work items `WI-XXX`, insights `DI-XXX`, requirements `PR-XXX`, validation rows `SV-XXX`; operations `add-item`, `close-item`, `trace-element`, `add-validation`, `impact-query`.
- `sysml/syside_adapter.py` — the single chokepoint for SysIDE, the commercial SysML v2 parser; nothing else may `import syside`.
- What `agentic-mbse init` installs into a project: 15 slash commands (`/spec-model`, `/design-model`, `/plan-model`, `/implement-model`, `/research`, `/audit-models`, …), 5 expert agents (sysml, kerml, syside, validator, debugger), 10 skills.

## 3.2 sysml-codegen turns the description into a sealed program that computes forward

A SysML v2 model describes; it does not run. To learn anything you have to evaluate it, thousands of times, with proof that what ran is what was modeled. Point `sysml-codegen` at the model tree (or a license-free snapshot of it) and it writes a Python package: one module per calculation, wired into a DAG, every asserted limit compiled into a verdict module, and two fingerprints a reader can use to tell exactly which model produced it.

On a normal day here: a modeling agent finishes a work item and runs `sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten`, reads the one log line that says whether any human-written code was touched, and re-derives the pins (§ 5.2). A human rarely writes code by hand; when the compiler cannot lower a calc (three cases in this package) it leaves a typed stub and a backlog entry, and someone implements it once.

**Parts** (`~/1cfe/sysml-codegen`, v0.1.1):

- Pipeline: parse (SysIDE) → elaborate into an `InstanceGraph` (one node per modelled value occurrence) → project into a `ComputationGraph` (the DAG; § 4) → render Python via Jinja2 → seal.
- The generated package: `modules/` (one teax module wrapper per calculation, 72 here), `handwritten/` (60 implementation files), `schemas/` (pydantic parameter groups), `inputs/` (7 JSON default groups), `pipelines/pipeline.yaml` (81 module declarations), `contracts/` (`model_contract.json`, `package_contract.json`, a verbatim `verify.py`), `IMPLEMENTATION_BACKLOG.md`.
- **Stencils and the manual stage.** A *stencil* is the generated implementation file for one calc. A calc the expression compiler can fully lower becomes an auto-implementation; one it cannot (loops, tables, iteration) becomes a `raise NotImplementedError` stub with the SysML source pointer, listed in `IMPLEMENTATION_BACKLOG.md` "Stage 1: Implement Calculation Functions" for a human or the `/teax-completion` command. Here: 3 manual functions (`Plasma_Sustainment`, `DT_Fusion_Power`, `Levelized_Replacement_Cost`), 11 auto-implemented, zero stubs left. The compiler refuses to fake behaviour it cannot express; that refusal is the seam between "the model said it" and "someone implemented it".
- **Smart regeneration** (`generation/preservation.py`): on regeneration the tool compares each handwritten file's `run_*` signature (`FunctionSignature`: name, input type, return type, referenced input fields) with the new module's; match → *Preserved*, mismatch → backed up to `handwritten/backup/` and *Regenerated*, no file → *New*. The log line `Stencils - New: 0, Preserved: 68, Regenerated: 0` means: no human code was touched.
- **Two fingerprints the package carries.** A *fingerprint* is a SHA-256 digest that names content, not a version label. `semantic_fingerprint` = sha256 of the canonical `ModelContract` (parameters, outputs, constraint catalog, evaluation semantics), pure over the graph. `executable_fingerprint` = sha256 over the sorted `path:hash` lines of every sealed file (195 here). `verify.py`, emitted into the package, checks the seal on load: `TAMPER | MISSING | EXTRA | NAME_MISMATCH`.
- A license-free path: `sysml-codegen snapshot` captures the v6 instance-graph envelope; `generate --from-snapshot` reproduces the byte-identical package without SysIDE.

## 3.3 teax runs the program many times and keeps the evidence crash-safe

Evaluating a sealed package once is easy; evaluating it at seven thousand points, classifying each by its verdicts, and surviving a killed process without a corrupted or mixed-up record is the job. You give `teax` a sealed package and a list of design points; it leaves behind a SQLite store in which every case carries its inputs, its channels, its verdicts and the fingerprint of the program that produced them.

On a normal day here: a study's `study.py` calls the package-owned route (`study_route.prepare`, `run_points`) which drives teax's `StudyRunner`; nobody writes a sweep loop by hand (`STUDY_POLICY.md` § 5 bars it). If the package changed since the store was created, the store refuses to open (`IncompatibleStore`).

**Parts** (`~/1cfe/teax/packages/teax-simkit`, import name `simkit`; reached by path via `STOP_PARSER_TEAX_ROOT`, not a declared dependency):

- `core/` — `ModuleBase`, `PipelineDagBuilder`, `SerialPipelineExecutor`: builds the runtime DAG from the YAML and executes in topological order.
- `evaluation/` — `ProvisionalPackageLoader(strict=True)` (verifies the seal by importing the package's own `verify.py`), `PreparedEvaluator` (in-memory evaluation; exposes `.fingerprint` and typed `.entry_models`), `ModelEvidence` (frozen: `responses` per constraint id, `outputs`, `provenance` with executable fingerprint and input digest, deliberately no wall-clock). A canonical headline map: `full_satisfaction → satisfied`, `violation → violated`, and *no report at all* is a sixth state, `unconstrained`.
- `study/` — `StudyDefinition` (carries both fingerprints; `.compatibility()` is bound once at store creation), `GridStrategy` / `PreparedListStrategy`, `StudyRunner` (validate → bridge → evaluate → assess → stage → atomic commit), `StudyStore` (SQLite, WAL + `synchronous=FULL`, fenced lease, content-addressed staging), `StudyQuery` → `CaseView`. Results are never merged across executable fingerprints.

**Isolation claim (documented intent):** teax never imports a generated class; it reads the report by four duck-typed attributes.

## 3.4 fusion-tea holds the model and the two layers above the tools

The three tools are each closed on their own terms. Someone has to decide *which* sweep to run, *what* the result means, *what* to change in the model, and keep that decision trail honest across sessions and agents. `fusion-tea` holds the fusion model, the generated package and its studies, the generic study tools and the integration seam, and the two operating procedures (`run-study`, `run-goal`) with their rulebooks.

**Parts:**

- `models/library/` (18 `.sysml`, concept-agnostic: `foundation/`, `cost_structure/`, `analyses/` — the 13 analysis files carry the physics and costing calcs and the constraint defs in `mfe_viability.sysml`) and `models/designs/stellarator_09/stellarator_plant.sysml` (1,311 lines: the Stellaris instance, every held value with a `Source/Ref/Basis` doc comment). A byte-identical twin at `exploration/stellarator_e2e/models/` is what the compiler actually reads; `tests/models/test_model_family_spines.py` fails on any drift (`STAGED_MODELS.md`).
- `exploration/stellarator_e2e/generated/` (the package; `pkg/stellarator_tea` is a symlink giving it its import name), `studies/` (one directory per study; `manifest.json`, `study_route.py`, `oracle_entry.py`, `ANNEX.md`, `DISCOVERY_LOG.md`), `verify_stellaris.py` (the *oracle*: a hand-written pure-Python recompute of every formula, independent of the generated code; § 5.4).
- `scripts/study/` — the generic study tools: `indicators.py`, `preflight.py`, `verify.py`, `manifest.py`, `identity.py`. `scripts/integrate.py` — the integration seam. `scripts/source_registry.py` and `research_seam.py` — the one write door into `knowledge/`.
- `.claude/skills/run-study/` and `run-goal/` — the two operating procedures; `work/orchestration/GOAL_RUNBOOK.md` and `modeling_project/STUDY_POLICY.md` — their rulebooks; `.project/adr/` — the ten decision records behind them.
- Two PM systems, deliberately separate: the coding PM in `.project/` and the modeling PM in `work/`. Each is mutated only through its own operations; an agent may *cite* the other by `<path>@<commit-sha>` (ADR-0006).

## 3.5 Who does what: programs gate, agents argue, fresh agents check, the owner rules

The user asked how agents and programs combine these parts to investigate a physical system. The division of labour, stated as the rule the records follow:

- **Programs do the mechanical, fail-closed work.** They compute digests, refuse mismatches, execute points, derive verdicts, and recount. *Instance:* `scripts/integrate.py` re-ran regeneration on the WI-043 package and reported zero bytes moved outside `handwritten/`, then returned `CANDIDATE` on ten gates (`trail.md` T-002 return).
- **Agents do the arguing, in files a stranger can audit.** They ground goals, write task scopes, choose windows, frame axes, read records, and propose dispositions. *Instance:* the burn-control grounding session read the sister systems codes, probed nine points oracle-side, and put one proposal with six facts to the owner (`goal.md` § Question).
- **Fresh agents check the arguing.** A session that did not do the work reviews it: the pre-execution critique of a study's framing, the administrator's recount of a record, the disposition checkpoint, the round review. *Instance:* the fresh administrator of `20260905-stored-energy-basis` re-derived every count from `results/points.csv` with an independent pandas script and found seven statement slips (§ 6).
- **The owner rules on policy and reserved gates,** never delegating the seal, the no-fallbacks rule, the axis rule, merge, push, close. *Instance:* *"we should fix the ash profile (and make sure this scales up for larger stellarators). and I don't want to add the footnote."* `[OWNER-VERBATIM 2026-09-05]`, which chose WI-042 over a disclosure footnote.

The seams a task invokes are named in § 7.5; the flow through one round is in § 9.

# 4. The DAG: what it buys and what it costs

*Where this sits in the frame:* role 2, the compiler, and the rule the description (role 1) must obey for the compiler to accept it.

**Visual cue:** a small graph of the stellarator calc network (levers R, a, n_e0, T_i0, I_coil at the left; `field_calc → sustain → beta_calc / wall_load → viability verdicts → lcoe` to the right) with a red "no" over a would-be back-edge from power balance to confinement.

**What it is (current code).** `sysml-codegen`'s projector orders modules with a hand-written Kahn topological sort; a cycle is a typed refusal (`SI_EDGE_DANGLING: typed module dependency cycle`), as is a self-dependency. `execution_order` must be a valid topological sort (REQ-PIPE-04). teax executes serially in that order. There is no iteration, relaxation, Newton step or convergence machinery anywhere in codegen or teax's executor (explorer, verified by absence). One evaluation = one case, one pass, every value computed exactly once.

**Why that is a real limitation for a fusion plant.** Physics is full of loops: confinement time depends on heating power, heating power on losses, losses on stored energy, stored energy on confinement. A systems code like PROCESS closes the power balance as an *equality* and solves. A DAG cannot.

**How the owner and the modelers handle it (`STUDY_POLICY.md`, ratified whole 2026-08-21).** Two rules and a ladder.

- **Inequalities accumulate safely; equalities over swept inputs collapse the feasible set to a thin manifold nobody's grid lands on.** So the modelers assert limits as inequalities (all ten verdicts are). The study records call such an inequality a *fence*: a limit that "catches" an edge of a swept window. A modeler writes an equality *inside* the forward computation, where it holds by construction at every point (§ 1, § 3).
- **The axis rule** `[OWNER-VERBATIM 2026-08-02]`: *"it should be justifiably the causal DESIGN parameter. E.g. choose all geometry and input powers, and get an output power."* Sweep only levers an engineer chooses; never a computed quantity. When a refinement makes a former lever computed, the study executor stops sweeping it; the policy's own word for this is that "the axis retires" (§ 2).
- **The resolution ladder for cycles (§ 4):** R1 re-examine causality (many "cycles" are a lever plus a margin: the designer specifies on-axis B, so coil field is downstream and the conductor limit enters as an inequality); R2 collapse algebraically on paper and write the closed form flat (pump power ⇄ thermal power isolates in one line); R3 merge the cluster into one calc def that returns the consistent tuple, solved in a handwritten body with the closure residual exposed for a thin guard assert (the ISS04 confinement chain does this: `'Plasma Sustainment'` returns τ_E, p_rad, the ash densities and `p_aux_required` from the levers, with a damped fixed-point iteration for the ash inside the handwritten body); R4 seed one variable from a coarse lever-derived estimate and assert a validity band. If the ladder runs out, the modeler records the cycle in the tripwire table rather than working around it; that record is the evidence a relational solver would need. The tripwire table is empty today (§ 8).
- **Barred:** a standing equality assert over swept axes; hand-rolled outer solve loops in harness or study scripts; sweeping a computed quantity; sweeping a subset of an attribute's entry keys (§ 5).

**The consequence you can see in the record.** Because the model computes *required* heating forward instead of solving for temperature, "is this plasma an operating point?" became two inequalities on one operand: `sustainment_ok` (`p_aux_required ≤ installed`) and, since 2026-09-07, `burn_hold_ok` (`p_aux_required ≥ 0`). The sister codes write the balance as an equality and define an ignited design point as P_aux = 0 exactly; the model's pair is the inequality form of that practice (`mfe_viability.sysml` 'Burn Hold' doc). A solved-temperature form was tried and rejected as the wrong architecture at this machine state: no stable feasible burn exists inside the limits at the baseline, and the paper's printed point sits on the unstable branch (`operating-point-closure` L-002, reviewer-accepted).

**Other stated DAG-adjacent limits (documented in codegen):** derived design-attribute expressions are refused, not lowered (`= my_calc.output * 0.95` fails; it needs a calc def); units are metadata only, no conversion; indexed references refuse; all calc defs must live in `models/library/`.

# 5. Managing model updates: digests everywhere, edits nowhere

*Where this sits in the frame:* the handoff from role 1 through role 2 to roles 3–4. A model change has to reach a study without anyone being able to run a study against a package that is not what the model says.

**Visual cue:** a timeline of one model change, left to right: *commit A* (SysML edit + restatement written before any regenerated byte) → *commit B* (regenerate; snapshot, census, six fixtures, manifest re-pinned; three fingerprints move) → *integrate.py* (ten gates, zero bytes moved) → *CANDIDATE pin* → *new study at that pin, joined to the committed study by case id*. Below it, the "never" list: never edit a committed record, never hand-patch a census, never tune.

The problem: a SysML change invalidates everything downstream (the package, the studies that ran on it, the goal readings that cite them). The designers' answer is a chain of content digests and a fixed-point proof, not a staleness marker. (The project's Stage-1 concept-analysis pipeline made the opposite bet, markers on artifacts and no hashes: `staleness-propagation.md`. Different subsystem.)

## 5.1 A reader can tell exactly what ran from five digests

| Name | What it is computed over | Owner | Current value (WI-043 pin) |
|---|---|---|---|
| semantic fingerprint | canonical `ModelContract`: parameters, outputs, constraint catalog | sysml-codegen | `baab7e4c7541…` |
| executable fingerprint | sha256 of every sealed file's hash (195 files) | sysml-codegen | `cd2c1c4aa535…` |
| indicator-input fingerprint, **the pin** | the 9 files the reachability tracer reads: `model_contract.json`, 7 `inputs/*.json`, `pipeline.yaml` (`scripts/study/manifest.py`, recipe `indicator-input-fingerprint/v1`) | fusion-tea | `1d4a06b0e0e9…` |
| effective executable fingerprint | the sealed fingerprint + digests of every file a study route was allowed to modify + the route's own sources (`scripts/study/identity.py`); for the stock route it degenerates to the sealed value | fusion-tea | = sealed |
| teax revision | `git rev-parse HEAD` of the teax checkout | fusion-tea (no producer exists; gap filed) | `8d877460…` |

A *pin* is *the exact package version a study runs against*, named by the indicator-input fingerprint. Promoting one fixes what "the model" means for that study so two results are comparable (`GOAL_RUNBOOK.md` § Opening and closing a round). A round has at most one promoted pin and one committed study.

## 5.2 A model change obliges four steps before anyone may study it

Observed in WI-041, WI-042 and WI-043; the modeling item's agent does all four.

1. **Write the restatement, then commit it before regenerating.** A *restatement* says what every column of every committed study will mean under the new package, gives the rule for re-reading it, and promises that no committed record is edited (the MR-WI043-7 shape). It is committed *before* the regenerated bytes so the git order attests the sequence (WI-043: commit A `b7e2d534`, commit B `a7afd8f1`).
2. **Regenerate in place** with `--smart-regen --preserve-handwritten`, and read the stencil line.
3. **Re-derive every pin; hand-patch none.** The instance-graph snapshot (`stellarator.snapshot.json`); the entry-point census (`tests/models/data/mfe_census.json`, stamped `derived_against_semantic_fingerprint`; a test emits "model meaning moved — re-derive" when it lags); the six known-answer fixtures under `tests/study/data/`; the study manifest's fingerprints and baseline headline; the single runner's expected verdict count; the oracle mirror whenever a held input changes (ADR-0010).
4. **Run the batteries:** `validate models --complete`, `tests/models`, `tests/study`, the single runner (bit-exact vs oracle).

## 5.3 The integration seam proves a package is a fixed point; it performs nothing (ADR-0009)

A *seam* in this project is a documented boundary a goal task invokes, with a fixed input and a fixed return (§ 7.5). The integration seam is `scripts/integrate.py`, and it answers one question: *is there exactly one verified, study-ready candidate for this package, and if not what stopped it?*

It re-runs every producer **in place** and requires each to change nothing: regeneration must move zero bytes outside `handwritten/`, the recaptured snapshot must equal the tracked file, the manifest's pin must recompute to the recorded value. Ten gates in producers' order: pinned-packages, teax-revision, regeneration, handwritten-preservation, census-snapshot, model-family-spine, manifest, preflight, verification (oracle parity, every verdict re-derived from the catalog's predicate and the operand bindings), lineage.

Return: `CANDIDATE` (exit 0) with the pin and both fingerprints, or `BLOCKER` (exit 1) naming the one producer and whether it *refused* or *could not run*. The program commits nothing; a refusal at regeneration means the model item's agent has unfinished work, not that the seam is broken. Runtime 15–20 s. The rule the round agent carries: a seam repair is a `PREREQUISITE` return, never a quiet scope expansion.

The program judges byte movement by its own per-file digests, not git (git is vacuous inside the gitignored test workspace); the designers measured mtime and rejected it (95 of 153 files move mtime on byte-identical regeneration).

## 5.4 Records are immutable; a stale reading is re-executed, never edited

- A committed study record is corrected only by appending `## Addendum <date>`. An *addendum* may correct the record's *statement* of a fact and may never alter `snapshot.json`, `indicators.json` or `results/`. **"A changed snapshot value is a different study and gets a new study id."** (`record-template.md` § Immutability.)
- A stale reading is restated by running a *new* study at the new pin over the same arms and joining every point to the committed record by case id, with both bases side by side in each row (`20260905-stored-energy-basis` and `20260907-burn-control` both do this).
- The discovery log is append-only: the executor writes a sighting row; a goal round appends a joined disposition row under the same id and never edits the sighting (ADR-0004).
- Goal files are append-only; corrections are dated `### Amendment` entries.
- Digest citations in goal artifacts are **read by people**; no goal procedure compares or recomputes one. That machine check is on the hardening path, and the owner promotes it only when a real run shows the human reading failing (ADR-0003, `GOAL_RUNBOOK.md` § When a cited artifact moves).
- The *oracle* (`verify_stellaris.py`, a hand-written recompute of every formula that never imports the generated code) is demo-scoped. It caught the first live case where the model moved and the oracle did not: WI-033's `p_pump` 1.0 → 195 MW left the oracle computing the old plant, 38 channels off, and gate 8 refused. It is the only non-circular verification of a regenerated package today (ADR-0010).

# 6. A study is one sweep with a record a stranger can audit

*Where this sits in the frame:* role 4. One study runs at one pin and ends in one immutable directory.

**Visual cue:** the 15 execute steps as a vertical ladder, each rung labelled with what it *deposits* (record section or file); a gate icon on the rungs that fail closed (3, 5, 6, 9, 10, 15). Beside it the three roles as swimlanes: user, executor, administrator.

**Definition (`run-study/SKILL.md`).** *A study runs a model package over a set of parameter points and records what the model's own objective and constraints did at each one. What makes it a study rather than a sweep is the record: one directory that a second agent, with no memory of the run, can read and recover what was asked, what was assumed, what came out, and what none of it supports.*

## 6.1 Three people or sessions hold three roles, one at a time

The **user** sets the intent and rules on any axis the model does not resist. The **executor** works the runbook and commits the record. The **administrator** reads *only* the committed record directory and writes `synthesis.md`, reporting a missing fact as missing rather than recovering it from elsewhere. Two modes: `execute` (intent, no record) and `administer` (record, no synthesis).

## 6.2 The record has seventeen fixed headings and splits values from arguments

`exploration/<pkg>/studies/<YYYYMMDD-slug>/` holds `record.md` (the seventeen headings in order: header, intake verbatim, objective and result, constraint outcomes by qualified id, framing as proposed and as judged, per-axis account, axis groups, indicators and rulings, preflight, route and glue disclosure, window provenance, cross-fingerprint correlation, verification, review outcomes, findings, snapshot, what this record does not contain), `snapshot.json` (resolved values and digests: the three fingerprints, `arms[].window`, `stores[]` with the teax compatibility tuple, `effective_executable_fingerprint`), `axes.json`, `indicators.json`, `results/`. A checker parses the snapshot; a human reads the record; neither restates the other. An unreplaced `<...>` placeholder in a committed record is a commit-blocking defect; `tests/study/test_records.py` enforces closure and the discovery-log join.

## 6.3 The executor works fifteen steps, and only mechanical conditions stop the study

1 intake verbatim → 2 declare each axis as a complete qualified entry-key group (a *tie* is declared, never derived: `magnet__R0` rides with `R` because they are the same physical radius) → 3 run indicators for every proposed axis, declined ones included → 4 argue the framing (`search` expects a boundary; `sensitivity` expects a monotone response and no boundary claim) and put it to a pre-execution critique before any point runs → 5 load the route and execute the pinned baseline → 6 preflight gates (declared keys, suffix siblings, identity, baseline headline reproduces, manifest/package fingerprints agree, package git-clean) → 7 scan with the oracle and fix the window; a restated window is re-scanned at the new package from an anchor feasible there (owner, 2026-09-06) → 8 choose and justify the route (`teax-study` CLI for plain grids; study-local `StudyRunner` for coordinated blocks) → 9 every point through the stock teax lifecycle, no hand-rolled loop → 10 verify a verdict-stratified sample against the oracle, re-deriving verdicts from operands → 11 judge the framing against the result → 12 review outcomes as named lenses → 13 report, every number recomputable from `results/` → 14 findings register and discovery-log rows → 15 resolve the snapshot and commit; from here the evidence is immutable.

**Fails closed means** the study stops only on mechanical conditions (missing key, fingerprint mismatch, unparseable artifact, dirty package). An axis that looks boring or a result that looks wrong never gates; the executor records and argues it.

## 6.4 Indicators give a sound negative and never a positive claim

`scripts/study/indicators.py` digests the nine pin files, then traces a deliberately over-approximate graph (every module output depends on every module input). So `no_constraint_response` is a **sound negative**: nothing in the model pushes back on this axis, which the owner reads as *"a signal the model is underdeveloped"* (`STUDY_POLICY.md` § 9); it forces a user ruling before execution and a model-development finding that the ruling does not discharge. `constraints_reachable` is only a possible path. Four things are never derivable and every record says so: monotonicity, identity of one quantity across differing key names, intra-module operand dependency.

## 6.5 What a real record looks like

`20260905-stored-energy-basis`: four arms, 7,712 points, ~1.1 s each per worker; 15 declared keys across 14 groups, 7 declined and held; preflight 6/6; verification 20 rows, 13 channels within 1e-9 (worst 4e-16), 9 verdicts re-derived, no mismatch.

The fresh administrator's recount (an independent pandas script over `results/points.csv`) agreed with every headline count, transition, flip, optimum and margin, and found seven statement slips, none changing a conclusion, all landed as the record's first Addendum (`synthesis.md` § 3.16). Four are location descriptions that were slightly too tidy: where the 28 newly excluded points sit in density; which 13 design-column points ignite (11 at 16–18 MA with the field ceiling violated, 2 at the pinned 15.4 MA with the wall violated); where the 145 points with rising W sit in (R, a); which limits catch the `a` transect at 1.3 (sustainment and beta, not sustainment and the wall). Three are ranges quoted from one cell rather than the window: the re-read arm's LCOE rise ("+2.8 % at every point" → mean +2.57 %, range +1.24 to +4.26); the W ratio by geometry (0.826–0.996, not 0.826–0.975); the derived electron exponent at the 145 points (0.406–0.450, not 0.44–0.5).

# 7. run-goal is a grounded question pursued in rounds that strangers review

*Where this sits in the frame:* role 5. The operator and the round agent decide what to work on next and what the evidence means; the native workflows do the work.

**Visual cue:** a nested-boxes diagram. Outer box *goal* (`goal.md`: question, consumer, answered-when, invariants, limits, reserved gates). Inside, *rounds* (one strategy each, closes on one of six triggers). Inside a round, *tasks* (six-line scope → start line → native work → return with one of six outcomes). Two gate icons: the pre-execution disposition checkpoint (before follow-up work) and the fresh round review (after close). Arrows out to the five native seams.

**What it is (`run-goal/SKILL.md`, `GOAL_RUNBOOK.md`).** *A goal is a grounded question pursued in rounds. A round is one agent's bounded attempt at one strategy, running one task at a time through the native workflows, ending in a mandatory written result and a review by a fresh agent who did not do the work.* The operator and the round agent, writing in the goal files, decide **what to work on next and what the evidence means**; they do no work in those files. They cite native artifacts and never restate them, so nothing can disagree.

## 7.1 Five files hold a goal, and a test keeps them from becoming copies of each other

`goal.md` (what are we answering; written once with the operator), `trail.md` (what happened and what was decided; append-only), `learnings.md` (what this run now knows; the result proposes, the fresh review accepts), the runbook (how), the ADRs (why). Templates in `work/orchestration/goal-templates/`; `tests/orchestration/test_goal_contract.py` checks the headings, the writer ownership, that the skill is a door and not a second copy, and that "fresh" is defined at owner strength.

## 7.2 A goal authorizes nothing until all five field classes are filled

Grounding evidence (repo paths for what is already known), the answer contract (§ Answered when, concrete enough that two people agree), invariants (so "better" cannot drift), limits (retry cap 2, checkpoint revision cap 2, round limit 6 by default; restated in every goal), reserved gates (what the owner keeps). A goal hollow in any class authorizes no task, not even a small one. The owner hardened that rule on 2026-08-27 after a five-session probe measured cold agents running full tasks on goals missing invariants or limits (`GOAL_RUNBOOK.md` § Grounding, amendment).

## 7.3 A round runs one strategy with no task list and closes on one of six triggers

The round agent opens with one `### Strategy revision` (approach, assumptions, abandonment conditions, intended model increment, intended study question) and **no future task list** (ADR-0001: a plan written before the evidence is authority granted in advance). A round is bounded to at most one promoted pin and one committed study. It closes on exactly one of: a valid study reading (adverse counts), a strategy blocker, changed comparison meaning, an unresolved owner gate, a declared limit, or the goal answered. The agent then writes `### Round N result` and *derives* the stop reason from the last outcome plus the limits, never keeping it as a second status.

## 7.4 A task is scoped before it starts and returns one of six outcomes

The round agent writes a six-line scope before any work (Objective, Why now, Scope, Inputs, Done when, Stop when); a one-line start entry before the first native side effect so an interruption leaves a trace; does the work through a native workflow; and writes a return with one outcome: `COMPLETE`, `BOUNDED_NEGATIVE` (a real, useful no), `PREREQUISITE` (discovered, never predicted), `STRATEGY_BLOCKER` (closes the round), `OWNER_GATE`, `MECHANICAL_FAILURE` (retry permitted only with identical task, inputs, scope and meaning). Every goal-level decision carries five fields: the trigger, the decision and reason, the tier (`execution detail | reserved gate | premise surprise`), who decided, what changed (resolving to paths, ids, commits, or `none`). Scope is a reviewable record, not a sandbox; the fresh reviewer catches drift afterwards.

## 7.5 A task invokes one of five native seams and reads what it returns

`research` (registered sources or a bounded negative), `model` (audited item or blocker), `integrate` (one `CANDIDATE` pin or a named `BLOCKER`), `study.execute` (committed record or blocker), `study.read` (synthesis and findings) (`GOAL_RUNBOOK.md` § The native seams). Every seam is native today; the `integrate` row flipped on its first live goal-round invocation (goal `p-pump-fence`, 2026-08-29).

## 7.6 Two fresh checks sit at two different moments (ADR-0005)

*Fresh* is the owner's word and a session boundary: *"The critic is never the author's session."* Not "someone who did not do that piece", but a session with none of the author's reasoning in front of it.

The **pre-execution disposition checkpoint**: after a study reading proposes dispositions and before any semantic follow-up executes, a fresh non-author session reads both and returns a verdict; each resubmission is a new `C-00N.rK` entry; hitting the cap writes a recorded stop and never permits execution. The **fresh round review**: after close, over the whole round — every citation resolves, strategy fidelity, every task scope, retry honesty, every touched discovery row landed, the learning delta, constraints carried forward; verdict `PASS | FINDINGS | OWNER_GATE`; the reviewer never resumes the closed round, and after a pass either recommends the owner-held close or writes the next strategy.

An agent that cannot start a fresh session **stops and hands back** with a recorded `### Stop` of kind `handoff`; it never reviews its own round. Unattended dispatch is barred until a real run shows prose failing (ADR-0003, lean-first; owner: "yeah I agree with (a)").

## 7.7 The owner keeps the gates; the round owes every touched finding a home

Merge, push, item close, archive, every reserved gate and the close of a goal stay owner-held. Policy is never delegated: no fallbacks, the hold-out seal, the axis rule. Every discovery row a round's evidence touches gets a disposition (`model fix | research | declared seam | upstream filing`); no touched row returns `unrouted` (ADR-0004, owner-settled criterion 4). The task is the authority unit; the finding stays the traceability unit (ADR-0007).

# 8. Structural view: every artifact has one home, and the tracked ones are hashed

**Visual cue:** a directory tree with four coloured regions (model source, generated package and studies, the goal layer, the two PM systems), and a legend "tracked and hashed / gitignored but cited through a tracked record / quarantined".

**Model source (authoring).** `models/library/{foundation,cost_structure,analyses}/*.sysml` (18 files, concept-agnostic; all calc defs and constraint defs live here); `models/designs/{generic_mfe,stellarator_09,generic_ife,hif_ife}/` (concept instances; `stellarator_09/stellarator_plant.sysml` binds every held Stellaris value with `Source/Ref/Basis`). Model-architecture decisions `AD-XXX` in `modeling_project/ARCHITECTURE.md` (plain `Real` everywhere, closed-form DCF for LCOE because calc defs cannot loop, CAS hierarchy as typed part defs).

**Model twin and package.** `exploration/stellarator_e2e/models/` (byte-identical twin, the compiler's input); `exploration/stellarator_e2e/generated/` (the package: `modules/`, `handwritten/`, `schemas/`, `inputs/`, `pipelines/pipeline.yaml`, `contracts/{model_contract.json,package_contract.json,verify.py}`, `IMPLEMENTATION_BACKLOG.md`); `pkg/stellarator_tea → ../generated`; `stellarator.snapshot.json`; `verify_stellaris.py` (oracle); `run_stellaris_single.py` (single runner); `HANDSHAKE_REPORT.md` (Anchor A, pinned).

**Studies.** `exploration/stellarator_e2e/studies/`: `manifest.json` (package path, three fingerprints, `ties`, 12-objective catalog by channel, baseline point R 12.7 / a 1.3 / availability 0.85 with headline `lcoe_calc__lcoe` = 322.31843948570247 and ten expected verdicts, the oracle declaration), `study_route.py` (package-owned route; `EXPECTED_CONSTRAINT_COUNT = 10`), `oracle_entry.py` (`evaluate(point)`, `operand_bindings()` for all ten constraints, fail-closed maps), `ANNEX.md` (package facts the generic runbook links to), `DISCOVERY_LOG.md` (172 lines, append-only), and ten study directories from `20260821-power-cycle-ab` to `20260907-burn-control`.

**Generic study tools and the seam.** `scripts/study/{indicators,preflight,verify,manifest,identity}.py`; `scripts/integrate.py`; `tests/study/` (~45 test files: gates, refusals, lineage, records, known answers), `tests/models/` (spines, census), `tests/orchestration/test_goal_contract.py`, `tests/test_dependency_provenance.py` (sha256-pinned sealed wheels for agentic-mbse 0.1.3, sysml-codegen 0.1.1, 1costingfe 0.1.0, at `/home/reid/1cfe/stop-parser-sealed-wheels/`).

**The goal layer.** `work/orchestration/GOAL_RUNBOOK.md`; `work/orchestration/goals/<slug>/{goal.md,trail.md,learnings.md,evidence/}` (nine goals: cryo-volume-basis, p-pump-basis, p-pump-fence, magnet-closure, operating-point-closure, priced-levers, wall-and-heating, stored-energy-basis, burn-control); `work/narratives/` (human-facing snapshots, explicitly not evidence or state; the goal contract test keeps them separate); `.project/adr/0001..0010`.

**Knowledge.** `knowledge/SOURCE_INDEX.md` (registered sources with raw and extract SHA-256), `knowledge/sources/` (30 extracted), `knowledge/concept_research/` (38 concept dossiers; binaries in R2, gitignored, cited through tracked markdown), `knowledge/KNOWLEDGE.md` (DI-XXX insights), `knowledge/holdout/aries-cs/` (sealed; never read).

**The two PMs.** `.project/` (coding: `active/`, `backlog/`, `completed/`, `concepts/`, `adr/`, `CURRENT_WORK.md`); `work/` (modeling: `BACKLOG.md` tool-owned, `active/WI-XXX_*/`, `completed/`, `learnings/`). Read across by digest; mutate only through your own operations.

**Name collisions to defuse for the reader (dropdown candidate).** "manifest" is three things (codegen's source manifest, teax's run manifest, fusion-tea's `study-package-manifest/v1`); "snapshot" is two (the instance-graph envelope; a study record's `snapshot.json`); "pipeline" is both the SysML calc network and the teax YAML DAG; "fingerprint" is at least five (§ 5.1).

# 9. Behavioral view: one round moves a question through five seams with a program gating each hop

**Visual cue:** a loop diagram with the goal at the top and the five seams around it: ground → open round → task (research | model | integrate | study.execute | study.read) → checkpoint → next task → round result → fresh review → next strategy or owner close. Annotate where programs gate (fail-closed) and where agents argue (record, trail).

The loop, as it actually ran for `burn-control` round 1 (2026-09-06/07):

1. **Ground.** The previous goal's fresh reviewer recommended grounding burn control before choosing its form. The grounding session deposited two checks under `evidence/` (a source reading of the sister systems codes; an oracle-side probe of nine points at the pin: density control, thermal-stability sign, fixed-density attractor, access ramp) and put one proposal with six facts to the owner. Owner: *"yes, please proceed with that /run-goal"* `[OWNER-VERBATIM 2026-09-07]`. Each call stays `[AGENT] (ratified by owner)`, challengeable by re-deriving against the recorded evidence, because the owner said *"I don't have the knowledge to answer questions like these. I need to lean on you for judgement."*
2. **Open the round** with one strategy: land the second inequality first, then measure. Five assumptions, three abandonment conditions, no task list.
3. **T-001, seam `model`.** WI-043 through `/spec-model → /design-model → /plan-model → /implement-model`. Restatement first (commit A), regeneration (commit B), batteries and the literal-count fixes (commit C). Return `COMPLETE` with two five-field decisions recorded. Details in § 10.6.
4. **T-002, seam `integrate`.** `scripts/integrate.py --audited-work work/active/WI-043_…@e7818fdf …` into a scratch dir. Return: `CANDIDATE`, ten gates first run; the pin `1d4a06b0e0e9…`; seven return documents deposited as `evidence/T-002_*.json`.
5. **T-003, seam `study.execute`.** `/run-study` in execute mode at that pin; the round agent spawned a pre-execution critique before any point runs. It returned MAJOR with eleven findings, all accepted (`evidence/T-003_precritique.md`): three MAJOR — F1 the falling-branch premise is false inside the window (§ 10.7); F2 the "every channel bit-identical" claim was being tested on four channels while the teax executor had moved between the bases, so identity must be measured over every channel and all nine committed verdicts; F3 "the first bound on `a`" is a transect reading at the edge of the closure's validity, not a bound. Eight MINOR or notes — F4 what the stability column may and may not say; F5 SV-059 is two identities and the export should carry one directly; F6 the expected-result posture is sound, say what the evidence is; F7 mechanics of the stability pass (guard it with a recompute phase); F8 stale comments in `study.py`; F9 which design-column numbers carry into the demo statement; F10 the join, the exclusions and the discovery rows are verified, nothing to fix; F11 the step-7 window re-read is done and correct. None changed an arm, a window or a held key. The study is staged (intake, axes, indicators, baseline, preflight 6/6, window edges re-read with the tenth fence, pre-screen) and, at this writing, not yet executed.
6. **Still to come in this round:** the run, the fresh administrator's synthesis, the C-001 checkpoint on the proposed dispositions, the discovery-log rows for `20260904-wall-and-heating#4` and `20260905-stored-energy-basis#1`, the round result, the fresh review, the owner's ruling on the restated design point (§ Answered when (c)).

Where programs gate in that flow: the validation battery and spine test (step 3), the ten seam gates (4), the indicators' fingerprint check and the six preflight gates (5), the store's compatibility tuple and `test_records.py` at commit. Where agents argue: the scope and return entries, the critique, the record's framing sections, the synthesis, the checkpoint, the review. Where the owner rules: grounding, reserved gates, the close.

# 10. Worked examples: one story, in order

**Visual cue:** a single timeline, 2026-08-22 to 2026-09-07, with seven markers; under each, one number that moved.

## 10.1 A typed-in pump power was 150 times too low, and the model could not tell

The stellarator model carried primary-coolant pumping power as 1.0 MW, a default inherited from 1costingFE. The first study on the package (`20260821-power-cycle-ab`) sighted it as finding #3: about 100× below helium-circulator figures. Goal `p-pump-basis` (closed 2026-08-28) asked whether 1.0 MW was defensible; the answer was no, and two EU DEMO helium-loop papers put it at 130–195 MW. WI-033 set it to 195 MW, still as a typed-in number. The next goal, `p-pump-fence`, re-ran the geometry sweep at 195 MW: LCOE rose 21 % at the reference point, and the infeasible region grew from a small-machine corner to a band across the window. Five other places still carried the old value; the round found and fixed them (`goal-overview` narrative).

**The point.** A forward model with a wrong input prints a smooth, plausible map. Nothing in the arithmetic objects. Only a researcher with a source, or a modeler who has asserted a limit, catches it. This is the "no observed failure" failure the designers built the whole platform against.

## 10.2 The handshake showed the machinery could reproduce another tool's arithmetic, and the owner released it

Told in § 2.1: 28 of 32 accounts at 1e-7, LCOE 123.7430 vs 123.7289, the gap itemized, pinned at `f22bd288`, the owner's *"I do not want to be anchored to 1costingFE."*

**The point.** Reproduction was a milestone, not a leash. Once proved, a standing duty to match the reference would have blocked every later step in which the modelers replaced a typed-in number with a calculation.

## 10.3 Seven goals in two weeks: the modelers made the model disagree with its source in more places, and hid none of them

From `work/narratives/20260904-234255Z-goal-overview.md` (a human-facing summary; the goal records win on any disagreement):

| Goal, closed | Asked | Answered? | Model changed | What got better |
|---|---|---|---|---|
| cryo-volume-basis, 08-27 | Can the 136.56 m³ of cooled coil be computed from coil current? | No | No | Two facts later goals relied on (the "ampere-turns" number is a cost stand-in; a simple field law undercounts stellarator coil current) |
| p-pump-basis, 08-28 | Is 1.0 MW of primary-coolant pumping defensible? | No | Value fixed by WI-033 | ~150× correction to 195 MW, two EU DEMO papers registered as sources |
| p-pump-fence, 08-29 | With 195 MW, what does the recirculating-power limit rule out? | Yes | Regenerated | LCOE +21 % at the reference point; the infeasible region grew from a corner to a band; five stale copies of the old value found and fixed |
| magnet-closure, 09-01 | Can field, coil stress and magnet cost be computed from the coil design? | Yes | WI-035 | Rubric score 1/2 → 3/3; magnet capital −14.6 %, every part explained |
| operating-point-closure, 09-02 | Can the model tell whether the machine can hold the chosen plasma? | Yes, after a first round showed a solved-T form cannot work | WI-037 | Rubric 2 → 3; the ISS04 sustainment chain; the model rejects designs the heating cannot hold; the paper's own point read as needing ~90 MW where the paper says zero, left visible |
| priced-levers, 09-03 | Higher-field magnet or more heating: which is cheaper? | Stopped, not answered | WI-036 | Coil cross-section follows current (matches the paper's 15.4 MA and 360 mm exactly); found the wall-load check was the real blocker and the coil material had no cost line |
| wall-and-heating, 09-04 | Fix the wall-load check (average vs peak); model heating as equipment | Open then | WI-039, WI-041 | Heating as a chain from wall-plug to plasma; peak-to-peak wall check; the reference design fails it narrowly |

**The point**, in the narrative's own words: across these goals the reference design's LCOE went from 275 to 313.5 $/MWh and it came to fail two of nine checks. Each time a typed-in number became a calculation, the calculation reproduced the paper's *inputs* and the outputs were left free to disagree. A goal that closes "answered: no" (two of the seven) is a result, not a failure.

## 10.4 A printed number turned out not to be a target, and the fix tuned nothing

**The inherited gap.** The model integrated assumed profiles to a stored thermal energy W of 551.4 MJ where the Stellaris paper prints 504.65 (+9.2 %). Conducted loss rises steeply with W, so the design point needed 90.6 MW of coupled heating against 50 installed: `sustainment_ok` violated, disclosed, never tuned. Two earlier goals carried this as "not a defect" on an agent-written rule that W is never tuned.

**Grounding flipped the premise.** Before the goal was ratified, the agent scaled W to the printed value inside a copy of the oracle: the requirement fell to 37.5 MW and both baseline violations flipped. But the same arithmetic showed no reading of the paper's own plotted profiles reaches 504.65, and the paper's printed beta implies 567 MJ. *The printed value is not a target* (L-002; now a standing invariant).

**The real gap was a profile shape.** Round 1 registered the same author's systems-code papers and applied their definition of W with the paper's own profile rules: 518.3 MJ. The attribution: 5.3 of the 9.2 points from the helium-ash profile shape (the model gave the ash the fuel's flat profile; the paper's rule peaks it in the core), 1.2 from profile exponents, 2.7 the paper's own and not closable from any admissible source.

**The owner chose the fix over the footnote.** *"we should fix the ash profile (and make sure this scales up for larger stellarators). and I don't want to add the footnote."* `[OWNER-VERBATIM 2026-09-05]`.

**WI-042 landed, round 2.** At the pinned baseline: W 551.444 → 519.914 MJ; τ_E 1.450 → 1.557 s; fusion power 2725.4 → 2652.6 MW; required heating 90.605 → 49.080 MW against 50 (satisfied by 0.92 MW); wall peak 4.088 → 3.979 MW/m² against 4.05 (flips to satisfied); LCOE 313.513 → 322.318 $/MWh. Oracle bit-exact on every sustainment channel; the seam promoted pin `ec984adc…` first run. The ash exponent became a function of ion temperature alone (4.73 at 10 keV, 4.05 at 14.63, 3.46 at 20), so the fix scales as the owner asked.

**The point.** The demo statement became L-004: *satisfied on every fence, on the boundary; "needs 90 MW" retired; "is feasible" undecidable from the source, whose own stored energy disagrees with itself by more than the margin in both directions.* Nothing was fitted to make the verdict flip; the flip is what the paper's own rule produces.

## 10.5 The restating study found that every feasibility count rested on a hand-applied reading

`20260905-stored-energy-basis` re-ran the committed 7,712-point window at the new pin, joined to the old record point by point. Of the committed 681 "driven" points, 510 now read a *negative* heating requirement with every other fence satisfied: they ignite. The one-sided fence passes them, so every feasibility count on the package rested on a hand-applied "driven" reading (L-005). The cheapest driven point moved to a row the old study had excluded (13 keV): 202.192 $/MWh at R 15.7 m, a 2.2 m, 13 MA, case `c2823`. The design column (R 12.7, a 1.3) at 100 MW has exactly one driven point, the pinned baseline. The two constant-scale counterfactuals predicted signs but not locations (L-006). Owner: *"close it"* at round 2 of 6; WI-043 and WI-044 minted to the backlog.

**The point.** A model change moved the feasible region, and the executor could say exactly how, because the old study was joinable by case id and the new one was run rather than edited. And the surprise became the next question: the modelers needed a second inequality.

## 10.6 The tenth verdict landed with zero bytes moved anywhere else

**What was added.** `constraint def 'Burn Hold' { in attribute p_aux_required_in : Real; p_aux_required_in >= 0.0 }` in `mfe_viability.sysml`, asserted as `burn_hold_ok` in the Stellaris instance on the operand `sustainment_ok` already reads (`stellarator_plant.sysml:1300`). One formal, a literal zero, no entry point minted.

**What its doc text says it is.** A **hold** condition: a point with a negative requirement has no heating authority; left alone at its density the plasma as modeled settles at 20–41 keV with the wall at 2.3–5.4× its limit, and the model has no burn-control mechanism because no admissible source quantifies one. **Not** a statement that ignition is infeasible: the sister codes define an ignited design point as P_aux = 0 exactly, and the paper's own point A is one (Table 5, read from a page render because the extracted table is corrupted).

**The restatement, committed first** (commit A `b7e2d534`): `burn_hold_ok` re-reads from any committed `p_aux_required_MW_oracle` column purely by sign; every committed `sustainment_ok` column means bit-for-bit what it meant; under the ten-verdict package "feasible" equals the committed "feasible driven" at every point by construction; no committed record is edited.

**The regeneration** (commit B `a7afd8f1`): one new module, `stellarisburnholdokconstraintmodule.py`, plus seven regenerated contract, aggregator and pipeline files; 78 insertions, 14 deletions; `Stencils - New: 0, Preserved: 68, Regenerated: 0`; no `handwritten/backup/`.

**The baseline did not move.** 102 channels compared, 0 differing. LCOE 322.31843948570247, unchanged to the digit. Nine verdicts unchanged; the tenth satisfied at 49.0796 MW. Verdict parity 10 / `full_satisfaction`; bit-exact vs oracle.

**The ignited points read as predicted.** Two points from the grounding probe, P1 `c2835` (−125.63 MW) and P3 `c2132` (−188.76 MW), run through the study route at the new package: `burn_hold_ok` violated, `sustainment_ok` satisfied, the oracle re-deriving both identically, LCOE equal to the committed record's to every printed digit.

**Eight places counted the constraint set by literal, and the batteries found every one.** Five in phase 4: `study_route.py:49` (`EXPECTED_CONSTRAINT_COUNT = 9`, which refused the verdict export "expected exactly 9 catalogued checks, found 10"); `run_stellaris_single.py:59`; `tests/study/test_operand_bindings.py:79` ("the nine viability constraints"); `tests/study/test_valid_empty.py:39-40`; `tests/study/test_known_answers.py:137`. Three more that the full `tests/study` run surfaced (commit C `e7818fdf`): `test_verify.py:100-107` (the re-derived catalogue set); `test_operand_bindings.py:100` (seventeen feature_ref operands became eighteen); `test_known_answers.py:167-190` (the I_coil reachable set, with a new `burn_hold_ok` assertion). Each was restated from the live package with a dated comment; none was patched to a number. The `tests/study` run of record: 67 failed / 415 passed / 1 skipped, the 67 being the branch's 64 pre-existing fail-closed cases plus those three sites; the four affected files then 52 passed / 1 skipped.

**The re-pin.** Indicator `ec984adc…` → `1d4a06b0…`; executable `8ac14fdf…` → `cd2c1c4a…`; semantic `c37fb58a…` → `baab7e4c…`; census 205 entry points, no key minted or retired; six fixtures re-derived; `burn_hold_ok` reachable from R, R+tie, a and I_coil and from neither economic axis. One prediction of the design missed: the tainted-channel count rose by one on the four plasma axes (the new module's own evaluation channel), recorded in the plan's phase-5 record.

**The seam.** `CANDIDATE`, ten gates first run, pin `1d4a06b0e0e9…`.

**The point.** Adding a physics constraint to a plant model changed one file's meaning and nothing else's, and every program in the chain could prove it: the compiler by its stencil line, the baseline diff by 102/0, the seam by ten gates. The eight literal sites are the honest cost: places where a human had written "nine" and the batteries, not memory, found them.

## 10.7 A premise turned out too broad, and the round agent amended the goal instead of fitting the data

The goal's fact 5 said the whole 13–18 keV window sits on the falling branch of the ignition curve, driven points included. The pre-execution critique (F1) probed 140 committed fence-feasible points and found 14, all driven, at 17–18 keV and low density (0.6–0.7×), on the *rising* branch; every ignited point probed is falling. The grounding probe had nine points, none at that corner.

What happened next, under the capture-fidelity rule that a premise conflict is never resolved silently: the round agent wrote a dated amendment to `goal.md` narrowing the fact; the hold argument stands, because it never rested on the branch (it rests on no non-negative heating closing an ignited point's balance); the model doc text that repeats the broad form was routed to a follow-on item and *not* corrected by the study; the study states the expected branch pattern before any point runs and will measure the column as it is (`goal.md` § Amendment 2026-09-07; `trail.md` § Amendment).

**The point.** An agent can be wrong on the record in a way that stays visible, dated, and separable from the parts that still stand. That is what "never tuned" costs and buys.

## 10.8 A measured quality trajectory without unsealing the hold-out

The depth rubric (`.project/active/demo-depth-rubric/rubric.md@dc0f0b6d`) grades each subsystem on two dimensions, physics self-consistency and structural/costing depth, written by reasoning against the class of systems-level design studies and never against the sealed ARIES-CS papers. A fresh grader re-scored Row 1 (plasma) after WI-037: **2 → 3**, on the anchor *"a confinement/transport relation links field and heating to density and temperature, and a beta, density, or power limit pushes back on the choice"*. The grader also recorded a contestable-anchor note (the preamble says "determine", the table says "links") and routed it to the owner rather than around them, and flagged that the six sustainment operand values reach only the oracle-side CSV, not the evidence store (EI-1). Cross-record LCOE comparisons are barred; the delta claimed is depth (`grading-r1-regrade.md`).

**The point.** "Is the model getting closer to ARIES-level quality" is answered by a re-graded delta, measured blind, rather than by a feeling or by opening the sealed papers.

# Judgment

- **Second-hand sibling internals.** Everything about sysml-codegen, teax, agentic-mbse and 1costingfe internals comes from three explorer reports. They cite files and line numbers and agree with what fusion-tea's records say those tools do, but I did not open those files. Spot checks worth making before the HTML: the Kahn sort and cycle refusal in `sysml-codegen/src/sysml_codegen/elaboration/project.py` (~1150–1213); `FunctionSignature.matches` subset semantics in `generation/preservation.py`; `CANONICAL_HEADLINE` in `teax/.../simkit/evaluation/evidence.py:66`.
- **The in-flight study has no results.** `20260907-burn-control` is staged, with §3/§4 placeholders and only preflight artifacts in `results/`. Its expected outcomes (ten-verdict "feasible" = committed "feasible driven" case by case; channel identity under a moved teax revision) are stated in the record as predictions, not measurements. The HTML must not report them as results.
- **The published post is unread.** The 1cf.energy post is blocked to fetch tools (memory: 403 to WebFetch; curl with a browser UA works). If the render needs its framing verbatim, fetch it that way.
- **Names collide across repos** (§ 8 last paragraph). A reader who does not get the disambiguation early will conflate the study manifest with the codegen source manifest, and the instance snapshot with a record snapshot.
- **What "fresh" costs.** The runbook's freshness rule means an agent cannot review its own round and must stop and hand back. That is deliberate (ADR-0003), and it is also why the trail shows several `Stop — handoff` entries and spawned-prompt deposits. The explainer should present it as the point, not as friction.
- **Tension worth naming honestly.** The DAG policy bars hand-rolled outer solve loops, while the ISS04 chain's handwritten body iterates a fixed point *inside* one calc def (R3). Both are consistent with the policy as written (the solve lives in the model, once); a reader may still ask why one loop is fine and the other is not. The answer is the "no math in two places" guard (`STUDY_POLICY.md` § 3) and the oracle mirror.
- **Two things the record files but does not close.** No producer exists for the teax revision (the seam checks it against an argument); `assert_read_set_covered` is run by nothing; `verify.py` records `teax.revision: "unrecorded"` (operator guide § What the seam does not check).
- **Owner-grade vs agent-grade.** I marked the owner's verbatim rulings where the sources do. Most of the goal-layer *mechanism* is agent-designed and owner-ratified (ADR provenance fields say so); the explainer should not present those mechanisms as the owner's own requirements.
- **Numbers I could not cross-check myself** and took from records: the 102/0 channel comparison, the 68 preserved stencils, the 205/113/10 contract counts, the handshake table. All are in committed artifacts named above; a reader can re-open them.
- **Noticed in revision.** (a) The verb sweep found the abstraction-as-actor shape mostly in my own prose about the goal layer, the seam and "the project"; the source documents themselves attribute judgment to the operator, the round agent, the reviewer or the owner, and the rewrite follows them. (b) The two "answered: no" goals in § 10.3 are the clearest case for a hardware reader that a bounded negative is a result, and the first draft buried that under the table. (c) Naming the eight literal sites shows something the count hid: five were found by the item's own batteries and three only by the *full* `tests/study` run, which argues for the full run as a gate rather than the affected files. That is my inference, not a recorded finding.

# Appendix

## A. The ten verdicts at the baseline (WI-043 pin)

`beta_ok`, `burn_hold_ok` (49.0796 MW ≥ 0), `cond_strain_ok`, `net_positive`, `peak_field_ok` (24.9 vs 24.9 T, at equality by design convention), `recirc_ok`, `sustainment_ok` (49.080 ≤ 50 MW coupled, margin 0.92), `tbr_ok`, `wall_load_ok` (3.979 vs 4.05 MW/m²), `wp_stress_ok`. Baseline point R 12.7 m, a 1.3 m, availability 0.85; LCOE 322.31843948570247 $/MWh (`manifest.json` → `baseline`; `ANNEX.md` § Baseline pin: the headline moved 307.087 → 313.513 → 322.318 across WI-039/041/042).

## B. Glossary of the project's own words

- **Lever / entry point / entry key.** A value a study may vary; qualified like `stellarator_09__stellaris__T_i0`. 205 in the package. A **tie** declares that two keys are one physical quantity.
- **Channel.** A computed output; 113. The **headline** channel is `stellarator_09__stellaris__lcoe_calc__lcoe`.
- **Verdict.** `satisfied | violated | indeterminate` per asserted constraint per point.
- **Fence.** The records' word for an inequality constraint that "catches" an edge of the window.
- **Driven / ignited / feasible.** Driven: every fence satisfied and `p_aux_required ≥ 0`. Ignited: `p_aux_required < 0` (two senses in the records: the bare column, and negative with every other fence satisfied; every claim says which). Under the ten-verdict package "feasible" equals the committed "feasible driven" by construction.
- **Fingerprint.** A SHA-256 digest naming content. Five kinds in § 5.1.
- **Pin.** The indicator-input fingerprint of the package a study runs against; one promoted per round.
- **Seam.** A documented boundary a goal task invokes with a fixed input and return; five in § 7.5. The **integration seam** is `scripts/integrate.py`.
- **Oracle.** `verify_stellaris.py`: an independent recompute of every formula, used to verify samples and to probe off-package (oracle-side diagnostics are never package evidence).
- **Census.** `tests/models/data/mfe_census.json`: the entry-point count and classification, derived against a semantic fingerprint.
- **Restatement.** The pre-regeneration note saying what every committed study column will mean under the new package.
- **Addendum.** The only way a committed record is corrected.
- **Fresh.** A session that did not do the work. Owner's definition.

## C. Files that carry the contracts

`work/orchestration/GOAL_RUNBOOK.md` (goal procedure) · `.claude/skills/run-study/runbook.md` and `record-template.md` (study procedure and record contract) · `modeling_project/STUDY_POLICY.md` (axis rule, equality rule, cycle ladder, verification) · `docs/integration_seam_operator_guide.md` (the ten gates, env vars, return schema) · `.project/adr/INDEX.md` (why) · `exploration/stellarator_e2e/studies/ANNEX.md` (package facts) · `STAGED_MODELS.md` (the twin rule).
