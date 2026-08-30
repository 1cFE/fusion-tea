# Study record — `20260829-p-pump-fence`

## 1. Study header

- **Study id:** `20260829-p-pump-fence`
- **Package:** `stellarator_tea`
- **Date executed:** 2026-08-29
- **Executor:** agent session, GSTH Item 6, goal `p-pump-fence` round 1
- **Mode:** execute
- **Arms:** single arm (`arm-package-default`) — the package's own held configuration

## 2. Intake

The owner's question, verbatim:

> With `p_pump` re-based to 195 MW, where does the `recirc_ok` fence move, and what happens to LCOE?

And the contract for an answer, verbatim:

> A committed, verified study on the regenerated, pinned package that locates the `recirc_ok` fence and quantifies the LCOE shift at the baseline point relative to the 1.0 MW record — with an adverse or inconclusive reading counting as an answer.

**Added by the executor to make that executable, and separated from the quote.** "The 1.0 MW record" is `20260821-power-cycle-ab`, and the comparison is against its published numbers at its own pin, not against a re-run of it. That study ran four power-conversion arms; the one this study compares against is `arm-rankine-paper`, because the package's own held `eta_th` and cost rates *are* that arm — its baseline-geometry LCOE, 275.264, is bit-for-bit the package's pre-WI-033 pinned headline. So this study runs one arm and the comparison is exact rather than approximate.

**Protocol rulings carried into this study.** Four, all recorded before the points ran.

| Ruling | Who | What |
|---|---|---|
| Framing | `[OWNER 2026-08-29]` "approved" | search on `R` and `a`; one arm, the package's own configuration |
| Declined axes | `[OWNER 2026-08-29]` "decline those" | `availability` and `discount_rate` declared and traced, not swept. The "no sensitivity" rationale is carried precedent from `20260821-power-cycle-ab` § 8 `[OWNER-VERBATIM 2026-08-22]`, not a fresh argument |
| Window | `[OWNER 2026-08-29]` "adopted" | the comparand's window and mask adopted whole, substituting for the runbook's step-7 window scan (§ 11) |
| Evaluability exclusion | orchestrator, execution-detail tier | pre-screen `p_net > 0` with the package-owned oracle, exclude the unevaluable points, disclose the boundary as a result. Not a new precedent: `20260823-magnet-technology-ab/record.md:224-226` established the pattern for that study's density floor (§ 11) |

## 3. Objective and result

- **LCOE objective channel:** `stellarator_09__stellaris__lcoe_calc__lcoe` ($/MWh; `…lcoe_1cfe_calc__lcoe` also exported as `lcoe_1cfe`)
- **Points:** 948 proposed, 42 excluded as unevaluable (§ 11), **906 evaluated**, all completed.

**The LCOE half of the question, at the baseline geometry (R 12.7 m, a 1.3 m):**

| | `p_pump` = 1.0 MW | `p_pump` = 195 MW | shift |
|---|---|---|---|
| `lcoe` | 275.264 | **333.067** | **+57.803, +21.0 %** |
| `lcoe_1cfe` | 269.862 | 326.512 | +56.650, +21.0 % |
| `p_net` (MW) | 915.081 | 752.413 | −162.668 |
| `rec_frac` | 0.151362 | 0.322514 | +0.171 |

The 1.0 MW column is `20260821-power-cycle-ab/record.md` § 3 `arm-rankine-paper` at its own pin; the 195 MW column is `results/points.csv` (`is_baseline_point = True`) and `results/oracle_operands.csv`. All six verdicts remain `satisfied` at that point — the re-basing moves the objective by a fifth without flipping any verdict there.

**Best feasible LCOE, and why the study does not call it an optimum.** 225.725 $/MWh at (R 20.0, a 1.65), against the comparand's 209.000 at (14.0, 1.65). The comparand's optimum was *interior* in R; this one sits on the largest R the window contains, and LCOE is still falling at the edge (225.725 at R 20.0, 225.793 at 19.5, 226.501 at 17.5). The constrained optimum is therefore outside the adopted window and this study does not locate it. That is a window consequence, not a result about the machine.

## 4. Constraint outcomes

