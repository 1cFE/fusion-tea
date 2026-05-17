---
source: "https://www.osti.gov/servlets/purl/1028880"
source_type: "url"
extracted_at: "2026-04-19T23:41:10.970490+00:00"
content_hash_sha256: "7bc80422b442f0de92d927b14cd439dddc770f579dd718e98e035beea8d028dc"
backend: "pdf_pipeline"
---

LLNL-JRNL-463734 

![](images/tmpd8v1iugk.pdf-0001-01.png)

## Chamber Design for the Laser Inertial Fusion Energy (LIFE) Engine 

J. F. Latkowski, R. P. Abbott, S. Aceves, T. Anklam, D. Badders, A. W. Cook, J. DeMuth, L. Divol, B. El-Dasher, J. C. Farmer, D. Flowers, M. Fratoni, R. G. ONeil, T. Heltemes, J. Kane, K. J. Kramer, R. Kramer, A. Lafuente, G. A. Loosmore, K. R. Morris, G. A. Moses, B. Olson, C. Pantano, S. Reyes, M. Rhodes, K. Roe, R. Sawicki, H. Scott, M. Spaeth, M. Tabak, S. Wilks 

December 7, 2010 

Fusion Science and Technology as part of the Proceedings of the Nineteenth Topical Meeting on the Technology of Fusion Energy (TOFE) 

## **Disclaimer** 

This document was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor Lawrence Livermore National Security, LLC, nor any of their employees makes any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or Lawrence Livermore National Security, LLC. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or Lawrence Livermore National Security, LLC, and shall not be used for advertising or product endorsement purposes. 

## **CHAMBER DESIGN FOR THE LASER INERTIAL FUSION ENERGY (LIFE) ENGINE** 

Jeffery F. Latkowski[1] , Ryan P. Abbott[1] , Sal Aceves[1] , Tom Anklam[1] , Andrew W. Cook[1] , James DeMuth[1] , Laurent Divol[1] , Bassem El-Dasher[1] , Joseph C. Farmer[1] , Dan Flowers[1] , Massimiliano Fratoni[1] , Thad Heltemes[2] , Jave Kane[1] , Kevin J. Kramer[1] , Richard Kramer[3] , Antonio Lafuente[1,4] , Gwendolen A. Loosmore[1] , Kevin R. Morris[1] , Gregory A. Moses[2] , Britton Olson[1] , Carlos Pantano[3] , Susana Reyes[1] , Mark Rhodes[1] , Rick Sawicki[1] , Howard Scott[1] , Max Tabak[1] , Scott Wilks[1] 

_1Lawrence Livermore National Laboratory, Livermore, CA 94550_ 

_2Department of Engineering Physics, University of Wisconsin-Madison, WI 53706_ 

_3Department of Mechanical Engineering, University of Illinois at Urbana-Champaign, 61801_ 

_4ETSI Industriales, Universidad Politecnica de Madrid, Madrid, Spain Email: latkowski@llnl.gov_ 

_The Laser Inertial Fusion Energy (LIFE) concept is being designed to operate as either a pure fusion or hybrid fusion-fission system.  The present work focuses on the pure fusion option.  A key component of a LIFE engine is the fusion chamber subsystem.  It must absorb the fusion energy, produce fusion fuel to replace that burned in previous targets, and enable both target and laser beam transport to the ignition point.  The chamber system also must mitigate target emissions, including ions, x-rays and neutrons and reset itself to enable operation at 10-15 Hz.  Finally, the chamber must offer a high level of availability, which implies both a reasonable lifetime and the ability to rapidly replace damaged components.  An integrated design that meets all of these requirements is described herein._ 

## **I. INTRODUCTION** 

The Laser Inertial Fusion Energy (LIFE) Engine is a laser-based energy system that can be constructed as either a pure fusion machine or as a fusion-fission hybrid.[1] As a starting point, the LIFE effort has focused on the ability to provide fusion power on a timescale consistent with the needs of the marketplace, to deliver commercial power production from the 2030s.[2] This necessitates the operation of pre-commercial plant in the 2020s.  This plant is denoted by a self-consistent facility “point design” known as LIFE.1, while plants in the first commercial fleet are denoted as LIFE.2. 

