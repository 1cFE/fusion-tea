# Current supplied-equipment interface

[AGENT] The Round 2 interface has 704 public inputs. It adds 118 inputs and retires eleven from the accepted 597-input Round 1 package. The exact membership, producer outputs and asserted predicates are in `interface-delta.json`. Historical packages and their recorded interfaces remain unchanged.

The new inputs comprise 49 physical ratings or offered operating conditions, 27 purchase amounts or procurement classes, forty generated Boolean administrative flags, and two single-module calculation formals. The electric-plant gross rating is owned by the physical specification and also supplies its matching price equation. The forty flags can only remove capability credit; they do not replace calculated applicability or support. Single-module formals reject another module count.

## Selecting and evaluating a design

A selected equipment offer includes its rated dimensions, declared operating conditions and purchase amount. The default purchase amounts are assumed estimates captured from the entering model, not vendor quotations. A replacement offer must supply its own specification and price. Changing a rating alone while retaining a price represents a hypothetical offer; the evaluator does not infer a price law for that upgrade.

Operation determines required flow, work, exchanger conductance, heat rejection and electrical demand. Those demands propagate to downstream components. Thirty-two new scalar capability assertions and the now-asserted existing exchanger-area check compare the resulting requirements with independently supplied capability. Raw capacity margins are rating minus demand, and equality passes. No spare margin is silently added. Undefined or unsupported checks expose a zero definedness flag and fail the assertion; their zero numeric carriers are not evidence of adequacy.

Five equipment groups also compare actual operating conditions with the conditions of the supplied offer. The hard-coded eight-ULP identity rule admits only floating-point representation differences. It is not a temperature, pressure or performance envelope. Missing off-design machine maps and equipment qualification remain missing.

## Retired inputs and current consumers

The eleven retired keys are the turbine and heat-rejection demand-price coefficients, the old cryogenic base and power-law facts, and the old divertor/power-supply bases and power-law facts. A previous per-MW coefficient or power-law base is not interchangeable with a purchase amount. Current proposals must select the new amounts explicitly or use the documented default assumed offer. The oracle rejects retired keys; native public schemas no longer declare them. Exact names are recorded in WI-079's `interface-migration.json`.

Material/geometry cost hybrids and grouped allowances retain their inherited formulas with independently selected procurement classes. Reachable legacy building, land, coolant and fuel-handling modes use the same separation. Staffing uses a selected reference class. Actual operating fuel, energy, maintenance frequency and LCOE remain responsive to operation.

Current regression consumers compose this explicit migration with the earlier migration in memory. Only the documented cost descendants receive current-equation comparisons. Historical evidence files are unchanged; unaffected physical channels retain their original comparisons. Every current numeric output and asserted predicate remains independently checked.