Status over the 906 evaluated points (`results/points.csv` verdict columns, named by `source_local_identity`; qualified ids from `results/baseline_result.json` `verdicts[]`).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied at all 906 | β is computed from profiles and `magnet__B`, which no axis here touches — inert by construction |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied at all 906 | **and this is the misleading one — see § 15.** It reads satisfied everywhere only because the 42 points where it would fail cannot be evaluated at all |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | satisfied at all 906 | B_peak = 24.9 T = B_max, untouched by any axis here — inert |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | **violated at 184, satisfied at 722** | the fence this study was run to locate; geography in § 6 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied at all 906 | TBR is a bound input (1.074 vs floor 1.05) — inert |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | violated at 353, satisfied at 553 | violated at a ≥ 1.70 m for every R; satisfied up to a = 1.65 m. Identical to the comparand's fence — wall load depends on `a` alone at fixed profiles, and `p_pump` does not enter it |

No verdict is `indeterminate`. Four verdict combinations occur: all satisfied (370), only `wall_load_ok` violated (352), only `recirc_ok` violated (183), and **both violated (1)**. The comparand recorded three combinations and explicitly "no point violates both"; at 195 MW that is no longer true.

Feasible fraction: **370 of 906 = 40.8 %**, against the comparand's `arm-rankine-paper` 563 of 948 = 59.4 %. Measured against the 948 originally proposed, 39.0 %.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `R` | search | Reaches `net_positive`, `recirc_ok`, `wall_load_ok` through computed operands (`indicators.json`); `recirc_ok`'s computed operand is `pb__rec_frac`, which is where `p_pump` enters. The comparand located the fence on this axis. |
| `a` | search | Same reach. The fence is two-dimensional: the comparand's violation set shrank with `a` and vanished above a = 1.10 m. |
| `availability` | not proposed | `no_constraint_response`; serves neither half of the question; the held-equal invariant needs it fixed at the comparand's 0.85. |
| `discount_rate` | not proposed | `no_constraint_response`; as above, held at 0.07. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `R` | search | no | Verdict structure found and it is large: `recirc_ok` violated at 184 points reaching the full R extent of the window at a = 0.80. Feasible fraction 40.8 %, below the comparand's 59.4 %. |
| `a` | search | no | Both fences are functions the run resolved: `wall_load_ok` at a ≥ 1.70 for every R, and the `recirc_ok` fence receding monotonically in `a` from R ≤ 20.0 at a = 0.80 to R ≤ 4.0 at a = 1.70. |
| `availability` | not run | — | Declined by owner ruling; held at 0.85 in every point. No account owed (§ 6). |
| `discount_rate` | not run | — | Declined; held at 0.07. As above. |

## 6. Per-axis account

Every number from `results/points.csv` and `results/oracle_operands.csv`. Fence positions are at grid resolution (ΔR 0.5 m, Δa 0.05 m) and no claim is made about where a boundary lies between nodes.

#### `R` — feasible structure (search framing)
**Applies:** yes

**The `recirc_ok` fence, and how far it moved.** The comparand at 1.0 MW: violated at R ≤ 8.0 m for a = 0.80, 32 points, vanishing above a = 1.10 m. At 195 MW:

| a | violated up to R | points | a | violated up to R | points |
|---|---|---|---|---|---|
| 0.80 | **20.0** (the whole window) | 22 | 1.30 | 7.5 | 8 |
| 0.85 | 17.5 | 20 | 1.35 | 7.0 | 7 |
| 0.90 | 16.0 | 18 | 1.40 | 6.5 | 6 |
| 0.95 | 14.0 | 16 | 1.45 | 6.0 | 5 |
| 1.00 | 12.5 | 14 | 1.50 | 5.5 | 4 |
| 1.05 | 11.5 | 13 | 1.55 | 5.0 | 3 |
| 1.10 | 10.5 | 12 | 1.60 | 5.0 | 3 |
| 1.15 | 9.5 | 11 | 1.65 | 4.5 | 2 |
| 1.20 | 9.0 | 10 | 1.70 | 4.0 | 1 |
| 1.25 | 8.0 | 9 | | | |

The fence changed character, not just position. At 1.0 MW it was a small-machine corner bounded in both axes. At 195 MW it spans the entire R range of the window at a = 0.80 and persists to a = 1.70 — 184 violating points against 32, plus 42 more points beyond it that cannot be evaluated at all. The window no longer contains the fence in R at small `a`: at a = 0.80 every R from 4.0 to 20.0 m violates, so the study cannot say where the fence would be if `R` ran further.

Constrained optimum: **not located** — the best feasible point sits on the window's R edge (§ 3).

