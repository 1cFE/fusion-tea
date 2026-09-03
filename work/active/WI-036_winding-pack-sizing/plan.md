---
Status: active
Created: 2026-09-03
Updated: 2026-09-03
Related Artifacts:
  Spec: work/active/WI-036_winding-pack-sizing/spec.md
  Design: work/active/WI-036_winding-pack-sizing/design.md
---

# WI-036 Implementation Plan

Phases run in order; each ends at a validation checkpoint. Mechanism is fixed by the design (D1–D8); this file sequences the work and records what actually happened.

## Phase 1 — Library calc defs (concept-agnostic)

- [x] `mfe_magnet_field.sysml`: add `'Winding Pack Sizing'` (D1), `'Coil Winding Length'` (D3), `'Winding Pack Cold Volume'` (D2), `'Conductor Strain'` (D4).
- [x] `mfe_viability.sysml`: add `constraint def 'Conductor Strain Limit'` (D5).
- [x] `mfe_power_core.sysml`: declare the new magnet attributes — `j_wp`, `f_wp_vol`, `k_coil`, `E_wp`, `f_cond`, `eps_cond_allow`.
- **Checkpoint:** Level 1 parse clean on every touched file.

## Phase 2 — Generic plant wiring

- [x] `mfe_plant.sysml`: calc usages for the four new calcs; `wp_side` and `c_coil` become EXPOSEd computed values rather than instance literals; the cryo chain's `vol_cold` receives the computed winding-pack volume; assert `cond_strain_ok`.
- **Checkpoint:** Level 1 parse; the stress calc consumes the computed `wp_side`.

## Phase 3 — Instance rebinds

- [x] `stellarator_plant.sysml`: bind `j_wp`, `f_wp_vol`, `k_coil`, `E_wp`, `f_cond`, `eps_cond_allow` with full `Source`/`Ref`/`Basis` doc comments; retire the `wp_side` and `c_coil` literals to computed; `vol_cold_cryo` receives the computed volume while remaining a settable slot (MR-WI036-3).
- **Checkpoint:** design-point reproduction — `wp_side` 0.360000 m, `c_coil` 25.0 m, `vol_cold_cryo` 136.56 m³, each to the design's tolerance (D7).

## Phase 4 — Regeneration, battery, restatement

- [x] Record the MR-WI036-11 committed-study restatement **before** regenerating.
- [x] Regenerate the package; run `tests/models` and `tests/study`.
- [x] Re-derive fixture expectations from live evidence, never patched to match. Named surface, per goal review constraint 6: runner anchors, known-answer fixtures, the census, suite constants, the manifest, and the ANNEX.
- **Checkpoint:** battery green; every changed expectation carries its own explanation.
- [x] **Verify `vol_cold_cryo` survives as a settable key in the generated package.** If it does not, the WI-032 ruling and the sizing chain are in genuine conflict — that is a finding to surface, not to paper over.

## Implementation record

(filled in as phases complete)

### MR-WI036-11 — committed-study restatement, recorded before regeneration (2026-09-03)

This increment changes what the model means, so committed study records are restated rather than silently broken. Each record stands at its own pin; none is re-run.

**What changed semantically.** `wp_side` and `c_coil` are no longer settable entry points — the winding pack is sized by the current it carries (`j_wp` is the new lever) and the winding length follows machine scale (`k_coil` is the new lever). `vol_cold_cryo` changes meaning from "total winding-pack cold volume" to "additional cold volume beyond the winding pack", and is bound to zero here because the computed chain now carries the whole printed cold mass. A new constraint, `cond_strain_ok`, joins the viability set.

**Consequences for the four prior committed studies.**

- `20260823-magnet-technology-ab`, `20260821-power-cycle-ab`, `20260829-p-pump-fence`, `20260830-stress-fence` — already non-replayable as written at pin `35e922c5…` per the WI-037 restatement; this increment adds two more retired keys (`wp_side`, `c_coil`) and one changed key meaning (`vol_cold_cryo`).
- `20260901-sustainment-fence` — the goal's own entering evidence. Its swept `I_coil` range 8–24 MA held `wp_side` at 0.36 m throughout, which this increment makes impossible: the pack now sizes with current. **Its stress-fence findings are therefore a fixed-pack reading, and a replay would not reproduce them.** The record stands at its own pin and its findings remain valid *for the machine it described*; the goal's `evidence/R1_deadlock_recount.md` already states the implied winding-pack current density that reading carried (119 → 154 A/mm² across the sweep).
- Any replay of any of the five must drop `wp_side` and `c_coil` from its point specification, re-read `vol_cold_cryo` under its new meaning, and expect an eighth constraint in the verdict set.

