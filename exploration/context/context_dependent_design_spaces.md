1cFE RESEARCH

**Context-Dependent Design Spaces**

Modeling Fusion Concept Diversity with Generative Decision Structures

Working Document --- February 2026

Reid Westwood, Systems Architect

1cFE --- Astera Institute

*This document explores the hypothesis that the fusion design space is not well-captured by fixed taxonomies or static decision trees. Instead, each architectural choice generates new sub-problems that reshape the downstream decision landscape---a **context-dependent** structure that requires generative models rather than enumerative ones.*

# 1. Introduction and Motivation

The 1cFE project asks what must be true for fusion energy to reach a levelized cost of electricity at or below \$0.01/kWh. Answering this requires modeling a diverse set of fusion approaches---from compact tokamaks to laser-driven inertial confinement to exotic lattice and orbital schemes---within a common analytical framework.

A natural first step is to organize these approaches into a taxonomy: a decision tree or morphological matrix that maps the design space. But in attempting this, a fundamental problem emerges: the fusion design space does not decompose into a fixed set of independent dimensions. The relevant design decisions, and even the relevant design questions, change depending on which architectural path you are on.

Choosing deuterium-tritium (D-T) as a fuel creates a neutron shielding problem that dominates downstream engineering. Choosing proton-boron-11 (p-B11) eliminates that problem entirely but creates an extreme plasma temperature challenge that D-T concepts never face. The top-level requirement "ensure safety" decomposes into fundamentally different sub-requirements depending on the fuel choice---and those sub-requirements generate further decisions that are unique to each branch.

This document formalizes this observation, surveys the theoretical frameworks that illuminate it, and proposes an experimental test: a structured comparison of fusion startup concepts that measures how much "context-sensitivity" the design space actually exhibits.

# 2. The Core Insight: Context-Dependent Design Spaces

The standard approach to organizing a design space assumes that you can define a fixed set of dimensions (e.g., confinement type, fuel, heating method, energy capture), enumerate the possible values along each dimension, and then represent any concept as a point in this space. This is the foundation of morphological analysis, and it works well when the dimensions are genuinely independent and universally applicable.

The hypothesis explored here is that the fusion design space violates this assumption in a fundamental way. Specifically:

-   The set of relevant design dimensions is not fixed---it changes depending on prior architectural choices.

-   Each major design decision generates new sub-problems that become first-class design dimensions on that branch but do not exist on other branches.

-   Top-level requirements (safety, structural soundness, economic viability) decompose differently depending on the path through the design space.

-   There is no single canonical ordering of decisions---different traversal orders through the same space produce differently-shaped decision structures.

If this hypothesis is correct, then any fixed-column taxonomy of fusion concepts will necessarily contain a high density of "N/A" cells---questions that are simply not relevant to certain approaches. The N/A density becomes a measurable indicator of context-sensitivity in the design space.

# 3. Theoretical Frameworks

Several intellectual traditions illuminate different facets of this problem. None captures it completely, but together they form a useful toolkit.

## 3.1 Alexander's Pattern Language and Generative Sequences

Christopher Alexander's A Pattern Language (1977) organized 253 design patterns for architecture and urban planning into a hierarchy from large scale (regional planning) to small scale (construction details). The patterns were meant to be applied roughly in order---large-scale decisions create the context that makes smaller-scale decisions meaningful.

In his later work, particularly The Nature of Order (2002--2004), Alexander moved beyond the static catalog toward generative sequences: design as a step-by-step unfolding where each step depends on all previous steps, and the order of decisions changes the outcome. He demonstrated that placing a garden before a building volume produces a fundamentally different result than the reverse---not just a rearranged version of the same design, but a different kind of design with different downstream questions.

**Relevance to fusion:** Alexander's generative sequences capture the core dynamic---that the act of making a design choice reshapes the problem space for subsequent choices. The primitive requirements in a fusion design (net energy, safety, structural soundness) are analogous to Alexander's large-scale patterns: invariant conditions that get decomposed differently depending on the generative path taken.

## 3.2 Zwicky's General Morphological Analysis and CCA

