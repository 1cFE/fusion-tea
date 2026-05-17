---
source: "https://www.osti.gov/servlets/purl/6360934"
source_type: "url"
extracted_at: "2026-04-06T05:33:58.862933+00:00"
content_hash_sha256: "e3fce39b7499dcc75a7f106c0a06d7ea90b95a16948cd0acaf4cb7a7dbaa53c3"
backend: "pdf_pipeline"
---

![](images/tmpb2nh9hqp.pdf-0-full.png)

_/ttP_ r.
**7>a** **3**
# **_(!)_**

## **UCRL-53356** **Electromagnetic Pumping of** **Liquid Lithium in Inertial** **Confinement Fusion Reactors** **R. S. Baker, J. A. Blink, and M. J. Tessier**

#### MASTER

## **BISTWBUT1GN Of THIS DOCUMENT IS IMUMcD**

![](images/tmpb2nh9hqp.pdf-0-0.png)

## DISCLAIMER

This report was prepared as an account of work sponsored by an agency of the United States Government. Neither the United States Government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

---

## DISCLAIMER

Portions of this document may be illegible in electronic image products. Images are produced from the best available original document.

![](images/tmpb2nh9hqp.pdf-2-full.png)
## **UCRL-53356** **Distribution Category UC-21** **DISCLAIMER**

This report was prepared as an account of work sponsored by an agency of the United States
Government. Neither the United States Government nor any agency thereof, nor any of their
employees, makes any warranty, express or implied, or assumes any legal liability or responsi- UCRL 53356

bility for the accuracy, completeness, or usefulness of any information, apparatus, product, or
process disclosed, or represents that its use would not infringe privately owned rights. Refer- DE83 010359
ence herein to any specific commercial product, process, or service by trade name, trademark,
manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recom­
mendation, or favoring by the United States Government or any agency thereof. The views
and opinions of authors expressed herein do not necessarily state or reflect those of the

United States Government or any agency thereof.

###### **Electromagnetic Pumping of**
##### **Liquid Lithium in Inertial**
###### **Confinement Fusion Reactors**

## R. S. Baker,* J. A. Blink, and M. J. Tessier*

**Manuscript** **date:** **March** **1,** **1983**

***Energy** **Technology** **Engineering** **Center**
**Canoga** **Park,** **California** **91304**

LAWRENCE LIVERMORE NATIONAL LABORATORY

University of California   - Livermore, California   - 94550

Available from: National Technical Information Service    - U.S. Department of Commerce
5285 Port Royal Road    - Springfield, VA 22161* $8.50 per copy    - (Microfiche $4.50)

BisraeunsN **of** _m_ **oecuser** **i;**

This is a nearly blank page containing only a page number "ii" at the bottom. There is no substantive content to extract.

![](images/tmpb2nh9hqp.pdf-4-full.png)

**Contents**

Abstract.............................................................................................................................................................. 1
Introduction......................................................................................................................................................... 1
Electromagnetic Pumps..................................................................................................................................... 2

History......................................................................................................................................................... 2
EM Pump Geometries................................................................................................................................ 3

Conduction Pumps .......................................................................................................................... 4
Induction Pumps.............................................................................................................................. 4
Comparison of HREMP and ALIP Geometries......................................................................................11

Largest Pumps Built to Date .............................................................................................................11
Flow-Rate Control............................................................................................................................. 12
Winding Effectiveness........................................................................................................................ 12
Power-Factor Correction.................................................................................................................... 12
Design Procedure for the HREMP.................................................................................................................. 13

Rotor Construction ....................................................................................................................................13
Normally Conducting Winding................................................................................................................ 14
Superconducting Winding........................................................................................................................ 20
Cryogenic Cooling Power for a Superconducting Winding.................................................................. 20
Rotor-Winding Power Supply and Current Control..............................................................................21
Design of an HREMP for the HYLIFE ICE Reactor....................................................................................... 22

Validation of the Design Procedure.........................................................................................................22
The HYLIFE Design Point........................................................................................................................ 22
Startup of the HYLIFE HREMP with a Normally Conducting Winding..............................................23
Sensitivity of Design Point to _Kv_ _K2,_ and _K3_ ......................................................................................... 27
Tradeoffs Among Efficiency, Mass, Diameter, and Winding Type.......................................................28
Selection of Pump Type............................................................................................................................29
Acknowledgments............................................................................................................................................. 30
References...........................................................................................................................................................31
Glossary.............................................................................................................................................................. 32

iii

![](images/tmpb2nh9hqp.pdf-5-full.png)

**Electromagnetic** **Pumping** **of**
**Liquid** **Lithium** **in** **Inertial**
**Confinement** **Fusion** **Reactors**

**Abstract**

The basic operating principles and geometries of ten electromagnetic pumps are de­
scribed. Two candidate pumps, the annular-linear-induction pump and the helical-rotor
electromagnetic pump, are compared for possible use in a full-scale liquid-lithium inertial
confinement fusion reactor. A parametric design study completed for the helical-rotor
pump is shown to be valid when applied to an experimental sodium pump. Based upon
the preliminary HYLIFE requirements for a lithium flow rate per pump of 8.08 m3/s at a
head of 82.5 kPa, a complete set of 70 variables are specified for a helical-rotor pump with
either a normally conducting or a superconducting winding. The two alternative designs
are expected to perform with efficiencies of 50 and 60%, respectively.

**Introduction**

One highly promising approach to the future
production of energy is inertial confinement
fusion (ICF). The HYLIFE reactor,1 which makes
maximum use of existing materials and technol­
ogy, is shown in Fig. 1. HYLIFE will circulate ap­
proximately 800 tonnes of free-flowing lithium at
a rate of 72 m3/s (1.14 X 106 gpm) to form a
liquid-metal wall (LMW) between the pulsed
fusion plasma and the reactor vessel. The LMW
will serve to

  - Absorb the pulsed fusion energy and
transport it from the reactor chamber.

  - Shield the reactor vessel from neutron,
x-ray, and debris damage.

  - Breed the tritium fuel.
Liquid-metal circuits in the HYLIFE ICF reac­
tor are characterized by a high flow rate, a low
head, and, because of the pulsed nature of the
energy source, cyclic pressure pulses. The HYLIFE
circuit characteristics, coupled with the reactive
nature of liquid lithium, comprise a demanding
set of requirements for the pumps.

Large, mechanical (impeller) pumps have
been developed for use with liquid-sodium
circuits in liquid-metal fast-breeder reactors
(LMFBR). Such impeller pumps are characteristi­
cally well suited for the high-head and relatively

steady-state conditions that prevail in the LMFBR.
Conversely, impeller pumps are poorly suited for
the high-flow, low-head circuits in HYLIFE. Fur­
ther, because the HYLIFE liquid-metal curcuit in­
cludes a vacuum region and because the pulsed
fusion source induces pressure pulses in the
liquid-metal circuit, impeller-type pumps will
have cavitation problems. Modification of impel­
ler pumps for use in the HYLIFE lithium circuits
would probably result in a significant degradation
of both efficiency and reliability.

Types of pumps that are well matched to the
requirements of ICF reactors are advanced me­
chanical (inducer) pumps and certain types of
electromagnetic (EM) pumps. In this report, we
present the results of our study on EM pumps in
general and on one promising candidate that is
suitable for use with ICF reactors, the helical-rotor
EM pump (HREMP).

Our report is divided into three sections. In
the first section, we describe the characteristics of
ten EM pumps, and we compare the two pump
types capable of being scaled up to HYLIFE de­
sign conditions. In the second section, we outline
the procedure used to design our candidate pump,
the HREMP. In the third section, we present the
results of our parametric design study.

![](images/tmpb2nh9hqp.pdf-6-full.png)

![](images/tmpb2nh9hqp.pdf-6-0.png)
## **Figure 1. Concept for the HYLIFE inertial confinement fusion reactor.**

**Electromagnetic** **Pumps**

History

In his Bakerian Lecture Series of 1832,
Michael Faraday2 reported what is perhaps the
first attempt to use an EM pump. During the next
century, the metals industry adapted EM pumps
as stirring devices used in steel production. The
first large-scale industrial application (1937) of
such devices was in Europe, where the ASEA
(Swedish) electromagnetic stirrer is still exten­
sively used.

Beginning in 1948, General Electric and AllisChalmers evaluated larger-scale EM pumps as al­
ternatives to mechanical pumps that were being
designed for liquid-metal cooled nuclear reactors.
These companies found that for high-head
steady-state conditions, mechanical pumps were
more efficient than EM pumps. Furthermore, the
disparity in efficiency increased with the tempera­
ture of the liquid metal being pumped because the
electrical conductivity of the liquid metal de­
creases with increasing temperature. Thus, be­
cause of their relative inefficiency, EM pumps

![](images/tmpb2nh9hqp.pdf-7-full.png)

were only considered as backup designs for mod­
ern nuclear reactors.

EM pumps have proven to be reliable compo­
nents on a smaller scale. They are extensively
used as liquid-metal stirring devices, as pumps in
experimental liquid-metal loops, and as pumps for
low-flow side-streams in liquid-metal-cooled
nuclear reactors.

For high-flow low-head ICF reactors with
neutron-induced pressure pulses in the liquid
metal, EM pumps may prove to be more reliable
than mechanical pumps. In addition, the effi­
ciency, weight, and cost of EM pumps promise to
be competitive.

EM Pump Geometries

All EM pumps operate by using the Lorentz
force. When a magnetic field is applied so that it is
perpendicular to an electrical current, the resul­
tant Lorentz force is perpendicular to both. The
basic equation that describes how the force on a
liquid metal is produced in an EM pump is

## **F = IT X B, (1)** where F is the resultant force in newtons; B is the

magnetic flux density in teslas, which acts on a
filament of liquid metal with length T in meters;
## and I is the filament current in amperes. If I and B

![](images/page_007_eq_0.png)
are perpendicular to one another, then the resul­
## tant force F will be mutually perpendicular to

both so that the liquid metal will flow in the direc­
tion shown in Fig. 2.

Direction of magnetic flux density B

Direction of liquid-metal
flow (force F)

**Figure** **2.** **Basic** **EM-pump** **geometry.**

In Table 1, EM pumps are classified3 accord­
ing to how the current is produced in the liquid
## metal, and the relative directions of B, I, and F are

listed. The two major types of pumps are conduc­
tion and induction. Conduction pumps are further
classified as either direct-current or alternatingcurrent pumps, while induction pumps are classi­
fied according to whether the pump has station­
ary windings or rotating magnets. Figures 3

![](images/tmpb2nh9hqp.pdf-7-0.png)

![](images/tmpb2nh9hqp.pdf-7-1.png)

## Table 1. Classification of electromagnetic pumps.

| Type of pump | Direction of magnetic flux density* B | Direction of electric current* J | Resultant force F |
|---|---|---|---|
| **Conduction** | | | |
| Direct current | | | |
| Electromagnetic | vertical | transverse | axial |
| Permanent magnet | vertical | transverse | axial |
| Alternating current | vertical | transverse | axial |
| **Induction** | | | |
| Rotating magnet | | | |
| Helical rotor (HEREMPS) | radial | equal vertical and circumferential components | equal circumferential and axial components |
| Cylindrical rotor | radial | vertical (axial) | circumferential (screw guided) |
| Circle-arc duct | horizontal | transverse | axial |
| Electromagnetic centrifugal | axial | | circumferential (spins outward?) |
| Stationary magnet | | | |
| Single-phase induction | radial | (circumferential) | vertical (axial) |
| Polyphase induction | | | |
| Flat linear induction (FLIP) | transverse | vertical | axial |
| Helical induction | radial | vertical (axial) | circumferential |
| Annular linear induction (ALIP) | radial | (circumferential) | axial |

* Directions apply to the location where the pumping force is produced. Since both the electric current and magnetic-field lines form loops, other directions apply at other locations.

