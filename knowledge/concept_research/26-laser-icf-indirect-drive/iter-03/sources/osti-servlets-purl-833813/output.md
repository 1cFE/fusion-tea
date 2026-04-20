---
source: "https://www.osti.gov/servlets/purl/833813"
source_type: "url"
extracted_at: "2026-04-20T18:30:41.630750+00:00"
content_hash_sha256: "1e3647f7d44098076238d75f520c44b19e316d523c92177d75fa4c9f8a05612f"
backend: "pdf_pipeline"
---

WJSA-92-01
DOE/ER/54100-1

# OSIRIS and SOMBRERO Inertial Fusion Power Plant Designs

Volume 1
Executive Summary and Overview

Final Report
March 1992

## DISCLAIMER

This report was prepared as an account of work sponsored by an agency of the United States Government. Neither the United States Government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

## DISCLAIMER

Portions of this document may be illegible in electronic image products. Images are produced from the best available original document.

WJSA-92-01
DOE/ER/54100-1

# OSIRIS and SOMBRERO Inertial Confinement Fusion Power Plant Designs

## Volume 1 Executive Summary and Overview

**W. J. Schafer Associates**
Wayne R. Meier, Robert L. Bieri, Michael J. Monsler,
Charles D. Hendricks, Paul Laybourne, Keith R. Shillito

**Bechtel**
Sunil K. Ghose, Lenard M. Goldman, Kim D. Auclair, Chan Y. Pang

**General Atomics**
Robert F. Bourque, Larry D. Stewart, Edward E. Bowles, Edward L. Hubbard

**Textron Defense Systems**
Chas. W. von Rosenberg, Jr., Malcolm W. McGeoch

**University of Wisconsin**
Igor N. Sviatoslavsky, Robert R. Peterson, Mohamed E. Sawan, Hesham Y. Khater,
Layton J. Wittenberg, Gerry L. Kulcinski, Gregory A. Moses, ElSayed A. Mogahed,
Joseph J. MacFarlane, Sean Rutledge

**Accelerator Consultants**
Stanley Humphries, Jr.

**TSI Research**
Edward T. Cheng

March 1992

### Disclaimer

This report was prepared as an account of work sponsored by an agency of the United States Government. Neither the United States Government nor any agency thereof, nor any of their employees, make any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product or process disclosed, or represents that its use would not infringe on privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise, does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof. The views and opinions of the authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

# Acknowledgments

The authors would like to acknowledge the help in the form of briefings and discussions with individuals in the Inertial Confinement Fusion Programs at the Laboratory for Laser Energetics, Lawrence Livermore National Laboratory, Los Alamos National Laboratory, and the Navy Research Laboratory, and individuals in the Heavy Ion Fusion Program at Lawrence Berkeley Laboratory. We also thank the members of the Oversight Committee for assembling the Study Guidelines and for providing feedback at our progress review meetings. We thank the secretaries at our institutions for their assistance in preparing this report with special thanks to Barbara Lane at W.J. Schafer Associates for editing the final report. Finally, we thank the Department of Energy, Office of Fusion Energy for supporting this study under contract No. DE-AC02-90ER54100.

|**1.0**|**INTRODUCTION**...................................................................................................|**1**|
|---|---|---|
|**1.1**|BACKGROUND......................................................................................................|**1**|
|**1.2**|ORGANIZATION**OF**THE OVERVIEW...............................................................|**1**|
|**2.0**|**OSIRIS HIB-DRIVEN POWER PLANT**.............................................................|**3**|
|**2.1**|SUMMARY OF OSIRIS PLANT PARAMETERS.................................................|3|
|**2.2**|OSIRISCHAMBER DESIGN..................................................................................|**3**|
|**2.3**|OSIRIS POWER CONVERSION**_`AND`_**PLANT FACILITIES..............................|**7**|
|**2.4**|HEAVY-ION DRIVER DESIGN.............................................................................|8|
|**3.0**|**SOMBRERO LASER-DRIVEN POWER PLANT**.............................................|**17**|
|**3.1**|SUMMARY OF SOMBRERO PLANT PARAMETERS........................................|**17**|
|**3.2**|SOMBRERO CHAMBER DESIGN........................................................................|**17**|
|**3.3**|SOMBRERO POWER CONVERSION_AND_PLANT FACILlTIES.....................|20|
|**3.4**|KrF DRIVER DESIGN.............................................................................................|**24**|
|**4.0**|**TARGET SYSTEMS**..............................................................................................|**32**|
|**4.1**|TARGET PRODUCTION........................................................................................|**32**|
|**4.2**|**`TARGET`**INJECTION. TRACKING.**_`AND`_**POINTING........................................|**39**|
|**4.3**|TARGET HEATING DURING INJECTION..........................................................|**43**|
|**5.0**|**ENVIRONMENTAL AND SAFETY ASSESSMENT**........................................|**45**|
|**5.1**|INTRODUCTION**i**...................................................................................................|**45**|
|**5.2**|**`SAFETY`**DESIGN GOALS......................................................................................|**45**|
|**5.3**|RESULTS.................................................................................................................|**46**|
|**6.0**|**RELIABILITY. AVAILABILITY.**&**MAINTAINABILITY ASSESSMENT**|**48**|
|**6.1**|INTRODUCTION....................................................................................................|**48**|
|**6.2**|AVAILABILITY ASSESSMENT............................................................................|**48**|
|**6.3**|MAINTAINABILITY OFTHEOSIRISPLANT....................................................|50|
|**6.4**|MAINTAINABILITY OF THE SOMBRERO PLANT...........................................|**52**|

