---
source: "chislett2022.pdf"
source_type: "local_file"
extracted_at: "2026-09-29T23:22:15.364904+00:00"
content_hash_sha256: "9bb092e6a9576f45aebc30f95b5f734c941241705fff2e6cf5df499c33288810"
backend: "pdf_pipeline"
---

# **Training and Upgrading Tokamak Power Plants with Remountable Superconducting Magnets** 

**S. B. L. Chislett-McDonald**[1] **, E. Surrey**[2] **, J. Naish**[2] **, A. Turner**[2] **and D. P. Hampshire**[1] 

> 1Superconductivity Group, Centre for Materials Physics, Department of Physics, Durham University, UK 

> 2Culham Centre for Fusion Energy, Culham Science Centre, Abingdon, UK 

E-mail: `simon.chislett-mcdonald@durham.ac.uk` 

## **Abstract.** 

All high field superconductors producing magnetic fields above 12 T are brittle. Nevertheless, they will probably be the materials of choice in commercial tokamaks because the fusion power density in a tokamak scales as the fourth power of magnetic field. Here we propose using robust, ductile superconductors during the reactor commissioning phase in order to avoid brittle magnet failure while operational safety margins are being established. Here we use the `PROCESS` systems code to inform development strategy and to provide detailed capital-cost-minimised tokamak power plant designs. We propose building a ‘demonstrator’ tokamak with an electric power output of 100 MWe, a plasma fusion gain _Q_ plasma = 17, a net gain _Q_ net = 1.3, a cost of electricity (COE) of $ 1148 (2021 US) per MW h (at 75 % availability) and high temperature superconducting operational TF magnets producing 5.4 T on-axis and 12.5 T peak-field. It uses Nb-Ti training magnets and will cost about $ 9.75 Bn (2021 US). An equivalent 500 MWe plant has a COE of $ 608 per MW suggesting that large tokamaks may eventually dominate the commercial market. We consider a range of designs optimised for capital cost (as the reactors considered are pilot plants) consisting of both 100 MWe and 500 MWe plants with each of two approaches for the magnets: training and upgrading. With training magnets, the plant is cost-optimised for REBCO TF magnets. For a 100 MWe plant, the Nb-Ti training magnets typically produce 70 % peak field on the toroidal field coils compared to REBCO magnets, 65 % peak field on the central solenoid and cost _≈_ 10 % of the total machine cost. Training magnets could in principle be reused for each of say 10 subsequent (commercial) machines and hence at 1 % bring only marginal additional cost. With upgrade magnets the plant is more expensive - first it is cost-optimised for Nb-Ti and then upgraded to REBCO coils. The upgrade increases the net electrical output from 100 to 280 MWe with an _≈_ 25 % increase in reactor capital cost. We also evaluate likely advances in fusion technology and find that technologies on the horizon will probably not bring further large reductions in capital cost, and that REBCO magnets are generally stress-limited rather than current density limited. We conclude that: the fusion community should develop high _Bc_ 2 alloys specifically for fusion applications; superconductors should be tested under operational-like radiation at cryogenic temperatures; and that we should proceed now with detailed design and construction of a prototype fusion power plant that integrates and de-risks all the key technologies including high temperature superconducting cables and joints using remountable training magnets, and hence is the last tokamak before commercialisation of fusion energy. 

_Keywords_ : Tokamak Pilot Plant, Fusion power, Remountable Magnets, REBCO 

## **1. Introduction** 

High temperature superconducting REBCO (Rare-Earth barium copper oxide) materials and the low temperature superconductor Nb3Sn are the candidate high field materials for the toroidal field (TF) and central solenoid (CS) coils for fusion reactors. The ITER [1] and SPARC [2] reactors use these materials and are expected to operate with fusion plasma gain _Q_ plasma _≈_ 10, as will pilot fusion power plants that will eventually generate 100s MW net electricity (MWe) (e.g. EU-DEMO [3], STEP [4], ARC [5]). During the commissioning phase after construction, in addition to the high stresses that occur in magnets during standard operation, unexpected powerful disruptions can also occur in the plasma such as vertical displacement events and associated halo currents. In the JET reactor, such uncontrolled events induce forces of order 4 MN, that have lifted the entire vessel by 9 mm [6, 7]. These disruptions are expected to be an order of magnitude greater in ITER [8]. More than half of all unintentional disruptions in JET were not due to physics instabilities, but were attributed to, for example, failure of one of the sub-systems, control errors or human error. Fewer disruptions predominantly followed better technical operation of JET [9]. In short, operating a tokamak properly requires completion of a ‘learning curve’ that does not require full plasma power operation [9]. These uncontrolled events would bring with them the risk of permanent and irreparable damage to a tokamak including the expensive brittle superconducting magnets. In ITER, were a TF coil failure to occur before nuclear operation starts, one can reasonably expect it to take 4 years to replace the coil (using an available spare) [10]. Once nuclear (i.e. D-T) operation has begun, the activation in the reactor vessel would be so high that, given there is no robotic control of magnet replacement, it would probably not be cost-effective to replace a TF coil [11]. Unfortunately all the very high field superconductors that we need in full operation for optimal (profitable) commercial fusion are brittle, and the largest Nb3Sn fusion magnets ever produced to-date (by size or weight) were resistive when first turned on [12]. In this paper, we propose using Nb-Ti during the critical commissioning and testing phase because although it has poorer high field performance, it is ductile and so is robust against mechanical or brittle failure. 

There are a number of road-maps [3, 13, 14] that focus on achieving a final build machine. It is now understood that both climate change and commercial imperatives mean that one simply can’t wait 15 years to further optimise plasma performance [15]. Indeed U.N. Secretary-General Ant´onio Guterres described the recent UN IPCC (United Nations Intergovernmental Panel for Climate Change) report as a “code red” for humanity [16]. Here, we recommend starting with lower risk machines with remountable magnets that eventually have components that are exchanged for higher-risk higherperformance components only when they are needed [17]. We calculate the cost of building various tokamak designs using the `PROCESS` systems code [18, 19, 20] and 

specify a commissioning roll-out that helps avoid single-point failure (and while high temperature superconducting cables are improved and made cheaper). We use an approach that takes advantage of new advances (e.g. if new higher field ductile superconductors are developed), so that the expensive and time-consuming tokamak recommended for construction still correctly identifies and de-risks the best available commercial solution. More specifically, in this paper we have considered swapping superconductors using two approaches: training and upgrading and have assumed that all magnets will be fully remountable. With training magnets, the plant is cost-optimised for full power operation with REBCO but trained first using commercial Nb-Ti TF and CS coils (for all tokamaks in this work with REBCO, Nb3Sn and commercial Nb-Ti TF and CS coils, commercial Nb-Ti is used for the PF coils; for all tokamaks in this work with quaternary Nb-Ti TF and CS coils, quaternary Nb-Ti is used for the PF coils). With the (more expensive) upgrading magnets approach, the plant is cost-optimised for Nb-Ti and then upgraded to REBCO coils. We have used `PROCESS` to find optimal designs, defined in all cases to minimise plant capital cost. `PROCESS` reports costs in 1990 US $, to convert to 2021 costs we have used CPI inflation [21, 22, 23] resulting in a conversion factor of 1 US $ 1990 = 2.13 $ in 2021. An alternative is the IHS-CERA index for nuclear fission power plant costs [24]. The index data were collected between 2000 and 2017, we therefore use the consumer price index (CPI) to extrapolate from the IHS-CERA index to 1990 and 2021. Using this metric, 1 US $ 1990 = 3.28 $ in 2021 (when spent in the nuclear power sector). One must therefore take care when converting to today’s costs as they can vary significantly depending on the choice of index. 

For each of the reactor training and upgrading approaches, we have considered three power plant designs which gives us six baseline tokamaks. In each approach two tokamaks produce 100 MWe and are designed for H98 = 1.2 and 1.6 (to encompass future advances) and the third produces 500 MWe and is designed for H98 = 1.2. For each of these six baseline designs we have then investigated swapping superconductors out whilst maintaining the baseline reactors’ architectures. Table 1 shows the key design and performance parameters for the six baseline tokamaks (including our preferred choice for build - a 100 MWe, H98 = 1.2, pilot power plant optimised for REBCO), together with the most important tokamaks that operated, are operating or are planned. Here we use the term ’demonstrator’ for those tokamaks that are intended to be a last tokamak before commercialisation, and therefore de-risk all the key technologies. Important issues concerning remote handling and remountable coils are considered in section 2. Section 3 details the reactor design choices associated with considerations of plasma physics and engineering design. The design of optimised radiation shield used for all reactor designs is described in section 4 using detailed `MCNP` [25] calculations. In section 5 we describe the cost models for current superconductors and the impact of future developments. Our preferred reactor design, the other five capital-cost-minimised reactor designs and the performance of all swapped superconducting magnets for each design are presented in section 6. Future developments of decreased REBCO cost and increased steel yield stresses on our preferred reactor design (as a proxy for both improved materials and 

better magnet design) are discussed in section 7. The range of tokamaks and preferred choice is discussed in section 8. Finally we summarise the most important results in section 9. 

## **2. Robotics, Remountable Magnets and Joints** 

In high aspect ratio reactors of the type considered here (similar to ITER and EUDEMO), robotics/crane systems can in principle be employed to extract the remountable CS and TF coils if they become damaged because they see little neutron flux due to thick radiation shielding (for example most EU-DEMO coils will be considered NonActive-Waste at end of life [26, 11, 27]). The requirements on remote handling (RH) for coils alone, are therefore not particularly demanding in the designs considered in this paper. However, maintenance of the first wall, blanket and the other internal reactor components will be extremely challenging due to the high radiation levels of order 100 - 600 GBq kg _[−]_[1] remaining 4 weeks after shutdown [26], similar to those found in the core container of a fission reactor 8 years after shutdown [28]. Specialised radiation hardened RH systems as found in EU-DEMO’s internal RH system [29, 30] will be required and have not been included in the costs (for replacing a damaged irradiated magnet) in this paper. The economic damage of a damaged or destroyed non-remoutable magnet would be unjustifiable: it would put a power plant out of action for years. This risk is simply unacceptable for a commercial plant, and is the reason why (in the author’s opinion) “life-time component” magnets will not be permitted in future reactors. Commercial reactors will require availabilities as large as possible (70% or higher). Magnet failure forces the reactor to shut down, and repairs and replacements must be made as swiftly as possible. Remountable magnets and joints will be required to enable magnet replacement without having to cut open the vacuum vessel and the shielding (using for example a ‘half-phi’ design [31]). Only the coils themselves would have to be taken apart (with careful engineering and masterful crane/robotics operation). This is as opposed to existing machines in which an entire reactor section must be removed (including components internal to the magnets) for the magnets themselves to then be removed. Remountable joints for both low temperature superconductors [32] and high temperature superconductors [5, 33, 34, 35] have been designed, though to-date none have been incorporated into working tokamaks. Indeed there is no published work (at time of writing) demonstrating full-scale remountable joints. There have been preliminary works on cable-to-cable remountable joints [36, 37] and there are no reasons why such joints couldn’t simply be scaled to a full winding pack [38]. With concentrated effort however, we are confident that full-scale, reactor ready remountable joints are feasible by 20352040: non-remountable joints in superconducting magnets are commonplace in largescale magnets; multiple institutions are working together and competitively to build them [36, 38, 37]; remountable joints are already present in resistive magnet tokamaks e.g. MAST-U. Remountable joints introduce additional thermal load on the reactor cryo-system, though the required wall plug cryoplant power to manage this is _≈_ 1 MW 

[5] (though, of course, dependent on the specifics of the magnet system) and has been omitted from the `PROCESS` calculations here as it is small compared to the pre-existing power demand for cooling of order 40 - 50 MWe. For example, soldered REBCO joints have resistances of _≈_ 50 nΩcm _[−]_[2] [39], which for an ITER TF coil system gives a total thermal load of _≈_ 600 W and a power demand for additional cooling that is only about 1 % of the total. 

In the current final development phase for commercial fusion, one would not want to use brittle REBCO magnets in the commissioning phase for the reactor when the risk of damaging the magnets is not well-known. Indeed, operating with Nb-Ti training magnets may be required as part of regulatory licensing of the construction prior to operation [40]. After the reactor has operated successfully for several years and completed all its commercial requirements, in the post-demonstrator research reactor phase one may reuse the Nb-Ti magnets as part of trialling new technologies and component designs, because the risk of disruptions during such trials may again be high. 

## **3. Reactor Design Choices** 

In this section, we consider the most important technological areas of tokamak development. We describe the choices and constraints that affect the design and costminimisation we have made in each area, explaining the reasoning for our choices. 

## _3.1. Plasma Operation_ 

_3.1.1. Confinement Time and H98-factor_ We have considered H98 = 1.2 as the most likely performance but have also considered the much higher value of H98 = 1.6 to quantify the possible effects on costs in future from new advanced tokamak designs such as spherical tokamaks [41]. H98-factor refers to the ratio between observed plasma energy confinement time, _τ_ E, and the _τ_ E[IPB98(y,2)] predicted by the ITER Physics Basis ELMy H-mode IPB98(y,2) scaling law [42] which is derived from a vast range of tokamaks. A subset of these data are shown in figure 1. Taking a subset of the IPB98(y,2) data for different reactor geometries can also yield quite different scaling laws and H98-factors. For example, confinement times of spherical tokamaks appear to have much stronger field dependence [43, 44, 45] than the standard _τ_ E[IPB98(y,2)] _∝ B_ T[0.15] e.g. _τ_ E[MAST] _∝ B_ T[1.4] in MAST [46]. Extrapolating this to stronger magnetic fields can result in H98-factors upward of H98 = 2.0. It is however not clear whether this strong field dependence extrapolates to power plant conditions. The field dependence is linked to strong _τ_ E scaling with plasma collisionality, _ν∗_ , which itself depends on absolute _ν∗_ [47]: at lower _ν∗_ the confinement time scaling with _ν∗_ is reduced. Therefore in higher field tokamaks with reduced _ν∗_ ( _whichis ∝ B_ T[-4][)][it][is][unlikely][that][the][strong][field][dependence][will] remain. Although ITER is nominally designed with H98 = 1.0, H98 _>_ 1.0 has been observed in a number of existing tokamaks, e.g. DIII-D [48]. Indeed ITER is expected 

to reach H98 = 1.57 in reversed-shear operation and H98 = 1.2 in hybrid operation [49]. 

_3.1.2. Density, β and Safety Factor_ We have chosen a maximum Greenwald fraction at the plasma edge of _fGW[edge]_[=][0.67][and][a][peaked][density][profile][such][that] _[f] GW[ line][−][avg]_ = 1.1. The minimum plasma safety factor at the 95 % poloidal flux surface was set to _q_ 95 = 3.45. The normalised thermal beta, _β_ N _≈_ 2.49 for all reactors. These safety limit choices broadly follow the ARC and SPARC philosophies which have ( _fGW[edge]_[=][0.67,] _[q]_[95] = 7.2 and _β_ N = 2.59 [50] and _fGW[edge]_[=][0.37,] _[q]_[95][=][3.4][and] _[β]_[N][=][1][[2],][respectively)] rather than the EU-DEMO philosophy which will operate closer to stability limits (with _fGW[edge]_[=][0.8,] _[q]_[95][=][3.25,][and] _[β]_[N][=][2.50][[3]).][We][use][the][familiar][expressions][for][fusion] plasma power [51]: _P_ plasma _∝ β_ N[2] _[B]_ axis[4] _[R]_[3] _[/q]_[2] _[A]_[4][(] _[B]_[axis][is][the][magnetic][field][on][the][axis] of the plasma), and safety factor _q ∝ RB_ axis _/A_[2] _I_ P (for a fixed shaping factor); for a reactor design point with fixed _P_ plasma: _β_ N _∝_ 1 _/I_ P _B_ axis _√R_ . Thus going to even higher fields reduces _β_ N. _q_ also scales positively with _B_ plasma, so larger fields would reduce further the probability of kink disruptions. In addition, _I_ P can be increased in tandem with _B_ plasma, increasing achievable plasma density (as the limiting density _nG_ = _I_ P _/πa_[2] ) whilst maintaining high _q_ and further reducing _βN_ . Our calculations show that had we used the higher risk EU-DEMO safety limits for our preferred reactor, it doesn’t change things very markedly. The capital cost decreases by 7.9 %, it decreases the major radius by 4.3 %, decreases the plasma current by 12.0 % and increases the field on plasma by 6.1 %. 

## _3.2. Superconductor Operating Temperature_ 

We have chosen 4.5 K as the operating temperature for all superconducting magnets. All of the reactors in this work use Nb-Ti TF and CS coils at some point during their lifetime, so the cryosystem must be able to cool the magnets to this temperature. Of course, the Nb-Ti training coils (mentioned below) need liquid-helium temperature operation. Even if a REBCO reactor could eventually be operated at 20 K, `PROCESS` shows our preferred choice reactor operating at 4.5 K actually has a net capital cost _≈_ 150 M$ lower than at 20 K (as explained below). For the preferred reactor, the cryogenic cost is 89 kW (compared to the 75 kW cryogenic requirement of ITER [52]). 

Table 2 shows the capital cost of our preferred REBCO plant operating at 4.5 K including the combined TF (130 M$) and CS coils’ (20 M$) cable cost also at 150 M$. Also shown are data for plants where Nb3Sn and Nb-Ti has been used as the superconductor in the highest field regions of the plant. Equivalent reactor power balances are shown in table 3. Given the plant with Nb3Sn TF and CS coils is more expensive than the REBCO-based plant (and still made from brittle material) we have not considered it further in this paper. If operation were at 20 K REBCO’s critical current density is _≈_ 1.7 _×_ lower, which demands larger coils and a larger overall reactor volume, increasing direct costs by 84 M$. On the other hand, modern cryoplant efficiency scales with temperature roughly as the ideal Carnot cycle (with a 

base temperature of about 2 K) [53]. 

The direct capital cost of cryoplant scales approximately linearly with cooling power and would be reduced from 88 $M (as shown in table 2) to 20 $M. Operation at 20 K does have the advantage of better REBCO quench mitigation due to the _≈_ 3 _._ 0 _×_ greater thermal conductivity and _≈_ 60 _×_ greater specific heat of RRR = 100 copper at 20 K than at 4.5 K [54]. Though, we expect that with rather modest advances in quench detection and mitigation technologies (e.g. LTS for HTS quench detection [55], acoustic MEMS [56], stray capacitance change monitoring [57]) operation at 4.5 K using REBCO will be straightforward in future. 

## _3.3. Tritium Breeding_ 

The blanket design in all reactors in this work based on the helium-cooled pebble bed (HCPB) [58] which has greatest breeding potential of the blanket designs under investigation for EU-DEMO [59]. We have required the minimum tritium breeding ratio (TBR) to be 1.1 in all reactors. The TBR was set using the in-built `PROCESS` breeder ratios for given breeder blanket thicknesses as calculated by the `FATI` (Fusion Activation and Transport Interface) code [60] for EU-DEMO (to which our designs are similar, to first order, so the model is applicable here). Tritium self sufficiency is required as current tritium supplies could not maintain multiple pilot plant reactors [61]. The TBR cannot be too large, as to avoid an excessive tritium inventory and issues of tritium permeation throughout the reactor. TBR = 1.1 is the widely accepted ratio for a power plant: “enough but not too much”. 

If the global tritium inventory were markedly increased, a cheaper pilot plant could be built with a lower TBR = 0.9 [13]. Our detailed `MCNP` (Monte Carlo N-Particle) calculations shows that the 0.53 m thick blanket and 0.25 m thick radiation shield in our preferred reactor each reduce the neutron flux by roughly two or three orders of magnitude (considered below in section 4 and figure 5). A TBR of only 0.9 can therefore be generated with a smaller inboard blanket of _≈_ 0.20 m and outboard blanket of _≈_ 0.35 m only. However, to maintain the same nuclear heating in the magnets, the radiation shield would need to be thicker by _≈_ 0.17 m leading to a net reduction in capital cost of _≈_ 24 %. The first wall blanket and shield in this case are 70 cm thick in total. This is a very significant reduction (discussed in Section 7.4), but we decided in the end not to pursue it, since although such an approach would still demonstrate (some) tritium breeding, it would be at the cost of losing tritium self-sufficiency (which may unacceptable to investors). 

Other breeding blankets are being developed: A water-cooled lithium lead blanket (WCLL) design [62, 63] is under consideration for EU-DEMO. The WCLL provides greater radiation shielding than the HCPB (due to neutron capture by the water coolant) whereas the latter has greater breeding potential (due to the inclusion of Be neutron multiplier modules). Other helium-cooled and dual-cooled lithium lead concepts are also under consideration [59]. A FLiBe molten salt blanket is being developed in the USA 

which includes a coolant outlet temperature of up to 930 _[◦]_ C [5], higher than either the HCPB (650 _[◦]_ C) or WCLL (330 _[◦]_ C) and may therefore eventually lead to more efficient electricity production. This higher temperature would however require the use of novel, low activation structural materials, EUROfer is limited to 550 _[◦]_ C [64]. 

## _3.4. Reactor Architecture_ 

