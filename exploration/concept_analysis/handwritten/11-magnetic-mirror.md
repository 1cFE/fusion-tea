# Deliverable 1: Qualitative Write-Up

## Device description

A magnetic mirror machine is a linear magnetic confinement device. Its main feature is a long confinement chamber, when the DT fuel is heated and fuses. The magnetic mirror can have an arbitrarily long main chamber, making magnetic mirror machines an inherently modular design.

A magnetic mirror module - some portion of the main cell - is relatively (to Tokamak section) easy to manufacture, as it requires simple extrusions of pipe-like sections. The structural strength of the HTS coils is also served by using a circular “pancake”, which reduces the stress induced on the coil structure by the magnetic field. 

These modules could be designed for disassembly and replacement, reducing the time the machine needs to be offline for maintenance. This feature would require working in a hot (radioactive) cell surrounding entire machine, or finding clever ways to isolate the interior, which is in of itself costly, so this idea has to be weighed. 

The radial build of the main fusion chamber for a DT reactor, like all other magnetic confinement approaches running DT fuel, is plasma - first wall - breeding blanket - vacuum vessel wall - shielding - solenoid coils. 

## Physics

The physics of a magnetic mirror are such that radial confinement is accomplished by the magnetic field confining particles to helical trajectories around magnetic field lines. In the axial direction, particles must be reflected to remain confined, and this is the origin of the machine name. 

The magnetic mirror uses the eponymous “magnetic mirror effect” to reflect charged particles along the machine axis. Charged particles traveling along field lines experience an effective potential that is the magnetic field strength, and the “charge” that is the particle magnetic moment. This means a particle who’s velocity is mostly in the direction of the magnetic field lines would experience a smaller potential barrier than a particle who’s velocity is mostly perpendicular to the magnetic field lines. This is called an loss cone. 

This means a magnetic mirror is prone to axial losses and a good amount of effort is invested in ameliorating it. 

The solution to this issue is end-plugs. Realta Fusion started their R&D path developing their end plug, WHAM. End plugs can implement various technologies. The tandem mirror is a small mirror chamber that is held at a high electron temperature, this is meant to generate an electrostatic barrier to confine the ions in the mirror. Other approaches are centrifugal forces, RF and ponderomotive barriers. 

The lossy ends of a mirror allow for a simple way to get rid of fusion ash - if alpha channeling is employed to cool the ash, it would naturally leave the device. 

## Subsystems

Other than end plugs, which are often small mirror cells, a magnetic mirror employs

- Neutral beams (NBIs), can be used to both heat the plasma and supply it with fresh fuel. Neutrals injected into the device by NBIs undergo charge exchange and become ionized. These ions are well confined when the NBIs are aimed with a large enough angle to the magnetic field. NBIs are used to heat up tandem mirror end plugs.
- Ion cyclotron resonance heating (ICRH), can either replace NBIs or supplement them.
- Electron cyclotron resonance heating (ECRH) would heat up the plasma in the mirror, but possibly cause a faster electron depletion.

A long magnetic mirror allows for a small percentage of its surface area to be punctured by NBIs or other ports to maintain plasma heating. 

- Blankets need to cover the mirror axially as well as radially, in order to capture the maximal amount of neutrons.
- Direct energy capture. This concept is one of few that has a direct energy capture concept associated with it. Venetian blinds are a set of ribbon electrodes in the loss cone past any end plugs. The magnetic field is expanded to reduce the heat load on them, and particles are collected by the electrodes that are maintained at high voltage. The Venetian blinds were tested in the 70s, but never in fusion reactor conditions. They have a ~50-65% efficiency, which is not *that* high compared to turbines. This technology has a TRL 5, but the added efficiency over and above a thermal cycle is small. The survivability of thin uncooled electrodes downstream of a fusion reactor is low. I think this is not worth considering.

### Tandem end plugs

The Tandem mirror approach is to maintain a pair of hot dense end plugs on the two sides of the main mirror chamber. These require large recirculating power to maintain their temperature and density. 

The hot dense plasma becomes positively charged, confining ions in the main chamber.

### Centrifugal end plugging

Another method to end plug a mirror is using the centrifugal force. To do so, one has to spin the plasma at high Mach number. There are several methods for doing so, with the most researched one (TAE, Realta) is using concentric electrodes which are biased relative to each other. This generates a radial electric field and an ExB drift cause the plasma to spin. 

Terra Fusion, on the other hand, uses a central electrode that is biased relative to the mirror first wall to rotate the plasma.

### Ponderomotive end plugging

This is my PhD thesis topic. One could use a radio frequency wave that is off-resonance to repel the plasma off the end plug, or attract it to a portion of the center cell. One could combine the rotation and a static perturbation to generate a ponderomotive effect as well. 

### Non-axisymmetric devices

In the past, non-axisymmetric configurations were considered for end plugs. Yin-yang coils, baseball coils. 

Additionally, non-axisymmetric main chamber, features generated by Ioffe bars, were used to enhance stability.

## **Availability of Data**

Magnetic mirror studies from the 70s are available (Post, Ryutov and others), and Realta published several studies of their own. Experiments such as Gamma-10 and the Gas dynamic trap in Russia are also a source of information.

Among contemporary efforts, Realta Fusion publish their progress, and may be among the first companies to utilize CFS’s HTS magnets. Terra Fusion and Gridfire spun out of Maryland. 

