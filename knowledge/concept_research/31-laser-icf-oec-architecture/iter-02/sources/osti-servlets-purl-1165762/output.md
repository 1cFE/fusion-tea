---
source: "https://www.osti.gov/servlets/purl/1165762"
source_type: "url"
extracted_at: "2026-04-20T18:25:48.403945+00:00"
content_hash_sha256: "b6de233083c2044f4c62f416809f220536f7c5950c670ff36298f2ca3021092b"
backend: "pdf_pipeline"
---

LLNL-TR-658973 

![](images/tmpub8jbof1.pdf-0001-01.png)

Assessment of Tritium Breeding Blankets from a Systems Perspective - Status Report 

W. R. Meier August 20, 2014 

## **Disclaimer** 

This document was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor Lawrence Livermore National Security, LLC, nor any of their employees makes any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or Lawrence Livermore National Security, LLC. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or Lawrence Livermore National Security, LLC, and shall not be used for advertising or product endorsement purposes. 

This work performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. 

**LLNL-TR-658973** 

## **Assessment of Tritium Breeding Blankets from a Systems Perspective – Status Report** 

## **Wayne Meier LLNL** 

## **August 20, 2014** 

This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. This material is based upon work supported by the U.S. Department of Energy, Office of Science, Office of Fusion Energy Sciences. 

## **Contents** 

1.  Introduction and Executive Summary 

2.  Mission Description 

3.  System Operational Context and Reference Operational Architecture 

4.  System Driver and Constraints 

5.  Preferred Concept Selection and Rationale 

6.  Proposed System Architecture 

7.  System Requirements 

8. Risks and Technology Assessment 

9. Key Findings and Recommendations 

## **Appendices** 

- A. Tritium Breeding Blanket Data Sheets 

- B. Comparison Criteria 

- C. Bibliography 

## **1. INTRODUCTION AND EXECUTIVE SUMMARY** 

## **1.1 Introduction** 

The author has been engaged in the review of tritium breeding blanket (TBB) concepts for magnetic fusion energy (MFE) for the past year. The main object of the review is to provide the DOE/Fusion Energy Sciences (FES) sponsor with information to help evaluate current and near term R&D priorities with the ultimate goal of developing a TBB for future commercial fusion power plants. The approach taken in this report is to look at the TBB in an integrated system fashion and compare options against a variety of high level system objectives. This systems engineering approach does not dig into the specific details of past, ongoing or future R&D activities. This report is based on my personal review of a large body of scientific literature indicated in the bibliography and on personal communications with key R&D leaders in the field, both nationally and internationally. The views are my own, informed by the underlying research; they are not meant to represent a consensus opinion. This is a status report as of August 2014, and it focuses more heavily on liquid breeders since that is where the majority of effort has been spent. Ceramic breeders  are include, but will be given more attention in the coming year. Finally, this report is intentionally written for the non-expert, beginning with an elementary description of the TBB and its functions. 

## **1.2 Executive Summary** 

The goal of developing a new source of electric power based on fusion has been pursued for decades. If successful, future fusion power plants will help meet growing world-wide demand for electric power. A key feature and selling point for fusion is that its fuel supply is widely distributed globally and virtually inexhaustible. Current world-wide research on fusion energy is focused on the deuterium-tritium (DT for short) fusion reaction since it will be the easiest to achieve in terms of the conditions (e.g., temperature, density and confinement time of the DT fuel) required to produce net energy. A key component of all DT fusion power plants will be a tritium breeding blanket (TBB) that has two key functions: 

- 1) produce more (just slightly) tritium fuel than is consumed, and 

- 2) absorb the fusion power and make it available to a power conversion cycle (to produce electricity). 

Over the past decades countless studies have examined various concepts for TBBs for both magnetic fusion energy (MFE) and inertial fusion energy (IFE). At this time, the key organizations involved are government sponsored research organizations world-wide. The nearterm focus of the MFE community is on the development of TBB mock-ups to be tested on the ITER tokamak currently under construction in Caderache France. TBB concepts for IFE tend to be different from MFE primarily due to significantly different operating conditions and constraints. 

This report focuses on longer-term commercial power plants where the key stakeholders include: electric utilities, plant owner and operator, manufacturer, regulators, utility customers, and inplant subsystems including the heat transfer and conversion systems, fuel processing system, plant safety systems, and the monitoring and control systems. 

In addition to meeting the two functions listed above, key stakeholder expectations include: safe operation in normal and off-normal conditions, high reliability, maintainability, high efficiency (e.g., operate at high temperature for efficiency power conversion and with low input power needs), low environmental impacts in terms of radioactive and other waste streams (over the life of the plant and after shutdown/ decommissioning). 

The TBB concept is explained in more detail in the body of the report, but its essential functional features are depicted in Fig. 1.1. The primary input is power from the fusion reactions (both surface heating and nuclear heating resulting from fusion neutron reactions with blanket material). The primary outputs are thermal power and tritium. The vast majority of the blanket thermal power is removed by a blanket coolant; thus the TBB requires a coolant inlet and outlet. A small fraction of the thermal power flows to surrounding components such as the shield via low energy neutron leakage, gamma radiation and thermal radiation. Tritium is created in the TBB via nuclear reaction with lithium (see Section 2.1) and is continuously removed from the blanket. Various options for this recovery have been proposed and depend strongly on the TBB design details; in some cases T is removed with the coolant flow while other designs provide a dedicated system to capture and remove the T from the TBB. A schematic of the top level inputs and outputs of the TBB is shown in Fig. 1.2. 

![Fig. 1.1. Essential functions of the tritium breeding blanket](images/tmpub8jbof1.pdf-0006-03.png)

![Fig. 1.2. Schematic of level inputs and outputs of the TBB.](images/tmpub8jbof1.pdf-0007-00.png)

The TBB is shown schematically in the operational context of a Tokamak power plant in Fig. 1.3. The TBB surrounds the fusion plasma and is surrounded by shielding and the magnetic coils that confine the plasma. This figure indicates the flow of DT fuel into the plasma, the D,T and He recovery from plasma exhaust (white pipe) and T extraction from the TBB (vertical green pipe not labeled). The coolant loops through the blanket provide heat to drive the turbine generator. 

The scope of this report is limited to TBBs for an MFE Tokamak. World-wide there are less than a dozen designs actively being developed. 

![Fig. 1.3. Schematic of the power core of tokamak power plant indicating the location of the TBB (adapted from mpg.de)](images/tmpub8jbof1.pdf-0007-04.png)

## **2. MISSION DESCRIPTION** 

## **2.1 Introduction to the Essential Functions of the TBB** 

As previously noted, current world-wide research on fusion energy is focused on the deuteriumtritium (DT for short) fusion reaction since it will be the easiest to achieve in terms of the conditions (e.g., temperature, density and confinement time of the DT fuel) required needed to produce net energy. Deuterium ([2] H or D) is a stable isotope of hydrogen with a single neutron in the nucleus (atomic mass ~ 2); it occurs naturally and can be extracted from water. Tritium ([3] H, or T) is also an isotope of hydrogen with two neutrons in the nucleus giving it an atomic mass of ~3. Tritium is radioactive, decaying by beta emission (which transforms this hydrogen isotope into a helium isotope, denoted[3] He) with a half-life of 12.3 years. Due to this relatively short half-life, there is no natural abundance of T. Therefore, fusion power plants based on the DT reaction must produce their own T. The process is referred to as tritium breeding, and the component of the fusion power plant that carries out this function is called the tritium breeding blanket (TBB), or breeding blanket, or simply blanket. 

To understand how it is possible for a power plant to create its own fuel, we need to look at the nuclear reactions involved. The DT fusion reaction is 

![](images/tmpub8jbof1.pdf-0008-04.png)

