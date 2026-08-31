# Study record — 20260830-stress-fence

Contract: `.claude/skills/run-study/record-template.md`; rules: `modeling_project/STUDY_POLICY.md`. Sections 3, 4, 6, and 9–17 are filled at their runbook steps; placeholders are cleared before commit.

## 1. Study header

- **Study id:** `20260830-stress-fence`
- **Package:** `stellarator_tea`
- **Date executed:** `2026-08-30`
- **Executor:** goal `magnet-closure` round 1 agent (T-005), Claude session 2026-08-30
- **Mode:** execute
- **Arms:** `arm-grid-R-I` (R × I_coil design search), `arm-transect-wp-side` (1-D coil-sizing transect)

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> "Intended study question: where does the new structural fence bind in (R, a, B) space, and do feasibility and the constrained optimum move once field is derived rather than cited?" — the round strategy revision (`work/orchestration/goals/magnet-closure/trail.md` § Round 1); pursued under the owner's in-session delegation, verbatim: "yo you are on the goal trajectory, you need to manage it per your best judgement."

Executor's additions, marked as the executor's own: the question's B axis is executed as `I_coil` — WI-035 retired `B` as an entry point, and at fixed geometry the old axis maps linearly onto the new lever (B = k·I). The `a` axis is proposed and *declined*: held at the baseline 1.3 m so the grid is the `20260829-p-pump-fence` comparand's a = 1.3 row and fence positions in R subtract exactly. The "coil sizing" half of the question is executed as a second arm, a 1-D `wp_side` transect at the baseline point, to locate the `wp_stress_ok` flip.

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09__stellaris__lcoe_calc__lcoe` (headline); `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` (1cfe-form comparison)
- **LCOE result:** baseline point (R 12.7 m, I_coil 15.4 MA, wp_side 0.36 m): **304.482 $/MWh**, feasible, sitting on the conductor fence by design (§13). Constrained minimum over the feasible grid: **236.634 $/MWh at (R = 20.0 m, I_coil = 18.0 MA)** — on the `beta_ok` floor, at the R window edge.

Over the feasible region LCOE falls monotonically toward large R along the beta floor (243.1 at R 17.5 → 236.6 at R 20.0, with the best I rising 16.0 → 18.0 MA along it). **Scope (pre-execution critique, MAJOR finding):** the optimum-in-R claim is frame- and model-scoped — the R = 20 corner is the engineered window's edge, and the decomposed magnet capital does not grow with R at fixed I (held `c_coil`; finding `20260830-stress-fence#1`) — so "the optimum sits at large R" is a statement about this package inside this frame, not a design recommendation.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status. Grid = 1,617 points (a = 1.3 m row); transect = 16 points; baseline appended once; 0 points excluded by the evaluability pre-screen.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | violated 586 / satisfied 1031 (grid) | the feasible band's floor at every feasible R; satisfied on all 16 transect points |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied 1617 (grid) + 16 (transect) | never violated in-window; 0 points needed the evaluability exclusion (WI-034 guard still pending) |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | violated 772 / satisfied 845 (grid) | the ceiling for R ≤ 15.0 m; satisfied on the transect |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | violated 392 / satisfied 1225 (grid) | violated at every I for R ≤ 7.5 — the sole killer of the low-R rows; identical per-R to the comparand (99/99 verdict agreement) |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied everywhere | held-vs-held, structurally inert (known, rubric row 2c) |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | satisfied everywhere in-window | the a = 1.3 row; the comparand's wall-load fence lives at other a values |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | violated 660 / satisfied 957 (grid); violated 5 / satisfied 11 (transect) | **the binding ceiling for R ≥ 16.5 m** (shared with `peak_field_ok` at 15.5–16.0); transect flip between 0.28 and 0.30 m |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `I_coil` | search | Two-sided fence structure expected: beta floor from below (beta ~ 1/B² ~ 1/I²), conductor and stress ceilings from above; the constrained optimum is half the question. |
| `R+tie` | search | The comparand's fences (wall load, recirc, net) plus — new since WI-035 — the field-side fences through B ~ I/R; where stress overtakes the conductor ceiling is the sharpest expected claim. |
| `wp_side` | search | The boundary claim is the point: locate the `wp_stress_ok` flip along the coil-sizing lever. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `I_coil` | search | no | A two-sided feasible band materialized at every feasible R (beta floor below, conductor/stress ceiling above), with the constrained optimum on the floor. |
| `R+tie` | search | no | Real fence structure: recirc kills R ≤ 7.5, the band widens with R, and the binding ceiling *changes identity* at R ≈ 16 m — verdict structure throughout. |
| `wp_side` | search | no | The boundary was found where sought: `wp_stress_ok` flips between 0.28 and 0.30 m. |

