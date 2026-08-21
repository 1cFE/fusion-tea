# Design Point Reasoning Trace — 06-magnetic-mirror

## 1. Sources walked

- `knowledge/concept_research/06-magnetic-mirror/dossier.md` — top-level synthesized summary; oriented source inventory and confirmed pre-incorporation status
- `knowledge/concept_research/06-magnetic-mirror/iter-02/dossier.md` — most-recent iteration dossier; confirmed no plant design, no electrical output, all plasma physics
- `knowledge/concept_research/06-magnetic-mirror/iter-02/sources/arpa-e-2025-fisch-presentation-notes.md` — full extraction of the July 9, 2025 ARPA-E presentation (Day2_08_Fisch.pdf, 20 slides); the most detailed public source for CHARM; no electrical output figure anywhere
- `knowledge/concept_research/06-magnetic-mirror/iter-01/sources/princeton-arpa-e-funding-2022.md` — Princeton press release; Fisch explicitly describes the proposal as "purely theoretical"; no power target of any kind
- `knowledge/concept_research/06-magnetic-mirror/iter-01/sources/technical-papers-summary.md` — synthesized summary of 7 Fisch group papers (2006–2025); all plasma physics; no engineering parameters, no P_native

## 2. Candidates surfaced

**CHARM commercial concept (no design point)** — Pale Blue Fusion's multi-chamber centrifugal mirror for p-B11. The ARPA-E presentation (July 2025) is the most complete public source: it shows a three-chamber schematic and lists nine theoretically-addressed derisking questions, but specifies no machine size, no plasma parameters, no fusion power, and no net electrical output. The group's stated next goal is to "Develop an in silico power-positive reactor" — even a computational design point does not yet exist. Fisch's own words from 2022: "Our proposal is purely theoretical."

**CMFX (University of Maryland — separate group)** — physics demonstrator validating centrifugal mirror confinement with D-D fuel, LTS magnets (3 T / 0.3 T, mirror ratio 10, 6.7 m). No electrical output by design. Separate group with no connection to Pale Blue Fusion as a commercial entity. Does not implement CHARM's distinguishing features. Does not qualify as a design point candidate.

**Any aspirational or informal P_native target** — none. No informal commercial power projection, no "if we built this it would be ~X MWe" estimate, and no scenario calculation with a stated electrical output appears in any source. The (PB)² 0D power balance code has not published output. No number of any kind traces to any source in the portfolio.

## 3. Selection

**Operator override of LLM routing.** The LLM proposal step correctly applied the discipline rule and routed this concept to freeform: no source-traceable P_native exists in any Pale Blue Fusion material. The operator (Reid) has decided to override that routing to keep Pale Blue in the 1 GWe cost comparison rather than drop it to the freeform tail. The override authors a notional P_native of **150 MWe**, defensible by architectural analogy to other corpus entries — Realta CoSMo Hammir (DT centrifugal mirror) at 50 MWe per module, HB11 Energy (PB11 ICF) at 500 MWe — and by the general observation that modular mirror commercial designs typically pitch into the 100–300 MWe range. PB11 fuel reactivity argues for the higher end relative to a DT mirror module, while the multi-chamber centrifugal architecture argues against ICF-reactor-hall scale. 150 MWe lands in the defensible middle. The CHARM architecture (centrifugal mirror, p-B11, alpha channeling, ponderomotive end-plug barriers) is published; the P_native is explicitly not — this row is operator-authored, `grounding_confidence: low`, and `proposal_model: hand` (set at ingestion). The verification gate may accept or override the 150 MWe figure.

