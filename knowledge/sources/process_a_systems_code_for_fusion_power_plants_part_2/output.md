---
source: "kovari2016.pdf"
source_type: "local_file"
extracted_at: "2026-09-08T14:02:34.358008+00:00"
content_hash_sha256: "f1acb2ed2d10c31bb82f4b8d6fcf5b8d7800d06d4bc465e19f305726d9f916f1"
backend: "pdf_pipeline"
---

Fusion Engineering and Design 104 (2016) 9–20 

![](images/kovari2016.pdf-0001-01.png)

Contents lists available at ScienceDirect 

## ~~Fusion Engineering and Design~~ 

jo ur nal home p age: www.elsevier.com/locate/fusengdes 

![](images/kovari2016.pdf-0001-05.png)

## “ ” – PROCESS : A systems code for fusion power plants Part 2: Engineering 

![](images/kovari2016.pdf-0001-07.png)

M. Kovari[∗] , F. Fox, C. Harrington, R. Kembleton, P. Knight, H. Lux, J. Morris 

CCFE, Culham Science Centre, Abingdon, Oxon OX14 3DB, UK 

## h i g h l i g h t s 

• PROCESS is an optimising systems code for fusion reactors. • It allows the user to choose which constraints to impose and which to ignore. • Multiple constraints greatly restrict the parameter space of the optimised model. • For example, when coil current is increased greatly, major radius hardly changes. 

a r t i c l e i n f o a b s t r a c t Article history: PROCESS is a reactor systems code – it assesses the engineering and economic viability of a hypothetical Received 10 July 2015 fusion power station using simple models of all parts of a reactor system. PROCESS allows the user to Received in revised form choose which constraints to impose and which to ignore, so when evaluating the results it is vital to 15 December 2015 study the list of constraints used. New algorithms submitted by collaborators can be incorporated – for Accepted 7 January 2016 Available online 1 February 2016 example safety, first wall erosion, and fatigue life will be crucial and are not yet taken into account. This paper describes algorithms relating to the engineering aspects of the plant. The toroidal field (TF) coils and the central solenoid are assumed by default to be wound from niobium-tin superconductor Keywords: Fusion reactor with the same properties as the ITER conductors. The winding temperature and induced voltage during Thermonuclear a quench provide a limit on the current density in the TF coils. Upper limits are placed on the stresses Deuterium in the structural materials of the TF coil, using a simple two-layer model of the inboard leg of the coil. Tritium The thermal efficiency of the plant can be estimated using the maximum coolant temperature, and the Economics capacity factor is derived from estimates of the planned and unplanned downtime, and the duty cycle if Magnet the reactor is pulsed. Neutronics An example of a pulsed power plant is given. The need for a large central solenoid to induce most of the Reliability plasma current, and physics assumptions that are conservative compared to some other studies, result Availability Capacity factor in a large machine, with a cryostat 36 m in diameter. Multiple constraints, working together, restrict the Blanket parameter space of the optimised model. For example, even when the ratio of operating current to critical Divertor current in the TF coils is increased by a factor of five, the total coil cross-section decreases only a little, DEMO because of the need for copper stabiliser, insulation, and structural support. The result is that the plasma major radius hardly changes. It is these surprising results that justify the development of systems codes. Crown Copyright © 2016 Published by Elsevier B.V. All rights reserved. 

## **1. Introduction** 

While physicists at experimental machines investigate whether a fusion plasma can be confined, it is equally important to assess whether a fusion plant is feasible from the engineering and economic points of view. Information on this is collated in reactor systems codes, which contain simple models of an entire power 

∗ Corresponding author. E-mail address: michael.kovari@ccfe.ac.uk (M. Kovari). http://dx.doi.org/10.1016/j.fusengdes.2016.01.007 

plant, including physics, engineering and costs. The process systems code has been used for many years, and details of its physics algorithms and general structure have been published previously [1]. This paper describes the engineering assumptions and models. PROCESS is one of the most flexible of all reactor systems codes. It finds a set of parameters that maximise (or minimise) a Figure of Merit chosen by the user, while being consistent with the constraints, by adjusting a set of variables known as iteration variables. Both the constraints and the iteration variables are chosen by the user from an extensive selection. In effect, therefore, the user can 

© 2016 Published by Elsevier B.V. All rights reserved. 

Copyright 

0920-3796/Crown 

![](images/kovari2016.pdf-0002-02.png)

**Fig. 1.** Cross-sections of PROCESS model of a pulsed reactor. In one of the TF coils the winding pack is shown in blue, and the shielding for the neutral beam duct in grey. The thermal shielding which is needed to separate the cold superconducting coils from the hot reactor inside, and from the cryostat outside, is not included explicitly. The ports for diagnostics and remote handling are not shown because they are not modelled in PROCESS. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.) 

choose which are input variables and which are outputs. Only those constraints specified by the user are enforced. We describe process version 393. 

Sections 2–8 describe the models for the superconducting magnets, the first wall, blanket and shield, the flow of thermal power and its conversion to electricity, and the availability model. Section 9 describes a pulsed DEMO model obtained using PROCESS, illustrated in Fig. 1. 

## **2. Toroidal field coil (TFC)** 

In PROCESS the TF coil consists of a winding pack with a homogenous current density, surrounded by a structural case. Several conductor models are available, but the default assumes the use of forced-flow helium cooled superconducting cables, such as the cable-in-conduit type. AC losses are not taken into account. A number of constraints are available for the TF coil but, as always, are only enforced if selected by the user. They include: (a) stress in case, (b) stress in conduit, (c) ratio of operating current to critical current, (d) superconductor temperature margin, (e) quench voltage, and (f) quench temperature. Details are below. 

Numerous input parameters are available as iteration variables, in which case PROCESS will vary them automatically, making them effectively outputs. These include the toroidal field on axis, the radial thickness of the TFC, the coil current per turn, the copper fraction in the conductor, the overall current density in TF coil inboard legs, and many others. The TFC is symmetrical, each half being approximated by 4 circular arcs along the edge facing the plasma. The height is determined purely by the vertical build – the coil is not required to have a constant tension “D” shape. Note that the inboard leg is not exactly straight. This model is used only to calculate the mass, inductance and stored energy. 

