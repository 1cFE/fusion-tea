# Reasoning Tree — Phase 2a

## Summary

- **Nodes**: 6 (1 expanded, 5 pending)
- **Constraints extracted**: 22
  - Validated: 0
  - Flagged: 0
  - Rejected: 0
  - Unmappable: 22
  - Validation rate: 0%

---

## Tree

### L0: How should we confine the fusion reaction to achieve sustained energy production?

**Requirements bearing**:
- **R1**: Confinement method determines what fuel reactions are accessible. High-density pulsed schemes can burn advanced fuels if confinement time is short enough to suppress losses. Continuous low-density schemes impose stricter ignition temperature requirements, favoring the lowest-barrier reactions.
- **R2**: This question is dominated by R2. Confinement IS the mechanism by which fusion conditions are created and sustained. Every viable approach must satisfy the Lawson triple product nTτ_E > threshold. The confinement architecture determines which axis (density, temperature, time) is leveraged.
- **R3**: The energy balance of the entire plant depends on recirculating power consumed by the confinement system itself — magnets, drivers, heating systems. A confinement approach that requires enormous recirculating power may satisfy R2 but fail R3.
- **R4**: Fusion energy products (neutrons, charged particles, photons) must escape the confinement volume and reach energy conversion systems. Confinement that also traps energy products undermines R4. The geometry of confinement determines how and where energy is deposited.
- **R5**: The spatial and temporal distribution of neutron flux is set by confinement geometry. Pulsed confinement creates burst irradiation; continuous creates steady-state activation. Both create radioactive inventories that must be managed.
- **R6**: The first wall, divertor, and structural components face plasma-facing loads determined by confinement geometry. Some confinement modes create continuous high heat flux on narrow regions; others distribute it or deliver it in pulses. This shapes material survivability requirements.

**Option: Closed Magnetic Topology Confinement**

*Thesis*: Arrange magnetic fields in a closed geometry — field lines that curve back on themselves — so that charged plasma particles, constrained to spiral along field lines, have no free path to escape. This solves the 'end loss' problem inherent to linear geometries by eliminating ends. The trade-off is that a closed toroidal field alone is insufficient: curvature and gradient drifts cause charge separation and radial loss, so the topology must incorporate helical field-line winding (rotational transform) to average out drifts — which either requires driving toroidal plasma current or imposing 3D coil complexity.

Requirement analysis:
- **R1**: Compatible with any fusion fuel. The continuous nature allows steady-state fuel injection and helium ash exhaust, which is favorable for any reaction. However, low tritium breeding blanket access is constrained by the closed geometry's structural complexity.
- **R2**: Achieves fusion conditions through the confinement-time axis of the Lawson criterion. Typical operating densities (~10^19–10^21 m^-3) require energy confinement times of seconds. Temperature (~10–20 keV for D-T) must be maintained by continuous external heating or alpha particle self-heating (ignition). The plasma is inherently MHD-unstable and requires careful field shaping for stability.
- **R3**: Recirculating power is consumed by superconducting magnet refrigeration, plasma heating, and current drive systems. Alpha-particle self-heating (burning plasma) is essential — below the ignition threshold, external heating power dominates and net electricity is marginal or negative. A continuous steady-state operation profile is favorable for grid delivery but requires uninterrupted plasma control.
- **R4**: Neutrons (for D-T) stream freely through the magnetic field and deposit energy in a surrounding blanket — this is the primary energy extraction path. Charged fusion products (alpha particles) are confined and heat the plasma, eventually thermalizing and being exhausted through a divertor. The closed geometry creates a natural annular blanket installation volume around the plasma.
- **R5**: Steady-state neutron flux continuously activates the first wall, blanket, and structural materials. Tritium is bred in the blanket and must be extracted continuously. The divertor handles plasma-facing particle and heat exhaust, concentrating erosion and activation in a localized region.
- **R6**: The first wall faces continuous plasma radiation and charge-exchange neutral bombardment. The divertor faces intense steady-state heat flux (~10–20 MW/m²). Superconducting magnets must be shielded from neutron-induced flux swamping and radiation damage to insulators. The closed geometry's complexity creates many structural joints and penetrations that must survive the neutron environment.

Constraints derived:
- DC-001 [NOVEL] (force, R2): field_topology=closed_toroidal → geometry=toroidal_or_quasi-toroidal_reactor_shape — Condition not mappable to table columns
  - *Closed field line topology that prevents end losses requires field lines to curve back on themselves. In 3D, this necessitates a toroidal or topologically equivalent shape; there is no flat or cylindrical geometry that satisfies this constraint without artificial boundaries.*
