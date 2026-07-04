# Epic Progress: Pipeline De-Risk & Demonstration

**Epic**: `work/backlog/epic-pipeline-derisk-demo.md` | **Timebox**: 2026-07-04 → 2026-07-18 | **Branch**: `epic/pipeline-derisk-demo`
**Orchestration**: main session orchestrates; subagents execute item stages; orchestrator owns git, quality gates, and this report.

## Status Board

| Item | Name | Status | Notes |
|------|------|--------|-------|
| WI-013 | Pipeline Execution Spike | **DONE** — execution closed, 11/11 assertions exact | commit df5835e6 |
| WI-014 | SysML Wiring Construct Validation | **done w/ riders** — 3 live checks pending license | verdicts via corpus proxy; see log |
| WI-015 | IFE End-to-End Demonstration | **blocked on syside license** | plumbing proven (WI-013); IFE models have no extraction snapshot, so live extraction needs syside |
| WI-016 | H2 Probe (blind derivation + differential) | **derivation done; comparison running** | firewall held (2 near-misses logged, no exposure) |
| WI-017 | Dossier & Explainer | rolling — dossier seeded | finalizes last |

**WI-009 (MFE library)**: paused per user 2026-07-04 (spec.md Status set to `paused`). Its design.md stays as-is; the WI-016 firewall excludes it.

## Log