The nuclear reaction between D and T produces a helium nucleus (also called an alpha particle,  ) and a neutron. In the process energy is released that appears in the form of kinetic energy of the alpha particle and neutron. To create tritium to provide a continuous supply of fuel, the neutron must initiate nuclear reactions with lithium (an alkali metal that is abundantly available in the earth’s crust). Lithium has two isotope,[6] Li and[7] Li and both have T producing reactions with neutrons emitted by the fusion reaction: 

![](images/tmpub8jbof1.pdf-0008-06.png)

> 7Li + n  T +  + n' 

Both reactions produce a new T and a helium nucleus. The reaction with[7] Li also emits another lower energy neutron (n') that can subsequently produce more reactions with[6] Li. In this way, one fusion neutron can result in more than one T reaction product. 

## _**The TBB must produce at least as much T as is consumed in the fusion reactions.**_ 

The ratio of T atoms produced in the blanket to T atoms consumed in the fusion reactions is called the tritium breeding ratio, TBR. Breeding blanket designs typically have a goal of breeding an extra10% (TBR = 1.10) to account for uncertainties in the predicted blanket performance, supply T start-up inventory for new power plants, account for radioactive decay, 

and account for losses in the fuel processing systems (losses to the environment must be extremely low). 

To accomplish the requirement of obtaining a TBR greater than 1.1, the TBB must completely surround the fusion power source, with the exception of areas required for plasma heating, vacuum pumping, and in the case of IFE, beam port entry. As a result, the TBB absorbs nearly all the fusion power and this power must be made available to a heat transfer systems that transports thermal power to a power conversion systems to produce electricity. This power flow is shown schematically in Fig. 1.3. 

While it is possible to achieve a TBR>1.1with a liquid Li blanket (just based on the extra neutrons from the 7Li reaction), most TBBs also include a neutron multiplier material. Beryllium (Be) or Be compounds are commonly use, particularly for TBB based on Li ceramics. Lead (Pb) is also an effective neutron multiplier and is present in TBB designs using a lithium-lead molten metal coolant. Both these elements undergo (n,2n) reactions thus multiplying the number of neutrons available that can subsequently be captured in T breeding reactions primarily with[6] Li, which has a high cross section for low energy neutrons. 

The fusion power is delivered to the TBB as both surface heating and penetrating nuclear heating. The structure that is directly exposed to the fusion source is called the first wall and is considered an integral part of the TBB. It must absorb and conduct the surface heat to the blanket coolant. Fusion neutrons penetrate into the blanket a cause heating due to nuclear reactions with blanket materials (nuclear heating), the most important of which are the tritium breeding reactions with lithium. In order for the plant to produce electric power, the blanket thermal power must be removed at a temperature that is high enough to drive the selected power conversion cycle. Designs being considered typically operate with blanket coolant outlet temperature greater than 400 C. 

_**The TBB must absorb the fusion power and make it available to the power conversion systems at high temperature.**_ 

## **2.2 Active Stakeholders** 

This section covers the active stakeholders. In this report we take the context as the future where fusion power has been proven feasible and it has become an option for a commercial electric power plant. The most important current stakeholders are the agencies currently sponsoring R&D on TBBs (e.g., DOE), but their plans must ultimately be focused on developing a product for commercial use. Thus the criteria should be similar if not the same. 

## **2.2.1 Utility Owner/Operator** 

We assume that it is the electric utility makes the decision to build and operate the fusion power plant as part of its energy supply mix. This is clearly a key stakeholder since without a positive 

decision on their part the plant, including the TBB, is not built. Top level expectations of the utility owner/operator include the ability to produce and sell electricity in an economically competitive, reliable, safe and environmentally acceptable manner. In order to meet these toplevel expectations, the TBB is expected to: 

- Supply the tritium fuel 

- Have an acceptable capital cost (as part of the overall plant capital cost) 

- Have an acceptable operating cost (fixed and variable) 

- Facilitate high efficiency power conversion 

- Have high availability 

   - Reliability (low unplanned outages) 

   - Maintainability (short maintenance times) 

- Operate safely in normal and off-normal conditions including (start-up and shut-down) 

- Have low radioactive and hazardous waste streams (during plant operations and at end of plant life). 

## **2.2.2 Plant Maintenance Personnel and Equipment** 

During the life of the power plant, the TBB will certainly require repair and/or replacement. Neutrons from the fusion reaction will cause blanket materials to become radioactive over time to the point that hands-on maintenance will not be possible. Therefore, the TBB must be designed to allow access and repair by remote maintenance equipment. Ideally the expectations would include easy access for either in situ repair or rapid removal and replacement with new or refurbished blanket components. 

## **2.2.3 Fusion Plasma** 

As previously noted the TBB nearly completely surrounds the fusion plasma with the exception of ports needed for heating, vacuum pumping, plasma fueling and exhaust at the divertor. As such, the geometry of the TBB must conform to the geometry of the plasma which is set by the magnetic configuration.  The inner surface of the TBB is called the first wall and it is directly exposed to the fusion plasma. Plasma interactions with the first wall can cause first wall material to be expelled into the plasma core. Expectations here are that the TBB blanket can be designed to conform to the plasma geometry and that the first wall design and operating conditions do not prevent the plasma from behaving as expected. 

## **2.2.4 Heat Transfer System** 

The heat transfer system also interacts directly with the TBB. Some means must be provided to extract the fusion power that is deposited in the blanket and deliver the power to a power conversion system. Various liquid and gases coolants are being considered. The heat transfer fluid is delivered through an inlet connection (typically a pipe), flows through the blanket as it is heated and then exits through an exit connection. The expectation is that the TBB can be design 

to allow enough heat transfer area between the blanket structure and the coolant to all for efficient heat transfer under reasonable coolant flow conditions (e.g., pressure, flow velocity, temperature change from inlet to outlet). 

## **2.2.5 Tritium Processing System** 

Tritium that is bred in the blanket must be continuously removed and delivered to the tritium processing system (TPS). Various approaches have been considered and deemed feasible. In some cases the T is removed as a part of the coolant flow stream, while other designs provide a dedicated method for T extraction, for example a flow stream of He that picks up T as it flows through the breeder material. The expectation is that the TBB can be designed to allow for continuous T removal in a manner that does not require excessive electrical power and does not allow a large inventory of T to build up in the blanket. Excessive power consumption would reduce the amount of electricity available for sale and thus adversely impact the plant economics. High T inventory in the blanket is a safety issue for the power plant. 

## **2.2.6 Instrumentation and Controls (I&C) System** 

Thermal and mechanical aspects of the TBB will be monitored to assuring that it is operating within allowable ranges. The expectation is that the design of the TBB will accommodate monitoring sensors needed to determine and, if need be, adjust plant operating parameters related to the TBB functions, e.g., adjusting the coolant flow rate. 

## **2.2.7 Plant Safety Systems** 

Various accident scenarios will be evaluated for the power plant including accidents that could involve the TBB, e.g., loss of coolant flow to the blanket, loss of T containment, etc. The specific types of possible accidents and safety systems needed to mitigate consequences will depend on the TBB design details. Expectations are that the TBB will be designed to operate safely in normal and off-normal conditions including accommodating possible active measures in response to an accident, e.g. supplemental cooling, drain tanks, fire suppression, etc. 

## **2.3 Passive Stakeholders** 

This section describes those stakeholders that indirectly influence the TBB. 

## **2.3.1 Manufacturer/Supplier** 

It is likely that the TBB components will be manufactured by an industrial supplier that will contract with the plant owner to build and deliver components to the plant site. Expectations of the manufacturer/ supplier are that the TBB can be built at a cost that is acceptable to the owner. Considerations include design complexity, cost and availability of materials, industrial experience with required manufacturing techniques, ability to meet industrial standards, e.g., AMSE. 

## **2.3.2 Builder/Installer** 

The TBB is too large to assemble in a factory and delivered as a single unit to the power plant; it will be delivered as a large number of components. The plant owner will contract with an Architect-Engineering firm to build the plant including installation of the TBB. The builder/installer expects that the TBB design can be assembled and installed in a straightforward manner and not lead to delays in the construction schedule. Considerations include component complexity, weight, number of on-site connections to other components, interfaces to coolant and T recovery systems. 

## **2.3.3 Regulators** 

The plant owner will need to secure a license to operate from regulators, which could include local, state and federal requirements. With respect to the TBB, the most important regulations will relate to plant safety. Expectations are safe operation in normal and off-normal conditions especially containment of T and preventing release of radioactive or chemically hazardous materials to the surrounding environments. 

## **2.3.4 Utility Customers** 

Utility customers are passive stakeholders in that they receive the electricity generated by the plant. Their expectation is for reliable delivery of electricity at an affordable price. A plant with high availability is needed to meet these expectations. The TBB must be highly reliable so as not to adversely impact overall plant availability. Also its capital and operating costs cannot be excessively high. 

## **2.3.5 Plant Personnel (other than maintenance)** 

The power plant will have hundreds of employees to operate and maintain the plant. Most will have no direct interaction with the TBB but expect a safe working environment. The TBB must be designed for safe operation in normal and off-normal conditions. 

## **2.3.6 Neighboring Public** 

The public in areas surrounding the power plant also expect that the plant will not endanger their safety or health. The TBB must be designed for safe operation in normal and off-normal conditions. 

## **2.3.7 Surrounding Ecosystem** 

The fusion plant is expected to operate in a manner that does not have significant environmental impacts and this will be carefully reviewed and studied as part of the licensing process. The expectation is that the TBB subsystem of the plant will not lead to adverse environmental impacts. 

## **2.4 Sacred Expectations** 

From the above, we conclude that the sacred expectations are that the TBB: 

- 1) Produce more T fuel than is consumed and allow for continuous recovery, 

