# Executor synthesis

[AGENT] Written by the study executor after record commit `8e6fb2f2`. This is an executor reading of that committed record, not an independent review. All evidence cited below is inside the frozen study directory. Formal goal closure remains the owner's decision, as stated in the [captured brief](results/sources/work/orchestration/goals/aries-integrated-heat-electricity/evidence/owner-brief.md).

**The positive conditional integration objective is achieved.** One native configuration connects supplied plasma profiles through fuel demand, deposited heat, fixed coolant/exchanger equipment, cycle work and auxiliaries to net electricity. The calculated nominal produces **423.106794 MW net**, accepts **2240.389047 MW heat**, has zero unmet duty and satisfies all ten scalar predicates. These are executed graph outputs under declared assumptions. They do not establish published ARIES performance or scientific qualification. [Record §§3–4](record.md), [exact cases](results/cases.json).

The study also demonstrates the required behavior away from nominal. Density changes alter fuel demand, three branch duties, turbine state/work and fuel-variable electricity while all 121 other public inputs remain unchanged. Net output becomes **140.230696 MW** and **735.759323 MW**. Lower supplied fuel and helium ratings fail their own capacity checks without changing physical demand. Lower helium exchanger conductance leaves **47.118607 MW** unmet heat. These results distinguish demand, operating state and chosen equipment. [Input and propagation evidence](results/propagation-and-input-preservation.json), [record §6](record.md).

The adverse source cases remain material. Source-conditioned nominal and literal Lyon leave **158.725848 MW** and **398.908524 MW** unmet heat. Literal Raffray leaves **502.134202 MW** unmet heat and a **182.03 MW** source-energy discrepancy. Positive computed export in these cases does not make them thermally adequate. Their distinct source meanings must remain attached to any comparison. [Record §§3–6](record.md).

All fourteen cases completed; eight satisfy all ten predicates and six retain violations. Verification covered every case across five verdict combinations: **420 scalar comparisons and 140 exact predicate comparisons passed**. Numerical coverage is thirty of 211 stored channels. The residual-only **1e-7 MW** absolute allowance is explicit; other channels keep the relative **1e-9** rule and verdict agreement remains exact. Scientific limits include profiles, reaction data, deposition transport, assumed equipment, hydraulics, magnets, breeding, materials and machine maps. No cost or LCOE result is supplied. [Verification](results/verification_summary.json), [record §§13 and 17](record.md).

I recommend retaining the eight recorded dispositions:

| Finding | Recommended disposition |
|---|---|
| #1 — repeated local predicate names | Keep the limited baseline gate and retain/check every full constraint ID. |
| #2 — near-zero residual parity | Keep the reviewed, explicit residual allowance and original refusal evidence. |
| #3 — connected calculated nominal | Accept the conditional integrated result with its supplied-profile and equipment assumptions. |
| #4 — inadequate source reconstructions | Preserve adverse cases and source labels; reconcile source boundaries and thermal assumptions before stronger claims. |
| #5 — upstream propagation | Accept the fixed-equipment response evidence with its approximation limits. |
| #6 — independently offered ratings | Retain insufficient/sufficient pairs without inferring sizing or equipment qualification. |
| #7 — conversion sensitivities | Retain bounded ratio/conductance findings without an optimum or general monotonicity claim. |
| #8 — missing producer revision label | Preserve the original summary and use the separately evidenced runtime identity. |

The full finding identities and homes are in [record §15](record.md). The [snapshot](snapshot.json) identifies the sole study executable, complete inputs, store and artifact digests. [Replay instructions](replay.md) use fresh outputs and preserve this record. Further inventory/cost work can build on this integrated assembly; source reconciliation and scientific qualification remain separate work.
