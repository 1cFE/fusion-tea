# Phase 2a Report: Generative Reasoning Tree

**Date**: 2026-03-13
**Status**: In progress — L0 expanded, L1 partial (1 of 5 branches)
**Branch**: `design-space-explore`

---

## 1. Introduction: What Phase 1 Established

The Fusion TEA project investigates the economics of fusion power across fundamentally different approaches. Before building cost models, we need to understand the *structure* of the design space — how the ~38 active fusion concepts relate to each other, what drives their divergence, and where knowledge might transfer between them.

The original concept document ([Context-Dependent Design Spaces](../context/context_dependent_design_spaces.md)) posed the motivating hypothesis: **the fusion design space is not well-captured by fixed taxonomies or static decision trees.** Each architectural choice generates new sub-problems that reshape the downstream decision landscape. If true, then any fixed-column table of fusion concepts will necessarily contain questions that simply don't apply to some approaches — and the standard tools for analyzing design spaces (morphological matrices, Cartesian grids) will fail to explain why concepts look the way they do.

Phase 1 tested this hypothesis empirically. Could we explain the diversity of ~38 active fusion concepts through morphological analysis — organizing them into a table of independent design dimensions? And if so, would that table be *explanatory* — not just recording what each concept chose, but illuminating why?

### Phase 1a: Building the differentiation table

We built a table with 38 rows (one per fusion concept — each an active startup or program) and 12 columns of categorical design choices: Confinement Family, Confinement Concept, Fuel, Primary Heating, Energy Capture, Plasma State, Magnet Type, Tritium Breeding, Neutron Management, Operation Mode, Repetition Rate, and Driver Technology. Each cell was filled with a controlled-vocabulary value, marked N/A (question is structurally inapplicable — e.g., "Tritium Breeding" for a concept that doesn't use tritium), or TBD (question applies but answer isn't public). ([v1 table](../phase_1a/table.csv), [v1 schema](../phase_1a/schema.md))

### Phase 1b: The "Confinement Concept" problem

When we analyzed the table, one column dominated everything: **Confinement Concept** had 29 unique values for 38 rows. It was almost a unique identifier — knowing the confinement concept alone was enough to look up nearly every other column. The minimum set of columns needed to distinguish all 38 concepts was just 2 (Confinement Concept + Tritium Breeding). This meant the table wasn't really a multi-dimensional analysis; it was a lookup keyed on one overloaded column.

The problem: "Confinement Concept" was doing all the descriptive work, but it wasn't a real morphological dimension. It was a hierarchy crammed into a flat column — "compact tokamak" and "spherical tokamak" differ in a specific way (aspect ratio), "tokamak" and "stellarator" differ in a different way (how rotational transform is provided), and "MFE" and "IFE" differ at a still higher level (the fundamental confinement mechanism). Packing all three levels into one column meant the table was a classification lookup, not a morphological analysis. There was no explanatory power.

### Phase 1b v2: Restructuring reveals context-dependence

To fix this, we decomposed the overloaded Confinement Concept column into an 8-column hierarchical tree, where each column is a genuine morphological question that applies only within its scope:

| Column | Applies to | Example values |
|---|---|---|
| Confinement Family | All 38 concepts | MFE, IFE, MIF, Non-Standard |
| MFE Topology | 19 MFE concepts only | Tokamak, Stellarator, FRC, Mirror, ... |
| Tokamak Shape | 6 tokamaks only | Compact, Spherical, Conventional, Neg-Tri |
| Stellarator Type | 6 stellarators only | QI modular, QI planar, Helical |
| IFE Driver | 12 IFE concepts only | Laser, Z-pinch, Projectile, Beam |
| *(etc.)* | | |

The resulting v2 table had 38 rows × 18 columns. ([v2 table](../phase_1b_v2/table_v2.csv), [v2 schema](../phase_1b_v2/schema_v2.md), [v2 report](../phase_1b_v2/report.md))

This restructuring solved the near-ID problem — the minimum discriminating set went from 2 to 4 columns — and gave us a much better *description* of each concept. But it introduced a new phenomenon: **N/A density** — the fraction of cells in the table that are "N/A" because the question simply doesn't apply to that concept. "Tokamak Shape" is meaningless for a laser ICF concept. "IFE Driver" is meaningless for a tokamak. These aren't missing data; they are *structurally inapplicable questions*.

N/A density went from 9.6% in the v1 table to **36.7%** in v2. More than a third of the cells in the restructured table are questions that don't exist for that concept. And the pattern was monotonic: as we asked more specific questions (Confinement Family → MFE Topology → Tokamak Shape), the fraction of N/A cells increased steadily (10.5% → 27.7% → 36.7%). Deeper questions apply to narrower concept subsets and are N/A for everything else. Every single N/A traced to an identifiable upstream design decision — zero were arbitrary or data-quality artifacts.

