---
source: "https://www.osti.gov/servlets/purl/1305833"
source_type: "url"
extracted_at: "2026-04-20T00:07:42.481119+00:00"
content_hash_sha256: "940a33485ae52213b5812c06052156cb5b11c35b84dbfe803e2855cd4512aaf3"
backend: "pdf_pipeline"
---

LLNL-TR-652984 

![](images/tmphfztki6w.pdf-0001-01.png)

Tritium Breeding Blanket for a Commercial Fusion Power Plant -A System Engineering Assessment 

W. R. Meier April 10, 2014 

## **Disclaimer** 

This document was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor Lawrence Livermore National Security, LLC, nor any of their employees makes any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or Lawrence Livermore National Security, LLC. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or Lawrence Livermore National Security, LLC, and shall not be used for advertising or product endorsement purposes. 

This work performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. 

**LLNL-TR-652984** 

## **Tritium Breeding Blanket for a Commercial Fusion Power Plant - A System Engineering Assessment** 

## **Wayne Meier LLNL** 

## **April 14, 2014** 

This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. 

## **Contents** 

1.  Executive Summary 

2.  Mission Description 

3.  System Operational context and Reference Operational Architecture 

4.  System Driver and Constraints 

5.  Operational Scenarios 

6.  Implementation Concept Selected and Rationale 

7.  Proposed System Operational Architecture 

8.  System Requirements 

9.  Organizational and Business Impact 

10. Risks and Technology Readiness Assessment 

## **1. EXECUTIVE SUMMARY** 

The goal of developing a new source of electric power based on fusion has been pursued for decades. If successful, future fusion power plants will help meet growing world-wide demand for electric power. A key feature and selling point for fusion is that its fuel supply is widely distributed globally and virtually inexhaustible. Current world-wide research on fusion energy is focused on the deuterium-tritium (DT for short) fusion reaction since it will be the easiest to achieve in terms of the conditions (e.g., temperature, density and confinement time of the DT fuel) required to produce net energy. A key component of all DT fusion power plants will be a tritium breeding blanket (TBB) that has two key functions: 

- 1) produce more (just slightly) tritium fuel than is consumed, and 

- 2) absorb the fusion power and make it available to a power conversion cycle (to produce electricity). 

Over the past decades countless studies have examined various concepts for TBBs for both magnetic fusion energy (MFE) and inertial fusion energy (IFE). At this time, the key organizations involved are government sponsored research organizations world-wide. The near-term focus of the MFE community is on the development of TBB mock-ups to be tested on the ITER tokamak currently under construction in Caderache France. TBB concepts for IFE tend to be different from MFE primarily due to significantly different operating conditions and constraints. 

This report focuses on longer-term commercial power plants where the key stakeholders include: electric utilities, plant owner and operator, manufacturer, regulators, utility customers, and in-plant subsystems including the heat transfer and conversion systems, fuel processing system, plant safety systems, and the monitoring control systems. 

In addition to meeting the two functions listed above, key stakeholder expectations include: safe operation in normal and off-normal conditions, high reliability, maintainability, high efficiency (e.g., operate at high temperature for efficiency power conversion and with low input power needs), low environmental impacts in terms of radioactive and other waste streams (over the life of the plant and after shutdown/decommissioning). 

The TBB concept is explained in more detail in the body of the report, but its essential functional features are depicted in Fig. 1.1. The primary input is power from the fusion reactions (both surface heating and nuclear heating resulting from fusion neutron reactions with blanket material). The primary outputs are thermal power and tritium. The vast majority of the blanket thermal power is removed by a blanket coolant; thus the TBB requires a coolant inlet and outlet. A small fraction of the thermal power flows to surrounding components such as the shield via low energy neutron leakage, gamma radiation and thermal radiation. Tritium is created in the TBB via nuclear reaction with lithium (see Introduction) and is continuously removed from the blanket. Various options for this recovery have been proposed and depend strongly on the TBB design details; in some cases T is removed with the coolant flow while other designs provide a dedicated system to capture and remove the T from the TBB. A schematic of the top level inputs and outputs of the TBB is shown in Fig. 1.2. 

