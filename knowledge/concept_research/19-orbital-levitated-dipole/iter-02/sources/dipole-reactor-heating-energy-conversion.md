---
source: "https://arxiv.org/html/2602.20564"
source_type: "url"
extracted_at: "2026-03-29T20:13:06.012582+00:00"
content_hash_sha256: "719316805637e9c39b96d8febfae50a00937cfe1fb8b8dacfe363610e411c5fa"
backend: "trafilatura"
title: "Deuterium–Tritium Levitated Dipole Fusion Power Plants"
author: "T Simpson tom simpson nz"
---

# Deuterium–Tritium Levitated Dipole Fusion Power Plants

###### Abstract

Levitated dipole reactors offer an attractive path towards economic fusion power generation. The intrinsic decoupling of the confining magnetic field-generating REBCO magnets and the vacuum vessel offer unparalleled accessibility and maintainability, allowing for high plant duty factors and theoretically low electricity prices. In order to achieve rapid deployment of fusion power to the grid, the use of the Deuterium-Tritium (DT) fuel cycle is required due to its lower required plasma triple products. Historically, designs of levitated dipole fusion power plants have targeted advanced fuels as a DT device was seen to be infeasible due to the high fluxes of MeV neutrons on the superconducting core magnet. This study presents high level designs for two feasible first-of-a-kind (FOAK) DT levitated dipole fusion power plants, the larger of which produces MW of fusion power and is predicted to produce MW of net electric power. Both designs consist of a heavily neutron-shielded, high-field REBCO core magnet capable of producing peak magnetic field strengths of T while keeping peak mechanical strains below %. The neutron shielding is comprised of a layered structure of tungsten and boron carbide, which allows for % of the heat deposited in the neutron shield to be radiated out to the first wall while still providing sufficient neutron attenuation to give adequate REBCO conductor lifetimes. The core magnet REBCO coil is comprised of a small “sacrificial” section and a larger semi-permanent section. The sacrificial section, comprising of the coil, will have a neutron damage limited lifetime of year, after which the core magnet will be quickly removed from the vacuum vessel and replaced. This allows the damaged core magnet to be refurbished and reused, reducing cost and allowing for economic fusion power generation from a DT levitated dipole reactor.

###### keywords:

Levitated Dipole, Fusion power plants, Fusion reactor study, Neutron Shielding, High magnetic field, Magnet Optimization, Magnet replacement†

†journal: Fusion Engineering and Design

[openstar]organization=OpenStar Technologies Limited, addressline=20 Glover Street, Ngauranga, city=Wellington, postcode=6035, country=New Zealand

## 1 Introduction