- DC-002 [NOVEL] (force, R2): field_topology=closed_toroidal → rotational_transform=required_for_radial_confinement — Condition not mappable to table columns
  - *In a purely toroidal field, grad-B and curvature drifts are in opposite vertical directions for ions and electrons, causing charge separation and a radial electric field that drives plasma outward. Only helical field winding (rotational transform) averages these drifts to zero over a field-line transit, suppressing the radial loss.*
- DC-003 [NOVEL] (force, R3): rotational_transform=provided_by_plasma_current → plasma_current_drive=continuous_power_requirement, disruption_risk=activated — Condition not mappable to table columns
  - *Toroidal plasma current that provides rotational transform must be driven continuously (or bootstrapped from pressure gradients); if it terminates suddenly, confinement collapses rapidly (disruption), releasing stored magnetic and thermal energy into the first wall in milliseconds.*
- DC-004 [NOVEL] (force, R6): rotational_transform=provided_by_external_3d_coils → coil_complexity=high_3d_geometry, bootstrap_current_drive=reduced_or_eliminated — Condition not mappable to table columns
  - *Externally imposed rotational transform via shaped coils eliminates the need for net plasma current and removes disruption risk, but requires coils of complex 3D geometry that must be fabricated, assembled, and maintained around a neutron-irradiated vessel — a formidable engineering challenge.*
- DC-005 [NOVEL] (force, R2): plasma_beta=exceeds_threshold → mhd_stability=lost, confinement=degraded_or_lost — Condition not mappable to table columns
  - *The ratio of plasma pressure to magnetic pressure (beta) is bounded above by MHD stability limits (typically a few percent for simple toroidal geometries). Above this limit, interchange and ballooning instabilities grow on Alfvénic timescales, causing rapid confinement degradation. This caps the pressure (and thus fusion power density) achievable at a given field strength.*
- DC-006 [NOVEL] (force, R5): closed_geometry=continuous_steady_state → neutron_fluence=continuous_material_damage_accumulation — Condition not mappable to table columns
  - *Continuous operation at fusion power levels means the first wall and blanket accumulate neutron damage (dpa) without interruption. Materials must survive multi-year fluences; no 'coast-down' period dilutes the dose rate as in pulsed systems.*

New questions:
- How should rotational transform be provided: plasma current (with disruption risk and current-drive power), external 3D coils (with manufacturing and maintenance complexity), or a hybrid?
- What is the maximum achievable beta (pressure/field ratio) in the chosen topology, and how does this set the minimum magnetic field strength for a given fusion power density?
- How should the plasma-exhaust channel (divertor) be designed to handle steady-state heat flux of ~10–20 MW/m² without material erosion exceeding acceptable limits?
- At what plasma conditions does alpha-particle self-heating exceed external heating power, and how is the transition to a burning plasma controlled?
- How are plasma-facing components replaced, and how does the closed geometry limit maintenance access?
- What is the minimum recirculating power fraction (heating + current drive + magnets) that still permits net electricity export at realistic thermal conversion efficiency?

**Option: Open Magnetic Topology Confinement (Mirror Confinement)**

*Thesis*: Confine plasma in a linear geometry using local maxima of magnetic field strength at each end. A charged particle moving toward a region of increasing field has its parallel velocity converted to perpendicular velocity (magnetic moment conservation); particles with sufficiently low parallel-to-perpendicular velocity ratio are reflected before reaching the end. This solves the geometric complexity of closed topologies — a linear device is far simpler to engineer and access — but introduces a fundamental loss mechanism: the velocity-space 'loss cone' is always present, and Coulomb collisions continuously scatter particles into it.

Requirement analysis:
- **R1**: Compatible with any fuel in principle, but end losses preferentially exhaust high-energy particles, which distorts the tail of the distribution and can reduce effective reaction rate. Aneutronic fuels may benefit from the ability to directly extract energy from escaping charged particles.
- **R2**: Loss-cone losses set a fundamental upper bound on τ_E that scales unfavorably with density (more collisions → faster pitch-angle scattering into loss cone → shorter effective confinement). Achieving the Lawson criterion requires either extremely long plasmas (reducing end-loss fraction) or active end-plugging using additional confining fields or electrostatic potentials.
- **R3**: End plugging schemes consume significant recirculating power. If plugging uses radio-frequency heated plasma at the ends (ambipolar trapping), the plugging power can exceed fusion power for plausible geometries unless the central cell plasma has very high Q. This is a severe R3 challenge.
- **R4**: Escaping charged particles carry kinetic energy directly out the ends — this can be converted directly to electricity via electrostatic deceleration (direct energy conversion), potentially at high efficiency. This is a unique R4 advantage over closed topologies where all energy must go through a thermal cycle.
- **R5**: Neutron flux is highest in the central cell, lower at the ends. The open geometry allows end regions to be physically separated and shielded differently. No continuous closed vessel is required, potentially simplifying tritium management.
- **R6**: The central cell first wall faces plasma radiation and particle loads. End regions face intense ion bombardment from particles that are not reflected. The linear geometry simplifies remote maintenance access compared to closed topologies.