#### `R` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `a` — feasible structure (search framing)
**Applies:** yes

Two fences bound the feasible band from opposite sides. `wall_load_ok` is violated at every a ≥ 1.70 m for every R (wall load 4.1647 MW/m² at a = 1.70 against the 4.05 limit), unchanged from the comparand and independent of `p_pump`, which does not enter neutron power or wall area. `recirc_ok` is active at small `a` and its reach in `a` grew: the comparand's violations vanished above a = 1.10 m, and here they persist to a = 1.70 m. At (4.0, 1.70) both fences are violated at once, which is the single both-violated point in the run and does not occur anywhere in the comparand.

The objective still falls monotonically toward the wall-load fence at every R, so a = 1.65 m is the optimal `a`, as in the comparand.

#### `a` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `availability` — feasible structure (search framing)
**Applies:** not applicable — declined by owner ruling (§ 8) and not swept; held at 0.85 in every point

#### `availability` — observed response (sensitivity framing)
**Applies:** not applicable — declined and not swept; this study ran no scan of it and makes no claim about it

#### `discount_rate` — feasible structure (search framing)
**Applies:** not applicable — declined by owner ruling (§ 8) and not swept; held at 0.07 in every point

#### `discount_rate` — observed response (sensitivity framing)
**Applies:** not applicable — declined and not swept; no claim made

### Near-fence re-evaluation

`20260823-magnet-technology-ab#11` requires a headline landing within one grid step of a fence to be re-evaluated across the sourced range of every held value it depends on, with the margin stated.

**The baseline-point headline is not near a fence.** At (12.7, 1.3) `rec_frac` is 0.32251 against the 0.5 threshold and `a` is eight grid steps below the wall-load fence. No re-evaluation owed.

**The fence itself is decided at the fourth decimal in places, so it is re-evaluated.** Two grid points sit within 0.0008 of the threshold: (16.0, 0.90) at `rec_frac` 0.50077 violated, and (13.0, 1.00) at 0.49942 satisfied. `p_pump` is the held value the fence depends on, and the goal records a sourced band of ~130–195 MW for it (~130 MW the documented lower bound from Moscato's 8-loop design, ~150 MW Cismondi's preliminary 9-loop figure, 195 MW the landed value). Re-evaluated with the independent oracle across that band, at a = 0.80:

| held `p_pump` | `recirc_ok` violated up to R | baseline `rec_frac` | baseline `lcoe` | shift vs 275.264 |
|---|---|---|---|---|
| 130 MW | 16.0 m | 0.26629 | 311.122 | +13.0 % |
| 150 MW | 17.0 m | 0.28371 | 317.554 | +15.4 % |
| 195 MW | 20.0 m | 0.32251 | 333.067 | +21.0 % |

**The margin.** Both headline claims survive the whole sourced band. At the bottom of the band the fence still reaches R = 16.0 m at a = 0.80 — double the comparand's 8.0 m — and the LCOE shift is still +13 %. The two knife-edge grid points do move: at 130 and 150 MW both read satisfied, so the fence position at a specific `a` is band-sensitive even though its scale is not. This is a margin statement about a held value; `p_pump` remains a held input and no point in this study moves it.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `R` | `stellarator_09__stellaris__R` | fan_out | plasma major radius, one plant-level entry point since the model migration |
| `R` | `stellarator_09__stellaris__magnet__R0` | tie | the magnet-cost Ampère's-law current runs on the same major radius under a separately authored attribute; declared in `manifest.json` `ties` and carried in `ANNEX.md § Declared ties` |
| `a` | `stellarator_09__stellaris__a` | fan_out | plasma minor radius |
| `availability` | `stellarator_09__stellaris__availability` | fan_out | capacity factor; declared and traced, declined, held at 0.85 |
| `discount_rate` | `stellarator_09__stellaris__discount_rate` | fan_out | discount / interest rate; declared and traced, declined, held at 0.07 |

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `R` | `constraints_reachable` (`net_positive`, `recirc_ok`, `wall_load_ok`; 7/8 objectives, 55 modules fired) | — | swept, search-framed |
| `a` | `constraints_reachable` (same three; 7/8 objectives, 55 modules) | — | swept, search-framed |
| `availability` | `no_constraint_response` (0/6; objectives `cas72`, `fuel`, `lcoe`, `lcoe_1cfe`) | `[OWNER 2026-08-29]` "decline those" | **declined**: not swept, held at 0.85. The "no sensitivity" rationale is carried precedent from `20260821-power-cycle-ab` § 8 `[OWNER-VERBATIM 2026-08-22]`; this study ran no scan of its own |
| `discount_rate` | `no_constraint_response` (0/6; objectives `cas72`, `lcoe`, `lcoe_1cfe`) | `[OWNER 2026-08-29]` "decline those" | **declined**: not swept, held at 0.07. Same carried precedent |

