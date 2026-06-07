# 1costingfe Model Update: FRC w/ Direct Conversion (Helion Energy)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/iter-3/model_setup.py` and apply
**targeted edits** based on the assessment findings below. Use the Edit tool — do
NOT rewrite the file from scratch, and do NOT restructure conforming code.

## Validator Contract (read this; do NOT go read the validator source)

Your output is judged by four validators run against the bytes on disk. Every
requirement they enforce is stated **here** — exhaustively. **Do not Read or
grep `scripts/lib/validators.py`, `scripts/lib/canonical_accounts.py`, the
costingfe source, or the orchestrator code to "check what's required" — the
contract is below. Reading those files is the single biggest time sink in
this step and is forbidden unless an assessment finding *explicitly* points
at one of them.**

1. **Python syntax** — file must `ast.parse()` clean.
2. **File modified** — the file's SHA-256 must change from the prior model.
   Editing in place satisfies this; copying the file unchanged does not.
3. **Three-forward contract** — module-level bindings, in this order:
   `spec`, `P_native`, `model = CostModel(...)`, `generic = generic_reference(model, spec, P_native)`,
   `overrides = [ ... ]`, `native, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`,
   then `print_cas_breakdown(generic, native, result_1gw, overrides)`. Do
   not inline a two-knob `forward()`. Do not drop `generic`.
4. **Override registry** (the validator that previously sent agents on
   archaeology expeditions — full contract here):
   - `overrides` must be a module-level **list literal of dict literals**
     (`overrides = []` is fine if there are none).
   - Each entry has **all six** fields: `account`, `value`, `enabled`,
     `provenance`, `source`, `rationale`. `provenance ∈ {"direct", "derived"}`.
   - `account` must be one of the concept's canonical accounts (already
     listed in the "Canonical account schema" section below — do not look it
     up elsewhere).
   - **Forbidden rollup accounts** (rejected outright): `C220111`, `C220000`,
     `C220100`, `C220200`, `C220300`, `C220400`, `C220500`, `C220600`,
     `C220700`. To express "this concept assembles more simply," override
     `installation_frac` via `costing_overrides`, not the C220111 dollar
     amount.
   - `value` may be a **number**, a **constant numeric expression** (e.g.
     `260.0 * 1.34`), or an **expression over `generic`** (e.g.
     `0.70 * generic.costs.cas21`). It **MUST NOT** reference `native`,
     `result_1gw`, or `result` (wrong reference frame).
   - Literal `value` must satisfy `|value| <= 5e4` (M$, never raw $).
   - **Disabled** entries (`enabled: False`) must carry a 7th field
     `blocked_by: "<org>/<repo>#NN"` (e.g. `"1cFE/1costingfe#42"`).
   - Every entry must declare `cost_basis: "noak"`. The framework runs
     `noak=True`; `foak`, `conceptual_design`, `vendor_target`, and
     `unspecified` are rejected. Non-NOAK published values: either disable
     with `blocked_by`, or apply a documented learning-curve adjustment in
     `rationale` and declare `cost_basis: "noak"`.
   - No two entries may share an `account`.

## Self-verification budget

You may run the edited model at most **twice** as a self-check:

- Once after your edits to confirm it executes and prints a CAS breakdown.
- (Optionally) once more if a *specific finding* requires you to numerically
  verify a value you changed.

Each `uv run python` cold-boot costs ~30s. Do not write ad-hoc test scripts
under `/tmp/` to probe library internals — if the model runs and the
override registry above is satisfied, you are done.

## Operational constraints

- This is an orchestrated pipeline run. **Do not write to your auto-memory**
  (`~/.claude/projects/.../memory/`) and do not take open-ended exploratory
  actions outside the scope of the findings below.
- If you discover a library bug while editing, **do not** investigate or
  fix it — record it as a `blocked_by: <org>/<repo>#NN` on the affected
  override (file the tracker issue out of band).

## Preserve the three-forward contract

