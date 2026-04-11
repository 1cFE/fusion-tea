---
source: "https://www.osti.gov/servlets/purl/901970/"
source_type: "url"
extracted_at: "2026-04-06T05:34:15.291370+00:00"
content_hash_sha256: "4f2be650aa675826ddc4c60eab704b79b707d281fd7a636412a32e0510576b86"
backend: "pdf_pipeline"
---

### **SANDIA REPORT**

SAND2006-7148
Unlimited Release
Printed October 2006

# **Z-Inertial Fusion Energy: Power Plant** **Final Report FY 2006**

Jason T. Cook, Gary E. Rochau, Benjamin B. Cipiti, Charles W. Morrow, Salvador B.
Rodriguez, Cathy O. Farnum, Marcos A. Modesto-Beato, Samuel Durbin, James D.
Smith, Paul E. McConnell, Dannelle P. Sierra, Craig L. Olson, Wayne Meier, Ralph
Moir, Per F. Peterson, Philippe M. Bardet, Chris Campen, James Franklin, Haihua
Zhao, Gerald L. Kulcinski, Mark Anderson, Jason Oakley, Ed Marriott, Jesse
Gudmundson, Kumar Sridharan, Riccardo Bonazza, Virginia L. Vigil, Mohamed A.
Abdou, Lothar Schmitz, Alice Ying, Tomas Sketchley, Yu Tajima, Said I. Abdel-Khalik,
Brian Kern, Said.M. Ghiaasiaan

Prepared by
Sandia National Laboratories
Albuquerque, New Mexico 87185 and Livermore, California 94550

Sandia is a multiprogram laboratory operated by Sandia Corporation,
a Lockheed Martin Company, for the United States Department of Energy’s
National Nuclear Security Administration under Contract DE-AC04-94AL85000.

Approved for public release; further dissemination unlimited.

Issued by Sandia National Laboratories, operated for the United States Department of Energy
by Sandia Corporation.

## NOTICE:  This report was prepared as an account of work sponsored by an agency of the

United States Government. Neither the United States Government, nor any agency thereof,
nor any of their employees, nor any of their contractors, subcontractors, or their employees,
make any warranty, express or implied, or assume any legal liability or responsibility for the
accuracy, completeness, or usefulness of any information, apparatus, product, or process
disclosed, or represent that its use would not infringe privately owned rights. Reference herein
to any specific commercial product, process, or service by trade name, trademark,
manufacturer, or otherwise, does not necessarily constitute or imply its endorsement,
recommendation, or favoring by the United States Government, any agency thereof, or any of
their contractors or subcontractors. The views and opinions expressed herein do not
necessarily state or reflect those of the United States Government, any agency thereof, or any
of their contractors.

Printed in the United States of America. This report has been reproduced directly from the best
available copy.

Available to DOE and DOE contractors from
U.S. Department of Energy
Office of Scientific and Technical Information
P.O. Box 62
Oak Ridge, TN 37831

Telephone: (865) 576-8401
Facsimile: (865) 576-5728
E-Mail: reports@adonis.osti.gov
Online ordering: http://www.osti.gov/bridge

Available to the public from
U.S. Department of Commerce
National Technical Information Service
5285 Port Royal Rd.
Springfield, VA 22161

Telephone: (800) 553-6847
Facsimile: (703) 605-6900
E-Mail: orders@ntis.fedworld.gov
Online order: http://www.ntis.gov/help/ordermethods.asp?loc=7-4-0#online

SAND2006-7148
Unlimited Release
Printed October 2006

## **Z-Inertial Fusion Energy: Power Plant Final** **Report FY06**

Jason T. Cook [1], Gary E. Rochau [1], Benjamin B. Cipiti [1], Charles W. Morrow [1], Salvador B.
Rodriguez [1], Cathy O. Farnum [1], Marcos A. Modesto-Beato [1], Samuel Durbin [1], James D. Smith [1],
Paul E. McConnell [1], Dannelle P. Sierra [1], Craig L. Olson [1], Wayne Meier [2], Ralph Moir [2], Per F.
Peterson [3], Philippe M. Bardet [3], Chris Campen [3], James Franklin [3], Haihua Zhao [3], Gerald L.
Kulcinski [4], Mark Anderson [4], Jason Oakley [4], Ed Marriott [4], Jesse Gudmundson [4], Kumar
Sridharan [4], Riccardo Bonazza [4], Virginia L. Vigil [4], Mohamed A. Abdou [5], Lothar Schmitz [5], Alice
Ying [5], Tomas Sketchley [5], Yu Tajima [5], Said I. Abdel-Khalik [6], Brian Kern [6], .M. Ghiaasiaan [6]

1 Sandia National Laboratories, P.O. Box 5800, Albuquerque, NM 87107, USA
2 Lawrence Livermore National Laboratories, 7000 East Ave., Livermore, CA 94550, USA
3 University of California, 4111 Etcheverry Hall, Berkeley, CA 94720-1730, USA
4 University of Wisconsin, 1415 Engineering Dr., Madison, WI 53706-1691, USA
5 University of California, 44-114 ENG IV, Los Angeles, CA 90095-1597, USA
6 Georgia Institute of Technology, 801 Ferst Dr., Atlanta, GA 30332-0405, USA

Jason T. Cook, Editor
Sandia National Laboratories
P.O. Box 5800
Albuquerque, New Mexico 87185-MS1076

**Abstract**

This report summarizes the work conducted for the Z-inertial fusion energy
(Z-IFE) late start Laboratory Directed Research Project. A major area of focus was
on creating a roadmap to a z-pinch driven fusion power plant. The roadmap ties ZIFE into the Global Nuclear Energy Partnership (GNEP) initiative through the use of
high energy fusion neutrons to burn the actinides of spent fuel waste. Transmutation
presents a near term use for Z-IFE technology and will aid in paving the path to
fusion energy. The work this year continued to develop the science and engineering
needed to support the Z-IFE roadmap. This included plant system and driver cost
estimates, recyclable transmission line studies, flibe characterization, reaction
chamber design, and shock mitigation techniques.

###### **ACKNOWLEDGMENTS**

The authors would like to acknowledge the support of the Laboratory Directed Research and
Development Projects 81753 and 102362 for this research.

# CONTENTS

1. Executive Summary ......................................................................................................... 13

2. Z-Inertial Fusion Energy Roadmap ................................................................................. 15
   - 2.1 The Path to Transmutation and Commercial Power .................................................. 17
     - 2.1.1 Critical Path ...................................................................................................... 17
     - 2.1.2 Target Yield ...................................................................................................... 17
     - 2.1.3 Recyclable Transmission line and Target Manufacturing Plant ......................... 18
     - 2.1.4 Driver Development .......................................................................................... 18
     - 2.1.5 Automation and Repetitive Rate ........................................................................ 18
   - 2.2 Z-IFE and the Global Nuclear Energy Partnership .................................................. 18

3. Z-IFE Power Plant Systems Analysis ............................................................................. 21
   - 3.1 Cost Models for Z-IFE ........................................................................................... 21
     - 3.1.1 Systems Economic Modeling for Z-IFE [5] ..................................................... 21
     - 3.1.2 Estimated Cost for a 1 PW LTD Driver ........................................................... 33
   - 3.2 Power Conversion Systems for the Power Plant ..................................................... 33
     - 3.2.1 Super Critical CO₂ Brayton Cycle .................................................................... 33
     - 3.2.2 Rankine, Helium Brayton, and Combined Cycles ............................................. 34
     - 3.2.3 An Analysis of the Rankine, Brayton, and Combined Cycles ........................... 36
   - 3.3 Tritium .................................................................................................................... 38
     - 3.3.1 Tritium Permeation [22] .................................................................................... 38
     - 3.3.2 Future Tritium Research .................................................................................... 42
   - 3.4 Recyclable Transmission Line (RTL) and Flibe ..................................................... 43
     - 3.4.1 Characterization of Frozen Salt Properties [28] ............................................... 43
     - 3.4.2 Interaction of Ferritic Steel Vapor and Flibe [28] ............................................ 44
     - 3.4.3 Chamber Dynamics [28] .................................................................................... 50
   - 3.5 Automation ............................................................................................................. 57
     - 3.5.1 Plant Layout ...................................................................................................... 57
     - 3.5.2 Loading New RTLs and Unloading used RTLs ................................................ 58
     - 3.5.3 Future Work ...................................................................................................... 59

4. Chamber Design and Shock Mitigation ........................................................................... 60
   - 4.1 Shock Mitigation .................................................................................................... 61
     - 4.1.1 Shock Mitigation Roadmap ............................................................................... 61
     - 4.1.2 ALEGRA Modeling of Gas Mitigation ............................................................. 62
     - 4.1.3 Single and Two-Phase Shock Mitigation (liquid curtains) ................................ 71
     - 4.1.4 Experimental Investigation of Chamber Liquid Structure Response [50] ......... 72
     - 4.1.5 Void Fraction Distribution in a Two-Phase (Gas-Liquid) Jet [56] ................... 83
     - 4.1.6 Shock Mitigation in Voided Liquids for Chamber Protection [57] ................... 99
     - 4.1.7 Aerosol Shock Mitigation ................................................................................ 109
   - 4.2 Chamber Design ................................................................................................... 115
     - 4.2.1 Thick Liquid Curtain Chamber Design Concept and RTL Design [5] ............ 115
     - 4.2.2 First Wall Chamber Design Concept with Aerosol Mitigation ....................... 126
     - 4.2.3 Chamber Materials .......................................................................................... 128
     - 4.2.4 Thermal Annealing ......................................................................................... 133
     - 4.2.5 Fatigue Analysis of F82H Steel ...................................................................... 135

5. Conclusion.................................................................................................................. 141

6. References .................................................................................................................. 143

Distribution ................................................................................................................................. 149

## FIGURES

Figure 2.1: Z-IFE Roadmap for Z-pinch Driven IFE Transmutation and Commercial
Power. .................................................................................................................. 16
Figure 2.2: An advanced closed fuel cycle with transmutation. ................................................... 19
Figure 3.1: Target yield versus driver energy. Fit through three calculated cases is shown. ...... 22
Figure 3.2: Dynamic hohlraum target gain versus driver energy. ................................................ 23
Figure 3.3: Driver energy per chamber required to achieve a net plant power of 1000 MWe
versus chamber rep-rate. ....................................................................................... 25
Figure 3.4: COE versus chamber rep-rate for 1000 MWe plants with 1-10 chambers per
plant. ...................................................................................................................... 26
Figure 3.5: COE and chamber rep-rate versus driver energy for 1000 MWe plants with 1 or
3 chambers. ............................................................................................................ 27
Figure 3.6: COE versus rep-rate for two-chamber plants with various net electric powers. ........ 28
Figure 3.7: Stochastic Distribution of Capital Cost for a 1 PW Driver. ..................................... 29
Figure 3.8: Sizing Sketch for Driver System. .............................................................................. 29
Figure 3.9: Purchase Price for Tanks. ......................................................................................... 30
Figure 3.10: Stochastic Distribution of LTD Cavity Costs – 12600 Cavity Case. ..................... 31
Figure 3.11: Chemical Engineering Plant Cost Index .................................................................. 32
Figure 3.12: A schematic of a supercritical CO₂ Brayton cycle (left), and an efficiency
verse turbine inlet temperature plot. ..................................................................... 34
Figure 3.13: A schematic of the standard Brayton cycle. ........................................................... 35
Figure 3.14: A schematic of the combined cycle. ........................................................................ 36
Figure 3.15: Brayton and combined cycle efficiency verse temperature. .................................... 38
Figure 3.16: Flibe Circulation Process Sketch. ........................................................................... 39
Figure 3.17: Conceptual 1 GW Fusion Power Plant Layout. ...................................................... 40
Figure 3.18: Results of DIFFUSE Code. ..................................................................................... 41
Figure 3.19: Z-Box flibe handling facility. .................................................................................. 44
Figure 3.20: Flibe and Na₂MgCl₄ phase diagram. ..................................................................... 45
Figure 3.21: Experimental Set-up showing 3" nickel crucible bedded in heater plate
(center) with detachable heater connections (left), glass-shielded transmission line
elements leading to the capacitor bank (in green), and the centrally mounted wire mesh
(purple). .................................................................................................................. 46
Figure 3.22: The video frame showing the plasma discharge (left) and the immediate
following frame (right). ......................................................................................... 47
Figure 3.23: (Left) Oblique view of inner pyrex cylinder wall (the large salt droplet is 300
μm wide). (Right) A Perpendicular view showing salt and embedded steel droplets. ........ 48
Figure 3.24: EDX surface analysis: 500μm, 2μm retion free of iron droplets. .......................... 48
Figure 3.25: EDX spectrum of 2 μm steel droplet indicated in Figure 3.23(right). ................... 49
Figure 3.26: Region containing clusters of small steel droplets (0.1–1 μm typical size). .......... 49
Figure 3.27: Schematic/image of HICAT device. ........................................................................ 51
Figure 3.28: Typical argon plasma density and temperature evolution from spectroscopic
line ratio measurements. ....................................................................................... 52
Figure 3.29: Emission spectrum with salt and ferritic steel present. ........................................... 53
Figure 3.30: Time resolved measurement of species density. ...................................................... 54
Figure 3.31: Iron I line intensities in pulse 2/pulse 1 versus the relative chlorine density in
the plasma, as evaluated from the 522 nm Cl II emission line. ............................. 54

## List of Figures

Figure 3.32: Time evolution of the discharge current and Fe I (385.8 nm) line intensity................. 54

Figure 3.33: Calculated three-body recombination rate constant for filbe components and iron in Argon gas (T= 5000K)................................................................................................... 56

Figure 3.34: Three-body recombination rate constant for NA, Mg, and Fe with Cl in Helium gas (T=5000K).......................................................................................................... 56

Figure 3.35: Major Stages in transferring RTL ................................................................................. 58

Figure 4.1: Illustration of a possible experimental setup on ZR.................................................... 62

Figure 4.2: Semi-coarse laser mesh.................................................................................................. 63

Figure 4.3: Spatial evolution of the argon spark as a function of time (UCSD laser data courtesy of Sivanandan S. Harilal)..................................................................................... 65

Figure 4.4: Argon 2D (left) and 3D (right) Z-IFE chamber meshes................................................ 68

Figure 4.5: Argon temperature (K) at 1 and 500ns........................................................................... 68

Figure 4.6: Argon Zbar (-) at 1 and 500 ns....................................................................................... 68

Figure 4.7: Argon Rosseland opacity (m²/kg) at 1 and 500 ns........................................................ 68

Figure 4.8: Argon absorption opacity (m²/kg) at 1 and 500 ns....................................................... 68

Figure 4.9: Argon pressure (Pa) at 1 and 500 ns.............................................................................. 69

Figure 4.10: Electron thermal conductivity (W/m-K) at 1 and 500 ns............................................ 69

Figure 4.11: EFLUX and PFLUX as functions of time during first 15 ns of the transient............. 70

Figure 4.12: Top view of a liquid curtain design for the Z-IFE Vessel........................................... 71

Figure 4.13: Nozzle assembly housing. Various nozzles can be inserted in the modular bay......................................................................................................................................... 73

Figure 4.14: Nozzle geometries. Phase 1 nozzle is made of 38 sections similar to the section depicted here; and phase 2 is made of 24 sections. The void fraction is 49% for phase 1 and 74% for phase 2........................................................................................... 74

Figure 4.15: Pictures of the full nozzle assemblies, with a yard stick for reference. a) is phase 1, and b) is phase 2................................................................................................ 75

Figure 4.16: Phase 2 nozzle in operation inside the VHEX chamber. Horizontal rod entering from left supports the explosive charge located on a stalk centered in the array 10 cm above the rod........................................................................................................... 76

Figure 4.17: Raw pressure measurements for Phase 1 nozzle for various HE masses. These measurements have not been corrected for vibrations which are, in certain cases, quite significant. a) corresponds to detonator alone, b) to an EBW with 2.5g of HE and c) to 5g of HE................................................................................................................... 78

Figure 4.18: Sequences of pictures from Phase 1 jets with an increasing mass of explosives. a) is a single detonator, b) a detonator with 2.5g of HE, c) an EBW with 5g of HE and d) an EBW with 23 g of HE. At the exception of d), the sequences are started with the apparition of gas venting through the jets and ended when the chamber has been cleared. The time intervals are also identical (except for d)).......................... 79

Figure 4.19: Pressure measurements for Phase 2 nozzle for various HE masses. Pressure measurement with a single EBW and no HE is not displayed because strong vibrations in the pressure sensor mount rendered data unusable.................................................... 80

Figure 4.20: Sequence of pictures from Phase 2 with increasing amount of HE. The first frames correspond to the first picture where venting is observed, about 1 ms following the detonation. Time intervals are identical and times noted in bold italic are similar to those of Figure 4.18............................................................................................................. 82

Figure 4.21: Coordinate system at nozzle exit................................................................................... 84

Figure 4.22: Experimental setup highlighting the flow conditioner and nozzle.............................. 85

Figure 4.23: Collapsed liquid thickness versus x-position...........................................................................86
Figure 4.24: Void Fraction versus distance from nozzle...............................................................................87
Figure 4.25: Void fraction versus distance from nozzle................................................................................88
Figure 4.26: Void fraction versus distance from nozzle................................................................................88
Figure 4.27: Slip ratio versus distance from nozzle......................................................................................90
Figure 4.28: Slip ratio versus distance from nozzle......................................................................................90
Figure 4.29: Measured void fraction versus correlation void fraction...........................................................92
Figure 4.30: Void fraction comparison..........................................................................................................93
Figure 4.31: Measured void fraction versus correlation void fraction...........................................................94
Figure 4.32: Void fraction comparison..........................................................................................................95
Figure 4.33: Measured void fraction versus correlation void fraction...........................................................96
Figure 4.34: Void fraction comparison..........................................................................................................97
Figure 4.35: Apparatus for simulating the shock mitigation response in the lower portion of the chamber..................................................................................................................................101
Figure 4.36: Open cell-cell morphology of the 40ppi aluminum foam used to create the bubble distribution..............................................................................................................................101
Figure 4.37: Water with 15% void fraction of Ar in a mock-up of the shock tube test section with transparent walls- the width of the test section is 25.4 cm...........................................102
Figure 4.38: Mineral oil with 5% void fraction of Ar in a mock-up of the shock tube test section with transparent walls- the width of the test section is 25.4 cm...........................................102
Figure 4.39: Pressure as a function of radius for the line of sight from the target to coolant pool at the bottom of the chamber calculated using BUCKY..........................................................103
Figure 4.40: Pressure traces for M=1.4 from a transducer located 3.5 cm below the surface of the pool for 0, 5, 10, and 15 % argon void fraction....................................................................105
Figure 4.41: Shaving cream foam photographs in shock tube, (a) side-view during fill, (b) top view profile, and (c) top view post shot.....................................................................................106
Figure 4.42: Pressure Traces from a transducer located 1 m below the surface of the shaving cream foam.....................................................................................................................107
Figure 4.43: SEM images for a sample in the water pool with no void fraction shown at increasing levels of magnification.................................................................................................108
Figure 4.44: SEM images for a sample in the water pool with 15% argon void fraction shown at increasing levels of magnification.................................................................................108
Figure 4.45: Schematic of CTH 1-D system model......................................................................................109
Figure 4.46: Initial density position profile for the CTH simulations..........................................................110
Figure 4.47: Initial temperature profile of the water in the CTH simulations.............................................111
Figure 4.48: Temperature profiles in the chamber at different times for the CTH simulations...................112
Figure 4.49: Pressure histories at different locations in the chamber for the CTH simulations...................113
Figure 4.50: Induced hoop stress in the chamber wall as a function of time for the CTH simulations.......114
Figure 4.51: Water mass as a function of chamber position.........................................................................115
Figure 4.52: The Z-IFE chamber and 3m RTL design are shown with full neutron and blast protection of structures....................................................................................................................116
Figure 4.53: The inductance of the RTL is 15 nH out to a radius of 2 m to include some of the MITL.........................................................................................................................................117

Figure 4.54: The 3m long RTL is shown shortly before shot time with its inner and outer
cones still separated. ............................................................................................................. 118
Figure 4.55: RTL at shot time with the MITL uncovered. ........................................................ 119
Figure 4.56: The vertical thickness of the pulsed jets above the shot point only needs to be
1m as shown here rather than the over 2m shown in prior figures....................................... 120
Figure 4.57: RTL before shot during insertion.......................................................................... 121
Figure 4.58: RTL at shot time.................................................................................................... 122
Figure 4.59: Illustration of injection sequence. ......................................................................... 123
Figure 4.60: A conceptual z-pinch fusion chamber utilizing an aerosol and ablation liquid
protection scheme. ................................................................................................................ 127
Figure 4.61: A conceptual z-pinch fusion chamber utilizing an aerosol mitigation scheme in
a spherical vessel................................................................................................................... 128
Figure 4.62: Shows a comparison between unirradiated and irradiated F82H steel versus
temperature. .......................................................................................................................... 134
Figure 4.63: Irradiation induced shifts for upper shelf energy (left) and ductile brittle
transition temperature (right) verse irradiation temperature................................................. 134
Figure 4.64: F82H endurance limit design parameters based on five year life .......................... 139
Figure 4.65: Maximum design stress versus design life based upon fatigue cycles to failure. .. 140

###### **TABLES**

Table 3.1: Summary of Costs for the Case of the Median Cost .................................................. 30
Table 3.2: Input to Monte Carlo Analysis .................................................................................... 33
Table 3.3: Flibe circulation loop pipe statistics ............................................................................ 41
Table 3.4: Measurement of Na2MgCl4 dielectric constant .......................................................... 44
Table 3.5: Free energy of formation (kJ/mol per fluorine/chlorine atom) for flibe
components versus iron and chromium fluoride and for Na2MgCl4 salt constituents
and iron. .................................................................................................................................. 50
Table 4.1: Comparison of Laser Experiment Data with ALEGRA Simulation .......................... 64
Table 4.2: Z-IFE X-ray simulation key output. ........................................................................... 67
Table 4.3: Experiments Conducted............................................................................................... 84
Table 4.4: The experiment parameters, for argon, calculated from 1-D gas dynamics............. 104
Table 4.5: Impulse measurements for the pool with argon bubbles. ......................................... 105
Table 4.6: Summary of RTL cycle times................................................................................... 125
Table 4.7: Long-lived radionuclides.......................................................................................... 129
Table 4.8: Short-lived radionuclides.......................................................................................... 129
Table 4.9: The specific activity for a Hastelloy chamber at discharge and after 10000
days. ...................................................................................................................................... 130
Table 4.10: The specific activity for a F82H steel chamber at discharge and after 10000
days. ...................................................................................................................................... 132

![](images/page_010_table_0.png)

|  |  |
| --- | --- |
| Table 3.1: Summary of Costs for the Case of the Median Cost .................................................. Table 3.2: to Monte Carlo | 30 33 |
| Input Analysis .................................................................................... |  |
| Table 3.3: Flibe circulation loop pipe statistics ............................................................................ | 41 |
| Table 3.4: Measurement of Na2MgCl4 dielectric constant .......................................................... Table 3.5: Free energy of formation (kJ/mol per fluorine/chlorine atom) for flibe | 44 |
| components versus iron and chromium fluoride and for Na2MgCl4 salt constituents and iron. | 50 |
| Table 4.1: Comparison of Laser Experiment Data with ALEGRA Simulation .......................... | 64 |
| Table 4.2: Z-IFE simulation | 67 |
| X-ray key output. ........................................................................... Table 4.3: Experiments Conducted............................................................................................... | 84 |
| Table 4.4: The experiment for calculated from 1-D dynamics............. | 104 |
| parameters, argon, gas Table 4.5: measurements for the with bubbles. | 105 |
| Impulse pool argon ......................................... Table 4.6: of RTL times................................................................................... | 125 |
| Summary cycle Table 4.7: radionuclides.......................................................................................... | 129 |
| Long-lived Table 4.8: Short-lived radionuclides.......................................................................................... | 129 |
| Table 4.9: The for chamber and after 10000 |  |
| specific activity a Hastelloy at discharge | 130 |
| days. ...................................................................................................................................... Table 4.10: The specific activity for a F82H steel chamber at discharge and after 10000 |  |

###### **NOMENCLATURE**

CEP Chemical Engineering Plant Cost Index
CLT Collapsed Liquid Thickness
COE Cost of Electricity
D-T Deuterium-Tritium
DBTT Ductile-Brittle Transition Temperature
dpa Displacements per Atom
DOE Department of Energy
DWT Demineralized Water Tank
EBW Exploding Bridge Wire
EDX Energy Dispersive X-Ray Spectrometer
EIA Energy Information Administration
Flibe (LiF)2-BeF2
FY Fiscal Year
GEN IV Generation IV
GNEP Global Nuclear Energy Partnership
HE High Explosive
IFE Inertial Fusion Energy
ITER International Thermonuclear Experimental Reactor
LDRD Laboratory Directed Research and Development
LTD Linear Transformer Driver
LTE Local Thermodynamic Equalibrium
LWR Light Water Reactor
MITL Magnetically Insulated Transmission Line
MFE Magnetic Fusion Energy
MSRE Molten Salt Reactor Experiment
NIF National Ignition Facility
ODS Oxide Dispersion Strengthened
PRF Permeation Reduction Factor
RGA Residual Gas Analysis
RTL Recyclable Transmission Line
SEM Scanning Electron Microscope
STP Standard Temperature and Pressure
TEP Total Energy and Diagnostic Tool
TGS Transmission Grating Spectrometer
USE Upper Shelf Energy
UTS Ultimate Tensile Strength
UV Ultraviolet
VHEX Vacuum Hydraulic Experiment
ZN Z-Neutron

###### **1. EXECUTIVE SUMMARY**

Past z-inertial fusion energy research concentrated mainly on the full scale plant design.
This year an effort was made to create a logical path to reach the ultimate goal of a fusion power
plant through transmutation. To illustrate this path forward a roadmap was created outlining the
current issues, needed steps, and time required to reach these goals.
The roadmap outlines the intermediate steps required to reach a full scale transmutation
plant with the advent of a pure fusion energy plant being built several years later. It starts with
utilizing existing facilities capable of handling various separate effects experiments. These facilities
include Sandia National Laboratories’ Z-beamlet and ZR where several containment and mitigation
experiments can be conducted. The next step is to build a test facility (Z-Neutron or ZN) where
automation, recyclable transmission line (RTL) remanufacturing, target fabrication, and driver
development can take place and eventually be integrated together. With the inception of the Global
Nuclear Energy Partnership (GNEP) initiative and the goal of a closed fuel cycle, an alternative use
for z-pinch driven fusion arises. Work conducted through the Advanced Fusion Concepts: Neutrons
for Testing and Energy Grand Challenge LDRD has shown that fusion neutrons can transmute the
actinides in spent fuel [1]. The ZN facility will also be the test bed for developing z-pinch inertial
fusion energy (IFE) transmutation. Once everything is integrated, ZN will become the pilot plant for
the full scale transmutation plant.
Substantial progress on various power plant systems such as the RTL, flibe
characterization, plant automation, power conversion systems, linear transformer drivers (LTD), and
tritium permeation studies have been made. A high level systems cost analysis was also created in
an attempt to optimize the number of fusion reaction chambers, target yield, and repetitive rate
required to be competitive with other fusion power plant design studies.
The system cost analysis indicated that fewer chambers were more economical than the
original Z-IFE power plant design of ten chambers. Three alternatives were suggested in the
analysis for reducing the amount of reaction chambers needed for a 1000 MWe power plant: 1) an
increase in target yield, 2) an increase in repetitive rate, or 3) both an increase in repetitive rate and
target yield. In changing these parameters the number of chambers was reduced thus reducing the
cost of the plant. The combination of the two options was found to be the most economical choice.
A detailed driver cost model was done in addition to the systems cost model. It
includes the cost of all of the LTD components, the auxiliary equipment, and the land and facilities
to support a full scale fusion power plant. The driver will be a significant percentage of the power
plant cost.
Various studies of the chemical interaction between a flibe-like salt and a steel RTL
post shot were conducted. This was done to gain an understanding of how the free ions of the
dissociated salt and steel interact. Further experimentation on the electrical properties of a frozen
flibe RTL was conducted to understand its effectiveness in transmitting the pulse to the target.
Four power conversion systems were investigated; supercritical CO2 cycle, Rankine
cycle, Brayton cycle, and a combined cycle (Brayton-Rankine). A cycle analysis of each showed
how temperature and component efficiency affect the overall thermal-to-electric efficiency of the
power plant. Assuming that high temperature materials would be available in the future, the cycle
analysis showed that the combined cycle power conversion system was best for the Z-IFE plant.
A tritium permeation study of the piping and chamber was addressed this year. It was
compared to the analysis conducted for the International Thermonuclear Experimental Reactor
(ITER). Both stainless steel and reduced activation steel piping were analyzed using a DIFFUSE
model. The results showed that using a permeation barrier coating on the pipes along with

optimizing partial pressure and diameter could reduce tritium leakage significantly. In fact,
optimizing the piping system for Z-IFE could result in a significantly lower leakage rate compared to
the results of the ITER analysis.
The shock mitigation work focused on attenuating the high energy x-rays before they
reached the chamber wall. Three possible x-ray absorbing methods were investigated; thick liquid
curtains, aerosols, and gas. Two possible chamber designs were proposed based on these proposed
shock mitigation schemes. The first was a thick liquid blanket design and the second a first wall
design.
Extensive liquid curtain research has been conducted under the Z-IFE program in
previous years. Thick liquid curtains were studied because they offer both x-ray and neutron
protection for the chamber wall. A new higher repetition rate was proposed for a thick liquid curtain
chamber design based on the results from the systems cost analysis. This proposed chamber design
required a slightly larger target yield and over fives times the repetitive rate of the original Z-IFE
design. It utilized a frozen flibe RTL to lower separations and remanufacturing costs. A detailed
analytical analysis of the shot timing is presented.
Due to recent research on aerosol x-ray absorption and thermal annealing, a new first
wall chamber design was proposed. Modeling results of aerosols absorbing x-rays have shown
promise that they may be able to mitigate fusion yields up to 3 GJ. Thermal annealing of the LWR
pressure vessels around the world has shown near to complete recovery of the materials mechanical
properties almost eliminating the effects of neutron embrittlement. If this is the case, the liquid
curtain could be relocated to the outside of the chamber and act only as the heat transfer fluid and
tritium breeder as opposed to also acting as the shock absorber in the liquid curtain design. This
would greatly reduce the complexity of the internals of the reaction chamber. However, the thick
liquid curtain design remains the prime candidate for shock mitigation for Z-IFE.
Previous chamber stress analyses focused on designing a chamber based on a static
pressure or impulse pressure. This year a fatigue study was performed to assess the endurance limit
of a chamber made from F82H steel (the baseline material for Z-IFE). A cyclic pulse to the chamber
wall is inherent in a z-pinch driven inertial confinement fusion power plant. The study concluded
that fatigue should be considered along with the impulse pressure when designing the chamber.
Substantial progress was made this year for the Z-IFE project. The roadmap illustrated
the need to start experimentation immediately so that the base science and engineering required to
build upon could be established. The initial experiments could be performed on existing facilities at
Sandia National Laboratories. Significant strides were made in the areas of systems cost modeling,
chamber design, and shock mitigation techniques for a Z-IFE power plant. It is time for the Z-IFE
program to focus more on conducting the necessary experiments needed to prove the science and
engineering required to forge ahead towards fusion energy.

###### **2. Z-INERTIAL FUSION ENERGY ROADMAP**

Inertial fusion energy (IFE) has the potential to generate safe, secure, and reliable
commercial power for future generations. Lasers (National Ignition Facility-NIF), heavy ions, and
more recently z-pinch technology have been used to create the necessary environment for IFE.
Although the first two methods have a head start, a z-pinch driven system has been shown to be an
excellent option. In addition to producing electricity, a great opportunity exists for a z-pinch driven
IFE system as an alternative to fast reactors in the Global Nuclear Energy Partnership (GNEP)
initiative. Research, as part of a Grand Challenge LDRD, has shown that fusion source neutrons can
transmute some or all of the transuranics of spent fuel from light water reactors [1]. The reduction in
heat load due to transmutation could greatly increase the storage capability of the repository and
diminish some of the long lived radionuclides.
Several major issues must be addressed before this can be realized. The first issue is
fusion yield. Currently, the Z-machine can not produce a sustainable fusion burn. The hope with
ZR is to obtain a fusion burn with a yield on the order of 0.1 MJ. However, there is no pulsed
power/fusion energy program to strive and create the higher yields that would be required for
transmutation and commercial energy production. The fusion yield required is approximately 200250 MJ for transmutation and 3-30 GJ for a power plant. A program must be created to increase the
fusion yield.
The second issue is that the time between each fusion event must be reduced
significantly in order to both transmute waste and produce continuous power. A fusion event must
occur every 1 to 10 seconds depending on the fusion yield to generate a sufficient amount of heat for
energy production and supply the necessary amount of fast neutrons needed for transmutation. This
involves research on several fronts. Extensive target and mass production capabilities must be
developed. A simple and light weight recyclable transmission line (RTL), which connects the target
to the power source, must be designed. Placing and removing the RTL in the containment vessel
will require state-of-the-art automation. Pumping the vessel and driver components down to the
appropriate vacuum will also be necessary to ensure the electric pulse integrity. All these issues
must be addressed in order for z-pinch driven IFE to be feasible. These issues are addressed in a
roadmap developed to outline the necessary steps to achieve transmutation and fusion energy.
The Z-Inertial Fusion Energy (Z-IFE) program has developed two roadmaps. The first
(original) roadmap outlines a direct path to fusion energy [2]. This roadmap describes two facilities
needed to reach a full scale demo Z-pinch IFE fusion power plant. The first is a proof-of-principle
(Z-PoP) facility which demonstrates repetitively rated drivers, RTL optimization, and thick liquid
wall development between the years of 2007 and 2010. The next facility is a high yield engineering
test facility (Phase I) which will be used to develop single shot high yield targets. Once high yield
targets have been demonstrated, the engineering test facility will be modified for repetitively rated
high yield shots (Phase II). The operational time required for both phase I and phase II of the
engineering test facility was estimated to be 16 years from 2010 to 2026. The full scale demo power
plant comes online around 2026. The original roadmap was intended to illustrate a direct and
accelerated path to a Z-pinch IFE power plant.
The new roadmap creates a path for a full scale IFE transmutation plant. A key
objective of this roadmap was to tie Z-IFE technology and transmutation into the GNEP initiative as
part of the closed fuel cycle. The new roadmap describes the necessary science and engineering
steps needed to achieve these goals by starting with small scale separate effects experiments on ZR
and ending up with the full transmutation plant. The new roadmap (red) and the original roadmap
(light blue) are shown in Figure 2.1.