## 2.1. Access required for neutral beams 

The maximum tangency radius for the neutral beams is determined by the size and shape of the TF coils, as the beams need to pass between them at an angle. This may be an important constraint on the achievable neutral beam current drive, as this is usually maximum when the tangency radius is equal to or slightly greater than the major radius [1,2]. Fig. 2 shows the geometry and symbols used. The need for remote handling may impose additional constraints. If the blanket modules run the full height of the machine, and are accessed for maintenance from above, then it would not be acceptable for a neutral beam duct to cut the whole blanket module in half, but this constraint has not been included 

## half, 

![](images/kovari2016.pdf-0002-12.png)

![](images/kovari2016.pdf-0002-13.png)

NTF is the number of TF coils, and C is the width required for the neutral beam duct, including any shielding required to protect the TF coils on either side, the thickness of the duct wall, the thermal shields and the vacuum gaps. 

## shields 

J = �G[2] − C[2] (7) 

![](images/kovari2016.pdf-0003-01.png)

**----- Start of picture text -----**<br>
M. Kovari et al. / Fusion Engineering and Design 104 (2016) 9–20<br>**----- End of picture text -----**<br>

![](images/kovari2016.pdf-0003-02.png)

**Fig.** 

**2.** 

for neutral beam access between TF coils. 

![](images/kovari2016.pdf-0003-06.png)

**Fig. 3.** Critical current of Nb3Sn TFC strand using ITER parameterisation. Strain = −0.3%. 

![](images/kovari2016.pdf-0003-08.png)

![](images/kovari2016.pdf-0003-09.png)

In the default model the parameterisation of critical current density in Nb3Sn as a function of magnetic field B, temperature T and strain ε uses the ITER formulation [3], correcting for the strand cross-section and the fraction of the strand occupied by copper (Fig. 3). The fitting parameters are in Table 1. The peak magnetic field is calculated using a parametric fit to detailed calculations from the Biot–Savart law, while the temperature and strain are set by the user. Critical strand current in the reference strand (0.82 mm diameter, copper: non-copper ratio = 1): 

![](images/kovari2016.pdf-0003-11.png)

**Table 1** ITER reference scaling parameters for TF and CS conductor design [4]. 

## Critical field: 

![](images/kovari2016.pdf-0003-15.png)

![](images/kovari2016.pdf-0003-16.png)

![](images/kovari2016.pdf-0003-17.png)

B b0 = (16) BC[∗] 2[(0][,] ε) Reduced temperature at zero field: T t = (17) TC[∗][(0][,] ε) The critical current density in a general strand is Jc[str] = Jc[sup] (1 − fCu) (18) where fCu is the fraction of each strand occupied by copper, and the current density in the superconductor, Jc[sup] , is derived from the reference strand described above. The critical current of the cable is Ic[cable] = Jc[str][A][cs][ (1] − fHe) (19) 

Geometry 

![](images/kovari2016.pdf-0004-02.png)

**Fig. 4.** Layout of the TFC cable, used for calculating current density and effective Young’s modulus. Additional structural material is taken into account as shown, and is described as “radial plates”. 

where Acs is the interior cross-sectional area of the cable, fHe is the fraction of that area occupied by helium coolant. The actual current per turn is an input, and is available as an iteration variable. The temperature margin is the difference between the temperature at which the critical current equals the actual current, and the actual temperature. 

The TF conductor is taken to be of the cable-in-conduit design, as illustrated in Fig. 4. The cross-sectional area of the conductor is calculated, after allowing for the rounded corners and the fraction occupied by helium coolant. 

occupied by 

## 2.3. Quench protection of TFC 

During a quench the coil needs to be discharged into an external resistor to protect the cable and limit the induced voltage. The maximum permissible winding temperature during a quench provides a limit on the current density. It is assumed that the superconductor, copper and helium remain in thermal equilibrium with each other, but no heat is taken up by the conduit. The variation of heat capacity and resistivity with temperature are taken into account, but not the effect of the magnetic field on the resistivity of the copper stabiliser. The dump resistor has a resistance much higher than that of the coil during the quench. The maximum current density in the cable space is given [5] by 

![](images/kovari2016.pdf-0004-09.png)

where V is the peak voltage developed across the coil, Iop = current per turn, EstoTF = stored energy per coil, fCu, fHe, fsc are the volume fractions of helium, copper and superconductor in the cable space, and 

![](images/kovari2016.pdf-0004-11.png)

![](images/kovari2016.pdf-0004-12.png)

where � = density, C = specific heat capacity, T0 is the operating temperature, Tmax is the maximum temperature reached (input by the user), and � = electrical resistivity of copper. No limits are placed on the pressure in the conduit or on the stability of the conductor. The user can specify the time constant for the quench (tdump), and can also set an upper limit for the peak voltage V developed by the quench. The stored energy per coil is LIop[2][/][ (2][N][TF][),] where L is the total inductance of the TF coil set, therefore 

![](images/kovari2016.pdf-0004-14.png)

![](images/kovari2016.pdf-0004-15.png)

**Fig. 5.** A portion of the inboard part of the TF coils, showing a self-supporting arch or vault. The arrows represent the net Lorentz force on each coil. 

![](images/kovari2016.pdf-0004-17.png)

**Fig. 6.** Mid-plane cross-section of inboard leg of TFC. (a) As used for calculating cross-sectional areas, (b) as used for calculating stress, showing the major radii of the dividing surfaces. 

the dividing 

This assumes that the energy deposited in a single dump resistor is derived from the energy stored in a single TF coil only. 

## 2.4. Stress in the TFC 

The net forces on the TF coils are inward (towards the major axis of the machine). In principle these can be supported on the central solenoid (as on JET) or on an additional structural part known as a bucking cylinder, or the straight sections of the coils can form an arch, also known as a vault (as on ITER), illustrated in Fig. 5. Tolerance problems make it difficult to use more than one method. Using the CS to support the TF coils is efficient, but causes problems as the stresses vary during the pulse, so PROCESS assumes that a vault is used. Only the stresses in the inboard leg at midplane are calculated. The field from the CS and PF coils is not included in any way, and only steady-state stress is calculated. Fig. 6 shows the layouts assumed. 

