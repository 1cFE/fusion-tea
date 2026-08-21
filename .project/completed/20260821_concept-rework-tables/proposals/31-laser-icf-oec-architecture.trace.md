# Design Point Reasoning Trace — 31-laser-icf-oec-architecture

## 1. Sources walked

- `knowledge/concept_research/31-laser-icf-oec-architecture/dossier.md` — synthesized concept summary; confirmed BLF publishes a single reactor architecture across a 1–10 Hz parametric range; no separate named commercial plant or near-term demonstrator with electrical output
- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/optics-express-2025-paper.md` — Sunahara et al. 2025, *Optics Express* 33(22), 47104–47120; primary authority source; contains Table 2 with the complete power balance (E_L = 5 MJ, G = 160, η_e = 0.44, P_grid = 102–2820 MW at f = 1–10 Hz), laser architecture (500 CBC-OEC modules, 150 m cavities, 10 kJ each), chamber design (radius 8–10 m), and OEC prototype results (1.5 m benchtop, finesse 419,000, enhancement 59,000)
- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/blf-website-and-news.md` — BLF website extraction; confirmatory value only — D-T fuel, dual energy conversion, 5 MJ laser, ~1 GW plant ambition
- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/finance-news-blue-laser-fusion-completes-37-114500457/output.md` — Series Seed announcement (March 2024, $37.5M); states "prototype by 2025, commercial-ready fusion reactor by 2030"; no reactor parameters
- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/semiconductor-today-news-items-2025-oct-blue-laser-fusion/output.md` — DOE INFUSE 2025 award (OEC mirror coating collaboration with Colorado State University); no new design parameters
- `knowledge/concept_research/31-laser-icf-oec-architecture/iter-02/sources/semiconductor-today-news-items-2025-oct-bluelaserfusion/output.md` — Japan JST Moonshot Goal 10 selection; no new design parameters
- `knowledge/concept_research/31-laser-icf-oec-architecture/changelog.md` — iteration log; confirms one Phase 1a iteration, 11/12 columns at high confidence, no alternative BLF designs found
- `exploration/concept_analysis/analyses/31-laser-icf-oec-architecture/analysis.md` — D1+ analysis (draft); used for source cross-referencing only per instructions; design-point choice made fresh here

## 2. Candidates surfaced

**BLF OEC Reactor — 10 Hz operating point (Sunahara et al., 2025)**
The Sunahara et al. paper describes a single reactor concept: 500 CBC-OEC modules, 5 MJ UV per shot, cryogenic D-T targets at 1–10 Hz, shock ignition, He-cooled LiPb blanket, and direct energy conversion. Table 2 presents two representative operating cases. At 10 Hz: P_grid = 2820 MWe, f_re = 0.170. Derivation: E_L × G × f × η_e × (1 − f_re) − P_op = 5 MJ × 160 × 10 Hz × 0.44 × 0.830 − 100 MW = 2820 MWe. Fuel: D-T (cryogenic). Chamber radius: 8–10 m. Maturity: paper-concept. This is the paper's commercial design point.

**BLF OEC Reactor — 1 Hz operating point (Sunahara et al., 2025)**
The same 500-module hardware at 1 Hz. P_grid = 102 MWe, f_re = 0.426. This is the lower bound in Table 2. At 42.6% recirculating power fraction the 1 Hz case is economically marginal — the paper does not frame it as a commercial design but as the minimum operating bound of the parametric range. Same geometry and fuel as the 10 Hz candidate.

**BLF "~1 GWe commercial plant" (BLF website)**
The BLF website references approximately 1 GWe as a commercial plant ambition. This is not a distinct design with published engineering parameters — it is an intermediate point on the parametric continuum (approximately 3.5 Hz back-calculated from the Table 2 power balance). No separate geometry, efficiency chain, or engineering parameters exist for this implied operating point. An aspirational scale statement, not a named engineering design.

## 3. Selection

BLF has published one reactor concept across a parametric rep-rate range. The 10 Hz case is selected because it is the economically viable design target (f_re = 0.170 vs. 0.426 at 1 Hz), the operating mode Table 2 presents as the commercial power plant case, and the only mode for which the full power balance and efficiency chain are fully worked. The 1 Hz case is the marginal lower bound of the same hardware, not the commercial target. The website's "~1 GWe" framing has no distinct engineering parameters.