![Fig. 1.1. Essential functions of the tritium breeding blanket](images/tmphfztki6w.pdf-0006-00.png)

![Fig. 1.2. Schematic of level inputs and outputs of the TBB.](images/tmphfztki6w.pdf-0006-02.png)

The TBB is shown schematically in the operational context of a Tokamak power plant in Fig. 1.3. The TBB surrounds the fusion plasma and is surrounded by shielding and the magnetic coils that confine the plasma. This figure indicates the flow of DT fuel into the plasma, the D,T and He recovery from plasma exhaust (white pipe) and T extraction from the TBB (vertical green pipe not labeled). The coolant loops through the blanket provide heat to drive the turbine generator. 

The scope of this report is limited to TBBs for an MFE Tokamak. World-wide there are less than a dozen designs actively being developed. Here we focus on one of the leading designs being developed by the US called the Dual-Cooled, Lithium Lead (DCLL) breeding blanket and show how it could meet expectations for future electric power utility owner/operators. 

![Fig. 1.3. Schematic of the power core of tokamak power plant indicating the location of the TBB (adapted from mpg.de)](images/tmphfztki6w.pdf-0007-00.png)

## **2. MISSION DESCRIPTION** 

## **2.1 Introduction to the Essential Functions of the TBB** 

As previously noted, current world-wide research on fusion energy is focused on the deuterium-tritium (DT for short) fusion reaction since it will be the easiest to achieve in terms of the conditions (e.g., temperature, density and confinement time of the DT fuel) required needed to produce net energy. Deuterium ([2] H or D) is a stable isotope of hydrogen with a single neutron in the nucleus (atomic mass ~ 2); it occurs naturally and can be extracted from water. Tritium ([3] H, or T) is also an isotope of hydrogen with two neutrons in the nucleus giving it an atomic mass of ~3. Tritium is radioactive, decaying by beta emission (which transforms this hydrogen isotope into a helium isotope, denoted[3] He) with a half-life of 12.3 years. Due to this relatively short half-life, there is no natural abundance of T. Therefore, fusion power plants based on the DT reaction must produce their own T. The process is referred to as tritium breeding, and the component of the fusion power plant that carries out this function is called the tritium breeding blanket (TBB), or breeding blanket, or simply blanket. 

To understand how it is possible for a power plant to create its own fuel, we need to look at the nuclear reactions involved. The DT fusion reaction is 

![](images/tmphfztki6w.pdf-0008-04.png)

The nuclear reaction between D and T produces a helium nucleus (also called an alpha particle,  ) and a neutron. In the process energy is released that appears in the form of kinetic energy of the alpha particle and neutron. To create tritium to provide a continuous supply of fuel, the neutron must initiate nuclear reactions with lithium (an alkali metal that is abundantly available in the earth’s crust). Lithium has two isotope,[6] Li and[7] Li and both have T producing reactions with neutrons emitted by the fusion reaction: 

![](images/tmphfztki6w.pdf-0008-06.png)

![](images/tmphfztki6w.pdf-0008-07.png)