- 2) Absorb fusion power and make it available to the power conversion system at high temperature, 

- 3) Have acceptable capital and operating costs (i.e., do not prevent economic viability of the overall plant), and 

- 4) Operate safely in normal and off-normal conditions. 

## **3. SYSTEM OPERATIONAL CONTEXT AND REFERENCE OPERATIONAL ARCHITECTURE** 

## **3.1 System Operational Context** 

The operational context for the TBB considered in this report is a future commercial MFE power plant. The functional boundary of the system is shown in Fig. 3.1 (the same as Fig. 1.2). A context diagram for the TBB showing active and passive stakeholders is given in Fig. 3.2. 

![Fig. 3.1 Function boundary of the TBB showing primary inputs and outputs.](images/tmpub8jbof1.pdf-0014-03.png)

![Fig. 3.2  Context diagram indicating Active and Passive Stakeholders.](images/tmpub8jbof1.pdf-0014-05.png)

## **3.2 Reference Operational Architecture** 

Since commercial fusion power is a couple decades off, there many TBB concepts under development worldwide. While there is not yet a clear _reference architecture_ , we take the helium cooled, lithium-lead (HCLL) TBB concept as the starting point for the purposes of this report. This concept is currently favored in the EU and is a candidate TBB several other countries with strong fusion development programs (i.e., ITER partners) including the US. The US, however, has proposed a modified version of the HCLL that has improved thermal efficiency potential; this concept will be considered as one of the alternates evaluated later in the report. 

## **3.2.1 Helium Cooled Li-Pb TBB** 

The HCLL blanket concept is illustrated schematically in Fig. 3.3. The essential features are the TBB module structure; He coolant inlet, distribution and outlet; LiPb supply, distribution and outlet. A steel containment structure defines the shape of the TBB module including the first wall (FW) that faces the plasma.  The entire blanket that surrounds the fusion plasma will be made up of hundreds of these modules. Helium coolant inlet/outlet pipes are attached to the structure as are LiPb inlets and outlets. The internal features of the TBB module are designed to distribute the LiPb and He in a manner that the tritium breeding and cooling functions are achieved. Figure 3.4 is a more realistic illustration of how the TBB module would look. 

![Fig. 3.3 Schematic of the HCLL TBB module.](images/tmpub8jbof1.pdf-0015-04.png)

![](images/tmpub8jbof1.pdf-0016-00.png)

**----- Start of picture text -----**<br>
PbLi outlet<br>He inlet<br>First Wall<br>He outlet<br>Breeding units<br>PbLi inlet<br>**----- End of picture text -----**<br>

Fig. 3.4.  More detail concept illustration of the PbLi TBB module (from L.V. Boccaccini et al, “Design and Development of DEMO Blanket Concepts in Europe,” IAEA Demo workshop, 2012) 

## **4. SYSTEM DRIVERS AND CONSTRAINTS** 

The performance drivers for the TBB design evolve from the sacred expectations. 

**Tritium Breeding Performance.** The materials used in the TBB and their configuration must be such that a TBR> 1 can be achieved. This sets constraints on the type of materials that can be used (e.g., strong neutron absorber must be avoided), the relative fractions of materials (i.e., need sufficient atomic density of Li), the arrangement of materials within the TBB (e.g., neutron multipliers if used must be placed toward the plasma side of the TBB to be effective), and the overall thickness of the TBB (since fusion neutrons are very penetrating). A wide variety of TBB design concepts have been proposed that meet these constraints. 

**Power Recovery and Conversion Performance.** The requirement for absorbing the fusion power and making it available to the power conversion system at high temperature is also a significant design driver. The design must incorporate a method for heat removal, typically accomplished by either flowing a liquid metal breeder (such as Li, PbLi or molten salt) or by incorporating coolant flow channels through the TBB. This cooling function must be achieved while not preventing the essential T breeding function. Constraints include considerations of compatibility of coolants with structural materials they contact at the temperatures needed for efficient power conversion (i.e., minimizing corrosion), possible magneto-hydrodynamics (MHD) power losses due to flowing liquid metals in the Tokamak’s magnetic fields, and the need to avoid contamination of the coolant by T if the breeder is not also the coolant. The ability to operate at high temperature is a strong economic driver for the plant since the power conversion efficiency increase with coolant temperature.  The pumping power to circulate the coolant, particularly He, reduces the net electric power available and thus net plant efficiency. 

**Safe Operation.** Safety is a significant design driver and impacts the selection of TBB structural materials (low activation materials are preferred or even required) and also the breeder itself (low chemical activity is preferred). The licensing and regulatory review will require integrated safety analyses of possible accident scenarios for the plant. Failure of the TBB and release of T or other radioactive material can impact those results. As such, constraints may arise from the safety but they are very design depend and cannot be generalized (e.g., limits on the amount of Li in the TBB). 

## **5. PREFERRED CONCEPT SELECTION AND RATIONALE** 

In this section we describe alternative for the key system elements that make up the TBB and give the rationale for selecting a preferred TBB design. 

## **5.1 TBB Components Options** 

The following tables highlight some key feature of the major constituents of possible TBB designs: Table 5.1 covers tritium breeders, Table 5.2 neutron multipliers, Table 5.3 coolants, and Table 5.4 structural materials. 

**Table 5.1 Tritium Breeder Options** 

**Table 5.2 Neutron Multiplier Options** 

**Table 5.3 Coolants Options (see Table 5.1 for coolants that are also breeders)** 

**Table 5.4 Structural Material Options** 

## **5.2 Example TBB Component Combinations** 

There have been a number of TBB conceptual designs proposed using various combinations of breeder, neutron multiplier, coolant and structural material: 

_Name (abbreviation): Breeder / Multiplier / Coolant / Structure_ 

1. Lithium/Vanadium (LV): Li / none / Li / V 

2. Water Cooled Lead Lithium (WCLL): PbLi / Pb in PbLi / water / FMS 

