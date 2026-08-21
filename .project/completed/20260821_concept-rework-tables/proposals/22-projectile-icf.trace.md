# Design Point Reasoning Trace — 22-projectile-icf

## 1. Sources walked

- `knowledge/concept_research/22-projectile-icf/dossier.md` — synthesized concept summary; established that First Light Fusion is the only meaningful pursuer of pure projectile ICF, that the company pivoted away from projectile-driven fusion to FLARE (pulsed-power liner implosion with fast ignition) in September 2025, and that NearStar's MTIF is a separate (MIF) concept
- `knowledge/concept_research/22-projectile-icf/iter-01/sources/first-light-fusion-technology.md` — First Light corporate technology page; high-level mission and "Z Machine validation" framing, no per-plant power numbers in the extracted text
- `knowledge/concept_research/22-projectile-icf/iter-01/sources/nearstar-fusion-technology.md` — NearStar Fusion technology page; railgun + MTIF, D-D preferred, ~10 km/s, 1 Hz; out of scope for this concept (different family per dossier)
- `knowledge/concept_research/22-projectile-icf/iter-02/sources/first-light-flare-pivot-update.md` — September 2025 FLARE pivot announcement; FLARE is explicitly the company's *post-projectile* architecture (pulsed-power amplifier + reactor concept), aspirational gain 200–1000, and the company has dropped its own plant build in favour of asset-light partnerships
- `knowledge/concept_research/22-projectile-icf/iter-02/sources/nearstar-fusion-2025-update.md` — NearStar update; confirms separate-concept status (railgun, D-D, 1 Hz)
- `knowledge/concept_research/22-projectile-icf/iter-03/sources/prnewswire-news-releases-first-light-achieves-world-first.md` — April 2022 First Light / UKAEA-validated fusion result with the projectile approach; states the **projectile pilot plant target of ~150 MWe at <$1B in the 2030s**, 30-second shot cadence, 6.5 km/s projectile velocity achieved on Machine 3, peer-reviewed LCOE analysis suggesting <$50/MWh — this is the only First Light source explicitly attaching an electric power figure to the *projectile* architecture
- `knowledge/concept_research/22-projectile-icf/iter-03/sources/theengineer-content-news-first-light-fusion-claims-tritium.md` — February 2026 tritium-breeding announcement; gives a 333 MWe figure but **explicitly tied to the FLARE design point**, not the projectile plant
- `knowledge/concept_research/22-projectile-icf/iter-03/sources/ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19.md` — IP Group portfolio announcement of the FLARE white paper; references "400 MW reactors" as the FLARE commercial-scale target (again post-pivot, not projectile)
- `knowledge/concept_research/22-projectile-icf/iter-03/sources/osti-servlets-purl-6360934.md` — older OSTI projectile-fusion reference document (background physics); no specific commercial plant design point
- `knowledge/concept_research/22-projectile-icf/iter-03/sources/osti-servlets-purl-6780071.md` — older OSTI projectile-fusion reference document; same role
- `knowledge/concept_research/22-projectile-icf/iter-03/sources/pmc-articles-pmc7658748.md` — projectile-fusion physics background article; no commercial plant design point

## 2. Candidates surfaced

**First Light 150 MWe projectile pilot plant (2022 / pre-pivot)**
First Light's stated pilot plant for the *projectile* approach: ~150 MW electric, target capital cost under $1B, online "in the 2030s," 30-second shot cadence ("In a power plant the process would be repeated every 30 seconds"). Driver basis is the Machine 3 two-stage hyper-velocity gas gun (6.5 km/s projectile demonstrated, with the target amplifying fuel velocity to >70 km/s on impact). Peer-reviewed LCOE analysis claims <$50/MWh at this scale. Liquid lithium blanket / steam Rankine balance-of-plant per the company's power plant description. Maturity tier: paper-concept (engineering whitepaper-level, no hardware built at plant scale; Machine 4 — the would-be commercial-scale driver — was cancelled February 2025). Fuel: D-T. This is the **only** First Light design point whose stated electric power is attached to the *projectile* architecture.