Fritz Zwicky's General Morphological Analysis (GMA) provides a systematic method for mapping multi-dimensional design spaces. The approach defines a set of parameters (dimensions), enumerates the possible values for each, constructs a morphological box (the Cartesian product of all values), and then uses Cross-Consistency Assessment (CCA) to prune logically, empirically, or normatively incompatible pairs.

CCA is powerful because the pruning is quadratic in the number of conditions even though the configuration space is exponential---it makes enormous spaces tractable. The Swedish Morphological Society has applied this to defense planning, policy analysis, and technology forecasting.

**Limitation for fusion:** GMA assumes fixed dimensions. CCA can handle "these two values are incompatible" (e.g., p-B11 fuel is incompatible with standard lithium blanket tritium breeding), but it cannot handle "this value creates an entirely new parameter axis." When choosing D-T fuel generates a "tritium breeding approach" dimension that simply does not exist for p-B11 concepts, GMA forces you to either include the dimension (with N/A entries for non-D-T concepts) or omit it (losing information for D-T concepts). Neither option is satisfactory.

## 3.3 AND/OR Graphs with Context-Dependent Subproblem Generation

AND/OR graphs, originating from Nilsson's work in AI problem-solving (1971), represent problems with two kinds of structure. OR nodes represent choices: pick one approach from several alternatives. AND nodes represent decompositions: to solve this problem, you must solve all of these sub-problems. A "solution" to an AND/OR graph is a subtree where every OR node has exactly one selected child and every AND node has all children solved.

In a standard AND/OR graph, the entire graph structure is defined upfront. The search process explores it, but the topology is fixed. What the fusion design space requires is a generalization: a lazily-evaluated AND/OR graph where the children of an AND node are not pre-specified but are generated as a function of the path from the root.

Concretely: once you choose D-T + tokamak (OR node resolved), the "solve this concept" AND node generates a specific set of children---plasma confinement, tritium breeding, neutron shielding, heat exhaust, remote maintenance. These children do not exist until the OR node is resolved. A different OR resolution (p-B11 + FRC) generates a completely different set of AND children: extreme-temperature plasma confinement, bremsstrahlung management, direct energy conversion, recirculating power management.

**Power of this model:** It captures both the divergence (one choice spawns multiple new sub-problems) and convergence (different paths can lead to shared challenges, e.g., "high-temperature structural materials" appears via multiple routes) that characterize the real fusion design space. The lazy evaluation property---nodes are generated on demand---mirrors the insight that you cannot enumerate the full space upfront.

3.4 Context-Sensitive Grammars

Formal language theory provides a useful analogy. A context-free grammar has fixed production rules: symbol A always expands the same way regardless of context. A context-sensitive grammar allows A to expand differently depending on its surrounding symbols. The Chomsky hierarchy classifies languages by the expressive power required to generate them.

The fusion design space is "context-sensitive" in this sense: the production rule for "solve the safety problem" depends on the symbols (design choices) that surround it in the derivation. This is more than a metaphor---it suggests that any fixed-column taxonomy (which is essentially a regular or context-free description) will be inherently lossy when applied to a context-sensitive space.

3.5 Design as Exploring Constraints (Gross)

Mark Gross's MIT thesis, Design as Exploring Constraints, directly addresses the path-dependent nature of design spaces. Gross demonstrates that in architectural design, the alternatives available at any stage depend on previous decisions, and different sequences of "fixes" through the same constraint network reveal different results. The same set of constraints, explored in a different order, yields different designs---because the path through constraint space determines which constraints become active and binding.

**Relevance:** This is precisely the phenomenon we observe in fusion. The constraint "manage 14 MeV neutrons" only activates on the D-T branch. The constraint "achieve T\_i \> 100 keV" only activates on the p-B11 branch. The path determines which constraints bind, and the binding constraints generate the next set of design decisions.

3.6 The IDEA Framework (LLM + MCTS)

Recent work on AI-assisted design space exploration, particularly the IDEA framework, uses large language models for constraint generation and Monte Carlo Tree Search for exploration. The key innovation is that constraints are discovered during exploration rather than defined upfront---the search process generates new constraints and design dimensions as it traverses the space.

