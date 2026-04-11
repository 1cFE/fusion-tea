# Phase 2 Concept: Formulating the AND/OR Graph

Working document — brainstorming different framings, self-evaluating, converging.

---

## What Phase 1 Tells Us (Constraints on Phase 2)

The flat table has ~2 effective degrees of freedom (concept + fuel). Three tightly coupled clusters (Confinement-Heating-Plasma, Fuel-Neutron-Energy, Driver-Hardware) account for most of the constraint structure. The table describes WHAT each concept chose but not WHY. Within-family differentiation fails — the table can't distinguish what makes CFS different from Tokamak Energy, or Xcimer different from Focused Energy.

**The deeper issue**: Every cell in the table is an ANSWER to a question, but the table only records the answer. "Magnet Type: HTS (wound)" is the answer to *some* question — but what question? For CFS, the question is "how do you generate a 20 T toroidal field in a compact volume while leaving space for a breeding blanket?" For Thea Energy, the question is "how do you produce the complex 3D field topology of a stellarator with coils simple enough to manufacture?" Same column, same answer category, completely different problems being solved.

The flat table strips away the problems and keeps only the solution labels. Any AND/OR graph worth building should restore the problems.

---

## Three Framings

### A. Subsystem Decomposition (Baseline)

**What the nodes represent**: Physical subsystems and technology choices.

**Structure**:
```
Fusion Power Plant [AND]
├── Plasma Core [AND]
│   ├── Confinement [OR]: Tokamak | Stellarator | FRC | Mirror | ...
│   ├── Heating [OR]: RF (ICRH) | RF (ECRH) | NBI | Ohmic | Laser | ...
│   └── Fueling [OR]: Pellet injection | Gas puffing | NBI fueling | ...
├── Nuclear Island [AND]
│   ├── Blanket [OR]: FLiBe | LiPb | Solid ceramic | Liquid Li | ...
│   ├── Shield [OR]: Integrated blanket/shield | Separate shield | ...
│   └── Tritium System [OR]: Bred | Self-bred | N/A (aneutronic) | ...
├── Power Conversion [AND]
│   ├── Energy Capture [OR]: Thermal (steam) | Thermal (sCO2) | Direct | Hybrid | ...
│   └── Generator [OR]: Steam turbine | sCO2 turbine | Direct converter | ...
└── Balance of Plant [AND]
    ├── Cooling [OR]: Wet cooling | Dry cooling | ...
    ├── Maintenance [OR]: Remote (full) | Remote (partial) | Hands-on | ...
    └── Site & Civil [AND]: ...
```

**Example — CFS compact tokamak**:
- Confinement → Tokamak (compact, high-field)
- Heating → RF (ICRH)
- Blanket → FLiBe
- Energy Capture → Thermal (steam)
- (etc.)

**What this captures**: The physical decomposition of the plant. Maps naturally to CAS cost accounts and WBS. Familiar to engineers. The tree structure makes N/A patterns explicit — if you're not MFE, the "Divertor" sub-node doesn't appear.

**What it misses**: This is the flat table reformatted as a tree. The nodes are still categories. "Blanket → FLiBe" tells you the same thing as "Tritium Breeding: FLiBe blanket" in the table. You've gained explicit structure (which helps) but haven't gained any understanding of WHY.

**Self-evaluation**:
- For understanding: Marginal improvement. You can see the tree structure, but you already knew it from Phase 1b_v2.
- For generation: No improvement. You're still combining categories, and we showed in Phase 1d that random combination doesn't work.
- For transfer: Slightly better — you can see which subsystems are shared across concepts. But the match is on LABELS, not on PROBLEMS, so the transfer justification is weak.

**Verdict**: Useful as a baseline to compare against. Not sufficient on its own. The main value is establishing the skeleton that richer approaches can hang information on.

---

### B. Primitive-Requirement Decomposition (Problem-First)

**Core idea**: Every fusion power plant, regardless of approach, must satisfy the same set of *primitive requirements* — invariant conditions that physics and economics impose. These primitives are the universal "questions." The AND/OR graph decomposes them, and the decomposition diverges based on concept choices.

