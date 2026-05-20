---
source: "Prost_2024_Nucl._Fusion_64_026007.pdf"
source_type: "local_file"
extracted_at: "2026-03-29T20:34:12.444529+00:00"
content_hash_sha256: "4919d907b75a8009d87d096c3a6c2abf253ef24d2ead3c88fbab24fd92676fe0"
backend: "pdf_pipeline"
---

## **PAPER • OPEN ACCESS** Economically optimized design point of high-field stellarator power-plant

To cite this article: Victor Prost and Francesco A. Volpe 2024 Nucl. Fusion 64 026007

View the [article online](https://doi.org/10.1088/1741-4326/ad142e) for updates and enhancements.

You may also like

[Direct optimization of neoclassical ion](https://iopscience.iop.org/article/10.1088/1741-4326/ad75a6)
[transport in stellarator reactors](https://iopscience.iop.org/article/10.1088/1741-4326/ad75a6)
B.F. Lee, S.A. Lazerson, H.M. Smith et al.

[Reactor-scale stellarators with force and](https://iopscience.iop.org/article/10.1088/1741-4326/adc318)
[torque minimized dipole coils](https://iopscience.iop.org/article/10.1088/1741-4326/adc318)
Alan A. Kaptanoglu, Alexander Wiedman,
Jacob Halpern et al.

[Improving the stellarator through advances](https://iopscience.iop.org/article/10.1088/1741-4326/ac29d0)
[in plasma theory](https://iopscience.iop.org/article/10.1088/1741-4326/ac29d0)
C.C. Hegna, D.T. Anderson, A. Bader et
al.

This content was downloaded from IP address 73.63.211.100 on 29/03/2026 at 21:26

International Atomic Energy Agency Nuclear Fusion

Nucl. Fusion **64** (2024) 026007 (30pp) [https://doi.org/10.1088/1741-4326/ad142e](https://doi.org/10.1088/1741-4326/ad142e)

# **Economically optimized design point of** **high-field stellarator power-plant**

**Victor Prost** _**[∗]**_ [](https://orcid.org/0000-0002-1680-5108) **and Francesco A. Volpe** [](https://orcid.org/0000-0002-7193-7090)

Renaissance Fusion, 38600 Fontaine, France

[E-mail: victor.prost@renfusion.eu](mailto:victor.prost@renfusion.eu)

Received 23 June 2023, revised 9 October 2023
Accepted for publication 11 December 2023
Published 3 January 2024

**Abstract**
High temperature superconductors (HTSs) expand the design space of stellarator power-plants
(PPs) toward high magnetic fields _B_, enabling compact major radii _R_ . The present paper scans
the space of _B_, _R_ and other design parameters, finding solutions that are promising from a
physics and engineering standpoint, while minimizing the capital cost of the PP and the
levelized cost of fusion electricity. Similarly, it identifies minimum-cost design points for
next-step burning plasma stellarator experiments of fusion gain 1 _< Q <_ 10. The study assumes
advanced stellarator configurations of reduced aspect ratio, heated by neutral beam injection.
Plasma-facing, flowing liquid metal (LM) walls protect it from high heat and neutron fluxes.
The study relies on analytical first-principle calculations, and established zero-dimensional (0D)
empirical scaling laws. Power flows are illustrated by Sankey diagrams. Plasma operating
contours are used to determine the reactor’s start-up path. Sensitivity analyses are conducted to
identify the most critical reactor parameters within physics, engineering and costing,
quantifying their influence on the economics of the PPs. Such 0D study suggests that the
assumed next generation HTS, flowing LM walls, and advances in compact plasma
configurations could lead to an ignited stellarator PP of aspect ratio _A ∼_ 4, _R_ ⩽ 4 m, _B >_ 9 T,
and normalized plasma pressure _β ∼_ 5% which would minimize both the cost of electricity and
capital cost while achieving a net electric power of about 1 GW.

Keywords: fusion power plant, systems code, compact stellarator, design optimization,
liquid metal first wall, high temperature superconductor, cost of electricity

(Some figures may appear in colour only in the online journal)

**1.** **Introduction**

Stellarators exhibit plasma confinement as good as tokamaks
of comparable plasma size and magnetic field [1] and offer
additional benefits such as steady state operation, no disruption
and low recirculating power. They also present disadvantages,
most notably their hard-to-build, non-planar coils [2].

_∗_
Author to whom any correspondence should be addressed.

Original Content from this work may be used under the
[terms of the Creative Commons Attribution 4.0 licence. Any](https://creativecommons.org/licenses/by/4.0/)
further distribution of this work must maintain attribution to the author(s) and
the title of the work, journal citation and DOI.

At fields of about 5 T in the plasma, obtainable with low
temperature superconductors, stellarator and Heliotron powerplants (PPs) are expected to have large major radii _R_, between
7 and 29 m [3, 4]. However, high temperature superconductors
(HTSs) such as rare earth barium copper oxides (REBCOs)
recently enabled the construction of large-bore planar, toroidal field coils generating 20 T at the coil and about 10 T
at the plasma center, in steady state [5]. If reproduced in
stellarators, these field-strengths could significantly reduce
the size and cost of stellarator PPs. Furthermore, developments are currently being made to create wide HTS tape
which would enable novel coil architectures for stellarators

[6, 7]. Moving from non-planar modular coils with intense toroidal excursions [8] toward complex current patterns engraved

1741-4326/24/026007+30$33.00 Printed in the UK 1 © 2024 The Author(s). Published by IOP Publishing Ltd on behalf of the IAEA

on wide HTS wound on simplified coil winding surfaces,
enabling increased coverage and strong shaping of the plasma
column with simplified magnet structures [6, 7]. These developments could allow for compact, high-field stellarators which
echoes ongoing research on the optimization and development
of novel compact advanced stellarator plasma configurations
(low aspect ratio and major radius) [9–11].

Flowing liquid metal (LM) walls are another fusionenabling technology [12], synergistic with HTS: thick LMs
shield HTS from neutrons and prevent crystal damage or loss
of superconductivity; at the same time, strong fields stabilize
LM flows and favor the adhesion of current-carrying LMs to
tilted or even inverted solid substrates, thus enabling full coating and neutron-shielding of the vessel, and heat removal. LM
walls enable increased wall loading constraints, which have
been traditionally _∼_ 10 MW m _[−]_ [2] for solid wall concepts [4,
13] but could reach 25 MW m _[−]_ [2] or higher as described in
recent first wall developments [14–17]. Furthermore, flowing
liquid walls intercept _α_ particle losses, which can be significant in some stellarators.

Stellarator reactor sizing and costing studies were issued in
the past [3, 18–20]. The one presented in this paper explore the
possible new opportunities offered by developments of wide
patterned HTS tapes, thick LM flows and reduced aspect ratio
plasma configurations. The study integrates plasma physics,
engineering and PP economics calculations. This zero dimensional (0D) system analysis identifies economically viable
high-field stellarator PPs and experiments,highlighting the
need for continuing the technological developments on HTS,
LMs, and compact plasma configurations for stellarators as
well as offering a starting point for future 3D studies in a smaller parameter-space.

It also isolates trends, regions of interest in the design
space and principal design parameters affecting the cost of
the reactor and cost of electricity (COE). This will serve as
a basis for further, 3D studies and refinements in a smaller
parameter-space by system-design codes such as PROCESS

[4, 21], TREND [22], BLUEPRINT [23] or ASC [19]. Due to
the limits of 0D analyses and the technological assumptions,
absolute estimates are therefore only indicative, but relative
arguments are reliable, e.g. in cost-savings with field increase,
reduced aspect ratio, improved confinement, etc.

The paper is organized as follows. Section 2 describes
the 0D system analysis calculations as well as the major
underlying assumptions. Section 3 illustrates how physical,
engineering and economic parameters depend on the fieldstrength _B_ and major radius _R_ . In section 4, the design point
is optimized for minimal reactor cost or electricity cost. In
section 5, said costs are found to highly depend on the
confinement re-normalization factor and on the aspect ratio,
among others. Two specific PP case studies are examined in
greater detail in section 6, under different assumptions on
HTS unit costs. Details include a Sankey diagram of power
flow, Plasma OPerating CONtours (POPCON), a discussion
on helium ashes and cost breakdown. Section 7 is dedicated
to experiments not producing net electricity but producing net
heat, i.e. fusion gain _Q >_ 1, investigating burning stellarator
plasmas.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-2-0.png)

**Figure 1.** Stellarator reactor model considered in the 0D system
analysis, main materials, along with an example plasma boundary
shown in transparent red.

**2.** **0D reactor system analysis**

Figures 1 and 2 schematically illustrate the stellarator model
and the optimization procedure to minimize the COE and capital cost of a stellarator PP. Here a stellarator design point is
defined by the following _reactor parameters_ (top of figure 2):
the magnetic field on axis _B_, the plasma major radius _R_, the
plasma aspect ratio _A_ = _R/a_, with _a_ the plasma minor radius,
the volume-averaged plasma temperature _T_, the blanket thickness _b_, the normalized pressure _β_, and the re-normalization
factor _f_ ren assigned to a specific plasma configuration in the
International Stellarator Scaling ISS04 [24].

From them other _physics parameters_, highlighted in pink in
figure 2: the density (section 2.1), fusion power _P_ fus, radiated
power, diffused power (section 2.2) and energy confinement
time section 2.3) are calculated. We then solve the steady-state
power balance (equation (6) in section 2.4) with the externally
injected heating power _P_ aux required to sustain the fusion reaction. This yields the fusion gain _Q_ = _P_ fus _/P_ aux. The information is combined with the power spent to operate various plant
systems, ultimately yielding the thermal power and net electric power from the PP (sections 2.4 and 2.5), associated with
the _PP engineering_ block in figure 2.

Sections 2.6–2.9 feature well-established _costing_ models
for the PP and its subsystems, adapting them to the present
study: the result is the total capital cost (TCC) of the PP, and
section 2.10 leads to the COE estimate. These two quantities are then optimized (equation (23)), subject to constraints.
This 0D model and the corresponding results, do not consider
specific density, temperature profiles, nor 3D geometries of
coil architectures and plasma configurations. It allows for high
level promising design space identification under specific technological assumptions which will require refined 3D analyses.

**Figure 2.** Schematic diagram of the 0D system analysis framework, with the color coding representing the different modules of the framework. The symbols and acronyms used in the schematic are detailed section 1.

## 2.1 Plasma density

We assumed a helium concentration $f_{He} = n_{He}/n_e = 5\%$ similar to Alonso *et al* [25] and equal amounts of D and T: $n_D = n_T = 0.45n_e$. The effects and implications of helium accumulation are discussed in section 6.3. The line-averaged electron density $n_e$ is computed from the normalized plasma pressure:

$$\beta = \frac{2\mu_0 T}{\hat{B}^2 \cdot 2\rho_0}$$
(1)

and is compared to the line-averaged radiative density limit found in W7-AS [26] as:

$$n_e < C_r \left(\frac{P_h}{V_p}\right)^{0.40} B^{0.34}$$
(2)

with $C_r$ a numerical constant set to 1.46 for a radiative density limit in units of $10^{20}$ m$^{-3}$ if power, volume and magnetic field are expressed in MW, m$^3$ and T, respectively.

The stellarator design points were chosen such that the plasma density remains under the empirical radiative density limit as a conservative estimate for 0D calculations which do not take into account density profiles and edge impurities which seems to have a major effect on the density limit in stellarators. However, the proposed system codes allow for varying a prefactor for the radiative limit constant $\lambda_n$ as the above empirical relation has been exceeded up to a factor of 3.5 in W7-X and LHD experiments [19, 27, 28]. $\lambda_n$ could then be varied to correspond to specific plasma configurations and edge density profiles identified in future 3D analyses [27].

## 2.2 Power balance in the plasma

The steady state, simplified 0D plasma power balance can be described as:

$$\frac{dW}{dt} = 0 = k_\alpha P_\alpha + P_{aux} - P_b - P_{rad}$$
(3)

![](images/page_003_eq_0.png)
In this analysis, the deuterium-tritium (D-T) fusion reaction was considered and all the species in the plasma were assumed to have the same temperature $T$. The alpha heating and fusion power can be calculated as follows:

![](images/page_003_eq_1.png)
$$P_\alpha = E_\alpha n_D n_T \langle \sigma v \rangle_{DT}(T) V_p$$
(4)

![](images/page_003_eq_2.png)
$$P_{fus} = (E_\alpha + E_n) P_\alpha / E_\alpha = 5 P_\alpha$$
(5)

![](images/page_003_eq_4.png)
![](images/page_003_eq_3.png)
with $E_\alpha = 14.08$ MeV and $E_n = 3.52$ MeV being the neutron and alpha particle energies from the D-T reaction, $n_D$ and $n_T$ the line-averaged densities of deuterium and tritium, $\langle \sigma v \rangle_{DT}(T)$ the D-T fusion reaction reactivity, and $V_p$ the plasma volume.

The D-T fusion reaction reactivity was calculated using the parametric fit from Bosch or Hale [29], valid for temperatures between 0.2 and 100 keV. The plasma volume was estimated as $V_p = 2\pi^2 Ra^2$ (figure 1).

The externally injected heating power $P_{aux}$, necessary to sustain the D-T fusion reaction was calculated from the steady-state power balance equation (3) written as:

$$P_b + P_{rad} = k_\alpha P_\alpha + P_{aux}$$
(6)

![](images/page_003_eq_5.png)
with $P_b$ the net diffused power, $P_{rad}$ the Bremsstrahlung radiation power, $P_\alpha$ the alpha particle heating power, and $k_\alpha$ the

alpha particle heating efficiency. The alpha particle heating efficiency was set to 90% as a conservative estimate, although recent work [11] suggest alpha particle heating efficiencies up to 99%. Synchrotron radiation losses were assumed negligible for the considered reactor design points in comparison with Bremsstrahlung radiation losses and diffused power as shown in other stellarator studies [19, 25] for similar compact highfield considerations. Verification of the synchrotron losses for our selected design space using Trubnikov's formulation [30] is conducted in sections 6 and 7. The Bremsstrahlung radiated power is:

$$P_{rad} = C_B Z_{eff} n_e^2 \sqrt{T_e} V_p$$

with $Z_{eff}$ the effective ion charge set to 1.1 for our analysis (consistently with the assumed 5% of He ashes), and $C_B$ a numerical constant set to 5.35 $10^{-37}$ for a Bremsstrahlung radiation power in units of MW if temperature and density are expressed in keV and $10^{20}$ m$^{-3}$ respectively.

The net diffused power $P_\alpha$ fulfills the following steady-state power balance equation:

$$P_\alpha = \frac{W}{\tau_E}$$

where the total DD internal plasma energy $W$, under our plasma composition assumption, is given by

$$W = 3n_e T V_p$$

## 2.3. Energy confinement

![](images/page_004_eq_0.png)
The energy confinement time $\tau_E$ is taken from the ISS04 scaling (equation (5)) in [29]:

$$\tau_E^{ISS04} = f_{ren} 0.134 a^{2.28} R^{0.64} P_{hea}^{-0.61} n_e^{0.54} B^{0.84} \iota_{2/3}^{0.41}$$

with $f_{ren}$ the re-normalization factor and $\iota_{2/3}$ the rotational transform at the $r = 2a/3$ magnetic surface. $\iota_{2/3}^{0.41}$ is provided in unit of s for $n_e$ expressed in $10^{20}$ m$^{-3}$. The energy confinement time scaling can also be expressed in terms of A and $\nu^*$ instead of $n_e$ and a:

![](images/page_004_eq_1.png)
$$\tau_E^{ISS04} = f_{ren} 0.063 A^{-2.28} R^{2.92} P_{hea}^{-0.61}$$
$$\times \left(\frac{\nu^*}{0.59 q^{-0.39} n_e^{0.54} B^{0.84} \iota_{2/3}^{0.41}}\right)$$

![](images/page_004_eq_2.png)
The optimal temperature $T$ is dictated by the D-T fusion reactivity, and the maximum, yet safe $\beta$ by equilibrium and stability limits, with a safety margin. Therefore, with good approximation, for fixed $\iota_{2/3}$ :

$$\eta_i \sim \frac{R^{0.8} B^3}{A^{0.28} P_{el}} \sim R^{0.8} B^3$$

![](images/page_004_eq_3.png)
From equations (8) and (9) it is concluded that the triple product scales like the 4th power of R:

$$nT\tau_E \sim \frac{P_{fus}}{P_{el}} \sim R^4 P_{el}$$

In this study, advanced compact plasma configuration parameters with optimized neoclassical transport and alpha particle confinement were fixed and assumed to match ongoing developments [9] and past reactor studies [19, 20, 31, 32]. The re-normalization factor was set to $f_{ren} = 1.4$ to match other stellarator reactor studies, recent developments and expectations for W7-X [19, 20, 31, 32]. The $\iota_{2/3}$ was set to 0.9 to match HELIAS [18, 31] and novel compact stellarator configurations [9]. The normalized plasma pressure $\beta$ was chosen to be 5% as a conservative estimate similar to those obtained in LHD and HELIAS studies [3, 18, 19] although higher values were shown to be possible for NCSX-type plasmas [3, 10, 16]. More optimistic plasma configuration parameters for low-aspect ratio will need to be further validated through 3D studies and plasma simulation codes [9].

![](images/page_004_eq_4.png)
## 2.4. Thermal power and net electric power

![](images/page_004_eq_5.png)
The net electric power produced by the PP is

$$P_{el} = \eta_{th} P_{th} - \frac{P_{hea}}{\eta_{hea}} - P_{cryo} - P_{lres}$$

with $\eta_{th}$ the thermal plant efficiency and $P_{th}$ the gross thermal power generated by the fusion reactions and energy multiplication occurring in the blanket. $P_{hea}$ is the pumping power required to sustain the LM flow in the stellarator blanket and $P_{cryo}$ the required cryogenic system operating power. $\eta_{hea}$ and $\eta_{cryo}$ denote the electric conversion efficiencies for the plasma heating and LM pumping systems.

![](images/page_004_eq_6.png)
The thermal power can be calculated as the sum of the power from the neutrons, from lost-$\alpha$ particles, from radiation and from diffusion, as all these contributions are captured by the LM plasma-facing wall:

$$P_{th} = f_{bl}[f_n P_n + (1 - f_{\alpha c}) P_\alpha + P_{rad} + P_\alpha - \frac{P_{hea}}{\eta_{hea}}]$$

The fraction of neutron-to-alpha fusion power is given by $f_n = E_n/(E_n + E_\alpha) = 0.8$ and the neutron energy multiplication factor set to $f_{bl} = 1.24$ consistently with our choice of fusion blanket module [34] and in a practical typical range of $f_{bl} \sim 0.9$–1.4, depending on the blanket configurations [25, 35–37].

![](images/page_004_eq_7.png)
The wall loading on the reactor blanket can then be calculated from the thermal power as:

![](images/page_004_eq_8.png)
$$P_{WL} = \frac{P_{n,0}}{S_p}$$

with $S_p$ the plasma-facing surface, estimated using the equivalent toroidal surface $S_p \sim 4\pi^2 R a$, as shown in figure 1. This 0D model considers average power density and heat extracted through the LM wall as it does not include any 3D considerations such as specific hot-spot locations, peak heat loads, or transient effects due to specific 7D plasma configurations.
![](images/page_004_eq_9.png)

_2.5._ _Power consumption_

The LM pumping power _P_ pump was calculated from the total
pressure drop in the LM loop ∆ _P_ loss and the volumetric flow
rate _Q_ LM. The volumetric flow rate was computed through the
LM transit time in the plasma facing region required to heat
the LM from a temperature _T_ [LM] in to _T_ [LM] out [. These inlet and out-]
let temperatures were set to match the heat conversion system
operating temperatures. As a 0D analysis simplified model, the
LM mass flow rate through the plasma facing region can be
calculated as:

( )
_P_ th = _c_ [LM] P _m_ ˙ LM _T_ [LM] out _[−]_ _[T]_ [LM] in

(17)

to _T_ [LM] out [=][ 900] _[◦]_ [C] [[][42][–][44][].] [The] [LM] [pump] [efficiency] [was]
set to _η_ pump = 0 _._ 20 to reflect current electromagnetic pump
technologies [45–47]. The conceptual blanket is composed
of a 33 cm LM layer flowing on the LM vessel (5 cm), followed by a 50 cm neutronic shielding layer (vanadium hydride
VH2) before the stellarator coils [34]. The LM layer is composed of a 15 cm thick moderator/multiplier layer of Lead,
and a 18 cm tritium breeding layer of non-enriched lithium–
lithium hydride chosen to be _f_ Li = 5% lithium and _f_ LiH = 95%
lithium hydride [34]. The flowing LM blanket was selected
![](images/page_005_eq_0.png)
for radiation protection, tritium breeding, and heat extraction
considerations [15, 34]. Heat extraction was assumed to be carried out by the flowing LM layer (Li–LiH) and the LM characteristics (mass density, heat capacity, conductivity and kinematic viscosity) were calculated from published temperature
dependent properties [48–51]. This assumed highly compact
radial build proposed by Renaissance Fusion [6, 34] follows
ongoing development toward compact radial build blankets

[52, 53].
Using equations (14)–(19) and the plasma power characteristics from section 2.2, the PP steady state net electric
power, _P_ e, can thus be calculated from the reactor parameters
_B,_ _R,_ _T,β,_ _b,_ _A,_ _f_ ren as shown in figure 2.

_2.6._ _Reactor cost model_

The cost model developed in this study is based on the ARIES
![](images/page_005_eq_1.png)
Cost Structure (ACS) [54, 55] similar to other stellarator
studies [19, 56]. The ACS cost model was updated for specific
reactor characteristics and components, such as the HTS magnets and flowing LM blanket. All costs are presented in 2021
dollars translated from the 2009, 2004 and 1992 dollars cost
values included in the ACS cost model. The developed cost
model is used to calculate both the capital costs of the major
PP components as well as the COE. It should be emphasized
that the focus of such cost models is the variation in the COE,
rather than its absolute value.
The cost accounts used to calculate the PP total capital cost
(TCC) are listed in table 1. The PP TCC can then be computed as the sum of the direct and indirect capital costs (items
90–98), with the total direct capital cost (TDC) calculated as
the sum of cost accounts 20–27. The indirect costs are calculated as fractions of the TDCs for construction services and
equipment, home office engineering and services, field office
engineering and services, the owner’s cost, process contingency, project contingency, and interest and escalation in cost
during construction. A detailed description of these costs is
provided in [54], including cost scalings with reactor’s parameters, components power, mass or volume. In general, the
cost accounts have a multi-level structure that includes subaccounts for which the costs are evaluated as _ci ·_ ( _Xi_ ) _[e][i]_, where
_ci_ is the unit cost for the sub-level account _i_ (given in $ kg _[−]_ [1],
$ W _[−]_ [1], $ m _[−]_ [3], etc), _Xi_ is the quantity to which the cost is proportional to (mass, power, volume etc) and _ei_ is an exponent

[54, 57].
The cost account 22.1 in table 1, which includes the
reactor’s blanket, was updated to reflect the flowing LM wall

with _c_ [LM] P the LM heat capacity, and _m_ ˙ LM the LM mass flow
rate. The volumetric flow rate can then be simply computed
using the LM mass density _ρ_ LM, as _Q_ LM = _m_ ˙ LM _/ρ_ LM.
The total pressure drop from the LM loop was estimated
as:

∆ _P_ loss = ∆ _P_ head + ∆ _P_ pipe + ∆ _P_ MHD (18)

with ∆ _P_ head the gravitational head losses, ∆ _P_ pipe the pressure drop from viscous pipe flow, and ∆ _P_ MHD the pressure
drop from the magneto-hydrodynamic (MHD) drag within the
reactor [38].
The gravitational head losses were estimated as ∆ _P_ head =
_ρ_ LM _gh_, with _h_ = 2( _a_ + _b_ ) assuming LM flowing from the top
to bottom of the plasma vessel ( _a_ the plasma minor radius, and
_b_ the LM blanket thickness).
The pressure drop from viscous pipe flow was estimated

as ∆ _P_ pipe = _f_ D _L_ pipe 2 [1] _[ρ]_ [LM] _Dv_ [2] pipepipe [,] [with] _[f]_ [D] [the] [Reynolds] [depend-]

ent Darcy friction factor, _L_ pipe the total pipe length, _D_ pipe
the average pipe diameter and _v_ pipe the mean LM velocity
through the pipes. The mean LM velocity through the pipes
![](images/page_005_eq_2.png)
was calculated so as to match the required LM mass flow rate
(equation (17)) when accounting for the number of inlet pipes
and pipe diameter.
The pressure drop from MHD effects was estimated as
∆ _P_ MHD = _kσ_ LM _B_ [2] _v_ LM _L_ MHD, with _σ_ LM the LM electrical conductivity, _v_ LM the LM velocity and _k_ the MHD drag coefficient

[38].
The total electric power required to run the cryogenic plant
_P_ cryo can be estimated from _P_ th, following the EU-DEMO
studies [39–41] and the TREND systems code [22], as:

_P_ cryo = _f_ cryo _P_ th (19)

with _f_ cryo the cryogenic power fraction, previously estimated
in the range of 0.8%–1.3% for fusion reactors with _P_ th = 2.3–
2.4 GW. The value of _f_ cryo = 1 _._ 3% was chosen conservatively
for this study, and could be further refined with a cryoplant
design model.
The balance of plant system efficiencies described in
equation (14), LM composition, and operating temperatures
were held fixed in the design exploration study. The thermal
plant efficiency was set to _η_ th = 0 _._ 49 assuming a combined
Brayton cycle with LM temperatures set to _T_ [LM] in [=][ 700] _[◦]_ [C]

**Table 1.** Cost accounts from the ACS cost model [54, 55].

| Code | Item |
|------|------|
| 20 | Land and land rights |
| 21 | Structures and site facilities |
| 22 | Reactor core equipment |
| 22.1 | Fusion energy capture and conversion |
| 22.2 | Plasma confinement |
| 22.3 | Plasma formation and sustainment |
| 22.4 | Vacuum for reactor core |
| 22.5 | Primary structure and supports |
| 22.6 | First heat transfer and transport |
| 22.7 | Radioactive materials treatment and management |
| 22.8 | Fuel handling and storage |
| 22.9 | Maintenance equipment |
| 22.10 | Instrumentation and control |
| 22.11 | Other reactor plant equipment |
| 22.98 | Spare parts |
| 22.99 | Contingency |
| 23 | Turbine plant equipment |
| 24 | Electric plant equipment |
| 25 | Heat rejection equipment |
| 26 | Miscellaneous plant equipment |
| 27 | Special materials |
| 90 | Total direct costs (TDC) |
| 91–98 | Indirect costs |
| 99 | Total capital cost (TCC) |

**Table 2.** Cost model specific mass densities and unit costs used in this study.

![](images/page_006_eq_0.png)
| Material | Density (kg·m⁻³) | Unit cost ($·kg⁻¹) |
|----------|-----------------|-------------------|
| Li | $5.12 \cdot 10^2$ | 86 |
| LiH | $8.20 \cdot 10^2$ | 20 |
| Pb | $1.13 \cdot 10^4$ | 2 |
| YH₂ | $4.42 \cdot 10^3$ | 200 |
| HTASS/RG SS | $7.80 \cdot 10^3$ | 10 |
| Hastelloy C-276 | $8.89 \cdot 10^3$ | 48 |

Blanket and neutronic shield used in these stellarator designs. The part of cost account 22.1 needed for the blanket was calculated as the sum of LM (liquid metal) shield components unit cost/mass times the mass of each component. The blanket is composed mostly of non-enriched lithium, lithium hydride, lead, and vanadium hydride, whose unit costs are summarized in table 2.

## 2.7. HTS cost model

The magnets' cost sub-account 22.2.1 for plasma confinement was also updated to reflect the use of ReBCO HTS material. As a simplified 1D model for costing the assumed current pattern HTS coil architecture [6, 7], the peak magnetic field $B_{peak}$ in the coils was calculated from the on-axis magnetic field and the reactor parameters following the $1/R$ dependence of toroidal fields [36, 58]:

$$B_{peak} = b_{peak} \cdot \frac{BR}{R - a - b} \tag{20}$$

The study considered $b_{peak} = 1$ instead of conventional peaking factors $b_{peak} > 1$ linked to modular non-planar stellarator coils with large toroidal excursions [8, 19, 20], due to the assumed patterned HTS coil architecture combined with current developments of coil winding surface optimization which have been shown to allow for reduced magnetic field peaking factors. [7, 59]. Appendix A investigates increased peaking factors $b_{peak} = 1, 1.2$, and 1.5 as seen in modular non-planar stellarator coils.

From the ReBCO at the coils, the HTS tape critical current density $J_c$ was evaluated from the parametric relationships that describe the dependency of ReBCO HTS tape critical current density based on the magnetic field, temperature, and field angle [60–64]. In this study we assumed a field angle of 0°. Note that this is a pessimistic assumption, corresponding to having the magnetic field perpendicular to the tape. In reality, accurate stellarator fields in the plasma volume require the field to be tangential to the plasma boundary and, by extension, to a close-fitting Coil Winding Surface. Therefore, the field will typically be at angle to properly wound coils.

We also assumed an operating temperature of 20 K, and a ReBCO 2G HTS tape from SuperPower Inc. (Glenville, USA) [63] following the following critical current dependency on the peak magnetic field:

$$J_c = 4.5 \cdot 10^{11} B_{peak}^{-0.807} \tag{21}$$

with $J_c$ in A·m⁻². This parametric relation is valid for $B_{peak}$ between 1 and 20 T, and was derived from a 4 mm tape with a 1.6 μm thick ReBCO layer.

![](images/page_006_eq_1.png)
We used 12 mm ReBCO tapes for the cost calculations, with a total thickness of $d = 1$ mm, and a 1.6 μm thick ReBCO layer. The number of layers of HTS tapes was then derived from the required current to generate the peak magnetic field $B_{peak}$ and the critical current density $J_c$ with the magnet operating at 75% of the critical current density value (critical current safety factor = 1/0.75 = 1.33 for quench protection). The total length of HTS tape $L_{HTS}$ was then computed from the reactor geometry and required number of HTS layers. Two HTS tape cost models are considered in the study: an optimistic bulk cost of 12 \$/m⁻¹ (or 303 \$/kA⁻¹ m⁻¹) that assumes further cost reductions due to high-volume production and improved manufacturing technologies and a conservative unit cost of 78 \$/m⁻¹ (or 2003 \$/kA⁻¹ m⁻¹) reflecting the current cost of HTS tapes [64, 65]. The tape cost was finally calculated from $L_{HTS}$ and the unit cost.

## 2.8. Heating

The externally injected fusion heating system, part of cost account 22.3 (plasma formation and sustainment), was assumed to be a negative neutral beam injection (NNB) from its better neutralization efficiency (~85%) compared to positive ion beams for beam energies above 100 keV [66]. NNBI is a candidate approach for energy capable of efficiently (30%–60%) heating the high-density, high-field plasmas required for compact fusion devices [67–69]. A single

heating system was considered in this analysis for simplification although electron cyclotron heating (ECH) could also be
used in conjunction with NNBI, provided that gyrotrons of sufficiently high power and frequency can be developed to operate in high magnetic field environments (10 T and above) [70].
Other heating systems such as ion cyclotron heating (ICH),
heating by lower hybrid (LH) waves, or helicon heating were
not considered due to the complex plasma boundary shape of
stellarators, the reduced need for current drive, or their lower
technology readiness level [8, 19, 71, 72].
For each reactor design point, the required beam energy
level was estimated primarily based on the average plasma
density and reactor geometry. The requirement was set for
the beam to deposit 95% of its energy by charge exchange,
proton collisions, and electron collisions after traveling a distance of 3a/2 in the plasma core. For this calculation, the
plasma was assumed to have an elongation of 4, leading to
a reduced beam penetration distance for an adequately positioned NNBI system injection port. The NNBI system’s beam
energy requirement is further described in the high-field stellarator case study (section 6). The auxiliary heating system’s
unit cost was assumed at 6.23 $ W _[−]_ [1], based on other reactor
studies [19, 54, 56].
Note that most PPs in this study are ignited and, as it
will be shown in section 6.2, the heating can be turned off
within a minute of initiating the plasma discharge. A shortpulse heating system will certainly be less expensive than a
steady-state one, but these cost-savings are not estimated here.
Considerations on how often the heating system needs to be
turned on again during a plasma pulse, e.g. for control purposes, are also left as future work.

_2.9._ _Structure and support_

The primary structure and supports, cost account 22.5, was
also updated for the use of 316LN-IG stainless steel for the
plasma confinement magnet’s support structure and Hastelloy
C-276 for the vacuum vessel. The materials choices were
motivated by their mechanical, neutronics and corrosion resistant characteristics as well as their use in other fusion experimental reactors [73, 74] and reactor studies [19, 42, 54, 56]. A
maximum allowable stress of 750 MPa was used for 316LNIG stainless steel under 20 K and a maximum allowable stress
of 790 MPa was used for Hastelloy C-276 [73, 75, 76]. The
structural materials mass densities and unit costs are summarized in table 2.
![](images/page_007_eq_0.png)
The magnet support structure was sized using a thickwalled cylindrical pressure vessel model [77] using the peak
magnetic field to compute the resulting Lorentz force. The
structure thickness was determined with a safety factor of 2.0
on the maximum allowed stress, as a conservative limit. The
sizing calculation was verified against the virial theorem limit

[78] and the empirical scaling from Warmer [79], which is
based on superconducting devices such as W7-X, LHD and
ITER: _M_ struc = 1 _._ 3483 _W_ [0] mag _[.]_ [7821], with _M_ struc the total structure
mass expressed in t, and _W_ mag the magnetic energy in MJ.

From the magnet support structure sizing, the reactor radial
build inboard clearance _r_ inboard is then calculated to ensure a
minimum space on the reactor inboard side for structures and
shielding. The 0D system code enforces an inboard clearance
positive constraint meaning that the radial buildup from the
magnet and structure thicknesses, blanket size, vacuum vessel size, plasma minor radius is smaller than the plasma major
radius. Additional constraints could also be applied when considering specific coil architecture, for instance discrete nonplanar modular coils which would require a large minimum
inboard clearance [19, 20].

_2.10._ _COE_

The COE is calculated as:

COE = _[C]_ [AC][ + (] _[C]_ [OM][ +] _[ C]_ [SCR][ +] _[ C]_ [F][)(][1][ +] _[ y]_ [)] _[Y]_ + _C_ DD (22)

8760 _P_ e _f_ avail

where _C_ AC is the annual capital cost charge (TCC multiplied
by the fixed charge tate (FCR)), _C_ OM the annual operations
and maintenance cost, _C_ SCR the annual scheduled component
replacement cost, and _C_ F the annual fuel cost. In this equation,
the annual costs are given in $ for a COE given in $ MWh _[−]_ [1] .
FCR is a charge to the TCC annualized over the operating life
of the plant: here it is set to 0.043, assuming a reactor lifetime
of 40 years, a discount rate of 3% that reflects the 2021 low
interest rates [80–86], and the Gen-IV guidance on simplified
FCR values [54]. A broader range of discount rates, up to 7%,
will be considered in Sec 4.2. to understand their effect on the
COE [83]. _y_ is the assumed escalation rate, chosen as 5% to
reflect the current inflation rates [82, 87, 88] and _Y_ the construction time, set to 6 years.
The _C_ AC is given as 101 _·_ ( _P_ e _/_ 1 _._ 2) [0] _[.]_ [5] in [M$ 2021] with _P_ e
in units of GW [54].
The fuel cost was calculated based on _P_ fus assuming a unit
cost of deuterium of 13.4 k$ kg _[−]_ [1] [89, 90]. The cost of tritium
is not included in the annual fuel cost as it will be bred from
the blanket and conditioned through a dedicated tritium plant
(cost account 22.8).
The _C_ SCR considers the expenses of replacing plasmafacing components or equipment subject to radiation damage.
The lifetime of these components are estimated when radiation damage reaches 200 dpa (displacement per atom) in the
materials for a given neutron wall loading power [15, 34, 42].
Our chosen LM blanket would not exceed 3–5 dpa yr _[−]_ [1] on the
blanket backing solid wall for the considered fusion PP solutions. These components would thus not require replacements
over the plant’s lifetime, leading to negligible _C_ SCR relative to
over cost accounts [15, 34].
The _C_ DD represents the decontamination and decommissioning allowance estimated at 3.49 M$ yr _[−]_ [1] following the
ACS model [54]. The plant capacity factor _f_ avail was set to 85%
similar to other reactor studies [54]. For reference, the TCC
of the PP generally accounts for more than 75% of the COE

[19, 42, 56, 89]

**Figure 3.** Results of a scan of _B_ and _R_, illustrating how it affects several physics plasma parameters for two aspect ratios, _A_ = 3 ( _a_ )–( _d_ ) and
_A_ = 9 ( _e_ )–( _h_ ). _f_ ren is set to 1.4, _T_ to 10 keV, and _β_ to 5%. The orange dashed line in ( _a_ ) and ( _e_ ) represents _n_ e _/n_ c = 1, the radiative density
limit threshold with _n_ c the stellarator radiative density limit (equation (2)).

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-8-0.png)
## **3. Exploration of ( B, R ) design space**

In this section we apply the 0D stellarator system analysis of
section 2 across the ( _B_, _R_ ) stellarator design space for fixed
_T_ = 10 keV, _β_ = 5%, _f_ ren = 1 _._ 4, blanket thickness _b_ = 83 cm
(consisting of 15 cm of Pb, 18 cm of Li–LiH and 50 cm of
VH2) and for two values of _A_ (3 and 9). Other combinations
of _T,β,_ _b,_ _A,_ _f_ ren were considered and not shown for brevity but
highlighted in the remainder of the paper.

_B_ was varied between 5 and 15 T, corresponding to
peak magnetic fields around 20–40 T, reflecting the current
HTS performance [91–93]. _R_ was kept smaller than 9 m
to reduce cost, operation complexity and construction time

[2, 19, 42, 91].

For each _B,_ _R_ pair we calculated the density _n_ e needed to
achieve the target _T_ and _β_ . We then computed the resulting
energy confinement time, triple product and peak magnetic
field at the coils. The results of this physics analysis are plotted
in figures 3 and 4. Likewise, powers relevant to the engineering analysis are contoured in figures 5 and 6 and costs from
the economic analysis are plotted in figures 7 and 8.

In all contours, different color-scales are adopted for quantities to be maximized or minimized: respectively shades of
blue and red, with lighter shades indicating preferred values.
‘Boxes’ around the color-scales highlight the targeted ranges.
Solid lines mark essential limits (for instance the triple product
for break-even). In other cases there was some degree of arbitrariness, so those values were marked as desirable and boxed
with a dashed line.

These hard, essential limits and the somewhat softer,
desirable limits, as well as the radiative density limit from
equation (2) (orange curve in figures 3( _a_ ) and ( _e_ )) define
regions of interest in ( _B_, _R_ ) where operation is possible, or at
least preferable, from a physical, engineering and economic
point of view. Such regions are highlighted respectively in
green in figure 4, in brown in figure 6 and in blue in figure 8.
Two shades of green are used because the desirable value _τ_ E =
2 s can only be obtained for _A_ = 3, hence a relaxed _τ_ E = 1 s is
also considered.

_3.1._ _Physics parameters exploration_

Per figure 4, physics operation is bound by _τ_ E and by the radiative density limit. For _A_ = 3, it is also bound by the limits on
the maximum _B_ peak and minimum _n_ e (figure 4( _a_ )). The essential limit is on _n_ e _Tτ_ E, but _T_ is fixed and soft limits are imposed
on _n_ e and _τ_ E to ‘share the weight’ in how they contribute to
high triple products. The radiative limit density having been
exceeded in some specific cases [27], the threshold of twice
the radiative limit is also shown highlighting a larger design
space (figure 3( _a_ )). For _A_ = 9, instead, physics operation can
also be limited by impractically large _R_, as expected, and large
_B_ (figure 4( _b_ )).

_3.2._ _Power parameters exploration_

Figure 6 shows that power engineering is upper-limited by
manageable values of wall load _P_ WL and radiated power _P_ rad.

**Figure 4.** Regions of interest shown in green of physics operations within the design space scan of _B_ and _R_ for two aspect aspect ratios
_A_ = 3 ( _a_ ) and _A_ = 9 ( _e_ ). _f_ ren is set to 1.4, _T_ to 10 keV, and _β_ to 5%. Regions of interest are bound by solid and dashed lines representing the
radiative limit, target _τ_ E, maximum _B_ peak, minimum _n_ e and _n_ e _Tτ_ E values.

**Figure 5.** Results of a scan of _B_ and _R_, illustrating how it affects several physics power parameters for two aspect ratios, _A_ = 3 ( _a_ )–( _g_ ) and
_A_ = 9 ( _h_ )–( _n_ ). _f_ ren is set to 1.4, _T_ to 10 keV, and _β_ to 5%. In the fusion gain plots ( _e_ ) and ( _k_ ), the black dashed line marks the boundary of the
_Q_ = _∞_ design points, and the red dashed line the _Q_ = 40 design points.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-9-0.png)

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-9-1.png)

**Figure 6.** Regions of interest shown in brown of relevant power considerations within the design space scan of _B_ and _R_ for two aspect
aspect ratios _A_ = 3 ( _a_ ) and _A_ = 9 ( _e_ ). _f_ ren is set to 1.4, _T_ to 10 keV, and _β_ to 5%. Regions of interest are bound by solid and dashed lines
representing targets or engineering limits on _Q_, _P_ fus, _P_ e, _P_ [max] aux [,] _[ P]_ WL [and] _[ P]_ rad [values.]

**Figure 7.** Results of a scan of _B_ and _R_, illustrating how it affects several economic parameters for two aspect ratios, _A_ = 3 ( _a_ )–( _d_ ) and _A_ = 9
( _e_ )–( _h_ ). _f_ ren is set to 1.4, _T_ to 10 keV, and _β_ to 5%.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-10-0.png)

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-10-1.png)

The high _P_ WL = 25MWm _[−]_ [2] is not achievable with solid
plasma-facing components [94, 95], but can be easily removed
by fast-flowing LM walls [12, 15]. At the lower boundary, the
region of interest is limited by the minimal _Q_ [25, 96–98],
_P_ fus and _P_ e, and maximum _P_ [max] aux [.] [The] [latter] [quantity] [will] [be]

discussed below but, in brief, it denotes the maximum auxiliary heating power to be administered to the plasma at any
time (‘saddle point’ in the POPCON analysis described in
section 6) in its start-up and ramp-up toward steady state operation. While most PPs in the present paper are ignited and
_P_ aux can eventually be turned off, the heating system must

be capable of _P_ [max]

[max] aux [, and excessive values of] _[ P]_ aux [max]

be capable of _P_ aux [, and excessive values of] _[ P]_ aux [are deemed]

impractical. The _Q_, _P_ fus, _P_ e and _P_ [max] aux [limits] [are] [all] [close] [to]

impractical. The _Q_, _P_ fus, _P_ e and _P_ aux [limits] [are] [all] [close] [to]

each other in the _A_ = 3 case. For _A_ = 9, the most stringent limit
comes from _P_ [max] aux [.]

The effect of _A_ on _P_ fus and _P_ rad in figure 5 is easily understood from their increase with the plasma volume _V_ a _∝_ _R_ [3] _/A_ [2],
assuming the same _n_ e and _T_ . Most of the power characteristics
are linearly related to _V_ a meaning that, for fixed _T_ and _B_, the
same value of _V_ a, thus _P_ fus for example, could be achieved
in a device with a major radius _∼_ 2.1 times smaller when
considering _A_ = 3 instead of _A_ = 9. Similarly, design points of

**Figure 8.** Regions of interest shown in blue of relevant economics considerations within the design space scan of _B_ and _R_ for two aspect
aspect ratios _A_ = 3 ( _a_ ) and _A_ = 9 ( _e_ ). _f_ ren is set to 1.4, _T_ to 10 keV, and _β_ to 5%. Regions of interest are bound by solid and dashed lines
representing targets or limits on COE and TCC values.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-11-0.png)

comparable fusion gain _Q_ follow the _B_ ( _R_ ) relation _B ∼_ _R_ _[−]_ [3] _[/]_ [4]

which can be derived from equations (1) and (5) assuming constant values of _P_ fus, _T_, _A_, and _β_ . This relationship emphasizes
that high-field magnet technologies can enable more compact
stellarator devices.

_3.3._ _Economics exploration_

Figure 8 highlights that PP’s economics are mostly bound
by the COE and the PP’s capital cost TCC. There is a
trade-off between low COE and low TCC (figure 7). The
region of economic interest is defined to include design points
with COE ⩽ 50 $ MWh _[−]_ [1], and TCC ⩽ of 7.0 $B. The COE
threshold was chosen to be competitive with renewable [83–
86, 99] and the TCC threshold was chosen to represent the
lower end of clean baseload electric plant technologies (such
as nuclear fission plants) [83–86, 100] in order to allow some
margin and account for our cost model uncertainties. This cost
exploration highlights that lower aspect ratio ( _A_ = 3) devices
enable reduced TCC for similar COE values, and a wider
range of reactors within the region of interest compared to
higher aspect ratio devices ( _A_ = 9). In addition, the design
space exploration for _A_ = 3 (figure 8( _a_ )) highlights that there
is a region of _B ≃_ 8 T and _R ≃_ 4 T that would minimize both
the COE and TCC for fixed value of _A_ = 3 and _T_ = 10 keV.

_3.4._ _Combined parameters exploration_

Figure 9 is constructed by overlaying contour lines of relevant
physics, engineering, and economics parameters. Overlaying
multiple parameters enables the identification of a region of
interest (yellow shaded area in figure 9) within which physics,
engineering and economics trade-offs can be visualized. The

achieve similar characteristics (COE, _P_ e, _C_ 22, _P_ aux _[...]_ [),] [and]

that one could trade-off magnetic field intensity _B_ with reactor
major radius _R_ following a _B_ ( _R_ ) relation _B ∼_ _R_ _[−]_ [3] _[/]_ [4] similar to
the fusion gain _Q_ dependency seen above.

Within the regions of potential reactor design points, the
design space exploration scan also shows that decreasing _R_
for a constant _B_ results in design points with increased COE
but decreased TCC and _C_ OM. There is a trade-off between
low COE and high TCC fusion PP designs. This initial design
space exploration for fixed _A_ and _T_ suggests that there is a specific set of reactor parameters ( _B_, _R_, _T_, _A_ ) that could minimize
both the COE and the TCC.

**4.** **Cost-optimal stellarator design points**

_4.1._ _Reactor design point optimization_

Using the 0D stellarator system analysis described in
sections 2.2–2.6, the reactor parameters ( _B_, _R_, _T_, _A_ ) were
optimized to minimize the COE and TCC, for chosen plasma
parameters (fixed _f_ ren, _ι_ 2 _/_ 3, and _β_ values) under a set of physics
and engineering constraints (figure 2).

( _B_, _R_ ) design space scan shows that there is a large family of
PP design points within our defined region of interest for _A_ = 3
(yellow shaded region in figure 9( _a_ )) but not for _A_ = 9. For the
_A_ = 9 case, relaxing the confinement time _τ_ E limit to 0.4 s, and
the peak heating power _P_ [max] aux [to 80 MW would then allow for]

a narrow range of interest although at _R >_ 6 m and _B >_ 10 T.

For the _A_ = 3 exploration, design points lying on the
COE = 50 $ MWh _[−]_ [1] line also lie on a the line of constant net
output power _P_ e = 1 _._ 0 GW, reactor core cost _C_ 22 = 1 _._ 5 $B and
required peak auxiliary power _P_ [max] [=][ 15 MW. There seem to]

required peak auxiliary power _P_ aux [=][ 15 MW. There seem to]

be a family of reactor designs with varying _B_ and _R_ values that
achieve similar characteristics (COE, _P_ e, _C_ 22, _P_ [max] aux _[...]_ [),] [and]

**Figure 9.** Results of a scan of B and R for aspect ratios A = 3 (a) and A = 9 (b), with overlaid contour regions of interest from the physics (green solid line), engineering (brown solid line), and economics (blue solid line) parameters highlighted in figures 3–8. The intersection of these contours defines a PP region of interest (yellow shaded area) for physics, engineering, and economics perspective.

The optimization problem was formulated as:

$$\min_{B,R,T,A} \{\text{COE, TCC}\}$$

s.t. $b_0 < b_\text{limit}$

$r_\text{minor} \geq 0.5 \text{ m}$

$P_\text{out}^\text{net} \geq 90 \text{ MW}$

$B_\text{peak} < 20 \text{ T}$

$P_f > 0 \text{ GW}$ (23)

![](images/page_012_eq_0.png)
The reactor parameters were varied from 5 to 15 T for the on-axis magnetic field, B, from 1 to 9 m for the major radius, R, from 5 to 15 keV for the plasma temperature, T, and 3 to 10 for the reactor aspect ratio, A. Peak magnetic fields at the coils, $B_\text{peak}$, was constrained to remain under 20 T to reflect current HTS conductors performance [91–93]. The $B_\text{peak}$ limit is not a hard limit but mostly indicative as ever higher magnetic fields have been achieved with HTS tapes (from 40 T in small devices [101, 102]) and it is not excluded that it could be reproduced within a stellarator. The density limit is not an absolute limit neither but linked to experimental results and $b_0 = 1$ was chosen to be conservative although higher density limit have been achieved in specific configurations [27]. In addition, an inboard clearance constraint on $r_\text{minor}$ was defined in order to allow for increased margin, plausible physical model and engineering basics. The stellarator parameters multi-objective constrained optimization was conducted in Python using a non-dominated sorting genetic algorithm [103]. The resulting solution was a set of Pareto-optimal design points with respect to the COE and TCC.

## 4.2. Minimizing COE and TCC

Optimal designs in terms of both COE, and TCC, obtained for varying reactor parameters (B, R, T, A) are presented below (figure 10).

The COE, TCC, and output grid power $P_e$ of the Pareto optimal PP design points are shown in figure 10. There is a trade-off between large PPs that minimize the COE and compact PPs that minimize the TCC (figure 10). Large fusion plants benefit from economies of scales, with increased net electricity output which reduces the COE (see equation (22)). On the contrary, PPs of smaller size require reduced volume of materials (such as HTS, structural and blanket materials) and result in lower cost which also reduces the TCC (section 2.6).

A design point lying in the region of low capital cost ($C_{22}$) and high COE is an attractive first of a kind (FOAK) PP (figure 10(*a*)) as it would demonstrate net electricity production while minimizing the capital cost. A PP with the following parameters: $B = 7.5$ T, $R = 3.8$ m, $T = 7.7$ keV, and $A = 3.1$ would fit in the Pareto curve FOAK region of interest. Such a design, could be retrofitted in a dismissed nuclear fission PP to reduce its capital cost and make use of existing installations such as the thermal power conversion plant. This FOAK PP would have a neutron wall loading of 5.3 MW m$^{-2}$, result in 0.7 GW of fusion power and produce 0.10 GW of electricity at 100 \$/MWe$^{-1}$ for a reactor core cost $C_{22}$ of 1.1 B\$.

A design point lying at the "elbow" of the Pareto-front curve (figure 10(*b*)) is economically attractive both in terms of COE and TCC. A PP with the following parameters: $B = 10.2$ T, $R = 3.8$ m, $T = 10.2$ keV, and $A = 4.1$ would lie in the Pareto curve "elbow" region of interest. Such a design would result in 1.8 GW of fusion power and produce 1.0 GW of electricity

**Figure 10.** Pareto front of the optimal design points in terms of cost of electricity (COE) and capital cost (( _a_ ) reactor core cost _C_ 22, ( _b_ )
TCC). Each marker represents an optimal plant and the color of the marker represents the plant’s net electric power ( _P_ e). The arrows
indicate how the stellarator characteristics changes along the Pareto front. ( _c_ ) The Pareto optimal design point’s parameters ( _B_, _R_, _T_, _A_ )
along with several PP characteristics are shown here. Each marker represents an optimal reactor resulting from the fusion PP cost
optimization (section 4.1). Red markers represent the design points that achieve ignition ( _Q_ = _∞_ ) and blue markers the ones with finite
fusion gains. For the the electron density plot, markers with light red and light blue colors represent the corresponding radiative density limit
for each reactor design point.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-13-0.png)

at 47.5 $ MWh _[−]_ [1] for a TCC around 5 B$. A more in depth
analysis and description of such a reactor is carried out in
section 6.

To further understand the family of Pareto cost optimal
reactors, the reactor parameters and reactor characteristics are
shown in figure 10. Each marker represents a Pareto optimal

reactor (shown in figure 10). The markers colored in red
describe ignited plasmas ( _P_ aux = 0) and in blue non-ignited
plasmas ( _P_ aux _>_ 0). Minimizing the TCC of the PP corresponds to reducing both _A_ and _R_, resulting in a more compact device of lower _B_ and _T_ . These highly compact reactors ( _R <_ 4 m, with _A_ = 3) would minimize the TCC needed

A discount rate of ¯ _r_ = 7%, would increase the COE and
TCC per watt of a stellarator based electric PP, however reactor
designs around 1 GWe would still remaining competitive with
the upper range of standard renewable electric plants. This
is even more so as stellarator based plants would provide
firm, base-load electric power unlike traditional renewables
without energy storage. Taking into account the reduced capacity factor of standard renewable energy [85] and the current
high cost of energy storage, a net-zero carbon electric grid
without firm base-load clean power, such as stellarator fusion
plants, would require up to five times the installed capacity and
50% increased electricity cost [104, 105].

**5.** **Reactor economics sensitivities**

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-14-0.png)

