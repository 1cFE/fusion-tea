---
Status: draft
Created: 2026-09-03
Updated: '2026-09-03'
Related Artifacts:
  Spec: ./spec.md
---

# WI-039 Design — the heating power chain

Designed under goal `wall-and-heating`, round 1, task T-002. The spec's four open decisions are settled here, each with its reasoning and its cost stated, because the round review and the fresh grader both read this file.

## Overview

Today the model holds three constants — installed plasma-coupled power (50 MW), a lumped wall-plug efficiency (0.5), and installed ECRH power for costing (50 MW) — and does one inline division inside another subsystem's sum. This design replaces them with a **forward chain from installed wall-plug electrical power to plasma-coupled power**, with the two efficiency stages the pinned source actually publishes as separate named quantities, and routes the chain's outputs to the two places that consume heating power: the power balance (coupled power into `p_th`, wall-plug into `recirculating`) and the CAS22.1.4 cost account (source-output power).

The arithmetic at the baseline is unchanged. 100 MW wall-plug x 0.50 source efficiency = 50 MW out of the gyrotrons, x 1.00 coupling = 50 MW coupled. Every downstream number holds; what changes is that these are now derived, and they move when an efficiency moves.

## Research findings

**The pinned source publishes exactly two stages, and no third.** `defaults.py:102-108` (1costingFE `0254385`): "Heating wall-plug source efficiency by method (wall-plug → delivered power, before plasma coupling). Combined with a per-concept `eta_couple` (in the concept YAML) to form `eta_pin = eta_source x eta_couple`." `eta_source_ecrh = 0.50` carries a "gyrotron wall-plug" basis and the per-MW rate beside it is calibrated to ITER gyrotron procurement (`defaults.py:92-99`). `eta_couple = 1.0` for this concept (`steady_state_stellarator.yaml:15`, comment "ECRH coupling; eta_pin = 0.50 x 1.0 = 0.50").

**There is no transmission efficiency anywhere in the pinned source.** A three-stage chain — source, transmission line, coupling — is the physically complete picture and it is what the item's minted title gestures at, but the third stage would carry a number no admissible source publishes. Under MR-WI039-2 and the goal's standing "surfaced with options, never defaulted", the chain is **two-stage**. The anchor names a chain, not a stage count.

**The cost rate's basis is source *output* power, not wall-plug.** The ECRH rate is $/MW calibrated to gyrotron procurement (`cas22.py:446-459`, C220104), and the model's `p_ecrh = 50.0` is documented as "delivered ECRH power". So the cost account must consume the chain's **post-source, pre-coupling** power — the 50 MW out of the gyrotrons — not the 100 MW at the wall plug. Getting this wrong would silently double the heating account.

**The WI-024 cryoplant chain is the precedent to copy, and it is already blessed in this repository.** `mfe_cryo_plant.sysml` defines a chain calc with dormant-safe defaults; `mfe_plant.sysml:369-395` declares the chain's inputs beside an additive **direct term** (`p_cryo`), so that a concept knowing its answer outright binds the direct term and leaves the chain dormant, while a concept deriving it binds the chain and zeroes the direct term (`stellarator_plant.sysml:724`). Same shape, same file layout, same dormancy rule. Following it costs nothing and makes this increment legible to anyone who has read WI-024.

**The oracle mirrors the model.** `verify_stellaris.py:391-392` computes `recirculating` with `p["p_input"] / p["eta_pin"]` — the model's own expression. Parity against that verifies nothing (MR-WI039-5).

## Design decisions

### D1 — Wall-plug is the entry point; coupled power is computed. `[AGENT]`

**The decision.** `p_wallplug_heat` becomes the settable installed quantity. Plasma-coupled power and source-output power are both computed from it.

**The alternative, and why it loses.** The obvious cheaper design keeps the sourced 50 MW coupled power as the entry point and computes wall-plug forward from it — a backward solve. It satisfies the anchor's letter, costs almost nothing, and retires no entry point. It loses on the grader's actual objection. G1's resolution reads: *"a held ratio dividing one held constant inside another subsystem's sum derives nothing."* A backward solve is that same division with names attached: coupled power held, both efficiencies held, wall-plug derived. A fresh grader could read it as a relabel and score R4.P = 1 again, and this round would have spent its increment for nothing.