The ITER TF coils have steel radial plates that provide extra support for the cable. To represent this in a simplified way, PROCESS allows additional structural material within the winding pack, of the same material as the TF case (see Fig. 4). The winding pack is modelled in the stress calculation as a homogeneous material. Because this cable is assumed to be square, an isotropic elastic modulus is used in the horizontal plane. The vertical Young’s modulus is used for the separate calculation of vertical tensile stress. The shear stresses with a vertical component are zero because the outof-plane forces on the coil due to the poloidal field are neglected. To calculate the effective Young’s modulus of the winding pack each turn of the coil is split conceptually into series and parallel 

![](images/kovari2016.pdf-0005-02.png)

**Fig. 7.** The cable plus radial plate shown split into series and parallel components. The insulation is i, conduit s, the conductor w, and the radial plate r. 

parts as shown in Fig. 7. While the turn is square and therefore symmetric, there are two different ways to split it, giving different values for the smeared Young’s modulus, although the difference is small and has no physical significance. One value has been chosen arbitrarily, as follows. Assuming that the force is applied in the direction of the arrow, the components a–d carry the load in parallel, so they have the same strain. In component b, for example, the insulation (i) and the radial plate (rp) are series, so they have the same stress. Components b and c have very little stiffness, since they are mostly composed of insulation, superconductor and helium. The effective Young’s moduli for the components labelled a–d in Fig. 7 are therefore 

![](images/kovari2016.pdf-0005-05.png)

![](images/kovari2016.pdf-0005-06.png)

where the subscripts are s, conduit (steel); rp, radial plate (also steel); i, insulator; w, conductor. The combined modulus is 

![](images/kovari2016.pdf-0005-08.png)

When the load is vertical the conductor, conduit, insulator and radial plate are all in parallel, so the modulus is 

## radial 

![](images/kovari2016.pdf-0005-11.png)

Poisson’s ratio _v_ is taken as 0.3 in all cases. 

## 2.4.1. Horizontal stress components 

The TF coil is split into two layers: the winding pack and the case (Fig. 6). The force on the inboard leg is primarily directed towards the machine axis, so the bulk of the case is best used on the side nearest this axis. The thin layer of steel on the plasma-facing side is ignored. The toroidal field at the outer edge of the winding pack is BmaxTF. 

force per unit volume is radial, 

![](images/kovari2016.pdf-0005-16.png)

The current density, assumed to be constant, is 

![](images/kovari2016.pdf-0005-18.png)

where r0 and ri are the radii of the winding pack and ITFC is the total current in the set of TF coils. Inside the winding pack at major radius r, Ampere’s law gives the field, assumed to be toroidally uniform, as B = 2[�] �r[0][j�][�] r[2] − ri[2] � . (33) By toroidal symmetry, the local displacement u is purely radial. Using a cylindrical co-ordinate system (r, �), and the definition of Poisson’s ratio _v_ , it can be seen that the strain components are 

![](images/kovari2016.pdf-0005-20.png)

![](images/kovari2016.pdf-0005-21.png)

> where _v_ is Poisson’s ratio, and E is the combined Young’s modulus for the layer in question. From local force balance a differential equation is derived for 

## each 

layer, 

![](images/kovari2016.pdf-0005-25.png)

![](images/kovari2016.pdf-0005-26.png)

The solution for the displacement is: 

![](images/kovari2016.pdf-0005-28.png)

where C1 and C2 are constants of integration, defined for each layer. The boundary conditions give a set of four equations, which are solved using Gaussian elimination each time the code is run, to give the strain as a function of radius in each layer. The peak tangential stress is much greater than the peak radial stress. The highest stress in the case is at the innermost radius and the highest stress in the winding at the innermost radius of the winding. In the winding pack the averaging procedure is reversed to give the stress in the structural portion (conduit and radial plates) and the strain in the conductor. 

The 

Lorentz 

2.4.2. Vertical stress components By Ampere’s law the inside the TF coil is 

toroidal field at major radius r 

## vacuum 

![](images/kovari2016.pdf-0006-04.png)

The field outside the coil is nearly zero (exactly zero for an infinite number of coils), so the average field inside the winding pack is approximately half this value. The Lorentz force per unit length of coil is therefore about 

![](images/kovari2016.pdf-0006-06.png)

(NTF = number of TF coils). This force is perpendicular to the coil segment, and its vertical component is fdr where dr is the component of the segment length along the major radius. The total vertical force on upper half of the coil is then 

![](images/kovari2016.pdf-0006-08.png)

It can be shown that the tensile force in the inboard leg is half of this. The superconductor is likely to be twisted, which minimises its tensile stress, so we neglect the stiffness of the conductor in the vertical direction. The vertical tensile stress in the inboard leg �z is given by dividing this force by the total area of case, conduit and radial plate. In the vertical direction the components of the winding pack are in parallel, so the fractional extension of the superconductor is �z/EEz. /EEz. . This is not a true strain if the conductor is twisted. 

�z/EEz. This 

## 2.4.3. Stress criteria 

PROCESS assumes that the principal axes of the stress at the mid-plane are vertical, radial and tangential, so there are no shear stresses in this coordinate system. The von Mises stresses in the case and in the structural part of the winding pack are then given in terms of the radial, tangential and vertical stress components �r, �t, �z. Because the structural material inside the winding pack is assumed to take the form of radial and tangential webs (Fig. 7), the limiting von Mises stress in this zone is given by the larger of the two values: 

![](images/kovari2016.pdf-0006-13.png)

In both zones the peak von Mises stress always occurs at the inner radius. These peak values can each be constrained to be no more than the permissible value, specified by the user. 

## **3. Central solenoid (CS)** 

The central solenoid provides a loop voltage for plasma initiation and current ramp-up. For a pulsed reactor it also provides some of the voltage required to maintain fusion burn. Quench protection is not taken into account. The CS contains a fraction of steel structural material, whose allowable stresses are the same as for the TF coils (Section 2.4.3). Only steady-state stress is considered, with no allowance for fatigue due to cyclic stress, although fatigue is likely to be significant for a pulsed reactor. The hoop force is calculated using the approximation, 

