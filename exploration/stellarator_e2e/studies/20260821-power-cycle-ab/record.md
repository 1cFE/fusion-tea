# Study record — 20260821-power-cycle-ab

## 1. Study header

- **Study id:** `20260821-power-cycle-ab`
- **Package:** `stellarator_e2e` (`exploration/stellarator_e2e/generated`, `stellarator_tea`, runtime contract 2.0.0, sealed after WI-030)
- **Date executed:** 2026-08-21
- **Executor:** Claude (RUN-STUDY Item 6 Phase 2 session, branch `feat/run-study-first-consumer`)
- **Mode:** execute
- **Arms:** `arm-rankine-paper`, `arm-rankine-upstream`, `arm-sco2`, `arm-sco2-eta-only`

Arms are variants of the same question, run to be compared. Two studies asking different
questions of the same package are two records, not two arms of one.

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> Compare steam Rankine against sCO2 on the stellarator
> Run sensitivity analysis on other axes for each type
> Try to find a non-intuitive result on the interactions

*(Owner, 2026-08-21, verbatim; three bullets as given.)*

**Executor's additions (mine, not the owner's):**

- "Steam Rankine" and "sCO2" are represented as the power-conversion block the package exposes: `eta_th`, the turbine rate (`turbine__cost_per_mw`, CAS23) and the heat-rejection rate (`heat_rejection__cost_per_mw`, CAS26). That is exactly what 1costingFE's cycle presets carry (`defaults.py:578-593`); CAS24/CAS25 and the primary pumping power are cycle-independent (DI-007). The cycle is the secondary side; the Stellaris primary coolant is helium regardless.
- Three arms, not two. The Stellaris paper assumes "a simple electrical conversion efficiency of 1/3" and names no cycle (`raw.pdf` p. 3). Its cost rates in the model are the upstream *Rankine* preset, but its efficiency is not (upstream Rankine is 0.40). So `arm-rankine-paper` (η 0.333, the model as built) and `arm-rankine-upstream` (η 0.40) separate "paper vs upstream" from "Rankine vs sCO2"; `arm-sco2` is the upstream sCO2 preset (η 0.47, lower rates). "Rankine" in the arm labels is this study's label, not the paper's.
- "Other axes for each type" is taken as: the two geometry levers the proof-of-life searched (`R`, `a`, same window) and the two economic levers it and the known-answer set already declare (`availability`, `discount_rate`), each swept identically in every arm. No new axis is invented; the interaction question is answered by running the same axes under each cycle.
- "Interactions" is read as: does the cycle change *where* the constraints bind and *which* one binds (the feasible region over R, a), and does it change the *shape* of the economic-lever responses, not only their level. The "non-intuitive result" is something to look for in the data, not a hypothesis fixed in advance; whatever is found is reported with its evidence, and "nothing non-intuitive found" is an acceptable answer.
- Every point runs on the one sealed package (post-WI-030, six constraints); the arms differ only in the three block values, so one fingerprint, one store.

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
| `R` | search | Reaches `net_positive`, `recirc_ok`, `wall_load_ok` through computed operands (`indicators.json`); the proof-of-life found both fences and a constrained optimum on this axis, and the oracle scan shows both fences inside the window in every arm. |
| `a` | search | Same reach as `R`; the wall-load fence is set by `a` first (wall area ∝ a at fixed R, fusion power ∝ a²). |
| `availability` | sensitivity | `no_constraint_response` (sound negative): no constraint operand is reachable. The oracle scan moves LCOE 455 → 248 $/MWh at baseline geometry with no verdict change. Swept only under the owner's ruling (§ 8). |
| `discount_rate` | sensitivity | `no_constraint_response`: reaches only CAS72, the two LCOE forms (levelization and IDC). Scan: 163 → 485 $/MWh, no verdict change. Swept only under the owner's ruling (§ 8). |
| cycle block (the arms) | search | The arms are the levels of one categorical axis: each holds a fixed (η, turbine rate, heat-rejection rate) triple. It reaches `net_positive` and `recirc_ok` through `p_et` and the recirculating sum, so the question is whether the feasible region and the active constraint move with it — search framing. Not a numeric sweep. |

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