The need for a scalable base load power generation source has been identified as a key requirement for addressing climate change and the rapid growth of global energy demands Intergovernmental Panel On Climate Change [[2023](https://arxiv.org/html/2602.20564v1#bib.bib45)], Wolfram et al. [[2012](https://arxiv.org/html/2602.20564v1#bib.bib46)], Mauleón [[2022](https://arxiv.org/html/2602.20564v1#bib.bib47)], de Vries [[2023](https://arxiv.org/html/2602.20564v1#bib.bib48)]. Fusion offers unparalleled scalability due to the energy density and abundance of Deuterium. However, to make a significant impact in the global energy market, the roll out of early fusion power plants will need to be rapid, which requires competitive energy prices. Recent studies into the economics of a fusion power plant Maris et al. [[2024](https://arxiv.org/html/2602.20564v1#bib.bib44)] show that plasma disruptions pose a major risk of raising the price of electricity, highlighting the benefit of disruption-free configurations. Additionally, the large external coils required for tokamaks and stellarators makes maintenance intrinsically difficult — usually requiring the complete or partial disassembly of the reactor Sorbom and others [[2015](https://arxiv.org/html/2602.20564v1#bib.bib43)], Rutherford and others [[2024](https://arxiv.org/html/2602.20564v1#bib.bib42)], Lion and others [[2025](https://arxiv.org/html/2602.20564v1#bib.bib41)] — impacting plant availability and resulting in an increased price of electricity. Commercial fusion power plants will need to treat accessibility and maintainability as a priority.

First proposed by Akira Hasegawa in 1987 after early observations of planetary magnetospheres Hasegawa [[1987](https://arxiv.org/html/2602.20564v1#bib.bib19)], levitated dipoles benefit from favorable physics and engineering properties that merit their investigation as fusion power plants. Although subsequent levitated dipole experiments have replicated many of the attractive features of these plasmas in a laboratory setting Boxer et al. [[2010](https://arxiv.org/html/2602.20564v1#bib.bib11)], Saitoh et al. [[2011](https://arxiv.org/html/2602.20564v1#bib.bib32)], Goto et al. [[2006](https://arxiv.org/html/2602.20564v1#bib.bib88)], little research has been carried out on their performance as fusion energy devices. Levitated dipoles are characterized by a single plasma confining superconducting coil, the ‘core magnet’, levitated in the center of a large vacuum vessel as shown in Fig. [1](https://arxiv.org/html/2602.20564v1#S1.F1). The levitation force and position control is provided by relatively weak poloidal field coils mounted outside of the inner vacuum vessel. In the simplest case, which we assume in this study, there will only be one external poloidal field coil which we name the ‘top magnet’. This configuration of magnets and vacuum vessel does not require any complex interlocking of components, allowing for a level of access and maintainability unique among magnetically confined fusion devices. Hence, the maintenance, replacement, and iteration of key components, such as the core magnet, vacuum vessel, and tritium breeding blanket can be fast and completed with simpler robotic systems than possible in other fusion concepts.

Operating a superconducting coil in the core plasma region introduces engineering challenges that must be accounted for in a commercial device. Previous studies have attempted to mitigate these challenges by focusing primarily on reactors using advanced fuel cycles Hasegawa et al. [[1990](https://arxiv.org/html/2602.20564v1#bib.bib21)], Kesner et al. [[2003](https://arxiv.org/html/2602.20564v1#bib.bib24)]. However, the order of magnitude increase in the required triple product to reach ignition compared to the deuterium–tritium (DT) fuel cycle places demanding requirements on the plasma performance, increasing the size of the device beyond what would be acceptable for a first-of-a-kind (FOAK) fusion power plant. Therefore, this study focuses on the design of levitated dipole reactors using the DT fuel cycle and tackles the key challenges introduced by the high flux of MeV neutrons. In this study we show that the use of a DT fuel cycle allows for levitated dipole reactors with smaller magnetic systems than comparable fusion power output tokamaks, as shown in Fig. [2](https://arxiv.org/html/2602.20564v1#S1.F2). This in turn can be leveraged along with the inherent accessibility to allow for appealing power plant economics.

The structure of this study aims to offer a concise introduction to the aspects of a levitated dipole reactor that differ from other magnetically confined fusion concepts. Section [2](https://arxiv.org/html/2602.20564v1#S2) discusses the equilibrium and stability of the dipole plasma and details the engineering of a levitated dipole reactor and the considerations necessary to satisfy the requirements of a viable FOAK fusion power plant. Section [3](https://arxiv.org/html/2602.20564v1#S3) describes the workflow and optimizer used to find viable operating points. This work presents for the first time a dipole magnet design that has been optimized for fusion performance within demonstrated engineering limits Hartwig and others [[2024](https://arxiv.org/html/2602.20564v1#bib.bib18)]. Section [4](https://arxiv.org/html/2602.20564v1#S4) then presents two design points and provides an analysis of key parameters.

## 2 Design Principles

### 2.1 Dipole Physics Basis

The levitated dipole mimics the plasma confinement of planetary magnetospheres, where a dipole magnetic field creates the environment for stable, steady state, and centrally peaked plasmas Schulz and Lanzerotti [[1974](https://arxiv.org/html/2602.20564v1#bib.bib69)], Lyon [[2000](https://arxiv.org/html/2602.20564v1#bib.bib66)], Birmingham [[1969](https://arxiv.org/html/2602.20564v1#bib.bib67)], Fälthammar [[1965](https://arxiv.org/html/2602.20564v1#bib.bib68)]. The key difference in a levitated dipole is, as the name suggests, the levitation of the core magnet. Removing the physical supports creates a region of closed flux surfaces and eliminates plasma losses along field-lines. Therefore, the plasma in a levitated dipole forms in this region of closed flux surfaces between the core magnet and the limiting vacuum vessel, and its equilibrium is governed by the reduced (toroidal-field-free) Grad-Shafranov equation Garnier et al. [[1999](https://arxiv.org/html/2602.20564v1#bib.bib14)]. Therefore unlike most magnetically confined plasmas there is both a last closed flux surface, , created by either a limiter on the vacuum vessel or a separatrix, and a first closed flux surface, , caused by the plasma limiting on the core magnet. Between these surfaces lies a single pressure peak located at the flux surface denoted by . Another key difference is that particles orbiting interior to travel in a region of absolute good curvature, denoted by , and those orbiting beyond do so in a region of absolute bad curvature, denoted by . The plasma in a levitated dipole can either be diverted or limited anywhere around , with the outer midplane offering the lowest wall loadings. In this work, we have elected to study a dipole configuration that is limited on the outer midplane. This merely serves as a test of feasibility and future designs will focus on diverted dipole plasmas.

Fundamentally, the core magnet and some form of plasma heating are all that is required to create a fusion plasma with a levitated dipole. Therefore, any particular levitated dipole design can be primarily characterized by four parameters: the major radius of the core magnet coil, ; the core magnet coil aspect ratio, , with the core magnet minor radius; the total core magnet current, ; and the effective plasma aspect ratio, , defined using the ratio of the differential flux tube volumes at and , respectively. As we show in Section [2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1), the plasma aspect ratio is the key factor that drives the peaked pressure profiles required for fusion.

#### 2.1.1 Equilibrium and Stability

Theory has predicted Rosenbluth and Longmire [[1957](https://arxiv.org/html/2602.20564v1#bib.bib31)], Hasegawa [[1987](https://arxiv.org/html/2602.20564v1#bib.bib19)] and observations have shown Boxer et al. [[2010](https://arxiv.org/html/2602.20564v1#bib.bib11)], Yoshida et al. [[2010](https://arxiv.org/html/2602.20564v1#bib.bib65)] that in a levitated dipole plasma equilibrium, an example of which is given in Fig [3](https://arxiv.org/html/2602.20564v1#S1.F3), is achieved at the limit of marginal stability to interchange modes:

| (1) |

where and are the differential flux tube volume and plasma pressure, respectively. This results in a critical pressure gradient:

| (2) |

which defines the MHD stability limit and, when exceeded, results in the formation of large scale convective cells that act to transport energy out to the last closed flux surface Kesner and Garnier [[2000](https://arxiv.org/html/2602.20564v1#bib.bib61)], Rey and Hassam [[2001](https://arxiv.org/html/2602.20564v1#bib.bib64)], Hassam and Kulsrud [[1979](https://arxiv.org/html/2602.20564v1#bib.bib63)], Shukla et al. [[1984](https://arxiv.org/html/2602.20564v1#bib.bib62)]. Convective cells can also form in a marginally stable profile which act to transport particles to and from the core without the net transport of energy Pastukhov and Sokolov [[1992](https://arxiv.org/html/2602.20564v1#bib.bib96)]. Therefore, in a levitated dipole where this results in the following scaling of the peak plasma pressure:

| (3) |

which heavily incentivizes the use of a relatively small magnet in a large vacuum chamber. A similar critical gradient for the temperature and density can also be obtained:

| (4) |

which describes the stability to drift frequency “entropy” modes Kesner [[2000](https://arxiv.org/html/2602.20564v1#bib.bib23)], Kesner and Hastie [[2002](https://arxiv.org/html/2602.20564v1#bib.bib70)], Simakov et al. [[2001](https://arxiv.org/html/2602.20564v1#bib.bib71)] and is valid for arbitrary plasma Simakov et al. [[2002](https://arxiv.org/html/2602.20564v1#bib.bib72)]. It has been shown in pellet injection experiments Garnier et al. [[2017](https://arxiv.org/html/2602.20564v1#bib.bib17)] that changing the density gradient will lead to either an outward particle flux when or an inward particle flux when which act to return the system to the profile.

#### 2.1.2 Pressure Peak Location

In steady state the pressure peak, , is the point that allows for power balance to be achieved in both the good and bad curvature regions of the plasma. The transport in has been characterized to some extent Boxer et al. [[2010](https://arxiv.org/html/2602.20564v1#bib.bib11)], Garnier et al. [[2017](https://arxiv.org/html/2602.20564v1#bib.bib17)], however, the transport at the plasma edges and in is unknown. The lack of degrading modes in suggests that the transport in this region could approach classical, allowing for very steep temperature and density gradients. However, the prompt particle losses will eventually dominate at a distance proportional to the Larmor radii of the energetic particles. The low magnetic field strengths at the outboard side of the core magnet result in prompt particle losses becoming the practical limit on the location of . The plasma equilibria in this study have located at the prompt loss limit. Determining whether or not defining in this way would result in a self-consistent equilibrium requires knowledge of the energy transport in . This particular problem is out of the scope of this study and will be a focus of future levitated dipole experiments. Furthermore, we assume the heat conducted to to be negligible () requiring all heat deposited in to be radiated away Kesner and Mauel [[1997](https://arxiv.org/html/2602.20564v1#bib.bib95)], Pastukhov and Sokolov [[1992](https://arxiv.org/html/2602.20564v1#bib.bib96)].

#### 2.1.3 Limit

Due to the extremely peaked nature of the pressure profile as shown in Fig. [3](https://arxiv.org/html/2602.20564v1#S1.F3), it is useful to quantify both the global :

| (5) |

where the average is taken over the plasma volume, and the local at the low field side pressure peak:

| (6) |

has to be finite in order to confine the plasma, which for a particular equilibrium solution will translate to an equivalent limit on . A more practical limit on is a result of the plasma expansion that follows increasing , which results in an outwards movement of the poloidal flux lines. This effect can be seen by comparing the low and high equilibria in Fig. [3](https://arxiv.org/html/2602.20564v1#S1.F3)(c). Fig. [3](https://arxiv.org/html/2602.20564v1#S1.F3)(d) then shows the evolution of the fusion power as a function of . As is increased the plasma pressure increases initially, however beyond a certain point the expansion results in a reduction of the peak pressure at the core according to Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)). This peak typically happens around values of . However, the total stored energy in the plasma is still increasing at these values of , which causes the fusion power to peak at a higher value of , in the range of for many reactor configurations.

#### 2.1.4 Plasma Edge Conditions

Following on from Eq. ([1](https://arxiv.org/html/2602.20564v1#S2.E1)), the pressure in the plasma core is determined by both the device aspect ratio, , as in Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)) and the pressure at , denoted as . For a given core pressure, , higher values of will allow for smaller vacuum vessels in proportion with Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)), reducing the overall cost of the plant. Hence there is an incentive to design reactors with the highest possible edge pressures.

The physics defining an upper bound on the value of is not well understood as no dipole experiments have yet had enough heating power to generate edge conditions applicable to fusion power plants. However, gyrokinetic simulations have shown promising results for zonal flow formation in certain collisionality regimes Ricci et al. [[2006](https://arxiv.org/html/2602.20564v1#bib.bib30)], Kobayashi et al. [[2009](https://arxiv.org/html/2602.20564v1#bib.bib25)], Hoffmann et al. [[2023](https://arxiv.org/html/2602.20564v1#bib.bib22)], suggesting the possibility of edge or internal transport barrier formation. It is also believed that ambipolarity due to preferential scrape-off of the large gyro radius ions near the plasma edge could result in shear flows which in turn could lead to edge pedestal formation. As such, for the purpose of this study we have assumed that pedestal-like edge conditions are possible Terry et al. [[2007](https://arxiv.org/html/2602.20564v1#bib.bib60)], Whyte and others [[2010](https://arxiv.org/html/2602.20564v1#bib.bib59)] and that plasma values at the plasma edge, denoted as , are taken to be the values at the pedestal. The presence of an edge pedestal will be confirmed with results from a fusion relevant levitated dipole device.

For this study we are considering an equilibrium limited on the outboard midplane. We do not expect this configuration to be able to create the edge conditions discussed in this section, however, this should not affect the engineering of the remaining reactor components. We anticipate that the higher performance assumed above will be achievable by adding shaping coils and diverting the equilibrium, the details of which are left for a future study.

#### 2.1.5 Energy Confinement Time

The goal of this study is to show the viability of a levitated dipole fusion power plant. Part of this analysis involves modeling the required auxiliary heating power and its effect on the overall power balance. This in turn requires the notion of an energy confinement time which is typically extrapolated from experimental data Luce et al. [[2008](https://arxiv.org/html/2602.20564v1#bib.bib89)]. In this case, attempting to scale the energy confinement time from existing levitated dipoles would be counterproductive as the large difference in device scale required for a reactor will lead to unacceptable errors in the predicted performance. In lieu of experimental data, this study takes the reverse approach of assuming a confinement time for a reactor and then using Bohm-like and gyro-Bohm-like scaling to generate performance requirements for a small scale demonstration device.

However, it is worth noting the differences in the construction of the confinement time in relation to those used by tokamaks and stellarators. The conductive losses in a levitated dipole are characterized by losses inwards towards the first closed flux surface, , and losses out towards the last closed flux surface, . In a levitated dipole, both mechanisms would contribute their own energy confinement time which could then be combined to reconstruct a global energy confinement time. However, due to the good curvature confinement in we expect the transport to approach classical limits. Therefore, we also expect losses out to the last closed flux surface to dominate (), implying the definition of global energy confinement time is generally well approximated by transport only in . Furthermore, as outlined in Section [2.1.2](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS2) we have assumed for simplicity that all energy deposited in is balanced by radiation alone (). For this reason, we define the energy confinement time using only losses through for the remainder of this study.

### 2.2 Engineering Considerations

One key advantage of the levitated dipole concept is the relative simplicity of the confinement magnet geometry, consisting of only poloidal field coils, in contrast to other magnetic confinement fusion systems. This simplicity would allow a dipole fusion power plant to be inherently maintainable and simple to manufacture at scale, enabling the rapid roll-out and iteration needed to make a significant impact in the electricity market. However, the cost of this overall system simplicity is the extreme operating environment experienced by the levitating high field core magnet. The core magnet must function without any physical connection to external systems for extended periods of time while being surrounded by the fusing core plasma. The engineering and radiation shielding of the core magnet is the main focus of this study. The remaining systems are not spatially constrained nor coupled to the core magnet, resulting in greatly reduced complexity and risk.

Fig. [4](https://arxiv.org/html/2602.20564v1#S2.F4) depicts a representative cross section of a DT fusion-power-plant levitated-dipole core magnet. There are three main regions to the core magnet: the cryogenic REBCO coil and structural support (c-f), the coolant reservoirs (g-h), and the neutron shield (a-b). Due to the sensitivity to plasma radius in Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)), there are implied spatial constraints on each of these regions. The equilibrium physics outlined in Section [2.1](https://arxiv.org/html/2602.20564v1#S2.SS1) allow for steady-state reactor operation. However, as the core magnet is physically disconnected from all systems that would traditionally provide the required cooling power, the operation of a levitated-dipole fusion power plant must be pulsed to allow periodic removal of heat from the core magnet. This same disconnection of the magnet systems from the vacuum vessel enables simple maintenance and/or replacement of the core magnet and other key reactor components at the end of their operational lifetime. The aim of the designs presented in this study is to maximize the plant duty cycle through the following means: a latent-heat based cryogenic reservoir to minimize downtime, an on-board superconducting power supply with energy storage to remove the need to recharge the magnet when docked, and a high-performance neutron shield to minimize heating and damage from fusion neutrons.

#### 2.2.1 HTS Coil Design

A simple design for the REBCO coil in a levitated dipole would have a rectangular Kesner et al. [[2003](https://arxiv.org/html/2602.20564v1#bib.bib24)], Garnier et al. [[2006a](https://arxiv.org/html/2602.20564v1#bib.bib16)] or circular cross section. Although simple to manufacture, these geometries are not efficient in producing the required poloidal magnetic flux needed to effectively confine a dipole plasma. In the case of the rectangular cross-section coil, the corners of the coil will intersect with lines of poloidal flux, reducing the number of closed flux surfaces and increasing the flux tube volume, , at the pressure peak. In accordance with Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)), this then results in a lower peak pressure, , which can only be compensated for by increasing the magnet strength. This is not the case for a circular cross section coil, instead the high curvature on the in-board side will result in high peak magnetic field strengths for a given amount of poloidal flux. In both cases, high peak magnetic field strengths are required which can result in untenable strains in the REBCO tape Kesner et al. [[2003](https://arxiv.org/html/2602.20564v1#bib.bib24)]. Furthermore, these designs would not allow for any magnetically sensitive systems, as described in Section [2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2), to be mounted on-board the core magnet.

The design of the REBCO coil in this study alters the cross-sectional profile to minimize the induced mechanical stresses, through the reduction of peak magnetic field strengths, whilst simultaneously maximizing the plasma performance. However, the coil also needs to produce adequate magnetic field strengths in the region of highest , located on the outboard side of the core magnet, in order to achieve higher plasma pressure as discussed in Section [2.1.3](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS3). Typically, magnets with a high aspect ratio () maximize this field strength. However, this comes at the expense of higher peak magnetic field strengths, and therefore stress, for a given total magnet current . The coil cross section is therefore defined as the shape that offers the optimal tradeoff between these two competing goals. The method used to find this shape is described in Section [3.2.1](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS1).

In order to accommodate magnetically sensitive equipment on-board the core magnet, there must be a region of low magnetic field. Passive magnetic-shielding materials are only effective up to mT, making them not suitable in this case. The solution is to create a region within the REBCO coil whose shape is chosen such that the REBCO coil acts as its own magnetic shielding. This method has been demonstrated to work in OpenStar’s Junior device Chisholm and others [[2026](https://arxiv.org/html/2602.20564v1#bib.bib12)] which utilizes an arrangement of 14 REBCO coils to both generate the confining field and produce a low-field region to house the superconducting power supply.

Unlike the Junior core magnet, the core magnet coil designs presented in this study utilize a cable-in-conduit conductor (CICC) architecture instead of simple non-insulated pancake style coils. The decision to move from pancake coils to a CICC architecture is motivated by the increased stiffness allowed by CICC, which in turn allows for Lorentz loads to be more easily transferred to an external structural over-band. The addition of an over-band will ultimately reduce the strain experienced by the REBCO tape, enabling high-field magnet designs.

The strict spatial constraints make shielding the REBCO coil from the MeV DT neutrons a challenging proposition. To this end, the REBCO coil is split into two regions as shown in Fig. [4](https://arxiv.org/html/2602.20564v1#S2.F4): A small region of “sacrificial” REBCO conductor and the remaining semi-permanent section. The sacrificial section will experience higher neutron fluxes due to the thinner neutron shield and will therefore have a shorter operational lifespan, however it will also act as additional shielding for the remaining permanent REBCO conductor. The sacrificial portion will be demountable from the rest of the magnet so that it can be replaced at regular intervals without much difficulty. Having this region of sacrificial REBCO conductor in the coil reduces the performance requirements on the neutron shield allowing it to be thinner and hence increasing the magnetic field strength applied to the plasma and allowing higher plasma pressures.

#### 2.2.2 Superconducting Power Supply

While required for the economic viability of a levitated dipole fusion power plant, the use of REBCO tape in the core magnet coil introduces the issue of resistive losses. There is no process for creating a superconducting joint with performance equal to that of a commercially available REBCO tapes Park et al. [[2014](https://arxiv.org/html/2602.20564v1#bib.bib10)], Kim et al. [[2013](https://arxiv.org/html/2602.20564v1#bib.bib9)]. Therefore, the coil requires the use of normal-conducting jointing methods which will result in the dissipation of the current in the core magnet. This means that some form of power supply, including its auxiliary systems and energy source, are required to be installed on-board to compensate for the ohmic losses and enable the quasi-persistent operation of the core magnet coil.

Superconducting transformer rectifiers Leuw et al. [[2022](https://arxiv.org/html/2602.20564v1#bib.bib6)], Geng et al. [[2025](https://arxiv.org/html/2602.20564v1#bib.bib5)], as shown in Fig. [5](https://arxiv.org/html/2602.20564v1#S2.F5), are a type of superconducting power supply, colloquially called “flux pumps” van de Klundert and ten Kate [[1981](https://arxiv.org/html/2602.20564v1#bib.bib4)], Wen et al. [[2022](https://arxiv.org/html/2602.20564v1#bib.bib8)], Hoffmann et al. [[2011](https://arxiv.org/html/2602.20564v1#bib.bib7)], which make use of both superconducting circuitry and switch elements Gong and Quéval [[2025](https://arxiv.org/html/2602.20564v1#bib.bib3)] to efficiently generate and maintain large currents in superconducting loads. Several circuit topologies exist, but they all make use of a step-down transformer to convert small amplitude AC currents from the primary side to large DC currents on the superconducting secondary side. Once the AC currents are in the superconducting circuit they can be rectified and driven into the core magnet coil over many cycles. There are a range of superconducting switching technologies, but currently the mechanism that provides the greatest switching action is a switch Badcock et al. [[2022](https://arxiv.org/html/2602.20564v1#bib.bib2)]. The energy source for the superconducting power supply will be either batteries or a bank of capacitors. Batteries offer higher energy densities than capacitors, however they could be more susceptible to radiation damage Leita and Bozzini [[2024](https://arxiv.org/html/2602.20564v1#bib.bib92)]. In either case, both solutions will be recharged when the magnet is docked.

Superconducting power supplies are not high-power devices but rather excel at minimizing heat load in cryogenic high-current applications by transforming energy into the optimal current and voltage states Hamilton [[2023](https://arxiv.org/html/2602.20564v1#bib.bib1)]. This is important for the commercial viability of levitated dipoles as it means that there is an efficient method of compensating for the energy loss in the core magnet during operation. Without this mechanism, the core magnet current would decay during operation and require an additional period for re-charging during its down time, which will be a significant overhead on the operational duty cycle of the dipole.

#### 2.2.3 Cryogenic Cooling

A cryogenic reservoir is required to keep the REBCO conductor in the core magnet coil in its superconducting state when operating in the levitated position. A traditional method to cool REBCO magnets is to run a cryogen loop and rely on the magnet’s specific heat capacity and a constant flow of coolant to keep the magnet cold. In a levitated dipole, a constant flow is not possible due to the need to operate without physical connections to the rest of the plant, resulting in an operating mode where the dipole is allowed to warm up to a maximum temperature during operation before docking and re-cooling during a servicing period or down time. However, this approach limits the duty cycle of the plant to the speed at which the magnet can be re-cooled. For a large magnet with significant thermal mass, this is a lengthy process which will negatively affect the economic viability of the dipole by greatly reducing duty cycle.

The cooling strategy proposed in this study is to use a cryogenic solid-liquid slush housed on-board the dipole that melts at a constant temperature. During operation, the latent heat of the slush provides the dipole with a constant-temperature thermal reservoir. This is doubly important for the dipole because it means the REBCO coil will not need to be designed with additional operational headroom to allow for a changing operating temperature. Once melted, the resulting liquid cryogen can be quickly pumped out of the reservoir and replaced with a new batch of slush cryogen. This can be achieved in a closed loop process such that the liquid cryogen can be re-processed into slush and stored in an external reservoir for future use.

There are two viable choices of cryogen for a high field REBCO magnet: Neon with a melting point of K Ekin [[2006](https://arxiv.org/html/2602.20564v1#bib.bib82)], and hydrogen with a melting point of K Ekin [[2006](https://arxiv.org/html/2602.20564v1#bib.bib82)]. The reactors designed in this study use Neon as the cryogen due to its superior volumetric latent heat capacity, however, the lower temperatures and cost of hydrogen could make it an appealing choice for future reactors. Ultimately, the driving parameter for an economical dipole is to increase the operating duty cycle. The time it takes to replace a slush cryogen reservoir can be much reduced compared to re-cooling large magnet structures.

#### 2.2.4 Neutron Shielding

The problem of shielding the core magnet from fusion neutrons is aided by the geometry of the device. As shown in Fig. [6](https://arxiv.org/html/2602.20564v1#S2.F6), the core magnet only takes up a small portion of the field of view from the neutron source. The fraction of neutrons that pass through the space occupied by the core magnet was calculated to be % using OpenMC for a wide range of plasma equilibria. This incident fraction makes the problem of neutron flux attenuation comparable in difficulty to shielding a central column in a tokamak Windsor et al. [[2021](https://arxiv.org/html/2602.20564v1#bib.bib40)], and hence similar shield materials are considered. The neutron shield thickness is optimized by defining the outer surface to coincide with the contour. This gives ample room for shielding on the outboard side where flux expansion results in higher total fusion rates than in the core magnet bore (See Fig. [18](https://arxiv.org/html/2602.20564v1#S4.F18) for more details). However, the only way to increase the neutron shield thickness in the core magnet bore is to move further out from the core magnet coil. This then moves the pressure peak contour, , further out, incurring a steep fusion performance penalty according to Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)). Therefore, the choice of shielding material should prioritize efficient attenuation length above all else.

The most suitable materials for the core magnet neutron shield are tungsten borides and metal hydrides Brand et al. [[2025](https://arxiv.org/html/2602.20564v1#bib.bib52)], Windsor et al. [[2021](https://arxiv.org/html/2602.20564v1#bib.bib40)] as they both offer superior flux attenuation. However, the physical isolation of the core magnet imposes extra constraints. Like the cryogenic region of the core magnet, there is no way to actively extract thermal energy from the shield during a fusion pulse. The only methods available in this scenario are radiating the thermal energy from the shield surface to the first wall, or storing it in an on-board reservoir to be extracted later at the end of the pulse. The internal space constraints make radiative cooling the preferable option as an on-board reservoir would need to store a significant portion of the plants output power and therefore require a significant amount of volume. Hence, the neutron shield requires materials with extremely high working temperatures exceeding K in order to effectively reject the heat without placing severe constraints on the achievable fusion power density. Surface temperatures exceeding K allow for wall loadings in excess of MW m-2 which is required for any form of moderately compact, and therefore economically viable, fusion reactor. Increasing the temperature of the neutron shield beyond this point would allow for even higher wall loadings resulting in smaller an more attractive reactor designs. Therefore, the operating temperature of the neutron shield material is a key parameter that must be maximized in order to build economically attractive fusion power plants.

This extra requirement immediately rules out metal hydrides as they begin to decompose between K Hirooka [[1984](https://arxiv.org/html/2602.20564v1#bib.bib74)], Pollard et al. [[2025](https://arxiv.org/html/2602.20564v1#bib.bib75)]. This can be improved by forming a composite material with the metal hydride Fletcher et al. [[2025](https://arxiv.org/html/2602.20564v1#bib.bib76)], however this still results in materials with operating temperatures below what is required here. Tungsten borides perform better as some phases are thermally stable up to K Kvashnin et al. [[2018](https://arxiv.org/html/2602.20564v1#bib.bib73)], however they have yet to be manufactured at scale due to lower technological maturity. Therefore, for the purposes of this study we shall limit the neutron shielding to use well understood materials such as common tungsten alloys and boron carbide (). If the use of these materials yields a neutron shield design that meets all requirements and results in an economically viable power plant, any advancements in material science will only act to improve performance and reduce the overall size of the reactor.

One advantage of pure tungsten is its extremely high melting temperature (C), albeit at the cost of reduced neutron attenuation performance compared to tungsten borides and metal hydrides. The performance of the overall shield can be improved back to tungsten boride levels by adding a layer of to increase the rate of neutron absorption. The optimal thickness of this layer, shown in Fig. [7](https://arxiv.org/html/2602.20564v1#S2.F7), was calculated for a range of shield thicknesses by solving a neutron transport problem on a thin column of material using the OpenMC code Romano et al. [[2015](https://arxiv.org/html/2602.20564v1#bib.bib51)]. The final performance of a layered shield with an optimal fraction was then calculated to be similar to that of a monolithic block of mono tungsten boride (WB) as shown in Fig. [8](https://arxiv.org/html/2602.20564v1#S2.F8).

It is also important for the neutron shield to maintain structural integrity during its operational lifetime. Here we will consider three main mechanisms that will lead to shield failure: tungsten recrystallization, thermal creep, and neutron damage. Tungsten undergoes recrystallization above temperatures of K Richou et al. [[2020](https://arxiv.org/html/2602.20564v1#bib.bib77)], Suslova et al. [[2014](https://arxiv.org/html/2602.20564v1#bib.bib78)] which can make the material excessively brittle when cooled. The ductile-brittle transition temperature is a function of the level of recrystallization and is typically K Tietz and Wilson [[1965](https://arxiv.org/html/2602.20564v1#bib.bib97)]. Therefore, if the shield is held above K, as it would be during standard plant operation, then the tungsten will only become brittle during infrequent plant maintenance shutdowns discussed in further detail in Section [2.3](https://arxiv.org/html/2602.20564v1#S2.SS3).

The lifetime of the shield is therefore set by neutron damage and thermal creep effects. For the purposes of this study, it was assumed that the tungsten could withstand 1 MW-year/m2 of neutron irradiation before it would require replacement National Academies of Sciences, Engineering, and Medicine [[2021](https://arxiv.org/html/2602.20564v1#bib.bib26)]. Thermal creep is then managed by first designating some portion of the shield to be held at a reduced temperature of approximately ∘C (warm shield) through the use of a secondary thermal reservoir. This ensures part of the neutron shield remains structurally stiff to support the remaining region (hot shield) which is radiatively cooled and split into tiles, as shown in Fig. [4](https://arxiv.org/html/2602.20564v1#S2.F4), to reduce gravity induced stresses and hence also thermal creep. The natural transition point between the two regions is between the outer tungsten layer and the layer as the majority of the neutron energy is deposited in the tungsten and has a lower melting point. OpenMC models predict that for shields with relevant thicknesses, % of the incident neutron energy is deposited in the outer tungsten layer leaving the rest to be transferred to the secondary reservoir. The interface between the warm and hot shields ( layer and tungsten tiles respectively) will need to have a low thermal conductivity to enable efficient heat rejection through radiation at the shield surface. For the purposes of this study, a thermal break with a W m-2K-1 conductance is assumed and will be treated as a requirement for future detailed shield designs. Further design of the neutron shield—including details such as shine through prevention, tile mounting mechanism, and specific secondary reservoir coolant choice—is an ongoing area of research.

The neutron energy deposited in the shield can be recovered. The energy radiated from the shield surface to the first wall will eventually be conducted to the tritium breeder blanket covered in Sections [2.2.5](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS5) and [2.2.6](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS6) where it will add to the total thermal output. The working fluid stored in the secondary reservoir will be removed when the magnet is docked where, due to its high temperature, it may be passed through an exchanger to extract useful energy.

Finally, the end of life of the shield is considered here as it can have a significant effect on the overall cost of the plant. The main damage mechanisms described in this section result in effects which can be repaired through reprocessing of the shield material. The outer tungsten tiles, which will see the most rapid degradation, can be removed and directly recycled into new tiles for future core magnets after a cool down period of year due to their low activation half life and relatively low transmutation rate Windsor et al. [[2022](https://arxiv.org/html/2602.20564v1#bib.bib39)]. The end of life processes for the layer is complicated by the production of tritium through the 10B(n, )3H reaction. However, the layer sees significantly lower fluences than the hot-shield tiles and is also significantly less expensive, which avoids the need to consider recycling the material.

#### 2.2.5 Vacuum Vessel

The vacuum vessels required for a levitated dipole fusion power plant are large due to the dependence described in Section [2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1), where peak pressures are related to radius as in Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)). However, a feature that is unique to this magnetic confinement scheme is that the vessel does not need to make accommodations for large high-field coils and their associated loads. Therefore, the vessel design can be simple and cost effective with a representative cross section shown in Fig. [9](https://arxiv.org/html/2602.20564v1#S2.F9). The outer wall of the reactor is proposed to be a thick dome constructed from reinforced concrete. This outer wall provides a rough vacuum ( Pa), and is designed to manage the loads from the vacuum pressure differential and the weight of the top and core magnets. Internal to the outer vessel, a tritium breeding blanket, as described in Section [2.2.6](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS6), forms the bulk of the inner vacuum vessel. The plasma facing side of the inner vacuum vessel would be constructed from a thin layer of Inconel 718 with a surface coating of tungsten. Aside from tritium breeding, the purpose of the inner vacuum vessel is to provide the final high-vacuum conditions required for fusion. Since the outer vessel already provides a rough vacuum, the pressure differential over the inner vacuum vessel is small enough to only require adequate structure to support the mass of the tritium breeding blanket. Additionally, the loads created by the interaction between the top and core magnets will be transferred directly to the outer vacuum vessel.

At least one large opening is required to remove and install the core magnet and other components. Other penetrations include ports for plasma heating, fuel handling, cryogenic slush, and fluid transfer for heat extraction. A reasonable analogue to this vessel is The Space Power Facility at NASA’s Glenn Research Center Sorge [[2013](https://arxiv.org/html/2602.20564v1#bib.bib56)], which is similar in size and function. The design and build of such a vessel is therefore not anticipated to be a large technical risk. The decoupling of the inner and outer wall allow for large spaces to be added for maintenance, gantries and other services without incurring significant additional cost. An allowance has been made for a m wide cavity between the breeding blanket and the inside of the outer wall, allowing plentiful space for vessel maintenance operations.

#### 2.2.6 Tritium Breeding

The reactors proposed in this study will use a DT fuel cycle which will require a tritium breeding blanket. They are designed to operate at a tritium breeding ratio (TBR) of 1.1 which is assumed to be sufficient for self fueling and supply for future reactors. There are theoretically two surfaces available for tritium breeding, the core magnet neutron shield and the first wall. However, all materials suited for tritium breeding do not have the neutron flux attenuation performance necessary for protecting the core magnet. Instead, the outer tungsten shield behaves as a neutron reflector due to it’s high neutron multiplication cross section shown in Fig. [10](https://arxiv.org/html/2602.20564v1#S2.F10), which accounts for the neutrons absorbed in the shield. The final neutron current that passes through the first wall will no longer be comprised solely of MeV neutrons, but instead the reflection process will introduce a significant population of MeV neutrons. These neutrons will not be able to undergo the endothermic 7Li(n, n’)3H reaction which is responsible for giving materials TBRs greater than unity as it has a threshold energy of MeV. Initial TBR calculations show that the effect from this low energy neutron population are negligible, and hence will be treated that way for the remainder of this study. More in depth modeling and design of a tritium breeder blanket will be left as a topic for future study.

The simple vacuum vessel structure lends itself to thick breeder blankets capable of achieving high TBRs. Additionally, the magnetic field at the first wall is small and steady state allowing for liquid metal blanket materials to be used without the need to consider MHD effects. These benefits would theoretically free up the choice of blanket material, however, in reality the size of the inner vessel places constraints on the cost of blanket material per square meter. As shown in Fig. [11](https://arxiv.org/html/2602.20564v1#S2.F11), materials such as LiPb and Li can achieve high TBRs with thick blankets, however the surface area these blankets need to cover would make the material costs prohibitive. Instead ceramic blanket materials show the most promise due to the lower blanket thickness Shanliang and Yican [[2003](https://arxiv.org/html/2602.20564v1#bib.bib50)], aiming to reduce overall system cost. Traditionally, ceramic blankets are discounted due to the increased maintenance requirements. This is not expected to be an issue for a levitated dipole due to the simple vacuum vessel structure allowing ample room for blanket access. This study assumes the use of a blanket as a performance benchmark. Other materials can match the TBR of with the help of a neutron multiplier, however the exact composition is not needed in order to determine the overall plant performance.

#### 2.2.7 Plasma Heating Systems

Plasma heating in levitated dipoles can be accomplished using several established auxiliary heating technologies. Previous dipole experiments have primarily employed electron-cyclotron resonance heating (ECRH) Garnier et al. [[2006b](https://arxiv.org/html/2602.20564v1#bib.bib15)], Nishiura et al. [[2015a](https://arxiv.org/html/2602.20564v1#bib.bib27)] and ion-cyclotron resonance heating (ICRH) Nishiura et al. [[2015b](https://arxiv.org/html/2602.20564v1#bib.bib28)], while early theoretical work by Hasegawa also proposed neutral beam injection (NBI) as a viable heating mechanism Hasegawa et al. [[1990](https://arxiv.org/html/2602.20564v1#bib.bib21)].

ECRH has been successfully demonstrated on multiple dipole experiments and offers a relatively straightforward heating approach with favorable absorption characteristics. A particular advantage for dipole geometries is the ability to launch waves vertically into the high-field side, enabling the use of high-frequency gyrotrons with high cutoff densities. However, current gyrotron systems suffer from low wall-plug efficiency (typically 30-40%) and rely on a specialized supply chain, which may present challenges for commercial deployment.

ICRH was demonstrated on the RT-1 experiment with mixed results. This approach benefits from higher efficiency RF sources compared to ECRH, approaching % Jardin and others [[2006](https://arxiv.org/html/2602.20564v1#bib.bib91)], Faugel et al. [[2020](https://arxiv.org/html/2602.20564v1#bib.bib90)], and access to a more established industrial supply chain. The primary disadvantage lies in the increased complexity of antenna design and wave propagation modeling in the dipole magnetic geometry, which introduces greater scientific uncertainty in predicting heating performance. Investigation of ICRH in higher performance levitated dipole devices is currently ongoing Wallace et al. [[2025](https://arxiv.org/html/2602.20564v1#bib.bib35)].

NBI represents a lower-risk heating option with well-understood physics and mature technology. Unlike conventional magnetic-confinement fusion concepts, dipole reactors are less constrained by the large vessel penetrations required for neutral beam injection. Further, dipoles present improved penetration pathways to the plasma core and avoid the need for immature negative source ion beams even at reactor scale. Nevertheless, low wall plug efficiencies and specialized supply chain may prove prohibitive for power plant economics.

OpenStar’s experimental program will systematically evaluate these heating methods in future devices to inform the selection of optimal heating systems for future commercial-scale implementations based on the trade-offs outlined above. The plasma parameters employed in the present modeling study assume ICRH as the baseline heating mechanism.

### 2.3 Plant Operation

Reliability, Accessibility, Maintainability, and Inspectability (RAMI) analysis for traditional fusion technologies often results in an emphasis on component lifetime due to the lengthy periods of downtime required for maintenance as the result of a comparative lack of accessibility. Levitated dipoles mitigate this by having excellent accessibility and maintainability due to the available space and modularity of the system, which takes considerable pressure off the overall RAMI requirements. Indeed, RAMI stands as one of the most challenging barriers to fusion energy deployment, and dipoles offer a unique pathway to an economic RAMI strategy.

#### 2.3.1 Magnet Replacement & Maintenance

The complete decoupling of the core magnet from the vacuum vessel allows for it to be treated as a semi-consumable item which is replaced once damage from the fusion neutrons degrades its performance below acceptable levels. As discussed in Section [2.2.1](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS1), a portion of the coil is designated as “sacrificial” and will experience a higher neutron flux than the rest of the coil. Once the degradation limit in this region is reached, the entire core magnet can be removed from the chamber and replaced with a refurbished unit. The replacement process involves first discharging the core magnet which should be relatively quick, occurring in a matter of days, assuming a functioning quench protection system is already built into the magnet. Next, the magnet is removed through the bottom of the inner vacuum vessel and passed through an airlock of some sort into a hot cell external to the reactor. The airlock in this case is desirable as it prevents load cycling of the outer vacuum vessel while also cutting down on the time required to pump down to full vacuum. The new core magnet is then passed in and charged in place. This charging process is expected to be the lengthiest part of the replacement process, however, we still expect the total down time to be less than weeks.

The damaged magnet—which is sitting in an external hot cell—can now be maintained without affecting plant down time, and in an environment without spatial constraints. The damaged sacrificial REBCO conductor is then replaced to create a refurbished core magnet that can be reused. We expect to be able to design the sacrificial section of the coil such that it comprises less than of the overall coil cross section, with the remainder lasting around ten times longer due to the shielding effects of the sacrificial region. Ideally, multiple reactors would share the same maintenance facility allowing for the more efficient use of replacement core magnets. For the purposes of this study however, we assume that each reactor will have an attached maintenance facility. In the case where the magnet needs to be replaced once a year, the power plant would be able to achieve an overall availability factor of more than .

#### 2.3.2 Vessel Maintenance

As discussed in Section [2.2.5](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS5), ample space can be allocated for access to the inner vacuum vessel without significantly affecting the cost of the overall reactor. This space allows easy access to the inner vacuum vessel and tritium breeding blanket with a relatively simple robotic system. Therefore, technologies that require more active and frequent maintenance become viable, reducing design constraints and thereby the overall cost of the plant. Furthermore, the longevity of the plasma facing components and blanket should be higher than in other confinement concepts because of the lower wall loading afforded by the large chamber size. The maintenance strategy for these components is once again aimed at reducing plant downtime, for which the best strategy is to take advantage of the system modularity and perform the maintenance while the core magnet is being swapped out.

## 3 Design Methodology

To fully capture the interaction between the systems outlined in Section [2](https://arxiv.org/html/2602.20564v1#S2), this study uses a full system optimization approach to generate reactor designs. The naïve choice of cost function for this problem would be the plant LCOE constrained with either plant size or total capital cost. However, for such a cost function to give valid results a method for calculating the energy confinement time would need to be provided. As outlined in Section [2.1.5](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS5), no such model exists for dipoles. Therefore, we take a reversed approach: instead of optimizing for reactor power under the constraints of expected device performance, we design a reactor assuming a value for and design to minimize the required confinement time of a small scale demonstration device. In this way the design points produced by this process have the greatest chance of being viable. Using this process we design two reactors: Reactor A which aims to be feasible assuming conservative Bohm-like scaling, and a smaller Reactor B which targets a smaller overnight capital cost while requiring more aggressive performance targets.

### 3.1 Cost Function

To minimize the required energy confinement time, , for a demonstration reactor, we first need to define the scaling to apply to of the generated power plant reactor. For this purpose we use the following formulation Waltz et al. [[1990](https://arxiv.org/html/2602.20564v1#bib.bib36)]:

| (7) |

where , is the relative Larmor radius normalized to the plasma minor radius, . Due to the highly peaked nature and shape of the plasma, cannot be assumed to be constant as it is in a tokamak and is treated here as a function of both and . The remaining parameters are the ion gyrofrequency, ; a constant of proportionality that captures the confinement performance, ; and which represents either Bohm-like () or gyro-Bohm-like () scaling. We have also chosen to take the average over the low field side midplane for to account for the significant non-uniformity of the plasma profile, as discussed further in [A](https://arxiv.org/html/2602.20564v1#A1). We then reformulate Eq. ([7](https://arxiv.org/html/2602.20564v1#S3.E7)) to extract a “device index” :

| (8) |

allowing the separation of the physical embodiment of a reactor, represented by , from the operating point defined by the ion temperature at constant pressure and .

The goal of minimizing the required of a small scale demonstration device can therefore be achieved by minimizing the implied of a reactor while assuming a fixed . This is distinct from minimizing as by fixing we have restricted any two reactors that produce the same fusion power and have the same plasma stored energy to also have the same even if they have different values of . Additionally, the demonstration device will operate with a set and plasma operating point determined by what is financially reasonable. Therefore, in accordance with Eq. ([8](https://arxiv.org/html/2602.20564v1#S3.E8)) the only factor that impacts of the smaller device is the value of .

The implied of a reactor is calculated from Eq. ([7](https://arxiv.org/html/2602.20564v1#S3.E7)) utilizing the 0D power balance:

| (9) |

where is the fraction of particle energy that contributes to self heating, is the fraction of the fusion reaction energy released as an particle, and is the total power lost from the plasma in the form of radiation. As in Section [2.1.2](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS2), it has been assumed that the power deposited in will be entirely balanced by radiation losses. The total radiated power is then modeled as the sum of the bremsstrahlung power, the main radiative mechanism, and the good curvature region heating power:

| (10) |

Defining the exact form of this additional radiative term is outside the scope of this study. If the self heating fraction is then defined as , the contribution of the heating in cancels and we are left with:

| (11) |

where for the sake of this optimization we have used and to calculate the bremsstrahlung losses.

However, simply minimizing by itself does not define a well-posed optimization problem. According to Eq. ([8](https://arxiv.org/html/2602.20564v1#S3.E8)) the size of the device, represented by , is inversely proportional to and therefore a global minimum cannot be defined. The optimizer will act to minimize by increasing to arbitrary levels. If we assume that the lower bound on overnight capital cost of the plant is a monotonically increasing function of the device size captured in , then this would also result in arbitrarily high plant costs. This is prevented by setting a limit on the capital cost which in turn defines an optimal device size, , which has the lowest achievable allowed by the cost constraint. Therefore, this cost function requires a constraint on the overnight capital cost of the plant in order to converge.

The exact optimal point is determined by whether the energy confinement time scales in a Bohm-like or gyro-Bohm like fashion. This study focuses on a Bohm-like scaling as it is the more conservative of the two, and hence reactors that are feasible given this scaling represent conservative design points. In the case where a future dipole displays better scaling, it would then be possible to design smaller and more capital-efficient reactors than those presented in this paper. Therefore, the cost function used in the optimization process is explicitly:

| (12) |

with a constraint placed on the total overnight capital cost of the implied power plant.

### 3.2 Optimization Process

| Parameter | Symbol | Range | Units |
|---|---|---|---|
| REBCO Coil Outer Radius | m | ||
| Magnet Shape Control Points | |||
| Operating Current Density | A/mm2
|
||
| Cryogen Reservoir Thickness | m | ||
| First Wall Radius | |||
| Pressure Peak Location | |||
| Core Temperature | keV | ||
| Edge Pressure | Pa | ||
| Neutron Shield Limiting Thickness | m | ||
| Neutron Shield Reservoir Thickness | m |

Designing a reactor that globally minimizes Eq. ([12](https://arxiv.org/html/2602.20564v1#S3.E12)) while still satisfying engineering and economic constraints requires the modeling of the full plant. The tightly coupled nature of the core magnet performance, core magnet geometry, and the final performance of the reactor require this modeling to take place within the optimization loop. This study uses the parameterization summarized in Table [1](https://arxiv.org/html/2602.20564v1#S3.T1) which, once constraints are applied to the magnet shape parameters, defines a 14 dimensional design space which is searched to find the global minimum. The sensitivity of the final reactor performance to some of these parameters rules out a brute force search as a viable method for finding the global optimum. Additionally, the high level nature of the constraints and the complexity introduced by the interacting systems also makes gradient- based optimization methods unsuited to this task. Instead, differential evolution Storn and Price [[1997](https://arxiv.org/html/2602.20564v1#bib.bib53)] (DE) was chosen for this study as it offers good flexibility and adequate performance while simultaneously remaining easy to implement, allowing more attention to be focused on the modeling stages that comprise the optimization loop as outlined in Fig. [12](https://arxiv.org/html/2602.20564v1#S3.F12). The parameters in Table [1](https://arxiv.org/html/2602.20564v1#S3.T1) are generated using DE and then passed through a series of modeling stages that progressively build up the reactor from the REBCO coil outwards.

#### 3.2.1 REBCO Coil Design

The first stage in the optimization process is the design of the REBCO coil that generates the confining magnetic field. This process is complicated by the requirement of a low-field region within the magnet to accommodate for the on-board superconducting power supply and electronics as introduced in Section [2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2). First, the upper half of the outer shape of the coil is constructed using a fourth order Bézier curve which is constrained to have the required outer radius and be vertical at the mid plane to ensure continuity. The resulting parameterization has five degrees of freedom that are determined through the optimization. Then, the boundary of the low-field region is created and optimized to reduce the interior magnet field strength.

The homogeneous current density is then divided into a grid of REBCO conductor conduits to represent the final winding geometry. The homogeneous region is first broken into cells whose required cross sectional area is constrained by the ratio of the target operating current, , to . The cell width is set by the turn with the lowest expected tape critical current, , which will require the highest number of parallel tapes to carry the target . The REBCO tape is most sensitive to magnetic field perpendicular to the tape’s surface, hence the lower cells will be located at the top and bottom of the coil. All other cells in the coil will require fewer parallel tapes, and therefore can support a higher ratio of structural material helping with transferring the Lorentz load to the structural over-band. Therefore, the coil can be broken into regions of high conductor-ratio conduit and high steel-ratio conduit to optimize the performance and mechanical strength of the coil. The design of the conduit beyond this point is outside the scope of this study and will be a topic of future publications.

The REBCO tape performance is based off the performance of SuperOx YBCO presented in the Robinson Supercurrent Database Wimbush [[2021](https://arxiv.org/html/2602.20564v1#bib.bib54)] and extrapolated to the required operating conditions using an elliptic function Grilli et al. [[2014](https://arxiv.org/html/2602.20564v1#bib.bib55)]. Recently, Faraday Factory, a REBCO tape manufacturer, announced a new “Mirai” family of REBCO tape which is expected to reliably produce engineering current densities in excess of A mm-2. This corresponds to a performance increase of % over their current generation product Wimbush [[2021](https://arxiv.org/html/2602.20564v1#bib.bib54)], Molodyk and others [[2021](https://arxiv.org/html/2602.20564v1#bib.bib80)]. This improvement is applied on top of the modeled tape extrapolated from the available data. The final grid of REBCO conduit will affect the optimization of the low-field region from the previous step. However, any deviation from this optimum is assumed to be correctable with the use of passive and active magnetic shielding and therefore ignored for the purposes of this optimization. The final output from this model is a grid of currents each with a required number of parallel tapes needed to carry the target .

#### 3.2.2 Plasma Equilibrium

The core magnet coil is then used as an input to the DipolEQ MHD equilibrium code Garnier et al. [[1999](https://arxiv.org/html/2602.20564v1#bib.bib14)] which solves the reduced (toroidal-field-free) Grad-Shafranov equation:

| (13) |

in the region between the first and last closed flux surfaces. To define the pressure, density, and temperature profiles a normalized poloidal magnetic flux is defined:

| (14) |

The choice of pressure profile used in Eq. ([13](https://arxiv.org/html/2602.20564v1#S3.E13)), assumed to be isotropic for simplicity, is based on whether the plasma is in a region of good or bad curvature. In the bad curvature region the pressure follows Eq. ([3](https://arxiv.org/html/2602.20564v1#S2.E3)) and in the good curvature region the pressure profile is arbitrarily defined as a cosine function:

| (15) |

where the peak location, , and an edge pressure, , need to be provided by the optimizer.

The density and temperature profiles can be obtained by realizing that Eq. ([1](https://arxiv.org/html/2602.20564v1#S2.E1)) can be equivalently expressed as and . These are then combined and integrated to obtain an explicit form of the density profile:

| (16) |

and temperature profile:

| (17) |

where the primed variables represent reference values, such as at the plasma edge or the pressure peak. The optimization algorithm provides the core temperature, , to enable this calculation. Using these profiles, the fusion and neutron production rates are calculated and then interpolated onto an grid to be used by the following models.

The optimizer is given control of in order to account for the large gyro radius of the 3.5 MeV particles. To maximize plasma performance a levitated dipole reactor design should always aim to place as close to as possible. However, at smaller values of the prompt loss of particles to the core magnet will increase to unacceptable levels. To prevent this, a constraint is placed on the minimum real-space separation between and expressed as a multiple of the particle gyro-orbit. This separation is impossible to calculate before producing the equilibrium, therefore it is necessary to allow the optimizer to control the peak location to iteratively approach the correct location.

#### 3.2.3 Neutron Shielding Design

The next stage in the optimization process is the design of the neutron shield. As discussed in Section [2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4), all space up to will be used to maximize shield thickness without encroaching on the region of closed field lines. The wall loading neutron flux can be calculated at points lying on by integrating over the plasma volume accessible via straight-line trajectories:

| (18) |

where and are the the unit surface normal and reaction rate density, respectively. Projection onto the plane reduces the numerical evaluation of Eq. ([18](https://arxiv.org/html/2602.20564v1#S3.E18)) to an effective 2D problem, for which polynomial straight-line intersections can be determined analytically.

The shield is then defined from the closest point on to the core magnet coil. Here the wall loading neutron flux is sampled and used alongside the optimizer determined characteristic shield thickness, , to calculate the shielded flux using the attenuation data for a W--W composite structure as presented in Fig. [8](https://arxiv.org/html/2602.20564v1#S2.F8). This predicted neutron flux is then used to calculate the neutron shield thickness around the rest of the core magnet.

This method shows good heating power correlation with the more accurate OpenMC models, however, it tends to underestimate the neutron flux in the shielded region. Contributions from geometric effects and material interactions, such as neutron multiplication, that are not included in this simple model account for this additional flux. In this study the lifetime of the REBCO tape used in the core magnet coil is calculated using a maximum fast neutron fluence of cm-2 Fischer et al. [[2018](https://arxiv.org/html/2602.20564v1#bib.bib57)]. As long as the neutrons can still be considered fast (energy MeV), this limit is assumed to be agnostic of the incident neutron direction. Therefore, the additional neutron flux modeled in OpenMC is assumed to impact the lifetime of the tape. To account for this mismatch, the flux predicted in this simplified model is multiplied by a factor of 3 informed from numerous comparisons with OpenMC.

#### 3.2.4 Internal Structure Design

Once the core magnet coil and neutron shield have been defined, the remaining volume can then be distributed among the core magnet coil structure, cryogenic reservoir, and the neutron shield reservoir. In order to properly capture the design pressures acting on each of these components, the optimizer is given control of the volume of both the cryogen and shield reservoirs through their midplane thicknesses, and respectively. The remaining volume is then allocated to the core magnet coil structural support. A more detailed design of the core magnet will alter the shapes of the reservoir to optimize the cooling power and docking speed. The geometry described here simply ensures there is enough volume of coolant available in the core magnet.

The stresses in the core magnet coil and structure are calculated using a 2D axi-symmetric FEA model. The grid of currents and magnetic field from the core magnet coil design are used to calculate the Lorentz body loads on the whole structure. For the optimization process it was sufficient to approximate the core magnet coil and structure as a homogeneous material. The calculated peak von Mises stress is then used to constrain the optimization process to ensure the final magnet design remains feasible.

#### 3.2.5 Reactor Performance

| Parameter | Symbol | Value | Units |
|---|---|---|---|
| Thermal Efficiency | |||
| Auxiliary Heating Efficiency | |||
| Cryogenic Efficiency | |||
| Blanket Power Fraction | |||
| Neutron Energy Multiplier | |||
| Blanket Energy Multiplier | |||
| Electrical Heating | kW | ||
| Shield Conduction Heating | kW | ||
| Core Magnet Docked Time | min |

The final stage in the optimization process is to calculate the net electrical output power of the plant, where the assumed input parameters have been summarized in Table [2](https://arxiv.org/html/2602.20564v1#S3.T2). The total thermal power is approximated by:

| (19) |

where and are the energy multiplication factors for the shield and blanket respectively; is the fraction of neutron power deposited in the blanket; and , , and are the fusion, auxiliary heating, and total neutron power respectively. For the purposes of this optimization process, the values are assumed to be independent of the plant geometry. As discussed in Section [2.2.6](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS6), the tungsten layers of the neutron shield have a high cross section for endothermic neutron multiplication reactions. From OpenMC calculations on a range of dipole designs, the effect of this reaction is to reduce the heating in the shield by approximately 12 %. The same OpenMC models were used to determine that approximately 80 % of the neutron energy is deposited in the blanket. Meanwhile, the Li2O breeder blanket is modeled as multiplying the incident neutron energy by % Sawan and Abdou [[2006](https://arxiv.org/html/2602.20564v1#bib.bib58)]. The net electrical power is then modeled as:

| (20) |

where is the core magnet duty cycle, is the electrical conversion efficiency, is the total efficiency of the auxiliary heating system, and is the efficiency of the cryogenic cooling system (see Section [2.2.3](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS3)) which we expect to be %. The total cryogenic heat load is modeled as the sum of the cryogenic neutron and photon heating, , the heat conducted from the neutron shield, , and the electrical resistive heating, , required to keep the magnet charged. is given by the previously described neutron shielding model in Section [3.2.3](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS3), whereas the values for and are given as a constant budget that must be met by later detailed engineering designs.

| Parameter | Symbol | Value | Units |
| Solid fraction | |||
| Cryogenic Reservoir | |||
| Solid Density | g cm-3
|
||
| Latent Heat of Fusion | J g-1
|
||
| Melting Temperature | K | ||
| Neutron Shield Reservoir | |||
| Solid Density | g cm-3
|
||
| Latent Heat of Fusion | J g-1
|
||
| Melting Temperature |
∘C |
||
| Neutron Power Fraction |

[2006](https://arxiv.org/html/2602.20564v1#bib.bib82)] while the shield reservoir uses an aluminum-copper alloy Shamberger and Bruno [

[2020](https://arxiv.org/html/2602.20564v1#bib.bib81)].

In order to model the core magnet duty cycle both the levitation time, , and the docked time, , are needed:

| (21) |

This study assumes that the use of the latent heat based slush cryogen described in Section [2.2.3](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS3) will allow short docked times of . The levitation time, on the other hand, is dependent on the volume of both reservoirs on-board the core magnet and the total amount of heating in those reservoirs. The total energy storage capacity of reservoir is calculated using:

| (22) |

Where is the fraction of solid material in the reservoir which is assumed to be 60%, is the reservoir volume, is the coolant solid density, and is the coolant latent heat of fusion. The values for these parameters for both reservoirs are given in Table [3](https://arxiv.org/html/2602.20564v1#S3.T3). The cryogenic reservoir limited levitation time can then be calculated as:

| (23) |

and the shield reservoir limited time as:

| (24) |

where represents the fraction of shield neutron power that will be stored in an on-board reservoir which uses the latent heat of fusion of an aluminum-copper alloy Shamberger and Bruno [[2020](https://arxiv.org/html/2602.20564v1#bib.bib81)] to store the thermal energy until the next docking cycle. This material was selected to give a representative estimate of the total levitation time, the final material selection will be a topic of future study. The total levitation time, , is then modeled as the minimum of Eqs. ([23](https://arxiv.org/html/2602.20564v1#S3.E23)) and ([24](https://arxiv.org/html/2602.20564v1#S3.E24)):

| (25) |

### 3.3 Optimization Constraints

| Name | Symbol | Reactor A | Reactor B | Units |
|---|---|---|---|---|
| Relative Max Overnight Cost | ||||
| Relative Max LCOE | 1 | |||
| Target Q | 15 | |||
| Tritium Breeding Ratio | 1.1 | |||
| Max Edge Temperature | 800 | eV | ||
| Max Edge Pressure | Pa | |||
| Min Separation | ||||
| Max Von Mises Stress | 700 | MPa | ||
| Max Coil REBCO Fill Fraction | 40 | % | ||
| Low-Field Region Width | 150 | mm | ||
| Max Neutron Shield Temperature | 2500 | K | ||
| Min Sacrificial REBCO Lifetime | 1 | yr |

Constraints on the performance and total cost of the reactor, as summarized in table [4](https://arxiv.org/html/2602.20564v1#S3.T4), are required to ensure the final power plant is economically viable and physically feasible. Each reactor is constrained with two economic parameters: overnight capital cost and levelized cost of electricity (LCOE). As discussed in Section [3.1](https://arxiv.org/html/2602.20564v1#S3.SS1), the constraint on the maximum overnight capital cost is core to the definition of the optimization problem as it allows for a global minimum to be defined. The constraint on the LCOE, on the other hand, acts to ensure the final reactor remains economically viable. OpenStar is currently in the process of developing a model for estimating the overnight capital cost and LCOE for levitated dipole fusion power plants which will be the topic of future work. This study uses preliminary results from this model which are subject to change as the model is developed. For this reason we avoid quoting specific values here, instead opting to present the relative cost and LCOE. Both reactors have been set with the same limit on the LCOE, but Reactor B was constrained to be less than half the overnight capital cost of Reactor A to encourage the design of a smaller plant.

The remaining constraints were then imposed in an attempt to ensure the practical viability of the plant. The overall plant is assumed to have and a to be comparable with other proposed FOAK fusion power plants Sorbom and others [[2015](https://arxiv.org/html/2602.20564v1#bib.bib43)], Rutherford and others [[2024](https://arxiv.org/html/2602.20564v1#bib.bib42)], Lion and others [[2025](https://arxiv.org/html/2602.20564v1#bib.bib41)]. The lifetime of the sacrificial portion of the core magnet coil, as discussed in Section [2.2.1](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS1), is limited to be above year. This ensures the core magnet can be replaced during a planned yearly maintenance window, which is already accounted for in the economics of the plant.

As mentioned in Section [2.1.4](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS4), the physics defining viable conditions at the plasma edge is not well understood. We expect there to be an edge pedestal due to preferential ion scrape off, however the magnitude of this effect is still unknown. I-mode tokamaks experience edge pedestals with temperatures and pressures exceeding eV and Pa respectively Whyte and others [[2010](https://arxiv.org/html/2602.20564v1#bib.bib59)], which we shall treat as an upper bound on performance in this study. The location of the pressure peak is constrained to reduce the possibility of excess prompt losses. Scattering events with the background plasma will cause some of the particles to transport further towards the first closed flux surface than what can be calculated using a simple orbit calculation. To account for this, was constrained to ensure the peak location was at least two MeV Larmor orbits, , away from , which is later verified with particle tracing codes to minimize prompt losses of the fusion products; see Section [4.2](https://arxiv.org/html/2602.20564v1#S4.SS2).

The core magnet coil is expected to produce extreme Lorentz forces in a power plant scale device. The final design is constrained to have a peak von Mises stress of less than MPa to prevent yielding of the structural materials and to ensure a strain in the REBCO tape below % Gaifullin et al. [[2023](https://arxiv.org/html/2602.20564v1#bib.bib79)], Shin et al. [[2007](https://arxiv.org/html/2602.20564v1#bib.bib85)]. To aid in this, the core magnet coil REBCO tape fill fraction was limited to % to allow for an adequate cross section of steel within the winding pack. The width of the low-field region is then set to be mm to allow adequate space for the on-board superconducting power supply outlined in Section [2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2) and any other sensitive on-board systems. Finally, the maximum surface temperature of the neutron shield tungsten tiles is limited to be less than K to prevent large thermal creep rates.

| Name | Symbol | Reactor A | Reactor B | Units |
| Net electric power | MW | |||
| Auxiliary heating power | MW | |||
| Target Q | 15 | |||
| Core magnet duty cycle | % | |||
| Core magnet outer radius | m | |||
| First wall radius | m | |||
| Outer chamber radius | m | |||
| Core Magnet Surface Area | m2
|
|||
| First Wall Surface Area | m2
|
|||
| Tritium breeding ratio | 1.1 | |||
| Plant availability factor | 96 | % | ||
| Component | Material | |||
| Outer VV | Reinforced Concrete | tonnes | ||
| Tritium Breeding Blanket | Li2O |
tonnes | ||
| Inner VV | Inconel 718 | tonnes | ||
| Neutron Shield Tiles | Tungsten | tonnes | ||
| Shield | tonnes | |||
| WC Shield | WC | tonnes | ||
| Core Magnet Structure | SS316LN | tonnes | ||
| Coil Conduit | SS316LN and Copper | tonnes | ||
| REBCO Tape | REBCO | km | ||
| CM total | tonnes | |||
| Reactor total | tonnes |

[3](https://arxiv.org/html/2602.20564v1#S3)).

## 4 Design Points and Analysis

The optimization process produces significantly different designs for the two overnight capital cost constraints described in Section [3.3](https://arxiv.org/html/2602.20564v1#S3.SS3). An overview of the two design points is given in Table [5](https://arxiv.org/html/2602.20564v1#S3.T5). Reactor A is a MWe plant with an outer core magnet radius, defined to include neutron shielding, of m, a first wall/limiter radius of m, and an outer vacuum vessel radius of m. This is a similar output power to ITER Aymar et al. [[2002](https://arxiv.org/html/2602.20564v1#bib.bib83)] and Commonwealth Fusion System’s 2016 ARC Sorbom and others [[2015](https://arxiv.org/html/2602.20564v1#bib.bib43)], making it a useful point of comparison. The overall size of Reactor A is much larger than either of the aforementioned tokamaks, however the majority of this space, as shown in Fig. [13](https://arxiv.org/html/2602.20564v1#S4.F13), is comprised of the extremely simple vacuum vessel. The core magnet, which is the most complex and expensive part of the reactor, is the same physical scale as the magnets that comprise the ARC tokamak Sorbom and others [[2015](https://arxiv.org/html/2602.20564v1#bib.bib43)] (Fig. [2](https://arxiv.org/html/2602.20564v1#S1.F2)). Therefore the capital cost of the plant remains competitive. Reactor B, on the other hand, generates a lower power of MWe with a smaller m radius core magnet and a m radius vacuum vessel. At this output power Reactor B is more suited for industrial applications instead of standalone grid power generation. The lower overnight capital cost may make Reactor B the more appealing choice as a FOAK fusion power plant.

The key plasma parameters of the target equilibrium for both reactors are presented in Table [6](https://arxiv.org/html/2602.20564v1#S4.T6). Both reactors operate with a core temperature of keV (see Section [5](https://arxiv.org/html/2602.20564v1#S5)) and require an edge temperature pedestal of eV. As shown in Fig. [14](https://arxiv.org/html/2602.20564v1#S4.F14), the total fusion power is significantly higher on the outboard side of the core magnet than in the bore. This difference is a result of the large flux expansion that is characteristic of dipole plasmas. As temperature and density are both purely functions of the poloidal magnetic flux (see Section [2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1)), this expansion leads to larger volumes of fusion reactions on the low field side of the core magnet. As a result, the total fusion power on the outboard side is times higher than in the magnet bore.

Levitated dipoles are often quoted as being high devices Hasegawa et al. [[1990](https://arxiv.org/html/2602.20564v1#bib.bib21)], Kesner et al. [[2003](https://arxiv.org/html/2602.20564v1#bib.bib24)], however due to the large inhomogeneity in the plasma pressure profile this is only true for a local definition of . Both reactors display which, as described in Section [2.1.3](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS3), is in the optimal fusion power range for the given magnet configuration. On the other hand, as defined in Eq. ([5](https://arxiv.org/html/2602.20564v1#S2.E5)) is much lower, sitting at just % for Reactor A and % for Reactor B. These values are coincidentally typical of an ARC class tokamak Sorbom and others [[2015](https://arxiv.org/html/2602.20564v1#bib.bib43)]. Unlike a tokamak, driving the plasma to higher results in a loss of confinement through infinite local and the resultant plasma expansion (Section [2.1.3](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS3)) instead of the excitement of MHD instabilities.

| Name | Symbol | Reactor A | Reactor B | Units |
|---|---|---|---|---|
| Fusion power | MW | |||
| Peak plasma pressure | MPa | |||
| Peak ion temperature | keV | |||
| Peak electron density | m-3
|
|||
| Peak local | ||||
| Peak pressure radius | m | |||
| Peak pressure flux | ||||
| field at | T | |||
| Edge ion temperature | eV | |||
| Edge electron density | m-3
|
|||
| MeV neutron power | MW | |||
| MeV neutron power | MW | |||
| Bremsstrahlung power | MW | |||
| Plasma stored energy | MJ | |||
| Global | % | |||
| Plasma Volume | m3
|
|||
| Energy confinement time | s |

The total stored energy in Reactor A is MJ. From this the energy confinement time required in this device was calculated using Eq. ([9](https://arxiv.org/html/2602.20564v1#S3.E9)) to be s. This is lower than the energy confinement time required for Reactor B of s. This implies that Reactor A is a more conservative design of a device, which is discussed further in Section [5](https://arxiv.org/html/2602.20564v1#S5). For now it is worth noting the implications of such a high energy confinement time. Due to the convective cells that form in the bad curvature region the particle confinement time in a dipole plasma will be short. In ideal conditions, marginal stability to interchange modes will result in these convective cells transporting no energy. However, due to losses at the plasma edge there must be some energy transport to maintain the MHD stable profile. It is expected that the resultant energy confinement time, which we have presented here, will be an order of magnitude larger than the particle confinement time Kesner et al. [[2003](https://arxiv.org/html/2602.20564v1#bib.bib24)]. This will allow for efficient removal of ash and refueling to occur near without excess loss of plasma energy.

The extra size and simplicity of the reactor vacuum vessel offers additional benefits when it comes to plant access and maintainability (Section [2.3](https://arxiv.org/html/2602.20564v1#S2.SS3)). The key advantage here is that the core magnet is completely decoupled from the vacuum chamber, meaning it can be removed and replaced without the disassembly of the whole plant. Although they are not the focus of this study, this modularity also applies to other systems in the reactor such as the breeder blanket, top magnet coil, and limiter. The blanket in particular is mounted to the outside of the inner vacuum vessel which allows easy access for maintenance and replacement. This replacement could be done in stages throughout the life of the plant with minimal impact on the plant up time, which is important as it allows the use of solid blanket materials. The large outer vacuum vessel is constructed using reinforced concrete at similar sizes to previously constructed vacuum vessels Sorge [[2013](https://arxiv.org/html/2602.20564v1#bib.bib56)].

In order to focus on the key engineering challenges in a levitated dipole fusion power plant, the details of the limiter and top magnet have not been considered. The strength and stored energy of the core magnet mean that it will only require a small secondary field provided by the top magnet in order to generate sufficient levitation force. This immediately ensures the top magnet will be a small fraction of the core magnet cost and therefore will not affect the cost of the overall plant significantly. As mentioned in Section [2.1.4](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS4), we also expect that a fully realized levitated dipole reactor will have a diverted plasma in order to achieve the edge conditions presented in this study, hence presenting a design for a limiter would be redundant.

| Name | Symbol | Reactor A | Reactor B | Units |
|---|---|---|---|---|
| Coil outer radius | m | |||
| Peak field on conductor | T | |||
| Current density | A/mm2
|
|||
| Inductance | H | |||
| Total current | MA-turns | |||
| Stored energy | GJ | |||
| Terminal current | kA | |||
| Peak structure Von Mises stress | MPa | |||
| Average structure Von Mises stress | MPa | |||
| Peak magnet axial stress | MPa | |||
| Peak magnet hoop stress | MPa | |||
| Peak magnet tensile strain | % | |||
| Operating temperature | K | |||
| Coolant | Neon slush | |||
| Float time | min |

Also presented in Table [5](https://arxiv.org/html/2602.20564v1#S3.T5) is a summary of the total masses of each component in the reactor. In Reactor A, the core magnet assembly is predicted to weigh in excess of tonnes, with the majority of the mass comprised of the neutron shield tungsten tiles. This mass does not pose much of a concern for the levitation of the core magnet, however, future designs of levitated dipole fusion power plants should aim to minimize this tungsten use. The sensitivity of the overall reactor size to the thickness of the neutron shield would allow even modest increases in material neutron attenuation performance to result in significant savings in overall shield mass. Therefore, the material selection for the core magnet neutron shield is still an area of active research.

### 4.1 Magnet Design

The core magnet required to confine the plasma is comprised of a single large REBCO coil whose cross section has been optimized to offer the best plasma performance constrained by material yield stress limits. The design parameters for the core magnets of both reactors are presented in Table [7](https://arxiv.org/html/2602.20564v1#S4.T7). For Reactor A, the core magnet coil generates a peak field of T and has a total stored energy of GJ, similar to that of the full ARC toroidal field magnet system Hartwig and others [[2024](https://arxiv.org/html/2602.20564v1#bib.bib18)]. As shown in Fig. [16](https://arxiv.org/html/2602.20564v1#S4.F16) this coil is mounted to a substantial 316LN stainless steel support with space for a reservoir for the slush cryogen coolant. This assembly is placed within a thin cryostat to thermally shield it from the inner surface of the neutron shield.

The REBCO coil is constructed using a cable-in-conduit (CICC) style cable where a stack of 6 mm wide REBCO tape is soldered to a copper channel and then wrapped in a square cross section steel jacket. The turns of the coil are then assumed to be welded together with insulation only placed between adjacent winding layers, leaving adjacent turns to be non-insulated. This configuration allows for both higher coil stiffness for more effectively transferring stress to the structural over-band, and better cooling and resilience in the event of a quench. The exact proportions of steel to copper and the specifics of the cooling method are out of the scope of this study. About % of the coil is designated as sacrificial, meaning that it will be replaced at a regular cadence due to damage from the fusion neutrons. This section will be mechanically separate from the remainder of the coil to ensure it can be removed easily.

The REBCO cable will be designed to carry kA of current continuously while in operation. This current is supplied by a superconducting power supply mounted in the low-field region in the center of the coil. This power supply includes components that will not function in the high field environment generated by the core magnet coil. The shape of the low-field region is optimized to reduce the field to a level mT where passive shielding methods become possible. Fig. [15](https://arxiv.org/html/2602.20564v1#S4.F15) shows that by choosing the correct coil and low-field region shape, the coil itself acts to create a region with field strengths two orders of magnitude lower than the peak coil field. The inclusion of the superconducting power supply allows the magnet to stay charged while levitating and is a key component in reducing the time the core magnet spends docked. One key limiting factor of superconducting power supplies is their inability to produce high voltages. At the time of writing, the highest performance flux pumps produce voltages ranging in the millivolts Geng et al. [[2025](https://arxiv.org/html/2602.20564v1#bib.bib5), [2025](https://arxiv.org/html/2602.20564v1#bib.bib5)], well below what is needed to charge a magnet of the sizes described here in a practical amount of time. For this reason, the superconducting power supply is only used to maintain the current in the coil, in a quasi-persistent state, while external semi-conducting power supplies are used in the rare occasions this magnet will need to be charged.

The coil will operate at a temperature of K set by the melting point of the chosen cryogen with some margin, in this case neon with a melting point of K Ekin [[2006](https://arxiv.org/html/2602.20564v1#bib.bib82)] which was chosen for its superior latent heat capacity. The neon will be stored on the magnet in the form of a solid-liquid slush mixture which will transition to be fully liquid as it absorbs energy. The volume of the reservoir determined through the optimization process is sufficient to allow for minutes of levitation before the core magnet will need to be docked and the melted slush pumped out and replaced. The overall plant duty cycle for both reactors is high, %, which offers the best tradeoff between increasing the float time and reducing the volume available for the core magnet coil and structural over-band. The amount of neon needed to achieve this levitation time is small, which is a result of the lifetime of the REBCO conductor in the core magnet coil being the limiting factor when determining the thickness of the neutron shield (Section [4.3](https://arxiv.org/html/2602.20564v1#S4.SS3)). The remaining heat loads from the attenuated neutrons and photons, electrical heating, and conduction from the neutron shield only sum to a few tens of kilowatts as shown later in Table [9](https://arxiv.org/html/2602.20564v1#S4.T9). Another possible cryogen would be hydrogen which is significantly cheaper than neon and has a lower melting point of K Ekin [[2006](https://arxiv.org/html/2602.20564v1#bib.bib82)], but needs times the volume to store the same amount of energy. This increased volume would have a small impact on the allowed volume for structural support and hence would result in slightly larger reactors. However if procuring and maintaining a supply of neon proves challenging it would be a viable alternative.

The expected stresses and strains in a homogenized version of the core magnet were modeled in COMSOL to verify that the conductor was not pushed beyond its mechanical strain limit. The coil material was treated as an arbitrary mixture of copper and steel with a Young’s modulus of GPa. We have also assumed that the low-field region will be able to carry stress in the plane, but not in the direction, to aid in the overall stress distribution. The structural over-band was assumed to be solid stainless 316LN for the purposes of this calculation with the expectation that some of the material will be removed to reduce weight and allow space for magnet services.

The results of this modeling, presented for Reactor A in Fig. [17](https://arxiv.org/html/2602.20564v1#S4.F17), show the peak hoop strain in the conductor is % for Reactor A and % for Reactor B. These are both below the mechanical limit of % Gaifullin et al. [[2023](https://arxiv.org/html/2602.20564v1#bib.bib79)] valid for most REBCO tapes. The peak von Mises stress in both reactors also remained below % of the cryogenic yield stress of 316LN of MPa Nyilas et al. [[2004](https://arxiv.org/html/2602.20564v1#bib.bib86)]. The average von Mises stress in Reactor A is MPa and in Reactor B is MPa, which is low enough to allow for significant material to be removed without compromising structural integrity. This would reduce the overall mass of the magnet, but would mainly serve to allow for cooling channels and docking infrastructure. One of the main concerns with previous proposed levitated dipole fusion reactors was the need of novel structural materials to generate reasonable output powers Kesner et al. [[2003](https://arxiv.org/html/2602.20564v1#bib.bib24)]. However, here we have shown a magnet design that can be built with contemporary materials and traditional manufacturing methods, substantially reducing cost and technology risk.

### 4.2 Fast Ion Confinement

Prompt -particle losses were calculated using ASCOT5, a test-particle orbit-following code Varje et al. [[2019](https://arxiv.org/html/2602.20564v1#bib.bib34)]. ASCOT5 simulations are based on a volume preserving algorithm integrating particle orbits through a fixed time step, which was set to , or of the shortest gyro-period in both reactors. Coulomb collisions with the deuterium and tritium ions in the background plasma are included in the simulations, allowing fast -particles to thermalize, with a cutoff set at twice the ion temperature. In each simulation test-particles were sampled from an energy-pitch distribution generated from the reaction rate of Maxwellian reactant pairs Sirén et al. [[2017](https://arxiv.org/html/2602.20564v1#bib.bib33)].

Losses are particles which pass through either or , and are defined as prompt-loss if they still have at least of their initial energy when lost. The ratios of confined -energy to total -energy in reactors A and B are %, and the corresponding values for the energy lost are given in Table [8](https://arxiv.org/html/2602.20564v1#S4.T8). The peak wall loads are kW m-2, which are two orders of magnitude less than the neutron loading. Therefore, neutron heating is the primary constraint when designing the shield, as discussed in Section [4.3](https://arxiv.org/html/2602.20564v1#S4.SS3). In total Reactor A sees kW of prompt heating on the neutron shield, and Reactor B sees kW.

Steep profiles are a key signature of dipole equilibria, where peak pressure, density and temperature values in the core are much greater than in the bulk plasma. heating on either side of the peak location, which separates the good-curvature and bad-curvature regions, has a significant effect on the power balance in each region. Heating in the good-curvature region must be balanced by losses to preserve steady state. This is an ongoing area of active research and will be discussed in future works.

### 4.3 Neutron Transport

The OpenMC code Romano et al. [[2015](https://arxiv.org/html/2602.20564v1#bib.bib51)] was used to to investigate the effectiveness of the neutron shielding mounted on the core magnet. The key results from this simulation are presented in Table [8](https://arxiv.org/html/2602.20564v1#S4.T8). A simplified version of the CAD model shown in Fig. [16](https://arxiv.org/html/2602.20564v1#S4.F16) was passed through the DAGMC Wilson et al. [[2010](https://arxiv.org/html/2602.20564v1#bib.bib93)] workflow for meshing and material assignment. The ENDF/BVII.1 Chadwick and others [[2011](https://arxiv.org/html/2602.20564v1#bib.bib49)] material library was used to calculate the material reaction cross sections. Unfortunately this database does not include an entry for neon hence the cryogen volume was treated as a vacuum. This should not affect the results substantially as the number density of the neon slush is low and it also only comprises a small portion of the physical cross section of the core magnet. The core magnet coil was modeled as a - - - mix of YBCO superconducting tape, PbSn solder, Copper, and 316LN stainless steel. The REBCO tape was also assigned the appropriate mix of YBCO, copper, and Hastelloy commonly found in tape from the larger REBCO tape suppliers Molodyk and others [[2021](https://arxiv.org/html/2602.20564v1#bib.bib80)]. The structural over-band was modeled assuming % density to account for cooling channels and docking infrastructure. Finally, the neutron source was modeled as a fine grid of isotropic mono-energetic ring sources spanning the plasma region depicted in Fig. [14](https://arxiv.org/html/2602.20564v1#S4.F14) with the MeV DD and MeV DT neutrons treated as separate sources. The source weighting was then calculated using the plasma equilibrium profile to get the fully resolved neutron source distribution.

Some important results from this model are given in Table [8](https://arxiv.org/html/2602.20564v1#S4.T8). The total heating in the cryogenic region from both neutrons and secondary photons is kW for Reactor A, and kW for Reactor B. In both cases the heating power is a sufficiently small percentage of the total fusion power required for the plant to be power positive. The factor requiring such a thick shield is therefore the lifetime of the sacrificial portion of the core magnet coil. For Reactor A, a mm thickness shield at the point closest to the core magnet is sufficient to reduce the fast neutron flux by four orders of magnitude to cm-2s-1. The neutron flux spatial distribution and attenuated neutron flux energy spectrum at the inner surface of the shield is given in Fig. [18](https://arxiv.org/html/2602.20564v1#S4.F18). The majority of the neutron energy is moderated down to a band between and MeV, which is a similar spectra to the neutron sources used to test the lifetime of REBCO samples Fischer et al. [[2018](https://arxiv.org/html/2602.20564v1#bib.bib57)]. At these energies the critical current of REBCO tape drops by % after a fluence of cm-2 Fischer et al. [[2018](https://arxiv.org/html/2602.20564v1#bib.bib57)].

| Name | Symbol | Reactor A | Reactor B | Units |
|---|---|---|---|---|
| Peak Neutron Flux | cm-2s-1
|
|||
| First Wall Neutron Flux | cm-2s-1
|
|||
| Neutron Flux on REBCO Coil | cm-2s-1
|
|||
| Max Neutron Shield Wall Loading | MWm-2
|
|||
| Max First Wall Loading | MWm-2
|
|||
| Blanket Neutron Energy Fraction | % | |||
| Total Neutron Shield Heating | MW | |||
| Total Cryogenic Heating | kW | |||
| Prompt Losses | kW | |||
| Maximum Shield Temperature | K | |||
| Neutron Shield Thickness | mm | |||
| Sacrificial REBCO Lifetime | years | |||
| Core Magnet Coil Lifetime | years |

With the observed neutron flux magnitudes, the sacrificial section of the core magnet coil will see a % reduction in its critical current after just over year at which point it will need to be replaced. The remaining portion of the REBCO in the core magnet coil will have a lifetime of at least years. The model used in Fig. [18](https://arxiv.org/html/2602.20564v1#S4.F18) assumes the material composition is the same through out the core magnet coil and as a result shows that % of the coil would see a high neutron flux. The final coil design will utilize neutron shielding materials in these regions such as tungsten borides or metal hydrides in order to reduce the neutron mean free path length and reduce the high flux area to % of the coil cross section. The lifetime of the steel in the structural over-band is expected to be significantly longer than the REBCO and therefore will not be replaced during the operational lifetime of the core magnet. This level of degradation is considered acceptable due to the modularity of the levitated dipole concept. As discussed in Section [2.3](https://arxiv.org/html/2602.20564v1#S2.SS3), there will be a short two week downtime period each year for maintenance and repair, which is comparable to many other mature power generation methods [11](https://arxiv.org/html/2602.20564v1#bib.bib94). The core magnet can be removed and replaced with a fresh magnet within this time period, allowing maintenance to take place on the damaged coil external to the reaction chamber, significantly reducing cost and maintaining a high plant availability. The cost of these replacements and the effects of the two week downtime have been included in the pricing model used to constrain the optimization process and were found to not make a significant impact on the economic viability of the plant.

In total % of the fusion neutrons pass into the region bounded by the first closed flux surface, . The majority of the energy carried by these neutrons gets deposited as heat in the shield, however some of the incident energy gets absorbed in endothermic neutron multiplication reactions and a larger portion gets scattered or reflected back out towards the first wall beyond the last closed flux surface, . The neutron multiplication and scattering in the outer tungsten tiles is sufficient for the total number of neutrons passing through to equal times the rate of neutrons being produced in the fusion reaction. The energy of these multiplied and scattered neutrons has been moderated down to the range of MeV as shown in Fig. [19](https://arxiv.org/html/2602.20564v1#S4.F19). This lower energy will have a small impact on the effectiveness of the tritium breeding blanket as discussed in Section [2.2.6](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS6).

Figure [18](https://arxiv.org/html/2602.20564v1#S4.F18) shows that the wall loading for Reactor A peaks at a value of MW m-2 on the outboard side of the of the core magnet. This is significantly lower than equivalent power tokamaks which range from MW m-2 depending on the size of the device Sorbom and others [[2015](https://arxiv.org/html/2602.20564v1#bib.bib43)], Aymar et al. [[2002](https://arxiv.org/html/2602.20564v1#bib.bib83)]. This results in the tungsten outer layer of the neutron shield reaching the MW-year m-2 limit National Academies of Sciences, Engineering, and Medicine [[2021](https://arxiv.org/html/2602.20564v1#bib.bib26)] after years on the outboard side and years on the inboard side. However, unlike those devices, all the heat deposited in the shield cannot be actively extracted until the magnet is docked. In total, Reactor A experiences MW of neutron induced heating and MW of radiative heating from the plasma. The heating from isotope decay has not been included in this model as it is only expected to contribute W m-3 after long periods of neutron irradiation Windsor et al. [[2022](https://arxiv.org/html/2602.20564v1#bib.bib39)].

The neutron heating, as shown in Fig. [20](https://arxiv.org/html/2602.20564v1#S4.F20), penetrates further into the shield. During a levitation cycle, the majority of the energy deposited in the shield is radiated away at the surface to the assumed first wall. Practicalities such as tritium retention may change this temperature in future designs. A 2D heat transfer model was constructed in COMSOL to calculate the required shield temperatures to support this radiative cooling. The neutron heating was exported from OpenMC and applied as a volumetric source, while the bremsstrahlung and prompt heating were applied as boundary heat load. The outer surface of the shield was assumed to have an emissivity of and a thermal break with a W m-2K-1 conductance was inserted between the outer tungsten tiles and the layer. A thermal break with this conductance is required in order to keep the heat conducted to the neutron shield reservoir low and encourage radiative cooling. The inner surface of the neutron shield was set to to mimic the effect of the on-board shield reservoir. The results of this modeling are shown in Fig. [20](https://arxiv.org/html/2602.20564v1#S4.F20) where the tungsten tiles in Reactor A reach a maximum steady state temperature of K which is well below the design constraint of K, but above the recrystallization temperature Richou et al. [[2020](https://arxiv.org/html/2602.20564v1#bib.bib77)], Suslova et al. [[2014](https://arxiv.org/html/2602.20564v1#bib.bib78)]. As long as the shield is maintained at these elevated temperatures it is possible that the onset of the degraded mechanical properties can be delayed until other forms of damage dominate. The energy that does not get radiated away at the surface is conducted inwards to the on-board reservoir. We calculate that % of the neutron power deposited in the shield will need to be stored in the on-board reservoir and extracted during the docking procedure.

At these temperatures the lifetime of the tungsten tiles is also determined by the rate of thermal creep which acts to deform the tiles from their manufactured specifications. This rate is determined by the temperature, tungsten grain size, and material stress which can be controlled by varying the tungsten tile size. Up to a grain size of m, stresses below MPa result in creep processes dominated by diffusion Webb et al. [[2019](https://arxiv.org/html/2602.20564v1#bib.bib37)] which can give part lifetimes in excess of a year. Determining the final tile size. and therefore their creep limited lifetime, requires a detailed design of the mounting mechanism of the tiles, which is outside the scope of this study.

At a preliminary level, the neutron shielding presented in this study satisfies all the requirements of an economically viable DT fusion power plant without the use of advanced materials. Further advancements in neutron shielding material science will only aid in the shield performance, allowing for more compact reactor designs and higher overall fusion power outputs.

| Name | Reactor A | Reactor B | Units |
| Plasma | MW | ||
4He heating |
|||
4He heating |
|||
| Auxiliary heating | |||
| Plasma Radiation | |||
| Conduction | |||
| First Wall | 733 | 261 | MW |
| Neutron Free Power | |||
| Blanket Energy Multiplication | |||
| Plasma Radiation | |||
| Core Magnet Black Body Radiation | |||
| Plasma Conduction | |||
| Neutron Shield | 7.76 | 2.65 | MW |
| Neutron Free Power | |||
| Endothermic Effects | |||
| Plasma Radiation | |||
Prompt 4He Heating |
|||
| Black Body Radiation | |||
| Core Magnet | 16.4 | 9.97 | kW |
| Neutron Heating | |||
| Photon Heating | |||
| Electrical Heating | |||
| Conductive Heating | |||
| Plant | MW | ||
| Fusion Power | |||
| Thermal Power | |||
| Total Electrical Power | |||
| Cryogenic Cooling | |||
| Plasma Heating Wall Power | |||
| Net Electric Power |

### 4.4 Power Balance

Combining the results from the previous sections the net electrical power of the reactor and the remaining full power balance can be calculated. The results of this calculation are provided in Table [9](https://arxiv.org/html/2602.20564v1#S4.T9) and visualized in Fig. [21](https://arxiv.org/html/2602.20564v1#S4.F21). Starting in the plasma, the total heating is sourced from the auxiliary heating power and charged fusion products. The auxiliary power is assumed to be deposited entirely in the bad curvature region to enable some control over the location of the pressure peak. The heating from the fusion particles is split between prompt losses to the surface of the core magnet neutron shield and the good and bad curvature regions. Of the particles that are not lost to the neutron shield, it was assumed that % of the energy was deposited in the good curvature region with the remainder depositing their energy in the bad curvature region based on initial results from the ASCOT5 model in Section [4.2](https://arxiv.org/html/2602.20564v1#S4.SS2). The energy deposited in the good curvature region is assumed to be converted to radiation and is included with the bremsstrahlung losses in the total radiation tally, . All energy in the plasma is lost either through radiation or conduction to . The fraction of neutron power and radiated power that gets directly deposited in the first wall is determined by the OpenMC calculations discussed in Section [4.3](https://arxiv.org/html/2602.20564v1#S4.SS3). Extra energy is generated by neutron induced exothermic reactions in the Li2O breeder blanket. The first wall also serves to capture the significant amounts of black body radiation emanating from the surface of the core magnet neutron shield, which indirectly captures the majority of the energy deposited in the shield. The bremsstrahlung and prompt losses to the neutron shield are assumed to be entirely balanced by black body radiation as they do not penetrate far into the shield volume. The deeper penetrating neutron power is then split between endothermic losses, black body radiation, and conduction to the thermal reservoir according to both the OpenMC model and the COMSOL neutron shield heat transfer model in Section [4.3](https://arxiv.org/html/2602.20564v1#S4.SS3). It is worth noting here that the endothermic effects in the neutron shield tungsten tiles removes of the useful thermal power of the plant. This aids the problem of cooling the neutron shield, but reduces the thermal power of the overall plant. This is not only because of the direct energy loss but also because of the loss of exothermic reactions that would have been available if a tritium breeding blanket was mounted on the core magnet. However, the reduction in shield thickness granted by using tungsten over other materials more than makes up for this loss by reducing the overall size of the plant.

The total thermal power is therefore the sum of the total power deposited in the first wall and the power deposited in the neutron shield reservoir. The total electrical power is then calculated assuming a electrical conversion efficiency. The electrical power required to cool the magnet is calculated using an efficiency of % (Section [2.2.3](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS3)) which is applied to the total heating power in the cryogenic region. The total efficiency of the auxiliary heating systems is assumed to be % which is then used to calculate the required total electrical power. Finally the net electrical power is calculated using Eq. ([20](https://arxiv.org/html/2602.20564v1#S3.E20)) to give a net output power of MW for Reactor A and MW for Reactor B.

## 5 Discussion

The final operating points are plotted in Fig. [22](https://arxiv.org/html/2602.20564v1#S4.F22) with their associated “operating contours” obtained by changing the core temperature at constant and device index, , as defined in Eq. ([8](https://arxiv.org/html/2602.20564v1#S3.E8)). Due to the temperature dependence of and the imposed constraint on the plant overnight capital cost, these optimized reactors are designed such that their operational contours are tangent to, or close to tangent to, the contour as this minimizes the scaling constant given the constraint on the overnight capital cost. Therefore, this optimization process has produced reactors with lower operating temperatures, in the range of keV, than would be expected for a tokamak Sorbom and others [[2015](https://arxiv.org/html/2602.20564v1#bib.bib43)], Rutherford and others [[2024](https://arxiv.org/html/2602.20564v1#bib.bib42)] or stellarator Lion and others [[2025](https://arxiv.org/html/2602.20564v1#bib.bib41)] DT fusion power plants. This is likely to change as more is understood about the scaling laws that govern the energy confinement time in a levitated dipole.

The assumption that these reactors will be is only valid if a smaller demonstration device, which we will call Tahi, displays adequate plasma performance. Tahi will be of a similar physical size as OpenStar’s current device, Junior Chisholm and others [[2026](https://arxiv.org/html/2602.20564v1#bib.bib12)] (a m diameter core magnet inside a m vacuum vessel), with more than MW of available auxiliary heating power. The aim of Tahi is to achieve triple products in excess of keV s m-3 with keV ions in the smallest possible form factor. The detailed design and final operating point of Tahi will be covered in a future publication.

In order for these reactors to be , Tahi will need to show double products above the required Bohm-like and gyro-Bohm-like scaled operational contours shown in Fig. [22](https://arxiv.org/html/2602.20564v1#S4.F22) calculated using Eq. ([8](https://arxiv.org/html/2602.20564v1#S3.E8)). For core temperatures of keV, Bohm-like scaling would require Tahi to show double products in excess of s m-3 for Reactor A and s m-3 for Reactor B. In both cases if Tahi were to show gyro-Bohm-like scaling, the requirement on the double product would be less than s m-3 therefore implying the reactors shown here would be .

The confinement time scaling in Eq. ([8](https://arxiv.org/html/2602.20564v1#S3.E8)) can also be applied to data from the LDX device Davis et al. [[2014](https://arxiv.org/html/2602.20564v1#bib.bib13)], which had a measured confinement time of ms, to obtain a bound on the expected performance of Tahi. Conservatively applying a Bohm-like scaling from this device implies that a keV s m-3 triple product can be achieved with a T core magnet. Additionally, LDX confined a plasma that was susceptible to significant charge exchange losses and as such was never ionized all the way to Boxer et al. [[2010](https://arxiv.org/html/2602.20564v1#bib.bib11)]. This, along with other possible effects caused by the drastic increase in available heating power over previous experiments, will only aid the plasma performance in Tahi further implying that Bohm-like scaling from LDX should provide a conservative lower bound. Therefore, we assume the upper performance bound to be 10 times the calculated lower bound as shown in Fig. [22](https://arxiv.org/html/2602.20564v1#S4.F22). As a point of comparison, a similar analysis on historical tokamak data yields an uplift factor of between 40 and 100 Wurzel and Hsu [[2022](https://arxiv.org/html/2602.20564v1#bib.bib38)]. It then becomes clear that some increase in performance over purely Bohm-like scaling is needed in order for either reactor to be given Bohm-like scaling from LDX, with Reactor B needing a more significant increase. However, the modest performance gain required for Reactor A would likely be achieved by fully ionizing the plasma in Tahi.

In the event that Tahi does not reach the double products outlined above, the reactors presented here would be . This would in turn either require an increase in the LCOE or the size, and therefore overnight capital cost, of the plant beyond the values set as constraints in this optimization. However, it is more likely, given the conservative scalings we have used, that Tahi will show the performance required for a Reactor A in the Bohm-like scaling case. Additionally, if Tahi were to show gyro-Bohm-like scaling or outperform the Bohm-like targets then this would allow for smaller, more capitally efficient plants such as Reactor B to be built.

## 6 Conclusions

This study has proposed two design points for first of a kind levitated dipole DT fusion reactors, a larger Reactor A with a total thermal power of MW ( MWe) and another smaller Reactor B producing MW of thermal power ( MWe). The levitated dipole allows for simple magnet geometries and stable steady state operation without damaging disruption-like events. The lack of a fusion relevant dipole experiment and the engineering design challenges associated with levitating a superconducting magnet within a fusing DT plasma have, until this study, been seen as the main detractor to the concept.

This work presents high level designs for two critical components of the levitated dipole that were previously thought to be impractically difficult: The large, high field core magnet and its neutron shield. The core magnet leverages advancements in superconducting technology to both produce strong magnetic fields ( T) and maintain a steady state operating current through the use of an on-board superconducting power supply. The shape of the core magnet coil was optimized to reduce mechanical strains to % with the help of a structural over-band. An internal low-field region was also created to house the superconducting power supply and other required on-board systems. These factors allow the presented core magnet structure to be built using traditional methods and materials. The neutron shielding we present here successfully attenuates the DT neutron flux down to acceptable levels, only depositing kW of heating into the cryogenic region and allowing for partial magnet lifetimes of year and full magnet lifetimes on the order of years. The neutron shield itself is constructed from layers of tungsten and , which allows the neutron shield to operate at the extreme temperatures ( K) required for radiative cooling to the first wall.

The large vacuum vessel will be constructed using a two layer approach. The outer layer will support close to the full loads of the vacuum and core magnet and will be built from reinforced concrete, enabling the large vessel diameters required for a levitated dipole fusion rector. This construction also allows excess room for a tritium breeding blanket mounted to the outside of the inner vacuum vessel. With assistance from neutron reflective core magnet shield, the space available for the tritium breeder blanket allows for tritium breeding ratios in excess of without the use of expensive molten salts and neutron multipliers.

These designs show that the engineering of a practically sized levitated dipole reactor is feasible. The presented reactors set performance requirements that a sub-scale demonstration device will need to exceed in order to fully validate the designs. This analysis in turn showed that levitated dipoles will likely need to show better than Bohm-like scaling in order for the reactor designs presented in this study to be valid. Both reactors were also designed with economic constraints in mind, leveraging the inherent modularity of the dipole which allows for easy replacement of the core magnet to compensate for the shorter coil lifetime. Hence, these design points are not only physically feasible, but they are also expected to be economically attractive.

## Appendix A Geometry Factors

In Section [3.1](https://arxiv.org/html/2602.20564v1#S3.SS1) we have derived the 0D power balance and confinement time relations using plasma averaged quantities to capture the effect of the highly peaked pressure profile. However, it is more convenient to index these relations using values measured at the pressure peak. To convert between peak and average values, we utilize the formalism of Wurzel and Hsu Wurzel and Hsu [[2022](https://arxiv.org/html/2602.20564v1#bib.bib38)] to define factors that capture the geometric effect of the plasma:

| (26) |

where is the volume average of quantity and is the value of measured at the pressure peak. The quantities of interest for a power balance are the fusion power density

| (27) |

bremsstrahlung power density

| (28) |

and the conductive power losses

| (29) |

Also useful for the study of dipoles are the geometric factors for local plasma :

| (30) |

and for the energy confinement time:

| (31) |

where, as discussed in Section [3.1](https://arxiv.org/html/2602.20564v1#S3.SS1), in this last case the average is taken only over the outer midplane as the transport there dominates:

| (32) |

Typically these values, aside from due to the strong dependence on in , are assumed to be constant for all operating points of any given device. While this remains true for variation in temperature in a dipole, Fig. [23](https://arxiv.org/html/2602.20564v1#A1.F23) shows that changing the pressure of the device, and therefore also the device , also has an effect on the geometry factors. For the standard factors , , and the dependence captures the overall expansion of the plasma as discussed in Section [2.1.3](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS3). The and factors on the other hand show very different behavior. Increased edge pressures result in more peaked local profiles, as expected from the lack of a limit on as the plasma expands. The large value of in the case of Bohm-like scaling () indicates that the quantity is close to uniform along the plasma outer midplane.

## References

-
The ITER design.
Plasma Physics and Controlled Fusion 44 (5), pp. 519.
External Links:
[Document](https://dx.doi.org/10.1088/0741-3335/44/5/304)Cited by:[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p5.12),[§4](https://arxiv.org/html/2602.20564v1#S4.p1.7). -
High-temperature superconducting switches and rectifiers.
Note: World Intellectual Property Organization (WIPO)International publication
Cited by:
[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1). -
Convection electric fields and the diffusion of trapped magnetospheric radiation.
Journal of Geophysical Research (1896-1977) 74 (9), pp. 2169–2181.
External Links:
[Document](https://dx.doi.org/10.1029/JA074i009p02169)Cited by:[§2.1](https://arxiv.org/html/2602.20564v1#S2.SS1.p1.7). -
Turbulent inward pinch of plasma confined by a levitated dipole magnet.
Nature Phys 6 (3), pp. 207–212.
External Links:
[Document](https://dx.doi.org/10.1038/nphys1510)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p2.1),[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.1),[§2.1.2](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS2.p1.15),[§5](https://arxiv.org/html/2602.20564v1#S5.p4.6). -
Material selection charts for optimised radiation shielding.
Materials Today 88, pp. 36–44.
External Links:
[Document](https://dx.doi.org/10.1016/j.mattod.2025.05.007)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p2.4). -
ENDF/B-VII.1 Nuclear Data for Science and Technology: Cross Sections, Covariances, Fission Product Yields and Decay Data.
Nuclear Data Sheets 112 (12), pp. 2887–2996.
External Links:
[Document](https://dx.doi.org/10.1016/j.nds.2011.11.002)Cited by:[Figure 10](https://arxiv.org/html/2602.20564v1#S2.F10),[Figure 10](https://arxiv.org/html/2602.20564v1#S2.F10.3.2),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p1.7). -
Design and initial results from the “Junior” Levitated Dipole Experiment.
Fusion Engineering and Design 223, pp. 115551.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2025.115551)Cited by:[§2.2.1](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS1.p3.1),[§5](https://arxiv.org/html/2602.20564v1#S5.p2.7). -
Pressure profiles of plasmas confined in the field of a magnetic dipole.
Plasma Phys. Control. Fusion 56 (9), pp. 095021.
External Links:
[Document](https://dx.doi.org/10.1088/0741-3335/56/9/095021)Cited by:[§5](https://arxiv.org/html/2602.20564v1#S5.p4.6). -
The growing energy footprint of artificial intelligence.
Joule 7 (10), pp. 2191–2194.
External Links:
[Document](https://dx.doi.org/10.1016/j.joule.2023.09.004)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1). -
Appendix: Data Handbook of Material Properties and Cryostat Design.
In Experimental Techniques for Low-Temperature Measurements: Cryostat Design, Material Properties and Superconductor Critical-Current Testing,
pp. 0.
External Links: ISBN 978-0-19-857054-7
Cited by:
[§2.2.3](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS3.p3.2),[Table 3](https://arxiv.org/html/2602.20564v1#S3.T3),[Table 3](https://arxiv.org/html/2602.20564v1#S3.T3.24.2),[§4.1](https://arxiv.org/html/2602.20564v1#S4.SS1.p4.6). -
[11]
(2025-11)
Electric power monthly.
Technical report
U.S. Energy Information Administration.
Cited by:
[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p3.5). -
Effects of time-dependent electric fields on geomagnetically trapped radiation.
Journal of Geophysical Research (1896-1977) 70 (11), pp. 2503–2516.
External Links:
[Document](https://dx.doi.org/10.1029/JZ070i011p02503)Cited by:[§2.1](https://arxiv.org/html/2602.20564v1#S2.SS1.p1.7). -
ICRF system efficiency.
Fusion Engineering and Design 156, pp. 111641.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2020.111641)Cited by:[§2.2.7](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS7.p3.1). -
The effect of fast neutron irradiation on the superconducting properties of REBCO coated conductors with and without artificial pinning centers.
Superconductor Science and Technology 31 (4), pp. 044006.
External Links:
[Document](https://dx.doi.org/10.1088/1361-6668/aaadf2)Cited by:[§3.2.3](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS3.p3.3),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p2.11). -
Design and Performance of Metal Hydride Composite Neutron Shields for Compact, High-Power Fusion Reactors.
Fusion Science and Technology 0 (0), pp. 1–16.
External Links:
[Document](https://dx.doi.org/10.1080/15361055.2025.2514910)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p3.3). -
Influence of mechanical stress on electron transport properties of second-generation high-temperature superconducting tapes.
Low Temperature Physics 49 (8), pp. 994–997.
External Links:
[Document](https://dx.doi.org/10.1063/10.0020169)Cited by:[§3.3](https://arxiv.org/html/2602.20564v1#S3.SS3.p4.5),[§4.1](https://arxiv.org/html/2602.20564v1#S4.SS1.p6.7). -
Design and initial operation of the LDX facility.
Fusion Engineering and Design 81 (20), pp. 2371–2380.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2006.07.002)Cited by:[§2.2.1](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS1.p1.2). -
Production and study of high-beta plasma confined by a superconducting dipole magneta).
Phys. Plasmas 13 (5), pp. 056111.
External Links:
[Document](https://dx.doi.org/10.1063/1.2186616)Cited by:[§2.2.7](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS7.p1.1). -
Magnetohydrodynamic stability in a levitated dipole.
Phys. Plasmas 6 (9), pp. 3431–3434.
External Links:
[Document](https://dx.doi.org/10.1063/1.873601)Cited by:[§2.1](https://arxiv.org/html/2602.20564v1#S2.SS1.p1.7),[§3.2.2](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS2.p1.3). -
Turbulent fluctuations during pellet injection into a dipole confined plasma torus.
Phys. Plasmas 24 (1), pp. 012506.
External Links:
[Document](https://dx.doi.org/10.1063/1.4973828)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.8),[§2.1.2](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS2.p1.15). -
High-tc superconducting transformer-rectifiers: principle, realization, and applications.
Superconductor Science and Technology 38 (4), pp. 043001.
External Links:
[Document](https://dx.doi.org/10.1088/1361-6668/adb80a)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1),[§4.1](https://arxiv.org/html/2602.20564v1#S4.SS1.p3.2). -
A field-controlled high-temperature superconducting switch: experiment and simulation.
IEEE Transactions on Applied Superconductivity 35 (5), pp. 1–5.
External Links:
[Document](https://dx.doi.org/10.1109/TASC.2025.3539269)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1). -
Plasma Production by Electron Cyclotron Heating on the Internal Coil Device Mini-RT.
Japanese Journal of Applied Physics 45 (6R), pp. 5197.
External Links:
[Document](https://dx.doi.org/10.1143/JJAP.45.5197)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p2.1). -
Self-Consistent Modeling of the
cof HTS Devices: How Accurate do Models Really Need to Be?. IEEE Transactions on Applied Superconductivity 24 (6), pp. 1–8. External Links:[Document](https://dx.doi.org/10.1109/TASC.2014.2326925)Cited by:[§3.2.1](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS1.p3.5). -
Superconducting electric aircraft powertrain mass reduction by wireless rotor energisation.
Ph.D. Thesis, Te Herenga Waka – Victoria University of Wellington.
External Links:
[Document](https://dx.doi.org/10.26686/wgtn.22351555)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p3.1). -
The SPARC Toroidal Field Model Coil Program.
IEEE Transactions on Applied Superconductivity 34 (2), pp. 1–16.
External Links:
[Document](https://dx.doi.org/10.1109/TASC.2023.3332613)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p4.1),[§4.1](https://arxiv.org/html/2602.20564v1#S4.SS1.p1.4). -
A D-3He fusion reactor based on a dipole magnetic field.
Nucl. Fusion 30 (11), pp. 2405.
External Links:
[Document](https://dx.doi.org/10.1088/0029-5515/30/11/018)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p3.1),[§2.2.7](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS7.p1.1),[§4](https://arxiv.org/html/2602.20564v1#S4.p3.8). -
A dipole field fusion reactor.
Comments on Plasma Physics and Controlled Fusion 11, pp. 147–151.
Cited by:
[§1](https://arxiv.org/html/2602.20564v1#S1.p2.1),[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.1). -
Convective cells and transport in toroidal plasmas.
The Physics of Fluids 22 (11), pp. 2097–2107.
External Links:
[Document](https://dx.doi.org/10.1063/1.862520)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.4). -
Thermal decomposition of titanium hydride and its application to low pressure hydrogen control.
Journal of Vacuum Science & Technology A 2 (1), pp. 16–21.
External Links:
[Document](https://dx.doi.org/10.1116/1.572617)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p3.3). -
Gyrokinetic simulations of plasma turbulence in a Z-pinch using a moment-based approach and advanced collision operators.
Journal of Plasma Physics 89 (2), pp. 905890214.
External Links:
[Document](https://dx.doi.org/10.1017/S0022377823000284)Cited by:[§2.1.4](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS4.p2.2). -
Flux pump for hts magnets.
IEEE Transactions on Applied Superconductivity 21 (3), pp. 1628–1631.
External Links:
[Document](https://dx.doi.org/10.1109/TASC.2010.2093115)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1). -
Climate Change 2021 – The Physical Science Basis: Working Group I Contribution to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change.
Cambridge University Press.
External Links:
[Document](https://dx.doi.org/10.1017/9781009157896), ISBN 978-1-009-15789-6 Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1). -
Physics basis for the advanced tokamak fusion power plant, ARIES-AT.
Fusion Engineering and Design 80 (1), pp. 25–62.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2005.06.352)Cited by:[§2.2.7](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS7.p3.1). -
Plasma Confinement in a Levitated Magnetic Dipole.
PLasma Physics Reports 23 (9), pp. 742–750.
Cited by:
[§2.1.2](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS2.p1.15). -
Helium catalysed D–D fusion in a levitated dipole.
Nucl. Fusion 44 (1), pp. 193.
External Links:
[Document](https://dx.doi.org/10.1088/0029-5515/44/1/021)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p3.1),[§2.2.1](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS1.p1.2),[§4.1](https://arxiv.org/html/2602.20564v1#S4.SS1.p6.7),[§4](https://arxiv.org/html/2602.20564v1#S4.p3.8),[§4](https://arxiv.org/html/2602.20564v1#S4.p4.5). -
Convective cell formation in a levitated dipole.
Physics of Plasmas 7 (6), pp. 2733–2737.
External Links:
[Document](https://dx.doi.org/10.1063/1.874123)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.4). -
Electrostatic drift modes in a closed field line configuration.
Physics of Plasmas 9 (2), pp. 395–400.
External Links:
[Document](https://dx.doi.org/10.1063/1.1431594)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.8). -
Interchange modes in a collisional plasma.
Phys. Plasmas 7 (10), pp. 3837–3840.
External Links:
[Document](https://dx.doi.org/10.1063/1.1287915)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.8). -
YBCO and bi2223 coils for high field lts/hts nmr magnets: hts-hts joint resistivity.
IEEE Transactions on Applied Superconductivity 23 (3), pp. 6800704–6800704.
External Links:
[Document](https://dx.doi.org/10.1109/TASC.2013.2243195)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p1.1). -
Gyrokinetic Simulations of Turbulent Transport in a Ring Dipole Plasma.
Phys. Rev. Lett. 103 (5), pp. 055003.
External Links:
[Document](https://dx.doi.org/10.1103/PhysRevLett.103.055003)Cited by:[§2.1.4](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS4.p2.2). -
New Tungsten Borides, Their Stability and Outstanding Mechanical Properties.
The Journal of Physical Chemistry Letters 9 (12), pp. 3470–3477.
External Links:
[Document](https://dx.doi.org/10.1021/acs.jpclett.8b01262)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p3.3). -
Impact of space radiation on lithium-ion batteries: A review from a radiation electrochemistry perspective.
Journal of Energy Storage 100, pp. 113406.
External Links:
[Document](https://dx.doi.org/10.1016/j.est.2024.113406)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1). -
A half-wave superconducting transformer-rectifier flux pump using jc(b) switches.
Superconductor Science and Technology 35 (3), pp. 035009.
External Links:
[Document](https://dx.doi.org/10.1088/1361-6668/ac4f3d)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1). -
Stellaris: A high-field quasi-isodynamic stellarator for a prototypical fusion power plant.
Fusion Engineering and Design 214, pp. 114868.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2025.114868)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1),[§3.3](https://arxiv.org/html/2602.20564v1#S3.SS3.p2.3),[§5](https://arxiv.org/html/2602.20564v1#S5.p1.6). -
Application of dimensionless parameter scaling techniques to the design and interpretation of magnetic fusion experiments.
Plasma Physics and Controlled Fusion 50 (4), pp. 043001.
External Links:
[Document](https://dx.doi.org/10.1088/0741-3335/50/4/043001)Cited by:[§2.1.5](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS5.p1.1). -
The Solar Wind-Magnetosphere-Ionosphere System.
Science 288 (5473), pp. 1987–1991.
External Links:
[Document](https://dx.doi.org/10.1126/science.288.5473.1987)Cited by:[§2.1](https://arxiv.org/html/2602.20564v1#S2.SS1.p1.7). -
The Impact of Disruptions on the Economics of a Tokamak Power Plant.
Fusion Science and Technology 80 (5), pp. 636–652.
External Links:
[Document](https://dx.doi.org/10.1080/15361055.2023.2229675)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1). -
A statistical model to forecast and simulate energy demand in the long-run.
Smart Energy 7, pp. 100084.
External Links:
[Document](https://dx.doi.org/10.1016/j.segy.2022.100084)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1). -
Development and large volume production of extremely high current density YBa2Cu3O7 superconducting wires for fusion.
Scientific Reports 11 (1), pp. 2084.
External Links:
[Document](https://dx.doi.org/10.1038/s41598-021-81559-z)Cited by:[§3.2.1](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS1.p3.5),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p1.7). -
Bringing Fusion to the U.S. Grid.
The National Academies Press.
External Links:
[Document](https://dx.doi.org/10.17226/25991)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p6.10),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p5.12). -
Improved beta (local beta 1) and density in electron cyclotron resonance heating on the RT-1 magnetosphere plasma.
Nucl. Fusion 55 (5), pp. 053019.
External Links:
[Document](https://dx.doi.org/10.1088/0029-5515/55/5/053019)Cited by:[§2.2.7](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS7.p1.1). -
Ion cyclotron heating experiments in magnetosphere plasma device RT-1.
AIP Conf. Proc. 1689 (1), pp. 040002.
External Links:
[Document](https://dx.doi.org/10.1063/1.4936485)Cited by:[§2.2.7](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS7.p1.1). -
Tensile, Fracture, Fatigue Life, and Fatigue Crack Growth Rate Behavior of Structural Materials for the ITER Magnets: The European Contribution.
AIP Conference Proceedings 711 (1), pp. 176–183.
External Links:
[Document](https://dx.doi.org/10.1063/1.1774567)Cited by:[§4.1](https://arxiv.org/html/2602.20564v1#S4.SS1.p6.7). -
A superconducting joint for GdBa2Cu3O7--coated conductors.
NPG Asia Materials 6 (5), pp. e98–e98.
External Links: ISSN 1884-4057,
[Document](https://dx.doi.org/10.1038/am.2014.18)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p1.1). -
Anomalous transport processes near a levitated coil immersed in a plasma.
Nuclear Fusion 32 (10), pp. 1725.
External Links:
[Document](https://dx.doi.org/10.1088/0029-5515/32/10/I03)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.4),[§2.1.2](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS2.p1.15). -
Hydrogen desorption kinetics of hafnium hydride powders.
Journal of Nuclear Materials 604, pp. 155499.
External Links:
[Document](https://dx.doi.org/10.1016/j.jnucmat.2024.155499)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p3.3). -
Convection in an asymmetrically sourced Z pinch.
Physics of Plasmas 8 (12), pp. 5151–5157.
External Links:
[Document](https://dx.doi.org/10.1063/1.1413228)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.4). -
Gyrokinetic linear theory of the entropy mode in a Z pinch.
Phys. Plasmas 13 (6), pp. 062102.
External Links:
[Document](https://dx.doi.org/10.1063/1.2205830)Cited by:[§2.1.4](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS4.p2.2). -
Recrystallization at high temperature of two tungsten materials complying with the ITER specifications.
Journal of Nuclear Materials 542, pp. 152418.
External Links:
[Document](https://dx.doi.org/10.1016/j.jnucmat.2020.152418)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p5.3),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p6.11). -
OpenMC: A state-of-the-art Monte Carlo code for research and development.
Annals of Nuclear Energy 82, pp. 90–97.
External Links:
[Document](https://dx.doi.org/10.1016/j.anucene.2014.07.048)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p4.4),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p1.7). -
Stability of plasmas confined by magnetic fields.
Annals of Physics 1 (2), pp. 120–140.
External Links:
[Document](https://dx.doi.org/10.1016/0003-4916%2857%2990055-6)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.1). -
MANTA: a negative-triangularity NASEM-compliant fusion pilot plant.
Plasma Physics and Controlled Fusion 66 (10), pp. 105006.
External Links:
[Document](https://dx.doi.org/10.1088/1361-6587/ad6708)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1),[§3.3](https://arxiv.org/html/2602.20564v1#S3.SS3.p2.3),[§5](https://arxiv.org/html/2602.20564v1#S5.p1.6). -
High- plasma formation and observation of peaked density profile in RT-1.
Nucl. Fusion 51 (6), pp. 063034.
External Links:
[Document](https://dx.doi.org/10.1088/0029-5515/51/6/063034)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p2.1). -
Physics and technology conditions for attaining tritium self-sufficiency for the DT fuel cycle.
Fusion Engineering and Design 81 (8), pp. 1131–1144.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2005.07.035)Cited by:[§3.2.5](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS5.p1.8). -
Particle Diffusion in the Radiation Belts.
Physics and Chemistry in Space, Vol. 7, Springer, Berlin, Heidelberg.
External Links:
[Document](https://dx.doi.org/10.1007/978-3-642-65675-0), ISBN 978-3-642-65677-4 978-3-642-65675-0 Cited by:[§2.1](https://arxiv.org/html/2602.20564v1#S2.SS1.p1.7). -
Review of metallic phase change materials for high heat flux transient thermal management applications.
Applied Energy 258, pp. 113955.
External Links:
[Document](https://dx.doi.org/10.1016/j.apenergy.2019.113955)Cited by:[§3.2.5](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS5.p2.10),[Table 3](https://arxiv.org/html/2602.20564v1#S3.T3),[Table 3](https://arxiv.org/html/2602.20564v1#S3.T3.24.2). -
Neutronic Comparison of Tritium-Breeding Performance of Candidate Tritium-Breeding Materials.
Plasma Science and Technology 5 (5), pp. 1995–2000.
External Links:
[Document](https://dx.doi.org/10.1088/1009-0630/5/5/011)Cited by:[Figure 11](https://arxiv.org/html/2602.20564v1#S2.F11),[Figure 11](https://arxiv.org/html/2602.20564v1#S2.F11.3.2),[§2.2.6](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS6.p2.2). -
Reversible tensile strain dependence of the critical current in YBCO coated conductor tapes.
Physica C: Superconductivity and its Applications 463–465, pp. 736–741.
External Links:
[Document](https://dx.doi.org/10.1016/j.physc.2007.04.319)Cited by:[§3.3](https://arxiv.org/html/2602.20564v1#S3.SS3.p4.5). -
Nonlinear convective motion in plasmas.
Physics Reports 105 (4), pp. 227–328.
External Links:
[Document](https://dx.doi.org/10.1016/0370-1573%2884%2990096-6)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.4). -
Kinetic stability of electrostatic plasma modes in a dipolar magnetic field.
Physics of Plasmas 8 (10), pp. 4414–4426.
External Links:
[Document](https://dx.doi.org/10.1063/1.1399058)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.8). -
Long mean-free path collisional stability of electromagnetic modes in axisymmetric closed magnetic field configurations.
Physics of Plasmas 9 (1), pp. 201–211.
External Links:
[Document](https://dx.doi.org/10.1063/1.1424309)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.8). -
Versatile fusion source integrator AFSI for fast ion and neutron studies in fusion devices.
Nucl. Fusion 58 (1), pp. 016023.
External Links:
[Document](https://dx.doi.org/10.1088/1741-4326/aa92e9)Cited by:[§4.2](https://arxiv.org/html/2602.20564v1#S4.SS2.p1.5). -
ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets.
Fusion Engineering and Design 100, pp. 378–405.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2015.07.008)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1),[§3.3](https://arxiv.org/html/2602.20564v1#S3.SS3.p2.3),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p5.12),[§4](https://arxiv.org/html/2602.20564v1#S4.p1.7),[§4](https://arxiv.org/html/2602.20564v1#S4.p3.8),[§5](https://arxiv.org/html/2602.20564v1#S5.p1.6). -
Space Power Facility-Capabilities for Space Environmental Testing Within a Single Facility.
Technical report
Technical Report NASA/TM-2013-217816, NASA.
Cited by:
[§2.2.5](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS5.p2.1),[§4](https://arxiv.org/html/2602.20564v1#S4.p5.1). -
Differential Evolution – A Simple and Efficient Heuristic for global Optimization over Continuous Spaces.
Journal of Global Optimization 11 (4), pp. 341–359.
External Links:
[Document](https://dx.doi.org/10.1023/A%3A1008202821328)Cited by:[§3.2](https://arxiv.org/html/2602.20564v1#S3.SS2.p1.1). -
Recrystallization and grain growth induced by ELMs-like transient heat loads in deformed tungsten samples.
Scientific Reports 4 (1), pp. 6845.
External Links:
[Document](https://dx.doi.org/10.1038/srep06845)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p5.3),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p6.11). -
The Scrape-Off Layer in Alcator C-Mod: Transport, Turbulence, and Flows.
Fusion Science and Technology 51 (3), pp. 342–356.
External Links:
[Document](https://dx.doi.org/10.13182/FST07-A1426)Cited by:[§2.1.4](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS4.p2.2). -
Behavior and properties of refractory metals.
Stanford University Press.
External Links: ISBN 0-8047-0162-8
Cited by:
[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p5.3). -
On fully superconducting rectifiers and fluxpumps. a review. part 2: commutation modes, characteristics and switches.
Cryogenics 21 (5), pp. 267–277.
External Links: ISSN 0011-2275,
[Document](https://dx.doi.org/https%3A//doi.org/10.1016/0011-2275%2881%2990002-3)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1). -
High-performance orbit-following code ASCOT5 for Monte Carlo simulations in fusion plasmas.
arXiv.
External Links: 1908.02482,
[Document](https://dx.doi.org/10.48550/arXiv.1908.02482)Cited by:[§4.2](https://arxiv.org/html/2602.20564v1#S4.SS2.p1.5). -
Ion Cyclotron Heating in a Levitated Dipole Fusion Reactor.
In Proceedings of the 25th Topical Conference on Radio-Frequency Power in Plasmas,
Cited by:
[§2.2.7](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS7.p3.1). -
Magnetic-field scaling of dimensionally similar tokamak discharges.
Phys. Rev. Lett. 65 (19), pp. 2390–2393.
External Links:
[Document](https://dx.doi.org/10.1103/PhysRevLett.65.2390)Cited by:[§3.1](https://arxiv.org/html/2602.20564v1#S3.SS1.p1.2). -
An overview of creep in tungsten and its alloys.
International Journal of Refractory Metals and Hard Materials 82, pp. 69–80.
External Links:
[Document](https://dx.doi.org/10.1016/j.ijrmhm.2019.03.022)Cited by:[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p7.3). -
High temperature superconducting flux pumps for contactless energization.
Crystals 12 (6).
Note: All Open Access, Gold Open Access, Green Open Access
External Links:
[Document](https://dx.doi.org/10.3390/cryst12060766)Cited by:[§2.2.2](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS2.p2.1). -
I-mode: an H-mode energy confinement regime with L-mode particle transport in Alcator C-Mod.
Nuclear Fusion 50 (10), pp. 105005.
External Links:
[Document](https://dx.doi.org/10.1088/0029-5515/50/10/105005)Cited by:[§2.1.4](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS4.p2.2),[§3.3](https://arxiv.org/html/2602.20564v1#S3.SS3.p3.9). -
Acceleration techniques for the direct use of CAD-based geometry in fusion neutronics analysis.
Fusion Engineering and Design 85 (10), pp. 1759–1765.
External Links:
[Document](https://dx.doi.org/10.1016/j.fusengdes.2010.05.030)Cited by:[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p1.7). -
Critical current characterisation of SuperOx YBCO 2G HTS superconducting wire.
figshare.
External Links:
[Document](https://dx.doi.org/10.6084/m9.figshare.13708690.v1)Cited by:[§3.2.1](https://arxiv.org/html/2602.20564v1#S3.SS2.SSS1.p3.5). -
Tungsten boride shields in a spherical tokamak fusion power plant.
Nuclear Fusion 61 (8), pp. 086018.
External Links:
[Document](https://dx.doi.org/10.1088/1741-4326/ac09ce)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p1.4),[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p2.4). -
Activation and transmutation of tungsten boride shields in a spherical tokamak.
Nuclear Fusion 62 (3), pp. 036009.
External Links:
[Document](https://dx.doi.org/10.1088/1741-4326/ac4866)Cited by:[§2.2.4](https://arxiv.org/html/2602.20564v1#S2.SS2.SSS4.p8.6),[§4.3](https://arxiv.org/html/2602.20564v1#S4.SS3.p5.12). -
How Will Energy Demand Develop in the Developing World?.
Journal of Economic Perspectives 26 (1), pp. 119–138.
External Links:
[Document](https://dx.doi.org/10.1257/jep.26.1.119)Cited by:[§1](https://arxiv.org/html/2602.20564v1#S1.p1.1). -
Progress toward fusion energy breakeven and gain as measured against the Lawson criterion.
Phys. Plasmas 29 (6), pp. 062103.
External Links:
[Document](https://dx.doi.org/10.1063/5.0083990)Cited by:[Appendix A](https://arxiv.org/html/2602.20564v1#A1.p1.5),[§5](https://arxiv.org/html/2602.20564v1#S5.p4.6). -
Magnetospheric Vortex Formation: Self-Organized Confinement of Charged Particles.
Physical Review Letters 104 (23), pp. 235004.
External Links:
[Document](https://dx.doi.org/10.1103/PhysRevLett.104.235004)Cited by:[§2.1.1](https://arxiv.org/html/2602.20564v1#S2.SS1.SSS1.p1.1).