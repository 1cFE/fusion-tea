# T-006 early independent oracle review — 2026-09-15

**Verdict: FINDINGS.** Nominal energy/cost accounting and dormant preservation match the reviewed design. New published-input domain checks need repair before this oracle validates sensitivity cases. This is an early oracle review; native generation, publication completeness and coupled integration remain separately owed.

**Scope:** non-author review of the working-tree changes in `exploration/stellarator_e2e/verify_stellaris.py` and `studies/oracle_entry.py`, against the already reviewed WI-059 design and its predictions. No source re-review, model/test edits or batteries. Read `candidate_oracle.json` and `entering_oracle.json` under the item's evidence directory. Read-only numerical probes used `.codex-test/run`; no shared files were changed by the probes.

## Must fix

1. **Thermal helper admits invalid physical inputs.** Its finite/nonnegative list omits Lorenz constant, Stefan–Boltzmann constant and turn current. Probes accepted `cryo_L0=NaN` and infinite turn current, returning NaN/infinite thermal and drive outputs. With `cryo_sigma_SB=-1`, the helper returned approximately −4.7 billion W cold heat while its total-warm check passed. Require finite positive physical constants, finite turn current, and finite nonnegative circumference/pack geometry before live arithmetic; retain the declared absolute-current convention. Effective emittance must lie in [0,1]. Check finite derived thermal outputs as well as nonnegative total warm load. Keep the early disabled branch so dormant inputs are not spuriously evaluated.
2. **New support/nuclear/accounting inputs lack physical domains.** A zero structure density produces incidental `ZeroDivisionError`; negative support coefficient produces negative support mass/cost; `cryo_q_nuc_structure=-35.5` produces negative total cold heat at the nominal candidate. Require finite positive structure density; finite nonnegative heating density and support coefficient; finite positive support exponent for an active mass fit; and finite nonnegative support mass. Require the accounting fractions to remain in their declared [0,1] range. Match the supported native failure contract with deliberate diagnostics. This does not require tightening unrelated inherited inputs.

## Checks passed

- All saved candidate outputs exactly equal the current oracle calculation. Its actual cold area is 2688 m², distinct from the explicitly illustrative 3360 m² source witness. The cold inventory is 9.586022 kW, shield inventory 41.599954 kW, direct lead-plus-joint electricity 0.050267327 MW, total refrigeration 2.137762109 MW, and support mass 11,615,604.483 kg.
- Warm radiation/support heat subtracts the portion sent onward to the cold stage. Lead direct power and 7.5 kW joint supply enter coil power once; their refrigeration remains a separate consumption. Residual uplift applies to old/residual cold terms only. No old nuclear term is added twice. Cryogenic capital reads total refrigeration and excludes direct coil supply.
- Support pricing uses the chosen total mass with legacy casing fraction zero. CAS22.1.5 uses the explicitly declared residual allowance; no source-based partition is implied.
- Disabling the inventory, setting support coefficient zero and legacy casing fraction one, retaining residual fraction one and zero structure-nuclear/joint-drive controls reproduces **all 168 entering oracle outputs exactly**. The disabled helper returns zeros even with otherwise unsupported new stage inputs.
- New map entries distinguish aggregate/cold/shield refrigeration, direct coil-drive sum, cold-load sum, mass and component thermal channels. Their semantic directions match the design. Actual generated identifiers and complete native/oracle publication coverage must be confirmed after generation; this early review does not certify them.

The repaired diff can be rechecked here, then reused by the coupled integration reviewer.
