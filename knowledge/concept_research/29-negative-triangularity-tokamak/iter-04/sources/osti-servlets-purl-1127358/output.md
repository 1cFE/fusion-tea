---
source: "https://www.osti.gov/servlets/purl/1127358"
source_type: "url"
extracted_at: "2026-04-19T23:01:19.848080+00:00"
content_hash_sha256: "093e9b06666cbb2aca4251ba1ffa00bb1a85fba8d0e37939bb837855fa1759fc"
backend: "pdf_pipeline"
---

**Princeton Plasma Physics Laboratory** 

## **PPPL5008** 

## **PPPL- 5008** 

# **The ARIES Advanced And Conservative Tokamak (ACT) Power Plant Study** 

Charles E. Kessel, et. al. 

MARCH, 2014 

![](images/tmpvln4n_oj.pdf-0001-06.png)

![](images/tmpvln4n_oj.pdf-0001-07.png)

**Prepared for the U.S. Department of Energy under Contract DE - AC02 - 09CH11466 .** 

## **Princeton Plasma Physics Laboratory Report Disclaimers** 

## **Full Legal Disclaimer** 

This report was prepared as an account of work sponsored by an agency of the United States Government. Neither the United States Government nor any agency thereof, nor any of their employees, nor any of their contractors, subcontractors or their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or any third party’s use or the results of such use of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise, does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof or its contractors or subcontractors. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof. 

## **Trademark Disclaimer** 

Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise, does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof or its contractors or subcontractors. 

## **PPPL Report Availability** 

## **Princeton Plasma Physics Laboratory:** 

http://www.pppl.gov/techreports.cfm 

## **Office of Scientific and Technical Information (OSTI):** 

http://www.osti.gov/bridge 

## **Related Links:** 

## **U.S. Department of Energy** 

**Office of Scientific and Technical Information** 

**Fusion Links** 

## **The ARIES Advanced and Conservative Tokamak (ACT) Power Plant Study** 

C. E. Kessel[1] , M. S. Tillack[2] , F. Najmabadi[2] 

F. M. Poli[1] , K. Ghantous[1] , N. Gorelenkov[1] 

1Princeton Plasma Physics Laboratory, Princeton, New Jersey, USA 

X. R. Wang[2] , D. Navaei[2] , H. H. Toudeshki[2] , C. Koehly[3 ] 2University of California, San Diego, California, USA 

3Karlsruhe Institute of Technology, Karlsruhe, Germany 

L. El-Guebaly[4] , J. P. Blanchard[4] , C. J. Martin[4] , L. Mynsburge[4 ] 

4University of Wisconsin, Madison, Wisconsin, USA 

## P. Humrickhouse[5] 

5Idaho National Laboratory, Idaho Fall, Idaho, USA 

M. E. Rensink[6] and T. D. Rognlien[6 ] 

6Lawrence Livermore National Laboratory, Livermore, California, USA 

M. Yoda[7] , S. I. Abdel-Khalik[7] , M. D. Hageman[7] , B. H. Mills[7] , J. D. Rader[7] , D. L. Sadowski[7] 

7Georgia Institute of Technology, Atlanta, Georgia, USA 

P. B. Snyder[8] , H. St. John[8] , A. D. Turnbull[8] 

7General Atomics, La Jolla, California, USA 

L. M. Waganer 

## S. Malang 

A. F. Rowcliffe 

## **Abstract** 

Tokamak power plants are studied with advanced and conservative design philosophies in order to identify the impacts on the resulting designs and to provide guidance to critical research needs.  Incorporating updated physics understanding, and using more sophisticated engineering and physics analysis, the tokamak configurations have developed a more credible basis compared to older studies.   The advanced configuration assumes a self-cooled lead lithium (SCLL) blanket concept with SiC composite structural material with 58% thermal conversion efficiency.  This plasma has a major radius of 6.25 total m, a toroidal field of 6.0 T, a q95 of 4.5, a βN of 5.75, H98 of 1.65, n/nGr of 1.0, and peak divertor heat flux of 13.7 MW/m[2] .  The conservative configuration assumes a dual coolant lead lithium (DCLL) blanket concept with ferritic steel structural material and helium coolant, achieving a thermal conversion efficiency of 45%.  The plasma major total radius is 9.75 m, a toroidal field of 8.75 T, a q95 of 8.0, a βN of 2.5, H98 of 1.25, n/nGr 

of 1.3, and peak divertor heat flux of 10 MW/m[2] .  The divertor heat flux treatment with a narrow power scrape-off width has driven the plasmas to larger major radius.  Edge and divertor plasma simulations are targeting a basis for high radiated power fraction in the divertor, which is necessary for solutions to keep the peak heat flux in the range of 10-15 MW/m[2] .   Combinations of the advanced and conservative approaches show intermediate sizes.  A new systems code using a database approach has been used and shows that the operating point is really an operating zone with some range of plasma and engineering parameters and very similar costs of electricity.  Papers in this issue provide more detailed discussion of the work summarized here. 

## **I. Introduction** 

The ARIES team has examined tokamak power plants with conservative and advanced assumptions applied to the physics and technology characteristics of the plant.  These are referred to as Advanced and Conservative Tokamaks or ACT.  Four configurations were studied, advanced physics with advanced technology, and conservative physics with conservative technology in the most depth with systems and both detailed physics and engineering analysis.  The remaining configurations, advanced physics with conservative technology, and conservative physics with advanced technology, were examined with only systems level analysis.  In addition, a number of extensions to the engineering and physics analysis have been included in these studies. 

As part of the detailed engineering analysis, improved approaches include history dependent inelastic component thermo-mechanical modeling, transient thermo-mechanics to model the effects of extremely short time-scale ELMs, electromagnetic mechanical analysis of disruptions on the primary conducting structures, modeling of brittle materials in the divertor (tungsten alloys) with fracture mechanics, and 3D CAD tied directly to neutronics modeling.  In addition, optimizing materials for their environment in the fusion core has begun with the identification of a potential new steel alloy for the vacuum vessel, that does not require post weld heat treatment like the reduced activation ferritic steels.   Experiments were performed at Georgia Institute of Technology to simulate the high heat flux He-cooled divertor concepts, demonstrating the strong trade-off of heat flux and pumping power, and providing a basis for assumptions made in the power plant divertor design. 

The last tokamak power plant study performed by this team, ARIES-AT[1] , was completed in 1999. Since that time, developments have occurred in both plasma physics understanding and modeling tools.  The present power plant study has included analysis of edge plasma and divertor analysis with 2D plasma and fluid/kinetic neutral particles, and solutions are sought for the high power handling required in these configurations.   In addition to this, formulations for ELM and disruption heat loading developed for ITER, based on experimental tokamak experience, were used to project the loading on the divertor and the first wall.   High fidelity heating and current drive models are now available and coupled to time dependent free-boundary integrated plasma evolution simulations, which are now used as part of the physics analysis.  The peeling-ballooning MHD stability was used to establish the H-mode pedestal height, and analysis has begun 

