# Package annex — `stellarator_tea`

Package fact, not rule. The universal runbook links to a section here at each step
that needs something only true of this package; nothing in this file is an
instruction, and nothing in it is inlined into the runbook.

Six sections, named exactly as the runbook links them.

---

## § Declared ties

`stellarator_09__stellaris__magnet__R0` rides with the major radius group
(`geom__R`, `rb__R`).

It is the same physical quantity under a separately authored attribute. The
magnet-cost model runs Ampère's law on the coil major radius
(`total_kAm = G · B · R0 · r_coil / µ0`), and that radius *is* the plasma major
radius — sweeping `R` while holding `magnet__R0` fixed would price coils for a
machine that does not exist.

Its suffix is `R0`, not `R`, so no suffix scan will ever surface it. That is why the
tie has to be declared rather than found. The tie **data** lives in the manifest
(`manifest.json` → `ties`); this section says why it is there and never restates it.

Known held-fixed semantic duplicates, recorded so a later study does not rediscover
them as surprises: `pb__p_input` and `heating_cost__p_ecrh` are both the 50 MW
installed heating power, and the two `ash_frac` entries carry the same fraction at
different precisions. None of the three is swept today.

---

## § Baseline pin

The pinned baseline point, its headline, and its five expected verdicts live in
`manifest.json` → `baseline`. Today: `R = 12.7 m`, `a = 1.3 m`,
`availability = 0.85`, headline `stellarator_09__stellaris__lcoe_calc__lcoe` =
`275.2642200420774`, all five viability constraints satisfied.

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

The study seam is `oracle_entry.py`, beside this file, and it publishes three things
and nothing else:

| Surface | Contract |
|---|---|
| `evaluate(point)` | qualified entry keys → qualified channel values |
| `operand_bindings()` | `{constraint_id: {source_name: {"kind", "key"}}}` |
| `glue_values(point)` | qualified entry keys → the values the adapter injects per point |

**Parameterization.** A point arrives keyed by the package's own qualified entry
keys. `ENTRY_KEY_TO_ORACLE_INPUT` maps each one to an oracle input name; several keys
carry one quantity (`geom__R` and `rb__R` are both the major radius) and they must
agree, because the oracle can only be given one. Two categories map to no oracle
input at all and say so: glue-fed values the oracle recomputes itself, and the dead
schema fillers. An undeclared key is a mechanical failure, never a silently skipped
one. The oracle's module-global `IN` is saved and restored around every call, and
`_profile_integral` is memoized — exactly, since it depends only on inputs no study
sweeps.

**Return.** 51 oracle outputs are mapped to qualified channels. The era's evidence
layer records only single-field float channels, so 45 of them appear in a study store
and 6 do not: the `pb__*` power-balance fields, which are fields of one multi-field
model. `net_positive` and `recirc_ok` reach their operands through those six, which
is why channel operands resolve from the oracle's return rather than from the store.

**The operand-binding table, and why it exists.** A predicate operand in
`contracts/model_contract.json` carries a short `source_name` and a SysML qualified
name, and neither resolves to a flat package key by construction. Checked against all
five constraints: `recirc_ok.threshold` is constraint-id-prefixed,
`beta_ok.beta_limit` is owner-instance-prefixed, `wall_load_ok.wall_load` is a channel
whose producing block name appears nowhere in the operand, and
**`net_positive.net_electric` resolves to nothing at all** — no parameter and no
channel contains that string; its value is `pb__p_net`. So a generic verifier that
matched names would guess wrong on one of five and guess among three composition rules
on three others. The package publishes the table instead, and the verifier fails
closed on anything it cannot resolve. A tool that guesses is worse than one that
refuses.

Worth knowing before you edit anything here: `oracle_entry.py`'s first channel map
sent the oracle's `annual_om` to `om_cost__annual_om`. The names agree; the numbers
are 158% apart, because the package channel is the *unlevelized* annual O&M. The
right source is `annual_om_unlevelized`. The map is validated against executed
evidence, not read for plausibility.

Known verification-coverage delta (Item 4 audit, 2026-08-20): `p_fus` and
`magnet_capital` are not compared by generic `verify.py` — coverage is the manifest's
objective catalog plus predicate-resolved operands, and those two channels are neither.
Recovering them is a data-only addition to `manifest.json`'s objective catalog (an
Item 3-owned file), not a tool change.

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

