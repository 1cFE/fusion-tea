---
source: "https://bluelaserfusion.com/wp-content/uploads/2025/10/Laser-based-inertial-fusion-energy-system-enabled-by-optical-enhancement-cavities-and-a-direct-drive-configuration-reactor.pdf"
source_type: "url"
extracted_at: "2026-04-04T16:35:24.333887+00:00"
content_hash_sha256: "6a0e75eb3dd4bc3282e2c998bdc9165897cb43ae9b9187eaa4ddde30b39ec753"
backend: "pdf_pipeline"
---

# **Laser-based inertial fusion energy system** **enabled by optical enhancement cavities and a** **direct-drive configuration reactor**

## **ATSUSHI SUNAHARA, [*] GAURAV RAJ, TREVOR COHEN, P.** **MORGAN PATTISON, PAUL RUDY, YUYA OHARA, SEITA IIZUKA,** **HIROAKI OHTA, AND SHUJI NAKAMURA**

_Blue Laser Fusion, Inc., 6950 Hollister Ave._ _Goleta, CA 93117, USA_
_*asunahara@bluelaserfusion.com_

**Abstract:** We propose a novel and highly efficient laser inertial fusion energy reactor concept
based on the shock ignition scheme, in which laser-plasma instabilities are mitigated through
500-beam, multicolor, slowly rotating polarization laser beam irradiation. The system employs
coherent beam-combined fiber lasers injected into high-finesse optical enhancement cavities,
which have already demonstrated energy enhancement factors approaching 60,000 and are
expected to surpass 100,000. The 1.06 µm laser output is frequency-tripled to 0.35 µm ultraviolet
light, resulting in an overall wall-plug-to-ultraviolet-light efficiency of approximately 10%. The
reactor integrates a helium-gas-cooled lead-lithium blanket and a direct energy conversion for
high-efficiency operation. It is designed for cryogenic deuterium-tritium targets in a direct drive
scheme at 1–10 Hz, repetition rate, providing net electric output at 0.1–2.8 GW. This approach
offers a compact, scalable, and credible pathway toward practical commercial laser fusion energy.

Published by Optica Publishing Group under the terms of the Creative Commons Attribution 4.0 License.

Further distribution of this work must maintain attribution to the author(s) and the published article’s title,

journal citation, and DOI.

**1.** **Introduction**

Blue Laser Fusion Inc. (BLF) was cofounded in California, USA, in 2022 by Prof. Shuji Nakamura,
recipient of the 2014 Nobel Prize in Physics [1], shortly before the historic demonstration of
net energy gain in laser inertial confinement fusion (ICF) at the National Ignition Facility (NIF)
at Lawrence Livermore National Laboratory (LLNL) [2–5]. His invention of highly efficient
blue LED [6] revolutionized global lighting by dramatically improving energy efficiency, which,
in turn, reduced carbon emissions [7]. Building on this legacy, we are now working to address
global energy and environmental challenges through the development of a laser fusion power
reactor. Our core technology is based on Coherent Beam Combining (CBC) [8] in combination
with Optical Enhancement Cavity (OEC) [9], which together will enable highly efficient and
cost-effective megajoule-class pulsed laser systems operating at repetition rates up to 10 Hz by
coherently injecting pulse trains from fiber lasers into the OEC.
The principles of the OEC have already been demonstrated in continuous-wave (CW) systems
such as the Laser Interferometer Gravitational Wave Observatory (LIGO) [10,11] and other
applications [12–17]. We are developing the OEC laser system to generate high-intensity,
nanosecond-duration pulses for laser fusion applications and have already achieved significant
power enhancement within the cavity [18]. We plan to scale up the CBC-OEC laser system to
achieve a power enhancement factor of 100,000, enabling pulses of approximately 10 kJ per OEC
module. By combining 500 such modules, we aim to construct a scalable 5 MJ-class laser system
suitable for a practical fusion power reactor. This system will be used to irradiate cryogenic
deuterium-tritium (DT) targets in a direct-drive ICF scheme. Our goal is to establish the first
full-scale CBC-OEC prototype by 2027 and to demonstrate a pilot fusion reactor in the 2030s.

#575181 https://doi.org/10.1364/OE.575181
Journal © 2025 Received 31 Jul 2025; revised 10 Oct 2025; accepted 15 Oct 2025; published 29 Oct 2025

A related concept, the "StarDriver" design proposed by Eimerl et al. [19], envisioned more
than 10,000 beams of 100 J each, amplified by DPSSL-pumped glass modules and spectrally
broadened to suppress Laser-plasma instabilities (LPIs) [20]. While this approach shares with
our CBC+OEC system the use of broadband multi-beam drivers for LPI mitigation, it faced
major challenges in both cost and implementation. The reliance on glass amplifiers made the
system relatively less cost-effective, and the extreme port density imposed severe constraints on
chamber engineering, including blanket layout and heat-transfer system design. Moreover, as
noted by Eimerl et al., fiber laser technology was not yet mature in 2014, preventing its use in that
concept. By contrast, our approach coherently combines mass-produced fiber lasers and stores
the energy in high-finesse optical enhancement cavities to generate 10 kJ per beam with 500
beams. This substantially reduces the number of external beams, relaxes both control-system
and chamber-integration constraints, and provides a more cost-effective driver architecture while
retaining the bandwidth and flexibility needed for advanced LPI suppression.
The main challenge in laser inertial fusion energy (IFE) [21] is to realize a plasma core with
high density, high areal density, and high temperature, and to initiate thermonuclear burning,
thereby efficiently achieving high fusion energy output. To achieve this, we adopt a slow implosion
approach to mitigate the growth of hydrodynamic instabilities to attain a high areal density of the
fuel, and then use the shock ignition scheme (SI) [22], which offers high gain. The fuel target is
first slowly imploded using a relatively low intensity compression laser pulse to achieve high
density and high areal density by keeping the inflight aspect ratio _R_ /∆ _R_ relatively small, thereby
achieving high density and high areal density, where _R_ and ∆ _R_ are the target radius and shell
thickness, respectively. Subsequently, a high intensity ignition pulse is injected to launch a strong
shock wave, generating high temperature and high density conditions by collision of shock waves
near the center of the core, triggering thermonuclear burn [23]. Here, since the ignitor pulse has
a significantly higher intensity than in conventional central ignition schemes, it is essential to
suppress laser-plasma instabilities (LPIs), which can degrade the coupling of the laser energy

[20].
Our BLF CBC-OEC laser system can generate pulses at high efficiency, 1–10 Hz repetition
rate, and low cost with design flexibility to tune the pulse duration, pulse shape, effective
spectral width, polarization state, and beam delivery configuration to the target. Using this
flexibility, we aim to realize the LPI-mitigated SI for effectively achieving high-gain fusion
energy output. The 500 beam CBC-OEC laser system provides significantly more uniform target
illumination than conventional direct-drive laser fusion systems [24]. By superimposing beams
with slightly shifted central wavelengths, the system achieves multicolor, effective broadband
illumination, which helps mitigate LPIs. Additionally, by overlapping circularly polarized beams
with different central wavelengths, a polarization state that rotates slowly over time, known as
slowly rotating polarization (SRP) [25], is generated. This dynamic polarization modulation
disrupts the spatial and temporal coherence required for LPI growth. Combined, these features
provide robust suppression of LPIs, ensuring symmetric target compression and robust shock
ignition. Furthermore, zooming is achieved by setting the compression pulse and ignition pulse
at different focal points, allowing more laser energy to be coupled into the plasma.
By combining these innovative CBC-OEC laser techniques and irradiation configurations
with shock ignition–based laser fusion, our approach aims to achieve a target gain exceeding
100, which is sufficient for practical laser fusion power generation. This enables the delivery
of sub-GW to GW-class electric output through 5-MJ laser pulses at a repetition rate of 1–10
Hz. To support this performance, the reactor incorporates a magnetized dry wall chamber [26],
which allows efficient and sustained repetition of the entire fusion cycle over extended operational
periods, including injection of cryogenic DT targets, fusion burn, plasma exhaust handling,
energy extraction, and tritium breeding.

This paper is structured as follows. Section 1 introduces the general concept; Section 2
describes the laser system; Section 3 discusses LPI-mitigated shock ignition; Section 4 presents
the conceptual reactor design; and Section 5 provides a conclusion.

