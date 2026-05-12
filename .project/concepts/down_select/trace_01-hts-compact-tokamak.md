# Trace: 01-hts-compact-tokamak (CFS ARC)

**Purpose:** Calibration pass populating the `concept_part2.md` trace template end-to-end for a single well-characterized concept. Inputs are the existing synthesis (`exploration/concept_analysis/analyses/01-hts-compact-tokamak/synthesis.md`), dossier (`knowledge/concept_research/01-hts-compact-tokamak/dossier.md`), and `research_q1_q3.md`. Findings about the methodology itself are flagged inline with **[METHOD]** and consolidated at the bottom.

---

## Stage 1 — Physics path (time-and-cost-to-Stage-2 discount)

- **Current TRL / Q achieved:** SPARC under construction (12.2 T burning-plasma demo, Q ~11 target, first plasma ~2027). ARC physics inherits SPARC validation + extrapolates I-mode to ARC operating point (modest field/density extrapolation).
- **Estimated capital and time to Stage-2 entry:** ~$3B already raised by CFS; SPARC + ARC FOAK at ~$12.6B total over ~7–10 years from now. Stage-2 entry conditional on SPARC's 2027–2028 results.
- **Discount-calibration inputs:**
  - *Paradigm co-development:* Very deep. ITER, JET, JT-60SA, DIII-D, plus 4+ private HTS-tokamak programs (Tokamak Energy, Renaissance, Type One via stellarator-HTS adjacency).
  - *Open scientific heritage:* Strong. Sorbom 2015, Colliva 2024, Lin 2020 all peer-reviewed. SPARC physics-basis JPP special issue (2020) is the gold standard.
  - *Workforce depth:* Deep. Tokamak plasma physics is the largest sub-discipline in fusion; MIT/PSFC, ORNL, GA, JET/JT-60 alumni in workforce.
- **Discount applied:** **Low.** Of all 38 concepts, this is the smallest Stage-1 discount available.

**[METHOD] Finding 1:** "Low/moderate/heavy" is too coarse — for this concept the discount could reasonably be "none." Suggest adding a fourth bucket *minimal* or making the discount a numeric multiplier on downstream NPV (`research_q4_q5` likely has anchors).

---

## Stage 2 — FOAK affordability

### Intrinsic F-factors
- **F2.a — Minimum-viable-plant capital cost:** FOAK ARC at $12.6B (synthesis §1). This is **above the $5B "sovereign-only" threshold**. Buyer pool: hyperscaler consortia (Google PPA template) or sovereign anchor. CFS has demonstrated the playbook works for ~$3B raised so far; reaching FOAK requires another ~$9B. **Pole: failure-leaning** (above threshold), but mitigated by existing crossover-platform pull (see E2.a).
- **F2.b — Build-time risk:** 7–10 year build for FOAK ARC after SPARC validates physics (2027–28). Within the Eash-Gates "regulatory ratcheting begins to bite" zone. NRC Part 30 pathway (favorable) partially mitigates. **Pole: moderate failure-leaning.**

### Ecosystem-relational F-factors
- **F2.c — Regulatory framework state:**
  - *Pole:* **Leverage.** NRC Part 30 (byproduct-material licensing) for D-T fusion finalized Feb 2026 — 2.2× cost markup avoided vs. Part 50 (Araiinejad & Shirvan 2025).
  - *Slack/bottleneck:* N/A (regulatory capacity not a scaling constraint at Stage 2).
  - *Caveat:* Part 30 rulemaking specifics for D-T tritium inventory, EPZ, and seismic Category I status remain unsettled — convergence toward Part 50 in practice would erase the leverage. Synthesis §3 rates this 70% confidence.
- **F2.d — Critical component supply maturity:**
  - *Pole:* **Failure.** REBCO at ~$100/kA-m in 2025 — 10× above the $10/kA-m commercial-viability target. CFS is *vertically integrating* REBCO tape manufacturing — the canonical "singleton-internalized" case. FLiBe + Be: no industrial base, fusion must build it. Tritium startup inventory: CANDU-byproduct only, sole-source supply.
  - *Slack/bottleneck:* **Slack at FOAK volumes** (5,730 km REBCO per ARC vs. >3,000 km/yr current production is meetable for FOAK; bottleneck arrives at fleet scale — see F3.a). FLiBe + tritium are bottleneck even at FOAK.

