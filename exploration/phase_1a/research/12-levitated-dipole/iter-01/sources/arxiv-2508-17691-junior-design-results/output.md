---
source: "https://arxiv.org/html/2508.17691v1"
source_type: "url"
extracted_at: "2026-03-29T19:06:28.173009+00:00"
content_hash_sha256: "f47dca29461271d0a84f82552ae20fe808dccbfe3c7ffe1e6ae5606146bfd0b3"
backend: "trafilatura"
title: "Design and initial results from the “Junior” Levitated Dipole Experiment"
author: "C S Chisholm craig chisholm nz"
---

# Design and initial results from the “Junior” Levitated Dipole Experiment

###### Abstract

OpenStar Technologies is a private fusion company exploring the levitated dipole concept for commercial fusion energy production. OpenStar has manufactured a new generation of levitated dipole experiment, called “Junior”, leveraging recent advances made in high-temperature superconducting magnet technologies. Junior houses a T REBCO high-temperature superconducting magnet in a m vacuum chamber, with plasma heating achieved via kW of electron cyclotron resonance heating power. Importantly, this experiment integrates novel high temperature superconductor power supply technology on board the dipole magnet. Recently OpenStar has completed first experimental campaigns with the Junior experiment, achieving first plasmas in late 2024. Experiments conducted with the full levitated system are planned for 2025. This article provides an overview of the main results from these experiments and details improvements planned for future campaigns.

[openstar]organization=OpenStar Technologies Limited, addressline=20 Glover Street, Ngauranga, city=Wellington, postcode=6035, country=New Zealand

## 1 Introduction