The reach structure is identical to the comparand's at the old pin — same three constraints reachable, same three not, same 7-of-8 objectives. The `p_pump` re-base moved values inside the channel without widening it.

**Not derivable, disclosed in every record.** These are not decidable from the indicator run and no indicator output claims them: monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a *possible* path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output.

**Model-development findings.** Every `no_constraint_response` axis carries one, in addition to the user's ruling. The ruling does not discharge it. Both gaps below were first sighted by the comparand and remain true at this pin; they are cited under their existing ids and not re-minted.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `availability` | Nothing ties the achievable capacity factor to what sets it: CAS72 prices the fluence-limited core replacements, but no coupling makes availability a consequence of core lifetime and replacement outage time. | `20260821-power-cycle-ab#1` (carried, not re-minted) |
| `discount_rate` | The cost of capital is a free multiplier; nothing couples it to construction duration, capital mix, or financing structure. | `20260821-power-cycle-ab#2` (carried, not re-minted) |

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 5 declared keys across 4 groups, all package inputs (`results/preflight_results.json`) |
| Suffix-sibling scan (warnings only) | pass, 0 warnings | no undeclared suffix siblings for any declared group |
| Identity | pass | kind sealed, digest `f97f084818723224bdd7f604a63e1941dadeb3e99af0cca3c9c6d30280d312f0` recomputed from 0 allowed-modified files; every sealed artifact matches (`results/package_identity.json`) |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk (`manifest_currency`) |
| Baseline gate against the pinned headline | pass | `lcoe_calc__lcoe` reproduces at relative deviation 0.000e+00; 6/6 pinned verdicts match (`results/baseline_result.json`) |
| Package cleanliness | pass | package tree byte-untouched (git clean) before execution |

All six ran and all six passed. The gates were run once; no declaration changed after them.

## 10. Execution route and why