With wall-plug forward, the quantities that **govern** — the coupled power that enters `p_th`, and the coupled power that `sustainment_ok` compares against the plasma's requirement (`stellarator_plant.sysml:1122`) — become derived. Change the gyrotron efficiency and the plasma's heating changes. That is a chain that derives something, and it cannot be read as a relabel.

**What it costs, stated plainly.** Three entry points retire (`p_input`, `p_ecrh`, `eta_pin`) and one is minted (`p_wallplug_heat`). Two committed studies swept the `p_input`/`p_ecrh` tie, so MR-WI039-9's restatement duty fires. The restatement is meaning-preserving and exactly derivable: a sweep of coupled power over 50–110 MW is the same experiment as a sweep of wall-plug power over 100–220 MW, at `eta_pin_eff = 0.50`. The last two entry-point retirements cost roughly 30 fixture sites each; this one is budgeted the same.

**A side effect worth having.** The `p_input`/`p_ecrh` tie is declared in `manifest.json` — a study-layer declaration that keeps two model constants moving together because the model does not know they are the same physical quantity. That is a workaround maintaining an invariant the model should declare itself. After this change the tie is **structural**: both powers descend from one wall-plug input, and no declaration is needed to keep them consistent. The workaround is removed rather than formalised.

**Fidelity note, surfaced not buried.** The source prints the *coupled* 50 MW; the wall-plug 100 MW is that value divided by the model's own stated chain efficiencies. It is an exact algebraic restatement of a sourced number under stated assumptions, not a new number, and its doc comment says so. The consequence is real and is the point: if a future study sweeps `eta_source`, coupled power moves off the printed 50 MW. That is the chain working. It is recorded here so that nobody later reads a moved coupled power as a lost source anchor.

### D2 — The chain is two-stage, and the coupling stage is a stated assumption. `[AGENT]`

`eta_source_heat = 0.50` is sourced (gyrotron wall-plug, ITER procurement basis). `eta_couple_heat = 1.00` is **not a source** — it is the pinned model's per-concept default. Under MR-WI039-3 it is carried as an explicitly stated assumption, in the model text, saying what it asserts and what it costs:

> All power leaving the gyrotrons is assumed to reach the plasma: no transmission-line loss, no window loss, no shine-through, no unabsorbed first pass. This is the pinned 1costingFE per-concept value for ECRH and it is an idealisation, not a measurement. It is optimistic in the direction of understating both wall-plug power and recirculating power. A real ECRH chain's transmission and single-pass absorption losses would lower it; the model carries no admissible source for either, so the loss is named here rather than guessed at. If a coupling figure is later sourced, it enters at this one attribute and the chain re-derives.

That paragraph is the "stated deposition assumption" the P2 anchor asks for. Stating it is not optional decoration — a default nobody wrote down is precisely what the anchor excludes.

### D3 — The chain lives in its own library file, wired at the generic plant. `[AGENT]`

`models/library/analyses/mfe_heating_chain.sysml`, a new file holding one concept-agnostic `calc def 'Heating Power Chain'`. This mirrors `mfe_cryo_plant.sysml` (AD-004: library subdirectory organisation; MR-3: library concept-agnostic). The `'Heating and CD'` part def gains nothing — the cryo precedent puts the chain in the analysis layer, not on the costed component, and splitting the pattern for one item would make both harder to read.

### D4 — Dormancy is preserved by additive direct terms, the WI-024 way. `[AGENT]`

The chain carries two additive direct terms so that a concept which knows its heating powers outright can bind them and leave the chain dormant, exactly as a concept can today bind `p_cryo` and leave the cryo chain dormant. With all chain inputs at their defaults and the direct terms bound, the chain reproduces today's semantics exactly. This keeps the library honestly concept-agnostic rather than shaped around the one concept in front of us.

## Proposed design

### New: `calc def 'Heating Power Chain'` — `models/library/analyses/mfe_heating_chain.sysml`

