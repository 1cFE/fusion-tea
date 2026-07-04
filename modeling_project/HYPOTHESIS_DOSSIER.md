# Hypothesis-Evidence Dossier

**Date**: 2026-07-04 (WI-017, phase 1 — WI-015 evidence pending)
**What this is**: the record of what the 1cFE modeling pipeline has actually demonstrated, hypothesis by hypothesis. Each section states the claim, the evidence with file pointers, and an honest status. The limits are stated as prominently as the wins — this document is only useful if it is unsalesy.

The four hypotheses come from the pipeline meta-review (`.project/research/20260704-120000_pipeline-hypothesis-meta-review.md`). The evidence comes from the Pipeline De-Risk & Demonstration epic (`work/backlog/epic-pipeline-derisk-demo.md`, WI-013–016) and the completed IFE epic (WI-006–008). Running log and erratum of record: `.project/reports/epic-pipeline-derisk-demo-progress.md`.

**Known corruption note**: the meta-review quotes "8.69 $/MWh" for the IFE anchor. That figure lost a leading digit somewhere in the knowledge registry (DI-006) and propagated. The verified values are **$252.30/MWh at Hawker defaults** and **$68.69/MWh at the realistic HIF design point** (`scripts/verify_ife_lcoe.py`, re-run 2026-07-04). The erratum of record is in the epic progress report.

---

## H1 — Agentic modeling

**Claim**: AI agents driven through the `agentic-mbse` workflow (spec → design → plan → implement, with 6-level validation) can write good SysML and build useful models.

**Evidence**:

- The IFE epic (WI-006/007/008) ran the full loop end-to-end: Hawker's 14-parameter framework → library calc defs → generic plant → HIF instantiation, all parse-clean, every numeric literal cited. Artifacts: `models/library/cost_structure/ife_cost_parameters.sysml`, `models/library/analyses/ife_lcoe.sysml`, `models/designs/hif_ife/`, work items under `work/completed/`.
- The retro-capture (`work/active/WI-016_h2-blind-derivation/retro_capture_hawker.md`) reconstructed that chain three months later from artifacts alone — the citation trail survives, which is itself part of the claim.
- The agent workflow self-corrected twice in the IFE chain: a design-stage LCOE estimate of ~$66/MWh for Osiris was caught as wrong ($270/MWh) by its own verification script, and the bank-vs-beam driver-energy convention conflict was resolved by reproducing Osiris's published gain (retro-capture §2e, §5).

**Status: partially validated.** The loop runs and its output is well-formed, cited, and reconstructible. What is *not* yet shown is that the models are **correct** by any independent standard:

- **The quality oracle is weak.** Validation is parse checks plus single-point reasonableness. No expert review of any model, no comparison against a hand-built equivalent. A model that is wrong in a plausibility-preserving way passes every current check (meta-review R5).
- **SV-008 is a criteria revision, not a clean pass.** The original acceptance criterion — LCOE at Hawker *defaults* within $25–120/MWh — failed ($252.30). Validation was re-anchored to a hand-picked design point ($68.69) and the failure became a domain insight (DI-006, LCOE nonlinearity). Defensible, and it went through the user-review gate, but the matrix row's "realistic parameters" wording quietly encodes a moved goalpost (retro-capture §4).
- **The distilled knowledge layer corrupted silently.** DI-006's figures sat in `knowledge/KNOWLEDGE.md` with a leading digit dropped for four months and propagated into the meta-review and this epic's own tasking. It was caught only by re-running the verification script, not by any process check. The primary artifacts were right; the summary layer was wrong (retro-capture §5).
- The executable oracle — generated code reproducing the verified anchors — is what WI-015 adds, and it is pending (see Pending evidence).

## H2 — Agentic research loop

**Claim**: AI agents can collect key input data from first-class research (papers, dossiers, expert material) and process it into effective model behaviors and structures — derivation, not transcription.

