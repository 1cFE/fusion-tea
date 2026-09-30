---
source: "https://ukaea.github.io/PROCESS/eng-models/tf-coil-superconducting/"
source_type: "url"
extracted_at: "2026-09-30T03:29:01.921514+00:00"
content_hash_sha256: "92c2db23180aceeca9532a26da6af1ac5d93ae30b3163898123b5a7a91d32e60"
backend: "trafilatura"
title: "Superconducting TF coil"
---

# Superconducting TF coil

### Superconducting coil geometry

The TF coils are assumed to be supporting each other against the net centering force. This can be described as a vaulted or wedged design. Each coil, illustrated in *Figure 1*, can be separated in two main sections:

**The winding pack (WP)**: section containing the superconducting cables (Blue area in*Figure 1*). The ground insulation and the insertion gap (the clearance required to allow the winding pack to be inserted, shown as the dark grey area in*Figure 1*) is considered part of the WP by convention.**The steel casing**: Section holding the WP providing the necessary structural support (light grey area in*Figure 1*).

The next sub-section describes the different parametrization proposed in *PROCESS*:

#### TF coil inboard radial size

Following the geometry and its parametrization presented in *Figure 1*, the TF total thickness *dr_tf_inboard* \( \left( \Delta R_\mathrm{TF} \right) \) is related with the inner and outer case radial thicknesses (*dr_tf_nose_case*, \( \Delta R_\mathrm{case}^\mathrm{in} \) and *dr_tf_plasma_case*, \( \Delta R_\mathrm{case}^\mathrm{out} \) respectively) and the WP radial thickness *dr_tf_wp_with_insulation* \(\Delta R_\mathrm{WP}\) by the following equation :

with \( R_\mathrm{TF}^\mathrm{in} \) (*r_tf_inboard_in*) the radius of the innermost TF edge, set by the central solenoid coil size and \( N_\mathrm{TF} \) the number of TF coils. Reverted, to provide the WP thickness, the same equation simply becomes:

The TF coil radial thickness (*dr_tf_inboard*) can parametrized in two ways in *PROCESS*:

**Direct parametrization**: the TF radial inboard thickness width is set as an input variable :`dr_tf_inboard`

(iteration variable 13). The WP radial thickness (`dr_tf_wp_with_insulation`

) is calculated from`dr_tf_inboard`

and the two case radial thicknesses. This parametrization is used by default.**WP thickness parametrization**: the TF inboard radial thickness is calculated from the the case and the WP radial thickness. This option is selected by using the WP thickness (`dr_tf_wp_with_insulation`

, iteration variable 140) as an iteration variable. Doing so, any`dr_tf_inboard`

values will be overwritten and for this reason`dr_tf_wp_with_insulation`

and`dr_tf_inboard`

cannot be used as iteration variables simultaneously. Although not set by default for backward compatibility, this parametrization provides a more stable optimization procedure (negative WP area layer cannot be obtained by construction) and is hence encouraged.

#### Case geometry

Although not physically divided into pieces, three sections of the case can be considered:

**The nose casing:**this section corresponds to the case separating the WP with the machine center. Due to the presence of net electromechanical centering forces, this case has a major structural purpose and is often much larger than the other sides. The nose case dimension is set by its radial thickness that the user can specify using the`dr_tf_nose_case`

input variable (iteration variable 57).**Sidewall casing:**this section corresponds to the lateral side of the case, separating the WP with the other vaulted coils. As in the WP geometry is generally squared, the sidewall case thickness may vary with the machine radius. For this reason, the user sets its dimensions though its minimal thickness`dx_tf_side_case_min`

. The user can either directly specify`dx_tf_side_case_min`

or define it as a fraction of the total coil thickness at the inner radius of the WP (`r_tf_wp_inboard_inner`

) with the`casths_fraction`

input. If`casths_fraction`

is set in the input file, the`dx_tf_side_case_min`

value will be overwritten.**Plasma side casing:**this section corresponds to the case section separating the WP with the plasma. As the geometry of this section is rounded, its thickness is set by its minimal value`dr_tf_plasma_case`

(user input). This parameter can also be defined as a fraction of the total TF coil thickness`dr_tf_inboard`

using`f_dr_tf_plasma_case`

. If the`f_dr_tf_plasma_case`

parametrization is used, the`dr_tf_plasma_case`

value will be overwritten.

#### Winding pack geometry

Several Winding pack geometries can chosen with the `i_tf_wp_geom`

integer switch as shown in Figure 3:

`i_tf_wp_geom = 0`

: Rectangular winding pack. It is the only geometry compatible with the integer turn parametrization (`i_tf_turns_integer = 1`

).`i_tf_wp_geom = 1`