**Figure 11.** TCC per watt and COE by technology assuming a
discount rate ¯ _r_ between 3% and 7%. The cost optimal reactors are
shown with colored circular markers representing their net electric
power output. The commercial plant green circle from figures 10( _a_ )
and ( _b_ ), is represented with the stellarator fusion magenta shaded
area.

to provide net electric power. However, they operate close
to the radiative plasma density limit, and require increased
steady state _P_ aux as they do not reach ignition. _B_ peak within
all the reactors in the Pareto front seems to be insensitive to
the size of the device with values between 16 and 20 T, below
the optimization constraint of 20 T. Compact reactors operate
at lower _T_, with reduced on-axis magnetic field. The reduced
_T_ compared to the optimal 14 keV for fusion power production can be linked to maintaining high plasma density _n_ and
energy confinement time _τ_ E, under an assumed constant _β_
(equation (1)), resulting in reduced auxiliary heating power
_P_ aux and increased electric output.

Although our analysis only provides a high-level 0D outlook on the potential of compact high-field stellarators within
the limits of the technological assumptions, the result of the
cost minimization (figure 10) was overlaid with current electric plant technologies in figure 11 from published annual
world energy outlook data [83–86, 99, 100]. To account for
the uncertainty of the financial landscape and varying economics per country, the cost minimization results for the stellarator PP are also provided assuming a discount rate of ¯ _r_ = 7%

