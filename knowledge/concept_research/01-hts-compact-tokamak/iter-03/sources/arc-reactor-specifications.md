---
source: "https://arxiv.org/pdf/1409.3540"
source_type: "url"
extracted_at: "2026-03-29T16:31:25.450669+00:00"
content_hash_sha256: "a03e380701a0a8ce515250ca6b35d647c9948e119e53221d88d41acd44ee3346"
backend: "pdf_pipeline"
---

## ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with demountable magnets

B.N. Sorbom, J. Ball, T.R. Palmer, F.J. Mangiarotti, J.M. Sierchio, P. Bonoli, C. Kasten, D.A. Sutherland, H.S. Barnard, C.B.
Haakonsen, J. Goh, C. Sung, and D.G. Whyte

_Plasma Science and Fusion Center, Massachusetts Institute of Technology, Cambridge, MA 02139, USA_

**Abstract**

The affordable, robust, compact (ARC) reactor is the product of a conceptual design study aimed at reducing the size, cost, and
complexity of a combined fusion nuclear science facility (FNSF) and demonstration fusion Pilot power plant. ARC is a ∼ 200 - 250
MWe tokamak reactor with a major radius of 3.3 m, a minor radius of 1.1 m, and an on-axis magnetic field of 9.2 T. ARC has rare
earth barium copper oxide (REBCO) superconducting toroidal field coils, which have joints to enable disassembly. This allows
the vacuum vessel to be replaced quickly, mitigating first wall survivability concerns, and permits a single device to test many
vacuum vessel designs and divertor materials. The design point has a plasma fusion gain of _Qp_ ≈ 13.6, yet is fully non-inductive,
with a modest bootstrap fraction of only ∼63%. Thus ARC offers a high power gain with relatively large external control of the
current profile. This highly attractive combination is enabled by the ∼23 T peak field on coil achievable with newly available
REBCO superconductor technology. External current drive is provided by two innovative inboard RF launchers using 25 MW of
lower hybrid and 13.6 MW of ion cyclotron fast wave power. The resulting efficient current drive provides a robust, steady state
core plasma far from disruptive limits. ARC uses an all-liquid blanket, consisting of low pressure, slowly flowing fluorine lithium
beryllium (FLiBe) molten salt. The liquid blanket is low-risk technology and provides effective neutron moderation and shielding,
excellent heat removal, and a tritium breeding ratio ≥ 1.1. The large temperature range over which FLiBe is liquid permits an
output blanket temperature of 900 K, single phase fluid cooling, and a high efficiency helium Brayton cycle, which allows for net
electricity generation when operating ARC as a Pilot power plant.

_Keywords:_ Compact pilot reactor, High magnetic field, Fusion nuclear science facility, Liquid immersion blanket,
Superconducting joints, Tokamak, High-field launch

**1.** **Introduction**

Most fusion reactor designs, such as the ARIES studies

[1, 2, 3, 4], assume a large, fixed 1000 MWe output for a power
plant. However, large-scale designs make fusion engineering
research and development difficult because of the high cost and
long construction time of experiments. This paper presents a
smaller, less costly, timelier, and lower risk alternative, the 200
MWe ARC reactor. ARC is a conceptual point design of a
fusion nuclear science facility/Pilot power plant that demonstrates the advantages of a compact, high-field design utilizing REBCO superconducting magnets and inboard launched
lower hybrid current drive (LHCD). The design was carried
out as a follow-on to the Vulcan conceptual design; a tokamak for studying plasma-material interaction (PMI) physics
that also utilized the demountable REBCO tape and high-field
side LHCD [5]. A goal of the ARC design is to minimize the reactor size in order to reduce the plant capital cost. Like Vulcan
and several other proposed tokamaks [2, 6, 7, 8], ARC makes
use of high-temperature superconductors (HTS), which enables
large on-axis magnetic fields and ultimately reduces the size
of the reactor. It is important to emphasize that ARC represents one of many possible compact, high-field design config

urations. As discussed later in this paper, the modular nature
of ARC allows it to change experimental direction and pursue
the nuclear materials and vacuum vessel configurations that are
determined to be most promising. This enables more innovative
and speculative designs because the cost and operational implications of failure are reduced. Indeed a starting design philosophy of ARC is that failure should and will occur as various
fusion materials and power exhaust technologies are tried and
tested. However, because they can be readily fixed, these failures should not compromise the overall capacity of the device
to produce fusing plasmas.

This paper is organized in the following way. Section 2
presents an overview of the ARC design. Section 3 describes
the plasma physics basis for the reactor and discusses the current drive system. Section 4 details the design of the magnet
system. Section 5 presents the design of the fusion power core,
consisting of the tritium breeding/heat exchange blanket and the
neutron shield. Section 6 presents a simple costing estimate.
Section 7 briefly lists the most vital research and development
necessary to enable a design similar to ARC. Lastly, Section 8
provides some concluding remarks.

_Preprint submitted to Fusion Engineering and Design_ _August 18, 2015_

![Figure 1: The ARC reactor, shown with the plasma in yellow and the TF superconducting tape in brown. Note the neutron shield is omitted for viewing clarity. Also](images/tmpc7ciscuc.pdf-1-0.png)
note that although the ARC design is based on a diverted plasma, the physical divertor design was left for later study and a simplified representation of the vacuum
vessel is shown here.

**2.** **Design motivation and overview**

The ARC reactor is a conceptual tokamak design that can
function as both a demonstration fusion power plant for energy
generation and a fusion nuclear science facility (FNSF) for integrated materials and component irradiation testing in a D-T
neutron field. The starting objective of the ARC study was to
determine if a reduced size D-T fusion device (fusion power ≤
500 MW) could benefit from the high magnetic field technology
offered by recently developed high temperature superconductors. The reasoning was that a high magnitude magnetic field in
a compact, superconducting device might offer not only access
to high plasma gain _Qp_, but also enable net electric gain _Qe_ - 1.
This specific option has not been explored previously in design studies, although the recent advanced tokamak (AT) Pilot
( _Qe_ =1) study of Menard et al. [9] had similar design goals, but
used conventional superconductor technology. A recent FNSF
study is the FDF design [10], which is a similar size to ARC,
but consumes > 500 MW of electricity because it does not use

superconducting magnets.
The reactor design is shown in Fig. 1, the inboard radial
build in Fig. 2, and the most significant design parameters are
given in Table 1. Another unique feature of the ARC design is
that significant margin to disruptive operational limits was enforced from the start, i.e. strict limits on the edge safety factor
(kink limit), Greenwald fraction (density limit) [11], and normalized beta below the no-wall limit (pressure limit) [12] were
imposed. This followed from the logic that high field designs
should provide scenarios less prone to disruptions, which are
nearly intolerable in burning plasmas because of internal material damage. Thus they should be strongly avoided in any
tokamak FNSF/Pilot plant.
ARC explores an innovative approach to current drive in
burning plasma. Lower hybrid waves, launched from the high
field side (HFS) of the tokamak, are used to noninductively
drive plasma current. High field side launch is shown in modeling to increase the current drive efficiency, which is crucial to
maximizing the power plant gain and providing better external

control of the radial current profile. Also, launching from the
more quiescent HFS of the plasma is expected to reduce damage to the launcher [13] from plasma-material interactions.
The use of REBCO superconducting technology in the
toroidal field (TF) coils permits significantly higher on-axis
magnetic fields than standard Nb3Sn superconductors. High
magnetic field strength is essential in small reactor designs
in order to achieve the necessary poloidal field/plasma current needed for sufficient confinement and stability against beta
(pressure) limits. In addition, when holding beta constant the
volumetric fusion power scales as ∼ _B_ [4] 0 [and, at constant safety]
factor, the plasma confinement strongly improves with magnetic field strength [14]. Since REBCO tapes allow the use of
resistive joints in the superconducting coils [15], the TF coils
can be made demountable, meaning the coils can be split into
two pieces (see Fig. 3). As discussed below, demountability
can provide a dramatically different and likely more attractive,
modular maintenance scheme for magnetic fusion devices. The
tradeoffs between modular component replacement [16] and
power dissipation in the TF joints [15] have only been explored
at small size in the Vulcan D-D device ( _R_ 0 ≈ 1.2m), which
motivates our exploration of demountability in a D-T reactor.
In sector maintenance, it is necessary to split all components
located inside the TF coils into toroidal sections that can fit between the gaps in the TF coils, which is complex and timeintensive. It necessitates significantly larger TF coils to allow
for space to remove sections of the vacuum vessel (e.g. ARIESAT [2]). With joints, the TF coils, which are the most expensive
component of a reactor [17], can be made smaller. Furthermore, the entire vacuum vessel (including all internal components) can be externally constructed and tested as one modular
part. This module can then, in principle, be relatively quickly
lowered into place with the TF coils demounted, minimizing or
eliminating the maintenance that must be performed inside the
TF volume itself. The relative ease of installation and external
testing of all internal components should greatly increase the
simplicity and reliability of component replacement. This is a
particularly attractive feature for an FNSF and was the motivation for using demountable copper coils in the FDF design

[10]. Additionally, demountable copper TF coils have already
been used in experimental devices such as COMPASS [18] and
Alcator C-Mod [19]. A major motivation for this study was to
explore the benefits of modular replacement versus the issues
associated with TF joints in REBCO superconductors. The preliminary conclusion is that it represents an attractive alternative
to sector maintenance in an FNSF and may also be the optimal
choice for future commercial reactors.
The replaceable vacuum vessel is made of corrosion-resistant
Inconel 718. Although the high nickel content of Inconel 718
makes this alloy much more prone to nuclear activation, it was
chosen as a “first-round” material due to its ability to maintain high strength and corrosion resistance at elevated temperatures. Ideally, further materials research will identify a more
suitable material for future iterations of the vacuum vessel design. The vessel is approximately shaped like an elliptical torus.
It is double-walled and contains a channel through which FLiBe
flows for cooling and tritium breeding. The vacuum vessel is at

tached to the blanket tank from above by 18 support columns,
which are evenly spaced between the 18 TF coils. All connections needed for in-vessel components (such as waveguides,
vacuum ports, etc.) run though these columns, which are also
curved to reduce the flux of neutrons streaming through. Thus,
the vessel is isolated from the permanent tokamak components,
so it can be designed to fail without damaging lifetime reactor components in the worst case of a full, unmitigated plasma
disruption.
Making the TF coils demountable has a direct impact on the
design of the breeding blanket. In order to permit modular
maintenance, the blanket is composed entirely of liquid FLiBe
that acts as a neutron moderator, shield, and breeder. The FLiBe
is contained in a large low-pressure tank, referred to as the blanket tank, and flows slowly past the vacuum vessel. The blanket
tank is a robust lifetime component and serves as the primary
nuclear containment boundary, as opposed to the vacuum vessel. Neutrons created by the deuterium-tritium fusion reaction
are captured in the FLiBe, transferring their energy and breeding tritium to fuel the reactor. Tritium can then be extracted
from the liquid FLiBe after it flows out of the blanket tank.
A neutron shield made of titanium dihydride (TiH2) surrounds the blanket tank. This is to protect the inboard leg of
the superconducting TF coil, which is particularly space constrained and susceptible to neutron radiation damage. Effective
neutron shielding and survivable TF superconducting material
is crucial to enable small reactor designs. A detailed MCNP
neutronics analysis of the reactor (see Section 5.2) shows that
the blanket/neutron shield combination reduces the neutron flux
to the TF coil by a factor of 9 × 10 [−][5] . This ensures at least 9
full-power years (FPY) of operation based on the TF fluence
limits currently available.
We estimated the thermal conversion efficiency of the fusion
power core (FPC) with a simple, non-ideal Brayton cycle and
used this to approximate _Qe_ . It should be noted that the _Qe_
of the entire power plant will be lower than this estimate, but
requires a full site design, which is beyond the scope of this
paper. The analysis assumed component efficiencies for the
compressor and turbine of 95% (the expected state of the art of
next-generation large-scale power turbomachinery components

[20]) to obtain the cycle thermal efficiencies. Three cases were
considered: an FNSF phase, a conservative Pilot phase, and an
“aggressive” Pilot phase. In the FNSF phase, the blanket outlet temperature is set at 900 K, based on a maximum FLiBe
flow rate of 0.2 m/s (see Section 5.4). This temperature is considered conservative with respect to material limits, but reduces
the Brayton cycle efficiency to ∼ 40%, resulting in _Pnet_ = 190
MW and _Qe_ = 3. The next two phases are more speculative,
and would require an evolution to higher temperature materials informed by the FNSF stage. The purpose of these phases
is to illustrate that first wall/vacuum vessel research during the
FNSF stage is crucial to allow a higher blanket temperature,
which would greatly increase the total plant efficiency. In the
conservative Pilot phase, the blanket outlet temperature is set
at 1100 K, for a Brayton cycle efficiency of ∼ 46%, resulting
in _Pnet_ = 233 MW and _Qe_ = 3.5. Finally, in the aggressive Pilot phase, the blanket outlet temperature is set at 1200 K, for

Table 1: List of significant ARC design parameters.

![Figure 2: The ARC reactor inboard radial build.](images/tmpc7ciscuc.pdf-4-0.png)

parameters in this section were determined, the design was iterated several times using codes such as ACCOME, MCNP, and
COMSOL. Note that in many cases the final design parameters
(e.g. in Table 1 and in the sections following this one) differ
from the initial parameters calculated in this section.
A fundamental equation for any magnetic fusion reactor design is the scaling [22]

_P_ _f_
∝ 8 ⟨ _p_ ⟩ [2] ∝ β [2] _T_ _[B]_ 0 [4][,] (1)
_VP_

![Figure 3: The upper half of ARC’s superconducting coils can be removed, allowing the vacuum vessel to be removed from the blanket tank as a single piece.](images/tmpc7ciscuc.pdf-4-1.png)

a Brayton cycle efficiency of ∼ 50%, resulting in _Pnet_ = 261
MW and _Qe_ = 3.8. It is noted that decreasing the FLiBe flow
rate allows access to higher exit temperatures and may reduce
corrosion. Recent molten salt fission studies [21] indicate that
many material candidates in molten salts up to temperatures of
∼ 1120 K are possible but require further testing in reactor environments, particularly at higher temperatures. Because the
FNSF phase of ARC is the obvious first iteration of the design,
all further material analysis in this paper (see Section 5) is done
assuming a blanket outlet temperature of 900 K.

![](images/page_004_eq_0.png)
**3.** **Core plasma physics**

_3.1._ _0-D point design optimization_

In order to determine a starting point for the ARC parameters, a 0-D design exercise was performed. After the initial

for volumetric fusion power density _P_ _f_ / _VP_, where ⟨ _p_ ⟩ is the
volume-averaged plasma pressure in MPa. This equation provides two strategies to achieve the high fusion power density desirable for an FNSF and required for economical fusion power:
high β _T_ ≡ [2][µ] _B_ [0][⟨][2] 0 _[p]_ [⟩] or large _B_ 0. However these two strategies are

dramatically different. Increasing β _T_ up to or past its intrinsic limit comes at the risk of exciting MHD modes [12] and
increasing the frequency of disruptions in devices that have almost no tolerance to disruption damage (see Section 5.5). Instead, the ARC reactor exploits the quartic dependence on the
magnetic field in Eq. (1) through the use of REBCO superconducting tapes, which provide access to approximately double
the magnetic field magnitude of conventional niobium-based
superconductors (see Section 4.1).
As with any tokamak, four principal stability considerations
restrict the ARC reactor design parameter space: the external
kink, Greenwald density, Troyon beta, and elongation (vertical
stability) limits. The simplified rules given here were used to
provide a 0-D scoping of the operating space available at high
B and small size. Operating at the Troyon beta limit [12], given
by

β _N_ ≡ _[aB]_ [0] β _T_ = 3, (2)

![](images/page_004_eq_1.png)

where _Ip_ is in MA and β _T_ is in percent, allows for a safety margin to pressure-driven instabilities and disruptions. Second, the
edge safety factor was constrained to be well above the disruptive kink limit [23], which is approximated by

_qa_ ≡ [5][ϵ] _[aB]_ [0] _S_ ≳ 2.2, (3)

![](images/page_004_eq_2.png)
where

_S_ = [1][ +][ κ][2] (4)

![](images/page_004_eq_3.png)

is the leading order shaping term [24]. The minimum value of 2.2 includes a safety margin of 10% above the hard disruption limit of $q_* = 2$ as violating this limit would result in large, damaging disruptions. Third, operating at a 10% safety margin below the disruptive Greenwald density limit [11]:

$$n_{G} = 0.9 \frac{I_{p}}{\pi a^{2}},\tag{5}$$

is enforced to allow for unexpected excursions of the plasma density above steady state operation. Lastly, operation at the empirical elongation limit for vertical stability of

$$\kappa \leq 5.4\epsilon \tag{6}$$

The elongation is chosen in order to gain the benefits of shaping (e.g. higher current at lower safety factor) without the use of complex position stabilization schemes, which fits the ARC design philosophy of minimizing operational limits. This empirical elongation limit is based on the standard elongations of existing devices with divertors and is valid over the range of $0.2 \leq \epsilon \leq 0.55$. A more rigorous treatment, given in Ref. [25], provides justification that the chosen elongation is achievable.

![](images/page_005_eq_0.png)
The desire to increase elongation as much as possible is well understood by combining Eqs. (1) through (4) to yield

$$\frac{P_f}{V_p} \propto \frac{\beta_{N}^{2}(1+\kappa^{2})}{q_{*}^{4}} B_0^4 \tag{7}$$

![](images/page_005_eq_1.png)
We see the fusion power density can also be optimized through the choice of geometry, in particular the aspect ratio. Although, we will see that the on-coil magnetic field is constrained rather than the on-axis field, which introduces a factor of $(1-\epsilon)^4$ into Eq. (7).

In addition to the four plasma physics constraints stated above, it is necessary to approximate nuclear engineering limitations, structural limitations, and current drive accessibility conditions to further constrain the design parameter space. Firstly, the limit on the minimum possible inboard blanket thickness is estimated to be

![](images/page_005_eq_2.png)
$$\Delta_b = 0.3\text{m},\tag{8}$$

in order to sufficiently moderate and absorb fusion neutrons. This distance becomes critical on the inboard side in compact tokamaks because it constrains the achievable on-axis magnetic field. It should be noted that Eq. (8) is an intentionally simple estimate used only to constrain the 0-D design. This limit is investigated in Section 5.2. Section 4.2 requires increasing the on-coil magnetic field to obtain high fusion power densities increases the mechanical stresses on the TF coils. As a result of space constraints and the $1/R$ dependence of the toroidal field, the mechanical constraints are most severe on the inboard leg. Therefore, the on-axis toroidal magnetic field was limited to be

$$B_0 = B_{0,\text{coil,max}}(1 - \epsilon - \frac{\Delta_b}{R_0}),\tag{9}$$

where $B_{0,\text{coil,max}} = 18$ T is the estimated maximum allowable on-coil toroidal magnetic field estimated from empirical mechanical stress limits [26]. It should again be noted that Eq. (9) is an intentionally simplified estimate used for the purpose of assessing the 0-D design. A full stress analysis, dependent on the particular support structure is performed in Section 4.2.3. For REBCO superconductors operating far below their critical temperatures, the toroidal field is generally limited by mechanical stress rather than the critical current density, which typically limits standard Nb$_3$Sn.

![](images/page_005_eq_3.png)
Finally a requirement for achieving a non-inductive scenario was added to the 0-D scoping by considering current drive (CD) and bootstrap current. For reactor-relevant RF current drive schemes in the lower hybrid and electron cyclotron range of frequencies it is highly desirable, or required, to keep the plasma under-dense such that

$$f_{pe} = \frac{89.9\sqrt{n_e}}{28B_c} < 1\tag{10}$$

![](images/page_005_eq_4.png)
is satisfied [13], where $f_{pe}$ is the electron plasma frequency and $B_c$ is the electron cyclotron frequency. It should be noted that Eq. (10) is evaluated on axis for simplicity. In addition, since the ECRH wave access condition is more limiting than that of LH, it was chosen to constrain the 0-D analysis. This allowed for flexibility in the choice of the current drive method, even though LH was ultimately chosen.

If the plasma is under-dense then the accessibility condition for LHCD determines the minimum allowable parallel index of refraction, $n_{||}$ (see Section 3.3 and Eq. (21) evaluated at $R = R_0$). This determines the maximum CD efficiency, using the analytic estimate [27]

$$\eta_{\text{LHCD}} = \frac{31}{(\ln \Lambda + 5)} \frac{1}{Z_{\text{eff}} + 1.48} \frac{b}{n_{||}^2}\tag{11}$$

![](images/page_005_eq_5.png)
where  $\ln \Lambda = 17$ and $Z_{\text{eff}} = 1.2$ are assumed and $\eta_{\text{LHCD}}$ is in units of $10^{20}$ A/W/m$^2$. A standard empirical characterization of current drive efficiency is given as

![](images/page_005_eq_6.png)
$$\eta_{CD} = \frac{I_{CD} n_0 R_0}{P_{cd}}\tag{12}$$

where $I_{CD}$ is the externally driven current (in MA), $n_0$ is the density (in units of $10^{20}$ m$^{-3}$), and $P_{cd}$ is the external heating power (in MW). We can use this to calculate the current drive fraction, $f_{CD} = I_{CD}/I_p$, from $P_{cd}$ (which is assumed to be entirely LHCD). The bootstrap fraction, $f_{bs}$, can be estimated from a global formula [2, 28, 29] as

