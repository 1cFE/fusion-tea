---
source: "https://www.osti.gov/servlets/purl/3008974"
source_type: "url"
extracted_at: "2026-04-20T16:40:10.329981+00:00"
content_hash_sha256: "7155beed1181bfca4962c5a0158cb1a146bb7d33670d9d15b285a30503161997"
backend: "pdf_pipeline"
---

LLNL-JRNL-2008670 

![](images/tmptsec273q.pdf-0001-01.png)

Diode laser pumps for future inertial fusion energy systems: status and perspectives 

W Fenwick 

December 2025 

Optics Express 

## **Disclaimer** 

This document was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor Lawrence Livermore National Security, LLC, nor any of their employees makes any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or Lawrence Livermore National Security, LLC. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or Lawrence Livermore National Security, LLC, and shall not be used for advertising or product endorsement purposes. 

This work performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. 

## **Diode Laser Pumps for Future Inertial Fusion Energy Systems: Status and Perspectives** 

**P. CRUMP[*(1)] , W. FENWICK[*(2)] , M. ELATTAR[(1)] , I. TAMER[(2)] , K. HÄUSLER[(1)] , M. NELSON[(2)] , J. E. BOSCHKER[(1)] , A. KNIGGE[(1)] , AND R. J. DERI[(2)]** 

_(1)Ferdinand-Braun-Institut (FBH), Gustav-Kirchhoff-Str. 4, 12489 Berlin, Germany_ 

_(2)Lawrence Livermore National Laboratory (LLNL), 7000 East Ave. Livermore, CA 94550, USA_ 

_*paul.crump@fbh-berlin.de; fenwick2@llnl.gov_ 

**Abstract:** Diode laser pumps are a critical enabling technology for inertial fusion energy (IFE), and will remain the largest contributor to facility cost, even assuming tenfold cost-reduction at high volumes. An overview of diode requirements for IFE and a technology path to achieve them are presented. 

© 2025 Optical Society of America under the terms of the OSA Open Access Publishing Agreement 

## **1. Introduction** 

We present here a collected overview of the technology status and development perspectives of diode laser pump sources for use in inertial fusion energy (IFE) systems, with special focus on the GaAs-based diode lasers themselves, as a critical enabling technology. Although such diode lasers are already the most efficient technology for generating light and the basis for world’s largest laser market (material processing), substantial performance and cost improvement are needed for economic power generation via IFE, with key open challenges and their potential solutions summarized here, expanding on an earlier review [1]. The article is structured as follows. We first summarize the current state of knowledge on diode laser requirements for IFE, noting the scaling needed in power, efficiency, and cost. Next, we present an analysis on prospects for cost reduction, with special focus on the benefit of manufacturing scaling of existing production, whilst also noting status on the potential benefit of emerging technologies such as monolithic grating stabilization (to eliminate wavelength loss) and connected metrology (to eliminate yield loss early in wafer processing). Parallel to cost reduction, efforts to advance diode laser design and technology to enable substantial power scaling (and hence cost reduction in $/W) are essential and are presented next, being especially important where these are possible without compromising suitability for high-volume low-cost manufacture. Topics covered here include rapidly emerging multi-junction laser designs and progress in facet passivation. In contrast, although efficiency scaling remains challenging, promising approaches for incremental scaling to levels above 70% are also summarized. Finally, we review the status of reliability studies of the quasi-continuous-wave stacked arrays, emphasizing the significant gap between published performance and IFE requirements, and suitable approaches for qualification efforts as the field develops. 

## **2. Overview on laser diode performance requirements** 

Recent experiments employing the world’s most energetic pulsed laser system at the National Ignition Facility (NIF) have demonstrated robust, repeatable fusion ignition events, producing higher fusion yields than the laser energy directed into the target capsule [2,3]. Although the currently utilized NIF beamline energy (> 10 kJ) and shaped nanosecond pulse formats are already anticipated to meet the requirements [4] for future beamlines in power plant applications, substantial advancements in repetition rate (≥ 10 Hz) and wall-plug efficiency (≥ 10%) will be required to achieve sustained and economically viable power generation through IFE [5]. 

Diode-pumped solid-state lasers (DPSSLs) offer a promising path to achieve the necessary performance metrics of IFE beamlines; however, considerable challenges remain for multiple 

DPSSL design aspects, in addition to efficiency and cost, including optics and coating survivability, thermal management, compactness, optical bandwidth, cooling complexity, and crucially, pump system performance and lifetime. The core enabling components of DPSSL pump systems are the semiconductor diode lasers: modular, high brightness sources utilized to deliver optical energy into gain materials that amplify the laser beam. Fig. 1 depicts the application of diodes for DPSSL architectures applicable to future IFE power plants. Here, diodes are fabricated in large numbers as 1-cm wide laser bars, containing multiple emitters and producing total peak powers of approximately 500 W/bar in volume manufacture and 1 kW/bar at industrial prototype level, and are subsequently assembled into stacks. These stacks are then assembled into arrays and installed in pairs around each laser amplifier head within a DPSSL beamline. In a similar manner to the NIF, 100’s of laser beamlines are anticipated for an IFE power plant. Previous comprehensive investigations at LLNL under the LIFE effort [68] have assessed total diode peak power requirements up to ~50  GW per plant, with similar conclusions reached in the EU under the HIPER effort [9]. At 1 kW/bar operating power, this would necessitate the fabrication and installation of approximately 50 million laser diode bars, thereby emphasizing the importance of continued diode development towards, e.g., improved power density (higher W/bar) and reduced cost (lower $/W). 

![Fig. 1: Schematic depicting the application of diode laser bars for IFE. Diode laser bars are fabricated in large numbers, assembled into stacks and arrays, and employed to pump the amplifiers of high power DPSSL beamlines within a future IFE power plant. _(Stack image courtesy of Leonardo Electronics, Inc.)_](images/tmptsec273q.pdf-0004-01.png)

In addition to peak power and cost improvements, multiple key diode performance metrics must be simultaneously satisfied for IFE power plant applications. Leveraging the developments of prior investigations, updated assessments of IFE DPSSL and diode requirements are currently being conducted at LLNL, considering both upscaled versions of previously demonstrated architectures, as well as new, advanced beamline concepts. Here, a beamline design approach similar to that of the LIFE study has been taken, and improved upon by employing updated beamline modeling and optimization capabilities, as well as expertise from multiple LLNL DPSSL programs. While exact diode requirements depend on the DPSSL architecture and gain material selection – based on, e.g., allowable operating fluence, impact on cooling complexity, and material availability at-scale – the parameter ranges detailed in Table 1 describe our current understanding of diode performance requirements for 10  kJ (3ω), high repetition rate (10 - 20 Hz) beamlines for IFE. 

**Table 1: Anticipated Diode Performance Requirements for 10 kJ (3ω), 10 - 20Hz IFE DPSSLs** 

|**Laser Material**|**Nd:glass**|**Yb:YAG**|
|---|---|---|
|Center Wavelength, Tolerance [nm]|869 ± 3|940 ± 3|
|Bandwidth (95% Energy Enclosed) [nm]|≤ 10|≤ 6|
|Peak Power Per Beamline [MW]|190**– **240|50**– **90|
|Pulse Duration [µs]|230**– **440|450**–**1100|
|Diode Array Peak Power Density [kW/cm2]|≥ 18|≥ 7|
|Fast-Axis**× **Slow-Axis Divergence (95% Energy Enclosed) [°]|≤ 6**×**10||
|Electrical-to-Optical Efficiency [%]|≥ 70||
|Polarization Purity [%]|≥ 90||
|Diode Replacement Lifetime [×109Shots]|3**–**20||