The pre-commercial plant, LIFE.1, is likely to have a fusion power of ~ 400 MW, a plant size which results in engineering breakeven and demonstrates fully integrated system operation.  Due to similar thermal and neutron wall loadings, LIFE.1 is relevant to either the pure fusion or fusion-fission hybrid options for LIFE.2 and beyond. The hybrid options are addressed in ref. 3-4. 

For any LIFE engine, the chamber is an important subsystem, and it must satisfy a number of complex, interrelated requirements.  These flow down from the LIFE primary criteria and overall plant requirements. They include: 

- Fabricate from commercially available materials; 

- Capture and transmit thermal power to the balance of plant (capable of 0.5-1.5 MW/m[2] thermal load); 

- Operate at high temperature for good thermal efficiency (T ≥600°C for  th ≥40%); 

- Remove residual target debris from previous shots (material recovery ≥99%); 

- Maintain high system availability for consistency with overall plant availability of ≥92%; 

- Produce tritium to replace that burned in previous targets (tritium breeding ratio ≥1.08); 

- Enable successful target and laser beam propagation to chamber center (laser propagation efficiency ≥95%); 

- Reset for the next shot (support 10-15 Hz operation). 

Through careful design and the selection of indirect-drive targets, the LIFE chamber meets the above requirements. 

## **II. THE USE OF INDIRECT-DRIVE TARGETS** 

Interestingly, a critical component of the LIFE _chamber_ design is the selection of indirect-drive _targets_ . Not only will LIFE-relevant, indirect-drive targets be tested on the National Ignition Facility, but they enable a different approach to protection of the chamber from the most troublesome target emissions.  While the thermal fragility of direct-drive targets requires that the chamber contain no more than mTorr of gas (really just unburned 

D-T fuel), indirect-drive targets are thermally robust and can accommodate much higher gas pressures within the chamber.[5] Specifically, the LIFE chamber design uses xenon as a fill gas at a density of 6  g/cc. 

The xenon within the chamber is able to completely range-out the ~ 10% of target output that is emitted as ions. In fact, the ions are stopped within a ball of gas that is only decimeters in radius.  An additional 12% of the target output is emitted as x-rays that are conservatively approximated as a 200 keV Maxwellian.  These x-rays are significantly attenuated in the xenon, and the prompt x- ray heating of the wall is only 210°C (from an ambient 600°C).  Over timescales of hundreds of microseconds, the gas re-emits soft x-rays and a Marshak wave arrives at the chamber wall.  Between pulses, the first wall nearly reaches ambient temperature.  Then, the secondary pulse heats the wall by ~230°C.  Figure 1 shows the timedependent heating of the first wall for LIFE.2 with a fusion yield of 147 MJ and a chamber radius of 5.7 meters.  These low-temperature pulses mean that a bare metal can be used as the first wall; refractory armor is unnecessary. 

![Fig. 1. The 6  g/cc of xenon fill gas limits the LIFE first wall heating to two pulses of 210-230°C.](images/tmpd8v1iugk.pdf-0004-02.png)

Due to the benefits of the xenon fill gas, the LIFE chamber can utilize near-term materials while being quite compact and enjoying a long lifetime.  For LIFE.1, the 400 MW fusion system is coupled with a 3.4-m-radius modified-HT9 (or a similar material) chamber.  LIFE.2 has a fusion power of 2200 MW and would utilize a 5.7m-radius chamber constructed from 12YWT or another oxide-dispersion strengthened ferritic steel (ODS-FS). On LIFE.1, the first wall would be subject to a damage rate of 10 displacements per atom per full-power-year of operation (10 dpa/fpy). The LIFE.2 first wall would experience 25 dpa/fpy. 

The xenon gas is initially heated to several eV, but it rapidly cools by radiation to a temperature of ~ 0.5 eV. At that time, the charge state of Xe is very close to zero, and it “stalls” from a radiative cooling perspective. Unless convection or radiative cooling from residual target debris provides significant additional cooling, the gas temperature at the time of the next shot (67 ms later) will be ~ 6000 K.  Thermal analysis of the target during injection indicates that this thermal load can be handled by the incoming target.[5 ] 

Laser propagation through the hot Xe is acceptable as shown in Figure 2.  Only 1-2% of the incoming, 3  laser is expected to be lost to inverse Bremsstrahlung near the target as the laser reaches peak intensity. 

![Fig. 2. Laser beam propagation through 6  g/cc xenon results in minimal transmission losses.](images/tmpd8v1iugk.pdf-0004-07.png)

