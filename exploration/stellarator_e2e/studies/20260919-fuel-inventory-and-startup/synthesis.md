# Executor synthesis

Prepared by the study executor from this record for coordinator commit. This is not an independent reading or final rubric grade. Native evidence: [points](results/points.csv), [verification](results/oracle-all-points.json) and [source/assumption account](report.md).

The reference calculation represents 4.418 kg of tritium, of which 2.038 kg is the declared interruption reserve. It needs 4.400 kg conservative initial supply under the specified immediate-full-power, delayed-return startup approximation. The processor must handle 7.743 kg T/day, irrespective of later calendar downtime.

The selected cases expose the important dependencies. Lower burn fraction increases circulating flow, processing stock and reserve demand. Shorter return times reduce startup draw and stock. Reserve policy can dominate total held fuel. Longer deficient commissioning increases initial supply without changing the ongoing makeup requirement. All calendar cases keep running capacity and maintained-stock decay distinct from annual productive demand.

All 26 cases are retained. The 23,556 mapped scalar comparisons and 650 independently derived predicate comparisons pass; all 70 new inventory outputs are mapped. The map covers 892 numeric outputs and 14 Boolean flags; 22 inherited numeric outputs remain native evidence only. No case satisfies every whole-plant predicate. These facts support a verified conditional inventory/startup/throughput calculation, not full self-sufficiency or a qualified plant.

The four findings in record §15 preserve the missing physical equipment/reliability/supply relationships, the startup-versus-stock distinction, the running-versus-calendar capacity distinction and failed whole-plant screens. Residence and reserve scenarios are sensitivity inputs, not optimization freedoms or confidence limits. Actual tritium supply, reactor-specific residence performance, wall retention, permeation and complete process costs remain unresolved.

The record includes the sealed producer package and exact route/helper/tool sources. `execution/reproduce.py --out /tmp/fuel-study-reproduction` replays the copied package into a new directory with the recorded external Python/teax environment. That script is provided for reproducibility; a separate cold reproduction has not been claimed by this executor.
