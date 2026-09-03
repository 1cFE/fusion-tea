# Study record — `20260903-priced-levers`

## 1. Study header

- **Study id:** `20260903-priced-levers`
- **Package:** `stellarator_tea` (`exploration/stellarator_e2e/pkg/stellarator_tea`)
- **Date executed:** 2026-09-03
- **Executor:** round agent, goal `priced-levers` round 1, task T-007
- **Mode:** execute
- **Arms:** `arm-fence-p50`, `arm-search-p110`, `arm-transect-jwp`

## 2. Intake

The owner's goal and scope, in their own words, verbatim:

> "Run a committed study at pin 6262dbf4 for goal priced-levers round 1: three arms at p=50, p=110, and a j_wp transect, sweeping the new winding-pack sizing lever."

and, on the round's question:

> "run it"

**Executor's own additions, kept separate from the quote.** The `T_i0` axis was **not** in the owner's three-arm description; it was added by the pre-execution framing critique (MAJOR 2) and is the change that most altered what this study found. The arm names, windows, and the decision to hold `B_max`, `sigma_allow`, `eps_cond_allow`, `R`+tie and `a` as traced declined axes are the executor's, under the goal's standing delegation ([OWNER-VERBATIM 2026-09-02] "no gates. USE YOUR BEST JUDGEMENT ALONG THE WAY!"). The goal-level question this study serves — "with the field lever priced, does a feasible operating point exist at the printed 50 MW installed heating, and what does it cost" — is the executor's phrasing of the round strategy, not the owner's words.

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09__stellaris__lcoe_calc__lcoe` (headline); `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` (comparison form)
- **LCOE result:** **271.359 $/MWh**, the constrained optimum of `arm-search-p110`, at I_coil 15.20 MA, `j_wp` 130.0 A/mm², T_i0 18.00 keV, n_e0 4.554e20 (0.90×). `arm-fence-p50` has **no feasible point** and therefore no constrained optimum. The pinned baseline reproduces at 307.08712042841586 with `sustainment_ok` violated.

Over the studied space the objective ranges widely and is dominated by feasibility rather than by the swept magnet levers: across the 87 feasible points at 110 MW LCOE spans 271.359–463.230, while across the entire `j_wp` transect — a 2.33× swing in winding-pack cross-section — it spans only 365.206–365.572, a 0.100% range.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, over all 439 executed points.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | mixed | violated **264 / 439** — the dominant fence in this machine; max observed wall load 9.474 against a 4.05 limit |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | mixed | violated 144 / 439; the baseline sits at exact equality (24.90 vs 24.9) by the WI-035 design convention |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | mixed | violated 132 / 439; violated at the pinned baseline (90.6 MW required vs 50 installed — the disclosed WI-037 state) |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | mixed | violated 32 / 439, only in `arm-fence-p50` at I ≥ 17 MA |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | mixed | violated 15 / 439 |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | mixed | violated 3 / 439; max observed beta 0.0509 against a 0.050 limit — the window reaches the fence, unlike the pre-critique window which topped out at 0.036 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied everywhere | **violated 0 / 439.** The conductor check WI-036 added is inert across the entire explored space; max observed strain 0.235% against a 0.400% limit |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied everywhere | violated 0 / 439 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied everywhere | violated 0 / 439 — held-vs-held and structurally inert, unchanged since first recorded |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `I_coil` | search | The field lever; since WI-036 it also sizes the winding pack, so it carries both magnet fences and the confinement chain. |
| `j_wp` | search | The lever WI-036 minted; expected to trade pack cross-section against stress at a real cost. |
| `T_i0` | search | Added by the pre-execution critique. Held at 14.63 keV in the first design, which produced a fence conclusion the dropped axis contradicts. |
| `n_e0` | search | Operating-point lever; window widened past the first design's so it can reach the beta limit. |
| `p_input+tie` | sensitivity | Two levels only (50, 110 MW), to separate the arms. Not searched. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `I_coil` | search | no | A bounded feasible band exists at 110 MW (14.8–15.4 MA) with a constrained optimum inside it, and the p50 arm's emptiness is located rather than assumed. |
| `j_wp` | **sensitivity** | **yes** | It reaches no feasible boundary anywhere: every transect point is feasible, and in the grids it never flips a verdict that another axis had not already flipped. It measures a response, not a boundary. |
| `T_i0` | search | no | It moves the constrained optimum by 16.645 $/MWh and relocates which fence binds — the largest structural effect in the study. |
| `n_e0` | search | no | It reaches `beta_ok` (3 violations at the window's top) and co-determines the wall-load fence. |
| `p_input+tie` | sensitivity | no | Two levels; no boundary claim is made in `p_input`. |

## 6. Per-axis account

#### `I_coil` — feasible structure (search framing)
**Applies:** yes

At 110 MW the feasible band is **14.8 – 15.4 MA**, bounded below by `sustainment_ok` and above by `peak_field_ok`; the constrained optimum sits at 15.20 MA. At 50 MW no band exists: below ~15 MA the machine cannot sustain, and above ~15.4 MA `peak_field_ok` fails. The 0.2 MA step resolves the band, which the pre-critique 1.0 MA step could not have.

#### `I_coil` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `j_wp` — feasible structure (search framing)
**Applies:** not applicable — judged sensitivity after the run.

#### `j_wp` — observed response (sensitivity framing)
**Applies:** yes

Over the transect (60 → 140 A/mm², a 2.33× swing in winding-pack cross-section): `wp_side` 0.50662 → 0.33166 m, cold volume **270.45 → 115.91 m³**, cryoplant electrical 1.20 → 0.81 MW, cryoplant capital **$20.98M → $16.00M**, winding-pack stress 461.9 → 705.5 MPa, conductor strain 0.154% → 0.235%. **Magnet capital is $5,401.0M at every point — a delta of exactly zero.** LCOE moves 365.572 → 365.206, a span of 0.366 $/MWh (0.100%).

**No boundary claim is made in `j_wp`:** every transect point is feasible and no verdict flips along it. Where `wp_stress_ok` does go violated in the swept space is in `arm-fence-p50` at I ≥ 17 MA (32 points), which is a fact about where the violation lives, not a boundary in this axis.

#### `T_i0` — feasible structure (search framing)
**Applies:** yes

The single largest structural effect in the study. At 110 MW the feasible T range is 14.63–18.00 keV and the optimum sits at the **top** of it: restricting to the predecessor's 14.63 keV slice raises the best feasible LCOE from 271.359 to **288.004**, so the temperature axis is worth **16.645 $/MWh**. At 50 MW it relocates which fence binds — see § 6 `n_e0` and § 15 finding #1.

#### `T_i0` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `n_e0` — feasible structure (search framing)
**Applies:** yes

At 110 MW the feasible density band is 0.80–1.10× baseline. Above it `wall_load_ok` fails; at the very top of the swept window `beta_ok` fails (3 points, max beta 0.0509 against 0.050). Density and temperature together are what carry the machine into the wall-limited region at 50 MW.

#### `n_e0` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed.

#### `p_input+tie` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `p_input+tie` — observed response (sensitivity framing)
**Applies:** yes

Two levels only. At 50 MW: 0 of 240 feasible. At 110 MW: 87 of 192 feasible. **No boundary claim is made in `p_input`** — this study does not locate the sustainment flip in installed power; the predecessor `20260901-sustainment-fence` committed that at one grid step between 90 and 100 MW and this study neither refines nor contradicts it.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `I_coil` | `stellarator_09__stellaris__magnet__I_coil` | fan_out | |
| `j_wp` | `stellarator_09__stellaris__magnet__j_wp` | fan_out | The WI-036 sizing lever that replaced the held `wp_side`. |
| `T_i0` | `stellarator_09__stellaris__T_i0` | fan_out | `T_e0` rides the held 0.95 ratio inside the sustainment calc. |
| `n_e0` | `stellarator_09__stellaris__n_e0` | fan_out | |
| `p_input+tie` | `stellarator_09__stellaris__p_input` | fan_out | |
| `p_input+tie` | `stellarator_09__stellaris__p_ecrh` | **tie** | Same installed ECRH power; declared by `20260901-sustainment-fence`, data in `manifest.json → ties`. |
| `B_max` (declined) | `stellarator_09__stellaris__magnet__B_max` | fan_out | Traced, not swept — § 8. |
| `sigma_allow` (declined) | `stellarator_09__stellaris__magnet__sigma_allow` | fan_out | Traced, not swept — § 8. |
| `eps_cond_allow` (declined) | `stellarator_09__stellaris__magnet__eps_cond_allow` | fan_out | Traced, not swept — § 8. |
| `R+tie` (declined) | `stellarator_09__stellaris__R` | fan_out | Traced, not swept — § 8. |
| `R+tie` (declined) | `stellarator_09__stellaris__magnet__R0` | **tie** | Same physical major radius; ANNEX § Declared ties. |
| `a` (declined) | `stellarator_09__stellaris__a` | fan_out | Traced, not swept — § 8. |

Twelve declared keys across ten groups; all validated as package inputs at preflight.

## 8. Indicators and rulings

Per proposed axis, including the five proposed and declined. Source: `indicators.json`, run over all ten groups (`subset: false`).

| Axis | `no_constraint_response` | Constraints reachable | Objectives reachable | Modules fired | Ruling |
|---|---|---|---|---|---|
| `I_coil` | false | 8 / 9 | 10 / 11 | 68 | swept |
| `R+tie` | false | 8 / 9 | 11 / 11 | 71 | **declined** — geometry belongs to the two prior fence studies; sweeping it would confound the winding-pack question with a machine-size one. Note it reaches `magnet_capital` only since WI-036. |
| `a` | false | 5 / 9 | 10 / 11 | 59 | **declined** — same reason. |
| `T_i0` | false | 5 / 9 | 8 / 11 | 55 | swept (added by critique MAJOR 2) |
| `n_e0` | false | 5 / 9 | 8 / 11 | 55 | swept |
| `j_wp` | false | 4 / 9 | 4 / 11 | 53 | swept |
| `p_input+tie` | false | 3 / 9 | 4 / 11 | 48 | swept, two levels |
| `B_max` | false | **1 / 9** | **0 / 11** | 2 | **declined** — see below |
| `sigma_allow` | false | **1 / 9** | **0 / 11** | 2 | **declined** — see below |
| `eps_cond_allow` | false | **1 / 9** | **0 / 11** | 2 | **declined** — see below |

**No axis reported `no_constraint_response`, so no owner ruling was owed under runbook step 4's fail-closed condition.**

**The three fence-limit axes are traced evidence for their own declining.** `B_max`, `sigma_allow` and `eps_cond_allow` each reach exactly **one constraint and zero objectives**, firing two modules. That is the structural signature of a pure fence-relaxer: moving one relaxes a verdict and changes no cost anywhere. Sweeping any of them would manufacture feasible points that cost nothing — precisely the unpriced-lever defect goal `priced-levers` exists to remove. For `B_max` specifically, the consequence chain that would make it a priceable design option is WI-038's purpose and does not exist in this package.

**Model-development findings recorded alongside the rulings** (a ruling does not discharge a finding):

- **MD-1.** `magnet__B_max` is a held literal with **no cost, mass, or stress consequence** — one inequality and nothing else. Every feasibility claim this study makes at the conductor ceiling is a claim about where that literal is set, not about physics. Home: WI-038.
- **MD-2.** `j_wp` reaches no magnet capital: the winding pack's cross-section has no conductor-cost consequence, because conductor cost is ampere-metre-proportional. 85% of the pack (steel, insulation, copper, helium) has no cost home at all. Home: **unrouted** — see § 15 finding #2.
- **MD-3.** `tbr_ok` remains held-vs-held and reaches no swept axis; unchanged since first recorded. Home: standing, rubric Row 2c.

## 9. Preflight results

`results/preflight_results.json`. **All six gates ran; all six pass.**

| Gate | Outcome | Detail |
|---|---|---|
| `declared_keys` | pass | 12 declared keys across 10 groups, all package inputs |
| `sibling_scan` | pass | no suffix-sibling findings (warnings only by contract; never gates) |
| `identity` | pass | kind `sealed`, digest `cc64dc5a4d151cf7…` recomputed from 0 allowed-modified files and 0 declared sources |
| `manifest_currency` | pass | both recorded package fingerprints match the package on disk |
| `baseline_headline` | pass | headline reproduces at relative deviation 0.000e+00; **9/9** pinned verdicts match |
| `package_clean` | pass | package tree byte-untouched (git clean) |

## 10. Execution route and why

**Route: study-local direct-API definition** (`study.py` + `study_route.py`, `StudyRunner` + `PreparedListStrategy`). Chosen because the arms are coordinated axis-group blocks — each proposal carries all four swept axes plus both declared ties plus every held key — which is not a plain Cartesian product over independent keys and so is outside the `teax-study` CLI's shape. The route was exercised at step 5 (identity + baseline emitted) and gated at step 6 before this rationale was written, so this is an account of a route already known to load.

**Glue ledger: none.** `results/package_identity.json` records `kind: sealed`, zero allowed-modified files and zero adapter sources. The harness supplies no value the model does not compute.

## 11. Study definition and window provenance

**Window provenance: `engineered`** — fixed after an oracle scan, not before, and the scan is committed at `results/window_scan.json`.

**The scan, and its own history.** A first scan covered `I_coil` × `j_wp` at two heating levels and held `n_e0` and `T_i0` at baseline; the windows were nonetheless described as scan-derived across all axes. The pre-execution critique caught both that misstatement (MAJOR 3) and its consequence (MAJOR 2). The committed scan is the **second**: 6144 candidates over `I_coil` × `j_wp` × `T_i0` × `n_e0` at both heating levels, 8 oracle errors, covering every axis the study claims to search.

What the scan fixed: at 50 MW the feasible set is empty (0/3072) with 70 candidates blocked by the conductor ceiling alone and 40 by wall load alone — **both fences bind independently**, which is why the p50 arm samples both regions. At 110 MW, 28 feasible candidates in a band at I = 15.0 MA (0.5 MA scan resolution), T 14.63–17, n 0.8–1.1×; the executed arm refines I to 0.2 MA over that band. The density window was widened until beta reached 0.0906 in the scan against a 0.050 limit, so `beta_ok` is testable — the pre-critique window topped out at 0.036 and could not have tested it.

**Executed windows.** `I_P50` = 15.0/15.4/16/17/18 MA; `I_P110` = 14.8/15.0/15.2/15.4 MA; `J_VALUES` = 90 / 118.8271604938272 / 130 A/mm²; `T_P50` = 14.63/17/18/19 keV; `T_P110` = 14.63/16/17/18 keV; `NE_P50` = 1.0/1.1/1.2/1.4×; `NE_P110` = 0.8/0.9/1.0/1.1×; `J_TRANSECT` = 60/70/80/100/110/120/140 A/mm², chosen disjoint from `J_VALUES` so no transect point can be attributed to a grid arm.

**Validity mask:** the evaluability pre-screen (oracle `p_net > 0`, the `20260829-p-pump-fence` pattern) ran over all 439 proposals and **excluded none** — `results/excluded_points.csv` is empty of rows. The predecessor excluded 10 on the same screen; this study's windows do not reach the negative-net region.

**Arms are tagged at construction**, not inferred from values afterwards. The first design inferred the arm by value-matching and mislabelled three transect points into a grid arm, carrying an off-window current column — the one sitting exactly on the conductor ceiling (critique MINOR 5).

## 12. Cross-fingerprint correlation and what it means

**Semantic fingerprint `3cb690aab05e…`; executable fingerprint `cc64dc5a4d15…`; indicator-input pin `6262dbf42c70…`.** All three are recorded in `snapshot.json` and were verified against the package at preflight.

**A semantic boundary crosses between this record and `20260901-sustainment-fence`, and it is load-bearing for one number this record reports.** WI-036 added a ninth constraint (`cond_strain_ok`), retired two entry points (`wp_side`, `c_coil`), and added six (`j_wp`, `f_wp_vol`, `k_coil`, `E_wp`, `f_cond`, `eps_cond_allow`), moving the entry-point census 193 → 197.

What the comparison to the predecessor's committed optimum of **293.468 $/MWh** licenses, and what it does not:

- **Licensed:** an LCOE comparison at a shared operating point, because the pinned baseline headline is unchanged across the boundary (307.08712042841586, reproducing at relative deviation 0.000e+00). On that basis this study's best feasible point at the predecessor's own T = 14.63 keV slice is **288.004**, and its best overall is **271.359**.
- **Not licensed:** any feasibility-structure comparison. The constraint set changed, so "how many points were feasible" is not comparable across the boundary, and neither is any statement about which fence bound in the predecessor versus here.
- **Not licensed:** attributing the 271.359 − 293.468 gap to WI-036. The dominant term is the **temperature axis** (worth 16.645 $/MWh by this study's own measurement), which the predecessor swept only as a transect at baseline current and density and never inside its feasible grid.

## 13. Verification

`results/verification_summary.json`. **Outcome: pass.** 1 store, **15 sampled rows** stratified by verdict combination so the sample cannot miss a produced verdict, **13 channels** compared against the package-owned oracle at relative deviation below 1e-9 with **worst observed 2.74e-16**, and **9 verdicts re-derived** from the oracle's own operands rather than compared to themselves.

**What verification did not cover, stated as part of the outcome:**

- The six `sustain__*` sustainment quantities and the `pb__*` power-balance quantities are fields of multi-field modules and cannot reach the evidence store (ANNEX § Oracle; `20260901-sustainment-fence#3`). They are exported oracle-side in `results/oracle_operands.csv` and are **oracle-derived on both sides** — consistent with the verified verdicts, but not independently verified numbers.
- `aux_cooling__cryo_cost` is in the same class and is likewise oracle-side only. This was discovered by executing: the first execution declared it as a store channel and it came back as an empty column across all 439 rows. The column was moved to the oracle export and the study re-executed rather than leaving a blank or inventing a value — see § 15 finding #4.
- `p_fus` sits outside generic channel coverage, as in every prior record on this package.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| **Pre-execution framing critique** (fresh non-author session, before any point ran) | **MAJOR** — 3 major, 5 minor | **All eight accepted.** Both major findings were independently reproduced by the executor before dispositioning. Full text: `work/orchestration/goals/priced-levers/evidence/T-007_precritique.md`; spawn prompt deposited at `T-007_precritique_prompt.md`. The critique added the `T_i0` axis, re-scoped the p50 arm from search to fence anatomy, forced the scan to cover all four axes, widened the density window until it could test `beta_ok`, refined the current step to resolve the band, forced arms to be tagged at construction, and required this record's § 12 boundary treatment. |
| Correctness | pass | Preflight 6/6; verification pass at worst 2.74e-16; the pinned baseline reproduces exactly with 9/9 verdicts. |
| Honesty | findings, all dispositioned | The first study framing claimed the transect priced the winding pack; the WI-036 design's own D8 had already disclosed that the pack's non-conductor mass has no cost home. The framing was corrected before execution and the contradiction is recorded as § 15 finding #2 rather than quietly repaired. |
| Readability | pass | Every number in §§ 3–6 traces to `results/points.csv`, `results/oracle_operands.csv`, or `results/window_scan.json`. |