Interaction with residual lead target debris is significant in that there will be stimulated Raman, however, the transition decay time is sufficiently long (110 ns) that one can excite all Pb atoms without any significant loss of laser energy. As a result of this, aggressive “chamber clearing” is not necessary.  A clearing ratio of just 1% per shot can be used to remove target debris for disposal or possible recycling. 

## **III. CHAMBER MECHANICAL DESIGN** 

There are several key features to the LIFE chamber design.  These include its modularity, the lack of beamtube connections to the chamber, the fact that the chamber is _not_ the primary vacuum barrier, and the selection of liquid lithium as the primary coolant for both the first wall and blanket. 

Figure 3 shows a model of the LIFE vacuum vessel with the first wall, blanket and support structure (these combine to form “the chamber”) sitting inside. The 

chamber consists of eight identical sections, which would be factory built and shipped to the power plant site.  Two chamber sections would be mounted within a support structure to form a ¼-section of the chamber.  This unit would provide common coolant injection and extraction manifolds for the two chamber sections.  The completed ¼-section of the chamber would be transported to the engine bay for installation.  Installation requires only the connection of four cooling pipes per ¼-section: two for the first wall and two for the blanket.  The two systems are independently plumbed to allow greater flexibility in optimizing flow rates and coolant temperatures. 

![Fig. 3.The LIFE chamber consists of eight identical modules assembled into ¼-sections for transport to the engine bay.](images/tmpd8v1iugk.pdf-0005-01.png)

Cooling connections will be made using mechanically-driven hydraulic couplers with integral ball valves.  This technology is in use on oil supertankers and can be adapted to high-temperature, corrosion-resistant materials such as molybdenum, Mo alloys such as TZM, and other materials.  Use of such materials is prohibited for the main structural materials, but cooling connections can be made far outside the region of high neutron fluxes. 

It is important to note that chamber installation does not require any connections to be made or broken for the forty-eight laser beam ports.  While the lasers themselves obviously propagate to the center of the chamber, the beamtubes stop at the wall of the vacuum vessel. 

Equally important is the fact that the chamber modules do not serve as the primary vacuum barrier.  In fact, they need not physically touch.  In some locations, steps will be utilized to reduce streaming.  In other 

locations, the spaces between chamber modules will be used by the target tracking and engagement systems.  The shield design will provide further protection to the vacuum vessel. 

Figure 4 shows the details of a chamber module.  The first wall is composed of a series of 10-cm-diameter tubes.  Advantages of pipes include high strength-toweight ratio and ease of fabrication.  The first wall pipes are plumbed in parallel and are attached to injection and extraction plena mounted to the sides of the blanket. Small gaps between first wall pipes limit the exposure of the blanket to high surface heat fluxes. 

![Fig. 4. The LIFE first wall is composed of steel tubes that are mounted to coolant plena on the sides of the blanket.](images/tmpd8v1iugk.pdf-0005-08.png)

To enable the laser beams to reach chamber center forty-eight openings totaling ~3% solid-angle are provided. At the beamports, the pipes are routed radially outward and then they wrap around on the back side of the blanket.  Additional openings are provided at the top and bottom of the chamber for interfaces with the target injection system and the debris clearing / vacuum pumping / target catching systems, respectively. 

The blanket is designed such that the coldest coolant is delivered to the structural materials.  This is accom- 

plished through use of “skin cooling” with the coolant entering the blanket at the top and flowing down at high speed through a trapezoidal cooling channel.  The coolant turns around when it reaches the bottom of the blanket and then flows up through the bulk region at much lower speed.  Figure 5 provides a cut through the mid-plant of the blanket. The low temperature and high speed in the skin region provides the most effective cooling. 

![Fig. 5. The LIFE blanket utilizes skin cooling to maintain structural material strength and corrosion resistance.](images/tmpd8v1iugk.pdf-0006-01.png)

Zinkle and Ghoniem state that ferritic-martensitic steels are compatible (corrosion is <5  m/year) with clean liquid lithium to temperatures of 550-600°C.[6] Coolant entering the blanket at 550°C will reach a temperature of 600°C at the bottom of the blanket.  Further heating in the bulk of the blanket can be allowed through use of nonstructural insulating panels.  Tungsten is compatible with liquid Li to more than 1300°C.[6] The current LIFE point design provides Li at an exit temperature of 800°C. Advanced designs that could provide even higher temperatures are under consideration.  Although it uses a single coolant, such designs are similar to the Dual Coolant Lead Lithium blanket design proposed by Tillack and Malang.[7 ] 

