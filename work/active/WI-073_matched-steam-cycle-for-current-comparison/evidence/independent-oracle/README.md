# Independent original-table numerical reference

[AGENT; numerical author, 2026-09-19] This directory supplies independently authored calculations for WI-073. It is authorship, not independent review of itself. The reference imports only Python's standard library and reads the three original NIST HTML tables. No author prototype, author checker, production solver, canonical table or generated package was read or imported to create it. The required design/interface and narrative proposal/physical-review summaries were read before implementation, including their reported baseline values. Thus the implementation is independent, but the author was not blind to the prior reported results. Original property-source dependence is shared and explicit.

The reference calculates all 71 numeric and seven Boolean matched-cycle outputs, all nine numeric and four Boolean conditional cooling-water outputs, and the three cycle-selection outputs in the interface inventory. The later native verification described below covers all mapped outputs and predicates. This author evidence is not a final model audit, source-custody review or integration/adoption decision.

## Reproduction and records

Run these commands from the repository root:

```bash
.codex-test/run python work/active/WI-073_matched-steam-cycle-for-current-comparison/evidence/independent-oracle/reference.py
.codex-test/run python work/active/WI-073_matched-steam-cycle-for-current-comparison/evidence/independent-oracle/check_reference.py
```

- `original-tables.json` retains independently parsed property rows, including separate saturation endpoints and original phase labels.
- `source-receipts.json` records original paths, SHA256 hashes, counts, endpoint anchors and maximum thermodynamic identity residuals.
- `reference-results.json` records baseline, 40/50°C condensation and 435°C main/reheat calculations.
- `resolution-sensitivity.json` records the signed change in every numeric cycle output when retaining alternating source rows separately by phase, always preserving endpoints.
- `reference-checks.json` records author checks, local liquid-pump comparisons, exact source transcription and explicit refusal cases.

## Original property basis

All three captures use water, NIST's default reference state, temperature in °C, pressure in MPa, specific volume in m³/kg and enthalpy/internal energy in kJ/kg. The entropy header is J/(g K), numerically identical to kJ/(kg K). The isobar grids support exactly 6.2 and 0.8 MPa; they do not support pressure interpolation. Both isobar tables explicitly contain saturated liquid and vapor at the same temperature. The condenser table is the corrected temperature-increment saturation query, not the previously captured pressure-increment query.

The 6.2 MPa capture contains 571 rows over 171–455°C, with saturation at 277.73289°C. The 0.8 MPa capture contains 603 rows over 42–455°C, with saturation at 170.40649°C. Its actual ordinary increment is about 0.688333°C despite a requested 0.5°C increment. The corrected saturation capture contains 162 rows: liquid and vapor at 81 temperatures from 20 to 60°C, every 0.5°C. The reference uses the captured rows rather than inferred query spacing.

An independent regular-expression extraction agrees with the HTML parser on all 1,336 rows and their first seven numeric fields. For every row, `h-u=1000*p*v` lies within the maximum rounding interval implied by the displayed last digits of h, u, p and v. The worst residual consumes 91.87% of that bound. This verifies displayed-source consistency, not uncertainty in the underlying equation of state.

Interpolation is piecewise linear. Pressure-held entropy inversion locates the adjacent entropy rows; enthalpy inversion locates adjacent enthalpy rows. Across the saturation interval, the two endpoint enthalpy/entropy values define the two-phase mixture and constant temperature. Interpolation within a single phase never borrows the opposite phase's temperature interval. The ordinary forward-temperature/inverse-enthalpy midpoint checks reconstruct temperature within 1.28e-13°C across all six table/phase pairs. Unsupported queries raise an error; no endpoint clamping is used.

## Thermodynamic derivation

Use `c` for saturated condensate, `cp` for pumped condensate, `f` for feed pump discharge, `m` for main steam, `hp` for HP exhaust before extraction, `r` for reheat discharge, `lp` for LP exhaust and `b` for saturated-liquid heater discharge. Let `y` denote extracted fraction and `M` the main flow. Water enthalpy and work are kJ/kg; multiplying by kg/s and dividing by 1,000 gives MW.

