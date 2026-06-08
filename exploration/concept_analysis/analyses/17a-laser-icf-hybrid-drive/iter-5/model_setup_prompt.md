# 1costingfe Model Update: Laser ICF Hybrid Drive (Xcimer Energy)

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/iter-5/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/iter-5/model_setup.py` and apply
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

### F-1: HYLIFE-II BOP full report resolves thermal efficiency and energy cycle data gaps
- **Target:** Section 5 (thermal_efficiency row), Section 6 Data Gaps #5 and #6, Section 2 Challenge #4 footnote [^10]
- **Category:** analysis
- **Finding:** `osti-servlets-purl-6137961.md` is the full text of the HYLIFE-II Power Conversion System Design and Cost Study (Hoffman, UCRL-CR-105908, 1990) — not an empty stub as Section 1 characterizes it. The report provides: thermal efficiency of 41.2% (low-viscosity FLiBe case, steam cycle at 800 K / 16 MPa), BOP architecture confirming FLiBe primary coolant → NaBF₄ secondary loop → steam generators (not He Brayton), and total FLiBe inventory of ~960 m³ for a single HYLIFE-II chamber. Section 2 Challenge #4 calls the energy conversion pathway "ambiguous (steam vs. He Brayton vs. combined cycle)"; Section 5 rates thermal_efficiency "~40–45%, low confidence"; Data Gaps #5 and #6 list the cycle and thermal efficiency as "important" unknowns. All three are now partially resolvable from heritage data that was previously in the repo but marked unavailable.
- **Recommendation:** Update the Section 5 thermal_efficiency row to "~41% (HYLIFE-II heritage: steam cycle via NaBF₄ intermediate at 800 K / 16 MPa; medium confidence pending Xcimer confirmation of cycle choice)." Update footnote [^10] and Section 2 Challenge #4 to note that the HYLIFE-II heritage design used a steam cycle (FLiBe → NaBF₄ → steam at 41.2% efficiency), and Xcimer's marketing references to "steam turbines" are consistent with this heritage. Revise Data Gaps #5 and #6 from "not-yet-sourced" to "partially resolved: HYLIFE-II heritage points to ~41% steam cycle; Athena-specific confirmation still needed." Cite `osti-servlets-purl-6137961.md` as the primary HYLIFE-II BOP source rather than the stub `hylife-energy-conversion-notes.md`.
- **Priority:** important

### F-2: CAS27 FLiBe mass reference is wrong by ~3× — override value underestimated
- **Target:** `model_setup.py` overrides list (CAS27 value and rationale)
- **Category:** model
- **Finding:** The CAS27 override rationale states "HYLIFE-II reference used ~600 t of FLiBe for a 6 Hz, 350 MJ-yield chamber" and derives $92M (600 t × $154/kg). The actual HYLIFE-II Power Conversion report (`osti-servlets-purl-6137961.md`, Case D single-chamber) gives total FLiBe inventory ~960 m³. At FLiBe operating density ~2,020 kg/m³, this is approximately 1,940 tonnes — roughly 3× the stated reference. Applying the same $154/kg unit cost yields ~$299M, not $92M. The analysis already acknowledges "could range 300–1,000 t" and "high uncertainty," but the reference point grounding that range is materially wrong, pulling the central estimate well below even the analysis's own lower bound.
- **Recommendation:** Update the CAS27 override rationale to cite the corrected HYLIFE-II FLiBe inventory (~960 m³ ≈ 1,940 t, Case D, `osti-servlets-purl-6137961.md`). Note that Athena's average thermal power (~1,100 MWth) is approximately one-third of HYLIFE-II's (~3,260 MWth), suggesting a proportionally smaller FLiBe circuit, but the per-shot yield is ~4.6× higher (~1.6 GJ vs 350 MJ), which may require a larger protective jet volume. A revised central estimate of ~600–1,000 t (not anchored to "~600 t as HYLIFE-II used") and a corresponding value of ~$92M–$154M is more defensible. Update the model_setup.py CAS27 value from 92.0 to a revised figure with an explicit note that the heritage reference is ~1,940 t and the Athena-specific mass remains unknown.
- **Priority:** important

### F-3: Hawker (2020) IFE LCOE model provides competitive benchmarks and Xcimer gain-threshold context
- **Target:** Section 7 (TEA implications, Delta 2 gain risk), Section 6 (Data Gap Inventory context)
- **Category:** analysis
- **Finding:** `pmc-articles-pmc7658748.md` contains Hawker (2020), a parametric IFE LCOE sensitivity study not referenced in the analysis. It establishes: (1) competitive LCOE benchmarks absent from the analysis ($50/MWh for renewables parity, $100/MWh for nuclear parity; historical HYLIFE-II baseline of 6.5 cents/kWh in 1988 dollars ≈ $120–130/MWh 2025-adjusted — marginal at best against nuclear); (2) a gain competitiveness threshold of ~400 under baseline cost assumptions, with viable designs possible at ~250 only under favorable plant cost and financing assumptions; (3) a Pearson sensitivity ranking showing that discount rate (+0.247) and plant cost / BOP (+0.210) dominate LCOE variance, while driver cost is the weakest cost lever (+0.075, 7th of 14 parameters). Xcimer's NOAK target gain of ~250 falls below the baseline threshold of ~400 but satisfies the ηwp × G > 10 viability criterion (7% × 250 = 17.5). The analysis's Section 7 Delta 1 calls the laser cost reduction "the single largest cost delta," which is accurate at the capital account level but overstates its influence on final LCOE relative to BOP costs and financing.
- **Recommendation:** Add to Section 7's Delta 2 TEA consequence paragraph: note that Xcimer's NOAK Qsci target (~250) is below the Hawker (2020) model's gain threshold for competitive LCOE under baseline BOP and financing assumptions (~400), and that achieving the $50–100/MWh competitive range requires simultaneously favorable plant cost, discount rate, and target cost parameters — not gain alone. Add competitive benchmarks ($50/MWh, $100/MWh) as reference points to Section 1 or Section 7 summary table. In Section 7 Delta 1, add a qualifying sentence noting that while the ~10× driver cost reduction is the dominant capital account delta, independent IFE sensitivity analysis (Hawker 2020) finds driver cost has weaker LCOE leverage than BOP cost and financing cost, so the laser advantage is necessary but not sufficient for competitive LCOE.
- **Priority:** important


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/analysis.md`
- **Example (pattern):** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.LASER_IFE`, `Fuel.DT`

### Canonical account schema (for any new/changed override)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | primary pulsed driver (laser/accelerator/gun) on $/J of driver energy; electrical-drive concepts cost it in C220107 |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | pulsed-power capacitor bank on $/J stored — usually the dominant driver cost for electrically-driven pulsed schemes |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | high-rep-rate target manufacturing factory (IFE/MIF) |
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
Write changes to: `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/iter-5/model_setup.py`