$$f_{bs} = 0.04 \frac{\beta_N B_0 R_0}{I_p a} \tag{13}$$

![](images/page_005_eq_7.png)
Since ARC must be steady state, we know that there is no inductive current, so

$$f_{CD} + f_{bs} = 1.\tag{14}$$

This gives the external heating power as a function of the plasma current. Plugging this into

![](images/page_005_eq_8.png)
$$Q_e = \frac{P_f}{P_{cd}} \geq 25\tag{15}$$
![](images/page_005_eq_9.png)
![](images/page_005_eq_10.png)

![Figure 4: The (a) reactor design _R_ 0-ϵ parameter space and (b) the most limiting constraints for _P_ _f_ = 500 MW with contours of blanket power loading](images/tmpc7ciscuc.pdf-6-0.png)
(in MW/m [2] ). Colored regions in (a) indicate allowable _R_ 0-ϵ combinations and
the point indicates the chosen initial design point assuming a maximum on-coil
magnetic field of 18 T.

we arrive our final condition which sets a lower limit on the
desired plasma gain, _Qp_ .
These 0-D constraints were imposed to scope _R_ 0 − ϵ parameter space, as shown in Fig. 4. As can be seen from the governing limit equations (see Eqs. (1) through (14)), _R_ 0 and ϵ play
critical roles in setting the physics limits and directly determine
the size of the device. The use of demountable coil magnets
(detailed in Section 4) strongly motivated this 0-D study and
optimization. With demountable magnets, sector maintenance
requirements (e.g. ensuring that components can fit between
the TF coils) no longer constrain the aspect ratio. This allowed
the design to forgo the standard AT aspect ratio of 4 (e.g. Refs.

[2] and [9]). Also, a very low aspect ratio (ϵ ≤ 1.5) was prohibited since it does not allow room for inboard shielding of
the superconducting tapes for a Pilot power plant. The purpose
of the 0-D study was then two-fold: identify a minimum size
for ARC to meet its FNSF/Pilot fusion mission and determine
a reasonable choice for the aspect ratio.
The scoping study used the following fixed parameters:
_Bcoil_, _max_ = 18 T, ∆ _b_ = 0.5 m, _fRF_ = 5 GHz, _P_ _f_ = 500 MW,
and β _N_ = 3. The _R_ 0-ϵ space allowed by the above constraints
is plotted in Fig. 4(a). Fig. 4(b) indicates that the boundary of
allowed space is mostly set by the _Qp_ limit (although the overdense limit becomes limiting at ϵ ≥ 0.5). Because total fusion
power is fixed, the contours of constant areal power density in

Fig. 4(a) are also contours of constant blanket area, _S b_, where
red denotes the smallest blanket and blue the largest. Blanket
area is a good measure of device “size”, since with a fixed blanket thickness it sets the volume of the blanket. Fig. 4(a) shows
the design goal of ARC to produce 500 MW at the smallest size
is thus met at ϵ ∼ 0.3 and _R_ 0 ∼ 3 m (red contour).
The ARC 0-D design point of _R_ 0 = 3.2 m, ϵ = 0.34 (the point
in Fig. 4) was chosen because, at _P_ _f_ / _S b_ = 2.5 MW/m [2], it
meets the FNSF/Pilot mission requirement for power density.
It should be noted that a wide range of aspect ratios, 0.2 ≤ ϵ ≤
0.5 could satisfy the power density requirement (yellow contour
of Fig. 4(a)) at fixed blanket size. The choice of our operating
point at ϵ = 0.34 was determined by locating the _R_ 0 - ϵ point
on the _P_ _f_ / _S b_ = 2.5 MW/m [2] contour that was furthest from the
operating boundary. Of course this optimization will change
with different assumptions, particularly blanket thickness. Thus
there are exciting opportunities to explore the use REBCO demountable magnet technology at various aspect ratios.
The 0-D design point has the following parameters: _R_ 0 = 3.2
m, a = 1.1 m, _B_ 0 = 9 T, _P f_ / _S b_ = 2.42 MW/m [2], _n_ 20 = 1.6, T = 13
keV, and estimated CD efficiency of η _CD_ = 0.5×10 [20] _AW_ [−][1] _m_ [−][2] .
The plasma current at the design point shown in Fig. 4(b) is
_Ip_ ∼ 6.75 MA and the safety factor is _qa_ ∼ 5.6 or _q_ 95 ∼ 7.6.
However these values are problematic for the starting design
point because they require the current to be over-driven (meaning the externally driven current must be used to partially cancel
the bootstrap current). This occurs because the scoping algorithm only assessed operational limits at the maximum β _N_ . The
design point was determined by increasing the current until a
self-consistent non-inductive fraction of unity was obtained. To
solve this problem the plasma current was increased to _Ip_ ∼ 8.4
MA, which decreased the safety factor to _qa_ ∼ 4.5 (still well
away from the kink limit) and the normalized beta to β _N_ ∼ 2.4
(further from the Troyon limit since the pressure is fixed because the fusion power is fixed). These values in turn set the
bootstrap fraction _fbs_ ∼ 0.76 and current drive fraction _fCD_ ∼
0.24, without any need for cancellation. Due to the limited accuracy of achieving this balance the 0-D design point was estimated to have _Ip_ ∼ 8-8.5 MA and _q_ 95 ∼ 6. The 0-D design point
is the starting point for the detailed 1-D plasma profile design
and current drive/equilibrium simulations below.
Due to its simplicity and transparency, it is worthwhile to
discuss the 0-D results in the context of “wins” gained by using
the high-field approach of ARC. A natural comparison is ITER
which also produces 500 MW of fusion power with a similar
shaping (ϵ ∼ 0.33), but with _B_ 0 ∼ 5.3 T. As expected from the
_B_ [4] 0 [dependence in fusion power density, the peak on-coil field of]
_Bcoil_, _max_ ∼ 20 T enabled by REBCO technology allows ARC to
achieve a FNSF/Pilot-relevant areal fusion power density (∼3
MW/m [2] ) in a device with roughly a tenth of ITER’s volume.
Additionally, as a consequence of the high toroidal field, the
ARC design point has double the safety factor of ITER, making
it more robust against disruptions. Looking at Eq. (13), we see
the high safety factor permits a reasonable bootstrap fraction of
∼75%, while staying below the no-wall beta limit. Thus, the
high toroidal field increases the bootstrap fraction, as well as
improves LHCD accessibility and efficiency (see Section 3.3).

This simultaneously provides the non-inductive solutions critical for an FNSF and an attractive _Qp_ ≥ 25, critical to a Pilot
power plant. It is worth noting that the above advantages of the
ARC over ITER come from a peak field ratio of only ∼ 1.5 between the two designs (this ratio becomes closer to ∼ 2 with the
ARC field from the more detailed analysis in Section 4). Energy confinement has not been considered within this scoping
because it is not a disruptive or operating limit. The effect of
confinement is discussed in Section 3.2.

_3.2._ _Plasma profiles and characteristics_

Due to the high field, compact nature of ARC we have chosen to explore the I-mode [30, 31] regime, which has produced excellent absolute and scaled performance in the highfield, compact tokamak Alcator C-Mod. I-mode is characterized by L-mode-like particle confinement and H-mode-like energy confinement [32], making it an attractive regime for reactor operations because it may allow for easier control of density
and impurities, critical control features for burning plasmas.
Another intriguing feature of I-mode is that it features weak
degradation of energy confinement time with heating power

[30], a highly desirable feature in a self-heated plasma. A
recent study [33] has confirmed a τ _e_ ∝ _P_ [−] _heat_ [0][.][27] scaling by examining a large database of I-mode plasmas, in comparison to
τ _e_ ∝ _P_ [−] _heat_ [0][.][69] for standard H-mode. Critically, because I-mode
has L-mode-like particle confinement properties, Edge Localized Modes (ELMs) are not required to control impurity content. ELMs are a relatively violent mechanism that regulates
impurities in H-mode discharges [34], but will be unacceptable
in burning plasma devices because they would likely damage
plasma-facing components. I-mode has its own high frequency
instability, the weakly coherent mode, which is suspected to
regulate edge impurity transport [35] while the plasma regime is
stationary, making it attractive for non-inductive operation. Simultaneously the lack of a density gradient results in stationary
regimes that are far from the ELM stability limit [33]. Therefore, I-mode has a much lower risk of large transient plasmamaterial interactions, which improves the wall and divertor lifetimes.
While I-mode has some attractive features for a fusion reactor regime, it must also be realized that there is significantly less
information regarding I-mode energy transport scaling, particularly with device size (although efforts are underway). Therefore, the ARC design will simply explore the use of scaled
density, temperature, and pressure radial profiles from I-mode
on C-Mod, rather than directly relying on global confinement
scaling laws for predicting performance. This approach also
allows us to evaluate how appropriate I-mode profiles are for
non-inductive reactor scenarios, since its weak density gradient
will have a strong effect on the bootstrap fraction compared to
standard H-mode. The resulting profiles needed to achieve the
design point will then be evaluated after the fact with respect to
required global scaling laws such as the H89 and H98(y,2) scalings as well as the total plasma gain (β _N_ _H_ / _q_ [2] ). We note that
this is a standard procedure for assessing fusion reactor performance (e.g. Ref. [2]).

As with the density, the temperature gradient is rolled off to zero
inside of ρ = 0.05. The C-Mod core gradient is ∼ 22 keV/m for
B = 5.4 T and _q_ 95 ∼ 3. The scaling in Eq. (17) reflects the
expectation that stored energy scales as _Ip_ (at fixed density),
but that the temperature profile scales weaker than linear with
heating power due to critical-gradient physics. Combining Eqs.
(16) and (17) near the ARC design point leads to _Wth_ ∝ _P_ [0] _heat_ [.][7] [,]
which is again consistent with C-Mod data [30, 33].
The temperature gradient scalings depend on _Pheat_ = _Pext_ +
_P_ α and _P_ α depends on the pressure profile. To determine _Te_ ( _r_ )
(and _Ti_ since we have assumed that _Ti_ = _Te_ ), the profile is
self-consistently iterated in the following way. Initially, the
total heating power is set to be the externally applied power,
![](images/page_007_eq_0.png)
_Pheat_ = _Pext_ = 25 MW based on the 0-D scaling. The temperature profile is then built as described above, and the fusion
power, _P_ _f_, is computed. The alpha heating power, _P_ α = _P_ _f_ /5,
is then added to the external heating power to compute a new
_Pheat_, which is used to build a new electron temperature profile

_3.2.1._ _Density and temperature profile scalings_
The density and temperature profiles (see Fig. 5) are generated using experimental scalings from Alcator C-Mod I-mode
profiles, with the assumption that _Ti_ = _Te_ . The density profile is calculated by setting an almost triangular profile achieving _n_ 0/ _ne_, _average_ ∼ 1.3 equal to the average of the C-Mod data

[30, 36] from 0 < ρ < 1, where ρ ≡ _r_ / _a_ . This omits the
density flattening effects of core sawteeth, which is appropriate
because ARC has _q_ - 1 everywhere. As in the 0-D design the
line-averaged density is not allowed above 90% of the Greenwald density limit. The gradient is rolled off to zero inside of
ρ = 0.05. Note that the extension of a constant slope _dn_ / _dr_ to
ρ = 1 is simply consistent with the lack of a particle transport
barrier in the edge, a feature that distinguishes I-mode from Hmode.
The electron temperature profiles are constructed inwards,
starting at ρ = 1.0, where the temperature is fixed to be 200
eV based on simple parallel heat conduction limits of the twopoint model [37]. From 0.95 < ρ < 1.0, the radial temperature
gradient is set according to an experimentally observed C-Mod
pedestal scaling at B = 5.4 T and _q_ 95 ∼ 3 [30, 36],

![](images/page_007_eq_1.png)
∇ _T_ _ped_ ≈ 70 _[B]_ [0]

_q_ 95

_Pheat_ / _S_ _p_, (16)

_n_ 20, _ped_

where _n_ 20, _ped_ is the pedestal density, _Pheat_ = _Pext_ + _P_ α is the
total heating power, _S p_ is the plasma surface area, and ∇ _T_ _ped_
is in units of keV/m. The factor _B_ 0/ _q_ 95 accounts for the experimentally measured linear increase of the pedestal gradient
with plasma current [33]. Note that _B_ 0/ _q_ 95 scales as _Ip_ since
ARC and C-Mod I-mode shots have very similar aspect ratio
and shaping [30].
From 0.05 < ρ < 0.95, a different core temperature gradient
scaling is used. This scaling is also based on experimentally
measured gradients in C-Mod [30, 36],

∇ _Tcore_, _ARC_ = ∇ _Tcore_, _CMod_

 - _qB_ 950 - _Pheat_ / _S p_ 

95 _ARC_

- _qB_ 950 - _Pheat_ / _S p_ 

. (17)

_CMod_

at a fixed density. The process is repeated until the fusion power
converges to within a few percent, indicating that the temperature profile and the heating power are consistent. The value of
_q_ 95 is chosen in these scalings such that the resulting heating
power is ∼ 500 MW.
The target final density and temperature profiles are shown
in Fig. 5 and the principle core parameters are listed in Table
1. Slight alterations to the 0-D point (see Section 3.1) were
made to accommodate evolving design choices. The inside
blanket/shield width was increased to ∆ _b_ = 0.85 m for magnet shielding (see Section 5.2). The major radius was increased
from _R_ 0 = 3.2 m to 3.3 m to help accommodate the larger ∆ _b_ .
Simultaneously, the peak field on coil was increased to _Bmax_ ∼
23 T based on a more detailed examination of the REBCO magnet limits (Section 4.1). This resulted in an on-axis field _B_ 0 =
9.2 T which was then fixed in the design. The core density was
decreased slightly to _n_ 20 = 1.3 for better CD efficiency.
The temperature and density profiles were built using the
rules stated above based on _B_ 0 = 9.2 T, the 0-D estimate _q_ 95 ∼
6, and total heating power _Pheat_ = 500 MW/5 + 25 MW = 125
MW. These values lead to a heating power density of _Pheat_ / _S p_ ∼
0.63 MW/m [2] . Equations (16) and (17) result in a pedestal temperature of ∼ 4 keV and a central temperature of _T_ 0 ∼ 26
keV (see Fig. 5). Coincidentally, the values of _B_ 0/ _q_ 95 ∼ 1.6,
_Pheat_ / _S p_, _n_ 20, and plasma shape are very close to the C-mod
I-mode shots used for the scaling (which was not by design),
and thus the assumed temperature gradients are also very close.
Therefore, at fixed gradient, the scaled temperature profiles in
ARC are ∼ 5 times larger than C-Mod simply due to the 5fold increase in linear size between ARC and C-Mod (C-Mod
I-mode has pedestal ∼ 800 keV and _T_ 0 ∼ 6 keV [30]).
The temperature and density profiles were required for input
into the ACCOME current drive and equilibrium code. Due to
the profile and geometry effects from the ACCOME equilibrium solution the design values were slightly increased: fusion
power _P_ _f_ = 500 to 525 MW, external power _Pext_ = 25 to 38 MW
(for sufficient current drive, see Section 3.3) and safety factor
_q_ 95 ∼ 6 to 7.2. These equilibrium results increase _Pheat_ / _S p_ by
15% and decrease _B_ 0/ _q_ 95 by 15% as compared to the starting assumptions for developing the profiles. Since these effects nearly cancel out and result in < 10% changes in the temperature and density profiles (which is within the uncertainty
of the scaling accuracy), no further iterations were performed.
The sensitivity of ARC performance to these uncertainties is
addressed in Section 3.5.
The ARC operating point has a volume-averaged temperature ⟨ _T_ ⟩∼ 13.9 keV and volume-averaged density ⟨ _n_ 20⟩∼ 1.3.
The on-axis temperature is _T_ 0 ∼ 27 keV and density _n_ 20 ∼ 1.75.
ARC has a β _N_ = 2.59, which respects the Troyon limit and a
1-D variant [38],

β _N_ ≡ _[aB]_ [0] β _T_ ≤ 4 _li_, (18)

where _li_ ≡ - _B_ [2] _p_ - / _B_ [2] _p_ [(] _[a]_ [)] [=] [0][.][67] [is] [the] [normalized] [inductance.]
The assumed I-mode pressure peaking _p_ 0/ ⟨ _p_ ⟩∼ 2.6 is modest
and also aids stability. Additionally, it should be noted that, un

like other aggressive reactor designs, this volume-average density is only 64% of the Greenwald density limit. This indicates ARC can readily explore various densities and associated
CD efficiency and divertor heat exhaust solutions around its design point without fear of a density limit disruption. Additionally, the operating point is accessible with the installed external
power and thermally stable, as shown by the plasma operating
contour plot given in Fig. 6. Based on the heating power density, _Pheat_ / _S p_, and volume-average plasma density at the operating point as well as I-mode experiments performed on C-Mod

[39] indicate that I-mode should be accessible in ARC. At the
minimum threshold of the experiments presented, I-mode may
be accessed by initially lowering the plasma density to _n_ 20 ∼ 1
and applying the installed heating power of ∼ 40 MW. The operating point is then reached by increasing the density through
fueling (due to L-mode particle transport) and the aid of the alpha heating. In fact, it may even be possible to access I-mode
directly at the operating volume-averaged plasma density given
the expected installed heating power with conditioned waveguides (see Section 3.6). Given its recent discovery, research
![](images/page_008_eq_0.png)
into I-mode is still required, as discussed in Section 7. It is
important to note that the use of I-mode in this study is not
primarily motivated by core fusion performance, but rather by
the absence of ELMs in a stationary regime. Stability analysis
of C-Mod I-mode pedestals [40] indicates they have considerable margin to the peeling (∼ factor of 2) and ballooning (∼
factor of 3) limits. While a dedicated pedestal stability analysis has not yet been performed for ARC, simple scalings indicate it will also be stable to ELMs. The ARC pedestal features
β _ped_ ≈ 0.4%, an increase of only 60% from the C-Mod _q_ 95 ∼
3.2 I-mode cases. The most universal metric for stability is the
Troyon-normalized pedestal pressure

_aB_
β _N_, _ped_ ≡ β _ped_, (19)

in units of %-m-T/MA. For an assumed pedestal width of r/a ∼
5% (typical of I-mode [40]), ITER and FIRE [41] reach stability
limits at β _N_, _ped_ = 1.09 and 1.16 respectively, while ARC is only
at β _N_, _ped_ ∼ 0.5, again indicating stability. While this treatment
is overly simple and does not consider the global stability of the
pedestal based on the pressure and current profiles, these trends
suggest the pedestal in ARC is away from ELM stability limits.
A critical open question is the expected pedestal width.
Despite these uncertainties, because of the absence of ELMs,
it is interesting to assess the compatibility of “I-mode-like” temperature and density profiles with current drive and bootstrap
current. The following sections investigate this compatibility
as part of designing a non-inductive scenario at modest β _N_ .

![](images/page_008_eq_1.png)

_3.3._ _Current drive physics_

The ARC reactor design utilizes a combination of RF power
in the “fast-wave” ion cyclotron range of frequencies (ICRF)
and the lower hybrid range of frequencies (LHRF) to heat the
plasma and shape the _q_ profile. ICRF is required to drive current efficiently in the core while lower hybrid current drive
(LHCD) provides increased efficiency for driving current near

Figure 5: Radial profiles of electron temperature and electron density at ARC.

Figure 6: Plasma operating contour plot, where the operating point, indicated by the star, requires an $n_0$ factor of 2.78 and is accessible and stable.

mid-radius and beyond. The goal of this combination of current drive methods is to create an 'advanced tokamak' (AT) q-profile, characterized by weak reverse magnetic shear. This provides self-consistency to higher confinement and also avoids dangerous instabilities.

![](images/page_009_eq_0.png)
LHCD is better than neutral beams or ICRF at driving current at mid-radius because of its high efficiency. The strategy for driving current at mid-radius is guided by the Vulcan study [13], which found a higher current drive efficiency from launching in regions of high magnetic field and better radial penetration from launching in a region of low poloidal field. This motivates HFS launch in regions of high flux expansion, such as the upper vertex of ARC's triangular plasma cross-section. The physical basis for this, as previously described in the Vulcan study, is briefly reviewed here.

A standard empirical characterization of current drive efficiency is given by Eq. (12). For the case of LH, the efficiency is determined in part by the phase velocity of the waves parallel to $B$ as they damp on electrons [42], and follows

$$\eta_{LH/D} \propto \frac{n_\parallel^2}{n_e} \tag{20}$$

![](images/page_009_eq_1.png)
Thus, it is advantageous to reduce $n_\parallel \equiv ck_\parallel/\omega$ as much as possible. The accessibility condition [43] provides the lower bound on $n_\parallel$, which limits the maximum achievable efficiency, and is given by

$$n_\parallel \geq n_{\parallel,\min} = \sqrt{1 + \frac{\omega_{pe}^2}{\omega_{ce}\omega_{ci}}} - \frac{\omega_{pe}}{\omega_{ce}} = \frac{\omega_{pe}}{\omega_{ci}^{1/2}\omega_{ce}^{1/2}} \tag{21}$$

![](images/page_009_eq_2.png)
where $\omega_{pe}$ is the electron plasma frequency, $\omega_{ce}$ is the electron cyclotron frequency, $\omega_{ci}$ is the ion plasma frequency, and $\omega_{pi}$ is the frequency of the LHRF waves. Thus, from Eq. (20), we find that

$$\eta_{LH/D} \propto \frac{B^2}{n_e} \tag{22}$$