Every declared qualified entry key, with its per-key provenance.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `R` | `stellarator_09__stellaris__R` | fan_out | plasma major radius, one plant-level entry point since the model migration |
| `R` | `stellarator_09__stellaris__magnet__R0` | tie | the magnet-cost Ampere's-law current runs on the same major radius under a separately authored attribute; declared in `manifest.json` `ties` (Item 3, 2026-08-19) and carried in ANNEX § Declared ties |
| `a` | `stellarator_09__stellaris__a` | fan_out | plasma minor radius |
| `availability` | `stellarator_09__stellaris__availability` | fan_out | capacity factor; one entry point (consuming calcs bind it by the `_in` convention) |
| `discount_rate` | `stellarator_09__stellaris__discount_rate` | fan_out | discount / interest rate; reaches CAS71, CAS72, CAS80 levelization and IDC |
| cycle block (held per arm) | `stellarator_09__stellaris__eta_th` | fan_out | thermal-to-electric efficiency |
| cycle block (held per arm) | `stellarator_09__stellaris__turbine__cost_per_mw` | fan_out | CAS23 turbine rate |
| cycle block (held per arm) | `stellarator_09__stellaris__heat_rejection__cost_per_mw` | fan_out | CAS26 heat-rejection rate; the two suffix siblings the scan found (`electric_plant__cost_per_mw`, `misc_plant__cost_per_mw`) are CAS24/CAS25, cycle-independent upstream (DI-007), and deliberately not in the block |

## 8. Indicators and rulings

Per proposed axis, including axes proposed and declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `R` | constraints_reachable (`net_positive`, `recirc_ok`, `wall_load_ok`; 7/8 objectives) | — | swept, search-framed |
| `a` | constraints_reachable (same three; 7/8 objectives) | — | swept, search-framed |
| `availability` | `no_constraint_response` (0/6; objectives `cas72`, `fuel`, `lcoe`, `lcoe_1cfe`) | **[OWNER-VERBATIM 2026-08-22]** "no sensitivity" | **declined** on the owner's ruling: not swept. Oracle scan (`results/oracle_scan.json`): LCOE 455 → 248 $/MWh over 0.50–0.95 with no verdict change in any arm. |
| `discount_rate` | `no_constraint_response` (0/6; objectives `cas72`, `lcoe`, `lcoe_1cfe`) | **[OWNER-VERBATIM 2026-08-22]** "no sensitivity" | **declined** on the owner's ruling: not swept. Oracle scan: LCOE 163 → 485 $/MWh over 0.03–0.12 with no verdict change. |
| cycle block (the arms) | constraints_reachable (`net_positive`, `recirc_ok`; `cas72`, `lcoe`, `lcoe_1cfe`, `total_capital`) | — | not a numeric sweep; four arm levels (owner added the fourth, 2026-08-22). Two suffix siblings (`electric_plant__cost_per_mw`, `misc_plant__cost_per_mw`) are CAS24/CAS25, cycle-independent upstream (DI-007), excluded. |

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
| `availability` | Nothing ties the achievable capacity factor to what sets it. CAS72 prices the fluence-limited core replacements but no coupling makes availability a *consequence* of the core lifetime and the outage time each replacement implies, or of any maintenance model; the model accepts any capacity factor at any wall load. The constraint that should push back is an availability ceiling derived from core lifetime and replacement duration. | `20260821-power-cycle-ab#1` |
| `discount_rate` | The cost of capital is a free multiplier. Nothing couples it to construction duration, to the capital mix, or to a financing structure; no bound or trade-off resists it. Whether anything *should* push back inside a techno-economic model is itself a modeling question (a finance-risk coupling would be a new input class); the gap is stated, not its fix. | `20260821-power-cycle-ab#2` |

## 9. Preflight results

Every mechanical gate that ran, with its outcome. The identity and baseline gates
read the documents the route-preparation step deposited in `results/`; name those
files in the detail column so a cold reader can open what the gate read. A gate that did not run is stated as
such with its condition.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 8 declared keys across 5 groups, all package inputs (`results/preflight_results.json`) |
| Suffix-sibling scan (warnings only) | warnings: 2 | `cycle_block`: `stellarator_09__stellaris__electric_plant__cost_per_mw`, `…misc_plant__cost_per_mw` — CAS24/CAS25 rates, cycle-independent (DI-007), excluded on purpose |
| Identity | pass | kind sealed, digest `7447efea9f20…` recomputed from 0 allowed-modified files; every sealed artifact matches (`results/package_identity.json`) |
| Baseline gate against the pinned headline | pass | `lcoe_calc__lcoe` expected 275.2642200420774, observed at relative deviation 0.000e+00; 6/6 pinned verdicts match (`results/baseline_result.json`) |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk (`manifest_currency`) |
| Package cleanliness | pass | package tree byte-untouched (git clean) before execution; re-checked after (§ 13) |