The file already follows the canonical shape; keep it:
1. `spec` dict (design-point inputs only) + `P_native`
2. `model = CostModel(...)`
3. `generic = generic_reference(model, spec, P_native)` — the mandatory
   overrides-off forward (forward 1), the reference a relative override is written against
4. `overrides = [ ... ]` — six-field registry entries
5. `native, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`

with `model`, `generic`, `native`, `result_1gw` at module level and the
`print_cas_breakdown(generic, native, result_1gw, overrides)` call retained. Do
not convert the helper call into an inline two-knob `forward()` (the contract
validator rejects it), do not drop the mandatory `generic` line, and do not
re-introduce `# DEFAULT:` comments or the uniform financial parameters
(`availability`, `lifetime_yr`, `interest_rate`, `inflation_rate`) into `spec`.
**Do not re-introduce power-conversion efficiencies (`eta_th`, `eta_de`,
`eta_dec`) into `spec`** — these are ENUM-driven; the way to express a
different value is to add an upstream ENUM member in costingfe, not a per-
concept override. `f_dec` (DEC fraction) MAY appear in `spec` with provenance —
it's a physics+architecture property, not a hardware-efficiency claim.
A relative override references `generic` (never `native` or `result_1gw`).

**Low archetype-fit concepts: do not empty `spec`.** When the frontmatter
declares `Archetype-Fit: Low`, the prior model may still have a populated `spec`
expressing the concept's actual geometry / physics using canonical kwargs (even
where the archetype isn't a perfect cost match). **Preserve those entries** and
only edit specific fields if a finding calls for it. Replacing a populated
low-fit `spec` with `spec = dict()` is a regression — the library would fall
back to pure archetype YAML defaults that carry zero signal for this concept's
actual machine. Cost-side overrides (the registry below) are where the "Low
fit" caveat properly lives.

**Archetype-specific spec key blocklist (library-bug workarounds).** Until library issues are
fixed, some spec keys must not be passed for specific archetypes — even when the published design
point has a value for them. If the prior model contains any of these keys in `spec`, **remove
them** as part of this edit:
- **DIPOLE**: remove `plasma_volume` if present. The MFE radiation calc treats `plasma_volume`
  as a uniform integrator and over-counts radiation for dipole-peaked profiles. Library issue:
  **1cFE/1costingfe#24**. Document the removal with a brief comment citing the issue.

**Override values are M$, never raw dollars** (validator rejects `|value| > 5e4`).
**Derived rollup accounts cannot be overridden**: C220111, C220000, C220100,
C220200, C220300, C220400, C220500, C220600, C220700. To express "this concept
assembles more simply," override `installation_frac` via `costing_overrides`,
not the C220111 dollar amount.
**Disabled overrides must carry a `blocked_by` field** matching `<org>/<repo>#<NN>`
(e.g. `"1cFE/1costingfe#42"`) so library-side findings route to a tracker
instead of dying in the rationale text.
**Every override must declare `cost_basis: "noak"` (strict).** The framework runs
`noak=True`; any other vintage (`foak`, `conceptual_design`, `vendor_target`,
`unspecified`) is rejected. If your source publishes a non-NOAK value, either
(a) disable + `blocked_by`, (b) apply a documented learning-curve adjustment in
`rationale` and declare `cost_basis: "noak"`, or (c) file a tracker issue.

## Override semantics and the 1 GWe headline (read before editing any override)

This is the same policy the analysis agent authored Section 5b against — the single
headline invariant, the S/U/P cost classes, and the modular-fleet rationale
baseline. Any override you add or change must match it: the value anchored to the
account's own storage shape, and the rationale in the modular-fleet frame (never a
"conventional 1 GWe plant").

# Override semantics and the 1 GWe headline

## The invariant (this is the whole rule)

Every concept's headline is one number: LCOE for a **1 GWe NOAK plant**, reached
by **replicating** the real `P_native` design point into a fleet of `n_mod`
identical modules (`run_native_and_1gw(...)`, `noak=True`). There is no monolithic
1 GWe machine — we never extrapolate the physics model to a single 1000 MWe
reactor we have no design basis for.

