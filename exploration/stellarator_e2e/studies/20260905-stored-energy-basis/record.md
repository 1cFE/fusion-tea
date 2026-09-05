# Record — `20260905-stored-energy-basis`

## 1. Study header

- **Study id:** `20260905-stored-energy-basis`
- **Package:** `stellarator_tea` (`exploration/stellarator_e2e/pkg/stellarator_tea` → `exploration/stellarator_e2e/generated`), at the WI-042 pin — indicator-input `ec984adc1572792c0d64d26776621ebb154d5b62187a1647e386abd3ff9eb096`, semantic `c37fb58a2b19973d1698aeace5184890107efdf0136d20a502ffe88a0eb956a4`, executable `8ac14fdf3745be9682723902c11a2245f423f2fc6d5bc4726b7fed3b09b5c18e` (integration return `work/orchestration/goals/stored-energy-basis/evidence/round2_T-002_integration_return.json`)
- **Date executed:** 2026-09-05
- **Executor:** the round-2 agent of goal `stored-energy-basis` (a Claude Code session on branch `goal/stored-energy-basis`, worktree `../fusion-tea-stored-energy-basis`)
- **Mode:** execute
- **Arms:** `arm-fence-p100`, `arm-search-p220`, `arm-reread-p220`, `arm-transect-ash` — the committed `20260904-wall-and-heating` arms, re-executed

Arms are variants of the same question, run to be compared. This record's question is one — what the committed window says at the paper's own ash rule — and its four arms are the committed study's four, inherited so that every point joins by coordinates to its committed reading.

## 2. Intake

The owner's ruling that this study serves, verbatim:

> *"ok I agree with next steps. we should fix the ash profile (and make sure this scales up for larger stellarators). and I don't want to add the footnote."* `[OWNER-VERBATIM 2026-09-05]` (`work/orchestration/goals/stored-energy-basis/trail.md` § Owner ruling — 2026-09-05)

The rest of the intake is the executor's, from the goal's round-2 strategy revision and the T-003 scope (`trail.md` § Strategy revision — 2026-09-05, intended study question; § T-003 scope (round 2)), marked as the executor's own: **at the round's pin, what does the `20260904-wall-and-heating` window say when the model integrates the paper's own ash profile — the feasible / ignited / driven counts and the design-column verdict at 100 and 220 MW at R 12.7, a 1.3, beside the committed record and the two constant-scale counterfactuals (0.915 and 0.940 of W) — and does the ash shape's effect on W hold across the geometry window, read as the effective ash exponent and W's move at every (R, a, T, n) the arms visit?** The study is a **restatement by re-execution**: WI-042's plan (§ MR-WI042-14) states that no multiplier re-reads any sustainment-dependent column of the committed record, because every one re-closes through the ash fixed point, so the honest re-read is the same points at the new pin. Hence every arm, window, held key and export column is inherited from the committed study verbatim, and the only additions are the WI-042 channels per point (`W_th`, `tau_E`, the effective ash and electron exponents, `⟨n_e⟩`, all oracle-side like every other multi-field channel) and a join by coordinates to the committed record's own columns (`committed_*`). Every number in this record is at the WI-042 profile family (the ash on the fusion-rate profile, electrons by quasi-neutrality); every `committed_*` number beside it is at the WI-037 family (the ash at the fuel's exponent, electrons at a point-A exponent). The comparison is by coordinates against the committed columns, never against a re-run of the committed record; "feasible", "ignited" and "driven" keep the committed record's definitions (`feasible_driven` = every verdict satisfied and `p_aux_required` ≥ 0).

## 3. Objective and result

- **LCOE objective channel(s):** `<qualified channel name(s)>`
- **LCOE result:** `<value with units, and what point or region it belongs to>`

`<one or two sentences: what the objective did over the studied space>`

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `<qualified id>` | `<local identity>` | `<satisfied \| violated \| indeterminate>` | `<where and why, one line>` |

