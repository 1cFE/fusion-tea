# Alignment Brief — WI-023 magnet-field-errata-B9

**Created:** 2026-07-18 (immutable — no stage cursor, no status, no execution log)
**Input source:** handoff `/tmp/handoff-20260718-094631.md` (2026-07-18)
**Work item:** WI-023 `magnet-field-errata-B9`, registered in `work/BACKLOG.md` (P1, epic "MFE Cost Modeling — Tokamak & Stellarator"). Standard route, entry at `/spec-model`.

## Objective

Correct the magnet subsystem's coil-cost field from B = 5.86 T (bound at `models/designs/stellarator_09/stellarator_plant.sysml:112` on a citation to a Table 3 text row that does not exist in the table image — an extraction phantom) to the axis-averaged B₀ = 9.0 T printed independently in the Table 2 and Table 5 images. Rewrite every doc that names 5.86 (instance "THREE MAPPING TRAPS" note, `verify_stellaris.py` oracle `magnet_B`, runner headline asserts), re-baseline, and hold the standing validation/regen/handshake bars. Additionally (owner decision, this Align): sweep the Stellaris source's coil/cryo sections and fold **all** sweep findings — the `p_tf = 111.0` phantom included — into WI-023 scope.

Expected movement (hand estimate, [AGENT], implement produces exact numbers): magnet $4.117B → ≈$6.32B (×9.0/5.86), total ≈$11.8B, LCOE ≈$215/MWh, magnet share ≈53%. Baseline moved from: WI-022 executed record (`work/completed/20260718_WI-022_predictive-confinement/plan.md` Implementation Record; total $9.586B, LCOE $176.07/MWh, net 804.1 MW).

## Decision-carrying inputs, graded

- **[OWNER] 2026-07-18 (WI-022 errata record, `work/completed/20260718_WI-022_predictive-confinement/spec.md` §"Surfaced extraction errata"):** magnet-field correction is a separate follow-up item, registered as WI-023.
- **[OWNER] 2026-07-18 (this Align, verbatim):** *"yes do the sweep during spec stage, and include in scope all findings"* — the coil/cryo source sweep runs during spec, and all findings (p_tf fold-in included) are in WI-023 scope.
- **[OWNER] 2026-07-18 (this Align):** hard stop for owner checkpoint after `/spec-model`; nothing past spec runs until scope approval.
- **[OWNER] 2026-07-18 (this Align):** SV-016 band (Q_eng ~10–40, `pending`) is re-flagged at close if p_tf changes (p_tf changes move p_net and q_eng).
- **[OWNER] standing:** one item at a time through the modeling PM pipeline; no-fallbacks rule (never invent a value for a missing input — if no admissible source value exists for a slot, surface the honest options, owner decides).
- **[AGENT] (evidence, WI-022 session, verified against images):** Table 3 image (`page_003_table_0.png`) has no B row; Table 2 (`page_002_table_0.png`) and Table 5 (`page_009_table_0.png`) images both print axis-averaged B₀ = 9.0 T; Table 2 also prints peak conductor field 24.9 T — a distinct quantity that must not be conflated with the loop-center field the cost formula takes. Table 2's only 111 is stored magnetic energy [GJ]; no coil-conduction-power row exists.
- **[INHERITED: handoff]** working procedures and bars: validation baseline (L1=0, L2–L5 pass, L6 = 6 pre-existing offenders, zero new), regen via `~/1cfe/sysml-codegen` snapshot + `bridge_v11_generate.py` (`preserve_handwritten=True` must survive), execute `run_stellaris.py` bit-exact rel 1e-9, handshake `handshake_1costingfe.py` with empty `git diff` on `handshake_comparison.json`, mirroring discipline canonical↔staged. Next free SV: **SV-030**.
- **[INHERITED: PROTOCOL]** `knowledge/holdout/aries-cs/PROTOCOL.md` §3 barred paths; physics from admissible Stellaris sources only; engineering/cost from 1costingFE (pinned `0254385`); every demo work item lists the PROTOCOL as Required Reading.

## Premise caveats (recorded, not resolved)

- The Table 3 image crop is right-truncated ("Valu[e]" header cut). "5.86 is a hallucinated row" is near-certain, not absolute: the 8 visible rows map 1:1 onto the extracted text's 8 rows, scrambled, with no B row. If a higher-fidelity crop or the original PDF ever surfaces, re-check. Positive evidence for 9.0: two independent printed values + the paper's "high-field" framing.
- The original Stellaris PDF is not in the repo; the iter-02 `stellaris-paper-details` extraction is the same pipeline lineage and is **not** an independent witness.

## Parked pending checkpoint

- **p_tf resolution choice.** The sweep decides what's presentable: a sourced replacement value if one exists in the coil/cryo sections, else the honest options (keep 111 MW with a downgraded "magnitude assumption, phantom-sourced" citation, or rescope the slot). If no sourced value: the choice is the owner's at the spec checkpoint — not made by any agent.
- Everything downstream of spec (design, plan, implement) parks until the checkpoint.
