1cFE set out to understand: what would have to be true for fusion electricity to cost a cent per kilowatt-hour. Answering that means searching a large design space:
- A broad survey of 38 high-level concepts
- And then within each, running optimizations to estimate the best long-term plant configuration for long-term LCOE

1costingFE is pivotal here: it is engine that allows the user to specify end conditions (e.g. the output size of the plant), and -- given input assumptions -- calculates the characteristics (physical size, component counts) 
In this way, it functions as "inverse design": provide the target **attributes** of a system, and derive the input design **parameters**. 

This approach is highly effective when you have a good understanding of the system being modeled. But what if you wanted to iteratively evolve and develop the very system you are studying? If the *execution* of your design model depends on the viability of the plant it represents, it can actually be quite hard to rapidly reimagine the plant and pus the boundaries of its cost and performance. 

In parallel, I have been working on an alternative methodology. My goal was to more closely emulate the engineering process itself:
- Build a rough concept design, parameterized by design decisions
- Evaluate the model: cost and performance across input parameters, learning about how the system works
- Refine design concept: model additional behaviors, decompose systems into its parts, add fidelity to costing
- Evaluate, study, and repeat
For this reason, I will refer to this as *exploratory modeling*. 

The motivation: how much useful feedback can we get before we start building? Can this methodology actually advance our understanding of the system, like what engineering limitations are holding us back? And could this methodology actually allow us to discover new routes to better cost? 

This post has five parts.

1. Why SysMLv2? 
* We use SysMLv2 as the language and specification for representing the system. While there may be some residual benefits from this (like bootstrapping your systems engineering when you do build hardware), the main motivation is actually what makes it harder to work with: strict semantics. I will argue that strong patterns and established semantics are critical for fighting the natural entropy (i.e. slop) of AI. ag

* As discussed in the prior post, SysMLv2 supports very convenient patterns around composability, which can be leveraged trade studies. E.g. vary categorical decisions (Material A v B, Component C v D) in addition to numerical parameters. 

2. Model Execution and Studies
So if one motivation for using SysMLv2 was to leverage the larger community and ecosystem, why would we need to write custom model execution code? 
- First, SysMLv2 is new so when we started there really wasn't anything available. 
- Second, I had a pretty specific idea of what capabilities were needed -- and wanted to make sure they were fully accessible via command line (not hidden behind complex human-centered GUI). 

The main capability: a "study"
- Identify some output attribute(s) of interest
- Figure out what all the input design parameters are in the model
- Be able to readily set, sample and sweep the input parameters and observe the output
That's really it. If we follow the primary modeling pattern (try and reflect the actual cause-effect of the modeled system), a forward-pass evaluation should be possible. The methodology discussed in more detail should be considered a POC for model execution; it is easier to scope the SysMLv2 semantics this supports than list the semantics that aren't supported. 

3. The Full Harness
* While the term "harness" wasn't really a thing when I started, it seems like a pretty good description of what this is: a large set of tools and prompts, scaffolded by a file system and rules. The goals:
- High performance
- Reasonable token efficiency
- Stability and scalability: the overall system stays reasonably organized on its own, so that performance and efficiency is maintained as the system grows
[Img: y-axis size of repo, x-axis time. color: actively used. Left behind, potentially conflicting data: CRUD]

Our harness includes research, knowledge ingestion, a modeling workflow with PM, the model execution tools, the run-study skill. And then an over-arching "run-goal" skill. 
[Img: SysMLv2 models bubble inside a larger circle. also include the data, reasoning traces, operational records and PM]

Will show a couple of views:
- Filesystem: where to find stuff
- Logical structure: tasks, responsibilities, sequencing

4. The Demo: exploratory modeling
A reminder about our motivation: Can we advance our understanding of the system? Reveal new ideas or insights? Actually discover new routes to better cost?

This is difficult to test. Of course there is the ambition of this in a short timeframe: the team has been studying these concepts for almost a year, so helping build further intuition would be a high bar. 