This is the empirical signature of a **context-dependent design space**: the questions that are meaningful change depending on what branch you're on, and the effect deepens at every level of specificity. The flat table hides this by cramming the hierarchy into one column; the restructured table exposes it.

### Phase 1d: Is it a design space or a classification scheme?

The v2 table was structurally sound, but a deeper question remained: even with proper discrimination and visible context-dependence, could the table *explain* fusion concepts? Could it *generate* new viable ones? Phase 1d ran four tests. ([Phase 1d report](../phase_1d/report.md))

**Test 1 — Vocabulary completeness.** Does the table's controlled vocabulary cover the full space of physically plausible approaches, or just the choices observed in the current 38 concepts? Result: 8 of 17 controlled-vocabulary columns were "open" (missing plausible values), with 21 missing candidates — mostly historical approaches no current startup has revived. The vocabulary is shaped by the commercial landscape, not by the full physics design space.

**Test 2 — Generative coherence.** If the columns were truly independent design dimensions, you could randomly sample one value per column and get a physically viable concept. We generated 30 random concepts this way. Result: **0 out of 30 were physically coherent.** Not low — zero. Random combination never produces a viable fusion concept because the columns are not independent. Choosing "IFE" for confinement but "sustained plasma" for plasma state is a physics contradiction. Choosing "p-B11" for fuel but "heavy shielding" for neutron management is nonsensical. The columns are tightly coupled, not independent dimensions.

When we conditioned the sampling on confinement family (only drawing values observed within that family), coherence rose to 23% — but most "hits" were trivial variants or known concepts, not genuine novel designs. The dominant failure mode was the fuel cascade: choosing D-T fuel forces heavy neutron shielding and tritium breeding; choosing p-B11 eliminates both but requires extreme plasma temperatures. These aren't free choices — they're consequences.

**Test 3 — Constraint density.** From the coherence failures, we mapped which column pairs were most tightly coupled. Three clusters accounted for most of the constraint structure: Confinement-Heating-Plasma (your confinement choice determines your heating method and plasma state), Fuel-Neutron-Energy (your fuel choice cascades deterministically into shielding, breeding, and energy conversion), and Driver-Hardware (the driver technology must match the confinement mechanism). The effective degrees of freedom were approximately 2 — concept and fuel — not the 15+ the column count implies.

**Test 4 — Blind row recoverability.** We presented table rows (with concept name and Driver Technology withheld) to an LLM assessor and asked: can you reconstruct the concept's design thesis, hard problems, and competitive differentiation from the columns alone? Result: approach-level information was recoverable (the assessor could tell it was a tokamak or a laser ICF concept), but within-family differentiation failed. The columns couldn't explain what makes CFS different from Tokamak Energy, or Xcimer different from Focused Energy. All 5 assessors independently flagged the same missing information: scale parameters, performance targets, cost basis, and engineering strategy — the *why* behind the *what*.

### Phase 1 verdict

The table is a **classification scheme, not a design space**. It correctly categorizes concepts by physics approach — but it cannot explain why concepts within the same family diverge, cannot generate new viable concepts, and has only ~2 effective degrees of freedom despite 18 columns. The effective structure is a shallow tree (Family → Concept → determined columns; Fuel → downstream cascade), not a Cartesian grid of independent dimensions.

---

## 2. The Problem Phase 2 Addresses

Phase 1 confirmed the original hypothesis: the fusion design space is context-dependent, and morphological analysis cannot capture it. But confirming the diagnosis doesn't solve the problem. We still need a way to understand what *drives* the current landscape of fusion concepts — why they diverge where they do, why certain combinations don't exist, and where knowledge might safely transfer from a well-studied concept to a less-studied one.

The table tells us that CFS builds a compact tokamak with HTS magnets and D-T fuel. It does not tell us *why* — that the bet is on high magnetic field (enabled by HTS) making the device small enough to be economically competitive, and that compactness creates cascading engineering challenges (blanket space for tritium breeding, disruption severity, neutron flux density) that define CFS's real R&D agenda. The table tells us that TAE pursues p-B11 fuel in an FRC. It does not tell us that this choice *eliminates* the entire neutron management and tritium breeding problem set while creating an extreme plasma temperature challenge that no other concept faces. The reasoning — the *why* — is where the understanding lives.

Phase 2 asks: **can we build a representation that captures this reasoning?** Specifically:

1. **Can we derive the constraints that shape the design space from first principles** — rather than reading them off the table? If the reasoning is sound, the derived constraints should match what the 38 known concepts actually exhibit.