- **Route:** study-local direct-API (`study.py` in this directory, over `studies/study_route.py`'s `run_points`: stock `ProvisionalPackageLoader(strict=True)` → `PreparedEvaluator` → `StudyDefinition` with `PreparedListStrategy` → `StudyRunner` → `StudyStore`)
- **Why this route:** the declared tie forces it. `magnet__R0` must carry the same value as `R` in every proposal, and stock teax's `teax-study` CLI builds only a `GridStrategy`, which would cross-multiply the two keys and price coils for machines that do not exist. A tie needs a coordinated proposal list, which is `PreparedListStrategy`. The route loaded and gated at steps 5–6 before this was written.

**Glue disclosure.** glue ledger: none. No adapter on this route, so nothing is harness-supplied. Every value in every proposal is either a swept axis, the declared tie, or a held economic input; every other input is the sealed package's own.

## 11. Study definition and window provenance

**The window was not scanned; it was adopted.** The runbook's step 7 fixes a window from an oracle scan of the candidate range. This study did not do that, by owner ruling (§ 2). The question is where the `recirc_ok` fence *moved*, and a fence position is only subtractable against another fence position measured on the same grid at the same resolution. `20260821-power-cycle-ab` swept R 4.0–20.0 at 0.5 m and a 0.80–2.20 at 0.05 m under the `R > a + 2.25` validity mask, and `study.py` reuses `study_route`'s own `R_VALUES`, `A_VALUES` and `BUILD_STACK_M` rather than restating them, so the two grids are the same object and not merely the same numbers.

**The window is engineered, and what that costs.** `ANNEX.md § Validity masks` states plainly that these bounds are agent-chosen so the constraint boundaries sit in frame, and are not sourced design bounds. Inherited here, that cost is larger than it was for the comparand: at a = 0.80 the `recirc_ok` fence now reaches the window's largest R, so the window no longer contains the fence and this study cannot say where it would lie beyond R = 20 m. The best feasible point likewise sits on the R edge with the objective still falling, so no constrained optimum is claimed (§ 3). A study run inside this window is not testing whether the window is right, and at 195 MW it is visibly no longer wide enough.

**The validity mask** excluded 10 of the 957 grid nodes — a derived geometric bound from held-fixed layer thicknesses (`ANNEX.md § Validity masks`), not a design screen. 947 grid points plus the off-grid baseline point (R 12.7, a 1.3, appended because the LCOE half of the question is asked exactly there) gives 948 proposed.

**The evaluability exclusion, disclosed.** Of those 948, **42 cannot be evaluated at all.** At `p_pump` = 195 MW a region of this window has net electric power below zero, and there the CAS10 land term takes the square root of a negative: the package returns `execution_failed` and the independent oracle returns a complex number. Those points are not worse designs and not infeasible designs — the model has nothing to say there. They were pre-screened out with the package-owned oracle on `p_net > 0` before execution, written to `results/excluded_points.csv` with the `p_net` that put each one there, and the remaining 906 were run.

This is the pattern `20260823-magnet-technology-ab/record.md:224-226` established for that study's density floor — an evaluability limit derived from the oracle and disclosed as a bound rather than a design screen — applied here to a two-dimensional staircase instead of a one-dimensional floor. The staircase, largest excluded `a` at each `R`:

| R (m) | excluded a ≤ | pts | R (m) | excluded a ≤ | pts |
|---|---|---|---|---|---|
| 4.0 | 1.20 | 9 | 7.0 | 0.90 | 3 |
| 4.5 | 1.10 | 7 | 7.5 | 0.85 | 2 |
| 5.0 | 1.05 | 6 | 8.0 | 0.80 | 1 |
| 5.5 | 1.00 | 5 | 8.5 | 0.80 | 1 |
| 6.0 | 0.95 | 4 | 9.0 | 0.80 | 1 |
| 6.5 | 0.90 | 3 | | | |

`p_net` on the excluded set runs from −154.411 MW at (4.0, 0.80) to −0.899 MW at (4.0, 1.20) and (9.0, 0.80); `rec_frac` runs 1.0027 to 1.8787, so recirculating power exceeds gross electric everywhere in it. The boundary is sharp: the smallest `p_net` among the 906 evaluated points is +0.061 MW at (8.0, 0.85).

**The exclusion is itself a result.** The comparand evaluated all 948 of these points at `p_pump` = 1.0 MW and recorded `net_positive` satisfied at every one, naming p_net = 8.3 MW at the (4.0, 0.80) corner. That same corner is −154.4 MW here. The unevaluable region was entirely outside the evaluated space at 1.0 MW and intrudes 42 points into it at 195 MW.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. This study has one arm and one store, under one executable fingerprint and one model-contract fingerprint.

A separate matter, stated here because a reader will ask: the comparison this record draws against `20260821-power-cycle-ab` **does** span fingerprints, and that comparison is not licensed by anything in this record. It is licensed at the goal layer, by the model delta between the two pins being known, audited and single (`p_pump` 1.0 → 195.0, WI-033). This record supplies its own numbers and names the comparand's; it does not certify that the two pins are otherwise identical.

## 13. Verification

Passed. 48 rows sampled stratified by verdict combination across the one store, 10 channels compared against the independent oracle at relative tolerance 1e-9, worst deviation **6.35e-16**. All six constraints re-derived from the oracle's own operands through the published binding table, with operand counts recorded; **zero verdict mismatches**. `not_independently_verified` is empty: every compared channel was recomputed by an implementation that shares no code with the package.

**What verification did not cover.**

- The 42 excluded points. They are not in the store, so nothing about them is verified by this step. Their `p_net` values in `results/excluded_points.csv` are oracle-derived and single-sourced — the package cannot produce a comparison value there, which is the very reason they are excluded.
- `results/oracle_operands.csv` is oracle-derived by construction, not a package-versus-oracle comparison. `pb__p_net`, `pb__rec_frac`, `pb__q_eng`, `pb__p_et` and `pb__p_th` are fields of one multi-field model and the evidence layer records only single-field float channels, so the store holds none of them (`ANNEX.md § Oracle`). Those numbers are the oracle's, labelled as such, and are not independently verified against the package.
- The near-fence re-evaluation across the 130–195 MW band (§ 6) is oracle-only. No package run at 130 or 150 MW exists; producing one would require regenerating the package at a different held value, which is out of this study's scope.
- `p_fus` is not compared by generic `verify.py` — coverage is the manifest's objective catalog plus predicate-resolved operands, and that channel is neither (`ANNEX.md § Oracle`, Item 4 audit).

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing critique | The framing was argued and submitted before any point ran; the reviewer (the orchestrator, carrying to the owner) approved search framing on `R` and `a`, ruled the two `no_constraint_response` axes declined, and ruled the window substitution explicitly rather than letting it pass as a detail. | Accepted as ruled; all four rulings recorded in § 2 before execution. |
| Correctness | Preflight 6/6; verification passed at 6.35e-16 with zero verdict mismatches; the pinned baseline reproduces at exactly 0.000e+00 deviation. | No defect found. |
| Honesty | Two things the run could have quietly swallowed: 42 unevaluable points, and a best-feasible point sitting on the window edge. Both are stated as results with their boundaries, not as footnotes. | Both disclosed in §§ 3 and 11; the window's inadequacy at this pin is stated in § 11 rather than left to inference. |
| Comparability | The comparison against `20260821-power-cycle-ab` spans fingerprints, and this record cannot license it. | Scoped explicitly in § 12: the record supplies numbers, the goal layer supplies the licence. |
| Completeness of the fence claim | At a = 0.80 the fence reaches the window's largest R, so the fence is not bounded in R by this study. | Stated in § 6 and § 11 as a limit of the window, and in § 17 as a fact the record does not contain. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260829-p-pump-fence#1` | model | At `p_pump` = 195 MW the region where `net_positive` cannot be observed intrudes 42 points into the comparand's standard (R, a) window — the mechanism is `20260823-magnet-technology-ab#1` (the CAS10 land term's `sqrt(p_net)` fails before the constraint is evaluated), but at 1.0 MW that region lay entirely outside the evaluated space, and it now overlaps the design space studies actually sweep. | Excluded and disclosed as an evaluability bound (§ 11); the underlying mechanism stays routed under `20260823-magnet-technology-ab#1` and is not re-minted here. | modeling item — the guard needs to survive a net-negative point |
| `20260829-p-pump-fence#2` | model | The adopted window no longer contains the `recirc_ok` fence: at a = 0.80 every R from 4.0 to 20.0 m violates, so the fence's extent in R is unbounded by this study, and the best feasible point sits on the R edge with the objective still falling. | Stated as a window limit (§ 11) and as a missing fact (§ 17); no constrained optimum claimed. A study that needs the fence's R extent at 195 MW must widen the window. | runbook step 7 — an inherited window needs a re-check that the fence is still in frame |
| `20260829-p-pump-fence#3` | process | `ANNEX.md § Baseline pin` restates the pinned headline as a literal (`275.2642200420774`) alongside the sentence saying the pin data lives in `manifest.json`. The value went stale when the package was re-pinned and nothing detected it — no test reads it. | Filed, not fixed by this study; the annex is package documentation, not a study artifact. | documented seam — `exploration/stellarator_e2e/studies/ANNEX.md` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `f59a698e611c36fca7e893d4b2fc3f34c6c542e227fdf47990d4d8e5e701eeea`
- **Schema version:** `study-record-snapshot/v1`

No snapshot content is restated here.

## 17. What this record does not contain

- **Where the `recirc_ok` fence lies in R at a ≤ 0.85.** The window stops at R = 20.0 m and the fence has not closed there. The table in § 6 reports "violated up to R = 20.0" at a = 0.80, which is the window's edge and not a fence position.
- **A constrained LCOE optimum.** The best feasible point is on the window's R boundary with the objective still decreasing (§ 3). The number 225.725 $/MWh is the best point *in this window*, not a minimum.
- **Anything about the 42 excluded points beyond their `p_net` and the reason.** No LCOE, no capital, no verdicts — the package produces none of it there.
- **Any package-side number at `p_pump` other than 195 MW.** The 130 and 150 MW figures in § 6 are the independent oracle's, used for a margin statement, and no package run exists at those values.
- **A comparand re-run.** The 1.0 MW numbers throughout are quoted from `20260821-power-cycle-ab/record.md` at its own pin. This study did not re-execute it, and a difference attributable to anything other than `p_pump` would not be visible here.
- **Any claim about `availability` or `discount_rate`.** Both were declared, traced and declined; this study ran no scan of either and the comparand's oracle-scan numbers are that record's, not this one's.
- **Monotonicity claims from the indicator run.** See § 8.

---

**END OF RECORD**