[83, 84].

Showing the TCC per watt of the stellarator reactor designs
with the corresponding COE (figure 11), we can further notice
that there is diminishing returns with plants producing more
than 2–3 GWe as the TCC per watt and COE reach asymptotic
values around 3 $ W _[−]_ [1] and 25 $ MWh _[−]_ [1] . In addition, targeting
plants around 1 GWe would allow for a competitive COE with
standard renewable energies (solar, hydro, wind _,..._ ) while
providing a TCC per watt below existing nuclear fission electric plants.

The sensitivity analysis described here identifies the reactors parameters with the highest effect on PPs economics, and
highlights target values for future research developments that
would allow for the realization of cost-effective stellarator
PPs.

To investigate the effects of the reactor configuration, and
model assumptions on the PP economics; _f_ ren, _β_, _kα_, _f_ He, _f_ m,
_b_, _η_ th, _η_ aux, auxiliary heating system unit cost and HTS unit
costs were systematically varied before conducting the costoptimization calculation described in section 4.1. Similarly,
the effects of the reactor’s geometry on the system’s economics were explored by conducting the cost-optimization with
varying fixed/constant values of _R_, _A_, _T_, _B_, and the _B_ peak constraint. For each of these sensitivity analyses, the effects on the
reactor economics (figures 12–14) were recorded through the
minimum achievable COE or minimum achievable TCC from
the Pareto front curve (figure 10).