This dependence on $B$ as well as the analysis below motivates the HFS launch of lower hybrid waves and the use of LHCD in a high-field tokamak. It should be noted that the choice of density is quite constrained in reactor regimes by the required plasma pressure, so lowering $n_e$ to increase efficiency is limited.

![](images/page_009_eq_3.png)
The physical motivation for launching near regions of high flux expansion is a direct result of the slow wave branch of the cold, electrostatic lower hybrid dispersion relation [13],

$$n_\perp^2 = \frac{\omega^2}{c^2} \frac{k_\perp^2}{k^2} \approx -\frac{S}{P} \left(n_\parallel^2 - P\right) \tag{23}$$

in the limit of $\omega^2 \ll \Omega_{pe}^2$. Differentiating Eq. (23) with respect to the wavenumber $k$ yields the group velocities in a given direction. Of particular concern is the radial, $v_{gr}$, and poloidal, $v_{g\theta}$, propagation velocities as these determine how far the wave will penetrate into the plasma before damping. The ratio of these velocities can be shown [13] to be

![](images/page_009_eq_4.png)
$$\frac{v_{g\theta}}{v_{gr}} = \frac{n_r}{n_\theta} \frac{n_e \cdot B_r}{n_r \cdot B_\theta} \tag{24}$$

where $n_r \equiv ck_r/\omega$, $k_r$ is the radial wavenumber, and $B_\theta$ is the poloidal magnetic field. This condition shows that for good effective radial penetration, lower hybrid systems should tend toward higher launch frequency, lower $n_r$, larger $B$ and lower $B_\theta$. Thus near the high-field poloidal null point, where lower $n_r$ is accessible and $1/B_\theta$ is maximum, is optimal for the best radial penetration of the LH slow wave rays. However, the resonant Landau damping condition [44],

$$n_\parallel^2 \leq \frac{35}{T_{keV}} \tag{25}$$

limits the radial penetration of slow lower hybrid waves. At the magnetic axis of ARC, the maximum $n_\parallel$ that is not Landau
![](images/page_009_eq_5.png)

damped is 1.2, while the minimum accessible $n_\parallel$ on axis is approximately 1.6. Therefore, slow lower hybrid waves will damp at mid-radius and cannot penetrate to the magnetic axis. Therefore, fast-wave drive using frequencies near the ion cyclotron resonance have been chosen for on-axis CD. However, it should be noted that EC current drive would also be attractive for central current drive if the high frequency sources (~300 GHz) were available to avoid cutoff issues.

The decay wavenumber for ICRF waves increases significantly off-axis, implying a significant increase in absorption because of the dependence on density and temperature given by [45]

$$2k_{i,\text{Im}} = \sqrt{\frac{2}{\pi}} \frac{\epsilon_R \omega_{ci} \epsilon_{R0}}{v} \beta_{i0} G_r \exp\left(-\frac{\xi_r^2}{2}\right), \quad (20)$$

where $G_r = \omega_{ci}/\omega / B_r$ and $\beta_i = 2\mu_0 n_i T_i / B^2$ is the local electron plasma beta. This shows the absorption of $\epsilon_r$ is proportional to $\omega_{ci}/\omega$, $n_i^{1/2}$, $T_i^{3/2}$, and $B^{-3}$. The dependence on the magnetic field also motivates high field side ICRF launch, as more of the wave energy will penetrate to the axis. Not only does this localize the current drive in the core, but it also increases the efficiency of current drive because of the dependence on the electron temperature [46]. In general, the ICRF fast wave will always weaken single-pass damping in high-field designs such as ARC because of the $B^{-3}$ dependence of the damping.

![](images/page_010_eq_0.png)
## 3.4. Current drive modeling using ACCOME

Using HFS launch as a starting point, the current drive and plasma performance were modeled using the ACCOME code [47], a 2-D, self-consistent, fixed-boundary, magnetic equilibrium solver. The code takes coil locations and plasma parameters, including the bootstrap temperature profile, as inputs (see Section 3.2.1). It then iterates with current drive modules to find a self-consistent solution to the MHD equilibrium as given by the Grad–Shafranov equation [48, 49]. The code can model various current drive methods, including LHCD and current drive due to bootstrap effects; however, there is no module for simulating ICRF current drive. Instead, a fast wave power deposition profile is assumed that has a volumetric power deposition centered on axis and a broad radial distribution based on evaluating Eq. (26). The magnitude of the power deposition on axis is chosen to give an integrated ICRF-driven current totaling 1.1 MA.

For lower hybrid current drive, the source frequency, launcher position, $n_\parallel$, and a 'Fisch–Karney-peaked' current in tokamak' current profile [2] is desired, characterized by weak reverse magnetic shear throughout the plasma, so the lower hybrid waves are required to damp primarily at mid-radius to supplement the current drive profile from ICRF and bootstrap current. In the optimization, the lower hybrid source frequency, launched $n_\parallel$, and launcher position were all varied. ACCOME results showed that the current drive efficiency is sensitive to the launch frequency. A fixed $n_\parallel$ value was used. At 8 GHz, it was seen to avoid parasitic damping on alpha particles, which occurs when the parallel phase velocity of the wave velocity is slower than the alpha-birth velocity. For a fixed $n_\parallel$, $v_\parallel$ is proportional to the

launch frequency. At 8 GHz, the entire coupled power of 25 MW contributes to driving current, while at 5 GHz as much as 20% of the injected power is lost to alpha particles. This shows at higher launch frequencies less power parasitically damps on alpha particles since $v_\parallel$ is higher than the birth speed of the alphas. Fig. 7 demonstrates that higher frequencies drive more current and penetrate farther radially.

[Figure 7: Lower hybrid driven current density for the design wave frequency of 8 GHz and several other frequencies as a function of normalized minor radial location.]

The launched $n_\parallel$ was varied between 1.4 and 1.7 for the ACCOME calculations. As shown in Eq. (20), LHCD efficiency increases with decreasing $n_\parallel$, therefore it is advantageous to minimize $n_\parallel$. However, the optimized launched $n_\parallel$ is found to be 1.67 with a small spectral width, $dn_\parallel = 0.05$. Decreasing the initial $n_\parallel$ below this value causes the fast-wave cutoff to be inaccessible. In Fig. 8 we see the consequences of this. The wave is launched inward, reflects back to the plasma edge, reflects again, and finally damps. In contrast, Figs. 9 and 10 show the wave trajectory in ARC, which propagates directly towards the magnetic axis and damps at mid-radius. Remember that a current drive efficiency depends on the $n_\parallel$ where the wave damps, not where it is launched. In ARC, the launched $n_\parallel$ of 1.67 outperforms a lower launched $n_\parallel$ as the wave penetrates without dramatic upshifts to a mid-radius location where a combination of poloidal magnetic field and toroidal effects cause a gradual downshift of $n_\parallel$, as shown in Figs. 9 and 10.

Throughout the ACCOME runs, the launcher position had a major impact on equilibrium convergence as well as the ability to drive current at mid-radius. The launcher position determined whether the waves could propagate radially, upshift, convert to fast waves, and/or reflect. Various positions were tested, ranging from the midplane to regions of high flux expansion (Fig. 11) demonstrates the high variability in ray trajectories resulting from varying only the launcher position. It is noted that ARC overcomes a commonly perceived limitation that LH cannot penetrate to current-drive radii (e.g., at $\rho \sim 0.9$–0.95 in ARIES-AT). Effective current drive at $\rho \sim 0.5$ is achieved in ARC by a) taking advantage of a) larger magnetic fields improving accessibility, b) employing HFS launch

![Figure 8: An example of the evolution of the parallel index of refraction when](images/tmpc7ciscuc.pdf-11-0.png)
violating the wave accessibility limit (see Eq. (21)), where blue represents the
wave _n_ ∥ along the trajectory and orange represents the critical value determined
by the local accessibility limit.

Figure 9: Evolution of the parallel index of refraction with propagation for the
launch conditions in ARC, where blue represents the wave value and orange
represents the critical value determined by the accessibility limit. Note that this
follows the ray until 99% of its energy is damped.

(which further improves accessibility and avoids damping at a
low temperature by launching at lower _n_ ∥), and c) the choice of
the poloidal launcher position to optimize the variation in _n_ ∥ as
the wave propagates.
At an _n_ ∥ of 1.7, damping will occur on electrons with a temperature of approximately 14 keV. This can be seen by comparing the peak in the LHCD profile in Fig. 12 with the temperature profile in Fig. 5. Note that the minor radius location of the
current peak roughly corresponds to the location where _Te_ = 14
keV (i.e. _r_ / _a_ = 0.6). This indicates that HFS LHCD is well
suited to a compact device where, due to confinement concerns,
⟨ _T_ ⟩∼ 14 keV is chosen to maximize the Lawson triple product.
Since ⟨ _T_ ⟩ approximately corresponds to the mid-radius T, efficient mid-radius CD naturally follows.
The safety factor profile calculated by ACCOME is plotted
in Fig. 13, showing an elevated edge safety factor and an onaxis safety factor greater than 3. Thus, ARC should avoid the

![Figure 10: ACCOME plasma equilibrium for ARC with the LHCD wave trajectory indicated in black. Each red tick mark along the ray trajectory indicates](images/tmpc7ciscuc.pdf-11-1.png)
a 10% decrease in the wave power due to electron Landau damping.

ballooning kink mode at the edge, the sawtooth instability on
axis, and low-order tearing modes (2/1, 3/2) (although an ideal
MHD stability analysis would be required to confirm ballooning stability). As previously noted, the profiles operate below
the no-wall Troyon limit. At the safety factor profile above,
the ratio of the banana orbit width to minor radius is approximately double that of ITER. However, this is not expected to
lead to prompt losses of fast-birth alpha particles (with banana
orbit width of ∼ 0.1m). Furthermore, ARC lacks energetic particles in the edge from beam heating. Therefore it is judged
that the high safety factor is justified in order to avoid global
disruptions.

In addition to solving the MHD equilibrium equations, ACCOME also calculates the global plasma and current drive performance. The code estimates a fusion power of 525 MW for
the plasma equilibrium obtained. ACCOME calculates that 25
MW of coupled lower hybrid current drive power will drive
1.77 MA and the total plasma current will be 7.75 MA after
including 1.1 MA from ICRF. This corresponds to a bootstrap
fraction, _fBS_, of approximately 63% and a lower hybrid efficiency, η _LHCD_, of 0.4 × 10 [20] _AW_ [−][1] _m_ [−][2] . This efficiency is somewhat below the 0-D estimate of ∼ 0.5 × 10 [20] _AW_ [−][1] _m_ [−][2] because
of trapped particle effects (estimated in ACCOME) at r/a ∼ 0.6.
For a design like ARIES-AT, the loss of efficiency due to trapping would be larger because r/a ∼ 0.9-0.95 (although these corrections were not included [50]). Minimizing these deleterious
trapping effects is another motivation for high magnetic fields
and HFS launch, since edge damping can be avoided.

The ICRF current drive is assumed to have a similar efficiency to the ideal lower hybrid current drive efficiency of
0.43 × 10 [20] _AW_ [−][1] _m_ [−][2] . This choice is based on the following considerations. The ICRF source frequency was chosen

![](images/tmpc7ciscuc.pdf-11-2.png)

[Figure 11: Lower hybrid ray traces for non-optimized launch locations; (a) midplane launch, (b) launch halfway between the midplane and the upper extremity of the plasma, and (c) launch near the lower null. The red X's represent the location of each 10% reduction in wave power due to damping.]

[Figure 12: Current profiles in ARC, with the total current (black, solid), the low cyclotron current drive (red, dashed), the bootstrap current (green, dashed dotted), and the lower hybrid driven current (blue, dotted) shown.]

[Figure 13: Safety factor profile in ARC.]

to be 50 MHz (similar to the ITER ICRF system [51]) in order to place the wave frequency below any fundamental or second harmonic ion cyclotron resonances. Furthermore, damping of the ICRF wave (given by Eq. (26)) maximizes for $\zeta_c = \omega/k_{||} v_t = 0.7$. For ARC parameters, this implies that we must have $n_{||} = 4.4$ on axis and $n_{||} = 3.3$ at the antenna. Using Fig. 2(a) of Ref. [46], the ICRF current drive efficiency can be estimated to be $0.4 – 0.5 \times 10^{20} AW^{-1}m^{-2}$ for a narrow spectrum of Landau damped ICRF waves, with $T_e(r_{res}) = 0.05$ and $p_\parallel/(m_e c_s) = 1/n_{||} = 0.25$. This efficiency leads to a required coupled power, $P_{IC}$, of 13.6 MW to drive 1.1 MA of ICRF current in ARC. Self-consistency between the MHD equilibrium and the current drive sources was achieved by allowing AC-COME to iterate between the solution of the Grad-Shafranov equation and a re-evaluation of the current drive sources [40]. The plasma equilibria for several iterations are shown in Fig. 14, demonstrating that, for the coil configuration and plasma current drive system chosen, the wave trajectory is anticipated to be stable to small changes in the equilibrium.

At this point, the relatively broad characteristic width assumed for the ICRF current density profile deserves further discussion. It can be seen in Fig. 12 that this corresponds to a $\delta r(a) = 0.4$. The parameters of ARC result in $2L_{||} \Delta R = 0.16$ for a single pass. This is calculated using $\Delta R = a/2 = 0.5$ m and Eq. (26), evaluated on axis with $f_{ICRF} = \omega_{ICRF}/(2\pi) = 50$ MHz, $m_i = 4.4$, $\zeta_c = 0.7$, and $\beta_t = 0.02$. The resulting single pass damping following Ref. [45] is then $1.0 – \exp(-2L_{||} \Delta R) = 0.15$. Therefore, the ICRF wave requires several passes through the plasma before the power is absorbed completely. This results in the relatively broad deposition profile with a damping profile that might even be characterized by

'eigenmode' features.

## 3.5. ARC Sensitivity to Confinement Quality

Energy confinement is almost always a constraint on achieving fusion performance, but this is particularly true at small scale where the plasma dimensions are forced to be smaller due to basic physics considerations. For ARC the 525 MW design point (see Table 1) minimizes the necessary energy confinement time, by operating at the minimum in the triple product Lawson criterion $T = 14$ keV. The calculated confinement quality is $H_{98} = 2.8$ for the design point, which is 40% above standard H-mode. However, this is common to reactor designs using AT plasmas [2, 50]. Such high confinement is justified by the theoretical expectation and experimental confirmation that weak shear q profiles and the lack of low-order rational q surfaces (q$_{min}$ > 2) lead to enhanced confinement factors. For example, DII-D achieved $H_{89} = 2.5 – 3$ under such conditions with an internal transport barrier [52]. Section 3.4 demonstrates that the computed q profile in ARC meets this criteria.

(a) (b)

Figure 14: The (a) initial and (b) final MHD equilibrium from ACCOME,
demonstrating the stability of the wave trajectory to variations in the plasma
equilibrium.

An even better measure of confinement would be the gain
factor [53]

_G_ ≡ [β] _[N]_ _H_, (27)

_q_ [2] 95

which provides a global assessment of the plasma physics dimensionless parameters required to meet the Lawson criterion
according to

_HB_ 0
_nT_ τ _E_ ∼ _pth_ τ _E_ ∼ β _N_ _B_ [2] 0 = _GB_ [3] 0 [.] (28)

_q_ 95

Substituting the values for ARC (calculated from computational
results in Section 3.4) gives an expected gain factor, _G_ 89, of
0.14 (or a _G_ 98 factor of 0.08) due to the low β _N_ and high _q_ 95 in
ARC. These gain factors have been achieved in non-inductive
scenarios in several tokamaks including DIII-D and JT-60 [52].
In fact, the representative weak shear DIII-D experiment chosen
in Ref. [52] and the stationary states reported in Ref. [54] have
nearly identical plasma parameters to the ARC design point.
Thus, ARC is unique among recent conceptual tokamak designs
(including those cited in Ref. [54]) in operating at previously
achieved gain factors. That being said, unlike DIII-D and JT60, ARC lacks neutral beams to drive plasma rotation, which
could have important consequences for confinement.
Nevertheless it is prudent to examine the effect of confinement quality on the ARC FNSF/Pilot plant mission. The results of a 0-D scoping for ARC are shown in Fig. 15 and were
carried out in the following manner. The total fusion power
![](images/page_013_eq_0.png)
is scanned by scaling the volume-averaged pressure ( _P_ _f_ ∝ _p_ [2] _th_ [)]
obtained from the _P_ _f_ = 525 MW baseline case. Simultaneously
the plasma current, volume-averaged density and shaping are
kept constant. Keeping these parameters fixed has the simplifying benefit of maintaining the same Greenwald density fraction
(well away from the limit) and current drive efficiencies. The
power/pressure scan is thus equivalent to a β _N_ scan or a ⟨ _T_ ⟩ scan
for the core plasma. This results in a variable bootstrap fraction. Here we have used the approximation from Sauter [55]
that 2/3 of the bootstrap current arises from the density gradient, which is fixed during the scan. The external power, which
is assumed to be used entirely for current drive, is modified to
assure unity non-inductive fraction. The heating power can be
set to _P_ α + _PCD_, which are both known, after which the plasma

![](images/page_013_eq_1.png)

gain and H factors can be recalculated. Since ARC operates far
from the kink limit and at the Troyon limit (see Table 1), it is
always advantageous to increase the plasma current because it
allows the device to confine more plasma pressure. Therefore,
any power needed to heat the plasma will always be injected
using the current drive system.
As can be seen in Fig. 15, _H_ 89 ∼ 2.2 results in only ∼ 200
MW of fusion, but this still meets general requirements for an
FNSF (steady state neutron flux density ∼ MW/m [2] ) and a Pilot
plant ( _Qe_ - 1), albeit with more modest performance. Therefore a general conclusion is that the ARC mission can be met
over a range of confinement quality _H_ 89 ∼ 2.2 − 2.8, spanning
from roughly standard H-mode confinement to “AT” confinement. The use of I-mode confinement may be beneficial to
achieving a burning plasma because it degrades more weakly
with heating power (τ _E_ ∼ _P_ [−] _heat_ [0][.][3][).] [This] [partially] [explains] [why]
the C-Mod I-mode, when scaled up to ARC, produces such a
high _H_ 89 factor. Designing ARC at a higher total current would
also improve confinement. There is considerable margin to
lower safety factor from _q_ 95 ∼ 7, but this could increase the fusion power too far past 500 MW and require reassessing the current drive. This path is left for future studies. Ultimately, global
confinement scalings are a crude tool to anticipate performance
and what is really required is a better predictive pedestal model
coupled to a core gradient model.
It is noted that improved confinement (over standard Hmode) is also expected from theoretical considerations due to
reduced turbulent transport from weak q shear as well as the
lack of low order rational q surfaces. In Ref. [52] the improved
confinement factor was observed to decrease back to _H_ 89 ∼ 2.2
(from 2.5 − 3) when the _q_ = 5/3 surface entered the profile.
Therefore one would estimate that the most important design
tool is sufficient current profile control. This is central to ARC,
where optimized CD efficiency (through high-field side launch)
and lower bootstrap fraction are paramount to the design. Indeed with reduced fusion power there is a tendency to gain more
external control of the q profile (see Fig. 13), which will permit
more control of the current profile. This control can be used to
improve confinement, thus providing a positive feedback for fusion power. An additional note is that a variety of fusion powers
should be considered because the quantitative limit on plasma
heat exhaust, driven by _Pheat_ / _S p_ and the radiated power fraction, is unknown.

_3.6._ _Conceptual engineering of current drive systems_

The chosen lower hybrid source frequency of 8 GHz allows
the industry standard waveguide, WR-112, to be used for the
transmission system. Access to the vacuum vessel will be provided through the hollow posts that support the vacuum vessel in the FLiBe. The launcher horns will be similar to those
discussed in the Vulcan study [13], except that, instead of having discrete launching structures distributed toroidally, the ARC
reactor will use two toroidally-continuous strips of alternating
active-passive waveguides [56, 57]. The use of toroidal continuous launchers will maximize spectral control, which is desirable for CD control. These two strips provide up to 40 MW

![](images/tmpc7ciscuc.pdf-13-0.png)

![](images/tmpc7ciscuc.pdf-13-1.png)

| Location | Power Output |
|----------|-------------|
| Wall plug | 69.6 MW |
| Klystrons | 34.8 MW |
| Cold waveguide | 30.0 MW |
| Hot waveguide | 28.0 MW |
| LHRF launcher | 25.0 MW |

*Table 2: Power invasions throughout the lower hybrid system.*

of LHCD with conditioned waveguides, nearly double that required for steady state operation. The effective launched power density exceeds 30 MW/m², a benefit of high frequency RF, and the launchers comprise a small fraction (~ 1%) of the ARC inner wall. A schematic of LCHD waveguide integration into the ARC reactor design is shown in Fig. 16, and the power budget is given in Table 2. The klystrons are assumed to have a conversion efficiency of 50% [58]. The attenuation coefficient $\alpha_e$ in the waveguide depends on resistivity according to [59]

![](images/page_014_eq_0.png)
$$\alpha_e = \frac{1}{ab} \sqrt{\frac{\omega_0^2}{\mu_0}} \left[ \frac{1+\frac{2b}{a}\left(\frac{\omega_c}{\omega}\right)^2}{\sqrt{1 - \left(\frac{\omega_c}{\omega}\right)^2}} \right]$$

(29)

where $\omega_c$ is the waveguide cut-off frequency, $\omega$ is the wave launch frequency, $a$ and $b$ are geometric constants of the waveguide, $\mu$ is the conductor permeability, $\sigma$ is the conductivity, $\eta = \sqrt{\mu/\varepsilon}$ is the medium impedance, and $\varepsilon$ is the permittivity. Since conductivity decreases (and resistivity increases) with increasing temperature, hot waveguides have significantly higher losses than cold waveguides. This motivates placing the launcher close to the support posts and is the primary reason for optimizing the launch location around the upper region of flux expansion rather than the lower (genetic X-point). It is important to note that the full effect of high gamma-radiation fluxes to the high frequency, high power density waveguides is unknown and could possibly limit achievable power density in the waveguides. Neutron irradiation will also increase the resistivity of the waveguides, but it may be possible to anneal some of this radiation damage by operating the waveguides at a higher temperature. Both of these effects motivate investigation into finding the optimal operation and location for the LHCD in a radiation field, and are discussed in further detail in Section 7.

This LH system has several advantages. First, the extra installed capacity will ensure enough current drive is available in the event of individual waveguide failures. The additional power can also be used to assist in plasma start-up, reducing load on the central solenoid, and to overdrive the plasma to recharge the central solenoid. Other lower hybrid designs incorporate phasing of launchers to better control the plasma current distribution [13, 57], but, instead of phasing entire launching structures at discrete toroidal locations, this design allows for continuous phasing of individual waveguides in the toroidal location. This added flexibility could allow current to be driven at

---

[Figure 15: Result of ARC 0-D sensitivity scan organized versus fusion power. The grey vertical line is the design point of $P_f = 525$ MW. Table 1 shows values of the parameters kept fixed during the scan: $T_e$, $R_0$, shape $\kappa_{95}$, and non-inductive fraction $f$. The four graphs show (a) the plasma and electricity multiplication factors, (b) the global plasma density for neutrons and heating, (c) the normalized beta $\beta_N$ and current drive fraction, and (d) the calculated normalized confinement qualities $H89$ and $H98(\gamma, 2)$ consistent with fusion performance. Note that $Q_e$ in (a) is calculated using the 50% thermal efficiency of the "aggressive" Pilot phase. The arrows point to the relevant axis for a given curve.]

![Figure 16: Schematic of the hot and cold portions of the LH waveguides (not](images/tmpc7ciscuc.pdf-15-0.png)
to scale and shown as straight for simplicity).

a specific poloidal location, in addition to a specific minor radial
location. Also, the precise phasing of neighboring waveguides
provides the narrow spectral width of the launched power spectrum assumed for the ACCOME simulations. Additionally, the
active-passive configuration allows for enhanced cooling of the
active waveguides by pumping coolant through the neighboring passive waveguides. The material (often copper and aluminum) and dimensions of the waveguides allow them to behave as fins, leading to high heat transfer rates. As discussed in
Vulcan [5], one of the greatest advantages to HFS launch is that
the launcher is in the good curvature region, which minimizes
plasma-material interactions.

The ICRF launcher system will follow a similar design to
the lower hybrid system. However, since ICRF waves can be
transmitted with simple coaxial cables, the transmission line
losses will be negligible. Additionally, ICRF sources (50 − 80
MHz) are more efficient than the envisioned sources for the 8
GHz lower hybrid waves, motivating an assumed source efficiency of approximately 70% [50]. Combined, this results in
a required wall-plug power of 19 MW, only 1.4 times greater
than the plasma-coupled ICRF power. The exact location of the
ICRF launchers has not yet been optimized with respect to the
device geometry, source frequency, wave trajectory, and wave
damping because it requires advanced simulation tools beyond
ACCOME. As with the LH launchers, the ∼ 13 MW ICRF antennae only occupy a very small fraction of the first wall.

_3.7._ _ARC as an inductive burning plasma_

While ARC was designed to operate under non-inductive
scenarios (see Sec. 3.1), evaluating its performance as an inductive burning plasma experiment is informative. The following
0-D exercise allows for a more straightforward comparison to
lower magnetic field, inductive burning plasmas such as ITER
( _B_ 0 = 5.3 T). Here ARC is assumed to operate with a monotonic
sawtoothing ( _qmin_ ∼ 1) current profile and thus have standard
confinement factors. The operating current of ARC is scanned
while the Greenwald fraction ( _fGr_ = 0.9), plasma shape, and
auxiliary heating is fixed at the standard ARC values (see Table
1). The required current is determined such that the device produces a fusion power of _P_ _f_ = 525 MW (and a plasma gain of
_Qp_ ∼ 13.5), consistent with a burning plasma mission. Following the _H_ 89 confinement scaling, we obtain: _H_ 89 = 2, _Ip_ ∼ 10.8
MA, _qa_ ∼ 3.6, _n_ 20 ∼ 1.9, and ⟨ _T_ ⟩∼ 10.5 keV. Following the
_H_ 98 confinement scaling we obtain: _H_ 98, _y_ 2 = 1, _Ip_ ∼ 12 MA,
_qa_ ∼ 3.3, _n_ 20 ∼ 2.1, and ⟨ _T_ ⟩∼ 9.4 keV. This compares favorably to ITER: _H_ 98, _y_ 2 = 1, _Ip_ ∼ 15 MA, _qa_ ∼ 2.5, _n_ 20 ∼ 1,
_fGr_ ∼ 0.9, _P_ _f_ = 500 MW, _Qp_ = 10. We see that ARC provides
larger margins to the disruptive safety factor and density limits,
a natural advantage seen in many high-field compact devices
(e.g. BPX [60]).

**4.** **Magnet design**

A central aspect of the ARC conceptual design is exploring
possible fusion reactor/FNSF scenarios at the much higher field
afforded by REBCO superconductors. It is imperative to explore these new magnet designs to understand the tradeoffs and
limitations. The magnet system, shown in Fig. 17, is divided
into four groups: toroidal field (TF) coils, poloidal field (PF)
coils, the central solenoid (CS), and auxiliary (AUX) coils. The
first two groups are steady state superconducting magnets that
provide the required magnetic fields for stability, shaping, and
startup. The large Lorentz forces on the superconducting coils
are supported by stainless steel 316LN structure. The demountable TF coils have been designed to provide a magnetic field of
9.2 T on axis, with a peak field of 23 T on coil, and their conceptual design has been introduced in Ref. [61]. The CS will
be used primarily for inductive startup of the plasma current.
While ARC is designed for a non-inductive scenario, the CS is
very useful for off-normal plasma current control. The auxiliary (AUX) coils are copper magnets that carry relatively small
currents for real-time shape adjustments. Located close to the
plasma, just on the outside of the vacuum vessel, these coils allow for quick feedback to the plasma shape and constitute the
main fast response magnetic control system.

_4.1._ _Superconductor choice_

To obtain 9.2 T on axis, the maximum magnetic field in the
conductors in the TF coils will be 23 T at the inboard midplane.
As shown in Fig. 18 (compiled by P.J. Lee [62]), at these large
magnetic fields, subcooled REBCO outperforms other welldeveloped superconductors such as NbTi and Nb3Sn. At 23 T

![Figure 17: Schematic design of the coil systems, including: 1 – outward force](images/tmpc7ciscuc.pdf-16-0.png)
support ring; 2 – top demountable leg of the TF coils; 3 – PF coils (in green); 4

- outer bolted joint between TF coil legs; 5 – bottom leg of the TF coils; 6 – TF
coil winding pack; 7 – glass-filled epoxy reinforcement plug; 8 – TF electrical
joints; 9 – AUX coils (in red); 10 – plasma; 11 – CS and bucking cylinder. The
superconducting cables in the TF coils are shown in brown, within the steel
support structure.

and 4.2 K, the critical current density of REBCO tape superconductors produced by SuperPower Inc. is between one and
two orders of magnitude higher than Nb3Sn, making REBCO
the best superconductor for ARC TF coils.
Fig. 19 shows a schematic view of the cross section of commercially available REBCO tape conductor by SuperPower Inc.
The conductor is mostly composed of copper and Hastelloy,
with a very thin layer (approximately 1% of the total thickness)
of REBCO superconductor. The buffer layers are used during
manufacturing to orient the REBCO crystals in a preferred direction, such that the c-axis of the crystals are perpendicular to
the face of the tape [63]. The critical current density of REBCO is very sensitive to the orientation of the magnetic field.
It is maximized when the magnetic field is parallel to the tape
surface ( _B_ ⊥ _c_ ) and minimum with the magnetic field perpendicular to the tape surface ( _B_ ∥ _c_ ). To achieve the largest possible critical current, ARC uses REBCO tape oriented parallel
to the toroidal magnetic field ( _B_ ⊥ _c_ ) in the inner leg of the TF
coils.
REBCO is a high temperature superconductor, meaning it
can operate at temperatures up to about 80 K, much higher than
the 4.2 K necessary for Nb3Sn. However, we operate the REBCO at 20 K, meaning it is “sub-cooled” and far from its critical temperature. Like Vulcan, ARC features finite-resistance
joints between REBCO tapes at the locations where the coils
demount. Operation at 20 K, rather than 4.2 K, has several
operational advantages: a) the overall thermodynamic cost of
cooling, including the resistive joints, is reduced, b) the thermal
stability of the coil is greatly enhanced because the heat capacity of materials is much higher (nearly eighty times higher in

![Figure 18: Engineering critical current density as a function of applied magnetic field for commercially available superconductors at 4.2 K. High temperature superconductors (REBCO, shown in the figure as YBCO, and BSSCO)](images/tmpc7ciscuc.pdf-16-1.png)
have orders of magnitude higher critical current density than standard Nb3Sn at
local fields > 20 T and their critical current decreases weakly with _B_ . Note that
the orientation of the tape relative to _B_ [⃗] alters the REBCO critical current. Plot
compiled by P.J. Lee [62].

Figure 19: Schematic, not to scale, view of the cross section of REBCO tape
superconductor by SuperPower Inc. Each layer is shown with its typical thickness. The tape is typically available in widths between 2 and 12 mm, and a total
thickness of about 0.1 mm.

![](images/tmpc7ciscuc.pdf-16-2.png)

the case of copper [64], between five and ten times higher for
Hastelloy [65] and steel [66]), and c) coolants other than liquid helium can be used (e.g. liquid hydrogen, liquid neon, or
helium gas). There are a variety of demountable joints, such
as butt and edge joints [67] and bridge lap joints [68], however
“comb-like” joints [61] were ultimately selected for the ARC
conceptual design (see Section 4.2.2).

