---
document: Alexander_et_al____2025___Affordable__manageable__practical__and_scalable__AMPS__high_yield_and_high
generated: 2026-03-02T23:48:33Z
source_checksum: sha256:7492e1df4fee48030b86ba7fae868f296a063b96f634d66e81754e7c38c94d61
total_lines: 762
depth: 3
section_count: 33
---

# Alexander_et_al____2025___Affordable__manageable__practical__and_scalable__AMPS__high_yield_and_high Index

## 1 Introduction
**Lines:** 46-89 | **Subsections:** 1.1

Motivates fusion energy commercialization by defining the AMPS criteria (Affordable, Manageable, Practical, Scalable), distinguishing MFE vs. IFE confinement approaches across the P-τ parameter space, and introducing pulser IFE as a more efficient alternative to laser IFE — citing MagLIF's second-highest experimental Pτ and ~200× better energy coupling efficiency than NIF's laser indirect-drive.

### 1.1 Pacific Fusion's Roadmap
**Lines:** 90-105

Pacific Fusion's roadmap targets two near-term goals by end of decade: demonstrating facility gain (Q_f > 1) using a pulser-driven inertial fusion approach with >60 MA current delivery in ~100 ns, and resolving key hurdles to commercial fusion power plants. Their DS facility uses impedance-matched Marx generator architecture with commodity components to achieve orders-of-magnitude better driver efficiency than NIF.

## 2 Physics basis for high-gain pulser-driven inertial fusion
**Lines:** 106-107 | **Subsections:** 2.1, 2.2, 2.3, 2.4, 2.5, 2.6

Here's the summary: Pulser-driven inertial fusion physics, covering how magnetically-accelerated conducting liners compress DT fuel at lower velocities and pressures than laser-driven ICF (using MagLIF as a baseline), the theoretical energy balance governing ignition (generalized Lawson criterion, alpha heating, magnetic insulation), efficient pulsed-power energy delivery to targets (~50% wall-plug efficiency vs. ~1% for lasers), high-fidelity simulation validation (HYDRA, GORGON, LASNEX benchmarked against Z-machine MagLIF experiments), gain scaling laws comparing laser-driven and pulser-driven ICF paths to facility gain Q_f > 1 (including Pacific Fusion's Demonstration System projections), and experimentally demonstrated MagLIF thermonuclear performance on Sandia's Z machine.

### 2.1 Physics of pulser-driven inertial fusion
**Lines:** 108-137

Pulser-driven inertial fusion uses pulsed-power machines to magnetically accelerate conducting liners (cylindrical shells) to compress DT fuel, achieving ignition at lower pressures (~10 Gbar) and velocities (~100 km/s) than laser-driven ICF by using magnetic preheat and thermal insulation. MagLIF (Magnetized Liner Inertial Fusion) at Sandia is presented as the baseline concept, with five key advantages enumerated: sound theoretical basis, efficient energy delivery, high-fidelity simulation capability, documented scaling paths to ignition/gain, and experimental demonstration of high fusion performance.

### 2.2 Theoretical basis for pulser-driven inertial fusion
**Lines:** 138-173

