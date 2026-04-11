## Test 2 & 3: Generative Coherence + Constraint Density

### Quantitative Results

| Metric | Value |
|--------|-------|
| Concepts assessed | 30 |
| Physically coherent | 0 (0%) |
| Engineering plausible | 0 (0%) |
| Errored assessments | 0 |

**Novelty distribution**: {"novel": 29, "variant": 1}

### Coherence by Confinement Family

| Family | Generated | Coherent | Rate |
|--------|-----------|----------|------|
| IFE | 11 | 0 | 0% |
| Non-Standard | 6 | 0 | 0% |
| MIF | 6 | 0 | 0% |
| MFE | 7 | 0 | 0% |

### Top Constraint Pairs

| Column Pair | Failures | Example Reason |
|-------------|----------|----------------|
| Fuel × Neutron Management | 20 | D-T fusion produces abundant 14.1 MeV neutrons (~80% of energy output). 'Reduced |
| Driver Technology × IFE Driver | 11 | An HTS dipole coil is a magnetic confinement device, not an acoustic driver. Aco |
| Driver Technology × Magnet Type | 8 | Self-confined means the plasma's own currents provide confinement with no extern |
| IFE Driver × Primary Heating | 7 | An acoustic-driven IFE concept derives its target compression and heating from a |
| Confinement Family × Primary Heating | 7 | Heavy ion beams are IFE drivers designed to deposit energy in small inertial tar |
| Confinement Family × Plasma State | 6 | IFE operates via discrete micro-explosions — the plasma exists only transiently  |
| Non-Standard Mechanism × Primary Heating | 6 | Electrostatic confinement uses electric fields to confine and accelerate ions. M |
| Magnet Type × Non-Standard Mechanism | 5 | A levitated HTS dipole coil implies dipole magnetic confinement (like MIT's LDX) |
| Operation Mode × Primary Heating | 5 | Magnetic compression heating requires cyclic ramp-up of fields, which is fundame |
| Confinement Family × Operation Mode | 5 | IFE is inherently pulsed — targets are compressed, burn for nanoseconds to micro |

### Qualitative Synthesis

## Qualitative Synthesis: Fusion Concept Morphological Table Coherence Test

### 1. Constraint Density Matrix

Pairs with observed coupling, grouped by strength. Based on failure frequency across 30 random concepts and the physics severity of the constraints.

**Strong coupling** (most value combinations forbidden — these columns are essentially correlated):

| Column A | Column B | Failures | Nature |
|---|---|---|---|
| Fuel | Neutron Management | 20/30 | Each fuel has a specific neutron spectrum; management must match |
| Driver Technology | IFE Driver | 11/30 | Driver hardware must implement the stated driver mechanism |
| Driver Technology | Magnet Type | 8/30 | Hardware must be consistent with stated magnet category |
| Confinement Family | Primary Heating | 7/30 | MFE/IFE/MIF each admit different heating physics |
| Confinement Family | Plasma State | 6/30 | IFE→transient/compressed, MFE→sustained/burning, MIF→compressed |
| Confinement Family | Operation Mode | 5/30 | IFE→pulsed, MFE→steady/quasi-steady, MIF→pulsed |
| IFE Driver | Primary Heating | 7/30 | The driver *is* the heating mechanism in IFE |
| Non-Standard Mechanism | Primary Heating | 6/30 | Each mechanism implies its own heating physics |
| Magnet Type | Non-Standard Mechanism | 5/30 | Electrostatic/plasma-focus don't use external magnets |
| Operation Mode | Primary Heating | 5/30 | Pulsed heating → pulsed operation; continuous heating → steady-state |
| Operation Mode | Plasma State | ~5 | Steady-state↔sustained; pulsed↔transient/compressed |

**Moderate coupling** (some combinations forbidden):

| Column A | Column B | Nature |
|---|---|---|
| Fuel | Energy Capture | D-He3/p-B11 strongly prefer direct conversion; D-T needs thermal |
| Fuel | Tritium Breeding | D-T requires blanket breeding; D-D/D-He3/p-B11 don't |
| MFE Topology | Driver Technology | Mirror coils ≠ stellarator coils ≠ tokamak coils |
| MFE Topology | Magnet Type | Topology constrains coil geometry and type |
| MIF Method | Operation Mode | All MIF methods are pulsed |
| MIF Method | Driver Technology | Each MIF method requires specific compression hardware |
| Confinement Family | Repetition Rate | IFE/MIF require rep rate; MFE typically N/A |
| Fuel | MFE Topology | p-B11 requires extreme confinement quality, eliminating mirrors |

**Weak coupling** (edge cases, soft constraints):

| Column A | Column B | Nature |
|---|---|---|
| Fuel | Laser Approach | D-He3/p-B11 ignition via laser is implausible but not forbidden |
| Energy Capture | Magnet Type | Inductive capture needs magnetic flux; minor constraint |
| Neutron Management | Tritium Breeding | Breeding blankets need neutrons; reduced management conflicts |

### 2. Independent vs. Coupled Dimensions

**Genuinely independent dimensions** (can be varied freely without breaking coherence):

Almost none. The only candidates for near-independence are:

- **Scale/Power level** (if it were a column) — largely decoupled from physics choices
- **Repetition Rate** *within* a family — once you know it's pulsed IFE, the exact Hz is a free parameter
- **Specific material choices** within a magnet type — REBCO vs YBCO vs Bi-2212 are interchangeable

**Tightly coupled clusters** (must be selected together):

1. **Confinement-Heating-Plasma cluster**: Confinement Family ↔ Primary Heating ↔ Plasma State ↔ Operation Mode. These four columns are so tightly correlated that selecting one constrains the others to a small set. IFE forces pulsed/transient/driver-is-heater. MFE forces sustained/steady-state/RF-or-NBI. MIF forces pulsed/compressed/compression-heating.

2. **Fuel-Neutron-Energy cluster**: Fuel ↔ Neutron Management ↔ Tritium Breeding ↔ Energy Capture. The fuel choice cascades deterministically: D-T → heavy shielding + breeding blanket + thermal capture. p-B11 → minimal shielding + no breeding + direct conversion. These aren't independent design choices; they're consequences of the fuel selection.

3. **Driver-Hardware cluster**: Driver Technology ↔ Magnet Type ↔ IFE Driver (or MIF Method or Non-Standard Mechanism). The hardware must implement the stated mechanism. A "laser driver" column paired with "HTS stellarator coils" hardware is nonsensical. These columns describe the same physical system at different abstraction levels.

4. **Topology-Magnet cluster** (MFE only): MFE Topology ↔ Magnet Type ↔ Driver Technology. Tokamak/stellarator/mirror each require specific coil geometries.

**Bottom line**: Of the ~15+ columns in the table, there are roughly **3-4 independent choice dimensions**, not 15+. The columns encode correlated observations of a few underlying decisions.

### 3. Failure Pattern Analysis

Dominant failure types, in order:

**Physics incompatibilities dominate (~60% of failures).** These are hard constraints where the values cannot coexist:
- IFE + sustained plasma (inertial confinement is transient by definition)
- Electrostatic mechanism + magnetic compression heating (different confinement universes)
- Muon catalysis + p-B11 (muons only catalyze light isotope fusion)
- D-T fuel + aneutronic neutron management (D-T *is* neutronic)
- Acoustic driver + laser heating (mutually exclusive energy delivery)

**Engineering mismatches are second (~25%).** The values describe hardware from incompatible paradigms:
- Stellarator coils in a mirror machine
- NBI heating for an IFE target (no plasma to inject into)
- HTS dipole coil as an acoustic driver
- Projectile impact heating in a tokamak

**Coherence gaps are rare (~15%).** These are "soft" failures where the combination is purposeless rather than forbidden:
- D-He3 fuel + thermal steam capture (works but defeats the purpose of choosing D-He3)
- p-B11 + integrated blanket/shield (works but massively over-engineered)
- D-D burning plasma (not forbidden, but no device can achieve it)

The dominance of hard physics incompatibilities — not edge-case engineering concerns — confirms that the columns encode deeply correlated physical parameters, not independent design choices.

### 4. Novel Coherent Concepts

**None.** Zero of 30 random concepts achieved coherence. The single "variant" (#1, which was still incoherent) simply happened to sample values close to an existing concept but still drew incompatible combinations.

There are no novel coherent concepts to evaluate. This is itself the most important finding: the design space is so constrained that random sampling across the full vocabulary *never* produces a viable concept. The probability of randomly generating a coherent concept from this table is effectively zero.

### 5. Verdict

**This is a classification scheme, not a design space.**

The evidence is unambiguous:

| Indicator | Design Space | Classification Scheme | This Table |
|---|---|---|---|
| Coherence rate | >50% | <20% | **0%** |
| Independent dimensions | Most columns independent | Most columns coupled | **3-4 of ~15+** |
| Failure mode | Engineering trade-offs | Physics impossibilities | **Hard physics** |
| Random generation | Usually viable concepts | Usually nonsense | **Always nonsense** |

The morphological table captures **how existing concepts are described** — their observable properties — not **what design choices are available**. The columns are correlated observations of a few deep choices (confinement approach, fuel, scale), not independent knobs that can be turned freely.

**Implications for richer representation:**

1. **AND/OR graph is the right next step.** The table should be restructured as a hierarchical decision tree where selecting a confinement family immediately constrains heating, plasma state, operation mode, and driver type. Each branch point narrows the remaining choices — this is AND/OR structure, not a flat Cartesian product.

2. **Pattern cards per archetype.** The real design space has ~5-8 archetypes (tokamak, stellarator, mirror, laser-IFE, heavy-ion IFE, magnetized-target MIF, Z-pinch, electrostatic), each with a small number of genuine free parameters (scale, specific materials, fuel within a feasible subset, engineering trade-offs). Pattern cards should capture each archetype's *fixed* choices and *free* parameters.

3. **The Cartesian product is misleading.** The current table implies a combinatorial space of thousands of concepts. The actual viable space contains ~36 known concepts and perhaps a few dozen plausible undiscovered variants. The table's apparent dimensionality vastly overstates the true degrees of freedom. Any generative use of this table needs pre-filtered compatibility constraints — or better, replacement with a structure that makes the constraints explicit.