The diode performance requirements identified in Table 1 are anticipated to change, or become more narrowly defined, as investigations into DPSSL beamline designs continue. The requirements have been developed for architectures based on selected laser materials that have been previously explored in detail through the LIFE and HIPER studies – specifically, Nd:glass and Yb:YAG – and are not intended to exclude other potential candidate materials for future consideration. Nevertheless, both laser materials listed in Table 1 exhibit spectroscopic and thermal management properties that have enabled their application in multiple high power pulsed DPSSLs [10,11], each indicating important milestones towards the development of future IFE-scale beamlines. A detailed breakdown and comparison between the material properties are provided in Table 2 of [8], and is otherwise not the focus of this paper. 

Employing a similar methodology as with the LIFE design, the diode requirements on central wavelength, bandwidth, and wavelength tolerance have been selected by evaluating the shape and thermal dependence of the laser material absorption properties, as well as by balancing designs across multiple amplifier constraints, e.g., the total absorption and extractable stored energy across each slab group, the maximum transverse gain and temperature rise per slab over the diode pulse duration, and more. While the central wavelength tolerance remains unchanged for both materials due to the amplifier design considerations above, the broad absorption band of Nd:glass allows for larger diode emission bandwidths of ≤ 10 nm (95% energy enclosed, averaged across the diode array), compared to Yb:YAG with ≤ 6 nm bandwidth. However, the longer fluorescence lifetime [8] of Yb:YAG compared to Nd:glass allows for high energy storage with longer pulse durations, thereby decreasing required diode peak power. While the longer Yb:YAG lifetime is attractive, this material must be operated at much colder temperatures (~200 K or lower) compared to Nd:glass (~320 K), which adds significant additional costs and efficiency losses associated with the cooling infrastructure. 

The required diode peak power will depend strongly on details of the IFE system, notably total energy output, target gain, and required DPSSL efficiency. The specified diode peak powers and pulse duration ranges in Table 1 are each sufficient for pumping 10 kJ (3ω), 10 - 20 Hz DPSSLs, yet result in different wall-plug efficiencies. These values are higher than those reported in the LIFE design [7], as Table 1 assumes a beamline with approximately twice the pulse energy to conform with updated assessments [4]. For example, with longer diode pulse durations, the same energy can be stored within the laser materials using a reduced quantity of diode arrays. However, as pulse durations approach and exceed the fluorescence lifetime of the laser material, a larger fraction of the stored energy is fluoresced out of the material prior to extraction, thereby reducing the extraction efficiency and with it, the beamline wall-plug efficiency. While the beamline wall-plug efficiency requirement – taking into account the cooling draw power – has been previously defined at ≥ 10% [4], the first IFE DPPSL demonstration may be operated using more relaxed values from 7% and with longer diode pump 

pulse durations, primarily due to schedule and cost constraints. However, the tradeoff is that operating at 7% wall-plug efficiency instead of 10% with a fixed average power would consequently increase the thermal loading within the beamline by over 40%. If the DPSSL is not specifically engineered to manage this increased heat – through advanced cooling techniques and a careful selection of material aperture, thickness, number of slabs, slab doping concentration, and other design parameters – the risk of thermal fracture and laser wavefront degradation rises significantly. These issues limit both the performance and reliability of the laser system and must be addressed to operate under relaxed efficiency conditions at IFE beamline average powers. 

Within future IFE DPSSL beamlines, an optical delivery system must be implemented that transforms the grid-like spatial profile of the diode array into a spatio-spectrally homogeneous pump spot with a sharp edge roll-off and minimized losses due to ghosting effects. The optical delivery system may employ a combination of ducts, diffusers, microlens arrays, or similar homogenizing elements. Here, the diode fast-axis and slow-axis divergence of ≤ 6° and ≤ 10°, respectively, satisfy both the angular acceptance of high power homogenizing elements and the pump beam sharpness requirements throughout the amplifier. At the diode array plane, peak power densities of ≥ 18 kW/cm[2] and ≥ 7 kW/cm[2] for Nd:glass and Yb:YAG, respectively, are required to store sufficient energy density within the amplifier slabs, while simultaneously maintaining both the compactness and performance of the optical delivery system. 

Despite the difference in spectroscopic properties between the laser materials in Table 1, several diode requirements remain consistent across both updated assessments of beamline designs. For example, diode electrical-to-optical efficiency expectations must remain at or above 70% to relax more challenging constraints on both the diode emission (e.g., peak power) and beamline operation (e.g., extraction efficiency). Additionally, while both laser materials are isotropic, a diode polarization purity of ≥ 90% is nevertheless required due to the polarization sensitivity of optical coatings under high power conditions between the diode array and the amplifier slabs (notably, dichroic elements used to overlap the pump laser and 1  laser), as well as to enable polarization beam combining with diode array pairs when peak power density requirements cannot otherwise be achieved [7]. 

The requirement on diode lifetime for IFE plant applications is not simply set by the expected IFE plant operational lifetime of 30 - 60 years to achieve economic viability. The plant operation lifetime sets an upper limit on the diode lifetime requirement of ~10 - 20 Gshots, assuming 10 Hz operation. 

Prior IFE power plant design studies have explored utilizing a modular framework, enabling replacement of plant components without materially impacting plant operations or performance [6-8]. This results in the integration of more beamlines than are minimally necessary to operate the plant. The additional beamlines come into operation when maintenance is required on beamlines, such as would be the case with diode replacements, resulting in very minimal, if any, impact on plant operations when diode replacement is necessary. Using line-replaceable beamlines that can be swapped during plant operation, diode replacement lifetimes can be much shorter than the plant operational lifetime. The tradeoff is that plant operating costs will increase due to periodic diode replacement. Optimizing this tradeoff depends on requirements for the levelized cost of electricity (LCOE) and associated financing costs, in addition to the replacement costs of the diodes themselves. By making these tradeoffs, diode replacement lifetime requirements may be reduced to several times shorter than the plant operation lifetime. 

## **3. Production scaling for purchase cost reduction** 

Several studies have shown that semiconductor laser diode (LD) costs are one of the strongest lever arms on IFE plant economics [5,6,12,13].  They show that LDs will account for at least one third to one half the cost of Nd:glass DPSSL beamlines, even when DPSSLs are produced at IFE scale and the LD cost is ~$0.01/W  At this time, at today’s considerably lower production 

volumes, LD costs are appreciably higher (typically $0.3/W to $1.3/W) [14], and are expected to comprise a larger fraction of the cost of early demonstrator beamlines and facilities.  For these reasons, the U.S. Department of Energy has identified LD cost as a gap in fusion enabling technologies [4]. 

LD manufacturing flow can be divided into three high-level, sequential process blocks: epitaxial growth, bar fabrication (wafer processing, thinning, cleaving, and coating to produce bars), and stack assembly (bar-to-submount attach, electrode and base attach, and lensing to produce stacks).  Epitaxial growth and wafer process cost reductions are achievable with capital investments, since similar process tools are used in other high-volume manufacturing (e.g.; LEDs, cell phone power amplifiers).  Other manufacturing steps are more specific to edgeemitting stacks and supported by a smaller ecosystem, with a critical capacity and performance bottle neck being facet passivation technology, that suppresses failure at the output surface and allows reliable operation to high powers (see section 4).  Advanced techniques in process control via methods such as in-situ optical-sensing-based connected metrology [15] and AIassisted process (visual) defect identification [16] show promise for yield increase and cost reduction, as they can quickly identify issues early in the process chain, before assembly and test takes place. Advances in process control metrology are likely to be especially important for realizing the complex, very thick epitaxial layer structures used in multi-junction diode laser with high yield and low cost. 