## 6. Per-axis account

#### `I_coil` — feasible structure (search framing)
**Applies:** yes

At every feasible R the current axis carries a two-sided band: `beta_ok` is the floor (below it the computed field is too weak to hold the plasma pressure ratio — the cheap-low-field escape WI-030 closed, now expressed through the lever itself), and the ceiling is `peak_field_ok` for R ≤ 15.0 m, both ceilings at 15.5–16.0 m, and **`wp_stress_ok` alone for R ≥ 16.5 m**. The band at R 12.7 is I ∈ [11.5, 15.0] MA on the grid (the off-grid baseline 15.4 MA is feasible, on the conductor fence). The constrained optimum sits on the beta floor, never on either ceiling: field still buys only beta margin and magnet capital (no confinement coupling — the standing row-1 gate), so the optimizer runs to the weakest permitted field.

#### `I_coil` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `R+tie` — feasible structure (search framing)
**Applies:** yes

Feasibility begins at R = 8.0 m: for R ≤ 7.5 every point violates `recirc_ok` regardless of I — the field window is open there (2–5 points per row satisfy all three field fences), so the kill is the held-`p_pump` recirculation economics, not the new physics. The three field-independent fences (`recirc_ok`, `net_positive`, `wall_load_ok`) are I-invariant at fixed R and **agree with the `20260829-p-pump-fence` comparand's a = 1.3 row at every one of the 33 R values (99/99 verdicts)** — the WI-035 increment moved none of the fences it should not have moved. What is new is the field-side structure riding on R through the tie (B ~ I/R0): the feasible I band shifts up and widens with R, and the binding ceiling hands over from the conductor limit to the stress limit at R ≈ 16 m. Min-LCOE falls monotonically to the window edge; the optimum-at-the-corner claim is scoped in §3.

#### `R+tie` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `wp_side` — feasible structure (search framing)
**Applies:** yes

The transect at the baseline point locates the `wp_stress_ok` flip **between 0.28 m (835.7 MPa, violated) and 0.30 m (780.0 MPa, satisfied)** — consistent with the closed form 650 × 0.36 / 800 = 0.2925 m. Five of sixteen points are infeasible, all below the flip. This is the executed evidence that the stress limit pushes back on coil sizing (rubric Row 3 P3; SV-039). Caveats carried from §11: `k_sigma` is anchored at 0.36 m and extrapolated in 1/side across the window; and the sizing lever carries no cost consequence (finding `#2`), so the flip is a feasibility statement only.

#### `wp_side` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

## 7. Axis groups

Every declared qualified entry key, with its per-key provenance.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `I_coil` | `stellarator_09__stellaris__magnet__I_coil` | `fan_out` | the WI-035 lever, one magnet-part entry point |
| `R+tie` | `stellarator_09__stellaris__R` | `fan_out` | plant-level major radius |
| `R+tie` | `stellarator_09__stellaris__magnet__R0` | `tie` | same physical quantity as R — declared in the manifest ties (ANNEX § Declared ties); since WI-035 it also carries the field response B ~ I/R0 |
| `wp_side` | `stellarator_09__stellaris__magnet__wp_side` | `fan_out` | worst-coil winding-pack side (WI-035) |
| `a` (declined) | `stellarator_09__stellaris__a` | `fan_out` | held 1.3 m — the comparand row |
| `availability` (declined) | `stellarator_09__stellaris__availability` | `fan_out` | held 0.85 (comparand value) |
| `discount_rate` (declined) | `stellarator_09__stellaris__discount_rate` | `fan_out` | held 0.07 (comparand value) |

## 8. Indicators and rulings

Per proposed axis, including axes proposed and declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `I_coil` | constraints_reachable: `beta_ok`, `peak_field_ok`, `wp_stress_ok`; 6 objectives | not required | swept (arm-grid-R-I) |
| `R+tie` | constraints_reachable: six of the seven (all but `tbr_ok`); 8 objectives | not required | swept (arm-grid-R-I) |
| `wp_side` | constraints_reachable: `wp_stress_ok` only; **zero objectives reachable** | not required | swept (arm-transect-wp-side); the zero-objective trace is finding `20260830-stress-fence#2` |
| `a` | constraints_reachable: `net_positive`, `recirc_ok`, `wall_load_ok` | not required — declined by the executor | held to the comparand row; not executed |
| `availability` | `no_constraint_response` | none needed — declined, not executed | held 0.85; the Row-11 gap already stands committed as `20260821-power-cycle-ab#1` and is not re-minted |
| `discount_rate` | `no_constraint_response` | none needed — declined, not executed | held 0.07; stated nil per §9: a pure finance lever — nothing physical should push back on it, so no model gap is claimed |

**Not derivable, disclosed in every record.** These are not decidable from the indicator run and no indicator output claims them: monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a *possible* path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output.

