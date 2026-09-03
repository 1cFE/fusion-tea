# Package annex — `stellarator_tea`

Package fact, not rule. The universal runbook links to a section here at each step
that needs something only true of this package; nothing in this file is an
instruction, and nothing in it is inlined into the runbook.

Four sections, named exactly as the runbook links them. The two the runbook treats as optional -- `§ Loader exception and glue` and `§ Era pin` -- do not exist for this package: since the stellarator model migration (2026-08-21) it is sealed at runtime contract 2.0.0 and runs on stock teax with no adapter and no glue (`studies/AFTER_MIGRATION_RECORD.md`).

---

## § Declared ties

`stellarator_09__stellaris__magnet__R0` rides with the major radius
`stellarator_09__stellaris__R` (one plant-level entry point since the model migration;
before it, the `geom__R` / `rb__R` fan-out).

It is the same physical quantity under a separately authored attribute. The
magnet-cost model runs Ampère's law on the coil major radius
(`total_kAm = G · B · R0 · r_coil / µ0`), and that radius *is* the plasma major
radius — sweeping `R` while holding `magnet__R0` fixed would price coils for a
machine that does not exist.

Its suffix is `R0`, not `R`, so no suffix scan will ever surface it. That is why the
tie has to be declared rather than found. The tie **data** lives in the manifest
(`manifest.json` → `ties`); this section says why it is there and never restates it.

`stellarator_09__stellaris__p_ecrh` rides with `stellarator_09__stellaris__p_input`
(declared by `20260901-sustainment-fence`, the first study to sweep installed
heating): both are the installed ECRH power — the power balance consumes the coupled
50 MW and the heating account prices the same 50 MW — so sweeping one while holding
the other would heat the plasma with a system that was never bought. Formerly listed
here as a known held-fixed semantic duplicate; promoted to a tie when the axis went
live. The remaining known duplicate: the two `ash_frac` entries carry the same
fraction at different precisions; neither is swept today.

---

## § Baseline pin

The pinned baseline point, its headline, and its expected verdicts live in
`manifest.json` → `baseline`. Today (WI-036 regeneration, 2026-09-03): `R = 12.7 m`,
`a = 1.3 m`, `availability = 0.85`, headline
`stellarator_09__stellaris__lcoe_calc__lcoe` = `307.08712042841586`, **nine**
verdicts — eight satisfied and `sustainment_ok` **expected violated** (the disclosed
WI-037 baseline state: required sustained coupled heating ~90.6 MW vs 50 installed).
WI-036 added the ninth, `cond_strain_ok`, and left the headline untouched: the
winding-pack sizing chain is neutral at the design point by construction (`wp_side`
reproduces 0.360000 m and `c_coil` 25.0 m from the new levers `j_wp` and `k_coil`),
so all nine anchors reproduce exactly across the regeneration.
The baseline also sits at exact equality on the conductor ceiling (B_peak 24.90 T vs
B_max 24.9, `<=` satisfied by the WI-035 one-ulp-low design convention) — a
by-construction fact of the design point, not a discovery any study makes.

The route executes exactly that point before preflight runs and deposits
`baseline_result.json`; preflight's `baseline_headline` gate compares the two at
rel < 1e-9 and matches the verdicts by `source_local_identity`.

**After the package is regenerated, the baseline and the ties are pinned against a
generation that no longer exists, and preflight fails until they are re-declared.**
That is `manifest_currency`, and it is deliberate: the pin is a claim about a
specific package, and a stale claim gating a new package is worse than no gate.

---

## § Oracle

The independent oracle is `exploration/stellarator_e2e/verify_stellaris.py`, a pure
Python recompute of the whole plant chain that shares no code with the generated
package. It is **not modified** by the study capability — that independence is the
entire value of comparing against it.

The study seam is `oracle_entry.py`, beside this file, and it publishes two things
and nothing else:

| Surface | Contract |
|---|---|
| `evaluate(point)` | qualified entry keys → qualified channel values |
| `operand_bindings()` | `{constraint_id: {source_name: {"kind", "key"}}}` |