A short display name is not a qualified identity. If the executed artifacts carry only
the short name, the qualified identity was dropped on export and recovering it is part
of this section, not optional.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `<axis>` | `<search \| sensitivity>` | `<one line>` |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `<axis>` | `<search \| sensitivity>` | `<yes \| no>` | `<what the result showed>` |

## 6. Per-axis account

One pair of subsections per axis. Both ship present; the `**Applies:**` line
discharges the one the axis's framing does not owe.

#### `<axis>` — feasible structure (search framing)
**Applies:** `<yes \| not applicable — this axis is sensitivity-framed>`

`<which constraint is active, where the boundary sits, whether a constrained optimum
was found and where>`

#### `<axis>` — observed response (sensitivity framing)
**Applies:** `<yes \| not applicable — this axis is search-framed>`

`<the observed response; an explicit statement that no boundary claim is made; and,
for any constraint that goes violated anywhere in the sweep, where in the swept space
it does — locating a violation is a fact about the run, not a boundary claim>`

## 7. Axis groups

The declaration is the committed study's, inherited verbatim (`axes.json` byte-identical to `studies/20260904-wall-and-heating/axes.json` at `a5b0b96a`); its per-group notes are that study's words and describe the reasoning that fixed these arms and windows. Nothing in WI-042 added, retired or re-tied a swept key (`alpha_n_e`, the retired entry point, was never an axis).

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `R+tie` | `stellarator_09__stellaris__R` | fan_out | Swept. |
| `R+tie` | `stellarator_09__stellaris__magnet__R0` | **tie** | Same physical major radius; declared in `manifest.json → ties`, reasons in ANNEX § Declared ties. |
| `a` | `stellarator_09__stellaris__a` | fan_out | Swept, the committed window (1.3–2.2). |
| `n_e0` | `stellarator_09__stellaris__n_e0` | fan_out | Swept. |
| `T_i0` | `stellarator_09__stellaris__T_i0` | fan_out | Swept; `T_e0` rides the held 0.95 ratio inside the sustainment calc; **since WI-042 the ash shape's effective exponent is a function of `T_i0` through the reactivity** (4.05 at 14.63 keV, 3.66 at 18), so this axis is also where the shape moves. |
| `I_coil` | `stellarator_09__stellaris__magnet__I_coil` | fan_out | Swept. |
| `p_wallplug_heat` | `stellarator_09__stellaris__p_wallplug_heat` | fan_out | Two levels, sensitivity. No tie since WI-039. |
| `tau_ratio_ash` | `stellarator_09__stellaris__tau_ratio_ash` | fan_out | Swept as the committed sensitivity transect (15 points); held at 8.0 everywhere else — § 8. Since WI-042 it moves the ash **amount** only; the shape does not depend on it. |
| `eta_source_heat` (declined) | `stellarator_09__stellaris__eta_source_heat` | fan_out | Held at 0.50 — § 8; the re-read arm carries round 1's four values. |
| `eta_couple_heat` (declined) | `stellarator_09__stellaris__eta_couple_heat` | fan_out | Held at 1.00 — § 8. |
| `f_suppr_ash` (declined) | `stellarator_09__stellaris__f_suppr_ash` | fan_out | Held at 0.50 — § 8. |
| `iota_23` (declined) | `stellarator_09__stellaris__iota_23` | fan_out | Held at 0.92 — § 8. |
| `j_wp` (declined) | `stellarator_09__stellaris__magnet__j_wp` | fan_out | Held at 118.827 — § 8. |
| `B_max` (declined) | `stellarator_09__stellaris__magnet__B_max` | fan_out | Not swept — § 8. |
| `wall_peak_q_ref` (declined) | `stellarator_09__stellaris__wall_peak_q_ref` | fan_out | The source anchor, held by definition — § 8. |

Fifteen declared keys across fourteen groups, all validated as package inputs at preflight (§ 9). Every held key is asserted per case in `study.py` `export()` as in the committed study, and the six `wall_peak_*` reference facts are checked per case through the store's calibration channel against the baseline's to 1e-9.

## 8. Indicators and rulings

