---
source: "https://arxiv.org/html/2408.15206v1"
source_type: "url"
extracted_at: "2026-03-29T17:42:28.918435+00:00"
content_hash_sha256: "7145ae4f71a828e89756f53b2f07aaf30fa2753a245fc56adb8c27d05e575a34"
backend: "trafilatura"
title: "Opportunities in Pulsed Magnetic Fusion Energy"
author: "C Leland Ellison Pacific Fusion; Fremont CA; USA"
---

# Opportunities in Pulsed Magnetic Fusion Energy

###### Abstract

Fusion is a potentially transformational energy technology, which promises limitless clean energy. Yet, it requires continued scientific and technological development to realize its potential. The conditions necessary for fusion energy gain in terms of the product of plasma pressure and confinement time have been known for many decades. An underappreciated fact is that pulsed magnetic fusion has demonstrated performance on par with laser-driven ICF and tokamaks despite receiving only a small fraction of investment relative to those concepts. In light of this demonstrated performance, well-established scaling relations, and opportunities for further innovations, here we advocate for pulsed magnetic fusion as the most attractive path towards commercialization of fusion energy.

## 1 Introduction

Increasing urgency for carbon-free energy sources [[1](https://arxiv.org/html/2408.15206v1#bib.bib1)] and recent scientific advances in fusion [[2](https://arxiv.org/html/2408.15206v1#bib.bib2), [3](https://arxiv.org/html/2408.15206v1#bib.bib3), [4](https://arxiv.org/html/2408.15206v1#bib.bib4)] have catalyzed a national conversation regarding the most promising path to commercial fusion energy.

Pulsed magnetic fusion (PMF), in which a rapid magnetically-driven implosion reaches fusion conditions, spans significant ranges in phase space (e.g. from O(100ps) to O(s) with a corresponding to exceed Lawson’s criterion). In recent years, leading PMF platforms have demonstrated performance exceeding the records achieved with steady-state magnetic confinement devices (e.g., tokamaks) and on par with laser-driven inertial confinement fusion (ICF) experiments at similar facility scale (e.g., OMEGA) [[5](https://arxiv.org/html/2408.15206v1#bib.bib5), [6](https://arxiv.org/html/2408.15206v1#bib.bib6)] (as the only ignition-scale ICF facility, the NIF has the highest measured ). Despite this performance, PMF remains less explored than magnetic confinement and laser-based ICF approaches.

As the U.S. moves towards a fusion-powered future under the White House’s “bold decadal vision,”[[7](https://arxiv.org/html/2408.15206v1#bib.bib7)] we believe PMF to be the most attractive path forward when balancing technology maturation, cost, and complexity. We find support for this conclusion in a recent JASON study [[8](https://arxiv.org/html/2408.15206v1#bib.bib8)], which considered a broad parameter space including PMF as a low-cost path towards fusion energy, and in a white paper on fusion by the Science for America organization [[9](https://arxiv.org/html/2408.15206v1#bib.bib9)] (see Fig. [1](https://arxiv.org/html/2408.15206v1#S1.F1)).

Our PMF community is driven by the following key principles:

-
•
The world is in immediate need of clean, deployable energy solutions including fusion.

-
•
Pulsed magnetic fusion is the best way to achieve high gain and high yield fusion, relevant for energy generation, and it has the potential to operate at lower stored energy and to be significantly more compact than competing technologies.

-
•
The U.S. is the leader in pulsed power technology and is in ideal position to lead high gain and high yield pulsed magnetic fusion, for both energy applications and national security, respectively.


Our key principles imply that to meet the bold decadal vision through PMF, we must do the following:

-
•
We must rapidly advance reliable, high power pulsers capable of high repetition-rate.

-
•
We need a paradigm shift in pulser operational excellence to drive experimental innovation.

-
•
We must advance high target designs in multiple pressure regimes.

-
•
We need target design codes and power flow modeling tools that are publicly available and have a large user base.

-
•
We need state-of-the-art diagnostics for inferring and critical plasma conditions that cover a wide range of parameter space and capable of rep rate.

-
•
We need to form partnerships across the fusion energy ecosystem to advance materials science, tritium processing, and commercial engineering code development for fusion power systems.

-
•
We need a focused science and engineering outreach program (ZNetUS and others) to develop future leaders and the supply chain that spans industry, national laboratories, and academia.

-
•
By the end of the decade, we can and must demonstrate facility gain () and remove significant technology hurdles to commercialization.


## 2 High-level vision

To realize the U.S. bold decadal vision for fusion energy through PMF and to realize the potential of PMF across the spectrum of energy and national security applications, we believe that the following three facilities are required:

-
1.
Demonstrate by the end of decade.

-
2.
Demonstrate a fusion pilot plant within 5 years after is demonstrated.

-
3.
Develop a high-yield source for NNSA’s national security mission [

[10](https://arxiv.org/html/2408.15206v1#bib.bib10)].

The first two facilities will advance the frontier of fusion energy. The first goal, to demonstrate , will require producing MJ fusion yields from a “single shot” scientific PMF facility. The second goal, a commercially-relevant demonstrator, will likely be s of MJ yields at fusion energy system-relevant shot rates and with power plant technologies (e.g. tritium breeding blanket, heat exchanger, load recycling, etc.).

The third facility has distinct requirements derived from NNSA’s national security mission, identified in recent roadmaps as a multi-mission111including x-ray sources, dynamic material properties, and high-energy-density physics studies in addition to the capability to execute high yield fusion experiments next-generation pulsed power (NGPP) capability[[11](https://arxiv.org/html/2408.15206v1#bib.bib11)]. It is possible that the NNSA’s most critical requirements could be met by the facility, motivating the development of a public-private partnership during its planning phase to ensure the national security elements required of NGPP were included during the initial build.

While the facilities required to achieve these three ambitious goals are distinct, successful execution of any of the facilities will require addressing a common set of scientific and engineering considerations. Recent workshops on the basic research needs for inertial fusion energy[[12](https://arxiv.org/html/2408.15206v1#bib.bib12)] did not fully explore the opportunities in pulsed magnetic fusion; here we provide a community-driven look at the key components of a program to advance the technology readiness level for pulsed magnetic fusion energy (PMFE). In the following sections, we present these considerations together with technical opportunities for innovation.

## 3 Pulser architectures

### 3.1 Overview

The Z Facility at Sandia National Laboratories [[11](https://arxiv.org/html/2408.15206v1#bib.bib11)] is presently the world’s largest and most powerful pulser. Z represents the culmination of conventional pulsed-power technology development. The pulser architecture and components upon which Z is based were developed in the 1900s.

Z is driven by conventional Marx generators that produce a power pulse with a 1-s rise time. Since many physics targets of interest require a 100-ns pulse, Z includes multiple stages of electrical-pulse compression. Such stages complicate the design, operation, and maintenance of Z, and reduce Z’s electrical-energy efficiency.

An advanced PMFE pulser architecture has the following objectives: high energy efficiency, simplicity of design, economies of scale, and engineered safety. Over the past decade, pulser architectures have evolved towards these objectives by using single-stage electrical pulse compression, low-voltage switching, and impedance matching [[13](https://arxiv.org/html/2408.15206v1#bib.bib13), [14](https://arxiv.org/html/2408.15206v1#bib.bib14), [15](https://arxiv.org/html/2408.15206v1#bib.bib15)]. Here, we propose future PMFE pulsers use a simplified architecture that meets all of these objectives [[16](https://arxiv.org/html/2408.15206v1#bib.bib16)].

### 3.2 Advantages of the advanced architecture

The conventional Marx generator was invented a century ago, in 1924, by Erwin Marx. Since then, most pulsers have been powered by such technology. A Marx is an electrical circuit that charges capacitors in parallel, and discharges them in series. A conventional Marx is modeled with 0-D lumped circuit elements, and is designed to stack voltages.

The IMG concept was invented in 2017 [[16](https://arxiv.org/html/2408.15206v1#bib.bib16)]. Like a conventional Marx, an IMG also charges capacitors in parallel and discharges them in series. However, an IMG is designed to account for electromagnetic-wave propagation: an IMG is modeled with 1-D transmission-line-circuit elements and is designed to stack waves.

Figure [3](https://arxiv.org/html/2408.15206v1#S3.F3) illustrates a transmission-line-circuit model of a four-stage IMG. An IMG is a pulsed-power analog of a laser, with an energy efficiency of 90%. (For comparison the flashlamp-pumped NIF laser is efficient, and modern diode-pumped lasers are efficient).

Table [1(a)](https://arxiv.org/html/2408.15206v1#S3.T1.st1) compares parameters of a Z Marx generator (which is a conventional 30-stage Marx) with those of a 30-stage IMG. As described by the table, even though the IMG stores a factor of 6 less energy, it generates 34 percent more power. Figure [4(a)](https://arxiv.org/html/2408.15206v1#S3.F4.sf1) compares the time history of the electromagnetic power generated by the 30-stage Z Marx with that of the 30-stage IMG. Today, implementation of the architecture in practice has been limited to the 4-stage, 8-brick 60-GW Sirius-1 prototype [[17](https://arxiv.org/html/2408.15206v1#bib.bib17)].

By design, the advanced pulser architecture delivers the following:

#### 3.2.1 Increased energy efficiency

Each Z Marx generates a power pulse with 1-s rise time. Since many physics targets of interest must be driven by a 100-ns pulse, the Z machine requires four stages of electrical pulse compression. By design, the IMGs of the new architecture directly generate a 100-ns pulse. Because electrical pulse compression reduces efficiency, the calculated energy efficiency of the new architecture is twice that of the Z machine[[17](https://arxiv.org/html/2408.15206v1#bib.bib17)].

#### 3.2.2 Increased component reliability and lifetimes

The Z Facility is powered by switches that operate at voltages as high as 6 MV. All the switches of the new architecture operate at 200 kV; lower-voltage switches are easier to design, fabricate, assemble, operate, trigger, and maintain. As indicated by Fig. 3, the switches of the Z Marx generators transfer 220 mC per shot; IMG switches transfer only 16 mC. Lower charge transfer will lead to longer operational lifetime and reduced maintenance. These improvements are expected to be significant, approaching an order of magnitude.

#### 3.2.3 Reduced pulser cost

A pulser that delivers a given current to a physics target has a reduced stored energy with the new architecture compared to a conventional system because of its improved energy efficiency. The physical size is also reduced by approximately a factor of 2 in area.
These factors lead us to expect that the cost of a new architecture pulser is significantly less than a conventional architecture. Additional cost savings will result from the immense simplifications offered by the new architecture. More specifically, the new architecture eliminates the following components of existing conventional pulsers: SF6 recirculation and processing, -kV switching and energy storage, laser triggering systems, and high voltage water switching.

#### 3.2.4 Commercialization

In the advanced pulser architecture, the basic building blocks of energy storage and switching components enable Hertz-scale repetition rates and significantly improved reliability for long-life applications such as fusion energy. This is because the RC charging time constant of the distributed architecture of the IMG is 20 times lower than conventional pulser technology, while the coulomb transfer is lower by no less than an order of magnitude (see Table [1(a)](https://arxiv.org/html/2408.15206v1#S3.T1.st1). Moreover, component optimization takes place on a relatively small physical scale (e.g. individual capacitors and switches). Advanced pulser architectures like the IMG thus open a path to mass-manufacturing that is not otherwise open to conventional pulser architectures.

Gaps in technology exist that need to be bridged to achieve the durability, high rep-rate, and affordability necessary for the commercialization of fusion energy, regardless of the system’s design. For instance, lasers, tokamaks, and pulsers all fundamentally rely on pulsed power systems. Regardless of fusion approach, to meet the capital expenditure (CapEx) goals for commercial viability, technology improvements are needed. For example, the energy storage and switching component replacement lifespan must extend by at least a factor of 1000 at Hertz operating rate. The cost of energy storage and switching must decrease by a factor of 5 to 10. There are design optimization axes to reduce coulomb transfer by several orders of magnitude in advanced pulsers to meet commercialization targets.

### 3.3 Advancing Technology Readiness Level

To advance pulser technology readiness level (TRL) at reactor-compatible energy, efficiency, and repetition rate, pulsed magnetic fusion power systems require maturation of pulser architectures (such as IMGs) that are capable of Hertz repetition rate, multi-million shot lifetimes, and production scale mass manufacturing. Focused investment in high reliability energy storage (i.e. capacitors) and switching technologies capable of very high power (100 kV, 50+ kA) benefits all fusion approaches, including PMFE.

## 4 Target physics, fabrication, and experimental capabilities

[6](https://arxiv.org/html/2408.15206v1#bib.bib6)] (purple point), a simulated current scaling gas-filled design [

[18](https://arxiv.org/html/2408.15206v1#bib.bib18)] (purple curve and point), and estimated conditions for a high-gain GJ yield (shaded region, e.g. Ref.

[19](https://arxiv.org/html/2408.15206v1#bib.bib19),

[18](https://arxiv.org/html/2408.15206v1#bib.bib18)).

### 4.1 Theoretical basis

As mentioned in Section [1](https://arxiv.org/html/2408.15206v1#S1), a single PMF facility can explore target designs that operate over orders of magnitude in and respectively, as shown in Fig. [5](https://arxiv.org/html/2408.15206v1#S4.F5). We identify three regions in the phase space, each with unique characteristics, all accessible using the same engineered pulser. At the center of this space is an inertial fusion regime where intermediate pressure systems can ignite when the fuel is highly magnetized (such as MagLIF, described later). Fig. [5](https://arxiv.org/html/2408.15206v1#S4.F5) shows an experimental point from Z (purple circle) and a simulated scaling curve from 20 to 60 MA from Ref. [18](https://arxiv.org/html/2408.15206v1#bib.bib18) for a gas-filled MagLIF target that produces up to MJ yield. To the left is an inertial fusion regime with higher pressure and lower confinement time (PMF high-). Slutz and others have published MagLIF simulated designs with ice layers that produce in excess of GJ yields; a simple estimate of for such shots is to assume similar liner , that the yield at high ion temperature, and that hydro confinement which produces the high-gain shaded region shown. To the right is a dynamic equilibrium regime where s duration pulses to drive targets at lower pressure with longer confinement time (PMF low-).

In the inertial regime, the requirements to heat and compress fusion fuel to ignition conditions are independent of the compression scheme. Lasers such as the NIF accelerate a DT fusion fuel shell to high velocity ( km/s) to compressively heat the central vapor hot spot. Such implosions are susceptible to hydrodynamic instabilities, but laser direct drive (LDD) and laser indirect drive (LID) implosions benefit from ablative stabilization. In pulsed magnetic fusion, magnetically driven shells (liners) are continuously driven throughout the power pulse. For a recent review of ICF theory see Ref. [20](https://arxiv.org/html/2408.15206v1#bib.bib20).

The target at the core of all pulsed DT fusion schemes must be hot enough to have high fusion reactivity (usually 10 keV temperatures or above) and be confined such that self-heating, from energy released in the form of 3.6 MeV alpha particles, compensates for or surpasses energy loss mechanisms. In the inertial fusion regime, the hot fuel’s self-heating surpasses all loss mechanisms and “ignites,” initiating a thermonuclear explosion in which the burn is only quenched by hydrodynamic expansion of the fuel, with a time scale set by its inertia.

As discussed above, these requirements can be met by systems with a wide range of energy density or fuel pressure as long as the product of pressure and confinement time is large enough. In the extensive PMFE regime shown in Figure [5](https://arxiv.org/html/2408.15206v1#S4.F5), the portion where burn duration and confinement time is less than O(10)s of nanoseconds, plasma conditions are achieved by rapid implosion of a fuel-containing target i.e. the “inertial fusion” regime.

For longer burn time scales (i.e. ns), but with the overall system still pulsed (current rise time s), a fusion system must operate in a “dynamic equilibrium” configuration, where the fuel is hydrodynamically quasi-static during the burn duration and the energy balance in the fuel is a competition between self-heating, auxiliary heating, and other energy loss mechanisms (e.g. radiation and thermal conduction). Plasma confinement is always required, with additional hydrodynamic confinement required when the plasma pressure exceeds the strength of materials (O(10) kBar).

PMF is the only fusion approach where a single facility can explore target concepts ranging from a classic inertial fusion regime, where the ignition physics has been demonstrated at NIF, to the dynamic equilibrium regime, where target physics is less explored but pressure requirements are more forgiving. This is illustrated by the wide range in confinement time shown in Figs. [1](https://arxiv.org/html/2408.15206v1#S1.F1) and [5](https://arxiv.org/html/2408.15206v1#S4.F5). In all cases considered, the target physics time scales are orders of magnitude shorter than the time over which the chamber absorbs the energy emitted and resets its conditions for the subsequent shot.

2/g. (from Ref.

[21](https://arxiv.org/html/2408.15206v1#bib.bib21)).

One pulsed magnetic fusion concept in the inertial fusion regime is Magnetized Liner Inertial Fusion, or MagLIF; of the space shown in Fig. [5](https://arxiv.org/html/2408.15206v1#S4.F5), we focus only on MagLIF here as a well-documented, high-performing concept. In the MagLIF concept, a cylindrical metal liner is accelerated by driving a large current across its outer surface. The shell is driven at lower velocity km/s to mitigate instabilities. Pre-heat energy and magnetic field, to suppress thermal conduction losses, are injected into the fuel cavity before the implosion stagnates, preconditioning the hot spot to ignite at lower stagnation pressure than a laser-driven implosion. MagLIF has a sound theoretical basis, extending the theory of Inertial Confinement Fusion (ICF) to include magnetized fuel [[22](https://arxiv.org/html/2408.15206v1#bib.bib22), [21](https://arxiv.org/html/2408.15206v1#bib.bib21)]. Fig. [6](https://arxiv.org/html/2408.15206v1#S4.F6) shows the diagram for cylindrical magnetized hot-spots, with magnetization relaxing the requirement on fuel . Thus, MagLIF provides a magnetic direct drive pathway to ignition and gain that takes advantage of low-cost, compact pulsers.

### 4.2 MagLIF scaling

The MagLIF concept has been explored experimentally at the Sandia Z facility, using the same measurement techniques employed on large lasers like the NIF and Omega. Bayesian inference techniques are used to determine proximity to ignition via the generalized Lawson parameter , the ratio of the measured to the value required for ignition. On Z, has been demonstrated[[6](https://arxiv.org/html/2408.15206v1#bib.bib6)]. While Z is far from ignition, scales favorably with facility size for pulsed magnetic approaches compared to laser schemes. Conservative similarity scaling theory and numerical simulations give , where is the peak drive current delivered to a target[[23](https://arxiv.org/html/2408.15206v1#bib.bib23)]. Facility size scales with delivered energy , so . In contrast, hydrodynamic scaling of laser-driven targets gives . Thus, while the obtained via laser direct drive on Omega is closer to ignition than Z, scaling this to a (symmetric) NIF-caliber 2.15 MJ laser results in and a fusion output of 1.6 MJ (target gain )[[24](https://arxiv.org/html/2408.15206v1#bib.bib24)].

[23](https://arxiv.org/html/2408.15206v1#bib.bib23)).

[18](https://arxiv.org/html/2408.15206v1#bib.bib18))

2D clean simulations using the rad-MHD code HYDRA, shown in Fig. [7(a)](https://arxiv.org/html/2408.15206v1#S4.F7.sf1), show that can be achieved by MagLIF driven at MA, with simulated energy production MJ[[23](https://arxiv.org/html/2408.15206v1#bib.bib23)]. This design scaling is conservative, meaning it maintains the dynamics of implosions tested on Z by conserving the values of dimensionless parameters that describe the system (similarity scaling)[[25](https://arxiv.org/html/2408.15206v1#bib.bib25), [26](https://arxiv.org/html/2408.15206v1#bib.bib26)]. This suggests ignition with a cylindrical magnetized hot-spot is accessible to a reasonable pulser. Conservative scaling is presently being evaluated on the Z facility. Adding a cryogenic DT fuel liner to the implosion (not yet tested on Z) can mitigate impurity mix and increase the potential yield to many hundreds of megajoules[[19](https://arxiv.org/html/2408.15206v1#bib.bib19), [18](https://arxiv.org/html/2408.15206v1#bib.bib18), [27](https://arxiv.org/html/2408.15206v1#bib.bib27)] (Fig. [7(b)](https://arxiv.org/html/2408.15206v1#S4.F7.sf2)).

Thus, pulsed magnetic driven ICF is the shortest path to ignition that takes advantage of low-cost compact pulsers while retaining the “ICF advantage” — the same facility can drive multiple designs and concepts, enabling rapid iteration and innovation. Pulsed magnetic targets are fabricated using the same technologies as laser targets, such as precision machining and electroplating. Pulsed magnetic targets are simpler than cryogenic hohlraum targets on the NIF, with fewer components and assembly steps, and with surface roughness requirements that are simpler to achieve - similar to that of 22-caliber bullet casings, which are made using rapid, low cost honing processes.

Finally, we emphasize that while MagLIF is an ideal starting point, it is only the start: Innovations in target physics design and target fabrication will enable rapid progress for high targets with higher and lower pressure than MagLIF. Experimental tests of innovative concepts are critical and are presently limited to publicly-funded facilities.

### 4.3 Advancing Technology Readiness Level

Demonstration of ignition and reactor-level gain requires a pulser that delivers multiple megajoules to an inertial fusion target, or equivalently delivering 50+ MA to a target region (r cm). This facility will also enable innovation on target physics relevant for PMFE. Fabrication of reactor-compatible targets with cost-effective manufacturing methods at scale is required for all IFE approaches, including PMFE.

Access to public-sector PMF facilities such as the Z Facility, which are presently the only ones capable of testing integrated target physics concepts, would advance innovation in design in the near term.

## 5 Simulations and modeling

### 5.1 Target Design

Computational modeling has been essential to the advancement of fusion, including the achievement of laboratory ignition [[28](https://arxiv.org/html/2408.15206v1#bib.bib28), [29](https://arxiv.org/html/2408.15206v1#bib.bib29)]. Designing high performance targets for future PMF facilities will require verified and validated radiation magnetohydrodynamics (MHD) codes available to a scientific community spanning national labs, academia, and private industry. Over the past decade, the PMF community has demonstrated the ability to model state-of-the-art PMF experiments to a high degree of accuracy [[30](https://arxiv.org/html/2408.15206v1#bib.bib30), [31](https://arxiv.org/html/2408.15206v1#bib.bib31), [32](https://arxiv.org/html/2408.15206v1#bib.bib32), [33](https://arxiv.org/html/2408.15206v1#bib.bib33), [34](https://arxiv.org/html/2408.15206v1#bib.bib34), [35](https://arxiv.org/html/2408.15206v1#bib.bib35), [36](https://arxiv.org/html/2408.15206v1#bib.bib36), [37](https://arxiv.org/html/2408.15206v1#bib.bib37)]. However, today the most heavily used and validated PMF design codes are not available for use outside of national laboratories and their chosen collaborators. Thus, a need exists for a more widely available, validated, rad-MHD design capability.

One exciting prospect for meeting the need for a widely used, verified and validated modeling capability is the FLASH code. FLASH [[38](https://arxiv.org/html/2408.15206v1#bib.bib38)] is a publicly-available, parallel, multi-physics, adaptive mesh refinement (AMR), finite-volume Eulerian hydrodynamics and magneto-hydrodynamics (MHD) code, developed at the University of Rochester by the Flash Center for Computational Science ([https://flash.rochester.edu](https://flash.rochester.edu)).
FLASH scales well to over 100,000 processors and uses a variety of parallelization techniques like domain decomposition, mesh replication, and threading, to optimally utilize hardware resources.
The FLASH code has a world-wide user base of more than 4,350 scientists, and more than 1,300 papers have been published using the code to model problems in a wide range of disciplines, including plasma astrophysics, combustion, fluid dynamics, high energy density physics (HEDP), and fusion energy.

Over the past decade and under the auspices of the U.S. DOE NNSA, the Flash Center has added in FLASH extensive HEDP and extended-MHD capabilities [[39](https://arxiv.org/html/2408.15206v1#bib.bib39)] that make it an ideal tool for the multi-physics modeling of PMF.
These include multiple state-of-the art hydrodynamic and MHD shock-capturing solvers [[40](https://arxiv.org/html/2408.15206v1#bib.bib40)], three-temperature extensions [[39](https://arxiv.org/html/2408.15206v1#bib.bib39)] with anisotropic thermal conduction that utilizes high-fidelity magnetized heat transport coefficients [[41](https://arxiv.org/html/2408.15206v1#bib.bib41)], heat exchange, multi-group radiation diffusion, state-of-the-art electrothermal transport coefficients [[42](https://arxiv.org/html/2408.15206v1#bib.bib42)], tabulated multi-material EOS and opacities, laser energy deposition, circuit models, and numerous synthetic diagnostics [[43](https://arxiv.org/html/2408.15206v1#bib.bib43)].

FLASH and its capabilities have been validated for over a decade through benchmarks and code-to-code comparisons [[44](https://arxiv.org/html/2408.15206v1#bib.bib44), [45](https://arxiv.org/html/2408.15206v1#bib.bib45), [46](https://arxiv.org/html/2408.15206v1#bib.bib46)] and through direct application to numerous laser-driven plasma physics experiments [[47](https://arxiv.org/html/2408.15206v1#bib.bib47), [48](https://arxiv.org/html/2408.15206v1#bib.bib48), [49](https://arxiv.org/html/2408.15206v1#bib.bib49), [50](https://arxiv.org/html/2408.15206v1#bib.bib50), [51](https://arxiv.org/html/2408.15206v1#bib.bib51), [52](https://arxiv.org/html/2408.15206v1#bib.bib52), [53](https://arxiv.org/html/2408.15206v1#bib.bib53), [54](https://arxiv.org/html/2408.15206v1#bib.bib54)], leading to innovative science and publications in high-impact journals.
For pulsed-power experiments, FLASH has been able to reproduce past analytical models [[55](https://arxiv.org/html/2408.15206v1#bib.bib55)], is being applied in the modeling of capillary discharge plasmas [[56](https://arxiv.org/html/2408.15206v1#bib.bib56)], and is being validated against gas-puff experiments at CESZAR [[57](https://arxiv.org/html/2408.15206v1#bib.bib57)] and canonical liner implosion experiments at Z. For instance, Fig. [8](https://arxiv.org/html/2408.15206v1#S5.F8) shows FLASH simulations of the magneto-Rayleigh-Taylor aluminum liner platform described in Refs. [[31](https://arxiv.org/html/2408.15206v1#bib.bib31), [32](https://arxiv.org/html/2408.15206v1#bib.bib32)].

[31](https://arxiv.org/html/2408.15206v1#bib.bib31),

[32](https://arxiv.org/html/2408.15206v1#bib.bib32)]. From top to bottom, the images correspond to radiographs taken at 0, 42.7, 57.0, 67.7 and 83.0 ns.

Accelerating the maturity of FLASH or any other widely available PMF design code will require enhanced collaboration across the PMF research community. Such enhanced collaboration has been recommended in the JASON study on low cost fusion development: “The National Laboratories should contribute their unclassified state-of-the-art simulation codes to collaborations with academic and commercial efforts, and support the training of qualified users" [[8](https://arxiv.org/html/2408.15206v1#bib.bib8)]. As a starting point, we recommend the community pursue the following, more limited collaborations and process improvements to rapidly benefit PMF simulation efforts.

Tabular material models for equation of state and transport coefficients, including magnetic resistivity, thermal conductivity, and single- and multi-group opacities, are known to have significant effect on the accuracy of the simulation results. These tables are maintained and controlled across a variety of institutions with a variety of access requirements and restrictions. Streamlining the processes for granting access to these tables while appropriately protecting the data and controlling their use would enhance the experimental relevance of the growing pulsed magnetic fusion simulation research effort.

Additionally, there exists an opportunity to accelerate open-code V&V efforts via focused collaborations between subject matter experts across the community. Similar scientific communities faced with comparable logistical complications have pursued a type of shared access development model for simulation and modeling abilities. This quasi open-sourced model seems to have accelerated the community’s computational abilities, as well as streamlined code verification and validation (V&V) [[58](https://arxiv.org/html/2408.15206v1#bib.bib58)] without duplicating efforts. We advocate enhanced avenues for collaboration on the following basic science research topics:

-
•
Identification of fruitful benchmark and validation problems for MHD and PMF

-
•
Best practices for linear solver settings for implicit diffusion equations (magnetic diffusion, radiation diffusion, thermal conduction) including preconditioner and solver settings

-
•
Treatments of floors and ceilings for densities and temperatures (e.g., vacuum density thresholds for magnetic resistivity)

-
•
Nominal algorithms and best settings for flux limited diffusion in the context of radiation diffusion and electron thermal conduction

-
•
Differencing algorithms for contact discontinuities (vacuum/conductor interfaces) and AMR refinement boundaries

-
•
Multispecies and multimaterial mixture rules for transport coefficients and EOS quantities spanning disparate parameter regimes (cold, solid to warm dense matter to weakly coupled plasma)

-
•
Development and identification of self-consistent EOS and transport coefficient tables


Active collaboration on these topics will accelerate PMF simulation research, both by disseminating existing knowledge and by activating a larger community of scientists to advance the state-of-the-art in modeling methodology. The high energy physics community has benefited from similar calls for enhanced knowledge transfer to leverage all available expertise in pursuit of mission-critical software advances [[58](https://arxiv.org/html/2408.15206v1#bib.bib58), [59](https://arxiv.org/html/2408.15206v1#bib.bib59)].

### 5.2 Power Flow and Pulser Design

Designing the PMF accelerator must include the impact of electrode plasmas created in the high power vacuum sections. The current delivered to the PMF load can be shunted by these plasmas. The state-of-the-art capability for the simulation of vacuum power flow in the accelerator has been demonstrated by the CHICAGO hybrid particle-in-cell (PIC) code.[[60](https://arxiv.org/html/2408.15206v1#bib.bib60)] CHICAGO permits high density and magnetic field plasma modeling with kinetic and/or fluid treatments[[61](https://arxiv.org/html/2408.15206v1#bib.bib61)]. The simulations include advanced surface physics and circuit modeling of upstream pulsed power components. Additionally, CHICAGO has demonstrated the ability to model the interaction of high-energy power-flow plasmas with PMF liners.[[62](https://arxiv.org/html/2408.15206v1#bib.bib62)] CHICAGO capabilities now enable modeling of the heating of solid-density liners by power-flow plasmas within a single integrated simulation. The simulations have been validated with detailed comparisons of simulated current loss with Z data (see Fig. [9](https://arxiv.org/html/2408.15206v1#S5.F9)).[[63](https://arxiv.org/html/2408.15206v1#bib.bib63)], [[64](https://arxiv.org/html/2408.15206v1#bib.bib64)] CHICAGO is currently being used to design next generation Z-pinch accelerators by LLNL, SNL and private companies.

[65](https://arxiv.org/html/2408.15206v1#bib.bib65)]

CHICAGO is a general-purpose three-dimensional (3D) fully-electromagnetic PIC code designed for executing multi-scale plasma physics and pulsed power component simulations. Advanced field solver techniques combined with multiple plasma models (quasi-neutral, inertial-fluid and fully-kinetic) allow CHICAGO to treat large spatial and temporal scale problems. Additionally, CHICAGO has detailed material models for designing of accelerator components.[[66](https://arxiv.org/html/2408.15206v1#bib.bib66)] CHICAGO is commercially available through Voss Scientific (https://www.vosssci.com/products/chicago) with various options including one for universities.

### 5.3 Advancing Technology Readiness Level

The theory of inertial fusion is as applicable to pulsed magnetic fusion as it is to laser-based fusion, and simulation capabilities are comparable with validated radiation-hydrodynamic models having similar experiment-driven pedigree.

DOE/NNSA is the organization to establish appropriate controls, including export controls, for data and simulation codes for this application space. We recommend that the PMFE community engage the NNSA laboratories to provide technical advice to DOE/NNSA on these controls. Agreements between national labs, industry, and academia that have been established in other domains may serve as a model. Similar to NIST data, publicly-funded unclassified tabular material data should be made publicly available when appropriate, with export controlled tables made available with appropriate restrictions. Cooperative Research and Development Agreements (CRADA) could be an appropriate venue for sharing models and data. Cost-sharing and a commitment to communicate model improvements to the laboratories could be made part of such agreements.

## 6 Diagnostics and measurement innovation

### 6.1 Overview

High yield and high rep-rate pulsed magnetic fusion systems require advances in diagnostic and data analysis methodologies. The two classes of facility outlined in Sec. [2](https://arxiv.org/html/2408.15206v1#S2) place different requirements on diagnostics and analysis. A single shot gain demonstration facility requires diagnostic systems that enable inference of key physical parameters, e.g. , and identification of failure mechanisms, allowing for the optimization of performance and gain. Such a facility will place a premium on diagnostic access during the design phase. In contrast, a rep-rate facility geared towards power generation will require fewer physics diagnostics to understand the details of target operation and will be more focused on facility operation and health.

Because the first step will be the construction and operation of a gain demonstrator at relatively low rep-rate for the purposes of establishing target operation and optimizing performance, we must consider the associated diagnostic requirements and how they will impact facility design. Nuclear diagnostics are needed to diagnose burn history, burn volume, yield, and temperature. Traditionally in ICF, x-ray diagnostics have proven valuable for understanding target performance, but x-rays require direct line of sight through vacuum to the target. This will inevitably impact the facility more than nuclear diagnostics, which can operate effectively in the presence of relatively thick, opaque windows. An additional consideration stems from the wide range of pressures and timescales accessible. As shown in Figs. [1](https://arxiv.org/html/2408.15206v1#S1.F1) and [5](https://arxiv.org/html/2408.15206v1#S4.F5), one facility and set of diagnostics may need to accommodate a wide range of pressures and burn durations that satisfy the condition, impacting instrument design. At the higher pressure regimes, technologies implemented on NIF/Z/OMEGA or upcoming through the NNSA National Diagnostic Working Group effort may be adaptable to this problem, but innovation is required for longer burn durations. Chamber diagnostics must operate reliably in the presence of high neutron yields ( MJ), which cause background radiation and activation of components and increase the risk of debris damage to electronics, optics, and other equipment.

Diagnostic access is a key design consideration for the pulser architecture, which affects the performance of the driver. These trade-offs with the facility design necessitate a quantitative means by which the value of an individual instrument can be weighed against its impact on the facility (performance, cost, schedule, etc.). This can be achieved through a system level model that integrates information from multiple diagnostics to make inferences about target performance. One can envision an optimization loop where diagnostics are included self-consistently with associated changes to the driver and the facility, target performance is simulated, and inferences are made from synthetic data. In this way, the information content of the instruments can be quantitatively weighed against their impact to the facility. Establishing this framework also conveniently establishes the models and tools needed to rapidly analyze and integrate diagnostic data post-shot to form a coherent picture of target performance, allowing rapid iteration and progress.

At high rep-rate, the diagnostic focus shifts from the target to the facility. System components must be monitored to ensure they are functioning properly. Monitoring the fusion chamber environment will also be critical so that an acceptable envelope of conditions can be maintained. Additionally, *in-situ* monitors for target tracking and other repetitive operational tasks are required. The real-time nature of these systems at high rep-rate invites the use of machine learning to allow the individual subsystems to adapt to changing inputs/outputs over time. For example, signals obtained from electrical components like capacitors and switches can be used to predict failure probabilities and flag items for replacement or isolation when probabilities grow unacceptably high. Research should be started immediately so that useful systems are available by the time the community is ready to build a commercial pilot plant.

### 6.2 Advancing Technology Readiness Level

Adaptation of existing diagnostic capabilities on flagship facilities (e.g. NIF, Z, OMEGA) will be key for developing next-generation PMFE facilities. Collaboration between national laboratories, universities, and private industry is needed to further advance diagnostic technologies and analysis methods. Research into diagnostic systems needed for a pulsed fusion pilot plant must begin immediately and has common challenges and TRL across IFE approaches; a new small-scale higher-repetition-rate pulser could benefit the PMF community specifically.

## 7 Chamber design and engineering

### 7.1 Overview

There are multiple facilities proposed in Section [2](https://arxiv.org/html/2408.15206v1#S2). They can be divided into two general classes. The first is single shot facilities for pulser and high gain platform development, national security or other missions that could benefit from intense radiation and fusion neutron fluxes. Examples include nuclear waste processing and tritium production. The second are rep-rated facilities, particularly those aimed at power generation, that need to fire at rates approaching 1 Hz with high average power, i.e., 100 MW. While there are no insurmountable hurdles, there are multiple engineering challenges to pulsed fusion energy systems, including[[67](https://arxiv.org/html/2408.15206v1#bib.bib67)]:

-
•
a tritium-producing blanket to replenish burnt, lost, and decayed inventory

-
•
a target chamber wall robust to high average power fusion product loading

-
•
rapid high gain target production and injection

-
•
rapid and sufficient clearing of the chamber to support continuous operations for up to 6 months


In the past few decades there have been fusion energy system studies that have addressed these issues for laser and ion beam driven fusion concepts. These include SOLACE, HYLIFE-II [[68](https://arxiv.org/html/2408.15206v1#bib.bib68)], LIFE [[69](https://arxiv.org/html/2408.15206v1#bib.bib69)], Z-IFE [[70](https://arxiv.org/html/2408.15206v1#bib.bib70), [71](https://arxiv.org/html/2408.15206v1#bib.bib71)], and similar studies for single shot applications for X-1 [[72](https://arxiv.org/html/2408.15206v1#bib.bib72)]. The most promising solutions devised in these studies will be reviewed using new computational tools and with modern material considerations for pulsed magnetic fusion systems.

For DT-based fusion systems, about 80% of the fusion energy released streams out of the fusion plasma in the form of 14 MeV neutrons. These pass easily through target materials and walls/hardware and are absorbed in a surrounding blanket. For pulsed fusion systems, be they laser- or pulser-based, much of the remaining energy from the alpha particles is deposited locally and vaporizes the target. The vaporized target radiates and expands into the surrounding chamber, which must be capable of withstanding the resulting thermal and mechanical loading.

In pulsed magnetic fusion systems the target is directly coupled to the pulser, which comes with two unique advantages. First, this reduces by two orders of magnitude the positioning requirements in rep-rate applications, i.e., mm scale positioning requirements for pulsed magnetic fusion systems compared to - positioning for NIF capsules. Second, the power flow hardware between the target and the vacuum chamber dielectric stack provides physical and optical protection of the insulators, thus avoiding the “direct exposure" problem of laser-based optics systems. Inline pressure-pulse baffling is also possible, since pulsed electrical energy can be made to follow curvilinear surfaces. Low-mass, low-cost magnetically insulated transmission lines (MITLs) designed to fully sublimate during the rising pulse need to be developed. These can be tested on single-shot pulsers, informed by modeling/simulation tools developed for power flow studies.

For all pulsed fusion power systems including pulsed magnetic fusion, safety, handling of radioactive byproducts, and efficient coupling of heat exchangers and balance of plant optimization are challenges the community faces. Pulsed magnetic fusion systems are, however, inherently shielded by the million gallon water insulated power delivery systems that deliver power to the vacuum region.

### 7.2 Advancing Technology Readiness Level

Aspects of chamber design, and development of appropriate first-wall materials, are common across IFE approaches and investment is needed to advance the TRL. Target injection, tracking, and engagement at reactor-compatible specifications is a commonality for IFE; PMFE has the advantage of operating at a relatively low repetition rate (e.g. Hz) with the unique aspect of electrically coupling to the target at reduced alignment tolerances versus laser-based approaches. Also, the upper and lower axial extents of the fusion target chamber are open allowing for significant access to the target region for target insertion equipment (targets can be launched through free space like in some concepts for laser-based IFE, but they can also be inserted with mechanical positioning equipment that remain attached to the target during fusion operation with no degradation of fusion performance). Inertial fusion requires minimizing the mass of vaporized material - testing of revolutionary low-mass concepts for PMFE is needed at existing academic-scale and publicly-funded facilities such as the Z Facility.

A key cost driver for techno-economic analysis is in cost scaling of key components, which can inform modern assessments of IFE concepts including PMF. Advanced cost optimization models and tools have been developed for tokamaks; investment in new reduced models is required so those tools may be applied to pulsed fusion systems to advance techno-economic analysis of reactor concepts.

## 8 Ensuring Long-term Intellectual Leadership

A critical factor in maintaining leadership in pulsed magnetic science and technology (PMS&T), including the area of pulsed magnetic fusion energy, is a dedicated initiative to train a new specialized workforce. This includes fusion engineers, pulser architects, target physicists, experimentalists, computational physicists, and precision fabricators. The ZNetUS program 222https://znetus.eng.ucsd.edu/ was launched in 2022 precisely for this purpose. ZNetUS represents a collaboration of experts from academic institutions, national laboratories, and the private sector, committed to advancing the fields of pulsed magnetic science, technology, and high-energy density physics for both energy and national security. The program’s central goal is to cultivate a diverse cadre of future scientific leaders.

ZNetUS’s mission encompasses the following objectives: i) organizing annual workshops, ii) managing a User Facilities Program, iii) coordinating a cross-institution transformational technologies development effort, and, iv) coordinating advanced code development activities to develop publicly accessible, high-impact simulation codes.

## 9 Conclusion and next steps

Pulsed magnetic fusion must be a key component of the fusion landscape to realize the U.S. bold decadal vision for fusion energy, as we believe it represents the most attractive path towards commercialization. Here, we have articulated a set of community-developed principles and our own bold vision to develop three major advances: the demonstration of facility gain () by the end of the decade, a subsequent commercial pilot plant, and a next-generation source for national security needs. Realizing this requires a vigorous program in the science and engineering of PMF. This program encompasses advanced pulser architectures, target physics, fabrication and experimental capabilities, simulations and modeling, diagnostic and measurement innovation, and energy system design and engineering. By building a community around this common vision for PMF and its supporting areas of science and engineering, we can achieve the bold vision laid out here. This document is therefore intended to advocate for PMF and begin organizing the community.

### 9.1 Summary of Recommendations

Year over year since the early 1990s pulsed magnetic ICF has received a factor of 5 to 10 less investment than laser-based ICF and tokamaks. Nonetheless, pulsed magnetic fusion has demonstrated P performance comparable with both approaches at similar facility scale, presenting the classic “innovator’s dilemma” [[73](https://arxiv.org/html/2408.15206v1#bib.bib73)].
Our view is that focused attention,
particularly to improving the distribution of resources within the publicly-funded fusion ecosystem, and focused investment to advance technology readiness level in the following areas will provide a similar rapid return on that investment.

-
•
Pulsed magnetic fusion power systems require maturation of pulser architectures that are capable of Hertz repetition rate, multi-million shot lifetimes, and production scale mass manufacturing.

-
•
Focused investment in high reliability energy storage and switching technologies capable of very high power (100 kV, 50+ kA) benefits all fusion approaches, including PMF.

-
•
Collaboration between fusion industry and national laboratories on target physics and innovative concepts is key to achieving high gain fusion and advancing the science of PMF.

-
•
Access to public-sector PMF facilities such as the Z Facility, which are presently the only ones capable of testing relevant-scale target physics concepts, would advance innovation.

-
•
DOE/NNSA is the organization to establish appropriate controls, including export controls, for data and simulation codes for this application space. Agreements between national labs, industry, and academia that have been established in other domains may serve as a model.

-
•
Similar to NIST data, publicly-funded unclassified tabular material data should be made publicly available, with export controlled tables made available with appropriate restrictions. CRADA could be an appropriate venue for exchanging models and data, potentially including cost-sharing and a commitment to share model improvements with the NNSA laboratories.

-
•
National laboratories, universities, and private industry should collaborate to advance diagnostic technologies and analysis methods.

-
•
Research into diagnostic systems needed for a pulsed fusion pilot plant must begin immediately and could include a new small-scale higher-repetition-rate pulser.

-
•
Technological challenges in materials and chamber design have significant commonality across fusion approaches and advances are needed that will benefit PMFE.

-
•
Inertial fusion requires minimizing the mass of vaporized material: testing of revolutionary low-mass concepts is needed at existing academic-scale and publicly-funded facilities such as the Z Facility.

-
•
Cost optimization tools developed for tokamaks require investment in new reduced models so those tools may be applied to pulsed fusion systems.

-
•
Academic-scale programs such as ZNetUS and publicly-funded facilities should be supported and made accessible to industry for long-term intellectual leadership and community growth.


## 10 Acknowledgments

We thank F. Beg, N. Nardelli, D. Rose, K. Peterson, and K. Raman, for review of the manuscript, and S. Davidson for contributions to Fig. [8](https://arxiv.org/html/2408.15206v1#S5.F8).

This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. This article has been authored by an employee of National Technology & Engineering Solutions of Sandia, LLC under Contract No. DE-NA0003525 with the U.S. Department of Energy (DOE). This paper describes objective technical results and analysis. The views and opinions expressed in this paper represents the individual views of the authors and do not necessarily represent the views of any of the affiliated national laboratories, U.S. Department of Energy or the United States Government. This work was supported by the U.S. Department of Energy through the Los Alamos National Laboratory. Los Alamos National Laboratory is operated by Triad National Security, LLC, for the National Nuclear Security Administration of U.S. Department of Energy (Contract No. 89233218CNA000001). The Flash Center for Computational Science acknowledges support by the U.S. Department of Energy National Nuclear Security Administration under Award Numbers DE-NA0003856, DE-NA0003842, DE-NA0004144, and DE-NA0004147, under subcontracts no. 536203 and 630138 with Los Alamos National Laboratory, and under subcontract B632670 with Lawrence Livermore National Laboratory. We also acknowledge support from the U.S. Department of Energy Advanced Research Projects Agency-Energy under Award Number DE-AR0001272 and the U.S. Department of Energy Office of Science under Award Number DE-SC0023246.

## References

- [1] Statistical review of world energy 2023 72nd edition. Technical report, Energy Institute, 2023.
- [2] B.N. Sorbom, J. Ball, T.R. Palmer, F.J. Mangiarotti, J.M. Sierchio, P. Bonoli, C. Kasten, D.A. Sutherland, H.S. Barnard, C.B. Haakonsen, J. Goh, C. Sung, and D.G. Whyte. Arc: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets. Fusion Engineering and Design, 100:378–405, 2015.
- [3] H. Abu-Shawareb et al. Lawson criterion for ignition exceeded in an inertial fusion experiment. Phys. Rev. Lett., 129:075001, Aug 2022.
- [4] H. Abu-Shawareb et al. Achievement of target gain larger than unity in an inertial fusion experiment. Phys. Rev. Lett., 132:065102, Feb 2024.
- [5] Samuel E. Wurzel and Scott C. Hsu. Progress toward fusion energy breakeven and gain as measured against the Lawson criterion. Physics of Plasmas, 29(6):062103, 06 2022.
- [6] P. F. Knapp et al. Estimation of stagnation performance metrics in magnetized liner inertial fusion experiments using Bayesian data assimilation. Phys. Plasmas, 29(5):052711, 05 2022.
- [7] White House Office of Science and Technology Policy. Readout of the White House Summit on Developing a Bold Decadal Vision for Commercial Fusion Energy, 2022. https://www.whitehouse.gov/ostp/news-updates/2022/04/19/readout-of-the-white-house-summit-on-developing-a-bold-decadal-vision-for-commercial-fusion-energy/.
- [8] JASON Report. Prospects for Low Cost Fusion Development. 2018.
- [9] Science for America. New Opportunities in Fusion Power. 2023.
- [10] NNSA. Fiscal Year 2024 Stockpile Stewardship and Management Plan. November 2023.
- [11] DB Sinars et al. Review of pulsed power-driven high energy density physics research on Z at Sandia. Phys. Plasmas, 27(7), 2020.
- [12] Basic research needs workshop on inertial fusion energy: Report of the fusion energy sciences workshop. Technical report, Dept. of Energy, Office of Science, Fusion Energy Sciences, 2023.
- [13] William A Stygar et al. Architecture of petawatt-class z-pinch accelerators. Physical Review Special Topics-Accelerators and Beams, 10(3):030401, 2007.
- [14] WA Stygar et al. Conceptual designs of two petawatt-class pulsed-power accelerators for high-energy-density-physics experiments. Physical Review Special Topics-Accelerators and Beams, 18(11):110401, 2015.
- [15] W Stygar et al. Conceptual design of a 960-TW accelerator powered by impedance-matched Marx generators. In 2017 IEEE 21st International Conference on Pulsed Power (PPC), pages 1–8. IEEE, 2017.
- [16] WA Stygar et al. Impedance-matched marx generators. Physical Review Accelerators and Beams, 20(4):040402, 2017.
- [17] KR LeChien et al. Sirius I: prototype of a prime-power source for future 1-10 GJ fusion-yield experiments. Technical report, Lawrence Livermore National Lab.(LLNL), Livermore, CA (United States), 2023.
- [18] S. A. Slutz et al. Scaling magnetized liner inertial fusion on Z and future pulsed-power accelerators. Phys. Plasmas, 23(2):022702, 02 2016.
- [19] S. A. Slutz and R. A. Vesey. High-gain magnetized inertial fusion. Phys. Rev. Lett., 108:025003, Jan 2012.
- [20] OA Hurricane, PK Patel, R Betti, DH Froula, SP Regan, SA Slutz, MR Gomez, and MA Sweeney. Physics principles of inertial confinement fusion and us program overview. Reviews of Modern Physics, 95(2):025005, 2023.
- [21] M.M. Basko, A.J. Kemp, and J. Meyer ter Vehn. Ignition conditions for magnetized target fusion in cylindrical geometry. Nuclear Fusion, 40(1):59, 2000.
- [22] John Lindl. Development of the indirect-drive approach to inertial confinement fusion and the target physics basis for ignition and gain. Phys. Plasmas, 2(11):3933–4024, 1995.
- [23] D. E. Ruiz et al. Exploring the parameter space of MagLIF implosions using similarity scaling. II. Current scaling. Phys. Plasmas, 30(3):032708, 2023.
- [24] CA Williams et al. Demonstration of hot-spot fuel gain exceeding unity in direct-drive inertial confinement fusion implosions. Nature Physics, pages 1–7, 2024.
- [25] P. F. Schmit and D. E. Ruiz. A conservative approach to scaling magneto-inertial fusion concepts to larger pulsed-power drivers. Physics of Plasmas, 27(6):062707, 06 2020.
- [26] D. E. Ruiz, P. F. Schmit, D. A. Yager-Elorriaga, C. A. Jennings, and K. Beckwith. Exploring the parameter space of MagLIF implosions using similarity scaling. I. Theoretical framework. Physics of Plasmas, 30(3):032707, 03 2023.
- [27] D.E. Ruiz et al. Similarity scaling MagLIF loads to achieve high fusion yields (200 MJ) in the laboratory, 12th International Conference on Inertial Fusion Sciences and Applications, Denver, CO. 2023.
- [28] A. L. Kritcher et al. Design of the first fusion experiment to achieve target energy gain . Phys. Rev. E, 109:025204, Feb 2024.
- [29] M. M. Marinak et al. How Numerical Simulations Helped to Achieve Breakeven on the NIF. Phys. Plasmas. submitted.
- [30] S. A. Slutz et al. Enhancing performance of magnetized liner inertial fusion at the Z facility. Phys. Plasmas, 25(11):112706, 11 2018.
- [31] D. B. Sinars et al. Measurements of Magneto-Rayleigh-Taylor Instability Growth during the Implosion of Initially Solid Al Tubes Driven by the 20-MA, 100-ns Z Facility. Phys. Rev. Lett., 105:185001, Oct 2010.
- [32] D. B. Sinars, S. A. Slutz, M. C. Herrmann, R. D. McBride, M. E. Cuneo, C. A. Jennings, J. P. Chittenden, A. L. Velikovich, K. J. Peterson, R. A. Vesey, C. Nakhleh, E. M. Waisman, B. E. Blue, K. Killebrew, D. Schroen, K. Tomlinson, A. D. Edens, M. R. Lopez, I. C. Smith, J. Shores, V. Bigman, G. R. Bennett, B. W. Atherton, M. Savage, W. A. Stygar, G. T. Leifeste, and J. L. Porter. Measurements of magneto-Rayleigh–Taylor instability growth during the implosion of initially solid metal liners. Phys. Plasmas, 18(5):056301, 04 2011.
- [33] D. E. Ruiz et al. Harmonic Generation and Inverse Cascade in the z-Pinch Driven, Preseeded Multimode, Magneto-Rayleigh-Taylor Instability. Phys. Rev. Lett., 128:255001, Jun 2022.
- [34] T. J. Awe et al. Experimental demonstration of the stabilizing effect of dielectric coatings on magnetically accelerated imploding metallic liners. Phys. Rev. Lett., 116:065001, Feb 2016.
- [35] P. F. Knapp et al. Direct measurement of the inertial confinement time in a magnetically driven implosion. Phys. Plasmas, 24(4):042708, 04 2017.
- [36] P. F. Knapp, M. R. Martin, D. Yager-Elorriaga, A. J. Porwitzky, F. W. Doss, G. A. Shipley, C. A. Jennings, D. E. Ruiz, T. Byvank, C. C. Kuranz, C. E. Myers, D. H. Dolan, K. Cochrane, M. Schollmeier, I. C. Smith, T. R. Mattsson, B. M. Jones, K. Peterson, J. Schwarz, R. D. McBride, D. G. Flicker, and D. B. Sinars. A novel, magnetically driven convergent Richtmyer–Meshkov platform. Phys. Plasmas, 27(9):092707, 09 2020.
- [37] K. J. Peterson et al. Simulations of electrothermal instability growth in solid aluminum rodsa). Phys. Plasmas, 20(5):056305, 04 2013.
- [38] B. Fryxell et al. FLASH: An adaptive mesh hydrodynamics code for modeling astrophysical thermonuclear flashes. Astrophys. J. Suppl. Ser., 131(1):273–334, nov 2000.
- [39] P. Tzeferacos et al. FLASH MHD simulations of experiments that study shock-generated magnetic fields. High Energy Density Phys., 17, Part A:24–31, 2015.
- [40] Dongwook Lee. A solution accurate, efficient and stable unsplit staggered mesh scheme for three dimensional magnetohydrodynamics. J. Computat. Phys., 243:269–292, jun 2013.
- [41] Jeong-Young Ji and Eric D. Held. Closure and transport theory for high-collisionality electron-ion plasmas. Phys. Plasmas, 20(4):042114, 2013.
- [42] J. R. Davies, H. Wen, Jeong-Young Ji, and Eric D. Held. Transport coefficients for magnetic-field evolution in inviscid magnetohydrodynamics. Phys. Plasmas, 28(1):012305, 2021.
- [43] P Tzeferacos et al. Numerical modeling of laser-driven experiments aiming to demonstrate magnetic field amplification via turbulent dynamo. Phys. Plasmas, 24(4):041404, 2017.
- [44] Milad Fatenejad, B. Fryxell, J. Wohlbier, E. Myra, D. Lamb, C. Fryer, and C. Graziani. Collaborative comparison of simulation codes for high-energy-density physics applications. High Energy Density Phys., 9(1):63–66, 2013.
- [45] Chris Orban, Milad Fatenejad, and Donald Q. Lamb. Code-to-code comparison and validation of the radiation-hydrodynamics capabilities of the FLASH code using a laboratory astrophysical jet. Phys. Plasmas, 29(5):053901, 05 2022.
- [46] J. P. Sauppe, Y. Lu, P. Tzeferacos, A. C. Reyes, S. Palaniyappan, K. A. Flippo, S. Li, and J. L. Kline. On the importance of three-dimensional modeling for high-energy-density physics experiments. Phys. Plasmas, 30(6):062707, 06 2023.
- [47] Katerina Falk, E. J. Gamboa, G. Kagan, D. S. Montgomery, B. Srinivasan, P. Tzeferacos, and J. F. Benage. Equation of state measurements of warm dense carbon using laser-driven shock and release technique. Phys. Rev. Lett., 112(15):155003, 2014.
- [48] R Yurchak et al. Experimental demonstration of an inertial collimation mechanism in nested outflows. Phys. Rev. Lett., 112(15):155001, 2014.
- [49] Jena Meinecke et al. Developed turbulence and nonlinear amplification of magnetic fields in laboratory and astrophysical plasmas. Proc. Natl. Acad. Sci. U. S. A., 112(27):8211–8215, 2015.
- [50] C. K. Li et al. Scaled laboratory experiments explain the kink behaviour of the Crab Nebula jet. Nat. Commun., 7(1):1–8, 2016.
- [51] P. Tzeferacos et al. Laboratory evidence of dynamo amplification of magnetic fields in a turbulent plasma. Nat. Commun., 9(1):1–8, 2018.
- [52] A Rigby et al. Electron acceleration by wave turbulence in a magnetized plasma. Nat. Physics, 14(5):475–479, 2018.
- [53] T. G. White et al. Supersonic plasma turbulence in the laboratory. Nat. Commun., 10(1):1–6, 2019.
- [54] J Meinecke et al. Strong suppression of heat conduction in a laboratory replica of galaxy-cluster turbulent plasmas. Science Advances, 8(10):eabj6799, 2022.
- [55] Stephen A. Slutz, Melissa R. Douglas, Joel S. Lash, Roger A. Vesey, Gordon A. Chandler, Thomas J. Nash, and Mark S. Derzon. Scaling and optimization of the radiation temperature in dynamic hohlraums. Phys. Plasmas, 8(5):1673–1691, 2001.
- [56] Nathan M. Cook, Johan Carlsson, Paul Moeller, Rob Nagler, and Petros Tzeferacos. Modeling of capillary discharge plasmas for wakefield acceleration and beam transport. J. Phys.: Conf. Ser., 1596(1):012063, 2020.
- [57] F. Conti et al. MA-class linear transformer driver for Z-pinch research. Phys. Rev. Accelerators and Beams, 23(9):090401, 2020.
- [58] The HEP Software Foundation et al. A roadmap for hep software and computing r&d for the 2020s. Computing and Software for Big Science, 3(1):7, 2019.
- [59] Benjamin Couturier et al. HEP Software Foundation Community White Paper Working Group - Software Development, Deployment and Validation. Technical report, 2017.
- [60] Dale R Welch, Nichelle L Bennett, Thomas C Genoni, David V Rose, Carsten Thoma, Craig Miller, and William A Stygar. Electrode contaminant plasma effects in 107-a z pinch accelerators. Physics of Accelerators and Beams, 22(070401), 2019.
- [61] Dale R Welch, Nichelle L Bennett, Thomas C Genoni, Carsten Thoma, and David V Rose. Fast hybrid particle-in-cell technique for pulsed-power accelerators. Physics of Accelerators and Beams, 23(110401), 2020.
- [62] Kurt Tummel, Dale R Welch, David V Rose, Anthony J Link, and Keith R LeChien. Impact of power flow on z-pinch loads. Physics of Plasmas, 29(113102), 2022.
- [63] Nichelle Bennett, Dale R Welch, Christopher A Jennings, Edmund Yu, Michael H Hess, Brian T Hutsel, George Laity, J K Moore, David V Rpse, Kyle Peterson, and Michael E Cuneo. Current transport and loss mechanisms in the z accelerator. Physics of Accelerators and Beams, 23(120401), 2019.
- [64] Nichelle L Bennett, Dale R Welch, Christopher A Jennings, Edmund Yu, Michael H Hess, Brian T Hutsel, George Laity, J K Moore, David V Rose, Kyle Peterson, and Michael E Cuneo. Magnetized particle transport in multi-ma accelerators. Physics of Accelerators and Beams, 24(060401), 2021.
- [65] N. Bennett, Derek Lamppa, Andrew Porwitzky, Christopher Jennings, Dale Welch, Evstati Evstatiev, Clayton Myers, Kathy Chandler, Jacob Banecek, Sonal Patel, Eric Watson, David Yager-Elorriaga, Mark Savage, Mark Johnston, Mark Hess, David Rose, and Michael Cuneo. Mrt 7365: Power flow physics and key physics phenomena. Technical Report SAND2023-nnnn, Sandia National Laboratories, 2023.
- [66] Carsten Thoma, Dale R Welch, Alexander m Russell, Robert E Clark, David V Rose, William A Styger, and B J Kelsall. Three-dimensional time-domain particle-in-cell calculations of impedances and centroid deflections in a linear-accelerator cell. Physics of Accelerators and Beams, 26(014602), 2023.
- [67] Ehud Greenspan. Fusion reactors blanket nucleonics. Progress in Nuclear Energy, 17(1):53–139, 1986.
- [68] RW Moir et al. HYLIFE-II: A molten-salt inertial fusion energy power plant design. Fusion technology, 25(1):5–25, 1994.
- [69] J F Latkowski et al. Chamber design for the laser inertial fusion energy (life) engine. Fusion Science and Technology, 60(1):54–60, 2011.
- [70] W Meier, R Abbott, J Latkowski, R Moir, S Reyes, and R Schmitt. Analyses in support of Z-IFE: LLNL progress report for FY-04. Technical report, Lawrence Livermore National Lab.(LLNL), Livermore, CA (United States), 2004.
- [71] Wayne R Meier. Systems modeling for Z-IFE power plants. Fusion science and technology, 52(4):948–952, 2007.
- [72] RR Peterson et al. X-1 experiment chamber design and analysis: Progress report for the period august 1, 1998 to september 30, 1998. 1998.
- [73] Clayton Christenson. The innovator’s dilemma. Harvard Business School Press, Cambridge, Mass, 1997.