_5.1._ _Sensitivity to plasma confinement parameters_

The parameter _f_ ren was varied between 1.0 and 2.6 to reflect the
wide range of current stellarator configurations such as W-7AS
and W7-X [24, 31, 106] as well as potential future optimized
configurations [3, 19, 32, 56, 107]. Increasing _f ren_ has a positive effect on the reactor’s economics, mostly on the minimum
TCC. Increasing _f_ ren increases the _τ_ E [ISS04] in the reactor leading

to a reduction of the required auxiliary heating power system
which reduces the reactor cost. However there are diminishing
effects on the reactor’s economics after _f_ ren exceeds 1.6–2.0.
The minimum COE has less sensitivity towards _f_ ren as reactors that achieve minimum COE tend to be large reactors with
relatively lower peak auxiliary heating power system cost.

_β_ was varied between 2% and 8% to represent the variety
of stellarator configurations [3, 33, 107, 108]. _β_ has a major
impact on the minimum COE design points, with increasing _β_
decreasing the minimum COE. We also notice limited reductions in the minimum COE with _β_ values above 4%–6%. The
effects on the minimum TCC from varying _β_ values differ
depending on the configuration’s re-normalization factor _f_ ren.
For _f_ ren _<_ 1.8, increasing _β_ increases the minimum TCC as it
increases _n_ e and the required auxiliary heating system power

**Figure 12.** Sensitivity analysis of the reactor’s minimum total capital cost TCC for varying reactor configurations ( _f_ ren, _β_, _R_, _A_, _T_, _B_ and
_B_ peak). The green marker represents the parameter value used in the cost-optimal design point selection (section 4.1). The _β_ sensitivity
analysis was carried out for varying _f_ ren values shown in varying shades of blue.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-15-0.png)

leading to increased capital cost. For _f_ ren _>_ 1 _._ 8, _β_ has little
effect on the minimum TCC as for increased _f_ ren values the
required auxiliary heating system power is reduced leading to
minimal cost increase.

The reactor design point cost-optimization was carried out
with fixed values of _R_ chosen between 3 and 8 m. In this case,
the cost-optimization algorithm only varied _B_, _A_, and _T_ in
order to minimize the reactor’s TCC and COE. This sensitivity analysis confirmed that low _R_ reactors were favorable
for reducing the TCC of fusion devices as shown in previous studies [91, 109]. In addition, there appears to be diminishing effects on the minimum TCC _R_ ⩽ 6 m. It also shows
that thanks to the increased allowable _B_ by HTS materials,
low COE reactors would not need to exceed 5–6 m in major
radius. The reactor design point cost-optimization was carried out with fixed values of _A_ chosen between 2 and 10.
Similarly to the _R_ parameter sensitivity analysis results, reducing _A_ (compact reactors) has a significant impact on lowering TCC. Interestingly, the minimum TCC was most sensitive
to changes in _A_ than _R_ . This could be explained from the fact
that reducing _A_ increases _a_ relative to _R_, increasing the plasma
volume at fixed _R_, making the reactor more compact and cost
effective. There also appears to be diminishing returns from

reducing the compactness of the reactor with _A_ ⩽ 4. _A_ has a
lower impact on the COE except for a _A <_ 3 as it reduces the
allowable _B_ due to the _B_ peak constraint (equation (20)), and
thus the resulting _P_ fus.

The reactor design point cost-optimization was carried
out with fixed values of _T_ chosen between 7 and 14 keV.
Increasing _T_ leads to increased minimum TCC but lower minimum COE. Increasing _T_ results in increased _n_ e and _B_ . This
increases _P_ fus and _P_ aux, both of which lead to higher TCC.
On the contrary, for large reactors that have low COE, the
increased _P_ fus increases the power density of the reactor, thus
reduces the COE.

The reactor design point cost-optimization was carried out
with fixed values of _B_ chosen between 5 to 15 T. Increasing
_B_ results in lower COE devices as it increases _P_ fus for fixed
reactor size, thus the power density of the reactor. For the minimum TCC, increased _B_ values leads to decreased TCC as it
allows for more compact reactors for similar _P_ fus. However,
for _B >_ 10 T, due to the _B_ peak constraint of 20 T, it leads to
larger reactors or larger _A_ values causing the minimum TCC
to increase. This means that for a given blanket thickness size,
there is a range of _B_ values, between 7 and 10 T, that minimizes
the reactor’s TCC.

The helium ash fraction _f_ He was varied from 1% to
10% to reflect the possible ash accumulation in the reactor
core depending on the alpha particle confinement times in
stellarators [110]. Additional analysis regarding helium ash
accumulation and _f_ He is presented in section 6.3. Increasing _f_ He
increases the minimum TCC, as it decreases the reaction fuel
densities, reducing _P_ fus, and increases _P_ rad leading to increased
auxiliary heating and reduced _P_ e.

_5.3._ _Sensitivity to PP parameters and efficiencies_

The blanket thickness _b_ was varied from 60 to 140 cm to reflect
the different fusion blanket configurations [15, 19, 20, 56,
111, 112] (figure 14). _b_ has a significant impact on the minimum TCC and COE as increasing _b_ reduces how compact
the reactor can be. In addition, increasing _b_ requires increased
_B_ peak, thus increased magnet costs as the coils are further away
from the plasma they need to confine. There are reducing
improvements when _b ∼_ 60 cm, as smaller _b_ also increases the
required volumetric flow rate and _P_ pump for extracting _P_ th. This
is especially the case for COE as the increased _P_ pump leads
to reduced _P_ e. In addition, further reducing _b_ will increase
the neutron damage to the reactor core components leading
to increased maintenance and replacement cost.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-16-0.png)

**Figure 13.** Sensitivity analysis of the reactor’s minimum total
capital cost TCC with varying model assumptions ( _kα_, _f_ He and _ι_ 2 _/_ 3).
The green marker represents the parameter value used in the
cost-optimal design point selection (section 4.1).

The reactor design point cost-optimization was carried out
with fixed values of peak coil magnetic field _B_ peak chosen
between 10 and 20 T. For both the COE and TCC, decreasing
the allowable _B_ peak leads to increased COE and TCC reactors.
However, the sensitivities toward _B_ peak of the reactor’s economics are low due to competing economic effects; reducing
_B_ peak reduces _P_ fus and power density of the reactor causing
the cost to increase but it also reduces the required amount of
HTS material and support structure, causing the overall cost to
decrease. Allowing for increased _B_ peak enables more compact
reactors that are less capital intensive and faster to build.

_5.2._ _Sensitivity to alpha particle parameters_

The alpha heating efficiency _kα_ was investigated for values
between 80% and 98% [11] (figure 13). Increasing _kα_ has little
effect on the reactor’s economics (TCC and COE). For plasma
configurations that achieve _fren_ ⩾ 1 _._ 2, _kα_ values of 80%–90%,
currently assumed by stellarator system studies and existing
plasma configurations [11], seem to be high enough to enable
both compact high-field reactors with low TCC and large scale
PPs with low COE. The small increase in TCC for low value
of _kα_ stems from the reduced alpha particles self-heating and
increased auxiliary heating.

The energy multiplication factor _f_ m, stemming from the tritium breeding reactions in the blanket, was varied from 1.0
to 1.5 to represent the range of potential blanket configuration
choice [15, 111, 113, 114]. _f_ m has a low effect on both the TCC
and COE, as there are competing effects from increasing _f_ m.
On the one hand, it increases _P_ e as it increases _P_ th extracted
by the flowing blanket. On the other hand, it increases the heat
load on the blanket requiring increased _P_ pump and _P_ cryo, as well
as the size of the turbine and heat rejection plant. Nonetheless,
increasing the _f_ m from 1.24 to 1.5 for the stellarator design
point described in section 6, would still decrease the TDC cost
per watt from 2.8 $ W _[−]_ [1] to 2.5 $ W _[−]_ [1] (TCC cost per watt from
5.1 to 4.8 $ W _[−]_ [1] ), and the COE from 47.7 to 44.3 $ MWh _[−]_ [1],
while increasing the TCC from 5.0 to 5.4 B$.

The thermal plant efficiency _η_ th was varied from 35%
to 70% to represent the current and possible improvements
in thermal plant such as multi-stage improved Brayton or
Rankine cycles, as well as the different operating temperatures

[20, 42, 43, 115]. Increasing _η_ th has a major impact on reducing the COE, as it increases _P_ e for the same _P_ fus. However,
increasing _η_ th could come from increasing the flowing LM
blanket operating temperatures which would have a significant impact on the piping and cooling system constraints
based on material limitations but also on the risk of increasing the plasma impurities from metal vapors produced by the
increased evaporation rates [14].

The auxiliary heating system efficiency _η_ aux was varied
from 25% to 70%, and the auxiliary system unit cost between
2 to 7 $ W _[−]_ [1] to reflect the wide range of heating system technologies (PNBI, NNBI, electron cyclotron resonant heating
(ECRH) and ion cyclotron resonant heating (ICRH)) and possible future developments [67–69]. _η_ aux had little effect on the
reactor’s economics as the reactors considered here achieve

**Figure 14.** Sensitivity analysis of the reactor’s minimum total capital cost TCC with varying reactor parameters ( _b_, _f_ m, _η_ th, _η_ aux, auxiliary
heating cost and HTS unit cost). The green marker represents the parameter value used in the cost-optimal design point selection
(section 4.1).

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-17-0.png)

high _Q_ values leading to small required heating power during
steady state operation and thus a low impact on _P_ e. However,
the auxiliary system unit cost has a major impact on the minimum TCC, as reactors achieving the minimum TCC are compact reactors that require increased auxiliary heating power
and thus high auxiliary heating system cost (figure 10).

The HTS unit cost was varied from 4 $ m _[−]_ [1] to 78 $ m _[−]_ [1]

curve shown in figures 10( _a_ ) and ( _b_ ). Both reactors are compact high-field stellarators with an estimated net electric output
of 1 GW.

A detailed analysis of Chartreuse P1 was then conducted
using the 0D system analysis (section 2) to understand the
power flow through the reactor (figure 15), the reactor start
up path using the POPCON analysis (figure 16), the helium
ash exhaust (figures 17 and 18), and a cost break down of the
PP cost accounts (figure 19).

_6.1._ _Power flow through the plant_

From the plasma and plant power balance of the Chartreuse
P1 stellarator reactor (table 3), a Sankey diagram (figure 15)
was constructed to show how the generated fusion power is
used for self-heating, extracted for thermal-to-electricity conversion and re-circulated to power the reactor auxiliary systems such as cryogenic and pumping. The power flow diagram
shown in figure 15 refers to steady state, for which the plasma
has reached ignition and the auxiliary system power has been
turned off.

For both P1 and P2, the radiative density limit constraint was not active and the electron density for both cases
remained at respectively 65% and 54% of the density limit.
Increasing the density at constant _β_ and _B_, would lead the _T_
to decrease, causing the Bremsstrahlung radiation to increase,
fusion power and net electric power to decrease.

(corresponding to 10 $ kAm _[−]_ [1] and 200 $ kAm _[−]_ [1] for typical
critical currents at the field and temperature of interest here) to
reflect the current cost of HTS tapes and possible future cost
reductions [64, 65, 91]. The HTS unit cost impacts both the
minimum TCC and COE values. The minimum TCC and COE
are linearly correlated to the HTS unit cost which is mostly due
to the linear relation between the magnet capital cost and HTS
unit cost. To achieve reactor design points that result in a TCC
below 6 B$ and a COE below 50 $ MWh _[−]_ [1], the HTS unit cost
should be decreased under 20 $ m _[−]_ [1] (50 $ kAm _[−]_ [1] for a 12 mm
wide tape).

**6.** **PP operations and cost**

Two cost optimal high-field stellarators, Chartreuse P1 and
Chartreuse P2, were designed to minimize the COE and
TCC (section 4.1), with respective HTS unit cost of 12 $ m _[−]_ [1]

(30 $ kAm _[−]_ [1] ) and 78 $ m _[−]_ [1] (200 $ kAm _[−]_ [1] ). The reactor parameters for Chartreuse P1 and P2 are shown in table 3. These
reactors were selected from the ‘elbow’ of the Pareto front

**Table 3.** Reactor parameters and cost details for two conceptual reactor design points, assuming an HTS manufacturing cost of 12 k\$am⁻¹ and 7\$.5 km⁻¹ respectively.

| | P1 | P2 |
|---|---|---|
| Configuration factor $f_{\text{cn}}$ | 1.4 | 1.4 |
| Normalized plasma pressure $\beta$ (%) | 5.0 | 5.0 |
| HTS unit cost (k\$ m⁻¹) | 12 | 7.5 |
| Major radius R (m) | 3.81 | 4.05 |
| Minor radius a (m) | 0.97 | 1.08 |
| Aspect ratio A | 4.11 | 3.75 |
| On axis magnetic field B (T) | 10.2 | 9.2 |
| Peak magnetic field $B_{\text{Peak}}$ (T) | 19.4 | 17.9 |
| Plasma temperature T (keV) | 10.2 | 10.2 |
| Blanket thickness B (cm) | 83 | 83 |
| Radiative limit ratio | 0.65 | 0.54 |
| Electron density $n_e$ (10²⁰ m⁻³) | 1.7 | 4.4 |
| Energy confinement time $\tau_E$ (s) | 0.8 | 1.8 |
| Fusion power (GW) | 1.8 | 2.2 |
| Total thermal power (GW) | 2.1 | 2.2 |
| Neutron reaction rate (10²⁰ s⁻¹) | 6.4 | 7.9 |
| Neutron wall loading (MW m⁻²) | 15.2 | 12.5 |
| NBI energy (keV) | 304 | 259 |
| Fusion Q | 3 | 4 |
| Max heating power $P_{\text{aux}}$ (MW) | 25.8 | 27.0 |
| Net electric power $P_e$ (GW) | 1.0 | 1.01 |
| Reactor core cost (B\$) | 1.5 | 2.0 |
| Total power plant cost TCC (B\$) | 4.3 | 5.5 |
| Total capital cost TCC (B\$) | 5.2 | 6.1 |
| Cost of electricity COE (c\$ kWh⁻¹) | 7.1 | 5.5 |
| Reactor core TDC cost per Watt (\$ W⁻¹) | 2.8 | 4.2[?] |
| Power plant TCC cost per Watt (\$ W⁻¹) | 5.1 | 6.1 |