|**7.0**|**TECHNOLOGY ASSESSMENTS**........................................................................|**54**|
|---|---|---|
|**7.1**|INTRODUCTION....................................................................................................|**54**|
|**7.2**|SUMMARYOFDEVELOPMENT PRIORITIES FOR OSIRIS............................|**54**|
|**7.3**|SUMMARYOFDEVELOPMENT**`PRIORITIES`**FORSOMBRERO...................**56**||
|**7.3**|GENERIC`IFE`**`ISSUES`**............................................................................................|**567**|
|**8.0**|**ECONOMIC ASSESSMENT**................................................................................|**58**|
|**8.1**|INTRODUCTION....................................................................................................|**58**|
|**8.2**|RESULTS FOR REFERENCE DESIGNS...............................................................|**58**|
|**8.3**|RESULTSOFPARAMETRIC STUDIES**`FOR`**OSIRIS_AND_SOMBRERO........**58**||
|**8.4**|CONCLUSIONS.......................................................................................................|**61**|
|**9.0**|**COMPARISONOFOSIRIS AND SOMBRERO DESIGNS**.............................|**62**|
|**9.1**|INTRODUCTION....................................................................................................|**62**|
|**9.2**|**DRIVERS**..................................................................................................................|**62**|
|**9.3**|**`TARGETS`**.................................................................................................................|**62**|
|**9.4**|CHAMBER DESIGNS.............................................................................................|62|
|**9.5**|POWER CONVERSION SYSTEMS.......................................................................|**_`64`_**|
|**9.6**|RESULTSOFASSESSMENT STUDIES...............................................................|**64**|
|**10.0**|**CONCLUSIONS AND RECOMMENDATIONS**................................................|**65**|
|**10.1**|INTRODUCTION....................................................................................................|**65**|
|**10.2**|OSIRIS POWER PLANT.........................................................................................|**65**|
|**10.3**|SOMBREROPOWER PLANT................................................................................|**68**|
|**10.4**|TARGETSYSTEMS................................................................................................|**71**|
|**10.5**|ENVIRONMENTAL_AND_SAFETY ASSESSMENT............................................|**72**|
|**10.6**|RELIABILITY. AVAILABILITY.**_`AND`_**MAINTAINABILITY...........................|**72**|
|**10.7**|ECONOMIC**ASSESSMENTS**.................................................................................|**73**|
|**11.0**|**REFERENCES**........................................................................................................|**74**|

|5.8|FUELREPROCESSING FACILITIES....................................................................|5-33|
|---|---|---|
|5.9|NUCLEAR GRADE COMPONENTS.....................................................................|5-33|
|5.10|COMPARISON OF SOMBRERO**_`AND`_**OSIRIS....................................................|**5-35**|
|5.11|REFERENCES FOR CHAPTER**_5_**...........................................................................|**`5-36`**|
|**6.0**|**RELIABILITY. AVAILABILITY. AND MAINTAINABILITY ASSESSMENT**||
|6.1|INTRODUCTION....................................................................................................|6-1|
|6.2|AVAILABILITY ASSESSMENT............................................................................|6-1|
|6.3|MAINTAINABILITYOFTHE OSIRIS PLANT...................................................|6-5|
|6.4|MAINTAINABILITY OF THE SOMBRERO PLANT...........................................|6-9|
|6.5|REMOTE HANDLING CAPABILITY&UTILIZATION CONSIDERATIONS|.6-10|
|6.6|REFERENCES FOR CHAPTER6...........................................................................|6-14|
|**7.0**|**TECHNOLOGY ASSESSMENTS**||
|7.1|APPROACH AND METHODOLOGY....................................................................|7-1|
|7.2|OSIRISISSUESANDDEVELOPMENT NEEDS..................................................|7-2|
|7.3|TECHNOLOGYASSESSMENT**`RATINGS`**FOROSIRIS....................................|**_7-9_**|
|7.4|SUMMARYOFDEVELOPMENT PRIORITIES FOROSIRIS............................|7-19|
|7.5|SOMBRERO ISSUES_`AND`_DEVELOPMENT NEEDS........................................|7-21|
|7.6|TECHNOLOGY ASSESSMENT RATINGS FOR SOMBRERO...........................|7-28|
|7.7|SUMMARYOFDEVELOPMENT PRIORITIES FOR SOMBRERO...................7-37||
|7.8|GENERIC IFE ISSUES............................................................................................|7-39|
|7.9|TECHNOLOGY ASSESSMENT**`RATINGS`**FOR GENERIC ISSUES.................7-43||
|7.10|SUMMARY..............................................................................................................|7-46|
|7.11|REFERENCES FOR CHAPTER7...........................................................................|7-46|
|**8.0**|**ECONOMIC ASSESSMENT**||
|8.1|INTRODUCTION....................................................................................................|8-1|
|8.2|COST OF ELECTRICITY........................................................................................|8-2|
|8.3|CALCULATING PLANT OPERATING PARAMETERS.....................................|8-4|
|8.4|COST MODELING FOROSIRIS............................................................................|8-12|
|8.5|COST MODELING FOR SOMBRERO..................................................................|8-25|
|8.6|COMPARISONOF**`OSIRIS`**_`AND`_SOMBRERO....................................................|8-42|
|8.7|SUMMARY..............................................................................................................|8-44|
|8.8|REFERENCES FOR CHAPTER8...........................................................................|8-45|

|**_9.0_**|**`COMPARISON`OFOSIRISANDSOMBRERODESIGNS**||
|---|---|---|
|**9.1**|INTRODUCTION....................................................................................................|**9-1**|
|**9.2**|CHAMBER**_`AND`_**VACUUM SYSTEMS...............................................................|**9-1**|
|**9.3**|POWER CONVERSION SYSTEMS.......................................................................|**9-5**|
|**9.4**|BUILDING VOLUME COMPARISON..................................................................|**9-6**|
|**9.5**|DRIVER SYSTEMS.................................................................................................|**9-7**|
|**9.6**|TARGET SYSTEMS................................................................................................|**9-8**|
|**9.7**|OPERATION**_`AND`_**MAINTENANCE COMPARISON.........................................|**9-9**|
|**9.8**|ENVIRONMENTALAND**_SAFETY_**COMPARISON..........................................|**9-10**|
|**9.9**|ECONOMIC COMPARISON..................................................................................|**9-11**|
|**9.10**|REFERENCES FOR CHAPTER**9**...........................................................................|**9-12**|

