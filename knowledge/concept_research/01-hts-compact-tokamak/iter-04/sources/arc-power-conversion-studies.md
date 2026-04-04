---
source: "ssrn-4482183.pdf"
source_type: "local_file"
extracted_at: "2026-03-29T16:28:47.400248+00:00"
content_hash_sha256: "df5a9c2059745fe8d0c92ee130a9d8f4b77c7d03717f8a554ed1d0053192c1ac"
backend: "pdf_pipeline"
---

**Analysis of different Power Conversion System options for ARC fusion reactor Balance of Plant**

Francesco Colliva [1 ] **,** Cristiano Ciurluini [1], Andrea Iaboni [2], Giulia Valeria Centomani [2], Antonio Trotta [2], Fabio Giannetti [1*]

_1 Sapienza University of Rome, DIAEE – Nuclear Section, Corso Vittorio Emanuele II 244, 00186 Rome, Italy_

_2 MAFE, Eni S.p.A., Venezia 30175, Italy_

*Corresponding authors
E-mail address: fabio.giannetti@uniroma1.it

Abstract

In these last years, fusion energy has assumed an important role in the energy scenario, being an environmentally friendly

and practically inexhaustible energy source. One of the studied reactors is ARC, a tokamak fusion device characterized

by a compact and high-field design initially conceived by researches at the Massachusetts Institute of Technology, which

Commonwealth Fusion System (CFS) plans to construct in the next decade. This paper is focused on the analysis and

development of different configurations for the ARC Balance of Plant Power Conversion System. Three cycles have been

studied, by using the General Electric GateCycle [TM] software: a supercritical steam Rankine cycle, a supercritical CO2

Brayton cycle and a supercritical helium Brayton cycle. The thermal efficiency of the three options has been compared

to select the most promising solution. The results show that the supercritical steam cycle is the best configuration in terms

of cycle efficiency for the ARC FNSF Pilot phase.

Keywords: PCS, BoP, Supercritical CO2, Supercritical He, Supercritical steam, GateCycle [TM] .

1. Introduction

Fusion has assumed an important role in last years, being one of the options able to guarantee a large scale,

environmentally friendly and practically inexhaustible energy source [1]. To increase the economic competitiveness of

fusion power plants, different strategies are currently being studied. Among the other, one possible solution is reducing

the reactor size in order to reduce material and in general, plant capital costs, [2]. In view of this objective, an Affordable

Robust and Compact (ARC) reactor has been proposed at Massachusetts Institute of Technology (MIT) and is under

development by Commonwealth Fusion System (CFS). ARC is a tokamak fusion reactor for the study of both energy

generation and the effects of high-magnetic technologies in a reduced size structure, obtained by using high-temperature

superconductor magnets [2]. One of the main goals of ARC project is obtaining a cheap source of energy, and this

necessarily requires the optimization of the Power Conversion System (PCS). Further analyses on ARC PCS are already

available in [3]. For this reactor, the use of a molten salt liquid blanket is envisaged. One of the eligible fluids for the

primary cooling system is FLiBe, a mixture of lithium fluoride (LiF) and beryllium fluoride (BeF2). Within the blanket,

the molten salt interacts with neutrons coming from the plasma and converts their kinetic energy into heat. Later, it delivers the removed thermal power to the ARC PCS. Because of the pulsed operation of the reactor, which alternates pulse and dwell phases, one of the proposed solutions foresees the presence of an intermediate circuit containing molten salts and equipped with an Energy Storage System (ESS). A storage system is therefore required, to ensure a constant load operation for the turbine even during the dwell phase, avoiding mechanical stresses and its disconnection from the grid. The available power during the pulse is split into two contributions: most of it is delivered to PCS in order to supply the grid, while the remaining part is stored in the ESS and released to the PCS during the dwell time [4]. The presence of the ESS affects the initial cost of the plant, because of the additional circuit and the molten salt inventory. In the ARC reactor R&D program, three different stages are foreseen, depending on the blanket outlet temperature: a "Fusion Nuclear Science Facility" (FNSF) phase, a "Conservative Pilot phase" and an "Aggressive Pilot" phase, where molten salt comes out from the blanket at 900 K, 1100 K and 1200 K respectively [2]. These three phases envisage the test of materials resistance under irradiation in different operative conditions. In this work, only FNSF phase has been considered. Three different thermodynamic cycles for the ARC Balance of Plant (BoP) have been studied: a supercritical Rankine cycle and two Brayton cycles. The others are characterized by CO₂ and helium (He) as working fluids, respectively. These three options are typically considered for fusion power plants, [5] and [6], as advanced options for high-temperature primary coolants, in addition to the traditional Rankine cycles used in water-cooled concepts [7], inspired by the typical PWR fission power plant. The supercritical steam cycle has been studied because its technology is well developed and widely applied in many energy applications, while CO₂ and He have been chosen for their promising features, such as the possibility to work at lower pressure and without phase change, also enabling more compact solutions. To study the cycle performances General Electric's GateCycle™ software has been used, [8]. This numerical tool is largely used for the design of thermal power plants and the simulation of design and off-design conditions. It simulates the behavior of a cycle through the definition of its configuration and of the conditions of the chosen fluid at different points of the layout. Through GateCycle™ the performances of the three cycles are evaluated and compared, in order to find the most promising configuration to be used for the ARC's BoP.

