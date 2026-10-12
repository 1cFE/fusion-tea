# Adapter v1 design

Status: independent semantic review required before implementation. All choices below are [AGENT].

## Selection and roles

`v1/mapping.json` will enumerate six retained historical quantities and two current magnet controls. Each row has exact current input, physical definition identifier and prose, unit, conversion information, role, missing policy and incompatible policy. Requests must carry the exact definition identifier, unit, a nonempty source label, matched resolution and finite scalar value. No numerical unit conversion or physical interpretation occurs inside the adapter. The eight entries are a preparation proposal; the original seven-input reference intent and criteria remain historical authority.

Retained inputs are major radius [m], minor radius [m], peak electron density [m^-3], peak ion temperature [keV], radial coil exterior allocation [m], and full transverse clear cavity [m]. The two current controls are supplied installed continuous reference turns [1] and per-turn operating current [A]. Ampere-turns are the calculated product. A supplied product never selects either factor. Field remains calculated. Winding side, conductor fractions, support/casing masses, facility layout, processing capacity, equipment ratings/conditions, procurement classes and purchase prices remain the selected package defaults unless a future reviewed mapping adds them. All 704 effective inputs are retained and labeled supplied or held.

Unlike the old selected-forward scenario, the preparation baseline is the current package default design. The old sizing/inventory overrides are retired. The old profile exponents are not silently reapplied: current defaults remain held and their values are recorded. This baseline change is disclosed; it makes no reference-comparison equivalence claim.

## Native execution and criteria

Use `exploration.stellarator_e2e.studies.study_route.run_points` with every numeric contract output requested and exact predicate inventory checked. Preserve native failed cases and database. Verify the package's sealed identity on the supported route. Pin the model contract, package contract, source-model digest, adapter/mapping and unchanged historical comparison manifest/accounting documents in a new identity ledger. Refuse identity drift. Runtime identity comes from the supported route and environment receipt.

Keep a byte-identical copy of the historical manifest and record its origin digest. Its acceptance bands, account definitions and monetary conventions remain unchanged. Export its existing producers from current native outputs, with explicit missing/inactive status. A quantity computed from supplied controls gets no independent prediction credit. No observations are loaded and no pass grade is issued. Historical engineering predicate inventory is not the current inventory: all 67 current predicates remain separately recorded. Supplied purchase-cost accounts now describe the selected offer; preserved ratios and arithmetic do not imply demand-sizing or physical qualification. Account parents and children remain alternative views; the formal pump row stays calculated primary compressor demand, not total pumping. Mixed-year money, C220107 and unresolved scope remain limitations.

## Custody

The preparation store is separate from the historical reveal register. Create an exclusive attempt directory, then atomically create `first-attempt.json` with the attempt name before reading the request. The first pointer is never overwritten. Later attempts carry its identity. Save raw request bytes before parsing. Save a terminal result exclusively, or leave the first attempt visibly incomplete on interruption. Raw exceptions and native stores stay in the attempt. Do not label a later successful execution as a corrected first result. This is the versioned custody correction: first-attempt identity covers refusal and incompletion, whereas historical report completion was insufficient for that obligation. No historical custody records are edited.

## Validation and review boundary

Use native current-default synthetic success, a partial synthetic selection showing held fallbacks, rejected average-density definition, rejected historical ampere-turn input, and a low-current conductor-domain failure. Check defaults/overrides retain hardware, ratings and prices. Test duplicate paths and failed-first-then-success identity. Unit tests cover malformed requests and custody; actual native execution proves the route. Review the semantics before code and inspect the completed adapter independently afterward.

## Open scientific decisions

A future reference adapter requires a decision about how reference ampere-turns relate to independently documented installed turns and operating current. Neither choosing default turns nor choosing default current resolves that question. Reference definitions for density/temperature profiles, shape/radius, local winding cavity and installed offers may also be incompatible or absent. Held default choices are visible scenario assumptions. The preparation mapping grants no permission to infer these quantities from reference outputs.
