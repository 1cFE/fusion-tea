# Brief — spec stage — Item 1 (anchor acceptance spec), STELLARATOR-DEMO epic

## Work item

Item 1 of `.project/backlog/epic_stellarator_mbse_demo.md`: write the **anchor acceptance spec** — the pass/fail bars for the demo's two validation anchors. The spec document IS the deliverable: `.project/active/demo-anchor-acceptance-spec/spec.md`. There is no design/plan/implement after it; a spec_review follows, then owner ratification.

Governing frame: `.project/concepts/stellarator-mbse-demo.md` (criteria 3, 4, and the criterion-8 stretch). Required reading, in order:
1. `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths absolute for this session
2. `.project/research/20260718-205525_anchor-acceptance-evidence-stellarator-demo.md` — the evidence base; every number you propose must trace to it (or to a record it cites)
3. `.project/backlog/epic_stellarator_mbse_demo.md` — Item 1 scope + how Items 3, 4, 7 consume this spec

## What the spec must contain

### 1. Anchor A (1costingFE handshake) — tolerance spec

- **Per-account pass bar** for formula-reproduced accounts. Research supports ~1e-6 relative (above the measured ~1e-7 float32 floor, far below percent-scale real errors). Propose a number with its basis; mark `[AGENT-PROPOSED — owner ratifies]`.
- **Do not conflate the three test tiers** (research §A): pipeline-vs-oracle (f64, rel 1e-9, already standing) is a different bar from pipeline-vs-1cfe-f32 (the per-account handshake bar). The spec states both and keeps them distinct.
- **The gap boundary, account-by-account** (research §D): which accounts Items 3–4 must bring under the per-account bar (CAS22 tail lines, CAS40/50/60 → Item 3; CAS70 levelization, CAS80 fuel, IDC treatment → Item 4), and what may remain as itemized-and-explained remainder. Word acceptance per the **[OWNER] criterion-3 ruling (2026-07-18): remaining discrepancies are itemized and explained; anything shown to be an error (model, mapping, or sourcing mistake) is closed; full structural-gap closure is not required.** Note the §D nuance: CAS21/CAS10/CAS70 are injected in the handshake but already forward-computed in the instance.
- **End-state LCOE bar**: after Items 3–4, what the end-to-end LCOE comparison must satisfy — propose a form consistent with the ruling (e.g. all modeled accounts under the per-account bar + remainder fully itemized with signed magnitudes, rather than a blanket LCOE percentage). Your call on the exact form; mark it proposed.
- **Mapping-trap discipline**: require every trap in research §C (14 entries + the rb__/geom__ separation) to be asserted in the handshake, not assumed; new traps introduced by Items 3–4 get added to the table with an assertion. The f_shape −20.6% failure is the cautionary precedent.
- **Version discipline**: the 1costingFE commit pin (`0254385`, asserted at `handshake_1costingfe.py:115`) must be recorded in every handshake report, and the spec defines the **pin-bump procedure** (research G-6: currently undocumented — write one: who decides a bump, what re-verification a bump triggers).
- **The G-8 premise conflict — surface, do not resolve** (research §G-8): the standing [OWNER] successor bar (edits to `handshake_1costingfe.py` only within `set_1cfe_inputs`'s injection map; `handshake_comparison.json` diff must be empty) collides with Items 3–4, which add modeled accounts and therefore MUST move the comparison. Propose an amendment (e.g. the bar as-is continues to govern refinement items that shouldn't move the handshake; for account-scope items it is superseded by this spec's acceptance: comparison JSON moves are expected, re-baselined per item, injection-map shrinkage documented) — but mark the whole block `[OWNER DECISION PENDING — proposed amendment, not in force]` and list it in the ratification items.

### 2. Anchor B (ARIES-CS hold-out) — pre-committed expectations

- **Band-shaped, per-axis, committed pre-reveal** (research G-1): the model's output at the ARIES-CS point does not exist yet and the reference is sealed, so expectations are band widths, not point targets.
- Axes per criterion 4: (a) **structural similarity** — propose a qualitative checklist (what structural correspondences count: subsystem decomposition, radial-build ordering, cost-account coverage); (b) **derived quantities** at their design point (radial-build consequences, coil mass, power flows) — research supports same-order-of-magnitude; (c) **rough per-component costs** — research supports factor-of-2 asymmetric-high (AACE Class 5, admissibly sourced; our own headline moved ±25–30% under corrections). Propose exact bands per axis; mark `[AGENT-PROPOSED — owner ratifies]`.
- **Exclusions**: C220107 power_supplies excluded or footnoted (the one ARIES-CS-derived 1cfe value — mandatory, research G-2; it stays included in Anchor A). The sizing axis is criterion 8's, NOT criterion 4's (research G-3) — state the exclusion, don't write a sizing expectation.
- **Pass/fail semantics**: per the concept, a miss beyond the bands fails the anchor and is reported as a demo finding — the spec says this plainly and defines what the comparison report must record per axis (band, observed value, verdict, explanation).
- **Basis discipline**: every band's written rationale draws ONLY from model-side evidence (research §E), the concept's axes, and general estimating knowledge (research §F). **No reasoning of the form "ARIES-CS is probably around X"** — this prior-leak bar goes in the spec itself as a constraint on how Item 7 argues too.
- **AACE provenance caveat** (research §F): the Class-5 table is a dossier extraction, not a registered primary source; since it is load-bearing, the spec requires Item 7 (or an earlier convenient moment) to cross-check the extracted table against the raw arXiv PDF and cite AACE 18R-97 as the standard.

### 3. Ratification package

End the spec with a **single consolidated list of every `[AGENT-PROPOSED]` number and the G-8 amendment**, formatted so the owner can ratify or adjust each line in one pass. Success criterion "Owner sign-off on both specs" is met by the owner marking this list.

## Constraints

- Barred paths (PROTOCOL §3) — same list as the research brief; do not read them. The research doc already consolidated everything needed.
- Spec format: this project's coding-PM spec conventions (Problem / Success Criteria / Known Requirements with provenance grades / Non-Goals / Open Questions). Use provenance grades per `capture-fidelity`: [OWNER] for the criterion-3 ruling and the successor bar, [AGENT-PROPOSED] for every number, [INHERITED: research §X] for evidence.
- Don't restate the research — cite it. The spec carries the bars and their one-line bases; the evidence lives in the research doc.
- Non-goals for this spec: running either comparison (Items 3/4/7); defining Item 2's constraint-execution acceptance; anything about criterion 8 beyond the sizing-axis exclusion note.

## Provenance key

- [OWNER 2026-07-18] criterion-3 bar: explain remaining discrepancies; close errors; full closure not required.
- [OWNER 2026-07-18] epic home + both anchors' numbers proposed by pipeline, ratified by owner.
- [OWNER, WI-024 close] the successor bar (G-8) — a standing rule only the owner can amend; propose, don't decide.
- [AGENT] everything graded proposed above; the research doc's §G flags are agent findings.