_3.4.1. Divertor Constraints and Configuration_ The divertor architecture in all the simulated reactors here is based on the single-null ITER design [65] [66], which is currently the baseline option considered for EU-DEMO [3]. The steady-state heat flux onto the divertor was required to be _<_ 6 MW/m[2] , below the maximum steady-state heat flux of _≈_ 10 MW/m[2] expected in ITER [65]. This is a conservative constraint, manageable with techniques such as divertor impurity seeding (e.g. in EAST which maintains high H98 [67]) or moving the divertor strike points (e.g. in SPARC [2]).In our `PROCESS` simulations we have allowed the argon impurity fraction to vary, to facilitate reduced power to the divertor through argon ionisation and bremsstrahlung. Other advanced techniques developed for much smaller machines with much higher fluxes are also potentially available including long legged [68, 69] or snowflake divertors [70] but they require additional plasma shaping coils which are exposed to large neutron fluxes, or raise demands (and costs) on the existing coil system [71, 72] (e.g. in ITER, the current through the upper-most and lower-most solenoid modules would have to be increased by more than factor 10 [73] in order to produce a snowflake). In the large, capital-cost minimised machines considered the primary limiting factor preventing smaller sized reactors was the yield stress of the magnet support structural material rather than the heat flux to the divertor; theses divertor configurations were therefore not needed. A hard limit of _P_ separatrix _/R_ major = 20 MW/m[-1] was set, similar to the values of _P_ separatrix _/R_ major = 17 and 30 MW/m[-1] expected for EU-DEMO and J-DEMO respectively [74]. We found that increasing the _P_ separatrix _/R_ major limit had negligible effect on our cost-optimal designs because they are predominantly magnet stress-limited. 

_3.4.2. Number of Toroidal Field Coils_ All reactors in this work have 18 toroidal field coils and a maximum field ripple at the plasma outboard mid-plane of 6 % (in following with EU-DEMO designs). Ripple cannot be avoided, but must be kept low in order to reduce ripple-induced drift of trapped particles and associated energy losses [75]. `PROCESS` runs were performed to ascertain the cost-optimal number of coils for each baseline reactor run in this work. In all cases 18 was the optimum number. The difference in total capital cost between a given reactor with 18 or 20 TF coils was typically quite small: for the preferred reactor the difference was only 0.3 %. Having a greater number of coils reduces the peak field that each coil must produce (due to the coils be closer together, and the field between them ‘dipping’ less), thereby slightly reducing the coil size and overall reactor volume. Each added coil however increases the cost of the magnet system. 

_3.4.3. Coil Structural Support_ The maximum allowable shear stress (used for the Tresca yield criterion in `PROCESS` ) was set to 660 MPa for both the CS and TF coils. This is 2/3 of the yield stress of standard fusion relevant, high strength structural steels [76]. A bucked and wedged (B&W) coil support structure [77, 78] has been incorporated in all reactors studied here. Performing dedicated `PROCESS` runs, we found that a B&W support structure reduces our preferred reactor’s CS coil bore by 13.7 % (27.9 cm), TF coil thickness by 13.4 % (10.9 cm) major radius by 5.6 % (40.7 cm) and capital cost by 400 M$ compared to a conventional wedged support structure that mechanically isolates the TF coils from the CS coil (as in ITER [1]). In the B&W support structure, stresses are shared throughout the whole support structure, rather than constrained to the supports of individual coils, reducing the size of the steel support structure required. The TF coils are wedged in a circular vault which bucks onto a low-friction bucking cylinder which itself is in contact with the central solenoid. Such an architecture does however require the use of a bespoke low-friction interfacial material [77] and comes at the cost of reduced plasma shaping flexibility, and additional cyclic loading on the TF coils [79] which reduce the fatigue-limited lifetime of the TF coil casing and has not been accounted for in our calculations. 

The `PROCESS` stress model is 1-D and only calculates the stress at the inboard midplane, from the inner edge of the CS coil to the outer edge of the TF coils. It does not take into account stress peaking along the circumference of a TF coil (due to say toppling forces from interaction with the fields from the PF coils) or within the winding pack. Results are generally consistent with finite element analysis [80]. 

_3.4.4. Central Solenoid Use and Burn Time_ We have chosen to include both a central solenoid coil and auxiliary heating system for current drive, start-up and plasma heating. To minimise the size of the central solenoid coil, a large 50 MW ECRH auxiliary heating current drive was used. This ECRH power follows EU-DEMO [3], which would make it the largest ever built. It would limit any further reduction in the blanket volume (as auxiliary heating systems take up valuable first wall surface area) and hence the tritium breeding ratio and electricity generated. The 50 MW ECR system is expected to produce 10 – 15 % of the plasma current (which has been included in the calculations). It was taken to have a power conversion efficiency _µ_ CD,conv = 0.4, and normalised current drive efficiency of _γ_ CD = 0.3 - taken from the `PROCESS` EU-DEMO 2018 baseline values and slightly more conservative than assumed for EU-DEMO [81]. `PROCESS` was then given freedom to vary the inductive and non-inductive current fractions and yielded an _≈_ inductive (CS and PF coil driven) current fraction of 50 % (the exact fractions depend on the reactor in question) and a bootstrap current fraction of _≈_ 40 %. The CS and PF systems produced _≈_ half of the total magnetic flux each at all times. 

A number of novel plasma start-up techniques have been developed that could in principle reduce the demand on the CS coil, and therefore reduce its size and cost. Helicity injection is a promising family of technologies and have seen implementation in a number of smaller tokamaks [82]. The most powerful system under construction 

is NSTX-U [83] which is predicted to produce _>_ 400 kA. Merging compression (MC) has seen some success in spherical tokamaks [84, 85, 86] and is expected to be used in Tokamak Energy’s ST-40 reactor [87] and produce a 2 MA current. To date MC magnets have been inside the vacuum vessel which brings with it huge neutron fluxes and the requirement for frequent replacement, reducing reactor availability. Designs that improve the location of the MC magnets will be developed, but we consider this approach too high risk just now. Up to 200 kA current has also been achieved inductively using the PF coil systems in JT60-U (with supplementation from the lower hybrid current drive system) with 1.9 Wb flux [88], but higher currents must be demonstrated before this technique becomes a practical solution for reactors of the scale considered in this work at this time. 

A radio frequency (RF) current drive was chosen for the auxiliary current drive system as it is cheaper, requires less radiation shielding, and consumes a smaller blanket volume than the alternative neutral beam injection system [89] [90]. In principle the ECR system could be exchanged for a different 50 MW RF current drive option without changing the overall reactor design should ion cyclotron or lower hybrid current drive systems prove more efficient or reliable in future. For an EU-DEMO-like reactor, at present ECR has the most flexible power deposition which gives the highest current drive efficiency [81]. 

For both the 100 MWe and 500 MWe reactors considered here, the capital cost is not very sensitive to burn-time so we have chosen to adopt the EU-DEMO standard of 2 hours [3]. The variation in the cost-optimal central solenoid bore, thickness and flux generation as a figure of required plasma burn time and resulting reactor capital cost are shown in figure 2. 

## **4. An Optimised Radiation Shield Thickness** 

In this section we optimise the thickness of the radiation shield. A thinner shield is cheaper and enables more compact reactor designs. However, the shield must be thick enough for both the lifetime of the tokamak to be sufficiently long, and the cryogenic load to be sufficiently small. We start by using state-of-the-art `MCNP` [25] calculations for the neutron flux spectrum at the first wall for a cost-optimised, H98 = 1.2, 100 MW REBCO CS and TF and Nb-Ti PF tokamak. We assume that the neutron flux predominantly determines lifetime limit for superconducting materials and hence can be used as a proxy for both the neutron and gamma flux. Then we use `MCNP` attenuation coefficients derived for neutron flux attenuation through slab geometries, to provide empirical attenuation coefficients for what we call in this paper benchmarking calculations. We have used them here to calculate the lifetime and cryogenic load for a range of simplified tokamak designs using different radiation shield thicknesses. These quick calculations provide a broad view of how changes in the component parts and size of the shield affects the tokamak’s performance. Then we progressed to larger `MCNP` [25] calculations that included the full complexity of the tokamak geometry and both the photon and neutron 

flux, and optimised the radiation shield thickness more accurately. This finalised the shield thickness of our preferred tokamak. We go on to use the properties for the optimised shield in our cryogenics analysis of the helium coolant mass flow rate required, and in all our subsequent power plant simulations. 

## _4.1. Neutronics - Thermal Load and Lifetime_ 

_4.1.1. Benchmarking Calculations_ The incident neutron flux density spectrum at the first wall (FW) for our preferred cost-optimised REBCO tokamak _I_ FW,RT( _E_ ) (n cm _[−]_[2] s _[−]_[1] ) was calculated using `MCNP` in terms of _i_ different energy bins of width _dEi_ and average energy _Ei_ (and the 175 Vitamin-J energy bin width size distribution [91] - a choice which does not significantly affect any results in this paper). For all other tokamaks under consideration, the flux density in any _i_ th energy bin was then simply given by 

![](images/chislett2022.pdf-0011-05.png)

where the flux density has simply been scaled by ratio of the total fusion power of the tokamak under consideration to the total fusion power of the preferred cost-optimised REBCO tokamak _PTotal/PRT_ . The empirical attenuation coefficients used were those calculated using `MCNP` for neutron transmission through 30 cm blocks of mono-material [92] and averaged for all fast neutron flux ( _E >_ 0 _._ 1MeV). This approach ignores the complexity of the multiple nuclear interactions (discussed below) and simply associates the reduction in energy and flux with a single attenuation coefficient. Table 4 lists the empirical values for the attenuation coefficients as well as those derived using standard total nuclear cross sections for comparison. We then take the thermal load onto the TF coils after passing through all the walls (the first wall, blanket, radiation shield, vacuum vessel and thermal shield) to be 

![](images/chislett2022.pdf-0011-07.png)

where _A_ is the surface area of the first wall. We have introduced two geometrical factors: _g_ which accounts for only a fraction of the flux reaching the cryogenic system where _g_ = ( _Rmajor − Rminor_ ) _/Rmajor_ (i.e. the cryogenic system unlike say the shielding, does not cover the entire surface of the toroid), and _a_ which accounts for the volume of a curved surface being smaller (and therefore attenuating less on the inner leg of the important TF coils) than a slab where _a_ = 1 _− tAll Walls/_ 2 _.rAll Walls_ . For the preferred reactor, _Rmajor_ = 6 _._ 75 m and _Rminor_ = 2 _._ 14 m (cf Table 1). Also _tAll Walls_ = 1 _._ 238 m taken for the first wall, breeder blanket, radiation shield and vacuum vessel given in Table 5 and _rAll Walls_ = 3 _._ 383 m from Figure 3, so _g_ = 0 _._ 682 and _a_ = 0 _._ 817. Because these corrections appear in exponential functions, they significantly improve the 

agreement between the benchmarking calculations and the `MCNP` calculations provided below. 

To calculate the lifetime of the tokamak, we note that neutron flux density initially increases _J_ c in superconductors, due to an increase in the density of flux pinning sites [93], but eventually causes a sharp irreversible decrease after a fluence of _≈_ 3 _._ 9 _×_ 10[22] fast neutrons m _[−]_[2] , for _Eneutron >_ 0 _._ 1 MeV . We have used this fluence threshold (aka the Weber dose limit [94]) to calculate the magnet lifetime of the toroidal field (TF) coils _τ_ TF (s), where 

![](images/chislett2022.pdf-0012-04.png)

To validate these benchmarking calculations, we first input the radial build dimensions and fusion plasma power for ITER [1] and compare the values obtained to more detailed neutronics calculations [95]. With _PITER,plasma_ = 500 MW, a first wall surface area of 610 m[2] , _RITER,major_ = 6 _._ 20 m, _RITER,minor_ = 2 _._ 00 m, _tITER,All Walls_ = 0 _._ 808 m and _rAll Walls_ = 3 _._ 817 m (as shown in Table 1), our benchmarking calculations yield a TF coil nuclear heating of 32.8 kW, within just a factor of two of the expected range of 14 - 18 kW [95] (The calculated magnet lifetime for ITER is 23.6 full-power years). Given the agreement, we then changed the radiation shield to be tungsten carbide and used `PROCESS` to vary the thickness of the components of the radial build and found the first approximate design of the preferred tokamak (the data for this initial design are listed in table 5). Having found the first approximate design for the preferred tokamak, `MCNP` was then used to finalise the radiation shield thickness. 

_4.1.2._ _`MCNP` Calculation_ The `MCNP` code is a dedicated numerical solver that considers the progressive creation and loss of approximately 4000 isotopes, via decay and nuclear reactions. These calculations include the complexity of considering flux in all directions, and the specific geometry of the component structures of the tokamak [96, 97]. It is used here to calculate the changes in the neutron flux and gamma flux as they pass through the component walls and magnets of the tokamak. The calculations do not include changes in composition or microstructure that affect mechanical properties, such as embrittlement or swelling [98, 99], nor do they include changes in transport properties, such as thermal or electrical conductivity [100], or magnetic properties. Having used the benchmarking calculations to identify the first approximate optimal design for a cost-optimised REBCO tokamak, we repeated the nuclear heating and superconductor lifetime calculations using `MCNP` near the optimal shield design. The space for the tungsten carbide radiation shield was set as a 30 cm block and split into six, 5 cm thick sections. The sections were successively set as void regions starting from the plasma facing side, and the neutron and photon flux density spectra were calculated for materials throughout the entire tokamak together with the lifetime and cryogenic load on the TF coil system, as shown in figure 4. Also shown are equivalent benchmarking values. The `MCNP` calculated lifetimes and TF coil nuclear heating as a function of shield 

thickness are _≈_ 3-4 _×_ and _≈_ 4 _×_ lower than the corresponding benchmarking values for a given radiation shield thickness. Further corrections can be added to the benchmarking calculations by accounting for the higher _>_ 10 MeV neutron flux and lower 0 _._ 1 _−_ 10 MeV neutron flux at the magnets, than `MCNP` calculations give, and which lead to the total fast neutron flux being a little lower (resulting in a longer superconductor lifetime) and the total power deposited in the magnets being a little larger (resulting in a larger nuclear heating). 

The neutron and photon spectra as a function of depth into the reactor wall at the inboard mid-plane are shown in figure 5. The data are presented as flux density per unit lethargy (i.e. flux density in the _i_ th bin, divided by the _i_ th energy bin width, and multiplied by the average energy in the bin) versus energy. This form is independent of the details of how the bins are discretised and enables direct comparison with for example Weber [94] who finds a peak value of _≈_ 4 _×_ 10[12] n m _[−]_[2] s _[−]_[1] at the magnet location, that is similar to the peak flux of 2 _._ 3 _×_ 10[12] n m _[−]_[2] s _[−]_[1] incident on the TF coils shown in figure 5. We note that the gamma flux is generally lower than the neutron flux although to our knowledge there are no reports of how this may affect the lifetime of the superconductors (cf Section 5.6). Neutron and photon (power) wall loading are shown in figure 6. 

The optimal tungsten carbide radiation shielding thickness was calculated using `MCNP` to be 24.5 cm, based on a 40 year superconductor lifetime criterion. With this shield the combined nuclear heating on the TF coils was very low, only _≈_ 1.4 kW. We note that if we had chosen to reduce the lifetime to just 3 years, the shielding would have reduced to 9.8 cm, but at the price of the nuclear heating increasing to a large value of 17.2 kW and the cost reducing by less than 5 %. We did not pursue this option further. A 25.0 cm shield was employed for all of our further `PROCESS` calculations. A breakdown of the resulting optimised reactor radial build is shown in table 5 and figure 3. The approach we have adopted here has identified the important properties of our preferred choice of reactor using state-of-the-art `MCNP` calculations. The benchmarking data in Table 4 demonstrates that the neutron and gamma flux typically reduces by an order of magnitude every 15 cm. The detailed `MCNP` calculations confirm that unless one is going to embark on regular component replacement, the range of radiation shield thicknesses available to the fusion engineer is limited, given the TBR requirements, and that currently, the optimum is determined by the lifetime of the best available brittle superconductors. 

## _- 4.2. Cryogenic flow Benchmarking_ 

In this paper, we assume that the cryogenic heat load is broadly constant throughout a plasma pulse and distributed evenly throughout each cooling channel. The benchmarking thermal calculations only consider the TF coils (whereas the detailed `PROCESS` calculations consider the entire magnet system - TF, CS and PF coils). The 

temperature of the superconductor can be estimated using Newton’s law of cooling [101] 

![](images/chislett2022.pdf-0014-03.png)

where ∆ _T_ coolant-sc is the difference between the temperature of the coolant and that of the superconductor, _Q_ is the heating load (in Watts) in each cooling channel, _L_ channel is the cooling channel length, _Wp_ is the cooling channel wetted perimeter, _m_ ˙ is the coolant mass flow rate, _x_ is the distance along the cooling channel, _cp_ ( _T_ ) is the coolant specific heat capacity per unit mass, and the heat transfer coefficient, _h_ ( _T, p_ ), can be derived from the Dittus-Boelter equation, written in terms of the Nusselt number, _Nu_ , [102]; 

![](images/chislett2022.pdf-0014-05.png)

where _Dh_ is the cooling channel hydraulic diameter, _κ_ ( _T, p_ ) is the coolant thermal ˙ conductivity _Re_ ( _T, p_ ) = _mDh/µ_ ( _T, p_ ) _Acoolant_ is the coolant Reynolds number, _Acoolant_ is the coolant cross section, _Pr_ ( _T, p_ ) = _µ_ ( _T, p_ ) _cp_ ( _T, p_ ) _/κ_ ( _T, p_ ) is the coolant Prandtl number and _µ_ ( _T, p_ ) is the coolant dynamic viscosity. From the maximum pressure drop allowed, the maximum mass flow rate can be calculated using the Darcy-Weisbach equation [102] 

![](images/chislett2022.pdf-0014-07.png)

˙ where _ρV_ is the density, _⟨v⟩_ = _m/ρAcoolant_ is the mean coolant flow velocity and the Darcy friction factor _fd_ can be expressed in terms of the Reynolds number and void fraction in the cable - _Vcoolant_ as [102] 

![](images/chislett2022.pdf-0014-09.png)

We validate this benchmarking approach by considering the JT60-SA tokamak and the materials properties used in Table 6. Using _Acoolant_ = 1 _._ 27 _×_ 10 _[−]_[4] m[2] , _Dh_ = 4 _._ 57 _×_ 10 _[−]_[4] ˙ m, _m_ = 3 _._ 5 g s _[−]_[1] , _Vcoolant_ = 0 _._ 32, _T_ coolant[inlet][=][4.4][K,][an][inlet][pressure][of][5][bar,] _[L]_[channel] = 123.3 m (5 double pancakes per TF coil, each of length 296 m [103] and 12 cooling channels per TF coil [102]), the time averaged heat load on each coolant channel is 12.1 W. Equations 4 - 7 yield a pressure drop of 0.9 bar and helium outlet temperature for each cooling channel of 5.2 K, which compares favourably to more detailed calculations of 1.1 bar and _≈_ 4.8 K [102]. 

For our preferred choice reactor, PROCESS gave 18 TF coils with a total cable cross section of 39.6 cm[2] and an inner (square) cross section of 23.6 cm[2] . We have set the number of cooling channels per TF coil to be 10 (note JT-60SA has 12 and ITER has 14), which given there are 100 turns per TF coil each of 36.4 m, leads to _L_ channel = 364 m. A 20 % conductor void fraction [104] then sets the cooling channel hydraulic diameter in the superconducting cable to be 2.45 cm (with _Vcoolant_ = 1 _._ 0 within this channel). Setting the inlet temperature to 4.5 K, inlet pressure to 5 bar and limiting the pressure 

drop along the coolant pipe to no more than ∆ _P_ = 1.0 bar sets an upper limit on the fluid mass flow rate of _≈_ 132 g s _[−]_[1] (much larger than in JT-60’s 3.5 g s _[−]_[1] because the channel is much wider and is unobstructed by conductor strands, with commensurately less drag). Including the TF coil winding pack circulator work, AC losses and static heat loads the total `PROCESS` calculated heat load is 89 kW and the TF coil coolant outlet temperature is 4.6 K. Hence we conclude that the cryoplant performance required by the preferred choice reactor is met using existing tokamak cryoplant systems. 

It is interesting to consider whether, if operation were required at 30 K, a different cryogen, would be preferred. Here we rule out hydrogen and oxygen mixes to avoid unnecessary additional safety considerations and just consider neon. Under 5 bar pressure, supercritical helium at 30 K has _≈_ 6 % of its density and _≈_ 120 % of its dynamic viscosity at 4.5 K [105]. If we maintain the 1.0 bar pressure drop, the mass flow rate reduces to 30 g s _[−]_[1] resulting in an outlet temperature of 30.3 K. At 30 K and 5 bar, liquid neon has a density _≈_ 9 _×_ greater and a dynamic viscosity _≈_ 25 _×_ greater than He at 4.5 K. A 1.0 bar pressure drop leads in this case to a mass flow rate of 380 g s _[−]_[1] and an outlet temperature of 30.1 K. Hence, at 30 K liquid neon only slightly outperforms supercritical helium as cryocoolant and so is not required/considered further. 

## **5. High Field Superconductors** 

Here we consider the important high-field superconductors that can enable commercial magnetically confined fusion: 

## _5.1. Fusion Relevant Superconductors_ 

