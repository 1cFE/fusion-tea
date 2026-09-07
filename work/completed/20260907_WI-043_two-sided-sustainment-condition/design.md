---
Status: complete
Created: 2026-09-07
Updated: '2026-09-07'
Related Artifacts:
  Spec: ./spec.md
---

# WI-043 Design — the two-sided sustainment condition

Procedure: `/design-model`. Written by the round agent of goal `burn-control` round 1 (task T-001). The research is the goal's grounding (`work/orchestration/goals/burn-control/evidence/`); no research agents were spawned for the design because the grounding already answered the design's questions.

## Overview

The package gains one verdict and moves no number. A new constraint def in the viability library, `'Burn Hold'`, asserts that the computed required sustained plasma-coupled heating is not negative; the stellarator instance asserts it as `burn_hold_ok` on the same operand `sustainment_ok` reads. Together the two asserts say what the sister systems codes say: an operating point is one whose power balance closes with an auxiliary heating that is zero or positive and no larger than what is installed. The model text carries the basis (a hold condition, never a physics limit on ignition) and the disclosure that the installed side is the paper's start-up sizing read in its point-B sense. The `sustainment_ok` doc comment is corrected to L-004's form. Everything else re-derives from the changed fingerprints.

## Research findings

From the grounding (`goal.md` § Question facts 1–6; `evidence/grounding_sources.md`; `evidence/grounding_probe/summary.md`), restated only as far as the design needs them:

- **The construct exists.** `'Net Power Positive'` (`mfe_viability.sysml:4-19`) is a single-formal constraint def with a literal comparand (`net_electric > 0.0`), emitted by the pinned codegen as `constraint_pred_definition_mfe_viability__net_power_positive(net_electric)`; `_cmp` in `generated/modules/constraints/predicates.py:42-50` handles `>=`. A `>= 0.0` predicate on one formal is the same shape.
- **The operand exists and is a channel.** `sustain.p_aux_required` is the `'Plasma Sustainment'` output the instance already binds into `sustainment_ok` (`stellarator_plant.sysml:1277`); the oracle seam publishes it as the channel `stellarator_09__stellaris__sustain__p_aux_required` (`studies/oracle_entry.py:292`). The new assert binds the same output; the seam binds the same channel.
- **What the verdict set touches.** `manifest.json` `baseline.verdicts` (nine entries; the schema admits only `source_local_identity` and `expected` — no `note`, per the re-pin recipe in memory); `run_stellaris_single.py` `EXPECTED_VERDICTS` / `EXPECTED_VERDICT_COUNT = 9` (`:32-58`); the six `tests/study/data/*.expected.json` (`constraints_reachable` per axis, bound to the semantic fingerprint) and `FIXTURE_CONTRACT` in `test_known_answers.py`; `mfe_census.json` (`derived_against_semantic_fingerprint`; 205 entry points); `stellarator.snapshot.json`; `generated/contracts/model_contract.json`.
- **The baseline is driven.** `p_aux_required` 49.0796 MW at the pin (probe P0, reproduced to zero relative deviation from the record); the new verdict is satisfied there. Ignited points for the independent check: P1 `c2835` (the cheapest fence-feasible ignited point at 100 MW) and P3 `c2132` (the committed headline, −188.8 MW), both `evidence/grounding_probe/selected_points.json`.
- **The doc text's sources**, all read from page renders: Lion 2021 L164, L211, Eq. 7; Lion 2023 Tables 4.2/4.5/4.7, L2154; Stellaris raw PDF p. 9 (Fig. 15 caption; the 50 MW "to reach the desired operation point"), p. 10 (Table 5: gain ∞ / 182, aux power 0 / 14.77 MW; the burn-control paragraph). The Table 5 render is deposited as `evidence/grounding_sources_table5.png`.

## Design decisions

### D1 — A second constraint def, not a two-sided rewrite of 'Sustainment Limit'. `[AGENT]`