through 12 illustrate the geometry and basic operating principles of each pump type.

## Conduction Pumps

A direct-current conduction pump is shown in Fig. 3. The field coil produces a steady magnetic field (illustrated here in the vertical direction) within the field structure. The magnetic field structure has a gap through which the liquid metal flows. A steady electrical current (shown in the transverse direction) is propagated across the liquid metal from bar to bar so that the current is perpendicular to the magnetic field. The resultant force F causes the liquid metal to flow in the mutually perpendicular (axial) direction. Direct-current conduction pumps may be constructed with either electromagnets or permanent magnets.

An alternating current conduction pump is shown in Fig. 4. Alternating current in the two transformer primary windings produces an alternating current in the transformer secondary circuit (transverse direction) consisting of the bus bars, pump duct, and liquid metal. A perpendicular magnetic field (vertical direction) is produced in the field structure by the four field coils (only one coil is shown). Once again, the resultant force F is in the direction of (axial) flow. The alternating current conduction pump in Fig. 4 has two pumping regions where the magnetic fields and electric currents pass through the liquid metal.

Small conduction pumps can be built inexpensively for high-pressure, low-flow-rate applications. However, they cannot be easily scaled up for high-flow-rate applications because of magnetic-field losses at the ends. Conduction pumps have low efficiencies; they require high current at low voltage, and their bus bars tend to break loose from the pump duct due to metallurgical problems with the liquid metal. They fail. In addition, the ac conduction pump produces a double-frequency pulsation in the pressure developed by the pump.

## Induction Pumps

Induction pumps do not directly supply the electrical current component of the Lorentz force. Instead, the magnetic field of the pump induces the current in the liquid metal. The induced current can be calculated using Faraday's Law of Induction.

![](images/tmpb2nh9hqp.pdf-9-full.png)

![](images/tmpb2nh9hqp.pdf-9-1.png)

Liquid-metal

of transformer

B (vertical)

structure (1 of 2)

**Figure** **4.** **Alternating-current** **conduction** **pump.**

_j_ E _■_ _dt=_ _—^f_ _B_ _■_ / (2)

where area _S_ is enclosed by curve C. The left-hand
side of Eq. (2) is the voltage induced around the
loop. The current flowing around the loop is this
voltage divided by the loop's electrical imped­
ance. Since Eq. (2) holds that current is propor­
tional to the time-rate-of-change of the magnetic
flux density, induction pumps require that the
magnetic field be varied. A varying magnetic field
can be produced by a moving magnet or by alter­
nating current in a stationary winding.

**Induction** **Pumps** **with** **Rotating** **Magnets.** A
![](images/page_009_eq_0.png)
helical-rotor EM pump (HREMP) is illustrated in
Fig. 5 and its operating principle is shown in
Fig. 6. The rotating (radial) magnetic field induces
diagonal currents, with both vertical and circum­
ferential components, in the liquid-metal pump­
ing region. The current loops roughly parallel the
windings, with the diagonal current in the liquid
metal appearing over the approximate centerline
of each pole on the rotor. The interaction of the
diagonal currents and the radial magnetic field
drives the liquid metal in a helical path without
the use of guide vanes.

![](images/tmpb2nh9hqp.pdf-9-0.png)

Flow

**Figure** **5.** **Helical-rotor** **electromagnetic** **pump**
## **(HREMP).**

![](images/tmpb2nh9hqp.pdf-9-2.png)

![](images/tmpb2nh9hqp.pdf-10-full.png)

(b) Magnetic flux density, B (d) Induced voltage, V, and current, I

## **Figure 6. Operating principle of the HREMP. (a) Pump rotor and winding slots, (b) Liquid-metal**

**annulus,** **where** **the** **solid** **diagonal** **lines** **are** **the** **magnetic** **poles** **(centers** **of** **the** **windings)** **at** **one**
**instant.** **Magnetic** **flux** **passing** **outward** **from** **the** **rotor** **through** **the** **liquid** **metal** **are** **indicated** **by** O.
**(c)** **Rate** **of** **change** **of** **the** **magnetic** **flux** **density** **is** **indicated** **by** O **where** **the** **flux** **density** **is** **changing**
**from** **inward** **to** **outward,** **(d)** **Currents** **induced** **in** **the** **liquid** **metal** **by** **the** **moving** **magnetic** **field,** **(e)**
**Forces** **on** **the** **liquid** **metal** **from** **the** **interaction** **of** **the** **induced** **currents** **and** **the** **magnetic** **field.**

![](images/tmpb2nh9hqp.pdf-10-0.png)

**Figure** **6(a)** **shows** **the** **pump** **rotor** **and** **wind­**
**ing** **slots.** **For** **a** **more** **detailed** **perspective** **of** **the**
## **way an HREMP operates, the liquid-metal annu­**

**lus** **is** **displayed** **in** **Fig.** **6(b)** **as** **if** **it** **were** **unfolded,**
**laid** **flat,** **and** **viewed** **from** **the** **outside** **of** **the**
**pump.** **The** **diagonal** **lines** **are** **the** **centerlines** **of**
**the** **magnetic** **poles** **produced** **during** **one** **instant** **at**
**the** **center** **of** **the** **windings.** **Here,** **magnetic** **fields**
**passing** **outward** **from** **the** **rotor** **through** **the** **liquid**
## **metal are indicated by O. For our simple geome­**

**try,** **Faraday's** **Law** **of** **Induction** **can** **be** **rewritten**
**so** **that** **the** **induced** **voltage** **is** **equal** **to** **the** **integral**
**of** _(dB/dt)_ _■_ _da._ **Clearly,** **induced** **voltage** **around**
**the** **eddy-current** **loop** **is** **maximized** **when** **the**
**quantity** _dB/dt_ **has** **the** **same** **algebraic** **sign** **every­**
**where** **inside** **the** **loop.** **In** **Fig.** **6(c),** _dB/dt_ **is** **shown**
**at** **one** **instant.** **The** **two** **maximum** **eddy-current**
**loops** **meet** **along** **each** **magnetic** **pole** **centerline,**
**as** **shown** **in** **Fig.** **6(d).** **Finally,** **Fig.** **6(e)** **shows** **the**
**direction** **of** **resultant** **forces** **acting** **on** **the** **liquid**
**metal** **from** **the** **interaction** **of** **the** **induced** **currents**
**and** **the** **magnetic** **flux** **density,** **where** **once** **again,**
## F = IP X B.

## **The cylindrical-rotor EM pump is shown in**

**Fig.** **7.** **The** **pump** **operates** **in** **a** **manner** **similar** **to**
## **the HREMP except that the magnetic field coils**

**and** **induced** **current** **loops** **are** **not** **slanted.** **The**
**moving** **(radial)** **magnetic** **field** **induces** **current**
**loops** **that** **are** **axial** **in** **the** **liquid-metal** **pumping**
**region.** **The** **interaction** **between** **the** **magnetic** **field**
**and** **the** **current** **forces** **the** **liquid** **metal** **to** **rotate**
**around** **the** **drive** **axis,** **and** **the** **guide** **vanes** **(helical**
**passages)** **force** **the** **fluid** **to** **follow** **a** **helical** **path**
**through** **the** **duct.**
## **The circle-arc-duct EM pump3 is shown in**

**Fig.** **8.** **The** **rotating** **magnet** **produces** **a** **rotating**
**magnetic** **field,** **which** **induces** **current** **loops** **that**
**cut** **across** **the** **liquid** **at** **the** **magnetic** **poles.** **The**
**liquid** **metal** **is** **forced** **through** **the** **pipe** **due** **to** **the**
**interaction** **between** **the** **magnetic** **field** **and** **the** **in­**
**duced** **currents.**
## **For the EM centrifugal pump3, the rotating**

**field** **coils** **shown** **in** **Fig.** **9** **produce** **a** **moving** **(ax­**
**ial)** **field** **across** **a** **stationary** **duct.** **Induced** **current**
**loops,** **which** **cut** **radially** **across** **the** **duct** **in** **the**
**region** **of** **the** **magnetic** **field,** **interact** **with** **the**

![](images/tmpb2nh9hqp.pdf-11-full.png)

Rotor drive axis

**Figure** **7.** **Cylindrical-rotor** **electromagnetic** **pump.**

![](images/tmpb2nh9hqp.pdf-11-0.png)

![](images/tmpb2nh9hqp.pdf-11-1.png)

![](images/tmpb2nh9hqp.pdf-12-full.png)

![](images/tmpb2nh9hqp.pdf-12-0.png)

field. The liquid metal rotates around the shaft,
and centrifugal force pushes it toward the outlet.

Induction pumps with rotating-magnet struc­
tures have distinct advantages when compared to
other types of EM pumps. They can be designed
to operate at higher efficiencies and with larger
clearances in the gap between windings and ducts
than EM pumps with stationary-magnet struc­
tures (discussed below). They have less tendency
to act as a piping system anchor point than any
other type of EM or mechanical pump due to their
larger clearances. Flow-rate control is achieved
easily and at low cost because the magnetic field
is set up by direct current. An additional benefit
that accrues from the use of direct current is that
ac-power-factor correcting apparatus is not re­
quired. Rotating-magnet induction pumps require
a source of motive power, such as a synchronous
motor or an induction motor to rotate the magnet
structure. High developed pressures (>3000 kPa)
can be obtained with the cylindrical-rotor pump.

Helical-rotor pumps have been successfully
applied to long-term pumping and stirring of mol­
ten aluminum. In such devices, the radial-gap dis­
tances are ~15 cm, much larger than the 1-cm gap
in a typical 10 000-hp induction motor. The gap
distance in the HREMP is taken from the surface
of the rotor to the inner surface of the flux-return
path and, thus, includes the radial thickness of the

refractory walls and of 8 cm of molten aluminum.
The limitations imposed by the manufacturer of
the refractories prevented the rotor diameter from
exceeding 31 cm. The resultant ratio of gap dis­
tance to pole pitch (-~l/3) is an order of magni­
tude larger than the ratios encountered in
synchronous- or induction-motor designs. The
successful experience with aluminum stirring de­
vices affirms our ability to design rotating EM
pumps with magnetic-circuit gaps that are large
compared to the gaps found in conventional
motors.
**Induction** **Pumps** **with** **Stationary** **Magnets.** In
contrast to the pumps discussed thus far, induc­
tion pumps can employ stationary ac windings
that cause a moving magnetic field to induce cur­
rent loops through the liquid metal. Our first ex­
ample of a stationary-magnet design is the single­
phase induction pump3 shown in Fig. 10. Seen in
cross section, the alternating current in the sta­
tionary winding sets up a time-varying magnetic
field that is illustrated at one instant by the
dashed lines. The changing field induces current
loops that are circumferential in the liquid-metal
pumping region. The result is a vertical (or axial)
force on the liquid metal, which flows upward
and toward the outlet.

A flat-linear-induction pump (FLIP) is shown
in Fig. 11. Three-phase alternating current in the

![](images/tmpb2nh9hqp.pdf-13-full.png)

![](images/tmpb2nh9hqp.pdf-13-0.png)

**Figure** **10.** **Single-phase**
## **induction EM pump.3**

**Figure** **11.** **Flat-linear-**
## **induction pump (FLIP).**

stationary windings sets up a traveling magnetic
field (shown at one instant and in the transverse
direction for the isometric projection of Fig. 11).
The moving field induces current loops that travel
along the top and bottom of the rectangular duct
and cut vertically across the liquid metal. Interac­
tion of the magnetic field and the induced current
in the liquid metal forces the liquid through the
duct in the axial direction.

The helical-induction pump is shown in
Fig. 12. Alternating current in the stationary
windings (only one is shown) produces a rotating
magnetic field that cuts radially across the annular
liquid-metal duct to an inner magnetic-field struc­
ture, and then back across the liquid metal to an

