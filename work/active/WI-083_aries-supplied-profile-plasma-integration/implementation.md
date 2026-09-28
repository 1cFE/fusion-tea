# WI-083: Forward quantities now execute

[AGENT] The declared-input plasma scenario computes fusion power and thermal pressure, then executes the unchanged beta calculation against that pressure. Fourteen supported native cases pass and 25 invalid or unconverged cases refuse. This is a conditioned design evaluation, not a reconstructed ARIES reference or LCOE result. Source/design review accepted the bounded contract; independent integrated review accepted this bounded result; see `work/orchestration/aries-transfer-experiment/evidence/plasma-integration-review.md`.

## Calculated scenario outputs

| Calculated quantity | Native result |
|---|---:|
| Fusion power | 1835.4512830147435 MW |
| Mean thermal pressure under selected measure | 724771.480507903 Pa |
| Thermal beta under selected measure | 0.05606492483679988 |
| Stored thermal energy | 482.69780601826346 MJ |
| Electron-density mean under selected measure | 3.619464285713925e20 m^-3 |
| Density-weighted temperature | 6.35553998717378 keV |
| Final Simpson intervals | 4096 |
| Largest last relative moment change | 1.5182339612217214e-12 |

[AGENT] Inputs retain the spec's selected amplitude 5e20 m^-3, finite-edge density shape, temperature sensitivity case with central 11.83 keV and selected 0.2-keV edge, constant local helium ratio 0.0335, equal D/T, supplied volume 444 m^3, field 5.70 T and normalized measure exponent 2. No published fusion-power, beta or density-mean target enters the computation. The mean is qualified by the chosen measure; the physical ARIES Jacobian is still missing. The absolute source profile and VMEC temperature remain unreconstructed.

## What transfers and what is new

- **Unchanged SysML calculation reuse:** `Radial Density Profile` supplies a real native sample and its accepted implementation is used throughout quadrature; `Volume-Averaged Beta` executes unchanged downstream of the new pressure producer. Their original library files remain unchanged.
- **Unchanged helper reuse:** `_sigv_dt` is extracted byte-for-byte as a function from the existing normative generated implementation. The new caller guards its inherited 0.2–100-keV domain before evaluation. This is helper reuse, not reuse of the old whole-plasma integration calculation.
- **New physics assembly:** one `Supplied Profile Plasma` calc combines source-supported profile equations with explicit species/measure choices and forward reaction/pressure integration. One new case owns those choices and exposes `aries_cs_plasma_integration::plasma::fusion_power_MW` as a stable calculated attribute for later consumers.
- **New numerical implementation:** a typed completion performs Simpson refinement, checks domain and finite arithmetic, reports interval count and successive change, and refuses an unresolved profile at 65536 intervals. The change estimate is not a rigorous integration error bound or a universal accuracy claim.

## Reproduction and verification

```bash
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/plasma_integration/verify.py
.codex-test/run agentic-mbse validate exploration/aries_transfer/plasma_integration/staged_models --complete
```

[AGENT] The first command parses the source, stages unchanged library files plus the two new files, generates the new package, installs exact helper reuse and the typed completion, regenerates its seal and runs actual native TEAx. `evidence/reuse-identity.json` records full source hashes and the original reaction function AST hash. The script checks the actual generated wrapper's output order before execution. Ephemeral package/link/run stores are locally ignored. `evidence/verification.json` retains every supplied value, output and refusal; `native-attempt-2.log` records the successful run and fingerprint.

[AGENT] Independent polynomial antiderivatives check density and pressure moments at the source shape under the selected measure. A constant-density/constant-temperature case checks the analytical reaction identity. Seven temperatures reproduce the original reaction helper exactly. Explicit 2048/4096/8192 integrations verify the baseline refinement behavior. A fractional endpoint case with measure exponent 1.5 and temperature profile exponent 0.5 converges at 16384 intervals; an unresolved density boundary layer refuses at 65536. Neither test is a blanket guarantee for all admitted shape values.

[AGENT] Actual public-input cases establish linear density/pressure/energy and quadratic fusion scaling with amplitude; volume scales total power/energy while pressure remains fixed; field changes beta inversely with its square while fusion power remains fixed; D/T symmetry and zero-fuel boundaries preserve the species accounting. Source-like low edge temperature 0.023 keV refuses rather than clipping. Other cases exercise invalid temperature order, exponents, species fractions, geometry/field/measure and nonfinite inputs. Supplied input artifacts remain unchanged. These are MR-7 choice-preservation checks; hardware sufficient/insufficient capacity pairs are not applicable.

[AGENT] Complete validator actual exit is **1**. Levels 1–5 pass. Level 4 counts zero SysML constraints; runtime guards are instead evidenced by native refusals. Level 6 reports nine pure EXPOSE dot-expression diagnostics corresponding to the eight integration attributes and beta output. Native generation resolves the output channels and all 14 supported cases execute them, including pressure's downstream beta binding. The independent reviewer accepted these nine exceptions narrowly, not a claim that the six-level aggregate passes. `evidence/validation-complete.log` retains the full result; a targeted verbose attempt did not expand the CLI's five-issue display limit and is retained as `validation-level6-verbose.log`.

## Failures retained and resolved

[AGENT] Initial generation failed because an inline `// AGENT-selected...` comment was interpreted as unit metadata on the amplitude's computed-edge consumer, conflicting with its Real calc inputs. `generation-initial.log` and `generation-metadata-debug.log` retain the failure and exact metadata witness. Removing ambiguous inline comments repaired the new case; units and authority remain in the calc/part documentation and spec. No parser/generator or existing model was changed. `generation-repaired.log` records successful normal generation.

[AGENT] The first native runner failed to relocate the unchanged beta calculation's additional default-parameter JSON when staging each run. `native-attempt-1.log` retains that failure. The runner now resolves every generated entry artifact path before applying case inputs. No physical input or equation changed; `native-attempt-2.log` records success.

## Tracking handoff

[AGENT] Trace element: `supplied_profile_plasma::'Supplied Profile Plasma'`, file `models/library/analyses/supplied_profile_plasma.sysml`. Case producer: `aries_cs_plasma_integration::plasma::fusion_power_MW`, file `models/designs/aries_cs_transfer/plasma_integration.sysml`. Verification identifier: `WI-083-native-supplied-profile-integration`; executable `exploration/aries_transfer/plasma_integration/verify.py`; durable receipt `evidence/verification.json`. Coordinator owns registry/commit operations. Final review accepted; SV-127 and the new calculation trace are registered.
