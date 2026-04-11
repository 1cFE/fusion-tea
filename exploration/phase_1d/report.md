# Phase 1d Synthesis Report: Classification Scheme or Design Space?

**Date**: 2026-03-08
**Input**: v2 differentiation table (38 concepts × 18 columns), Phase 1b_v2 quantitative results
**Tests completed**: Test 1 (Vocabulary Completeness), Test 2 (Generative Coherence), Test 2v2 (Family-Conditional Coherence), Test 4 (Blind Row Recoverability)
**Test skipped**: Test 5 (Concept Initiation Gap Analysis) — preempted by Test 4 findings

---

## Verdict

**The v2 differentiation table is a classification scheme, not a design space.**

It describes *what* each fusion concept chose across 18 columns, but it does not capture *why* those choices cohere into a design thesis, and it cannot generate new viable concepts. The columns are not independent design dimensions — they are correlated observations of approximately two underlying decisions (confinement concept and fuel cycle). The table's apparent 18-dimensional Cartesian structure vastly overstates the true degrees of freedom.

This verdict rests on converging evidence from four tests and the Phase 1b_v2 quantitative baseline. The evidence ranges from strong (computational N/A analysis, 0% unconditional coherence) to softer (LLM-assessed coherence scoring, domain-knowledge-contaminated blind-row test). No individual test is conclusive; the convergence across methods is what makes the verdict robust.

---

## 1. Vocabulary Completeness (Test 1)

**Question**: Does the controlled vocabulary span the physically plausible design space, or just the choices observed in the 38-concept sample?

**Result**: 9 closed columns, 8 open columns, 1 open by design (Driver Technology).

| Classification | Count | Columns |
|:---:|:---:|---|
| Closed | 9 | Confinement Family, Tokamak Shape, Fuel, Plasma State, Tritium Breeding, Neutron Management, Operation Mode, Repetition Rate, Stellarator Type* |
| Open | 8 | MFE Topology, IFE Driver, MIF Method, Non-Standard Mechanism, Laser Approach, Primary Heating, Energy Capture, Magnet Type |
| Open (by design) | 1 | Driver Technology (free text, 37 unique values) |

*Stellarator Type is technically open (missing QA, QH) but the missing values are historical and unlikely to reappear commercially.

### What's missing and why

21 missing vocabulary candidates were identified across the 8 open columns:

| Gap Type | Count | Pattern |
|---|:---:|---|
| **(a) Historical** — no startup has revived | 10 | RFP, spheromak, wire-array Z-pinch, light ion beam, plasma jet MITF, QA stellarator, QH stellarator, shock ignition, MHD direct conversion (coal-era) |
| **(b) Theoretical** — never attempted for power | 4 | Beam-target, pyroelectric, MHD direct conversion (fusion), He Brayton |
| **(c) Lumped** — exist but hidden under coarser labels | 7 | Spheromak in "Compact Toroid," LH in "RF," NI-HTS in "HTS," laser-driven MIF in "Magnetized target," He Brayton in "Thermal," QA/QH vs coil-type conflation, permanent magnets in primary coil type |

**Interpretation**: The vocabulary is shaped by the current commercial landscape — what the ~38 funded startups chose — not by the full space of physically achievable approaches. The dominant gap type is historical approaches that were investigated and abandoned. The lumped gaps (type c) reveal places where independent design axes are compressed into compound labels, hiding combinatorial structure that a design space would expose.

### Structural findings

Three cross-cutting observations emerged that bear directly on the classification-vs-design-space question:

