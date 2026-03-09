# Test 4 Rubric — Ground Truth & Scoring

**Purpose**: Score blind assessments against known ground truth. This file is NOT shown to the assessor.

## Scoring Scale (per dimension, per concept)

- **0**: Cannot determine — answer is absent, wrong, or too vague to be useful
- **1**: Partial — correct general direction but missing the specific claim or mechanism
- **2**: Full — articulates the specific thesis/challenge/logic accurately

**Dimensions**: Thesis (T), Hard Problems (HP), Design Logic (DL), Differentiation (D)
**Max per concept**: 8. **Max total**: 40.

---

## Concept A: Type One Energy — QI Modular HTS Stellarator "Infinity Two"

**Row** (Driver Technology withheld: "Modular HTS stellarator coils (REBCO, 9 T)"):
- MFE / Stellarator / Modular / D-T / RF (ECRH) / Thermal (steam) / Burning / HTS (3D stellarator) / Solid ceramic breeder (HCPB) / Integrated blanket/shield / Steady-state

### Ground Truth

**Thesis**: Modular-coil stellarator for manufacturability. The modularity is the key innovation — factory-fabricable coil modules that can be transported and assembled on site, with individual modules replaceable for maintenance. QI optimization gives good confinement. Steady-state avoids tokamak disruptions entirely. HCPB breeder is compatible with the modular maintenance concept (solid, removable segments).

**Hard Problems**:
1. Achieving adequate QI field optimization with modular (non-continuous) coils — fewer shaping degrees of freedom than continuous 3D wound or helical coils
2. First-wall and blanket integration in complex 3D stellarator geometry — access, replacement, neutron streaming through gaps
3. Demonstrating Q > 1 in a stellarator (no stellarator has achieved burning plasma; W7-X is closest)

**Design Logic**: Stellarator → inherently steady-state, no disruption risk, no current drive power needed. D-T → proven fuel, lower temperature requirement. HTS 3D coils → compact machine, but modular approach trades peak field for manufacturing. ECRH → standard stellarator heating (good coupling to electron species in stellarator geometry). HCPB → solid breeder compatible with modular blanket segments (easier to replace than liquid systems in 3D geometry).