**What the nodes represent**: PROBLEMS at AND nodes. SOLUTIONS at OR nodes. Every node carries a problem statement with context — not just "breed tritium" but "maintain a tritium breeding ratio >1.0 in a toroidal geometry with 14.1 MeV neutron flux from a compact D-T plasma, given that the blanket must share space with HTS magnets requiring <100°C operating temperature."

**The primitives** (every concept must address all of these):

| Primitive | What it demands | Why it's universal |
|---|---|---|
| **P1: Achieve fusion conditions** | Sufficient temperature, density, confinement | Can't make a fusion plant without fusion |
| **P2: Achieve net energy gain** | Q_eng > 1 after all recirculating power | Can't sell energy you don't produce |
| **P3: Convert energy to deliverable form** | Electricity, process heat, or neutrons | Must deliver a product |
| **P4: Sustain operation** | Not a one-shot; fuel supply, component life | Must run continuously or repeatedly |
| **P5: Manage nuclear environment** | Radiation, activation, waste, safety | Physics creates nuclear byproducts |
| **P6: Be economically competitive** | LCOE at or below alternatives | Must compete in energy market |
| **P7: Be licensable and buildable** | Regulatory, manufacturing, supply chain | Must actually get built |

**Structure**:
```
Viable Fusion Power Plant [AND of all primitives]
│
├── P1: Achieve Fusion Conditions [AND]
│   ├── Reach ignition temperature [context-dependent sub-problem]
│   │   D-T: T_i > 10 keV (relatively accessible)
│   │   p-B11: T_i > 100-300 keV (extreme, cross-section peak ~600 keV)
│   │   D-He3: T_i > 50 keV (intermediate)
│   │
│   ├── Achieve sufficient confinement [context-dependent]
│   │   MFE: n·τ_E·T > Lawson criterion → need τ_E ~ seconds at n ~ 10²⁰/m³
│   │   IFE: ρR > ignition threshold → need extreme compression, driver energy
│   │   MIF: intermediate — magnetized target, lower requirements on both
│   │
│   └── Maintain plasma stability [context-dependent]
│       Tokamak: disruptions, ELMs, current drive
│       Stellarator: no disruptions (advantage), but 3D optimization
│       FRC: tilt/shift instabilities, beam-driven stabilization
│       Z-pinch: MHD instabilities, sheared-flow stabilization
│       IFE: implosion symmetry (Rayleigh-Taylor instabilities)
│
├── P2: Achieve Net Energy Gain [AND]
│   ├── Fusion power sufficient [depends on P1 + fuel + volume]
│   ├── Driver/heating efficiency [context-dependent]
│   │   RF: wall-plug to plasma coupling ~50-70%
│   │   NBI: ~30-40%
│   │   Laser: ~5-15% (dominant IFE challenge)
│   │   Compression: mechanical → plasma coupling ~??%
│   ├── Recirculating power fraction manageable [depends on all above]
│   └── Energy multiplication adequate [depends on fuel + blanket]
│       D-T with blanket: M_n ~ 1.1-1.3 (neutron multiplication in blanket)
│       Aneutronic: no multiplication, direct conversion efficiency dominates
│
├── P3: Convert Energy [OR — major branch point]
│   ├── Thermal conversion [selected by: D-T, D-D, most MFE/IFE]
│   │   AND: {heat capture → working fluid → turbine → generator}
│   │   Sub-OR: Steam Rankine | sCO2 Brayton | He Brayton
│   ├── Direct conversion [selected by: aneutronic, some D-He3]
│   │   AND: {charged particle collection → voltage generation}
│   │   Sub-OR: Electrostatic decel | Inductive capture | Traveling wave
│   └── Hybrid [selected by: some D-He3, some p-B11 with side neutrons]
│       AND: {thermal for neutron energy + direct for charged particles}
│
├── P4: Sustain Operation [AND]
│   ├── Fuel supply [context-dependent]
│   │   D-T: MUST breed tritium (no natural source) → creates P4a
│   │   D-He3: He3 sourcing (moon mining? DD side reaction?) → creates P4b
│   │   p-B11: commercially available fuels → trivial
│   │   D-D: commercially available → trivial
│   │
│   ├── P4a: Tritium breeding cycle [AND, D-T only]
│   │   ├── Breeding blanket [OR]: FLiBe | LiPb | Solid breeder | Liquid Li
│   │   ├── Tritium extraction from blanket
│   │   ├── Tritium processing & storage
│   │   └── Achieve TBR > 1.0 (accounting for burnup, losses, decay)
│   │
│   ├── Component longevity [context-dependent]
│   │   D-T: neutron damage dominates → DPA limits on first wall/blanket
│   │   Aneutronic: no neutron damage → thermal/mechanical fatigue instead
│   │   IFE: repetitive shock loading → chamber survival
│   │
│   └── Repetitive operation [if pulsed]
│       IFE: target fabrication + injection + chamber clearing at rate
│       MIF: target reset + compression system cycling
│       Pulsed MFE (Z-pinch, FRC): electrode/coil cycling
│
├── P5: Manage Nuclear Environment [AND, severity depends on fuel]
│   ├── Radiation shielding [context-dependent]
│   │   D-T: 14.1 MeV neutrons → heavy shielding (1-2 m)
│   │   D-D: 2.45 MeV neutrons → moderate shielding
│   │   Aneutronic: minimal → mostly secondary reactions
│   ├── Activated material handling
│   ├── Waste classification & disposal
│   └── Personnel & public safety (ALARA, emergency planning)
│
├── P6: Be Economically Competitive [AND]
│   ├── Capital cost [depends on everything physical]
│   ├── O&M cost [depends on P4, P5]
│   ├── Availability [depends on component life, maintenance approach]
│   ├── Plant lifetime [depends on P5]
│   └── Financing [depends on risk, regulatory, market]
│
└── P7: Be Licensable and Buildable [AND]
    ├── Regulatory pathway [depends on P5]
    ├── Manufacturing capability [concept-specific]
    │   Tokamak: HTS coil winding, vacuum vessel fabrication
    │   Stellarator: 3D coil fabrication (unique challenge)
    │   IFE: target mass production at cost
    │   MIF: liquid metal handling systems
    ├── Supply chain [depends on exotic materials, magnets, lasers]
    └── Siting [depends on P5, cooling, grid connection]
```