![](images/kovari2016.pdf-0006-17.png)

where Bo and Bi are the fields at the outer and inner edge of the coil (calculated by the code, taking account of the field due to the 

plasma and all the other PF coils), ICS is the total central solenoid current, and RCS is the radius of the midline of the coil. The minimum cross-section of steel is calculated from the hoop force and the allowable stress. The current density in the superconductor is derived taking account of the area of steel and of helium coolant. The critical current density in the superconductor is calculated using same parameterisation for Nb3Sn described in Section 2.2 above, at beginning of flat-top and end of pulse. By comparing the actual current density and the critical current density, the temperature margin is derived at each time point. The smaller of these values is reported, and can be given a lower limit using a constraint. 

## **4. Poloidal field (PF) coils** 

The current per turn (i.e. the current in the conductor) is an input parameter. The number of turns in each coil is then calculated from the total current. The mass of superconductor in each coil is calculated from the cross-section, length, void fraction and density. The tangential tension (hoop) force is 

![](images/kovari2016.pdf-0006-22.png)

where R is the radius of the coil, BPF is the field at the inner edge, BPF2 is the field at the outer edge, and I is the peak current. The crosssectional area and mass of the structural material, assumed to be steel, in each PF coil is calculated using the maximum permissible tensile stress in the steel, and a specified fraction of the hoop force to be supported by the steel. The steel required is not included in the dimensions output. 

## **5. First wall, blanket and shield** 

The neutron wall loading is calculated by dividing the neutron power by the wall area. 

![](images/kovari2016.pdf-0006-26.png)

where Sarea, plasma surface area; Pneut, neutron fusion power per volume; V is the plasma volume and Farea, user-specified ratio between first wall area and plasma surface area. An upper limit can be imposed on the neutron wall load, which is a nominal quantity, only loosely representative of the actual neutron flux whose angular and energy spectra are important. The volumes of the first wall, blanket, shield and vacuum vessel are calculated using one of two models: they may be D-shaped in cross-section (Fig. 8), in which the inboard part is cylindrical, or both inboard and outboard parts may be defined by half-ellipses. In practice the thicknesses of the blanket and shield at the top are taken as the mean of the inboard and outboard thicknesses, while the vacuum vessel thickness is constant. 

![](images/kovari2016.pdf-0006-28.png)

**Fig. 8.** D-shaped model used for calculating volumes of blanket, shield and vacuum vessel: each is half a toroidal shell. The thickness varies between a and b. The inboard part is modelled as a cylinder. 

part 

![](images/kovari2016.pdf-0007-00.png)

**----- Start of picture text -----**<br>
M. Kovari et al. / Fusion Engineering and Design 104 (2016) 9–20 15<br>**----- End of picture text -----**<br>

![](images/kovari2016.pdf-0007-01.png)

**Fig. 9.** Power flows. LGH is low grade heat, rejected to the environment. Red lines represent neutrons. The dashed lines represent alternative options. The heat loads on the cryogenic components are not included in this diagram. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.) 

The mass of the blanket is determined by its volume and by its volumetric composition which by default includes titanium beryllide (TiBe12), lithium orthosilicate (Li4SiO4), helium and steel. 

## **Plant** 

## **balance** 

## **6.** 

## **power** 

6.1. 

## Reactor power 

The plant power flowchart is shown in Fig. 9. The cooling system consists of two parts – the part heated by “primary” heat, which contributes to electricity production, and the part heated by “low grade heat”, which does not. The options for how power is divided are shown in Table 2. The wall-plug efficiency of the heating and current drive system used is specified by the user. 

## 6.2. Power deposition 

The deposition of nuclear power in the reactor components are derived from the transport model for neutrons and secondary particles illustrated in Fig. 10. (The photon power on the first wall and divertor are derived from the radiation model described in (1).) The following functions provide a reasonable fit to the results for nuclear heating power in each component, as follows: 

for nuclear 

armour and first wall = fCFWPfusionMFW (48) blanket = fCblanket Pfusion (1 − e[−][aM][blanket] ) (49) shield = fCshieldPfusionMshielde[−][dL][blanket] e[−][fL][shield] (50) 

![](images/kovari2016.pdf-0007-15.png)

**Fig. 10.** The neutronic model used to derive heat deposition. The plasma is shown in pink, breeding blanket in red, shield in black, vacuum vessel (including ports) in grey, the TF coil in green and the CS and PF coils in yellow. The face of the first wall armour facing the plasma is blue. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.) 

fCcoilsPfusionMcoilse[−][bL][blanket] e[−][c][(][L][shield][+][L] _[vv]_[)] (51) 

## coils 

## = 

Type of heating Fraction where Pfusion is the fusion power, MFW is the mass of the first Nuclear heating 100% wall and its armour, Mblanket is the mass of the blanket, Mcoils Photon radiation is the mass of the TF and PF coils (heating in the CS is negliPumping power gible), Lblanket, Lshield and Lvv are the integrated line densities of Nuclear heating, 0% or 100% armour + first wall + blanket, the shield, and the vacuum vessel Pumping power Fusion power to � particles 0% or 100% respectively. Although the neutronics calculations give absolute Nuclear heating results, we have introduced a factor f to renormalise the power Photon radiation deposition making the assumption that 100% of the neutrons are Pumping power absorbed. 

## **7. Heat extraction from first wall and electricity generation** 

The heat from the primary coolant is transferred to a secondary coolant (working fluid), which is used to generate electricity in a power conversion cycle. The theoretical efficiency of conversion will be determined by the mean temperature at which heat is added to the working fluid by the primary coolant, and the temperature at which heat is rejected to the environment. However, the primary coolant temperature must be sufficiently low for the materials in the reactor structure to be below their practical limits. It is further necessary to minimise the power demand for pumping the primary and secondary coolants. Two models are available that combine the thermohydraulics of the blanket and first wall with the secondary cycle: a simple model and a detailed model, described below. PROCESS assumes that for a pulsed reactor the energy conversion system can be rapidly switched between operation and standby modes, without losing any additional thermal or electrical energy. The dwell time between pulses is input by the user. 