to examine the critical question of whether fast alpha particles MHD instabilities will lead to losses to the first wall or only to redistribution in these burning plasmas. 

The ARIES systems analysis code has been rebuilt around a new approach, utilizing a database methodology, solving for large numbers of viable operating points and filtering them to identify attractive candidates.   This has allowed the observation that there are always nearby operating points with plasma or engineering parameter changes that have only small differences in the cost of electricity.  This leads to the conclusion that although we choose a particular design point to analyze in detail, there are in fact other nearby points that could be viable design points, depending on the progress of plasma science and various areas of fusion technology. 

More detailed descriptions of the ACT power plant engineering and physics results can be found in the accompanying papers in this issue[2-11] . 

## **II. Four Corners Study of Advanced and Conservative Power Plant Features** 

The advanced and conservative examination is intended to show how the overall configuration changes with the plant technical philosophy. The advanced physics is described by high normalized plasma beta (βN ~ 5.8), assuming wall stabilization, and high global energy confinement (H98 ~ 1.65).  The conservative physics is described by low normalized plasma beta (βN ~ 2.6) assuming no wall stabilization and lower global energy confinement (H98 ~ 1.25).   In both cases the lowest density relative to the Greenwald density limit is sought, although it is always equal to or greater than 1.0.  In the conservative case this ratio must exceed 1.0, as the devices become larger and the expression nGr = Ip/πa[2] shrinks.   The advanced engineering is embodied by the choice of SiC composite structural material blanket concept using self-cooled lead lithium (SCLL), where PbLi eutectic serves as both breeder and coolant, obtaining a thermal conversion efficiency reaching ~ 58% in a Brayton cycle.  The peak heat flux in the divertor is allowed to rise up to 15 MW/m[2] , roughly consistent with projections based on the experimental results[5] .  The conservative engineering is embodied by the choice of dual coolant lead lithium (DCLL) blanket concept using ferritic steel structure with helium coolant, and PbLi eutectic as breeder and coolant.  This blanket does require flow channel inserts for electrical and thermal insulation between the liquid metal and ferritic steel. This blanket concept can reach thermal conversion efficiencies of ~ 45% with a Brayton cycle.   In both cases the divertor is helium cooled tungsten alloy, with tungsten plasma facing armor.  The conservative case has an upper limit of 10 MW/m[2] divertor peak heat flux.  The four corners are illustrated in Fig. 1, with dominant features that emerged from the systems analysis of these points, and will be described later. 

There are numerous other prescriptions that are common to both advanced and conservative configurations, and these are listed here, 

Plasma aspect ratio, A = 4.0 Up-down symmetric double null Plasma shape, κx = 2.2, δx = 0.63 

Power radiated in the divertor is 90% (Prad,div/PSOL) 100% non-inductive flattop plasma, inductive assist in rampup Nb3Sn superconductor for TF and PF coils He-cooled tungsten alloy divertor Li15.7Pb84.3 breeder Net electric power production is 1000 MW 

Table I shows several parameters of the ACT designs.  Focusing on the ACT1 (adv phys / adv tech) and ACT2 (cons phys / cons tech) the former has a major radius of 6.25 m, while the latter is 9.75 m.  Since the plasma beta’s are different βNth of 4.75 in ACT1 and 2.25 in ACT2, they have compensating toroidal fields, with 6.0 T in ACT1 and 8.75 T in ACT2.  Since in both cases the plasma is required to have 100% non-inductive plasma current, the higher bootstrap current fraction (0.91) in ACT1 allows the q95 to remain low at 4.5, a value commonly achieved in present day tokamaks.   ACT2 on the other hand, has higher total plasma current and lower bootstrap current fraction (0.77), leading to a high q95 of 8.0, which is not commonly targeted on present facilities.   Both cases assume a total wall plug efficiency for heating and current drive (source, transmission, and coupling) of 0.4.  For all cases examined the recirculating electrical requirement includes an auxiliary function power of 32 MW, a total pumping power for He and LiPb of ~ 1% of the total thermal power, and the calculated heating and current drive power.  In general, power plant design points require plasma densities near or above the Greenwald density in order to obtain the required level of fusion reactions.  The advanced physics provides solutions down to nGr, while the conservative physics points require up to 1.3nGr.  Some density peaking is assumed in all cases, n(0)/<n> ranging from 1.3-1.5, since transport theory[12] predicts that peaking is inevitable under the collisionalities typical of power plant plasmas. 

The neutron wall loading values are lower than found in previous studies, which is driven mostly by the heat flux in the divertor, driving solutions to larger major radii.  A divertor heat flux calculation is used, in all cases, that includes a power scrape-off width from ref (13), combined with a highly radiative divertor solutions.   It is assumed that 90% of the power entering the divertor (PSOL = Palpha + Paux – Pbrem – Pcycl – Pline) is radiated in the divertor, leaving only 10% to be conducted to the divertor target plate.  The ACT1 case has a peak divertor heat flux on the outboard target of 13.7 MW/m[2] , while ACT2 is constrained to a prescribed limit of 10 MW/m[2] . All cases include some argon as a core plasma impurity to provide line radiation, in addition to the cyclotron and bremsstrahlung radiation.  The latter two terms dominate the core radiation loss for the power plant regime plasmas.  The cyclotron loss is particularly high in the cases with high toroidal field and/or high central electron temperature, and for the systems analysis the reflection of cyclotron radiation from the first wall is taken to be 0.6.  The required heating and current drive power is lowest in ACT1 and highest in ACT2 as would be expected, 42.7 MW and 105.5 MW, respectively.  The fusion plasma gains range from 25 for ACT2 to 42.5 for ACT1.  The resulting engineering Qengr, defined as the ratio of net electric power to the recirculating electric power (Pelec/Precir), was highest in ACT1 at 6.5, and lowest was in ACT2 at 3.1.  The ACT1 power plant layout is shown in Fig. 2, indicating the 

primary components.   The plasma cross-sections for the ACT1, 2, 3, and 4 are shown in Fig. 3. 

Table I.  ACT plasma and plant parameters for the four corners examined. 

## **III. Detailed Physics Characterization for ACT1 and ACT2** 