This is conceptually close to what the fusion design space requires: a search process that generates the decision structure as it goes, rather than navigating a pre-defined map.

# 4. Application to Fusion: Measuring Context-Sensitivity

The theoretical frameworks above suggest that the fusion design space is genuinely context-dependent. But how much context-dependence actually exists? Is it a minor inconvenience (a few N/A cells in a mostly-full matrix) or a fundamental structural property (large regions of the matrix are inapplicable to large subsets of concepts)?

To answer this empirically, we propose a structured experiment using the set of currently active fusion startups as the concept population.

## 4.1 Why Startups?

Using startups as the concept set provides several advantages. They represent real, funded, engineering-committed approaches---not hypothetical combinations that might be physically possible but that no one has seriously pursued. They provide a natural boundary for what counts as an "established concept" (someone has raised capital to build it) versus a hypothetical one, which would otherwise be difficult to draw. The set is large enough to be interesting (\~20+ companies) but small enough to analyze manually. And they span a wide range of the design space, from conventional tokamaks to exotic lattice confinement.

## 4.2 The Differentiation Table

The first step is to construct a table where rows are fusion startup concepts and columns are decision categories. The table must satisfy two constraints: no two rows can be identical (every concept must be distinguishable), and columns should be the minimum set required to achieve this.

An initial table with 13 columns and 21 startup concepts is presented in Section 5. This is a first draft intended to be refined through the experimental process described below.

# 5. Fusion Startup Differentiation Table (Draft)

The following table attempts to differentiate 21 fusion startups across 13 decision categories. Initial columns: Confinement Family, Confinement Concept, Fuel, Primary Heating, Energy Capture, Plasma State, Magnet Type, Tritium Breeding, Neutron Shielding, Pulsed/Steady-State, Repetition Rate Concept, and Driver Technology.

**N/A density:** Of 252 non-name cells, 26 are marked N/A (10.3%). These represent questions that are structurally irrelevant to the given approach---not unknown answers, but inapplicable questions. This is a lower bound; a more granular table would expose more context-dependent dimensions.

Note: this table is presented in landscape orientation on the following page.