2. **Can the reasoning explain the negative space** — why certain combinations don't exist (no p-B11 tokamak, no steady-state IFE, no D-T with direct energy conversion)? The table records these as absent rows; the reasoning should trace the absence to specific physics contradictions.

3. **Can the reasoning make transfer opportunities formally visible** — when two different concepts face the same sub-problem because their upstream choices created the same context? If a D-T tokamak and a D-T mirror both need to breed tritium because they both chose D-T fuel, that shared context should justify sharing the tritium-breeding solution (partially — the geometry differs). The reasoning should make the shared part and the different part both explicit.

4. **Can this kind of algorithm scale to future discovery** — if someone proposes a new confinement concept, can the algorithm rapidly elaborate what downstream challenges it would face, where existing knowledge applies, and where genuine unknowns begin?

This is not about building a better taxonomy. It is about testing whether a *reasoning-driven algorithm* can rediscover the structure of the fusion design space and produce formalized knowledge artifacts — validated constraints, transfer maps, negative-space explanations — that the flat table cannot. ([Phase 2 concept](../phase_2_concept.md), [concept review](../phase_2_concept_review.md), [algorithm ideation](../algorithm_ideation.md))

---

## 3. Strategy: The Generative Reasoning Tree

### 3.1 The Core Idea

Phase 1 showed the flat table records WHAT each concept chose but not WHY. The reasoning tree inverts this: instead of starting from 38 known concepts and trying to fit them into columns, it starts from universal requirements and builds outward. At each step, an LLM reasons from first principles about what approaches are viable given the accumulated context — what each choice forces, eliminates, and creates. The tree grows one level at a time, with each node producing a set of options that become the next level's nodes.

The key bet: **the same universal requirement, interpreted in different accumulated contexts, should produce different constraints and solutions.** If we choose magnetic confinement, the requirement "maintain structural integrity" (R6) generates questions about steady-state neutron damage to the first wall. If we choose inertial confinement, the same R6 generates questions about cyclic shock loading on the blast chamber. The requirement is the same; the context changes what it demands. This is the context-dependence mechanism — and the tree's job is to make it explicit.

The reasoning tree produces two artifacts:
- **The tree itself** — a branching structure where each node carries the reasoning trace (thesis, requirement analysis, derived constraints, downstream questions). Paths through the tree correspond to recognizable fusion concepts.
- **The constraint registry** — a growing set of formal rules extracted from the LLM's reasoning and validated against the 38-concept table. This registry is the primary knowledge artifact — the formalized "rules of the design space."

### 3.2 The Requirement Lenses

Every fusion power plant, regardless of approach, must satisfy six universal requirements. These are not nodes in the tree — they are *lenses* applied at every decision point. Each time the algorithm faces a design question, it asks: how does each requirement bear on this choice? How does each option affect satisfaction of each requirement?

| ID | Requirement | What It Demands | What Questions It Generates (examples) |
|---|---|---|---|
| R1 | Fuel the reaction | Sustainable fuel supply | D-T → where does tritium come from? p-B11 → commercially available (trivial) |
| R2 | Achieve fusion conditions | Create and sustain conditions for fusion | How do you confine? What geometry? How do you heat? How do you maintain stability? |
| R3 | Produce net energy | More energy out than the plant consumes | What's the gain? What's the driver efficiency? How much power recirculates? |
| R4 | Extract usable energy | Convert fusion products into deliverable form | Neutrons vs. charged particles? Thermal conversion or direct? |
| R5 | Manage the nuclear environment | Safely handle nuclear byproducts | Shielding? Activation? Waste classification? Tritium safety? |
| R6 | Maintain structural integrity | The plant must survive the environment it creates | Neutron damage? Thermal loads? Cyclic stress? |

The requirements are what produce the cross-cutting analysis the flat table missed. R6 (structural integrity) means completely different things for a tokamak (steady-state neutron flux on the first wall) versus a laser ICF plant (repeated blast loading on the chamber wall) versus a Z-pinch (electrode erosion). The requirement is universal; the engineering challenge is context-dependent.

### 3.3 How the Algorithm Works

#### Step 1: Expansion (creative reasoning)

Each node in the tree represents a design question to resolve. The algorithm gives an LLM three inputs:

- **Accumulated context**: all design choices made on the path from root to this node — for example, "we chose closed magnetic topology, which provides confinement via field-line geometry that eliminates end losses"
- **The six requirement lenses**: R1–R6 as described above
- **The current question**: the design question to resolve — for example, "How should rotational transform be provided?"

The LLM reasons from first principles (the prompt explicitly prohibits naming known companies or reactor designs) and produces, for each viable option:

- A **thesis** — what problem does this approach solve, what trade-off does it navigate
- A **requirement-by-requirement analysis** — how does this option affect R1–R6
- **Derived constraints** — what is forced, eliminated, or activated by this choice
- **New downstream questions** — what design questions does this choice *create* that didn't exist before
- A **context addition** — a summary of what this choice means, which becomes part of the accumulated context for the next level

The LLM also identifies **negative space** — approaches that are NOT viable in this context, with the physics reasoning that rules them out.

**Where do the questions come from?** This is worth being explicit about, because the question at each node is what drives the tree's shape. The root question ("How should we confine the fusion reaction?") is a manually written seed. After that, every question comes from the LLM's expansion output: each option includes a list of downstream questions it creates, and the *first* question on that list becomes the child node's question. The remaining questions are discarded.

So the LLM plays two roles: it is both the *reasoner* (producing options, constraints, and negative space) and the *question generator* (deciding what the next design question should be on each branch). There is no separate mechanism for ranking or selecting which question is most important — the tree's branching structure is entirely determined by the LLM's ordering within each expansion. This is a significant limitation discussed in Section 6 (Open Questions).

The LLM calls are stateless and headless (`claude -p`). Each node sees only its own path from root — no cross-branch memory. This isolation is deliberate: we want each branch to be an independent test of whether requirements + context produce the right constraints, without the LLM reasoning comparatively across branches.

Here's how this looks concretely at the first two levels:

> **Root question** (L0): "How should we confine the fusion reaction?"
> **Context**: None (root node)
> **Output**: 5 options — closed magnetic topology, open magnetic (mirror), inertial, magnetized target, electrostatic potential well. Plus 5 negative-space entries (gravitational confinement, direct material containment, beam-target, chemical confinement, radiative confinement — each with the physics reason it fails).
>
> Each option generates a list of downstream questions. The closed magnetic option lists 6 questions; the first — "How should rotational transform be provided?" — becomes the L1 node's question. The inertial option's first question is "What driver technology?" These questions only exist *because* of the choice made — that's the context-dependence in action.

> **L1 question** (closed magnetic branch): "How should rotational transform be provided?"
> **Context**: "We chose closed magnetic topology — field-line geometry eliminates end losses but requires rotational transform for radial confinement"
> **Output**: 3 options — plasma-current-driven (→ tokamak family), external 3D coils (→ stellarator family), hybrid. Each option again generates its own list of downstream questions. The concepts emerge from reasoning about physics trade-offs, not from naming known devices.

#### Step 2: Constraint extraction and validation (analytical)

The LLM's reasoning contains claims about what each choice forces or eliminates — these are the *constraints* of the design space. The second step extracts these into a formal format and checks them against reality.

Each constraint has:
- A **condition** — what accumulated context triggers it (e.g., `confinement_approach = magnetic`)
- A **consequence** — what is forced, eliminated, or activated (e.g., `magnet_type ≠ N/A`)
- A **requirement basis** — which of R1–R6 drives it
- **Reasoning** — the physics/engineering justification

These are then validated against the Phase 1 table (`table_v2.csv`). For each constraint, we ask: does this rule hold for all 38 known concepts that match the condition? The constraint gets classified as:

- **Validated** — holds for all matching concepts. The LLM derived a real pattern from first principles.
- **Flagged** — holds for most but not all. These are the most interesting analytically: is the table wrong, is the constraint over-general, or is the exception a genuine outlier?
- **Rejected** — doesn't hold. The LLM generated a plausible-but-incorrect rule.
- **Unmappable** — the constraint references variables that don't correspond to any table column (e.g., "field topology," "loss cone"). These can't be validated against the table, but they are valuable — they are design dimensions the classification scheme missed.

As the registry grows, new constraints are also checked against *existing* constraints for cross-branch consistency. If two branches independently derive the same rule (reinforcing), that's strong evidence it's real. If they derive contradictory rules for the same variable (contradicting), either one is wrong or both are right in their respective contexts — which IS context-dependence.

#### Step 3: Justification tracking (transfer mechanism)

Every validated constraint carries its **justification set** — the accumulated context that produced it. This is what makes transfer analysis possible.

Example: suppose the D-T tokamak branch produces the constraint "must breed tritium" with justification `{fuel: D-T}`, and the D-T mirror branch independently produces the same constraint with justification `{fuel: D-T}`. The shared justification tells us the constraint depends only on fuel choice, not on confinement type — so the *problem* (tritium breeding) transfers across all D-T concepts. Whether the *solution* (specific blanket design) also transfers depends on whether the broader context differs (toroidal geometry vs. linear geometry affects blanket design).

