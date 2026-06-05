VERDICT: FINDINGS

### F-1: CFETR Phase II (DEMO-class scenario) absent from analysis

- **Target:** Section 5 (CFETR parameter table) and Section 2 (experimental device extrapolation challenge)
- **Category:** analysis
- **Finding:** The arxiv-1907-11919 paper (Deng et al. 2019) presents CFETR Phase II as a validated DEMO-adjacent scenario within the same machine footprint: Pfus = 1084 MW, Qfus = 23.5, fbs = 89%, Ip = 11 MA, NWL ≈ 6× Phase I. The existing analysis models CFETR Phase I (200 MW) as the only anchored intermediate step and then leaps to an unspecified commercial PFPP. Phase II is the actual bridge between the experimental device and commercial operation — its parameters are essential for bounding PFPP extrapolation. Two material Phase II risks are also absent: (a) Phase II divertor heat load (~32 MW/m) exceeds ITER design guidelines and requires active radiative cooling mitigation not yet validated; (b) Phase II requires pellet injection fueling (not yet implemented in simulations) and RWM feedback stabilization (not yet modeled). These are not cosmetic additions — they directly affect the maturity and risk characterization of the extrapolation chain that the LCOE estimate rests on.
- **Recommendation:** Add a CFETR Phase II block to the Section 5 parameter table: Pfus = 1084 MW, Qfus = 23.5, fbs = 89%, Ip = 11 MA, H98y2 ≈ 2.4, NWL ≈ 1.1 MW/m² (source: arxiv-1907-11919). In Section 2 (experimental device extrapolation challenge), add a paragraph noting that Phase II validates DEMO-class feasibility in principle but with outstanding readiness gaps: divertor heat flux exceeding ITER limits, pellet injection requirement, and RWM stabilization. Add arxiv-1907-11919 as a numbered source in Section 8.
- **Priority:** blocking

---

### F-2: CFETR Phase I geometry superseded — model anchors to stale design point

- **Target:** Section 5 (CFETR Phase I parameter table) and Section 7 (PFPP modeling parameters)
- **Category:** model
- **Finding:** The existing analysis anchors CFETR Phase I to R₀ = 5.7 m, B₀ = 5 T (from osti-pages-servlets-purl-1465662). The 2019 paper (arxiv-1907-11919) validates a preferred larger configuration at R₀ = 6.6 m, B₀ = 6.0 T, Ip = 7.6 MA, which achieves Qfus = 3.2 with H98y2 = 1.31 and 54 MW of auxiliary power — better performance with the same heating investment. The two papers represent different design iterations; the 2019 update is the preferred configuration. Machine volume scales approximately as R³, so the transition from R₀ = 5.7 m to R₀ = 6.6 m implies roughly 55% more plasma volume. This propagates directly to magnet mass, structural steel, vacuum vessel, and blanket area estimates used in capital cost scaling — all currently anchored to the smaller geometry.
- **Recommendation:** Update the CFETR Phase I parameter rows in Section 5 to reflect R₀ = 6.6 m, B₀ = 6.0 T, Ip = 7.6 MA, Pfus = 171 MW, Qfus = 3.2 (source: arxiv-1907-11919), with a note that the 5.7 m design (osti-pages-servlets-purl-1465662) is an earlier iteration. In Section 7 (PFPP modeling parameters), update the PFPP capital cost scaling basis to use the 6.6 m geometry, and note that the revised geometry makes ARIES-ACT1 (R₀ = 6.25 m, B₀ = 6.0 T, from osti-servlets-purl-1178069) a closer Western cost analog than ARIES-AT (R₀ = 5.2 m) for the overnight capital cost estimate.
- **Priority:** important

---

### F-3: ARIES-ACT1 is geometrically closer to CFETR than ARIES-AT — cost baseline should shift

- **Target:** Section 7 (Cross-Concept Notes, modeling parameters) and Section 5 (PFPP overnight capital cost row)
- **Category:** model
- **Finding:** The existing analysis uses ARIES-AT (R₀ = 5.2 m, B₀ = 5.9 T) as the primary Western cost analog for PFPP capital cost estimation. The osti-servlets-purl-1178069 source is the ARIES-ACT study (Kessel et al.), which includes ARIES-ACT1: R₀ = 6.25 m, B₀ = 6.0 T with SiC/SCLL blanket and 58% thermal efficiency, and ARIES-ACT2: R₀ = 9.75 m, B₀ = 8.75 T as a conservative variant. ARIES-ACT1's geometry (R₀ = 6.25 m, B₀ = 6.0 T) is far closer to the updated CFETR (R₀ = 6.6 m, B₀ = 6.0 T) than ARIES-AT. Applying ARIES-AT cost scaling to a 6.6 m machine introduces systematic error because capital cost drivers (magnet conductor length, vacuum vessel area, structural steel) scale non-linearly with machine size. ARIES-ACT2 (R₀ = 9.75 m) provides the upper bound for a conservative LTS design, bracketing the PFPP estimate more tightly than ARIES-AT alone.
- **Recommendation:** In Section 7 PFPP modeling parameters list, replace or supplement ARIES-AT with ARIES-ACT1 as the primary Western cost analog, noting the geometry match (6.25 m vs. 6.6 m). In Section 5, update the overnight capital cost row's source annotation to reference ARIES-ACT1 alongside ARIES-AT. Add osti-servlets-purl-1178069 as a numbered source in Section 8 (ARIES-ACT study, Kessel et al., describing four commercial tokamak configurations from ACT1 advanced to ACT2 conservative).
- **Priority:** important