**Evidence** — two probes, one prospective and blind, one retrospective:

**(a) Blind derivation with a held-out answer key (WI-016).** Agents derived three tokamak relations — fusion power, power balance, magnet cost — from the research corpus alone, firewalled from 1costingfe, WI-009 artifacts, and the meta-review (`derivation.md`, `process_log.md` in `work/active/WI-016_h2-blind-derivation/`). A separate unfirewalled step compared them against 1costingfe at real design points (`comparison.md`). Results:

- **Every functional form matched or beat the answer key.** P_fus derived/key ratio is a constant 0.942 across a 16-point R×B grid (identical scaling; the 6% is the quadratic-⟨σv⟩ vs Bosch-Hale temperature choice, inside the derivation's own declared 10% band). Conductor ampere-meters are bit-identical at every grid point. Power balance agrees to 0.01 MW once constants are aligned. Q_p identical (13.6).
- **The derived model captured physics the answer key lacks.** Its virial structure term reproduces ARC's structure-dominated magnet cost to −8% FOAK and reconverges on the $1030M analyst override to 4% — the number 1costingfe can only reach by manual override (comparison.md D11).
- **The comparison found two answer-key bugs** (see Findings filed upstream). Both surfaced only because a corpus-derived model was held against the code.
- **The loop caught source-extraction errors before they poisoned anchors**: a P_heat row mislabeled P_fus in the extracted markdown, and "$198/m" REBCO that the table image shows is $18/m (process_log.md rows 17–18).
- **Self-declared uncertainty was well calibrated**: everything the derivation flagged as weak is exactly where the divergences are; everything it declared solid held up.
- Adjudication count: 4 equivalent, 6 both-defensible, 2 answer-key wrong, 4 one-side-captures-what-the-other-lacks (3 derived-over-key, 1 key-over-derived).

**(b) Hawker→IFE retroactive capture** (`retro_capture_hawker.md`): the one research loop that ran before it was framed as an experiment. Paper → extraction under OCR noise → 42 correct numbers with surviving citations → a genuine derivation step (Hawker's iterative DCF converted to closed form because SysML can't loop) → cross-source unit-convention reconciliation worth ~3× on LCOE → a validation failure converted into a correct, reusable insight (DI-006).

**Status: substantially validated — one family, one probe.** The limits, stated plainly:

- **One concept family, one probe.** Three DT-tokamak relations plus a stellarator note. The answer key covers four fuels, eight-plus topologies, inverse/sizing modes, radiation physics, and a full CAS stack. The comparison is per-relation, not per-model.
- **M_n = 1.2 was consistency-closure, not sourcing.** No corpus source states blanket multiplication; the value was inferred by closing ARC's published numbers. It happens to be right, but a source with an internal arithmetic inconsistency would have poisoned the constant with no error signal.
- **Same-machine calibration.** C_prof = 1.05 was calibrated on ARC and validated on ARC; it works only through the β-form channel, where ARC's β_N already carries the profile peaking.
- **Constants don't travel.** k_st = 20 extrapolates absurdly off-anchor ($17.6B of structure at concept 20a). The derived model is trustworthy near its anchors, not globally — and nothing in the artifact would stop a downstream user from using it globally.
- **In the Hawker chain, every consequential choice was human**: framework, concept, validation approach, all approval gates. The agent operated the loop; the human aimed it. And Hawker was easy mode — the paper *is* already a parametric model.

## H3 — SysML v2 as methodology

**Claim**: the language can capture the functional and structural relationships, and encode the constraints, that a real TEA needs.

**Evidence**:

- **The reuse idiom exists and carried one full concept family**: `'Costed Component'` interface, typed CAS hierarchy with a scope enum built to receive an MFE branch, a closed-form DCF calc with 14 technology-agnostic parameters, and a viability `constraint def` asserted by the plant (`models/library/`, per the MFE epic's Context section).
- **The two load-bearing wiring constructs were validated as far as tooling allows** (WI-014, `work/active/WI-014_sysml-wiring-construct-validation/findings.md`): usage-level calc chaining (`in x = calc.result`) passes parse (identical syntax live at `hif_plant.sysml:199`) and passes codegen extraction (committed chain_spike baseline wires calc→calc channels), including calcs declared inside a part def and projected onto part-usage instances. Toy models are committed at `exploration/construct_validation/`.
- **The language forced one real derivation and absorbed it**: SysML calc defs can't loop, so Hawker's year-by-year DCF became a geometric-series closed form (WI-006 DD-3) — an expressiveness constraint handled inside the methodology, with the equivalence argument recorded.

**Status: partially validated — structural half solid, behavioral half constrained.** The limits:

- **`assert constraint` is model-documentation only today.** It parses and belongs in the model, but codegen extraction stubs constraints to an empty list; no committed computation graph contains one (WI-014 construct b). Viability must be evaluated harness-side until codegen Phase 6 lands. The idiom stands; the constraint half of it does not execute.
- **Live validation is license-gated.** The syside license expired 2026-05-25; WI-014's parse/evaluate/extract verdicts on the toy itself rest on corpus proxy (identical syntax elsewhere) and committed baselines, not on a live run. Three enumerated checks are runnable the moment the license is renewed (findings.md, "Remaining once license is renewed").
- **The validated envelope is arithmetic.** Everything proven so far is flat `Real` arithmetic — no `exp()`, no conditionals, no loops. The meta-review's point stands: if models stay inside this envelope, H3 is validated for a small arithmetic subset, and that is a toolchain finding, not a language finding.
- One rider for future plant models: a part def with no concrete part usage produces nothing under codegen — the plant must be instantiated (WI-014, construct a).

## H4 — Executable exploration

**Claim**: `sysml-codegen` + `teax` can turn the models into executable pipelines that support design-space exploration — vary inputs, observe outputs, check constraints.

**Evidence** (WI-013, `work/active/WI-013_pipeline-execution-spike/findings.md`):

- **The never-executed gap is closed.** A sysml-codegen-generated pipeline (solar_battery, 36 modules) executed end-to-end through the teax executor for the first time ever. All 11 asserted outputs match hand-computed expectations exactly (relative 1e-12); LCOE 288.675539 $/MWh, reproduced across two runs. The generated registry is byte-identical to the committed baseline modulo package name. Artifacts: `exploration/pipeline_spike/`.
- **The AI implementation pass worked and was checkable**: 15 calc-def stencils filled by mechanical translation of the SysML expressions, each line citing its `library.sysml` source; nothing needed anything beyond `+ - * /` and `**`. The 21 aggregation modules were auto-implemented by codegen with no work.

**Status: plumbing validated — the fusion demonstration is pending.** The limits:

- **This was the cheapest possible model, deliberately.** A fixture with a committed extraction snapshot, all-arithmetic bodies, and no constraints. It proves the assembled path exists; it does not prove it on fusion-tea's models.
- **Constraint predicates are not emitted — confirmed at code level.** Extraction stubs constraints to `[]`; the standalone constraint extractor and the constraint→Pydantic translator both have zero callers, and the validator template body is a TODO (findings.md, "Constraint-predicate status"). Every sweep classifies viability harness-side until Phase 6 lands.
- **The run only worked because the fixture ships an extraction snapshot.** Live extraction requires syside, and the license is expired. The IFE models have no snapshot, which is exactly why WI-015 is blocked.
- Two teax executor gaps required a harness-built workaround to complete the run (see below) — the codegen→teax contract has real seams.

---

## Findings filed upstream

Holding our own tools against real work produced concrete, filed findings — arguably the epic's second product. The register:

| # | Finding | Repo | Pointer |
|---|---------|------|---------|
| 1 | ExitPoint cannot validate primitive-typed channels (`float`, `RootModel[float]`) that codegen emits; validation hard-fails without a custom router | teax | `packages/teax-simkit/simkit/core/pipeline_validator.py:320`; WI-013 findings, teax #1 |
| 2 | `write_json_model` assumes a Pydantic model; plain-float channels crash at write time — same contract gap, second layer | teax | `simkit/io/writers.py:25`; WI-013 findings, teax #2 |
| 3 | Constraint predicate generation (Phase 6) is a stub: extraction returns `[]`, the constraint extractor and translator have zero callers, the validator template is a TODO | sysml-codegen | `extraction/extractor.py:106-107`, `extraction/constraint_extractor.py:39`, `templates/constraint_validator.py.jinja2:9`; WI-013 + WI-014 findings |
| 4 | Stellarator coil cost priced at YAML calibration field `b_center = 6 T`, ignoring the design point's field (9 T at concept 20a) — silent ~33% coil-cost undercount, and the explorer serves these numbers | 1costingfe | `model.py:1272-1275`, `steady_state_stellarator.yaml:29`; WI-016 comparison D13 |
| 5 | `compute_beta_N` is exactly half the standard β convention, so the Troyon and disruption gates are ~2× permissive | 1costingfe | `tokamak.py:117-126,649`; WI-016 comparison D15 |

WI-013 additionally filed five smaller codegen findings (no snapshot-input CLI path, literals rendered as `LiteralRationalEvaluation()` in stencil docs, warning noise, class-name collisions, snapshot `compilation_results` limits) — see its findings doc.

## What the MFE epic does and does not validate

The MFE cost modeling epic (`work/backlog/epic-mfe-cost-modeling.md`, WI-009–012, currently paused at WI-009) tests **H1** (a second family through the same agentic loop — replication), **H3** (the reuse/divergence claim: tokamak and stellarator differing only in the coil and current-drive subsystems, everything else inherited), and **H4** (codegen and sweep on MFE models). It does **not** test H2, and no one should claim otherwise: its formulas are transcribed from 1costingfe (the WI-009 design's explicit sourcing decision), so the epic exercises code→SysML transcription, not literature→model derivation. Whatever 1costingfe gets wrong, those models get wrong with a citation — including, until fixed, the two bugs in the register above. The H2 evidence lives in WI-016 and the Hawker capture, not in the MFE epic.

## Pending evidence

What is not in this dossier yet, and what unblocks it:

**WI-015 — IFE end-to-end demonstration** (blocked on the syside license; the IFE models have no extraction snapshot, so live extraction is required). When it runs, it adds:

- The **executable correctness oracle H1 currently lacks**: generated IFE code reproducing the verified anchors — $252.30/MWh at Hawker defaults, $68.69/MWh at the realistic HIF point, $270/MWh for Osiris (SV-013) — within a stated tolerance.
- The **H4 fusion demonstration**: a viability sweep over Hawker parameters with the ηG > 10 constraint (DI-001) classifying the grid and the feasible region visualized — the SIMULATE box of the pipeline vision, on a real model.

**License-gated live checks** (runnable the day the syside key is renewed; enumerated in WI-014 findings):

1. `syside check` on the construct-validation toys (Level 1 on the toy itself, not by corpus proxy).
2. syside evaluation of the toy plant (`demo_plant.total_cost` = 3000.0; whether an asserted constraint evaluates to a boolean).
3. Codegen generation over the toy — confirm the calc chain enters the graph live (and the constraint, predictably, does not).

**Also unscheduled but named**: authoring WI-016's derived relations as SysML calc defs with SV entries (gated on the license and a user call on the library quality bar — `comparison.md` has the recommendation inputs), and the two vision claims with no implementation path — uncertainty propagation and inverse solving — now framed as draft epics (`work/backlog/epic-uncertainty-propagation.md`, `work/backlog/epic-inverse-solving.md`).

---

**Last Updated**: 2026-07-04 — updates when WI-015 lands (phase 2 of WI-017).
