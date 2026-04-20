---
source: "https://www.osti.gov/pages/servlets/purl/1465662"
source_type: "url"
extracted_at: "2026-04-20T00:46:46.091627+00:00"
content_hash_sha256: "c56b9e013fef671ee83c571e4061a484a6f50f5a53236765fccb411cf5cf36b1"
backend: "pdf_pipeline"
---

## **The time-dependent simulation of CFETR baseline steady-state scenarios** 

Li Liu[a] , Charles Kessel[b] , Vincent Chan[a] , Yong Guo[c] , Jiale Chen[c] , Xiang Jian[d] , Shifeng Mao[a] , Minyou Ye[a*] and 

CFTER Physics Team 

_aSchool of Physical Sciences, University of Science and Technology of China, Hefei 230026, China bPrinceton Plasma Physics Laboratory, PO Box 451, Princeton University, Princeton, NJ, USA cInstitute of Plasma Physics, Chinese Academy of Sciences, No.350 Shushanhu Road, Hefei 230031, China_ 

_dState Key Laboratory of Advanced Electromagnetic Engineering and Technology, School of Electrical and Electronic Engineering, Huazhong University of Science and Technology, Wuhan 430074, China_ 

## **Abstract** 

One of the key issues to achieve the phase I mission of China Fusion Engineering Test Reactor (CFETR) is steady-state operation with a modest fusion power up to 200MW. To study this feasibility, time-dependent modeling of CFETR baseline scenario is performed. The time-dependent scenario design examines actual discharge features, including auxiliary heating and current drive scheme, equilibrium, transport, PF coil systems and plasma control system during the plasma evolution. During plasma current ramp-up, 10 MW of EC or LH heating is used to effectively save volt-second consumption to a reasonable level within magnet coil capability and to reduce li for better plasma control. Three reference scenarios are designed to target full non-inductive operation with different external heating and current drive (H&CD), which are NB+EC, NB+LH, and LH+EC, respectively. Two scenarios with neutral beams reach the required fusion power of CFETR phase I target, while for LH+EC scenario the fusion power and confinement is somewhat lower. A reversed magnetic shear with _q_ min 2 is sustained with off-axis current drive and bootstrap current for all cases examined. Ideal MHD analysis shows that both large toroidal mode number n ballooning mode and low n kink mode are stable in the three reference cases independent of whether the current is totally relaxed or not. The L mode and H-L back transition ramp-down are designed to successfully reduce the plasma current to 2 MA and keep li below 2 with ramp-down rate of 80 kA/s. The H-L back transition ramp-down yields improvements in the power transfer and coil current evolution as well as the li evolution. The heating and current drive characteristics of three auxiliary heating sources are indicated by scanning studies. A 2D scan of NB energy and tangency radius indicates the features of NB power deposition, current drive, torque and 

shine through issue. Both ramp-up and flattop are considered in the scanning of radio frequency parameters. For EC waves, the ramp-up phase constrains the parameter space more. The 2D scan of EC launch angle shows that EC waves launched above the midplane yield a better CD efficiency than using a midplane launcher. Specifically, 10 MW of EC waves launched from LFS above the midplane yield a maximum on axis driven current of about 0.55 MA, while waves launched from top yield a maximum near edge driven current of about 0.45 MA in the region of 0.5 . Scanning of _[n]_ ||[ in LH spectrum shows that ] _[n]_ ||[ should be set around 1.7 to get enough penetration ] (inside 0.7 ) for current drive and avoid strong accessibility problem. It is found that LH waves launched from HFS drives more current than that launched from LFS when _n_ is small. The maximum LH driven current reaches || 1.1 MA with 10 MW of LH power launched from HFS. 

## **1. Introduction** 

CFETR [1, 2] is recently proposed in China as a next step fusion facility to bridge the gaps between fusion experimental reactor ITER [3] and commercial demonstration reactor DEMO. It is designed as an important complement of ITER and DEMO. There are many challenging missions in the CFETR conception design, including demonstrating significant fusion neutron production, tritium self-sufficiency with high tritium breeding ration (TBR) >1.0, steady-state operation with a duty cycle of 0.3~0.5, and advanced blanket and divertor options for DEMO. One of the most challenging issues in physics design is developing a time-dependent scenario to predict the CFETR plasma performance and optimize the operation space within the physic and engineering constraints. The initial assessment of CFETR plasma from the 0D analysis [4] provided several scenarios for the baseline operation and advanced operation, which agrees well with other systems codes in a benchmarking study [5]. The optimized CFETR baseline scenario targets a steady-state operation with plasma current of 10 MA and fusion power of 200MW. Possible operations with higher B field and larger tokamak size for CFETR are also researched [6]. 

Multi-dimensional simulations of CFETR steady state scenario are also developed. A self-consistent integrated modeling workflow (consisting of transport solver, MHD equilibrium solver, sink and source calculations) within the OMFIT framework [7] is used to find the optimized physic conditions for the steady-state scenarios. In previous work [8, 9], the target fusion power of CFETR steady-state in phase I is achieved using an iterative method to find a converged and self-consistent solution. The key advantage of this method using OMFIT is fast simulation of plasma profiles, which provides effective optimization of plasma performance towards to the steady-state target 

effectively. 

Besides the steady-state targets, the plasma evolution, including flattop, ramp-up and ramp-down phase, and relative key issues during evolution also need to be addressed to make sure that the whole plasma discharge satisfies both the physics and engineering constraints. The time-dependent scenario can examine actual discharge features, which are absent from previous research on the steady-state targets. Coupling the poloidal field systems controller and passive conductors, the free boundary equilibrium solver, auxiliary heating, current and temperature profile evolution dynamics is a very challenging task for both physics and engineering. The tool we use for time-dependent simulation is the Tokamak Simulation Code (TSC) [10, 11] coupled with some auxiliary heating subroutine packages, which is being applied as a workflow for scenario designs on the CFETR integrated design platform [12-14]. 

For the CFETR phase I with a moderate bootstrap current fraction (36%) from the 0D analysis, off-axis current drive and heating are needed to build the equilibria with reversed magnetic shears. In this work, three types of heating systems are investigated: neural beam (NB), electron cyclotron waves (EC) and low hybrid waves (LH). The three heating systems have been demonstrated on various tokamak experiments and developed or designed on ITER [15-17]. Each heating systems has its own set of physics and engineering advantages and disadvantages. We choose different systems to work together to make the optimization of heating systems flexible to achieve the CFETR design target. Specifically, three reference scenarios are studied with different external heating and current drive (H&CD), which are NB+EC, NB+LH, and LH+EC, respectively. The evolution information of CFETR plasma during both ramp-up phase and flattop phase are simulated. Main global parameters at the steady-state phase for the three scenarios are compared with the 0D analysis. The ramp-down phase is discussed by comparison 

of L-mode ramp-down and H-L transition ramp-down. The parameter optimizations of heating systems are researched in our work. The current driven efficiency and power deposition of EC and LH during both ramp-up and flattop are studied with different EC and LH system parameters. In fact, the auxiliary heating is essential for the ramp-up phase to save flux consumption, to prevent the CS coils reaching their current or field limits. NBs with different energies and different injected positions are investigated. Besides the power deposition and current drives, the shine through power is also examined, especially when NB injection begins with a low density. Parameter optimizations of the auxiliary heating systems not only provides the best parameters space for the heating systems but also gives more choices for the detailed heating system engineering design. 

This paper is organized as follows. Section 2 presents the model tools, including the computing codes, physic 

models and assumptions. The three reference scenarios with different auxiliary heating sources are described in section 3. This is followed by scanning studies of external heating sources in section 4. Analysis of ramp-down phase is given in section 5. Conclusions are given in section 6. 

## **2. Modeling tools** 

## **2.1. Computational models** 

The free-boundary transport evolution code TSC is used to examine the full discharge evolutions. TSC computes the plasma equilibrium and field evolution equations on a two-dimensional Cartesian grid with the circuit conditions of the PF coils and passive structures, while plasma temperature profiles are solved by transport models on the one-dimensional flux surface averaged grid. The plasma control system is set to control the plasma position, shape and total current. TSC code has been used not only to reproduce the present experiments on many tokamaks, like TFTR [10], NSTX [18], EAST [19] and so on, but also to predict the features of future tokamak like ITER [20, 21], FNSF [22]and K-DEMO [23]. 

