---
Verdict: pass
Created: 2026-09-15
Related Artifacts:
  Spec: ../../../../active/WI-064_current-driven-magnet-inventory-sizing/spec.md
---
# Independent source, mathematics and interface review

**PASS for the bounded conditional design; implementation may proceed.** Fresh non-author reviewer `/root/reviewer`, entering revision `c4d720db886213de94bf2dc4c3131a3453dca690`. Reviewed spec SHA256 `c006b93280f908c4f987181550a32d59322dce52b39165dd052411fb253d1378`, goal, coupled-dependencies assessment, canonical current/grade/fit/inventory/procurement equations, magnet bindings and radial-center equation. No material design defect found. This releases design only; preservation, generated behavior and coupled agreement require implementation evidence.

## Derivation and interfaces

[AGENT REVIEW] With tape area At in m² and available per-tape critical current Ia in A, the proposed required pack area simplifies to `Areq = NI*At/(u_allow*Ia*ft)`. Thus `jreq = u_allow*Ia*ft/(At*1e6)` is A/mm². Turn current cancels from area but remains in required parallel tape count and series turns. All six proposed outputs have distinct meanings; the available-current output excludes the operating allowance.

[AGENT REVIEW] Existing procurement gives `Lt = n*Apack*f_vol*c*ft/At` and `Lc = n*NI*f_set*c/Iturn`. Consequently `(Lt/Lc)*f_set/f_vol = Apack*ft*Iturn/(NI*At)`. Selecting `jreq/m` reconstructs exactly `m*Nreq` reference parallel tapes algebraically. The reference operating fraction is `u_allow/m`; allowance enters once. Set-effective count remains different by `f_vol/f_set`. Continuous counts do not certify integer cable stacks or the weakest coil.

[AGENT REVIEW] Binding final effective density to the selector, while supplying the unchanged grade output as its legacy input, avoids duplicate field-envelope enlargement. Mode 1 purchases inventory from actual field; the separate selected-envelope predicate remains necessary. Mode 0 retains its density producer and must demonstrate unchanged old scalars and all twenty predicates at reference and off-design points.

[AGENT REVIEW] The dependency is acyclic: independent radial allocation → coil center (`mfe_plasma_scaling.sysml:144`) → actual peak field → required inventory → pack dimensions → fit against that allocation. A fixed-field required cavity is only a diagnostic; choosing a larger allocation requires reevaluation. Required cavity must never overwrite allocation.

## Evidence and limits

[INHERITED] The original-source checks in `absolute-conductor-current-margin/evidence/source-design-review.md` and reviewed fit implementation in `winding-pack-casing-fit/evidence/implementation-review.md` remain applicable. No empirical normalization or interpretation changes; no new source inspection was necessary. Preserve their construction, field-domain/extrapolation, sharing and qualification limits. Only the quarantine protocol was read.

[AGENT REVIEW] The stated finite-domain guards and unchanged exact predicates are appropriate. Test multiplier 1 boundary residuals without clipping; multiplier 1.01 is explicit extra inventory, not altered acceptance. Report relative current closure separately from pass/fail.

[AGENT REVIEW] Coordinator clarification holds selected B_max at 24.9 T for the principal comparison; historical 30 T cases are separate controls. Mode 0 must pass the legacy density through exactly. Its new required-output arithmetic may refuse extreme inputs through overflow/underflow even where a legacy intermediate remained representable; reference/off-design preservation tests do not certify equality of every floating-point admissible domain. New mode/multiplier inputs have explicit guards in both modes.

[AGENT REVIEW] Fixed 50 kA and square principal sections support the bounded comparison. Missing pack-width field effects, casing stiffness, actual thermal surfaces, coolant behavior and manufacturing effort prevent engineering qualification. Existing stress/thermal proxies and energy-derived support cost are conditional estimates. No missing dependency defeats the explicitly conditional internal-consistency claim; broader physical feasibility claims are not released.

## Oracle and protocol follow-up

**PASS for static oracle/interface and pre-scan protocol review, 2026-09-15.** No package or study execution was performed. Generated ABI, numerical preservation and coupled runtime acceptance remain for the later integration audit. Reviewed SHA256: `verify_stellaris.py` = `9a429bba9eacb853423d3481d9ea8001f906036870106a046d5889a13a414aab`; `studies/oracle_entry.py` = `e496a5e6690fb7109190913c0edaddc866f922152af15abe8aeb6ded861e5007`; `studies/20260915-joint-magnet-sizing/protocol.md` = `71237e5be95936ec08b02ffd0337a812e14d60702bc1514c7dd779dd1751df45`.

[AGENT REVIEW] `_current_driven_sizing` independently inverts capacity per composite area. Its six outputs match the released meanings and current native interface. Retention enters capacity once; allowable fraction enters usable density once. Mode 0 returns the legacy density unchanged; mode 1 divides required density by physical inventory multiplier. `compute` sends that selected density through the existing size, volume, stress, thermal and material paths. Its direct mode 1 procurement-volume calculation and selected-area fit calculation are algebraically equivalent independent expansions. Neither reintroduces the grade factor. Both new owner inputs and all six outputs have explicit oracle mappings. Final current margin still comes from reconstructed procurement inventory.

[AGENT REVIEW] The sizing helper obtains tape performance by invoking the existing independent current checker with unit dummy lengths. This imports extra distribution/count arithmetic and its numerical refusals, although those quantities cancel from the sizing equations. It also moves current-domain validation earlier in mode 0. No issue is apparent inside the proposed scan domain; extreme-domain equivalence and legacy invalid-input diagnostic precedence are not certified by this static pass. Cover relevant refusals and preservation in the forthcoming tests.

[AGENT REVIEW] The protocol preserves 24.9 T, allowance 0.8 and all twenty predicates for the principal scan, with fixed turn current, square section and default performance. Historical 30 T controls and hypothetical performance cases are explicitly separate. The proposed space/current bounds are declared study assumptions; the allocation-first formulation requires no iterative closure. Failed/refused proposals, exact boundary signs and numerical residuals are retained. The native-case cap, recorded rationale for expansion and finite-sample interpretation adequately bound this exploration. Material factors 1.10/1.35 correspond to the previously reviewed 220/270 A versus 200 A scenario; construction and qualification limitations remain. Any tightened scan must retain the broad-scan diagnostics and cannot support a claim beyond the actually evaluated bounds.

[AGENT REVIEW] No material correction is required before the oracle scan. This verdict does not assert native/oracle agreement, feasible-design existence, complete cost propagation or engineering qualification.