**Worked example — how CFS vs. TAE diverge on P1**:

CFS (D-T compact tokamak): "Achieve fusion conditions" decomposes into:
- Reach T_i > 10 keV → achievable, tokamak physics well-understood
- Achieve n·τ_E at 10 keV → compact + high field → good confinement in small device
- Maintain stability → disruption risk managed by SPARC experience; ELMs managed by regime choice
- **The hard problem is NOT P1** — it's P4a (tritium breeding in compact geometry) and P7 (HTS manufacturing)

TAE (p-B11 FRC): "Achieve fusion conditions" decomposes into:
- Reach T_i > 100-300 keV → extremely hard, requires beam-driven approach, not thermal equilibrium
- Achieve sufficient confinement at extreme temperature → FRC confinement scaling uncertain at these parameters
- Maintain FRC stability at extreme β → beam stabilization is the key innovation, demonstrated at C-2W but not at reactor scale
- **P1 IS the hard problem** — if you can solve it, P4 and P5 become much easier (no tritium, minimal neutrons)

**What this captures**: The causal/functional structure — WHY each design element exists, what problem it solves, and how the problem depends on upstream choices. The primitives provide a universal skeleton that makes concepts comparable: every concept must address P1-P7, so you can compare HOW they address each one.

**What it enables**:
- *Understanding*: Reading the graph tells you the story of each concept. CFS's thesis becomes visible: "P1 is not the hard problem (proven physics); the bet is that HTS makes P6 favorable by enabling compactness." TAE's thesis: "We accept extreme difficulty on P1 in exchange for trivializing P4-P5."
- *Transfer*: Two concepts sharing a sub-problem share the problem STATEMENT with context. "D-T tokamak needs TBR > 1.0 in toroidal geometry with 14 MeV flux" vs. "D-T laser ICF needs TBR > 1.0 in spherical chamber with pulsed 14 MeV flux." Similar problem, different geometry/timing → partial transfer, with the differences made explicit.
- *Generation*: You can ask "what other solutions exist for this specific sub-problem?" and the search is grounded by the context. You can also ask "what if we changed an upstream choice — how does the problem decomposition change?"

