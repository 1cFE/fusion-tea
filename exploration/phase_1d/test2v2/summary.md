## Test 2v2: Family-Conditional Generative Coherence

### Method

Sampling conditioned on Confinement Family (using `table_corrected.csv` with single Confinement Concept column). Non-confinement columns sampled from family-conditional vocabularies. Driver Technology excluded.

**Comparison**: Original test2 used unconditional sampling from `table_v2.csv` → 0/30 coherent (0%).

### Quantitative Results

| Metric | test2 (unconditional) | test2v2 (family-conditional) |
|--------|----------------------|------------------------------|
| Concepts assessed | 30 | 30 |
| Physically coherent | 0 (0%) | 7 (23%) |
| Engineering plausible | 0 (0%) | 5 (17%) |
| Exact matches | 0 | 0 |
| Novel coherent | 0 | 7 |

**Novelty distribution**: {"variant": 16, "novel": 12, "existing": 2}

### Coherence by Confinement Family

| Family | Generated | Coherent | Rate |
|--------|-----------|----------|------|
| Electrostatic | 1 | 0 | 0% |
| IFE | 10 | 2 | 20% |
| MFE | 11 | 2 | 18% |
| Other | 6 | 3 | 50% |
| MIF | 2 | 0 | 0% |

### Top Constraint Pairs (remaining failures)

| Column Pair | Failures | Example Reason |
|-------------|----------|----------------|
| Fuel × Neutron Management | 19 | p-B11 is nearly aneutronic; side-reaction neutron production is orders of magnit |
| Confinement Concept × Primary Heating | 13 | Projectile ICF uses kinetic impactor compression as its driver — the defining fe |
| Confinement Concept × Magnet Type | 9 | Polywells use magnetic coils (conventional or superconducting) arranged in a pol |
| Fuel × Tritium Breeding | 6 | D-T fuel requires a tritium breeding system (lithium blanket or equivalent) sinc |
| Confinement Concept × Fuel | 6 | p-B11 requires ~300 keV ignition temperatures and has a cross-section ~100x lowe |
| Energy Capture × Fuel | 6 | p-B11 fusion produces three alpha particles carrying most of the fusion energy a |
| Confinement Concept × Plasma State | 6 | Tokamak plasmas are magnetically confined in a toroidal equilibrium and achieve  |
| Confinement Concept × Repetition Rate | 4 | Tokamak plasma pulses last seconds to hours (or are steady-state). A 10 Hz repet |
| Confinement Concept × Operation Mode | 4 | Stellarators are inherently steady-state devices. The external coil geometry pro |
| Neutron Management × Tritium Breeding | 2 | The LiPb blanket already serves as the primary neutron management system in D-T  |

### Qualitative Synthesis

## Family-Conditional Coherence Analysis: Synthesis

### 1. Impact of Family-Conditional Sampling

The jump from **0/30 (0%)** to **7/30 (23.3%)** is significant but modest. It confirms that cross-family contamination was a real problem — IFE heating methods landing on MFE concepts, pinch plasma states on tokamaks, etc. Eliminating that source of incoherence recovered some valid combinations.

But 23% is not high. The delta tells us:

- **Cross-family coupling accounted for roughly a quarter of the failure budget.** Removing it bought ~7 coherent concepts out of 30.
- **The remaining ~77% of failures are within-family constraints.** The dominant coupling structure is not "MFE vs IFE" — it's "stellarator vs ohmic heating" or "D-T vs aneutronic shielding." These are concept-level and fuel-cascade constraints that family conditioning cannot resolve.

The implication is clear: **family is necessary but far from sufficient to determine valid combinations.** The design space is not "pick a family, then choose freely within it."

### 2. Within-Family Constraint Structure

**Families where within-family sampling works:**

- **Other (3/6 = 50%)**: All three coherent cases are Dense Plasma Focus. DPF is a tightly self-consistent concept — its fuel options (D-D, p-B11), heating (electromagnetic pinch), and plasma state are all internally determined. The "Other" family is small and heterogeneous, but DPF happens to have few cross-column dependencies beyond its own identity. Muon-catalyzed fusion (0/3) drags the family down — it's an extreme outlier with unique physics (no plasma, no heating, non-standard fuels) that makes random column assignment almost always wrong.

- **IFE (2/10 = 20%)**: Two coherent out of ten. IFE concepts are heavily coupled to their driver technology — laser direct drive, fast ignition, heavy ion, projectile impact are mutually exclusive heating methods. Family-conditional sampling still mixes these drivers freely.

