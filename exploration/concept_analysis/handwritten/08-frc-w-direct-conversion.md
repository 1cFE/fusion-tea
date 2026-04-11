# Deliverable 1: Qualitative Write-Up

## Device description

Helion’s pulsed colliding FRC generator employs a unique formation and heating sequence that doesn’t exist elsewhere. The device is a linear, bilaterally symmetric machine. Compact FRCs are generated at chambers at the ends of the device, and accelerated towards each other by a linear magnetic accelerator - like a magnetic rail gun. The colliding FRCs with opposite currents merge and heat the plasma ions via magnetic reconnection. Further compression is performed by ramping up the magnetic field to achieve fusion conditions. The aneutronic burn increases plasma pressure, and the its expansion in the magnetic fields is directly converted to electricity. 

### **Direct Electromagnetic Energy Recovery**

The unique direct conversion method is the main selling point of Helion. They are capable of recovering ~90% of the stored energy in the compressed plasma back into electricity, and to use the fusion to the fullest extent they have to run a pulsed aneutronic fuel. A high-beta confined plasma is also a critical component.

## **Availability of Data**

The FRC experimental database is extensive by the standards of non-mainstream fusion concepts, spanning six decades, multiple national programs, and over 600 published papers from the primary U.S. and Japanese FRC programs alone. Key milestones in the public record include the Los Alamos FRX series (1975–1990), the University of Washington large-s experiment (LSX, 1990–2000), the Translation Confinement Sustainment (TCS) experiment at the Redmond Plasma Physics Laboratory, and ongoing work at the Air Force Research Laboratory. This database provides a solid empirical foundation for FRC confinement scaling, formation physics, and stability behavior at moderate parameters.

The pulsed colliding approach specifically has an experimental lineage traceable through multiple prototype generations, progressing from proof-of-concept single-plasmoid systems through increasingly capable double-ended colliding configurations. Demonstrated milestones include formation of centimetre-scale FRC plasmoids, their supersonic translation and collision, the achievement of merged-and-compressed FRC plasma temperatures exceeding 100 million degrees Celsius (greater than 9 keV) at peak compressed field strengths of approximately 8 T, and the demonstration of high-efficiency direct energy recovery from a pulsed magnetic compression system at over 95% round-trip efficiency at subscale.

Recent press release by Helion showed they can achieve D-T fusion in their device. This is a good progress milestone, but this not a sufficient risk retirement for the device as a whole.

What is missing, in my estimate is a decent theory of the magnetic reconnection, or experimental validation of a sizeable fusion yield in D-He3 fuel. The reliability of the colliding FRCs generation and collisions can also be a weak point. 

Helion hasn’t published too much on their progress. Their device sound relatively cheap to construct, but I’m not convinced the fusion works. 

What’s missing:

- Detailed plasma parameters (density, confinement time, triple product) - Fusion yield per pulse (how many neutrons per shot, at what consistency) - Confinement scaling data at their achieved parameters
- Any D-He3 plasma operation (all experiments are DD)
- System-level reliability data (pulse count, failure rates)
- Quantitative merging efficiency measurements
- Anything resembling the data package one would need to validate the LCOE claims

## **Challenges in Capturing System Function**

The two items we keep getting back into are the fusing plasma and the fuel sourcing. The fuel seems to be one of the largest cost. 

## **Maturity of Key Subsystems and Components**

### The two subsystems with the highest risks are:

**He3 breeding** - TRL of 2-3. There are several ways to do it, but the main method proposed by Helion is running a D-D machine. This is as complicated as figuring out D-D fusion on its own, with some added complexity in exhaust separation and tritium storage. If tritium decay is a path for He3, this can invite a large regulatory burdern,

**D–He3 fusion in the colliding FRC -** TRL of 2–3. D–He3 reactions not yet operated at 200+ keV ion temperatures in any FRC device. D–D neutron experiments provide indirect validation. The 20x temperature scale-up from demonstrated to required is the largest single physics extrapolation. This includes coil fatigue and repetitive operation.

### Subsystems and components that are relatively mature:

Helion invested significantly in pulsed power systems and the energy recovery circuits. This is their main selling point and why they managed to raise significant money. 

## **Key Materials and Supply Chain Considerations**

He3

# Deliverable 2: Quantitative LCOE Model

Using 1costingfe. This model is quite unorthodox, requiring some manual cost overrides for 1costingfe to capture the device.

[dhe3_pulsed_frc_output.txt](attachment:2327c38d-189e-4844-b8ff-bf3e1f8ee4a8:dhe3_pulsed_frc_output.txt)

[dhe3_pulsed_frc.py](attachment:ca24f413-b90c-4094-a7b6-749d92cac1ec:dhe3_pulsed_frc.py)

Surprisingly, my current estimate is for 4 cent/kWh, which is very good, approximately half of the D-T mirror we looked at previously. The D-He3 capital cost is extremely cheap, with cheap coils and no tritium breeding and handling. The copper coils are great, and not requiring turbines saves $127M. 

If HTS coils are a requirement, and nearly every other fusion device uses HTS coils and not copper for performance reasons, the capital costs skyrocket and the LCOE becomes 20 cent/kWh.

The He3 costs are enormous. If Helion consumes significant portion of the inventory before setting up breeding, the costs would go through the roof.