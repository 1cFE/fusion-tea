---
source: "https://arxiv.org/pdf/1512.01930"
source_type: "url"
extracted_at: "2026-09-29T23:04:52.199362+00:00"
content_hash_sha256: "7ad34fc68efe87d0199399e15cdd063a8089db12940f663559f045df28f84895"
backend: "pdf_pipeline"
---

## **Field and temperature scaling of the critical current density in commercial REBCO coated conductors** 

Carmine Senatore, Christian Barth, Marco Bonura, Miloslav Kulich, Giorgio Mondonico 

Département de Physique de la Matière Quantique (DQMP) and Département de Physique Appliquée (GAP), University of Geneva, Geneva CH-1211, Switzerland 

## **Abstract** 

Scaling relations describing the electromagnetic behaviour of coated conductors (CCs) greatly simplify the design of REBCO-based devices. The performance of REBCO CCs is strongly influenced by fabrication route, conductor architecture and materials, and these parameters vary from one manufacturer to the others. In the present work we have examined the critical surface for the current density, Jc(T,B,  ), of coated conductors from six different manufacturers: American Superconductor Co. (US), Bruker HTS GmbH (Germany), Fujikura Ltd. (Japan), SuNAM Co. Ltd. (Korea), SuperOx ZAO (Russia) and SuperPower Inc. (US). Electrical transport and magnetic measurements were performed at temperatures between 4.2 K and 77 K and in magnetic field up to 19 T. Experiments were conducted at three different orientations of the field with respect to the crystallographic c-axis of the REBCO layer, θ = 0°, 45° and 90°, in order to probe the angular anisotropy of Jc. In spite of the large variability of CCs’ performance, we show here that field and temperature dependences of Jc at a given angle can be reproduced over wide ranges using a scaling relation based only on three parameters. Furthermore, we present and validate a new approach combining magnetic and transport measurements for the determination of the scaling parameters with minimal experimental effort. 

## **1. Introduction** 

Second generation REBa2Cu3O7-x (REBCO, RE = rare earth) coated conductors are complex multilayer materials. Processing technology and tape architecture vary from one industrial manufacturer to the other, resulting in largely different electromagnetic, electromechanical and thermal properties [1-3]. 

Coated conductor (CC) development has been driven so far by the perspectives of applications in the electrical utility sector. The efforts of manufacturers have focused on the optimization of the critical currents in low fields (1-3 T) and at temperatures ranging between 50 and 77 K. Only in the last few years the interest for high field magnets based on REBCO coils started to emerge, even if research in HTS coils made with BSCCO tapes goes back to mid-90s [4, 5]. Ongoing projects include solenoidal magnets in the 30 T range [1, 6, 7], 20 T dipole 

magnets for particle accelerators [8], the DEMO design studies for fusion power plants [9]. However, there have been limited reports on the electrical transport properties of REBCO tapes at 4.2 K in magnetic fields above 15 T [10-12]. 

The intrinsic anisotropy of REBCO superconducting properties determines the angular anisotropy of the critical current, Ic. Beyond the challenge of winding a coil using a tape with large aspect ratio, the anisotropy of the critical current introduces an additional layer of complexity to the magnet design. Ic at T = 4.2 K and B > 10 T is maximum when magnetic field is parallel to the tape surface (i.e. in the crystallographic ab-plane of the REBCO layer) and minimum when the field is normal (i.e. parallel to the c-axis). Therefore, the most critical part in a tape-wound solenoid is at the coil ends, where the radial component of the magnetic field – perpendicular to the tape surface – is high. However, the Ic(θ) curve, θ being the angle between the field and the crystallographic c-axis of the REBCO layer, may show multiple peaks as an effect of nanoparticle doping, with a second maximum when B is parallel to the c-axis. A detailed knowledge of the anisotropy of Ic at the operating temperature and field is thus crucial for magnet design. It is worth mentioning that Long et al. [13] and, more recently, Hilton et al. [14] proposed practical expression to fit the experimental Ic(  ) dependence, even in the presence of multiple peaks. 

The protection of REBCO-based coils represents another critical issue. The operating temperature margin is clearly much larger compared to LTS-based magnets. This results in a much slower normal zone propagation velocity that makes difficult the detection of quenches [15, 16]. A magnet quench can be triggered when the winding temperature locally exceeds the current sharing temperature, Tcs, i.e. the temperature at which the current in the tape is equal to the critical current. The characterization of the temperature dependence of Ic between 4.2 K and Tcs is thus necessary to consolidate the electromagnetic models simulating the coil behaviour in case of quenches. 