**2.** **Laser system**

Key requirements for commercialization include ultraviolet (UV) wavelength, pulse shaping
control, spatial beam profile homogeneity, and broad bandwidth [27]. In addition, low production
and maintenance costs, high reliability, MJ-class laser energy on the target, and a 1-10 Hz
repetition rate are essential [21]. To meet these demanding requirements, we are developing a
novel laser system architecture in which fiber-laser outputs are first coherently combined (CBC)

[8] and then injected into an OEC [9].
Traditional solid-state amplifying technologies utilize large doped gain glass and either flash
lamp or diode laser pump lasers to excite the amplifying medium. This approach is limited
in repetition rate, requires large volumes of specialty gain glass panels, requires novel thermal
management to avoid saturation, and requires extensive pump sources to achieve very high peak
pulse power levels at very low repetition rates due to the required long cooling time [28].
In contrast, our CBC-OEC laser operates on a fundamentally different principle and represents
a breakthrough in laser technology, capable of generating high-power laser pulses with high
efficiency, low cost, and high repetition rates, as required for laser fusion. The core part of this
laser system is a passive optical resonator that stores energy by coherently accumulating a train
of externally injected laser pulses. This approach enables a compact system to deliver high power
and high repetition rate without relying on a conventional gain medium. In this section, we
describe the configuration of the CBC-OEC system, its operating principles, energy enhancement
scaling, and the current status and roadmap for our laser development.

_2.1._ _CBC-OEC configuration_

Figure 1 shows the basic structure of the CBC-OEC laser module. This system coherently
combines the laser output from many high-repetition-rate fiber lasers and injects a phase-coherent
train of laser pulses into a Fabry–Pérot resonator formed by two highly reflective mirrors. The
injected pulses constructively interfere through multiple reflections between the mirrors, resulting
in efficient optical pulse stacking and energy buildup in the cavity. Owing to the high gain and
compact single-pass configuration of fiber lasers, they can be easily parallelized to generate pulse
trains with energy levels required for laser fusion implosions. Fiber amplifiers have superior cost
scaling relative to gain glass media. Moreover, they allow for the precise temporal pulse shaping
suitable for fusion applications.
Table 1 summarizes the characteristics of the laser output produced by the CBC-OEC module.
As a laser source for IFE, the fiber lasers generate pulses at a wavelength λ of 1060 nm, with ∆λ
of ± 10 nm and pulse duration of 0.1–10 ns, and inject them into the OEC. The OEC provides
polarization flexibility, allowing selection between linear and circular polarization. Inside the
cavity, the injected pulse train is coherently stacked to reach the desired high intensity. The
resulting output, which exhibits an effective spectral bandwidth of 30 GHz, is extracted and
subsequently wavelength-converted via second-harmonic generation (SHG) and third-harmonic
generation (THG) to 0.53 µm and 0.35 µm, respectively. These UV pulses are then used for
fusion target irradiation at repetition rates of 1–10 Hz.

_2.2._ _Scaling of OEC_

Efficient light storage in the OEC requires that the frequency components of the injected laser
pulses match the resonant modes of the cavity. The round trip time _TR_ of the cavity is determined
by its length _L_ and the speed of light _c_, and is given by: _TR_ = 2 _L_ / _c_ . This round trip time sets
the injection repetition frequency: _f_ rep = 1/ _TR_ . For example, a cavity length of 1.5 meters

**Fig. 1.** Pulses stack internally to yield a single enhanced pulse.Schematic of the CBC-OEC laser module. A phase-coherent pulse train is injected into an optical enhancement cavity formed by highly reflective mirrors, where the pulses constructively interfere and accumulate, enabling high-intensity output for laser fusion applications.

### Table 1. CBC-OEC Laser Pulse Conditions

| | | |
|---|---|---|
| Wavelength | $\lambda$ | 1060 nm |
| Changeable wavelength range | $\Delta\lambda$ | ±10 nm |
| Pulse width | $\tau$ | 0.1–10 ns |
| Polarization | | Linear and circular |
| Effective bandwidth of the each OEC output | $\Delta f$ | 30 GHz |
| Wall plug-to-light efficiency | $\eta_e$ | 0.16 |

corresponds to a repetition frequency $f_{\rm rep}$ of 100 MHz, whereas a 150-meter cavity corresponds to 1 MHz. When the repetition frequency of the injected pulse train matches $f_{\rm rep}$, a coherent buildup of energy occurs inside the cavity. The free spectral range, defined as FSR = $1/T_R = f_{\rm rep}$, corresponds to the frequency spacing between adjacent longitudinal modes. When pulses are injected at intervals that match $T_R$, their temporal periodicity creates a frequency comb that overlaps with these cavity modes. An OEC can support a narrow but non-zero bandwidth of captive frequencies in the form of a frequency comb.

As $L$ increases, the FSR decreases, allowing a larger number of modes to fit within the spectral bandwidth $\Delta f$ of the pulse. Specifically, the number of resonant modes within the pulse bandwidth is approximately $\Delta f/$FSR. This improves spectral matching between the injected pulse trains and the cavity resonances, enabling more efficient energy buildup. The enhancement factor, which is defined as the ratio of stored intra-cavity energy to injected energy, is governed by the finesse $F$, given by: $F \approx \pi(T + A + S)$, where $T$, $A$, and $S$ represent fractional losses per round trip due to mirror transmission, absorption, and scattering, respectively.

Minimizing these losses is essential to maximize finesse $F$ and enhance cavity performance. Under ideal conditions with negligible internal losses, the finesse is primarily determined by the mirror reflectivity. With mirrors of reflectivity greater than or equal to 99.999% and an ultraclean vacuum environment, energy enhancement factors greater than $10^5$ can be achieved at repetition rates of 1–10 Hz, as shown in Fig. 2.

While each mode of the frequency comb is as narrow as 1–5 Hz when the cavity finesse is high, the aggregate total of the modes sums up to a "bandwidth-in-parts" of $\Delta f = 30$ GHz. This bandwidth can be further enhanced if multiple OECs are used. Small tunable changes of the central wavelength, ranging from 1050–1070 nm wavelength to the spacing between the mirrors

**Fig. 2.** Ideal enhancement in an OEC vs the mirrors’ reflectivity

of each individual OEC, can result in a multitude of frequency combs, each spanning a slightly
different range. These combs can then be combined by dumping the pulse out of the cavities
which are directed to the overlapping irradiation on the fusion target as the multicolor, effective
broadband light. Thus, the relative bandwidth ∆ω/ω0 = |∆λ/λ| can be expanded to ∼ 1.9%
with multibeams, where ω0(= 2π _c_ /λ) and ∆ω are the angular frequency of the laser and its
changeable range, respectively.
The ideal enhancement in an OEC builds up as a function of the number of incident pulses into
the OEC. As the incident pulse, the pulse stacking begins gradually, grows exponentially, and
eventually saturates. The ratio of power accumulated in the OEC to injected power reaches 75%.
Consequently, the wall-plug-to-light efficiency of the CBC-OEC laser system η _w_, defined as the
ratio of electrical input to optical output at a wavelength of 1.06 µm, is estimated to reach 16%.
We have assembled a meter-class, benchtop OEC to validate the concepts described above.
Figures 3(a) and 3(b) show the high-quality beam profile and the vacuum chamber of the 1.5
m OEC in our US laser facility. High-finesse operation requires ultra-high reflectivity mirrors,
minimized optical loss, and excellent thermal and mechanical stability. High-reflectivity mirrors
with total optical losses below 10 ppm have already been experimentally demonstrated in the
near- or mid-infrared spectral regions [29–33]. We have successfully constructed the high-finesse
OEC prototype 1.5 m cavity using mirrors with more than 99.9995% reflectivity [18]. Under
CW operation, this system achieved a finesse of 419,000 and an energy enhancement factor of
59,000. The design of the OEC is briefly described below. The benchtop OEC is a two-mirror,
high-finesse, Fabry–Pérot cavity operated within a vacuum system. The vacuum system is
comprised of two 0.3 _m_ × 0.3 _m_ × 0.3 _m_ aluminum cubes that house each of the cavity mirrors.
The cubes are connected by a stainless-steel vacuum tube and pumped to a working pressure
of approximately 1 × 10 [−][5] torr by a turbomolecular pump from the center of the tube. The
cavity mirrors are 2 inches in diameter with a measured transmission of T = 3.4 ppm by the
coating vendors. These mirrors were mounted in stainless steel, vacuum-compatible mounts
from Thorlabs.
A simplified diagram of the optical layout is shown in Fig. 4. The laser is injected into the
OEC externally through one of the cavity mirrors that comprise the OEC. The output of a CW,
15 mW, wavelength tunable, 20 kHz bandwidth, vertically polarized, fiber laser is coupled to a

