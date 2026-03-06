# Capturing Logical Models Before Formal Modeling: Frameworks for Pre-SysML Concept Representation

**Reid Westwood — February 2026 — 1cFE / Astera Institute**

---

## The Problem

We are researching fusion energy approaches. The design space has the structure of a **decision tree**: confinement method → fuel type → heating scheme → blanket concept → ... Each leaf is a mostly-formed conceptual model for how a fusion power plant would operate. For each conceptual model, the literature provides key challenges, known pros and cons, and basic analytical formulas for energy production and major cost factors.

We need a way to **capture these logical models and their mathematical heuristics** in a structured, executable form — *before* building formal SysML v2 models. These representations become the data source for architecting proper structural and behavioral models downstream.

The question is not "what optimization tools exist" (that's a later problem) but rather: **what frameworks exist for structuring design knowledge during the concept exploration phase, so that it's useful both to humans reasoning about the problem and to machines that will eventually formalize it?**

---

## 1. Structuring the Design Space: Morphological Analysis

The most directly applicable framework for the "decision tree of fusion approaches" is **General Morphological Analysis (GMA)**, developed by Fritz Zwicky in the 1940s and refined computationally by Tom Ritchey at the Swedish Morphological Society since the 1990s [^zwicky][^ritchey2015].

### How it works

A morphological field is a multi-dimensional matrix where each dimension represents a design parameter (e.g., confinement method, fuel type, blanket concept) and each value along a dimension represents an option. The total space is the Cartesian product of all options — for fusion, this could easily be 10 dimensions × 3-8 options each, yielding millions of combinations.

The key computational contribution is **Cross-Consistency Assessment (CCA)**: systematically evaluating pairs of parameter values for logical or empirical consistency. CCA typically eliminates 90-99% of the total space [^ritchey2015], leaving a manageable set of internally consistent configurations — each one a candidate conceptual model.

### Why this fits

The fusion design space has exactly this structure. A valid fusion concept requires mutually consistent choices across confinement (tokamak, stellarator, mirror, inertial, magneto-inertial, ...), fuel (DT, DD, DHe3, pB11), plasma heating (NBI, ICRH, ECRH, laser), first wall / blanket (liquid lithium, solid ceramic, flowing salt, ...), and so on. Many cross-dimension combinations are infeasible — CCA makes these exclusions explicit and traceable.

### Tools

The primary tool is **MA/CARMA** (Computer Aided Resource for Morphological Analysis), proprietary software maintained by the Swedish Morphological Society [^macarma]. A Python implementation exists on GitHub [^zwicky-python] but is limited. For 1cFE, the matrix structure and CCA logic are simple enough to implement directly or use as a data model.

### Key references

[^zwicky]: Zwicky, F. (1969). *Discovery, Invention, Research Through the Morphological Approach.* Macmillan.

[^ritchey2015]: Ritchey, T. (2015). "Principles of Cross-Consistency Assessment in Morphological Modelling." *Acta Morphologica Generalis* 4(2). Available: https://www.swemorph.com/amg/

[^macarma]: Swedish Morphological Society. MA/CARMA software. https://www.swemorph.com/macarma.html

[^zwicky-python]: Buchner, J. Zwicky Morphological Analysis (Python). https://github.com/JohannesBuchner/zwicky-morphological-analysis

### Has MA been applied to fusion?

I searched specifically for this and the answer is **no** — there is no published application of formal GMA/CCA to fusion reactor concept exploration. This is a notable gap given how naturally the problem fits.

What does exist:

- **Zwicky himself** applied MA to propulsive power systems (1962), which included nuclear propulsion concepts — his morphological field had 6 dimensions and 576 configurations [^zwicky1962]. Freeman Dyson noted that Ted Taylor used morphological thinking at Los Alamos for nuclear weapons design [^dyson2020]. So the method has nuclear-adjacent roots.

- **Fusion Energy Future** (an advocacy group, "International Fusion Energy Consortium") has a ["Fusion Reactor Classifications" project page](https://www.fusionenergyfuture.org/project/project-4-fusion-reactor-classifications/) describing plans to classify fusion reactors by confinement method, fuel type, power output, cost, and environmental impact — but it appears to be aspirational rather than published work. No deliverables, papers, or datasets are available. Not a morphological analysis.

- **Lee et al. (2025)** built the **first automated knowledge graph of nuclear fusion energy** using LLMs (Llama 3.1/3.3) and Neo4j, extracting entities and relationships from fusion literature [^fusion-kg]. This captures *what the literature says* but doesn't structure it as a design space with cross-consistency constraints.

- The **DOE Fusion S&T Roadmap (2025)** [^doe-roadmap] classifies concepts by confinement family (tokamak, stellarator, FRC, Z-pinch, mirror, inertial) and explicitly embraces "concept diversity" — supporting multiple approaches as hedges. The Emergent Plasma Concepts program [^doe-roadmap] funds across traditional and novel confinement approaches. But again, this is a taxonomy, not a morphological analysis.

- **Ritchey's GMA reference list** [^ritchey-refs] catalogs 80+ published applications including nuclear facility security scenarios in Sweden, but nothing on fusion reactor concept design.

- **Droste-Franke et al. (2020)** [^droste-franke] applied MA to regional energy scenarios, and **Ramirez-Acosta et al. (2022)** [^ramirez-acosta] used MA for electricity market categorization — both energy-adjacent but not fusion-specific.

The implication: **this is greenfield for 1cFE.** A rigorous morphological analysis of the fusion design space — with explicit CCA marking which cross-dimension combinations are infeasible and why — would be a genuine contribution to the field, not just an internal tool.

[^zwicky1962]: Zwicky, F. (1962). *Morphology of Propulsive Power.* Society for Morphological Research. https://books.google.com/books/about/Morphology_of_Propulsive_Power.html?id=lFHxAAAAMAAJ

[^dyson2020]: Dyson, F. (2020). "The Power of Morphological Thinking." *New York Review of Books*, January 16, 2020. https://sites.astro.caltech.edu/~srk/Dyson_On_Zwicky.pdf

[^fef]: Fusion Energy Future. "Fusion Reactor Classifications." https://www.fusionenergyfuture.org/project/project-4-fusion-reactor-classifications/

[^doe-roadmap]: U.S. Department of Energy (2025). *Fusion Science & Technology Roadmap.* https://www.energy.gov/sites/default/files/2025-10/fusion-s&t-roadmap-101625.pdf

[^ritchey-refs]: Ritchey, T. Morphological Analysis Reference-by-Area List. Swedish Morphological Society. https://www.swemorph.com/ref-by-subject.html

[^droste-franke]: Droste-Franke, B., Voge, M. & Kanngießer, A. (2020). "Achieving transparency and robustness of regional energy scenarios by using morphological fields." *Energy Strategy Reviews* 27.

[^ramirez-acosta]: Ramirez-Acosta, N., Lehnhoff, S. & Gomez, J. (2022). "Electricity market categorization based on morphological analysis for smart grid development."

---

## 2. Capturing Design Rationale: Why These Choices?

Morphological analysis generates *what* the options are. A complementary question is *why* certain combinations are preferred, excluded, or uncertain. The design rationale literature addresses this.

### QOC (Questions, Options, Criteria)

The most lightweight and applicable framework is **QOC** (Questions, Options, Criteria), developed by MacLean et al. (1991) [^maclean1991]. It represents design exploration as:

- **Questions**: Key design issues ("What confinement scheme?", "What fuel cycle?")
- **Options**: Candidate answers (tokamak, stellarator, mirror, ...)
- **Criteria**: Reasons for or against each option (plasma stability, engineering complexity, cost scaling, technological maturity, ...)

Links between options and criteria carry positive or negative assessments. The result is a lightweight, readable map of the design space and the reasoning behind it.

QOC maps directly to the morphological dimensions (questions) and values (options), adding the argumentative layer that CCA's binary consistency judgments lack. For fusion, criteria include physics feasibility, engineering maturity (TRL), cost sensitivity, and fuel availability.

### IBIS (Issue-Based Information Systems)

For more complex argumentation, **IBIS** (Kunz & Rittel, 1970) [^kunz1970] provides a richer notation: Issues → Positions → Arguments, with support/object/generalize relationships. IBIS is the foundation of tools like Compendium [^compendium] (open-source knowledge mapping, now unmaintained) and modern design deliberation platforms.

The advantage over QOC is richer argumentation structure; the disadvantage is heavier notation. For 1cFE's scale, QOC is probably sufficient for most concept-level decisions, with IBIS reserved for the most contested trade-offs.

### Key references

[^maclean1991]: MacLean, A., Young, R.M., Bellotti, V.M.E., & Moran, T.P. (1991). "Questions, Options, and Criteria: Elements of Design Space Analysis." *Human-Computer Interaction*, 6(3-4), 201-250. https://doi.org/10.1080/07370024.1991.9667168

[^kunz1970]: Kunz, W. & Rittel, H.W.J. (1970). *Issues as Elements of Information Systems.* Institute of Urban and Regional Development, UC Berkeley.

[^compendium]: Compendium Institute. "About Compendium." http://www.compendiuminstitute.org/about-compendium/

---

## 3. Representing Conceptual Models: The "Concept Card" Pattern

Each leaf of the decision tree — each mostly-formed fusion concept — needs a structured representation. The literature suggests several patterns, which I'll synthesize into a recommended approach.

### Engineering Model Cards

Google's **Model Cards** framework (Mitchell et al., 2019) [^mitchell2019] provides structured documentation for ML models: purpose, intended use, inputs, outputs, assumptions, limitations, performance metrics. The concept translates directly to engineering analytical models.

An **Engineering Model Card** for a fusion concept would document:

- **Identity**: Name, approach family, morphological configuration (which options from the morphological matrix)
- **Scope**: Physics regime, fuel type, confinement approach, scale range
- **Key parameters**: Entry variables, their physical meaning, typical ranges, literature sources
- **Analytical relationships**: The formulas — power balance, confinement scaling, cost estimation relationships
- **Assumptions**: Which physics are included/excluded, which engineering constraints are enforced/relaxed
- **Known challenges**: Technical risks, unsolved problems, TRL assessments
- **Pros/Cons**: Comparative advantages and disadvantages relative to other concepts
- **Validation status**: Comparison to literature, experimental data, or higher-fidelity codes
- **Sources**: Traceability to specific papers, reports, databases

### Christopher Alexander's Pattern Language

Alexander's *A Pattern Language* (1977) [^alexander1977] provides a deeper conceptual foundation. A pattern is not just a template — it captures a **recurring problem-solution pair in context**, with explicit forces (competing concerns) and consequences. Each pattern links to others, forming a network.

For fusion, a pattern language might look like:

- **Pattern: Steady-State Tokamak** — *Context*: When selecting magnetic confinement with DT fuel for baseload power... *Problem*: Pulsed operation creates fatigue and intermittent output... *Forces*: Bootstrap current fraction vs. external current drive power... *Solution*: Target >90% bootstrap current with ECCD assist... *Consequences*: Requires advanced plasma shaping, increases capital cost of heating systems... *Related patterns*: Advanced Divertor, High-Field Magnets, Liquid Metal Blanket...

This is more expressive than a flat card because it captures the *reasoning* and *trade-offs* that led to the concept, and the *network of dependencies* between design choices.

### MOKA Knowledge Capture

The **MOKA methodology** (Stokes et al., 2001) [^stokes2001], developed for aerospace knowledge-based engineering, provides a practical capture framework. Its ICARE forms structure knowledge into five types:

- **Illustrations**: Examples, diagrams, reference designs
- **Constraints**: Physics limits, material limits, regulatory requirements
- **Activities**: Design procedures, calculation sequences
- **Rules**: Heuristic decision rules ("if aspect ratio < 3, use high-field magnets")
- **Entities**: The physical things being designed (components, subsystems)

MOKA was designed to bridge the gap between informal expert knowledge and formal engineering systems — precisely the pre-formalization problem.

### Key references

[^mitchell2019]: Mitchell, M., Wu, S., Zaldivar, A., et al. (2019). "Model Cards for Model Reporting." *Proceedings of the Conference on Fairness, Accountability, and Transparency*, 220-229. https://doi.org/10.1145/3287560.3287596

[^alexander1977]: Alexander, C., Ishikawa, S., & Silverstein, M. (1977). *A Pattern Language: Towns, Buildings, Construction.* Oxford University Press.

[^stokes2001]: Stokes, M. (2001). *Managing Engineering Knowledge: MOKA Methodology for Knowledge Based Engineering Applications.* Professional Engineering Publishing. ISBN: 978-1860582950.

---

## 4. Capturing Mathematical Heuristics: From Literature to Executable Models

The analytical formulas that describe each fusion concept — power balance, confinement scaling, cost estimation relationships — need to be captured in executable form. Several frameworks address this.

### Cost Estimation Relationships (CERs)

In aerospace and defense, **parametric cost estimation** captures cost scaling laws as simple power-law relationships before detailed design exists [^nasa-ceh]. A CER has the form:

```
Cost = a × (Parameter_1)^b × (Parameter_2)^c × Complexity_Factor
```

where coefficients are derived from historical data or physics-based reasoning. NASA's **NAFCOM** model and the PRICE/SEER family use hundreds of CERs derived from thousands of projects [^price-validation]. The key insight: 70-80% of lifecycle costs are locked in during early design, so parametric models are *essential* for concept screening — detailed models come later [^nasa-lifecycle].

For fusion, the analogs are:

- **Physics scalings**: P_fusion ∝ n² × ⟨σv⟩ × V_plasma (from cross-section physics)
- **Confinement scalings**: τ_E ∝ I_p^α × B^β × R^γ × ... (empirical, e.g., IPB98(y,2) for tokamaks)
- **Cost scalings**: C_magnet ∝ B^2 × R^3 (stored energy scaling), C_blanket ∝ A_surface × t_blanket × ρ_material × C_material
- **Balance-of-plant**: Scaling from conventional power plant cost databases (NETL, NREL)

These are the "mathematical heuristics" that characterize each concept. They exist in the literature — the challenge is capturing them in a structured, executable, traceable format.

### Fusion 0-D Systems Codes

The fusion community has direct precedent for this: **0-dimensional systems codes** that couple power balance, confinement scaling, and engineering constraints into a self-consistent model that can be evaluated parametrically.

**PROCESS** (UKAEA) [^process] is the most established open-source example. It calculates fusion reactor parameters self-consistently from first principles: 0-D power balance + energy confinement scaling + engineering constraints → optimize a figure of merit (e.g., LCOE or major radius). PROCESS demonstrates exactly the "lightweight analytical model" pattern at the concept level.

**POPCON** (Plasma Operation Contour) diagrams [^popcon] map the steady-state operating space by enforcing zero-dimensional power and particle balance. They are the minimal executable model of plasma performance — one chart tells you whether a given (density, temperature) operating point is physically accessible.

**OpenPOPCON** [^openpopcon] is a modern open-source implementation. **PLASMOD** [^plasmod] extends to 1-D transport, representing the progression from 0-D screening to higher fidelity.

### Computational Notebooks as Design Artifacts

The natural container for "narrative + math + executable model" is the **computational notebook**. Knuth's literate programming (1984) [^knuth1984] introduced the core idea: interleave human-directed narrative with machine-executable code, so the document *is* the program.

Stephen Wolfram's "computational essay" concept [^wolfram2017] refines this for scientific/engineering contexts: an intellectual story told through collaboration between author and computer, where code produces results that fit the narrative. Jupyter notebooks are the standard open-source implementation [^jupyter-eng].

For 1cFE, each fusion concept could be a **computational notebook** that:

1. **Narrates** the concept (confinement scheme, fuel, operating regime) with literature citations
2. **Defines** the analytical relationships (power balance, confinement scaling, cost CERs) as executable Python
3. **Evaluates** baseline performance (LCOE estimate, key sensitivities)
4. **Documents** assumptions, limitations, and open questions

This is both a research artifact and a machine-readable specification. The formulas in the notebook become the source of truth for later SysML formalization.

### Symbolic Regression: Discovering Formulas from Data

When analytical relationships aren't available from the literature — or when you want to verify/simplify literature formulas against simulation data — **symbolic regression** discovers parsimonious mathematical expressions from data.

**PySR** (Cranmer et al., 2023) [^cranmer2023] is the leading open-source tool: evolutionary search over expression trees, Pareto-optimal trade-off between accuracy and complexity, Julia backend with Python interface. It has been used to rediscover known physics laws and discover new empirical correlations.

For fusion, symbolic regression could extract compact CERs from PROCESS/PLASMOD runs, or simplify complex empirical confinement scalings into interpretable forms suitable for rapid concept evaluation.

### Key references

[^nasa-ceh]: NASA. *Cost Estimating Handbook Version 4.0, Appendix K.* https://www.nasa.gov/wp-content/uploads/2020/11/ceh_appk.pdf

[^price-validation]: NASA. "Blind Study Validating Parametric Costing Tools PRICE." https://ntrs.nasa.gov/api/citations/20200003013/downloads/20200003013.pdf

[^nasa-lifecycle]: NASA. "Estimating the Life Cycle Cost of Space Systems." https://ntrs.nasa.gov/api/citations/20160001190/downloads/20160001190.pdf

[^process]: Kovari, M. et al. "PROCESS: A systems code for fusion power plants." *Fusion Engineering and Design.* GitHub: https://github.com/ukaea/PROCESS. Technical: https://scientific-publications.ukaea.uk/wp-content/uploads/PROCESS-PHYSICS-PAPER-15.PDF

[^popcon]: Houlberg, W.A. et al. (1982). "Contour Analysis of Fusion Reactor Plasma Performance." *Nuclear Fusion* 22(7), 935. https://www.osti.gov/biblio/5258172

[^openpopcon]: Hansec. OpenPOPCON. https://github.com/hansec/OpenPOPCON

[^plasmod]: Fable, E. et al. (2019). "Plasma physics for fusion reactor system codes: framework and model code PLASMOD." *Fusion Engineering and Design* 130, 131-136. https://doi.org/10.1016/j.fusengdes.2018.03.019

[^knuth1984]: Knuth, D.E. (1984). "Literate Programming." *The Computer Journal* 27(2), 97-111.

[^wolfram2017]: Wolfram, S. (2017). "What Is a Computational Essay?" https://writings.stephenwolfram.com/2017/11/what-is-a-computational-essay/

[^jupyter-eng]: Barba, L.A. et al. *Teaching and Learning with Jupyter.* https://jupyter4edu.github.io/jupyter-edu-book/

[^cranmer2023]: Cranmer, M. (2023). "Interpretable Machine Learning for Science with PySR and SymbolicRegression.jl." *arXiv:2305.01582.* GitHub: https://github.com/MilesCranmer/PySR

---

## 5. The Data Model: What a "Logical Model" Looks Like Concretely

Synthesizing the above, here's what a structured representation of a fusion concept could look like — lightweight enough for the research phase, structured enough to be machine-processable and to feed SysML formalization.

### Proposed schema (JSON-LD compatible)

The representation should capture four kinds of information:

1. **Morphological identity**: Which options from the design space this concept selects
2. **Qualitative knowledge**: Challenges, pros/cons, design rationale (QOC arguments)
3. **Quantitative relationships**: Analytical formulas, parameter ranges, CERs
4. **Provenance**: Where each piece of knowledge came from

**JSON-LD** [^jsonld] is the recommended serialization: human-readable, version-controllable in git, queryable via SPARQL when loaded into a triple store, and natively compatible with LLM ingestion. A recent (2025) paper demonstrated automated construction of a knowledge graph specifically for nuclear fusion energy using LLMs and structured data [^fusion-kg].

### Example structure

```yaml
concept:
  name: "Compact Advanced Tokamak (CATF-MFE)"
  family: "Magnetic Fusion Energy"

  morphology:
    confinement: "tokamak"
    fuel: "DT"
    heating: ["NBI", "ECRH"]
    blanket: "solid ceramic breeder"
    magnets: "HTS (REBCO)"
    plasma_regime: "advanced tokamak (high bootstrap fraction)"

  qualitative:
    challenges:
      - "Disruption mitigation at high plasma pressure"
      - "Tritium self-sufficiency with solid breeder"
      - "Neutron damage to first wall materials"
    pros:
      - "Most experimentally validated confinement approach"
      - "Strong empirical confinement scaling database"
      - "HTS magnets enable compact geometry"
    cons:
      - "Complex geometry (toroidal, limited access)"
      - "Disruption risk increases with plasma pressure"
      - "Tritium handling infrastructure"
    design_rationale:
      - question: "Why compact?"
        answer: "B^4 fusion power scaling means doubling field ~ 16x power density"
        criteria: ["capital_cost_per_watt", "neutron_wall_loading"]

  formulas:
    power_balance:
      expression: "P_fusion = n_e^2 * sigma_v * E_fusion * V_plasma / 4"
      source: "Freidberg, Plasma Physics and Fusion Energy (2007), Ch. 3"
      parameters:
        n_e: { description: "electron density", unit: "m^-3", range: [1e19, 3e20] }
        sigma_v: { description: "DT reactivity", unit: "m^3/s", note: "function of T_i" }
        V_plasma: { description: "plasma volume", unit: "m^3" }

    confinement_scaling:
      expression: "tau_E = 0.0562 * I_p^0.93 * B_T^0.15 * n_e^0.41 * P^-0.69 * R^1.97 * kappa^0.78 * epsilon^0.58 * M^0.19"
      source: "ITER Physics Basis, Nucl. Fusion 39 (1999) 2175, Eq. (20) — IPB98(y,2)"
      note: "Empirical multi-machine scaling, H-mode"

    magnet_cost:
      expression: "C_magnet = k * B^2 * R^3"
      source: "Stored energy scaling; Woodruff et al. arXiv:2601.21724"
      parameters:
        k: { description: "cost coefficient", unit: "$/J", note: "depends on conductor type" }

    blanket_cost:
      expression: "C_blanket = A_surface * t_blanket * rho_material * c_material * f_manufacturing"
      source: "Sheffield & Milora, Fus. Eng. Des. 86 (2011)"

  provenance:
    primary_sources:
      - "Freidberg, J.P. (2007). Plasma Physics and Fusion Energy. Cambridge University Press."
      - "ITER Physics Basis (1999). Nucl. Fusion 39, 2175-2249."
      - "Woodruff, S. et al. (2026). arXiv:2601.21724."
    data_quality: "Confinement scaling: high confidence (multi-machine database). Cost scaling: moderate (limited fusion construction data)."
```

This is not SysML. It's a **pre-formal specification** that captures what the literature says in a structured way. The morphology section traces to the design space. The qualitative section captures what a domain expert would tell you. The formulas section captures what you'd put in a 0-D systems code. The provenance section makes everything traceable.

### Why JSON-LD / YAML?

Several properties matter for the research phase:

- **Git-friendly**: Text format, diffable, mergeable — essential for collaborative research
- **Human-readable**: Researchers can read and edit directly, unlike RDF/XML or SysML textual notation
- **Machine-parseable**: Standard formats with mature tooling (Python yaml/json libraries, JSON Schema validation)
- **LLM-compatible**: Can be ingested directly by Claude or other LLMs for reasoning, comparison, and eventually SysML generation
- **Evolvable**: Easy to add fields, restructure, or migrate to richer representations as needs emerge

### Key references

[^jsonld]: Sporny, M., Longley, D., Kellogg, G., Lanthaler, M., & Lindström, N. (2020). "JSON-LD 1.1: A JSON-based Serialization for Linked Data." W3C Recommendation. https://www.w3.org/TR/json-ld11/

[^fusion-kg]: Lee, H.J. et al. (2025). "Automated Construction of a Knowledge Graph of Nuclear Fusion Energy for Effective Elicitation and Retrieval of Information." *arXiv:2504.07738.* https://arxiv.org/abs/2504.07738

---

## 6. The Pipeline: From Concept Research to SysML

The frameworks above fit together as a pipeline — not a rigid process, but a natural progression of formalization:

### Phase 1: Map the design space (Morphological Analysis)

Define the dimensions (confinement, fuel, heating, blanket, magnets, ...) and options for each. Apply CCA to eliminate infeasible cross-combinations. Output: a morphological field with ~10-50 internally consistent configurations.

**Artifact**: Morphological matrix with CCA annotations (spreadsheet or structured data).

### Phase 2: Document each concept (QOC + Engineering Model Cards)

For each surviving configuration, create a concept card documenting: identity, challenges, pros/cons, design rationale (QOC), and preliminary analytical relationships from the literature.

**Artifact**: YAML/JSON-LD files per concept, one per leaf of the decision tree.

### Phase 3: Make the math executable (Computational Notebooks)

For each concept, implement the analytical formulas in Python (Jupyter notebooks). Run baseline evaluations: estimate LCOE, identify dominant cost drivers, map sensitivity to key parameters. Use 0-D fusion codes (PROCESS, OpenPOPCON) as reference points.

**Artifact**: Jupyter notebooks that are simultaneously documentation and executable models.

### Phase 4: Screen and prioritize (Sensitivity Analysis + Pugh/Trade Study)

Run Morris screening [^salib] across concepts to identify which parameters dominate LCOE for each approach. Use Pugh matrices [^pugh] or NASA trade study methodology [^nasa-trade] to systematically compare concepts against criteria (LCOE potential, TRL, risk, timeline).

**Artifact**: Parameter importance rankings, concept comparison matrices.

### Phase 5: Formalize the winners (SysML v2)

For the most promising concepts (those that survive screening and show plausible sub-cent corridors), formalize the physics and cost relationships as SysML v2 calculation definitions, constraint definitions, and requirement definitions. Use the YAML concept cards and Jupyter notebooks as primary data sources.

**Artifact**: SysML v2 models in `fusion-tea/models/`, validated by `agentic-mbse`, code-generated by `sysml-codegen`.

### The key insight

Each phase increases formalization and decreases breadth. Morphological analysis is broad but shallow. Concept cards add structure but no execution. Notebooks add execution but no formal semantics. SysML adds formal semantics but requires significant investment per concept.

The pipeline is designed so that **you invest formal modeling effort only in concepts that have survived lighter-weight screening**. The pre-formal representations (YAML, notebooks) are not throwaway — they become the `knowledge/` layer that grounds and validates the SysML models.

### Key references

[^salib]: Herman, J. & Usher, W. "SALib: An open-source Python library for Sensitivity Analysis." https://salib.readthedocs.io/

[^pugh]: Pugh, S. (1991). *Total Design: Integrated Methods for Successful Product Engineering.* Addison-Wesley. See also: Burge, S. (2009). "The Systems Engineering Tool Box — Pugh Matrix." https://www.burgehugheswalsh.co.uk/uploaded/1/documents/pugh-matrix-v1.1.pdf

[^nasa-trade]: Baker, J.D. (2002). "Survey of Trade Study Methods for Practical Decision-Making." NASA. https://www.nasa.gov/wp-content/uploads/2016/10/survey_of_trade_study_methods_-_baker.pdf

---

## 7. Related Work: What Exists in Adjacent Domains

### ESA Concurrent Design Facility

ESA's CDF [^esa-cdf] at ESTEC has run >100 concurrent design studies since 2000, reducing pre-Phase A duration from months to weeks. The methodology uses an **Integrated Design Model** (a shared spreadsheet/database) where multidisciplinary teams work simultaneously, with immediate feedback between subsystems.

The CDF demonstrates that lightweight, parametric models (essentially fancy spreadsheets with linked variables) are sufficient for concept-level exploration when the goal is screening, not detailed design. The 1cFE approach is conceptually similar but with more formal structure (YAML → SysML) and AI augmentation.

### NASA TIES Methodology

NASA's **Technology Identification, Evaluation, and Selection (TIES)** framework [^ties] combines morphological matrices with Response Surface Methodology and Monte Carlo simulation for concept evaluation under uncertainty. TIES generates the concept space morphologically, builds response surfaces from a DOE, and evaluates probabilistically.

This is close to what 1cFE needs but oriented toward technology selection rather than cost target backcasting.

### Modelica / Equation-Based Modeling

**Modelica** [^modelica] is an open-standard, equation-based modeling language for multi-domain physical systems. Unlike procedural code, Modelica defines systems as sets of equations (differential-algebraic) without prescribed execution order — the solver figures out causality.

For the concept phase, Modelica is arguably overkill — its strength is in detailed behavioral simulation, not lightweight parametric screening. However, Modelica's *philosophy* (declare relationships, let the tool solve) is aligned with the SysML v2 approach to constraint definitions. Concept-level Modelica models could serve as an intermediate formalization between notebooks and SysML.

### Pyomo / CasADi for Algebraic Optimization

**Pyomo** [^pyomo] and **CasADi** [^casadi] provide Python-embedded algebraic modeling for optimization and sensitivity analysis. Both allow defining cost and physics relationships as symbolic expressions, computing derivatives automatically, and solving constrained optimization problems.

For the concept phase, these are useful when analytical relationships are known and you want to answer "what parameter values minimize LCOE subject to physics constraints?" directly — without going through a full simulation pipeline. They sit naturally between Jupyter notebooks (pure forward evaluation) and SysML-generated TEAx pipelines (full formal model).

### Key references

[^esa-cdf]: Bandecchi, M. et al. (2000). "The ESA/ESTEC Concurrent Design Facility." *Proceedings of the 2nd European Systems Engineering Conference.* https://technology.esa.int/lab/concurrent-design-facility

[^ties]: Kirby, M.R. & Mavris, D.N. (2000). "TIES for Dummies." Georgia Tech / NASA. https://ntrs.nasa.gov/api/citations/20030032969/downloads/20030032969.pdf

[^modelica]: Modelica Association. https://modelica.org/. See also: Fritzson, P. (2014). *Principles of Object-Oriented Modeling and Simulation with Modelica 3.3.* Wiley-IEEE Press.

[^pyomo]: Hart, W.E., Laird, C.D., Watson, J.-P., et al. (2017). *Pyomo — Optimization Modeling in Python.* Springer, 2nd ed. https://doi.org/10.1007/978-3-319-58821-6

[^casadi]: Andersson, J.A.E. et al. (2019). "CasADi — A software framework for nonlinear optimization and optimal control." *Mathematical Programming Computation* 11(1), 1-36. https://doi.org/10.1007/s12532-018-0139-4

---

## 8. Synthesis: What to Actually Build

Given the state of 1cFE's toolchain and the research above, here's what I'd recommend.

### The representation layer: YAML concept files

Create a standard schema for fusion concept descriptions (as sketched in Section 5). Store them in `fusion-tea/knowledge/concepts/` or similar. Each file captures one leaf of the decision tree: morphological identity, qualitative knowledge, analytical formulas, and provenance. Version-control in git.

This is the **source of truth** for what each concept is and what the literature says about it. It replaces unstructured research notes with something that's both human-readable and machine-parseable.

### The executable layer: Jupyter notebooks per concept

For each concept file, a companion notebook implements the analytical relationships in Python and runs baseline evaluations. The notebook imports formulas from the YAML (or defines them inline with clear mapping to the YAML), computes LCOE under nominal assumptions, and runs one-at-a-time sensitivity sweeps on key parameters.

These notebooks are the "living specifications" that validate the analytical relationships work before investing in SysML formalization.

### The comparison layer: Morphological matrix + screening

A master morphological matrix (could be a spreadsheet, a structured YAML, or a simple Python data structure) defines the design space dimensions and options. CCA annotations mark infeasible combinations. A Pugh-style comparison matrix or NASA trade study scores surviving concepts against criteria.

### The formalization bridge: Concept → SysML

When a concept is ready for formal modeling, the YAML file and Jupyter notebook become the primary data sources for authoring SysML v2. The morphological identity maps to SysML `part def` hierarchy. The analytical formulas map to `calc def` blocks. The constraints map to `constraint def` and `requirement def` elements. Provenance maps to SysML comments and `knowledge/SOURCE_INDEX.md` entries.

This is not automated (SysML authoring requires engineering judgment) but it's **structured** — the concept card tells you exactly what needs to be formalized, with traceability to sources.

### What not to build

- Don't build a knowledge graph (Neo4j, RDF) at this stage — the number of concepts is small enough that flat files with cross-references suffice. A KG becomes valuable when there are hundreds of concepts and complex queries, not dozens.
- Don't build a custom DSL — YAML + Python is sufficient for the concept phase, and SysML v2 is the target formal language.
- Don't build a GUI — the audience is a small technical team; text files and notebooks are faster to iterate than a visual tool.

---

## Appendix: Tool Summary

| Tool | Role | Phase | Status |
|------|------|-------|--------|
| YAML/JSON-LD | Concept specification format | 1-2 | Standard; no special tooling needed |
| Jupyter | Executable concept models | 2-3 | Standard; already in use |
| SALib | Sensitivity screening | 3-4 | Production-ready Python library |
| PROCESS | Reference 0-D fusion systems code | 3 | Open-source (UKAEA), Python |
| OpenPOPCON | Reference POPCON implementation | 3 | Open-source, Python |
| PySR | Symbolic regression (formula discovery) | 3 | Open-source, Python/Julia |
| Pyomo | Algebraic optimization | 3-4 | Production-ready Python library |
| CasADi | Symbolic differentiation + optimization | 3-4 | Production-ready Python library |
| GPkit | Geometric programming (convex submodels) | 3-4 | Stable Python library (MIT) |
| Pugh matrix | Concept screening | 4 | Manual method; no special tool needed |
| SysML v2 / syside | Formal modeling | 5 | Available via Sensmetry license |
| sysml-codegen | Code generation from SysML | 5 | 1cFE internal tool |