| quantity | kind | units | meaning |
|---|---|---|---|
| `p_wallplug` | in, default 0.0 | MW | installed wall-plug electrical power drawn by the heating system |
| `eta_source` | in, default 1.0 | 1 | wall-plug → source output (gyrotron/klystron/injector conversion) |
| `eta_couple` | in, default 1.0 | 1 | source output → power coupled into the plasma (the deposition assumption) |
| `p_delivered_direct` | in, default 0.0 | MW | directly-specified source-output power, for a dormant-chain concept |
| `p_coupled_direct` | in, default 0.0 | MW | directly-specified plasma-coupled power, for a dormant-chain concept |
| `eta_pin_eff` | out | 1 | `eta_source * eta_couple` — the lumped efficiency, retained as a derived quantity |
| `p_delivered` | out | MW | `p_wallplug * eta_source + p_delivered_direct` — the cost driver |
| `p_coupled` | out | MW | `p_wallplug * eta_source * eta_couple + p_coupled_direct` — into the plasma |
| `p_wallplug_total` | out | MW | `p_wallplug + p_coupled_direct / eta_pin_eff` — into the recirculating sum |

`p_wallplug_total`'s second term is what keeps a dormant concept's recirculating power identical to today's `p_input / eta_pin`. With the chain live and `p_coupled_direct = 0` it is just `p_wallplug`. `eta_pin_eff` defaults to 1.0 x 1.0, so a fully dormant chain never divides by zero — the WI-024 `f_carnot` dormant-safety rule, applied to the same problem.

All arithmetic sits **inside** the calc def, none in an input binding: the pinned codegen refuses an expression in a calc input binding (`SI_EXPRESSION_SOURCE_UNSUPPORTED`).

### Changed: `models/library/analyses/mfe_power_balance.sysml`

- `in attribute eta_pin_in` is **removed**; `in attribute p_wallplug_in : Real default 0.0;` replaces it.
- `recirculating` drops `+ p_input_in / eta_pin_in` and takes `+ p_wallplug_in` (MR-WI039-4 — the objection is about *this line*, so this line has to change).
- `p_input_in` stays and keeps its meaning (plasma-coupled power into `p_th`); it is now fed by the chain rather than by a held constant.

### Changed: `models/designs/generic_mfe/mfe_plant.sysml`

- New attributes beside the cryo block, same shape: `p_wallplug_heat` (default 0.0), `eta_source_heat` (1.0), `eta_couple_heat` (1.0), `p_delivered_direct_heat` (0.0), `p_coupled_direct_heat` (0.0).
- `attribute p_input` and `attribute eta_pin` are **retired**; `attribute p_ecrh` is retired into `p_delivered_direct_heat`.
- `calc heat : 'Heating Power Chain'` wired from those attributes.
- `calc pb`: `in p_input_in = heat.p_coupled;` and `in p_wallplug_in = heat.p_wallplug_total;`.
- Heating cost: `in p_ecrh_in = heat.p_delivered;`.