Both reactions produce a new T and a helium nucleus. The reaction with[7] Li also emits another lower energy neutron (n') that can subsequently produce more reactions with[6] Li. 

## _**The TBB must produce at least as much T as is consumed in the fusion reactions.**_ 

The ratio of T atoms produced in the blanket to T atoms consumed in the fusion reactions is called the tritium breeding ratio, TBR. Breeding blanket designs typically have a goal of breeding an extra10% (TBR = 1.10) to account for uncertainties in the predicted blanket performance, supply T start-up inventory for new power plants, account for radioactive decay, and account for losses in the fuel processing systems (losses to the environment must be extremely low). 

To accomplish the requirement of obtaining a TBR greater than 1.1, the TBB must completely surround the fusion power source, with the exception of areas required for plasma heating, vacuum pumping, and in the case of IFE, beam port entry. As a result, the TBB absorbs nearly all the fusion power and this power must be made available to a heat transfer systems that transports thermal power to a power conversion systems to produce electricity. This power flow is shown schematically in Fig. 3. 

The fusion power is delivered to the TBB as both surface heating and penetrating nuclear heating. The structure that is directly exposed to the fusion source is called the first wall and is considered an integral part of the TBB. It must absorb and conduct the surface heat to the blanket coolant. Fusion neutrons penetrate into the blanket a cause heating due to nuclear reactions with blanket materials (nuclear heating), the most important of which are the tritium breeding reactions with lithium. In order for the plant to produce electric power, the blanket thermal power must be removed at a temperature that is high enough to drive the selected power conversion cycle. Design being considered typically operate with blanket coolant outlet temperature greater than 400 C. 

_**The TBB must absorb the fusion power and make it available to the power conversion systems at high temperature.**_ 

## **2.2 Active Stakeholders** 

This section covers the active stakeholders. In this report we take the context as the future where fusion power has been proven feasible and it has become an option for a commercial electric power plant. That is, we are past the government sponsored R&D phase. 

## **2.2.1 Utility Owner/Operator** 

We assume that it is the electric utility makes the decision to build and operate the fusion power plant as part of its energy supply mix. This is clearly a key stakeholder since without a positive decision on their part the plant, including the TBB, is not built. Top level expectations of the utility owner/operator include the ability to produce and sell electricity in an economically competitive, reliable, safe and environmentally acceptable manner. In order to meet these top-level expectations, the TBB is expected to: 

- Supply the tritium fuel 

- Have an acceptable capital cost (as part of the overall plant capital cost) 

- Have an acceptable operating cost (fixed and variable) 

- Facilitate high efficiency power conversion 

- Have high availability 

   - Reliability (low unplanned outages) 

   - Maintainability (short maintenance times) 

- Operate safely in normal and off-normal conditions including (start-up and shut-down) 

- Have low radioactive and hazardous waste streams (during plant operations and at end of plant life) 

## **2.2.2 Plant Maintenance Personnel and Equipment** 

During the life of the power plant, the TBB will certainly require repair and/or replacement. Neutrons from the fusion reaction will cause blanket materials to become radioactive over time to the point that hands-on maintenance will not be possible. Therefore, the TBB must be designed to allow access and repair by remote maintenance equipment. Ideally the expectations would include easy access for either in situ repair or rapid removal and replacement with new or refurbished blanket components. 

## **2.2.3 Fusion Plasma** 

As previously noted the TBB nearly completely surrounds the fusion plasma with the exception of ports needed for heating, vacuum pumping, plasma fueling and exhaust at the divertor. As such, the geometry of the TBB must conform to the geometry of the plasma which is set by the magnetic configuration.  The inner surface of the TBB is called the first wall and it is directly exposed to the fusion plasma. Plasma interactions with the first wall can cause first wall material to be expelled into the plasma core. Expectations here are that the TBB blanket can be designed to conform to the plasma geometry and that the first wall design and operating conditions do not prevent the plasma from behaving as expected. 

## **2.2.4 Heat Transfer System** 

The heat transfer system also interacts directly with the TBB. Some means must be provided to extract the fusion power that is deposited in the blanket and deliver the power to a power conversion system. Various liquid and gases coolants are being considered. The heat transfer fluid is delivered through an inlet connection (typically a pipe), flows through the blanket as it is heated and then exits through an exit connection. The expectation is that the TBB can be design to allow enough heat transfer area between the blanket structure and the coolant to all for efficient heat transfer under reasonable coolant flow conditions (e.g., pressure, flow velocity, temperature change from inlet to outlet). 

## **2.2.5 Tritium Processing System** 

Tritium that is bred in the blanket must be continuously removed and delivered to the tritium processing system (TPS). Various approaches have been considered and deemed feasible. In some cases the T is removed as a part of the coolant flow stream, while other designs provide a dedicated method for T extraction, for example a flow stream of He that picks up T as it flows through the breeder material. The expectation is that the TBB can be designed to allow for continuous T removal in a manner that does not require excessive electrical power and does not allow a large inventory of T to build up in the blanket. Excessive power consumption would reduce the amount of electricity available for sale and thus adversely impact the plant economics. High T inventory in the blanket is a safety issue for the power plant. 

## **2.2.6 Instrumentation and Controls (I&C) System** 

Thermal and mechanical aspects of the TBB will be monitored to assuring that it is operating within allowable ranges. The expectation is that the design of the TBB will accommodate monitoring sensors needed to determine and, if need be, adjust plant operating parameters related to the TBB functions, e.g., adjusting the coolant flow rate. 

## **2.2.7 Plant Safety Systems** 

Various accident scenarios will be evaluated for the power plant including accidents that could involve the TBB, e.g., loss of coolant flow to the blanket, loss of T containment, etc. The specific types of possible accidents and safety systems needed to mitigate consequences will depend on the TBB design details. Expectations are that the TBB will be designed to operate safely in normal and off-normal conditions including accommodating possible active measures in response to an accident, e.g. supplemental cooling, drain tanks, fire suppression, etc. 

## **2.3 Passive Stakeholders** 

This section describes those stakeholders that indirectly influence the TBB. 

## **2.3.1 Manufacturer/Supplier** 

It is likely that the TBB components will be manufactured by an industrial supplier that will contract with the plant owner to build and deliver components to the plant site. Expectations of the manufacturer/supplier are that the TBB can be built at a cost that is acceptable to the owner. Considerations include design complexity, cost and availability of materials, industrial experience with required manufacturing techniques, ability to meet industrial standards, e.g., AMSE. 

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

![Fig. 3.1 Function boundary of the TBB showing primary inputs and outputs.](images/tmphfztki6w.pdf-0013-03.png)

![Fig. 3.2  Context diagram indicating Active and Passive Stakeholders.](images/tmphfztki6w.pdf-0013-05.png)

## **3.2 Reference Operational Architecture** 

Since commercial fusion power is a couple decades off, there a several TBB under development worldwide. While there is not yet a clear _reference architecture_ , we take the helium cooled, lithium-lead (HCLL) TBB concept as the starting point for the purposes of this report. This concept is currently favored in the EU and is a candidate TBB several other countries with strong fusion development programs (i.e., ITER partners) including the US. The US, however, has proposed a modified version of the HCLL that has improved thermal efficiency potential; this concept will be considered as one of the alternates evaluated later in the report. 

## **3.2.1 Helium Cooled Li-Pb TBB** 

The HCLL blanket concept is illustrated schematically in Fig. 3.3. The essential features are the TBB module structure; He coolant inlet, distribution and outlet; LiPb supply, distribution and outlet. A steel containment structure defines the shape of the TBB module including the first wall (FW) that faces the plasma.  The entire blanket that surrounds the fusion plasma will be made up of hundreds of these modules. Helium coolant inlet/outlet pipes are attached to the structure as are LiPb inlets and outlets. The internal features of the TBB module are designed to distribute the LiPb and He in a manner that the tritium breeding and cooling functions are achieved. Figure 3.4 is a more realistic illustration of how the TBB model would look. 

![Fig. 3.3 Schematic of the HCLL TBB module.](images/tmphfztki6w.pdf-0014-04.png)

![Fig. 3.4.  More detail concept illustration of the PbLi TBB module (from A. Li Puma et al, “Design and Development of DEMO Blanket Concepts in Europe,” ISFNT-11, Barcelona, Spain, 9-17-14)](images/tmphfztki6w.pdf-0015-00.png)

## **4. SYSTEM DRIVERS AND CONSTRAINTS** 

The performance drivers for the TBB design evolve from the sacred expectations. 

**Tritium Breeding Performance.** The materials used in the TBB and their configuration must be such that a TBR> 1 can be achieved. This sets constraints on the type of materials that can be used (e.g., strong neutron absorber must be avoided), the relative fractions of materials (i.e., need sufficient atomic density of Li), the arrangement of materials within the TBB (e.g., neutron multipliers if used must be placed toward the plasma side of the TBB to be effective), and the overall thickness of the TBB (since fusion neutrons are very penetrating). A wide variety of TBB design concepts have been proposed that meet these constraints. 

**Power Recovery and Conversion Performance.** The requirement for absorbing the fusion power and making it available to the power conversion system at high temperature is also a significant design driver. The design must incorporate a method for heat removal, typically accomplished by either flowing a liquid metal breeder (such as Li, PbLi or molten salt) or by incorporating coolant flow channels through the 

TBB. This cooling function must be achieved while not preventing the essential T breeding function. Constraints include considerations of compatibility of coolants with structural materials they contact at the temperatures needed for efficient power conversion (i.e., minimizing corrosion), possible magnetohydrodynamics (MHD) power losses due to flowing liquid metals in the Tokamak’s magnetic fields, and the need to avoid contamination of the coolant by T if the breeder is not also the coolant. The ability to operate at high temperature is a strong economic driver for the plant since the power conversion efficiency increase with coolant temperature. 

**Safe Operation.** Safety is a significant design driver and impacts the selection of TBB structural materials (low activation materials are preferred or even required) and also the breeder itself (low chemical activity is preferred). The licensing and regulatory review will require integrated safety analyses of possible accident scenarios for the plant. Failure of the TBB and release of T or other radioactive material can impact those results. As such, constraints may arise from the safety but they are very design depend and cannot be generalized (e.g., limits on the amount of Li in the TBB). 

## **5. OPERATIONAL SCENARIOS** 

Here we discuss operational scenarios that will be required for the TBB to meet stakeholder expectations for three different phases of operation: start-up, normal full power operation, and shutdown. We also include one example accident scenario based on a mechanical failure in the TBB where a coolant pipe exterior to the blanket ruptures and coolant flow to the TBB is lost. 

## _**Startup**_ 

Starting the fusion power plant will involve activation of many systems in a prescribed fashion including bring the TBB to a start where is can perform its primary function of tritium breeding and power handling. Figure 5.1 illustrates the process. As part of the TBB startup, its structures must be brought up to a temperature higher than the melting point of the PbLi coolant (300C) so that the molten coolant does not freeze when it enters the TBB. The most likely approach for the dual cooled, PbLi TBB is to flow heated He through the He coolant channels and allow conduction to bring all structures up the desired temperature. The He would likely be heated by a natural gas fired burner. Thermal sensors indicate when the TBB is hot enough to accept PbLi flow. The PbLi flow begins and once the TBB is filled and full flow achieved, the fusion plasma can be initiated and will supply power to the blanket. At that point the He flow must be switch from its heating function to its cooling function, which will be accomplished by diverting the flow through the He heat exchanger instead of the gas heater. 

As soon as the plasma begins, the TBB will also begin breeding tritium. A portion of the flow will be diverted to the T recovery system either immediately or after a short period of operation that brings the T concentration in PbLi to the level needed for efficient recovery. 

![Fig. 5.1 Block diagram illustrating key components involved in start-up of the TBB.](images/tmphfztki6w.pdf-0017-00.png)

## **Table 5.1 TBB Start-up Steps** 

- Heat TBB structures with hot He flow. 

   - Start He heater. 

   - Flow He through 1) heater, 2) TBB, and 3) He-to-secondary-coolant heat exchanger (HX). He flow path is same as normal operations expect it is diverted through the He heater. 

   - Sense TBB temperature and report to control system continuously. 

