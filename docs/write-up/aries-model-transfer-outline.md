# Testing whether a stellarator model could support another design

Working narrative for discussion, supporting [the main post](fusion-tea-exploratory-modeling.md). [OWNER, clarified 2026-09-25] The organizing sequence is the generalization hypothesis, a brief false-start disclosure, a design-instance-only test, the required model enhancements and the resulting studies. Explanations and takeaways are proposed editorial synthesis; the linked records supply the evidence.

## 1. The hypothesis and the test

Our larger goal was to assess whether an AI-assisted modeling process could help us develop and evaluate engineering concepts. The hypothesis was that we could start from one documented stellarator design, abstract it into a generalized system model, and use that model to explore alternatives.

“Generalized” has a concrete meaning here. The model should separate the relationships that describe a component from the choices made for a particular plant. We should be able to change dimensions and operating conditions, select different components or materials, and change how the plant is assembled. Those are the [three kinds of design-space exploration](sysml-codegen-model-evaluation.md#11-exploring-the-design-space-parameters-components-and-architecture) the modeling strategy is intended to support.

The challenge is assessing whether those abstractions are realistic and coherent. A program can execute correctly and produce plausible numbers while describing the wrong physical system. Reproducing the design used to build the model is useful, but it does not tell us how well the model applies elsewhere.

Our strategy for addressing this challenge was using a hold-out set: is there a thorough publication that we could intentionally not use during an initial modeling phase; and then during a "reveal" see how well our system models generalize to the design points in the publication?

We chose to use Stellaris as the design point for a stellarator and intentionally withhold ARIES publications. ARIES would provide a documented alternative against which to assess generalization: could our system models represent its components and architecture, and did their physical assumptions apply? Where the quantities and definitions matched, numerical comparisons would be a stretch goal.

## 2. One false start before the main assessment

Our first attempt quickly exposed major violations of the intended modeling patterns. Some calculations automatically selected equipment from demand instead of evaluating the equipment supplied by the designer. We returned to the pre-reveal code, strengthened the harness instructions and ran repair goals to restore that separation.

We had already learned something from opening ARIES. We documented that exposure and tried to keep reference-specific details out of the repair goals. With that limitation recorded, we proceeded to the main assessment.

Evidence: [false start and repair basis](../../.project/active/aries-comparison-preparation/current-readiness/revealed-results/post-reveal-repair-results-note.md), [completed design-pattern repairs](../../work/orchestration/goals/preserve-model-design-choices/answer.md).

## 3. Part 1: could we assemble ARIES from the existing component library?

Think of the system as **a library of component definitions and a plant assembled from them**. A definition describes a component's behavior and limits. A plant design selects instances of those components, connects them and supplies their input values.

For Part 1, we could change the assembly, wiring and inputs. The restriction was that we had to reuse the existing definitions. Could that library support an ARIES design without adding or changing component behavior?

**The first thing that broke was the conductor calculation.** In the attempted run, the magnetic-field calculation supplied 56.6 tesla. The conductor model only supported fields between 20 and 32 tesla, so it refused to calculate a result. We did not obtain a complete plant assessment or LCOE, the lifecycle cost per unit of electricity.

That failure told us where to investigate. It did not, by itself, prove that no arrangement of existing components could work. The inspection that followed identified the actual library gaps:

- **Magnetic field:** the field approximation lacked support for the ARIES coil geometry. ARIES reported about 15.1 tesla at the coils; the attempted calculation still used inherited coil choices and was not a reconstruction of those magnets.
- **Conductor performance:** the library lacked an Nb3Sn performance model for the ARIES magnets.
- **Heat removal and conversion:** ARIES needed separate helium and liquid-metal PbLi heat paths and helium Brayton power conversion. Our existing assembly used a different cooling arrangement and steam conversion. Representing ARIES required both new component behavior and different connections.

**Part 1 failed because applicable definitions were missing or inadequate.** Changing wiring was allowed, but wiring alone could not supply those missing relationships.

Evidence: [attempt and supplied inputs](../../.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/report.md), [field investigation](../../.project/active/aries-comparison-preparation/post-reveal-investigation/findings.md), [structural and numerical assessment](../../.project/active/aries-comparison-preparation/final-assessment/report.md).

## 4. Part 2: what did we have to add, connect or assume?

We then allowed changes to the library. The question became: what work was necessary to reach an integrated ARIES-based model, and what could we reuse?

### Add missing component behavior

- Add plasma-profile calculations that could represent the hollow density distribution described for ARIES and calculate fusion power from supplied profiles.
- Add material inventories for blanket regions with different thicknesses and compositions.
- Add separate coolant heat accounting and helium Brayton components: compressors, intercoolers, a turbine and a recuperator that reuses turbine exhaust heat.
- Reuse existing fuel balances, capacity checks and applicable accounting relationships. For example, the fuel component could consume the new plasma calculation's fusion power without needing a new fuel-flow equation.

### Assemble and connect the plant

- Connect the calculations into one chain: **plasma → heat removal → power conversion → net electricity**.
- Make an upstream change propagate. Increasing plasma density should change calculated fusion power, fuel demand, heat and electricity through the actual component connections.
- Keep selected equipment fixed while calculating operating states. An exchanger that cannot remove enough heat should report a shortfall; the model should not silently enlarge it.

### Supply explicit assumptions where evidence was missing

- Use documented assumptions for quantities such as heat deposition, equipment performance and auxiliary electricity demand so the rest of the plant can execute.
- Keep unavailable magnetic and breeding checks unverified. Supplying an assumed value to a downstream calculation does not establish that the missing subsystem works.
- This distinction allowed an integrated calculation before every scientific model was complete. We did not finish replacing every missing physical relationship.

### Connect equipment and operation to cost

- Connect selected exchanger area to both heat-transfer capability and purchase cost. Connect pump capacity to purchase cost and its adequacy check.
- Calculate operating expenses from the represented demands and declared assumptions.
- Reuse financial machinery to combine capital, financing, fuel, operation, replacement and terminal costs with calculated electricity production.

The result was one connected model producing **423.1 MW net under explicit assumptions**. It was an ARIES-based scenario, not a reproduction of the published 1,000 MW plant. Cases using published source inputs still retained heat-removal failures. During this extension, the Stellaris baseline established after the earlier repairs remained unchanged, with its numerical outputs checked separately.

Evidence: [reused and added components](../../work/orchestration/aries-transfer-experiment/report.md), [thermal/electrical integration](../../work/orchestration/goals/aries-integrated-heat-electricity/answer.md), [equipment and cost integration](../../work/orchestration/goals/aries-integrated-equipment-costs/answer.md), [lifecycle calculation](../../work/orchestration/goals/aries-integrated-lcoe/answer.md).

## 5. What we learned once studies were possible

We could now study alternatives through the same integrated model. The final three studies evaluated 266 cases without changing its equations. Two examples show the difference between an equipment improvement and a result driven by an uncertain assumption. All prices below are expressed in constant 2004 US dollars.

**The equipment example was small but easy to trace.** Reducing two selected exchanger areas from 50,000 to 45,000 square metres each reduced modeled capital cost by about $17.4 million. The smaller exchangers still transferred all the required heat in the tested cases, so electricity and fuel demand were unchanged. LCOE fell by about $0.38/MWh. The saving survived the tested individual assumption changes, although missing hydraulic and detailed geometry effects prevent treating it as a purchase recommendation.

**The tritium example had a much larger effect.** The assumed baseline needed about 104.7 kg of new tritium per year after accounting for internal fuel recycling. Buying all of it at the assumed external price produced an LCOE of about $1,119/MWh. Assuming 100 kg/year of usable breeder output, with a separate $30 million/year service allowance, reduced that to about $177/MWh. The model did not establish that breeding capability or its cost; these were explicitly different supply scenarios.

That supply assumption changed which operating point looked attractive. Lowering plasma density reduced electricity from 423.1 to 349.6 MW, but also brought annual tritium demand just below 100 kg. In the assumed breeder-supply scenario, eliminating the remaining external purchases more than compensated for producing less electricity. Without breeding credit, the same lower-density case became more expensive per MWh.

The useful result was the explanation. We could identify whether a lower LCOE came from buying less equipment, producing electricity more effectively, or crossing an assumed fuel-supply threshold. Testing other assumptions showed when the ranking reversed. A lower numerical result alone would have hidden those distinctions.

Evidence: [candidate comparisons, contribution breakdowns and assumption studies](../../work/orchestration/goals/aries-integrated-design-studies/answer.md).

## 6. What this says about the modeling strategy

- **The existing library was insufficient.** We could not represent ARIES just by assembling and configuring the components we already had. Inspection identified missing or inapplicable definitions; the failed run alone was not an exhaustive test of possible assemblies.
- **The machinery supported extension.** We reused applicable relationships, added component behavior, changed the assembly and connected the resulting plant to costs. That produced an integrated model on which studies could run.
- **The studies provided useful feedback.** We could follow a design change through performance, adequacy and cost, and distinguish a small equipment saving from a much larger effect driven by an uncertain fuel-supply assumption.
- **Realism remains a separate question.** An executable integrated model and verified arithmetic do not establish actual ARIES performance. Important magnetic, breeding, equipment and economic assumptions remain unverified.

The result supports exploratory modeling as a way to develop and examine engineering models. It also identifies the work still needed before their numerical results can support a real plant recommendation.