|**9.10**|REFERENCES FOR CHAPTER**9**...........................................................................|**9-12**|
|---|---|---|
|**10.0**|**CONCLUSIONS AND RECOMMENDATIONS**||
|**10.1**|INTRODUCTION....................................................................................................|**10-1**|
|**10.2**|OSIRISPOWER PLANT.........................................................................................|**10-1**|
|**10.3**|SOMBRERO POWER PLANT................................................................................|**10-4**|
|**10.4**|TARGET SYSTEMS................................................................................................|**10-7**|
|**10.5**|ENVIRONMENTAL**_`AND`S A F E R_**ASSESSMENT............................................|**10-8**|
|**10.6**|RELIABILITY. AVAILABILITY.**_`AND`_**MAINTAINABILITY...........................|**10-9**|
|**10.7**|ECONOMIC ASSESSMENT...................................................................................|**10-9**|

# Executive Summary

## EXECUTIVE SUMMARY

### INTRODUCTION

Conceptual designs and assessments have been completed for two inertial fusion energy (IFE) electric power plants. The detailed designs and results of the assessment studies are presented in this report. Osiris is a heavy-ion-beam (HIB) driven power plant, and SOMBRERO is a Krypton-Fluoride (KrF) laser-driven power plant. Both plants are sized for a net electric power of 1000 MWe. Key design features and operating parameters are given in Table I.

### OSIRIS POWER PLANT

#### Osiris Chamber Design

- The Osiris chamber features a flexible, porous carbon fabric first wall and blanket that contains the molten salt, Flibe, which serves as the tritium breeding material and primary coolant. The first wall radius at the nearest point to the target is 3.5 m.

- A thin layer of Flibe coats the first wall to protect it from x-ray and debris damage.

- A spray of Flibe at the cold-leg temperature (500°C) is injected at the bottom of the chamber to condense the Flibe that is vaporized with each pulse.

#### HIB Driver Design

- The HIB driver uses linear induction accelerator technology. Twelve beams of 3.8 GeV Xe$^{+1}$ ions deliver a total of 5 MJ to an indirect drive target at a pulse repetition rate of 4.6 Hz.

- The driver is designed to carry the maximum transportable current at every point along the accelerator in order to minimize cost.

- The driver efficiency is 28%, and the power consumption is 82 MWe.

- The design is conservative in that it does not use beam combination, beam separation, or recirculation.

- High performance Nb₃Sn superconductors in the quadrupole focusing magnets improve performance and reduce cost.

**Osiris Balance of Plant**

- The reactor building is quite compact and features a movable shielding wall for access to the maintenance building.

- The power conversion system uses a double reheat rankine power cycle with a gross electric conversion efficiency of 45%. After accounting for driver and auxiliary power consumption, the net efficiency of the power plant is 40%.

## SOMBRERO POWER PLANT

### SOMBRERO Chamber Design

- SOMBRERO features a carbon/carbon first wall and blanket structure with a granular Li₂O breeding blanket. The Li₂O granules flow through the blanket region of the chamber and serve as the primary coolant.

- The first wall is protected from x-ray and debris damage by xenon gas at 0.5 torr.

- Low pressure He is used to remove tritium from the breeding blanket and also to transport the Li₂O granules to and from the intermediate heat exchangers.

### KrF Laser Design

- The KrF laser uses e-beam pumped amplifiers and angular multiplexing for pulse compression. Sixty beams deliver a total of 3.4 MJ to a direct drive target at 6.7 Hz.

- The non-intercepting e-beam cathode technology promises long-life operation and improves the system efficiency.

- The laser design achieves an overall system efficiency of 7.5% and has a total power consumption of 304 MWe.

## Power Conversion and BOP

- SOMBRERO requires a large (110 m diameter) reactor building to accommodate the final focusing optics for the laser. The entire building is a vacuum structure filled with 0.5 torr of xenon used for first wall protection.

- The sensitive dielectric optics are protected from neutron damage by the use of grazing incidence metal mirrors (GIMMs). While the lifetime of the dielectric optics is very uncertain, present assumptions indicate that they could last for the life of the power plant. The life of the GIMMs depends on the degree to which radiation damage can be annealed by heating.

- SOMBRERO uses the same intermediate coolant loop and steam power cycle as Osiris. The gross efficiency is 47% and includes a credit for using waste heat from the laser in the feedwater heaters. After accounting for laser and auxiliary power consumption, the net plant efficiency is 35%.

## TARGET SYSTEMS

### Target Production Facility

- The target production facility design uses controlled microencapsulation for shell production, cryogenic injection fill for fuel loading, and a combination of cold-gas jets and pulsed laser heating to establish a uniform fuel layer.

- The design is 100% redundant to improve reliability and minimize the need to store extra targets and the associated tritium inventory.

- The DT-fill and layering techniques minimize production time and thus minimize tritium inventory.

- The total estimated tritium inventory of the target factory is only 300 g.

**Target Injection, Tracking, and Beam Pointing**

- A gas gun injector accelerates targets at 130 g's over a distance of 9 m to a final velocity of 150 m/s.

- A laser Doppler interferometer and laser diode tracking stations measure the target trajectory and provide pointing information to the drivers.

- Active beam pointing is proposed for both the HIB and KrF-laser drivers.

## ENVIRONMENTAL AND SAFETY ASPECTS

- Only low activation materials are used in the first walls, blankets, breeding materials, and chamber structures of both the Osiris and SOMBRERO designs.

- Both power plants achieve a Level of Safety Assurance of 1.

- Structures and shielding for both designs qualify for Class A shallow land burial. Osiris breeding material qualifies for Class A while SOMBRERO breeding material qualifies for Class C shallow land burial.

- Nuclear grade construction is not needed for either design.

## MAINTAINABILITY

- The first wall and blanket structure for Osiris are removed as a single unit by first draining the blanket of Flibe and then lifting the internal components out the vacuum vessel with an overhead crane.

- The SOMBRERO chamber is constructed of 12 first-wall / blanket units. To replace a segment, it is lowered to a transport carriage and moved to the maintenance building.

## TECHNOLOGY DEVELOPMENT NEEDS

- To realize the attractive features of these designs, technology development is needed in several areas.

- Driver technology should be given the highest priority in both cases. Beam delivery systems (heavy-ion-beam transport and final optics for lasers) are important research areas.

- Economical automated target production techniques are required for both designs.

- For Osiris, technology development and experiments are needed to prove the feasibility of the operation of the first wall protection scheme and chamber operation in a rep-rated mode.

- For SOMBRERO, the development of large-structures made of low activation material is needed.

## ECONOMICS