**Differentiation vs. other stellarators (Proxima QI, Thea planar, Gauss large-scale, Renaissance liquid-wall, Helical Fusion helical)**:
- Modularity for manufacturing and maintenance (vs. Proxima's continuous 3D coils which optimize field but are harder to manufacture)
- HCPB solid breeder (vs. LiPb or liquid metal wall used by others)
- Mid-field (9 T) vs. higher fields claimed by others

### Scoring Guide

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Thesis** | "A stellarator" | "Steady-state D-T stellarator with HTS, avoiding disruptions" | Identifies modularity as the core differentiator — manufacturing, maintenance access, factory fabrication |
| **Hard Problems** | Generic "stellarator challenges" | Names confinement optimization or blanket integration | Names the specific modular-coil optimization trade-off (fewer shaping DOF) AND blanket integration in 3D |
| **Design Logic** | Lists choices without connecting them | Connects stellarator → steady-state, D-T → breeding | Connects modular coils → HCPB (solid breeder fits modular maintenance), and explains the ECRH choice for stellarator geometry |
| **Differentiation** | Can't distinguish from other stellarators | Notes coil type differs | Identifies modularity as the distinguishing strategy vs. continuous-coil or planar-coil stellarators |

---

## Concept B: TAE Technologies — p-B11 FRC

**Row** (Driver Technology withheld: "Neutral beam injection (high-energy, tangential)"):
- MFE / Compact Toroid / p-B11 / NBI / Thermal (steam) / Sustained / Resistive / N/A (Tritium Breeding) / Minimal (aneutronic) / Steady-state

### Ground Truth

**Thesis**: Aneutronic fusion via p-B11 eliminates the entire tritium fuel cycle and neutron damage problem. FRC (field-reversed configuration, a type of compact toroid) sustained by neutral beam injection provides the high-β, compact confinement needed. Accepts extreme temperature requirements (~300 keV ion temperature, ~10× D-T) as the price for eliminating neutrons. Near-term stepping stones through D-T/D-He3 on the roadmap to p-B11.

**Hard Problems**:
1. p-B11 requires ion temperatures of ~300 keV (3+ billion degrees), roughly 10× higher than D-T — no device has come close
2. p-B11 reactivity is ~100× lower than D-T — requires extreme confinement quality (nτT product)
3. Bremsstrahlung radiation losses at high-Z boron and extreme temperatures may prevent net energy gain (the "radiation barrier")
4. FRC stability at the required temperatures — current experimental record (~100M degrees in C-2W) is still far from p-B11 requirements

**Design Logic**: p-B11 → no tritium breeding needed, minimal neutron management. Compact Toroid (FRC) → high-β plasma (β ~ 1), no toroidal field coils, simple geometry. NBI → sustains FRC against decay (beam-driven current maintains field reversal). Resistive magnets → adequate for FRC external mirror fields (don't need SC for primary confinement since β ~ 1). Sustained plasma state → NBI maintains the FRC continuously.

**Notable**: Energy Capture = Thermal (steam) is surprising for p-B11. The standard argument for p-B11 is that charged-particle products enable direct energy conversion. Thermal capture for p-B11 suggests either (a) near-term D-T stepping stone economics, (b) the table is wrong, or (c) the concept plans thermal conversion even for aneutronic products (possible but defeats a key advantage).

**Differentiation vs. other MFE concepts**: Only major company pursuing p-B11 as primary fuel. FRC (compact toroid) is unique topology — most MFE is tokamak or stellarator. NBI-sustained FRC is a unique operational approach.

### Scoring Guide

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Thesis** | "Some kind of MFE" | "Aneutronic approach using p-B11 to avoid neutrons" | Articulates the specific bet: FRC + NBI sustains plasma at extreme temperatures required for p-B11, trading temperature difficulty for eliminating the entire neutron/tritium engineering problem |
| **Hard Problems** | Generic "needs high temperature" | Names the temperature or reactivity challenge | Names the radiation barrier (bremsstrahlung at high-Z boron), the 100× reactivity gap, AND the FRC stability challenge |
| **Design Logic** | Lists choices | Connects p-B11 → no breeding, aneutronic | Connects the full chain: p-B11 → no breeding → no blanket → simpler reactor, FRC → high-β → minimal external field → resistive magnets adequate, NBI → FRC sustainment. Notes the Thermal (steam) anomaly |
| **Differentiation** | "Different fuel" | "Only p-B11 MFE concept" | Identifies both the fuel uniqueness AND the FRC + NBI sustainment as the differentiating approach |

---

## Concept C: Xcimer Energy — Laser ICF, Hybrid Direct Drive

**Row** (Driver Technology withheld: "Excimer laser (KrF, 248 nm, 10+ MJ, ASPEN architecture)"):
- IFE / Laser / Hybrid drive / D-T / Laser (direct drive) / Thermal (unspecified) / Compressed / N/A (Magnet Type) / FLiBe blanket / Integrated blanket/shield / Pulsed / Sub-Hz

### Ground Truth

**Thesis**: KrF excimer laser provides a fundamentally cheaper cost-per-joule than solid-state lasers (DPSSL), enabling the 10+ MJ pulse energies needed for high-gain ICF at manageable cost. Hybrid direct drive (combination of direct illumination and indirect X-ray conversion in the same geometry) improves symmetry and coupling efficiency vs. pure direct or indirect drive. The ASPEN architecture (single-pass amplifier, no optical cavity) is the key innovation.

**Hard Problems**:
1. KrF excimer laser repetition rate — historically limited to low rep rates; Sub-Hz is acknowledged in the table
2. Target fabrication and injection at scale — precision D-T capsules at the required quality and rate
3. Chamber environment — surviving repeated micro-explosions, debris clearing, optical path maintenance
4. Laser efficiency — KrF wall-plug efficiency (~5-7% historically) is lower than DPSSL (~10-15%)

**Design Logic**: Laser IFE → pulsed, compressed plasma, no magnets. Hybrid drive → better symmetry than pure direct drive, don't need hohlraum (indirect drive) engineering. D-T → standard fuel, proven ignition physics (NIF). FLiBe blanket → neutron capture + tritium breeding + heat transfer in single fluid. Sub-Hz rep rate → reflects KrF laser limitation (not a choice, a constraint).

**Differentiation vs. other laser IFE (Focused Energy fast ignition, BLF direct drive, GenF direct drive, Inertia Enterprises indirect drive)**:
- Laser type: KrF excimer vs. DPSSL (everyone else)
- Drive scheme: Hybrid direct drive is unique to Xcimer
- Pulse energy: 10+ MJ (highest claimed) enabled by cheaper KrF joules
- Rep rate: Sub-Hz is lowest — a weakness, not a strength

### Scoring Guide

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Thesis** | "Laser fusion" | "Hybrid drive approach for better coupling" | Identifies that the driver technology (not shown) must be non-standard (Sub-Hz constraint suggests a laser type with rep-rate limitations), and that hybrid drive is the distinguishing coupling scheme |
| **Hard Problems** | Generic "target fabrication" | Names rep rate or chamber issues | Names rep rate as a binding constraint (Sub-Hz), target fab, AND chamber survivability |
| **Design Logic** | Lists choices | Connects laser → pulsed → compressed | Connects hybrid drive choice to coupling/symmetry advantages, FLiBe to multi-function (breed + shield + cool), and notes Sub-Hz as a constraint rather than a design choice |
| **Differentiation** | "A laser IFE concept" | "Uses hybrid drive, which is unusual" | Identifies hybrid drive as unique AND notes the Sub-Hz weakness relative to ~10 Hz competitors |

---

## Concept D: General Fusion — Magnetized Target Fusion, Pneumatic Compression

**Row** (Driver Technology withheld: "Pneumatic pistons + liquid metal"):
- MIF / Magnetized target / D-T / Mechanical compression / Thermal (steam) / Compressed / Self-confined / Liquid metal wall / Integrated blanket/shield / Pulsed / ~1 Hz

### Ground Truth

**Thesis**: Mechanical compression of a magnetized plasma inside a liquid metal vortex achieves fusion conditions without expensive superconducting magnets or high-energy lasers. The liquid metal serves simultaneously as compression medium, first wall, tritium breeding blanket, neutron shield, and heat transfer fluid. By using cheap, replaceable mechanical hardware (pneumatic pistons), the concept avoids the most expensive components of both MFE and IFE approaches.

**Hard Problems**:
1. Compression symmetry — dozens of pneumatic pistons must synchronize to microsecond precision to achieve uniform implosion
2. Liquid metal vortex formation and stability — maintaining a stable cavity in swirling liquid metal for plasma injection
3. Plasma lifetime — the magnetized target plasma (FRC or CT) must survive long enough (~milliseconds) to be compressed before it decays
4. Rep rate at ~1 Hz — reforming the vortex and re-injecting plasma between shots

**Design Logic**: Magnetized target → pre-magnetizing the plasma reduces the compression ratio needed (vs. unmagnetized ICF). Mechanical compression → cheapest possible driver (pistons are commodity hardware). Self-confined → plasma's own magnetic field provides confinement during compression, no external SC magnets. Liquid metal wall → multi-function: breeding (lithium), shielding (high-Z metal), first wall (renewable surface), coolant (pumped loop). Thermal (steam) → liquid metal transfers heat to steam cycle.

**Differentiation vs. Pacific Fusion (MagLIF-style pulsed power MIF)**:
- Compression driver: mechanical (pistons) vs. electromagnetic (pulsed power)
- Wall: liquid metal (renewable, multi-function) vs. solid (needs replacement)
- Hardware cost: pistons are cheap, pulsed power capacitor banks are expensive
- Rep rate: ~1 Hz achievable with mechanical systems; pulsed power MIF is Sub-Hz

### Scoring Guide

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Thesis** | "MIF concept" | "Magnetized target compressed mechanically — avoids expensive magnets/lasers" | Identifies the multi-function liquid metal wall as the second key innovation (not just compression, but breeding + shielding + first wall in one medium) |
| **Hard Problems** | Generic "compression challenges" | Names compression symmetry or plasma lifetime | Names synchronization precision of mechanical compression AND liquid metal vortex stability |
| **Design Logic** | Lists choices | Connects magnetized target → lower compression ratio | Connects the full chain: mechanical → cheap hardware, liquid metal → multi-function (breed + shield + cool + renewable wall), self-confined → no external magnets needed during compression |
| **Differentiation** | "A MIF concept" | "Uses mechanical compression, which is unusual" | Identifies mechanical compression + liquid metal wall as the paired differentiators vs. electromagnetic MIF |

---

## Concept E: LPPFusion — Dense Plasma Focus, p-B11

**Row** (Driver Technology withheld: "Pulsed coaxial electrodes (capacitor bank, 2.7 MA)"):
- Non-Standard / Plasma focus / p-B11 / Electromagnetic pinch (DPF) / Direct (charged particle) / Pinch / Self-confined / N/A (Tritium Breeding) / Minimal (aneutronic) / Pulsed / High (>10 Hz)

### Ground Truth

**Thesis**: Dense plasma focus (DPF) can achieve the extreme densities and temperatures needed for p-B11 fusion in an extraordinarily simple, cheap device — just coaxial electrodes and a capacitor bank. Combined with p-B11's aneutronic products, this enables direct energy conversion of alpha particles without breeding blankets, neutron shielding, or superconducting magnets. The concept bets on extreme simplicity: if DPF physics works at the required scale, the reactor is orders of magnitude cheaper than any other approach.

**Hard Problems**:
1. DPF scaling — no DPF has achieved net energy gain; the physics of pinch formation at higher energies is poorly understood and may not scale favorably
2. p-B11 conditions in DPF — achieving the required >300 keV ion temperatures and sufficient confinement time in a transient pinch is undemonstrated
3. Pinch instabilities — Rayleigh-Taylor, sausage, and kink instabilities limit achievable compression and confinement time
4. Electrode erosion — at >10 Hz rep rate, electrode lifetime becomes a critical engineering constraint
5. Scientific credibility — DPF fusion is far outside the mainstream research consensus; many physicists doubt it can achieve net energy at any scale

**Design Logic**: Plasma focus → extreme density/temperature in a transient pinch (10^26 /m³, kT magnetic fields). p-B11 → aneutronic, all energy in charged alphas. Direct (charged particle) → capture alphas electrostatically or inductively. Self-confined → pinch provides own confinement via J×B forces. High rep rate → compensate for small energy per pulse (μJ to mJ per shot) — need many shots per second for power output. Pulsed → inherent to DPF operation.

**Differentiation vs. Avalanche/Polywell (other Non-Standard)**:
- DPF is fundamentally different from electrostatic (Polywell/Avalanche) — uses electromagnetic pinch, not potential wells
- p-B11 fuel (vs. D-T for Avalanche/Polywell)
- Direct conversion (vs. thermal for electrostatic concepts)
- Extreme simplicity and low hardware cost — DPF is the cheapest conceivable fusion device

### Scoring Guide

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Thesis** | "Some exotic fusion concept" | "Aneutronic DPF — trying to use pinch for p-B11 with direct conversion" | Articulates the extreme-simplicity thesis: DPF is the cheapest possible device, and p-B11 eliminates blanket/shielding/tritium, so IF the physics works, this is orders of magnitude cheaper than anything else |
| **Hard Problems** | Generic "needs to prove physics" | Names DPF scaling or instabilities | Names DPF scaling uncertainty, pinch instability limits, AND the rep-rate electrode erosion problem |
| **Design Logic** | Lists choices | Connects p-B11 → aneutronic → direct conversion | Connects the full chain: DPF → extreme conditions cheaply, p-B11 → no blanket/shielding, direct conversion → no thermal cycle, high rep rate → compensates for tiny energy per pulse |
| **Differentiation** | "Non-standard concept" | "Uses plasma focus, different from electrostatic" | Identifies DPF's extreme simplicity/cost as the differentiator and explains how it differs from electrostatic Non-Standard approaches |

---

## Scoring Summary Template

| Concept | Thesis (0-2) | Hard Problems (0-2) | Design Logic (0-2) | Differentiation (0-2) | Total |
|---------|:---:|:---:|:---:|:---:|:---:|
| A: Stellarator | | | | | /8 |
| B: p-B11 FRC | | | | | /8 |
| C: Hybrid Laser ICF | | | | | /8 |
| D: Pneumatic MIF | | | | | /8 |
| E: DPF p-B11 | | | | | /8 |
| **Total** | | | | | **/40** |

## Execution

```bash
# Run each concept as a separate blind assessment
# Template: exploration/phase_1d/test4-prompt.md
# Replace {{CONCEPT_LETTER}} with A-E, {{ROW_DATA}} with the stripped row

# Concept A
claude -p < <(sed 's/{{CONCEPT_LETTER}}/A/' exploration/phase_1d/test4-prompt.md | sed 's/{{ROW_DATA}}/.../')

# Or manually construct prompts and pipe them
```

After all 5 responses are collected, score each against this rubric and compile into the Test 4 section of the Phase 1d report.
