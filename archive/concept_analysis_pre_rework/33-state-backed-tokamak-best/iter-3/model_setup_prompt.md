# 1costingfe Model Update: State-Backed Tokamak - BEST

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

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

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

### F-1: Chinese construction discount applied only to CAS21 buildings — H1 untestable
- **Target:** Model scenario output (§Scenario: Chinese construction cost discount) and Section 2 (H1 hypothesis)
- **Category:** model
- **Finding:** The analysis's primary economic hypothesis — H1: "If the Chinese 2× construction cost discount holds for fusion, PFPP LCOE drops from ~140 $/MWh to ~80 $/MWh (capital cost halved at ~70% capital share of LCOE)" — cannot be tested by the current model. The discount is applied only to CAS21 Buildings ($787M, ~8% of total capital). A 4× buildings discount produces only 11 $/MWh change (140.6 → 129.2), far short of H1's ~60 $/MWh prediction. H1 requires the discount to apply broadly across all construction-labor-intensive capital accounts. CAS21+CAS22+CAS23+CAS24+CAS25+CAS26 total ~$5,813M (~57% of overnight capital), and the labor-intensive CAS22 reactor plant equipment ($4,514M) is precisely the account where Chinese labor rate differentials, domestic supply chains, and streamlined regulatory costs would apply. The analysis correctly identifies this as the concept's most distinctive differentiator (Impact: High) — the model must be able to test it.
- **Recommendation:** Expand the Chinese construction discount scenario to cover all direct capital accounts (CAS21–CAS26), not just buildings. Rerun the three-scenario table (1×, 2×, 4× discount) with this broader scope. The resulting LCOE range should approach H1's ~80 $/MWh prediction at 2× discount, making the hypothesis testable and meaningful. Document which accounts are discounted and why in the scenario output.
- **Priority:** blocking

### F-2: No commercial Q value sweep — cliff-edge behavior near viability threshold not revealed
- **Target:** Model sensitivity sweep (§Sensitivity) and Section 5 commercial PFPP parameter table
- **Category:** model
- **Finding:** The analysis identifies commercial PFPP Q as low-confidence spanning Q=5–15, yet the model fixes Q~10 (p_input=200 MW) and sweeps only capacity factor, blanket type, and buildings discount. This omits a critical non-linearity. At Q=5, p_input rises to ~735 MW thermal; at 60% wall-plug efficiency that requires ~1,225 MW of electrical recirculating power. With gross electrical output ~1,270 MWe (from 3,673 MW fusion at 34.7% efficiency), net output collapses near zero. The current p_input elasticity of +0.09 at Q=10 gives no hint of this behavior — it only samples the benign high-Q operating regime. The analysis's Section 2 H&CD challenge and Section 6 gap #11 both flag Q as uncertain and high-stakes, but the model does not explore it.
- **Recommendation:** Add a Q sweep from Q=5 to Q=15 at fixed plant geometry, reporting both LCOE and net electrical output at each point. This will reveal the minimum economically viable Q for the PFPP design point and expose the non-linear cliff edge that the current sensitivity table obscures. The sweep output should appear alongside the existing CF and blanket-type scenarios.
- **Priority:** important

### F-3: LTS vs HTS cost comparison — "central LCOE question" unanchored in Section 7
- **Target:** Section 7 (cross-concept positioning, final modeling parameters paragraph)
- **Category:** analysis
- **Finding:** Section 7 correctly names 01-hts-compact-tokamak and 28-hts-tokamak-full-hts as structurally appropriate nearest neighbors and identifies the LTS-large-machine vs. HTS-compact-machine trade-off as "the central LCOE question for LTS-based commercial tokamaks." It then defers resolution entirely, pending approval of those analyses. The analysis already has all inputs needed to make a rough parametric bound: BEST magnet mass ~2,000 t at R₀=3.6 m; a CFETR-class PFPP at R₀≈5.7 m implies ~3–4× the magnet mass (~6,000–8,000 t); Nb3Sn at $2–10/kA-m. Even an order-of-magnitude estimate of total LTS conductor cost per net MWe, compared to a compact HTS design using published REBCO pricing at SPARC-class conductor volume, would anchor whether the LTS route is cheaper or more expensive in capital terms — the question the analysis names as central but leaves entirely open.
- **Recommendation:** Add a short paragraph in Section 7 (under the nearest-neighbor comparison) providing a rough bound: estimate total LTS conductor cost for the PFPP using published Nb3Sn pricing and ARIES-AT magnet mass scaling, and compare it to a compact HTS design at equivalent net electrical output using REBCO pricing and CFS/Tokamak Energy scale. Label clearly as an order-of-magnitude estimate. Even a 2–5× uncertainty band would be more useful than the current qualitative deferral of the concept's defining cost question.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/33-state-backed-tokamak-best/iter-3/model_setup.py`