**Model-development findings.** No swept axis traced `no_constraint_response`. The two axes that did are declined and unexecuted; the availability gap already stands as `20260821-power-cycle-ab#1`, and re-minting it here would duplicate a committed sighting.

## 9. Preflight results

Every mechanical gate ran; outcome **pass** (`results/preflight_results.json`). The identity gate read `results/package_identity.json` and the baseline gate read `results/baseline_result.json`, both deposited by the route at step 5.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 7 declared keys across 6 groups, all package inputs |
| Suffix-sibling scan (warnings only) | pass | none |
| Identity | pass | kind sealed, digest `75f90a24…` recomputed; 0 allowed-modified files, 0 declared sources; every sealed artifact matches |
| Baseline gate against the pinned headline | pass | `lcoe_calc__lcoe` reproduces at relative deviation 0.000e+00; **7/7** pinned verdicts match (`wp_stress_ok` among them) |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk |
| Package cleanliness | pass | package tree byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API definition (`study.py` → `study_route.run_points`: `StudyRunner` + `PreparedListStrategy` on the stock strict loader)
- **Why this route:** the proposals are coordinated axis-group blocks — every point carries the R tie, the held economics, and both arms' keys explicitly — which is the direct-API route's case; the package needs no adapter, and the route was first exercised at step 5 (it loaded, emitted the identity document, and reproduced the pinned baseline) before this rationale was written.

**Glue disclosure.** Glue ledger: none. No adapter on this route, so nothing is harness-supplied; the sealed fingerprint is the identity.

## 11. Study definition and window provenance

The window is **engineered**, chosen after an oracle scan (`results/window_scan.json`): I_coil was scanned 2–29 MA at R ∈ {4.0, 12.7, 20.0} and wp_side 0.20–0.52 m at the baseline. The scan showed the expected two-sided structure in I — a beta floor rising with R (~12 MA at R 12.7, ~18 MA at R 20), the conductor ceiling (~15 MA at R 12.7, ~24 MA at R 20), and the stress ceiling (~17 MA at R 12.7, ~21 MA at R 20) — so the ceilings **cross** inside R ∈ [4, 20]: at R 20 the stress fence sits below the conductor fence. The I window 2.0–26.0 MA (step 0.5) brackets every fence at every scanned R; the wp_side window 0.20–0.52 m brackets the scanned stress flip (between 0.28 and 0.30 m) with the printed per-coil sides 0.30–0.36 m in frame.

The R values are **the comparand's own grid object** (`study_route.R_VALUES`, reused rather than restated — the `20260829-p-pump-fence` precedent), so fence positions in R subtract exactly against that record's a = 1.3 row. a, availability, and discount_rate are held at the comparand's values. The engineered window costs the usual claim: the study tests structure inside the frame, not whether the frame is right.

**Comparability scope (critique finding 2):** "fence positions subtract exactly" holds only for the field-independent fences the comparand measured — `recirc_ok`, `wall_load_ok`, `net_positive`, whose operands the scan shows constant in I at fixed R. The field-side fences (`beta_ok`, `peak_field_ok`, `wp_stress_ok`) have no comparand row, and no single I row reproduces the comparand's cited B = 9.0 T across all R — this is not a matched-field comparison.

**k_sigma validity (critique finding 5):** the stress concentration fact is anchored at wp_side = 0.36 m and the transect applies its 1/side form over 0.20–0.52 m — a held-fact extrapolation, disclosed here; the flip location claim carries it.

**Timing note (critique finding 7):** this section was written after the oracle-only window scan and before steps 5–6 ran; no package point had executed.

