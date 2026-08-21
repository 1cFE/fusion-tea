# Brief — research stage — Item 1 (anchor acceptance spec), STELLARATOR-DEMO epic

## Work item

Item 1 of `.project/backlog/epic_stellarator_mbse_demo.md`: write the pass/fail bars for the demo's two validation anchors. This research stage consolidates the evidence a spec stage will use to **propose** tolerance numbers (Anchor A) and per-axis expectations (Anchor B). The owner ratifies the numbers at the end ([OWNER] reserved gate, 2026-07-18) — your job is the evidence base, not the final ruling.

Governing frame: `.project/concepts/stellarator-mbse-demo.md` (criteria 3 and 4). Required reading before anything else: `knowledge/holdout/aries-cs/PROTOCOL.md` — §3 barred paths are absolute for this session (see Constraints).

## What to research

**Topic: what evidence exists in this repo to ground (a) Anchor-A handshake tolerances and (b) Anchor-B hold-out expectations, and what does it support?**

### Anchor A (1costingFE handshake) — consolidate the measured-parity record

1. **Measured agreement levels across the WI-019–025 run.** Known data points to verify and complete from the records: formula-isolation parity ~1e-8 (magnet 5.4e-10, worst −7.63e-08 at WI-021); power channels ≤6.3e-8 (SV-025, described as the float32 floor); 12 power-scaled accounts ≤1e-7 end-to-end (SV-026); pipeline-vs-oracle bit-exact at rel 1e-9. Sources: `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`, `work/completed/2026*_WI-019*` through `WI-025*` (specs/plans/audits), `work/orchestration/stale-basis-recompute.md` (§inherited bars).
2. **The float32 finding** (WI-025 design record): 1costingFE cost layers run jax float32 at runtime; the f64 comparison path used their code with x64 enabled. This bounds any realistic per-account tolerance — pin down exactly what was measured and where.
3. **Parameter-mapping traps** — the known list (WI-018 record; concept Open Question 1): `r_coil`, `sigma_v`, radiation-model `B` = 5 T vs coil-cost `b_center` = 6 T, `geom__f_shape` injection (WI-020), `rb__*` vs `geom__*` separation (WI-021), the injection-map/om_direct identity path (WI-025). The spec needs a complete trap inventory so the tolerance spec can require each mapping to be asserted, not hoped.
4. **The injected-value inventory**: exactly which account scopes the current handshake fills by injecting 1cfe's own values (the −31% structural gap: CAS22 tail, CAS40/50/60, LCOE construction). List them account-by-account from the handshake report. This defines the boundary between "must come under tolerance after Items 3–4" and "itemized-and-explained remainder" under the [OWNER] criterion-3 ruling (2026-07-18: explain remaining discrepancies; close anything shown to be an error; full gap closure not required).
5. **Version discipline**: confirm the 1costingFE pin currently in the records (`0254385` appears throughout) and where/how the handshake records the commit it ran against.

### Anchor B (ARIES-CS hold-out) — what can ground blind expectations

6. **The concept's axes** (criterion 4): structural similarity, derived-quantity agreement at their design point (radial-build consequences, coil mass, power flows), rough per-component costs. Also the C220107 exclusion rule (PROTOCOL §3 admissible list) and criterion 8's stretch scope (sizing axis lives there, not in criterion 4).
7. **Our own model's sensitivity record** — how much did headline quantities move under the WI-019–025 corrections (power balance, geometry, radial build, B field, parasitic power, account recompute)? These re-baselines (e.g. LCOE $251 → $189 → $247 → $176 → $201 → $204) are admissible, model-side evidence of our own uncertainty scale — useful for reasoning about what agreement is even achievable blind.
8. **Admissible external calibration for expectation-setting**: general cost-estimating accuracy classes (e.g. AACE estimate classes for concept-stage estimates) or equivalent general TEA accuracy conventions — as *general* knowledge, NOT anything ARIES-CS-specific. If the repo has admissible sources on conceptual-design cost accuracy (check `knowledge/SOURCE_INDEX.md`), cite them; otherwise note general-knowledge basis explicitly.

## Constraints (absolute)

- **Barred paths — do not read** (PROTOCOL §3): `knowledge/holdout/aries-cs/*.pdf`; `exploration/concept_analysis/analyses/09-qi-stellarator-hts/**`; the two ARIES-CS OSTI stubs and `helios-stellarator-comparison.md` under `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/`; `knowledge/sources/overview_of_the_helios_design_a_practical_planar_coil/**`; `knowledge/concept_research/36-helical-coil-stellarator/iter-02/sources/academia-144327326*`; `knowledge/sources/aries_cost_account_documentation/**`; `knowledge/sources/tea_dt_mfe_cost_analysis/**`. Reading PROTOCOL.md itself is required and fine.
- **Prior-leak bar for Anchor B**: no reasoning of the form "ARIES-CS is probably around X". Every expectation-grounding fact must come from the model side, the concept, or general (non-ARIES-CS) estimating knowledge, with its basis written down.
- Python via `uv run` only, if you run anything.

## Output

Save via the research command's convention to `.project/research/` (topic: anchor acceptance evidence for the stellarator demo). Structure the findings as: (A) measured-parity table with sources; (B) float32/tolerance-floor evidence; (C) mapping-trap inventory; (D) injected-value inventory (the gap boundary); (E) model-side sensitivity record; (F) admissible expectation-calibration bases; (G) gaps/unknowns the spec stage must flag rather than paper over. Cite file paths for every claim.

## Provenance key for what's settled

- [OWNER] criterion-3 bar (2026-07-18): explain remaining discrepancies; close errors; full closure not required.
- [OWNER] both anchors' numbers are proposed by the pipeline, ratified by the owner at the end.
- [OWNER] reveal is owner-triggered (PROTOCOL §6); expectations are committed pre-reveal.
- [AGENT] the research-topic decomposition above is the orchestrator's; if the records contradict any listed "known data point," report the contradiction — do not force agreement.