- Heat PbLi in supply/storage reservoir until it reaches minimum operating temperature (~50C above melting temperature). 

- Start flow of PbLi to fill TBB and entire PbLi/HX loop. 

   - At this point both He and PbLi coolant loops are operating at full flow and constant temperature. 

- Start plasma heating and stop flow through He heater and PbLi heater sub-loops. 

- Activate power conversion systems. 

   - Secondary coolant flow through heat exchangers and steam generators. 

   - Steam flow through turbine/generators. 

- Tritium breeding begins as soon as plasma starts. 

- Activate T recovery process. 

   - Tritium breeding begins as soon as plasma starts. 

- Steady state power conversion and T recovery achieved. 

## **Steady State Operation** 

Steady state operation of the TBB is straight forward as indicated in Table 5.2. The TBB absorbs the plasma power and breeds tritium, while the He and PbLi coolants extract the power and deliver it to the power conversions system. Key operating conditions are monitored and reported to the power plant control systems. 

## **Table 5.2 Steady State Operations** 

- He flow conditions (e.g., temperature, pressure, mass flow rate) into and out of TBB are monitored and adjusted if necessary. 

- PbLi flow conditions (e.g., temperature, pressure, mass flow rate) into and out of TBB are monitored and adjusted if necessary. 

- TBB structural components (e.g., temperature, strain) are monitored. 