[Figure 15: Sankey diagram of Chartreuse P1 reactor power flow]

[Figure 16: Plasma operating contour plot for the example stellarator reactor design point]

For this 0D analysis, the synchrotron radiation loss were not considered as a first order effect compared to other power losses. Using Trubnikov's synchrotron power loss estimates [10, 116], approximately 6 MW would be loss through synchrotron radiation compared to 48 MW of Bremsstrahlung radiation, and 245 MW of diffused power. The synchrotron power loss is accounting for larger fraction of the total power loss compared to other stellarator studies [50] but remains below 2% of the Bremsstrahlung and diffused power losses.

The overall PP efficiency defined as $\eta_{PP} = P_e / P_{\text{fus}}$ is equal to $\eta_{PP} = 57\%$ for Chartreuse P1. This overall optimistic PP efficiency results from the simplifications that were carried out in the 0D system analysis, which did not account for the electric power consumption of a series of auxiliary systems such as the tritium plant, power supplies for the magnet systems, additional coolant pumps, or vacuum pumps. These additional internal electric power requirements could amount up to 320 MW [19–21, 37, 42, 56, 115] reducing $P_e$ to 0.7 GW and the plant efficiency to $\eta_{PP} = 39\%$, similar to other reactors studies [19, 56, 115]. The reduction in $P_e$ would increase the COE to 71 \$\$ MWh⁻¹ and the TDC cost per watt to 4.2 \$ W⁻¹ and TCC cost per watt to 7.6 \$ W⁻¹.

## 6.2. Operating point and start-up path

Figure 16 shows the POPCON plot that represents the auxiliary (non-ω) heating power $P_{\text{aux}}$ to sustain a plasma of given density and temperature. The steady state operation point is

## 6.3. Helium ash accumulation $f_{He}$

The accumulation of helium ashes in the plasma can deteriorate the reactor's $P_{fus}$ and increase $P_{aux}$ as it dilutes the D-T fuel and enhances plasma-cooling losses [19, 110, 118]. $f_{He}$ was systematically varied from 2% to 10% for the selected reactor design point ($P_{out} = 27.1$ MW) and the effects on $P_{out}$, COE and required steady state $P_{aux}$ were recorded in figure 17.

Increasing $f_{He}$ reduces $P_{fus}$ and increases $P_{aux}$ and COE. Similar to other studies, we conclude that parasitic ash fraction should be minimized. With increasing $f_{He}$ for constant density operations, the reacting fuel density decreases which reduces the $P_{fus}$ and thus $P_\alpha$. Moreover, the increase in $f_{He}$ leads to an increase in $P_{rad}$ which increases $P_{aux}$ leading to further reduction of $P_\alpha$. For Charthouse P1, the auxiliary heating system is for a peak power during operation of 27.1 MW, meaning that $f_{He}$ should remain under 8.9% in order for the fusion reaction to be sustained, and under 6.6% for the $P_{out}$ to be almost null during steady state operations.

The helium ash accumulation in the plasma is modeled by carrying a particle evolution analysis assuming fusion reactions as the only source of helium particles. In addition, the alpha particle confinement time $\tau_{He}^*$ is assumed equal to which and to the energy confinement time $\tau_E$ such that $\tau_{He}^* \geq \tau_E$ [19, 25, 110, 118, 119]. Under these assumptions, the helium density fraction evolution equation can be described as:

[Figure 17: Effects of variations in helium ash fraction $f_{He}$ on Charthouse P1 output grid power $P_o$, the required steady state auxiliary power $P_{aux}$, and the corresponding cost of electricity COE]

![](images/page_019_eq_0.png)
$$\frac{df_{He}}{dt} = \left(\frac{1}{2} - f_{He}\right) \cdot n_e \langle \sigma v \rangle_{DT} / (f \cdot \bar{n}_e) - \frac{f_{He}}{\tau_{He}^*} \tag{24}$$

For P1, the helium ash accumulation analysis was conducted for ratios of $f_s = \tau_{He}^*/\tau_E$ varied between 1 and 7 to represent experimental and theoretical predictions [25, 110, 119]. For each case, the helium ash fraction time variations were recorded in figure 18.

To achieve $f_{He} > 5\%$ in the Charthouse P1 reactor, the helium particles confinement time should be $\tau_{He}^* \leq 4.0 \tau_E$. Increased values of $\tau_{He}^*$ lead to increased $f_{He}$ values which could be detrimental to the reactor's operation and output power. As shown in figure 17, for Charthouse P1, $f_{He}$ should not reach values above 6.6% to maintain plasma-related conditions leading to a maximum helium particles confinement time of $\tau_{He}^* \leq 7.7 \tau_E$ unless active helium ash removal systems are implemented.

The helium ash analysis presented here was conducted to understand the effects on the reactor's performance. More refined simulations should be carried out based on transport simulations, in order to accurately calculate $\tau_{He}^*$ and $f_{He}$.

## 6.4. Charthouse P1 cost breakdown

To further understand the economics and costing of Charthouse P1, breakdowns of the reactor's TDC main cost accounts (table 1) and the reactor core equipment's (C<sub>2</sub>) sub-accounts are shown in figure 19. The reactor core equipment is the largest contributor (50.7%) to the TDC of the P1, followed by the building's cost at 15.4% and the turbine plant cost at 13.9%. Re-purposing decommissioned fission reactors into fusion P1s could cut the cost of the fusion plant by half without considering the cost of re-purposing the fission reactor control systems.

Within the reactor core equipment, with the optimistic assumption of a HTS unit cost of 12.5 m<sup>−1</sup> (30 \$ kAm<sup>−1</sup>), the

that provides increased protection against neutron radiation

[34], without a solid first wall nor divertors, also contributes
to the reduction of the blanket and shielding sub-account cost
in the reactor core equipment compared to other stellarator
reactor studies [19, 56], for which the blanket and shielding cost amount to about 11.2% of the reactor core cost. The
effects of operating the superconducting magnets at 20 K will
also reduce the reactor core equipment cost, since the heat
transfer systems sub-cost as well as the maintenance systems
cost will be reduced, resulting in a more cost-effective PP.

For P2, the HTS unit cost assumption of 78 $ m _[−]_ [1]

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-20-0.png)

**Figure 18.** Helium ash evolution (equation (24)) within the plasma
of Chartreuse P1 for varying ratios of the helium particles
confinement time and the energy confinement time, _fτ_ _≃_ _τ_ He _[∗]_ _[/τ]_ [E][.]

**Figure 19.** Breakdown of the reactor core cost components ( _a_ ) and
the power-plant total direct cost components ( _b_ ) for the example
stellarator design point, Chartreuse P1.

heat transfer systems and equipment become the main cost
contributor, accounting for 21.0% of the reactor core direct
cost. The heat transfer systems and equipment include pumps
for all the heat transfer fluids (such as the blanket’s flowing
LM or the cryogenic fluids), motor drives, insulated pipes,
tanks, pressurized equipment, interfaces with tritium extraction, fluid clean-up systems, as well as dedicated instrumentation and metering. The magnets and their structures account
for 11.7% and 17.0% of the reactor core direct cost, respectively. The auxiliary heating system’s cost accounts for 11.1%
of the reactor core cost but becomes a major cost driver (25%
or more of the reactor core cost) for plasma configurations for
which _f_ ren _<_ 1 _._ 2 or _β <_ 3%. The use of a flowing LM blanket

(200 $ kAm _[−]_ [1] ) was used resulting in a slight larger major
radius, but lower aspect ratio, on-axis field and peak magnetic
field. In that case, the PP economics are increased by 13%–
21%. Even with this increased cost, the fusion plant could
remain competitive in respect to the other baseload electric
plants and renewable energy sources [83–86, 100]. In the P2
cost breakdown provided in appendix B (figure 26), the magnet cost would reach 33% of the reactor core direct cost, closer
to previous stellarator reactors system studies [56, 107], in
which the magnets amounted to almost half of the reactor
core direct cost. Reducing the HTS unit cost has an significant
impact on both the PP design point and its economics.

More detailed and extensive 3D analyses of the Chartreuse
P1 device and corresponding plasma configurations [9] are
necessary to refine the reactor parameters (major radius R,
aspect ratio A, on-axis magnetic field B _..._ ) but this initial
0D high-level system analysis provide preliminary insights on
potential high-field compact stellarators.

**7.** **Burning plasma experimental stellarator design**
**points**

The 0D reactor system analysis (section 2) was applied to
explore the physics, engineering and economics landscape
of burning plasma (fusion gain _Q_ ⩾ 1) experimental fusion
stellarator reactors based on HTS magnets and flowing LM
blankets.

_7.1._ _Minimizing reactor cost for varying fusion gain targets_

In this section, high-field compact burning plasma experimental stellarator reactors that minimize the reactor core cost
_C_ 22 were investigated by varying target fusion gain values
from _Q_ = 1 to _Q_ = 10. The reactor design point optimization
process presented in section 4.1 was modified to minimize the
reactor core cost _C_ 22 (table 1), and maximize the target fusion
gain value Q, with the added constraint of 1 ⩽ _Q_ ⩽ 10. _C_ 22 was
considered here instead of TCC as the burning plasma experiment will aim at validating the high-field compact stellarator
core technologies and will not aim at producing net electricity. Since there will be no electricity production, there will
be fewer systems compared to a PP (no turbine nor electric
plant), leading to reduced land footprint and facilities’ costs
(table 1).

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-20-1.png)

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-21-0.png)

**Figure 20.** Pareto fronts of the optimal reactors in terms of fusion
gain and reactor core cost, for three assumed blanket thicknesses,
_b_ = 10, 20 and 41 cm. Each marker represents an optimal reactor
and the color of the marker represents the thermal flux _P_ fus _/S_ plasma.
The arrows indicate how the stellarator characteristics change along
the Pareto front.

The HTS unit cost of 12 $ m _[−]_ [1] (30 $ kAm _[−]_ [1] ) was assumed
here as well as three blanket thicknesses were considered:
half-sized blanket compared to Chartreuse P (section 2.4), a
quarter-sized blanket, and an eighth-size blanket to assess the
potential cost savings of reducing the blanket thickness for
burning plasma experiments as lower neutron flux, and shorter
run times are expected in line with the neutronics simulations
results [34, 96]. In addition, the analysis was also conducted assuming catalyzed deuterium–deuterium (D–D) as reaction fuel to investigate the cost-saving from conducting a D–D
experiment for which the D-T equivalent fusion gain _Q_ would
be assessed. Lastly, _β_ = 1% was chosen for the burning plasma
experiment cost optimization and blanket thickness investigation, in order to minimize _P_ [max] aux [and further reduce the cost of]

the device as explained further in section 7.2.

For each assumed blanket thickness and for each target
fusion gain _Q_, the reactors that minimized _C_ 22 are represented in figure 20. The device parameters, as well as the reactor
characteristics for the family of burning plasma experiment
reactors with the blanket thickness of 41 cm width and varying
fusion gain values, are explored in appendix C (figure 27). A
burning plasma experiment of higher fusion gain has higher
core cost _C_ 22, and thermal flux _P_ fus _/S_ plasma. In addition, a
reduced blanket thickness increased thermal flux but reduced
reactor core cost _C_ 22 as higher _B_ can be achieved with smaller
_R_ . Interestingly, there is a cost asymptote for high fusion gains,
which means that increasing the fusion gain target from _Q_ = 4
to _Q_ = 10 has a minor impact on the reactor core cost _C_ 22.
However, to achieve higher fusion gain values Q, the reactor
major radius, on-axis magnetic field, and plasma temperature
have to be increased (figure 27).

A reactor with _R_ = 3.82 m, _B_ = 10.9 T, _T_ = 6.9 keV, and
_A_ = 3.5 would achieve a fusion gain of _Q_ = 10 while

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-21-1.png)

We also investigated the effect of varying _β_ on the reactor core
cost _C_ 22, as for a _β_ value of 5% similarly to Chartreuse P, the
heating system cost contributed the almost half of the _C_ 22 cost
for burning plasma experiments. Reducing _β_ should reduce
the plasma density and the required _P_ [max] aux [to sustain the fusion]

reactions (equations (1) and (6)). Similarly to section 7.1, the
burning plasma experiment’s design parameters were varied
for each value of _β_ with a fixed blanket thickness ( _b_ = 41 cm)
so as to minimize _C_ 22 and _Q_ .

Figure 21, represents the heating power _P_ [max] aux [of the design]

points that minimize the reactor core cost _C_ 22 for varying
target _Q_ values and for _β_ = 1%, 3%, and 5%. Reducing _β_ results in a lower reactor cost while achieving the same _Q_ values. For lower _β_ values, the plasma density is reduced leading to lower _P_ aux, thus _P_ fus to achieve the same _Q_ value. The
burning plasma experiment optimal devices for _β_ = 5% all

**Figure 21.** Sensitivity analysis on the reactor core cost for varying
normalized plasma pressure _β_ parameters. Each marker represents
the minimum cost reactor for a given fusion gain (similar to
figure 20) for varying _β_ values of 1.0%, 3%, and 5.0%. Here the
peak auxiliary heating power _P_ [max] aux [for each design point is shown]

along with the reactor core cost, and the color coding represents the
reactor’s fusion gain.

minimizing the reactor core cost _C_ 22 with a thermal flux
_P_ fus _/S_ plasma = 0 _._ 5 MW m _[−]_ [2] . The device parameters of optimal
burning plasma experiments (figure 27) show that in order to
minimize cost, it is necessary to aim for compact reactors with
low magnetic fields, but also to minimize the peak auxiliary
heating power _P_ [max] aux [as most of the devices on the Pareto front]

display similarly low values of heating power. Reducing the
cost of the plasma heating system or the blanket thickness
could lead to further cost reductions but might represent a
major technical and engineering challenge.

_7.2._ _Burning plasma experiment economic sensitivity to β_

**Table 4.** Reactor parameters, characteristics and cost details for three conceptual burning plasma experiment design points, assuming $\beta$ values of 1.0%, 3.0%, and 5.0% respectively.

| | X1 | X2 | X3 |
|---|---|---|---|
| Norm. plasma pressure $\beta$ (%) | 1.0 | 3.0 | 5.0 |
| Major radius R (m) | 3.82 | 3.13 | 2.84 |
| Minor radius a (m) | 1.08 | 1.04 | 0.94 |
| Aspect ratio A | 3.5 | 3.0 | 3.0 |
| On-axis magnetic field B (T) | 10.9 | 8.8 | 8.5 |
| Peak magnetic field $B_{\text{BCS}}$ (T) | 18.3 | 17.6 | 16.9 |
| Plasma temperature T (keV) | 6.9 | 6.9 | 8.9 |
| Blanket thickness b (cm) | 41 | 41 | 41 |
| Configuration factor $f_{\text{on}}$ | 1.4 | 1.4 | 1.4 |
| Radiative limit ratio | 0.97 | 0.96 | 0.98 |
| Electron density $n_e$ ($10^{20}$ m$^{-3}$) | 2.1 | 4.2 | 6.5 |
| Energy confinement time $\tau_E$ (s) | 3.22 | 1.6 | 1.0 |
| Fusion power (MW) | 93 | 272 | 485 |
| Neutron production rate ($10^{19}$ s$^{-1}$) | 3.2 | 9.5 | 17 |
| Neutron wall loading (MW m$^{-2}$) | 0.7 | 2.7 | 5.9 |
| NBI energy (keV) | 105 | 228 | 338 |
| Plasma gain Q | 10 | 40 | 10 |
| Peak heating power $P_{\text{aux}}^{\text{max}}$ (MW) | 9 | 27 | 48 |
| Relative cost (IBS) | 1.0 | 0.67 | 0.88 |
| Total power-plant cost TDC (B\$) | 0.9 | 1.2 | 1.6 |

[Figure 22: Sankey diagram of the burning plasma experimental reactor, Chartreuse X2, power flow]

require high $P_{\text{aux}}^{\text{max}}$ between 45-65 MW. With the auxiliary system power unit cost of 6.215 W$^{-1}$, these required $P_{\text{aux}}$ values have a major impact on the reactor core cost, amounting to 280-405 M\$. Reducing the required $P_{\text{aux}}$ has a significant impact on the device's cost. This impact of lower $\beta$ values for the burning plasma experiment led us to consider $\beta = 1\%$ for section 7.1.

For $\beta = 1\%$, 3%, and 5%, the burning plasma experiment parameters that minimize $C_n$ for $Q = 10$ are shown in table 4. While reducing $\beta$ reduces the required auxiliary heating power and cost, it leads to increased R and A. In this particular case, a compact device with high normalized plasma pressure value would prove more expensive to build than a larger device with lower $\beta$. However, for the burning plasma experiment scenario, a more refined cost analysis that includes more specific assembly, manufacturing, procurement, and logistics considerations might increase the cost for larger devices. Similarly, the construction of the larger experimental devices would likely take longer and increase the indirect costs. A trade-off between reactor size and required heating power could be made with a $\beta = 3\%$ device.

