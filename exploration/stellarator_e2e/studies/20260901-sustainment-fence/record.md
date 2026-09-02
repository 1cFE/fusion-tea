# Record — 20260901-sustainment-fence

## 1. Study header

- **Study id:** `20260901-sustainment-fence`
- **Package:** `stellarator_tea`
- **Date executed:** 2026-09-01
- **Executor:** goal `operating-point-closure` round-2 agent (T-005), owner-delegated session
- **Mode:** execute
- **Arms:** `arm-grid-I-ne`, `arm-transect-T`, `arm-transect-p-input`

Arms are variants of the same question, run to be compared. Two studies asking different
questions of the same package are two records, not two arms of one.

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> "Intended study question: with the sustainment fence active, is field rewarded — does the constrained optimum leave the beta floor (the `20260823-magnet-technology-ab#4` pathology) — and where do the power, beta, wall-load, conductor-ceiling, and stress fences bind over (I_coil/B, n_e0, T_i0) and geometry, i.e., is the three-way trade of L-003 visible in a committed study?"

Provenance of the quote: the round-2 strategy revision, authored by the round-1 fresh reviewer under the owner's 2026-09-01 full delegation ("take ownership and accountability, and execute the entire goal" — `work/orchestration/goals/operating-point-closure/trail.md` § Owner directive, § Round 2). The owner set the goal and delegated; the strategy text is the closest thing this study has to the user's own words, and it is quoted verbatim.

Executor's additions to make it executable (mine, not the quote's): geometry is held at the baseline machine (R = 12.7, a = 1.3, wp_side = 0.36) rather than swept — the (R, a) fence structure is `20260829-p-pump-fence`/`20260830-stress-fence` territory and re-sweeping it here would spend the round's one study re-measuring known structure; the field lever I_coil carries the "is field rewarded" question directly. The three arms: an (I_coil × n_e0) design-search grid at the baseline operating point, a T_i0 transect (the committed form of round 1's required-aux curve), and a p_input transect with the newly declared p_ecrh tie (where does installed heating satisfy sustainment, and what does buying it cost). Sustainment held facts (iota_23, f_ren, f_alpha_fast, tau_ratio_ash, f_suppr_ash, Z_eff_core, f_W_core, Ti_over_Te) are package-held sourced values, not swept; an f_ren sensitivity is named future work. Further held facts that shape the fence positions, disclosed per the pre-execution critique (findings 6–7): the profile exponents (alpha_n, alpha_n_e, alpha_T) and the synchrotron facts (kappa_sync, R_w_sync) are package-held; the legacy entry key `n_e` (vol-av, 3.17e20) is a physical sibling of the swept `n_e0` that feeds only the fusion calc's 0D bypass and is inert here solely because `sigma_v = 0` — no tie is needed only while the bypass is off; and the baseline sits at exact equality on the conductor ceiling (B_peak 24.90 = B_max 24.9 by the WI-035 one-ulp-low convention), so at 50 MW installed there is zero field headroom by construction — a design-point fact, not a discovery of this study. Grid slice 2 (p_input = 110 MW) was added on the critique's finding 1 so the optimum question is answerable; screened-out points count as infeasible-by-exclusion in every feasible-fraction denominator, and "net_positive never violated among evaluated points" is barred phrasing (finding 3).

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09__stellaris__lcoe_calc__lcoe` (with `lcoe_1cfe` recorded alongside)
- **LCOE result:** best **feasible** point: **293.468 $/MWh** at (I_coil 15.0 MA, n_e0 1.1× = 5.566e20, T_i0 14.63 keV, p_input 110 MW) — `arm-grid-I-ne-p110`, case in `results/points.csv`. Baseline (p_input 50): 307.087 $/MWh, `sustainment_ok` violated, infeasible.

The objective spans 127.8–112,220 $/MWh over the 334 evaluated points (the top end is deep-infeasible low-power territory); among the nine feasible points across all arms it spans 293.5–415.3. The headline structural result: at the printed installed heating (50 MW) **no evaluated or excluded point is feasible** — the pre-registered empty set — while at 110 MW a four-point feasible region exists whose best member beats the baseline headline by 4.4% despite buying 2.2× the heating, because it runs denser (1.1×) at slightly lower field with p_fus 3270 MW. The feasible optimum's beta is **0.0311 against the 0.05 limit — off the beta floor**: its I-range is bounded below by `sustainment_ok` (I ≥ 15.0 MA) and above by the conductor ceiling (I ≤ 15.4 MA), not by `beta_ok`. Field is rewarded through confinement, and the fence that stops it is magnet technology, not plasma stability — the `20260823-magnet-technology-ab#4` pathology inverted.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | violated 219/334 | the new WI-037 power fence; satisfied only at I ≥ 18 MA (p=50, over-ceiling), in a 15–21 MA band at p=110, and at p ≥ 100 on the transect; never satisfied in T at 50 MW |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | violated 155/334 | the conductor ceiling B_peak ≤ 24.9 T binds at I > 15.4 MA — every point where field could buy sustainment relief past the baseline |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | violated 119/334 | σ ∝ I·B_peak: breaks at I ≥ 18 MA at wp_side 0.36 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | violated 101/334 | low-output points (low I or low n) with the fixed wallplug burden; at p=110 the 220 MW wallplug pushes the low-n columns over 0.5 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | violated 96/334 | n ≥ 1.2× columns and T ≥ 17 keV on the transect |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | violated 69/334 | low-field columns (I ≤ 11 MA at baseline density) and T ≥ 28 keV |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | violated 0/334 | never violated **among evaluated points by construction** — the pre-screen excludes p_net ≤ 0 (10 points), which count as infeasible-by-exclusion (§ 2, § 8); the fence's true boundary is the exclusion edge |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | violated 0/334 | held-vs-held, structurally inert on these axes (the standing Row-2c finding; unchanged by WI-037) |