1. Liquid pump ideal work is `v_in*(p_out-p_in)*1000`; actual fluid enthalpy rise is ideal work divided by the selected pump efficiency. Thus `h_cp=h_c+w_cp` and `h_f=h_b+w_fp`. The heater discharge is saturated liquid at 0.8 MPa. The feed discharge state follows enthalpy inversion at 6.2 MPa. The condensate-pump discharge has only pressure, enthalpy and flow outputs because the original compressed-liquid table does not cover its entire diagnostic range.
2. For each turbine, first find the downstream-pressure enthalpy at inlet entropy. Then use `h_out=h_in-eta_t*(h_in-h_out_isentropic)`. The HP reference uses the 0.8 MPa table. The LP reference uses `x_s=(s_r-s_c)/(s_v-s_c)` and `h_lp_s=h_c+x_s*(h_v-h_c)` at condenser temperature. Actual quality is `x=(h_lp-h_c)/(h_v-h_c)` and entropy is `s_c+x*(s_v-s_c)`. Both ideal and actual qualities must lie within the supported two-phase domain.
3. The open heater has unit main-flow output and incoming fractions `1-y` and `y`: `(1-y)*h_cp+y*h_hp=h_b`. Therefore `y=(h_b-h_cp)/(h_hp-h_cp)`. This fixes extraction rather than assigning it. Main/feed/HP/heater mass flow is `M`; reheater/LP/condenser/condensate-pump mass flow is `M*(1-y)`.
4. External heat per unit main flow is `h_m-h_f+(1-y)*(h_r-h_hp)`. Divide available heat by this quantity to obtain `M`. The main and reheat duties sum to the single admitted heat. Salt branch flow fractions equal their duty fractions; total salt flow is per-circuit flow times active circuit count. Each branch spans the same supply/return temperatures.
5. Turbine shaft work is `M*(h_m-h_hp)+(1-y)*M*(h_r-h_lp)`. Generator gross is shaft work times mechanical and generator efficiencies. Pump electricity is pump shaft work divided by motor efficiency. Cycle net before cooling subtracts only the two water-pump electric demands from generator gross.
6. Condenser duty is `(1-y)*M*(h_lp-h_c)`. Add mechanical loss, generator loss and pump motor loss to obtain cycle heat rejection before cooling. The fluid already contains pump shaft heat, so adding that shaft heat again would double count it. Both `Q_in+W_pump_shaft=W_turbine+Q_condenser` and `Q_in=P_cycle_net+Q_rejection` close below 1e-8 MW for the four retained cases.

## Heat profiles and conductance

For each branch, traverse water enthalpy from inlet to outlet. Countercurrent salt temperature on that coordinate is `T_salt=T_return+(T_supply-T_return)*(h-h_in)/(h_out-h_in)`. Water temperature follows every table knot, including both ends of boiling at 6.2 MPa. Between adjacent knots both temperatures are affine in enthalpy, so their difference is affine. Its true piecewise-linear minimum occurs at one of those endpoints.

For a segment with transferred heat `dQ` and positive endpoint gaps `a,b`, required conductance is `dQ*log(b/a)/(b-a)`. Equal gaps use `dQ/a`; nearly equal gaps use `log1p((b-a)/a)`. Sum every segment. A nonpositive gap is retained as a failed heat-admission diagnostic. UA then has numeric placeholder zero and availability false. This is not a claimed zero required conductance or a valid exchanger. No installed area or capacity is inferred.

## Conditional cooling-water calculation

The selected scenario is 25→35°C water, 20 m head, pump efficiency 0.80 and motor efficiency 0.95. Saturation-liquid enthalpy differences approximate low-pressure water heating. Specific shaft input is `g*head/(1000*eta_pump)` and electric input divides this by motor efficiency. Both inputs ultimately heat the represented water. Therefore `water_flow=1000*Q_cycle_rejection/(h_out-h_in-w_electric)`. The denominator must be positive. Total rejection adds cooling pump electricity once. The water-energy residual closes below 1e-8 MW.