### 2026-07-04 — Epic start
- Meta-review completed: `.project/research/20260704-120000_pipeline-hypothesis-meta-review.md` (the epic's motivating analysis)
- Epic authored and registered; items WI-013–017 added to BACKLOG.md under "Pipeline De-Risk & Demonstration" (P0)
- Item 4 reshaped per user direction: blind derivation from the full `knowledge/concept_research/` corpus + pretraining, with 1costingfe as held-out answer key
- Branch `epic/pipeline-derisk-demo` created
- Wave 1 launched (3 parallel subagents): WI-013 spike, WI-014 constructs, WI-016 derivation phase
- Firewall for WI-016 derivation: whitelist = `knowledge/concept_research/`, `knowledge/sources/`, `knowledge/SOURCE_INDEX.md`, pretraining. Excluded: 1costingfe repo, WI-009 artifacts, the meta-review, `archive/models/` (PyFECONS port), `exploration/concept_analysis/` computed values.

### 2026-07-04 — WI-016 derivation phase complete (commit 7d52f9dc)
- Three relations derived blind from corpus + declared pretraining: fusion power P_fus ∝ C_prof·β_T²·B0⁴·V with Troyon/Greenwald/kink closures; power balance with 4:1 alpha split; magnet cost = conductor ampere-meters ($18–36/m REBCO, image-verified) + virial-theorem structure term
- ARC worked example: P_fus 522 MW (published 525), P_net 189 MW (published 190), magnet ≈$5.1–5.2B FOAK reproducing ARC Table 11
- **Notable**: the blind derivation includes a *structure* cost term the conductor-only answer key lacks — the known 1costingfe undercount surfaced independently
- **Notable**: image cross-checking caught two extraction errors that would have poisoned anchors (a P_heat row mislabeled P_fus; "$198/m" REBCO actually $18/m)
- Corpus sufficiency: strong (P_fus) / good with one gap (M_n blanket multiplication — inferred by consistency) / good-form-weak-constant (structure cost)
- Comparison-phase agent launched (unfirewalled, 1costingfe as answer key)

### 2026-07-04 — WI-014 complete-with-riders (commit 2211efd8)
- **Construct (a), calc chaining `in x = calc.result`**: parse pass (identical syntax live in `hif_plant.sysml:199`), extraction pass (chain_spike baseline wires calc→calc channels). **Rider for WI-010**: the plant def needs a concrete part usage or codegen emits nothing.
- **Construct (b), part-level `assert constraint`**: extraction **FAIL** — `sysml-codegen extraction/extractor.py:106-107` stubs constraints to `[]`; `constraint_extractor.py` has zero callers. Constraints are model-documentation only today. **Consequence (already planned for)**: WI-015/WI-012 sweeps evaluate viability harness-side. Filed as the epic's first codegen finding.
- **WI-010 verdict**: idiom usable as sketched, with the two riders above.
- Toy models committed at `exploration/construct_validation/`; live parse/evaluate/extract checks enumerated in findings.md, runnable the moment the license works.

### ⚠ BLOCKER — syside license expired (user action required)
- Key expired 2026-05-25, machine file 2026-06-01; vendor server confirms subscription lapsed (Sensmetry, syside.support@sensmetry.com)
- Blocks: `syside check` (all Level-1 validation), syside Python evaluation, live codegen extraction (SysideAdapter imports syside)
- **Impact**: WI-014's 3 live checks; WI-015 (IFE demo) is **critically blocked** at its extraction step unless WI-013 finds a baseline-graph path around syside; WI-013 may partially route around via committed baselines
- Once renewed: `uv run syside-license check --license-key <KEY>`, then run the checks in WI-014 findings.md

### 2026-07-04 — WI-013 DONE: the never-executed gap is closed (commit df5835e6)
- **First-ever end-to-end run** of a sysml-codegen-generated pipeline through the teax executor: solar_battery, 36 modules, 15 AI-pass impl bodies (all mechanical translations — nothing outside the arithmetic envelope)
- **11/11 numeric assertions pass exactly** (1e-12 rel), reproduced across two runs; LCOE 288.675539 $/MWh; generated registry byte-identical to committed baseline modulo package name
- H4 evidence: the plumbing works. Remaining H4 risk concentrates in extraction-of-our-models (license-blocked) and constraint emission (confirmed Phase 6 stub — harness-side evaluation stands)
- Findings filed in `work/active/WI-013_pipeline-execution-spike/findings.md`: 2 teax exit-contract gaps (`pipeline_validator.py:320`, `writers.py:25` — generated `float` exit types the executor can't validate/write; worked around with explicit OutputRouter; must be fixed on one side), 5 codegen issues, Phase 6 constraint stub confirmed with zero-caller evidence
- **Critical-path consequence**: WI-013 worked only because the fixture ships an extraction snapshot. The IFE models have none → WI-015 waits on the syside license renewal (see blocker above)

### 2026-07-04 — WI-016 part (a): Hawker→IFE retro-capture complete — with two integrity findings
- Chain reconstructed step-by-step from artifact quotes: Hawker 2020 extraction → DI-003/005 → human framework selection → WI-006 library → WI-007 assembly → WI-008 HIF instantiation → SV-008/012–014. `work/active/WI-016_h2-blind-derivation/retro_capture_hawker.md`
- **ERRATUM (propagating data corruption caught and fixed)**: DI-006 in KNOWLEDGE.md had lost a leading "2" from every figure — real values are **$252.30/MWh** at Hawker defaults and **$68.69/MWh** at the realistic HIF point (verified by re-running `scripts/verify_ife_lcoe.py`), not "52"/"8.69". The corruption had already propagated into the meta-review, this epic's WI-015 anchor, and earlier entries in this report. KNOWLEDGE.md and the epic file corrected; **WI-015's anchor check now targets $252.30 (defaults) / $68.69 (HIF point) / $270 (Osiris, SV-013)**. Historical docs left as written; this entry is the erratum of record.
- **SV-008 caveat for the dossier**: the original criterion (defaults within Hawker's $25–120 range) *failed*; validation was re-anchored to a hand-picked design point and the failure became DI-006. Defensible, but it's a criteria revision, not a clean pass — the dossier must say so.
- Strongest autonomous H2 evidence in the chain: the bank-vs-beam driver-energy convention conflict caught by reproducing Osiris's published gain (~3× LCOE error averted), and the closed-form DCF derivation replacing Hawker's iterative formula (SysML can't loop).

## Quality Gates (orchestrator-enforced before any item closes)

1. Item has spec.md in `work/active/WI-XXX_*/` (light is fine; scope + success criteria + firewall/protocol where applicable)
2. All `.sysml` deliverables pass `uv run syside check` (Level 1) minimum; Levels 2–3 where applicable
3. Numeric claims verified against stated anchors (SV-008 for WI-015; hand-computed expectations for WI-013)
4. Findings filed, not worked around: codegen/teax gaps recorded in the item's findings doc with repo pointers
5. Every item ships its written record (findings/process doc) — documentation is a deliverable
6. Git: one commit per meaningful milestone, orchestrator-authored; subagents never commit

## Decisions & Escalations

- (none yet)

## Hypothesis Evidence Tracker (feeds WI-017 dossier)

| Hypothesis | Evidence so far | Status |
|-----------|----------------|--------|
| H1 agentic modeling | IFE epic (prior); this epic adds the SV-008 oracle via WI-015 | partial |
| H2 research loop | pending WI-016 | untested → in progress |
| H3 SysML methodology | pending WI-014 (wiring constructs) | partial |
| H4 executable exploration | pending WI-013/015 | untested → in progress |
