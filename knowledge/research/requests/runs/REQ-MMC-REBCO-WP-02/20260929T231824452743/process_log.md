# Research run REQ-MMC-REBCO-WP-02

**Question:** Which permitted open sources give an insulated or cable-in-conduit fusion REBCO conductor or winding construction with material composition, tape count and conductor or winding-pack current density at about 12-20 T near 20 K?

**Consumer:** goal:magnet-material-comparison/T-003  ·  **Request key:** `29c6343d937df6d120fff1878c99fdc05aaf8ba9141b256174694f48a2ed3e64`

- searched: `Bruzzone 2018 High temperature superconductors for fusion magnets Nuclear Fusion 58 103001 pdf`
- searched: `infoscience.epfl.ch High temperature superconductors for fusion magnets Bruzzone Fietz Minervini Novikov Yanagi Zhai Zheng`
- failed https://iopscience.iop.org/article/10.1088/1741-4326/aad835/pdf — open-access publisher PDF returned a Radware bot-check captcha page to curl; an operator with a browser can download it (queued)
- searched: `Hartwig 2020 VIPER industrially scalable high-current high-temperature superconductor cable SuST 11LT01 pdf`
- searched: `osti.gov High temperature superconductors for fusion magnets Bruzzone 2018 Nuclear Fusion accepted manuscript`
- candidate https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPMAGCP16_16576_submitted.pdf — **keeper** SPC IAEA FEC 2016 preprint: forced-flow REBCO twisted-stack cable layouts (60 kA/12 T TF: 20 strands x 16 tapes 4 mm; 53 kA/18 T CS layouts) and Tcs vs Iop at 8-12 T up to 40 K
- candidate https://dspace.mit.edu/bitstream/1721.1/133134/2/SST_VIPER_Overview_Final.pdf — **keeper** VIPER accepted manuscript (MIT DSpace; fetched via DSpace REST content endpoint after AWS WAF page on bitstream URL): insulated soldered 4-stack cable, Ic 31.5 kA at 10.9 T and 20 K, 27.7 mm OD, cycling degradation 2.0-4.1 percent
- candidate https://infoscience.epfl.ch/entities/publication/bdfd5aac-b4c0-4fdd-9499-18a094464771 — **rejected** Different paper (Use of high temperature superconductors for future fusion magnet system); no bitstream
