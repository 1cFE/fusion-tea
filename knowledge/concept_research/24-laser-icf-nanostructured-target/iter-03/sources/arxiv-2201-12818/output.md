---
source: "https://arxiv.org/pdf/2201.12818"
source_type: "url"
extracted_at: "2026-04-20T16:20:02.571215+00:00"
content_hash_sha256: "e690759208922a964ee4e8e07a523c0b929fe13a3ab66ef907f88ae5b651be57"
backend: "pdf_pipeline"
---

## **A study of the requirements of p-[11] B fusion reactor by tokamak** 

## **system code** 

**Jianqing Cai[1,2] , Huasheng Xie*[1,2] , Yang Li[1,2] , Michel Tuszewski[3] , Hongbin** 

## **Zhou[1,2] and Peipei Chen[1,2 ]** 

1Hebei Key Laboratory of Compact Fusion, Langfang 065001, China 

2ENN Science and Technology Development Co., Ltd., Langfang 065001, China 

3ENN Consultant, Riverside, CA 92506, USA 

E-mail: *xiehuasheng@enn.cn, huashengxie@gmail.com 

Accepted for Publication July 31, 2021, FUSION SCIENCE AND TECHNOLOGY 

## **Abstract** 

Most tokamak devices including ITER exploit the D-T reaction due to its high reactivity, but the wall loading caused by the associated 14MeV neutrons will limit the further development of fusion performance at high beta. To explore p-[11] B fusion cycle, a tokamak system code is extended to incorporate the relativistic bremsstrahlung since the temperature of electrons is approaching the rest energy of electron. By choosing an optimum p-[11] B mix and ion temperature, some representative sets of parameters of p-[11] B tokamak reactor, whose fusion gain exceeds 1, have been found under the thermal wall loading limit and beta limit when synchrotron radiation loss is neglected. However, the fusion gain greatly decreases when the effect of synchrotron radiation loss is considered. Helium ash also plays an important role in the fusion performance, 

and we have found that the helium confinement time must be below the energy 

confinement time to keep the helium concentration ratio in an acceptable range. 

## **I. Introduction** 

A successful design of tokamak device is based on the good understanding of dependence of performance on key plasma parameters, such as density, temperature, magnetic field, current, etc. To study the dependence of these parameters, a tokamak system code (TSC) based on one-dimensional model has been developed, which considers a simple profile assumption. 

The tokamak system code was firstly developed in the design of tokamak reactor since 1980s.[1, 2] Stambaugh et al gave a more concise description of the system code to study the physical and engineer limits that restrict the design of fusion power reactor. 3, 4 Then it has been extended by Costley et al to study the regime of steady-state reactors with high fusion gain, who found the fusion gain depends strongly on the fusion power and energy confinement, and weakly on the size of device, while the steady-state reactor is operating at fixed fractions of the density and beta limits.[5] 

The tokamak system code has been used successfully on the deuterium-tritium (D-T) fusion reactor,[3-6] while the 14MeV-neutrons-induced damage and degradation would limit the useful lifetime of reactor component.[7] The neutron production in p- 11B fuel is lower than that in D-T and deuterium- deuterium (D-D) fuel by orders of magnitude. Furthermore, hydrogen and boron are abundant and fairly accessible on earth, while[3] He might be mined and transported from the moon, which is one of the 

ingredients of deuterium-helium-3 (D-[3] He) fuel. Therefore, there are sufficient reasons 

for us to pay more attention on proton-boron (p-[11] B) fusion cycle. Since the core temperature of electrons is approaching the rest energy of electron, relativistic effect has to be considered in the extended tokamak system code to incorporate the relativistic bremsstrahlung. This extended tokamak system code is designed to include physics module, engineer module and economy module, the latter two of which are still under development and will be finished in the future work. 

Of course, the ion temperature and 𝑛"𝜏$ being high as 300keV and 10[''] 𝑚[)*] 𝑠 for p-[11] B fuel, is far beyond the current experiment condition. In this paper, we hypothesize the fuel ions could be heated up to the temperatures that p-[11] B fusion reaction requires by certain method, mechanism of which is not the main point this paper discuss. Under this premise, we could further explore the p-[11] B fusion cycle and study the requirements of p-[11] B fusion reactor under some optimistic assumptions. 

This paper is organized as follow: Sec 1 is the introduction of p-[11] B fusion and the Tokamak System Code. Sec. 2 is the main equations used in this code. Sec. 3 is the results derived by the extended Tokamak System code. Sec. 4 is the conclusion and discussion. 

## **II. Equations of the tokamak system code** 

In this tokamak system code, a simple parabolic radial profile has been considered. Here, 0-dimensional model does not include the profile effects of density and temperature, whereas 1-dimensional model considers some certain density and temperature radial profiles. 

The extended tokamak system code is developed from the models described in the paper by Stambaugh[3, 4] , Petty[6] and Costley[5] . In terms of the fusion power of p-[11] B fuel and the relativistic bremsstrahlung, the model has been revised accordingly, and the confinement enhancement factor H has been used here to measure the confining capacity needed for p-[11] B reactor compared with the existing capabilities. 