But even more difficult is assessing AI's actual modeling judgement along the way. If you provide a well-defined system, the task becomes pure translation. If you start modeling a system that doesn't exist, how would we evaluate the realism (cost and viability results)? 

Our idea: try to build a hold-out set. 
  a. Provided documentation around one stellarator design point: Stellaris
  b. Strictly held out any publications related to ARIES
  c. Set goals for modeling Stellaris, and then expanding its model scope
  d. See if we could represent 




- 

Takeaways / A Foreward Outlook. 

(what does this mean for Fusion?)

* Hope this serves as inspiration:
  - SysMLv2 as a way to share data and modeling
  - Opportunity to keep pushing the cost boundary

* Would also love to hear if anyone tries putting this into practice for modeling or concept design of other physical systems

* Looking foreward, a LOT of opportunity for AI-native software systems. 
  - Models (esp GPT-6 Astra) are starting to demonstrate better "intuition" for 3d and physical systems
  - Structure + transparency & flexibility seem to be a winning combination

---

1. 
- Code is unbounded: you define your own semantics, and you are free to change those semantics on the fly. Every large piece of software has to solve 
- Our goal is modeling physical hardware/software systems. SysML and then SysMLv2 are specifications developed by really smart engineers and used broadly specifically because it is very effective as describing hardware/software systems. 



2. 
DAG limitation:
Our model execution cannot handle cycles. There are two situations where this becomes an issue: 
  1. When the "design parameters" (inputs) versus "attributes" (outputs) are not black and white. You can reasonably say A -> B -> C -> A. 
    - Workaround: reform as a constraint. Rather than A.x = f(C), have A.x, C -> D and constraint |A.x - C| < tol
    - Still not great: really collapses the feasible design region. Need help from numerical folks here
  2. Actually coupled systems. 


3. 

Process
- Set a goal ("Model X")
- Round 1: 
  - Task: Research
  - Task: Ingest knowledge
  - Task: Update model for system X
  - Task: Update model for system y
  - Study
  - Eval: goal accomplished? 
- Round 2: 
  - ...

4. 

- Example goal iteration
- Visualize models before/after
  - animation of evolution?


---

 before anyone builds anything, and the owner's framing question for this effort is: how much useful feedback can we get before building, and how can that feedback make the building count for more?

This project's answer is a machine you can ask questions of. A fusion plant is written down as text (SysML v2), compiled into a program that computes the plant's consequences in one direction (sysml-codegen generates it, teax runs it), and swept over design choices in a **study**. Every physics or engineering limit the model knows about returns a verdict at every point. Those verdicts are the feedback. When a sweep shows nothing resisting some choice, or a limit firing where the source paper says the design works, the model is telling you where it is too shallow. A **goal** is the loop in which a round agent takes such a finding and makes one bounded model change, an integration check proves the regenerated program is exactly the model, the agent re-runs the study, and an agent who did not do the work reviews the whole round before anyone builds on it.

The difference from 1costingFE, the team's own costing engine, is the direction of computation. 1costingFE decides in code what is input and what is derived, and solves fusion power backward from a net-electric target. This system computes forward from engineering choices and only asserts viability, so any lever can be swept and any limit added, at the cost of never solving for anything. The two were reconciled to one part in a million on the cost accounts, and the owner then ruled the reproduction closed so the model could grow past it.

The best evidence it works is one continuous thread on a stellarator model built from the Stellaris design paper. The model said the paper's design point needed 90.6 MW of heating against 50 installed. A goal traced the gap to how helium ash was shaped in the plasma; the sourced fix moved the requirement to 49.08 MW, on the boundary, with nothing tuned. The re-run sweep then showed most "feasible" points were ignited plasmas the model could not hold, which became the next goal and a new constraint. Nine goals and ten committed studies have run this way since late August 2026. The ARIES-CS blind comparison, the demo's biggest planned test, is still sealed.
