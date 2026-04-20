---
source: "https://www.nature.com/articles/s41467-025-58849-5?error=cookies_not_supported&code=fc2ea5c1-62fd-4887-9025-42620602244d"
source_type: "url"
extracted_at: "2026-04-20T04:49:46.848043+00:00"
content_hash_sha256: "5b5b9eb08ac964944a931702605aadb7194a6092d36245fb5849a7ab6dee2f7b"
backend: "trafilatura"
title: "Generation of field-reversed configurations via neutral beam injection - Nature Communications"
author: "Roche; T; Dettrick; S; Fontanilla; A; Gupta; Onofri; M; Romero; L C; Granstedt; Galeotti; L; Karbashewski; Yushmanov; P; E; Gota; H; I; R; V; J; Barnes; D C; Beall; Bolte; N G; Bui; D; Ceccherini; F; Clary; B; K; Nations; Necas; Nicks; G N; Y; G; Ufnal; Weixel; White; C; Wollenberg; Zhai; Ziaei"
---

## Abstract

We report evidence of successful generation of field-reversed configuration plasmas by neutral beam injection. This is achieved by trapping the steady-state beams in an initial seed plasma, hence providing a direct source of toroidally directed energetic ion current and increase plasma density and temperature until plasma and magnetic pressures become comparable. Magnetic flux trapping occurs gradually, and the change in topology from open field line to fully a formed field-reversed configuration is complete within ~ 10 ms. Field reversal is first established using a traditional metric and complemented by advanced reconstruction algorithms of the magnetic topology and plasma pressure profiles; observations of characteristic changes to fast-ion orbits inferred from magnetic fluctuations; and an experimentally validated model of field reversal by neutral beam injection. These results establish a field-reversed configuration formation method which may offer technological and economic advantages on a path to a future fusion energy system.

### Similar content being viewed by others

## Introduction

Most magnetically-confined plasma systems with an eye on a fusion energy application have a core of closed magnetic flux surfaces, of which the field-reversed configuration (FRC) is no exception. The FRC is interesting as a fusion reactor concept due to its compact nature, high power density (typical average *β* ~90%), axisymmetric geometry with simple circular confinement coils, and linear unrestricted divertors which can facilitate power, ash, and impurity removal. The FRC has been explored in many experimental facilities 1,2.

All FRC systems require an initial start-up method. Several approaches have successfully been implemented, creating a core of closed flux surfaces. These include electron-beam injection 3,4, even- and odd-parity rotating magnetic fields (RMF)

, spheromak merging

