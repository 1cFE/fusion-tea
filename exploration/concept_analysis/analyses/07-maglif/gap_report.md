Here is the gap assessment, written to `analyses/07-maglif/gap_report.md`. Key findings:

---

## Overall Readiness: **Mostly Ready**

The most important correction to the prior draft: SAND2006-7148 is **already substantially extracted** (277 KB) and contains real LCOE data — COE estimates of **7–20 ¢/kWh** depending on configuration, driver capital of **$372M/1 PW LTD**, thermal efficiency **42–50%**, and capacity factor **85%**. These are now in the Available Parameters table and the "blocking" flags for those items have been removed.

### What's available for each section:

| Section | Coverage | Key assets |
|---------|----------|-----------|
| Data availability | Moderate | arXiv:2408.15206 (physics/IMGs), Pacific Fusion interview (DS specs), Fuse Not Boring (TITAN/Z STAR), SAND2006-7148 (full plant study) |
| System function challenges | Partial | Energy partitioning, pulsed-system logistics, coupling efficiency, IMG vs. legacy architecture |
| Subsystem TRL | Partial | IMGs (TRL 4-5), target physics (TRL 3-4), FLiBe blanket (TRL 2-3), RTL automation (TRL 2) |
| Materials/supply chain | Partial | FLiBe/Li-6, capacitor bottleneck (arXiv explicitly calls this out), liner simplicity |
| LCOE parameters | Partial | Full SAND2006-7148 cost model available; missing commercial rep rate, yield, and coupling efficiency |

### Remaining blocking gaps for the LCOE model:
1. **Commercial rep rate** — 0.1 vs. 1 Hz swings COE by ~3× (both bounded by available data)
2. **IMG driver capital cost** — derivable from LTD baseline with arXiv's stated 5× reduction factor
3. **Commercial coupling efficiency** — demo is ~10%; commercial target unknown but constrains effective Q

The Z-IFE SAND2006-7148 study provides the structural template; the analysis just needs explicit stated assumptions for translating from LTD to IMG architecture.

## Structured summary (machine-readable)

```yaml
overall_rating: "Mostly Ready"
blocking_count: 3
important_count: 0
counting_method: "manual_prose_count"
section_coverage:
  availability_of_data:       "Unknown"
  system_function:            "Unknown"
  subsystem_maturity:         "Unknown"
  materials_supply_chain:     "Unknown"
  lcoe_parameter_extraction:  "Unknown"
```