In this work, TSC is used to establish the full time-dependent scenario and compute all parameter evolutions, targeting to the CFETR design goals. With experimental conditions (temperature, density, current and equilibrium information) provided from TSC, ONETWO [24] can call various code packages to compute the power deposition and current drive profiles of auxiliary heating and return them back to TSC. The converged results can be obtained by iteration with standardized data exchanges and iteration criterions in the scenario design workflow on the CFETR integrated design platform [12]. The NB source model is the Monte Carlo code NUBEAM [25]. The EC wave mode is the ray-tracing code TORAY-GA [26]. Both the two codes are coupled with ONETWO. The LH source code is the 1D ray-tracing LSC code [27], which can be called in TSC. 

## **2.2. Physic models and scenario assumption** 

The CFETR geometry structures including coils and passive structures have been built as a digital tokamak in the TSC (as shown in figure 1). The corresponding 3D structures are shown in ref [12]. The constructed geometry structures are based on the CFETR conceptual design [1, 28], which is available on CFETR Integrated design platform. The main parameters from OD CFETR baseline case are used, which defines the plasma current of 10MA, major radius of 5.7m, minor radius of 1.6m, central magnetic field of 5T, elongation of 2.0, and triangle deformation of 0.4. 

![](images/tmpun_my039.pdf-0005-00.png)

**Figure1.** Geometry of CFETR. PF and OH coils (red boxes with inscribed ‘x’), vacuum vessels (green parallelograms) and first wall (thin blue lines) are shown. The contour line is the 2D poloidal flux distribution for CFETR baseline case at steady-state operation. The thick blue line is the plasma boundary controlled by the plasma control systems. 

Since individual transport models have different features that are more appropriate for ramp-up experiments [29-31]and stationary H-mode, two different transport models are used for flattop (H-mode) and ramp-up (L-mode), respectively. The Coppi-Tang model [10] has demonstrated good agreements with selected L-mode or current ramp-up experiments on TFTR [10], EAST [19], JET [32], and ASDEX [33]. Recent simulations [30, 31] of some large-bore ramp-up experiments on DIII-D show that the Coppi-Tang model tends to overestimate the confinement at the beginning of ramp-up phase just after formation of plasma equilibrium. Therefore, a scale factor is applied to the overall transport to make the H factor close to 0.5 for the beginning of the ramp-up phase (before 10s for CFETR). 

For H mode in the CFETR baseline scenario, the CDBM model [34] is used. The CDBM is a reduced-physics transport model of turbulence induced by current diffusivity constructed by solving the eigenvalue equations for the ballooning mode and the interchange mode. The thermal transport is considered as the sum of neoclassical transport and turbulence transport _CDBM_ 

2 _CDBM_ 12 _F s_ ,ˆ _Fk FE_ 3/2 _c_ 2 _vA_ , _wpe qR_ where c is the speed of light, _wpe_ the electron plasma frequency, _vA_ the toroidal Alfven velocity, _s rq_ 1 _dq_ / _dr_ the magnetic shear, _q_ 2 _R d_ / _dr_ the normalized pressure gradient, 2 _k r_ / _R_ 1 1/ _q_ the magnetic curvature. The factor _F s_ ,ˆ represents the effect of weak or negative magnetic shear and the Shafranov shift. The term _Fk_ represents the correction for plasma shape. The term _FE_ 1 _G s_ , _wE_ 2 1 represents the effect of _E B_ rotation shear, which contributes significantly to turbulence stabilization when strong rotation exists in CFETR scenario with NBI. The plasma rotation induced by ~70 MW of NBI for CFETR is calculated based on the results of ONETWO and NUBEAM. The CDBM model has been able to describe ITB formations in high _p_ and reversed shear plasmas for JT-60U [34] and ITER [20, 35, 36]. CDBM is a model for core transport and not valid near pedestal region, while Coppi-Tang mode includes empirical temperature boundary condition. According to F.M. Poli’s similar work for ITER [36], the CDBM model is used inside 0.75 , the Coppi-Tang model and the EPED1 pedestal are applied outside this radius, and a hyperbolic function is used to match the two regions. The pedestal pressure evolution is determined by a correlation fit [37, 38] of density and Zeff to the peeling-ballooning model EPED1 [39] results, which is generated by the prescribed thermal diffusivity from the pedestal top to the separatrix. 

The simulation is performed on L-mode for current ramp-up and H-mode for the flattop. Based on the  0.72 0.8 0.94 Martin’s scaling law [40] _Pthr_  0.049 _ne BT S_ , where S is the plasma surface area, L-H transition threshold is depended on electron density when plasma shape is fixed. Therefore, the volume-average density _ne_ is designed to be 0.18 _nGW_ at the end of current ramp-up phase and 0.4 _nGW_ ~ 0.45 _nGW_ at the final burning phase, not only to avoid the H-mode entry problem with high density, but also avoid low-density issues such as tearing modes and possible NBI shine through problems. _ne_ (0) is set to be linearly increasing with plasma current during ramp up, and turning over parabolically to an asymptotic value after entering H-mode. Because of the lack of well-validated density transport model in TSC, the density profile is assumed to be parabolic with peaking factor _ne_ (0) / _ne_  1.35 ~ 1.6 during the plasma density evolution. At the end of density increase, the density profile for plasma burning is CFETR baseline density profile with a scale factor. The baseline density profile is evolved by a 

physics-based transport model with sources and sinks in previous work [9] within the OMFIT framework. The DT fuel density is determined by quasi-neutrality assuming equal amounts of D and T. The helium concentration is * determined by an input of τHe /τE =5 . For CFETR, the external impurity seeding of Ar is a viable way to radiate power from the core plasma and disperse heat flux for divertor control [41]. In our simulation, Ar is the main impurity. In addition, tungsten and carbon impurities are expected from erosion of the divertor and first wall. The impurity density profile shapes are assumed to be the same as the electron density profile, with different fractions as a function of time. The fraction of tungsten is fixed at 5 10 6 . The fractions of other impurities are selected to make Zeff close to the OD design value of 2.1. Bremsstrahlung, cyclotron and line radiation are included. The Sauter bootstrap current model [42] and the Hirshman plasma resistivity formulation [43] are used. 

The L-H transition or H-L back transition is determined by the comparison of the net power ( _Pnet P_ int _Prad dW_ / _dt_ ) and threshold power ( _Pthr_ ) from Martin's scaling law. However, there are still many uncertainties in the physics of confinement bifurcation. Experiments on different tokamaks indicate different features on the power requirements of L-H transition and the hysteresis of H-L back transition [44, 45]. To account for these uncertainties, a conservative criterion with larger net power requirement is considered ( _Pnet_ 1.5 _Pthr_ for L-H transition and _Pnet Pthr_ for H-L back transition). 

## **3. The reference scenarios** 

The main differences among the reference scenarios are the heating schemes. The heating and current drive sources are essential for CFETR to achieve the design target of steady-state operation while not interfering with tritium self-sufficiency. The driven currents combining with the bootstrap current determine the safety factor profile. The heating systems during plasma evolution can effectively improve the plasma temperature to save flux consumption for ramp-up phase and enter H-mode and sustain the plasma burning phase. For CFETR, three types of heating systems (NB, LH and EC) are considered as candidates. The preferred choice is two systems working together to achieve CFETR design goals. For CFETR with high duty cycle, two kinds of heating systems are attractive in saving first wall surface for blankets and reducing maintenance difficulty. Meanwhile, using two systems retains a capability of flexibly controlling the current profiles. Simulations only using one NB system show that it is hard to control the q profiles to obtain a board reverse shear region. The paper reports on the three reference scenarios, NB+EC, NB+LH, and LH+EC, respectively. 

## **3.1. The ramp-up phase** 