| Company | Conf. Family | Confinement Concept | Fuel | Primary Heating | Energy Capture | Plasma State | Magnet Type | Tritium Breeding | Neutron Shielding | Pulsed/Steady | Rep Rate | Driver Technology |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CFS | MFE | Compact tokamak | D-T | RF + Ohmic | Thermal (steam) | Burning | HTS | Li blanket | Required | Steady-state | *N/A* | HTS magnets |
| Helion | MFE | FRC (pulsed) | D-He3 | Compression + beams | Direct (flux) | Transient | Pulsed EM | Self-bred (DD side) | Minimal | Pulsed | ~1 Hz | Pulsed EM coils |
| TAE | MFE | FRC (beam-driven) | p-B11 (target) | Neutral beams | Direct + thermal | Sustained FRC | Conventional | *N/A* | *N/A* | Steady-state | *N/A* | Neutral beams |
| General Fusion | MIF | Magnetized target | D-T | Compression | Thermal (liq. metal) | Compressed | None (self) | Liq. metal wall | Liq. metal wall | Pulsed | ~1 Hz | Pneumatic pistons |
| Zap Energy | MFE | Z-pinch (SFS) | D-T | Ohmic (pinch) | Thermal (steam) | Pinch plasma | None (self) | TBD | Required | Pulsed | High freq. | Pulsed power |
| Pacific Fusion | MIF | Mag-driven ICF | D-T | Implosion | Thermal | Compressed | Pulsed | TBD | Required | Pulsed | TBD | Pulsed power |
| First Light | IFE | Projectile ICF | D-T | Projectile impact | Thermal (steam) | Compressed | *N/A* | Required | Required | Pulsed | ~1 Hz | Electromagnetic gun |
| Tokamak Energy | MFE | Spherical tokamak | D-T | RF + NBI | Thermal (steam) | Burning | HTS | Li blanket | Required | Steady-state | *N/A* | HTS magnets |
| Proxima Fusion | MFE | Stellarator (QI) | D-T | RF (ECRH) | Thermal (steam) | Burning | HTS | Li blanket | Required | Steady-state | *N/A* | HTS magnets |
| Type One Energy | MFE | Stellarator (modular) | D-T | RF (ECRH) | Thermal (steam) | Burning | HTS | Li blanket | Required | Steady-state | *N/A* | HTS magnets |
| Thea Energy | MFE | Stellarator (planar) | D-T | RF | Thermal (steam) | Burning | HTS (planar) | Li blanket | Required | Steady-state | *N/A* | Planar HTS coils |
| Xcimer | IFE | Laser ICF | D-T | Laser (excimer) | Thermal (steam) | Compressed | *N/A* | Required | Required | Pulsed | ~10 Hz | Excimer laser |
| Focused Energy | IFE | Laser ICF (FI) | D-T | Laser (fast ign.) | Thermal (steam) | Compressed | *N/A* | Required | Required | Pulsed | ~1 Hz | Solid-state laser |
| EX-Fusion | IFE | Laser ICF (FI) | D-T | Laser (fast ign.) | Thermal (steam) | Compressed | *N/A* | Required | Required | Pulsed | High freq. | High-rep laser |
| HB11 Energy | IFE | Laser ICF | p-B11 | Laser (PFI) | Direct (charged) | Compressed | *N/A* | *N/A* | *N/A* | Pulsed | ~1 Hz | Pico/nanosec laser |
| Marvel Fusion | IFE | Laser ICF (nanostructured) | p-B11 | Ultra-short laser | Direct (charged) | Compressed | *N/A* | *N/A* | *N/A* | Pulsed | TBD | Ultra-short pulse laser |
| Realta Fusion | MFE | Magnetic mirror | D-T | RF + NBI | Thermal (steam) | Confined | HTS | Li blanket | Required | Steady-state | *N/A* | HTS magnets |
| SHINE Tech | Hybrid | Subcritical (IEC) | D-T | Electrostatic | Neutron apps | Non-burning | *N/A* | *N/A* | *N/A* | Steady-state | *N/A* | IEC accelerator |
| NT-Tao | MFE | Compact (propri.) | D-D | Ultra-fast heating | Thermal | High-density | Compact | Self-bred | Reduced | Pulsed | High freq. | Proprietary |
| Astral Systems | Other | Lattice + IEC | D-D / D-T | Lattice / electro. | Neutron capture | Solid-state | *N/A* | Integrated | Integrated | Steady-state | *N/A* | Lattice medium |
| Avalanche | Other | Orbital confine. | D-D / D-T | Electrostatic | TBD | Orbital ions | None | TBD | TBD | Steady-state | *N/A* | Micro-scale E-fields |

**Table reads:** Gray italic N/A cells indicate structurally inapplicable questions. TBD indicates the approach requires an answer but it is not yet public. Shaded rows alternate for readability.

# 6. Experimental Plan

The goal is to determine how much context-sensitivity the fusion design space actually exhibits, and whether a more expressive formal model (such as the lazily-evaluated AND/OR graph) provides meaningful advantages over a flat morphological table.

## 6.1 Phase 1: Minimum Column Set Discovery

The first question is: what is the minimum set of columns needed to uniquely distinguish every fusion startup concept?

**Algorithmic approach:** This is equivalent to finding a minimum discriminating set in a feature-selection problem. For 21 concepts and \~13 candidate columns, the search space is manageable (2¹³ = 8,192 subsets). A greedy set-cover approach would work: start with the column that creates the most unique partitions, add columns until all rows are distinct. Alternatively, use an information-theoretic criterion (maximum mutual information with concept identity) to rank columns.

**LLM-assisted approach:** Task an AI agent with an iterative refinement loop. Provide the full current table, ask it to propose a reduced column set, check for uniqueness violations, and iterate. Maintain a running log of changes and results. This is the "easy mode" approach---less formally optimal but faster to execute and more flexible in handling qualitative distinctions.

**Expected outcome:** We hypothesize that the minimum column set is around 4--6 columns for the current 21-concept set, but that achieving uniqueness with fewer columns forces increasingly coarse-grained distinctions that lose important engineering information.