Per proposed axis, including the seven proposed and declined. Source: `indicators.json`, run over all fourteen groups (`subset: false`) on the WI-042 package. The reach is the committed study's on every axis — the same constraints and objectives — with **four more channels tainted on every axis that reaches `sustain`** (the WI-042 outputs `p_avg`, `n_e_volav`, `alpha_n_e_eff`, `alpha_He_eff`); no axis reaches a plant-level electron exponent any more, because there is none.

| Axis | Indicator | Constraints reachable | Objectives reachable | Modules fired | Ruling |
|---|---|---|---|---|---|
| `R+tie` | `constraints_reachable` | 8 / 9 | 11 / 11 | 72 (103 tainted) | swept — the committed geometry lever, re-executed |
| `I_coil` | `constraints_reachable` | 8 / 9 | 10 / 11 | 69 (95 tainted) | swept |
| `a` | `constraints_reachable` | 5 / 9 | 10 / 11 | 60 (91 tainted) | swept, the committed window |
| `T_i0` | `constraints_reachable` | 5 / 9 | 8 / 11 | 56 (82 tainted) | swept; the axis the ash shape moves along |
| `n_e0` | `constraints_reachable` | 5 / 9 | 8 / 11 | 56 (82 tainted) | swept |
| `p_wallplug_heat` | `constraints_reachable` | 3 / 9 | 4 / 11 | 49 (61 tainted) | swept, two levels, sensitivity |
| `tau_ratio_ash` | `constraints_reachable` | 5 / 9 | 8 / 11 | 56 (82 tainted) | swept as the committed sensitivity transect (15 points), not a design lever |
| `f_suppr_ash` | `constraints_reachable` | 5 / 9 | 8 / 11 | 56 (82 tainted) | **declined, held at 0.50** — as committed |
| `iota_23` | `constraints_reachable` | 5 / 9 | 8 / 11 | 56 (82 tainted) | **declined, held at 0.92** — as committed |
| `eta_source_heat` | `constraints_reachable` | 3 / 9 | 4 / 11 | 49 (61 tainted) | **declined, held at 0.50** — as committed; the re-read arm carries the predecessor's four values as its grid |
| `eta_couple_heat` | `constraints_reachable` | 3 / 9 | 4 / 11 | 49 (61 tainted) | **declined, held at 1.00** — as committed |
| `j_wp` | `constraints_reachable` | 4 / 9 | 4 / 11 | 53 (62 tainted) | **declined, held** — as committed |
| `B_max` | `constraints_reachable` | 1 / 9 | 0 / 11 | 2 (2 tainted) | **declined** — as committed |
| `wall_peak_q_ref` | `constraints_reachable` | 1 / 9 | 3 / 11 | 8 (9 tainted) | **declined, held by definition** — the source anchor, as committed |

**No axis reported `no_constraint_response`, so no owner ruling was owed under runbook step 4's fail-closed condition.** The rulings are the committed study's, inherited: this record asks what the committed window says at the new pin, and a changed axis set would be a different study.

**Not derivable, disclosed in every record.** Monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a possible path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output. Every response reported in § 6 is an executed observation on the grid, not an indicator claim.

**Model-development findings.** No axis reported `no_constraint_response`; the obligation is discharged by a stated nil: none owed. The committed study's observations carried beside its rulings (the unbounded `a`, the one-sided sustainment fence, the optimistic coupling, the bare `B_max` inequality, the un-priced `j_wp`, replacements costing no availability, `tbr_ok` held-vs-held) stand as its § 8 records them and are re-sighted here only where this record's own data speaks to them (§ 15).

## 9. Preflight results