**First Light 500 MWe commercial plant (pre-pivot, dossier-only reference)**
The dossier mentions a ~500 MWe commercial plant figure with a 10-second shot cadence as an older First Light long-term target. The underlying source files in the research directory do not contain an explicit 500 MWe + projectile-architecture statement at the same level of grounding as the 150 MWe pilot — the figure appears as company-internal scaling commentary referenced through the dossier rather than as a self-contained, citable design point file in the source tree. Maturity tier: paper-concept aspiration. Plant-stitching risk: high (the 500 MWe figure is a scaled aspiration of the same projectile architecture, with no separate published geometry or thermal cycle).

**First Light FLARE 333 MWe / 400 MWe (post-pivot, September 2025)**
After the September 2025 pivot, First Light's reactor concept is FLARE — pulsed-power-driven amplifier targets with fast ignition, **not** a projectile-driven scheme. The TUV SUD-validated TBR-1.8 work cites a "333 MWe design point," and the IP Group / FLARE white-paper announcement references "400 MW reactors." These are the company's current published power figures, but they belong to an explicitly non-projectile architecture and would mis-attribute FLARE economics to projectile ICF. **Disqualified by concept scope**: FLARE is not projectile-driven.

**NearStar Fusion MTIF railgun plant (no published P_native)**
Plasma-armature railgun, 50 g projectiles at 10 km/s, >1 MJ per shot, ~1 Hz, D-D preferred, molten lead first wall, no specified thermal cycle, no published electric power figure for a named plant. Architecturally MTIF (magnetized fuel) — the dossier flags it as arguably belonging in a separate MIF concept row, not under pure projectile ICF. **Disqualified by concept scope** (and would lack a P_native even if in scope).

## 3. Selection

The First Light **150 MWe projectile pilot plant** (2022 pre-pivot target) is selected. It is the only candidate whose stated electric power is genuinely attached to the *projectile* ICF architecture in a primary source: the April 2022 PR Newswire release explicitly states "First Light is working towards a pilot plant producing ~150 MW of electricity and costing less than $1 billion in the 2030s," together with the projectile-architecture details (Machine 3 / 6.5 km/s driver basis, 30-second shot cadence, target-design IP). The FLARE 333/400 MWe figures are disqualified because FLARE is the post-September-2025 *non-projectile* pivot architecture (pulsed-power amplifier + fast ignition) — adopting FLARE's power as the projectile ICF design point would be exactly the plant-stitching the rules forbid (geometry from architecture A, power from architecture B). The 500 MWe long-term commercial figure surfaced in the dossier is rejected as both more aspirational and less independently grounded in the source tree than the 150 MWe pilot. NearStar is excluded as a different concept (MTIF / MIF). Grounding confidence is **low**: the 150 MWe figure is a forward-looking company headline tied to a 2030s pilot plant whose target gain had not been demonstrated, whose commercial-scale driver (Machine 4) was subsequently cancelled, and which the company has now formally walked away from in favour of FLARE — there is no engineering whitepaper specifying geometry, thermal cycle efficiency, or per-shot energy balance for the plant at the level of e.g. the 2015 ARC paper. The row exists to keep projectile ICF in the comparison with the user warned by the asterisk.