## 6.2 Phase 2: N/A Density Analysis

With the full (non-minimized) table, measure the N/A density across different column groups.

-   Compute overall N/A rate: what fraction of cells are structurally inapplicable?

-   Compute per-column N/A rates: which decision categories are most concept-dependent?

-   Compute per-row N/A rates: which concepts have the most unique (non-shared) decision structure?

-   Look for block structure: do N/As cluster by confinement family or fuel type? If so, this suggests the context-dependence is driven by a small number of early branching decisions.

**Interpretation:** If N/A density is low (\<10%), the design space is well-captured by a flat table and the context-dependence is minor. If N/A density is high (\>20%) and shows strong block structure, the context-dependence is real and driven by identifiable architectural choices. If N/A density is high but diffuse (no clear block structure), the space may be even more complex than a simple branching model suggests.

## 6.3 Phase 3: Expand Granularity

The initial 13-column table uses relatively coarse categories. Phase 3 expands the table with more granular, engineering-specific columns to see if the N/A density increases or plateaus.

Candidate additional columns include: blanket concept (Li/FLiBe/LiPb/none), coolant type, first wall material, plasma-facing component design, magnet topology, divertor concept (tokamak-specific), beam injection geometry, target fabrication approach (IFE-specific), repetition rate requirement, tritium processing rate, waste classification, and maintenance approach (remote vs. hands-on).

If the N/A density increases substantially with granularity, this confirms that the context-sensitivity is not just a surface-level effect but deepens at every level of engineering detail.

6.4 Phase 4: Formal Model Assessment

Armed with the empirical data from Phases 1--3, we evaluate whether a more expressive formal model provides practical advantages.

### Option A: Annotated Morphological Box (Minimal)

Keep the flat table structure but add explicit annotations for which columns apply to which concept families. This is essentially GMA + CCA with an additional "applicability" layer. Low implementation cost, compatible with existing tools, but does not capture the generative structure.

### Option B: Typed AND/OR Graph (Moderate)

Represent the design space as an AND/OR graph where OR nodes are annotated with the sub-problem sets they generate. This captures the context-dependent decomposition explicitly and enables automated reasoning about which questions apply to which paths. Moderate implementation cost; could be represented in SysML v2 using variability and constraint constructs.

### Option C: Generative Sequence Model (Full)

Implement a fully generative model where each design decision triggers a rule-based or LLM-assisted generation of downstream sub-problems. This is the most expressive option and most closely mirrors Alexander's generative sequences, but is the most complex to implement and validate.

The choice between these options should be driven by the empirical findings: if the N/A density is modest and the block structure is clean, Option A may suffice. If the space is deeply context-dependent with complex interactions, the additional expressiveness of Option B or C may be warranted.

# 7. Connections to the 1cFE Toolchain

This inquiry has direct implications for several active workstreams in the 1cFE project.

**The spanning set.** If the design space is context-dependent, then the spanning set is not spanning a fixed-dimensional space but rather spanning the set of distinct generative paths. Two concepts belong in different spanning set entries when they face structurally different design challenges, not just when they have different parameter values.

**SysML v2 model structure.** Context-dependent design spaces suggest that different fusion approaches may need structurally different SysML models, not just different parameter values within a common model. The variability and constraint constructs in SysML v2 (§7.13, §7.20) may provide the right mechanisms for encoding this.

**Full-dimensional TEA.** The current sysml-codegen pipeline exposes all independently variable parameters as entry points. In a context-dependent space, the set of entry points itself is concept-dependent---a D-T tokamak has fundamentally different entry points than a p-B11 laser concept. This is already implicitly handled (different SysML models produce different generated code), but making it explicit could improve the Lens pattern.

**Inverse design.** Backcasting from a cost target through a context-dependent space means that the optimization problem itself changes shape depending on which branch you are on. The search is not over a fixed parameter space but over a space of generative paths, each of which defines a different optimization landscape.

**Cross-concept transfer via shared context.** This may be the most practically valuable implication of the context-dependent framing, and it connects directly back to Alexander's pattern language. If we successfully identify the generative structure of the design space---which sub-problems arise from which architectural choices, and which contexts produce similar downstream challenges---we gain a principled mechanism for transferring solutions across concepts.