**Self-evaluation**:
- For understanding: Strong. The primitives provide a universal comparison framework. The context-dependent decomposition is the interesting part — it shows where concepts face the same challenge and where they face different ones.
- For generation: Moderate. Better than subsystems (problem-oriented search is more generative than category recombination), but the primitives themselves are fixed — you can't generate a concept that doesn't need to achieve fusion conditions. Generation happens at the solution level, not the problem level.
- For transfer: Strong. Shared sub-problem nodes with explicit context provide principled transfer criteria. You can compare problem contexts and decide whether transfer is justified.
- Risk: Could become very deep/complex. Need to control depth. The "context" at each node is doing a lot of work — how do you formalize it?

---

### C. Force-Resolution Cascades (Design Thesis)

**Core idea**: Every design choice resolves competing forces — requirements that pull in opposite directions. A fusion concept is a specific chain of force resolutions, where each resolution creates new tensions downstream. The graph traces these cascades. This is directly from Alexander (The Nature of Order) and Gross (Design as Exploring Constraints).

**What the nodes represent**: FORCES (competing requirements in tension) and RESOLUTIONS (design choices that navigate the tension). Edges connect resolutions to the new forces they create.

**What is a "force"?** A pair (or set) of requirements that compete:
- "Higher magnetic field improves confinement" vs. "Higher magnetic field costs more and creates structural stress"
- "Aneutronic fuel eliminates neutron damage" vs. "Aneutronic fuel requires 10× higher temperature"
- "Pulsed operation simplifies plasma control" vs. "Pulsed operation creates cyclic fatigue and reduces availability"

A force is the TENSION between desirable properties. Every concept navigates these tensions differently. The navigation IS the design thesis.

**Structure** (not a tree — a directed graph with cycles possible):

