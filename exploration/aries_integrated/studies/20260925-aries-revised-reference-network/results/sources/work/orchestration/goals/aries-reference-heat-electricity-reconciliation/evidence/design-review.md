# Design review — WI-092 network heat-driven closure

Verdict: **FINDINGS**

1. **R3 "sufficient" leg is not what the model will show.** Design and plan say that at C3 inputs s = 0.85 transfers the PbLi heat ("all removed at that stage"). The scratch check contradicts this: at s = 0.85, q_pbli = 1429.4 of 1485.8 MW (56 MW unmet); 50 MW still at 0.90. Cause: above s ≈ 0.61 (Ch_pbli/C) the PbLi stage is bounded by its primary capacity rate, which no split lifts; and the higher turbine temperature raises the heater inlet, so the helium stage also caps (≈53 of the 109.9 MW total). Restate the triple as a direction test (PbLi unmet falls from 0.55 to 0.85; divertor unmet appears at 0.98; hardware identical) and state that the helium stage binds in mode 1 at C3. Severity: correct-before-implementation.

2. **Consumer meaning under mode 1 is asserted, not shown.** In mode 1 `pbli_secondary_out` and `divertor_secondary_out` become per-stream outlets, the series identity `pbli_secondary_out = turbine_temperature` breaks, and `*_terminal_difference` must use the branch Cs. Turbine, recuperator and precooler (plant.sysml 324–367) bind only `turbine_temperature` and keep meaning; `heater_inlet` stays the first-stage whole-flow inlet, so the recuperator residual holds. The ledger and screens lie past the given lines; list which residuals read per-stage channels and confirm none assumes chaining. Severity: correct-before-implementation.

3. **Interface change is more than two keys.** Five outputs are added (546 → 551 per point) and the bound calc type changes; the migration report should list them. Note.

4. **Domain of s in mode 0 is ambiguous** ("refused otherwise" in mode 1 versus "unused but validated"). State one rule. Note.

5. **Disclosure.** The copy and the retained, unbound definition are stated plainly in spec and design; put the same sentence in the new calc def's doc comment and the completion docstring. Note.

Equations verified: stage formulas match the reviewed completion; Tmix = T1 + (q_p + q_d)/C and Tt = Tmix at the root; F is strictly increasing (slope ≥ C(1 − ε_r·k) > 0 minus nonincreasing Σq, with T1 nondecreasing because K_he ≤ C); bracket signs hold in mode 1 since Tmix ≤ max(R, L_he, L_pbli, L_div); refusing s ∉ (0,1) is the right domain. Fidelity: Fig. 12 shows the blanket-helium stage on the whole flow, then PbLi and divertor-helium stages in parallel rejoining before the turbine; the design matches and names its omissions (branch pressure loss, mixing loss, control law).

**MR-7: compliant** for the affected scope at design level. Both new quantities are supplied inputs; no UA, flow, rating or bound is derived from demand; a wrong split reports unmet heat and enlarges nothing; hardware roles are unchanged. Add to the role table that s stands in for the unmodelled branch hydraulic balance and that the 0.85 default was informed by the C3 heat proportion. Executed evidence is for the implementation review, after finding 1 is corrected.

Not covered: ledger and capacity-screen bindings past plant.sysml line 420; the SysML definition and completion code (unwritten); replay tolerance for exactly-zero outputs; source truth, attribution and study design (excluded).

— fresh design reviewer, 2026-09-25

## Recheck r2 — 2026-09-25

Verdict: **PASS**

1. Addressed. The MR-7 section, spec R3 and plan R3 now state a direction test with the helium-stage statement. The numbers agree with a self-consistent recomputation from the scratch inputs (PbLi unmet ≈ 197 MW at s = 0.55, ≈ 56 MW at 0.85 with ≈ 54 MW helium unmet, divertor ≈ 149 MW at 0.98). Validation item (c) still says "insufficient/sufficient split triple"; rename to "direction triple", no re-review needed.
2. Addressed. The consumer paragraph names the ledger's two state residuals, `heat_removal_ok`, the heat-duty screens and the pumps, and states that none reads a per-stage channel; terminal differences use the stream's own Cs. This is the author's inspection of files outside my brief; the implementation review should confirm it against the built package.
3. Addressed. Five outputs, 546 → 551, and the calc-type change go into the migration report; exactly-zero outputs are compared absolutely at 1e-12.
4. Addressed. One rule: 0 < s < 1 in both modes, refused otherwise.
5. Addressed. The disclosure sentence goes into the calc def doc comment and the completion docstring; the role table says s stands in for the unmodelled branch hydraulic balance and that 0.85 was informed by the C3 heat proportion, not fitted to an output.

**MR-7: compliant** for the affected scope at design level. Both new quantities are supplied inputs; no UA, flow, rating or bound is derived from demand; a wrong split reports unmet heat and enlarges nothing; hardware roles are unchanged. Executed evidence remains for the implementation review.

— fresh design reviewer, 2026-09-25
