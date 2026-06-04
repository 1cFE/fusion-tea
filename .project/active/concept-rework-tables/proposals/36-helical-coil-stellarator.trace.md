# Design Point Reasoning Trace — 36-helical-coil-stellarator

## 1. Sources walked

- `knowledge/concept_research/36-helical-coil-stellarator/dossier.md` — synthesized summary of Helical Fusion's HESTIA concept; used for orientation and cross-checking source relevance
- `knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/aip-2023-paper-abstract.md` — Miyazawa & Goto (2023), *Phys. Plasmas* 30, 050601; primary reactor design paper with full Table I parameters including P_net, geometry, cost, and operating phases for HESTIA-Primary, HESTIA, and the FOAK plant
- `knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/helical-fusion-technology-overview.md` — compiled overview of Helical Fusion's company and HESTIA design; cross-checks 50 MWe class claim, roadmap naming (HARUKA → KANATA), and subsystem list
- `knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/helical-fusion-2025-2026-updates.md` — updates through December 2025; confirms Helix HARUKA / Helix KANATA roadmap and sCO₂ evidence; no new design points
- `knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/nifs-ffhr-blanket-heritage.md` — NIFS FFHR heritage summary; confirms HESTIA is the Helical Fusion commercial evolution of the FFHR line; no new candidate designs
- `knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/arxiv-2512-08027/output.md` — Swanson et al. (2024), Thea Energy Helios preconceptual design; opened as context for stellarator design space comparison; this is a *different company* (planar coil stellarator, not helical coil) and is not a candidate for concept 36
- `exploration/concept_analysis/analyses/36-helical-coil-stellarator/analysis.md` — prior analysis output; read only for source orientation; not used as authority for parameter values

## 2. Candidates surfaced

**Candidate A — HESTIA (Fusion Pilot Plant)**

From Miyazawa & Goto (2023) Table I, "HESTIA (FPP)" column. Computed using the HELICOSOPE systems code and TASK/3D integrated transport code. The paper designates HESTIA as the company's Fusion Pilot Plant (FPP) — the first reactor to demonstrate net electricity generation. Parameters: major radius R₀ = 7.8 m, helical coil minor radius a_c = 1.87 m, field at coil center B_c = 8.0 T (~9 T at plasma center), P_net = 70.4 MWe, P_gross = 139 MW, Q_eng = 2.0, C_direct = $5B (1990s prices), fusion power P_fus = 250 MW, Q (plasma) = ~13, availability target >80–85%. Fuel: DT confirmed. Maturity: paper-concept with full journal publication. The abstract and company materials describe HESTIA as "50 MWe class" (a design bucket), but the section II body states "maximum net electrical output is 70 MWe" and Table I computes P_net = 70.4 MW as the reference parameter. Section V confirms "demonstrate 70 MWe of net electricity generation." Section III also says "a net electricity generation of 50 MW at the maximum" — this appears to be a more conservative demonstration commitment (minimum threshold to be demonstrated) rather than the computed design maximum; the Table I value of 70.4 MWe is the authoritative systems-code result.

**Candidate B — SOARHER (alternative FPP)**

Briefly described in Miyazawa & Goto (2023) §I as the second candidate for the FPP role alongside HESTIA. Same device size (twice LHD), same field (~5 T), same nominal output: "maximum electrical output of 50 MWe." Uses conventional NI STARS conductor (not WISE) and molten-salt or ceramic-pebble blanket (not liquid metal). No Table I equivalent, no detailed engineering parameters, no cost estimate. Only a conceptual-level description exists in the paper. P_native implied: 50 MWe (stated, not computed). Fuel: DT.

**Candidate C — FOAK commercial plant (after HESTIA)**

Also in Table I, rightmost column. P_net = 103 MW, B_c = 6.8 T. The paper's Section III forecasts the FOAK plant as available "late 2030s to early 2040s." However, the Table I entry for FOAK has multiple "—" entries, including for R_c (major radius) — the geometry is partially unspecified. C_direct is also "—" (not given). This design exists at a higher aspirational maturity than SOARHER but with less complete published specification than HESTIA itself. The company's stated goal is a 100 MWe class commercial plant.

**Candidate D — HESTIA-Primary (prototype)**

Also in Table I. R₀ = 2.73 m, roughly 1/3 the size of HESTIA. Operated in non-nuclear (hydrogen-only) mode. P_net = 0 by design — no electrical output and no DT fusion reaction. Explicitly excluded by the selection rule.

## 3. Selection

