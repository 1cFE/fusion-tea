# Modularity Score Matrix

This matrix scores 39 fusion concepts on a "Manufacturability & Scale-Out" (M&SO) axis from 1 (least modular) to 5 (most modular). The score answers: *how much of this concept's commercial plant can be factory-built and replicated, vs. stick-built on-site as a one-of-a-kind megaproject?*

A score of 5 means SMR-like factory production. A score of 1 means ITER-like bespoke construction.

## What the score is made of

Each concept's M&SO score is a weighted sum of three components:

```
M&SO  =  0.50 × min_viable_device_scale          ("how small can a viable plant be?")
       + 0.25 × percent_mod                       ("how modular are the three big subsystems?")
       + 0.25 × unit_multiplicity                 ("how many factory-built units per plant?")
```

Each component is also on a 1–5 scale, so the overall score stays bounded between 1 and 5.

**1. Minimum viable device scale (mvs).** How small can the smallest commercially viable plant be? Concepts with hard scale floors (ITER-class tokamaks, large industrial accelerators) score low. Concepts that can be deployed at small scale (MIF pulsed devices, desktop electrostatic concepts, Magnetic mirror chains) score high.

**2. Percent modularized (percent_mod).** Of the three subsystems that fusion plants realistically *can* modularize — the **vessel**, the **magnet/driver**, and the **blanket** — how modular are they collectively? Each is rated 1–5 based on whether its design is bespoke (low) or factory-built and replaceable (high). The three are then combined using each family's capex shares (e.g., a tokamak's coils are ~55% of plant cost, so its magnet/driver rating dominates). The remaining four subsystems (power conversion, fuel cycle, auxiliaries, civil) are excluded because they're rarely modularized in any concept and dilute the signal.

**3. Unit multiplicity (um).** How many identical factory-built precision units does one plant contain? This rewards SMR-style replication. A DPSSL plant with 1000 beamlines, a MIF plant with 100 capacitor bricks, and a desktop fusion plant with 200 Orbitrons all score 5. A plant with a single bespoke driver (a heavy-ion accelerator, an ITER coil set, a continuous helical stellarator winding) scores 1.

The curve saturates at 50 units — beyond that, additional copies don't add modularity (and arguably add commissioning burden). Concepts with N=1 score 1; N=2 scores 2; N=5–10 scores 3; N=15–30 scores 4; N≥50 scores 5.

## How to read each cell

Cells use this format:

```
[Concept name] (ID): [score]   mvs=X + pmod=Y (v/md/bl) + um=Z (N=count)
[one-line explanation]
```

Where:
- **mvs** is the min-viable-scale rating (1–5)
- **pmod** is the percent_mod aggregate (1–5)
- **v/md/bl** are the three subsystem ratings making up pmod: vessel, magnet/driver, blanket
- **um** is the unit_multiplicity rating (1–5)
- **N** is the estimated factory-built unit count per plant

Example: *"CFS ARC: 3.71 mvs=3 + pmod=4.84 (4/5/5) + um=4 (N=18)"* means: ARC is compact enough to earn mvs=3, has highly modular vessel/coils/blanket (4/5/5 weighted to 4.84), and has 18 factory-built TF coil segments per plant (earning um=4).

Empty cells mean no concept in the current 39-concept registry occupies that confinement × fuel combination.

---

## Matrix

