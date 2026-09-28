# WI-081 implementation evidence

[AGENT] The new local-density relationship executes through the normal generated TEAx route. Thirteen supported cases pass and 25 unsupported inputs refuse. This proves one new equation component and one new ARIES-shape case, with explicit amplitude preserved; it does not demonstrate reuse of the previous whole-plasma module or predict fusion power/LCOE. Source/design acceptance is in `work/orchestration/aries-transfer-experiment/evidence/profile-review.md`; independent final review accepted the bounded implementation in `work/orchestration/aries-transfer-experiment/evidence/implementation-review.md`.

## Files and semantic scope

- `models/library/analyses/radial_density_profile.sysml`: one new reusable calculation, authored equation and supported mathematical domain, no ARIES-selected values.
- `models/designs/aries_cs_transfer/density_profile.sysml`: one new profile component occurrence; source shape parameters, explicit arbitrary unit amplitude, independent edge-ratio choice, and calculated local density.
- `exploration/aries_transfer/density_profile/radial_density_profile_impl.py`: typed completion enforcing finite/range and arithmetic checks around the authored equation. It consumes the generated schema; no replacement generator or numerical framework.
- `exploration/aries_transfer/density_profile/verify.py`: isolated parser check, model staging, normal generation, completion/sealing, and real TEAx execution. Ephemeral generated packages, runtime stores and import links are locally ignored; source and verification scripts remain durable.

[AGENT] The generated graph has two arithmetic modules: the case's simple amplitude-times-edge-ratio binding and the new density calculation. Six case choices remain public inputs. All original shared calculations and plant bindings remain unchanged. The amplitude is an equation coefficient and is not relabeled as actual center, peak or average density.

## Verification and reproduction

```bash
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/density_profile/verify.py
```

[AGENT] `evidence/verification.json` records the generated package fingerprint, exact model/completion hashes, supplied values, numerical outputs and rejection messages for every check. `evidence/parse-api.json` records zero parser/semantic errors. Generation and sealed-completion logs are `generation.log` and `generation-completed.log`; `native-final.log` records the successful result. The final fingerprint is reported in that receipt and must be read from it rather than assumed stable after regeneration.

[AGENT] Numerical checks use the independently reviewed expanded reference polynomial at five radial coordinates. Other cases verify sevenfold amplitude scaling, an explicitly synthetic `1e20 m^-3` amplitude, a changed edge ratio, constant-density `E=A`, nonhollow `h=1`, zero-density hollow center, different exponents and largest-finite constant density. The invalid cases exercise both sides of coordinate/hollowness bounds, nonpositive amplitude/exponents, edge outside `[0,A]`, NaN/Inf in every public choice, and overflow in the upstream edge-density binding. The density guard refuses that nonfinite producer result through actual TEAx.

[AGENT] All six applicable validation levels were assessed with `.codex-test/run agentic-mbse validate exploration/aries_transfer/density_profile/staged_models --complete`. Actual exit status is **1**, retained with full output in `evidence/validation-complete.log`. Levels 1–5 pass: no syntax errors, unbound/self-named/undefined inputs or dependency cycles; documentation coverage passes. Level 4 counts zero SysML constraints, so its green status does not validate the runtime domain: the typed completion and 25 native refusal checks provide that evidence separately. Level 6 has one diagnostic, `Unsupported operator '.'` for the pure EXPOSE `density = profile.density` at case line 31. This is the project-prescribed EXPOSE pattern; successful generation resolves it into the native exit output `plasma_profile__density.json`, which all 13 valid executions read. That exact source/consumer evidence supports a scoped exception, subject to independent review; the six-level aggregate is not reported as passing.

[AGENT] Finite intermediates/output are checked explicitly. Inside the supported domain each shape factor is bounded by one and output lies between zero and the supplied amplitude, so an interior overflow cannot be independently forced without violating the domain first. The largest-finite constant test checks the upper boundary; the upstream binding-overflow test verifies the refusal path. This is mathematical-domain evidence, not a measured plasma-validity envelope.

[AGENT] MR-7 evidence: altered amplitude, ratio, exponents and hollowness reach actual generated consumers; output follows the supplied values and input files remain unchanged. No automatic normalization, inverse peak/mean solve, capacity purchase or hardware selection occurs. Insufficient/sufficient hardware tests are inapplicable to this local profile relationship. Four-view coverage is the bounded requirement → radial density behavior → profile-owned properties → explicit calc/EXPOSE → checks described in the design.

## Failed attempts and limits

[AGENT] `evidence/native-attempt-1.log` retains a runner failure after native evaluation: TEAx returns `RootModel[float]`, while the initial assertion expected a raw float. The runner now reads `.root`; `native-attempt-2.log` records the successful correction. `evidence/parse.log` retains a failed attempt to invoke an unavailable `syside` CLI executable. The installed Python `syside.try_load_model` API then verified parsing and semantic diagnostics successfully; that check is now in the reproduction script.

[AGENT] The primary page's coefficient-versus-axis ambiguity remains visible in the model and spec. No source amplitude was recovered. Moments, temperature/composition profiles, coupled plasma closure, plant applicability and cost remain outside the evidence.

## Native tracking handoff

[AGENT] Suggested trace element: `radial_density_profile::'Radial Density Profile'`, file `models/library/analyses/radial_density_profile.sysml`; comparison occurrence `aries_cs_density_profile::plasma_profile`, file `models/designs/aries_cs_transfer/density_profile.sysml`. Test identifier: `WI-081-native-profile-contract`, executable `exploration/aries_transfer/density_profile/verify.py`, evidence `evidence/verification.json`. Coordinator owns native trace/validation registry operations and final work-item disposition.
