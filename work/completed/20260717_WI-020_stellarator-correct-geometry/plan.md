---
Status: complete
Created: 2026-07-17
Updated: '2026-07-17'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-020 Plan: Stellarator-Correct Plasma Geometry

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths not read.

Owner ruling (2026-07-17): Decision B = B1 (target Table-2 V = 448 m³ at R=12.7); Decision A = **no sigma_v re-solve** — fusion power is a computed output, headline re-baselines.

## Phase 1 — Library: shape factor on `'Plasma Geometry'`

- [x] Add `in attribute f_shape : Real default 1.0;` to `'Plasma Geometry'`; change `V` to `... * f_shape`; update the doc comment (`models/library/analyses/mfe_plasma_scaling.sysml`).
- [x] Mirror the identical edit into the staged copy (`exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml`) — `diff` first to confirm byte-identity of the geometry calc.
- [x] Validate L1 (0 errors) on canonical `models/`.

## Phase 2 — Plant: thread `f_shape`

- [x] `models/designs/generic_mfe/mfe_plant.sysml`: add `attribute f_shape : Real default 1.0;` and `in f_shape = f_shape;` in the `geom` calc block. If the plant-attribute default trips codegen (D4), drop the default and rely on the instance binding.
- [x] Mirror into the staged plant copy.
- [x] Validate L1.

## Phase 3 — Instance: bind factor, rewrite docs

- [x] `models/designs/stellarator_09/stellarator_plant.sysml`: add `:>> f_shape = 0.794259` with citation + the WI-020 shaping note; **delete** the wrong "R/a rounding" cross-check note (lines 250-255).
- [x] Rewrite the `:>> sigma_v` doc comment — value stays `5.985e-23`; remove the back-solve/2700-MW/564-m³ justification; state the 0D-effective reactivity and the visible 2145-vs-2700 gap handed to item 2.
- [x] Lightly clarify the `wall_area` doc note (the "same build that yields plasma_vol = 564" line) — 564 is 1cfe's internal torus volume; the SysML plasma volume is now 448. No value change.
- [x] Mirror into the staged instance copy.
- [x] Validate L1–L6 on canonical `models/`; compare counts to the WI-019 baseline (L1=0, L2=3, L6=105) — zero new issues.

## Phase 4 — Oracle, regen, runner

- [x] `verify_stellaris.py`: add `f_shape=0.794259` to `IN`; apply it in the `V` line. sigma_v unchanged.
- [x] Regenerate: `sysml-codegen snapshot` over the staged models → `bridge_v11_generate.py` (env from `~/1cfe/fusion-tea/.env`).
- [x] `run_stellaris.py`: change the V assertion 564 → 448 (tol 2); refresh other asserted headline values to executed.
- [x] Run `run_stellaris.py` — bit-exact vs the updated oracle; record V=448, computed p_fus (~2145), and the full re-baselined headline.

## Phase 5 — Handshake (closure proof) + sensitivity