The LIFE chamber is designed according to the ASME piping code.[8] Specifically, the LIFE chamber is designed to 1/3 of a given material’s ultimate tensile strength, 2/3 of its yield strength, 2/3 of its creep rupture strength and a 0.01% creep rate per 1000 hours. Temperature-dependent properties are used in such evaluations.  These properties can be seen in Figure 6. 

For LIFE.1, an HT9 chamber could be as small as 2.7 meters in radius, however, a radius of 3.4 m has been selected to limit the damage rate to 10 dpa/fpy in order to provide a chamber lifetime of 1 year.  The superior strength at temperature shown by 12YWT and other ODS-FS materials enables ~8× as much fusion power with a chamber radius of only 5.7 m.  Although clearly more data is needed, the void swelling lifetime of ferriticmartensitic steels is likely to be more than 100 dpa or >4 fpy in LIFE.2.[6] 

## **IV. THE USE OF LIQUID LITHIUM COOLANT** 

Liquid lithium is the primary coolant for both the first wall and blanket in LIFE.  Lithium has many advantages as well as a couple of disadvantages that are well-known. Engineering controls are included in the design to mitigate risks associated with the disadvantages. 

![](images/tmpd8v1iugk.pdf-0006-08.png)

**----- Start of picture text -----**<br>
Non‐ODS Ferritic<br>316FR<br>9Cr‐ODS<br>1400<br>12YWT<br>SiCf/SiC<br>1200<br>HT-9<br>1000<br>800<br>LIFE.2<br>600<br>400 LIFE.1<br>200<br>0<br>0 200 400 600 800 1000<br>Temperature (  C)<br>Yield Strength (MPa)<br>**----- End of picture text -----**<br>

Fig. 6. Near-term materials such as HT9 could be used for LIFE.1, with ODS-FS materials, such as 12YWT, being used on LIFE.2 and enabling high temperature operations. 

Advantages of liquid Li include its low density and resulting low hydrostatic pressures and stresses.  It has good heat transfer properties (Pr ~ 0.05) and excellent corrosion properties as long as the coolant is maintained in a relatively pure state (e.g., <100 wppm nitrogen). Mass transfer from the hot to the cold leg requires attention, and it may ultimately dictate the maximum temperature rise allowed within a given cooling circuit.[9 ] 

Lithium melts at only 181°C, and thus freeze-up is less of a concern than for LiPb or molten salt coolants. Li has the widest spread between its melting and boiling temperatures of any element.  Its low viscosity and density and high specific heat result in a low pumping power. 

Lithium is a low-activation coolant that offers superior tritium breeding capability.  In fact, the tritium breeding is good enough to allow multiple blanket modules on LIFE.1 to be dedicated to materials testing. Sufficient tritium can be produced without the need for beryllium, which has health and safety, economic, radiation swelling, supply chain, and public perception challenges. 

Lithium’s challenges include its fire hazard and its high solubility for tritium.  The risks related to the former are quite similar to those for all liquid metal systems (e.g. Na, NaK) and can be reduced through prevention, detection and mitigation features such as avoiding water 

in the vicinity of liquid lithium cooling lines and heat exchangers, using steel liners on concrete surfaces that could be exposed to liquid lithium, and using inert gases to avoid Li-air reactions in the event of a leak. Additionally, lithium inventories are segregated to the extent possible. 

Lithium’s affinity for hydrogen isotopes, including tritium, means that permeation is much less of a concern than it is for molten salt coolants. This affinity requires that tritium recovery systems be utilized in order to maintain the tritium inventories to levels that are acceptable from a safety perspective.  Fortunately, such a tritium recovery process was developed and demonstrated in the mid-1970s by Maroni and his group at Argonne National Laboratory.[10] 

The Maroni process works by intimately contacting the liquid lithium with a molten lithium salt such as LiClKCl. The lithium and salt are subsequently centrifugally separated, and the tritium is removed as a gas following electrolysis of the salt.[10] Figure 7 shows a schematic of the tritium recovery process. 

![Fig. 7. Tritium can be removed from liquid lithium by intimate contact with a molten salt and subsequent electrolysis of that salt.](images/tmpd8v1iugk.pdf-0007-03.png)