![](images/tmpk0ego815.pdf-4-0.png)

![](images/tmpk0ego815.pdf-4-1.png)

**Fig. 3.** (a) Beam profile of the transmission through the cavity when the laser is locked to
the TEM0,0 mode. The beam diameter is 3.2 mm (FWHM). (b) OEC vacuum chamber with
1.5 m cavity length [18].

30 GHz bandwidth, phase modulating fiber Electro-Optic Modulators (EOMs). This fiber EOM
modulates the laser at approximately 20 MHz, generating two reference sidebands used for the
PDH lock. The output of the two EOMs is directed into a fiber amplifier outputting a maximum
of 1.2 W and collimated in free space.

**Fig. 4.** A simplified optical layout of the 1.5 m OEC.

The laser is locked to the cavity using the Pound-Drever-Hall (PDH) method [34]. The cavity
mirrors within the OEC are passively mounted without any feedback control. Feedback control
is instead actuated on the laser, adjusting the output wavelength of the oscillator to match the
cavity free spectral range. Sensing for the feedback mechanism is accomplished by a photodiode
detector positioned to receive light rejected by the injection-side cavity mirror. The finesse of the
cavity was evaluated by measuring the storage lifetime of the cavity through a cavity ringdown
experiment, as described by Isogai et al. [35]. The finesse of a 2-mirror Fabry–Pérot cavity, F,
can be calculated by the following formula: _F_ = 2π × _FSR_ × τ, where τ is the lifetime the laser
remains within the cavity. The length of the cavity was measured by a ruler to be 1.25 m and the
free spectral range of the cavity was estimated by the formula: _FSR_ = 2 _cL_ [to be 120 MHz.]
The storage lifetime of the OEC, which is the time it takes for the light to exit the cavity by 1/e
of the locked intensity, was measured by means of a cavity ringdown experiment. To measure
τ, a 1 GHz response photodiode detector was positioned at the transmission end of the OEC,
intercepting any laser light that leaks through both high reflectivity mirrors.
After locking the cavity and reaching a resonant steady state, the source laser is turned off,
unlocking the cavity and resulting in the slow leak out of light from the cavity through both cavity
mirrors. This leakage is observed on the photodiode detector as an exponential decay, which was
fitted and was found to have a half-life of 557.5 µ _s_ in Fig. 5. The resultant finesse of the cavity
was determined to be 419,000.
The enhancement factor of the cavity is a measure of the ratio of the average power circulating
within the cavity and the power injected into the cavity. The power incident to the cavity and
the power transmitted through the cavity while locked were measured to be 1.2 W and 240 mW,

![](images/tmpk0ego815.pdf-5-0.png)

![](images/tmpk0ego815.pdf-5-1.png)

**Fig. 5.** The cavity ringdown of the OEC upon shutting off the injection laser entering the
cavity.

respectively. The power circulating within the cavity while locked can be estimated as the power
transmitted through the cavity divided by the transmission of the end cavity mirror. This was
estimated to be 71 kW. While not all of the light is coupled to the cavity due to mode mismatch
between the injection laser and the resonant TEM0,0 mode of the cavity, we can conservatively
estimate the enhancement factor of the cavity as 59,000 times.
The 15 meter long CBC-OEC systems are currently being constructed at both the Blue Laser
Fusion Goleta site and Osaka University, as shown in Figs. 6(a)–6(c), targeting a pulse energy of
100 J and 10 kW injection laser.

**Fig. 6.** (a) the 15m OEC at the Goleta facility in the US, (b) an 8-channel CBC utilizing
fiber rod amplifiers under construction, and (c) the 15 m OEC developed and built at the
BLF Japan Osaka site.

_2.3._ _Toward a reactor-scale laser_

We plan to scale up the CBC-OEC system by increasing both the injection laser power and the
optical storage capacity of the OEC, primarily through extending the cavity length. Figure 7
shows the output pulse energy as a function of the injection laser power for various cavity lengths.
A 150-meter-scale cavity, capable of producing 10–16 kJ pulses 100 kW injection laser, is
currently under design in collaboration with Caltech, Osaka University, and other partners. This
configuration supports amplification factors up to 100,000, enabling the delivery of pulses at the
reactor scale.

![](images/tmpk0ego815.pdf-6-0.png)

![](images/tmpk0ego815.pdf-6-1.png)

![](images/tmpk0ego815.pdf-6-2.png)

**Fig. 7.** BLF Laser-OEC power-energy-length stages. The pulse energy output per OEC as a
function of the averaged power of the injected laser.

To meet these specifications, development efforts are focused on improving the vacuum system,
high-reflectivity mirror alignment, thermal management, and active stabilization techniques.
Enhanced optical coatings, precision mirror mounts, and real-time feedback control systems
are being advanced to ensure stable and efficient operation under high thermal loads. In the
150-meter OEC configuration, each CBC-OEC laser module will coherently combine a 100
mJ, 1 MHz injection beam using mirrors with 99.9995% reflectivity. This architecture is being
developed as a baseline laser driver for laser fusion reactors targeted for practical application in
the early 2030s, with the first full-scale CBC-OEC prototype to be developed by 2027.
The purple markers in Fig. 7 indicate experimental milestones along the projected scaling
trajectory. A gigawatt-scale laser IFE power plant can be realized by aggregating the outputs of
500 to 1,000 CBC-OEC modules, delivering 5 MJ of laser energy per shot at a repetition rate of
1–10 Hz to the fusion targets. The CBC-OEC platform offers a high degree of configurational
flexibility, allowing precise control over polarization, phase, timing, pulse shaping, wavelength,
and spectral bandwidth across all modules. This flexibility is critical for maximizing laserplasma coupling efficiency and achieving the target gain necessary for practical, high-efficiency,
gigawatt-class laser IFE power generation.

**3.** **LPI-mitigation**

In the SI, the initial target compression is driven by 5–10 ns laser pulses with moderate intensities
( _I_ 0 _c_ ≈ 5 × 10 [14] W/cm [2] ). In a later stage, the ignition shock is delivered by a much shorter pulse
of duration τ0 _i_ ≈ 0.5–1 ns, but with significantly higher intensity ( _I_ 0 _i_ ≈ 10 [15] –10 [16] W/cm [2] ).
One of the main challenges in this scheme is the mitigation of LPIs [36,37], which arise from
the interaction of laser beams with the dynamically evolving plasma corona surrounding the
irradiated fuel target. Parametric LPIs such as stimulated Brillouin scattering (SBS), stimulated
Raman scattering (SRS), two-plasmon decay (TPD), and cross-beam energy transfer (CBET)

[20,38] can grow and saturate both linearly and nonlinearly, resonantly exciting secondary
electromagnetic and electrostatic waves in the plasma corona with electron density _ne_ . As shown
in Fig. 8, these LPIs occur in different density regions of the plasma corona and significantly
modify the energy deposition and transport of the laser. Although such interactions often reduce

![](images/tmpk0ego815.pdf-7-0.png)

![](images/tmpk0ego815.pdf-7-1.png)

![](images/tmpk0ego815.pdf-7-2.png)

![](images/tmpk0ego815.pdf-7-3.png)

the efficiency of laser–plasma coupling, some LPI-induced hot electrons with energies below
∼100 keV can beneficially contribute to strengthening the shock wave [39,40].

**Fig.** **8.** Parametric LPIs in the corona region with electron plasma density _ne_ regimes,
such as SRS, SBS, TPD, and CBET, respectively. Below the critical density _ne_ = _ncr_,
the laser is absorbed and unabsorbed one is reflected. TPD occurs at the quarter-critical
density _ne_ = _ncr_ /4. Energetic hot electrons with energies exceeding 100 keV can preheat
the compressed plasma core, thereby degrading the compression process. In contrast, hot
electrons with energies below 100 keV can enhance the shock wave.

