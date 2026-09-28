---
Status: complete
Created: 2026-08-30
Updated: '2026-09-01'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-035 Plan: Magnet Closure Implementation

**Approved 2026-08-30** `[AGENT] (approval delegated by owner 2026-08-30)` — same delegation as the design.

## Source documents

Design `./design.md` (primary — decisions D1–D8, § Proposed design, § Expected design-point values, § Implementation checklist); spec `./spec.md` (MR-WI035-1..7, SV-038/039/040); epic `work/backlog/epic-mfe-cost-modeling.md`.

## Design summary

Coil current becomes the lever: a new field calc EXPOSEs computed `B_axis` into `magnet.B` (all consumers unchanged); a winding-pack stress constraint with computed operand is asserted; magnet capital splits into winding-pack + casing-structure accounts with the old lump kept as a `magnet_capital_1cfe` comparison channel. See design D1–D8; do not re-derive values — the § Expected design-point values table is the checklist.

## Prototype baseline

`scratchpad/wi035_proto/proto_magnet_closure.sysml` — all new defs plus the EXPOSE + assert wiring shape, L1 "Checks passed!" (`python -m syside check`, license via `set -a; source ~/1cfe/agentic-mbse/.env; set +a`). Level 4–6: no findings at design; the offender-list bar (6 pre-existing, zero new) is the final gate.

## Phases

### Phase 1 — Library definitions
- [x] `models/library/analyses/mfe_magnet_field.sysml` (NEW): `'Coil Set Axis Field'`, `'Winding Pack Stress'` (design D2/D3 stencils, full Source/Ref/Basis docs).
- [x] `models/library/analyses/mfe_viability.sysml`: append `'Winding Pack Stress Limit'` (design D3).
- [x] `models/library/analyses/mfe_magnet_cost.sysml`: add `'Winding Pack Cost'`, `'Magnet Structure Cost'`; update `'Magnet Coil Cost'` doc to comparison-form (design D4/D5/D6).
- [x] `models/library/analyses/mfe_account_costs.sysml`: `'Aux Cooling Cost'` gains `aux_cost`/`cryo_cost` outs, `cost` = sum unchanged (design D7).
- [x] `models/library/cost_structure/mfe_power_core.sysml`: `'Magnet System'` +12 attributes (design D8 list), doc updated.
- [x] Checkpoint: L1 on the five files.

### Phase 2 — Generic plant wiring
- [x] `models/designs/generic_mfe/mfe_plant.sysml`: `field_calc`, `:>> B = field_calc.B_axis` EXPOSE in the magnet part, `wp_stress`, `assert wp_stress_ok`, `winding_pack_cost` + `magnet_structure_cost` calcs, `magnet.capital_cost` rebind to the sum, exposed `magnet_capital_1cfe` and `cryoplant_capital` (design § Cross-file bindings).
- [x] Checkpoint: L1 on the plant; dataflow acyclic per design.

### Phase 3 — Instance rebinds + twins
- [x] `models/designs/stellarator_09/stellarator_plant.sysml`: delete `:>> B = 9.0`; add the 12 literal bindings with image-verified Source/Ref/Basis (design D8 names; § Research findings citations; `m_casing` doc names the floor-bound seam; `k_link`/`f_set`/`k_sigma` docs show the printed-pair arithmetic).
- [x] Mirror every edit byte-identically into `exploration/stellarator_e2e/models/**`.
- [x] Checkpoint: L1 both trees; `diff -r` between trees clean for the touched files.

### Phase 4 — Validation + record
- [x] Offender bar: L1 errors 0; L2+ offender list = the 6 pre-existing, zero new.
- [x] `tests/models` green (re-derive the census per the suite's own instruction if the semantic fingerprint moved — expected: it will).
- [x] Static design-point arithmetic re-checked against design § Expected design-point values.
- [x] Implementation record appended here: what changed, deviations, headline notes. SV-038/039/040 stay `pending` until executed channels exist (post-`integrate`, a later task).

## Validation strategy

L1 after each phase (`python -m syside check`); the offender-list and `tests/models` bars at Phase 4. Executed-channel verification (expected-values table, constraint verdicts, SV flips to `passing`) belongs to the post-`integrate` execution, out of this item per spec.

## Risks

Carried from design § Risks (EXPOSE-through-codegen with recorded fallback; float64 statement order; casing floor bound). Plan-level addition: `tests/models` may pin the semantic fingerprint — follow the failing test's own re-derivation instruction rather than hand-editing baselines.

## Implementation record — 2026-08-30

All four phases complete, both trees. Evidence:

- **Phase 1–3 edits**: `models/library/analyses/mfe_magnet_field.sysml` (NEW: 'Coil Set Axis Field', 'Winding Pack Stress'); 'Winding Pack Stress Limit' appended to `mfe_viability.sysml`; 'Winding Pack Cost' + 'Magnet Structure Cost' + 'Magnet Capital' added to `mfe_magnet_cost.sysml` ('Magnet Coil Cost' doc updated to comparison-form); 'Aux Cooling Cost' split into `aux_cost`/`cryo_cost` outs with `cost` their exact sum (bit-identical arithmetic); 'Magnet System' +12 attributes; plant wiring per design § Cross-file bindings; instance: `:>> B = 9.0` retired with the cross-check note, 12 literal bindings added with image-verified Source/Ref/Basis. All seven touched files byte-identical across canonical and twin trees (`cmp` clean).
- **Deviation from design (recorded)**: the D6 rollup is expressed as a library calc def `'Magnet Capital'` (in: winding, structure; out: capital_cost) rather than an inline plant sum, so `magnet.capital_cost` stays a *reference* redefinition — inside the codegen envelope the WI-030 gotcha excludes arithmetic redefinitions from. Value-identical.
- **Validation**: L1 pass, both trees. Full L1–L6 sweep: offender set **identical to the HEAD baseline** modulo line shifts (true baseline captured via scoped stash with the new file moved aside; 5 L2 literal-binding WARNs + 5 L6 rollup ERRORs, all pre-existing; the validator lists at most 5 rows per level — the earlier apparent delta was the display cap plus the untracked new file leaking into the first baseline attempt).
- **tests/models**: 48 passed / 13 skipped. Two suite-maintenance edits per the suite's own rules: `tests/model_families.py` MFE family gains `analyses/mfe_magnet_field.sysml` (owned-paths coverage test named it); `tests/models/data/mfe_census.json` re-derived from a scratch-generated package per the census test's instruction — semantic fingerprint `f08daa7b…` → `819a5a05…`, entry points 173 → 186 (−`magnet__B`; +the 12 design levers; +`field_calc__{mu0,two_pi}` library defaults). The delta equals design D8 exactly.
- **Pipeline wiring confirmed** (scratch package): `field_calc` emits `B_axis` consumed by `peak_field_calc.B_axis_in`, `beta_calc.B_in`, and `magnet_cost.B`; `wp_stress`, `winding_pack_cost`, `magnet_structure_cost`, `magnet_capital_rollup` all present as modules. Design Risk 1 (EXPOSE dropped) did not occur.
- **Not in this item** (per spec/plan): package regeneration/verification/pinning (`integrate` seam), executed-channel checks of the § Expected design-point values table, SV-038/039/040 flips to `passing`, study re-runs. Headline delta (magnet capital $6.3235B → $5.4010B expected) is recorded as *expected*, to be confirmed at execution.