The ECRH slot is the chain's consumer because this generic plant already carries ECRH-specific slots and this concept is ECRH-only with no current drive (sourced, `stellarator_plant.sysml:821-837`). A multi-method concept binds its other per-method powers exactly as today; nothing about them changes.

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml`

`:>> p_wallplug_heat = 100.0` (with the D1 derivation in its doc comment: Table 2's printed 50 MW plasma-coupled ECRH power, divided by the chain's stated `eta_source x eta_couple = 0.50`); `:>> eta_source_heat = 0.50` (sourced); `:>> eta_couple_heat = 1.00` (carrying D2's stated assumption verbatim); direct terms zeroed with the reason. `p_input`, `eta_pin`, `p_ecrh` bindings are removed.

### Changed: `exploration/stellarator_e2e/verify_stellaris.py`

The oracle computes the chain **itself** from `p_wallplug_heat`, `eta_source_heat`, `eta_couple_heat` — its own three lines of arithmetic, written from this design's table and not transcribed from the generated package — and uses its own `p_wallplug_total` in its recirculating sum. The existing `p["p_input"] / p["eta_pin"]` term goes. Without this the parity check is a tautology (MR-WI039-5).

## Cross-file bindings

| consumer | input | source |
|---|---|---|
| `pb` (power balance) | `p_input_in` | `heat.p_coupled` |
| `pb` | `p_wallplug_in` | `heat.p_wallplug_total` |
| heating cost | `p_ecrh_in` | `heat.p_delivered` |
| `heat` | `p_wallplug`, `eta_source`, `eta_couple`, direct terms | plant attributes, bound per concept |
| `sustainment_ok` | `p_aux_installed_in` | `heat.p_coupled` (was `p_input`) |

Dataflow stays unidirectional: concept attributes → chain → power balance and cost. No new cross-file coupling beyond the one new library import.

## Expected baseline behaviour

| quantity | today | after | why |
|---|---|---|---|
| coupled heating power | 50.0 (held) | 50.0 (computed) | 100 x 0.50 x 1.00 |
| source-output power for cost | 50.0 (held) | 50.0 (computed) | 100 x 0.50 |
| `heating_cost__cost` | $264.145M | $264.145M | 5282900 x 50, unchanged |
| wall-plug into `recirculating` | 100.0 (inline division) | 100.0 (chain output) | same number, different provenance |
| `q_eng`, `rec_frac`, LCOE, all nine verdicts | — | unchanged | no term in any sum changed value |

**If any of these moves, it is a finding to disclose and derive, not a number to fit** (`goal.md` § Invariants). A moved value means the design's arithmetic differs from the model's, and the honest response is to find out why.

## Validation plan

1. Parse and Levels 1–3 on the new library file and the two changed files.
2. Codegen through the pinned generator; confirm no `SI_EXPRESSION_SOURCE_UNSUPPORTED`.
3. Execute at the baseline; compare every quantity in the table above against the pinned `baseline_result.json`.
4. Independence check on the oracle: the chain is written from this design, and its agreement with the model is then evidence.
5. Perturbation check for the anchor: change `eta_source_heat` alone and confirm coupled power, cost, and recirculating power all move — the grader's stated `why_not_next` test ("re-derives when efficiencies or delivered power change independently").
6. `tests/models` and `tests/study` green; every changed study expectation re-derived from live evidence per MR-WI039-9.

SV rows are created at implementation, once the chain's element names are fixed.

## Risks

1. **A fresh grader reads the chain as a relabel anyway.** *Mitigation:* D1 — the governing quantities are derived, not the derived quantity governed. The perturbation check in the validation plan is the evidence.
2. **`eta_couple = 1.0` judged insufficient as a "stated" assumption.** *Mitigation:* D2 states it in full, including its direction of optimism. If it is still judged insufficient, that is a sourced-coupling-figure research question for a later round, surfaced rather than defaulted.
3. **The study restatement is larger than budgeted.** *Likelihood: medium.* Two committed studies, roughly 30 fixture sites at the last comparable retirement. *Mitigation:* the mapping is exact (`p_wallplug = p_input / 0.50`), so every restated expectation is derivable rather than guessable — but each one is re-derived from live evidence, never patched to match.
4. **A baseline value moves.** *Mitigation:* disclose and derive; never fit.

## Prototype and validation report

**Prototype: PASS.** `models/library/analyses/mfe_heating_chain.sysml` written as designed and validated with `uv run agentic-mbse validate models`.

- **Level 1 (syntax): 0 errors, 0 warnings** across all 25 SysML files. The calc def parses, the doc comment and the nine quantities are well-formed, and the `out attribute` chain resolves.
- **Level 2 (structural): one new warning, and it is the expected one** — `Unused calc def: mfe_heating_chain::'Heating Power Chain'`. Nothing consumes it yet; that is what implementation does. The other 12 issues (placeholder literal bindings in `mfe_plant.sysml`) are pre-existing and untouched by this file.
- Levels 3–6 were not reached because the run stops at Level 2's first failure. They are implementation gates, not design gates.

**What the prototype confirms.** The arithmetic sits inside the calc def with no expression in any input binding, so the pinned codegen's `SI_EXPRESSION_SOURCE_UNSUPPORTED` refusal is avoided by construction. The dormant-safe defaults (`eta_source`, `eta_couple` at 1.0) keep `eta_pin_eff` defined and `p_wallplug_total`'s division safe with the chain unbound.

**What it does not confirm**, and what implementation must therefore check: codegen actually generating the chain, the baseline numbers in the expected-behaviour table, the perturbation test, and the oracle's independent agreement.

**Files created:** `models/library/analyses/mfe_heating_chain.sysml`. **Files modified:** none yet — the wiring is implementation.

## Approval

Settled by the round agent under goal `wall-and-heating`, which reserved no gates and delegated execution decisions `[OWNER 2026-09-03, ruling 5]`. D1 is the load-bearing judgment and carries a real cost (three entry points retired, two committed studies restated); its reasoning and its rejected alternative are written above so the round review and the fresh grader can challenge it by re-derivation rather than by argument.