![](images/tmpk0ego815.pdf-8-0.png)

![](images/tmpk0ego815.pdf-8-1.png)

The SBS can grow when the three-wave matching condition is fulfilled among the incident
light angular frequency ω0 = 2π _c_ /λ, ion acoustic wave, and scattered light, and its growth
rate is defined by γ _SBS_ = ω _pivos_ /4√︁ _ki_ /ω0 _cs_, where the ion-acoustic wave’s frequency ω _i_, wave

rate is defined by γ _SBS_ = ω _pivos_ /4√︁ _ki_ /ω0 _cs_, where the ion-acoustic wave’s frequency ω _i_, wave

vector _ki_, and velocity _cs_ are related through the dispersion relation ω _i_ = _cski_ . In the case
of Back SBS _ki_ ≈ 2 _k_ 0, where in plasma _k_ 0 = (ω0/ _c_ )(1 − _ne_ / _ncr_ ) [1][/][2], for λ0 = 0.351 µ _m_ and
_cs_ ≈ 0.1% × _c_ = 0.3 µ _m_ / _ps_, Fig. 9 shows the dependence of γ _SBS_ on the laser strength parameter
_a_ 0 ≈ 8.55 × 10 [−][10] λ0[µ _m_ ]√︁ _I_ 0[ _W_ / _cm_ [2] ] and a linear increase in plasma electron density _ne_ / _ncr_

_a_ 0 ≈ 8.55 × 10 [−][10] λ0[µ _m_ ] _I_ 0[ _W_ / _cm_ [2] ] and a linear increase in plasma electron density _ne_ / _ncr_

along the laser propagation direction, where _ncr_ = _me_ ω0 [2][/][4][π] _[e]_ [2] [is the critical density for incident]
laser light, with _e_ and _me_ being the elementary electron charge and mass, respectively. The
strength parameter _a_ 0 is related to the amplitude of the electron quiver velocity in the laser field
_vos_ = _a_ 0 _c_ = _eE_ 0/ _me_ ω0, where _E_ 0 is the laser electric field. In Fig. 9, γ _SBS_ increases significantly
as _a_ 0 and _ne_ / _ncr_, however, as _ne_ / _ncr_ → 1, the instability growth rate is suppressed after reaching
a maximum value at _ne_ / _ncr_ ≈ 0.6 as the simplified expression for γ _SBS_ does not include damping
effects. In a realistic situation, where damping effects are significant, the SBS growth rate peaks
at _ne_ / _ncr_ ≈ 0.2–0.3.
Another critical LPI is CBET [41–45], which scatters incident laser light out of the plasma
corona, bypassing the high-absorption region near _ne_ ≃ _ncr_ and thereby reducing ablation pressure
and drive symmetry in SI. CBET occurs when the beat wave of two overlapping electro-magnetic
waves (ω1,2, **k** 1,2) drives density perturbations via the ponderomotive force; these modify the
refractive index, forming a Bragg grating that transfers energy between beams (via SBS). CBET
can reduce hydrodynamic coupling by ∼ 30% [46], with projections up to ∼ 50% for an MJ-class
direct-drive facility [47]. SRS excites electron-plasma waves that scatter incident light and
reduce absorption [38,48,49]; when the incident, scattered, and plasma waves resonate, the
scattered-light and plasma-wave amplitudes grow exponentially [38].
In TPD, incident laser light decays into two electron-plasma waves near the quarter-critical
density in the fusion fuel. The electron plasma waves excited by TPD or SRS can resonantly
accelerate electrons to their phase velocity, producing hot electrons (∼ 40–100 keV) that transfer
laser energy to the electron population. In normal direct drive, such hot electrons can preheat the

**Fig.** **9.** Variation of the Back SBS instability growth rate γ _SBS_ with the laser strength
parameter _a_ 0 for _I_ 0 ≈ 10 [14]    - 10 [16] _W_ / _cm_ [2] and the plasma density _ne_ / _ncr_ .

compressed fuel and disrupt compression, whereas in SI, sub 100 keV electrons can be beneficial
by enhancing the shock pressure during ignition [39,40], which is also confirmed experimentally

[50].
Given the resonant nature of LPIs, any increase in the temporal incoherence, i.e. bandwidth,
of the laser driver will disrupt the seeding and growth of the LPIs. Previous investigations have
predicted that a large bandwidth can be effective in suppressing LPIs [51–54]. Recent numerical
studies [55,56] show strong suppression of LPIs such as CBET, by using the frequency-tripled
Nd:glass broadband laser with a bandwidth of ≈ 8 THz, (∆ω/ω0 ≃ 1.0% where ∆ω = 2π∆ _f_ ).
Another recent study shows that laser bandwidth can be used to increase threshold intensities for
LPIs by minimizing the coherence time of broadband laser pulses with random spectral phases

[56]. The 500 beam CBC-OEC laser system, to be constructed at the BLF site, can effectively
deliver the relative bandwidth of ∆ω/ω0 ∼ 1.9% (16 THz), which covers most of γ _SBS_ up to
_a_ 0 = 0.025 in Fig. 9, with multicolor illumination to the target, providing a unique framework
for LPI suppression. The solid-state ultraviolet Fourth-generation Laser for Ultrabroadband
eXperiments (FLUX) [57,58], recently built as a part of the OMEGA laser facility, is a highbandwidth (15 THz) system which will be used to quantitatively test the effects of bandwidth on
the LPIs. The FLUX can provide quantitative data for LPI suppression thresholds as a function of
bandwidth, helping to validate the CBC-OEC strategy proposed here to realize LPI-mitigated SI.
Another important strategy for reducing the coherence between the laser beam and the
plasma, thus suppressing the LPIs is to use Polarization Smoothing (PS) [59–63]. Recent
experiments have shown that a simple polarization state (linear or circular) has no effect on
reflection and transmission due to LPIs such as Back SBS [64]. However, for the case of
laser beams with SRP, the overall reflectivity due to LPIs can be significantly reduced due
to a reduction in the total interaction length [25]. In such a case of SBS the growth rate is
given by γ _SBS_ = _a_ 0 _ckp_ ω _pi_ /4[ω _s_ ω0] [−][1][/][2] | _cos_ Θ|, where ω _s_ and ω _pi_ are the angular frequency of
the scattered light and the ion plasma frequency, respectively, and Θ = Θ( _t_, _x_ ) is the rotation
angle of the polarization as a function of time and the 1D longitudinal spatial coordinate _x_ .
Particle-in-cell (PIC) simulations show that, for parameters similar to those of an ICF plasma,
polarization rotation can reduce the SBS reflectivity by a factor of 5. To effectively reduce
reflectivity, the rotation frequency of the polarization, Ω = |ω _L_ - ω _R_ |/2 given by overlapping
counter-rotating circularly polarized beams with angular frequencies of ω _L_ and ω _R_ [25], should
match the dominant instability growth rate ( _e_ . _g_ γ _SBS_ ), corresponds to a rotation frequency in

![](images/tmpk0ego815.pdf-9-0.png)

![](images/tmpk0ego815.pdf-9-1.png)

the tens of THz range, but the reduction saturates for higher rotation frequencies (Ω ≫ γ _SBS_ ).
Since the future BLF, IFE reactor plans to use 500 OEC lasers, pairs of frequency-shifted,
counter-rotating circularly polarized lasers can be used to generate SRP lasers, thus offering a
novel approach to modulating laser pulses for suppressing LPI reflectivity, in ICF plasmas.
Furthermore, currently all high-power laser-based ICF experiments rely on "smoothed" laser
beams, which use smoothing techniques such as random phase plates (RPP) [43,44,65,66] to
introduce spatial incoherence into the beams. Such beams, on a coarse scale, show a smooth
average intensity profile in their cross section, while on a fine laser wavelength scale they have a
speckle structure statistical distribution of the speckle peak intensity [43,44,67]. RPP produces
speckled laser beams with well-controlled and reproducible focal spot profiles with speckles fixed
in space and modulated in time by the varying amplitude of the laser intensity, thus reducing
any phase-front aberrations originating at the lens. From a time-domain viewpoint, the speckle
pattern in the focal plane changes at a rate determined by the total bandwidth of the modulation,
and thus, the time-integrated intensity seen by the plasma is smoothed. If this rate is faster than
the plasma response time, it significantly suppresses the LPIs. Thus, the BLF OEC laser system
offers a practical and scalable solution for mitigating LPIs in future laser IFE systems. These LPI
mitigation strategies are essential to enable robust and efficient operation of the laser-plasma
coupling in our reactor-scale architecture, discussed in Section 4.