The plasma configurations identified by the systems analysis were reproduced as well as possible in 1.5D time-dependent free-boundary simulations of the plasma evolution from early startup at Ip = 0.5 MA to the flattop current value, and allowed to relax over ~ 25003000 s.  Both  ACT1 and ACT2 configurations were examined.   The energy transport was modeled with a modified Coppi-Tang[14,15] formulation, to allow temperature profile variation (broad to peaked), and scaling to match the required beta.  Pedestals were enforced to match the peeling-ballooning theory projections from EPED1[16] , with ~ 140 kPa at the pedestal density of 1.0x10[20] /m[3] for ACT1, and with 185 kPa at the pedestal density of 0.65x10[20] /m[3] for ACT2.  The density profiles and magnitudes were prescribed, allowing some level of peaking of ~ 1.3-1.4 in ACT1, and slightly higher up to 1.55 in ACT2.  Argon impurity fractions of 0.3% were used, although in ACT1 it was determined that 0.9% of neon could be substituted for core line radiation.  The plasmas have strong shaping with κx = 2.2 and δx = 0.625. 

For the advanced physics of ACT1, wall stabilization of the low-n kink mode was assumed.   The broad pressure profile cases were high-n ballooning stable, and stable to the resistive wall mode with a tungsten shell on the outboard side at b/a = 0.3, for βN = 5.49-5.79 at BT = 6.0 T.  The medium pressure case was stable to these modes at βN = 5.28 at BT = 6.75 T.  The peaked pressure case was not stable even at βN = 5.15 at BT = 7.0 T, and was not pursued further.  The plasma triangularity was reduced to 0.63 to accommodate engineering design in the divertor, and the stabilizing wall location was determined as a function of triangularity.  The fast alpha particle MHD stability was analyzed and although found to be unstable, the fast alphas were redistributed to a larger minor radius rather than being lost from the plasma.  This result is sensitive to the central ion temperature, the fast beta, and the central safety factor. 

The heating and current drive systems for ACT1 are ion cyclotron radio-frequency fast wave (ICRF FW) at 65 MHz, and lower hybrid (LH) at 5 GHz.  The on-axis current is provided by the FWCD and the off-axis is provided by the LHCD.  The analysis was performed with TORIC full wave analysis[17] , and the ray-tracing 1D Fokker Planck Lower Hybrid Simulation Code (LSC)[18] .   The LH was found to optimize if launched at 60[o] above the midplane, limited by the passive stabilizer plates for vertical stability, achieving 0.18 A/W-m[2] .  The FWCD was launched from the midplane, and achieved 0.45 A/W-m[2] .  The total installed LH power was 40 MW, the total installed ICRF power was 20 MW, although the flattop only required ~ 5-10 MW.  Electron cyclotron was also examined as a possible replacement for the FWCD, however its CD efficiency was too low, at 0.1 A/W-m[2] .  Although the flexibility to deposit ECCD from minor radii of 0.20.6 can be effectively used to modify the q-profile with about 20 MW of installed power, and a reduction in the fusion plasma gain from 42 to 30.  Extensive scans of the launcher 

location and steering angle were examined to find the highest CD efficiency combinations. 

Detailed edge plasma simulations of the heat flux on plasma facing components from exhausting core plasma have been performed for two ACT1 divertor configurations[7] .  One configuration utilizes divertor plates strongly inclined with respect to the poloidal magnetic flux surfaces similar to that planned for ITER and results in a partially detached divertor-plasma with about 75% of the power entering the divertor being radiated.  The second configuration has divertor plates orthogonal to the flux surfaces, which leads to a fully detached divertor-plasma if the width of the divertor region is sufficient, and is found capable of radiating > 95% of the power entering the divertor.  Both configurations use scrape-off layer impurity seeding to yield an acceptable peak heat flux of ~10 MW/m[2] or smaller on the divertor plates and chamber walls.  The simulations are performed with the UEDGE 2D transport code[19] to model both plasma and neutral components with some supplementary neutral modeling performed with the DEGAS 2 Monte Carlo code[20] . 

For the conservative physics ACT2 configuration, no wall stabilization is assumed and the resulting stable βN < 2.45 for current profiles with li(1) > 0.75, and tends to drop as li(1) decreases.  The introduction of a far away wall, located 1.35 m from the plasma, which places it behind the ring structure and shield, can allow access to βN of 2.8-3.25 over li(1) from 0.85-0.65.  The high H-mode pedestal was playing a strong role in the low-n stability due to the bootstrap current near the plasma edge. 

The heating and current drive systems for ACT2 are primarily ICRF/FW at 95 MHz and negative ion neutral beams (NB) at 1 MeV particle energy.   The on-axis current drive is provided by both the ICRF, 0.7 MA for 30 MW injected power, and NB, about 2.7-3.0 MA with 65-80 MW injected power.  The NB provides a broad current profile across the entire plasma minor radius.   Since this configuration requires ~ 4 MA of current drive, the NBs are attractive from the deposition viewpoint since they do not concentrate the driven current.  Analysis was performed with the TORIC full wave code and NUBEAM orbit following Monte Carlo routine[21] in the TRANSP code.  Lower hybrid was examined with the LSC and found to penetrate to a normalized minor radius of 0.65 with a broad deposition, where the electron temperature reached 15-17 keV.  The combination of high toroidal field and low density was favorable for LH in spite of a high pedestal temperature of ~ 9.0 keV.  With no wall up to 1.0 MA of LH could be driven with no effect on the low-n stability, but 1.5 MA or more required the far away stabilizing wall. EC was examined with TORAY[22,23] and GENRAY[24,25] to identify the flexibility of deposition and its current drive flexibility.  Deposition from ρ = 0.2-0.6 was established with scans of the poloidal and toroidal steering, for a range of launching locations.  The q-profile could be modified with ~ 20 MW of EC injected power, but bulk current drive, to displace NBCD for example, was not efficient. 

## **IV. Detailed Engineering Characterization of ACT1 and ACT2** 

Engineering design and analysis of ARIES ACT1 and ACT2 were performed using the most sophisticated tools available in the areas of thermofluids, themomechanics, neutronics and safety.  3D CAD modeling helped to establish a self-consistent configuration, to demonstrate assembly and maintenance procedures, and to provide design details for individual components in support of analysis.  Complete engineering design and analysis results are reported in several accompanying papers. 

Power core configuration and maintenance.  The configuration of both ACT1 and ACT2 is based on a full-sector horizontal maintenance strategy.  This choice has been shown to provide the fastest changeout of in-vessel components, with the main penalty being larger TF coils to provide sufficient clearance.  Each sector is self-supporting, with sector-tosector connections but no attachment to the vacuum vessel.  Gravity loads are transferred vertically through the bottom of the vessel and into support pillars.  Full CAD drawings were produced and 3D motion studies demonstrated adequate clearances for assembly and maintenance. 