- TBB is also monitored for He or PbLi leaks. 

- Tritium concentration in PbLi flow is monitored and information used to determine T production rate (needs to be greater than or equal to plasma burn rate). 

## **Normal Shutdown** 

Normal shutdown will be required periodically for maintenance of the tokamak. The shutdown process returns the TBB to pre-operating conditions by draining the PbLi (so it does not solidify in the TBB) and allowing the structure to return to ambient temperature. The key steps are listed in Table 5.3. 

## **Table 5.3 Shutdown Procedures** 

- Plasma is stopped (discontinue fueling, external heating if any). 

- PbLi flow is diverted to storage reservoir. 

- He flow through the TBB continues at reduced flow rate sufficient to removed low level of afterheat (if necessary). 

- He flow stopped. 

- He loop depressurized. 

- Entire system cools by thermal radiation until it reached equilibrium with surrounding environment (confinement building). 

- End condition: TBB is empty (no PbLi), depressurized and at room temperature. 

## **Emergency Shutdown** 

The system, including the TBB, must also be design to deal with off-normal scenarios including accidents. One type of accident that is typically included in the safety review for plant licensing is a loss of cooling capability, either a simple loss of coolant flow (e.g., pump failure) or actual loss of coolant due to a pipe break or component rupture. Table 5.4 gives a possible emergency shutdown scenario due to a PbLi inlet pipe break external to the TBB. 

