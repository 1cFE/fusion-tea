# Upstream Fix Verification: UPSTREAM-FINDINGS epic vs. fusion-tea's real IFE models

**Date**: 2026-07-06
**Verified against**: sysml-codegen `upstream-findings-epic` @ `66b616e12d29e761d13e8723c32347b31f4ff360` (PR #3, unmerged). Verification ran on the `docs-scrub` working tree @ `1bab05ac` — it branches directly off the epic HEAD and its delta (committed and uncommitted) touches no `src/` or `tests/` files, so the code under test is the epic branch exactly. Test suite green at start: 1989 passed, 4 skipped, 5 xfailed. (`uv.lock` had uncommitted modifications; dependencies resolved without issue.)
**Models**: `exploration/ife_e2e/models/` (byte-identical to canonical `models/`, workaround-applied state). Canonical models untouched; all experiments ran on fresh copies.
**Artifacts**: `snapshots/` (three extraction snapshots — the license-independent record), `evidence/` (all run logs), `bridge_v11_generate.py`, `run_anchors_bridged.py`, and in `exploration/ife_e2e/`: `generated_bridged/` (the emitted package), `pkg_bridged/`, `outputs_bridged/`.

---

## Executive verdict

The epic's fixes hold on fusion-tea's real models, and the anchors reproduce **bit-exactly** — with one loudly-labeled bridge and one genuine new defect.

Four fixes are cleanly confirmed end-to-end: quoted-name sanitization (SC-4 — `sanitize_names.py` is dead), return-style extraction with auto-implementation (SC-2 — the six `out attribute` conversions can be reverted), retyped-part indexing (SC-3 — `hif_driver_instance` is deletable), and expression fidelity (SC-6 — docstrings now show faithful math). Literal pre-fill (SC-5 stage 1) works: every emitted input-JSON key carries its value. Snapshot generation (Item 2) works on real external models and produced a V11 abort identical to the live path.

The whole plant still does not generate: the V11 params-coverage check aborts on **exactly the 10 documented cross-part bindings** — measured, reconciled 1:1 against sysml-codegen's BACKLOG P1. With a 10-value bridge (this report's `bridge_v11_generate.py`, which fills the 10 valueless entry points with the model's own literals), the package emits and anchor C ($270.1211779380445/MWh) reproduces through the teax executor **in a single pass**: both Meier feedback edges (gamma → lcoe, cost_billions → meier_capital) close via generated wiring, so the WI-015 two-pass harness feedback is dead. Anchors A ($252.30) and B ($68.69) reproduce at module level.

The new defect: the SC-1 constraint-drop warning (Item 1, REQ-EXT-09) **does not fire on fusion-tea's models**. It enumerates `ConstraintUsage` exact-type, but `assert constraint viability` parses as `AssertConstraintUsage` — syside's `model.elements()` does not match subtypes. The silent drop SC-1 complained about persists for precisely the def-typed assert shape fusion-tea uses.

---

## Per-finding verification matrix

| Finding | Epic item | What ran | Evidence | Verdict |
|---|---|---|---|---|
| SC-2 return-style extraction | 3 | Fresh copy, six outputs reverted to `return x : Real = expr` (incl. the mixed form: `out attribute cost_billions` + `return gamma` in one def); `syside check`; live extraction; generation | All 6 defs extract with correct outputs; all 6 `fully_compilable`; all 6 impls `AUTO_IMPLEMENTED = True`, zero `NotImplementedError`; checks pass (`evidence/06`, snapshot `e2_return`) | **FIXED** |
| SC-3 type indexing | 4 | Fresh copy, `part hif_driver_instance` removed; live extraction; graph inspection | `meier_cost` instantiates once, from `part :>> driver` alone (`hif_plant_pkg__hif_plant__driver__meier_cost`); gamma edge intact; V11 offenders 10→9; `syside check` passes (`evidence/07`, `08`) | **FIXED** |
| SC-4 quoted names | 5 | Bridged package emitted with `'IFE LCOE'` + four quoted Meier defs, **no post-processor** | 0 quoted/spaced filenames; 32/32 `.py` compile; registry imports and instantiates in the executor venv, 6 modules, consistent class names | **FIXED** — `sanitize_names.py` dead |
| SC-5 literal pre-fill | 9 | Derived input JSONs from the graph | Every minted key pre-filled (22/22 non-null vs WI-015's 2 of 18); the ~14 Hawker literals all present with correct values (`evidence/04`) | **FIXED** (within the wiring boundary — see below) |
| SC-5 cross-part wiring | 10 | Graph inspection + whole-plant generate (live AND from-snapshot) | gamma→lcoe edge wired: `lcoe_calc.driver_cost_constant` ← `driver__meier_cost__gamma` as `module_output`. **Bonus beyond the Item 10 audit**: `meier_capital.driver_cost` ← `cost_billions` is wired too. Whole-plant generate aborts at V11 on exactly 10 offenders, identical live vs snapshot (`evidence/01`–`03`) | **PARTIAL** — wired edges execute (bridged); 10 bindings remain |
| SC-6 expression fidelity | 6 | Docstring/stencil inspection of emitted package | 0 `LiteralRationalEvaluation` in the package; lcoe expression byte-faithful to `ife_lcoe.sysml:122-125` including parens; Meier constants render as values | **FIXED** |
| SC-1 constraint warning | 1 | Live extraction + generation of the plant containing `assert constraint viability` (`ife_plant.sysml:155`) | **No warning fires.** `report_dropped_constraints` enumerates `ConstraintUsage`; the assert parses as `AssertConstraintUsage` (subclass); syside `model.elements()` is exact-type — probe: 0 ConstraintUsage, 1 AssertConstraintUsage (`viability`) found. REQ-EXT-09's test can't catch it: it counts with the same enumeration, and catf_mfe's constraints are all plain inline usages | **FAILED on real models** — new finding, file upstream |
| SC-9/SC-10 snapshot CLI | 2 | `sysml-codegen snapshot` capture of the IFE set; `generate --from-snapshot`; E2 auto-impl from snapshot | Capture works on external models; `snapshot_format_version: 1`; 6 `compilation_results` serialized; from-snapshot V11 abort byte-identical to live; return-style auto-impl survived the snapshot round-trip | **FIXED** |
| Anchors | — | `run_anchors_bridged.py` | A/B module-level, C full pipeline single-pass: all pass at rel 1e-6; run-C LCOE bit-exact vs WI-015 (`270.1211779380445`), gamma exact (`68.247088`) (`evidence/09`) | **REPRODUCED** (bridged) |

Keep the three levels separate: the gamma edge is (1) in the ComputationGraph — verified from generated wiring alone; (2) in emitted YAML — verified only via the bridge; (3) executed — verified via the bridge, bit-exact. Levels 2–3 carry the BRIDGED label, never FIXED.

---

## Workaround retirement status

| Workaround | Status after PR #3 merges |
|---|---|
| `sanitize_names.py` (SC-4) | **Retire now.** Package emits valid Python directly; the script's step-2 slot in the repro is dead. |
| Six `out attribute` conversions (SC-2) | **Optional style, no longer a workaround.** Reverting to `return` is safe (extracts, auto-implements, `syside check` passes — verified live). Revert or keep per taste; the mixed form also works. |
| `hif_driver_instance` (SC-3) | **Retire after re-anchoring channels.** Removing it works and drops one V11 offender. It moves the Meier channel EQNs: `hif_driver__hif_driver_instance__meier_cost__*` → `hif_plant_pkg__hif_plant__driver__meier_cost__*`. `run_anchors.py`'s `D`-prefix and `sweep_ife.py` must migrate; the driver's `beam_energy_mj`/`num_chambers`/`rep_rate` entry keys move the same way. |
| Two-pass gamma feedback in `run_anchors.py` (SC-5) | **Dead once the package emits.** Both feedback edges (gamma → `lcoe.driver_cost_constant`, cost_billions → `meier_capital.driver_cost`) close via generated wiring — run C passed single-pass. Gated on the 10-binding gap (or the bridge) for emission. Note the semantic shift: with the edge wired, `driver_cost_constant` is no longer an entry point, so anchors A/B (which feed it 5.0) become module-level checks — that is the model's own semantics, not a regression. |
| teax OutputRouter + scalar WriteHandler (T-1/T-2) | **Keep.** Out of the epic's scope; still required (the bridged run reused it verbatim). |
| Harness-side `ηG > 10` viability in `sweep_ife.py` (SC-1) | **Keep.** Constraints still don't execute — and see the new finding: the promised drop-warning doesn't fire either. |

---

## The residual gap (goes back to sysml-codegen BACKLOG P1)

Measured offender list, identical live and from-snapshot, reconciled 1:1 against the documented 10:

| # | Module | Input | Cross-part source (model) |
|---|---|---|---|
| 1 | `hif_plant__lcoe_calc` | `driver_efficiency` | `driver.efficiency` = 0.35 (`hif_driver.sysml:81`) |
| 2 | `hif_plant__lcoe_calc` | `driver_energy` | `driver.energy` = 14.286e6 |
| 3 | `hif_plant__lcoe_calc` | `driver_lifetime_shots` | `driver.lifetime_shots` = 6.0e9 |
| 4 | `hif_plant__lcoe_calc` | `blanket_energy_multiple` | `chamber.blanket_energy_multiple` = 1.15 |
| 5 | `hif_plant__lcoe_calc` | `yield_cost_constant` | `chamber.yield_cost_constant` = 5.0e6 |
| 6 | `hif_plant__lcoe_calc` | `target_cost_constant` | `target_factory.cost_per_target` = 10.0 |
| 7 | `hif_plant__recirc_calc` | `eta` | `driver.efficiency` |
| 8 | `hif_plant__recirc_calc` | `blanket_multiplier` | `chamber.blanket_energy_multiple` |
| 9 | `hif_plant__driver__meier_cost` | `driver_efficiency` | own part's `efficiency` (in-part self reference through the calc-usage binding) |
| 10 | `hif_driver_instance__meier_cost` | `driver_efficiency` | same, on the workaround instance (disappears when the instance is deleted — offenders drop to 9) |

Mechanically: the entry points for all 10 already exist in the derived parameter groups but are **valueless** (`default_value: None`); JSON emission omits null keys; V11 correctly refuses. So the P1 fix can land as either wiring (module_output edges, like gamma) or value propagation (fill the defaults from the referenced attributes' literals) — the bridge demonstrates the latter is sufficient for the anchor semantics. The BACKLOG P1 acceptance test (full YAML, zero offenders, run-C $270.12 within tolerance) is now known-achievable: this run produced exactly that result with 10 hand-supplied values.

**New finding to file alongside**: the SC-1/Item 1 constraint-drop warning misses `AssertConstraintUsage`. Fix is small — enumerate assert usages too (or make the adapter's `elements_of_type` subtype-aware) — plus a def-typed-assert fixture, since the REQ-EXT-09 test's structural count uses the same blind enumeration and catf_mfe carries no assert-shape constraints. Owner split: the exact-type behavior is in agentic-mbse's `syside_adapter.py` / syside's `model.elements()`; the consumer is sysml-codegen's `extractor.py:report_dropped_constraints`.

Minor observation, same theme: the `snapshot` capture subcommand (`snapshot/capture.py`) does not run the constraint report at all — it never calls `report_dropped_constraints` (`pipeline_builder.py:685` is on the generate path). Once the assert-shape bug is fixed, capture should report too, or a snapshot-first workflow never sees the warning.

---

## Out-of-this-epic items still open (known, don't re-file)

- **teax T-1/T-2** — primitive exit channels still need the harness router + scalar WriteHandler (reused verbatim here).
- **SC-1 full constraint execution** — deferred to its own future epic; viability stays harness-side. (The *warning* regression above IS new and should be filed.)
- **A-1/A-2 validation-stack items** — agentic-mbse side, tracked by epic Item 12's close-out.

---

## Coordination actions for fusion-tea once PR #3 merges

1. **Delete `sanitize_names.py`** and drop step 2 from the WI-015 repro recipe.
2. **Delete `part hif_driver_instance`** from `hif_driver.sysml:100` (canonical models), then **re-anchor channel names** in `run_anchors.py` and `sweep_ife.py`: Meier channels move to `hif_plant_pkg__hif_plant__driver__meier_cost__*` (exact list in `evidence/08`).
3. **Optionally revert the six `out attribute` back to `return`** (`ife_lcoe.sysml:122`, `fusion_cycle.sysml:26`, `hif_economics.sysml:40,60,80,103`) — verified safe. Keep `cost_billions` as `out attribute` (it is a consumed channel).
4. **Simplify `run_anchors.py`** once whole-plant emission lands (BACKLOG P1): drop the two-pass feedback and the hand-built input writing for wired values; keep the T-1/T-2 router. `run_anchors_bridged.py` in this folder is the working template — it is the post-P1 harness minus the bridge.
5. **Keep `sweep_ife.py`'s ηG > 10** and don't expect a constraint warning until the AssertConstraintUsage fix lands.
6. The captured snapshots in `snapshots/` decouple all future inspection of this model set from the syside license (expires 2026-08-06). Re-capture after any model edit.

---

## Reproduce

```bash
# Whole-plant V11 abort (license-free, from the committed snapshot)
cd ~/1cfe/sysml-codegen && uv run sysml-codegen generate \
  --from-snapshot ~/1cfe/fusion-tea/work/active/20260706_upstream-fix-verification/snapshots/ife_workaround_applied.snapshot.json \
  --output /tmp/gen_wholeplant --package-name ife_tea --pipeline-name ife_hif --overwrite
# -> ERROR V11, 10 offenders

# Bridged emission + anchors
uv run python ~/1cfe/fusion-tea/work/active/20260706_upstream-fix-verification/bridge_v11_generate.py
cd ~/1cfe/fusion-tea/exploration/ife_e2e && ../pipeline_spike/.venv-exec/bin/python \
  ~/1cfe/fusion-tea/work/active/20260706_upstream-fix-verification/run_anchors_bridged.py
# -> ALL ANCHOR CHECKS PASSED (rel tol 1e-6) — run C wired, single pass
```

Note on the license: live commands need `SYSIDE_LICENSE_KEY`; the CLI picks it up via `load_dotenv()` in agentic-mbse's CLI module (resolving `~/1cfe/agentic-mbse/.env` regardless of cwd). Bare `uv run python` scripts must `source` a `.env` themselves — this cost the session a detour and is worth knowing.
