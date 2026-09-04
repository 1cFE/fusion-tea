---
Status: draft
Created: 2026-09-03
Updated: '2026-09-03'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-039 Plan — building the heating power chain

## Source documents

Design (primary): `./design.md`. Spec: `./spec.md`. Epic: `work/backlog/epic-mfe-cost-modeling.md`. Governing goal task: `work/orchestration/goals/wall-and-heating/trail.md` § T-002 scope.

## Design summary

A two-stage forward chain — installed wall-plug electrical power → source output → plasma-coupled power — replaces three held constants and one inline division. Wall-plug is the entry point (design D1); the coupling stage is a stated assumption, not a source (D2); the chain lives in its own library file (D3) and preserves dormancy with additive direct terms (D4). Rationale, the rejected backward-solve alternative, and the source basis are in the design; they are not repeated here.

## Prototype baseline

`models/library/analyses/mfe_heating_chain.sysml` **exists and passes Level 1 with 0 errors and 0 warnings** across all 25 SysML files (design § Prototype and validation report). One Level-2 warning stands — `Unused calc def: 'Heating Power Chain'` — which is by construction: nothing consumes it until Phase 2. The 12 other Level-2 issues are pre-existing placeholder literal bindings in `mfe_plant.sysml` and are not this item's.

Levels 3–6 were never reached (the runner stops at Level 2's first failure). They are gates for Phases 2 and 5.

**Refinements the prototype still needs:** none to its syntax. Its doc comment already carries the `Source`/`Ref`/`Basis` triple. What it lacks is consumers.

## Phasing approach

Library before instances, and the expensive irreversible step last. Five phases:

1. **Library** — finish the chain and change the power balance's interface. Both are library-side and neither can be checked without the other, because removing `eta_pin_in` from the power balance is what forces the chain to supply wall-plug power.
2. **Plant wiring** — the generic plant grows the chain and retires three attributes. This is where codegen either accepts the design or refuses it, so it comes before anything that depends on generated code.
3. **Concept instance and baseline parity** — bind the stellarator's values and prove every number in the design's expected-behaviour table. Nothing downstream is worth doing until the baseline is proven identical.
4. **Independent verification and the anchor test** — the oracle's own chain, plus the perturbation check that is the grader's stated test.
5. **Restatement, regression, and traceability** — the committed studies, the handshake fixtures, the test battery, SV rows.

**Why phase 3 sits before phase 4.** If the baseline moves, the design is wrong and phase 4's work would be thrown away. Prove the arithmetic first.

**Why the restatement is last and not first.** It is mechanical once the entry points are final, and doing it before the entry-point names settle would mean doing it twice.

## Validation strategy

Levels 1–3 after every phase, so errors never accumulate. Full Levels 1–6 plus both test batteries in Phase 5. Environment, from memory and confirmed at handoff:

```bash
set -a; source ~/1cfe/agentic-mbse/.env; set +a
uv run agentic-mbse validate models
rm -rf .integration_workspace
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python -m pytest tests/study -q   # ~7.5 min
```

`tests/study` leaves `.integration_workspace` behind; remove it before each run.

---

## Phase 1 — Library: the chain and the power-balance interface

**Overview.** Finish the chain definition and change what the power balance asks for. These land together because the power balance's `recirculating` term cannot lose `p_input_in / eta_pin_in` until something supplies wall-plug power.

**Design reference.** § Proposed design → "New: `calc def 'Heating Power Chain'`" (the nine-quantity table) and "Changed: `models/library/analyses/mfe_power_balance.sysml`". Key decisions: two stages only, because the pinned source publishes two (D2); all arithmetic inside the calc def, because the pinned codegen refuses an expression in a calc input binding.

**Prototype baseline.** `mfe_heating_chain.sysml` is written and parses. It needs no refinement — only review against the design table before its consumers exist.

**Files.**
- `models/library/analyses/mfe_heating_chain.sysml` — REFINE (review only)
- `models/library/analyses/mfe_power_balance.sysml` — REFINE

**Checklist.**
- [ ] Re-read `mfe_heating_chain.sysml` against the design's nine-quantity table; confirm names, defaults, units, and the four output expressions match exactly
- [ ] Confirm the doc comment's `Source`/`Ref`/`Basis` triple resolves (`defaults.py:102-108`, `cas22.py:446-459`, `physics.py:321-323`)
- [ ] `mfe_power_balance.sysml`: remove `in attribute eta_pin_in` (`:62`)
- [ ] `mfe_power_balance.sysml`: add `in attribute p_wallplug_in : Real default 0.0;` with a unit comment
- [ ] `mfe_power_balance.sysml`: change `recirculating` (`:134-136`) — drop `+ p_input_in / eta_pin_in`, add `+ p_wallplug_in`
- [ ] Update the `recirculating` doc/source comment to say the wall-plug heating term now arrives computed from the chain, and keep the `physics.py:321-323` citation
- [ ] Check the header doc comment at `:23-33` for statements about `p_input`/`eta_pin` that are no longer true; correct them **by amendment of the wrong sentence**, not by adding a new paragraph beside it
- [ ] `uv run agentic-mbse validate models` — Level 1 clean

**Test requirements.** None new yet; `tests/models/test_power_balance.py` will fail on the changed interface and is repaired in Phase 5, deliberately — a test patched before the interface settles is a test patched twice.

**Validation checkpoint.** Level 1: 0 errors. Level 2: no *new* warnings beyond the pre-existing 12 and the still-unused calc def.

**Gate.** The chain's four outputs and the power balance's new input are named exactly as the design's binding table says. A rename here costs three files later.

---

## Phase 2 — Plant wiring and codegen

**Overview.** The generic plant grows the chain, retires three attributes, and re-routes three consumers. This is the phase where the pinned codegen accepts the design or refuses it.

**Design reference.** § Proposed design → "Changed: `models/designs/generic_mfe/mfe_plant.sysml`"; § Cross-file bindings (the five-row table). Key decision: the ECRH cost slot consumes the chain's `p_delivered` because the per-MW rate is calibrated to source-output power, not wall-plug (design § Research findings) — getting this backwards silently doubles the heating account.

**Files.** `models/designs/generic_mfe/mfe_plant.sysml` — REFINE.

**Checklist.**
- [ ] Add the five chain attributes beside the cryo block (`:369-382`), same comment style: `p_wallplug_heat` (0.0), `eta_source_heat` (1.0), `eta_couple_heat` (1.0), `p_delivered_direct_heat` (0.0), `p_coupled_direct_heat` (0.0)
- [ ] Write the dormancy comment on that block, mirroring the cryo block's (`:370-374`): a concept knowing its heating powers binds the direct terms; a concept deriving them binds the chain and zeroes the direct terms
- [ ] Add `calc heat : 'Heating Power Chain'` with its five input bindings — **attribute references only, no expressions**
- [ ] Remove `attribute p_input` (`:343`) and `attribute eta_pin` (`:351`)
- [ ] Remove `attribute p_ecrh` (`:517`); its role passes to `p_delivered_direct_heat`
- [ ] `calc pb`: `in p_input_in = heat.p_coupled;` (was `= p_input`) and `in p_wallplug_in = heat.p_wallplug_total;` (replacing `in eta_pin_in`)
- [ ] Heating cost calc (`:526`): `in p_ecrh_in = heat.p_delivered;`
- [ ] Add the `mfe_heating_chain` import
- [ ] Grep the whole plant for every other reader of `p_input`, `eta_pin`, `p_ecrh` and re-route each; **`sustainment_ok`'s `p_aux_installed_in` (`stellarator_plant.sysml:1122`) is one of them** and must read `heat.p_coupled`
- [ ] `uv run agentic-mbse validate models` — Levels 1–3
- [ ] Run codegen; confirm no `SI_EXPRESSION_SOURCE_UNSUPPORTED` and that the chain appears as a module with its four outputs

**Test requirements.** None; Phase 3 is the first phase with a checkable number.

**Validation checkpoint.** Levels 1–3 pass. Codegen produces the chain module. The `Unused calc def` warning is gone.

**Gate.** No reader of the three retired attributes remains anywhere under `models/`. A missed reader becomes a silent zero, not a parse error — grep, do not assume.

---

## Phase 3 — Concept instance and baseline parity

**Overview.** Bind the stellarator's values and prove the baseline is unchanged.

**Design reference.** § Proposed design → "Changed: `models/designs/stellarator_09/stellarator_plant.sysml`"; § Expected baseline behaviour (the five-row table); D1's fidelity note and D2's stated-assumption paragraph, both of which are written **verbatim into doc comments**, not paraphrased.

**Files.** `models/designs/stellarator_09/stellarator_plant.sysml` — REFINE.

**Checklist.**
- [ ] `:>> p_wallplug_heat = 100.0` with a doc comment carrying: the source (Table 2 image, "Required plasma-coupled ECRH power [MW] 50"), the derivation (that 50 divided by the chain's stated `eta_source x eta_couple = 0.50`), and D1's fidelity note that a future `eta_source` sweep moves coupled power off the printed 50
- [ ] `:>> eta_source_heat = 0.50` citing `costing_constants.yaml:105` / `defaults.py:104-108`, basis "gyrotron wall-plug, ITER procurement calibrated"
- [ ] `:>> eta_couple_heat = 1.00` carrying **D2's stated-assumption paragraph in full** — what it asserts, that it is an idealisation and not a measurement, its direction of optimism, and that a sourced figure would enter at this one attribute (MR-WI039-3; this doc comment is the requirement's evidence)
- [ ] `:>> p_delivered_direct_heat = 0.0` and `:>> p_coupled_direct_heat = 0.0`, each saying the chain is live so the direct term is zeroed (the `p_cryo = 0.0` precedent at `:724`)
- [ ] Remove the `p_input` (`:636-638`), `eta_pin` (`:648`), and `p_ecrh` (`:845`) bindings; **preserve the WI-037 coupled-power correction's substance** — it now belongs on the chain's `p_coupled`, and losing it would re-open a closed question
- [ ] Regenerate; execute at the baseline
- [ ] Compare against `20260903-priced-levers/results/baseline_result.json`: coupled power 50.0, delivered 50.0, `heating_cost__cost` $264.145M, wall-plug term 100.0, `q_eng`, `rec_frac`, LCOE 307.08712042841586, and **all nine constraint verdicts** including `sustainment_ok` violated and `cond_strain_ok` satisfied
- [ ] `uv run agentic-mbse validate models` — Levels 1–3

**Test requirements.** Record every compared number in the phase notes with its before/after, whether or not it moved.

**Validation checkpoint.** Every row of the design's expected-behaviour table holds.

**Gate.** **If any baseline value moves, stop and derive why before continuing.** A moved number means the design's arithmetic and the model's differ. Disclose and explain it; never fit it (`goal.md` § Invariants, MR-WI039-10). A tuned baseline would forfeit the round.

---

## Phase 4 — Independent verification and the anchor test

**Overview.** The oracle computes the chain itself, and the perturbation test demonstrates the anchor.

**Design reference.** § Proposed design → "Changed: `exploration/stellarator_e2e/verify_stellaris.py`"; § Validation plan items 4 and 5. Key decision: the oracle's chain is written **from the design's table**, not transcribed from the generated module — parity between two copies of one expression verifies nothing (MR-WI039-5).

**Files.** `exploration/stellarator_e2e/verify_stellaris.py` — REFINE.

**Checklist.**
- [ ] Replace the `p_input=50.0, ..., eta_pin=0.5` defaults (`:187`) with `p_wallplug_heat=100.0, eta_source_heat=0.50, eta_couple_heat=1.00`
- [ ] Write the oracle's own chain arithmetic — delivered, coupled, wall-plug total — **from `design.md`, with the file's other source-facing code closed**
- [ ] `p_th` (`:380`) takes the oracle's own coupled power; `recirculating` (`:391-392`) takes the oracle's own wall-plug total; the `p["p_input"] / p["eta_pin"]` term goes
- [ ] Heating cost (`:417`) takes the oracle's own delivered power
- [ ] Run the parity check; record the agreement and its tolerance
- [ ] **Perturbation test:** set `eta_source_heat` to 0.45 alone and confirm coupled power, heating cost, wall-plug draw, `q_eng`, and `sustainment_ok`'s margin all move; confirm the oracle moves with the model; restore 0.50. Record the numbers — this is the grader's stated `why_not_next` test and its evidence
- [ ] Note in the phase record that the oracle was written independently and by what means

**Test requirements.** The perturbation numbers are recorded in the implementation notes and become the round's evidence for the P2 anchor's "verified".

**Validation checkpoint.** Oracle and model agree at the baseline; both move together under perturbation.

**Gate.** If the oracle disagrees, one of the two is wrong — find out which before touching either. Do not adjust the oracle to match the model; that is what MR-WI039-5 exists to prevent.

---

## Phase 5 — Restatement, regression, traceability

**Overview.** Three entry points retired; every consumer of them restated, re-derived from live evidence and never patched to match (MR-WI039-9). This phase is bookkeeping in character and unforgiving in practice.

**Design reference.** § Design decisions D1 (what retires, and the exact `p_wallplug = p_input / 0.50` mapping); spec MR-WI039-9.

**Known surface, mapped before starting** (grep of `p_input|p_ecrh|eta_pin`, 2026-09-03):

| file | what it is |
|---|---|
| `exploration/stellarator_e2e/studies/manifest.json` | the declared `p_input`/`p_ecrh` tie — **removed, not rewritten**: the tie is structural after D1 |
| `studies/20260901-sustainment-fence/` — `axes.json`, `study.py`, `scan.py`, `indicators.json`, `snapshot.json` | swept the tie; restated to wall-plug |
| `studies/20260903-priced-levers/` — `axes.json`, `study.py`, `scan.py`, `indicators.json`, `snapshot.json`, `results/window_scan.json` | same |
| `studies/oracle_entry.py` | entry-point names |
| `exploration/stellarator_e2e/emit_1cfe_point.py:108-110` | emits `p_input`, `p_ecrh`, and `eta_pin_effective` via `model._effective_eta_pin` |
| `exploration/stellarator_e2e/handshake_1costingfe.py:210,238-240,262,439` | the 1costingFE handshake reads `eta_pin_effective` and `p_ecrh` |
| `exploration/stellarator_e2e/onecfe_point.json` | handshake fixture at `p_input = 30.0` |
| `tests/models/test_power_balance.py` (9 hits), `tests/models/data/mfe_census.json` (3) | model-side battery |
| `tests/study/data/{R,a,I_coil,R+tie,availability,interest_rate}.expected.json` (2 each) | study-side expectations |

**The handshake is the sharp edge.** `emit_1cfe_point.py` calls `model._effective_eta_pin(p)`; with `eta_pin` retired that call breaks. The handshake compares this model against 1costingFE, which still has `eta_pin`, so the seam must translate rather than propagate: emit `eta_pin_effective` from the chain's `eta_pin_eff` output. **If the handshake cannot be honestly translated, that is a `PREREQUISITE` return, not a thing to force.**

**Checklist.**
- [ ] Restate both committed study definitions: coupled 50–110 MW becomes wall-plug 100–220 MW at `eta_pin_eff = 0.50`; **write the restatement note into each study's record dir** naming what changed and why the experiment is the same experiment
- [ ] Remove the `p_input`/`p_ecrh` tie from `studies/manifest.json`; record in the round trail that a workaround was removed because the model now declares the invariant itself
- [ ] Re-derive every changed expectation **by running it**, not by editing the number to match; note each one's derivation
- [ ] Repair `emit_1cfe_point.py` and `handshake_1costingfe.py` to emit `eta_pin_effective` from `eta_pin_eff`; re-run the handshake and record its agreement
- [ ] `tests/models/test_power_balance.py` and `mfe_census.json` updated to the new interface
- [ ] Six `tests/study/data/*.expected.json` re-derived
- [ ] Create the SV rows (`uv run agentic-mbse pm add-validation`) now that element names are fixed: the baseline chain identity, and the perturbation response
- [ ] Traceability rows for the new elements (`uv run agentic-mbse pm trace-element`)
- [ ] Full `uv run agentic-mbse validate models` — Levels 1–6, with 4–6 reviewed and any residue recorded
- [ ] `tests/models` → expect 48 passed / 13 skipped or better, with any delta explained
- [ ] `rm -rf .integration_workspace`; `tests/study` → expect 356 passed / 1 skipped or better, with any delta explained
- [ ] Verify each spec success criterion explicitly and record where its evidence is

**Gate.** Both batteries green with every delta explained; every restated expectation carries its derivation; no expectation patched to match.

---

## Feasibility concerns

1. **Codegen refuses something in Phase 2.** *Mitigation:* all arithmetic is inside the calc def and every input binding is a bare attribute reference — the known refusal mode is avoided by construction. If it refuses anyway, that is a `MECHANICAL_FAILURE` with a retry, not a design defect, until proven otherwise.
2. **A missed reader of a retired attribute becomes a silent zero.** *Likelihood: medium. Impact: high* — a silent zero in `recirculating` would move `q_eng` without any error. *Mitigation:* Phase 2 greps rather than assumes, and Phase 3's baseline parity is the backstop that catches it.
3. **The handshake cannot be honestly translated.** *Mitigation:* named above; a `PREREQUISITE` return is the honest outcome, not a forced fixture.
4. **The restatement is larger than the ~30 sites budgeted.** *Mitigation:* the mapping is exact, so the work is mechanical; if it runs long the round still closes on it, because a half-restated study is worse than a slow one.
5. **`tests/study` costs ~7.5 minutes per run.** *Mitigation:* run it once at the end of Phase 5, not per checklist item.

---

## MR-WI039-9 restatement — entry-point retirement and committed-study consequences (2026-09-03)

**An ordering deviation, recorded first.** MR-WI039-9 and the WI-037 precedent both say this restatement is written *before* the regeneration commit. It was written after. The regeneration was reversible and was in fact re-run (the package regenerates idempotently now), and no committed study was touched in between, so nothing was lost — but the sequence was not followed and saying so is cheaper than the alternative.

### What retired, what replaced it

| retired entry point | value | replaced by |
|---|---|---|
| `stellarator_09__stellaris__p_input` | 50.0 | `p_wallplug_heat = 100.0` through the chain (`p_coupled = p_wallplug x eta_source x eta_couple`) |
| `stellarator_09__stellaris__p_ecrh` | 50.0 | the chain's `p_delivered`, which the heating account now reads |
| `stellarator_09__stellaris__eta_pin` | 0.5 | `eta_source_heat = 0.50` and `eta_couple_heat = 1.00`, whose product the chain exposes as `eta_pin_eff` |

Minted, and settable: `p_wallplug_heat`, `eta_source_heat`, `eta_couple_heat`, `p_delivered_direct_heat`, `p_coupled_direct_heat`.

**Census, re-derived from a live generation and not patched to match** (`/tmp` scratch script against `tests/model_families.materialize_canonical_subset` + `run_codegen`, the same path the spine suite uses): entry points **197 → 199**; the three retired keys leave `design_attribute` and the five new ones enter it; semantic fingerprint `3cb690aab05e…` → `48731d1570bb…`. `tests/models/data/mfe_census.json` was rewritten from that generation's own model contract.

### The mapping, and why it preserves meaning

At `eta_source_heat x eta_couple_heat = 0.50`, a point that swept installed plasma-coupled power `p` is the same point as one that sweeps wall-plug power `2p`:

- `p_coupled = p_wallplug x 0.50` → the power balance's `p_th` term and `sustainment_ok`'s installed side are unchanged.
- `p_delivered = p_wallplug x 0.50` → the heating account's driver is unchanged, so `heating_cost__cost` is unchanged.
- `p_wallplug_total = p_wallplug` → the recirculating term equals the old `p_input / eta_pin` exactly.

So the coupled-power sweeps of both committed studies map to wall-plug sweeps by a factor of exactly 2: **50 → 100 MW** and **110 → 220 MW**. The mapping is exact in IEEE arithmetic (multiplication and division by 0.5 are exact), not approximate.

### The two committed studies

`20260901-sustainment-fence` and `20260903-priced-levers` each swept the axis `p_input+tie` — `p_input` fanned out with `p_ecrh` riding as a declared tie.

**They are not replayable as written at this package, and their record dirs are not edited.** That is the standing position for every committed study at a moved pin (`goal.md` § Invariants: the five prior committed studies "stand at their own pins and are not reproducible as written at `6262dbf4…`"). Their `axes.json`, `study.py`, `scan.py`, `indicators.json` and `snapshot.json` describe what ran, at the pin it ran on. Rewriting them would falsify a record rather than restate it.

**What a replay at this package would do instead:** sweep `stellarator_09__stellaris__p_wallplug_heat` over 100 and 220 MW, with no tie declared, and read the same channels. Every measured result carries over unchanged, because every channel it read is unchanged at the mapped points.

### The tie is gone, and that is the point

`studies/manifest.json` declared `p_ecrh` as riding with `p_input`, on the reasoning that "sweeping `p_input` while holding `p_ecrh` would heat a plasma with a heating system that was never bought." That is true, and it was a study-layer declaration compensating for the model not knowing the two constants were one physical quantity.

They now descend from one wall-plug input, so the invariant holds structurally and the declaration has nothing left to do. The tie entry is **removed** from `manifest.json`, not rewritten. Only the `magnet__R0` / `R` tie remains, which is a genuinely different case: two model attributes for one physical radius, with no chain relating them.

### The 1costingFE handshake — a pre-existing break, not one this item caused

`handshake_1costingfe.py` injects `pb__eta_pin` and `heating_cost__p_ecrh` at the calc-input level, and `emit_1cfe_point.py:110` emits `eta_pin_effective`. Both would need translation through the chain's dormant path (`eta_source = eta_pin_effective`, `eta_couple = 1.0`, `p_coupled_direct = p_input`, `p_delivered_direct = p_ecrh`, which reproduces the old arithmetic exactly and is a fair exercise of design D4).

**It was not translated, because the script does not run at this pin and has not for some time.** Verified here: it raises `FileNotFoundError` on `generated/inputs/system_design.json`, a file the package stopped generating at the model migration — and it fails there *before* reaching any heating key. Confirmed against the pre-WI-039 tree at `860ce7d1`, where that file is equally absent. `tests/study/test_no_retired_identifiers.py:36` already classifies the script as a historical record rather than an executable path.

Repairing a script that is broken for an unrelated and older reason is not this item's work, and repairing only the heating keys would leave it broken while looking repaired. The keys it would need are written above so that whoever revives it does not have to re-derive them. `emit_1cfe_point.py` needs no change at all: `model._effective_eta_pin` is *1costingFE's* method on *1costingFE's* params, and nothing in it refers to this model.

### The test surface, re-derived

- `tests/model_families.py` — `analyses/mfe_heating_chain.sysml` added to the MFE family's owned paths (the ownership test proved the omission).
- `tests/models/test_power_balance.py` — the interface test now expects `p_wallplug_in`; two stale comments describing `p_input / eta_pin` as the model's recirculating form were **amended**, not annotated beside.
- `tests/models/data/mfe_census.json` — re-derived, above.
- `exploration/stellarator_e2e/stellarator.snapshot.json` — recaptured through `capture_instance_graph_snapshot`, the producer the seam's gate 4 uses.
- `tests/study/data/*.expected.json` — six files named `p_input`; each re-derived by running, never edited to match.