## **5.4 Emergency Shutdown Procedures** 

- PbLi flow sensors detect a sudden drop in flow rate the TBB module. 

- TBB temperature sensors may also detect a rise in component temperature outside normal range. 

- Instrumentation and controls give an emergency shutdown signal and the plasma is stopped. 

- PbLi is diverted to storage reservoir (design may require gravity flow to accomplish this). 

- Remainder of steps is the same as for normal shutdown. 

## **6. IMPLEMENTATION CONCEPTS AND RATIONALE** 

In this section we describe alternative for the key system elements that make up the TBB and give the rationale for selecting a new preferred TBB design, the dual cooled PbLi TBB with flow channel inserts (FCI). 

## **6.1 TBB Components Options** 

The following tables highlight some key feature of the major constituents of possible TBB designs: Table 6.1 covers tritium breeders, Table 6.2 neutron multiplier, Table 6.3 coolants, and Table 6.4 structural materials. 

**Table 6.1 Tritium Breeder Options** 

**Table 6.2 Neutron Multiplier Options** 

**Table 6.3 Coolants Options (see Table 6.1 for coolants that are also breeders)** 

**Table 6.4 Structural Material Options** 

## **6.2 Example TBB Component Combinations** 

There have been a number of TBB conceptual designs proposed using various combinations of breeder, neutron multiplier, coolant and structural material. To illustrate the systems engineering approach to comparative concept evaluation, we consider five liquid breeder concepts denote by: _Name (abbreviation): Breeder/Multiplier/Coolant/Structure_ 

1. Lithium/Vanadium (LV): Li / none / Li / V 

2. Single Coolant Lead Lithium (SCLL): PbLi / Pb in PbLi / PbLi / FMS 

3. Dual Coolant Lead Lithium (DCLL): PbLi / Pb in PbLi / PbLi and He / FMS 

4. DCLL with FCI: (DCLL-FCI): PbLi / PbLi / Pb in PbLi / PbLi and He / FMS with FCI 

5. Molten Salt (MS): Flibe / Be in Flibe / Flibe / ODS 

## **6.2.1 Comparison with Respect to Stakeholders Expectations** 

The following table gives a relative comparison of the concepts against stakeholder expectations with an emphasis on the sacred expectations (entries 1-4 in row 1). 

**Table 6.1 Comparison of concepts on ability to meet key expectations** 

*Key to expectations used in Table 6.1: 

- 1) Tritium Supply (TS): Produce more T fuel than is consumed and allow for continuous recovery 