[5](https://www.nature.com/articles/s41467-025-58849-5#ref-CR5),[6](https://www.nature.com/articles/s41467-025-58849-5#ref-CR6), and theta pinch

[7](https://www.nature.com/articles/s41467-025-58849-5#ref-CR7). These differ in the physics and technology approaches for the startup. For example, the theta pinch method, which has received the most attention over the years, requires fast-pulsed power technology. In addition, one promising startup method failed to achieve field reversal, namely Neutral Beam Injection (NBI) in the 2XIIB experiments

[8](https://www.nature.com/articles/s41467-025-58849-5#ref-CR8),[9](https://www.nature.com/articles/s41467-025-58849-5#ref-CR9). Various speculations about the requirements for field-reversal by this means have been postulated

[10](https://www.nature.com/articles/s41467-025-58849-5#ref-CR10).

[11](https://www.nature.com/articles/s41467-025-58849-5#ref-CR11),[12](https://www.nature.com/articles/s41467-025-58849-5#ref-CR12)The Norman machine (also known as C-2W) at TAE Technologies, Inc. 13,14 was originally designed to use theta-pinch sections at each end to form, translate, collide, merge, and thermalize two FRCs in a central confinement vessel (CV). The resulting FRC is a suitable target for ionization and capture of the injected neutral beams. The beam ions enhance the stability of the plasma via large-orbit effects and help maintain plasma confinement by sourcing a fast-ion current

. The predecessors of C-2W at TAE had passed through several startup methods, beginning with an inductively accelerated ion ring in the C-1 facility

[15](https://www.nature.com/articles/s41467-025-58849-5#ref-CR15). The subsequent C-2 device was built to study NBI into the FRC

[16](https://www.nature.com/articles/s41467-025-58849-5#ref-CR16)based in part on simulations to optimize the neutral beam configuration. Later, after reports of rotational-shear stabilization

[17](https://www.nature.com/articles/s41467-025-58849-5#ref-CR17),[18](https://www.nature.com/articles/s41467-025-58849-5#ref-CR18)in the GDT experiments

[19](https://www.nature.com/articles/s41467-025-58849-5#ref-CR19), plasma guns were added, creating the C-2U facility

[20](https://www.nature.com/articles/s41467-025-58849-5#ref-CR20).

[21](https://www.nature.com#ref-CR21),[22](https://www.nature.com#ref-CR22),[23](https://www.nature.com#ref-CR23),[24](https://www.nature.com#ref-CR24),[25](https://www.nature.com/articles/s41467-025-58849-5#ref-CR25)The concept of steady state FRCs with current drive provided by neutral beam injection was studied by various authors in the 1980s 26,27,28,29,30. Indeed, theta-pinch experiments exhibited noticeable increases in the confinement time with the addition of NBI

. Simulations also addressed the steady-state concept

[31](https://www.nature.com/articles/s41467-025-58849-5#ref-CR31),[32](https://www.nature.com/articles/s41467-025-58849-5#ref-CR32).

[33](https://www.nature.com#ref-CR33),[34](https://www.nature.com#ref-CR34),[35](https://www.nature.com#ref-CR35),[36](https://www.nature.com/articles/s41467-025-58849-5#ref-CR36)In the present paper we demonstrate that in Norman, the combination of NBI with electrical biasing and other controls is sufficient to produce both startup of an FRC and its sustainment thereafter. This is achieved with inactive theta-pinch source sections. Moreover, in a major reconfiguration, both theta-pinch sections were removed, creating the modification known as Norm. This more compact configuration also achieves both startup and sustainment, with parameters similar to Norman.

## Results

### Machine configurations

Extensive details of the original configuration of Norman are given elsewhere 13,14.

Both the original and present forms are illustrated in Fig. [1](https://www.nature.com/articles/s41467-025-58849-5#Fig1). In the Norm configuration, plasmas primarily reside in the CV bounded at each end by divertors. Between the CV and divertors is a fueling region located between the M1 magnetic coil (closest to the CV) and the mirror plug (MP) (closest to the divertor). The M2 coil adjusts the field in the fueling region to facilitate neutral-gas ionization and refueling on field lines closer to the separatrix. Current is driven in the plasma by 8 neutral beams with 15 keV energy, that can deliver up to 13 MW of neutral power 37. Beams are injected 20° from normal to the CV with an impact parameter of 20 cm such that ionized particles will orbit in the ion-diamagnetic direction; the resulting ion current produces a field antiparallel to the external field produced by EQ magnet coils. Typically about 8 MW of NB power is attenuated by the plasma after accounting for duct losses and shine-through. NBI on its own tends to cause the plasma to rotate in the ion-diamagnetic direction. If the injection of angular momentum is left unchecked magneto hydrodynamic instabilities (typically n = 2 deformation) can arise. To counter this rotation concentric edge biasing electrodes in the divertors drive a radial current through the plasma that generates a torque in the electron diamagnetic direction

. This balance of forces stabilizes the FRC core enabling a steady-state equilibrium to persist

[38](https://www.nature.com/articles/s41467-025-58849-5#ref-CR38).

[39](https://www.nature.com/articles/s41467-025-58849-5#ref-CR39)### Field reversal sequence

Seed plasmas are generated in Norman by an \(\overrightarrow{E}\times \overrightarrow{B}\) discharge of axial plasma guns and edge biasing electrodes fueled by gas injection in an open magnetic mirror configuration; plasma can be generated by the electrodes alone but this method is less reliable. Within 1 to 4 ms this generates a plasma target sufficient to begin trapping an injected neutral beam thereby providing a substantial fast-ion current. Over the next several *m**s* plasma current grows leading to a robust FRC equilibrium in the CV. This is much longer than formation sequences in other formation methods, such as RMF 40. This is likely due to the slow process of fast ion accumulation and resulting current drive. This elegant procedure stands in stark contrast to the startup sequence in the original Norman design and its predecessors: gas injection, pre-ionization, theta-pinch, translation, acceleration, and collision-merging. Direct measurements of field reversal were obtained via an internal magnetic field probe in the C-2 device using this formation method

. The FRC equilibria created by both methods are very similar, as demonstrated in Fig.

[41](https://www.nature.com/articles/s41467-025-58849-5#ref-CR41)[2](https://www.nature.com/articles/s41467-025-58849-5#Fig2)where core plasma emission is confined within the excluded flux radius

, defined as

[42](https://www.nature.com/articles/s41467-025-58849-5#ref-CR42)where *p**l**a**s**m**a* and *v**a**c* subscripts refer to the quantities with and without plasma present.

The characteristics of the formation phase, i.e., the rise of plasma current, can be controlled by adjusting settings for magnet coil currents, neutral beam settings, electrode voltage, plasma-gun discharge, and gas fueling. During the formation the external magnetic field must be strong enough to balance the pressure of the diamagnetic object and weak enough to allow adequate field reversal. Section “Direct field reversal by neutral beam injection” will describe the criteria for these boundaries. Norman has been operated with both hydrogen and deuterium for both background plasma and beam species, but we typically use hydrogen and our analysis here will focus on those discharges for simplicity. After formation the FRC equilibrium parameters and shape can be manipulated.

### Verification of field-reversal

A non-destructive direct measurement of the magnetic field inside the FRC is beyond current state-of-the-art diagnostic techniques. We are actively pursuing several methods, such as, Faraday rotation of far-infrared radiation, terahertz pulsed polarimetry, circular differential polarimetry, among others 43, to make this measurement, but as of now we rely on model-based inferences. Now we describe those models in detail, from comparison with early methodology to more sophisticated Monte Carlo and Bayesian techniques.

#### Past methodology

The results from Norman will be contrasted with the efforts on 2XIIB 10. That effort was in support of the concept then labeled a field-reversed mirror. While approaching field reversal, it was not achieved. Based on our findings this was due to inadequate neutral current and impact parameter given beam energy and external magnetic field. In the meantime, research on field-reversed configurations (FRC) continued using other formation methods. One of these employed the traditional theta-pinch (some including translation). The other applied rotating magnetic fields. Pursuit of these methods, which continue to this day, were surveyed in two review papers

. Since the 2XIIB experiments, FRC formation by NBI has not been attempted, until now.

[1](https://www.nature.com/articles/s41467-025-58849-5#ref-CR1),[2](https://www.nature.com/articles/s41467-025-58849-5#ref-CR2)This is the first experimental demonstration of successful NBI-based field reversal. To verify successful NBI-based field reversal, two non-direct approaches are taken here. The first adapts the field-reversal index method used in the 1979 paper 10. The second approach builds on several fully two-dimensional (2D) reconstructions of experimental discharges to infer the trapped magnetic flux arising in true FRCs.

The original method defines the field reversal index *ζ* ≡ ∣Δ*B*∣/*B* vac: here Δ

*B*is the field increment on axis at the plasma mid-plane which is produced by plasma current, and

*B*

is the on-axis vacuum field at the mid-plane. Field reversal requires

*v**a**c**ζ*≥ 1. The Δ

*B*for an idealized thin current sheet is found by an integral of the fields from a ring current,

where *I* is the total sheet current, *R* p and

*L*

are the sheet radius and half-length respectively. Complementing this is an equation for the field at the wall

*p**B*

(also a measurable). In the far-field approximation the field due to the sheet current at the wall is

*w*where *r* w is the wall radius. The current inferred from Eq. (

[3](https://www.nature.com/articles/s41467-025-58849-5#Equ3)) is substituted into Eq. (

[2](https://www.nature.com/articles/s41467-025-58849-5#Equ2)) thence yielding

A maximum field reversal of *ζ* = 0.9 was claimed for 2XIIB 10. The foregoing method applied to Norman is shown in Fig.

[3](https://www.nature.com/articles/s41467-025-58849-5#Fig3), clearly exhibiting the achievement of field reversal according to this simple model.

The model rests on assumptions about plasma current distribution. Using Norm’s large data set, more sophisticated techniques will be explored to strengthen the case.

#### Current Tomography equilibria reconstruction

Measurements verify the common assumption of azimuthal symmetry of the FRC. By exploiting this fact models can be developed to describe the equilibrium in 2D. In the following sections we examine two methods that rely on experimental data to produce plasma parameter profiles and magnetic field structures. Reconstructions of hundreds of shots showed field reversal; we will illustrate and compare results of both methods in Fig. [4](https://www.nature.com/articles/s41467-025-58849-5#Fig4) taking shot #147783 as an example. Neither of these reconstruction methods make any assumption about the presence of a field-reversed configuration; both methods can and do yield solutions where the field lines are open in some cases.

The current tomography method uses Bayesian inversion to find the most likely plasma current distribution given the information from a variety of magnetic sensors, external magnet currents, and a physics model. Two advantages of the Bayesian inversion are its ability to combine sensor information from heterogeneous sources and its flexibility in incorporating physics models of variable complexity and certainty. This flexibility makes it ideally suited to study the time evolution of plasma during formation. The method has been validated extensively in axisymmetric plasmas in Tokamaks (JET, TCV) and FRCs (C-2U, Norman)[44](https://www.nature.com#ref-CR44),[45](https://www.nature.com#ref-CR45),[46](https://www.nature.com#ref-CR46),[47](https://www.nature.com/articles/s41467-025-58849-5#ref-CR47)

The inference process takes place in two steps. First, the evolution of magnet currents are used to estimate the currents induced in the CV using an eddy current model. This gives an initial guess for the CV currents prior mean. In the second step Bayesian inference is used to calculate a posterior distribution of plasma currents and CV currents given the magnetic measurements and the magnet currents.

These parameters are obtained directly from the data by running an optimization algorithm that maximizes the evidence (empirical Bayes’), making the inference completely data driven. From the inferred currents, it is straightforward to obtain magnetic flux. Figure [4](https://www.nature.com/articles/s41467-025-58849-5#Fig4)a–d shows the plasma flux evolution resulting from the inference process including a time history of trapped flux and total plasma current, which is determined to be ~300 kA. The inference process creates a distribution of possible states, and by interrogating that distribution we can arrive at the probability that the state is an FRC. This is written as P(FRC) in Fig. [4](https://www.nature.com/articles/s41467-025-58849-5#Fig4)d.

#### Monte Carlo equilibria reconstruction

To gain further insight into the internal magnetic field structure of the FRC, TAE developed a 2D axisymmetric equilibrium reconstruction tool to solve Ampere’s law (\(\overrightarrow{\nabla }\times \overrightarrow{B}={\mu }_{0}\overrightarrow{J}\)) called SEQUOIIA (Synthetic Equilibrium from Observational Input Interpretative Algorithm) 48. It uses experimental measurements of density and temperature along with machine inputs, such as coil currents and neutral beam parameters, in a realistic Norm geometry.

The magnetic field is calculated from diamagnetic currents in the thermal background plasma, fast ion currents, and vacuum field with coil and eddy currents. Neutral beam fast ion density and current are calculated using a 2D full-orbit Monte Carlo code with realistic neutral beam sources and sinks.

The simulation begins with the vacuum magnetic field and thermal plasma. Profiles and currents are calculated in the initial field. Fast ions are introduced and parameters are recalculated using the quasi-neutrality condition *n* i =

*n*

−

*e**n*

, where

*f**n*

is the fast ion density. In the modified magnetic field, the thermal diamagnetic and fast ion currents are calculated in an iterative manner until a steady state solution is achieved. The difference between experimental magnetic flux and simulated magnetic flux is minimized by adjusting

*f**n*

by varying fast ion losses. The final steady state solution is also compared with the other experimental measurements.

*f*Radial profiles from reconstructions of shot #147783 during its steady-state equilibrium (21–30 ms) are shown in Fig. [4](https://www.nature.com/articles/s41467-025-58849-5#Fig4)e–h. The resulting equilibrium state is a field-reversed configuration with a separatrix radius of 0.4 m, axial length of 2 m, and trapped poloidal flux of ~ 6 mWb. A total plasma current, produced by thermal plasma and fast ions, of 350 kA is required to create the resulting FRC. Most of the thermal plasma current is near the boundary of the closed field region resulting in a peaking of total current near the separatrix as shown in Fig. [4](https://www.nature.com/articles/s41467-025-58849-5#Fig4)h. The total energy of the plasma is 9 kJ with nearly equal contributions from the thermal plasma and fast ions.

### Mirror-to-FRC transition

During the transition from a high-beta mirror plasma to a field-reversed configuration, the structures of certain fast-ion-driven wave modes observed in C-2W evolve consistent with the magnetic topology change. In C-2W, magnetic fluctuations are monitored using an array of 3-axis Mirnov probes mounted on the interior walls of the CV. These probes are arranged in arrays of eight rings of eight probes each that are spaced at nearly regular intervals azimuthally, and an additional linear array covering most of the length of the CV 49. The ring arrays can be used to extract the azimuthal mode number,

*n*, of the fluctuations and the linear array can inform on the axial structure of the modes. Here, we discuss two distinct observations: first, magnetic oscillations related to the azimuthal structure and precession of the fast-ion orbits; and second, an energetic-particle mode corresponding to the fast-ion axial bounce motion and axial turning points.

#### Precession motion

The evolution of fast-ion driven fluctuations from an *n* = 1 toroidal mode structure to *n* = 2 follows changes in the excluded flux radius. These fluctuations are attributed to the fast ion precession mode, a finite Larmor radius mode first described in the context of relativistic electron layers in the Astron device 50,51. This mode arises from energetic particle orbit precession phase coherence induced by the self-field generated by the injected energetic particles (electrons in Astron, ions in Norman). The precession phase coherence leads to macroscopic perturbations to the magnetic field and density profiles observable in magnetic field measurements at the vessel wall

and line-integrated density measurements through the plasma, respectively.

[52](https://www.nature.com/articles/s41467-025-58849-5#ref-CR52)The macroscopic perturbations are expected to exhibit a toroidal mode structure matching that of the fast ion orbits themselves 53. The mode frequencies evolve over the course of each discharge, but typically fall within the range of 50–400 kHz, consistent with expected precession frequencies of the fast ion orbits. The mode frequencies begin higher at the start of the shot and decrease as the field is reversed. The toroidal mode shape evolution is experimentally consistent with the expected evolution of the fast ion orbit types as the field reverses, in the absence of direct measurements of fast ion orbit types. Thus, as the field reversal parameter increases and fast ion orbit shapes transition from predominantly

*n*= 1 (cyclotron orbits) to

*n*= 2 (betatron orbits), the strength of fluctuations with the latter toroidal mode shape is expected to increase

.

[54](https://www.nature.com/articles/s41467-025-58849-5#ref-CR54)Indeed, this transition is consistently observed during FRC formation. Figure [5](https://www.nature.com/articles/s41467-025-58849-5#Fig5) depicts this transition in the dominant fast ion mode structure during FRC formation for several shots with similar excluded flux evolutions taken from across the Norman operational campaign without the use of theta-pinch formation sections. The amplitude of these fluctuations are small in both cases due to the stabilizing effect of edge biasing electrodes 55.

#### Axial bounce motion

Energetic-particle modes (EPMs) are plasma wave modes that correspond to resonances of the characteristic periodic motions of fast ions 56. In open field-line mirror-trapped plasmas, fast ions will bounce axially between turning points with a frequency

*ω*

determined by the external magnetic field profiles. In FRC plasmas, fast ions will bounce axially between the ends of the FRC, a shorter distance leading to a higher

*z**ω*

. During the mirror-to-FRC transition, the fast-ion turning points are expected to move toward the mid-plane and the axial bounce frequency will increase accordingly. Recently, an EPM was identified in C-2W that corresponds to a resonance of the axial bounce motion and its harmonics

*z*. We have called this mode the Axial Bounce Mode (ABM) and will adopt this language herein. The results of several experiments on the ABM have been reported

[57](https://www.nature.com/articles/s41467-025-58849-5#ref-CR57), and we expect to publish a more detailed article soon.

[57](https://www.nature.com/articles/s41467-025-58849-5#ref-CR57)The ABM in C-2W manifests as an axisymmetric magnetic fluctuation (*n* = 0 azimuthal mode structure) primarily in the *B* z and

*B*

components of the magnetic field; eddy currents in the wall artificially reduce the observed amplitudes of the

*r**B*

fluctuations and we restrict ourselves to the

*r**B*

component in diagnosing this mode. In dedicated mirror experiments, the turning points of fast ions sourced from NBI were dynamically scanned using field shaping to establish that the ABM is a resonance of their axial bounce motion; the mode was shown to oscillate with frequency

*z**ω*=

*ℓ*

*ω*

, where

*z**ℓ*is a positive integer and

*ω*

is the axial bounce frequency of the fast ions in the mirror field. The mode typically has a standing wave structure with odd parity about the mid-plane in

*z**B*

, the magnitude peaks near the fast ion turning points, and the amplitude increases with the total NBI power. We have established robust control of the mode using beam species, energy, and injection angle, and suppression of the ABM shows it is not detrimental to plasma confinement. The mode is understood to arise from the axial bunching of fast ions in phase space. A reduced model of ion rings in an axial potential well has been constructed to reproduce many experimentally observed features of the ABM

*z*.

[58](https://www.nature.com/articles/s41467-025-58849-5#ref-CR58)Since the mode is observed in both mirror and FRC plasmas, it can be used to assess changes to the magnetic topology after the mirror-to-FRC transition. Figure [6](https://www.nature.com/articles/s41467-025-58849-5#Fig6) shows an example of the transition from a mirror plasma to an FRC and how the features of the ABM evolve. The plasma is initially kept as a mirror plasma with a small *r*Δ ϕ using a lower level of NBI power, Fig.

[6](https://www.nature.com/articles/s41467-025-58849-5#Fig6)a. Applying additional NBI power at 10 ms increases the trapped flux until FRC formation at approximately 16 ms. Figure

[6](https://www.nature.com/articles/s41467-025-58849-5#Fig6)b shows a spectrogram of the Mirnov probe signals at

*z*= ± 0.45 m decomposed into

*n*= 0 fluctuations with the fundamental and two harmonics of the ABM mode indicated. In the mirror region, we can see the mode has a low amplitude due to the lower beam power and has a nearly constant frequency that matches well with the bounce frequency determined from the vacuum magnetic field; typically, the third harmonic has the largest amplitude in the mirror regime, as is the case here. When the beam power is increased, we see the amplitude of the mode increase rapidly, and the frequency begins to rise; this increase in frequency is due to a constriction of the fast-ion turning points towards the mid-plane.

In Fig. [6](https://www.nature.com/articles/s41467-025-58849-5#Fig6)c, cross-correlation of the ring Mirnov array with the linear Mirnov array is used to extract the axial structure of the mode in the mirror and FRC regions of Fig. [6](https://www.nature.com/articles/s41467-025-58849-5#Fig6)a. In the mirror, the mode is observed to peak around *z* = ±1.6 m, a good match for the vacuum field turning point at approximately *z* = ±1.5 m, calculated using ionization at the mid-plane of the vacuum field profile indicated and the nominal beam injection angle. Once the FRC has formed the mode peaks sharply at the probes located at *z* = ±0.48 m and rapidly decays indicating the reduced extent of the axial confinement of the fast ions. The evolution of this *n* = 0 ABM as presented for the shot here is consistently observed in the formation of FRC plasmas across all Norm campaigns and represents a clear signature of the changing magnetic topology induced by the NBI reversal process.

### Direct field reversal by neutral beam injection

Now we construct a theoretical model to describe the generation of an FRC object. It is a zero-dimensional construct focusing on beam and plasma currents. It derives a minimum criterion for field reversal and is compared to experimental results.

A cylindrical ring of ion current creates a magnetic field,

where *I* f is the total ion current and

*L*is the length of the cylindrical ring of current. If the ion current is carried by fast ions injected by neutral beams then the ion current buildup is determined by the equation \({I}_{f}=\frac{{I}_{b}{\tau }_{\ell }}{{\tau }_{2\pi }}\left[1-\exp \left(-\frac{t}{{\tau }_{\ell }}\right)\right]\), and the steady-state fast ion current is \({I}_{f}=\frac{{I}_{b}{\tau }_{\ell }}{{\tau }_{2\pi }}\), where

*τ*

is the lifetime of fast ions determined by loss mechanisms such as charge-exchange and collisions with background plasma,

*ℓ**τ*

2is the average orbit time about the cylindrical axis, and

*π**I*

is the portion of injected neutral beam current that has been trapped in the plasma (i.e., that part which is not lost to beam shine-through S),

*b**I*

= (1 −

*b**S*)

*I*

, where

*i**n**j**I*

is the injected current of neutral particles.

*i**n**j*A background magnetic field, *B*, is reversed by the neutral beam injected fast ion current if *B* f >

*B*. The condition for fast ion current to reverse the field,

*B*

>

*f**B*, is that \(\frac{{\mu }_{0}{I}_{b}{\tau }_{\ell }}{{\tau }_{2\pi }L} > B\), or in other words,

In the initial vacuum magnetic field, the most efficient way to impart current from the beams is if the impact parameter of beam injection is equal to the initial ion gyroradius so that the fast ion orbits are Larmor orbits encircling the cylindrical axis and the average period of gyration is equal to the gyroperiod, \({\tau }_{2\pi }=\frac{1}{f}=\frac{2\pi }{\Omega }=\frac{2\pi }{eB/m}\). The requirement to reverse the field becomes

This expression is approximate because the magnetic field changes as the fast ion current builds up, however it is a useful rule of thumb which has been validated empirically. Experiments which scanned over various values of magnetic field and neutral beam current have been conducted on Norman to explore the operational boundaries between reversed and non-reversed mirror plasmas. Figure [7](https://www.nature.com/articles/s41467-025-58849-5#Fig7) shows estimated values of the field produced by the fast ions versus the external field for discharges that achieved *r*Δ Φ > 35

*c*

*m*(shown as green dots) and those that did not (as red crosses). The quantities shown are window-averaged between 1 and 5 milliseconds. The apparent boundary for FRC formation aligns well with theoretical arguments laid out above and reflects what has long been observed in our NBI generated FRC campaigns.

## Discussion

Field-reversed configurations have been generated from seed mirror plasmas via neutral beam injection. The resulting equilibria have been shown to be comparable to those established through the merging and acceleration of theta-pinch generated FRCs. Historical metrics show conclusively that field reversal has been established. Additionally, many contemporary diagnostic techniques provide a preponderance of evidence for the same. Furthermore, simulations matching the conditions in Norman plasmas indicate that NBI generated field reversal has been realized.

This desired yet unexpected breakthrough discovery made during the operational campaign of Norman has vastly simplified the start-up requirements and operational complexities for FRC based fusion reactor designs. It also marks a material advance towards the ultimate goal of aneutronic power generation via high-beta self-confined plasmas, which are arguably the most magnetically efficient topology for an economic fusion reactor.

## Methods

### Ensemble results

After more than 50,000 individual shots on Norman extensive operational mastery has been attained. FRCs are generated by NBI which results in gradual increase of plasma diamagnetism; the FRCs are held in steady-state until the storage capacity of the power supplies that drive the neutral beams has been extinguished (40 ms). The plasma has been optimized in several stages which should be the topic of future publications, but the underlying result is that FRCs with thermal energies (determined by pressure balance and interferometry measurements 59) approaching 10 kJ are now produced repeatedly. Figure

[8](https://www.nature.com/articles/s41467-025-58849-5#Fig8)shows a representative ensemble of 39 shots.

### Bayesian current tomography

Given a forward model **D** = *H*(*X*) relating a set of continuous variables \(X\left(r\right)\), each a function of location \({{\bf{r}}}=\left({{{\bf{r}}}}_{{{\bf{1}}}},\,{{{\bf{r}}}}_{{{\bf{2}}}},\,{{{\bf{r}}}}_{{{\bf{3}}}}\right)\), to a set of measurements arranged in a vector **D**, we can find all the solutions in *X* that explain the data in *D* and arrange them in a posterior probability distribution \(P\left(D| X\right)\). The misfit between the measurements and model predictions is also modelled by a probability distribution \(P\left(X| D\right)\), known as the likelihood function. Bayes’ theorem allows us to obtain the posterior \(P\left(D| X\right)\) from the likelihood \(P\left(X| D\right)\) given a model for the relationships of the variables in *X* expressed in probabilistic form, termed the prior distribution \(P\left(X\right)\).

The denominator \(P\left(D\right)\) is the marginal likelihood or evidence and normalizes the volume of the posterior to 1.

For this work, the information from external magnetic sensors and magnet current time evolution are used to infer the most likely plasma current distribution. The CV and plasma region are described by a large set of discrete current carrying elements as in Fig. [9](https://www.nature.com/articles/s41467-025-58849-5#Fig9).

Since the location of the current sources and magnetic measurements are fixed in space, the current sources on the plasma and CV in *X* can be linearly related to the magnetic sensor measurements in *D* through the matrix representation *K* of the Biot-Savart operator

Assuming additive measurement noise \(\epsilon=N\left(0,{\Sigma }_{D}\right)\) independent of *X*, the likelihood function can be modelled as a n-dimensional Gaussian distribution.

Where \({\Sigma }_{D}\,\epsilon \,{{\mathbb{R}}}^{nxn}\) is the data covariance matrix. The prior distribution can also be approximated by a multivariate probability distribution over *X*

Where \({\Sigma }_{X}\epsilon {{\mathbb{R}}}^{kxk}\) is the prior covariance matrix and \({\mu }_{X}\epsilon {{\mathbb{R}}}^{k}\) is the prior mean. The posterior distribution can likewise be approximated by a k-dimensional Gaussian Probability distribution

Since all the probability distributions above are Gaussian, and Gaussian distributions are related to Gaussian distributions through linear operations, the posterior mean and covariance can be obtained explicitly from the prior and data covariances, prior mean and measurements

The prior probability distribution encapsulates the physics model expressed as a probability distribution. Our prior belief about \(X\left(r\right)\) is that it must be a smooth function of *r*, so we use a simple parametrization for the prior covariance matrix based on the expected current ranges and correlations between neighboring current elements parametrized with scale lengths \(\left({\lambda }_{1},{\lambda }_{2},{\lambda }_{3}\right)\) along the spatial dimensions

With \(\Lambda={{\rm{diag}}}\left({\lambda }_{1},{\lambda }_{2},{\lambda }_{3}\right)\). The standard deviation *σ* determines the expected excursion level for the currents, while the scale lengths *λ* i determine how quickly the currents can change with the coordinate

*r*

.

*i*## Data availability

The data that support the findings of this study are available from the corresponding author upon request due to IP considerations.

## Code availability

Code used to analyze experimental data can be made available upon request due to IP considerations.

## References

Tuszewski, M. Field reversed configurations.

*Nucl. Fusion***28**, 2033 (1988).Steinhauer, L. C. Review of field-reversed configurations.

*Phys. Plasmas***18**, 070501 (2011).Christofilos, N.C. Astron thermonuclear reactor. Technical report, California. Univ., Livermore. Radiation Lab., October 1958. Prepared for the Second U.N. International Conference on the Peaceful Uses of Atomic Energy, 1958.

Davis, H. A., Meger, R. A. & Fleischmann, H. H. Generation of field-reversing

*e*layers with millisecond lifetimes.*Phys. Rev. Lett.***37**, 542–545 (1976).Blevin, H. & Thonemann, P. Experimental studies of a theta-pinch discharge.

*Nucl. Fusion,***Suppl. 1**, 55, (1962).Cohen, S. A. et al. Formation of collisionless high-

*β*plasmas by odd-parity rotating magnetic fields.*Phys. Rev. Lett.***98**, 145002 (2007).Wells, D. R. Injection and Trapping of Plasma Vortex Structures.

*Phys. Fluids***9**, 1010–1021 (1966).Kolb, A. C., Dobbie, C. B. & Griem, H. R. Field mixing and associated neutron production in a plasma.

*Phys. Rev. Lett.***3**, 5–7 (1959).Slough, J. T. et al. Confinement and stability of plasmas in a field-reversed configuration.

*Phys. Rev. Lett.***69**, 2212–2215 (1992).Turner, W. C. et al. Field-reversal experiments in a neutral-beam-injected mirror machine.

*Nucl. Fusion***19**, 1011 (1979).Hammer, J. H. & Berk, H. L. A steady-state beam-driven field-reversed mirror.

*Nucl. Fusion***22**, 89 (1982).Tsidulko, Yu. A. Adiabatic model of field reversal by fast ions in an axisymmetric open trap.

*Plasma Phys. Rep.***42**, 559–565 (2016).Gota, H. et al. Overview of c-2w, high temperature, steady-state beam-driven field-reversed configuration plasmas.

*Nucl. Fusion***61**, 106039 (2021).Gota, H. et al. Formationtion of hot, stable, long-lived field-reversed configuration plasmas on the c-2w device.

*Nucl. Fusion***59**, 112009 (2019).Rostoker, N., Binderbauer, M. W. & Monkhorst, H. J. Colliding beam fusion reactor.

*Science***278**, 1419–1422 (1997).Rostoker, N., Binderbauer, M., Garate, E., & Bystritskii, V. Formation of a field reversed configuration for magnetic and electrostatic confinement of plasma, May 2005. U.S. Patent 6891911B2.

Binderbauer, M. W. et al. Dynamic formation of a hot field reversed configuration with improved confinement by supersonic merging of two colliding high-

*β*compact toroids.*Phys. Rev. Lett.***105**, 045003 (2010).Tuszewski, M. et al. A new high performance field reversed configuration operating regime in the C-2 devices.

*Phys. Plasmas***19**, 056108 (2012).Anikeev, A. V., Bagryansky, P. A., Ivanov, A. A., Kuzmin, S. V. & Salikova, T. V. Experimental observation of non-mhd effects in the curvature driven flute instability.

*Plasma Phys. Control. Fusion***34**, 1185 (1992).Anikeev, A. V. et al. Observation of magnetohydrodynamic stability limit in a cusp-anchored gas-dynamic trap.

*Phys. Plasmas***4**, 347–354 (1997).Tuszewski, M. et al. Field reversed configuration confinement enhancement through edge biasing and neutral beam injection.

*Phys. Rev. Lett.***108**, 255008 (2012).Binderbauer, M. W. et al. A high performance field-reversed configurationa).

*Phys. Plasmas.***22**, 056110 (2015).Guo, H. Y. et al. Achieving a long-lived high-beta plasma state by energetic beam injection.

*Nat. Commun.***6**, 6897 (2015).Binderbauer, M. W. et al. Recent breakthroughs on C-2U, Norman’s legacy.

*AIP Conf. Proc.***1721**, 030003 (2016).Gota, H. et al. Achievement of field-reversed configuration plasma sustainment via 10 mw neutral-beam injection on the c-2u device.

*Nucl. Fusion***57**, 116021 (2017).Hirano, K. A steady-state axisymmetric toroidal system.

*Nucl. Fusion***24**, 1159 (1984).Hamada, S. A model of equilibrium transport and evolution of field reversed configurations.

*Nucl. Fusion***26**, 729 (1986).Okamoto, M. A steady state solution to a field reversed configuration.

*Nucl. Fusion***27**, 833 (1987).Ohnishi, M., Kuranaga, H. & Okamoto, M. Suppression, by ion beams, of the m = 2 rotational instability in a field reversed configuration.

*Nucl. Fusion***28**, 1427 (1988).Okamoto, M., Berk, H. L. & Hammer, J. H. Relation between beam driven seed current and rotation in a steady state field reversed configuration.

*Nucl. Fusion***29**, 2063 (1989).Asai, T. et al. Experimental evidence of improved confinement in a high-beta field-reversed configuration plasma by neutral beam injection.

*Phys. Plasmas***7**, 2294–2297 (2000).Okada, S. et al. Experiments on additional heating of frc plasmas.

*Nucl. Fusion***41**, 625 (2001).Takahashi, T., Kato, T., Kondoh, Y. & Iwasawa, N. Power deposition by neutral beam injected fast ions in field-reversed configurations.

*Phys. Plasmas***11**, 3801–3807 (2004).Lifschitz, A. F., Farengo, R. & Arista, N. R. Monte carlo simulation of neutral beam injection into a field reversed configuration.

*Nucl. Fusion***42**, 863 (2002).Lifschitz, A. F., Farengo, R. & Hoffman, A. L. Calculations of tangential neutral beam injection current drive efficiency for present moderate flux frcs.

*Nucl. Fusion***44**, 1015 (2004).Yamada, M. et al. A self-organized plasma with induction, reconnection, and injection techniques, the spirit concept for field reversed configuration research.

*Plasma Fusion Res.***2**, 004–004 (2007).Titus, J. B., Korepanov, S., Tkachev, A., Pirogov, K. & Knapp, K. Wire calorimeter for direct neutral beam power measurements on c-2w.

*Rev. Sci. Instrum.***92**, 053520 (2021).Nations, M., Romero, J. A., Gupta, D. K., Sweeney, J. & the TAE Team. High-fidelity inference of local impurity profiles in C-2W using Bayesian tomography.

*Rev. Sci. Instrum.***93**, 113522 (2022).Ryutov, D. D., Berk, H. L., Cohen, B. I., Molvik, A. W. & Simonen, T. C. Magneto-hydrodynamically stable axisymmetric mirrorsa.

*Phys. Plasmas***18**, 092301 (2011).Cohen, S. A. et al. Laboratory study of the PFRC-2’s initial plasma densification stages.

*Phys. Plasmas***30**, 102503 (2023).Gota, H. et al. Internal magnetic field measurement on C-2 field-reversed configuration plasmasa.

*Rev. Sci. Instrum***83**, 10D706 (2012).Tuszewski, Michel. Excluded flux analysis of a field reversed plasma. Informal Report LA-8512-MS, Los Alamos Scientific Laboratory, September (1980).

Nations, Marcel. Internal magnetic field measurements for beam-driven field-reversed configuration fusion devices. Technical report, TAE Technologies, Foothill Ranch, CA, January (2024).

Svensson, J., Werner, A. & JET-EFDA Contributors. Current tomography for axisymmetric plasmas.

*Plasma Phys. Control. Fusion***50**, 085002 (2008).Romero, J. A. & Svensson, J. Optimization of out-vessel magnetic diagnostics for plasma boundary reconstruction in tokamaks.

*Nucl. Fusion***53**, 033009 (2013).Romero, J. A., Dettrick, S. A., Granstedt, E., Roche, T. & Mok, Y. Inference of field reversed configuration topology and dynamics during alfvenic transients.

*Nat. Commun.***9**, 691 (2018).Romero, J.A. Optimization and feedback control of the c-2w configuration. 29th IAEA Fusion Energy Conference, October 2023.

Gupta, S., Sato, I., Dettrick, S. Hubbard, K. & Yushmanov, P. Equilibrium reconstruction of beam driven c-2w plasmas. In

*APS Division of Plasma Physics Meeting Abstracts*volume 2022, pages TP11–027, 2022.Roche, T. et al. Magnetic diagnostic suite of the c-2w field-reversed configuration experiment.

*Rev. Sci. Instrum.***89**, 10J107 (2018).Briggs, R. J. et al. Astron program final report. Technical report, Lawrence Livermore National Laboratory, 8 (1975).

Furth, H. P. Unstable Precession under the Influence of Drag Forces.

*Phys. Fluids***8**, 2020–2025 (1965).Tobin, M., Roche, T., Matsumoto, T. & TAE Team. MHD mode identification by higher order singular value decomposition of C-2W Mirnov probe data.

*Rev. Sci. Instrum.***92**, 043510 (2021).Deng, B. H. et al. First experimental measurements of a new fast ion driven micro-burst instability in a field-reversed configuration plasma.

*Nucl. Fusion***58**, 126026 (2018).Harned, D. S. Kink instabilities in long ion layers.

*Phys. Fluids***25**, 1915–1921 (1982).Schmitz, L. et al. Suppressed ion-scale turbulence in a hot high-beta plasma.

*Nat. Commun.***7**, 13860 (2016).Heidbrink, W. W. & White, R. B. Mechanisms of energetic-particle transport in magnetically confined plasmas.

*Phys. Plasmas***27**, 030901 (2020).Karbashewski, S. et al. Observation of an axisymmetric energetic particle mode driven by axial bounce oscillations of fast ions in c-2w. In

*APS Division of Plasma Physics Meeting Abstracts*volume 2024, page TP12. 00127, (2024).Granstedt, E. M. et al. Theory, control, and use of a fast ion axial bounce mode on c-2w. In

*APS Division of Plasma Physics Meeting Abstracts*volume 2024, page TP12. 00128, (2024).Roche, T. et al. The integrated diagnostic suite of the C-2W experimental field-reversed configuration device and its applications.

*Rev. Sci. Instrum.***92**, 033548 (2021).

## Acknowledgements

The TAE Team would like to thank its shareholders for the financial support.

## Author information

### Authors and Affiliations

### Contributions

T.R. executed initial NBI reversal experiments. T.R, A.F, S.G., J.A.R, M.T.T, E.M.G, and S.K. analyzed experimental data. S.D, A.F, M.O., L.G., and L.C.S. provided theoretical interpretation. R.M.M., P.Y, E.T., H.G., and M.W.B supported the development of this work. T.R., S.D., A.F., S.G., M.O., J.A.R., L.C.S., M.T.T., E.M.G., L.G., S.K., R.M.M., P.Y., E.T., H.G., S.A., I.A., R.A., V.A., J.A., D.C.B., M.B., N.G.B., D.B., F.C., R.C., T.D., B.D., A.V.D., P.F., D.K.G., K.H., J.S.K., K.K., B.K., S.A.K., A.K., C.K.L., D.L., D.MacD., D.M., J.A.M., J.M., P.M., T.M., M.P.M., R.Me., R.Mi., H.M., M.E.M., M.N., A.N., B.S.N., R.P, E.P., J.P., K.P., T.W.R., L.S., J.H.S., G.N.S., A.G.H.S., M.S., R.J.S., G.S., V.S., Y.S., G.L.S., L.T., J.B.T., J.U., T.V., C.E.W., S.W., C.W., M.W., K.Z., S.Z., M.T., A.S., S.P., T.T., M.W.B. supported the experimental program.

### Corresponding author

## Ethics declarations

### Competing interests

TAE Technologies is a private corporation owned and financially supported by its shareholders. The authors of this manuscript may have financial interest in the company.

## Peer review

### Peer review information

*Nature Communications* thanks the anonymous reviewer(s) for their contribution to the peer review of this work. A peer review file is available.

## Additional information

**Publisher’s note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

## Supplementary information

## Rights and permissions

**Open Access** This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit [http://creativecommons.org/licenses/by-nc-nd/4.0/](http://creativecommons.org/licenses/by-nc-nd/4.0/).

## About this article

### Cite this article

Roche, T., Dettrick, S., Fontanilla, A. *et al.* Generation of field-reversed configurations via neutral beam injection.
*Nat Commun* **16**, 3487 (2025). https://doi.org/10.1038/s41467-025-58849-5

Received:

Accepted:

Published:

Version of record:

DOI: https://doi.org/10.1038/s41467-025-58849-5