Figure 2 shows the time evolution of plasma parameters for the three reference scenarios, including the power, current, temperature, density, internal inductance, beta, safety factor and flux consumption. Figure 3 shows the trajectories of main parameters in the NB+EC scenario during current ramp-up and density ramp-up. Table 1 lists the global parameters of the three scenarios, compared with 0D results. The initial plasma (500 kA) is constrained to start on the Last Flux Surface (LFS) of outer torus at 2s after breakdown, while X-points formation takes place ~ 10s at _I p_ =2 MA. The plasma current ramps to 10 MA at 50s (ramp rate 0.2 MA/s) to save flux consumption. A slower ramp leads to a peaked current profile (high _li_ ) and strong vertical instability as well as a large volt-second consumption. Simulation with the ramp rate of 0.125MA/s shows that the total consumed volt-seconds reaches 170 Wb, which exceeds the designed PF coil systems capability. With a low ramp rate of 0.125MA/s, it is difficult to reduce volt-seconds to satisfy the coil systems’ limit even with the assist of auxiliary heating systems. On the other hand, faster current ramp-up implies not only larger required power supply abilities and eddy current loads on the conducting structures, but also increases the possibility of MHD instability due to the hollow current profile. The ramp rate is set 0.2 MA/s as a trade-off, and is typical for full superconducting device like EAST and ITER. The RZIP control system [46] and the plasma shape control system [47, 48] are used to control the plasma current, shape and position evolution [49]. 

According to the CFETR conceptual design of PF magnetic system and basic physics parameter, the total volt-seconds provided by coil systems is expected to be about 160 Wb [28]. The final value should be a little different based on the actual plasma current evolutions. Ohmic current ramp-up with ramp rate of 0.2 MA/s and shape evolution approximately consumes 140 Wb volt-seconds. Additionally, a conservative estimate of 20 Wb volt-seconds is needed for breaking down the plasma and building the initial equilibrium. Hence, there are not enough volt-seconds left to support and control a long flattop. As a result, some coil currents approach or exceed the maximum current limit. To save volt-seconds in the ramp-up to allow access to a long and controllable flattop, the auxiliary heating is absolutely needed. LH and EC waves can drive current in the ramp-up phase, reduce the inductively driven current, and improve the plasma temperature. The additional current drive and higher temperature can reduce the inductive and resistive volt-second consumed in the ramp up, resulting in more volt-seconds for the flattop. It is found that the current drive efficiency of NB during ramp-up is low and the NB shine through restricts its application in the early heating until near the end of ramp-up. 

With the assist of 10 MW EC or LH wave, the total flux consumption during current ramp-up is reduced to be close to the 0D design of 120Wb [4] as shown in figure 2, figure3 and table 1. The CS coil current evolutions stay within the maximum current limit in the three reference cases. The LH assist ramp-up scenario saves 9 Vs more than EC assist ramp-up scenario. The difference in volt-seconds between the two cases is mainly caused by an additional 5 MW of LH heating between 20s and 30s in the LH case. The current driven and power deposition of LH wave are efficient when the plasma temperature and density are very low at 20s, while the power deposition of EC wave at that time is very low due to low absorption. The EC steering will not be changed during a discharge. Optimizing the EC injected angles can improve the EC efficiency at 20s, which also decreases the EC efficiency during the burning phase. High edge temperature induced by LH or EC waves slows the current penetration. The off-axis current drive changes the plasma current composition. Both mechanisms change the current profile evolution, leading to the final _li_ changing from 1.0 (at the end of ohmic ramp-up) to below 0.8. The lower li reduces the risk of vertical instability and make the current profile closer to the totally relaxed burning H-mode state. 

## **3.2. The flattop phase** 

To bridge of the gap between the ramp-up and burning phase, the heating systems are designed to turn on step by step to ensure a smooth evolution without sudden changes of plasma parameters. Immediately after ramp-up at 50s, additional heating systems are turned on to assist the confinement to enter H-mode ( _Pnet_ 1.5 _Pthr_ ). Simulations [40, 

50, 51] of ITER and EU-DEMO L-H transition show that more heating power than burning phase is required to obtain a robust entrance of H-mode. But CFETR baseline case with smaller size and lower toroidal field and density requires a much smaller L-H transition threshold power. As shown in figure 2 and 3, only half of the full power of NB and LH heating systems is required, which provides enough power to enter H mode. In the NB scenarios, half power operation reduces total NB shine through power when the plasma density is low, avoiding possible damage to the first wall. Full power operation begins from 100s when the density rises to the burning level. The combination of auxiliary heating and alpha heating sustains the high confinement mode and continuously burning plasma. 

For NB+EC scenario, there are two tangential neutral beams. One beam with high energy (~300 keV) and large tangency radius ( _Rrt_ 6.5 _m_ ) is used to drive a broad off-axis current. The beam power is adjusted to make sure the full non-inductive operation. Additional 10 MW of neutral beam with low energy (~100 keV) and small 

tangency radius ( _Rrt_ 5.3 _m_ ) is used to directly heat the ion in the central and provide torque for plasma rotation. The NB energy and tangency radius are based on the optimization work [8, 9] made with a tradeoff between high global fusion gain and low edge heating. As shown in figure 4, the NB heating and current drive are dominantly located in the region of 0.4 . With a total of 73 MW of injected power, 66 MW of NB power is absorbed and 5.93 MA of NBCD is driven. The fraction of heating on the ions reaches 69.7%, which contributes to higher ion temperature and stronger fusion reaction. To sustain a broad reversed magnetic region, 10 MW of electron cyclotron waves from top launch is used to modify the q profile and maintain _q_ min 2.0 . The frequency is 190 GHz. The launch angles of ( , ) = (146, 250) are optimized to get the maximum off-axis current drive of 0.44 MA of ECCD located at 0.65 . Simulation without EC source produces a smaller reversed magnetic region 0.3 and smaller minimum safety factor _q_ min 2.0 . Scanning studies of NB and EC parameters are also given in section 4. 

In the NB+LH scenario, the lower hybrid wave is used to drive more current than EC and reduce the power requirement of NBs, while the NB energy and tangency radius are same with NB+EC case. Due to different plasma condition and NB power, the NB current drive and heating profiles are a little different from NB+EC scenario. The radio frequency current drive is quite different. LH waves used in the reference scenarios are launched form outboard side at 60 degree with _n_ =1.75. Launched from other position including HFS is discussed in section 4. As shown in table 1, with the same power the current driven by LH wave is two times larger than ECCD, which saves 4MW of the power requirement for the NB with high energy. LHCD is distributed more broadly and is located closer to plasma boundary ( 0.7 ). The edge located LHCD expands the magnetic field reversed region from 0.69 to 0.8. 

In the EC+LH scenario, 40 MW of EC and 57 MW of LH waves are used to replace NB heating and current drives. Two EC antennas with different injection positions (top with ( , ) = (146, 250) and LFS above the midplane with ( , ) = (120, 220)) are used to broaden the EC current drive profile and avoid strong sudden changes in the q profiles, which may lead to MHD instabilities. The EC current drive profile covers the region 0.3 0.7 as shown in figures 4. The all radio frequency assisted scenario can save window areas on the first wall and space occupied beside the vacuums vessel. However, the central plasma temperature especially ion temperature decreases a lot, since there is no plasma rotation to suppress turbulence transport and no direct heating 

on ions sustained by NBs. Consequently, fusion reactivity decreases and fusion gain drops to 1.2. 

Comparing with the 0D study [4], the two scenarios with neutral beams reach the required fusion power although the fusion gain is a little smaller because of the larger input power. Comparing H factor and normalized 

beta as well as the plasma temperature, the plasma confinement in the physic base simulation seems not as good as 0D system code expected. The density for three references is designed larger than the 0D studies to produce similar bootstrap current fraction and fusion power as 0D designs. The normalized current drive efficiency of main heating systems in the 1.5-dimensional simulation is larger than 0D. However, lower temperature and higher density in 1.5-dimensional simulation make the total current drive fall below the 0D prediction with the same power, which means that more power is required to obtain a fully non-inductive scenario. 

![](images/tmpun_my039.pdf-0011-03.png)

**Figure2.** The trajectories of main parameters in the three reference scenarios (Left：NB+EC, Mid: NB+LH, Right: EC+LH). (a) Total plasma current (black solid), ohmic current (black dash), bootstrap current (blue), NBCD (red), ECCD (green) and LHCD (pink); (b) total heating power (black solid), radiation power (black dash), alpha heating power (blue), L-H transition power threshold (yellow), NB (red), EC (green) and LH power (pink); (c) toroidal and poloidal beta, and fusion gain; (d) safe factor on-axis q0, qedge and q95; (e) central electron and ion temperature; (f) 

central, line and volume average electron density; (g) internal inductance li ( _i BP_ 2 / 0 _I_ / _LP_ 2 ) and li(3); (h) the 

internal, resistive and total flux consumption. 

![](images/tmpun_my039.pdf-0012-03.png)

**Figure3.** The trajectories of main parameters in the NB+EC scenario during current ramp-up and density ramp-up. (The meaning of color and symbols for individual lines is the same as in figure 2). 