In contrast to silicon integrated circuits (ICs), LD manufacturing costs for high-power, edge-emitting LD stacks are dominated by packaging costs, which contribute well over 50% of the stack cost [5,6].  High packaging cost results in part due to the tight alignment tolerances (typically < 10  m) required for mounting bare LD bars to metal submounts and aligning fastaxis collimation (FAC) lenses to the bars.  These tolerances are currently not achievable using the pick & place tools used in IC manufacturing.  FAC attach typically employs active alignment, with the LD powered on, requiring moderately expensive production tools with relatively slow throughput.  Certain components used in the stack package also add significant cost.  These include the expansion-matched CuW submounts and FAC collimators, which typically have stringent mechanical tolerances.  Because packaging costs are so important, classic semiconductor cost-volume scaling strategies (larger wafer diameter, automated wafer processing, cluster tools, etc., see e.g. [17]), although important to enable sufficient throughput from a given facility, will have less impact on the cost of LDs for IFE.  IFE LD costs can be reduced by automating bar attach and collimator alignment/attach; while such tools have been developed, e.g. [18–20], and are in use at several manufacturers, the modest demand for such tools currently increases their capital costs and limits widespread use. While increasing utilization and improvements in automation technology should reduce the cost of these tools, their cost is likely to remain significantly greater than that of conventional pick & place machines due to the increased complexity required to achieve tighter alignment tolerances. 

An additional factor contributing to LD stack costs is the yield at or near final assembly, when process fallout results in discarding high value, nearly completed stacks.  Requirements on the stack emission spectrum, which flow down from beamline requirements for high absorption in the DPSSL gain medium, can contribute significantly to such fallout because of the challenges with predicting final spectral characteristics from measurements on unmounted bars. 

For a fixed number of packaged bars, LD pump fabrication costs in $/bar are roughly constant and relatively insensitive to the output power per bar (W/bar); increases in epitaxial layer thickness and cavity length at higher bar powers add small cost changes relative to packaging costs.  Since a given DPSSL design will require a fixed amount of diode pump power (in watts) while the pump fabrication cost per bar ($/bar) is weakly sensitive to bar power, maximizing bar power is an attractive approach to mitigate IFE pump LD costs in $/W [1]. This strategy can leverage recent advance in bar power, which has been demonstrated at levels exceeding 1 kW/bar [21,22]. The limitations to this strategy are set by reductions in pump 

electro-optic efficiency and lifetime as bar power increases, as discussed in sections 5 and 6 [1,23]. For this reason, development of higher power LD bars that maintain high efficiency and lifetime is of particular importance for IFE.  A promising approach to such scaling is the use of multi-junction bars, which layer several _p-i-n_ LD junctions on top of each other in a single set of epitaxial layers, connected via a series of tunnel junctions [24–30]. Along similar lines, the actual requirement to meet DPSSL output energy involves storage of a fixed amount of pump _energy_ (rather than power) to the gain medium.  Thus, operating the pump LDs with longer pulse-widths can also mitigate LD costs.  For a fixed gain medium, this approach is limited by the gain medium’s excited state lifetime; that is, DPSSL efficiency is reduced to excited state decay during the pump pulse-width.  As discussed in section 2, an approach to leverage potential cost reductions with longer LD pulse-width involves the use of gain media with longer excited state lifetimes; e.g. Yb-doped media instead of Nd-doped media. However, some longer lifetime materials require operation at much lower temperatures (e.g.; ~200 K), for which the cooling subsystem adds system cost and reduces overall system efficiency.  Quantitative tradeoffs at the DPSSL level involving pulse-width selection have been explored elsewhere [8]. At the stack level, longer pulse-widths increase heat loads on the bars and may require package modifications to improve thermal management and control spectral width [31,32]. 

In addition to the benefit of power scaling, the evolution of IFE LD costs will be a strong function of cumulative production volume (“learning”) and production rate (“economies of scale”) [5,6,12,13]. “Learning curve” scaling models describe price evolution with increasing demand over time, and have successfully described cost evolution across many technologies and industries using a small range of scaling exponent values; e.g. [33].  The cost scaling in these models include both “learning” associated with improved designs, manufacturing processes, and yields as well as volume scaling of subcomponent costs at higher volumes. Based on observed scaling exponents of 0.4~0.6, such models indicate that LD costs below $0.01/W for IFE are highly likely, provided that a sustained market for DPSSL-driven IFE develops with 1,000x increase in demand from today.  While such models do not describe the rate at which costs decrease, recent experience with LEDs for both general lighting and display backlighting has shown that costs can decrease rapidly (over just a few years) for similar components, under favorable market conditions [6,13,34,35]. 

Once a clear, sustained market demand for IFE LDs emerges, volume learning and scaling can achieve LD costs near those required for economically feasible IFE plants.  The primary challenge for IFE is achieving sufficiently low LD costs in the near term, to facilitate building the intermediate demonstration systems needed to prove out IFE.  These systems range from single beamlines to the first IFE plant.  During this interim period, uncertainty about the future IFE market may limit investment in production tooling to lower manufacturing costs.  For this reason, technological solutions that can be implemented without large capital outlays will be important. These include increasing bar power, yield and fabrication cost of the diode lasers, cost-reduced packaging designs and subcomponents, and methods to improve the effective yield at stacking. 

Since the complete pump subsystem includes both the laser diodes pumps as well as their drive electronics, it is worth briefly addressing diode driver costs.  Cost estimates for the LIFE design [7] indicated that driver electronics will contribute approximately 15% of the pump diode cost to an IFE facility, after diode costs have decreased due to volume learning and scaling.  This value assumed the use of tantalum-based capacitors to maximize energy storage density and minimize the volume of the driver circuity.  Since capacitors dominate the overall driver costs, driver costs can be significantly (>40x) reduced by using aluminum electrolytic capacitors, with the tradeoff of increased driver footprint. 

## **4. Scaling semiconductor capability: Facet passivation as critical enabling technology** 

For edge emitting diode laser, the optical output surface, the front facet, is a location of critical failures, and one of the major limits to achievable reliable output power. To protect this region against failure, various forms of facet passivation technology are available, that hinder failure, at cost of greater process complexity, so that passivation is typically a significant fabrication bottle neck. Reliable operation at the _P_ opt ≥ 1 kW targeted for IFE application is only possible if some form of facet passivation is used.  In this section we discuss laser facettechnologies that are suitable for high volume production of laser bars. In particular, we focus on facet-technologies that are suitable for multi-junction bars, because this is one of the most promising paths for realizing low cost ($/W) bars (see section 5). Catastrophic optical mirror damage is one of the main failure modes that limit the output power of 1-cm laser bars and it is expected that this remains the case for multi-junction bars. 