- **MFE (2/11 = 18%)**: Two coherent. MFE has the deepest constraint structure: magnet topology is locked to concept (stellarator ≠ tokamak ≠ mirror ≠ dipole), operation mode is concept-determined (stellarator = steady-state, tokamak = pulsed or steady), and repetition rate is concept-class-determined (continuous, not Hz-scale).

- **MIF (0/2 = 0%)** and **Electrostatic (0/1 = 0%)**: Too few samples to draw conclusions, but both failures involved fuel-cascade errors (D-T with wrong tritium breeding/neutron management).

**The top constraint pairs confirm this:**

| Pair | Failures | Nature |
|------|----------|--------|
| Fuel × Neutron Management | 19 | Fuel cascade |
| Concept × Primary Heating | 13 | Concept-specific |
| Concept × Magnet Type | 9 | Concept-specific |
| Fuel × Tritium Breeding | 6 | Fuel cascade |
| Concept × Fuel | 6 | Concept feasibility |
| Energy Capture × Fuel | 6 | Fuel cascade |
| Concept × Plasma State | 6 | Concept-specific |

**Fuel × Neutron Management** dominates at 19 failures — this is the single biggest remaining coupling. It's a hard physical constraint: D-T produces 14.1 MeV neutrons requiring heavy shielding + breeding blanket; D-D produces 2.45 MeV neutrons; p-B11 is aneutronic. These are not independent columns.

### 3. Remaining Failure Patterns

Three distinct failure types persist, roughly in order of rigidity:

**Concept-specific constraints (hard physics):** The largest category. These are cases where the confinement concept mechanistically determines one or more other columns.

- Stellarator → no ohmic heating (zero plasma current by design)
- Stellarator → steady-state (not pulsed)
- Stellarator → non-planar or modular coils (not planar array, not levitated dipole)
- Tokamak → not self-pinch heating, not 10 Hz rep rate
- Levitated dipole → superconducting floating coil (not resistive)
- Z-pinch → self-confined (not stellarator coils)
- Laser ICF → laser driver (not projectile impact, not heavy ion beam)
- Muon catalysis → no plasma, no heating, hydrogen isotopes only

These are **definitional** — violating them changes what the concept *is*.

**Fuel-cascade constraints (hard physics):** The second largest category. Fuel choice creates a cascade through 3-4 downstream columns:

```
Fuel choice
├── Neutron Management (energy spectrum, flux level)
├── Tritium Breeding (required for D-T, N/A for others)
├── Energy Capture (charged particle fraction determines optimal method)
└── Shielding mass/complexity
```

D-T, D-D, D-He3, and p-B11 each impose a distinct downstream signature. These four columns are not four degrees of freedom — they are one degree of freedom (fuel) with three dependent consequences.

**Soft engineering preferences (debatable):** A minority. Cases like:
- p-B11 with thermal steam conversion (physically possible, but defeats the purpose)
- Integrated blanket/shield on an aneutronic concept (works, but wasteful)
- NBI on a levitated dipole (risky due to orbit losses, but not impossible)

These appeared in ~3-4 assessments, usually as secondary complaints alongside hard failures. They represent genuine design-space ambiguity — reasonable engineers might disagree.

### 4. Independent vs. Coupled Dimensions (Within-Family)

Within each family, the effective degrees of freedom are far fewer than the column count suggests.

**MFE (~11 columns sampled → ~2-3 genuine DOF):**

| Column | Status |
|--------|--------|
| Confinement Concept | Free choice (within MFE) |
| Primary Heating | **Locked to concept** |
| Magnet Type | **Locked to concept** |
| Operation Mode | **Locked to concept** (stellarator=SS, tokamak=pulsed/SS) |
| Repetition Rate | **Locked to concept** (continuous for all MFE) |
| Plasma State | **Locked to concept** |
| Fuel | Semi-free (concept constrains feasible fuels, but 2-3 options exist) |
| Neutron Management | **Locked to fuel** |
| Tritium Breeding | **Locked to fuel** |
| Energy Capture | **Locked to fuel** |

Effective DOF: **Concept** (free) + **Fuel** (semi-free) ≈ **2**. Everything else is determined.

**IFE (~11 columns → ~2-3 DOF):**

Concept determines driver/heating. Fuel determines neutron/breeding/capture chain. Rep rate is somewhat free (1-10 Hz range). Similar structure to MFE: ~2-3 DOF.

**Other:** Too heterogeneous to characterize as a family. Each concept (DPF, muon catalysis, etc.) is essentially its own island with 1-2 DOF.

