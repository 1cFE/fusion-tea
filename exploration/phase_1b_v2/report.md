# Phase 1b v2: Confinement Hierarchy Analysis Report

**Date**: 2026-03-08
**Input**: `table_v2.csv` — 38 concepts × 18 differentiation columns
**Script**: `analyze.py` — brute-force discriminating set + N/A density + granularity progression

---

## 1. Data Summary

The v2 table replaces the original 2 confinement columns (Confinement Family, Confinement Concept) with an 8-column hierarchical tree:

| Column | Scope | Values | N/As |
|--------|-------|--------|------|
| Confinement Family | All 38 | 4 | 0 |
| MFE Topology | 19 MFE | 5 | 19 |
| IFE Driver | 12 IFE | 4 | 26 |
| MIF Method | 3 MIF | 2 | 35 |
| Non-Standard Mechanism | 4 NS | 3 | 34 |
| Tokamak Shape | 6 Tokamaks | 4 | 32 |
| Stellarator Type | 6 Stellarators | 4 | 32 |
| Laser Approach | 9 Laser IFE | 6 | 29 |

The 10 non-confinement columns (Fuel through Driver Technology) are unchanged from v1.

**Total**: 251 N/A cells out of 684 (38 × 18) = **36.7%**.

---

## 2. Discrimination Analysis

### Is the near-ID problem gone?

**Yes.** In v1, {Confinement Concept} alone discriminated 37/38 rows — it was functionally an ID column. The minimum discriminating set was {Confinement Concept, Tritium Breeding}, meaning 9 of 11 CV columns were informationally redundant.

In v2, no single confinement column comes close to being an ID. The **minimum discriminating set is 4 columns**, with 6 distinct 4-column sets achieving maximum discrimination (37/38 groups):

| Set | Columns |
|-----|---------|
| 1 | Laser Approach, Primary Heating, Magnet Type, Tritium Breeding |
| 2 | Fuel, Primary Heating, Magnet Type, Tritium Breeding |
| 3 | Primary Heating, Energy Capture, Plasma State, Tritium Breeding |
| 4 | Primary Heating, Energy Capture, Magnet Type, Tritium Breeding |
| 5 | Primary Heating, Magnet Type, Tritium Breeding, Neutron Management |
| 6 | Primary Heating, Magnet Type, Tritium Breeding, Repetition Rate |

Every discriminating set requires columns from BOTH the confinement hierarchy AND the non-confinement columns. No single branch of the table carries all the information.

**Remaining collision**: Laser ICF - Indirect Drive (D-T) ↔ Laser ICF - NIF Commercialization (D-T). These are two plant designs from the same company (Inertia Enterprises) using the same physics approach — identical on all 17 CV columns. Only the free-text Driver Technology column distinguishes them. This is expected: they ARE the same concept with different engineering implementations.

### Greedy column ranking

| Rank | Column | Groups | Collisions |
|------|--------|--------|------------|
| 1 | Primary Heating | 20 | 18 |
| 2 | Tritium Breeding | 34 | 4 |
| 3 | Energy Capture | 36 | 2 |
| 4 | Plasma State | 37 | 1 |

Primary Heating is the top discriminator — its 20 unique values immediately resolve most of the table. The confinement hierarchy columns don't appear until rank 5+ because their high N/A rates limit their marginal discrimination. This is correct behavior: family-specific columns can't help discriminate across families.

### Entropy comparison

The highest-entropy columns are the non-confinement columns that apply universally:

| Column | Entropy (bits) | Unique values |
|--------|---------------|---------------|
| Primary Heating | 3.96 | 20 |
| Magnet Type | 3.06 | 12 |
| Tritium Breeding | 2.91 | 9 |

The family-specific confinement columns have lower entropy because N/A dominates their distributions:

| Column | Entropy (bits) | Unique values |
|--------|---------------|---------------|
| MFE Topology | 2.06 | 6 (incl. N/A) |
| IFE Driver | 1.28 | 5 (incl. N/A) |
| MIF Method | 0.47 | 3 (incl. N/A) |

This is expected and desirable — these columns carry concentrated information within their scope, diluted by N/A outside it.

---

## 3. N/A Density

### Overall

| Metric | v1 (12 cols) | v2 (18 cols) |
|--------|-------------|-------------|
| Total cells | 456 | 684 |
| N/A cells | 44 | 251 |
| N/A rate | 9.6% | 36.7% |
| Differentiation columns | 12 | 18 |
| Min discriminating set | 2 | 4 |

### Per-column rates

Columns with highest N/A rates (all from the confinement hierarchy):

| Column | N/A rate | Why |
|--------|---------|-----|
| MIF Method | 92% (35/38) | Only 3 MIF concepts |
| Non-Standard Mechanism | 89% (34/38) | Only 4 NS concepts |
| Tokamak Shape | 84% (32/38) | Only 6 tokamaks |
| Stellarator Type | 84% (32/38) | Only 6 stellarators |
| Laser Approach | 76% (29/38) | Only 9 laser IFE |
| IFE Driver | 68% (26/38) | Only 12 IFE |
| MFE Topology | 50% (19/38) | Only 19 MFE |

Non-confinement columns with N/A:

| Column | N/A rate | Why |
|--------|---------|-----|
| Repetition Rate | 55% (21/38) | Steady-state/quasi-steady concepts |
| Magnet Type | 34% (13/38) | IFE + muon-catalyzed |
| Tritium Breeding | 24% (9/38) | Non-tritium fuels |
| Plasma State | 3% (1/38) | Muon-catalyzed only |

Seven columns have zero N/As: Confinement Family, Fuel, Primary Heating, Energy Capture, Neutron Management, Operation Mode, Driver Technology.

### Structural N/A chains

Every N/A traces to an upstream design decision:

```
Confinement Family ≠ MIF  ─────────────────────→  N/A MIF Method (35)
Confinement Family ≠ Non-Standard  ────────────→  N/A Non-Standard Mechanism (34)
Confinement Family ≠ IFE  ─────────────────────→  N/A IFE Driver (26)
                                                   N/A Laser Approach (26)
Confinement Family ≠ MFE  ─────────────────────→  N/A MFE Topology (19)
                                                   N/A Tokamak Shape (19)
                                                   N/A Stellarator Type (19)
MFE Topology ≠ Tokamak  ──────────────────────→  N/A Tokamak Shape (13)
MFE Topology ≠ Stellarator  ──────────────────→  N/A Stellarator Type (13)
IFE Driver ≠ Laser  ──────────────────────────→  N/A Laser Approach (3)
Operation Mode = Steady-state/Quasi-steady  ──→  N/A Repetition Rate (21)
Fuel = p-B11 / D-D / D-He3  ─────────────────→  N/A Tritium Breeding (9)
```

Every N/A is structurally justified. There are zero arbitrary or data-quality N/As.

### Block structure

N/A density is remarkably uniform across families:

| Family | Concepts | N/A rate |
|--------|----------|---------|
| MFE | 19 | 36% |
| IFE | 12 | 37% |
| MIF | 3 | 33% |
| Non-Standard | 4 | 42% |

This uniformity is expected: each family gets N/A in the other families' columns, and each has its own sub-type columns that only it fills in. Non-Standard is slightly higher because it has fewer sub-type columns to fill (only 1 applicable: Non-Standard Mechanism) while still getting N/A in all other families' columns.

---

## 4. Granularity Progression

The core prediction from the context-dependent design spaces hypothesis: N/A density should increase monotonically with confinement granularity, because deeper questions become applicable to narrower concept subsets.

| Level | Confinement cols | Conf N/As | Total N/As | Total cells | N/A rate |
|-------|-----------------|-----------|-----------|-------------|---------|
| 0: Family only | 1 | 0 | 44 | 418 | 10.5% |
| 1: + sub-type | 5 | 114 | 158 | 570 | 27.7% |
| 2: + shape/type/approach | 8 | 207 | 251 | 684 | 36.7% |

**Level 0 → 1**: Adding 4 family-specific columns (MFE Topology, IFE Driver, MIF Method, Non-Standard Mechanism) introduces 114 new N/As. These are "which family are you NOT in?" N/As — each concept gets N/A in 3 of 4 family-specific columns.

**Level 1 → 2**: Adding 3 sub-type columns (Tokamak Shape, Stellarator Type, Laser Approach) introduces 93 more N/As. These are deeper "which sub-type are you NOT?" N/As — each concept gets N/A in columns for sub-types outside its branch.

The progression is monotonic and accelerating in absolute terms (0 → 114 → 207 N/As from confinement), though the marginal rate decreases (0 → +114 → +93) because the deeper columns apply to smaller subsets.

**This directly confirms the hypothesis**: the fusion concept design space is context-dependent. Questions that are meaningful for one branch are structurally inapplicable to others, and the deeper you go, the more branch-specific the questions become.

---

## 5. v1 → v2 Comparison

| Metric | v1 | v2 | Interpretation |
|--------|----|----|---------------|
| Differentiation columns | 12 | 18 | +6 from decomposing confinement |
| N/A rate | 9.6% | 36.7% | Context-dependence now visible |
| Min discriminating set | 2 | 4 | No more near-ID column |
| Top discriminator | Confinement Concept (29 groups) | Primary Heating (20 groups) | Genuine morphological dimension |
| Remaining collisions | 1 pair | 1 pair (same pair) | Identical physics, different engineering |
| Block alignment | N/As scattered | N/As align with family boundaries | Clean hierarchical structure |

---

## 6. Conclusions

**Does decomposing Confinement Concept into semantically meaningful, family-specific columns reveal the context-dependence that the flat table hid?**

Yes. Three lines of evidence:

1. **The near-ID problem is eliminated.** The minimum discriminating set went from 2 to 4 columns, requiring information from multiple independent dimensions. No single column dominates.

2. **N/A density jumped from 9.6% to 36.7%**, and every N/A is structurally justified. The flat table hid context-dependence by cramming a hierarchical tree into a single column with 29 unique values. Decomposing it reveals that most questions only make sense within a specific branch.

3. **The granularity progression is monotonic.** N/A density grows from 10.5% (family only) to 27.7% (+ sub-types) to 36.7% (+ shape/type/approach). Each level of specificity introduces questions that apply to a narrower subset and are N/A for everything else. This is exactly the signature of a branching, context-dependent design space.

The morphological table is no longer a lookup keyed on a near-unique label. It's a structured comparison across genuine dimensions, with the N/A pattern itself carrying information about where the design space branches.