A well-known early technological breakthrough that enabled the stabilization of the laser facets and the commercial application of GaAs-based diodes in high reliability application is the cleaving of laser bars in vacuum and the subsequent deposition of an amorphous silicon layer to prevent oxidation of the III-V semiconductor once exposed to air [36]. This process is known as the E2-process and results in highly stable laser facets. One drawback of this method is the use of amorphous silicon, because it absorbs light that has an energy above its bandgap, so that the silicon layer thus has to be as thin as possible. Unfortunately, it cannot be made too thin, because it will lose its protective properties and degrade the lifetime of diode lasers [37]. Recently, it was shown that this lower limit can be overcome by using superlattice structures consisting of Si/SiO2 layers with very thin Si layers [37]. Importantly, the quantum confinement of the silicon layers results in a bandgap increase and thus reduces the absorption in the layer. An additional improvement of this configuration is obtained due to the formation of a crystalline silicon layer at the facet either by laser operation or ex-situ conditioning [37,38]. Lattice matching with the III-V semiconductor can be achieved by using germanium instead of silicon, but at the costs of a reduced optical bandgap. Alternatively, epitaxial ZnSe can be grown on the laser facet after vacuum cleaving [39,40]. Due to the small lattice mismatch between GaAs and ZnSe the interface between ZnSe and GaAs has a low defect density, resulting in a high facet stability. An advantage of this approach is that is does not require conditioning by laser operation or other methods. The drawback is that the epitaxial growth requires temperatures of around 250°C and is thus more time consuming compared to a deposition at room temperature and adds to the thermal budget of the materials. 

A general drawback of vacuum cleaving is the difficulty of handling bars within vacuum. This requires specialized jigs and sophisticated automated tools for cleaving and handling the bars that are expensive, slow, and not necessarily compatible with further processing steps. This requires a handling step between the passivation and optical coating of the bar, limiting throughput and adding to their costs. In order to overcome these challenges atomic hydrogen cleaning with subsequent ZnSe passivation was developed. This method allows for cleaving and stacking in air, while maintaining a high facet stability [41]. For example, 20 W (CW) 980 nm broad area single emitters with an aperture of 96 µm were shown to have a lifetime exceeding 4000 hours [42]. A drawback is the large thermal budget of the method. Furthermore, it is currently unclear how facet stability obtained by this method is affected by the high aluminum content of laser structures used for wavelengths below 900 nm. This is potentially critical, because atomic hydrogen is not suited for removing the stable native oxides formed after cleaving on the surface of high Al-content layers (AlOx). 

We illustrate here the potential of ZnSe-based facet passivation for use at  < 900 nm. In Fig. 2, we show ongoing aging experiments performed at the FBH using 880 nm broad area lasers with a 200 µm aperture and 4 mm resonator length, where the diodes are operated in quasi-continuous wave (QCW) mode, to enable higher output powers to be reached and hence to assess the limits of the passivation. Here, a single-junction epitaxial layer design was used. 

The broad area emitter is operated at 50 A and produces 40 W of optical power. This would correspond to _P_ opt = 1.5 kW/bar, when around 35 emitters are included per bar. Two failures occurred during the initial 0.5 Gshot (=10[9 ] shots), whereas three diodes are currently still functional and two have surpassed 1 Gshot. Even though this is still far off from the requirement for fusion (10-20 Gshot), it demonstrates the potential of operating 880 nm diode lasers at the power levels required for kW-bars for a prolonged period of time. Further improvements can, for example, be expected by using more efficient epitaxial laser structures. Currently, state of the art passivation systems for hydrogen cleaning are based on 4” molecular beam epitaxy systems, whereas ion beam systems used for the deposition of optical coatings are generally suited for platens of 8” or larger. This implies that there is a capacity difference between the passivation systems and the coating systems. This can be overcome by increasing the size of the passivation system. This could contribute to a cost reduction of the bars due to the higher capacity of such systems, at higher investment cost. 

We note that a new passivation method based on the formation of an epitaxial oxide layer has become available in recent years [43]. Unfortunately, detailed performance analysis of high-power broad area lasers with this technology are not available, making it difficult to assess it suitability for high power applications using multiple junctions. 

![](images/tmptsec273q.pdf-0010-02.png)

**----- Start of picture text -----**<br>
50 A  40 W<br>250 µs  100 Hz<br>15°C<br>**----- End of picture text -----**<br>

Fig. 2: QCW aging of five 880 nm broad area single emitters using the indicated parameters. 

Even though the use of a facet passivation improves the reliability of laser diode, the use of facet passivation systems significantly adds to the costs of a high-power laser bar. Technologies that realize a high facet stability without requiring an additional passivation system are therefore desirable. The creation of a non-absorbing mirror (NAM) region by quantum well intermixing [44], epitaxial regrowth [45] or other methods [46] are therefore of interest. Using quantum well intermixing (QWI), 20 W (CW) 915 nm broad area lasers with an aperture of 100 µm and lifetime exceeding 5000 hours were demonstrated [47]. An advantage of this technology is that it can be performed at the wafer level. A downside of this method is the undesirable wavelength shift that occurs upon annealing outside of the NAM-area. This makes it more complicated to control the emission wavelength  of the diode lasers across a wafer. At the moment, the use of QWI on multi-junction bars has not been demonstrated yet. Given the increased complexity of the epitaxial layer structure it is currently not clear if this can be realized and should urgently be studied. 

In summary, we identified three facet-technologies that can be used for high volume production of multi-junction laser bars. The main challenges for these techniques are the following: throughput/costs for vacuum cleaving, facet stability at wavelengths  < 900 nm for hydrogen cleaving (with promising results shown) and the creation of NAM-regions for multijunction bars for passivation free facet-technologies. In all cases lifetime studies on multijunction bars with parameters corresponding to the operation conditions for fusion applications are still lacking and are clearly needed in order to assess the best facet technology for this particular application. 

## **5. Diode power & efficiency scaling for purchase and operating cost reduction** 

In parallel with scaling production volume and process yields, efforts towards performance scaling remain of utmost importance. Maximizing optical power ( _P_ opt) on individual LD bar level means that fewer bars are required to fulfill system requirements, thus significantly reducing purchasing cost, while maximizing electrical-to-optical conversion efficiency (ηE) reduces operating costs. In fact, this approach has historically been the largest contributor to cost reduction [14]. As previously mentioned, the current benchmark in industrial pulsed DPSSL systems is around _P_ opt = 1 kW per 1-cm-wide bar, where power conversion efficiency is around  E = 65%, slightly reduced from peak efficiency of  E = 70% [14,20,48]. In this section, we briefly review recent progress towards power and efficiency scaling in LD bars. Starting with standard broad-area (BA) LD bars operated under QCW conditions at 15 - 25°C, in studies around  = 940 nm, _P_ opt has continued to increase from 1 kW in 2007 [49], to 1.5 kW in 2013 [50] (both actively cooled), to 1.85 kW at 2 kA from a passively-cooled high-fill-factor bar in 2022 [51], as demonstrated in Fig. 3(a), where the peak power is slowly approaching the facet failure power defined by passivation. This was enabled in large part by a strong enhancement of ηE at high _P_ opt levels, with ηE at 1 kW increasing from 35% in 2007 to 66% in 2020 [20, 52]. It remains challenging to reach and surpass ηE = 70% at 1 kW, that to date has only been directly demonstrated at operating temperatures of around 200 K (currently uneconomic for IFE) [53]. Recent research studies offer a path to around  E = 80% at room temperature [48], in the most optimized designs. 