![](images/tmpvlzzzdgp.pdf-15-0.png)

###### **2.1 The Path to Transmutation and Commercial Power**

The roadmap consists of a single critical path which leads to the construction and
operation of a full scale transmutation plant. The required science and engineering involved in
developing these facilities are nested around and feed into the critical path. The crucial facility on
the critical path is the Z-Neutron (ZN) facility which evolves from a low repetitively rated testing
facility to a transmuter pilot plant. The critical path, target development, RTL and target
manufacturing, driver development, and repetitively rated automation are described in detail below.

_2.1.1 Critical Path_

The critical path starts with planned experiments utilizing the ZR machine and ZBeamlet. Z-beamlet is a kilojoule pulsed laser that can be used to ionize gas or liquids. It will be
used to demonstrate shock mitigation along with the ZR machine. Shock mitigation can be
demonstrated by absorbing the x-rays produced by the fusion yield through a gas, aerosol, thick or
liquid curtain medium. Several other crucial demonstrations will be performed on ZR including
tritium containment post shot and the use of a conical transmission line. The expected target yield
for ZR is approximately 0.01 MJ while producing 2-3 MJ of x-rays.
The Z-Neutron (ZN) Facility will be designed and built once these experiments are
successful along with the demonstration of the target yield, LTD drivers, repetitive rated shots, and
vacuum pumping of system components. This facility could be compared to the Advanced Burner
Test Reactor, which is described in the GNEP initiative, providing a test bed for further science and
engineering development. Once this facility is functional it is expected to operate at 24 fusion shots
per day at 20-30 MJ, meanwhile, transmuting small quantities of transuranics. The facilities for
developing the other transmutation and power plant technologies will be constructed around ZN so
that they can easily be integrated together. After 8-10 years of operation ZN will become a
transmutation pilot plant capable of a fusion shot every 100 seconds at a target yield of 20 MJ and
will be able to transmute 12.8 kg/yr of transuranics. The goal of the pilot plant is to have several
years of operational success before the ultimate decision between z-pinch driven or fast reactor
transmutation is made.
If z-pinch IFE driven transmutation is chosen, possible commercial involvement may
be enlisted to design and build a full scale transmutation plant capable of burning 1280 kg/yr of
transuranics. This plant will also generate 1000 MWe while transmuting the waste. Eventually the
demand for electricity will be so great that z-pinch driven fusion power plants will be needed. At
this point 3-30 GJ of fusion yield will be required at a rate of 1 shot per 10 seconds to generate 1000
MWe of power.

_2.1.2 Target Yield_

Target yield development will be done in a separate facility outside of ZN. The target
physicists at Sandia National Laboratories predict the maximum fusion yield on ZR will be on the
order of 0.01 MJ [3]. However, it will produce 2-3 MJ of x-rays so that shock mitigation and
containment experiments can be performed using this facility. A separate facility (ZX or X1) will
need to be designed and built to develop and contain the larger fusion yields on the order of 3-30 MJ.
The hope is a ZX facility will be built and operational by the time the work on ZN requires larger
fusion yields.

_2.1.3 Recyclable Transmission line and Target Manufacturing Plant_

A facility for RTL and target development is necessary to achieve simple cost effective
designs which can easily be manufactured and assembled together. The material for the RTL has yet
to be determined, so ongoing studies and experiments on ZN will be needed. The RTL must also be
easily remanufactured so that it can be used in future fusion shots. This requires significant
automation to maneuver the RTL in and out of the chamber and into the manufacturing plant. A
separate facility will be needed to develop the RTL and manufacturing plant. For ease of integration
the manufacturing development plant will probably be located next to ZN.
Target fabrication can probably be developed in the same facility as the RTL because
they are integrated together before being inserted into the fusion vessel. Ensuring a target is free of
defects is crucial to creating the necessary conditions for fusion. Currently on Z they are assembled
by hand which is not practical for fusion energy. This will have to become automated over time for
transmutation and power production to be possible. Both the target and RTL must be manufactured
at such a rate that it can support the ZN facility at the pilot plant level which requires one shot every
100 seconds. Further increase in repetitive rate will be required for the full scale transmutation and
power plants.

_2.1.4 Driver Development_

The most capable driver for a full scale transmuter or power plant is the linear
transformer driver (LTD). This driver has the potential to be repetitively rated at speeds needed for
these plants. However, this driver has yet to be implemented into a system to drive a fusion reaction.
Eventually, a separate facility will be needed for prototyping, assembling, and to house the massive
foot print of the driver. Another crucial step in the roadmap is acquiring the necessary parts required
to build the large number of LTDs. The necessity of the drivers is such that the roadmap shows
research and development on LTDs starting immediately.

_2.1.5 Automation and Repetitive Rate_

In order for ZN to be repetitively rated at the necessary scale needed for transmutation
and power, state-of-the-art automation is needed to maneuver the RTL in and out of the reaction
chamber. It will also be needed in the manufacturing plant for both the RTL and target fabrication.
Another crucial issue is pumping down and maintaining the necessary vacuum conditions in the RTL
and chamber for each shot in a matter of seconds. Demonstrating a relatively high repetitive rate
while maintaining vacuum will more than likely be necessary before ZN can be built [3].
A facility will be needed for developing the necessary automation and repetitive rate
demonstration. The ZN facility will be built once a moderate rate has been demonstrated, probably
on the order of one cycle per hour. Over time the repetitive rate and automation will develop so that
ZN can operate at a rate of 1 shot per 100 seconds. Eventually, the rate will need to be increased to
1 shot every 10 seconds to support the full scale plants.

###### **2.2 Z-IFE and the Global Nuclear Energy Partnership**

The Global Nuclear Energy Partnership initiative strives to expand and develop safe,
clean, and secure nuclear energy. The plan includes utilizing the knowledge gained by other nuclear
power capable countries and advancing a closed fuel cycle. This involves reprocessing spent fuel

from LWRs and transmuting or burning some of the long-lived nuclear waste. The current plan is to
use fast reactors to transmute this waste into forms that are less radioactive or have shorter half-lives.
This will allow a single repository, Yucca Mountain, to store all of the remaining spent fuel waste up
into the next century [4]. Z-pinch driven IFE technology offers several advantages over fast reactors
for burning the actinides which is discussed in more detail in a report on z-pinch transmutation [5].
Figure 2.2 illustrates a closed fuel cycle that includes transmutation.

**Figure 2.2: An advanced closed fuel cycle with transmutation.**

As mentioned above the ultimate goal of creating this roadmap was to show how Z-IFE
can be included in the GNEP initiative. Sandia National Laboratories has the state-of-the-art
facilities and the full spectrum of technical capability to provide the necessary elements for a
strategic initiative. The ZR-machine provides an ample facility for conducting the necessary physics
and engineering experiments required for increasing fusion yield, demonstrating fusion containment,
and target development. Sandia has a talented robotics group which can aid in designing the
automation required for maneuvering the RTLs in and out of the containment vessel. Sandia has
experts in materials science which will be valuable in several aspects of this work. Material
development for the vessel, RTL, and power plant will be essential to ensure safe operating
conditions. Sandia has extensive programs that support energy research and development ranging
from solar and wind to nuclear power.
The green circles shown on the roadmap represent the milestones set forth by the
GNEP initiative for developing a fast reactor for transmutation. However, a more realistic timeline
is shown directly below the GNEP proposed timline and is what the critical path to z-pinch driven
transmutation is based on. According to GNEP a full scale Advanced Burner Reactor is proposed to
be on-line by the year 2025. If z-pinch driven IFE transmutation was funded as planned, then
around the year 2025 ZN would be fully operational and demonstrating its capabilities.

![](images/tmpvlzzzdgp.pdf-18-0.png)

Realistically, having a full-scale fast burner reactor on line by the year 2025 is not feasible due to all
the needed research, development, and licensing before such a plant can be built. It is possible to
foresee that maybe once ZN has demonstrated transmutation at a substantial scale and is ready for a
full scale plant design the fast reactor will be in the same stages of development. The hope is that
there will be options when a decision needs to be made to choose the technology for transmutation.

![](images/page_019_table_0.png)

|  |  |
| --- | --- |
|  | 20 |

###### **3 Z-IFE POWER PLANT SYSTEMS ANALYSIS**

Rather than mount an integrated system-wide look at the Balance-of-Plant processes
this year, the power plant group focused on specific problems.
The operating temperature range for the z-pinch process is narrowing to the 600 K to
900 K range. A heat source operating in this range can support commercially available Rankine
cycles at the low end and the conceptual phase Brayton and combined cycles when and if they
become commercially available. A simple power conversion cycle efficiency comparison was
completed this year. Since any of these three generic thermodynamic cycles will work, the project
will concentrate on producing a heat source compatible with one or the other of these two options,
relying on such other projects as GNEP or GenIV to provide details on the options themselves.
A first order comprehensive economic model was developed by Lawrence Livermore
National Laboratory (LLNL) to estimate the total capital cost of the Z-IFE power plant. This
includes the driver (high level), chamber, balance-of-plant, RTL, and target factory. The capital
costs are then compared with economic studies of other fusion power plant designs such as the laser
driven IFE concept. It shows the economic advantage of using fewer chambers with higher
repetitive rates and target yields.
Another major accomplishment this year was the production of a conceptual design for
a pulsed driver scaled to support a full sized power plant, permitting an initial capital cost estimate.
The driver will be expensive with a median price of $372 million per driver. The cost is dominated
by the 12,600 (minimum) LTD cavities, each of which is a high technology compilation of switching
and capacitance hardware. The cost analysis underlines the need for optimization aimed at cost
reduction and provides insight into the best places to begin that analysis.
This year marked the beginning of modeling to predict and manage waste production.
Activities concentrated on tritium production and the prediction of tritium loss to atmosphere. While
this vital area needs more analysis, it would appear that the overall design of the facility allows
operation within the limits of tritium release set by ITER.
The University of California at Los Angles continued experiments characterizing the
debris created by a plasma discharge, and the rate and chemistry of recombination of free radicals
created by the fusion reaction. These first experiments form important first steps in the many tests
needed to bring Z-pinch to reality.

###### **3.1 Cost Models for Z-IFE**

Two cost models were developed this year for the Z-IFE power plant. The first was a
high level comprehensive systems cost model covering the major components of the power plant. It
illustrates the economic benefits of increasing the target yield and increasing the shot rate. The
systems cost model for the optimized Z-IFE power plant is then compared to other IFE fusion power
plant concepts based on the cost of electricity (COE). The second model was a detailed cost analysis
of the linear transformer driver (LTD). This component in particular will be a significant percentage
of the total cost of the power plant.

_3.1.1 Systems Economic Modeling for Z-IFE [6]_

An update and more comprehensive systems model for a Z-IFE electric power plant
was completed this year. The code was written in Mathcad [®], which makes it easy to read and easy
for even novice users to exercise. All assumptions and the bases for the physics, engineering and

cost scaling relationships were documented in the code and are not reproduced in detail as part of
this report. In this section, only the key assumptions and important results and findings were
presented.

**3.1.1.1** **Target Gain and Yield**

A fundamental relationship for any IFE concept is the target gain as a function of driver
energy. For Z-IFE this relationship was determined based on reported results for target yield for the
dynamic hohlraum [6, 8]. Figure 3.1 shows the target yield as a function of the z-pinch energy, i.e.,
the energy delivered to the pinch.

**Figure 3.1: Target yield versus driver energy. Fit through three calculated cases is shown.**

The fit through the three reported cases was used to determine the target gain versus
driver energy as

###### G = 30.15 ⋅ ( E −122.).038 for E > 122. MJ 3.1

This is plotted in Figure 3.2.

![](images/page_021_eq_0.png)
22

![](images/tmpvlzzzdgp.pdf-21-0.png)

![](images/tmpvlzzzdgp.pdf-22-0.png)

**Figure 3.2: Dynamic hohlraum target gain versus driver energy.**

**3.1.1.2** **Driver Efficiency and Cost**

The Z-IFE systems code does not have a detailed model for the pulsed power driver.
At this point the driver cost is simply given as the product of the energy delivered to the pinch (J)
times a unit cost expressed in $/J. The driver unit cost is a variable in the cost of electricity
calculation, so the user may examine the sensitivity of the results to driver cost. At the time of this
report, a good unit cost estimate was not received, so the reference case value of $15/J was used to
estimate the driver cost. This is based on statements by SNL researchers that current pulsed power
machines cost ~$30/J and the linear transformer driver (LTD) should be a factor of two lower. The
driver efficiency is assumed to be 60% based on material presented at the August 2005 Z-IFE
workshop for the LTD [9]. A more detailed driver cost estimate is found in section 3.1.2.

**3.1.1.3** **Chamber and Power Plant**

The cost scaling relationship for the chamber and power plant are based on the thick
liquid wall chamber using flibe as the working fluid. The chamber cost is estimated on a $/J of
structure basis. Two options are given: a chamber in the geometry of a flattened ellipsoid (original
SNL design) and the more cylindrical chamber developed by LLNL and reported in FY05. The base
case structure is low activation ferritic steel (F82H), but the code includes the option to use carboncarbon composite for chamber structures, a high performance option proposed by LLNL.
The balance of plant facilities and equipment models are based on the Osiris cost
scaling relationships, but escalated from 1991 dollars to 2005 dollars [10, 11]. Many of the Osiris
models were based on previous design studies and for the most part were consistent with those used
for HYLIFE-II [12]. The plant power conversion efficiency (total thermal to gross electric) is 42%
for the steel chamber and 50% for the carbon-composite chamber.

An important design variable in the systems model is the number of chambers in the
power plant. The original SNL reference design for a Z-IFE power plant consisted of ten chambers
each producing ~100 MWe net power for a total plant power of ~1000 MWe, a typical standard
power for this type of study. Our previous preliminary economic systems analyses indicated that a
power plant with many small chambers is not competitive with a plant with fewer chambers
operating at higher yield and pulse repetition rate (rep-rate). As shown in the following results,
those preliminary findings are confirmed and better quantified by this year’s work.
Consistent with previous SNL conceptual designs, each chamber is assumed to have an
independent driver, heat transfer system and power conversion system. Only the heat rejection
system (e.g., cooling towers) is shared in chamber plants.

**3.1.1.4** **RTL and Target Factory**

The cost and power consumption of the factory needed to produce the recyclable
transmission lines (RTLs) was developed and reported by SNL for two cases: steel RTLs and RTLs
made of flibe [13]. The systems code includes options for both cases, but due to the significant cost
and power advantages of using cast flibe RTLs, flibe is the base case in the analyses.
The cost of the fuel capsule and hohlraum connection to the RTL is also accounted for
in the model. The capsule cost and cost scaling with yield and production rate are based on a
detailed study completed by General Atomics for direct-drive laser IFE [14]. To account for the
added cost of the dynamic hohlraum components of the target, the capsule factory cost is simply
doubled. That is, the Z-IFE capsule plus hohlraum is twice the cost of the laser IFE capsule (for a
given yield). The RTL and target factories were assumed to service the entire power plant, i.e., all
chambers.

**3.1.1.5** **Total Capital Cost and Cost of Electricity**

The total capital cost of the Z-IFE power plant is calculated from the sum of the direct
capital costs of the driver, chamber, balance-of-plant, RTL and target factory using indirect costs
equal to 93.6% of the total direct capital cost. Annual capital charges are based on a fixed charge
rate of 9.66%. These capital cost factors are consistent with other fusion economic studies. Annual
operation and maintenance costs are included for the power plant and target factory. The cost of
electricity (COE) is then the sum of annual costs divided by the annual net energy produced. The net
energy is the product of the plant net electric power multiplied by the hours of operation per year
(plant capacity factor = 85%). The net electric power is equal to the gross electric power produced
minus the power recirculated to 1) the driver, 2) the RTL factory, 3) the plant pumping for creating
the thick liquid wall and for the heat transfer system, and 4) other auxiliary power requirements
(taken as 4% of the gross electric power).

**3.1.1.6** **Key Results**

Several key results of the systems analyses are given below. The basic plant design
variables are the driver energy, chamber rep-rate, and number of chambers per plant. The net
electric power of the plant can be allowed to vary with these parameters, or more instructively, fixed
(e.g., at 1000 MWe) in order to compare plants that deliver the same product.

Figure 3.3 gives the driver energy required to produce a fixed net power of 1000 MWe
as a function of the chamber rep-rate. Results are shown for plants consisting of 1, 3, 5 or 10
chambers (Z-IFE baseline). Note that this is the driver energy required by each chamber. At a given
rep-rate, plants with fewer chambers require higher yield per pulse and thus higher driver energy.
Clearly pushing the rep-rate higher than the original SNL base case of 0.1 Hz is attractive if it is
technically feasible. In section 4.2.1 of this report, an estimate that a rep-rate of 0.5 Hz might be
possible is described. This is higher than the 0.3 Hz quoted by SNL as a “stretch” case. At 0.5 Hz
the single chamber plant requires a driver energy of ~ 42 MJ corresponding to a target yield of
~4600 MJ.

**Figure 3.3: Driver energy per chamber required to achieve a net plant power of 1000 MWe**
**versus chamber rep-rate.**

The resulting COE as a function of chamber rep-rate for the 1000 MWe plant with
various numbers of chambers is shown in Figure 3.4. This figure quantifies the economic
advantages of configuring the Z-IFE power plant with fewer chambers and pushing the chamber
pulse rate as high as possible. Only the 1 and 3-chamber plants reach a COE less than 10 ¢/kWeh.
For comparison, recent MFE and IFE studies quote COEs of 7-9 ¢/kWeh. Even at that it will be
hard to compete with advanced fission reactors at 4-6 ¢/kWeh (depending on the size). The single
chamber Z-IFE plant operating at 0.5 Hz, has a COE of 7.0 ¢/kWeh, roughly the same as the most
recent direct-driver laser IFE result of 7.2 ¢/kWeh [15]. The 10 unit, 0.1 Hz plant has a COE of ~20
¢/kWeh, which is a factor of 2-3 higher than needed to compete with other fusion concepts.
Another way to display these results to show the range of driver energies needed is
shown in Figure 3.5. Here we limit the plot range to COEs less than 10 ¢/kWeh and chamber reprates less than 0.5 Hz. The single chamber plant needs a driver energy > 42 MJ for a chamber rep

![](images/tmpvlzzzdgp.pdf-24-0.png)

rate < 0.5 Hz, and at 60 MJ, the rep-rate is down to 0.29 Hz. The 3-chamber plant has a chamber
rep-rate < 0.5 Hz for driver energies > 22.5 MJ and is down to 0.3 Hz at E ~ 30 MJ. The minimum
COEs occur at 20 MJ for the 1 chamber case and 16 MJ for the 3-chamber plant, but the required
rep-rates of 1.8 and 1.0 Hz, respectively, are beyond the reach of the replaceable RTL concept.

**Figure 3.4: COE versus chamber rep-rate for 1000 MWe plants with 1-10 chambers per plant.**

![](images/tmpvlzzzdgp.pdf-25-0.png)

![](images/tmpvlzzzdgp.pdf-26-0.png)

**Figure 3.5: COE and chamber rep-rate versus driver energy for 1000 MWe plants with 1 or 3**
**chambers.**

One final result highlights the dependence of the COE on the net electric power of the
plant. Figure 3.6 gives the COE as a function of rep-rate for two-chamber power plants with total
net powers of 500, 1000 and 2000 MWe. The 500 MWe plant has a COE > 10 ¢/kWeh over the
entire range of rep-rates considered (up to 0.5 Hz). The 2000 MWe case shows the favorable
economies and benefits of sharing the single RTL and target factory; the COE is down to 5.7
¢/kWeh at 0.5 Hz. Note that the COE for the 2-chamber, 1000 MWe case is only 10% higher than
for the single-chamber plant discussed previously (i.e., 7.7 ¢/kWeh instead of 7.0 ¢/kWeh at 0.5 Hz).

![](images/tmpvlzzzdgp.pdf-27-0.png)

**Figure 3.6: COE versus rep-rate for two-chamber plants with various net electric powers.**

**3.1.1.7** **Conclusions and Recommendations**

In summary, the results of the more detailed Z-IFE power plant systems code indicate
that power plant configurations with fewer chambers (perhaps 1-3) operating at as high a pulse rate
at possible (perhaps up to 0.5 Hz) have the most attractive economics in terms of COE. The COE
for the single chamber plant operating at 0.5 Hz is slightly better than the most recent result for
laser-driven IFE. We note that this Z-IFE systems code is a “first generation” model and as such
would benefit from careful critique and further refinement. In particular, a more detailed and
documented cost and performance model is needed for the driver. The code should also be updated
as progress is made and new information is developed on target performance. Finally, a future
version should examine the impact of fast ignition targets, which could significantly reduce the
driver energy (and associated cost) needed to achieve the very high target yields that are compatible
with the inherently low rep-rate and desire to minimize the number of chambers for a given net
electric power.

_3.1.2 Estimated Cost for a 1 PW LTD Driver_

This section presents a cost estimate for an LTD based driver that delivers 1000 TW (1
PW) to the vacuum insulator stack. The estimate is a composite of parametric and stochastic
estimating techniques. Figure 3.7 contains a plot of the results.

![](images/tmpvlzzzdgp.pdf-28-1.png)

**Figure 3.7: Stochastic Distribution of Capital Cost for a 1 PW Driver**

The median price for a 1 PW driver would be $372 million. This cost excludes acreage
and site preparation. This cost distribution is based on a Monte Carlo simulation. Using the same
Monte Carlo simulation, a 1 PW driver has a 95% probability of costing less than $862 million.
The design on which the estimate is built comes from an as yet unpublished paper

[16], section IV.C. Figure 3.8 contains a sketch with basic sizing information of the driver. The
driver consists of a large (75 m diameter by 10 m high) water tank containing a triplate pulse
transmission system connected to a vacuum stack estimated to be 20 m diameter and 10 m high. The
system is driven by 210 stacks of 60 linear transformer driver (LTD) cavities for a total of 12,600
LTD cavities. The tank contains demineralized water, the initial charge of which is included in the
estimate.

**Figure 3.8: Sizing Sketch for Driver System**

Table 3.1 contains for illustration the cost components extracted from the Monte Carlo
analysis for the median total cost. These individual costs are only those that combined to produce
the median total cost. They are not the median costs in their own individual distributions.

![](images/tmpvlzzzdgp.pdf-28-0.png)

![](images/tmpvlzzzdgp.pdf-28-2.png)

**Table 3.1: Summary of Costs for the Case of the Median Cost**

**3.1.2.1** **Demineralized Water Tank**

The demineralized water tank was priced as a 44,200 cubic meter cone roofed stainless
steel tank using data from the Ulrich and Vasudevan reference [17] which is reproduced in Figure
3.9. Tank purchase price was $674,000 using 2004 costs as the basis. These tank costs should be
multiplied by a bare module factor that accounts for hookup and ancillary equipment. The bare
module factor for stainless steel is 3.5 yielding a total direct cost of $2,360,000.
For variability, costs could be as much as 80% of the costs reported above. For a high
estimate, assume the tank was 15 meters deep instead of 10 meters. Costs increase to $8.26 million.

**3.1.2.2** **Water Tank Internals**

Triplate internals were assumed to cost 10% of the tank direct cost. Assume that high/low
costs track at 10% of the costs reported for the tank. This is an approximation based on experience
with vessel internals in general.

**Figure 3.9: Purchase Price for Tanks**

![](images/tmpvlzzzdgp.pdf-29-0.png)

![](images/page_029_table_0.png)

| Cost Component | Cost at Median Total Cost |
| --- | --- |
| Demineralized Water Tank | $2,540,000 |
| Tank Internals @10% of DWT | 251,000 |
| LTD (12,600) | 358,000,000 |
| Vacuum Stack | 11,200,000 |
| Initial Charge Demineralized Water | 154,000 |
| Total | $372,000,000 |

### 3.1.2.3 Linear Transmission Drivers

LTD costs amount to slightly more than 96% of the total cost. Figure 3.10 presents the results of a stochastic distribution of LTD cavity costs. The median cost for the 12,600 cavities would be $353,000,000 in 2004 dollars. There is a 95% probability that the 12,600 cavities would cost less than $844,000,000 on the same basis. The median price per unit is $28,000.

[Figure 3.10: Stochastic Distribution of LTD Cavity Costs – 12600 Cavity Case]

LTD cost distribution is approximated by a lognormal curve in the overall Monte Carlo simulation. This makes the natural logarithms of costs are distributed normally. The mean of these natural logarithms is 19.68 and the standard deviation of these logarithms is 0.529. Note that the median cost for 12,600 LTD cavities is $353 million while the LTD cost contribution to the median total cost shown in Table 3.1 is $358 million.

### 3.1.2.4 Vacuum Stack

The vacuum stack cost was estimated based on an average price per unit weight for parts manufactured from steel. This is typically taken as $20/lb. This method, as simple as it is, has proven remarkably robust. For example, a friend's new car costing approximately $60,000 weighed 1.5 tons. The vacuum stack was assumed to be a porous cylinder weighing 33.9 tons (10 m diameter and 5% porosity). This comes out to $13,600,000 direct.

These costs were in 2005 dollars, and theoretically should be deflated to a 2004 basis. However, the estimation method was so simplistic that the effort was not considered worthwhile.

For variability, assume on the low end that manufacturing cost was $15/lb. For the high end, maintain the same cost per pound and assume 10% porosity. Under these conditions, costs range from $10.2 to $27.2 million.

**3.1.2.5** **Initial Charge for Demineralized Water**

Demineralized water was estimated at $3.15/m [3] using the utilities estimation method
proposed by Ulrich and Vasudevan [17].

_Cs_, _u_ = _a_ ⋅ _CEP_ + _b_ ⋅ _Cs_, _f_ 3.2

Where

0.00025
_a_ = 0.007 + _q_ & 0.6, _b_ = 0.004 3.3

![](images/page_031_eq_0.png)

In the above, _Cs,u_ represents a utility cost for demineralized water in _$/m_ _[3]_, CEP
represents the Chemical Engineering Plant Cost Index [18], _Cs,f_ is a fuel cost in $/GJ and _q_ &
represents demineralized water plant design capacity in _m_ _[3]_ _/s_ . As would be expected, demineralized
water is relatively insensitive to fuel cost. Surprisingly, it is also relatively insensitive to plant size
for plants bigger than 500 _m_ _[3]_ _/s_ . Fuel was assumed to cost $7/GJ based on DOE EIA estimates for
natural gas priced for industrial use [19]. The CEP for 2004 is 444.2.

![](images/page_031_eq_1.png)

400

200

0