Component design and analysis.  Extensive 3D analysis was performed to assist in design and to demonstrate acceptable performance of the main power core components.  As compared with earlier studies, increased emphasis was placed on inelastic behavior of materials ( _e.g.,_ thermal stress relaxation, ratchetting, creep and fracture mechanics), transient loading conditions, and coolant manifold design and fabrication.  Here we summarize very briefly the most salient features and conclusions from component design studies. 

- a. _First wall and blanket_ .  The heart of the power core is the integrated first wall and blanket, which produces the majority of high-grade heat, breeds all of the tritium fuel and shields other components from the radiation environment.  Plasma stabilizing shells are embedded in the blanket, and the whole assembly is held together within a “strongback” structural ring made of an alloy of ferritic steel.  Both ACT1 and ACT2 adopted liquid PbLi eutectic as both breeder and coolant.  ACT1 uses the self-cooled PbLi concept with SiC composite structures, while ACT2 uses a dual-cooled blanket with about half of the heat removed by He in steel structures.  Notably, ACT2 is the first integrated power plant study by the ARIES Team using the DCLL blanket; previous applications included a spherical torus and compact stellarator power plant. Detailed analysis was performed on the first wall and blanket, demonstrating that all design rules and material limits were met.  Two novel alternative concepts were developed for ACT2: a first wall design capable of handling up to 2 MW/m[2] heat flux and a “small-module” DCLL design that offers potential advantages in fabrication and simplicity.  For both ACT1 and ACT2, far more detail was included in the design of manifolding that takes both He and PbLi coolant from the external headers and distributes it into each cooling channel. 

- b. _Divertor_ .  Few options are available for a divertor capable of withstanding timeaveraged heat fluxes in the range of 10-15 MW/m[2] with acceptable radiation damage and activation characteristics.  Based on our previous studies and a growing body of international research, we chose to use a He-cooled W-alloy divertor for both ACT1 

and ACT2.  The natural high operating temperature of W allows efficient utilization of the thermal power, roughly 20% of the plant total.  Several internal design options were explored, all using impinging jets to provide adequate heat transfer to maintain all materials within their operating limits.  For ACT1, the final design uses the platetype design with slot jets throughout the majority of the divertor and circular jet arrays in a modified multi-jet “finger” design in regions where the heat flux exceeds 8 MW/m[2] .  For ACT2, a pure plate-type divertor was possible due to the lower peak heat fluxes.  One of the most important design features of our divertor is the absence of “duplex” structures, in which W is bonded to steel, within the high heat flux region. Extensive “birth-to-death” inelastic stress analysis was performed on the external transition joint from W-alloy to the external steel piping, including a tantalum alloy interlayer and braze materials. 

- c. _High heat flux experiments_ .  Due to the importance of the choice of He as divertor coolant, experiments were conducted as part of this study to demonstrate acceptable performance and, in conjunction with numerical simulations, to provide semiempirical design relations for several impinging jet concepts including both linear slot jets ( _e.g._ for the plate-type and T-tube designs) and circular jet arrays ( _e.g._ for “finger” designs).  The experiments were carried out under “dynamically similar” conditions to a power plant, and produced both heat transfer coefficient and pressure drop relations. The results substantiate our design choices for the specified loading conditions, up to 10 MW/m[2] in ACT2 and 13.7 MW/m[2] in ACT1. 

- d. _Vacuum vessel_ .  A novel vacuum vessel was designed and thoroughly analyzed using 3D FEM analysis.  The vessel operates at an elevated temperature of the order of 350500˚C and uses He as coolant; the absence of water and high operating temperature help control tritium migration and inventory.  We chose to use a low-activation 3Cr3WV bainitic steel that provides lower activation than 316SS and no need for postweld heat treatment, which would be extremely difficult to perform[26] .  Thermomechanical analysis was performed for gravity, pressure, thermal stress and transient EM loading conditions. 

- e. _Power conversion_ .  Achieving high thermal conversion efficiency is important not only because it directly affects the cost of electricity, but also because system studies show that the design space for a tokamak power plant is significantly larger when the efficiency is high.  Less demand on other systems, especially the plasma, enables a more modest plasma beta, lower peak toroidal field, and other advantages.  The helium Brayton cycle was chosen for both ACT1 and ACT2 because it offers a good match to the high operating temperatures of He and PbLi coolants on the primary side.  The intermediate heat exchanger was designed with careful attention to the operating temperature limits of all of the components contributing to power conversion. Thermal cycle analysis predicts a thermal conversion efficiency (including cycle pumping powers but not the plant ancillary electrical equipment) of 58% for ACT1 and 45% for ACT2. 

Materials choices.  Many materials are needed within the radiation environment to satisfy all of the functions of the power core, including structures, joining materials, plasma armor, coolant and breeder, thermal and electrical insulators, connectors, conducting shells, _etc_ .  We attempted to identify attractive candidates for all of the mission-critical materials, but focused our more detailed evaluations on structural materials.  Further alloy development and characterization, and the development of design rules, are needed for both ACT1 and ACT2.  Both designs require a W-alloy and advanced ferritic steel alloy for the divertor.  The ACT2 blanket relies primarily on conventional ferritic steel structures ( _e.g._ F82H or EUROFER97), whereas ACT1 depends on the development of SiC composites.  Of particular note is the proposed 3Cr-3WV bainitic steel alloy for the vacuum vessel.  This alloy is not new, but has been applied for the first time in a fusion power plant design.  More details on materials assumptions and R&D needs can be found in accompanying papers [2,10]. 

Nuclear analysis.  Nuclear analysis (neutronics, shielding and activation) has a major impact on the evolution of our designs and their safety and environmental characteristics. For the nuclear analysis in ARIES ACT1 and ACT2 state-of-the-art 3-D computational tools were utilized to determine the neutronics, shielding, and activation parameters. Essential measures that helped deliver optimal ACT designs include estimating the TBR with higher fidelity than was previously possible, defining the radiation environment within the fusion power core in terms of accurate NWL profile, optimizing all components comprising the radial/vertical builds keeping in mind the activation characteristics of the preferred materials, determining the nuclear heat loads to all components including the fine details of the blanket, and estimating the radiation damage to structural components and their service lifetimes, taking into consideration the peaking due neutron streaming through assembly gaps. Our nuclear results reveal that both ACT1 and ACT2 designs satisfy the breeding requirements of 1.05 TBR with 40%[6] Li enrichment (< 90%), have an energy multiplication of ~1.16, He:LiPb thermal power ratio of 27:73 for ACT1 and 49:51 for ACT2.  The service lifetimes for ACT1 of 5 FPY for FW, blanket and divertor, 20 FPY for SR, and 40 FPY for outer components based on radiation damage considerations. The ACT2 components exhibit extended lifetimes due to lower NWL (~8 FPY for FW, blanket and divertor, and 40 FPY for outer components).   The nuclear heating and decay heat analyses also proved to be of particular interest as they called for redefining the IB and OB radial builds to enhance the power balance, control the unrecoverable low-grade heat deposited in the VV and LT shield, and reduce the temperature response during severe accidents for IB components. 

