# WI-081 design

[AGENT] Proposed design; independent review pending. Source interpretation and unresolved amplitude identification are in `spec.md`. No source amplitude is inferred.

## Responsibilities and roles

| Owner | Responsibility |
|---|---|
| `models/library/analyses/radial_density_profile.sysml` | Generic `Radial Density Profile` calc defining the explicit equation and mathematical domain, with six supplied Real inputs and one local-density output. Use absolute `m^-3` values with documented units, matching the existing scalar codegen convention. |
| `models/designs/aries_cs_transfer/density_profile.sysml` | A `plasma_profile` part occurrence owns the source shape parameters, arbitrary demonstration amplitude `1 m^-3`, edge ratio `0.1`, coordinate and density EXPOSE. A sibling arithmetic binding sets edge density from amplitude and the case's chosen ratio; calc formals have distinct names to avoid self-binding. |
| `exploration/aries_transfer/density_profile/` | Reproducible isolated model staging/generation, typed manual completion if required, native verification and recorded outputs. No baseline regeneration. |

[AGENT] Equation inputs `amplitude_in`, `edge_density_in`, `rho_in`, `radial_exponent_in`, `profile_exponent_in` and `hollowness_in` remain supplied choices; `density` is calculated. The ratio is a source case choice, not generic physics. An arbitrary amplitude of one exposes the normalized equation shape numerically while preserving physical units; it is not a physical reference density.

## Execution and validity

[AGENT] Author the equation in the library calc and document the runtime domain there. Generate the isolated package normally. A typed handwritten implementation may be necessary to enforce finite/range guards before exponentiation; if so, preserve the equation in SysML as the authoritative declared relationship, consume the generated typed input contract, return the generated wrapper's actual scalar contract, and raise `ValueError` for unsupported inputs or arithmetic. Regenerate with `--overwrite --preserve-handwritten` so the generated seal includes the final body. This follows `work/orchestration/aries-transfer-experiment/native-route.md` and introduces no generator/runtime change.

[AGENT] The supported subset bounds guarantee nonnegative finite mathematical density, but finite float operations can still overflow or underflow. Require a finite result; exact zero at an explicitly zero edge or hollow center is valid. Input bounds exclude the ambiguous `0^0` endpoint. No empirical fidelity claim follows from these guards. Real TEAx must propagate invalid-input failures, which the tests will demonstrate.

## Four views and verification

[AGENT] Requirement R1/R2 demands a supported source-profile relationship. The behavior is radial particle-density distribution; the profile component owns its supplied properties and calculated local density. Its calc bindings are the analysis view. Tests trace those outputs to R1–R4: center `(A-E)*h+E`, edge `E`, a separately evaluated reference interior point, general shape changes, linear scaling when both `A` and `E` scale, and invalid-input failure. R5 is checked by the scoped diff.

[AGENT] A special `q=1` case admits independent polynomial arithmetic, giving a check distinct from copying the generic implementation. The source case's center is `0.694 m^-3` and edge `0.1 m^-3` under its demonstration amplitude. Tests also hold amplitude/edge fixed while changing hollowness, and hold the shape fixed while changing amplitude and its explicitly coupled case edge value. Mean/max conversion and downstream plasma integration are deferred.
