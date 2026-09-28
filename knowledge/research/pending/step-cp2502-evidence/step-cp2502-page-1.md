were costed independently, it could be overlooked how their size affects the pumping power required for the cooling, which then has a knock-on effect on the recirculating power and net electric output of the plant. 

These oversights can be avoided by using a systems code like PROCESS where not only are the physics and engineering models fully integrated, but the cost models are too. The ability for rapid iterations mentioned above also lends itself to costing fusion power plants, allowing for continuous evaluation and reevaluation of estimates for subsystems, and the plant as a whole. The built-in ability to scan in a desired variable also facilitates extrapolating a particular design and its costs up to a commercial scale plant, an example of which we will discuss in detail in the next section. However, due to the simplicity of the cost evaluation, especially in the extrapolation towards commercial plants, these cost models are more relevant for differential cost assessments than absolute cost assessments. 

## _C. Scans_ 

To extrapolate to a commercial scale plant, we started with a plant design with a Spherical Tokamak (ST) reactor similar to the current conceptual design point of the STEP Prototype reactor [19]. We then performed a scan in net electric output radius _P_ net _,_ elec[1] .: 100MW - 2GW, in steps of 25MW, minimising majorSome of the important parameters are listed in Table I. The major radius at the start point, and the parameters which are fixed, are consistent with the current STEP Prototype Powerplant design point [19]. The additional parameters listed have been allowed to vary as part of this study, and therefore do not correspond to any baseline design. 

Once the scan was successfully performed, a plot of which can be seen in Fig. 1, the point at 1.2GW was selected, around which we performed some sensitivity analysis on certain parameters to explore their impact on LCOE: 

- **Allowable blanket fluence** (MW-yr/m[2] ) - Determines lifetime of blanket/first wall based on neutron wall load 

- **Allowable divertor fluence** (MW-yr/m[2] ) - Determines lifetime of divertor based on divertor heat load 

   - Neither of these fluences are currently consistently influencing the plant availability and therefore only impact operational costs. This is not an issue in regimes where the overall plant availability is consistent with those lifetimes but this is unlikely over the entire scan range 

- **N**[th] **-of-a-kind (NOAK) factor** - represents the cost of an item/system at its N[th] generation with respect to its 1[st] generation (due to e.g. improved manufacturing, mass production etc.) 

- **Thermal efficiency** - efficiency converting total thermal power into gross electrical power. It was shown in [2] how critically the thermal to electric conversion efficiency impacts the estimated capital costs. As capital costs are expected to dominate the LCOE for commercial fusion 

- 1All PROCESS work done as part of this paper used PROCESS v3.0.0 

- Git hash: 536de61792fd064f13421b2e1d9209645a9a7180 

   - power plants, this is expected to have a similarly significant impact on LCOE 

- **Availability fraction** - what percent of the time the plant is producing electricity. Given that achievable availability fractions on commercial fusion power plants cannot be understood without building demonstration/prototype fusion power plants, scanning this parameter helps us understand the impact of different availability factors on LCOE 

- **Heating and Current Drive (HCD) efficiency** - wallplug efficiency of HCD systems. As the HCD systems are expected to be the source of highest recirculating power in a tokamak, having higher efficiency systems is being explored as an option to reduce LCOE by increasing net electric output 

- **H-factor (IPB98(y,2))** - radiation corrected H-factor [20], [21]. Varying the H-factor helps us explore the effect of uncertainty in the plasma performance in the design and potential performance gains if higher performing plasma scenarios can be found 

- **Gyrotron redundancy** - ratio of gyrotrons needed for start-up to flat-top. PROCESS sets the flat-top heating and current drive requirements in line with what is needed to achieve the relevant plasma current. This is also to allow system redundancy. Depending on the design a higher amount of HCD will be needed for start-up/ramp-down or for redundancy to cover unreliable systems. Reducing the ratio between the the flat-top HCD requirements and the overall gyrotrons costed, assumes that going towards commercialisation we can create more reliable HCD sources and learn to ramp-up plasmas more efficiently 

The point for the sensitivity study was chosen as it has an achievable net electric output with respect to the starting point design, also there are diminishing returns in LCOE reduction beyond this point. 

In the next section, we will discuss the results of these scans in more detail, as well as any potential implications for current and future endeavours to design fusion power plants. 

## III. RESULTS 

The scan in net electric output is plotted in Fig. 1 where the blue line is LCOE normalised with respect to the value at 100MW net electric and the red line is major radius. Firstly, it demonstrates a potentially obvious but still worthwhile point: that by building a bigger device, the power plant is not only generating more electricity, but is doing so in a more cost efficient way, reducing the LCOE. However, it is the size of this reduction that is most striking, reaching as low as _∼_ 20% of the LCOE of a 100MW device. It is worth noting that the major radius only begins to increase at a net electric output of _∼_ 500MW, at which point the LCOE has reduced to _∼_ 30% of that of a 100MW device. Nevertheless, STEP’s target of 100MW is to account for margins and uncertainties. Secondly, as mentioned previously, there are dimishing returns in LCOE reduction beyond _∼_ 1.2GW. This behaviour is driven predominantly by the large recirculating power to net electric 