Safety analysis.  In assessing safety aspects, both ARIES-ACT1 and -ACT2 employ multiple coolants and coolant loops that give rise to a number of different possible accident scenarios involving loss of flow or coolant.  Helium is used as the coolant in the divertor, structural ring and vacuum vessel, while LiPb cools the blanket.  Water is used in the low temperature shield outside the vacuum vessel.  Due to resource limitations, detailed safety analysis was performed only on ARIES-ACT1.  Three variations of Fukushima-like scenarios were considered, involving long term station blackout (LTSBO, or loss of forced convection in all loops), and demonstrated that no releases from the ARIES-ACT1 power core can be expected.  The LTSBO/LOFA scenario alone 

constitutes a design-basis accident, and it has been demonstrated that the water coolant (which functions as both a neutron shield and emergency cooling system) adequately removes decay heat in this scenario.  We also considered two beyond design-basis accidents in which the loss of power is accompanied by a LOCA, in the helium and water loops respectively.  The helium LOCA does not represent an extreme for structure temperatures (helium in the cryostat provides another decay heat removal path), but it is necessary to ensure resulting pressure increases in the cryostat do not exceed the design limits of this confinement boundary, which was demonstrated.  In the third accident scenario, a water LOCA occurs during the power outage.  Since the water is the intended emergency heat removal mechanism, and the intact PbLi heat transfer system still contributes considerable decay heat, this represents a worst-case scenario from a decay heat removal standpoint.  The only mechanism for its removal is radiation through the maintenance ports to the vacuum boundary.  The MELCOR model does not predict any catastrophic failures in this case, though some potentially non-conservative assumptions remain to be more thoroughly investigated. 

## **V. Systems Analysis of Operating Points** 

The systems code is used to evaluate a large number of possible operating points while satisfying physics and engineering constraints.   The modeling of the plasma and plant systems is simplified in order to examine the integrated plant rapidly over many possible configurations.   It does require sufficient accuracy in its representations, but ultimately an operating point or points are examined with detailed analysis outside the scope of the systems code. 

The systems code can be described by its modules; physics, engineering, buildout, and costing[27] .  The physics module solves for 0D power and particle balance, including expressions for the radiated powers, bootstrap current, fast particle beta, Bosch-Hale DT fusion reactivity, up to four heating and CD systems, and up to 3 impurities.  The plasma profiles are parabolic modified to include a finite value at the edge.   The plasma operating space is identified by scanning all the critical plasma configuration variables * (R, BT, q95, βN, κ, δ, ε, Q, li, T profile, n profile, impurity fraction, n/nGr, ηCD, τp /τE). Initially the ranges for these parameters are chosen to be very broad, while later scans reduce the range as attractive parameter space is identified.  The resulting database will have a large number of operating points that satisfy the physics constraints, with a wide range of fusion powers. 

The physics points are passed through all the primary engineering assessments with input from neutronics for the IB radial build of the FW, blanket, shield (adjustable to <NW>), and VV.  The outboard radial build is also available for costing, but this region is not critical to operating point identification.  Evaluations include the FW heat flux, divertor heat flux, fusion core and overall plant power balance (including breakdown in blanket and divertor), TF coil, bucking cylinder/superstructure, CS/PF coils.  A graphical user 

interface was developed in order to help visualize the design space resulting from the scans described above[28] .  However, we found that a pre-screening process was valuable in order to reduce the dataset to a more tractable and meaningful number of points.  This was accomplished using a set of “filters” on individual parameters.  For example, net electric power output was typically filtered to accept only values between 975 and 1025 MWe. The database will include a wide range of plasmas with different values for fusion power, which allows one to easily scan engineering and balance-of-plant parameters such as the thermal conversion efficiency, heating and current drive wall-plug efficiency, or the impacts of pumping power or other electrical requirements.  Different net electric power can be requested, as well as the sensitivity to assumed engineering constraints such as the peak toroidal field at the magnet, or the peak heat flux in the divertor. 

Other filters are generally applied to isolate the physics points to meet some criteria, such as βN or H98 or n/nGr.   Ultimately the smallest major radii solutions are sought, although this is not a hard criterion in general, and a range of radii are normally left in the database.  The operating points that are left are passed through the full buildout of the plant, adding the top and bottom radial build and divertors, and the outboard radial build. These are then costed based on unit costing, such as $/kg, $/watt, or scalings involving thermal power or other relevant parameter. 

The most important observation from this database approach to systems analysis is that the idea of an optimal operating point, as one might derive from an optimizer systems analysis, is not appropriate since the uncertainty in virtually all associated parameters is too high.   It is seen in the database that there are several operating points with very close cost of electricity, having different values for the toroidal field in the plasma, the beta, fusion gain, peak heat flux in the divertor, bootstrap current fraction, impurity content, and so on.   For example, our knowledge of the maximum achievable toroidal field at the TF coil, or the maximum achievable beta, do not justify such a precise single operating point.  Shown in Table II are a sampling of solutions found for the advanced physics and advanced technology ACT1 power plant search, each with a COE that is within 5% of the reference case.   The parameter minimum or maximum is highlighted for the alternate configurations, which includes the highest βN, lowest major radius, lowest divertor peak heat flux, lowest βN, and lowest toroidal field.  The operating point is actually a space and could be identified by a set of parameter ranges, such as R = 6.0-6.75 m, BT = 5.25-7.25 T, βNtotal = 4.8-6.0, qdivpeak = 10.5-14.7 MW/m2, for example.   These parameter ranges total can be further prescribed by their inter-relationships, or trade-offs, such as BT-βN of 5.25-5.96 to 7.25-4.77.  Comparing the first and fourth columns, if the highest peak heat flux tolerable in the divertor is ~ 10 MW/m[2] , then the operating point must obtain a higher major radius, a lower beta, a higher q95, associated H/CD and radiation loss powers, and a higher cost to accommodate the requirement. 

Table II.   Several nearby operating points for ACT1 with < 5% increase in COE from the reference, indicating a range of plasma parameters are accessible. 