: Double rectangle winding pack. The two rectangles are have the same radial thickness and their width in the toroidal direction is defined with the minimal sidewall thickness at their innermost radius.`i_tf_wp_geom = 2`

: Trapezoidal WP. The WP area is defined with a trapezoid, keeping the sidewall case thickness constant. This is however probably not a realistic shape as the turns are generally rectangular. This option has been added mostly to allow comparison with simplified FEA analysis configurations.

#### Turns geometry

*Figure 4* illustrates the winding pack internal structure and the
individual turns structure.

The winding pack is assumed to be made of N_\mathrm{turn} (`n_tf_coil_turns`

)
turns. The number of turns can be parametrized in three different ways :

**Current per turn parametrization (default):**`i_tf_turns_integer = 0`

the user sets the value of the current flowing in each turns`c_tf_turn`

. The number of turns necessary to carry the total TF coil current is then deduced from`c_tf_turn`

. There is no guarantee that a realistic turn configuration (with all the turn geometrically fitting in the allocated space) or even have an integer number of turn is used with this parametrization. If the turn thickness`dx_tf_turn_general`

or the cable space thickness`dx_tf_turn_cable_space_general`

is defined by the user, this parametrization is not selected.**Turn size parametrization:**the dimension of the turn`dx_tf_turn_general`

can be set by the user. To do so, the user just have to select the following option:`i_tf_turns_integer = 0`

and to set a value to the variable`dx_tf_turn_general`

. The area of the corresponding squared turn and the number of turns necessary to fill the WP area is deduced. There is no guarantee that a realistic turn configuration (with all the turn geometrically fitting in the allocated space) or even have an integer number of turns is used with this parametrization. The current per turn`c_tf_turn`

will be overwritten.**Cable size parametrization:**the dimension of the SC cable`dx_tf_turn_cable_space_general`

can be set by the user. To do so, the user just have to select the following option:`i_tf_turns_integer = 0`

and to set a value to the variable`dx_tf_turn_cable_space_general`

. The area of the corresponding squared turn is deduced adding the steel conduit structure and the turn insulation. The number of turns necessary to fill the WP area is then deduced. There is no guarantee that a realistic turn configuration (with all the turn geometrically fitting in the allocated space) or even have an integer number of turns is used with this parametrization. The current per turn`c_tf_turn`

will be overwritten.**Integer turn parametrization:**`i_tf_turns_integer = 1`

the user sets the number of layers in the radial direction (`n_tf_wp_layers`

) and the number of turns in the toroidal direction (`n_tf_wp_pancakes`

). The number of turns is integer. The turn cross-section is not necessarily square, giving different averaged structural properties in the radial and toroidal directions. Only a rectangular WP can be used for this parametrization.

The turn internal structure, illustrated in *Figure 4*, is inspired
from the cable-in-conduit-conductor (CICC) design, with the main different
being that a rounded squared cable space is used (grey area in *Figure 4
*). The rounding curve radius is take as 0.75 of the steel conduit
thickness. The turn geometry is set with with the following thicknesses:

**Turn insulation thickness**user input setting the thickness of the inter-turn insulation.`dx_tf_turn_insulation`

:**Steel jacket/conduit thickness**user input thickness of the turn steel structures. As it is a crucial variable for the TF coil structural properties it is also an iteration variable.`dx_tf_turn_steel`

(iteration variable 58):**Helium cooling channel diameter**user input defining the size of the cooling channel.`dia_tf_turn_coolant_channel`

:

#### Cable composition

As the conductor cable composition is only used to correct the area used to
compute current density flowing in the superconductor material, to be compared
with its critical current density, an average material description is enough
for the *PROCESS*models. The composition is set with the following
material fractions:

**Cable void fraction (**user input setting the void fraction between the strands. This fraction does not include the helium cooling pipe at the cable center.`f_a_tf_turn_cable_space_extra_void`

):**Copper fraction (**user input setting the copper fraction. This fraction is applied after the void and helium cooling channels areas has been removed from the conductor area. Does not include any copper from REBCO tape if used.`f_a_tf_turn_cable_copper`

):

## Critical current density for the superconductor

The minimum conductor cross-section is derived from the critical current density for the superconductor in the operating magnetic field and temperature, and is enforced using constraint 33.

Switch `i_tf_sc_mat`

specifies which superconducting material is to be used:

`i_tf_sc_mat == 1`

-- Nb_3Sn superconductor, ITER critical surface parameterization[^5], standard critical values`i_tf_sc_mat == 2`

-- Bi-2212 high temperature superconductor`i_tf_sc_mat == 3`

-- NbTi superconductor`i_tf_sc_mat == 4`

-- Nb_3Sn superconductor, ITER critical surface parameterization[^5], user-defined critical parameters`i_tf_sc_mat == 5`

