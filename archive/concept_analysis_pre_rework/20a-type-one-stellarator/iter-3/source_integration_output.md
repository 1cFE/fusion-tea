VERDICT: FINDINGS

---

**Source assessment notes:**

- `arxiv-2512-08027` — Thea Energy *Helios* preconceptual design (2-field-period QA stellarator, A=4.5,
  planar/convex HTS coils, X-point divertor, 1.1 GW thermal / 390 MWe, 88% capacity factor, 84-day
  biennial maintenance). This is a different company and concept; no direct contradictions to the
  Infinity Two analysis were found. Its 88% capacity factor and 84-day maintenance window are consistent
  with (and reinforce) the analysis's existing conservative range from Araiinejad & Shirvan. No material
  gaps identified from this source.

- `cambridge-core-services-aop-cambridge-core-content-view` — JPP 2025, E67 (Bader et al., "Power and
  particle exhaust for the Infinity Two fusion pilot plant"). This is one of the six-paper Type One
  Energy physics basis series and is a direct primary source for Infinity Two. It is not extracted in
  the Phase 1a dossier. Three material gaps are identified below.

---

### F-1: Island divertor is two distinct design options with different TRL — not a single concept

- **Target:** Section 3 (Island Divertor at Burning Plasma Power Level — TRL 3–4) and Section 2
  (challenge 4, island divertor performance)
- **Category:** analysis
- **Finding:** The E67 paper defines two separate divertor designs under development for Infinity Two:
  (1) a classical island divertor following W7-X geometry (8 plates, 2 per field period), and (2) a
  novel Large Island Backside Divertor (LIBD) with a dome structure inserted inside the island interior
  plus active baffling, designed to improve neutral confinement and particle exhaust. The current
  analysis treats island divertor as a single TRL 3–4 system. In practice, these represent two
  scenario branches with substantially different risk profiles: the classical design is a direct
  W7-X extrapolation (TRL 4–5) but has critically poor particle exhaust efficiency (0.44–2.9%,
  W7-X scale), while the LIBD targets 12.6% exhaust efficiency but is TRL 2–3 and explicitly requires
  Infinity One experimental validation before Infinity Two final design commitment. The LIBD dome must
  survive deep inside the island interior with challenging active cooling access — a cooling access
  problem the E67 paper does not resolve and flags as future work. Choosing the classical divertor
  reduces TRL risk but may create a particle exhaust shortfall that affects steady-state operability
  and availability; choosing the LIBD preserves exhaust performance but adds a TRL 2–3 item to the
  critical path. This is a scenario-determining design choice, not a single system at a single TRL.
- **Recommendation:** Split the island divertor discussion in Section 3 into two named options
  (classical and LIBD) with separate TRL ratings (4–5 vs 2–3), separate validation requirements, and
  separate O&M implications. In Section 2, update challenge 4 to distinguish the exhaust efficiency
  gap as the core reason the LIBD exists and flag LIBD cooling-access uncertainty as an additional
  cost/schedule risk on top of the general island divertor unknowns. Add a row to the Section 6 data
  gap inventory for divertor design selection (classical vs LIBD) as a scenario branch with blocking
  criticality for the availability and O&M model.
- **Priority:** important

---

### F-2: Error field correction coil requirement is an unresolved capital cost risk — not mentioned anywhere in the analysis

- **Target:** Section 2 (Challenges) and Section 6 (Data Gap Inventory)
- **Category:** analysis
- **Finding:** E67 explicitly states that sensitivity of the Infinity Two divertor design to magnetic
  field errors is "left to future work." W7-X required auxiliary external correction coils to suppress
  low-order error modes (n/m=1) that would otherwise degrade island topology and divertor
  performance. The current Infinity Two design goal is to avoid such auxiliary coils, but this has not
  been validated — it is an open engineering question. If field errors at Infinity Two scale require
  correction coils, this is an unbudgeted capital item (additional coil systems, power supplies, and
  cryogenic infrastructure) with no cost estimate. The current analysis does not mention error field
  correction coil requirements anywhere in Sections 2, 3, 5, or 6.
- **Recommendation:** Add a brief item to Section 2 under challenge 1 or as a new challenge noting
  that error field tolerance for the Infinity Two island divertor topology is unvalidated, that W7-X
  required auxiliary correction coils, and that the need for equivalent coils in Infinity Two has not
  been assessed. Add a corresponding row to the Section 6 data gap inventory (gap type: truly-unknown,
  criticality: important) noting that if correction coils are required, this adds unbudgeted capital
  to CAS22 with no published cost basis.
- **Priority:** important

---

### F-3: Particle exhaust efficiency range (order-of-magnitude uncertainty) is an LCOE-relevant parameter missing from Section 5

- **Target:** Section 5 (LCOE-Relevant Parameters) and Section 2 (challenge 4)
- **Category:** analysis
- **Finding:** E67 quantifies the required particle exhaust efficiency for Infinity Two as 0.5%–5%
  (bracketing conservative and optimistic particle-transport assumptions), with W7-X-equivalent
  classical divertor achieving only 0.44%–2.9% and the LIBD targeting 12.6% (untested). This
  order-of-magnitude uncertainty in pumping efficiency directly sizes the vacuum pumping system — a
  larger pump installation is needed at lower exhaust efficiency — and affects whether steady-state
  helium ash removal is achievable at all with the classical design. The current analysis flags island
  divertor performance at burning plasma conditions as Impact: Moderate but does not capture exhaust
  efficiency as a specific parameter, does not quantify the vacuum pumping system cost sensitivity,
  and does not state that the classical divertor may be marginal for helium ash removal at burning
  plasma throughput. This gap leaves the Section 5 parameter table silent on a component cost driver
  that the primary source explicitly calls out as a major design uncertainty.
- **Recommendation:** Add a row to the Section 5 available/missing parameters table for particle
  exhaust efficiency, with value 0.44%–12.6% depending on divertor design choice, source E67, and
  low confidence. In Section 2, update challenge 4 to state that classical divertor exhaust efficiency
  (W7-X analogue) is at the low end of the required 0.5%–5% range and may require LIBD to ensure
  reliable helium ash removal over a 2-year operating cycle. Add exhaust efficiency as a scenario
  parameter in Section 6 linked to the divertor design selection gap.
- **Priority:** important