exterior magnetic field structure. The rotating
magnetic field induces current loops that are axial
in the pumping region shown in Fig. 12. The in­
duced current interacts with the radial field to
produce a circumferential force on the liquid
metal. The guide vanes force the circulating fluid
in a helical path down the duct. Although not
shown in Fig. 12, reentrant geometry is possible
for the helical-induction pump. Flow at the outlet
is simply redirected so that liquid metal returns
through a hollow inner-magnetic-field structure.

The annular-linear-induction pump (ALIP),
also known as the Einstein-Szilard pump, is illus­
trated in Fig. 13. The ALIP is similar to the FLIP in
that a three-phase current in the stationary

![](images/tmpb2nh9hqp.pdf-13-1.png)

![](images/tmpb2nh9hqp.pdf-14-full.png)

Flow End View

field structure

Field coil

![](images/tmpb2nh9hqp.pdf-14-1.png)

Outlet

**Figure** **12.** **Helical** **induction** **pump.**

windings sets up a traveling magnetic field; how­
ever, the ALIP field is oriented in the radial direc­
tion as it cuts across the liquid metal. At the in­
stant shown in Fig. 13, one magnetic-field line
extends along the outer magnetic-field structure,
crosses the liquid metal radially to the inner
magnetic-field structure (torpedo), and extends
along the torpedo to the point where it recrosses
the liquid metal to the outer magnetic field struc­
ture. The moving magnetic field induces circum­
ferential current loops in the annular liquid metal.
Interaction of the induced current and magnetic
field forces the liquid metal to flow in the axial
direction along the annular duct. For the ALIP, the
liquid metal can enter or exit from the same end of
the pump by using the center of a hollow torpedo
for flow return (reentrant geometry).

Induction pumps with stationary ac windings
are more efficient than conduction pumps for
medium-pressure applications. The helical

![](images/tmpb2nh9hqp.pdf-14-0.png)

F (circumferential)

induction pump can be designed to develop high
pressures (~2 MPa), but flow rates of this pump
are limited to ~0.03 m3/s. For flow-rate control,
all induction pumps with stationary ac windings
require an ac source with variable frequency, vari­
able voltage, or both. In addition, either static
capacitors or an overexcited-synchronous motor
are required for power-factor correction. The sta­
tionary windings must also be designed to reduce
back pressures caused by space harmonics of the
traveling magnetic field. For induction pumps,
the magnetizing current in the stationary
windings constitutes nearly 70% of the total wind­
ing current; consequently, close clearances are re­
quired to minimize the magnetizing current and,
hence, to minimize the required power-factor cor­
rection equipment. Cooling of the windings is also
made difficult by their proximity to the hightemperature liquid-metal pump duct.

![](images/tmpb2nh9hqp.pdf-15-full.png)

Torpedo
(inner magnetic-field structure)

Outer magnetic-field

End view

Flow

I (circumferential)

![](images/tmpb2nh9hqp.pdf-15-0.png)

![](images/tmpb2nh9hqp.pdf-15-1.png)
## **Figure 13. Annular-linear-induction pump (ALIP).**

Comparison of HREMP and ALIP
Geometries

Of the ten EM pump configurations we have
illustrated, only two, the HREMP and the ALIP,
appear to have the potential for cost-effective
scaleup to HYLIFE design requirements. Before
we describe our design procedure in detail for the
HREMP, we first make several preliminary com­
parisons between HREMP and ALIP geometries.
Specifically, we address four parameters that can
be examined on the basis of current designs: the
relative size of existing pumps, flow-rate control,
winding effectiveness, and power-factor correc­
tion. A more detailed comparison will only be
possible when an ALIP is designed for the flowrate and pressure-rise requirements of HYLIFE.

**Largest** **Pumps** **Built** **to** **Date**

At present, the largest HREMP is a sodium
pump designed to operate at 370 °C with a peak
flow rate of 0.13 m3/s (2000 gpm) at a pressure rise
of 260 kPa (38 psi). In 1962, this pump demon­
strated a peak efficiency of 26% at its best operat­
ing point.5 The largest ALIP built to date is a so­
dium pump designed to operate at 540 °C with a
flow rate of 0.91 m3/s (14 500 gpm) and a pressure
rise of 1.26 MPa (183 psi). This as-yet-untested
pump, designed for use with an LMFBR, is pre­
dicted to have an efficiency of 46% (Ref. 6). Both
pumps have flow rates that are far too small for
use in a reactor such as HYLIFE, which requires
pumping of 500 °C Li at a flow rate of 7.8 m3/s per
pump (124 000 gpm) and a pressure rise of 83.6
kPa (12.1 psi).

![](images/tmpb2nh9hqp.pdf-16-full.png)

**Flow-Rate** **Control**

The flow rate of an HREMP is easily con­
trolled by simply adjusting the direct current sup­
plied to the rotor windings. If, in addition, a
variable-speed drive is used, an HREMP can oper­
ate at a wide range of flow rates with little loss of
efficiency. When a fixed-speed drive is used, a
gear-speed reduction unit between the HREMP
and the drive motor sets the speed of the drive
![](images/page_016_eq_0.png)
motor at the level that produces the highest pump
efficiency for the anticipated flow rate. Once a
fixed-speed drive is selected, the flow rate can still
be adjusted over a limited range with little loss of
efficiency by varying the winding current.

The ALIP flow rate can be controlled by vary­
ing the voltage, the frequency, or both. However,
the ratio of voltage to frequency has an optimum
value for highest pump efficiency, and both volt­
age and frequency must be varied for flow control
if the pump efficiency is to remain high. Thus,
flow control for the ALIP requires either silicon
controlled rectifiers (SCR) or rotating machinery,
such as a motor generator. Both SCRs and motor
generators are more bulky and expensive than the
HREMP winding-current control circuit and gearreduction unit.

**Winding** **Effectiveness**

The pressure that can be produced by any
EM pump is a function of the parameters from
Eq. (1), one of which is the magnetic flux density
in the liquid metal. The flux density is propor­
![](images/page_016_eq_1.png)
tional to the magnetomotive force (mmf) pro­
duced by the electrical currents in the magnet
windings. The effectiveness of the windings in
producing the mmf is important because all EM
pumps have much wider magnetic-circuit gaps
than standard motors and generators, and the
magnetizing current required to set up the mag­
netic flux density in the gaps causes severe heat­
ing problems in the windings.

The winding of an ALIP consists of many
coils spaced along the pump duct so that they pro­
duce the traveling magnetic field that is required
to operate the pump. As a consequence of the
winding distribution, the vector sum of the mmfs
causing the flux to penetrate the liquid metal is
less than the sum of the mmfs of the individual
coils.

The winding effectiveness of a linear EM
pump with three-phase windings (such as the
ALIP or FLIP) is given7 by

where Fm is the effective maximum mmf per pole,
_Nse_ is the number of effective turns per phase, _N_
is the number of poles, and _Is_ is the rms value of
the winding current.

In contrast, the magnetomotive forces of the
coils in an HREMP act in the same direction and
on the same geometric axis. For an HREMP, a cor­
responding expression for the mmf per pole is

3 | 1 _1_ ampere-turns per pole. (4)

where is the number of rotor turns per pole,

and _I_ is the dc winding current, which has the
same value as _Is._

The resultant mmf per pole is larger for an
HREMP than for an ALIP with the same number
of ampere-turns; that is, the winding effectiveness
is higher for an HREMP. Specifically, a compari­
son of Eqs. (3) and (4) shows that the mmf of the
HREMP is 1.4 times that of the ALIP on a normal­
ized basis. Thus, an HREMP can be designed to
produce a higher pump head and higher effi­
ciency and, at the same time, be smaller in size
and weight than an ALIP designed for the same
flow rate.

**Power-Factor** **Correction**

As previously mentioned, an HREMP does
not require any equipment for correcting the
power factor because the magnetic field penetrat­
ing the liquid metal is set up with direct current.
To estimate the power-factor-correction equip­
ment required for an ALIP, we must calculate the
volt-amperes required to set up the magnetic flux
penetrating the liquid metal, i.e., the volt-amperes
consumed by the gap through which the liquid
metal passes.

We have calculated the reactive power for
two considerably different ALIP geometries with
the head and flow rate of each of the 11 large
HYLIFE pumps. In the worst case, a 660-MVAR
(megavolt-amperes reactive) three-phase capac­
itor bank would be required to correct the power
factor to 80%. Although reactive power does not
affect the efficiency, its correction equipment
would add about $2.6 million to the pump cost in
the worst case. In the best case, no power-factor
correction equipment would be required. How­
ever, the pump diameter could become excessive,

= **2.11**

N,se

![](images/page_016_eq_2.png)
Is ampere-turns per pole, (3)
N

![](images/tmpb2nh9hqp.pdf-17-full.png)

and the power supply frequency might be too low
to be supplied efficiently and inexpensively.

Our rough ALIP power-factor calculations
used a 6-m/s (20-ft/s) flow velocity, as did the

HREMP design presented later. A faster flow ve­
locity would significantly improve both pump de­
signs if materials problems such as duct erosion
were overcome.

## **Design Procedure for the HREMP**

The goals of our design procedure are to
achieve the highest possible efficiency and reli­
ability with minimum capital cost. Minimizing
capital cost requires minimization of weight, floor
space, and auxiliary systems. In addition, we
would like to avoid lengthy and expensive devel­
opment programs by using proven materials and
components, where possible.

In this section, we develop the HREMP de­
sign procedure. First, the two types of rotors are
compared, and a choice is made. The next two
subsections develop the design equations for nor­
mally conducting windings and for super­
conducting windings. Then, the heat load on the
cryogenic winding is calculated. Finally, a flowrate control system is described.

Rotor Construction

Two alternative designs are possible for an
HREMP rotor: the nonsalient-pole and the
salient-pole rotor. These designs can be compared
on the basis of ease of winding-heat removal,
winding efficiency, and manufacturing cost.

For a nonsalient-pole rotor, the windings are
placed within multiple slots located in the rotor.
Thus, the winding effectiveness is less than that
for a rotor with consolidated windings. The
nonsalient-pole rotor shown in Fig. 14 was used in
an HREMP designed to pump 730°C aluminum.
The windings in each slot were split so that cool­
ing air could circulate between the two winding
halves. The air flowed from the hollow rotor shaft

![](images/tmpb2nh9hqp.pdf-17-0.png)

![](images/tmpb2nh9hqp.pdf-18-full.png)

radially outward to the small channels located at
the bottom of the slots and then into the spaces
between the split windings. In this pump, the
winding temperature was sucessfully held below
the specified upper limit of 190°C.

For a salient-pole rotor, the windings are lo­
cated on the rotor surface, and the pole shoes are
attached to the rotor in the spaces between the
windings. The salient-pole rotor shown in Fig. 15
was used in the 1962 HREMP5 to pump 370°C
sodium. Since the consolidated salient-pole
windings are thicker, careful design attention was
given to heat removal. Cooling was accomplished
with fiberglass blade spacers to provide air pas­
sages between the windings and the rotor core.
The pole shoes were then placed in the winding
loops and attached to the rotor core.

To keep the load on the rotor heat-removal
system to the absolute minimum (the winding _12R_
loss), thermal insulation must be attached to the
duct wall facing the rotor. Heat flowing through
the insulation is removed by blowing air axially
between the rotor and the duct wall insulation. If
the air velocity is too low, the surface temperature
of the insulation will overheat the rotor winding
due to radiative heat transfer. Conversely, if the

driving head of the blower in the air circulating
system is too high, portions of the thermal insula­
tion can be torn loose from the duct wall. Because
the latter problem was encountered in the
HREMP used to pump molten aluminum (Fig. 14),
the insulation was encased between two 1/32-in.thick stainless-steel cylinders, which were fas­
tened to the inner duct wall.