`'Burn Hold'` is its own def with one formal, asserted as its own verdict `burn_hold_ok`. **Why:** (i) every committed record since `20260901-sustainment-fence` carries a `sustainment_ok` column; a rewrite to `0 ≤ x ≤ y` would make that column mean something different at 3,654 points of the last record, and the goal's invariant is that "driven" keeps its definition and counts compare by case id (MR-WI043-7); a separate verdict keeps every committed column's meaning bit-for-bit and adds one column that re-reads from the committed `p_aux_required_MW_oracle` by sign. (ii) Codegen friendliness: the single-formal literal-comparand shape is already emitted; a compound `and` predicate is not exercised by any existing def. (iii) Readability: the study's three-state classification (violated / driven / ignited) maps onto two verdicts, one each side. **Rejected alternative:** the two-sided rewrite — one verdict, no new column, but the committed columns' meaning changes and the compound predicate is new ground for the tool.

### D2 — The comparand is a literal zero and mints no entry point. `[AGENT]`

`p_aux_required_in >= 0.0`. **Why:** zero is the balance's own closing value (the equality `P_loss = P_heat` with `P_aux = 0` is the ignited limit in the sister codes), not a sourced number that could be re-sourced or swept; a `p_aux_floor` attribute would be a settable entry point with no reason to move. The census stays at 205 entry points (predicted; re-derived, never asserted).

### D3 — The doc text is split by concern: the library carries the basis, the instance carries this machine's numbers and the paper's claim. `[AGENT]`

- `'Burn Hold'` (library): the hold-condition basis, the falling-branch reading, the sister codes' practice, the "not a statement that ignition is infeasible" sentence, with the sources (prototyped below, as written into the file).
- `'Sustainment Limit'` (library): its doc gains one paragraph — the installed side is the source's start-up sizing (Table 2 "Required plasma-coupled ECRH power 50" is what the paper installs to *reach* point A; point A itself runs at 0 MW), read here in the paper's point-B sense (a driven point under the installed heating; point B: Q 182 at 14.77 MW); the access requirement is not modelled; the pair with 'Burn Hold'.
- `sustainment_ok` (instance): the comment rewritten — the numbers unchanged (49.08 against 50, 0.92 MW), the reason in L-004's form (the model's W at the rule 519.9 MJ above the sourced-rules 518.3 and the printed 504.65, the verdict satisfied throughout that band; undecidable because of the source's two-sided spread on its own stored energy), the "2.7 % residual" sentence gone, and one sentence on the installed side's sense with a pointer to the library paragraph.
- `burn_hold_ok` (instance): `EXPECTED SATISFIED` at 49.08 MW; the paper's point A is ignited at 0 MW where this model reads 49 MW driven — the two readings named side by side, the difference inside the source's own spread (L-004); the ignited points of the committed window read VIOLATED here and pass `sustainment_ok`, by design.

### D4 — The oracle seam publishes the new operand binding; nothing in the oracle's arithmetic changes. `[AGENT]`

`OPERAND_BINDINGS` gains `f"{P}burn_hold_ok__<hash>": {"p_aux_required_in": {"kind": "channel", "key": f"{P}sustain__p_aux_required"}}`, the hash read from the regenerated `model_contract.json` (codegen derives it; it is never guessed). `verify_stellaris.py` is untouched — the oracle already returns the operand.

### D5 — Every pinned artifact re-derives by its producer, in the recorded order. `[AGENT]`

Snapshot → manifest (three fingerprints; a tenth verdict entry `burn_hold_ok: satisfied`; the headline re-pinned, expected unchanged to the digit) → census (`derived_against_semantic_fingerprint`; 205) → the six fixtures and `FIXTURE_CONTRACT` (predicted: `burn_hold_ok` joins `constraints_reachable` on R, R+tie, a and I_coil — every axis that reaches `sustain` — and on neither availability nor interest_rate; modules fired +1 on those four axes for the new constraint module; channels tainted unchanged) → the single runner (`EXPECTED_VERDICT_COUNT` 10, `burn_hold_ok: satisfied`, the summary message restated). The recipe is `gotcha_repin_after_regeneration` in memory, verbatim.