## T3. Chartreuse X2 power flow and operation point

The power flow analysis through the burning plasma experiment, start-up time analysis, and helium ash accumulation calculations were carried out for Chartreuse X2 ($\beta = 3\%$) as a case study.

Figure 22 represents the power flow through the burning plasma experiment, X2. In this case, there would be no heat to electricity conversion plant and thus no electricity generation. The electric power required to power the experiment's auxiliary systems is depicted as an input power flow accounting for 95 MW. For this D-D analysis, the synchrotron radiation loss were not considered as a first order effect compared to other power losses. Approximately 1.2 MW would be loss

for X2 through synchrotron radiation [30, 116] compared to
18 MW of Bremsstrahlung radiation, and 57 MW of diffused
power remaining below 2% of the Bremsstrahlung and diffused power losses.
From the POPCON analysis of X2, _P_ [max] aux [also corresponds]
to the required steady state auxiliary heating power _P_ aux.
Similarly to Chartreuse P, the X2 auxiliary heating system
sized to be _P_ [sys] aux [=][ 1] _[.]_ [05] _[ ·][ P]_ [max] aux [,] [or] _[P]_ [sys] aux [=][ 28 MW,] [would] [lead]
to a start-up time for steady state operation of _τ_ start = 15 s.
For the helium ash fraction to remain below _f_ He _<_ 5%,
the helium particles confinement time should remain under
_τ_ He _[∗]_ _[<]_ [ 9] _[ τ]_ [E][. In the case of a lower] _[ τ][ ∗]_ He [, the required] _[ P]_ [aux][ would]
be lower and the achieved _Q_ higher. For _τ_ He _[∗]_ _[≃]_ [5] _[τ]_ [E] [similar to]
other advanced reactors [110], the helium ash fraction would
reduce to _f_ He _≃_ 3%, leading to a peak auxiliary power of
_P_ [max] aux [=][ 22] _[.]_ [1 MW,] [and] [fusion] [power] [of] _[P]_ [fus] [=][ 297 MW,] [thus]
resulting in an increased fusion gain of _Q_ = 13.4.

**8.** **Discussion and conclusion**

The 0D physics, engineering, and economical system study
for high-field compact stellarators presented here provides a
framework to investigate, at a high-level, a wide range of
reactor design points and highlight possible directions for
research developments. The costing model provided an understanding of the required trade-offs to achieve PPs that minimize TCC and COE. (section 4). The use of HTS magnets enabling higher magnetic fields _B_, and flowing liquid
metal walls ensuring a protection against high heat and neutron fluxes within a thin blanket thickness expand the design
space towards compact high field devices. A stellarator PP
of aspect ratio _A_ = 4.1, _R_ = 3.8 m, _B_ = 10.2 T, _T_ = 10.2 keV,
and _β_ = 5% minimizes both the COE and TCC, at values of
47.5 $ MWh _[−]_ [1] and 5.2 B$ while achieving 1 GWe.
Similarly, a next-step burning plasma stellarator experiment of aspect ratio _A_ = 3.0, _R_ = 3.1 m, _B_ = 8.8 T,
_T_ = 6.9 keV, and _β_ = 3% could achieve a fusion gain _Q_ = 10
while minimizing the reactor core cost _C_ 22 to 670 M$
(section 7).
The economic sensitivity analysis described in section 5,
highlighted the parameters with the highest effects on the
reactor economics. To reduce the reactor TCC, improving the
confinement properties ( _f_ ren) would have the most impact up to
_f_ ren _≃_ 1 _._ 8, followed by reducing the blanket thickness, developing advanced compact _A_ plasma configurations, between 3
and 4.0, with _R_ between 3 and 5 m and _B_ between 7 and 10 T,
and lastly minimizing the HTS unit cost and auxiliary heating
system’s cost.
The 0D model developed in this work relies on an extensive
number of technological assumptions (high NWL, HTS performance and coil architecture, etc.) and simplifications that
limit the generalization of the results. The 0D simplifications
neglect the effects of temperature, density, and pressure profiles in the plasma, coil geometries, as well as the stellarator
plasma shape (such as elongation, triangularity or field periods). A 1D analysis would improve the accuracy of the results
as it has been shown that the 0D simplifications can lead to

an over-estimation of the Bremsstrahlung radiation over the
fusion power, thus the required auxiliary heating power [4,
25]. This means that the 0D analysis also over-estimates the
required on-axis magnetic field for a target fusion gain (15%
overestimation of _B_ according to Alonso _et al_ [25]). In addition, the current study relies on scaling laws for both the energy
confinement time which could be improved by the use of transport codes [31, 121–123]. Similarly, the cost models used in
the study relies on costing power laws developed in the late
1990s and early 2000s which might not reflect the current cost
of both raw materials nor services [54, 55, 58]. Many reactor
component costs were based on the raw material unit costs
with few considerations [21, 42, 54, 56] on the manufacturing,
procurement, maintenance scheme [124–126] and assembly
costs.
Future work will focus on iterating the design points with
physics plasma configuration analyses, and refined engineering models allowing for more accurate plasma parameters and
engineering assumptions that would be then fed to the 0D
system analysis (inboard clearance, magnetic field peaking
factor, NWL limits, alpha confinement times, etc). In addition
emphasis will be put on refining the stellarator system study by
carrying a 1D analysis using temperature, density and pressure
profiles; including neutronics and transport simulations; and
refining the costing structure with more detailed component
list within the PP along with their current procurement cost.

**Acknowledgments**

The authors would like to thank Carlo Sborchia, Achilleas
Evangelias, Chris Smiet and Julien Fausty at Renaissance
Fusion, Felix Warmer at TUE, Jorrit Lion at IPP, and Clara
Cottet at the UKAEA for their feedback on this work.

**Appendix A.** **Investigation of the effect of increased**
**on-axis to peak coil magnetic field ratio**

Stellarator coil architectures ranging from helical structures

[56] and non-planar modular coils [8], to novel architectures
of wide engraved HTS technologies [6, 7], can have a major
effect on the resulting peak magnetic field strength at the coils
for a given target on-axis field. For this reason a varying magnetic field peaking factor _k_ peak = 1 _,_ 1 _._ 2 _,_ and 1.5 as defined
in equation (20) was explored to understand its effect on the
optimal design points.
Pareto optimal designs in terms of both COE, and TCC,
obtained for varying reactor parameters ( _B_, _R_, _T_, _A_ ), following the process described in section 4.1, are presented below
(figure 23). The design points lying at the ‘elbow’ of the Pareto
front curves (figure 23) and achieving _P_ e = 1 GW are highlighted in table 5.
Increasing the peaking factor leads to less advantageous
design points in terms of economics with both higher COE and
TCC costs on the Pareto optimal fronts (figure 23). Increasing
the peaking factors leads to increased major radii, and aspect
ratios, along with reduced on-axis field in order to maintain

[Figure 23: Pareto fronts of the optimal design points in terms of cost of electricity (COE) and capital cost (TCC) with varying magnetic field peaking factor $k_\text{peak} = 1, 1.2$, and $1.5$ as defined in equation (20). Increasing peak factors are shown with increasing transparency. Each marker represents an optimal plant and the color of the marker represents the plant's net electric power ($P_e$).]

**Table 5.** Reactor parameters and cost details for three Pareto optimal conceptual reactor design points corresponding to peaking factor of $k_\text{peak} = 1, 1.2$, and $1.5$ respectively.

| Peaking factor $k_\text{peak}$ | 1 | 1.2 | 1.5 |
|---|---|---|---|
| Configuration factor $f_\text{con}$ | 1.4 | 1.4 | 1.4 |
| Normalized plasma pressure $\beta$ (%) | 5.0 | 5.0 | 5.0 |
| HTS unit cost ($\text{k m}^{-1}$) | 12 | 12 | 12 |
| Major radius $R$ (m) | 3.81 | 4.32 | 5.02 |
| Minor radius $a$ (m) | 0.95 | 1.03 | 1.07 |
| Aspect ratio $A$ | 4.11 | 4.19 | 4.71 |
| On-axis magnetic field $B$ (T) | 9.4 | 9.4 | 8.9 |
| Peak magnetic field $B_\text{max}$ (T) | 19.4 | 19.8 | 20.6 |
| Plasma temperature $T$ (keV) | 10.2 | 10.4 | 10.2 |
| Blanket thickness $b$ (cm) | 85 | 85 | 83 |
| Radiative limit $\text{ratio}$ | 0.65 | 0.65 | 0.67 |
| Electron density $n_e$ ($10^{20}$ m$^{-3}$) | 6.3 | 5.3 | 4.9 |
| Energy confinement time $\tau_E$ (s) | 0.8 | 0.9 | 1.0 |
| Fusion power (GW) | 2.0 | 2.0 | 2.1 |
| Total thermal power (GW) | 2.1 | 2.2 | 2.2 |
| Neutron reaction rate ($10^{18}$ s$^{-1}$) | 6.4 | 6.4 | 6.4 |
| Neutron wall loading (MW m$^{-2}$) | 15.2 | 12.1 | 10.0 |
| NBI energy (keV) | 304 | 253 | 264 |
| Fusion gain $Q$ | $\infty$ | $\infty$ | $\infty$ |
| Max heating power $P_\text{aux}$ (MW) | 25.8 | 27.5 | 34.5 |
| Net electric power $P_e$ (GW) | 1.01 | 1.00 | 1.02 |
| Reactor core cost (B\$) | 1.5 | 1.6 | 1.9 |
| Total power plant cost TDC (B\$) | 4.7 | 5.0 | 5.4 |
| Total capital cost TCC (B\$) | 5.2 | 5.5 | 6.2 |
| Cost of electricity COE (\$MWh$^{-1}$) | 47.5 | 49.6 | 55.7 |
| Reactor core TDC cost per Watt (\$W$^{-1}$) | 1.5 | 1.6 | 1.9 |
| Power plant TCC cost per Watt (\$W$^{-1}$) | 5.1 | 5.4 | 6.1 |

**Figure 24.** Sankey diagram of the power flow through the minimum TCC reactor in the Pareto front shown in figure 10.

**Figure 25.** Sankey diagram of the power flow through the minimum COE reactor in the Pareto front shown in figure 10.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-25-0.png)

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-25-1.png)

the peak field at the coils below the 20 T threshold. The
most stringent peaking factor _k_ peak = 1 _._ 5 which corresponds
to standard non-planar modular coils [8, 19] would still lead
to a relatively compact high-field design point with _R_ = 5.0 m,
_A_ = 4.7, _B_ = 8.9 T. The increased in overall PP cost highly
motivates the development of novel coil architectures with
reduced peaking factors.

**Appendix B.** **Additional power plant and burning**
**plasma design points of interests**

A specific case study was conducted in section 6 on Chartreuse
P1, an identified stellarator power plant design that would
minimize both the COE and TCC. In this study, additional
design of interests were highlighted throughout the analyses;
a first of kind power plant design that would minimize the
TCC (figure 10), a large power plant that would minimize the
COE (figure 10), an alternative power plant design (Chartreuse
P2) based on increased HTS unit cost (section 6), as well as
varying burning plasma experiments based on varying normalized plasma pressure values _β_ (section 7.2). The power flow
Sankey diagram are illustrated here for the FOAK and COE
minimizing power plants (figures 24 and 25).

The FOAK design point could be: _B_ = 7.5 T, _R_ = 3.8 m,
_T_ = 7.7 keV, and _A_ = 3.1 and generate 0.7 GW of fusion power
and 0.3 GW of electricity at 100 $ MWh _[−]_ [1] for a TCC of

3.5 B$. This device has characteristics similar to Chartreuse
X1, meaning that a combined burning plasma experiment and
first of kind device could be although with varying operation plans, _β_ = 1% up to _β_ = 5%. The large PP minimizing the COE (figure 10) appears an unlikely design points
with un-plausible large dimensions: _B_ = 13 T, _R_ = 6.3 m,
_T_ = 13.1 keV, and _A_ = 6.9 and generate 8.3 GW of fusion
power and 4.4 GW of electricity at 22 $ MWh _[−]_ [1] for a TCC
of 12 B$.

In addition, the cost breakdown for the various burning plasma experiments (X1–X3) and chosen power plant
designs (Chartreuse P1 and P2) is also shown her in
figure 26.

**Appendix C.** _**β**_ **= 1% burning plasma design points**
**parameters**

The device parameters, as well as the reactor characteristics
for the family of Pareto optimal burning plasma experiment
reactors for _β_ = 1% with the blanket thickness of 41 cm width
and varying fusion gain values, are shown in figure 27. The
device parameters show relatively similar devices suggesting
that to achieve _Q_ values from 1 to 10, a single cost-effective
reactor of major radius _R ∼_ 3 _._ 4 with aspect ratio of _A_ = 3.4,
heating power _P_ [max] aux _[∼]_ [10 MW] [and] [varying] _[B]_ [from] [8] [to] [11 T]

could be used.

**Figure 26.** Cost comparison of the reactor design points considered in this study Chartreuse X1-3 and Chartreuse P1-2.

**Figure 27.** Stellarator reactor’s characteristics of each optimal reactor along the Pareto front shown in figure 20 for a blanket thickness of
_b_ = 41 cm, and _β_ = 1.0. The reactors’ parameters ( _B_, _R_, _T_, _A_ ) along several reactors characteristics are shown here. Each marker represents
an optimal reactor resulting from minimizing the reactor core cost _C_ 22 for a target fusion gain value _Q_ . For the the electron density plot,
markers with light blue colors represent the corresponding radiative density limit for each reactor design point.

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-26-0.png)

![](images/Prost_2024_Nucl._Fusion_64_026007.pdf-26-1.png)

**ORCID iDs**