## 7.1. Simple model 

In this model, the power required to pump the primary coolant through each of the first wall, breeder zone, divertor, and shield, is calculated as a user input fraction of the thermal power deposited in the coolant from the reactor. The pumping power is deposited in the primary coolant. The default values for this fraction are 0.0005 for a water coolant, and 0.085 for a helium coolant, based on very preliminary calculations made for DEMO in EUROfusion. The separation of power into first wall, breeder zone, divertor, and shield allows a different coolant to be assumed for each system if required. The gross electric power is derived using a thermal efficiency based on the user’s choice of blanket. The options are watercooled lithium-lead (WCLL), helium-cooled lithium-lead (HCLL), or helium-cooled pebble-bed (HCPB). The resulting thermal efficiencies used are taken from studies that modelled Rankine cycles for the different options of a helium-cooled primary circuit with a top temperature of 500[◦] C [6], and a water-cooled primary circuit with a top temperature of 320[◦] C [7]. (For historical reasons in both cases the divertor was cooled by water with a top temperature of 150[◦] C in the helium-cooled reactor, and 250[◦] C for the water-cooled reactor.) Hence, no variation of efficiency with primary coolant temperature is possible using the simplified model; indeed, no temperatures are even considered in the model. The defined thermal efficiencies for the given blanket choices are shown in Table 3. For a helium-cooled reactor a penalty is applied as the coolant in the divertor has to operate at much lower temperature than the blanket, which may be the case because of the greater heat flux that has to be removed. Efficiencies differ depending on whether the heat from the divertor is utilised to preheat the secondary coolant, or is discarded as waste heat. Note that these thermal efficiencies are for the cycle only, describing the conversion of primary heat to gross electric power. The overall plant net power, accounting for recirculating power (including, for instance, the primary coolant pumping power demands), and hence the plant net efficiency, will be lower. 

**Table 3** Simple energy conversion model: secondary cycle thermal efficiency, defined as gross electric power divided by thermal power deposited in the secondary coolant. f = fraction of heat to the divertor. 

## 7.2. Detailed model: first wall 

The detailed model for heat extraction and power conversion calculates the maximum temperature of the first wall for given coolant inlet and outlet temperatures and channel dimensions. An iteration loop is utilised to decrease the thickness of the first wall, up to practical limits, if the temperature is found to be above the material limits. From this, the efficiency of the secondary cycle can be found from the coolant outlet temperature. The divertor heat is included in the primary cycle. The outlet temperature of the primary coolant is (a) for water, 20 K below the boiling point; (b) for helium, a user input. To calculate the maximum temperature of the first wall, the method of LeClaire is used [8,9]. In this approach, the first wall is assumed to consist of a set of parallel pipes, such that the surface is not flat, but a repeating semi-circular pattern. This geometry is unlikely to be used in practice, but allows a convenient analytical approach. The calculation of the peak temperature assumes that this occurs at the point closest to the plasma on each pipe and where the coolant temperature is at its maximum (which occurs at the top of the front face of the module). The temperature is calculated analytically by considering the conduction of heat through the pipe structure to the coolant, where heat is deposited both volumetrically from the incident neutron power, and upon the surface from radiative power. The heat transfer coefficient is calculated using the Sieder-Tate correlation. If the first wall temperature is found to be above specified limits, the thickness of the first wall is reduced, until it becomes too low to withstand the pressure of the coolant. (Note that if both criteria are satisfied using the initial inputs, the code does not vary the thickness of the first wall.) If the temperature and thickness requirements cannot both be satisfied the code returns an error. The peak hoop stress is given by Lamé’s solution for a thick-walled cylinder: 

![](images/kovari2016.pdf-0008-09.png)

where bfw and afw are the outer and inner radii of the first wall pipes, and P is the maximum coolant pressure. This must be less than the permissible stress. The plasma-facing side of the pipe may be eroded by sputtering, so an ad hoc adjustment is made, 

![](images/kovari2016.pdf-0008-11.png)

where werosion is the specified erosion thinning over the lifetime of the first wall. There is also a neutron fluence limit which determines the lifetime of the first wall and blanket – see Section 8.1 below. The power required to pump the coolant through the first wall and breeder zone is not trivial to calculate, as it depends sensitively on the diameter of the channels, and on the design of the feeder pipes and manifolds. The relevant algorithms are still under development. 

## 7.3. Detailed model: energy conversion 

From the coolant outlet temperature, the thermal efficiency of the power conversion cycle is determined. The user can choose between a steam Rankine cycle and a supercritical carbon dioxide Brayton cycle. If the Rankine cycle is chosen and the primary coolant is water, it is assumed that the cycle is similar to that of pressurised water reactors currently in operation. This cycle was modelled for a range of different top temperatures in order to find a correlation of cycle efficiency with temperature. The modelling method is described in [7]. A penalty of 0.042 was subtracted from the efficiency to account 

**Table 4** Fitting functions for secondary cycle efficiency. T1 and T3 are the maximum temperatures of the primary blanket and divertor coolants; T2 is the temperature of the secondary fluid at the inlet to the turbine. �� is a correction to represent the loss in cycle efficiency due to the lower temperature of the divertor coolant. 