```yaml
proposal:
  concept_id: 06-magnetic-mirror
  design_name: "Pale Blue Fusion CHARM commercial notional plant (operator-authored, 150 MWe)"
  maturity_tier: paper-concept
  grounding_confidence: low
  p_native_mwe: 150
  primary_sources:
    - knowledge/concept_research/06-magnetic-mirror/iter-02/sources/arpa-e-2025-fisch-presentation-notes.md
    - knowledge/concept_research/06-magnetic-mirror/iter-01/sources/technical-papers-summary.md
    - knowledge/concept_research/06-magnetic-mirror/iter-01/sources/princeton-arpa-e-funding-2022.md
  selection_rationale: |
    No source-traceable P_native exists in any Pale Blue Fusion published material — not
    in the July 2025 ARPA-E presentation, not in the Princeton press release (Fisch:
    "purely theoretical"), not in any of the seven Fisch-group technical papers. The LLM
    proposal step correctly routed this concept to freeform per the discipline rule.
    The operator has overridden that routing and chosen 150 MWe as a notional P_native
    so this concept stays in the 1 GWe cost comparison. The number is defensible by
    analogy to other corpus entries: Realta's CoSMo Hammir (DT centrifugal mirror) is
    50 MWe per module; HB11 (also PB11 fuel, ICF approach) is 500 MWe; modular mirror
    architectures targeting commercial deployment typically sit in the 100–300 MWe
    range, and PB11 reactivity argues for the larger end relative to a DT mirror. The
    CHARM architecture (multi-chamber centrifugal mirror, p-B11, alpha channeling,
    ponderomotive end-plug barriers) is published; the P_native is not. This row is
    operator-authored, grounding_confidence: low, and will be asterisked in the
    comparison view.
  alternatives_considered:
    - design: "(no published Pale Blue design with a P_native)"
      reason_rejected: "No published source defines a P_native for any Pale Blue design; the LLM proposal step correctly identified this and routed to freeform. Operator override produced this row."
      sensitivity_implication: "If Pale Blue publishes any reactor concept with a stated power output, replace this notional row with a source-grounded proposal."
    - design: "CMFX (Centrifugal Mirror Fusion Experiment, University of Maryland)"
      reason_rejected: "Separate group's physics demonstrator with D-D fuel; no electrical output by design; does not implement CHARM architecture, alpha channeling, ponderomotive barriers, or p-B11 fuel."
      sensitivity_implication: "n/a — CMFX is not a Pale Blue design and cannot serve as a stand-in P_native source."
    - design: "Notional P_native in 50–100 MWe range (small-module mirror analogue, Realta Hammir-like)"
      reason_rejected: "PB11 fuel cycle requires substantially higher plasma parameters and chamber volume than DT mirrors of comparable architecture; choosing the small end of the modular-mirror range understates the natural unit size for a p-B11 centrifugal mirror."
      sensitivity_implication: "If picked instead, P_native would be lower → more modules at 1 GWe → 1 GWe LCOE shifts up. Worth probing if Pale Blue ever publishes a per-chamber sizing that lands in this range."
    - design: "Notional P_native in 300–500 MWe range (HB11-scale PB11 plant)"
      reason_rejected: "HB11's 500 MWe scenario is an ICF (laser-driven) PB11 plant with a different architectural family; magnetic centrifugal mirror modules are typically pitched smaller than ICF reactor halls. Choosing the high end overstates the natural module size for a multi-chamber mirror."
      sensitivity_implication: "If picked instead, P_native would be higher → fewer modules at 1 GWe → 1 GWe LCOE shifts down. Worth probing if Pale Blue publishes a single-chamber sizing or full-plant target at multi-hundred-MWe scale."
```

## 4. Open questions

- **Operator override of LLM routing** — first concept in the batch to require manual P_native authorship. If/when Pale Blue publishes any plant concept, replace this notional row with a source-grounded proposal.
- **If Pale Blue Fusion publishes any commercial reactor concept study** — even a rough conceptual design with a stated power output — the operator-authored notional 150 MWe should be replaced immediately with a source-grounded value.
- **If the (PB)² power balance code results are published** — the group has a 0D code framework that could yield a design-point-like calculation. Released results with a stated fusion power and efficiency would constitute an informal P_native and supersede the operator override.
- **Company incorporation and device roadmap** — Pale Blue was pre-incorporation as of July 2025. A first hardware device announcement with a design implying some net power could change the candidate inventory and the grounding tier.
- **CMFX upgrade scope** — if a successor device is built with electrical output capability, it would provide geometry anchor data; however this would not directly constitute a Pale Blue design point.