![](images/tmpun_my039.pdf-0013-00.png)

**Figure4.** The power, current, temperature, density and safety factor of three reference scenarios (Left：NB+EC, Mid: 

NB+LH, Right: EC+LH). (a) Alpha (blue), NB (red), EC (green), LH (pink) and radiation (black) power density profiles; (b) total current (black), bootstrap current (blue), NBCD (red), ECCD (green) and LHCD (pink); (c) ion and electron temperature profiles; (d) ion and electron density profiles; (e) safe factor profiles. 

## **3.3. Ideal MHD** 

One of the main challenges in the CFETR physic design is to avoid MHD instabilities. For CFETR profile target, a reversed magnetic shear with _q_ min 2 is selected so that some dangerous low n MHD modes occurring with _q_ min 2 can be avoided. However, the large pressure gradients and large current density near the edge may reduce the no-wall limit and cause harmful MHD instabilities over a wide range of _N_ [52]. The ideal kink instabilities 

(dominate n=1 modes with multiple harmonics) are observed in many reversed shear discharges with strong peak pressure profiles in JT60-U [53], JET [54], DIII-D [55], which may lead to disruptions. For CFETR, the reversed 

shear could improve plasma confinement and enlarge the pressure gradients. It is necessary to check the ideal MHD 

stability of CFETR during the plasma evolution. In our work, the time-dependent equilibrium simulated by TSC is recalculated with a flux coordinate fixed boundary equilibrium code J-SOLVER [56] to facilitate investigation of ideal MHD activities on the selected time point. PEST1 (Princeton Equilibrium and Stability) code [57] is used to analyze the low n linear stability of fast growing ideal MHD modes. The code is based on the energy principle, which introduces linearized perturbations of equilibrium to determine the stability of a given equilibrium. For large n ballooning modes, the code BALMSC [57, 58] is used to solve _n_ ballooning stability with finite shear, using a 4th order Runge–Kutta method. Simulations show that both high n ballooning mode and low n ( _n_ 3 ) kink mode are stable in the three reference cases with low _N_ . It should be noted that the ideal modes are still stable when the current profiles have not yet reached a relaxed state such as at 200s and 500s. The ideal MHD problem should be serious in the next step of CFETR phase II design with the target of 1GW fusion power. In that case, _N_ would be large and might exceed the Troyon no-wall limit [59]. 

**Table1.** The global parameters of the three CFETR steady-state scenarios with different auxiliary heating and current drives, comparing with the 0D systems study[4]. Almost all the plasma parameters calculated at 3000s, except that the value of volt-seconds is consumed during current ramp-up. It should be noted that the total power is the absorbed power in the 0D study, while the NB power in 1.5-dimensional simulations is the injected power. The last two lines show whether the relaxed equilibrium is stable (S) or unstable (U) to ideal MHD modes. 

![](images/tmpun_my039.pdf-0015-01.png)

**Figure5.** Plan view of geometry sketch for the two tangential neutral beam injections used in CFETR. 

## **4. Scanning studies of auxiliary sources** 

## **4.1. Optimization of Neutral Beams** 

Generally, the optimizations of NB parameters are very complicated. Both the physic and engineering constraints should be considered to settle the NB energy, location and orientation. Neutral beams with higher energies are more efficient for current drive. Recently MeV accelerator experiments [60] show that the negative ion current density in the beam line increases with beam energy, which indicates that the requirements of beamline numbers and NB window areas on the first wall decrease with increasing beam energy. However, higher energy reduces the injected torque and thus the plasma confinement. Also, the shine through power increases with increasing beam energy. Technically, high-energy NB development still faces more challenges in achieving MeV beam energy and expanding the pulse duration. Significant development remains to improve the pulse duration to a suitable level for steady state operation base on the MeV accelerator experiments [60, 61]. The NB location and orientation will 

determine the NB footpath in the plasma hence the current drive profiles and shine through power. Compromise among these constraints should be reached for the final Neutral Beam engineering design. To get a comprehensive consideration in the final NB design, it is necessary to perform NB parameter scans and map out the NB parameter space for CFETR. 

The NB orientation and location should be fixed to avoid engineering uncertainty and save more space for breeding blanket to achieve tritium self-sufficiency. Typically, the neutral beam path should straightly thread through TF coils, PF coils, blanket modules and other structures, which strongly restricts the choices of orientation and location. This is the main reason to design the CFETR neutral beam to be tangentially injected into the plasma from the outer midplane. In recent calculations for future tokamaks [62], tipping the beamline and mounting the neutral beams above or below the midplane, and steering to the innermost tangency radius, provided feasible current profiles that extend across the whole minor radius. For CFETR, we choose to change the tangency radius to obtain the desired heating or current drive profile (as shown in figure 5). To get the optimized parameters of neutral beams, a two-dimensional scan that varies the tangency radius and beam energy is studied. 

The optimization of the Neutral beams is based on the NB+EC scenario. The profile information and equilibrium of background plasma are selected at 3000s after the plasma current has totally relaxes. We focus on the NB1 with high energy ( _E_ =300 keV) and large tangency radius ( _Rrt_ 6.5 _m_ ). Another beam with low energy is 

used to provide ion heating and plasma torque. The current driven by lower energy beam is very small (about 0.25MA). The tangency radius and beam energy of neutral beam are scanned over 200~700 cm and 100~1000 keV, respectively. The power deposition, current drive, current center and total torque caused by the NB with different energy and tangency radius are shown in figure 6. The gray star in the plots indicates the NB parameters used for CFETR based on the previous optimization of fusion gain. The optimum region where the driven current is larger than 4 MA and absorbed power is larger than 64 MW, is indicted by white dash. In the scanning study, more features of NB heating on different aspects are explored. In the region of 400 _Rrt_ 660 cm and 300  _E_  1000 keV, the power 

deposition is maximum (more than 64 MW of absorbed power with total 73 MW of injected power). As shown in figure 7, ion heating is dominant with low NB energy, while electron heating increases with NB energy and becomes dominant when NB energy reaches 1000 keV. The NB current drive center moves from the core to the edge with the tangency radius increasing and energy decreasing. The total current drive increases with the beam energy. The low energy NBs trend to heat the ion and drive less toroidal plasma current because of their wide distribution in pitch angle. In the direction of the radial tangency, the current drive reaches the maximum values 

from 3.5MA to 8.2MA near _Rrt_ 6.6 _m_ . The corresponding current drive efficiency changes from _Icd R_ 0 _ne_ ,20 / _Pb_ 0.16 0.37A W-1 m-2 , with higher efficiency occurring with high beam energy. Current 

drive decreases with _Rrt_ decreasing from 6.6m to 2.0m, while the current drive location changes from plasma edge with low density to the plasma core with high density. The total torque decreases with increasing energy, and the tangency radius scan shows that total torque reaches a maximum value also near 6.6m. The neutral beam path length in the plasma becomes short when _Rrt_ 6.6 _m_ , which means the interactions between plasma and neutral beams are inadequate. This causes strong decrease of power deposition, current drive and total torque in the region of _Rrt_ 6.6 _m_ . 

The shine through problem is another key point we should take into account for the NB design. The high shine through power density on the first wall will definitely cause sputtering and thermal damage on the first wall material. The shine through power for the parameter scan is shown in figure 8(a). The density of steady state operation is high enough to avoid beam shine through in most plasma parameters space. Immediately after NB injection begins, the shine through is also given in figure 8(b) when plasma density is low and shine through problem is most serious. The shine through power in the low-density case is much larger than that in high-density case. It should be noted that the total power in the low-density case is only half of the full power. Half power operation during initial NB injection avoids strong shine through power and drastic changes in plasma parameters. Generally, the shine through power increases with the NB energy. The minimum shine through power is located around _Rrt_ 5.0 _m_ where the neutral beam path is longest and the density on the beam footprint is highest. When _Rrt_ 4.1 _m_ , the neutral beamline targets to the inner wall, which greatly increases the shine through power, as clearly shown in figure 8(b). Through the optimization of NB parameters, it is easier to find low shine through power region such as below 1 MW. However, it is not possible to calculate to the maximum power density on the first wall before the detailed blanket and NB design are completed. The power density distribution is strongly influenced by NB orientation and first wall shape. Non-uniform structures like the gaps between blanket modules will be easily damaged by high power density, which increases the complexity of the extreme power density calculation. These considerations will be important topics of NB engineering design in the future. 