All parts of the Maroni process were demonstrated, however, they were not integrated into a complete system. For LIFE, full flow processing of the lithium can limit the tritium content to only 100 weight parts per billion (wppb). This would require approximately eighty units such as those built and demonstrated by Maroni (45 cm in height and 25 cm in diameter).  An integrated system would occupy approximately 30 m[3] , including piping and redundancy.  The power consumed would be only ~ 1 MWe.  With this process, the total tritium inventory within the lithium loops is expected to be only ~ 40 g. 

## **V. NEUTRONICS PERFORMANCE** 

## **V.A. Tritium Breeding and Chamber Energy Gain** 

The LIFE chamber design easily produces sufficient tritium without the use of beryllium or lithium isotopic enrichment.  The current point design has a tritium breeding ratio (TBR) of 1.59 and a chamber energy gain 

of 1.10.  The chamber energy gain is defined as the ratio of the sum of the nuclear heating (neutrons and neutroninduced gamma-rays), x-ray heating and debris heating to the initial energy of 17.6 MeV that is released from every fusion reaction.  Note that this is called the “chamber energy gain.”  Blanket energy gain would be an inaccurate label due to the fact that a significant portion of the gain occurs within the first wall. 

Past studies have shown that excess TBR can be traded for additional energy gain.[11-12] Ongoing work has achieved a chamber energy gain, including penetrations for beamports, target injection and pumping, as high as 1.23 while reducing the TBR to 1.05.  Optimization of the chamber energy gain, TBR, and thermal efficiency is underway.  From a first order systems analysis perspective, the product of the chamber energy gain and the thermal-to-electric conversion efficiency is the figure of merit.  While exceptionally high chamber energy gains may be achievable, these may require the use of materials that limit the maximum temperature, and thus, the thermal efficiency of the chamber.  In combination, we estimate the product of chamber energy gain and thermal conversion efficiency to be in the region of 0.6. 

## **V.B. Waste Management** 

If used with published compositions, HT9 steel would not qualify for disposal via shallow land burial as specified by Fetter et al.[13] The use of 1% molybdenum leads to large production of[99] Tc, which is a waste disposal hazard.  Past work has demonstrated that tungsten can be substituted for the molybdenum found in HT9.[14] By reducing both the Mo and Nb (produces[94] Nb) impurities to the parts per million levels, it is possible for modified-HT9 to qualify for shallow land burial after 1-4 fpy of operation on LIFE.1. Such a composition is amenable to manufacture using existing production processes. A similar level of impurities must be achieved for 12YWT or alternate ODS-FS materials to qualify for shallow land burial after years of operation on LIFE.2. 

## **V.C. Residual Dose Rates** 

12YWT and other ODS-FS materials have acceptable residual dose rates that will enable the use of remote equipment for their routine maintenance.  Figure 8 shows the residual dose rate, following 1 fpy of LIFE.2 operation, at the back surface of the blanket once the lithium coolant has been drained.  Within several hours, as[56] Mn decays with its 2.6-hour half-life, the residual dose rate falls to less than 10[4] Gy/hour.  An additional order of magnitude reduction is achieved by ~ 10 days of decay as[187] W decays with its 24-hour half-life.  Beyond approximately 4 days of decay,[54] Mn (312-day half-life) dominates the residual dose rate. 

## **VI. ACCELERATED DAMAGE TESTING** 

The LIFE.1 chamber, which will be constructed from modified-HT9 or a similar material, will experience a damage rate of 10 dpa/fpy and will likely have a lifetime in the range of 1-2 fpy.  Although there is significant nuclear experience with HT9, there is relatively little with the ODS-FS materials and a testing campaign is needed. While 12YWT and other ODS-FS materials can be tested to a certain extent using currently available reactors and methods such as ion beam irradiation, an adequate 14 MeV neutron source is not available at this time. Rather than waiting for construction of expensive, dedicated fusion materials testing facilities, we propose to use the LIFE.1 facility as a platform to test structural materials and even integrated components for use on LIFE.2 and subsequent facilities. 

![](images/tmpd8v1iugk.pdf-0008-02.png)

**----- Start of picture text -----**<br>
Sc-46<br>V-52<br>4 hours 7 days Mn-54<br>Mn-56<br>10 [5] Fe-59Co-58<br>Co-60<br>Y-88<br>10 [4] Ta-182<br>W-187<br>Total<br>10 [3]<br>10 [2]<br>10 [1]<br>10 [0]<br>10 [-1]<br>10 [0] 10 [1] 10 [2] 10 [3] 10 [4] 10 [5] 10 [6] 10 [7] 10 [8]<br>Time after shutdown (seconds)<br>Dose rate (Gy/hour)<br>**----- End of picture text -----**<br>