_5.1.1. Nb-Ti_ The Nb-47wt.%Ti alloy [106] is the most important commercial superconducting material. It has been optimised for maximum critical current density between _≈_ 4 T and 6 T for MRI and accelerator magnet applications [107]. Its relatively low upper critical field ( _B_ c2(4.2 K) _≈_ 10 T [108]) means that it has only been used for the poloidal field coils in next generation fusion reactors such as ITER [109] and EU-DEMO [3] (though it is being used for the TF coils in JT60-SA [110]). 

_5.1.2. Nb_ 3 _Sn_ Nb3Sn is a brittle intermetallic compound with _B_ c2(4.2 K) _≈_ 20 T [111] which has long made it the material of choice for applications when _>_ 10 T fields are required. The Nb3Sn superconducting matrix can also include tantalum and titanium [112] (to increase the upper critical field) or hafnium [113] dopants (for improved _J_ c at fields above 15 T). Nb3Sn cables are broadly produced in one of two ways: Wind & React where unreacted cables are jacketed and wound into a coil which then undergoes heat treatment; or React & Wind where the cables are heat treated and then wound into a coil [114, 115]. When using the former process one has to be careful about the fracture of the Nb3Sn filaments and consequent degradation of the cables’ critical current during manufacture [116, 117] due to the different thermal expansions of the cable jacket and 

superconducting filaments. The latter method avoids this issue, but the reacted cable can only be used to produce magnets with large bending radii. Nb3Sn is not considered in detail in this work because we have found almost always that a cost minimised Nb3Sn reactor has a larger capital cost than an equivalent REBCO reactor, as shown in table 2. However as discussed below in section 5.4, Nb3Sn could still have a role to play in cost optimising graded coils where different superconductors are used within the same winding pack. 

_5.1.3. REBCO_ The exciting new results from MIT which achieved a field of _>_ 20 T [118, 119] at elevated temperatures (20 K) in a fusion relevant coil, demonstrate REBCO cables are on a fast track to fusion applications [36]. REBCO’s _≈_ 90 K critical temperature [120] allows for large temperature margins in cable design and higher operation temperature that reduces cryo-power requirements. However there is more work to be done to demonstrate reliability - it is a ceramic oxide material, that is prone to brittle fracture under tensile strain _>_ 0.3 - 0.7 % [121, 122] and tape delamination under cyclic loading [38, 123]. Although stable against quenches, quench protection and detection are more demanding than in low temperature superconductors due to REBCO’s low normal zone propagation velocities [124] and the low thermal conductivity in the tapes ( _≈_ 100 - 600 W m _[−]_[1] K _[−]_[1] at 20 K and zero field [125]). 

_5.1.4. New fusion-focused high-field superconducting alloys_ Other Nb-Ti based alloys have been produced with larger upper critical fields than commercial Nb-Ti. Indeed the record upper critical field at 4.2 K is held by a quaternary alloy Nb 38.5%wtTi 6.1%wtZr 24.3%wtTa with _B_ c2(4.2 K) _≈_ 13 T [126, 127]. Although the alloy is not produced commercially, its higher _B_ c2 and ductility make it a obvious candidate material to optimise for future high-field fusion coils. In this work we have completed cost calculations using both the commercially available Nb-Ti used in ITER, and quaternary Nb-Ti (with the implicit assumption that fusion on an industrial scale would provide the commercial driver for quarternary Nb-Ti if required, at a similar cost to current commercial Nb-Ti). These calculations demonstrate that in fusion magnets, unlike accelerator magnets, it is is the low resistance rather than the high _Jc_ values that is required from superconducting materials. This points to future work (beyond the scope of this paper) developing fusion-focused high _Bc_ 2 superconductors that may be new alloys, or perhaps exploit reduced dimensionality to produce high _Bc_ 2 [128] in say artificial multilayer alloys that bring the huge potential advantages of lower cost, more straightforward robotic handling, higher radiation tolerance and higher strength than brittle materials and hence could displace high temperature superconductors. 

## _5.2. Critical current density - field, temperature and strain dependence_ 

Updated `PROCESS` subroutines for Nb-Ti, Nb3Sn and REBCO have been used throughout this investigation, primarily based on data collected at Durham University. All data in 

table 7 correspond to the whole strand or whole tape critical current density (aka the engineering current density). When modelling the low temperature superconductors using `PROCESS` the cable conductor fraction of copper is 69 % and of superconductor is 31 %. The cable conductor helium void fraction is 33 % (similar to the ITER cables [129]). For REBCO, we have assumed the cable is fabricated with stacked tapes (similar to [104]) and has a helium void fraction of 20 %. The operating current was in all cases set to 100 kA and limited to 50 % of the cable critical current in all cases. The parameterisations for the critical current density, _J_ c, of Nb-Ti, quaternary Nb-Ti, Nb3Sn and REBCO are based on a standard scaling law [108, 130] itself based on the wellestablished Ginzburg-Landau theory for the high field properties of superconductors [131, 132, 133]: 

![](images/chislett2022.pdf-0017-03.png)

where _B_ is the applied magnetic field, _T_ is the temperature, _ϵ_ is the strain, _A[∗]_ is a constant, _T_ c _[∗]_[is][the][critical][temperature,] _[B]_ c2 _[∗]_[is][the][upper][critical][field,] _[b]_[=] _[B/B]_ c2 _[∗]_ and _t_ = _T/T_ c _[∗]_[.] _A[∗]_ , _T_ c _[∗]_[and] _[B]_ c2 _[∗]_[have][been][given][their][standard][literature][values] [111, 134] found for an operating temperature of 4.5 K and an applied strain of - 0.5 % (equivalent to an intrinsic strain of -1.0%). These strain values were fixed for all conductors, representative of typical cryogenic pre-strain (a compressive strain of -0.58% is expected for ITER conductors [135]). Data from measurements on ITER specification commercial Nb-Ti have yielded the fit parameters detailed in table 7 [108]. As mentioned, although quaternary Nb-Ti has not been commercialised or produced in wire form, we have addressed its potential by using the literature values of _B_ c2(4.2 K) and _T_ c for bulk materials reported in [126, 127]. All other fitting parameters for this quaternary material were assumed to be the same as for commercial Nb-Ti. The REBCO scaling parameters were taken from previous measurements on SuperPower tapes [120, 136]. A comparison between the overall strand and tape critical current densities of commercial Nb-Ti, quaternary Nb-Ti and REBCO at 4.5 K is shown in figure 7. 

## _5.3. Costing Superconductors_ 

The superconductors have been costed using the industry standard units [137] of $/kA m where 

![](images/chislett2022.pdf-0017-07.png)

where _B_ ref and _T_ ref are reference conditions at which cost is usually quoted. Increasing the tape/wire current density for a factor of _n_ decreases the cost by the same factor of _n_ (assuming that manufacturing costs remain unchanged). We have used a cost of 1.7 $/kA m (6 T, 4.2 K) for both commercial Nb-Ti and quaternary Nb-Ti strands, and 8.0 $/kA m (6 T, and 4.2 K) for Nb3Sn strands [138] (in 2021 costs). Currently, REBCO tapes are priced at _≈_ 80 $/kA m (6 T, 4.2 K) with the aim to reduce this to 30 

$/kA m (6 T, 4.2 K) in the near future [137]. Increased demand could reduce this even further to 10 $/kA m (6 T, 4.2 K) [137, 139]. Here REBCO costs of 10 $/kA m and 30 $/kA m have been used for the H98 = 1 _._ 6 and H98 = 1 _._ 2 reactor studies respectively and are representative of the market prices of the superconducting strands/tapes, which are typically 10 _×_ [137] or even 20 - 35 _×_ the raw material costs [140]. 

The trustworthiness of this cost model was ascertained in three ways: (1) the cost model was applied to `PROCESS` test-cases (such as the 2018 EU-DEMO baseline model). (2) Runs were performed using the $/kg model and then $/kA m model. Typically, magnet costs from the new cost model differed from those of the original model by _<_ 20 %, and were as expected in more extreme cases (such as for a REBCO cost of 0.025 $/kA m as in section 7). (3) The relative costs between systems were compared to those from independent studies of other tokamaks (such as ARC [5], ITER and EU-DEMO [15]). Relative costs between plant components are broadly in line with what would be expected for the size of reactors investigated. 

## _5.4. Graded and Sectioned Coils_ 

Here, we have used the most simple winding pack design which retains the same superconductor cross section along the entire cable length (as determined at the peak field on coil) [141]. However in the regions of the magnets where the field is low, the superconductor operates well below its critical current density and one can consider graded coils in which the cross section of the cables are reduced [115, 142]. Further cost reductions follow when cheaper superconductors are used in the outer parts of the winding pack e.g. Nb-Ti in the low field regions, Nb3Sn in the middle of the winding pack and REBCO in the high field regions [143]. Figure 8 shows the clear benefit using graded TF coils. The inboard side of the TF outer leg sees fields _≈_ 30 % lower than the maximum on-coil field (at the outboard side of the TF inner leg), and the outboard side of the outboard leg sees fields 75 % lower than the maximum on-coil field. The toppling forces are also localised, meaning that grading cable conduit thickness is also beneficial. Taking the example of the central solenoid coil in [144] and using a REBCO cost of 30 $/kA m (6 T, 4.2 K), we calculate the graded multi-superconductor solenoid to have a materials cost _≈_ 21 % cheaper (equivalent to an overall capital cost reduction of just 0.3 %) than the ungraded REBCO-only solenoid. 

As well as traditionally graded coils, the field-on-coil data of figure 8 show that given we need remountable magnets to enable timely repair, we can also consider sectioned coils, perhaps with a half-phi design [31]: coils where the inner and outer coil limbs are based on different superconductors [145, 31]. For the preferred reactor TF coils, the field on the outer limb is below 8 T, making Nb-Ti the obvious choice. Nb-Ti at 8 T has a cost in $/kA m _≈_ 16 _×_ lower than that of REBCO at 12.5 T, so adopting Nb-Ti outer limbs would reduce the preferred reactor’s TF coil direct cost by _≈_ 16 % (reducing the reactor’s overall capital cost by _≈_ 2 %). 

_5.5. Stress-limited, Jc-limited and Bc2-limited magnets_ 

In general, superconducting magnets can be: stress-limited, in which case the Lorentz force induced stresses are close to the yield-stress of the component magnet material; _J_ c- limited, where the current density in the superconductor is sufficiently high to overcome flux pinning and the material may become resistive. Here we also consider a type of _J_ c-limited, that we call _B_ c2-limited. In this case, the operating field is close to the upper critical field of the superconductor so the description makes clear that increasing _B_ c2 will significantly affect the operating field achievable - equivalent to the critical current density being low because the superconductor’s bulk critical properties are low rather than the strength of flux pinning per se. The limiting factors for magnets can be understood with reference to the hoop stress in a magnet approximated by [132] 

![](images/chislett2022.pdf-0019-04.png)

where these are averaged properties over the magnet, and _B_ magnet is the magnetic field, _J_ is the magnet current density, and _R_ magnet is the radius of the magnet. 

In commercial, small bore superconducting accelerator magnets such as those at CERN, the operating current density of the component superconductors is close to the critical current density of 10[9] A m _[−]_[2] at the operating field of 16 T and the magnets are _J_ c-limited. In contrast, the relatively huge bore of our preferred fusion reactor has _B_ coil = 12.5 T and a leg-centre to leg-centre distance at the mid-plane of 9.2 m. At _σ_ hoop[max][=][660][MPa][the][operating][current][density][in][the][TF][coil][winding][pack][is] _[≈]_[2.3] _×_ 10[7] A m _[−]_[2] , two orders of magnitude lower than that in accelerator magnets or that in the whole tape critical current density of REBCO at 12 T, 4.5 K (see figure 7). It is important to distinguish whether a magnet is stress limited or _J_ c limited. If the magnet is _J_ c limited, improvements in _J_ c directly increase the field the magnet can produce, whereas in a stress-limited magnet where say only a few percent of the cross-section of the coil is superconductor, improvements in _J_ c only allow marginal increases in the steel volume content, whereas improvements in stress limits (or design) are markedly more beneficial because they increase the space for more superconductor and hence increase the operating field. If the magnet is _B_ c2-limited, increases in the superconductor upper critical field are most effective in increasing the cost-optimal field on-coil. These considerations demonstrate that in tokamaks where magnets are stress-limited and the overall current density in the cable is far from the operating _J_ c limits of REBCO, current superconductors are far from optimised for fusion applications. REBCO magnets are stress-limited and cable design benefits most from improvements of structural material, as it is the yield stress of the material (and the design of the magnets, discussed below) that primarily determines operational limits and cost. Likewise increasing the upper critical field of Nb-Ti (e.g. via the use of a higher _B_ c2 alloy) would significantly improve its use in fusion magnets. 

## _5.6. Superconductors in a sea of neutron and photon radiation_ 

Superconducting magnets in a fusion environment are located in a rather special sea of neutron and photon flux, with both charged particle (ion) cascades and low energy photons continuously created in the interior (or bulk) of all the materials (cf Figure 5). Typical penetration depths for photons vary hugely as a function of energy from tens of cms at MeV to the atomic scale at meV. This means that it is difficult to artificially replicate the properties of a fusion plant flux and test a materials’ performance under operation-like conditions, since high energy photons are not easily absorbed by materials, and low energy photons cannot easily penetrate material’s interior. Nevertheless, the nature of the (ionised) equilibrium electronic state of a superconductor in the neutron+photon+cascade (n+p+c) sea is important since the superconducting Cooper pairs have an energy of several tens of meV ( _∼_ 3.5 k _B_ T _c_ ) and it is not clear whether the pairs remain intact [146]. Unfortunately theoretical considerations provide little insight, not least because we don’t yet know the details of the mechanism that causes superconductivity and whether for example we should consider preformed Cooper pairs that condense, or charge carriers that both pair and condense at the same temperature. In standard superconductor lifetime experiments, superconductors are exposed to (very high) neutron flux, usually (but not always [147]) warmed to room temperature and then cooled to have their superconducting properties measured in a radiation-free environment [94]. However, there have been no published in-situ cryogenic measurements of the critical current density during (operational-like) n+p irradiation to confirm the superconducting properties are unaffected by the rather special sea of neutron and photon radiation produced by a fusion energy spectrum. The concern of course is that as you start turning the tritium plasma and the fusion radiation spectrum on in the tokamak, you simultaneously start turning the superconducting magnets off. Currently the community relies on at best a working assumption, perhaps guided by the uncertainty principle, that the Cooper pairs reform quickly enough for their equilibrium density to be broadly unaffected by the n+p+c fusion flux. We note that relatively low operational-level neutron flux is required for the measurements (i.e. far below those used in life-time experiments), and that data for both low temperature superconductors and high temperature superconductors are required because the electronic charge carrier densities are very different. Such measurements could be attempted using international neutron sources (the total flux at ILL is 1.5 x 10[15] _n.cm[−]_[2] _.s[−]_[1] [148]) or better, during a deuterium-tritium campaign [149]. 

## **6.** `PROCESS` **Power Plant Simulations** 

In this section we present results from our two different approaches: (a) Training: where we use Nb-Ti training magnets during the (high risk) commissioning stage (Phase 1) of a reactor that has been designed to be cost-optimised for REBCO magnets (Phase 2); (b) Upgrading: This reactor design is cost-optimised for Nb-Ti coils and later upgraded 

for REBCO magnets. Baseline reactors at the 100 MWe, optimised for for H98 = 1.2 and 500 MWe with H98 = 1.6 were generated for both approaches. For each of these baseline reactors the geometry was fixed and the superconducting materials used in the TF and CS coils were replaced with either REBCO, commercial Nb-Ti or quaternary Nb-Ti. By “reactor geometry”, we mean the reactor’s physical build (e.g. the location of the coils, thickness of blanket, location of the first wall, etc.) - the plasma shape was allowed to vary. In both approaches, the magnet systems from the first phase were replaced by magnets where the combined sizes of the CS and TF coils changed by less than 1% (equivalent to re-optimising the cable dimensions and construction, but keeping the reactor radius and height fixed). In all cases the second phase reactors had magnets re-optimised for maximum net electricity yield in order to maximise the swapped magnets’ performance. For each of the six baseline tokamaks shown in Tables (7 - 12), we have also calculated the effect a reduction in H98-factor to a value of unity would have. These data show the drop in fusion power and net electricity generation that would occur were plasma quality not to meet the higher values hoped for. The six baseline reactors considered in this paper (including the preferred reactor in bold) are compared to other world-wide tokamak designs in table 1.. 

For the training approach, the capital costs were calculated by adding the cost of the full-power reactor to the cost of the training magnets alone. We have assumed that other plant components can simply operate with reduced capacity. For upgrading approach, the capital costs were calculated as the cost of the respective baseline reactor combined with the cost of the new magnets and costs associated with increasing the scale of additional plant components (enhanced generator capacity, heat transport, fuel handling etc.). In all cases as noted above, we have not added cost associated with making the magnets remountable or the design and operational costs associated with robotic handling. During the commissioning of the reactor, the full-power REBCO coils must of course be tested and commissioned themselves. Indeed the reactor will have to itself be recommissioned at full power.The training coils will allow allow the operational team to iron out the majority of user error and manufacturing error related disruptions and unexpected events which could destroy the brittle REBCO magnets, before they are – installed. Plasma will be generated, power plant systems will be able to be tested etc. simply not at full capacity, but close enough to full capacity to discover and significantly reduce the risk of magnet-destruction-capable events. Experience has shown that the majority of disruptions occur at the beginning of reactor life [9] - using training coils therefore puts the brittle full-power magnets at much less risk. 

## _6.1. REBCO tokamaks with training magnets_ 

Table 8 shows that for our preferred reactor, the use of commercial Nb-Ti TF and CS training magnets during the training phase reduces fusion power to _≈_ 60 MW from 860 MW, and results in an electricity deficit of _≈_ -180 MWe. Despite the less energetic plasma and the lower peak fields on TF coils (70 %) and CS coil (66 %) that commercial 

Nb-Ti training magnets would generate, they would nevertheless allow rather thorough machine testing during the plant commissioning phase. The table shows that the final total cost for the training magnets and the final preferred tokamak together is $ 4.54 Bn (1990 US) equivalent to about $ 9.75 Bn (2021 US) - along the lines of $ 20 Bn estimated for a DEMO reactor [150]. Interestingly, quaternary Nb-Ti TF training magnets are almost able to match the field of the full-power REBCO TF coils (93 %) when REBCO is used for the CS coil. These large percentages are because the high _B_ c2 quaternary Nb-Ti coils are able to produce a large fraction of the stress limited cost-optimal field and provide a prima facie case for the fusion community to develop as a priority, new high _B_ c2 ductile low temperature superconductors specifically for fusion, but with _J_ c values that by the standards of other applications are (undemandingly) low. At H98 = 1.6 (Table 9) the lower plasma current reduces the peak field on the REBCO baseline CS coil, so commercial Nb-Ti CS coils produce 77 % of the CS coil peak field and the quaternary Nb-Ti coils produces 87 %. Similarly, higher H-factor means the CS training coils also do not have to produce as high a magnetic flux. The commercial Nb-Ti CS and PF system delivers only 105 Wb compared to the 261 Wb of the training coils for the preferred reactor (note that the plasma current fractions of the respective baseline reactors are however approximately equal at 62 % at H98 = 1.6 and 66 % at H98 = 1.2). Given the peak field on the CS remains 9.2 T in both cases and the number of turns falls by only 10 %, the lower flux requirement allows a larger proportion of the available CS-TF space to be occupied by the TF coils and a 32 % larger TF conductor cross-section as a result - allowing for the production of a larger toroidal field. The quaternary Nb-Ti case is similar. 

The effect of a range of different H98-factors (H98 = 1.2 and H98 = 1.6) for two REBCO 100 MWe reactors are shown in figure 9. For increases in H98 factor above design expectations the fusion power is not greatly increased. However, if in practice the H98 factor achieved is below the design specification, the plasma loses energy faster than it is supplied, energy confinement is lost [151] and the plasma burn cannot be maintained for the required 2 hours. As a result the fusion power collapses, resulting in negative net electricity production. It is therefore important that tokamak power plant designs are conservative with regard to H98-factor, since the consequences of unexpectedly poor performance are quite severe. 

If we consider building a very large 500 MWe REBCO baseline design, the reactor with commercial Nb-Ti TF and CS training magnets is able to generate 78 % field on TF (Table 10). This larger percentage is because the TF coils of the 500 MWe reactor have larger radii (11.1 m from leg centre to leg centre at the mid-plane compared to the 9.2 m of the 100 MWe preferred reactor) which reduces the optimal field on TF for the baseline design due to the larger stresses (equation 10). The larger plasma current requirement for the larger fusion power means that the poloidal field coils generate a larger proportion of the magnetic flux (it is more cost-beneficial to increase the output of the Nb-Ti poloidal field coils, than it is to greatly increase the size of the REBCO CS and overall reactor volume as a result). Here, the PF system delivers 51 % of the 

total magnetic flux, compared to 43 % of the flux in the 100 MWe REBCO reactor. The flux requirement when the commercial Nb-Ti training coils are used drops from 446 Wb to 321 Wb, so now the (unchanged) PF system delivers 66 % of the flux, reducing the flux demand on the CS, reducing its necessary size and allowing for larger TF coil thickness. The larger cross-section of the TF coils of the commercial Nb-Ti training coils for the 500 MWe reactor leads to a 24 % larger conductor cross-section (in comparison to the 100 MWe reactor case) and the generation of an additional _≈_ 0.5 T on-coil. Commensurately, a full quaternary Nb-Ti set of training coil can generate a TF coil field of nearly 97 % of that of REBCO with a field on coil of 11.5 T. 