_4.2._ _Toroidal field coils_

The TF coil system is composed of 18 demountable TF coils
with stainless steel 316LN structure, which has been well characterized for use in superconducting coils [69]. The shape of
the coils is based on the constant tension Princeton D-shape

[70]. The magnets are cooled to 20 K, an operating point chosen based on the Vulcan findings of the minimum total capital and operating cost for superconductor and cryoplant volume

[15]. The TF coil is divided into two parts: a removable upper
leg and a stationary lower leg. The joints are located at the outer
midplane and the top of the coils, as shown in Fig. 17. The legs
are bolted together in the outer joint and a steel tension ring
serves as structural support for the top joint.
The TF coils are composed of a winding pack and a stainless
steel coil case. The winding pack consists of a set of 120 jacketed superconducting cables, described in Section 4.2.1. The
inner leg of each TF coil is supported by bucking against the
central solenoid and bucking cylinder, and shear keys placed between adjacent TF coils help support the overturning moments
in the central column. The vertical axis area ( _R_ = 0–0.45 m)
is filled with a glass-filled epoxy plug to reduce the maximum
stresses in the inboard side of the central solenoid and TF coils.
The epoxy was chosen such that it does not influence the magnetic field from the central solenoid, which acts as an air-core
solenoid.

_4.2.1._ _Superconducting cables performance_
To generate an on-axis toroidal magnetic field of 9.2 T, the
net current in each TF coil must be 8.4 MA. This current is
carried by 70 kA REBCO cables, each composed of a stack of
12 mm wide, 0.1 mm thick REBCO tapes. The cables are built
with the cable-in-conduit conductor (CICC) method: the superconducting tapes lay in grooves in an extruded copper stabilizer,
forming a cable that is surrounded by a square steel jacket. The
square steel jacket is 40 mm x 40 mm. The coolant flows in
cooling channels extruded in the copper stabilizer.
The coil insulation is similar to the K-STAR design [71].
Each CICC cable will be insulated by wrapping Kapton and S2
glass around them. The total stored magnetic energy in the TF
coil system is approximately 18 GJ and the maximum expected
quench voltage is 2 kV. The required insulation thickness to
withstand this voltage is about 2 mm.
The coils are graded, to leverage the increased critical current with lower magnetic fields. The amount of superconductor
is chosen such that the current density never exceeds 50% of
critical current density in the layer. The amount of copper in
each layer is determined by requiring that the conductor stays
below 200 K during a current quench (see Ref. [72], pp. 471–
475). The remainder of the cross section of the cable is made of

stainless steel. A plot of the cable composition in each layer,
including the copper stabilizer and structural steel, is shown
in Fig. 20. The first layer corresponds to the layer closest to
the plasma (subject to the largest magnetic field) and the last
layer is the outermost. Additional structural steel is required
for the coil case and reinforcements, but those components are
not taken into account in Fig. 20. The average composition of
the winding pack (by area) is: 45.9% copper, 46.1% steel, and
8.0% REBCO tapes (corresponding to a stack of 106 REBCO
tapes of 12 mm width). The winding pack current density, including the copper and steel area, is 44 A/mm [2] . In addition to
the factor of two margin already enforced on the critical current,
there is substantial margin in the operating temperature. At full
current, the temperature can increase by 10 K and the tape will
remain superconducting.

Figure 20: Winding pack composition of the TF coil as a function of layer
number. The three components of the winding pack are the steel jacket, copper stabilizer and REBCO tapes. Layer #1 corresponds to the layer closest
to the plasma (subject to the largest magnetic field) and layer #15 is the outermost. The amount of superconductor required for the outermost layers is
slightly larger due to the larger magnetic field perpendicular to the REBCO
tape plane near the ends of the central solenoid (see main text for details).

