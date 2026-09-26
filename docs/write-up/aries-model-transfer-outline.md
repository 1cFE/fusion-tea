# Testing whether a stellarator model could support another design

Draft supporting [the main post](fusion-tea-exploratory-modeling.md). The interpretation below is editorial synthesis; linked assessment and study records provide the evidence.

## 1. The hypothesis and the test

Our larger goal was to assess whether an AI-assisted modeling process could help us develop and evaluate engineering concepts. The hypothesis was that we could start from one documented stellarator design, abstract it into a generalized system model, and use that model to explore alternatives.

“Generalized” has a concrete meaning here. The model should separate the relationships that describe a component from the choices made for a particular plant. We should be able to change dimensions and operating conditions, select different components or materials, and change how the plant is assembled. Those are the [three kinds of design-space exploration](sysml-codegen-model-evaluation.md#11-exploring-the-design-space-parameters-components-and-architecture) the modeling strategy is intended to support.

The challenge is assessing whether those abstractions are realistic and coherent. A program can execute correctly and produce plausible numbers while describing the wrong physical system. Reproducing the design used to build the model is useful, but it does not tell us how well the model applies elsewhere.

We used a hold-out test: develop the model using one design, then assess it against a documented design we had deliberately withheld.

We chose to use Stellaris as the design point for a stellarator and intentionally withhold ARIES publications. ARIES would provide a documented alternative against which to assess generalization: could our system models represent its components and architecture, and did their physical assumptions apply? Where the quantities and definitions matched, numerical comparisons would be a stretch goal.

If the existing library was insufficient, a second part would examine what had to change to evaluate the new design. The endpoint was an explained assessment of performance and cost: what the model could calculate, how its results compared with the publication, and which differences or missing capabilities remained unresolved.

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

## 4. What changed, and what became reusable?

Adding new physics was expected once we allowed library extensions. We had only modeled a steam cycle; we did not have a model for a helium Brayton cycle. The test in Part 2 was whether we could add the missing options while retaining useful relationships and connections elsewhere in the plant.

| Design choice | Extension for ARIES | Structural result |
|---|---|---|
| Plasma density distribution | Added a hollow-profile representation and profile integration | New plasma calculations used existing reaction mathematics and passed calculated fusion power into existing fuel balances. |
| Blanket construction and coolants | Added region/material inventories and separate helium/PbLi heat accounting | Different blanket regions and heat paths could be represented explicitly, with existing capacity checks applied to their demands. |
| Power-conversion system | Added helium Brayton components: compressors, intercoolers, turbine and recuperator | Another way to convert heat into power could be assembled. This required new behavior and connections; it was not demonstrated as a drop-in replacement for the steam cycle. |
| Equipment and operating conditions | Connected selected capacities, operating demands and purchases | Existing adequacy checks and lifecycle calculations could consume the extended plant's results. |

The strongest reuse example is the plasma-to-fuel connection. The new plasma calculation produced fusion power; the existing fuel model used that power to calculate fuel demand. Raising the density by 50% increased calculated fusion power from about 1.84 to 4.13 GW and exceeded the selected exhaust-processing capacity. The existing check caught that failure without a new ARIES-specific fuel equation or automatic equipment enlargement.

**The stronger structural claim remains only partly tested.** Independent component and material choices should multiply the configurations we can explore, subject to physical compatibility. This work demonstrated particular connections and reuse, not a systematic set of substitutions between the Stellaris and ARIES assemblies. We should not count definitions and call that proven coverage of the design space.

The Stellaris baseline remained unchanged during these extensions. Evidence: [component additions, reuse and executed cases](../../work/orchestration/aries-transfer-experiment/report.md), [plant integration](../../work/orchestration/goals/aries-integrated-heat-electricity/answer.md), [equipment and cost integration](../../work/orchestration/goals/aries-integrated-equipment-costs/answer.md).

## 5. What the comparison with ARIES established

After the major component additions above, we evaluated the model against ARIES's published power balance and costs. We used explicit assumptions for unfinished physics, including magnet qualification and breeding. The purpose was to identify what explained agreement or disagreement, rather than keep adding detail until the totals matched.

- **Power balance: the disagreement was not just in the core.** We entered ARIES's reported fusion power in place of our plasma calculation to test the balance of plant separately. This exposed incorrect exchanger connections and input mappings, which we corrected. With explicit flow and equipment choices, the model then removed all the reactor heat and produced **891 MW net, versus ARIES's 1,000 MW**. The remaining difference involved heat delivery to the power cycle: we could not reconcile the published exchanger conditions with its stated turbine inlet temperature. We isolated a downstream disagreement; we did not finish quantifying core error or prove the published design wrong. [Power-balance assessment](../../work/orchestration/goals/aries-reference-heat-electricity-reconciliation/answer.md)

- **Cost: tritium-supply assumptions dominated the difference.** For that configuration, purchasing all required new tritium at the assumed price gave **$686/MWh**; assuming 100 kg/year of new supply reduced it to **$238/MWh**, against the published **$77.6/MWh**. Substituting fuel and accounting conventions closer to ARIES gave **$59/MWh at 5% real financing**. These figures are all in 2004 dollars. The comparison showed why the estimates differed, but did not independently validate cost: much of the capital came from ARIES accounts, breeding supply remained assumed, and the published financing details were incomplete. [Cost assessment](../../work/orchestration/goals/aries-reconciled-alternative-economics/answer.md)

The useful result was that we could trace a whole-plant disagreement to specific connections, physical assumptions and cost inputs. We demonstrated model extension and diagnosis, but did not reproduce the complete ARIES design. Whether the added components support a broader range of usable combinations is the subject of the next tests; the two assembled plants alone do not establish that.
