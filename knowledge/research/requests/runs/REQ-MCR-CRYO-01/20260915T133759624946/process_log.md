# Research run REQ-MCR-CRYO-01

**Question:** Which admissible primary sources anchor current-lead, thermal-radiation and support-conduction heat loads for a 20 K HTS coil set, and which Stellaris-specific inputs remain missing?

**Consumer:** 20260914-magnet-coil-realism#3  ·  **Request key:** `796ec772c46cf7f6bbe6fe15c6464e91cc1d53b594184e6723a7fb77bb60b265`

- searched: `site.cds.cern.ch Ballarino current leads 20 K heat load`
- searched: `site.nist.gov cryogenic G-10 CR thermal conductivity 4 300 K`
- searched: `site.ntrs.nasa.gov multilayer insulation 20 K 80 K heat flux`
- candidate https://cds.cern.ch/record/1026941/files/at-2007-005.pdf — **keeper** Clean-room screened: CERN HTS lead operating regimes, no stellarator costing. Primary design analysis; useful for regime distinctions, not a Stellaris coefficient.
- candidate https://trc.nist.gov/cryogenics/materials/G-10%20CR%20Fiberglass%20Epoxy/G10CRFiberglassEpoxy_rev.htm — **keeper** Clean-room screened: material-property database only. Anisotropic G10 conductivity candidate, conditional on support material choice.
- candidate https://ntrs.nasa.gov/api/citations/20150018118/downloads/20150018118.pdf?attachment=true — **keeper** Clean-room screened: NASA insulation-system presentation, no stellarator design data. Search-index triage relevant; web open failed, native capture will determine availability. Useful for warm-to-shield transfer limits.