3. He Cooled Lead Lithium (HCLL): PbLi / Pb in PbLi / He / FMS 

4. Dual Cooled Lead Lithium (DCLL): PbLi / Pb in PbLi / PbLi and He / FMS 

5. DCLL with FCI: (DCLL-FCI): PbLi / PbLi / Pb in PbLi / PbLi and He / FMS with FCI 

6. Molten Salt (MS): Flibe / Be in Flibe / Flibe / ODS 

7. He Cooled Pebble Bed (HCPB): Ceramic Breeder / Be / He / FMS 

## **5.2.1 Comparison with Respect to Stakeholders Expectations** 

The following table gives a relative comparison of the concepts against stakeholder expectations with an emphasis on the sacred expectations (entries 1-4 in row 1). A rough relative comparison (1= higher than others, 2 = comparable, 3 = lower than others) is given. 

**Table 5.5 Comparison of concepts on ability to meet key expectations** 

*Key to expectations used in Table 5.5: 

- 1) Tritium Supply (TS): Produce more T fuel than is consumed and allow for continuous recovery 

- 2) Power Handling (POW): Absorb fusion power and make it available to the power conversion system at high temperature 

- 3) Costs (COST): Have acceptable capital and operating costs 

- 4) Safety (SAF): Operate safely in normal and off-normal conditions 

- 5) Reliability (REL): Potential for high reliability leading to high availability 

- 6) Environmental (ENV): Low environmental impact from induced radioactivity waste 

- 7) Tritium extraction (TEX): Ease of tritium recovery from breeder 

- 8) Fabricability (FAB): Can be fabricated with standard proven methods 

The results of this top level comparison are summarized as follows: 

- The LV concept has advantages in terms of good T breeding performance, power extraction (good heat transfer and low pumping power) and environmental criteria (since Li does not activate). It suffers for safety concern with the use of Li, the difficulty of extracting T from Li and the use of an expensive structural material (V) that is difficult to fabricate. 

- The WCLL main advantage is a power cycle based on proven technology leading to lower cost and likely higher reliability for the overall system. It disadvantages are limited 

operating temperature giving a lower conversion efficiency than the others and concerns over the possibility of accidental interaction of water and PbLi. 

- The HCLL concept gets solid ratings across the board with the except of power extraction. Relying on He to recover all the blanket power requires significant coolant pumping power and impact overall conversion efficiency. 

- The DCLL overall is an attractive concept meeting all expectations. 

- The DCLL-FCI exceeds the DCLL since higher outlet temperatures and thus higher efficiency can be obtained. 

- The MS concept has several negatives related to its poor convective heat transfer coefficient, high cost of the molten salt and fabricability using the more advanced ODS steel. 

- The HCPB is a solid performer across the board, but like the HCLL, will have higher coolant pumping power impacting the plant’s net efficiency. 

## **6. PROPOSED SYSTEM ARCHITECTURE** 

## **6.1 Recommended Configuration** 

Based on the previous comparison, the recommended configuration is the DCLL with flow channel inserts (FCI).  Key features of this TBB configuration are illustrated in Figs. 6.1 and 6.2. The schematic in Fig. 6.1 illustrate how the FCI is positioned between the flowing PbLi breeder and the steel structures of the TBB which are cooled with high pressure He. The FCI insulates the steel so that the outlet temperature of the PbLi coolant can exceed the limiting operating temperature of the steel. Figure 6.2 gives a more realistic view of the TBB configuration. This figure illustrates the routing of the He and PbLi coolants. It also shows how all regions that are filled with PbLi are lined with SiC. 

![Fig. 6.1 Schematic of DCLL configuration showing how the SiC flow channel insert is positioned in the PbLi coolant/breeding region (from N. Morley, FPA meeting, 10/11/2005)](images/tmpub8jbof1.pdf-0023-03.png)

![Fig. 6.2.  A more detail diagram showing the internal configuration of the DCLL TBB using FCI (from N. Morley, FPA meeting, 10/11/2005).](images/tmpub8jbof1.pdf-0023-05.png)

## **6.2 Comparison of Processes** 

The original DCLL TBB design and the selected DCLL-FCI design operate in virtually the same manner with a two key differences: 

- 1) The DCLL-FCI can achieve a higher PbLi outlet temperature which leads to a more efficient thermal conversion systems and better overall plant economics. This is due to the thermal insulating effects of the FCI. 

- 2) The electrical insulating properties of the FCI reduce the MHD pressure drop and overall pumping power for the PbLi coolant. This translates into less recirculating power and higher net plant efficiency.  Alternatively, a higher flow rate for the same MHD loss may have some advantage in terms of maintaining a lower T inventory in the PbLi by virtue of more rapid processing for T recovery. 

Beyond these two factors, the concepts are comparable. 

## **7. SYSTEM REQUIREMENTS** 

## **7.1 List of System Requirements** 

The system requirements for the DCLL design are listed here. 

1. The tritium breeding material shall be the eutectic of PbLi with 15.7 atomic percent Li. 

2. The PbLi shall be molten to allow flow through the TBB. 

3. The inlet temperature of the PbLi shall be at least 50 C above the melting point. 

4. The outlet temperature of the PbLi shall be 600C or more. 

5. All PbLi flow channels shall be lined with SiC flow channel inserts. 

6. The FCI material shall be constructed in a manner to provide thermal insulation between the PbLi and steel structures. 

7. The FCI shall be constructed to provide magnetic isolation between the flowing PbLi and the steel channel walls. 

8. The TBB structure shall be the ferrtic/martensitic steel, such as FH82. 

9. The maximum steel temperature shall be 550C. 

10. The coolant for the TBB structures shall be He at ~8 MPa pressure. 

11. The helium coolant channels shall be configured to keep the He pumping power as low as possible, ideally below 10% of the plant gross electrical power. 

12. The TBB shall accommodate sensors for temperature, pressure and strain. 

13. The PbLi inlet/outlet flow connects shall allow for gravity draining. 

## **7.2 Mapping of Systems Requirements to Expectations** 

Table 7.1 shows a mapping of the system requirements to the same list of stakeholder expectations discussed in Section 5. This is done to show that the system requirements are indeed required. 

**Table 7.1 Mapping Systems Requirement to Key Expectations** 

*See Table 5.5 for list of Expectations 

The rationale for the mapping of system requirements (SR) against stakeholder expectations is briefly summarized here. 

- SR1:  PbLi is an effective tritium breeding material, it is used for power extraction is safer than the alternative liquid lithium and tritium extraction via vacuum permeation is feasible. 

- SR2:  PbLi must be molten in order to performance the cooling function and allow for continuous T extraction. It also allows online replenishment of Li that is depleted in the T breeding process, thus impacting the tritium supply expectation. 

- SR3:  Inlet temperature must be high enough to avoid the possibility of freezing and plugging a coolant channel, which could impact safety and reliability of operations. 

- SR4:  Outlet temperature determines the thermal cycle efficiency thus impacting power extraction expectation. If it is too high, structural materials could exceed safe and reliable limits. 

- SR5:  Use of the FCI has a major impact on the upper limit on operating temperature. It impacts the safety expectation indirectly in that is allow for more rapid PbLi flow and thus T extraction to lower levels. 

- SR6:  Thermal insulation allows high outlet temperature and efficiency. Also allows the use of available FM steel 

- SR7:  FCI magnetic isolation reduces MHD losses and lowers pumping power. 

- SR8:  FH82 is likely lower cost and easier to fabrication than more advanced steels. Its low activation characteristics impact safety. 

- SR9:  The maximum steel temperature is set by strength and corrosion consideration, thus related to safety and reliability. 

- SR10:  He coolant is used for power extraction. Operating at a high pressure allows for more efficient heat removal. 

- SR11:  The limit on He coolant pumping power impacts the TBB he coolant channel configuration for power extraction.  The impact of He pumping power on the net electric power for sale can be viewed as an operating cost. 