**Axis conflation**: Three columns — Stellarator Type, Magnet Type, Primary Heating — each conflate multiple independent design axes into a single vocabulary. Stellarator Type mixes optimization strategy (QI, QA, QH) with coil engineering (modular, planar, helical). Magnet Type mixes superconductor material, winding geometry, insulation strategy, and operating mode. This conflation is invisible for classification (each concept maps to one compound label) but prevents generative use (the compound labels can't be independently varied).

**Family-dependent semantics**: Primary Heating has 18 real values — 4.5× more than Confinement Family — and its information-theoretic role changes by family. For MFE, it's a genuine design choice (ECRH vs. ICRH vs. NBI). For IFE/MIF/Non-Standard, it's a concept identifier — "Laser (direct drive)" doesn't describe a choice *within* the concept, it IS the concept. This is context-dependence hiding inside a flat column, a milder version of the Phase 1b near-ID problem.

**Granularity asymmetry**: Vocabulary size varies 9× across controlled-vocabulary columns (2 values for MIF Method, 18 for Primary Heating). Zwicky's morphological analysis assumes comparable vocabulary sizes per dimension. The 9× range means the columns operate at fundamentally different levels of abstraction — some are genuine morphological dimensions, others are empirical inventories approaching near-ID behavior.

---

## 2. Generative Coherence (Tests 2 and 2v2)

**Question**: Can the table produce viable new concepts by random combination?

### Test 2: Unconditional sampling

30 random concepts generated by uniform sampling from per-column vocabularies, with structural N/A rules applied.

| Metric | Result |
|---|---|
| Physically coherent | 0/30 (0%) |
| Engineering plausible | 0/30 (0%) |
| Novel coherent | 0 |

Zero coherence. Not low — zero. Random combination across the full vocabulary never produces a viable concept. The failures are dominated by hard physics incompatibilities (~60%): IFE + sustained plasma, D-T fuel + aneutronic shielding, acoustic driver + laser heating. Engineering mismatches account for ~25%, coherence gaps ~15%.

### Test 2v2: Family-conditional sampling

30 random concepts generated with sampling conditioned on Confinement Family — each concept draws non-confinement column values only from the vocabulary observed within its family.

| Metric | Unconditional | Family-conditional |
|---|:---:|:---:|
| Physically coherent | 0/30 (0%) | 7/30 (23%) |
| Engineering plausible | 0/30 (0%) | 5/30 (17%) |
| Novel coherent | 0 | 7 |

The jump from 0% to 23% confirms that cross-family contamination was a real failure source — about a quarter of the failure budget. But 77% of failures persist as within-family constraints: concept-level coupling (stellarator → no ohmic heating, tokamak → not 10 Hz rep rate) and fuel-cascade constraints (D-T → heavy shielding + breeding blanket).

**Quality of the 7 "coherent" concepts**: 3 DPF near-duplicates, 2 known concepts (fast ignition, DPF p-B11), 1 trivial fuel swap (D-D stellarator), 1 genuinely interesting variant (orbital dipole + p-B11 + NBI). Hit rate for interesting novel concepts: **~3%** (1/30).

### Interpretation thresholds (from sprint plan)

| Coherence rate | Interpretation | Observed |
|---|---|---|
| >50% | Columns largely independent; approximates a true design space | — |
| 10-50% | Moderate coupling; some independent dimensions, some correlated | 23% (family-conditional) |
| <10% | Tightly coupled; classification scheme, not design space | 0% (unconditional) |

The unconditional result (0%) places the table firmly in "classification scheme" territory. The family-conditional result (23%) reaches "moderate coupling" on paper, but the quality of the coherent concepts (mostly trivial variants) undermines even this modest reading.

---

## 3. Constraint Structure (Derived from Tests 2 and 2v2)

**Question**: Which column pairs are tightly coupled, and how far is the table from a Cartesian product?

### Coupling clusters

Three tightly coupled clusters account for most of the constraint structure:

**Cluster 1 — Confinement-Heating-Plasma** (4 columns): Confinement Family ↔ Primary Heating ↔ Plasma State ↔ Operation Mode. Selecting one constrains the others to a small set. IFE forces pulsed/compressed/driver-is-heater. MFE forces sustained/steady-state/RF-or-NBI. MIF forces pulsed/compressed/compression-heating.

**Cluster 2 — Fuel-Neutron-Energy** (4 columns): Fuel ↔ Neutron Management ↔ Tritium Breeding ↔ Energy Capture. Fuel choice cascades deterministically: D-T → heavy shielding + breeding blanket + thermal capture. p-B11 → minimal shielding + no breeding + direct conversion. These are consequences of fuel selection, not independent design choices.

**Cluster 3 — Driver-Hardware** (3+ columns): Driver Technology ↔ Magnet Type ↔ IFE Driver (or MIF Method or Non-Standard Mechanism). The hardware must implement the stated mechanism.

### Top constraint pairs by failure frequency

| Column Pair | Test 2 failures | Test 2v2 failures | Nature |
|---|:---:|:---:|---|
| Fuel × Neutron Management | 20/30 | 19/30 | Fuel cascade — persists even with family conditioning |
| Confinement × Primary Heating | — | 13/30 | Concept-specific — concept determines heating |
| Driver Technology × IFE Driver | 11/30 | — | Cross-family contamination — eliminated by conditioning |
| Confinement × Magnet Type | — | 9/30 | Concept-specific — concept determines coil geometry |
| Confinement Family × Primary Heating | 7/30 | — | Cross-family — partially eliminated by conditioning |

**Fuel × Neutron Management** is the single most persistent coupling, dominating both tests. It's a hard physical constraint that no amount of table restructuring can soften — D-T produces 14.1 MeV neutrons, p-B11 doesn't, and the management approach must match.

### Effective degrees of freedom

Within each family, the effective DOF are far fewer than the column count suggests:

| Family | Columns sampled | Effective DOF | Free choices |
|---|:---:|:---:|---|
| MFE | ~11 | ~2 | Concept (free) + Fuel (semi-free, ~2-4 options) |
| IFE | ~11 | ~2-3 | Concept (free) + Fuel (semi-free) + Rep rate (somewhat free) |
| MIF | ~11 | ~2 | Concept (free) + Fuel (semi-free) |
| Other | ~11 | ~1-2 | Each concept is its own island |

The effective design space is approximately **19 concept types × ~3 fuel options ≈ 57 cells**, minus infeasible pairs (p-B11 on most MFE topologies, muon catalysis with non-hydrogen fuels), yielding perhaps **30-40 physically coherent combinations**. This is a lookup table, not a combinatorial space.

---

## 4. Explanatory Power (Test 4)

**Question**: How much of a concept's design thesis can an expert reconstruct from the table row alone?

### Scores

5 concepts spanning families, assessed via blind presentation (concept name and Driver Technology withheld):

| Concept | Family | Thesis | Hard Problems | Design Logic | Differentiation | Total |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Type One Energy (QI modular stellarator) | MFE | 1 | 2 | 1 | 2 | 6/8 |
| TAE Technologies (p-B11 FRC) | MFE | 2 | 2 | 2 | 2 | 8/8 |
| Xcimer Energy (hybrid laser ICF) | IFE | 2 | 2 | 2 | 2 | 8/8 |
| General Fusion (pneumatic MIF) | MIF | 2 | 2 | 2 | 2 | 8/8 |
| LPPFusion (DPF p-B11) | Non-Standard | 2 | 1 | 2 | 2 | 7/8 |
| **Total** | | **9** | **9** | **9** | **10** | **37/40** |

### Methodological caveat

The 37/40 score is an **upper bound** on column informativeness, contaminated by the assessor's (Claude's) domain knowledge. Evidence of recognition rather than inference: the assessor mentioned TAE-specific operational details, LPPFusion-specific physics claims, and historical context not derivable from columns. The absolute scores overstate what the columns alone carry.