A short display name is not a qualified identity. If the executed artifacts carry only
the short name, the qualified identity was dropped on export and recovering it is part
of this section, not optional.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `I_coil` | search | The field lever: where the sustainment relief (loss ~ B^-2.15), the conductor ceiling, and the stress ceiling carve feasibility. Run as two grid slices (critique finding 1): at the baseline installed heating 50 MW — where pre-execution probes predict the feasible set is EMPTY (sustainment vs ceiling exclude each other's relief; the baseline sits at exact ceiling equality with zero field headroom) and the pre-registered claim is that emptiness with its fence anatomy, reported per H1 as the first-order finding — and at 110 MW (above the ~91 MW flip), where a live feasible region lets the constrained-optimum question ("does it leave the beta floor?") be answered. |
| `n_e0` | search | Paired grid axis on both slices: density trades alpha power (~n^2) against conducted loss (~n^1.38) and wall load; the feasible region's density edge is the claim. |
| `T_i0` | search | Pre-execution probes (critique finding 4) predict NO sustainment crossing in-window (required aux bottoms ~72–74 MW > 50 across T ∈ [6,30]): the arm's search structure is the wall-load fence (~T ≈ 16), the beta fence (~T ≈ 28), and the location of the required-aux minimum — the committed form of round 1's curve, with the no-crossing result pre-registered. |
| `p_input+tie` | search | Finds the installed-power threshold where `sustainment_ok` flips (probe-predicted ~91 MW) and what the heating account charges for it (the p_ecrh tie rides). |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `I_coil` | search | no | the run delivered the claimed structure: the p=50 slice is empty exactly as pre-registered, and the p=110 slice has a bounded feasible band in I with a constrained optimum |
| `n_e0` | search | no | the density edge exists (wall load at 1.2×, recirc at ≤0.8× under the 110 MW wallplug) and the optimum sits at 1.1× |
| `T_i0` | search | no | pre-registered no-sustainment-crossing confirmed; the wall (17 keV) and beta (28 keV) fences and the required-aux minimum (T ≈ 18) were located |
| `p_input+tie` | search | no | the installed-power threshold was found between 90 and 100 MW (oracle: ~91), with the cost of buying it priced by the tie |

## 6. Per-axis account

One pair of subsections per axis. Both ship present; the `**Applies:**` line
discharges the one the axis's framing does not owe.

#### `I_coil` — feasible structure (search framing)
**Applies:** yes

At p_input = 50 (154 points incl. baseline): **feasible set empty.** Below the ceiling every point violates `sustainment_ok` (required ≈ 72–139 MW vs 50); at I ≥ 16 MA the ceiling (`peak_field_ok`) and then stress (I ≥ 18) take over — 29 points do satisfy sustainment (I ≥ 18 MA) but all sit over the ceiling: **the sustainment fence and the conductor ceiling exclude each other's relief at this machine and installed power.** At p_input = 110: the feasible band in I is [15.0, 15.4] MA — bounded below by `sustainment_ok`, above by `peak_field_ok` at 15.4 → 16.0 — with the constrained optimum at I = 15.0 MA, LCOE 293.468, beta 0.0311 (the beta fence inactive at the optimum; beta binds only at I ≤ 11 MA). The oracle scan additionally shows the sustainment relief is **non-monotonic in field** (satisfied 18–21 MA, lost again at 22 at p=50 — the Albajar synchrotron term, ~B^2.62, reclaims the confinement gain; `results/window_scan.json` I-edge).

#### `I_coil` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `n_e0` — feasible structure (search framing)
**Applies:** yes

At p=110, the feasible density band at I = 15.0 MA is [0.9×, 1.1×]: below it `recirc_ok` breaks (the 220 MW wallplug against shrinking output); above it `wall_load_ok` breaks at 1.2× (wall load crosses 4.05). The optimum sits at the top of the band (1.1×) — denser is better until the wall says no, because fusion power ~ n² outruns the fixed costs. At p=50 no density is feasible at any I (the sustainment/ceiling deadlock above).

#### `n_e0` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `T_i0` — feasible structure (search framing)
**Applies:** yes

No feasible point on the transect (pre-registered): `sustainment_ok` is violated at every T ∈ [9, 30] (required aux bottoms at ≈ 72.6 MW near T = 18 — `results/oracle_operands.csv`), with `recirc_ok` additionally violated at T ≤ 11 (low output), `wall_load_ok` from T = 17, and `beta_ok` from T = 28. T = 6–8 keV excluded by the fail-loud pre-screen (oracle p_net complex through the CAS10 land term; `results/excluded_points.csv` carries their converged sustainment operands). The committed form of round 1's required-aux curve, with both fence crossings located.

#### `T_i0` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `p_input+tie` — feasible structure (search framing)
**Applies:** yes

`sustainment_ok` flips between 90 and 100 MW installed (oracle threshold ≈ 91 MW = the baseline required aux + margin); p ∈ [100, 150] is fully feasible at baseline levers with LCOE rising strictly from 354.3 to 415.3 — installed heating is pure cost once sustainment is met (heating capital through the p_ecrh tie plus the p/η_pin wallplug recirculation). The cheapest route to feasibility in the whole study is therefore not more heating at the printed operating point but the p=110 grid's denser, slightly-lower-field optimum at 293.5.

#### `p_input+tie` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

## 7. Axis groups

Every declared qualified entry key, with its per-key provenance.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `I_coil` | `stellarator_09__stellaris__magnet__I_coil` | fan_out | one plant-level entry point |
| `n_e0` | `stellarator_09__stellaris__n_e0` | fan_out | one plant-level entry point |
| `T_i0` | `stellarator_09__stellaris__T_i0` | fan_out | one plant-level entry point |
| `p_input+tie` | `stellarator_09__stellaris__p_input` | fan_out | installed plasma-coupled ECRH power |
| `p_input+tie` | `stellarator_09__stellaris__p_ecrh` | tie | same physical quantity — the heating account's installed ECRH power; declared by this study (manifest `ties`, annex § Declared ties) when installed heating first became a swept axis; formerly the annex's known held-fixed semantic duplicate |

Held keys asserted per case by the driver (`study.py`): R (+R0 tie), a, availability, discount_rate, wp_side.

## 8. Indicators and rulings

Per proposed axis, including axes proposed and declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `I_coil` | constraints_reachable (7: beta_ok, net_positive, peak_field_ok, recirc_ok, sustainment_ok, wall_load_ok, wp_stress_ok) | not required | swept. WI-037 extended the field lever's reach from 3 constraints to 7 — the first study on a package where the field has a path to fusion power. |
| `n_e0` | constraints_reachable (5) | not required | swept. First study ever to sweep a density lever on this package. |
| `T_i0` | constraints_reachable (5) | not required | swept. First study ever to sweep a temperature lever (T was a held referent in every prior record). |
| `p_input+tie` | constraints_reachable (3: net_positive, recirc_ok, sustainment_ok) | not required | swept. Installed heating now has physics consequence (it was recirculation-only before WI-037). |
| `R+tie` | constraints_reachable (7) | not required | **declined** (traced per runbook step 3, critique finding 2): geometry structure is `20260829-p-pump-fence`/`20260830-stress-fence` territory; re-sweeping it would spend the round's one study re-measuring known structure. Declared at full group completeness (R + the R0 tie). |
| `a` | constraints_reachable (5) | not required | **declined** (traced): same grounds. |

No axis — swept or declined — reported `no_constraint_response`; no ruling was required. This is itself a WI-037 result: every operating-point lever now has pushback (STUDY_POLICY §9's demand — the committed `no_constraint_response` findings of `20260821-power-cycle-ab` do not recur on these axes; `availability` remains the standing counterexample and was not proposed here — it is Row 11's finding, out of this goal's scope).

**Not derivable, disclosed in every record.** These are not decidable from the
indicator run and no indicator output claims them: monotonicity of any channel in any
axis; identity of the same physical quantity across differing key names; intra-module
operand dependency. `constraints_reachable` is a *possible* path and never a statement
that a constraint responds. `unresisted` is the agent's recorded judgment, never a
tool output.

**Model-development findings.** Every `no_constraint_response` axis carries one, in
addition to the user's ruling. The ruling does not discharge it.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| — | not applicable: no swept axis reported `no_constraint_response` | — |

## 9. Preflight results

Every mechanical gate that ran, with its outcome. The identity and baseline gates
read the documents the route-preparation step deposited in `results/`; name those
files in the detail column so a cold reader can open what the gate read. A gate that did not run is stated as
such with its condition.

Every mechanical gate ran; outcome **pass** (`results/preflight_results.json`). The identity gate read `results/package_identity.json` and the baseline gate read `results/baseline_result.json`, both deposited by the route at step 5.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 8 declared keys across 6 groups (4 swept + 2 traced declined), all package inputs |
| Suffix-sibling scan (warnings only) | pass | none |
| Identity | pass | kind sealed, digest `41e06ecb…` recomputed; every sealed artifact matches |
| Baseline gate against the pinned headline | pass | `lcoe_calc__lcoe` reproduces at rel 0.000e+00; **8/8 pinned verdicts match, `sustainment_ok` violated as pinned** |
| Manifest / package fingerprint match | pass | both recorded fingerprints match the package on disk |
| Package cleanliness | pass | byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API definition (`study.py` → `study_route.run_points`: `StudyRunner` + `PreparedListStrategy` on the stock strict loader)
- **Why this route:** the proposals are coordinated axis-group blocks — every point carries both declared ties (R0 with R; p_ecrh with p_input), the held machine keys, and all four operating-point levers explicitly, and the four arms interleave two grid slices and two transects — which is the direct-API route's case; the package needs no adapter, and the route was first exercised at step 5 (it loaded, emitted the identity document, and reproduced the pinned baseline with all eight verdicts) before this rationale was written.

The rationale is recorded after the route was first exercised and gated, so it accounts
for a route already known to load rather than predicting one.

**Glue disclosure.** What the harness supplies that the model does not, and what that
means for the claims. The ledger's entries are values and live in `snapshot.json`
under `glue_ledger`; this is the argument about them.

Glue ledger: none. No adapter on this route, so nothing is harness-supplied; the sealed fingerprint is the identity.

## 11. Study definition and window provenance

The candidate ranges were scanned with the independent oracle (`scan.py` → `results/window_scan.json`) along the two grid edges and both transects before any bound was fixed. The scan showed every fence crossing inside the frame: on the I edge at baseline (n, T, p=50) — wall load clears at 10→11 MA, beta clears at 11→12 MA, the conductor ceiling breaks at 15→16 MA, stress at 17→18 MA, and `sustainment_ok` flips satisfied at 17→18 MA then back violated at 21→22 MA (the synchrotron term, ~B^2.62, reclaims the relief — a non-monotonic sustainment window the grid must keep in frame); on the n edge — wall load breaks at 1.1×→1.2×; on the T transect — wall load at 16→17 keV, beta at 27→28 keV, with T = 6–8 keV raising the oracle's fail-loud exception (the low-T radiation barrier drives p_net complex through the CAS10 land term; recorded, screened, disclosed); on the p transect — sustainment flips at 90→100 MW. The bounds were then fixed to hold all of these crossings with margin on both sides; the 110 MW grid slice sits above the sustainment flip per the pre-execution critique's finding 1.

The window is **engineered**. The usual cost applies: the study tests structure inside the frame, not whether the frame is right — and the T and I windows deliberately include regions where the oracle's fail-loud chain excludes points, counted as infeasible-by-exclusion in every denominator (§ 2, § 8).

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. All four arms ran in one store against one sealed executable (`41e06ecb…`) at one semantic fingerprint (`5b9abdfc…`), the T-004 candidate pin `35e922c5…`. Comparisons against the pre-WI-037 records (`20260830-stress-fence` and earlier) cross a semantic boundary — the operating point moved from held to computed-fuel (baseline p_fus −0.83%, LCOE +0.86%) — and any such comparison in the synthesis must say so; none is made in this record.

## 13. Verification

Pass: 21 sampled rows covering all 21 observed verdict combinations (the stratification cannot miss a verdict this study produced), 12 channels at relative deviation below 1e-9 with worst 5.33e-16, and all eight constraints re-derived from the oracle's own operands — `sustainment_ok` among them, with both operands resolved (the computed `p_aux_required` from the oracle's sustainment mirror against the `p_input` input key).

Not covered, named: the six sustainment quantities exported in `results/oracle_operands.csv` (p_aux_required, tau_E, p_rad, n_He0, n_D0, W_th) are **oracle-derived on both sides** — the store cannot record them (fields of one multi-field model, the pb__* precedent), so their CSV values are not independently verified against a store channel; what IS independently verified is the `sustainment_ok` verdict they feed, re-derived per sampled row. `p_fus` remains outside generic verification coverage (the standing annex delta). The 10 pre-screen exclusions were never executed, so nothing about them is verified beyond the oracle's own refusal.

## 14. Review outcomes

| Lens | Reviewer | Verdict | Disposition |
|---|---|---|---|
| Pre-execution framing critique (runbook step 4) | fresh non-author session, spawned 2026-09-01 (full text deposited at `work/orchestration/goals/operating-point-closure/evidence/T-005_precritique.md`) | **MAJOR** — 3 major, 4 minor findings | All seven dispositioned before any point ran: (1) second grid slice at p_input = 110 MW added so the constrained-optimum question is answerable, with the p = 50 slice's predicted empty feasible set pre-registered as an H1 first-order finding; (2) R+tie and a declared as traced declined groups and indicators re-run over all six; (3) excluded points now carry the oracle-side sustainment operands, and screened points count as infeasible-by-exclusion in every denominator ("never violated among evaluated points" barred); (4) the T-row framing rewritten to pre-register no sustainment crossing in-window; (5) `ANNEX.md § Baseline pin` corrected to the WI-037 manifest facts; (6) held-fact disclosures added (`n_e` bypass sibling, profile exponents, sync facts; recirc threshold read from the package); (7) the baseline's exact ceiling equality stated as a design-point fact. |



Each named lens, its verdict, and its disposition. The pre-execution framing critique is the table above; the post-run lenses:

| Lens | Verdict | Disposition |
|---|---|---|
| Correctness (executor pass) | pass with one corrected defect | the first export shipped six empty sustainment columns (finding #3); corrected pre-commit by the oracle-side re-export, with the store's multi-field limitation named in § 13 and the ANNEX. Preflight, verification, and the baseline gate all pass at rel ≤ 5.33e-16. |
| Honesty (executor pass) | pass | the p=50 emptiness was pre-registered, its H1 reading is the first-order claim (not boundary-mapping success); denominators include exclusions; the barred phrasing (§ 2) is avoided; the engineered window's cost is stated (§ 11); comparisons across the WI-037 semantic boundary are barred in-record (§ 12). |
| Readability (executor pass) | pass | every § 3/§ 6 number traces to `results/points.csv`, `oracle_operands.csv`, or `window_scan.json`; fence claims name the constraint by qualified identity in § 4. |

The fresh administrator's synthesis is the reading of record; these are the executor's own lenses and claim no independence.

## 15. Findings

Four findings; ids joined verbatim to `DISCOVERY_LOG.md` rows.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260901-sustainment-fence#1` | `model` | At the printed installed heating (50 MW) the baseline machine has **no feasible operating point anywhere in the swept space**: below the conductor ceiling every point fails sustainment (required ≥ ~72 MW), and every sustainment-satisfying field sits over the ceiling/stress fences — the deadlock is between the ISS04 relief (~B^-2.15) and the held conductor grade (B_max 24.9, a sourced REBCO fact). Feasibility returns at ≥ ~91 MW installed or, presumably, at a different conductor grade — the unswept axis. | First-order H1 reading, pre-registered before execution; carried to the goal round result and the synthesis. | goal `operating-point-closure` round result; candidate follow-on: a conductor-grade (B_max) arm study or a heating-system item |
| `20260901-sustainment-fence#2` | `model` | The CAS10 land term (√p_net) re-sighted: 10 points (T ≤ 8 keV and deep low-power corners) fail to evaluate before any verdict is written — the third committed sighting of the WI-034 defect, now on the temperature axis. | Excluded-by-pre-screen with converged sustainment operands exported; counted infeasible-by-exclusion in every denominator. | modeling item `WI-034` (backlog; standing) |
| `20260901-sustainment-fence#3` | `process` | The sustainment quantities are fields of one multi-field module and do not reach the evidence store — exactly the pb__* limitation; the first export shipped six empty columns before the oracle-side re-export (corrected pre-commit). | `points.csv` carries no sustainment columns; `oracle_operands.csv` carries them oracle-labelled; ANNEX § Oracle already documents the pattern and now names `sustain__*` in it. | documented seam, `ANNEX.md § Oracle` |
| `20260901-sustainment-fence#4` | `model` | Installed heating is pure cost once sustainment is met (LCOE strictly rising in p on the transect): the heating account is per-MW capital with no system structure (sources, transmission, launchers) and heating buys nothing but the sustainment verdict and recirculation burden — a heating-system model (rubric Row 4, whose P3 was deferred pending Row 1) would change the trade. | Disclosed at the claim site (§ 6); the Row 4 target note ("rides on row 1") is now unblocked by this goal. | unrouted — future goal/item at rubric Row 4 |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling
item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `5bf3cfba5880d29229dbce6e0049bc48c6f040a8fb975f0a1d1fa86956e7a0ae`
- **Schema version:** 1

No snapshot content is restated here.

## 17. What this record does not contain

- **No geometry sweep.** R and a are traced declined groups (§ 8); nothing here locates the sustainment fence in machine size. The p110 optimum is an optimum of this machine at this installed power, not of the design space.
- **No sustainment-fact sensitivities.** iota_23, f_ren, and the radiation-model facts are held at their sourced values; the fence positions carry their uncertainty undisplayed (f_ren = 1.0 is the printed Stellaris assumption, and the round-1 evidence shows the balance residual is dominated by the model's own W-form +9.2%). A ±f_ren arm would move the ~91 MW threshold materially; none was run.
- **No per-point sustainment values in the store.** The store carries verdicts and single-field channels only; the sustainment operands exist in `results/oracle_operands.csv` (oracle-derived, § 13) and nowhere else.
- **No claim about the excluded band's physics.** T ≤ 8 keV died on the CAS10 evaluability defect, not on a physical verdict; the record does not say what that band would have read.
- **The store itself is not committed** (`20260821-power-cycle-ab#11` convention); `snapshot.json` carries its compatibility tuple and the committed CSVs carry the per-point evidence.
- **The T = 8.32 up-crossing of round 1's driven analysis is not re-exhibited** — the transect starts at 9 keV after exclusions; the unstable-branch reading rests on `oracle_operands.csv`'s monotone-falling required-aux from 9 → 18 keV plus round 1's deposited analysis, not on a committed sub-9-keV point.

---

**END OF RECORD**

---

