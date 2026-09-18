# Finite toroidal transport prototype design

Date: 2026-09-18. Status: proposed architecture awaiting the fresh method precheck. No physical prototype, response table, or production implementation was written in this task. `[OWNER]` Scientific choices are delegated in the round brief. All implementation choices below are `[AGENT]` proposals. The represented assembly and unsettled material authority come from [physical-method-proposal.md](physical-method-proposal.md); runtime identity comes from [transport-runtime.md](transport-runtime.md).

## Executable geometry and one required correction

Use the installed OpenMC 0.15.2 continuous-energy engine with concentric `ZTorus` surfaces. Its parameters are major radius `a`, vertical minor radius `b`, horizontal minor radius `c`, all in centimetres. For the circular-average model, construct every surface with `a=100*R, b=c=100*r_boundary`. The installed API and [official surface documentation](https://docs.openmc.org/en/stable/pythonapi/generated/openmc.ZTorus.html) agree. Read the model's actual radial-build inputs, accumulate its layer boundaries, then convert units once. Require positive ordered shell thicknesses and `R > outer_minor_radius`.

An inner volume is `-surface`; a shell is `+inner & -outer`. Split 2 mm W armor from the remaining 48 mm first-wall envelope. Preserve separate breeder, reflector, high-temperature shield, structure, gap and vessel cells. Increasing breeder thickness moves every downstream boundary outward while holding its individual thickness fixed. Do not reuse reference boundaries while changing the breeder inventory. Pure-shell volumes are `2*pi**2*R*(r_outer**2-r_inner**2)`; stochastic volume verification, point ownership and isotope inventory checks precede a transport result.

**Premise correction for review:** the proposal's initial vacuum boundary on the outer vessel torus would kill neutrons entering the central hole or surrounding vacuum that could strike the opposite side of the same assembly. Put a transmitting boundary on the vessel. Fill the complement of the torus with void inside an enclosing vacuum sphere centred at the machine origin and larger than `R+r_outer`. This convex enclosing boundary permits all straight vacuum return paths to the torus; once a particle crosses it outward, a straight ray cannot return. Increase the enclosing radius as a numerical check. Adding real external structures is a separate physical backscatter sensitivity, still required by the method proposal. Do not treat the exterior void as a fabricated shielding layer.

Explicit openings can use intersections of toroidal shells with toroidal-angle planes and bounded poloidal sectors; write disjoint removed-material cells and their declared fill. Angular windows must be measured by actual removed wall area and breeder volume, not equated to a uniform angular fraction on the curved torus. Freeze one opening scenario for any one table. Alternative poloidal placement and material scenarios require separate transport cases or tables; they are not post-hoc multipliers on TBR.

## Exact source measure without a source bank

The installed `IndependentSource` supports domain rejection with `rejection_strategy='resample'`. Use its native cylindrical source over an annular bounding cylinder, then reject points outside the plasma cell:

```python
space = openmc.stats.CylindricalIndependent(
    r=openmc.stats.PowerLaw(100*(R-a_plasma), 100*(R+a_plasma), 1),
    phi=openmc.stats.Uniform(0, 2*pi),
    z=openmc.stats.Uniform(-100*a_plasma, 100*a_plasma),
)
source = openmc.IndependentSource(
    space=space,
    angle=openmc.stats.Isotropic(),
    energy=openmc.stats.Discrete([14.06e6], [1.0]),
    strength=1.0,
    constraints={'domains': [plasma_cell], 'rejection_strategy': 'resample'},
)
```

Here `r` is cylindrical distance from the machine axis, not plasma minor radius. Sampling it with density proportional to `r` cancels the cylindrical coordinate Jacobian, so candidate points are uniform per physical volume. Conditioning on the plasma domain leaves exactly uniform toroidal volume density. The geometric acceptance is π/4 for the circular case. The general elliptical bounding cylinder also has π/4 acceptance when the vertical range follows its minor semiaxis. A uniform distribution in cylindrical radius would be biased.

An equivalent explicit minor-coordinate sampler proposes `rho=a_plasma*sqrt(U)`, `theta=2*pi*V`, `phi=2*pi*W`, then accepts with probability `(R+rho*cos(theta))/(R+a_plasma)`. Convert to `x=(R+rho*cos(theta))*cos(phi)`, `y=(R+rho*cos(theta))*sin(phi)`, `z=rho*sin(theta)`. Its accepted density is proportional to `rho*(R+rho*cos(theta))`, the exact toroidal Jacobian. This is a verification sampler, not a reason to add a finite reusable source bank and its extra source-sampling uncertainty.

Verify positions lie in plasma and compare moments against analytical volume averages: `E[z]=0`, `E[z²]=a_plasma²/4`, and `E[sqrt(x²+y²)]=R+a_plasma²/(4*R)`. In minor coordinates, `E[rho²]=a_plasma²/2`. Check source directions are isotropic independently of position. For the centrally peaked alternative, weight physical volume by the specified fusion emissivity derived from the model profiles; do not substitute uniform minor radius or just density alone. That profile mapping remains a separate defined case.

## Tritium score and source normalization

Use fixed-source mode, unit source strength and unit source particle weights. Score total tritium production, `(n,Xt)` in the installed 0.15.2 API, separately for `nuclides=['Li6', 'Li7']` in the breeder cells. MT205 exists in both downloaded lithium evaluations. Keep a separate direct combined-lithium tally for the uncertainty of their sum, and an all-material total-tritium tally as an accounting diagnostic. Specify which breeder regions' production is recoverable when wiring the fuel ledger. Do not silently count tritium born in unextractable structural material as usable breeding.

The integrated tally is tritons per emitted source neutron. It needs no division by breeder volume, no multiplication by blanket area or coverage, and no multiplication by history count. One DT fusion consumes one triton and emits one source neutron, so the integrated recoverable-production tally is the nuclear TBR for this stated assembly. Multiplication and secondary-neutron histories are already transported. A physical neutron source rate converts TBR to production rate downstream and cancels from the ratio. [OpenMC tally documentation](https://docs.openmc.org/en/stable/usersguide/tallies.html) distinguishes integrated reaction/production scores from volume-normalized flux. Current upstream score names have changed; retain the smoke-tested installed version and score alias in the manifest.

The lithium components are correlated because they share histories. Their means can be summed, but do not combine their standard deviations in quadrature. Read the combined tally's batch uncertainty or compute covariance from retained batch realizations. Check that its mean agrees with the component sum. Retain absorption, leakage and multiplication diagnostics; `absorption + leakage = 1` is not a valid neutron balance when neutron multiplication occurs.

## Offline transport and generated-model execution

Use a small offline transport table for repeated generated-model evaluation. The table is an approximation to newly computed transport for the declared assembly, not a transplanted published TBR curve. The direct OpenMC builder remains the authority for table-node and withheld-case generation. Record XML, material manifest, data hashes, source prescription, seed, histories, wall time and tallies for each case.

The repository already supports a typed manual implementation behind a generated SysML calculation. The wrapper at `exploration/stellarator_e2e/generated/modules/mfe_lifecycle/lifecycle_calendar.py:402` calls its handwritten implementation; `models/library/analyses/mfe_lifecycle.sysml:71` explicitly documents that route. Domain rejection through `ValueError` is used in `exploration/stellarator_e2e/generated/handwritten/mfe_cryo_plant/cryoplant_electrical_power_impl.py:13`. Use that supported route for a small piecewise bilinear interpolator with standard-library `bisect`; no new runtime scientific dependency is needed. Place its numeric nodes and identity in the handwritten package as literal data or a packaged immutable resource. The existing package coverage policy covers all files except its seal and bytecode; nevertheless verify inclusion in the regenerated seal and executable fingerprint before relying on it. The integration seam preserves handwritten files (`docs/integration_seam_operator_guide.md:180`). A production package must never depend on ignored runtime paths.

Proposed first grid: breeder thickness `[0.60, 0.70, 0.80, 0.90, 1.00]` m and Li-6 atom fraction `[0.60, 0.70, 0.80, 0.90]`, giving 20 transport nodes. This includes the retained 0.80 m / 0.70 reference. The grid is an agent-selected initial numerical domain, not a sourced engineering bound. Keep lithium concentration, constituent fractions, physical temperatures, density laws, all non-breeder layer thicknesses, major/minor radius, elongation, source profile, opening recipe, exterior materials and nuclear-data identity fixed to the selected scenario. Bilinear interpolation uses four neighbouring node values with nonnegative weights that sum to one; interpolate lithium components and their sum consistently.

**Scope restriction:** every physically active fixed input must reach the calculation as an input or a checked scenario identity. Reject changes to it, nonfinite values, or thickness/enrichment outside the closed grid domain. Floating comparison tolerances may cover only representation roundoff, never a physical change. No clamping, extrapolation, radius-independence assumption, or silently stale table. This first implementation computes response to two build levers; it does not supply a breeding prediction across the existing major/minor-radius design space. A radius study must acquire extra transport dimensions or run transport directly. That limitation must be visible to the goal owner before selecting this integration scope.

Expose at least mean TBR, numerical interpolation allowance, Monte Carlo uncertainty and domain validity through declared calculation outputs or its immutable diagnostics contract. Scientific scenario uncertainty is separate. Do not make a favorable physical verdict merely because the interpolated mean clears a threshold when the uncertainty/scenario interval crosses it.

## Withheld validation and release condition

Freeze the 20-node grid, interpolation algorithm and numerical acceptance rule before inspecting withheld outcomes. Evaluate the 12 cell centres with independent source/transport seeds; add four predeclared off-centre edge cases, one on each outer edge. A suggested edge set in `(thickness_m, enrichment)` is `(0.60,0.65)`, `(1.00,0.85)`, `(0.65,0.60)`, `(0.95,0.90)`. These 16 cases validate interpolation error, not the physical transport model. Repeated seeds at the reference and representative extremes separately check Monte Carlo behavior.

Target node and withheld standard errors ≤0.001 absolute TBR initially. Proposed release tolerance: every withheld discrepancy, conservatively increased by twice the combined node-prediction/withheld standard error, must be ≤0.005 absolute TBR. The 0.005 limit is an agent-selected approximation budget; tighten it when the fuel decision margin demands. For independently generated node estimates, the prediction variance is the sum of squared interpolation weights times node variances. Do not treat two standard errors as a guaranteed simultaneous coverage bound. Publish the largest observed discrepancy and statistical terms separately. If the criterion fails, refine the affected cells and declare a new independent withheld set; previously seen points cannot remain the sole validation set.

An experimental benchmark, nuclear-data alternatives, temperature/material choices, toroidal reduction, openings and external structures retain separate evidence. Passing table checks does not repair a failed or unavailable physical benchmark. The final conditional plant claim must carry those remaining bounds.

## Runtime budget and next authorized steps

Measured smoke execution transported 10,000 histories in 0.01698 seconds, with total engine time 0.06021 seconds and roughly 1 second for Python launch plus setup. It used a small two-isotope sphere. The layered heavy-material torus has many more evaluations, secondary histories and expensive torus intersections, so **these timings do not establish its throughput**. A linear sphere-only extrapolation would be misleading as a scheduling promise.

After the fresh method precheck and material manifest are ready, run one 100,000-history torus pilot in 50 batches and record initialization time, active-history throughput, peak memory and combined-TBR standard error. Estimate needed histories from `N_target=N_pilot*(sigma_pilot/0.001)**2`, then check that scaling with a larger independent run. Use at least 50 batches for production uncertainty estimates and repeat seeds at the reference. Record the completed pilot before committing to the 20+16 case table. A provisional wall-time estimate is `(36*N_target/observed_histories_per_second) + 36*observed_initialization_seconds`, with additional budget for sensitivity scenarios and repeat seeds. This formula is a planning estimate, not a convergence result.

Implement in this order: review the geometry/source/material premise; build the direct torus and verify its geometry/source/inventory; run the pilot and independent benchmark; declare one physical scenario and compute/validate the small table; then add the SysML calculation and typed handwritten integration under the normal model implementation and integration checks. The source acquisition and method precheck remain upstream of substantial implementation.