The **relative scores** are more informative — domain knowledge is roughly constant across concepts, so score differences reflect genuine differences in column legibility.

### What the columns carry vs. what they don't

The table is most informative for concepts that ARE their design choice:

| Column legibility | Concepts | Why |
|---|---|---|
| High — thesis recoverable from columns | TAE (p-B11 FRC), General Fusion (pneumatic MIF), LPPFusion (DPF p-B11) | The mechanism or fuel IS the thesis |
| Medium — approach recoverable, technology thesis hidden | Xcimer (hybrid laser ICF) | KrF cost advantage lives in withheld Driver Technology |
| Lower — family thesis visible, manufacturing thesis invisible | Type One (modular stellarator) | Modularity-for-manufacturing isn't a column value |

**Pattern**: The table is a good approach-level classification — it correctly groups concepts by physics category and captures the primary design choices. It fails at within-family differentiation, where competing concepts (multiple stellarators, multiple D-T laser ICF concepts) are distinguished by engineering strategy and technology details that the columns don't encode.

### Information gap categories

All 5 assessors independently identified the same types of missing information:

| Category | Requested by | Example |
|---|:---:|---|
| Scale parameters (volume, field, power) | 5/5 | "Cannot estimate power output without knowing machine size" |
| Performance targets (Q, τ_E, T_i) | 5/5 | "What fusion gain has been achieved and what is projected?" |
| Cost basis ($/W, capex, driver cost) | 5/5 | "No validated cost models exist for 3D HTS coils at scale" |
| Driver Technology (withheld) | 5/5 | "The specific hardware approach likely distinguishes this" |
| Development status / experimental evidence | 4/5 | "What T_i, n_e, τ_E have been demonstrated?" |

