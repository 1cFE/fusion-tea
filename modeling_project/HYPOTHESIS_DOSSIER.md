# Hypothesis-Evidence Dossier

**Date**: 2026-07-05 (WI-017, phase 2 — final; all five epic items landed)
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
- **The executable oracle now exists and passed bit-exactly** (WI-015, `work/active/WI-015_ife-end-to-end-demo/findings.md`): generated Python from the IFE models reproduces all three verified anchors — $252.30/MWh (Hawker defaults), $68.69/MWh (realistic HIF), $270.12/MWh (Osiris) — with relative deviation 0.0 against `scripts/verify_ife_lcoe.py` (SV-023, passing). Every generated calc body was reviewed line-by-line against its SysML expression and is faithful.

**Status: partially validated — the loop now has an execution-backed oracle, but still no independent correctness standard.** What the bit-exact anchors prove and don't:

- **They prove faithful translation of THESE models, not model correctness.** Generated code reproducing the oracle exactly means the SysML → Python chain preserves the math; the oracle itself (`verify_ife_lcoe.py`) mirrors the SysML line-for-line, so both sides descend from the same modeling decisions. No expert review of any model, no comparison against a hand-built equivalent. A model wrong in a plausibility-preserving way still passes every check (meta-review R5).
- **The validation stack does not catch "unworkable SysML."** The gap audit (`.project/research/20260705-120000_validation-stack-gap-audit.md`) found that none of the traps this epic surfaced — self-named binding recursion, `return`-style calc outputs, silently dropped constraints, uninstantiated part defs — is caught by the 6-level stack today. They surfaced only because WI-013/014/015 *executed* the pipeline for the first time. The rules exist as prose in `work/learnings/RAW_LEARNINGS.md`; the recommended per-level checks are filed as an agentic-mbse backlog item, and the sysml-conventions skill stencil actively teaches the broken `return` pattern until fixed.
- **SV-008 is a criteria revision, not a clean pass.** The original acceptance criterion — LCOE at Hawker *defaults* within $25–120/MWh — failed ($252.30). Validation was re-anchored to a hand-picked design point ($68.69) and the failure became a domain insight (DI-006, LCOE nonlinearity). Defensible, and it went through the user-review gate, but the matrix row's "realistic parameters" wording quietly encodes a moved goalpost (retro-capture §4).
- **The distilled knowledge layer corrupted silently.** DI-006's figures sat in `knowledge/KNOWLEDGE.md` with a leading digit dropped for four months and propagated into the meta-review and this epic's own tasking. It was caught only by re-running the verification script, not by any process check. The primary artifacts were right; the summary layer was wrong (retro-capture §5).

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
- **The two load-bearing wiring constructs are now live-validated** (WI-014, `work/active/WI-014_sysml-wiring-construct-validation/findings.md`; license renewed 2026-07-05, all three deferred checks run): usage-level calc chaining (`in x = calc.result`) passes parse live, **evaluates end-to-end under syside** (`demo_plant.total_cost` = 3000.0), and **survives codegen extraction into the pipeline graph** — including calcs declared inside a part def and projected onto part-usage instances. The asserted constraint's predicate also evaluates live (True), via a two-step API (evaluate the def's predicate expression with the assert usage as scope). Toy models at `exploration/construct_validation/`.
- **The whole model set survived translation to executable code with zero manual work** (WI-015): everything in the IFE models is flat arithmetic, live extraction carried the compiled expression ASTs, and codegen auto-implemented all six calc bodies faithfully. The language captured what the TEA needed, and the capture was mechanical to execute.
- **The language forced one real derivation and absorbed it**: SysML calc defs can't loop, so Hawker's year-by-year DCF became a geometric-series closed form (WI-006 DD-3) — an expressiveness constraint handled inside the methodology, with the equivalence argument recorded.

**Status: substantially validated for the arithmetic envelope — structural and behavioral halves both live-proven; the constraint half still does not execute.** The limits:

- **`assert constraint` is model-documentation only today — now live-confirmed, and the drop is silent.** WI-014's live codegen run completed with no error or warning while the constraint vanished from every generated artifact (extraction stubs constraints to `[]`; Phase 6 TODO). Viability must be evaluated harness-side until codegen Phase 6 lands — WI-015's sweep did exactly that (ηG > 10 applied in the sweep script, not in generated code). The idiom stands; the constraint half of it does not execute.
- **The executable envelope has authoring rules the language doesn't enforce.** Two syntax traps from the live checks (WI-014 findings, "Syntax deltas"; `work/learnings/RAW_LEARNINGS.md`): calc outputs must be `out attribute x : Real = expr`, not `return` — `return` is legal SysML and evaluates in syside, but codegen sees zero outputs and crashes (this bit WI-015 six times across the canonical IFE models before conversion). And calc bindings must never self-name (`in x = x;` parses but infinite-recurses at syside evaluation). Both are tooling-contract constraints, not language findings — but a model that ignores them is unworkable in practice.
- **Nothing in the validation stack enforces those rules.** The gap audit confirmed the 6-level stack catches none of the traps above; they live as prose learnings until the filed agentic-mbse checks land. Today, H3-compliant authoring depends on agents having read the learnings file.
- **The validated envelope is arithmetic.** Everything proven, including the full WI-015 chain, is flat `Real` arithmetic — no `exp()`, no conditionals, no loops. If models stay inside this envelope, H3 is validated; outside it, the AI implementation pass exists but is unexercised on these models.
- Two riders for future plant models, both live-confirmed: a part def with no concrete part usage produces nothing under codegen (the plant must be instantiated — this dropped the Meier driver calc in WI-015 until an instance was added), and a derived attribute reading a calc result (`attribute x = calc.out`) evaluates but loses its *name* at extraction — the value survives only as the raw channel.

## H4 — Executable exploration

**Claim**: `sysml-codegen` + `teax` can turn the models into executable pipelines that support design-space exploration — vary inputs, observe outputs, check constraints.

**Evidence** (WI-013 `work/active/WI-013_pipeline-execution-spike/findings.md`; WI-015 `work/active/WI-015_ife-end-to-end-demo/{findings,demo_report}.md`):