A constraint like "blanket space is limited" with justification `{fuel: D-T, confinement: tokamak, design_point: compact}` is much more specific — it only applies to compact tokamaks. The justification set makes the transfer scope explicit.

This layer becomes useful once multiple branches are expanded. With only one branch expanded (as of now), there's nothing to compare against yet.

#### Putting it together

The algorithm runs in rounds, one tree level at a time:

1. **Expand** all pending nodes at this level (LLM calls)
2. **Validate** — extract constraints, check against table, check cross-branch consistency
3. **Render** — produce human-readable markdown of tree + constraint registry
4. **Human review** — are the options physically reasonable? Are the constraints correctly extracted? Which branches should be expanded next?

Review between rounds catches errors before they propagate down the tree. ([Spec](phase_2a_spec.md), [Design](phase_2a_design.md))

### 3.4 What We Are Testing

**Primary tests** (the tree must pass these to earn its keep):

1. **Negative space explanation** — Can the tree explain *why* certain concept combinations don't exist? Not by recalling that they're absent, but by showing which requirement lens, applied to which accumulated context, produces the contradiction. Target examples: why no p-B11 tokamak, why no steady-state IFE, why no D-T with direct energy conversion.

2. **Constraint validation rate** — Do the constraints derived from first-principles reasoning actually hold when checked against 38 real concepts? Target: >70% validation rate among mappable constraints, <20% rejection rate.

3. **Divergence reasoning depth** — At branch points where the Phase 1 table had only category labels ("Confinement: MFE"), does the tree provide richer reasoning about the trade-offs motivating each choice?

4. **Concept family recovery** (sanity check) — Do paths through the tree arrive at recognizable concept families (tokamak, stellarator, laser ICF, etc.)?

**Secondary tests** (assessed opportunistically):

5. **Novel paths** — Do any tree paths lead to concept configurations not in the 38-concept table that pass a basic physics sniff test?
6. **Novel variables** — Does the algorithm generate design dimensions not represented in the table's 18 columns?
7. **Transfer visibility** — Do different paths produce the same validated constraint with overlapping justification sets?

### 3.5 Implementation

Three Python scripts execute the pipeline:

| Script | Role |
|---|---|
| `expand.py` | Builds prompt from tree state, calls `claude -p` headlessly, parses JSON, creates child nodes |
| `validate.py` | Extracts constraints from expansions, maps to table columns, validates against `table_v2.csv`, checks cross-branch consistency |
| `render.py` | Renders tree + constraint registry into human-readable markdown |

State is stored in `tree.json` (full tree: nodes, contexts, expansions, child pointers) and `constraints.json` (the growing constraint registry). The prompt template is in `prompt.md`; rendered output for human review goes to `reasoning_tree.md`.

The LLM calls use Sonnet for cost efficiency (~$0.15/node). Each call is stateless — the node sees only its own path from root, with no cross-branch memory.

---

## 4. Results So Far

### 4.1 L0 Expansion: The Root Question

**Question**: "How should we confine the fusion reaction to achieve sustained energy production?"

**Context**: None (root node — no prior decisions).

The LLM produced 5 confinement approaches and 5 negative-space entries, deriving 22 constraints total.

#### Options Generated

| Option | Thesis Summary | Constraints | New Questions |
|---|---|---|---|
| **Closed magnetic topology** | Eliminate end losses via toroidal geometry; trade-off is need for rotational transform (plasma current OR 3D coil complexity) | 6 | 6 |
| **Open magnetic topology (mirror)** | Accept end losses for geometric simplicity; compensate with plugging and/or direct energy conversion | 4 | 5 |
| **Inertial confinement** | Invert the Lawson trade-off — extreme transient density instead of sustained confinement; fundamentally pulsed architecture | 5 | 6 |
| **Magnetized target (magneto-inertial)** | Embed magnetic field in target to reduce compression ratio; enables efficient mechanical drivers at intermediate density | 4 | 5 |
| **Electrostatic potential well** | Use electric fields to confine ions; fundamentally limited by Earnshaw's theorem and space-charge constraints | 3 | 3 |

#### Quality Assessment: Reasoning Depth

The L0 expansion demonstrates reasoning that goes well beyond what the flat table captures. The requirement analysis for each option shows *how* the confinement choice interacts with every downstream requirement:

- **Closed magnetic**: R2 drives the choice (confinement-time axis of Lawson). R3 analysis reveals the alpha-heating threshold is critical — below ignition, external heating dominates and net electricity is marginal. R4 analysis distinguishes the neutron extraction path (through blanket) from charged-particle path (thermalized in plasma, exhausted via divertor). R6 identifies the steady-state heat flux problem (10–20 MW/m² on the divertor) as the structural challenge.