## II.A. Geometry of tokamak 

The geometry of tokamak size is described by parameters like aspect ratio 𝐴 major radius 𝑅. , elongation 𝜅 and triangularity 𝛿 , from which other geometry parameters can be deduced: 

The minor radius 

![](images/tmpuvd0j4ve.pdf-0004-04.png)

The elongation 

![](images/tmpuvd0j4ve.pdf-0004-06.png)

The plasma volume 

![](images/tmpuvd0j4ve.pdf-0004-08.png)

The wall area 

![](images/tmpuvd0j4ve.pdf-0004-10.png)

Since low-aspect-ratio tokamak has the advantage of burning plasmas in a 

compact geometry at a lower cost than in conventional tokamak, we consider a low- 

aspect ratio tokamak device 𝐴= 1.4 and 𝛿= 0.5 as Figure 1 shows, which would 

prove to be a convenient choice later in the paper. 

## II.B. Pressure and beta 

In the p-[11] B plasma, the density related parameters are as follows: the proton density 𝑛H, the density of boron ion 𝑛U, the ion density of p-B fuel 𝑛",HU, the electron density 𝑛W and the density of helium ion 𝑛XW, the profiles of which are described by the same parabolic form 

![](images/tmpuvd0j4ve.pdf-0005-03.png)

where x=r/a is the normalized radial distance, the suffix zero in the subscripts means 

the core density and 𝑆\ is the exponent of density profile. In this paper, densities are 

in units of 10[20] m[-3] , and in what follows the units are generally m, s, T, MW, MA, keV. 

Besides, the fractional ion densities are defined as 𝑓HU = 𝑛H/𝑛U, 𝑓U = 𝑛U/𝑛",HU, 

𝑓XW = 𝑛XW/𝑛W. From proportional relation, we have 

![](images/tmpuvd0j4ve.pdf-0005-09.png)

From charge balance, we have 

![](images/tmpuvd0j4ve.pdf-0005-11.png)

and core electron and ion density can be expressed as 

![](images/tmpuvd0j4ve.pdf-0005-13.png)

![](images/tmpuvd0j4ve.pdf-0005-14.png)

The line-averaged density is 

![](images/tmpuvd0j4ve.pdf-0005-16.png)

The effective charge is 

![](images/tmpuvd0j4ve.pdf-0006-00.png)

And the average mass is 

![](images/tmpuvd0j4ve.pdf-0006-02.png)

The temperature profiles are assumed to be the similar parabolic form 

![](images/tmpuvd0j4ve.pdf-0006-04.png)

and 𝑆l is the exponent of temperature profile, indicating this is one-dimensional model. The cross-section is considered to be elliptic in the integral computation, and 

triangularity is only used while calculating the volume and area. Refer to the previous 

papers,[5, 6] the density profile has taken Sn=0.5 for a broad H-mode profile with a pedestal, and the temperature profile was assumed steeper, ST=1.5, which is shown in Figure 1. 

The profile effect has been considered in the calculation of triple product to compare with the result of 0-dimensional mode, which is shown in Figure 2. Figure 2 illustrates that, Lawson criterion of D-T, D-[3] He and D-D fusion reactor could meet at the same density of fuel ions, and the same ion and electron temperature whether in 0-dimensional model or in 1-dimensional model. But in the p-[11] B fusion reactor, the optimum mix of proton and Boron is not 1:1, and the ion and electron temperature must also be different while the profile effect has been considered. Here we define the ratio of ion to electron temperature as 

![](images/tmpuvd0j4ve.pdf-0006-09.png)

The optimum mix of proton and Boron and the critical ratio of ion to electron 

temperature will be discussed in more details in Section 3. The toroidal beta, normalized beta and poloidal beta is given by 

![](images/tmpuvd0j4ve.pdf-0007-01.png)

![](images/tmpuvd0j4ve.pdf-0007-02.png)

where 𝐼H is plasma current and 𝐵l. is core magnetic field strength. 

## II.C. Fusion power 

In p-[11] B fuel, the fusion power element is written as 

![](images/tmpuvd0j4ve.pdf-0007-06.png)

in which the fusion reactivity is used from the recent evaluation by Sikora and Weller.[8] 

Using 𝑥= 𝑟/𝑎, the fusion power can be represented as 

![](images/tmpuvd0j4ve.pdf-0007-09.png)

𝜎𝑣 is determind by x, since the fusion reactivity is a function of ion temperature, and 

ion temperature is a function of 𝑥. We use 𝜙 to replace with fusion reactivity integral 

![](images/tmpuvd0j4ve.pdf-0007-12.png)

and once the core ion temperature and the profile exponent has been given, the fusion 

reactivity integral is determined. The core ion density of p-B fuel can be represented 

as 

![](images/tmpuvd0j4ve.pdf-0007-16.png)

The fusion gain equals fusion power divided by auxiliary heating power 