```
F1: Confinement quality vs. device cost
  │
  ├── Resolution: High-field compact tokamak (CFS thesis)
  │   "HTS enables 20 T → small device with good confinement → cheaper plant"
  │   Creates new forces:
  │   ├── F2: Compactness vs. blanket/shield space
  │   │   "Smaller device → less room for breeding blanket → harder to achieve TBR > 1.0"
  │   │   └── Resolution: FLiBe dual-function blanket
  │   │       Creates: F3: FLiBe chemical reactivity vs. safety case
  │   │       Creates: F4: FLiBe MHD drag in high-field environment vs. flow rate needs
  │   ├── F5: Field strength vs. magnet cost
  │   │   "20 T HTS costs more per coil, but fewer coils needed"
  │   │   └── Resolution: REBCO tape + demountable joints
  │   │       Creates: F6: Joint reliability vs. maintenance access benefit
  │   │       Creates: F7: HTS manufacturing yield vs. cost projection
  │   └── F8: Disruption severity scales with stored energy / volume
  │       "Compact + high-field → high energy density → severe disruptions"
  │       └── Resolution: Disruption avoidance regime (not mitigation)
  │           Creates: F9: Operating regime restriction vs. Q_eng optimization
  │
  ├── Resolution: Large low-field stellarator (Gauss Fusion thesis)
  │   "Stellarator eliminates disruption risk entirely; large size gives room for blanket"
  │   Creates new forces:
  │   ├── F10: 3D coil complexity vs. manufacturing cost
  │   ├── F11: Large device → high absolute capital cost, even if $/W is good
  │   └── F12: Stellarator optimization (QI/QA) accuracy vs. plasma performance
  │
  └── Resolution: Avoid magnetic confinement entirely (IFE thesis)
      "Inertial confinement → no magnets, no disruptions, no steady-state plasma"
      Creates new forces:
      ├── F13: Driver cost vs. repetition rate
      │   "Each shot needs MJ of driver energy; driver dominates capex"
      │   ├── Resolution: KrF excimer (Xcimer thesis)
      │   │   "KrF inherently cheaper per joule, UV wavelength optimal for coupling"
      │   │   Creates: F14: KrF gas handling vs. rep rate; F15: KrF maturity vs. DPSSL
      │   └── Resolution: DPSSL (most other laser IFE)
      │       Creates: F16: Diode cost vs. efficiency; F17: Nd:glass bandwidth
      ├── F18: Target cost vs. target performance
      │   "Must fabricate millions of precision cryogenic targets per year at ~$0.10-0.50 each"
      └── F19: Chamber survival under repeated neutron/debris loading
          "IFE chamber sees shock loading every ~0.1 sec; no magnetic protection"

F20: Neutron burden vs. fuel accessibility
  │ "D-T is easiest to burn (lowest T_i) but creates severe neutron problems"
  │ "Aneutronic fuels avoid neutrons but are much harder to burn"
  │
  ├── Resolution: Accept neutron burden (D-T path)
  │   "Well-understood fusion physics; accept the engineering complexity"
  │   Creates:
  │   ├── F21: Tritium self-sufficiency vs. blanket complexity
  │   ├── F22: First-wall lifetime vs. neutron damage
  │   ├── F23: Remote maintenance requirement vs. availability
  │   └── F24: Nuclear waste classification vs. public acceptance
  │
  ├── Resolution: Reject neutron burden (p-B11 path — TAE, LPPFusion, Marvel, HB11)
  │   "Eliminate entire neutron/tritium problem set; accept extreme plasma challenge"
  │   Creates:
  │   ├── F25: T_i > 100 keV achievability vs. physics understanding
  │   ├── F26: Bremsstrahlung losses vs. net energy gain
  │   └── F27: Direct conversion efficiency vs. plant Q_eng
  │
  └── Resolution: Partial compromise (D-He3 — Helion, Zephyr)
      "Much reduced neutrons (D-D side reaction only); intermediate T_i"
      Creates:
      ├── F28: He3 sourcing vs. fuel cost
      └── F29: D-D side neutrons still require some shielding
```

**What this captures**: The REASONING behind each concept. Why CFS chose high field (to resolve F1 via compactness), why that creates F2 (blanket space), why FLiBe resolves F2 but creates F3 and F4. The cascade IS the design thesis.

**Key properties**:

1. **Forces are SHARED across concepts.** F1 (confinement quality vs. cost) faces every magnetic confinement concept. But different concepts resolve it differently, and the downstream cascades diverge. Two concepts sharing a force are dealing with the same tension — even if they resolve it differently.

2. **Forces can CONVERGE from different paths.** F22 (first-wall lifetime vs. neutron damage) is reached via ANY D-T concept, regardless of confinement type. The force is the same; only the geometry and neutron spectrum differ. This convergence is where transfer opportunities live.

3. **The "design thesis" is the resolution chain.** CFS's thesis isn't "compact tokamak with HTS magnets" — it's "resolve confinement-vs-cost through compactness, then accept and manage the cascading forces that compactness creates (blanket space, disruption severity, HTS manufacturing)." The thesis is a PATH through force space, not a point in category space.

4. **Un-explored resolutions are visible.** If you can see all the forces, you can ask: "are there resolutions of F1 that no current concept has tried?" This is generative — it produces novel concepts by identifying unexplored force resolutions.

**Self-evaluation**:
- For understanding: Excellent. This is what the Test 4 assessors said was missing — the WHY. Each concept becomes a narrative of tensions and resolutions. You understand not just what they chose, but what they're betting on.
- For generation: Good potential. Un-explored resolutions and novel force combinations could generate genuinely new concepts. But requires deep domain knowledge to evaluate whether a resolution is physically feasible.
- For transfer: Different mechanism than Approach B. Transfer here means "these two concepts face the same FORCE" rather than "these two concepts face the same PROBLEM." Forces are more abstract — they identify the tension, not the engineering challenge. This could be higher-level but less actionable.
- Risk: Hard to formalize. Forces are inherently qualitative. The cascade structure could become tangled (forces create forces create forces...). Where do you stop? How do you validate that you've identified the real forces vs. post-hoc rationalization?