### D6 — The independent check at ignited points is a package execution, deposited under the item. `[AGENT]`

The package is executed at P1 and P3 (the study route's per-point execution, the same route the studies use) and the two result files are deposited under `work/active/WI-043_*/evidence/`; `burn_hold_ok` must read violated and `sustainment_ok` satisfied at both, and the seam's re-derivation from the oracle channel must agree. This is the disagreement the grounding predicts and the reason the verdict exists.

### D7 — The restatement is written before regeneration, in the plan, and commits first. `[AGENT]`

MR-WI043-7 in the MR-WI041-11 shape: which records carry `p_aux_required_MW_oracle` (every record from `20260904-wall-and-heating` on) and `ignited` (the same), the sign rule, the identity "every committed 'feasible' re-reads as that record's 'feasible driven'", and the statement that no record is edited. Commit A carries the model edits, the twins, the spec, this design, the plan through the restatement; commit B the regenerated bytes and the re-pin.

## Proposed design

### New: `constraint def 'Burn Hold'` — `models/library/analyses/mfe_viability.sysml` (prototyped, lines 229–287)

One formal, `in attribute p_aux_required_in : Real;` (the required sustained plasma-coupled heating, MW, computed); predicate `p_aux_required_in >= 0.0`. The doc text as prototyped: the hold-condition basis; the falling-branch reading with the probe cited; the no-mechanism statement with the research cited; the "NOT a statement that ignition is infeasible" paragraph with the sister codes' equality and the paper's point A; `**Source**` / `**Ref**` / `**Basis**` lines citing the two Lion extractions, the Stellaris extraction with the Table 5 render, Lion 2021 L164/L211/Eq. 7, Lion 2023 Tables 4.2/4.5/4.7 and L2154, Stellaris raw PDF p. 9 and p. 10; the basis line naming the literal zero as the balance's own closing value.

### Changed: `constraint def 'Sustainment Limit'` — same file, doc text only

After the existing "Basis" line's paragraph, add: the installed side's sense (start-up sizing; point-B sense; access not modelled; the pair with 'Burn Hold'), citing Stellaris raw PDF p. 9 and p. 10 (Table 5). The predicate and the formals do not change.

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml` — the assert site (`:1262-1279`)

- The `sustainment_ok` comment rewritten per D3 (numbers unchanged; L-004's form; the installed side's sense; no "2.7 % residual").
- New, immediately after `sustainment_ok`:

```sysml
        // Burn hold (WI-043; goal burn-control): the same operand must not be
        // NEGATIVE -- the lower half of the operating-point condition
        // 0 <= p_aux_required <= installed coupled heating. At this lever point
        // EXPECTED SATISFIED (p_aux_required ~= 49.08 MW >= 0): the model reads
        // the machine as designed as a DRIVEN point on the falling branch of the
        // ignition curve, held by feedback on its own heating. The source's own
        // Table 5 reads its point A as IGNITED (fusion gain infinity, auxiliary
        // power at the operation point 0 MW); the 49 MW between the two readings
        // sits inside the source's two-sided spread on its own stored energy
        // (goal stored-energy-basis L-004) and nothing here is tuned. The ignited
        // points of the committed studies (p_aux_required below zero) read
        // VIOLATED here and SATISFIED on sustainment_ok, by design: they are
        // points this heating system cannot hold, not points that need no heating.
        assert constraint burn_hold_ok : 'Burn Hold' {
            in p_aux_required_in = sustain.p_aux_required;
        }
```

### Changed: `exploration/stellarator_e2e/studies/oracle_entry.py` — one binding (D4)

### Changed: `exploration/stellarator_e2e/run_stellaris_single.py` — `EXPECTED_VERDICTS` gains `burn_hold_ok: satisfied` with its comment; `EXPECTED_VERDICT_COUNT` 10; the parity message restated ("ten satisfied")

### Re-derived (D5): `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, the six `tests/study/data/*.expected.json`, `tests/study/test_known_answers.py` (`EXPECTED_SEMANTIC_FINGERPRINT`, `FIXTURE_CONTRACT`), the regenerated `generated/**`

### Twins: `exploration/stellarator_e2e/models/analyses/mfe_viability.sysml` and `.../designs/stellarator_09/stellarator_plant.sysml` copied byte-for-byte (the flat twin layout: `analyses/`, `designs/`, not `library/analyses/`)

## Cross-file bindings

| Binding | Where | Source |
|---|---|---|
| `burn_hold_ok.p_aux_required_in` | `stellarator_plant.sysml` (instance) | `sustain.p_aux_required` — `'Plasma Sustainment'` output, `mfe_plasma_sustainment.sysml`, already bound into `sustainment_ok` |
| oracle operand `p_aux_required_in` | `studies/oracle_entry.py` `OPERAND_BINDINGS` | channel `stellarator_09__stellaris__sustain__p_aux_required` (existing) |

Imports: `mfe_viability` is already imported by the instance (`sustainment_ok` and the other eight asserts). No new import; no new dataflow edge — the new assert is a second reader of an existing output. Dataflow stays unidirectional.

## Expected baseline behaviour

Every number below is a prediction the implementation checks, not a target it fits.

| quantity | today (pin `ec984adc1572…`) | after | why |
|---|---|---|---|
| every channel (LCOE 322.318439, `p_aux_required` 49.0796, wall peak 3.9788, W 519.914, …) | — | **bit-identical** | no calc, binding or held fact changes |
| the nine existing verdicts | all satisfied | all satisfied, bit-identical | operands unchanged |
| `burn_hold_ok` | — | **satisfied** | 49.0796 ≥ 0 |
| verdict count / headline | 9 / `full_satisfaction` | 10 / `full_satisfaction` | one more satisfied assert |
| semantic, executable, indicator fingerprints | `c37fb58a…`, `8ac14fdf…`, `ec984adc…` | all three move | a new assert is a semantic change |
| census entry points | 205 at `c37fb58a…` | 205 at the new fingerprint | D2: no entry point minted |
| fixtures `constraints_reachable` | — | +`burn_hold_ok` on R, R+tie, a, I_coil; unchanged on availability, interest_rate | reachability follows `sustain` |
| P1 `c2835` / P3 `c2132` | `sustainment_ok` satisfied, `p_aux_required` < 0 | `burn_hold_ok` **violated**, `sustainment_ok` satisfied, every channel bit-identical | the disagreement the verdict exists for |

**If anything else moves, it is a finding to derive, not a number to fit.**

## Validation plan

1. Levels 1–3 on the edited models (done at the prototype for the library def; repeated after the instance edit and the twin sync).
2. Regeneration: expect `New: 1` (the `burn_hold_ok` constraint module), `Regenerated: 0`, every handwritten impl preserved byte-identical, no `handwritten/backup/`, seal clean. A `Regenerated: 1` on any manual-stage calc is a stop — nothing here changes a manual stage's interface.
3. Baseline execution through the single runner and `study_route.execute_baseline`; diff every channel against the pre-change execution (deposited before the change under `evidence/baseline_before/`); verdict parity 10 / `full_satisfaction`.
4. P1 and P3 executions deposited; the seam's re-derivation agrees.
5. The re-pin in D5's order; `m.load` on the manifest; the census count; the fixture contract read from the report.
6. `uv run agentic-mbse validate models --complete` — Levels 1–6, residue compared with the pre-change run (`scratchpad/validate_proto.txt`: Level 6 236 issues, design attrs 207, the WI-042 set).
7. `tests/models` (expect 48 / 13 or better); `tests/study` after commit B (expect the branch's 64 fail-closed cases and nothing else red; every delta explained).
8. SV rows (MR-WI043-12) and `pm trace-element` for the new def; `pm update-validation` to `passing` with the evidence.

## Risks

1. **Codegen names the constraint module or its hash differently from the guess.** *Mitigation:* nothing is guessed; the hash and module name are read from the regenerated contract before the seam and the runner are edited.
2. **A consumer counts nine verdicts by literal.** *Mitigation:* grep for `EXPECTED_VERDICT_COUNT`, `nine`, `9` near verdict logic in `exploration/` and `tests/` before regenerating; the batteries catch the rest.
3. **The fixtures' reachability prediction is wrong** (e.g. the new module changes a trace size on availability). *Mitigation:* the contract is re-derived from the report, never asserted; the prediction is recorded here and the plan says what it actually was.
4. **The doc text reads as a loosening or a tightening of the installed side.** *Mitigation:* D3's wording says the installed side does not move; the disclosure is about what the number is, not what it should be. Reviewed as text against the deposited evidence (MR-WI043-2/-3).
5. **The `sustainment_ok` rewrite drops a fact the trail cites.** *Mitigation:* the numbers stay; only the reason sentence changes; the superseded form is named in the archived WI-042 spec's § Amendments, not here.

## Prototype and validation report

**Prototype: PASS.** `'Burn Hold'` written into `models/library/analyses/mfe_viability.sysml` (lines 229–287) and validated with `uv run agentic-mbse validate models --complete` (SysIDE licence sourced; 2026-09-07):

- **Level 1 (syntax): 0 errors, 0 warnings.**
- **Level 2 (structural): the 12 pre-existing placeholder-literal warnings in `mfe_plant.sysml`, nothing new** (unused definitions 0 — the validator does not flag an unasserted constraint def).
- **Level 3 (dataflow): pass.** **Level 4 (constraint coverage): pass.** **Level 5 (traceability & documentation): pass** — the new def's `**Source**` / `**Ref**` / `**Basis**` lines resolve.
- **Level 6: the pre-existing residue** — 236 issues, design attrs 207, the WI-042 set unchanged (`scratchpad/validate_proto.txt`); nothing names `'Burn Hold'`.

**What the prototype confirms.** The def parses; the single-formal `>= 0.0` shape is accepted; the doc text's citations resolve at Level 5.

**What it does not confirm**, and implementation must: codegen emitting the constraint module; the baseline's bit-identity; the P1/P3 verdicts; the fixture contract.

**Files modified:** `models/library/analyses/mfe_viability.sysml` (prototype; not yet copied to the twin). **Files created:** none.

## Implementation checklist (phased; the plan carries the checkboxes)

1. Library: 'Sustainment Limit' doc paragraph; twin sync; Levels 1–3.
2. Instance: the `sustainment_ok` rewrite and the `burn_hold_ok` assert; twin sync; Levels 1–3; `tests/models`.
3. The restatement (MR-WI043-7) and the pre-change baseline deposit; **commit A**.
4. Regeneration; the contract read; the seam binding; the single runner; baseline parity; P1/P3.
5. Re-pin (D5); Levels 1–6; batteries; SV rows; trace rows; **commit B**.

## Approval

Settled by the round agent under goal `burn-control`, whose owner delegated the modelling judgement and ratified the second-inequality form at grounding `[OWNER-VERBATIM 2026-09-07]` "yes, please proceed with that /run-goal" (`goal.md` § Reserved gates). D1 and D3 are the load-bearing judgments; D1's rejected alternative is written above so the round review can challenge it by re-derivation. `/review-model` is available for an independent design review; not invoked, on the WI-041/WI-042 precedent (the fresh round review checks the item).