- SR12:  Sensors for monitoring TBB conditions are needed to assure power extraction, detect offnormal conditions with potential safety impacts and assure operating conditions do not overly stress the system which could lead to early failure and reduced reliability. 

- SR13:  The requirement for gravity drain of the PbLi coolant is needed for off-normal shutdown and will also make normal servicing easier. 

## **8. RISKS AND TECHNOLOGY ASSESSMENT** 

## **8.1 Risk Assessment** 

Here we compare the risk of not meeting stakeholder sacred expectations (SE) for the original DCLL TBB and the DCLL-FCI TBB. 

## _SE1) Produce more T fuel than is consumed and allow for continuous recovery_ 

There is high confidence that both concepts can meet the tritium breeding requirement due to the use of the same breeding materials which has enough margin (TBR > 1.1) to present little risk. The DCLL-FCI has additional material that could have a slight negative impact on the TBR, but the use of SiC minimizes this impact. 

_SE2) Absorb fusion power and make it available to the power conversion system at high temperature_ 

Both concepts provide viable methods of extracting the fusion power and delivering it to the power conversion system. The risk of not meeting this expectation is low. As previously note, the selected concept with FCI can achieve high PbLi outlet temperatures and thus improved thermal efficiency for the plant. To take advantage of the higher outlet temperature, more advance power conversion systems must be employed which carried a degree of additional development risk. This is significantly mitigated by the fact that the international power industry is already developing advance, high temperature systems for other energy systems such as nuclear, coal and natural gas. 

_SE3) Have acceptable capital and operating costs_ 

There is significant uncertainty and risk associated with the economics of future fusion power plants, but these are not strongly coupled to the TBB. The addition of FCI should not have a significant impact on the total capital cost of the power plant since the blanket is small part of the overall system. The fact the DCLL-FCI allows for a higher flow rate and minimizes conduction of the breeder heat into the He coolant stream means that there is less power removed by the He coolant. This is an advantage due to the potentially high pumping power demands of the He cooling. Further R&D is needed to see if lower He pressure and therefore thinner structures can be used with the FCI enhance design. 

_SE4) Operate safely in normal and off-normal conditions_ 

With proper overall design, there is confidence that the plant will meet safety expectations. Tritium management (total inventory, losses, accidental leaks, etc.) is extremely important in this regard. The DCLL-FCI may have somewhat lower risk if the higher allowable flow velocity translates to a lower steady state T concentration in the PbLi. Continued R&D on efficient T extraction processes are needed for both designs. 

## **8.2 General Technology Assessment** 

Both concepts have similar low levels of technology readiness and R&D requirements as early phase conceptual design. Prototypes have not yet been built or tested, but scaled models will eventually be tested on ITER. 

## **9. KEY FINDINGS AND RECOMMENDATIONS** 

## **9.1 Findings** 

The overall systems level comparison of TBB concepts supports the U.S. R&D community’s decision to focus on the Dual Coolant Lithium Lead design with Flow Channel Inserts (DCLLFCI) as the top candidate. It is one of several concepts that have a good chance of meeting all the system requirements, and it has some potential advantages, although not dramatic, over competing concepts in terms of its eventual performance. 

## **9.2 Recommendations** 

All concepts are in early stages of development, and component level testing in a fusion relevant environment will not take place until the Test Blanket Modules are deployed in ITER. Therefore, it is prudent to 1) continue along the current path of also conducing R&D on a solid breeder blanket concept, and 2) devote some portion of the R&D effort to less developed, innovative ideas that have the potential for addressing key issues with the mainline approaches or improving predicted performance. Most Major fusion programs, including the EU, Japan, Korea and China, recognize the risk of down selecting to a single concept at this stage; they are all conducting R&D on different breeders (liquid and solid) and coolants (water, gas and liquid metal). Even with limited funding it is recommended that the U.S. strive to do the same. 

# Appendix A

## Tritium Breeding Blanket Data Sheets

## **Korean Helium Cooled Ceramic Reflector (HCCR)** 

**Proponent:** South Korea 

**Breeding Material:** Li4SiO4 pebble bed (Li2TiO3 alternate) 

**Reflector:** Graphite pebble bed (SiC coated) 

**Coolant** : Helium at 8 MPa 

**Structural Material:** Korean Reduced Activation Ferrritic/ Martensitic (KO-RAFM) steel 

## **Tritium Recovery** : He purge 

- SiC coated, graphite pebble bed reflector improves neutron economy (reduced leakage) and thus reduces the amount of Be multiplier needed. This is a cost and resource management advantage. 

- Basis of ITER TBM design 

Seungyon Cho et al., “Design and R&D progress of Korean HCCR TBM,” _Fusion Engineering and Design_ ,” **89** , p. 1137 (2014). 

Seungyon Cho et al., “Overview of Helium Cooled Ceramic Reflector Test Blanket Module Development in Korea,” _Fusion Engineering and Design_ , **88** , p. 621 (2013). 

![](images/tmpub8jbof1.pdf-0033-13.png)

Concept of the HCCR TBM (a), and a sub-module (b) 

## **China Helium Cooled Ceramic Breeder (HCCB)** 

## **Proponent:** China 

**Breeding Material:** Li4SiO4 pebble bed (enriched to 80%[6] Li) 

**Coolant** : Helium 

**Structural Material:** China’s Reduced Activation Ferritic Martensitic (RAFM) CLF-1 steel 

## **Tritium Recovery** : He purge 

- Primary option for China’s ITER TBM design 

K.M. Feng et al., “New progress on design and R&D for solid breeder test blanket module in China,” _Fusion Engineering and Design_ ,” in press (2014). 

Paper Highlights: 

- The new progress on design and R&D of Chinese solid breeder TBM are introduced. 

- The mock-up fabrication and component tests for Chinese HCCB TBM have being developed. 

- The neutron multiplier Be pebbles, tritium breeder Li4SiO4 pebbles, and structure material CFL-1 are being prepared. 

- The fabrication of 1/3 sized mock-up is being carried-out. 

- The key technology development is proceeding to the large-scale mock-up fabrication. 

![](images/tmpub8jbof1.pdf-0034-16.png)

Structural view of sub-module. 

## **Dual Cooled Lithium Lead (DCLL) with Flow Channel Inserts (FCI)** 

**Proponent:** US (also EU) 

**Breeding Material:** PbLi (84 wt% Pb, 16 wt% Li, enriched to 90%[6] Li) 

**Multiplier:** Pb in PbLi 

**Coolant** : Helium (8 MPa) for first wall and structures, PbLi secondary coolant 

## **Structural Material:** F82H RAFM 

**Tritium Recovery** : Recovered from slip stream off PbLi coolant via vacuum pumping on permeation windows. 

- SiC Flow channel insert will allow high PbLi coolant outlet temperature in power plant designs giving improved thermal efficiency 

Damien Sutevski, Sergey Smolentsev, Mohamed Abdou, “3D numerical study of pressure equalization in MHD flow in a rectangular duct with insulating flow channel insert, _Fusion Engineering and Design_ **89** , 1370 (2014). 

![](images/tmpub8jbof1.pdf-0035-10.png)

## **He Cooled Lithium Lead (HCLL)** 

**Proponent:** EU 

**Breeding Material:** PbLi (84 wt% Pb, 16 wt% Li, enriched to 90%[6] Li) 

**Multiplier:** Pb in PbLi 

**Coolant** : Helium (8 MPa) for first wall, structures, and PbLi breeder 

**Structural Material:** Eurofer RAFM 

**Tritium Recovery** : Recovered from PbLi that slowly circulates out of TBB via vacuum pumping on permeation windows. 

L.V. Boccaccini, et al., “Present status of the conceptual design of the EU Test Blanket Systems, _Fusion Engineering and Design_ (2011), 