Secondary cycle Primary coolant Efficiency (T2 in[◦] C) T2 range ([◦] C) T1–T2 ([◦] C) T3 ([◦] C) Steam Rankine Water 0.3720 ln (T2 + 273) − 2.0219 275–310 40 250 Helium 0.1802 ln (T2 + 273) − 0.7823 − �� 384–642 20 150 Supercritical CO2 Brayton Water or Helium 0.4347 ln (T2 + 273) − 2.5043 135–750 20 T3 = T2 pressure losses in the cycle using a more detailed model as a by the first wall area. In contrast, the divertor lifetime is estimated benchmark [7].. If the Rankine secondary is chosen but the primary using the particle and photon heat load: is helium, it is assumed that the cycle is a superheatedused,RankinebutRankinebutbut cycle.withwith anTheefficiencyresultsTheefficiencyresultsefficiencyresultsresults ofpenaltymodellingofpenaltymodellingofmodellingofof 0.0179byby Dostaltoto giveetet al.agree-[10]agree-[10][10] tlife,div =[�] qdiv[div] (56) at one point with a benchmark [6].. For the supercritical CO22 where �div is the allowable cumulative heat load and qdiv is the peak the correlation of efficiency with temperature is derived from heat load on the divertor. This formula will usually ensure that the of cycle modelling carried out by CCFE in collaboration with divertor lifetime reduces as the power into the divertor increases, industry. The derived fits are in Table 4.. For both Rankine cycles the but the absolute values derived should not be taken seriously. divertor heat is used in a separate heat exchanger to preheat the PROCESS calculates which of the two components has the feedwater, while for CO2 cycle2 cycle cycle it is used in the main heat exchanger. shorter lifetime. For example, if the divertor has a shorter life, one both cases the divertor heat is counted as primary heat, and is or more outages, noutages, may be required for divertor replacement included in the calculation of the efficiency. within the lifetime of a single blanket. The unavailability is given 

for pressure losses in the cycle using a more detailed model as a benchmark [7].. If the Rankine secondary is chosen but the primary coolant is helium, it is assumed that the cycle is a superheatedsteamwere used,RankinebutRankinebutbut cycle.withwith anTheefficiencyresultsTheefficiencyresultsefficiencyresultsresults ofpenaltymodellingofpenaltymodellingofmodellingofof 0.0179byby Dostaltoto giveetet al.agree-[10]agree-[10][10] ment at one point with a benchmark [6].. For the supercritical CO22 cycle, the correlation of efficiency with temperature is derived from results of cycle modelling carried out by CCFE in collaboration with industry. The derived fits are in Table 4.. For both Rankine cycles the divertor heat is used in a separate heat exchanger to preheat the feedwater, while for CO2 cycle2 cycle cycle it is used in the main heat exchanger. In both cases the divertor heat is counted as primary heat, and is included in the calculation of the efficiency. 

by: 

## **8. Availability** 

The availability of a power plant is crucial for generating electricity economically. A new availability module has recently been added. Our definitions are as follows. Availability is the fraction of the time in which the plant is operating normally. For a pulsed reactor the dwell time in between pulses is considered to be normal operation. Capacity factor is the electrical energy delivered to the grid over the lifetime of the plant, divided by the maximum rate at which electrical power can be delivered. These are the same for a steady-state, fixed power reactor, but for a pulsed reactor capacity factor will be less than availability. (No allowance has been made for load following–reduction of output at times of low demand.) The total availability is derived from the addition of the planned and unplanned availabilities, Uplanned and Uunplanned, and a term to take account of the overlap: 

## Availability 

![](images/kovari2016.pdf-0009-09.png)

![](images/kovari2016.pdf-0009-10.png)

The cost of electricity (COE) is the mechanism by which the availability is fed back into the PROCESS optimiser. For a pulsed reactor the duty cycle Fdc is calculated using the pulse length and the time between pulses (dwell time). The capacity factor is AtotFdc. The code uses this value and cost data (including the capital cost) to estimate the cost of electricity for the plant. The lifetime of the components of a pulsed reactor may be substantially reduced because of fatigue, but this is not currently taken 

U = tmain , (57) top + tmain where top is the total operational time, and tmain is the total time required for maintenance, both over the entire life of the machine. The operational time top is given by tlife,blanket (or tlife,div, if lower). The total planned unavailability is then: 

U 

Uplanned = tlife,blanketnoutages + ntoutagesdiv,reptairdiv +,repairtcom +pletetcomplete,repair ,repair , (58) where tdiv,repair is the time to replace the divertor and tcomplete,repair is the time taken to replace both the blanket and the divertor. The time to replace the blanket and divertor are estimated by Crofts et al. [11], who studied the influence of the number of remote handling systems on the length of scheduled maintenance. A fit to their results gives the time to repair both the blanket and divertor 

as: 

![](images/kovari2016.pdf-0009-16.png)

where N is the number of remote handling systems working in parallel. The extra two months are to allow the dose-rate to reduce to an acceptable level before remote handling operations start, and to allow pump-down and preparation for operation at the end of the shutdown. Crofts et al. comment that to replace the blanket one must remove the divertor also. On the other hand it is possible to replace the divertor alone and this is estimated to take 70% of the time taken to repair the blanket. 

## Unplanned 

## downtime 

## 8.2. 

## Planned unavailability 

The planned unavailability in PROCESS is linked to the lifetimes of the blanket and divertor and the time taken to replace them. The lifetime for the blanket is based only on the neutron flux, using the following very loose scaling: 

![](images/kovari2016.pdf-0009-23.png)

where �blanket is the allowable fast neutron fluence and qblanket is the nominal neutron wall load, defined as the fusion power divided 

Each subsystem is represented by a simple model that tries to capture the degradation of reliability when approaching operational and technological limits. This increases the risk of unplanned downtime as the design margins are reduced. This approach is well suited to a systems code, as it ensures that the optimiser will choose a design point that has adequate design margins whenever possible. The total unplanned unavailability is the sum of the unplanned unavailabilities for each system. For the heating and current drive systems the unplanned unavailability is taken as 2%. This is far less than currently operating systems – large improvements will need to be made in order to meet the requirements of a power plant. The failure rate for the steam turbine system can be estimated from experience [12] 

Atot = 

into account. 

8.1. 

the nominal 

N 

≤ Nref 

N 

as 9.39 × 10[−][5] failures per hour, with an associated average repair time of 96 h. 

## 8.2.1. Magnets 

It is likely that the chance of a quench in a magnet is the largest driver of the risk of unplanned unavailability, and this may depend on the temperature margin in the TF coils – the difference between the actual temperature and the critical temperature of the superconductor (Section 2.2). The unplanned unavailability of the magnet system is given by: 

## magnet 

![](images/kovari2016.pdf-0010-08.png)

U = �main + �bquench 

where �main is the maintenance time for the magnet system and �bquench is the estimated time between quenches of the magnet This is calculated as follows. 

## system. 

![](images/kovari2016.pdf-0010-12.png)