**Fixture and suite surface named in advance** (goal review constraint 6, and the L-006 budget of ~30 sites): runner anchors, known-answer fixtures, the census, suite constants, the manifest, and the ANNEX. Expectations are re-derived from live evidence after regeneration, never patched to match.

## Implementation record

**Phases 1–3 (2026-09-03).** Four library calc defs added (`Winding Pack Sizing`, `Coil Winding Length`, `Winding Pack Cold Volume`, `Conductor Strain`), one constraint def (`Conductor Strain Limit`), six magnet attributes, plant wiring, and instance rebinds. Level 1 clean throughout. Level 2 reports 12 warnings — **verified pre-existing**: the same 12 on the stashed tree, so this item added none.

**One mechanism change forced by the toolchain, and it improved the design.** The first plant wiring put the additive cold-volume term in the calc input binding (`in vol_cold = wp_volume.vol_cold_wp + vol_cold_cryo`). The pinned codegen refused it — `SI_EXPRESSION_SOURCE_UNSUPPORTED`: an input binding must be a single reference, not an expression. The arithmetic moved inside `Winding Pack Cold Volume` as a `vol_extra` input, which is where it belonged anyway. Not a workaround: the calc is the right home for arithmetic.

**Phase 4 (2026-09-03).**

- Staged model twin synced (`exploration/stellarator_e2e/models/`), byte-identical to the canonical five files.
- Snapshot recaptured; package regenerated with `--preserve-handwritten --smart-regen`. All four new calcs came back `AUTO_IMPLEMENTED = True` — the codegen compiled the arithmetic, including `** 0.5`. No handwritten implementation was needed.
- **Design point reproduces every one of the nine anchors exactly** — LCOE 307.087120, total capital 14,542,872,713.455379, p_net 743.910232, q_eng 3.078430, rec_frac 0.324841, magnet share 37.138687, CAS70, CAS80, and the 1cfe comparison channel. The sizing chain is exactly neutral at the design point, by construction (D7): `wp_side` reproduces 0.360000 m, `c_coil` 25.0 m, cold volume 136.56 m³.
- **`cond_strain_ok` evaluates satisfied at the design point**, as D5 predicted. Verdicts go 8 → 9; `sustainment_ok` remains the one expected violation (WI-037, disclosed, never tuned).
- Oracle bit-exactness holds (`p_rad`, `p_aux_required` at reldev 0.00e+00) and the CAS72 guard-live spot-check passes.

**Fixtures re-derived from live evidence, never patched to match:**

| site | change | why |
|---|---|---|
| `tests/models/data/mfe_census.json` | 193 → 197 entry points; new semantic fingerprint | re-derived by running the suite's own `_generate`/`_contract`/`_by_entry_type` helpers against a freshly generated package |
| `run_stellaris_single.py` `EXPECTED_VERDICT_COUNT` | 8 → 9 | `cond_strain_ok` added |
| `run_stellaris_single.py` banner and parity message | "EIGHT"→"NINE", "seven satisfied"→"eight satisfied" | same |
| `studies/study_route.py` `EXPECTED_CONSTRAINT_COUNT` | 8 → 9 | same |

**Census delta is exactly what the design predicted.** Retired as entry points: `wp_side`, `c_coil`. Added: `j_wp`, `f_wp_vol`, `k_coil`, `E_wp`, `f_cond`, `eps_cond_allow`.

**MR-WI036-3 verified, not assumed.** `stellarator_09__stellaris__vol_cold_cryo` **survives as a settable entry point** in the regenerated census. The standing `[OWNER 2026-08-27]` WI-032 ruling holds: the chain behind the input is modelled, the input itself is not retired. The plan's Phase 4 check was written to catch the opposite outcome and would have reported it as a genuine conflict.

**`tests/models`: 48 passed, 13 skipped** — the WI-037 baseline count, green.
