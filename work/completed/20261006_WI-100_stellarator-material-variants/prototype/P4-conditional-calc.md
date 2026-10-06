# Probe P4 — does `'REBCO Shape Branch'` auto-implement?

Design § 7 P4 (K12, D15). Run 2026-09-30 on the scratch probe tree.

## What was run

1. `sources/probe_variants.sysml` first declared the calc exactly as design § 2.4 writes it: `out attribute shape_mode : Real = if B_peak_in > B_knot_max_in ? 1.0 else 0.0;`. `syside check` passed; `sysml-codegen generate` then refused the model (`evidence/generation-p4-if-expression.log`): `ERROR: Model failed exact-route validation: SI_EVIDENCE_INCOMPLETE: if B_peak_in > B_knot_max_in ? 1.0 else 0.0: … resolved reference has no exact target`.
2. The expression was removed, leaving `out attribute shape_mode : Real;` with the equation in the doc (the form of every other manual calc, e.g. `'Conductor Peak Field'`). Generation succeeded and emitted a manual stub `handwritten/probe_variants/rebco_shape_branch_impl.py` that raises `NotImplementedError` (45 manual stubs: the reference's 44 plus this one).

## Result

**Does not auto-implement — and the `if` form is refused outright, not stubbed.** The design expected a stub from the `if` form; the toolchain rejects that form at validation instead. The design's fallback absorbs it: the calc def declares its inputs and its one output with the equation stated in its doc, and the handwritten fallback body `bodies/magnet_material_variants/rebco_shape_branch_impl.py` (`shape_mode = 1.0 if B_peak > B_knot_max else 0.0`, WI-099 typed adapter) completes it. The build's body-set assertion includes it (§ 1.6 step 4, test 10). The calc is single-output, so its generated stub returns a bare `float` rather than a tuple; the adapter returns the single value.
