---
source: "https://www.frontiersin.org/journals/nuclear-engineering/articles/10.3389/fnuen.2026.1714531/full"
source_type: "url"
extracted_at: "2026-05-18T06:12:31.014280+00:00"
content_hash_sha256: "bc320ed54fe78c9186147f6c84da14a2185e7baa8497d2239fbe1e3968c2401e"
backend: "trafilatura"
title: "Frontiers | Evaluation of the Lawson criterion for aneutronic proton-boron-11 fusion: effects of ion temperature and bremsstrahlung losses"
author: "Ahmad; Irfan Maulana; Husin; Abd Djamil; Tai; Duong Thanh; Tamam; Nissren; Sulieman; Abdelmoneim; Yani; Sitti"
---

## Abstract

Nuclear fusion, the process of combining light nuclei to form heavier nuclei, offers a promising pathway to sustainable clean energy with minimal radioactive waste. The Lawson criterion, expressed as the product of plasma density, confinement time, and temperature, establishes the conditions required for ignition and net energy gain. This study investigates the Lawson criterion for proton-boron-11 (p-11B) fusion across ion temperatures of 75–500 keV, incorporating fusion reactivity data from Tentori-Belloni and Nevins-Swain, as well as energy losses from bremsstrahlung radiation under different electron-to-ion temperature ratios (*=* 1, 0.5, 0.25). The Tentori-Belloni dataset yields higher fusion reactivity than Nevins-Swain, resulting in more favorable Lawson values. Net energy production is achieved only when *<*, with optimal operating windows identified at 190–330 keV for *= 0.5* and 125–500 keV for *= 0.25*. At *< 230 keV*, the Lawson criterion decreases due to plasma instabilities and confinement limitations; in this work, radiative losses are evaluated using derived from the p-11B fuel mixture () only, while external impurity contributions are not explicitly modeled. For *> 230 keV*, the Lawson criterion increases, reaching characteristic minima around 330 keV and 500 keV. These thresholds represent the minimum conditions required to achieve ignition and sustain a self-sufficient fusion reaction. The minimum Lawson values obtained were 1.3 × 1022 m−3s (no radiation), 1.2 × 1023 m−3s (*= 0.5*), and 1.5 × 1022 m−3s (*= 0.25*). These findings highlight the critical role of accurate cross-section data and electron-ion temperature control in advancing aneutronic p-11B fusion toward practical, self-sustained clean energy systems.

## 1 Introduction