1-cm bars with monolithic wavelength stabilization are potentially attractive for IFE applications, as they bypass one of the largest yield loss terms: wavelength (as noted in section 2). DBR-BA bars fabricated using surface gratings are a promising candidate for extremely high volume application, due to their relatively simple manufacture (no regrowth step) and have been realized, recently exhibiting promising QCW performance with _P_ opt up to 0.88 kW at ~970 nm and 0.8 kW at ~880 nm, albeit to date with reduced  E ~ 55% [54,55]. 

![](images/tmptsec273q.pdf-0011-03.png)

![](images/tmptsec273q.pdf-0011-04.png)

![Fig. 3: (a) Voltage, optical power and conversion efficiency as functions of current for a 940-nm high-fill-factor 1-cm-wide BA-LD bar under QCW operation (200 µs, 10 Hz) at 25°C [51]. (b) Development of reported pulsed optical power for single- and multi-junction 1-cm-wide BA-LD bars, with and without DBR wavelength stabilization, at varying pulse widths (10 ns – 200 µs) and temperatures (10 – 25 °C). (c) is similar to (b), but for multijunction BA-LD single emitters.](images/tmptsec273q.pdf-0011-05.png)

A different approach to epitaxial design of LD bars has demonstrated very promising power scaling potential in recent years, namely epitaxially stacking multiple active laser junctions with tunnel junctions separating them, ideally enabling N-fold higher _P_ opt at the expense of higher voltage and heat density. The rapid development of maximum achievable _P_ opt by multijunction bars relative to their single-junction counterparts is demonstrated in Fig. 3(b), with representative examples further described in the following. 

In one such multi-junction variant, each active junction is surrounded by an independent vertical waveguide, optically isolated from the other junctions, thereby forming a so-called 

“nanostack” LD which is already commercially available, e.g. [56]. Under QCW operation (~200 µs pulse width), the optical power of double-junction nanostack LD bars has successfully scaled in recent years, reaching 1.8 kW at 1 kA in 2017 [24] and 2.7 kW at ~1.35 kA in 2025 [27]. However, the optical isolation of the stacked waveguides means that wavelength stabilization via surface gratings is not applicable, and significant spectral broadening is typically observed. 

This limitation has been overcome using an alternative multi-junction variant, based on integrating the active and tunnel junctions within a single vertical waveguide core, optimized for single higher-order vertical mode emission, with nodes and antinodes overlapping with the tunnel and active junctions, respectively [28]. This technique has demonstrated very rapid power scaling in recent years, albeit mostly at short-pulse LiDAR specifications (~10 ns pulse width) and thus very low heat loads. An early realization of a 3-junction bar with 25% fill factor already demonstrated 2.2 kW at 1.13 kA in 2022 [29]. Further power scaling has been demonstrated on single-emitter (SE) level, with the highest so far being 420 W at 210 A from a 5-junction SE with 200 µm stripe width at 25°C [30]. Extrapolating to a high-fill-factor 1- cm-wide bar with 35 emitters, this proportionally scales to a very high bar power of 14.7 kW at 7.35 kA. Although such a high current supply and the needed bar assembly is difficult to realize in practice, these recent promising results show the potential of this technique for significant power scaling. 

## **6. Scaling of operating / replacement cost: achieving needed replacement and wear-out lifetime** 

Laser diode bars are assembled in stacks for delivering sufficient optical power density for pumping the solid state laser slabs. For laser stacks, besides optical power and drive current, the internal temperature rise can impact the reliability. The temperature rise by self-heating during pulsed operating strongly depends on the conversion efficiency and the thermal management of the laser stack, with the difference in temperature of the diode material between off- and on-states depending strongly on the operating conditions ( _P_ opt, pulse duration  p, repetition rate _f_ ) and details of the stack assembly used [20,57]. 

Over the past decade, GaAs based laser bars and stacks emitting in the range from 800 nm to 980 nm have been improved to achieve reliable high power operation from >110 W (CW) and >160 W QCW for mini bars in year 2012 [58,59] up to > 520 W per bar, assembled in multi-bar stacks of 56 bars, emitting 29 kW at 940 nm for 28 Mshots without degradation, as recently reported in [20]. As mentioned in section 2, the anticipated performance requirements for an economic IFE system are _P_ opt from 500 W to 1 kW per bar, with a lifetime of 3–20 Gshots under QCW pulsed operation at _f_ = 10–20 Hz and  p between ~200 µs and ~1000 µs, corresponding to duty cycles in the 0.2–2% range. As discussed in section 5, there are clear paths towards fulfilling and surpassing these requirements using 1-cm-wide wavelengthstabilized bars with high fill factor, e.g. 35 emitters with 200 µm stripe width, which corresponds to _P_ opt of 14.3 to 28.6 W per emitter. A precise assessment of the reliability and replacement lifetime of laser bars and stacks at the anticipated operating conditions is a crucial element towards realizing economic IFE systems. 

Aging data on single laser emitters, i.e. laser chips with a single laser stripe, operating at continuous wave (CW) can be used to assess the endurance of the material against the applied power densities during operation. Reliability on single emitters for different wavelengths from 790 nm to 980 nm was reported in 2013 by Bao et al. [60]. Their lifetests were analyzed with Weibull (wear out) statistics and acceleration parameters from literature resulting in an estimated reliability of 95% in 11 years for 6 W at 880 nm and no wear out at 915-980 nm with only one sudden failure, from which a reliability of 95% in 12 years at 12 W was derived. Those lasers had a stripe width of _W_ = 95 µm. Laser chips at 880 nm with wider stripe ( _W_ = 200 µm) are 95% reliable for over 9 years at higher powers of 10 W. Laser modules with 72 single 

emitters coupled into the 400 µm core of a fibre reach powers up to 540 W with no failure over more than 7000 h in continuous wave (CW) mode. This work has demonstrated that laser chips can sustain the required power density in CW mode for the equivalent emission time under pulsed operation. 

From the same group and one year earlier, the reliability of 880 nm laser bars, assembled in 3 mm mini bars was tested by accelerated aging tests for 100 Mshots at about 160 W peak power corresponding to 530 W from 1 cm [59]. Only 1 emitter out of more than 800 failed. Around the same time, Kissel et al. [61] reported on life test results of stacks of 8 laser bars at 940 nm with 2.4 kW peak power for 40 Mshots and one laser bar at 400 W for 30 Mshots (each duty cycle _dc_ ~ 1%) without degradation. Wölz et al. [13] presented in 2016 their work on life testing of 880 nm bars for 1.2 Gshots at 500 W peak power, among others. In 2018, Thiagarajan et al. [62] reported on lifetest of a 40 bar 890 nm stack emitting up to 23 kW at 600 A. Lifetests were performed for over 200 Mshots at accelerated conditions from which a median life of 2 Gshots was derived. A 9x5 matrix of stacks with 1800 bars can deliver 1 MW of peak power. Bai et al. [59] reported on aging tests of 30 pieces of 880 nm laser diode mini bars with 20 emitters each, having COMD-suppression by laser facet passivation. Those indicate no failure when tested over 100 Mshots at 150 A (>160 W) well below the COD-level. This corresponds to a power of 8 W per emitter and 540 W per 1 cm bar. 

Overall, while the studies summarized above successfully demonstrated the high reliability of GaAs-based diode lasers, none of them were conducted with reliability specifications as high as those required for IFE systems (at least 3 Gshots at up to 1 kW per bar). To our knowledge, such reliability levels have not yet been demonstrated in any configuration; be it stacks or individual bars or even single emitters with comparable power density, and certainly not with the low percent per Gshot failure rates that would be acceptable for a full-scale IFE facility. 