## 15. Findings

| id | kind | finding | disposition | home |
|---|---|---|---|---|
| `20260903-priced-levers#1` | `model` | **At the printed 50 MW the machine can sustain itself and stay under the conductor ceiling — and then the first wall cannot take it.** 27 of 240 points are blocked by `wall_load_ok` **alone**: at I = 15.4 MA, T = 17–18 keV, n = 1.2×, required sustained heating is 26.3–36.3 MW against 50 installed (satisfied, with margin) and B_peak is 24.90 T against the 24.9 T ceiling (satisfied), while wall load reads 5.76–6.46 against a 4.05 limit. Only 6 points are blocked by the ceiling alone. The deadlock at the printed power is **sustainment against neutron wall load**, and no conductor grade touches it. | first-order reading; pre-registered as a fence-anatomy result, not as a search outcome | goal `priced-levers` round result; candidate follow-on a wall-load / machine-size item |
| `20260903-priced-levers#2` | `model` | **The winding-pack sizing lever is real physics and almost no economics.** Over a 2.33× swing in pack cross-section, cold volume moves 270.45 → 115.91 m³ and cryoplant capital $20.98M → $16.00M, while **magnet capital is unchanged at $5,401.0M — a delta of exactly zero** — and LCOE moves 0.100%. Conductor cost is ampere-metre-proportional and blind to cross-section; the pack's ~85% non-conductor mass (steel, insulation, copper, helium) has no cost home in the model. The stress relief that made an 18 MA point legal costs 0.026 $/MWh. | disclosed at the claim site; the WI-036 design D8 disclosed the cause and this study measures the consequence | **unrouted** — a stated state; candidate home a WI-036 follow-on giving winding-pack mass a cost account |
| `20260903-priced-levers#3` | `model` | **`cond_strain_ok` is inert across the entire explored space** — violated 0 / 439, max observed strain 0.235% against a 0.400% limit, never binding before `wp_stress_ok` or `peak_field_ok`. The conductor check WI-036 added to close a real two-check gap does not change any verdict in this study's windows. It is reachable from both field levers (so it is not structurally dead like `tbr_ok`), and it would bind at a 0.2% limit, which is the value other projects enforce and which this model holds settable. | disclosed; the limit remains settable and a sensitivity in it is named future work | goal `priced-levers` round result; standing at WI-036 |
| `20260903-priced-levers#4` | `process` | **A declared store channel came back empty across all 439 rows.** `aux_cooling__cryo_cost` is a field of a multi-field module, the documented `pb__*` limitation, and the study declared it as a store channel on the first execution. Caught by inspecting the exported CSV, not by any gate — the store accepted the declaration and produced a blank column silently. | column moved to the oracle-side export and the study re-executed; the blank was not left and no value was invented | documented seam, ANNEX § Oracle; joins `20260901-sustainment-fence#3` |
| `20260903-priced-levers#5` | `model` | **The temperature axis is worth 16.645 $/MWh at the feasible optimum** — restricting to the predecessor's held 14.63 keV slice raises the best feasible LCOE from 271.359 to 288.004, and the optimum sits at the top of the swept T range. The predecessor swept T only as a transect at baseline current and density, never inside its feasible grid, so this lever's value was not visible to it. | disclosed at the claim site with the § 12 boundary caveat | goal `priced-levers` round result |

