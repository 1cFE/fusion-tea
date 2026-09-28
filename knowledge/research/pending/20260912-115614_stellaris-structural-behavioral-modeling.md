---
date: 2026-09-12
researcher: Claude
topic: Structural and behavioral modeling for the Stellaris stellarator in SysML v2
tags: [sysml, structural-modeling, behavioral-modeling, stellarator, stellaris, best-practices]
research_type: domain + methodology
---

# What a Proper Stellaris Structural+Behavioral Model Would Look Like

## Research Question

The current Stellaris model (`stellarator_plant.sysml`) uses SysML v2 exclusively as a parameterized cost ledger: 181 attributes, 65 calcs, 14 constraints, but zero ports, connections, flows, interfaces, nested parts, actions, or state machines. What would a model following SysML v2 and systems engineering best practices look like — and what would it take to get there?

## Summary

- The Stellaris source material (Fusion Engineering and Design 2025 paper) describes a physically rich system with two separate cooling loops, 50 non-planar modular coils with 6 unique designs, a WCLL breeding blanket with liquid PbLi, an island divertor, and sector-based maintenance architecture. None of this physical structure is represented in the model.
- SysML v2 provides seven structural/behavioral mechanisms beyond attributes and calcs: nested parts, ports, connections, flows, actions, states, and allocations. The current model uses zero of them.
- A proper model would layer these incrementally: nested parts first (decompose subsystems into physical components), then ports and connections (declare the energy/material topology), then flows (what moves through the connections). Actions and states come later, if needed for availability modeling.
- The existing calc chain already computes what flows and connections would declare — the energy balance, power conversion, and cost rollup are correct. What's missing is the structural declaration of *why* those calcs are wired the way they are. The model computes the right numbers but can't answer "what connects to what" or "if I change this interface, what's affected."
- A practical first step would add structural depth to the three subsystems where the sources describe clear internal decomposition and inter-subsystem interfaces: the magnet system, the blanket/shield/vessel cluster, and the power conversion chain (blanket → primary loop → steam generator → turbine → generator).

## Detailed Findings

### What the Sources Describe (and the Model Doesn't Capture)

The Stellaris paper (Fusion Engineering and Design 214, 2025) and the Helios comparison design describe a machine with clear physical architecture. Here is what the sources describe, organized by what kind of SysML modeling would capture it.