doi:10.1016/j.fusengdes.2011.02.036. 

![](images/tmpub8jbof1.pdf-0036-10.png)

## **Helium Cooled Pebble Bed (HCPB)** 

**Proponent:** EU 

**Breeding Material:** Li4SiO4 (30% 6Li) or Li2TiO3 (60%[6] Li) 

**Coolant** : Helium (8 MPa) 

**Structural Material:** Eurofer RAFM 

**Tritium Recovery** : He purge through pebble bed in blanket 

- One of two top candidates for EU Demo 

L.V. Boccaccini, et al., “Present status of the conceptual design of the EU Test Blanket Systems, _Fusion Engineering and Design_ (2011), 

doi:10.1016/j.fusengdes.2011.02.036. 

![](images/tmpub8jbof1.pdf-0037-11.png)

## **Water Cooled Ceramic Breeder (WCCB)** 

**Proponent:** Japan (back-up concept for EU) 

**Breeding Material:** Li2TiO3 (30%[6] Li) 

**Coolant** : Pressurized water 

**Structural Material:** FH82 RAFM 

**Tritium Recovery** : He purge 

- T permeation barriers used to prevent T permeation into water 

- Considered for Demo 

M. Enoeda et al., “Development of the Water Cooled Ceramic Breeder Test Blanket Module in Japan,” _Fusion Engineering and Design_ ,” **87** , p. 1363 (2012). 

![](images/tmpub8jbof1.pdf-0038-11.png)

Configuration of the WCCB-TBM 

## **Appendix B** 

## **Comparison Criteria** 

The comparison criterial used in this report are listed here (See Table 5.5, Section 5): 

1. Tritium Supply (TS): Produce more T fuel than is consumed and allow for continuous recovery 

2. Power Handling (POW): Absorb fusion power and make it available to the power conversion system at high temperature 

3. Costs (COST): Have acceptable capital and operating costs 

4. Safety (SAF): Operate safely in normal and off-normal conditions 

5. Reliability (REL): Potential for high reliability leading to high availability 

6. Environmental (ENV): Low environmental impact from induced radioactivity waste 

7. Tritium extraction (TEX): Ease of tritium recovery from breeder 

8. Fabricability (FAB): Can be fabricated with standard proven methods 

## S. Malang et al. used the following criteria in Ref. B-1: 

- A. Engineering complexity of the design (EC) 

- B. Magneto-hydrodynamic issues (MHD) 

- C. Tritium extraction and control (TXC) 

- D. Compatibility issues (CI) 

- E. Pumping power (PP) 

- F. Achievable efficiency in the power conversion system (EFF) 

- G. Required Li-6 enrichment to achieve tritium self-sufficiency (TSS) 

- H. Potential for liquid metal (LM)/water reaction (LMR) 

- I. Required extrapolation of the present technologies (development risks) DR 

- J. Potential for extrapolation to more advanced concepts (AC) 

Table B.1 shows how the criterial used by Malang map onto the criteria used in this report. As indicated, everything considered by Malang is included by one or more of the top level criteria used here. 

B-1 

**Table B.1 Mapping Malang Criteria to Meier Criteria** 

|**Meier criteria**|**1. TS**|**2. POW**|**3. COST**|**4. SAF**|**5. REL**|**6. ENV**|**7. TEX**|**8. FAB**|
|---|---|---|---|---|---|---|---|---|
|**Malang criteria**|||||||||
|**A. EC**|||X||X|||X|
|**B. MHD**||X|||||||
|**C. TXC**|X|||X|||X||
|**D. CI**||X||||X||x|
|**E. PP**||X|||X||||
|**F. EFF**||X|||||||
|**G. TSS**|X||X||||||
|**H. LMR**||||X|||||
|**I. DR**||||||||x|
|**J. AC**||X|||||||

## **Reference** 

- B-1 S. Malang, A. R. Raffray, and N. B. Morley, “An example pathway to a fusion power plant system based on lead–lithium breeder: Comparison of the dual-coolant lead–lithium (DCLL) blanket with the helium-cooled lead–lithium (HCLL) concept as initial step,” _Fusion Eng. Des._ , vol. 84, no. 12, pp. 2145–2157, Dec. 2009. 

B-2 

## **Appendix C** 

## **Bibliography of Articles Related to Tritium Breeding Blankets** 

M. Abdou, D. Sze, C. Wong, M. Sawan, A. Ying1, N. B. Morley, “U.S. Plans and Strategy for ITER Blanket Testing,” _Fusion Sci. Technol._ , vol. 47, pp. 475–487, 2005. 

M. Abdou, APEX Team, A. Ying, N. Morley, K. Gulec, S. Smolentsev, M. Kotschenreuther, S. Malang, S. Zinkle, T. Rognlien, P. Fogarty, B. Nelson, R. Nygren, K. McCarthy, M. . Youssef, N. Ghoniem, D. Sze, C. Wong, M. Sawan, H. Khater, R. Woolley, R. Mattas, R. Moir, S. Sharafat, J. Brooks, a Hassanein, D. Petti, M. Tillack, M. Ulrickson, and T. Uchimoto, “On the exploration of innovative concepts for fusion chamber technology,” _Fusion Eng. Des._ , vol. 54, no. 2, pp. 181–247, Feb. 2001. 

A. Aures, L. W. Packer, and S. Zheng, “Tritium self-sufficiency of HCPB blanket modules for DEMO considering time-varying neutron flux spectra and material compositions,” _Fusion Eng. Des._ , vol. 88, no. 9–10, pp. 2436–2439, Oct. 2013. 

L. V. Boccaccini, a. Aiello, O. Bede, F. Cismondi, L. Kosek, T. Ilkei, J.-F. Salavy, P. Sardain, and L. Sedano, “Present status of the conceptual design of the EU test blanket systems,” _Fusion Eng. Des._ , vol. 86, no. 6–8, pp. 478–483, Oct. 2011. 

B. Bornschein, C. Day, D. Demange, and T. Pinna, “Tritium management and safety issues in ITER and DEMO breeding blankets,” _Fusion Eng. Des._ , vol. 88, no. 6–8, pp. 466–471, Oct. 2013. 

C. Bustreo, G. Casini, G. Zollino, T. Bolzonella, and R. Piovan, “FRESCO, a simplified code for cost analysis of fusion power plants,” _Fusion Eng. Des._ , vol. 88, no. 12, pp. 3141–3151, Dec. 2013. 

D. Carloni and L. Boccaccini, “Requirements for helium cooled pebble bed blanket and R&D activities,” _Fusion Eng. Des._ , 2014. 

S. Cho, M.-Y. Ahn, D. W. Lee, Y.-H. Park, E. H. Lee, J. S. Yoon, T. K. Kim, C. W. Lee, Y.-H. Yoon, S. K. Kim, H. G. Jin, K. I. Shin, Y. Il Jung, Y. H. Jeong, Y. O. Lee, D. Y. Ku, C.-S. Kim, S. C. Park, I.-K. Yu, and K. Jung, “Overview of Helium Cooled Ceramic Reflector Test Blanket Module development in Korea,” _Fusion Eng. Des._ , vol. 88, no. 6–8, pp. 621–625, Oct. 2013. 

S. Cho, M. Ahn, D. Lee, and Y. Park, “Design and R&D progress of Korean HCCR TBM,” _Fusion Eng. Des._ , 2014. 

G. Dell’Orco, A. Ancona, and P. Di Maio, “Experimental tests on Li-ceramic breeders for the helium cooled pebble bed (HCPB) blanket design,” _Fusion Eng. Des._ , vol. 69, pp. 233–240, 2003. 