Overall, the best NB parameters should be inside the region of 400 _Rrt_ 660 cm and 300 _E_ 1000 keV, as indicated by white dash in figure 6, through synthetical considerations of power deposition, current drive, torque 

and shine through power. It should be noted that the shine through should be treated seriously in the parameter space corner of high tangency radius and energy. The final decision of NB design depends on comprehensive considerations of all the limits, which should be a compromise of physic performance and engineering constraints. The development of MeV accelerator experiments in the future will also influence the final NB construction. 

![](images/tmpun_my039.pdf-0018-01.png)

**Figure6.** Scans of beam energy and _Rrt_ for the NB1. The distribution of total (a) NB power deposition, (b) current driven, (c) current center, (d) injected total torque are given. The gray star marked on the plots indicates the parameters used for CFETR. The region surrounded by the white dash indicts the optimum region where the driven current is larger than 4 MA and the absorbed power is larger than 64 MW. 

![](images/tmpun_my039.pdf-0018-03.png)

**Figure7.** The power deposition of NB1 on the ions (a) and electrons (b) when scanning the beam energy and _Rrt_ . The power deposition of 10 MW low energy NB2 is 6.89 MW and 1.01MW on the ions and electrons, respectively. 

![](images/tmpun_my039.pdf-0019-00.png)

**Figure8.** The scans of beam energy and _Rrt_ for the shine through power at the plasma burning phase at 3000s (a) and the beginning of flattop at 50s (b). The NBI injection begins at 50s and the shine through is large because of low density even with half power operation. The white dash is the same as that in figure 6. 

## **4.2. Optimization of Electron cyclotron waves** 

The EC system is designed to provide modification of the q profile and active control of MHD activities as well as saving the flux consumption during the ramp-up phase. Typically, the optimization of EC parameters requires a four-dimensional scan among frequency, launch position, poloidal injection angle and toroidal injection angle. For CFETR, the optimized frequency for the fundamental O-mode EC wave is about 190 GHz with _BT_ 5.0T . Three launch positions are taken into consideration. The positions of top, low field side above the midplane (LFS) and equatorial launcher (midplane) are (R, Z) = (5.5, 4.0) m, (R, Z) = (7.1, 2.2) m and (R, Z) = (7.4, 0.0) m, respectively. Now the task of scanning EC parameters is reduced to the scanning of the poloidal injection angle and toroidal injection angle at the three launch positions. 

The optimization of the EC parameters is based on the scenario with NB+EC, since the EC+LH case is not competitive in fusion gain. Figure 9 provides the power deposition, current drive and current location of the top, LFS and midplane launch, respectively. Overall, the maximum on-axis CD efficiency in the region of 0.5 

0.55 MA launched from LFS above midplane, while the maximum off-axis CD efficiency in the region of 0.5 is 0.45 MA launched from top. EC waves launched from LFS also allows a larger range of current drive locations, while the driven current drops with the current drive location changing from plasma core to the edge. EC waves launched from the midplane exhibits a litter smaller maximum CD efficiency but a larger parameter space where the current drive is larger than 0.35 MA. For the top launcher, it’s hard to drive current near the magnetic axis. 

However, the CD efficiency of top launch is larger than that of LFS launch when only comparing the current location region of 0.5 . With moving the launcher form midplane to the top, the current location moves from plasma core to the edge and the parameter space with large current drive (IECCD>0.35 MA) becomes smaller. The comparison of efficiency between LFS and midplane launchers agrees with studies of the ECCD efficiency on DEMO plasma [63], which show that injection from an upper port rather than midplane launched tends to yield a higher CD efficiency. It is because of the larger aspect ratio leading smaller trapped-particle fraction, and shorter paths through the region of parasitic absorption resulting in less second-harmonic absorption [63]. With top launch, location 0.5 with low temperature results in low current drive. 

The EC waves launched from top is good for tailoring the current profiles and broadening the magnetic reversed shear region for CFETR, while the EC waves launched from LFS or midplane is good at driving current near the magnetic axis and for active control of MHD activities for the whole region. This feature of launch position agrees with the similar scan work in a different scenario with higher EC power and using the OMFIT framework [8]. Due to the advantages of the different launch positions in different regions, the combination of two launch positions is an attractive way to broaden the EC current drive profile. As shown in figure 4, both top and LFS launcher are used in the EC+LH scenarios to broaden the driven current profiles and provide a relatively smooth q profile to avoid any undesirable MHD activities. 

The usage of auxiliary heating during the ramp-up phase saves volt-second consumption and reduces the CS coil size. Both auxiliary heating and current drive can save volt-second consumption. The current drive current during ramp-up reduces the amount of inductive current driven, while the heating improves electron temperature in order to reduce resistive volt-second consumption. It is necessary to study the heating and current drive characteristic of EC during current ramp-up. The features of EC waves with three launch positions on the ramp-up phase at 30s are indicated in figure 10. The current drive of top launch still mainly locates in the region of 0.5 . 

The CD efficiency of top launch is higher than that of LFS launch, which is different from flattop. Comparing with flattop, all the three cases with lower density yield a higher CD efficiency. Comparing the two figures, the region of power deposition larger than 9 MW and the region of current drive larger than 0.35MA become smaller in current ramp-up, which means that the parameter space is more limited during ramp-up phase. Scanning studies at 40s and 50s yield a larger region of high power deposition because of higher density and temperature. The region where 

current drive is larger than 0.35 MA at 3000s is also indicated by a magenta dash on the results of ramp-up phase in figure 10. The overlapping of optimum regions for the two conditions (surrounded by white and magenta dash) 

provides a good parameter space for both ramp-up phase and flattop phase. It should be noted that the proximity of the maximum current drive region to the region of low power deposition and current causes the rapidly changing results in some directions with launch angle changes. For example, the maximum current in LFS launch case at flattop locates at ( , ) = (124, 233). By only increasing the launch angles a little to ( , ) = (130, 240), the power deposition and current drive decrease below 1 MW and 0.05 MA, respectively. The launch angle design should be kept away from this rapidly changing region to minimize the influnence of plasma fluctuations on EC proformance. 

![](images/tmpun_my039.pdf-0022-00.png)

**Figure9.** Scans of the poloidal and toroidal steering angles for EC waves at launched from top, LFS and midplane. The power deposition (a), current drive (b) and current location (c) are given. The scan studies are based on the equilibrium and profiles information EC+NB scenario at 3000s during the burning phase. The region where current drive is larger than 0.35 MA is indicated by a white dash in the plots of power deposition and current location. 

![](images/tmpun_my039.pdf-0023-00.png)

**Figure10.** Scans of the poloidal and toroidal steering angles for EC waves at launched from top, LFS and middle plane during current ramp-up at 30s. The power deposition (a), current drive (b) and current location (c) are given. The scan studies are based on the equilibrium and profiles information EC+NB scenario at 30s during the ramp-up phase. The region surrounded by a white dash in the plots of power deposition and current location is the region where current drive is larger than 0.35 MA. The region surrounded by a magenta dash in the plots is the region where current drive is larger than 0.35 MA in the scanning study of flattop. The overlapping region of white and magenta provides good parameter space for both ramp-up phase and flattop phase. 

## **4.3. Optimization of Low Hybrid waves** 

The LH wave is selected as an important current drive tool because of its high CD efficiency. The frequency of LH wave is selected to be 5 GHz like ITER [64], which is a balance of avoiding high LH power absorption on the fast alpha particle and reasonable waveguide width. The launched spectrum is modeled as two Gaussian lobes with _n_ || 0.2 about the central _[n]_ ||[ to approximate the typical spectra from a LH wave grill. To describe the ] experimental passive-active multi-junction (PAM) launcher [17], the one lobe is set with a variable _n_ in the co-Ip direction, while another lobe is set with _n_ 6.0 in the counter-Ip direction. The power split is set as 87% in the co-Ip and 13% in the counter-Ip lobes to match the total CD prediction with GENRAY/CQL3D ray-tracing 2D Fokker–Planck model[65]. 

![](images/tmpun_my039.pdf-0024-02.png)

**Figure11.** Total current driven by 10 MW of Low Hybrid waves at 3000s during flattop (a) and at 40s during ramp-up (b) as a function of _n_ changing from 1.35 to 2.25, launched with different poloidal angles on the outboard side (0 and 

60 degree from LFS, 130 and 150 degree from HFS). 