- 2) Power Handling (POW): Absorb fusion power and make it available to the power conversion system at high temperature 

- 3) Costs (COST): Have acceptable capital and operating costs. 

- 4) Safety (SAF): Operate safely in normal and off-normal conditions. 

- 5) Reliability (REL): Potential for high reliability leading to high availability 

- 6) Environmental (ENV): Low environmental impact from induced radioactivity waste 

- 7) Tritium extraction (TEX): Ease of tritium recovery from breeder 

- 8) Fabricability (FAB): Can be fabricated with standard proven methods 

The results of this top level comparison are summarized as follows: 

- The LV concepts suffers for safety concern with the use of Li, the difficulty of extracting T from Li and the use of an expensive structural material that is difficult to fabricate. 

- The SCLL concept has challenges in cooling the TBB first wall due to MHD pumping losses with PbLi. Tritium concentration in the slower flowing PbLi is higher than others impacting safety. 

- The DCLL overall is an attractive concept meeting all expectations 

- The DCLL-FCI exceeds the DCLL since higher outlet temperatures and thus higher efficiency can be obtained. 

- The MS concept has several negatives related to its poor convective heat transfer coefficient, high cost of the molten salt and fabricability using the more advanced ODS steel. 

## **7. PROPOSED SYSTEM ARCHITECTURE** 

## **7.1 Recommended Configuration** 

Based on the previous comparison, the recommended configuration is the DCLL with flow channel inserts (FCI).  Key features of this TBB configuration are illustrated in Figs. 7.1 and 7.2. The schematic in Fig. 7.1 illustrate how the FCI is positioned between the flowing PbLi breeder and the steel structures of the TBB which are cooled with high pressure He. The FCI insulates the steel so that the outlet temperature of the PbLi coolant can exceed the limiting operating temperature of the steel. Figure 7.2 gives a more realistic view of the TBB configuration. This figure illustrates the routing of the He and PbLi coolants. It also shows how all regions that are filled with PbLi are lined with SiC. 

![Fig. 7.1 Schematic of DCLL configuration showing how the SiC flow channel insert is positioned in the PbLi coolant/breeding region (from N. Morley, FPA meeting, 10/11/2005)](images/tmphfztki6w.pdf-0024-03.png)

![Fig. 7.2.  A more detail diagram showing the internal configuration of the DCLL TBB using FCI (from N. Morley, FPA meeting, 10/11/2005).](images/tmphfztki6w.pdf-0024-05.png)

## **7.2 Comparison of Processes** 

The original DCLL TBB design and the selected DCLL-FCI design operate in virtually the same manner with a two key differences: 

- 1) The DCLL-FCI can achieve a higher PbLi outlet temperature which leads to a more efficient thermal conversion systems and better overall plant economics. This is due to the thermal insulating effects of the FCI. 

- 2) The PbLi flow velocity and total rate can be higher with the DCLL-FCI design. This allows a higher flow rate to the T extraction system resulting in lower T concentration in the PbLi and reduced safety risk. The allowed higher flow velocity is due to the electrical insulating properties of the FCI, which reduce MHD pressure drop. 

Beyond these two factors, the concepts are comparable. 

## **8. SYSTEM REQUIREMENTS** 

## **8.1 List of System Requirements** 

The system requirements are listed here. 

1. The tritium breeding material shall be the eutectic of PbLi with 17 atomic percent Li. 

2. The PbLi shall be molten to allow flow through the TBB. 

3. The inlet temperature of the PbLi shall be at least 50C above the melting point. 

4. The outlet temperature of the PbLi shall be 600C or more. 

5. All PbLi flow channels shall be lined with SiC flow channel inserts. 

6. The FCI material shall be constructed in a manner to provide thermal insulation between the PbLi and steel structures 

7. The FCI shall be constructed to provide magnetic isolation between the flowing PbLi and the steel channel walls 

8. The TBB structure shall be the ferrtic/martensitic steel FH82. 

9. The maximum steel temperature shall be 550C. 

10. The coolant for the TBB structures shall be He at 8 MPa pressure. 

11. The helium coolant channels shall be configured to keep the He pumping power below 10% of the plant gross electrical power. 