**4.** **Reactor**

_4.1._ _System configuration_

Figure 10 illustrates the conceptual system of the prototype laser-driven inertial fusion energy
power plant. This design leverages the innovative direct-drive, LPI-mitigated SI uniquely enabled
by the CBC-OEC laser system. Each subsystem in this reactor is engineered to optimize energy
conversion, support high-repetition operation of 1–10 Hz, and ensure reactor longevity.

**Fig. 10.** Configuration of the laser IFE reactor

The wall-plug-to-light efficiency of the CBC-OEC laser at a wavelength of 1.06 µm, denoted
as η _w_, is projected to be 0.16. Subsequently, these infrared pulses (λ = 1.06 µm) are frequencytripled to UV light (λ = 0.35 µm) via THG in nonlinear optical crystals such as KDP/DKDP,
with a typical conversion efficiency of η3ω ≈ 0.6 [68]. The resulting overall wall-plug-to-0.35
µm light efficiency is η _w_ [∗] [=][ η] _[w]_ [×][ η][3][ω] [=][ 0.1.] [The 0.35] [µ][m UV light is used to irradiate cryogenic]
deuterium-tritium (DT) targets directly. The LPI-mitigated SI as described in the previous
chapter employs 500-beam multicolor pulses, providing superior irradiation uniformity. Mostly,
360 beams are designated for compression and another 140 for ignition. SRP is generated by

![](images/tmpk0ego815.pdf-10-0.png)

![](images/tmpk0ego815.pdf-10-1.png)

![](images/tmpk0ego815.pdf-10-2.png)

overlapping counter-rotating circularly polarized beams with slightly different center wavelengths
on the target. This temporal modulation of polarization interferes with the three-wave matching
conditions required for LPI growth, thereby effectively suppressing SBS, SRS, and TPD, while
irradiating the target uniformly. Additionally, the use of zooming and spatiotemporal pulse
shaping further optimizes the laser-target energy coupling, contributing to higher implosion
efficiency.
Approximately 70% of the fusion energy, carried by 14.1 MeV neutrons, is deposited in the
blanket, which converts thermal energy to electricity via helium gas cooling and a conventional
turbine generator. The blanket employs natural lithium (containing 7.5% [6] Li and 92.5% [7] Li)
as breeding material and a lead neutron multiplier (Pb). This configuration benefits from the
volumetric flexibility of IFE systems compared to Tokamak magnetic fusion energy (MFE)
reactors. The thermal-to-electric efficiency is assumed to be η _th_ = 0.4 with an additional 10%
contribution from the exothermic [6] Li(n, α)T reaction with tritium breeding, resulting in an
effective η _th_ [∗] [=] [0.44.] [In the collaborative development of the blanket system with universities]
and national laboratories, we focus on a blanket using silicon-carbide (SiC)-based ceramics
and cooling with helium gas, and we are investigating the possibility of integrating it with high
temperature gas-cooled reactor (HTGR) technology [69,70], which has operating temperatures
even higher than those envisioned for conventional nuclear fusion.
The remaining 30% of the fusion energy, associated alpha particles and plasma exhaust, are
guided to direct electricity conversion (DEC) units [71–73] positioned along magnetic field lines.
DEC systems utilize electrodes to extract electric power from ion kinetic energy. A conservative
efficiency of η _DEC_ = 0.44 is assumed. Designs based on recent theoretical work [73] will be used
to optimize ion collection geometries. DEC integration reduces the plant footprint and enhances
overall system efficiency.
In addition, unlike Tokamak MFE reactors that store DT fuel in the reactor chamber, the
amount of tritium in the IFE reactor chamber is limited to a few mg. Hence, the tritium cycle
system dominates the tritium inventory of the entire reactor system for separating and recovering
tritium from the blanket and plasma exhaust, and producing a new target and then injecting it
into the reaction chamber at 1 to 10 Hz. Therefore, by designing the tritium cycle to increase the
efficiency and speed of tritium processing, the tritium inventory of the system can be minimized.
This approach reduces the risk of radioactive tritium leakage throughout the reactor system,
supporting the realization of a safe fusion reactor.
The first wall should be designed to withstand impulsive loads from fusion-generated x-rays,
alpha particles, and plasma debris. A layered structure is adopted, with tungsten (W) [74,75] as
the facing material and reduced-activation ferritic-martensitic (RAFM) steel [76] as the structural
support. Helium gas is used for active cooling. To mitigate the localized wall loading due to the
deposition of charged particles, a chamber radius of 8–10 m is adopted, with embedded magnetic
fields [75] to deflect alpha particles toward exhaust ports. Magnetic fields generated at each laser
port provide magnetic fields within the dry-wall chamber. These magnetic fields serve to: (1)
spread and decelerate ion trajectories, reducing thermal spot intensity and (2) redirect relatively
low-energy plasma toward collection regions for DEC. Comprehensive magnetohydrodynamic
(MHD) and particle-in-cell (PIC) simulations will be performed to optimize field geometry and
wall survivability.
Reliable cryogenic DT target production at 1–10 Hz repetition rates is essential. Design
specifications include: (1) Submicrometer surface roughness, (2) Uniform cryo-layering, (3)
Positional accuracy, (4) Thermal shielding during flight. Although these are still major issues,
development will continue with the aim of demonstrating power generation in early 2030.
Component survivability under repetitive operation is a critical concern. Radiation-resistant
optics, tungsten-based wall coatings, and modular component design are designed to be adopted.
Remote handling and robotic inspection systems are incorporated for component replacement.

Survivability and radioactivation modeling of the first wall and chamber components will inform
replacement intervals and long-term operational planning.
Unlike HiPER [77] and LIFE [78], which relied on DPSSL-driven glass amplifiers, our
approach employs CBC of fiber lasers injected into OEC. This architecture is expected to
substantially reduce the cost of the system and enable the straightforward implementation of
broadband operation. In addition, in the LIFE design, the xenon-gas-protected dry-wall chamber
wall was considered [79]. In contrast, the HiPER design adopted a vacuum dry-wall chamber,
for which various plasma-facing materials (PFMs) were investigated [80]. Our reactor concept
further advances these dry-wall approaches by applying an external magnetic field to mitigate the
heat load on the first wall.

_4.2._ _Power balance_

The parameters related to the power flow in Fig. 10 are summarized in Table 2. The net fusion
power output _Pfus_ from laser irradiation of a target with laser energy _EL_ at a repetition rate f (Hz)
and target gain G, is expressed as: _Pfus_ = _EL_ × _G_ × _f_ . Of this total fusion energy, approximately
70% is carried by neutrons n [81] and captured in the blanket, where nuclear reactions with lead
′
Pb as follows: n + [208] _Pb_ → [207] _Pb_ + 2 _n_ - 7.4 MeV. Here, the number of neutrons is multiplied
′
and the neutron emitted n has a lower energy ∼ 1 MeV. This Pb has the reaction cross-section over
7 MeV of neutron energy. Also, 14.1 MeV neutrons can react with [7] Li over 2 MeV of neutron
energy as follows [82]: [7] _Li_ + _n_ → _T_ + [4] _He_ + _n_ ′′ - 2.8 MeV. Here, tritium T, alpha-particle 4He,
′′
and low-energy neutrons n are produced, respectively. Then, the relatively lower energy neutrons
< 2 MeV can react with [6] Li to produce T and [4] He as follows: [6] _Li_ + _n_ → _T_ + [4] _He_ + 4.8 MeV.

**Table** **2.** **Key parameters for the power balance of the laser IFE reactor.**

These reactions release thermal energy, providing an additional 10% contribution of the
thermal energy from the neutron-lithium reactions. The thermal energy is then used to drive a
conventional turbine-generator system to produce electricity. Assuming a nominal thermal to
electric conversion efficiency of η _th_ = 0.4, the effective conversion efficiency that includes the
10% thermal gain [27] becomes: η _th_ [∗] [=][ 1.1][ ×][ η] _[th]_ [=][ 0.44.]

