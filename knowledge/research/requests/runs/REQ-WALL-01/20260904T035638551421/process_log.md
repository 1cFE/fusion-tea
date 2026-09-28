# Research run REQ-WALL-01

**Question:** What is the peak-to-average neutron wall load ratio (first-wall peaking factor) for a quasi-isodynamic or helical-axis stellarator reactor, and on what geometry is it defined?

**Consumer:** 20260903-priced-levers#1  ·  **Request key:** `9b38f15645d0c139bc38ee1724694f68d4591af10b395c1516d4cddd63c51142`

- searched: `HELIAS 5-B neutronics analysis neutron wall loading maximum average first wall`
- candidate https://pure.mpg.de/rest/items/item_3017527_3/component/file_3215814/content — **keeper** Haeussler, Warmer, Fischer -- 'Neutronics analyses for a stellarator power reactor based on the HELIAS concept'. Table 2 prints maximum and average NWL for HELIAS-5B by two independent codes (KIT DAGMC and IPP nflux); text states the average is total NWL divided by total plasma-facing area. No ARIES-CS content, not even a reference.
- candidate https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPS2CPR17_17310_submitted-4.pdf — **rejected** EUROfusion preprint cover-sheet version of the same Haeussler et al. ISFNT paper already taken as keeper via pure.mpg.de; duplicate content, no added numbers.
- searched: `deterministic method fast evaluation optimisation 3D neutron wall load generic stellarator configurations peak average`
- candidate https://iopscience.iop.org/article/10.1088/1741-4326/ac6a67 — **keeper** Lion et al., Nucl. Fusion 62 (2022) -- deterministic 3D NWL evaluation for generic stellarator configurations; open access; reports peak and average NWL per configuration including HELIAS-5, with wall-geometry variants. Method paper on HELIAS/QA configurations, no ARIES-CS design data.
- failed https://iopscience.iop.org/article/10.1088/1741-4326/ac6a67/pdf — iopscience.iop.org serves a Radware bot-check page to the extractor, so the URL registration captured that interstitial instead of the open-access paper. It committed a junk registry entry at slug 'a_deterministic_method_for_the_fast_evaluation_and' (title 'We apologize for the inconvenience...', 1415-byte output.md) which an operator must remove -- the registry CLI has no unregister. The paper itself IS registered, correctly, from the publisher PDF at slug 'a_deterministic_method_for_the_fast_evaluation_and_2'. Nothing about the question is blocked; only the junk entry needs a human. (queued)
