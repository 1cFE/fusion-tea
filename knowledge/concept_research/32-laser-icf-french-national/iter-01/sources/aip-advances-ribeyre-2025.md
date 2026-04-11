---
source: "perspectives-in-laser-driven-inertial-fusion.pdf"
source_type: "local_file"
extracted_at: "2026-04-04T17:04:18.963233+00:00"
content_hash_sha256: "29715bd3aa2b8c46e661d6a16a0525b058155bfe023a45d99a89c9284acb9601"
backend: "pdf_pipeline"
---

RESEARCH ARTICLE | SEPTEMBER 09 2025
### **Perspectives in laser-driven inertial fusion reactor system**

[X. Ribeyre](javascript:;)  [; H. Chesneau](javascript:;) [; H. Besaucèle; J. Néauport](javascript:;) [; A. Casner](javascript:;)

_AIP Advances_ 15, 095013 (2025)

[https://doi.org/10.1063/5.0266860](https://doi.org/10.1063/5.0266860)

# 

# 

View Export
# Online [] Citation

Export
Citation

![](images/perspectives-in-laser-driven-inertial-fusion.pdf-0-1.png)

![](images/perspectives-in-laser-driven-inertial-fusion.pdf-0-2.png)

## **AIP Advances ARTICLE pubs.aip.org/aip/adv** Perspectives in laser-driven inertial fusion reactor system

Cite as: AIP Advances **15** [, 095013 (2025); doi: 10.1063/5.0266860](https://doi.org/10.1063/5.0266860)
Submitted: 21 February 2025  - Accepted: 18 August 2025  Published Online: 9 September 2025

X. Ribeyre, [1,a)] H. Chesneau, [2] H. Besaucèle, [2] J. Néauport, [1] and A. Casner [1]

AFFILIATIONS

**1** CEA, DAM, CEA-CESTA, F-33114 Le Barp, France

**2** GenF, 2 Avenue Gay Lussac, 78990 Elancourt, France

**a)** Author to whom correspondence should be [addressed: xavier.ribeyre@cea.fr](mailto:xavier.ribeyre@cea.fr)

ABSTRACT

For the first time in any fusion approach, a target gain greater than one was achieved on 5 December 2022 at the National Ignition Facility
using lasers in an indirect drive configuration. This breakthrough has been repeated seven times since, making fusion a possibility rather
than a concept. Inertial fusion for energy production and power plant design is now gaining credibility. In this paper, we present a historical
overview of major discoveries that brought this momentum. We detail the fundamental principles of these reactors, emphasizing the key
challenges and obstacles in their development. We analyze various reactor figures of merit and discuss different hydro-scaled target designs,
exploring different ignition schemes.