![](images/page_012_table_0.png)

| Variable | Symbol | Reactor value |
| --- | --- | --- |
| Laser wavelength | λ0 | 0.35 µm |
| Relative bandwidth with multicolor beam irradiation | ∆ω/ω0 | 1.9 % |
| Laser energy irradiating the target per shot | EL | 5 MJ |
| Laser operation frequency | f | 1 to 10 Hz |
| CBC-OEC Laser wall-plug-to-light efficiency (λL = 1 µm) | ηw | 0.16 |
| Wavelength conversion efficiency, from 1 to 0.35 µm | η3ω | 0.6 |
| Overall wall-plug-to-0.35 µm light efficiency: η ∗ w = ηw × η3ω | η ∗ w | 0.1 |
| Target gain = fusion energy output / laser energy input | G | 160 |
| Conversion efficiency to electricity via blanket | ηthe | 0.44 |
| Direct Electricity Conversion efficiency | ηDEC | 0.44 |
| Total conversion efficiency from fusion to electricity: |  |  |
| ηe = 0.7ηthe + 0.3ηDEC | ηe | 0.44 |
| Facility operation power: (non-laser) | Pop | 100 MW |
| Laser operation power PLop = EL · f /η ∗ w | PLop | 50 to 500 MW |
| Fraction of recirculation, [Eq. (1)] | fre | 0.426 to 0.170 |
| Electricity power to grid, [Eq. (2)] | Pgrid | 102 to 2820 MW |

The remaining 30% of the fusion output, carried by alpha particles and other plasma exhaust

[81], is guided to the lower exhaust ports of the chamber by the applied magnetic field. There, it
is converted into electricity using a direct energy conversion (DEC) system that extracts electric
power from the kinetic energy of particles. Since actual efficiency η _DEC_ depends heavily on
the design, we conservatively assume: η _DEC_ = η _th_ [∗] [=] [0.44.] [Consequently,] [the] [total] [effective]
conversion efficiency from fusion to electricity, including both thermal and DEC channels, is
given by: η _the_ [∗] [=][ 0.7][ ×][ η] _th_ [∗] [+][ 0.3][ ×][ η] _[DEC]_ [=][ 0.44.]
Also assuming a wall-plug-to-0.35 µm wavelength light efficiency of η _w_ [∗] [=][ 0.1, the electrical]
power required to operate the laser is given by: _PLop_ = _EL_ × _f_ /η _w_ [∗] [.] [Furthermore, assuming the]
auxiliary facility operation power _Pop_ = 100 MW, the fraction of the generated power consumed
internally by the plant, the fraction of recirculating power _fre_ is calculated by:

[︃ 1
_fre_ =

_EL_ - _f_

![](images/page_013_eq_0.png)

+ _[P][op]_
η _w_ [∗] _EL_ 

]︃ 1

  - . (1)
_G_  - η _e_

![](images/page_013_eq_1.png)
Here, the first term in parentheses represents the laser operation, and the second term represents
other plant systems. Assuming _Pop_ is a constant independent of _EL_ or f, increasing the laser
energy _EL_ and the repetition rate f decreases _Pop_ ’s relative contribution to the recirculation
power. This indicates that, at higher laser throughput, the recirculating power is dominated
by the laser system itself. For example, when _EL_ = 5 MJ and f is varied from 1 to 10 Hz, the
recirculating power fraction, _fre_, decreases from approximately 0.426 to 0.170. The net electric
power delivered to the grid, _Pgrid_, can be expressed as:

_Pgrid_ = (1 − _fre_ ) · _EL_                 - _f_                 - _G_                 - η _e_                 - _Pop_ (2)

Thus, _Pgrid_ is strongly dependent on _EL_, f, and G. According to the study by Froula et al.

[56,83], the gain G as a function of the input laser energy _EL_ varies depending on the level of
suppression of hydrodynamic instability and LPIs, where three gain curves are reported: (i)
baseline with instabilities, (ii) CBET-mitigated, and (iii) ideal 1D case with CBET-mitigated,
respectively. As described in Section 3, our design employs 500 beams with relative bandwidth
∆ω/ω0 ∼ 1.9 %, SRP light to achieve: (1) high uniform irradiation, (2) LPI mitigation strategies
applicable to Direct Drive, and (3) independent focus (zooming) of compression and ignition
pulses. Given this advanced configuration, we anticipate a higher target gain G beyond the
CBET-mitigated curve of Froula (ii) and achieving a target gain of G = 160 at _EL_ = 5 MJ.
Therefore, for a repetition rate of f = 1–10 Hz, the net deliverable electric power _Pgrid_ ranges
from 102 MW to 2820 MW.

**5.** **Conclusion**

We have presented a new laser IFE reactor concept based on LPI-mitigated shock ignition
enabled by the CBC-OEC. The CBC-OEC with >99.9995% reflectivity mirrors enables energy
enhancement factors exceeding 59,000 and are projected to surpass 100,000 in scaled systems.
This configuration achieves an overall wall-plug-to-UV light (0.35 µm) efficiency of 10%. To
suppress LPIs, which have been a long-standing barrier to direct-drive laser fusion, potentially in
the SI, we employ an integrated strategy of 500-beam, multicolor, relative bandwidth ∆ω/ω0 ∼
1.9 %, SRP light irradiation with RPP and zooming. Together, these features enable exceptional
irradiation uniformity and LPI mitigation, achieving target gains exceeding 160 at 5 MJ input.
The reactor design incorporates a lithium-lead blanket cooled by helium gas and a direct energy
conversion system for ion energy recovery. These combined systems yield a net thermal plus
direct energy conversion efficiency exceeding 44%, enabling 0.1–2.8 GW _e_ net output at 1–10
Hz operation. The compact architecture, modularity, and limited tritium inventory support
scalability, maintainability, and operational safety. This approach offers a realistic and scalable

path toward commercial laser fusion power. The continued advancement of high-repetition OEC
platforms, integrated LPI suppression, and reactor subsystems is expected to enable net energy
gain and gigawatt-class electricity generation within the next decade. Compared to conventional
direct-drive or indirect-drive schemes, this approach leverages OEC-enabled optical architectures
to reduce system size and improve energy coupling, offering a transformative and scalable path
toward high-gain, high-repetition-rate laser fusion power plants.

**Funding.** This work was self funded by Blue Laser Fusion.

**Acknowledgment.** Preliminary OEC development support was provided by Professor Rana Adhikari of the
California Institute of Technology under a 2024 DOE INFUSE grant.

**Disclosures.** The authors declare no conflict of interest.

**Data availability.** Data underlying the results presented in this paper are not publicly available at this time but may
be obtained from the authors upon reasonable request.

**References**

