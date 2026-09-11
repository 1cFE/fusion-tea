# Package annex — `ife_tea`

Package facts for the native study runbook. WI-048's operating-point audit and WI-049's discount-limit audit supply the model authority: `work/analysis/20260911-045617_audit_WI-048_ife-operating-point-repair-r1.md` and `work/analysis/20260911-145626_audit_WI-049_ife-zero-discount-repair-r1.md`. Metadata preparation supplies a candidate, not a committed study.

## § Declared ties

No external ties. WI-048 binds beam energy, driver efficiency and repetition rate structurally into the bank-energy, operating-power and price paths. WI-049 evaluates the existing discount factors stably, including exact zero, and binds Real plant durations into both factors and annual costs. `axes.json` names the single qualified discount-rate entry key proposed for this round. A study declares its framing, windows and held inputs after reading native indicators.

## § Baseline pin

`manifest.json` carries the executed baseline, headline, two expected verdicts and native fingerprints. All thirty-two numerical channels appear in its objective catalog to require independent verification coverage, including both discount factors; these are observables, not thirty-two optimization objectives. `study_route.execute_baseline` deposits the sealed identity and stored baseline evidence through stock TEAx with strict package loading. Stores and loader aliases live in the caller's output directory.

The Hawker interpretation remains mixed-basis $/MWh. The Meier interpretation remains 1988 cents/kWh. Neither is normalized against the other. Historical Osiris source facts, retained later assumptions and executable outputs are distinguished in the audited model. This package does not claim that its computed baseline reproduces every historical Osiris table number.

Regenerate package-owned metadata with `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.ife_e2e.studies.prepare_metadata --work-dir /tmp/ife-metadata'`. It independently checks executed baseline outputs, captures the native instance snapshot and derives the census. The integration seam subsequently proves that regeneration and recapture move no package or snapshot bytes.

## § Oracle

`oracle_entry.py` exposes `evaluate(point)` and `operand_bindings()`, imported as `exploration.ife_e2e.studies.oracle_entry` with repository-root `sys_path`. Its arithmetic dependency is the WI-049-audited `tests/ife_oracle.py`, which computes source power identities, explicit annual discounted cash flows and both factors independently of generated arithmetic. Immutable study records must capture both files. Explicit bindings connect the net predicate to independently computed net power and the heuristic to efficiency, gain and threshold inputs.

The adapter refuses unknown qualified keys, nonfinite inputs and nonpositive or fractional construction/operation years. Current duration keys are `hif_plant_pkg__hif_plant__construction_duration` and `hif_plant_pkg__hif_plant__operational_duration`; retired `lcoe_calc` duration keys are rejected. Integral years are a limit of this annual-cash-flow oracle, not an added model constraint. Other arithmetic domain errors propagate. Oracle agreement establishes the audited arithmetic and bindings within this scope; it does not establish engineering completeness or normalize cost conventions.

## § Validity masks

Both named predicates are retained in stored evidence. `net_positive` checks strictly positive computed net generation. `viability` checks the historical efficiency-times-gain heuristic; it is insufficient to establish positive net power by itself. No epsilon changes the strict net comparison.

Non-generating cases remain in the store with zero price sentinels and generating flags of zero. `study_route.eligible_prices` applies the audited consumer rule separately to both price paths: generating flag one, named net verdict satisfied, finite positive price. A zero sentinel is never an eligible generating price. Any broader study feasibility mask must state its policy and retain both verdicts.
