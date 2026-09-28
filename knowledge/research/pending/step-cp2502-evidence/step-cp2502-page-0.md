# Extrapolating Costs to Commercial Fusion Power Plants 

Jack Foster _[∗†]_ , Hanni Lux _[∗]_ , Samuel Knight _[∗]_ , Dan Wolff _[∗]_ , Stuart I. Muldrew _[∗]_ 

> _∗United Kingdom Atomic Energy Authority Culham Science Centre Abingdon Oxfordshire OX14 3DB, UK_ 

> _†_ jack.foster@ukaea.uk 

_**Abstract**_ **—For mega-projects like fusion power plants, modularity is a key enabler to cost and schedule efficiency e.g. [1]. One way of achieving more modularity is aiming for higher numbers of smaller fusion reactors. Previous work [2], [3] has demonstrated that the Levelised Cost of Electricity (LCOE) of commercial magnetic confinement fusion power plants falls at a decreasing rate with increasing net electric power. Furthermore, net electric power increases more rapidly than size/cost. This is because as fusion power increases the proportion of energy being exported as net electric power plateaus but the size of plant required increases linearly. Increases in plant size increase upfront capital costs and project complexity. Therefore there is an optimal design point beyond which any increases in net electric power continue to increase the project cost and complexity but deliver only marginal gains in LCOE. This helps identify a sweetspot between better economy of size and economy of scale.** _**Index Terms**_ **—Commericialization, costs, fusion power generation, fusion reactors, spherical tokamaks.** 

## I. INTRODUCTION 

Many different prototypes or demonstrator fusion power plant concepts are in their conceptual or even engineering design phases [4]–[9]. Estimates of costs of prototype/demonstrator fusion power plants and their potential commercial successors have been attempted in order to understand the potential commercial viability of specific concepts to support investment decisions into specific designs [10]–[13]. 

However, estimating costs of prototype or demonstration fusion power plants is difficult due to the often still preliminary designs combined with a non-existing supply chain for many bespoke technologies or materials. Extrapolating to commercial fusion power plants without a clear design is even harder and uncertainties are large. As a result, forecasts of commercial viability of fusion are often built on many assumptions that cannot be validated or refuted until the next set of prototype plants has been built. However, it is crucial to understand which factors impact the costs of commercial power plants to address the right validations either on prototypes or separate rigs/facilities on the path to commercialisation. Relative costs can be used to determine expected cost drivers for commercial power plants and help determine decisions that affect the balance between operational and capital costs. 

The Spherical Tokamak for Energy Production (STEP) programme is consciously designed to test the smallest scale of 

prototype fusion power plants by targeting at least 100 MW of net electric output [14]. This assures the prototype is at lowest capital costs to demonstrate electricity production and fuel self-sufficiency, but is not expected to produce electricity at commercially competitive costs. While we expect commercial power plants to have higher net electric output to have commercially viable costs, this work is exploring more the expected impact on major radius and net electric output for potentially smallest commercially viable scales. 

In Section II, we describe our methodology used in this work. In Section III, we analyse our results, and in Section IV, we draw some conclusions and assess potential next steps. 

## II. METHODOLOGY 

## _A. PROCESS_ 

PROCESS [15]–[18] is a systems code for assessing the engineering and economic viability of potential fusion power plant designs using simple 0D and 1D models of the reactor and all plant subsystems. It uses a constrained optimisation solver to find an optimal solution given a user-specified Figureof-Merit (FoM, e.g. minised major radius) while simultaneously adhering to user-selected engineering constraints and physical laws (e.g. a fixed net electric output). PROCESS does this by varying iteration variables within user-defined bounds in order to satisfy both the FoM and the constraints. The simplicity of the models within PROCESS allow for rapid iterations of power plant designs while also providing an integrated overview of the plant as a whole. The results can then be used to inform more detailed and specialised design work but needs to be interpreted within the limitations of the simple models that cannot capture all real life aspects. 

## _B. Cost Modelling in PROCESS_ 

Due to their highly integrated nature, estimating costs for fusion power plants is ideally done in the same tool as the integrated plant design is created, to allow trade offs and evaluations of all design drivers including costs to be taken into account. Subsytems and facilities could be costed independently and then totalled to give a whole plant cost but this would not capture any interdependencies between systems. For example, if the superconducting magnets and cryoplant 