1. J. Heber, “Nobel prize 2014: Akasaki, Amano & Nakamura,” Nat. Phys. **10** (11), 791 (2014).
2. H. Abu-Shawareb, R. Acree, P. Adams, _et al._, “Achievement of Target Gain Larger than Unity in an Inertial Fusion
Experiment,” Phys. Rev. Lett. **132** (6), 065102 (2024).
3. O. A. Hurricane, D. A. Callahan, D. T. Casey, _et al._, “Energy Principles of Scientific Breakeven in an Inertial Fusion
Experiment,” Phys. Rev. Lett. **132** (6), 065103 (2024).
4. M. Rubery, M. Rosen, N. Aybar, _et al._, “Hohlraum Reheating from Burning NIF Implosions,” Phys. Rev. Lett. **132** (6),
065104 (2024).
5. A. Pak, A. Zylstra, K. Baker, _et al._, “Observations and properties of the first laboratory fusion experiment to exceed a
target gain of unity,” Phys. Rev. E **109** (2), 025203 (2024).
6. S. Nakamura, T. Mukai, and M. Senoh, “High-power Gan P-N Junction Blue-Light-Emitting Diodes,” Jpn. J. Appl.
Phys. **30** (12A), L1998–L2001 (1991).
7. U.S. Department of Energy, “Energy Savings Forecast of Solid-State Lighting in General Illumination Applications,”
Tech. rep., Office of Energy Efficiency and Renewable Energy (2014). By 2030, LED lighting is projected to reduce
electricity use for lighting by nearly 40% and avoid 198 million metric tons of CO2 emissions annually.
8. V. Kozlov, J. Hernandez-Cordero, and T. Morse, “All-fiber coherent beam combining of fiber lasers,” Opt. Lett.
**24** (24), 1814–1816 (1999).
9. H. Stark, M. Müller, M. Kienel, _et_ _al._, “Electro-optically controlled divided-pulse amplification,” Opt. Express
**25** (12), 13494–13503 (2017).
10. J. Aasi, B. Abbott, R. Abbott, _et al._, “Advanced LIGO,” Classical Quantum Gravity **32** (7), 074001 (2015).
11. D. Ganapathy, W. Jia, M. Nakano, _et_ _al._, “Broadband Quantum Enhancement of the LIGO Detectors with
Frequency-Dependent Squeezing,” Phys. Rev. X **13** (4), 041021 (2023).
12. I. Chaikovska, K. Cassou, R. Chiche, _et_ _al._, “High flux circularly polarized gamma beam factory: coupling a
Fabry-Perot optical cavity with an electron storage ring,” Sci. Rep. **6** (1), 36569 (2016).
13. Z. Li, X. Deng, Z. Pan, _et al._, “Generalized longitudinal strong focusing in a steady-state microbunching storage
ring,” Phys. Rev. Accel. Beams **26** (11), 110701 (2023).
14. X. Deng, A. Chao, J. Feikes, _et al._, “Experimental demonstration of the mechanism of steady-state microbunching,”

Nature **590** (7847), 576–579 (2021).
15. B. Günther, R. Gradl, C. Jud, _et al._, “The versatile X-ray beamline of the Munich Compact Light Source: design,
instrumentation and applications,” Synchrotron Radiation **27** (5), 1395–1414 (2020).
16. X.-Y. Lu, R. Chiche, K. Dupraz, _et al._, “Stable 500 kW average power of infrared light in a finesse 35000 enhancement
cavity,” Appl. Phys. Lett. **124** (25), 251105 (2024).
17. X.-Y. Lu, R. Chiche, K. Dupraz, _et al._, “710 kW stable average power in a 45,000 finesse two-mirror optical cavity,”

Opt. Lett. **49** (23), 6884–6887 (2024).
18. T. Cohen, J. Mance, S. Gandrothula, _et al._, “Recent progress for commercializing IFE based on a novel high efficiency
10MJ laser and high-gain fuel target,” Optical Technologies for Inertial Fusion Energy **13358**, 14–19 (2025).
19. D. Eimerl, E. M. Campbell, W. F. Krupke, _et al._, “StarDriver: A Flexible Laser Driver for Inertial Confinement
Fusion and High Energy Density Physics,” Journal of Fusion Energy **33** (5), 476–488 (2014).
20. E. Campbell, V. Goncharov, T. Sangster, _et al._, “Laser-direct-drive program: Promise, challenge, and path forward,”

Matter Radiat. Extremes **2** (2), 37–54 (2017).
21. National Research Council, Division on Engineering and Physical Sciences, Board on Energy and Environmental
Systems, Board on Physics and Astronomy, Committee on the Prospects for Inertial Confinement Fusion Energy
Systems, _An Assessment of the Prospects for Inertial Fusion Energy_ (National Academies Press, 2013).
22. R. Betti, C. Zhou, K. Anderson, _et al._, “Shock Ignition of Thermonuclear Fuel with High Areal Density,” Phys. Rev.
Lett. **98** (15), 155001 (2007).
23. S. Atzeni, X. Ribeyre, G. Schurtz, _et al._, “Shock ignition of thermonuclear fuel: principles and modelling,” Nucl.
Fusion **54** (5), 054008 (2014).

24. T. Boehly, R. McCrory, C. Verdon, _et al._, “Inertial confinement fusion experiments with OMEGA-A 30-kJ, 60-beam
UV laser,” Fusion Eng. Des. **44** (1-4), 35–42 (1999).
25. I. Barth and N. J. Fisch, “Reducing parametric backscattering by polarization rotation,” Phys. Plasmas **23** (10), 102106
(2016).
26. L. A. Booth, D. A. Freiwald, T. G. Frank, _et al._, “Prospects of Generating Power with Laser-Driven Fusion,” Proc.
IEEE **64** (10), 1460–1482 (1976).
27. S. E. Bodner, “Comparison of an Argon-Fluoride Gas Laser with a Solid-State Laser for Application to Laser Fusion
Energy,” Journal of Fusion Energy **42** (2), 33 (2023).
28. S. B. Sutton, A. Erlandson, R. A. London, _et al._, “Thermal recovery of the NIF amplifiers,” in _Third International_
_Conference on Solid State Lasers for Application to Inertial Confinement Fusion_, vol. 3492 (SPIE, 1999), pp. 665–675.
29. G. D. Cole, W. Zhang, B. J. Bjork, _et al._, “High-performance near-and mid-infrared crystalline coatings,” Optica

**3** (6), 647–656 (2016).
30. I. Ito, A. Silva, T. Nakamura, _et al._, “Stable CW laser based on low thermal expansion ceramic cavity with 4.9 mHz/s
frequency drift,” Opt. Express **25** (21), 26020–26028 (2017).
31. G. Wachter, S. Kuhn, S. Minniberger, _et al._, “Silicon microcavity arrays with open access and a finesse of half a
million,” Light: Science Applications **8** (1), 37 (2019).
32. G.-W. Truong, L. W. Perner, D. M. Bailey, _et al._, “Mid-infrared supermirrors with finesse exceeding 400 000,” Nat.
Commun. **14** (1), 7846 (2023).
33. J. Agil, B. Letourneur, S. George, _et al._, “Characterisation of the waveplate associated to layers in interferential
mirrors,” The European Physical Journal Applied Physics **98**, 61 (2023).
34. R. W. Drever, J. L. Hall, F. V. Kowalski, _et al._, “Laser phase and frequency stabilization using an optical resonator,”

Appl. Phys. B **31** (2), 97–105 (1983).
35. T. Isogai, J. Miller, P. Kwee, _et al._, “Loss in long-storage-time optical cavities,” Opt. Express **21** (24), 30114–30125
(2013).
36. A. J. Schmitt and S. P. Obenschain, “The importance of laser wavelength for driving inertial confinement fusion
targets. I. Basic physics,” Phys. Plasmas **30** (1), 012701 (2023).
37. A. J. Schmitt and S. P. Obenschain, “The importance of laser wavelength for driving inertial confinement fusion
targets. II. Target design,” Phys. Plasmas **30** (1), 012702 (2023).
38. W. L. Kruer, _The Physics of Laser Plasma Interactions_ (CRC Press, 2019).
39. W. Shang, R. Betti, S. Hu, _et al._, “Electron Shock Ignition of Inertial Fusion Targets,” Phys. Rev. Lett. **119** (19),
195001 (2017).
40. W. Yuan, Z. Zhao, S. Zhu, _et al._, “Nonlocal effects on the shock-augmented ignition scheme of laser inertial fusion,”

Phys. Rev. Res. **6** (1), 013332 (2024).
41. I. V. Igumenshchev, W. Seka, D. H. Edgell, _et al._, “Crossed-beam energy transfer in direct-drive implosions,” Phys.
Plasmas **19** (5), 056314 (2012).
42. J. Moody, P. Michel, L. Divol, _et al._, “Multistep redirection by cross-beam power transfer of ultrahigh-power lasers in
a plasma,” Nat. Phys. **8** (4), 344–349 (2012).
43. G. Raj and S. Hüller, “Impact of Laser Beam Speckle Structure on Crossed Beam Energy Transfer via Beam
Deflections and Ponderomotive Self-Focusing,” Phys. Rev. Lett. **118** (5), 055002 (2017).
44. S. Hüller, G. Raj, W. Rozmus, _et al._, “Crossed beam energy transfer in the presence of laser speckle ponderomotive
self-focusing and nonlinear sound waves,” Phys. Plasmas **27** (2), 022703 (2020).
45. L. Yin, K. L. Nguyen, B. J. Albright, _et al._, “Effects of ion trapping and fluctuations of electron temperature and
plasma flow on cross-beam energy transfer,” Phys. Plasmas **30** (10), 102703 (2023).
46. T. Boehly, D. Brown, R. Craxton, _et al._, “Initial performance results of the OMEGA laser system,” Opt. Commun.