Constraints derived:
- DC-007 [NOVEL] (force, R2): topology=open_linear → loss_cone=always_populated_by_collisions — Consequence not mappable to table columns
  - *In any magnetic mirror, there exists a cone in velocity space (v_parallel/v_total > sin(θ_min)) of particles that are not reflected. Coulomb collisions occur at rate ~n/T^(3/2) and scatter particles from the confined region into the loss cone continuously; this is irreversible without active intervention.*
- DC-008 [NOVEL] (force, R2): end_loss=not_plugged → confinement_time=insufficient_for_lawson_at_feasible_length — Condition not mappable to table columns
  - *An unplugged mirror with mirror ratio R has confinement time τ ~ (ln R) × τ_ii (ion-ion collision time). For D-T at fusion-relevant densities, this is far too short unless the device is kilometers long. Plugging is not optional for net energy.*
- DC-009 [NOVEL] (force, R3): end_plugging=electrostatic_ambipolar → plug_power=scales_with_plug_potential_times_particle_loss_rate — Condition not mappable to table columns
  - *An electrostatic plug must maintain a positive potential well in the end cells to confine electrons (which otherwise escape, creating a potential that drains ions). Sustaining this requires continuous plug heating power proportional to the particle loss rate and potential height — this power is parasitic and must be subtracted from gross fusion power.*
- DC-010 [NOVEL] (force, R4): geometry=linear → direct_energy_conversion=physically_accessible — Condition not mappable to table columns
  - *Ions escaping the end mirrors carry kinetic energy in a directed beam; passing this beam through an electrostatic decelerator (inverse accelerator) recovers kinetic energy as electrical energy at efficiencies potentially >80%, far exceeding the ~40% of thermal cycles. This option is geometrically unavailable in closed topologies.*

New questions:
- What is the minimum plug power fraction at which a mirror system can achieve net electricity, including direct conversion efficiency at the ends?
- How does the mirror ratio need to be optimized given the trade-off between better confinement (high ratio) and magnet capital cost and field stress?
- Can plasma instabilities specific to loss-cone distributions (e.g., drift-cyclotron, loss-cone instabilities) be suppressed, and at what cost in recirculating power or plasma control complexity?
- If direct energy conversion is used at the ends, how is tritium bred, since there is no natural blanket geometry around the plasma?
- What is the optimal central-cell length and density for a given end-plug technology?

**Option: Inertial Confinement**

*Thesis*: Compress a small fuel target to extreme density so rapidly that fusion conditions are achieved and burn propagates before the plasma pressure can disassemble the target. 'Confinement' is provided by the inertia of the fuel itself — at densities of ~200–1000 g/cm³ and radii of ~1 mm, the disassembly time τ ~ R/c_s is ~100 picoseconds, which is sufficient for significant burn fraction if the hot-spot ignites and a burn wave propagates outward. This approach inverts the Lawson trade-off: instead of long confinement time at moderate density, it achieves fusion via extreme transient density.

Requirement analysis:
- **R1**: Fuel is a discrete target — batch processing. Tritium (for D-T) is a small quantity per shot (~few mg), enabling precise fuel accounting. Target fabrication must produce thousands of targets per day for commercial power, which becomes a supply-chain and manufacturing challenge. Fuel injection into the reaction chamber at ~10 Hz is a logistics requirement activated by this choice.
- **R2**: The Lawson criterion is satisfied transiently: density ~10^31 m^-3, temperature ~5–20 keV in the hot spot. The challenge is achieving these conditions: compression must be hydrodynamically stable, the hot spot must form before the main fuel is compressed cold (cold fuel quenches the hot spot if they mix), and energy coupling from driver to target must be efficient.
- **R3**: Net energy requires target gain G (fusion energy / driver energy on target) >> 1/η_driver, where η_driver is the wall-plug-to-driver efficiency. For η_driver ~ 10–15%, target gain must exceed ~50–100 to break even. High target gain requires near-perfect compression symmetry and hot-spot formation — this is a central physics challenge. Repetition rate (~1–10 Hz) determines average power.
- **R4**: Each target releases energy as a micro-explosion: neutron burst, x-ray pulse, debris, and a pressure wave. The chamber must absorb this repetitively. Thermal energy is deposited in a liquid or solid first wall/blanket and extracted as heat. The pulsed nature requires chamber recovery between shots — dwell time, gas refill, target injection cycle.
- **R5**: Pulsed neutron bursts activate chamber materials episodically. Tritium is consumed in discrete shots; unburned T must be recovered from target debris. The blast chamber accumulates activation inventory continuously.
- **R6**: The first wall faces repeated impulsive loading: neutron flux, X-ray ablation, plasma debris impact. Material must survive both the peak impulse stress and fatigue from ~10^8 shots over plant lifetime. No material contact with the burning plasma occurs (targets are injected, not held), but standoff distance from explosion to wall must be sufficient to dilute the loading to survivable levels.