Publicly available magnetic mirror costing studies are the MARS (Mirror Advanced Reactor Study) and the MINIMARS studies from 1983 and 1986. They projected an LCOE of 7cent/kWhr in 1983 dollars, and that the LCOE saturates around 600 MWe. The saturation is surprising, as it means a mirror becomes competitive at smaller outputs compared to Tokamaks that require large size to be competitive.

Both of these studies were using old magnet technology, and yin-yang coils. Current developments allow to use simpler magnet geometry and better HTS. 

![image.png](attachment:6a0ed641-bce3-48f6-9ccb-5b6eea7448cc:image.png)

## **Challenges in Capturing System Function**

The questions remaining in magnetic mirror physics are

1. Stability. Mirror were plagued by MHD stability issues. 
2. Axial confinement needs to be addressed - this is the current experimental campaign by Realta. 
3. Start-up. The path through parameter space that reaches from no plasma to hot fusion plasma needs to be mapped.
4. The magnetic mirror naturally have two “divertors” - the axial ends of the machine. Heat loads on these components need to be assessed.

These join the open questions pertaining to DT fusion

1. Material limits and damage accumulation
2. Activation
3. Tritium breeding
4. Hot cell operation
5. Neutron shielding

## **Maturity of Key Subsystems and Components**

Mirror end plugs are under developments. These represent the largest loss channel, and are in the critical development path. Every company pursuing a mirror machine has their own end plugging approach.

Venetian blinds are TRL 5 system that was never used in fusion conditions. The were demonstrated in lab settings. 

For long mirrors, the “diverters” at the ends are going to have to withstand large heat and particle fluxes. 

Blankets and the Tritium breeding were never demonstrated.

HTS neutron shielding also hasn’t been developed. The issue here is the possible requirement of large magnet radius to compensate for the shielding in addition to the rest of the layers, which may generate large stresses in the magnets.

## **Key Materials and Supply Chain Considerations**

The usual DT issues - enriched Li6, REBCO, first wall materials (Tungsten, Beryllium).

## References

Moir, R. W., and W. L. Barr. ‘“Venetian-Blind” Direct Energy Converter for Fusion Reactors’. *Nuclear Fusion* 13, no. 1 (1973): 35–45. https://doi.org/10.1088/0029-5515/13/1/005.

Post, R. F. ‘The Magnetic Mirror Approach to Fusion’. *Nuclear Fusion* 27 (1987): 1579. https://doi.org/10.1088/0029-5515/27/10/001.

Ryutov, D. D. ‘Open-Ended Traps’. *Soviet Physics Uspekhi* 31, no. 4 (1988): 300–327. https://doi.org/10.1070/PU1988v031n04ABEH005747.

Endrizzi, D., J. K. Anderson, M. Brown, et al. ‘Physics Basis for the Wisconsin HTS Axisymmetric Mirror (WHAM)’. *Journal of Plasma Physics* 89, no. 5 (2023): 975890501. https://doi.org/10.1017/S0022377823000806.

Forest, C. B., J. K. Anderson, D. Endrizzi, et al. ‘Prospects for a High-Field, Compact Break-Even Axisymmetric Mirror (BEAM) and Applications’. *Journal of Plasma Physics* 90, no. 1 (2024): 975900101. https://doi.org/10.1017/S0022377823001290.

Gordon, James D. ‘Mirror Advanced Reactor Study Engineering Overview’. *Nuclear Engineering and Design. Fusion* 3, no. 2 (1986): 119–50. [https://doi.org/10.1016/0167-899X(86)90002-9](https://doi.org/10.1016/0167-899X(86)90002-9).
Lee, J. D. ‘MINIMARS conceptual design: Report I. Volume 1.’ No. UCID--20559-Vol. 1. Lawrence Livermore National Lab., CA (USA), 1985.

# Deliverable 2: Quantitative LCOE Model

Using 1costingfe, here is a script generating a DT magnetic mirror costing, and its output. 

[dt_mirror.py](attachment:3b416b69-2c71-4712-830d-a2b7b417ff01:dt_mirror.py)

[dt_mirror_output.md](attachment:e17e1e05-0a9e-4d29-8bd3-8eb058ff0585:dt_mirror_output.md)

The main pieces are

```markdown
| Metric | Value |
|--------|-------|
| LCOE | 80.2 $/MWh (8.02 ¢/kWh) |
| Overnight cost | 5,862 $/kW |
| Fusion power | 1,137 MW |
| Net electric | 500 MW |
| Q_eng | 4.6 |
| Recirculating fraction | 22.0% |
```

## Back-Solve to $0.01/kWh

Using 1costingfe with the current information therein, DT mirror can't reach 1 ¢/kWh, even with extreme assumptions. The best case (2 GWe, 95% availability, 2-yr construction, 3% WACC, 60% thermal efficiency, aggressive DEC) gets to 2.70 ¢/kWh.

The bottleneck is structural: the mirror's high recirculating fraction (end losses requiring large P_fus for modest P_net) and the CAS22 costs (coils + heating) don't shrink fast enough with scale. The single-parameter sweeps show that no individual lever gets more than a ~40% reduction — you need all of them simultaneously and even then it's not enough.     

## Key Uncertainties

HTS magnet cost is the largest cost, and is expected to go down.