The third consideration in the choice of rotor
design is manufacturing cost. (The other consider­
ations are winding effectiveness and heat re­
moval.) The manufacturing cost of slotting a solid
steel forging to produce a nonsalient-pole rotor
must be weighed against the cost of manufactur­
ing the windings for a salient-pole rotor. For the
HREMP design procedure described below, we
have used a salient-pole rotor with consolidated
windings.

Normally Conducting Winding

The basic equations for designing our
HREMP were derived from Rudenberg's8 treat­
ment of eddy-current brakes for motor testing.
The absolute cgs electromagnetic system, in

![](images/tmpb2nh9hqp.pdf-18-0.png)

![](images/tmpb2nh9hqp.pdf-19-full.png)

which the permeability of free space is unity, was
used in the original article and in a later analysis5
as well. In this article, the preferred SI units are
used.

The dimensions and operating parameters
computed by the pump design procedure are
bounded by the following fixed-input data:

  - Liquid-metal volumetric flow rate,
Q (m3/s).

  - Liquid-metal temperature (500 °C).

  - Liquid-metal velocity within the pump
annulus, _vf_ (m/s).

![](images/page_019_eq_0.png)
  - Pressure rise developed by the pump,
_P_ (Pa).
P is assumed to be 110% of the pressure rise re­
quired by the system; i.e., 10% of the pressure is
assumed to be lost within the pump.

The width of the liquid-metal annular duct,
shown as Dj in Fig. 16, is calculated by assuming
values for the duct wall thickness D2 and the
clearances D3 and D4. The final value of D2 is ob­
tained from stress calculations after the pump di­
mensions have been tentatively determined. The
clearance dimensions D3 and D4 are based on ex­
perience. Small values reduce both the magnetic
flux leakage across the gap and the winding cur­

Pump duct

![](images/page_019_eq_1.png)

rent. Large values make the pump act as less of an
anchor point on the piping system.

To calculate Dj, we first write the flow rate in
terms of velocity, duct width, and duct circumfer­
ence so that

_Q_ = NDgDjff cos, (5)

where N is the number of poles on the rotor, D6 is
the pole pitch (see Fig. 17), _vf_ cos 0, is the axial
component of the fluid velocity, and 03 is the helix
angle of the eddy-current path (see Fig. 18). The
optimum value for _61_ has been experimentally de­
termined to be 45° (Ref. 9).

Next, a dimensionless term, _Ku_ is introduced,

where D5 = Dx + 2D2 + D3 + D4 is the total gap
length between the rotor steel and flux return
path (Fig. 16). This ratio of pole pitch to gap
length is also important in the design of magnetic
circuits in motors, generators, and other magnetic
devices. The ratio establishes a lower limit on the
size and weight of electromechanical devices. If

°4

°5

°8
_°9_

_DV_

_DV_

CL

![](images/tmpb2nh9hqp.pdf-19-1.png)

![](images/tmpb2nh9hqp.pdf-19-0.png)
## **Figure 16. Longitudinal cross section of an HREMP. The geometric**

**variables** **are** **shown.**

the pole pitch is made too small in relation to the gap length, most of the flux produced in the magnetic circuit will consist of leakage flux, which does not traverse the gap. Our design procedure investigates the result of varying $K_2$ in the 3 to 20 range. Using Eqs. (5) and (6) and the definition of $D_5$:

$$D_3 = \frac{1}{2}\left[-(2D_5 + D_3 + D_4) + \sqrt{(2D_5 + D_3 + D_4)^2 - \frac{4Q}{NK_1 \cos\theta_1}}\right] \tag{7}$$

A second dimensionless ratio, $K_2$, is used to define the ratio of rotor length to pole pitch,

$$K_2 = \frac{D_{20}}{D_6} \tag{8}$$

A good first estimate for $K_2$ is 1.0. Once again, consider Fig. 6 and Faraday's Law of Induction

$$\oint \mathbf{E} \cdot d\boldsymbol{\ell} = -\frac{d}{dt} \int_B \mathbf{B} \cdot d\mathbf{a} \tag{9}$$

![](images/page_020_eq_0.png)
The eddy-current path $d\ell$ will be that for which both sides of Eq. (9) are maximized.[?] Figure 6(c) shows $\partial B/\partial t$ at one instant. The eddy-current paths surround each area in which $\partial B/\partial t$ has the same algebraic sign. The two eddy-current paths shown in Fig. 6(d) are parallelograms that surround each area in which $\partial B/\partial t$ has the same algebraic sign. When the rotor is too long compared to the pole pitch ($K_2 > 1.0$), the eddy-current

![](images/page_020_eq_1.png)
[Figure 17: Horizontal cross section of an HREMP. The pole pitch is shown for a two-pole rotor.]

[Figure 18: Helix angle $\theta_1$ of the eddy-current paths in the center of the liquid-metal duct. A developed view of an annulus for a two-pole rotor is shown.]
![](images/page_020_eq_2.png)

![](images/tmpb2nh9hqp.pdf-21-full.png)

paths will have a higher resistance, and the pump
head will be reduced. When the pump is too short
_(K2_ « 1.0), the region where the current path
turns at an angle sharper than 90° becomes im­
portant. Since the current actually turns smoothly,
this part of the current path is not as sharply
slanted, and the resultant force has a smaller axial
component. Our design procedure investigates the
result of varying _K2_ in the range from 0.5 to 2.0.

It is possible to force the liquid metal to flow
in helical paths by constructing the pump duct
with guide vanes in the annulus so that the value
of _K2_ could be much less than 1. However, when
the liquid metal is forced to change its direction
by being driven circumferentially against a guide
vane, a loss in performance will result because of
turbulence and because of eddy-current braking
due to a change of liquid-metal direction in the
presence of the magnetic field of the rotor.

A third parameter, the field-to-fluid-velocity
ratio (fC3 = u2/yi), was varied in the design proce­
dure. Here, _v2_ indicates the circumferential field
velocity, and zq = _vt_ sin _9X_ is the circumferential
component of the fluid velocity. When _K3_ _=_ 1.0,
the flow rate is said to be synchronous; the flow
rate is maximum, but the developed pressure is
zero. When _K3_ = oo, there is no flow, and the
developed pressure is called the shutoff pressure.

Our first estimate of _K3_ was obtained from
the head-flow curve shown in Fig. 19. Operating
at the top of the curve minimizes the rotor current
and consequent heat-removal. Mathematically,
this point is found by setting

**(** 10 **)**

This estimate of fC3 works well for high-head
pumps, but for the low-head HYLIFE reactor, effi­
ciency and pump weight can be improved by con­
sidering other values of _K3._ In our design proce­
dure, _K3_ was varied between 1.05 and 1.25.

For a given set of the variable parameters, _Kj,_
_K2,_ and _K3,_ we can complete the pump design.
Equations (5) through (7) used the total-gaplength definition (D5 = D, + 2D2 + D3 + D4) and
fCj to find Dj. The resulting _D1_ can be combined
with the previously determined values of D2, D3,
![](images/page_021_eq_0.png)
and _D4_ to find the total gap D5 and the pole pitch
(D6 = _KjD5)._ The annulus mean diameter (D8 =
_D6N/tt),_ and the rotor diameter (D9 = Dg - Dj 2D2 - 2D3) are easily found. The rotor length is
D10 = _K2D6,_ and the developed length of the pole
in the liquid metal is D12 = D10/sin 0j. We have,
thus, set most of the dimensions of the pump.

![](images/tmpb2nh9hqp.pdf-21-0.png)
## **Figure 19. Head-flow curve for an HREMP.**

The rotational speed of the pump has also
been set because we have specified the fluid ve­
locity _Vf,_ the helix angle _dv_ and the field-to-fluidvelocity ratio _K3._ That is, the field velocity is

_v2_ _=_ _K3Vf_ _=_ _K3Vf_ sin . (11)

To produce _v2,_ the rotor must spin at _2-kv2/Di3N_
rad/s.

![](images/page_021_eq_1.png)
Next, we calculate the peak magnetic flux
density in the liquid-metal. The resistance of the
eddy-current path in the liquid metal for one
pole is

_P\_ j /^12

D, sin 0,/ y D6 D12,

![](images/page_021_eq_2.png)

**(12)**

![](images/page_021_eq_3.png)

where _px_ _=_ 3.5 X 10 7 fl-m is the electrical resis­
tivity of lithium at 500°C. The inductive reactance
of the same eddy-current path is

X] = 4 X 10~7(u2 - Uj) —^ . (13)
_U5_

The peak magnetic flux density is

![](images/page_021_eq_4.png)

(PQ/N) Z?
## **B =**

_Vf(v2_ _-_ u,) _D2wRf_

1/2

(14)

where Z3 = _(R\_ _+_ Xj)172 is the eddy-current-path
impedance.

The detailed derivation of these equations is
available in Ref. 5 and is not reproduced here due
to its length; however, Eq. (14) can be considered
on intuitive grounds. The eddy current induced is
_I_ = _V/Z,_ where _V_ = _BLv,_ and the power is W =
## I2R. Thus, B = [WZ2/{v2L2R)]U2. In Eq. (14), the

