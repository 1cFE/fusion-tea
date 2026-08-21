# Audit — WI-028 Handshake account scope: CAS22 tail + CAS40/50/60

**Scope:** Work-item audit (final pipeline stage) of WI-028, implemented at commits `feb13ff3` (G-8 re-baseline) + `ad41a1d5` (implement work), stage log `3ea63ffe`.
**Auditor posture:** Fresh session. Every bar independently reproduced from source — nothing accepted on the implementer's word.
**Date:** 2026-07-20 (run at repo HEAD `3ea63ffe`, branch `feat/stellarator-mbse-demo`).
**Exec:** `~/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python` (this repo is a git worktree of `~/1cfe/fusion-tea`; the exec venv and `.env` live in the main checkout). License resolved (len 37).

## Overall verdict: **POSITIVE**

All 9 audit bars reproduce POSITIVE. The headline, oracle, handshake A-2 table, rollup, reconstruction arithmetic, two-tree mirroring, trap assertions, G-8 compliance, standing bars, citations, and SV-034 all check out against independent reproduction. Two cosmetic notes are recorded below (neither affects a verdict): a one-line-off citation on `concept_scale`, and a point-in-time staleness in the plan's "only commit made" note.

## Toolchain pins (verified before executing — all exact)

| Tool | Required | Live HEAD | Status |
|---|---|---|---|
| sysml-codegen | `06d95f8` | `06d95f854f30f77f1a7c93f9c0f13be878765165` | ✓ on pin |
| teax | `07eb0ac` | `07eb0accd4852742a6da1820a05a4cae4fe707df` | ✓ on pin |
| agentic-mbse | `4c18d61` | `4c18d616f77e26932a8e158cefc2637db47f9b07` | ✓ on pin |
| 1costingFE | `0254385` | `02543850089be175ea7c28b92a8b2a4184e1637e` | ✓ on pin |

---

## Bar 1 — A-2 per-account table + reconstruction — **POSITIVE**

Re-ran `handshake_1costingfe.py`. Reproduced the emitted point at `0254385` (drift-assert passed) and the full A-2 table:

**8/11 newly-scoped accounts under 1e-6** (reproduced rel devs, matching the record exactly):

| account | rel dev | bar |
|---|---|---|
| remote_handling | −3.23e-08 | PASS |
| coolant | +1.62e-08 | PASS |
| aux_cooling | −2.92e-08 | PASS |
| waste | +7.60e-08 | PASS |
| fuel_handling | −5.21e-08 | PASS |
| other_rpe | +2.86e-09 | PASS |
| inc | +7.95e-08 | PASS |
| owner (CAS40) | +3.51e-08 | PASS |
| installation (C220111) | −1.98e-04 | MISS → A-4 |
| supplementary (CAS50) | −6.24e-05 | MISS → A-4 |
| idc (CAS60, reported) | +1.89e-03 | MISS → A-4 (Option C) |