© _2025_ _Author(s)._ _All_ _article_ _content,_ _except_ _where_ _otherwise_ _noted,_ _is_ _licensed_ _under_ _a_ _Creative_ _Commons_ _Attribution_ _(CC_ _BY)_ _license_
_(https://creativecommons.org/licenses/by/4.0/)._ [https://doi.org/10.1063/5.0266860](https://doi.org/10.1063/5.0266860)

I. INTRODUCTION

The ignition achieved at the National Ignition Facility (NIF)
in 2022 marks a crucial milestone in advancing fusion energy
research. [1,2] This achievement is the culmination of almost a century of major scientific breakthroughs, from the discovery of light
elements, hydrogen isotopes, the neutron, fusion reactions, and the
invention of the laser. The demonstration of an energy gain greater
than unity has paved the way to the design of inertial fusion energy
(IFE) power plants. [3,4] In recent years, numerous companies around
the world have been working to develop reactor concepts capable of producing energy from fusion reactions. In this landscape,
the CEA and the CNRS have joined their expertise and capabilities
to support the initiative of the GenF company under the Taranis
project. [5] GenF is a new company, a spin-off of Thales, created in
2024 with the support of the French government as part of the
France 2030 plan (2024–2027). In this first stage, a study of a reactor based on the direct drive DT fusion scheme will be performed,
including fusion reaction modeling, laser developments, experimental calibration, and the development of a reactor digital twin. This
research initiative, supported by the French government, underlines the growing momentum in fusion energy development and its
potential to address future energy needs.

This article is organized as follows: In Sec. II, we present an
overview of some of the major historical steps bridging the gap to the
ignition. Section III details a power plant reactor model. Section IV
compares different hydro-scaled target design simulations in the
reactor operation context. In these sections, we try to highlight,
when pertinent, the technological challenges that will have to be
addressed.

II. SHORT FUSION RESEARCH HISTORY

A century ago, Aston, in 1920, discovered isotopes of light elements [6] such as hydrogen and helium using his mass spectroscopy
devices. Shortly after, Eddington understood that helium can be
produced by the fusion of hydrogen nuclei. From the mass difference between the two elements, a large amount of energy can be
released. [7] Eddington had just proposed how nuclear fusion powers stars such as the Sun. Following the early development of the
quantum theory, Gamow made a significant contribution to nuclear
physics. He proposed the idea that the tunnelingeffect could allow us
to obtain nuclei of higher atomic number from proton interactions. [8]
He then explained the alpha particle decay responsible for radioactivity. The field of nuclear physics made rapid progress in the early
1930s. In 1932, the first nuclear transmutation by using artificially

accelerated protons to split lithium nuclei into two alpha particles [9]
was demonstrated. The neutron, discovered by Chadwick, [10] completed the understanding of the basic components of the atomic
nucleus. The first fusion reaction in a laboratory was obtained by
Oliphant [11] from deuterium–deuterium fusion reactions, producing
helium-3 and tritium. After these pioneering first steps, scientists
identified the key nuclear components, demonstrated artificial transmutation, and observed fusion reactions in a laboratory setup. All
the key elements were there to begin research toward fusion energy.
During wartime, classified and unclassified work on
fission–fusion began. However, a major step forward was made,
probably from ideas from Bethe, with the first deuterium–tritium
(DT) fusion cross section measurement. [12–15] The results showed
that the DT fusion cross section is 10–100 times greater than
deuterium–deuterium reactions, leading to a significant interest
in this reaction for fusion research. The research in fusion physics
accelerated during the Second World War with the development of
thermonuclear weapons; [16] it involved numerous brilliant physicists:
Fermi, Bethe, Teller, Ulam, and Neddermeyer for the United States.
A similar effort was conducted in Russia with Zel’dovich, Sakharov,
Tamm, and Popov. Both teams independently concluded that
achieving high-density compression of deuterium–tritium (DT)
fuel was essential to produce fusion energy. During the Cold War
era, despite the intense focus on nuclear weapons development,
many scientists recognized the immense potential of fusion for
peaceful energy production.
One of the foundational studies on thermonuclear reactors
was published by Lawson [17] in 1957. Originating from a classified
report written in 1955, this seminal work, titled “Some Criteria for
a Power Producing Thermonuclear Reactor,” aimed also to alert the
community to the difficulties of producing energy from fusion reactions. This analysis led to the formulation of the Lawson criterion,
which provides a minimum required value for the product of plasma
density and energy confinement time necessary for a net energy production. These results were also based on another important paper
published by Post [18] shortly before in 1956. His work introduced the
concept of a critical plasma temperature, above which the power
generated by fusion reactions exceeds the power lost through radiation. This definition paved the way for controlled fusion research.
However, it was not until 1958 that a significant portion of fusion
research was declassified. Prior to this date, fusion research was
conducted under strict secrecy, with the United States program
code-named “Project Sherwood.” [19] Declassification in 1958 marked
a turning point in fusion research history, allowing open sharing of
information and fostering international collaboration.
The development of fusion energy and laser technology, while
following parallel paths, both stem from the applications of quantum
mechanics and relativity theories to different aspects of physics. As
described before, the idea of a fusion reaction originated from the
study of the properties of matter. Nevertheless, a significant scientific breakthrough emerged from the investigation of the properties
of light. Einstein in 1917 predicted that radiation emission can be
stimulated by light. [20] Maiman applied this idea in 1960 to create the
first solid state laser. [21] This invention opened up numerous applications in fields as diverse as medicine and communications, as well
as opened up the ability to trigger fusion reactions for energy production. In 1964, Basov and Dawson understood that the laser light
properties could concentrate energy in a small volume. From there

was born the idea to use a pulsed laser to drive the implosion of a tiny
bullet of fusible material. It follows the first publication on plasma
heating by laser by Basov and Khrokin [22] and by Dawson, [23] which
opened the way to laser–plasma interaction physics and high energy
density physics.
The first neutron production in laser–matter interaction was
obtained by Basov’s group in 1968 by irradiating a Li–D solid target,
but the neutron signal was weak. [24] We have to wait for the confirmation of the neutron emission from fusion reactions by Floux’s team
at CEA Limeil. [25,26] A clear neutron signal from a fusion reaction was
measured coming from a cryogenic D2 planar target irradiated by
a high power laser. It marked the beginning of a new era in high
energy density physics, opening up the possibility of using powerful
lasers to study nuclear reactions and potential fusion applications.
Information and references of historical interest can be found in
Refs. 27–29.
In the early 1970s, Nuckolls and his colleagues proposed a
groundbreaking approach to fusion energy using high-power lasers,
which laid the foundation for inertial confinement fusion (ICF)
research. Using powerful lasers to implode a spherical target containing DT fuel, [30,31] this work describes in detail a conceptual design
for a DT fusion reactor, the numerical simulations of the imploded
shell, and the predicted high energy gain target. This DT fusion reactor design included (i) multiple high-power laser beams focused on
a spherical target, (ii) a reaction chamber to contain the fusion reactions, and (iii) a wall system designed to capture and convert neutron
energy. This first study concluded that the laser energy needed was
about 100 kJ, which turned out to be very optimistic. However, all
the key elements of an ICF reactor were already there. During the
1970s, the nuclear explosion program Centurion–Halite, classified
underground nuclear tests, demonstrated that the idea proposed
by Nuckolls was indeed feasible [32] and required 1–10 MJ of laser
energy in short wavelength to achieve ignition. From the 1970s to
the present day, the fusion research community has moved from
theoretical concepts to large-scale experiments to achieve controlled
fusion reactions using high-power lasers. [33]

Laser research programs in various countries have led to the
development of advanced high power laser facilities. In the United
States, several generations of laser systems have been built, from
Janus, Argus, Shiva, and Nova to the NIF, [34] culminating in an energy
of 2.2 MJ at 351 nm. [35] A similar path was followed in France at CEA,
with various laser systems located first at CEA Limeil and then at
CEA Cesta near Bordeaux since 2000. [36] Three years after the invention of the laser, a ruby laser called L1 was installed, delivering 25 J
with millisecond pulses (spiking mode), shortly followed by the L2
laser, a Q-switched ruby laser of 7 J, 50 ns pulse duration. The L3
laser was commissioned in 1964, delivering 1 J, 30 ns with either a
ruby laser or an Nd:silicate glass laser. In 1965, the first laser beamline, called L4, started up. It was constituted of an oscillator and
Nd:silicate rod amplifiers to deliver 30 J, 30 ns. [37] While the first
systems were used for laser/gas interaction experiments, their use
has evolved toward laser/solid target experiments. The two beamlines 2 × 120 J, 30 ns Nd:silicate rod L5 laser, were commissioned
in 1967. Nuclear fusion reactions in solid-deuterium laser-produced
plasma were demonstrated on L5 in 1969. [25] This laser system was
followed by the C6 laser, commissioned in 1969 and equipped with a
4 × 100 J, 1.5 ns Nd:silicate rods beamline. [38] The final optic assembly
included aspheric focusing lenses developed in collaboration with

the Institute of Optics (J. P. Marioge, Paris, Orsay) to improve the
focal spot quality on target and promote fusion reactions. [39] Using
C6, the frequency conversion of the fundamental 1053 nm amplified
wavelength to the green (526 nm) with a 30% conversion yield was
demonstrated using KDP crystals from the Quartz et Silice company.
This green light was used to trigger the first “green” neutrons in a
solid-deuterium laser-produced plasma. [40] The P-101 laser, installed
in 1974, delivered 10 J, 100 ps to investigate shorter pulse durations. It combined Nd:silicate rod and slab amplifiers for the first
time. [41] It evolved into P-102 (100 J, 100 ps) in 1976. The P-102 laser
demonstrated the chirped pulse amplification technique for the first
time [42] on a high power laser system in 1991. [43] OCTAL, an 8 beamline 1.6 TW (8 × 10 J at 50 ps) laser, [44] was in operation in 1978.
It was replaced in 1986 by the PHEBUS [45] laser, a 2 × 10 kJ, 1 ns
Nd:phosphate glass NOVA laser [46] replica, and a 1 kJ, 1 ns beamline, all built and installed thanks to a collaboration with the United
States. The work carried out under the direction of Dautray in
France in support of the Inertial Confinement Fusion research and
ICF reactor program (now called IFE, for Inertial Fusion Energy)
should be highlighted. [47] After the PHEBUS laser system came the
MJ-class laser era, with the Laser Megajoule (LMJ). After the operation of a prototype LMJ beamline, the LIL [48] between 2004 and 2014,
and the first light of the LMJ first bundle started in 2014. At present,
the LMJ is in operation with 132 beamlines delivering up to 500 kJ at
351 nm on target. Ongoing efforts continue to commission the last
bundles and ramp up to full energy and power. [49] High power laser
technology for ICF and IFE programs has also been developed all
over the world, in Japan, Russia, and China. [50]

Following the Lawson criterion, [13,17] there are different ways
to achieve the condition to sustain controlled fusion reactions:
magnetic confinement, magneto-inertial fusion and inertial fusion,
magnetic–pinch confinement, and laser confinement. Afterward,
only laser inertial fusion will be considered. In ICF, two main
approaches have been studied: the indirect and the direct drive. In
the indirect-drive approach, x rays generated by laser absorption in
the walls of a high-Z material Hohlraum irradiate a spherical target contained within the cavity. While in the direct-drive, the laser
directly irradiates the target. [3]

Since December 2022, a critical milestone has been achieved
on the NIF (National Ignition Facility). It is the first demonstration,
in the indirect drive scheme, [1,51] of controlled nuclear fusion that
produced more energy than the laser energy focused onto the DT
target. Since then, the NIF has achieved fusion ignition 7 times, with
target gains (ratio of fusion energy to laser energy) ranging from
1.3 to 4 and a laser energy between 1.9 and 2.2 MJ. These successive experiments established NIF’s consistent progress in achieving
and improving fusion ignition conditions. While significant challenges persist for scientists and engineers, this pivotal breakthrough
paves the way for the development of fusion power plants based
on fusion energy. Section III will examine the fundamental components and critical considerations essential for designing a laser fusion
reactor.

III. REACTOR MODEL

Substantial challenges remain before fusion power plants
become a reality. While the NIF demonstrated net energy gain,

two main key factors limit its practical application for power
generation: insufficient fusion energy gain and low shot repetition
rate. To overcome these challenges, researchers must focus on the
following:

  - Increasing the target gain through improved target design
(laser/target/plasma coupling) and laser efficiency.

  - Developing high-repetition-rate driver technologies capable
of sustaining frequent fusion reactions.

  - Addressing engineering challenges related to continuous
operation, such as heat extraction and tritium breeding.

Since the 1970s, many reactor designs have been proposed
based on laser fusion drivers; some pioneers can be cited: Lubin
and Frass, [52] Emmett _et al._, [31] and Basov [53] for the first concepts and
Badger _et al._ [54] for more advanced designs. This list is obviously not
exhaustive. The number of companies focused on fusion reactor
concepts has grown exponentially over the past three decades, [55] particularly since the early 2000s. When there were a few companies in
2000, ∼40 existed in 2023. This significant increase demonstrates the
growing attractiveness and potential of the fusion energy field. Since
the NIF ignition, a major effort has been made to define the key elements to be solved in order to move toward IFE. [56] Figure 1 describes
the general reactor concept. The DT spherical targets are injected
into the center of the chamber, and then multiple laser pulses are
shot onto the target. The target implodes, ignites, and burns the
compressed DT fuel and produces neutrons, ions, and hard x rays
from the nuclear reactions. All the delivered energy is collected by
the blanket. This energy heats coolant, and the steam generated is
converted into electric energy by an alternator to supply the grid. In
addition to power generation, a closed fuel cycle for the supply of tritium and targets is required and will be discussed later. To provide
enough power to the grid, this process needs to be repeated several
times per second. [53]

![](images/page_003_eq_0.png)
We sketch in Fig. 2 a laser fusion reactor model with its essential parameters, allowing the computation of the power delivered
onto the grid. We define the driver efficiency by _ηd_, which is the
ratio between the laser driver energy and the wall-plug energy _Ew_
and the thermal to electricity efficiency _ηth_ . The target gain _G_ is
the ratio between the driver energy _Ed_ and the fusion energy _E f_ .
The blanket gain _Gb_ takes into account the nuclear reactions inside
the chamber wall to amplify the fusion energy [53] (this point will be
detailed further). Finally, _rr_ is the repetition rate of the process.
A part of the recirculated power, _Pe_, _recirc_, called _Pe_, _aux_, is used to
supply energy to auxiliary systems such as pumps, lights, target factory, etc. With all these parameters, the power delivered to the grid,
_Pe_, _grid_ = _Pe_, _th_ - _Pe_, _recirc_, is written as follows:

_Pe_, _grid_ = _ηthGGbEd_ _rr_       - _Ed_ _rr_ / _ηd_       - _Pe_, _aux_ . (1)

It is important to distinguish some key parameters: the engineerexample, considering that the NIF target gain ising gain _Geng_ = _E f_ / _Ew_ = _ηdG_ and the target gain _G_ ∼ _G_ 2, consequently = _E f_ / _Ed_ . For
_G_ electricity is needed, then _eng_ ∼ 10 [−][2] because for 2 MJ of laser energy, more than 400 MJ of _ηd_ = 0.5% due to the flash-lamp pumping
technology used by amplifiers. [57] From the expression (1), the target
gain is written as follows:

## **AIP Advances ARTICLE pubs.aip.org/aip/adv** FIG. 1. Schematic overview of the laser-driven fusion reactor power plant. The targets are injected into the reaction chamber. High-power laser beams ignite the targets,

initiating fusion. A surrounding blanket captures the fusion products and absorbs the heat. The heated blanket transfers the energy to a liquid coolant, generating steam. The
steam drives a turbine-alternator system. The system generates electricity, which is fed into the power grid. The closed fuel cycle (especially for tritium) and target supply
bricks are also displayed. Unburned tritium (among other species) is extracted from the chamber using vacuum pumps. These pumped materials are cleaned (separation
between hydrogen isotopes and other species) and then sent to an isotope separation system before the tritium can be reused to make new targets. The second black
arrow, running from the chamber to the fuel cycle, represents the tritium extracted from the blanket breeder.

## FIG. 2. Laser fusion reactor model. This

model incorporates both the laser driver
efficiency _ηd_ and the thermal cycle efficiency _ηth_ . The target gain is denoted
by _G_, while the blanket gain is represented by _Gb_ . The power delivered to
the electrical grid is expressed as _Pe_, _grid_ .
The repetition rate is denoted _rr_, and the
supply power is _Pe_, _aux_ .

![](images/perspectives-in-laser-driven-inertial-fusion.pdf-4-0.png)

![](images/perspectives-in-laser-driven-inertial-fusion.pdf-4-1.png)

_G_ = 1 [ _[P][e]_ [,] _[grid]_ [ +] _[ P][e]_ [,] _[aux]_
_Gbηth_ _Ed_ _rr_

[1] ]. (2)

_ηd_

_[ P][e]_ [,] _[aux]_ + [1]

_Ed_ _rr_ _η_

In what follows, we consider _ηd_ = 10% an estimation of what
can be achieved with a diode-pumped solid-state laser [58] (DPSSL).
DPSSL can reach a higher gain, but there exists a trade-off between
the beam quality and the efficiency. [59] For example, a laser efficiency of 13% was demonstrated on LUCIA, [60] 13% on Mercury, [61]
and 11.7% on HALNA [62] laser facilities. Then, in an industrial context, a projection of 10% seems realistic. Concerning the thermal to

![](images/page_004_eq_0.png)
This expression shows that for a given _Pe_, _grid_ + _Pe_, _aux_ and repetition
rateincreases, the gain tends to a constant value of 1 _rr_, when _Ed_ decreases, the target gain increases,/ _Gbηthη_ and _d_ . when _Ed_

electrical efficiency _ηth_, the choice of this value is limited by the
Carnot cycle for thermal conversion and by the Rankine cycle (gas
turbine) for thermal to electricity conversion (Ref. 53, p. 227). The
value of _ηth_ depends on the blanket temperature, and this efficiency
can vary between 45% and 55%. More recent values are given for the
LIFE reactor design, which gives the same range. [63,64] Then _ηth_ = 40%
seems a reasonable value.

Figure 3(a) displays the target gain _G_ vs the laser energy _Ed_
_G_ for 1 GWtion _b_ = 1, _Pe_, _aux_ this _e_ =power on the grid. Assuming auxiliary power consump- 0.05parameter _Pe_, _grid_ (typicalis takenvalue;into accountsee Ref. in53)theandmodel,blanketbutgainits

## FIG. 3. (a) Target gain vs the laser energy, for Pe, grid = 1 GW e with rr = 10 Hz,

_ηd_ = 10%, _ηth_ = 40%, _Gb_ = 1, and _Pe_, _aux_ = 0.05 _Pe_, _grid_ . (b) Same function with
_rr_ = 5, 10, 20 Hz, and for each frequency, the driver efficiencies are _ηd_ = 5%
(green curve), 7% (blue curve), and 10% (black curve). Representative target
design specifications: _Ed_ = 3 MJ for _G_ = 120 (black star).

effect is not studied in this work, and for a repetition rate _rr_ = 10 Hz.
It shows that, for a “realistic” target gain, i.e., below 150, the laser
energy needed is greater than 2 MJ. Indeed, for 1 MJ, the target gain
reached 300. However, between 5 and 6 MJ of laser energy, the gain
decreased only by 10%. This shows that there is a trade-off to make.
For low laser energy, the target gain is too high, and for high energy,
the gain variation becomes small. Finding this balance is crucial for
developing economically viable fusion energy systems. It requires
careful optimization of the target design, of the laser parameters, and
of the overall system architecture to maximize performance while
minimizing costs.

Figure 3(b) shows how the target gain is sensitive to the repetition rate and the driver efficiency. The system operates with
a repetition rate ranging from 5 to 20 Hz, while its driver efficiency fluctuates between 5% and 20%. Higher repetition rate and
improved driver efficiency lead to a reduction in the required target gain, which could simplify some aspects of target design and
plasma physics challenges. It is important to highlight that, considering Fig. 3(b), the curves corresponding to grid power of 1 GW _e_,
10, and 20 Hz are equivalent to 500 MW _e_, 5, and 10 Hz, assuming
everything else is constant. This means that, to generate 500 MW _e_
instead of 1 GW _e_, the repetition rate is halved while maintaining the
original target design. Indeed, only the target injection frequency is
adjusted. As shown in Fig. 3(b), it is crucial to note that the repetition
rate is very restrictive compared to the driver efficiency, especially
atget gain increases bylow laser energy. ∼For50% when doubling the repetition rate, whileexample, for _Ed_ = 3 MJ, the required tarit varies by ∼20% when the driver efficiency is doubled for a constant repetition rate. Considering a configuration given in Fig. 3(b)
for 10 Hz andcorresponding _η_ gain _d_ = 7% (blue curve), for laser energyis _G_ ≃ 120. This point is displayed _Ed_ in= 3 MJ, theFig. 3(b)
asAssuminga black thestar.ignitionThe releasedand burningfusion characteristicenergy is _E f_ =time _GEd_ is= 360∼100MJ.ps,
the corresponding fusion power is 3.6 × 10 [18] W = 3.6 EW. To have
a better appreciation of this power, let us compare this power to
the solar power delivered on Earth. Knowing that the Sun’s intensity on the Earth is ∼1 kW/m [2], the total solar power reaching the
Earth is ∼2.6 × 10 [17] W = 0.26 EW. Then, the power released by the
fusion reaction is more than 10 times the solar power illuminating the Earth. Consequently, one of the most important challenges
in inertial fusion energy is to effectively confine and manage this
tremendous power within a controlled environment.
Considering the energy released by the fusion reactions in the
reaction chamber, the fractional output energy split for a typical
direct drive reactor (DT fusion reactions) is 75% in neutrons, 6%
in x rays, and 19% in ions and debris. [13] This estimation was realized for the Sirius reactor [54] and was confirmed within the next study
called Sirius-P. [65] According to a recent study in the context of the
HiPER project, [66,67] the share of each element is as follows: 71% of
neutrons, 1%–2% of x rays, and 27% of ions. For all these configurations, the fractions are quite close. The slight differences could be
due to the presence of a low pressure of xenon gas inside the reaction chamber in the case of the Sirius-P reactor design. One of the
criteria for choosing the chamber radius _R_ is to keep the x-ray flux
below ∼1 J/cm [2] to prevent the chamber’s material vaporization. [68]
Assuming the reactor parameters given above, which led to a fusion
energy of _E f_ = 360 MJ (close to the value cited in Ref. 65), taking the
HiPER design, we will get ∼7 MJ of x rays, then a chamber radius

![](images/perspectives-in-laser-driven-inertial-fusion.pdf-5-0.png)

R∼8 m is needed. The ions’ interaction with the chamber wall of
pure tungsten shows a significant lifetime reduction due to thermal
load and atomistic damage. [67] New materials must be investigated to
reduce this effect; see recent work on tantalum in Ref. 69. This estimate should be further refined to incorporate the effects of ion and
neutron deposition; nevertheless, it provides a reliable approximation of the chamber’s radius. When subjected to an intense neutron
flux, the materials in the chamber undergo changes in structural
and mechanical properties; they can also be activated. It should
be emphasized that the radiation and particle flux significantly elevate the chamber wall temperature, [65,67] with values typically ranging
from 1000 to 3000 K. Furthermore, some reactors employ lowpressure xenon gas within the chamber to reduce the flow of ions
toward the walls. [65]

Another important reactor issue is the fuel mass supply. The
released energy in the DT reaction is 337 MJ/mg; therefore, for
360 MJ of fusion energy, at least 1 mg of DT is needed. Considering a
burn fraction of 25%, only one target needs 4 mg of DT. For a 10 Hz
reactor repetition rate, several kg of DT per day are needed (86 400
targets/day). The deuterium could be extracted from the ocean, 33
mg for one cubic meter. Nevertheless, the process for tritium is considerably more complex. A significant challenge is the instability of
tritium, which decays into helium-3 with a half-life of 12.3 years
and, therefore, needs to be produced. Indeed, the available global
tritium inventory [70] is around 30 kg between 2020 and 2035. The
only commercially available tritium comes from Canada’s CANDU
(CANada Deuterium Uranium) power plants, which produce less
than 2 kg of tritium per year at maximum, [71] while an inertial reactor operating at 10 Hz will consume more than 1 kg of tritium per
day, depending on the target’s fuel composition. Therefore, tritium
breeding and a closed fuel cycle are mandatory in the hope of getting a reactor up and running. Tritium breeding is possible through
neutron irradiation of lithium [53] and could take several forms. [72] The
neutron reaction with Li [6] produces tritium and He, and because this
reaction is exothermic, energy is produced and increases the blanket gain _Gb_ to 1.2 (standard value; see Ref. 53). While the neutron
reaction with Li [7] is endothermic and produces tritium, helium, and
neutrons. Liquid lithium blankets inside the chamber could be used
to produce tritium and energy. If steps forward have been made concerning tritium breeding, much remains to be done. In fact, to be
commercially viable, the tritium breeding ratio, which is the ratio of
tritium produced to tritium consumed, must be greater than unity.
However, to this day, and to the best of our knowledge, the highest
tritium breeding ratio reached [73] with Li [6] or Li [7] is 3.57 × 10 [−][4] . The
United Kingdom has recently initiated a new project concerning this
topic. [74]

The list of IFE challenges is numerous and not exhaustive; other
issues remain concerning target injection, target tracking, cryogenic target fabrication, safety problems, tritium inventory, reaction
chamber material, high repetition multi-beams lasers, focusing systems, etc. For instance, considering the target injection, [75] for an 8 m
reaction chamber radius, the needs are a target in-flight velocity in
a range of 40–160 m/s and enduring acceleration ranging from 100
to 1000 g (where g is the Earth’s gravitational acceleration). Most of
the target design examples presented in Sec. IV consider cryogenic
DT targets. This raises the question of the survivability of the cryogenic target during its injection and under the high temperature wall
chamber. If this problem is not solved, the target gain will eventually

drop. Moreover, the survivability of the final optics with respect to
the neutron radiation flux is crucial for delivering laser energy to the
target (see p. 316 in Ref. 53 and in Ref. 76).
Assuming that the cost model depends mainly on _Pe_, _th_, the thermal to electricity power, an expression for _Pe_, _th_ can be derived from
Eq. (1). This expression, considering _Gb_, _ηth_, _Pe_, _grid_, and _Pe_, _aux_ constant, depends only on the product _ηdG_, which is the engineering
gainand for _GengG_ previously _eng_ - 8 − 10,defined. _Pe_, _th_ becomes _Pe_, _th_ decreasesa constantwithatincreasingthe minimum _Geng_,
value _Pe_, _grid_ + _Pe_, _aux_ . [53] The cost function follows the same trend, so
there is little economic benefit in higher _Geng_ . Then, for instance,
if the desired gain is 120, it is more economically advantageous
to select laser efficiency _ηd_ - 7%. Nevertheless, it is crucial to consider that the power plant cost will increase with the needed laser
energy. As the laser energy demand increases, for example, the volume of laser amplifiers will accordingly expand, leading to higher
overall expenses. In addition, target manufacturing economics must
be carefully evaluated as a critical factor in the overall feasibility
of inertial confinement fusion energy production. A comprehensive global assessment of electricity generation economics requires
in-depth multidisciplinary research.
Section IV highlights the crucial role of a systemic approach in
the reactor design, enabling the identification and implementation
of appropriate scientific solutions.

IV. REACTOR DESIGN AND TARGET GAIN

We established through Eq. (2) the required target gain for
a given driver energy. To go further, it is essential to determine
the target gain based on specific target designs. It can primarily be
performed through numerical simulations or analytical modeling
approaches. It enables the generation of a second category of curves,
_G_ = _f_ ( _Ed_ ), but linked to target design considerations.
Before going any further, some background is useful. The ignition condition can be expressed by Lawson’s criterion, [17] _nτ_ - 2
× 10 [14] s/cm [3] for a plasma temperature of 20 keV, where _n_ is the
plasma density and _τ_ is the plasma lifetime in the hot state. This criterion is a figure of merit that specifies the minimum required value
for the product of plasma density and confinement time needed to
achieve a self-sustaining fusion reaction for a given temperature. Let
us consider an initial DT hotspot plasma of diameter _D_ compressed
_τ_ rionto a diameterand _c_ = _τ_ theis( _D_ rewrittencharacteristic _c_ / _D_ ) _D_, respectively. _c_ at the same temperature. The compressed densityas follows:time scaleThen _ncτ_ are _c_ the∼ written _nτ_ compressed( _D_ / _D_ as _c_ ) [2] _n_ . _c_ This=Lawson’s _n_ ( _D_ final/ _Dc_ )equa- [3] crite-and
tion demonstrates how the hotspot compression facilitates the
achievement of ignition conditions. [77]

Once the DT hotspot ignites, the target energy gain _G_ is proportional to the fraction of mass burned [13] _ρR_ /( _ρR_ + 7) (for a constant
implosion velocity), where _ρR_ is the areal density of the cold DT
fuel assembly in g/cm [2] . To burn 30% of the DT mass, it needs
_ρR_ ∼ 3 g/cm [2] . The greater the _ρR_, the greater the target gain. Power
plant design aims to maximize this value in order to optimize the
electrical output power.
There are different ways to achieve target gain in direct drive
inertial fusion: [78] (i) the standard direct drive implosion, which
ignites a central hotspot; [30,79] (ii) the fast ignition, a method where
the hotspot is created by high energy particles; [80] and (iii) the

shock/shock augmented ignition, in which a strong shock ignites
the compressed fuel assembly hotspot. [81–84] In the following, only
standard and shock/shock augmented ignition will be considered.
Hydrodynamic scaling family targets enable the determination
of target gain as a function of laser energy input. An essential point
of distinction needs to be established for each hydro-scaled target
point. The target (DT mass and diameter), laser pulse shape duration, energy, and focal spot size shall be increased with the scaling
factor. [85,86] In the following, the target gain provided by several works
will be incorporated into the reactor’s figure of merit, as illustrated
in Fig. 3(a). This approach aims to constrain the target design from
the reactor’s operational point of view.
The hydrodynamic scaling curve derived from onedimensional simulations at 3 _ω_ for shock ignition is plotted in
Fig. 4(a) from Ref. 87. Hereafter, 3 _ω_ corresponds to frequency
tripling and 2 _ω_ corresponds to frequency doubling in high-power
laser systems. The capsule aspect ratio (defined as the ratio of
the mean shell radius to the shell thickness) is 2.5. Such thick
targets have good hydrodynamic stability during the implosion
acceleration phase. The selected invariant parameter for the scaling
is the peak areal density (2.5 g/cm [3] ), chosen to maintain the same
burn fraction of approximately ∼30% for all targets. For the shock
ignition scheme, the implosion velocity is quite low (below the
ignition threshold). However, the high intensity pulse during
shock launch initiates laser–plasma instabilities such as stimulated
Brillouin scattering (SBS), stimulated Raman scattering (SRS), and
two-plasmon decay (TPD). In particular, SRS and TPD can generate
suprathermal electrons, which preheat the precompressed fuel. [78]
This effect is not taken into account in these simulations. This curve
intersects the reactor target gain given on the previous Fig. 3(b)
for different laser energies, which defines several points. The curve
shows that for 10 Hz, at least 2 MJ of laser energy is needed. While
at 5 Hz, the required laser energy increases to 3 MJ.
Another hydro scaling, detailed in Ref. 88, compares shockignited targets with blue (3 _ω_ ) and green light (2 _ω_ ). These results
come from one dimensional simulations. The design is based on the
HiPER target. To keep the LPI level low (even if LPI was not taken
into account in the simulations), scaling the target from a constant
_Iλ_ [2] allows us to plot the hydro-scaled target gain at 2 _ω_ . Figure 4(b)
shows that for 10 Hz at 3 _ω_, ∼1.5 MJ seems sufficient, and ∼2.3 MJ
at 5 Hz. At 2 _ω_, at 10 Hz, a laser energy of about ∼2 MJ is needed,
and ∼3 MJ at 5 Hz. The gain curves in Figs. 4(a) and 4(b) differ due
to different constraints used in the modeling (such as the invariant
parameter selected for hydro-scaled targets). From the reactor system point of view, these results show that the 2 _ω_ scaling needs to be
considered as a serious option. However, the point at 20 Hz (at 2 _ω_ )
is too close to the ignition threshold to be considered as robust. An
interesting review about the effect of the wavelength in ICF can be
found in Ref. 89 from the laser–plasma interaction point of view.
Concerning the low gain part (just above the ignition threshold),
when the gain curve decreases rapidly, Fig. 4(b) shows that at 3 _ω_,
_Ed_ has to be less than ∼500 kJ, while at least 2 _ω_, 1.5 MJ is required (3
times higher), because of lower laser absorption and lower ablation
pressure. This gap is less important when considering the reactor
point operation for higher laser energies.
More recent models of target gain scaling are available in
Ref. 90. In this work, target gain scaling based on a constant implosion velocity is given for different laser wavelengths and focal spot

![](images/perspectives-in-laser-driven-inertial-fusion.pdf-7-0.png)
## FIG. 4. (a) Target gain as a function of laser energy, based on scaling models from

Ref. 87 (growing black curve), superimposed on Fig. 4(b). (b) Target gain vs the
laser energy from target scaling coming from Ref. 88. Hydro-scaled target gain
curve at 3 _ω_ (blue diamonds) and at 2 _ω_ (green squares).

zooming with excimer lasers (ArF 193 nm wavelength and KrF
248 nm wavelength). Figure 5(a) shows a part of the results from
Ref. 90, considering only two laser wavelengths, 248 nm (KrF) and
351 nm (3 _ω_ ), for standard or shock ignited DT fuel implosion for
an initial target aspect ratio of 3.74 (ratio between target radius and
thickness). These results were obtained with one dimensional hydrodynamic simulations in which zooming is taken into account (the
laser spot size decreases during implosion). The target gain is higher
at 248 nm than at 351 nm because of higher laser absorption and
higher ablation pressure. Figure 5(a) shows that all the scaled points
are on the cliff of the reactor gain region. At 10 Hz and for a wavelength of 248 nm, the shock ignition needs at least ∼1 MJ, when

Finally, Fig. 5(b) shows the hydro-scaled target design extracted
from Table II in Ref. 91; the target aspect-ratio is kept constant for
an energy greater than 1.3 MJ. In the cited reference, 3D hydrodynamic simulations at 3 _ω_ are performed to compare the target gain
obtained with the standard ignition scheme and the shock/shock
augmented ignition. The simulations took into account the crossbeam energy transfer. One may note that shock ignition [81,82] is used
for a laser energy of about 0.5 MJ, while the shock augmented
ignition [84] scheme is preferred for greater laser energy (see Fig. 3
in Ref. 91). Figure 5(b) highlights that the shock augmented ignition design needs at least ∼2 MJ laser energy at 10 Hz and ∼3 MJ
energy at 5 Hz. While for standard ignition, ∼3 MJ and ∼4 MJ are,
respectively, needed at 10 and 5 Hz. At higher laser energy, the
two ignition schemes lead to approximately the same target gain.
Consequently, at high laser energy, the differences between the two
ignition approaches (standard and shock augmented) are not so significant with respect to the reactor’s operating points. The threshold
gain is achieved for energies lower than ≈500 kJ.
Considering laser energy _Ed_ = 3 MJ [see point Fig. 3(a)] from
a solid state laser driver frequency converted at 351 nm perspective
and taking into account a chamber radius of 8 m (LMJ is 5 m), with
a limit laser fluence of ∼4 J/cm [2] . This fluence at 351 nm is under
the damage growth threshold [92] of fused silica of ∼5 J/cm [2] . Considering the scaled total beam surface from LMJ conditions, i.e., 240
LMJ beams with size 35 × 35 cm [2] and 5 m chamber diameter, the
scaledfor _Ed_ =fluence 3 MJ, is _F_ ∼written4 J/cmas [2] canfollows:be achieved. _F_ = (5/8Such) [2] _Ed_ /an240operating/35/35; then,fluence is likely to suppress optics maintenance, as is experienced on
current MJ-class laser systems. [49,93,94]

![](images/perspectives-in-laser-driven-inertial-fusion.pdf-8-0.png)
## FIG. 5. (a) Target gain vs laser energy from target scaling derived from Ref. 90

superimposed on Fig. 4(b). At 248 nm (KrF), blue circles are for shock ignition and
blue diamonds are for standard hotspot ignition. At 3 _ω_ (351 nm), red circles are
for shock ignition and red diamonds are for standard hotspot ignition. (b) Target
gain vs laser energy from target scaling is coming from Ref. 91. Hydro-scaled
target gain curve at 3 _ω_ for shock/shock augmented ignition (green diamonds),
and standard hotspot ignition (blue diamonds).

∼1.6 MJ is needed for standard ignition. At the same laser repetition rate at 351 nm, the shock ignited target needs at least ∼1.5 MJ,
when ∼1.8 MJ is needed for standard ignition. From the reactor’s
operational point of view, the laser wavelength variation and ignition scheme are not so crucial. Concerning the low gain part, i.e.,
the gain cliff, it is less than 1 MJ for all the configurations, from
less than ∼500 kJ at 248 nm in the shock ignition scheme to less
than ∼1 MJ at 351 nm for the standard ignition scheme. In the gain
cliff region (low laser energy), the gain value uncertainty under laser
energy variations is greater than at high laser energy.

The results presented in this section show that the optimization of hydro-scaled target gain needs to be done with regard to
the design of the reactor’s operating points. A laser system with
a greater wavelength than 3 _ω_ needs to be investigated experimentally. Such a system could be beneficial for a reactor due to a greater
laser wall-plug efficiency and a higher optical component damage
threshold. At lower wavelengths than 351 nm, the operation is not
so robust, and short wavelengths are problematic for laser damage
to optics. [56,95] Moreover, the difference between shock/shock augmented ignition and hotspot (standard) reactor point design does
not seem so crucial, as at high laser energy, they tend to the same
target gain. However, shock ignition allows us to decrease the laser
energy required for a reactor. The physics governing laser–plasma
interactions during the initiation of the ignition spike remains a subject of ongoing research for all wavelengths. A trade-off needs to be
found to optimize the reactor point design. [96]

All the target gain curves presented above require significant
R & D efforts and experimental validations. Concerning shock ignition and shock augmented experimental ignition, validation needs
to be investigated concerning LPI, hot electron generation, etc.
Research and development needs to done concerning laser driven
architecture, reducing the cost of diodes, increasing the optical damage threshold, laser broadband bandwidth to mitigate LPI, smoothing techniques, etc. Many experiments and R & D have been done at
the 351 nm wavelength, but efforts need to be made at other wavelengths. For example, concerning the KrF laser, kJ level energy has
been achieved, but for reactor operation, several 100-kJ or MJ scale
lasers need to be demonstrated. [96] Many aspects of the R & D needed
have been listed in Ref. 56.

V. CONCLUSION

Placing recent IFE advances within a historical framework
underscores the remarkable progress achieved, a century of scientific
endeavor that spans from the initial discovery of nuclear fusion to
the groundbreaking ignition at the National Ignition Facility (NIF).
This study of a reactor system allows us to raise the main unanswered questions to be addressed. The reactor model allows us to
constrain the target design and shows the interest of studying the
reactor system as such. This model shows that for a 1 GW _e_ reactor operation point, repetition rate is an important parameter. For
the parameters chosen in this study, a laser energy greater than
3 MJ, with a repetition rate greater than 5 Hz, allows us to expect
a target gain lower than 200. Then, based on this reactor figure of
merit, the hydro-scaled target gain derived from numerical simulations is constrained. The selection of the ignition scheme (standard,
shock/shock augmented) and laser wavelength remains an open
question. It has to be considered also with respect to the reactor
operation context.
Concerning low target gain, i.e., near the ignition threshold
simulations, for laser wavelengths below 351 nm (3 _ω_ ), a laser ranging from 500 kJ to 1 MJ is needed. However, at 532 nm (2 _ω_ ), 1.5 MJ
of laser energy is required. To make further progress, more sophisticated reactor models are needed, and three-dimensional numerical
simulations will be instrumental in identifying more realistic reactor point designs. This study shows the importance of comparing
scaled-target designs in the reactor operation points framework.

ACKNOWLEDGMENTS

This project was supported by the French government as part
of France 2030 (AAP Réacteurs Nucléaires Innovants—Grant No.
DOS0237680/00). The authors acknowledge N. Bonod for the useful
comments and discussions. We would like to dedicate this work to
the memory of R. Dautray (1928–2023).

AUTHOR DECLARATIONS

Conflict of Interest

The authors have no conflicts to disclose.

DATA AVAILABILITY

The data that support the findings of this study are available
from the corresponding author upon reasonable request.

REFERENCES

1H. Abu-Shawareb, R. Acree, P. Adams, J. Adams, B. Addis, R. Aden, P. Adrian,
B. B. Afeyan, M. Aggleton, L. Aghaian _et_ _al._, “Achievement of target gain larger
[than unity in an inertial fusion experiment,” Phys. Rev. Lett.](https://doi.org/10.1103/physrevlett.132.065102) **132**, 065102 (2024).
2
O. A. Hurricane, “How ignition and target gain - 1 were achieved in inertial
[fusion,” High Energy Density Phys.](https://doi.org/10.1016/j.hedp.2024.101157) **53**, 101157 (2024).
[3S. Atzeni and D. Callahan, “Harnessing energy from laser fusion,” Phys. Today](https://doi.org/10.1063/pt.zghg.fite)
**77** (8), 44–50 (2024).
4D. A. Callahan, “A prospectus on laser-driven inertial fusion as an energy
[source,” Phys. Plasmas](https://doi.org/10.1063/5.0232701) **31**, 120601 (2024).
5H. Besaucèle, “Inertial confinement fusion: A path to carbon-free energy?,”
[Photoniques Rev.](https://doi.org/10.1051/photon/202412850) **128**, 39 (2024).
[6F. W. Aston, “The mass-spectra of chemical elements,” London Edinburgh Phi-](https://doi.org/10.1080/14786440508636074)
los. [Mag.](https://doi.org/10.1080/14786440508636074) J. Sci. **39**, 611 (1920); “Isotopes and atomic weights,” [Nature](https://doi.org/10.1038/107334a0) **107**, 334
(1921).

[7A. S. Eddington, “The internal constitution of stars,” Science](https://doi.org/10.1126/science.52.1341.233) **52**, 233 (1920).
[8G. Gamow, “Zur Quantentheorie des Atomkernes,” Z. Phys.](https://doi.org/10.1007/bf01343196) **51**, 204–212 (1928).
9J. D. Cockcroft and E. T. S. Walton, “Experiments with high velocity positive
[ions,” Proc. R. Soc. London, Ser. A](https://doi.org/10.1098/rspa.1932.0133) **137** (831), 229 (1932).
10J. Chadwick, “The existence of a neutron,” Proc. R. Soc. [London,](https://doi.org/10.1098/rspa.1932.0112) Ser. A
**136** (830), 692 (1932).
11M. L. Oliphant, P. Harteck, and Rutherford, “Transmutation effects observed
[with heavy hydrogen,” Nature](https://doi.org/10.1038/133413a0) **133**, 413 (1934).
12M. B. Chadwick and B. C. Reed, “Introduction to special issue on the early
[history of nuclear fusion,” Fusion Sci. Technol.](https://doi.org/10.1080/15361055.2024.2346868) **80**, 3 (2024).
13S. Atzeni and J. Meyer-Ter-Vehn, _The_ _Physics_ _of_ _Inertial_ _Fusion:_ _Beam_
_Plasma_ _Interaction,_ _Hydrodynamics,_ _Hot_ _Dense_ _Matter_, _International_ _Series_ _of_
_Monographs on Physics Vol. 125_ (Clarendon Press-Oxford, 2004).
14B. C. Diven, J. H. Manley, and R. F. Taschek, “Nuclear data—The numbers
needed to design the bombs,” Los Alamos Sci. **23** (28), 114 (1983).
[15G. Gamow and E. Teller, “The rate of selective thermonuclear reactions,” Phys.](https://doi.org/10.1103/physrev.53.608)
[Rev.](https://doi.org/10.1103/physrev.53.608) **53**, 608 (1938).
16G. A. Goncharov, “American and Soviet H-bomb development programmes:
[Historical background,” Phys.-Usp.](https://doi.org/10.1070/pu1996v039n10abeh000174) **39** (10), 1033 (1996).
17J. D. Lawson, “Some criteria for a power producing thermonuclear reactor,”
[Proc. Phys. Soc. B](https://doi.org/10.1088/0370-1301/70/1/303) **70** (1), 6 (1957).
18R. F. Post, “Controlled fusion research—an application of the physics of high
[temperature plasmas,” Rev. Mod. Phys.](https://doi.org/10.1103/revmodphys.28.338) **28** (3), 338–362 (1956).
19A. S. Bishop, Project sherwood: The US program in controlled fusion, 1958.
20A. Einstein, “On the quantum theory of radiation,” Phys. Z. **18**, 121–128 (1917).
21T. H. Maiman, “Stimulated optical radiation in ruby,” [Nature](https://doi.org/10.1038/187493a0) **187**, 493–494
(1960).
22N. Basov and O. N. Khrokin, “Condition for heating up of a plasma by the
irradiating from an optical generator,” Sov. Phys. JETP **19**, 1 (1964).
[23J. M. Dawson, “On the production of plasma by giant pulse lasers,” Phys. Fluids](https://doi.org/10.1063/1.1711346)
**7**, 981–987 (1964).
24N. G. Basov, P. Kriukov, S. Zakharov, Y. Senatsky, and S. Tchekalin, in _IQE-_
_Conference Miami_ (1968); “Experiments on the observation of neutron emission
at a focus of high-power laser radiation on a lithium deuteride surface,” [IEEE](https://doi.org/10.1109/JQE.1968.1074981) J.
[Quantum Electron.](https://doi.org/10.1109/JQE.1968.1074981) **4** (11), 864 (1968).
25F. Floux, D. Cognard, L. G. Denoeud, G. Piar, D. Parisot, J. L. Bobin, F.
Delobeau, and C. Fauquignon, “Nuclear fusion reactions in solid-deuterium
[laser-produced plasma,” Phys. Rev. A](https://doi.org/10.1103/physreva.1.821) **1** (3), 821 (1970).
26J. L. Bobin, “Il y a cinquante ans: les premières réactions de fusion nucléaire
[induites par laser,” Reflets Phys.](https://doi.org/10.1051/refdp/202067021) **67**, 21 (2020).
27N. Carpintero-Santamaría and G. Velarde, “The pioneers’ legacy of inertial
[confinement nuclear fusion,” Prog. Nucl. Energy](https://doi.org/10.1016/j.pnucene.2013.10.019) **78**, 349–354 (2015).
28G. Velarde, “Academician Nikolai G. Basov: The Father of inertial fusion. A
[scientific and human approach,” Quantum Electron.](https://doi.org/10.1070/qe2002v032n12abeh002346) **32** (12), 1038–1040 (2002).
29J. L. Bobin, _Insaisissable Graal_ (EPD Science, 2023).
30J. Nuckolls, L. Wood, A. Tiessen, and G. Zimmerman, “Laser compression of
[matter to super-high densities: Thermonuclear (CTR) applications,” Nature](https://doi.org/10.1038/239139a0) **239**,
139–142 (1972).
[31J. L. Emmett, J. Nuckolls, and L. Wood, “Fusion power by laser implosion,” Sci.](https://doi.org/10.1038/scientificamerican0674-24)
[Am.](https://doi.org/10.1038/scientificamerican0674-24) **230** (6), 24–37 (1974).
[32M. Crawford, “Underground tests used in laser fusion effort,” Science](https://doi.org/10.1126/science.233.4770.1256) **233**, 1256
(1986).
[33K. A. Brueckner and S. Jorna, “Laser-driven fusion,” Rev. Mod. Phys.](https://doi.org/10.1103/revmodphys.46.325) **46** (2), 325
(1974).
34M. Dunne, “NIF bringing star power on Earth,” in _Annual_ _Graduate_ _Student_
_Symposium_ (Michigan University, 2013).
35K. Budil, A. C. Askin, S. T. Storar, C. N. Meissner, A. Chen, and E. Jaffe,
“Science & technology review: Laser program celebrates 50 years,” Report
No. LLNL-TR-52000; 1055674, Lawrence Livermore National Laboratory, 2022,
[https://www.osti.gov/biblio/1960485.](https://www.osti.gov/biblio/1960485)
36J. L. Bobin, _Fusion Thermonucléaire Contrôlée_ (EDP sciences, 2011).
37P. Veyrie, “Contribution to the study of the ionization and heating of gases by
[laser radiation,” J. Phys.](https://doi.org/10.1051/jphys:0196800290103300) **29**, 1 (1968).

38D. Billon, P. A. Holstein, J. Launspach, C. Patou, J. M. Reisse, and D. Schirmann,
“Laser driven implosion experiments at limeil,” in _Laser Interaction and Related_
_Plasma Phenomena_ (Springer, 1977), Vol. 4A.
[39J. De Metz, “Optical design of a laser system for nuclear fusion research,” Appl.](https://doi.org/10.1364/ao.10.001609)
[Opt.](https://doi.org/10.1364/ao.10.001609) **10** (7), 1609–1614 (1971).
40A. Carion, J. Lancelot, J. De Metz, and A. Saleres, “Fusion reactions in a plasma
[created by the second harmonic of a Nd glass laser,” Phys. Lett. A](https://doi.org/10.1016/0375-9601(73)90698-1) **45** (6), 439–440
(1973).
41J. P. Babuel-Peyrissac and J. P. Watteau, Laser Fusion Research at the Centre
D’Etudes De Limeil, France, Technical Document issued by IAEA, Vienna, 1976,
p. 27.
42D. Strickland and G. Mourou, “Compression of amplified chirped optical
[pulses,” Opt. Commun.](https://doi.org/10.1016/0030-4018(85)90151-8) **55** (6), 447–449 (1985).
43C. Sauteret, D. Husson, G. Thiell, S. Seznec, S. Gary, A. Migus, and G. Mourou,
“Generation of 20-TW pulses of picosecond duration using chirped-pulse
[amplification in a Nd:glass power chain,” Opt. Lett.](https://doi.org/10.1364/OL.16.000238) **16**, 238–240 (1991).
44R. Dautray, F. Delobeau, J. M. Reisse, and J. P. Watteau, “Works on laser-matter
interaction at the Centre d’Etudes de Limeil,” J. [Phys.](https://doi.org/10.1051/jphyscol:1978143) (Paris) **39**, 218 (1978),
Colloq. C1 supplément au no 5, Tome.
45N. A. Fleurot, M. L. Andre, P. Estraillier, D. Friart, C. Gouédard, C. Rouyer, J.
P. Thebault, G. Thiell, and D. Veron, “Output pulse and energy capabilities of the
[PHEBUS laser facility,” Proc. SPIE](https://doi.org/10.1117/12.46898) **1502**, 230–241 (1991).
46J. T. Hunt and D. R. Speck, “Present and future performance of the Nova laser
[system,” Opt. Eng.](https://doi.org/10.1117/12.7976974) **28** (4), 284461 (1989).
47R. Dautray and J. P. Watteau, _La_ _Fusion_ _Thermonucléaire_ _Inertielle_ _Par_ _Laser_,
CEA éd. (Eyrolles, 1991).
48X. Julien, A. Adolf, E. Bar, V. Beau, E. Bordenave, T. Chiès, R. Courchinoux,
J. M. Di-Nicola, C. Féral, P. Gendeau _et al._ [, “LIL laser performance status,” Proc.](https://doi.org/10.1117/12.874466)
[SPIE](https://doi.org/10.1117/12.874466) **7916**, 791610 (2011).
49J. Néauport, J. Ph. Airiau, N. Beck, N. Belon, E. Bordenave, S. Bouillet,
M. Chanal, C. Chappuis, H. Coic, R. Courchinoux _et_ _al._, “Laser megajoule
[performance status,” Appl. Opt.](https://doi.org/10.1364/AO.520482) **63**, 4447–4464 (2024).
50S. Jacquemot, “Inertial confinement fusion for energy: Overview of the ongoing
[experimental, theoretical and numerical studies,” Nucl. Fusion](https://doi.org/10.1088/1741-4326/aa6d2d) **57**, 102024 (2017).
51T. Ma, “Burning plasma and ignition threshold on NIF, and what it means for
aggressive IFE development,” ARPA-E Workshop, 2022, see [https://lasers.](https://lasers.llnl.gov/news/fusion-ignition-and-the-path-to-inertial-fusion-energy)
[llnl.gov/news/fusion-ignition-and-the-path-to-inertial-fusion-energy.](https://lasers.llnl.gov/news/fusion-ignition-and-the-path-to-inertial-fusion-energy)
52M. J. Lubin and A. P. Frass, “Fusion by laser,” Sci. Am. **224** (6), 21–33 (1971).
53W. J. Hogan, J. Coutant, S. Nakai, V. R. Rosanov, and G. Velarde, _Energy from_
_Inertial Fusion_ (IAEA Vienna, 1995), ISBN: 92-0-100794-9.
54B. Badger, H. M. Attaya, T. J. Bartel, M. L. Corradini, R. L. Engelstad, G. L.
Kulcinski, E. G. Lovell, G. A. Moses, R. R. Peterson, M. E. Sawan _et_ _al._, _Pre-_
_liminary_ _Conceptual_ _Design_ _of_ _Sirius,_ _A_ _Symmetric_ _Illumination,_ _Direct_ _Drive_
_Laser_ _Fusion_ _Reactor_ (UMFDM-568 Fusion Technology Institute University of
Wisconsin, Madison, Wisconsin, 1984).
[55Fusion industry association, see https://www.fusionindustryassociation.org for](https://www.fusionindustryassociation.org)
The global fusion industry, 2023.
56Basics Research Needs, US DOE report, 2022.
57M. A. Newton, E. S. Fulkerson, S. D. Hulsey, R. E. Kamm, D. L. Pendleton, D. E.
Petersen, C. R. Smith, G. T. Ullery, P. F. McKay, W. B. Moore, and D. A. Muirhead,
“Overview and status of the power conditioning system for the national ignition facility,” in _Pulse Power Plasma Science Conference Las Vegas_ (LLNL, 2001),
UCRL-JC-142112.
58B. Le Garrec, “Challenges of high power diode-pumped lasers for fusion
[energy,” High Power Laser Sci. Eng.](https://doi.org/10.1017/hpl.2014.33) **2** (7), e28 (2014).
59B. Le Garrec and D. Dumitras, “Laser-diode and flash lamp pumped solid-state
[lasers,” AIP Conf. Proc.](https://doi.org/10.1063/1.3426039) **1228**, 111 (2010).
60T. Gonçalvès-Novo, D. Albach, B. Vincent, M. Arzakantsyan, and J.-C.
Chanteloup, “14 J / 2 Hz Yb [3][+] [:YAG diode pumped solid state laser chain,” Opt.](https://doi.org/10.1364/OE.21.000855)
[Express](https://doi.org/10.1364/OE.21.000855) **21** (1), 855–866 (2013).
61A. Bayramian, P. Armstrong, E. Ault, R. Beach, C. Bibeau, J. Caird, R. Campbell,
B. Chai, J. Dawson, C. Ebbers _et al._, “The mercury project: A high average power,
[gas-cooled laser for inertial fusion energy development,” Fusion Sci. Technol.](https://doi.org/10.13182/fst07-a1517) **52**,
383–387 (2007).

62R. Yasuhara, T. Kawashima, T. Sekine, T. Kurita, T. Ikegawa, O. Matsumoto,
M. Miyamoto, H. Kan, H. Yoshida, J. Kawanaka _et al._, “213 W average power of
24 GW pulsed thermally controlled Nd:glass zigzag slab laser with a stimulated
[brillouin scattering mirror,” Opt. Lett.](https://doi.org/10.1364/ol.33.001711) **33** (15), 1711–1713 (2008).
63W. R. Meier, A. M. Dunne, K. J. Kramer, S. Reyes, T. M. Anklam, and LIFE
[Team, “Fusion technology aspects of laser inertial fusion energy (LIFE),” Fusion](https://doi.org/10.1016/j.fusengdes.2013.12.021)
[Eng. Des.](https://doi.org/10.1016/j.fusengdes.2013.12.021) **89**, 2489–2492 (2014).
64M. Dunne, T. Anklam, and W. Meier, “Inertial confinement fusion power
[plants,” Encycl. Nucl. Energy](https://doi.org/10.1016/b978-0-12-819725-7.00170-7) **2021**, 807–821.
65I. N. Sviatoslavsky, G. L. Kulcinski, G. A. Moses, R. L. Engelstad, H. Y. Khater, E.
M. Larsen, E. G. Lovell, J. J. MacFarlane, E. A. Mogahed, R. R. Peterson, Sirius-P
_et al._, An Inertial Confined Direct Drive Laser Fusion Power Reactor UMFDM950, Fusion Technology Institute University of Wisconsin, Madison, Wisconsin,
1993.
66J. Alvarez, D. Garoz, R. Gonzalez-Arrabal, A. Rivera, and M. Perlado, “The role
of spatial and temporal radiation deposition in inertial fusion chambers: The case
[of HiPER,” Nucl. Fusion](https://doi.org/10.1088/0029-5515/51/5/053019) **51**, 053019 (2011).
67R. Gonzalez-Arrabal, A. Rivera, and J. M. Perlado, “Limitations for tungsten as
plasma facing material in the diverse scenarios of the European inertial confine[ment fusion facility HiPER: Current status and new approaches,” Matter Radiat.](https://doi.org/10.1063/5.0010954)
[Extremes](https://doi.org/10.1063/5.0010954) **5**, 055201 (2020).
68T. J. Renk, C. L. Olson, T. J. Tanaka, M. A. Ulrickson, G. A. Rochau, R. R. Peterson, I. E. Golovkin, M. O. Thompson, T. R. Knowles, A. R. Raffray, and M. S.
Tillack, “IFE chamber dry wall materials response to pulsed X-rays and ions at
[power-plant level fluences,” Fusion Eng. Des.](https://doi.org/10.1016/s0920-3796(03)00009-7) **65** (3), 399–406 (2003).
69M. Ialovega, M. Xavier Navarro-Gonzalez, R. Bisson, J. Anderson, T. Angot, T.
Dabney, C. Forest, A. Kreter, D. Velez, E. Willing, H. Yeom, K. Sridharan, and O.
Schmitz, “Deuterium retention in cold spray tantalum coatings vs. polycrystalline
[tungsten and tantalum,” Nucl. Fusion](https://doi.org/10.1088/1741-4326/ade4d7) **65**, 076042 (2025).
70R. J. Pearson, A. B. Antoniazzi, and W. J. Nuttall, “Tritium supply and use: A
key issue for the development of nuclear fusion energy,” Fusion [Eng.](https://doi.org/10.1016/j.fusengdes.2018.04.090) Des. **136**,
1140–1148 (2018).
71M. Kovari, M. Coleman, I. Cristescu, and R. Smith, “Tritium resources available
[for fusion reactors,” Nucl. Fusion](https://doi.org/10.1088/1741-4326/aa9d25) **58**, 026010 (2018).
72D. W. S. Clark, B. Goh, S. Ramirez, E. Pflug, J. Smandych, J. R. Kessing, C.
Moreno, T. D. Bohm, P. P. H. Wilson, L. Singh, A. Cerfon, N. R. Mandell, J. C.
Schmitt, W. Guttenfelder, C. Lau, M. S. Tillack, and J. M. Canik, “Breeder blanket
[and tritium fuel cycle feasibility of the infinity two fusion pilot plant,” J. Plasma](https://doi.org/10.1017/s002237782500039x)
[Phys.](https://doi.org/10.1017/s002237782500039x) **91** (3), E86 (2025).
73R. Delaporte-Mathurin, R. Chochoy, J. Mougenot, Y. Charles, E. A. Hodille, and
C. Grisola, “3D effects on hydrogen transport in ITER-like monoblocks,” [Nucl.](https://doi.org/10.1088/1741-4326/ad1019)
[Fusion](https://doi.org/10.1088/1741-4326/ad1019) **64**, 026003 (2024).
74See UK Atomic Energy Authority for information about : Multi-milion pound
investment to fast-track fusion fuel development (2025).
75J. P. Perin, “Cryogenic systems for LMJ cryotarget and HiPER application,”
[Laser Part. Beams](https://doi.org/10.1017/s0263034610000091) **28** (1), 203–208 (2010).
76M. E. Sawan, A. Ibrahim, T. D. Bohm, and P. P. H. Wilson, “Three-dimensional
nuclear analysis of the final optics of a laser driven fusion power plant,” [Fusion](https://doi.org/10.1016/j.fusengdes.2008.04.004)
[Eng. Des.](https://doi.org/10.1016/j.fusengdes.2008.04.004) **83**, 1879–1883 (2008).
77O. N. Krokhin, IAEA Conference, Basics of Laser Fusion, Lebedev Institute,
2013.
78R. S. Craxton, K. S. Anderson, T. R. Boehly, V. N. Goncharov, D. R. Harding,
J. P. Knauer, R. L. McCrory, P. W. McKenty, D. D. Meyerhofer, J. F. Myatt _et al._,
“Direct-drive inertial confinement fusion: A review,” Phys. [Plasmas](https://doi.org/10.1063/1.4934714) **22**, 110501
(2015).
79J. Lindl, “Development of the indirect-drive approach to inertial confinement
fusion and the target physics basis for ignition and gain,” Phys. [Plasmas](https://doi.org/10.1063/1.871025) **2** (11),
3933 (1995).
80M. Tabak, J. Hammer, M. E. Glinsky, W. L. Kruer, S. C. Wilks, J. Woodworth,
E. M. Campbell, M. D. Perry, and R. J. Mason, “Ignition and high gain with
[ultrapowerful lasers,” Phys. Plasmas](https://doi.org/10.1063/1.870664) **1** (5), 1626 (1994).
81V. A. Shcherbakov, “Ignition of a laser-fusion target by a focusing shock wave,”
Sov. J. Plasma Phys. **9** (2), 240 (1983).
82R. Betti, C. D. Zhou, K. S. Anderson, L. J. Perkins, W. Theobald, and A. A.
[Solodov, “Shock ignition of thermonuclear fuel with high areal density,” Phys. Rev.](https://doi.org/10.1103/physrevlett.98.155001)
[Lett.](https://doi.org/10.1103/physrevlett.98.155001) **98** (15), 155001 (2007).

83S. Atzeni, X. Ribeyre, G. Schurtz, A. J. Schmitt, B. Canaud, R. Betti, and L. J.
[Perkins, “Shock ignition of thermonuclear fuel: Principles and modelling,” Nucl.](https://doi.org/10.1088/0029-5515/54/5/054008)
[Fusion](https://doi.org/10.1088/0029-5515/54/5/054008) **54**, 054008 (2014).
84R. H. H. Scott, D. Barlow, W. Trickey, A. Ruocco, K. Glize, L. Antonelli, M.
Khan, and N. C. Woolsey, “Shock-augmented ignition approach to laser inertial
[fusion,” Phys. Rev. Lett.](https://doi.org/10.1103/physrevlett.129.195001) **129**, 195001 (2022).
85C. D. Zhou and R. Betti, “Hydrodynamic relations for direct-drive fast-ignition
and conventional inertial confinement fusion implosions,” Phys. [Plasmas](https://doi.org/10.1063/1.2746812) **14** (7),
072703 (2007).
86S. Atzeni, A. Marocchino, A. Schiavi, and G. Schurtz, “Energy and wavelength
[scaling of shock-ignited inertial fusion targets,” New J. Phys.](https://doi.org/10.1088/1367-2630/15/4/045004) **15**, 045004 (2013).
87L. J. Perkins, R. Betti, K. N. LaFortune, and W. H. Williams, “Shock ignition:
A new approach to high gain inertial confinement fusion on the national ignition
[facility,” Phys. Rev. Lett.](https://doi.org/10.1103/physrevlett.103.045004) **103**, 045004 (2009).
88S. Atzeni, A. Marocchino, and A. Schiavi, “Driving high-gain shock-ignited
[inertial confinement fusion targets by green laser light,” Phys. Plasmas](https://doi.org/10.1063/1.4754307) **19**, 090702
(2012).
89C. Labaune, “Effect of the laser wavelength: A long story of laser-plasma interac[tion physics for inertial confinement fusion Teller medal lecture,” EPJ Web Conf.](https://doi.org/10.1051/epjconf/20135901012)
**59**, 01012 (2013).
90A. J. Schmitt and S. P. Obenschain, “The importance of laser wavelength for
[driving inertial confinement fusion targets. II. Target design,” Phys. Plasmas](https://doi.org/10.1063/5.0118093) **30**,
012702 (2023).

91A. Colaïtis, R. K. Follett, C. Dorrer, A. G. Seaton, D. Viala _et al._, “Exploration
of cross-beam energy transfer mitigation constraints for designing an ignitionscale direct-drive inertial confinement fusion driver,” Phys. [Plasmas](https://doi.org/10.1063/5.0150813) **30**, 082701
(2023).
92K. R. Manes, M. L. Spaeth, J. J. Adams, M. W. Bowers, J. D. Bude, C. W. Carr, A.
D. Conder, D. A. Cross, S. G. Demos, J. M. G. D. Nicola _et_ _al._, “Damage mechanisms avoided or managed for NIF large optics,” Fusion [Sci.](https://doi.org/10.13182/fst15-139) Technol. **69** (1),
146–249 (2016).
93C. Lacombe, L. Lamaignère, G. Hallo, M. Sozet, T. Donval, G. Razé, C. Ameil, M.
Benoit, F. Gaudfrin, E. Bordenave _et al._, “Full-scale optic designed for onsite study
[of damage growth at the laser megajoule facility,” Opt. Express](https://doi.org/10.1364/oe.474581) **31** (3), 4291–4305
(2023).
94P. A. Baisden, L. J. Atherton, R. A. Hawley, T. A. Land, J. A. Menapace, P.
E. Miller, M. J. Runkel, M. L. Spaeth, C. J. Stolz, T. I. Suratwala _et_ _al._, “Large
optics for the national ignition facility,” Fusion [Sci.](https://doi.org/10.13182/fst15-143) Technol. **69** (1), 295–351
(2016).
95H. Blaschke, R. Thielsch, J. Heber, N. Kaiser, S. Martin, and E.
Welsch, “Laser resistivity and causes of damage in coating materials for 193 nm by photothermal methods,” Proc. SPIE **3578**, 74
(1998).
96J. A. Sullivan, D. B. Harris, J. McLeod, N. A. Kurnit, J. Pendergrass, and E. Rose,
[“Design of a 100-kJ KrF single-pulse inertial confinement fusion driver,” Fusion](https://doi.org/10.13182/fst91-a29419)
[Technol.](https://doi.org/10.13182/fst91-a29419) **19** (3P2A), 652 (1991).

