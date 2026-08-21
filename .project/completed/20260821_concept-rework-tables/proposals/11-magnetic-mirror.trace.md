# Design Point Reasoning Trace — 11-magnetic-mirror

## 1. Sources walked

- `knowledge/concept_research/11-magnetic-mirror/dossier.md` — synthesized concept summary; identified the WHAM → Anvil → Hammir development pathway, named Frank et al. arXiv 2411.06644 and the APS DPP 2025 Sutherland talk as the two sources that quote a published `P_native` for Hammir, and confirmed no other Realta design has an electrical-output figure in the dossier
- `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions.md` — Frank et al. 2024 Hammir tandem mirror pre-conceptual design paper; provides the only published Hammir operating point with stated geometry (ℓ_c = 50 m central cell, B_m = 25 T, a_m = 0.15 m), heating (P_NBI = 30 MW into end plugs), fusion power (P_fus = 157.4 MW), and a derived P_ele,out > 50 MWe under stated efficiency assumptions (η_NBI = 60%, η_ele = 50% Brayton, C_mult = 1.1). Also references and explicitly rejects the Fowler et al. 2017 classical tandem mirror design as too aggressive (β ~ 1, T_i = T_e = 150 keV, 1 MeV NBI, P_fus > 1 GW).
- `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/aps-dpp-2025-sutherland.md` — APS DPP 2025 Sutherland presentation; corroborates the Hammir target (Q_e > 1, P_ele,out > 50 MWe, 3+ hour continuous operation) and confirms Anvil is an end-plug demonstrator / D-T volumetric neutron source rather than a power plant. The shortest, most authoritative confirmation of Hammir's stated `P_native`.
- `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/realta-fusion-hub-spotlight.md` — Fusion Hub spotlight on Realta; corroborates the WHAM → Anvil → Hammir pathway, the HTS-enabled mirror-ratio approach, and the hybrid (thermal + DEC) energy capture; useful for fuel and architecture context but does not introduce a separate design candidate with its own published `P_native`.
- `knowledge/concept_research/11-magnetic-mirror/iter-01/sources/wham-experiment-details.md` — WHAM experiment description; confirms WHAM is a physics test stand (17 T REBCO, ECH + NBI + HHFW) with no electrical output by design.
- `knowledge/concept_research/11-magnetic-mirror/iter-02/sources/fusion-report-interview-realta.md` — Realta interview; confirms the Q > 5 / Q_e > 1 targets, the dual thermal + DEC energy capture, the ~7 MW per meter of center-cell scaling, and the qualitative statement that Q > 10 is reachable with a longer center cell. Provides no separate engineered design point.

## 2. Candidates surfaced

**WHAM (Wisconsin HTS Axisymmetric Mirror, operational 2024)**
University of Wisconsin–Madison experiment sponsored by Realta. Simple-mirror physics test stand with two 17 T CFS-built HTS magnets, ECH + NBI + HHFW heating. Designed as a confinement physics demonstrator; no D-T operation, no electrical output by design. P_native: none. Disqualifies as design point per the selection rule.