**Reconstruction recomputed independently** (not accepting the trap's own claim), from the raw compared values in the handshake:
- Implied C220106 pump from the cas20 shortfall: `−cas20_delta / 1.14 = 821,614.25 / 1.14 = $720,714` ≈ the documented **$0.721M**. (At the handshake point 1cfe is NOAK → c29 contingency = 0, so `cas20 = cas2x`; the missing pump propagates as 1× via vessel-in-powercore + 0.14× via installation = 1.14× pump.)
- Installation short = `$-100,901.77` vs `0.14 × pump = $-100,900` → reconstructs to **$1.77 (rel ~3e-8)**.
- CAS10 remainder = model precon 34.5M − 1cfe 18.5M = **+$16,000,000 exactly** (F-4, pre-existing WI-025 remainder).

The 3 misses are the two documented A-4 remainders (pump; CAS10 +16M) propagating through downstream formulas — each reconstructs to 1cfe when the remainder is added back. **No formula error.**

## Bar 2 — Rollup + no-third-source — **POSITIVE**

Reproduced (SysML $): **cas20 = 5,710.12 M$** (5,710,124,674.81), **cas30 = 1,522.70 M$** (1,522,699,913.28), **overnight = 7,887.07 M$** (7,887,072,570.37). Matches the record and the stage log.

**Overnight delta arithmetically verified, no third source:**
```
overnight delta = +14,922,984.65   (SysML − 1cfe target 7,872,149,585.72)
reconstruction  = CAS10(+16,000,000) + cas20d(−821,614.25) + cas30d(−219,276.17) + suppd(−36,126.52)
                = +14,922,983.06
residual        = $1.59   (rel 1.1e-7 — display-rounding of the cents-level compared values)
```
Every dollar of the three rollup deltas resolves to the two remainders (CAS10 +16M net of the pump propagating through cas20/cas30/supplementary). No unexplained third source.

## Bar 3 — Design point + oracle independence — **POSITIVE**

Re-ran `run_stellaris_single.py`:
- total capital `$16,145,706,216.036476` (expect 16,145,706,216.04) ✓
- LCOE `$258.013640/MWh` ✓; p_net `915.081088` ✓; q_eng `6.606662` ✓; rec_frac `0.151362` ✓
- **5 constraint verdicts all `satisfied`** (beta_ok, net_positive, recirc_ok, tbr_ok, wall_load_ok); VERDICT PARITY PASS.
- **Oracle bit-exact:** worst reldev `4.41e-16` (lcoe); total_capital 3.54e-16, cas20 3.17e-16, overnight 3.54e-16 — all << 1e-9.

**Oracle genuinely independent (verified by reading `verify_stellaris.py`):** `compute()` is a self-contained pure-Python re-derivation of the entire chain — plasma geometry, radial build, the 200k-interval Bosch-Hale profile integral, power balance, all account costs, and the D2 overnight assembly (cas2x → contingency → cas20 → indirect → cas30 → overnight; CAS60 idc reported line; Option-C `total_capital = overnight`, lines 233–275). Inputs come from a hardcoded `IN` dict of Stellaris design-point bindings — it reads **no pipeline JSON output**. It is a separate implementation path (Python vs codegen→teax), so it catches execution/codegen faults while the A-2 handshake catches formula faults — the two-tier structure the anchor spec (A-1) intends.

## Bar 4 — Two-tree mirroring — **POSITIVE**

Region diff of the three WI-028-edited files, canonical `models/` vs staged `exploration/stellarator_e2e/models/`:
- `mfe_account_costs.sysml` — **IDENTICAL**
- `stellarator_plant.sysml` — **IDENTICAL**
- `mfe_plant.sysml` — differs **only** by the two sanctioned Item-10 comment blocks (lines ~402–406 and ~564; explanatory `//` comments, no code).

Broad `diff -rq` confirms no other `.sysml` file differs. The other "Only in" entries (`models/analyses` vs `models/library/analyses`, `generic_ife`/`hif_ife` absent from the stellarator-only staged tree) are the known flattened staged-tree layout, not WI-028 edits.
**Snapshot provenance = staged tree:** `stellarator.snapshot.json` `document_path` entries resolve to `.../exploration/stellarator_e2e/models/...`; `captured_at 2026-07-21T02:26Z`.

## Bar 5 — Trap assertions executable — **POSITIVE**

The `trap(name, ok, detail)` helper (`handshake_1costingfe.py:577-579`) ends in `assert ok, f"D6 TRAP FAIL [{name}]: {detail}"` — a real executable assert, not a comment. Each `ok` is computed from live values. All six D6 trap classes present and asserting (traps 1&2 jointly asserted by the clean-account pass, per design):
1/2. plant-total/per-module + reference-power split — `all(abs(r) ≤ 1e-6 for the 8 clean accounts)` (`:590`)
3. installation base = 0.14·Σ(C220101..110) [+pump] — reconstruction ≤ 1e-6 (`:600`)
4. fuel-keyed bases (DT) — equality on 6 config values (`:581`)
5. F-2/F-3 structural — `cas28==5.0` and cas20/cas30 reconstruct (`:607`)
6. CAS60 Option C — `|total − overnight|/overnight < 1e-12` (`:611`)

The handshake ran to completion (printed all traps, wrote JSON) → every assert passed. Reproduced all `[PASS]`.

## Bar 6 — G-8 compliance — **POSITIVE**

- `git show --stat feb13ff3`: **1 file changed** — `handshake_comparison.json` only (+105/−6). ✓
- **Comparison logic unchanged:** `rel(a,b)` (the deviation function) is **byte-identical** between `5127efa4` and current. The handshake `.py` changes (145 ins/12 del) are new channels/rows/injection/traps plus removal of the retired `direct_capital` aggregation channel (the D2 restructure) — i.e. *what feeds* the comparison, not the comparison machinery. Exactly what G-8 permits.
- **Message documents absent→computed:** `feb13ff3` body lists all 11 accounts with signed magnitudes and A-2 result, and explicitly states "structurally absent before, NOT previously injected; so the injection map did not shrink." ✓

## Bar 7 — Standing bars — **POSITIVE**

- **WI-022 sha256:** `dt_fusion_power_impl.py` = `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f` → matches `8d2357…794a9f`. ✓
- **IFE anchors** (`run_anchors.py`): Run A LCOE `252.29996307` byte-exact; Run B `68.69020165` byte-exact; **Run C fails on `PipelineValidationError` (teax-vs-HIF-package field-name skew)** — precisely the documented out-of-scope leg (owner ruling 2026-07-20). ✓
- **pytest** (`uv run pytest tests/models/`): **11 failed / 18 passed / 14 skipped / 0 errors**. ✓
- **L1** (`agentic-mbse validate --level 1 models`): **Errors 0**, all checks pass. ✓
- **MR-2 grep:** no hand-coded viability/feasibility flags in `exploration/stellarator_e2e/*.py` (constraint verdicts are generated, not hand-coded). ✓

## Bar 8 — MR-4 / MR-3 — **POSITIVE**

All 16 new instance bindings in `stellarator_plant.sysml` carry a `**Source**`/`**Ref**`/`**Basis**` doc comment resolving to 1costingFE at pin `0254385`. Spot-checked well beyond the required 4 — verified the cited *values* against actual 1cfe source (checked out at `0254385`):

| binding | cited value | 1cfe source | match |
|---|---|---|---|
| remote_handling_base | 150.0 M$ | costing_constants.yaml:131 (`remote_handling_dt_base: 150.0`) | ✓ |
| installation_frac | 0.14 | costing_constants.yaml:137 | ✓ |
| fuel_handling_base | 120.0 M$ | costing_constants.yaml:165 | ✓ |
| owner_base | 41.2 M$ | costing_constants.yaml:245 (`owner_cost_dt: 41.2`) | ✓ |
| spares/startup/decom | 0.03 / 40.0 / 272.0 | yaml:253 / :259 / :263 | ✓ |
| cas28 | 5.0 M$ | yaml:229 (`digital_twin: 5.0`) | ✓ |
| coolant 166.0 + 40.6 | cas22.py:684/685 | ✓ | ✓ |
| waste 1.96 / other 11.5 / inc 85.0 | cas22.py:702/724/731 | ✓ | ✓ |
| owner ^0.5 power-law | costs.py:256 | ✓ | ✓ |

**MR-3:** the 7 new library defs carry no Stellaris-specific literals — bases (150e6, 120e6, 41.2e6…) and `concept_scale` appear **only** at the instance; the library carries only concept-agnostic cited defaults (ref powers, exponents, `installation_frac 0.14`). ✓

*Cosmetic note:* the `concept_scale` binding cites `cas22.py:641 (ConfinementConcept.STELLARATOR: 1.0)`, but line 641 is `TOKAMAK: 1.0` — STELLARATOR: 1.0 is at `:642`. Value (1.0, toroidal) is correct; the line cite is off by one. Not a bar failure.

## Bar 9 — SV-034 + A-4 table — **POSITIVE**

- **SV-034** (`VALIDATION_MATRIX.md:60`): exactly one row, status `passing`. Content is consistent with what I reproduced (A-2 8/11 under 1e-6, A-4 misses itemized, oracle rel 1e-9 at the new headline, IFE A/B byte-exact + Run C out-of-scope, pytest 11/18/14/0, L1=0, pin 0254385). (The `pm update-validation` CLI corrupts rows containing `|` in text — the implementer edited the status column directly; the row parses cleanly now, single instance, no duplication.)
- **A-4 remainder table complete:** (1) C220106_pump $0.721M (vessel shell-only, standing WI-025 remainder); (2) CAS10 model 34.5 vs 1cfe 18.5 M$ = +16.0M (F-4, isolated at overnight); (3) CAS60/`total_capital` convention (Option C — CAS60 A-2-checked reported line; 1cfe folds CAS60 into `total_capital` = 10,095.84M, model keeps `total_capital = overnight = 7,872.15M` and folds IDC into the LCOE `idc_factor`). Present in the plan record, the handshake output, and the `feb13ff3` message; the residual reconciles to this itemized sum (Bar 2). ✓

---

## MR-WI028 requirement coverage

| Req | Verdict | Evidence |
|---|---|---|
| MR-WI028-1 (CAS22 tail forward-computed) | PASS | 8 tail accounts computed; 6 under A-2, installation A-4 (pump) |
| MR-WI028-2 (CAS40 + CAS50) | PASS | owner under A-2; supplementary A-4 (pump propagation), reconstructs |
| MR-WI028-3 (CAS60 documented mapping) | PASS | Option C ruled; reported line, A-2-checked, excluded from total_capital |
| MR-WI028-4 (A-2, no grandfathering) | PASS | 8/11 under 1e-6; 3 misses are A-4 remainders, not loosened bars |
| MR-WI028-5 (A-4 itemized) | PASS | 3-item table, signed magnitudes, reconciles |
| MR-WI028-6 (A-5 trap discipline) | PASS | 6 executable-assert trap classes, all pass |
| MR-WI028-7 (MR-3/MR-4 traceability) | PASS | 16 cited bindings verified vs 1cfe; no library concept literals |
| MR-WI028-8 (G-8 re-baseline, logic untouched) | PASS | feb13ff3 JSON-only; rel() byte-identical; move list documented |
| MR-WI028-9 (headline re-baseline + oracle) | PASS | $16.146B / $258.014; oracle worst 4.4e-16 |
| MR-WI028-10 (standing bars carried) | PASS | WI-022 sha, IFE A/B, pytest, L1, PROTOCOL; Run C supersession recorded |

## Findings (both cosmetic; no verdict impact, no re-work required)

1. **`concept_scale` citation off by one line** — cites `cas22.py:641` for `STELLARATOR: 1.0`; the actual line is `:642` (`:641` is `TOKAMAK: 1.0`). Value correct. Optional one-character fix.
2. **Plan record staleness (point-in-time)** — the Implementation Record's "Only commit made: the G-8 re-baseline `feb13ff3` … all other WI-028 edits remain staged-clean/uncommitted" was written mid-implement; the implement work was subsequently committed as `ad41a1d5` and the stage log as `3ea63ffe`. This is expected (the two-commit structure `feb13ff3` + `ad41a1d5` is the audited baseline) and consistent with Bar 6 — `feb13ff3` still touches only the JSON. No action needed beyond awareness.

## PROTOCOL

`knowledge/holdout/aries-cs/PROTOCOL.md` §3 honored — no barred artifact was read, cited, or opened during this audit. The whole account scope sources from 1costingFE (the ARIES-lineage exception scoped in §3) and the model's own computed powers/geometry.

## Recommendation

**Close-eligible.** All MR-WI028-1…10 satisfied, all 9 audit bars POSITIVE, Levels 1–3 clean, standing bars hold. The two findings are cosmetic and do not block close. Per Align ruling 2, owner holds close (`agentic-mbse pm close-item WI-028`); the orchestrator commits after close.

ARTIFACT: work/analysis/20260720-195640_audit_WI-028_handshake-account-scope.md