`water_pump_rise_K` is the apparent temperature rise from specific pump-plus-motor heat divided by mean heat capacity `(h_out-h_in)/(T_out-T_in)` over the selected span. This definition was explicitly agreed with the coordinator during implementation. It is not an exact local pump-discharge state. The raw approach is condenser temperature minus cooling-water outlet temperature, with a strict positive-gap check. Cooling-site qualification remains false.

## Assumptions and limitations

[INHERITED: reviewed interface design] Pressures, 445°C main/reheat temperature, 42°C condensation, HP/LP efficiencies 0.90, water-pump efficiencies 0.80, motor efficiency 0.95, mechanical efficiency 0.99 and generator efficiency 0.98 are selected component/topology assumptions. They are separate from the conservation equations and NIST property authority. The source review locates a broad turbine-efficiency range in the original EPA source and mechanical/generator loss assumptions in Dostal's CO₂ application. Neither establishes these specific steam machines. The original-source performance review remains the authority for that transfer; this task adds no new source qualification.

The baseline heat 3,306.889098848892 MW, salt temperatures 465/269.664729914530°C, flow 10,852.114436183412 kg/s and cp 1.560 kJ/(kg K) are entering reference values. The callable interface accepts the actual supplied values. Its salt heat identity check rejects inconsistent heat and flow inputs. An 18-circuit identity check with adjusted per-circuit flow preserves all outputs; substituting twice the circuit count without changing heat explicitly refuses.

The liquid-pump approximation differs from local isentropic table inversion. Ideal feed work is 6.01983144 rather than 6.01109542 kJ/kg, a 0.14533% difference. Condensate differences are +0.00414% at 42°C and −0.06970% at 50°C. The 40°C compressed-liquid comparison is outside the captured table and remains unavailable. These are local approximation observations, not global error bounds.

Raw LP quality and moisture are retained. Turbine qualification and installed SG capacity qualification remain false. There is no moisture pass/fail threshold. Cooling water availability, hydraulics, NPSH, discharge conditions, condenser UA and equipment pricing are unresolved. The full 3% plant allowance is outside this cycle calculation. The results do not represent total plant export or total plant environmental rejection.

## Results and local resolution sensitivity

| Case | Gross MW | Cycle pumps MW | Cooling pump MW | LP quality | Main UA MW/K | Reheat UA MW/K |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 1219.998170 | 9.706961 | 13.023180 | 0.972809355 | 41.074378 | 11.186763 |
| Condenser 40°C | 1229.192293 | 9.708618 | 12.966080 | 0.969017230 | 41.092709 | 11.156605 |
| Condenser 50°C | 1183.129909 | 9.699501 | 13.252144 | 0.987965210 | 41.000039 | 11.309070 |
| Main/reheat 435°C | 1212.627619 | 9.801827 | 13.069552 | 0.968392490 | 39.823408 | 8.954071 |

Alternating-row reconstruction changes gross output by at most 0.000475 MW in these four cases. Maximum absolute UA changes are 3.04e-5 MW/K for the main SG and 2.86e-5 MW/K for reheat. Quality changes are at most 9.11e-8. The full signed per-output differences are retained. These are local table-resolution observations, not physical uncertainty or proposed comparison tolerances. Production comparisons retain the existing relative 1e-9/absolute 1e-6 policy and any stricter old-quantity policies; residual closure separately uses 1e-8 MW or kg/s. Any observed disagreement must be investigated before changing tolerances.

The author checks additionally retain 21 expected refusal cases, disabled branches that do not access properties, zero-gap failures with unavailable UA and zero cooling approach. They include the subsequently approved source-plus-recovered-heat consistency check.

## Durable oracle and native verification