## 2. Investigated BoP configurations

For each of configuration analyzed, the input data to be used in GateCycle™ are obtained by performing a preliminary energy balance, referring to pre-existing cycles. The configuration scheme for the three cycles is presented in the following subsections. In all cases, the ARC reactor pulse phase has been considered as the reference scenario. The reactor thermal power produced in this scenario and delivered to the PCS by the intermediate circuit is 645 MW$_{\text{th}}$. This value is obtained through an energy balance, performed considering data provided in [9]. In addition, in the present work, the

intermediate circuit has been included in view of the ESS, whose presence is not considered in the analysis discussed in [9]. The conditions of the intermediate fluid exchanging power with the secondary fluid through the secondary Heat Exchanger (HX) are derived from [10] and are listed in Table 1. They have been postulated according to engineering judgment and experience in order to obtain enough BoP efficiency and to avoid excessive thermal stresses in the primary and secondary heat exchangers (due to the high-temperature differences between the primary and secondary sides of the components).

| Parameter | Value |
|-----------|-------|
| Inlet SG Intermediate Temperature (°C) | 565 |
| Outlet SG Intermediate Temperature (°C) | 505 |
| Intermediate Mass Flow Rate (kg/s) | 1500 |

*Table 1 – Intermediate FLiBe conditions*

## 2.1. Rankine cycle

The first cycle investigated is the supercritical Rankine cycle, chosen because of the advanced studies on the technology of its components. An energy balance has been performed on the preliminary scheme presented in Figure 1 and based on the cycle reported in [10]. The thermal power coming from the intermediate circuit is exchanged through the secondary steam generator, which allows the secondary feedwater entering at 320 °C to become supercritical steam at 540 °C, at a pressure of 250 bar. This is done with a feedwater flow rate of 344 kg/s that circulates into the steam generator. As stated above, the feedwater inlet and steam outlet conditions were preliminary selected to optimize the cycle efficiency while avoiding excessive thermomechanical stresses in the secondary heat exchanger. The thermal power is converted into electricity that must be supplied to the grid through a turbogenerator system constituted by three groups of turbines of high, medium and low pressure (HP, IP, LP). These units are divided into two, two and four separate turbine components, respectively (keeping a single extraction for each turbine). The high-pressure turbine is designed to work with a steam bleed driven to the second to last element of the feedwater preheater train (PH5, see Figure 1). A reheater (RH) is expected to regenerate the steam leaving the HP turbine. This operation is accomplished by using part of the steam directly leaving the secondary steam generator (SG). Once flowed the RH shell-side, such fluid is sent to preheat the feedwater (PH6). The regenerated steam exiting from the reheater is sent to the intermediate-pressure turbine group, characterized by two extractions. The first one is directed to the PH4, and the other one to the Deaerator (DEA). From the intermediate pressure turbine group, the steam is then received by the low-pressure turbine group, whose extractions preheat feedwater in the first three elements of the feedwater preheater train. The two-phase mixture from the low-pressure turbine is sent to the Condenser (COND). From here, the secondary water is drawn from the Extraction Pump (EP) and sent to the preheating line. The latter is made up of six preheaters, separated by the deaerator into two groups of three, respectively of high and

low pressure. The deaerator is meant to remove the non-condensable gases from the feedwater through the steam received

from one of the intermediate pressure turbine extractions. At its outlet, the Primary Pump (PP) increases the water pressure

up to the rated value set for the SG inlet (see above). For each preheater, the water flowing out of the component shell is

