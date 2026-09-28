# WI-073 native physical structure review

[AGENT; independent non-author `/root/cycle_physical_critic`; 2026-09-19] **PASS after structural corrections, for the inspected canonical representation and scalar wiring only.** This does not certify generated numerical execution, the complete input census, conservation tests, property support at runtime, integration, depth grading or adoption. The coordinator authored all corrections; the reviewer changed no model.

## Findings resolved during review

- HP total flow originally connected directly to both downstream paths. The explicit `extraction_splitter` now separates full HP flow into reheat and bleed branches, retaining common HP pressure/enthalpy. Reheater/LP/condenser/condensate-pump aliases use unextracted flow; boiler/HP/feed-pump aliases use full flow. The heater consumes condensate plus bleed and exposes the reviewed mass/energy residuals.
- Salt branches originally lacked a visible distribution connection. The explicit `salt_distributor` now connects the assembly coolant boundary to parallel SG/reheater branches. Paired thermal ports represent both hot splitting and equal-temperature return joining. Total and branch flows bind to solver outputs. Celsius state attributes are distinguished from the existing port's Kelvin convention; pressure loss remains outside this calculation.
- Component temperature/entropy properties were initially absent. Supported inlet/outlet aliases now reference solved states. Condensate-pump outlet and the heater's pumped-condensate inlet intentionally have no unsupported temperature/entropy. Reheater pressure aliases its solved pressure instead of introducing an unused independent assumption.
- Heat and shaft exchanges now have distinct thermal/mechanical item types. Condenser and conversion-loss connections join at one total-rejection boundary; only that boundary connects to heat rejection. Electrical assembly boundaries delegate to pump leaves, avoiding duplicate external supply connections. Generator output connects to the existing gross boundary.

## Checked ownership and remaining verification

The matched calculation receives existing heat-transport heat, salt temperatures, heat capacity, per-circuit flow and `ihx_count` aliases. It does not use installed pump count as active circuit count. Component-owned pressures, temperatures and efficiencies feed the intended calculation inputs. Component results alias solver outputs and do not create solver feedback. The old fit argument remains connected to the old equipment diagnostic; selected gross efficiency uses the separate mode calculation.

Power balance adds cycle-pump and cooling-water electricity once while preserving the existing subsystem allowance formula. Heat rejection receives the cycle's total pre-cooling rejection and a one-hop solved condenser-temperature alias. CAS25 retains thermal input as its price driver. No additional component price or installed-capacity claim is introduced.

Ports remain declarative under this repository's documented convention; they do not execute conservation equations or bind every item attribute numerically. The scalar aliases carry the calculated states/work. Native output and entry-point checks must therefore establish that these aliases resolve as intended, that no result becomes an independent input, and that the actual generated dependency graph is acyclic.

The constraint encoding `enabled <= 0 or gap > 0` is accepted only over the solver-enforced exact mode domain `{0,1}`. Negative, fractional, NaN and infinite modes must refuse before predicate reporting. Tests remain required; the physical gap stays strictly positive.

The clarified `water_pump_rise_K` equals specific pump electricity divided by mean liquid heat capacity over the selected span. This is the original prototype's apparent-rise diagnostic, not an exact new pump-outlet state. It stays within the existing scientific release.

## Reviewed byte identities

These hashes identify the inspected files, not a generated-package certificate.

| File | SHA256 |
| --- | --- |
| `models/library/structure/mfe_steam_cycle_components.sysml` | `4b85df78da5006526586ce8ede958cde0c6ec93a689e48cab5e7087d2415c7eb` |
| `models/library/structure/mfe_interfaces.sysml` | `a785da709eb579de4439588cbc74b27a5971bcc01604a16d379155f584daaecb` |
| `models/library/analyses/mfe_matched_steam_cycle.sysml` | `1d15aff5eb82202c9d62ee8bccf378ee864e112d8cd4cfa963ca70602552baa9` |
| `models/library/analyses/mfe_power_balance.sysml` | `692dc6784c1dcfee8c5533ce5c5beace11c80491a35894e4238518c231452713` |
| `models/library/structure/mfe_plant_systems.sysml` | `cac594f5d82cb9c23295ef36241f74073ad069f14aa93195b111c0a10dddc3f8` |
| `models/designs/generic_mfe/mfe_subsystems.sysml` | `e823bc16e0b93128428d6bfde831e4b20aa6a8786de2cb3da093151bfb9a8151` |
| `models/designs/generic_mfe/mfe_plant.sysml` | `f8086cd465c549d4ddc31f496327b0e3b362b417e65c3641ab6cda55653230f1` |
| `models/designs/stellarator_09/stellarator_plant.sysml` | `942edb2c8185a7b1b0f8a34187c0add2a93a57f028ac7259e2126563e47a468e` |
| `work/active/WI-073_matched-steam-cycle-for-current-comparison/interface-inventory.md` | `edec6c9e8d19bc96beb6251cded8f5db7815eee40e3408102bcf49903507ad6a` |