Fig. 8. Residual dose rates from the LIFE chamber fall to remote maintenance levels within ~ 4 hours of decay. 

LIFE benefits from the fact that samples and even components can be placed closer to the fusion source and be exposed to increased neutron damage rates without quenching or otherwise significantly distorting the fusion plasma.  As a result, it is possible to complete many cycles of sample exposures during a relatively limited testing timeframe.  For example, by placing samples ~75 cm from the center of the LIFE.1 chamber, one can provide a 10× damage rate increase relative to the expected LIFE.2 first wall damage rate.  If 10% of the solid angle is devoted to such a test (possible given the exceptional TBR from liquid Li), then a front-facing area of 0.7 m[2] could be accommodated.  Such a component, if flat and square in cross section, would experience a 1.3× variation in the damage rate from the center to the corner. This is quite similar to the 1.2× variation expected in the largest sections of a LIFE.2 blanket module. 

The use of smaller components and/or reduced acceleration rates can limit the damage gradients, if desired.  For example, 10 cm samples could be tested at a 20× damage rate acceleration with <1% variation across their surfaces. 

Although the LIFE.1 system availability will likely be low in the beginning, it is reasonable to expect there will be a total of ~1.5 fpy during years 2-6 of its operation.  By accelerating the damage by 10×, LIFE.1 can provide the equivalent of ~15 fpy of exposure. Assuming a conservative lifetime limit of only 2 fpy (equal to 50 dpa), many cycles of exposure can be provided during this 5-year operational window.  It is envisioned that accelerated testing would be completed in phases that include material coupons, samples with welds or other joining methods, and sub-scale integrated components. 

A detailed design of the LIFE.1 Accelerated Damage Testing (ADT) system is currently underway.  Significant challenges faced by the ADT system and program include handling the increased thermal load (12 MW/m[2] rather than the 1.2 MW/m[2] level expected at the LIFE.2 first wall), neutron damage gradients, remote maintenance, and multi-scale materials modeling.  Fortunately, the ADT has reduced requirements in other areas: it does not have to breed tritium due to the superior TBR in the rest of the LIFE.1 blanket, and its thermal shield does not need to operate at high temperatures since thermal conversion efficiency is not a consideration. 

Risks associated with accelerated testing will be mitigated in a couple of ways.  First, ADT samples will not all receive a 10× acceleration; instead, there will be a variety of damage rates in the samples.  These will likely range from 0.4-10×.  This broad range of data will enable development of a sufficient understanding of ratedependent effects.  Second, it is important to note that the ADT program will include extensive use of fast fission and ion beam facilities for code development and validation purposes. 

Finally, once ADT results are used to provide the initial qualification of LIFE.2 structural materials, it will be possible to continue ADT operations and provide additional data that might support a “lifetime extension” to damage levels beyond 50 dpa. 

## **VII. CONCLUSIONS** 

A LIFE point design has been developed along with a LIFE delivery plan.  A pre-commercial plant, LIFE.1, will demonstrate full integration of LIFE systems as well as provide a materials testing platform to support material selection for LIFE.2.  Commercial plants could be either pure fusion or fusion-fission hybrid machines. Construction and operation of LIFE.1 is relevant to both options. 

The selection of indirect-drive targets is not only interesting due to the ability to test such targets on the NIF.  Due to their compatibility with relatively high chamber gas pressures, indirect-drive targets also offer a solution to the chamber ion damage problem that plagues direct-drive concepts.  Both target injection and laser beam propagation are consistent with high-Z chamber gas densities of 1-10  g/cc.  By averting ion damage and greatly reducing thermal pulsing at the first wall, gasprotected chambers avoid the need for refractory armor and offer compact, maintainable chambers that can be constructed from near-term materials. 

Through factory-built, modular chamber design, it is possible to reduce costs, speed maintenance and reduce the risks associated with materials selection for a hostile environment.  Simple, easy-to-fabricate designs and rapid maintenance due to minimal connections in the engine bay significantly mitigate the uncertainties associated with materials performance and survivability.  This increases plant availability relative to past ideas. 

