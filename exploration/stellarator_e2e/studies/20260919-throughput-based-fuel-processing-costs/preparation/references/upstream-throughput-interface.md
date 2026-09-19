# Throughput interface for fuel-processing costs

The fuel-processing cost goal is absent at entry; this record supplies its contract. Breeding owns gross production and applicability. WI-069 owns fuel inventory, startup stock and isotope-specific processing rates. This goal installs no equipment price, capital scaling or startup purchase cost.

## Named quantities

All generated output names below begin `stellarator_09__stellaris__fuel_cycle__inventory__`. Native output names and formal units are enumerated in `work/active/WI-069_fuel-inventory-and-startup/evidence/proposed-abi.md`.

| Output suffix | Unit | Meaning and costing use |
|---|---|---|
| `exhaust_kg_s`, `exhaust_kg_day` | kg T/s, kg T/day | Running tritium load at combined exhaust cleanup/isotope-separation inlet, before recovery loss |
| `dt_processor_kg_s`, `dt_processor_kg_day` | kg D+T/s, kg D+T/day | Running hydrogen-isotope mass load at that inlet; equimolar D/T, unequal isotope masses |
| `injection_kg_s`, `dt_injection_kg_s` | kg T/s, kg D+T/s | Running injection-equipment capacity; no unmodeled fueling bypass multiplier |
| `recycle_kg_s` | kg T/s | Usable recovered T leaving combined processor |
| `production_kg_s`, `extracted_kg_s` | kg T/s | Gross bred and usable extracted tritium; neither is PbLi carrier flow |
| `processor_kg`, `feed_kg`, `blanket_kg`, `extraction_kg` | kg T | Nominal held stocks for equipment inventory/containment scope; not throughput |
| `working_kg`, `reserve_kg`, `total_kg` | kg T | Represented minimum working inventory, separate interruption reserve and their sum |
| `startup_minimum_kg` | kg T | Minimum initial external supply for the stated no-decay, constant-power delay model |
| `startup_decay_allowance_kg`, `startup_conservative_kg` | kg T | Conservative decay allowance and initial supply including it; no external-supply availability claim |
| `annual_exhaust_kg`, `calendar_processor_kg_s` | kg T/year, kg T/s | Calendar amount and average; unsuitable substitutes for required running equipment capacity |
| `annual_decay_kg`, `annual_makeup_signed_kg`, `annual_external_shortfall_kg` | kg T/year | Maintained-inventory decay replacement, signed annual balance, and nonnegative net shortfall; not a procurement schedule |
| `defined_flag` | 0 or 1 | Production-dependent physical interpretation is valid only at1; all stock predictions remain conditional on declared process assumptions |

## Boundary conditions

[AGENT] Values are per modeled fusion module; the current stellarator has one. A future multi-module cost calculation must state whether trains and storage are shared before multiplying quantities. No isotope purity, concentration, pressure, equipment design margin, carrier gas, helium-ash processing or PbLi circulation is inferred from these outputs. Such specifications and a reference installed-price basis are needed to turn throughput into equipment cost. Required running capacity follows fusion power and burn fraction; annual availability changes annual amounts only.

[AGENT] Inventory is nominal maintained stock, using source-scenario residence times and explicit reserve policy. Wall retention, coolant permeation, diverted-water detritiation and bypass remain unresolved contributions. `total_kg` means total within the represented boundary, not a qualified complete plant inventory. Undefined breeding keeps finite diagnostic carriers under `defined_flag=0`; cost consumers must not treat those carriers as physical predictions.