Shown in Table III is a similar sampling of points around the conservative physics and conservative technology ACT2 configuration.   The alternate cases have their COE within ~ ±4% of the reference case.   This plasma operating space was strongly affected total by the divertor peak heat flux and the βN constraints, driving the major radius up to 9.75 m.  The parameter minimum or maximum is highlighted for each alternate case including minimum major radius, highest fusion gain, lowest divertor peak heat flux, and lowest toroidal field.  The last column in the table shows the reduction in major radius total from the reference case by 1.0 m when allowing βN to rise to 3.0, and the peak divertor heat flux is only slightly above our limit of 10 MW/m[2] .  This increase in βNtotal is consistent with a far away wall behind the blanket and ring structure shield, as identified in the detailed ideal MHD stability analysis.  On the other hand comparing columns one and two, if higher peak divertor heat fluxes are tolerable, then the major radius can be reduced compared to the reference case, with most other parameters very similar, and a reduced cost.  The operating point range here for ACT2 would be described as R = 9.2510.0 m, BT = 8.0-8.75 T, βNtotal = 2.6, qdivpeak = 9.0-14.9 MW/m2, and Q = 20-27.5 for example, which is clearly differentiated from that for ACT1.  The benefit of allowing a total slightly higher βN can be clearly identified with the database approach, and the implications can be examined with detailed analysis. 

Although the cost of electricity (COE) is a useful collective measure for a configuration, it does not adequately represent the operating space of possible configurations that exists, 

since we typically impose several constraints or limits based on what plasma physics or technology advances is considered reachable.   These projections are in fact quite uncertain, and demonstrating viable configurations where these projections are both more or less aggressive, provides greater credibility to the plant identification.   The database approach can clarify the impact of the projections on the other plasma and engineering parameters, like the geometry (major radius), for example. 

Table III.  Several nearby operating points for ACT2 with ±4% difference in COE from the reference, indicating that a range of plasma parameters are accessible. 

## A. Comparison of ARIES-ACT1 and ARIES-AT 

The last tokamak power plant study performed by this team was the ARIES-AT[1] design in 1999, and comparing the advanced physics and advanced technology ACT1 design point to that older design is of interest to account for the changes that have taken place. Table IV provides some physics parameters of the two plants.  In 1999 the power scrapeoff width formulation from the physics community[29] was proportional to the scrape-off layer (SOL) power in the numerator, so that as the power leaving the plasma and transporting to the divertor increased, the scrape-off width would also increase.   The calculated peak heat flux in the divertor for ARIES-AT was then 5 MW/m[2] , which could be handled by a PbLi coolant and SiC composite structure, with a thin tungsten coating 

for resistance to sputtering. By 2002-2003 the formulation for the power scrape-off width had changed to having the SOL power in the denominator, causing a reduction of the power scrape-off width with increasing power.  The ACT activity adopted an explicit scrape-off layer width formulation derived from Fundamenski[13] for the systems analysis, and an expression for the peak divertor heat flux, given by 

![](images/tmpvln4n_oj.pdf-0017-01.png)

![](images/tmpvln4n_oj.pdf-0017-02.png)

in combination with a high radiated power fraction (fdiv,rad = Pdiv,rad/PSOL = 90%) in the divertor.  The conducted power footprint areas can then be given approximately by 2π(Ra/2) λpowfψftilt for the outboard and 2π(R-a) λpowfψftilt for the inboard, where fψ is the poloidal flux expansion (determined from equilibria), and ftilt is the divertor target tilt angle expansion.   These are reasonably accurate for the typical plasma geometries examined in the ARIES studies.  The radiated power footprint areas are taken approximately as 2π(R-a/2)x(a/2)x2 on the outboard and 2π(R-a)x(a/4)x2 on the inboard, which includes the dome and sidewalls of the divertor slot.  The power plants typically have power scrape-off widths of 3-5 mm, which provide the need for highly radiating divertor (partially to fully detached) operating regimes.  Using the same formulation for ARIES-AT, the peak heat flux on the outboard divertor would be 22.6 MW/m[2] , as opposed to the original 5 MW/m[2] .  Simulations with UEDGE 2D plasma and fluid/kinetic neutral codes[19,20] indicate that the highly radiating regimes may be accessible both with an ITER style strongly inclined target to obtain 75% radiated power and about 12-13 MW/m[2] peak heat flux, or with a perpendicular target and wide slot geometry divertor to obtain >95% radiated power and ~ 2 MW/m[2] on the target and side walls.   The engineering design of the divertor was also changed to helium cooled tungsten utilizing plate or finger jet-impingement designs in order to handle the resulting heat fluxes over a range up to 10-15 MW/m[2] . 

Another critical parameter that was updated in the ACT studies is the wall-plug efficiency for the heating and current drive (H/CD) systems, and should include the source efficiency, the transmission efficiency, and any coupling to the plasma efficiency that applies.   In the ARIES-AT study, this parameter was generally taken to be ~ 0.70.75.  Recent reviews of this parameter[30,31] indicate it is approximately ~ 0.4 for all sources (NB, EC, LH, and IC) in spite of varying values for the individual contributions among the different sources.   For simplicity this value is assumed in the systems analysis regardless of the H/CD scheme.   This parameter, which increases the recirculating power associated with the H/CD system, and the treatment for the peak heat flux in the divertor both contribute to the larger plasma major radius for ARIES-ACT1 at 6.25 m compared to ARIES-AT at 5.20 m.   Although both ACT1 and ARIES-AT operate at their Greenwald density limit, the ACT1 case has a 60% lower density due to the increased size of the plasma and lower plasma current.   The shift to larger plasma size in ACT1, for the divertor heating, and the reduced wall-plug efficiency conspire to lower the plasma current and raise the minor radius, both making the Greenwald density lower. 

The larger plasma volume can compensate the lower plasma density to provide a similar fusion power, since Pfusion = ∫nDnT<σv>EfusiondVplasma. 

The physics description of the plasma is improved by incorporating 1.5D analysis that has limited the broadness of temperature and current profiles compared to the purely equilibrium analysis of the ARIES-AT study.   The use of the peeling-ballooning pedestal constraint [17] has provided a consistent profile constraint at the plasma edge compared to the L-mode or adhoc H-mode edge treatments in ARIES-AT.  The triangularity has been lowered to accommodate engineering space and shielding requirements, however it still remains high at 0.63.  Higher fidelity heating and current drive analysis using the modern tools like TORIC full wave[17] for ICRF, NUBEAM[21] for NBs, LSC[18] for lower hybrid, and GENRAY[24,25] and TORAY[22,23] for EC, has allowed more consistent configurations to be defined, with significantly better predictions for current drive efficiency than previously available. 

Table IV.  Parameters for the advanced physics and advanced technology design ARIESACT1 and the ARIES-AT also an advanced physics and technology plant. 

*original divertor peak heat flux was reported as 5 MW/m[2] , this value uses the same approach as the ACT studies 

B. The ACT3 and ACT4 Operating Points Identified 