The minimum engineering critical current density in the coil
occurs in outermost layer (layer #15 in Fig. 20), at the inner leg
of the TF coil, close to the end of the central solenoid. In that
area, the toroidal component of the magnetic field (parallel to
the REBCO tape plane) is much lower than the radial component caused by the end effects of the CS (perpendicular to the
REBCO tape plane). In this situation, at 20 K, with a perpendicular magnetic field of 4.2 T and a parallel magnetic field of
0.8 T, the critical current density of REBCO is estimated to be
815 A/mm [2] . For comparison, Table 3 shows the largest components of the magnetic field in layers #1, #7 and #15, with
the resulting critical current of REBCO oriented parallel to the
toroidal field at 20 K.
The critical current of REBCO superconductors is expected
to increase as the technology continues to evolve. The average
critical current density of REBCO tapes produced by SuperPower Inc. increased by over 50% between 2006 and 2011 [73].
Furthermore, increasing the thickness of the REBCO film in the

![](images/tmpc7ciscuc.pdf-17-0.png)

| Layer | #1 | #7 | #15 |
|-------|----|----|-----|
| $B_{tot}^{max}$ (T) | 23 | 13.5 | 0.8 |
| $B_{r,r}^{max}$ (T) | 1.2 | 1.4 | 4.2 |
| $B_{\phi,r}^{max}$ (T) | 23 | 13.5 | 4.3 |
| $\lambda_c$ (A/mm²) | 1025 | 1280 | 815 |
| $J_{op}$ (A/mm²) | 512 | 640 | 407 |
| $I_{op}$ (kA) | 70 | 70 | 70 |
| $N^{turns}$ | 114 | 91 | 144 |

Table 3. *The maximum toroidal magnetic field ($B_{tot}^{max}$), radial magnetic field ($B_{r,r}^{max}$), total magnetic field ($B^{max}$), and critical current density ($\lambda_c$) in layers #1, #7 and #15. The critical current density was calculated for REBCO tapes at 20 K, oriented parallel to the toroidal magnetic field and perpendicular to the radial magnetic field. The operating current density ($J_{op}$) is calculated to be 50% of the maximum critical current in the layer. The operating current ($I_{op}$) is necessarily the same for all layers, but the number of 12 mm wide REBCO tapes, $N^{turns}$, is not.*

tape will increase (although not proportionally) the critical current. For example, increasing the REBCO thickness from 1 μm to 4 μm increases the critical current by approximately 200% [74].

Each leg of the TF coils will require a total of 120 CIC cables and the total number of superconducting tape turns is 106 (upscaling to 120 cables/leg for the full CS coil). The total required length of 12 mm wide REBCO tape for the entire TF coil system is about 57.30 km. However, the length of the individual CIC cable is 6.7 m for the bottom leg and 7 m for the top leg. Compared with continuous coil winding such as in ITER (where the length of individual cables is 760 m [75]), ARC requires relatively small lengths of continuous REBCO tape. This allows for more economic quality control of the superconductor since a defect in a REBCO tape spool can be easily removed with minimal loss of material.

## 4.2.2. Electrical joints

There are a wide variety of electrical and mechanical considerations that go into selecting the type of joints in the superconducting tapes. A thorough of these design choices is beyond the scope of our study. Therefore we choose a rather simple joint topology and simply investigate an estimate of the electrical consumption that arises from the finite resistance of each joint. The electrical joints between the two legs of the TF coils were chosen to be "comb-style". A schematic of the joint is shown in Fig. 21. Unlike other types of joints, this design is robust to errors in the connection of the tapes since the movement of the tapes does not significantly change the joint resistance. The joint requires pressure normal to the conductors, provided by a mechanical loading structure and the out of plane Lorentz force generated by the PF coils.

Each TF coil requires 120 comb comb joints in series. During steady state operation, the expected failure mode is partial damage, specifically degradation of a small number of tape-to-tape joints in a single comb joint. The comb joints are robust with regards to this scenario, as shown in Fig. 22, because each comb joint is composed of several tape-to-tape joints in parallel. This means damage to a tape will just cause the current to redistribute across the other tapes, bypassing the defect. This will allow the joint and coil to continue operation even with the failure of a tape-to-tape joint.

Each set of comb joints is insulated with Kapton and S2 glass. The insulation of the terminals overlap with each other in each joint, to increase the interface length. The insulation must protect the joint against Paschen and tracking discharges in the event of a magnet quench. Design concepts of joint insulation schemes are under development but not yet demonstrated.

Preliminary experimental measurements of REBCO comb joint resistance have been performed at 77 K without a background magnetic field [61]. They yield an average contact resistance of 30 μΩ/mm². For an average joint of 105 × 12 mm wide tapes per 70 kA cable, each tape pair will have an overlap length of 50 mm, corresponding to a tape-to-tape contact area of 600 mm². This configuration would require 35 comb teeth per joint, each tooth 150 mm long.

This would thus yield a tape-to-tape connection resistance of 50 nΩ, which corresponds to a power dissipation of 2.3 W in each comb joint. Coil grading does not have an effect on the total power loss in the comb joints, as the overlap length and the tape-to-tape contact area is adjusted according to the number of tapes in each 70 kA cable to keep the power dissipation constant. Thus, each TF coil will dissipate a total of 550 W, for a total of 9.9 kW of Joule power dissipation in all the electrical joints of the TF coil system at 20 K. Taking into consideration the practically achievable Carnot efficiency (calculated with the correlations recommended by Knezt [76]), it requires a cooling power of 0.57 MW to cool the resistive joints. However, this is small compared to the power requirements for the other coil systems and the rest of the power plant (∼500 MW [10]). This strongly contrasts with the copper-based FNSF designs, where the coil electricity consumption is about 500 MW [10].

## *4.2.3. Stress analysis in the coil structure*

A 2D finite element method (FEM) stress analysis was performed on the TF coils using COMSOL, a multiphysics code [77]. The geometry includes the 2D depiction of the winding and CS systems, corresponding to half the toroidal extent of a single TF coil. The out-of-plane forces are not simulated. In Fig. 23, the model of the section and boundaries are illustrated. Roller boundaries were applied on the side faces of the CS and some of the side faces of the TF, appropriate for the symmetry of the problem. The CS and TF coils are analyzed together, with sliding frictionless contact conditions applied at the boundary between the two coil structures. The tension ring was also a contact condition. The body load in the superconductors was set to be the Lorentz load from the total toroidal field. The winding pack was modeled as a homogeneous isotropic material with the average composition: 45.9% REBCO/Copper, with yield calculated as 49% copper, 55% Hastelloy, and 46.1% steel.

The results of the FEM simulation are shown in Fig. 24. The von Mises yield criterion [78] is satisfied at stress levels of 660 MPa in the backing cylinder (about 65% of the yield stress in Hastelloy C-276 [79]), 180-250 MPa at cryogenic temperatures ([69]) and 500 MPa in the TF coils structure. The strain in

![Figure 21: Schematic drawing of comb-style joint before mounting (top) and](images/tmpc7ciscuc.pdf-19-0.png)
after mounting (bottom). The REBCO tapes are glued or clamped to the steel
structure, oriented such that the Hastelloy layer is between the REBCO layer
and the steel structure. This way, the electrical resistance from the REBCO
layer to the surface of the tape is minimum. Clamping the two halves together
and applying pressure as shown completes the circuit. Cooling channels are
located in both structural pieces, at the base of each comb.

Figure 22: Schematic drawing of expected failure mode of comb-style joint.
The current in the coil section of the conductor can redistribute to avoid a defect
in one of the tape to tape connections.

the superconductor is less than 0.2%, half the limit of reversible
critical current degradation (a 5% degradation occurs with 0.4%
strain [78]). In this analysis the CS was not energized because
simulations showed that this yielded slightly lower stresses in
the central column. Therefore the scenario without a magnetic
field generated by the CS was used as a conservative approximation for the steady state stress. Note that during operation
the CS will be energized, thus the actual steady state stresses
are lower.
There may be other choices of stainless steel alloys that exhibit higher yield stress at cryogenic temperatures (e.g. AISI
301 with a yield stress of about 1500 MPa [79]), but this higher
strength comes at the expense of less ductility. The key observation is that structural stress is an important limit to consider
for implementing REBCO in high-field applications. While further optimization should be carried out through modeling and
experiments (e.g. on the choice of materials and geometry), it
is not unreasonable to expect 20–23 T peak field on coil, given
the known strength limit of various non-magnetic alloys.

Figure 23: Boundary conditions applied to the stress simulation, from two different angles. Surfaces shown in green have roller boundaries. Surfaces with
the same color are located in the same plane. The contact areas between the
three bodies (top leg, bottom leg, tension ring) are marked with arrows.

_4.3._ _PF, CS and AUX coil systems_

The PF, CS and AUX coils were designed based on ACCOME requirements, as shown in Fig. 25. Stress simulations have been performed for the CS as detailed in Section
4.2.3. However, no analysis was performed for the PF and AUX
coils because they carry relatively little current and are not constrained by stress limits due to the availability of physical space
for structure.
The Central Solenoid is part of the bucking cylinder, and occupies the space _R_ = 0.5–0.7 m, _Z_ = -3–3 m, as shown in Fig.
25. It is layer-wound with REBCO CICC cables, similar to
the TF coils conductors. It does not have vertical segmentation
since this would weaken its mechanical strength. The solenoid
operates from 63 MA/turn to -63 MA/turn. This configuration
generates a peak field on the coil of 12.9 T, similar to the ITER
solenoid [17]. During reactor start-up, a flux swing of 32 Wb
is available if the current in the solenoid is ramped across its

![](images/tmpc7ciscuc.pdf-19-1.png)

![](images/tmpc7ciscuc.pdf-19-2.png)

![Figure 24: Results of stress simulations in the TF coils. The maximum stress](images/tmpc7ciscuc.pdf-20-0.png)
in the stainless steel 316LN structure is 660 MPa, which gives safety margin of
approximately 65%.

Figure 25: CS, PF, AUX coil requirements from ACCOME, where the CS is in
blue, the PF coils are green, and the AUX coils are red. The location of the coils
is to scale, but the sizes of the coils are not (except for the CS). The direction
of positive current is defined to be the direction of the plasma current.

full operating range. The maximum stress in the CS structure
is 660 MPa, due to the compressive force from the TF coils.
However, the CS differs in that it experiences transient stresses.
The mission of ARC requires non-inductive scenarios and thus
the number of cycles is expected to be limited compared to inductive designs like ITER. This eases fatigue concerns, plus the
superconductor already has a large margin in critical current because the REBCO tapes in the CS are wound with the vertical
magnetic field of the solenoid lying in the plane of the REBCO
tapes.
The REBCO superconducting CS and PF coils provide the
principal poloidal field required for plasma shaping. The use
of superconducting coils minimizes recirculating power in support of the Pilot plant mission of ARC. The PF coils used for
pulling the X-points are situated outside the vacuum vessel, but
inside the TF volume at _R_ ∼ 2 m, _Z_ = ±3m. These PF coils do
not need joints because the TF demountability allows for their
modular insertion and extraction. The PF pull coils are shielded
by the FLiBe blanket and can be relatively small because they
are inside the TF volume. Outboard plasma shaping and equilibrium fields are supplied by PF coils placed outside the TF at
_R_ ∼ 6m.
The copper AUX coils allow for fast control of the plasma,
on the resistive time of the vacuum vessel, helping to avoid disruptions. They are effectively unshielded from neutron damage, so they are single-turn to improve radiation survivability. Additionally, they are part of the replaceable vacuum vessel, so they have a short in-vessel lifetime before they are
removed/replaced. The degradation in electrical conductivity
from the radiation damage is negligible, as at 800–900 K the
radiation damage in copper is largely annealed out. These coils
require standoffs from the vacuum vessel, which are assumed
to be thin stainless steel (with much higher resistance to ground
than the loop resistance in the copper coils). The resistivity of
the coils is approximately 5.3 × 10 [−][8] Ω-m at 800 K [80]. Given
a 5 cm circular coil cross section, each lower AUX coil requires
approximately 1 MW of electrical power, while the upper AUX
coils require about 9 kW. At this size, the AUX coils have very
little effect on the neutronics, as discussed in Section 5.

_4.4._ _Magnet cooling_

The magnet system could be cooled by liquid hydrogen,
neon, or gaseous helium. For this study we assume liquid hydrogen, which is relatively inexpensive and abundant, pressurized to 5–10 bar to increase the liquid temperature range. Independent cooling loops will refrigerate each TF coil leg and joint.
The coil cooling channels are located in the copper stabilizer,
while the joint cooling channels are located in the comb-style
steel structure (as shown in Fig. 21).
Radiant and conductive heat from the 900 K FLiBe tank (see
Section 5.4) is removed in several stages before it can reach
the superconducting coils. The thermal shielding, composed of
aluminum silicate surrounding the low-pressure blanket tank,
is cooled with water at room temperature. The neutron shield
surrounds this and is also cooled with liquid water. A set of
three vacuum gaps separate the TF coils and the neutron shield
(see Fig. 2). The thermal shield of the first gap (closest to the

![](images/tmpc7ciscuc.pdf-20-1.png)

| System | Coolant | $P_{in}$ | $P_p$ |
|--------|---------|----------|-------|
| Nuclear heating | LH₂ | 14 kW | 0.8 MW |
| TF coil joints | LH₂ | 10 kW | 0.6 MW |
| TF coil joints load | — | — | 10 kW |
| Thermal shielding | Water | 12 kW | ~ 0 |
| Vacuum shielding | LN₂ | 160 kW | 15 kW |
| Vacuum shielding | LH₂ | 100 W | 35 kW |
| AUX coils | FLiBe | 2 MW | ~ 0 |
| AUX coils load | — | — | 2 MW |
| **Total Power** | | **2.1 MW** | **5.1 MW** |

Table 4: Electrical power, $P_{in}$, required for cool current supply and the removal of waste heat, $P_p$, in the magnet systems.

neutron shield) is cooled with liquid nitrogen and the thermal shield of the outer gap is cooled with liquid hydrogen.

The water cooling loop removes several MW of heat to maintain components at room temperature, although the pumping power required to do this is negligible (see section 5.4.5). In the nitrogen loop, 160 kW of heat must be removed, requiring 15 MW of electricity. The hydrogen loop removes 700 W of heat that is radiated through the first vacuum gap, 10 kW from resistive heating in the TF coil joints and 14 kW of distributed nuclear heating throughout the volume of the TF magnets (see section 5.4). The total electrical power required to remove heat in the hydrogen loop is approximately 1.4 MW. It is noted that these levels of electrical consumption are relatively small (see Table 4) compared with the 70 MW of power required for the LHCD system (see Table 2) and thus has a small impact on $Q_e$. The practically achievable efficiencies in the cryocooler systems have been calculated with the correlations recommended by Kittel [76].

The coil system must also cycle between room temperature and 20 K for maintenance. Additional refrigeration channels and electrical heaters in the magnets structure will be used for the thermal cycling. When warming up, the electrical heaters will be used and gaseous helium at 300 K will be pumped into the refrigeration channels. Once the structure reaches approximately 100 K, gaseous neon at 100 K will flow into the vacuum chamber, to accelerate the heating process and to prevent humidity from entering the magnet once at 100 K [?]. When cooling down, cold gaseous helium will be pumped into the refrigeration channels until the magnet temperature reaches 20 K, at which point the supercritical hydrogen loop will start flowing. Liquid refrigerants are avoided in the 300 K − 20 K cycle to prevent evaporation from causing bursts in the cooling channels.

## 4.5 Alternative Designs

In addition to the D-shaped coils presented above, a "picture-frame" magnet design (see Fig. 20) was also considered. The picture-frame design is based on the TF coil of Alcator C-Mod, modified to use REBCO instead of copper [19]. We present the picture-frame design to illustrate the wide variety of coil choices possible when utilizing the idea of a compact, modular,

[Figure 20: The "picture frame" TF coil arrangement represents an alternative possible magnet configuration. The joints on all four corners of the magnets are demountable, allowing for even easier reactor maintenance than the D-shape design. However, this configuration is mechanically weaker than the D-shaped coils, thus limiting the toroidal field and making the "picture frame" design more suitable for an FNSF.]

demountable design. While the D-shaped coils are mechanically stronger, allowing for a higher on-axis field, the window-pane coils would be more suitable for a flexible, FNSF design. Unlike the D-shape coils, which only are demountable at two points, the picture-frame coils have sliding joints at every corner. These joints allow easier access to the blanket tank and vacuum vessel in addition to offering further mechanical stability in the event of a large disruption. However, the additional joints in this design increase the total heat generated by resistive dissipation and the electricity required to remove it.

## 5. Fusion power core

Traditional tritium breeding and neutron absorbing blankets for fusion reactor designs involve complex components containing significant solid, structural material. Since the blanket is generally contained within the TF coils, these structures must also be separable into modular sections so they can be installed through access ports between the TF coils. This results in challenging engineering constraints, difficult remote handling, and a low tritium breeding ratio (TBR) because the structural part of the blanket does not usually contribute to breeding. ARC utilizes a fully liquid blanket, where the TF molten salt coolant FLiBe surrounded by demountable superconducting TF coils to facilitate disassembly [81]. To maximize the tritium breeding volume, the vacuum vessel is completely immersed in the continuously recycled FLiBe blanket, with the exception of minimal support columns extending the vacuum vessel in the FLiBe. For modeling simplicity, the support columns are straight, but in a final engineering design, the support columns will be curved to minimize neutron streaming through them.

$F_2LiBe$ is a eutectic mixture of lithium fluoride and beryllium fluoride and has been used in fission reactors as a high temperature, high thermal efficiency moderator/coolant. Liquid

## Temperature-Dependent Properties

| Property | FLiBe | Water |
|---|---|---|
| Melting point (K) | 732 | 273 |
| Boiling point (K) | 1700 | 373 |
| Density (kg/m³) | 1940 | 1000 |
| Specific heat (kJ/kg·K) | 2.4 | 4.2 |
| Thermal conductivity (W/m·K) | 1 | 0.58 |
| Viscosity (mPa·s) | 4 | 1 |

Table 5: Comparison of the properties of liquid FLiBe and water. Note that temperature-dependent properties are given for liquid water at 293 K and liquid FLiBe at 950 K.

FLiBe has been considered in fission and fusion nuclear technology applications due to its favorable characteristics: a wide operating temperature range in the liquid phase, high effectiveness, and similar thermal-hydraulic characteristics to water (see Table 5) [82, 83]. For magnetic fusion, it also has the desirable feature of low electrical conductivity, which will help to minimize any MHD effects caused by the large background magnetic field. The beryllium in FLiBe allows the blanket to multiply and moderate high-energy neutrons via the $^7\text{Be}(n,2n)^6\text{He}$ reaction. Through the exothermic $^6\text{Li}(n,t)^4\text{He}$ and endothermic $^7\text{Li}(n,t+n)^4\text{He}$ reactions, the lithium breeds tritium, multiplies neutrons, and can generate substantial additional heating power. While modeling the intermixing with FLiBe in traditional blanket designs is difficult, we use MCNP neutronics analysis to show that the immersion blanket design, coupled with a non-structural beryllium-containing blanket, meets the TBR target. This TBR relies on using FLiBe with the lithium enriched to be 90% $^6$Li by isotopic abundance. We also show that, when coupled with a TiH₂ shield, FLiBe is able to protect the TF coils from neutron irradiation, despite the extreme space constraints of the compact ARC design.

Due to its favorable thermodynamic characteristics, FLiBe can be used as an effective coolant for the vacuum vessel and divertor, allowing for a simplified single-phase, low-pressure, single-fluid cooling scheme. The immersion blanket permits the entire vacuum vessel and the immersed divertor to become an interchangeable component, allowing for modular replacement. This mitigates the activation issues common to solid blanket coils. In addition, having the vacuum vessel as a single component allows for full off-site testing and quality assurance of all exposed components before installation into a machine. Using an all-liquid blanket eliminates the problem of radiation damage in the blanket and can reduce the amount of solid radioactive waste by a factor of ~ 20 (because ARC only has ~ 5 cm of vacuum vessel rather than a ~ 1 m thick solid blanket).

### 5.1. Open-ended divertor and vacuum vessel design

The design of commercial-scale fusion reactors requires significant knowledge of plasma material interactions. Presents the response of Plasma Facing Components (PFCs) to the extreme heat and particle fluxes of a reactor environment [84]. While proposed facilities such as IFMIF [85] and VULCAN [5] could inform this research, ARC would allow several vacuum vessel and divertor designs to be tested in actual reactor conditions.

Demountable coils allow for relatively simple removal and replacement of the vacuum vessel as a single "plug-and-play" component. This allows the ARC reactor to serve as a test bed for several PFC and divertor design configurations. With this in mind, the specific vacuum vessel and divertor designs have been left open-ended. For the purposes of neutronics analysis of the ARC design, the divertor has been modeled as an 8 cm thick layer of tungsten covering 17% of the lower vacuum vessel surface area. An actual divertor will almost certainly be thinner, but, due to the open-ended nature of the design, an overly-thick layer was modeled to give a conservative estimate of tritium breeding. The first wall has been modeled as 1 cm of tungsten on top of a thin structural lining (718 alloy). Both of these choices have been made based on current experimental designs. However, as mentioned above, ARC may possible experimental configurations for the ARC design.

### 5.2. TF coil neutron shielding

Superconducting magnets have been shown to be sensitive to high-energy neutron radiation [86]. In order to assess the radiation survivability of the REBCO tape, a model axisymmetric neutronics study was carried out using the Monte Carlo neutron transport code MCNP [87] (see Fig. 27). The most recent irradiation experiments have shown that the critical current of $\text{Nb}_3\text{Sn}$ begins to degrade at a total neutron fluence (considering only "high-energy" neutrons with energy $> 0.1$ MeV) of $3 \times 10^{18}$ neutrons/cm² [88]. This measured degradation point is a lower bound to the neutron fluence on superconductor survivability, providing a definite limit for design. The radiation resistance of REBCO is expected to be at least as good, if not better than $\text{Nb}_3\text{Sn}$ [86], and ARC can continue to operate with degraded critical current. This is especially important, as the its of the tapes are set by magnet stress limits, rather than the critical current of REBCO (see Section 4).

Given the compact size of ARC, FLiBe alone is insufficient as a neutron shield for the REBCO superconducting coils. Motivated by this, the neutronics analysis includes a neutron shield composed of TiH₂ around the blanket task (the component that holds the high-temperature molten FLiBe), with additional stainless steel in the inboard TF leg. TiH₂ has a very high hydrogen density, appropriate for neutron moderation, and a high cross section for the neutron absorption, making it an ideal shielding material [88].

We find that, after adding the TiH₂ shield, it takes 9 Full-Power Years (FPY) of reactor operation to reach a fluence of $3 \times 10^{18}$ neutrons/cm² in any part of the magnet. While this lifetime is likely insufficient for a dedicated, commercial-scale power plant, 9 FPY provides a lower bound due to insufficient data on tape irradiation. Furthermore, the lifetime could be extended significantly by reducing the reactor volume ratio, or by adding increasing the total amount of room for shielding (see Fig. 28).

[Figure 27: Cross section of the axisymmetric geometry used to model neutron transport in ARC using MCNP. Yellow indicates the plasma region, orange indicates the TF coil cases, light blue indicates FLiBe, and brown indicates the superconducting coil structure. Gray indicates either Inconel 718 or tungsten for the neutron vessel, connection port, and shield cap. The "squaring" of some corners in this simplified model has a negligible effect on the neutronics analysis.]

[Figure 28: The effect of increasing the reactor major radius (using all of the extra length for TBR shielding) on the yearly neutron fluence to the TF coils. Note that a small increase in the major radius results in a dramatic reduction of the yearly TF neutron fluence. While ARC was designed to be as small as possible, a full commercial reactor would likely have a slightly larger major radius to extend the plant lifetime.]

## 5.3. Tritium breeding

The same MCNP model described above was used to assess the TBR. In order to account for uncertainties in cross section libraries as well as the fact that the model is 2-D rather than 3-D, ARC was designed with the goal of obtaining a TBR ≥ 1.1 [89]. In addition, it is critical for the first fusion devices that consume substantial tritium to have good margin for TBR, so they do not jeopardize the world tritium inventory. To maximize TBR, enriched FLiBe with a 90% isotopic abundance of ⁶Li was chosen to enhance the tritium breeding cross section for lower-energy neutrons. Early designs with a single-walled vacuum vessel proved inadequate to provide both a TBR ≥ 1.1 and the needed mechanical strength (see Section 5.5.1). Therefore, a double-walled vacuum vessel design was developed, featuring a FLiBe channel and a non-structural beryllium neutron multiplier sandwiched between two layers of structural material (see Figs. 29 and 31).

TBR is extremely sensitive to the amount and type of material between the neutron source and the breeding blanket. Use of a double-walled, ribbed vacuum vessel addresses this by allowing the FLiBe channel to be very close to the core of the reactor while also maintaining the structural integrity of the vacuum vessel. Even with a FLiBe cooling channel close to the fusion plasma, the choice of first wall material and thickness plays a large role in determining TBR. As can be seen in Fig. 30, beryllium and tungsten first walls increase TBR, while Carbon Fiber Composite (CFC) and Inconel 718 first walls decrease the TBR. It is surprising that small thicknesses of tungsten increase TBR when using ⁶Li [90], but this is due to the high-energy neutron multiplication cross section of tungsten. The ARC design uses a 1 cm tungsten first wall to achieve a TBR of 1.1, but (as shown in Fig. 30) many other configurations are possible if the *TBR* ≥ 1.1 limit is relaxed.

| Reactor Volume | Total Heating (MW) |
|---|---|
| Inner VV | 26 |
| Coolant Channel | 33 |
| Neutron Multiplier | 81 |
| Outer VV | 18 |
| Neutron Shield | 2.8 |
| TF Coil | 0.014 |

Table 6: Nuclear (neutron and photon) heating of relevant ARC volumes from MCNP.

## 5.4. Steady state thermal analysis

Thermal analysis was performed self-consistently from the plasma-facing first wall to the superconducting magnets.

### 5.4.1. Nuclear heating

In order to perform a complete thermal analysis, nuclear heating was evaluated in MCNP for key volumes of the reactor (see Table 6). It is important to note that both neutron and photon heating needed to be taken into account in order to accurately capture the physics of the nuclear reactions induced within the reactor materials.

### 5.4.2. Bulk blanket thermal analysis

The input temperature of FLiBe in the bulk blanket was set at 800 K to give some margin from its freezing point of 732 K. The temperature rise across the blanket was estimated using simple energy conservation. With the specific heat of FLiBe, an input flow velocity of 0.2 m/s, and 18 inlets each with an area of

## Double-Walled Vacuum Vessel Design with FLiBe Coolant Channel

[Figure 29: Double-walled vacuum vessel design with FLiBe coolant channel]

[Figure 30: Effect of first wall PFC material and thickness (excluding the divertor) on TBR]

0.3 m², the exit temperature is found to be 900 K. This calculation includes energy generated from breeding reactions within the blanket, which is significant. Turbulent 2-D COMSOL simulations were performed to verify this output temperature and estimate the peak blanket temperature to be less than 1000 K.

![](images/page_024_eq_0.png)
### 5.4.3 Vacuum vessel and channel thermal analysis

In addition to providing favorable TBR and structural characteristics, the double-walled vacuum vessel design allows for the FLiBe in the channel to be used as active liquid cooling for the first wall. Single phase fluid cooling, with low conductivity/MHD issues, is a highly attractive cooling scheme for magnetic fusion. The vacuum vessel has 1 cm thick tungsten tiles facing the plasma, mounted on a 1 cm inner vacuum vessel. On the other side of a 2 cm channel is a non-structural 1 cm beryllium neutron multiplier attached to the 3 cm thick outer vacuum vessel. As can be seen in Fig. 29, centrifugal pumps (with an externally located motor and drive shaft) circulate cool FLiBe at 800 K through the channels in the vacuum vessel to remove heat from the first wall. These channels flow in both poloidal directions for half the circumference and exhaust to the bulk blanket. A separate set of channels and pumps exist for divertor cooling.

![](images/page_024_eq_1.png)
In order to calculate the vacuum vessel cooling requirements, a 1-D analytic estimate was performed for a slab model of the system using

$$T_{\text{channel,outlet}} \simeq T_{\text{channel,inlet}} + \frac{\langle I \rangle_{m}}{\dot{m} C_p} \tag{30}$$

![](images/page_024_eq_2.png)
and

![](images/page_024_eq_3.png)
$$T_{\text{VV,inner}} \simeq T_{\text{channel,outlet}} + \Delta T_{\text{inner,face}} + \frac{\Delta T}{\delta_{VV}} \tag{31}$$

Here $P_m$ is the total power deposited in the entire vacuum vessel model (the heat flux from the plasma plus the volumetric neutron power from Table 6), $\dot{m}$ is the mass flow rate, $C_p$ is the specific heat, $\Delta t$ is the inner vacuum vessel thickness, and $k_{VV}$ is the thermal conductivity. The temperature jump across the channel-wall interface, $\Delta T_{\text{inner,face}}$, is estimated using the Dittus-Boelter correlation

$$Nu = 0.023 Re^{0.8} Pr^{0.4}, \tag{32}$$

and the relation

$$\Delta T_{\text{inner,face}} = \frac{\langle 2\Delta t \rangle q}{k_{\text{channel}} Nu} \tag{33}$$

where $Re$ and $Pr$ are the channel Reynolds and Prandtl numbers. Lastly $q$ is the heat flux through the inner vacuum vessel, estimated as $q = q_{\text{plasma}} + P_{VV,\text{inner}} / S_{VV}$, where $q_{\text{plasma}}$ is the heat flux on the inner vacuum vessel surface from the plasma, $P_{VV,\text{inner}}$ is the total neutron power deposited in the inner vacuum vessel, and $S_{VV}$ is the vacuum vessel plasma-facing surface area. It was assumed that the inner vacuum vessel surface received a uniform radiative heat flux of 30% of the plasma heating power (the sum of alpha, ICRF, and LHCD power), which is equal to 0.2 MW/m². This yields an average output FLiBe temperature of 823 K and a maximum Inconel temperature of 1030 K.

These analytic estimates agree with a higher fidelity 2-D COMSOL calculation (see Fig. 31), with volumetric heat in each layer taken from Table 6. Note the apparent discontinuities across the fluid/solid interface are due to the convective boundary layer condition in COMSOL (33). The FLiBe fluid layer in contact with the main FLiBe blanket was fixed at the maximum blanket temperature of ~1000 K to be conservative, although the average blanket temperature is expected to be ~800-900 K. Importantly the maximum temperature on the vacuum vessel, which approaches the tungsten facing surface, is insensitive to the boundary condition on the blanket facing surface.

The fluid flow velocity in the vacuum vessel coolant channel was limited to be 2 m/s because of concerns about flow-assisted corrosion, although nickel-based alloys have excellent corrosion resistance in molten fluoride salts [91] at these temperatures. At this fluid velocity, the COMSOL simulation (see

## 5.4.4. Divertor thermal analysis

Explicit thermal modeling of the heat loading of a FLiBe-cooled divertor is beyond the scope of this study. However, we note that FLiBe would offer significant advantages for heat removal compared with the typical design choice of helium: a much higher heat capacity, low flow rates, and low pressures. Instead, we will estimate the scale of the divertor heat loading in order to show that the compact size and high magnetic field of ARC do not dramatically intensify the problem.

The key metric that determines the viability of cooling is the divertor heat flux, given by

$$P_{div} = \frac{P_{heat}}{2\pi R_{div} \lambda_q},\tag{34}$$

where $P_{heat} \approx P_\alpha + P_{CD}$. This formula does not attempt to give an accurate prediction for the divertor heat loading. Rather it ignores detailed, albeit important, effects (such as the radiative power fraction) and tries to reveal how ARC compares to other more thoroughly-analyzed machines, when holding these detailed effects constant. Unfortunately, the scrape-off layer width, $\lambda_q$, cannot currently be predicted with any certainty, so we instead investigate where the ARC design falls between two heat flux benchmarks of merit. The upper extreme uses the Eich/Goldston scaling which estimates $\lambda_{q,EG} \sim 1/B_p$ [92]. The lower extreme assumes a pressure limited Scrape-off Layer (SOL) and leads to the estimate $\lambda_{q,p} \sim 2\pi q_s (1 + \kappa^2)/2$ [92]. Table 7 shows where ARC falls in comparison to a range of current and proposed tokamaks. Based on this analysis, we conclude that the difficulty of the divertor problem in ARC resides

between ITER and reactor designs, which seems appropriate for a Pilot power plant.

![](images/page_025_eq_0.png)
As previously noted, a rather large range in steady state fusion power (up to 525 MW) can be used to test divertor solutions. It is important to note that power exhaust issues are improved by operating at high safety factor (which decreases $B_p$ and widens $\lambda_{q,EG}$) and by having high $Q_p$ (which reduces the required $P_{heat}$ at fixed $P_f$). Both these design features result from operating at high toroidal fields.

## 5.4.5. Neutron shield/thermal shielding and cooling

In order to thermally isolate the 900 K blanket tank from the neutron shielding and magnet systems, the blanket tank is surrounded by 1 cm of aluminum silicate wool. The heat flux through the blanket thermal shield can be analytically estimated as

![](images/page_025_eq_1.png)
$$q = \frac{\kappa_{VS} \Delta T_{VS}}{\Delta r_{VS}},\tag{35}$$

where $\kappa_{VS}$ is the thermal conductivity of the aluminum silicate thermal shield, $\Delta T_{VS}$ is the temperature difference across the shield, and $\Delta r_{VS}$ is the shield thickness. Using the thermal conductivity $\kappa_{VS} = 0.1 \text{ W m}^{-1} \text{ K}^{-1}$ [96] and keeping the outside of the blanket thermal shield at 293 K (room temperature), the heat flux through the blanket thermal shield is calculated to be 6.1 W/m². However, this is negligible compared to the 2.8 MW of neutron power (see Table 6) deposited in the neutron shield. This heat is removed by a 1 cm thick, toroidally continuous, coolant channel of vertically flowing water. We can use 0-D power balance to find that

$$P_n = \rho_c v_c c_p 2\pi R \Delta r_c \Delta T_c,\tag{36}$$

![](images/page_025_eq_2.png)
where $P_n = 2.8 \text{ MW}$ is volumetric neutron heating, $\rho_c = 1000 \text{ kg/m}^3$ is the coolant density, $v_c = 1 \text{ m/s}$ is the coolant flow velocity, $R = 3.5 \text{ m}$ is the major radius position, $\Delta r_c = 1$ cm is the coolant channel thickness, $C_p = 4200 \text{ J/kg K}$ is the specific heat, and $\Delta T_c = 7 \text{ K}$ is the coolant temperature difference. Using the Moody friction factor for engineering medium roughness metal pipes, the pressure drop through our cooling channel is calculated to be $\Delta P = 1.1 \times 10^2$ Pa. Assuming a conservative pump efficiency of 50%, the pumping power required to cool the neutron shield will be ~ 2.5 kW, which is negligible compared to the other reactor power requirements. Thus, the neutron shield can be cooled using water in the remaining 5 cm of inboard radial build allocated for thermal insulation of the neutron shield (see Fig. 2).

## 5.5. Disruption analysis

Primarily, disruptions pose two distinct threats to a device. First, during the disruption plasma current can transfer to the wall over a short timescale (~1 ms), which can induce electromagnetic stresses on components. Second, the plasma can move and directly contact the wall. This transfers the energy contained in the plasma to the FWCs while they melt and erode the surface. Here we will show that the small size and high fields of ARC do not dramatically affect disruption survivability compared to other devices.

[Figure 31: COMSOL model predicted temperature distribution across the vacuum vessel (with the plasma-facing surface on right) at both the channel inlet and outlet]

| | ARC | ARIES-AT | JET | C-Mod | ITER |
|---|---|---|---|---|---|
| Major radius, $R_0$ (m) | 3.3 | 5.2 | 2.92 | 0.67 | 6.2 |
| Aspect ratio, $1/\epsilon$ | 3 | 4 | 3.07 | 3.05 | 3.1 |
| Minor radius, $a$ (m) | 1.13 | 1.3 | 0.95 | 0.22 | 2.0 |
| Elongation, $\kappa$ | 1.84 | 2.2 | 1.81 | 1.68 | 1.75 |
| On-axis magnetic field, $B_0$ (T) | 9.2 | 5.8 | 3.6 | 5.4 | 5.3 |
| Plasma current, $I_p$ (MA) | 7.8 | 12.5 | 4 | 1.5 | 15 |
| $P_{\text{fus}}$ (MW) | 143 | 589 | 28.9 | 8 | 150 |
| $1/B_0$ (T$^{-1}$) | 1.07 | 0.89 | 1.74 | 1.01 | 0.95 |
| $P_{\text{fus}}B_0/R_0$ (MW$\cdot$T/m) | 41.0 | 84.2 | 5.69 | 11.8 | 25.5 |
| $P_{\text{fus}}/S_p$ (MW/m$^2$) | 0.67 | 0.85 | 0.18 | 1.00 | 0.21 |

Table 7: Inter-machine comparisons [17, 2, 94, 95] of diverse heat loading metrics, where $S_p$ is the surface area of the plasma.

| | ITER | ARC | ARIES-AT | JET | C-Mod |
|---|---|---|---|---|---|
| $\Lambda_0/117$ | 1 | 0.91 | 0.84 | 0.24 | 0.56 |
| $\Lambda_0^N/56$ | 1 | 0.89 | 1.72 | 0.26 | 0.53 |
| $\Lambda_0^D/1.1$ | 1 | 3.14 | 0.13 | 0.14 | 0.18 |

![](images/page_026_eq_0.png)
Table 8: Inter-machine comparisons [17, 2, 94, 95] of the severity of the disruption forces and disruption thermal loading (normalized to the value for ITER).

## 5.5.1 Disruption mechanical analysis

![](images/page_026_eq_1.png)
The most significant steady state force acting on the vacuum vessel is buoyancy, due to the significant volume of FLiBe it displaces. The vacuum vessel and posts must be designed to support themselves. However this requirement is insignificant compared to the transient forces during a plasma disruption. These stresses were modeled in COMSOL and treated analytically using a simplified model. Stresses arise from the $J \times B$ forces between the background magnetic fields and plasma current that has been transferred to the vessel. Disruptions manifesting themselves as kink modes are particularly troublesome because they can deposit significant poloidal current, which interacts with the dominant toroidal background field. Halo current can only interact with the background vertical field and generally produces forces an order of magnitude below those from the poloidal halo current.

We assumed a worst case unmitigated, asymmetric disruption with a toroidal mode number of $n = 1$,  $f_{\text{halo}} = 40\%$ (the fraction of the plasma current directed poloidally as halo current), and a toroidal peaking factor of 2 (the ratio of the maximum halo current to the toroidal average). The most significant stresses occur on the inboard midplane at the toroidal location of peak current. Here the force density distribution becomes:

$$F_V = \frac{f_{\text{halo}} I_p B_0 d_{VV}}{\pi (R_0 - a)^2 d_{VV}}$$
(37)

where $d_{VV}$ is the vacuum vessel thickness. Modeling the vacuum vessel as a thin cylinder we find the stress to be:

$$\sigma_{VV} = \frac{p_{VV} D_{VV}}{2d_{VV}} = \frac{f_{\text{halo}} I_p B_0}{\pi (1 + \epsilon) d_{VV}}$$
(38)

where $p_{VV} = F_V d_{VV}$ is the effective pressure acting on the vacuum vessel and $D_{VV} = 2(R_0 - a)$ is the diameter of the cylinder. This demonstrates that the parameter

$$\Lambda_0 = \frac{(I_p/\text{MA}) B_0}{1 + \epsilon}$$
(39)

is representative of the severity of disruptions in a given machine. If two machines have the same value of $\Lambda_0$, then they both require similarly strong thin vacuum vessels to withstand a disruption with a given $f_{\text{halo}}$. Table 8 shows that, despite the small size and high fields of ARC, the difficulty of tolerating the forces of a disruption is comparable to what ITER faces. However, it should be noted that, even though ARC faces a similar problem to ITER, it has half the space (in major radius) available for a vacuum vessel that addresses it.

![](images/page_026_eq_2.png)
Calculating the exact magnitude of the stresses caused by a disruption is difficult because the halo current distribution varies with time and may not flow through the full thickness of the vacuum vessel. In the worst case the current will be confined only to the 3 cm outer layer of the shell. In the best case it will be distributed over the inner vacuum vessel and the 3 cm outer inconel shell.

We define the mechanical factor of safety to be the ratio of the yield stress of the material to the peak stress expected during the disruption. The yield stress of Inconel 718 at the maximum vacuum vessel temperature of 1030 K is roughly 940 MPa [97]. Both analytic theory and COMSOL give similar results, shown in Fig. 32. We see that, in the most pessimistic case, it seems unlikely that the vacuum vessel will survive. However, ideally a full, worst-case, unmitigated disruption should never occur and our assumptions have been conservative. Even if it does the connecting structure between the vessel and the permanent reactor components can be designed to fail gracefully and the

[Figure 32: COMSOL (crosses) and analytic (squares) estimates from Eq. (38) of the mechanical factor of safety as a function of the effective vacuum vessel thickness]

vessel can be replaced. This is a much better scenario than similar first wall damage happening to large solid blanket modules.

It is important to note that in the ARC design, the blanket tank, rather than the vacuum vessel, is the primary nuclear safety barrier. Thus, even in the worst-case scenario of a catastrophic vessel breach, both the activated vessel and the tritium-containing FLiBe inside of it would still be contained within the nuclear safety barrier of the blanket tank.

## 5.5.2. Disruption thermal analysis

As the plasma contacts the wall it deposits its energy into the plasma-facing components. Depending on how much energy is deposited and how fast it happens the first wall PFCs can melt. Melting of the first wall is undesirable because it deforms the PFCs, ruining their alignment to the B field. This leads to uneven distribution of heat during subsequent disruptions and further melting. We will study this effect following methods discussed in Ref. [95].

![](images/page_027_eq_0.png)
In the limit of an instantaneous heat pulse, the maximum temperature rise on the surface is given by

$$\Delta T_{max} = T_{init}(t) - T_0 = \frac{H_{max}}{\sqrt{\pi}}\tag{40}$$

![](images/page_027_eq_1.png)
where $H_t$ is the radiant energy given in units of energy per unit surface area.

There are two types of energy contained by the plasma and each are transferred to the vacuum vessel at different rates. The current quench of a disruption transfers the energy contained in the poloidal field, given by

![](images/page_027_eq_2.png)
$$W_{pol} = \frac{L}{2}I_p^2,\tag{41}$$

where $L = \mu_0 R_0 \left(\ln\frac{8R_0}{a} - 2 + \frac{l_i}{2}\right)$ is the plasma inductance ignoring shaping effects. The thermal quench of a disruption transfers the energy contained in the thermal energy of the plasma given by

$$W_{th} = \frac{3}{2}V\langle p \rangle_0 \tag{42}$$

![](images/page_027_eq_3.png)
The timescales for these two processes are the current quench time, $t_{CQ}$, and the thermal quench time, $t_{TQ}$, respectively. Since the maximum radiant exposure can be approximated as

$$H_{t,max} = \frac{W}{S_{VV}},\tag{43}$$

![](images/page_027_eq_4.png)
where $S_{VV}$ is the vacuum vessel surface area, the temperature rise from each phase is

$$\Delta T_{max,CQ} = \frac{I_p^2}{a\sqrt{\pi t_{CQ}}}\tag{44}$$

and

$$\Delta T_{max,TQ} = \frac{aBI_p\beta_p}{\sqrt{\pi t_{TQ}}}\tag{45}$$

![](images/page_027_eq_5.png)
The current quench timescale is given by the $L/R$ time of the plasma, meaning

$$t_{CQ} = \frac{L}{R} = a^2,\tag{46}$$

![](images/page_027_eq_6.png)
where $a^2$ is the plasma resistance. Therefore, we will define

$$A_q^{CQ} \equiv \frac{(I_p/MA)^2}{(a/m)^2}\tag{47}$$

to approximate the difficulty of handling the current quench heat loading. The thermal quench time is not precisely known, however Fig. 54 of Ref. [99] shows that, to best approximation, $t_{TQ} \propto a$, i.e. the thermal quench follows a convective timescale. Therefore, we will define

$$A_q^{TQ} \equiv \sqrt{a}(R_0/T)^2 \beta_p^2\tag{48}$$

to represent the difficulty of handling the current quench heat loading. We see in Table 8 that, because of the low current (high $q_{95}$) in ARC, the current quench should be relatively modest. However, because of the small size and high power density, the thermal quench will be more problematic. One sees that ARC is intermediate with respect to ITER and a large fusion reactor. Safe dissipation of thermal energy, especially during a disruption, remains a research challenge for all burning plasma tokamaks.

![](images/page_027_eq_7.png)
## 5.6. Material damage and activation

MCNP was used to compute material damage due to irradiation, keeping track of both DPA and $^4$He production in several components (see Table 9). Little research has been done regarding how Inconel 718 responds to the irradiation environment of a fusion power plant. However, studying the response of components to fusion neutron effects is part of the motivation for ARC.

For context, the irradiation lifetime of ferritic steel is estimated at 150-200 DPA [2]. Additionally, with a helium concentration of 500 appm, martensitic steel survives, but shows some increase in yield strength and some reduction in ductility
![](images/page_027_eq_8.png)

| Component | $^4$He (ppm) | DPA |
|-----------|-------------|-----|
| Inner vacuum vessel | 280 | 44 |
| Outer vacuum vessel | 140 | 26 |
| Blanket tank | 0.56 | 0.4 |
| Support column | 8.3 | 3.0 |

*Table 9. Component helium production and DPA in one FPY. The production of $^4$He was found to be negligible.*

[101, 102]. It is unknown if Inconel 718 would behave similarly in a fusion neutron spectrum, but one expects the vacuum vessel would survive for at least 6–12 months.

Initial tests suggest that rewelding steel might become problematic at around 1 He appm [17, 103], which implies that the blanket tank would need replaced after only one FPY. In order to eliminate this issue, the replaceable components will be bolted, rather than welded to the permanent structure. However, this isn't perfect, as it creates concerns about differential swelling and diffusive bonding (a critical area of active research for both fission and fusion materials). One possible solution would be to increase the blanket height to allow for additional FLiBe/shielding between the plasma and the bolted sections.

A primary advantage of the liquid immersion blanket design is that it significantly reduces the amount of solid material near the plasma. The vacuum vessel design for ARC will have only 85 metric tons (~ 11 m³) of solid material compared to over 2000 metric tons in ITER [104]. This drastically lowers the amount of material that could become activated.

## 3.7. *Material corrosion*

While a full flow-assisted corrosion analysis of the structural materials in contact with FLiBe is beyond the scope of this paper, basic corrosion rates were investigated to ensure that the design is reasonable. Recent experimental work as part of the FNSF design study [105] investigated the corrosion effects of FLiBe on Inconel 625, an alloy similar to ARC's Inconel 718, which was chosen for its high temperature strength. At a temperature of 873 K (similar to that of the ARC blanket), the static corrosion rate of Inconel 625 was found to be 1.1 μm/yr [106]. These results, combined with the extremely slow 0.2 m/s peak flow velocity of FLiBe in the ARC blanket give confidence that the Inconel 718 vacuum vessel and blanket tank will survive the corrosive effects of the FLiBe blanket, particularly in the "FNSF stage". As discussed in Section 7, further research into radiation-assisted corrosion of Inconel is required.

## 6. Economics

The main driver for minimizing the size of ARC is to reduce the cost of building the reactor. While a full costing of the ARC reactor is beyond the scope of this paper, a rough scaling based on volumes and materials prices has been performed. With a major radius of 3.3 m, ARC is similar in size to experiments that have already been built (JET and TFTR). The following

| Component | Cost |
|-----------|------|
| Beryllium [108] | $257/kg |
| Inconel 718 [109] | $56/kg |
| Tungsten [108] | $29/kg |
| Stainless steel 316LN [109] | $9.6/kg |
| Copper [108] | $8.3/kg |
| REBCO tape [110] | $198/m ~ $36/m |
| FLiBe [111] | $154/kg |
| TiH₂ [112] | $26.4/kg |

*Table 10. Materials costs in 2014 US dollars. Due to the large amount of REBCO required, the quote was given as a price range. Note the REBCO cost is in $/m, rather than $/kg.*

analysis aims to justify that ARC is feasible from a materials cost standpoint.

In order to assess the bulk materials costs of the ARC reactor, the reactor was broken down into three subsystems: the replaceable vacuum vessel, the blanket, and the magnet/structure. In order to estimate the costs of components requiring extensive machining, a volumetric cost scaling based on several design studies was used [107].

### 6.1. *Materials Costs*

Material prices were obtained either from estimates of commodity prices or quotes requested from manufacturers (see Table 10). Although the REBCO tape and FLiBe are not technically raw materials they are included in the bulk costing analysis.

### 6.2. *Fabricated Component Scaling*

In order to provide a better cost estimate than simple materials costs, a rough scaling based on total cost per weight was employed, following Ref. [107]. In this scaling, the total projected costs of four baseline plasma devices (FIRE, BPX, PCASTS, and ARIES-RS) were divided by the weight of the device from the cryostat inward. As seen in Ref. [107], these cost-per-mass are very similar, which gives confidence that the scaling is not machine specific. As a simple estimate the ARC study averaged the four cost/mass and adjusted for inflation. The adjusted scale was $1.06/tonne (mass in metric tonnes) in FY2014 US dollars. This scaling will be referred to as the "fabricated" component scaling. To calculate the total cost of a component using the fabricated component scaling, we multiply the total weight of the component by $1.06M/tonne. In the case of components that do not require machining (e.g. the FLiBe blanket), the fabricate cost will be the same as the material cost.

### 6.3. *Replaceable Vacuum Vessel*

The materials in the replaceable vacuum vessels were analyzed using the MCNP neutronics model to estimate the material volumes. The

| Component | Volume | Weight | Material | Material Cost | Fabricated Cost |
|-----------|--------|--------|----------|---------------|-----------------|
| First wall | 2.01 m³ | 3.72 tonnes | Tungsten | $110k | $4.03M |
| Inner VV wall | 2.03 m³ | 16.6 tonnes | Inconel 718 | $930k | $183M |
| Multiplier | 4.09 m³ | 3.82 tonnes | Beryllium | $990k | $4.1M |
| Outer VV wall | 6.27 m³ | 51.4 tonnes | Inconel 718 | $2.9M | $55M |
| VV ribbing | 0.83 m³ | 6.80 tonnes | Inconel 718 | $380k | $7.2M |
| VV posts | 0.51 m³ | 4.14 tonnes | Inconel 718 | $230k | $4.4M |
| **Replaceable VV Subtotal** | **157 m³** | **86.5 Tonnes** | **N/A** | **$5.5M** | **$92M** |
| Blanket tank | 11.8 m³ | 97.1 tonnes | Inconel 718 | $5.4M | $100M |
| TiH₂ shield | 101 m³ | 380 tonnes | TiH₂ | $10M | $10M |
| Channel FLiBe | 4.09 m³ | 8.07 tonnes | FLiBe | $1.2M | $1.2M |
| Blanket tank FLiBe | 241 m³ | 475 tonnes | FLiBe | $73M | $73M |
| Heat exchanger FLiBe | 241 m³ | 475 tonnes | FLiBe | $73M | $73M |
| **Blanket Subtotal** | **599 m³** | **1440 tonnes** | **N/A** | **$160M** | **$260M** |
| Magnet structure | 544 m³ | 4350 tonnes | SS316 LN | $42M | $4.6B |
| Magnet top ring | 120 m³ | 959 tonnes | SS316 LN | $9.2M | $9.2M |
| REBCO structure | 40 m³ | 358 tonnes | Copper | $3.03M | $380M |
| REBCO tape | 5730 km | ~0 tonnes | REBCO | $103M – $206M | $100M – $210M |
| **Magnet/Structure Subtotal** | **704 m³** | **5670 tonnes** | **N/A** | **$160M – $260M** | **$5.1B – $5.2B** |
| **Grand Total** | **1320 m³** | **7190 tonnes** | **N/A** | **$330M – $430M** | **$5.5B – $5.6B** |

Table 11: Cost/weight breakdown table for ARC reactor (excluding the balance of plant equipment).

material volumes were multiplied by the material densities and
assigned a total cost using Table 10. The Inconel “ribbing”
structure inside the vacuum vessel cooling channel was estimated to be 10% of the channel volume and the total vacuum
vessel post volume was approximated to be 10% of the value reported by MCNP (because the posts are discrete, not toroidally
continuous as in the 2-D model). The divertor cost was left out
of the analysis because the design was left as an open question. However, a rough estimate for a 2 cm tungsten divertor
covering 20% of the first wall area is on the order of $500 _k_ for
materials, implying a $17.5 _M_ fabricated cost. The replaceable
vacuum vessel cost breakdown and subtotal are shown in Table
11.

_6.4._ _Blanket_

The blanket costs were analyzed using the MCNP neutronics
model to estimate the material volumes. The material volumes
were multiplied by the material densities and assigned a total
cost using Table 10. In order to estimate the volume of FLiBe
required for the heat exchanger (in the balance of plant), a simple shell and tube model with cooling fins using helium as the
secondary fluid was used. With this estimate, the volume of
FLiBe in the heat exchanger was calculated to be between 160
m [3] and 600 m [3], depending on the details of the heat exchanger
design. It was assumed that the heat exchanger would be designed to minimize the amount of FLiBe required, so a volume
of 241 m [3] (the same volume as in the blanket tank) was chosen
as a rough estimate. Since the TiH2 is in powder form and the
FLiBe is liquid, the fabricated cost for components made from
these materials was set equal to the material cost. The blanket
cost breakdown and subtotal are shown in Table 11.

_6.5._ _Magnets_

The magnet structure costs were analyzed using the COMSOL magnet stress model to estimate the volume of steel required. In order to estimate the required length of tape, the
area of REBCO needed to produce the given magnetic field was
computed (taking into account the geometry of the coils). This
was divided by the area of a single tape to find the number of
tapes required and then multiplied by the perimeter of the superconducting coil (see Section 4). Material volumes/lengths
were assigned a total cost using Table 10. Note that because
the magnet tension ring (holding the top coil flanges together)
is a large but very simple component, the fabricated cost is expected to be similar to the material cost. The reactor base is
treated the same. It is important to note that the reactor base
is conservatively modeled as entirely steel for the cost evaluation, but the actual structure would likely be comprised of both
concrete and steel. The magnet/structure cost breakdown and
subtotal are shown in Table 11.

_6.6._ _Cost Feasibility_

Assuming the higher cost estimate for the REBCO tape, the
materials costs for ARC total $428 _M_ and the total fabricated
component cost estimates total $5.56 _B_ . While these are simple estimates, they provide several critical insights. The material costs of the “novel” materials/components in the ARC

reactor (REBCO tape, FLiBe, TiH2 shielding) are only a small
fraction of the total fabricated cost predicted by the fabricated
component scaling. While there is a price to generating higher
magnetic fields due to the extra structure in the magnets, this
premium is easily overcome by the overall ability to reduce the
volume of the plasma, shield, and coils. This can be seen by
noting that 9.2 T ARC has a fifth of the ∼ $24 _B_ price of the 5.3 T
ITER (calculated by applying the fabricated component scaling
to the ∼ 23,000 tonne ITER). Yet ARC matches ITER’s fusion
power and produces net electricity. The cost of ARC is approximately one-third the cost of the 8 T ARIES-RS (∼ $14 _B_ ), but
ARIES-RS has approximately four times the electrical output.
The smaller ARC is appropriate for an “entry-level” fusion Pilot plant, but there likely exists a better economic optimization
of magnetic field strength versus mass for a full power plant.
Finally, one notes that the “fabricated” cost for a commercial
version of ARC will be reduced through economies of scale if
multiple reactors are built.

**7.** **Identification of R&D requirements**

_7.1._ _Plasma physics and current drive_

First, the I-mode regime must be further studied, characterized, and demonstrated with non-inductive profiles. As with all
small reactor designs the core scenario exploits enhanced confinement from current profile and q control. Therefore, a fully
developed and consistent non-inductive scenario with the required physics parameters should be explored more completely.
Ideally, we would use a burning plasma experiment in order to
also test the self-determining effect of alpha-dominated heating
on the plasma profiles. One aspect of I-mode of particularly significant to the ARC design is the maximum power density normalized to density achievable before transition to H-mode [39].
The published range spans _Pheat_ / _S p_ / _n_ 20 = 0.2 to 0.5 MW/ _m_ [2]

over a range of magnetic fields (up to 6 T). The operating point
of ARC is characterized by _Pheat_ / _S p_ / _n_ 20 ∼ 0.55 at 9.2 T. In
addition, it is important to understand the mechanisms allowing I-mode to maintain a stationary pedestal without damaging
ELMs.
The engineering of the lower hybrid system also requires
significant research. Currently, reliable lower hybrid klystron
sources exist at 6 GHz, but the 8 GHz system incorporated in
ARC has yet to be demonstrated. Like all components, there is
limited data on the integrated response of possible waveguide
materials in the fusion neutron environment. A particular challenge for an RF launcher in a reactor is surviving the high temperatures and radiation damage, while maintaining high electrical conductivity to avoid resistive losses and heating. However,
the ARC LHCD design is no more problematic than ARIESAT design, which uses LHCD launched from the low-field side.
Still, since the waveguides will be hot, they will likely be made
more resilient because of annealing. Furthermore, we only require that they have a lifetime longer than that of the vacuum
vessel, which is only a couple of years in ARC.

_7.2._ _Magnets_

The most important outstanding magnet research pertaining
to ARC is the design and testing of REBCO superconducting
joints. While several designs have been tested in a small-scale
“bench top” setting [61], they must be proven to be robust at
reactor-level fields and stresses. The joint insulation must be
tested at the high quench voltages (about 2 kV) and has to protect the joint against Paschen and tracking discharges.
In addition, further research into the properties of REBCO at
liquid hydrogen temperatures (20 K) is required to assess the
feasibility of different temperature regimes of superconductor
operation. The performance of REBCO cables at 20 K in a
complex and varying (in both space and time) magnetic field
needs to be studied. Also, cabling methods must be developed
for the industrial production of coil conductors. Lastly, an effective quench detection/protection system must be designed and
demonstrated at 20 K.

_7.3._ _Fusion power core_

Crucial, both for ARC and any other superconducting reactor, is an accurate understanding of how superconducting tape
responds to fast neutron irradiation. The amount of material
needed to shield REBCO directly constrains the minimum possible major radius needed to achieve a given TF coil lifetime.
Current fluence experiments only establish a conservative irradiation limit, and REBCO has never been tested to failure in a
fusion relevant environment [86].
Additionally, some designs have been proposed for extracting tritium from FLiBe [113, 114]. However, due to the cost of
tritium handling, few experiments have been built to assess the
turn around time needed for extraction and subsequent refueling. This turn around time directly determines the necessary tritium inventory and the quantity that is needed to initially start a
reactor. More experiments are required to demonstrate that this
turn around time is sufficiently fast to meet regulatory limits on
the total on-site tritium inventory.
Another source of uncertainty is the effect of a strong background magnetic field on the flow, turbulence, and heat transfer characteristics of FLiBe. Initial computational investigation seems to show that these effects can be neglected in a wide
range of fusion relevant parameters [115], but a more detailed
investigation is required for an engineering design. Specifically, it is unknown if the magnetic field will alter flow assisted
corrosion, which could impact the vacuum vessel and divertor
coolant channels. In addition, it is unknown how much the resistivity of the FLiBe will be affected by exposure to high neutron and gamma fluxes from the core.
Finally, a better understanding of radiation-assisted corrosion
of Inconel in contact with FLiBe is required to reduce uncertainty in vacuum vessel and blanket tank lifetimes. While the
experiments in Ref. [106] indicate that the corrosion of Inconel
in FliBe will be minimal (see Section 5.7), these experiments
do not take into account radiation effects (such as radiationassisted transport of chromium to the surface). This could significantly speed up corrosion in a fusion reactor. In addition,
experiments at higher temperatures (up to 1400 K) are required

to assess corrosion for a Pilot configuration of ARC, where the
blanket temperature will be increased to allow for more efficient
electricity generation. Simple estimates based on a non-ideal
Brayton cycle (see Section 2) indicate that increasing the FLiBe
blanket operating temperature from 900 K to 1200 K would allow the plant thermal efficiency to improve from 40% to 50%.
This increase in blanket temperature would require more robust
structural and first wall materials, further highlighting the need
for fusion materials research.

**8.** **Conclusions**

With a major radius of 3.3 m and minor radius of 1.1 m, ARC
is significantly smaller in size and thermal output than most current reactor designs, which typically generate ∼ 1 GWe. ARC
produces 525 MW of fusion power (∼ 200 MWe), operating
in the promising I-mode regime. Steady state plasma current
is driven by ICRF fast wave and lower hybrid waves, both
launched from the high field side. The reactor has a bootstrap
fraction of only 63%, which gives operators greater control of
the current profile. This, together with the high safety factor
of _q_ 95 ∼ 7, reduces the likelihood of disruptions. The TF coils
use REBCO superconductors, allowing ARC to have an on-axis
magnetic field of 9.2 T and peak field on coil of ∼ 23 T. The TF
coils are also demountable and the tritium breeding blanket is
a tank of liquid FLiBe, which permits all internal components
to be installed as a single module. This allows the device to
perform as a fusion nuclear science facility, testing many different vacuum vessel and divertor configurations. The initial
vacuum vessel is two concentric Inconel 718 shells, separated
by structural ribbing and FLiBe coolant channels that enable a
tritium breeding ratio of 1.1. Neutron shielding allows for ARC
to operate for 9 FPY before the reaching the lower bound on the
TF coils neutron survivability. This lifetime could be increased
dramatically with just a small increase in reactor size.

The ARC reactor design study has shown that high magnetic
field, demountable TF coils, and an all-liquid blanket synergistically combine to provide several advantages over traditional
tokamak designs. First and foremost, the ARC design allows
for much smaller devices. As shown in Section 6, even with the
novel materials required for the ARC design, this small size reduces the overall cost of building a reactor. The modular nature
of ARC allows for the demonstration reactor to also be used as
an FSNF, testing several vacuum vessel/first wall/divertor designs in a reactor-relevant environment. The all-liquid blanket
of ARC simplifies cooling and dramatically reduces the amount
of activated waste produced.

While a full engineering design is beyond the scope of the
ARC study, the benefits and feasibility of compact, high-field
reactor/FNSF designs have been shown. The ARC study has
not identified any insurmountable difficulties with the given design, motivating more detailed study into compact, high-field
devices.

**9.** **Acknowledgments**

We thank Leslie Bromberg, Charles Forsberg, Martin Greenwald, Amanda Hubbard, Brian LaBombard, Bruce Lipschultz,
Earl Marmar, Joseph Minervini, Geoff Olynyk, Michael Short,
Pete Stahle, Makoto Takayasu, and Stephen Wolfe for conversations and comments that improved this paper. We also
thank Zach Hartwig for allowing us to use his C++ wrapper
for MCNP and for advice regarding neutronics. BNS was supported by U.S. DoE Grant No. DE-FG02-94ER54235. JB was
supported by U.S. DoE Grant No. DE-SC008435. FJM was
supported by the U. S. Department of Energy, Office of Fusion
Energy Science under Grant No. DE-FC02-93ER54186. JMS
is supported by the National Science Foundation Graduate Research Fellowship Program, under grant No. 1122374. This
work originated from a MIT Nuclear Science and Engineering
graduate course. DGW acknowledges the support of the NSE
Department and the PSFC.

**References**

[1] F. Najmabadi, et al., The ARIES-I tokamak reactor study, Fusion Technology 19 (3) (1991) 783.

[2] F. Najmabadi, et al., The ARIES-AT advanced tokamak, Advanced technology fusion power plant, Fusion Engineering and Design 3 (23).

[3] F. Najmabadi, et al., Overview of the ARIES-RS reversed-shear tokamak
power plant study, Fusion Engineering and Design 38 (1) (1997) 3.

[4] F. Najmabadi, The ARIES Team, Spherical torus concept as power
plants—the ARIES-ST study, Fusion Engineering and Design 65 (2)
(2003) 143.

[5] G. Olynyk, Z. Hartwig, D. Whyte, H. Barnard, P. Bonoli, L. Bromberg,
M. Garrett, C. Haakonsen, R. Mumgaard, Y. Podpaly, Vulcan: a steadystate tokamak for reactor-relevant plasma–material interaction science,
Fusion Engineering and Design 87 (3) (2012) 224.

[6] B. Coppi, A. Airoldi, F. Bombarda, G. Cenacchi, P. Detragiache,
C. Ferro, R. Maggiora, L. Sugiyama, G. Vecchi, Critical physics issues
for ignition experiments: Ignitor, MITRLE Report PTP99/06.

[7] T. Ando, S. Nishio, Design of the tf coil for a tokamak fusion power
reactor with ybco tape superconductors, in: Fusion Engineering 2005,
Twenty-First IEEE/NPS Symposium on, IEEE, 2005, pp. 1–4.

[8] D. Kingham, A. Sykes, M. Gryaznevich, Efficient compact fusion reactor, uS Patent App. 14/240,809 (Aug. 24 2012).

[9] J. Menard, L. Bromberg, T. Brown, T. Burgess, D. Dix, L. El-Guebaly,
T. Gerrity, R. Goldston, R. Hawryluk, R. Kastner, et al., Prospects for
pilot plants based on the tokamak, spherical tokamak and stellarator,
Nuclear Fusion 51 (10) (2011) 103014.

[10] R. Stambaugh, V. Chan, C. Wong, J. Smith, A. Garofalo, J. Leuer,
[Candidates for a fusion nuclear science facility (FDF and ST-CTF), in:](https://fusion.gat.com/fdf/files/A26780conf_v4.pdf)
37th EPS Conf. on Plasma Physics (Dublin, Ireland), no. P2.110, 2010.
URL `[https://fusion.gat.com/fdf/files/A26780conf_v4.](https://fusion.gat.com/fdf/files/A26780conf_v4.pdf)`
`[pdf](https://fusion.gat.com/fdf/files/A26780conf_v4.pdf)`

[11] M. Greenwald, J. Terry, S. Wolfe, S. Ejima, M. Bell, S. Kaye, G. Neilson, A new look at density limits in tokamaks, Nuclear Fusion 28 (12)
(1988) 2199.

[12] F. Troyon, R. Gruber, H. Saurenmann, S. Semenzato, S. Succi, MHDlimits to plasma confinement, Plasma Physics and Controlled Fusion
26 (1A) (1984) 209.

[13] Y. Podpaly, et al., The lower hybrid current drive system for steady-state
operation of the Vulcan tokamak conceptual design, Fusion Engineering
and Design.

[14] ITER Physics Basis Editors et al, Plasma confinement and transport,
Nuclear Fusion 39 (1999) 2175.

[15] Z. Hartwig, C. Haakonsen, R. Mumgaard, L. Bromberg, An initial study
of demountable high-temperature superconducting toroidal magnets for
the Vulcan tokamak conceptual design, Fusion Engineering and Design
87 (3) (2012) 201.

[16] H. Barnard, Z. Hartwig, G. Olynyk, J. Payne, Assessing the feasibility
of a high-temperature, helium-cooled vacuum vessel and first wall for
the Vulcan tokamak conceptual design, Fusion Engineering and Design
87 (3) (2012) 248–262.

[17] R. Aymar, et al., Summary of the ITER final design report, ITER document G A0 FDR 4 (2001) 01.

[18] R. Crossland, R. Hayward, T. Todd, P. Haynes, J. Hill, A. Morris,
P. Nicholson, R. Crook, COMPASS TF coil dynamic vertical preload
device and PF coil alignment using a fixed coil array, Fusion Technology 1 (1990) 632.

[19] W. Beck, Alcator C-MOD toroidal field magnet assembly, in: 14 [th]

IEEE/NPSS Symposium on Fusion Engineering, IEEE, 1991, p. 292.

[20] [J. Mattingly, Elements of Gas Turbine Propulsion, AIAA education se-](http://books.google.com/books?id=vA98AAAACAAJ)
ries, American Institute of Aeronautics and Astronautics, 2005.
URL `[http://books.google.com/books?id=vA98AAAACAAJ](http://books.google.com/books?id=vA98AAAACAAJ)`

[21] K. Clarno, C. Forsberg, J. Gehin, C. Slater, J. Carbajo, D. Williams,
T. Taiwo, J. Cahalan, T. Kim, J. Sienicki, et al., Trade studies for
the liquid-salt-cooled very high-temperature reactor: Fiscal year 2006
progress report.

[22] J. Wesson, Tokamaks, 3rd Edition, Oxford University Press, 2004, Ch.
1.5, p. 11.

[23] M. Sugihara, V. Lukash, R. Khayrutdinov, Y. Neyatani, Edge safety factor at the onset of plasma disruption during VDEs in JT-60U, Plasma
Physics and Controlled Fusion 46 (2004) 1581.

[24] S. Jardin, C. Bathke, D. Ehst, S. Kaye, C. Kessel Jr, B. Lee, T. Mau,
J. Menard, R. Miller, F. Najmabadi, Physics basis for a tokamak fusion
power plant, Fusion Engineering and Design 48 (3) (2000) 281–298.

[25] R. Stambaugh, L. Lao, E. Lazarus, Relation of vertical stability and aspect ratio in tokamaks, Nuclear Fusion 32 (9) (1992) 1642.

[26] R. J. Thome, J. M. Tarrh, Mhd and fusion magnets: field and force design concepts.

[27] N. Fisch, A. H. Boozer, Creating an asymmetric plasma resistivity with
waves, Physical Review Letters 45 (9) (1980) 720.

[28] N. Pomphrey, Bootstrap dependence on plasma profile parameters, Tech.
rep., Princeton Univ., NJ (1992).

[29] C. Kessel, Bootstrap current in a tokamak, Nuclear Fusion 34 (9) (1994)
1221.

[30] D. Whyte, A. Hubbard, J. Hughes, B. Lipschultz, J. Rice, E. Marmar, M. Greenwald, I. Cziegler, A. Dominguez, T. Golfinopoulos,
N. Howard, L. Lin, R. McDermott, M. Porkolab, M. Reinke, J. Terry,
N. Tsujii, S. Wolfe, S. Wukitch, Y. Lin, the Alcator C-Mod Team, Imode: an H-mode energy confinement regime with L-mode particle
transport in Alcator C-Mod, Nuclear Fusion 50 (10) (2010) 105005.

[31] A. E. Hubbard, D. G. Whyte, R. M. Churchill, I. Cziegler,
A. Dominguez, T. Golfinopoulos, J. W. Hughes, J. E. Rice, I. Bespamyatnov, M. J. Greenwald, N. Howard, B. Lipschultz, E. S. Marmar, M. L.
Reinke, W. L. Rowan, J. L. Terry, the Alcator C-Mod Group, Edge energy transport barrier and turbulence in the I-mode regime on Alcator
C-Mod, Physics of Plasmas 18 (5) (2011) 056115.

[32] F. Wagner, G. Becker, K. Behringer, D. Campbell, A. Eberhagen, W. Engelhardt, G. Fussmann, O. Gehre, J. Gernhardt, G. v. Gierke, et al.,
Regime of improved confinement and high beta in neutral-beam-heated
divertor discharges of the ASDEX tokamak, Physical Review Letters
49 (19) (1982) 1408.

[33] [J. R. Walk, Pedestal structure and stability in high-performance plasmas](http://dspace.mit.edu/handle/1721.1/95524)
[on Alcator C-Mod, Sc.D. thesis, Massachusetts Institute of Technology](http://dspace.mit.edu/handle/1721.1/95524)
(2014).
URL `[http://dspace.mit.edu/handle/1721.1/95524](http://dspace.mit.edu/handle/1721.1/95524)`

[34] M. B´ecoulet, G. Huysmans, Y. Sarazin, X. Garbet, P. Ghendrih, F. Rimini, E. Joffrin, X. Litaudon, P. Monier-Garbet, et al., Edge localized
mode physics and operational aspects in tokamaks, Plasma Physics and
Controlled Fusion 45 (12A) (2003) A93.

[35] A. Dominguez, Study of density fluctuations and particle transport at the
edge of I-mode plasmas, Ph.D. thesis, Massachusetts Institute of Technology, Cambridge, MA (2012).

[36] D. Whyte, E. Marmar, A. Hubbard, J. Hughes, A. Dominguez,
M. Greenwald, I-mode for ITER?, in: 53 [rd] Annual Meeting of the APS
Division of Plasma Physics, 2011.

[37] P. Stangeby, The plasma boundary of magnetic fusion devices, The
Plasma Boundary of Magnetic Fusion Devices. Series: Series in Plasma
Physics, ISBN: 978-0-7503-0559-4. Taylor & Francis, Edited by Peter

Stangeby, vol. 7 7.

[38] T. Taylor, E. Lazarus, M. Chu, J. Ferron, F. Helton, W. Howl, G. Jackson, T. Jensen, et al., Profile optimization and high beta discharges, and
stability of high elongation plasmas in the DIII-D tokamak, in: Plasma
Physics and Controlled Nuclear Fusion Research 1990, Vol. 1, IAEA,
1991, p. 177.

[39] A. E. Hubbard, D. G. Whyte, R. M. Churchill, A. Dominguez, J. W.
Hughes, Y. Ma, E. Marmar, Y. Lin, M. L. Reinke, A. E. White, Threshold
conditions for transitions to I-Mode and H-Mode with unfavorable ion
grad B drift direction, Nuclear Fusion 52 (11) (2012) 114009.

[40] J. Walk, J. Hughes, A. Hubbard, J. Terry, D. Whyte, A. White, S. Baek,
M. Reinke, C. Theiler, R. Churchill, et al., Edge-localized mode avoidance and pedestal structure in I-mode plasmas, Physics of Plasmas
(1994-present) 21 (5) (2014) 056103.

[41] P. Snyder, H. Wilson, J. Ferron, L. Lao, A. Leonard, D. Mossessian,
M. Murakami, T. Osborne, A. Turnbull, X. Xu, Elms and constraints
on the H-mode pedestal: peeling–ballooning stability calculation and
comparison with experiment, Nuclear Fusion 44 (2) (2004) 320.

[42] J. Freidberg, Plasma Physics and Fusion Energy, 1st Edition, Cambridge
University Press, 2007, Ch. 15.9.4, p. 623.

[43] M. Porkolab, Fusion, 1st Edition, Academic Press, New York, NY, 1981,
Ch. 13, p. 151.

[44] M. Brambilla, Ignition with lower hybrid heating, Physics of Plasmas
Close to Thermonuclear Conditions 1 (1980) 291–311.

[45] M. Porkolab, Plasma heating by fast magnetosonic waves in tokamaks,
in: AIP Conf. Proc., Vol. 314, 1994, p. 99.

[46] C. Karney, N. Fisch, Efficiency of current drive by fast waves, Physics
of Fluids 28 (1985) 116.

[47] R. Devoto, D. Blackfield, M. Fenstermacher, P. Bonoli, M. Porkolab,
G. Tinios, Modelling of lower hybrid current drive in self-consistent
elongated tokamak equilibria, Nuclear Fusion 32 (5) (1992) 773.

[48] H. Grad, H. Rubin, Hydromagnetic equilibria and force-free fields, Journal of Nuclear Energy (1954) 7 (3) (1958) 284.

[49] V. Shafranov, Plasma equilibrium in a magnetic field, Reviews of Plasma
Physics 2 (1966) 103.

[50] S. Jardin, C. Kessel, T. Mau, R. Miller, F. Najmabadi, V. Chan, M. Chu,
R. LaHaye, L. Lao, T. Petrie, et al., Physics basis for the advanced tokamak fusion power plant, ARIES-AT, Fusion Engineering and Design
80 (1) (2006) 25.

[51] A. Messiaen, M. Vervier, P. Dumortier, D. Grine, P. Lamalle, F. Durodi´e,
R. Koch, F. Louche, R. Weynants, Preparing ITER ICRF: development
and analysis of the load resilient matching systems based on antenna
mock-up measurements, Nuclear Fusion 49 (5) (2009) 055004.

[52] A. Garofalo, E. Doyle, J. Ferron, C. Greenfield, R. Groebner, A. Hyatt, G. Jackson, R. Jayakumar, J. Kinsey, R. La Haye, et al., Access to
sustained high-beta with internal transport barrier and negative central
magnetic shear in DIII-D, Physics of Plasmas 13 (5) (2006) 056110.

[53] T. Luce, M. Wade, J. Ferron, P. Politzer, A. Hyatt, A. Sips, M. Murakami, High performance stationary discharges in the DIII-D tokamak,
Physics of Plasmas (1994-present) 11 (5) (2004) 2627.

[54] M. Zarnstorff, Prospects and risk tradeoffs for steady-state MFE, in:
MFE Roadmapping Workshop, PPPL, Princeton, NJ, 2011.

[55] O. Sauter, C. Angioni, Y. Lin-Liu, Neoclassical conductivity and bootstrap current formulas for general axisymmetric equilibria and arbitrary
collisionality regime, Physics of Plasmas 6 (1999) 2834–2839.

[56] R. Motley, W. Hooke, Active-passive waveguide array for wave excitation in plasmas, Nuclear Fusion 20 (2) (1980) 222.

[57] M. Preynas, A. Ekedahl, N. Fedorczak, M. Goniche, D. Guilhem,
J. Gunn, J. Hillairet, X. Litaudon, J. Achard, G. Berger-By, J. Belo,
E. Corbel, L. Delpech, T. Ohsako, M. Prou, Coupling characteristics
of the ITER-relevant lower hybrid antenna in Tore Supra: experiments
and modelling, Nuclear Fusion 51 (2) (2011) 023001.

[58] S. Maebara, T. Imai, T. Nagashima, S. Itoh, K. Tetsuka, S. Miyake,
H. Yonezawa, K. Ohya, Development of high RF efficiency 5GHz
klystron for LHRF system in next tokamak machine, in: Fusion Technology, Vol. 1, 1994, p. 561.

[59] S. Orfanidis, Electromagnetic [Waves](http://www.ece.rutgers.edu/$\sim $orfanidi/ewa/) and Antennas, Orfanidis, S.J.,
2013, Ch. 9.8, p. 382.
URL `[http://www.ece.rutgers.edu/$\sim$orfanidi/ewa/](http://www.ece.rutgers.edu/$\sim $orfanidi/ewa/)`

[60] R. Goldston, Burning plasma experiment physics design description.

[61] F. Mangiarotti, J. Goh, M. Takayasu, L. Bromberg, J. Minervini,

D. Whyte, Demountable toroidal field magnets for use in a compact
modular fusion reactor, Journal of Physics: Conference Series 507
(2014) 032030.

[62] [P. J. Lee, A comparison of superconductor critical currents (Apr 2014).](http://fs.magnet.fsu.edu/~lee/plot/plot.htm)
URL `[http://fs.magnet.fsu.edu/~lee/plot/plot.htm](http://fs.magnet.fsu.edu/~lee/plot/plot.htm)`

[63] P. N. Arendt, S. R. Foltyn, Biaxially textured [ibad-mgo](http://journals.cambridge.org/article_S0883769400016018) templates
for [ybco-coated](http://journals.cambridge.org/article_S0883769400016018) conductors, MRS Bulletin 29 (2004) 543–550.
`[doi:10.1557/mrs2004.160](http://dx.doi.org/10.1557/mrs2004.160)` .
URL `[http://journals.cambridge.org/article_](http://journals.cambridge.org/article_S0883769400016018)`
`[S0883769400016018](http://journals.cambridge.org/article_S0883769400016018)`

[64] R. P. Reed, A. F. Clark, Materials at low temperatures, American Society
for Metals, 1983.

[65] [J. Lu, E. S. Choi, H. D. Zhou, Physical properties of hastelloy R⃝](http://scitation.aip.org/content/aip/journal/jap/103/6/10.1063/1.2899058) c-276 [TM]

[at cryogenic temperatures, Journal of Applied Physics 103 (6) (2008) –.](http://scitation.aip.org/content/aip/journal/jap/103/6/10.1063/1.2899058)
`[doi:http://dx.doi.org/10.1063/1.2899058](http://dx.doi.org/http://dx.doi.org/10.1063/1.2899058)` .
URL `[http://scitation.aip.org/content/aip/journal/jap/](http://scitation.aip.org/content/aip/journal/jap/103/6/10.1063/1.2899058)`
`[103/6/10.1063/1.2899058](http://scitation.aip.org/content/aip/journal/jap/103/6/10.1063/1.2899058)`

[66] J. W. Ekin, Experimental Techniques for Low-Temperature Measurements, Oxford University Press, 2006.

[67] S. Ito, T. Ohinata, L. Bromberg, H. Hashizume, Structure Improvement
and Joint Resistance Estimation in Demountable Butt and Edge Joints of
a Stacked REBCO Conductor Within a Metal Jacket, IEEE Transactions
on Applied Superconductivity 23 (3) (2013) 4802408.

[68] S. Ito, N. Yanagi, H. Hashizume, A. Sagara, Development of a 100-kAclass HTS conductor and its mechanical joint for the helical fusion reactor, in: Second HTS4Fusion Conductor Workshop, Villigen, Switzerland, 2014.

[69] A. Nyilas, K. Nikbin, A. Portone, C. Sborchia, Tensile, fracture, fatigue
life, and fatigue crack growth rate behavior of structural materials for
the ITER magnets: the European contribution, Advances in Cryogenic
Engineering Materials 50 (2004) 176.

[70] R. J. Thome, J. M. Tarrh, MHD and fusion magnets, John Wiley & Sons,
Inc., New York, NY, 1982.

[71] W. Chung, B. Lim, M. Kim, H. Park, K. Kim, Y. Chu,
S. Lee, Mechanical and thermal [characteristics](http://scitation.aip.org/content/aip/proceeding/aipcp/10.1063/1.1774582) of insulation
materials for the kstar magnet system at cryogenic tempera[ture,](http://scitation.aip.org/content/aip/proceeding/aipcp/10.1063/1.1774582) AIP Conference Proceedings 711 (1) (2004) 297–306.
`[doi:http://dx.doi.org/10.1063/1.1774582](http://dx.doi.org/http://dx.doi.org/10.1063/1.1774582)` .
URL `[http://scitation.aip.org/content/aip/proceeding/](http://scitation.aip.org/content/aip/proceeding/aipcp/10.1063/1.1774582)`
`[aipcp/10.1063/1.1774582](http://scitation.aip.org/content/aip/proceeding/aipcp/10.1063/1.1774582)`

[72] Y. Iwasa, Case Studies in Superconducting Magnets, Springer, New
York, NY, 2009.

[73] T. Lehner, Y. Zhang, Development, manufacturing and applications of
2G HTS wire at SuperPower, in: Center for Emergent Superconductivity

   - Fall 2011 Workshop, Urbana, IL, 2011.

[74] V. Selvamanickam, Y. Yao, Y. Liu, J. Liu, N. Khatri, E. Galtsyan, G. Majkic, Y. Chen, C. Lei, Progress in development of MOCVD-based coated
conductors, in: Applied Superconductivity Conference, Portland, OR,
2012.

[75] C. Sborchia, E. Soto, R. Batista, B. Bellesia, A. Oliva, E. Rebollo,
T. Boutboul, E. Bratu, J. Caballero, M. Cornelis, J. Fanthome, R. Harrison, M. Losasso, A. Portone, H. Rajainmaki, P. Readman, P. Valente,
Overview of ITER magnet system and European contribution, in: Fusion Engineering (SOFE), 2011 IEEE/NPSS 24th Symposium on, 2011,
pp. 1–8. `[doi:10.1109/SOFE.2011.6052218](http://dx.doi.org/10.1109/SOFE.2011.6052218)` .

[76] P. Kittel, Cryocooler performance estimator, Cryocoolers (14) (2007)
563.

[77] COMSOL Inc., COMSOL Multiphysics 4.3b, `[http://www.comsol.](http://www.comsol.com)`
`[com](http://www.comsol.com)` (2013).

[78] H. Shin, J. Dizon, R. Ko, T. Kim, D. Ha, S. Oh, Reversible tensile strain
dependence of the critical current in YBCO coated conductor tapes,
Physica C: Superconductivity 463 (0) (2007) 736, proceedings of the
19th International Symposium on Superconductivity (ISS 2006).

[79] T. W. Orange, Tensile coupon tests of cryoformed aisi 301 stainlesssteel pressure vessels at cryogenic temperatures, NASA Technical Note
NASA TN D-2202, National Aeronautics and Space Administration
(1964).

[80] R. A. Matula, Electrical resistivity of [copper,](http://scitation.aip.org/content/aip/journal/jpcrd/8/4/10.1063/1.555614) gold, palladium, and
[silver,](http://scitation.aip.org/content/aip/journal/jpcrd/8/4/10.1063/1.555614) Journal of Physical and Chemical Reference Data 8 (4) (1979)
1147–1298. `[doi:http://dx.doi.org/10.1063/1.555614](http://dx.doi.org/http://dx.doi.org/10.1063/1.555614)` .
URL `[http://scitation.aip.org/content/aip/journal/](http://scitation.aip.org/content/aip/journal/jpcrd/8/4/10.1063/1.555614)`

`[jpcrd/8/4/10.1063/1.555614](http://scitation.aip.org/content/aip/journal/jpcrd/8/4/10.1063/1.555614)`

[81] B. Sorbom, J. Ball, H. Barnard, C. Haakonsen, Z. Hartwig, G. Olynyk,
J. Sierchio, D. Whyte, Liquid immersion blanket design for use in a compact modular fusion reactor, Bulletin of the American Physical Society
57.

[82] D.-K. Sze, K. McCarthy, M. Sawan, M. Tillack, A. Ying, S. Zinkle, Flibe
assessments, Tech. rep., Argonne National Lab., IL (US) (2000).

[83] D. Williams, L. Toth, K. Clarno, Assessment of candidate molten salt
coolants for the advanced high temperature reactor (AHTR), United
States. Department of Energy, 2006.

[84] G. Federici, C. H. Skinner, J. N. Brooks, J. P. Coad, C. Grisolia, A. A.
Haasz, A. Hassanein, V. Philipps, C. S. Pitcher, J. Roth, et al., Plasmamaterial interactions in current tokamaks and their implications for next
step fusion reactors, Nuclear Fusion 41 (12) (2001) 1967.

[85] A. M¨oeslang, V. Heinzel, H. Matsui, M. Sugimoto, The IFMIF test facilities design, Fusion Engineering and Design 81 (8) (2006) 863.

[86] L. Bromberg, M. Tekula, L. El-Guebaly, R. Miller, Options for the use
of high temperature superconductor in tokamak fusion reactor designs,
Fusion Engineering and Design 54 (2) (2001) 167.

[87] F. B. Brown, R. Barrett, T. Booth, J. Bull, L. Cox, R. Forster, T. Goorley,
R. Mosteller, S. Post, R. Prael, et al., MCNP version 5, Transactions of
the American Nuclear Society 87 (273) (2002) 4.

[88] R. Beck, Research and development of metal hydrides, USAEC report
LAR1960-10.

[89] L. A. El-Guebaly, S. Malang, Toward the ultimate goal of tritium selfsufficiency: Technical issues and requirements imposed on ARIES advanced power plants, Fusion Engineering and Design 84 (12) (2009)
2072.

[90] S. Sato, T. Nishitani, Impact of armor materials on tritium breeding ratio
in the fusion reactor blanket, Journal of Nuclear Materials 313 (2003)
690.

[91] S. Delpech, C. Cabet, C. Slim, G. S. Picard, Molten fluorides for nuclear
applications, Materials Today 13 (12) (2010) 34–41.

[92] T. Eich, A. Leonard, R. Pitts, W. Fundamenski, R. Goldston, T. Gray,
A. Herrmann, A. Kirk, A. Kallenbach, O. Kardaun, et al., Scaling of the
tokamak near the scrape-off layer H-mode power width and implications
for ITER, Nuclear Fusion 53 (9) (2013) 093031.

[93] D. Whyte, G. Olynyk, H. Barnard, P. Bonoli, L. Bromberg, M. Garrett,
C. Haakonsen, Z. Hartwig, R. Mumgaard, Y. Podpaly, Reactor similarity
for plasma–material interactions in scaled-down tokamaks as the basis
for the Vulcan conceptual design, Fusion Engineering and Design 87 (3)
(2012) 234–247.

[94] P. Rebut, R. Bickerton, B. Keen, The Joint European Torus: installation,
first results and prospects, Nuclear Fusion 25 (9) (1985) 1011.

[95] M. Greenwald, R. Boivin, F. Bombarda, P. Bonoli, C. Fiore, D. Garnier,
J. Goetz, S. Golovato, M. Graf, R. Granetz, et al., H mode confinement
in Alcator C-Mod, Nuclear Fusion 37 (6) (1997) 793.

[96] K. Daryabeigi, Analysis and testing of high temperature fibrous insulation for reusable launch vehicles, Tech. Rep. AIAA 99-1044, NASA
Langley Research Center (January 1999).

[97] Special Metals Corporation, Pub. No. SMC-045 (September 2007).

[98] G. Olynyk, Radiation asymmetry and MHD activity in rapid shutdowns
on Alcator C-Mod, Ph.D. thesis, Massachusetts Institute of Technology
(September 2013).

[99] S. Mirnov, J. Wesley, N. Fujisawa, Y. Gribov, O. Gruber, T. Hender,
N. Ivanov, S. Jardin, J. Lister, F. Perkins, et al., ITER physics basis,
chapter 3: MHD stability, operational limits and disruptions, Nuclear
Fusion 39 (12) (1999) 2251.

[100] H. Iida, V. Khripunov, L. Petrizzi, G. Federici, et al., Nuclear analysis
report, ITER Design Description Document, G 73.

[101] P. Jung, C. Liu, J. Chen, Retention of implanted hydrogen and helium
in martensitic stainless steels and their effects on mechanical properties,
Journal of Nuclear Materials 296 (2001) 165.

[102] A. M¨oeslang, D. Preininger, Effect of helium implantation on the mechanical properties and the microstructure of the martensitic 12% Crsteel 1.4914, Journal of Nuclear Materials 155 (1988) 1064.

[103] L. El-Guebaly, Nuclear performance assessment of ARIES-AT, Fusion
Engineering and Design 80 (1) (2006) 99.

[104] S. Sborchia, et al., Design and manufacture of the ITER vacuum vessel,
in: 25 [th] Symposium on Fusion Engineering (SOFE), San Francisco, CA,
2013.

[105] A. Sagara, O. Mitarai, S. Imagawa, T. Morisaki, T. Tanaka,
N. Mizuguchi, T. Dolan, J. Miyazawa, K. Takahata, H. Chikaraishi,
et al., Conceptual design activities and key issues on lhd-type reactor
ffhr, Fusion Engineering and Design 81 (23) (2006) 2703–2712.

[106] M. Kondo, T. Nagasaka, T. Muroga, A. Sagara, N. Noda, Q. Xu, D. Ninomiya, N. Masaru, A. Suzuki, T. Terai, High performance corrosion
resistance of nickel-based alloys in molten salt flibe, Fusion Science and
Technology 56 (1) (2009) 190.

[107] [D. Meade, A comparison of unit costs for FIRE and ITER (July 2002).](http://fire.pppl.gov/snow_ITERFIRE_cost.pdf)
URL `[http://fire.pppl.gov/snow_ITERFIRE_cost.pdf](http://fire.pppl.gov/snow_ITERFIRE_cost.pdf)`

[108] Metal prices in the United States through 2010, Tech. rep., U.S. Geological Survey (2013).

[109] A. Ascione, Continental [steel](http://continentalsteel.com/) and tube, private communication (July
2014).
URL `[http://continentalsteel.com/](http://continentalsteel.com/)`

[110] [E. Lord, Superpower inc., private communication (July 2013).](http://www.superpower-inc.com/)
URL `[http://www.superpower-inc.com/](http://www.superpower-inc.com/)`

[111] J. Sanders, A review of possible choices for secondary coolants for
molten salt reactors, ORNL CF-71-8-10, Oak Ridge National Laboratory, Oak Ridge, TN.

[112] [V. Duz, Adma products, private communication (June 2014).](http://www.admaproducts.com/)
URL `[http://www.admaproducts.com/](http://www.admaproducts.com/)`

[113] T. Dolan, G. Longhurst, E. Garcia-Otero, A vacuum disengager for tritium removal from HYLIFE-II reactor flibe, Tech. rep., EG and G Idaho,
Inc., Idaho Falls, ID (United States) (1992).

[114] S. Fukada, A design for recovery of tritium from flibe loop in FFHR-2,
Fusion Power Plants and Related Advanced Technologies.

[115] M. Abdou, The APEX TEAM, A. Ying, N. Morley, K. Gulec, S. Smolentsev, M. Kotschenreuther, et al., On the exploration of innovative concepts for fusion chamber technology, Fusion Engineering and Design
54 (2) (2001) 181.