Use of liquid lithium with demonstrated, compact tritium recovery technologies provides a low radiological hazard due to low inventory and low permeation without use of beryllium.  Lithium’s exceptional tritium breeding enables use of a large solid-angle fraction on LIFE.1 for accelerated damage testing of LIFE.2 materials as well as offering the possibility of high chamber energy gains on LIFE.2 and beyond.  Lithium’s high-temperature compatibility with tungsten offers a high-efficiency blanket option utilizing insulating panels. 

Accelerated damage testing can be performed on LIFE.1 without negatively affecting the fusion plasma.  A robust program utilizing multiple irradiation sources (fast fission and multi-beam ion) and multi-scale materials modeling is needed to enable use of LIFE.1 damage rates that are as high as 10× that expected during LIFE.2 operations.  The ability to perform materials qualification on LIFE.1 during the 2020s is a key element in the plan to deliver commercial fusion energy in the 2030s, which is consistent with the expected needs of the marketplace. 

## **ACKNOWLEDGMENTS** 

This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Security under contract DE-AC52-07NA27344. 

## **REFERENCES** 

1. E. MOSES, T. DIAZ DE LA RUBIA, J. F. LATKOWSKI, et al., “A Sustainable Nuclear Fuel Cycle Based On Laser Inertial Fusion Energy (LIFE),” _Fusion Science and Technology_ , **56** , 2, 566572 (2009). 

2. T. ANKLAM, A. J. SIMON, W. R. MEIER, and S. S. POWERS, "LIFE Economic and Commercial Pathway," this issue (2011). 

3. K. J. KRAMER, J. F. LATKOWSKI, R. P. ABBOTT, et al., “Neutron Transport and Nuclear Burnup Analysis for the Laser Inertial Confinement Fusion-Fission Energy (LIFE) Engine,” _Fusion Science and Technology_ , **56** , 2, 625-631 (2009). 

4. K. J. KRAMER, M. FRATONI, J. F. LATKOWSKI, et al., "Fusion-Fission Blanket Options for the Laser Inertial Fusion Energy (LIFE) Engine," this issue (2011). 

5. R. MILES, M. SPAETH, K. MANES, et al., "Challenges Surrounding the Injection and Arrival of Targets at IFE Target Chamber Center," this issue (2011). 

6. S. J. ZINKLE and N. M. GHONIEM, "Operating temperature windows for fusion reactor materials," _Fusion Engin. Des._ **51-52** (2000) 55-71. 

7. M. S. TILLACK and S. MALANG, "High performance PbLi blanket," Proc. 17[th] IEEE/NPSS Symp. on Fusion Energy, San Diego, CA (1997) 1000-1004. 

8. Process Piping: ASME Code for Pressure Piping, B31, The American Society of Mechanical Engineers, 2008. 

9. J. E. SELLE and D. L. OLSON, "Lithium Compatibility Research -- Status and Requirements for Ferrous Materials," presented at the National Association of Corrosion Engineers Annual Meeting, Houston, TX (1978). 

10. V. A. MARONI, R. D. WOLSON, and G. E. STAAHL, "Some Preliminary Consideration of a Molten-Salt Extractions Process to Remove Tritium from Liquid Lithium Fusion Reactor Blankets," _Nucl.Technol._ 25 (1975) 83 and MARONI, V.A., "Process for Recovering Tritium from Molten Lithium Metal," United States Patent 3,957,597, May 18, 1976. 

11. E. GREENSPAN and S. K. HO, "Blanket Energy Multiplication Enhancement Without Afterheat Safety Hazards," Proceedings of the Thirteenth IEEE Symposium on Fusion Engineering, Knoxville, TN (1989) 62-65. 

12. W. R. MEIER and E. C. MORSE, "Blanket Optimization Studies for the HYLIFE ICF Reactor," LLNL Report UCRL-91522 (Sept. 1984), _Fusion Technol_ . **8** (1985) 2681. 

13. S. A. FETTER, E. T. CHENG, and F. M. MANN, "Long-term Radioactive Waste from Fusion Reactors: Part II," _Fusion Eng. Des._ **13** (1990) 239246. 

14. R. L. KLUEH and E. E. BLOOM, "The development of ferritic steels for fast induced-radioactivity decay for fusion reactor applications," _Nucl. Eng. Des._ **2** (1985) 383-389. 

The image appears to be a blank white page with no visible text or content to extract.