`results/preflight_results.json`. **All six gates ran; all six pass.** The identity gate read `results/package_identity.json` and the baseline gate read `results/baseline_result.json`, both deposited by `study_route.execute_baseline` at step 5, before any study point ran.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation (`declared_keys`) | pass | 15 declared keys across 14 groups, all package inputs |
| Suffix-sibling scan (warnings only; `sibling_scan`) | pass | no suffix-sibling findings |
| Identity (`identity`), against `results/package_identity.json` | pass | kind `sealed`, digest `8ac14fdf3745be96…` recomputed from 0 allowed-modified files and 0 declared sources; every other sealed artifact matches |
| Baseline gate against the pinned headline (`baseline_headline`), against `results/baseline_result.json` | pass | `stellarator_09__stellaris__lcoe_calc__lcoe` reproduces at relative deviation 0.000e+00 (322.31843948570247); **9/9** pinned verdicts match — **all nine satisfied**, `sustainment_ok` and `wall_load_ok` expected-satisfied since WI-042 (both were expected-violated at the committed pin) |
| Manifest / package fingerprint match (`manifest_currency`) | pass | both recorded package fingerprints match the package on disk |
| Package cleanliness (`package_clean`) | pass | package tree byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API definition (`study.py` + `study_route.py`, `StudyRunner` + `PreparedListStrategy`) — the committed study's route, inherited with its definition.
- **Why this route:** the arms are coordinated axis-group blocks with every held key explicit per proposal, the declared `R` tie, one arm omitting a column another carries, the pinned baseline as an explicit member, and the derived geometric mask (`R > a + 2.25`) applied at construction; none of that is a Cartesian grid the `teax-study` CLI runs. The route was exercised at step 5 (the baseline executed and deposited) and gated at step 6 before this rationale was written. `study.py` differs from the committed definition only in the places its docstring names (the id, the four oracle channels, the per-point WI-042 columns, the join to the committed record) and in two mechanics disclosed in § 11: the oracle pre-screen runs in a process pool (one evaluation per proposal, the same evaluation the committed screen made serially) and the run is split into a screen phase and an execute phase so the critique could read the screen before any point ran — with the execute phase guarded (critique F5): the cache is bound to the proposal count, the oracle's source digest and the package identity; an existing store is refused; the executed key set is asserted equal to the screened set.

**Glue disclosure — glue ledger: none.** `results/package_identity.json` records `kind: sealed`, zero allowed-modified files and zero adapter sources. The harness supplies no value the model does not compute; the package is sealed on stock teax at revision `744745f895677f3344b9884627369a6a47ed987f`.

## 11. Study definition and window provenance

**Window provenance: `engineered`, inherited — and amended in one respect before any point ran.** Every window, grid, anchor and held key is the committed study's (`studies/20260904-wall-and-heating/study.py` at `a5b0b96a`, its `record.md` § 11: windows fixed after two oracle passes and the pre-execution critique's revisions F6/F7): `R` 11.2 / 12.7 / 14.2 / 15.7 / 17.2 with its tie; `a` 1.3 / 1.5 / 1.7 / 1.8 / 2.0 / 2.2; `I_coil` 13 / 14 / 15 / 16 / 18 MA; `T_i0` 14.63 / 16 / 17 / 18 keV; `n_e0` 0.6–1.0× of 5.06e20 at 100 and 220 MW wall-plug; the re-read arm's 384-point grid at four source efficiencies less the 24 shared points; the ash transect τ*/τ_E 2 / 4 / 6 / 12 / 16 through the committed three anchors; the pinned baseline as an explicit member of `arm-fence-p100`; the derived geometric mask `R > a + 2.25` (ANNEX § Validity masks) at construction. **The one amendment (critique F1(b); trail § Amendment 2026-09-05 — amends § T-003 scope (round 2)): the T 13 keV rows are restored on the two geometry grids** — about 1,500 proposals at both levels, the pre-F6 committed grid rows the committed critique dropped because sustainment blocked all of them at the WI-037 pin (`20260904-wall-and-heating` `window_edges.json`: 117 MW required at 13 keV). Sustainment is the fence WI-042 relieved; the critique's probes at the rule find the driven region at large minor radius at roughly 12.5–13.5 keV, below the committed window's bottom, where the committed window's own points ignite. Those rows are a named class (`class_vs_committed = not_proposed_by_committed`) and every comparison against the committed record is over the points executed in both. **No other window was chosen and the full scan was not re-run**, because this study's object is the committed window itself: it asks what those points say at the WI-042 pin, and a window fixed from the new package's own scan would answer a different question. That is the disclosure the runbook's step 7 asks for: the provenance is engineered, by the committed study, for the committed study's reasons, and inherited here as the restatement's object. Consequently the committed record's own caveats on its windows travel with this one: the `a`-top is not fence-caught (the window stops at 2.2 by choice); the 220 MW optima sat on the window's bottom current and temperature; R 9.7 m and T 13 keV are bracketed by the committed transects and not executed.