- **Open magnetic (mirror)**: The thesis statement captures the fundamental trade-off concisely — accept end losses for geometric simplicity. The R4 analysis identifies a unique advantage: escaping ions can be directly converted to electricity at >80% efficiency, geometrically unavailable in closed topologies. The R3 analysis identifies the core challenge: plug power can exceed fusion power for plausible geometries.

- **Inertial**: The thesis cleanly captures the Lawson inversion. The constraint analysis derives specific quantitative thresholds from first principles: burn fraction formula (ρR/(ρR + H_burn)), compression ratio (~1000×), implosion symmetry requirement (<1% RMS nonuniformity from Rayleigh-Taylor analysis), driver peak power (petawatt scale from implosion velocity requirements).

- **Electrostatic**: The analysis correctly identifies Earnshaw's theorem as the fundamental physics limit and derives the space-charge density cap. The R3 analysis explains *why* the grid-loss power exceeds fusion power (ratio of fusion cross-section to Coulomb scattering cross-section). This is a more complete explanation than "IEC can't reach net energy" — it traces the impossibility to a specific physical ratio.

#### Quality Assessment: Negative Space

The negative space entries are particularly strong. Five non-viable approaches were identified with physics-grounded reasoning:

1. **Gravitational confinement**: Minimum mass for self-confinement exceeds ~10²⁹ kg (brown dwarf scale). Dismissed via fundamental force ratio.
2. **Direct material containment**: Plasma at 10⁸ K vs. wall materials at ~4000 K. Energy density gradient is insurmountable.
3. **Beam-target at sub-thermal energies**: Coulomb scattering cross-section exceeds fusion cross-section by ~10⁴ at relevant energies. Net energy impossible from this ratio alone.
4. **Chemical/molecular confinement**: Fusion temperatures (~10 keV) exceed chemical bond energies (~eV) by four orders of magnitude. All molecular structure dissociates.
5. **Purely radiative confinement**: Radiation pressure at fusion temperatures is ~10¹³ Pa, but producing this externally would consume more power than fusion produces (R3 violation).

These are genuine negative-space explanations — each traces non-viability to a specific physical constraint interacting with a specific requirement lens. This is exactly the kind of reasoning the flat table could never provide.

#### Constraint Analysis: All Unmappable (Expected)

All 22 L0 constraints are classified as "unmappable" — their condition and consequence variables don't correspond to any of the 18 table columns. This is **expected and informative**:

L0 reasoning operates at the *physics* level: field topology, loss cones, compression ratios, Rayleigh-Taylor instability, Earnshaw's theorem. The table operates at the *engineering classification* level: Confinement Family, Magnet Type, Operation Mode. The vocabulary gap between these levels confirms that the reasoning tree captures design dimensions the classification scheme misses (success criterion 6).

The 22 novel variables include:
- `field_topology`, `rotational_transform`, `loss_cone`, `implosion_symmetry`
- `target_density`, `compression_ratio`, `driver_peak_power`
- `liner_fabrication`, `magnetic_flux_conservation`
- `electron_confinement`, `space_charge_limit`

These are the physics-level design dimensions that the flat table collapsed into coarser categories. Validation becomes meaningful at L2+ where the tree's reasoning reaches engineering choices that map to table columns.

### 4.2 L1 Expansion: Closed Magnetic Topology

**Question**: "How should rotational transform be provided: plasma current, external 3D coils, or a hybrid?"

**Context**: Closed magnetic topology confinement — field-line topology eliminates end losses; requires rotational transform for radial confinement.

This is the first expansion with accumulated context. The LLM sees only one prior decision (closed magnetic topology) and must reason about the next branching point.

#### Options Generated

| Option | Maps To | Constraints | New Questions |
|---|---|---|---|
| **Plasma-current-driven transform** | Tokamak-like concepts | 5 | 5 |
| **External 3D coil-generated transform** | Stellarator-like concepts | 5 | 6 |
| **Hybrid (external baseline + supplemental current)** | Hybrid stellarator/tokamak concepts | 4 | 5 |

#### Concept Family Recovery

This expansion demonstrates concept family recovery (success criterion 4):
- "Plasma-current-driven" → tokamak family (axisymmetric coils, disruption risk, current drive)
- "External 3D coils" → stellarator family (disruption-free, complex coil geometry, fixed transform profile)
- "Hybrid" → advanced/quasi-symmetric concepts that blend both approaches

The concepts are arrived at through *reasoning about physics trade-offs*, not by naming known devices. The trade-off structure is made explicit:
- Tokamak path: simple coils, but disruption risk and continuous current-drive power
- Stellarator path: no disruptions, but 3D coil manufacturing and reduced blanket coverage
- Hybrid path: larger optimization space, altered disruption character (graceful degradation rather than catastrophic collapse)