---

## Cross-Evaluation

| Criterion | A (Subsystems) | B (Primitives) | C (Forces) |
|---|---|---|---|
| **What nodes represent** | Hardware categories | Problems to solve | Tensions to navigate |
| **What edges represent** | Contains / implements | Generates / decomposes | Resolves / creates |
| **Captures WHY** | No | Yes — why each element exists | Yes — why each choice was made |
| **Captures trade-offs** | No | Partially (constraint context) | Yes — forces ARE trade-offs |
| **Universal comparison skeleton** | Weak (subsystems vary) | Strong (primitives are universal) | Moderate (top-level forces shared) |
| **Captures design thesis** | No | Partially (which problems are hard) | Yes (resolution chain IS thesis) |
| **Formal / testable** | Easy | Moderate | Hard |
| **Transfer mechanism** | Label matching | Shared problem with context | Shared force |
| **Generation mechanism** | Combinatorial (bad) | Novel solutions to problems | Novel resolutions of forces |
| **Maps to CAS/cost** | Direct | Indirect (problems → cost drivers) | Indirect (forces → cost) |
| **Risk of over-abstraction** | Low (too concrete) | Medium | High |
| **Depth control** | Easy (physical hierarchy) | Moderate (when to stop decomposing?) | Hard (cascades multiply) |

---

## What's Missing from All Three

Writing out these three approaches reveals gaps that none of them address:

**1. Quantitative parameters.** All three are structural/qualitative. None carries numbers. But the Test 4 assessors unanimously requested scale (MWe, volume, field), performance targets (Q, τ_E, T_i), and cost basis ($/W). These aren't structural elements of the graph — they're ANNOTATIONS on nodes. Any approach needs a parameter layer.

**2. Confidence / maturity.** Some sub-problems are well-understood (steam turbines), others are speculative (p-B11 ignition). The graph should distinguish between "we know how to solve this" and "no one knows if this is solvable." This is a maturity annotation on solution nodes.

**3. The economic lens.** The project's ultimate goal is TEA comparison (LCOE). None of these approaches directly connects to cost. The cost structure emerges from the problem/subsystem decomposition, but the mapping needs to be explicit: which nodes drive which cost accounts?

**4. Time / development sequence.** Concepts are at different stages. Some sub-problems are being worked on now; others are deferred to later development phases. The graph is static but reality is dynamic.

Of these, #1 and #2 are the most important and the easiest to add as annotation layers on any of the three approaches.

---

## Synthesis: Are These Really Three Alternatives?

After writing them out, I notice something: these three approaches operate at different levels of abstraction and might be complementary rather than competing.

- **A (Subsystems)** answers: "What is the plant made of?"
- **B (Primitives)** answers: "What problems must the plant solve?"
- **C (Forces)** answers: "What trade-offs does the concept navigate?"

A concept's full story might use all three:

> CFS resolves the confinement-vs-cost tension (C) by choosing compactness-via-high-field. This means the problem "achieve fusion conditions" (B) decomposes into proven tokamak physics at high β, which is implemented by an HTS magnet system with REBCO coils (A). But compactness creates a new tension: blanket space (C), which means the problem "breed tritium" (B) becomes harder than it would be in a larger device, requiring a dual-function FLiBe blanket (A).

The three levels interleave naturally. Forces (C) motivate choices. Choices generate problems (B). Problems get solved by subsystems (A). Subsystems create new physical realities that generate new forces (C).

This is actually the generative sequence Alexander describes — each level feeds the next.

**But for a prototype, we can't do all three at once.** We need to pick one primary framing and test it.

---

## What I'd Prioritize

**Start with B (Primitive-Requirement Decomposition), enriched with elements of C.**

Reasoning:

1. **B has the strongest skeleton.** The 7 primitives are universal and non-controversial — every concept MUST address them. This gives you a comparison framework immediately: "how does Concept X address P1? P4? P6?" The flat table couldn't do this because its columns were approach-specific, not requirement-universal.

