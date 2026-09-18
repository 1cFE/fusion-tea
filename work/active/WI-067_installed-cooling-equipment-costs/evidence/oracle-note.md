# Independent cooling arithmetic oracle

[AGENT] `exploration/stellarator_e2e/oracle_cooling.py` reconstructs the released combined design, primary candidate and source-equation evidence independently. The author did not read the new production calculator or manual implementation. The shared `equipment-interface.json` supplies vocabulary, defaults and output types only, embedded as constants for standalone verification. The oracle imports no production code and does not read the interface at runtime. No excluded demo, ARIES holdout or derivative was read.

The derivation uses annular volumes for pipes/tubes, cylindrical and spherical shell differences for exchanger metal, geometric internal volumes for inventory, ideal-gas conversion for helium standard volume, the original BNL pressure/power expression, and the original Seider pump/motor expressions. The source IHX effective conductance is reconstructed from 267.8 MW, source geometry and the 35/19.3 K terminal differences. Monetary quantities retain the source-year CPI ratios; 2021 uses the corrected rounded 271.0 index. Plant price incompleteness and physical qualification do not disappear because the arithmetic agrees.

Lifecycle verification explicitly enumerates purchases strictly before the operating horizon and discounts each event. Its annualization uses `expm1` and `log1p` for numerical stability at tiny positive discount rates, with an exact zero-rate branch. This is independent of a closed geometric-series implementation. Machine removal repeats the assembly allowance as the released scenario; bundle removal repeats only the 2.4% labor line. First-design engineering and initial spares never recur.

Dormant mode returns zero for every numeric output and false for every Boolean before inspecting active operands. Active mode requires one module, integer positive circuits, finite operands, valid geometry, positive thermal approaches and usable efficiencies. Failed meaningful engineering/source screens remain calculated outputs. Constant false qualification outputs mean unestablished qualification; they are not arithmetic failures.

Interface conventions: exchanger masses, duty and installed/required areas are per exchanger. Circuit count is separate. Pipe and inventory geometry are plant totals. Inventory-volume outputs report wetted geometry before reserve; inventory mass and helium standard purchased volume include reserve. Reserve purchases do not invent additional filled geometry. Salt flow is per circuit, salt-pump flow/shaft power are per machine, and salt electric/shaft totals are plant quantities.

## Focused selfchecks

Executed with `.codex-test/run python` on 2026-09-18. Original Seider example with source-fitted efficiencies reconstructs 23,623.710845 USD2006 per pump and 16,204.414109 USD2006 per motor, within 0.02 USD of the image-checked source-method report. This check is separate from the selected fixed-efficiency 0.75/0.95 scenario.

The BNL original alternative reconstructs 298,621 USD1978 from 550,000 × [0.5 + 0.5 × (50/735) × (115/50)^0.28], consistent with the rounded 300,000 source table. Pressure is absolute; the source denominator is the 50 hp pumping duty. See `round2/circulator-transfer.md` for the original table/section locators and distinction from the 140 hp motor rating.

[AGENT] The coordinator clarified the target-duty transfer to use primary fluid/shaft work per machine for the BNL pumping-duty term. The released candidate used electrical duty at the retained unity drive efficiency; both agree there. The explicit shaft mapping avoids treating external drive losses as additional compression duty. This remains an unvalidated source-to-target transfer. A nonunity-drive selfcheck raises electric demand by dividing by 0.9 at fixed shaft work: reported machine electric power rises and BNL package cost remains unchanged.

Exact zero-rate checks give two 10-year purchases and one 15-year purchase in a 30-year horizon; life equal to horizon gives no purchase. Zero, 1e-12 and 0.07 discount cases remain finite. The seven installed subaccounts sum to total purchase plus installation. Salt shaft power equals electric demand times motor efficiency. Disabled evaluation with NaN circuit count returns finite zero values. Active fractional circuits, two modules, nonpositive thermal approach and NaN heat fail explicitly.

Layout multiplier 2 doubles pipe geometry and modifies pressure-loss diagnostics without changing the retained primary hydraulic input. Price choice 1, 14 circuits, cost scale zero, and machine/bundle lives equal to the horizon all return finite results. Zero cost scale sets all actual cost totals and annual costs to zero while raw historical source prices remain reported.

These are focused reconstruction and identity checks, not an independent source applicability assessment or the integrated generated/manual/oracle comparison. The parent verification run supplies that latter evidence.

## Evidence read

- `work/active/WI-067_installed-cooling-equipment-costs/combined-design.md` and `primary-candidate.md`.
- `work/orchestration/goals/installed-cooling-equipment-costs/evidence/round2/primary_hardware_estimate.py`, `reference_sizing.py` and `reference-sizing.json`.
- `work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md`.
- The interface JSON and required repository instructions/context. No new model or production/manual calculator implementation was used as derivation evidence.
