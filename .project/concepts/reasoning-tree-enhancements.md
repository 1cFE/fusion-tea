# Reasoning Tree: Enhancement Proposals

Companion to: `reasoning-tree-formal-model.md` (definitions), `reasoning-tree-problem-statement.md` (goals)

---

## 0. Foundational Issues in the Current Ontology

The formal model (`reasoning-tree-formal-model.md`) defines the algorithm's objects and operations, but review exposed three issues where the current ontology is underspecified or internally confused. These must be resolved before the enhancements below can be precisely defined.

### 0.1 The prompt for generating constraints is vague

The expansion prompt (`exploration/phase_2a/prompt.md`, line 23) instructs:

> "Derive CONSTRAINTS — what is FORCED by this choice? What is ELIMINATED? What new problems are ACTIVATED that don't exist without this choice?"

This conflates three different things under one label. In engineering practice, these map to distinct concepts with different downstream uses:

- **FORCED**: a derived requirement — choosing D-T fuel means you MUST have a tritium breeding blanket. This is a hard implication traceable through physics.
- **ELIMINATED**: a ruled-out option — choosing D-T fuel means direct energy conversion is NOT the primary extraction path. This is negative space scoped to a specific design variable.
- **ACTIVATED**: a new design dimension — choosing D-T fuel creates a tritium handling problem that didn't exist before. This is closer to a new QUESTION than a constraint.

The prompt treats all three as "constraints" with the same `{condition, consequence, type}` structure. The LLM produces them all in the same list, and they all go into the same registry. But their intended roles differ: FORCED constraints are checkable rules about the design space; ELIMINATED constraints are scoped negative space; ACTIVATED constraints are really downstream questions wearing constraint syntax.

The actual constraints in `exploration/phase_2a/tree.json` confirm this confusion. Compare these two from the closed-magnetic option:

- `{field_topology: closed_toroidal} → {rotational_transform: required}` — this is a genuine derived requirement (FORCED).
- `{plasma_beta: exceeds_threshold} → {mhd_stability: lost}` — this is a conditional physics fact, but "exceeds_threshold" is unspecified. The threshold depends on geometry and profile, which depend on other context. This is more like a caution than a constraint.

**What needs resolution**: Define precisely what a constraint IS — what function it serves in the algorithm, what makes it different from a context entry, and what makes it different from negative space. The current definition ("a claim about the design space") is too broad to guide either the LLM's generation or downstream use.

### 0.2 Context entries lose their question

A context entry (the `context_addition` field of each option) is currently a pair (*choice*, *reasoning*). It does not carry the question it answered. The accumulated context is presented to the LLM as:

```
1. Closed magnetic topology confinement
   Reasoning: This approach distinguishes itself by using field-line
   topology to eliminate end losses...
```

The question ("How should we confine the fusion reaction?") that gave this choice its meaning is absent.

At L0-L1 this works because choices are broad enough to be self-explanatory. At deeper levels it will not. A choice like "dual-coolant FLiBe blanket" without the question "How should tritium be bred given compact toroidal geometry with limited blanket space?" is a design detail with no scope. The *reasoning* field is doing double duty — explaining both what was chosen and why it was a relevant question — but it is not structured to reliably carry both.

In engineering practice, the design record for a trade study always includes: the question (what decision was being made), the options considered, the selection (what was chosen), and the rationale (why). The current context entry carries selection and rationale but drops the question and the alternatives. This makes the accumulated context increasingly opaque as the tree deepens.