![](images/tmpun_my039.pdf-0025-00.png)

**Figure12.** Current drive profiles for lower hybrid waves during flattop with different _n_ of the co-Ip lobe, launched from 60 degree at LFS (a) and 130 degree at HFS (b). 

![](images/tmpun_my039.pdf-0025-02.png)

**Figure13.** The window of _n_ defined by the accessibility limit and strong Landau damping with the information of CFETR baseline scenario (NB+LH). The strong electron Landau damping occurs at the flux surface where electrons having the parallel velocity of electron ( _vp_ || _c_ / _n_ || ) with ~ 3 _vth_ , where _vth_ is the electron thermal velocity defined by 

2 _Te_ / _me_ . The window at the high field side allows lower _n_ for penetration to the plasma deeper. 

The scanning study of LH is based on the NB+LH scenario. Figure 11 shows the total LH current driven by 10 MW of LH power with different _n_ in the co-Ip direction and different launcher’s poloidal angle on the outboard side. Both LFS (0 and 60 degree) and HFS (130 and 150 degree) launcher are considered. Figure 12 shows the current profiles for waves during flattop launched form outboard side at 60 degree and 130 degree with _n_ =1.35, 1.55, 1.75, 1.95 and 2.15. The negative current drives in the plasma edge in all the cases are associated with the counter-Ip lobe of the launched spectrum. The maximum LHCD changing from 0.9MA to 1.1 MA for different launcher’s position is obtained around _n_ 1.7 with penetrating inside 0.7 . When the launched _n_ is small 

and there is no enough _n_ upshift before cut off in the ray trajectory, the accessibility condition [66] 

_n ck_ || / 1 2 _pi_ / 2 2 _pe_ / _ce_ 2 _pe_ / _ce n_ || _acc_ , prevents the LH wave penetration into the plasma. _n acc_ is the maximum inaccessible _n_ limited by accessibility condition. As shown in figure 13, the plasma is inaccessible to the LH waves when _n_ is too small. The slow waves are cut off at the plasma edge and converted into fast waves, which propagate back to the separatrix and then reflect into the plasma with _n_ upshifts and subsequently damp close to the separatrix. Damping close to the separatrix leads to low current drive efficiency due to low temperature. As shown in figure 12, the current profiles around 0.9 are the converted fast wave driven currents when _n_ =1.35, 1.55. When launched _n_ is large, the electron Landau damping is very strong in the large radius region as shown in figure 13. The LH waves are fully absorbed before penetrating into plasma core and less current drive occurs there. As shown in figure 12, the penetration decreases with _n_ increasing no matter where the launch position is. 

Launching from HFS is proposed as an attractive candidate for future tokamaks based on recent studies by MIT team [67]. Compared with LFS, plasma with HFS launcher meets a better scrape off layer condition and impurities screening condition. HFS launcher can also improve the LHCD performance by allowing the use of smaller _n_ penetrating deeper into the plasma as shown in figure 13. That is because that higher toroidal field _B_ 0 on HFS improves wave accessibility by lowering the accessibility condition limit _n acc_ . For LFS launcher, higher _n_ or rapidly upshift of _n_ are required to get the access to the plasma core. As shown in figure 12, LH waves launched from HFS drive more current than LFS, especially when _n_ is small. LH wave penetrates deeper and 

drives current deeper than that launched from LFS when _n_ =1.35 and 1.55. However, large edge current driven by 

converted fast wave reduces the total driven current when _n_ is small. Since the WKB approximation is poor for ray tracing of the converted fast wave, estimate of the edge current should only be considered qualitative. Nevertheless, the launched _n_ should not be too low to avoid large edge current for both LFS and HFS. The 

scanning studies of LH in this paper focus on the CFETR baseline scenario with low density. For CFETR phase II with higher density, the advantage of HFS launch may be more obvious regarding the possibility of penetrating inside the pedestal. 

It should be noted that _n acc_ is very low during current ramp-up with low density. The wave penetrates deep into the plasma core and drives much more current than that of flattop. The LH current drive increases with _n_ changing from 2.15 to 1.35. The maximum current drive is 3 MA launched form outboard side at 130 degree when _n_ =1.35 as shown in figure 11(b). 

## **5. The ramp-down scenario** 

Safe and controlled termination of burning plasma is a necessary task in the CFETR scenario design. The task of CFETR ramp-down phase is to terminate the plasma burn, exhaust the high stored plasma energy and particle, and reduce the plasma current from 10 MA to a low level (1~2 MA) while avoiding strong electromagnetic stress on the vacuum vessel. In this process, additional flux consumption and coil current should be avoided, which increases the undesirable requirement of central solenoid coil size. The vertical instability and low-density instability should be handled carefully to avoid a disruption. To achieve these goals, a controlled ramp-down is necessary. Figure 14 shows the plasma shape evolutions during the ramp-down phase. The plasma shape is well controlled and limited to the consistent divertor configuration. However, it is very challenging to maintain the strike point on the divertor target surfaces with the elongation reducing, especially when plasma current falls below 4 MA. More detailed prescriptions of the required control steps are needed to improve the strike point control in the future, and consideration of when the plasma can be limited on the wall are needed. 

For CFETR ramp-down, two schemes are present here as candidates. The first one is immediately transiting the H mode into L mode by turning down all the auxiliary heating, while another is sustaining H mode in the proper time and then transiting into L mode. The ramp-down rate is the 80 kA/s for the two cases. The plasma ramps down from 3100s to 3200s to reduce the plasma current from 10 MA to 2MA and plasma elongation from 2.0 to 1.5. 

Higher ramp rates will increase the requirement of plasma controller ability and increase li above 2. Then coil requests would become very demanding to control a plasma with such high li. The impurity fraction to the electron density is set to match the 0D Zeff. The density ramp-down is designed with the same speed as current ramping down. Lower density reduction rate may raise the ratio of the line average density to the Greenwald density ( _nGr I p_ / _a_ 2 ) close to 1, which can cause a disruption. If the density reduces quickly, the temperature may rise instead of falling in the H mode operation of ramp-down phase, which is also undesirable. Also, the low-density MHD activities like tearing modes can occur. 

Figure 15 shows the heating schemes of the two candidates in a mixed NB+EC heating scenario. Figure 16 shows the evolution of some important parameters in the two cases. In the L mode ramp-down, all the auxiliary heating systems are shut down at the beginning. Consequently, the plasma temperature and _T_ drops to low levels in 15s. After 15s, the alpha heating power reduces to zero and the ohmic heating power increases to 5 MW to sustain the plasma current and temperature. In the H-L mode transition ramp-down, the auxiliary is shutdown step by step and the confinement is still sustained in H mode. Unlike additional power being required to sustain H mode in ITER and EU DEMO ramp-down [50, 51], the original auxiliary heating system can sustain the H mode confinement for CFETR baseline case. That is because a smaller size and lower density in the CFTER baseline lead to a smaller threshold power compared to ITER and EU DEMO. The plasma temperature remains very high and contributes to effective fusion reaction. The alpha heating power remains above 20 MW for more than 40s, contributing to the H-mode sustainment while the density is still high. The entry of L mode occurs at 3160s when all the auxiliary heating is shut down and the net power is below the threshold power. The ohmic heating power just increases to 1~2 MW after entering L mode. 

The OH current increases to a big value immediately in the L mode case, while in the H-L transition case the OH current stays small until all the heating sources are shut down. Although the OH current sustained by the PF coil systems causes the increase of resistive flux consumption, no additional total flux consumption is required. The total flux consumption actually decreases because of the ramp-down of plasma current leading the external and inductive flux consumption to fall in a favorable account. Additional 14 kA/t coil current is required in CS1U coil in the L mode ramp-down at 3120s as shown in figure 16, while in H-L back transition ramp-down there is no additional coil current required. The increase of CS1U coil current is due to the feedback control of the rapid changes of plasma store energy after the H-L back transition. It might make the coil current exceed coil system’s 

limit in a faster ramp-down. 

During current ramp-down, the high central heating and the edge cooling due to radiation result in a peaked current density profile, leading to the increase of internal inductance. As shown in figure 16, the trajectories of li show that simulations with H-L back transition describe a lower li, although the li in the two cases are close near the end of ramp-down. The L-mode case has li rising faster and earlier, while in the H-L transition case li rises fast only after entering L mode at 3160s. The slow rising of li in H mode is a combination of higher edge temperature near pedestal and off-axis auxiliary heating and as well as off-axis current drives. In the beginning of ramp-down, lower li in H-L back transition case decreases the risk of vertical control lapse especially when the elongation is still large. 