**The window's edges at the rule** (critique F1(a); `edges.py`, `results/window_edges.json`): the committed transects' anchors ignite at the rule, so the one-axis transects were re-read anchored on a point driven at the rule at both levels (R 15.7, a 2.2, I 13 MA, T 13 keV, n 1.0×) and on the design column (R 12.7, a 1.3, I 15.4 MA, T 14.63, n 1.0×), the T transect refined to 11–20 keV: `<each executed edge stated as caught or not caught at the rule, per axis and anchor, from window_edges.json>`.

**The oracle pass this record does make** is the evaluability pre-screen over every proposal (the committed study's pattern, exception-hardened): the oracle at the WI-042 chain, evaluated once per proposal and fed to both exports, decides which proposals the sealed package could close (`p_net` above zero, no exception). Its exclusions are `results/excluded_points.csv`, each with its reason and — new here — whether the same coordinates were excluded by the committed screen (`committed_excluded`) and the committed case id where the committed run executed them. The counts, once the screen ran: `<screen counts: proposed / evaluable / excluded; how many of the excluded were excluded at the committed pin, how many are new, how many committed exclusions are now evaluable>`.

**Two mechanics disclosed, neither changing what is evaluated.** (i) The pre-screen runs in a process pool (`study.py` `screen()`: `multiprocessing.Pool`, `imap` preserving order, one oracle evaluation per proposal, each worker with its own oracle memo) because the WI-042 chain costs about 1.1 s per oracle evaluation — five reactivity-weighted profile integrals per point where the WI-037 chain had one — and a serial screen of 6,376 proposals would take two hours where a pooled one takes minutes; the committed screen was serial. (ii) The run is split into a `screen` phase and an `execute` phase (`study.py` `run(phase=…)`): the screen deposits `results/excluded_points.csv` and caches the evaluable list under `results/_work/` (gitignored, not evidence), and the execute phase loads that cache and runs the points; the oracle is still evaluated once per proposal and joined to the executed cases by input key exactly as the committed `run()` did. The split exists so the pre-execution critique could read the screen's result before any point ran through the sealed package.

**The ordering, recorded rather than hidden.** The pre-screen (an oracle pass, no point through the sealed package) ran **before** the critique, as the committed study's scan did and disclosed, so that the critique could read real numbers — the new excluded set beside the committed 65. No study point ran through the sealed package before the critique's verdict was recorded (§ 14); the only execution before it was the manifest's pinned baseline point (step 5), a route-preparation act.

**What the screen shows about the closure's validity edge (row `20260904-wall-and-heating#8`).** `<the excluded set at the WI-042 chain beside the committed 65: the reasons (non-positive fuel / non-real), where they sit (R, a, I), whether the edge moved inward or outward, and the counterfactual's prediction of 35 further points falling off at the 0.940 scale, against what actually happened at the rule>`.

**The per-point columns this record adds to the committed export** (`study.py` `export()`): `W_th_MJ_oracle`, `tau_E_s_oracle`, `alpha_He_eff_oracle`, `alpha_n_e_eff_oracle`, `n_e_volav_oracle` (the WI-042 derived-profile channels, oracle-side like every `sustain__*` field), and the join `committed_case_id`, `committed_excluded`, `committed_lcoe`, `committed_p_fus`, `committed_wall_load_peak`, `committed_beta`, `committed_p_aux_required_MW`, `committed_W_th_MJ`, `committed_tau_E_s`, `committed_n_He0`, `committed_sustainment_ok`, `committed_wall_load_ok`, `committed_beta_ok`, `committed_recirc_ok`, `committed_feasible`, `committed_ignited`, `committed_feasible_driven`, `W_ratio_vs_committed`, `feasible_driven_changed` — every one read from the committed record's own `results/points.csv` and `results/oracle_operands.csv` at `a5b0b96a` by the nine coordinates a proposal is defined by (`_coord_key`), never recomputed.

**Arms are tagged at construction**, and the pinned baseline is a member of `arm-fence-p100` by construction (`is_baseline_point` true once) — as committed.

## 12. Cross-fingerprint correlation and what it means

`<when the arms span fingerprints: which boundary was crossed; that constraints were
matched by definition qualified name plus local identity; every predicate_ir
difference, disclosed; and what the correlation licenses and does not license. The
compatibility tuples themselves are snapshot values under stores[]. When they do not
span fingerprints, discharge the nil by naming the condition: "single fingerprint — no
cross-arm correlation needed".>`

## 13. Verification

`<the outcome: what passed, what did not, and what the result licenses. The command,
sampling scheme, tolerance, and summary digest are snapshot values under
arms[].verification — do not restate them here.>`

`<what verification did not cover, named. A value that is identical by construction on
both sides is not independently verified, and saying so here is part of the outcome.>`

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| **Pre-execution framing critique** (runbook step 4; a fresh non-author `general-purpose` session from the deposited prompt `work/orchestration/goals/stored-energy-basis/evidence/round2_T-003_precritique_prompt.md`; verbatim at `evidence/round2_T-003_precritique.md`; ran before any point ran, while the first oracle pre-screen was in progress) | **MAJOR** — eleven findings | **All accepted.** F1 (the committed window's T-bottom was fixed by the fence WI-042 relieved; at the rule the driven optimum lies below it): (a) the edges re-read at the rule (`edges.py`, § 11); (b) the T 13 keV rows restored on both geometry grids by a dated scope amendment before any point ran (trail § Amendment 2026-09-05). F2 (the constant-scale counterfactuals do not bracket the rule): joined per point by committed case id and read only as predictions the rule tested; counts at three bases with basis and denominator (§§ 3, 4, 12). F3 (the design column opens at the pinned baseline point only, on three fences at once, at coupling 1.00): stated at the claim site (§§ 3, 6). F4 (the ignited set dominates): `feasible_driven` first, the transitions split (`transition_vs_committed`), a row-`#4` disposition (§ 15). F5 (the execute phase could execute a set other than the screened set): the cache stamped and checked, an existing store refused, the executed set asserted equal to the screened set (`study.py` `run()`). F6 ("the shape scales" is true by construction): stated as met by construction and demonstrated, with what it rests on (§ 6). F7 (W as package evidence): `W_th_MJ_store` from three store channels, asserted against the oracle (§ 13). F8 (four point classes and denominators): `class_vs_committed` on every point and every exclusion (§§ 4, 11). F9 (the counterfactuals' third basis): § 2 and every comparative sentence carry it. F10 (shadow columns): inherited, not re-read, labelled so (§ 6). F11 (exception classes): the screen's reasons classified (§ 11). |
| Correctness (the executor's own re-derivations from `results/`) | `<verdict>` | `<disposition>` |
| Honesty (what the record claims against what `results/` carries) | `<verdict>` | `<disposition>` |
| Readability (a cold reader's recovery of the question, the bases and the answer) | `<verdict>` | `<disposition>` |

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md` as `<study-id>#<n>`.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `<study-id>#<n>` | `<model \| process>` | `<one line>` | `<one line>` | `<home, or unrouted>` |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling
item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `<digest>`
- **Schema version:** `<snapshot_schema_version>`

No snapshot content is restated here.

## 17. What this record does not contain

`<every fact a reader might expect and will not find, stated rather than left to
inference. Gaps in the record itself only — the glue disclosure belongs in §10 and a
framing-conditional nil belongs in §6.>`

---

