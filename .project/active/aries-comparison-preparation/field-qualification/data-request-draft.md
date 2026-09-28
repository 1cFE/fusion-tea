# Draft request for reproducible Stellaris magnet inputs

[AGENT] Prepared for possible owner use. No message has been sent. Public dataset identity checks are recorded separately; this request is for the named published baseline, not permission to substitute another optimized coil set.

Subject: Geometry and field-calculation inputs for the published Stellaris coil set

We are independently evaluating the magnetic-field calculation for the Stellaris design published in Fusion Engineering and Design, DOI 10.1016/j.fusengdes.2025.114868. The paper's data-availability statement says data can be requested. Could you provide, or point us to, the following inputs for the published configuration?

An associated public coil-optimization example refers to `tests/test_files/input.stellaris` and `tests/test_files/coils.stellaris`. If these are suitable baseline inputs, could you identify their revision and whether they match the published configuration?

- The six independent coil centreline curves, coordinate units/frame, symmetry transformations and current-direction conventions, or the equivalent complete 48-coil set.
- The current normalization and family currents, with the mapping to Table 8. We want to distinguish rounded table values from the simulation inputs.
- The finite winding-pack cross sections and local orientation/placement along each curve, including the represented current-density distribution.
- The magnetic-axis/equilibrium data and the averaging convention for the stated axis field. Does the reported field include plasma current, or only the coil-generated vacuum field?
- The field-evaluation setup or reference output sufficient to reproduce the conductor maxima: peak search region, interior versus surface convention, field component/norm, solver and convergence information.

If only part of this information can be shared, a versioned coil/current dataset would still help us establish exactly which calculations are possible. Please identify whether any released geometry matches the published baseline or is a later alternative configuration. We would retain the source identity and respect its license and stated limitations.