mixed with the feedwater coming from the previous preheater, by using a pump or a valve depending on whether an

increase or a reduction in pressure is required, respectively. The water exiting from the PH4 shell side is sent to a valve

that vaporizes it. This steam is then sent to the DEA where, with the steam coming from the intermediate extraction, it is

used to remove the non-condensable gases. After the usage, this steam flow is discharged from the deaerator, to be then

reintegrated.

_Figure 1 - Scheme proposed for ARC’s supercritical Rankine cycle._

2.2. CO2 Brayton cycle

The CO2 Brayton cycle is the second cycle analyzed, reported in Figure 2. Some assumptions are made: a precooler is

adopted to perform the compression near the critical point, where the fluid is characterized by a lower specific volume,

bringing to a reduction of the compression work; an auxiliary compressor is used to reduce problems due to the difference

of CO2 specific volumes between high and low pressure; regeneration is foreseen, divided into two phases of low and

high temperatures, to avoid the excessive difference of specific heat that, in case of a single HX, would occur between

fluid streams flowing along tube and shell sides; reheating is carried out after a first turbine expansion to further increase

the efficiency. The CO2 flux which must be compressed is divided into two branches, see Figure 2. The former is cooled

by a Precooler (PRC) and then is sent to the Main Compressor (C1). Instead, the second gas stream is sent to the Auxiliary

Compressor (C2). The flow elaborated by the main compressor is then driven to the tube side of a Low-Temperature

Regenerator (LTR). Once exited, such flow is mixed with the one coming from C2 and finally drawn to the High

Temperature Regenerator (HTR). In this configuration, the thermal power coming from the intermediate circuit is

![](images/ssrn-4482183.pdf-3-0.png)

exchanged through two passages into the secondary HX (shown as SHX in Figure 2). The first passage occurs after the

CO2 preheating in the HTR, and it is followed by the gas expansion into the High-Pressure Turbine (T1). The flow is then

reheated with a second passage into the SHX and expands in a Low-Pressure Turbine (T2). Finally, the exiting flow is

driven to the shell side of the HTR and LTR to provide the needed heat to preheat the flow coming from the compression

zone. For what concerns the choice of temperatures and pressures in the preliminary balance, reference is made to a

configuration studied for the DEMO facility [12]. For the evaluation of the required CO2 mass flow rate, the inlet and

outlet conditions of the two passages in the SHX have been imposed, and an energy balance has been performed.

_Figure 2 - Scheme proposed for ARC’s supercritical CO2 Brayton cycle._

2.3. He Brayton Cycle

The last analyzed cycle is the supercritical helium Brayton cycle. Studies in literature are limited, since this technology

is not yet very well developed at an industrial scale. The investigated cycle scheme, reported in Figure 3, is inspired by a

supercritical He cycle configuration analyzed for the Indonesian reactor RGTT200K, developed by BATAN [13]. The

adopted scheme is characterized by an inter-cooling stage and a recuperator, which provides a significant efficiency

enhancement but requires a higher system complexity and, consequently, higher costs. The Intercooler (ITC) divides the

compression into two consecutive phases and, together with a Precooler (PRC), it reduces the specific volume of the gas,

bringing a reduction of the required compression work. The supercritical helium flows through the Secondary HX (shown

as SHX in Figure 3) and, once heated up, it is sent to the Turbine (T1). The fluid is expanded and then sent to a Regenerator

(REG, shell-side) where preheats the fluid exiting from the compression zone. The fluid is then drawn to the PRC, which

cools it, and to a series of two compressors (C1 and C2). They are separated by the ITC, which refrigerates the fluid

exiting from C1 and heading to C2. Finally, the fluid coming from C2 is sent to the regenerator and then to the SHX

(Figure 3).

![](images/ssrn-4482183.pdf-4-0.png)

![](images/ssrn-4482183.pdf-5-0.png)

_Figure 3 - Scheme proposed for ARC’s supercritical He Brayton cycle._

3. Simulation Activity

3.1. Numerical model

In the following paragraphs, the simulation results obtained with GateCycle [TM] software, [8], are reported. For calculation

purposes, the numerical models presented so far and corresponding to the preliminary cycles have been used. First

tentative pressure and temperature fields have been obtained for the configurations presented in Figure 1, Figure 2 and

Figure 3 by performing the energy balance in some selected points of the scheme. The obtained data have been used as

