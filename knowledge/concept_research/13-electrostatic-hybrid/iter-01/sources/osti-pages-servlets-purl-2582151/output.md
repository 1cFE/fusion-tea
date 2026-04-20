---
source: "https://www.osti.gov/pages/servlets/purl/2582151"
source_type: "url"
extracted_at: "2026-04-19T19:30:30.292728+00:00"
content_hash_sha256: "6355f2515fe49ce8d9a48d9f72480e7e27b8cbd3cdee24ccbd8086c2c0bc6103"
backend: "pdf_pipeline"
---


![](images/tmpt737zoze.pdf-0001-01.png)

RESEARCH ARTICLE | AUGUST 20 2024 

## **The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons** 

M. Affolter  ; R. Thompson ; S. Hepner ; E. C. Hayes ; V. Podolsky ; M. Borghei ; J. Carlsson ; A. Gargone ; D. Merthe ; E. McKee ; R. Langtry 

![](images/tmpt737zoze.pdf-0001-05.png)

_AIP Advances_ 14, 085025 (2024) https://doi.org/10.1063/5.0201470 

 CHORUS 

 View Export Online[] Citation 

## **Articles You May Be Interested In** 

The Orbitron as a stimulated ‐ bremsstrahlung glow ‐ discharge maser 

_J. Appl. Phys._ (July 1986) 

The circular orbit linear theory of the axial injection orbitron maser (AXIOM) oscillator 

_Phys. Fluids B_ (February 1991) 

A simplified Vlasov–Landau treatment of electron motion in the orbitron maser 

_Phys. Fluids_ (June 1985) 

![](images/tmpt737zoze.pdf-0001-16.png)

# The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons 

![](images/tmpt737zoze.pdf-0002-05.png)

![](images/tmpt737zoze.pdf-0002-06.png)

Cite as: AIP Advances **14** , 085025 (2024); doi: 10.1063/5.0201470 Submitted: 1 July 2024 • Accepted: 3 August 2024 • Published Online: 20 August 2024 

M. Affolter,[a)] R. Thompson, S. Hepner, E. C. Hayes, V. Podolsky, M. Borghei, J. Carlsson, A. Gargone, D. Merthe, E. McKee, and R. Langtry 

![](images/tmpt737zoze.pdf-0002-09.png)

![](images/tmpt737zoze.pdf-0002-10.png)

## AFFILIATIONS 

Avalanche Energy, 9100 E Marginal Way S, Tukwila, Washington 98108, USA 

> **a)** Author to whom correspondence should be addressed: maffolter@avalanche.energy 

## ABSTRACT 

To explore the confinement of high-energy ions above the space charge limit, we have developed a hybrid magnetic and electrostatic confinement device called an Orbitron. The Orbitron is a crossed-field device combining aspects of magnetic mirrors, magnetrons, and orbital ion traps. Ions are confined in orbits around a high-voltage cathode with co-rotating electrons confined by a relatively weak magnetic field. Experimental and computational investigations focus on reaching ion densities above the space charge limit through the co-confinement of electrons. The experimental apparatus and suite of diagnostics are being developed to measure the critical parameters, such as plasma density, particle energy, and fusion rate for high-energy, non-thermal plasma conditions in the Orbitron. Initial results from experimental and computational efforts have revealed the need for cathode voltages on the order of 100–300 kV, leading to the development of a custom high voltage, ultra-high vacuum bushing rated for 300 kV. 