**What needs resolution**: The context entry should be (*question*, *choice*, *reasoning*) at minimum — possibly also carrying the rejected alternatives (since knowing what WASN'T chosen is part of the design record). See the actual prompt template at `exploration/phase_2a/prompt.md` (lines 66-70) and the context formatting in `exploration/phase_2a/expand.py` (lines 31-39) for the current implementation.

### 0.3 The intended roles of choices vs. constraints are unclear

The formal model defines both **context entries** (choices that shape future reasoning) and **constraints** (checkable claims in the registry). Both are extracted from the same option analysis. But their intended roles diverge in ways the current design doesn't make operational:

- **Context entries** participate in the algorithm: they go into accumulated context → the LLM sees them → they shape the next expansion. They are the mechanism by which upstream decisions influence downstream reasoning.
- **Constraints** do NOT participate in the algorithm: they go into the constraint registry (*K*), but no part of the expansion process reads *K*. The next LLM call sees accumulated context, NOT the constraint registry. Constraints are a write-only analytical side product.

This means the algorithm has two parallel representations of the same design knowledge — context entries (operational, shape the process) and constraints (inert, stored for post-hoc analysis) — without a clear account of why both exist or how they relate.

The intended distinction was:
- Context entries carry the DECISION (what was chosen and why) — they are narrative and branch-specific
- Constraints carry the IMPLICATIONS (what follows from that decision) — they are supposed to be generalizable rules, applicable to any branch matching their condition

But in practice, constraints are often just the context entry restated in `{condition, consequence}` syntax. The condition `{field_topology: closed_toroidal}` is the choice "closed magnetic topology" under a different name. The constraint adds a consequence, but the condition IS the choice. The constraint format LOOKS like a standalone rule, but its vocabulary comes from the same LLM generation and is not grounded in any shared ontology.

The original vision (see `exploration/algorithm_ideation.md`, Section "Synthesis: Constraint Propagation + ATMS") intended constraints to serve three roles: (1) validated against the 38-concept table, (2) compared across branches for convergence, (3) used for transfer analysis via shared justification sets. None of these are operational. The constraint registry accumulates claims that no part of the system reads back.

**What needs resolution**: Either (a) give constraints an operational role — feed them back into the expansion process, use them for navigation decisions, or make convergence detection real — or (b) merge them into richer context entries that carry both the decision and its structured implications, eliminating the parallel representation.

---

Five enhancements derived from the formal model. Each addresses a structural gap identified by the model's analysis. Ordered by impact. **Enhancements 1-5 assume the foundational issues above (Section 0) are resolved first** — their definitions depend on having clear concepts of what constraints are, what context entries carry, and how both relate to the algorithm.

---

## 1. Question Value — Making Navigation Intentional

### What `select()` represents

In the formal model, `select(oᵢ.downstream_questions)` chooses which design question to investigate next from the set of questions that a given option creates. Currently this is the first element — the LLM's arbitrary ordering within a single generation.

In real concept exploration, this choice is **work sequencing**: given that a trade study has identified several open questions, which do you pursue next? Engineering practice has well-established sequencing strategies — risk-driven (investigate what might kill the concept soonest), critical-path (investigate what blocks the most downstream decisions), and information-value (investigate what resolves the most uncertainty). The algorithm currently uses none of these. It sequences work in the order it happens to come up, which is the engineering equivalent of exploring whatever subsystem the last meeting mentioned.

### What needs to be defined

**Question value**: a function *v*(*q*, *C*, *K*, *T*) → ℝ that scores a candidate question *q* given the accumulated context *C*, the current constraint registry *K*, and the tree state *T*. This is the conceptual gap — there is no definition of what makes one question more worth pursuing than another.

The formal model identifies two dimensions of value, and they may conflict:

**Constraint activation potential.** A question is valuable if its answer would make requirements binding that aren't currently binding. "What fuel?" activates R1 (fuel supply), R4 (energy extraction), and R5 (nuclear environment) in new ways. "What color should the control room be?" activates nothing. In engineering terms, this is risk-driven sequencing — pursue questions that could eliminate options or reveal showstoppers.

**Abstraction descent.** A question is valuable if its answer bridges the gap between the algorithm's physics-level reasoning and the engineering-level vocabulary where validation is possible (formal model, Section 5). "What magnet type?" produces constraints mappable to the table. "What is the maximum achievable beta?" produces rich physics constraints that remain unmappable. For Goal 1 (reproduce table columns), descent is a precondition. In engineering terms, this is the progression from concept selection to preliminary design — at some point you must move from physics trade-offs to engineering choices.

These dimensions can conflict: a question about beta limits has high constraint activation potential (it bears on R2, R3, R6) but low abstraction descent (stays at physics level). A question about magnet type has high abstraction descent but may not activate deep physics constraints. Question value must navigate this tension — which is itself a design question about what the tree is FOR in any given exploration.

### What this enables

With a defined question value function, navigation becomes intentional rather than incidental. Different value functions produce different trees from the same root — making the exploration strategy explicit and adjustable. The tree shape becomes a choice, not an artifact.

---

## 2. Parallel Investigation — Following Multiple Questions per Option

### What the current algorithm discards

Each option *oᵢ* generates *n* downstream questions [*q*₁, …, *q*ₙ] (typically 5-6). The algorithm follows one and discards the rest. These discarded questions are not noise — they are context-dependent design questions that the algorithm correctly identified as created by a specific upstream choice. "Ash handling" in laser IFE, "current drive" in tokamaks — these are real engineering questions that Goal 2 asks for. They exist in the expansion output. They are thrown away.

### What this represents in engineering practice

In real concept exploration, when you choose an approach (say, tokamak confinement), you don't then investigate one downstream question at a time in series. You investigate multiple aspects in parallel: magnet design, fuel cycle, heating method, divertor concept. Each is a separate line of inquiry, pursued by different teams or in different study phases, all within the same concept branch. The results interact — magnet choice constrains blanket space which constrains tritium breeding — but the investigations proceed in parallel.

The current algorithm serializes this inherently parallel structure into a single path. One question is followed; the others are abandoned. The constraint yield is a fraction of what the algorithm's own reasoning identified as relevant.

### What needs to be defined

**Investigation breadth** *N*: how many downstream questions to follow per option. *N* = 1 is the current behavior. *N* = |*downstream_questions*| is full parallel investigation. The right *N* depends on depth — at shallow levels (concept selection), pursuing multiple questions per option is high-value because each opens a different constraint cascade. At deeper levels (detailed design), questions are more specific and their constraint cascades overlap more, so the marginal value of additional questions decreases.

This interacts with Enhancement #1: if question value is defined, parallel investigation becomes "follow the top-*N* valued questions" rather than "follow all" or "follow the first." The combination of ranking and breadth gives the algorithm a deliberate exploration strategy — which questions, how many, at what depth.

### What this enables

More constraints per expansion, more paths for convergence detection (Enhancement #4), faster pruning (more constraints activate more requirements), and directly addresses Goal 2 — the context-dependent questions that are currently generated and discarded would be explored.

---

## 3. Seeding — Design-To Assumptions as Initial Context

### What seeding represents

In engineering, you rarely explore a design space from a blank slate. You enter with assumptions: "we are designing for the European grid market," "we assume HTS magnets are available at $X/kA-m," "our target LCOE is $0.05/kWh." These are not results of the exploration — they are preconditions that constrain it. They change what's viable, what's attractive, and what questions matter. In engineering terminology, these are **design-to requirements** or **technology assumptions**.

In the formal model, a seed *s* is a context entry injected as *C*₀ = [*s*], replacing the empty initial context *C*₀ = []. The expansion mechanism is unchanged — the LLM still sees (*C*, *q*, *R*) and reasons from first principles. But *C* now includes *s* at every node, which changes how R1-R6 interact with the accumulated context at every expansion.

### What needs to be defined

**Seed format**: a context entry *c* = (*choice*, *reasoning*) that describes the assumption and its justification. The reasoning component matters — it's not enough to say "direct energy conversion is cheap"; the seed must include WHY it's being assumed and what implications the assumer expects. This gives the reasoner enough context to trace the seed's effects through R1-R6.

**Seed types** (distinguished by what they constrain):
- **Technology assumption**: "efficient direct energy conversion exists at low cost" — changes what's viable under R3 and R4
- **Constraint removal**: "tritium is freely available in unlimited quantities" — disables constraints driven by R1
- **Requirement tightening**: "LCOE must be below $0.01/kWh" — makes R3 binding earlier
- **Path closure**: "steady-state plasma confinement with no disruptions is impossible" — eliminates the tokamak branch

These types are not formal categories — they describe different ways a seed interacts with the requirement lenses. The algorithm doesn't need to know which type a seed is; the LLM's requirement analysis will trace the effects regardless.

### What this enables

Comparative exploration: run the tree unseeded, then run it with a seed, and compare. The differences — which options survive, which questions emerge, where branches converge — map how the design space changes under the assumption. This directly tests Goal 3. It also tests the formal model's predictions: the model predicts that a seed changes convergence patterns, and the seeded tree either confirms or refutes that prediction.

The deeper analytical value: seeds let you ask counterfactual questions about the design space. "What would the fusion landscape look like if tritium weren't a problem?" is not a hypothetical — it's a precise perturbation of the initial condition whose effects propagate through every downstream expansion. The tree makes those effects traceable.

---

## 4. Convergence Detection — Finding Shared Structure Across Branches

### What convergence represents

When two different engineering teams, working on two different fusion concepts, independently arrive at the same sub-problem — "we need to breed tritium with a TBR > 1.0" — that convergence is meaningful. It means the sub-problem is driven by a shared upstream cause (both chose D-T fuel), not by a coincidence of their respective design paths. The shared cause justifies sharing solutions, models, and cost estimates between the concepts — at least for the parts of the solution that depend only on the shared cause.

In the formal model, convergence is defined as: constraints *κ*_A and *κ*_B from different branches share the same consequence variable while having been derived from different source nodes. The overlapping portion of their conditions defines the transfer scope — what's shared vs. what's concept-specific.

### What is currently missing

The algorithm runs each branch in isolation. The constraint registry accumulates constraints from all branches, but there is no operation that compares constraints ACROSS branches. The data exists — each constraint carries its condition, consequence, and justification — but no process examines the registry for convergence patterns.

This matters because convergence is the primary validation mechanism the formal model identifies for Goal 1 across concepts. If two branches independently derive "D-T fuel → thermal energy conversion," that agreement is stronger evidence than either derivation alone. And the convergence pattern itself is an analytical output — it maps which parts of the design space are shared (driven by common upstream choices) and which are genuinely concept-specific.

### What needs to be defined

**Consequence similarity**: when do two constraints address "the same" consequence? The simplest case is exact variable match (both constrain `energy_conversion`). But the algorithm produces constraints in free-form vocabulary — one branch might say `energy_capture: thermal` while another says `conversion_method: steam_cycle`. These reference the same engineering reality but use different strings. Consequence similarity must handle vocabulary variation, which is itself an instance of the abstraction gap (Section 5 of the formal model).

**Condition overlap**: given two converging constraints, what portion of their conditions is shared vs. divergent? The shared portion defines the transfer scope — the set of contexts where the constraint holds regardless of which branch derived it. The divergent portion identifies what makes the constraint concept-specific — where the same sub-problem has different solutions because of different upstream context.

### What this enables

Transfer analysis becomes operational. Convergence maps — showing which constraints are shared across which branches, with what transfer scope — are the primary knowledge artifact the original vision described (algorithm ideation doc, Phase 2 concept). They answer: "where can I reuse models and cost estimates from a well-studied concept to fill gaps in a less-studied one, and where is that transfer NOT justified?"

---

## 5. Multi-Level Constraint Expression — Bridging Abstraction Levels

### What the abstraction gap means for constraints

The formal model (Section 5) identifies that the algorithm reasons at the physics level while the validation target (the table) operates at the engineering level. The gap narrows through descent (more specific questions force more concrete vocabulary), but may stabilize at an intermediate level where the most analytically interesting constraints live — physics-of-failure applied to engineering concerns.

Currently, each constraint is expressed at whatever abstraction level the LLM happens to reason at. A constraint derived at L0 might say `{field_topology: closed_toroidal}` (physics) while the same structural fact, expressed at the engineering level, would be `{confinement_family: MFE}` (table column). The constraint captures the physics cause; the table records the engineering classification. Both describe the same reality, but they use incommensurable vocabularies.

### What this represents in engineering practice

Engineers routinely express the same fact at multiple levels. A materials engineer says "14 MeV neutron flux causes helium embrittlement in ferritic steels above 10 DPA" (physics-of-failure). A project manager records "first-wall replacement required every 5 years" (engineering consequence). A cost analyst writes "CAS 22.01.02 maintenance cost: $X/year" (cost classification). These are the same constraint — neutron damage limits component lifetime — expressed at different levels for different purposes.

The algorithm currently produces constraints at ONE level per expansion. It doesn't bridge between levels because it isn't asked to.

### What needs to be defined

**Constraint expression level**: a property of how a constraint's condition and consequence are stated, ranging from physics-level (variables like field topology, loss cones, cross-section ratios) through intermediate (physics-of-failure: "disruption severity scales with stored energy per unit volume") to engineering-level (variables like Confinement Family, Magnet Type, Operation Mode that map to table columns).

**Multi-level expression**: for a given constraint *κ*, the set of equivalent expressions at different levels. The physics-level expression captures the causal mechanism. The engineering-level expression enables table validation. The intermediate expression captures the analytically interesting relationship between cause and consequence. These are not different constraints — they are different VIEWS of the same constraint, connected by causal reasoning.

### What this enables

Constraints that carry both physics and engineering expressions can be validated against the table WITHOUT losing physics-level reasoning. The algorithm's strength (physics-grounded first-principles derivation) and Goal 1's requirement (engineering-level validation) cease to be in conflict. The gap doesn't need to "close" through descent — it can be bridged at each node by expressing the same constraint at multiple levels.

This also makes the intermediate level — physics-of-failure applied to engineering — visible as an explicit output rather than something that might or might not emerge from the LLM's reasoning.

---

## 6. Question-Level Convergence — Shared Problems Before Shared Answers

### What the current model misses

The formal model defines convergence through **constraints**: two branches independently producing rules with overlapping consequences (Section 6, `κ_A.consequence ∩ κ_B.consequence ≠ ∅`). Enhancement 4 identifies the hard problem — constraint vocabulary varies across branches because the LLM generates free-form text. `energy_capture: thermal` vs. `conversion_method: steam_cycle`. Same reality, different strings.

But there is a different convergence medium already present in the data: **the questions themselves**.

Each option generates 5-6 downstream questions. These questions are the algorithm's most direct representation of what sub-problems a given context creates — the original hypothesis ("each choice generates new sub-problems") made concrete. Both documents treat questions as navigational inputs. Neither treats them as analytical objects to compare across branches.

### Question convergence vs. constraint convergence

These detect different things:

**Constraint convergence**: same answer from different paths. Two branches both derive `{fuel: D-T} → {neutron_shielding: heavy}`. This means the same rule holds across contexts.

**Question convergence**: same problem from different paths. The tokamak branch generates "How should tritium be bred given compact toroidal geometry?" and the mirror branch generates "How should tritium be bred given linear open geometry?" Same sub-problem, different contexts.

Same problem ≠ same answer. The tokamak and mirror both face "how to breed tritium," but their blanket geometries differ completely — constraints diverge even though the question converges. Question convergence identifies WHERE transfer might happen (shared sub-problem). Constraint convergence within those shared sub-problems then determines WHAT actually transfers (shared vs. context-specific solutions).

Enhancement 4 jumps to the second step without doing the first.

### Why question matching is easier

Questions operate at a higher level of abstraction than constraints. They use problem-level vocabulary ("how to manage neutron damage?") rather than solution-level vocabulary (`{geometry: compact_toroidal, blanket_space: constrained}`). There is less vocabulary variation at the problem-identification level than at the solution-specification level, because the LLM is explicitly prompted to generate questions about sub-problems — framed as PROBLEMS, not as solutions.

And question-level convergence is detectable WITHOUT expanding the questions. Every option in every expansion already carries its full downstream question list. Comparing question sets across branches requires no additional LLM calls — just semantic comparison on existing data. Constraint convergence requires actually running expansions and then solving the vocabulary bridge; question convergence is available for free from the tree's existing state.

### What this changes about the unfollowed questions

Enhancement 2 frames unfollowed questions as wasted expansion opportunities — signal that would produce constraints if followed. This enhancement reframes them: **unfollowed questions are already useful as analytical objects.** Their overlap pattern across branches maps the shared problem structure of the design space without spending a single LLM call.

The question space at each option isn't just "what to explore next." It's "what sub-problems this context creates." The union of question spaces across the tree IS the design space's problem structure.

### What this enables

A two-stage convergence analysis:

1. **Question-level scan** (cheap, immediate): compare question sets across all branches. Identify sub-problems that appear in multiple contexts. This produces a map of shared problem structure — where branches face the same design challenge from different starting points.

2. **Constraint-level analysis** (expensive, targeted): for converged questions, expand both branches' versions and compare constraints. The question match tells you WHERE to look; the constraint comparison tells you WHAT transfers.

This also gives the navigator (Enhancement 1) a new signal: question overlap across branches. Branches that have converged in questions but haven't been compared are high-priority for targeted expansion and convergence analysis.

---

## 7. Active Ontology — Shared Vocabulary Across the Tree

### The problem this addresses

The tree generates free-form vocabulary at every expansion. One branch says `energy_capture: thermal`, another says `conversion_method: steam_cycle`. One branch asks "How should tritium be bred?" another asks "What blanket configuration supports adequate TBR?" Same physical reality, different strings. Enhancements 4 and 6 both require matching terms across branches — and the matching problem is hard precisely because there is no shared vocabulary.

An active ontology would build a growing vocabulary of terms (design variables, sub-problems, physics concepts) alongside the tree, extracted from questions, choices, and constraints as the tree grows. When the tree references tritium breeding in one branch, that term becomes available for recognition — and potentially for reuse — in other branches.

### Two possible implementations

#### Implementation A: Post-hoc index (analysis-only)

The ontology is built FROM the tree but never fed back INTO it.

- Expansions run independently, as they do now — each node sees only its own accumulated context, no cross-branch vocabulary
- After each expansion round, terms are extracted from new questions, choices, and constraints
- The ontology is a searchable index: "term X appears in nodes [N1, N3, N7] with these usages in these contexts"
- Convergence analysis (Enhancements 4 and 6) uses the index to identify candidate matches, then validates them by comparing usages in context
- Human reviewers use the index to understand the tree's vocabulary landscape

**Preserves**: the algorithm's independence property. Convergence detected through the index is genuine — two branches arrived at the same term independently, which is evidence of shared structure. The index doesn't cause convergence; it detects it.

**Costs**: the vocabulary matching problem remains at generation time. Two branches may describe the same physics using different terms, and the index must solve the synonymy problem after the fact. Semantic similarity, LLM-based mapping, or human review is still needed to bridge vocabulary gaps. The index makes this tractable (scope the matching to likely candidates) but doesn't eliminate it.

#### Implementation B: Vocabulary guidance (participates in generation)

The ontology is fed back into the expansion prompt as available vocabulary.

- After each expansion round, terms are extracted and added to the ontology
- During expansion, the system searches the ontology for terms relevant to the current context and question
- Relevant terms are presented to the LLM alongside the standard inputs: "The following terms have been used elsewhere in the tree: [tritium breeding, neutron shielding, direct energy conversion, ...]"
- The LLM is encouraged to use existing terms where they fit, but is not forced — novel terms can still be introduced
- This changes the expansion signature from LLM(*C*, *q*, *R*) to LLM(*C*, *q*, *R*, *O*) where *O* is a set of ontology terms deemed relevant

**Preserves**: the algorithm's decomposition structure, grounding, and requirement-lens mechanism. The ontology provides vocabulary, not conclusions. "The term 'tritium breeding' exists" doesn't tell the LLM whether tritium breeding is needed, feasible, or important in this context.

**Costs**: breaks the independence property. The LLM now sees information from other branches (via the ontology terms), which creates three specific risks:

1. **Ontology-induced convergence.** If two branches both say "tritium breeding" because the ontology provided the term, you cannot tell whether the convergence reflects shared design-space structure or shared vocabulary input. The analytical meaning of convergence degrades.

2. **Vocabulary-as-framing.** Vocabulary shapes reasoning. If the ontology has 20 neutron-related terms and 3 direct-conversion terms (because more branches have explored neutron issues), the LLM's attention and expression will be biased toward neutron concerns. Novel framings that don't fit the existing ontology are harder to produce. This is the Sapir-Whorf effect applied to LLM reasoning — available language shapes available thoughts.

3. **Polysemy across contexts.** The same term can mean different things in different contexts. "Plasma stability" in a tokamak context is MHD stability against kink and ballooning modes. "Plasma stability" in an IFE context is hydrodynamic stability against Rayleigh-Taylor during compression. An ontology that strips context from terms creates false matches — two branches appear to converge on "plasma stability" when they face physically distinct problems.

### The sequencing consideration

The tradeoffs between A and B depend on what tree you're building:

**First tree (baseline exploration):** Implementation A is strongly favored. The first tree establishes the design space's structure. Independent derivation is what makes convergence signals trustworthy. Ontology-induced convergence on the baseline tree undermines the primary analytical output.

**Subsequent trees (seeded explorations per Enhancement 3):** Implementation B becomes viable. The baseline tree's structure is established. Using its vocabulary for seeded trees improves comparability — you're measuring how a seed changes the tree, and shared vocabulary makes the comparison precise. The first tree is the independent baseline; seeded trees can use its ontology because you're explicitly measuring differences against it.

**Deep expansion of specific branches:** Implementation B is also viable when expanding a single branch to greater depth. The branch's own earlier vocabulary is already in the accumulated context, so the ontology is just surfacing terms from sibling branches at the same depth — useful for vocabulary consistency within a concept family without cross-family contamination.

---

## Sequencing

**3 → 1 → 5 → 7A → 2 → 6 → 4**

**Seeding first** (3): lowest effort, highest immediate insight. Tests Goal 3 and validates the formal model's predictions. Produces comparative analytical output immediately. Requires only defining the seed format and modifying the root node's initial context.

**Question value second** (1): prerequisite for intentional navigation. Without it, the tree explores arbitrarily regardless of other enhancements. Requires defining the value function and the abstraction concepts it depends on.

**Multi-level constraints third** (5): low effort (prompt-level change), enables Goal 1 testing. Requires defining constraint expression levels and the concept of multi-level equivalence.

**Parallel investigation fourth** (2): amplifies the value of 1 and 5. More questions explored × better question selection × multi-level constraints = multiplicative constraint yield. Requires defining investigation breadth and its interaction with depth.

**Post-hoc ontology fifth** (7A): extract terms from existing expansions and build the searchable index. This is a prerequisite for both convergence enhancements — the index provides the vocabulary bridge that makes question and constraint matching tractable. No changes to the expansion process; analysis-only.

**Question-level convergence sixth** (6): using the ontology index, scan for shared sub-problems across branches. Produces the shared-problem map that makes targeted constraint comparison (Enhancement 4) tractable.

**Constraint-level convergence last** (4): targets the shared sub-problems identified by Enhancement 6. Rather than solving vocabulary matching across the entire constraint registry, scope comparison to converged question clusters. All prior enhancements increase the tree's constraint density, question coverage, and vocabulary consistency, making convergence detection more productive when it arrives.

**Vocabulary guidance for seeded trees** (7B): when building seeded trees (Enhancement 3), use the baseline tree's ontology as vocabulary input. This is the only point where the ontology participates in generation — and only because you're explicitly comparing against the baseline, so shared vocabulary improves the comparison.
