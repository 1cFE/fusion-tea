# 1costingfe Model Update: Negative-Triangularity Tokamak

## Mode: Feedback Pass (Edit Existing Model)

An existing three-forward model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-3/model_setup.py` and apply
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

### F-1: Vertical stability degradation — an NT-specific risk absent from the analysis
- **Target:** Section 2 (Challenges) and Section 7 (Family-Delta vs comparables)
- **Category:** analysis
- **Finding:** Two new sources (arxiv-2401-15217, Guizzo et al. 2024, "Assessment of vertical stability for negative triangularity pilot plants"; arxiv-2501-14682, Guizzo et al. 2025, "Electromagnetic System Conceptual Design for a Negative Triangularity Tokamak") establish that NT configurations are measurably *less* vertically stable than PT at the same elongation, and that this degradation worsens at higher poloidal beta — opposite to PT behavior. At MANTA-relevant elongations (κ ≈ 1.8) the vertical instability growth rate without mitigation is substantially elevated; passive conducting plates (optimally placed outboard) reduce growth rates to ~16–25% of baseline. The analysis discusses ELM-free operation and edge stability as NT advantages in detail but never mentions vertical stability as a design challenge. This is a real, NT-specific engineering cost: passive stabilizer plates must be incorporated into the vacuum vessel and divertor assembly, adding fabrication complexity and a VV integration constraint not present in PT designs. The family-delta summary (Section 7) lists six NT deltas; vertical stability penalty is absent from all of them.
- **Recommendation:** Add a new numbered challenge to Section 2 titled "Vertical Position Control and Passive Stabilizer Plates" describing (a) that NT configurations are less vertically stable than PT at the same elongation, (b) that passive conducting plates are required and are confirmed effective (growth rate reduction to ~16–25% of baseline), and (c) that this adds fabrication cost and integration complexity to the VV design. Add a corresponding row to the Section 7 delta summary table: "Vertical stability (worse than PT at κ = 1.8)" → Direction: Penalty → Magnitude: Small (passive plates required; cost increment modest relative to $3.4B overnight) → Confidence: Medium. Cite arxiv-2401-15217 and arxiv-2501-14682.
- **Priority:** important

### F-2: Ohmic-only heating is field-strength-conditional, not generically uncertain
- **Target:** Section 2 (Challenge 5: Ohmic-Only Operation Feasibility) and Section 7 (Family-Delta: Auxiliary Heating Uncertainty)
- **Category:** analysis
- **Finding:** The existing analysis frames ohmic-only operation as a binary unknown ("validated or not"), treating it as symmetrically uncertain. The Ball et al. paper contains a result the analysis does not capture: ohmic-only NT performance is machine-dependent and field-strength-conditional. Specifically, the paper shows that at ITER parameters (B = 5.3 T), ohmically-heated NT *cannot* match PT H-mode performance — the Ohmic drive is insufficient at low field. At SPARC parameters (B = 12.2 T), ohmically-heated NT achieves Q ≈ 80 versus Q ≈ 12 for PT H-mode. MANTA at B = 11 T sits near the lower edge of the regime where ohmic-only becomes viable. This is not a symmetric uncertainty — it is a regime boundary. The risk framing should reflect this: the question is not "will ohmic-only work?" in the abstract, but "is MANTA's 11 T field above the viability threshold, and how sensitive is the threshold to NT confinement scaling assumptions?" The current text says the community "has not yet converged on ohmic-only as a baseline strategy," which understates the conditional nature of the result.
- **Recommendation:** Revise Challenge 5 (Ohmic-Only Operation Feasibility) to state that Ball et al. demonstrate a field-strength threshold: ohmic-only fails at ITER-level fields (~5 T) and succeeds at SPARC-level fields (~12 T), with MANTA at 11 T near the low end of the viable regime. Frame the risk as: "the uncertainty is not whether ohmic-only works in principle, but whether MANTA's parameters are comfortably above the threshold given confinement scaling uncertainty." Similarly revise the corresponding delta in Section 7 to note that the advantage accrues only if MANTA's 11 T field is above the ohmic-viability boundary — a condition that itself depends on the same NT confinement scaling (H_NA = 2.0) that is the analysis's primary uncertainty.
- **Priority:** important

### F-3: Maintenance scheduling economics add a quantitative TEA input for capacity factor
- **Target:** Section 2 (Challenge 6: Capacity Factor and Remote Maintenance) and Section 5 (Design Point Parameters — Availability row)
- **Category:** analysis
- **Finding:** arxiv-2405-01514 (Schwartz et al., "Valuing maintenance strategies for fusion plants as part of a future electricity grid") is a new source not cited in the analysis. It reports that on a 2050-era decarbonized US grid, a fusion plant that optimizes its maintenance window to spring–early summer can achieve plant value up to 15% higher than naive availability calculations suggest, and that fractional component replacement over multiple shorter maintenance blocks can outperform a single long annual outage even at lower total availability. MANTA's analysis uses 79% effective availability and notes PF2 replacement every ~2 full-power years as the limiting maintenance cycle. The Schwartz et al. result is directly applicable: MANTA's demountable TF coil design and modular FLiBe blanket enable fractional maintenance strategies, and the 2-month PF replacement window falls in a duration range where seasonal scheduling matters. The current analysis does not reflect that the *economic value* of availability is non-linear with timing, which is a TEA input distinct from the raw availability fraction.
- **Recommendation:** Add a note to Challenge 6 (Capacity Factor and Remote Maintenance) that Schwartz et al. (2025) find seasonal maintenance scheduling can recover up to 15% of plant economic value relative to naive availability assumptions, and that MANTA's modular demountable architecture is compatible with fractional-replacement strategies that amplify this benefit. Flag this as a positive TEA input that partially offsets the availability downside risk, and note it as a sensitivity parameter (maintenance scheduling strategy) for the TEA rather than a fixed cost driver.
- **Priority:** minor


## Reference

- **Concept Analysis (Design Point + Section 5b overrides):** `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/analysis.md`
- **Example (pattern):** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`
- **Concept mapping:** `ConfinementConcept.TOKAMAK`, `Fuel.DT`

### Canonical account schema (for any new/changed override)

| Account | What it costs | Applies when |
| --- | --- | --- |
| `C220101` | First wall, blanket & neutron multiplier (DT: tritium-breeding blanket; DD/aneutronic: energy-capture blanket) | always (for this archetype) |
| `C220102` | Radiation shield (sized to neutron wall loading; scales down for low-neutron fuels) | always (for this archetype) |
| `C220103` | Confinement magnets / coils (HTS-REBCO conductor + winding + cryostat) | always (for this archetype) |
| `C220104` | Supplementary plasma heating (steady-state) or primary pulsed driver (laser/accelerator/gun) | supplementary heating (NBI/ICRF/ECRH/LHCD) per installed MW |
| `C220105` | Primary structure — gravity supports, thermal shields, inter-coil structure, machine base | always (for this archetype) |
| `C220106` | Vacuum system — vessel, port extensions, cryopumps, leak detection | always (for this archetype) |
| `C220107` | Power supplies (steady-state magnet supplies / switchgear) or pulsed-power capacitor bank ($/J stored) | DC magnet power supplies and switchgear |
| `C220108` | Divertor (steady-state, W monoblock cassettes) or target factory (IFE/MIF target manufacturing) | divertor (W monoblock cassettes on CuCrZr heat sinks) |
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
Write changes to: `/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/29-negative-triangularity-tokamak/iter-3/model_setup.py`