Nuclear fusion has emerged as a promising sustainable energy source with the potential to replace conventional fossil-based systems. Fusion occurs when two light nuclei combine to form a heavier nucleus, releasing a substantial amount of energy due to the mass-energy conversion. Importantly, the radioactive waste generated is considerably lower than that produced in nuclear fission, making fusion an attractive solution to the dual challenges of rising global energy demand and environmental sustainability ([Cohn and Bromberg, 1986](https://www.frontiersin.org#B5); [Mohamed et al., 2024](https://www.frontiersin.org#B17); [Nicholas et al., 2021](https://www.frontiersin.org#B20); [Sadik-Zada et al., 2024](https://www.frontiersin.org#B26)).

Current fusion research has largely focused on deuterium-tritium (D-T) fuel. Although D-T reactions achieve high cross sections at relatively low temperatures (less than 200 keV), they generate energetic neutrons that cause severe damage to reactor materials ([Eliezer et al., 1998](https://www.frontiersin.org#B6); [Koohrokhi and Azadifar, 2016](https://www.frontiersin.org#B11)). This reaction uses relatively low plasma temperatures, making it more realistic to develop in fusion reactors, especially in confinement technology. In addition, this reaction releases a significant amount of energy, around 17.6 MeV, making it more efficient in energy conversion. However, tritium fuel is very rare and must be produced through a series of complex processes called tritium breeding. Furthermore, the D-T fusion reaction produces high-energy neutrons, which cause neutron activation in reactor materials and subsequent production of radioactive waste, which are difficult to control in fusion reactors ([Pettinari et al., 2024](https://www.frontiersin.org#B23); [Sandri et al., 2020](https://www.frontiersin.org#B27); [Serikov and Sheludjakov, 2001](https://www.frontiersin.org#B28); [Vogelsang and Khater, 1987](https://www.frontiersin.org#B33)). While major international fusion programs remain centered on the D–T fuel cycle, aneutronic fuels have attracted sustained scientific interest for several decades because of their potential to reduce neutron-induced material damage and long-lived radioactive waste ([Meschini et al., 2023](https://www.frontiersin.org#B16); [Meschini et al., 2021](https://www.frontiersin.org#B15); [Mohamed et al., 2024](https://www.frontiersin.org#B17); [Nayak, 2013](https://www.frontiersin.org#B18); [Sadik-Zada et al., 2024](https://www.frontiersin.org#B26)). Foundational studies, including those of ([Feoktistov, 1998](https://www.frontiersin.org#B8); [Shmatov, 2019](https://www.frontiersin.org#B29)), highlight both the promise and the challenges associated with aneutronic fusion. Among these, the proton-boron-11 (p-11B) reaction is particularly attractive for future applications ([Liu, 2024](https://www.frontiersin.org#B13); [Oh and Lee, 2017](https://www.frontiersin.org#B21); [Rogers et al., 2025](https://www.frontiersin.org#B25)).

The p-11B fusion reaction primarily yields three alpha particles (helium-4 nuclei) through multiple pathways, including sequential decay via beryllium-8. In this process, an excited carbon-12 nucleus with an extremely short half-life decays into one alpha particle and an unstable beryllium-8 nucleus, which subsequently disintegrates into two additional helium-4 nuclei ([Adam and Bednarz, 2016](https://www.frontiersin.org#B1)). Both ground-state and excited-state decay channels of beryllium-8 contribute to the overall reaction. The total energy released is about 8.68 MeV-approximately 10 MeV less than that of the D-T reaction. However, a significant challenge for p-11B fusion is the high Coulomb barrier, requiring ion temperatures on the order of 200 keV to achieve appreciable reactivity ([Oh and Lee, 2017](https://www.frontiersin.org#B21)). The challenges discussed here primarily concern magnetic confinement systems, where ignition thresholds and bremsstrahlung losses dominate the feasibility of p–11B fusion. In inertial confinement fusion, however, the primary limitation shifts to the acceptability and confinement of the energy release during the microexplosion, as highlighted in the works of ([Weaver et al., 1973](https://www.frontiersin.org#B34); [Feoktistov, 1998](https://www.frontiersin.org#B8); [Shmatov, 2019](https://www.frontiersin.org#B29)).

The feasibility of sustaining fusion reactions is commonly evaluated using the Lawson criterion, which relates the energy balance of a plasma to the so-called triple product: electron density (*n* e), confinement time (τ), and temperature (

*T*). For ignition to occur, the energy produced by fusion must exceed the total losses, including those from radiation and transport; (

[Chaerani et al., 2024](https://www.frontiersin.org#B4);

[Entler et al., 2023](https://www.frontiersin.org#B7);

[Shumlak et al., 2024](https://www.frontiersin.org#B30)). Thus, analysis of the Lawson criterion is essential for determining whether a plasma can be maintained in a self-sustaining state. Since both reactivity and losses are strongly temperature-dependent, evaluating the effect of varying ion and electron temperatures is critical.

The discussion of the internal heating mechanism that affects the energy balance—and ultimately determines the tightness or looseness of the three products required by the Lawson Criteria—includes the contribution of fusion particles, particularly α particles. An early discussion of the non-thermal α particle population and its impact on the p–11B energy balance can be found in the classic work by [Weaver et al. (1973)](https://www.frontiersin.org#B34), as well as in subsequent analyses by [Shmatov (2019)](https://www.frontiersin.org#B29). Recent research by [Ghorbanpour and Belloni (2024)](https://www.frontiersin.org#B9) shows that the suprathermal α particle population formed during the deceleration of 2.9 MeV fusion products can significantly modify the effective energy balance of the p–11B plasma. Within the framework of the power balance, heating by α particles (both through energy deposition during deceleration and after thermalization) acts as an additional internal heating source that generally reduces the confinement requirement to achieve sustainable conditions. Because the Maxwellian thermal model used in this study does not explicitly include α particle heating and does not resolve the non-Maxwellian kinetics required to describe the suprathermal α distribution, the Lawson Criteria estimates obtained here should be viewed as conservative: the neglect of α heating tends to make the Lawson criterion appear more stringent, i.e., it increases the minimum predicted value of neτ (or the product of three neTτ) for a given operating temperature compared to when α heating is taken into account in a self-consistent manner. Thus, the results presented here should be interpreted as a basic Maxwellian complement to, rather than a replacement for, a more comprehensive suprathermal analysis.

The objective of this study is to determine the minimum Lawson criterion for p-11B fusion by analyzing ion temperatures in the range of 75–500 keV. The analysis incorporates different electron-to-ion temperature ratios, fusion reactivity based on the parameterizations of Tentori-Belloni and Nevins-Swain, and bremsstrahlung radiation losses, in order to identify the plasma conditions most favorable for ignition.

## 2 Methodology

### 2.1 Fusion parameters and reactivity

This study builds on the work of

[Tentori and Belloni (2023)](https://www.frontiersin.org#B32)

who reported that the reactivity of proton-boron-11 (p-

11

B) fusion reaches a minimum at an ion temperature (

*Tᵢ*

) of approximately 70 keV. Accordingly, the present analysis evaluates

*Tᵢ*

in the range of 75–500 keV, with increments of 5 keV. For reference, 1 keV corresponds to 1.16 × 10

7

K (

[Tentori and Belloni, 2023](https://www.frontiersin.org#B32)

). In addition to fusion reactivity, the study incorporates energy losses due to bremsstrahlung radiation, which is a dominant radiative loss mechanism in high-temperature plasmas. To capture its dependence on electron temperature, three electron-to-ion temperature ratios were considered:

and

.


These scenarios enable evaluation of how reduced electron temperatures relative to ions can mitigate bremsstrahlung losses and influence the overall Lawson criterion. The selection of the ratio used is based on previous research in which the ion and electron temperature ratio is adjusted to compare the energy obtained between the fusion energy rate and the bremsstrahlung energy rate so as to produce the optimal net energy rate in the fusion reaction ([Wurzel and Hsu, 2022](https://www.frontiersin.org#B35); [Xie, 2024](https://www.frontiersin.org#B36)).

### 2.2 Fusion reactivity calculations

Fusion reactivity was determined using a combination of experimental measurements and analytical formulations based on the Maxwell-Boltzmann distribution of fusion cross sections. These approaches are consolidated into a simplified expression for reactivity, as proposed by [Peres (1979)](https://www.frontiersin.org#B22). The fusion reactivity calculation uses the following [Equation 1](https://www.frontiersin.org#e1).

In which is a Pade approximation based on Basdevant (1972) in accordance with [Equation 2](https://www.frontiersin.org#e2).

*P* n is a fitting constant based on research by

[Tentori and Belloni (2023)](https://www.frontiersin.org#B32)and

[Nevins and Swain (2000)](https://www.frontiersin.org#B19)in

[Table 1](https://www.frontiersin.org#T1)(

[Nevins and Swain, 2000](https://www.frontiersin.org#B19);

[Tentori and Belloni, 2023](https://www.frontiersin.org#B32)).

*k*is the Boltzmann constant with a value of 1,

*T*

is the plasma ion temperature in keV, and

*i**E*

is the Gamow energy in keV. Gamow energy is the minimum energy required for a fusion reaction to begin. This energy is based on the Coulomb barrier of a nuclear fusion reaction (

*G*[Khodadadi Azadboni et al., 2024](https://www.frontiersin.org#B10)).

TABLE 1

| Parameters | Tentori-Belloni | Nevins-Swain |
|---|---|---|
P1 [keV m3 s−1] | 4.4467 | |
P2 [keV−1] | 5.9357 | |
P3 [keV−1] | 2.0165 | |
P4 [keV−1] | 1.0404 | |
P5 [keV−1] | 2.7621 | |
P6 [keV−1] | −9.1653 | |
P7 [keV−1] | 9.8305 | |
Eg [keV] | 22,589 | 22,589 |
| [keV] | 859,526 | 859,526 |

Parameters used in the Tentori-Belloni and Nevins-Swain studies.

### 2.3 Fusion energy rate

The nuclear fusion energy rate refers to [Lawson’s (1957)](https://www.frontiersin.org#B12) modification of the general nuclear fusion energy rate equation in [Equation 3](https://www.frontiersin.org#e3) below ([Lawson, 1957](https://www.frontiersin.org#B12))

According to [Rider (1997)](https://www.frontiersin.org#B24), the values can be modified based on the plasma neutrality condition ([Equation 4](https://www.frontiersin.org#e4)) ([Rider, 1997](https://www.frontiersin.org#B24)).

With and is charge and density n particle, is the total ion density, and is the average charge of the ion. is the ratio of *n* 1 and

*n*

, is the ratio of the ion density of particle 1 to the total ion density, and . If , then the electron charge equation becomes as follows.

*2*Therefore, *n* 1 and

*n*


*2*The modified fusion energy rate equation is as follows ([Equation 5](https://www.frontiersin.org#e5)).*n* e is electron density in m

-3, is fusion reactivity in m

3s

−1, and is energy released in fusion reactions in keV.

### 2.4 Plasma heating rate

The plasma heating energy rate equation refers to a modification of [Xie (2024)](https://www.frontiersin.org#B36) basic formula, as shown in [Equation 6](https://www.frontiersin.org#e6) below ([Xie, 2024](https://www.frontiersin.org#B36)).with , so that the [Equation 6](https://www.frontiersin.org#e6) can be rewritten as [Equation 7](https://www.frontiersin.org#e7) as follows:*k* is Boltzmann konstant = 1, *W* is the rate of plasma heating energy in keV m-6, *n* e and

*z*

is electron density and average ion charge, respectively.

*i*### 2.5 Rate of energy loss

Nuclear fusion loses a certain amount of energy during the fusion process. The rate of energy lost during nuclear fusion is caused by the interaction of ions and plasma electrons, known as bremsstrahlung ([Wurzel and Hsu, 2022](https://www.frontiersin.org#B35)). The rate of energy lost due to bremsstrahlung is formulated in [Equation 8](https://www.frontiersin.org#e8) as follows.

The relativistic correction factor is formulated as [Equation 9](https://www.frontiersin.org#e9) as follows.

With

And is bremsstrahlung constant = 5.39 × 10−37 m3 ke , is relativistic correction factor, *Z* eff is effective charge, is rest energy of electrons, and is plasma electron temperature in keV.

### 2.6 Lawson criterion analysis

The Lawson criterion equation was calculated based on Lawson’s research used in [Chaerani et al. (2024)](https://www.frontiersin.org#B4) by modifying the plasma heating.

Lawson criterion is modified into the following [Equation 10](https://www.frontiersin.org#e10). is Lawson criterion in m-3 s, is the energy recovery factor based on Lawson’s research = , *T* i and

*T*

are the ion and electron temperatures in keV, and

*e**k*is Boltzmann constant = 1. The energy recovery factor is a measure of the amount of energy released by a fusion reaction that can be reused to support the fusion reaction process.

## 3 Results and discussion

### 3.1 Fusion reactivity

Fusion reactivity is the probability of a nuclear fusion reaction to occur, calculated based on the fusion cross section or the probability of two nuclei colliding, the velocity of the nuclear particles, and the plasma temperature function (*T* i and

*T*

) using the basic concepts of the Maxwell-Boltzmann distribution (

*e*[Chaerani et al., 2024](https://www.frontiersin.org#B4)). The fusion reactivity calculation uses the Peres formula, with the results presented in

[Figure 1](https://www.frontiersin.org#F1)resulted in Tentori-Belloni and Nevins-Swain fusion reactivity value of approximately 2.777 × 10

−235.619 × 10

−22m

3s

−1and 2.455 × 10

−233.741 × 10

−22m

3s

−1, respectively.

FIGURE 1

As expected, reactivity increases with ion temperature, indicating that more fusion reactions occur as *Tᵢ* rises. Both datasets show a sharp increase in ⟨σν⟩ for *Tᵢ* > 100 keV, with an exponential-like growth. However, the Nevins-Swain reactivity curve tends to plateau between 200 and 500 keV, whereas the Tentori-Belloni dataset continues to rise.

The Tentori-Belloni parametrization yields consistently higher fusion reactivity values compared to Nevins-Swain. This is because Tentori-Belloni incorporates the most recent and accurate cross-section measurements reported by [Sikora and Weller (2016)](https://www.frontiersin.org#B31), combined with earlier data from [Buck et al. (1983)](https://www.frontiersin.org#B3) covering proton energy ranges of 0.15–3.80 MeV and 5.70–9.76 MeV ([Buck et al., 1983](https://www.frontiersin.org#B3)). In contrast, the Nevins-Swain study relied on older and less precise cross-section data from [Becker et al. (1987)](https://www.frontiersin.org#B2) and Segel et al. (1965) which were limited to narrower proton energy ranges of 0.22–1.10 MeV and 1.10–3.48 MeV ([Becker et al., 1987](https://www.frontiersin.org#B2)). Furthermore, Tentori-Belloni explicitly accounts for contributions from both ground-state and excited-state decay channels of beryllium-8 and applies more accurate data extrapolations, whereas Nevins-Swain does not separate these effects. As shown in [Figure 4](https://www.frontiersin.org#F4), fusion reactivity in both datasets increases significantly for *Tᵢ* > 100 keV; however, Nevins-Swain remains relatively constant in the range *Tᵢ* = 200–500 keV.

Overall, the Tentori-Belloni parametrization predicts more favorable reactivity for p-11B fusion, reinforcing the importance of modern cross-section evaluations in accurately assessing ignition feasibility.

### 3.2 Fusion energy rate and Bremsstrahlung radiation

The fusion of protons and boron-11 releases 8.68 MeV of energy, with the reactivity value of proton and boron-11 fusion being relatively smaller than that of deuterium-tritium and deuterium-helium-3 fusion. As a result, ideal conditions are required to achieve the net energy rate stage, where the rate of fusion energy produced can exceed the rate of radiation produced. The ideal ratio of *n* 1 (protons) and

*n*

(boron-11) must be adjusted so that the rate of fusion energy produced exceeds the rate of radiation produced. The assumed ratio of proton density to total ion density () is 0.9. Boron density () is set to 0.1 or the ratio of proton and boron ion density is approximately 90:10 (

*2*[Wurzel and Hsu, 2022](https://www.frontiersin.org#B35)).

Bremsstrahlung radiation is influenced by the effective charge of and , where the effective charge of proton and boron-11 fusion is 2.4. Relativistic corrections affect the bremsstrahlung radiation rate, especially at >100 keV, so this ion temperature was chosen for this study. The conditions Te and Ti are also varied with the assumptions *T**e**= T* i,

*T*

= 0.5

*e**T*

, and

*i**T*

= 0.25

*e**T*

to determine the ideal Ti condition so that the resulting fusion energy rate exceeds the bremsstrahlung radiation rate.

*i*#### 3.2.1 Case 1: Bremsstrahlung radiation rate for Te = Ti

[Figure 2](https://www.frontiersin.org#F2) shows that at *T* e=

*T*

, the bremsstrahlung radiation rate is 8.968 × 10

*i*−207.780 × 10

−19keV s

−1m

-3for the range

*T*

= 75–500 keV. The rate of fusion energy produced by protons and boron-11 is lower than the bremsstrahlung radiation rate. The bremsstrahlung radiation effect is very dominant under these conditions due to low fusion reactivity. The relatively large mass number of boron-11 (

*i**Z*

= 5) and the relativistic correction factor contribute to an increase in the bremsstrahlung radiation rate, resulting in an exponential curve. This condition cannot produce net energy in either the Tentori-Belloni or Nevins-Swain fusion reactions, necessitating a fusion reaction condition where

*2**T*

<

*e**T*

to reduce the bremsstrahlung radiation rate.

*i*FIGURE 2

#### 3.2.2 Case 2: Bremsstrahlung radiation rate for Te = 0.5Ti

[Table 2](https://www.frontiersin.org#T2) shows a comparison of the results of the Tentori-Belloni fusion energy rate, the bremsstrahlung radiation rate, and the net energy rate produced. The ideal conditions for achieving the net energy of the Tentori-Belloni fusion system need to be achieved and maintained at *T* i = 190–330 keV with a net energy rate of 11.254 × 10

−211.362 × 10

−21keV s

−1m

-3. The bremsstrahlung radiation rate will increase at

*T*

> 330 keV so that no net energy from proton and boron-11 fusion is produced. However, these ideal conditions are not achieved in Nevins-Swain due to the fusion reactivity produced being much smaller than the Tentori-Belloni fusion energy rate, thus requiring conditions of

*i**T*

< 0,5

*e**T*

.

*i*TABLE 2

T temperature (keV)i |
a |
|---|


b

c−19−19−21−19−19−22−19−19−21−19−19−21−19−19−21−19−19−21−19−19−21−19−19−21−19−19−21−19−19−23−19−19−20−19−19−20−19−19−20Fusion energy rate and Tentori-Belloni Bremsstrahlung radiation with *Te =* 0.5*Ti*.


aEnergy rate produced by fusion reactions ().


bBremsstrahlung radiation rate ().


cNet energy rate ().

[Figure 3](https://www.frontiersin.org#F3) shows the condition *T* e <

*T*

assuming

*i**T*

= 0.5

*e**T*

, the bremsstrahlung radiation rate curve has a value of 5.534 × 10

*i*−203.001 × 10

−19keV s

−1m

−3. The Tentori-Belloni fusion energy rate can overcome the bremsstrahlung radiation effect at

*T*

= 190–330 keV to meet the net energy requirement, whereas at

*i**T*

< 190 keV or

*i**T*

> 330 keV, the net energy rate will be negative or the nuclear fusion system will produce more bremsstrahlung radiation than the fusion energy rate produced, making it not profitable. At

*i**T*

> 330 keV, conditions of

*i**T*

< 0.5

*e**T*

are required to reduce bremsstrahlung radiation, which increases rapidly under these conditions. The Nevins-Swain fusion energy rate curve cannot compensate for the bremsstrahlung radiation rate produced because the resulting curve is smaller and accompanied by a flat curve at

*i**T*

> 300 keV, so a condition of

*i**T*

< 0.5

*e**T*

is required to obtain ideal net energy conditions.

*i*FIGURE 3

#### 3.2.3 Case 3: Bremsstrahlung radiation rate for Te = 0.25Ti

[Table 3](https://www.frontiersin.org#T3) shows that bremsstrahlung radiation is much greater than the fusion energy rate produced at *T* i < 125 keV for Tentori-Belloni and

*T*

< 140 keV for Nevins-Swain. The ideal conditions of the Tentori-Belloni fusion system in the Ti = 125–500 keV range produce net energy of 1.058 × 10–21 8.474 × 10–20 keV s

*i*−1m

−3, while the Nevins-Swain fusion system requires a

*T*

range of 140–500 keV with a net energy of 2.075 × 10

*i*−219.885 × 10

−21keV s

−1m

−3.

TABLE 3

T (keV)i |
a |
|---|

[(keV s](https://www.frontiersin.org#Tfn5)

b−1m

-3)


c−20−20−20−21−20−20−20−20−21−21−20−20−20−21−21−20−20−20−21−21−20−20−20−21−22−20−20−20−20−21−20−20−20−20−21−19−19−19−20−20−19−19−19−20−20−19−19−19−20−21Fusion and bremsstrahlung energy rates with *T* e = 0.25

*T*

.

*i*

aEnergy rate produced by fusion reactions ().


bBremsstrahlung radiation rate ().


cNet energy rate ().

The Nevins-Swain fusion system at *T* i > 500 keV requires other

*T*

assumptions to minimize the bremsstrahlung radiation energy that begins to increase at that ion temperature.

*e*[Figure 4](https://www.frontiersin.org#F4) shows the bremsstrahlung radiation rate of 3.673 × 10−20 to 1.392 × 10−19 keV s−1 m−3 for the range *T* i = 75–500 keV under the assumption

*T*

= 0.25

*e**T*

. The Tentori-Belloni fusion energy rate requires an ion temperature greater than 125 keV in order to overcome the bremsstrahlung radiation effect and produce minimum net energy, while the Nevins-Swain fusion energy rate requires Ti greater than 140 keV. The assumption

*i**T*

= 0.25

*e**T*

is the ideal condition for a proton and boron-11 fusion system to overcome the effects of the bremsstrahlung radiation rate. However, for

*i**T*

> 500 keV, especially at the Nevins-Swain fusion energy rate, other

*i**T*

assumptions are needed because the bremsstrahlung rate begins to increase.

*e*FIGURE 4

Bremsstrahlung radiation affects the net energy yield of proton and boron-11 nuclear fusion. The net energy yield can only be achieved when the condition *T* i >

*T*

is used to reduce the effect of bremsstrahlung radiation. The Tentori-Belloni net energy rate is satisfied under two conditions, namely

*e**T*

= 0.5

*e**T*

in the range of

*i**T*

= 190–330 keV and

*i**T*

= 0.25

*e**T*

in the range of

*i**T*

= 125–500 keV with a minimum

*i**T*

of 125 keV. The Nevins-Swain net energy rate is only satisfied at

*i**T*

= 0.25Ti with the net energy rate located in the range of

*e**T*

= 140–500 keV. The net energy rate is used as a condition to ensure that the fusion reaction produces more energy than the energy wasted during the fusion process by optimizing the ion temperature (

*i**T*

) and electron temperature ratio (

*i**T*

).

*e*### 3.3 Lawson criterion analysis

The Lawson criterion is used in fusion systems to assess sustainable nuclear fusion based on plasma temperature (ions and electrons), electron density (*n* e), and plasma confinement time, also known as the triple product. These three factors are essential for the energy produced to exceed all losses due to energy dissipation during the fusion reaction process. The Lawson criterion value depends on fusion reactivity, the rate of energy produced by nuclear fusion, and the average ion charge value, where the average ion charge of proton and boron-11 fusion is 1.4. In addition, the Lawson criterion value is influenced by bremsstrahlung radiation with several

*T*

and

*e**T*

assumptions. Differences in fusion reactivity data and

*i**T*

and

*e**T*

conditions cause differences in the Ti range used and differences in the Lawson criterion values produced.

*i*The Lawson criterion calculated using Tentori-Belloni are satisfied in three conditions: without bremsstrahlung radiation, with bremsstrahlung radiation at *T* e = 0.25

*T*

and with bremsstrahlung radiation at

*i**T*

= 0.25

*e**T*

. The Lawson criterion values vary, where without radiation the value is 1.322 × 10

*i*22–1.740 × 10

22m

−3s for the range

*T*

= 200–500 keV, with radiation (

*i**T*

= 0.5

*e**T*

) values of 2.586 × 10

*i*23–1.337 × 10

24m

−3s for the

*T*

= 200–330 keV range, and with radiation (

*i**T*

= 0.25

*e**T*

) values of 1.717 × 10

*i*22–2.586 × 10

22m

−3s.

Meanwhile, the Lawson Nevins-Swain criterion is satisfied in two cases: without radiation, with values of 1.611 × 1022–2.613 × 1022 m-3 s at *T* i = 200–500 keV and with the addition of bremsstrahlung radiation (

*T*

= 0.25

*e**T*

) so that the Lawson criterion value is 2.928 × 10

*i*22–2.217 × 10

23m

−3s in the range of

*T*

= 200–500 keV. The Nevins-Swain Lawson criterion value is much greater than the Tentori-Belloni Lawson criterion value due to the much smaller fusion energy produced, which affects the difference in the Lawson criterion value calculation results. In addition, the Lawson criterion value without radiation has a lower value than with radiation. The presence of bremsstrahlung radiation will increase the minimum ion temperature, confinement time, and electron density (

*i**n*

) required to confine the plasma.

*e*[Figures 5](https://www.frontiersin.org#F5), [6](https://www.frontiersin.org#F6) show the Lawson Tentori-Belloni criterion value curve and the Lawson Nevins-Swain criterion value curve. The Tentori-Belloni curve is relatively more varied than the Nevins-Swain curve, with both resembling a half parabolic and a parabolic. The Tentori-Belloni curve without radiation and with (*T* e = 0.5

*T*

) resembles a half parabolic with a flatter curve compared to radiation, while the curve with radiation (

*i**T*

= 0.25

*e**T*

) resembles a parabolic curve.

*i*FIGURE 5

FIGURE 6

The Nevins-Swain curve is satisfied only in two conditions, namely without radiation and with radiation (*T* e = 0.25

*T*

). The curve with radiation is more parabolic in shape than the curve without radiation, which is flatter. Both figures will experience a decrease in Lawson’s criterion value at

*i**T*

< 230 keV. This decrease is caused by plasma instability and cooling, plasma confinement mechanisms in the reactor, impurities, and other factors.

*i*The minimum point of the Lawson Tentori-Belloni criterion is achieved at *T* i = 245 keV with 1.289 × 10

22m

−3s without radiation,

*T*

= 250 keV with 1.171 × 10

*i*23m

−3s with radiation (

*T*

= 0.5

*e**T*

), and

*i**T*

= 270 keV with 1.503 × 10

*i*22m

−3s with radiation (

*T*

= 0.25

*e**T*

). The minimum of the Lawson Nevins-Swain criterion is achieved at

*i**T*

= 230 keV with 1.598 × 10

*i*22m

−3s without radiation and

*T*

= 250 keV with 2.600 × 10

*i*22m

−3s with radiation (

*T*

= 0.25

*e**T*

). Under these conditions, the Lawson criterion value will increase as a function of Ti. This value indicates a sufficiently dense electron density during the plasma confinement duration to achieve self-sustained plasma and ignition.

*i*Theoretically, the and ratios can be optimized and adjusted to obtain the optimal fusion energy rate in a fusion reaction as simulated in this study. However, in practice, the condition is very difficult to apply because electrons absorb energy more easily, so the electron temperature () value is easier to adjust, and easier to increase than the ion temperature (.

## 4 Conclusion

This study evaluated the Lawson criterion for aneutronic proton-boron-11 fusion over ion temperatures of 75–500 keV, considering different electron-to-ion temperature ratios and updated cross-section datasets. The results show that ignition is unattainable when *T**e**= Tᵢ* because bremsstrahlung losses dominate, but becomes feasible when *T**e**< Tᵢ*, particularly at *Tᵢ ≥ 125–190 keV*. The Tentori-Belloni parametrization predicts higher reactivity and broader ignition windows than Nevins-Swain, with minimum Lawson triple product values of 1.3 × 1022–1.2 × 1023 m-3s depending on *T**e**/Tᵢ*. These findings highlight the critical importance of accurate cross-section data and electron-ion temperature control in enabling p-11B fusion, reinforcing its potential as a sustainable, neutron-free pathway to clean energy.

## Statements

### Data availability statement

The raw data supporting the conclusions of this article will be made available by the authors, without undue reservation.

### Author contributions

IA: Conceptualization, Data curation, Resources, Formal Analysis, Methodology, Investigation, Writing – original draft. AH: Methodology, Supervision, Conceptualization, Writing – original draft, Investigation. DT: Writing – review and editing, Funding acquisition, Project administration, Validation. NT: Writing – review and editing, Funding acquisition, Project administration, Validation. AS: Supervision, Project administration, Writing – review and editing, Resources, Funding acquisition. SY: Writing – original draft, Funding acquisition, Supervision, Investigation, Project administration, Visualization.

### Funding

The author(s) declared that financial support was received for this work and/or its publication. This work was supported by the Program Riset dan Inovasi untuk Indonesia Maju (RIIM), LPDP, and BRIN (Contract Nos. B-4131/II.7.5/TK/01.03/02/2025 and B-1703/III.2/TK.01.03/1/2-25), and the Princess Nourah bint Abdulrahman University Researchers Supporting Project (Grant No. PNURSP2026R12).

### Acknowledgments

We extend our gratitude to the Program Riset dan Inovasi untuk Indonesia Maju (RIIM), an initiative by Lembaga Pengelola Dana Pendidikan (LPDP) and Badan Riset dan Inovasi Nasional (BRIN), for their support. This research was conducted under the contract agreement between the Directorate of Research and Innovation Funding, National Research and Innovation Agency (BRIN), and the Research Organization for Nuclear Energy (ORTN), through the Skema Riset dan Inovasi untuk Indonesia Maju Invitasi Strategis Gelombang ke-2, under contract numbers B-4131/II.7.5/TK/01.03/02/2025 and B-1703/III.2/TK.01.03/1/2-25. The authors also express their gratitude to Princess Nourah bint Abdulrahman University Researchers Supporting Project (Grant No. PNURSP2026R12), Princess Nourah bint Abdulrahman University, Riyadh, Saudi Arabia. We acknowledge Nguyen Tat Thanh University, Ho Chi Minh City, Vietnam for supporting this study.

### Conflict of interest

The author(s) declared that this work was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

### Generative AI statement

The author(s) declared that generative AI was not used in the creation of this manuscript.

Any alternative text (alt text) provided alongside figures in this article has been generated by Frontiers with the support of artificial intelligence and reasonable efforts have been made to ensure accuracy, including review by the authors wherever possible. If you identify any issues, please contact us.

### Publisher’s note

All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those of the publisher, the editors and the reviewers. Any product that may be evaluated in this article, or claim that may be made by its manufacturer, is not guaranteed or endorsed by the publisher.

## References

1

AdamD.BednarzB. (2016). SU-F-T-140: assessment of the proton boron fusion reaction for practical radiation therapy applications using MCNP6.

*Med. Phys.*43, 3494. 10.1118/1.49562762

BeckerH. W.RolfsC.TrautvetterH. P. (1987). Low-energy cross sections for11B(p, 3α). Z. Für Phys. At.

*Nucl.*327, 341–355. 10.1007/BF012844593

BuckW.HoylerF.StäblerA.StaudtG.KlapdorH. V.OeschlerH. (1983). Alpha-cluster break-up and reaction mechanism in (p, α) reactions on light nuclei.

*Nucl. Phys. A*398, 189–202. 10.1016/0375-9474(83)90482-74

ChaeraniJ.HusinA. D.YaniS. (2024). Lawson criterion analysis of D-3He fusion reaction.

*J. Phys. Conf. Ser.*2734, 012067. 10.1088/1742-6596/2734/1/0120675

CohnD. R.BrombergL. (1986). Advantages of high-field tokamaks for fusion reactor development.

*J. Fusion Energy*5, 161–170. 10.1007/BF010506106

EliezerS.HenisZ.Martínez-ValJ. M.PieraM. (1998). Deuterium-tritium fusion reactors without external tritium breeding.

*Phys. Lett. A*243, 311–318. 10.1016/S0375-9601(98)00258-87

EntlerS.HoracekJ.FickerO.KovarikK.KolovratnikM.DostalV. (2023). Estimation of fuel operating ranges of fusion power plants.

*Nucl. Eng. Technol.*55, 2687–2696. 10.1016/j.net.2023.04.0248

FeoktistovL. P. (1998). Thermonuclear detonation.

*Phys.-Uspekhi*41, 1139–1147. 10.1070/PU1998v041n11ABEH0005069

GhorbanpourE.BelloniF. (2024). On the ignition of H11B fusion fuel.

*Front. Phys.*12, 1405435. 10.3389/fphy.2024.140543510

Khodadadi AzadboniF.MahdaviM.KhademloE. (2024). Proton-boron-11 fusion under effect of the temperature turbulence. Iran.

*J. Phys. Res.*24, 99–109. 10.47176/ijpr.24.3.7193711

KoohrokhiT.AzadifarR. (2016). Effect of internal breeding of tritium and helium-3 on the ignition of an ICF fuel pellet.

*J. Fusion Energy*35, 493–497. 10.1007/s10894-016-0077-y12

LawsonJ. D. (1957). Some Criteria for a power producing thermonuclear reactor.

*Proc. Phys. Soc. Sect. B*70, 6–10. 10.1088/0370-1301/70/1/30313

LiuS. J.WuD.HuT. X.LiangT. Y.NingX. C.LiangJ. H.et al (2024). Proton-boron fusion scheme taking into account the effects of target degeneracy.

*Phys. Rev. Res.*6, 013323. 10.1103/PhysRevResearch.6.01332314

MeschiniS.ZucchettiM.PagliucaE. (2021). Development of an advanced-fuel nuclear fusion experiment.

*Fusion Sci. Technol.*77, 784–790. 10.1080/15361055.2021.192146115

MeschiniS.LavianoF.LeddaF.PettinariD.TestoniR.TorselloD.et al (2023). Review of commercial nuclear fusion projects.

*Front. Energy Res.*11, 1157394. 10.3389/fenrg.2023.115739416

MohamedM.ZakuanN. D.Tengku HassanT. N. A.LockS. S. M.Mohd ShariffA. (2024). Global development and readiness of nuclear fusion Technology as the alternative source for clean energy supply.

*Sustainability*16, 4089. 10.3390/su1610408917

NayakB. (2013). Reactivities of neutronic and aneutronic fusion fuels.

*Ann. Nucl. Energy*60, 73–77. 10.1016/j.anucene.2013.04.02518

NevinsW. M.SwainR. (2000). The thermonuclear fusion rate coefficient for p-11B reactions.

*Nucl. Fusion*40, 865–872. 10.1088/0029-5515/40/4/31019

NicholasT. E. G.DavisT. P.FedericiF.LelandJ.PatelB. S.VincentC.et al (2021). Re-examining the role of nuclear fusion in a renewables-based energy mix.

*Energy Policy*149, 112043. 10.1016/j.enpol.2020.11204320

OhB. S.LeeJ. I. (2017). Proton and Boron-11 nuclear fusion reaction experiment using proton accelerator.

21

PeresA. (1979). Fusion cross sections and thermonuclear reaction rates.

*J. Appl. Phys.*50, 5569–5571. 10.1063/1.32674822

PettinariD.TestoniR.ZucchettiM.ParisiM. (2024). Neutron transport and activation comparison between OpenMC and FISPACT-II in ARC-class reactor.

*Fusion Eng. Des.*209, 114713. 10.1016/j.fusengdes.2024.11471323

RiderT. H. (1997). Fundamental limitations on plasma fusion systems not in thermodynamic equilibrium.

*Phys. Plasmas*4, 1039–1046. 10.1063/1.87255624

RogersJ. G.EglyA. A.RohY. S.TerryR. E.WesselF. J. (2025). A Quasi-spherical fusion reactor burning boron-11 fuel.

*Plasma*8, 26. 10.3390/plasma803002625

Sadik-ZadaE. R.GattoA.WeißnichtY. (2024). Back to the future: revisiting the perspectives on nuclear fusion and juxtaposition to existing energy sources.

*Energy*290, 129150. 10.1016/j.energy.2023.12915026

SandriS.ContessaG. M.D’ArienzoM.GuardatiM.GuarracinoM.PoggiC.et al (2020). A review of radioactive wastes production and potential environmental releases at experimental nuclear fusion Facilities.

*Environments*7, 6. 10.3390/environments701000627

SerikovA. G.SheludjakovS. V. (2001). Method for three-dimensional activation analysis of fusion reactor materials.

*Plasma Devices Oper.*9, 237–272. 10.1080/1051999010822976028

ShmatovM. L. (2019). Igniting a microexplosion by a microexplosion and some other controlled thermonuclear fusion scenarios with neutronless reactions.

*Phys.-Uspekhi*62, 70–81. 10.3367/UFNe.2018.03.03830429

ShumlakU.MeierE. T.LevittB. J. (2024). Fusion gain and triple product for the sheared-flow-stabilized Z pinch.

*Fusion Sci. Technol.*80, 1–16. 10.1080/15361055.2023.219804930

SikoraM. H.WellerH. R. (2016). A new evaluation of the

11B(p,*α*)*α**α*Reaction Rates.*J. Fusion Energy*35, 538–543. 10.1007/s10894-016-0069-y31

TentoriA.BelloniF. (2023). Revisiting p-11B fusion cross section and reactivity, and their analytic approximations.

*Nucl. Fusion*63, 086001. 10.1088/1741-4326/acda4b32

VogelsangW. F.KhaterH. Y. (1987). The impact of D—3He fusion reactors on waste disposal.

*Fusion Eng. Des.*5, 367–377. 10.1016/S0920-3796(87)90157-833

WeaverT.ZimmermanG.WoodL. (1973). “Exotic CTR fuels: non-thermal effects and laser fusion applications,” in

*Report number: UCRL--74938; CONF-731009--10*(Livermore: Lawrence Livermore Lab).34

WurzelS. E.HsuS. C. (2022). Progress toward fusion energy breakeven and gain as measured against the Lawson criterion.

*Phys. Plasmas*29, 062103. 10.1063/5.008399035

XieH. (2024). Introduction to fusion ignition principles: zeroth order factors of fusion energy research. 10.48550/arXiv.2410.18054


## Summary

Keywords

Bremsstrahlung radiation, fusion reaction, fusion reactivity, Lawson criterion, proton-boron-11

Citation

Ahmad IM, Husin AD, Tai DT, Tamam N, Sulieman A and Yani S (2026) Evaluation of the Lawson criterion for aneutronic proton-boron-11 fusion: effects of ion temperature and bremsstrahlung losses. *Front. Nucl. Eng.* 5:1714531. doi: [10.3389/fnuen.2026.1714531](http://dx.doi.org/10.3389/fnuen.2026.1714531)

Received

17 October 2025

Revised

08 February 2026

Accepted

09 February 2026

Published

24 February 2026

Volume

5 - 2026

Edited by

[Mahmoud Bakr Arby](https://loop.frontiersin.org/people/2733329/overview), University of Bristol, United Kingdom

Reviewed by

[Fabio Panza](https://loop.frontiersin.org/people/2244918/overview), Energy and Sustainable Economic Development (ENEA), Italy

[Arkady Serikov](https://loop.frontiersin.org/people/1543895/overview), Karlsruhe Institute of Technology (KIT), Germany

Updates

Copyright

© 2026 Ahmad, Husin, Tai, Tamam, Sulieman and Yani.

This is an open-access article distributed under the terms of the [Creative Commons Attribution License (CC BY)](https://creativecommons.org/licenses/by/4.0/). The use, distribution or reproduction in other forums is permitted, provided the original author(s) and the copyright owner(s) are credited and that the original publication in this journal is cited, in accordance with accepted academic practice. No use, distribution or reproduction is permitted which does not comply with these terms.

*****Correspondence: Sitti Yani, [sittiyani@apps.ipb.ac.id](mailto:sittiyani@apps.ipb.ac.id); Duong Thanh Tai, [dttai@ntt.edu.vn](mailto:dttai@ntt.edu.vn)

Disclaimer

All claims expressed in this article are solely those of the authors and do not necessarily represent those of their affiliated organizations, or those of the publisher, the editors and the reviewers. Any product that may be evaluated in this article or claim that may be made by its manufacturer is not guaranteed or endorsed by the publisher.