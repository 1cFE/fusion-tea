# Test 4: Blind Row — Design Thesis Recoverability

**Date**: 2026-03-08
**Input**: 5 concepts from `table_v2.csv`, stripped of Concept Name, Company, Overall Confidence, and Driver Technology
**Assessor**: Claude (via `claude -p`, no project context, no rubric shown)
**Rubric**: `test4_rubric.md` (ground truth + scoring criteria, hidden from assessor)

---

## Method

5 concepts selected to span families and vary in expected "column legibility":

| Letter | Concept (hidden from assessor) | Family | Selection rationale |
|--------|-------------------------------|--------|---------------------|
| A | Type One Energy — QI Modular HTS Stellarator | MFE | Differentiator (modularity-for-manufacturing) is subtle; columns overlap with other stellarators |
| B | TAE Technologies — p-B11 FRC | MFE | p-B11 is highly distinctive; Energy Capture = Thermal (steam) is anomalous for aneutronic fuel |
| C | Xcimer Energy — Laser ICF Hybrid Direct Drive | IFE | Core thesis (KrF cost advantage) lives in the withheld Driver Technology column |
| D | General Fusion — Pneumatic MTF | MIF | Mechanical compression + liquid metal wall is highly legible from columns |
| E | LPPFusion — Dense Plasma Focus p-B11 | Non-Standard | DPF + p-B11 is distinctive; extreme-simplicity thesis may or may not come through |

Each concept was sent as a separate `claude -p` call using `test4-prompt.md` (column glossary + 5 open-ended questions). Driver Technology was withheld because it is a near-identifier (37 unique free-text values for 38 concepts).

---

## Scores

| Concept | Thesis (0-2) | Hard Problems (0-2) | Design Logic (0-2) | Differentiation (0-2) | Total |
|---------|:---:|:---:|:---:|:---:|:---:|
| A: Stellarator | 1 | 2 | 1 | 2 | 6/8 |
| B: p-B11 FRC | 2 | 2 | 2 | 2 | 8/8 |
| C: Hybrid Laser ICF | 2 | 2 | 2 | 2 | 8/8 |
| D: Pneumatic MIF | 2 | 2 | 2 | 2 | 8/8 |
| E: DPF p-B11 | 2 | 1 | 2 | 2 | 7/8 |
| **Total** | **9** | **9** | **9** | **10** | **37/40** |

---

## Scoring Rationale

### Concept A — Type One Energy (6/8)

**Thesis = 1**: The assessor's lead thesis is "steady-state without disruptions + HTS makes it compact" — which describes any HTS stellarator, not specifically Type One. Modularity is mentioned but as a sub-choice, not the core bet. In the differentiation section they approach it ("manufacturable enough") but don't articulate the specific innovation: factory-fabricable coil modules, field-replaceable segments, maintenance access through modularity.

**Hard Problems = 2**: Correctly names (1) 3D HTS coil fabrication in non-planar geometry, (2) blanket integration in complex 3D surfaces, (3) achieving burning plasma in an optimized stellarator. Identifies the tension between physics-optimal and engineering-optimal coil shapes.

**Design Logic = 1**: Good connections (stellarator → steady-state, D-T → breeding, ECRH → stellarator geometry) but misses the key HCPB ↔ modular maintenance link. The solid ceramic breeder was chosen specifically because solid, removable blanket segments fit the modular maintenance concept — unlike liquid systems in 3D geometry. The assessor calls HCPB a "conservative choice" without seeing this connection.

**Differentiation = 2**: Correctly identifies modularity as distinguishing this from other stellarator types (QI, helical, planar). States the USP as "the first stellarator that can be built at reactor scale."

### Concept B — TAE Technologies (8/8)

All dimensions at 2. The assessor reconstructed the full thesis (aneutronic simplification bet), named all three critical challenges (radiation barrier with Z² bremsstrahlung, 500× harder Lawson criterion, compact toroid stability), connected the full design logic chain (p-B11 → no breeding → simpler reactor, FRC → high-β → resistive magnets adequate, NBI → sustainment), and correctly flagged the Thermal (steam) anomaly for p-B11 with three hypotheses.

### Concept C — Xcimer Energy (8/8)

All dimensions at 2. Despite the core thesis (KrF excimer cost advantage) being in the withheld Driver Technology column, the assessor correctly inferred: Sub-Hz implies a driver with rep-rate limitations, hybrid drive provides coupling/symmetry advantages, and the concept trades rep rate for higher gain per shot. The rubric was designed to be achievable from approach-level inference rather than requiring specific technology identification.

### Concept D — General Fusion (8/8)

All dimensions at 2. The assessor reconstructed the complete thesis including both key innovations: cheap mechanical compression AND the multi-function liquid metal wall ("serves as blanket, shield, and structural medium all at once — this is a feature, not a compromise"). Correctly identified all major challenges (repetitive target formation, plasma lifetime vs. compression timescale, liquid metal hydrodynamics).

### Concept E — LPPFusion (7/8)

**Hard Problems = 1**: Correctly named electrode erosion at high rep rate and the bremsstrahlung radiation barrier (Z² scaling). But did not name pinch instabilities (Rayleigh-Taylor, sausage, kink) which are the specific physics mechanism limiting DPF performance, and did not frame DPF scaling as a distinct challenge (whether net energy gain is achievable at any scale). Substituted direct-conversion engineering as the third challenge — valid but not the most critical. All other dimensions at 2, including the extreme-simplicity thesis and the non-equilibrium plasma claim.

---

## Methodological Concern: Domain Knowledge Contamination