Consider: a well-studied concept like the compact D-T tokamak has been modeled in detail. Its tritium breeding subsystem, neutron shielding design, and associated cost models are relatively mature. Now suppose we are fleshing out a less-studied concept---say, a D-T magnetic mirror or a D-T Z-pinch. When we reach the "solve tritium breeding" node in the AND/OR graph, the *context* at that node (D-T fuel, thermal neutron spectrum, similar first-wall conditions) may look structurally similar to the tokamak case, even though the confinement physics is completely different.

If the contexts match at a given sub-problem node, we have a justified reason to borrow the solution---the models, cost estimates, engineering constraints, and even the further decomposition of that sub-problem---from the more mature concept. The transfer is not ad hoc ("tokamaks use lithium blankets, so maybe mirrors should too") but structurally grounded: the sub-problem arose from the same generative path (D-T fuel → neutron management → tritium breeding), so the solution space is genuinely shared.

This is Alexander's pattern language in its most useful form. A pattern is not just a label ("lithium blanket"); it is a problem-solution pair embedded in a context ("when you have 14 MeV neutrons from D-T fusion and need to breed tritium while protecting structural materials, a lithium-bearing blanket with these properties resolves the forces"). The context tells you *when* the pattern applies, and the generative structure tells you *why*. Two concepts that arrive at the same context via different generative paths can share the same pattern---and by extension, the same models and cost estimates.

This has direct practical value for the 1cFE pipeline. Rather than modeling every subsystem of every concept from scratch, we can identify shared sub-problem contexts across the spanning set and reuse validated models where the context justifies it. The context-dependent graph becomes a map of where transfer is safe (shared subgraph) versus where it is not (divergent sub-problems). For exotic or early-stage concepts with limited engineering detail, this provides a principled way to fill in gaps by borrowing from better-understood neighbors in the design space---not based on surface-level similarity, but on verified structural correspondence in the generative decomposition.

# 8. Toward AI-Driven Design Exploration

There is a broader question behind this work that is worth naming explicitly: *how would AI actually drive genuinely new invention in engineering?*

The popular narrative is that AI will "accelerate design." But the mechanism is usually left vague, and when you try to make it concrete, you run into a series of fundamental limitations.

**Pure inference is not invention.** A large language model, at inference time, is sampling from a distribution shaped by its training data. While this can produce outputs that *feel* creative---surprising juxtapositions, elegant syntheses, novel-sounding combinations---it is, by definition, interpolating within the space of what has already been written and thought. It can recombine existing ideas with remarkable fluency, but it cannot generate something that lies outside the convex hull of its training distribution. For incremental engineering improvement, this is often sufficient. For genuine architectural innovation---the kind that produces a qualitatively new approach to a problem---it is not.

**Structured reasoning helps, but hits walls.** Test-time compute techniques (chain-of-thought, tree-of-thought, MCTS-guided reasoning) allow models to explore beyond what a single forward pass would produce. The reasoning traces can land at genuinely interesting ideas by composing familiar elements in unfamiliar ways. This is closer to real invention. But applying structured reasoning directly to complex engineering design runs into two hard constraints:

First, *context limitations*. The amount of domain knowledge, physical data, prior art, constraint relationships, and internal reasoning required to work through a novel fusion plant design far exceeds what fits in a context window. You cannot "one-shot" innovation on a problem this complex---not because the model lacks capability, but because the problem doesn't fit in the model's working memory.

Second, *physical grounding*. Engineering design is ultimately constrained by physical reality. Until we have closed-loop AI systems that can propose experiments, run them, and learn from the results, grounding AI reasoning in real-world data will remain a bottleneck. The model can reason about what *might* work, but validating whether it *does* work requires physical data that may not exist for novel configurations.

**The case for scaffolding.** If pure inference cannot invent, and structured reasoning hits context and grounding limits, then the path forward is likely *external structure*---harnesses and scaffolds that allow AI to explore new designs while staying grounded in physical reality. I believe it is worth investing in the high-level algorithms and data structures that could make this possible, even before we know exactly which formalism will prove most useful.