In order to achieve higher reliability levels from diode lasers at high power levels, it is important to have a good understanding of their failure modes. Semiconductor laser material is prone to degradation that is accelerated by high densities of optical power and current and elevated temperature in the active zone. Sources of defects originate from thermal activation of point defects, such as anti-side states forming EL2 deep level traps [63], arrays of dislocation loops and networks formed at pre-existing threading dislocations or defect clusters. Those extended defects can be detected with electroluminescence or cathodoluminescence as dark spot defects (DSD) or dark line defects (DLD). Non-radiative recombination and optical absorption at dislocations and traps cause the defects to grow in size and density [64,65]. Degradation and failure events are known to be randomly distributed among nominally identical laser chips. The growth and multiplication of defects depends on random distribution of pre-existing defects, random accumulation of non-radiative recombination and absorption events, potentially leading to hot spot formation by filamentation in a chaotic regime, eventually causing catastrophic optical mirror damage (COMD) or bulk damage (COBD) [66]. Degradation rates and failure events are statistically distributed. In general, higher reliability and lower failure rates can be achieved by reducing the defect density, which in turn can be achieved by enhancing and optimizing device technology, similar to the earlier discussion of facet passivation in section 4. 

For a given device technology and configuration, aging tests are usually performed at accelerated conditions with higher stress than under operational conditions in order to obtain information on reliability after limited test time of typically 2000 h. The reliability _R_ acc(t) = _R_ ( _t_ acc) can be described by the phenomenological model of scale accelerated failure time _t_ acc = _t_ ×  acc as follows: 

![](images/tmptsec273q.pdf-0013-05.png)

where _I_ is the current (density), _P_ opt the optical power (density). The temperature _T_ is the internal steady state temperature in the active zone at the peak: _T_ = _T_ sub + _R_ th _P_ w, for waste heat _P_ w = _IU_ - _P_ opt, where _U_ is the bias voltage at a given _I_ . A usual way to accelerate the number of shots is to increase the frequency. This can be done in a sufficiently small range of the duty cycle, where thermal roll-over is avoided, and further by controlling the base temperature. 

Since the degradation depends on the specific material, intentional and unintentional impurities, such as dopants, lattice point defects, residual foreign atoms, threading dislocations, growth defects, built-in strain, etc., it is useful to determine the acceleration parameters ( _m_ , _n_ , _E_ a) exemplary for each material, that was identically processed [58]. The methods involve lotspecific testing by varying temperature, power and current per lot. Gradual degradation and failure times can be analyzed by probability plotting and fitting or numerical likelihood methods [67]. 

As discussed above, for assessing the reliability of laser bars and stacks for long life (~10 Gshots) and high powers in the range of 500 W to 1 kW, there are still not sufficient data available from publications or a detailed qualification program. Furthermore, well-resolved experimentally determined acceleration factors are not available, with literature values normally used, which may not apply to the diode technology and stack fabrication used. Since laser chips with single emitters operating in CW mode appear to be more reliable compared to the accumulated switch-on times at QCW in bars or stacks [60], there are additional effects that may originate from additional stress, such as thermo-mechanical strain, mounting stress, defect growth towards neighboring emitters, increased average temperature by self-heating and timeresolved temperature differentials within the diode laser and between the diode and its surrounding assembly. Indeed, strong relation between packaging approach and reliability has been reported [68]. A phenomenological reliability model can involve the dependence on the number S of shots in addition to current, power and temperature: 

![](images/tmptsec273q.pdf-0014-03.png)

where F is an unknown function, for example ℱ(𝑆) = 𝑆[𝑘] . Such dependence can be assessed, for example by varying the pulse frequency up to CW while keeping the internal temperature constant via external temperature control. We note also that failures may be accelerated as a function of temperature differences between on-state and off-state operation, as well as by differential temperatures within the device and its housing [57]. We note also that efforts to monitor and successfully qualify the selected facet passivation approach are likely also needed, as significant drop in failure power with operating time can be seen, and must be accounted for in reliability predictions [69]. 

Future work should address the issue of proving the required reliability of _R_ > 95% for wear-out beyond 3 Gshots / 10 Hz (9.5 years) at the component level, as well as on establishing agreed and properly documented and standardized qualification procedures for both entry-level and full-system, similar to standardization efforts in the early phases of the telecommunications industry. The documented reliability studies must be sufficient to motivate use in all stages of IFE development, from the fabrication of prototype beamline assemblies through to the realization of full power generation systems. 

## **7. Summary, Conclusions, Prospects** 

An overview of current studies into diode laser pumps for application in IFE systems was presented, summarizing current understanding on the requirements, and a suitable technological path to achieving them. Analysis of the likely benefits of production scaling as volume rises confirmed the plausibility of the needed more than tenfold reduction in purchase price. The benefits of emerging device technologies for substantial power scaling and yield 

increases were also summarized, with approaches based on multi-junction epitaxial layer designs that appear especially promising, particularly when supported by sufficiently robust facet passivation and advanced process control methods. Although efficiency-scaling is challenging, achieving the required 70% peak efficiency at the kilowatt-per bar power level was shown to be plausible. Finally, an overview of the status of reliability studies was presented, with significant gaps noted between demonstrated lifetime and understanding of failure modes (acceleration factors) and the requirements of IFE industry, with no suitable qualification standards currently available. In short, diode lasers have a clear path to meet in full the need of IFE, if the promise of current analysis can be fulfilled. 

## **Acknowledgements** 

This work was performed in part under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under contract DE-AC52-07NA27344 and was supported by the LLNL LDRD program under Project No. 24-ERD-034 and by the DOE FES IFE-STAR Program under Project Number SCW1835-1 STARFIRE. 

The work was further supported in part within the BMFTR Project DIOHELIOS (FKZ: 13F1015F) and the ProFIT Innovation project HOTSTACK (10198838), that itself is cofinanced by the European Regional Development Fund (ERDF) 

Data underlying the results presented in this paper are not publicly available at this time but may be obtained from the authors upon reasonable request. 

## **Disclosures** 

The authors declare no conflicts of interest. 

## **References** 

1. P. Crump and W. E. Fenwick, “Performance scaling of high-power diode laser pumps for fusion applications”, Proc. SPIE **13343** , 133430C (2025). 

2. H. Abu-Shawareb _et al_ . (The Indirect Drive ICF Collaboration), “Lawson Criterion for Ignition Exceeded in an Inertial Fusion Experiment,” Phys. Rev. Lett. **129** , 075001 (2022). 

3. H. Abu-Shawareb _et al_ . (The Indirect Drive ICF Collaboration), “Achievement of Target Gain Larger than Unity in an Inertial Fusion Experiment,” Phys. Rev. Lett. **132** , 065102 (2024). 

4. T. Ma _et al_ ., “Basic Research Needs Workshop on Inertial Fusion Energy,” U.S. Department of Energy report (2022), https://science.osti.gov/-/media/fes/pdf/workshop-reports/2023/IFE-Basic-Research-Needs-FinalReport.pdf [last accessed 17 July 2025]. 

5. C. Häfner _et al._ , “Status and Perspectives of High-Power Pump Diodes for Inertial Fusion Energy Lasers,” IFE Science & Technology Community Strategic Planning Workshop (2022), https://lasers.llnl.gov/sites/lasers/files/2023-11/haefner-ILT-IFE-workshop-2022-1.pdf [last accessed 17 July 2025]. 