- The estimated constant dollar cost of electricity (COE) for Osiris is 5.6 ¢/kWh, while the COE for SOMBRERO is 6.7 ¢/kWh. Both COEs compare favorably with reported COEs for magnetic fusion energy reactors.

## CONCLUSIONS

- The conceptual designs developed in this study show the potential promise of IFE for electric power production. We have developed technically credibly concepts with environmental, safety, and economic characteristics that are every bit as attractive as magnetic fusion energy reactors designs. Realizing IFE potential will require continued research and development in the areas of target physics, driver technologies, heavy ion beam transport, laser optics, chamber phenomenology, low activation materials, and automated target production.

||**Osiris**|**SOMBRERO**|
|---|---|---|
|**Driver**|||
|Driver Energy (MJ)|5.0|3.4|
|Rep-Rate**`(Hz)`**|4.6|6.7|
|Driver Efficiency(%)|28.2|**7.5**|
|**Target**|||
|Type|Indirect Drive|Direct Drive|
|Target Gain|86.5|118|
|Yield(MJ)|432|400|
|**Chamber Design**|||
|First Wall Material|Woven Graphite Fabric|4-D C/C Composite|
|X-ray and Debris Protection|Liquid Flibe|3.25 torr-m of Xe|
|First Wall Radius,m|3.5|6.5|
|Estimated First Wall Life (fpy)|1.8|**_5_**|
|Breeding Material|Molten Flibe|**Liz0**Granules|
|Tritium Breeding Ratio|**1.24**|1.25|
|**Power Conversion System**|||
|Primary Coolant|Flibe|He**`w/`Li20**granules|
|Intermediate Coolant|Lead|Lead|
|Secondary Coolant|Water/Steam|Water/Steam|
|Power Conversion Eff.(%)|45|47|
|**Power Balance**|||
|Fusion Power(MW)|1987|2677|
|Total Thermal Power (MWt)|2504|2891|
|Gross Electric Power (MWe)|1127|1359|
|Driver Power (MWe)|82|304|
|Auxiliary Power (MWe)|45|**_55_**|
|Net Electric Power (MWe)|1000|1000|
|Net Plant Efficiency(%)|40|35|
|**Environmental**&**Safety**|||
|Waste Disposal Ratings|**A**|A & C|
|Level of Safety Assurance|1|1|
|**Economics**|||
|Cost of Electricity (#/kWh)|5.6|6.7|

# Overview

## CONTENTS

**1.0 INTRODUCTION**
- 1.1 BACKGROUND
- 1.2 ORGANIZATION OF THE OVERVIEW

**2.0 OSIRIS HIB-DRIVEN POWER PLANT**
- 2.1 SUMMARY OF OSIRIS PLANT PARAMETERS
- 2.2 OSIRIS CHAMBER DESIGN
- 2.3 OSIRIS POWER CONVERSION AND PLANT FACILITIES
- 2.4 HEAVY-ION DRIVER DESIGN

**3.0 SOMBRERO LASER-DRIVEN POWER PLANT**
- 3.1 SUMMARY OF SOMBRERO PLANT PARAMETERS
- 3.2 SOMBRERO CHAMBER DESIGN
- 3.3 SOMBRERO POWER CONVERSION AND PLANT FACILITIES
- 3.4 KrF DRIVER DESIGN

**4.0 TARGET SYSTEMS**
- 4.1 TARGET PRODUCTION
- 4.2 TARGET INJECTION, TRACKING, AND POINTING
- 4.3 TARGET HEATING DURING INJECTION

**5.0 ENVIRONMENTAL AND SAFETY ASSESSMENT**
- 5.1 INTRODUCTION
- 5.2 SAFETY DESIGN GOALS
- 5.3 RESULTS

**6.0 RELIABILITY, AVAILABILITY, & MAINTAINABILITY ASSESSMENT**
- 6.1 INTRODUCTION
- 6.2 AVAILABILITY ASSESSMENT
- 6.3 MAINTAINABILITY OF THE OSIRIS PLANT
- 6.4 MAINTAINABILITY OF THE SOMBRERO PLANT

**7.0 TECHNOLOGY ASSESSMENTS**
- 7.1 INTRODUCTION
- 7.2 SUMMARY OF DEVELOPMENT PRIORITIES FOR OSIRIS
- 7.3 SUMMARY OF DEVELOPMENT PRIORITIES FOR SOMBRERO
- 7.4 GENERIC ISSUES

**8.0 ECONOMIC ASSESSMENT**
- 8.1 INTRODUCTION
- 8.2 RESULTS FOR REFERENCE DESIGNS
- 8.3 RESULTS OF PARAMETRIC STUDIES FOR OSIRIS AND SOMBRERO
- 8.4 CONCLUSIONS

**9.0 COMPARISON OF OSIRIS AND SOMBRERO DESIGNS**
- 9.1 INTRODUCTION
- 9.2 DRIVERS
- 9.3 TARGETS
- 9.4 CHAMBER DESIGNS
- 9.5 POWER CONVERSION SYSTEMS
- 9.6 RESULTS OF ASSESSMENT STUDIES

**10.0 CONCLUSIONS AND RECOMMENDATIONS**
- 10.1 INTRODUCTION
- 10.2 OSIRIS POWER PLANT
- 10.3 SOMBRERO POWER PLANT
- 10.4 TARGET SYSTEMS
- 10.5 ENVIRONMENTAL AND SAFETY ASSESSMENT
- 10.6 RELIABILITY, AVAILABILITY, AND MAINTAINABILITY
- 10.7 ECONOMIC ASSESSMENT

**11.0 REFERENCES**

# OVERVIEW

## 1.0 INTRODUCTION

### 1.1 BACKGROUND

The Inertial Fusion Energy (IFE) Reactor Design Studies were sponsored by the Department of Energy's Office of Fusion Energy. The results of the study conducted by the W. J. Schafer Associates (WJSA) team, which consisted of Bechtel, General Atomics (GA), Textron Defense Systems, and the University of Wisconsin, are reported here.

The primary objective of the IFE Reactor Design Studies was to provide the Department of Energy with an evaluation of the potential of inertial fusion for electric power production.<sup>1</sup> Conceptual designs were completed for two IFE electric power plants, one using an induction linac heavy ion beam (HIB) driver and the other using a Krypton Fluoride (KrF) laser driver. The two designs are the HIB-driven Osiris reactor and the KrF laser-driven SOMBRERO reactor. (SOMBRERO is an acronym for SOlid Moving BREder Reactor.)

These studies included the conceptual design and analysis of all aspects of the IFE power plants: the chambers, heat transport and power conversion systems, other balance of plant facilities, target systems (including the target production, injection, and tracking systems), and the two drivers. After the two point designs were developed, they were assessed in terms of their 1) environmental and safety aspects; 2) reliability, availability, and maintainability; 3) technical issues and technology development requirements; and 4) economics. Finally, we compared the design features and the results of the assessments for the two designs.