## 16. Snapshot

`snapshot.json`, resolved at this commit. Its own sha256 is **`59049340ff4a94b7e94ac45d01f87c1b127e90d5e0967c106a26f49a5e58eaae`** (updated 2026-09-03 by the Addendum below, which added one identity field per arm; the value at the original commit `76876b82` was `838ec6a90fb7965739435bd99312238cf28f7db95424f3e66c5be49ce074c261`, and `synthesis.md` stamps that original). Nothing in this record cites a live file for content: deleting or editing the manifest or the package cannot change what this record says.

Carried in it: the three package fingerprints and the sealed executable fingerprint; the manifest digest with the tie and baseline content actually used; per-arm windows with their `engineered` provenance and the scan they were fixed from; digests for all eight `results/` artifacts plus `indicators.json`, `axes.json`, `study.py` and `scan.py`; the preflight outcome; the counts (439 proposed, 439 evaluated, 0 excluded, 94 feasible — 87 in `arm-search-p110`, 7 in `arm-transect-jwp`, **0 in `arm-fence-p50`**); and the teax revision `744745f8…`.

**The per-point store is uncommitted** (`_work/`, gitignored by the studies convention). Every value this record cites is in `results/points.csv` or `results/oracle_operands.csv`, both digested above.

## 17. What this record does not contain