6. R. Deri, J. Geske, M. Kanskar, _et al._ , “Semiconductor Laser Diode Pumps for Inertial Fusion Energy Lasers,” Lawrence Livermore National Labs Technical Report, LLNL-TR-465931 (2011). 

7. A. Bayramian, S. Aceves, T. Anklam, _et al._ , “Compact, Efficient Laser Systems Required for Laser Inertial Fusion Energy,” Fusion Science and Technology **60** (1), 28–48 (2011). 

8. A. C. Erlandson, S. M. Aceves, A. J. Bayramian, _et al._ , “Comparison of Nd:phosphate glass, Yb:YAG and Yb:S-FAP laser beamlines for laser inertial fusion energy (LIFE) [Invited],” Opt. Mater. Express **1** , 1341–1352 (2011). 

9. D. Batani, A. Colaïtis, F. Consoli, _et al._ , “Future for inertial-fusion energy in Europe: a roadmap,” High Power Laser Science and Engineering **11** , e83 (2023). 

10. E. Sistrunk, T. Spinka, A. Bayramian, _et al._ , “All Diode-Pumped, High-repetition-rate Advanced Petawatt Laser System (HAPLS),” Conf. on Lasers and Electro-Optics (CLEO), San Jose, CA, USA, STh1L.2 (2017). 

11. M. Divoký, J. Pilař, M. Hanuš, _et al._ , “150 J DPSSL operating at 1.5 kW level,” Opt. Lett. **46** , 5771–5773 (2021). 

12. R. J. Deri, A. J. Bayramian, A. C. Erlandson, _et al._ , “High-Power Diode Laser Arrays for Large Scientific Lasers and Inertial Fusion,” IEEE Photonics Conf., San Diego, CA, USA, TuD2.3 (2014). 

13. M. Wölz, A. Pietrzak, A. Kindsvater, _et al._ , “Laser diode stacks: pulsed light power for nuclear fusion,” High Power Laser Science and Engineering **4** , e14 (2016). 

14. M. S. Zediker and E. P. Zucker, “High-power diode laser technology XX: a retrospective on 20 years of progress”, Proc. SPIE **11983** , 1198302 (2022). 

15. A. Maaßdorf, J. K. Zettler, M. Brendel, _et al._ , “Efficient Front-End Manufacturing of High-Quality VCSEL – Enabled by In-Situ and Ex-Situ Optical Metrology During Epi Growth and Processing,” Int. Conf. Compound Semicond. Manufacturing Technology (CS ManTech), New Orleans, Louisiana, USA, 10A.3 (2025). 

16. C. Zink, M. Ekterai, D. Martin, _et al._ , “Deep-learning-based visual inspection of facets and p-sides for efficient quality control of diode lasers”, Proc. SPIE **12403** , 124030E (2023). 

17. R. Todt, S. Deubert, and D. Jaeggi, “High-Volume Manufacturing of State-of-the-Art High-Power Laser Diodes on 6-inch GaAs,” Proc. SPIE **11983** , 1198303 (2022). 

18. D. D. Evans and Z. Bok, “Micron Level Placement Accuracy Case Studies for Optoelectronic Products,” 59[th] Electron. Comp. Technol. Conf., 1937–1941 (2009) & related Palomar Technologies eBook: https://www.palomartechnologies.com/guide-to-micron-level-placement-for-wafer-scale-packaging-of-p-sidedown-lasers-in-optoelectronic-components [last accessed 17 July 2025] 

19. J. Wallace, “Assembly of high-power laser diodes is automated for the first time,” Laser Focus World **45** (2009). 

20. T. Barnowski, T. Vethake, K. Atwater, _et al._ , “Advances in manufacturing technology for low cost QCW diode laser stacks suitable for high energy pumping applications”, Proc. SPIE **12867** , 1286713 (2024). 

21. P. Crump and G. Tränkle, “A brief history of kilowatt-class diode-laser bars,” Proc. SPIE **11301** , 113011D (2020). 

22. M. J. Miah, A. Boni, D. Martin, _et al._ , “Kilowatt-class, 1-cm diode laser bars at 910-940 nm with improved power, conversion efficiency and beam quality,” Proc. SPIE **11983** , 1198304 (2022). 

23. R. J. Deri, W. E. Fenwick, J. Li, _et al._ , “Slope Efficiency and Voltage Reduction at High Current Densities in AlInGaAs Diode Lasers”, IEEE J. Sel. Top. Quant. Electron. **31** (2), 1502108 (2025). 

24. M. Kanskar, Z. Chen, W. Dong, _et al._ , “High power and high efficiency 1.8-kW pulsed diode laser bar”, J. Photon. Energy **7** (1), 016003 (2017). 

25. Y. Zhao, Z. Wang, A. Demir, _et al._ , “High Efficiency 1.9 kW Single Diode Laser Bar Epitaxially Stacked with a Tunnel Junction,” IEEE Photonics Journal **13** (3), 1500708 (2021). 

26. J. Wang, S. Tan, Y. Shao, _et al._ , “Double-Junction Cascaded GaAs-Based Broad-Area Diode Lasers with 132W Continuous Wave Output Power,” Photonics **11** , 258 (2024). 

27. G. Liu, Z. Xu, J. Li, _et al._ , “Multi kW high efficiency high filling factor 870nm and 940nm QCW semiconductor diode laser bars for inertial fusion energy applications”, Proc. SPIE **13345** , 133450V (2025). 

28. H. Wenzel, A. Maaßdorf, C. Zink, _et al._ , “Novel 900 nm diode lasers with epitaxially stacked multiple active regions and tunnel junctions”, Electron. Lett. **57** (11), 445–447 (2021). 

29. A. Knigge, N. Ammouri, H. Christopher, _et al._ , “2 kW Pulse Power from Internal Wavelength Stabilized Diode Laser Bar for LiDAR Applications”, 28[th] Int. Semicond. Laser Conf. (ISLC), Matsue, Japan, TuB-02 (2022). 

30. N. Ammouri, H. Christopher, A. Maaßdorf, _et al._ , “420 W pulse power from a 905 nm distributed bragg reflector laser with multiple active regions and tunnel junctions”, Physica Scripta **100** , 075514 (2025). 

31. M. Leers and K. Boucke, “Cooling Approaches for High Power Diode Laser Bars,” 58[th] Electronic Components and Technology Conference, Lake Buena Vista, FL, USA, 1011–1016 (2008). 

32. S. Heinemann, S. D. McDougall, G. Ryu, _et al._ , “Advanced chip designs and novel cooling techniques for brightness scaling of industrial, high power diode laser bars,” Proc. SPIE **10514** , 105140Y (2018). 

33. C. T. Goddard, “Debunking the Learning Curve,” IEEE Transactions on Components, Hybrids, and Manufacturing Technology 5(4), 328–335 (1982). 

34. R. Haitz and J. Y. Tsao, “Solid-state lighting: ‘The case’ 10 years after and future prospects,” Phys. Status Solidi A **208** (1), 17–29 (2011). 

35. McKinsey & Company, “Lighting the Way: Perspectives on the Global Lighting Market (Second edition)” market report (2012). 

36. M. Gasser and E. E. Latta, “Method for mirror passivation of semiconductor laser diodes,” United States Patent US5144634A (1992). 

37. A. Jakubowicz, “Quantum well passivation structure for laser facets,” United States Patent US10418781B1 (2019). 