**Anvil (Realta's next-step simple mirror, ~2028)**
Per Frank et al. and the Sutherland APS DPP 2025 talk, Anvil is a "commercial-scale high-field simple mirror" whose primary objective is to demonstrate stable sustainment of tandem-mirror end-plug conditions, with a secondary role as a D-T volumetric neutron source for materials testing. Anvil is in the same class as the BEAM device of Forest et al. 2024. No net electric output is part of Anvil's design intent. P_native: none. Disqualifies as design point.

**Hammir pilot plant — Frank et al. 2024 conservative operating point**
The named Realta Fusion pilot plant and the focus of Frank et al. (arXiv 2411.06644). The paper explicitly identifies a "more conservative" classical tandem mirror operating point as the Hammir reference design: B_m = 25 T (HTS end-plug mirror coils), a_m = 0.15 m, ⟨n⟩_p = 1.5×10²⁰ m⁻³, ℓ_c = 50 m, β_c ≈ 0.6, n_c/n_p ≈ 0.55, T_i ≈ 45 keV, T_e ≈ 125 keV, P_NBI = 30 MW into the end plugs. Computed performance: P_fus = 157.4 MW; with η_NBI = 60%, η_ele = 50% (Brayton), C_mult = 1.1 the operating point satisfies the NASEM "Bringing Fusion to the U.S. Grid" pilot plant criterion of continuous net electricity P_ele,out > 50 MWe for at least 3 hours. The APS DPP 2025 Sutherland talk independently restates the Hammir targets as Q_e > 1, P_ele,out > 50 MWe, ≥ 3 hr continuous. Fuel: D-T central cell (with the paper noting a T-only end plug is optimal classically). Maturity tier: paper-concept (RealTwin / POPCON modelling; no Hammir hardware yet — the precursor Anvil is roughly five years out per the dossier).

**Hammir "longer-center-cell" variant (Q > 10 to ~Q = 20)**
Mentioned in the Fusion Report Realta interview and in the dossier (~7 MW per additional meter of central cell, theoretical ~500 MW from Q = 20). This is a qualitative scaling statement, not a separately engineered design point: no specific ℓ_c is named, no operating point is documented, and the electrical-output number ("~500 MW fusion" or any associated P_ele,out) is informal. Does not qualify as a primary design point per the selection rule, but is a meaningful alternative for the sensitivity branch.

**Fowler et al. 2017 classical tandem mirror (Fowler, Moir, Simonen)**
Frank et al. cites this as the prior-art aggressive tandem mirror design: B_m = 24 T, a_m = 0.21 m, ⟨n_p⟩ = 2.6×10²⁰ m⁻³, ℓ_c = 55 m, β_c ~ 1.0, T_i = T_e = 150 keV, 1 MeV NBI, P_fus > 1 GW. Frank et al. explicitly position Hammir as the "more conservative" replacement for this design; Fowler et al. 2017 is not Realta's pilot plant. It also has no engineering design beyond a paper concept, and its high-β / 1 MeV / 150 keV parameters are flagged as outside what the underlying physics and engineering can currently support. Considered and rejected as the Realta-concept design point.

**Realta "100–200 MW initial deployment" (Frank et al. acknowledgements line)**
The Frank et al. acknowledgements section says Realta is "targeting initial fusion power plant deployment at the 100–200 MW scale at industrial sites and datacenters for process heat and/or electricity." This is a single corporate-targeting sentence, with no geometry, no operating point, no fuel mix, no thermal-vs-electric breakdown, and no distinction from Hammir. Per the plant-stitching prohibition this cannot be paired with the Hammir geometry, and on its own it is not an engineered design candidate.

## 3. Selection

The Hammir pilot plant operating point published in Frank et al. 2024 (the 25 T / 0.15 m / 50 m / 30 MW NBI / 157.4 MW fusion / >50 MWe net-electric case) is selected. WHAM and Anvil are excluded — both are physics demonstrators with no net electrical output by design. The Fowler et al. 2017 tandem mirror is excluded — it is the prior-art design Hammir was specifically engineered to be more conservative than, and is not the Realta pilot plant. The longer-center-cell Q > 10 variant is excluded — it is a qualitative scaling statement, not a documented operating point with geometry and power. The 100–200 MW industrial-deployment line in the acknowledgements is excluded — it is a one-sentence corporate-targeting note without a design, and adopting it would require plant-stitching it onto Hammir's geometry.

`P_native` is set to **50 MWe**, the value the Frank et al. operating point is explicitly engineered to deliver and that the Sutherland APS DPP 2025 talk independently restates as the Hammir net-electric target. Using the computed 157.4 MW fusion is not appropriate — that is thermal, not net electric — and using a higher figure would require an undocumented assumption about cycle efficiency, DEC contribution, or center-cell length that the paper does not commit to for Hammir.

Grounding confidence is **medium**. The physics design point is well-grounded in a peer-style RealTwin / POPCON analysis with stated geometry, heating, end-plug density, and central-cell parameters, and the electrical-output figure traces to a specific operating point rather than a slogan. However, the chosen design point has substantial engineering gaps relative to a `high` grade: the blanket type, direct energy converter architecture, and overall balance-of-plant are not specified in published sources; Realta's announced Hammir pre-conceptual engineering design paper is expected in 2026 and would materially raise grounding if it lands. Maturity tier is `paper-concept` — Hammir exists only as POPCON + RealTwin simulation; the precursor Anvil hardware does not yet exist.

```yaml
proposal:
  concept_id: 11-magnetic-mirror
  design_name: "Hammir pilot plant — Frank et al. 2024 conservative operating point (Realta Fusion)"
  maturity_tier: paper-concept
  grounding_confidence: medium
  p_native_mwe: 50
  primary_sources:
    - knowledge/concept_research/11-magnetic-mirror/iter-01/sources/arxiv-2411-06644-confinement-predictions.md
    - knowledge/concept_research/11-magnetic-mirror/iter-01/sources/aps-dpp-2025-sutherland.md
  selection_rationale: |
    The Hammir pilot plant is Realta Fusion's only published design point with a stated net
    electrical output. Frank et al. 2024 (arXiv 2411.06644) specifies a concrete operating
    point — B_m = 25 T, a_m = 0.15 m, ℓ_c = 50 m, P_NBI = 30 MW, ⟨n⟩_p = 1.5×10²⁰ m⁻³,
    β_c ≈ 0.6, T_i ≈ 45 keV, T_e ≈ 125 keV — producing 157.4 MW of D-T fusion and, under
    stated efficiency assumptions (η_NBI = 60%, η_ele = 50% Brayton, C_mult = 1.1),
    satisfying the NASEM pilot plant criterion of P_ele,out > 50 MWe continuous. The APS
    DPP 2025 Sutherland talk independently restates the Hammir target as Q_e > 1,
    P_ele,out > 50 MWe, 3+ hours. WHAM and Anvil have no electrical output by design and
    are excluded. The Fowler et al. 2017 classical tandem (P_fus > 1 GW at β ~ 1, 150 keV,
    1 MeV NBI) is the prior-art design Hammir was specifically engineered to be more
    conservative than, and is not Realta's pilot plant. P_native is set to the 50 MWe
    Hammir is engineered to deliver, not the 157.4 MW thermal fusion power.
  alternatives_considered:
    - design: "WHAM (Wisconsin HTS Axisymmetric Mirror, UW–Madison)"
      reason_rejected: physics test stand; no electrical output by design
      sensitivity_implication: "n/a — WHAM has no P_native and cannot serve as a design point."
    - design: "Anvil (Realta simple-mirror end-plug demonstrator / DT neutron source)"
      reason_rejected: end-plug physics demonstrator and materials-test neutron source; no net electric output by design
      sensitivity_implication: "n/a — Anvil has no P_native and cannot serve as a design point."
    - design: "Hammir longer-center-cell variant (Q > 10, ~500 MW fusion scaling)"
      reason_rejected: qualitative ~7 MW/m scaling statement; no documented geometry, operating point, or net-electric figure
      sensitivity_implication: >
        If picked instead, P_native would be substantially higher (a longer center cell at
        the same ~7 MW/m thermal scaling and similar conversion chain would push net electric
        well above 50 MWe → fewer modules at 1 GWe → 1 GWe LCOE shifts down. Worth probing
        if Realta publishes an engineered longer-ℓ_c Hammir variant with its own operating
        point.
    - design: "Fowler, Moir & Simonen 2017 classical tandem mirror"
      reason_rejected: prior-art aggressive design (β ~ 1, T_i = T_e = 150 keV, 1 MeV NBI, P_fus > 1 GW) that Frank et al. explicitly position Hammir as more conservative than; not Realta's pilot plant
      sensitivity_implication: >
        If picked instead, P_native would be much higher (>1 GW fusion class implies ≫ 50 MWe
        net) → far fewer modules at 1 GWe → 1 GWe LCOE shifts down substantially. Worth
        probing only if HTS magnets, 1 MeV NBI, and high-β operation mature enough for that
        operating regime to become Realta's design point.
    - design: "Realta '100–200 MW initial deployment' note (Frank et al. acknowledgements)"
      reason_rejected: one-line corporate-targeting statement; no geometry, no operating point, ambiguous between thermal and electric, and not a separate engineered design
      sensitivity_implication: >
        If this targeting line resolves into an engineered deployment design at ~100–200 MW
        net electric, P_native would rise (likely 2–4×) → fewer modules at 1 GWe → 1 GWe
        LCOE shifts down. Eligible for design-point revisit when Realta publishes a deployment
        design (industrial heat or electricity) with its own engineering parameters.
```

## 4. Open questions

- **Hammir pre-conceptual engineering design (expected 2026 per dossier)**: Realta has signalled a forthcoming Hammir engineering design paper. If it specifies a blanket type, DEC architecture, and a committed thermal cycle — and especially if it commits to a center-cell length or NBI configuration different from the Frank et al. 2024 conservative point — `grounding_confidence` would upgrade from `medium` to `high` and `P_native` could shift. This is the primary watch-item for re-selection.
- **Center-cell length commitment**: The Frank et al. operating point uses ℓ_c = 50 m, but the dossier (citing the Realta interview) repeatedly emphasises Realta's ability to scale linearly with center-cell length at ~7 MW/m and notes that Q > 10 is reachable with a longer cell. If Realta commits Hammir to a longer center cell at a documented operating point, the design-point row should be revised to that case rather than the 50 m / 50 MWe conservative point.
- **Direct energy conversion contribution**: Frank et al. uses a plain 50% Brayton cycle efficiency to derive 50 MWe and notes DEC could enhance performance. The dossier highlights venetian-blind DEC as a Realta architectural feature; the MARS historical reference reports ~54% DEC efficiency. If Realta commits to a hybrid efficiency higher than the Brayton-only baseline, the same geometry could publish a higher `P_native`, forcing a revisit.
- **Industrial heat vs net electric framing**: Realta's recent SVB funding round and public messaging emphasise industrial process heat as an early market. If Realta publishes a Hammir variant whose `P_native` is denominated in MWth rather than MWe, the design-point row would either need a unit-conversion convention or a different selected variant.