All three baseline reactors in Tables (8 - 10) operate with TF and CS coils at the stress limit of 660 MPa. Taking the case of the 100 MWe preferred reactor, when only commercial Nb-Ti TF training coils are used, operation close to upper critical field demands a larger superconducting fraction in the cable and reduces TF coil steel fraction from 52.8 % to 38.5 %. Operation below the designed-for field reduces stress on the TF by 270 MPa and CS by 210 MPa. When both TF and CS training coils are used the steel fraction must also decrease (from 80.4 % to 42 %) in order to maximise the CS superconductor fraction and magnetic flux the coil can generate. The peak stresses rise closer to the 660 MPa limit as the interplay between the TF and CS coil thicknesses allows for better optimisation of the coil steel fractions. 

## _6.2. Nb-Ti Tokamaks with Upgrade Coils_ 

Table 11 shows that upgrading tokamaks is a significantly more expensive approach than the training approach (cf 6470 M$ in Table 11 compared to 4540 M$ in Table 8). Although swapping the CS and TF coils for REBCO, or the CS coil for REBCO and the TF coil for quaternary Nb-Ti produces more electricity (i.e. _≈_ 280 MWe) and swapping all coils for quaternary Nb-Ti yields more electricity (i.e. _≈_ 230 MWe), we feel these increases do not significantly better de-risk fusion energy production for commercialisation (considered in detail below). In the former case, the CS and TF coils are stress limited, so although in principle the REBCO upgrade coils could produce higher fields on the plasma and in the CS coil, they are prevented from doing so by the thickness of the steel support required to resist the greater magnetic forces in the limited space available. In the latter case, the limiting factor is the critical current density of the quaternary Nb-Ti cable, in the CS coil. Just swapping the centre solenoid alone for REBCO, while keeping the original commercial Nb-Ti TF coils offers no benefit, as the TF coils in the baseline design are already _B_ c2 limited. The H98 = 1.6 commercial Nb-Ti case, shown in table 12, is very similar to the H98 = 1.2 case. The larger fields produced by the upgraded magnets are due to the higher H98-factor reactor’s smaller major radius, meaning that the stresses on the TF coils are consequently lower for a given field-on-coil. 

For the larger 500 MWe tokamak (Table 13), upgrading the reactor with a REBCO CS coil and either REBCO or quaternary Nb-Ti TF coils results in an increase in net 

electricity output of _≈_ 36%. The smaller percentage increase in this larger machine is due to the more stringent stress limits in the larger radius coils. Indeed, a fully quaternary Nb-Ti upgraded reactor would only generate 8 % more electricity as the current in the CS coil is limited by the critical current density of the conductor. 

The cost-optimised upgraded tokamaks again operate with 660 MPa stresses on the TF and CS coils in order to minimise the amount of steel support used. Focusing on the 100 MWe, H98 = 1.2 reactor, when REBCO TF and CS coils are used, the peak fields on coil increase by 9 % and 63 %, the current densities increase by 1 % and 14 % and the coil radii decrease by 0 % and by 6 % respectively. The resulting change in stress (equation 10) necessitates increases in the TF and CS coil steel fractions by 2.3 % and 27.6 %. The same is true of quaternary Nb-Ti upgrade coils, though the increases in steel fractions are more modest due to the lower increases in 

## _6.3. Spherical Tokamak Power Plants_ 

Spherical tokamaks have some significant advantages and disadvantages over conventional aspect ratio tokamaks and are being considered for pilot fusion power plants [4, 41]. Spherical tokamaks operate at higher beta (of up to 40 % [152]) and at higher safety factors (e.g. _q_ 95 = 8 _._ 9 in FNSF [153]) than conventional reactors, meaning that that their plasmas are inherently more stable (and disruptions less likely) for a given field on plasma axis [152, 154, 155]. Spherical tokamak pilot plants have proposed designs that are compact, with major radii _<_ 3 _._ 5 m [41, 156, 157, 153] (in principle reducing construction costs and time [158]) whilst producing a plasma fusion gain _≈_ 30 [41, 159]. 

Spherical tokamaks’ compact size however also increases average neutron wall loading, above 3.5 MW m _[−]_[2] in some proposed pilot plant designs [156, 157], to more than three times that of EU-DEMO [3]. This very high flux necessitates thick radiation shielding (or breeding blanket) of _≈_ 60 cm for the central column [153] (reducing the field on coil for a fixed reactor major radius), or frequent remote replacement of the central column magnets (on the order of every 3 years [157]). The small size also increases the power through the separatrix (above 30 MW m _[−]_[1] in some designs [156, 157]) necessitating the use of advanced divertor configurations [160] which would either make use of sacrificial, resistive, inboard coils (that are part of a higher order reactor design than that discussed in this work) or require heavily distorted TF coil architectures [71, 72]. Large tokamak design studies of ITER-type plants have shown the cost of electricity is lower for large tokamaks, scaling proportionally to the electric power of the tokamak raised to the power -0.59 (i.e. increasing the electric power produced by a factor 10 reduces the cost of electricity by about 4) [138] and ultimately means that large fusion power plants are likely to produce the cheapest electricity. Nevertheless compact spherical tokamaks may offer the opportunity for lower capital costs to demonstrate fusion energy is commercially viable - it is beyond the scope of this paper on ITER-like aspect ratio machines to assess to what degree these reductions are offset by the specific 

technical challenges of spherical tokamaks, and hence how effectively they provide a short-cut to demonstrating commercial fusion energy is cost-effective. 

## _6.4. Aluminium/Copper Tokamak Power Plants_ 

Copper [161, 162] and aluminium [163] have the best combination of high strength and high electrical conductivity to have been the choices for for magnets in experimental – fusion reactors. Resistive magnets for tokamaks are typically operated at 300 400 K and do not suffer the same cut-off in current carrying capacity with neutron fluence as superconductors, meaning that shielding requirements are reduced and reactors can (in principle) be made more compact. However, the (magneto-)resistivity of these materials is unchanged for many decades and can be contrasted with developments in superconductivity where large scale projects such as ITER and CERN continue to drive improvements in materials with higher current density, and one can expect commercial fusion to drive the development of the more neutron tolerant materials (eg high-field alloys). Resistive tokamaks have indisputably helped drive our experimental understanding of, and encouraged new designs for, high-field fusion plasma physics. For example, ARIES-ST [157] which was designed with only a 20 cm ferritic steel centrepost shield leading to a predicted nuclear heating of 164 MW and total magnet system losses of _≈_ 730 MWe, an order of magnitude more than the cryoplant power and magnet system losses for the superconducting reactors in table 3. 

Proposed resistive reactors however have very low plasma burn times (e.g. FIRE _≈_ [164] (a prototype reactor) with a 20 s plasma burn and 3 h repetition time) or rely on non-inductive start-up mechanisms and assume large _H_ 98 ≳ 1.5 (e.g. ARIES-ST [157] and STPP [156]). Even the small size of proposed resistive tokamaks would not obviously reduce their capital cost compared to superconducting reactors. Both ARIES-ST’s cost of _≈_ 4200 M$ (1990 $) and our `PROCESS` generated capital costs for a 100 MWe STPP-like reactor (with minimised capital costs) of 5200 M$ shown in 14 are similar to the cost of the _H_ 98 = 1.2 preferred reactor, and in fact larger than the _H_ 98 = 1.6 REBCO reactor in this work. The reduced costs due to smaller size are counterbalanced by cost increases in coil bussing and power conditioning. It has been argued that high temperature superconductors are an essential technology that will enable commercial fusion power [50]. We broadly concur that the scarce resources for commercialisation of fusion are best focussed on de-risking and up-skilling in commercialising the unprecendently large superconducting magnets required for fusion, rather than resistive ones. 

Using a similar validation process to the one above, we first confirm the reliability of our `PROCESS` calculations by comparing them with some simple benchmark calculations and with JET experimental results. Our approach was to compare the maximum current per resistive magnet turn to the maximum current per superconducting magnet turn in a tokamak with space allocated to the magnets equal to that in our preferred tokamak. Note that a turn consists of the cable and the insulation. The cable has a structural, conducting and cooling channel components. In our `PROCESS` simulations the insulation 

is 1.5 mm thick. Making explicit our use of Ampere’s law [165], we can write: 

![](images/chislett2022.pdf-0026-03.png)

where _I_ turn[resistive] and _I_ turn[preferred] are the coils’ currents per turn on the resistive reactor and the preferred choice reactor and _B_ plasma[preferred] and _B_ plasma[resistive][are the magnetic fields on plasma] axis of the preferred choice reactor and resistive reactor respectively. The maximum current per resistive magnet turn was calculated using 

![](images/chislett2022.pdf-0026-05.png)

where _ϱn_ is the conductor resistivity, _L_ turn is the length of each turn and _A_ turn is the cross-section of each turn. The maximum cooling power per turn _Q_[max] cooling[is][given][by] 

![](images/chislett2022.pdf-0026-07.png)

where _m_ ˙ is calculated from equation 6 noting that for _m_ ˙ _≈_ 0.1 kg s _[−]_[1] _fd ≈_ 0 _._ 0231 _/Vcoolant_[0] _[.]_[742][.] In each of JET’s 32 TF coils [166, 167, 168], there are 24 turns of length 15 m, and average turn cross section of _≈_ 32 cm[2] . Each turn has its own cooling channel with a cooling channel hydraulic diameter of _Dh_ = 1.5 cm, an inlet over-pressure is 5 bar and ∆ _P_ = 0.5 bar. The temperature of the coolant is _T_ coolant[inlet][=][293][K][and][∆] _[T][turn]_[=][75] K. We have set the average copper magnetoresistivity over the temperature range (and typical field _≈_ 6 T) to be 2.20 _×_ 10 _[−]_[8] Ωm (c.f. Table 6 [169, 54]) and used the wellknown properties of water for the coolant (rather than the anticorrosion fluid Galden HT55 used in practice). The simple benchmarking equations above yield a current per turn of 63.4 kA, very close to the JET current per turn of 66 kA and resistive losses for the TF magnet system of 497 MW, close to the JET power requirements of 700 - 1375 MW [168, 170]. 

Turning to use the geometry of our preferred choice reactor, there are 18 TF coils each with 100 turns each of length 38.1 m and a cross-section for each cable of 39.6 cm[2] . Following JET, we consider resistive copper magnets operating at room temperature where each turn has its own cooling channel. The inlet pressure was set to that of JET with 5 bar and ∆ _P_ = 1 bar, as well as the temperature of the coolant, _T_ coolant[inlet] = 293 K and ∆ _Tturn_ = 75 K. The cooling channel hydraulic diameter was optimised and found to be at 56 % of the cross-section (i.e. _Dh_ = 5.3 cm). Equations (11 - 13) then yield a maximum current per turn of 57.1 kA compared to the preferred reactor which has 100 kA per turn. Not surprisingly for resistive magnets, we find a huge power consumption of 3 GW. We now consider whether running resistive magnets at cryogenic temperatures is more viable and calculate the performance of cryogenically cooled resistive aluminium magnets cooled to 65 K using liquid nitrogen as the coolant, and then at 20 K using supercritical helium. Aluminium and copper have similar room temperature resistivity ( _≈_ 2.7 _×_ 10 _[−]_[8] Ωm and _≈_ 1.7 _×_ 10 _[−]_[8] Ωm respectively), but it is cheaper to make high-purity high-strength aluminium than copper, so aluminium is 

generally preferred at low temperatures for cyocooled resistive magnets. Ensuring the nitrogen doesn’t solidify or become gaseous requires setting _T_ coolant[inlet][=][65][K][and][∆] _[T]_ = 15 K. Averaging over the temperature range, at 6 T and RRR = 10000, Al has a resistance of _≈_ 3 _×_ 10 _[−]_[9] Ωm [171, 172]. Using the benchmarking calculations we find the current in each turn is only 35.6 kA which is lower than the 100 kA in the preferred superconducting reactor. Of greater concern commercially (also found below for 20 K) is that the required resistive heating is 148 MW which even with ideal Carnot losses require a cryocooler electric power of 683 MWe. Turning to 20 K operation with ∆ _T_ = 20 K and using supercritical helium: averaging over the temperature range, at 6 T and RRR = 10000, Al has a resistance of _≈_ 10 _[−]_[10] Ωm [171, 172]. Under these conditions, the current in each turn is higher than the superconductor by about 50 % (were it not to be stress limited), however the resistive losses of the Al magnet system would be _≈_ 90 MW at 20 K equivalent to a huge cryocooler electric power 1.35 GWe. Our calculations show why superconductivity is a disruptive technology for fusion: resistive magnets in a fusion power plant would consume most of the power (and sometimes more) than the plant would produce. At room temperature, huge levels of power are needed to drive the magnets themselves. At cryogenic temperatures, equally huge levels of power would be required to drive the cryoplant. 

Finally we note that plasma control is more demanding with resistive magnets compared to superconducting ones. When the current changes in a resistive magnet, along with the magnetic field changing, the temperature and the size of the magnets change because of the thermal expansion of the various components. In the superconducting case, the current does not substantially heat the magnets so the differential thermal properties of the component parts of the tokamak play little role. We have not included any calculations for the cost of robotic replacement of resistive parts, which will almost certainly be cheaper than removing and installing brittle superconducting components. However, we have not proceeded any further with calculations for resistive magnets given their huge power demands, and that we feel the magnetoresistance of copper and aluminium is well enough understood that no significant reduction in the magneto-resistivity is likely. Our calculations, table 14, show that even if we could find some way for the plasma to perform well beyond current expectations at _H_ 98 = 1.6, we might get a little electricity. In the context of identifying the remaining challenges of making fusion energy commercial, engineering large robotically-remountable superconducting magnets is best explicitly included for clarity of purpose [173]. Unfortunately resistive magnets are a very mature technology and history teaches us what inevitably happens to technologies that can’t evolve, if they compete commercially with a continuously improving disruptive technology - superconductivity. Hence, we set aside considering large resistive magnets in the tokamak for the rest of the paper. 

## **7. Future Technological Developments** 

Magnet technology is a rapidly evolving field. In this section we address whether the inevitable improvements in technology that are on the horizon are likely to bring significant cost reductions. We discuss how increases in structural steel yield stress (which we use as a proxy for both improved strength of materials and improved magnet design support architectures) and how reductions in REBCO cost would affect our preferred reactor design and capital cost. Then we discuss the utility of producing some new fusion-specific high _B_ c2 superconductors, some disruptive designs and finally some general comments about future costs of tokamaks. 

## _7.1. Novel Support Architectures and Strengthened Steels_ 

Although it seems unlikely that the strength of (steel) materials will very siginficantly be increased (eg that the Tresca yield criterion (used in PROCESS) will be increased much beyond 660 MPa - 2/3 yield strength of 316LN steel [76]), improved designs of the external support structures such as those proposed for the ARC reactor [5], do reduce the stresses on the TF coils. For example, the ARC support rings at the top and bottom of the TF coils resist both toroidal and vertical forces, and have been shown to increase very markedly the possible fields on plasma. In figure 10, data are included for increasing the TF and CS coils’ operational stress limits for various inflated costs of complete structural steel components; representative of increased cost of enhanced steels or increased volumes of steel used in advanced support architectures. Also shown are data for decreased cost versus increased stress limits, which are a proxy for improvements in design rather than the steel itself. Increasing the TF and CS coils’ operational stress limits to 1000 MPa in our preferred choice reactor increases the cost-optimal field on coil to 14.4 T ( _B_ plasma = 6 _._ 3 T) and reduces the capital cost to 3920 M$ (assuming steel costs do not change). With larger allowed stresses the field increases further, plateauing by _≈_ 2000 MPa with a field on coil of 16.8 T ( _B_ plasma = 7 _._ 7 T) and capital cost of 3690 M$ (due to the _P_ sep _/R_ major = 20 MW/m _[−]_[1] limit). These magnetic fields approach those of the SPARC and ARC tokamaks (cf Table 1) that include more advanced designs of the TF coils. However, the trade-off between the reduction in reactor capital cost associated with a reduction in reactor volume enabled by larger toroidal fields, and the additional cost of the support structure required to reach these fields means, as shown in figure 10, that the capital cost reductions are modest. 

## _7.2. Fusion-Specific Superconducting Materials_ 

The superconducting strands and tapes currently used to develop cables for fusion tokamaks were optimised for other applications. The Nb47%wt.Ti alloy used in ITER was developed for the MRI market to maximise _J_ c between 4-6 T; the Nb3Sn strands were developed for particle accelerator magnets to maximise _J_ c between 8-10 T; and the aim of the REBCO industry has focussed on developing higher _J_ c tapes (at reduced cost) 

for power applications and ultra high field magnets. REBCO cables for tokamaks are currently being optimised for immediate use - CORC [174], slotted core cables [36, 175], twisted-stack cables [176, 177]) - but commercial fusion will drive the development of new REBCO conductors. As we have seen in section 6, the huge fusion magnets in our optimised REBCO design include magnet support structures that are stress limited. Indeed, the critical current density of the REBCO tapes is already two orders of magnitude larger than current density of the winding pack, which opens the possiblity of developing cheaper, lower _J_ c tapes (that are already available) and that can also help mitigate other important issues such as quench mitigation and brittle fracture. We note for example that were commercial quaternary Nb-Ti training magnets available, they would produce a 10 - 20 % larger field fraction than conventional Nb-Ti - an increase driven solely by the alloy’s larger upper critical field. 