© _2024 Author(s). All article content, except where otherwise noted, is licensed under a Creative Commons Attribution-NonCommercialNoDerivs 4.0 International (CC BY-NC-ND) license (https://creativecommons.org/licenses/by-nc-nd/4.0/)._ https://doi.org/10.1063/5.0201470 

## I. INTRODUCTION 

Various classes of ion traps have been studied and characterized with respect to their confinement time _τ_ and space charge limited density. In particular, Penning–Malmberg traps,[1–3] Paul traps,[4] and orbital ion traps[5–7] have all demonstrated long confinement times with _τ_ ≳ 1 s. However, these traps are typically limited by space charge effects to low ion densities. For a 4.5 T magnetic field, the space charge limited density (Brillouin limit) for Be[+] of _n_ ≈ 6 × 10[9] cm[−][3] has been achieved in a Penning trap.[8] Confinement schemes have been explored with Penning traps to exceed this density limit;[9,10] however, research has been limited. 

Here, we describe a new approach for reaching ion densities above the space charge limit by co-confining electrons in an orbital ion trap called an Orbitron.[11] Orbital ion traps have long been studied for applications to neutralization of electron space charge[12] and mass spectrometry.[13] Commercial mass spectrometer orbital ion traps operate with confined ion kinetic energies 1–5 keV, and negligible center-of-mass collisional energies _E_ com due to the use 

of circularized orbits.[14] In the Orbitron, _E_ com of 10–60 keV are achieved by scaling the cathode voltage to values on the order of −100 kV and by inserting ions into elliptical orbits. At these high ion energies, reasonable fusion rates are achievable if the ion density is scaled above the ion space charge limit. Therefore, initial investigations of the Orbitron are focused on reaching densities above the ion space charge limit through the co-confinement of electrons with a relatively weak magnetic field. Key challenges are the impacts of Coulomb collisions and particle transport on _τ_ and _E_ com, plasma stability, and achieving a sufficient ion loading rate. 

The rest of this manuscript is structured as follows. In Sec. II, we discuss the principle of operation of the Orbitron device. Sections III and IV describe the experimental apparatus and diagnostics for the Orbitron deuterium–deuterium fusion experiments. In Sec. V, Particle-in-Cell (PIC) simulations are presented, which show the mitigation of the ion space charge limit through co-confinement of electrons. Finally, Sec. VI enumerates areas of investigation underway for assessing the Orbitron’s ability to achieve high fusion reaction rates. 

## II. PRINCIPLE OF OPERATION 

## A. Particle confinement 

The Orbitron is a crossed-field ( _E_ × _B_ ) device. As in an orbital ion trap,[7] ions with sufficient azimuthal ( _θ_ ) velocity are confined in orbits and accelerated by an electrostatic potential between an outer anode and inner cathode arranged in an annular configuration, see Fig. 1. While orbiting in _θ_ around the cathode, ions simultaneously oscillate back and forth along the _z_ -axis due to the electrostatic pinch formed by the geometry of the electrodes. The cathode is held at a high magnitude negative potential to confine ions in elliptical orbits and accelerate them to center-of-mass energies having high fusion reactivity. To support long ion confinement times, the pressure of neutral particles is held in an ultra-high vacuum (UHV) regime (<10[−][8] Torr) to reduce particle scattering and charge exchange. Simulations (see Sec. V) predict ion density limitations due to space charge are mitigated by co-confining electrons with a longitudinal magnetic field as in a magnetron.[15] 

In a perfect vacuum, the Orbitron particle dynamics for a single charged particle are determined by the azimuthally symmetric electromagnetic fields imposed by the outer and inner electrodes and the external magnets. In addition to modifying the ideal quadro-logarithmic electrostatic potential of an orbital ion trap[7] 

is applied to the device for electron confinement. Here, _k_ and _Rm_ are electrode geometry design parameters for an ideal quadrologarithmic potential, _G_ ( _r_ , _z_ ) represents deviations from this ideal geometry to aid electron confinement, and _C_ shifts the potential relative to an arbitrary reference point. When _G_ = 0 and **B**[0] = 0, the ions are confined in a quadro-logarithmic potential well, and ion motion along _z_ is simple harmonic oscillation as in an orbital ion trap.[7] When _G_ ≠ 0, ion acceleration in the _z_ direction depends on _r_ ; thus, elliptical orbits in the _r_ - _θ_ plane cause randomly driven oscillator motion along _z_ . 

Magnetron-like electron confinement in the Orbitron is achieved with non-zero values of _G_ , _B_[0] _z_[,][and] _[B]_[0] _r_[,][see][Sec.][II][A][2][.] The effect of the magnetic field on ion and electron orbits is related to the cathode voltage and the spatial dimensions of the trap, which are characterized by the maximum radii _Rc_ and _Ra_ of the cathode and anode, respectively ( _Rc_ < _Ra_ ). For our investigations, 𝒪( _Ra_ ) = 𝒪( _z_ max) ∼ 10 cm, where _z_ max is the maximum extent of the trap in the ± _z_ directions. For cathode voltages near −100 kV, we focus on ∣ **B**[0] ∣∼ 0.05–0.1 T so that fuel ions (mass ∼2 amu) are weakly magnetized (Larmor radius ≫ _Ra_ − _Rc_ ), while electrons are strongly magnetized (Larmor radius ≪ _Ra_ − _Rc_ ). 

## _1. Ion confinement_ 

![](images/tmpt737zoze.pdf-0003-11.png)

an external magnetic field 

![](images/tmpt737zoze.pdf-0003-13.png)

**----- Start of picture text -----**<br>
B [0] ( r ,  z ) =  B [0] z [(] [r] [,] [ z] [)] [z] [ˆ][ +] [ B] r [0][(] [r] [,] [ z] [)] [r] [ˆ] (2)<br>**----- End of picture text -----**<br>

![](images/tmpt737zoze.pdf-0003-14.png)

![](images/tmpt737zoze.pdf-0003-15.png)

**FIG. 1.** Cross-sections of an orbital electrostatic ion trap with a quadro-logarithmic potential and no external magnetic field ( _G_ = 0 and **B**[0] = 0). Ions orbit around the high-voltage cathode (gray) and are confined along the z-axis by the potential well formed by the pinched geometry. 

An ion orbit is illustrated in Fig. 1. With **B**[0] = 0, ion confinement has been intensively investigated for both quadro-logarithmic ( _G_ = 0)[7,16] and non-quadro-logarithmic ( _G_ ≠ 0)[5,12–14,17] potentials. Ions loaded into this azimuthally symmetric potential with sufficient angular momentum are confined radially through the conservation of angular momentum and energy. Axial confinement is provided by the potential well in _z_ formed by the pinch in the geometry of the electrodes at each end of the device. 

Adding the magnetic field described in Eq. (2) will perturb the ion dynamics. We explore how the presence of a uniform axially magnetic field changes the ion confinement region in velocity space in a simplified _r_ – _θ_ approximation of Eqs. (1) and (2) with _G_ = 0. For a given radius, we use the conserved energy _E_ = _m_ **v** ⋅ **v** /2 + _q_ Φ[0] ( _r_ , 0) and canonical angular momentum _pθ_ = _mrvθ_ + _r_[2] _qBz_[0][(] _[r]_[, 0][)/][2 to numerically solve for the minimum and] maximum _vθ_ that are confined in the device without hitting the cathode and anode, respectively. This calculation assumes no initial radial velocity. Figure 2 shows the results of this calculation. The gray-shaded region represents velocities confined in the device in the absence of the magnetic field with the lower and upper bounds representing ions colliding with the cathode and anode, respectively. The red-shaded region shows the small perturbation in the confinement region with the addition of a 0.1 T axial magnetic field. The slight perturbation of ion orbital behavior with **B**[0] is a trade-off for enabling electron co-confinement described in Sec. II A 2. 

Ions confined to elliptical orbits will cross paths with one another within the Orbitron and collide. With high _E_ com in a collisional event, fusion fuel ions, such as deuterium, will have a probability of fusing. We examine the range of collisional energies in a reduced _r_ – _θ_ model considering only the difference in radial velocity Δ _vr_ . The ranges of ion confinement in phase space depicted in Fig. 2 are associated with a corresponding range of orbital ellipticities. Using the approach in Ref. 18, the ellipticity of an orbit in a logarithmic potential is quantified with the unitless parameter _βO_ . 

![](images/tmpt737zoze.pdf-0004-04.png)

**FIG. 2.** Azimuthal velocity required for ion confinement at different radii in a simplified _r_ – _θ_ model of the dynamics. The red- and gray-shaded regions show the confinement space with and without a 0.1 T axial magnetic field, respectively. Slightly lower velocities are necessary with the axial magnetic field. 

For circular orbits, _βO_ = 0.844. Larger _βO_ values indicate more elliptical orbits. Figure 3 illustrates the range of _E_ com vs _βO_ for deuterium ions with the same apoapsis in an Orbitron at three different cathode voltages. One of the benefits of higher cathode voltages is that less elliptical orbits are required for collisional energies at the deuterium–tritium and deuterium–He[3] fusion cross section peaks. Depending on cathode voltage, the range of _E_ com covers the high fusion reactivity range for deuterium–deuterium, deuterium–tritium, and deuterium–He[3] fusion.[19] When high reactivity is coupled with high ion densities, which is the focus of our research, meaningful fusion reaction rates are achievable. 

## _2. Electron confinement_ 

Electron confinement in the Orbitron is magnetron confinement in the _r_ - _θ_ plane coupled with magnetic mirror confinement in _z_ . The magnetic mirror confinement in _z_ is augmented electrostatically by the protrusions on each end of the cathode in the ± _z_ directions, forming an electrostatically plugged magnetic bottle. The 

![](images/tmpt737zoze.pdf-0004-09.png)

**FIG. 3.** For a fixed apoapsis and cathode voltage, the eccentricity of the ion orbits, described by _βO_ , determines the collisional energy _E_ com and, thus, fusion reactivity in this simplified _r_ – _θ_ approximation of confined ion dynamics. Collisional energies with high fusion reactivity are possible for a range of cathode voltages and eccentricities. 

_E_ × _B_ field arrangement that supports these mechanisms is illustrated in Fig. 4. Electrons are pushed away from the cathode by the strong electric field shown by the black arrows (∇Φ[0] ≡− **E** ). The magnetic field, which provides both radial and axial confinement of the electrons, is shown with the red field lines and gray dashed magnetic field contours. 

Two confined electron trajectories are shown in Fig. 4 (blue and magenta curves). Without the magnetic field, electrons would be pushed radially outward from the cathode toward the anode. With the magnetic field as shown, the electrons are radially confined. Electrons undergo _E_ × _B_ orbits in the _r_ – _θ_ plane around the cathode similar to the electron confinement in a magnetron.[15] For illustration purposes, these trajectories were simulated for the geometry and fields shown in Fig. 4 using IBSimu,[20] a computer simulation package for ion optics with capabilities for tracking particles in electric and magnetic fields. 

As shown in Fig. 4, electrons in the Orbitron encounter increasing ∣ **B**[0] ∣ as they take excursions in ± _z_ . This increasing magnetic field creates a magnetic mirror, which helps provide axial confinement of the electrons.[21,22] Figure 5 illustrates this axial confinement for the two test particles shown in Fig. 4. These test electrons experience 

![](images/tmpt737zoze.pdf-0004-14.png)

**FIG. 4.** An r–z cross section showing the gradient of the electric potential (black arrows), magnetic field lines (red curves), and magnetic field magnitude (in Tesla) contours (gray dashed) for the prototype −100 kV Orbitron with _Bz_ = 0.05 T at the mid-plane ( _z_ = 0, _r_ = 6 cm). Electrons are confined in _E_ × _B_ orbits by the axial magnetic field and in _z_ by the magnetic mirror augmented by the electric field created by the cathode end-caps. Two sample electron trajectories are shown in blue and magenta. 

![](images/tmpt737zoze.pdf-0005-04.png)

**FIG. 5.** Electron _z_ -axis magnetic mirror confinement. In (a), the top electron in Fig. 4, the magnetic force alone maintains the correct polarity of _z_ -axis acceleration. The mirror effect is reduced, however, by the presence of the electric field—a compromise for enabling ion confinement. In (b), the bottom electron in Fig. 4, an example of an electron that would become accelerated in the wrong direction (at far right) was it not for the electrostatic augmentation of the mirror. 

an acceleration from the increasing magnetic field that pushes them back toward _z_ = 0. 

The _z_ component of acceleration due to the electric field, _Ez_ , is also shown in Fig. 5. Some of the _z_ electric force on electrons is a necessary by-product of the shaping of the electric field for the purpose of ion acceleration and is, thus, a compromise in electron behavior in order to support ion confinement. Separately, some of the electric force is due to the protrusions on each end of the cathode. These protrusions shape the electric field in order to augment the _z_ -confinement of the electrons. The presence or lack of these protrusions, and their geometry, is an additional design parameter that allows us to trade off the degree to which the magnetic mirror _z_ -confinement of electrons is augmented by electric force vs the effect of the protrusions on ion orbits. 

## B. Field perturbations at high density 

As the charged particle density increases, significant deviations from these single particle models will occur due to collective effects of the plasma, particle energy losses, and particles leaving the confinement region. For example, with non-zero particle conduction loss to the trap walls, the electric field will become perturbed due to sheath formation effects near the walls of the device.[22] Sheath perturbation effects will depend on rates of electron and ion flux to the walls, which are affected by the degree to which the particles are confined. In addition to wall sheath effects, our numerical studies described in Sec. V indicate the presence of collective ionelectron space-charge coupling effects in the trap, which also cause field perturbations. 

![](images/tmpt737zoze.pdf-0005-10.png)

**FIG. 6.** Perturbations in the electromagnetic field with the plasma will alter the particle trajectories from the vacuum potential model. (a) Orbitron electric potential contours in vacuum (black curves) and with a simulated (see Sec. V) high-density _n_ = 10[11] cm[−][3] quasi-neutral plasma density profile (red dashed). (b) Magnetic field magnitude (Tesla) contours in vacuum (black curves) and in the same high-density simulation (red dashed). The electrodes are shown in gray. 

Figure 6(a) illustrates simulated Orbitron electric field perturbations in a high-density scenario ( _n_ ≈ 10[11] cm[−][3] ) with co-confined electrons and ions. The presence of this nearly charge neutral plasma alters the confining potential (red dashed curves) from the ideal vacuum potential (black curves). The −100 and 0 kV contour lines correspond to the walls of the cathode and anode, respectively. Figure 6(b) illustrates the magnetic field perturbations in the same high-density scenario. The magnetized electrons rotate azimuthally at a higher velocity than the co-rotating ions. This induces an azimuthal current that alters the magnetic field. Our simulations (see Sec. V) indicate that ion and electron densities above the ion space charge limit are attained in the presence of these field perturbations; however, the particle trajectories are modified from the single particle model discussed previously. 

## III. DESIGN AND SUBSYSTEMS 

The core of the Orbitron system for deuterium–deuterium ( _D_ – _D_ ) fusion is illustrated in Fig. 7. A _D_[+] or _D_[+] 2[ion beam accelerated] across a voltage drop ∼10% of the magnitude of the cathode voltage is injected through a hole in one of the outer anodes. The cathode voltage is nominally −100 kV but is reduced depending on the experiment, and the beam energy is adjusted accordingly. Ions and electrons are confined as described in Sec. II. This section details the design and subsystems of the prototype −100 kV Orbitron, including 

![](images/tmpt737zoze.pdf-0006-04.png)

**FIG. 7.** An r–z cross section of the Orbitron. Ions (red arrow) are loaded into the potential well and orbit around the cathode. The high-voltage vacuum feedthrough currently enables voltages below −200 kV on the cathode. Electrons are confined through a magnetic field (colored contours) supplied by permanent magnets and an electromagnet trim coil. 

the vacuum chamber, our high voltage capabilities, the formation of the magnetic field, and the source of ions and electrons. Preliminary experiments on this −100 kV device are ongoing. We also describe future upgrades to the design that will enable higher cathode voltages and stronger magnetic fields. 

## A. Vacuum 

High neutral background pressures (>10[−][8] Torr) have been shown to reduce the lifetime of pure ion and pure electron plasmas confined at low-energies (<10 eV) in Penning–Malmberg traps[1] and reduce the coherence time of higher energy (≲ 5 keV) ions in orbital ion traps.[23] These traps rely on azimuthal symmetry for confinement in a similar way as the Orbitron. Collisions of the trapped particles with the neutral background exert a torque on the particles causing transport toward the conducting walls and particle loss. With pressures below 10[−][8] Torr, particle confinement times greater than a second have been observed in Penning–Malmberg traps[1] and orbital ion traps.[23] In Penning–Malmberg traps, confinement times are limited by azimuthal asymmetries of the device[24–26] in the absence of externally applied torque.[27] For the high-energy particles confined in the Orbitron (>10 keV), the collisional dynamics will be significantly different and work is currently underway to understand the influence of background pressure on the confinement time. However, to minimize transport from neutral collisions and the loss of ions from charge exchange [a typical challenge in inertial electrostatic confinement (IEC) devices], the Orbitron is typically operated in the ultra-high vacuum (UHV) regime (<10[−][8] Torr). 

Figure 8 shows an overview schematic of the vacuum system. A cryopump with a pumping speed of 2500 l/s for H2 enables a base vacuum pressure near 10[−][9] Torr in the Orbitron. The ion source (see Sec. III D) typically operates above 10[−][3] Torr; thus, strong differential pumping is required between the ion source and vacuum chamber. Differential pumping enables ion loading into the Orbitron with a slightly elevated pressure of near 10[−][8] Torr. 

![](images/tmpt737zoze.pdf-0006-10.png)

**FIG. 8.** An overview schematic of the vacuum system. Differential pumping connects the medium vacuum D2 ion source to the ultra-high vacuum chamber that holds the Orbitron. A cryopump connected to this chamber enables a base pressure near 10[−][9] Torr with the ion source off and near 10[−][8] Torr while loading ions. 

## B. High voltage

Given the compact geometry of the Orbitron and the UHV requirement, the generation, transmission, and maintenance of high voltage on the cathode are major challenges. There have been several attempts to develop HV vacuum bushings, such as those for ITER's Neutral Beam Injector and the University of Wisconsin-Madison's inertial electrostatic confinement (IEC) reactor.[?] These designs, however, either failed to achieve the desired values or were too large for the Orbitron.

Figure [?] depicts our design of a 300 kV UHV bushing.[?] This bushing incorporates a MACOR [?] spacer placed between UHV and a potting compound at atmospheric pressure. The potting compound, whether oil, room temperature vulcanizing (RTV) silicone, or resin, ensures the electrical integrity of the cable–cathode connection. The resistivity pattern on the insulator surface is designed to reduce the probability of surface flashovers. This bushing has been tested below −200 kV on the Orbitron device, and experiments are underway to achieve the −300 kV design operation.

At these high voltages, the choice of materials, the machining process, and polishing are pivotal to controlling electron emission rates and prevention of flashovers and arcs. The cathode and anode are machined from molybdenum (the cathode) and copper (anode). MACOR is used as the dielectric due to its machinability, ease of use, and high dielectric strength (129 MV/m). Future research on high-voltage materials will aim to investigate alternative substitutes for the aforementioned components with the objective of enhancing reliability and reducing current loss.

To achieve these high voltages, the cathode is conditioned to safely quench and redistribute as probabilistically as many and 'primary' microparticle events as possible so that the total number of potential hazards to the stability is significantly reduced. These are conditioning procedures in which the protrusions and field emitters at the surface of the cathode are removed with the aid of controlled discharges, which arise from electric fields. On Orbitron, the most common methods is current conditioning in which the protrusions are exposed either to an arc eroding them, or an emission by the bombardment of the cathode with the desorbted gases ejected from the anode during conditioning. We have adopted two different conditioning methods, current conditioning and gas conditioning.

## C. Magnets

In the device capable of ~100 kV cathode voltages, a 0.05 T magnetic field at the midplane ($z = 0$, $r = 0$) is sufficient to capture fine electrons (see Sec. II A 3). For this low magnetic field, we use neodymium magnets in a Halbach array modified by a trim coils system mounted on the drift plates (see Sec. III B).[?] For electron confinement at higher cathode voltages down to ~300 kV, we rely on superconducting magnets for higher magnetic field strengths. Two specially designed, high-temperature superconducting magnet coils placed on either side of the midplane will generate a sole magnetic field with a field strength of 0.5 T at the mid-plane ($z = 0$, $r = 0$ m). With the addition of a variable trim coil, investigations of how the magnetic field topology affects the electron confinement time will be explored.

## D. Ion sources and loading

Since ions are confined in the Orbitron by their angular momentum, ions must be loaded into the trap with significant azimuthal energy to form elliptical orbits about the cathode. One of the significant achievements of the orbital ion trap used for mass spectrometry was developing a loading scheme that preserves to a high degree the azimuthal symmetry of the device. In these traps, the cathode voltage is increased during the first few axial oscillations to reduce the ion's apoapsis and form stable orbits well above the anode walls. Here, we assume that with a sufficient loading efficiency and ion beam current, cathode ramping will reach ion densities above the space charge limit. Significant work is underway to explore alternative loading techniques and to experimentally demonstrate the operation of the Orbitron above the space charge limit.

To create the highly elliptical orbits needed for fusion, ions are accelerated across a voltage drop of 30–50% the magnitude of the cathode voltage. The desired beam current necessarily scales with the loading efficiency and confinement time; however, our estimates predict that 1–10 mA will be sufficient for reaching ion densities above the space charge limit of ~10$^{12}$ cm$^{-3}$ in the trap.

Our experiments use a readily available MARK I End Hall ion source, which we have modified to suit our needs.[?] The source outputs a high current, broad beam of singly ionized deuterium gas, D$^+$. Ion energies of up to 20 keV are possible by floating this source. The energy spread of the beam at the design point operating conditions was measured to be −75% D$^+$, 20% D$_2^+$, and 5% D$_3^+$. This source is currently operated with a cathode voltage of 120–150 V and a discharge current of 0.7 A. The beam is focused and steered into the Orbitron using a Sikler lens.

## E. Electron source

For our electron source, we are currently taking advantage of the cold field emission of the cathode.[?] This leakage current serves as an ideal electron source since it loads the trap from the center of the device. When ~100 kV is applied to the conditioned molybdenum cathode, a leakage current of ~1–10 mA is achieved; however, higher source currents are achieved for optimum loading through field emission by the application of an extended duration of electrons through ion impacts on the cathode surface. We have also designed a dedicated electron gun capable of utilizing the cathode voltage to provide this high loading current if required.

## IV. DIAGNOSTICS

To measure the plasma density, particle energy, particle confinement time, fusion rate, and fusion spatial distribution, we are currently deploying an initial set of diagnostics. For initial experiments of proof of densification of the ions above the space charge limit of the trap, the plasma density will be relatively low $\leq 10^8$ cm$^{-3}$. For such low density plasmas, some diagnostics targeting low density rules out some diagnostics such as laser interferometry and optical Thomson scattering borderline. These density diagnostics will be more useful for future higher density experiments. Our current diagnostics are at a relatively low complexity, which adds a level of complication to the analysis of some of the diagnostics we will be discussing in this section.

Depending on the type of experiment, the Orbitron confines pure ion plasmas, pure electron plasmas, or quasi-neutral plasmas in the magnetic field region. As for pure electron plasma and electron or pure ion plasma, we are able to characterize the confinement

properties of the Orbitron and benchmark simulations in a simpler system. In this section, we will introduce some of the diagnostics we are currently developing for this device.

## A. Microwave interferometry

Microwave interferometry is sensitive to electron plasma densities from about $10^9$ to $10^{15}$ cm$^{-3}$, which makes it an ideal diagnostic for probing densities near the space charge limit. Interferometry probes the electron plasma density by launching an electromagnetic wave through the plasma (signal arm) and comparing the phase shift of the signal arm to a reference arm (reference arm), which is phase locked to the signal arm. The phase shift, caused by the index of refraction of the plasma, is related to the plasma density through:

$$\delta\phi = \frac{2\pi}{\lambda} \int_0^L \frac{\omega_p^2}{2\omega^2} dl = \frac{e^2}{m_e \epsilon_0 c \omega} \int_0^L n_e \, dl, \tag{3}$$

where $\delta\phi$ is the phase shift in radians, $\lambda$ is the wavelength of the probing electromagnetic radiation, $n_e$ is the electron density, and the integral is over the path length through plasma. The lowest electron density that can be successfully resolved is determined by the path length (which is constrained by other design requirements to about 6 cm), the wavelength of the probing radiation, and the phase resolution of the measurement. Electron densities on the order of $10^9$ cm$^{-3}$ will produce 100ths of degrees of phase shift with a probe frequency of 60 GHz. The interferometry operates at 60 V-band (50–70 GHz); higher frequency designs will become feasible as the electron density increases. At 60 GHz, the spatial resolution of this density diagnostic is about 5 mm. This diagnostic will mainly be used to measure the average electron density in the device.

## B. Optical emission spectroscopy

Optical emission spectroscopy (OES) is commonly used in laboratory plasmas to diagnose plasma parameters like temperature and electron density. This technique requires the presence of optically-photon-emitting species. In the case of impurities, common discharge state ions, such as $\text{C}^+$, $\text{O}^+/\text{O}^{2+}$, $\text{N}^+/\text{N}^{2+}$, and the vibrations of molecular species, can be identified through the assignment of characteristic lines.

In the case of a pure electron plasma, the intentional introduction of a background gas is used to study the electron properties. Initial experiments in the Orbitron have introduced argon gas into the electron plasma and observed peaks from excited neutral argon (Ar) and singly ionized argon (Ar$^+$) due to collisions of the confined electrons with the background gas. At lower sub-keV voltages (~20 keV), these data may be used to study electron energies in density by the common line ratio analysis. At higher cathode voltages, more complex coronal indirect modeling of line emission is being explored, which will require electron gas collisional cross sections. Measurements are with an intensity-calibrated spectrometer. This diagnostic enables narrower lines of sight than microwave interferometry so that it can aid the understanding of the electron density profile.

For experiments with $D^+$ ions, line emission will not be observed. In this case, molecular band emission arising from passing the fast D$^+$ ion with a neutral gas or beam will be explored. This will give information on the fast ion properties of the confined deuterium beam.

## C. Soft x-ray radiation

The high-energy electrons confined in the Orbitron will emit x-ray radiation when they undergo acceleration from particle collisions, which is referred to as Bremsstrahlung radiation. This radiation is peaked in the soft x-ray range (<10 keV) because the dominant collision per unit angle scattering occurs for thermal plasmas; measurements of this radiation spectrum are a diagnostic tool to extract the electron temperature. For our non-thermal plasma, this radiation is present; however, a more detailed analysis is required to deconvolve the electron energy distribution from the energy spectrum of the Bremsstrahlung emission.

Experiments with pure electron plasmas are investigating the soft x-ray radiation emitted from electron collisions with a neutral gas backfill. The electron collisional cross sections for x-ray radiation from collisions with neutral gases, such as argon, have been well-studied theoretically. This will enable measurements of the electron energy distribution along a line-of-sight. Density measurements can also be possible with an intensity-calibrated soft x-ray spectrometer by measuring the intensity of this Bremsstrahlung emission along with additional spectral contributions from electron excitation of line emission from the background gas. This diagnostic will also be used in the future to quantify power loss in our system from Bremsstrahlung radiation.

## D. Image current

For the purpose of optimizing the ion loading process and measuring ion lifetimes in the low-density limit, we employ the method of image current measurement using a cryogenic amplifier mass spectrometry. The anode is bisected through the mid-plane as shown in Fig. 1 and electrically reconnected via a high-speed, low noise current sensor, which measures the transfer of image charge between the two halves as charged particles bounce axially. For the typical operating conditions of the Orbitron, the oscillation frequency is in the MHz range. To measure this image current, a pulsed ion beam can be injected and the image current sensor records up to a half period of this oscillation. A packet of ions injected in this way will ride a decaying sinusoidal image-current signal. The amplitude of this signal indicates loading efficiency, and the decay rate is a combination of when the ion experiences loss; if that ion loss rate is faster than the decoherence time of the ion pulse.

Image current measurements are also routinely used in nonneutral electron plasmas at densities to diagnose space-charge waves and instabilities. Similar to Trivelpiece–Gould waves in Penning traps, bulk plasma instabilities in the Orbitron could be detectable by the induced axial image current. By segmenting an anode azimuthally, we will also be able to measure diocotron waves and bulk instabilities like the diocotron mode [see Sec. VI].

## E. Neutron measurements

The Orbitron produces fusion products when deuterium ions fuse via either the through-going beam fusion or the trapped beam–target fusions. At high ion densities, beam–beam fusion will dominate since it scales as the ion density squared. However, initially with low ion densities, it is important to test to distinguish between these fusion processes. To this end, we have added several diagnostics to determine both the total and spatial neutron production and the energy spectra of neutrons.

## _1. Total rate_ 

For total neutron production rates, bubble and Helium-3 (He-3) detectors are useful and simple diagnostics. Bubble detectors contain a polymer gel interspersed with small liquid droplets. When a high-energy neutron strikes the liquid, the droplet vaporizes, leaving behind a bubble. Bubble detectors BD-PND (personal neutron dosimetry) from Bubble Technology Industries (BTI Chalk River, Ontario) have a response range from 0.2 to 15 MeV, isotropic angular response, and zero responsivity to gamma radiation. 

Helium-3 neutron proportional counters provide a real-time measurement of the fusion rate. These detectors consist of tubes of He-3 gas with a central anode wire surrounded by a cathode. The tubes are encased in a moderator, such as High-Density Polyethylene (HDPE), which converts the fast fusion neutrons into thermal neutrons. Thermal neutrons interact with the He-3 gas to produce H[1] and H[3] , which both carry kinetic energy. The high-energy particles ionize the surrounding background gas, and electrons move toward the anode, while cations move toward the cathode. There is an avalanche amplification effect that occurs as the moving charges ionize more of the carrier gas. The charge on the anode is recorded on a preamplifier as a voltage pulse and counted. 

## _2. Neutron spatial and energy measurements_ 

In addition to measuring total production, properties of the neutrons, including energy and location of production, help distinguish the fusion process. The Orbitron can operate in both pulsed and steady-state modes. Steady-state operation prevents the use of some typical neutron detection systems that rely on timeof-flight measurements for neutron/gamma-ray discrimination and neutron spectroscopy. Instead, we use pulse-shape discriminating scintillators, which employ a scintillating material that produces a pulse of visible light when hit with either a gamma ray or a highenergy neutron.[50–52] By taking the integrated area of short ( _QS_ ) and long ( _QL_ ) time periods that include the tail of the pulse, a pulse shape discriminating ratio is defined as PSD = ( _QL_ − _QS_ )/ _QL_ . This ratio is small for gamma interactions and large for neutron interactions allowing discrimination of the two events. Measurements of the neutron energy spectrum may be used to distinguish between beam–target fusion at the cathode and beam–beam fusion.[53] 

Determining the spatial location of the fusion event will support the discrimination of beam–beam vs beam–target fusions. To measure the spatial location of neutron production, an array of small PSD detectors is embedded in high-density polyethylene, which acts as a collimator. The collimator thermalizes some neutrons that reach detectors off the desired line-of-sight, therefore, lowering their energy. By counting only neutrons that retain their full energy, spatial resolution on the order of centimeters is achieved. Beam–beam fusion will occur slightly away from the cathode where the relative radial energy of the ions is the largest, which will be resolvable with this neutron camera. 

## V. MITIGATING THE SPACE CHARGE LIMIT 

Both pure electron and pure ion plasmas confined in the Orbitron are limited in density by the space charge potential of the 

confined particles. For pure electron plasmas in this device, this density limit is near the well-known Brillouin limit,[2,3] 

![](images/tmpt737zoze.pdf-0009-13.png)

In the initial prototype Orbitron with _B_ = 0.05 T, the electron density is, therefore, limited to _nB_ ≈ 1.2 × 10[10] cm[−][3] . For pure ion plasmas, the axially confining potential is weaker than the radial confinement. At ion densities _n_ ≳ 10[9] cm[−][3] , the ion plasma potential will overcome the axial confinement for a −100 kV cathode voltage, and the ions will leak out the ends of the device, limiting the ion density. 

Figure 9(a) shows the density evolution of two separate WarpX[54] particle-in-cell simulations of a pure electron (black) and a pure ion (red) plasma confined in the Orbitron. For these simulations, the cathode voltage is −100 kV and the magnetic field strength is about 0.05 T at the mid-plane ( _z_ = 0, _r_ = 6 cm). These simulations assume azimuthal ( _θ_ ) symmetry. To build up high densities with less computation time, high injection currents are used. In the first 2 _μ_ s, the electron and ion injection currents are ramped up to 0.4 A. This loading current remains on for a total of 25 _μ_ s. The D[+] loaded ions in the pure ion simulation are given an initial azimuthal energy of 10 keV from an initial position inside the Orbitron spanning _r_ = 4–5 cm and _z_ = −3 to −2 cm to place them in elliptical orbits around the cathode. External ion loading is not modeled in these simulations. In the pure electron simulations, the electrons are loaded over a thin ( _z_ = −1 to 1 mm) radial plane spanning from cathode to anode with an initial energy of 600 eV. The electron and ion macroparticle weight is 1 × 10[7] particles, the grid size is 0.25 × 0.25 mm[2] , and the time step is 2.0 × 10[−][12] s. We use the WarpX electromagnetostatic solver option that includes the calculation of self-magnetic fields induced by the plasma. Here, we are plotting the average density over an annulus spanning from the cathode to the anode with a width of 2 cm centered at _z_ = 0. 

These non-neutral plasma simulations show the space charge limited density of this trap. The pure electron plasma (black solid line) reaches a max average density of 7.4 × 10[9] cm[−][3] , which is near the predicted Brillouin limit (black dashed line). After the electron source is turned off at 25 _μ_ s, the electron density decreases with a loss rate of 20 mA. With this high cathode voltage and weak magnetic field, the electrons are weakly confined; thus, this loss current is not too surprising. Superconducting magnets will enable stronger magnetic fields, which should reduce this loss current. In the pure ion plasma (red line) simulations, the ions are more strongly confined with a loss current of 0.3 mA but are limited by space charge to a lower density of 1.1 × 10[9] . To reach high ion densities relevant for fusion applications, this ion space charge limit must be mitigated. 

Figure 9(b) shows a PIC simulation in which electrons are coloaded with ions in this device to mitigate this ion space charge limit. The simulation parameters and particle loading are identical to the pure electron and pure ion plasma simulations shown in Fig. 9(a). Here, we see that the electron and ion densities couple enabling loading to higher densities. An average ion density of 5.4 × 10[10] cm[−][3] , about 50 times larger than the pure ion plasma density, is reached with the same loading conditions. After the loading current is ceased at 25 _μ_ s, the density begins to decrease, with 

![](images/tmpt737zoze.pdf-0010-04.png)

**FIG. 9.** PIC simulations of (a) pure electron and pure ion plasmas confined separately in this device. These simulations show the respective space charge limited density for these two charge species. When electrons and ions are co-confined, simulations (b) predict that quasi-neutral plasma densities above these space charge limits are achievable. 

the two loss rates tracking together. It is likely that the loss rate is determined by the transport losses of one species, which the other species tracks in accordance with the associated reduction in the space charge limit. These simulations include Coulomb collisions, using the WarpX implementation of the Direct Simulation Monte Carlo method, but the collision time at these high energies is larger than the duration of the simulations. 

As illustrated in Fig. 6, the plasma self-fields weaken the magnetic field in some areas. This may be a factor in reducing confinement performance. These self-fields may also limit the achievable density for a given magnetic field and are currently being explored in more detail. These effects are taken into account in calculating Fig. 9. 

The spatial density profiles of deuterons and electrons at _t_ = 35 _μ_ s are shown in Fig. 10. The two species are illustrated separately; however, in the simulation, they are co-confined together throughout the trap. Both density profiles are rotated 360[○] in _θ_ around the cathode. The density profile suggests the presence of a collective space-charge coupling effect. In the high-density regions along _z_ = 0, the two densities were calculated to match within ±10%. The ion density in Fig. 10 is more constricted axially than the electrons since the ions are confined by the potential well created by the anode/cathode geometry, whereas the electrons are confined in _z_ by the electrostatically plugged magnetic mirror that extends to the cathode protrusions. 

To exceed the space charge limit of this device with a reasonable computation duration, we have artificially increased the loading currents. Experimentally, the initial electron and ion injection currents will be around 1–10 mA. Therefore, to reach the simulated densities, we will require an experimental loading duration on the order of 1–10 ms assuming the ideal simulated loading. On this 

timescale, collective effects, instabilities, and collisional effects (see Sec. VI) may arise, which are not captured in these simulations. However, the computation time to replicate the exact experimental conditions is outside of the scope of this work. These initial 

![](images/tmpt737zoze.pdf-0010-11.png)

**FIG. 10.** Particle density spatial profile from PIC simulation at _t_ = 35 _μ_ s. Deuterons and electrons are illustrated separately but are co-confined together. Both density profiles are rotated 360[○] in _θ_ around the cathode. The simulations assume azimuthal symmetry. 

simulations show promising results for exceeding the space charge limit, and we will attempt to understand these possible limitations through experiments. 

## VI. INSTABILITIES, COLLISIONS, AND RADIATION 

A key focus of experiments on this device is mitigating the space charge limit. However, to achieve efficient fusion events, ion densities well above this limit must be achieved with a relatively low loss of energy. Instabilities, particle diffusion to the conducting walls, and radiative losses can all limit the fusion efficiency. 

Instabilities are a collective process in which a plasma relaxes from a non-thermal state in a time scale faster than a collision time. Initial simulations of pure electron plasmas on this device have seen the classic diocotron instability.[49] Nascent theory with the support of simulations suggests that this mode might be stabilized at our higher cathode voltages, and experiments are planned to test this voltage suppression. Similar _E_ × _B_ devices have also observed anomalous transport due to the electron cyclotron drift instability.[55,56] Simulations of quasi-neutral plasmas above the space charge limit have not been dominated by configuration-space instabilities, which might be due to damping from the strong shear flow in our device as predicted in mirror machines.[57] Velocity–space instabilities, such as beam–beam and beam–plasma instabilities, are a concern as a possible source of energy loss from the colliding beams. These instabilities have not been directly observed in simulations of this device; however, they may be an issue at higher densities and will be explored. 

Collisional diffusion of the particles to the conducting walls is another source of energy loss. Ion–ion Coulomb collisions are scattering events, which will alter the ideal elliptical trajectory. A feature of this device is that the frequency of 90[○] scattering events is small compared to the orbital frequency of the ions. Work is in progress to understand the impact of these small angle scattering events on the trajectory of the ions and the timescale at which they cause diffusion to a conducting surface. Electrons will also diffuse across the magnetic field toward the anode due to Coulomb collisions with electrons and ions. With a moderate magnetic field, this diffusion will be on a timescale of multiple collision times. 

Particle collisions will not only cause diffusion but also thermalization of the velocity distribution function. The fusion reaction rate will be highly dependent on the velocity distribution of the ions. With the beam–beam velocity distribution predicted in the absence of thermalization, high fusion rates can be achieved at densities and for device scales significantly lower than traditional reactors. In practice, the ion velocity distribution will most likely be somewhere in-between a pure beam and thermal distribution, which will reduce the neutron flux. 

An inherent energy loss mechanism of this device is Bremsstrahlung radiation, which is a commonly cited concern for fusion reactors with non-Maxwellian energy distributions.[58] A key goal of our research is to characterize the Orbitron particle distribution functions and phase space dynamics in order to substantiate a detailed power balance analysis using the methodology described in Ref. 59. 

## VII. CONCLUSIONS 

In summary, we have presented the physics of single-charge particle confinement and detailed the experimental apparatus of a 

new plasma confinement scheme called an Orbitron. This crossedfield device confines ions in orbits around a high-voltage cathode at fusion-relevant energies with co-rotating electrons confined by a relatively weak magnetic field. Particle-in-cell simulations show that these co-rotating electrons enable ion densities above the ion space charge limit. Demonstrating this space charge mitigation will be the focus of initial experiments. After this fundamental science goal is − achieved, this device will be scaled up to higher voltages ( 300 kV) and stronger magnetic fields (0.5 T) to achieve higher fusion reaction rates. 

## ACKNOWLEDGMENTS 

The authors thanked A. Makarov, S. Tsurkan, C. Reilly, M. Prato, J. Hummelt, and R. Wirz for helpful discussion and a careful review of our manuscript. This material was based upon work supported by the National Science Foundation under Grant No. 2303759. This research used the open-source particlein-cell code WarpX (https://github.com/ECP-WarpX/WarpX), primarily funded by the U.S. DOE Exascale Computing Project. Primary WarpX contributors are with LBNL, LLNL, CEALIDYL, SLAC, DESY, CERN, and TAE Technologies. They acknowledged all WarpX contributors. This research also used resources of the National Energy Research Scientific Computing Center, a DOE Office of Science User Facility, supported by the Office of Science of the U.S. Department of Energy under Contract No. DE-AC02-05CH11231 using NERSC Award No. FES-ERCAP0029121. 

## AUTHOR DECLARATIONS 

## Conflict of Interest 

The authors have no conflicts to disclose. 

## Author Contributions 

**M. Affolter** : Investigation (equal); Writing – original draft (equal); Writing – review & editing (equal). **R. Thompson** : Writing – original draft (equal); Writing – review & editing (equal). **S. Hepner** : Writing – original draft (equal). **E. C. Hayes** : Writing – original draft (equal). **V. Podolsky** : Writing – original draft (equal). **M. Borghei** : Writing – original draft (equal). **J. Carlsson** : Investigation (equal). **A. Gargone** : Investigation (equal); Writing – original draft (equal). **D. Merthe** : Writing – original draft (equal). **E. McKee** : Writing – original draft (equal). **R. Langtry** : Supervision (equal). 

## DATA AVAILABILITY 

The data that support the findings of this study are available from the corresponding author upon reasonable request. 

## REFERENCES 

> 1J. H. Malmberg and C. F. Driscoll, “Long-time containment of a pure electron plasma,” Phys. Rev. Lett. **44** , 654–657 (1980). 

> 2D. H. E. Dubin and T. M. O’Neil, “Trapped nonneutral plasmas, liquids, and crystals (the thermal equilibrium states),” Rev. Mod. Phys. **71** , 87–172 (1999). 

> 3J. R. Danielson, D. H. E. Dubin, R. G. Greaves, and C. M. Surko, “Plasma and trap-based techniques for science with positrons,” Rev. Mod. Phys. **87** , 247–306 (2015). 

> 4R. E. March, “An introduction to quadrupole ion trap mass spectrometry,” J. Mass Spectrom. **32** , 351–369 (1997). 

> 5R. D. Knight, “Storage of ions from laser-produced plasmas,” Appl. Phys. Lett. **38** , 221–223 (1981). 

6K. J. Gillig, B. K. Bluhm, and D. H. Russell, “Ion motion in a Fourier transform ion cyclotron resonance wire ion guide cell,” Int. J. Mass Spectrom. Ion Processes **157–158** , 129–147 (1996). 

> 7A. Makarov, “Electrostatic axially harmonic orbital trapping: A highperformance technique of mass analysis,” Anal. Chem. **72** , 1156–1162 (2000). 

> 8X.-P. Huang, J. J. Bollinger, T. B. Mitchell, W. M. Itano, and D. H. E. Dubin, “Precise control of the global rotation of strongly coupled ion plasmas in a Penning trap,” Phys. Plasmas **5** , 1656–1663 (1998). 

9T. B. Mitchell, M. M. Schauer, and D. C. Barnes, “Observation of spherical focus in an electron Penning trap,” Phys. Rev. Lett. **78** , 58–61 (1997). 

> 10D. C. Barnes, T. B. Mitchell, and M. M. Schauer, “Beyond the Brillouin limit with the Penning fusion experiment,” Phys. Plasmas **4** , 1745–1751 (1997). 

11R. Langtry and B. Riordan, Orbital Confinement Fusion Device, 2023. 

> 12K. H. Kingdon, “A method for the neutralization of electron space charge by positive ionization at very low gas pressures,” Phys. Rev. **21** , 408–418 (1923). 

13R. H. Perry, R. G. Cooks, and R. J. Noll, “Orbitrap mass spectrometry: Instrumentation, ion motion and applications,” Mass Spectrom. Rev. **27** , 661–699 (2008). 

> 14A. Kharchenko, G. Vladimirov, R. M. A. Heeren, and E. N. Nikolaev, “Performance of orbitrap mass analyzer at various space charge and non-ideal field conditions: Simulation approach,” J. Am. Soc. Mass Spectrom. **23** , 977–987 (2012). 

> 15D. Andreev, A. Kuskov, and E. Schamiloglu, “Review of the relativistic magnetron,” Matter Radiat. Extremes **4** , 067201 (2019). 

16A. Makarov, E. Denisov, and O. Lange, “Performance evaluation of a high-field orbitrap mass analyzer,” J. Am. Soc. Mass Spectrom. **20** , 1391–1396 (2009). 

> 17D. Grinfeld, M. Monastyrskiy, and A. Makarov, “Control of aberration and space-charge effects in the orbitrap mass analyzer,” Microsc. Microanal. **21** , 176–181 (2015). 

18R. H. Hooverman, “Charged particle orbits in a logarithmic potential,” J. Appl. Phys. **34** , 3505–3508 (1963). 

19S. E. Wurzel and S. C. Hsu, “Progress toward fusion energy breakeven and gain as measured against the Lawson criterion,” Phys. Plasmas **29** , 062103 (2022). 

> 20T. Kalvas, O. Tarvainen, T. Ropponen, O. Steczkiewicz, J. Ärje, and H. Clark, “IBSIMU: A three-dimensional simulation software for charged particle optics,” Rev. Sci. Instrum. **81** , 02B703 (2010). 

> 21M. I. Fuks and E. Schamiloglu, “Application of a magnetic mirror to increase total efficiency in relativistic magnetrons,” Phys. Rev. Lett. **122** , 224801 (2019). 

> 22F. F. Chen, _Introduction to Plasma Physics and Controlled Fusion_ (Springer, Cham, 2016). 

23Q. Hu, R. J. Noll, H. Li, A. Makarov, M. Hardman, and R. Graham Cooks, “The orbitrap: A new mass spectrometer,” J. Mass Spectrom. **40** , 430–443 (2005). 

24J. D. Crawford, T. M. O’Neil, and J. H. Malmberg, “Effect of nonlinear collective processes on the confinement of a pure-electron plasma,” Phys. Rev. Lett. **54** , 697–700 (1985). 

25D. H. E. Dubin, “Theory and simulations of electrostatic field error transport,” Phys. Plasmas **15** , 072112 (2008). 

> 26A. A. Kabantsev, D. H. E. Dubin, C. F. Driscoll, and Y. A. Tsidulko, “Chaotic transport and damping from _θ_ -ruffled separatrices,” Phys. Rev. Lett. **105** , 205001 (2010). 

> 27X.-P. Huang, F. Anderegg, E. M. Hollmann, C. F. Driscoll, and T. M. O’Neil, “Steady-state confinement of non-neutral plasmas by rotating electric fields,” Phys. Rev. Lett. **78** , 875–878 (1997). 

> 28M. Boldrin, M. Simon, G. Escudero Gomez, M. Krohn, H. Decamps, T. Bonicelli, and V. Toigo, “The high voltage deck 1 and bushing for the ITER neutral beam injector: Integrated design and installation in MITICA experiment,” Fusion Eng. Des. **146** , 1895–1898 (2019). 

29A. N. Fancher, M. Michalak, G. Becerra, and G. Kulcinski, “Design and testing of a high voltage feedthrough for extending IEC operations to 300 kilovolts,” in _Fusion Technology Institute_ (University of Wisconsin, Madison, WI, 2014). 

> 30M. Borghei, R. Langtry, R. McMullen, B. Riordan, and R. Walker, “A compact, 300-kVDC bushing for operation under ultra-high vacuum pressure,” in _2022 IEEE Conference on Electrical Insulation and Dielectric Phenomena (CEIDP)_ (IEEE, 2022), pp. 471–474. 

> 31M. Borghei, D. Velazquez, R. McMullen, G. Latchford, B. Riordan, and R. Langtry, “Impact of direct current conditioning on cathode dark current in high vacuum,” in _2023 30th International Symposium on Discharges and Electrical Insulation in Vacuum (ISDEIV)_ (IEEE, 2023), pp. 74–77. 

> 32V. Podolsky, S. Hepner, S. Schipmann, S. Valenteen, R. Thompson, and R. Langtry, “Characterization of a broad beam ion source converted into a high intensity deuterium beam,” J. Phys.: Conf. Ser., **2743** , 012075 (2024). 

> 33P. Mandal, G. Sikler, and M. Mukherjee, “Simulation study and analysis of a compact einzel lens-deflector for low energy ion beam,” J. Instrum. **6** , P02004 (2011). 

> 34E. Z. Engelberg, J. Paszkiewicz, R. Peacock, S. Lachmann, Y. Ashkenazy, and W. Wuensch, “Dark current spikes as an indicator of mobile dislocation dynamics under intense dc electric fields,” Phys. Rev. Accel. Beams **23** , 123501 (2020). 

> 35D. Velazquez, W. Ohlinger, B. Vancil, F. Smith, B. Riordan, and R. Langtry, “Physicochemical structure of carburized thoriated tungsten and its effect on thermionic emission,” E-J. Surf. Sci. Nanotechnol. **2024** , 2024–022 (n.d.). 

36H. J. Hartfuss, “RF techniques in plasma diagnostics,” Plasma Phys. Controlled Fusion **40** , A231 (1998). 

37V. Podolsky, A. Khomenko, and S. Macheret, “Time-resolved measurements of electron number density in argon and nitrogen plasmas sustained by high-voltage, high repetition rate, nanosecond pulses,” Plasma Sources Sci. Technol. **27** , 10LT02 (2018). 

> 38A. Kramida, Y. Ralchenko, and J. Reader, NIST ASD Team, _NIST Atomic Spectra Database_ (NIST, 1999), https://physics.nist.gov/asd. 

39K. Behringer and U. Fantz, “Spectroscopic diagnostics of glow discharge plasmas with non-Maxwellian electron energy distributions,” J. Phys. D: Appl. Phys. **27** , 2128 (1994). 

40J. B. Boffard, C. C. Lin, and C. A. DeJosephJr, “Application of excitation cross sections to optical plasma diagnostics,” J. Phys. D: Appl. Phys. **37** , R143 (2004). 

> 41X.-M. Zhu and Y.-K. Pu, “Optical emission spectroscopy in low-temperature plasmas containing argon and nitrogen: Determination of the electron temperature and density by the line-ratio method,” J. Phys. D: Appl. Phys. **43** , 403001 (2010). 

42L. C. Pitchford, L. L. Alves, K. Bartschat, S. F. Biagi, M. C. Bordage, A. V. Phelps, C. M. Ferreira, G. J. M. Hagelaar, W. L. Morgan, S. Pancheshnyi, V. Puech, A. Stauffer, and O. Zatsarinny, “Comparisons of sets of electron–neutral scattering cross sections and swarm parameters in noble gases: I. Argon,” J. Phys. D: Appl. Phys. **46** , 334001 (2013). 

> 43Y.-K. Kim, “Scaling of plane-wave Born cross sections for electron-impact excitation of neutral atoms,” Phys. Rev. A **64** , 032713 (2001). 

> 44W. W. Heidbrink, K. H. Burrell, Y. Luo, N. A. Pablant, and E. Ruskov, “Hydrogenic fast-ion diagnostic using Balmer-alpha light,” Plasma Phys. Controlled Fusion **46** , 1855 (2004). 

> 45I. H. Hutchinson, _Principles of Plasma Diagnostics_ , 2nd ed. (Cambridge University Press, Cambridge, 2002). 

46S. M. Seltzer and M. J. Berger, “Bremsstrahlung energy spectra from electrons with kinetic energy 1 keV–10 GeV incident on screened nuclei and orbital electrons of neutral atoms with Z = 1–100,” At. Data Nucl. Data Tables **35** , 345–418 (1986). 

47A. W. Trivelpiece and R. W. Gould, “Space charge waves in cylindrical plasma columns,” J. Appl. Phys. **30** , 1784–1793 (1959). 

> 48M. Affolter, F. Anderegg, D. H. E. Dubin, and C. F. Driscoll, “Measurements of long-range enhanced collisional velocity drag through plasma wave damping,” Phys. Plasmas **25** , 055701 (2018). 

> 49C. F. Driscoll, “Observation of an unstable _l_ = _1_ diocotron mode on a hollow electron column,” Phys. Rev. Lett. **64** , 645–648 (1990). 

> 50E. V. Ryabeva, I. V. Urupa, E. E. Lupar, V. V. Kadilin, A. V. Skotnikova, Y. A. Kokorev, and R. F. Ibragimov, “Calibration of EJ-276 plastic scintillator 

for neutron–gamma pulse shape discrimination experiments,” Nucl. Instrum. Methods Phys. Res., Sect. A **1010** , 165495 (2021). 

> 51S. Nyibule, J. Tõke, E. Henry, W. U. Schröder, L. Acosta, L. Auditore, G. Cardella, E. De Filippo, L. Francalanza, S. Gianì, T. Minniti, E. Morgana, E. V. Pagano, S. Pirrone, G. Politi, L. Quattrocchi, P. Russotto, A. Trifiró, and M. Trimarchi, “Birks’ scaling of the particle light output functions for the EJ 299-33 plastic scintillator,” Nucl. Instrum. Methods Phys. Res., Sect. A **768** , 141–145 (2014). 

52C. C. Lawrence, M. Febbraro, T. N. Massey, M. Flaska, F. D. Becchetti, and S. A. Pozzi, “Neutron response characterization for an EJ299-33 plastic scintillation detector,” Nucl. Instrum. Methods Phys. Res., Sect. A **759** , 16–22 (2014). 53J. M. Mitrani, J. A. Brown, B. L. Goldblum, T. A. Laplace, E. L. Claveau, Z. T. Draper, E. G. Forbes, R. P. Golingo, H. S. McLean, B. A. Nelson, U. Shumlak, A. Stepanov, T. R. Weber, Y. Zhang, and D. P. Higginson, “Thermonuclear neutron emission from a sheared-flow stabilized Z-pinch,” Phys. Plasmas **28** , 112509 (2021). 

54L. Fedeli, A. Huebl, F. Boillod-Cerneux, T. Clark, K. Gott, C. Hillairet, S. Jaure, A. Leblanc, R. Lehe, A. Myers, C. Piechurski, M. Sato, N. Zaim, W. Zhang, J.-L. Vay, and H. Vincenti, “ _Pushing the frontier in the design of laser-based electron accelerators with groundbreaking mesh-refined particle-in-cell simulations on exascale-class supercomputers_ ,” in _SC22: International Conference for High Performance Computing, Networking, Storage and Analysis_ (IEEE, 2022), pp. 1–12. 55D. W. Forslund, R. L. Morse, and C. W. Nielson, “Electron cyclotron drift instability,” Phys. Rev. Lett. **25** , 1266–1270 (1970). 

> 56S. Tsikata and T. Minea, “Modulated electron cyclotron drift instability in a high-power pulsed magnetron discharge,” Phys. Rev. Lett. **114** , 185001 (2015). 

> 57R. Ellis, A. Case, R. Elton, J. Ghosh, H. Griem, A. Hassam, R. Lunsford, S. Messer, and C. Teodorescu, “Steady supersonically rotating plasmas in the Maryland Centrifugal Experiment,” Phys. Plasmas **12** , 055704 (2005). 

> 58T. H. Rider, “Fundamental limitations on plasma fusion systems not in thermodynamic equilibrium,” Phys. Plasmas **4** , 1039–1046 (1997). 

59N. Rostoker, A. Qerushi, and M. Binderbauer, “Colliding beam fusion reactors,” J. Fusion Energy **22** , 83–92 (2003). 