| Confinement \\ Fuel | **D-T** | **D-He³** | **p-B11** | **D-D** |
|---|---|---|---|---|
| **Tokamak** | **CFS ARC (01): 3.71** &nbsp;`mvs=3 + pmod=4.84 (4/5/5) + um=4 (N=18)`<br>*compact HTS + demountable + FLiBe*<br><br>**Tokamak Energy ST (22): 3.59** &nbsp;`mvs=3 + pmod=4.37 (4/5/4) + um=4 (N=14)`<br>*spherical HTS demountable; HCPB → bl=4*<br><br>**Energy Singularity (29): 3.50** &nbsp;`mvs=3 + pmod=4.00 (4/4/4) + um=4 (N=16)`<br>*integrated coils → md=4*<br><br>**Firefly NTT (30): 3.71** &nbsp;`mvs=3 + pmod=4.84 + um=4`<br>*identical to CFS — compact HTS + demountable + FLiBe (MANTA proxy)*<br><br>**Neo Fusion BEST (34): 1.91** &nbsp;`mvs=2 + pmod=2.62 (2/2/4) + um=1 (N=1)`<br>*LTS + non-compact + single bespoke coil set = bottom of matrix* | — | **ENN EHL-2 (39): 3.63** &nbsp;`mvs=3 + pmod=4.52 (4/5/5) + um=4 (N=14)`<br>*compact spherical HTS demountable + aneutronic* | — |
| **Stellarator** | **Thea planar (05): 3.11** &nbsp;`mvs=2 + pmod=3.44 (2/3/5) + um=5 (N=40)`<br>*FLiBe → bl=5; 40 planar coil segments*<br><br>**Proxima QI (09): 3.03** &nbsp;`mvs=2 + pmod=3.13 (2/3/4) + um=5 (N=50)`<br>*~50 non-planar coil segments*<br><br>**Gauss HELIAS (10): 3.03** &nbsp;`mvs=2 + pmod=3.13 + um=5`<br>*~40 non-planar coils (W7-X-like)*<br><br>**Type One Infinity (20): 3.03** &nbsp;`mvs=2 + pmod=3.13 + um=5`<br>*segmented HTS coils*<br><br>**Renaissance (21): 3.03** &nbsp;`mvs=2 + pmod=3.13 + um=5`<br>*segmented HTS; liquid Li wall*<br><br>**Helical Fusion (36): 2.03** &nbsp;`mvs=2 + pmod=3.13 + um=1 (N=1)`<br>***Significant drop:*** continuous helical winding → 1 unit = um=1 (no segments to replicate) | — | — | — |
| **FRC** | — | — | **TAE (18): 3.77** &nbsp;`mvs=4 + pmod=4.10 (3/5/5) + um=3 (N=8)`<br>*p-B11 aneutronic; ~8 NBI modules*<br>*(steady-state, not pulsed)* | — |
| **MIF / Pulsed compression** | **MagLIF (07): 4.93** &nbsp;`mvs=5 + pmod=4.74 (5/5/4) + um=5 (N≈100)`<br>***#3 in matrix.*** MIF mvs=5; demountable pulsed-power; 100+ Marx generator bricks<br><br>**General Fusion MTF (14): 4.88** &nbsp;`mvs=5 + pmod=4.52 + um=5 (N=60)`<br>*MIF + pneumatic compression + ~60 capacitor modules* | **Helion (08): 5.00** &nbsp;`mvs=5 + pmod=5.00 (5/5/5) + um=5 (N=75)`<br>***Top scorer.*** Reclassified MIF (capacitor compression of FRC); aneutronic + demountable HTS + ~75 capacitor modules | — | **NearStar MTIF (37): 5.00** &nbsp;`mvs=5 + pmod=5.00 + um=5 (N=100)`<br>***Top scorer.*** MIF + Pulsed EM + D-D + ~100 capacitor modules |
| **Mirror / Open-linear** | **Realta (11): 4.01** &nbsp;`mvs=4 + pmod=4.03 (3/5/4) + um=4 (N=12)`<br>*demountable HTS mirror cells; ~12 cells*<br><br>**Zap Z-pinch (15): 4.07** &nbsp;`mvs=4 + pmod=3.28 (3/3/4) + um=5 (N=50)`<br>*~50 capacitor modules; pulsed-power* | — | **Pale Blue (06): 4.08** &nbsp;`mvs=4 + pmod=4.33 (3/5/5) + um=4 (N=30)`<br>*aneutronic + open/linear + ~30 mirror cells* | — |
| **Levitated dipole** | **OpenStar (12): 2.68** &nbsp;`mvs=3 + pmod=3.73 (3/5/3) + um=1 (N=1)`<br>***Major drop:*** single levitated dipole coil = N=1 → um=1<br>*(architecture replaces 1 coil/year — annual swap, but only 1 coil per plant)* | **Zephyr orbital (19): 2.70** &nbsp;`mvs=3 + pmod=3.82 + um=1 (N=1)`<br>*same N=1 issue; aneutronic D-He3 boosts pmod* | — | **Polomac (35): 2.84** &nbsp;`mvs=3 + pmod=3.35 (3/3/5) + um=2 (N=4)`<br>*4 poloidal magnets; D-D fuel boosts pmod* |
| **ICF (laser)** | **Focused Energy (17): 4.36** &nbsp;`mvs=4 + pmod=4.43 (3/5/4) + um=5 (N=200)`<br>***Tied tier at 4.36:*** Focused, Inertia, Blue Laser, GenF all score identically (DPSSL D-T baseline)<br><br>**Inertia (31): 4.36** &nbsp;`mvs=4 + pmod=4.43 + um=5 (N=1000)`<br>*1000+ DPSSL beamlines (Thunderwall)*<br><br>**Blue Laser OEC (32): 4.36** &nbsp;`N=200`<br><br>**GenF French (33): 4.36** &nbsp;`N=200`<br><br>**Xcimer (27): 2.86** &nbsp;`mvs=3 + pmod=3.44 (3/3/5) + um=2 (N=4)`<br>*~4 large e-beam KrF tanks; FLiBe → bl=5* | — | **hb11 (04): 4.37** &nbsp;`mvs=4 + pmod=4.48 (3/5/5) + um=5 (N=500)`<br>*DPSSL p-B11 aneutronic; ~500 beamlines*<br><br>**Marvel (24): 4.37** &nbsp;`same rule path` | **Cortex (03): 4.41** &nbsp;`mvs=4 + pmod=4.62 (3/5/5) + um=5 (N=200)`<br>*DPSSL D-D; D-D triggers bl=5*<br><br>**Sonofusion (02): 4.59** &nbsp;`mvs=5 + pmod=3.35 (3/3/5) + um=5 (N=100)`<br>***Big lift:*** acoustic mvs=5 (desktop) + 100-unit array + D-D bl=5 |
| **ICF (non-laser)** | **First Light (23): 3.80** &nbsp;`mvs=3 + pmod=4.20 (3/5/4) + um=5 (N=50)`<br>*Pulsed EM driver md=5; 50 launcher modules*<br><br>**Intensity heavy-ion (26): 3.04** &nbsp;`mvs=4 + pmod=3.15 (3/3/4) + um=1 (N=1)`<br>*single accelerator → um=1 drags it down* | — | — | — |
| **Electrostatic / Exotic** | **Avalanche (13): 4.78** &nbsp;`mvs=5 + pmod=4.12 (3/5/4) + um=5 (N=200)`<br>***Big lift to #5:*** electrostatic mvs=5 + serial-product md=5 + ~200 desktop units<br><br>**Acceleron muon (16): 2.54** &nbsp;`mvs=3 + pmod=3.18 (3/3/4) + um=1 (N=1)`<br>*muon accelerator → mvs=3, single accelerator → um=1*<br><br>**EMC2 Polywell (28): 4.28** &nbsp;`mvs=5 + pmod=4.12 + um=3 (N=6)`<br>*Polywell mvs=5 + demountable md=5; only 6 grid units*<br><br>**SHINE accelerator (38): 2.54** &nbsp;`mvs=3 + pmod=3.18 + um=1 (N=1)`<br>*identical defaults to Acceleron* | — | **LPPFusion DPF (25): 3.59** &nbsp;`mvs=4 + pmod=3.35 + um=3 (N=8)`<br>*DPF mvs=4; aneutronic D-D fuel; 8 electrode units* | — |