|Chemical Engineering Pla|nt Cost Index|
|---|---|
|||
|`||
|||
|||

1950 1960 1970 1980 1990 2000 2010

**Year**

**Figure 3.11: Chemical Engineering Plant Cost Index**

Figure 3.11 contains CEP values for the period 1950 to 2005. As a matter of interest,
note the rapid plant cost growth of the past three years. This represents worse inflation than seen
during the 1980’s. Assume the unit cost for demineralized water can vary between $1.5/ _m_ _[3]_ and
$6/ _m_ _[3]_ .

**3.1.2.6** **Scaling**

Estimated median cost, _Ctot_, can be scaled using Equation 3.4. This is an application of
equation 5.1 from the Ulrich and Vasudevan text [17]. The exponent was taken as 0.6 after
inspection of Table 5-1 of the same reference.

⎛ _TW_ ⎞ 0.6
_Ctot_ = 372 ⎜ ⎟ 3.4
⎝ 1000 ⎠

The relationship is scaled using power, _TW_, in terawatts delivered to the vacuum insulator stack.
This cost excludes acreage and site preparation.

![](images/page_032_eq_0.png)
**3.1.2.7** **Cost Distribution**

A Monte Carlo analysis was done using the variability numbers discussed above. Four
of the five cost components are assumed to vary stochastically within triangular distributions. Their
parameters are summarized in Table 3.2. Costs for the LTD were assumed to vary within a
lognormal distribution as discussed above.

**Table 3.2: Input to Monte Carlo Analysis**

The Monte Carlo model was implemented in Microsoft™ Excel. Figure 3.7 contains a
plot of the results based on 10,000 iterations of model. Costs were assumed to vary independently.

###### **3.2 Power Conversion Systems for the Power Plant**

The efficiency of a power plant depends on how effectively the total thermal energy
input is converted to electrical output. An effective use of the energy is often related to high
operating temperature. This discussion is based on existing models developed for the supercritical
Brayton cycle, Rankine cycle, helium Brayton cycle, and the combined cycle. The suitability of a
specific cycle does not depend on thermal performance only, since many other constraints could
impede its implementation. In some cases, economical and compatibility reasons prevent the use of
some materials that show an adequate performance at high temperature. For this discussion, it is
assumed that readily available materials can be used for low and high temperature applications.

_3.2.1 Super Critical CO2 Brayton Cycle_

A possible power conversion system for the Z-IFE power plant or the transmutation
plant could involve the use of one of the supercritical cycles, specifically the CO2 cycle.
Supercritical Brayton cycles are currently being investigated extensively at SNL and the

![](images/page_032_table_0.png)

| Cost Component | Low Estimate | Mode Estimate | High Estimate |
| --- | --- | --- | --- |
| Demineralized Water Tank | 1,862,000 | 2,327,500 | 8,155,000 |
| Tank Internals @10% of DWT | 186,200 | 232,750 | 815,500 |
| Vacuum Stack | 10,200,000 | 13,600,000 | 27,200,000 |
| Initial Charge Demineralized Water | 66,300 | 139,000 | 265,200 |

Massachusetts Institute of Technology (MIT) for possible use with nuclear reactors in order to
reduce capital cost, shorten construction period, and increase nuclear power plant efficiency. The
efficiency of the supercritical CO2 Brayton cycle operating at moderate temperatures (~550 [o] C) is
comparable to the efficiency of the helium Brayton cycle. One drawback is the higher operating
pressure (20 MPa). At this pressure, there is an abrupt property change at the CO2 critical point.
The increase in density leads to a reduction in compression work, which results in a significant
efficiency improvement. X.L. Yan offered the following comparison for helium and a supercritical
CO2 turbine: 17 stages are needed for a 167 MWe helium turbine while only 4 stages are required for
a 300 MWe supercritical CO2 turbine. Overall, the cycle offers an attractive alternative to the steam
cycle. Figure 3.12 shows the supercritical Brayton cycle components and performance comparison
curves [18, 22].

**Figure 3.12: A schematic of a supercritical C02 Brayton cycle (left), and an efficiency verse**
**turbine inlet temperature plot.**

_3.2.2 Rankine, Helium Brayton, and Combined Cycles_

The other three power-generation alternatives presented are well-established
technologies. The selection of any one of them depends mainly on its performance and suitability
for a particular application. The Rankine cycle is of primary interest when the required operating
temperature is relatively low (370 ºC). The helium Brayton and combined cycles are attractive when
the available temperature is high (usually greater than 800 ºC). The power conversion analysis is
mostly based on an energy balance. If in the near future existing materials are improved or new
materials are developed for high temperature applications, the standard Rankine cycle will probably
be the least attractive option. This assumes that new or improved materials are affordable and
available in large quantities.

![Figure 3.13 and Figure 3.14 show the Brayton and combined cycle configuration used](images/tmpvlzzzdgp.pdf-33-0.png)
for modeling purposes, respectively. The selected power cycles are represented by a limited number
of elements. Since the principal purpose was to model a simplified cycle for evaluating the
performance under different operating conditions, the number of components was kept to a
minimum. Thus, only the major components are represented. In most cases, only one component
represents a group of components of the same class normally present in actual cycles.

**Figure 3.13: A schematic of the standard Brayton cycle.**

The components for the gas cycle are the main heat exchanger (heater and reheater),
high pressure turbine, low pressure turbine, high pressure compressor, low pressure compressor,
regenerator, compressor intercooler, turbine exit fluid cooler, and an electric generator. Most gas
power plants operate in an open cycle. If a plant operates in a closed cycle, an additional heat
exchanger (the cooler) is required. In this work, helium is used as the Brayton cycle working fluid.
The final selection of the Brayton cycle fluid depends on the constraints imposed by the reacting
fluid. A closed cycle should be considered only when the environmental impact excludes the
operation of an open cycle.
The combined cycle is a combination of a topping Brayton cycle and a bottoming
Rankine cycle. The combined cycle consists of the following components: the main heat exchanger,
compressor, gas turbine, steam turbine, heat recovery steam generator (economizer, evaporator,
drum, and superheater), condenser, and a high pressure pump. Higher efficiency can be obtained
from combined cycles since the energy contained on the gas turbine exhaust is used to generate
additional power.

![](images/tmpvlzzzdgp.pdf-34-0.png)

![](images/tmpvlzzzdgp.pdf-35-0.png)

**Figure 3.14: A schematic of the combined cycle.**

_3.2.3 An Analysis of the Rankine, Brayton, and Combined Cycles._

A parametric analysis was conducted using the Rankine, Brayton, and combined cycles.
It was assumed that the thermal efficiency of the turbines, compressors and pumps were 90%, and
the thermal effectiveness of the economizers, evaporators, superheaters and other types of heat
exchangers were 90%. The first objective of the parametric analysis was to determine the suitability
of using any of these cycles for the operating conditions set in the chemical reactor heat exchanger.
If higher temperatures are allowed in the chemical reactor heat exchanger, the Brayton and
combined cycles will have a great advantage.
The maximum operating temperature depends on the average flow temperature. The
average flow temperature depends on the thermodynamic properties of the fluid selected and reactor
type, the initial operating conditions, and the exit temperature in the chemical reactor heat
exchanger. The thermal energy is transported to a power cycle through the reactor heat exchangers.
The turbine inlet temperature was set to 800 K for the steam cycle and to 1000 K or more to allow
operation of the gas and combined cycle. There are many losses associated with each component.
The efficiency/effectiveness is used to group most of them. The impact of each component on cycle
efficiency was determined by varying one parameter while keeping all others constant.
In a Rankine cycle, there is not much opportunity to increase the temperature over a
wide interval due to the critical point of water. The turbine inlet temperature should not be low with
respect to the saturation temperature corresponding to the operating pressure to avoid low quality
vapor in the steam turbine exit. On the other hand, the temperature should not be so high that the
vapor behaves as a real gas. When the steam turbine temperature increases from 675 to 800 K, the
net power output increases by about 10%. The amount of energy consumed by the pump is small
when compared with the energy generated by the steam turbine. Likewise, the impact of the pump
performance on energy generation is not significant.

The performance of the steam turbine is of crucial importance in a vapor cycle. If the
efficiency of the steam turbine is decreased from 95% to 65%, the total energy generation is reduced
by about 50%. The back pressure also has a significant influence on the plant performance. The
condenser usually operates under vacuum conditions which increases the vapor quality at the steam
turbine exit and promotes better conversion efficiency. The energy invested to maintain the vacuum
is greatly compensated. When the back pressure increases from 10 kPa to 55 kPa, the net power
output is reduced by 23%.
As was mentioned previously, the helium Brayton and combined cycles probably need
to wait for future material development. Nonetheless, it is important to know what the benefits and
drawbacks of operating at higher temperatures are if the advances in materials allow it. By varying
the turbine inlet temperature from 1000 to 1210 K, the gas cycle energy generation was raised by
23%. Both the gas turbine and compressor performance are critical to the performance of the plant.
If the efficiency of either the gas turbine or the compressor is degraded from 95% to 65%, the total
power output is reduced by more than a factor of 2 for the turbine and close to a factor of 2 for the
compressor. The compressor inlet temperature is also of great interest. Since it has a significant
impact on performance, a refrigeration system is used frequently to keep it under certain limits.
When the compressor inlet temperature is raised from 270 K to 360 K, the net power output is
reduced by 30%.
In a combined cycle, most of the energy is generated by the gas turbine. The
efficiencies of the pump and steam turbine have a small effect on plant performance when they are
compared to the impact of the compressor and gas turbine. If either the efficiency of the gas turbine
or the compressor is reduced from 95% to 65%, the energy generation of the plant is reduced by
about 50%. When the efficiency of the steam turbine is decreased by the same amount, the energy
generation of the plant is reduced by 10%. This indicates that, if a combined cycle were used for a
particular application, special attention should be placed in optimizing the whole system so that the
compressor and turbine can operate at their highest possible efficiency. If the gas turbine inlet
temperature is increased from 1000 K to 1300 K, the power generation of the plant is increased by
30%.
Since the objective of this analysis was to show the impact of the turbine inlet
temperature on the power generation, it took into consideration the practicability of all processes
involved. With a turbine inlet temperature equal to 1000 K, it is impractical to operate the
bottoming cycle due to the high humidity content in the last stages of the steam turbine. In general,
for specified operating conditions, the Brayton cycle consistently shows better overall performance
when compared with the Rankine cycle. The better performance of the Brayton cycle can be
associated with higher turbine inlet temperatures. Likewise, the combined cycle shows better
performance compared to the Brayton cycle. Better performance is usually associated with even
higher constraint on the minimum turbine inlet temperature. Figure 3.15 is an example of the
Brayton and combined model outcomes.

![](images/tmpvlzzzdgp.pdf-37-0.png)

**Figure 3.15: Brayton and combined cycle efficiency verse temperature.**

Both the Brayton and the combined cycle become more attractive for use in the Z-IFE
power plant at higher working fluid temperatures. The gas turbine dominates the generation of
energy for both the Brayton and combined cycles. For similar operating conditions, the combined
cycle shows better performance. Probably the major advantage of the combined cycle is the
generation of additional power from the energy contained in the gas turbine exhaust.

###### **3.3 Tritium**

Tritium is essential for designing any fusion power plant. The quantity of naturally
occurring tritium on earth is very small due to its short half-life (12.32 years), which makes it
impossible to use in large scale operations such as fusion power plants. In order to generate a
significant amount of fusion energy for power production, tritium must be created through a nuclear
process. The current Z-IFE design uses flibe to breed tritium. The proposed process for extracting
the tritium from flibe is explained in the Z-IFE transmutation report [5]. This section focuses on
minimizing tritium permeation from the chamber and the process piping.

_3.3.1 Tritium Permeation [23]_

Consider the fusion plant process sketch contained in Figure 3.16. The permeation
losses from the flibe circulation system are shown in the figure as heavy lines. Estimated losses are
on the order of 0.0467 grams per year for the flibe system. This includes all ten fusion chambers.
Such a loss rate would be slightly less than 1/20 [th] the total losses predicted for ITER. To ensure this
level of emission, the plant is constrained to a maximum operating temperature in the flibe
circulation loop of 850 K. The pipes necessary to achieve this rating were made of 304 stainless
steel with a permeation barrier having a permeation reduction factor (PRF) of 100. This is a fraction
of the probable permeation loss from the Z-IFE fusion plant. Additional work is needed to address
other likely tritium leak sources.

![](images/tmpvlzzzdgp.pdf-38-0.png)

![](images/tmpvlzzzdgp.pdf-38-1.png)

**Figure 3.16: Flibe Circulation Process Sketch**

The vacuum permeator shown in the process sketch (Figure 3.16) is the same device
recommended for ITER. The permeate side would operate at approximately 1x10 [-5] Torr. This
analysis makes the assumption that such a permeate pressure would result in a partial pressure on the
upstream side one order of magnitude higher, or 1x10 [-4] Torr (1.33E-07 bar).
Figure 3.17 contains one possible plant layout for the fusion plant with the flibe piping
discussed above. This is high temperature piping that is insulated with an outer metal sleeve.
Neither the insulation nor the outer sleeve was assumed to provide any impediment to tritium
migration.

[Figure 3.17: Conceptual 1 GW Fusion Power Plant Layout]

The piping shown in Figure 3.17 forms a dendritic header system with two main trunks. The header telescopes to maintain a pressure drop of 0.11 bar per 100 m (0.5 psi/100 ft). That is, header diameter varies as flow varies to maintain a constant pressure drop per unit distance. The pipe inventory used in this study is shown in Table 3.3. The total area of the piping system was increased by 25% to account for changes in elevation and other unaccounted length. While this level of allowance might be too small in tight quarters, the long lines of flat run justify it.

Piping was assumed to be 1.2 cm thick (0.5 inches). Actual pressure will be low, on the order of 1 atm gauge. Such pressure requires thin walls to contain it. Commercially in such cases, wall thickness is set by a minimum necessary to provide pipes robust enough to resist damage from handling and access during construction and operation. A typical specification for a pipe of this size (27" to 60" diameter) would be 1.2 cm (0.5 inches) thick, the wall thickness assumed herein.

## Table 3.3: Flibe circulation loop pipe statistics

| Piping Location | Run Count | Flow Rate (kg/s) | Run Length (m) | Pipe Diameter (m) | Surface Area (m²) | Total Length (m) |
|---|---|---|---|---|---|---|
| Laterals | 20 | 365 | 30 | 0.540 | 1700 | 1800 |
| 1–3, 2–4, 7–9, 8–10 | 4 | 1730 | 100 | 0.700 | 880 | 400 |
| 3 to 5, 4.6 | 2 | 3460 | 100 | 0.900 | 565 | 200 |
| 5, 6 to Ht Exchanger | 2 | 5190 | 100 | 1.10 | 691 | 200 |
| 9, 10 to Ht Exchanger | 2 | 3460 | 350 | 0.900 | 1980 | 700 |
| Heat exchanger external pipe | 1 | 8650 | 100 | 1.30 | 408 | 100 |
| | | | | Sub-total without contingency | 6220 | 3600 |
| | | | | Total with 25% contingency | 7770 | 3250 |

Tritium permeation estimates were made using the DIFFUSE tritium permeation code and the piping system specification discussed above [24]. The predictions were made for two materials. Results are plotted in Figure 3.18.

[Figure 3.18: Results of DIFFUSE Code — Graph showing permeation (tritium atoms·s⁻¹·cm⁻²) vs. Temperature (K) from 700–1200 K for multiple materials: Ferritic Steel (F82H) @ 16.4 bar, Stainless Steel (304SS) @ 16.4 bar, Stainless Steel (304SS) @ 36.7 bar (16.4 Ton), and Stainless Steel (304SS) @ 36.7 bar (16.4 Ton) with PRF = 100. The green (shaded) area presents a rough estimate of normal operating zone. Melting Point of Flibe ≈ 733 K is marked. Data points at 787 and 850 are indicated. Right axis shows Tritium Loss (tritium g/y). Scale ranges from 1.E+03 to 1.E+14 on left axis and 1.E-05 to 1.E+06 on right axis.]

Highest permeation rates were obtained using F82H, a type of ferritic steel designed for
low activation potential [25]. F82H steel performance for 1x10 [-4] bar partial pressure, a
concentration to be expected if tritium is allowed to accumulate without aggressive removal, is
depicted in the top curve of the figure. Substituting stainless steel (Type 304) reduced permeation
by up to three orders of magnitude at the same driving pressure difference, as shown by the second
from the top curve in the figure [26, 27]. The next curve down shows the impact of a lower partial
pressure similar to that possible on the permeate side of a vacuum permeator, 1x10 [-4] Torr (1.3x10 [-7]
bar). The last and lowest curve reflects the permeation of low partial pressure hydrogen through
pipe equipped with a permeation barrier. A permeation reduction factor (PRF) of 1000 has been
achieved in laboratories [28]. This lowest curve uses a PRF of 100 as a long term commercial value
to be expected after significant continued development.
Imposing limiting criteria on Tritium release will be difficult in the absence of such site
specifics as geography and weather and demographics. For now, the release will be compared to the
ITER results. In rough numbers, ITER is currently limited to 1 gram/year of tritium release based on
a 10 millirem allowable exposure at the site boundary which is about 1 km from the emission source.
A limit of 1.0 g/y of tritium imposed on this piping system equals 6.2x10 [7] tritium atoms per
centimeter per second permeation. The shaded box in the bottom of the curve reflects this limit.
The box is foreshortened on the left to limit the area where flibe is liquid. The box provides an
approximate map of operating space for the flibe system based on tritium release to atmosphere.
A reasonable operating temperature for a flibe system is 850 K. This allows operation
approximately 100 K above freeze point, and is still low enough to avoid undue impact to piping. At
this temperature, the piping system in question would allow a permeation loss of 3.8E06 tritium
atoms per cm [2] per second. For this system, such a permeation rate equates to a loss to atmosphere of
0.0467 g/y, slightly less than 1/20 [th] of the current ITER criterion of 1 g/y. This limited release must
now combine with such other sources as hydrogen piping, vessels and equipment, and periodic offdesign releases.

_3.3.2 Future Tritium Research_

1. Consequence modeling using MACCS2 or other atmospheric transport codes that relate
leakage rates to long term dose rates will be needed for future safety analyses. This will
require assumptions regarding plant location.
2. Estimate tritium leakage from the gas processing system piping. This will probably add a
significant mass per year to the 0.0467 g/y already accounted for.
3. Investigate a system that combines hydrogen (all forms) with carbon to form methane or
larger hydrocarbons. This effectively traps the tritium, reducing permeation to the point of
virtual elimination. This would allow hydrogen transport over long distances without loss.
It would, however, require reforming at the downstream end.
4. Investigate tritium losses across the steam boiler and superheater into the steam system and
the formation of tritiated water and possible subsequent leakage. This should be an easy
investigation as similar processes occur today at commercial nuclear power plants.
5. Investigate tritium losses from such operating equipment as pumps, compressors, valves,
flanges and other piping system components. These sources could be the most significant
source of tritium losses.
6. Investigate the best permeation barrier to use with temperatures in the 850 K range.

###### **3.4 Recyclable Transmission Line (RTL) and Flibe**

The RTL connects the target to the driver. It has to be designed in such away that it
does not add a significant amount of impedance to the path of the pulse. A significant portion of the
RTL is destroyed after each fusion event. The remaining material collects in the vessel and is
recycled for use in another shot. Since it is recycled after each shot the material must be such that it
is easily melted and formed into the appropriate shape. Ferritic steel has been studied extensively in
past Z-IFE studies as a candidate for the RTL material. Its abundance and chemical compatibility
with the liquid curtain material (flibe) makes it a viable choice. A steel RTL however requires an
extensive amount of energy (170 MWe of a 1000 MWe power plant) to remanufacture [31].
An alternative material to ferritic steel that has been investigated in the past was frozen
or frangible flibe. Using the same material for the RTL as the liquid curtain eliminates the issue of
material separations, and cuts down on manufacturing costs. Continuing optimization and
characterization of frozen salt properties has been investigated further this year and is presented in
section 3.4.1. Also, a proposed frozen flibe RTL design is discussed in section 4.2.1.
Flibe (LiF)2-(BeF2) and carbon steel remain the baseline materials for the Z-IFE power
plant. The University of California in Los Angles conducted experiments analyzing the interaction
between vapor ferritic steel and a molten flibe pool. The results are described below in section 3.4.2.

_3.4.1 Characterization of Frozen Salt Properties [29]_

For the design of frozen salt transmission line elements, the mechanical and dielectric
properties have to be well known. In preparation for measuring the electrical properties of flibe,
during 2005 an initial evaluation of the dielectric breakdown properties of ¾ x ¾” substitute frozen
salt samples has been made [29]. The Na2MgCl4 samples produced in 2005 were cast in POCO
graphite dies. The resulting surface carbon contamination provided enough electrical conductivity to
prevent measuring the dielectric constant, which will be needed for electrical modeling of the RTL
and to determine the appropriate driver impedance. In 2006, high purity Na2MgCl4 samples with a
diameter of 1” and a thickness of about 1/16” were successfully produced. These samples were cast
in a Hastalloy crucible. The salt was slowly heated to 480ºC under vacuum to remove water vapor.
Once a homogeneous molten layer was achieved without further out gassing, the crucible was
allowed to cool to room temperature slowly over a five hour time period to avoid tension and stress
cracking. The chamber was then filled with dry argon gas. Thin Cu foil was attached to both sides
of the sample exactly matching its diameter. The subsequent measurement of the dielectric constant
was performed under Argon atmosphere to prevent conductivity changes of the sample by hydride
formation. Two different devices were used: A calibrated Micona capacitance meter for DC
measurements and a HP auto balance bridge for measurements at DC and frequencies up to 1 Mhz.
were used. Table 3.4 summarizes the results of these measurements.

_3.4.2 Interaction of Ferritic Steel Vapor and Flibe [29]_

It has been expected that most of the RTL steel precipitates in the flibe coolant and can
be recovered by mechanical separation. However, recent calculations show that a large fraction of
the RTL (up to ½ of the total mass) will be vaporized and partially ionized by the discharge [32].
This plasma cloud composed of the constituents of ferritic steel (iron, chromium, etc) will expand
and interact with the neutral gas present in the background as well as with the excited and ionized
fluorine, lithium and beryllium that is generated by the absorption of the x-rays emerging from the
target in the surrounding flibe liquid. The goal of the experiments described here is the
characterization of the chemical composition and size distribution of the condensed vapor and
precipitated steel droplets.
Figure 3.19 shows a schematic of the Z-box facility (completed in 2005) and an
overview of the experimental hardware and the capacitor bank used to produce the discharge. The
Z-box has excellent optical access with large UV/visible view ports for high speed cameras and
optical spectroscopy. In addition, fast piezoelectric pressure sensors, Langmuir/Mach probes for
flibe plasma characterization, and RGA access are provided. In-situ handling of high temperature
molten salt and modifications of the experimental set-up in high purity argon are possible via gloves.
For evacuation, the glove ports can be sealed. Flexible heating configurations are provided for flibe
melting and casting.

**Figure 3.19: Z-Box flibe handling facility.**

![](images/tmpvlzzzdgp.pdf-43-0.png)

![](images/tmpvlzzzdgp.pdf-43-1.png)

![](images/page_043_table_0.png)

|  | εr (DC) | εr (500 kHz) | εr (1 MHz) |
|---|---|---|---|
| Auto balance Bridge | 4.5 + - 0.2 | 4.65 + - 0.25 | 4.7 + - 0.25 |
| Capacitance Meter | 4.4 + - 0.3 | | |

There are several difficulties in the laboratory handling of flibe, which greatly
complicate the experiments described here. The first difficulty is the control of the impurities
dissolved in the salt, which significantly modify the material properties. This limits the range of
suitable containing materials, diagnostics, etc. The second problem is related to the toxicity of
beryllium particulate in any of its chemical forms and composites which complicates handling and
modifications of the experimental set-up. The latter is a particularly severe limitation during the
initial scoping phase of this research and development project. Because of these issues the most
common beryllium free mixture of salts available are used in the experiment, sodium chloride NaCl
and magnesium chloride MgCl2.
Each element of the salt eutectic corresponds to an element in flibe but shifted down
one line in the table of elements: Li to Na, Be to Mg, F to Cl. This means that the electron valance
of the atoms is the same, and the eutectic chemical bonds are similar. This is confirmed by the fact
that the phase diagram of the two mixtures are actually quite similar, as shown in Figure 3.20 [33].
In addition, the thermochemical properties of the two compounds at high temperature are also very
similar.

**Figure 3.20: Flibe and Na2MgCl4 phase diagram.**

Na2MgCl4 is produced by mixing the salts in the same eutectic composition as flibe
(2/3 NaCl and 1/3 MgCl2 in moles). During this preliminary phase the substitute eutectic was
formed by heating the mixture inside a nickel crucible (chosen because of its inherent low reactivity
with molten salts) under high vacuum to eliminate water vapor residues. The mixture was then
heated to 900ºC to form the eutectic and subsequently cooled slowly. The eutectic was then remelted in less then 1 atmosphere of argon. Once liquid, the eutectic was conditioned further under
vacuum. During the experiments the salt was kept molten above the eutectic temperature of 470ºC.
The experimental investigation of the interaction of ferritic steel and molten salt vapors
was started at UCLA in 2005. Capacitor discharges (1-5 kJ) were used to vaporize and ionize
ferritic steel wire or mesh over a molten salt pool, using the beryllium free Na2MgCl4 instead of
flibe. The discharge vaporized some of the molten salt surface, and the vapor interacted with the
expanding metal vapors from the vaporized wire mesh (in these experiments, 300 mg of steel wool

![](images/tmpvlzzzdgp.pdf-44-0.png)

with a wire diameter of 2 μm was used). The analysis of the process was performed by using high
speed/video cameras, spectroscopic diagnostics and by surface characterization of the deposited
precipitate. Figure 3.21 shows a schematic of the experimental set-up.

**Figure 3.21** : **Experimental Set-up showing 3” nickel crucible bedded in heater plate (center)**
**with detachable heater connections (left), glass-shielded transmission line elements leading**
**to the capacitor bank (in green), and the centrally mounted wire mesh (purple).**

Figure 3.22 shows a video frame of the discharge and the glowing salt surface recorded
in the next video frame. Heating of the salt layer is mainly due to the anodic plasma heat flux which
may peak at 20-50 kW/cm [2] .

![](images/tmpvlzzzdgp.pdf-45-0.png)

![](images/tmpvlzzzdgp.pdf-46-0.png)

**Figure 3.22: The video frame showing the plasma discharge (left) and the immediate**
**following frame (right).**

A time-integrated spectrum acquired with an Ocean Optics USB 2000 compact
spectrometer shows high intensity sodium, magnesium, and chlorine lines from the molten salt pool
(in addition to the Ar lines from the nearly fully ionized background gas) as well as iron lines from
the exploding wire, which confirm the presence of these materials in the arc plasma. After
accumulating 20 discharges (4 kJ each), the 3” diameter pyrex cylinder surrounding the discharge
was removed after a clean dry argon vent of the chamber, stored in argon, and examined by SEM
and EDX. A 100-200 μm thick salt layer was found on the inside wall of the pyrex tube. Figure
3.23 shows an oblique and perpendicular view of the pyrex surface. The surface morphology shows
a re-deposited salt layer and abundant salt droplets (20-500 μm size, clearly visible in the oblique
view). The perpendicular SEM view (Figure 3.23 (right)) shows clusters of iron droplets with a
typical size distribution of 0.1-30 μm peaked around 25 μm (bright features). The purity of the salt
was confirmed by the EDX spectrum taken in a region free of iron droplets (Figure 3.24). The
oxygen peak was due to air (moisture) exposure in connection with the SEM work. The other
impurities, Ni and Si, originate from the crucible and pyrex. The iron concentration of ~0.5 atompercent was typical for the regions free of visible droplets and represents a lower bound of the iron
content due to re-deposition and vapor condensation. The EDX spectrum originates from a surface
layer 2 μm in depth. Integrating over the re-deposited part of the pyrex surface and assuming codeposition of salt and iron, the minimum vaporized/sputtered iron quantity was calculated as 0.8 mg
(or 0.04 mg per discharge shot).

![](images/tmpvlzzzdgp.pdf-47-0.png)

**Figure 3.23: (Left) Oblique view of inner pyrex cylinder wall (the large salt droplet is 300 μm**
**wide). (Right) A Perpendicular view showing salt and embedded steel droplets.**

**Figure 3.24: EDX surface analysis: 500x500 μm refion free of iron droplets.**

The EDX spectrum of a typical iron droplet (partially covered with salt) is shown in
Figure 3.25. Figure 3.26 shows another region containing small steel fragments. Since the pyrex
tube is an insulator, droplets smaller than 0.1 μm could not be directly observed due to space charge
limitations in the SEM.

![](images/tmpvlzzzdgp.pdf-47-1.png)

![](images/tmpvlzzzdgp.pdf-47-2.png)

![](images/tmpvlzzzdgp.pdf-48-0.png)

![](images/tmpvlzzzdgp.pdf-48-1.png)

**Figure 3.25: EDX spectrum of 2 μm steel droplet indicated in Figure 3.23(right).**

**Figure 3.26: Region containing clusters of small steel droplets (0.1-1 μm typical size).**

![](images/tmpvlzzzdgp.pdf-48-2.png)

_3.4.3 Chamber Dynamics [29]_

**3.4.3.1** **Reactivity and Recycling of Transmission Line Elements**

The vapor dynamics and chemical interactions of the excited/ionized vapors in the ZIFE chamber will determine in which form the atoms recombine and ultimately precipitate in the
coolant. Predicting the composition of the precipitate is crucial for evaluating which processes
would be effective in the recovery of vaporized/precipitated transmission line material from the
coolant loop and to design suitable means of chemical separation from the coolant.
The negative free energy of formation of lithium fluoride LiF and beryllium fluoride
BeF2 is the highest among the metal elements that would be present, at -524.2 KJ/mol and -445.4
KJ/mol respectively per fluorine atom at 1000ºC [34]. For comparison, that of iron fluoride FeF2 is 126 KJ/mol and that of chromium fluoride CrF2 is -157.4 KJ/mol. Thus, from equilibrium
considerations, the free fluorine generated by the vaporization of flibe is expected to recombine
more likely in its original chemical form. However, the recombination process is highly dynamic
and the precipitate composition is expected to depend on the plasma dynamics and the density and
temperature dependent recombination rates more than on equilibrium properties. Using the
substitute eutectic described above in section 3.4.2, our work in 2006 is directed towards the
experimental determination of the recombination rates of excited salt and ferritic steel vapors. In
addition to the similarities between flibe and Na2MgCl4, the ratio of the free energies of formation of
NaCl and MgCl2 to the energy of formation of FeCl2 are quite similar to the case of flibe, as outlined
in Table 3.5.

**Table 3.5: Free energy of formation (kJ/mol per fluorine/chlorine atom) for flibe components**

![](images/tmpvlzzzdgp.pdf-49-0.png)

![](images/page_049_table_0.png)

|  | T = 1000 K | T = 5000 K |
|---|---|---|
| **LiF** | -401.3 | -272.1 |
| **BeF2** | -445.4 | -279.5 |
| **FeF2** | -212.0 | -126.0 |
| **CrF2** | -157.4 | -5.0 |

|  | T = 1000 K | T = 5000 K |
|---|---|---|
| **NaCl** | -238.2 | -95.6 |
| **MgCl2** | -205.6 | -46.6 |
| **FeCl2** | -93.5 | -22.8 |

Regarding the separation of metal halides in the flibe coolant loop, hydro-fluorination
has been investigated in the MSRE program for the removal of fluorides (by hydrogen injection) [35,
36]. This process can be used in principle to reduce halides like FeF2, although the removal of the
precipitated metal is difficult and has not been successfully demonstrated. The removal of CrF2 is
very difficult due to the low reactivity with hydrogen. Hence, future work will include measurements
of the recombination rate of free fluorine and chromium in order to estimate the quantity of CrF2
produced during the Z-IFE fusion pulses.

**3.4.3.2** **Recombination Rate Experiments and Calculations**

Initially, the ferritic steel vapor for the recombination experiments was generated using
the exploding wire technique, using the pulsed power capability of the Z-box. The main drawback
of the exploding wire technique is the low pulse rate due to the vacuum vent required in between
pulses for the exchange of the wire. Recently a different approach was used. A pulse hollow
cathode discharge (HICAT [37], see Figure 3.27) was integrated into the Z-Box. HICAT is operated
in He or Ar gas at pressures of 0.1- 6 torr and allows repetitive discharges with a typical pulse rate of
2-5 discharges per minute. For the recombination experiments, the cylindrical cathode of HICAT
was lined with ferritic steel foil or a thin layer of #0000 steel wool. Fe vapor is generated primarily
by ion sputtering. The concentration of Fe vapor can be controlled to some extent by the total
discharge energy. Two different methods for providing free chlorine were explored. In the first
approach, a heated Ni-coated crucible containing the molten salt eutectic or a wire coated with 200
mg of salt is placed near the HICAT device. In the second approach, a variable proportion of
chlorine gas was mixed with the background gas to vary the free chlorine concentration
independently.

**Figure 3.27: Schematic/image of HICAT device**

The spectroscopic analysis is based on time-resolved line intensity measurements of the
(fully dissociated) atomic species. A cross section of the arc discharge is viewed via a fiber optic
coupler. Two double monochromators (2x Jarrel-Ash 0.25 m or Spex 1680) with attached
photomultiplier detectors are used to measure the time resolved line intensities of spectral lines
characteristic of the molten salt constituents and the vaporized metals. Atomic energy level
populations depend on both the atomic number density and electron density, and on the electron

![](images/tmpvlzzzdgp.pdf-50-0.png)

temperature. In the high density, low temperature arc plasmas are considered, the approximation of
Local Thermodynamic Equilibrium (LTE) holds typically for temperatures above ~0.8 eV [38]. The
temperatures of the different atomic species can then be considered equal and also equal to the
electron temperature, and the population density of the atomic energy levels follows a MaxwellBoltzmann distribution. Since the plasma temperature evolution can be determined from the line
intensity ratio using a pair of lines from the same element (but different ionization stage) provided
the transition probabilities, upper level energy, and statistical weights are known. The spectroscopic
information can be used to extract the relative density of both the molten salt constituents and the
ablating metal as a function of time by analyzing line intensity ratios (for example, IBe I/ IFe I, ILi I/ IFe

I). Information about molecular recombination rates of the salt constituents in the presence of metal
vapor can be deduced provided the time evolution of suitable spectral lines for all constituents is
analyzed. The measurements of the substitute eutectic salt used to develop the diagnostic procedure
and analysis are reported.

**Figure 3.28: Typical argon plasma density and temperature evolution from spectroscopic**
**line ratio measurements.**

![](images/tmpvlzzzdgp.pdf-51-0.png)

![](images/tmpvlzzzdgp.pdf-52-0.png)

**Figure 3.29: Emission spectrum with salt and ferritic steel present.**

In principle, the time evolution of the Fe, Na and Cl density can be determined from the
time evolution of the emission line intensities once the plasma temperature and density evolution is
known. Recombination of free fluorine (or chlorine for the substitute salt) with metal (Li, Be, Fe, Cr
or Na, Mg, Fe, Cr in the substitute case) is weakly temperature dependent. However, since the
temperature evolution of the plasma pulse depends on the local arc plasma heat losses and cannot be
independently controlled, a double pulse technique to determine the time decay of Fe, Na, and Cl
densities was used (Figure 3.30). This technique allows the decoupling of the recombination
dynamics from the intrinsic plasma temperature evolution. The first (high energy) pulse is used to
produce and excite/ionize Fe and salt vapor. The second (low energy) pulse is applied with a time
delay and is used to re-excite the amount of Fe still present at that time. The iron density ratio can
be directly evaluated from the line intensity ratio of the two pulses and is a measure of the
recombination rate. Helium (typically at 1.5-3 torr pressure) is used as background gas to produce
the plasma. Helium has the advantage of a simpler emission spectrum with less masking of
potentially interesting metal and salt emission lines.
The recombination rate for steel vapor was measured with this method. Figure 3.31
shows the time history of the discharge current and the Fe I line intensity, and Figure 3.32
demonstrates that the Fe intensity ratio (second pulse intensity divided by first pulse intensity) is
inversely proportional to the chlorine concentration indicating strong reactivity. The time delay
between the pulses is Δτ = 180 μs. The useful data range extends to a chlorine concentration of
about 120 (a.u.). At higher concentration the iron density at the time of the second pulse is too low
to be measured reliably. The measured recombination rate at the highest chlorine concentration (1
x10 [-8] mol/cc corresponding to 150 mtorr) is ~ 10 kHz, corresponding to a rate constant 2x10 [12]
cc/mol-s (at a helium pressure of 1.5 torr). The expected recombination rate coefficients for fluorine
with Li and BeF and Fe, and for chlorine with Na, Mg, and Fe have been calculated. Reliable
thermodynamic data are only available up to a temperature of 5000 K, while the plasma temperature
in our experiment is 20000-25000 K (2-2.5 eV) [35].

![](images/tmpvlzzzdgp.pdf-53-0.png)

**Figure 3.30: Time resolved measurement of species density.**

**Figure 3.31: Iron I line intensity ratio (pulse 2/pulse 1) verse the relative chlorine density in**
**the plasma, as evaluated from the 522 nm CI II emission line.**

**Figure 3.32: Time evolution of the discharge current and Fe I (385.8 nm) line intensity.**

![](images/tmpvlzzzdgp.pdf-53-1.png)

![](images/tmpvlzzzdgp.pdf-53-2.png)

In the limit of low densities (which applies to the conditions expected in Z-IFE as well
as to the experiments) vapor recombination rate as the result of three-body collisions and the
recombination rate is proportional to the background (Helium) gas density. The recombination rates
can be calculated from the dissociation rate. In the so-called strong collision regime, the dissociation
rate is [39,40]

                 - _Eo_
###### [ M ] Z I, J [ρ vib ( Eo ) kT / Qvib ] e kT Fanh FE Frot Frot,int

![](images/page_054_eq_0.png)

                  - _o_
###### = [ M ] Z [ρ ( E ) kT / Q ] e kT F F F F 3.5

![](images/page_054_eq_1.png)

###### k odiss = [ M ] Z I, J [ρ vib ( Eo ) kT / Qvib ] e kT Fanh FE Frot F

Here,

![](images/page_054_eq_2.png)
###### Z I, J = N A σ A 2− M (8π kT / μ A − M )1/ 2 Ω A − M 3.6

is the gas-kinetic binary collision frequency, ρvib is the vibrational density of states, Qvib is the
vibrational partition function, Eo is the activation energy, and the factors F are corrections due to
rotational and vibrational oscillations. The recombination rate is calculated using the equilibrium
dissociation constant

![](images/page_054_eq_3.png)
###### [ A ][ B ] p K c = [ AB ] = RT exp(− Δ Go / RT ) 3.7

Here [A], [B], and [AB] are the molar densities of the two constituent atoms and the product
molecule, and - ΔG0 is the Gibbs free energy of formation. The recombination rate is then given by:

_k_ 0 _rec_ = _kodiss_ / _K_ _c_ 3.8

These rates are calculated for equilibrium conditions which may marginally hold for the expected
high density in Z-IFE plasmas.

![](images/tmpvlzzzdgp.pdf-55-0.png)

**Figure 3.33: Calculated three-body recombination rate constant for flibe components and**
**iron in Argon gas (T= 5000K).**

**Figure 3.34: Three-body recombination rate constant for NA, Mg, and Fe with Cl in Helium**
**gas (T=5000K).**

![Figure 3.33 and Figure 3.34 show a comparison of the calculated gas phase](images/tmpvlzzzdgp.pdf-55-1.png)
recombination rates for Li +F > LiF, BeF + F > BeF2. and FeF + F > FeF2 for T = 5000 K. verse the
background gas concentration [M] for Argon. The latter rate is calculated to be much larger than the
flibe recombination rate constants. A similar scenario is also found for the substitute salt, where the
reaction Fe + Cl > FeCl is calculated to be larger than the recombination rate constants for NaCl,
MgCl2, and the reaction Fe + FeCl > FeCl2. It should be noted that FeF and FeCl exist only at high
temperature in the gas phase and are not very stable but may subsequently react with fluorine and
chlorine to form stable iron halides. In summary, the preliminary experimental evidence of large
recombination rates for iron-chlorine reactions is consistent with calculated results. These results
indicate that reaction rates of fluorine with transmission line material may be high, and an effective
scheme for reduction/removal of metal halides may be needed.
Substantial progress has been made in evaluating the condensation and recombination
behavior of molten salt plasmas. The deposition of evaporated/sputtered iron from a molten salt
plasma have been investigated. Preparations for tests involving a Sn wire/mesh are underway.
Molten salt vacuum casting has been refined and high purity samples have been produced in
preparation for electrical/mechanical testing of cast flibe. The dielectric constant of the substitute
Na2MgCl4 has been measured. First measurements of the iron recombination rate constant in a
molten salt high density plasma have been made and suggest large reaction rates of iron with
chlorine/fluorine. Based on these results, more comprehensive studies of the reaction kinetics of
molten salt plasmas with iron and chromium will be needed in the future. Upgrading the
spectroscopic capabilities by adding a second higher resolution (1 Angstroem) spectrometer will
allow simultaneous measurement of emission lines from different elements. In addition, an effective
means of separating out metal halides and precipitated metal from liquid flibe need to be
investigated. The detailed spectroscopic work as well as initial separation experiments can be
carried out with Na2MgCl4 which allows much more flexible experimentation.

###### **3.5 Automation**

The ZPoP (Proof of Principle) dynamic simulation from 2005 provides a detailed view
of the automation needed for the Z-Pinch Power Plant while loading a single RTL into the chamber
and removing it from the chamber. ZPoP also provides information on the automation required for
an energy pulse delivered to a single chamber given through a recyclable transmission line (RTL).
The baseline Z-IFE power plant operating at 0.1Hz will have ten chambers emitting high energy
pulses simultaneously. This overview will discuss some of the considerations that should be
accounted for in the full scale power plant operating at 0.1Hz.

_3.5.1 Plant Layout_

The overall layout of the Z-IFE power plant will largely determine the automation that
will be required. The ZPoP simulation featured a conveyor system by WARD Systems Inc. This
system contains a conveyor and battery powered Power Pallets that carry payloads along the
conveyor. In the case of the ZPoP simulation, the payloads are the RTLs. A main controller is used
to control the movements of the conveyors. The conveyor costs $250 per foot and each pallet is
$30,000. The WARD Power Pallets will travel at speeds over 350 ft/min (roughly 3.98 mi/hr). If
the WARD System is used, this speed will constrain RTL travel along the conveyor in addition to
the overall layout of the conveyor system.

![](images/page_056_table_0.png)

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| layout | conveyor | system. |  |  |  |  |  |
|  |  |  | 57 |  |  |  |  |

In order to determine the length of conveyor and the number of power pallets required,
the overall design of the plant layout is needed. Some of the important features of the plant layout
will include the location of the chambers and the spacing between the different conveyors. Figure
3.35 illustrates several of the major events in handling the RTLs beginning from removing the new
RTLs from the storage facility (1) to the removal of used RTLs to be recycled at the manufacturing
plant (7).

**Figure 3.35** : **Major Stages in transferring RTL**

As is illustrated in Figure 3.35, the RTL will be transferred to many locations within a
short span of time. The ZPoP simulation demonstrates that it is dynamically feasible to insert an
RTL into the chamber, remove it from the chamber and replace the used RTL with a new RTL. In
the full-scale power plant ten of these cycles will be staggered at one per second so that each
chamber operates at 0.1 Hz. Therefore, it is important to consider the most efficient plant layout that
will allow for easy loading of the RTLs from storage, to the chambers, and then back to the
manufacturing plant.

_3.5.2 Loading New RTLs and Unloading used RTLs_

Another key factor in the automation design is loading the new RTLs from the RTL
storage and removing the used RTLs to be remanufactured. Whether or not the RTLs enter single
file on one conveyor line or arrive on several conveyor lines to conserve time has yet to be
determined. It is likely that the removal of the used RTLs could occur similarly to loading the new
RTLs.

![](images/tmpvlzzzdgp.pdf-57-0.png)

RTLs will be manufactured and remain in storage until they are ready for use.
However, it is important to decide the number of RTLs that will be on the conveyor at any given
time to determine the approximate amount of Power Pallets to purchase. In addition, the Power
Pallets carrying the used RTLs will need to be cycled back to the RTL storage to transport new
RTLs to the chambers.

_3.5.3 Future Work_

Future work regarding the automation for the Z-IFE Power Plant involves determining
a plant layout that allows for efficient loading and removal of RTLs from storage and back to the
manufacturing facility. The plant layout must also allow the power pallets to easily transfer the
RTLs to each of the ten chambers based on the energy pulses occurring every ten seconds.

###### **4 CHAMBER DESIGN AND SHOCK MITIGATION**

A z-pinch IFE driven power plant has several advantages over laser or heavy-ion driven
concepts. Laser and heavy-ions require high vacuum conditions so that the energy path to the target
is unobstructed. This limits x-ray and neutron attenuation mechanisms such as gas or liquid, which
can greatly reduce the impact on containment chamber wall. As a result, the laser or heavy-ion
driver reactor chambers are very large to take advantage of the inverse square law that describes the
attenuation of photon intensity with distance. Z-Pinch driven IFE directly links the power source to
the target through a transmission line. This allows a myriad of shock mitigation schemes without
having the concern of obstructing the path of lasers or heavy-ion beams. Absorbing the x-rays could
greatly reduce the chamber radius needed to contain the fusion reaction.
The chamber for a z-pinch driven IFE reaction must survive under harsh conditions. It
is constantly being bombarded with neutrons, RTL and target shrapnel, and x-rays. The high energy
neutrons from the D-T reaction displace atoms in the crystal lattice of the chamber wall. This causes
embrittlement which can greatly reduce the integrity of the wall over a long period of time. The
major cause of immediate degradation in the containment vessel is x-rays depositing their energy
into a small volume of chamber wall. This creates large temperature gradients in the wall, resulting
in ablation that drives a shock wave through the material. This shock wave can destroy a chamber
rapidly, and since IFE power plants require fusion events on the order of 0.1 to 1 Hz, it is clear that
such a situation makes it impossible for a wall to last the life-time of the plant. Therefore, a shock
mitigation scheme must be implemented into the chamber to absorb all or most of the x-ray energy.
Several mitigation schemes are presented in this section.
Two fundamentally different chamber designs have been proposed for the Z-IFE power
plant. The first was a thick liquid curtain design which mitigates the x-rays and neutrons before they
interact with the chamber wall. The second design used gas or aerosols to mitigate the x-rays while
allowing the neutrons to pass through the chamber wall (first wall design).
Experiments at the University of Wisconsin and University of California in Berkeley
have been conducted studying the effects of shock mitigation through two-phase liquid with a small
void fraction and thick liquid curtains respectively. Also, experiments characterizing two-phase
turbulent jets have been conducted at The Georgia Institute of Technology. The results of the
models and experiments are discussed below.
A new first wall chamber design has been proposed this year in response to some
promising modeling results of aerosol mitigation. Aerosols have shown to be effective x-ray
absorbers up to Z-IFE power plant target yields, which can sufficiently protect the chamber of a
much smaller radius. A disadvantage of this design is that there is no protection from the high
energy neutrons impacting the chamber wall. This issue may be addressed through thermal
annealing. Thermal annealing has proven to effectively heal LWR pressure chamber walls and
welds by allowing atoms to diffuse back into the gaps of the crystal lattice [41]. Thus, if the
chamber is kept at an elevated temperature neutron embrittlement may not be an issue. RTL
shrapnel may be a concern but may only have a second order effect on the vessel wall for both the
thick liquid curtain and first wall chamber designs. The first wall chamber design has several
advantages over the thick liquid curtain design but presents a whole new set of science and
engineering issues that must be addressed in future studies.

Experiments on ZR are discussed briefly below which are outlined in more detail in the
Advance Fusion Concepts Grand Challenge LDRD [1]. These will help provide crucial information
on x-ray mitigation using gases, aerosols, and thick liquid curtains. They will also be necessary for
demonstrating complete containment of tritium. These experiments are shown on the critical path of
the roadmap and are necessary before a ZN facility can be designed and built.
Due to the cyclical nature of an IFE power plant design, fatigue will be great concern
when designing the chamber. The ductility of the chamber plays a large role in determining a
material’s fatigue limit. The fatigue limit should be the main design parameter for the chamber
instead of the maximum allowable stress based on a static pressure, which was used in previous
studies. A first order fatigue analysis is described in section 4.2.5 for F82H steel in an attempt to
predict that maximum design stress of the chamber.

###### **4.1 Shock Mitigation**

Shock mitigation within the reaction chamber is a crucial stepping stone on the way to
developing fusion energy systems. Since a large percentage of D-T fusion reactions are in the form
of x-rays, approximately 30%, most of that energy must be mitigated to dampen or eliminate a
shock. The x-rays, if no mitigation medium is used, will deposit their energy into a very small
volume of the chamber wall causing it to ablate, generating a catastrophic shock. An attenuating
medium such as gases, aerosols, thick liquid curtains, and foams allow the x-rays to deposit their
energy over a large volume thus mitigating or preventing a shock. Gas may be used for lower power
fusion yields on the order of 10 MJ while aerosols, foams, and liquid curtains are needed for larger
yields.

_4.1.1 Shock Mitigation Roadmap_

The initial set of shock mitigation experiments can be performed on Z-beamlet. Zbeamlet is a high power laser that can simulate intense photon environments as would be seen in a
fusion reaction. X-rays can also be generated using this laser to further simulate a fusion event. The
only limitation may be that the energy of the x-rays produced will not match that generated by a
fusion reaction but still may be able to effectively demonstrate mitigation. Savings in both cost and
time make experiments with Z-beamlet an attractive option as compared to ZR, so many of the
initial x-ray mitigation experiments can be conducted in this facility. Once a mitigation scheme has
been chosen to be the most promising, then it can be further tested on ZR.
The experiments on ZR will show that the x-rays can be mitigated sufficiently
minimizing the impact to the chamber wall. The sealing of the containment chamber and
transmission line post shot will also be demonstrated with these experiments. Several of the
diagnostics required for these experiments will be available on ZR such as: a calorimeter to measure
total radiated energy from the pinch with no time resolution, a total energy and power diagnostic
(TEP) tool that measures peak pinch power levels up 350 TW, and a transmission grating
spectrometer (TGS) to measure the time-resolved spectrum of the x-ray source. Thermocouples,
strain gages, and gas detection equipment will also be needed but are readily available through
outside vendors.
Over several years of containment studies the experiments will transition to
demonstrating the containment of tritium from D-T fusion reaction. Showing that tritium can be
contained safely is a crucial step for moving forward for both defense testing and power production
of z-pinch technology. An illustration of the possible experimental setup on ZR is shown in Figure
4.1.

![](images/tmpvlzzzdgp.pdf-61-0.png)

**Figure 4.1: Illustration of a possible experimental setup on ZR.**

A more detailed description of these experiments can be found in the Advanced Fusion
Concepts: Grand Challenge LDRD [1].

_4.1.2 ALEGRA Modeling of Gas Mitigation_

ALEGRA, a shock physics code developed at Sandia National Laboratories, was used
to estimate the amount of ionization of the gas, the temperature rise in the vessel wall, and the
resulting heat load caused by a z-pinch driven IFE event. Plasma phenomena such as
bremsstrahlung radiation, electron thermal conduction, material opacity, and radiation transfer were
considered. ALEGRA currently does not consider plasma viscosity, a potentially-important
diffusive mechanism [43, 44, 45].
Two models were created in ALEGRA. The purpose of the first model was to
benchmark ALEGRA with experimental data. The second model simulates a Z-IFE like
containment chamber filled with argon gas that houses a target capable of generating 10 MJ of xrays. This would simulate more of a test type environment leading up to full scale experiments at
power plant yields.

**4.1.2.1** **ALEGRA Simulation of Laser Ionization of Argon Gas Experiment**

In order to benchmark ALEGRA for the simulation of electromagnetic radiation
incident upon a gaseous environment, an experiment conducted at the University of California at San
Diego was modeled [46, 47]. The laser provided 155 mJ for 8 ns at a pulse of 532 nm. The argon
gas was initially at 1 atmosphere and room temperature.
Various quarter-symmetry circular 2D Cubit meshes were generated. The simulation
used ALEGRA’s “radiation hydrodynamics conduction” modules with an Eulerian mesh option.
Whereas multiple time-step schemes are available, a constant time step of 5.0E-12 seconds was
initially selected. The calculational time step and mesh size were reduced until the solution was
spatially and temporally resolved.
The radiation package called the linearized diffusion model with a flux limiter based on
Larsen. The boundary conditions were such that there was no displacement and no heat flux along
the symmetry of the mesh. Additionally, the symmetry surfaces employed reflective boundaries.
Because ALEGRA requires a curve in 2D geometry for temperature boundary sidesets, the reader
will notice that a small segment of the mesh’s inner radius was clipped off (see Figure 4.2). This
was done to incorporate a sideset which allowed the blackbody emission of the laser photons that
were emitted for 8 ns.

The argon gas was modeled using the following material models:

       - ideal gas equation of state (EOS)

       - Spitzer thermal conductivity

       - XSN and CDF opacity models (Rosseland, absorption, and scattering)

**Figure 4.2: Semi-coarse laser mesh.**

As shown by Table 4.1, the agreement between ALEGRA and the laser experiment was
quite good. Temperatures, spark length, and degree of ionization were predicted between a few
percent to up to 15% error. The ionization was measured in the experiment by using optical

![](images/tmpvlzzzdgp.pdf-62-0.png)

emission spectroscopy. According to personal communication with Sivanandan Harilal, most of the
spectral lines were due to Ar+ (singly-ionized argon), but some Ar++ (doubly-ionized argon) was
also spotted [48]. ALEGRA calculated a maximum (averaged) ionization of 1.9, which compares
very well with the 2 levels of ionization seen in the experiment. Figure 4.3 compares the spatial
evolution of the argon spark. The ALEGRA quarter symmetry results are shown on the far left.
These are to be compared directly with the quarter-symmetry data. As the figure shows, the
agreement is excellent. For added convenience, the full-geometry data are shown on the far right of
the figure. Notice that the data’s shape tended to be spherically symmetrical for the most part. It
should be pointed out that despite the reasonable agreement, better agreement is expected if
ALEGRA’s two-temperature models are used. Currently, due to time constraints, thermal
equilibrium between the ions and electrons was assumed.

**Table 4.1: Comparison of Laser Experiment Data with ALEGRA Simulation**

![](images/tmpvlzzzdgp.pdf-63-0.png)

![](images/page_063_table_0.png)

| Parameter | Data | ALEGRA |
|---|---|---|
| T_max at 22.9E-9 s (K) | 35,972 | 35,673 |
| T_max at 100.0E-9 s (K) | 20,590 | 25,673 |
| ΔX_peak (maximum transverse length) at 22.9E-9 s (mm) | 4.0 | 4.4 |
| ΔX_peak (maximum transverse length) at 100.0E-9 s (mm) | 5.5 | 5.2 |
| maximum ionization distance during transient | 1 | 1.9 |

![](images/tmpvlzzzdgp.pdf-64-0.png)

**Figure 4.3: Spatial evolution of the argon spark as a function of time (UCSD laser data**
**courtesy of Sivanandan S. Harilal).**

**4.1.2.2** **ALEGRA Simulation of X-ray Ionization of Argon Gas within a Z-IFE Chamber**

Cubit meshes were generated for 2 and 3D models representing 1/8 of a sphere. The
relevant parameters were assembled into Table 2 for convenience. Like the laser simulation, the X
ray simulation also employed ALEGRA’s “radiation hydrodynamics conduction” Eulerian modules.
In fact, many of the modules were similar, as will be shown later.
Whereas multiple time-step schemes are available, the authors chose a constant time
step of 5.0E-12 s as a starting point. The calculational time step and mesh were reduced until the
solution was spatially and temporally resolved. For quick turnaround testing, a 2D, extremely coarse
mesh with about 2,000 elements was used. For the final calculations, about 65,000 elements were
used.
The radiation package called the linearized diffusion model with a flux limiter based on
Larsen. The boundary conditions were such that there was no displacement and no heat flux along
the symmetry of the mesh. Additionally, the symmetry surfaces employed reflective boundaries.
The outermost curve of the 2D mesh (the steel wall) was set at a constant temperature boundary
condition (300 K). This temperature did not matter much, as the relatively slow transient heat
conduction response of the steel meant that the outermost radial elements of the steel mesh changed
very little with respect to time. Because ALEGRA requires a curve (2D) or surface (3D) for

temperature boundary sidesets, the reader will again notice that a small segment of the mesh’s inner
radius was clipped off; see Figure 4.4. This was done to incorporate Sideset 2, which allowed the
blackbody emission of the 1.0 keV X rays that were emitted for a given time (1.0E-09 s in this case).
It should be pointed out that such numbers can be easily modified to whatever number
is desired. For example, even though the black body may be at 3 keV, only 1 keV was considered.

**Figure 4.4: Coarse 2D (left) and 3D (right) Z-IFE chamber meshes**

The argon gas was modeled using the following material models:

  - ideal gas EOS

  - Spitzer thermal conductivity

  - XSN and CDF opacity (Rosseland, absorption, and scattering)

The steel was modeled using the following material models:

  - Mie-Gruneisen EOS

  - Spitzer thermal conductivity with cold material interpolation,

  - XSN and CDF opacity

The Spitzer thermal conductivity was linearized from a room temperature thermal conductivity (16
W/mK).

**4.1.2.3** **Z-IFE Simulation Results**

As the simulations began, the strong x-rays quickly ionized the first few centimeters of
the argon gas, where the average ionization z was 15.6. At this point in the chamber, the plasma
temperature peaked at 1.25E6 K. Because of its strong dependence on temperature, the argon
opacity quickly reached very high values, causing the x-ray energy to not penetrate beyond the high
temperature region. For example, at room temperature, opacity was near zero, but climbed steeply
to about 1.39E5 m [2] /kg. This meant that energy transfer was limited to the diffusion of heat via

![](images/tmpvlzzzdgp.pdf-65-0.png)

electron thermal conduction. This generated a Marshak wave that initially propagated at about
100,000 m/s, but that gradually slowed down as the plasma spread outwardly and its temperature
cooled. By the time the plasma hit the steel wall 1 m later, the Marshak wave was only moving at
about 10,000 m/s. Furthermore, the plasma that struck the steel wall was about 25,000 K initially,
with an average ionization of 1.9. Despite its high temperature, the plasma temperature adjacent to
the wall quickly dropped as heat was conducted to the innermost layer of the steel wall.
Nevertheless, the peak temperature at the inner surface was about 1,900 K. For comparison
purposes, steel melts at about 1,700 K. It must be noted that because of the relatively-slow heatconduction diffusion time of steel, only the first two innermost steel elements were above the melt
point, and the rest remained cool. This implies that only about 0.00006 m of the steel wall melted,
with the rest (0.03994 m), remained well below the melting point. Note that the excessive heat-up of
the innermost part of the steel wall can be minimized relatively easily by placing a liquid wall that so
it convects away the heat from the steel wall. For convenience, the key transient parameters are
summarized in Table 3.

**Table 4.2: Z-IFE X-ray simulation key output.**

Figure 4.5 through Figure 4.10 show the transient temperature, zbar, Rosseland opacity,
absorption opacity, pressure, and electron thermal conduction at 1 and 500 ns.

![](images/tmpvlzzzdgp.pdf-66-0.png)

![](images/page_066_table_0.png)

| Parameter | Magnitude |
|---|---|
| Peak Argon Plasma Temperature (K) | 2.5E4 |
| Average Temperature of Argon Plasma that Reaches Steel Wall (K) | 1,900 |
| Peak Steel Wall Temperature (K) | 1,900 |
| Minimum Ionization of Argon Plasma Adjacent to the Steel Wall | 15.6 |
| Peak Marhsak Wave Velocity (m/s) | 1.0E5 |
| Minimum Marshak Wave Velocity (m/s) | 1.0E4 |
| Peak Absorption Opacity (m²/kg) | 1.39E5 |
| Peak Rosseland Opacity (m²/kg) | 3.7E8 |
| Peak Pressure (Pa) | 3.7E8 |
| Peak Electron Thermal Conductivity (W/m-K) | 6.04E4 |

![](images/tmpvlzzzdgp.pdf-67-0.png)

![](images/tmpvlzzzdgp.pdf-67-1.png)

**Figure 4.5: Argon temperature (K) at 1 and 500ns.**

**Figure 4.6: Argon zbar (-) at 1 and 500 ns.**

![](images/tmpvlzzzdgp.pdf-67-2.png)

![](images/tmpvlzzzdgp.pdf-67-3.png)

![](images/tmpvlzzzdgp.pdf-67-4.png)

![](images/tmpvlzzzdgp.pdf-67-5.png)

![](images/tmpvlzzzdgp.pdf-68-0.png)

![](images/tmpvlzzzdgp.pdf-68-1.png)

**Figure 4.8: Argon absorption opacity (m** **[2]** **/kg) at 1 and 500 ns.**

**Figure 4.9: Argon pressure (Pa) at 1 and 500 ns.**

**Figure 4.10: Electron thermal conductivity (W/m-K) at 1 and 500 ns.**

Finally, Figure 4.11 shows EFLUX and PFLUX. EFLUX is defined as the net, timeintegrated energy that has flowed across a surface (or curve in 2D). PFLUX is the total power
computed at a given time step for a given surface. Therefore, PFLUX should be zero if the
cumulative variable, EFLUX, is not changing. For the 10 MJ and 2D 1/4 symmetry mesh, we used
¼ the quoted energy, or 2.5E6 J (quarter domain, quarter the energy). As noted by the figure,
EFLUX started at zero (and due to curve orientation has a negative value), and resulted in a
deposition of 2.5E6 J, as desired. This energy was distributed during a nanosecond, so P=E/Δt =
2.5E6/1E-9 = 2.5E15 W, which is what the PFLUX figure shows. Note that the figure shows that

![](images/tmpvlzzzdgp.pdf-68-2.png)

![](images/tmpvlzzzdgp.pdf-68-3.png)

![](images/tmpvlzzzdgp.pdf-68-4.png)

![](images/tmpvlzzzdgp.pdf-68-5.png)

the total energy insertion occurred during 1E-9 s, as expected. After that time, EFLUX stayed
constant (i.e. there was no further addition of energy), and PFLUX therefore remained zero. This
verified that the right amount of energy was input to the system during the right time period.

**Figure 4.11: EFLUX and PFLUX as functions of time during first 15 ns of the transient.**

**4.1.2.4** **Conclusion**

The relevant models for calculation of ionized gases were discussed. The literature was
consulted to determine which key parameters could determine the transient’s signature. It was noted
that opacity, electron thermal conduction, and degree of ionization are important, as well as several
other physics. Then, ALEGRA was benchmarked against a UCSD laser experiment that ionized
argon gas. The ALEGRA output for zbar, peak temperatures, and spark spatial domain agreed quite
well with data.
Next, a simulation of a hypothetical Z-IFE chamber with argon gas at 53,300 Pa was
conducted using ALEGRA. The calculation showed that for the first few centimeters of the 1 m
chamber, the argon gas reached a peaked at 1.25E6 K, with an averaged ionization of 15.6. As the
gas heated up, the absorption and Rosseland opacities increased exponentially to 1.39E5 and 8.5E4
m [2] /kg, respectively. The sharp temperature increase effectively meant that the photons were not able
to traverse the optically thick plasma medium. Heat was conducted away through electron thermal
conduction at a large rate; the electron thermal conductivity reached a maximum of 6.04E4 W/m-K.
Nevertheless, as the transient evolved, the plasma spread outwardly and began to cool down.

![](images/tmpvlzzzdgp.pdf-69-0.png)

As a result of the heat conduction, a diffusion (Marshak) wave initially traveled at close
to 100,000 m/s and proceeded to slow down as the plasma expanded and cooled. By the time the
wave reached the inner steel wall, it was traveling at about 10,000 m/s, its temperature was about
2.5E4 K, and it had an average ionization of 1.9.  The cool steel wall (300 K) quickly cooled the
adjacent argon plasma. Nevertheless, the heat transfer caused the two innermost mesh elements of
the steel wall to reach peak temperature of nearly 1,900 K. Therefore, about 0.00006 m of the steel
wall melted, while the majority of the wall (0.03994 m) remained near room temperature.
Note that the excessive heat-up of the innermost part of the steel wall can be minimized
relatively easily by placing a liquid wall so that it convects away the heat from the steel wall, or
alternatively, the chamber diameter can be increased.

_4.1.3 Single and Two- Phase Shock Mitigation (liquid Curtains)_

The thick liquid blanket concept was developed to mitigate the x-rays and neutrons
from the fusion reaction. Gas and aerosol mitigation only stop the x-rays while allowing the
neutrons through to interact with the wall. Since thick liquid curtains have the potential to mitigate
both neutrons and x-rays, they have been researched extensively in past Z-IFE work [32, 48].
Two curtain designs have been proposed. The first being separated liquid curtains that
are strategically placed around the fusion source to prevent line-of-sight to the chamber wall and
mitigate the shock caused by the x-rays. This curtain orientation has shown to be effective in
mitigating the neutrons and x-rays very well. The only drawback is that when absorbing the x-rays
an ablation shock wave is generated on the inner surface of the liquid curtains. The ablation causes
the curtains to accelerate and impact the chamber wall creating a dynamic stress. Depending on the
chamber radius, curtain geometry, and target yield, substantial stresses are induced in the wall due to
the momentum of the liquid curtains. Figure 4.12 shows an example of a possible liquid curtain
design created by LLNL [50]. The University of California at Berkeley (UCB) conducted several
shock mitigation experiments involving thick liquid curtains arranged in two different geometries.

**Figure 4.12: Top view of a liquid curtain design for the Z-IFE Vessel.**

![](images/tmpvlzzzdgp.pdf-70-0.png)

An alternative to this design is using a two-phase liquid curtain. The void fraction of a
two-phase liquid is defined as the ratio between volume occupied by the a gas and the total volume
occupied by both the liquid and gas. This can range from aerosols with a void fraction of 99% to
bubbly flow with a void fraction as low as 1%. Georgia Institute of Technology (GT) and the
University of Wisconsin (UW) have conducted experiments studying two-phase flow curtains. The
UW experiments involved sending shock waves through oil and water with void fractions ranging
from 5% to 15%. GT looked at characterizing two-phase flow jets with various void fractions and
jet velocities.

_4.1.4 Experimental Investigation of Chamber Liquid Structure Response [51]_

The use of free jets to create a porous blanket allows for venting paths to be formed to
control the transient pressure following the fusion reaction. The transient pressure contributes, along
with x-rays ablations of target facing jets, to the impulse loading delivered to the liquid jets. The
resulting velocity imparted to the liquid must be maintained at reasonable values to prevent erosion
of solid structures resulting from impingement of high velocity sprays, jets and slugs. Porous liquid
structures delay shock propagation through the liquid blanket and thus can allow for the jets to clear
the chamber center before being fully accelerated outward.
Previous studies [51,53] have shown that the fluid mechanics of liquid-salt porous
blanket disruptions by a fusion explosion could be reproduced with little distortion in reduced scaled
facilities using room temperature water and high explosives, such as composition C4.
To study those phenomena in a Z-Pinch-chamber configuration, two annular porous
liquid blankets, with different venting path and void fractions, have been tested in a sealed vacuum
chamber at UCB’s Vacuum Hydraulics Experiment (VHEX) under various impulse loads. A high
frame rate camera and fast pressure sensors were used to record the liquid response to the impulse
loading and detailed pressure history inside the pocket.

**4.1.4.1** **Annular Nozzles Description**

In the VHEX facility, water is driven by both gravity and a vacuum induced pressure
difference. The jets are created with a modular nozzle assembly. The assembly has a 30.5 cm (12”)
inner diameter and is 43.2cm (17”) long. VHEX was fitted with an annular flow diffuser, to provide
a transition between the VHEX inlet pipe and the outlet annular flows that would surround an actual
recyclable transmission line in a Z-Pinch fusion power plant. The annular, modular bay used for
these experiments can house a variety of nozzles (Figure 4.13).

![](images/tmpvlzzzdgp.pdf-72-0.png)

**Figure 4.13: Nozzle assembly housing. Various nozzles can be inserted in the modular bay.**

**4.1.4.2** **Diffuser Geometry**

Expansion of the 10.2 cm (4 in) diameter inflow to the 30.5 cm (12 in) diameter
outflow is achieved by the employment of an axisymmetric annular diffuser (Figure 4.13). The
diffuser is comprised of two components, a conical expansion and a central cone with radial flow
directing vanes. The conical expansion is fabricated from foam and polished fiberglass, has a length
of 30.2 cm (12 in), and a total angle (2θ), wall to wall, of 44.3º. The central cone is 27.9 cm (11 in)
in length with a base diameter of 14.0 cm (5.5in) and is fitted with 8, 0.16 cm (0.0625 in) thick, 25.4
cm (10 in) long, aluminum flow directing vanes, which originate 2.5 cm from the apex of the central
cone [54]. The leading edge of each vane is filed to a round elliptical shape and the trailing edge
sharpened off. Mounting the vanes on a slotted base and fitting 45º slices of the central cone
between them ensure symmetry. The central cone with radial vanes is set upon a 14.0 cm (5.5 in)
diameter, 12.7cm (5 in) tall, cylindrical base and fit into the conical expansion yielding an annular
diffuser with an area ratio of 7.7.

**4.1.4.3** **Nozzle Geometries**

Two nozzles are tested in the nozzle assembly. They are referred as phase 1 and 2 in the
subsequent sections (Figure 4.14).
The phase 1 nozzle reuses a system previously developed at UCB [55]. In this
configuration, the fluid is allowed to flow freely for 3.8 cm after exiting the diffuser. It then passes
through a fine copper wire cloth, 15 mesh per centimeter, which is directly followed by a 10.16
centimeters (4 in) long aluminum honeycomb with hexagonal cell of size 0.318cm (1/8”). Finally,
342 cylindrical free jets are formed by passing through a 0.95 cm thick aluminum plate. The jets are
arranged in 3 sets of 3 concentric rings, each consisting of 38 bores, with jets diameter increasing

radially in each set as 0.8 cm, 1.0 cm, and 1.2 cm. The total exit area of the annular curtain is 0.049
m [2] . The void fraction, based on the exit jets diameters, is 49%. A picture of the complete phase 1
nozzle is depicted on Figure 4.15.a).

**Figure 4.14: Nozzle geometries. Phase 1 nozzle is made of 38 sections similar to the section**
**depicted here; and phase 2 is made of 24 sections. The void fraction is 49% for phase 1 and**
**74% for phase 2.**

The phase 2 nozzle was developed and constructed for this study. In this configuration,
the fluid is allowed to flow freely for 3.8 cm after exiting the diffuser. The liquid then passes through
a series of three 2.2 cm thick aluminum conditioning plates and then through 5 cm long nozzle
contraction plate. Each conditioning plate contains 5 concentric rings, each consisting of 24 bores,
with the jet diameter increasing radially as 12.7 mm (.5 in), 15.2 mm (.6 in), and 17.8 mm (.7 in).
The nozzle plate has the same geometric layout with each bore contracting inward by 0.3 cm over a
distance of 3.8 cm.
The liquid conditioning sequence consists of passing the liquid through a fine stainless
steel mesh, 30 mesh per inch .0065in diameter wire, and into the first plate which houses 1/16”
hexagonal aluminum honeycomb, then through a larger stainless steel mesh, 18 mesh per inch
0.009in diameter wire, and into the second plate which contains only the bores. The liquid is then
passed through a fine mesh again and allowed to homogenize as it passes through the third plate and
into the nozzle plate. The liquid exits the nozzle plate and enters the VHEX chamber with reduced
lateral turbulence. The void fraction is 74% and the exit area is 0.027m [2] . Figure 4.15 b) depicts a
picture of this nozzle, and Figure 4.16 shows the nozzle in operation inside the VHEX chamber.

![](images/tmpvlzzzdgp.pdf-73-0.png)

![](images/tmpvlzzzdgp.pdf-74-0.png)

**Figure 4.15: Pictures of the full nozzle assemblies, with a yard stick for reference. a)**
**is phase 1, and b) is phase 2.**

**4.1.4.4** **Experiment Description**

In VHEX, high-explosives (composition C4) are used to simulate the scaled impulse
load delivered by the fusion reaction. The C4 was detonated using exploding bridge wires (EBW)
because they require a brief electrical pulse of several thousand volts and hundreds of amps to be
triggered which makes them safe to work with. The quantity of high-explosives used is varied to
simulate various impulse loads. An optimum impulse of 100 Pa-s is desired. The explosives are
positioned at the center of the annular liquid blanket and about 12.5 cm below a mounting block that
houses two pressure transducers used to record the pressure history. The mounting block is fixed
under the nozzles endplate and inside the inner cavity of the jets curtain. The mounting block can be
seen through the liquid curtain in Figure 4.16. Pressure measurements and videos are acquired
simultaneously.

![](images/tmpvlzzzdgp.pdf-75-0.png)

![](images/tmpvlzzzdgp.pdf-75-1.png)

**Figure 4.16: Phase 2 nozzle in operation inside the VHEX chamber. Horizontal rod entering**
**from left supports the explosive charge located on a stalk centered in the array 10 cm above**
**the rod.**

**4.1.4.5** **Phase 1 Results**

In phase 1, 4 sets of data were taken with respectively 0, 2.5, 5 and 23 g of high
explosives. Pressure history (Figure 4.17) and high speed video (Figure 4.18) were recorded for all
cases but the last where only video is available, because it was feared that the detonation might
damage the pressure transducers.

Pressure History Measurements

It should be noted that at the time of completion of the report, no post processing had
been performed on the pressure data yet. Hence the system vibrations have not been filtered out of
the pressure data. That can result in an underestimation of the impulse, by integration of the
pressure history, in the order of 50% for certain cases.
Further, due to the cylindrical geometry of the jets curtain, the shock waves are more
effectively contained radially than longitudinally. The radial characteristic length is on the order of
the curtain inner diameter or 16.75 cm, while the longitudinal characteristic length is about 1m. The

impulse imparted to the jets directly facing the charge is thus likely to be more important than
measured. That can be confirmed from the videos by estimating the momentum of the moving jets
after the explosion.
The measured raw impulses (Figure 4.17) range from 22Pa.s for a single detonator to
100Pa.s for 5g of HE; however, the actual impulses should be greater based on the above arguments.
On all experiments, but with the EBW alone, the charge was held from below. This is probably the
source of the dual peak observed on the pressure history of the EBW alone (Figure 4.17 a)). For that
experiment, the bulky and heavy wire feedthrough of the housing was directly between the
explosives and the pressure transducer. The feedthrough, which survived that particular explosion,
probably created a stagnation point on the front of the shock wave. The peaks observed are then
reflections of the shock wave arriving at the sensor location slightly out of phase.
Further when 5g of HE was employed, vibrations strongly affected the pressure
measurements (Figure 4.17 c)). Those vibrations could be due to shrapnel hitting the pressure sensor
mount. As a consequence, the impulse load is significantly misestimated.
It is very interesting to compare these impulse values, where the explosion is contained,
with previous measurements in an open geometry [55]. For the latter, between 20 and 30g of HE
(depending on the packing density) was required to reach an impulse of 100Pa.s, compared with a
mere 5g in this study.

Visualization Results

For small impulses, the porous blanket effectively delays the liquid outwards
acceleration (Figure 4.17.a) and b)) as anticipated by the snow plow model [56]. However, for
larger impulses (Figure 4.17 a) and b)), the liquid is accelerated outwardly very quickly. For the
case where 23g was used, it took less than 30ms for the viewing window of VHEX (a good 1.5m
away from the edge of the jets) to be drenched!

![](images/tmpvlzzzdgp.pdf-77-0.png)

![](images/tmpvlzzzdgp.pdf-77-1.png)

![](images/tmpvlzzzdgp.pdf-77-2.png)

**measurements have not been corrected for vibrations which are, in certain cases, quite**
**significant. a) corresponds to detonator alone, b) to an EBW with 2.5g of HE and c) to 5g of**
## **HE.**

![](images/tmpvlzzzdgp.pdf-78-0.png)

**Figure 4.18: Sequences of pictures from Phase 1 jets with an increasing mass of explosives.**
**a) is a single detonator, b) a detonator with 2.5g of HE, c) an EBW with 5g of HE and d) an**
**EBW with 23 g of HE. At the exception of d), the sequences are started with the apparition of**
**gas venting through the jets and ended when the chamber has been cleared. The time**
**intervals are also identical (except for d)).**

For all impulses it took nearly 144ms to clear the center of the chamber from any
residual drops and sprays and have a new liquid curtain.

**4.1.4.6** **Phase 2 Results**

In phase 2, 3 sets of data were taken with respectively 0, 2.70 and 5.25 g of high
explosives. Pressure history (Figure 4.19) and high speed video (Figure 4.20) were recorded for all
cases.

**Figure 4.19: Pressure measurements for Phase 2 nozzle for various HE masses. Pressure**
**measurement with a single EBW and no HE is not displayed because strong vibrations in the**
**pressure sensor mount rendered data unusable.**

The impulses measured with the phase 2 nozzle are smaller than in phase 1 (Figure
4.19). This demonstrates the importance of venting to reduce the impulse load delivered to the jets.
It should be noted that the measurement of impulse in phase 1 for 5 g of HE (Figure 4.17 c)) are
contaminated with strong vibrations, which explains why the measured impulses are similar in phase
1 and 2.

![](images/tmpvlzzzdgp.pdf-79-0.png)

When a single EBW was used, strong vibrations were recorded by the pressure
transducers. Consequently no accurate pressure history could be measured. The vibrations were
probably due to shrapnel from the detonator that hit the pressure sensors mount.
In Phase 2, the camera is used at 1000 fps with a resolution of 512×768 pixels. A fast
(f 1.8) 20 mm lens is used, which allows the exposure time to be reduced to 50 µs. The jet quality of
the phase 2 nozzle is significantly better than in phase 1, as no drops are observed breaking off the
jets.
High speed video images confirm the presence of significant venting in phase 2
experiments. For example, on the first picture of Figure 4.20 b), hot gases are present outside the
jets curtain while the shadow of undisturbed jets can be discerned. The jets start moving a few
milliseconds after the venting.

![](images/tmpvlzzzdgp.pdf-81-0.png)

**Figure 4.20: Sequence of pictures from Phase 2 with increasing amount of HE. The first**
**frames correspond to the first picture where venting is observed, about 1 ms following the**
**detonation. Time intervals are identical and times noted in bold italic are similar to those of**
**Figure 4.18** .

**4.1.4.7** **Conclusions**

Two nozzles, phase 1 and phase 2, were used to study the response of porous blanket
for thick liquid protection of Z-Pinch chambers. The simultaneous use of high speed camera and
pressure transducers allowed the jets response to various impulse loads to be studied. In particular
the importance of venting with the phase 2 nozzle to reduce the pressure build-up in the jets curtain
inner cavity is illustrated. Further, for small enough impulses, the snow plow effect effectively
delays the emergence of shocked liquid outside of the layer. These initial experiments provide the
necessary background to develop a more effective single-phase thick liquid curtain design for Z-IFE
conditions.
In the future, it could be possible to block out a small section of jets and in place insert
a plate with pressure transducers mounted on it to record the impulse directly felt by the jets facing
the high explosives charge.

_4.1.5 Void Fraction Distribution in a Two-Phase (Gas-Liquid) Jet [57]_

The hydrodynamics of falling two-phase (gas-liquid) jets were investigated.
Experiments were performed using air and water. The jets were produced by injecting well mixed
air-water mixtures through a 10 cm x 1 cm rectangular nozzle. The jet thickness and thicknessaverage void fractions were measured at nine different locations at three distances from the nozzle
exit, and at three lateral locations for each specific distance from the nozzle for a total of 20 flow
conditions. High speed photography and a needle tester were used for the measurements of the jet
width and thickness respectively, and gamma-ray densitometry was applied for the void fraction
measurement. Based on the experimental results, the two-phase jet stability was studied, and the
void fractions were empirically correlated. Three different correlations were developed in order to
provide flexibility with respect to their application. The correlations are of the generic form:

![](images/page_082_eq_0.png)

ε _g_ = _Co_ Re _la_ _FribWelc_ _D_ ∗

_g_ = _Co_ Re _la_ _FribWelc_ _D_ ∗ _d_

_go_

where ε _g_ is the local void fraction, ε _go_ is the homogeneous void fraction at the nozzle exit; _Rel_,

_Wel_ and _Frl_ are appropriately defined Reynolds, Weber and Froude numbers, and _D_ - is a ratio of
lengths.

**4.1.5.1** **Experimental Results and Discussion**

**Table 4.3: Experiments Conducted**

Table 4.3 is a summary of the experimental runs. Note that in each experiment the jet
void fraction and thickness were measured at nine points, namely three z values (5.4 cm, 13.7 cm
and 21.9 cm) from the nozzle exit, and for each z, three x locations (0 cm, -1.43 cm and 1.43 cm)
from the jet centerline shown in Figure 4.21.

**Figure 4.21: Coordinate system at nozzle exit**

![](images/tmpvlzzzdgp.pdf-83-0.png)

![](images/tmpvlzzzdgp.pdf-83-1.png)

![](images/page_083_table_0.png)

| Experiment | Water Flow (Q_l) in L/min and (gpm) and Inlet Liquid Velocity (U_l) in m/s | Gas Flow (Q_g) in L/min | Q_g / Q_l (%) |
|---|---|---|---|
| 1 | 60; (15.9); 1 | 0 | 0 |
| 2 | 120; (31.7); 2 | 0 | 0 |
| 3 | 180; (47.6); 3 | 0 | 0 |
| 4 | 240; (63.5); 4 | 0 | 0 |
| 5 | 288; (76); 4.79 | 0 | 0 |
| 6 | 120; (31.7); 2 | 1.5 | 1.25 |
| 7 | 180; (47.6); 3 | 4.5 | 2.5 |
| 8 | 240; (63.5); 4 | 6 | 2.5 |
| 9 | 288; (76); 4.79 | 7.2 | 2.5 |
| 10 | 180; (47.6); 3 | 9 | 5 |
| 11 | 240; (63.5); 4 | 12 | 5 |
| 12 | 288; (76); 4.79 | 14.4 | 5 |
| 13 | 180; (47.6); 3 | 18 | 10 |
| 14 | 240; (63.5); 4 | 24 | 10 |
| 15 | 288; (76); 4.79 | 28.8 | 10 |
| 16 | 180; (47.6); 3 | 27 | 15 |
| 17 | 240; (63.5); 4 | 36 | 15 |
| 18 | 288; (76); 4.79 | 43.2 | 15 |
| 19 | 240; (63.5); 4 | 48 | 20 |
| 20 | 288; (76); 4.79 | 57.5 | 20 |

The gamma-ray densitometer and radiation detection station were used in order to
measure the number of radiation counts for a total of 20 experiments. Five of the experiments were
single phase water with initial velocities ranging from 1 m/s to the maximum value of the system of
4.79 m/s. The 15 two-phase experiments were done with initial gas fractions ranging from 1.25% to
20%. Thus, a total of 180 data points were recorded. Figure 4.22 shows the experimental setup.

**Figure 4.22: Experimental setup highlighting the flow conditioner and nozzle.**

**4.1.5.2** **Void Fraction**

Using the calibration values of _[I]_ _l_ [ and ] _[I]_ _g_ [the average void fraction across the container ]

was calculated as

![](images/tmpvlzzzdgp.pdf-84-0.png)

![](images/tmpvlzzzdgp.pdf-84-1.png)
##### ( I 2φ / Il ) ( I g / Il )

##### ln ( I 2φ /

_I_ 2φ / _Il_

_I_ / _I_

2φ _l_

_g_ =

2φ _l_

~~ε~~ = . 4.2

_c_ ln _I_ /

_g_ _l_

![](images/page_084_eq_0.png)

If the void fraction of the jet is assumed to be zero (in the case of single phase flow), the thickness of the jet can be determined from this technique. Moreover, regardless of the initial gas flow, the collapsed liquid thickness (denoted with subscript CLT) of the jet is determined using the following equation

$$\delta_{CLT} = L\left(1 - \bar{\varepsilon}_g\right) \tag{4.3}$$

where $L$ is the inner distance of the container (the span across which the void fraction was determined [6.35 cm]). The $\delta_{CLT}$ is plotted as a function of x position for a fixed z position for given water and air flow rates. When $\delta_{CLT}$ is plotted against x position, the plot is asymmetric about the centerline. It is proposed that the asymmetry of the $\delta_{CLT}$ is due to asymmetry within the nozzle and flow straightener as opposed to the jet hydrodynamic phenomena.

![](images/page_085_eq_0.png)
[Figure 4.23: Collapsed liquid thickness versus x-position.]

**Ql = 47.6 gpm; Ul = 3 m/s (inlet); Qg/Ql = 0%**

| Legend | Distance from Nozzle |
|--------|----------------------|
| ◆ | 5.4 cm from Nozzle |
| ■ | 13.7 cm from Nozzle |
| ▲ | 21.9 cm from Nozzle |

**Figure 4.23: Collapsed liquid thickness versus x-position.**

Figure 4.23 shows a typical asymmetric profile. Asymmetry was observed independent of gas and liquid initial flow rates. The analysis of the void fraction and other such related parameters will be one-dimensional (z-direction [distance from nozzle]) and x-averaged values will be used at each fixed z distance. Nevertheless, the occurrence of this asymmetry should be noted.

The experiments noted in Table 4.3 were repeated and the jet thickness was measured; and again the experiments were repeated and the photos needed for the jet width measurements were taken. The void fraction of the jet is then simply

###### ε g j = 1− (δ CLT /δ MT ) 4.4

where δ _MT_ is the measured thickness of the jet.

![](images/page_086_eq_0.png)
**Ql = 76 gpm; Ul = 4.79 m/s (inlet); Centered in X-POS**

**Void Fraction**

-0.2 0 0.2 0.4 0.6 0.8

![](images/tmpvlzzzdgp.pdf-86-0.png)

**Figure 4.24: Void Fraction versus distance from nozzle.**

In Figure 4.24, the void fraction of the jet is plotted against the distance from the nozzle
for a fixed water flow rate. Each line corresponds to a specific gas flow rate. An atypical result of
the void fraction calculations was that the void fraction was negative for low gas flow rates. The
negative void fraction physically means that the collapsed liquid thickness is greater than the
measured jet thickness; therefore the collapsed liquid thickness has been over predicted and or the
measured thickness has been under predicted. This suggests that the error associated with one or
more facets of the measurements needed in the computation of the void is on the order of the void
fraction or greater. The error associated with the measurement of the thickness of the jet, while
small, is likely on the order of the void fraction measurements for the range of _Qg_ / _Ql_ = 0-5%. The

other potential source of error is from liquid droplet deposition onto the walls on the container while
the densitometer is in use. It is difficult to predict the amount of the droplet deposition, but it would
lead to a slight over prediction of the collapsed liquid thickness.
Only the high gas flow rate experiments (resulting in void fractions of 10% and greater) are shown
below.

![](images/tmpvlzzzdgp.pdf-87-0.png)

**Figure 4.25: Void fraction versus distance from nozzle.**

![](images/tmpvlzzzdgp.pdf-87-1.png)

**Figure 4.26: Void fraction versus distance from nozzle.**

Figure 4.25 and Figure 4.26 display the six high gas flow rate experiments studied. The
void fractions ranged from below 10% to almost 60%. The void fraction increases with increasing
the initial gas flow rate – an expected trend. An additional trend is that the void fraction increases

with increasing distance from the nozzle. Therefore the slip ratio is decreasing since the liquid is
accelerating downward, while the gas resists downward flow due to the buoyancy effect – this trend
was also expected.

**4.1.5.3** **Velocity Slip**

Once the collapsed liquid thickness, jet thickness and jet width are known, many
hydrodynamic properties can be studied. The gas and liquid velocities are of interest for the slip
ratio calculations, where

_S_ = _U_ _g_, 4.5
_U_

_l_

_U_ _g_ ( _z_ ) = δδ _inwwin_ _j_

_j_

![](images/page_088_eq_0.png)

( _z_ ) = _in_ _in_ _g_,

_g_ ( _z_ ) = _in_ _in_ _g_, _in_

![](images/page_088_eq_1.png)

=, 4.6
δ _w_ ε

_MT_ _MT_ _g_

![](images/page_088_eq_2.png)

_U_ _l_ ( _z_ ) = δ _inwin_ _j_

δ _w_ 1
#### (

_l_ ( _z_ ) = _in_ _in_ _l_, _in_

![](images/page_088_eq_3.png)

( _z_ ) = _in_ _in_ _l_, _in_
#### δ MT wMT (1−ε g j

= 4.7
δ _w_ 1−ε
#### ( )

![](images/page_088_eq_4.png)

#### (1−ε g j )

_MT_ _MT_ _g_

![](images/page_088_eq_5.png)

where the “MT” subscript denotes measured values and the “in” subscript denotes nozzle
dimensions. As previously discussed,

_jg_, _in_ = _QAg_, 4.8

_g_, _in_ = _Aing_

,

_jl_, _in_ = _QAinl_ 4.9

where the area is simply

_Ain_ = δ _inwin_ 4.10

![](images/tmpvlzzzdgp.pdf-89-0.png)

**Figure 4.27: Slip ratio versus distance from nozzle.**

![](images/tmpvlzzzdgp.pdf-89-1.png)

**Figure 4.28: Slip ratio versus distance from nozzle**

Figure 4.27 and Figure 4.28 show the relationship between the slip ratio and the
distance from the nozzle. The slip ratio values ranged from less than 0.2 to greater than 0.8. Thus,
at no positions studied was the gas velocity greater than the liquid velocity. Generally as the
distance from the nozzle increased, the slip ratio decreased, indicting the liquid is accelerating and or
the gas is decelerating.

**4.1.5.4** **Empirical Correlations in Plunging Jets or Nozzles**

The void fraction in plunging jets or nozzles is dependent on several dimensionless
parameters. These parameters are the liquid Reynolds number, the Weber number, and the Froude
number, and they are defined here as:

_Rel_ ( _z_ ) = _U_ ν _l_ δ _lMT_, 4.11

_Wel_ ( _z_ ) = _Ul_ 2 _g_ δ _c_ σ _MT_ ρ _l_ 4.12

_l_ ( _z_ ) = _Ul_ 2

_Frl_ ( _z_ ) = _gU_ δ _l_ 2 . 4.13

_MT_

![](images/page_090_eq_0.png)

The simplest form of an empirical correlation is

εε _gog_ = _CoReaFr_ _bWecD_               - _d_ 4.14

![](images/page_090_eq_1.png)

where _Co_, _a_, _b_, _c_, and _d_ are constants. _D_ - is a dimensionless distance defined as

⎛ _z_ ⎞
_D_ - = ⎜ ⎟ 4.15
⎝ δ _in_ ⎠

![](images/page_090_eq_2.png)

where _z_ is the distance from the nozzle and δ _in_ is the nozzle thickness (1 cm). ε _go_ is the

![](images/page_090_eq_3.png)
homogeneous-flow void fraction at the nozzle exit defined as:

_Q_

![](images/page_090_eq_4.png)

_in_ . 4.16

_Q_ + _Q_

_l_ _g_

![](images/page_090_eq_5.png)

_in_ _in_

Using the numerical software, DataFit, the constants in the above correlation were optimized,
leading to the following correlation:

0.101
2 ⎛ _z_ ⎞

= 2.07 ×10−1 ⎡ _Rel_ −9.91×10−2 _Frl_ −0.591 _Wel_ 0.772 ⎤ ⎛⎜ _z_ ⎞⎟ . 4.17
⎣ ⎦⎝ δ _in_ ⎠

ε _g_ = 2.07 ×10−1 ⎡ _Rel_ −9.91×10−2 _Frl_ −0.591 _Wel_ 0.772 ⎤ ⎛⎜ _z_

ε ⎣ δ

_g_ = 2.07 ×10−1 ⎡ _Rel_ −9.91×10−2 _Frl_ −0.591 _Wel_ 0.772 ⎤ ⎜
_go_ ⎣ ⎦⎝ δ _in_

![](images/page_091_eq_0.png)

The strong dependence on the Weber number is largely attributed to the two free
surfaces of the jet. The above correlation is in fact a relation amongε _g_, _Ql_, _Qg_, δ _MT_ and _wMT_,

when the nozzle geometry and fluid properties are fixed. In terms of these parameters the correlation
can be recant as:

−9.91×10−2 2 −0.591

−9.91×10−2 2 

⎜⎜⎝⎛ _QlinQ_ ε+ _gginQgin_ ⎟⎟⎠⎞ = 2.07 ×10−1 ⎢⎢⎢⎢⎢⎢⎢⎢⎢⎜⎜⎜⎜⎜⎜⎜⎛⎜⎜ ⎝⎜⎜⎜⎛⎜⎜ δδ _MTinwwinMT_ ⎝⎛⎜ δ(ν1 _inQl_ - _wl_ ε _in_ _g_ ⎠⎞⎟ ) ⎠⎟⎟⎟⎞⎟⎟ δ _MT_ ⎟⎟⎟⎟⎟⎟⎟⎟⎞⎟ −9.91×10− ⎜⎜⎜⎜⎜⎜⎜⎛⎜⎜ ⎝⎜⎜⎜⎛⎜⎜ δδ _MTinwwinMTg_ ⎝⎛⎜ δδ( _MT_ 1 _inQ_ - _wl_ ε _in_ _g_ ⎠⎞⎟ ) ⎠⎟⎟⎟⎞⎟⎟ 2 ⎟⎟⎟⎟⎟⎟⎟⎞⎟⎟

⎢⎜ ⎟ ⎜ ⎟
⎢⎜ ⎟ ⎜ ⎟
⎢⎝ ⎠ ⎝ ⎠

_win_ ⎛⎜ _Ql_ ⎞⎟ ⎟ ⎟ ⎜ ⎜ δ _inwin_ ⎛⎜ _Ql_

δ _w_ ⎜ δ _w_

2 0.772

_inwin_ ⎜ _l_ ⎟ ⎟ ⎟ ⎜ δ _inwin_ ⎜ _l_
_MT_ _wMT_ ⎝ δ(1 _in_ - _w_ ε _in_ _g_ ⎠ ) ⎟⎟ δ _MT_ ⎟⎟ ⎜⎜ ⎜⎜ δ _MT_ _wMT_ ⎝ δ(1 _in_ - _w_ ε _in_ _g_

![](images/page_091_eq_1.png)

ε ⎢⎢⎢⎢⎜⎜⎜⎜⎜ ⎜⎜⎜⎜⎜ δδ _MTinwwinMT_ ⎝⎜ δ(1 _in_ - _wl_ ε _in_ _g_ ⎠⎟ ) ⎟⎟⎟⎟⎟ δ _MT_ ⎟⎟⎟⎟⎟ ⎜⎜⎜⎜ ⎜⎜⎜⎜⎜ δδ _MTinwwinMT_ ⎝⎜ δ(1 _in_ - _wl_ ε _in_ _g_ ⎠⎟ ) ⎟⎟⎟⎟⎟ ⎟⎟⎟⎟ ⎜⎜⎜⎜ ⎜⎜⎜⎜⎜ δδ

_win_ ⎛⎜ _Ql_

δ _w_

_z_

(1 −ε _g_ ) ⎟ _MT_ ⎟ ⎜ δ _MT_ _wMT_ (1−ε _g_ )

δ _w_ ⎝ δ(1 _in_ - _w_ ε _in_ ⎠ ) ⎟⎟ δ _MT_ ρ _l_

_inwin_ ⎜ _l_ ⎟ ⎟
_MT_ _wMT_ ⎝ δ(1 _in_ - _w_ ε _in_ _g_ ⎠ ) ⎟⎟ δ _MT_ ρ _l_

1 −ε δ _w_ 1

_w_

_w_ 1 −ε δ _w_

(1 −ε _g_ )

(1 −ε _g_ ) ⎟ ⎟ ⎥ 0.101

2.07 ×10

⎡⎢⎢⎢⎢⎢⎢⎢⎜⎜⎜⎜⎜⎛⎜⎜ ⎝⎜⎜⎜⎛⎜⎜ δδ _MTinwwinMT_ ⎝⎛⎜ δ(ν1 _inQl_ - _wl_ ε _in_ _g_ ⎠⎞⎟ ) ⎠⎟⎟⎟⎞⎟⎟ δ _MT_ ⎟⎟⎟⎟⎟⎟⎞⎟ −9.91×10−2 ⎜⎜⎜⎜⎜⎛⎜⎜ ⎝⎜⎜⎜⎛⎜⎜ δδ _MTinwwinMTg_ ⎝⎛⎜ δδ( _MT_ 1 _inQ_ - _wl_ ε _in_ _g_ ⎠⎞⎟ ) ⎠⎟⎟⎟⎞⎟⎟ 2 ⎟⎟⎟⎟⎟⎞⎟⎟ −0.591 ⎛⎜⎜⎜⎜⎜⎜⎜ ⎛⎜⎜⎜⎜⎜⎝ δδ _MTinwwinMT_ ⎛⎜⎝ δ(1 _inQ_ σ− _wl_ ε _in_ _g_ ⎞⎟⎠ ) ⎞⎟⎟⎟⎟⎟⎠ 2 δ _MT_ ρ _l_ ⎞⎟⎟⎟⎟⎟⎟⎟ 0.772 ⎤⎥⎥⎥⎥⎥⎥⎥⎝⎛⎜ δ _zin_ ⎞⎟⎠
⎢⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎥
⎢⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎥
⎢⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎥
⎢⎜ ⎟ ⎜ ⎟ ⎜ ⎟ ⎥
⎢⎣⎝ ⎠ ⎝ ⎠ ⎝ ⎠ ⎥⎦

−1

ν _g_ δ

_Q_ ⎞ ⎢ ν _l_ _g_

_g_ _l_ _MT_

σ δ

_Q_ + _Q_

_lin_ _gin_

The correlation has an R [2 ] fit of 0.95, and the correlation values of the void fraction are
compared to the measured values of the void fraction.

![](images/tmpvlzzzdgp.pdf-91-0.png)

**Figure 4.29: Measured void fraction versus correlation void fraction**

The dashed line in Figure 4.29 represents an exact agreement between the correlation
and the measured values. It is of interest to identify which experiments were outliers.

![](images/tmpvlzzzdgp.pdf-92-0.png)

**Figure 4.30: Void fraction comparison.**

Figure 4.30 is shown to compare the correlation and individual measured values of the
void fraction. The x-axis is setup so that the experiments (unique initial water and air flow rates) are
listed in groups of three, which correspond to the three different distances from the nozzle measured
(increasing distances from the nozzle). Point 2 is an outlier since measured void fraction decreased
compared to point 1 as the distance from the nozzle increased.
One disadvantageous feature of the aforementioned correlation is the need for iteration
in order to solve for the void fraction. This is due to the dependence of the void fraction in the liquid
velocity term used in the Reynolds, Weber, and Froude numbers. Rather than using the local
velocity, the superficial velocity is modified such that

_jl_ = δδ _inwinwj_

_l_ = _in_ _in_ _l_, _in_

= . 4.19
δ _w_

![](images/page_092_eq_0.png)

_MT_ _MT_

This term is used in lieu of the _Ul_ term in the computation of the dimensionless numbers and the
correlation is still of the form

![](images/page_092_eq_1.png)
εε _gog_ = _CoRelo_ ′ _a_ _Frlo_ ′ _bWelo_ ′ _cD_               - _d_ . 4.20

where, now

_Relo_ ′ = _jl_ νδ _lMT_, 4.21

![](images/page_092_eq_2.png)

_Welo_ ′ = _jl_ 2δ _gMTc_ σρ _l_ 4.22

![](images/page_093_eq_0.png)
_lo_ ′ = _jl_ 2

_Frlo_ ′ = _g_ δ _jl_ 2 . 4.23

![](images/page_093_eq_1.png)

_MT_

Using numerical analysis for the optimization of the constants, the correlation becomes:

![](images/page_093_eq_2.png)

= 1.30×10−5 ⎣⎡ _Rel_ ′1.41 _Frl_ ′−0.420 _Wel_ ′−0.189 ⎤ ⎜⎛ _z_ ⎟⎞ 4.24
⎦⎝ δ _in_ ⎠

ε _g_ = 1.30×10−5 ⎣⎡ _Rel_ ′1.41 _Frl_ ′−0.420 _Wel_ ′−0.189 ⎤ ⎜⎛ _z_

ε δ

_g_ = 1.30×10−5 ⎣⎡ _Rel_ ′1.41 _Frl_ ′−0.420 _Wel_ ′−0.189 ⎤ ⎜
_go_ ⎦⎝ δ _in_

with an R [2 ] fit of 0.95.

![](images/tmpvlzzzdgp.pdf-93-0.png)

**Figure 4.31: Measured void fraction versus correlation void fraction.**

![](images/tmpvlzzzdgp.pdf-94-0.png)

where

**Figure 4.32: Void fraction comparison**

A yet third type of correlation can be developed, and based on the generic form

εε _gog_ = _CoReloa_ _FrlobWeloc_ _D_         - _d_ 4.25

_Relo_ = _j_ ν _lo_ δ _l_ _in_, 4.26

_lo_ = _jlo_ 2 _g_ δ _c_ σ _in_ ρ _l_

![](images/page_094_eq_0.png)

_Welo_ = _jlo_ 2 _g_ δσ _in_ ρ _l_

![](images/page_094_eq_1.png)

= _lo_ _in_ _l_ 4.27

![](images/page_094_eq_2.png)
_g_ σ

_Frlo_ = _g_ δ _jlo_ 2 _in_ . 4.28

![](images/page_094_eq_3.png)

The advantage of this correlation is that it provides

_g_ in terms of easily measurable

![](images/page_095_eq_0.png)

_go_

parameters (i.e., δ _MT_ and _wMT_ are not used). The optimization of the coefficients in this correlation
led to:

= 1.58×10−5 ⎡⎣ _Relo_ 0.874 _Frlo_ −0.252 _Welo_ 0.306 ⎤ ⎛⎜ _z_ ⎞⎟ 4.29
⎦⎝ δ _in_ ⎠

ε _g_ = 1.58×10−5 ⎡⎣ _Relo_ 0.874 _Frlo_ −0.252 _Welo_ 0.306 ⎤ ⎛⎜ _z_

ε δ

_g_ = 1.58×10−5 ⎡⎣ _Relo_ 0.874 _Frlo_ −0.252 _Welo_ 0.306 ⎤ ⎜
_go_ ⎦⎝ δ _in_

This correlation has an R [2 ] fit of 0.81, and the correlation values of the void fraction are compared to
the measured values of the void fraction.

![](images/tmpvlzzzdgp.pdf-95-0.png)

**Figure 4.33: Measured void fraction versus correlation void fraction.**

![](images/tmpvlzzzdgp.pdf-96-0.png)

**Figure 4.34: Void fraction comparison.**

**4.1.5.5** **Gas Flow Limits**

Bubbly flow is the desired flow regime for the test flow. For each flow rate of water
studied, the maximum gas flow for the bubbly flow regime was visually determined. For _Ql_ = 60
L/min (15.9 gpm), as gas is injected into the flow, the resulting flow regime is slug flow; therefore
the maximum gas flow rate ( _Qg_ / _Ql_ ) is equal to 0. For _Ql_ = 120 L/min (31.7 gpm), bubble flow

regime was observed for a maximum _Qg_ / _Ql_ of 1.25% ( _Qg_ = 1.5 L/min). If the gas flow rate is

increased, the resulting flow regime is slug flow. For _Ql_ = 180 L/min (47.6gpm), bubble flow
regime was observed for a maximum _Qg_ / _Ql_ of 15% ( _Qg_ = 27 L/min). At this value of _Qg_, spray

was observed from the jet. Additional gas resulted in slug formation within the nozzle. For _Ql_ = 240
L/min (63.5 gpm), bubble flow regime was observed for a maximum _Qg_ / _Ql_ of 21% ( _Qg_ = 50.5

L/min). Additional gas causes significant water spray since gas is escaping from the flow. And for

_Ql_ = 288 L/min (76 gpm), bubble flow regime was observed for a maximum _Qg_ / _Ql_ of 21% ( _Qg_ =

60.4 L/min). Additional gas causes significant water spray since gas is escaping from the flow.

**4.1.5.6** **Conclusions**

In this investigation, the hydrodynamics of falling two-phase jets were investigated.
The jets were produced using a vertically-oriented, 10 cm x 1 cm rectangular nozzle and using air
and water as the working fluids.
A total of 20 different flow rates were studied and local void fraction measurements
were performed at nine locations for each flow rate covering the z-dimension range from 5.4 cm to
21.9 cm at the nozzle exit. The collapsed liquid thickness was measured for all points using a
gamma-ray densitometer, and the jet thickness was measured using a thickness tester. The void
fraction was then calculated for all data points. However, due to the relatively large error associated
with the jet thickness measurements as well as the potential “jet spray”, the data representing low
liquid flow rates were excluded, and the void fraction was empirically correlated for only the six,
highest velocity tests. The local gas phase and liquid phase velocities as well as the slip ratios were
also studied for the six flow rates. The limits for jet stability were qualitatively assessed.
The trends in the void fraction of the aforementioned six flow rates were studied in
some detail. The void fractions ranged from below 10% to almost 60%. In all cases, however, the
void fraction was greater than the volumetric flow rate ratio. Generally as the distance from the
nozzle increased, the void fraction increased. Three different correlations were developed, all using
inlet flow conditions and jet exit thickness, as well as two using local thickness and width
measurements. The distinction between them is the definition of a velocity used in the calculation of
the dimensionless numbers used in the respective correlations; the first used a localized velocity with
dependence on the local void fraction and local thickness, the second used a superficial velocity and
local thickness, and the third used the superficial velocity and jet thickness at nozzle exit. All three
correlations fitted the data well.
The slip ratio of six different flow rates was extensively studied. The values of the slip
ratio ranged from less than 0.2 to greater than 0.8. Thus, at no positions studied was the gas velocity
greater than the liquid velocity. This suggests that the homogeneous equilibrium model is
inappropriate (since the assumption that the slip ratio is equal to 1 is clearly invalid). Generally as
the distance from the nozzle increased, the slip ratio decreased, indicting the liquid is accelerating
and or the gas is decelerating. The deceleration of the gas is of course expected, due to the buoyancy
effect.
The stability limits were studied for five different water flow rates. In the context of
the present experiments, jet stability is primarily determined by the two-phase flow regime upstream
the exit from the nozzle. The bubbly flow regime was required for the formation of a stable jet. It
was observed that, when the water flow rate was small (60 L/min [15.9 gpm], 120 L/min [31.7
gpm]), the flow became slug flow almost immediately with any gas injection. For higher water flow
rates (240 L/min [63.5 gpm], 288 L/min [76 gpm]), the flow became unstable only after a substantial
amount of gas was added ( _Qg_ / _Ql_ - 20%).

**4.1.5.7** **Recommendations**

Further study of plane two-phase falling jets with the current test facility is
recommended. There are several different facets that can be elaborated. First, the number of
experimental data points can be increased by studying higher water flow rates (greater than 288
L/min [76 gpm]), and by increasing the number of positions where measurements are performed for
each flow rate.

As previously discussed, at low gas flow rates, the thickness measurements are slightly
under-predicted and the collapsed liquid thickness values have been slightly over-predicted. It is not
completely clear why this anomaly occurs, and whether the anomaly is physical or it is caused by
experimental errors. If the latter possibility is to be believed, then the method used to measure the
thickness of the jet is not accurate enough for measuring small void fractions (less than 10%).
Further investigation of this anomaly is recommended. Another means of measurement for the jet
thickness (photography, etc.) is recommended. The spray from the jet that deposits onto the
container walls can possibly be estimated by normalizing the void fraction of single phase flow to
0% (if a negative value is observed due to the spray).
The measurements in this study were restricted to a minimum distance from the nozzle
exit of 5.4 cm and a maximum distance from the nozzle exit of 21.9 cm. It is recommended that the
facility be modified so that measurements at larger distances from the nozzle exit become feasible.
Finally, the stability of liquid jets when bubbles are generated inside the falling jet (due
to flashing caused by volumetric heating for example) should be investigated in the future.

_4.1.6 Shock Mitigation in Voided Liquids for Chamber Protection [58]_

Inertial fusion energy (IFE) power plant designs require a shock mitigation strategy to
protect the chamber from repeated thermonuclear blasts. One proposed idea for a high repetition
rate (6 Hz) moderate yield (350 MJ) conceptual power plant design is to use flowing liquid flibe
(F2LiBe4), either as sheets or jets in a staggered configuration, to protect the walls [59] and also to
serve the functions of heat transfer and nuclear fuel breeding. Currently, there is an ongoing
conceptual power plant design that instead utilizes high yield reactions (3 GJ) at a much lower rate
(0.1 Hz), and this provides a more challenging scenario where shock mitigation becomes more
important. This new design, utilizing Z-pinch technology [60], is investigating the use of foam(s) to
reap the benefits that a two-phase material can provide for shock mitigation [61]. The IFE target is
suspended from above in the center of the chamber filled with low pressure gas (10-20 torr), inside
of a hohlraum, by a conical recyclable transmission line (RTL). The interior of the RTL will be
filled with solid foam Flibe to protect the top of the chamber, while a bubbly pool protects the
bottom, and foamed liquid (two-phase) jets and sheets protect the side walls.
Previous shock tube investigations for chamber protection used solid aluminum foam
(as a model for flibe or PbLi foams) to study both thin foam layers, to model the vertical coolant
sheets, and a thick layer, to model the RTL. A series of low Mach number experiments (M=1.34)
studied the shock attenuation properties of a single 2.54 cm layer suspended in a shock tube and also
the effect of two layers separated by two different spacings [62]. The pressure behind the
transmitted shock was reduced by 30% (compared with the incident shock) while the wave speed
was reduced by 10% for the single layer configuration in Ar initially at atmospheric pressure. The
two layer configuration resulted in even greater pressure attenuation (50%) while the spacing
between the layers was found to have little effect. The solid foam, to model that incorporated into
the RTL, was modeled using two layers of 10.2 cm thick high-porosity aluminum foam of three
different cell sizes subjected to a very strong M=6 shock wave [63]. The presence of the thick
aluminum foam mitigated the shock wave; however, a very strong compression wave was
transmitted through the foam. Energy absorption was found to be a function of cell size while the
overall pressure load reduction was not, and larger pores were more effective at reducing the endwall impulse.

![](images/page_098_table_0.png)

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| impulse. |  |  |  |  |  |  |
|  |  | 99 |  |  |  |  |

The experiments reported here are for a new set of experiments, with varying shock
strengths, M=1.4, 2.0, and 3.1, where the objectives are: 1) to study the attenuation of the shock
wave as it passes through the bubble-filled, two-phase, pool, and 2) the impulse reduction observed
when voids are present in the liquid. This data can then be used for initial code calculation
verification and validation, before higher energy (e.g. high explosive) shock mitigation experiments
are performed.

**4.1.6.1** **Experiment**

The Wisconsin Shock Tube Laboratory [64] is utilized to conduct these shocked liquid
pool studies. The 9.2 m long vertical shock tube has a large internal square cross section (25.4 cm
sides), and is designed to withstand pressures of 20 MPa. Shock piezoelectric pressure transducers
are mounted along a vertical wall of the shock tube to measure the transient nature of the pressure
and the wave speeds. The driven section of the shock tube is filled with argon at atmospheric
pressure, and nitrogen or helium is used in the driver to obtain the desired shock strength.
Figure 4.35 shows the experimental setup in the bottom of the shock tube. Gas flows
through a fitting on the bottom of the shock tube into a cavity which remains slightly above
atmospheric pressure. The Ar flows through a Tyvek [TM] layer, whose presence is necessary to
prevent water from filling up the Ar cavity during experiment preparation, and then through a 2.54
cm thick aluminum foam [64, 65]. The aluminum foam is an open-celled structure, Fig. 2, with a
linear pore size of 0.64 mm and 40 pores per inch (ppi), and a porosity of φ= 0.89, where φ= 1− ρ _c_,

φ= 1− ρ _c_,
ρ _s_

ρ _s_ = 2,700 kg/m [3 ] (solid Al 6061 T6 density), and the cellular density is ρ _c_ = 0.11ρ _s_ . The compressive
yield strength for the 40 ppi foam with this porosity has a plateau of σ _yc_ = 3.0 MPa and is relatively

independent of the pore size [66]. The aluminum foam creates bubbles that are small, relative to the
cross section of the shock tube, and randomly distributed throughout the volume. An exhaust line is
located above the pool’s surface so that the pressure of the driven section of the shock tube remains
at 1 atm. A solenoid-actuated valve for this line is pneumatically closed just prior to shock passage.
Piezoelectric shock pressure transducers sampling at 1 MHz are located along the center of one side
of the shock tube with the faces flush mounted with the shock tube wall. There are four pressure
transducers located above the pool to accurately measure the speed/pressure of the initial shock wave
and the transducers are vertically spaced at intervals of 2.54 cm in the pool. The appendix contains
engineering drawings for the test section transducer plug, the test section, and the support structure
for the aluminum foam.

Ar

Liquid, Rising Bubbles

Porous Plate
Tyvek layer

Plate Support

Pressure
Transducers

Ar filled cavity

Ar

**Figure 4.35: Apparatus for simulating the shock mitigation response in the lower portion of**
**the chamber.**

3 cm

**Figure 4.36: Open cell-cell morphology of the 40ppi aluminum foam used to create the**
**bubble distribution.**

Figure 4.37 and Figure 4.38 show Ar bubbling up through water and oil in a mock-up
of the shock tube test section having polycarbonate walls. The bubble population in the water is
uniform across the width of the pool as well as the height. The turbulent nature of the bubble-bubble
interaction while rising results in non-spherical gas bubbles at any moment in time, but over time,
the bubbles in water may be considered spherical with an average diameter of _D_ =5.6 mm with a
standard deviation of 2.6 mm. Void fraction of gas was controlled by measuring the volumetric flow
rate, during characterization, levels up to 15% could be achieved. Numerous attempts to achieve
higher void fractions were unsuccessful, including: increased flow rate (limited by the head loss of
the aluminum foam); different pore size foam (no effect, most likely because porosity remained
constant); and a stainless steel porous plate instead of aluminum foam (resulted in very small
bubbles and very low void fraction due to high head loss). The same 15% void fraction observed in
the water was also seen in the mineral oil, however, the bubbly flow was much different than the
flow in water, as seen in Figure 4.37, and resulted in a bimodal bubble size distribution. The argon
bubbling-up through the oil created a near-foam (in appearance) two-phase fluid, with many tiny
bubbles of _D_ <2 mm. In addition, there were a number of large-scale bubbles 15< _D_ <30 mm that
originated at the locations of small cap screws that were used to secure the porous plate to the
support around the perimeter of the plate.

![](images/tmpvlzzzdgp.pdf-100-0.png)

![](images/tmpvlzzzdgp.pdf-100-9.png)

A final series of experiments were conducted at the high Mach number for shaving
cream foam occupying the bottom 1.3 m of the shock tube. These experiments provide the contrast
of a very low density, closed-cell foam, to the high-density water pool experiments.

**Figure 4.37: Water with 15% void fraction of Ar in a mock-up of the shock tube test section**
**with transparent walls- the width of the test section is 25.4 cm.**

**Figure 4.38: Mineral oil with 5% void fraction of Ar in a mock-up of the shock tube test**
**section with transparent walls- the width of the test section is 25.4 cm.**

![](images/tmpvlzzzdgp.pdf-101-0.png)

![](images/tmpvlzzzdgp.pdf-101-1.png)

**4.1.6.2** **Shock Strength Scaling**

Calculations of the shock strength following target ignition were carried out using
BUCKY [67] to determine the pressure loading on the pool in the bottom of the reactor. Pressure as
a function of chamber radius is shown in Figure 4.39 for a 3.05 GJ target yield in a chamber with an
initial argon gas pressure of 12 mtorr (1.6 Pa). The pressure traces for _t_ =115 and 900 ns show the
regions of the target (DT, Be, CH, Au), argon, and flibe (considered incompressible in the
calculation). There is a compression wave moving radially outwards through the argon (shown at
115 ns), and when it reaches the flibe, vaporization occurs (moving back into the argon, shown at
900 ns) which raises the local pressure above that of the argon. The steepening compression wave
that first reaches the flibe raises the pressure to 1 J/cm [3] ( _P_ contact=1 MPa) and then reaches a
maximum of 23 J/cm [3] ( _P_ max=23 MPa). For the shock tube experiments in atmospheric pressure
argon, the shock strength required for _P_ contact=1 MPa is _M_ =2.85, which would then result in an ideal
_P_ max=4.2 MPa for a reflected shock wave off of an incompressible boundary.  To reach the
maximum argon pressure calculated from BUCKY ( _P_ max=23 MPa) a shock strength of _M_ =5.8 which
is above the structural design limit of the shock tube. The pressure loading of the bubbly pool in the
shock tube for the considered Mach numbers is on the same order as would be expected in the Z
reactor, but not as high as the maximum pressure; however, the pressure ratios, and therefore Mach
numbers, would be quite different.

target

argon

**Radius [cm]**

target

argon

flibe

**Radius [cm]**

**Figure 4.39: Pressure as a function of radius for the line of sight from the target to coolant**
**pool at the bottom of the chamber calculated using BUCKY.**

**4.1.6.3** **Results**

Prior to conducting the two-phase fluid experiments, a series of calibration runs were
performed to quantify the shock wave and verify the operability of the pressure transducers. The
data collected from the experiments include pressure traces and material surface corrosion. This
campaign consisted of a total of 52 experiments covering three Mach numbers, and the response of
three different two-phase fluids of: water/argon, oil/argon, and shaving cream foam.

Pressure Trace and Impulse

Three shock strengths were chosen for these studies and the properties are listed in
Table 4.4. The initial shock wave speed, _W_ i, is for the listed Mach number in argon at standard
temperature and pressure; the reflected shock wave speed, _W_ r, is the calculated speed for the
reflection off an incompressible surface; the gas velocity behind the incident shock is _u_ 2; and the
pressure, P, with subscripts 1, 2, and 5 are the initial pressure, the pressure behind the incident shock
wave, and the pressure behind the reflected shock wave, respectively.

**Table 4.4: The experiment parameters, for argon, calculated from 1-D gas dynamics.**

Pressure traces from the same transducer for each of the void fraction pools are shown
in Figure 4.40 for some low Mach number water pool experiments. The pressure in the pool without
a void fraction resemble the _P_ 5 plateau that would be observed for a shock wave reflected off a rigid
surface, this is indicative of the relative incompressibility of the water compared with the argon. At
longer times, _t_ >1 ms, the pressure trace resembles the _P_ 5 plateau for each of the void fractions. The
early time behavior is quite variable for the different void fractions as seen in Fig. 6(b). When there
is no void fraction, a near-discontinuity pressure rise is observed as would be expected for a shock
wave (not traveling through the water but reflecting off the surface of the water back into the argon);
however, the presence of the argon bubbles in the pool has a strong effect on the pressure traces and
oscillations are observed in the traces before leveling out at later times. Each of the pressure traces
for void fractions of 5, 10, and 15% argon show an initial compression that is not discontinuous, and
is the response of the argon bubbles in the pool compressing. The time when the bubbles in the pool
have reached maximum compression corresponds to the time of peak pressure; this is then followed
by an expansion of the bubbles which reduces the pressure. Cyclic compression and expansion
continues during the early times and the measured oscillations reflect this cycling, and not
necessarily reverberating pressure waves in the bubbly pool. There are some higher frequency
oscillatory content in the 5 and 15% argon void fraction traces which is most likely due to a
proximity effect for a single bubble being closer to the transducer face (circular, 5 mm diameter) and
therefore responding slightly different than the overall, average, pool response.

![](images/page_103_table_0.png)

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| M | Wi (m/s) | Wr (m/s) | u2 (m/s) | P1 (MPa) | P2 (MPa) | P5 (MPa) |
| 1.4 | 456 | 343 | 170 | 0.101 | 0.227 | 0.453 |
| 2.0 | 646 | 405 | 363 | 0.101 | 0.482 | 1.52 |
| 3.1 | 1,001 | 554 | 672 | 0.101 | 1.19 | 5.26 |

![](images/tmpvlzzzdgp.pdf-104-0.png)

**Figure 4.40: Pressure traces for M=1.4 from a transducer located 3.5 cm below the surface**
**of the pool for 0, 5, 10, and 15 % argon void fraction.**

Results for the impulse calculations are given in Table 4.5. The impulse time ( _t_ I) is
chosen as the time it takes an unattenuated shock wave to travel through the distance of the pool
depth, _h_ =0.3048 m. The impulse interval begins when a pressure is first registered by the transducer.
The impulse time goes down with increasing shock strength but the impulse goes up due to the
stronger effect of the higher shock strength’s pressure rise. Although very different behavior is seen
in individual pressure traces, the presence of argon voids in the pool has little, if no, effect on the
calculated impulse at the low and medium Mach number experiments. At the low and medium
Mach number experiments, the shock wave speed is well below the sound speed in water (1,500 m/s
at STP) and the pool shows a primarily incompressible response to the shock loading- even though
the bubbles are compressing within the pool. A pool with a much higher void fraction (e.g. foam)
would be expected to show a different response, with the increased void fraction resulting in an
impulse reduction. A 12% reduction was observed in the high Mach number experiments, which
indicates that the compressible nature of the bubbly pool was playing a role. The wave speed of the
high Mach number experiments is approaching that of the acoustical speed in pure water, thus, the
response of the bubbly pool is that of a two-phase mixture and is no longer purely dominated by the
incompressible nature of the water as observed in the lower shock strength experiments. Also,
heating of the pool due to compression of the bubbles will lower the sound speed during the shock
wave interaction.

**Table 4.5: Impulse measurements for the pool with argon bubbles.**

![](images/tmpvlzzzdgp.pdf-104-1.png)

![](images/page_104_table_0.png)

| M | I₀ [Nt s] | I₅ [Nt s] | I₁₀ [Nt s] | I₁₅ [Nt s] | t₁ [ms] |
|---|---|---|---|---|---|
| 1.4 | 13.2 | 14.9 | 14.5 | 13.1 | 0.67 |
| 2.0 | 40.3 | 39.8 | 38.2 | 41.7 | 0.47 |
| 3.1 | 82.0 | - | - | 72.0 | 0.31 |

Experiments to study the response of a mineral oil pool with argon bubbles were only
conducted at the higher void fraction (15%) and the high Mach number. An even greater impulse
reduction was seen in this two-phase pool as the impulse dropped from 131 N-s to 86 N-s (34%).
The greater reduction in impulse may be partially attributed the lower bulk modulus of oil compared
to water (resulting in a lower sound speed, 1,300 m/s at STP); however, given the magnitude, it is
more likely due to the very different bubble distribution of the argon in the oil, particularly the
smaller bubbles that resulted in a more foamy liquid.
Using the bubbly-pool configuration, only a low gas fraction two-phase pool could be
achieved. Shaving cream foam was used to contrast the behavior of a high density pool to a very
low density foam which also has a closed-cell structure (density of 66 kg/m [3] and an estimated gas
void fraction of 94%). The bottom 0.3 m of the shock tube was filled with the foam (shown in
Figure 4.41(a) and (b) and it experienced no visible settling from the time of preparation to the time
of shock arrival (typically less than 30 minutes). A pressure trace result is shown in Figure 4.42 and,
for comparison, the reference is a shock wave in the gas (air). In the pure gas trace, the shock wave
initially steps up the pressure to 1.2 MPa ( _P_ 2) and then at 0.8 ms the pressure is stepped up to 5.3
MPa ( _P_ 5). After 1.5 ms it is clear that the rarefaction from the shock tube driver has expanded down
to the pressure transducer location which lowers the pressure in an exponentially decaying fashion.
When the shaving cream foam is present, the response is much different, with the initial pressure rise
showing fast compression, although not stepped as in the shock wave case, which is between the _P_ 2
and _P_ 5 pressures of the shock wave in the argon. At the later times, during the rarefaction phase, the
exponential decay of the pressure is the same in both cases. An arbitrary time of 2 ms was chosen
for comparing the impulse between the foam and no-foam cases and a reduction from 441 N-s to 344
N-s was observed, a 22% reduction. Figure 4.41(c) is a photograph, taken from higher up in the
shock tube, of the top surface of the foam after an experiment. The foam expanded from the initial
0.3 m depth to 1.3 m, and by the time the high pressure had been vented and a port was opened for
taking the photograph, the foam had settled to this 1.3 m depth (there are visible liquid traces on the
walls that indicate that the foam had splattered during the test.) One experiment was conducted on
this already expanded foam and the shock mitigation was still evident, but less effective, with an
impulse of 427 N-s. Thus, it appears that the responsible mode for impulse reduction is one where
the energy of the shock wave is transferred into expanding, and breaking-up, the foam. Once
expanded, the foam loses most of its impulse reducing function.

**Figure 4.41: Shaving cream foam photographs in shock tube, (a) side-view during fill, (b) top**
**view pre-test, and (c) top view post test**

![](images/tmpvlzzzdgp.pdf-105-0.png)

5

3

1

![](images/tmpvlzzzdgp.pdf-106-0.png)

0
-1 0 1 2 3 4 5 6

Time [ms]

**Figure 4.42: Pressure Traces from a transducer located 1 m below the surface of the**
**shaving cream foam.**

**4.1.6.4** **Surface Corrosion**

Polished stainless steel material samples were placed in the pool for the high Mach
number experiments with no void fraction and with 15% void fraction. The scanning electron
microscope (SEM) images are shown in Figure 4.43 and Figure 4.44. Each sample was only
exposed during one experiment. The most notable feature observed in both samples was the
presence of pits following the experiment. Surface oxidation particles were concentrated in the
pitted regions and were more prevalent in the experiment without argon voids. It was anticipated
that more pitting would occur in the experiment with 15% argon void fraction due to the
compression (and expansion, and possible jetting) of the gas bubbles near the surface of the sample;
however, the amount of pitting was similar in both of the samples.  The corrosion/erosion of a
wetted surface, enhanced by being repeatedly exposed to shock waves, will need to be a
consideration for first-wall material selection.

![](images/tmpvlzzzdgp.pdf-107-0.png)

**Figure 4.43: SEM images for a sample in the water pool with no void fraction shown at**
**increasing levels of magnification.**

**Figure 4.44: SEM images for a sample in the water pool with 15% argon void fraction shown**
**at increasing levels of magnification.**

![](images/tmpvlzzzdgp.pdf-107-1.png)

**4.1.6.5** **Conclusions**

A series of shock tube experiments were conducted to model the flibe pool response in
the Z-chamber. Only low gas void fraction (5-15%) could be achieved by bubbling argon through
an aluminum foam plate beneath a pool of liquid, either water or oil. Although the pressure traces in
the pools with gas bubbles exhibited much different behavior than the measured traces for pure gas
or pure liquid, the overall effect on impulse was not observed at the low and medium ( _M_ =1.4 and
2.0) experiments. The shock mitigation effect of the bubbly pool was observed in both the water and
oil pools in the higher shock strength experiments ( _M_ =3.1) with the bubble distribution playing a
role in the amount of observed mitigation to the impulse- smaller bubbles resulted in a foamy-like
liquid resulted in greater impulse reduction. A very high gas void fraction shaving cream foam
resulted in a 17% reduction in impulse for the high Mach number experiments which indicates that
more experiments need to be done in the intermediate void fraction regimes to reach any conclusion
about the optimum concentration of gas to liquid for shock mitigation. Polished stainless steel
witness samples placed in the pools exhibited a notable amount corrosion/erosion following just a
single experiment. This is a potential issue for a first wall exposed to a very high number of
repeated exposures- both for the integrity of the structure and the contamination of the coolant.

_4.1.7 Aerosol Shock Mitigation_

Aerosol protective schemes provide a unique means by which to shield the first wall
from the brunt of the x-ray energy released from the fusion burn while allowing neutrons to pass
relatively unmitigated. This feature is important for designs requiring tritium breeding and/or
transmutation in a blanket external to the chamber. Ultimately, the success or failure of any
mitigation technique is measured by the ability to shield the first wall while inducing an acceptable
stress in the containment vessel. Figure 4.45 shows a schematic of the model used in these
investigations.

**Figure 4.45: Schematic of CTH 1-D system model.**

![](images/tmpvlzzzdgp.pdf-108-0.png)

The aerosol system consisted of a water and argon matrix with a volume fraction of α =
0.3%. Water and argon were chosen because the code has well-defined equations of state for these
materials. Also, these materials are likely candidates for early experiments. The water droplets each
had a diameter of 30 μm and were assumed to be uniformly distributed throughout the chamber.
The argon was at a pressure of 0.06 bar, roughly twice the vapor pressure of water at 300 K. Finally,
the chamber was modeled as a sphere with radius R = 1 m and wall thickness of tw = 0.04 m. The
shock was generated by an x-ray source of 10 MJ depositing into the aerosol. To address the postburn physics of a chamber filled with an aerosol, the CTH shock code was employed to model the
time from immediately after detonation to the subsequent chamber dynamic response.
The CTH suite of codes was created at Sandia National Laboratories to model systems
with large deformations and/or strong shocks. The code utilizes an Eulerian architecture to solve the
mass, momentum, and energy equations. The x-ray energy deposition profiles were input as an
initial condition of 1-D spherical gas contained by a steel vessel (Figure 4.46) [1]. These CTH runs
assumed a constant x-ray source radius of 0.036 m for all cases. The code then output a time
dependent response of the gas as a shock wave formed and propagated to the steel containment wall.
This response does not include any high order plasma physics, _e.g._ re-radiation of the gas via
Bremsstrahlung. Ultimately, the shock wave impacts the steel vessel causing a sharp rise in stress
before the wave is reflected back towards the center of the chamber.

0 0.2 0.4 0.6 0.8 1 1.2

**Radius (m)**

**Figure 4.46: Initial energy deposition profile for the CTH simulations.**

![](images/tmpvlzzzdgp.pdf-109-0.png)

This initial modeling effort assumed all x-ray energy was deposited into the water.
This assumption was made due to the water constituting 98% of the mass of the system. Figure 4.47
shows the resultant initial temperature profile of the water in the system from the deposited x-ray
energy. The water near the center of the x-ray source reached temperatures exceeding 8 × 10 [5] K.
However, the water temperature drops quickly away from the center, falling below boiling at
approximately r = 0.4 m.
Figure 4.48 gives the temperature profile inside the chamber at times up to 1800 μs.
The model shows that the system peak temperature quickly drops, while the energy redistributes.
However, this diffusion of temperature should not be confused as heat transfer. For this version of
the model, the code does not treat any modes of heat transfer. Conduction was allowed in a later
version of the model but did not affect the results appreciably. Rather, the change in temperature is
simply due to the advection of water in the chamber.

**Figure 4.47: Initial temperature profile of the water in the CTH simulations.**

![](images/tmpvlzzzdgp.pdf-110-0.png)

![](images/tmpvlzzzdgp.pdf-110-1.png)

![](images/tmpvlzzzdgp.pdf-111-0.png)

![](images/tmpvlzzzdgp.pdf-111-1.png)

![](images/tmpvlzzzdgp.pdf-111-2.png)

**Figure 4.48: Temperature profiles in the chamber at different times for the CTH simulations.**

Figure 4.49 shows the pressure histories at different locations inside the chamber. The
shock wave and subsequent reflections are characterized by the sharp pressure peaks. The solid line
(Case 10.1) represents the aerosol system described earlier. The dashed line (Case 9.2) denotes a
system with matching dimensions but only argon gas as an x-ray mitigation shield. For protection in
this system, the gas pressure must be almost nine times greater or P = 0.533 bar. The response of
both systems is similar in character, but the shock wave is greater in magnitude in the aerosol
protected system. This increased shock wave is perhaps due to the addition of more mass into the
system, nearly 12 kg of water.

![](images/tmpvlzzzdgp.pdf-111-3.png)

![](images/tmpvlzzzdgp.pdf-111-4.png)

![](images/tmpvlzzzdgp.pdf-111-5.png)

![](images/tmpvlzzzdgp.pdf-112-0.png)

![](images/tmpvlzzzdgp.pdf-112-1.png)

![](images/tmpvlzzzdgp.pdf-112-2.png)

**Figure 4.49: Pressure histories at different locations in the chamber for the CTH simulations.**

Figure 4.50 gives the induced hoop stress in the chamber wall for the two
aforementioned cases. The aerosol protected system produced a stress of nearly one and a half times
that of the gas protected one. This stress is directly correlated to the strength of the shock waves
interacting with the chamber walls. Still, the stress in the vessel wall did not exceed the elastic limit
of common stainless steels (~ 2000 bar). Although the gas protected system does incur a lower
stress, the potential shielding capacity of aerosols far exceeds that offered by gas alone. A gas
system in moderately sized chambers is limited to x-ray energies of about 100 MJ and below based
on the temperature rise of the gas, whereas a similar geometry with an aerosol has a limit just
exceeding 1000 MJ [1].

![](images/tmpvlzzzdgp.pdf-112-3.png)

![](images/tmpvlzzzdgp.pdf-112-4.png)

![](images/tmpvlzzzdgp.pdf-113-0.png)

**Figure 4.50: Induced hoop stress in the chamber wall as a function of time for the CTH**
**simulations.**

Water mass as a function of position in the chamber at various times is plotted in Figure
4.51. Again, the water was assumed to be distributed uniformly in each differential node at the
beginning of the simulation. As time progresses, the water is preferentially pushed towards the
chamber wall. The agglomeration of water is possibly an artifact of the code, which is evident at
times late in the simulation. However, the first arrival of the main pressure wave that accelerates the
steel shell to its motion is concluded before all the water has accumulated. Therefore, the response
of the steel shell should be unaffected by this anomalous numerical result.
The response of a water-argon aerosol in a post-detonation chamber was modeled using
the CTH shock code. These simulations indicated that the stress induced from the ensuing shock
wave was acceptable for a chamber with the assumed geometry and construction. Further
refinements of the model were attempted, including a partitioned energy deposition into the water
and argon based on mass ratio (98% into the water, 2% into the argon) and a model including
conductive heat transfer. Both attempts did not produce significantly different results from those
already presented. The model appears to be capturing, at least to a first order approximation, the
physics within and the mechanical response of the chamber to relatively short times after detonation.
Future two dimensional modeling in ALEGRA, a shock physics code, will be necessary to capture
the plasma physics phenomenon not available in CTH for aerosol mitigation.

![](images/tmpvlzzzdgp.pdf-114-0.png)

![](images/tmpvlzzzdgp.pdf-114-1.png)

![](images/tmpvlzzzdgp.pdf-114-2.png)

**Figure 4.51: Water mass as a function of chamber position.**

###### **4.2 Chamber Design**

Lawrence Livermore National Laboratories continued to optimize the thick liquid
curtain chamber design this year by increasing the target yield and repetitive rate. A proposed
frozen or frangible flibe RTL was used in this design to alleviate separation and remanufacturing
issues immediately following the fusion event. The study focused mainly on the timing of placing
and removing the RTL in and from the chamber. It is described in detail in section 4.2.1.
Due to the possibility of using aerosols to mitigate the x-rays, a first wall chamber
design was proposed. This concept was first developed to be used for the transmutation plant where
target yield requirements were much less compared to what was required from the power plant [5].
However, results from the computer modeling described in section 4.1.7 indicate that aerosols may
be able to mitigate fusion yields upward to 3 GJ (~1000 MJ x-rays). A first wall chamber design for
the Z-IFE power plant is presented in section 4.2.2.

_4.2.1 Thick Liquid Curtain Chamber Design Concept and RTL Design [6]_

The main features of the proposed Z-IFE chamber are shown in Figure 4.52. The 3.5m-tall, 2.2-m-diameter (13.3 m [3] ) pocket protects the chamber walls by containing the x-rays and
target debris generated by the fusion shot so as to delay their effect on the wall. Note that all
structures are protected against neutrons, x rays, and target debris by 1 m of the molten salt flibe,
which also serves as the primary coolant and tritium breeder.

![](images/tmpvlzzzdgp.pdf-114-3.png)

![](images/tmpvlzzzdgp.pdf-114-4.png)

![](images/tmpvlzzzdgp.pdf-114-5.png)

The RTL is made of frozen flibe. It is shown in more detail in Figure 4.53. This RTL
material is frangible meaning it shatters following a shot and quickly becomes part of the coolant.
The cost advantages of the frangible flibe RTL compared to that of steel, of the rapid pulse rate of
1.9 s compared to 10 s resulting in only one chamber and power supply needed, and the liquid
protection of all structures making them lifetime components should greatly enhance economics.

![](images/tmpvlzzzdgp.pdf-115-0.png)

**Figure 4.52: The Z-IFE chamber and 3m RTL design are shown with full neutron and blast**
**protection of structures.**

![](images/tmpvlzzzdgp.pdf-116-0.png)

**4.2.1.1** **Inserter Design**

Figure 4.54 shows the 3-m RTL shortly before shot time with the MITL covered and
the inner and outer RTL cones still separated. About 0.5 m (0.05 s) before reaching the shot position
and shot time, the downward acceleration is increased from 1 g to 2 g's; which is just enough to
make the inner cone close the gap to 1.5 mm at the shot position and time as shown in the next
figure. The downward acceleration must be increased quickly enough so as to decisively overcome
the friction that can hold the two cones together but not so rapidly as to cause the RTL to
prematurely shatter. Too slow an application of force will result in jitter in the time and place of
closure of the gap. The gap will be measured in realtime (possibly by radar techniques) so as to time
the pulsed power system to fire when the gap is attained.

![](images/tmpvlzzzdgp.pdf-117-2.png)

![](images/tmpvlzzzdgp.pdf-117-1.png)

be needed. Thermal shock will be an important design consideration for future studies.

![](images/tmpvlzzzdgp.pdf-118-0.png)

**Figure 4.55: RTL at shot time with the MITL uncovered.**

Figure 4.52-Figure 4.55 show a 2-m-high pulsed column of flibe above the shot. Figure
4.56 shows the design with only 1-m-high column (3 m [3] ) of flibe. For overcoming upward impulse
due to the shot and for neutron protection, 1 m would be quite sufficient and ease injection and
filling of the inserter during insertion. The fill time will be about 1 s, which gives a required fill rate
of 3 m [3] /s. If the flow speed in the fill pipes is kept to a reasonably low 5 m/s then the area of the fill
pipes is 0.6 m [2] . There would be 76 pipes of 0.1 m diameter, which would represent only a small
percentage of the available area on the injection cylinder wall.

![](images/tmpvlzzzdgp.pdf-119-0.png)

**Figure 4.56: The vertical thickness of the pulsed jets above the shot point only needs to be**
**1m as shown here rather than the over 2m shown in prior figures.**

**4.2.1.2** **RTL Detail**

Details of the RTL are shown in Figure 4.57 and Figure 4.58. Notice the outer cone in
Figure 4.57 rests on the inner cone and is centered by the inner cone. The outer cone is guided by
the injection tube. The estimated mass in the two 1-mm-thick RTL cones is 90 kg plus the thicker
regions of 40 kg for a total of 130 kg. A 2-mm-thick RTL set would have a mass of 220 kg.

**Figure 4.57: RTL before shot during insertion.**

**Figure 4.58: RTL at shot time.**

**4.2.1.3** **Time-Motion Study**

A time-motion analysis determines the time between shots. The following is a list of separate events
that each contribute to the time elapsed between shots.
1. The RTL is translated into the breach of the injector tube and the breach cover is closed.
2. The inserter is mated to the RTL.
3. Downward motion:
a. The inserter is accelerated downward at 1 g until a distance of about 0.53 m before the
shot position.
b. The acceleration is increased to 2 g to cause the inner RTL cone to catch up to the outer
cone to within 1.5 mm at shot time.
c. Simultaneously the cover over the MITL opening is slide upward or opened.
d. Simultaneously the liquid is injected through a sequence of valves into the inserter cavity.
e. Simultaneously the plunger ejects the liquid at 15 m/s (5 m/s relative to the inserter speed
of ~10 m/s).
f. The inserter is accelerated upward at 20 g but continues its downward motion until the
turn around point.

4. Upward motion:
a. The inserter is accelerated upward at 20 g to a certain point.
b. Then the inserter is decelerated at 21 g until it comes to rest at the top.
c. Simultaneously the breach cover is removed.
d. Simultaneously the MITL faces are inspected by optical techniques for damage and
possibly cleaned off with a broaching tool. This step might add time to the sequence.

##### s2

**Figure 4.59: Illustration of injection sequence.**

We now go into detail to estimate the time needed for each operation. Definitions are given in the
Figure 4.59 above.

1. The RTL is translated into the breach of the injector tube and the breach cover is closed.

s = distance for deceleration,
t = time for deceleration,
a = deceleration rate,
v = translation speed to the breach.
Example, s = 0.5 m, a = 1 g,

_v_ = _at_ = 10 _m_ / _s_ [2] × 0.32 _s_ = 3.2 _m_ / _s_ 4.31

![](images/page_122_eq_0.png)

![](images/page_122_eq_1.png)

![](images/tmpvlzzzdgp.pdf-122-1.png)

2. The inserter is mated to the RTL

Time assumed to be 0.1 s.

3. Downward motion.
a. The inserter is accelerated downward at 1 g until a distance of about s2= 0.6 m before the
shot position. This downward motion is guided free fall. The outer cone is resting on the
inner cone.

The time for the outer cone to reach the shot point is:

_v_ = _at_ = 10 _m_ / _s_ [2] ×1.1 _s_ = 10.1 _m_ / _s_ = speed of the RTL at shot time. 4.33

b. The acceleration is increased to 2 g to cause the inner RTL cone to catch up to the outer cone
to within 1.5 mm at shot time assuming a starting gap of 15 mm.

![](images/page_123_eq_0.png)

Change in speed of the inner cone relative to the outer cone.

Δ _v_ = _at_ = 10 _m_ / _s_ 2 × .0037 _s_ = .037 _m_ / _s_ 4.35

![](images/page_123_eq_1.png)

_s_ 2 ≈ _vt_ = 101. _m_ / _s_ × .0037 _s_ = .037 _m_ = starting point for increased acceleration. 4.36

c. Simultaneously the cover over the MITL opening is slid upward or opened.
d. Simultaneously the liquid is injected through a sequence of valves into the inserter cavity.
e. Simultaneously the plunger ejects the liquid at 15 m/s (5 m/s relative to the inserter).
f. The inserter is accelerated upward at 20 g but continues its downward motion until the turn
around point.

![](images/page_123_eq_2.png)
The time to bring the inserter to 3 m from its starting position is

![](images/page_123_eq_3.png)
_a_ 20 ×

![](images/page_123_eq_4.png)
_m_ / _s_

_a_

20 ×10 _m_ /

![](images/page_123_eq_5.png)
2

= 0.23 s.

![](images/page_123_eq_6.png)

The time to turn-around is 0.053 s and the distance is

_s_ 4 = [1] 2 _[at]_ [ 2][ =][ 0.5][ ×][ 20][ ×][10] _[m]_ [/] _[s]_ [2][ ×][ (0.053] _[s]_ [)][2][ =][ 0.28] _[m]_ 4.38

4. Upward motion.
a. The inserter is accelerated upward at 20 g to a certain point 3 m from the starting point in
0.23 s.

![](images/page_124_eq_0.png)
The upward speed at 3 m from the starting position is

_v_ = _at_       - _vdown_ = 20 ×10 _m_ / _s_ [2] × 0.23 _s_ −10.62 _m_ / _s_ = 35.4 _m_ / _s_ 4.39

b. Then the inserter is decelerated at 21 g until it comes to rest at the top.

![](images/page_124_eq_1.png)

_a_ = _[v]_ [ 2]

2 _s_ 3

![](images/page_124_eq_2.png)

= [(35.4] _[ m]_ [ /] _[s]_ [)][2] = 209 _m_ / _s_ [2] = 21 _g_ 4.40

![](images/page_124_eq_3.png)
2 × 3 _m_

_t_ = _[v]_ _a_ [=] [35.4] 209 _m_ _[ m]_ / [/] _s_ _[s]_ [2] [=][ 0.17] _[s]_ [ = time to bring inserter to rest. ] 4.41

c. Simultaneously the breach cover is removed.

d. Simultaneously the MITL faces are inspected and possibly cleaned off.

**Table 4.6: Summary of RTL cycle times.**

The time for the various steps is tallied in Table 4.6 for a total estimated cycle time of
1.9 s. The most delicate operation occurs during loading the RTL in the breach of the inserter tube
where the sideways force is 1 g. The 1 g downward motion is a force-free operation (except for the
1-2 g jerk) taking the most time. The high g force operations are without the RTL during return of
the inserter to the starting point. The cycle time allows a fusion power of 3 GJ/1.9 s = 1.6 GW from
one chamber.

![](images/page_124_table_0.png)

|  | g force | Time, s |
| --- | --- | --- |
| Load the breach | -1 sideways | 0.32 |
| Mate inserter/RTL | 0 | 0.1 |
| Accelerate to shot point | 1 downward | 1.1 |
| Accelerate upward | 20 upward | 0.23 |
| Decelerate | 21 downward | 0.17 |
| Total time |  | 1.92 |

**4.2.1.4** **Features of the RTL and Chamber Design**

Features of the proposed RTL and chamber design are summarized here.
1. Inductance of the 3-m-long, 1-m-radius RTL transmission line is 15 nH out to 2 m radius where
the gap is proportional to radius and is assumed to be 30 mm at 2 m.
2. All structures are protected by 1 m of flibe. This should result in long life structures and better
economics due to reduced maintenance and downtime.
3. Guides or “bumps” in the RTL casting keep the spacing of 15 mm during insertion; gap =
0.015  - r
4. The 1.5 mm gap near the target is created “on the fly” with the shot triggered when it is
achieved. The inner and outer RTL cones are accelerated downward at 1 g (free fall) for 1.1 s or
a distance of 5.6 m. When the RTL is 0.6 m above and 0.055 s before shot time and position the
inner cone acceleration is increased to 2 g, which causes the gap to close from 15 mm to 1.5 mm
at which time the transmission line is triggered.
5. The two 2-mm-thick shells making up the RTL have a mass 150 kg and assuming another 100 kg
of stiffeners and electrode rings, 250 kg must be cooled from the liquid by about 400 K (heated
back up by a shot) amounting to 238 MJ of lost useful yield (250 kg × 2380 J/kg·K × 400 K =
238 MJ), representing 8% yield loss. The energy conversion efficiency of the plant will be
reduced by this amount. Said another way this amount of energy is not available to be converted
to electricity. Clearly a lighter mass RTL cone set would be desirable. Would RTL cones of 1
mm wall thickness be practical?
6. The RTL inserter also serves as a nozzle for pulsed injection of flibe. The RTL will be moving at
about 10 m/s at shot time and the liquid will be injected at about 15 m/s. The downward
momentum of this liquid (60,000 Pa·s) overcomes the upward shot momentum or impulse.
7. Steady or pulsed jets protect the chamber sidewalls from neutrons and blast.
8. A mushroom jet protects the bottom of the chamber from neutrons and blast.
9. The gas in the chamber will be that of the vapor pressure of the flibe.
10. The inserter covers the 15 mm MITL opening about 1.5 ms after the shot and resurfaces or
cleans the MITL electrode faces as it makes a two-way pass. The MITL cover covers the
opening at all times except at shot time and a few ms afterwards. Since flibe vapor is
condensable its pumping can be rapid. Very much non-condensable gas will preclude MITL
operation as rapid pumping is difficult. Designs with gas fill may be unfeasible based on the
inability to rapidly pump out the MITL and RTL.
The RTL shatters and is driven into downward moving liquid jets that carry them away. A worry is
contamination of the interior of the MITL before closure by the inserter in 1.5 ms. Flibe vapor
primarily from the transmission line current produced plasma will enter the MITL. This needs
estimating.

_4.2.2 First Wall Chamber Design Concept with Aerosol Mitigation_

Recent x-ray mitigation models have shown the possibility of designing a chamber with
a first wall. The idea of simplifying the internals of the fusion reaction chamber is beneficial. First,
the flibe blanket is moved to the exterior of the reaction chamber where it is used to breed tritium
and also acts as the heat transfer fluid. The reaction chamber would only contain the aerosol/gas
mixture and a possible sacrificial liquid (ablation liquid) to coat the wall. Both the aerosol and
ablation liquid layer could possibly be the same material as the RTL. This would simplify or

eliminate the separation issues in the internal thick liquid blanket design.. Tin and flibe have been
considered as possible candidate materials for such a design. Figure 4.60 illustrates a conceptual
vessel design using aerosols and a sacrificial liquid coating on the wall.

**Figure 4.60: A conceptual z-pinch fusion chamber utilizing an aerosol and ablation liquid**
**protection scheme.**

The target and RTL are inserted into the middle of the chamber through a top orifice.
The RTL connects to the driver and also forms a seal to contain the contents of the vessel before,
during, and after the fusion reaction. If the RTL is constructed of flibe, then the inner cone is filled
with flibe to protect the driver and RTL automation components from x-rays, debris, and neutrons.
If the RTL is Tin, then possibly a foamed Tin can fill the inner cone of the RTL. The key idea is to
keep all of the components and x-ray attenuating materials inside the chamber the same, with the
exception of the target, to eliminate separation issues. A rarified gas mixed with aerosolized liquid
is dispersed within the vessel through the nozzles shown in Figure 4.60 to act as the x-ray
attenuating medium. A thin liquid layer (ablation liquid) coats the vessel wall and protects it from
the remaining x-rays and extremely hot gas. The ablation liquid (same as RTL material) is injected
into the vessel through the jets illustrated in Figure 4.60.
It may be possible to sufficiently coat the chamber walls by the aerosol jets, thus
eliminating the need for additional jets for the ablation liquid. So a chamber design without the
ablation jets could be conceived for the power plant. If this were the case a spherical chamber could
be designed to contain the fusion reaction. Figure 4.61 illustrates a spherical chamber design
concept.

![](images/tmpvlzzzdgp.pdf-126-0.png)

![](images/tmpvlzzzdgp.pdf-127-0.png)

**Figure 4.61: A conceptual z-pinch fusion chamber utilizing an aerosol mitigation scheme in a**
**spherical vessel.**

As shown in Figure 4.60 and Figure 4.61 the ablation liquid, aerosol, RTL, and target
debris collect at the bottom of the vessel. The shrapnel from the RTL melts and mixes with the
ablation liquid at which time part of it is sent to be recycled into a new RTL and the remaining
material circulated back into the chamber. The target debris is filtered out from the liquid and either
recycled or re-fabricated into another target. Flibe surrounds the inner chamber and acts as the
tritium breeding and heat transfer working fluid. It is pumped from the top and exits through the
bottom after being heated by neutron deposition.
Moving the liquid flibe to the outside of the reaction chamber may cause neutron
embrittlement issues with the first wall. In addition, activation issues may also be a concern for
waste disposal depending on the material chosen for the vessel. Solutions to these issues may be
addressed by methods used to extend the life of LWR vessels and current fusion materials
development. Neutron embrittlement may be countered by thermal annealing which is discussed
briefly in section 4.2.4. Activation and waste disposal may not be as big of an issue if low activation
steels are used for the chamber. The materials analyzed as possible candidates for the fusion
reaction vessels for both transmutation and power plant designs are described in section 4.2.3.

_4.2.3 Chamber Materials_

Materials for the fusion reaction chamber were chosen on two criteria. The first was
that a material maintains reasonable mechanical properties at elevated temperatures. The second
was that the materials have very low elemental impurities minimizing the radioactivity of the
chamber at the end-of-life of the plant. Three materials were studied based on one or both of these

criteria. The two metallic material candidates were Hastelloy and low activation F82H ferritic steel.
The third material was carbon-carbon composites which was the material of choice for the thick
liquid fusion chamber concept described above in section 4.2.1.
End-of-life waste analysis was performed on both Hastelloy and F82H steel chambers.
ORIGEN2 was used to determine the long-lived and short-lived radionuclides that would developed
over the life of the power plant in operation for 40 years. ORIGEN2 models were run under the
assumption of the first wall chamber concept, meaning no neutron attenuation between the target and
the chamber wall. ORIGEN2 was then used to determine the specific activity at 10000 days after the
plant end-of-life or chamber discharge. The goal was to ensure that the specific activity (curies/m [3] )
of the chamber could be categorized as Class-C low level waste. The limits for Class C low level
radioactive wastes are shown in Table 4.7 and Table 4.8 [68].

**Table 4.7: Long-lived radionuclides.**

**Table 4.8: Short-lived radionuclides.**

**4.2.3.1** **Hastelloy**

Hastelloy has good mechanical properties at elevated temperatures up to 1100 K [68].
It has a fair amount of materials characterization available in the literature because it has been
considered for use in high temperature nuclear reactor designs [70]. However, it is alloyed with
significant amounts of Molybdenum and Niobium which may cause a waste disposal issue at the
plants end-of-life. Typical mechanical properties for Hastelloy as a function of temperature are
shown below [70].

![](images/tmpvlzzzdgp.pdf-128-0.png)

![](images/tmpvlzzzdgp.pdf-128-1.png)

![](images/page_128_table_0.png)

| Radionuclide | Concentration curies per cubic meter |
|---|---|
| C-14 | 8 |
| C-14 in activated metal | 80 |
| Ni-59 in activated metal | 220 |
| Nb-94 in activated metal | 0.2 |
| Tc-99 | 3 |
| I-129 | 0.08 |
| Alpha emitting transuranic nuclides with half-life greater than 5 years | 100 nanocuries/g |
| Pu-241 | 3,500 nanocuries/g |
| Cm-242 | 20,000 nanocuries/g |

![](images/page_128_table_1.png)

| Radionuclide | Concentration curies per cubic meter |
|---|---|
| Total of all nuclides with less than 5 year half-life | No limit (1) |
| H-3 | No limit (1) |
| Co-60 | No limit (1) |
| Ni-63 | 700 |
| Ni-63 in activated metal | 7000 |
| Sr-90 | 7000 |
| Cs-137 | 4600 |

Tensile Strength (MPa) as a function of temperature (K)

_TS_ = −.50659 ×10 −6 _T_ 3 + .90943×10 −3 _T_ 2     - .52334 _T_ + .18537 ×103 4.42

Yield Strength (MPa) as a function of temperature (K) :

![](images/page_129_eq_0.png)

_YS_ = −.28601×10 −6 _T_ 3 + .58034 ×10 −3 _T_ 2     - .37504 _T_ + .12031×103 4.43

Elastic Modulus (GPa) as a function of temperature (K):

![](images/page_129_eq_1.png)

_EM_ = .26541×10 −8 _T_ 3   - .97284 ×10 −5 _T_ 2 + .26188 ×10 −2 _T_ + .20838 ×10 2 4.44

![](images/page_129_eq_2.png)

10,000 hrs Rupture Strength (MPa) as a function of temperature (K):

_RS_ = .27870 ×10 −3 _T_ 2         - .64775 _T_ + .37922 ×103 4.45

![](images/page_129_eq_3.png)

**4.2.3.2** **Hastelloy Chamber Waste and Disposal**

Specific activity results from ORIGEN2 runs for a Hastelloy chamber, with an outer
radius of 5.9 m and a wall thickness of 35 cm, at discharge and 10000 days later were calculated.
These chamber dimensions were based on the Z-IFE baseline parameters determined in FY2005 [5].
The ORIGEN results for a Hastelloy chamber are shown in Table 4.9.

**Table 4.9: The specific activity for a Hastelloy chamber at discharge and after 10000 days.**

At 10,000 days (27.4 years) the intact Hastelloy chamber is below the Class C limits,
except for Ni63, which it exceeds slightly. For the intact chamber to meet the limits on this nuclide,
the volume would need to be about 10% larger. However, with the structural and piping supports, it
is likely that the disposal volume would be 10% larger. If the chamber is dismantled and cut or
disassembled into smaller sections, then it will exceed Class C limits of several isotopes.

![](images/tmpvlzzzdgp.pdf-129-0.png)

![](images/page_129_table_0.png)

| Radioactive Nuclides | Discharge | After 1000 Days | Intact Chamber (Vol=980.3 m³) | Compacted Chamber (Vol=144.2 m³) | Class C Limits |
|---|---|---|---|---|---|
| | Curies/kg | Curies/kg | Curies/m³ | Curies/m³ | Curies/m³ |
| H 3 | 4.30E-02 | 4.06E-02 | 1.43E-01 | 9.72E-01 | 8.00E+03 |
| Co 60 | 1.10E+02 | 3.00E+00 | 4.37E+01 | 2.61E+04 | no limit |
| Ni 63 | 6.49E+00 | 6.49E+00 | 2.44E+00 | 1.66E+01 | 7.00E+01 |
| Nb 94 | 1.27E-04 | 1.27E-04 | 1.86E-05 | 1.26E-04 | 0.019 |
| Tc 99 | 1.40E-03 | 1.40E-03 | 5.26E-04 | 3.57E-03 | 3.00E+00 |

This takes into account only the nuclides resulting from activation of the original
chamber materials. Fusion, transuranic, and coolant products that contaminate the chamber walls are
not taken into account and may result in the chamber being transuranic waste if it is not removed
during decommissioning.

**4.2.3.3** **F82H Low Activation Steel**

F82H (Fe-8%Cr-2%WVTa) is a low activation martensitic steel. This steel is
fabricated in such away to minimize impurities that have activation issues while in operation and
also for disposal. It is not produced commercially so it has not been fully thermally and
mechanically characterized compared to other conventional steels, especially in the area of fatigue
properties. Tavassoli et al. collected data from tests on standard specimens measuring creep and
rupture strength to estimate maximum allowable stress values using internationally accepted
procedures [71]. According to this study F82H steel alone maintains reasonable strength up 973K.
In a study by Zinkel et al., if Y2O3 is added to the alloy it increases the creep rupture strength from
100 MPa to 300 MPa at a temperature of 923 K for a rupture time of 1000 hours [72]. This
improvement in strength allows the material to be used for operating temperature in excess of 973 K.
F82H is the leading candidate for the fusion power plant chamber because of its low-waste hazard
and possibility of being used in elevated temperatures using ODS alloying. Typical mechanical
properties as a function of temperature for this steel are shown below [71]. The fatigue properties
are illustrated in detail in section 4.2.5.

Tensile Strength (MPa) as a function of temperature (K):

_TS_ = .62357 ×10 −9 _T_ 4 −.11166 ×10 −5 _T_ 3 + .5472 ×10 −3 _T_ 2 −.11617 _T_ + 6288. 4.46

![](images/page_130_eq_0.png)

Yield Strength (MPa) as a function of temperature (K):

_YS_ = −.35596 ×10 −9 _T_ 4 + .22141×10 −6 _T_ 3   - .3603×10 −4 _T_ 2 −.18491×10 −1 _T_ + 5442. 4.47

![](images/page_130_eq_1.png)

Elastic Modulus (GPa) as a function of temperature (K):

![](images/page_130_eq_2.png)

_EM_ = 233 − .00558 _T_ 4.48

**4.2.3.4** **F82H Steel Chamber Waste and Disposal**

Specific activity results from ORIGEN2 runs for a F82H steel chamber, with an outer
radius of 5.9 m and a wall thickness of 35 cm, at discharge and 10000 days later were calculated.
These chamber dimensions were based on the Z-IFE baseline parameters determined in FY2005 [5].
The ORIGEN results for a F82H chamber are shown in Table 4.10.

**Table 4.10: The specific activity for a F82H steel chamber at discharge and after 10000 days.**

For all times evaluated from discharge after a 40 year life, to 10,000 days later, the
activity of the selected nuclides are less than the limits for Class C low-level waste. This is true for
both the intact chamber volume and the compact chamber volume.

**4.2.3.5** **Carbon-Carbon Composites**

PAN (polyacrylonitrile) based fibers constitute the largest segment of the carbon fiber
industry [73]. They have a high tensile strength over a large range of temperatures. Carbon fibers
are joined together in various orientations in a matrix material, which is also carbon based. The
carbon-based matrix does have an impact on the mechanical properties of the composite by affecting
its modulus of elasticity, stress-strain behavior, bond strengths between fibers and matrix, and
strength in tension [74].
The mechanical properties of carbon-carbon composites are highly dependant on the
orientation of the fibers. The fibers can range from one to four dimensional geometries. The
mechanical properties shown below are based on a two-dimensional arrangement of fibers. This
orientation was chosen for two reasons. First, the mechanical properties for a two dimensional
carbon-carbon composite were readily available. Second, internal loading applies tensional stress
perpendicular to the pressure force in the chamber, which two fiber orientations should be able to
address. A third fiber orientated parallel to the pressure force will probably be needed in order to
handle external induced stresses in the chamber caused by the between shot vacuum condition. The
external loading induced stresses are not considered for carbon-carbon composites
The major contributions to cost of carbon-carbon composites are how they are
processed and cured. Depending on the application, curing temperatures can exceed 1273 K
requiring use of special equipment [73]. The fatigue properties of C-C composites still need to be
assessed extensively for both irradiated and normal type environments. Typical properties for PAN
based C-C composites are shown below. The tensile strength increases with temperature in contrast
to metal materials.

![](images/tmpvlzzzdgp.pdf-131-0.png)

![](images/page_131_table_0.png)

| Radioactive Nuclides | Discharge | After 3 Days | Intact Chamber (Vol =860.3 m³) | Compacted Chamber (Vol =144.2 m³) | Class C Limits |
|---|---|---|---|---|---|
| | Curies/kg | Curies/kg | Curies/m³ | Curies/m³ | Curies/m³ |
| H 3 | 1.05E+04 | 9.46E+03 | 1.16E+01 | 6.92E+01 | 8.00E+03 |
| C 14 | 5.38E-06 | 5.38E-06 | 6.60E-09 | 3.94E-08 | 8.00E+00 |
| Co 60 | 1.97E-01 | 5.36E-03 | 6.58E-06 | 3.93E-05 | 7.00E+01 |
| Nb 93 | 4.18E-06 | 4.18E-06 | 5.12E-09 | 3.06E-08 | no limit |
| Ni 63 | 7.46E-06 | 7.46E-06 | 9.15E-09 | 5.46E-08 | 7.00E+01 |
| Si 90 | 3.05E-10 | 1.90E-10 | 5.92E-06 | 1.49E-06 | 4.16E-06 |
| Nb 94 | 1.85E-06 | 1.85E-06 | 2.27E-09 | 1.35E-08 | 0.016 |
| Tc 98 | 2.05E-06 | 2.05E-06 | 2.51E-09 | 1.50E-08 | 4.16E-06 |

Tensile Strength (MPa) as a function of temperature (K):

_TS_ = .00261 _T_ + 302.47 4.49

![](images/page_132_eq_0.png)
Elastic Modulus (GPa) as a function of temperature (K):

![](images/page_132_eq_1.png)
_EM_ = −.00278 _T_ + 118.29 4.50

_4.2.4 Thermal Annealing_

Thermal annealing of LWR pressure vessels to extend their operational life has been
demonstrated in Europe, Russia, and the United States [41, 75, 76]. The Nuclear Regular
Commission has approved an annealing process for LWR pressure vessels following the guidelines
set forth by the ASME Boiler and Pressure Vessel Code [77]. The main areas of concern for LWR
pressure vessels are in the weld joints in particular the beltline region. It is subject to the most
intense neutron flux. The weld areas on the Z-IFE vessel will probably be the greatest concern as
well.
Thermal annealing has shown to be effective in completely recovering the upper shelf
energy (USE) and yield strength while partially recovering the ductile-brittle transition temperature
(DBTT) of WWER-400 and WWER-1000 steels [41]. WWER-1000 and WWER-400 steels are
commonly used in Russian reactor vessels. The only partial recovering of the DBTT seems to be
dependant on the amount of nickel in the material [41]. Nickel, which is common alloy in weld
materials, seems to both effect the extent of radiation damage and recovery of the DBTT. The time
and extent of healing was greatly dependant on the annealing temperature. As the annealing
temperature increased the recovery of the materials’ properties increased. Annealing temperatures
ranging from 420ºC to 490ºC have been investigated [41}. Thermal annealing may be useful for the
Z-IFE chamber.
Candidate fusion materials have shown to be irradiation resistant at elevated
temperatures. Several irradiation tests have been conducted on F82H steel and yielded similar
results. Experiments showed that the yield strength of the steel under normal and irradiation
conditions did not change significantly at higher temperatures. Figure 4.62 shows the yield strength
of F82H steel for both normal and irradiated results as a function of temperature [72].

![](images/tmpvlzzzdgp.pdf-133-0.png)

**Figure 4.62: Shows a comparison between unirradiated and irradiated F82H steel versus**
**temperature.**

The green line represents the best fit curve for the unirradiated steel. At lower
temperatures (0ºC- 400ºC) a significant increase in yield strength is observed for irradiated steel. As
the temperature is increased above 400ºC the change in yield strength is less thus indicating thermal
annealing effects.
Further studies of various fusion materials were conducted on USE and DBTT. These
parameters did not show a significant change at high irradiation temperatures. If the vessel is to
operate in the material’s annealing range the irradiation damage effects seem to be minimal and may
not pose a serious threat. Figure 4.63 shows irradiation induced shifts in the USE and DBTT versus
irradiation temperature of various materials [78].

**Figure 4.63: Irradiation induced shifts for upper shelf energy (left) and ductile brittle**
**transition temperature (right) verse irradiation temperature.**

![](images/tmpvlzzzdgp.pdf-133-1.png)

Once again, as the temperature increases the difference in USE and DBTT between
unirradiated and irradiated steel is insignificant. Since the Z-IFE chamber will be operating at or
above the effective annealing temperature of these steels it may be possible to minimize or eliminate
the effects of irradiation damage.

_4.2.5 Fatigue Analysis of F82H Steel_

Fatigue is a crucial design parameter for both the transmuter and power plant designs.
Both vessels will be subject to cyclical loading on the order of 0.1 Hz. Effects such as irradiation
damage and dynamic loading can greatly reduce the lifetime of the chamber wall. This is a firstorder analysis of the expected lifetime of the inner-liner of an operating fusion reactor. The analysis
uses only readily available data for F82H from the open literature. The results of the analysis are
highly dependent upon the assumed sustained operating temperature of the reactor, specifically the
temperature of the inner wall, and the stresses imparted to the F82H lining during operation of the
reactor.

**4.2.5.1** **Selection of F82H Steel for the Vessel Wall**

F82H is a ferritic/martensitic reduced activation steel which comprises of between 812wt% Cr and has been alloyed with low activation elements. Ferritic steels have also shown lower
irradiation induced swelling compared to standard fission reactor stainless steel liners [79]. F82H is
one of the leading candidates for fusion power systems and so a fairly large mechanical and thermal
material property database exists.
The mechanical properties of F82H have shown to exhibit embrittlement in irradiation
environments. However, increasing amounts of data are becoming available to account for
irradiation damage. Another important area where data is becoming more readily available is in the
area of welds. Irradiation damage has generally been more of a concern on the welds of fission
reactor chambers, consequently, welding of the F82H steel which has not be studied in-depth must
be analyzed further. Creep is another potentially harmful mechanism if the fusion system operates at
temperatures above 550°C (823°K) [80]. Thus, the chamber must be designed to operate at a lower
temperature where creep is not as significant.
Some of the key properties of F82H steel that are not well understood are fracture
properties in radiation environments. Also, helium induced swelling of the liner material and its
effects on the fracture properties. High cycle fatigue data still needs to be assessed for IFE based
systems.

**4.2.5.2** **Vessel Dimensions and Operating Conditions**

It is assumed that the reactor is a sphere with a radius of five meters. The inner lining
of this sphere is composed of F82H steel. The surface area of the inner lining is 314.16 m [2] (A =
4πr [2] ) or 3.1416x10 [6] cm [2] . The lining is subjected to an irradiation pulse every ten seconds which
imparts 1x10 [21] neutrons to it. So the average flux on the inner lining is:

1x10 [21] neutrons/pulse = 1x10 [21] n/10 seconds = 1x10 [20] n/s

And, the flux density is:

(1x10 [20] n/s) / (3.1416 cm [2] ) = 3.185x10 [13] n/s-cm2

The fluence to which the lining would be subjected is expressed in units of
neutrons/cm [2] . So, for example, in one hour (3600 seconds; 360 pulses) of continuous operation, the
inner lining of the reactor would have a fluence of: 3.185x10 [13] n/s-cm [2] X 3.6x10 [3] seconds =
1.15x10 [17] n/cm2,

![](images/page_135_eq_0.png)
and, in one day, 2.75x10 [18] n/cm2,
in thirty days (one month), 8.25x10 [19] n/cm2,
and, in 365 days (one year), 1.00x10 [21] n/cm2 (= 1 dpa)

[80, 81, 82, 83]. The properties of the F82H steel are, of course affected by the total damage to the
material (the total fluence). The time to impart a dpa of 1, 10, or 100 is 1, 10, or 100 years for the
scenario analyzed.

**4.2.5.3** **Inner-Wall Operating Temperature**

The operating temperature of the reactor, specifically the inner lining, has yet to be
fixed, but may range from 600K – 900K (327ºC – 627ºC). This is an important consideration
because the temperature of the F82H affects its properties and the degree to which irradiation further
affects the properties. At certain elevated temperatures irradiation damage, which affects, e.g.,
strength and fatigue endurance, is partially or nearly completely annealed from the material. And,
above a certain temperature creep affects severely affect the useful life of F82H steel.
There have been numerous studies of the creep and stress-rupture behavior of
unirradiated and irradiated 8-9%Cr steels at temperatures up to 923K (650°C [0.5 TM]) [84]. Good
creep resistance exists for temperatures up to ~823K (550°C [0.45 TM]), but poor creep resistance
occurs at 873K (600°C) and above. For example, the 10,000 h creep rupture strength of F82H is 200
MPa at 823K, 120 MPa at 873K and 50 MPa at 923K. Improvements in the thermal creep resistance
of reduced-activation ferritic steels can be achieved with oxide dispersion strengthened alloys.
This suggests maintaining a temperature on the inner wall of the reactor to below 823K
(550ºC) to avoid the affects of creep:

Tcreep > 823K (>550ºC), Tinner-wall < 823K (<550ºC)

**4.2.5.4** **Irradiation Damage**

At ambient temperatures irradiation damage affects the mechanical properties of F82H
steel. Irradiation damage also occurs at elevated temperatures up to a certain temperature where the
temperature effectively anneals out the damage (at least below some threshold of fluence or dpa).
One measure of irradiation damage is an increase in yield strength of the material, or a decrease in
elongation (ductility). And the temperatures at which irradiation occurs for which there is no

increase in yield strength are those for which thermal annealing mitigates the irradiation damage.
Several references provide data that suggests that at irradiation temperatures of 623K – perhaps
750K (350ºC – 477ºC) the properties of the F82H are not significantly affected by the irradiation
hardening at least up to ten dpa or higher [85, 86, 87, 88, 89].
Using the midrange of the temperatures for which thermal annealing seems effective,
say, 673K – 723K (400ºC – 450ºC), the detrimental affects of irradiation hardening (and creep [Tcreep

- 823K (>550ºC)]) may be negligible:

Tirr. damage < 673K (<400ºC), Tinner-wall > 673K (>400ºC)

Thus, a suggested temperature range for operation of the reactor to avoid both irradiation damage
effects and creep is:

823K > Tinner-wall > 673K 550ºC > Tinner-wall > 400ºC

**4.2.5.5** **Applied Stresses**

The maximum design stress to which the inner lining may be subjected is assumed to
be ¼ the ultimate tensile strength (¼UTS) of unirradiated and ambient temperature F82H. Data
from typical references suggest a UTS of approximately 663.3 MPa (96.3 ksi) at approximately
293K (20C) [71, 85, 86, 87, 88, 89]. So, the maximum stress, σmax, assumed for the inner wall of the
lining is 663.3/4 = 165.8 MPa (24.1 ksi). (This stress shall be used for the analysis despite the fact
that the UTS of F82H steel at an elevated temperature or in an irradiated condition will be less than
that at ambient temperatures.) Young’s modulus for F82H steel is approximately 217 GPa (31E6
psi) at a temperature of 293 K (20C) [90].

**4.2.5.6** **Fatigue as the Failure Mode**

The assumed failure mode for the inner liner is fatigue failure. The applied stresses,
¼UTS, are below the stress required to plastically deform the material. Assuming no significant
flaws in the lining, the fracture toughness should be adequate to preclude crack growth from an
existing flaw. However, the lining is subjected to tensile stresses every pulse (ten seconds) and this
cyclic loading of the material could induce fatigue and ultimately failure (large crack) of the liner.
Each stress impulse imparts strain to the lining. The magnitude of this strain can be
used to estimate the number of cycles the lining can withstand before there may be a fatigue failure.
The strain on the lining is estimated to be:

Maximum strain per irradiation pulse = εmax
= maximum stress / Young’s modulus = ¼UTS / Young’s modulus
= 165.8 MPa / 217E3 MPa
= 0.00076 (cm/cm), or 0.076%

This strain per cycle is actually relatively low. The total strain is twice that value since
the stress is reversed after the irradiation pulse. So, the total strain per cycle is:

εtotal = 0.0015 (cm/cm) = 0.15%

![](images/page_136_eq_0.png)

There is little fatigue data available for F82H steel either in the unirradiated or
irradiated condition. However, total strain versus number of fatigue cycles to rupture is available in
the literature. If the reactor operates in a temperature regime where thermal annealing is effective,
the fatigue data for unirradiated F82H may be used. For a total strain of 0.15%, the 450ºC and
500ºC data indicate that the number of cycles to rupture may be as few as approximately 500000
cycles. Those same data indicate that to operate the reactor for five years (which translates to
15778800 irradiation pulses), the total strain should not exceed 0.05%. This would require that the
maximum stress on the lining per pulse be reduced by a factor of three [71].
The Hirose et al. reference is less useful because the data are for fewer than 10000
cycles [75]. It does indicate that F82H irradiated at 363K (90ºC) can withstand fewer cycles to
failure than unirradiated material when tested at 293K (20ºC). For example, at 1% total strain, F82H
can with stand 4575 cycles before failure, but in the irradiated condition (0.02 dpa) only 2364 cycles.
Linear extrapolation of the available Hirose data for a total strain of 0.15% suggests that the F82H
lining can withstand perhaps more than 25000 cycles before failure if operating at a temperature
where irradiation hardening is not a significant factor. The number of cycles may be many more
than that depending on the trend of the fatigue curve at low strain / high cycle conditions [75].
The Tavassoli et al. data are plotted in Figure 4.64, below [71]. Endurance limit strain
data plotted in Figure 4.64 appears to fit a log-log relationship.

![](images/page_137_eq_0.png)

lnε= ln _A_ + _m_ ln _N_ 4.51

![](images/page_137_eq_1.png)
Or

ε= _A_ ⋅ _N_ _m_ 4.52

A linear regression analysis of the data using Equation lnε= ln _A_ + _m_ ln _N_ 4.51
returns A = 5.472 and m = -0.237. The standard error of the estimate, _sey_, for this regression is
0.181. The dashed lines in Figure 4.64 denote bounds 3 _sey_ on each side of the regression. The lower
bound represents a factor of safety of 1.72.

10

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|E|nd|uranc|e L|im|it D|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||
|||||||||||||||||||||||||~~ °~~|~~ C~~||||
|||||||||||||||||||||||<br>|<br>|<br>|<br>||||
|||||||||||||||||||||||||~~0~~|~~ °C~~||||
|||||||||Ex|tra|p|ol|ate|d end|ura|ura|nc|e|||||||~~0~~|~~ °C (d~~|~~  am~~|~~  et~~|~~  ral)~~|
|||||||||<br>lim<br>|<br>it<br>|<br> b<br>|<br> as<br>|<br> ed<br>|<br>  on ch<br>|<br>   am<br>|<br>   am<br>|<br>   be<br>|<br>   r<br>|||||<br>|<br>|<br>50|<br> °C||||
|||||||||op<br>0.|er<br>|at<br> z|io<br> .|n f|r 5 ye|ars|ars|at||||||<br>5<br>5|<br> <br>|<br>00<br>50|<br> °C (d<br> °C|iam|et|ral)|
||||||||||||||||||||||||||||||
|||||~~±3~~σ|~~  bound~~|~~  s~~||||||||||~~y~~|~~ =~~<br>~~R~~<br>|~~  5.4~~<br>2 =|~~  179x~~<br>-0.<br> 0.821|237<br> 9|2||||||||
||||||||||||||||||||||||||||||
||~~Sou~~|~~rce~~|~~:  A~~|~~  .F. Ta~~|~~   vassoli,~~|~~    J.W. Ren~~|~~     sman,~~|~~      M.~~|~~       Sc~~|~~       hi~~|~~       rra~~|~~      , K~~|~~        .~~||||||||||||||||
||~~Shi~~|~~ba;~~|~~ "M~~|~~ aterial~~|~~ s Design~~|~~   Data fo~~|~~    r Reduc~~|~~     ed~~|~~      A~~|~~      ti~~|~~      va~~|~~      tio~~|~~      n~~||||||||||||||||
||<br>~~Mar~~<br>|<br>~~ten~~<br>|<br>~~siti~~<br>|<br>~~c Stee~~<br>|<br>~~ l type F8~~<br>|<br>~~   2H"; Fus~~<br>|<br>~~    ion Eng~~<br>|<br>~~     ine~~<br>|<br>~~     er~~<br>|<br>~~     in~~<br>|<br>~~     g~~|<br>~~      an~~|<br>~~      d~~||||||||||||||||
||~~Des~~<br>~~http~~|~~ign~~<br>~~://fu~~|~~, 2~~<br>~~sio~~|~~ 002, V~~<br>~~nnet.~~|~~  olume 6~~<br>~~eas.ucl~~|~~   1-62, Pa~~<br>~~.edu/Fu~~|~~    ge 617~~<br>~~sionNe~~|~~     62~~<br>~~two~~|~~     8.~~<br>~~rk~~|<br>~~/p~~|~~ro~~|~~pe~~|~~rties.p~~||||||||||||||||
||~~Des~~<br>~~http~~|~~ign~~<br>~~://fu~~|~~, 2~~<br>~~sio~~|~~ 002, V~~<br>~~nnet.~~|~~  olume 6~~<br>~~eas.ucl~~|~~   1-62, Pa~~<br>~~.edu/Fu~~|~~    ge 617~~<br>~~sionNe~~|~~     62~~<br>~~two~~|~~     8.~~<br>~~rk~~|<br>~~/p~~|~~ro~~|~~pe~~|~~rties.p~~||||||||||||||||
|hp?|hp?|mi|d=S|T-M-F|M-%231|01&tid=|0204P-0|20|0|||||||||~~D~~<br>us<br>sa|~~sign s~~<br>ing a fa<br>fety of 3|~~ ra~~<br>  ct<br>  .5|~~ n~~<br>  or|~~  li~~<br>   of|<br>|~~  t~~|||||
|hp?|hp?||||||||||||||||||||||||||||

1.E+02 1.E+03 1.E+04 1.E+05 1.E+06 1.E+07 1.E+08

**Number of Cycles to Rupture (N)**

**Figure 4.64: F82H endurance limit design parameters based on five year life**

This factor of safety was judged inadequate based primarily on the degree of
extrapolation necessary to reach the projected life for fusion equipment, in particular the chamber.
A factor of safety of 3.5 is qualitatively more acceptable.

Based on this, the maximum allowable stress based on endurance limit (cycles to
failure) and accounting for a safety factor on the strain (hence, stress) may be estimated for F82H
from the following equation

_m_

![](images/page_138_eq_0.png)

_AEN_ _m_
_s_ = . 4.53
_F_

_s_

![](images/page_138_eq_1.png)
As discussed above, Young’s modulus, E, for F82H is 217x10 [9] Pa (217x10 [4] bar). Using
a factor of safety, _Fs_, this yields the equation

_s_ = 1.18 _E_ 07 _N_ [−] 0.232 bar 4.54

Figure 4.65 plots this equation based upon a loading frequency of 0.1 Hz.

1400

1200

1000

800

600

400

5 7 9 11 13 15 17 19 21 23

**Design Life (years)**

**Figure 4.65: Maximum design stress versus design life based upon fatigue cycles to failure.**

For a design life of, say, ten years, the F82H steel lining could tolerate a stress of
approximately 560 bar (≅ 56MPa ≅ 8 ksi ≅ 0.08UTS) with a safety factor of 3.5 on the number of
fatigue cycles to failure. Lesser factors of safety, or fewer years of design life, allow the applied
stress to the F82H steel lining to be increased.

###### **5. CONCLUSION**

In the six months given to work on the Z-Inertial Fusion Energy (Z-IFE) late start
LDRD, an effort was made to create a logical path to reach the ultimate goal of a fusion power plant.
To illustrate this path forward a roadmap was created outlining the current issues, needed steps, and
time required to reach these goals.
The purpose of the roadmap is an attempt to gain an understanding on what it would
take to develop Z-IFE fusion energy. It begins with utilizing existing facilities capable of handling
various separate effects experiments. These facilities include Sandia National Laboratories’ Zbeamlet and ZR where several containment and mitigation experiments can be conducted. The next
step is to build an engineering test facility (ZN) where automation, RTL, target fabrication, and
driver development can take place and eventually be integrated together. With the inception of the
Global Nuclear Energy Partnership (GNEP) initiative and the goal of a closed fuel cycle, an
alternative use for z-pinch driven fusion arises. Work conducted through the Advanced Fusion
Concepts: Neutrons for Testing and Energy Grand Challenge LDRD has shown that fusion neutrons
can transmute the actinides in spent fuel. The ZN facility will also be the test bed for developing ZIFE fusion transmutation. Once these concepts are integrated, ZN becomes a pilot plant which will
be the final stage before the full scale transmutation and power plants are built.
Z-IFE progress this year is an extension of the work competed for the Advanced Fusion
Concepts Grand Challenge LDRD, with a focus on the full scale transmutation and power plants [1].
The grand challenge LDRD concentrated on developing the early steps in the roadmap involving
containment experiments on ZR.
Substantial progress was made in the areas of shock mitigation, chamber design, RTL
development, Flibe chemistry, and systems cost models for both the transmutation and power plants.

     - The transmutation work focused on designing a chamber capable of utilizing the high
energy neutrons from a z-pinch reaction to burn actinides. The key advantages to
transmuting actinides with this design are: a safer design compared to faster reactors, no
additional actinides are created since no fertile material such as uranium is required, and
provides valuable operating experience that will be needed for the full scale power plant.
A separate report, “Fusion Transmutation of Waste: Design and Analysis of the InZinerator Concept,” describes this work in more detail[5]

     - A systems cost model was created to optimize the number of chambers, the target yield,
and shot rate needed for a fusion power plant. The results indicated that less chambers at
a higher repetitive rate and yield are more economical than the original Z-IFE power
plant design of ten chambers.

     - A detailed cost analysis of the linear transformer driver (LTD), the device that supplies
the power to the fusion target, was conducted for the power plant facility. The results
indicated that it will be a significant percentage of the total cost of the plant.

     - Various studies between the chemical interaction between a flibe like salt and a steel RTL
post shot were conducted. This was to gain an understanding of how the free ions of the
dissociated salt and steel interact. Further experimentation on the electrical properties of
a frozen flibe RTL was conducted to understand its effectiveness of transmitting the pulse
to the target.

     - An analysis on four power conversion systems was conducted; supercritical CO2 cycle,
Rankine cycle, Brayton cycle, and a combined cycle. Assuming that high temperature
materials are available in the future, the analysis shows that the combined cycle is best
for both transmutation and power plants.

     - A tritium permeation study of the piping and chamber was addressed this year. It was
compared to the analysis conducted for the International Thermonuclear Experimental
Reactor (ITER). The results showed that using a permeation barrier coating on the pipes
along with optimizing partial pressure and diameter could reduce tritium leakage
significantly.

     - A new higher repetitively rated thick liquid curtain chamber design was proposed based
on the results from the systems cost analysis. This proposed chamber design requires a
slightly larger target yield and over fives times the repetitive rate of the original Z-IFE
design.

     - Modeling results of aerosols absorbing x-rays show promise that they may be able to
mitigate fusion yields up to 3 GJ. Based on these results a new first wall chamber design
was conceived that may significantly reduce the complications associated with the thick
liquid curtain designs.
The research this year is leading towards an experimental program to address issues
such as x-ray mitigation and containment, rapid vacuum development, driver testing, RTL
optimization, target development, and automation. Sandia has the state-of-the-art facilities and the
full spectrum of technical capability to provide the necessary elements for a strategic initiative. The
ZR-machine provides an ample facility for conducting the necessary physics and engineering
experiments required for increasing fusion yield, demonstrating fusion containment, and target
development. Sandia has a talented robotics group which can aid in designing the automation
required for maneuvering the RTLs in and out of the containment chamber. Sandia has experts in
materials which will be valuable in several aspects of this work. Material development for the
vessel, RTL, and power plant will be essential to ensure safe operating conditions. Sandia has
extensive programs that support energy research and development ranging from solar and wind to
nuclear power. There are also several years of research completed through the Z-IFE program on
using z-pinch IFE to create commercial power. Recently the focus of Z-IFE has shifted to include
using z-pinch fusion for transmutation, tying Z-IFE directly into the GNEP initiative and its focus on
a closed nuclear fuel cycle. Sandia National Laboratories leads the way in developing z-pinch
driven IFE energy for both power production and transmutation.

###### **6. REFERENCES**

1 Executive Summary

2 Z-Inertial Fusion Energy Roadmap

1. Morrow, C. et al., “Roadmaps and Containment Concepts for Early Z-Pinch Fusion
Applications,” Sandia National Laboratories, To be published SAND report, SAND####
(2006).
2. Olson, C., Personal Conversation, (October 2006).
3. Vesey, R., Slutz, S., & Mattsson, T., Personal Conversation, (June 2006).
4. “The Global Nuclear Energy Partnership: Greater Energy Security in a Safer, Cleaner
World,” Power Point Presentation: Department of Energy, USA, February 2006.
5. Cipiti, B. et al., “Fusion Transmutation of Waste: Design and Analysis of the In-Zinerator
Concept,” Sandia National Laboratories, To be published SAND report, SAND#### (2006).

3 Z-IFE Power Plant Systems Analysis

6. Meier, W.R., & Moir, R.W., “Analysis in Support of Z-Pinch IFE and Actinide
Transmutation- LLNL Progress Report for FY-06,” Lawrence Livermore National
Laboratories, UCRL-TR-224558, (2006).
7. Olson, C., “Target Physics Scaling for Z-Pinch Inertial Fusion Energy, “Fusion Science and
Technology, 47 1147-1151 (2005).
8. Vessy, R., “Multi-GJ Indriect-Drive Targets for Z-IFE Using the Double Ended Hohlraum,
“Z-IFE Workshop, SNL (Aug. 2005).
9. Melhourn, T., “Overview of Targets for IFE,” Z-IFE Workshop, SNL (Aug. 2005).
10. Meier, W.R. et al., “OSIRIS and SOMBRERO Inertial Fusion Power Plant Designs, “WJSA
report WJSA-92-01, DOE/ER/541000-1 (March 1992).
11. Meier, W.R., Bieri, R.L., “Economic Modeling and Parametric Studies for Osiris- AN HIFDriven IFE Power Plant,” Fusion Technology, 121, 1547 (1992).
12. Moir, R.W. et al., “HYLIFE-II progress report” LLNL Report UCID-211816 (1991).
13. Rochau, G., “Power Plant Utilizing Z-Pinch Fusion Technology,” Z-IFE Workshop, SNL
(Aug. 2005).
14. Rickman, W., & Goodin, D., “Cost Modeling for Fabrication of Direct Drive Inertial Fusion
Energy Targets,” Fusion Science and Technolgy, 43, 353 (2003).
15. Meier, W.R., “Systems Modeling and Analyses – Progress Update and Recent Results,”
HAPL Project Meeting (ORNL, MARch 21-22, 2006), LLNL document UCRL-PRES219894.
16. Stygar, W.A., Cuneo, M.E., Headley, D.I, Ives, H.C., Leeper, R.J., Mazarakis, M.G., Olson,
C.L., Porter, J.L., Wagoner, T.C; Architecture of PetaWatt-class Z-Pinch Accelerators;
Unpublished draft; 2006.
17. Ulrich, G.D., Vasudevan, P.T.; Chemcial Engineering Process Design Process Design and
Economics a Practical Guide; 2 [nd] edition; Process Publishing; 2004; ISBN 0-9708768-2-3.
18. Chemical Engineering Magazine ongoing feature.
19. http://www.eia.doe.gov/; U.S. Department of Energy, Energy Information Administration.
20. http://www1.jsc.nasa.gov/bu2/learn.html NASA; Cost Estimating Web Site; Learning Curve
Calculator

21. Dostal, V., Driscoll, M.J., Hejzlar, P., Wang, Y., “Supercritical CO2 cycle for Fast GasCooled Reactors,” Proceedings of ASME Turbo Expo 2004, Power for Land, Sea, and Air,
June 14-17, Vienna, Austria, 2004.
22. Pikard, P., Energy Conversion, Workshop for Universities, Githersburg, MD, 2004.
23. Williams, S. & Causey R., Personal communication on Tritium recovery and processing.
DIFFUSE models, Sandia National Laboratory, Livermore, July 2006.
24. Baskes, M.I.; DIFFUSE-83; SAND83-8231; 1983.
25. Serra, E., Benamati, G., Ogorodnikova, O.V., Hydrogen isotopes transport parameters in
fusion reactor materials; J. Nucl. Mater.; 255 (1998) 105.
26. Sugisaki, M., Furuya, H., Ueki, H., Ejima, S.; Surface Reaction and Bulk Diffusion of
Tritium in SUS-316 Stainless Steel; J. Nucl. Mater.; 133&134 (1985) 280
27. Sugisaki, M., Furuya, H., Ono, K, Idemitsu, K., Tritium Solubility in SUS-316 Stainless
Steel; J. Nucl. Mater.; 120 (1984) 36.
28. Hollenberg, G.W., Simonen, E.P., Kalinin, G., Terlain, Tritium/hydrogen barrier
development; Fusion Eng. & Design 28 (1995) 190.
29. Abdou, M., Schmitz, L., Ying, A., Sketchley, T., & Tajima, Y., “UCLA Research Activities
in Support of the Z-Pinch IFE Program – Final Report for FY06,” University of California at
Los Angles (2006).
30. Calderoni, P., Schmitz, L., & Ying, A., Progress Report to Sandia National Laboratories
(1995).
31. Cipiti, B., “RTL Manufacturing Plant Options: Z-Pinch IFE Final Report,” Sandia National
Laboratories (2005).
32. Morrow, C. et al., “ZIFE Project Process Flow Sheet Preparation for Z-Pinch Driven Fusion
Power Plant,” Sandia National Laboratories (2005).
33. Moir, R., Personal Correspondence, Lawrence Livermore National Laboratories (2006).
34. Chase, W.M., “JANAF Thermochemical Tables,” Journal of Physics and Chemistry Ref.
Data, 14, Suppl. 1 (1985).
35. Baes, C.F., “The Chemistry and Thermodynamics of Molten Salt Reactor Fuels,” Journal of
Nuclear Mateials, 51, (1974) 149.
36. Nishimura, H. et al., “Chemical Behaviour of Li2BeF4 Molten Salt as a Liquid Tritium
Breeder” Fusion Engineering and Design, 58-59 (2001) 667.
37. Schmitz, L., Calderoni, P., Ying, A., & Abdou, M., JNM 337-339 (2005) 1096.
38. Griem, H., “Plasma Spectroscopy” McGraw Hill, New York (1984), pp. 267.
39. Gardiner, W.C., “Combustion Chemistry, Springer, New York (1984), pp. 177.
40. Chan, X.M., Schrock, V.E., & Peterson, P.F., Fusion Technology 21 (1992) 1536.

4 Chamber Design and Shock Mitigation

41. Kryukov, A.M., Nikolaev, Yu.A, & Nikolaeva, A.V., “Behavior of Mechanical Properties of
Nickel-Alloyed Reactor Pressure Vessel Steel Under Neutron Irradiation and Post-Irradiation
Annealing,” Nuclear Engineering and Design, 186, p. 535-359, (1998).
42. Romero, D.H., Personal interview July 2006, Sandia National Laboratories
43. Brunner, T.A. et al., “A User’s Guide to Radiation Transport in ALEGRA-HEDP, Version
4.7-beta,” Sandia National Laboratories, SAND200x.
44. Brunner, T.A. et al., “ALEGRA-HEDP: Version 4.6 (revised),” Sandia National
Laboratories, SAND2005-draft, February 2005.

45. Haill, T.A. et al., “ALEGRA-MHD: Version 4.6,” Sandia National Laboratories,
SAND2004-5997, January 2005.
46. Bindhu, C.V. et al., “Laser Propagation and Energy Absorption by an Argon Spark,” _Journal_
_of Applied Physics,_ 94, 12, p. 7402-7407 (2003).
47. Harilal, S.S., “Spatial and Temporal Evolution of Argon Sparks,” Applied Optics, 43, 19,
July 2004.
48. Harilal, S.S., Personal communication, University of California at San Barbra, September
2006.
49. Olson, C. et al., “Z-Pince IFE Program: Final Report for FY04,” Sandia National
Laboratories, SAND-2005-2742P (2005).
50. Abbot, R.P., “Z-IFE Chamber Design and Modeling,” Lawrence Livermore National
Laboratory, Z-IFE Program Workshop August 2, 2005
51. Bardet, P.M., Abbott, R.P., Campen, C., Franklin, J., Zhao, H., & Peterson, P.F.,
“Experiment Investigation of Z-Pinch IFE Chamber Liquid Structure Response,” University
of California at Berkeley (2006).
52. Peterson, P.F., “Design Methods for Thick-Liquid Protection of Inertial Fusion Chambers,”
Fusion Technology, 39 (2) (2001) 702-710.
53. Pemberton, S., Jantzen, C., Kuhn, J., & Peterson, P.F., “Partial-Pocket Experiments for IFE
Thick-Liquid Pocket Disruption and Clearing,” Fusion Technology, 39 (2001) 726-731.
54. Rao, D.M., “Method of Flow Stabilixation with High Pressure Recovery in Short, Conical
Diffusers,” Aeronautical Journal, 75(725) (1971) 336.
55. Bardet, P.M., Debonnel, C.S., Freeman, J., Fukuda, G., Supiot, B., & Peterson, P.F.,
“Dynamics of Liquid-Protected Fusion Chambers,” Fusion Science and Technology,
47(2005) 626-636.
56. Cooper, P.W., _Explosives Engineering,_ Wiley-Verlach, New York, NY, 1996.
57. Kern, B., Abdel-Khalik, S.I., & Ghiaasiaan, S.M., “Void Fraction Distribution in Two-Phase
(Gas-Liquid) Jets for Z-Pinch IFE Reactor Applications,” Georgia Institute of Technology,
Z-IFE (2006).
58. Anderson, M., Oakley, J., Marriott, E., Gudmundson, J., Sridharan, K., Vigil, V., Rochau, G.,
& Bonazza, R., “Shock Mitigation Studies in Voided Liquids for Fusion Chamber
Protection,” University of Wisconsin- Z-IFE FY06 Final Report, Madison, WI, 2006.
59. Moir, R., “HYLIFE-II: A Molten-Salt Inertial Fusion Energy Power Plant Design-Final
Report,” Fusion Technology, 25, 5-25 (1994).
60. Olson, C. et al., “Development Path for Z-Pinch IFE,” Fusion Science and Technology, 47,
633-640 (2005).
61. Kitagawa, K., Yokoyama, M., & Yasuhara, M., “Attenuation of Shock Waves by Porous
Materials,” 24 [th] International Symposium on Shock Waves Proceedings, Beijing, China,
Paper 2692 (2004).
62. Anderson, M.H., Oakley, J.G., Vigil, V., Rodriquez, S., & Bonazza, R., “The Dynamics of a
Shock Wave and Aluminum Foam Layer Interaction,” 25 [th] International Symposium on
Shock Waves Proceedings, Bangalore, India, Paper 1197 (2005).
63. Anderson, M.H., Puranik, B.P., Oakley, J.G., Brooks, P.W., & Bonazza, R., “Shock
Mitigation Studies of Solid Foams for Z-Pinch Chamber Protection,” report following the ZPinch IFE Workshop, Sandia National Laboratories, Albuquerque, NM, Aug 1-2, 2005.
64. Anderson, M.H., Puranik, B.P., Oakley, J.G., Brooks, P.W., & Bonazza, R., “Shock Tube
Investigation of Hydrodynamic Issues Related to Inertial Confinement Fusion,” Shock
Waves, 10, 5, 377-387 (2000).

65. Gibson, L.J., & Ashby, M.F., “Cellular Solids, Structure & Properties,” Pergamon Press,
Oxford, 1988.
66. Energy Research and Generation, Inc. “Duocell Aluminum Foam Brochure,” 900 Stanford
Ave., Oakland, CA, (510) 658-9758.
67. Heltemes, T.A., Marriott, E.P., Moses, G.A., Peterson, R.R., “Z-Pinch (LiF)2-BeF2 (flibe)
Preliminary Vaporization Estimation Using the BUCKY 1-D Radiations Hydrodynamic
Code,” 21 [st] IEEE/NPSS Symposium on Fusion Energy (SOFE), 26-29 Sept. 2005, Knoxville,
TN.
68. 10 CFR 61.55, Technical Requirements for Land Disposal Facilities, Waste Classification.
69. American Society of Mechanical Engineers, “ASME Boiler and Pressure Vessel Code,” New
York, NY: ASME (2004).
70. Special Metals Corporation, Downloaded from the World Wide Web July3, 2005,

www.specialmetals.com.
71. A.F. Tavassoli, J.-W. Rensman, M. Schirra, K. Shiba, “Materials Design Data for Reduced
Activation Martensitic Steel type F82H”, Fusion Engineering and Design, 2002, Volume 6162, pp 617-628.
72. Zinkle, S.J., Robertson, J.P, and Klueh, R.L., “Thermophysical and Mechanical Properties of
Fe-(8-9)%Cr reduced activation steels,” Fusion Materials 24: Semiannual Progress Report
(1998), 135-43.
73. Pierson, H.O., “Handbook of Carbon, Graphite, Diamond and Fullerenes – Properties,
Processing and Applications,” William Andrew Publishing/Noyes (1993).
74. Papakonstantinou, C.G., Balaguru, P., and R.E. Lyon, “Comparative study of high
temperature composites,” Composites: Part B 32 (2000), 637-49.
75. Mager, T.R., “Thermal Annealing of an Embrittled Reactor Vessel: Feasibility and
Methodology,” Nuclear Engineering and Design, 124, p.43-51 (1990).
76. Reijo, P., & Torronen, K., “On Thermal Annealing of Irradiated PWR Pressure Vessels,”
International Journal of Pressure Vessels and Piping, 75, p. 1075-1095 (1998).
77. Vassilaros, M.G., Mayfield, M.E., & Wichman, K.R., “Annealing of Nuclear Reactor
Pressure Vessels,” Nuclear Engineering and Design, 181, p.61-69 (1998).
78. Reith, M., Dafferner, B., Rohrig, H.D., “Charpy Impact Properties of Low Activation Alloys
for Fusion Applications after neutron Irradiation,” Journal of Nuclear Material, 233-237
(1996) p. 351-355.
79. “Introduction to Fusion Power Plant Materials,” Downloaded from the World Wide Web:

http://www.msm.cam.ac.uk/phasetrans/2006/Irradiated_Steel/Irradiated_Steel.html#SECTION00232000000000000000
80. “Materials for the Plasma-Facing Components of Steady State Stellarators” Down loaded
from the World Wide Web: < http://www-fusion.ciemat.es/SW2005/talks/BoltH_Talk.pdf  81. Irradiation Behavior of Three Candidate Structural Materials for ADS Systems: EM10, T91,
and HT9 (F/M Steels),” Downloaded from the World Wide Web.
<http://www.extremat.org/media/static/Paper%201116%20-%20Lucon1.pdf>
82. Shiba, et al., “Tensile results of low-activation martensitic steel irradiated in HFIR RB-11J
and RB-12J spectrally tailored capsules”, Fusion Materials Semiannual Progress Report
(DOE/ER-0313/28) pp.131-135, June 2000.
83. Depreist, Kendall Russell, Org. 01384, _communication_, July 2006.
84. Zinkle, S.J., Robertson, J.P., Klueh, R.L., “Thermophysical and Mechanical Properties for
Fe-(8-9)%Cr reduced activation steels” Oak Ridge National Laboratory <http://wwwferp.ucsd.edu/LIB/PROPS/FS/FS.html#8>.

85. Hishinuma, A. Kohyama, R.L. Klueh, D.S. Gelles, W. Dietz, K. Ehrlich, “Current status and
future R&D for reduced-activation ferritic/martensitic steels” Journal of Nuclear Materials,
1998, Volume 258-263, pp. 193-204.
86. Kohno, Y., Gelles, O.S., Kohyama, A., Tamura, M., Hamilton, M.L., “Irradiation Response
of F82H, a Reduced Activation Fe-8Cr-2W Martensitic Steel” Fusion Materials Semi-Annual
Progress Reports, 1991, Volume 10, pp. 78-85.
87. Miwa, Y., Jitsukawa, S., Yonekawa, M., “Fatigue properties of F82H irradiated at 523K to
3.8 dpa”, Journal of Nuclear Materials, 2004, Volume 329-333, pp. 1098-1102.
88. Shiba, K., Enoeda, M., Jitsukawa, J., “Reduced Activation Martensitic Steels as a Structural
Material for ITER Test Blanket” Journal of Nuclear Materials, 2004, Volume 329-333, pp.
243-247.
89. Shiba, K., Klueh, R.L., Miwa, Y., Robertson, J.P, Hishinuma, A., “Tensile Behavior of F82H
with and without Spectral Tailoring”, Journal of Nuclear Materials, 2000, Volume 283-287,
pp. 358-361.
90. Shiba, K., Yamanouchi, N., Tohyama, A., “Preliminary Results of the Round-Robin Testing
of F82H”, Fusion Materials Semi-Annual Progress Reports, 1996, Volume 20, pp 190-194.
91. Hirose, T., Tanigawa, H., Ando, M., Kohyama, A., Katoh, Y., Narui, M., “Radiation Effects
on Low Cycle Fatigue Properties of Reduced Activation Ferritic/Martensitic Steels”, Journal
of Nuclear Materials, 2002, Volume 307-311, pp. 304-307.

The image is essentially a blank page containing only a page number (148) at the bottom. There is no extractable content.

###### **DISTRIBUTION**

Wayne Meier (Lawrence Livermore National Laboratory)
Ralph Moir (Lawrence Livermore National Laboratory)
Per F. Peterson (University of California at Berkeley)
Philippe M. Bardet (University of California at Berkeley)
Chris Campen (University of California at Berkeley)
James Franklin (University of California at Berkeley)
Haihua Zhao (University of California at Berkeley)
Gerald Kulcinski (University of Wisconsin)
Mark Anderson (University of Wisconsin)
Jason Oakley (University of Wisconsin)
Ed Marriott (University of Wisconsin)
Jesse Gudmundson (University of Wisconsin)
Kumar Sridharan (University of Wisconsin)
Riccardo Bonazza (University of Wisconsin)
Virginia Vigil (University of Wisconsin)
Mohamed Abdou (University of California at Los Angles)
Lothar Schmitz (University of California at Los Angles)
Alice Ying (University of California at Los Angles)
Tomas Sketchley (University of California at Los Angles)
Yu Tajima (University of California at Los Angles)
Said Abdel-Khalik (Georgia Institute of Technology)
Brain Kern (Georgia Institute of Technology)
M. Ghiaasiaan (Georgia Institute of Technology)

1 MS0123 D. Chavez, LDRD Office 01011
1 MS0513 Rick Stulen 01000
1 MS0701 Peter Davies 06700
1 MS0719 Paul McConnell 06793
1 MS0724 Les Shephard 06000
1 MS0736 Ron Lipinski 06771
1 MS0736 JD Smith 06772
1 MS0748 Ben Cipiti 06763
1 MS0748 Virginia Cleary 06761
1 MS0748 Jason Cook 06763
1 MS0748 Sam Durbin 06763
1 MS0748 Cathy Farnum 06763
1 MS0748 Rodney Keith 06763
1 MS0748 Charlie Morrow 06763
1 MS0748 Gary Rochau 06763
1 MS0748 Sal Rodriguez 06763
1 MS0748 Matt Turgeon 06764
1 MS0748 Mike Young 06763
1 MS0771 Dennis Berry 06800
2 MS0899 Technical Library 04536
1 MS1190 Keith Matzen 01600
1 MS1190 Craig Olson 01600
2 MS9018 Central Technical Files 08944

![](images/page_148_table_0.png)

|  |  |  |
| --- | --- | --- |
| 2 2 |  | Said Brain M. |
| MS0748 MS0748 MS0748 MS0748 MS0748 MS0748 MS0771 MS0899 MS1190 MS1190 MS9018 | MS0736 MS0736 MS0748 MS0748 MS0748 MS0748 MS0748 | Abdel-Khalik Kern (Georgia Ghiaasiaan MS0123 MS0513 MS0701 MS0719 MS0724 |
| Rodney Keith Charlie Morrow Gary Rochau Sal Rodriguez Matt Turgeon Mike Young Dennis Berry Technical Library Keith Matzen Craig Olson Central Technical | Ron Lipinski JD Smith Ben Cipiti Virginia Cleary Jason Cook Sam Durbin Cathy Farnum | (Georgia Institute Institute of (Georgia Institute of D. Chavez, Rick Stulen Peter Davies Paul McConnell Les Shephard |
| Files |  | of Technology) Technology) Technology) LDRD Office |
|  | 06771 06772 06763 06761 06763 06763 06763 06763 06763 06763 06763 06764 06763 06800 04536 01600 01600 08944 | 01011 01000 06700 06793 06000 |