**----- Start of picture text -----**<br>
�bquench<br>⎧⎪⎪⎪⎪ LMag Tmarg > Tmarcg,min<br>= Tmarg − Tmarg,min c Tmarg,min<br>⎨⎪⎪⎪⎪ LMag Tmarg,min 1 − c Tmarg,min < Tmarg < c<br>⎩ 0 Tmarg < Tmarg,min<br>(61)<br>**----- End of picture text -----**<br>

where LMag, lifetime when design margin is large; Tmarg, superconductor temperature margin; Tmarg,lim, temperature margin lower limit; c, determines the temperature margin at which lifetime starts to decline. 

The suggested range for c is 0.9–0.99. Fig. 11 shows an example for a minimum temperature margin of 1.5 K. The magnet never quenches if the temperature margin is above a critical value, and it will not operate at all below the temperature margin lower limit. In between, there is a finite risk of quench. 

blanket replacements, N, is determined by the blanket lifetime which is based on the neutron flux (Section 8.1 above): 

![](images/kovari2016.pdf-0010-16.png)

This approach allows PROCESS to improve the availability of the blanket by increasing the neutron flux, until the planned downtime starts to dominate. This is counter-intuitive, but is correct if one assumes that the neutron flux affects the total life of the blanket but not the cycle life. 

The life of the blanket is expressed in terms of a reference number of cycles Nref. The probability of failure in one pulse cycle before the reference cycle life is a constant, pf. During the reference lifetime the instantaneous availability after n cycles since the blanket was last repaired or replaced is: 

![](images/kovari2016.pdf-0010-19.png)

where tmain is the time required to repair the blanket, tcycle is the length of one pulse cycle. After the reference lifetime we assume that the reliability of the blanket starts to decline, so the instantaneous availability is given by: 

length of that the 

![](images/kovari2016.pdf-0010-22.png)

where NU is the cycle when the blanket fails with 100% probability. The availability decreases linearly beyond the reference lifetime. Integrating the instantaneous availability gives the mean availability over the planned cycle life N: 

![](images/kovari2016.pdf-0010-24.png)

a0 

![](images/kovari2016.pdf-0010-26.png)

The availability of the divertor is estimated in a similar way. 

## 8.2.3. Vacuum system 

## 8.2.2. First wall, blanket and divertor 

The first wall and blanket will be subject to neutron irradiation during operations. In addition, the first wall will be exposed to photon radiation, and particle bombardment by ions and neutral atoms. The unplanned downtime is based on the number of cycles a blanket set experiences before replacement. (This model is restricted to pulsed reactors.) The number of cycles between planned 

![](images/kovari2016.pdf-0010-31.png)

**Fig. 11.** Illustration of the approach used to estimate unplanned failures: estimated time between quenches in the TF coils. 

The vacuum system will be extensive and complex, as it must capture unburnt fuel, helium ash and impurities, as well as evacuating the reactor before operation. PROCESS assumes that there is a pumping duct between every pair of adjacent TF coils, and that cryopumps are used, so that for each duct there are two pumps that can be regenerated alternately. During planned maintenance broken pumps can be replaced, so the calculation of unplanned downtime is done for an operational period between planned shutdowns and then multiplied by the number of operational periods in the machine lifetime. The total operational time between 

shutdowns 

is 

![](images/kovari2016.pdf-0010-36.png)

Nshutdowns + 

where top,total is the total operational time in the life of the machine. The failure rate for a cryopump is taken from [13]: 

## The 

![](images/kovari2016.pdf-0010-40.png)

If the total number of pumps is Ntot, then the probability of n failures in the operational period top is: 

P (n) = Ntot (toppf )[n][�] 1 − toppf �Ntot−n (68) n � � where Ntot are the binomial coefficients. If the number of failn � � ures exceeds the number of redundant pumps then it will cause 

time between 

additional unplanned downtime. The total downtime over the entire operational period is then 

## entire operational 

![](images/kovari2016.pdf-0011-04.png)

where tmain is the unscheduled maintenance time for a vacuum pump, and Nr is the number of redundant pumps. If there are several redundant pumps then this unscheduled downtime can be reduced to a negligible level. Then the unplanned unavailability is 

![](images/kovari2016.pdf-0011-06.png)

The lower limit Umin allows for common mode failures that affect 

## several pumps. 

## **9. Application to DEMO** 

A model for a pulsed reactor generating 500 MW net electricity has been obtained using PROCESS, referred to as DEMO A [1]. Some of the engineering aspects are discussed here, and illustrated in Fig. 1. The engineering constraints selected are listed in Table 5. The machine is large – the outside dimensions of the cryostat are 36 m (diameter) × 29 m (height). The TF coils allow the neutral beam to be tangent to the plasma axis or even further out, allowing optimum current drive to be achieved if required. The power flows are summarised in Table 6, and some thermodynamic parameters are in Table 7. The 40% wall plug efficiency assumed for the heating system contrasts with achieved values of about 25% [14]. 

**Table 5** 

Some of the engineering constraints applied in the DEMO A model. 

## **Table 7** 

Thermodynamic and energy parameters. 

![](images/kovari2016.pdf-0011-18.png)

**Fig. 12.** Dependence of plasma major radius, total TF coil cross-section and superconductor cross-section on normalised maximum permissible current density in TF coil. Figure of Merit is major radius. Fig. 12 illustrates the way in which multiple constraints can conspire to limit the space for variability of the optimised model. Even when the ratio of operating current to critical current in the TF coils is increased by a factor of five, the total coil cross-section decreases only a little, because of the large non-superconducting area needed for copper stabiliser, insulation, and, especially, structural support. The result is that the plasma major radius reduces by just 12 cm, or 1.4%. This shows that to make effective use of improved superconductors, stronger structural materials would also be required. Another illustration of this effect of multiple constraints is shown in Fig. 13. As the output power requirement is increased, the code increases the seeded impurity fraction, in order to increase the radiation fraction, thus maintaining the power per unit length into the divertor zone at a constant value. The injected power was fixed in this run, so the electric power required for current drive drops as a fraction of gross electric power. As the machine gets bigger, 

![](images/kovari2016.pdf-0012-02.png)