**Parameterization.** A point arrives keyed by the package's own qualified entry
keys. `ENTRY_KEY_TO_ORACLE_INPUT` maps each one to an oracle input name. The map is not
fixed: it grows with each study that moves a new key (four keys at the migration;
WI-030's magnet and profile keys and the power-cycle study's block and discount-rate
keys since -- finding `20260821-power-cycle-ab#4`, `DISCOVERY_LOG.md`). Should two keys ever carry one quantity
again they must agree, because the oracle can only be given one. An undeclared key is a
mechanical failure, never a silently skipped one. The oracle's module-global `IN` is saved and restored around every call, and
`_profile_integral` is memoized — exactly, since it depends only on inputs no study
sweeps.

**Return.** 52 oracle outputs are mapped to qualified channels, CAS27
(`special_materials_capital`) among them since the migration -- the oracle recomputes it
from its own blanket volume, so parity verifies it for the first time. The evidence
layer records only single-field float channels, so 46 of them appear in a study store
and 6 do not: the `pb__*` power-balance fields, which are fields of one multi-field
model — and since WI-037 the `sustain__*` sustainment fields share the same limitation (`20260901-sustainment-fence#3`); their per-point values are exported oracle-side in that study's `oracle_operands.csv`. `net_positive` and `recirc_ok` reach their operands through those six, which
is why channel operands resolve from the oracle's return rather than from the store.

**The operand-binding table, and why it exists.** A predicate operand in
`contracts/model_contract.json` carries a short `source_name` and a SysML qualified
name, and neither resolves to a flat package key by construction. Checked against all
six constraints: `recirc_ok.threshold` is usage-prefixed (`recirc_ok__threshold`),
`beta_ok.beta_limit_in` is owner-instance-prefixed and carries the library formal's
`_in` suffix while the key does not, `wall_load_ok.wall_load` is a channel
whose producing block name appears nowhere in the operand, and
**`net_positive.net_electric` resolves to nothing at all** — no parameter and no
channel contains that string; its value is `pb__p_net`. So a generic verifier that
matched names would guess wrong on one of six and guess among three composition rules
on three others. The package publishes the table instead, and the verifier fails
closed on anything it cannot resolve. A tool that guesses is worse than one that
refuses.

Worth knowing before you edit anything here: `oracle_entry.py`'s first channel map
sent the oracle's `annual_om` to `om_cost__annual_om`. The names agree; the numbers
are 158% apart, because the package channel is the *unlevelized* annual O&M. The
right source is `annual_om_unlevelized`. The map is validated against executed
evidence, not read for plausibility.

Known verification-coverage delta (Item 4 audit, 2026-08-20): `p_fus` is not
compared by generic `verify.py` — coverage is the manifest's objective catalog plus
predicate-resolved operands, and that channel is neither. `magnet_capital` was in the
same position until Item 6 added it to the objective catalog (design D9, 2026-08-21);
recovering `p_fus` is the same data-only addition, not a tool change.

---

## § Validity masks

**`R > a + 2.25 m`.** Points failing this are excluded from the design-search grid
before execution.

This is a **derived geometric bound from held-fixed inputs, not a design screen.**
The plasma minor radius plus the radial-build stack must fit inside the major radius
or the torus self-intersects — the point is not a worse design, it is not a machine.
The 2.25 m is the sum of the held-fixed layer thicknesses, in order:

| Layer | m | | Layer | m |
|---|---|---|---|---|
| vacuum | 0.10 | | vessel | 0.10 |
| first wall | 0.05 | | coil | 0.30 |
| blanket | 0.80 | | gap 2 | 0.10 |
| reflector | 0.20 | | LT shield | 0.15 |
| HT shield | 0.20 | | | |
| structure | 0.15 | | **total** | **2.25** |
| gap 1 | 0.10 | | | |

If any of those thicknesses is ever swept or re-declared, the bound moves with it and
the exclusion must be recomputed rather than carried forward as the number 2.25.

The exploration windows themselves — `R ∈ [4.0, 20.0] m`, `a ∈ [0.80, 2.20] m`,
`availability ∈ [0.50, 0.95]` — are agent-chosen so the constraint boundaries sit in
frame. They are **not sourced design bounds**, and a study run inside them is not
testing whether the window is right.

---