power is _PQ/N,_ the velocity squared is _(v2_ _—_ _v{)vx,_
and the length L is D10.

The voltage induced in the liquid-metal along one pole-face projection is

$$V_1 = B(\varepsilon_2 - \varepsilon_1)D_{10} \quad . \tag{15}$$

The eddy current induced in the liquid metal along one pole-face projection is $V_1/Z_e$. This current has a demagnetizing effect, which must be overcome by $I_2$ ampere turns on the rotor.

![](images/page_022_eq_0.png)
$$I_2 = \left(\frac{V_1}{Z_e}\right)\left(\frac{X_e}{Z_e}\right) = \frac{V_1 X_e}{2Z_e^2} \quad , \tag{16}$$

![](images/page_022_eq_1.png)
where $V_1/Z_e$ is the current per pole in each eddy-current loop and $X_e/(2Z_e) = \sin\theta$ is the power-factor phase angle of the eddy-current loop. Only 50% of the current is used because the induced current splits into two branches.

Equation (16) also shows that Fig. 6 was over-simplified. As shown, Fig. 6 has eddy-current paths with zero inductance and no net demagnetization of the rotor magnetic fields (one-half of the rotor fields are reinforced and one-half are degraded). If the eddy-current loop has any inductive reactance, the eddy currents lag behind the positions shown by the power-factor phase angle.

![](images/page_022_eq_2.png)
A similar analysis holds for the eddy-current loops per pole in the inner and outer annulus walls such that

$$R_e = \left(\frac{\rho_e}{D_2 \sin\theta_1}\right)\left(\frac{D_{13}}{D_s} - \frac{D_s}{D_s}\right) \tag{17}$$

$$X_2 = 4 \times 10^{-7} \varepsilon_3 \left(\frac{D_{13}}{D_s}\right) \quad , \tag{18}$$

![](images/page_022_eq_3.png)
and

$$V_2 = B\varepsilon_3 D_{13} \quad , \tag{19}$$

![](images/page_022_eq_4.png)
where $\rho_e = 9.16 \times 10^{-7}\ \Omega\ \text{m}$ is the resistivity of type 304 stainless steel at 500°C and Eqs. (17) through (19) refer to either wall. The total ampere turns per pole required to overcome the demagnetizing effect of the eddy-current loops in both walls is

$$I_2 = \frac{V_2 X_2}{Z_2^2} \quad . \tag{20}$$

The gap $D_s$ also requires $I_3$ ampere turns to overcome its reluctance, where

![](images/page_022_eq_5.png)
$$I_3 = 7.96 \times 10^5\ BD_s \quad . \tag{21}$$

![](images/page_022_eq_6.png)
The total ampere turns required per pole is then

$$I_a = I_1 + I_2 + I_3 \quad . \tag{22}$$

![](images/page_022_eq_7.png)
The design is completed by specifying the rotor winding geometry. If a salient pole geometry is used with two poles, then the rotor cross section is as shown in Fig. 20. The pole-shoe arc length is $D_{11} = 0.8\pi D_r/2$ if 60% of the rotor is assumed to be shoe. The half angle subtended by the shoe is $\phi = D_{11}/D_r$ and the shoe depth is $D_{12} = (1 - \cos\phi)D_r/2$. The winding arc length is $D_{13} = \pi D_r/2 - D_{11}/2$. The total winding width is $D_{14} = D_{13} - 2D_{12}$ and the mean winding width is $D_{14}/2$. The final rotor dimension, the pole waist thickness $D_{16}$, requires calculation of the flux through the pole. The flux through the liquid metal is

$$\phi_1 = BD_2 D_{10} \quad . \tag{23}$$

The flux leaking from pole shoe to pole shoe by traversing the clearance between the rotor and liquid metal annulus is

$$\phi_2 = 5.1 \times 10^{-7} \left[\frac{D_{10}^2 D_{11}}{D_{12} \sin^2\theta_1}\right] \quad . \tag{24}$$

[Figure 20: Cross section of a salient pole rotor with two poles.]
![](images/page_022_eq_8.png)
![](images/page_022_eq_9.png)

where $\beta_s$ is the helix angle of the pole centerline at the rotor edge. As shown in Fig. 21, the angle at the rotor is always larger than the angle in the liquid metal.

$$\beta_s = \tan^{-1}\left[\left(\frac{D_R}{D_s}\right)\tan\beta_i\right] \tag{25}$$

The flux leaking from shoe to shoe by going through the winding is

$$\phi_3 = 5.1 \times 10^{-6} \left[\frac{I_p D_{12}}{\sin^2\beta_s}\right] \tag{26}$$

The flux leaking from pole to pole by going over the top of the rotor and windings is

![](images/page_023_eq_0.png)
$$\phi_4 = 7.5 \times 10^{-8} I_p D_{14} \log_{10}\left(1 + \frac{\pi D_{14}}{2D_{15}}\right) \tag{27}$$

Finally, the flux leaking from pole to pole over the top of the rotor and rotor waist is

$$\phi_5 = 3.74 \times 10^{-8} I_p D_{14} \log_{10}\left(1 + \frac{\pi D_{14}}{D_{14}}\right) \tag{28}$$

![](images/page_023_eq_1.png)
The equations for the leakage flux are taken from Ref. 11. The total flux is $\phi_m = \phi_1 + \phi_2 + \phi_3 + \phi_4 + \phi_5$. Then, the pole waist width is

$$D_{18} = \frac{\phi_m}{1.39 D_{10}} \tag{29}$$

where the maximum flux density is 1.39 T. The same maximum flux density fixes the thickness of the flux-return path

![](images/page_023_eq_2.png)
$$D_{19} = \frac{1}{2}\left[\frac{\phi_m}{(1.39)D_{10}}\right] \tag{30}$$

where the factor of one-half accounts for the clockwise and counterclockwise flux-return loops.

The total pump diameter is

![](images/page_023_eq_3.png)
$$D_{20} = D_9 + D_1 + 2(D_2 + D_3 + D_{19}) \tag{31}$$

![](images/page_023_eq_4.png)
For a two-pole rotor, the rotor-winding cross section area per pole is

$$A_1 = \frac{1}{4}\left[\frac{D_4^2}{4}(\pi - 2\delta + \sin 2\delta) - D_{16}D_{10}\right] \tag{32}$$

The rotor-steel cross section area is

[Figure 21: Helix angle $\beta_s$ of the pole centerline at the rotor surface.]

![](images/page_023_eq_5.png)
$$A_2 = \frac{\pi D_4^2}{4} - 2A_1 \tag{33}$$

![](images/page_023_eq_6.png)
The masses of the various components are

Rotor-steel mass
$$M_1 = 7750 D_{20} A_2 \tag{34}$$

![](images/page_023_eq_7.png)
Copper-winding mass
$$M_2 = 8900(2A_1)(D_4 + D_{10}) \tag{35}$$

![](images/page_023_eq_8.png)
Flux-return-path mass
$$M_3 = 7750(D_{20}D_{19})K(D_{20} - D_{10}) \tag{36}$$

![](images/page_023_eq_9.png)
Total mass
$$M_4 = M_1 + M_2 + M_3 \tag{37}$$

![](images/page_023_eq_10.png)
The power input to the pump is

![](images/page_023_eq_11.png)
$$W = (PQ) + \left[\frac{PQ(D_2 + D_{12} - D_3)}{r_1}\right] + 2N\left(\frac{V_t}{r_s}\right)^2 R_2$$

![](images/page_023_eq_12.png)
$$+ 0.168\, M_1 + (N I_4)^2 R_1 \tag{38}$$
![](images/page_023_eq_13.png)
![](images/page_023_eq_14.png)

where

$PQ$ is the gross hydraulic power added to the liquid metal (10% is lost to friction within the pump);

$PQ(\nu_2 - \nu_1)/\nu_2$ is the liquid-metal slip loss due to the difference between the circumferential fluid and field velocities. The slip loss is also the liquid-metal $I^2R$ loss, numerically equal to $N(\bar{V}/Z_t)^2R_t$. Calculation of this loss from the two independent formulas is a check on the design procedure.

$2N(\bar{V}/Z_t)^2R_2$ is the total $I^2R$ loss in the duct walls. This is also a slip loss, but with $\nu_1 = 0$ and $Q = 0$, the slip formula would have to be calculated in the limit rather than directly.

$0.168 M_2$ is the combined eddy-current and hysteresis loss in the flux-return path.

$(N_t/t)^2R_r$ is the $I^2R$ loss in the rotor windings. The factor of $N = 2$ accounts for the two poles on the rotor. Each pole is assumed to be a single-turn winding (ampere turns = amperes).

The winding resistance, $R_2$, in Eq. (38) is

![](images/page_024_eq_0.png)
$$R_2 = 8900\rho_c \left( D_3 + \frac{D_{10}}{2} \right) \frac{t_2}{4} (M_2/2) \quad , \tag{39}$$

where $\rho_c = 2.8 \times 10^{-8}\ \Omega \cdot m$ is the resistivity of copper at 250°C, the expected peak winding temperature. The winding mass is reduced by one half due to a 50% copper-packing fraction in the winding.

The pump efficiency $\eta$ is the ratio of the net hydraulic power to the total input power, expressed as

$$\eta = \left(\frac{F_2}{1.1}\right) \frac{Q}{W} \quad . \tag{40}$$

## Superconducting Winding

Our design procedure for an HREMP with superconducting windings is nearly the same as that for normally conducting windings. The only changes are as follows:

- The steel mass in the rotor is ignored since it will be an open structure rather than a monolithic rotor. The winding mass is calculated using copper density and assuming that the winding occupies 43% of the rotor cross-sectional area.

![](images/page_024_eq_1.png)
- The ampere turns required to overcome the reluctance due to the magnetic-circuit gap are changed because the gap includes open space within the rotor as well as space between the rotor and the flux-return path [cf Eq. (21)] so that

$$I_r = 7.96 \times 10^5 B \left( D_3 + \frac{t_2}{2} \right) \quad . \tag{41}$$

- The pole winding geometry is not calculated. Hence, $\delta$, $R_2$, $D_{12}$, $D_{13}$, $D_{14}$, and $D_{15}$ may be ignored.

- No magnetic flux leakage is considered. Thus, $\alpha_{fs}$ and $\alpha_2$ are set to zero.

- The resistivity of the windings is set to zero. Thus, there is no $I^2R$ loss in the windings.

![](images/page_024_eq_2.png)
## Cryogenic Cooling Power for a Superconducting Winding

Typical cryogenic cooling systems operate at efficiencies in the 0.2% range or even higher. If a relatively small fraction of the pump losses must be removed as heat by the cryogenic system, the system efficiency can be significantly reduced, as shown in Fig. 22. For example, consider our preliminary HYLIFE design point (82 kPa, 8.08 m³/s). The gross output hydraulic power is 667 kW, and the pump is assumed to be 60% efficient. If only 1% of the losses (4.4 kW) are removed by a 0.1%-efficient cryogenic system, 4.4 MW is required by the cryogenic system in addition to the 1.11 MW (667 kW/0.6) required by the pump. Thus, the cryogenic system penalty is very large. From Fig. 22, for a 60%-efficient pump, the heat load on the cryogenic system should be limited to ~0.01% of the pump losses, which is about 44 W for the HYLIFE pump. Thus, heat flow from the ~500°C liquid metal to the cryogenic rotor must be shown to be smaller than 30–40 W.

A two-dimensional (radial, axial) finite-difference heat-transfer calculation used 510°C lithium in the annulus. The radial heat transfer went through a 12.7-mm steel annulus wall, a 6.35-mm Fiberfrax (Carborundum Co.) insulation layer, a 12.7-mm gap filled with argon, a 6.35-mm Fiberfrax insulation layer on with [?] Dewar

![](images/tmpb2nh9hqp.pdf-25-full.png)

![](images/tmpb2nh9hqp.pdf-25-0.png)

Fraction of pump losses in
superconducting coil (%)

**Figure** **22.** **Pump** **system** **efficiency** **vs** **cryo­**
## **genic system load for a superconducting EM**

**pump.**

outer wall, and a 12.7-mm Dewar vacuum gap to
the Dewar inner wall, which was assumed to be at
4.3 K. Four cases were run:

  - The static argon in the gap was assumed
to support only conduction heat transfer (no natu­
ral convection). The thermal emissivity of the
Dewar walls was set at 0.55 (unpolished stainless
steel). The result was an unacceptable 4.36 kW
heat load on the cryogenic system.

  - The argon in the gap was circulated at
30.6 kg/s, and forced-convection heat transfer was
used to remove heat in the axially flowing argon
before it could be radially transferred to the cryo­
genic rotor. With the same unpolished stainless
steel Dewar walls, the cryogenic system heat load
was reduced to 850 W, still unacceptably high.

  - Static argon in the gap was combined
with a Dewar containing five radiation shields
with polished stainless steel (emissivity = 0.074).
The cryogenic system heat load was reduced to
580 W, still unacceptably high.

  - The forced convection argon in the gap
was combined with the radiation shields in the
Dewar to produce a cryogenic heat load of only
21 W, an acceptable value.

Further reduction in either the insulation
thickness or the cryogenic heat load could be ob­
tained by replacing the Fiberfrax insulation (ther­
mal conductivity = 3.45 X 10 2 W/ffi'K) with a
superinsulation such as Linde SI-4 (4.33 X 10-5
W/m-K).

Rotor-Winding Power Supply and
Current Control

The rotor-winding power supply for an
HREMP must furnish direct current that is as
nearly pure as possible. As can be seen from Fig.
6(c), alternating current in the rotor would change
the distribution of _dB/dt,_ and the eddy-current
paths would have a net demagnetizing effect on
the applied magnetic field. Thus, the Lorentz
force, pump head, and pump efficiency would all
be reduced.

A typical rotor-winding power supply for an
HREMP is shown schematically in Fig. 23. A

Three-phase distribution system

) [Circuit] [breaker]

Variable
three-phase
autotransformer

Variable ac output

## /WW Three-phase

Flowcontrol
signal

![](images/tmpb2nh9hqp.pdf-25-1.png)

![](images/tmpb2nh9hqp.pdf-26-full.png)

three-phase full-wave bridge rectifier provides a
dc output voltage with a 4% ripple. The induc­
tance of the rotor winding tends to produce a
smoothing or filter choke effect that further de­
creases the voltage ripple to an acceptable level.

The most satisfactory method for controlling
the rotor-winding current is by adjusting the ac
voltage to the desired value between zero and the
line value. We use a variable autotransformer con­
sisting of a laminated steel stator on which is
wound the regulating or series winding and a
laminated steel rotor on which is wound the excit­
ing or shunt winding. The construction is similar
to an electric motor except that the rotor does not
spin; instead, it is turned to the new desired posi­
tion when the flow rate must be changed.12 The
output voltage is a sine wave with the same fre­
quency as the incoming line voltage.

Since the three-phase rectifier operates at
considerably lower voltage than the incoming line
voltage, the output voltage of the variable trans­

## **Design of an HREMP for**

Validation of the Design Procedure

Before we applied the design procedure to
specify a pump that would meet the HYLIFE de­
sign requirements, we tested the validity of our
equations on an experimental HREMP. The unit
selected was a sodium HREMP built in 1962 by
Atomics International in Canoga Park, Calif.5 This
HREMP pumped 0.13 m3/s (2000 gpm) at a head
of 260 kPa (38 psi). Figure 24 shows the pressure
and efficiency of the sodium pump as a function
of flow rate. The curves based on our calculations
were generated from the design procedure by set­
ting the dimensions and winding current to the
test values. The test data points were taken with
pressure gauges in the flow circuit; hence, the
pressure and efficiency losses in entrance and exit
volutes to the pump resulted in test data values
lower than would have been measured inside the
pump.

Figure 24 shows that the design procedure
underpredicted pump performance. In fact,
underprediction was anticipated for two reasons.
First, whenever there was uncertainty in the the
design procedure, conservative choices were
made. Second, the detailed derivation of the de­
sign equations was based on a magnetic flux that

former is stepped down by a second transformer.
The three-phase full-wave bridge rectifier then
converts the ac to dc with a ripple of less than 4%.
If a stepdown transformer and thyristor were used
in place of the described system, the nominally dc
rotor-winding voltage would contain the steep
pulses that are characteristic of thyristor output. A
steep-sided pulse represents high frequency; the
hysteresis loss in the magnetic steel varies as the
first power of the frequency, and the eddy-current
loss varies as the square of the frequency. Thus, in
addition to the demagnetizing effect of the liquidmetal eddy-current loops, the steep pulses would
increase the hysteresis and eddy-current losses in
the steel body of the rotor and in the flux-return
path. Unfortunately, solid-state technology has
yet to achieve a "soft" turn-on thyristor. There­
fore, the variable autotransformer-stepdown
transformer-rectifier system is the preferred
method for rotor-winding-current and flow con­
trol in an HREMR

## **the HYLIFE ICE Reactor**

varies sinusoidally in both the axial and circum­
ferential directions. In reality, the HREMP mag­
netic flux approximates a square wave (step func­
tion) in both directions; thus, the actual pumping
force is higher than predictions based upon the
design equations. The success of our design proce­
dure in reproducing the 1962 sodium pump data
gives us confidence that the design procedure is,
indeed, valid.

The HYLIFE Design Point

The current HYLIFE ICF reactor design13 re­
quires 11 recirculation pumps with flow rates of
7.8 m3/s (124 000 gpm) and 2 heat-transfer-loop
pumps with flow rates of 4.9 m3/s (78 000 gpm).
All 13 pumps will have a lithium head of 17.6 m
(83.6 kPa or 12.1 psi). The values selected in gen­
erating our preliminary design point were based
upon a flow rate of 8.08 m3/s (128 000 gpm) at a
head of 82.5 kPa (12.0 psi). Our values, chosen
prior to the update of the HREMP design, are
nearly the same as those required for the 11 large
HYLIFE pumps and can be easily modified to con­
form to final design requirements.

Results of the design tradeoffs are shown in
Table 2 and in Figs. 25 and 26. Table 2 provides

[Figure 24: Pressure and efficiency vs flow rate for the 1962 sodium HREMP.]

values for the following variables in both the normally conducting and superconducting windings:

- Flow and pressure specifications.
- The three dimensionless variables $k_1$, $k_2$, and $k_3$.
- Pump dimensions.
- Velocities, pole angles, and magnetic-flux density.
- Eddy currents in the lithium and duct walls.
- Winding ampere turns required.
- Magnetic flux lost in various paths.
- Rotor design.
- Masses of the pump components.
- Power flow.
- Pump efficiency.

The pump efficiency does not include power supplied to the drive motor that turns the rotor or the power used to cool a cryogenic (superconducting) rotor because these values are expected to be negligible compared to the winding and wall $I^2R$ losses and the slip loss.

Figures 24 and 25 show the pressure and efficiency of both designs as a function of flow rate. The HREMP with a normally conducting winding, shown in Fig. 25, operates near the peak of the pressure curve, and the shutoff pressure (the pressure at no flow) is insufficient to overcome the HYLIFE gravity head (which is 91% of the head at the design flow rate).

In contrast, although the HREMP with a superconducting winding also operates at a pressure near the peak of the curve, the shutoff pressure is higher than the HYLIFE gravity head, and startup will not require additional winding current or reduced rotor velocity. At startup, the flux density in the flux return path is 1.39 T, the same value as at the design flow, and comfortably below the saturation limit of 2 T. Also, at startup, the power required by the pump is less than 99% of the input power at the design flow rate; hence, the rotor drive motor will be sized by the input power at full flow.

## Startup of the HYLIFE HREMP with a Normally Conducting Winding

For the normally conducting winding, the zero-flow head is lower than the HYLIFE gravity head (Fig. 25). Thus, for startup, the pump must be adjusted to temporarily produce a higher pressure. By combining Eqs. (9) and (14) and then solving for $P$, the pressure dependence on the flux density, $B$, and the field velocity, $v_s$, can be calculated.

$$P_m = \frac{B^2 (v_s - v_t) D_c^2 R_1}{D_c D_d R_1^2 + [4 \times 10^{-7}] (v_s - v_t) D_t [D_c D_d K]^{1/2}} \tag{42}$$

![](images/page_027_eq_0.png)
At startup, $R_s << X_s$ and $v_t = 0$. In addition, the

## Table 2. Design Point for the HYLIFE HREMP.

| Variable | Description | Pump with normal winding | Pump with superconducting winding |
|----------|-------------|--------------------------|-----------------------------------|
| **Flow and pressure specifications** | | | |
| $Q$ | Liquid-metal flow rate (m³/s) | 8.08 | 8.08 |
| $P$ | Pressure developed by the pump (kPa) | 90.75 | 90.75 |
| $P_i$ | Pressure rise required (kPa) | 82.50 | 82.50 |
| — | Pressure lost in the pump (kPa) | 8.25 | 8.25 |
| **Dimensionless ratios** | | | |
| $k_1$ | Ratio of pole pitch to magnetic gap | 6.50 | 3.00 |
| $k_2$ | Ratio of rotor length to pole pitch | 1.77 | 0.55 |
| $k_3$ | Ratio of field to fluid velocity | 1.13 | 1.40 |
| **Pump dimensions** | | | |
| $D_1$ | Thickness of liquid metal (m) | 0.343 | 0.322 |
| $D_2$ | Duct-wall thickness (m) | 0.0127 | 0.0127 |
| $D_3$ | Rotor-to-duct clearance (m) | 0.0254 | 0.0254 |
| $D_4$ | Duct-to-flux-return-path clearance (m) | 0.0254 | 0.0254 |
| $D_5$ | Total rotor-to-flux-return-path gap (m) | 0.420 | 0.380 |
| $D_6$ | Pole pitch (m) | 2.73 | 1.79 |
| $D_9$ | Duct-centerline diameter (m) | 1.74 | 1.14 |
| $D_{10}$ | Rotor diameter (m) | 1.32 | 0.544 |
| $D_{20}$ | Rotor length (m) | 4.83 | 0.987 |
| $D_{11}$ | Pole length in liquid metal (m) | 6.93 | 1.40 |
| — | Pole-shoe fraction of rotor surface (%) | 60 | — |
| — | Pole-shoe half angle (deg) | 34.0 | — |
| $D_{16}$ | Pole-shoe arc length (m) | 1.24 | — |
| $D_{14}$ | Maximum pole-shoe depth (m) | 0.271 | — |
| $D_{24}$ | Winding-arc length (m) | 0.807 | — |
| $D_{18}$ | Winding width (m) | 0.774 | — |
| $D_{19}$ | Pole-waist width (m) | 1.13 | — |
| $D_{22}$ | Flux-return-path width (m) | 0.190 | 0.235 |
| $D_{30}$ | Total HREMP outer diameter (m) | 2.54 | 2.51 |
| **Velocities, poles, and flux density** | | | |
| $N$ | Number of poles | 2 | 2 |
| $\beta_1$ | Pole angle (to horizontal) at duct centerline (deg) | 45.0 | 45.0 |
| $\beta_2$ | Pole angle (to horizontal) at rotor surface (deg) | 52.8 | 64.5 |
| $v_1$ | Liquid-metal velocity (m/s) | 6.10 | 6.10 |
| $v_2$ | Circumferential component of fluid velocity (m/s) | 4.31 | 4.31 |
| $v_3$ | Field velocity at duct centerline (m/s) | 4.87 | 4.87 |
| $B$ | Flux density in the liquid metal (T) | 0.194 | 0.364 |
| **Eddy current in lithium** | | | |
| — | Resistivity of lithium at 300°C (Ω·m) | $3.5 \times 10^{-7}$ | $3.5 \times 10^{-7}$ |
| $R_1$ | Resistance of eddy-current path in lithium (Ω) | $4.18 \times 10^{-5}$ | $1.96 \times 10^{-5}$ |
| $X_1$ | Inductive reactance of eddy-current path in lithium (Ω) | $2.50 \times 10^{-4}$ | $1.14 \times 10^{-4}$ |
| — | Lithium loop power-factor phase angle (deg) | 51.6 | 80.3 |
| $Z_1$ | Impedance of eddy-current path in lithium (Ω) | $4.92 \times 10^{-4}$ | $2.26 \times 10^{-4}$ |
| $V_1$ | Voltage induced per pole around one lithium eddy-current loop (V) | 0.521 | 0.620 |

**Table 2. (Continued.)**

| Variable | Description | Pump with normal winding | Pump with superconducting winding |
|---|---|---|---|
| | Eddy current per pole in lithium (A) | 107 000 | 274 000 |
| **Eddy current in duct wall** | | | |
| $\rho_3$ | Resistivity of steel at 500°C (Ω·m) | $9.16 \times 10^{-7}$ | $9.16 \times 10^{-7}$ |
| $R_3$ | Resistance of lithium duct wall (Ω) | $2.96 \times 10^{-5}$ | $2.13 \times 10^{-5}$ |
| $X_3$ | Inductive reactance of eddy-current path in each wall (Ω) | $2.24 \times 10^{-5}$ | $5.99 \times 10^{-6}$ |
| $Z_3$ | Impedance of eddy-current path in each wall (Ω) | $2.97 \times 10^{-5}$ | $2.11 \times 10^{-5}$ |
| $V_3$ | Voltage induced per pole around each lithium eddy-current loop in each wall (V) | 4.56 | 2.17 |
| | Eddy current in each wall (A) | 15 400 | 10 300 |
| **Winding ampere turns** | | | |
| $I_1$ | Winding ampere turns per pole to overcome the lithium eddy currents | 28 000 | 68 900 |
| $I_2$ | Winding ampere turns per pole to overcome steel eddy currents in both walls | 1 160 | 195 |
| $I_3$ | Winding ampere turns per pole to overcome reluctance of $D_1$ | 64 700 | 252 000 |
| $I_4$ | Total winding ampere turns per pole | 93 900 | 321 000 |
| **Flux losses** | | | |
| $e_1$ | Flux per pole through lithium (Wb) | 2.55 | 0.645 |
| $e_2$ | Flux leaking across inter-duct gap (Wb) | 1.20 | — |
| $e_3$ | Flux leaking through winding (Wb) | 3.64 | — |
| $e_4$ | Flux leaking over top of winding (Wb) | 3.103 | — |
| $e_5$ | Flux leaking over top of rotor waist (Wb) | 0.0877 | — |
| $e_6$ | Total flux per pole (Wb) | 7.58 | 0.645 |
| **Rotor design** | | | |
| $A_1$ | Area of rotor winding per pole (m²) | 0.0415 | 0.050 |
| $A_2$ | Total area of rotor steel (m²) | 1.28 | ignored |
| $\rho_2$ | Resistivity of copper winding at 225°C (Ω·m) | $2.8 \times 10^{-8}$ | — |
| $R_2$ | Resistance of copper winding (Ω) | $5.98 \times 10^{-6}$ | — |
| **Masses** | | | |
| $M_1$ | Rotor-steel mass (kg) | 47 800 | — |
| $M_2$ | Rotor-winding mass (kg) | 4 340 | 1 360 |
| $M_3$ | Total return-path mass (kg) | 51 500 | 14 100 |
| $M_4$ | Total HREMP mass (kg) | 105 000 | 12 500 |
| **Power flow** | | | |
| $\overline{PQ}$ | Gross hydraulic power (MW) | 0.733 | 0.733 |
| — | Slip loss (MW) | 0.0955 | 0.293 |
| — | Total $I^2R$ loss in walls (MW) | 0.279 | 0.0894 |
| — | $I^2R$ loss in windings (MW) | 0.211 | — |
| — | Hysteresis and eddy-current loss in flux return (MW) | 0.00881 | 0.00187 |
| — | Total input power to pump (MW) | 1.32 | 1.11 |
| — | Net hydraulic power (MW) | $0.667^*$ | 0.467 |
| **Efficiency** | | | |
| $\eta$ | Pump efficiency (%) | 50.2 | 39.6 |

![](images/tmpb2nh9hqp.pdf-30-full.png)

![](images/tmpb2nh9hqp.pdf-30-0.png)

![](images/tmpb2nh9hqp.pdf-30-1.png)

**Figure** **25.** **Pressure** **vs** **flow**
## **rate for an HREMP with a nor­**

**mally** **conducting** **winding**
**and** **with** **a** **design** **flow** **of** **8.08**
**m3/s** **at** **a** **head** **of** **82.5** **kPa.** **Ef­**
**ficiency** **contours** **and** **the**
**pressure-drop** **curve** **for** **the**
## **HYLIFE loop are also shown.**

**Figure** **26.** **Pressure** **and** **flow**
## **rate for an HREMP with a**

**superconducting** **winding** **and**
**with** **a** **design** **flow** **of** **8.08**
**m3/s** **at** **a** **head** **of** **82.5** **kPa.** **Ef­**
**ficiency** **contours** **and** **the**
**pressure-drop** **curve** **for** **the**
## **HYLIFE loop are also shown.**

![](images/tmpb2nh9hqp.pdf-31-full.png)

values of _Rv_ _Dlr_ _D5,_ D6, and D10 cannot be easily
changed. Hence,

From Fig. 25, if _v2_ is held constant, the mag­
netic flux density, B, must be increased to 143% of
the design value to produce the HYLIFE gravity
head. However, the flux density increases to 2 I in
the flux return path and 3 T in the rotor core. To
decrease the rotor core-flux density to the 2 T
saturation limit, the rotor must either be enlarged
![](images/page_031_eq_0.png)
or be constructed with more than 60% pole shoe
area. Alternatively, the rotor could be designed to
have a flux density less than 1.39 T at the design
point, but this would also increase the rotor
diameter.

If the flux density and rotor dimensions are
left at their design point values, the zero-flow
pressure can still be increased by decreasing the
rotor speed and, hence, the field velocity, _v2._ At a
field velocity of 2.09 m/s (43% of the design
value), the zero-flow pressure equals the HYLIFE
gravity head. The lower field velocity can be pro­
duced by using a two-speed gear box between the
drive motor and the rotor. Actually, a three-speed
gear box will be required (Fig. 27). The low rotor
speed (43% of design) will increase the flow rate
to ~3 m3/s when the pump-head curve falls be­
low the loop pressure drop. Shifting to an inter­
mediate rotor velocity (72% of design) will in­
crease the flow rate to ~6 m3/s. A second shift to
the design rotor speed will allow the flow rate to
increase to the desired value of ~8 m3/s.

**Figure** **27.** **Startup** **pressure-**
**flow** **rate** **curves** **for** **an**
## **HREMP with normally con­**

**ducting** **windings** **and** **with**
**guidevanes** **in** **the** **pump** **annu­**
**lus.** **The** **rotor** **velocity** **will** **se­**
**quentially** **be** **switched** **from**
**43%** **to** **72%** **to** **100%** **of** **the** **de­**
**sign** **value** **as** **the** **developed**
## **pressure falls to the HYLIFE**

**pressure-drop** **curve.**

At startup, and using the lower field velocity,
the magnetic flux densities in the rotor core and
flux return path are 1.9 T and 1.4 T, respectively;
both values are below the 2 T saturation level. In
addition, the power required by the pump at
startup is less (36%) than the input power at the
design point; hence the drive motor need not be
oversized for startup.

The preceding startup analysis for an HREMP
with a normally conducting winding is oversim­
plified because it assumes the liquid can only flow
in a helical path through the pump duct, as would
be the case if helical guide vanes were placed
within the pump annulus. Consider our situation
where no guide vanes are used. At startup, the
circumferential component of the Lorentz force
will spin the fluid until the force is balanced by
friction and MHD losses. However, the spinning
fluid will then have a nonzero value of tq, and the
developed pressure will increase [see Eq. (42)]. If
the developed pressure increases to above the
HYLIFE gravity head, a multispeed gear box will
not be required. Alternatively, if the loop is only
partially filled at startup, the gravity head will be
reduced, and startup can be accomplished at the
design rotor speed and magnetic-flux density.

Sensitivity of the Design Point to _**Kv**_
## K2, and K3

The HREMP designs for both a normally con­
ducting and a superconducting winding, pre­
sented above, were selected from a large number

![](images/tmpb2nh9hqp.pdf-31-0.png)

![](images/tmpb2nh9hqp.pdf-32-full.png)

of potential designs in which the three dimension­
less variables _Kv_ _K2,_ and X3 were varied paramet­
rically. Figures 28 and 29 show the result of
changing each dimensionless variable while hold­
ing the other two constant at their design values
for each type of winding. The ratio of efficiency to
mass-diameter product was selected as a figure of
merit because our overall objectives are to maxi­
mize the pump efficiency and to reduce power
plant capital cost. Minimizing the pump mass
(M4) reduces pump cost and minimizing the pump
diameter (D2o) reduces building cost. Because both
of these terms appear in the denominator of the
ratios plotted in Figs. 28 and 29, the optimal val­
ues for the three dimensionless variables may be
derived from the points where the ratios are maxi­
mized. In terms of cost, the pump height is rela­
tively unimportant because it is less than the
height of both the reactor vessel and the steam
generators. In fact, there is sufficient height in the
building to allow for mounting of the rotor drive
motor either above or below the pump.

Tradeoffs Among Efficiency, Mass,
Diameter, and Winding Type

For each winding type, the design values of
Xj, _K2,_ and _K3_ were chosen to maximize the ratio

of efficiency to mass-diameter product. Actually,
this ratio is an overly simple figure of merit. For
example, increased efficiency may be more or less
valuable than decreased diameter or mass. If effi­
ciency alone were the figure of merit, the maxi­
mum pump efficiency would increase from 50%
to 54% for the normal winding and from 60% to
69% for the superconducting winding. A value
may be assigned to the increased efficiency if the
electricity cost and interest rate are known. For
example, increasing each HYLIFE pump efficiency
from 50% to 69% increases the plant output by
0.36 MW (per pump). At 5(t/kW-hr and a 70% ca­
pacity factor, this energy has an annual value of
$110 000. If the interest rate is 10%, up to $1.1 mil­
lion could be invested in each wider or heavier
pump (and larger building) before the efficiency
savings are lost. However, if the efficiency is in­
creased by using a more complex pump (such as
one with cryogenic windings), the pump is likely
to be less reliable, and the plant will be opera­
tional less of the time. Decreased plant availability
of only 0.3% would cancel the benefit of increas­
ing the efficiency of 11 HYLIFE pumps from 50%
to 69% if that efficiency improvement could be
obtained with no capital cost.

Both pumps could have improved efficiency
if the duct walls could be made thinner (below the
assumed 12.7 mm) and if the duct-to-flux-returnpath clearance could be eliminated. The ultimate

**Figure** **28.** **Sensitivity** **of** **the**
**design** **point** **to** **changes** **in** _K3,_
_K2,_ **and** _K3_ **for** **the** **normally**
**conducting** **winding.**

![](images/tmpb2nh9hqp.pdf-32-0.png)

1.6 1.64 1.68 1.72 1.76 I.S^a

duct wall thickness will be determined by a stress analysis, and the clearance will depend on differential thermal expansion between the duct and the flux return path and on construction procedures.

For a given winding type, tradeoff of efficiency and size can be made when the pump cost per kg of pump mass and the building cost per meter of pump diameter are known. The design ratio to be optimized will be a function of these cost factors in addition to the interest rate and electric energy value. Thus, the design ratio may have the form

$$\frac{(\text{efficiency})^a}{(\text{mass})^b \cdot (\text{diameter})^c} \tag{44}$$

where a, b, and c are positive constants.

When the normal and superconducting windings are compared, additional consideration must be given to the effect of each pump type on the plant availability.

## Selection of Pump Type

![](images/page_033_eq_0.png)
Our design values for the three dimensionless variables ($K_1$, $K_2$, and $K_3$), and the efficiency; mass,

and diameter are shown in Table 3 for each pump type.

At first glance, the pump with a superconducting winding seems superior but because its design ratio is 11.5 times larger than the design ratio of a pump with a normal winding. However, if a more realistic figure of merit were used, e.g., when the cost of the cryogenic cooling system is coupled with decreased plant availability resulting from reduced reliability, the pump with a normal winding may prove to be the best choice.

### Table 3. Design values for an HREMP with either normal or superconducting windings.

| Variable | Normal winding | Superconducting winding |
|---|---|---|
| $K_1$ | 6.5 | — |
| $K_2$ | 1.77 | 0.55 |
| $K_3$ | 1.13 | 1.40 |
| Efficiency (%) | 50.2 | 59.6 |
| Mass* (Mg) | 109 | 12.5 |
| Diameter (m) | 2.54 | 2.21 |
| Design ratio | 0.188 | 2.19 |

\* Neither design includes the mass of the drive motor or heat removal systems.

[Figure 29: Sensitivity of the design point to changes in $K_1$, $K_2$, and $K_3$ for the superconducting winding.]

> $K_1$ = pole pitch/magnetic gap
> $K_2$ = rotor length/pole pitch
> $K_3$ = field velocity/fluid circumferential velocity
>
> The (efficiency/(mass × diameter) ratios have been normalized to the value at $K_1$ = 3.0, $K_2$ = 0.56, and $K_3$ = 1.4

![](images/tmpb2nh9hqp.pdf-34-full.png)

**Acknowledgments**

The support of Mike Monsler (LLNL) and Nate Hoffman (ETEC), and the substantial editorial efforts
of Bob Kirvel (LLNL Technical Information Department) are gratefully acknowledged.

![](images/tmpb2nh9hqp.pdf-35-full.png)

**References**

1. _Laser_ _Program_ _Annual_ _Report_  - _1978,_ Lawrence Livermore National Laboratory, Livermore, CA,
UCRL-50021-78 (1979), pp. 8-1 to 8-118.
2. M. Faraday, "Experimental Researches in Electricity," _Phil._ _Trans._ _Roy._ _Soc._ 15, 125 (1832).
3. R. S. Baker, "Electromagnetic Pumps," _Sodium-NaK_ _Eng._ _Handbook,_ O. J. Foust, Ed. (Gordon and
Breach Science Publishers, Inc., New York, NY, 1978), vol. 4, section 1-3.
4. _Alternating_ _Current_ _Electromagnetic_ _Pump_ _(Conducting_ _Type)_ _for_ _Liquid_ _Metals,_ MSA Research Corpora­
tion, Evans City, PA, Bulletin EP-3 (1965).
5. R. S. Baker, _Theory,_ _Design,_ _and_ _Performance_ _of_ _Helical-Rotor_ _Electromagnetic_ _Pump,_ Atomics Interna­
tional, Canoga Park, CA, NAA-SR-7455 (May 31, 1963).
6. G. B. Kliman, "Large Electromagnetic Pumps," _Electric_ _Machines_ _and_ _Electromechanics:_ _An_ _International_
_Quarterly_ (Hemisphere Publishing Corp., Washington, DC, 1979), vol. 3, pp. 129-142.
7. G. R. Slemon and A. Straughen, _Electric_ _Machines_ (Addison-Wesley Publishing Co., Reading, MA,
1980), pp. 380-382.
8. R. Rudenberg, "Energie der Wirbelstrome in Elektrischen Bremsen und Dynamomaschinen," in
_Sammlung_ _Elektrotechnischer_ _Vortrage;_ English trans.: "Energy of the Eddy-Currents in Electric Brakes
and Dynamo Machines," in _Collection_ _of_ _Electrotechnical_ _Lectures_ (Ferdinand Enke, Stuttgart, Ger­
many, 1907), vol. 10, pp. 269-370. English trans. available from the Eng. Soc. Libraries, 345 East 47th
St., New York, NY 10017.
9. R. S. Baker, _Effect_ _of_ _Rotor_ _Helix_ _Angle_ _on_ _Performance_ _of_ _Helical_ _Rotor_ _Electromagnetic_ _Pump,_ Atomics
International, Canoga Park, CA, AI-65-TDR-215 (Jan. 27, 1966).
10. R. S. Baker, "Eddy Current Reaction with Magnetic Field Produced by Helical-Rotor," _IEEE_ _Trans._
_Ind._ _Gen._ _Applic._ _IGA-4,_ 6, pp. 673-675 (1968).
11. A. Gray and P. M. Lincoln, _Electrical_ _Machine_ _Design_ (McGraw-Hill, New York, NY, 1926), 2nd ed.,
p. 212.
12. _Inductrol_ _Voltage_ _Regulators_ _Buyer's_ _Guide,_ General Electric Company, Pittsfield, MA, GEP-1450B
(1962).
13. _Laser_ _Program_ _Annual_ _Report_ - _1981,_ Lawrence Livermore National Laboratory, Livermore, CA,
UCRL-50021-81 (1982), pp. 212-243.

RDK/kas

# Glossary

## Acronyms and Keywords

| Term | Definition |
|------|------------|
| ALIP | Annular-linear-induction pump, also called the Einstein-Szilárd pump. |
| Ampere-turn | A current of one ampere in a single-turn winding. |
| ASEA | An international manufacturer of electrical machinery for heavy industry, with headquarters in Sweden. |
| Cavitation | The formation of vapor bubbles in a liquid. When the vapor bubbles collapse, the resulting small, high-velocity liquid jets can pit or wear pump components. |
| Eddy-current braking | Retardation of liquid-metal flow caused by interaction of magnetic fields and electric currents. An EM pump running backwards acts as an eddy-current brake. In an EM pump running normally, the braking force operates where the liquid metal enters and exits the magnetic field of the pump. |
| Eddy-current path | The path followed by electrical currents induced by changing magnetic fields. |
| Electromagnet | A magnet that produces its magnetic field from electric current in a winding (field coil). |
| EM | Electromagnetic, used in reference to a pump that applies a magnetic field perpendicular to an electrical current in a liquid-metal so that metal will flow in the mutually perpendicular direction. |
| Field coil | A winding designed to produce a magnetic field. |
| FLIP | Flat-linear-induction pump. |
| Head | The height of fluid required to produce a specified pressure. |
| HREMP | Helical-rotor electromagnetic pump. |
| HYLIFE | High-yield lithium-injection fusion energy (converter), an ICF reactor design. |
| ICF | Inertial confinement fusion. |
| Impedance | The square root of the sum of squares of reactance and resistance. |
| Impeller pump | A mechanical pump that applies the pumping force with blades on a rotating assembly. Impeller pumps use many blades with only small extensions into the fluid. |
| Inducer pump | A mechanical pump with fewer and larger blades than an impeller pump. Compared to impeller pumps, inducer pumps require a much smaller pressure in the fluid at the pump entrance (net positive suction head or NPSH). |
| Lorentz force | The force that results when a magnetic field is applied perpendicular to an electric current. The resultant Lorentz force in an electromagnetic pump drives the liquid metal in a direction that is mutually perpendicular to both the magnetic field and the electric current. |
| LMFBR | Liquid-metal fast-breeder reactor. |
| LMW | Liquid-metal wall. |
| MHD | Magneto-hydrodynamic. |
| mmf | Magnetomotive force. The line integral of the magnetic field strength around a closed path (field line). |
| MVAR | Megavolt-amperes reactive. |

Piping system anchor point
: A point on a piping system that cannot move because it is secured to the building. Expansion of pipes between anchor points during startup and shutdown (when temperature changes) must be accommodated by either pipe bends or bellows.

Pole
: The regions on a magnet at which the magnetic flux density is concentrated.

Pole pitch
: The distance between pole centerlines on a magnet. In an HREMP, the pole pitch is the arc length between pole centerlines at the duct-centerline radius.

Pole shoe
: Portions of the rotor surface not covered by the winding in an HREMP.

Power-factor correction
: Capacitance added to a circuit to balance that circuit's intrinsic inductance. Because only the resistive power can do work at the load, lagging volt-amperes due to inductance must be corrected by leading volt-amperes (static capacitors or overexcited synchronous motors) to avoid carrying nonuseful power and to minimize wire size. The power factor for a fully corrected circuit is 100%.

Power-factor phase angle
: The angle between the resistance and the impedance (zero when the impedance is purely resistive).

Pump annulus
: The region where fluid flows between two concentric cylindrical walls.

Pump efficiency
: The ratio of net hydraulic power to total input power.

SCR
: Silicon-controlled rectifier, also called a thyristor. A solid-state device that permits current flow in only one specified direction and only after a control pulse is applied to a third terminal.

SI
: Systeme Internationale, the international metric system of dimensional units.

Space harmonic
: A traveling magnetic flux wave of higher spatial frequency that has among its zero points all the zero points of the fundamental wave.

Static pressure
: The product of the fluid density and the height the fluid is to be lifted ($P = \rho g h$, where $P$ is the static pressure and $h$ is the static head).

Volute
: The entrance and exit regions of a pump, where the circular pipe cross section is changed to the pump-duct shape.

Winding
: Electric wire arranged in concentric loops so that a magnetic field is produced through the center of the loops when electric current flows in the wire.

## Symbols

| Symbol | Description |
|--------|-------------|
| $A_1$ | Area of rotor winding per pole |
| $A_2$ | Area of rotor steel |
| $B$ | Magnetic flux density |
| $C$ | Curve that defines the loop in Faraday's Law of Induction |
| $dA$ | Infinitesimal area on surface $S$ with a direction that is normal to the surface |
| $dl$ | Infinitesimal length along curve $C$ |
| $D_1$ | Width of liquid-metal |
| $D_2$ | Duct-wall thickness |
| $D_3$ | Rotor-to-duct-wall clearance |
| $D_4$ | Duct-to-flux-return-path clearance |
| $D_5$ | Total magnetic circuit gap between rotor and flux-return path |
| $D_6$ | Pole pitch |
| $D_8$ | Duct-centerline diameter |
| $D_9$ | Rotor diameter |
| $D_{10}$ | Rotor length |
| $D_{11}$ | Length of pole in the liquid metal |
| $D_{12}$ | Pole-shoe arc length |
| $D_{13}$ | Maximum pole-shoe depth |
| $D_{14}$ | Winding-arc length |
| $D_{15}$ | Winding width |
| $D_{16}$ | Pole-waist thickness |
| $D_{19}$ | Flux-return-path width |
| $D_{20}$ | Total HREMP outer diameter |
| $E$ | Electric field vector in Faraday's Law of Induction |
| **F** | Lorentz force |
| $F_{em}$ | Electromagnetic force |
| $I_f$ | Filament current |
| $I_s$ | Winding rms current in an ALIP or FLIP |
| $I_1$ | Number of ampere turns on the rotor to overcome the demagnetizing effect of the eddy-current flow in the liquid metal |
| $I_2$ | Ampere turns required to overcome the demagnetizing effect of current loops in the inner and outer annulus walls |
| $I_3$ | Ampere turns required to overcome reluctance of $D_5$ |
| $I_4$ | Total ampere turns required per pole on the HREMP rotor |
| $K$ | Ratio of pole pitch to magnetic-circuit gap ($D_6/D_5$) |
| $K_1$ | Ratio of rotor length to pole pitch ($D_{10}/D_6$) |
| $K_2$ | Ratio of circumferential field velocity to circumferential fluid velocity ($v_2/v_1$) |
| $M$ | Copper-winding mass |
| $M_1$ | Flux-return-path mass |
| $M_2$ | North-pole mass |
| $M_4$ | Total HREMP mass |
| $N$ | Number of poles |
| $N_W$ | Number of effective turns per phase |
| $P$ | Pressure rise actually developed by the pump |
| $Q$ | Liquid-metal volumetric flow rate |
| $R_1$ | Resistance of eddy-current path in the liquid metal |
| $R_2$ | Resistance of duct-wall eddy-current path |
| $S$ | South pole |
| $S$ | Surface defined by the loop in Faraday's Law of Induction |
| $v$ | Liquid-metal velocity within the pump annulus |
| $v_1$ | Circumferential component of the fluid velocity |
| $v_2$ | Circumferential field velocity |

| Symbol | Definition |
|--------|-----------|
| $V_1$ | Voltage induced by one pole around the liquid-metal eddy-current loop |
| $V_2$ | Voltage induced by one pole around the eddy-current loops in the inner and outer duct walls |
| $\dot{W}$ | Power input to an HREMP |
| $X_1$ | Inductive reactance of the eddy-current path in the liquid metal |
| $X_2$ | Inductive reactance of the eddy-current path in each pump-duct wall |
| $Z_1$ | Impedance of the eddy-current path in the liquid metal |
| $Z_2$ | Impedance of the eddy-current path in each pump-duct wall |
| $\eta$ | Efficiency |
| $\ell$ | Liquid-metal filament length through which the electric current and magnetic field interact to produce the Lorentz force |
| $\phi_1$ | Flux through the liquid metal |
| $\phi_2$ | Flux leaking from pole shoe to pole shoe through the gap between rotor and liquid-metal annulus |
| $\phi_3$ | Flux leaking from pole shoe to pole shoe through the winding |
| $\phi_4$ | Flux leaking from pole shoe to pole shoe over the top of the rotor and winding |
| $\phi_5$ | Flux leaking from pole shoe to pole shoe over the top of the rotor and pole waist |
| $\phi_t$ | Total flux |
| $\rho_1$ | Electrical resistivity of lithium at 500°C |
| $\rho_2$ | Electrical resistivity of type 304 stainless steel at 500°C |
| $\rho_3$ | Electrical resistivity of copper at 250°C |
| $\theta_1$ | Helix angle of the eddy-current path in the liquid metal |
| $\theta_2$ | Helix angle of the pole centerline at the rotor edge |