Constraints derived:
- DC-011 [NOVEL] (force, R2): confinement_mode=inertial → target_density_required=>200_g_per_cc_compressed — Condition not mappable to table columns
  - *The burn fraction f ~ ρR/(ρR + H_burn), where ρR is the areal density and H_burn is a fuel-dependent constant (~6 g/cm² for D-T). For acceptable burn fraction (>30%), ρR > ~3 g/cm². Starting from solid D-T (~0.2 g/cm³), this requires radial compression by ~1000x in density.*
- DC-012 [NOVEL] (force, R2): compression_ratio=~1000x → implosion_symmetry_required=<1%_rms_nonuniformity — Condition not mappable to table columns
  - *Rayleigh-Taylor instability grows at the decelerating shell surface during implosion. Perturbations with spatial modes grow exponentially, and at the high convergence ratios required, even sub-percent nonuniformities in driver illumination can seed modes that break up the shell before stagnation, preventing hot-spot formation.*
- DC-013 [NOVEL] (force, R2): driver_energy=deposited_in_nanoseconds → driver_peak_power=petawatt_scale — Condition not mappable to table columns
  - *Implosion velocity must exceed ~300 km/s to reach required compression. Driver energy of ~1–2 MJ must be delivered faster than the shock transit time (~few ns), requiring instantaneous power of ~10^14–10^15 W, regardless of driver technology (laser, ion beam, z-pinch, etc.).*
- DC-014 [NOVEL] (force, R3): power_plant=continuous_output → driver_repetition_rate=~1-10_Hz_required, target_factory=required_at_scale — Condition not mappable to table columns
  - *A 1 GW(e) plant at Q~50 and η_thermal~40% needs ~50 MJ/shot at 1 Hz or ~5 MJ/shot at 10 Hz. Each shot requires a precision target with cryogenic D-T ice layer of micron-scale uniformity. Fabricating, storing, and injecting ~10^8 targets/year demands an industrial-scale target factory integrated with the plant.*
- DC-015 [NOVEL] (force, R6): fusion_events=pulsed_microsecond_scale → chamber_wall_standoff=meters_required_for_neutron_flux_dilution — Condition not mappable to table columns
  - *At ~10^9 J/shot yield, the first wall at 5 m radius receives ~3 MJ/m² per pulse in neutrons and X-rays. This impulse must not exceed the material fatigue threshold per cycle. Larger chamber radius distributes the fluence but increases structural cost and driver coupling geometry.*

New questions:
- What driver technology (directed-energy, ion beam, pulsed-power z-pinch) best combines wall-plug efficiency, repetition rate, and beam uniformity for the required implosion symmetry?
- How should the ignition scheme (central hot-spot, fast ignition, shock ignition) trade off between compression uniformity requirements and driver energy?
- How should the blast chamber first wall be protected — dry wall, wetted wall, liquid-metal flow, gas fill — given the repeated impulse loading?
- What is the minimum chamber radius that permits first-wall survival for a given shot yield, and how does this interact with driver focusing geometry?
- How is unburned tritium recovered from target debris, and what is the minimum achievable tritium inventory given target batch processing?
- What repetition rate is achievable with realistic driver technology, and how does this constrain minimum plant size?

**Option: Magnetized Target Confinement (Magneto-Inertial)**

*Thesis*: Embed a magnetic field in a pre-formed plasma target, then compress that target. The magnetic field inhibits electron thermal conduction during compression (electrons are constrained to spiral along field lines, reducing cross-field transport by factors of 10^4 or more), dramatically reducing the energy that must be supplied to heat the plasma to ignition temperature. This allows fusion conditions to be reached at intermediate density — orders of magnitude below pure inertial confinement but far above pure magnetic confinement — using mechanical or electromagnetic drivers that are much more wall-plug efficient than laser or ion-beam drivers. The trade-off: the physics of simultaneously compressing both plasma and magnetic flux, maintaining flux conservation, and avoiding MHD instabilities during rapid compression is complex.