The two cases of ramp-down for the CFETR baseline successfully change the plasma properties to a sufficiently low level to be shut down. The H-L back transition ramp-down is more preferred in the power transfer and coil 

current evolution as well as the li evolution. 

![](images/tmpun_my039.pdf-0029-04.png)

**Figure14.** Plasma equilibrium at four time points in the L-mode ramp-down phase. The plasma shape is limited to the divertor configuration. But the strike point is poorly controlled in the divertor region, especially at the end of ramp-down phase with very low current and high li. 

![](images/tmpun_my039.pdf-0030-00.png)

**Figure15.** Heating schemes for L-mode (a) and H-L back transition ramp-down scenarios. In the H-L back transition case, the auxiliary heating is closed step by step while keeping total net power larger than transition threshold power until 3160s. 

![](images/tmpun_my039.pdf-0031-00.png)

**Figure16.** The evolutions of OH current, _q_ 95 , density, temperature, _T_ , li, flux consumption and CS1U coil current in the L mode (red) and H-L back transition (blue) ramp-down scenarios. The total plasma current is feedback controlled to follow a prescribed trajectory. 

## **6. Conclusion and discussion** 

In this paper, the time-dependent simulations of CFETR baseline scenario for steady-state operation and relative key issues during the plasma evolution are studied. 10 MW of EC or LH is used to save the flux consumption and avoid high li during the ramp-up phase. For plasma burning phase, three heating schemes with NB+EC, NB+LH, EC+LH, respectively, are used to drive non-inductive current for steady-state operation and to modify the q profile for stable MHD activity. A reversed magnetic shear with _q_ min 2 is sustained with off-axis 

current drive and bootstrap current for all cases examined. The most harmful NTMs (2/1 and 3/2) can be avoided 

with _q_ min 2 , which is validated on many tokamak experiments[68]. Because of low _N_ , both high n ballooning mode and low n kink modes are stable in the three reference cases. Two scenarios with neutral beams reach the required fusion power of 0D CFETR phase I target, while in the LH+EC scenario the fusion power and confinement are somewhat lower without strong rotation driven by neutral beam injection. For plasma current ramp-down, both L-mode ramp-down and H-L back transition ramp-down are researched. The H-L back transition ramp-down yields better results in the power transfer and coil current evolution as well as the li evolution. However, there are still many problems for ramp-down to be addressed in the future. The optimization of ramp-down design with a higher ramp rate may be required for an emergency shutdown. Some impurity physics like accumulation and transport during the ramp-down is still not very clear, which need more experimental evidence. 

A 2D scan of NB energy and tangency radius indicate that the possible NB parameters should be inside the region of 410 _Rrt_ 660 cm and 300 _E_ 1000 keV through considerations of power deposition, current drive, torque and shine through power. Shine through problem is also researched when NB injection begins with low density. However, to quantitatively analyze the shine through density on the first wall, detailed engineering design of NB and blanket is required. The final decision of NB design depends on comprehensive considerations of all the limit, which should be a compromise of physic performance and engineering constraints. The development of negative-ion based neutral beam with high energy and long pulse duration for ITER and CFETR will help. 

EC waves at 190 GHz launched from top, LFS and midplane are studied with varying the launch angle. EC waves launched above the midplane yield a better CD efficiency than midplane, which agrees with previous work about ECCD for DEMO plasma [63]. As to the top launch, damping in the low-temperature region causes the low current drive. Overall view, the maximum on-axis CD efficiency in the region of 0.5 is 0.55 MA launched from LFS above the midplane, while the maximum off-axis CD efficiency in the region of 0.5 is 0.45 MA launched from top. A combine of top launcher and LFS launcher is an attractive tool to broaden EC current profiles as shown in the EC+LH scenario. EC waves during current ramp-up are also investigated. The overlapping of optimum regions, which yields good power deposition and current drive for both ramp-up phase and flattop phase, should be a good choice for CFETR. 

LH waves with 5 GHz is studied with varying _[n]_ ||[ and launched position. It is found that ] _[n]_ ||[ for CFETR plasma ] should be around 1.7 to penetrate inside 0.7 , which is a trade-off of penetration depth and avoiding strongly cut 

off by accessibility condition. The maximum LHCD changes from 0.9MA to 1.1 MA with 10 MW of LH power for different launcher positions. LH waves launched from HFS drive more current than that launched from LFS when _n_ || is small. In the view of the advantage of accessibility into plasma and better SOL condition, experimental demonstration of HFS launcher benefits is required to enhance our confidence in CFETR HFS launcher design. 

Demonstrating advanced divertor options for DEMO is an important part of CFETR’s scientific mission. It is necessary to check the compatibility of the simulated scenarios with the divertor power load. The heat load to divertor _Pdiv R_ in the three scenarios with NB+EC, NB+LH, EC+LH are 19.0, 18.2 and 18.7 MW/m, respectively. All of the value are larger than these from OD estimates, which is a result of higher input power required and lower impurity radiation power assumed in the 1.5D modeling. However, all the heat loads to divertor are under the 20 MW/m upper limit, which is used as an ITER design reference for conventional divertors. For the NB+EC scenario with maximum heat load, the power to divertor is ~108 MW. Base on the scaling law from Loarte’s analysis of ITPA database[69], the scrape-off layer width _q_ is ~7.9 mm. According to the simulated ITER-like divertor configuration [1], the flux expansion at the outer divertor target is ~10 and the tilt angle is 15 deg. The corresponding wetted area is ~11.1 m[2] . Assuming the outer divertor is responsible for ~80% of the total power exhaust, the heat flux to the outer divertor is ~7.8 MW/m[2] . Including the radiation in SOL with Matthews’ scaling 

law [70], the heat flux is reduced to ~5.6 MW/m[2] . More detailed calculations using multi-dimensional codes are in progress. SOLPS modelling shows that with an assumed 100 MW power into SOL in the CFETR baseline scenario, using gas puffing and advanced divertor design can drop the peak heat flux on the divertor to under 10 MW/m[2] and 

achieve detachment operation[71, 72]. For CFETR phase II with fusion power ~1 GW, detachment operation is indispensable to handle the larger power on the divertor[73, 74]. Research on controlled impurity injection and pumping for CFETR are ongoing. Consistent core-edge integrated modeling is under development to ensure the impurity does not affect core performance [41, 75]. As a test reactor, CFETR prefers grassy-ELM or ELM-free operation to reduce transient heat flux to the divertor. The way to grassy ELM will be explored in further work. 

For ITER, mature engineering designs have been settled. Some engineering constraints like coil force limit strongly limit the tokamak operation space. For CFETR, the detailed engineering design, including inside vacuum vessel components and auxiliary heating systems, is now under development. In the future, a wide range of plasma scenarios will be designed to examine the operation space of CFETR tokamak within both engineering and physics constraints. Research in progress on CFETR scenario design is playing an important role to help engineers to 

determine the final engineering design. 

## **Acknowledgements** 

This work is supported by National Magnetic Confinement Fusion Research Program of China (Grant Nos.:2014GB110000, 2014GB110003), and is performed while visiting Princeton Plasma Physics Laboratory under the support of China Scholarship Council. We would like to express our thanks to all members of the CFETR physics team. We acknowledge the Princeton Plasma Physics Laboratory for permission to use the TSC code, the General Atomics theory group for permission to use the GA code suite like ONETWO, and for their valuable technical support. Numerical computations were performed on the supercomputing system in the Supercomputing Center of University of Science and Technology of China and the cluster in the Princeton Plasma Physics Laboratory. 

## **References** 

- [1] Song Y.T., Wu S.T., et al., Ieee Transactions on Plasma Science **42** (3), 503-509 (2014). 

- [2] Wan Y.X., Li J.G., et al., Nuclear Fusion **57** (10), 102009 (2017). 

- [3] Aymar R., Barabaschi P., et al., Plasma Physics and Controlled Fusion **44** (5), 519-565 (2002). 

- [4] Wan B.N., Ding S.Y., et al., Ieee Transactions on Plasma Science **42** (3), 495-502 (2014). 

- [5] Chan V.S., Costley A.E., et al., Nuclear Fusion **55** (2), 023017 (2015). 

