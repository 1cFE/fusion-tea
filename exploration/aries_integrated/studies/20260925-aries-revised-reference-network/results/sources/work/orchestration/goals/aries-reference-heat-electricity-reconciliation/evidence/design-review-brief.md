# Design review brief — WI-092 network heat-driven closure (fresh reviewer)

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 12 tool calls and a 500-word return, written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/design-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks, goal trails or any other work item.

## Exact question

Is the proposed additive closure in `work/active/WI-092_aries-parallel-exchanger-network/design.md` (with `spec.md`, `plan.md`) correct in its equations, honest in its MR-7 variable roles, and safe for the existing consumers, so that implementation may proceed?

## Entry files

1. `work/active/WI-092_aries-parallel-exchanger-network/spec.md`, `design.md`, `plan.md` — the proposal.
2. `exploration/aries_integrated/native_completions/heat_driven_closure_impl.py` — the reviewed series closure whose equations mode 0 copies.
3. `models/designs/aries_cs_integrated/plant.sysml` lines 244–420 — the `heat_exchangers`, `turbine`, `recuperator`, `precooler` and `generator_auxiliaries` parts (consumers of the closure outputs).
4. `modeling_project/REQUIREMENTS.md` — only the section headed "MR-7" (search for it).
5. `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p736.png` — the published network (Fig. 12); view once.
6. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/parallel-network-scratch.py` and `.txt` — a first-principles scratch check of the network (not model code).

## Expected checks

- **Equations:** stage formulas, the mode-1 network (helium stage on the whole flow, PbLi and divertor stages on the split flows from the helium-stage outlet, adiabatic mixing), the identity `Tt = Tmix` at the root, the monotonicity argument and bracket validity for mode 1, domain of the split.
- **Fidelity to Fig. 12:** does the design represent the drawn arrangement, and does it state what it does not represent (branch pressure loss, mixing loss, control law)?
- **MR-7:** is `pbli_split_fraction` an operating choice rather than a sizing rule? Does any calculation now derive an installed capacity or a design quantity from demand? Are the insufficient/sufficient tests (split 0.55 / 0.85 / 0.98 at fixed hardware) the right kind of evidence? Return **MR-7 compliant / violated / unverified** for the affected scope.
- **Consumers and migration:** do the turbine, recuperator, precooler and ledger keep meaning under mode 1 (the ledger's turbine/recuperator state residuals; the definition of `heater_inlet`)? Is the mode-0 exactness plan sufficient to claim the original failing case is retained? Are the two new public keys and their defaults the only interface change?
- **Disclosure:** the design copies the reviewed equations into mode 0 and keeps the old definition unbound; is that disclosed plainly?

## Exclusions

Do not evaluate the sources' scientific truth, the goal's attribution, or the study design. Do not run anything.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; numbered findings (each: what the design says, what is wrong or missing, severity blocking / correct-before-implementation / note); the MR-7 statement; one paragraph on what the review did not cover. Sign as "fresh design reviewer, 2026-09-25".