#### Negative Space

Four non-viable approaches were identified within the closed-magnetic context:

1. **No rotational transform at all**: Charge separation from grad-B drifts destroys confinement in microseconds. This is a direct R2 violation.
2. **Pulsed operation with inductive drive only**: Finite flux swing limits pulse duration. For power plants, this produces unacceptable duty cycle.
3. **Open field lines within a nominally closed geometry**: Field lines terminating on material surfaces are not equivalent to truly closed topology — defeats the purpose of closing the geometry.
4. **Passive (uncontrolled) plasma current**: Resistive decay and uncontrolled profile evolution lead to instability. R2 and R6 demand active control.

Each negative-space entry is context-dependent — these approaches are non-viable *specifically because we chose closed magnetic topology*. This demonstrates the core context-dependence mechanism: the accumulated context activates specific requirements that rule out specific approaches.

#### Constraint Quality

The L1 constraints are richer than L0 because they operate within a specific context. Notable constraints:

- **Disruption risk is non-zero for any current-carrying plasma** (DC from plasma-current option, R6): "MHD theory shows that no known control scheme can guarantee disruption probability exactly zero over plant lifetime." This is a physics-grounded constraint that explains a real engineering challenge.

- **Disruption risk eliminated by construction** (DC from external-coils option, R2): "With no net current, the MHD free energy source for disruptions does not exist." This is the *complementary* constraint — the same variable (disruption risk) takes opposite values depending on the rotational-transform choice. If both validate, this IS context-dependence.

- **Blanket coverage reduced by external coils** (DC from external-coils option, R4): "Physical coil conductors, their casings, and structural supports must occupy radial and poloidal space around the plasma vessel." This constraint connects the rotational-transform choice to a tritium-breeding consequence — exactly the kind of cross-requirement interaction the tree is designed to reveal.

- **Disruption character altered in hybrid** (DC from hybrid option, R2): "When external transform is present, losing plasma current does not immediately destroy confinement — the plasma settles to a lower-transform state." This captures a *nuance* — not binary disruption/no-disruption, but a spectrum of disruption severity depending on how much transform is externally provided.

These constraints have not yet been run through `validate.py` for table checking. That is the next step.

---

## 5. Preliminary Assessment Against Success Criteria

| Criterion | Status | Evidence So Far |
|---|---|---|
| **1. Negative space explanation** | Promising | L0 produced 5 physics-grounded negative-space entries. L1 produced 4 context-dependent entries. Not yet tested against the target examples (p-B11 tokamak, steady-state IFE, D-T direct conversion) — those require deeper expansion. |
| **2. Constraint validation rate** | Not yet testable | All 22 L0 constraints are unmappable (expected — physics-level vocabulary). L1 constraints not yet validated. Becomes testable at L2+ where engineering choices map to table columns. |
| **3. Divergence reasoning depth** | Strong | L0 and L1 reasoning goes well beyond table labels. Trade-off structures, requirement interactions, and quantitative physics thresholds are captured. |
| **4. Concept family recovery** | Confirmed at L1 | Closed-magnetic → {plasma-current (tokamak), external-coils (stellarator), hybrid} recovered through physics reasoning, not label recall. |
| **5. Novel paths** | Not yet assessable | Requires L3+ depth |
| **6. Novel variables** | Confirmed | 22 novel variables at L0, referencing physics-level design dimensions absent from the table |
| **7. Transfer visibility** | Not yet assessable | Requires multiple branches expanded to detect shared constraints |

### Key Early Observations

**The unmappability gap is real and informative.** At L0, the LLM reasons about field topology, loss cones, and compression ratios. The table talks about Confinement Family and Magnet Type. These are different levels of abstraction. The reasoning tree exposes the physics-level structure that the classification scheme compressed away. This confirms that the tree captures design dimensions the table missed, but it also means constraint validation (the primary quantitative test) requires deeper expansion to reach the engineering-classification level.

**The requirement lenses produce cross-cutting analysis.** At every node, the LLM examines how each option affects all six requirements. This reveals trade-off structures that the flat table's column-per-dimension format cannot represent — how R2 (achieve fusion) trades against R3 (net energy) differently for mirrors (plug power) vs. tokamaks (current-drive power) vs. IFE (driver efficiency).

**Negative space is the tree's strongest early signal.** The explanations for why certain approaches don't work are precise, physics-grounded, and trace to specific requirement-context interactions. This is the explanatory power the flat table lacked.

---

## 6. Next Steps