```yaml
proposal:
  concept_id: 22-projectile-icf
  design_name: "First Light projectile pilot plant (2022 pre-pivot ~150 MWe target)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 150
  primary_sources:
    - knowledge/concept_research/22-projectile-icf/iter-03/sources/prnewswire-news-releases-first-light-achieves-world-first.md
    - knowledge/concept_research/22-projectile-icf/iter-01/sources/first-light-fusion-technology.md
  selection_rationale: |
    First Light's pre-pivot projectile pilot plant — ~150 MWe, <$1B, 2030s, with a
    30-second shot cadence and the Machine 3 hyper-velocity gas gun (6.5 km/s, target
    amplification to >70 km/s) as driver basis — is the only design point in any
    primary source that attaches an electric power figure to the *projectile* ICF
    architecture. The 333 MWe / 400 MWe figures from First Light's 2025–2026
    communications belong to FLARE, the post-September-2025 pulsed-power-amplifier
    architecture that explicitly replaces the projectile approach, and so cannot be
    adopted as projectile ICF's design point without plant-stitching. The plant is
    a single-chamber single-shot architecture, so P_native is the plant value, not a
    per-module decomposition. Grounding is honestly `low`: the 150 MWe figure is a
    company headline target rather than a documented engineering design point, and
    the company itself walked away from the architecture in 2025.
  alternatives_considered:
    - design: "First Light 500 MWe commercial plant (pre-pivot long-term target)"
      reason_rejected: aspirational scaling target referenced via the dossier without a self-contained primary-source design-point file; less grounded than the 150 MWe pilot
      sensitivity_implication: >
        If picked instead, P_native would be substantially higher (500 vs 150 MWe) →
        many fewer modules at 1 GWe → 1 GWe LCOE shifts down. Worth probing only if a
        primary source documenting projectile-architecture geometry at the 500 MWe
        scale surfaces, which is unlikely now that First Light has abandoned the
        projectile architecture.
    - design: "First Light FLARE 333 MWe design point (post-pivot, TBR-1.8 context)"
      reason_rejected: FLARE is a pulsed-power-amplifier / fast-ignition architecture, not projectile-driven; outside the concept scope
      sensitivity_implication: >
        If projectile ICF were redefined to follow First Light's portfolio into FLARE,
        P_native would rise (333 vs 150 MWe) → fewer modules at 1 GWe → 1 GWe LCOE
        shifts down. Worth probing only if upstream taxonomy reclassifies FLARE as
        within the projectile-ICF family, which the dossier explicitly argues against.
    - design: "First Light FLARE 400 MWe reactor (post-pivot commercial target)"
      reason_rejected: same architectural mismatch as the 333 MWe FLARE figure; FLARE is non-projectile
      sensitivity_implication: >
        If projectile ICF were redefined to include FLARE, P_native would rise further
        (400 vs 150 MWe) → fewer modules at 1 GWe → 1 GWe LCOE shifts down further.
        Same gating condition as the 333 MWe FLARE alternative.
    - design: "NearStar MTIF railgun plant"
      reason_rejected: architecturally MTIF (magnetized fuel), D-D preferred, and no published P_native; dossier recommends a separate MIF concept row
      sensitivity_implication: >
        n/a for projectile-ICF row — NearStar has no published P_native to compare
        against, and its inclusion is a taxonomy question (separate concept row), not
        a within-concept sensitivity.
```

## 4. Open questions

- **Whether projectile ICF should remain a populated row at all**: First Light has abandoned the projectile architecture in favour of FLARE, and no other company is meaningfully pursuing pure projectile ICF at plant scale. If the upstream taxonomy concludes that the architecture has no active commercial pursuer and should be routed to freeform or retired, this whole selection becomes moot. Watch the taxonomy review.
- **NearStar reclassification**: If upstream taxonomy moves NearStar into a separate MIF row (as the dossier recommends), this row's sole basis remains First Light's pre-pivot work; if NearStar is *kept* in this row, a separate D-D MTIF design point at ~1 Hz would surface and likely dominate the row's downstream economics.
- **Hypothetical updated First Light projectile whitepaper**: If a detailed engineering whitepaper for the 150 MWe (or 500 MWe) projectile pilot/commercial plant were ever released — geometry, target manufacturing economics, thermal cycle — the grounding could move from `low` to `medium` without changing P_native. This is unlikely given the pivot but would be the cleanest path to re-grounding without re-selection.
- **Machine 4 cancellation implications**: Machine 4 (the would-be 60 km/s, 100 MJ commercial-scale driver, cancelled February 2025) was the engineering bridge from Machine 3 to the 150 MWe pilot. With Machine 4 cancelled, the 150 MWe pilot has no current driver-development path, which is the strongest single reason the grounding is `low` rather than `medium`. If a successor driver program is ever announced, revisit.