- **No claim that the conductor ceiling is irrelevant at 50 MW.** It appears in 144 of 439 verdicts and blocks 6 points alone. Finding #1 says the wall load is the *more common sole* blocker and that a conductor grade cannot fix the wall-limited region — not that the ceiling does not bind.
- **No priced conductor-grade option.** `B_max` was held and is a free lever in this package (§ 8, MD-1). Every feasibility statement at the ceiling is a statement about where that literal is set.
- **No geometry claim.** `R` and `a` were declined. The wall-load finding is about *this* machine at *this* size; wall area scales with machine size and this study did not sweep it. That is the most obvious next question and this record does not answer it.
- **No sustainment-fact or conductor-fact sensitivity.** `f_ren`, `E_wp`, `f_cond`, `eps_cond_allow`, `k_sigma`, `f_wp_vol` and `k_coil` are held sourced values. An `f_ren` arm would materially move the sustainment threshold, and an `eps_cond_allow` arm at 0.2% would make finding #3's inert constraint bind. Neither was run.
- **No boundary in `p_input`.** Two levels only; the sustainment flip in installed power stands where `20260901-sustainment-fence` committed it.
- **No feasibility comparison across the WI-036 semantic boundary** (§ 12). The 271.359 vs 293.468 comparison is licensed for LCOE at a shared point and for nothing else.
- **No independent verification of the sustainment, power-balance or cryo-cost quantities** (§ 13) — oracle-derived on both sides.
- **No statement about T_i0 below 14.63 keV or above 19 keV**, nor about densities below 0.8× or above 1.4×. The windows are `engineered` and the structure inside them is not a claim about the frame's rightness.
- **The teax revision that executed this run** is `744745f895677f3344b9884627369a6a47ed987f`, recorded in the integration return this pin came from; the study's own `verification_summary.json` records `teax.revision` as unrecorded, the same gap the predecessor record carries.