### 1.2 ORGANIZATION OF THE OVERVIEW

The main sections of the Overview correspond to the chapters of Volume 2 - Designs, Assessments, and Comparisons. Therefore, to get more detailed information on the topics described in the Overview, the reader is referred to the corresponding chapters in Volume 2.

**Description of the Designs.** Sections 2 to 4 contain brief descriptions of the designs. Section 2 is devoted to the Osiris HIB-driven power plant, Section 3 provides a description of the SOMBRERO laser-driven power plant, and Section 4 deals with the target systems for both plants.

**Assessment of the Designs.** Sections 5 to 8 are assessments of the designs. Section 5 covers the environmental and safety assessments for SOMBRERO and Osiris, Section 6 contains the reliability, availability, and maintainability (RAM) assessments, Section 7 summarizes the

technology development needs and priorities, and Section 8 summarizes the results of our economic assessment of the two designs.

**Comparison of the Designs.** Section 9 gives some of the key comparisons between the two designs.

**Conclusions and Recommendations.** Section 10 reproduces Chapter 10 from Volume 2 in its entirety.

## 2.0 OSIRIS HIB-DRIVEN POWER PLANT

### 2.1 SUMMARY OF OSIRIS PLANT PARAMETERS

Osiris is a 1000 MWe, HIB-driven power plant design. The Osiris Chamber is of the thick liquid-wall family, a descendent of HYLIFE,² HIBALL,³ Pulse*Star,⁴ and HYLIFE-II.⁵ The Osiris chamber design features a porous carbon fabric blanket that is filled with the molten salt Flibe (2LiF-BeF₂). A key feature of Osiris is the use of low activation ceramics in a configuration in which brittleness and leak-tightness are not issues. A thin layer of liquid Flibe coats the carbon fabric first wall to protect it from x-ray and debris damage. Part of this protective layer is vaporized with each pulse. The vaporized Flibe condenses in a spray at the bottom of the chamber. Flibe circulates through the blanket and serves as the primary coolant and tritium breeding material. The blanket support structures and vacuum vessel are made of low activation carbon/carbon composites. Liquid lead is used in the intermediate loop to transfer heat to a steam generator and a double reheat steam power cycle.

The heavy ion driver uses singly-charged xenon ions. The design approach is conservative in that it does not use beam combination, separation, or recirculation. The design maximizes component standardization. It uses a propagation mode in the accelerator with constant beam radius, high-performance Nb₃Sn quadrupoles with constant strength and length, and a single quadrupole array configuration. There are only two inductor cell designs, one each for low and high energy. Illumination of the target is double-sided with six beams from each side.

The key plant operating parameters are listed in Table 2.1.

### 2.2 OSIRIS CHAMBER DESIGN

The Osiris chamber is shown in Fig. 2.1, and the key chamber design parameters are given in Table 2.2. The first wall and blanket are made of a flexible, woven carbon fabric that is stitched together much like a tent. To minimize stress on the fabric from the hydrostatic and pressure head of the Flibe, the fabric blanket is constructed like an air mattress, as shown in Fig. 2.2. Flibe enters the top of the chamber at 500°C and flows down the 5-cm-thick flow channel behind the first wall at a maximum velocity of 5 m/s. A small fraction of the Flibe flows through the porous first wall to provide a protective liquid layer. The fabric weave is adjusted to control the flow rate through the first wall. The high flow rate in the first wall channel limits the temperature rise of the Flibe near the first wall. Therefore, the Flibe that weeps though the fabric to coat the

|Driver Energy(MJ)|5.0|
|---|---|
|Target**`Gain`**|86.5|
|Target Yield(MJ)|432|
|Rep rate (Hz)|4.6|
|Fusion Power_(MW)_|1987|
|Energy Multiplication|1.26|
|TotalThermal Power_( M W )_|2504|
|Power Conversion Efficiency(%)|**45**|
|Gross Electrical Power (MWe)|1127|
|Driver Efficiency(%)|28|
|Driver Power( W e )|82|
|Auxiliary Power ( W e )|**45**|
|Net Electric Power W e )|1000|
|Tritium**Breeding**Ratio|**1.24**|

[Figure 2.1: Osiris chamber design.]

[Figure 2.2: Cross section of the carbon fabric blanket.]

The figure shows a cross section with labeled dimensions: 5 cm First Wall Coolant Channel, 55 cm Blanket Coolant Channel, 0.5 cm Cloth, and Stitch.