This convergence preempted Test 5 (Concept Initiation Gap Analysis). The gap between classification and design specification is the same regardless of concept: the table lacks quantitative parameters, performance claims, cost basis, and engineering detail.

---

## 5. The Tree Structure

The combined evidence from all tests converges on the same structural picture. The table is not a grid of 18 independent dimensions — it is a shallow tree with approximately two branch points:

```
Confinement Family (MFE / IFE / MIF / Non-Standard)
  └── Confinement Concept (~19 types)
        ├── Primary Heating          ← determined by concept
        ├── Magnet Type              ← determined by concept
        ├── Operation Mode           ← determined by concept
        ├── Repetition Rate          ← determined by concept
        ├── Plasma State             ← determined by concept
        └── Fuel (semi-free, ~2-4 options per concept)
              ├── Neutron Management  ← determined by fuel
              ├── Tritium Breeding    ← determined by fuel
              └── Energy Capture      ← determined by fuel
```

The flat table representation forces this tree into a Cartesian product, creating the illusion of combinatorial freedom that doesn't exist. The 0% unconditional coherence rate is a direct consequence: randomly sampling across correlated columns is equivalent to randomly assembling tree nodes from different branches.

### Evidence for tree structure from each test

| Test | Evidence |
|---|---|
| Phase 1b_v2 | N/A density 36.7%, monotonically increasing with granularity — deeper questions apply to narrower concept subsets |
| Test 1 | Primary Heating has family-dependent semantics (design choice for MFE, identifier for IFE/MIF/NS) |
| Test 2 | 0% coherence from flat sampling; three tightly coupled clusters map to tree branches |
| Test 2v2 | Family conditioning recovers 23% — confirming the first branch point matters, but within-branch coupling dominates |
| Test 4 | Approach-level information recoverable, strategy-level invisible — the tree carries "what branch," not "why this leaf" |

---

## 6. Strength of Evidence

Not all evidence is equal. An honest accounting:

### Strong (computational, reproducible)

- **N/A density progression** (Phase 1b_v2): 10.5% → 27.7% → 36.7% across three granularity levels. Computed by Python script from CSV data. Every N/A traces to a structural upstream decision.
- **Minimum discriminating set** (Phase 1b_v2): Went from 2 (with near-ID column) to 4 (without). Brute-force enumeration of all 2^18 column subsets.
- **0% unconditional coherence** (Test 2): Even with generous LLM assessment, zero of 30 random concepts passed. The magnitude of the failure is robust to assessor bias.
- **Vocabulary completeness inventory** (Test 1): Direct enumeration of observed vs. plausible values. Factual claims about physics, verifiable against literature.

### Moderate (LLM-assessed, but pattern is clear)

- **23% family-conditional coherence** (Test 2v2): The absolute number has unknown assessor bias (Claude may be too strict or lenient). But the delta from 0% → 23% and the quality breakdown (mostly trivial variants) are informative regardless of the exact threshold.
- **Constraint pair frequencies** (Tests 2, 2v2): Derived from LLM failure annotations, not systematic pairwise review. The top pairs (Fuel × Neutron Management at 19-20/30) are robust; the long tail of weaker couplings is less certain.
- **~2 DOF estimate** (Test 2v2): Inferred from failure pattern analysis, not computed by enumerating valid combinations. Directionally correct but the exact number is soft.

### Softer (significant caveats)

- **Blind row scores** (Test 4): 37/40, but contaminated by Claude's training-data recognition of specific companies. Relative scores (A < E < B=C=D) are more trustworthy than absolute scores.
- **~30-40 valid combinations estimate** (Test 2v2 synthesis): Stated but not verified by enumeration.
- **Granularity progression causality** (Phase 1b_v2): The v2 table was designed with the context-dependence hypothesis in mind. The clean monotonic progression confirms the prediction, but the table's architect chose the decomposition.