input values for the GateCycle [TM] code. Starting from them, the software makes several iterations until the layout

converges to the final pressure, temperature, and mass flow values. To perform the simulations, some initial assumptions

have been made. GateCycle [TM] does not include the molten salt as operating fluid. For this reason, in the primary side of

the secondary HX the molten salt has been substituted by steam or gas at conditions necessary to exchange the required

power. In addition, in these preliminary cycle analyses, pressure drops in pipelines have been neglected. For each

component, there is the possibility to select “design mode” or “off design mode”. With the first option, the components

are designed ex novo and their input parameters are chosen by the user, while in the second one the design of components

is imported from a previous case, [8]. In the current work, all components are set in “design mode”.

3.2. Rankine cycle

The analysis of the Rankine cycle scheme (presented in Figure 1) as implemented in GateCycle [TM], obtaining the model

reported in Figure 4, is here reported. In Table 2 the main input values considered in GateCycle [TM] are shown. The inlet

and outlet steam generator temperatures have been set referring to [10], while the others were assumed based on

engineering judgment and experience. For steam thermodynamic properties GateCycle [TM] uses IAPWS-IF97

formulations, [14]. In addition, some approximations have been done. The secondary HX (shown as HX1 in Figure 4)

has been simulated with a pure countercurrent flow HX, that exchanges the required power from the intermediate to the

secondary circuit. The HP, IP and LP steam turbines are divided into two, two and four separate stages, and extractions

have been placed at the end of each stage. This procedure has been suggested by GateCycle [TM] manual, in order to obtain

a faster convergence of the simulation. IP and LP turbines are modeled with the Spencer Cotton Cannon (SCC) method

[15], while the HP turbine efficiency is assumed equal to 0.9. The latter happens because the SCC method is not intended

for supercritical applications. The pressures of each extraction are optimized and fixed (see Table 3). In Table 3 each

extraction is accompanied by the name of the corresponding stream, as shown in Figure 4. Pumps are modeled setting the

output pressure values of the flow, assuming an input efficiency of 0.85. The GateCycle [TM] calculation, once convergence

is achieved, allowed the cycle optimization. Table 4 reports the power required by the pumps and the power produced by

turbines, while Table 5 summarizes the loads of the different HXs. It is possible to calculate the efficiency of the cycle in

the conversion of thermal energy into electricity. According to indications provided in [16], two different powers can be

calculated and used as relevant figures of merit to evaluate the cycle performances: the gross power and the net electric

power. Their formulas are reported below.

𝑊𝑔𝑟𝑜𝑠𝑠 = 𝜂𝑔𝑒𝑛

𝑊𝑒 = 𝑊𝑔𝑟𝑜𝑠𝑠 

(1)
𝑖 [𝑊][𝑡,𝑖]

(2)
𝑖 [𝑊][𝑝𝑢𝑚𝑝,𝑖]

![](images/page_006_eq_0.png)

where 𝜂𝑔𝑒𝑛 represents the generator efficiency (assumed equals to 0.985 ), while 𝑊𝑡,𝑖 represents the power extracted from

![](images/page_006_eq_1.png)

the different turbines of high, medium and low pressure and 𝑊𝑝𝑢𝑚𝑝,𝑖 the power absorbed by the pumps. From these

powers, it is possible to evaluate the corresponding efficiencies, as shown in the following.

(3)

(4)

𝜂𝑔𝑟𝑜𝑠𝑠 =

![](images/page_006_eq_2.png)

𝑊𝑔𝑟𝑜𝑠𝑠
𝑄𝑟𝑒𝑎𝑐𝑡𝑜𝑟

![](images/page_006_eq_3.png)

𝜂𝑒 =

𝑊𝑒
𝑄𝑟𝑒𝑎𝑐𝑡𝑜𝑟

In Table 6 are reported the final values of PCS power and efficiency obtained through the simulation. Values evaluated

are overestimated, because referred only to the PCS without considering the power required by other auxiliary systems.

In Table 6, the efficiencies values for HP, IP and LP turbines are evaluated as mean values of the components’ efficiency

of each of the three chains.

