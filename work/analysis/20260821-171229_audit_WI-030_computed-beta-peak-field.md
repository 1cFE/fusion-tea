# Audit — WI-030 Computed beta and conductor peak-field limit (Stellaris)

**Scope:** work item audit, `work/completed/20260822_WI-030_computed-beta-peak-field/`
**Commits audited:** `ba5c9945` (model, package, oracle, fixtures), `72dc7699` (SV-036 record, spec criteria, plan record); working tree at `72dc7699` with no uncommitted change under `models/`, `exploration/stellarator_e2e/`, or `tests/`
**Auditor session:** fresh — every number below was reproduced in this session (independent Python recompute, the generated impls and predicate executed directly, the runner, preflight, both suites, the validator on the before and after trees, and the Table 2 / Table 5 page images read by eye). Nothing is inherited from the Implementation Record.
**Date:** 2026-08-21
**Overall verdict: POSITIVE.** All six MR-WI030 requirements satisfied, every spec success criterion met, Levels 1–3 clean, SV-036 confirmed passing. One WARN (a validator count the plan's gate could not see, introduced by design decision D10), one record-precision nit, five informational notes. Nothing blocks close.

**PROTOCOL.** No path under `knowledge/holdout/` was read, listed, or cited in this audit. The WI-030 diff (models, oracle, studies) contains no reference to ARIES-CS or the hold-out.

---

## Executive summary

WI-030 makes the on-axis field a physics lever (beta is now computed from the model's own profiles and `magnet.B`) and adds the first conductor-technology constraint (`B_peak = B × peak_ratio ≤ B_max`). The audit reproduced all of it:

| bar | subject | verdict |
|---|---|---|
| 1 | Bound values vs the Table 2 / Table 5 page images and 1costingFE at pin `0254385` | **PASS** — every value matches its source; the extraction text (which prints 4.55 / 3.37) is the corrupted one, as SOURCE_INDEX warns |
| 2 | Computed beta vs the printed values | **PASS** — Point A 0.026834157 (−2.77 %), Point B 0.028690519 (+2.10 %), both inside the spec's ±3.5 % band |
| 3 | Peak-field predicate at the four SV-036 points | **PASS** — margins 0.0 / −11.9 / +0.02433 / −0.00333, exactly as claimed |
| 4 | Design-point headline unchanged, six verdicts, oracle bit-exact | **PASS** — runner exit 0, 16 channels at rel ≤ 4.13e-16, `beta` and `B_peak` at 0.0 |
| 5 | Study capability | **PASS** — preflight 6/6 incl. `package_clean`; `tests/study` 267 passed / 1 skipped; `tests/models` 48 passed / 13 skipped |
| 6 | Validator | L1 0; L2 12 → 12 placeholder bindings (unchanged); L6 ERROR line list unchanged; **L6 `DESIGN_ATTR_INCOMPLETE` 98 → 102** (finding F1) |
| 7 | MR-3 / MR-4 | **PASS** — no concept value in the library defs, no Stellaris value in `mfe_plant.sysml`; every new Ref resolves |
| 8 | Twin byte-identity, contract facts | **PASS** — five files identical in both trees; 173 / 75 / 6, `beta` absent, `beta_ok` id unchanged |

**Environment verified:** sysml-codegen 0.1.1 at `8a758e92` (fusion-tea pin), stock teax at `744745f`, 1costingFE at `0254385` (cited lines read with `git show 0254385:`), agentic-mbse validator from the fusion-tea venv.

---

## Validation results (`agentic-mbse validate --complete models`, 22 files)

| level | result | before WI-030 (`ba5c9945^`, same validator) | after |
|---|---|---|---|
| 1 Syntax | ✅ | 0 errors | 0 errors |
| 2 Structural | ❌ (pre-existing) | 12 placeholder bindings, 0 unused defs | 12 placeholder bindings, 0 unused defs — the displayed five WARN lines identical (line numbers shifted) |
| 3 Dataflow | ✅ | 0 cycles | 0 cycles |
| 4 Constraint coverage | ✅ | 6 usages, 100 % executable | 7 usages, 100 % executable (+`peak_field_ok`) |
| 5 Traceability & docs | ✅ | 79 / 79 documented | 81 / 81 documented |
| 6 Architecture | ❌ (pre-existing) | 219 issues; `DESIGN_ATTR_INCOMPLETE` 98, `UNEXTRACTABLE` 56; 5 ERROR lines displayed | 223 issues; `DESIGN_ATTR_INCOMPLETE` **102**, `UNEXTRACTABLE` 56; the same 5 ERROR lines displayed |

Levels 1–3: clean. Level 6 delta attributed by experiment: giving `n_e0`, `T_e0`, `n_He0`, `alpha_n_e` in `mfe_plant.sysml:188-194` a `default 0.0` returns the count to 98 and the issue total to 219. See F1.

---

## Numerical verification

Baseline sources: Stellaris design paper page images `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_009_table_0.png` (Table 5) and `page_002_table_0.png` (Table 2); Eqs. 2–3 images `page_007_eq_0.png`, `page_007_eq_1.png`; 1costingFE `src/costingfe/defaults.py` and `src/costingfe/layers/tokamak.py` at `0254385`. Thresholds per the model-validation skill (PASS ≤ 1 %, WARN 1–5 %, FAIL > 5 %); where the spec states its own bar (beta ±3.5 %), the spec's bar governs.

### New bound values

| parameter | model value (file:line) | baseline value (source) | discrepancy | status |
|---|---|---|---|---|
| `n_e0` | 5.06e20, `stellarator_plant.sysml:473` | Table 5 image "Peak el. density 5.06" (Point A) | 0 % | PASS |
| `T_e0` | 15.40, `:476` | Table 5 image "Peak el. temperature 15.40" | 0 % | PASS |
| `n_He0` | 0.56e20, `:479` | Table 5 image "Peak helium ash density 0.56" | 0 % | PASS |
| `alpha_n_e` | 0.596, `:482` | derived: 5.06/3.17 − 1 = 0.59621 (both printed in the Table 5 image) | 0.04 % (rounding) | PASS (calculated) |
| `magnet.peak_ratio` | 2.7666666666666666, `:153` | Table 2 image: 24.9 T peak conductor / 9.0 T axis av.; `24.9/9.0` in float64 = `2.7666666666666666`; `9.0 × value == 24.9` exactly | 0 % | PASS (calculated) |
| `magnet.B_max` | 24.9, `:161` | Table 2 image "Peak conductor magnetic field strength 24.9" | 0 % | PASS — **design-specific by owner ruling**; 1costingFE `defaults.py:611` REBCO `b_max = 23.0` disclosed in the doc (model exceeds the upstream ceiling by 8.3 %, intentionally) |
| `'Volume-Averaged Beta'.mu0` (default) | 1.25663706212e-6, `mfe_plasma_scaling.sysml:312` | model's own `mfe_magnet_cost.sysml:41` (same value); 1costingFE `tokamak.py:37` 1.25663706127e-6 | 6.8e-10 vs 1costingFE | PASS (model-consistent; the 1costingFE value is the CODATA 2022 figure, the model's is CODATA 2018 — immaterial at 7e-10) |
| `'Volume-Averaged Beta'.e_keV` (default) | 1.602176634e-16, `:314` | `tokamak.py:36,40` `_EV × 1e3`, exact SI | 0 % | PASS |

### Existing inputs the new calc reads (not re-derived here; checked against the image)

`n_D0 = n_T0 = 1.96e20` (`:450,453`; Table 5 1.96 / 1.96), `T_i0 = 14.63` (`:456`; Table 5 14.63), `magnet.B = 9.0` (`:133`; Table 2 / Table 5 9.0) — all PASS. `alpha_n = 0.33`, `alpha_T = 1.19` are WI-022 Fig. 16 digitizations, audited in that item.

### Computed values (independent recompute, generated impls executed directly, runner)

| quantity | generated impl | independent Python | printed / expected | discrepancy | status |
|---|---|---|---|---|---|
| beta, Point A | 0.026834157382368398 | 0.0268341573823684 | Table 5 "Vol. av. beta 2.76" | **−2.77 %** | PASS vs spec bar ±3.5 % (WARN-band under the generic threshold; explained: thermal beta only, the paper's Table 4 carries a fast-particle pressure fraction) |
| beta, Point B (`alpha_n_e = 0.6366`) | 0.028690519111644643 | 0.028690519111644643 | Table 5 "2.81" | **+2.10 %** | PASS vs spec bar |
| beta, Point B (`alpha_n_e = 6.89/4.21 − 1 = 0.636580`) | 0.028690626389808134 | same | 2.81 | +2.10 % | PASS — this is the value the record prints (F2) |
| beta, Point A, helium on the electron exponent (recorded tolerance) | — | 0.026679846 | 2.76 | −3.33 % | inside the band, as recorded |
| beta at B = 4.69 T | 0.09881600592704343 | 0.09881600592704345 | record 0.098816 | 0 | PASS |
| `B_peak` at 9.0 T | 24.9 (exact) | 24.9 | Table 2 24.9 | 0 % | PASS |
| `B_peak` at 4.69 / 4.70 T | 12.975666666666667 / 13.003333333333334 | same | record | 0 | PASS |
| Nb3Sn ceiling on axis | — | 13.0 × 9.0 / 24.9 = 4.6988 T | design D6 "use 4.69" | — | confirmed (4.70 is violated) |

### Generated predicate `constraint_pred_definition_mfe_viability__conductor_peak_field_limit` (executed)

| (`B_peak`, `B_max_in`) | result | margin | claimed |
|---|---|---|---|
| (24.9, 24.9) | satisfied | 0.0 | 0.0 ✓ |
| (24.9, 13.0) | violated | −11.9 | −11.9 ✓ |
| (12.975667, 13.0) | satisfied | +0.024333 | +0.0243 ✓ |
| (13.003333, 13.0) | violated | −0.003333 | −0.0033 ✓ |

### Design point (`run_stellaris_single.py`, stock teax, exit 0)

Nine anchors OK: total capital 16,129,706,216.036476; LCOE 275.264220; p_net 915.081088; q_eng 6.606662; rec_frac 0.151362; magnet 39.203876 % / $6,323,469,946.33; CAS70 170,974,516.955938; CAS80 773,037.517724; lcoe_1cfe 269.861538. Six verdicts satisfied (`recirc_ok`, `beta_ok`, `net_positive`, `wall_load_ok`, `tbr_ok`, `peak_field_ok`), `assessed_entry_count = 6`, headline `full_satisfaction`. Bit-exact vs the oracle on 16 channels, worst rel 4.13e-16; `beta = 0.026834157` and `B_peak = 24.9` at reldev 0.00e+00. CAS72 guard-live spot-check PASS.

**MR-WI030-6 confirmed:** the headline is identical to `AFTER_MIGRATION_RECORD.md` § 2 and SV-035's re-baseline to the cent; the only change is the sixth verdict.

---

## Critical issues (FAIL)

None.

## Warnings (WARN)

**F1 — Level 6 `DESIGN_ATTR_INCOMPLETE` rose 98 → 102; the plan's gate could not see it.**
- What: the validator reports "design attribute has no value or binding" at ERROR severity (`agentic-mbse/src/agentic_mbse/validation/level6_architecture.py:552-563`) for the four new no-default plant attributes `n_e0`, `T_e0`, `n_He0`, `alpha_n_e` (`mfe_plant.sysml:188-194`). The validator displays only five issue lines per level, so `baseline_validate.txt` / `phase2_validate.txt` compared the displayed lines only, and those are identical.
- Why it happened: design decision D10 declares the four attributes without defaults on purpose ("a beta without its peaks is not a beta"), matching the existing convention for `n_e` and `E_fus`, which sit among the pre-existing 98. The instance binds all four (`stellarator_plant.sysml:473-482`); the validator does not follow cross-file `:>>` redefinition.
- Assessment: by design, same class as the existing 98, no runtime effect (generation has zero readiness diagnostics; every one of the four is a bound entry point in the contract). The spec's "Levels 2 and 6 offender list unchanged (zero introduced)" is met for the offender *list* the gate defined and not for the per-code *count*.
- Recommendation: record the +4 as a known, deliberate deviation in the plan's Implementation Record / spec success criterion (one line), so the next item's baseline is 102, not 98. No model change.

## Minor (record precision)

**F2 — Point B override value.** `verification_record.md` § 3 and the SV-036 row state Point B was run with `alpha_n_e 0.6366` and give beta 0.028690626. With 0.6366 the generated impl returns 0.028690519; 0.028690626 is what the exact pair ratio 6.89/4.21 − 1 = 0.636580 produces. Both round to +2.10 % and both are inside the band; the oracle-parity claim is unaffected (package and oracle received the same override). Recommend the record state the override actually used (0.636580) so the printed digits reproduce.

## Informational

- **F3** — `tests/study` tallies 267 passed / 1 skipped here vs 262 / 1 in the record; `tests/` is byte-identical between `ba5c9945` and HEAD, so the difference is collection, not a regression. `tests/models` 48 / 13 matches.
- **F4** — `data/traceability_matrix.csv` now carries rows for the three new definitions only. `'Magnet System'` (modified by this item) and `'Beta Limit'` (rewired) have no rows, as no MFE definition before WI-029 does; MR-4 states the matrix is superseded by inline citations. Pre-existing, not introduced.
- **F5** — pre-existing non-ASCII `—` at `mfe_viability.sysml:26,31,51`; none in the new text (generation has always passed with them).
- **F6** — `agentic-mbse status` warns that `spec.md Status='active'` overrides BACKLOG `backlog` for WI-030; resolved by `pm close-item`.
- **F7** — the DI ruled in design D3 ("B enters MFE physics through beta; thermal beta from a source's peaks sits 2–3 % under its printed equilibrium beta") is not yet minted; the uncommitted `knowledge/KNOWLEDGE.md` diff carries WI-031's DI-007…010 only. Due at close, as planned.

---

## Traceability

**Definitions with MR-4 doc citations:** `'Volume-Averaged Beta'` (`mfe_plasma_scaling.sysml:257-326`), `'Conductor Peak Field'` (`:328-356`), `'Conductor Peak Field Limit'` (`mfe_viability.sysml:97-121`) — Source / Ref / Basis present; every Ref resolved in this session: `tokamak.py:36-40` (constants), `:117-126` (`compute_beta_N`, half-form disclosed correctly — the upstream code is `MU_0 * n_e * p_J / B**2`), `defaults.py:597-603` (`MagnetProperties.b_max`), `:605-614` (`MAGNET_TABLE` 23.0 / 13.0 / 9.0), the four image files present and readable. Six new instance bindings carry `{ doc }` blocks with image Refs. `'Magnet System'` doc parameter list extended (`mfe_power_core.sysml:79-80`).

**Definitions missing citations:** none in scope.
**Definitions missing traceability-matrix entries:** none of the three new definitions (rows at `data/traceability_matrix.csv:50-52`); `'Magnet System'` has none (pre-existing, F4).

---

## PR-XXX compliance

| requirement | verdict | evidence |
|---|---|---|
| PR-1 Taxonomy before modeling | n/a | Stage-2 item under an established epic |
| PR-2 Shared vs divergent structure | n/a | — |
| PR-3 Documented patterns before production models | PASS | The beta calc reuses the WI-022 profile pattern (`u = 1 − ρ²` average, cited in the doc at `mfe_plasma_scaling.sysml:258-291`) and the `magnet.B` read idiom of `magnet_cost`; the calc-then-compare shape mirrors `wall_load_ok`. Design "Research Findings" records the prototype that proved both. |
| PR-4 Iteration with feedback | PASS | Risk R1 (arithmetic in a predicate) was discovered at design research, looped back to a design change (D1) and a run-study backlog row, not papered over. |
| PR-5 Committed artifacts per phase | PASS | spec, design, plan, research (`knowledge/research/approved/20260821-152108_…`), verification record, three validation baselines all committed in `ba5c9945` / `72dc7699`. Note: the research report reached `approved/` by hand because upstream `pm approve-research` refuses an empty insight list — filed as an owed upstream filing in `CURRENT_WORK.md`. |
| MR-3 Library concept-agnostic | PASS | New library defs carry only `1.0` / `2.0` arithmetic literals and the two cited constants; `mfe_plant.sysml` carries no Stellaris value (grep for `5.06e20|15.40|0.56e20|0.596|2.7666|24.9` empty); `tests/models/test_beta_peak_field.py` guards it. |
| MR-4 Traceable citations | PASS | See Traceability. No `[ASSUMED]` value introduced; the owner's 24.9 T ruling and the 23.0 T upstream disagreement are both in the binding's doc (`stellarator_plant.sysml:155-163`). |

## AD-XXX adherence

| decision | verdict | evidence |
|---|---|---|
| AD-001 plain `Real`, units in docs | PASS | all 14 new formals/attributes are `Real` with unit comments |
| AD-002 `attribute def` bundles metadata | no deviation introduced | the MFE models use plain attributes throughout (pre-existing MFE convention); WI-030 follows it |
| AD-006 parameters separate from calculation | PASS | both calc defs take `Real` inputs; values live on the plant / magnet part and are bound per instance |
| AD-007 magnet system in the library | PASS | `peak_ratio`, `B_max` added to the library `'Magnet System'` (`mfe_power_core.sysml:94-96`), bound in the instance's `part :>> magnet` block. AD-007's prose lists six magnet parameters; it is now eight — a one-line refresh is optional, not a deviation. |

## SV-XXX

| criterion | evaluated | status |
|---|---|---|
| SV-036 | every clause re-executed (beta A/B, oracle parity, headline, six verdicts and margins, LTS points 9.0 / 4.69 / 4.70 T, contract 173/75/6 with `beta` absent, L1 0 and displayed-offender diff empty, preflight 6/6, suites green) | **passing** (re-affirmed via `pm update-validation`) |
| SV-033 (five → six verdicts) | design-point verdict parity 6/6 | still passing; the sixth verdict is additive |
| SV-034 / SV-035 headline bars | reproduced to the cent | still passing (their `handshake_1costingfe.py` mechanism not re-run: it cannot execute on the 2.0.0 package, P3 backlog) |

## MR-WI030 verification (work item acceptance)

| requirement | verdict | evidence |
|---|---|---|
| MR-WI030-1 beta computed, not bound | **PASS** | formula in `mfe_plasma_scaling.sysml:317-325` is the spec's; `beta_ok` reads `beta_calc.beta` (`stellarator_plant.sysml:911`); bound `beta` deleted, cross-check comment in place (`:862-866`); `stellarator_09__stellaris__beta` absent from the contract; `beta_calc__beta` channel present; A −2.77 %, B +2.10 % |
| MR-WI030-2 peak-field limit executes | **PASS** | six concrete catalog entries, 0 excluded; `peak_field_ok__49c6b8228a73cac5` with `definition_typed` source; predicate `B_peak <= B_max_in`; margins as claimed; `indicators.predicate_operands` parses all six (tests green) |
| MR-WI030-3 library concept-agnostic | **PASS** | see MR-3 row |
| MR-WI030-4 every value sourced | **PASS** | six bindings' Refs read citation by citation; all resolve to an image or a pinned upstream line; nothing from a typical-literature value |
| MR-WI030-5 regenerate, re-pin, keep green | **PASS** | contract 2.0.0 at semantic `1ca93d0c…` / executable `7447efea…`; manifest verdicts six and `beta` in the objective catalog; `oracle_entry.py:145-156` binds `beta_in` as a channel and the new row; preflight 6/6; `tests/study` + `tests/models` green; IFE census untouched |
| MR-WI030-6 headline unchanged | **PASS** | runner anchors to the cent; 16 channels bit-exact |

**Spec success criteria:** all eleven met. The "Levels 2 and 6 offender list unchanged (zero introduced)" criterion is met for the offender list the plan defined and carries the F1 caveat at the count level.

**Plan completion gates:** Phases 0–5 all ticked; every gate claim I re-ran (validator diff, contract facts, sha256 of the two normative impls surviving regeneration, runner, preflight, suites) reproduces. The Phase 0 handwritten-sha256 deviation (plan quoted pre-migration hashes) is recorded there correctly.

---

## Recommendations

**Immediate (before or at close)**
1. Add one line to the plan's Implementation Record (or the spec's success criterion) recording the L6 `DESIGN_ATTR_INCOMPLETE` +4 as deliberate (D10), so the next baseline is 102 (F1).
2. Correct the Point B override value in `verification_record.md` § 3 and the SV-036 row to `alpha_n_e = 0.636580` (F2).
3. Mint the D3 DI at close (F7).

**Follow-up**
- Future validator gates should diff the per-code counts as well as the five displayed lines; the tool hides everything past five. Worth a line in the migration ledger's gate rule or an agentic-mbse `--verbose` that itemizes.
- Optional: refresh AD-007's parameter list to include `peak_ratio` and `B_max`.

**Promotable pattern (flagged in the spec, not promoted here):** "a viability limit on a technology-dependent quantity is bound on the library part that owns the technology and asserted once in the generic plant through a library constraint def" — used once (`peak_field_ok`); promote to a PR-XXX after the tokamak instantiation exercises it a second time, as the spec proposes.

---

## Audit metadata

- **Models audited:** `models/library/analyses/mfe_plasma_scaling.sysml` (new defs `:257-356`), `models/library/analyses/mfe_viability.sysml` (`:97-121`), `models/library/cost_structure/mfe_power_core.sysml` (`:79-80`, `:94-96`), `models/designs/generic_mfe/mfe_plant.sysml` (`:188-216`, `:836-839`), `models/designs/stellarator_09/stellarator_plant.sysml` (`:153-163`, `:466-483`, `:862-866`, `:911`); twins under `exploration/stellarator_e2e/models/` verified byte-identical with `cmp`.
- **Package:** `exploration/stellarator_e2e/generated/` at semantic `1ca93d0c988c2828bb1ce3fef18be85be86947a296a33b236d77daeb0f1ab860`, catalog fingerprint `43443297…`.
- **Baseline sources:** Table 5 and Table 2 page images, Eqs. 2–3 images (paths above); 1costingFE `0254385` via `git show`.
- **Thresholds:** model-validation skill PASS ≤ 1 % / WARN 1–5 % / FAIL > 5 %; spec bar beta ±3.5 %; oracle rel 1e-9; headline exact to the cent.
- **Tools executed:** `agentic-mbse validate --complete` (current tree and `git archive ba5c9945^` tree), `run_stellaris_single.py`, `scripts/study/preflight.py gates`, `pytest tests/study tests/models`, generated `run_volume_averaged_beta` / `run_conductor_peak_field` / predicate called directly, independent Python recompute.
- **Scratch:** session scratchpad only; nothing written under the repo except this report and the SV-036 status re-affirmation.