- **The never-executed gap is closed.** A sysml-codegen-generated pipeline (solar_battery, 36 modules) executed end-to-end through the teax executor for the first time ever (WI-013). All 11 asserted outputs match hand-computed expectations exactly (relative 1e-12). Artifacts: `exploration/pipeline_spike/`.
- **The fusion demonstration happened.** WI-015 ran the validated IFE/HIF models through the full assembled path — live syside extraction (first since the license lapse, first ever of these models) → sysml-codegen generation → teax execution — and all three LCOE anchors reproduce bit-exactly: $252.30/MWh (Hawker defaults), $68.69/MWh (realistic HIF), $270.12/MWh (Osiris). SV-023 registered, passing. Artifacts: `exploration/ife_e2e/`.
- **Design-space exploration is demonstrated, not hypothetical**: an 11,505-point sweep over driver efficiency × target gain × rep rate, generated module implementations called in-process, 0.1 s total. The map shows real physics — the ηG = 10 viability knee (DI-001) emerges from generated code as a sharp LCOE cliff, with 75.8% of the grid viable and 64.5% attractive (≤$100/MWh). Figures: `data/ife_sweep/`.
- **The AI implementation pass had zero work to do on the IFE models** — live extraction carries compiled expression ASTs, so codegen auto-implemented all six bodies, each reviewed against the SysML and faithful. (WI-013's snapshot-driven run needed 15 hand-filled stencils; live extraction is strictly better.)

**Status: demonstrated on a real fusion model.** The limits, stated plainly:

- **Constraint predicates are still not emitted** (Phase 6 stub, confirmed three times: WI-013 code-level, WI-014 live, WI-015 on the real model). The `assert constraint viability` in `ife_plant.sysml` appears nowhere in the generated package. Every sweep classifies viability harness-side; the constraint in the model is documentation of intent, and the harness re-implements it.
- **Cross-part wiring is manual glue.** Bindings that cross part boundaries (`driver.cost_per_joule = meier_cost.gamma`, all the subsystem-attribute inputs to the LCOE calc) drop to unresolved entry points: no channel wiring, no literal pre-fill. The harness closes the γ → LCOE loop by feeding run-A outputs into run C's inputs (WI-015 finding 4). Numbers flow through generated code end to end, but one edge of the plumbing is hand-built — the single biggest gap for plant-idiom models, flagged for WI-010/WI-012.
- **Getting through extraction required three model fixes** (all trivially safe, all Level-1 verified: six `return` → `out attribute` conversions, one output promotion, one added part instance) and a name-sanitizing post-processor because quoted SysML names generate invalid Python. The path is proven, not smooth.
- **Bit-exact is a property of this envelope.** The models are flat floating-point arithmetic and the generated bodies came from compiled ASTs, so exactness is expected, not miraculous. Models needing `exp()`, conditionals, or hand-translated bodies would re-open the translation-fidelity question the anchors currently close.
- The two teax executor gaps from WI-013 (primitive-channel handling) are unchanged; WI-015 reused the workaround verbatim.

---

## Findings filed upstream

Holding our own tools against real work produced concrete, filed findings — arguably the epic's second product. The register:

| # | Finding | Repo | Pointer |
|---|---------|------|---------|
| 1 | ExitPoint cannot validate primitive-typed channels (`float`, `RootModel[float]`) that codegen emits; validation hard-fails without a custom router | teax | `packages/teax-simkit/simkit/core/pipeline_validator.py:320`; WI-013 findings, teax #1 |
| 2 | `write_json_model` assumes a Pydantic model; plain-float channels crash at write time — same contract gap, second layer | teax | `simkit/io/writers.py:25`; WI-013 findings, teax #2 |
| 3 | Constraint predicate generation (Phase 6) is a stub: extraction returns `[]`, the constraint extractor and translator have zero callers, the validator template is a TODO — live-confirmed silent drop (no error, no warning) | sysml-codegen | `extraction/extractor.py:106-107`, `extraction/constraint_extractor.py:39`, `templates/constraint_validator.py.jinja2:9`; WI-013 + WI-014 (live) + WI-015 findings |
| 4 | Stellarator coil cost priced at YAML calibration field `b_center = 6 T`, ignoring the design point's field (9 T at concept 20a) — silent ~33% coil-cost undercount, and the explorer serves these numbers | 1costingfe | `model.py:1272-1275`, `steady_state_stellarator.yaml:29`; WI-016 comparison D13 |
| 5 | `compute_beta_N` is exactly half the standard β convention, so the Troyon and disruption gates are ~2× permissive | 1costingfe | `tokamak.py:117-126,649`; WI-016 comparison D15 |
| 6 | `return`-style calc outputs are invisible to extraction (`ReferenceUsage` with direction Out; only `AttributeUsage` inspected) → zero outputs → template crash. Legal SysML, evaluates in syside, kills codegen | sysml-codegen | `extraction/extractor.py:152-153`, `templates/teax_module.py.jinja2:118`; WI-015 finding 1, independently hit by WI-014 live check 3 |
| 7 | Part-usage index keys each usage under its *first* type (supertype-first for redefinitions), so `part :>> driver : 'HIF Driver'` leaves 'HIF Driver' looking uninstantiated and its calcs are dropped | sysml-codegen | `extraction/usage_extractor.py:160-167`; WI-015 finding 2 |
| 8 | Quoted SysML names ('IFE LCOE') leak raw into Python file names, imports, and class names — generated package is not valid Python and is internally inconsistent with the registry's sanitized names | sysml-codegen | WI-015 finding 3; deterministic workaround at `exploration/ife_e2e/sanitize_names.py` |
| 9 | Cross-part references drop to unresolved entry points: no channel wiring between parts, no literal pre-fill of inputs — plant-idiom models generate modules but not the connections between them | sysml-codegen | WI-015 finding 4; the γ→LCOE edge is harness glue in `run_anchors.py` |
| 10 | Stencil/docstring expression reconstruction loses parenthesization on top of the known literal corruption — docstrings show wrong math next to correct auto-implemented bodies | sysml-codegen | WI-015 finding 5 (extends WI-013's `LiteralRationalEvaluation()` finding) |
| 11 | Self-named calc bindings (`in x = x;`) parse and extract fine but infinite-recurse at syside evaluation — invisible until something evaluates | syside (behavior) / agentic-mbse (check) | WI-014 live check 2; `work/learnings/RAW_LEARNINGS.md` trap 1 |
| 12 | The 6-level validation stack catches none of the unworkable-SysML traps above (per-level checks specified in the gap audit); the sysml-conventions skill stencil actively teaches the broken `return` pattern | agentic-mbse | `.project/research/20260705-120000_validation-stack-gap-audit.md` gap matrix |

WI-013 additionally filed five smaller codegen findings (no snapshot-input CLI path, literals rendered as `LiteralRationalEvaluation()` in stencil docs, warning noise, class-name collisions, snapshot `compilation_results` limits) — see its findings doc. One positive WI-015 finding balances the register: with live extraction, codegen auto-implemented every calc body correctly from compiled ASTs — the AI implementation pass had zero work to do (WI-015 finding 6).

## What the MFE epic does and does not validate

The MFE cost modeling epic (`work/backlog/epic-mfe-cost-modeling.md`, WI-009–012, currently paused at WI-009) tests **H1** (a second family through the same agentic loop — replication), **H3** (the reuse/divergence claim: tokamak and stellarator differing only in the coil and current-drive subsystems, everything else inherited), and **H4** (codegen and sweep on MFE models). It does **not** test H2, and no one should claim otherwise: its formulas are transcribed from 1costingfe (the WI-009 design's explicit sourcing decision), so the epic exercises code→SysML transcription, not literature→model derivation. Whatever 1costingfe gets wrong, those models get wrong with a citation — including, until fixed, the two bugs in the register above. The H2 evidence lives in WI-016 and the Hawker capture, not in the MFE epic.

## Pending evidence

Everything phase 1 listed as pending has landed; what remains pending now is listed at the end of this section. The record:

**WI-015 — IFE end-to-end demonstration: delivered both promised items.** The syside license was renewed 2026-07-05; live extraction ran the same day. The executable correctness oracle exists and passed bit-exactly (all three anchors, rel. deviation 0.0, SV-023 — folded into H1 and H4 above), and the viability sweep delivered the H4 fusion demonstration (11,505 points, ηG > 10 knee mapped, `data/ife_sweep/` — folded into H4).

**License-gated live checks: all three run, all passed** (WI-014 findings, "Live checks — license restored"). Parse clean on the toys; `demo_plant.total_cost` evaluates to 3000.0 and the asserted constraint's predicate to True (via the two-step API); the calc chain enters the codegen graph live and the constraint, as predicted, silently does not. Two syntax traps surfaced on the way (folded into H3 and the register).

**What is pending now** — three named items, none evidence gaps in the epic's scope, all gating what comes next:

- **WI-016 SysML authoring decision**: whether the derived tokamak relations become library calc defs with SV entries. The license gate is lifted; what remains is a user call on the library quality bar (`comparison.md` has the recommendation inputs).
- **Codegen Phase 6 (constraint emission)**: until it lands, every viability constraint is documentation in the model and a re-implementation in the harness (register #3). This is the standing asterisk on H3's constraint half and H4's "check constraints" clause.
- **The cross-part-binding gap** (register #9): must be fixed — or a harness idiom accepted — before the MFE plant models, where essentially all wiring crosses part boundaries. WI-010/WI-012 should not start codegen work assuming generated inter-part channels.

**Also unscheduled but named**: the two vision claims with no implementation path — uncertainty propagation and inverse solving — framed as draft epics (`work/backlog/epic-uncertainty-propagation.md`, `work/backlog/epic-inverse-solving.md`).

---

**Last Updated**: 2026-07-05 — final for the Pipeline De-Risk & Demonstration epic (WI-017 phase 2). Future evidence (MFE epic replication, uncertainty/inverse epics) belongs in a successor revision.