To qualify REBCO coated conductors for operation in very high field magnets, magnet design must be carefully adapted to the specific Ic(T,B,  ) characteristics of the tapes provided by the various manufacturers. On the other hand, the large performance variability would make necessary to conduct extensive critical current measurements in magnetic fields up to 30 T at various orientations and with temperatures ranging between 4.2 K and Tcs for each conductor batch, and this would be an extremely time-consuming process. Scaling relations describing the electromagnetic behaviour of coated conductors are therefore essential for the proper design of the superconducting device. Hence, it is crucial to identify a minimum number of experimental results necessary for a comprehensive characterization of the electrical transport properties of REBCO tapes as well as determine the extrapolations’ error margins. This is the motivation of the present paper. In particular, we propose a simple expression allowing the reconstruction of the Ic(T,B) surface for a given field orientation using only three parameters. The paper is structured as follows: 

- We have examined the electrical properties of coated conductors from six industrial manufacturers. Details about the tapes are given in Sec. 2. 

- The temperature and magnetic field dependences of the critical current density were determined by transport and inductive measurements, as described in Sec. 3. 

- Results are reported in Sec. 4 and discussed in Sec. 5. 

- Sec. 6 is devoted to the conclusions. 

## **2. Characteristics of the investigated samples** 

In the present work we have investigated the electrical and magnetic properties of coated conductors from six different industrial manufacturers: American Superconductor Co. (US), Bruker HTS GmbH (Germany), Fujikura Ltd. (Japan), SuNAM Co. Ltd. (Korea), SuperOx ZAO (Russia) and SuperPower Inc. (US). 

Commercial coated conductors rely on two common features: a biaxially textured template, consisting of a flexible metallic tape coated with a multifunctional oxide barrier, and an epitaxial REBCO layer. The textured template is created by either deforming the metal substrate with the Rolling Assisted Biaxially Textured Substrate technology (RABiTS) [17] or by texturing the buffer layers deposited on the metal substrate by the so-called Ion Beam Assisted Deposition (IBAD) [18] and by its variant, the Alternating Beam Assisted Deposition (ABAD) [19]. The epitaxial REBCO layer is grown either by chemical routes, such as metal organic deposition (MOD) [20] and metal organic chemical vapor deposition (MOCVD) [21], or by physical routes, such as pulsed laser deposition (PLD) [22-24] and reactive co-evaporation (RCE) [25, 26]. The deposition of the precursors and conversion of the precursors into REBCO can occur in a single step ( _in situ_ process), as for MOCVD and PLD, and or in two steps ( _ex situ_ process), as for MOD and RCE. Typically, a few-µm Ag layer for protection against the moisture from the environment and a Cu layer for thermal and electrical stabilization are added to complete the conductor. 

The characteristics of the investigated coated conductors are summarized in table I. 

**Table I – Fabrication process and technical data of the investigated REBCO tapes** 

![](images/tmpwtbipewf.pdf-0004-00.png)

