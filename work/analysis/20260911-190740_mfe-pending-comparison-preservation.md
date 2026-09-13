# Pending plant-closure comparison: preservation decision

## Scope and authority

[AGENT] Read-only companion to T-015's native F04 assessment. This report identifies the pending comparison affected by an operating-heating correction and presents owner choices. It does not amend either goal or authorize shared MFE changes. The owner-reserved decision is in `work/orchestration/goals/fusion-audit-remediation/goal.md`, Reserved gates: how to preserve, finish or supersede the pending plant-closure comparison before shared changes invalidate its current-artifact assumptions.

## Current evidence

The plant-closure trail ends with T-007 COMPLETE and has no T-008 start or round result. Its integration evidence is committed at `9dd59883c44a0b29d1f905e87e84a424b086ce55`, under `work/orchestration/goals/plant-closure/evidence/T-007_pin/`. The native return records candidate pin `e2b0fe3979af1c75a92d8b58f310e0f07f6059af3f3236f4a812bf2227baa7d9`, semantic fingerprint `42237b2b07673bfde916b9749bab93634eafa91f1205abde4b7a70dd1881038f`, executable fingerprint `234d0b27d2b5327ede2cae1c05a2e1c1ead1d89337fd019782bdda03d841e81d`, and TEAx revision `8d877460ac4f6f264561d916e40c1708adb13397`. The recorded baseline LCOE is 224.60952472804465, with fourteen verdicts and `divertor_heat_ok` violated. These are producer-reported historical results, not a new integration certification.

Read-only `git diff a9ec0b76 --name-only -- models/designs/generic_mfe models/designs/stellarator_09 exploration/stellarator_e2e work/orchestration/goals/plant-closure` returns no paths at assessment time. The stellarator generated package's last modifying commit is `d235dde40bb459d80a35378823981e4a6e573915`. The model/package and prior evidence remain recoverable by their committed revisions, subject to the external pinned runtime and native reproduction checks. Git retention alone is not a fresh executability certificate.

## Why an operating-heating correction changes this comparison

The installed-heating basis is explicit in `work/orchestration/goals/plant-closure/evidence/round1_basis_packet.md:52`, its first amendment at line 108, and the trail's T-001 decision. It holds the thermal sum and divertor ledger to installed coupled heating for that round's compatibility bridge; moving to operating heating is a named follow-on. This is an inherited agent-originated execution decision, not evidence that installed capacity is the correct sustained operating demand.

The pending goal requires a single-pin study with exact held-value compatibility, single-closure attribution, inherited-window feasibility counts, and engineering-lever scenarios (`plant-closure/goal.md`, Answered when (b), Invariants). Its reserved attribution bridge rejects treating an old-package rerun as the internal compatibility arm. A different heating state cannot silently replace the current operand and retain those claims.

| Affected path | Current artifact | Consequence for a correction |
|---|---|---|
| Reactor source heat and primary loop | `models/designs/generic_mfe/mfe_plant.sysml:524` | Operating heating changes source heat and therefore flow, pump draw and recovered heat. Holding the old pump result would omit an existing response. |
| Electrical balance and downstream price | `models/designs/generic_mfe/mfe_plant.sysml:559` | Coupled input and wall-plug draw must describe the same operating state. Net power, related fences, power-scaled costs and LCOE can move. |
| Divertor heat and fence | `models/designs/generic_mfe/mfe_plant.sysml:1056` | The ledger explicitly uses installed coupled heating. Changing only electrical accounting would leave its physical state inconsistent. |
| Installed heating procurement | `models/designs/generic_mfe/mfe_plant.sysml:681` | Installed delivered capacity supplies the ECRH cost operand. A correction must retain reserve-capacity procurement rather than price only operating demand. Other heating technologies and missing part-load/access relations remain separate scope questions. |

## Concrete owner choices

| Choice | What happens to the pending comparison | Cost and benefit |
|---|---|---|
| Supersede the unfinished comparison after retaining its evidence (recommended) | Record an owner ruling in the appropriate native goal trail; close/review its interrupted round honestly without a study or answered-goal claim. Retain its pin, audits and historical results. Author a revised comparison after an audited operating-state repair and a new native integration candidate, under a later reviewed strategy. | Avoids spending the next study on a known operating-state inconsistency. Loses immediate completion of the original three-closure attribution promise; the replacement must explicitly restate any retained compatibility and attribution requirements. No second pin is inserted into the existing round. |
| Finish the existing comparison first | Keep shared MFE artifacts unchanged; resume the pending plant-closure study at its current pin and declared installed-heating basis, including its limitations. Review that round before beginning an operating-state correction. | Preserves the original attribution experiment and its exact compatibility requirement. Delays F04 repair and produces a study whose operating-heating interpretation remains defective. |

[AGENT] Recommend superseding the unfinished comparison while retaining all historical evidence. The owner's active request is audit remediation, and no pending study has started. This recommendation does not accept F04 as a residual, redefine the financial basis, close plant-closure as successful or authorize a replacement comparison's details. Those changes require the owner's ruling and normal native scope/review steps.

## Limits

This report assesses recorded obligations and current bindings. T-015's separate numerical assessment supplies the live counterexample and its interpretation. No pending goal, source, shared model, package, manifest, census, historical study or integration evidence was changed. No candidate was promoted and no study was executed here.

## Numerical companion

The T-015 executed counterexample is retained in `20260911-190758_mfe-operating-state-evidence/results.json`. At the unchanged plasma point, raising installed wall-plug capacity from 100 to 120 MW leaves the 49.07960078792678 MW sustainment requirement unchanged, lowers net generation by 17.029497549 MW and changes the executed LCOE from 224.609524728 to 229.541287969. Procurement also increases, as expected for greater installed capacity. This distinguishes the legitimate capacity-cost effect from the spurious continuous operating load. Both cases still violate the divertor fence. The separate held-efficiency operating-demand substitution is an algebraic diagnostic, not an executed corrected model or corrected LCOE.
