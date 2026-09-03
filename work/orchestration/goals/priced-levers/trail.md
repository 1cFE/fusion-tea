# Trail: priced-levers

What happened, and what was decided. Append-only, newest entry last, ISO dates; no entry is ever edited in place — corrections are `### Amendment` entries. This file logs judgment, not routine stage motion; native workflows keep their own stage records and are cited, never restated. Procedure: `work/orchestration/GOAL_RUNBOOK.md`.

Goal grounded 2026-09-02 (`goal.md`, owner-present session, straight off the close of `operating-point-closure`). No round open.

## Round 1 — priced-field-lever

### Strategy revision — 2026-09-02

- **Approach:** make the *field* lever real, because that is where the deadlock actually binds. The goal-grounding recount (goal.md § Amendment 2026-09-02) shows every sustainment-satisfying point at p = 50 is blocked by the conductor ceiling **and** the winding-pack stress limit together, so pricing either one alone opens nothing. Three moves: (1) **winding-pack sizing chain (WI-036)** — `wp_side` becomes a design variable that feeds winding-pack volume, conductor and coil cost, and the WI-024 cryo cold-mass chain, so relieving stress costs conductor, cold mass and radial build instead of being free; (2) **conductor-grade consequence chain (WI-038)** — `B_max` carries an admissible sourced basis and a cost consequence, so raising the ceiling is priced rather than granted; (3) a committed study sweeping the field lever at the printed p = 50 — does a feasible region open once both fences can be bought past, and at what LCOE. Research runs first and in parallel, because the conductor basis is the one input the pinned 1costingFE cannot supply.
- **Assumptions:** the model's stress form σ = k_sigma·I_coil·B_peak/wp_side (k_sigma held, calibrated at the printed worst-coil pair) is usable as the relief channel, so a wider pack lowers stress at fixed current and field; the cost and cryo chains can consume a computed `wp_side` (WI-036 is exactly that item); an admissible, clean-room-legal basis exists in the open literature for REBCO winding performance near 29–30 T at 20 K and for how conductor cost scales with it; the 800 MPa 316LN allowable is the model's own sourced structural limit and is challenged only with a source, never relaxed to fit.
- **Abandonment conditions:** no admissible field-ceiling basis **and** no structural relief that opens feasibility at p = 50 — that is a bounded negative on the field escape, and routes the goal to its heating half rather than continuing here; the stress relief channel proves not to be `wp_side` (the held k_sigma form cannot bear a sizing sweep with an admissible basis); a load-bearing basis fails image verification with no admissible substitute (surfaced with options, never defaulted); or the committed-study restatement cannot be honestly written.
- **Intended model increment:** WI-036 and WI-038 minted into spec/design/plan through the modelling PM — computed winding-pack volume and cost from `wp_side` and coil geometry, cold mass into the cryo chain, and `B_max` with a sourced grade basis plus its cost consequence; instance rebinds in `stellarator_09`; entry-point retirement with the MR-WI037-7 restatement duty recorded before regeneration.
- **Intended study question:** with the field lever priced on both fences, does a feasible operating point exist at the printed 50 MW installed heating, what does it cost in LCOE, and which fence binds at the constrained optimum?

No future task list. One pin, one committed study, close on the first valid reading.

### T-001 scope

- **Objective:** establish whether an admissible, clean-room-legal sourced basis exists for (a) a REBCO winding-pack peak-field capability at or above ~29 T at 20 K, (b) how conductor cost scales with that capability, and (c) whether the 800 MPa structural allowable has a defensible higher-strength alternative — or return a bounded negative naming what is missing.
- **Why now:** the strategy's move (2) cannot be specified without a basis, and the pinned 1costingFE cannot supply one — its `MAGNET_TABLE` tops out at `rebco_hts b_max = 23.0` (`defaults.py:609-617`), below the model's own 24.9 T. Research has latency and is the input to the model increment, so it runs first and in parallel with nothing else executing.
- **Scope:** authorized — the native research seam (`scripts/research_seam.py` request/open/log/close, `scripts/source_registry.py register`, `/research-acquire`), read-only reads of admissible sources and of the pinned 1costingFE, and the run directory under `knowledge/research/requests/`; excluded — any edit under `models/` or `exploration/`, any modelling-PM stage, discovery-log writes, and every artifact barred by `knowledge/holdout/aries-cs/PROTOCOL.md` §3 (the four sealed PDFs, the ARIES-CS-informed extractions, and the two documented-exception costing sources without an owner exception).
- **Inputs:** `goal.md` including § Amendment 2026-09-02; `knowledge/holdout/aries-cs/PROTOCOL.md` §3 (narrower constraint: clean room binds every search and every registration, and the seam's own hold-out check is a backstop, not a substitute for not looking).
- **Done when:** the seam returns for each request — `REGISTERED` with citable paths, `BOUNDED_NEGATIVE` with the durable negative written, or `OPERATOR_QUEUE` naming what a person must fetch — and the goal-level reading says which of the three model inputs are now sourced and which are not.
- **Stop when:** a discovered prerequisite, a strategy blocker, or a declared limit.

### T-001 start — 2026-09-02

Task T-001 under § T-001 scope: run the research seam for the conductor field-ceiling basis, the conductor cost-vs-field basis, and the structural-allowable alternative. Native target: `knowledge/research/requests/` (requests, run records, receipts, returns) and, on a keeper, `knowledge/sources/` + `knowledge/MANIFEST.jsonl` + `knowledge/SOURCE_INDEX.md` through `source_registry.py`. Expected artifacts: three request files, three run directories with `return.json`, and either registered source directories or durable bounded negatives.

### Strategy evidence — 2026-09-02

Deposited at `evidence/R1_deadlock_recount.md`: the recount behind `goal.md` § Amendment 2026-09-02 and behind this round's strategy, from `20260901-sustainment-fence/results/points.csv` (record dir `@62a1fa7b`). Goal-layer analysis of committed artifacts; no native side effect. Three results carry the round:

1. **No point at p = 50 is blocked by the conductor ceiling alone** — all 29 sustainment-satisfying points violate `peak_field_ok` and `wp_stress_ok` together.
2. **The model's stress form is a real relief channel** — σ = k_sigma·I_coil·B_peak/wp_side reproduces the committed `sigma_wp` column to the printed digit at every I_coil, and the relief `wp_side` needed for 800 MPa is tabulated (0.400 m at 18 MA, rising to 0.710 m at 24 MA). Nothing charges for it today.
3. **Eleven points fail only those two fences** — the candidate feasible region at the printed 50 MW. The unlock condition is concrete and conjunctive: **B_max ≥ 29.1 T and wp_side ≥ 0.400 m**.

**Pre-registered expectation, recorded before any model change:** the cheapest field-escape point reads 332.95 $/MWh with the wider pack and better grade **not** charged, against the committed heating-escape alternative at 293.468 $/MWh (p = 110). The field escape is 13.5% behind before it is priced, and pricing can only move it up — so this round is expected to return a *negative* on the field escape. It is run anyway because the grid is coarse, the 11 points were never optimized against a live sizing lever, and the heating escape's own number is not yet honestly priced either. The pre-registration exists so a confirming result is not mistaken for a discovery; it pre-settles nothing, and the dispositions still go to the fresh checkpoint reviewer.