## 10. Execution route and why

- **Route:** study-local direct-API (`study.py` in this directory, over `studies/study_route.py`'s `run_points`: stock `ProvisionalPackageLoader(strict=True)` → `PreparedEvaluator` → `StudyDefinition` with `PreparedListStrategy` → `StudyRunner` → `StudyStore`)
- **Why this route:** three arms that each hold a three-key block constant while four axes sweep is a coordinated proposal list, not a Cartesian product; stock teax `744745f`'s CLI builds only a `GridStrategy` (`simkit/study/config.py:126`), which would cross-multiply the block keys. The route loaded and gated at steps 5–6 before this was written.

The rationale is recorded after the route was first exercised and gated, so it accounts
for a route already known to load rather than predicting one.

**Glue disclosure.** What the harness supplies that the model does not, and what that
means for the claims. The ledger's entries are values and live in `snapshot.json`
under `glue_ledger`; this is the argument about them.

glue ledger: none. No adapter on this route, so nothing is harness-supplied. Every value in every proposal is either a swept axis, the declared tie, or an arm's block; every other input is the sealed package's own.

## 11. Study definition and window provenance

The candidate windows were scanned with the package-owned oracle (`oracle_entry.evaluate`, `results/oracle_scan.json`) at the corners and the baseline of each arm before any package point ran. What the scan showed and what it fixed:

- **(R, a):** the proof-of-life window (R 4–20 m, a 0.8–2.2 m, validity mask R > a + 2.25 m) contains both fences in every arm: the small-machine corner fails `recirc_ok` (rec_frac 0.94 / 0.79 / 0.68 by arm) and the fat-plasma corner fails `wall_load_ok` (5.46 MW/m², cycle-independent). Reused unchanged so the arms join the proof-of-life record by coordinate.
- **availability 0.50–0.95:** LCOE only; no verdict moves in any arm. Reused unchanged from the proof-of-life.
- **discount_rate 0.03–0.12 (step 0.005):** LCOE only; no verdict moves. Engineered bracket around the model's 0.07, spanning a public-utility to a merchant cost of capital.

All three windows are **engineered**: the geometry window is the proof-of-life's choice, the two economic windows are brackets around the model's bound values. What that costs: no claim that the swept ranges are the physically or commercially attainable ranges; a result at a window edge is a result about the window, not about the plant.

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

Each named lens, its verdict, and its disposition. The pre-execution framing critique
is one of them.

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing critique (fresh `general-purpose` subagent, 2026-08-21, read § 1–2, `axes.json`, `indicators.json`, policy §§ 2/5/7/9, runbook step 4) | PROCEED WITH CHANGES. Framings honest; axes legal under policy §§ 2/5. Required: rulings + findings for the two `no_constraint_response` axes; a framing row for the cycle block; the objective channel and baseline geometry named; the aspect mask sourced; per-arm window scan; three verdicts (`beta_ok`, `peak_field_ok`, `tbr_ok`) inert over the whole study and must be declared so. Recommended: a fourth arm (sCO2 η with Rankine rates) to split efficiency from cost rates; econ sweeps at more than one geometry. Structural limits named: the cycle reaches none of the wall-load, beta, peak-field fences nor magnet cost, so no interaction with those can appear. | Rulings taken and recorded (§ 8); cycle-block row added (§ 5); objective channel `lcoe_calc__lcoe`, baseline geometry (R 12.7, a 1.3), and the inert verdicts stated (§ 3, § 4, § 17); the mask is sourced — a derived geometric bound from the held-fixed radial-build stack, `ANNEX.md § Validity masks`, cited in § 11; the window scan was run in all three arms before the critique (`results/oracle_scan.json`). Fourth arm **added** (`arm-sco2-eta-only`, owner 2026-08-22). Multi-geometry econ sweeps: owner said yes, but also declined both econ axes — conflict recorded as an open item for the next session (see handoff). |

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