**----- Start of picture text -----**<br>
B = 0.5 T<br> = 0° B = 1 T<br>100 B = 2 T<br>B = 3 T<br>B = 4 T<br>B = 5 T<br>B = 6 T<br>B = 7 T<br>10 B = 8 T<br>B = 15 T<br>B = 19 T<br>(a)<br>1<br> = 45°<br>100<br>10<br>(b)<br>1<br> = 90°<br>100<br>10<br>(c) Bruker HTS<br>1<br>0 10 20 30 40 50 60 70 80<br>Temperature [K]<br>2]<br>2]<br>2]<br> [kA/mmJc<br> [kA/mmJc<br> [kA/mmJc<br>**----- End of picture text -----**<br>

**Figure 1** Temperature dependence of the critical current density Jc for the tape from Bruker HTS, measured for three orientations of the magnetic field, θ = 0° (a), 45°(b) and 90° (c). Orientations are referred to the angle between the magnetic field and the crystallographic c-axis of the REBCO layer. Jc data are extracted from inductive (B  8 T) and transport (B > 8 T) measurements. 

## **3. Experimental details** 

Transport critical current and magnetization were measured over a broad range of temperatures and magnetic fields for three orientations of the tapes with respect to the field, θ = 0° and θ = 90°, defined, respectively, when field is normal and parallel to tape surface, and θ = 45°. 

The characterization protocol of Ic includes four temperatures, T = 4.2, 20, 30 and 40 K, in magnetic fields up to 19 T. In all following experiments, the critical current is defined as the current at the critical electric field of 0.1 μV/cm. Our setup for critical current measurements is limited to current values of 1000 A at 4.2 K and to ≈ 250 A above 4.2 K. Due to these limitations, we performed measurements on full width tapes only in the orientations with θ = 0 and 45°, while Ic in parallel field (θ = 90°) was measured on samples with reduced width. Two different techniques were adopted for the reduction of the REBCO layer width: chemical etching and electrical discharge machining (EDM). In the etching process, a lift-off photolithographic technique was used to obtain a 1 mm bridge at the center of the tape. This approach was preferred for coated conductors with electrodeposited stabilizer. EDM cutting was used for the tapes with laminated stabilizer: the sample width was reduced with a single cut from one 

![](images/tmpwtbipewf.pdf-0005-00.png)

**----- Start of picture text -----**<br>
100<br>Bruker HTS<br>10<br> T = 30 K<br> = 0°<br> T = 40 K<br>1<br>0 2 4 6 8 10 12 14 16 18 20<br>Magnetic field [T]<br> [kA/mmJc<br>2]<br>**----- End of picture text -----**<br>

**Figure 2** Magnetic field dependence of the transport (full symbols) and inductive (solid lines) Jc(θ = 0°) at T = 30 K and 40 K for the Bruker HTS tape. The Jc value at T = 40 K and B = 7 T from the transport Ic was used to convert magnetization to critical current density. 

side, varying the bridge width between 1 and 2 mm. In the case of reduced width samples, transport measurements were always repeated on different bridges in order to exclude etching or cutting defects. 

Magnetization measurements in the field orientations with θ = 0° and 45° were performed using a vibrating sample magnetometer (VSM). Magnetization vs. magnetic field, M(B), loops were recorded at fixed temperatures between 4.2 and 77 K in fields up to 8.8 T. The field was swept at a rate of 1 T/min. At θ = 90°, the signal from the superconductor is overwhelmed by the magnetic moment of the substrate. In fact, the area where the superconducting screening currents flow and thus the corresponding magnetic moment are small, being proportional to the REBCO film thickness. To overcome this problem, we prepared special samples by separating the superconductor from the substrate. It is well known that coated conductors are prone to delamination at the interface between REBCO layer and buffers. We exploited this structural weakness to peel off the stack made of Cu, Ag and REBCO layers from the substrate. A high sensitivity Superconducting Quantum Interference Device (SQUID) magnetometer was used to measure magnetization of the Cu/Ag/REBCO stack in parallel fields up to 7 T. As for the other orientations, magnetic field was swept at a rate of 1 T/min and temperature was varied between 4.2 and 77 K. 

## **4. Experimental results** 

## _**4.1. Temperature dependence of the critical current density**_ 

To design high-field magnets based on REBCO tapes and which operate at 4.2 K it is necessary to parameterize the in-field critical current performance over a large range of temperatures, the temperature margin being of the order of 30 K. Figure 1 presents, in a lin-log chart, the temperature dependence of the critical current density in the REBCO layer, Jc, between 4.2 and 77 K for the tape from Bruker HTS. Magnetic field ranges between 0.5 and 19 T for the three orientations,  θ = 0° (Fig. 1a), 45° (Fig. 1b) and 90° (Fig. 1c). Critical current density values extracted from the magnetization data were used to expand the explored window of temperatures and magnetic fields. Figure 2 compares the Jc(B) curves at 30 K and 40 K as determined from transport and magnetic measurements. It is well known that the irreversible magnetization (  M)  is proportional to Jc via a geometrical coefficient related to the length scale of the current flow. The value of Jc(40 K, 7 T) extracted from transport Ic 

![](images/tmpwtbipewf.pdf-0006-00.png)

**----- Start of picture text -----**<br>
35 AMSC   =  0° Bruker HTS   =  0°   =  0° 35<br>  =  45°   =  45°   =  45°<br>  =  90°   =  90°   =  90°<br>30 30<br>25 25<br>20 20<br>15 (a) (b) Fujikura (c) 15<br>35 SuNAM   =  0° SuperOx   =  0° SuperPower   =  0° 35<br>  =  45°   =  45°   =  45°<br>  =  90°   =  90°   =  90°<br>30 30<br>25 25<br>20 20<br>15 (d) ( e) (f) 15<br>0 2 4 6 8 10 12 14 16 18 20 0 2 4 6 8 10 12 14 16 18 20 0 2 4 6 8 10 12 14 16 18 20<br>Magnetic field [T]<br>T* [K]<br>**----- End of picture text -----**<br>

**Figure 3** Field dependence of the temperature scaling parameter, T*, as determined for the tapes from six industrial manufacturers: open symbols for θ = 0°, half-filled symbols for θ = 45° and solid symbols for θ = 90°. Dashed lines are given as guides to the eye. 

was used to set the coefficient of proportionality between  M and Jc and thus to convert magnetization to critical current density. The two datasets, transport and inductive Jc, exhibit identical magnetic field dependence, as shown from the curves at T = 30 K and 40 K in Fig. 2. 

From the curves shown in Fig. 1, it follows that the temperature dependence of Jc can be described over a broad range of temperatures and magnetic fields by the equation 

![](images/tmpwtbipewf.pdf-0006-04.png)

The exponential T-dependence holds up to ≈ 50 K for θ = 0° and 45°, and between 10 K and ≈ 40 K for θ = 90°, with a typical error below 2%. At θ = 90°, the higher is the field the lower is the deviation from the exponential behaviour at temperatures below 10 K. We encountered the same scaling behaviour for all the investigated tapes regardless of the manufacturer. 

The temperature dependence of Jc is determined by the thermal activation processes associated to the pinning centres. In particular, the exponential decay of Jc is connected to the presence of defects generating weak isotropic pinning and T* is the characteristic pinning energy at these defects [27, 28]. A high value of T* implies a slow decrease of Jc with T. The values of T* vary significantly from one manufacturer to the others. The dependence of T* on B may also vary from tape to tape of the same manufacturer, as the vortex pinning landscape depends on the fabrication route and on the possible addition of artificial precipitates. 

T* values have been obtained by fitting the experimental results by Eq. 1 in the temperature range where the linearity in the lin-log plot is observed. Results are summarized in Figure 3 for the examined CCs. At the lowest field, B = 0.5 T, T* values span between 20 K and 30 K. At higher fields, the general trend is T*(0°) > T*(45°) > T*(90°). The only exception comes from the Fujikura CC, which exhibits T*(45°) > T*(0°) between 4 and 8 T. 

![](images/tmpwtbipewf.pdf-0007-00.png)

**----- Start of picture text -----**<br>
T = 5 K<br>100  = 0° T = 10 K<br>T = 15 K<br>T = 20 K<br>T = 25 K<br>10 T = 30 K<br>T = 35 K<br>T = 40 K<br>T = 50 K<br>T = 60 K<br>1 T = 77 K<br>(a)<br>0.1<br>100   = 45°<br>10<br>(b)<br>1<br> = 90°<br>100<br>10<br>Bruker HTS<br>(c)<br>1<br>0.01 0.1 1 10<br>Magnetic field [T]<br> [kA/mmJc<br> [kA/mmJc<br> [kA/mmJc<br>2]<br>2]<br>2]<br>**----- End of picture text -----**<br>

**Figure 4** Magnetic field dependence of Jc between 5 K and 77 K for the tape from Bruker HTS. Measurements were performed for three orientations of the magnetic field, θ = 0° (a), 45°(b) and 90° (c). Jc data are extracted from inductive (smaller symbols) and transport (larger symbols) measurements. Magnetic and transport data are in good agreement at all temperatures using the abovementioned normalization at 40 K, 7 T. 

Tapes from SuNAM and SuperOx exhibit a monotonic decrease of T* with field independently of the orientation. For the other coated conductors, T*(0°) and T*(45°) reach a maximum between 2 T and ≈ 8 T followed by a smooth decrease as field increases, while T*(90°) decreases (BHTS and Fujikura) or stays nearly constant (AMSC and SuperPower) with increasing field. 

The exponential T-dependence in eq. (1) provides a simple rule to estimate the variations of Jc with temperature. If temperature is varied by  T, the value of Jc changes by a factor 𝑒[−][][𝑇𝑇] ⁄[∗] that does not depend on initial and final temperatures. For a given tape, the temperature lift-factor depends only on B. 

## _**4.2. Magnetic field dependence of the critical current density**_ 

Typical results for the magnetic field dependence of Jc are reported in Figure 4, which shows exemplary data measured for the BHTS tape in the temperature range between 5 K and 77 K. The curves, obtained by electrical transport and inductive measurements, show a low field plateau followed by a smooth decrease of Jc for fields higher than a given threshold. The threshold field depends on temperature and orientation. Its value is typically  0.5 T between 5 K and 77 K. The log-log plot of the data reveals that the field-induced decrease of Jc is well 

![](images/tmpwtbipewf.pdf-0008-00.png)

**----- Start of picture text -----**<br>
1.4 1.4<br>AMSC   =  0° Bruker HTS   =  0° Fujikura   =  0°<br>1.2   =  45°   =  45°   =  45° 1.2<br>  =  90°   =  90°   =  90°<br>1.0 1.0<br>0.8 0.8<br>0.6 0.6<br>0.4 0.4<br>0.2 (a) (b) (c) 0.2<br><br>1.4 1.4<br>SuNAM   =  0° SuperOx   =  0° SuperPower   =  0°<br>1.2   =  45°   =  45°   =  45° 1.2<br>  =  90°   =  90°   =  90°<br>1.0 1.0<br>0.8 0.8<br>0.6 0.6<br>0.4 0.4<br>0.2 (d) (e) (f) 0.2<br>0 20 40 60 80 0 20 40 60 80 0 20 40 60 80<br>Temperature [K]<br>**----- End of picture text -----**<br>

**Figure 5** Temperature dependence of the field scaling parameter,  , for Jc as determined for the tapes from six industrial manufacturers: open symbols for θ = 0°, half-filled symbols for θ = 45° and solid symbols for θ = 90°. Dashed and solid lines are given as guides to the eye. 

![](images/tmpwtbipewf.pdf-0008-02.png)

**----- Start of picture text -----**<br>
400 B = 3 T SuperPower<br>T = 5 K<br>T = 20 K<br>T = 30 K<br>300<br>T = 20 K<br>T = 50 K<br>200<br>100<br>0<br>0 45 90<br>Angle respect to the c-axis<br> [kA/mmJc<br>2]<br>**----- End of picture text -----**<br>

**Figure 6** Jc at B = 3 T for the three angular orientations θ = 0°, 45° and 90° and the temperatures T = 5 K, 20 K, 30 K, 40 K and 50 K, as measured for the SuperPower tape. As a consequence of the artificial pinning, Jc(50 K, 3 T, 0°) > Jc(50 K, 3 T, 90°). 

described by a power law dependence, i.e. Jc  B[-][] , with an uncertainty of 5% or better. We observed the power law regime in the field range 0.5 – 19 T for T  30 K, but only between 0.1 and 1 T at 77 K. When approaching the irreversibility line, Jc decreases faster and departs from the power law. 

Figure 5 shows the temperature dependence of the power law coefficient  at θ = 0°, 45° and 90° for the investigated samples.  values have been obtained by fitting the Jc(B) curves using a power law in the field range where the linearity in the log-log plot is observed.  (0°) is almost constant in the temperature range 5 – 40 K, the lowest and the highest  -values being ≈ 0.55 for SuperOx and BHTS and ≈ 0.75 for SuperPower, respectively. The value of  (0°) is lower for the PLD-grown REBCO films (BHTS, Fujikura, SuperOx). From a fundamental point of view, the dependence with  = 0.5 is determined by the interaction between vortices nucleated at the grain 

![](images/tmpwtbipewf.pdf-0009-00.png)

**----- Start of picture text -----**<br>
100<br>BHTS T2290<br>BHTS T2291 BHTS T2289<br>BHTS T150 SuperPower SuperOx<br>BHTS T003<br>Fujikura<br>AMSC<br>SuNAM<br>BHTS T002<br>10<br>2.5<br>2.5 10 100<br>Jc(77K,s.f.) [kA/mm2]<br>(4.2K,19T,0°) [kA/mmJc<br>2]<br>**----- End of picture text -----**<br>

**Figure 7** Jc of the REBCO layers measured at 4.2 K, 19 T, θ = 0° versus Jc of the same layers measured at 77 K, self-field for six different manufacturers. 

boundaries and those strongly pinned to the dislocation cores [29, 30]. In the coated conductors where the REBCO layer is grown by chemical routes, dislocations do not connect from the bottom to the top of the film due to the grain boundary meandering [31, 32]. Therefore, c-axis correlated disorder becomes weaker and point-like defects play a role in the pinning landscape, leading to higher values of  [31]. 

The higher is the value of  , the faster is the decrease of Jc with increasing field. We observe that at temperatures below 30 K,  (90°) is smaller than  (0°) for all the examined tapes, while at higher temperatures the  (90°) curve intersects  (0°). The interpretation of this behaviour is intuitive. Since Jc goes to zero at Tc regardless of the field orientation, the higher is Jc the faster has to be its in-field decrease when increasing temperature. In REBCO tapes without artificial pinning, the highest Jc is observed for the orientation corresponding to θ = 90° and it follows that  (90°) has to become larger than  (0°) when temperature approaches Tc. The tape from SuperPower with artificial pinning represents a case apart.  (0°) stays higher than  (90°) over the explored temperature range and exhibits an upturn curvature at 40 K (see Fig. 5f).  The manufacturer introduced BZO nanosized columns oriented along the REBCO c-axis to modify the pinning landscape and improve the electrical transport properties. One of the consequences is that the angular dependence of Jc in the field region below 10 T varies with the temperature. This is illustrated in Fig. 6 where we report the values of Jc for the three orientations at B = 3 T and T = 5, 20, 30, 40 and 50 K. Below 30 K, the orientation with θ = 0° exhibits the lowest critical current. In the range from 30 K to 40 K, the minimum Jc was measured at θ = 45°, while at T = 50 K we observe a peak at θ = 0°, i.e. Jc(0°) > Jc(45°) > Jc(90°). When approaching Tc, the in-field decrease has to be faster in the orientation corresponding to the highest Jc that, in case of the SuperPower tape, corresponds to  (0°) >  (90°). 

## **5. Discussion** 

Figure 7 reports a plot of Jc(77 K, self field) versus Jc(4.2 K, 19 T) measured at θ = 0° for various tapes, including the CCs listed in table I and five additional tapes from BHTS (T003, T150, T2289, T2290 and T2291). Our results show that it is not possible to find a univocal correlation between critical current values at low temperature/high field and at 77 K/self field when comparing the performance of CCs from various manufacturers or even from 

different production batches of a single manufacturer. A recent study on REBCO thin films made by MOCVD, both doped and undoped, finds a linear correlation between Jc(T, B, θ = 0°) and Jc(77 K, 3 T, 0°) from 77 K down to 20 K and magnetic fields up to 9 T [33]. This is not the case for the commercial tapes examined in this work. In particular, we observe that tapes with inferior performance at 77 K yield superior critical currents at low temperature/high field. This occurs in the tapes from Bruker specially developed for high-field magnet applications, where the addition of nanoscale defects tailored in shape, size and spatial distribution leads to a strong enhancement of vortex pinning. 

In spite of the large variability of CCs’ performance, our analysis shows that field and temperature dependences of the critical current density at a given angle are well described by the simple expression 

![](images/tmpwtbipewf.pdf-0010-02.png)

over a wide range of temperatures and magnetic fields. In particular, magnetization data show that Eq. (2) holds for fields starting from ~0.1 T up to ~60% of the irreversibility field, Birr, with a moderate dependence of  on temperature below 40 K. On the other hand, the scaling parameter for the temperature dependence, T*, was found to vary with magnetic field and the largest variations are encountered for the orientation with θ = 90°. 

## **6. Conclusions** 

In summary, we have investigated the electromagnetic properties of REBCO coated conductors from six industrial manufacturers. The analysis proposed in this paper shows that the critical surface Jc(T, B) at a given orientation can be reconstructed with a reduced number of measurements by combining the results of transport and magnetic measurements. To this end, it is sufficient to 

- measure the transport Ic at a single temperature over a field range that partly overlaps the range explored by magnetization. 

- use the values of Jc extracted from the transport Ic to set the coefficient of proportionality between irreversible magnetization and critical current density. 

Thanks to the lower technical complexity of magnetization measurement, it becomes easy to explore the critical surface over a wide range of fields and temperatures. Our study provides also the scaling relations for the field and temperature dependences of Jc. The experiments show that, in spite of the large variability of the CCs’ performance, the Jc of the examined tapes follows an exponential law for the temperature dependence, between 4.2 K and 50 K, and a power law for the field dependence, up to 60% of Birr. Moreover, the temperature and field scaling parameters can be determined with minimal experimental effort by combining magnetic and transport measurements. This analysis is intended to provide a basic tool to magnet designers for modelling the behaviour of a high field insert. 

## **Acknowledgments** 

Financial support was provided by the Swiss National Science Foundation (Grant No. PP00P2_144673 and Grant No. 51NF40-144613). Research also supported by FP7 EuCARD-2 http://eucard2.web.cern.ch. EuCARD-2 is cofounded by the partners and the European Commission under Capacities 7th Framework Programme, Grant Agreement 312453. The authors warmly acknowledge Damien Zurmuehle for his technical assistance. 

## **References** 

- [1] Senatore C, Alessandrini M, Lucarelli A, Tediosi R, Uglietti D and Iwasa Y 2014 Progresses and challenges in the development of high-field solenoidal magnets based on RE123 coated conductors _Superconductor Science and Technology_ **27** 103001 

- [2] Barth C, Mondonico G and Senatore C 2015 Electro-mechanical properties of REBCO coated conductors from various industrial manufacturers at 77K, self-field and 4.2K, 19T _Superconductor Science and Technology_ **28** 045011 

- [3] Bonura M and Senatore C 2015 High-field thermal transport properties of REBCO coated conductors _Superconductor Science and Technology_ **28** 025011 

- [4] Hazelton D W, Rice J A, Hascicek Y S, Weijers H W and Vansciver S W 1995 Development and Test of a Bscco-2223 Hts High-Field Insert Magnet for Nmr _Applied Superconductivity, IEEE Transactions on_ **5** 234-7 

- [5] Snitchler G, Kalsi S S, Manlief M, Schwall R E, Sidi-Yekhlef A, Ige S, Medeiros R, Francavilla T L and Gubser D U 1999 High-field warm-bore HTS conduction cooled magnet _Applied Superconductivity, IEEE Transactions on_ **9** 553-8 

- [6] Markiewicz W D, Larbalestier D C, Weijers H W, Voran A J, Pickard K W, Sheppard W R, Jaroszynski J, Xu A, Walsh R P, Lu J, Gavrilin A V and Noyes P D 2012 Design of a Superconducting 32 T Magnet With REBCO High Field Coils _Applied Superconductivity, IEEE Transactions on_ **22** 4300704 

- [7] Bascunan J, Hahn S, Park D K, Kim Y and Iwasa Y 2012 On the 600 MHz HTS Insert for a 1.3 GHz NMR Magnet _Applied Superconductivity, IEEE Transactions on_ **22** 4302104 

- [8] Rossi L, Badel A, Bajko M, Ballarino A, Bottura L, Dhalle M M J, Durante M, Fazilleau P, Fleiter J, Goldacker W, Haro E, Kario A, Kirby G, Lorin C, van Nugteren J, de Rijk G, Salmi T, Senatore C, Stenvall A, Tixador P, Usoskin A, Volpini G, Yang Y and Zangenberg N 2015 The EuCARD-2 Future Magnets European Collaboration for Accelerator-Quality HTS Magnets _Applied Superconductivity, IEEE Transactions on_ **25** 4001007 

- [9] Gade P V, Barth C, Bayer C, Fietz W H, Franza F, Heller R, Hesch K and Weiss K P 2014 Conceptual Design of a Toroidal Field Coil for a Fusion Power Plant Using High Temperature Superconductors _Applied Superconductivity, IEEE Transactions on_ **24** 4202705 

- [10] Uglietti D, Seeber B, Abächerli V, Carter W L and Flükiger R 2006 Critical currents versus applied strain for industrial Y-123 coated conductors at various temperatures and magnetic fields up to 19 T _Superconductor Science and Technology_ **19** 869-72 

- [11] Braccini V, Xu A, Jaroszynski J, Xin Y, Larbalestier D C, Chen Y, Carota G, Dackow J, Kesgin I, Yao Y, Guevara A, Shi T and Selvamanickam V 2011 Properties of recent IBAD–MOCVD coated conductors relevant to their high field, low temperature magnet use _Superconductor Science and Technology_ **24** 035001 

- [12] Senatore C 2014 Overview of CC critical surface for EuCARD-2, 1st Workshop on Accelerator Magnets in HTS, Germany http://indico.cern.ch/event/308828/session/7/contribution/22/material/slides/0.pdf 

- [13] Long N J 2013 Maximum Entropy Distributions Describing Critical Currents in Superconductors _Entropy_ **15** 2585-605 

- [14] Hilton D K, Gavrilin A V and Trociewitz U P 2015 Practical fit functions for transport critical current versus field magnitude and angle data from (RE)BCO coated conductors at fixed low temperatures and in high magnetic fields _Superconductor Science and Technology_ **28** 074002 

- [15] Markiewicz W D 2008 Protection of HTS Coils in the Limit of Zero Quench Propagation Velocity _Applied Superconductivity, IEEE Transactions on_ **18** 1333-6 

- [16] Trillaud F, Ang I, Kim W-S, Lee H G, Iwasa Y and Voccio J P 2007 Protection and Quench Detection of YBCO Coils Results With Small Test Coil Assemblies _Applied Superconductivity, IEEE Transactions on_ **17** 2450-3 

- [17] Goyal A, Norton D P, Kroeger D M, Christen D K, Paranthaman M, Specht E D, Budai J D, He Q, Saffian B, List F A, Lee D F, Hatfield E, Martin P M, Klabunde C E, Mathis J and Park C 1997 Conductors with controlled grain boundaries: An approach to the next generation, high temperature superconducting wire _Journal of Materials Research_ **12** 2924-40 

- [18] Groves J R, Arendt P N, Kung H, Foltyn S R, DePaula R F, Emmert L A and Storer J G 2001 Texture development in IBAD MgO films as a function of deposition thickness and rate _Applied Superconductivity, IEEE Transactions on_ **11** 2822-5 

- [19] Usoskin A, Kirchhoff, Knoke J, Prause B, Rutt, Selskij and Farrell D E 2007 Processing of Long-Length YBCO Coated Conductors Based on Stainless Steel Tapes _Applied Superconductivity, IEEE Transactions on_ **17** 3235-8 

- [20] Malozemoff A P, Fleshler S, Rupich M, Thieme C, Li X, Zhang W, Otto A, Maguire J, Folts D, Yuan J, Kraemer H P, Schmidt W, Wohlfart M and Neumueller H W 2008 Progress in high temperature superconductor coated conductors and their applications _Superconductor Science and Technology_ **21** 034005 

- [21] Selvamanickam V, Galinski G B, Carota G, DeFrank J, Trautwein C, Haldar P, Balachandran U, Chudzik M, Coulter J Y, Arendt P N, Groves J R, DePaula R F, Newnam B E and Peterson D E 2000 High-current Y–Ba–Cu–O superconducting films by metal organic chemical vapor deposition on flexible metal substrates _Physica C: Superconductivity_ **333** 155-62 

- [22] Nagaishi T, Shingai Y, Konishi M, Taneda T, Ota H, Honda G, Kato T and Ohmatsu K 2009 Development of REBCO coated conductors on textured metallic substrates _Physica C: Superconductivity_ **469** 1311-5 

- [23] Igarashi M, Kakimoto K, Hanyu S, Tashita C, Hayashida T, Hanada Y, Fujita S, Morita K, Nakamura N, Sutoh Y, Kutami H, Iijima Y and Saitoh T 2010 Remarkable progress in fabricating RE123 coated conductors by IBAD/PLD technique at Fujikura _Journal of Physics: Conference Series_ **234** 022016 

- [24] Usoskin A, Knoke J, Garcia-Moreno F, Issaev A, Dzick J, Sievers S and Freyhardt H C 2001 Large-area HTS-coated stainless steel tapes with high critical currents _Applied Superconductivity, IEEE Transactions on_ **11** 3385-8 

- [25] Oh S S, Ha H S, Kim H S, Ko R K, Song K J, Ha D W, Kim T H, Lee N J, Youm D, Yang J S, Kim H K, Yu K K, Moon S H, Ko K P and Yoo S I 2008 Development of long-length SmBCO coated conductors using a batch-type reactive co-evaporation method _Superconductor Science and Technology_ **21** 034003 

- [26] Matias V, Rowley J, Coulter Y, Maiorov B, Holesinger T, Yung C, Glyantsev V and Moeckly B 2010 YBCO films grown by reactive co-evaporation on simplified IBAD-MgO coated conductor templates _Superconductor Science and Technology_ **23** 014018 

- [27] Puig T, Gutierrez J, Pomar A, Llordes A, Gazquez J, Ricart S, Sandiumenge F and Obradors X 2008 Vortex pinning in chemical solution nanostructured YBCO films _Superconductor Science and Technology_ **21** 034008 

- [28] Gutierrez J, Puig T and Obradors X 2007 Anisotropy and strength of vortex pinning centers in YBa2Cu3O7-x coated conductors _Applied Physics Letters_ **90** 162514 

- [29] Dam B, Huijbregtse J M, Klaassen F C, van der Geest R C F, Doornbos G, Rector J H, Testa A M, Freisem S, Martinez J C, Stauble-Pumpin B and Griessen R 1999 Origin of high critical currents in YBa2Cu3O7-delta superconducting thin films _Nature_ **399** 439-42 

- [30] Palau A, Puig T, Gutierrez J, Obradors X and de la Cruz F 2006 Pinning regimes of grain boundary vortices in YBa2Cu3O7-x coated conductors _Physical Review B_ **73** 132508 

- [31] Miura M, Maiorov B, Baily S A, Haberkorn N, Willis J O, Marken K, Izumi T, Shiohara Y and Civale L 2011 Mixed pinning landscape in nanoparticle-introduced YGdBa2Cu3Oy films grown by metal organic deposition _Physical Review B_ **83** 184519 

- [32] Feldmann D M, Holesinger T G, Feenstra R, Cantoni C, Zhang W, Rupich M, Li X, Durrell J H, Gurevich A and Larbalestier D C 2007 Mechanisms for enhanced supercurrent across meandered grain boundaries in high-temperature superconductors _Journal of Applied Physics_ **102** 083912 

- [33] Xu A, Delgado L, Heydari Gharahcheshmeh M, Khatri N, Liu Y and Selvamanickam V 2015 Strong correlation between Jc(T, H||c) and Jc(77K, 3T||c) in Zr-added (Gd, Y)BaCuO coated conductors at temperatures from 77 down to 20K and fields up to 9T _Superconductor Science and Technology_ **28** 082001 