---

## Top scorers ranked

| Rank | ID | Concept | M&SO | Notes |
|---|---|---|---|---|
| 1 | 08 | **Helion** | **5.00** | Reclassified MIF + aneutronic + 75 capacitor modules |
| 1 | 37 | **NearStar MTIF** | **5.00** | MIF + Pulsed EM + D-D + 100 modules |
| 3 | 07 | Pacific Fusion MagLIF | 4.93 | MIF + 100 Marx bricks; vessel=md=5 |
| 4 | 14 | General Fusion MTF | 4.88 | MIF + pneumatic + 60 modules |
| 5 | 13 | Avalanche electrostatic | 4.78 | Desktop Orbitron + 200 serial units |
| 6 | 02 | Sonofusion | 4.59 | Desktop acoustic + 100 units + D-D |
| 7 | 03 | Cortex liquid jet | 4.41 | DPSSL + D-D + 200 beamlines |
| 8 | 04 | hb11 fast ignition | 4.37 | DPSSL + p-B11 + 500 beamlines |
| 8 | 24 | Marvel nanostructured | 4.37 | same rule path |
| 10 | 17 | Focused Energy FI | 4.36 | DPSSL D-T baseline tier |
| 11 | 31 | Inertia indirect | 4.36 | same — 1000 beamlines hits curve plateau |
| 12 | 32 | Blue Laser OEC | 4.36 | same |
| 13 | 33 | GenF French | 4.36 | same |
| 14 | 28 | EMC2 Polywell | 4.28 | Polywell + demountable, only 6 units |
| 15 | 06 | Pale Blue centrifugal | 4.08 | aneutronic mirror + 30 cells |
| 16 | 15 | Zap Z-pinch | 4.07 | open/linear + 50 capacitor modules |
| 17 | 11 | Realta mirror | 4.01 | demountable + 12 cells |