The context-dependent design space framework developed in this document is one attempt at building such scaffolding. It is unproven, and much of what follows is speculative. But it is worth sketching how the pieces *could*, in theory, meet the needs outlined above.

The *lazily-evaluated AND/OR graph* could give AI a structured search space to explore. Rather than reasoning about an entire fusion plant in one pass, an agent would traverse the graph node by node, making one architectural decision at a time and generating the downstream sub-problems that follow. Each node would be a tractable reasoning problem. The graph structure would help ensure that the agent's exploration stays physically coherent---you cannot arrive at a tritium breeding sub-problem without having first committed to a fuel choice that requires it.

The *pattern library with embedded context* (Section 7, cross-concept transfer) could give AI a grounded knowledge base. Each pattern would be a validated solution---backed by engineering data, cost models, and physical constraints---attached to the context in which it applies. When the agent reaches a sub-problem node, it could query the library: "has this context been solved before?" If yes, it could reuse the solution with some confidence. If no, it would have discovered a genuinely novel sub-problem---a point where real invention (or at minimum, new engineering analysis) is needed.

The *generative sequence* could give AI a mechanism for composing known patterns in novel ways. Alexander's key insight was that the *order* of design decisions matters---the same set of patterns, applied in a different sequence, produces a fundamentally different design. An AI agent traversing the AND/OR graph would be executing a generative sequence. If it explores a path that no human designer has taken---choosing an unconventional combination of fuel, confinement, and heating---it would encounter sub-problems in a novel context. Some of those sub-problems might match known patterns (safe transfer). Others would not (genuine novelty). The graph structure would tell the agent where the frontier of known solutions ends and where new territory begins.

If something like this works, it suggests a model of AI-driven invention that is quite different from the popular narrative: not a single flash of insight from a large model, but a *structured exploration process* where an agent traverses a generative design space, composing validated patterns where the context is familiar, and flagging genuinely novel sub-problems where it is not. The scaffolding would not replace the AI's reasoning---it would focus it on the problems where reasoning can actually make a difference, and ground it in physical data where that data exists.

The investment thesis, then, is not primarily in bigger models or longer context windows. It is in the *algorithms and data structures* that could allow AI to efficiently explore genuinely new designs while leveraging the physical knowledge we already have. The context-dependent AND/OR graph, the pattern library with context-aware transfer, and the generative sequence framework are all candidate components of that scaffolding. Whether they prove to be the right abstractions is an open question---but the *need* for some such scaffolding seems clear.

For fusion specifically, this reframes the question: rather than asking "what does the AI think the best fusion concept is?" (pure inference), we would ask "what happens when we let AI systematically explore the generative design space, composing validated patterns in novel sequences, and identify where the known solution library runs out?" The answer to that question---the map of where known patterns apply and where they don't---would itself be a valuable contribution to the field, even before the AI proposes any novel solutions.

# 9. References

1.  Alexander, C. et al. A Pattern Language. Oxford University Press, 1977.

2.  Alexander, C. The Nature of Order (4 vols). Center for Environmental Structure, 2002--2004.

3.  Zwicky, F. Discovery, Invention, Research through the Morphological Approach. Macmillan, 1969.

4.  Ritchey, T. "General Morphological Analysis: A general method for non-quantified modelling." Swedish Morphological Society.

5.  Nilsson, N. Problem-Solving Methods in Artificial Intelligence. McGraw-Hill, 1971.

6.  Gross, M.D. Design as Exploring Constraints. MIT PhD Thesis, 1986.

7.  Simon, H. The Sciences of the Artificial (3rd ed). MIT Press, 1996.

8.  IDEA Framework: LLM-assisted design space exploration with MCTS. arXiv:2506.10587, 2025.

9.  Dalsgaard, P. and Biskjaer, M. "A Constraint-Based Understanding of Design Spaces." DIS 2014.

10. "Architecture Design Space Generation via Decision Patterns." Systems 12(9):336, MDPI, 2024.

11. Kruchten, P. "Classifying architectural constraints as a basis for software quality assessment." Advanced Engineering Informatics, 2006.
