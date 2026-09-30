# Research run REQ-MMC-FIELD-01

**Question:** What permitted primary evidence fixes the winding-pack term of the stellarator peak-field relation (Lion et al. 2021 eq. 39, B_max = B_axis·[a0(C)·R/(R−a_coil) + a1(C)·R/√A_wp] or the printed form) for the Stellaris/HELIAS coil sets: printed a0, a1 values, a second (B_max, A_wp) anchor for the same coil set, the explicit cuboid-beam Biot–Savart formula of its appendix A, or a sourced self-field form for a rectangular winding pack (e.g. tokamak PROCESS TF peak-field treatment)?

**Consumer:** goal:magnet-material-comparison/T-011  ·  **Request key:** `837099d4ad5ea84f6efa926a450d30f0d40299b24d674b473b0d9fbd34c44703`

- searched: `registered corpus: Lion 2021 NF 61 126021 eq 37-39, Table 1, appendix A; Lion 2023 thesis; Kovari 2016 Part 2 TF peak field; Stellaris 2025 FED; Proxima simplified CAD`
- searched: `ukaea.github.io PROCESS TF coil peak field ripple fit winding pack peak_tf_with_ripple`
- searched: `Schauer Egorov Bykov 2013 HELIAS 5-B magnet system Fusion Engineering and Design pdf`
- candidate https://aries.pppl.gov/MEETINGS/0709/Dragojlovic.pdf — **rejected** clean-room screen: ARIES program library host; not opened
- candidate https://ukaea.github.io/PROCESS/eng-models/tf-coil-superconducting/ — **keeper** official PROCESS docs: on-coil ripple peaking factor fit f_rip = A0 + A1 e^-t + A2 z + A3 z t vs relative WP toroidal/radial thickness, FIESTA fits for 16/18/20 coils, domain t 0.35-0.99, z 0.2-0.7; the only sourced pack-size dependence of a TF peak field found
- failed https://pure.mpg.de/pubman/item/item_2536884_1 — MPG PuRe record returned HTTP 403 to the fetcher; may hold an author copy of Schauer 2013 HELIAS 5-B magnet system; needs a person to open (queued)
- failed https://doi.org/10.1016/j.fusengdes.2013.01.035 — Schauer, Egorov, Bykov 2013 FED 88 1619-1622 'HELIAS 5-B magnet system structure and maintenance concept': Elsevier, no open-access copy located within the search limit; paywalled (queued)
- candidate https://ukaea.github.io/PROCESS/eng-models/tf-coil/ — **rejected** index page only: axisymmetric B_peak = B_T R0 / R_TF,peak; the ripple treatment lives on the superconducting subpage
