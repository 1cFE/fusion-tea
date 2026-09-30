# Research run REQ-MMC-CRYO-02

**Question:** Which permitted primary sources give fusion superconducting-magnet cold-load magnitudes at about 4-5 K (thermal radiation from shields, support conduction, nuclear heating, joints) and a citable stored copy of Green 2015 large 4.5 K refrigerator efficiency and capital-cost laws?

**Consumer:** goal:magnet-material-comparison/T-003  ·  **Request key:** `78e4716de6cc616d3efbb7eff0c1ed96291f20567376c9e8a4cc6709174d6a5a`

- searched: `Koncar DEMO thermal shields heat loads design temperature optimization EUROfusion WPPMI-CPR(17) 17578`
- candidate https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPPMICPR17_17578_submitted-4.pdf — **keeper** EUROfusion open preprint; DEMO static heat loads on 4 K magnets and 80 K shields, Table 1 and Figs 1-3; verified real 8-page PDF via curl
- searched: `EU DEMO magnet cryogenic heat loads nuclear heating TF coil 4.5 K kW EUROfusion scipub`
- searched: `ITER magnet system heat loads 4.5 K nuclear heating TF coils kW cryoplant budget open access`
- candidate https://www.fusion.qst.go.jp/ITER/FDR/PDD/PDD_3_2_Cryoplant.pdf — **keeper** ITER FDR 2001 Plant Description Document ch. 3.2 (official, hosted by QST); Table 3.2.1.2-1 magnet-system static and averaged pulsed 4.5 K heat loads; verified real 20-page PDF via curl
- failed https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPMAGCPR17_18607_submitted-4.pdf — open keeper not captured because max_captures (3) was spent: Lewandowska et al. 2017 EU-DEMO LTS TF WP thermal-hydraulics; gives nuclear heat density law 50 W/m3 exp(-r/lambda) from the TF case plasma-facing edge (Eq. 1, decay length is an equation image) and joint resistance 1 nOhm (queued)
- candidate https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPMAGCP16_15044_submitted.pdf — **rejected** Sedlak et al. 2016 DEMO TF WP1 thermal-hydraulics: nuclear heat per layer only in an image table (36.1 W layer 1) and 2 W joint per layer; early WP superseded by Lewandowska 2017 and the registered Sedlak 2020 review
- candidate https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPMAGCP16_15415_submitted.pdf — **rejected** Brighenti et al. 2016 coolant blockage in DEMO TF coil; no heat-load budget
- candidate https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPMAGCPR17_17863_submitted-4.pdf — **rejected** Zappatore et al. 2017 DEMO PF coil performance; PF-specific, no magnet-system budget