The ACT3 advanced physics with conservative technology and ACT4 conservative physics with advanced technology configurations provide a way to view permutations on the all advanced or all conservative designs.  ACT3 combines the high βN and high energy confinement plasma with the conservative DCLL blanket concept and its thermal conversion efficiency of ~ 45%.  The major radius of this design is 8.5 m, and a corresponding peak heat flux in the divertor of 9.6 MW/m[2] with 90% radiated power fraction.  The edge safety factor q95 is 4.25.  ACT3’s fusion power is similar to the conservative ACT2 since the thermal conversion efficiency dominates the determination of the required fusion power to generate 1000 MW of electricity. 

The ACT4 combines a low βN and lower energy confinement plasma with the advanced technology SiC composite blanket with a thermal conversion efficiency of ~ 58%.   The major radius of this design is 8.0 m, and a corresponding divertor peak heat flux of 8.6 MW/m[2] with 90% radiated power fraction.  In this particular case it was not difficult to find low divertor peak heat flux cases, since the power terms are similar to ACT1, and the major radius is 30% larger.  Its fusion power is close to that of the all advanced ACT1 design, due to its high thermal conversion efficiency.  The peak toroidal field at the TF coil did reach 16 T, which we have used as a limit in these studies.  The limiting criteria to keeping the plasma major radius from dropping were the toroidal field limit of 16 T at the TF coil and the desire for higher fusion gain.  For example, 7.5 m major radius plasma solutions existed with peak toroidal field at 16 T, however the fusion gain had dropped to 17.5, so a slightly higher major radius was chosen to recover a fusion gain of 27.5. 

Both ACT3 and ACT4, which combine advanced and conservative features, demonstrate a larger major radius than ACT1 and a lower major radius than ACT2, as might be expected.   Since the technology philosophy is primarily a change in the thermal conversion efficiency, the fusions powers are similar between the advanced technology (ACT1 and ACT4) and conservative technology (ACT2 and ACT3) variants.  Similarly the physics philosophy is primarily a βN-BT-q95-H98-n/nGr combination change, and the ACT3 and ACT4 retain the physics parameters associated with the advanced or conservative choice.   On the other hand, several parameters end up intermediate between the all conservative and all advanced configurations, in addition to the major radius. These include the plasma density, neutron wall load, heating and current drive power, recirculating power, fusion plasma and engineering gains, and cost of electricity.  Overall, these configurations show that advancing physics or technology can potentially reduce the device size and cost over a all conservative configuration. 

In 1991 the first ARIES power plant design was completed, referred to as ARIES-I[32] , which targeted conservative physics and advanced technology.  The assumption for βN was 3.2, the global energy confinement multiplier H98 was 1.49, a current drive efficiency of 0.37 for ICRF/FW, a wall-plug efficiency for that heating and current drive system of 0.72, a SiC composite blanket with a thermal conversion efficiency of 49%, a neutron multiplication factor for heating in the blanket of 1.3, and assumptions about the pumping and auxiliary systems recirculating powers.   At the time, the estimated peak heat flux in the divertor was 3.88 MW/m[2] , while our present analysis finds a value of 15.3 MW/m[2] , which is too high for our conservative technology assumptions and at the upper limit for our advanced technology assumptions.  Table V shows several parameters of the ARIESACT4 (cons phys / adv tech), ACT2 (cons phys / cons tech), and ARIES-I.  ARIES-I obtained a smaller major radius than either of these recent ACT designs, which has been tracked down to a higher H98 assumption, a higher βN assumption, a higher wall-plug efficiency, and a high divertor peak heat flux.  Better understanding and analysis shows us that the βN = 3.2 for the profiles assumed is too high without a stabilizing shell.  The strategy for externally driving current with ICRF/FW is not considered feasible since it relied on multi-pass absorption to distribute the current across the minor radius, and this 

is not experimentally observed.  The current drive efficiency assumed for ICRF was close to that obtained from simulations for the ACT studies.  The assumed energy confinement in ARIES-I is high relative to ACT2 and ACT4, which have conservative physics assumptions.  The ARIES-I design was also attempting to take advantage of high magnetic field at the plasma and TF coil, above those now considered feasible for low temperature superconductors based on Nb3Sn. 

Table V. Selected parameters from ARIES-I, as compared with ARIES-ACT4 and ACT2. 

*these parameters are generated from the present systems code to recover the ARIES-I design point, so that some of these parameters are slightly different due to different models. 

## **C. Conclusions** 

The ARIES ACT study has examined the impact of conservative and advanced physics and technology assumptions on the steady state tokamak power plant configuration to total produce 1000 MW of net electric power.   The advanced characterization of high βN (5.75), high H98 (1.65), and SiC composite structure SCLL blanket concept (ηth = 58%) results in a 6.25 m plasma, with 11 MA plasma current and 6.0 T toroidal field.  The conservative characterization of low βNtotal (2.60), low H98 (1.25), and ferritic steel structure DCLL blanket concept (ηth = 45%) results in a 9.75 m plasma, with 14 MA of plasma current and 8.75 T toroidal field.   Both of these configurations have assumed H/CD wall plug efficiency of 0.4, subsystems electric power requirement of 32 MW, and pumping power requirement of ~ 1% of the total thermal power.  The peak heat flux in 

the divertor has employed a power scrape-off width formulation, in combination with a 90% radiated power in the divertor assumption, that has led to larger device size, particularly compared to the previous ARIES-AT and ARIES-I design points.  Detailed analysis of the edge and divertor plasma provides some support of this high radiation power-handling regime.  The increased size has reduced the neutron wall loading compared to previous studies as well, allowing a 5 FPY lifetime for the ACT1 and 8 FPY lifetime for ACT2.  Both configurations utilize Li15.7Pb84.3 as liquid metal breeder/coolant, with 40% Li-6 enrichment, reaching TBR’s of 1.05.  The helium cooled tungsten alloy with tungsten armor is the divertor concept for both.  Up-down symmetric double null geometry with strong shaping is also common to these configurations. 

The ACT activity simultaneously improved and expanded the analysis approaches in both engineering and physics.   Engineering activities expanded with the use of inelastic analysis on critical components like the blanket and divertor structures, fracture analysis on the brittle tungsten components, transient analysis of ELM type heat loading on the divertor, and electromagnetic disruption analysis of conducting structures during the current quench.   The nuclear analysis has developed routine examination of 3D CADbased first wall, blanket, structural ring/shield, and vacuum vessel, and divertor regions. The combination of similarity experiments for the high heat flux He-tungsten divertor designs with detailed thermo-mechanical and CFD analysis was used to provide the basis for the ACT divertor designs.  The physics analysis utilized time-dependent freeboundary plasma simulations, with high fidelity heating and current drive models.  Ideal MHD expanded to include the peeling-ballooning pedestal stability and fast alpha particle stability.   2D edge and divertor plasma modeling with fluid and kinetic neutrals was employed to find solutions to the high power handling for ACT1.  Experimental observations were used to determine the ELM and disruption thermal loading of the divertor and first wall in order to provide engineering analysis with some guidance, and begin to establish power plant regime limitations for these phenomena. 