**Fig. 13.** Dependence of the density of the seeded impurity (xenon), radiation power, major radius and recirculating electric power on net electric output required. Figure of Merit is major radius. 

the increased space allows the toroidal field to increase slightly. Because of these factors and others, the major radius grows by only 9%, even though the power output has increased by a factor of 2.2. Fully annotated input and output files for these models are available in the Supplementary Data accompanying this paper. 

## **10. Discussion and future work** 

A new neutronics module is being developed [15]. The timedependent code FATI was used to simulate the depletion of breeding and neutron multiplying isotopes in an HCPB blanket. 594 models were run, covering the parameter space of lithium fraction,[6] Li enrichment, and blanket thickness. The results were fitted with analytical expressions, which will be incorporated into PROCESS. In the future it will be important to obtain improved parametric expressions for energy multiplication, and for nuclear energy deposition in the coils, with and without neutral beam ducts. New estimates of the approximate likely cost of building a tokamak fusion power station, on the assumption that the outstanding issues can be resolved, are being developed for PROCESS. 

PROCESS allows the user to choose which constraints to impose and which to ignore, so when evaluating the results it is vital to study the list of constraints used. Work is underway on the sensitivity of PROCESS results to variations in input parameters, and 

sitivity 

on the robustness of the optimiser in finding global solutions. New algorithms submitted by collaborators can be incorporated – for example safety, first wall erosion, and fatigue life will be crucial and are not yet taken into account. The PROCESS homepage is www. ccfe.ac.uk/powerplants.aspx. 

## **Acknowledgments** 

We would like to thank H. Latham for the Thermoflow modelling, J. Shimwell and P. Pereslavtsev for the neutronics model, and C. Bachmann, F. Maviglia, and E. Surrey for helpful comments. This work has been carried out within the framework of the EUROfusion Consortium and has received funding from the Euratom research and training programme 2014–2018 under grant agreement No. 633053 and from the RCUK Energy Programme [grant number EP/I501045]. To obtain further information on the models underlying this paper please contact the authors, or PublicationsManager@ccfe.ac.uk. The views and opinions expressed herein do not necessarily reflect those of the European Commission. 

## **Appendix** 

## **Supplementary** 

## **data** 

## **A.** 

Supplementary data associated with this article can be found, in the online version, at http://dx.doi.org/10.1016/j.fusengdes.2016. 01.007. 

## **References** 

- [1] M. Kovari, R. Kemp, H. Lux, P. Knight, J. Morris, D.J. Ward, PROCESS: a systems code for fusion power plants – Part 1: Physics, Fusion Eng. Des. 89 (12) (2014) 3054–3069, http://www.sciencedirect.com/science/article/pii/ S0920379614005961. 

- [2] E. Surrey, A. Benn, I. Jenkins, M. Porton, W. Timmis, A. Turner, The influence of neutral beam optimization for DEMO on injector design, Fusion Eng. Des. 87 (4) (2012) 373–383, http://www.sciencedirect.com/science/article/pii/ S0920379612002311. 

- [3] A. Devred, ITER Nb3Sn Critical Surface Parameterization, 2008, https://user. iter.org/?uid=2MMF7J. 

- [4] N. Mitchell, DDD11-7: Conductors (2NBKXY v1.2), 2009, https://user.iter.org/ ?uid=2NBKXY. 

- [5] R. Reid, H.L. Barr, C.G. Bathke, J.M. Brooks, R.H. Bulmer, A. Busigin, et al., ETR/ITER Systems code, ORNL/FEDC-87/7, 1988, pp. 200. 

- [6] M. Porton, Z. Vizvary, H. Latham, P. Clarkson, Assessment of DEMO relevant helium-cooled balance of plant technology, EFDA ~~D 2~~ M4XFP, 2012. 

- [7] H. Latham, J. Charlton, M. Kovari, C. Harrington, C. Kiely, Z. Vizvary, Definition of Steam Based Power Conversion System for Fusion DEMO reactor, EFDA report, 2013, https://user.efda.org/?uid=2M97B7. 

- [8] R.J. LeClaire, Methods of first wall structural analysis with application to the Long Pulse Commercial Tokamak reactor design PFC/RR-84-9, DOE/ET/51013-123, Plasma Fusion Center, Department of Nuclear Engineering, MIT, 1984, http://www.psfc.mit.edu/library1/catalog/reports/ 1980/84rr/84rr009/84rr009 full.pdf. 

- [9] R.J. LeClaire, J.E. Meyer, The impact of thermal fatigue and other design limits on pulsed commercial tokamak reactor design, J. Fusion Energy 4 (5) (1985) 353–364, http://link.springer.com/10.1007/BF01058360. 

- [10] V. Dostal, M.J. Driscoll, P. Hejzlar, A supercritical carbon dioxide cycle for next generation nuclear reactors, MIT-ANP-TR-100, 2004. 

- [11] O. Crofts, J. Harman, Maintenance duration estimate for a DEMO fusion power plant, based on the EFDA WP12 pre-conceptual studies, Fusion Eng. Des. 89 (9–10) (2014) 2383–2387, http://www.sciencedirect.com/science/article/pii/S0920379614000398. 

- [12] Dongiovanni DN. RAMI analysis for DEMO: Helium Cooled Pebble Bed cooling system, EFDA ~~D 2~~ KZVUG v1.0. 

- [13] L.C. Cadwallader, Vacuum system operating experience review for fusion applications, EGG-FSP-11037, ITER/US/93/TE/SA-18, 1994, http://www.osti. gov/scitech/servlets/purl/10167503. 

- [14] P. Franzen, U. Fantz, On the NBI system for substantial current drive in a fusion power plant: status and R&D needs for ion source and laser neutralizer, Fusion Eng. Des. 89 (November (11)) (2014) 2594–2605, http://www. sciencedirect.com/science/article/pii/S0920379614004335. 

- [15] J. Shimwell, M. Kovari, S. Lilley, S. Zheng, L. Morgan, L. Packer, et al., A parameter study of time-varying tritium production in solid-type breeder blankets, Fusion Eng. Des. (2015), http://dx.doi.org/10.1016/j.fusengdes.2016. 01.011. 

