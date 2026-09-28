# Evidence needed to qualify the field calculation

[AGENT] This contract states what a defensible configuration-specific calculation needs. It is not evidence that those inputs have been obtained, a new automatic-sizing policy or a declaration that the present equations are qualified.

## Chosen quantities and calculated quantities

The design supplies coil geometry, winding-pack geometry, turns and operating currents. The evaluator calculates the magnetic field. A constraint compares that result with material and equipment performance. Geometry or current may be optimized in a separately declared design search; they are not silently changed by field evaluation. This preserves MR-7.

| Chosen input or evidence | Required content | Why it matters |
|---|---|---|
| Configuration identity | Named design, revision, source file hashes and mapping to the published configuration | Another optimized coil set is another design, even if it surrounds a similar plasma |
| Coil paths | Closed three-dimensional centreline curves, coordinate units/frame, symmetry operations and current-direction conventions | Major/minor radii and a drawing do not determine the magnetic field |
| Current distribution | Signed ampere-turns for each independent coil family; selected turns and per-turn current when winding inventory is assessed | A single largest coil current does not specify the other families |
| Finite winding packs | Cross-section dimensions, location about each path, local orientation and assumed current-density distribution | Peak field depends on pack size and orientation; evaluating a filament at its own location is singular |
| Magnetic-axis definition | Axis curve or a reproducible field-line/equilibrium calculation; distinguish vacuum and finite-pressure state | An on-axis field needs a specified axis and averaging convention |
| Output definitions | Point field vector, axis field convention and maximum-field search region | A local maximum, axis average and toroidal-field component cannot be interchanged silently |
| Independent checks | Matching source cases or independently implemented calculations with stated geometry/current/pack identities | Reproducing one scalar calibration does not validate transfer or pack response |

An imported dataset must pass these checks before it is called the published baseline. A plasma boundary alone cannot identify a unique coil set. A coil centreline file alone may permit a vacuum field away from the coils, but does not establish a conductor peak field without a finite-pack representation.

## Calculation and verification

Use the supplied signed current distribution in a finite-conductor magnetic calculation. The source method described in Lion 2021 §3.7 and Lion 2023 §2.3.5 discretizes rectangular, uniformly filled packs into finite straight beams. That is an available method, not evidence that this project's Stellaris geometry has been reconstructed. Different pack shapes/current distributions require an explicit representation and corresponding verification.

Verify units and current normalization; analytical loop/straight-conductor cases away from singularities; signed superposition; current reversal and proportional scaling; convergence in coil segmentation, pack integration and peak-field search; and independent selected pack-size changes. Compare like-for-like axis averages and conductor maxima. Choose numerical error targets from the intended engineering decision and source precision; do not infer acceptance from a tolerance chosen merely to match the source result.

If using the Lion peak-field surrogate, determine both configuration-specific coefficients from calculations at multiple independently selected pack areas, then verify withheld pack sizes. Changes in coil shape, count, family-current ratios or axis convention require new support. A surrogate's supported interval is the verified calculation domain, not the union of convenient input values.

The six families in Stellaris Table 8 are not six independent pack-size experiments. Their shapes and currents differ within one mutually interacting coil set. Fitting one pair of peak-field coefficients to those six columns would confuse coil-to-coil differences with controlled pack-size response.

## What can already be justified

For a fixed current-path configuration in a linear magnetostatic model, multiplying every coil current by the same positive factor multiplies the field by that factor. Scaling every spatial dimension, including finite packs and the evaluation locations, by a factor s at fixed ampere-turns divides the field by s. This describes a family of physically similar calculations; it does not validate the absolute calibration or prove that independently supplied scalar radii describe a similar three-dimensional shape. Finite-pressure equilibrium changes and nonlinear magnetic materials need separate treatment.

Lion 2023 Eqs. 2.65–2.66 explicitly define the axis quantity by an arclength integral and its configuration-specific current scaling. Lion 2021 Eq. 39 retains two independent peak-field coefficients. The [exact algebra checks](evidence/identifiability.json) demonstrate that two positive coefficient pairs can reproduce the same reference point while disagreeing when pack size changes. The illustrative coefficients are not physical bounds, estimates or replacements for missing data.

## Current limitations

The present generated peak-field function has no winding-pack-area input. Its positive-clearance checks establish arithmetic admissibility only. The field input interface supplies a single peak-family current with a fixed calibration factor rather than an explicit set of family curves/currents. The radial build supplies a coil-radius proxy; it does not certify three-dimensional similarity. These are scope limitations, not reasons to select new geometry or current for the user.

A scientifically qualified replacement must satisfy the data and verification requirements above. Until then, retain the current field values only as calculations of the declared approximation and propagate their unqualified status in the partial assessment. Do not turn a theoretical scaling relation into blanket approval of the existing design envelope.