An new database systems analysis approach was employed in the ACT studies, in which a large database of viable operating points are produced, rather than a single optimized operating point based on cost of electricity, as was done previously in the ARIES studies. The new approach confirmed the expectation that there are many nearby operating points with only slightly different cost of electricity, that exhibit variations in both plasma and engineering parameters.  The conclusion is that within the uncertainty inherent in our present knowledge of achievable parameters in a fusion power plant, such as maximum toroidal field at the TF coil or maximum βN achievable, we can actually only determine a range of solutions that meet our technical criteria within a cost of electricity zone.   This range allows us to see the impact of more or less aggressive assumptions.  This is considered a preferable and more credible way to describe power plant visions for the future. 

## **Acknowledgements** 

This work is partially supported by the US DOE contracts DE-AC02-76CH03073, DEAC52-07NA27344, and DE-FC02-04ER54698. 

## **References** 

- [1]  F. NAJMABADI et al, _Fus Eng Des,_ **80** , 1, (2006). 

- [2] M. S. TILLACK et al, _Fus Sci Tech_ , this issue. 

- [3]  C. E. KESSEL et al, _Fus Sci Tech_ , this issue. 

- [4]  X. R. WANG et al, _Fus Sci Tech_ , this issue. 

- [5]  M. YODA et al, _Fus Sci Tech_ , this issue. 

- [6]  J. P. BLANCHARD and C. J. MARTIN, _Fus Sci Tech_ , this issue. 

- [7]  M. E. RENSINK and T. D. ROGNLIEN, _Fus Sci Tech_ , this issue. 

- [8]  P. W. HUMRICKHOUSE and B. J. MERRILL, _Fus Sci Tech_ , this issue. 

- [9]  L. EL-GUEBALY and L. MYNSBURGE, _Fus Sci Tech_ , this issue. 

- [10]  X. R. WANG et al, _Fus Sci Tech_ , this issue. 

- [11]  C. E. KESSEL and F. M. POLI, _Fus Sci Tech_ , this issue. 

- [12]  C. ANGIONI, et al., Plasma Phys. Control. Fusion 51 (2009) 124017. 

- [13]  W. FUNDAMENSKI et al, _Nucl. Fusion,_ **45,** 950, (2005). 

- [14]  W. M. TANG, _Nucl. Fusion_ , **26** , 1605, (1986). 

- [15]  C. E. KESSEL et al, _Nucl. Fusion_ , **47** , 1274, (2007). 

- [16]  P. B. SNYDER et al, _Nucl. Fusion_ , **51** , 103016, (2011). 

- [17]  BRAMBILLA, M., _Plas Phys Control Fus_ , **41** , 1, (1999). 

- [18]  D. W. IGNAT et al, _Nucl. Fusion_ , **34** , 837, (1994). 

- [19]  T.D. ROGNLIEN and M.E. RENSINK, _Fus Eng Des_ , **60,** 497 (2002). 

- [20]  D. STOTLER and C. KARNEY, _Contrib. Plas Phys_ , **34,** 392, (1994). 

- [21]   R. J. GOLDSTON et al, _J Comp Phys_ , **43** , 61, (1981). 

- [22]  A. H. KRITZ et al, Heating in Toroidal Plasmas, _Proc. 3[rd] Joint Varenna-Grenoble Int. Symp (Grenoble, 1982), vol 2 (Brussels, CEC), pg 707, 1982._ 

[23]  Y. R. LIN-LIU et al, _Phys. Plasmas_ , **10** , 4064, (2003). 

[24]  R. W. HARVEY AND M. G. MCCOY, 1993 Proc. Of the IAEA Technical Committee on Advances in Simulation and Modeling of Thermonuclear Plasmas (Montreal, Quebec) (Vienna: IAEA) pg 489.  USDOC NTIS Doc. No. DE93002962. [25]  A. SMIRNOV et al, in Proceedings of the 15th Workshop on ECE and ECRH, World Scientific, 2009, p. 301. 

[26]  L. EL-GUEBALY et al, _Fus Sci Tech,_ **61** 449 (2013). 

[27]  Z. DRAGOJLOVIC et al, _Fusion Eng. and Design,_ **85,** 243, (2010). 

[28] L. C. CARLSON et al, _Fus Sci and Tech,_ **60** , 459, (2011). 

- [29]  A. LOARTE et al, J Nuc Mat, **266-269** , 587, (1999). 

[30]  D. STORK, “Technical Challenges on the Path to DEMO”, MFE Roadmapping in the ITER Era, Sept. 2011, http://advprojects.pppl.gov/Roadmapping/presentations.asp; D. STORK, “DEMO and the Route to Fusion Power”, 3[rd] Karlsruhe School on Fusion Technology, Sept. 2009. 

[31]  P. THOMAS, “Heating and Current Drive Systems, Their Impact on Scenario/Economics (Lessons Learned from ITER Design)”, 2[nd] IAEA DEMO Workshop, 

Vienna, Austria, Dec. 2013, http://www-naweb.iaea.org/napc/physics/meetings/TM45256/talks/Thomas.pdf

[32] R. W. CONN et al, *Nuc Fus Supplement*, **3**, 659, (1991).

![](images/tmpvln4n_oj.pdf-0024-00.png)

**----- Start of picture text -----**<br>
ACT3 ACT1<br>Advanced   Physics Advanced   Physics<br>Conservative   Technology Advanced   Technology<br>Four   Corners   Study<br>Conservative   Physics Conservative   Physics<br>Conservative   Technology Advanced   Technology<br>ACT2 ACT4<br>Technology<br>Physics<br>**----- End of picture text -----**<br>

Figure 1.   The four corners study of tokamak power plants examines the impact of advanced or conservative assumptions in both physics and technology, referred to as ARIES-ACT1, 2, 3, or 4. 

![Figure 2.   ARIES-ACT1 advanced physics and advanced technology power plant configuration.](images/tmpvln4n_oj.pdf-0025-00.png)

![Figure 3.  The plasma boundaries for the 4 corners ACT plants identified.   ACT1 and ACT2 were examined I detail, while ACT3 and ACT4 are examined only at the systems level.](images/tmpvln4n_oj.pdf-0026-00.png)

The image appears to be a blank white page with no visible text or content to extract.

The Princeton Plasma Physics Laboratory is operated by Princeton University under contract with the U.S. Department of Energy. 

## Information Services 

Princeton Plasma Physics Laboratory P.O. Box 451 Princeton, NJ 08543 

Phone: 609-243-2245 Fax: 609-243-2751 e-mail: pppl_info@pppl.gov Internet Address: http://www.pppl.gov 