|First Wall Radius at Midplane(m)|3.5|
|---|---|
|Flibe Vaporized per Shot (kg)|4.2|
|Peak Pressure on First Wall (GPa)|37|
|Impulse on First Wall (Pa-s)|90|
|Blanket Thickness (m)|0.7|
|Total Thermal Power_(MW)_|2504|
|Surface Power_(MW)_|596|
|Blanket Power_(MW)_|1908|
|Flibe Inlet Temperature("C)|500|
|Flibe Outlet Temperature**`("C)`**|650|
|Spray Flow Rate**(kg/s)**|2265|
|Blanket Flow Rate**(kg/s)**|4598|
|**`Max.`**First Wall Channel Velocity_( d s )_|5|
|HibeUpflow Average Velocity_( d s )_|**0.2**|
|Spray Velocity_( d s )_|46|
|Spray Manifold Pressure (MPa)|2.1|
|Spray Ideal Pumping Power_(MW)_|3|
|Total Flibe Mass in Chamber**(kg)**|456,000|
|Total Supported Mass (kg)|274,000|
|Main Support Hanger Diameter(m)|0.1|
|Number of Hangers|24|
|Hanger Tensile Stress (MPa)|14|
|Total Flibe Inventory (kg)|940,000|

not significantly increase the down-time of the power plant. The entire fabric assembly, drained of Flibe, is lifted out the top and replaced with a new assembly.

The vacuum vessel for Osiris is constructed of a low-activation carbon/carbon composite and is at a radius of ~6.5 m. The Flibe blanket effectively reduces the radiation damage and helium production rates to the composite vacuum vessel wall to 0.2 dpa/fpy and 10 appm/fpy, respectively. This component is, therefore, expected to last the full 30 year life of the plant.

## 2.3 OSIRIS POWER CONVERSION AND PLANT FACILITIES

### 2.3.1 Heat Transport System

The primary coolant for Osiris is liquid Flibe. Flibe enters the chamber at 500°C and exits at 650°C. The primary loop consists of two coolant circuits including one intermediate heat exchanger (IHX) in each circuit. Two circuits are used to keep the size of the IHXs from getting too large.

An intermediate coolant loop is used to isolate the primary coolant, which will contain radioactive elements, from the steam cycle. The intermediate loop consists of two circuits including one steam generator in each circuit. Liquid lead, operating between 400 and 600°C, is the intermediate coolant. It offers a safety advantage over sodium, which was considered as a possible alternative. While modest technology extrapolation is needed for the steam generators, their size appears to be reasonable.

To achieve a high efficiency power conversion, a high pressure/high temperature steam cycle is used. The steam pressure and temperature conditions chosen are consistent with the intermediate coolant temperature. These conditions also represent the state-of-the-art steam conditions used for fossil-fired steam power plants. A double-reheat steam cycle is used with the peak steam pressure and temperature of 24.2 MPa (3500 psig) and 538°C (1000°F), respectively. These conditions provide a power conversion efficiency of 45%.

There are two steam generators, and each is sized to handle half of the plant thermal output. Thus the thermal rating of each steam generator is 1250 MWt. To accommodate the double reheat feature of the power cycle, each steam generator is made up of three separate vessels: superheater, first reheater, and second reheater. These steam generator vessels are supplied with liquid lead from the IHXs.

The reactor plant is provided with a turbine-generator capable of generating 1127 MWe gross electrical power. The turbine-generator is a state-of-the-art design consisting of one high-pressure section, one intermediate-pressure section, and two low-pressure sections arranged in a cross-compound configuration.

### 2.3.2 Reactor Building

The reactor building provides housing for the reactor and shielding of the public from fusion neutrons. In addition, the building also accommodates remote maintenance of the reactor. The reactor building size is dictated by the maintenance handling requirements for the vacuum vessel cover and reactor internals. The conceptual arrangement of the building is shown in Figs. 2.3 and 2.4. The reactor is located at the center of the reactor hall. The IHXs are located in a separate hall so that the area can be accessed for limited periods during normal power operation; the reactor hall is provided with requisite shielding for this purpose. The nearest shielding wall is 10 m from the center of the chamber, and the shield thickness is 3.2 m.

Another feature of the reactor building is that there is no direct piping penetration between the reactor and IHX halls. The primary coolant piping is routed via an underground piping tunnel; there is no direct neutron path from the reactor hall to the IHX hall. The shield wall of the IHX hall is 1 m thick to allow unlimited access to the steam generator building.

## 2.4 HEAVY-ION DRIVER DESIGN

### 2.4.1 Summary of Results

The base 5-MJ heavy-ion induction driver design uses conservative design assumptions and has an efficiency of 28% and a direct cost of only $120/J. Combining the driver efficiency with an estimated target gain of 86.5 gives a recirculating power fraction for a 1000 MWe plant of only ~7%. We created a high-performance, low-cost design by

- using an original design for compact arrays of high-performance, Nb$_3$Sn quadrupoles that leads to small sizes and costs for the inductor cells as well as for the focusing arrays, and
- conducting a parametric search over a wide range of possible driver parameters to choose parameters that give an attractive design.

We use minimal extrapolation from existing accelerator technology and physics to create highly credible driver performance. We do not use any bends in the accelerator, beam combination, or beam separation. Although driver designs with bends, such as recirculating induction accelerators, offer the potential for cost savings by bending the beams in a circle and reducing the number of required driver elements, present performance uncertainties are large for high-current circular accelerators. Linear driver costs and projected target gains could be improved by combining beams early in the driver and separating them before final focusing; again we avoid performance uncertainties by not using beam combination or separation.

[Figure 2.3: Elevation view of Osiris reactor and steam generator buildings.]

[Figure 2.4: Plan view of Osiris reactor and steam generator buildings.]

![](images/tmpnzkalo9i.pdf-0032-00.png)

![](images/tmpnzkalo9i.pdf-0032-02.png)

![](images/tmpnzkalo9i.pdf-0034-00.png)

|Energy(MJ)|**_5_**|
|---|---|
|IonMass( m u )|131|
|Charge State|1|
|Superconductor|NbgSn|
|NumberofBeams|12|
|B-max at**S/C**(T)|10|
|Driver Efficiency(%)|28.2|
|Beam Voltage||
|Initial**_(W)_**|3|
|Final**(GV)**|3.83|
|Current per Beam||
|Initial**(A)**|3.5|
|Final(kA)|1.09|
|Pulse Length||
|Initial(rns)|34|
|Final (ns)|100|
|Accelerator Length||
|Low Energy (m)|359|
|Pulse Matching (m)|33|
|High Energy(km)|4.4|
|Total Length(km)|4.8|

|FinalFocusHalf-angle (mrad)|33|
|---|---|
|Spot Radius (mm)|2.3|
|Ion Range (g/cm2)|0.07|
|Quads||
|Max.Axial Quad. Occupancy|0.8|
|NumberofArrays|1978|
|NumberofQuads|23,736|
|Effective Field Length(crn)|18.1|
|Quad Length (cm)|22.6|
|Beam Radius (cm)|6.8|
|Quad Bore (cm)|8.9|
|LET Cores||
|Number|804|
|Length (cm)|20|
|Radial Build (cm)|80|
|HETCores||
|Number|6840|
|Length(crn)|10|
|Radial Build (cm)|40|
|TotalMetglass(MT)|14.3|

![](images/tmpnzkalo9i.pdf-0035-02.png)

**Table 2.4. Final Compression and Focus Design Parameters**

| Parameter | Value |
|---|---|
| Transport Length (m) | 611 |
| Linac-to-Target Distance (m) | 187 |
| Total Width (⊥ to linac) (m) | 484 |
| Number of Quadrupoles | 984 |
| Number of Dipoles | 528 |

**Transport Section.** The transport section splits the 12-beam bundle from the linac into two 6-beam bundles, then transports each of the 6-beam bundles so that they are aimed at the target from a sufficient distance to accommodate compression and transverse focus. The transport section is composed of four elements: an initial transition element to transform the 12-beam bundle into two 6-beam columns, a 90 degree bend to direct the columns away from the linac axis, a straight section to carry the columns the required distance from the axis, and a 180 degree bend to direct the bundles back towards the target.

**Compression Section.** The compression section provides the specified 10 ns longitudinal focus in the middle of the final focusing quadrupole set. The compression section is comprised of three elements: the compressor element to provide the required velocity tilt, a transition element to transform the 6-beam column into a hexagonal ring, and a spreading element to provide sufficient clearance between the beams so that the final focusing quads of adjacent beams can be packaged.

Pulse shaping to provide a pre-pulse at the target would be done by tailoring the applied voltage gradient waveform in the compressor. This approach allows an arbitrary fraction of the pulse energy to be in the pre-pulse while preserving the equivalence of the individual beams.

**Transverse Focus Section.** The transverse focus section delivers the longitudinally-compressed beam to the target. It consists of two elements: a focusing telescope, which provides the required convergent angle to the beam bunches, and a reactor transport element, which provides the final beam steering and the auto-neutralizing electrons immediately before the beam bunches enter the reactor chamber. Some combination of shielding, baffles, and shutters at the reactor interface must be included to protect the final focusing components from target radiation, target debris, and hot molten Flibe.

|Driver Energy(MJ|3.4|
|---|---|
|Target Gain|118|
|Target Yield (MJ)|400|
|Rep Rate (Hz)|6.7|
|Fusion Power (MW)|2677|
|Energy Multiplication|1.08|
|Total Thermal Power_(MW)_|289 1|
|Power Conversion Efficiency(%)|47|
|Gross Electrical Power (MWe)|1359|
|Driver Efficiency(%)|7.5|
|Driver Power (MWe)|304|
|Auxiliary Power (MWe)|**_55_**|
|Net Electric Power (MWe)|1000|
|Tritium Breeding Ratio|1.25|

|First Wall Radius at Midplane (m)|6.5|
|---|---|
|Overall Internal Height(m)|18|
|First Wall Thickness (cm)|1.o|
|Maximum**Stress**in First Wall (MPa)|43|
|Blanket Thickness (m)|1.o|
|Total Thermal Power_(MW)_|2981|
|Surface Power_(MW)_|803|
|Blanket Power_(MW)_|2088|
|Li20 Inlet Temperature ("C)|550|
|Li20 Avg. Outlet Temperature ("C)|740|
|Liz0 Flow Rate**_(kgls)_**|5590|
|Max Li20 Velocity at**`FW`**_( d s )_|1.15|
|Number of Blanket Modules|12|
|Structural Mass Per Module (Tonne)|37.8|
|Number of Beam Ports|60|
|Li20 MassinChamber (kg)|670,000|
|Total Li20 Inventory (kg)|2,000,000|

![](images/tmpnzkalo9i.pdf-0039-00.png)

![](images/tmpnzkalo9i.pdf-0042-00.png)

![](images/tmpnzkalo9i.pdf-0043-00.png)

|**Overall Driver:**||
|---|---|
|Total Energy on Target'(MJ)|3.6|
|Number of Beam Clusters|60|
|Beamlets per Cluster|100|
|Final Pulse Width (ns)|6|
|Efficiency**`(96)`**|7.5|
|**Ultimate Amplifier:**||
|Final Amp Energy(kJ)|60|
|ArinKr(%)|50|
|Pressure (atm)|1|
|InitialTemperature(C)|500|
|Pumping (k~/cm3)|400|
|Extraction Time (ns)|600|
|Amplifier Gain|16|
|Reg-Rate**(Hz)**|6.7|
|LengthinOptical Direction(m)|1|
|Length in Flow Direction (m)|2|
|LengthinE-beam Direction(m)|1|
|Flush Factor|1.3|
|Fluence (Jkm2)|**_5_**|
|E-beam Voltage &V)|610|
|**DiodeCurrent**(Ncm2)|**40.6**|
|Diode Impedance(ohms)|0.6|
|Inductance (nH)|23|
|Applied Field**_(kG)_**|6|
|Intrinsic Efficiency(%)|14.5|

![](images/tmpnzkalo9i.pdf-0049-00.png)

![](images/tmpnzkalo9i.pdf-0050-03.png)

|**Production Step**|**Chosen Technique**|
|---|---|
|Capsule Production|Drop Generator/Microencapsulation|
|FuelFill|InjectionFillTechniques|
|DT Layer Formation|Freeze-Laser Pulse Vaporization-Refreeze|

![](images/tmpnzkalo9i.pdf-0056-01.png)

|Acceleration(8)|130|
|---|---|
|Accelerator Length (m)|9|
|Final Injection Velocity**_( d s ) _**|151|
|Time in Accelerator(m)|119|
|Sabot Removal Length(m)|**2.5**|
|Time for Sabot Removal(m)|17|
|Rotational Velocity for Sabot Removal**`(RPM)`**|570|
|Time for Tracking (ms)|50|
|Time in Chamber(ms)|50|
|Total Time from Target FiringtoIgnition(ms)|**235**|
|Time Allowed forCoarseCorrections(ms)|100|
|Time Allowed for Fine Corrections(ms)|_50_|

![](images/tmpnzkalo9i.pdf-0060-01.png)

![](images/tmpnzkalo9i.pdf-0062-00.png)

||**SOMBRERO**|**Osiris**|
|---|---|---|
|**`Wall`**Temperature(K)|**1758**|**923**|
|**`Gas`**Temperature**(K)**|**1758**|**923**|
|Gas Density (cm-3)|**3.55**x1016|**3.55**x**1012**|
|**`Gas`**Species|**Xenon**|**mbe**|
|Conductive Heat Load (W/cm2)|**4.2**|**6**x**10-5**|
|Radiative Heat Load (W/cm2)|**54.2**|**4.1**|
|Total Heat Load (W/cm2)|**58.4**|**4.1**|

||**Osiris**|**SOMBRERO**|
|---|---|---|
|Time (ms)|**33**|43|
|Hohlraum|**22**|N/A|
|Capsule|**`22`**|700|
|DT Fuel|**`8`**|17|

||**Osiris**|**SOMBRERO**|
|---|---|---|
|Maintenance of Chamber Components|Remote|Remote|
|Maintenance of Power Cycle Components|Hands-on|Hands-on|
|Chamber Radwaste Classification|A|A|
|Shield Radwaste Classification|A|A|
|Breeder Radwaste Classification|A|C|
|RoutineT2Release (Cud)|92|93|
|Maximum Dose to Exposed Individual|||
|from Routine Release (mredy)|2.43|0.93|
|Total T2Inventory(8)|||
|Reactor|13|183|
|Fuel Processing|54|74|
|Target Factory|300|300|
|Accidental WB Early Off-SiteDoseat1**km**(rem)|||
|Reactor|0.13|2.22|
|Fuel Processing|0.48|0.68|
|Target Factory|2.70|2.70|

||**Osiris**|**SOMBRERO**|
|---|---|---|
|Driver Systems|0.87|0.89|
|Reac tor**S**ys tems|0.90|0.89|
|Target Systems|0.92|0.90|
|Energy Conversion&**BOP**|0.96|0.96|
|Total|0.69|0.68|

||**Osiris**|**SOMBRERO**|
|---|---|---|
|Driver Systems|0.94|0.93|
|Reactor Systems|0.94|0.95|
|Target Systems|0.94|0.94|
|Energy Conversion&BOP|0.98|0.98|
|Total Unplanned|0.81|0.81|
|Planned|0.92|0.92|
|Overall|0.75|0.75|

![](images/tmpnzkalo9i.pdf-0071-01.png)

![](images/tmpnzkalo9i.pdf-0073-01.png)

|Technical Immaturity|10%|
|---|---|
|Critical Technology|30%|
|High Development Cost|30%|
|**LongLead**Time|20%|
|%Cost in Experiments|10%|

||**Current**|||
|---|---|---|---|
||**Technical**|**Development**|**Devel.**|
|**Item**|**Credibility**|**Needs**|**Priority**|
|Driver|Low|High|**1**|
|Target Fabrication|Low|High|2|
|Reactor Chamber|Low|Moderate|**3**|
|Target Injection|Moderate|Moderate|**4**|
|IHX|Moderate|Low|**_5_**|
|Steam Generator|Moderate|Low|**6**|
|Hibe PumpdDucts|High|Low|**`7`**|
|Shielding|High|Low|**8**|
|Reactor Building|High|Low|9|
|Power Conversion|High|Low|10|

||**Current**|||
|---|---|---|---|
||**Technical**|**Develop men t**|**Devel.**|
|**Item**|**Credibility**|**Needs**|**Priority**|
|Driver|Low|High|1|
|Target Fabrication|Low|High|**2**|
|Reactor Chamber|Moderate|Moderate|3|
|Target Injection|Moderate|Moderate|**4**|
|Final Optics|Moderate|Moderate|5|
|Reactor Building|Moderate|Moderate|6|
|Li20 Transport|High|Low|7|
|IHX|High|Low|**8**|
|Steam Generator|High|Low|9|
|Shielding|High|Low|10|
|Power Conversion|High|Low|11|

![](images/tmpnzkalo9i.pdf-0080-00.png)

||**Osiris**|**SOMBRERO**|
|---|---|---|
|Reference Design|5.61|**6.67**|
|Higher Rep-rate Designs|**5.37**|**6.45**|
|Conservative**`Gain`**Curve|**5.64**|**7.44**|
|Optimistic Gain Curve|5.15|**5.89**|
|Lower Net Power(500MWe)|**7.69**|**8.88**|
|Higher Net Power (1500 MWe)|**4.48**|**5.49**|

||**Osiris**|**SOMBRERO**|
|---|---|---|
|**Driver**|||
|Driver Energy**(MJ)**|**_5_**_.O_|3.4|
|Rep-Rate (Hz)|4.6|6.7|
|Driver Efficiency|28.2|7.5|
|**Target**|||
|Type|Indirect Drive|Direct Drive|
|Target Gain|86.5|118|
|Yield(MJ)|432|400|
|**Chamber Design**|||
|First Wall Material|Woven Graphite Fabric|**4-D**C/C Composite|
|X-ray and Debris Protection|Liquid Flibe|3.25 torr-mofXe|
|First Wall Radius,m|3.5|6.5|
|Estimated First Wall Life (fpy)|1.8|5|
|Breeding Material|Molten Flibe|Li20 Granules|
|Blanket Thickness(m)|0.7|1.o|
|Tritium Breeding Ratio|1.24|1.25|
|Overall Energy Multiplication|1.26|1.08|
|Chamber OuterWallMaterial|C/C Composite|C/C Composite|
|Outer Wall Radius(m>|6.5|7.5|
|**Power Conversion System**|||
|Primary Coolant|Flibe|He w/ Li20 granules|
|Temperature Range ("C)|500-650|550-700|
|Intermediate Coolant|k a d|Lead|
|Temperature Range("C)|400-600|**`400`**-600|
|Secondary Coolant|Water/Steam|Water/Steam|
|Temperature Range("C)|286-538|286-538|
|Cycle|Double Reheat|Double Reheat|
|Peak Steam Pressure (MPa)|24|24|
|Power Conversion**Eff.**(%)|**45**|**`47`**|
|**Power Balance**|||
|Fusion Power(MW)|1987|2677|
|Total Thermal Power (MWt)|2504|2891|
|Gross Electric Power ( m e )|1127|1359|
|Driver Power( W e )|82|304|
|Auxiliary Power (MWe)|45|55|
|Net Electric Power ( W e )|1000|1000|