[Figure 4: GateCycle™ model of proposed ARC's supercritical Rankine Cycle]

*Table 2 – GateCycle™ input data for supercritical Rankine Cycle.*

| Parameter | Value |
|---|---|
| Inlet SG Temperature (°C) | 320 |
| Outlet SG Temperature (°C) | 540 |
| Outlet SG Pressure (bar) | 250 |
| Condenser Pressure (bar) | 0.045 |
| Extraction Pump Pressure (bar) | 5 |
| Primary Pump Pressure (bar) | 250 |
| Mass Flow Rate (kg/s) | 344 |

*Table 3 – Extraction pressure values.*

| Parameter | Value |
|---|---|
| EX1 pressure (S19) (bar) | 1.5 |
| EX2 pressure (S46) (bar) | 2.2 |
| EX3 pressure (S47) (bar) | 4.3 |
| EX4 pressure (S18) (bar) | 6 |
| EX5 pressure (S41) (bar) | 7.5 |
| EX6 pressure (S4) (bar) | 100 |

*Table 4 – Auxiliary pumping powers and turbine powers.*

| Parameter | Power |
|---|---|
| Extraction pump (MW) | 0.1 |
| Primary pump (MW) | 6.7 |
| Pump 1 (MW) | 0.007 |
| Pump 4 (MW) | 0.006 |
| Pump 5 (MW) | 1.9 |
| Pump 6 (MW) | 1.4 |
| **Total consumption (MW)** | **10.1** |
| HP turbine (MW) | 80.4 |
| IP turbine (MW) | 120.6 |
| LP turbine (MW) | 104.8 |
| **Total production (MW)** | **311.8** |

| Heat exchanger | Power |
|---|---|
| Condenser (MW) | 329.4 |
| PHEX1 (MW) | 55.4 |

| PIX2 (MW) | 7.9 |
| PIX3 (MW) | 17.9 |
| PIX4 (MW) | 6.2 |
| PIX5 (MW) | 123.9 |
| PIX6 (MW) | 17.5 |
| RH (MW) | 93.6 |

*Table 5 – Heat exchangers loads*

| Parameter | Value |
|---|---|
| Gross power (MW) | 367.1 |
| Net electric power (MW) | 297 |
| Isentropic efficiency (HP turbine) | 87.4% |
| Isentropic efficiency (IP turbine) | 86.9% |
| Isentropic efficiency (LP turbine) | 85% |
| Gross efficiency | 47.6% |
| **Net efficiency** | **46%** |

*Table 6 – PCN power and efficiency*

## 3.3. CO₂ Brayton cycle

![](images/page_008_eq_0.png)
The scheme in Figure 5 represents the implementation in GateCycle™ of the cycle presented in Figure 2. As for the first cycle, Table 7 reported the input values for GateCycle™. In this configuration, the heat exchangers HX4 and HX5 model the double passage of the secondary heat exchanger, and the molten salt which should feed their primary sides is simulated with equivalent gas conditions, as already discussed in section 3.1. As regards the repartition of mass flow between the two compressors C1 and C2, it has been assumed that nearly the 80% of CO₂ is sent to the main compressor, while the remaining part to the auxiliary one. This distribution influences the power exchanged by HX4 and HX5 (see Figure 5), and optimizes the exchange efficiency, by obtaining a constant temperature difference through the LTR. The exact values are computed by the code to exchange the rated thermal power (645 MW_th) coming from the intermediate circuit. The pre-cooler HX1 uses water as cooling fluid. Compressors C1 and C2 are modelled with an efficiency equal to 0.9, setting the desired outlet pressure. The efficiencies which characterize the turbines EX1 and EX2 are reported in Table 10. For supercritical CO₂ thermodynamic properties, GateCycle™ refers to NASA thermodynamic data [8]; presented in [16]–[19]. Results are presented in Table 8 and Table 9. The former contains the power required by compressors and produced by turbines, while the latter provides the loads characterizing the heat exchangers in operating conditions. In this case, the formula of the net electric power reported in section 3.2 must be modified, obtaining the new expression given below.

$$W_e = \eta_{gen} \left( \sum W_{t,i} + \sum W_{c,i} \right) \tag{5}$$

where $\eta_{gen}$ is the generator efficiency, assumed equal to 0.985, and $W_{t,i}$ and $W_{c,i}$ are the powers extracted from the turbine and absorbed by compressors, respectively. From these two parameters it is possible to evaluate the corresponding efficiencies, using the same formulas presented in section 3.2. All the parameters' values are reported in Table 10.

[Figure 5: GateCycle™ model of proposed ARC's supercritical CO₂ Brayton cycle]

**Parameter** | **Value**
---|---
Inlet EX1 Temperature (°C) | 455
Outlet EX1 Pressure (bar) | 128
Inlet EX2 Temperature (°C) | 455
Outlet EX2 Pressure (bar) | 85.8
Inlet C1 Pressure (bar) | 30
Outlet C2 Pressure (bar) | 281.6
Outlet C2 Pressure (bar) | 281.2
Mass Flow Rate (kg/s) | 2014

*Table 5 – GateCycle™ input data for supercritical CO₂ Brayton cycle*

| **Parameter** | **Power** |
|---|---|
| C1 compressor (MW) | 56.1 |
| C2 compressor (MW) | 39.4 |
| **Total consumption (MW)** | **95.5** |
| EX1 turbine (MW) | 235.7 |
| EX2 turbine (MW) | 123.7 |
| **Total production (MW)** | **359.4** |

*Table 8 – Compressor and turbine powers*

| **Heat exchanger** | **Power** |
|---|---|
| HX1 (MW) | 377 |
| HX2 (MW) | 410.9 |
| HX3 (MW) | 561.3 |
| HX4 (MW) | 371.1 |
| HX5 (MW) | 273.9 |

*Table 9 – Heat exchangers loads*

| **Parameter** | **Value** |
|---|---|
| Gross power (MW) | 354 |
| Net electric power (MW) | 259.9 |
| Isentropic efficiency (EX1 turbine) | 90% |
| Isentropic efficiency (EX2 turbine) | 92% |
| Gross efficiency | 54.9% |
| **Net efficiency** | **40.3%** |

*Table 10 – PCS power and efficiency*

## 3.4. He Brayton cycle

The GateCycle™ scheme for the supercritical He cycle is reported in Figure 6, and the input data needed for this model are presented in Table 11. As for the CO₂ configuration, for supercritical He properties GateCycle™ refers to NASA thermodynamic data.[16]-[19]. Similarly to the model adopted for the supercritical CO₂ cycle, also in this case the heat exchanger IHX simulating the secondary heat exchanger uses gas as a substitute for the intermediate FLiBe molten salt. Gas conditions are selected to allow the transfer of required power. Intercooling (ITC) and precooling (PRC) heat exchangers are instead modeled with two dedicated components using water to bring helium to the desired conditions (see Table 11). The turbine EX1 and the compressors C1 and C2 are modeled with an efficiency of 0.9 and with a fixed value of outlet pressure equal to 23 bar for the turbine, and with efficiencies of 0.9 and outlet pressures of 35 bar and 30 bar for the two compressors, respectively. The cycle mass flow rate has been calculated by performing the energy balance at the IXH shell side and considering the rated thermal power (645 MW$_{th}$) and the imposed fluid thermodynamic conditions. The resulting value for the PCS mass flow is of 569 kg/s. Such value was used as input data for the GateCycle™ calculation.

Table 12 and Table 13 collect the main simulation results, in terms of power produced and absorbed (the former) and heat exchanger loads (the latter). As for the case shown in section 3.3, it is possible to evaluate the gross and net powers and, from these, the corresponding efficiencies, reported in Table 14.

[Figure 6: *GateCycle™ model of proposed ARC's supercritical He cycle.*]

| Parameter | Value |
|---|---|
| Outlet IHX Temperature (°C) | 550 |
| Outlet EX1 Pressure (bar) | 23 |
| Outlet PRC Temperature (°C) | 40 |
| Outlet C1 Pressure (bar) | 35 |
| Outlet ITC Temperature (°C) | 40 |

Outlet C2 Pressure (bar) 50
Mass Flow Rate (kg/s) 569
_Table 11 - GateCycle™ input data for supercritical Helium Brayton cycle._

**Parameter** **Power**
C1 compressor (MW) 199.96
C2 compressor (MW) 166.28
**Total consumption (MW)** **366.24**
EX1 turbine (MW) 576.95
**Total production (MW)** **576.95**
_Table 12 – Compressor and turbine powers._

**Heat exchanger** **Power**
ITC (MW) 198.7
PRC (MW) 233.3
_Table 13 – Heat exchangers loads._

**Parameter** **Value**
Gross power (MW) 568.3
Net electric power (MW) 207.5
Isentropic efficiency (EX1 turbine) 0.95
Gross efficiency 88%
**Net efficiency** **32%**
_Table 14 – PCS power and efficiency._

3.5. Result discussion

In this paragraph, the simulation results are discussed evaluating the most affordable configuration from the point of view

of net electric efficiency. The three options are compared in terms of: efficiency, mass flow rate, and maximum pressure

that characterizes each cycle. Their values are summarized in Table 15. Thanks to the adoption of regeneration and

preheating phases, the Rankine cycle results to be the one with the higher net efficiency, but also the one with the highest

pressure difference. This results in higher pressure drops within the circuit, which have not been considered in this

analysis, and higher mechanical stresses on components. The Rankine cycle is also characterized by a significant number

of extractions, which results in a more complex configuration with respect to the Brayton ones. From the temperatures

point of view, the supercritical steam cycle is the one that reaches higher temperatures (540°C), followed by the helium

cycle (530°C) and CO2 cycle (about 450°C), and also the higher difference temperature. This results in higher thermal

stresses for the first configuration, but allows the achievement of higher efficiencies. Comparing values for the three cases

presented in Table 6, Table 10, and Table 14, the supercritical steam cycle resulted as the one with the smaller difference

between gross and net powers, because of the lower power required from pumps on this configuration with respect to the

power required by compressors of Brayton cycles. In addition, it is worth to be noted that the analysis performed has not

considered the presence of auxiliary systems, which reduce the net power actually obtained from the cycles. However,

the present study has shown how, despite of problems such as layout complexity and thermo-mechanical stresses, the supercritical steam design results to be the most promising solution among the investigated options.

| Parameter | Net Efficiency (-) | Gross Efficiency (-) | Mass Flow Rate (kg/s) | P max (bar) |
|---|---|---|---|---|
| Rankine Cycle | 46% | 47.6% | 344 | 250 |
| CO2 Brayton Cycle | 41% | 54.9% | 2014 | 280 |
| Helium Brayton Cycle | 32% | 88.0% | 569 | 50 |

*Table 15 – Comparison of some parameters for the three configurations*

## 4 Conclusions

The aim of this work is the pre-conceptual design and analysis of the most promising configurations for the ARC "FNSF phase" power conversion cycle, comparing three layouts: supercritical Rankine cycle, supercritical CO₂ Brayton cycle and supercritical He Brayton cycle. Efficiency is (obviously) the most important parameter to be considered for the choice of a cycle, but the latter should be also supported by other considerations. For example, it must be taken into account that, for the ARC reactor, compactness is one of the most important requirements. By comparing the different solutions investigated, it can be seen that the Rankine cycle is the most suitable from the net efficiency point of view, reaching a value of 0.46. However, Brayton cycles using CO₂ and He allow the adoption of less complex and more compact configurations, in support of the objectives of ARC reactor. From the point of view of the required mass flow rate too, Rankine cycle results to be the cycle that requires the least amount of mass flow, with 344 kg/s (and the same in terms of volumetric flow rate). This lower mass flow rate brings in a smaller size of the secondary heat exchanger. Moreover, the Rankine cycle is resulted as the best one from the point of view of commercial availability, being the most diffused and technologically advanced. Currently, there are operating supercritical and ultra-supercritical steam power plants which are characterized by higher pressure and rated power values than those considered within this study. Instead, power plants based on CO₂ and He cycles are still under development. Around the world, only a few experimental power stations characterized by these technologies are already in operation. In addition, such facilities do not host components suitable for the ARC Balance of Plant either in terms of size or working conditions. For all these technical and economic reasons, the Rankine cycle seems to be the most suitable option to satisfy the required conditions, and therefore the best choice to be adopted within the short period for the realization of ARC PCS in FNSF phase.

## References

[1] A.J.H. Donné et al., European roadmap to fusion energy, Presentation at 2018 Symposium On Fusion Technology (SOFT), Giardini Naxos, Italy, September 16-21 2018. Available online at: https://www.euro-fusion.org/fileadmin/user_upload/EUROfusion/Documents/180917.Donne.SOFT.Roadmap.v2.pdf.

[2] B.N. Sorbom et al., ARC: A compact, high-field, fusion nuclear science facility and demonstration power plant with

demountable magnets, Fusion Engineering and Design 100 (2015) 378-405,

[http://dx.doi.org/10.1016/j.fusengdes.2015.07.008.](http://dx.doi.org/10.1016/j.fusengdes.2015.07.008)

[3] S. Segantin et al., Exploration of power conversion thermodynamic cycles for ARC fusion reactor, Fusion

[Engineering and Design, 155 (2020) 111645, https://doi.org/10.1016/j.fusengdes.2020.111645](https://doi.org/10.1016/j.fusengdes.2020.111645)

[4] L. Barucca et al., Pre-conceptual design of EU DEMO balance of plant systems: Objectives and challenges, Fusion

Engineering and Design, 169 (2021) 112505.

[5] S. Ishiyama et al., Study of steam, helium and supercritical CO2 turbine power generations in prototype fusion

power reactor, Progress in Nuclear Energy, 50 (2008) 325-332, [https://doi.org/10.1016/j.pnucene.2007.11.078](https://doi.org/10.1016/j.pnucene.2007.11.078)

[6] F. R. Famà et al., An optimized power conversion system for a stellarator-based nuclear fusion power plant, Energy

Conversion and Management, 276 (2023) 116572, [https://doi.org/10.1016/j.enconman.2022.116572](https://doi.org/10.1016/j.enconman.2022.116572)

[7] L. Barucca et al., Maturation of critical technologies for the DEMO balance of plant systems, Fusion Engineering

and Design, 179 (2022) 113096, [https://doi.org/10.1016/j.fusengdes.2022.113096](https://doi.org/10.1016/j.fusengdes.2022.113096)

[8] GE Energy. GateCycle [TM] Help, User Manual, General Electric, 1989 – 2011.

[9] C. Forsberg, G. Zheng, R.G. Ballinger, S.T. Lam, Fusion Blankets and Fluoride Salt Cooled High Temperature

Reactors with FLiBe Salt Coolant: Common Challenges, Tritium Control, and Opportunities for Synergistic

Development Strategies Between Fission, Fusion and Solar Salt Technologies, Nuclear Technology, 206 (2020)

[1778-1801, https://doi.org/10.1080/00295450.2019.1691400.](https://doi.org/10.1080/00295450.2019.1691400)

[10] A. Iaboni, Pre-conceptual design of blanket cooling circuit’s heat exchangers of ARC fusion reactor, Master Thesis

work discussed in January 2022.

[11] Y. Yuan, J. Shan, L. Wang, X. Zhang, Control and thermal analysis for SCWR startup, Annals of Nuclear Energy

134 (2019) 27-37, [https://doi.org/10.1016/j.anucene.2019.05.057.](https://doi.org/10.1016/j.anucene.2019.05.057)

[12] J. I. Linares, L. E. Herranz, I. Fernández, A. Cantizano, B. Y. Moratilla, Supercritical CO2 Brayton power cycles

for DEMO fusion reactor based on Helium Cooled Lithium Lead blanket, Applied Thermal Engineering 76, (2015)

[123-133, http://dx.doi.org/10.1016/j.applthermaleng.2014.10.093.](http://dx.doi.org/10.1016/j.applthermaleng.2014.10.093)

[13] I. D. Irianto, Design and Analysis of Helium Brayton Cycle for Energy Conversion System of RGTT200K, J. Tek.

Reaktor. Nukl. 18 (2018) 75-86.

[14] W. Wagner, A. Kruse, Properties of Water and Steam, The Industrial Standard IAPWS-IF97, Springer-Verlag,

Berlin Heidelberg, New York, 1998, ISBN: 3-540-64339-7.

[15] R. C. Spencer, K. C. Cotton, C. N. Cannon, A method for Predicting the Performance of Steam Turbine Generators

[– 16,500 kW and Larger., J. Eng. Gas Turb. Power, 85 (1963) 249-298, https://doi.org/10.1115/1.3677341.](https://doi.org/10.1115/1.3677341)

[16] V. Narcisi, C. Ciurluini, G. Padula, F. Giannetti, Analysis of EU-DEMO WCLL Power Conversion System in two

relevant Balance of Plant configurations: direct coupling with auxiliary boiler and indirect coupling, MDPI

[Sustainability 14 (2022) 5779, 2022, https://doi.org/10.3390/su14105779.](https://doi.org/10.3390/su14105779)

[17] B. J. McBride, S. Gordon, Computer Program for Calculation of Complex Chemical Equilibrium Compositions and

Applications I. Analysis, NASA Reference Publication 1311 (1994).

[18] B. J. McBride, S. Gordon, Computer Program for Calculation of Complex Chemical Equilibrium Compositions and

Applications II. User’s Guide, NASA Reference Publication 1311 (1996).

[19] B. J. McBride, S. Gordon, Thermodynamic Data to 20 000 K for Monatomic Gases _,_ NASA/TP 208523 (1999).