- [6] Shi N., Chan V.S., et al., Fusion Engineering and Design **112** , 47-52 (2016). 

- [7] Meneghini O. and Lao L., Plasma and Fusion Research **8** , 2403009-2403009 (2013). 

- [8] Chen J.L., Jian X., et al., Plasma Physics and Controlled Fusion **59** (7), 075005 (2017). 

- [9] Jian X., Chen J.L., et al., Nuclear Fusion **57** (4), 046012 (2017). 

- [10] Jardin S.C., Bell M.G., et al., Nuclear Fusion **33** (3), 371-382 (1993). 

- [11] Jardin S.C., Pomphrey N., et al., Journal of Computational Physics **66** (2), 481-507 (1986). 

- [12] Liu L., Wang M., et al., Fusion Engineering and Design **123** , 137-142 (2017). 

- [13] Wang S.J., Ye M.Y., et al., Ieee Transactions on Plasma Science **44** (9), 1745-1750 (2016). 

- [14] Ye M.Y., Wang S.J., et al., 2015 Ieee 26th Symposium on Fusion Engineering (Sofe), 1-4 (2015). 

- [15] Hemsworth R., Decamps H., et al., Nuclear Fusion **49** (4), 045006 (2009). 

- [16] Henderson M., Saibene G., et al., Physics of Plasmas **22** (2), 021808 (2015). 

- [17] Bibet P., Litaudon X., et al., Nuclear Fusion **35** (10), 1213 (1995). 

- [18] Kessel C.E., Synakowski E.J., et al., Nuclear Fusion **45** (8), 814-824 (2005). 

- [19] Guo Y., Xiao B.J., et al., Plasma Physics and Controlled Fusion **54** (8), 085022 (2012). 

- [20] Poli F.M., Kessel C.E., et al., Nuclear Fusion **54** (7), 073007 (2014). 

- [21] Kessel C.E., Campbell D., et al., Nuclear Fusion **49** (8), 085034 (2009). 

- [22] Kessel C., Batchelor D., et al., Fusion Engineering and Design (2017). 

- [23] Kim K., Im K., et al., Nuclear Fusion **55** (5), 053027 (2015). [24] Pfeiffer W., Davidson R., et al., No. GA-A-16178. General Atomic Co., San Diego, CA (USA) (1980). [25] Goldston R.J., Mccune D.C., et al., Journal of Computational Physics **43** (1), 61-78 (1981). 

- [26] Lin-Liu Y.R., Chan V.S., et al., Physics of Plasmas **10** (10), 4064-4071 (2003). 

- [27] Ignat D.W., Valeo E.J., et al., Nuclear Fusion **34** (6), 837-852 (1994). 

- [28] Liu X.F., Zheng J.X., et al., Journal of Fusion Energy **34** (6), 1438-1444 (2015). 

- [29] Imbeaux F., Citrin J., et al., Nuclear Fusion **51** (8), 083026 (2011). 

- [30] Liu L., Guo Y., et al., Nuclear Fusion **57** (6), 066033 (2017). 

- [31] Casper T.A., Meyer W.H., et al., Nuclear Fusion **51** (1), 013001 (2010). 

- [32] Voitsekhovitch I., Sips A.C.C., et al., Plasma Physics and Controlled Fusion **52** (10), 105011 (2010). 

- [33] Fietz S., Fable E., et al., Nuclear Fusion **53** (5), 053004 (2013). 

- [34] Takei N., Nakamura Y., et al., Plasma Physics and Controlled Fusion **49** (3), 335-345 (2007). 

- [35] Poli F.M., Kessel C.E., et al., Nuclear Fusion **52** (6), 063027 (2012). 

- [36] Poli F.M. and Kessel C.E., Physics of Plasmas **20** (5), 056105 (2013). 

- [37] Polevoi A.R., Loarte A., et al., Nuclear Fusion **55** (6), 063019 (2015). 

- [38] Snyder P., Wilson H., et al., Plasma Physics and Controlled Fusion **46** (5A), A131 (2004). 

- [39] Snyder P.B., Groebner R.J., et al., Nuclear Fusion **51** (10), 103016 (2011). 

- [40] Martin Y.R., Takizuka T., et al., 11th Iaea Technical Meeting on H-Mode Physics and Transport Barriers **123** , 012033 (2008). 

- [41] Shi N., Chan V.S., et al., Nuclear Fusion **57** (12), 126046 (2017). 

- [42] Sauter O., Angioni C., et al., Physics of Plasmas **6** (7), 2834-2839 (1999). 

- [43] Hirshman S.P., Physics Of Fluids **31** (10), 3150-3152 (1988). 

- [44] Ryter F., Fuchs J.C., et al., 11th Iaea Technical Meeting on H-Mode Physics and Transport Barriers **123** (1), 012035 (2008). 

- [45] Andrew Y., Biewer T.M., et al., Plasma Physics and Controlled Fusion **50** (12), 124053 (2008). 

- [46] Xiao B.J., Humphreys D.A., et al., Fusion Engineering and Design **83** (2-3), 181-187 (2008). 

- [47] Hofmann F. and Jardin S.C., Nuclear Fusion **30** (10), 2013-2022 (1990). 

- [48] Gates D., Ferron J., et al., Nuclear Fusion **46** (1), 17 (2005). 

- [49] Kessel C.E., Jardin S.C., et al., Fusion Technology **30** (2), 184-200 (1996). 

- [50] Kessel C.E., Koechl F., et al., Nuclear Fusion **55** (6), 063038 (2015). 

- [51] Vincenzi P., Ambrosino R., et al., Fusion Engineering and Design **123** , 473-476 (2017). 

- [52] Hender T.C., Wesley J.C., et al., Nuclear Fusion **47** (6), S128-S202 (2007). 

- [53] Takeji S., Tokuda S., et al., Nuclear Fusion **42** (1), 5-13 (2002). 

- [54] Huysmans G.T.A., Hender T.C., et al., Nuclear Fusion **39** (11), 1489-1507 (1999). 

- [55] Turnbull A.D., Brennan D.P., et al., Nuclear Fusion **42** (7), 917-932 (2002). 

- [56] Delucia J., Jardin S.C., et al., Journal of Computational Physics **37** (2), 183-204 (1980). 

- [57] Todd A.M.M., Manickam J., et al., Nuclear Fusion **19** (6), 743-752 (1979). 

- [58] Greene J. and Chance M., Nuclear Fusion **21** (4), 453 (1981). 

- [59] Bourliere M., Barberin J.M., et al., J Viral Hepat **9** (1), 62-70 (2002). 

- [60] Taniguchi M., Kashiwagi M., et al., Review of Scientific Instruments **83** (2), 02B121 (2012). 

- [61] Umeda N., Hiratsuka J., et al., AIP Conference Proceedings **1869** (1), 030008 (2017). 

- [62] Kessel C.E. and Poli F.M., Fusion Science and Technology **67** (1), 220-239 (2015). 

- [63] Poli E., Tardini G., et al., Nuclear Fusion **53** (1), 013011 (2012). 

- [64] Hoang G.T., Bécoulet A., et al., Nuclear Fusion **49** (7), 075001 (2009). 

- [65] Smirnov A., Harvey R., et al., Proceedings of the 15th Workshop on ECE and ECRH, 301-306 (2009). 

- [66] Golant V.E., Plasma penetration near the lower hybrid frequency, Ioffe Inst. of Physics and Tech., Leningrad (1972). 

- [67] Wallace G.M., Baek S.G., et al., Radiofrequency Power in Plasmas **1689** (1), 030017 (2015). 

- [68] Maraschek M., Nuclear Fusion **52** (7), 074007 (2012). 

- [69] Loarte A., Lipschultz B., et al., Nuclear Fusion **47** (6), S203 (2007). 

- [70] Matthews G., Allen S., et al., Journal of Nuclear Materials **241** , 450-455 (1997). 

- [71] Mao S., Guo Y., et al., Journal of Nuclear Materials **463** , 1233-1237 (2015). 

- [72] Chen B., Mao S., et al., Proceedings of ICONE-23, ICONE23-1882 (2015). 

- [73] Zhou Y., Mao S., et al., Fusion Engineering and Design (2018). 

- [74] Liu X., Li G., et al., Ieee Transactions on Plasma Science (2017). 

- [75] Xu G., Zhou Y., et al., Ieee Transactions on Plasma Science (2018). 