M. Enoeda, H. Tanigawa, T. Hirose, S. Suzuki, K. Ochiai, C. Konno, Y. Kawamura, T. Yamanishi, T. Hoshino, M. Nakamichi, H. Tanigawa, K. Ezato, Y. Seki, A. Yoshikawa, D. Tsuru, and M. Akiba, “Development of the Water Cooled Ceramic Breeder Test Blanket Module in Japan,” _Fusion Eng. Des._ , vol. 87, no. 7–8, pp. 1363–1369, Aug. 2012. 

K. Feng, G. Zhang, G. Hu, and Y. Chen, “New progress on design and R&D for solid breeder test blanket module in China,” _Fusion Eng. Des._ , 2014. 

K. Feng, G. Zhang, G. Hu, and Y. Chen, “New progress on design and R&D for solid breeder test blanket module in China,” _Fusion Eng. Des._ , 2014. 

F. Franza and A. Ciampichetti, “Sensitivity Study for Tritium Permeation in Helium-Cooled Lead-Lithium DEMO Blanket with the FUS-TPC Code,” _Fusion Sci. Technol._ , pp. 631–635, 2013. 

M. Fütterer, H. Albrecht, and P. Giroux, “Tritium technology for blankets of fusion power plants,” _Fusion Eng. Des._ , vol. 50, pp. 735–743, 2000. 

A. M. Garofalo, M. a. Abdou, J. M. Canik, V. S. Chan, A. W. Hyatt, D. N. Hill, N. B. Morley, G. a. Navratil, M. E. Sawan, T. S. Taylor, C. P. C. Wong, W. Wu, and A. Ying, “A Fusion Nuclear Science Facility for a fast-track path to DEMO,” _Fusion Eng. Des._ , Apr. 2014. 

L. M. Giancarli, M. Abdou, D. J. Campbell, V. a. Chuyanov, M. Y. Ahn, M. Enoeda, C. Pan, Y. Poitevin, E. Rajendra Kumar, I. Ricapito, Y. Strebkov, S. Suzuki, P. C. Wong, and M. Zmitko, “Overview of the ITER TBM Program,” _Fusion Eng. Des._ , vol. 87, no. 5–6, pp. 395–402, Aug. 2012. 

B. G. Hong, D. W. Lee, S. J. Wang, Y. Kim, W. K. In, and K. H. Yoon, “Basic concepts of DEMO and a design of a helium-cooled molten lithium blanket for a testing in ITER,” _Fusion Eng. Des._ , vol. 82, no. 15–24, pp. 2399–2405, Oct. 2007. 

Y. Kang and T. Terai, “Moderate tritium properties in lithium–tin alloy as a liquid breeder/ coolant,” _Fusion Eng. Des._ , vol. 81, no. 1–7, pp. 519–523, Feb. 2006. 

V. Kapyshev, I. Danilov, I. Kartashev, V. Kovalenko, a. Leshukov, V. Poliksha, a. Razmerov, Y. Strebkov, M. Sviridenko, E. Trusova, N. Vladimirova, and a. Kalashnikov, “Initial design and test of the tritium breeder monitoring system for the lead-lithium cooled ceramic breeder (LLCB) module of the ITER,” _Fusion Eng. Des._ , vol. 88, no. 9–10, pp. 2293–2297, Oct. 2013. 

K. Kim, H. C. Kim, S. Oh, Y. S. Lee, J. H. Yeom, K. Im, G.-S. Lee, G. Neilson, C. Kessel, T. Brown, and P. Titus, “A preliminary conceptual design study for Korean fusion DEMO reactor,” _Fusion Eng. Des._ , vol. 88, no. 6–8, pp. 488–491, Oct. 2013. 

Y. Kim, B. G. Hong, and C. H. Kim, “A neutronic investigation of He-cooled liquid Li-breeder blankets for fusion power reactor,” _Fusion Eng. Des._ , vol. 75–79, pp. 1067–1070, Nov. 2005. 

I. Kirillov, “Lithium cooled blanket of RF DEMO reactor,” _Fusion Eng. Des._ , vol. 49–50, pp. 457–465, 2000. 

M. Kwon, Y. S. Na, J. H. Han, S. Cho, H. Lee, I. K. Yu, B. G. Hong, Y. H. Kim, S. R. Park, and H. T. Seo, “A strategic plan of Korea for developing fusion energy beyond ITER,” _Fusion Eng. Des._ , vol. 83, no. 7–9, pp. 883–888, Dec. 2008. 

D. W. Lee, B. G. Hong, S. K. Kim, and Y. Kim, “Design and preliminary safety analysis of a helium cooled molten lithium test blanket module for the ITER in Korea,” _Fusion Eng. Des._ , vol. 83, no. 7–9, pp. 1217–1221, Dec. 2008. 

D. Lee, J. Yoon, K. Jung, and S. Kim, “Preliminary Study on the Melting and Reaction of Liquid Metal Breeders for a Korean Test Blanket Module in ITER,” _Fusion Sci. Technol._ , pp. 171–179, 2012. 

E. Lee, S. Kim, J. Yoon, D. Lee, and S. Cho, “Progress of Tritium Extraction and Measurement Methods Development from Liquid Breeder Blanket in Korea,” _Fusion Sci. Technol._ , pp. 77–82, 2012. 

A. Li Puma, J. L. Berton, B. Brañas, L. Bühler, J. Doncel, U. Fischer, W. Farabolini, L. Giancarli, D. Maisonnier, P. Pereslavtsev, S. Raboin, J.-F. Salavy, P. Sardain, J. Szczepanski, and D. Ward, “Breeding blanket design and systems integration for a helium-cooled lithium–lead fusion power plant,” _Fusion Eng. Des._ , vol. 81, no. 1–7, pp. 469–476, Feb. 2006. 

A. Li Puma, C. Bachmann, L. V Boccaccini, P. Norajitra, G. Aiello, J. Aubert, D. Carloni, and C. Mistrangelo, “Design and Development of Demo Blanket Concepts in Europe,” Presented at ISFNT-11, Barcelona, Sept. 17, 2013. 

S. Malang, M. Tillack, C.P.C. Wong, N. Morley, S. Smolentsev, “Development of the lead lithium (DCLL) blanket concept,” _Fusion Sci. Technol._ , vol. 60, pp. 249–256, 2011. 

S. Malang, a. R. Raffray, and N. B. Morley, “An example pathway to a fusion power plant system based on lead–lithium breeder: Comparison of the dual-coolant lead–lithium (DCLL) blanket with the helium-cooled lead–lithium (HCLL) concept as initial step,” _Fusion Eng. Des._ , vol. 84, no. 12, pp. 2145–2157, Dec. 2009. 

S. Malang and R. Mattas, “Comparison of lithium and the eutectic lead-lithium alloy, two candidate liquid metal breeder materials for self-cooled blankets,” _Fusion Eng. Des._ , vol. 27, pp. 399–406, 1995. 

H. Matsuura, H. Nakaya, Y. Nakao, S. Shimakawa, M. Goto, S. Nakagawa, and M. Nishikawa, “Evaluation of tritium production rate in a gas-cooled reactor with continuous tritium recovery system for fusion reactors,” _Fusion Eng. Des._ , vol. 88, no. 9–10, pp. 2219–2222, Oct. 2013. 

R . Mattas, D. Smith, C. Reed, and J. Park, “Results of R and D for lithium/vanadium breeding blanket design,” _Fusion Eng. Des._ , vol. 39–40, pp. 659–668, 1997. 

B. Merrill, “Challenges Leading to a FNSF.” Presented to FESAC Materials Science Panel, Dec. 7, 2011. 

E.A. Mogahed and G.L Kulcinski, “Bibliography of a Promising Tritium Breeding Material - Pb83Li17,” Univ. of Wisc. Report UWFDM-994, 1995. 

H. Moriyama, S. Tanaka, and D. Sze, “Tritium recovery from liquid metals,” _Fusion Eng. Des._ , vol. 28, pp. 226–239, 1995. 