![](images/tmpuvd0j4ve.pdf-0008-00.png)

The condition of Q=1, when the fusion power is equal to the auxiliary heating power, 

is referred to as scientific breakeven. Since this paper is mostly focus on physics 

module, the engineering breakeven and economic breakeven are not discussed here. 

## II.D. Plasma current 

In p-[11] B reactor, an empirical current driven efficiency formula derived in tokamak 

has been used,[9] and the driven current can be calculated by 

![](images/tmpuvd0j4ve.pdf-0008-07.png)

𝜁‘’ is the dimensionless current drive efficiency, which is taken as 0.2 here. The safety factor can be calculated from 

![](images/tmpuvd0j4ve.pdf-0008-09.png)

In addition to the driven current, the rest is the bootstrap current 

![](images/tmpuvd0j4ve.pdf-0008-11.png)

where 𝑓^{  is the bootstrap current fraction. From Andrade and Ludwig,[10] the 

bootstrap current fraction 𝑓^{ can be deduced from 

![](images/tmpuvd0j4ve.pdf-0008-14.png)

∗ where 𝐶^{ = 0.1558 ± 0.0005 , 𝐶H = 1 + 𝑆\ + 𝑆l , internal inductance  𝑙"  has 

been taken as 0.5, and ––n = 0.8. We define a constant 𝑐𝑜𝑛𝑠𝑡= Q›œˆ∗ ¡"›[u.o] b ¨¨n = 7.16𝐶H, 

then substitute the equation of 𝛽q and 𝑞W\™ into equation (22), after which the bootstrap current fraction could be expressed as 

![](images/tmpuvd0j4ve.pdf-0009-00.png)

where 𝐹= 𝐴[..Q] 7[®] Ukno rkM/–n . The plasma current and bootstrap current can be J.. deduced by equation (21) and (23), and the solution is 

![](images/tmpuvd0j4ve.pdf-0009-02.png)

Hence the bootstrap current fraction could also be deduced. The Greenwald density limit is expressed as 

![](images/tmpuvd0j4ve.pdf-0009-04.png)

## II.E. Radiation 

One of the main difficulties for p-[11] B fuel is that the bremsstrahlung radiation 

power loss is even higher than fusion power without synchrotron radiation. In the non- 

relativistic case, the bremsstrahlung radiation power per unit volume is given by 

![](images/tmpuvd0j4ve.pdf-0009-09.png)

In the p-[11] B reaction, the relativistic electrons have to be considered since electron 

temperature is approaching the rest energy of electron. The relativistic electron-ion 

bremsstrahlung power per unit volume is given by 

![](images/tmpuvd0j4ve.pdf-0009-13.png)

where classical electron radius 𝑟W = 2.818×10[)JQ] 𝑚 , fine structure constant  𝛼= 

1/137 , electron mass m¹ = 9.11×10[)*J] 𝑘𝑔 , light speed c = 2.998×10[Š] 𝑚/𝑠 , elementary charge e = 1.6×10[)J½] 𝐶 ,the normalized electron temperature with 

lh respect to the rest energy of electron 𝑡= and 𝜂$ ≈0.5616.[11, 12] 6h‘[o] 

At this temperature, the bremsstrahlung radiation caused by the electron-electron 

scattering is comparable to that caused by the electron-ion scattering. And the relativistic electron-electron bremsstrahlung power per unit volume is[11, 12] 

![](images/tmpuvd0j4ve.pdf-0010-03.png)

Hence, the total bremsstrahlung power is 

![](images/tmpuvd0j4ve.pdf-0010-05.png)

In addition to bremsstrahlung radiation, synchrotron radiation is one of the important energy loss mechanisms in magnetically confined p-[11] B plasmas, whose critical role has been discussed in the previous work,[13, 14] showing the p-[11] B fuel can’t generate net power in a magnetic confinement device with the synchrotron radiation loss. The synchrotron radiation loss could be obtained from 

![](images/tmpuvd0j4ve.pdf-0010-07.png)

J where 𝑛Waa = 𝑛W./(1 + 𝑆\) is the volume averaged density, 𝑇Waa = . 𝑇W(𝑥) 𝑑𝑥 is the effective electron temperature, _Rw_ is the wall reflectivity, 𝑎Waa = 𝑎𝜅[..Q] is the effective minor radius and 𝑉= 2𝜋𝑅.𝜋𝑎Waa' is the approximation of the plasma volume.[15, 16] In this paper, the cases of considering the effect of synchrotron radiation loss and neglecting synchrotron radiation loss would both been discussed. 

## II.F.Confinement 

The confinement time could be obtained by 

![](images/tmpuvd0j4ve.pdf-0011-02.png)

and a confinement enhancement factor H is used here to compared the confinement 

time needed for p-[11] B fuel compared with the confinement time predicted by ITER98y2 High-confinement mode (H-mode) scaling[17] 

![](images/tmpuvd0j4ve.pdf-0011-05.png)

![](images/tmpuvd0j4ve.pdf-0011-06.png)

## **III.Results** 