### Distinct E-factors
- **E2.a — Crossover platform attracts non-fusion investment:** **Strong.** REBCO HTS magnets serve MRI ($7B/yr global), grid superconducting cables (R&D + early deployment), maglev transport (Japan SCMaglev operational), high-field NMR. CFS's vertical-integration play is partly funded by non-fusion contracts (rumored CFS-Tape spinout). Pacific Fusion is a different concept entirely; here the analogue is *CFS itself* using non-fusion HTS demand to underwrite the gigafactory.
- **E2.b — Intra-fusion early-mover effect:** **Net negative for ARC; net positive for the cohort.** ARC is itself the first mover of the HTS-tokamak cohort (SPARC validates the magnet, ARC ships the plant). Subsequent cohort members (Tokamak Energy ST-E1, mirror-HTS concepts) inherit CFS-built supply chain. ARC pays the cost; cohort reaps the leverage.

### Plausible FOAK buyer
Hyperscaler-anchor PPA (Google template) + DOE Loan Programs Office + sovereign co-investment. Multi-billion equity tranches from CFS investor base (Breakthrough Energy, Khosla, Coatue, etc.). **No single buyer of the plant**; the wedge is *bundled financing* with the off-take pre-sold.

### Dominant failure factor at this stage
**F2.d (failure pole) + F2.a:** REBCO singleton-internalization at FOAK volumes combined with $12.6B capital ask. The combined kill chain is "REBCO doesn't track to the cost-curve fast enough to make the $12.6B financeable."

### Dominant leverage factor at this stage
**E2.a (crossover platform).** HTS demand from MRI/grid/transport underwrites the REBCO gigafactory CFS must build. Without it, vertical integration is uneconomic at FOAK volume; with it, the gigafactory has a non-fusion revenue floor.

---

## Stage 3 — Chasm crossing

### Intrinsic F-factors
- **F3.b — Site-specialization fraction:** Synthesis §8 C1 calculation: CAS22 reactor plant is 94.7% of direct capital, dominated by factory-modular TF coils (82% of CAS22). Weighted construction-mode score ~3.9–4.4 out of 5 (high modularity). **Pole: leverage-leaning** — far better than ITER-class. The 6–12 month vacuum vessel replacement is *enabled* by demountable joints (a unique architectural choice). Caveat: BOP (cooling towers, buildings) is conventional site-built, but small cost fraction.
- **F3.c — Replication unit size:** 261 MWe FOAK; updated 400 MWe design (unpublished). At ~$12.6B/unit FOAK → ~$30/We — far above $4/We threshold for hyperscaler bulk-ordering. At NOAK $5–6B/unit (if magnet cost halves), 5-unit hyperscaler commit is ~$25–30B. Plausible but constrained. **Pole: failure-leaning at FOAK price, leverage-leaning if NOAK target hit.**

### Ecosystem-relational F-factors
- **F3.a — Supply-chain maturity at chasm scale:**
  - *Pole:* **Failure-leaning at chasm-era volumes, leverage-leaning long-term.** At fleet scale (~10–100 ARC plants/decade × 5,730 km REBCO each → 50,000–500,000 km/yr), demand vastly exceeds current REBCO production. Whether external MRI/grid/transport demand co-scales fast enough to keep slack is uncertain.
  - *Slack/bottleneck:* **Bottleneck at chasm.** This is the single most acute supply risk for this concept. ~8 other fusion concepts also need REBCO; combined demand strains supply even if external markets scale.
- **F3.d — Regulatory amortization path:**
  - *Pole:* **Leverage.** Part 30 framework + standardized ARC design + SPARC precedent → second plant inherits the licensing template. ARC's vertical-integration model also amortizes the regulatory pathway across CFS's planned fleet.
  - *Caveat:* Standardization requires CFS to actually ship identical plants, which competes against site-specific optimization pressure (cooling water, grid interconnect, etc.).

### Distinct E-factors
- **E3.a — Intra-fusion fleet co-development:** **Strong.** ~8 concepts in our 38-candidate set need REBCO (CFS, Tokamak Energy, multiple mirror concepts, some stellarator-HTS programs). Combined fusion demand on REBCO is itself a scale-driver. Cohort R&D on quench protection, joint reliability, AC losses benefits all.
- **E3.b — Shared sub-problem solutions:** **Strong.** FLiBe handling (shared with ARC variants + select IFE liquid-wall concepts). HTS quench protection (shared with all HTS magnet concepts). High-heat-flux divertor (shared with all MFE). Tritium breeding (shared across all D-T concepts).

### Most plausible chasm-crossing path
First 3–5 plants on hyperscaler PPAs (data-center anchor demand for clean firm power at premium $/MWh). Fleet 6–20 on policy-created markets (EU green hydrogen, CBAM-driven industrial decarb). Regulatory amortization helps but the cost gap ($642/MWh NOAK vs. $60–80/MWh wholesale) remains too wide for unsubsidized buyers.

### Dominant failure factor at this stage
**F3.a (failure pole, bottleneck-tagged).** REBCO production at fleet scale is the single constraint that could prevent a 5–20-plant fleet build. Compounds with F4.c (specialty-input cost floor).