## Patterns in the rankings

The scores cluster into four bands that map onto recognizable plant archetypes:

**Top tier (4.5–5.0)**: MIF concepts (Helion, NearStar, MagLIF, General Fusion) and desktop electrostatic concepts (Avalanche, Sonofusion). What they share: small min-viable plants, many factory-built precision units per plant, and modular vessel/driver hardware. These are the closest analogs to SMR-style fusion.

**Strong tier (4.0–4.5)**: ICF DPSSL concepts (Inertia, Focused, Cortex, hb11, Marvel, Blue Laser, GenF), aneutronic mirror concepts (Pale Blue), and pulsed-power concepts (Zap, Realta, Polywell, First Light). What they share: high unit multiplicity (DPSSL beamlines, mirror cells, capacitor modules), good modular driver hardware, but slightly larger min-viable plants than the top tier.

**Middle tier (3.0–4.0)**: Most tokamaks (CFS, Firefly NTT, Tokamak Energy ST, ENN, Energy Singularity), large stellarators, and TAE. What they share: 10–50 factory-built segments per plant (good but not maxed), modular HTS coils, but compactness penalties from min-viable scale.

**Lower tier (below 3.0)**: Conventional LTS tokamaks (Neo BEST), single-unit drivers (OpenStar, Zephyr, Acceleron, SHINE, Helical Fusion, Intensity), and excimer ICF (Xcimer). What they share: either large bespoke construction (LTS tokamak) or a single one-of-a-kind driver per plant (single dipole coil, single industrial accelerator, continuous helical winding).

## Notable distortions to consider

**Single-unit drivers score low.** Concepts that have one large bespoke driver per plant (OpenStar's levitated coil, Acceleron's muon accelerator, SHINE's proton accelerator, Helical Fusion's continuous winding, Intensity's heavy-ion accelerator, Neo BEST's LTS coils, Zephyr's dipole) all score around or below 3.0 because um=1.

For some of these (Neo BEST, Acceleron, SHINE) this seems correct — they're genuinely non-modular plant architectures. But for **OpenStar and Zephyr**, the N=1 framing arguably understates the modularity story. OpenStar's commercial pitch is "annual sacrificial section replacement" — they replace the coil every year. That's *temporal* multiplicity (1 coil/year × many years) rather than *spatial* multiplicity (many coils simultaneously). The framework currently doesn't reward this.

A future refinement might allow temporal replication (replaceable consumables) to count toward um. An ARC-class concept that swaps blanket modules every 2 years could be argued to have effective multiplicity > 1.

**The DPSSL tier compresses around 4.36.** Inertia at 1000 beamlines and Focused at 200 beamlines score identically because the curve saturates at N≥50. This is intentional (diminishing returns above 50 units) but means the framework can't differentiate Inertia's scale-out story from concepts with smaller beamline counts.

**Helion vs MagLIF.** Helion scores 5.00 vs MagLIF's 4.93. The 0.07 difference is from MagLIF's blanket rating (4 instead of 5 — HCPB pebble bed, not aneutronic-free). Helion's aneutronic fuel gives it the maximum blanket score, edging out MagLIF.

## Caveats on unit counts (N)

The N values for each concept are spec-author estimates. Some are well-supported (DPSSL beamline counts are published in literature; CFS ARC's 18 TF segments is in the design paper). Others are less certain:

- **Helion N=75** — based on commercial design disclosures of ~50-100 capacitor modules per machine. Could be 50 or 100.
- **Avalanche N=200** — based on their "desktop reactor" commercial deployment narrative; specific unit count not published.
- **MagLIF N=100** — based on Pacific Fusion's Marx generator brick count for the commercial design.
- **Polywell N=6** — six magnetic cusps form the standard Polywell geometry; not really "modular" in the assembly-line sense, but the device is small and replicable.

These unit counts will be analyst-verified as part of the concept-feature population workflow. Some scores may shift slightly when the N values are tightened.