38. A. Jakubowicz and M. Sueess, “Ex-situ conditioning of laser facets and passivated devices formed using the same,” United States Patent US11411373B2 (2022). 

39. N. Chand, W. S. Hobson, J. F. de Jong, _et al._ , “ZnSe for mirror passivation of high power GaAs based lasers,” Electronics Letters **32** (17), 1595–1596 (1996). 

40. J. E. Boschker, U. Spengler, P. Ressel, _et al._ , “Stability of ZnSe-Passivated Laser Facets Cleaved in Air and in Ultra-High Vacuum,” IEEE Photonics Journal **14** (3), 1–6 (2022). 

41. P. Ressel, G. Erbert, U. Zeimer, _et al._ , “Novel passivation process for the mirror facets of Al-free active-region high-power semiconductor diode lasers,” IEEE Photonics Technology Letters **17** (5), 962–964 (2005). 

42. P. Crump, G. Blume, K. Paschke, _et al._ , “20W continuous wave reliable operation of 980nm broad-area single emitter diode lasers with an aperture of 96µm,” Proc. SPIE **7198** , 719814 (2009). 

43. J. Lång, J. Mäkelä, J.-P. Lehtiö, _et al._ , “Advanced facet passivation for high-power edge-emitting laser diodes,” Proc. SPIE **12867** , 128670F (2024). 

44. J. H. Marsh, “Quantum well intermixing,” Semicond. Sci. Technol. **8** (6), 1136–1155 (1993). 

45. M. L. Osowski, W. Hu, R. M. Lammert, _et al._ , “Advances in high-brightness semiconductor lasers,” Proc. SPIE **6876** , 68761E (2008). 

46. S. Arslan, S. Gündoğdu, A. Demir, and A. Aydınlı, “Facet Cooling in High-Power InGaAs/AlGaAs Lasers,” IEEE Photonics Technol. Lett. **31** (1), 94–97 (2019). 

47. H. Naito, T. Nagakura, K. Torii, _et al._ , “Long-Term Reliability of 915-nm Broad-Area Laser Diodes Under 20W CW Operation,” IEEE Photonics Technol. Lett. **27** (15), 1660–1662 (2015). 

48. P. Crump, A. Boni, M. Elattar, _et al._ , “Power and Efficiency Scaling of GaAs-Based Edge-Emitting HighPower Diode Lasers,” IEEE J. Sel. Top. Quantum Electron. **31** (2), 1502512 (2025). 

49. D. Schröder, J. Meusel, P. Hennig, _et al._ , “Increased power of broad-area lasers (808nm/980nm) and applicability to 10-mm bars with up to 1000Watt QCW”, Proc. SPIE **6456** , 64560N (2007). 

50. P. Crump, C. Frevert, H. Wenzel, _et al._ , “Cryolaser: innovative cryogenic diode laser bars optimized for emerging ultra-high power laser applications”, Conf. on Lasers and Electro-Optics (CLEO), San Jose, CA, USA (2013). 

51. M. J. Miah, A. Boni, S. Arslan, _et al._ , “Optimizing Vertical and Lateral Waveguides of kW-Class Laser Bars for Higher Peak Power, Efficiency and Lateral Beam Quality”, IEEE Photonics J. **14** (3), 1525505 (2022). 

52. M. M. Karow, D. Martin, P. Della Casa, _et al._ , “Design Progress for Higher Efficiency and Brightness in 1 kW Diode-Laser Bars”, Proc. SPIE **11983** , 1198302 (2022). 

53. C. Frevert, F. Bugge, S. Knigge, _et al._ , “940nm QCW diode laser bars with 70% efficiency at 1 kW output power at 203K: analysis of remaining limits and path to higher efficiency and power at 200K and 300K,” Proc. SPIE **9733** , 97330L (2016). 

54. P. Crump, M. Elattar, M. J. Miah, _et al._ , “Progress in efforts to increase power in GaAs-based high-power diode lasers”, 28[th] Int. Semicond. Laser Conf. (ISLC), Matsue, Japan, TuA-01 (2022). 

55. M. Elattar, H. Wenzel, J. Fricke, _et al._ , “Monolithic DBR broad-area diode lasers with high conversion efficiency in the 87x–88x nm wavelength range”, Proc. SPIE **13345** , 1334507 (2025). 

56. ams OSRAM, “SPL DS90A_3” chip datasheet (2021), https://ams-osram.com/products/lasers/ir-laserseel/osram-chip-spl-ds90a-3 [last accessed 17 July 2025]. 

57. M. Elattar, M. Hübner, M. Wilkens, _et al._ , “Finite-Element Thermal Simulation of High-Power Diode Laser Stacks for High-Duty-Cycle Pump Applications,” IEEE J. Sel. Top. Quantum Electron. **31** (2), 1500407 (2025). 

58. K. Häusler, J. Fricke, R. Staske, _et al._ , “Highly Reliable Low Noise Pump Sources for Solid State Lasers in Laser Communication Terminals”, Proc. SPIE **10910** , 109100N (2019). 

59. J. G. Bai, Z. Chen, P. Leisher, _et al._ , “High-efficiency kW-class QCW 88x-nm diode semiconductor laser bars with passive cooling,” Proc. SPIE **8241** , 82410W (2012). 

60. L. Bao, J. Bai, K. Price, _et al._ , “Reliability of high power/brightness diode lasers emitting from 790 to 980 nm,” Proc. SPIE **8605** , 86050N (2013). 

61. H. Kissel, W. Faßbender, J. Lotz, _et al._ , “Reliable QCW diode laser arrays for operation with high duty cycles,” Proc. SPIE **8605** , 86050V (2013). 

62. P. Thiagarajan, J. Goings, B. Caliva, _et al._ , “Megawatt-class peak power laser diode pump sources,” Proc. SPIE **10637** , 106370G (2018). 

63. Y. Sin, S. Stuart, M. Brodie, and Z. Lingley, “Physics of failure based reliability model of high-power InGaAsAlGaAs strained QW lasers prone to COBD failure,” Proc. SPIE **11262** , 1126207 (2020). 

64. L. Wang, E. McVay, S. H. Baxamusa, _et al._ , “Imaging of dark line defect growth in high-power diode laser cavities using broadband near infrared light emission from the laser cavity,” Appl. Phys. Lett. **125** , 251101 (2024). 

65. S. Dadgostar, J. L. Pura, I. Mediavilla, _et al._ , “Catastrophic optical damage in 808 nm broad area laser diodes: a study of the dark line defect propagation,” Opt. Express **30** (23), 42624–42638 (2022). 

66. Y. Sin, C. Lewis, J. Theiss, _et al._ , “Micro- and macroscopic analysis of degradation in high-power broad-area QW and QD lasers,” Proc. SPIE **13345** , 1334517 (2025). 

67. W. Q. Meeker and L. A. Escobar, _Statistical Methods for Reliability Data_ , (John Wiley & Sons, 1998). 

68. Y. Berk, Y. Karni, G. Klumel, _et al._ , “Space-grade reliability of 808nm QCW laser diode arrays (LDAs) delivering over 20 billion shots,” Proc. SPIE **7198** , 71980C (2009). 

69. K. Häusler, C. Stölmacker, A. Maaßdorf, _et al._ , “Investigations on Operational Reliability of 808 nm QCW Laser Diode Half-Bars for Space-Borne Applications,” 27[th] Int. Semicond. Laser Conf. (ISLC), Potsdam, Germany, TuP2.4 (2021). 