It is a concern for rapid commercialisation of fusion energy that commercial HTS manufacturing capability is modest. Nevertheless, fusion power plants represent a multibillion-dollar market for high temperature superconductors, and ITER demonstrates a precedent for rapid growth in superconductor manufacturing capacity when required. ITER required _≈_ 600 tons Nb3Sn strands [129] which led to a rapid increase in annual global production from _<_ 2 ton/year in the early 1990s to 100 tons/year today [178]. Equally, REBCO tapes have seen a substantial decrease in production cost in the two decades [137] and it is likely that this will continue as global demand increases - note that doubling superconductor _J_ c (for the same manufacturing cost) has the same effect as halving cost in $/kA m, see equation 9. Remaining focused on our preferred choice reactor design, if we reduced the REBCO cost from 30 $/kA m (6 T, 4.2 K) to make it almost free (0.025 $/kA m (6 T, 4.2 K), the resulting capital cost minimised reactor has an increased toroidal field of 12.7 T and a capital cost reduced from 4230 M$ to 4000 M$. It is noteworthy that these very modest changes in cost are less than those obtained by increasing the steel stress limits. We conclude that a reduction in REBCO cost beyond those presented in [137] would not offer much benefit in overall reactor cost as the cable cost and design-limiting factors are dominated by non-superconducting components. 

## _7.3. Driving down Costs_ 

Paymasters inevitably ask whether there may be any developments in the future that are likely to substantially reduce costs. For fusion technology this will be informed by the commercial research that will be completed using the prototype, and that may enable some additional reductions in costs or improvements in operation. 

In this context, the exciting very high field values for the ARC and SPARC tokamaks (noted in Table 1) using high temperature superconductors, can be seen as both derisking a fully integrated tokamak with high power density and gain, while also enabling a search for more stable plasma operation at the highest fields available. However, small tokamaks bring high power fluxes and make radiation-hard robotic handling more challenging, and remind us that there may be more than one successful 

approach to commercial fusion technology. 

If we use our minimum cost approach using `PROCESS` to consider a tokamak with a TBR reduced from 1.1 to 0.9, it produces a capital cost reduction of _≈_ 24 % , not just from the reduction in the cost of the blanket (which makes up _≈_ 12 % of the preferred reactor direct cost, see table 2) but also by reducing the reactor volume (by reducing the inboard and outboard blanket modules’ thicknesses by 64 %) by 28 %. Given that magnetic technology is the primary driver for the tokamak size and hence cost, we again use the the maximum yield stresses as a proxy for better design of/stress management in the TF and CS coils and set it (unrealistically high) to 1000 MPa. We also set the REBCO cost unrealistically low to 0.025 $/kA m, the H-factor set to _H_ 98 = 1.8 and the limit on the power through the separatrix was increased to _P_ sep _/R_ = 25 MW as further proxies for reasonable improvements in design and materials improvements. These (unrealistic nay extreme) choices provide a means to find just how sensitive capital cost can be to future developments. All other constraints from our preferred choice reactor were retained. Under these conditions, the optimised reactor has a field on plasma of 5.7 T, field on TF coil of 14.0 T, peak field on CS coil of 12.4 T, plasma current of 9.7 MA, major radius of 5.37 m, aspect ratio of 3.36 and a capital cost of 3400 M$. This leads to a cost only 19.5 % lower than our preferred reactor. 

To drive costs down even further and pursue the cost of a cheapest possible tokamak demonstrator, we combined these approaches to consider a machine that only produced enough electricity to break-even, but would otherwise demonstrate all the core magnet technologies, capabilities of the blanket and successful coupling to electricity generating turbines. Keeping the same low REBCO costs, allowable maximum of the shear stresses and burn time as in our preferred reactor, with a TBR = 0.9, such a tokamak would need to produce _≈_ 560 MW fusion power and would have a capital cost of 3170 M$, about 31 % lower compared to our preferred reactor. The reduced blanket size would allow for a more compact _R_ major = 6.2 m, operating with a field on plasma of 6.1 T and field on TF coil of 12.5 T. These calculations show the limitations of the further cost reductions that are possible. We suggest that finalising the best tokamak to build would include consideration of the possible potential developments in fusion-focused high B _c_ 2 alloys, as well as whether or not large fusion power plants are inevitably the commercial endgame. We conclude that if we require retaining the CSC, we can reduce the cost by up to one third if we reduce the performance and fast-track design and material improvements. Naturally, investors (who have so far invested more than $ 2.4 B) [179] would want to ensure that such a reduction in cost and performance nevertheless still de-risks the commercial build. 

## **8. Discussion** 

The scientific evidence for the climate emergency [180] and the damage it is causing is now sufficiently clear [181, 182] that there is a global commitment to zero carbon [183]. For example, the UK Government has banned the sale of new cars powered solely by 

petrol or diesel from 2030 [184] and a legally binding commitment to “at least” zero carbon by 2050 [185]. 

Market-ready, intermittent solar and wind resources are the natural place to start. However the decarbonisation commitments to replace the carbon fuels used both in power stations and in transportation in the UK, will require several orders of magnitude more green electricity than is currently planned for. Unfortunately, unlike other low-CO2 energy sources, although a relatively small power plant can de-risk the holistic integration and operation of the key-technologies for commercial fusion, cost of electricity will eventually drive commercial fusion power plants to be large [138] (as is the standard for fission plants; Hinkley C will produce _>_ 3 GWe [186]. To what degree fusion power will be used to provide base-load electricity directly [187], rather than produce synthetic fuel for say aviation [188], or hydrogen [189], or conversion of carbon dioxide back into carbon black [190]) or reduce methane [191] are open questions that will depend on the particular commercial realities of global warming when commercial fusion energy arrives, and whether we will need it to reverse global warming. 

Fusion energy is clearly a huge-risk huge-return investment that only a relatively small group of wealthy Governments [4, 13, 192, 193] or philanthropic billionaires [194] can lead. Much more work is needed to bring the scientists, policy makers, investors, defence interests, and public together to de-risk fusion power and make it commercial as quickly as possible. Even the excellent texts that deal with the science of renewable energy [195] or the economic opportunity (or green premium) it presents [196], hardly mention fusion at all. Fusion technology is quite different from other renewable technologies in that the scale of investment required to make meaningful commercial advances is much larger. Of course there have been huge projects in the past, including space travel (i.e. putting the first man on the moon [197] and the development of fission power). Those projects had straightforward aims and welldefined competitive environments, but crucially, did not have to broadly operate in the free-market while being commercialised. Commercialising fusion is far more complex. The green changes that are underway were not driven by the free-market, but by an unprecedented alignment of public social awareness and enlightened policy. However in order for the commercialisation of fusion energy to be a success, it must roll-out across the developed world on a huge scale. It therefore needs the resources and skills of the markets with commensurate and proper financial returns for investors. 

The approach for designing, financing and building the last fusion tokamak before commercialisation requires very careful planning. There are precedents for Governments simply outsourcing everything, and it leads to poor management [198]. Managing the process to commercialise fusion energy will require an approach that is more than that of just an ‘intelligent business’ that knows what it needs. Experience suggests that an ‘intelligent customer’ will be needed that includes an extremely capable inhouse capability, that can manage procurement, understand opportunities and potential innovation on the horizon, as well as integrate the programme into (changing) overall policies and structures [199]. Of course the scientific challenges addressed in this paper 

and required to develop commercial fusion are huge. But perhaps as challenging is developing an in-house management environment to roll-out fusion that attracts the required calibre of personnel with the relevant scientific, financial and administrative skills, and that provides a clear career development path for early career staff while retaining and developing its in-house expertise over a protracted capital-rich period of investment [198]. 

In this paper we focus on our ‘preferred choice’ 100 MWe REBCO TF,CS and NbTi PF tokamak with a plasma fusion gain _Q_ plasma = 17, a net gain _Q_ net = 1.3. The machine it is most similar to in size is ITER (cf Table 1). In a competitive commercial environment, the best machine must be sufficiently close to market to de-risk all the key technologies, provide a working demonstrator and a cost for producing fusion energy that the markets can rely on. Analysis of the power balance and direct capital cost for this preferred reactor are shown in figure 11. The magnets are a single-point of failure for the entire project so we have mitigated damage to the brittle and expensive magnets by recommending the use of Nb-Ti training coils for the preferred choice reactor. Such training coils would increase overall preferred reactor capital cost by _<_ 10%, and would allow for the thorough testing of the reactor (at 70 % field on TF coil 66 % field on CS coil) - reducing the risk of damage to the full-power REBCO magnets. The training coils are re-usable, so the increase in cost can shared across say 10 tokamaks meaning the increased cost per tokamak is rather marginal at only 1 % [150]. These considerations hold for machines both with higher H98 = 1.6 and for the 500 MWe scale. The cost of electricity is expensive from our preferred choice 550 $ MW _[−]_[1] h _[−]_[1] , compared to 50100 $ MW _[−]_[1] h _[−]_[1] for fossil fuels or solar/wind (in 1990 US $) - equivalent to 1148 $ MW _[−]_[1] h _[−]_[1] and 100-200 $ MW _[−]_[1] h _[−]_[1] respectively in 2021 US$ costs [200]. However, the primary aim of this paper is to minimise the capital cost of de-risking commercial fusion technology, not produce cheap electricity. The 500 MWe machine produces electricity at a lower cost of 290 $ per MW h, a plasma fusion gain _Q_ plasma = 41, a net gain _Q_ net = 1.9, demonstrating the benefits of large scale plants [138]. 

We have identified two areas of research that should be prioritised by the fusion community: Measurements and theoretical calculations are required to evaluate the properties of superconductors shielded but exposed to a fusion-like flux as a matter of urgency. MCNP calculations have been extended down to photon energies of 1 eV [96], but need to be extended to consider even lower energies of order the superconducting gap (of order 10 meV). Perhaps even more challenging will then be developing the calculations and understanding of the superconducting state in such a photon and neutron flux; The development of high _Bc_ 2 multifilamentary superconducting alloys that will bring ductility, more straightforward robotic handling and maintenance of the magnets, and enhanced radiation tolerance (without requiring very high critical current density), opens the possibility to eliminate the need in large commercial machines to use the brittle HTS superconducting materials. We have concluded that superconducting magnets are the enabling technology for commercialisation of fusion power and that resistive magnets on any large scale are an unhelpful diversion of resources. 

Finally we return to consider the global imperatives of net zero carbon economies with huge base-load electricity needs [201]. These requirements have an obvious solution using nuclear power. Nuclear fission plants are currently the only commercial nuclear option [202], but bring with them a current estimated cost of £132 billion (UK 2020) to decommission the UK’s current civil nuclear waste [203]. We haven’t costed managing the nuclear waste for fusion power here, but support the intention for fusion technology to have no high level waste after 100 years (i.e. after the iron and cobalt isotopes have decayed) [26, 11, 27, 204] which brings public support for nuclear fusion power with it and remains essential [205]. 

## **9. Conclusions** 

Prototype fusion reactors must demonstrate a commercial viability that proves fusion is a key option for large scale decarbonisation of global electricity production. To this end, here we have used the `PROCESS` systems code to minimise the capital cost of superconducting tokamak pilot plants using best-in-class technologies available on the time scales of 2035-2040. Should the cost of REBCO continue to fall and reach the expected 30 $/kA m (6 T, 4.2 K) [137], our preferred reactor which uses REBCO CS and TF coils and Nb-Ti PF coils has a lower capital cost than a reactor with Nb3Sn CS and TF coils, or an entirely Nb-Ti reactor. This preferred reactor has _R_ major = 6.75 m, _A_ = 3.15, _P_ fusion = 870 MW, _Qplasma_ = 17, _Qnet_ = 1.3, _BT_ = 5.4 T and _B_[max][12.5][T.][The][cost][of][the][preferred][REBCO][power][plant][is][$][4230][M][(US][1990)] t,coil[=] (cf Table 7), but if we use training magnets the total cost only increases to $ 4.54 Bn (US 1990) equivalent to $ 9.75 Bn (US 2021). We find the cost-optimal winding pack current density and field on coil is limited by the yield stress of the steel support structure and not the critical current density of the REBCO superconductor. In order to achieve the necessarily high availability of a base-load power plant we assert that commercial tokamaks must have remountable magnets, and hence a prototype reactor must also demonstrate them. Remountability offers the possibility of easily swapping superconductors at different stages during a reactor lifetime. Here we have focused on using robust Nb-Ti training coils during plant commissioning in order to protect the brittle REBCO magnets from powerful disruptions as a result of operator inexperience, manufacturing errors etc. The full power magnets would then be mounted for full-power operation. The addition of Nb-Ti training coils for reactor commissioning increases costs by _<_ 10 % and would allow for thorough reactor testing (generating 70 % field on TF, 66 % field on CS of the preferred reactor). We also suggest that the fusion community should commit itself to: developing higher _B_ c2 alloys dedicated to fusion applications [126, 127]. They would aim to displace current commercial Nb-Ti, and because of their ductility also may displace high temperature superconductors for fusion magnets; measure the critical current density of superconductors under operational conditions (bathed in an n+p sea at cryogenic temperatures). 

We conclude: the cost of building the human resources, engineering processes, 

supply chains, and capital-intensive demonstrator power plant that is the last one before commercialisation will not change significantly (against inflation) over the next few decades; all the relevant information is available now for the complex scientific and economic choices to be made about de-risking and then building a state-of-theart tokamak. It should include all the key technologies and identify whether fission power plants can be replaced on a commercial footing by fusion power plants that produce no long-term high-level waste, reduce proliferation of nuclear weapons in a increasingly carbon-free world, and provide long-term energy security for base load electricity production. 

## **10. Acknowledgements** 

This work is funded by EPSRC grant EP/L01663X/1 that supports the EPSRC Centre for Doctoral Training in the Science and Technology of Fusion Energy. The data are available at: http://dx.doi.org/10.15128/r24q77fr362 and associated materials are on the Durham Research Online website: http://dro.dur.ac.uk/. We would like to thank, A. Turner and J. Naish for the MCNP calculations, as well as M. Kovari, J. Morris, S. Muldrew, S. Kahn, A. Blair, M. Coleman, P. Daniels, P. Bruzzone, K. Sedlak, S. Thomas, B. Davies, S. Frank, F. Schoofs, J. Schwartz, and also M. Raine, J. Greenwood, C. Gurnham and B. Din for their expertise and helpful discussions. 

## **References** 

- [1] Aymar R, Barabaschi P, Shimomura Y and design team I 2002 _Plasma Physics and Controlled Fusion_ **44** 519–565 ISSN 0741-3335 URL `https://iopscience.iop.org/article/10.1088/ 0741-3335/44/5/304/pdf` 

- [2] Creely A J, Greenwald M J, Ballinger S B, Brunner D, Canik J, Doody J, F¨ul¨op T, Garnier D T, Granetz R, Gray T K, Holland C, Howard N T, Hughes J W, Irby J H, Izzo V A, Kramer G J, Kuang A Q, LaBombard B, Lin Y, Lipschultz B, Logan N C, Lore J D, Marmar E S, Montes K, Mumgaard R T, Paz-Soldan C, Rea C, Reinke M L, Rodriguez-Fernandez P, S¨arkim¨aki K, Sciortino F, Scott S D, Snicker A, Snyder P B, Sorbom B N, Sweeney R, Tinguely R A, Tolman E A, Umansky M, Vallhagen O, Varje J, Whyte D G, Wright J C, Wukitch S J and Zhu J 2020 _Journal of Plasma Physics_ **86** 865860502 ISSN 0022-3778 URL `https://www.cambridge.org/ core/article/overview-of-the-sparc-tokamak/DD3C44ECD26F5EACC554811764EF9FF0` 

- [3] Federici G, Bachmann C, Barucca L, Biel W, Boccaccini L, Brown R, Bustreo C, Ciattaglia S, Cismondi F, Coleman M, Corato V, Day C, Diegele E, Fischer U, Franke T, Gliss C, Ibarra A, Kembleton R, Loving A, Maviglia F, Meszaros B, Pintsuk G, Taylor N, Tran M Q, Vorpahl C, Wenninger R and You J H 2018 _Fusion Engineering and Design_ **136** 729–741 ISSN 0920-3796 URL `http://www.sciencedirect.com/science/article/pii/S0920379618302898` 

- [4] UK Atomic Energy Authority 2020 Spherical tokamak for energy production accessed 2020/02/19 URL `https://step.ukaea.uk/` 

- [5] Sorbom B N, Ball J, Palmer T R, Mangiarotti F J, Sierchio J M, Bonoli P T, Kasten C, Sutherland D A, Barnard H S, Haakonsen C B, Goh J, Sung C and Whyte D G 2015 _Fusion Engineering and Design_ **100** 378–405 

- [6] Balshaw N 2018 A collection of sensational technical ‘factoids’ for jet tour guides (internal document) 

- [7] Riccardo V, Hender T C, Lomas P J, Alper B, Bolzonella T, Vries P d, Maddison G P and Contributors t J E T E 2004 _Plasma Physics and Controlled Fusion_ **46** 925–934 ISSN 07413335 1361-6587 URL `http://dx.doi.org/10.1088/0741-3335/46/6/001` 

- [8] Riccardo V, Arnoux G, Cahyna P, Hender T C, Huber A, Jachmich S, Kiptily V, Koslowski R, Krlin L, Lehnen M, Loarte A, Nardon E, Paprok R and Tskhakaya D 2010 _Plasma Physics and Controlled Fusion_ **52** 124018 ISSN 0741-3335 1361-6587 URL `http://dx.doi.org/10.1088/ 0741-3335/52/12/124018` 

- [9] de Vries P C, Johnson M F, Alper B, Buratti P, Hender T C, Koslowski H R and Riccardo V 2011 _Nuclear Fusion_ **51** 053018 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10. 1088/0029-5515/51/5/053018` 

- [10] Private communication with Prof. Hampshire. Confidential 2022/02/11 

- [11] Gilbert M R, Eade T, Bachmann C, Fischer U and Taylor N P 2018 _Fusion Engineering and Design_ **136** 42–48 ISSN 0920-3796 URL `https://www.sciencedirect.com/science/ article/pii/S0920379617309717` 

- [12] Lubell M S and Clinard J A 1988 _IEEE Transactions on Magnetics_ **24** 761–766 

- [13] 2021 Bringing fusion to the u.s. grid Report National Academies of Sciences Engineering and Medicine URL `https://doi.org/10.17226/25991.` 

- [14] Tobita K, Hiwatari R, Sakamoto Y, Someya Y, Asakura N, Utoh H, Miyoshi Y, Tokunaga S, Homma Y, Kakudate S, Nakajima N and for Fusion Demo t J S D T 2019 _Fusion Science and Technology_ **75** 372–383 ISSN 1536-1055 URL `https://doi.org/10.1080/15361055.2019. 1600931` 

- [15] Neil M, Jinxing Z, Christian V, Valentina C, Charlie S, Michael S, Brandon Nils S, Robert Andrew S, Greg B, Rod B, Yasuyuki M, Nobuya B, Kasuyoshi S, Anna K, Herman H J T K, Pierluigi B, Rainer W, Thierry S, Nikolay B, Alexey D, Matthias G T M, Franco Julio M, Kamil S, David E, Danko C v d L, Jeremy D W, Min L and Gen L 2021 _Superconductor Science and Technology_ ISSN 0953-2048 URL `http://iopscience.iop.org/article/10.1088/1361-6668/ac0992` 

- [16] United Nations 2021 Secretary-general calls latest ipcc climate report ‘code red for humanity’, stressing ‘irrefutable’ evidence of human influence accessed 2021/10/26 URL `https://www. un.org/press/en/2021/sgsm20847.doc.htm` 

- [17] Chislett-McDonald S B L, Kovari M, Surrey E and Hampshire D P 2020 How to train your tokamak: by swapping re-mountable superconducting magnets presented at Symposium on Fusion Technology 2020 

- [18] Kovari M, Kemp R, Lux H, Knight P, Morris J and Ward D J 2014 _Fusion Engineering and Design_ **89** 3054–3069 ISSN 09203796 URL `https://www.sciencedirect.com/science/ article/pii/S0920379614005961?via%3Dihub` 

- [19] Kovari M, Fox F, Harrington C, Kembleton R, Knight P, Lux H and Morris J 2016 _Fusion Engineering and Design_ **104** 9–20 ISSN 09203796 

- [20] Power Plant Technology Group, United Kingdom Atomic Energy Authority 2017 PROCESS: A systems code for fusion power plants version 2.0.4 

- [21] 2021 CPI inflation calculator URL `https://www.bls.gov/data/inflation_calculator.htm` 

- [22] Oishi T, Yamazaki K, Arimoto H, Ban K, Kondo T, Tobita K and Goto T 2012 _Plasma and Fusion Research_ **7** 2405115–2405115 

- [23] 2001 Final report of the iter eda Report IAEA IAEA/ITER EDA/DS/21 

- [24] IHS- CERA US power plant costs accessed 2022/02/18 URL `https://ihsmarkit.com/info/ cera/ihsindexes/index.html` 

- [25] Goorley T, James M, Booth T, Brown F, Bull J, Cox L J, Durkee J, Elson J, Fensin M, Forster R A, Hendricks J, Hughes H G, Johns R, Kiedrowski B, Martz R, Mashnik S, McKinney G, Pelowitz D, Prael R, Sweezy J, Waters L, Wilcox T and Zukaitis T 2012 _Nuclear Technology_ **180** 298–315 ISSN 0029-5450 URL `https://doi.org/10.13182/NT11-135https: //www.tandfonline.com/doi/abs/10.13182/NT11-135` 

- [26] Gilbert M R, Eade T, Bachmann C, Fischer U and Taylor N P 2017 _Nuclear Fusion_ **57** 046015 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/aa5bd7` 

- [27] Gilbert M R, Eade T, Rey T, Vale R, Bachmann C, Fischer U and Taylor N P 2019 _Nuclear Fusion_ **59** 076015 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/ab154e` 

- [28] 1998 Radiological characterization of shutdown nuclear reactors for decomissioning purposes Report International Atomic Energy Agency 

- [29] Damiani C, Palmer J, Takeda N, Annino C, Balagu´e S, Bates P, Bernal S, Cornell´a J, Dubus G, Esqu´e S, Gonzalez C, Ilkei T, Lewczanin M, Locke D, Mont L, Perrier B, Puiu A, Ruiz E, Shuff R, Van De Ven N, Van Hille C, Van Uffelen M, Choi C H, Friconneau J P, Hamilton D, Martin J P, Murakami S, Reichle R, Cuevas J S, Maruyama T, Noguchi Y and Saito M 2018 _Fusion Engineering and Design_ **136** 1117–1124 ISSN 0920-3796 URL `http://www.sciencedirect.com/science/article/pii/S0920379618303739` 

- [30] Keep J, Wood S, Gupta N, Coleman M and Loving A 2017 _Fusion Engineering and Design_ **124** 420–425 ISSN 0920-3796 URL `https://www.sciencedirect.com/science/article/ pii/S0920379617300996` 

- [31] Hampshire D P Granted 2018 URL `https://worldwide.espacenet.com/publicationDetails/ biblio?DB=worldwide.espacenet.com&II=0&ND=3&adjacent=true&locale=en_EP&FT=D& date=20181114&CC=GB&NR=2562385A&KC=A` 

- [32] Powell J, Hsieh S, Danby G, Bezler P, Gardner D, Laverick C, Finkelman M, Brown T, Bundy J, Balderes T, Zatz I, Verzera R and Herbermann R 1980 _Cryogenics_ **20** 59 – 74 

- [33] Hashizume H and Ito S 2014 _Fusion Engineering and Design_ **89** 2241–2245 

- [34] Hartwig Z S, Haakonsen C B, Mumgaard R T and Bromberg L 2012 _Fus. Eng. and Design_ **87** 201 

- [35] Mangiarotti F J and Minervini J V 2015 _IEEE Transactions on Applied Superconductivity_ **25** 1–5 ISSN 1558-2515 

- [36] Hartwig Z S, Vieira R F, Sorbom B N, Badcock R A, Bajko M, Beck W K, Castaldo B, Craighill C L, Davies M, Estrada J, Fry V, Golfinopoulos T, Hubbard A E, Irby J H, Kuznetsov S, 

Lammi C J, Michael P C, Mouratidis T, Murray R A, Pfeiffer A T, Pierson S Z, Radovinsky A, Rowell M D, Salazar E E, Segal M, Stahle P W, Takayasu M, Toland T L and Zhou L 2020 _Superconductor Science and Technology_ **33** 11LT01 ISSN 0953-2048 1361-6668 URL `http://dx.doi.org/10.1088/1361-6668/abb8c0` 

- [37] Weiss J, van der Laan D, Allen S, Holt J, Alsworth I, Daniels P and Schoofs F 2021 Development of low-resistance CORC-CICC joints for use in demountable magnets for fusion and their performance up to 10 kA within a background magnetic field of up to 8 T. presented at EUCAS 2021, Moscow 

- [38] Bruzzone P, H Fietz W, V Minervini M, Novikov M, Yanagi N, Zhai Y and Zheng J 2018 _Nuclear Fusion_ **58** 103001 ISSN 0029-5515 URL `http://stacks.iop.org/0029-5515/58/i= 10/a=103001` 

- [39] Tsui Y, Surrey E and Hampshire D P 2016 _Supercond. Sci. and Technology_ **290** 075005 

- [40] Taylor N, Merrill B, Cadwallader L, Di Pace L, El-Guebaly L, Humrickhouse P, Panayotov D, Pinna T, Porfiri M T, Reyes S, Shimada M and Willms S 2017 _Nuclear Fusion_ **57** 092003 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/57/9/092003` 

- [41] Sykes A, Costley A E, Windsor C G, Asunta O, Brittles G, Buxton P, Chuyanov V, Connor J W, Gryaznevich M P, Huang B, Hugill J, Kukushkin A, Kingham D, Langtry A V, McNamara S, Morgan J G, Noonan P, Ross J S H, Shevchenko V, Slade R and Smith G 2018 _Nuclear Fusion_ **58** 016039 ISSN 0029-5515 URL `http://stacks.iop.org/0029-5515/58/i=1/a=016039` 

- [42] McDonald D C, Cordey J G, Thomsen K, Kardaun O J W F, Snipes J A, Greenwald M, Sugiyama L, Ryter F, Kus A, Stober J, DeBoo J C, Petty C C, Bracco G, Romanelli M, Cui Z, Liu Y, Miura Y, Shinohara K, Tsuzuki K, Kamada Y, Takizuka T, Urano H, Valovic M, Akers R, Brickley C, Sykes A, Walsh M J, Kaye S M, Bush C, Hogewei D, Martin Y R, Cote A, Pacher G, Ongena J, Imbeaux F, Hoang G T, Lebedev S, Chudnovskiy A and Leonov V 2007 _Nuclear Fusion_ **47** 147 ISSN 0029-5515 URL `http://stacks.iop.org/0029-5515/47/i=3/a=001` 

- [43] Kaye S M, Bell M G, Bell R E, Fredrickson E D, LeBlanc B P, Lee K C, Lynch S and Sabbagh S A 2006 _Nuclear Fusion_ **46** 848–857 ISSN 0029-5515 1741-4326 

- [44] Buxton P F, Connor J W, Costley A E, Gryaznevich M P and McNamara S 2019 _Plasma Physics and Controlled Fusion_ **61** 035006 ISSN 0741-3335 1361-6587 URL `http://dx.doi.org/10. 1088/1361-6587/aaf7e5` 

- [45] Costley A E and McNamara S A M 2021 _Plasma Physics and Controlled Fusion_ **63** 035005 ISSN 0741-3335 1361-6587 URL `http://dx.doi.org/10.1088/1361-6587/abcdfc` 

- [46] Valoviˇc M, Akers R, Cunningham G, Garzotti L, Lloyd B, Muir D, Patel A, Taylor D, Turnyanskiy M and Walsh M 2009 _Nuclear Fusion_ **49** ISSN 0029-5515 1741-4326 

- [47] Valoviˇc M, Akers R, Bock M d, McCone J, Garzotti L, Michael C, Naylor G, Patel A, Roach C M, Scannell R, Turnyanskiy M, Wisse M, Guttenfelder W, Candy J and the M t 2011 _Nuclear Fusion_ **51** 073045 ISSN 0029-5515 URL `http://stacks.iop.org/0029-5515/51/i= 7/a=073045` 

- [48] Wade M R, Murakami M, Luce T C, Ferron J R, Petty C C, Brennen D P, Garofalo A M, Greenfield C M, Hyatt A W, Jayakumar R, Kinsley J E, La Haye R J, Lao L L, Lohr J, Politzer P A, Prater R, Strait E J and Watkins J G 2003 _Nuclear Fusion_ **43** 634–646 

- [49] Sips A C C 2005 _Plasma Physics and Controlled Fusion_ **47** A19 ISSN 0741-3335 URL `http: //stacks.iop.org/0741-3335/47/i=5A/a=003` 

- [50] Whyte D G, Minervini J, Marmar E S, Greenwald M J, LaBombard B, Bromberg L and Sorbom B M 2016 _Journal of Fusion Energy_ **35** 41–53 

- [51] Zohm H 2019 _Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences_ **377** 20170437 URL `https://doi.org/10.1098/rsta.2017.0437` 

- [52] Monneret E, Benkheira L, Fauve E, Henry D, Voigt T, Badgujar S, Chang H S, Vincent G, Forgeas A and Navion-Maillot N 2017 _IOP Conference Series: Materials Science and Engineering_ **171** 012031 ISSN 1757-8981 1757-899X URL `http://dx.doi.org/10.1088/1757-899X/171/ 1/012031` 

- [53] Strobridge T W 1974 _NBS technical note 655_ TN–655 

- [54] Simon N J, Drexler E S and Reed R P 1992 _NIST Monograph 177_ 

- [55] Kang R, Wang J and Xu Q 2021 Https://arxiv.org/abs/2109.03982, Accessed 2021/12/04 URL `https://arxiv.org/abs/2109.03982` 

- [56] Takayasu M 2020 _IEEE Transactions on Applied Superconductivity_ **30** 1–5 ISSN 1558-2515 

- [57] Ravaioli E, Davis D, Marchevsky M, Sabbi G, Shen T, Verweij A and Zhang K 2020 _Physica Scripta_ 015002 

- [58] Hern´andez F, Pereslavtsev P, Kang Q, Norajitra P, Kiss B, N´adasi G and Bitz O 2017 _Fusion Engineering and Design_ **124** 882–886 ISSN 0920-3796 URL `http://www.sciencedirect.com/science/article/pii/S0920379617300911https: //www.sciencedirect.com/science/article/pii/S0920379617300911?via%3Dihub` 

- [59] Federici G, Boccaccini L, Cismondi F, Gasparotto M, Poitevin Y and Ricapito I 2019 _Fusion Engineering and Design_ **141** 30–42 ISSN 0920-3796 URL `http://www.sciencedirect.com/ science/article/pii/S0920379619301590` 

- [60] Shimwell J, Kovari M, Lilley S, Zheng S, Morgan L W G, Packer L W and McMillan J 2016 _Fusion Engineering and Design_ **104** 34–39 ISSN 0920-3796 URL `http://www.sciencedirect.com/ science/article/pii/S0920379616300114` 

- [61] Kovari M, Coleman M, Cristescu I and Smith R 2017 _Nuclear Fusion_ **58** 026010 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/aa9d25` 

- [62] Martelli E, Del Nevo A, Arena P, Bongiov`ı G, Caruso G, Di Maio P A, Eboli M, Mariano G, Marinari R, Moro F, Mozzillo R, Giannetti F, Di Gironimo G, Tarallo A, Tassone A and Villari R 2017 _International Journal of Energy Research_ **42** 27–52 ISSN 0363-907X URL `https://doi.org/10.1002/er.3750` 

- [63] Tassone A, Nevo A D, Arena P, Bongiov`ı G, Caruso G, Maio P A d, Gironimo G d, Eboli M, Forgione N, Forte R, Giannetti F, Mariano G, Martelli E, Moro F, Mozzillo R, Tarallo A and Villari R 2018 _IEEE Transactions on Plasma Science_ **46** 1446–1457 ISSN 1939-9375 

- [64] Baluc N, Boutard J L, Dudarev S L, Rieth M, Correia J B, Fournier B, Henry J, Legendre F, Leguey T, Lewandowska M, Lindau R, Marquis E, Mu˜noz A, Radiguet B and Oksiuta Z 2011 _Journal of Nuclear Materials_ **417** 149–153 ISSN 0022-3115 URL `https://www. sciencedirect.com/science/article/pii/S0022311510008871` 

- [65] Pitts R A, Bonnin X, Escourbiac F, Frerichs H, Gunn J P, Hirai T, Kukushkin A S, Kaveeva E, Miller M A, Moulton D, Rozhansky V, Senichenkov I, Sytova E, Schmitz O, Stangeby P C, De Temmerman G, Veselova I and Wiesen S 2019 _Nuclear Materials and Energy_ **20** 100696 ISSN 2352-1791 URL `https://www.sciencedirect.com/science/article/pii/ S2352179119300237` 

- [66] Morris J, Asakura N, Homma Y, Hoshino K and Kovari M 2020 _IEEE Transactions on Plasma Science_ **48** 1799–1803 ISSN 1939-9375 

- [67] Xu G S, Yuan Q P, Li K D, Wang L, Xu J C, Yang Q Q, Duan Y M, Meng L Y, Yang Z S, Ding F, Liu J B, Guo H Y, Wang H Q, Eldon D, Tao Y Q, Wu K, Yan N, Ding R, Wang Y F, Ye Y, Zhang L, Zhang T, Zang Q, Li Y Y, Liu H Q, Jia G Z, Liu X J, Si H, Li E Z, Zeng L, Qian J P, Lin S Y, Xu L Q, Wang H H, Gong X Z and Wan B N 2020 _Nuclear Fusion_ **60** 086001 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/ab91fa` 

- [68] Wigram M R K, LaBombard B, Umansky M V, Kuang A Q, Golfinopoulos T, Terry J L, Brunner D, Rensink M E, Ridgers C P and Whyte D G 2019 _Nuclear Fusion_ **59** 106052 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/ab394f` 

- [69] Umansky M V, LaBombard B, Brunner D, Rensink M E, Rognlien T D, Terry J L and Whyte D G 2017 _Physics of Plasmas_ **24** 056112 ISSN 1070-664X URL `https://doi.org/10.1063/ 1.4979193` 

- [70] Ryutov D D and Soukhanovskii V A 2015 _Physics of Plasmas_ **22** 110901 ISSN 1070-664X URL `https://doi.org/10.1063/1.4935115` 

- [71] Ambrosino R, Castaldo A, Ha S, Loschiavo V P, Merriman S and Reimerdes H 2019 _Fusion_ 

_Engineering and Design_ **146** 2717–2720 ISSN 0920-3796 URL `https://www.sciencedirect. com/science/article/pii/S0920379619306350` 

- [72] Reimerdes H, Ambrosino R, Innocente P, Castaldo A, Chmielewski P, Di Gironimo G, Merriman S, Pericoli-Ridolfini V, Aho-Mantilla L, Albanese R, Bufferand H, Calabro G, Ciraolo G, Coster D, Fedorczak N, Ha S, Kembleton R, Lackner K, Loschiavo V P, Lunt T, Marzullo D, Maurizio R, Militello F, Ramogida G, Subba F, Varoutis S, Zag´orski R and Zohm H 2020 _Nuclear Fusion_ **60** 066030 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/ab8a6a` 

- [73] Lackner K and Zohm H 2013 _Fusion Science and Technology_ **63** 43–48 ISSN 1536-1055 URL `https://doi.org/10.13182/FST12-520` 

- [74] Asakura N, Hoshino K, Utoh H, Someya Y, Suzuki S, Bachmann C, Reimerdes H, Wenninger R, Kudo H, Tokunaga S, Homma Y, Sakamoto Y, Hiwatari R, Tobita K, You J H, Federici G, Ezato K, Seki Y, Ueda Y and Ohno N 2018 _Fusion Engineering and Design_ **136** 1214–1220 ISSN 09203796 URL `http://www.sciencedirect.com/science/article/pii/S0920379618303983` 

- [75] Narl Davidson J 1976 _Nuclear Fusion_ **16** 731–742 ISSN 0029-5515 1741-4326 URL `http: //dx.doi.org/10.1088/0029-5515/16/5/001` 

- [76] Hamada K, Nakajima H, Kawano K, Takano K, Tsutsumi F and Okuno K 2007 _Fusion Engineering and Design_ **82** 1481–1486 ISSN 0920-3796 URL `https://www.sciencedirect. com/science/article/pii/S0920379607003894` 

- [77] Titus P 2003 Structural design of high field tokamaks Report Plasma Science and Fusion Centre, Massachusetts Institute of Technology URL `https://core.ac.uk/download/pdf/78059375. pdf` 

- [78] Titus P 2018 Coil concepts for demo and next step reactors URL `https://nucleus.iaea.org/ sites/fusionportal/Shared%20Documents/DEMO/2018/3/Titus.pdf` 

- [79] Schultz J H, Antaya T, Feng J, Gung C Y, Martovetsky N, Minervini J V, Michael P, Radovinsky A, Titus P and Ieee 2006 _The ITER Central Solenoid_ 21st IEEE/NPSS Symposium on Fusion Engineering - SOFE 05 (New York: Ieee) ISBN 1-4244-0149-6 URL `<GotoISI>://WOS: 000241188700030` 

- [80] Morris J, Kemp R, Kovari M, Last J and Knight P 2015 _Fusion Engineering and Design_ **98-99** 1118–1121 ISSN 0920-3796 URL `http://www.sciencedirect.com/science/article/pii/ S0920379615301290` 

- [81] Franke T, Barbato E, Cardinali A, Ceccuzzi S, Cesario R, Eester D V, Lerche E, Mayoral M L, Mirizzi F, Nightingale M, Noterdaeme J M, Poli E, Tuccillo A A, Wenninger R and Zohm H 2014 _AIP Conference Proceedings_ **1580** 207–210 ISSN 0094-243X URL `https: //aip.scitation.org/doi/abs/10.1063/1.4864524` 

- [82] Raman R and Shevchenko V F 2014 _Plasma Physics and Controlled Fusion_ **56** 103001 ISSN 0741-3335 1361-6587 URL `http://dx.doi.org/10.1088/0741-3335/56/10/103001` 

- [83] Raman R, Jarboe T R, Nelson B A, Mueller D, Jardin S C, Neumeyer C, Ono M and Menard J E 2014 _IEEE Transactions on Plasma Science_ **42** 2154–2160 ISSN 1939-9375 

- [84] Sykes A, Akers R J, Appel L C, Arends E R, Carolan P G, Conway N J, Counsell G F, Cunningham G, Dnestrovskij A, Dnestrovskij Y N, Field A R, Fielding S J, Gryaznevich M P, Korsholm S, Laird E, Martin R, Nightingale M P S, Roach C M, Tournianski M R, Walsh M J, Warrick C D, Wilson H R, You S, Team M and Team N B I 2001 _Nuclear Fusion_ **41** 1423–1433 ISSN 0029-5515 URL `http://dx.doi.org/10.1088/0029-5515/41/10/310` 

- [85] Inomoto M, Watanabe T G, Gi K, Yamasaki K, Kamio S, Imazawa R, Yamada T, Guo X, Ushiki T, Ishikawa H, Nakamata H, Kawakami N, Sugawara T, Matsuyama K, Noma K, Kuwahata A and Tanabe H 2015 _Nuclear Fusion_ **55** 033013 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/55/3/033013` 

- [86] Chung K J, An Y H, Jung B K, Lee H Y, Sung C, Na Y S, Hahm T S and Hwang Y S 2013 _Plasma Science and Technology_ **15** 244–251 ISSN 1009-0630 URL `http://dx.doi.org/10. 1088/1009-0630/15/3/11` 

- [87] Gryaznevich M P and Sykes A 2017 _Nuclear Fusion_ **57** 072003 ISSN 0029-5515 1741-4326 URL 

`http://dx.doi.org/10.1088/1741-4326/aa4ffd` 

- [88] Ushigome M, Ide S, Itoh S, Jotaki E, Mitarai O, Shiraiwa S, Suzuki T, Takase Y, Tanaka S, Fujita T, Gohil P, Kamada Y, Lao L, Luce T, Miura Y, Naito O, Ozeki T, Politzer P, Sakamoto Y and Team t J T 2006 _Nuclear Fusion_ **46** 207–213 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/46/2/003` 

- [89] Darbos C, Henderson M, Albajar F, Bigelow T, Bomcelli T, Chavan R, Denisov G, Farina D, Gandini F, Heidinger R, Goodman T, Hogge J P, Kajiwara K, Kasugai A, Kern S, Kobayashi N, Oda Y, Ramponi G, Rao S L, Rasmussen D, Rzesnicki T, Saibene G, Sakamoto K, Sauter O, Scherer T, Strauss D, Takahashi K and Zohm H 2009 _AIP Conference Proceedings_ **1187** 531–538 ISSN 0094-243X URL `https://aip.scitation.org/doi/abs/10.1063/1.3273807` 

- [90] Hemsworth R S, Boilson D, Blatchford P, Palma M D, Chitarin G, de Esch H P L, Geli F, Dremel M, Graceffa J, Marcuzzi D, Serianni G, Shah D, Singh M, Urbani M and Zaccaria P 2017 _New Journal of Physics_ **19** 025005 ISSN 1367-2630 URL `http://dx.doi.org/10.1088/ 1367-2630/19/2/025005` 

- [91] Vontobel P and Pelloni S 1987 Jef/eff based nuclear data libraries Report URL `http://inis. iaea.org/search/search.aspx?orig_q=RN:19034790` 

- [92] Colling B 2016 _Blanket Performance and Radioactive Waste of Fusion Reactors: A Neutronics Approach_ Thesis Lancaster University 

- [93] Fischer D X, Prokopec R, Emhofer J and Eisterer M 2018 _Superconductor Science and Technology_ **31** 044006 ISSN 0953-2048 URL `http://stacks.iop.org/0953-2048/31/i=4/a=044006` 

- [94] Weber H W 2011 _International Journal of Modern Physics E_ **20** 1325–1378 ISSN 0218-3013 URL `https://doi.org/10.1142/S0218301311018526` 

- [95] Richard L S, Bonifetto R, Bottero U, Foussat A, Mitchell N, Seo K and Zanino R 2014 _IEEE Transactions on Applied Superconductivity_ **24** 1–4 ISSN 1558-2515 

- [96] Goorley T, James M, Booth T, Brown F, Bull J, Cox L J, Durkee J, Elson J, Fensin M, Forster R A, Hendricks J, Hughes H G, Johns R, Kiedrowski B, Martz R, Mashnik S, McKinney G, Pelowitz D, Prael R, Sweezy J, Waters L, Wilcox T and Zukaitis T 2016 _Annals of Nuclear Energy_ **87** 772–783 ISSN 0306-4549 URL `https://www.sciencedirect. com/science/article/pii/S0306454915000900` 

- [97] Mashnik S G 2011 _The European Physical Journal Plus_ **126** 49 ISSN 2190-5444 URL `https: //doi.org/10.1140/epjp/i2011-11049-1` 

- [98] Gilbert M R, Dudarev S L, Zheng S, Packer L W and Sublet J C 2012 _Nuclear Fusion_ **52** 

- [99] Chakin V P, Posevin A O and Latypov R N 2006 _Atomic Energy_ **101** 743–749 ISSN 1573-8205 URL `https://doi.org/10.1007/s10512-006-0162-9` 

- [100] Hofmann F, Mason D R, Eliason J K, Maznev A A, Nelson K A and Dudarev S L 2015 _Scientific Reports_ **5** 16042 ISSN 2045-2322 URL `https://doi.org/10.1038/srep16042` 

- [101] Newton I 1701 _Philosophical Transactions of the Royal Society of London_ **22** 824–829 URL `https://doi.org/10.1098/rstl.1700.0082` 

- [102] Varin S, Bonne F, Hoa C, Nicollet S, Zani L, Vallet J C, Fukui K and Natsume K 2020 _Cryogenics_ **109** 103092 ISSN 0011-2275 URL `http://www.sciencedirect.com/science/article/pii/ S0011227520300941` 

- [103] 2007 3. plant description: 3.1 magnets Report Japan Atomic Energy Agency accessed 2021/11/22 URL `http://www.jt60sa.org/pdfs/CDR/06-3.1_Magnets.pdf` 

- [104] Slade R A Pending 2019 Cable design in HTS tokamaks URL `https://patentimages.storage. googleapis.com/5a/a0/f8/fd75370480e502/US20190267171A1.pdf` 

- [105] Thermophysical properties of fluid systems URL `https://webbook.nist.gov/chemistry/ fluid/` 

- [106] Liu W T, Liu X H, Feng Y, Xie H J, Wang T C and Li J F 2010 _IEEE Transactions on Applied Superconductivity_ **20** 1504–1506 URL `https://ieeexplore.ieee.org/ielx5/77/5471713/ 05438876.pdf?tp=&arnumber=5438876&isnumber=5471713&ref=` 

- [107] Lee P J and Strauss B 2012 _Nb-Ti - from beginnings to perfection._ (National High Magnetic Field 

Laboratory) 

- [108] Chislett-McDonald S B L, Tsui Y, Surrey E, Kovari M and Hampshire D P 2020 _Journal of Physics: Conference Series_ **1559** 012063 ISSN 1742-6588 1742-6596 URL `http://dx.doi. org/10.1088/1742-6596/1559/1/012063` 

- [109] Sborchia M, Barbero Soto E, Batista R, Bellesia B, Bonito Oliva A, Boter Rebollo E, Boutboul T, E B, Caballero J, Comelis M, Fanthome J, Harrison R, Losasso M, Portone A, Rajainmaki H, Readman P and Valente P 2011 _IEEE/NPSS 24th Symposium on Fusion Engineering_ 1–8 

- [110] Shirai H, Barabaschi P and Kamada Y 2017 _Nuclear Fusion_ **57** 102002 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/aa5d01` 

- [111] Taylor D M J and Hampshire D P 2005 _Superconductor Science and Technology_ **18** S241–S252 

- [112] Cheggour N, Goodrich L F, Stauffer T C, Splett J D, Lu X F, Ghosh A K and Ambrosio G 2010 _Superconductivity Science and Technology_ **23** 052002 

- [113] Balachandran S, Tarantini C, Lee P J, Kametani F, Su Y F, Walker B, Starch W L and Larbalestier D C 2019 _Superconductor Science and Technology_ **32** 044006 URL `http://dx. doi.org/10.1088/1361-6668/aaff02` 

- [114] Bruzzone P, Sedlak K, Sarasola X, Stepanov B, Uglietti D, Wesche R, Muzzi L and Corte A d 2018 _IEEE Transactions on Applied Superconductivity_ **28** 1–5 ISSN 1051-8223 URL `https://ieeexplore.ieee.org/ielx7/77/8114526/08125755.pdf? tp=&arnumber=8125755&isnumber=8114526&ref=` 

- [115] Sedlak K, Bruzzone P, Sarasola X, Stepanov B and Wesche R 2017 _IEEE Transactions on Applied Superconductivity_ **27** 1–5 ISSN 1051-8223 URL `https://ieeexplore.ieee.org/ielx7/77/ 7753093/07744580.pdf?tp=&arnumber=7744580&isnumber=7753093&ref=` 

- [116] Bruzzone P 2011 _IEEE Transactions on Applied Superconductivity_ **21** 2036–2041 ISSN 1051-8223 URL `https://ieeexplore.ieee.org/ielx5/77/5776774/05643099.pdf?tp=&arnumber= 5643099&isnumber=5776774&ref=` 

- [117] Uglietti D, Sedlak K, Wesche R, Bruzzone P, Muzzi L and dellaCorte A 2018 _Superconductor Science and Technology_ **31** 055004 ISSN 0953-2048 URL `http://stacks.iop.org/ 0953-2048/31/i=5/a=055004` 

- [118] Commonwealth Fusion Systems 2021 Commonwealth fusion systems creates viable path to commercial fusion power with world’s strongest magnet URL `https://cfs.energy/ news-and-media/cfs-commercial-fusion-power-with-hts-magnet` 

- [119] Commonwealth Fusion Systems 2021 Highlights from the live-streamed 20 tesla hts magnet demo event accessed 2021/11/19 URL `https://www.youtube.com/watch?v=rAv6p3grFVM` 

- [120] Branch P, Osamura K and Hampshire D 2020 _Superconductor Science and Technology_ **33** 104006 ISSN 0953-2048 1361-6668 URL `http://dx.doi.org/10.1088/1361-6668/abaebe` 

- [121] Osamura K, Machiya S and Nishijima G 2016 _Superconductor Science and Technology_ **29** 094003 ISSN 0953-2048 URL `http://stacks.iop.org/0953-2048/29/i=9/a=094003` 

- [122] Barth C, Mondonico G and Senatore C 2015 _Superconductor Science and Technology_ **28** 

- [123] Maeda H and Yanagisawa Y 2014 _IEEE Transactions on Applied Superconductivity_ **24** 1–12 ISSN 1558-2515 

- [124] Lacroix C, Fournier-Lupien J, McMeekin K and Sirois F 2013 _IEEE Transactions on Applied Superconductivity_ **23** 4701605–4701605 ISSN 1558-2515 

- [125] Bonura M and Senatore C 2015 _Superconductor Science and Technology_ **28** 9 ISSN 09532048 URL `<GotoISI>://WOS:000351046300007https://iopscience.iop.org/article/10. 1088/0953-2048/28/2/025001/pdf` 

- [126] Horiuchi T, Monju Y and Nagai N 1973 _Japan Institute of Metals_ **37** 882–887 

- [127] Collings E W 1986 _Applied superconductivity, metallurgy, and physics of titanium alloys. Volume 1: fundamentals_ (New York: Plenum Press) 

- [128] Tinkham M 1996 _Introduction to Superconductivity_ 2nd ed (Singapore: McGraw-Hill Book Co.) 

- [129] Devred A, Backbier I, Bessette D, Bevillard G, Gardner M, Jong C, Lillaz F, Mitchell N, Romano G and Vostner A 2014 _Superconductor Science & Technology_ **27** 39 ISSN 0953- 

2048 URL `<GotoISI>://WOS:000334435900004https://iopscience.iop.org/article/10. 1088/0953-2048/27/4/044001/pdf` 

- [130] Keys S A and Hampshire D P 2003 _Superconductor Science and Technology_ **16** 1097–1108 

- [131] Dew-Hughes D 1974 _Philosophical Magazine_ **30** 293–305 URL `file://X:%5Ce_papers% 5CDew-Hughes%201974%2062.pdf` 

- [132] Wilson M N 1986 _Superconducting Magnets_ (Oxford, UK: Oxford University Press) ISBN 0 19 854810 0 

- [133] Tilley D R and Tilley J 1990 _Superfluids: An Introduction_ (Bristol: IOP publishing Ltd.) p 18 3rd ed 

- [134] Lu X F, Taylor D M J and Hampshire D P 2008 _Superconductor Science and Technology_ **21** 105016 

- [135] Nijhuis A, Wessel W A J, Knoopers H G, Ilyin Y, Corte A d and Kate H H J 2005 _IEEE Transactions on Applied Superconductivity_ **15** 3466–3469 ISSN 1558-2515 

- [136] Braccini V, Xu A, Jaroszynski J, Xin Y, Larbalestier D C, Chen Y, Carota G, Dackow J, Kesgin I, Yao Y, Guevara A, Shi T and Selvamanickam V 2010 _Superconductor Science and Technology_ **24** 035001 ISSN 0953-2048 1361-6668 URL `http://dx.doi.org/10.1088/0953-2048/24/3/ 035001` 

- [137] Cooley L and Pong I 2016 URL `https://indico.cern.ch/event/438866/ contributions/1085142/attachments/1257973/1858756/Cost_drivers_for_VHEPP_ magnet_conductors-v2.pdf` 

- [138] Lee T S, Jenkins I, Surrey E and Hampshire D P 2015 _Fusion Engineering and Design_ **98-99** 1072–1075 URL `https://www.sciencedirect.com/science/article/pii/ S0920379615301526?via%3Dihub` 

- [139] Yamada Y and Marchionini B 2015 High temperature superconductivity a roadmap for the electric power section Report International Energy Agency 

- [140] Bruzzone P 2021 Open issues and challenges for fusion magnets of future generations presented at Frontiers of Fusion 2021, University of York 

- [141] Sborchia C, Fu Y, Gallix R, Jong C, Knaster J and Mitchell N 2008 _IEEE Transactions on Applied Superconductivity_ **18** 463–466 ISSN 1051-8223 URL `<GotoISI>://WOS: 000256625700090https://ieeexplore.ieee.org/ielx5/77/4538104/04523021.pdf?tp= &arnumber=4523021&isnumber=4538104&ref=` 

- [142] Savoldi L, Brighenti A, Bonifetto R, Corato V, Muzzi L, Turt`u S and Zanino R 2017 _Fusion Engineering and Design_ **124** 45–48 ISSN 0920-3796 URL `https://www.sciencedirect.com/ science/article/pii/S0920379617306646` 

- [143] Wesche R, Sarasola X, Dicuonzo O, Ivashov I, Sedlak K, Uglietti D and Bruzzone P 2018 _Fusion Engineering and Design_ ISSN 0920-3796 URL `http://www.sciencedirect.com/science/ article/pii/S0920379618306896https://www.sciencedirect.com/science/article/ pii/S0920379618306896?via%3Dihub` 

- [144] Sarasola X, Wesche R, Ivashov I, Sedlak K, Uglietti D and Bruzzone P 2020 _IEEE Transactions on Applied Superconductivity_ **30** 1–5 ISSN 2378-7074 

- [145] Chislett-McDonald S B L, Surrey E and Hampshire D P 2019 _IEEE Trans. Appl. Supercond._ **29** 4200405–8 

- [146] Bardeen J, Cooper L N and Schrieffer J R 1957 _Physical Review_ **108** 1175–1204 

- [147] Wiesinger H P, Sauerzopf F M, Weber H W, Gerstenberg H and Crabtree G W 1992 _Europhysics Letters (EPL)_ **20** 541–546 ISSN 0295-5075 1286-4854 URL `http://dx.doi.org/10.1209/ 0295-5075/20/6/012` 

- [148] Andersen K 2021 23rd national school on neutron and x-ray scattering URL `https://www. dropbox.com/s/mst8yjyl6vb0yvp/Andersen%20NXSchool%202021%20-v3.pdf?dl=0` 

- [149] Joffrin E, Abduallev S, Abhangi M, Abreu P, Afanasev V, Afzal M, Aggarwal K M, Ahlgren T, Aho-Mantila L, Aiba N, Airila M, Alarcon T, Albanese R, Alegre D, Aleiferis S, Alessi E, Aleynikov P, Alkseev A, Allinson M, Alper B, Alves E, Ambrosino G, Ambrosino R, Amosov 

   - V, Andersson Sund´en E, Andrews R, Angelone M, Anghel M, Angioni C, Appel L, Appelbee C, Arena P, Ariola M, Arshad S, Artaud J, Arter W, Ash A, Ashikawa N, Aslanyan V, Asunta O, Asztalos O, Auriemma F, Austin Y, Avotina L, Axton M, Ayres C, Baciero A, Bai˜ao D, Balboa I, Balden M, Balshaw N, Bandaru V K, Banks J, Baranov Y F, Barcellona C, Barnard T, Barnes M, Barnsley R, Baron Wiechec A, Barrera Orte L, Baruzzo M, Basiuk V, Bassan M, Bastow R, Batista A, Batistoni P, Baumane L, Bauvir B, Baylor L, Beaumont P S, Beckers M, Beckett B, Bekris N, Beldishevski M, Bell K, Belli F, Belonohy E, Benayas J, Bergs˚aker H, Bernardo J, Bernert M, Berry M, Bertalot L, Besiliu C, Betar H, Beurskens M, Bielecki J, Biewer T, Bilato R, Biletskyi O, B´ılkov´a P, Binda F, Birkenmeier G, Bizarro J P S, Bj¨orkas C, Blackburn J, Blackman T R, Blanchard P, Blatchford P, Bobkov V _et al._ 2019 _Nuclear Fusion_ **59** 112021 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/ab2276` 

- [150] Lopes Cardozo N J, Lange A G G and Kramer G J 2016 _Journal of Fusion Energy_ **35** 94–101 ISSN 1572-9591 URL `https://doi.org/10.1007/s10894-015-0012-7` 

- [151] Jakobs M, Cardozo N L and Jaspers R 2014 _Nuclear Fusion_ **54** 122005 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/54/12/122005` 

- [152] Robinson D C 1999 _Plasma Physics and Controlled Fusion_ **41** A143 ISSN 0741-3335 URL `http://stacks.iop.org/0741-3335/41/i=3A/a=009` 

- [153] Menard J E, Brown T, El-Guebaly L, Boyer M, Canik J, Colling B, Raman R, Wang Z, Zhai Y, Buxton P, Covele B, D’Angelo C, Davis A, Gerhardt S, Gryaznevich M, Harb M, Hender T C, Kaye S, Kingham D, Kotschenreuther M, Mahajan S, Maingi R, Marriott E, Meier E T, Mynsberge L, Neumeyer C, Ono M, Park J K, Sabbagh S A, Soukhanovskii V, Valanju P and Woolley R 2016 _Nuclear Fusion_ **56** 106023 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/56/10/106023` 

- [154] Peng Y K M 2000 _Physics of Plasmas_ **7** 1681–1692 URL `https://aip.scitation.org/doi/ abs/10.1063/1.874048https://aip.scitation.org/doi/pdf/10.1063/1.874048` 

- [155] Friedberg J 2007 _Plasma Physics and Fusion Energy_ 1st ed (Cambridge University Press) ISBN ISBN-13 978-0-521-85107-7 URL `www.cambridge.org/9780521851077` 

- [156] Wilson H R, Ahn J W, Akers R J, Applegate D, Cairns R A, Christiansen J P, Connor J W, Counsell G, Dnestrovskij A, Dorland W D, Hole M J, Joiner N, Kirk A, Knight P J, Lashmore-Davies C N, McClements K G, McGregor D E, O’Brien M R, Roach C M, Tsaun S and Voss G M 2004 _Nuclear Fusion_ **44** 917–929 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/44/8/010` 

- [157] Najmabadi F 2003 _Fusion Engineering and Design_ **65** 143–164 ISSN 0920-3796 URL `http: //www.sciencedirect.com/science/article/pii/S0920379602003022` 

- [158] Windridge M 2019 _Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences_ **377** 20170438 URL `https://doi.org/10.1098/rsta.2017.0438` 

- [159] Costley A E 2019 _Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences_ **377** 20170439 URL `https://doi.org/10.1098/rsta.2017.0439` 

- [160] Fishpool G, Canik J, Cunningham G, Harrison J, Katramados I, Kirk A, Kovari M, Meyer H and Scannell R 2013 _Journal of Nuclear Materials_ **438** S356–S359 ISSN 0022-3115 URL `http://www.sciencedirect.com/science/article/pii/S0022311513000755https: //www.sciencedirect.com/science/article/pii/S0022311513000755?via%3Dihub` 

- [161] Joseph S 2014 High strength, high conductivity copper alloys and electrical conductors made therefrom 

- [162] Troxell J D 1989 Glidcop dispersion strengthened copper, potential application in fusion power generators _IEEE Thirteenth Symposium on Fusion Engineering_ pp 761–765 vol.2 

- [163] Flores F U, Seidman D N, Dunand D C and Vo N Q Development of high-strength and highelectrical-conductivity aluminum alloys for power transmission conductors _Light Metals 2018_ ed Martin O (Springer International Publishing) pp 247–251 ISBN 978-3-319-72284-9 

- [164] Meade D M 2002 _Fusion Engineering and Design_ **63-64** 531–540 ISSN 0920-3796 URL `https: //www.sciencedirect.com/science/article/pii/S092037960200282X` 

- [165] Hampshire D P 2018 _Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences_ **376** 20170447 URL `https://doi.org/10.1098/rsta.2017.0447` 

- [166] Bertolini E, Buzio M, Kaye A, Last J, Miele P, Noll P, Papastergiou S, Riccardo V, Sannazzaro G, Sjoholm M and Walton R 2000 Raising the jet toroidal field to 4 tesla Report 

- [167] Mlyn´aˇr J 2007 Focus on: Jet the european centre of fusion research Report EURATOM 

- [168] 1982 Jet joint undertaking Report ECSC/EEC/EURATOM eUR8306 EN (EUR-JET-RI I) URL `http://aei.pitt.edu/88591/1/1982.pdf` 

- [169] Matula R A 1979 _Journal of Physical and Chemical Reference Data_ **8** 1147–1297 

- [170] EuroFusion 2018 Power supply : Research for tomorrow’s energy supply URL `https://web.archive.org/web/20160105221442/https://www.euro-fusion.org/fusion/ jet-tech/jets-flywheels/` 

- [171] Egan J P and Boom R W 1990 _Measurement of the Electrical Resistivity and Thermal Conductivity of High Purity Aluminum in Magnetic Fields_ (Boston, MA: Springer US) pp 679–686 ISBN 978-1-4613-9880-6 URL `https://doi.org/10.1007/978-1-4613-9880-6_88` 

- [172] Fickett F R 1972 Magnetoresistivity of copper and aluminum at cryogenic temperatures _4th International Conference on Magnet Technology (MT-4)_ vol C720919 ed Winterbottom Y p 539 

- [173] Strategy D f B E and Industrial 2021 Towards fusion energy the uk government’s fusion strategy Report URL `https://assets.publishing.service. gov.uk/government/uploads/system/uploads/attachment_data/file/1022540/ towards-fusion-energy-uk-government-fusion-strategy.pdf` 

- [174] Weiss J D, Mulder T, ten Kate H J and Van der Laan D C 2017 _Superconductor Science and Technology_ **30** URL `https://iopscience.iop.org/article/10.1088/0953-2048/30/ 1/014002/pdf` 

- [175] Celentano G, Marzi G D, Fabbri F, Muzzi L, Tomassetti G, Anemona A, Chiarelli S, Seri M, Bragagni A and Corte A d 2014 _IEEE Transactions on Applied Superconductivity_ **24** 1– 5 ISSN 1051-8223 URL `https://ieeexplore.ieee.org/ielx7/77/6594876/06670053.pdf? tp=&arnumber=6670053&isnumber=6594876&ref=` 

- [176] Bykovsky N, Uglietti D, Wesche R and Bruzzone P 2016 _IEEE Transaction on applied superconductivity_ **26** 6600104 

- [177] Wolf M J, Bayer C M, Fietz W H, Heller R, Schlachter S I and Weiss K 2016 _IEEE Transactions on Applied Superconductivity_ **26** 1–4 ISSN 1558-2515 

- [178] Uglietti D 2019 _Superconductor Science and Technology_ **32** 053001 ISSN 0953-2048 13616668 URL `http://dx.doi.org/10.1088/1361-6668/ab06a2https://iopscience.iop.org/ article/10.1088/1361-6668/ab06a2/pdf` 

- [179] Ball P 2021 The chase for fusion energy accessed 2021/11/19 URL `https://www.nature.com/ immersive/d41586-021-03401-w/index.html` 

- [180] Masson-Delmotte V, Zhai P, Pirani A, Connors S L, P´ean C, Berger S, Caud N, Chen Y, Goldfarb L, Gomis M I, Huang M, Leitzell K, Lonnoy E, Matthews J, Maycock T K, Waterfield T, Yelek¸ci O, Yu R and Zhou B 2021 Climate change 2021: The physical science basis. Report Intergovernmental panel on climate change URL `https://www.ipcc.ch/report/ar6/wg1/ downloads/report/IPCC_AR6_WGI_Full_Report.pdf` 

- [181] Lustgarten A and Kohut M 2020 The great climate migration accessed 2021/06/01 URL `https://www.nytimes.com/interactive/2020/07/23/magazine/climate-migration.html` 

- [182] McMichael A J and Lindgren E 2011 _Journal of Internal Medicine_ **270** 401–413 ISSN 09546820 https://doi.org/10.1111/j.1365-2796.2011.02415.x URL `https://doi.org/10.1111/j. 1365-2796.2011.02415.x` 

- [183] 2015 Paris agreement Report United Nations URL `https://unfccc.int/sites/default/ files/english_paris_agreement.pdf` 

- [184] Johnson B 2020 Pm climate ambition summit opening remarks: 12 december 2020 accessed 2021/06/01 URL `https://www.gov.uk/government/speeches/` 

`pm-climate-ambition-summit-opening-remarks-12-december-2020` 

- [185] Shepheard M 2020 Uk net zero target accessed 2021/06/01 URL `https://www. instituteforgovernment.org.uk/explainers/net-zero-target` 

- [186] EDF Energy 2021 URL `https://www.edfenergy.com/energy/nuclear-new-build-projects/ hinkley-point-c/about` 

- [187] Fedkin M 2020 9.1. base load energy sustainability URL `https://www.e-education.psu.edu/ eme807/node/667` 

- [188] Henning C D Synfuel production in nuclear reactors URL `https://www.osti.gov/biblio/ 5677716` 

- [189] Ward D J 2009 _Fusion Science and Technology_ **56** 581–588 ISSN 1536-1055 URL `https: //doi.org/10.13182/FST56-581` 

- [190] 2020 _Additives for Polymers_ **2020** 5–6 ISSN 0306-3747 URL `https://www.sciencedirect.com/ science/article/pii/S0306374720300841` 

- [191] 2021 Cop26 accessed 2021/11/20 URL `https://ukcop26.org/` 

- [192] 2020 The demonstration power plant: Demo URL `https://www.euro-fusion.org/programme/ demo/` 

- [193] Zhuang G, Li G Q, Li J, Wan Y X, Liu Y, Wang X L, Song Y T, Chan V, Yang Q W, Wan B N, Duan X R, Fu P and Xiao B J 2019 _Nuclear Fusion_ **59** 112010 

- [194] 2021 Polio URL `https://www.gatesfoundation.org/our-work/programs/ global-development/polio` 

- [195] MacKay D J C 2008 _Sustainable Energy - without the hot air_ (Cambridge: UIT) ISBN 9780954452933 / 978-1-906860-01-1 

- [196] Carney M 2021 _Value(s) building a better world for all_ (Penguin Random House Canada) ISBN 9780771051555 

- [197] 1962 John f. kennedy moon speech - rice stadium URL `https://er.jsc.nasa.gov/seh/ ricetalk.htm` 

- [198] Jenkin B, de Bois N, Cairns A, Dugher M, Elphicke C, Flynn P, Halfon R, Heyes D, Hopkins K, Mulholland G and Roy L 2011 Public administration committee - twelfth report government and it- ”a recipe for rip-offs”: Time for a new approach URL `https://publications. parliament.uk/pa/cm201012/cmselect/cmpubadm/715/71502.htm` 

- [199] Chassels D 2013 Public administration written evidence submitted by david chassels (proc 6) URL `https://publications.parliament.uk/pa/cm201314/cmselect/cmpubadm/ 123/123vw09.htm` 

- [200] IRENA(2021) 2021 _Renewable Power Generation Costs in 2020_ (Abu Dhabi: International Renewable Energy Agency) ISBN 978-92-9260-348-9 

- [201] International Energy Agency 2021 World energy outlook 2021 Report International Energy Agency URL `https://www.iea.org/topics/world-energy-outlook` 

- [202] Corkhill C and Hyatt N 2018 _Nuclear Waste Management_ (IOP Publishing) ISBN 978-0-75031638-5 URL `http://dx.doi.org/10.1088/978-0-7503-1638-5ch1` 

- [203] UK Parliament 2020 The nuclear decommissioning authority’s management of the magnox contract URL `https://publications.parliament.uk/pa/cm5801/cmselect/cmpubacc/ 653/65305.htm#_idTextAnchor003` 

- [204] Bailey G W, Vilkhivskaya O V and Gilbert M R 2021 _Nuclear Fusion_ **61** 036010 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/abc933` 

- [205] Turcanu C, Prades A, Sala R, Perko T and Oltra C 2020 _Fusion Engineering and Design_ **161** 111891 ISSN 0920-3796 URL `https://www.sciencedirect.com/science/article/pii/ S0920379620304397` 

- [206] Liu X, Wu F, Wang Z, Li G, Liu X, Li H, Li J, Ren Y, Wu Y and Gao X 2020 _Nuclear Fusion_ **60** 046032 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/ab742d` 

- [207] Greenwald M, Whyte D, Bonoli P, Hartwig Z, Irby J, LaBombard B, Marmar E, Minervini J, Takayasu M, Terry J, Vieira R, White A, Wukitch S, Brunner D, Mumgaard R and Sorbom 

B 2018 The high-field path to practical fusion energy Report Massachusetts Institute of Technology URL `https://library.psfc.mit.edu/catalog/reports/2010/18rr/18rr002/ 18rr002_full.pdf` 

- [208] Romanelli F 2015 _Nuclear Fusion_ **55** 104001 

- [209] Pam´ela J, Solano E R and Contributors J E 2003 _Nuclear Fusion_ **43** 1540–1554 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/43/12/002` 

- [210] Lee G S, Kwon M, Doh C J, Hong B G, Kim K, Cho M H, Namkung W, Chang C S, Kim Y C, Kim J Y, Jhang H G, Lee D K, You K I, Han J H, Kyum M C, Choi J W, Hong J, Kim W C, Kim B C, Choi J H, Seo S H, Na H K, Lee H G, Lee S G, Yoo S J, Lee B J, Jung Y S, Bak J G, Yang H L, Cho S Y, Im K H, Hur N I, Yoo I K, Sa J W, Hong K H, Kim G H, Yoo B J, Ri H C, Oh Y K, Kim Y S, Choi C H, Kim D L, Park Y M, Cho K W, Ha T H, Hwang S M, Kim Y J, Baang S, Lee S I, Chang H Y, Choe W, Jeong S G, Oh S S, Lee H J, Oh B H, Choi B H, Hwang C K, In S R, Jeong S H, Ko I S, Bae Y S, Kang H S, Kim J B, Ahn H J, Kim D S, Choi C H, Lee J H, Lee Y W, Hwang Y S, Hong S H, Chung K H, Choi D I and Team K 2001 _Nuclear Fusion_ **41** 1515–1523 ISSN 0029-5515 URL `http://dx.doi.org/10.1088/0029-5515/41/10/318` 

- [211] Kim K, Park H K, Park K R, Lim B S, Lee S I, Chu Y, Chung W H, Oh Y K, Baek S H, Lee S J, Yonekawa H, Kim J S, Kim C S, Choi J Y, Chang Y B, Park S H, Kim D J, Song N H, Kim K P, Song Y J, Woo I S, Han W S, Lee S H, Lee D K, Lee K S, Park W W, Joo J J, Park H T, An S J, Park J S and Lee G S 2005 _Nuclear Fusion_ **45** 783–789 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/45/8/003` 

- [212] Ahn J W, Kim H S, Park Y S, Terzolo L, Ko W H, Park J K, England A C, Yoon S W, Jeon Y M, Sabbagh S A, Bae Y S, Bak J G, Hahn S H, Hillis D L, Kim J, Kim W C, Kwak J G, Lee K D, Na Y S, Nam Y U, Oh Y K and Park S I 2012 _Nuclear Fusion_ **52** 114001 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/52/11/114001` 

- [213] Shen B, Xi W B, Qian J P, Sun Y W and Fan H Y 2009 _Fusion Engineering and Design_ **84** 19–23 ISSN 0920-3796 URL `https://www.sciencedirect.com/science/article/pii/ S0920379608002585` 

- [214] Weng P 2005 Experimental advanced superconducting tokamak (east) design, fabrication and assembly URL `https://fire.pppl.gov/sofe_05_weng.pdf` 

- [215] Liu Z X, Gao X, Zhang W Y, Li J G, Gong X Z, Jie Y X, Zhang S B, Zeng L and Shi N 2012 _Plasma Physics and Controlled Fusion_ **54** 085005 ISSN 0741-3335 1361-6587 URL `http://dx.doi.org/10.1088/0741-3335/54/8/085005` 

- [216] Bourdelle C, Artaud J F, Basiuk V, B´ecoulet M, Br´emond S, Bucalossi J, Bufferand H, Ciraolo G, Colas L, Corre Y, Courtois X, Decker J, Delpech L, Devynck P, Dif-Pradalier G, Doerner R P, Douai D, Dumont R, Ekedahl A, Fedorczak N, Fenzi C, Firdaouss M, Garcia J, Ghendrih P, Gil C, Giruzzi G, Goniche M, Grisolia C, Grosman A, Guilhem D, Guirlet R, Gunn J, Hennequin P, Hillairet J, Hoang T, Imbeaux F, Ivanova-Stanik I, Joffrin E, Kallenbach A, Linke J, Loarer T, Lotte P, Maget P, Marandet Y, Mayoral M L, Meyer O, Missirlian M, Mollard P, Monier-Garbet P, Moreau P, Nardon E, P´egouri´e B, Peysson Y, Sabot R, Saint-Laurent F, Schneider M, Trav`ere J M, Tsitrone E, Vartanian S, Vermare L, Yoshida M and Zagorski R 2015 _Nuclear Fusion_ **55** 063017 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/0029-5515/55/6/063017` 

- [217] Duchateau J L, Bremond S, Lamaison V, Prochet P, Tena M, Ciazynski D and Torre A 2017 The superconducting magnet system of tore supra: lessons learnet and perspectives for west steady state operation 

- [218] Harrison J R, Akers R J, Allan S Y, Allcock J S, Allen J O, Appel L, Barnes M, Ben Ayed N, Boeglin W, Bowman C, Bradley J, Browning P, Bryant P, Carr M, Cecconello M, Challis C D, Chapman S, Chapman I T, Colyer G J, Conroy S, Conway N J, Cox M, Cunningham G, Dendy R O, Dorland W, Dudson B D, Easy L, Elmore S D, Farley T, Feng X, Field A R, Fil A, Fishpool G M, Fitzgerald M, Flesch K, Fox M F J, Frerichs H, Gadgil S, Gahle D, Garzotti L, Ghim Y C, Gibson S, Gibson K J, Hall S, Ham C, Heiberg N, Henderson S S, Highcock E, 

Hnat B, Howard J, Huang J, Irvine S W A, Jacobsen A S, Jones O, Katramados I, Keeling D, Kirk A, Klimek I, Kogan L, Leland J, Lipschultz B, Lloyd B, Lovell J, Madsen B, Marshall O, Martin R, McArdle G, McClements K, McMillan B, Meakins A, Meyer H F, Militello F, Milnes J, Mordijck S, Morris A W, Moulton D, Muir D, Mukhi K, Murphy-Sugrue S, Myatra O, Naylor G, Naylor P, Newton S L, O’Gorman T, Omotani J, O’Mullane M G, Orchard S, Pamela S J P, Pangione L, Parra F, Perez R V, Piron L, Price M, Reinke M L, Riva F, Roach C M, Robb D, Ryan D, Saarelma S, Salewski M _et al._ 2019 _Nuclear Fusion_ **59** 112011 ISSN 0029-5515 1741-4326 URL `http://dx.doi.org/10.1088/1741-4326/ab121c` 

- [219] Bora D 2002 _Brazilian Journal of Physics_ **32** 193–216 ISSN 0103-9733 URL `http://www.scielo. br/scielo.php?script=sci_arttext&pid=S0103-97332002000100032&nrm=iso` 

- [220] Saxena Y 2004 First experiments with sst-1 tokamak URL `https://www. researchgate.net/publication/282251654_First_Experiments_with_SST-1_Tokamak_ Presentation-IAEA04-F3-4Ra` 

- [221] Evaluated nuclear data file (endf) retrieval & plotting accessed 2020/02/28 URL `https://www. nndc.bnl.gov/sigma/` 

**Table 1.** Key design and performance parameters of `PROCESS` generated 100 MW net electricity (MWe) and 500 MW net electricity (MWe) tokamaks. Our preferred REBCO tokamak is shown in **bold** . Also shown are: EU-DEMO [3], ARIES-ST [157], a `PROCESS` generated pulsed Cu reactor based on STPP [156], ARC [5], CFETR [193, 206], ITER [1, 109], SPARC [2, 207], JET [166, 208, 209], JT60SA [103, 110], KSTAR [210, 211, 212], EAST [213, 214, 215], WEST [216, 217], MAST-U [153, 218] and SST-1 [219, 220]. Tokamaks have been grouped into: those in this work, demonstration reactors, proof of concept reactors and research tokamaks. Estimated parameters indicated with (*). Tokamaks with resistive primary magnets are indicated with ( _†_ ). 

**Table 2.** Capital cost of the preferred reactor and two other `PROCESS` generated, costoptimised, 100 MW net electricity, H98 = 1.2 tokamak pilot plants. Bold - preferred reactor with REBCO TF and CS coils. Also shown are plants with: Nb3Sn TF and CS coils; Commercial Nb-Ti TF and CS coils and quaternary Nb-Ti TF and CS coils. In all cases the PF coils are Nb-Ti. Note that these costs are for simply building the plant without mitigating risk with training or upgrading coils. Plant direct cost is the cost of the buildings, raw materials and labour only. Plant constructed costs also include the indirect costs (R&D, admin, licensing etc.), contingency costs and budget loan repayments. Total capital investment is the plant constructed cost as well as accrued interest on loan repayments and loss of buying power from the budget due to inflation during construction. All costs are in 1990 M$. 

**Table 3.** Power balance of the preferred reactor and two other `PROCESS` generated, cost-optimised, 100 MW net electricity, H98 = 1.2 tokamak pilot plants. Bold - preferred reactor with REBCO TF and CS coils. Also shown are plants with: Nb3Sn TF and CS coils; Commercial Nb-Ti TF and CS coils and quaternary Nb-Ti TF and CS coils. In all cases the PF coils are Nb-Ti. 

**Table 4.** Mean attenuation coefficients for (fast) neutrons of energy _>_ 0.1 MeV of tokamak relevant materials. _µ_ TCA are calculated from total neutron cross section data [221]. _µ_ i calculated using data from `MCNP` calculations of neutron transmission through a 30 cm block of (ith) mono-material [92] except for Tungsten Carbide which is derived from the `MCNP` data in figure 4. 

**Table 5.** Thicknesses and material compositions (derived from the ITER radial build) of the layers between the first wall and the central solenoid at the inboard mid-plane for the initial 100 MW net electricity REBCO CS, TF and Nb-Ti PF reactor using a radiation shield thickness from the benchmarking calculations. As well as those for the preferred reactor (in bold) using a radiation shield thickness optimised using `MCNP` . Outboard dimensions are shown in brackets () where significantly different. 

**Table 6.** Above: Useful cryogenic materials properties under 5 bar pressure [105]. Below: (magneto)resistances of RRR = 1000 copper and RRR = 10000 aluminium [54, 171, 172]. 

**Table 7.** Parameters for the Durham scaling law for transport critical current measurements on ITER specification Nb-Ti strands, quaternary Nb-Ti (not available commercially in long lengths), internal-tin Nb3Sn and REBCO. Extensive measurements have yielded that _B_ c2( _T_ ) = _B_ c2(0)(1 _− t[ν]_ ) _,_ for low temperature superconductors [108, 111, 130, 134], and _B_ c2( _T_ ) = _B_ c2(0)(1 _− t_ ) _[s]_ for REBCO [120]. The ITER spec. Nb-Ti parameters were found by extensive measurements taken at Durham university. _B_ c2 _[∗]_[(0)][and] _[T][ ∗]_ c[for][quaternary][Nb-Ti][were][taken][from][[126],][all] other parameters are from ITER specification Nb-Ti. The value of _A[∗]_ for REBCO was found by fitting to literature data [136], all other parameters were taken from measurements on REBCO tapes [120]. Nb3Sn parameters were taken from [111]. 

**Table 8.** Trained tokamaks designed for 100 MW net electricity and H98 = 1.2: Performance and cost data for the (preferred) tokamak optimised for REBCO toroidal field and central solenoid coils with minimised capital cost and training magnets of different superconductors (with maximised net electricity yield). The different superconductors considered are the high temperature superconductor _REBa_ 2 _Cu_ 3 _O_ 7 (REBCO where _RE_ :rare-earth), commercial NbTi (Comm. NbTi) used in MRI scanners, and quaternary NbTi (Quat. NbTi) that is not yet available commercially. In bold are the preferred tokamak ($ 4230 M) and the preferred tokamak with commercial Nb-Ti training magnets ($ 4540 M). Also shown are the power values that would result, were a reduced H98 = 1.0 to occur in practice. 

**Table 9.** Trained tokamaks designed for 100 MW net electricity and H98 = 1.6: Performance and cost data for a tokamak optimised for REBCO toroidal field and central solenoid coils with minimised capital cost (*) and training magnets of different superconductors (with maximised net electricity yield). Also shown are the power values that would result, were a reduced H98 = 1.0 to occur in practice. 

**Table 10.** Trained tokamaks designed for 500 MW net electricity and H98 = 1.2: Performance and cost data for a tokamak optimised for REBCO toroidal field and central solenoid coils with minimised capital cost (*) and training magnets of different superconductors (with maximised net electricity yield). Also shown are the power values that would result, were a reduced H98 = 1.0 to occur in practice. 

**Table 11.** Upgraded tokamaks designed for 100 MW net electricity and H98 = 1.2: Performance and cost data for a tokamak optimised for Nb-Ti toroidal field and central solenoid coils with minimised capital cost (*) and upgraded magnets of different superconductors (with maximised net electricity yield). Also shown are the power values that would result, were a reduced H98 = 1.0 to occur in practice. 

**Table 12.** Upgraded tokamaks designed for 100 MW net electricity and H98 = 1.6: Performance and cost data for a tokamak optimised for Nb-Ti toroidal field and central solenoid coils with minimised capital cost (*) and upgraded magnets of different superconductors (with maximised net electricity yield). Also shown are the power values that would result, were a reduced H98 = 1.0 to occur in practice. 

**Table 13.** Upgraded tokamaks designed for 500 MW net electricity and H98 = 1.2: Performance and cost data for a tokamak optimised for Nb-Ti toroidal field and central solenoid coils with minimised capital cost (*) and upgraded magnets of different superconductors (with maximised net electricity yield). Also shown are the power values that would result, were a reduced H98 = 1.0 to occur in practice. 

**Table 14.** Performance and cost of a steady-state H98 = 1.6, 100 MWe reactor with copper TF, CS and PF coils (with minimised capital cost). Based on STPP [156]. 

![](images/chislett2022.pdf-0062-02.png)

**Figure 1.** A comparison between experimentally measured plasma energy confinement times from various tokamaks and the confinement time predicted by the IPB98(y,2) scaling law and adapted from [42]. The solid line is _H_ 98 = 1 _._ 0 dashed line is _H_ 98 = 1 _._ 2 and the dotted line is _H_ 98 = 2 _._ 0. Inset: H-factor as a function of toroidal field on the plasma axis for a tokamak with _IP_ = 8.20 MA, _PL_ = 46 MW, _n_ = 1.8 _×_ 10[20] _m[−]_[3] , _M_ = 2.5, _Rmajor_ = 2 m, _A_ = 1.8, _κ_ = 3 using the NSTX Gyro-Bohm [44] confinement time scaling. 

![](images/chislett2022.pdf-0063-02.png)

**Figure 2.** Top: Total central solenoid coil (CS) and poloidal field coil (PF) flux, central solenoid bore and thickness, and (Bottom:) plasma major radius and plant total capital cost as a function of plasma burn time, of 100 MWe tokamak power plants with REBCO CS and TF coils and Nb-Ti PF coils (i.e. magnet materials as per the preferred tokamak design) optimised for minimum capital cost. Note that the preferred reactor has a 7200 s plasma burn time. 

![](images/chislett2022.pdf-0064-02.png)

**Figure 3.** Cross-sections and inboard mid-plane radial build of the preferred reactor (a cost-optimised H98 = 1.2, 100 MW net electricity tokamak with REBCO toroidal field and central solenoid coils) with an optimised 25.0 cm radiation shield. Details of the layer constituents can be found in table 5. The inboard blanket is 53 cm in radial thickness and based on the EU-DEMO helium-cooled pebble bed design [58], guaranteeing a tritium breeding ratio _>_ 1.1. 

![](images/chislett2022.pdf-0065-02.png)

**Figure 4.** Nuclear heating in the TF coil system and number of full-power operation years until the Weber dose limit [94] is achieved for the preferred reactor (a costoptimised H98 = 1.2, 100 MW net electricity tokamak with REBCO toroidal field and central solenoid coils) as a function of the thickness of its tungsten carbide radiation shield as calculated by `MCNP` (closed squares) and the benchmarking calculation (open diamonds). The material layers between the plasma and the TF coil are given in table 5. The dotted black lines indicate the minimum 40 year conductor lifetime limit (and corresponding minimum shield thickness as calculated by `MCNP` ). The dotted red lines indicate the maximum 10 kW heating limit on the TF system (and corresponding minimum shield thickness as calculated by our benchmarking calculations). 

![](images/chislett2022.pdf-0066-02.png)

**Figure 5.** `MCNP` calculated (a) fast neutron flux through the poloidal cross-section of the preferred reactor (a cost-optimised H98 = 1.2, 100 MW net electricity tokamak with REBCO toroidal field and central solenoid coils) with an optimised 25.0 cm radiation shield detailed in the right hand column of table 5. (b) The neutron flux spectrum and (c) photon flux spectrum as a function of distance into inboard mid plane of the preferred reactor with a 25.0 cm radiation shield. These spectra were converted to flux density per unit lethargy by multiplying the spectral histogram fluxes by the ratio between the energy bin average energies and the bin widths. 

![](images/chislett2022.pdf-0067-02.png)

**Figure 6.** Neutron and photon induced wall loading along the mid-plane within the preferred reactor (a cost-optimised H98 = 1.2, 100 MW net electricity tokamak with REBCO toroidal field and central solenoid coils) with an optimised 25.0 cm radiation shield. The radial positions of the central solenoid coil (light pink), toroidal field coil legs (blue), vacuum vessel (green), radiation shield (black) and blanket (deep pink) are shown. 

![](images/chislett2022.pdf-0068-02.png)

**Figure 7.** Whole strand/tape critical current density of commercial ITER specification Nb-Ti (Comm. Nb-Ti), quaternary (Quat.) Nb-Ti, internal tin Nb3Sn, and REBa2Cu3O7 (REBCO where RE: rare-earth) at 4.5 K, used in this work. Quaternary Nb-Ti is not commercially available (but could be optimised for fusion applications). 

![](images/chislett2022.pdf-0068-04.png)

**Figure 8.** Toroidal magnetic field through the midplane of the preferred reactor (a cost-optimised H98 = 1.2, 100 MW net electricity tokamak with REBCO toroidal field and central solenoid coils). 

![](images/chislett2022.pdf-0069-02.png)

**Figure 9.** Fusion power, gross electric power and net electric power as a function of operating H98-factor for two reactors with REBCO CS and TF coils and Nb-Ti PF coils. The reactors were optimised for minimum capital cost (open data points) at H98-factors of H98 = 1.6 (black) and H98 = 1.2 (red) and produce 100 MWe. Reactors at higher or lower than expected H98-factors were optimised to produce maximum net electricity (solid data points). The discontinuities in fusion power that occur between high and low H98 factors are due to a loss of energy confinement at H98 factors that are too low. 

![](images/chislett2022.pdf-0070-02.png)

**Figure 10.** (a) Change in cost-optimal field on coil and (b) capital cost of the preferred reactor (a cost-optimised H98 = 1.2, 100 MW net electricity tokamak with REBCO toroidal field and central solenoid coils) as a function of the allowable maximum of the shear stresses (as used for the Tresca yield criterion) on the central solenoid and inboard toroidal field coil mid-planes. Different data sets correspond to different costs of steel components (standard, 1.5 _×_ standard etc.), representative of either more expensive steels or larger steel volumes. 

![](images/chislett2022.pdf-0071-02.png)

**Figure 11.** (a) Reactor power balance (where “Core Systems” includes the cryosystem (46 MWe) and the tritium handling system (15 MWe)); (b) direct capital cost breakdown of our preferred 100 MW net electricity producing REBCO based tokamak power plant. Costs are in 1990 US M$. 