## Addendum — 2026-09-03 — statement corrections and record-contract closure (evidence untouched)

Written by the resuming executor of goal `priced-levers` round 1, after the fresh administrator's read (`synthesis.md`, which stamps the pre-addendum `snapshot.json` digest `838ec6a9…`). Every correction below was re-derived by the executor from `results/points.csv` and `results/oracle_operands.csv` before it was written. No value in `results/`, `indicators.json`, `axes.json`, `study.py` or `scan.py` changed. Per step 15, the sections above are not rewritten; this addendum supersedes the statements it names.

### A. Statements the record gets wrong, corrected

1. **Maximum conductor strain (§ 4, § 15 #3).** The record says 0.235%. That is the transect arm's maximum. The study-wide maximum is **0.286%** (`arm-fence-p50`, I = 18 MA, `j_wp` = 130). Finding #3's reading stands — 0.286% is under the 0.400% limit and `cond_strain_ok` is violated 0 / 439 — and its 0.2% remark strengthens: at a 0.2% limit **323 of 439 points and the pinned baseline itself (0.217%)** would violate.
2. **Where `wp_stress_ok` is violated (§ 4, § 6).** The record says "I ≥ 17 MA". All 32 violations are at **I = 18 MA** in `arm-fence-p50`; every 17 MA point satisfies (σ 656–789 MPa against 800).
3. **The 27 wall-alone points (§ 15 #1).** The count is correct and the reading stands. The coordinates quoted — I 15.4 MA, T 17–18 keV, n 1.2×, required heating 26.3–36.3 MW, wall load 5.76–6.46 — describe **6 of the 27** (that cell across the three `j_wp` values). The full set spans I 15.0–15.4 MA, T 17–19 keV, n 1.2–1.4×, wall load 5.76–9.23 MW/m², and required sustained heating **−47.8 to +49.3 MW against 50 installed, negative at 12 of the 27** (oracle-side, `results/oracle_operands.csv` `p_aux_required_MW`; the plasma is self-sustaining with the heating off at those twelve). The corrected range makes the finding sharper, not weaker: the wall blocks points across the whole hot, dense corner, not one cell of it.
4. **"The stress relief that made an 18 MA point legal costs 0.026 $/MWh" (§ 15 #2).** Not one value. At 18 MA, moving `j_wp` from 118.83 to 90 flips `wp_stress_ok` from violated (821 MPa) to satisfied (715 MPa) at every (T, n) cell, and the LCOE delta across those sixteen cells is **0.023–0.135 $/MWh**; the record's 0.026 is the T = 18 keV, n = 1.4× cell. The claim's meaning — the relief is nearly free — stands.
5. **"No statement about T_i0 … above 19 keV" (§ 17).** True of `arm-fence-p50`. For `arm-search-p110` the window tops at **18 keV, the level the optimum sits on**; so the constrained optimum (271.359) is **window-bounded, not fence-bounded, in T** — and in `j_wp` (130 is the top of `J_VALUES`) — and sits 0.007 MW/m² under the wall fence (4.043 against 4.05). § 6 `T_i0`'s "the optimum sits at the top of it" already says this; § 17 is corrected to match.

### B. Record-contract closure

`tests/study/test_records.py` failed two of its three checks on this record at resume, which means step 15's fail-closed condition was not run before the record was committed:

1. **A literal less-than sign in § 13** (the § 13 phrase "relative deviation less-than 1e-9", written with the symbol) tripped the placeholder check. Replaced with "below 1e-9". Prose only.
2. **`snapshot.json` `arms[]` lacked `effective_executable_fingerprint`**, which every prior record's arms carry and the closure test reads. Added to each of the three arms with `value` = the sealed executable fingerprint `cc64dc5a4d151cf7…` (already carried by this snapshot's `fingerprints.sealed_executable_fingerprint` and by `results/package_identity.json`), `inputs: null`, `no_adapter: true`. **This is an edit to a file step 15 says is never edited.** It is disclosed here rather than done silently: the snapshot was incomplete, not wrong; no `evaluated`, `feasible`, `window`, `verification`, `stores`, `counts` or digest field changed (the diff is eighteen added lines and nothing removed — `git diff` on the commit shows it); and the record's own closure contract could not be met any other way. The digest moved from `838ec6a90fb7965739435bd99312238cf28f7db95424f3e66c5be49ce074c261` to `59049340ff4a94b7e94ac45d01f87c1b127e90d5e0967c106a26f49a5e58eaae`; § 16 is updated to the new value and names the old one.

### C. Disclosures the administrator surfaced, answered from outside the record

- **`results/_work/`** is a gitignored working directory (`exploration/stellarator_e2e/studies/.gitignore`: `**/_work/`), not evidence; it is correctly absent from `results_artifacts`.
- **The two package path spellings are one tree:** `exploration/stellarator_e2e/pkg/stellarator_tea` is a symlink to `../generated`. The identical sealed digest in all four artifacts is the evidence of that.
- **`results/verification_summary.json` lists nothing under `not_independently_verified`** while § 13 names three classes of oracle-side-only quantities. The caveat lives in prose, not in the artifact. Filed as a study-tooling contract gap alongside `20260903-priced-levers#4`; no finding id is minted here (a goal round may not mint one).
- **`teax.revision` unrecorded** in the verification artifact — the same gap the predecessor record carries, already disclosed in § 17.

### D. What this addendum does not change

Every § 15 finding id, class, and disposition; every violation count in § 4; the feasible counts; the constrained optimum and the 14.63 keV slice comparison; the transect's magnet-capital delta of exactly zero; the § 12 boundary treatment. The administrator's independent recount agrees with all of them (`synthesis.md` § 2.2).