**Source**: `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/output.md`
**Source**: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/helios-stellarator-comparison/output.md`

#### Physical Decomposition (needs nested parts)

The model's flat subsystem list obscures significant internal structure:

**Magnet System** — the most detailed subsystem in the sources:
- 50 modular non-planar coils (5-fold rotational symmetry, 6 unique designs)
- REBCO HTS conductor in pre-soldered tape stacks with copper jacket
- Winding packs (15% conductor, 10% copper, 45% insulation, 26% steel, 4% helium cooling)
- Steel casings (63-200 tons each, castings)
- Inter-coil support plates (0.7-1 m thick, up to 58 tons, forged)
- Central inner support rings (~0.7 m thick, ~200 tons each)
- Current leads (flat plate connections, cryogenic to room temperature)
- Non-insulated (NI) concept for passive quench protection

**Blanket/Shield/Vessel cluster** — a radial build with distinct physical layers:
- First wall: EUROFER97 with 2 mm tungsten armor, helium-cooled at 8 MPa
- Breeding blanket: WCLL (Water-Cooled Lithium-Lead), PbLi eutectic at 70% Li-6 enrichment
- In-vessel neutron shield: tungsten-carbide, 100-225 mm variable thickness
- Vacuum vessel: SS316LN, double-walled, with boron-carbide neutron absorber

**Power Conversion** — currently absent as parts entirely:
- Steam generator / heat exchanger (implied by WCLL + steam Rankine)
- Turbine and generator
- Condenser
- Feedwater system

**Support Structures** — three distinct structural element types, not one "structure" part.

#### Energy and Material Topology (needs ports, connections, flows)

The sources describe clear interfaces between subsystems that the model doesn't represent:

**Two separate cooling loops** (a key architectural fact):
1. First wall → helium at 8 MPa, 350°C inlet, <370°C outlet
2. Breeding blanket → pressurized water at PWR conditions

These are physically separate coolant circuits with separate manifolds. The current model has a single `primary_loop` calc that doesn't distinguish them.

**Power flow chain** (quantified in the paper, Table 2):
- Fusion power (~2700 MW) → 80% neutron power (~2160 MW) + 20% alpha power (~540 MW)
- Neutron power → blanket (energy multiplication factor 1.20) → thermal power (~3150 MW)
- Thermal power → steam cycle (η ≈ 1/3) → gross electric (~1000 MW)
- Gross electric → recirculating power (ECRH 50 MW, cryoplant, pumps) → net electric
- 111 GJ stored magnetic energy → 7.5 kW steady-state losses → cryoplant load

**Tritium fuel cycle** (a closed material loop):
- D-T fuel → plasma → neutrons → Li-6 in PbLi → tritium bred (TBR 1.074)
- Tritium extracted from circulating PbLi → processed → re-injected
- Liquid breeder can be drained for maintenance

**ECRH heating** (power + waveguide interface):
- 50 MW total, 240 GHz, 8 port locations
- Injected from high-field side between coils
- Waveguide inner diameter ~60 mm
- Ports minimize TBR degradation

#### Operational Modes (needs actions, states)

**Maintenance cycle** — affects availability and thus LCOE:
- 4-year operating cycle between major maintenance
- 5-7 month maintenance windows
- Sector splitting: 4 interfaces, ~7000-ton modules, radial extraction
- Sequence: de-energize coils → warm up → drain PbLi → disconnect services → breach cryostat

**Magnet charging**: 600 hours (25 days) to reach full operating current. Deliberate slow ramp to avoid quench from transient losses.

**Quench response** (NI concept): Passive — entire coil energy dissipated within coil cold mass, peak temperature below 300 K.

### SysML v2 Modeling Patterns Available

SysML v2 (Spec Part 1, Sections 7.11-7.18) provides seven mechanisms beyond attributes and calcs. Here is what each one does and when it earns its place in the Stellaris model.

**Spec reference**: `/home/reid/1cfe/agentic-mbse/docs/sysmlv2/SysML_Spec_v2_Part1/full_document.md`

#### 1. Nested Parts (Spec §7.11) — structural decomposition

A `part def` can own other `part` usages as composite features. This is the most natural extension of what we have.

```sysml
part def 'Magnet System' {
    part coils[50] : 'Modular Coil';
    part cryostat : 'Cryostat';
    part current_leads[*] : 'Current Lead';
    part structural_casing : 'Coil Casing';
    part support_plates[*] : 'Inter-Coil Support';
    part support_rings[*] : 'Central Support Ring';
}
```

**When it earns its place**: when the sub-components have their own attributes, interfaces, or cost drivers. The magnet system is the clear candidate — the sources describe coils, casings, and support structure as separate cost items with distinct materials and fabrication methods. The blanket/shield/vessel cluster is another — they share a radial build and each layer has distinct material properties and cost scaling.

**When it's overkill**: if a sub-component is just a cost line item with one `capital_cost` attribute. The balance-of-plant subsystems (turbine, electric plant, heat rejection, misc plant) are currently modeled as `cost_per_mw` scalars, and there's no source material to decompose them further.

#### 2. Ports (Spec §7.12) — connection points

A `port def` defines a connection point with directed features (`in`, `out`, `inout`). The conjugation mechanism (`~PortName`) reverses directions so a producer's port matches a consumer's port.

```sysml
port def 'Thermal Port' {
    out item heat_out : 'Coolant';
    in item heat_in : 'Coolant';
}

part def 'Blanket' {
    port neutron_in : ~'Neutron Port';
    port thermal_out : 'Thermal Port';
}
```

**When it earns its place**: when you need to reason about the topology — which subsystem connects to which, and through what medium. For Stellaris, ports would express the two separate cooling circuits (helium first wall, water blanket) as distinct interfaces rather than merged parameters.

#### 3. Connections (Spec §7.13) — system wiring

Connections wire ports together. The `connect ... to ...` syntax is the most common form.

```sysml
connect blanket.thermal_out to primary_loop.hot_leg_in;
connect primary_loop.hot_leg_out to steam_generator.hot_side_in;
```

**When it earns its place**: when the wiring diagram itself is information. The Stellaris power flow chain (blanket → primary loop → steam generator → turbine → generator → grid, with recirculation back to ECRH, cryoplant, pumps) is a wiring diagram that the current model only captures as calc bindings.

#### 4. Flows (Spec §7.16) — what moves between parts

Flows declare what physically transfers through connections: coolant, electrical power, neutrons, tritium.

```sysml
flow of 'Coolant'
    from blanket.thermal_out.heat_out
    to primary_loop.hot_leg_in.heat_in;