2. **B directly serves Goal 1 (understanding).** Reading a primitive decomposition tells you what problems each concept faces and which are the hard ones. CFS's hard problem is P4a+P7 (tritium breeding in compact geometry + HTS manufacturing). TAE's hard problem is P1 (achieving fusion conditions with p-B11). This is immediately more informative than the flat table.

3. **B directly serves Goal 2 (transfer).** Shared sub-problems with explicit context are exactly the transfer mechanism described in the context document Section 7. "D-T tokamak tritium breeding" and "D-T mirror tritium breeding" share the same problem statement with different geometric context — the graph makes the shared part and the divergent part both visible.

4. **C enriches B where it matters most.** The force-resolution framing adds the most value at the TOP of the graph — where the big architectural choices happen (confinement approach, fuel choice). These are the points where understanding the trade-off reasoning matters most for differentiation. Below the first 1-2 levels, B's problem decomposition is clearer and more tractable than C's cascading forces.

5. **A is recoverable.** Once you have B, you can map each leaf-level solution to a subsystem. The subsystem view is derivable from the problem view; the reverse is not true.

**What "enriched with C" means concretely**: At the top-level OR nodes (the big architectural choices — confinement, fuel, energy conversion), annotate with the forces being resolved. "Why D-T instead of p-B11?" → "Resolves F20 (neutron burden vs. fuel accessibility) by accepting neutron burden in exchange for proven plasma physics." At lower levels, pure problem decomposition suffices.

### Three things to try (in order of priority):

**Priority 1: Primitive decomposition for 3 concepts.** Build B-style graphs for CFS (D-T compact tokamak), TAE (p-B11 FRC), and one IFE concept. Focus on the first 3-4 levels. See whether the primitive skeleton reveals structure that the flat table hid, and whether the divergence points make sense.

**Priority 2: Force annotation at decision points.** At each major OR node in the Priority 1 graphs, annotate with the forces being resolved. "Why did this concept choose THIS resolution?" Test whether the force annotations capture the design thesis (what Test 4 showed was missing from the flat table).

**Priority 3: Transfer analysis at shared sub-problem nodes.** Identify where two concepts' graphs converge on the same sub-problem (different paths, same problem node). Compare the context at convergence. Write one pattern card for the strongest shared sub-problem. Test whether the context comparison provides a principled transfer criterion.

These three build on each other. Priority 1 produces the skeleton. Priority 2 enriches it with reasoning. Priority 3 tests the transfer hypothesis. If Priority 1 doesn't reveal interesting structure, there's no point doing 2 and 3.

---

## Open Questions for Discussion

1. **Depth control.** How many levels deep? The primitives give you 2 levels for free (primitive → context-dependent sub-problem). Going to 3-4 levels (sub-sub-problems, specific engineering challenges) is where it gets interesting but also where complexity explodes. Proposal: go deep enough that the leaf nodes are recognizable engineering challenges with known solution approaches — things you could write a cost model for.

2. **Format.** YAML? Markdown? The graph structure suggests a format that can represent AND/OR nodes with typed edges and annotation layers. YAML can do this but might get cluttered. An alternative: each concept gets its own markdown document (readable), plus a machine-readable YAML for cross-concept analysis.

3. **Which IFE concept?** For maximum learning, probably D-T laser ICF (Xcimer or Focused Energy). This shares fuel (D-T) with CFS, enabling the tritium-breeding transfer test, while having completely different confinement physics. Alternative: projectile ICF (First Light), which shares D-T fuel and pulsed operation with MIF concepts.

4. **Are the primitives right?** The 7 primitives above are a first cut. P6 (economic) and P7 (licensable/buildable) might be too "downstream" for a prototype — they depend on everything else and might not decompose interestingly. Maybe start with P1-P5 only and add P6-P7 later.

5. **What does "success" look like?** How do we know the AND/OR graph is better than the flat table? Proposal: apply the same Phase 1d tests (blind row recoverability, generative coherence) to the graph representation and compare. If the graph enables better concept recovery AND better generation, it's better.