1. **Run `validate.py`** on the L1-closed-magnetic expansion to extract and validate its 14 constraints against `table_v2.csv`.
2. **Expand remaining L1 branches** (open magnetic, inertial, magnetized target, electrostatic) to build the breadth needed for cross-branch consistency checking and transfer detection.
3. **Expand L2 selectively** — at minimum the tokamak and stellarator branches under closed-magnetic, and the laser-ICF branch under inertial — to reach the engineering-choice level where constraint validation becomes meaningful.
4. **Run the target negative-space tests**: verify whether the tree's reasoning structure explains the absence of p-B11 tokamaks, steady-state IFE, and D-T direct energy conversion.
5. **Assess transfer visibility** once multiple D-T branches exist (tokamak, stellarator, mirror, laser ICF) to test whether shared tritium-breeding constraints emerge with overlapping justification sets.

### Open Questions

Two design issues surfaced during early execution that need to be resolved before deeper expansion.

#### How should the "next question" be determined?

Currently, each option in an expansion produces a list of 5–6 downstream questions, and the first one on the list automatically becomes the child node's question. The rest are discarded. This means the tree's entire branching structure — which questions get explored, which are ignored — is determined by the LLM's ordering within a single call. There is no ranking, no selection heuristic, and no human choice at this step.

This matters because the LLM at L0 generated questions like "How should rotational transform be provided?" alongside "What is the maximum achievable beta?" and "How should the divertor be designed?" — all valid downstream questions, but they lead to very different tree shapes and would produce different constraint registries. The current design makes this choice implicitly and invisibly.

Possible approaches:
- **Human selection**: after each expansion, present the full question list and let the human reviewer choose which to explore. This is the most controlled option but slows down the expansion loop.
- **Expand all questions as siblings**: treat each downstream question as a separate child node, producing a wider tree. This explores more structure but multiplies the LLM calls proportionally.
- **LLM-ranked selection**: add a second prompt that asks the LLM to rank the downstream questions by which is most architecturally discriminating — i.e., which question's answer would most change the downstream problem landscape.
- **Accept the current approach**: if the constraint registry (not the tree shape) is the primary artifact, the specific question ordering may matter less than it seems. Different tree shapes might produce overlapping constraint sets.

#### How should constraints be validated?

The current validation pipeline uses a hand-built vocabulary map (~90 entries) to translate LLM-generated constraint variables into table column lookups. If the LLM says `{confinement_approach: "magnetic"}`, the mapper finds this in its dictionary and checks `Confinement Family = MFE` in the table. If the LLM says `{field_topology: "closed_toroidal"}`, there is no dictionary entry, and the constraint is classified as UNMAPPABLE.

At L0, all 22 constraints are unmappable. The LLM reasons about physics-level concepts (field topology, loss cones, compression ratios, Earnshaw's theorem) that have no representation in the engineering-classification table. The vocabulary map was designed hoping that deeper tree levels (L2, L3) would produce engineering-level constraints that map naturally to table columns. That hypothesis hasn't been tested yet.

If the LLM continues reasoning at a level of abstraction above the table even at deeper levels — which seems likely given that the interesting constraints are precisely the ones that *aren't* simple category assignments — then the current validation approach won't work. Four options:

1. **Structured ontology**: Force the LLM to express constraints using a predefined vocabulary that maps directly to table columns. This would increase the mappable rate but would constrain the LLM's reasoning to the table's level of abstraction — potentially losing the physics-level reasoning that has been the most interesting output so far.

2. **LLM-based qualitative assessment**: Accept free-form constraints, then use a second LLM call to assess whether a given constraint is consistent with each matching concept. More flexible but introduces assessor bias and is harder to automate reliably.

3. **Cross-branch consistency as the primary validation mechanism**: Rather than validating against the table, focus on whether independently expanded branches produce compatible or contradictory constraints for the same variables. This doesn't require column mapping — it requires only that constraints reference the same *LLM-generated* variables. The spec already describes this (reinforcing/contradicting/extending), but it can only be exercised once multiple branches are expanded.

4. **Accept that table validation may not be practical**: Recognize the constraint registry's value as a *reasoning artifact* rather than an empirically validated rule set. The constraints capture the LLM's first-principles derivation of design-space structure; the table captures engineering classifications. These may operate at different levels of abstraction that don't bridge cleanly. Even without table validation, the constraints are valuable for negative-space explanation, transfer analysis, and understanding concept divergence — the other success criteria don't depend on table validation.

These options are not mutually exclusive. A hybrid approach — structured ontology for engineering-level constraints at L2+, LLM assessment for physics-level constraints at L0–L1, cross-branch consistency throughout — may be the right answer. But the question needs to be resolved before investing heavily in deeper expansion.