Requirement analysis:
- **R1**: Like inertial confinement, fuel is batch-processed as discrete targets. Magnetic field must be embedded in the target at formation, which constrains fuel geometry (typically a compact torus or field-reversed configuration). D-T is the most accessible fuel; the reduced ignition threshold may eventually open paths to higher-temperature fuels.
- **R2**: The embedded field reduces thermal losses during compression by a factor ~(ρ_e/r_i) (ratio of electron gyroradius to plasma size), so the driver only needs to do hydrodynamic work rather than also resupplying thermal losses. Required compression ratio drops to ~30–100x rather than ~1000x, substantially relaxing the symmetry requirement.
- **R3**: Mechanical piston or electromagnetic coil compression can achieve ~50–80% driver efficiency (vs ~5–15% for laser drivers), enabling net energy at lower target gain. The lower compression ratio also reduces the peak instantaneous power required. This is the primary R3 motivation for this approach.
- **R4**: Pulsed energy release, similar to inertial confinement. However, lower yield per shot and lower peak pressures may allow more conventional first-wall protection. Neutrons still dominate energy output for D-T.
- **R5**: Pulsed neutron bursts as in inertial confinement. The magnetized plasma may retain a fraction of charged fusion products within the target during burn (if the gyroradius of alpha particles is small compared to target size at stagnation), which could improve alpha heating efficiency.
- **R6**: The compression liner (which drives the target implosion) is destroyed each shot. Liner fabrication, like target fabrication in ICF, becomes a plant-scale supply chain requirement. The blast chamber must survive repeated liner-destruction events at lower yield than ICF but potentially at higher repetition rate.

