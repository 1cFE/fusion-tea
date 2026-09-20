# Turning a SysML model into a calculator

## 1. Introduction

We want to iterate on engineering designs quickly enough to learn from them. That means varying numerical parameters, comparing component and material choices, and changing how the system is assembled. After each change, we want to evaluate the consequences: what performance does this design deliver, what does it cost, and which engineering limits does it violate?

The [earlier post on agentic modeling](https://1cf.energy/searching-the-fusion-design-space-systematically/) described why SysML v2 is useful for representing these alternatives. This post covers the next step: turning those models into executable calculations with **sysml-codegen**, and running them with **TEAx**.

### 1.1 The model needs to support change

There are three kinds of design decisions we want to explore:

- **Parameters:** dimensions, operating conditions, efficiencies, prices, and other numerical inputs.
- **Composition:** which component or material to use, such as one magnet technology versus another.
- **Architecture:** which subsystems exist, how they are connected, and how responsibilities are divided among them.

SysML v2 gives us a useful separation between a **definition** and a **usage**. A part definition describes a reusable kind of component: its attributes, internal components, and associated calculations. A part usage places a component of that kind in a design, with its particular values and connections. A definition can itself contain usages of other definitions, so reusable components can be whole subsystems.

In our stellarator demo, the magnet model calculates field from chosen coil ampere-turns and geometry, then evaluates limits on field and conductor current. Some inputs are design parameters; others come from connected components, such as the radius supplied by the plasma model. The reusable component carries the equations, while its use in a particular plant supplies the values and connections those equations operate on.

These features matter because we want the shared engineering model to survive a comparison. Two designs can use the same component equations while differing in dimensions, material, or arrangement. Textual models also let people and agents edit, review, and version those changes with ordinary software tools.

### 1.2 Why build an execution pipeline?

When we started, we did not have an out-of-the-box SysML v2 execution tool ready for this workflow. We also wanted two specific capabilities: a simple interface for parameter-based optimization, and a way to incorporate calculations that we could not express or execute through our supported SysML subset.

Our approach is to generate a Python program from the assembled plant model. It:

- Takes the design parameters as inputs,
- Calculates the resulting performance and cost, and
- Checks the modeled engineering limits.

TEAx runs that program and lets a study evaluate it repeatedly with different parameter values.

Python also gives us access to more sophisticated computation and flexibility than we can express and execute through our supported SysML subset alone. Later, we will show how a custom calculation, such as a surrogate for a detailed simulation, can become part of the plant model.

This is a scoped execution method. The model author specifies which quantities are inputs and which are derived. The resulting calculations must have an order with no circular dependencies. The toolchain does not automatically rearrange equations or construct a solver for mutually dependent quantities.

### 1.3 From component models to a study

The engineer or agent authors reusable component models and assembles them into a plant. In our workflow, agentic-mbse provides modeling guidance and checks, including the conventions needed by this execution pipeline. The components capture their inputs, outputs, mathematical relationships, and constraints; the assembled design supplies values and binds components together.

Once the plant is assembled, sysml-codegen works through each component used in the design and identifies its calculations and constraints. For every calculation input, it determines whether the value comes from a supplied design parameter or another calculation’s output. It then generates the Python calculations and the instructions TEAx needs to pass values between them. Parameters that must be supplied to run the plant become the generated program’s input interface—the values a study can vary.

![Model changes regenerate the program; parameter studies reuse the generated stellarator program.](sysml-codegen-assets/iteration-overview.png)

A study repeats the evaluation with different input values. The stellarator study we will examine varies major radius and coil ampere-turns, calculating electricity cost and checking engineering limits at each point. A change to component composition or architecture generally means editing the SysML and generating a new package; a numerical sweep reuses the existing package.

The worked example follows our stellarator demo through seven steps:

- **2.1 Model a component:** separate the magnet's reusable equations from the values and connections chosen for the plant.
- **2.2 Define acceptable designs:** express engineering limits as constraints that each design point must pass.
- **2.3 Construct the calculation network:** determine where every calculation gets its inputs and which other calculations it depends on.
- **2.4 Implement the mathematics:** translate equations into Python and incorporate custom methods, including a simulation surrogate.
- **2.5 Change the component model:** give the blanket a more detailed calculation while keeping its place in the plant.
- **2.6 Assemble the executable program:** connect the Python calculations with TEAx and expose the inputs a study can vary.
- **2.7 Run a study:** evaluate many design points and compare their feasibility and cost.

All code examples come from the stellarator demo. Excerpts omit surrounding imports and documentation where indicated.

## 2. Process: a worked example

### 2.1 Modeling a component: separate its equations from the plant's choices

To compare magnet designs, we need to change the chosen dimensions and operating parameters without rewriting the equations each time. We also need the magnet to use the same plant geometry as the other components. The component model therefore holds the calculation method, while the assembled plant supplies the design choices and connections.

In the stellarator, the reusable `'Magnet System'` definition groups the coil, winding pack, and casing with their field, geometry, conductor-quantity, and cost calculations. We will follow one of those calculations: the magnetic field produced by the chosen coil ampere-turns and geometry.

There are four pieces to read together in the figure below. The **calculation definition** declares the equation and its inputs. The **plant** supplies values to the coil, including a connection to the plasma's radius. The **calculation usage**, named `field_calc`, binds those coil attributes to the equation's inputs. Finally, the magnet exposes the equation's output, `B_axis`, as an attribute named `B`, which other components can use.

![Plant values and the shared plasma radius feed the coil attributes; field_calc binds those inputs to the Coil Set Axis Field equation, and the magnet exposes the computed B_axis as B.](sysml-codegen-assets/stellarator-component.png)

*Sources: the [calculation definition](../../models/library/analyses/mfe_magnet_field.sysml), [magnet component definition](../../models/library/cost_structure/mfe_power_core.sysml), [generic plant connections](../../models/designs/generic_mfe/mfe_plant.sysml), and [stellarator design values](../../models/designs/stellarator_09/stellarator_plant.sysml). Documentation and unrelated members are omitted. The calculation usage and exposed attribute belong inside `'Magnet System'`; the radius connection is inherited from the generic plant.*

The equation calculates axis-averaged magnetic field from coil count, ampere-turns, major radius, and a held linkage factor. `mu0` is vacuum permeability; `two_pi` is twice π. Their declared defaults supply the two inputs that the usage leaves unbound.

The plant supplies 48 coils and 15.4 million ampere-turns at the reference point. Its inherited radius connection makes `coil.R0` read `plasma.R`, rather than giving the coil a separate radius to maintain. The usage then binds its `R0` input to `coil.R0`. Following that chain shows how a plant-level choice reaches the equation.

Here `I_coil` denotes ampere-turns for the reference coil; current in an individual conductor is checked separately. The linkage factor holds the reference coil set's field transfer, making this a reference-scaled approximation rather than a full three-dimensional magnetic-equilibrium calculation.

The final attribute declaration makes the result available as the magnet's `B`. Downstream calculations use it for peak conductor field and plasma beta, which compares plasma pressure with magnetic pressure. Changing a shared input propagates through those modeled relationships.

### 2.2 Constraints test whether a design point meets engineering limits

As we will see in the studies, we can vary plant input variables such as radius and coil ampere-turns and evaluate different combinations. Each complete set of input values defines a **design point**. The calculations tell us what field, performance, and cost that point produces. How do we determine whether it is feasible?

We express engineering limits as **constraints**: expressions that evaluate to true or false for the design point. A constraint can compare a calculated quantity with a limit, or relate several quantities that must be consistent with one another. For example, the current required by a design must not exceed the conductor's allowable current. The current calculation produces a value; the constraint tests whether that value meets the requirement.

In SysML, an `assert constraint` applies such a condition to the model. During evaluation, the generated program checks it using that design point's values. A point passes the modeled feasibility checks only when all applicable asserted constraints have been evaluated and satisfied. Changing inputs can therefore improve cost while causing a constraint to fail, which is precisely the tradeoff we want a study to reveal.

The recent stellarator work provides a concrete example: does the winding pack fit inside the space allocated to it?

The magnet's `'Winding Pack Casing Fit'` calculation takes the calculated pack size, insulation and assembly allowances, wall thickness, and available cavity dimensions. It returns the clearance in two directions and the smaller of those margins. The magnet exposes that result as `fit_minimum_margin`.

The [constraint definition](../../models/library/analyses/mfe_winding_pack_fit.sysml) is short:

```sysml
constraint def 'Winding Pack Fits Casing' {
    in attribute minimum_margin_in : Real;
    minimum_margin_in >= 0.0
}
```

The stellarator plant applies it to its magnet:

```sysml
assert constraint wp_fit_ok : 'Winding Pack Fits Casing' {
    in minimum_margin_in = magnet.fit_minimum_margin;
}
```

The calculation determines how much space remains. The assertion judges the result. A negative finite margin is a valid evaluation of a design that fails the check; it does not crash the study or automatically enlarge the casing. That distinction lets us inspect the cost and other consequences of an unacceptable design.

This check represents a local, aligned rectangular section of the pack and cavity. It does not establish that an entire nonplanar coil can be manufactured or assembled. Similarly, a point that passes every modeled constraint has passed those particular checks. It has not acquired evidence for physical limits the model does not yet represent.

The pipeline executes supported `assert constraint` forms using the same dependency machinery as calculations. Other constraint forms remain cataloged with their execution disposition. Results report which assertions were assessed, so unassessed checks cannot silently count as passes.

### 2.3 Reconstructing the calculation network

We have described calculations and checks inside components, and connected those components in the plant. To evaluate a design point, the program must turn those connections into an order of work. It cannot check winding-pack clearance until it knows the pack dimensions, and it cannot calculate those dimensions until it knows the required conductor inventory.

SysML organizes the model around physical components. Codegen constructs a second view organized around calculations: each calculation is a node, and a connection from one calculation's output to another's input is an edge. This is the **computational graph**. It tells the execution system which results must be available before a calculation can run. The following figure shows the magnet branch of the generated stellarator graph.

![Actual magnet calculation dependencies: field feeds sizing; pack dimensions feed fit and material costs; separate checks assess field, current, and fit.](sysml-codegen-assets/stellarator-calculation-graph.png)

*Each arrow represents a direct output-to-input binding in the generated TEAx specification. Multiple values exchanged by the same pair of modules share an arrow. Secondary inputs and other plant branches are omitted. These connections also match the saved pipelines for both studies discussed below. The procurement module reports winding quantities and cost; its tape and conductor lengths feed the current-margin calculation. Its cost is not total plant cost. [Exact nodes, connections, and package identities](sysml-codegen-assets/graph-evidence.md).*

Read the graph from the top. The axis field and radial build determine the peak conductor field. The current-sizing calculation determines the required conductor inventory from that field and the material assumptions, then selects either current-based or legacy sizing according to the chosen mode. The selected effective current density and the chosen ampere-turns determine the winding-pack side length.

The pack size then feeds two branches. One checks whether the pack fits. The other calculates volume, material inventory, and procurement cost. A separate calculation checks conductor-current margin from the realized inventory. The assertions consume those results; they do not change the candidate's dimensions to force it to pass.

Codegen constructs this network in three steps.

#### 2.3.1 Parse declarations and references

SysIDE parses the SysML files into an abstract syntax tree: objects representing the declarations, mathematical expressions, and their relationships. It also resolves references to declarations. For `coil.I_coil`, the parser identifies the coil feature and the attribute it refers to. Codegen does not search the source text for a matching spelling.

A declaration in a reusable definition still needs a location in the assembled design. The field calculation belongs to the magnet definition; evaluating this plant means applying it specifically inside `stellaris.magnet`.

#### 2.3.2 Expand the assembled design

Parsing tells codegen what a definition contains. It must next determine where that definition is used and which values apply there. Codegen walks the assembled component hierarchy, selects the definitions and redefinitions that apply at each location, and creates records for the values and calculations there. For this plant, those records include the magnet's field calculation, pack-sizing calculation, casing dimensions, and constraint evaluations.

Each location in the assembled component hierarchy is an **occurrence**. Codegen identifies a value or calculation by that occurrence together with the member it represents. A redefined attribute remains the same logical feature, with the effective assignment selected for that occurrence. Arrayed components are expanded into separate occurrences with separate value records.

That preserves both kinds of relationships we need: independent components can have independent values, while several calculations connected to one plant attribute still share that value.

#### 2.3.3 Resolve each input to its supplier

With those records in place, codegen can connect each calculation input to the value it needs. It has to distinguish two cases: a value supplied externally, such as the chosen plant radius, and a result that another calculation must produce first.

For each reference, codegen uses the declaration identified by the parser together with its path through the assembled components. That combination identifies the particular attribute or calculation output being read. If an attribute refers to another attribute or output, codegen follows that connection to the supplier. It creates the records before resolving the connections, so a supplier can appear later in the source file.

The field calculation's radius input provides a concrete example. Its SysML binding names `coil.R0`; the assembled plant binds that quantity to `plasma.R`. The generated field calculation therefore reads the public plasma-radius input directly. It does not create a second independently adjustable radius for the coil.

The pack-sizing calculation provides the other case: its effective current density comes from the current-sizing calculation. Codegen records an edge to that output. There is no extra user input standing in for the computed density.

A missing or ambiguous supplier stops generation with a diagnostic. A failed reference lookup must not become an extra study parameter. Once these connections are resolved, codegen assigns public names and renders the executable modules and wiring.

### 2.4 Turning modeled mathematics into executable Python

The graph tells us which calculations are needed and how they depend on one another. Each calculation also needs executable code that turns its input numbers into output numbers. For equations written in the supported SysML expression language, codegen generates that code directly, so the author does not have to maintain a second copy of the equation in Python.

Consider the magnetic-field equation from section 2.1. SysIDE represents its arithmetic as nested operations: multiply the numerator's terms, multiply the denominator's terms, then divide. Codegen visits those operations and writes the equivalent Python expression. References to the calculation's inputs become fields on an input object. The [generated function](../../exploration/stellarator_e2e/generated/handwritten/mfe_magnet_field/coil_set_axis_field_impl.py) returns:

```python
return ((((inputs.mu0 * inputs.k_link) * inputs.n_coils) * inputs.I_coil)
        / (inputs.two_pi * inputs.R0))
```

Only the line break has changed for readability. A generated wrapper validates the inputs and returns the result in the form TEAx expects. More involved expressions can have intermediate values, ordered before the outputs that use them.

The compiler supports a subset of SysML mathematics. Unit annotations do not become an automatic numerical unit-conversion system; the authored model and implementations must use consistent quantities.

#### 2.4.1 Incorporating calculations beyond the expression translator

Some engineering calculations need numerical algorithms, external libraries, or a fast approximation to an expensive simulation. We can supply a Python function for those methods while keeping their inputs, outputs, and plant connections in SysML. TEAx can then call a custom function through the same interface as a translated equation, and the study can evaluate both as part of one plant program.

The stellarator's winding-pack sizing shows a small use of this option: adding explicit input checks around a simple equation. Its [handwritten implementation](../../exploration/stellarator_e2e/generated/handwritten/mfe_magnet_field/winding_pack_sizing_impl.py) rejects negative or non-finite ampere-turns and requires a finite, positive current density before calculating the pack size:

```python
def run_winding_pack_sizing(inputs: Winding_Pack_SizingInput) -> float:
    """Size finite nonnegative amp-turn magnitude at finite positive A/mm²."""
    if not math.isfinite(inputs.I_coil) or inputs.I_coil < 0:
        raise ValueError("Winding Pack Sizing: I_coil must be finite and nonnegative")
    if not math.isfinite(inputs.j_wp) or inputs.j_wp <= 0:
        raise ValueError("Winding Pack Sizing: j_wp must be finite and positive")
    return (((inputs.I_coil / inputs.j_wp) ** 0.5) / 1000.0)
```

The square root converts required cross-sectional area into a side length; dividing by 1,000 converts millimetres to metres. TEAx calls this function just as it calls the automatically translated field equation.

The blanket model shows why this flexibility matters for a study. We want to vary blanket thickness and estimate how much tritium the blanket breeds. Running a detailed neutron-transport simulation for every candidate would make that evaluation much more expensive. Instead, the model uses a [response table from prior neutron-transport calculations](../../models/designs/stellarator_09/breeding_response.json). A [handwritten Python function](../../exploration/stellarator_e2e/generated/handwritten/mfe_tritium_breeding/blanket_tritium_breeding_impl.py) estimates the response between the stored results by interpolation. That function is a **surrogate**: a cheaper approximation to the detailed simulation, which the plant can call at each design point.

This is a table-based surrogate, with five thickness nodes spanning 0.60–1.00 m under fixed remaining geometry and scenario assumptions. The implementation checks that its inputs stay within that scope and marks the response undefined outside it. It is not a trained machine-learning model or a full shaped-stellarator transport solution. Another surrogate method could occupy the same kind of calculation interface, with its own validity checks.

For a calculation whose expression cannot be translated, codegen can generate the function interface with a placeholder body. That body raises `NotImplementedError` until someone supplies the method. The declared inputs and outputs give the implementation a defined place in the plant's calculation network; broken plant wiring still blocks generation.

Both translated and custom implementations live under `handwritten/`. Preservation options can keep an existing body when its interface is unchanged, even if the SysML equation has changed. Generating a fresh package updates translated equations; retaining implementations requires checking them against the revised model.

### 2.5 Changing a component's calculations without rebuilding the plant

Changing a parameter only explores relationships the model already contains. If tritium breeding is represented by a fixed assumption, varying blanket thickness cannot tell us how breeding changes. We need to change the blanket model itself to add that relationship.

This is where the separation between definitions and usages helps. The generic plant already contains a blanket, with a place and connections in the plant. We can define a more detailed kind of blanket that inherits the common structure and adds the transport-based calculation from section 2.4. Then the stellarator design selects that definition for its blanket. The surrounding plant can continue referring to the same component.

The three declarations below express those choices. They come from separate source locations; the bodies are omitted:

```sysml
// Generic plant: the inherited component usage
part blanket : 'Blanket' {
    // ...
}

// Specialized component definition
part def 'Transport Calculated Blanket' :> 'Blanket' {
    // ...
}

// Stellarator design: select the specialization
part :>> blanket : 'Transport Calculated Blanket' {
    // ...
}
```

The first declaration places a blanket in the generic plant. In the second, `:>` means that the new definition extends the base blanket. In the third, `:>>` selects that more detailed definition for the blanket the stellarator inherits. Its breeding result now comes from the surrogate calculation instead of a held value. [Generic plant](../../models/designs/generic_mfe/mfe_plant.sysml), [specialized blanket](../../models/designs/generic_mfe/mfe_subsystems.sysml), [stellarator selection](../../models/designs/stellarator_09/stellarator_plant.sysml).

After this model change, we regenerate the program. Codegen includes the selected blanket's calculation and connects it to the plant, so a subsequent study can evaluate its response to thickness. This example changes the detail of a component model. Changes to plant architecture use the same edit-and-regenerate process, adding or removing component usages and changing their connections.

### 2.6 Putting together the Python computational model

At this point, codegen has identified the calculations, resolved their dependencies, and supplied Python implementations. To run the whole plant, we need to connect those functions and provide the values that do not come from another calculation. The generated package captures both: a TEAx specification describes the connections, and input files hold the externally supplied parameters.

#### 2.6.1 Wiring the functions into an executable calculation network

A Python function for winding-pack size knows how to calculate a size from current density and ampere-turns. It does not decide which plant values to use. Codegen writes those choices into a YAML specification using the connections resolved in section 2.3. TEAx reads that specification to assemble and run the program.

Here is the complete pack-sizing entry from the stellarator pipeline:

```yaml
stellarator_09__stellaris__magnet__wp_sizing:
  module_type: mfe_magnet_field.Winding_Pack_SizingModule
  inputs:
    j_wp: float stellarator_09__stellaris__magnet__current_sizing__selected_effective_density
    I_coil: float stellarator_plant_params.stellarator_09__stellaris__magnet__coil__I_coil
  outputs:
    root: RootModel[float] stellarator_09__stellaris__magnet__wp_sizing__wp_side
```

The long names encode where each value belongs. The `j_wp` input reads a calculation output: the density selected by current sizing. The `I_coil` input reads a field in the external plant-parameter group. The output has a channel name identifying this magnet's calculated pack side; `root` holds the scalar inside its typed wrapper. [Generated pipeline](../../exploration/stellarator_e2e/generated/pipelines/pipeline.yaml).

TEAx uses these connections to order the modules so every producer runs before its consumers. For each module, it gathers the bound inputs, calls the implementation, and makes its outputs available to downstream calculations. It computes field before current-based sizing, sizing before pack dimensions, and dimensions before the fit check.

The model can remain organized into physical systems and subsystems for authoring. The generated program already has the connections it needs, so evaluation does not repeatedly interpret that component hierarchy.

#### 2.6.2 Exposing the free input parameters

The connected calculations still need starting values. In our example, the program calculates magnetic field, but the study supplies radius and coil ampere-turns. These externally supplied values form the program's input interface. Changing them lets us evaluate a new design point without regenerating the program.

Codegen finds these inputs while resolving the graph. It keeps a value connected to its producing calculation when one exists. When a calculation instead reads a plain attribute, such as the plasma radius, codegen exposes that supplying attribute as a public input. Several calculations that read the same attribute share the same input.

The authored values provide the initial settings. A literal bound directly to a calculation input is also exposed with that literal as its initial value. A calculation input left unbound becomes a public input with its supported modeled default, or a `null` placeholder that must be filled before evaluation. An unresolved reference is an error, as described in section 2.3; it does not become a new free parameter.

Here is an exact subset of the stellarator's generated plant-input JSON:

```json
{
  "stellarator_09__stellaris__plasma__R": 12.7,
  "stellarator_09__stellaris__magnet__coil__I_coil": 15400000.0,
  "stellarator_09__stellaris__magnet__coil__n_coils": 48.0,
  "stellarator_09__stellaris__magnet__coil__k_link": 0.7731331164622419
}
```

The field calculation takes these inputs, along with its library constants, and produces `B_axis`. There is no independent field input replacing that calculation. Changing radius updates every calculation connected to the same modeled radius. [Full generated input file](../../exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json).

Inputs are grouped into files, normally by their declaring model source. The keys inside each file are flat, with names that preserve component paths. The JSON does not reproduce the nested component tree. Schemas describe the types and defaults; file-based runs load the JSON, while studies can supply the typed values in memory.

Being exposed is not the same as being a sensible design variable. A study selects which inputs to vary and which assumptions to hold. For the radius–current study, the linkage factor and coil count remain fixed. The study changes radius and ampere-turns rather than treating every available input as a design freedom.

### 2.7 Running a study: compare feasibility and cost across design points

We can now use the generated program to ask an engineering question: which combinations of geometry and operating parameters meet the modeled limits, and what do they cost? A **study** evaluates a set of design points against the same generated plant program. It chooses which inputs to vary, which assumptions to hold fixed, and which results to compare.

For the radius–current study, the varied inputs include `stellarator_09__stellaris__plasma__R` and `stellarator_09__stellaris__magnet__coil__I_coil`. The study reads the electricity-cost output, `stellarator_09__stellaris__lcoe_calc__lcoe`, alongside the constraint results. For each candidate, the radius and ampere-turns flow through the connected calculations, producing both a cost estimate and a record of which checks passed or failed.

TEAx prepares the evaluator once by loading the generated package and building its execution graph. Each candidate supplies a new input set and runs with a fresh execution context. Numerical outputs and constraint results return in memory. The study layer records the inputs, results, assessment, and model identity in a persistent store. It does not need to rewrite and reread JSON files for every candidate.

The existing study strategies evaluate grids and prepared lists of candidates. An external optimizer can call the same prepared evaluator; adaptive optimization within the native study runner requires further implementation. A different component composition or architecture requires a newly generated model variant, as described in section 2.5.

The following figures use retained results from two recent stellarator studies. They are **dated model snapshots**, illustrating the evaluation workflow. Their electricity costs reflect the assumptions and incomplete cost scope at that time; later breeding, cooling, and facility work changed the checks and cost estimates.

#### 2.7.1 See how a local change affects the rest of the design

The [15 September joint magnet-sizing study](../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/report.md) examined conductor inventory and available space together. Three matched reference cases show why evaluating the complete dependency chain matters:

![Three recorded stellarator cases: current sizing raises cost and fixes current capacity; enlarged space fixes fit but violates the field limit.](sysml-codegen-assets/stellarator-magnet-tradeoff.png)

*Recorded native results from one study package. The second case enables current-based sizing with a 1% physical inventory reserve; the third also enlarges the radial allocation and transverse cavity. Every case retains a divertor heat-load failure. [Extracted values and original case identities](sysml-codegen-assets/magnet-sizing-comparison.csv).*

The original conductor inventory fails the current-capacity check, and the pack does not fit the assumed casing interior. Sizing the inventory to carry the required current fixes the first problem but increases pack size and cost. Enlarging the allocated space fixes the fit problem, but the changed radial geometry raises peak conductor field to 25.30 T, above the retained 24.9 T limit.

Those are connected consequences of the model's equations. The study does not copy the cost or fit logic into its own script, and the constraint checks do not conceal a failure by changing the design. We can see what a proposed fix buys and what it makes worse.

#### 2.7.2 Map feasibility and cost together

The [17 September neighborhood study](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/report.md) varied geometry and operating choices, then evaluated a two-dimensional slice at fixed settings for the other parameters. The axes are major radius and coil ampere-turns. Each mark below is one native evaluation.

![Stellarator radius–ampere-turn map showing 44 passing samples, 210 failing samples, two invalid power accounts, and the conditional electricity cost at valid points.](sysml-codegen-assets/stellarator-feasibility-cost.png)

*This slice contains 256 samples: 44 pass all twenty then-implemented checks with a valid power account, 210 fail at least one check, and two have invalid power accounts. The passing samples span $149.77–152.36/MWh under that snapshot's cost assumptions. Circles identify passing samples in both panels; crosses retain failing results. No feasible region has been interpolated between the points. [Plot data](sysml-codegen-assets/feasibility-cost-map.csv).*

The passing samples form a narrow band. At fixed ampere-turns, reducing radius increases the modeled field and can violate its limit. Increasing radius reduces field and changes the plasma power balance, eventually running into divertor heat or installed-heating limits. The cost plot explains why minimizing price alone would not answer the design question: low calculated costs also occur at points that fail engineering checks.

For this slice, minor radius is held at about 1.491 m, peak ion temperature at 14.036 keV, and peak electron density at 4.892 × 10²⁰ m⁻³. The scenario also holds eighteen representative helium loops, 0.65 m radial allocation and transverse cavity, and a 1.01 conductor-inventory multiplier. The [study record](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/record.md) preserves the full-precision inputs and other held assumptions. These selected samples do not establish a global optimum or the fraction of the whole design space that is feasible.

That is the practical link back to rapid iteration. A model change alters the calculations or checks available to the next study. A parameter change asks a new question of the existing executable model. The recorded results show which decisions improve cost, which constraints resist them, and where the engineering model needs more work.

## 3. Sources and figure data

- [Original agentic-mbse post](https://1cf.energy/searching-the-fusion-design-space-systematically/): motivation and the modeling workflow.
- [Codegen pipeline](https://github.com/1cFE/sysml-codegen/blob/main/docs/architecture/reference/00-pipeline-overview.md) and [TEAx evaluation and studies](https://github.com/rwestwood89/teax/blob/main/docs/evaluation-and-study.md): execution architecture.
- [Stellarator code excerpts and source hashes](sysml-codegen-assets/model-evidence.md): field, winding fit, handwritten calculations, and blanket specialization.
- [Graph extraction](sysml-codegen-assets/graph-evidence.md): exact generated connections and comparison against both frozen study pipelines.
- [Study extraction](sysml-codegen-assets/study-evidence.md): selected cases, fixed assumptions, data joins, source hashes, and later-model qualifications.
- [Figure sources and regeneration instructions](sysml-codegen-assets/README.md): PNG and SVG files, plotting code, and retained data.

<!-- Editorial provenance: The owner supplied the purpose and story in the drafting conversation and requested all examples be drawn from the stellarator demo. Three subagents verified code, graph, and study evidence for this revision on 2026-09-19. The graph and code excerpts use current local sources; study numerical claims use the named immutable record artifacts. This revision extracts and plots existing runs; it does not claim new physical qualification or a new study execution. -->