### Not tested

- Whether the AND/OR graph representation actually adds value over the flat table for TEA comparison
- Whether context-dependence deepens further with engineering-level columns (blanket type, coolant, first-wall material)
- Whether pattern-card transfer across concepts sharing sub-problem context actually works
- Whether the ~38-concept sample is sufficient (21 missing vocabulary candidates suggest the full historical space is materially larger)

---

## 7. Implications for Chunk 2

The diagnosis is clear. The table is a classification scheme with ~2 effective degrees of freedom, not an 18-dimensional design space. The question for Chunk 2 is: what representation should replace or augment it?

### What the flat table does well (keep)

- **Approach-level classification**: Correctly groups concepts by physics category. For concepts with distinctive approaches, the classification itself carries the thesis.
- **Cross-concept comparison on universal axes**: Fuel, Operation Mode, and Repetition Rate are genuinely comparable across families.
- **N/A pattern as structural information**: The N/A distribution itself encodes where the design space branches — which questions apply to which families.

### What Chunk 2 must add

**1. Explicit constraint structure.** The tree should be encoded, not implied. Concept → {determined columns} as a bundle. Fuel → {downstream consequences} as a cascade. The AND/OR graph representation from the context document is the natural fit — OR nodes for concept/fuel choices, AND nodes for the sub-problems each choice generates.

**2. Within-family differentiation.** The table fails to distinguish concepts competing in the same approach category. The missing information is engineering strategy (manufacturing approach, cost thesis, development pathway) and technology-specific detail (KrF vs. DPSSL, insulated vs. NI-HTS, modular vs. continuous winding). Pattern cards should capture what makes each concept's implementation unique — not just which branch of the tree it sits on.

**3. Quantitative parameters.** All 5 Test 4 assessors requested the same categories: scale (volume, field, power), performance targets (Q, τ_E, T_i), cost basis ($/W, capex), and development status. These are what bridge classification → design specification. They don't belong in the morphological table (they're continuous, not categorical), but they must be associated with each concept in whatever structure Chunk 2 builds.

**4. Cross-concept transfer mapping.** The strongest practical motivation from the context document (Section 7): when two concepts arrive at the same sub-problem via different branches (e.g., D-T tokamak and D-T mirror both reaching "solve tritium breeding"), the shared context justifies reusing models and cost estimates. The AND/OR graph should make these shared sub-problem nodes explicit, enabling principled transfer rather than ad hoc analogy.

### What Chunk 2 should NOT attempt

- **Generative concept exploration via the flat table.** The 0% coherence rate rules this out. New concepts emerge from domain insight and physics reasoning, not from combinatorial sampling.
- **Expanding the column set.** Adding more columns to a classification scheme makes it a more detailed classification scheme. The problem is structural (correlated columns, tree crammed into grid), not a matter of resolution.
- **Precise constraint density quantification.** The constraint structure is dominated by a few obvious clusters (concept-identity, fuel-cascade, driver-hardware). Quantifying every pairwise coupling to three decimal places adds precision without insight.

---

## Summary Table

| Question | Answer | Confidence | Key evidence |
|---|---|---|---|
| Design space or classification scheme? | Classification scheme | High | 0% unconditional coherence, ~2 DOF, 3 tightly coupled clusters |
| Is the design space context-dependent? | Yes | High | 36.7% N/A density, monotonic granularity progression, family-dependent column semantics |
| Does the vocabulary span the physics design space? | Partially — 8 of 17 CV columns are open | Moderate | 21 missing candidates, dominated by historical approaches |
| Can the table generate viable new concepts? | No | High | 0% unconditional, 3% interesting-novel with family conditioning |
| Does the table carry design thesis information? | Approach-level yes, strategy-level no | Moderate | 37/40 blind-row score (upper bound), within-family differentiation fails |
| What's the effective dimensionality? | ~2 (concept + fuel) | Moderate | Inferred from failure analysis, not enumerated |
| What should Chunk 2 build? | AND/OR graph with constraints, parameters, and pattern cards | — | Recommendation, not a test result |