12. The TBB shall accommodate sensors for temperature, pressure and strain. 

13. The PbLi inlet/outlet flow connects shall allow for gravity draining. 

## **8.2 Mapping of Systems Requirements to Expectations** 

Table 8.1 shows a mapping of the system requirements to the same list of stakeholder expectations discussed in Section 6. 

**Table 8.1 Comparison of Concepts on Ability to Meet Key Expectations** 

*See Table 6.1 for list of Expectations 

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

- SR12:  Sensors for monitoring TBB conditions are needed to assure power extraction, detect off-normal conditions with potential safety impacts and assure operating conditions do not overly stress the system which could lead to early failure and reduced reliability. 

- SR13:  The requirement for gravity drain of the PbLi coolant is needed for off-normal shutdown and will also make normal servicing easier. 

## **9. ORGANIZATIONAL AND BUSINESS IMPACTS** 

The relevant organizations are the fusion technology development programs in the countries actively engaged in magnetic fusion energy R&D. Primarily these are the ITER partner countries. 

## **9.1 United States Impacts** 

The selected DCLL-FCI concept is currently the leading candidate for a liquid breeder type TBB in the US. Thus the current legacy R&D plan is not altered. However, the fact that the analyses supports the current path provides the funding agency (DOE) with greater assurance and confidence in this approach, supporting an argument for continued or even increased R&D funding. 

## **9.2 International Impacts** 

Various alternative TBB blanket concepts are leading candidates in other countries. The identification of the DCLL-FCI design as the favored concept in this study should motivation a closer look and perhaps expanded whole-wide R&D contributing to its development. 

## **10. RISKS AND TECHNOLOGY ASSESSMENT** 

## **10.1 Risk Assessment** 

Here we compare the risk of not meeting stakeholder sacred expectations (SE) for the original DCLL TBB and the DCLL-FCI TBB. 

## _SE1) Produce more T fuel than is consumed and allow for continuous recovery_ 

There is high confidence that both concepts can meet the tritium breeding requirement due to the use of the same breeding materials which has enough margin (TBR > 1.1) to present little risk. The DCLL-FCI has additional material that could have a slight negative impact on the TBR, but the use of SiC minimizes this impact. 

## _SE2) Absorb fusion power and make it available to the power conversion system at high temperature_ 

Both concepts provide viable methods of extracting the fusion power and delivering it to the power conversion system. The risk of not meeting this expectation is low. As previously note, the selected concept with FCI can achieve high PbLi outlet temperatures and thus improved thermal efficiency for the plant. To take advantage of the higher outlet temperature, more advance power conversion systems must be employed which carried a degree of additional development risk. This is significantly mitigated by the fact that the international power industry is already developing advance, high temperature systems for other energy systems such as nuclear, coal and natural gas. 

_SE3) Have acceptable capital and operating costs_ 

There is significant uncertainty and risk associated with the economics of future fusion power plants, but these are not strongly coupled to the TBB. The addition of FCI should not have a significant impact on the total capital cost of the power plant since the blanket is small part of the overall system. The fact the DCLL-FCI allows for a higher flow rate and minimizes conduction of the breeder heat into the He coolant stream means that there is less power removed by the He coolant. This is an advantage due to the potentially high pumping power demands of the He cooling. Further R&D is needed to see if lower He pressure and therefore thinner structures can be used with the FCI enhance design. 

_SE4) Operate safely in normal and off-normal conditions_ 

With proper overall design, there is confidence that the plant will meet safety expectations. Tritium management (total inventory, losses, accidental leaks, etc.) is extremely important in this regard. The DCLL-FCI has somewhat lower risk due to the fact the steady state T concentration in the PbLi can be maintained a lower level thus reducing the consequence of an accidental release and the demands for confinement (handling permeation losses) during normal operations. Continued R&D on efficient T extraction processes are needed for both designs. 

## **10.2 General Technology Assessment** 

Both concepts have similar low levels of technology readiness and R&D requirements as early phase conceptual design. Prototypes have not yet been built or tested, but scaled models will eventually be tested on ITER. The DCLL-FCI concept needs more work on the FCI material and how it is incorporated into the TBB. 