An oracle `p_net > 0` evaluability pre-screen runs before execution (the comparand's pattern; the CAS10 land-term defect is WI-034, pending); exclusions, if any, are disclosed in `results/excluded_points.csv` with the oracle-derived `p_net` that put each point there.

**Held-fact caveat, disclosed:** the winding-pack cost's `f_set` (set current distribution) and `c_coil` (25 m circumference) are package-held facts, and `wp_side` carries no cost consequence — so the decomposed magnet capital responds to I_coil but not to R or wp_side. Fence positions are unaffected; cost-response claims along R are made on the retained 1cfe-form comparison channel only.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. Both arms run in one store against one package identity (semantic `819a5a05…`, executable `75f90a24…`, the T-004 candidate); the comparand comparison in §11 is a *cross-record* reading against `20260829-p-pump-fence`, scoped there, and licenses fence-position subtraction in R for the field-independent fences only — never absolute-LCOE comparison across the WI-035 re-baseline.

## 13. Verification

**Outcome: pass** (`results/verification_summary.json`). 12 rows sampled stratified by verdict combination across the single store; 12 channels compared against the package-owned oracle at relative deviation below 1e-9, worst **4.37e-16**; **all seven** catalog constraints re-derived from published operand bindings with zero verdict mismatches; `not_independently_verified` is empty.

What verification did **not** cover: the 1,622 unsampled rows (stratification guarantees every observed verdict combination was sampled, not every point); and the *choice* of the held coil-set facts — the oracle mirrors the model's own `k_link`/`k_sigma`/`f_set` literals, so parity verifies transcription and execution, never the sourcing of those facts (that lives in the WI-035 item record).

**Baseline-on-fence margin statement** (rule `20260823-magnet-technology-ab#11`): the baseline headline sits *on* the conductor fence — `B_peak` = 24.899999999999995 vs `B_max` = 24.9, margin 5.3e-15 T — **by construction**: Stellaris designs its winding to the 24.9 T conductor value, and WI-035 bound `k_link` on the low side deliberately so the design point lands under the ceiling under float64 rounding (design D2). The held values the fence position depends on (`k_link`, `peak_ratio`, `B_max`) are float64 anchors of printed pairs, not sourced bands — both printed sourcings of the coil-set current facts (Table 2 peak-coil basis; Table 8 set-sum basis) collapse to the same anchored values — so no sourced-range re-evaluation can flip the baseline verdict; the ulp-scale margin is disclosed as a design fact, not a robustness claim. The stress fence carries a real margin at baseline (650 vs 800 MPa, 23%).

## 14. Review outcomes

Each named lens, its verdict, and its disposition. The pre-execution framing critique is one of them.

| Lens | Verdict | Disposition |
|---|---|---|
| pre-execution framing critique (independent agent, 2026-08-30, before any point ran) | **FINDINGS — none blocking.** 1 MAJOR: the optimum-in-R claim is confounded by the R-flat decomposed magnet capital (held `c_coil`); 6 minor/info: comparability scope, low-R recirc infeasibility narrative, baseline-on-fence margin duty (rule `20260823-magnet-technology-ab#11`), k_sigma transect validity, discount_rate nil, far-corner heat-map caveat. | MAJOR: caveat restated at the optimum claim site (§3/§6) and the held-`c_coil` gap minted as finding `20260830-stress-fence#3`. Minors: §8 nil added, §11 scope + k_sigma + timing lines added pre-execution; low-R recirc and per-arm H1 reporting owed in §6; the baseline-on-fence margin statement owed in §13/report. |

## 15. Findings

Each finding's id is used verbatim in `DISCOVERY_LOG.md` (`20260830-stress-fence#1`, `#2`).

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260830-stress-fence#1` | `model` | The decomposed magnet capital does not respond to R at fixed I: the winding length is the held `c_coil` = 25 m over a 5× machine-size range (and `f_set` is held), so the optimum-in-R and any R-scaling cost claim ride partly on a cost-decomposition artifact. The winding length should follow coil geometry. | Disclosed at the claim sites (§3, §11); pre-execution critique MAJOR finding, minted here. | `unrouted` — modeling item under the MFE Cost Modeling epic |
| `20260830-stress-fence#2` | `model` | `wp_side` reaches zero objectives: the coil-sizing lever moves only the stress operand — winding-pack and casing costs are sized by other held facts — so escaping the stress fence by enlarging the pack is cost-free, which no real design change is. Coil sizing should enter the winding-pack/structure sizing chain. | Disclosed at the transect claim (§6); indicator trace recorded before execution (§8). | `unrouted` — modeling item under the MFE Cost Modeling epic |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `98209df3ef1326dc4f6d35054ac0cfaa8dad515bf0d04ee5e960eb0d1e4c1efb`
- **Schema version:** `1`

No snapshot content is restated here.

## 17. What this record does not contain

- The per-point store (`_work/20260830-stress-fence/20260830-stress-fence.db`) is beside, not inside, the record directory and is not committed; its path and compatibility tuple are in `snapshot.json` (`stores[0]`), and `results/points.csv` + `results/oracle_operands.csv` carry the committed per-point evidence.
- No (R, a) plane: `a` is held at 1.3 m throughout, so nothing here locates the wall-load fence or reproduces the comparand's two-dimensional structure.
- No availability or discount-rate response (declined, held).
- No magnet-capital response to R at fixed I — absent by construction (finding `#1`), so this record cannot support R-scaling claims about the decomposed magnet cost.
- No absolute-LCOE comparison against any pre-WI-035 record: the headline re-based (333.067 → 304.482 at the baseline) when the magnet account decomposed; only per-R verdicts of the three field-independent fences subtract against the comparand.
- No confinement response to field: B still reaches beta and the magnet accounts only (standing row-1 gate), so "the optimum sits on the beta floor" is a fact about this package, not about stellarator physics.