### Dominant leverage factor at this stage
**E3.a (intra-fusion fleet co-development).** The 8-concept REBCO cohort is large enough that combined demand drives gigafactory build-out faster than fusion-alone or non-fusion-alone would. This is the single most distinctive structural feature of HTS-tokamak class.

---

## Stage 4 — Learning-curve descent

### Intrinsic F-factors
- **F4.b — Volume vs. R&D learning mechanism:** **Mixed.** REBCO conductor cost is volume-driven (Wright's Law with strong external pull from MRI/grid). Plant integration is R&D-driven (modular maintenance, vessel replacement tempo, FLiBe handling — all benefit from learning-by-doing across the CFS fleet, not from volume). **Pole: moderate.** Not a pure volume story (no billions of identical units) but not a pure R&D story either (REBCO is a commodity ride-along).
- **F4.d — Modularization-vs-scale crossover:** Modular at component level (TF coils, vessel) but plant-scale economy of scale still applies (261 MWe vs. 1 GWe penalty in BOP). Crossover N (where manufacturing learning offsets scale penalty) probably ~10–20 plants for CFS-only; lower if cohort-shared. **Pole: leverage-leaning if cohort hits scale; failure-leaning if CFS goes it alone.**

### Ecosystem-relational F-factors
- **F4.a — Cost-reduction knobs and non-fusion ride-along:**
  - *Knob count:* ~4–5 independent: (1) REBCO $/kA-m trajectory, (2) demountable-joint reliability/replacement labor, (3) FLiBe chemistry plant scale economies, (4) tritium extraction efficiency, (5) capacity factor via maintenance tempo. Below Kavlak's PV count (≥6) but not extreme.
  - *Non-fusion ride-along:* (1) is funded by non-fusion HTS demand (MRI/grid). (2)–(5) are fusion-specific.
  - *Pole:* **Mixed.** Best knob (REBCO) has strong ride-along; other knobs are fusion-funded.
- **F4.c — Specialty-input external-market position:**
  - *Pole:* **Leverage for REBCO; failure for FLiBe/Li-6/Be.** REBCO at fleet scale: non-fusion demand (MRI + maglev + grid + NMR) likely co-dominates with fusion demand → Wright's Law runs from combined volume → cost floor is not bounded by fusion deployment alone. FLiBe and Li-6 have no external market; cost floor is fusion-determined.
  - *Slack/bottleneck:* REBCO **slack-leaning at maturity** (if MRI/grid/transport scale as projected). FLiBe/Li-6 **bottleneck**.

### Distinct E-factors
- **E4.a — Crossover platform revenue funds continued R&D:** **Strong for REBCO.** CFS-Tape (if spun out) sells into non-fusion markets, amortizing R&D investment. WACC reduction at fleet scale could be 100–200 bps.
- **E4.b — Talent inflow from adjacent industries:** **Strong.** Cryogenics + RF engineering + precision welding + power electronics all draw from large adjacent industries (semiconductors, aerospace, medical devices). FLiBe chemistry workforce is narrower (fission MSR programs at Kairos, ORNL alumni).

### Plausible learning-curve mechanism
**Mixed: volume-driven REBCO + R&D-driven plant integration.** Strongest path is fleet build to ~20 plants by 2050; REBCO rides external markets to $15/kA-m; demountable-joint replacement labor descends a learning curve from $123M/swap to <$50M/swap. Cost floor at maturity: $200–300/MWh — *above* unsubsidized grid competitiveness but below advanced fission.

### Dominant failure factor at this stage
**F4.c (failure pole) for FLiBe/Li-6/Be.** Even if REBCO succeeds, fusion-specific specialty inputs cap the cost floor.

### Dominant leverage factor at this stage
**F4.c (leverage pole) for REBCO + E4.a.** Crossover platform revenue + non-fusion demand dominance at fleet scale provides Wright's Law without fusion deployment volume.

---

## Cross-stage carriers

### F-carriers
- **Tritium / Li-6 / Be supply:** Bites hardest at **Stage 4** (self-sufficiency at fleet scale). Stage 2 startup inventory is solvable via CANDU byproduct purchase. Stage 3 scaled breeding ramps with first 3–5 plants. Stage 4 100% self-sufficiency requires Li-6 enrichment capacity that does not exist today.
- **First-wall / divertor / blanket lifetime:** Bites hardest at **Stage 3 and Stage 4** simultaneously. 6–12 month vacuum vessel replacement is the single most acute operational risk for this concept (capacity factor elasticity = −0.96 per synthesis). Acts as a *recurring capex line* at Stage 4 ($2.5–7.4B over 30-year plant life in vessel swaps).
- **HTS conductor cost trajectory:** Bites at all three (covered in F2.d / F3.a / F4.c above).

### E-carriers
- **Fuel-ecosystem R&D position:** D-T cohort is the largest in fusion (~20+ concepts) → shared R&D investment in tritium breeding, Li-6 enrichment, FLiBe chemistry amortizes across the cohort.
- **Workforce / intellectual depth:** Tokamak workforce is the deepest in fusion at Stages 1–2; ARC inherits operational expertise from JET/JT-60/EAST campaigns.

---

## Concept's dominant failure mode (single biggest gate across all stages)

**Stage 3 / F3.a (failure pole, bottleneck-tagged): REBCO supply chain doesn't scale fast enough to support a 5–20 plant fleet at chasm-era timelines.**

*Rationale:* Stage 1 risk is genuinely low for this concept. Stage 2 FOAK is financeable via the crossover-platform-anchored CFS playbook (~$3B raised, more available). Stage 4 cost floor is structurally beatable *if* REBCO rides external demand. The fragility lives at Stage 3, where combined intra-fusion demand on REBCO (8+ concepts) collides with finite gigafactory build-out, and where the 6–12 month vacuum-vessel-replacement tempo must be proven at power-plant cadence — both at the same time.

**[METHOD] Finding 2:** The dominant failure for this concept is genuinely a compound — REBCO bottleneck *and* vessel-replacement tempo. The current template forces a single (stage, F-code) tag. Suggest allowing a primary + secondary failure, or making the dominant-failure tag a *compound code* like `F3.a@bottleneck + ops/vessel-tempo`.

**[METHOD] Finding 3:** "Vessel-replacement tempo" doesn't cleanly fit any F-factor. It's an operational/recurring-capex risk anchored to a specific engineering choice (modular maintenance). Closest fits: F3.b (site-specialization, but vessel-swap is *factory* work) or F4.c (specialty input, but the input is labor and reactor-grade fabrication). Suggest adding **F3.e — Operational tempo at fleet-relevant uptime** as an intrinsic F-factor, or expanding F3.b to include "frequency of disassembly cycles" alongside site-specialization fraction.

## Concept's dominant leverage (single biggest tailwind across all stages)

**Stage 3 / E3.a (intra-fusion fleet co-development) + carries forward to Stage 4 / F4.c leverage pole (REBCO ride-along).**

*Rationale:* The ~8-concept REBCO cohort + ~$7B/yr non-fusion HTS demand combine to drive a gigafactory that fusion-alone could not justify. This is the single structural feature that distinguishes the HTS-tokamak class from every other concept in the candidate set — it makes the Stage-3-to-Stage-4 transition possible by combining intra-fusion scale with external market pull. **Slack-leaning at maturity** (REBCO supply expanding faster than fusion alone could drive).

**[METHOD] Finding 4:** Dominant leverage here is also compound (intra-fusion cohort + non-fusion crossover platform). Same observation as Finding 2 — the spanning algorithm needs to handle multi-tag leverage.

---

## Methodology findings consolidated

1. **Stage-1 discount needs finer granularity.** "Low/moderate/heavy" leaves no room to distinguish this concept (essentially no discount needed) from a heritage-bearing-but-still-distant concept. Numeric multiplier or 4–5 bucket gradation.
2. **Dominant failure / leverage can be compound** for concepts that span structural features. Current template forces single (stage, F-code) tag; spanning algorithm operates on this. Solutions: (a) allow compound tags and adjust spanning to operate on tag *sets*, or (b) force single tag but record the secondary explicitly elsewhere.
3. **Operational-tempo failure mode is missing** from the F-factor taxonomy. Vessel-replacement-frequency for ARC is real, distinctive, and outside the current vocabulary. Either add `F3.e — Operational tempo` or broaden F3.b semantics.
4. **LCOE lower bound emerged naturally** in this trace (Stage-4 mechanism produced "~$200–300/MWh floor"). Suggests it should be a first-class output of every trace, not a tiebreaker — confirming the standing-critique gap #3.
5. **F2.d slack/bottleneck has stage-dependent value.** REBCO at FOAK is slack, at chasm is bottleneck, at maturity is slack again (if external markets scale). The current tag is single-valued; reality is a three-element vector. Either tag per-stage explicitly or accept the simplification.
6. **Concept-cohort positioning is itself an axis.** ARC is *first mover* in the HTS-tokamak cohort — that role choice (pay-the-cost vs. fast-follow) is structural. Suggest adding it as an explicit field per trace: `{first-mover | fast-follower | isolated}`.

---

## What this trace teaches the broader methodology

Populating one trace surfaced six concrete methodology improvements that would not have been visible from staring at the template. Worth committing to populating **a second trace** for a structurally-opposite concept (a physics-gated, isolated, non-cohort concept like p-B11 FRC or stabilized Z-pinch) before locking the template. Two traces will produce a vocabulary good enough to apply at scale.