Energy balance governing DT fuel self-heating in cylindrical liner implosions (Eq. 1), including alpha-particle heating, PdV work, radiation, conduction, and end losses, plus a generalized Lawson criterion (GLC', Eq. 3) adapted for magnetized inertial confinement. Demonstrates that magnetizing the fuel (BR ≳ 1.0 MG·cm) reduces the areal density and compression required for ignition by >10×, comparing parameter regimes for NIF, MagLIF on Z, and projected DS conditions.

### 2.3 Efficient energy delivery to target
**Lines:** 174-211

Pulser-driven ICF achieves ~200× higher overall efficiency (stored energy → fuel internal energy) compared to NIF laser indirect drive, primarily due to direct magnetic acceleration of the fuel liner eliminating inefficient energy conversion stages. Key efficiency definitions and equations are provided: driver efficiency (η_D), implosion/hydrodynamic efficiency (η_imp) derived from circuit-coupled liner inductance models (Eqs. 4–6), and stagnation efficiency (η_stag), with quantitative comparisons across pulser ICF (1.25%), laser indirect drive (6×10⁻⁵), and laser direct drive schemes.

### 2.4 Simulation capability for ignition and high gain
**Lines:** 212-243

Pacific Fusion co-develops the FLASH radiation MHD code (with University of Rochester) for ICF target design, validated against analytic tests, Z facility experiments, and HYDRA/LASNEX/ALEGRA benchmarks including the MagLIF current-scaling study from 15–60 MA. FLASH simulations of cryogenic DT ice liner MagLIF targets driven by a DS pulser circuit model at 56 MA demonstrate facility gain (Q_f = 1.36 for beryllium liner, Q_f = 4.75 for aluminum liner), confirming that conservatively scaled MagLIF enters the ignition regime above ~50 MA peak current.

### 2.5 Scaling to facility gain
**Lines:** 244-247 | **Subsections:** 2.5.1, 2.5.2, 2.5.3

Scaling to facility gain compares how laser-driven and magnetically-driven inertial confinement fusion systems scale differently to achieve ignition, noting that fuel heating and compression requirements are independent of the compression scheme. It uses NIF laser ignition results (DT shell velocity ≥400 km/s) as a baseline for understanding the technical basis of pulser-driven ICF.

#### 2.5.1 Scaling laser-driven ICF
**Lines:** 248-279

Hydrodynamic-equivalent scaling laws for laser-driven inertial confinement fusion, where geometric and temporal quantities scale together (r ∝ E_L^{1/3}), keeping implosion velocity, ablation pressure, and stagnation conditions constant. Derives how DT yield scales as E_L^{4/3} and target gain as E_L^{1/3} in the robustly-burning regime, showing unfavorable gain scaling — e.g., reaching Q_target ≈ 10 from NIF's Q ≈ 2.4 would require ~10 MJ laser energy.

#### 2.5.2 Scaling pulser-driven ICF
**Lines:** 280-294

Scaling laws for pulser-driven ICF (MagLIF-style) show fusion yield scales as Y_DT ∝ I_max^6 and target gain as Q_target ∝ E_liner^2, which is much more favorable than laser ICF hydro-equivalent scaling. The section also covers efforts to simplify target designs by eliminating separate preheat lasers and Helmholtz coils in favor of current pre-pulse approaches.

#### 2.5.3 Comparing scaling on the NIF to Pacific Fusion's DS
**Lines:** 295-338

Compares NIF ignition performance metrics (target gain, fuel gain, burn-up fraction, facility gain) to simulated MagLIF targets on Pacific Fusion's Demonstration System (DS), using 1990 Mead gain curves and FLASH current-scaling studies. Key result: MagLIF achieves Q_f > 1 on the DS (1.36–4.75) by efficiently compressing ~50× larger fuel masses than NIF at comparable burn-up fractions (3–10%), with Table 1 providing a detailed metric comparison across NIF, Be-liner, and Al-liner DS targets.

### 2.6 Demonstrated performance with thermal fusion reactions
**Lines:** 339-346

Magnetically-driven pulsed fusion systems historically produced neutrons via non-thermal beam-driven mechanisms (e.g., in Z-pinches and dense plasma focus devices), which scale poorly toward ignition. MagLIF avoids this by using thick metal liner implosions that shield fuel from driver currents, with extensive experimental evidence from Sandia — including neutron spectra, Bayesian data assimilation, yield-temperature scaling, and mix degradation studies — confirming fully thermal fusion burn, supporting favorable scaling to ignition and gain.

## 3 Pulser Design
**Lines:** 347-348 | **Subsections:** 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8

Pacific Fusion's Demonstration System (DS) pulsed-power driver architecture, covering IMG module design (156 modules, 80 MJ stored energy, >60 MA delivery), water-insulated transmission lines, target area subsystems (MITLs, cassette, diagnostics), full-system electromagnetic modeling with 96% driver coupling efficiency, pulse shaping capabilities, a comprehensive nuclear/x-ray/optical diagnostic suite, and facility cost (~$500M, 10x less than NIF).

### 3.1 Demonstration System (DS) Overview
**Lines:** 349-356

Pacific Fusion's Demonstration System (DS) is a pulsed-power facility (~73m × 80m) designed to store ~80 MJ of electrical energy and deliver >60 MA over ~100 ns timescales to a fusion target, using a three-level impedance-matched Marx generator (IMG) architecture with water-insulated transmission lines, magnetically insulated transmission lines (MITLs), and a post-hole convolute to compress fusion fuel via Lorentz force.

### 3.2 Pulser Modules: IMGs
**Lines:** 357-366

IMG (Intensifier Marx Generator) modules are the building blocks of the DS pulser, structured hierarchically: two capacitors + spark gap switch form a "brick," 10 bricks per stage discharge in parallel, and 32 stages per module are connected in series, yielding 512 kJ storage per module at ±100 kV bipolar charging with 160 nF capacitors. The full DS pulser contains 156 modules in parallel storing ~80 MJ total and delivering >350 TW to the water section.

### 3.3 Water Transmission Lines
**Lines:** 367-370

Coaxial pulse tube and tri-plate transmission lines use deionized water as the dielectric to deliver current to the target chamber, where magnetically insulated transmission lines connect to the ICF target. The system's low capacitance and inductance eliminate the need for pulse compression at pulses as short as 100 ns, with longer pulses achievable by varying module trigger timing.

### 3.4 Target Area
**Lines:** 371-382

Pacific Fusion's Target Area comprises five subsystems — vacuum power flow (insulator stack, outer-MITLs, triple post-hole-convolute, inner-MITL), a replaceable cassette housing the target and inner-MITL for shot-to-shot flexibility, chamber support systems, target diagnostics with multiple line-of-sight ports, and blast management hardware. The cassette-based design enables offline assembly, rapid iteration on target designs, and at least 1 shot/day tempo, while a 5 m water tank surrounding the target chamber provides neutron shielding.

### 3.5 Full DS Modeling
**Lines:** 383-390 | **Subsections:** 3.5.1, 3.5.2

Full driver system (DS) circuit modeling using the CASTLE code at the module level, validated by 2D/3D electromagnetic and particle-in-cell (CHICAGO) simulations of each subsystem, with a proprietary optimizer balancing component designs and facility layout constraints.

#### 3.5.1 Power Delivery in Vacuum Section
**Lines:** 391-402

Magnetically Insulated Transmission Lines (MITLs) carry current from the water-vacuum interface to the fusion target through six outer MITLs joined by a triple-post-hole convolute into a single inner MITL, with the insulator stack delivering ~310 TW peak power and designed to keep flashover probability below 0.2%. Full electromagnetic kinetic PIC simulations (CHICAGO) model the vacuum section in three overlapping spatial regions, incorporating space-charge-limited electron emission (>240 kV/cm), ion emission (>600 K surfaces), and 1D thermal/magnetic diffusion models on electrode surfaces.

#### 3.5.2 Driver coupling efficiency
**Lines:** 403-414

Driver coupling efficiency for the AMPS pulsed-power driver, quantifying current loss through the vacuum section (outer MITLs, convolute, inner MITL) via plasma formation and Hall-like current diversion mechanisms. At peak current, the driver delivers ~62.8 MA, 115 TW, and 10 MJ to the load, coupling 96% of insulator-stack current to the final load, with simulations showing progressive current loss as plasma sources are added to each vacuum component.

### 3.6 Pulse Shaping
**Lines:** 415-422

Pulse shaping on the DS pulser is achieved at two levels — independent module triggering (~715 ns transit-time isolation) and level-to-level isolation (~750 ns) — with optional water switches for longer pulses, enabling replication of Z-Machine pulse profiles using only ~30% of stored energy, or a 2.75× peak current increase at full charge voltage.

### 3.7 Diagnostic Suite
**Lines:** 423-440

The DS (Diagnostic Suite) diagnostic plan for achieving net facility gain in ICF experiments, comprising nuclear diagnostics (NTOF, ENDOR neutron imaging, CEKOV, RIDE, MARS, ASTRA), x-ray diagnostics (CRAB, GALAXI, VIRGO, SPICE, DIPPER), and optical diagnostics (FARAD, VISAR, PDV) arranged around a ~13m radius water chamber, with a model-driven Bayesian inference approach to track implosion performance via the Generalized Lawson Criterion (GLC) χ.

### 3.8 Facility cost comparison
**Lines:** 441-446

Pacific Fusion's 80 MJ Driver System (DS) is estimated to cost ~$500M (~$6/J), comparable to the ZR facility rebuild ($6.3/J in 2025 dollars) and roughly 10× cheaper than the NIF ($4.9B in 2025 dollars).

## 4 Path to commercial power
**Lines:** 447-464 | **Subsections:** 4.1, 4.2, 4.3

Covers the three additional technical developments needed to transition from a demonstration system (DS) to commercial pulsed IFE power plants: component lifetime for repetitive long-cycle operation, fusion chamber durability and rapid shot clearing, and tritium breeding blanket/first-wall compatibility with efficient energy capture.

### 4.1 Component lifetime
**Lines:** 465-474

IFE pulsed-power plants require component lifetimes averaging 1 billion shots at 0.1–10 Hz repetition rates — 10⁴–10⁶× higher than current single-shot-per-day facilities like NIF. The two limiting components are high-voltage capacitors and spark gap switches, addressable via (1) derating/parallelization (e.g., reducing voltage 3× increases capacitor lifetime from ~10⁵ to ~10⁹ shots at the cost of 9× more units) or (2) innovative designs (improved dielectrics, multi-channel spark gaps, solid-state switches).

### 4.2 Fusion chamber
**Lines:** 475-478 | **Subsections:** 4.2.1, 4.2.2, 4.2.3

Rapid cycling of IFE fusion chambers requires solving three engineering challenges: safe ejection of replaceable electrodes, wall protection from post-shot impulse loading, and fast restoration of high vacuum between shots.

#### 4.2.1 Replaceable electrode disassembly
**Lines:** 479-486

Low-mass replaceable inner MITLs (iMITLs) for pulsed-power fusion chambers, designed to minimize debris and recycled mass by using thin copper electrodes (~50–100μm) that carry surface current without significant deformation, with a promising configuration showing only ~14% inductance penalty versus large-mass immovable MITLs.

#### 4.2.2 Post-shot vacuum chamber impulse response
**Lines:** 487-510

Post-shot vacuum chamber impulse response in pulser ICF systems, covering the four categories of loads on target-facing structures (hydrodynamic blast, radiative x-ray emissions/ablative shocks, neutron damage, debris/shrapnel), the simulation approaches used to predict structural effects (radiation MHD, shock EOS, structural dynamics, fatigue), and the finding that residual magnetic fields direct ~93% of mass and ~85% of momentum axially along the poles, minimizing radial damage to driving hardware.

#### 4.2.3 Chamber pumping and reloading
**Lines:** 511-514

Unique engineering challenges for pulsed ICF (specifically pulser-driven) systems operating at ~1 Hz repetition rate: each shot cycle requires inserting a new target and new inner MITL sections (split into consumable/recyclable and permanent shielded segments), then rapidly re-establishing high vacuum between MITLs. Chamber preparation strategies include mechanical target exchange hardware and getter-based vacuum recovery, alongside broader concerns about blanket neutronics, tritium breeding, energy recovery, and radiation shielding.

### 4.3 Tritium breeding
**Lines:** 515-528

Tritium breeding ratio (TBR) exceeding unity is required for feasible fusion power plants; pulsed-power MITL-driven systems achieve this using lithium-containing blankets (e.g., FLiBe molten salt), with MCNP neutronics confirming sufficient TBR at appropriate blanket thickness. Unlike laser IFE, MITL energy coupling allows nearly full blanket coverage around the target (no line-of-sight constraint), which also enables first-wall protection from blast loading, radiation, and DPA limits via thick liquid blanket or aerosol shielding.

## 5 Utility to the broader fusion community
**Lines:** 529-540

Pacific Fusion's Demonstration System (DS) supports both US fusion commercialization goals (Fusion Pilot Plant by 2035-2040) and national defense needs for high-yield (>100 MJ) inertial fusion, while generating community-wide benefits in pulsed power technology, neutron sources, plasma diagnostics, and simulation capabilities. The section advocates for public-private partnerships (e.g., DOE's INFUSE, Milestone-Based Fusion Development Program) to leverage Pacific Fusion's private investment for broader fusion community advancement.

## 6 Conclusion
**Lines:** 541-544

Pulser-driven inertial fusion (specifically Pacific Fusion's DS device) offers a near-term path to commercial fusion power by delivering tens of MJ to magnetized targets at high efficiency, targeting Qf > 1. The DS exceeds 60 MA and represents a claimed 1000× improvement over NIF (100× gain at 1/10 cost), advancing both commercial energy and high-yield fusion goals.

## 7 Acknowledgments
**Lines:** 545-762

Acknowledgments listing 12 contributors, followed by Appendix A deriving a generalized Lawson criterion (GLC') for pulser-driven ICF that accounts for magnetized fuel self-heating, thermal conduction losses, and liner confinement — showing ignition at lower areal densities via fuel magnetization (Eqs. 8–17, Figure 21). Appendix B describes pulser-target coupling physics in magnetically insulated transmission lines (MITLs), including frozen-flux MHD concepts, Alfvén velocity limits on current delivery, and plasma-induced current loss mechanisms. The section concludes with 142 references spanning pulsed-power accelerators, MagLIF experiments, NIF results, and Z-pinch IFE reactor concepts.