-- WST Nb_3Sn parameterization`i_tf_sc_mat == 6`

-- REBCO HTS tape in CroCo strand`i_tf_sc_mat == 7`

-- Durham Ginzburg-Landau critical surface model for Nb-Ti`i_tf_sc_mat == 8`

-- Durham Ginzburg-Landau critical surface model for REBCO`i_tf_sc_mat == 9`

-- Hazelton experimental data combined with Zhai conceptual model for REBCO

The fraction of copper present in the superconducting filaments is given by `f_a_tf_turn_cable_copper`

(iteration variable number 59). For cases where REBCO tape is used this copper fraction does not include the copper within the tape.

For `i_tf_sc_mat = 2`

, a technology adjustment factor `fhts`

may be used to modify
the critical current density fit for the Bi-2212 superconductor, to describe the
level of technology assumed (i.e. to account for stress, fatigue, radiation,
AC losses, joints or manufacturing variations). The default value for `fhts`

is
0.5 (a value of 1.0 would be very optimistic).

For `i_tf_sc_mat = 4`

, important superconductor properties may be input as follows:
- Upper critical field at zero temperature and strain: `bcritsc`

,
- Critical temperature at zero field and strain: `tcritsc`

.

The toroidal field falls off at a rate 1/R, with the peak value occurring at the outer edge of the inboard portion of the TF coil winding pack (radius `r_b_tf_inboard_peak`

).

Three constraints are relevant to the operating current density J_{\mbox{op}} in the TF coils.

-
Critical current (

`constraint 33`

): f_{\text{iooic}}J_{\mbox{op}} must not exceed the critical value J_{\mbox{crit}} where`f_j_tf_wp_critical_max`

is a margin on the constraint that defaults to`0.7`

. -
Temperature margin (

`constraint 36`

) -- The critical current density J_{\mbox{crit}} falls with the temperature of the superconductor. The temperature margin \Delta T is the difference between the current sharing temperature (at which J_{\mbox{crit}} would be equal to J_{\mbox{op}}) and the operating temperature. The minimum allowed \Delta T can be set using`tmargmin`

together with constraint equation 36. Note that if the temperature margin is positive, J_{\mbox{op}} is guaranteed to be lower than \jcrit, and so constraints 33 and 36 need not both be turned on. It is recommended that only one of these two constraints is activated.

## Quench protection

Superconducting quenches in the TF coil are modelled using a simple 0-D adiabatic heat balance in which the heat rise in the copper during a quench is equal to the heat rise required to increase the material temperature by dT. This is known as a ``hotspot criterion'' model, as the maximum temperature during a quench is the termination criterion (the point at which the quench is considered irreparably damaging).

The copper is assumed to carry the full current during a quench, and the materials are assumed to be in thermal equilibrium. We have:

Where P(t) is the power deposited in the copper through Joule heating at time t, and the sum on the RHS is over the conductor constituents (copper, helium, superconductor), where V_{i} is the volume of said constituent. This can be rewritten as:

The LHS is solved analytically, assuming that the current is at the operational value J_{op} for some quench detection time t_{detection} and then decays exponentially with a time constant \tau_{discharge}. The RHS is solved numerically by integration of the temperature-dependent material properties over dT.

The resistivity of copper, \nu_{Cu}, is an extremely important parameter in this model. The residual-resistance-ratio (RRR) of the copper can be specified, and magneto-resistive and irradiation-induced increases in resistivity are accounted for. The magnetic field at which the copper resistivity is calculated is kept constant at B_{TF,peak}. This is conservative, and to simplify the implementation (keeping the separation of the t and T integrations).

Formally this gives:

`Constraint 35`

-- To ensure that J_{\mbox{op}} does not exceed the quench protection current density limit, J_{TF,\mathrm{quench}}, turn on constraint equation no. 35.

## Supercoducting TF coil class | `SuperconductingTFCoil(TFCoil)`


### Winding Pack Geometry | `superconducting_tf_wp_geometry()`


Depending on the value of `i_tf_wp_geom`

different WP geometries will be configured.

Initial general dimensions are calculated first as follows:

Find the straight toroidal width of the TF coil at the inside edge of the winding pack:

To find the straight toroidal length of the winding pack we now take off the side case thicknesses:

We also set a commonly used parameter for the radial thickness of the winding pack without the insulation and insertion gap.

#### Rectangular WP

For a [rectangular winding pack](https://ukaea.github.io#winding-pack-geometry) (`i_tf_wp_geom == 0`

) of constant shape:

The full winding pack area with insulation is:

The area of the winding pack with no insulation or gap is:

The area of the surrounding winding pack insulation is:

#### Double rectangular WP