HESTIA (FPP) is the selection. It is the most-mature design in Helical Fusion's published portfolio with the best quantitative data: the only design with a full computed parameter set (Table I), confirmed geometry, computed P_net, cost estimate, and fuel cycle documented in a peer-reviewed journal paper. HESTIA-Primary has no electrical output. SOARHER has only a stated nominal power with no engineering parameters. The FOAK commercial plant has incomplete geometry in the publication. Among designs with a P_native, HESTIA has uniquely strong documentation.

The design name is specified precisely as the FPP operating configuration from Miyazawa & Goto (2023): P_net = 70.4 MWe is the computed value from HELICOSOPE, not the rounded "50 MWe class" headline. This is a single-plant architecture (not multi-module), so P_native equals the plant net output.

```yaml
proposal:
  concept_id: 36-helical-coil-stellarator
  design_name: "HESTIA Fusion Pilot Plant — reference operating case (Miyazawa & Goto, Phys. Plasmas 2023)"
  maturity_tier: paper-concept
  grounding_confidence: high
  p_native_mwe: 70.4
  primary_sources:
    - knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/aip-2023-paper-abstract.md
    - knowledge/concept_research/36-helical-coil-stellarator/iter-01/sources/helical-fusion-technology-overview.md
  selection_rationale: |
    HESTIA (the Helical Fusion Pilot Plant) is the only design in the company's public portfolio with a
    fully computed parameter set: Table I of Miyazawa & Goto (2023) gives P_net = 70.4 MWe via the
    HELICOSOPE systems code, along with geometry (R₀ = 7.8 m, a_c = 1.87 m, B_c = 8.0 T), engineering
    gain (Q_eng = 2.0), cost estimate ($5B, 1990s prices), and fuel (DT with liquid metal TBR blanket).
    The "50 MWe class" headline in the abstract is the design bracket; 70.4 MWe is the computed design
    value, confirmed by the body text ("maximum net electrical output is 70 MWe") and the Section V
    summary ("demonstrate 70 MWe of net electricity generation"). The FOAK commercial plant in Table I
    has P_net = 103 MW but incomplete geometry (major radius "—"), making HESTIA the better-grounded
    single-plant selection. This is a single-unit architecture; P_native is the plant net output, not a
    per-module value.
  alternatives_considered:
    - design: "SOARHER (alternative FPP candidate)"
      reason_rejected: "no Table I entry; only a stated nominal 50 MWe output with no computed parameters, no geometry, no cost estimate"
      sensitivity_implication: >
        If picked instead, P_native would be lower (50 vs 70.4 MWe) → more modules at 1 GWe → 1 GWe
        LCOE shifts up. SOARHER's more conservative technology stack (NI STARS conductor, molten-salt
        blanket) may reduce execution risk but the design is too underdocumented to ground a cost
        projection; revisit only if Helical Fusion publishes a SOARHER parameter set.
    - design: "FOAK commercial plant (Table I, Miyazawa & Goto 2023)"
      reason_rejected: "incomplete geometry in the publication (major radius '—', cost '—'); HESTIA is the more completely specified design"
      sensitivity_implication: >
        If picked instead, P_native rises substantially (103 vs 70.4 MWe) → fewer modules at 1 GWe →
        1 GWe LCOE shifts down. Worth revisiting if Helical Fusion publishes engineering parameters for
        the FOAK plant following HESTIA operation.
    - design: "HESTIA-Primary (prototype, Table I)"
      reason_rejected: "non-nuclear hydrogen-only device; no electrical output by design (P_net = 0)"
      sensitivity_implication: "n/a — no P_native; cannot serve as a design point under any scenario"
```

## 4. Open questions

- **P_net consistency in the paper**: Table I and Section II agree on 70.4 MWe, but Section III states "net electricity generation of 50 MW at the maximum." If a future reading of the full paper text behind the paywall resolves this as a distinct lower-bound demonstration commitment versus the design maximum, the design point would remain 70.4 MWe; if 50 MWe turns out to be an independent operating case with different plasma parameters, a case-specific selection would need to be revisited.

- **SOARHER parameter publication**: Helical Fusion described SOARHER as a parallel FPP candidate in 2023. If the company publishes a full SOARHER parameter set, it becomes a legitimate alternative design point at a nominally lower P_native (~50 MWe), with sensitivity implications described above.

- **FOAK geometry publication**: Table I gives the FOAK plant P_net = 103 MWe but leaves the major radius unspecified. If the company publishes FOAK engineering parameters after HESTIA operation, this becomes the natural revisit candidate for the commercial design point at higher P_native.

- **Helix KANATA naming**: The 2025–2026 roadmap updates name the pilot plant "Helix KANATA" and describe it as "50 MWe class (HESTIA design basis)" — it is not clear whether KANATA is HESTIA renamed, a design update, or a differently scoped device. If KANATA represents a revision of HESTIA with different power output or geometry, the design point should be re-evaluated against any KANATA-specific parameter publication.