The 37/40 aggregate score must be interpreted with a major caveat: **the assessor (Claude) has extensive training data about these specific companies and concepts.** Even without the concept name, column combinations like "p-B11 + Compact Toroid + NBI" are effectively identifiable by a domain-knowledgeable assessor. Evidence of recognition rather than pure inference:

- Concept B: Assessor mentions "beam-target fusion" strategy — a TAE-specific operational detail not in the columns
- Concept E: Assessor mentions "non-equilibrium T_ion >> T_electron" — a specific LPPFusion physics claim not in the columns
- Concept A: Assessor references the "post-Wendelstein-7-X approach" — a historical context not derivable from columns

This means the scores measure **columns + domain knowledge**, not columns alone. A non-domain-expert assessor would score lower. The scores are an upper bound on column informativeness.

However, the **relative scores** remain informative, because domain knowledge is approximately constant across concepts while column legibility varies. The finding that Concept A scores 6/8 while B/C/D score 8/8 reflects a real difference in how much the columns carry.

---

## Findings

### 1. The columns carry approach-level information, not strategy-level

The columns encode *what choices were made* but not *why those choices constitute an advantage*. For concepts with distinctive design choices (unique fuel, unique mechanism), the "what" implies the "why":

| Concept | Distinctive column values | Thesis recoverable? |
|---------|--------------------------|:---:|
| B (TAE) | p-B11, Compact Toroid, NBI, Resistive, Minimal neutrons | Yes — fuel choice implies entire thesis |
| D (General Fusion) | Mechanical compression, Liquid metal wall, Self-confined | Yes — mechanism is the thesis |
| E (LPPFusion) | Plasma focus, p-B11, Direct conversion, High rep rate | Yes — mechanism + fuel imply thesis |
| C (Xcimer) | Hybrid drive, Sub-Hz | Partially — approach thesis yes, technology thesis (KrF) no |
| A (Type One) | Modular (Stellarator Type) | Partially — family thesis yes, manufacturing thesis no |

**Pattern**: The table is most informative for concepts that ARE their design choice (DPF IS the concept, p-B11 IS the bet). It is least informative for concepts competing within the same approach category, where differentiation lives in engineering strategy (modularity-for-manufacturing, KrF cost-per-joule) rather than in morphological choices.

### 2. The table doesn't carry what experts would consider "the interesting part"

For most concepts, the engineering strategy and innovation thesis are invisible in the columns:

| Missing information | Example |
|--------------------|---------|
| **Manufacturing strategy** | Type One's factory-fabricable modules vs. Proxima's continuous 3D wound coils |
| **Technology cost thesis** | Xcimer's KrF cost-per-joule advantage vs. DPSSL competitors |
| **Development roadmap** | TAE's stepping-stone path (D-T → D-He3 → p-B11) |
| **Key parameter claims** | General Fusion's piston synchronization precision requirements |
| **Physics innovation** | LPPFusion's non-equilibrium ion/electron temperature claim |

These are exactly the things that differentiate competing concepts within the same family — and they're what investors, engineers, and domain experts care about most. The table correctly classifies the approach category but doesn't reach the level of information that matters for evaluation.

### 3. The "Information Gaps" responses converge on common missing categories

All 5 assessors independently identified the same types of missing information needed for a preliminary engineering assessment:

| Category | All 5 requested? | Example |
|----------|:-:|---------|
| Scale parameters (volume, field, power) | Yes | "Cannot estimate power output without knowing machine size" |
| Performance targets (Q, τ_E, T_i) | Yes | "What fusion gain has been achieved and what is projected?" |
| Cost basis ($/W, capex, driver cost) | Yes | "No validated cost models exist for 3D HTS coils at scale" |
| Withheld Driver Technology | Yes | "The specific hardware approach, which likely distinguishes this" |
| Development status / experimental evidence | 4 of 5 | "What T_i, n_e, τ_E have been demonstrated?" |

This convergence partially preempts Test 5 (Concept Initiation Gap Analysis). The gap between "classification table" and "design specification" is the same regardless of which concept you examine: the table lacks quantitative parameters, performance claims, cost basis, and engineering detail.

### 4. Score gradient matches predicted column legibility

Pre-test prediction was: D (highest) → B, E (high) → C (medium, KrF hidden) → A (lowest, modularity invisible). Actual results: B=C=D > E > A. The prediction was mostly correct — A is the lowest, D is tied for highest, and E's slightly lower score (missed pinch instabilities) was a minor surprise.

The interesting case is C = 8/8 despite the thesis being in the withheld column. This tells us the rubric measured approach-level inference (achievable from columns) rather than technology-level thesis (requires Driver Technology). A rubric that required "identify KrF excimer as the laser type" would have scored C at 6/8 or lower — revealing that the Driver Technology column carries the thesis for concepts whose innovation is in the specific technology, not the approach category.

---

## Implications for the Phase 1d Synthesis

1. **The table is a good approach-level classification** — it correctly groups concepts by physics category and captures the primary design choices. For concepts with distinctive approaches (unique fuel, unique mechanism), the classification itself carries the thesis.

2. **The table fails at within-family differentiation** — concepts competing in the same approach category (multiple stellarators, multiple D-T laser ICF concepts) are not meaningfully distinguished by their column values. The differentiation lives in engineering strategy and technology details that the table doesn't encode.

3. **The gap between classification and design specification is quantitative parameters + engineering strategy** — the missing information is: scale, performance targets, cost basis, and the "why this implementation" rationale. This is what Chunk 2's pattern cards or AND/OR graph would need to add.

4. **Test 5 may be redundant** — the "Information Gaps" responses from all 5 concepts already identify the common gap categories that Test 5 was designed to find. The synthesis report can draw on these directly.