At that headline, for **every account in every class**:

    account = M × (the library's 1 GWe fleet cost for that account)

`M` is the fraction of the library's fleet answer you believe this concept should
pay. `M = 1.0` means "trust the library default"; you only write an override when
evidence says this concept departs from it. That is the entire authoring rule.

The framework guarantees this invariant regardless of *which* `generic` value you
anchor to: `_scale_overrides` (in `1costingfe/src/costingfe/model.py`) rescales
your override from the native frame to the fleet frame by the per-account ratio
`fleet_cost / native_cost`, so the headline always lands on `M × fleet_cost`. You
do **not** compute that ratio yourself — you pick the right `generic` anchor for
the account's storage shape (below) and the framework does the rest.

## The cost classes — comprehension, not three rules

The classes below explain **why** the fleet cost is what it is (so you can sanity-
check `M`) and dictate the **authoring shape** — which `generic` value you anchor
to. They do **not** introduce per-class multipliers. If you delete the table, the
invariant above still tells you what an override means; the table only tells you
*where to anchor it* and *why the fleet cost looks the way it does*.

| Class | Why the fleet cost is what it is | Authoring shape (what to anchor to) | Accounts |
|---|---|---|---|
| **S — Shared / fixed** | A site needs these **once**, however many modules it runs — the library charges them once across the fleet. That single charge *is* the amortization that gives a small machine a fair shot. | whole-plant M$ → `M * generic.costs.<rollup>` | CAS10, CAS21, CAS28, CAS40, CAS70 |
| **U — Per-unit** | One per module: `N` modules → `N` cores. The library multiplies by `n_mod`; `noak=True` credits mass-production learning as the offset for losing single-core economy of scale. | per-module M$ → `M * generic.cas22_detail["C2201xx"]` | CAS22 reactor-island sub-accounts `C2201xx`; CAS80 fuel (taught, but not overridable today — see note) |
| **P — Power-proportional** | Scales with the **total** plant power, so the value is the same whether you replicate or not. | whole-plant M$ → `M * generic.costs.<rollup>` | CAS23, CAS24, CAS25, CAS26, CAS27; plant-wide CAS22 sub-accounts `C2202xx`–`C2207xx` |

**Storage-shape footnotes (which `generic` attribute exists):**
- Only the CAS22 reactor-island sub-accounts (`C2201xx`) live under
  `generic.cas22_detail["C220xxx"]`. Everything else — CAS21, CAS23–27, CAS70,
  CAS80, and the CAS22 rollup — is a top-level attribute on `generic.costs`.
- **Taught but NOT overridable today: CAS40 (owner's costs), CAS70 (O&M), and
  CAS80 (fuel).** Overrides on these are silently dropped — e.g. a CAS80 override,
  whether absolute (`0.050`) or relative (`M * generic.costs.cas80`), leaves the
  fleet value at the library default and does **not** move the headline
  (`1cFE/1costingfe#106`; the CAS70 / CAS80 no-op is pinned by
  `1costingfe/tests/test_override_scaling_semantics.py`). They are in the class
  table so you know *why* the library prices them as it does (and so a future
  override surface lands on prepared ground) — but do **not** author an override
  against them expecting an effect. Use only codes from the canonical account
  schema you are given.

**Reading the output — how to verify a Class-U override actually scaled:**
The `print_cas_breakdown` **CAS22 sub-account detail table shows per-module M$ at
every scale** — its `native` (n_mod=1) and `1 GWe` (n_mod=200) columns are
*supposed to be identical* for a `C2201xx` row, because the per-module cost does not
change; the ×`n_mod` fleet multiplication shows up in the **`C220000` / `CAS22`
rollup**, not in the detail row. So a Class-U detail row that reads the same at
native and 1 GWe is **expected, not a scaling failure.** To confirm a Class-U
override reached the fleet, check that the **`CAS22` (or `C220000`) rollup** moved
by roughly `Δ(per-module value) × n_mod` — never infer "it didn't scale" from the
detail row alone.

## The rationale baseline (one named frame, always)

Every relative override's `rationale` answers "why is `M` what it is?" against
**one** named baseline:

> **the library's default for a fleet of this device at 1 GWe.**

Never against "a conventional 1 GWe plant" / a monolithic 1000 MWe machine — under
the always-replicate decision that baseline does not exist. Anchor the rationale
to the same frame as the value. (Citing a monolithic plant from the literature as
a *comparable* — ARC, STEP — is fine; using one as the override's *anchor
baseline* is the inconsistency this policy removes.)

A multiplier above 1.0 is legitimate: it means "this concept's account costs more
than the library's modular-fleet default" (e.g. a harder-to-build module), still
in the fleet frame — not "more than a conventional plant."

## What wrong looks like

- **Value/rationale frame mismatch.** Value reads `0.70 * generic.cas22_detail["C220101"]`
  (70% of one module's blanket) while the rationale says "70% of a conventional
  1 GWe plant's blanket." The value is per-module fleet-frame; the rationale is
  monolithic. Rewrite the rationale in the modular-fleet frame.
- **Monolithic baseline in rationale.** Any "vs a conventional / standard 1 GWe
  plant," "vs a monolithic reactor," or bare "vs library default" with no fleet
  frame. Replace with "vs the library's 1 GWe modular-fleet default."
- **Class/anchor mismatch.** Overriding a CAS22 sub-account (Class U) but anchoring
  to a top-level rollup (e.g. `C220101` valued against `generic.costs.cas21`).
  Anchor each account to its own storage location: `C2201xx` →
  `generic.cas22_detail["C2201xx"]`; top-level rollups → `generic.costs.<rollup>`.


**Rules**:
- Preserve all existing sweeps, scenarios, and sensitivity analyses unless a
  finding specifically says to change them.
- Add content incrementally; every change must be traceable to a specific finding
  or a direct consequence of one.
- Any override you add or change uses a **canonical** account code (schema below)
  and the six-field shape; keep `provenance` honest and show derivation arithmetic
  in `rationale`.


## Assessment Findings

Focus on findings tagged `Category: model`. Findings tagged `Category: analysis`
are informational (the analysis agent handles prose), but you may adjust model
parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: CAS80 is the second-largest 1 GWe cost driver but is absent from the narrative
- **Target:** Section 7 (TEA Implications / Family-Delta) and model output interpretation note
- **Category:** analysis
- **Finding:** The model output shows CAS80 at $524M for the 1 GWe fleet — 22% of the $2404M overnight total and the second-largest category after CAS22 ($1273M). The library's D-He3 default prices He3 at commercial procurement rates, which directly contradicts Helion's self-breeding economic thesis (DD → tritium → He3 via 12.3-yr decay). The analysis correctly notes CAS80 is not overridable and flags the He3 startup inventory as a data gap, but never states that CAS80 is already inflating the 132 $/MWh LCOE by a substantial margin — or that the library default cannot represent Helion's self-bred fuel cost. A reader comparing Helion's 132 $/MWh to other concepts will not know that the number embeds an implicit He3 procurement cost that Helion's architecture is specifically designed to eliminate.
- **Recommendation:** Add an explicit note to Section 7 (or the model output interpretation block) stating: the 1 GWe LCOE of 132 $/MWh includes ~$524M in CAS80 priced at the library's D-He3 commercial-procurement default; since CAS80 is not overridable, this embedded cost cannot be adjusted to reflect Helion's self-breeding strategy, and the quoted LCOE is materially pessimistic on fuel relative to Helion's economic thesis. Estimate the LCOE sensitivity: if He3 self-breeding reduces fuel cost to near-zero (Helion's claim), CAS80 removal would reduce 1 GWe overnight cost by ~22% and LCOE by a comparable fraction.
- **Priority:** important

### F-2: Section 7 family-delta has no fixed comparables and the hypothetical deltas lack model grounding
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The frontmatter carries `Comparables: []`, so Section 7 correctly states "No comparable concept in the corpus." The section then provides account-level hypothetical deltas against D-T MIF concepts (MagLIF, MTF). These deltas are qualitatively sound and name specific accounts with cost directions, which satisfies the "not generic framing" criterion. However, the MagLIF analysis (concept 07) is at iter-2/PASS and its model output is available — the hypothetical figures cited in Section 7 ("~$200M penalty for D-T relative to Helion" for CAS23) are asserted without reference to MagLIF's actual modeled CAS23 value. This leaves the delta magnitudes unanchored.
- **Recommendation:** Pull MagLIF's actual modeled CAS23, C220101, and CAS26 values from its model output and use them as the reference numbers in the Section 7 delta table, with a note that MagLIF is used as the nearest available MIF neighbor even though it is not formally assigned as a comparable. If the upstream tables can assign MagLIF as a comparable, request that change; if not, document the informal reference explicitly so the delta is reproducible.
- **Priority:** important

### F-3: C220107 provenance flag appears resolved in current artifacts — verify the iteration-2 snapshot
- **Target:** Section 5b (Override Candidates), account C220107
- **Category:** analysis
- **Finding:** The coherence pipeline flagged a provenance mismatch for C220107 (model_setup=derived, analysis.md=direct). Reading the current analysis.md and model_setup.py, both carry `provenance: derived` for C220107 and both rationales explicitly state "provenance is derived." Since analysis.md is in a modified state (per git status), the mismatch was likely present in an earlier draft and has since been corrected. However, the coherence check was run against iteration-2 artifacts, and the current files' consistency has not been verified against the snapshot the check scanned.
- **Recommendation:** Confirm that the C220107 entry in the iteration-2 analysis snapshot (the artifact the coherence pipeline compared) matches the current `derived` label, and re-run the coherence check if the iteration snapshot differs from the working file. No change is needed if both artifacts at the same revision carry `derived`.
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/analysis.md`
- **Example (pattern):** `/home/reid/1cfe/1costingfe/examples/dhe3_pulsed_frc.py`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.PULSED_FRC`, `Fuel.DHE3`

### Canonical account schema (for any new/changed override)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220103` | Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | primary pulsed driver (laser/accelerator/gun) on $/J of driver energy; electrical-drive concepts cost it in C220107 |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | pulsed-power capacitor bank on $/J stored — usually the dominant driver cost for electrically-driven pulsed schemes |
| `C220109` | Direct energy converter (electrostatic for mirror/FRC exhaust, or inductive DEC on a pulsed driver) | only if the design point uses direct energy conversion (directed axial exhaust or an inductive DEC stage) |
| `C220110` | Remote handling & maintenance equipment (rad-hardening tier x vessel geometry) | always (for this archetype) |
| `C220111` | Reactor-equipment installation & assembly (fraction of the CAS22 subtotal) | always (for this archetype) |
| `CAS21` | Buildings & site structures (reactor, turbine, hot cell, balance-of-plant) | always (for this archetype) |
| `CAS23` | Turbine plant equipment (thermal cycle; zero for direct-conversion / eta_th=0 plants) | zero if the design point is direct-conversion (no thermal cycle) |
| `CAS24` | Electric plant equipment (switchyard, transformers, plant distribution) | always (for this archetype) |
| `CAS26` | Heat rejection system (cooling towers, circulating water) | always (for this archetype) |
| `CAS27` | Special materials — initial reactor material inventory / blanket fill (distinct from C220101 structure) | always (for this archetype) |
| `CAS70` | Annualized O&M + scheduled component replacement (staffing-based) | always (for this archetype) |
| `CAS80` | Annualized fuel cost — consumables and enriched-isotope procurement | always (for this archetype) |

### Canonical `spec` field glossary (for any new/changed spec key)

If your edit touches the `spec` dict (adding/renaming/replacing a field),
the new key MUST come from the glossary below. Read the "Common confusions"
block before editing — most prior errors (concept 05/09 fusion-vs-heating
mix-up, dipole `plasma_volume` regression, kJ-vs-MJ driver-energy mistakes)
trace back to ignoring these warnings.

{{canonical_spec_keys}}

## Output
Write changes to: `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/iter-3/model_setup.py`