```

**When it earns its place**: when you need to trace what moves through the system. The tritium fuel cycle is a closed material loop that the sources describe but the model doesn't capture at all — tritium bred in PbLi, extracted, processed, re-injected as fuel.

#### 5. Actions (Spec §7.17) — what the system does

Action definitions model temporal processes. Sub-actions can be sequenced (`then`), forked, joined, or decided between.

```sysml
action def 'Steady State Operation' {
    action burn : 'Fusion Burn';
    flow burn.neutron_power to convert.neutron_power;
    action convert : 'Thermal Conversion';
    flow convert.thermal_power to cycle.thermal_power;
    action cycle : 'Power Cycle';
}
```

**When it earns its place**: when operational sequences affect cost drivers. The maintenance cycle (4-year operation, 5-7 month maintenance window, sector splitting sequence) directly affects availability and thus LCOE. The magnet charging sequence (25 days to reach operating current) affects startup costs.

#### 6. States (Spec §7.18) — operating conditions

State definitions model event-driven behavior with transitions.

```sysml
state def 'Plant States' {
    state shutdown;
    state startup;
    state steady_state;
    transition shutdown accept 'Start Command' then startup;
    transition startup if startup_complete then steady_state;
}
```

**When it earns its place**: when the model needs to distinguish operating modes that have different cost implications. A stellarator is steady-state (unlike a tokamak's pulsed operation), so state modeling is less critical here than for pulsed concepts. But the maintenance/operation cycle still affects capacity factor.

#### 7. Allocations (Spec §7.15) — function-to-structure mapping

Allocations map behavioral elements to structural elements: "this function is realized by this component."

```sysml
allocate burn to plasma;
allocate convert to blanket;
allocate generate to turbine_island;
```

**When it earns its place**: for traceability — linking requirements or functions to the components that realize them. Useful when you need to answer "if this requirement changes, which components are affected?"

### What the Model Already Does Well

The attribute/calc/constraint pattern is not wrong — it's incomplete. The existing model:

- Correctly implements the physics-to-cost computation chain (65 calcs, validated against 1costingFE)
- Carries full source traceability on every parameter (doc comments with Source/Ref/Basis)
- Asserts viability constraints at the top level (14 constraints covering field limits, wall loading, sustainment, burn hold, recirculation)
- Uses the library/design separation well (reusable calc defs in library, concept-specific bindings in designs)

Adding structural and behavioral elements does not replace any of this. It layers on top: ports and connections would declare the topology that the calc bindings already compute; nested parts would decompose the subsystems that the attributes already parameterize; flows would name the physical transfers that the calcs already model as equations.

### What a Proper Model Would Look Like

A "properly modeled" Stellaris plant would have three views layered on the same model:

**Structural view** — what the machine is made of:
- Stellaris contains a magnet system, which contains 50 modular coils, a cryostat, current leads, structural casings, support plates, and support rings
- Stellaris contains a blanket/shield/vessel cluster, where the first wall, breeding blanket, neutron shield, and vacuum vessel are distinct parts with a shared radial build
- Stellaris contains a power conversion chain (steam generator, turbine, generator, condenser)
- Each subsystem has ports declaring its interfaces (thermal, electrical, neutron, material)

**Behavioral view** — what the machine does:
- The power conversion chain as a sequence of actions (fusion → neutron capture → heat transfer → steam generation → electrical generation)
- The tritium fuel cycle as a closed loop (fuel injection → burn → breeding → extraction → processing → re-injection)
- The maintenance cycle as a state machine (operation → shutdown → maintenance → startup → operation)

**Analytical view** — what the machine costs (what we already have):
- Calc defs computing costs from physical parameters
- Constraints asserting viability bounds
- LCOE rollup from all cost accounts

The structural and behavioral views would share attributes and ports with the analytical view. A change to a structural parameter (e.g., coil bore radius) would flow through the ports and connections in the structural view, through the calcs in the analytical view, and affect the flows in the behavioral view.

## Feasibility Assessment

### Incremental Path (Recommended)

The model does not need all seven mechanisms at once. A pragmatic sequence:

**Step 1: Nested parts** — decompose the magnet system, blanket/shield/vessel cluster, and power conversion chain into physical sub-components. This is the smallest step from where we are. It doesn't change any calcs or attributes — it just groups the existing attributes under the sub-components they belong to. Estimated effort: 1-2 work items.

**Step 2: Ports and connections** — define thermal, electrical, and neutron port defs. Declare ports on subsystems and connect them. This makes the energy balance topology explicit. The calcs continue to compute the same values; the ports and connections declare *why* those calcs are wired that way. Estimated effort: 1-2 work items.

**Step 3: Flows** — declare what moves through the connections (coolant, electrical power, neutrons, tritium). This layers on top of ports and connections. The tritium fuel cycle is the highest-value flow to model because it's a closed material loop that the current model doesn't capture at all. Estimated effort: 1 work item.

**Step 4 (optional): Actions and states** — model the maintenance cycle and magnet charging sequence. Only worth doing if availability modeling becomes a priority. Estimated effort: 1 work item.

### Risk: Syside Parser Support

The syside parser (our SysML v2 tooling) may not fully support all structural/behavioral constructs. Before investing in ports, connections, and flows, we should verify that syside can parse them and that the codegen pipeline can handle them. If syside doesn't support ports or connections, the structural model would be documentation-only (still valuable for human understanding, but not computable).

### Risk: Library vs Design Boundary

The current library/design separation puts all `part def`s and `calc def`s in the library and all attribute bindings in the design. Adding ports and connections requires deciding: do port defs go in the library (reusable across concepts) or in the design (concept-specific)? The thermal and electrical port defs should be library elements. The specific wiring (which port connects to which) is concept-specific and belongs in the design.

### What Does NOT Need to Change

- The calc chain stays exactly as-is. Ports and connections don't replace calcs.
- The attribute bindings stay. Nested parts just group them under the right sub-component.
- The constraint assertions stay. They already operate at the right level.
- The cost rollup logic stays. The CAS hierarchy is a cost structure, not a physical structure — both are valid views of the same system.

## Gaps in Source Material

Several subsystems lack enough source detail for structural modeling:

1. **Power conversion system**: No turbine, generator, condenser, or BOP details for Stellaris. Must be inferred from WCLL blanket (implies steam Rankine). Helios provides a concrete reference (steam Rankine, 40% efficiency, 635°C superheated steam).
2. **Tritium processing**: Extraction from PbLi, purification, storage, and re-injection are acknowledged as future work in the Stellaris paper.
3. **Vacuum pumping**: Pump types, locations, capacities not specified. Helios references turbomolecular pumps and divertor pump ducts.
4. **Electrical power supplies**: Coil power supplies, bus bars, grid connection architecture not specified.
5. **Instrumentation and control**: No details provided.
6. **Cryo-plant internals**: Size, power consumption, cooling capacity not detailed beyond 20 K operating temperature and nuclear heating loads.

These gaps mean a structural model would be unevenly detailed: rich for the magnet system and blanket cluster (where the sources are thorough), thin or absent for BOP and auxiliaries (where the sources don't go).

## Recommendations

1. **Start with nested parts in the magnet system.** This subsystem has the richest source material (26 attributes already, detailed physical descriptions of coils, casings, support structure) and the most to gain from decomposition. It's also the most complex cost account (CAS22.1.1) and the one where sub-component cost drivers are most distinct.

2. **Add thermal ports to the blanket/primary-loop/turbine chain.** This makes the power flow chain explicit and captures the two-cooling-loop architecture. Even without flows, the ports and connections would show the energy balance topology that the current model hides in calc bindings.

3. **Verify syside support first.** Before writing structural model code, test whether `port def`, `connect`, and `flow` parse correctly in syside. If they don't, the structural model should be deferred until tooling catches up.

4. **Don't model what the sources don't describe.** The BOP subsystems (turbine, electric plant, heat rejection, misc plant) are single-parameter cost items in both the model and the sources. Decomposing them would be inventing structure, not modeling it.

5. **Keep the analytical view intact.** The calc chain is the project's core deliverable. Structural and behavioral modeling should layer on top, not require reworking the existing computations.

## Open Questions

1. Does syside parse `port def`, `connect`, and `flow` constructs? If not, what's the timeline for support?
2. Should structural modeling be a library concern (reusable across MFE concepts) or a design concern (concept-specific)? The answer affects where port defs and connection patterns live.
3. How would structural elements interact with the codegen pipeline? The current pipeline extracts attributes and calcs — would it need to handle ports and connections too?
4. Is the two-cooling-loop architecture (helium FW + water blanket) shared across stellarator concepts, or specific to Stellaris's WCLL choice? This determines whether the port topology goes in the library or the design.