## § Loader exception and glue

Current teax main refuses this package's `v1.0.0` seal, so studies run under the era
pin (below) through `era_adapter.py`. That adapter is temporary and states its own
expiry.

**The accept-set is exactly two files.** Of the 139 sealed artifacts in
`contracts/package_contract.json`, exactly two differ from their sealed hashes:

- `inputs/system_design.json`
- `pipelines/mfe_stellarator.yaml`

The adapter runs the era's **full** verification — version gate, authenticated
verifier, per-file hashes — and accepts only if every diagnostic is a `TAMPER` on one
of those two. A different file, a different diagnostic kind, or an era-version
mismatch still refuses. This is a precisely scoped exception, not a relaxation of
sealing, and its scope is held by a negative test that modifies a third artifact.

**The identity is earned, not borrowed.** The adapter does *not* return the sealed
`executable_fingerprint` as the identity of a route that bypassed the seal. It
returns an **effective executable fingerprint** over three declared inputs: the sealed
fingerprint, the actual digests of the two allowed-modified files, and the digests of
its own declared sources. Touch any of them and the identity changes, so a
pre-existing store refuses to resume.

**Declared sources — editing any of these retires every existing store:**
`studies/era_adapter.py`, `studies/oracle_entry.py`, `verify_stellaris.py`. All three
can move a number that is fed into a run. It is a sharp edge, and it is the correct
one; the refusal message names the file whose digest moved.

**Consequence for the pre-capability evidence.** The committed proof-of-life stores
under `study/_work/` were written under the *sealed* fingerprint, which that route
never earned. `verify.py` refuses them for exactly that reason. They stay as executed
evidence of what ran before the capability existed, and they are not re-verified under
the promoted identity because they are not that lineage.

**The glue ledger.**

| Rung | What it supplies that the model does not | Independently verified |
|---|---|---|
| `g1` | The two seal exceptions above: a BOP repoint and three schema fillers. | Yes — every *other* sealed artifact is checked on every load, and both files' actual digests are inputs to the identity. |
| `g2` | Constant injections per proposal: the CAS28 costing constant (2 keys, 5.0 M$), the declared replacement `n_mod` default codegen could not resolve, and three dead `mfe_plant__MFE_Power_Plant__p_*` schema fillers. | Yes — the three fillers are asserted **dead** on every load: nothing in the executed pipeline spec reads them, so they move no number either way. |
| `g3` | `special_materials_capital` (2 keys). CAS27 is a function of the radial-build blanket volume, which the package cannot wire cross-part, so it is recomputed **per point** from the same formula the oracle uses and off-baseline points stay self-consistent. | **No.** Fed identically to the package and to the oracle, so oracle parity verifies the package's arithmetic *given* this value. The CAS27 ingredient itself is not independently checked. `verification_summary.json` says so in `not_independently_verified`. |

### Deletion condition

The stock `ProvisionalPackageLoader` accepts the (regenerated) package with
`strict=True`. When it does, `era_adapter.py` is deleted whole, the study-local
definition swaps this loader for the stock one and `scripts/study/identity.py`'s
sealed emitter, the sealed `executable_fingerprint` becomes the identity again,
`promotion_equivalence.py` is deleted with it, and `oracle_entry.py` stays — it is the
verification seam, not glue. There is no partial retirement and no dormant
compatibility branch.

---

## § Era pin

Studies on this package run against a **read-only git worktree of teax at `fa0e06a`**,
at `/home/reid/1cfe/teax-v1-era` (`packages/teax-simkit` on `sys.path`; override the
location with `TEAX_V1_ERA`).

`fa0e06a` is the commit that built the study layer, and the same v1 era that generated
and certified this package. The adapter **asserts** the pin on every load — it reads
the worktree's HEAD and fails closed naming the expected and found commits — rather
than merely recording it.

**Current teax main refuses this package's `v1.0.0` seal, and that refusal is
principled. It is not to be chased upstream.** Main's fail-closed re-vendor is doing
its job; the package is from an earlier runtime contract. The fix is regenerating the
package, not weakening the loader — and regenerating it is also what retires the
adapter (see § Loader exception and glue → Deletion condition). Nothing in teax or
sysml-codegen is modified by this capability.