```yaml
proposal:
  concept_id: 31-laser-icf-oec-architecture
  design_name: "BLF OEC Reactor, 10 Hz design point (Sunahara et al., 2025)"
  maturity_tier: paper-concept
  grounding_confidence: medium
  p_native_mwe: 2820
  primary_sources:
    - knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/optics-express-2025-paper.md
    - knowledge/concept_research/31-laser-icf-oec-architecture/iter-01/sources/blf-website-and-news.md
  selection_rationale: |
    The BLF portfolio contains a single published reactor concept: a 500-module CBC-OEC
    direct-drive shock ignition plant described in Sunahara et al. (2025). The design
    spans a 1–10 Hz repetition-rate range with P_grid ranging from 102 MWe to 2820 MWe
    for the same physical hardware. The 10 Hz case is selected as P_native because it is
    the paper's commercial design point (Table 2 labels it the "reactor value"), the only
    operating mode with an economically viable recirculating power fraction (f_re = 0.170),
    and the case for which the power balance and efficiency chain are fully worked out. The
    1 Hz case (102 MWe) is not a distinct design — it is the marginal lower bound of the
    same hardware, with f_re = 0.426. P_native = 2820 MWe is a single-chamber design;
    n_mod = 1000/2820 ≈ 0.35 means the 1 GWe comparison represents a proportionally
    scaled-down version of this reactor.
  alternatives_considered:
    - design: "BLF OEC Reactor, 1 Hz operating point (Sunahara et al., 2025)"
      reason_rejected: economically marginal — f_re = 0.426 at 1 Hz; not the commercial design target
      sensitivity_implication: >
        If picked instead, P_native drops substantially (102 vs 2820 MWe) → n_mod rises
        to ~9.8 → many more plants needed for 1 GWe → 1 GWe LCOE shifts sharply up from
        high fixed-cost multiplication. Represents the same capital base producing 27× less
        output. Worth probing in scenarios where 10 Hz operation proves unachievable — the
        G and rep-rate viability cliff must be explored jointly, not independently.
    - design: "BLF '~1 GWe commercial plant' (BLF website)"
      reason_rejected: not a distinct engineering design — no Table 2 parameters, geometry, or efficiency values published for an intermediate-rep-rate case
      sensitivity_implication: >
        If ~1 GWe is taken as P_native instead of the 10 Hz full-power case, P_native
        is substantially lower → n_mod rises toward ~1 → 1 GWe LCOE shifts modestly upward
        relative to the 10 Hz baseline. Worth revisiting if BLF publishes engineering
        parameters for a distinct 1 GWe commercial design with its own rep rate and
        efficiency chain.
```

## 4. Open questions

- **Target gain G = 160 is the pivotal unresolved question.** P_native = 2820 MWe is directly derived from G = 160, which the paper places "beyond the CBET-mitigated curve" of Froula et al. — an unvalidated projection. If validated gain is G = 80–120 at 5 MJ, P_native at 10 Hz drops to roughly 800–1800 MWe, changing n_mod and the LCOE comparison substantially. FLUX facility broadband direct-drive experiments at OMEGA are the proposed validation path; results there would force a revisit.

- **If BLF publishes a distinct 1 GWe commercial design** with its own engineering parameters (separate from the parametric Table 2 range), it would become the primary candidate and should displace the 10 Hz extrapolation as P_native.

- **The 1–10 Hz operating range may bifurcate into distinct program phases** — a near-term low-rep-rate pilot and a subsequent production unit — as BLF's commercialization path becomes clearer. If that happens, the near-term pilot becomes a separate candidate that may qualify under the "most-mature design" criterion even if it has lower P_native.

---

**Grounding confidence rationale (medium):** The P_native figure comes from Table 2 of a peer-reviewed paper with a complete published efficiency chain — better than a back-of-envelope estimate. However, 2820 MWe depends critically on G = 160 which is a projection beyond demonstrated direct-drive baselines with no experimental validation at multi-MJ scale, and there is no independent engineering study. This combination sits clearly at medium: the data exists and is internally consistent, but the key parameter anchoring the number is a physics projection rather than a hardware-validated value.