Dipole confined plasmas were first proposed as a fusion concept by Hasegawa in 1987 [[1](https://arxiv.org/html/2508.17691v1#bib.bib1)] after spacecraft observations of strongly peaked plasma pressure and density profiles in magnetospheres due to strong inward particle pinch caused by turbulence [[2](https://arxiv.org/html/2508.17691v1#bib.bib2), [3](https://arxiv.org/html/2508.17691v1#bib.bib3)]. The magnetospheres of Earth and Jupiter are examples of stable plasmas confined by a simple dipole field found in nature [[4](https://arxiv.org/html/2508.17691v1#bib.bib4), [5](https://arxiv.org/html/2508.17691v1#bib.bib5)] and laboratory dipole magnetic confinement dates back to supported “terrellae” experiments conducted by Birkeland in the early twentieth century [[6](https://arxiv.org/html/2508.17691v1#bib.bib6)]. The Collisionless Terrella Experiment (CTX) is a supported dipole experiment which studied the phase-space evolution of dipole-trapped energetic plasma in the presence of drift-resonant fluctuations in the 1990s through to the 2010s [[7](https://arxiv.org/html/2508.17691v1#bib.bib7), [8](https://arxiv.org/html/2508.17691v1#bib.bib8), [9](https://arxiv.org/html/2508.17691v1#bib.bib9), [10](https://arxiv.org/html/2508.17691v1#bib.bib10), [11](https://arxiv.org/html/2508.17691v1#bib.bib11)]. The Space Plasma Environment Research Facility is a supported terrella-like experiment for magnetospheric plasma physics studies [[12](https://arxiv.org/html/2508.17691v1#bib.bib12), [13](https://arxiv.org/html/2508.17691v1#bib.bib13)]. Supported magnetic dipoles are limited to very low collisionality regimes where pitch angle scattering into the loss cone is slow enough to compare to cross field turbulent transport [[14](https://arxiv.org/html/2508.17691v1#bib.bib14)].

Magnetic dipoles without mechanical supports are required to study transport with higher collisionality and for fusion relevance. Levitated magnetic dipoles have been investigated in the Levitated Dipole Experiment (LDX) [[15](https://arxiv.org/html/2508.17691v1#bib.bib15)] and the Ring Trap 1 (RT-1) experiment [[16](https://arxiv.org/html/2508.17691v1#bib.bib16)]. In particular, the LDX experiment was able to show peaked plasma pressure profiles resulting from a turbulent pinch when the dipole coil was levitated but not while it was supported [[17](https://arxiv.org/html/2508.17691v1#bib.bib17)]. Peaked density profiles were also observed in RT-1 where they achieved peak local ( is the ratio of the plasma and magnetic pressures) [[18](https://arxiv.org/html/2508.17691v1#bib.bib18)].

The “Junior” experiment, built by OpenStar Technologies, is a new generation of dipole confined plasma experiment which builds on the pioneering work of LDX and RT-1. In both experiments, a toroidal superconducting current ring, the “core magnet” is levitated in a vacuum chamber by a second electromagnet, the “top magnet” which provides an antisymmetric stabilized levitation magnetic field. The LDX core magnet was made from Nb3Sn which is a low temperature superconductor (LTS) [[19](https://arxiv.org/html/2508.17691v1#bib.bib19)] and was inductively charged using an additional charging coil [[20](https://arxiv.org/html/2508.17691v1#bib.bib20)]. The RT-1 core magnet is made from first generation high temperature superconductor (HTS) BI-2223 and is charged using current leads in the docked position [[16](https://arxiv.org/html/2508.17691v1#bib.bib16)]. The RT-1 magnet current decays by % after hours of levitation due to finite HTS joint resistance [[16](https://arxiv.org/html/2508.17691v1#bib.bib16)].

The Junior experiment is a proof of concept aiming to replicate results of LDX with a second generation HTS core magnet whilst integrating novel HTS power supplies onboard the core magnet to maintain current during levitation. The successful integration of these novel HTS technologies opens a pathway to higher field magnets which enable the production of magnetically confined plasmas with fusion relevant densities and temperatures. Beyond these initial engineering goals, the Junior facility is an attractive platform for the investigation of fundamental plasma physics phenomena including but not limited to multi-scale plasma turbulence and energy cascades [[9](https://arxiv.org/html/2508.17691v1#bib.bib9)], self-organization phenomena [[21](https://arxiv.org/html/2508.17691v1#bib.bib21), [22](https://arxiv.org/html/2508.17691v1#bib.bib22)], high- () plasma stability regimes [[23](https://arxiv.org/html/2508.17691v1#bib.bib23), [15](https://arxiv.org/html/2508.17691v1#bib.bib15), [24](https://arxiv.org/html/2508.17691v1#bib.bib24), [25](https://arxiv.org/html/2508.17691v1#bib.bib25)], “artificial radiation belt” formation [[7](https://arxiv.org/html/2508.17691v1#bib.bib7), [8](https://arxiv.org/html/2508.17691v1#bib.bib8)], non-linear Alfvén wave dynamics [[26](https://arxiv.org/html/2508.17691v1#bib.bib26)], wave-particle and wave-wave interactions in magnetospheric geometries [[27](https://arxiv.org/html/2508.17691v1#bib.bib27), [28](https://arxiv.org/html/2508.17691v1#bib.bib28)], the effect of anisotropy on stability and confinement [[29](https://arxiv.org/html/2508.17691v1#bib.bib29)], and energetic particle dynamics with hot electron interchanges modes [[30](https://arxiv.org/html/2508.17691v1#bib.bib30), [15](https://arxiv.org/html/2508.17691v1#bib.bib15)]. In this article, we present an overview of the “Junior” levitated dipole experiment and some initial results from the first plasma campaign, conducted with the magnet mechanically supported.

## 2 Physics Basis

A levitated dipole is an antisymmetric configuration that confines a torus shaped plasma that surrounds the core magnet. With diamagnetic but no driven currents, the plasma equilibrium consists of a purely poloidal field, i.e. toroidal confinement without toroidal fields. In Junior, near to the core magnet, there is a first closed flux surface (FCFS) created by the limiting inner bore. The outer boundary or last closed flux surface (LCFS) can be alternatively set by a magnetic separatrix or an outboard limiter. An example of a diverted plasma equilibrium is shown in Fig. [1](https://arxiv.org/html/2508.17691v1#S1.F1).

In contrast to most magnetic confinement approaches, which require average good curvature and magnetic shear for stability, dipole confined plasmas have bad curvature everywhere outside of the pressure peak and magnetohydrodynamic (MHD) stability is achieved through plasma compressibility [[31](https://arxiv.org/html/2508.17691v1#bib.bib31), [32](https://arxiv.org/html/2508.17691v1#bib.bib32), [33](https://arxiv.org/html/2508.17691v1#bib.bib33)]. Inside the pressure peak, there is absolute good curvature and plasma instabilities should be damped such that transport may be classical as particle drifts conserve poloidal magnetic flux when the toroidal field is zero. For a sufficiently gentle plasma pressure gradient, defined by , with the plasma pressure, the differential flux tube volume, and the ratio of specific heats, dipole confined plasmas are stable to interchange and ballooning instabilities [[23](https://arxiv.org/html/2508.17691v1#bib.bib23)].

The differential flux tube volume is given by where is the equatorial radius so that the marginal stability condition, , implies a pressure gradient given by . This constrains the peak pressure in the dipole according to the edge pressure and flux-tube geometry as [[23](https://arxiv.org/html/2508.17691v1#bib.bib23)].
This is the stationary profile for low-frequency interchange-like turbulence which leads to the condition . Therefore, the particle density (which is constant within a flux tube) scales as where is the number of particles per flux tube, which is constant. The pressure profile is linked to the temperature and density profiles as leading to a peaked temperature profile given by [[21](https://arxiv.org/html/2508.17691v1#bib.bib21), [17](https://arxiv.org/html/2508.17691v1#bib.bib17)].

The location of the pressure peak has been observed to be strongly influenced by the heat source of the plasma [[34](https://arxiv.org/html/2508.17691v1#bib.bib34)] but is not strongly influenced by whether the particle source is external or internal [[35](https://arxiv.org/html/2508.17691v1#bib.bib35)]. Central heating in a levitated dipole plasma can create a strong central pressure gradient such that [[21](https://arxiv.org/html/2508.17691v1#bib.bib21)]. For a marginally stable plasma satisfying , an interchange of flux tubes does not transport net energy and leaves the temperature and density profiles unchanged. Due to adiabatic compression, cool source particles from the edge are heated as they move inwards towards the peak and hot particles from the peak are cooled as they move outwards and expand.

Since the peak plasma pressure depends on the edge pressure, the energy and particle balance is partly determined by the physics of plasma flowing along field lines into the walls. It has been observed that when the core magnet is supported rather than levitated, parallel losses result in density profiles which are approximately uniform in flux space so that the number of particles per flux tube peaks on the outside [[17](https://arxiv.org/html/2508.17691v1#bib.bib17)].

In Junior, a separatrix may be formed that defines the LCFS when the core magnet has lower current and the top magnet current must be increased to maintain levitation as shown in Fig. [1](https://arxiv.org/html/2508.17691v1#S1.F1). For some conditions with high plasma , the plasma may also shift outward to return to an outboard limited configuration. As the presence of a separatrix may change the stability properties of edge and scrape off layer plasma [[36](https://arxiv.org/html/2508.17691v1#bib.bib36)], this operational flexibility allows the edge stability to be studied experimentally.

## 3 Experiment Overview

The Junior system described in this article was designed and built in under years at a cost of M USD and serves as a proof of concept for powering the Core Magnet using an HTS transformer rectifier [[37](https://arxiv.org/html/2508.17691v1#bib.bib37), [38](https://arxiv.org/html/2508.17691v1#bib.bib38)] known as a flux pump [[39](https://arxiv.org/html/2508.17691v1#bib.bib39), [40](https://arxiv.org/html/2508.17691v1#bib.bib40)] housed inside the magnet coils. As such, many of the key design choices were based on the design of LDX [[33](https://arxiv.org/html/2508.17691v1#bib.bib33)] which saw electron temperatures and densities of eV and m-3 [[21](https://arxiv.org/html/2508.17691v1#bib.bib21)].

### 3.1 Vacuum Vessel Size and Material

The vacuum vessel is made from 304L stainless steel and has an inner radius of m. The maximum internal height of the vacuum vessel is m and the wall thickness is mm. Figure [2](https://arxiv.org/html/2508.17691v1#S3.F2) shows a photo of the vacuum vessel. There are a large number of vacuum ports available for plasma diagnostic installation. Eight ISO-F ports with sizes ranging from DN200 to DN500 are equally spaced around the chamber on the mid-plane. On the bottom of the vessel, four ISO-K flanges (one DN100 and three DN250) are equally spaced on a circle of radius m and each flange is at an angle of from the horizontal. On the top of the vessel, four DN250ISO-K flanges are attached in positions corresponding to the lower ports at an angle of from the horizontal. A custom DN1240 ISO-F flange on the bottom of the vessel allows the core magnet cryostat to be brought in and out of the vessel in one piece, decoupling the magnet and vacuum vessel engineering and allowing for modular upgrades of the core magnet. For recooling, the magnet is docked at the bottom flange and all necessary ground connections are fed through the bottom flange. At the top of the chamber a custom re-entrant flange allows for an independent cryostat for the top magnet.

| Parameter | Design Value | This Work |
|---|---|---|
| T | T | |
| max at windings | T | T |
| max at windings | T | T |
| Current | kA | A |
| Ampere-turns | MA-turns | kA-turns |
| Total flux | Wb | Wb |
| Stored energy | MJ | MJ |
| Free bore | mm | |
| Tape length | km | |
| Inductance | H | |
| Floating mass | kg |

### 3.2 Core Magnet Description

The Junior core magnet is a kA, T magnet consisting of 14 non-insulated (NI) [[41](https://arxiv.org/html/2508.17691v1#bib.bib41)] solder impregnated HTS coils [[42](https://arxiv.org/html/2508.17691v1#bib.bib42)] connected in series. Key design parameters of the core magnet and actual values used for the first plasma campaign are summarized in Tab. [1](https://arxiv.org/html/2508.17691v1#S3.T1). The magnet is wrapped in multi layer insulation and contained within a 304L stainless steel shell with feed-throughs for cooling and electrical connections while docked. The magnet is nominally cooled to K using forced helium and all diagnostic sensors are contained within the cryostat shell. The total joint resistance of the coils is estimated to be . The vacuum vessel walls and the cryostat shell limit the usable flux to Wb.

During plasma experiments, the core magnet has no connection to external services and current will be maintained using an HTS flux pump (see Sec. [3.3](https://arxiv.org/html/2508.17691v1#S3.SS3)). The HTS circuit in the flux pump as well as iron yokes used for electromagnet switching are sensitive to magnetic field. A differential evolution algorithm [[43](https://arxiv.org/html/2508.17691v1#bib.bib43)] was used to optimize the distribution of current carrying HTS coils to achieve an adequately low flux such that iron shielding could be used to eliminate stray field at sensitive components. Figure [3](https://arxiv.org/html/2508.17691v1#S3.F3) shows a cross section of the core magnet after coil placement optimization.

### 3.3 Flux Pump Description

The core magnet is powered by a superconducting transformer rectifier [[44](https://arxiv.org/html/2508.17691v1#bib.bib44)], a type of “flux pump” [[39](https://arxiv.org/html/2508.17691v1#bib.bib39), [40](https://arxiv.org/html/2508.17691v1#bib.bib40)]. A schematic representation of this flux pump is shown in Fig. [4](https://arxiv.org/html/2508.17691v1#S3.F4). An AC waveform is applied on the normal conducting primary circuit. A stepped down AC voltage is produced on the HTS secondary circuit. The waveform is rectified to the load by actuating two switches, which are parallel to the load, out of phase with each other. Each switch consists of lengths of HTS tape kept at an elevated operating temperature. Normal conducting electromagnets are used to apply magnetic field to the switch tape thus driving the switches into a partially resistive state thereby generating voltage. The tape is cut and joined to run back past the electromagnet without capturing magnetic flux in a loop of tape.

The rate of charging of the core magnet is determined by the switch voltages, the inductance of the magnet, and the resistance of the magnet. To maintain current during levitation, the switch voltages must be equal to roughly twice the magnet joint resistance multiplied by the magnet current.

### 3.4 Top Magnet Description

The top magnet is a wax impregnated double pancake HTS coil. The coil has been designed and tested to twice the current required to levitated the core magnet when the core magnet is operating at full current. This means that the core magnet can be levitated when operating at half current, allowing for the formation of a separatrix as shown in fig: [1](https://arxiv.org/html/2508.17691v1#S1.F1). Key parameters of the top magnet are given in Tab. [2](https://arxiv.org/html/2508.17691v1#S3.T2).

| Parameter | Design Value |
|---|---|
| T | |
| max at windings | T |
| Current | A |
| Ampere-turns | kA-turns |
| Tape length | km |
| Inductance | mH |

### 3.5 Plasma Heating Systems

Plasma heating is via electron cyclotron resonance heating (ECRH). Microwaves with a frequency of GHz are generated by two magnetron heads (Rell GEN15KW2I400-50-0). Each head is capable of generating up to 15 kW of microwave power. The magnetrons are connected to the vacuum chamber using WR430 waveguide and the interface between atmospheric pressure and vacuum pressure is a glass window (Muegge MW0003B-110DC). Similarly to the LDX experiment, we rely on “cavity heating” with small first pass absorption and multiple reflections from the vacuum vessel walls to achieve isotropic power distribution [[14](https://arxiv.org/html/2508.17691v1#bib.bib14)].

Microwaves are launched into the vessel using pieces of waveguide cut off at the Vlasov angle. The launchers are positioned at the mid-plane with the H-plane of the waveguide vertical in order to minimize directionality of the launchers and to ensure that microwaves are launched in X-mode [[45](https://arxiv.org/html/2508.17691v1#bib.bib45)]. Three stub tuners (Muegge GA1006) are installed on the atmosphere side of the waveguide windows to further minimize reflected power. In the near future, two klystron sources will be added to enable multiple frequency ECRH [[15](https://arxiv.org/html/2508.17691v1#bib.bib15), [21](https://arxiv.org/html/2508.17691v1#bib.bib21)]. These two additional sources are up to kW at GHz (Varian VA-936R12) and up to kW at GHz (Varian VA-911 P).

| Number | Location | (mm) | (m) | Turns |
|---|---|---|---|---|
| External | ||||
| External | ||||
| External | ||||
| External | ||||
| External | ||||
| External | ||||
| External | ||||
| External | ||||
| Internal | ||||
| Internal | ||||
| Internal | ||||
| Internal |

### 3.6 Diagnostics

There is very little restriction on space available for plasma diagnostics since levitated dipole experiments do not have any interlocking coils and importantly, do not need much space for coils on the outer walls of the vacuum vessel. The Junior plasma diagnostic set is illustrated in Fig [5](https://arxiv.org/html/2508.17691v1#S3.F5) along with calculated equilibrium flux contours in Fig [5](https://arxiv.org/html/2508.17691v1#S3.F5)(a). The plasma diagnostics set includes:

-
1.
A four chord microwave interferometer for line integrated electron density measurements [

[17](https://arxiv.org/html/2508.17691v1#bib.bib17)]. -
2.
a UV-VIS spectrometer for measurement of edge neutral spectra.

-
3.
Visible light cameras.

-
4.
Twelve magnetic flux loops (eight external to the vacuum vessel and four internal) for reconstruction of plasma pressure profiles [

[46](https://arxiv.org/html/2508.17691v1#bib.bib46)]. -
5.
Two cadmium-zinc-telluride (CZT) x-ray detectors

-
6.
A sodium-iodide (NaI) x-ray detector.

-
7.
A silicon drift detector (SDD).

-
8.
Langmuir probes.


The four chord interferometer consists of a single transmitter horn and four receiver horns. As microwaves transmit through the plasma they are phase shifted proportionally to the integrated electron density. This phase shift is measured by beating with a local oscillator which is sent through waveguide on the outside of the chamber and demodulating the signal [[17](https://arxiv.org/html/2508.17691v1#bib.bib17)]. The four chords pass through the plasma with tangency radii of m, m, m, and m. We intend to upgrade the interferometer with four additional channels doubling the span of tangency radii. Visible light data is collected using a UV-vis spectrometer (Avantes, Avaspec-2048) and horizontal (Basler a2A2448-105g5cBAS) and top mounted (Basler a2A4096-44g5cBAS) visible light video cameras.

Magnetic measurements are made using 12 circular flux loops attached to the vacuum chamber which produce a voltage proportional to changing magnetic flux . Eight of the flux loops are wound around the outside of the vacuum chamber where their bandwidth is limited to Hz due to screening currents in the vessel walls [[47](https://arxiv.org/html/2508.17691v1#bib.bib47)] but they are able to capture large flux due to their large size. The remaining four flux loops are located inside the chamber and are significantly smaller so have a greater number of turns to compensate for the reduced flux. Two of the internal flux loops are mounted on the top impact attenuator which limits the forces on the core magnet to in the event of an upward crash ( is the acceleration due to gravity). Table [3](https://arxiv.org/html/2508.17691v1#S3.T3) details the radii and vertical positions of the eight external and four internal flux loops as well as the number of turns in each coil. All of the coils are oriented horizontally and concentric with the core magnet and the positions and radii were optimized for measurement sensitivity given spatial constraints imposed by other mechanical structures. The voltage signals are fed into integrator circuits to obtain magnetic flux which can then be used to reconstruct plasma pressure [[46](https://arxiv.org/html/2508.17691v1#bib.bib46), [22](https://arxiv.org/html/2508.17691v1#bib.bib22)]. Additionally, the un-integrated signals of the internal flux loops will be used as a feedback signal in the levitation control loop to compensate for rapid changes in the plasma diamagnetic current which affects the coupling between the top and core magnets.

Since heating in the Junior experiment is achieved using electron cyclotron resonance, the plasma energy is largely electron stored energy with high plasma . We use pulse height analyzers to distinguish photon energies from bremsstrahlung radiation and construct histograms from which electron temperature can be inferred. Specifically we employ one NaI detector (Bicron, IA-1378) from which we integrate the counts to obtain total x-ray power between keV and MeV with a viewing angle of . Two cadmium zinc telluride (CZT) detectors (eV Products SPEAR) with viewing angles of and distinguish photons in the range keV to keV with fields of view determined by lead collimators. Finally, a silicon drift detector (AmpTek XR-100SDD) with a viewing angle of measures photons with energy keV and a resolution of eV. We intend to install an x-ray camera which will allow us to observe the localization of hot electrons and assist with pressure profile reconstruction [[46](https://arxiv.org/html/2508.17691v1#bib.bib46)].

Edge density and temperature measurements are made using Langmuir probes. Specifically, we have installed a fixed triple probe [[48](https://arxiv.org/html/2508.17691v1#bib.bib48)] and an array of probes subtending an azimuthal angle of with equal angular spacing at a radius of m similar to the probe array which was installed on LDX [[49](https://arxiv.org/html/2508.17691v1#bib.bib49)]. Two thirds of the probes are typically operated in floating potential configuration for measurement of electric field fluctuations [[35](https://arxiv.org/html/2508.17691v1#bib.bib35)] and the remaining probes will be operated in ion saturation configuration for local ion density measurements. The vertical probe array can be adjusted over a range of m, as indicated in Fig. [5](https://arxiv.org/html/2508.17691v1#S3.F5)(a).

## 4 Initial Results

Figure [6](https://arxiv.org/html/2508.17691v1#S3.F6)(a) shows the temperature of the core magnet during a cooling cycle. The magnet was cooled from room temperature to operating temperature ( K) in hours with a cooling rate of K/minute and temperature differences around coils controlled at K. A charging campaign with the flux pump is shown in Fig [6](https://arxiv.org/html/2508.17691v1#S3.F6)(b) where the magnet was charged to A which is % of its design current achieving the greatest magnetic stored energy delivered by an HTS flux pump to date. The flux pump was stopped and restarted a number of times to test magnet discharge.

The first plasma campaign on Junior was conducted late 2024 using 4He as the fueling gas and a reduced diagnostics set. Seventeen shots were completed over two days of operation. The results in these shots were dominated by neutrals coming off of the wall (additional pumping has since been installed and installation of a glow discharge cleaning system is underway). Because the dipole was not levitated, end point losses resulted in flat line integrated density profiles (also observed in LDX [[17](https://arxiv.org/html/2508.17691v1#bib.bib17)]). Figure [7](https://arxiv.org/html/2508.17691v1#S3.F7)(a) shows fueling, pressure, and heating data from a typical plasma shot numbered . Line integrated densities from four chord interferometer data are shown in Fig [7](https://arxiv.org/html/2508.17691v1#S3.F7)(b), the flat line integrated density profile indicates a hollow density consistent with a radially localized plasma source. A color photo of the plasma is shown in Fig. [7](https://arxiv.org/html/2508.17691v1#S3.F7)(c).

## 5 Conclusion

The Junior experiment is a new levitated dipole experiment integrating novel HTS power supply technology into a non-insulated HTS magnet. The low cost and rapid construction of the Junior experiment can be attributed to the relative simplicity of levitated dipole as a concept. The same reduced complexity, in particular the lack of interlocking coils, allows a large surface area on the vacuum vessel to be used for prototyping plasma diagnostics. Similarly, large access to the plasma will enable testing of low power ion cyclotron resonance heating in dipole magnetic plasmas as well as initial divertor investigations including strike point control and shaping coils or edge electric field effects from a biased divertor. The first experimental campaign on Junior resulted in 17 plasma shots across two days with the magnet in supported configuration. In this configuration, interferometer data shows a localized plasma density source near ECRH resonance with transport dominated by parallel losses to the stainless steel supports.

The decoupling of magnet and vacuum vessel engineering means that the core magnet can easily be removed and upgraded or swapped out for different designs with relatively little down time. This platform flexibility will enable prototype magnet and fusion technology development in parallel to the construction of larger facilities for fusion relevant plasmas. Homed in New Zealand, we invite external researchers to use the Junior experiment to investigate fundamental plasma physics phenomena of interest to basic plasma science, space physics, and fusion science.

## Acknowledgments

We thank A. Hasegawa for encouragement and insightful discussions and G.M. Wallace for support and discussions during first plasma operations. We gratefully acknowledge support from the entire OpenStar team. Funding was provided by OpenStar Technologies Limited and we acknowledge additional support from the New Zealand government through Ara Ake Limited.

## References

- [1] A. Hasegawa, A dipole field fusion reactor, Comments on Plasma Physics and Controlled Fusion 11 (3) (1987) 147–151.
-
[2]
D. Melrose, Rotational effects on the distribution of thermal plasma in the
magnetosphere of jupiter, Planetary and Space Science 15 (2) (1967) 381–393.
[doi:10.1016/0032-0633(67)90202-4](https://doi.org/10.1016/0032-0633(67)90202-4). -
[3]
T. A. Farley, A. D. Tomassian, M. Walt, Source of high-energy protons in the
van allen radiation belt, Physical Review Letters 25 (1) (1970) 47–49.
[doi:10.1103/physrevlett.25.47](https://doi.org/10.1103/physrevlett.25.47). -
[4]
T. Gold, Motions in the magnetosphere of the earth, Journal of Geophysical
Research 64 (9) (1959) 1219–1224.
[doi:10.1029/jz064i009p01219](https://doi.org/10.1029/jz064i009p01219). -
[5]
T. Gold, Plasma and magnetic fields in the solar system, Journal of Geophysical
Research 64 (11) (1959) 1665–1674.
[doi:10.1029/jz064i011p01665](https://doi.org/10.1029/jz064i011p01665). - [6] A. Egeland, Kristian Birkeland: The first space scientist, Astrophysics and space science library, Springer, Dordrecht, 2005.
-
[7]
H. P. Warren, M. E. Mauel, Observation of chaotic particle transport induced by
drift-resonant fluctuations in a magnetic dipole field, Physical Review
Letters 74 (8) (1995) 1351–1354.
[doi:10.1103/physrevlett.74.1351](https://doi.org/10.1103/physrevlett.74.1351). -
[8]
H. P. Warren, M. E. Mauel, Wave-induced chaotic radial transport of energetic
electrons in a laboratory terrella experiment, Physics of Plasmas 2 (11)
(1995) 4185–4194.
[doi:10.1063/1.871044](https://doi.org/10.1063/1.871044). -
[9]
B. A. Grierson, M. W. Worstell, M. E. Mauel, Global and local characterization
of turbulent and chaotic structures in a dipole-confined plasma, Physics of
Plasmas 16 (5) (Apr. 2009).
[doi:10.1063/1.3099319](https://doi.org/10.1063/1.3099319). -
[10]
T. M. Roberts, M. E. Mauel, M. W. Worstell, Local regulation of interchange
turbulence in a dipole-confined plasma torus using current-collection
feedback, Physics of Plasmas 22 (5) (2015) 055702.
[doi:10.1063/1.4918352](https://doi.org/10.1063/1.4918352). -
[11]
T. M. Roberts, M. E. Mauel, M. C. Abler, B. K. Makansi, Imaging free-falling
particles for multipoint measurement of plasma fluctuations, Review of
Scientific Instruments 86 (8) (2015) 083510.
[doi:10.1063/1.4929407](https://doi.org/10.1063/1.4929407). -
[12]
Q. Xiao, Z. Wang, X. Wang, C. Xiao, X. Yang, J. Zheng, Conceptual design of
dipole research experiment (drex), Plasma Science and Technology 19 (3)
(2017) 035301.
[doi:10.1088/2058-6272/19/3/035301](https://doi.org/10.1088/2058-6272/19/3/035301). -
[13]
X. He, A. Mao, S. Apatenkov, Z. Wang, M. Sun, J. Zou, X. Wang, Topological
analysis of three-dimensional magnetic reconnection in sperf-arex for
simulated magnetopause events, Physics of Plasmas 30 (10) (2023) 102901.
[doi:10.1063/5.0168682](https://doi.org/10.1063/5.0168682). -
[14]
A. Hansen, ECRH in the levitated dipole experiment, in: AIP Conference
Proceedings, Vol. 595, AIP, 2001, pp. 362–365.
[doi:10.1063/1.1424211](https://doi.org/10.1063/1.1424211). -
[15]
D. T. Garnier, A. Hansen, M. E. Mauel, E. Ortiz, A. C. Boxer, J. Ellsworth,
I. Karim, J. Kesner, S. Mahar, A. Roach, Production and study of high-beta
plasma confined by a superconducting dipole magnet, Physics of Plasmas 13 (5)
(2006) 056111.
[doi:10.1063/1.2186616](https://doi.org/10.1063/1.2186616). -
[16]
J. Morikawa, Z. Yoshida, Y. Ogawa, S. Watanabe, Y. Yano, S. Mizumaki,
T. Tosaka, Y. Ohtani, M. Shibui, Development of a super-conducting levitated
coil system in the rt-1 magnetospheric confinement device, Fusion Engineering
and Design 82 (5–14) (2007) 1437–1442.
[doi:10.1016/j.fusengdes.2007.03.050](https://doi.org/10.1016/j.fusengdes.2007.03.050). -
[17]
A. C. Boxer, R. Bergmann, J. L. Ellsworth, D. T. Garnier, J. Kesner, M. E.
Mauel, P. Woskov, Turbulent inward pinch of plasma confined by a levitated
dipole magnet, Nature Physics 6 (3) (2010) 207–212.
[doi:10.1038/nphys1510](https://doi.org/10.1038/nphys1510). -
[18]
M. Nishiura, Z. Yoshida, H. Saitoh, Y. Yano, Y. Kawazura, T. Nogami,
M. Yamasaki, T. Mushiake, A. Kashyap, Improved beta (local beta
>1) and density in electron cyclotron resonance heating on the
RT-1 magnetosphere plasma, Nuclear Fusion 55 (5) (2015) 053019.
[doi:10.1088/0029-5515/55/5/053019](https://doi.org/10.1088/0029-5515/55/5/053019). -
[19]
A. Zhukovsky, M. Morgan, D. Garnier, A. Radovinsky, B. Smith, J. Schultz,
L. Myatt, S. Pourrahimi, J. Minervini, Design and fabrication of the cryostat
for the floating coil of the levitated dipole experiment (LDX), IEEE
Transactions on Appiled Superconductivity 10 (1) (2000) 1522–1525.
[doi:10.1109/77.828531](https://doi.org/10.1109/77.828531). -
[20]
A. Zhukovsky, J. Schultz, B. Smith, A. Radovinsky, D. Garnier, O. Filatov,
V. Beljakov, S. Egorov, V. Kuchinsky, A. Malkov, E. Bondarchouk,
V. Korsunsky, V. Sytnikov, Charging magnet for the floating coil of LDX,
IEEE Transactions on Appiled Superconductivity 11 (1) (2001) 1873–1876.
[doi:10.1109/77.920214](https://doi.org/10.1109/77.920214). -
[21]
J. Kesner, M. S. Davis, J. L. Ellsworth, D. T. Garnier, J. Kahn, M. E. Mauel,
P. Michael, B. Wilson, P. P. Woskov, Stationary density profiles in the
levitated dipole experiment: toward fusion without tritium fuel, Plasma
Physics and Controlled Fusion 52 (12) (2010) 124036.
[doi:10.1088/0741-3335/52/12/124036](https://doi.org/10.1088/0741-3335/52/12/124036). -
[22]
M. S. Davis, M. E. Mauel, D. T. Garnier, J. Kesner, Pressure profiles of
plasmas confined in the field of a magnetic dipole, Plasma Physics and
Controlled Fusion 56 (9) (2014) 095021.
[doi:10.1088/0741-3335/56/9/095021](https://doi.org/10.1088/0741-3335/56/9/095021). -
[23]
D. T. Garnier, J. Kesner, M. E. Mauel, Magnetohydrodynamic stability in a
levitated dipole, Physics of Plasmas 6 (9) (1999) 3431–3434.
[doi:10.1063/1.873601](https://doi.org/10.1063/1.873601). -
[24]
H. Saitoh, Z. Yoshida, J. Morikawa, Y. Yano, T. Mizushima, Y. Ogawa,
M. Furukawa, Y. Kawai, K. Harima, Y. Kawazura, Y. Kaneko, K. Tadachi,
S. Emoto, M. Kobayashi, T. Sugiura, G. Vogel, High- plasma formation
and observation of peaked density profile in rt-1, Nuclear Fusion 51 (6)
(2011) 063034.
[doi:10.1088/0029-5515/51/6/063034](https://doi.org/10.1088/0029-5515/51/6/063034). -
[25]
H. Saitoh, M. R. Stoneking, T. S. Pedersen, A levitated magnetic dipole
configuration as a compact charged particle trap, Review of Scientific
Instruments 91 (4) (2020) 043507.
[doi:10.1063/1.5142863](https://doi.org/10.1063/1.5142863). -
[26]
D. A. Kozlov, A. S. Leonovich, Polarization splitting of the alfvén wave
spectrum in a dipole magnetosphere with a rotating plasma, Plasma Physics
Reports 32 (9) (2006) 765–774.
[doi:10.1134/s1063780x06090078](https://doi.org/10.1134/s1063780x06090078). -
[27]
A. Kouznetsov, J. P. Freidberg, J. Kesner, Quasilinear theory of interchange
modes in a closed field line configuration, Physics of Plasmas 14 (10) (Oct.
2007).
[doi:10.1063/1.2773711](https://doi.org/10.1063/1.2773711). -
[28]
H. Saitoh, M. Nishiura, N. Kenmochi, Z. Yoshida, Experimental study on chorus
emission in an artificial magnetosphere, Nature Communications 15 (1) (2024)
861.
[doi:10.1038/s41467-024-44977-x](https://doi.org/10.1038/s41467-024-44977-x). -
[29]
A. N. Simakov, R. J. Hastie, P. J. Catto, Anisotropic pressure stability of a
plasma confined in a dipole magnetic field, Physics of Plasmas 7 (8) (2000)
3309–3318.
[doi:10.1063/1.874196](https://doi.org/10.1063/1.874196). -
[30]
B. Levitt, D. Maslovsky, M. E. Mauel, J. Waksman, Excitation of the
centrifugally driven interchange instability in a plasma confined by a
magnetic dipole, Physics of Plasmas 12 (5) (2005) 055703.
[doi:10.1063/1.1888685](https://doi.org/10.1063/1.1888685). -
[31]
M. Rosenbluth, C. Longmire, Stability of plasmas confined by magnetic fields,
Annals of Physics 1 (2) (1957) 120–140.
[doi:10.1016/0003-4916(57)90055-6](https://doi.org/10.1016/0003-4916(57)90055-6). -
[32]
I. B. Bernstein, E. A. Frieman, M. D. Kruskal, R. M. Kulsrud, An energy
principle for hydromagnetic stability problems, Proceedings of the Royal
Society of London. Series A. Mathematical and Physical Sciences 244 (1236)
(1958) 17–40.
[doi:10.1098/rspa.1958.0023](https://doi.org/10.1098/rspa.1958.0023). -
[33]
D. Garnier, A. Hansen, J. Kesner, M. Mauel, P. Michael, J. Minervini,
A. Radovinsky, A. Zhukovsky, A. Boxer, J. Ellsworth, I. Karim, E. Ortiz,
Design and initial operation of the LDX facility, Fusion Engineering and
Design 81 (20–22) (2006) 2371–2380.
[doi:10.1016/j.fusengdes.2006.07.002](https://doi.org/10.1016/j.fusengdes.2006.07.002). -
[34]
A. C. Boxer,
[Density profiles of plasmas confined by the field of a levitating dipole magnet](http://hdl.handle.net/1721.1/53195), Ph.D. thesis, Massachusetts Instititute of Technology (2008).

URL[http://hdl.handle.net/1721.1/53195](http://hdl.handle.net/1721.1/53195) -
[35]
D. T. Garnier, M. E. Mauel, T. M. Roberts, J. Kesner, P. P. Woskov, Turbulent
fluctuations during pellet injection into a dipole confined plasma torus,
Physics of Plasmas 24 (1) (Jan. 2017).
[doi:10.1063/1.4973828](https://doi.org/10.1063/1.4973828). - [36] J. Kesner, M. Mauel, Plasma confinement in a levitated magnetic dipole, Plasma Physics Reports 23 (1997) 742–750.
-
[37]
J. Geng, Y. Lin, C. W. Bumby, R. A. Badcock, High-tc superconducting
transformer-rectifiers: principle, realization, and applications,
Superconductor Science and Technology 38 (4) (2025) 043001.
[doi:10.1088/1361-6668/adb80a](https://doi.org/10.1088/1361-6668/adb80a). -
[38]
J. H. P. Rice, Increasing the current output of
high-temperature-superconducting transformer-rectifier circuits (8 2024).
[doi:10.26686/wgtn.26445619](https://doi.org/10.26686/wgtn.26445619). -
[39]
L. van de Klundert, H. ten Kate, Fully superconducting rectifiers and fluxpumps
part 1: Realized methods for pumping flux, Cryogenics 21 (4) (1981) 195–206.
[doi:10.1016/0011-2275(81)90195-8](https://doi.org/10.1016/0011-2275(81)90195-8). -
[40]
L. van de Klundert, H. ten Kate, On fully superconducting rectifiers and
fluxpumps. a review. part 2: Commutation modes, characteristics and switches,
Cryogenics 21 (5) (1981) 267–277.
[doi:10.1016/0011-2275(81)90002-3](https://doi.org/10.1016/0011-2275(81)90002-3). -
[41]
S. Hahn, D. K. Park, J. Bascunan, Y. Iwasa, Hts pancake coils without
turn-to-turn insulation, IEEE Transactions on Applied Superconductivity
21 (3) (2011) 1592–1595.
[doi:10.1109/TASC.2010.2093492](https://doi.org/10.1109/TASC.2010.2093492). -
[42]
Y. Li, D. Hu, J. Zhang, W. Wu, Z. Li, K. Ryu, Z. Hong, Z. Jin, Feasibility
study of the impregnation of a no-insulation hts coil using solder, IEEE
Transactions on Applied Superconductivity 28 (1) (2018) 1–5.
[doi:10.1109/TASC.2017.2773831](https://doi.org/10.1109/TASC.2017.2773831). - [43] K. Price, R. M. Storn, J. A. Lampinen, Differential Evolution A Practical Approach to Global Optimization, Springer, 2005.
-
[44]
B. Leuw, J. Geng, J. H. P. Rice, D. A. Moseley, R. A. Badcock, A half-wave
superconducting transformer-rectifier flux pump using jc(b) switches,
Superconductor Science and Technology 35 (3) (2022) 035009.
[doi:10.1088/1361-6668/ac4f3d](https://doi.org/10.1088/1361-6668/ac4f3d). - [45] T. H. Stix, Waves in plasmas, American Inst. of Physics, New York, NY, 1992, rev. and updated ed. of: The theory of plasma waves. 1962.
-
[46]
I. Karim, M. E. Mauel, J. L. Ellsworth, A. C. Boxer, D. T. Garnier, A. K.
Hansen, J. Kesner, E. E. Ortiz, Equilibrium reconstruction of anisotropic
pressure profile in the levitated dipole experiment, Journal of Fusion Energy
26 (1–2) (2007) 99–102.
[doi:10.1007/s10894-006-9033-6](https://doi.org/10.1007/s10894-006-9033-6). - [47] I. Karim, Equilibrium and stability studies of plasmas confined in a dipole magnetic field using magnetic measurements., Ph.D. thesis, Massachusetts Insistitute of Technology (2007).
-
[48]
K. A. Polzin, E. Blumhagen, A. C. Sherrod, T. Moeller, Behavior of triple
langmuir probes in non-equilibrium plasmas, in: AIAA Propulsion and Energy
2019 Forum, American Institute of Aeronautics and Astronautics, 2019, p.
3990.
[doi:10.2514/6.2019-3990](https://doi.org/10.2514/6.2019-3990). - [49] R. M. Bergmann, Characterization of low-frequency electric potential oscillations near the edge of a plasma confined by a levitated magnetic dipole., Master’s thesis, Massachusetts Institute of Technology (2009).