For a [double rectangular winding pack](https://ukaea.github.io#winding-pack-geometry) (`i_tf_wp_geom == 1`

):

The straight toroidal width of the primary winding pack is:

The straight toroidal width of the secondary winding pack is:

The average toroidal straight width is calculated:

The total winding pack area is calculated from the average:

The area of the winding pack with no insulation or gap is:

The area of the surrounding winding pack insulation is:

#### Trapezoidal WP

For a [trapezoidal winding pack](https://ukaea.github.io#winding-pack-geometry) (`i_tf_wp_geom == 2`

):

The straight toroidal width of the primary winding pack is (longest side of trapezoid):

The straight toroidal width of the secondary winding pack is (shortest side of trapezoid):

The average toroidal straight width is calculated:

The total winding pack area is calculated from the average:

The area of the winding pack with no insulation or gap is:

The area of the surrounding winding pack insulation is:

### Case geometry | `superconducting_tf_case_geometry()`


The areas of the total casing surrounding the winding packs on the inboard and outboard leg are calculated:

The plasma facing front case area is calculated:

If `i_tf_case_geom == 0`

then the front case is circular so:

The first term is equal to the area of an arc segment of radius R_{\text{TF,inboard-out}}. Since the value of `rad_tf_coil_inboard_toroidal_half`

is a fraction of \pi for each TF coil it can be substituted as the fraction of a full circle.

If `i_tf_case_geom == 1`

then the front case is straight so:

Next the nose case area is calculated:

Finally the average side case thickness is calculated:

If `i_tf_wp_geom == 0`

then a rectangular casing is:

This is equal to the sidewall casing thickness at the very centre of the winding pack.

If `i_tf_wp_geom == 1`

then a double rectangular casing is:

Finally, if `i_tf_wp_geom == 2`

then a trapezoidal casing is:

### On coil ripple | `peak_b_tf_inboard_with_ripple()`


The ratio of TF coil magnetic field increase with respect to the axisymmetric formula has been defined as :

with B_\mathrm{rip} being the maximum field measured at the middle of the
plasma facing sides of the winding pack and B_\mathrm{nom} the nominal maximum
field obtained with the axisymmetric formula (see [section TF coils current](https://ukaea.github.io/tf-coil/#tf-coil-currents-tf_current)).
The same `FIESTA`

runs have been used to estimate the on-coil ripple.
This peaking factor has been fitted separately for 16, 18 and 20 coils using
the following formula:

with the A_n the fitted coefficients and t the relative winding pack lateral thickness defined as:

with \Delta R_\mathrm{tWP}^\mathrm{out} defined in Figure 1 and 3 and \Delta R_\mathrm{tWP}^\mathrm{out\ max} the same value calculated without sidewall case as illustrated in Figure 12.

And the relative winding pack radial thickness z given by

The three fits (for 16, 18 and 20 coils) are valid for:

-
**relative toroidal thickness:**t\in[0.35-0.99] -
**relative radial thickness:**z\in[0.2-0.7] -
**Number of TF coils:**Individual fits has been made for 16, 18 and 20.**For any other number of coils, the**and a default ripple increase of 9% is taken ( f_\mathrm{rip}^\mathrm{coil} = 1.09). This default value is also used for 17 and 19 coils.*FIESTA*calculations are not used

Figure 6 shows a contour plot of the on-coil ripple peaking factor as a function of the winding pack sizing parameters for 16 coil.

These ripple calculations are out of the spherical tokamak design range, which generally have fewer coils (between 10 and 14) and more radially thick winding packs. It is also worth mentioning that the the ripple must be evaluated layer-by-layer for graded coil designs, to get the genuine B field of each layer used to quantify the SC cross-section area per layer. Finally, resistive coils do not suffer from on-coil ripple as there is no radial case present.

## Cable in Conduit TF coil class | `CICCSuperconductingTFCoil(SuperconductingTFCoil)`


WIP

### Averaged turn geometry | `tf_cable_in_conduit_averaged_turn_geometry()`


### Integer turn geometry | `tf_cable_in_conduit_integer_turn_geometry()`


### Superconductor length | `calculate_cable_in_conduit_superconductor_length()`


### Superconductor strand count | `calculate_cable_in_conduit_strand_count()`


### Superconductor properties | `tf_cable_in_conduit_superconductor_properties()`


## Cross Conductor TF coil class | `CROCOSuperconductingTFCoil(SuperconductingTFCoil)`


WIP

### Cable space dimensions | `tf_turn_croco_cable_space_properties()`


This function calculates the dimensions of the circular cable space in the CroCo turn and that of the cables required to properly pack into the cable space.

The required diameter of a single cable element in the turn is given by:

The full area of the circular cable space is:

The effective cable space is just the total cable space minus the central full copper cable in the middle.