In D-T, D-[3] He and D-D fusion reactor, one of the main goals is to study the 

dependence of the fusion performance especially fusion gain Q on which plasma and devices parameters. But in p-[11] B fusion reactor, a lot of optimistic assumptions and optimum parameters are needed to consider firstly to achieve Q=1, which is described 

by a simple logic diagram as shown in Figure 3. 

In p-[11] B fusion reactor, the hydrogen-boron mix needs to be carefully evaluated 

firstly to maximize the ratio of fusion power to radiation power. The range of ion temperature and 𝑛"𝜏$ could be confirmed by the breakeven condition. Besides, the 

constraint of beta and thermal wall loading are also important, which are related with 

the magnetic field limit and ion density limit, respectively. Combined with the IPB98y2 

scaling of energy confinement time, the effect of H factor and major radius on fusion 

performance can be studied. 

## III.A. The concentration ratio of hydrogen to boron 

The ratio of fusion power to radiation power …†‡ˆ is a function of ion …œ±h 

temperature, electron temperature and the concentration ratio of hydrogen to boron 𝑓HU. To obtain the optimum value of 𝑓HU which maximizes equation (34), the ratio of ion to electron temperature 𝑓l has been extracted, and the extremum problem has been simplified to maximizing 𝐹(𝑓HU, 𝑇W) by choosing the optimum value of 𝑓HU. 

![](images/tmpuvd0j4ve.pdf-0012-04.png)

A color map of ……œ±h †‡ˆ versus electron temperature and 𝑓HU is shown in figure 4. The optimal value of ratio 𝑓HU =9:1, which maximizes ……œ±h †‡ˆ with fixed electron temperature. Nevertheless, the maximum value of …†‡ˆ obtained in this simulation …œ±h is still below 0.5, which indicates that higher ratio of ion to electron temperature is 

…†‡ˆ needed in order to obtain higher ~~.~~ …œ±h 

## III.B. The ratio of ion to electron temperature 

One of the main difficulties of p-[11] B fuel is that the bremsstrahlung radiation 

power is much higher than the fusion power produced by fuel ions of p-[11] B, as shown 

in figure 4, with equal ion and electron kinetic temperature 

![](images/tmpuvd0j4ve.pdf-0012-11.png)

To study the dependence of Lawson criterion on 𝑇"/𝑇W, we scan the 𝑇"/𝑇W ratio, 

and plot the minimum value of 𝑛"𝜏$ and the corresponding ion temperature to meet fusion gain Q=1 as figure 5(a) shows, which indicates when ld < 1.12, there are no lh 

positive values of 𝑛"𝜏$, and to obtain a fusion gain greater than 1, the ion temperature 

is at least 1.12 times the electron temperature. In the later paper, the value of 𝑇"/𝑇W is assumed to be 2.5 in order to get a higher gain fusion while the value of 𝑛"𝜏$ could be as low as possible. 

## III.C. The constraint of thermal wall loading 