The durable integration is `exploration/stellarator_e2e/oracle_matched_cycle.py`, its independently extracted `oracle_matched_cycle_properties.json`, the corresponding producer ordering in `verify_stellaris.py`, and exact generated entry/output/predicate mappings in `studies/oracle_entry.py`. The active independent property loader checks its own asset digest. This is distinct from the production approach: production embeds property bytes in its manual seeds and checks canonical/staged source assets during generation. Its runtime does not require external source JSON. Production asset-custody and tamper evidence is owned by the generation/author checks, not claimed by this receipt.

The matched-cycle producer follows the existing salt calculation. Cooling water follows the matched state calculation. Mode selection routes either matched gross efficiency or the unchanged historical efficiency into power and gross-driven costs. The historical raw efficiency/domain diagnostics remain mapped separately. Recirculation includes the two new electric pump loads once. The dormant zero-demand branch retains historical floating-point arithmetic.

`native_check.py` executed nine cases against the final generation-v3 package. Each compares all 1,050 mapped scalar/status outputs and independently re-derives all 28 predicates from generated expression IR with independent operands. Results retain native outputs, case inputs, semantic/executable fingerprints, headline quantities and every predicate verdict. In total, 9,450 mapped comparisons and 252 exact predicate comparisons pass. Real comparisons use relative 1e-9/absolute 1e-6, with the prior 1e-18 inventory absolute tolerance preserved. Boolean channels compare exactly. Applicable heat/work/mass residuals remain below 1e-8 in their units.

Cases are baseline, both modes disabled, 40/50°C condensation, 435°C main/reheat, 18 active circuits, cooling water disabled, zero cooling approach and disabled modes with invalid inactive property inputs. The baseline has four raw violated native constraints: divertor heat, tritium breeding, reference conductor current and winding-pack fit. The old equipment cycle-interface diagnostic remains zero. Zero cooling approach adds the new raw cooling-direction violation. No failure is converted to a pass. The logical OR verifier extension is separately owned/tested by the tooling agent.

| Headline | Historical modes | Matched cycle and cooling |
| --- | ---: | ---: |
| Gross electricity MW | 1360.310504326472 | 1219.998170176474 |
| Plant net electricity MW | 1008.898405504204 | 850.065300667500 |
| Overnight capital USD | 17918171013.726093 | 17751224887.079790 |
| LCOE USD/MWh | 271.584319917295 | 318.737170421704 |
| Alternate existing LCOE USD/MWh | 266.458930566605 | 312.710788413481 |

Disabling only cooling water increases plant net by exactly its 13.023180063562 MW pump demand within 1e-8 MW. Gross and cycle-pump output remain unchanged. Native gross also equals independently calculated cycle gross within the heat-closure policy in every active coherent case.

## Heat-boundary finding and correction

The first native adversarial check found that disabling selected primary or secondary recovered heat while leaving matched mode active allowed two different heat bases. The power-balance gross output was respectively 64.665736542158 or 2.093983798263 MW below the state solver's gross. Both initial production and oracle reproduced that inconsistent wiring. The failing results are retained in `native-domain-pre-heat-guard.json`; the initial nine coherent passing cases remain in `native-check-pre-heat-guard.json`.

The coordinator's separately reviewed correction adds two bound producer inputs: source heat and selected recovered heat. Active execution now requires available cycle heat to equal their sum, using the existing relative 1e-12/absolute 1e-8 heat residual policy. This check runs after the enable branch and before properties. It creates no new free design parameter. The independent oracle implements the same conservation requirement from its independently computed producers.

The final `native-domain-results.json` records seven paired native/oracle refusals: invalid matched mode, invalid cooling mode, cooling enabled without the cycle, unsupported pressure, unsupported condenser temperature, missing selected secondary heat and missing selected primary heat. The latter two now refuse residuals of 5.675887361899 and 175.280934404488 MW. Dormant invalid property inputs still execute without property access. The nine coherent cases were rerun after this correction and retain their original values.