**133** (1-6), 495–506 (1997).
47. V. N. Goncharov, T. Sangster, R. Betti, _et_ _al._, “Improving the hot-spot pressure and demonstrating ignition
hydrodynamic equivalence in cryogenic deuterium–tritium implosions on OMEGA,” Phys. Plasmas **21** (5), 056315
(2014).
48. P. Michel, _Introduction to Laser-Plasma Interactions_ (Springer Nature Switzerland AG, 2023).
49. M. N. Rosenbluth, “Parametric Instabilities in Inhomogeneous Media,” Phys. Rev. Lett. **29** (9), 565–567 (1972).
50. B. Yaakobi, A. A. Solodov, J. F. Myatt, _et al._, “Measurements of the divergence of fast electrons in laser-irradiated
spherical targets,” Phys. Plasmas **20** (9), 092706 (2013).
51. H. Baldis, E. Campbell, W. Kruer, _et al._, “Handbook of Plasma Physics,” Elsevier Science, New York **19911**, 361–434
(1991).
52. W. L. Kruer, “Intense laser plasma interactions: From Janus to Nova,” Phys. Fluids B **3** (8), 2356–2366 (1991).
53. H. Yoneda, T. Miura, Y. Yokota, _et al._, “Bandwidth effects on laser–plasma interaction with a 1/4-µm laser,” Laser
Part. Beams **11** (1), 15–23 (1993).
54. A. Mostovych, S. Obenschain, J. Gardner, _et al._, “Brillouin scattering measurements from plasmas irradiated with
spatially and temporally incoherent laser light,” Phys. Rev. Lett. **59** (11), 1193–1196 (1987).
55. J. Bates, R. Follett, J. Shaw, _et al._, “Suppressing cross-beam energy transfer with broadband lasers,” High Energy
Density Phys. **36**, 100772 (2020).
56. D. H. Froula, C. Dorrer, A. Colaïtis, _et al._, “A future of inertial confinement fusion without laser-plasma instabilities,”

Phys. Plasmas **32** (5), 052713 (2025).

57. C. Dorrer, E. M. Hill, and J. D. Zuegel, “High-energy parametric amplification of spectrally incoherent broadband
pulses,” Opt. Express **28** (1), 451–471 (2020).
58. C. Dorrer, M. Spilatro, S. Herman, _et al._, “Broadband sum-frequency generation of spectrally incoherent pulses,”

Opt. Express **29** (11), 16135–16152 (2021).
59. E. M. Epperlein, “LLE Review Quarterly Report (October-December 1990), Volume 45,” Tech. rep., Univ. of
Rochester, NY (United States). Laboratory for Laser Energetics (1990).
60. E. Lefebvre, R. L. Berger, A. B. Langdon, _et_ _al._, “Reduction of laser self-focusing in plasma by polarization
smoothing,” Phys. Plasmas **5** (7), 2701–2705 (1998).
61. S. Skupsky and R. S. Craxton, “Irradiation uniformity for high-compression laser-fusion experiments,” Phys. Plasmas

**6** (5), 2157–2163 (1999).
62. T. R. Boehly, V. A. Smalyuk, D. D. Meyerhofer, _et al._, “Reduction of laser imprinting using polarization smoothing
on a solid-state fusion laser,” J. Appl. Phys. **85** (7), 3444–3447 (1999).
63. K. Tsubakimoto, M. Nakatsuka, H. Nakano, _et al._, “Suppression of interference speckles produced by a random
phase plate, using a polarization control plate,” Opt. Commun. **91** (1-2), 9–12 (1992).
64. J. G. Moreau, N. Blanchot, C. Rousseaux, _et al._, “Stimulated Brillouin scattering dependence on polarization state,
speckle shape, and polarization smoothing implementation,” Phys. Plasmas **32** (3), 032102 (2025).
65. S. M. Hamadani, F. Soltanmoradi, M. H. Marvasti, _et al._, “Laser plasmas,” Appl. Phys. B **29** (3), 186–188 (1982).
66. H. A. Rose and D. F. DuBois, “Initial development of ponderomotive filaments in plasma from intense hot spots
produced by a random phase plate,” Phys. Fluids B **5** (9), 3337–3356 (1993).
67. H. A. Rose and D. F. DuBois, “Statistical properties of laser hot spots produced by a random phase plate,” Phys.
Fluids B **5** (2), 590–596 (1993).
68. P. J. Wegner, J. M. Auerbach, C. E. Barker, _et_ _al._, “Frequency converter development for the National Ignition
Facility,” in _Third International Conference on Solid State Lasers for Application to Inertial Confinement Fusion_, vol.
3492 (SPIE, 1999), pp. 392–405.
69. A. Koster, H. Matzner, and D. Nicholsi, “PBMR design for the future,” Nucl. Eng. Des. **222** (2-3), 231–245 (2003).
70. K. Nagatsuka, H. Noguchi, S. Nagasumi, _et al._, “Current status of high temperature gas-cooled reactor development
in Japan,” Nucl. Eng. Des. **425**, 113338 (2024).
71. A. Haught, “Magnetic Field Confinement of Laser Irradiated Solid Particle Plasmas,” in _Laser_ _Interaction_ _and_
_Related Plasma Phenomena:_ _Volume 2 Proceedings of the Second Workshop, held at Rensselaer Polytechnic Institute,_
_Hartford Graduate Center, Hartford, Connecticut, August 30–September 3, 1971_, (Springer, 1972), pp. 289–289.
72. Y. P. Zakharov, A. V. Melekhov, V. G. Posukh, _et al._, “Direct Conversion of the Energy of Laser and Fusion Plasma
Clouds to Electrical Energy During Expansion in a Magnetic Field,” Journal of Applied Mechanics and Technical
Physics **42** (2), 185–195 (2001).
73. J.-M. Rax, E. Kolmes, and N. Fisch, “Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in
Axisymmetric Fields,” PRX Energy **4** (1), 013007 (2025).
74. J. Sethian, A. Raffray, J. Latkowski, _et al._, “Considerations for the chamber first wall material in a laser fusion power
plant,” J. Nucl. Mater **347** (3), 161–177 (2005).
75. M. W. McGeoch and S. P. Obenschain, “Direct Drive Laser Fusion Facility and Pilot Plant,” Journal of Fusion Energy

**43** (2), 23 (2024).
76. S. M. G. De Vicente, N. A. Smith, L. El-Guebaly, _et al._, “Overview on the management of radioactive waste from
fusion facilities: ITER, demonstration machines and power plants,” Nucl. Fusion **62** (8), 085001 (2022).
77. B. Le Garrec, M. Novaro, M. Tyldesley, _et al._, “HiPER laser reference design,” Proc. SPIE **8080**, 80801V-1–80801V-9
(2011).
78. M. Dunne, E. Moses, P. Amendt, _et al._, “Timely delivery of laser inertial fusion energy (LIFE),” Fusion Sci. Technol.

**60** (1), 19–27 (2011).
79. J. F. Latkowski, R. P. Abbott, S. Aceves, _et al._, “Chamber design for the laser inertial fusion energy (LIFE) engine,”

Fusion Sci. Technol. **60** (1), 54–60 (2011).
80. R. Gonzalez-Arrabal, A. Rivera, and J. Perlado, “Limitations for tungsten as plasma facing material in the diverse
scenarios of the European inertial confinement fusion facility HiPER: Current status and new approaches,” Matter
Radiat. Extremes **5** (5), 055201 (2020).
81. T. Johzaki, Y. Nakao, H. Nakashima, _et al._, “Effects of neutron heating on ignition and energy gain of laser-imploded
DT pellets,” Laser Part. Beams **15** (2), 259–276 (1997).
82. H. M. Şahin, G. Tunç, A. Karakoç, _et al._, “Neutronic study on the effect of first wall material thickness on tritium
production and material damage in a fusion reactor,” Nucl. Sci. Tech. **33** (4), 43 (2022).
83. R. Follett, A. Colaïtis, I. Igumenshchev, _et_ _al._, “An experimentally informed design process for future inertial
confinement fusion facilities,” Phys. Plasmas **32** (4), 042705 (2025).