The minimum value of 𝑛"𝜏$ meeting the Lawson criterion of p-[11] B fusion with 𝑇"/𝑇W =2.5 is 2.3×10['J] 𝑚[)*] 𝑠, which is still much higher than the current experiment parameters. To make a further study on the parameters of p-[11] B fusion devices, a higher confinement enhancement factor H is assumed, not limited by the IPB98y2 energy scaling. 

The p-[11] B fusion reactor may be not limited by neutron irradiation, but thermal loading due to the significantly high bremsstrahlung radiation power at the ion temperature of 300-500keV would restrict the regime of ion density. In this paper, we 

take the maximum value of the thermal wall loading caused by radiation as 10MW/m[2] , which is the maximum tolerable steady-state perpendicular power flux density onto the ITER divertor plate.[18] This wall-loading limit might further increase within the nearterm development of materials technology. 

If we assume all radiation power must be brought out through the first wall, we have the constraint of thermal wall loading 

![](images/tmpuvd0j4ve.pdf-0013-07.png)

where 𝜙P is the wall loading limit. The thermal wall loading is a function of the ion 

temperature, ion density and major radius, and for a given ion temperature, a larger major radius would restrict the increase of density. 

In figure 6, the magenta and blue line are the bremsstrahlung radiation power curve corresponding to wall loading limit with R0=2m and R0=3m, which is also a limit of ion density for a given ion temperature. The parabola describes the value of 𝑛"𝜏$ versus ion temperature satisfying fusion gain Q=1 while ld = 2.5, where the minimum lh value of 𝑛"𝜏$ = 2.3×10['J] 𝑚[)*] 𝑠 can be found at 𝑇" = 380𝑘𝑒𝑉. Since the fusion power density is directly related to the economic benefits, one approach to achieving 

economic benefits maximum is to operate at marginal ion density, which is shown by the circles in Figure 6. 

## III.D. The constraint of Beta 

A strong magnetic field is required to confine p-[11] B plasma with extremely high pressure, which might exceed the engineer constraints greatly. In this paper, the on- 

axis magnetic field is designed below 20T considering foreseeable development of technology. The normalized beta 𝛽q , which is related with economic benefits and plasma stability, is designed to be the maximum allowed for stability to confine the high-pressure p-[11] B plasma. 

To study the dependence of magnetic field on 𝛽q, we combine equation (13) and equation (14), and substitute the value ld = 2.5, \h = 1.4 derived before into it, and lh \d obtain the relation of plasma current, magnetic field and 𝛽q 

![](images/tmpuvd0j4ve.pdf-0014-07.png)

Recalling the safety factor limit 𝑞W\™ > 2, we have 

![](images/tmpuvd0j4ve.pdf-0015-01.png)

To minimize magnetic field at fixed fusion power density and tokamak geometry, ½ the normalized beta has been set to be the maximum 𝛽q~ .[4, 5] . In Table I 𝑛". = • 6×10['.] 𝑚[)*] , 𝑇". = 380𝑘𝑒𝑉 and 𝑅. = 3𝑚 is assumed, the minimum value of magnetic field needed in p-[11] B fuel is 10.7T for a low-aspect-ratio tokamak with A=1.4, while it turns out to be 23.2T for a conventional tokamak with A=2.4. 

## III.E. The size effects and H effects on fusion gain 

As discussed above, the optimal value of \b = ½ , ld = 2.5, 𝑇" = 380𝑘𝑒𝑉 have \c J lh 

been found, and two constraint conditions 𝜙P = 10𝑀𝑊𝑚[)'] 𝑎𝑛𝑑 𝛽q = 6.4 have been confirmed. 

To study the dependence of fusion gain on H and major radius R under the input 

and constraint condition, we plot the fusion gain Q versus major radius R at four different confinement cases H=1.5, H=3 and H=5 and H=10 while ion temperature, normalized beta and wall loading are fixed. Figure 7 indicates the fusion gain is strongly 

dependent on major radius and H, both of which have a positive effect on Q by increasing the energy confinement time. 

H=1.5 is the confinement enhancement factor that can be achieved by current experiments, and the minimum value of major radius which could meet Q=1 is 5m. In 

p-[11] B reactions, the core ion temperature could be higher than 300keV, in which the 

neo-classical transport decreases significantly. Once a new method has been found to effectively suppress the anomalous transport, the confinement enhancement factor of H=3, 5, 10 might be possible in the future. In any case, H=3 is an overly optimistic 

but still foreseeable confinement enhancement factor, and could reach Q=1.5 at R0=3m as shown in Figure 7. 

## III.F. The impurity effect 

In the preceding discussion, the helium concentration has been ignored. In an actual reactor, helium as a production of p-[11] B reaction, would decrease the fusion power output by diluting the fuel and increase bremsstrahlung radiation power, which would result in the termination of fusion reaction eventually. 

The number of helium ions could be obtained from the continuity equation 

![](images/tmpuvd0j4ve.pdf-0016-05.png)

where 𝑁XW is number of helium ions, 𝑁XW[ is the helium ion generation speed and ] 

𝜏XW is the helium confinement time. 

The helium ion generation speed is obtained by the fusion power 

![](images/tmpuvd0j4ve.pdf-0016-09.png)

And the core helium ion density is 

![](images/tmpuvd0j4ve.pdf-0016-11.png)

If we assume a breakeven case, 𝑛". = 6×10['.] 𝑚[)*] , 𝑇". = 38𝑜𝑘𝑒𝑉, 𝑃az{ = 5400𝑀𝑊 ∙𝑚[)*] , 𝜏$ = 5𝑠 and  𝜏XW = 10𝜏$ ≈50𝑠 , we could get 𝑛XW. = 9.5× 

10['.] 𝑚[)*] , even higher than the fuel ion density. Since the helium ash is poisonous to 

the fusion performance, excessive density of helium ions should be prevented. 

In figure 8, we plot Q versus the ratio of helium density to ion density at three 

different confinement cases H=3 and H=5 and H=10 while ion temperature, normalized beta and wall loading are set constant. The dependence of fusion gain on 𝑓XW is illustrated in figure 8, which indicates 𝑓XW does play an important role in fusion gain. At H=3 case, the highest ratio of 𝑓XW that the device could tolerate is 5%, which means 

the divertor ash removal efficiency should be high enough to keep the helium confinement time below energy confinement time. 

## III.G. The effect of synchrotron radiation loss 

In the previous discussion, all these optimistic predictions have been done without considering the synchrotron radiation loss, whose effect critical role can hardly be ignored in the relatively high strong magnetic field up to 10T. As one of the most important energy loss mechanisms, its effect has to be taken into consideration in the actual reactor, and in this section, we will discuss the effect of synchrotron radiation loss on p-[11] B fuel. 

The equation (30) gives the volume-integrated synchrotron radiation power loss, which is determined by averaged density, toroidal magnetic field on axis, effective electron temperature, wall reflectivity, effective minor radius and approximated plasma volume. The range of parameters such as electron temperature, electron density, toroidal magnetic field and the device size in p-[11] B tokamak have been already discussed in the previous section, hence one possible way to reduce the synchrotron 

power loss density is to increase the wall reflectivity high enough to reflect most of the radiation back and get re-absorbed in the core plasma. 

To give a better insight into the effect of the synchrotron radiation loss on p-[11] B fusion, the synchrotron radiation loss has been considered in the model predictions while other assumptions and constraints are still the same, and the helium concentration is set as 5%. The change of fusion gain and ratio of synchrotron radiation to bremsstrahlung radiation power loss in 3 different high-confinement cases H=5, H=10 and H=20 with wall reflectivity varied from 0.5 to 0.99 has been shown in figure 

9. 

In figure 9, the fusion gain of three high-confinement cases is even less than 0.5 with a low wall reflectivity of 0.5. When the wall reflectivity increases to 90%, the fusion gain of three high-confinement cases cannot meet the breakeven condition, and the synchrotron radiation power loss is slightly higher than the bremsstrahlung power loss. When the wall reflectivity is greater than 0.96, the breakeven condition can be obtained in the high confinement case of H=20. However, in this case the wall reflectivity and confinement enhancement factor are both unrealistically high for the existing technology. The results reveal that the fusion gain of p-[11] B fuel is strong affected by synchrotron radiation loss, and one of the biggest challenges to the p-[11] B fusion reactor is the reduction of synchrotron radiation loss. 

## III.H. The parameters of future device design 

In the actual reaction, helium, which is poisonous to fusion performance, and 

synchrotron radiation loss, which greatly decreases the fusion gain, should be taken into consideration. Based on the calculations of system code, five representative sets of p-[11] B tokamak device parameters which set helium concentration to 5% have been given in Table II. Among these sets, the wall reflectivity is assumed as 1 in set A to D, and in set E the wall reflectivity is assumed as 0.95 as a comparison. To keep the Helium concentration ratio in an acceptable range, the helium confinement time is assumed to be less than the energy confinement time, which also could be seen in Table II. 

A normal-aspect-ratio tokamak with A=2.5 in set A could be found, in which a high magnetic field of 36.8T is needed, indicating low-aspect-ratio tokamak would be a better choice for p-[11] B plasma with extremely high pressure. Besides, the plasmastored energy is much higher in the low-aspect-ratio tokamak from set B to D than that in set A with the same size of major radius. 

Three low-aspect-ratio tokamaks with A=1.4 from set B to set D are shown in Table II. Compared with Set B and Set C, when one increases the ratio fT from 2 to 2.5, the requirement for confinement condition is reduced to meet the breakeven condition. When one considers a hypothetical confinement enhancement factor H=10 in set D, fusion gain Q=4.14 could be obtained, which indicates a more optimistic confinement condition would bring a greater economic benefit. In set E, the effect of synchrotron radiation loss is considered by changing the wall reflectivity from 1 to 0.95, and the fusion gain is decreased from 4.14 to 0.84, which shows the synchrotron radiation loss would greatly decrease the fusion gain. 

## **IV. Conclusion and discussion** 

p-[11] B reaction is hard to meet Lawson criterion because of its low reactivity. However, if we choose the optimum proton-Boron mix and ion temperature, and assume the ratio of ion to electron temperature to be 2.5, the fusion power produced by fuel ions of p-[11] B can be comparable to heating power meeting Lawson criterion with Q=1. 

The helium is poisonous to the fusion performance by diluting the fuel and increasing bremsstrahlung radiation loss, and excessive density of helium ions would result in the termination of fusion reaction. In order to keep Helium concentration ratio in acceptable range, the technique of active ash removal is needed to develop in order to reduce the helium confinement time less than energy confinement time. 

Based on the calculation of tokamak system code, the fusion gain increases with the increasing major radius and confinement enhancement factor at fixed wall loading limit and beta limit. A major radius of 5m is needed to obtain fusion gain Q=1 with the current confinement condition of H=1.5 without helium concentration. After considering the helium concentration, if one can achieve a more optimistic confinement enhancement factor of H=10, the fusion gain of Q=4.14 at R0=3m could be found, which is of economic benefit. 

Although the ion temperature of above 300keV and energy confinement time of 10s required for p-[11] B reaction is not achievable by existing technologies, the main point of this paper is to study the requirements needed for p-[11] B fusion reactor, not to 

give engineering solutions to the requirements. In this point, this paper could achieve its aim if calls the colleagues’ attention to the p-[11] B fusion. 

Finally, we should bear in mind that all these optimistic assumptions have been done by neglecting the synchrotron radiation loss, which is relatively high in the strong magnetic field. If we consider synchrotron radiation loss and assume a high wall reflectivity of 95% in the calculations of the case H=10, the fusion gain would decrease from 4.14 to 0.84. The results shows the p-[11] B fusion reactor will not come true unless some techniques have been found in the future to avoid excessive synchrotron radiation loss. 

## **Acknowledgement** 

This work is supported by the China central government which guides the development of local science and technology funding No. 206Z4501G and the Compact Fusion Project of the ENN group. 

## **References** 

- [1] R. Reid et al. "Tokamak systems code": Oak Ridge National Lab., TN (USA) 1985. 

- [2] W. Barr et al. "ETR/ITER systems code": Oak Ridge National Lab., TN (USA) 1988. 

- [3] R. D. Stambaugh et al.,"The Spherical Tokamak Path to Fusion Power," _Fusion_ 

_Technology_ , **33** , 1-21 (1998) 

- [4] R. D. Stambaugh et al.,"Fusion Nuclear Science Facility Candidates," _Fusion Science and Technology_ , **59** , 279-307 (2011) 

- [5] A. E. Costley, J. Hugill and P. F. Buxton,"On the power and size of tokamak fusion pilot plants and reactors," _Nuclear Fusion_ , **55** , 033001 (2015) 

- [6] C. C. Petty et al.,"Feasibility study of a compact ignition tokamak based upon gyrobohm scaling physics," _Fusion science and technology_ , **43** , 1-17 (2003) 

- [7] W. M. Nevins,"A review of confinement requirements for advanced fuels," _Journal of Fusion Energy_ , **17** , 25-32 (1998) 

- [8] M. Sikora and H. Weller,"A New Evaluation of the 11B(p, α)αα Reaction Rates," _Journal of Fusion Energy_ , **35** , 538-543 (2016) 

- [9] T. Luce et al.,"Generation of localized noninductive current by electron cyclotron waves on the DIII-D tokamak," _Physical review letters_ , **83** , 4550 (1999) 

- [10] M. Andrade and G. Ludwig,"Scaling of bootstrap current on equilibrium and plasma profile parameters in tokamak plasmas," _Plasma Physics and Controlled Fusion_ , **50** , 065001 (2008) 

- [11] R. Svensson,"Electron-positron pair equilibria in relativistic plasmas," _The Astrophysical Journal_ , **258** , 335 (1982) 

- [12] S. Putvinski, D. Ryutov and P. Yushmanov,"Fusion reactivity of the pB11 plasma revisited," _Nuclear Fusion_ , **59** , 076018 (2019) 

- [13] D. C. Moreau,"Potentiality of the proton-boron fuel for controlled thermonuclear fusion," _Nuclear Fusion_ , **17** , 13 (1977) 

- [14] A. Kukushkin and V. Kogan,"Relativistic boron-hydrogen plasma as a fusion fuel," _Soviet Journal of Plasma Physics_ , **5** , 708-711 (1979) 

- [15] A. Kukushkin and P. Minashin,"Generalization of Trubnikov formula for electron cyclotron total power loss in tokamak-reactors", _XXXVI International_ 

   - _Conference On Plasma Physics And CF, Zvenigorod_ ( _2009)_ 

- [16] A. Kukushkin, P. Minashin and V. Neverov "Electron cyclotron power losses in fusion reactor-grade tokamaks: Scaling laws for spatial profile and total power loss," _Proc. 22nd IAEA Fusion Energy Conference, Geneva, Switzerland_ : Citeseer 2008. 

- [17] ITER Physics Expert Group on Confinement and Transport et al. "Plasma confinement and transport," _Nuclear Fusion_ , **39** , 2175-2249 (1999) 

- [18] R. Pitts et al.,"Status and physics basis of the ITER divertor," _Physica Scripta_ **2009** , 014001 (2009) 

![](images/tmpuvd0j4ve.pdf-0024-00.png)

**Fig. 1.** The left figure is the sketch of a low -aspect -ratio tokamak geometry (a), and the right 

figure is a broader profile of density (b) and a steeper profile of temperature (c). In this paper, 

Sn=0.5 and ST=1.5. 

![](images/tmpuvd0j4ve.pdf-0025-00.png)

![](images/tmpuvd0j4ve.pdf-0025-01.png)

**Fig. 2.** Upper panel (a) is ~~𝑛~~ Ó 𝜏$ versus volume averaged ion temperature 𝑇Ó which meet Lawson criterion for D-T, D-[3] He, D-D and p-[11] B reactions with Q=1 in the 0- 

dimensional model. Lower panel (b) is  𝑛".𝜏$ versus core ion temperature 𝑇". which meet Lawson criterion for D-T, D-[3] He, D-D and p-[11] B reactions with Q=1 in the 1- 

dimensional model. In both models, 𝑇" = 𝑇W for D-T, D-[3] He and D-D reactions. As for 

p-[11] B reaction, \b = 9 and ld = 1 in 0-dimensional model, while \b = 9 and ld = \c lh \c lh 

1.2 in 1-dimensional model. 

![](images/tmpuvd0j4ve.pdf-0026-00.png)

**Fig. 3.** The logic diagram of requirements for p-[11] B fusion reactor. 

![](images/tmpuvd0j4ve.pdf-0027-00.png)

**Fig. 4.** The color map of ……œ±h †‡ˆ versus 𝑇" and 𝑓HU for the constant 𝑓l = 1. To maximize output of fusion power, the optimal value of \b is chosen as 9. \c 

![](images/tmpuvd0j4ve.pdf-0028-00.png)

![](images/tmpuvd0j4ve.pdf-0028-01.png)

**Fig. 5.** The upper figure (a) is the minimum value of ~~𝑛~~ Ó𝜏$ which meets Lawson criterion 

and the corresponding volume averaged ion temperature 𝑇Ó versus 𝑇"/𝑇W in zero-dimensional 

model and in one-dimensional model. When 𝑇"/𝑇W<1.12, no positive solution that meet Lawson 

criterion with Q=1 can be found. The lower figure (b) is the minimum value of  𝑛".𝜏$ which meets 

Lawson criterion and the corresponding core ion temperature 𝑇". versus 𝑇"/𝑇W in one- 

dimensional model. 

![](images/tmpuvd0j4ve.pdf-0029-00.png)

**Fig. 6.** The left Y axis shows the ion density versus ion temperature for bremsstrahlung 

radiation power density limit, and the right Y axis shows 𝑛"𝜏$ versus ion temperature meeting 

Lawson criterion with Q=1. The magenta and blue line is the wall loading limit by radiation when 

R=2m and R=3m, and the circles intersected by optimum temperature of 𝑇" = 380𝑘𝑒𝑉 and the 

curve of bremsstrahlung radiation power limit indicate the marginal ion density. 

![](images/tmpuvd0j4ve.pdf-0030-00.png)

**Fig. 7.** Fusion gain Q versus major radius R at four different confinement cases H=1.5, H=3, 

H=5 and H=10. 

![](images/tmpuvd0j4ve.pdf-0031-00.png)

**Fig. 8.** Fusion gain Q versus the ratio of helium density to ion density at three different 

confinement cases H=3, H=5 and H=10. 

![](images/tmpuvd0j4ve.pdf-0032-00.png)

**Fig. 9.** Fusion gain (left y-axis) and the ratio of synchrotron radiation to bremsstrahlung radiation 

power loss (right y-axis) versus wall reflectivity at three different confinement cases H=5, H=10 and 

H=20. 

**TABLE I** . The aspect ratio versus the minimum value of magnetic field required for 

confining p-[11] B plasma and the corresponding plasma current. 

|A|1.4|1.9|2.4|
|---|---|---|---|
|Bt0,min(T)|10.7|17.3|23.2|
|Ip (MA)|147|91.2|68.2|

**TABLE II.** Five typical sets of p-[11] B tokamak device parameter based on tokamak 

system code. 

|**Parameters**|**Set A**|**Set B**|**Set C**|**Set D**|**Set E**|
|---|---|---|---|---|---|
|**A**|2.5|1.4|1.4|1.4|1.4|
|𝐟𝐓(**Ti/Te)**|2.5|2|2.5|2.5|2.5|
|**H**|3|5|3|10|10|
|**fHe**|0.05|0.05|0.05|0.05|0.05|
|𝛈𝐰|1|1|1|1|0.95|
|**R0(m)**|3|3|3|3|3|
|**a(m)**|1.2|2.14|2.14|2.14|2.14|
|**Vp(m3)**|185|919|919|919|919|
|**Sw(m2)**|233.3|548|548|548|548|
|𝜿|2.24|3.57|3.57|3.57|3.57|
|𝜹|0.5|0.5|0.5|0.5|0.5|
|**Q**|0.8|1.17|1.06|4.14|0.84|
|**Pfus(MW)**|2311|4424|5427|5427|5427|
|**Paux(MW)**|2878|3771|5316|1311|6426|
|**Pcd(MW)**|576|754|1063|262|1292|
|**Pbrem(MW)**|2333|5480|5480|5480|5480|
|**Pcycl(MW)**|0|0|0|0|4762|
|𝝓𝒘**(MW/m2) **|10|10|10|10|10|
|**Bt0(T)**|36.8|11.3|11.4|12.9|11|
|**Ip(MA)**|63|140|140|124|145|
|**Wdia(MJ)**|7685|25864|26256|26256|26256|
|**fbs**|0.77|0.72|0.72|0.92|0.67|
|**Zeff**|2.4|2.4|2.4|2.4|2.4|
|**Te0(keV)**|152|190|152|152|152|
|**Ti0(keV)**|380|380|380|380|380|
|**ne0(1020m-3)**|12.4|7.72|8.55|8.55|8.55|
|**ni0(1020m-3)**|8.70|5.40|5.98|5.98|5.98|
|𝛕𝐄**(s)**|2.69|9.52|4.88|20.8|15.9|
|𝛕𝐇𝐞**(s)**|1.08|1.73|1.57|1.57|1.57|
|𝛃𝐓 **(%)**|5.12|36.7|36.8|28.8|39.5|
|𝛃𝐩|1.90|1.9|1.9|2.4|1.8|
|𝛃𝐍|3.6|6.4|6.4|6.4|6.4|

| **q**eng | 3.14 | 2.22 | 2.2 | 2.8 | 2.06 |
|---|---|---|---|---|---|