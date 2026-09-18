# Research run REQ-computed-tritium-breeding-01

**Question:** What published parametric neutronics model or reproducible benchmark can compute TBR from helium-cooled PbLi blanket thickness, composition and lithium enrichment, with validation and applicability adequate for the retained stellarator scenario?

**Consumer:** work/orchestration/goals/computed-tritium-breeding/goal.md  ·  **Request key:** `b780f3d494849a582fda908b0ff13be94700ae733d0cbd2dbf8f2c6471714cd3`

- searched: `UKAEA PROCESS HCLL tritium breeding ratio thickness lithium enrichment fit`
- searched: `helium cooled lithium lead blanket parametric neutronics TBR benchmark thickness surrogate -"ARIES"`
- searched: `helium cooled lithium lead parametric TBR excluding ARIES`
- searched: `Proof-of-principle parametric stellarator neutronics Serpent2`
- candidate https://acris.aalto.fi/ws/portalfiles/portal/150683939/Proof-of-principle_of_parametric_stellarator_neutronics_modeling_using_Serpent2.pdf — **keeper** Primary published parametric stellarator blanket study; assess DCLL applicability and independent validation rather than assume transfer.
- searched: `HCLL blanket TBR surrogate dataset parametric model lead lithium -ARIES`
- searched: `helium cooled lead lithium tritium breeding ratio fitting function thickness enrichment -ARIES`
- candidate https://scientific-publications.ukaea.uk/wp-content/uploads/Shimwell_2019_Nucl._Fusion_59_046019.pdf — **keeper** Primary HCLL parametric geometry and TBR enrichment/plate-height interpolation study; assess applicability and benchmark evidence.
- candidate https://upcommons.upc.edu/bitstream/handle/2099.1/17426/Neutronic_fusion_final_thesis_Martinez_Arroyo_Javier.pdf — **keeper** Repository thesis search identifies HCLL surrogate; inspect through native quarantine registration before relying on applicability.