- [x] Re-run `handshake_1costingfe.py`; confirm SV-025 (six power channels) and SV-026 (power-scaled account gap) are **numerically unchanged** — the D2 proof that f_shape=1.0 leaves 1cfe's torus point intact.
- [x] IFE regression: re-run SV-023 anchors (no IFE files touched) — still passing.
- [x] Confirm all three viability asserts (beta, wall load, TBR) pass at the lower power.
- [x] sigma_v sensitivity: record p_fus and LCOE at a small sweep around 5.985e-23 (supports the owner's "test various inputs at codegen").

## Phase 6 — Close

- [x] `pm update-validation SV-027 --status passing`.
- [x] Record the re-baselined headline + sensitivity in this plan's Implementation Record and `.project/CURRENT_WORK.md`; note the torus/448 gap closed and the 2145-vs-2700 gap handed to item 2; update the STALE-BASIS annotations to the new p_net.
- [x] `pm close-item WI-020`.

## Implementation Record

**Completed 2026-07-17.** All six phases landed; SV-027 passing.

**Model change (small, as designed):**
- `'Plasma Geometry'` (`mfe_plasma_scaling.sysml`) gained `in attribute f_shape : Real default 1.0;`; `V = 2·pi²·R·a²·κ·f_shape`. Doc updated.
- `mfe_plant.sysml`: plant attribute `f_shape : Real default 1.0` threaded through the `geom` block. The plant-attribute default compiled cleanly through codegen (D4 fallback not needed).
- `stellarator_09/stellarator_plant.sysml`: `:>> f_shape = 0.794259` bound with citation + shaping note; the wrong "R/a rounding" cross-check note deleted; sigma_v doc rewritten (value unchanged, back-solve claim removed, 2145-vs-2700 gap made visible); headline block, wall_area note, and three STALE-BASIS annotations refreshed to the new p_net.
- Staged e2e copies mirrored (geometry file byte-identical; plant/instance carry only the pre-existing codegen adaptations).

**Validation:**
- L1 = 0 errors; L2 = 3 (pre-existing IFE); L3/L4/L5 pass; L6 = 105 (pre-existing IFE + canonical rollups). Zero new issues — matches the WI-019 baseline exactly.
- Codegen: snapshot + V11 bridge regenerated; the same 3 known rollup offenders bridged, no new offenders from `f_shape`.
- `run_stellaris.py`: pipeline bit-exact vs oracle at rel 1e-9 on every channel, per-account cost, rollup, and LCOE. Headline check passes.
- **Handshake closure**: first re-run FAILED (−20.6%) — the generated params carry the instance's f_shape=0.7943, so the handshake's torus point was shrunk. Fixed by explicitly injecting `geom__f_shape = 1.0` (`handshake_1costingfe.py`). Re-run: SV-025 six power channels +0.000%, formula-isolation −7.63e-08 worst; SV-026 power-scaled accounts +0.00% — **byte-identical to the WI-019 result**. This is the D2 closure proof; the "default 1.0 is automatic" assumption in the spec was wrong and is corrected in the SV-027 record.
- IFE regression SV-023: $252.30 / $68.69/MWh — unchanged.
- Viability: wall_load 2.14 < 4.95, beta 0.0276 < 0.05, TBR 1.074 > 1.05 — all pass.

**Re-baselined Stellaris headline (V=448):** fusion power **2144.5 MW** (was 2700, computed not pinned), p_th 2538.0, gross 845.2, **net 578.0 MW**, rec_frac 0.316, q_eng 3.16, total **$9.683B**, **LCOE $247.34/MWh**, magnet **$4.392B (45.4%, unchanged — power-independent)**. Net electric and LCOE land near the pre-WI-019 range: WI-019's power-balance gain and this volume correction nearly cancel.

**sigma_v sensitivity (owner's "test various inputs at codegen"):**

| sigma_v [m³/s] | p_fus [MW] | p_net [MW] | q_eng | LCOE [$/MWh] |
|---|---|---|---|---|
| 5.000e-23 | 1791.6 | 445.8 | 2.69 | 312.10 |
| **5.985e-23 (current)** | **2144.5** | **578.0** | **3.16** | **247.34** |
| 6.500e-23 | 2329.0 | 647.2 | 3.40 | 223.91 |
| 7.000e-23 | 2508.2 | 714.3 | 3.63 | 205.45 |
| **7.535e-23 (→ p_fus 2700, old WI-019 headline)** | **2699.9** | **786.1** | **3.87** | **189.13** |
| 8.000e-23 | 2866.5 | 848.5 | 4.08 | 177.17 |

The old 2700 MW / $189 headline is exactly recoverable at sigma_v = 7.535e-23 — the design point is a visible input choice, not baked in.

**Surfaced (owner attention):**
1. **SV-016 band** ("Q_eng ~10–40") reads low at q_eng = 3.16 — carried open from WI-019, still `pending`. Owner adjust/annotate.
2. STALE-BASIS pass-throughs: at p_net 578 they are nearly back on their 575.3 basis (WI-019 had pushed them to 786). Annotations updated; recomputation still a Stage-3 account item.
3. The 2145-vs-2700 fusion-power gap is now visible in the model — the target of item 2 (predictive confinement).