K. Okano, G. Federici, and K. Tobita, “DEMO design activities in the broader approach under Japan/EU collaboration,” _Fusion Eng. Des._ , pp. 4–8, Apr. 2014. 

Y. Park, I. Yu, M. Ahn, S. Cho, and D. Ku, “Fabrication OF Li4SiO4 Pebbles using Slurry Droplet Wetting Method for Solid Breeding Material,” _Fusion Sci. Technol._ , pp. 185–189, 2012. 

Y. Poitevin, “The Tritium Breeding Blankets for Fusion Reactors - A key component for sustainability of Fusion Energy,” Presentation at Swiss Nuclear Forum, March 23, 201. 

Y. Poitevin, L. V. Boccaccini, M. Zmitko, I. Ricapito, J.-F. Salavy, E. Diegele, F. Gabriel, E. Magnani, H. Neuberger, R. Lässer, and L. Guerrini, “Tritium breeder blankets design and technologies in Europe: Development status of ITER Test Blanket Modules, test & qualification strategy and roadmap towards DEMO,” _Fusion Eng. Des._ , vol. 85, no. 10–12, pp. 2340–2347, Dec. 2010. 

Y. Poitevin, L. V. Boccaccini, M. Zmitko, I. Ricapito, J.-F. Salavy, E. Diegele, F. Gabriel, E. Magnani, H. Neuberger, R. Lässer, and L. Guerrini, “Tritium breeder blankets design and technologies in Europe: Development status of ITER Test Blanket Modules, test & qualification strategy and roadmap towards DEMO,” _Fusion Eng. Des._ , vol. 85, no. 10–12, pp. 2340–2347, Dec. 2010. 

Y. Poitevin and L. Boccaccini, “The European breeding blankets development and the test strategy in ITER,” _Fusion Eng. Des._ , vol. 79, pp. 741–749, 2005. 

A. R. Raffray, “Future Developments : Blanket Technology and Material Engineering for FNT.” pp. 1–23, 2013. 

A.R. Raffray, S. Malang, L. El-Guebaly, X. Wang, “Ceramic Breeder Blanket for ARIES-CS,” _Fusion Sci. Technol._ , vol. 47, no. May, pp. 1068–1073, 2005. 

A. Raffray, M. Akiba, V. Chuyanov, L. Giancarli, and S. Malang, “Breeding blanket concepts for fusion and materials requirements,” _J. Nucl. Mater._ , vol. 307–311, pp. 21–30, Dec. 2002. 

I. Ricapito, A. Ciampichetti, and R. Lässer, “Tritium Extraction from Liquid Pb-16Li: A Critical Review of Candidate Technologies for ITER and DEMO Applications,” _Fusion Sci. Technol._ , pp. 1159–1162, 2011. 

N. Roux, J. Avon, a. Floreancing, J. Mougin, B. Rasneur, and S. Ravel, “Low-temperature tritium releasing ceramics as potential materials for the ITER breeding blanket,” _J. Nucl. Mater._ , vol. 233–237, pp. 1431–1435, Oct. 1996. 

N. Roux, S. Tanaka, C. Johnson, and R. Verrall, “Ceramic breeder material development,” _Fusion Eng. Des._ , vol. 41, no. 1–4, pp. 31–38, Sep. 1998. 

S. Sharafat, N. Ghoniem, M. Sawan, A. Ying, and B. Williams, “Breeder foam: an innovative low porosity solid breeder material,” _Fusion Eng. Des._ , vol. 81, no. 1–7, pp. 455–460, Feb. 2006. 

S. Sharafat and N. Ghoniem, “Cellular foams: a potential innovative solid breeder material for fusion applications,” _Fusion Sci. Technol._ , vol. 47, no. May, pp. 6–10, 2005. 

K. I. Shin, D. W. Lee, E. H. Lee, S.-K. Kim, J. S. Yoon, and S. Cho, “Design and performance analysis of structural components for a Korean He Cooled Ceramic Reflector TBM in ITER,” _Fusion Eng. Des._ , vol. 88, no. 9–10, pp. 1866–1871, Oct. 2013. 

D. L. Smith, C. C. Baker, and D. A. I. K. A. I. Sze, “Overview of the Blanket Comparison And Selection Study,” _Fusion Technol._ , vol. 8, pp. 10–44, 1985. 

Y. Someya, H. Takase, H. Utoh, K. Tobita, C. Liu, and N. Asakura, “Simplification of blanket system for SlimCS fusion DEMO reactor,” _Fusion Eng. Des._ , vol. 86, no. 9–11, pp. 2269–2272, Oct. 2011. 

D. Stork, “Materials R & D for a timely DEMO: Key Findings and Recommendations of the EU Roadmap Materials Assessment Group,” Presented at ISFNT-11, Barcelona, Sept. 16-20, 2013. 

K. Tobita, S. Nishio, A. Saito, and M. Enoeda, “Water-cooled solid breeding blanket for DEMO,” _Proceeding ITC18, 2008_ , pp. 285–288, 2009. 

S. Tosti and A. Pozio, “Hydrogen solubility and electrical resistivity measurements of hydrogenated Pb-Li,” 2013. 

C. P. C. Wong, M. Abdou, M. Dagher, Y. Katoh, R. J. Kurtz, S. Malang, E. P. Marriott, B. J. Merrill, K. Messadek, N. B. Morley, M. E. Sawan, S. Sharafat, S. Smolentsev, D. K. Sze, S. Willms, a. Ying, and M. Z. Youssef, “An overview of the US DCLL ITER-TBM program,” _Fusion Eng. Des._ , vol. 85, no. 7–9, pp. 1129–1132, Dec. 2010. 

C. P. C. Wong, S. Malang, M. Sawan, M. Dagher, S. Smolentsev, B. Merrill, M. Youssef, S. Reyes, D. K. Sze, N. B. Morley, S. Sharafat, P. Calderoni, G. Sviatoslavsky, R. Kurtz, P. Fogarty, S. Zinkle, and M. Abdou, “An overview of dual coolant Pb–17Li breeder first wall and blanket concept development for the US ITER-TBM design,” _Fusion Eng. Des._ , vol. 81, no. 1–7, pp. 461–467, Feb. 2006. 

I. Yamamoto, T. Nishitani, A. Sagara, “Overview of Recent Japanese Activities and Plans in Fusion Technology,” _Fusion Sci. Technol._ , vol. 52, pp. 347–356, 2007. 

A. Ying, J. Reimann, L. Boccaccini, M. Enoeda, M. Kamlah, R. Knitter, Y. Gan, J. G. Van Der Laan, L. Magielsen, P. A. Di Maio, G. D. Orco, R. Kumar, J. T. Van Lew, H. Tanigawa, and S. Van Til, “Status of ceramic breeder pebble bed thermo-mechanics R&D and impact on breeder material mechanical strength,” _Fusion Eng. Des._ , vol. 87, no. 7–8, pp. 1130–1137, 2012. 

D. Youchison and S. N. Laboratories, “Flow Instabilities in Helium-cooled Porous Media and the Helium Micro-Jet Array alternative to the HEMJ” Presented at US-Japan High Heat Flux Component Workshop, Livermore, Jan. 8, 2014. 

S. J. Zinkle, J. P. Blanchard, R. W. Callis, C. E. Kessel, R. J. Kurtz, P. J. Lee, K. a. McCarthy, N. B. Morley, F. Najmabadi, R. E. Nygren, G. R. Tynan, D. G. Whyte, R. S. Willms, and B. D. Wirth, “Fusion materials science and technology research opportunities now and during the ITER era,” _Fusion Eng. Des._ , Mar. 2014. 

H. Zohm, “Assessment of DEMO challenges in technology and physics,” _Fusion Eng. Des._ , vol. 88, no. 6–8, pp. 428–433, Oct. 2013. 