Constraints derived:
- DC-016 [NOVEL] (force, R2): field_embedded_in_plasma=True → magnetic_flux_conserved_during_compression=True, field_scales_as_density_to_2_3=True — Condition not mappable to table columns
  - *In an ideal plasma (high conductivity), magnetic flux is frozen into the fluid (Alfvén's theorem). Compressing the plasma compresses the flux: B ∝ ρ^(2/3) for isotropic compression. Starting from a seeded field of ~1 T, stagnation fields of ~1000 T are reached — far beyond any steady-state magnet.*
- DC-017 [NOVEL] (force, R6): compression_driver=liner_or_mechanical → liner_destroyed_each_shot=True, liner_fabrication_at_scale_required=True — Condition not mappable to table columns
  - *Whether the compressing element is a metal liner driven by high explosive or electromagnetic force, it is driven to velocities of ~1–10 km/s and compressed until the plasma reaches ignition conditions, at which point the liner is destroyed by neutron flux and plasma pressure. Each shot requires a new liner assembly.*
- DC-018 [NOVEL] (force, R2): plasma_formed_and_then_compressed=True → timing_precision_required=sub-microsecond_plasma_formation_and_compression_synchronization — Condition not mappable to table columns
  - *The magnetized plasma target must be formed, reach sufficient field strength and density, and be compressed before the target decays (loses its field through resistive diffusion, which scales as τ_diffuse ~ μ₀σL²). This requires tight synchronization between target formation and compression initiation, typically on microsecond timescales.*
- DC-019 [NOVEL] (force, R2): intermediate_density_regime=10^23_to_10^27_m3 → mhd_instability_growth_timescale=microseconds, requires_active_or_passive_stabilization=True — Condition not mappable to table columns
  - *At intermediate densities, the MHD instability growth time τ_MHD ~ L/v_A is microseconds — slow enough that instabilities must be considered but fast enough that active feedback is impractical. Passive stabilization (wall stabilization by the conducting liner during compression) must be relied upon, which requires the liner to be in close proximity during the compression phase.*

New questions:
- What target configuration (field-reversed configuration, compact torus, magnetized plasma ball) is most stable during rapid compression and how is it formed reliably?
- How should the compression driver be implemented — explosively driven metal liner, electromagnetic z-pinch, laser-driven shocks, or mechanical ram — given the trade-offs in efficiency, repetition rate, and precision?
- At what stagnation density and field strength does the alpha particle gyroradius become small enough that alpha self-heating improves burn efficiency, and how does this affect minimum target size?
- What is the minimum liner-fabrication cost and cycle time consistent with commercial power, and does this approach favor small targets at high repetition rate or large targets at low repetition rate?
- How is flux loss through resistive diffusion during the compression phase managed, and what is the maximum acceptable pre-compression plasma temperature (higher T → lower resistivity → better flux conservation but harder to form)?

**Option: Electrostatic Potential Well Confinement**

*Thesis*: Use electric potential gradients to confine fuel ions. A deep negative potential at the center of the device attracts positive ions, which converge, collide, and fuse. Energy is extracted from the fusion products rather than from a thermal cycle. This approach is appealing in its simplicity — no superconducting magnets, no high-powered drivers — but must overcome a fundamental constraint: you cannot simultaneously confine positive ions (which need a negative central potential) and negative electrons (which are expelled by that same negative potential). Without electron confinement, the plasma is not quasi-neutral, and space charge limits severely bound achievable density. The achievable fusion rate is thus capped well below what is needed for net energy.

Requirement analysis:
- **R1**: Fuel ions are accelerated to fusion-relevant energies; any ion fuel could in principle be used. The low density means reaction rate is low, which in practice limits the approach to fuels with high cross-sections at low energies.
- **R2**: Ion-ion collision rates at achievable densities (limited by space charge) are far below what is required for Lawson criterion satisfaction. More fundamentally, even if two ions collide with fusion-relevant energy, the recirculating current of ions that do not fuse and pass through the center carries kinetic energy that must be repeatedly resupplied against electrode losses.
- **R3**: The recirculating power problem is intrinsic: at any given time, only a small fraction of ions undergo fusion. The remainder recirculate, and a fraction of those are lost to the electrode grid per pass. The ratio of fusion power to grid-loss power has been shown to be insufficient for net energy in any configuration obeying Earnshaw's theorem constraints.
- **R4**: In principle, charged fusion products could be directly converted to electricity if they escape the potential well with excess kinetic energy. However, the low total reaction rate means gross power output is too small.
- **R5**: Low fusion rate means low neutron flux — reduced activation compared to magnetic or inertial approaches. This could be advantageous for non-D-T fuels (p-B11, D-He3) which produce fewer neutrons.
- **R6**: The central electrode faces ion bombardment from recirculating ions, causing erosion. At any commercially meaningful ion current, electrode lifetime becomes a fundamental limitation.

Constraints derived:
- DC-020 [NOVEL] (force, R2): confinement=purely_electrostatic → electron_confinement=impossible_simultaneously_with_ion_confinement — Consequence not mappable to table columns
  - *Earnshaw's theorem states that no stable static equilibrium exists for a charged particle in an electrostatic field in free space. A potential that confines ions (negative center) expels electrons, creating net positive space charge that self-limits the achievable well depth and density far below fusion-relevant values.*
- DC-021 [NOVEL] (force, R3): ion_recirculation=required_for_density_buildup → electrode_ion_loss=unavoidable_grid_transparency_below_100% — Condition not mappable to table columns
  - *Physical grids or magnetic cusps used to create the potential structure intercept a fraction of recirculating ions on every pass. Even at 99.9% transparency, the power deposited in the grid by ion impact exceeds fusion power output for all geometries satisfying the Lawson triple product — this is a direct consequence of the ratio of fusion cross-section to Coulomb scattering cross-section.*
- DC-022 [NOVEL] (force, R2): no_magnetic_field=pure_electrostatic_only → plasma_density=space_charge_limited_orders_of_magnitude_below_lawson — Condition not mappable to table columns
  - *Without a magnetic field to decouple electron and ion motion, quasi-neutrality fails above a density set by the Debye screening length, which at fusion-relevant temperatures and achievable well depths is many orders of magnitude below the density required by the Lawson criterion.*

New questions:
- Can a hybrid approach — using a magnetic field to confine electrons while an electric field confines ions — overcome the Earnshaw's theorem constraint, and what new instabilities does this introduce?
- At what fusion neutron yield does the approach become useful as a neutron source (not a power plant), and does that application change the engineering requirements in a productive direction?
- Is there a regime at very low power (research, isotope production) where the simplicity advantage justifies the inability to achieve net energy?

**Negative space**:
- **Gravitational confinement — relying on gravitational self-attraction to hold plasma together**: The gravitational force is ~10^36 times weaker than the electromagnetic pressure of a hot plasma. The minimum mass for gravitational self-confinement of a fusion plasma exceeds ~10^29 kg (roughly a brown dwarf). This is a stellar phenomenon, not a terrestrial engineering option. (R2)
  - Context: There is no accumulated context that modifies the ratio of gravitational to electromagnetic forces; this is a universal physical constant ratio.
- **Direct material containment — holding plasma in a physical vessel whose walls touch the plasma**: Fusion plasma temperatures of ~10^8 K vastly exceed the melting point of any known material (~4000 K for tungsten). Energy conduction from a plasma at 10^8 K to a material wall at 10^3 K would instantaneously ablate any material before fusion conditions could be sustained. The energy density gradient is ~10^4 orders of magnitude beyond any material's thermal tolerance. (R6)
  - Context: This is non-viable regardless of accumulated context; it is a consequence of the temperature requirement in R2, which sets a lower bound on plasma temperature that is incompatible with material contact.
- **Beam-target fusion at sub-thermal energies — accelerating a beam of ions into a cold dense target, without thermalization**: When an energetic ion enters a dense target, Coulomb collisions with electrons remove its kinetic energy ~10^4 times faster than a fusion collision occurs (ratio of elastic scattering cross-section to fusion cross-section). The vast majority of beam energy thermalizes the target rather than inducing fusion. Net energy is impossible: the energy deposited in heating the target is always far greater than the fusion yield per beam ion. (R3)
  - Context: This constraint follows from the ratio of Coulomb to nuclear cross-sections at sub-thermal energies, which is a fixed physical ratio independent of design choices.
- **Chemical or molecular confinement — using chemical binding or molecular trapping to prevent plasma disassembly**: Fusion requires temperatures of ~10 keV = ~10^8 K, at which all chemical bonds are ionized (bond energies are ~eV = ~10^4 K). Any molecular structure is fully dissociated at fusion temperatures; chemistry operates four orders of magnitude below the energy scales relevant to fusion ignition. R2 renders this non-viable by requiring temperatures that destroy the confinement mechanism. (R2)
  - Context: The temperature requirement of R2 is thermodynamically incompatible with chemical bond energies; no design choice can bridge this gap.
- **Purely radiative confinement — using intense radiation pressure to confine plasma**: Radiation pressure P_rad = u_rad/3 = 4σT^4/3c. At fusion-relevant temperatures (~10 keV), radiation pressure is ~10^13 Pa — comparable to plasma pressure. However, producing a radiation field of this intensity requires the radiation to be trapped inside the plasma (radiation-dominated regime), which only occurs at densities far above any practical target (~10^34 m^-3). No external light source could produce sufficient radiation pressure at reasonable power input. (R3)
  - Context: Creating an externally sustained radiation pressure sufficient to confine a fusion plasma would require more power than the fusion reaction produces, violating R3 regardless of other design choices.

---

#### L1-closed-magnetic-topology-confinement: How should rotational transform be provided: plasma current (with disruption risk and current-drive power), external 3D coils (with manufacturing and maintenance complexity), or a hybrid?

**Accumulated context**:
- Closed magnetic topology confinement — This approach distinguishes itself by using field-line topology to eliminate end losses and achieve continuous steady-state confinement at moderate density, leveraging the confinement-time axis of the Lawson criterion.

*Pending expansion*

#### L1-open-magnetic-topology-confinement-mirro: What is the minimum plug power fraction at which a mirror system can achieve net electricity, including direct conversion efficiency at the ends?

**Accumulated context**:
- Open magnetic topology (mirror) confinement — This approach is distinct in accepting end losses and using active plugging or direct energy conversion to compensate, trading confinement perfection for geometric simplicity and potential direct conversion efficiency.

*Pending expansion*

#### L1-inertial-confinement: What driver technology (directed-energy, ion beam, pulsed-power z-pinch) best combines wall-plug efficiency, repetition rate, and beam uniformity for the required implosion symmetry?

**Accumulated context**:
- Inertial confinement — This approach achieves fusion by satisfying the Lawson criterion through extreme transient density rather than sustained confinement time, creating a fundamentally pulsed plant architecture with discrete targets and a blast chamber.

*Pending expansion*

#### L1-magnetized-target-confinement-magneto-in: What target configuration (field-reversed configuration, compact torus, magnetized plasma ball) is most stable during rapid compression and how is it formed reliably?

**Accumulated context**:
- Magnetized target (magneto-inertial) confinement — This hybrid approach occupies a distinct regime from both pure magnetic and pure inertial confinement, using an embedded field to reduce the compression ratio required for ignition, enabling more efficient mechanical drivers at the cost of complex pulsed plasma formation and liner fabrication logistics.

*Pending expansion*

#### L1-electrostatic-potential-well-confinement: Can a hybrid approach — using a magnetic field to confine electrons while an electric field confines ions — overcome the Earnshaw's theorem constraint, and what new instabilities does this introduce?

**Accumulated context**:
- Electrostatic potential well confinement — This approach is included because it represents a distinct physical mechanism — direct ion focusing via electric fields — but is characterized primarily by its net-energy constraint; it may be viable for non-power applications but cannot satisfy R3 in its pure form.

*Pending expansion*

---

## Constraint Registry

### Unmappable / Novel Variables (22)

| ID | Condition | Consequence | Req | Reasoning | Source |
|---|---|---|---|---|---|
| DC-001 | field_topology=closed_toroidal | geometry=toroidal_or_quasi-toroidal_reactor_shape | R2 | Closed field line topology that prevents end losses requires field lines to curv | L0 |
| DC-002 | field_topology=closed_toroidal | rotational_transform=required_for_radial_confinement | R2 | In a purely toroidal field, grad-B and curvature drifts are in opposite vertical | L0 |
| DC-003 | rotational_transform=provided_by_plasma_current | plasma_current_drive=continuous_power_requirement, disruption_risk=activated | R3 | Toroidal plasma current that provides rotational transform must be driven contin | L0 |
| DC-004 | rotational_transform=provided_by_external_3d_coils | coil_complexity=high_3d_geometry, bootstrap_current_drive=reduced_or_eliminated | R6 | Externally imposed rotational transform via shaped coils eliminates the need for | L0 |
| DC-005 | plasma_beta=exceeds_threshold | mhd_stability=lost, confinement=degraded_or_lost | R2 | The ratio of plasma pressure to magnetic pressure (beta) is bounded above by MHD | L0 |
| DC-006 | closed_geometry=continuous_steady_state | neutron_fluence=continuous_material_damage_accumulation | R5 | Continuous operation at fusion power levels means the first wall and blanket acc | L0 |
| DC-007 | topology=open_linear | loss_cone=always_populated_by_collisions | R2 | In any magnetic mirror, there exists a cone in velocity space (v_parallel/v_tota | L0 |
| DC-008 | end_loss=not_plugged | confinement_time=insufficient_for_lawson_at_feasible_length | R2 | An unplugged mirror with mirror ratio R has confinement time τ ~ (ln R) × τ_ii ( | L0 |
| DC-009 | end_plugging=electrostatic_ambipolar | plug_power=scales_with_plug_potential_times_particle_loss_rate | R3 | An electrostatic plug must maintain a positive potential well in the end cells t | L0 |
| DC-010 | geometry=linear | direct_energy_conversion=physically_accessible | R4 | Ions escaping the end mirrors carry kinetic energy in a directed beam; passing t | L0 |
| DC-011 | confinement_mode=inertial | target_density_required=>200_g_per_cc_compressed | R2 | The burn fraction f ~ ρR/(ρR + H_burn), where ρR is the areal density and H_burn | L0 |
| DC-012 | compression_ratio=~1000x | implosion_symmetry_required=<1%_rms_nonuniformity | R2 | Rayleigh-Taylor instability grows at the decelerating shell surface during implo | L0 |
| DC-013 | driver_energy=deposited_in_nanoseconds | driver_peak_power=petawatt_scale | R2 | Implosion velocity must exceed ~300 km/s to reach required compression. Driver e | L0 |
| DC-014 | power_plant=continuous_output | driver_repetition_rate=~1-10_Hz_required, target_factory=required_at_scale | R3 | A 1 GW(e) plant at Q~50 and η_thermal~40% needs ~50 MJ/shot at 1 Hz or ~5 MJ/sho | L0 |
| DC-015 | fusion_events=pulsed_microsecond_scale | chamber_wall_standoff=meters_required_for_neutron_flux_dilution | R6 | At ~10^9 J/shot yield, the first wall at 5 m radius receives ~3 MJ/m² per pulse  | L0 |
| DC-016 | field_embedded_in_plasma=True | magnetic_flux_conserved_during_compression=True, field_scales_as_density_to_2_3=True | R2 | In an ideal plasma (high conductivity), magnetic flux is frozen into the fluid ( | L0 |
| DC-017 | compression_driver=liner_or_mechanical | liner_destroyed_each_shot=True, liner_fabrication_at_scale_required=True | R6 | Whether the compressing element is a metal liner driven by high explosive or ele | L0 |
| DC-018 | plasma_formed_and_then_compressed=True | timing_precision_required=sub-microsecond_plasma_formation_and_compression_synchronization | R2 | The magnetized plasma target must be formed, reach sufficient field strength and | L0 |
| DC-019 | intermediate_density_regime=10^23_to_10^27_m3 | mhd_instability_growth_timescale=microseconds, requires_active_or_passive_stabilization=True | R2 | At intermediate densities, the MHD instability growth time τ_MHD ~ L/v_A is micr | L0 |
| DC-020 | confinement=purely_electrostatic | electron_confinement=impossible_simultaneously_with_ion_confinement | R2 | Earnshaw's theorem states that no stable static equilibrium exists for a charged | L0 |
| DC-021 | ion_recirculation=required_for_density_buildup | electrode_ion_loss=unavoidable_grid_transparency_below_100% | R3 | Physical grids or magnetic cusps used to create the potential structure intercep | L0 |
| DC-022 | no_magnetic_field=pure_electrostatic_only | plasma_density=space_charge_limited_orders_of_magnitude_below_lawson | R2 | Without a magnetic field to decouple electron and ion motion, quasi-neutrality f | L0 |