**MIF:** Small sample, but same pattern — concept + fuel determine nearly everything.

### 5. Novel Coherent Concepts

Seven coherent concepts emerged. Examining them:

1. **#3 — Laser ICF (direct drive) / D-D / ultrashort pulse / hybrid capture**: Labeled coherent with a minor tension (ultrashort pulse is atypical for direct drive). This is a **plausible variant** — direct-drive fast ignition with D-D fuel. Genuinely interesting as a concept not well-represented in the literature, though the D-D energy balance would be challenging.

2. **#6 — Stellarator (modular) / D-D / ICRH / thermal**: A straightforward D-D stellarator. The only flag was overspecified neutron shielding. This is a **trivial variation** of W7-X-class reactor studies with a fuel swap.

3. **#8 — Dense plasma focus / D-D / EM pinch / thermal**: Essentially LPPFusion with D-D instead of p-B11. **Trivial variation.**

4. **#25 — Dense plasma focus / p-B11 / EM pinch / thermal**: This IS LPPFusion's actual concept. **Not novel at all** (labeled "variant" but is essentially existing).

5. **#26 — Laser ICF (fast ignition) / D-T / direct drive / hybrid capture**: HiPER-like. **Known concept**, well-studied in EU fusion roadmaps.

6. **#27 — Levitated dipole (orbital) / p-B11 / NBI / direct conversion**: Interesting — an orbital dipole with aneutronic fuel. The NBI concern is real but the concept is a **genuinely interesting variant** of Kesner-Mauel proposals. One of the few cases where random sampling found something worth thinking about.

7. **#30 — Dense plasma focus / D-D / EM pinch / thermal**: Duplicate of #8.

**Verdict on novelty:** 3 DPF near-duplicates, 2 known concepts (fast ignition, DPF p-B11), 1 trivial fuel swap (D-D stellarator), and 1 genuinely interesting variant (orbital dipole). The hit rate for *interesting* novel concepts is roughly **1/30 (3%)**. Family-conditional sampling is not an effective concept generator.

### 6. Revised Verdict

**The table is a classification scheme, not a design space.**

The evidence is now quite strong:

- **Unconditional sampling: 0% coherence.** Cross-family constraints dominate.
- **Family-conditional sampling: 23% coherence.** Within-family constraints dominate what remains.
- **The 23% that passed are mostly trivial variations** of known concepts (DPF × {D-D, p-B11}, known fast ignition, known stellarator).

The table has approximately **2 genuine degrees of freedom**: confinement concept and fuel cycle. Everything else is either determined by concept identity (heating, magnets, operation mode, rep rate, plasma state) or determined by fuel choice (neutron management, tritium breeding, energy capture). These two choices interact (not all fuels work with all concepts), further reducing the combinatorial space.

**Structural assessment:**

```
Family (MFE/IFE/MIF/Other)          ← Classification (rigid)
  └── Confinement Concept            ← Classification (rigid, ~19 values)
        ├── Heating                   ← Determined by concept
        ├── Magnet Type               ← Determined by concept  
        ├── Operation Mode            ← Determined by concept
        ├── Rep Rate                  ← Determined by concept
        ├── Plasma State              ← Determined by concept
        └── Fuel                      ← Semi-free choice (~2-4 options per concept)
              ├── Neutron Management   ← Determined by fuel
              ├── Tritium Breeding     ← Determined by fuel
              └── Energy Capture       ← Determined by fuel
```

This is a **tree**, not a grid. The table's flat structure (N independent columns) misrepresents what is actually a hierarchical dependency graph with ~2 branch points.

**Implications for AND/OR graph / pattern card design:**

1. **The AND/OR graph should encode the tree structure explicitly.** Concept → {determined columns} as a bundle, not as independent choices.

2. **Pattern cards should be concept-centric**, not column-centric. A "Stellarator" pattern card includes its heating options, magnet topology, and operation mode as fixed or narrowly constrained attributes — not as free parameters to be composed.

3. **Fuel is the only real cross-cutting design choice.** It should be modeled as an orthogonal axis that interacts with concept feasibility (some concept×fuel pairs are infeasible) and determines a downstream bundle (neutron management, breeding, capture).

4. **The effective design space is ~19 concepts × ~3 fuel options ≈ 57 cells**, minus infeasible pairs (p-B11 on most ICF, muon catalysis with non-hydrogen fuels, etc.), yielding perhaps **30-40 physically coherent combinations**. This is a lookup table, not a combinatorial space. The AND/OR graph's job is to encode these valid combinations and their cost-model implications, not to enable generative exploration.