[Victor Prost ](https://orcid.org/0000-0002-1680-5108) [https://orcid.org/0000-0002-1680-5108](https://orcid.org/0000-0002-1680-5108)
[Francesco A. Volpe ](https://orcid.org/0000-0002-7193-7090) [https://orcid.org/0000-0002-7193-](https://orcid.org/0000-0002-7193-7090)
[7090](https://orcid.org/0000-0002-7193-7090)

**References**

[1] Dinklage A. _et al_ 2018 Magnetic configuration effects on the
Wendelstein 7-X stellarator _Nat. Phys._ **[14](https://doi.org/10.1038/s41567-018-0141-9)** [855–60](https://doi.org/10.1038/s41567-018-0141-9)

[2] Gates D.A. _et al_ 2018 Stellarator research opportunities: a
report of the National Stellarator Coordinating Committee
_J. Fusion Energy_ **[37](https://doi.org/10.1007/s10894-018-0152-7)** [51–94](https://doi.org/10.1007/s10894-018-0152-7)

[3] Sagara A., Igitkhanov Y. and Najmabadi F. 2010 Review of
stellarator/heliotron design issues towards MFE DEMO
_Fusion Eng. Des._ **[85](https://doi.org/10.1016/j.fusengdes.2010.03.041)** [1336–41](https://doi.org/10.1016/j.fusengdes.2010.03.041)

[4] Lion J., Warmer F., Wang H., Beidler C., Muldrew S. and
Wolf R. 2021 A general stellarator version of the systems
code PROCESS _Nucl. Fusion_ **[61](https://doi.org/10.1088/1741-4326/ac2dbf)** [126021](https://doi.org/10.1088/1741-4326/ac2dbf)

[5] Cho A. 2021 This powerful electromagnet could help make
fusion energy a reality _Science_ [1–5](https://doi.org/10.1126/science.acx9064)

[6] Volpe F.A. 2023 _Renaissance Fusion Technologies_ (available
[at: https://renfusion.eu/technology) (Accessed 1 October](https://renfusion.eu/technology)
2023)

[7] Pereira Bothelo D. and Volpe F.A. 2023 Considerations for
the development of neutral beam injection for fusion
reactors or demo _IAEA 5th Technical Meeting on Fusion_
_Data Processing, Validation and Analysis_ (IAEA)
[(available at: https://conferences.iaea.org/event/346/](https://conferences.iaea.org/event/346/contributions/27299/)
[contributions/27299/) (Accessed 1 December 2023)](https://conferences.iaea.org/event/346/contributions/27299/)

[8] Erckmann V. _et al_ 1997 The W7-X project: scientific basis
and technical realization _17th IEEE/NPSS Symp. Fusion_
_Engineering (Cat. No. 97CH36131)_ [vol 1 (IEEE) pp 40–48](https://doi.org/10.1109/FUSION.1997.685662)

[9] Evangelias A. and Volpe F.A. 2023 Compact equilibrium
configurations for next-step HTS stellarators _49th_
_European Conf. on Plasma Physics Proc._ (EPS)

[10] Jorge R. and Landreman M. 2020 The use of near-axis
magnetic fields for stellarator turbulence simulations
_Plasma Phys. Control. Fusion_ **[63](https://doi.org/10.1088/1361-6587/abc862)** [014001](https://doi.org/10.1088/1361-6587/abc862)

[11] Landreman M. and Paul E. 2022 Magnetic fields with precise
quasisymmetry for plasma confinement _Phys. Rev. Lett._
**[128](https://doi.org/10.1103/PhysRevLett.128.035001)** [035001](https://doi.org/10.1103/PhysRevLett.128.035001)

[12] Castro A., Moynihan C., Stemmley S., Szott M. and
Ruzic D.N. 2021 Lithium, a path to make fusion energy
affordable _Phys. Plasmas_ **[28](https://doi.org/10.1063/5.0042437)** [050901](https://doi.org/10.1063/5.0042437)

[13] You J. _et al_ 2021 High-heat-flux technologies for the
European demo divertor targets: state-of-the-art and a
review of the latest testing campaign _J. Nucl. Mater._
**[544](https://doi.org/10.1016/j.jnucmat.2020.152670)** [152670](https://doi.org/10.1016/j.jnucmat.2020.152670)

[14] Morgan T., Rindt P., Van Eden G., Kvon V., Jaworksi M. and
Cardozo N.L. 2017 Liquid metals as a divertor
plasma-facing material explored using the Pilot-PSI and
Magnum-PSI linear devices _Plasma Phys. Control. Fusion_
**[60](https://doi.org/10.1088/1361-6587/aa86cd)** [014025](https://doi.org/10.1088/1361-6587/aa86cd)

[15] Abdou M.A. _et al_ 2001 On the exploration of innovative
concepts for fusion chamber technology _Fusion Eng. Des._
**[54](https://doi.org/10.1016/S0920-3796(00)00433-6)** [181–247](https://doi.org/10.1016/S0920-3796(00)00433-6)

[16] Smolentsev S. 2021 Design window for open-surface lithium
divertor with helium-cooled substrate _Fusion Eng. Des._
**[173](https://doi.org/10.1016/j.fusengdes.2021.112930)** [112930](https://doi.org/10.1016/j.fusengdes.2021.112930)

[17] Fisher A., Sun Z. and Kolemen E. 2020 Liquid metal
“divertorlets” concept for fusion reactors _Nucl. Mater._
_Energy_ **[25](https://doi.org/10.1016/j.nme.2020.100855)** [100855](https://doi.org/10.1016/j.nme.2020.100855)

[18] Igitkhanov Y., Andreeva T., Beidler C., Harmeyer E.,
Herrnegger F., Kisslinger J., Wagner F. and Wobig H.

2006 Status of HELIAS reactor studies _Fusion Eng. Des._
**[81](https://doi.org/10.1016/j.fusengdes.2006.07.049)** [2695–702](https://doi.org/10.1016/j.fusengdes.2006.07.049)

[19] Lyon J., Ku L., El-Guebaly L., Bromberg L., Waganer L. and
Zarnstorff M. (ARIES-CS Team) 2008 Systems studies
and optimization of the ARIES-CS power plant _Fusion_
_Sci. Technol._ **[54](https://doi.org/10.13182/FST54-694)** [694–724](https://doi.org/10.13182/FST54-694)

[20] Najmabadi F. _et al_ 2008 The ARIES-CS compact stellarator
fusion power plant _Fusion Sci. Technol._ **[54](https://doi.org/10.13182/FST54-655)** [655–72](https://doi.org/10.13182/FST54-655)

[21] Kovari M., Kemp R., Lux H., Knight P., Morris J. and
Ward D. 2014 “PROCESS”: a systems code for fusion
power plants—part 1: physics _Fusion Eng. Des._
**[89](https://doi.org/10.1016/j.fusengdes.2014.09.018)** [3054–69](https://doi.org/10.1016/j.fusengdes.2014.09.018)

[22] Hartmann T. 2013 Development of a modular systems code
to analyse the implications of physics assumptions on the
design of a demonstration fusion power plant _Thesis_
Technische Univ. Muenchen (Germany) (available at:
[https://inis.iaea.org/search/search.aspx?orig_q=RN:](https://inis.iaea.org/search/search.aspx?orig_q=RN:45031642)
[45031642)](https://inis.iaea.org/search/search.aspx?orig_q=RN:45031642)

[23] Coleman M. and McIntosh S. 2019 BLUEPRINT: a novel
approach to fusion reactor design _Fusion Eng. Des._
**[139](https://doi.org/10.1016/j.fusengdes.2018.12.036)** [26–38](https://doi.org/10.1016/j.fusengdes.2018.12.036)

[24] Yamada H. _et al_ 2005 Characterization of energy
confinement in net-current free plasmas using the extended
International Stellarator Database _Nucl. Fusion_ **[45](https://doi.org/10.1088/0029-5515/45/12/024)** [1684](https://doi.org/10.1088/0029-5515/45/12/024)

[25] Alonso J., Calvo I., Carralero D., Velasco J.,
García-Rega˜na J., Palermo I. and Rapisarda D. 2022
Physics design point of high-field stellarator reactors _Nucl._
_Fusion_ **[62](https://doi.org/10.1088/1741-4326/ac49ac)** [036024](https://doi.org/10.1088/1741-4326/ac49ac)

[26] Giannone L. _et al_ 2000 Physics of the density limit in the
W7-AS stellarator _Plasma Phys. Control. Fusion_ **[42](https://doi.org/10.1088/0741-3335/42/6/301)** [603](https://doi.org/10.1088/0741-3335/42/6/301)

[27] Fuchert G. _et al_ 2020 Increasing the density in Wendelstein
7-X: benefits and limitations _Nucl. Fusion_ **[60](https://doi.org/10.1088/1741-4326/ab6d40)** [036020](https://doi.org/10.1088/1741-4326/ab6d40)

[28] Miyazawa J. _et al_ 2008 Density limit study focusing on the
edge plasma parameters in LHD _Nucl. Fusion_ **[48](https://doi.org/10.1088/0029-5515/48/1/015003)** [015003](https://doi.org/10.1088/0029-5515/48/1/015003)

[29] Bosch H.-S. and Hale G. 1992 Improved formulas for fusion
cross-sections and thermal reactivities _Nucl. Fusion_
**[32](https://doi.org/10.1088/0029-5515/32/4/I07)** [611](https://doi.org/10.1088/0029-5515/32/4/I07)

[30] Trubnikov B. 1979 Universal coefficients for synchrotron
emission from plasma configurations _Rev. Plasma Phys._
**7** 345–79

[31] Turkin Y., Beidler C., Maaßberg H., Murakami S.,
Tribaldos V. and Wakasa A. 2011 Neoclassical transport
simulations for stellarators _Phys. Plasmas_ **[18](https://doi.org/10.1063/1.3553025)** [022505](https://doi.org/10.1063/1.3553025)

[32] Warmer F., Beidler C.D., Dinklage A., Turkin Y. and Wolf R.
2015 Limits of confinement enhancement for stellarators
_Fusion Sci. Technol._ **[68](https://doi.org/10.13182/FST15-131)** [727–40](https://doi.org/10.13182/FST15-131)

[33] Beidler C. _et al_ 2001 The helias reactor HSR4/18 _Nucl._
_Fusion_ **[41](https://doi.org/10.1088/0029-5515/41/12/303)** [1759](https://doi.org/10.1088/0029-5515/41/12/303)

[34] Prost V. and Volpe F.A. 2023 Compact fusion blanket using
plasma-facing liquid Li-LiHwalls and Pb pebbles _30th_
_IEEE Symp. on Fusion Engineering_ ( _Oxford, UK_, _9–13_
_July 2023_ [) (IEEE) (available at: https://sofe2023.co.uk/)](https://sofe2023.co.uk/)

[35] Rubel M. 2019 Fusion neutrons: tritium breeding and impact
on wall materials and components of diagnostic systems _J._
_Fusion Energy_ **[38](https://doi.org/10.1007/s10894-018-0182-1)** [315–29](https://doi.org/10.1007/s10894-018-0182-1)

[36] Freidberg J., Mangiarotti F. and Minervini J. 2015 Designing
a tokamak fusion reactor—how does plasma physics fit
in? _Phys. Plasmas_ **[22](https://doi.org/10.1063/1.4923266)** [070901](https://doi.org/10.1063/1.4923266)

[37] Schoofs F. and Todd T. 2022 Magnetic field and power
consumption constraints for compact spherical tokamak
power plants _Fusion Eng. Des._ **[176](https://doi.org/10.1016/j.fusengdes.2022.113022)** [113022](https://doi.org/10.1016/j.fusengdes.2022.113022)

[38] Melchiorri L., Narcisi V., Giannetti F., Caruso G. and
Tassone A. 2021 Development of a RELAP5/MOD3. 3
module for MHD pressure drop analysis in liquid metals
loops: verification and validation _Energies_ **[14](https://doi.org/10.3390/en14175538)** [5538](https://doi.org/10.3390/en14175538)

[39] Franza F. 2019 Development and validation of a
computational tool for fusion reactors’ system analysis
_PhD Thesis_ Karlsruher Institut für Technologie (KIT)

[40] Wenninger R. _et al_ 2017 The DEMO wall load challenge
_Nucl. Fusion_ **[57](https://doi.org/10.1088/1741-4326/aa4fb4)** [046002](https://doi.org/10.1088/1741-4326/aa4fb4)

[41] Bustreo C., Casini G., Zollino G., Bolzonella T. and
Piovan R. 2013 FRESCO, a simplified code for cost
analysis of fusion power plants _Fusion Eng. Des._
**[88](https://doi.org/10.1016/j.fusengdes.2013.09.005)** [3141–51](https://doi.org/10.1016/j.fusengdes.2013.09.005)

[42] Dragojlovic Z., Raffray A.R., Najmabadi F., Kessel C.,
Waganer L., El-Guebaly L. and Bromberg L. 2010 An
advanced computational algorithm for systems analysis of
tokamak power plants _Fusion Eng. Des._ **[85](https://doi.org/10.1016/j.fusengdes.2010.02.015)** [243–65](https://doi.org/10.1016/j.fusengdes.2010.02.015)

[43] Wright S.A., Vernon M.E. and Pickard P.S. 2006 Concept
design for a high temperature helium brayton cycle
with interstage heating and cooling _Sandia Report_
[SAND2006-4147 (Sandia National Laboratories) (https://](https://doi.org/10.2172/1323907)
[doi.org/10.2172/1323907)](https://doi.org/10.2172/1323907)

[44] Fam`a F.R., Loreti G., Calabr`o G., Ubertini S., Volpe F.A. and
Facci A.L. 2023 An optimized power conversion system
for a stellarator-based nuclear fusion power plant _Energy_
_Convers. Manage._ **[276](https://doi.org/10.1016/j.enconman.2022.116572)** [116572](https://doi.org/10.1016/j.enconman.2022.116572)

[45] Polzin K.A. 2007 _Liquid-metal pump technologies for_
_nuclear surface power_ NASA/TM-2007-214851 NASA

[46] Hvasta M., Nollet W. and Anderson M. 2018 Designing
moving magnet pumps for high-temperature, liquid-metal
systems _Nucl. Eng. Des._ **[327](https://doi.org/10.1016/j.nucengdes.2017.11.004)** [228–37](https://doi.org/10.1016/j.nucengdes.2017.11.004)

[47] Bucenieks I. 2000 Perspectives of using rotating permanent
magnets for electromagnetic induction pump design
_Magnetohydrodynamics_ **36** 181–7

[48] Zinkle S. 1998 Summary of physical properties for lithium,
Pb-17Li and (LiF) n _·_ BeF2 coolants _APEX Study Meeting_
_Sandia National Laboratories_ ( _27–28 July 1998_ ) (Sandia
[National Laboratories) pp 1–8 (available at: https://bpb-](https://bpb-us-w2.wpmucdn.com/research.seas.ucla.edu/dist/d/39/files/2019/08/1zinkle0798.pdf)
[us-w2.wpmucdn.com/research.seas.ucla.edu/dist/d/39/](https://bpb-us-w2.wpmucdn.com/research.seas.ucla.edu/dist/d/39/files/2019/08/1zinkle0798.pdf)
[files/2019/08/1zinkle0798.pdf)](https://bpb-us-w2.wpmucdn.com/research.seas.ucla.edu/dist/d/39/files/2019/08/1zinkle0798.pdf)

[49] Yakimovich K.A., Tsitsarkin A. and Mozgovoi A.G. 2000
Experimental investigation of the density of liquid
lithium hydride at high temperatures _High Temp._
**[38](https://doi.org/10.1023/A:1004133121642)** [867–74](https://doi.org/10.1023/A:1004133121642)

[50] Welch F. 1961 Lithium hydride properties _Technical Report_
(General Electric Co. Aircraft Nuclear Propulsion Dept.)

[51] Smith R.L. and Miser J.W. 1963 _Compilation of the_
_properties of lithium hydride_ X-483 NASA

[52] Segantin S., Testoni R. and Zucchetti M. 2020 Neutronic
comparison of liquid breeders for arc-like reactor blankets
_Fusion Eng. Des._ **[160](https://doi.org/10.1016/j.fusengdes.2020.112013)** [112013](https://doi.org/10.1016/j.fusengdes.2020.112013)

[53] Kuang A. _et al_ 2018 Conceptual design study for heat
exhaust management in the arc fusion pilot plant _Fusion_
_Eng. Des._ **[137](https://doi.org/10.1016/j.fusengdes.2018.09.007)** [221–42](https://doi.org/10.1016/j.fusengdes.2018.09.007)

[54] Waganer L. 2013 ARIES cost account documentation
UCSD-CER-13-01 University of California, San Diego

[55] Miller L.R. 1996 _Systems Analysis_ (University of California)

[56] Dolan T., Yamazaki K. and Sagara A. 2005 Helical fusion
power plant economics studies _Fusion Sci. Technol._
**[47](https://doi.org/10.13182/FST05-A599)** [60–72](https://doi.org/10.13182/FST05-A599)

[57] Delene J., Krakowski R., Sheffield J., Dory R. 1988
Generomak: fusion physics, engineering and costing
model _Technical Report_ (Oak Ridge National Lab.)

[58] Miller R., Krakowski R. 1981 Modular stellarator fusion
reactor concept _Technical Report_ (Los Alamos National
Lab.)

[59] Robin R. and Volpe F.A. 2022 Minimization of magnetic
forces on stellarator coils _Nucl. Fusion_ **[62](https://doi.org/10.1088/1741-4326/ac7658)** [086041](https://doi.org/10.1088/1741-4326/ac7658)

[60] Fleiter J. and Ballarino A. 2014 Parameterization of the
critical surface of REBCO conductors from Fujikura
EDMS 1426239 CERN

[61] Fleiter J., Konstantopoulou K., Richter D. and Ballarino A.
2017 Characterization of REBCO tape and Roebel cable at
CERN _WAMHTS-4_ ( _Barcelona, SPAIN_, _15 February_
_2017_ [) pp 15–17 (available at: https://indico.cern.ch/event/](https://indico.cern.ch/event/588810/)
[588810/)](https://indico.cern.ch/event/588810/)

[62] Senatore C., Barth C., Bonura M., Kulich M. and
Mondonico G. 2015 Field and temperature scaling of the
critical current density in commercial REBCO coated
conductors _Supercond. Sci. Technol._ **[29](https://doi.org/10.1088/0953-2048/29/1/014002)** [014002](https://doi.org/10.1088/0953-2048/29/1/014002)

[63] Xu A. 2012 Flux pinning study of REBCO coated conductors
for high field magnet applications _Thesis_ Florida State
[University (available at: https://diginole.lib.fsu.edu/](https://diginole.lib.fsu.edu/islandora/object/fsu%3A183200)
[islandora/object/fsu%3A183200)](https://diginole.lib.fsu.edu/islandora/object/fsu%3A183200)

[64] Van Nugteren J. 2016 High temperature superconductor
accelerator magnets _PhD Thesis_ University of Twente

[65] Grant P.M. and Sheahen T.P. 2002 Cost projections for high
[temperature superconductors (arXiv:cond-mat/0202386)](https://arxiv.org/abs/cond-mat/0202386)

[66] Hemsworth R.S. and Inoue T. 2005 Positive and negative ion
sources for magnetic fusion _IEEE Trans. Plasma Sci._
**[33](https://doi.org/10.1109/TPS.2005.860090)** [1799–813](https://doi.org/10.1109/TPS.2005.860090)

[67] Hemsworth R. and Boilson D. 2017 Considerations for the
development of neutral beam injection for fusion reactors
or DEMO _AIP Conf. Proc._ **[1869](https://doi.org/10.1063/1.4995788)** [060001](https://doi.org/10.1063/1.4995788)

[68] McAdams R. 2014 Beyond ITER: neutral beams for a
demonstration fusion reactor (DEMO) _Rev. Sci. Instrum._
**[85](https://doi.org/10.1063/1.4852299)** [02–319](https://doi.org/10.1063/1.4852299)

[69] Hopf C., Starnella G., Harder N. and Fantz U. 2021 Neutral
beam injection for fusion reactors: technological
constraints versus functional requirements _Nucl. Fusion_
**[61](https://doi.org/10.1088/1741-4326/ac227a)** [106032](https://doi.org/10.1088/1741-4326/ac227a)

[70] Thumm M. 2021 _State-of-the-Art of High-Power_
_Gyro-Devices. Update of Experimental Results 2021_ (KIT
Scientific Publishing)

[71] Caughman J.B. _et al_ 2017 Plasma source development for
fusion-relevant material testing _J. Vac. Sci. Technol._ A
**[35](https://doi.org/10.1116/1.4982664)** [03–114](https://doi.org/10.1116/1.4982664)

[72] Dumont R. 2021 Magnetic confinement fusion-plasma
theory: heating and current drive _Encyclopedia of Nuclear_
_Energy_ (Elsevier)

[73] Iguchi M., Sakurai T., Nakhira M., Koizumi N. and
Nakajima H. 2016 Cryogenic structural materials of the
ITER toroidal field coil structure _Proc. SMINS-4_
( _Manchester, UK_, _11–4 July 2016_ ) p IV-1 (available at:
[www.oecd-nea.org/jcms/pl_22687/fourth-international-](https://www.oecd-nea.org/jcms/pl_22687/fourth-international-workshop-on-structural-materials-for-innovative-nuclear-systems-smins-4)
[workshop-on-structural-materials-for-innovative-nuclear-](https://www.oecd-nea.org/jcms/pl_22687/fourth-international-workshop-on-structural-materials-for-innovative-nuclear-systems-smins-4)
[systems-smins-4)](https://www.oecd-nea.org/jcms/pl_22687/fourth-international-workshop-on-structural-materials-for-innovative-nuclear-systems-smins-4)

[74] ITER Technical Basis 2002 _ITER EDA Documentation Series_
_No._ 24 (International Atomic Energy Agency)

[75] Sas J., Weiss K. and Jung A. 2015 The mechanical and
material properties of 316LN austenitic stainless steel for
the fusion application in cryogenic temperatures _IOP_
_Conf. Ser.: Mater. Sci. Eng._ **[102](https://doi.org/10.1088/1757-899X/102/1/012003)** [012003](https://doi.org/10.1088/1757-899X/102/1/012003)

[76] Barabash V. _et al_ 2007 Materials challenges for ITER–current
status and future activities _J. Nucl. Mater._ **[367](https://doi.org/10.1016/j.jnucmat.2007.03.017)** [21–32](https://doi.org/10.1016/j.jnucmat.2007.03.017)

[77] Spence J. and Tooth A.S. 2012 _Pressure Vessel Design:_
_Concepts and Principles_ (CRC Press)

[78] Moon F.C. 1982 The virial theorem and scaling laws for
superconducting magnet systems _J. Appl. Phys._
**[53](https://doi.org/10.1063/1.330423)** [9112–21](https://doi.org/10.1063/1.330423)

[79] Warmer F., Beidler C., Dinklage A., Egorov K., Feng Y.,
Geiger J., Schauer F., Turkin Y., Wolf R. and
Xanthopoulos P. 2015 HELIAS module development for
systems codes _Fusion Eng. Des._ **[91](https://doi.org/10.1016/j.fusengdes.2014.12.028)** [60–66](https://doi.org/10.1016/j.fusengdes.2014.12.028)

[80] Sheffield J. and Milora S.L. 2016 Generic magnetic fusion
reactor revisited _Fusion Sci. Technol._ **[70](https://doi.org/10.13182/FST15-157)** [14–35](https://doi.org/10.13182/FST15-157)

[81] Maisonnier D. _et al_ 2005 The European Power Plant
conceptual Study _Fusion Eng. Des._ **[75](https://doi.org/10.1016/j.fusengdes.2005.06.095)** [1173–9](https://doi.org/10.1016/j.fusengdes.2005.06.095)

[82] ECB Statistical Data Warehouse 2022 Statistics bulletin
_Technical Report_ (European Central Bank (ECB))
[(available at: https://sdw.ecb.europa.eu/reports.do?node =](https://sdw.ecb.europa.eu/reports.do?node%20=%201000004045)
[1000004045)](https://sdw.ecb.europa.eu/reports.do?node%20=%201000004045)

[83] International Energy Agency and Organisation for Economic
Co-operation and Development/Nuclear Energy Agency
2020 Projected costs of generating electricity—2020

edition _Technical Report_ (International Energy Agency
[(IEA)) (available at: www.iea.org/reports/projected-costs-](https://www.iea.org/reports/projected-costs-of-generating-electricity-2020)
[of-generating-electricity-2020)](https://www.iea.org/reports/projected-costs-of-generating-electricity-2020)

[84] Lazard 2021 Lazard’s levelized cost of energy
analysis—version 15.0 _Technical Report_ (Lazard)
[(available at: www.lazard.com/perspective/levelized-cost-](https://www.lazard.com/perspective/levelized-cost-of-energy-levelized-cost-of-storage-and-levelized-cost-of-hydrogen/)
[of-energy-levelized-cost-of-storage-and-levelized-cost-of-](https://www.lazard.com/perspective/levelized-cost-of-energy-levelized-cost-of-storage-and-levelized-cost-of-hydrogen/)
[hydrogen/)](https://www.lazard.com/perspective/levelized-cost-of-energy-levelized-cost-of-storage-and-levelized-cost-of-hydrogen/)

[85] US Energy Information Administration 2022 _Annual Energy_
_Outlook 2022_ AEO2022 (Energy Information
[Administration) (available at: www.eia.gov/outlooks/aeo/](https://www.eia.gov/outlooks/aeo/IIF_carbonfee/)
[IIF_carbonfee/)](https://www.eia.gov/outlooks/aeo/IIF_carbonfee/)

[86] World Nuclear Association (WNA) 2017 Nuclear power
economics and project structuring—edition 2017
_Technical Report_ [(available at: https://world-nuclear.org/](https://world-nuclear.org/our-association/publications/online-reports/nuclear-power-economics-and-project-structuring.aspx)
[our-association/publications/online-reports/nuclear-](https://world-nuclear.org/our-association/publications/online-reports/nuclear-power-economics-and-project-structuring.aspx)
[power-economics-and-project-structuring.aspx)](https://world-nuclear.org/our-association/publications/online-reports/nuclear-power-economics-and-project-structuring.aspx)

[87] US Bureau of Labor Statistics 2022 Consumer price index
(CPI) _Technical Report_ (US Bureau of Labor Statistics)
(available at: www.bls.gov/cpi/data.htm)

[88] World Bank 2022 Inflation, consumer prices _Technical_
_Report_ (FRED, Federal Reserve Bank of St. Louis)
[(available at: fred.stlouisfed.org/series/FPCPITO](https://fred.stlouisfed.org/series/FPCPITOTLZGUSA)
[TLZGUSA)](https://fred.stlouisfed.org/series/FPCPITOTLZGUSA)

[89] Entler S., Horacek J., Dlouhy T. and Dostal V. 2018
Approximation of the economy of fusion energy _Energy_
**[152](https://doi.org/10.1016/j.energy.2018.03.130)** [489–97](https://doi.org/10.1016/j.energy.2018.03.130)

[90] _DEUTERIUM (D, 99.8%) (D2,99.6%_ + _HD,0.4%)_
(Cambridge Isotope Laboratories, Inc. (CIL)) (available
[at: https://isotope.com/en-us/deuterium-d-99-8-pct-d-99-](https://isotope.com/en-us/deuterium-d-99-8-pct-d-99-6-pct-plus-hd-0-4-pct-in-dlm--408--pk)
[6-pct-plus-hd-0-4-pct-in-dlm--408--pk)](https://isotope.com/en-us/deuterium-d-99-8-pct-d-99-6-pct-plus-hd-0-4-pct-in-dlm--408--pk)

[91] Whyte D., Minervini J., LaBombard B., Marmar E.,
Bromberg L. and Greenwald M. 2016 Smaller and sooner:
exploiting high magnetic fields from new superconductors
for a more attractive fusion energy development path _J._
_Fusion Energy_ **[35](https://doi.org/10.1007/s10894-015-0050-1)** [41–53](https://doi.org/10.1007/s10894-015-0050-1)

[92] Majkic G., Pratap R., Paidpilli M., Galstyan E., Kochat M.,
Goel C., Kar S., Jaroszynski J., Abraimov D. and
Selvamanickam V. 2020 In-field critical current
performance of 4.0 _µ_ m thick film REBCO conductor with
Hf addition at 4.2 K and fields up to 31.2 T _Supercond._
_Sci. Technol._ **[33](https://doi.org/10.1088/1361-6668/ab9541)** [07–03](https://doi.org/10.1088/1361-6668/ab9541)

[93] Benkel T., Miyoshi Y., Chaud X., Badel A. and Tixador P.
2017 REBCO tape performance under high magnetic field
_Eur. Phys. J. Appl. Phys._ **[79](https://doi.org/10.1051/epjap/2017160430)** [30601](https://doi.org/10.1051/epjap/2017160430)

[94] Loarte A. _et al_ 2007 Power and particle control _Nucl. Fusion_

**[47](https://doi.org/10.1088/0029-5515/47/6/S04)** [203](https://doi.org/10.1088/0029-5515/47/6/S04)

[95] You J. _et al_ 2018 European divertor target concepts for
DEMO: design rationales and high heat flux performance
_Nucl. Mater. Energy_ **[16](https://doi.org/10.1016/j.nme.2018.05.012)** [1–11](https://doi.org/10.1016/j.nme.2018.05.012)

[96] Creely A. _et al_ 2020 Overview of the SPARC tokamak _J._
_Plasma Phys._ **[86](https://doi.org/10.1017/S0022377820001257)** [865860502](https://doi.org/10.1017/S0022377820001257)

[97] Federici G. _et al_ 2019 Overview of the DEMO staged design
approach in Europe _Nucl. Fusion_ **[59](https://doi.org/10.1088/1741-4326/ab1178)** [066013](https://doi.org/10.1088/1741-4326/ab1178)

[98] Wurzel S.E. and Hsu S.C. 2022 Progress toward fusion
energy breakeven and gain as measured against the
Lawson criterion _Phys. Plasmas_ **[29](https://doi.org/10.1063/5.0083990)** [6](https://doi.org/10.1063/5.0083990)

[99] International Renewable Energy Agency (IRENA) 2020
_Renewable capacity statistics 2020_ (International
[Renewable Energy Agency) (available at: https://irena.org/](https://irena.org/publications/2020/Mar/Renewable-Capacity-Statistics-2020)
[publications/2020/Mar/Renewable-Capacity-Statistics-](https://irena.org/publications/2020/Mar/Renewable-Capacity-Statistics-2020)
[2020)](https://irena.org/publications/2020/Mar/Renewable-Capacity-Statistics-2020)

[100] Lovering J.R., Yip A. and Nordhaus T. 2016 Historical
construction costs of global nuclear power reactors _Energy_
_Policy_ **[91](https://doi.org/10.1016/j.enpol.2016.01.011)** [371–82](https://doi.org/10.1016/j.enpol.2016.01.011)

[101] Pugnat P. and Schneider-Muntau H.J. 2020 Conceptual
design optimization of a 60 T hybrid magnet _IEEE Trans._
_Appl. Supercond._ **[30](https://doi.org/10.1109/TASC.2020.2972498)** [1–7](https://doi.org/10.1109/TASC.2020.2972498)

[102] Hahn S. _et al_ 2019 45.5-Tesla direct-current magnetic field
generated with a high-temperature superconducting
magnet _Nature_ **[570](https://doi.org/10.1038/s41586-019-1293-1)** [496–9](https://doi.org/10.1038/s41586-019-1293-1)

[103] Deb K., Pratap A., Agarwal S. and Meyarivan T. 2002 A fast
and elitist multiobjective genetic algorithm: NSGA-II
_IEEE Trans. Evol. Comput._ **[6](https://doi.org/10.1109/4235.996017)** [182–97](https://doi.org/10.1109/4235.996017)

[104] Baik E., Chawla K.P., Jenkins J.D., Kolster C., Patankar N.S.,
Olson A., Benson S.M. and Long J.C. 2021 What is
different about different net-zero carbon electricity
systems? _Energy Clim. Change_ **[2](https://doi.org/10.1016/j.egycc.2021.100046)** [100046](https://doi.org/10.1016/j.egycc.2021.100046)

[105] Sepulveda N.A., Jenkins J.D., Sisternes F.J. and Lester R.K.
2018 The role of firm low-carbon electricity resources in
deep decarbonization of power generation _Joule_
**[2](https://doi.org/10.1016/j.joule.2018.08.006)** [2403–20](https://doi.org/10.1016/j.joule.2018.08.006)

[106] Dinklage A. _et al_ 2007 Physical model assessment of the
energy confinement time scaling in stellarators _Nucl._
_Fusion_ **[47](https://doi.org/10.1088/0029-5515/47/9/025)** [1265](https://doi.org/10.1088/0029-5515/47/9/025)

[107] Warmer F., Beidler C.D., Dinklage A. and Wolf R. 2016
From W7-X to a helias fusion power plant: motivation and
options for an intermediate-step burning-plasma stellarator
_Plasma Phys. Control. Fusion_ **[58](https://doi.org/10.1088/0741-3335/58/7/074006)** [074006](https://doi.org/10.1088/0741-3335/58/7/074006)

[108] El-Guebaly L.A. 2010 Fifty years of magnetic fusion
research (1958–2008): brief historical overview
and discussion of future trends _Energies_
**[3](https://doi.org/10.3390/en30601067)** [1067–86](https://doi.org/10.3390/en30601067)

[109] Ward D., Cook I., Lechon Y. and Saez R. 2005 The
economic viability of fusion power _Fusion Eng. Des._
**[75](https://doi.org/10.1016/j.fusengdes.2005.06.160)** [1221–7](https://doi.org/10.1016/j.fusengdes.2005.06.160)

[110] Reiter D., Wolf G. and Kever H. 1990 Burn condition, helium
particle confinement and exhaust efficiency _Nucl. Fusion_
**[30](https://doi.org/10.1088/0029-5515/30/10/012)** [2141](https://doi.org/10.1088/0029-5515/30/10/012)

[111] Sorbom B. _et al_ 2015 ARC: a compact, high-field, fusion
nuclear science facility and demonstration power plant
with demountable magnets _Fusion Eng. Des._
**[100](https://doi.org/10.1016/j.fusengdes.2015.07.008)** [378–405](https://doi.org/10.1016/j.fusengdes.2015.07.008)

[112] Fischer U., Boccaccini L., Bongioví G., Häußler A. and
Warmer F. 2018 Nuclear design issues of a stellarator
fusion power plant with breeder blanket in comparison to
tokamaks _27th IAEA Fusion Energy Conf. (FEC 2018)_

[113] Maki K. 1988 Energy multiplication in high tritium breeding
ratio blanket with front breeder zone for fusion reactors _J._
_Nucl. Sci. Technol._ **[25](https://doi.org/10.1080/18811248.1988.9733557)** [72–80](https://doi.org/10.1080/18811248.1988.9733557)

[114] Palermo I., Rapisarda D., Fernández-Berceruelo I. and
Ibarra A. 2017 Optimization process for the design of the
DCLL blanket for the European demonstration fusion
reactor according to its nuclear performances _Nucl. Fusion_
**[57](https://doi.org/10.1088/1741-4326/aa6c14)** [076011](https://doi.org/10.1088/1741-4326/aa6c14)

[115] Warmer F. and Bubelis E. 2019 First considerations on the
balance of plant for a HELIAS fusion power plant _Fusion_
_Eng. Des._ **[146](https://doi.org/10.1016/j.fusengdes.2019.03.167)** [2259–63](https://doi.org/10.1016/j.fusengdes.2019.03.167)

[116] Tamor S. 1988 Synchrotron radiation loss from
hot plasma _Nucl. Instrum. Methods Phys. Res._ A
**[271](https://doi.org/10.1016/0168-9002(88)91123-0)** [37–40](https://doi.org/10.1016/0168-9002(88)91123-0)

[117] Houlberg W., Attenberger S. and Hively L. 1982 Contour
analysis of fusion reactor plasma performance _Nucl._
_Fusion_ **[22](https://doi.org/10.1088/0029-5515/22/7/006)** [935](https://doi.org/10.1088/0029-5515/22/7/006)

[118] Beidler C., Harmeyer E., Kisslinger J., Ott I. and Wobig H.
1993 _Studies on a Stellarator Reactor of the Helias Type:_
_The Power Balance_ (Max-Planck-Institut für
Plasmaphysik)

[119] Lotz W. and Nührenberg J. 1988 Monte Carlo
computations of neoclassical transport _Phys. Fluids_
**[31](https://doi.org/10.1063/1.866955)** [2984–91](https://doi.org/10.1063/1.866955)

[120] Grekov D. 2005 High frequency way of helium ash removal
from stellarator-reactor _20th IAEA Fusion Energy Conf._
( _Villamoura, Portugal_, _1–6 November 2004_ ) vol 36 p 35
[(available at: https://inis.iaea.org/search/search.](https://inis.iaea.org/search/search.aspx?orig_q=RN:36080679)
[aspx?orig_q=RN:36080679)](https://inis.iaea.org/search/search.aspx?orig_q=RN:36080679)

[121] Hegna C.C. _et al_ 2022 Improving the stellarator
through advances in plasma theory _Nucl. Fusion_
**[62](https://doi.org/10.1088/1741-4326/ac29d0)** [042012](https://doi.org/10.1088/1741-4326/ac29d0)

[122] Landreman M. 2011 _Electric Fields and Transport in_
_Optimized Stellarators_ (MIT Plasma Science and Fusion
Center)

[123] Staebler G., Kinsey J. and Waltz R. 2007 A theory-based
transport model with comprehensive physics _Phys._
_Plasmas_ **[14](https://doi.org/10.1063/1.2436852)** [055909](https://doi.org/10.1063/1.2436852)

[124] Wang X., Malang S. and Raffray A. (ARIES Team) 2005
Maintenance approaches for ARIES-CS compact
stellarator power core _Fusion Sci. Technol._ **[47](https://doi.org/10.13182/FST05-A829)** [1074–8](https://doi.org/10.13182/FST05-A829)

[125] Maisonnier D. 2018 RAMI: the main challenge of fusion
nuclear technologies _Fusion Eng. Des._ **[136](https://doi.org/10.1016/j.fusengdes.2018.04.102)** [1202–8](https://doi.org/10.1016/j.fusengdes.2018.04.102)

[126] Brown T. 2018 Three confinement systems—spherical
tokamak, standard tokamak and stellarator: a comparison
of key component cost elements _IEEE Trans. Plasma Sci._
**[46](https://doi.org/10.1109/TPS.2018.2832457)** [2216–30](https://doi.org/10.1109/TPS.2018.2832457)

