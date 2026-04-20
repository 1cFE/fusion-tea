"""
Orbital Levitated Dipole (D-He3) LCOE Model
============================================
1cFE First Pass Concept Analysis
Concept: Orbital Levitated Dipole — D-He3 aneutronic fuel, power beaming to ground
Company: Zephyr Fusion (San Diego, CA; YC F25)

Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage

This is a free-form LCOE model for an orbital fusion concept with no direct CAS analogue
in the standard 1costingfe framework. The conventional CAS 21–26 accounts (blanket,
shield, thermal cycle, turbine, coolant) are replaced by spacecraft-industry categories:
spacecraft hardware, launch cost, direct energy converter, power beaming transmitter,
and ground rectenna infrastructure.

Cost accounting follows the CAS (Code of Accounts) structure where possible, with
documented overrides for accounts that do not apply or require concept-specific treatment.
Scaling laws follow 1costingfe costing_constants.yaml where applicable.

The model explicitly represents the FOUR-STAGE efficiency chain identified in analysis
Section 2, Challenge 1 (addressing finding F-3):
  Stage 1: Proton deceleration (DEC) — 14.7 MeV proton → DC electricity
  Stage 2: DC-RF conversion (transmitter with phased-array steering)
  Stage 3: Beam collection (free-space propagation)
  Stage 4: RF-DC rectenna conversion
Prior estimates (analysis rough skeleton) omitted Stage 1, understating the full-chain
efficiency penalty by ~2×.

He3 self-breeding feasibility is assessed in analysis Section 2, hypothesis (b) (F-1):
The equimolar D:He3 self-breeding rate is ~7.5% of consumption, requiring a 13:1 D:He3
ratio to approach sufficiency — which destroys the aneutronic advantage. The model treats
He3 cost as the dominant scenario branch parameter.

Economy-of-scale scaling to 1000 MWe reference:
  scaled_lcoe = native_lcoe × (p_native_MWe / 1000) ** (1 - alpha)
  where alpha = 0.6 (standard economy-of-scale exponent, 1costingfe convention)

Key references:
  - analysis.md (this repo) — primary data source for all concept parameters
  - dipole-reactor-heating-energy-conversion.md — OpenStar D-T terrestrial dipole analogue
  - nss-wp-content-uploads-2017-07-space-solar-power-workshop.md — beaming efficiency
  - handwritten exemplar 11-magnetic-mirror.md — DEC efficiency data
  - everycrsreport-reports-r41419.md — He3 supply and pricing
  - ntrs-api-citations-20140003205-downloads-20140003205.md — rectenna cost (SPS analogue)
  - 1costingfe costing_constants.yaml — scaling laws adopted for applicable accounts
  - Bosch & Hale (1992), Nucl. Fusion 32(4):611 — D-He3 and D-D reactivities
"""

import math
from dataclasses import dataclass

# === Reference scales for 1costingfe power-law scaling ===
P_TH_REF = 2500.0   # MW thermal reference (1costingfe)
P_ET_REF = 1100.0   # MW gross electric reference (1costingfe)
P_NET_REF = 1000.0  # MW net electric reference (1costingfe)

# === He3 consumption constant ===
# D + He3 → He4 (3.6 MeV) + p (14.7 MeV), total 18.3 MeV per reaction.
# He3 molar mass: 3.016 g/mol; Avogadro: 6.022e23 /mol.
# Energy per kg He3 = 18.3e6 eV × 1.602e-19 J/eV × (6.022e23/0.003016 kg⁻¹)
# = 18.3e6 × 1.602e-19 × 1.996e26 = 5.851e14 J/kg
# Consumption rate (kg/yr) = P_fus [W] × 3.156e7 [s/yr] / 5.851e14 [J/kg]
# = P_fus_MW × 1e6 × 3.156e7 / 5.851e14 = P_fus_MW × 0.0539 kg/yr/MW
# Ref: Bosch & Hale 1992; analysis.md §Section 7 LCOE skeleton (0.38 kg/yr at 7 MW → checks)
_HE3_CONSUMPTION_KG_PER_MWY = 0.0539   # kg He3 consumed per MW_fusion per year


@dataclass
class OrbitalDipolePlantParams:
    """
    Orbital Levitated Dipole (D-He3) plant parameters.
    All values have source annotations. Uncertainty levels:
      (no tag)             = well-established value with cited source
      MODERATE UNCERTAINTY = reasonable estimate from analogues
      HIGH UNCERTAINTY     = speculative or poorly constrained
    """

    # =========================================================================
    # === PLASMA / FUSION PHYSICS ===
    # =========================================================================

    p_fus_MW: float = 30.0
    """Total fusion power per spacecraft [MW].
    Source: Back-calculated to yield ~1 MWe delivered at baseline efficiency chain.
    At eta_total (full 4-stage chain) ≈ 3.1%, p_fus ≈ 30 MW gives p_net ≈ 1 MWe.
    Zephyr target: "megawatt-class power in orbit" [yc-launch-page.md §Launching Zephyr].
    Ref: analysis.md §Section 5 (target power class). HIGH UNCERTAINTY."""

    Q_sci: float = 10.0
    """Scientific Q = fusion power / heating power.
    Source: OpenStar D-T terrestrial dipole target Q=15 [dipole-reactor-heating-
    energy-conversion.md §Design Point]. D-He3 requires ~10× higher triple product
    than D-T; Q=10 is optimistic for D-He3. Q=5 is more conservative.
    Ref: analysis.md §Section 2 (Challenge 4). HIGH UNCERTAINTY."""

    f_charged_particle: float = 0.80
    """Fraction of D-He3 fusion energy carried by the 14.7 MeV proton (charged particle).
    Source: D + He3 → He4 (3.6 MeV) + p (14.7 MeV), total 18.3 MeV.
    Proton fraction: 14.7/18.3 = 0.803. He4 fraction: 0.197.
    Additional ~10% of total energy from D-D side reactions (50% neutrons/50% charged).
    Net charged particle fraction accounting for D-D: approximately 0.80.
    Ref: Bosch & Hale 1992; standard D-He3 nuclear data. Well-established."""

    f_neutron: float = 0.10
    """Fraction of fusion energy as 2.45 MeV neutrons from D-D side reactions.
    Source: D-D/D-He3 rate ratio ≈ 7.5% at 100 keV [analysis.md §Section 2, hypothesis b].
    50% of D-D reactions produce 2.45 MeV neutrons (D+D → He3+n branch).
    Net neutron energy fraction ≈ 0.075 × 0.5 × (D-D energy/reaction)/(D-He3 energy/reaction).
    Using 0.10 as rounded estimate. Neutrons radiate into space; no shielding required.
    Ref: analysis.md §Section 4 (Advantage: No Neutron Shielding). MODERATE UNCERTAINTY."""

    # =========================================================================
    # === STAGE 1: PROTON DECELERATION (DEC) ===
    # =========================================================================

    eta_dec: float = 0.57
    """Efficiency of direct energy conversion (proton deceleration): fusion-charged-particle
    power → DC electricity [fraction].
    Source: Venetian blind DEC achieved 50–65% for non-fusion ions in 1970s experiments
    [handwritten exemplar 11-magnetic-mirror.md §Direct Energy Capture]. This is an
    UPPER BOUND and likely OPTIMISTIC for 14.7 MeV protons: proton range ~1.4 mm in
    condensed matter exceeds original electrode gaps, requiring qualitatively different
    DEC design. Actual efficiency for 14.7 MeV protons is truly-unknown.
    Ref: analysis.md §Section 2, Challenge 1; §Section 5 (DEC row). HIGH UNCERTAINTY."""

    # =========================================================================
    # === STAGES 2–4: POWER BEAMING (DC → AC at ground) ===
    # =========================================================================

    eta_transmitter: float = 0.15
    """DC-RF conversion efficiency at phased-array transmitter [fraction].
    Source: High-efficiency microwave tubes achieve 70–80% WITHOUT beam steering.
    With phased-array steering (required for LEO tracking): 4–6 dB phase shifter
    losses per element drop efficiency to <20%. Using 15% (center of sub-20% range).
    This is the dominant beaming bottleneck.
    Ref: analysis.md §Section 5 (power beaming rows);
         nss-wp-content-uploads-2017-07-space-solar-power-workshop.md §6.3.
    HIGH UNCERTAINTY — phased-array efficiency at MW scale undemonstrated."""

    eta_beam: float = 0.89
    """Free-space beam collection efficiency (transmitter → rectenna) [fraction].
    Source: ~89% for reference GEO geometry (1 km transmitter, 10×13 km rectenna,
    2.45 GHz, 36,000 km distance). LEO geometry (shorter range, smaller footprint)
    is comparable or slightly better.
    Ref: analysis.md §Section 5; nss-wp-content-uploads-2017-07-space-solar-power-
         workshop.md §6.2. MODERATE UNCERTAINTY."""

    eta_rectenna: float = 0.82
    """RF-DC rectenna conversion efficiency [fraction].
    Source: World record ~90%; practical installed efficiency >80%.
    Most mature beaming sub-component.
    Ref: analysis.md §Section 5;
         nss-wp-content-uploads-2017-07-space-solar-power-workshop.md §6.1."""

    # =========================================================================
    # === HEATING SYSTEM ===
    # =========================================================================

    eta_icrh: float = 0.70
    """ICRH (Ion Cyclotron Resonance Heating) wall-plug efficiency [fraction].
    Source: OpenStar D-T dipole reactor baseline ICRH efficiency = 70%
    [dipole-reactor-heating-energy-conversion.md §Heating Methods, Table 2].
    ECRH alternative: 30–40% wall-plug. Using ICRH as baseline (higher efficiency).
    Ref: analysis.md §Section 3 (TRL 1–2 for heating). MODERATE UNCERTAINTY."""

    # =========================================================================
    # === RECIRCULATING / PARASITIC LOADS ===
    # =========================================================================

    p_cryo_MW: float = 0.10
    """Cryocooler power for HTS dipole coil [MW].
    Source: No space-qualified HTS cryocooler at fusion scale demonstrated.
    LDX terrestrial cryogenic system analogy. Orbital thermal environment
    (passive radiation cooling helps but cryocooler still needed for ~20 K).
    Ref: analysis.md §Section 3 (HTS TRL 2–3). HIGH UNCERTAINTY."""

    p_misc_MW: float = 0.05
    """Housekeeping, I&C, and communications power [MW].
    Source: Analogy to satellite housekeeping loads (typical ~0.1–0.5 kW for
    small satellites; scaled up for fusion instrumentation complexity).
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # === SPACECRAFT MASS BUDGET ===
    # Analysis estimates 5,000–15,000 kg total; 10,000 kg used as baseline.
    # Ref: analysis.md §Section 4 (Launch Capacity).
    # =========================================================================

    m_hts_coil_kg: float = 2000.0
    """HTS dipole coil + cryostat mass [kg].
    Source: Meter-scale REBCO coil for LEO deployment. LDX coil (1T, ~1m) weighed
    ~565 kg; orbital system adds cryostat, thermal shielding, quench protection.
    Ref: analysis.md §Section 1 (LDX heritage); §Section 3 (HTS TRL).
    HIGH UNCERTAINTY — no space-qualified fusion HTS coil designed."""

    m_heating_kg: float = 1500.0
    """ICRH/ECRH heating system mass [kg].
    Source: ICRH systems for tokamaks are ~100–200 kg/MW (hardware only) at
    terrestrial scale; space qualification adds structural and thermal mass.
    Ref: analysis.md §Section 3 (Heating TRL 1–2). HIGH UNCERTAINTY."""

    m_dec_kg: float = 1000.0
    """Direct energy converter hardware mass [kg].
    Source: No space-qualified DEC designed. Venetian blind DEC concept was
    laboratory-scale; orbital scale extrapolated from power density estimates.
    Ref: analysis.md §Section 3 (DEC TRL 2–3). HIGH UNCERTAINTY."""

    m_transmitter_kg: float = 2500.0
    """Phased-array microwave transmitter mass [kg].
    Source: SPS concepts use ~1–5 kg/kW for transmitter subsystem; at 10 MW
    transmitted power (before beam/rectenna losses), ~2,500 kg is a rough estimate.
    Ref: analysis.md §Section 5 (power beaming). HIGH UNCERTAINTY."""

    m_bus_kg: float = 1000.0
    """Spacecraft bus mass (structure, thermal, ADCS, comms, power distribution) [kg].
    Source: Analogy to large LEO spacecraft bus at ~1 tonne class.
    MODERATE UNCERTAINTY."""

    m_cryo_kg: float = 1500.0
    """Cryocooler + thermal radiator mass [kg].
    Source: Space cryocoolers (Stirling, pulse-tube) at sub-kW cooling power: ~50–200 kg
    each; arrays needed for HTS coil cooling. Radiator panels: additional mass.
    Ref: analysis.md §Section 3 (HTS TRL 2–3). HIGH UNCERTAINTY."""

    m_fuel_system_kg: float = 500.0
    """He3 + D fuel tanks, injection system, and fuel management hardware [kg].
    Source: Small-scale fuel storage and gas injection for laboratory scale.
    He3 consumption rate ~1.6 kg/yr; pressurized storage at modest mass.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # === LAUNCH ===
    # =========================================================================

    launch_cost_per_kg: float = 2700.0
    """Launch cost to LEO [$/kg].
    Source: Falcon 9 rideshare pricing (~$2,700/kg to LEO) as documented baseline.
    Starship target: ~$100–200/kg (not yet operational).
    Ref: analysis.md §Section 4 (Launch Capacity); §Section 5 (Available Parameters)."""

    n_spacecraft: int = 1
    """Number of orbital spacecraft (each delivering p_net_MW to separate ground stations).
    Source: Baseline concept is a single-spacecraft demonstrator.
    Analysis targets MW-class power — single unit."""

    # =========================================================================
    # === SPACECRAFT HARDWARE COSTS (concept-specific CAS22 overrides) ===
    # Note: these are spacecraft fabrication costs, distinct from launch cost.
    # The analysis used $20M as an explicit placeholder (labeled too low);
    # this model provides a component-level breakdown.
    # Ref: analysis.md §Section 7 (spacecraft fabrication cost $20M placeholder).
    # =========================================================================

    c_hts_coil_M: float = 15.0
    """HTS dipole coil system fabrication + space qualification cost [$M].
    Source: REBCO tape for small orbital coil: ~$5M hardware.
    Space qualification (thermal cycling, radiation testing, quench protection):
    ~$10M for first unit. Subsequent units: ~$5M.
    Ref: analysis.md §Section 4 (REBCO supply chain); §Section 3 (HTS TRL).
    HIGH UNCERTAINTY — no precedent for space-qualified fusion HTS coil."""

    c_heating_M: float = 15.0
    """ICRH heating system fabrication + space qualification cost [$M].
    Source: Terrestrial ITER ICRH (20 MW): ~$70M → ~$3.5M/MW.
    Space qualification multiplier ~3×: ~$10M/MW. At ~3 MW heating power: ~$15M FOAK.
    Ref: dipole-reactor-heating-energy-conversion.md §Heating Methods.
    HIGH UNCERTAINTY — no space-qualified fusion heating system designed."""

    c_dec_M: float = 10.0
    """Direct energy converter hardware cost [$M].
    Source: 1costingfe dec_base = $100M at 400 MWe DEC output (reference scale).
    Scaling: $100M × (p_dec_out_MW / 400)^0.7. At ~14 MW DEC output: ~$10M.
    Additional FOAK development premium included in base estimate.
    Ref: 1costingfe costing_constants.yaml (dec_base=100, scale^0.7).
    HIGH UNCERTAINTY — no commercial DEC supply; 1970s Venetian blind never scaled."""

    c_transmitter_M: float = 20.0
    """Phased-array microwave transmitter cost [$M].
    Source: No commercial MW-scale space power beaming transmitter manufactured.
    JAXA/USN small-scale experiments at kW level. Cost extrapolated from phased-array
    radar analogy: ~$2,000/kg × 2,500 kg mass estimate + integration.
    Ref: analysis.md §Section 3 (DEC/beaming TRL 2–3). HIGH UNCERTAINTY."""

    c_bus_M: float = 5.0
    """Spacecraft bus fabrication cost [$M].
    Source: Commercial satellite buses at 500–2,000 kg: $3–10M per unit (NOAK).
    FOAK premium for novel fusion-compatible bus design.
    MODERATE UNCERTAINTY."""

    c_cryo_M: float = 6.0
    """Cryocooler + thermal radiator fabrication + integration cost [$M].
    Source: Space-qualified Stirling cryocoolers: ~$1–2M each; multiple needed
    + radiator panel fabrication + thermal bus integration.
    Ref: analysis.md §Section 3 (cryocooler noted as missing-at-scale).
    HIGH UNCERTAINTY."""

    c_electronics_M: float = 4.0
    """Power electronics, onboard I&C, and comms hardware cost [$M].
    Source: Analogy to high-power satellite electronics and mission avionics.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # === GROUND INFRASTRUCTURE ===
    # =========================================================================

    rectenna_cost_per_MW_M: float = 2.0
    """Ground rectenna field cost per MWe received [M$/MWe].
    Source: GW-class GEO SPS analogue: ~$2B total for 10×13 km elliptical receiving
    field (34 km² including keep-out zone) → $2M/MW.
    LEO concept: smaller footprint due to shorter transmission distance; cost
    comparable per MW of received power.
    Ref: analysis.md §Section 2, Challenge 6; §Section 7 Cross-Concept Notes;
         ntrs-api-citations-20140003205-downloads-20140003205.md §VI.
    MODERATE UNCERTAINTY — SPS analogue not directly applicable to LEO fusion."""

    c_ground_control_M: float = 5.0
    """Ground control + mission operations facility cost [$M].
    Source: Analogy to small satellite operations facilities.
    Includes: tracking antennas, control room, grid-tie switchgear.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # === FUEL ===
    # =========================================================================

    he3_cost_per_kg: float = 30.0e6
    """He3 market purchase cost [$/kg].
    Source: Current market allocation price ~$5,000–6,000/std L
    (~$28–34M/kg). Using $30M/kg as central estimate.
    Scenario branch: self-bred He3 ≈ $0 variable cost (see analysis §2, hypothesis b).
    Pre-shortage market price was $40–85/std L (subsidized); post-2011 shortage:
    $5,000–6,000/std L [everycrsreport-reports-r41419.md §Production Costs].
    Ref: analysis.md §Section 2, Challenge 2; §Section 5 (He3 price rows).
    MODERATE UNCERTAINTY — current allocation price; commercial scale unknown."""

    burn_fraction: float = 0.05
    """Fraction of injected He3 fuel burned per pass [fraction].
    Source: 1costingfe costing_constants.yaml default (burn_fraction=0.05).
    Typical fusion burn-up fraction. MODERATE UNCERTAINTY."""

    fuel_recovery: float = 0.90
    """Fraction of unburned He3 recovered and recycled [fraction].
    Source: 1costingfe costing_constants.yaml default (fuel_recovery=0.95).
    Using 0.90 as slightly more conservative for orbital fuel management.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # === OPERATIONS ===
    # =========================================================================

    plant_availability: float = 0.90
    """Plant capacity factor / availability.
    Source: Orbital steady-state concept with no day/night cycle, no weather.
    Levitated dipole is inherently steady-state [analysis.md §Section 7].
    10% downtime for orbit maintenance, anomaly recovery, and scheduled checks.
    Ref: analysis.md §Section 5 (Operation Mode: steady-state). HIGH UNCERTAINTY
    — no orbital fusion precedent; debris/radiation events uncharacterized."""

    plant_lifetime_years: float = 10.0
    """Plant economic lifetime [years].
    Source: Analysis rough LCOE skeleton uses 10-year asset life
    [analysis.md §Section 7]. Satellite lifetimes: typically 10–15 years.
    HTS coil radiation lifetime in LEO is uncertain."""

    noak: bool = False
    """Nth-of-a-kind (True) vs First-of-a-kind (False).
    Source: Concept is pre-prototype; FOAK costs apply (higher contingency,
    development overhead). Ref: 1costingfe CAS29 convention."""

    # =========================================================================
    # === O&M ===
    # =========================================================================

    orbital_om_frac_annual: float = 0.03
    """Annual O&M cost as fraction of overnight capital cost.
    Source: Analysis LCOE skeleton uses 3% of CAPEX per year [analysis.md §Section 7].
    Orbital O&M has no precedent in fusion LCOE literature. Includes: ground ops
    staffing, tracking station upkeep, anomaly recovery. HIGH UNCERTAINTY."""

    # =========================================================================
    # === FINANCIAL ===
    # =========================================================================

    interest_rate: float = 0.08
    """Real discount rate (WACC) [fraction].
    Source: 1costingfe default. Appropriate for early-stage concept. Standard."""

    construction_time_years: float = 3.0
    """Deployment timeline (spacecraft manufacturing + launch) [years].
    Source: No construction site; satellite manufacturing timelines ~2–4 years.
    MODERATE UNCERTAINTY."""

    # =========================================================================
    # === PRIVATE PARAMETERS (used in CAS22 scaling only) ===
    # =========================================================================

    plasma_radius_m: float = 20.0
    """Plasma separatrix radius [m].
    Source: "Magnetized volume exceeding ITER" claim [yc-launch-page.md].
    ITER plasma radius ~2 m; volume scales R³ → separatrix R ~ tens of meters.
    Range: 10–50 m per dossier [analysis.md §Section 5].
    HIGH UNCERTAINTY — unverified; no Zephyr design disclosed."""

    # =========================================================================

    def _compute_power(self) -> dict:
        """Layer 1: Power balance — 4-stage efficiency chain (D-He3 orbital dipole)."""
        r = {}

        # --- Fusion and particle power ---
        p_fus = self.p_fus_MW
        r["p_fus"] = p_fus
        r["Q_sci"] = self.Q_sci

        # Charged particle power (14.7 MeV proton + 3.6 MeV He4, combined ≈ 80%)
        p_charged = self.f_charged_particle * p_fus
        r["p_charged"] = p_charged

        # Neutron power (2.45 MeV from D-D side reactions, radiates into space)
        p_neutron = self.f_neutron * p_fus
        r["p_neutron_space"] = p_neutron

        # Bremsstrahlung / radiation loss (radiated from plasma, not captured)
        f_radiation = max(0.0, 1.0 - self.f_charged_particle - self.f_neutron)
        r["p_radiation_loss"] = f_radiation * p_fus

        # --- Stage 1: Proton deceleration (DEC) → DC electricity ---
        # p_th maps to DEC input (charged particle power)
        r["p_th"] = p_charged  # conventional alias: "thermal power" = DEC input
        p_dec_out = self.eta_dec * p_charged
        r["p_dec_out_DC"] = p_dec_out
        r["p_et"] = p_dec_out  # conventional alias: "gross electric" = DEC DC output

        # --- Heating system (draws from onboard DC bus) ---
        p_heat_fusion = p_fus / self.Q_sci   # fusion heating power required [MW]
        p_heat_wall = p_heat_fusion / self.eta_icrh  # wall-plug power for heating
        r["p_heat_fusion_MW"] = p_heat_fusion
        r["p_heat_wall_MW"] = p_heat_wall

        # --- Total recirculating power (taken from DEC DC output before beaming) ---
        p_recirc = p_heat_wall + self.p_cryo_MW + self.p_misc_MW
        r["p_recirc"] = p_recirc
        r["p_recirc_breakdown"] = {
            "heating": p_heat_wall,
            "cryocooler": self.p_cryo_MW,
            "housekeeping": self.p_misc_MW,
        }

        # --- Power available for beaming ---
        p_beam_in = max(0.0, p_dec_out - p_recirc)
        r["p_beam_in"] = p_beam_in

        # --- Stages 2–4: Power beaming (DC → RF → free space → rectenna AC) ---
        p_after_transmitter = self.eta_transmitter * p_beam_in
        p_after_beam = self.eta_beam * p_after_transmitter
        p_net = self.eta_rectenna * p_after_beam
        r["p_after_transmitter"] = p_after_transmitter
        r["p_after_beam"] = p_after_beam
        r["p_net"] = p_net

        # Multi-module totals
        n = self.n_spacecraft
        r["p_net_plant"] = p_net * n
        r["p_et_plant"] = p_dec_out * n
        r["p_th_plant"] = p_charged * n

        # --- Derived figures of merit ---
        eta_beaming_3stage = self.eta_transmitter * self.eta_beam * self.eta_rectenna
        eta_full_4stage = self.eta_dec * eta_beaming_3stage  # before recirculating
        # Net end-to-end (accounting for recirculating power)
        eta_net_to_fus = p_net / p_fus if p_fus > 0 else 0.0
        r["eta_dec"] = self.eta_dec
        r["eta_beaming_3stage"] = eta_beaming_3stage
        r["eta_full_4stage_charged"] = eta_full_4stage
        r["eta_net_to_fus"] = eta_net_to_fus

        # Engineering Q = p_fus / total recirculating power
        r["Q_eng"] = p_fus / p_recirc if p_recirc > 0 else float('inf')

        # Recirculating fraction = recirc / DEC output
        r["recirc_fraction"] = p_recirc / p_dec_out if p_dec_out > 0 else 1.0

        # He3 consumption rate [kg/yr] — derived from fusion power
        r["he3_consumption_kg_per_yr"] = p_fus * _HE3_CONSUMPTION_KG_PER_MWY
        # Effective He3 purchase rate (accounting for burn fraction and recycling)
        # make-up He3 needed = consumed × (1 - burned_fraction × recovery_correction)
        # Per pass: fraction burned = burn_fraction; fraction recovered unburned = fuel_recovery × (1-burn_fraction)
        # Net loss per pass = 1 - fuel_recovery × (1 - burn_fraction) ≈ burn_fraction + (1-fuel_recovery)×(1-burn_fraction)
        # Effective consumption ≈ (total He3 throughput) × (1 - fuel_recovery × (1 - burn_fraction)) / burn_fraction
        # Simplified: effective = he3_consumption / (burn_fraction × fuel_recovery) ... (no, that's overcomplicated)
        # Analysis uses simple consumption rate. Keep it simple:
        # He3 consumed = p_fus × 0.0539 kg/yr. Makeup rate = consumption × (1 - fuel_recovery*(1-burn_fraction))/burn_fraction
        # Using analysis §Section 7 approach: just use consumption directly.
        r["he3_purchase_kg_per_yr"] = r["he3_consumption_kg_per_yr"]  # conservative (no recycling credit)

        return r

    def _compute_geometry(self, power: dict) -> dict:
        """Layer 2: Spacecraft mass budget and derived geometric parameters."""
        r = {}

        # --- Spacecraft mass budget ---
        r["m_hts_coil_kg"] = self.m_hts_coil_kg
        r["m_heating_kg"] = self.m_heating_kg
        r["m_dec_kg"] = self.m_dec_kg
        r["m_transmitter_kg"] = self.m_transmitter_kg
        r["m_bus_kg"] = self.m_bus_kg
        r["m_cryo_kg"] = self.m_cryo_kg
        r["m_fuel_system_kg"] = self.m_fuel_system_kg

        m_total = (self.m_hts_coil_kg + self.m_heating_kg + self.m_dec_kg
                   + self.m_transmitter_kg + self.m_bus_kg + self.m_cryo_kg
                   + self.m_fuel_system_kg)
        r["m_spacecraft_total_kg"] = m_total

        # Launch cost per spacecraft
        r["launch_cost_M"] = m_total * self.launch_cost_per_kg / 1e6

        # Specific power [W/kg] — key figure of merit for orbital power concepts
        p_net = power["p_net"]
        r["specific_power_W_kg"] = (p_net * 1e6 / m_total) if m_total > 0 else 0.0

        # Plasma volume (order-of-magnitude, dipole geometry ≈ sphere at separatrix)
        r_sep = self.plasma_radius_m
        r["plasma_volume_m3"] = (4.0 / 3.0) * math.pi * r_sep**3

        # Rectenna area (MW-scale LEO: shorter range allows smaller footprint)
        # SPS analogue at GW-scale: 34 km²; scale as P^0.5 (beam spread geometry)
        # MW-scale: ~34 km² × (p_net/1000)^0.5 × (500km/36000km)^0.25 (range correction)
        # Simplified rough estimate: 1 km² per 100 MWe at LEO, or ≈ 10,000 m²/MWe
        # Ref: ntrs-api-citations-20140003205 §VI (GW-scale SPS rectenna)
        r["rectenna_area_m2"] = max(1000.0, p_net * 1e4)  # ASSUMED: 1 ha/MWe at LEO scale

        return r

    def _compute_cas22(self, power: dict, geom: dict) -> dict:
        """Layer 3: CAS22 Reactor Plant Equipment — spacecraft hardware accounts.
        Per-module accounts map to individual spacecraft subsystems.
        Plant-wide accounts map to shared ground infrastructure.
        Scaling laws from 1costingfe costing_constants.yaml adopted where applicable."""
        r = {}

        p_dec_out = max(power["p_dec_out_DC"], 0.1)
        p_fus = max(power["p_fus"], 1.0)
        p_net = max(power["p_net"], 0.001)

        # ---- Per-module spacecraft accounts ----

        # C220101: First Wall / Blanket — NOT APPLICABLE
        # D-He3 orbital concept has no blanket; DD neutrons radiate into space.
        # Ref: analysis.md §Section 4 (No Tritium Breeding Infrastructure Required).
        r["C220101"] = 0.0

        # C220102: Shield — NOT APPLICABLE
        # No 14 MeV neutrons; 2.45 MeV DD neutrons radiate into space without shielding.
        # Ref: analysis.md §Section 4 (No 14 MeV Neutron Shielding Requirement).
        r["C220102"] = 0.0

        # C220103: Magnet system — HTS dipole coil
        # OVERRIDE: direct spacecraft hardware cost (not kAm scaling — orbital scale
        # is fundamentally different from terrestrial tokamak magnets).
        # Includes: REBCO coil winding, cryostat, quench protection, space qualification.
        r["C220103"] = self.c_hts_coil_M

        # C220104: Supplementary Heating — ICRH/ECRH system
        # OVERRIDE: direct spacecraft heating hardware cost.
        # For space-qualified ICRH: ~$10M/MW at MW scale (3× terrestrial + space qual).
        # Ref: dipole-reactor-heating-energy-conversion.md §Heating Methods.
        r["C220104"] = self.c_heating_M

        # C220105: Primary Structure — spacecraft bus
        # OVERRIDE: spacecraft structural bus, including ADCS, thermal, and comms.
        r["C220105"] = self.c_bus_M

        # C220106: Vacuum System — NOT APPLICABLE
        # Space provides vacuum inherently; no vacuum vessel or pumping system needed.
        # Ref: analysis.md §Section 7 (No vacuum vessel — key differentiator).
        r["C220106"] = 0.0

        # C220107: Power Supplies — spacecraft power electronics
        # OVERRIDE: onboard power management, DC bus, conditioning electronics.
        # Standard spacecraft power electronics: ~$500k/kW at small scale.
        # Using fixed estimate for coherence.
        r["C220107"] = self.c_electronics_M

        # C220108: Target Factory — NOT APPLICABLE (steady-state fusion, no targets).
        r["C220108"] = 0.0

        # C220109: Direct Energy Converter (DEC) — proton deceleration hardware
        # Scaled from 1costingfe dec_base ($100M at 400 MWe DEC output) using ^0.7 exponent.
        # At p_dec_out, DEC capital = dec_base × (p_dec_out / 400)^0.7
        # Ref: 1costingfe costing_constants.yaml (dec_base=100.0, scale exponent 0.7).
        # Note: 1costingfe baseline was calibrated for non-orbital DEC; space qualification
        # premium is embedded in the FOAK estimate.
        dec_base_M = 100.0      # M$ at 400 MWe output (1costingfe)
        p_dec_ref_MW = 400.0    # Reference DEC output power
        r["C220109"] = dec_base_M * (p_dec_out / p_dec_ref_MW) ** 0.7
        # Enforce minimum (FOAK development cost floor even at low power)
        r["C220109"] = max(r["C220109"], self.c_dec_M)

        # C220110: Remote Handling / Maintenance Equipment
        # Minimal: orbital spacecraft has no in-orbit servicing capability planned.
        # Ground crew tooling + integration test equipment only.
        r["C220110"] = 2.0  # ASSUMED: $2M for ground integration tooling

        # C220113: Phased-array transmitter fabrication
        # OVERRIDE: direct spacecraft hardware cost for MW-scale phased-array transmitter.
        # ~$2,000/kg × 2,500 kg mass estimate; the most technically novel component in
        # the power chain. Not captured in C220107 (power electronics/I&C — covers
        # onboard DC bus and I&C only) or C220109 (DEC — covers proton deceleration).
        # Ref: analysis.md §Section 5 (power beaming); mass budget m_transmitter_kg.
        r["C220113"] = self.c_transmitter_M

        # C220111: Installation labor (spacecraft integration, TVAC testing, launch prep)
        # Standard installation fraction applied to spacecraft hardware subtotal.
        # Ref: 1costingfe costing_constants.yaml (installation_frac=0.14).
        hardware_subtotal = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110", "C220113"])
        r["C220111"] = 0.14 * hardware_subtotal
        # Note: space integration has ~2× higher integration cost than terrestrial;
        # 14% still likely an underestimate for a FOAK fusion spacecraft.

        # C220112: Isotope Separation / Fuel System
        # He3 + D on-board fuel storage and injection system (not isotope separation per se).
        # Small pressurized vessels, mass flow controllers, injection nozzles.
        # ASSUMED based on gas handling system analogy.
        r["C220112"] = 2.0  # ASSUMED: $2M for orbital fuel handling system

        # Per-module subtotal
        r["CAS22_per_module"] = sum(r[k] for k in [
            "C220101", "C220102", "C220103", "C220104", "C220105",
            "C220106", "C220107", "C220108", "C220109", "C220110",
            "C220111", "C220112", "C220113"])

        # ---- Plant-wide (ground infrastructure) accounts ----

        # C220200: Coolant Systems — NOT APPLICABLE (no thermal cycle)
        r["C220200"] = 0.0

        # C220300: Auxiliary Cooling / Cryoplant
        # In this context: spacecraft cryocooler + thermal radiator system.
        # Cost based on 1costingfe cryoplant scaling: 200 × (p_cryo/30)^0.7
        # Ref: 1costingfe costing_constants.yaml (C220302 formula).
        p_cryo_total = self.p_cryo_MW * self.n_spacecraft
        r["C220300"] = max(2.0, 200.0 * (max(p_cryo_total, 0.01) / 30.0) ** 0.7)
        # This covers the cryocooler hardware cost; thermal radiator panels included.

        # C220400: Radioactive Waste Management — NOT APPLICABLE
        # DD neutrons radiate into space; no activated components require handling.
        # Ref: analysis.md §Section 4 (No 14 MeV Neutron Shielding — advantage).
        r["C220400"] = 0.0

        # C220500: He3 Fuel Handling (ground side)
        # He3 procurement logistics, ground storage, launch-pad loading.
        # Using 1costingfe fuel_handling_dhe3_base = $40M at 1 GWe, scaled by ^0.7.
        # Ref: 1costingfe costing_constants.yaml (fuel_handling_dhe3_base=40.0).
        p_net_total = p_net * self.n_spacecraft
        r["C220500"] = 40.0 * (max(p_net_total, 0.001) / 1000.0) ** 0.7

        # C220600: Ground Control Systems
        # Mission operations center, tracking antennas, network.
        r["C220600"] = self.c_ground_control_M

        # C220700: Instrumentation & Control (onboard + ground segment)
        # 1costingfe formula: 85.0 × (p_th_total/3500)^0.65
        # Adapted: I&C scales with plant complexity.
        p_th_total = power["p_th"] * self.n_spacecraft
        r["C220700"] = 85.0 * (max(p_th_total, 1.0) / 3500.0) ** 0.65

        # Plant-wide subtotal
        r["CAS22_plant_wide"] = sum(r[k] for k in [
            "C220200", "C220300", "C220400", "C220500", "C220600", "C220700"])

        # Total CAS22
        r["CAS22"] = r["CAS22_per_module"] * self.n_spacecraft + r["CAS22_plant_wide"]

        return r

    def _compute_costs(self, power: dict, geom: dict, cas22: dict) -> dict:
        """Layer 4: CAS10–60 capital costs — adapted for orbital concept."""
        r = {}
        p_net = max(power["p_net"], 0.001)
        p_net_plant = max(power["p_net_plant"], 0.001)
        p_et = max(power["p_et"], 0.001)

        # === CAS10: Pre-construction / Licensing ===
        # D-He3 = least restrictive fuel class; but orbital nuclear raises new issues.
        # Orbital nuclear safety (IAEA Outer Space Nuclear Safety Guidelines 2023) adds
        # regulatory overhead beyond NRC jurisdiction for terrestrial D-He3.
        # Ref: 1costingfe costing_constants.yaml (licensing_cost_dhe3=1.0M).
        # Using 3× for orbital nuclear complexity.
        site_permits = 1.0      # Minimal (no terrestrial nuclear site)
        plant_studies = 8.0 if not self.noak else 2.0  # FOAK development studies
        plant_permits = 2.0     # FCC spectrum licensing for MW beaming
        plant_reports = 1.0
        other_precon = 1.0
        orbital_nuclear_licensing = 5.0  # IAEA + international coordination (ASSUMED)
        r["CAS10"] = (site_permits + plant_studies + plant_permits + plant_reports
                      + other_precon + orbital_nuclear_licensing)

        # === CAS21: Ground facilities (replaces conventional buildings) ===
        # No reactor building, turbine building, or hot cell.
        # Minimal ground station + grid tie + operations facility.
        # Ref: analysis.md §Section 7 (no building — advantage of orbital concept).
        # Using D-He3 building cost scale from 1costingfe, heavily reduced:
        # site_improvements: $75M at 1 GWe → scaled down; control_room: $12M at 1 GWe
        # Ref: 1costingfe costing_constants.yaml building_costs (dhe3 column).
        r["CAS21"] = max(2.0, 10.0 * (p_net_plant / 1000.0) ** 0.5)  # ASSUMED: minimal footprint

        # === CAS22: Spacecraft equipment (computed separately) ===
        r["CAS22"] = cas22["CAS22"]

        # === CAS23: Power beaming transmitter (replaces turbine plant) ===
        # The phased-array transmitter is the DC→RF conversion stage.
        # Cost included in C220107 (CAS22). This account captures the
        # integration and system-level beaming overhead.
        # OVERRIDE: direct cost from spacecraft hardware (transmitter is in CAS22).
        # Putting a small residual here for ground-side beam management hardware.
        r["CAS23"] = self.c_transmitter_M  # Phased array: primary cost in CAS22; duplicate avoidance
        # CORRECTION: to avoid double-counting with C220107, set this to 0.
        # The transmitter cost is captured in C220107 (electronics) and C220109 (DEC).
        # CAS23 here represents ONLY the ground-side beaming receive/control hardware.
        r["CAS23"] = 2.0  # ASSUMED: $2M ground-side RF management + spectrum monitoring

        # === CAS24: Ground rectenna + grid connection (replaces electric plant) ===
        # Rectenna field is the primary revenue-generating ground infrastructure.
        # Cost: ~$2M/MWe (SPS analogue, ref above).
        r["CAS24"] = self.rectenna_cost_per_MW_M * p_net_plant
        # Add grid-tie: ~$0.08M/MWe (from 1costingfe electric_per_mw = 0.08418)
        r["CAS24"] += 0.084 * p_net_plant

        # === CAS25: Miscellaneous ground equipment ===
        r["CAS25"] = max(0.5, 0.05 * p_net_plant)

        # === CAS26: Spacecraft thermal management ===
        # Cryocooler + radiator panel system (primary thermal control).
        # Cost included in C220300. Residual here: thermal testing + ground support.
        r["CAS26"] = 1.0  # ASSUMED: $1M thermal ground support equipment

        # === CAS27: Special Materials (He3 startup inventory) ===
        # Using 1costingfe startup_fuel_dhe3 = $10M at 1 GWe, scaled.
        # For ~1 MWe: first-year He3 inventory at market price.
        he3_startup_kg = power["he3_purchase_kg_per_yr"] * self.n_spacecraft
        r["CAS27"] = he3_startup_kg * self.he3_cost_per_kg / 1e6

        # === CAS28: Digital twin ===
        # Ref: 1costingfe costing_constants.yaml (digital_twin=5.0M)
        r["CAS28"] = 5.0

        # === CAS29: Contingency on direct costs ===
        # Ref: 1costingfe convention: FOAK=10%, NOAK=0%.
        cas20_pre_contingency = sum(r[k] for k in [
            "CAS21", "CAS22", "CAS23", "CAS24", "CAS25", "CAS26", "CAS27", "CAS28"])
        contingency_rate = 0.0 if self.noak else 0.10
        r["CAS29"] = contingency_rate * cas20_pre_contingency

        # === CAS20: Total Direct Costs ===
        r["CAS20"] = cas20_pre_contingency + r["CAS29"]

        # === CAS30: Integration / Indirect Costs ===
        # For orbital concept: system integration, test campaigns, regulatory interface.
        # 1costingfe: indirect_fraction = 0.20, scaled by construction time.
        ref_time = 6.0
        r["CAS30"] = 0.20 * r["CAS20"] * (self.construction_time_years / ref_time)

        # === CAS40: Owner's Costs ===
        # Licensee preparation, regulatory engagement, insurance during deployment.
        # 1costingfe: owner_cost_dhe3 = $23M at 1 GWe, scale ^0.5.
        r["CAS40"] = 23.0 * (p_net_plant / 1000.0) ** 0.5

        # === CAS50: Launch + Supplementary ===
        # Launch cost is the primary CAS50 item for this concept.
        # This maps most naturally here as the "deployment" analog.
        launch_total = geom["launch_cost_M"] * self.n_spacecraft
        spare_parts = 0.015 * r["CAS20"]   # 1costingfe shipping_frac applied
        decom = max(1.0, 65.0 * (p_net_plant / 1000.0))  # 1costingfe decom_provision_dhe3
        r["CAS50"] = launch_total + spare_parts + decom
        r["CAS50_launch"] = launch_total
        r["CAS50_decom"] = decom

        # === Overnight Capital ===
        overnight = r["CAS10"] + r["CAS20"] + r["CAS30"] + r["CAS40"] + r["CAS50"]
        r["overnight_capital"] = overnight

        # === CAS60: Interest During Construction (IDC) ===
        i = self.interest_rate
        T = self.construction_time_years
        if i > 0 and T > 0:
            f_idc = ((1 + i) ** T - 1) / (i * T) - 1
        else:
            f_idc = 0.0
        r["CAS60"] = f_idc * overnight
        r["f_IDC"] = f_idc

        # === Total Capital ===
        r["total_capital"] = overnight + r["CAS60"]

        # Specific capital cost ($/kWe, per delivered net MW)
        if power["p_net_plant"] > 0:
            r["specific_capital_USD_per_kWe"] = (
                r["total_capital"] * 1e6 / (power["p_net_plant"] * 1e3)
            )
        else:
            r["specific_capital_USD_per_kWe"] = float("inf")

        return r

    def _compute_economics(self, power: dict, costs: dict) -> dict:
        """Layer 5: CAS70–90 annualized costs and LCOE."""
        r = {}
        p_net_plant = power["p_net_plant"]

        # Capital Recovery Factor
        i = self.interest_rate
        n = self.plant_lifetime_years
        crf = i * (1 + i) ** n / ((1 + i) ** n - 1)
        r["CRF"] = crf

        # === CAS90: Annualized Capital Charge ===
        r["CAS90"] = crf * costs["total_capital"]  # M$/yr

        # === CAS71: Annual O&M ===
        # 1costingfe formula for D-He3: om_cost_dhe3 = $26M at 1 GWe, scale ^0.5.
        # But orbital O&M has no precedent; using fraction-of-capital approach per analysis.
        # Analysis §Section 7: "O&M (3% of CAPEX/yr)".
        annual_om = self.orbital_om_frac_annual * costs["overnight_capital"]
        r["CAS71"] = annual_om  # M$/yr

        # === CAS72: Scheduled Replacement ===
        # HTS coil replacement after radiation lifetime (truly-unknown; no DPA data).
        # D-He3 core lifetime from 1costingfe: 30 FPY (minimal neutron flux).
        # For orbital concept, radiation damage from Van Allen belts may dominate.
        # Using 10-year coil replacement cycle (= plant lifetime; no mid-life replacement).
        core_lifetime_FPY = 30.0  # D-He3 benchmark (minimal neutron damage)
        effective_yr = core_lifetime_FPY / self.plant_availability
        n_replacements = max(0, int(math.ceil(n / effective_yr)) - 1)
        # Replacement cost = HTS coil cost (dominant replaceable component)
        replacement_cost_M = self.c_hts_coil_M
        pv_replacements = 0.0
        for k in range(1, n_replacements + 1):
            yr = k * effective_yr
            if yr < n:
                pv_replacements += replacement_cost_M / (1 + i) ** yr
        r["CAS72"] = crf * pv_replacements
        r["n_coil_replacements"] = n_replacements

        r["CAS70"] = r["CAS71"] + r["CAS72"]

        # === CAS80: Annualized Fuel Costs (He3 dominated) ===
        # He3 fuel is the dominant variable cost in the pessimistic scenario.
        # Ref: analysis.md §Section 2 (Challenge 2); §Section 7 LCOE skeleton.
        annual_he3_kg = power["he3_purchase_kg_per_yr"] * self.n_spacecraft
        annual_he3_cost_M = annual_he3_kg * self.he3_cost_per_kg / 1e6  # M$/yr

        # Deuterium co-fuel (negligible cost)
        # Deuterium ≈ 1 D per D-He3 reaction; mass ≈ 2/3 of He3 mass consumed.
        # At $2,175/kg deuterium (1costingfe u_deuterium), cost is negligible.
        annual_d_kg = annual_he3_kg * (2.0 / 3.0)  # approximate stoichiometry
        annual_d_cost_M = annual_d_kg * 2175.0 / 1e6

        r["CAS80"] = annual_he3_cost_M + annual_d_cost_M
        r["CAS80_he3"] = annual_he3_cost_M
        r["CAS80_deuterium"] = annual_d_cost_M
        r["annual_he3_kg"] = annual_he3_kg
        r["annual_he3_cost_M"] = annual_he3_cost_M

        # === LCOE ===
        annual_rev_req = r["CAS90"] + r["CAS70"] + r["CAS80"]
        r["annual_revenue_req"] = annual_rev_req

        annual_energy_MWh = 8760.0 * p_net_plant * self.plant_availability
        r["annual_energy_MWh"] = annual_energy_MWh

        if annual_energy_MWh > 0:
            r["lcoe_USD_per_MWh"] = annual_rev_req * 1e6 / annual_energy_MWh
            r["lcoe_cents_per_kWh"] = r["lcoe_USD_per_MWh"] / 10.0
        else:
            r["lcoe_USD_per_MWh"] = float("inf")
            r["lcoe_cents_per_kWh"] = float("inf")

        # Cost fractions
        if annual_rev_req > 0:
            r["capital_fraction"] = r["CAS90"] / annual_rev_req
            r["om_fraction"] = r["CAS70"] / annual_rev_req
            r["fuel_fraction"] = r["CAS80"] / annual_rev_req

        return r

    def compute(self) -> dict:
        """Compute LCOE and all derived quantities. Returns structured result dict."""
        power = self._compute_power()
        geom = self._compute_geometry(power)
        cas22 = self._compute_cas22(power, geom)
        costs = self._compute_costs(power, geom, cas22)
        econ = self._compute_economics(power, costs)

        return {
            "power": power,
            "geometry": geom,
            "cas22": cas22,
            "costs": costs,
            "economics": econ,
        }


# ===========================================================================
# Module-level required interface (for concept explorer)
# ===========================================================================

params = OrbitalDipolePlantParams()
results = params.compute()

# Economy-of-scale scaling to 1000 MWe reference (alpha = 0.6)
_ALPHA = 0.6
_p_native = results["power"].get("p_net_plant", results["power"]["p_net"])
_factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)
_overnight = results["costs"]["overnight_capital"] * 1e3 / _p_native

scaled_headline = {
    "p_net_mw": 1000.0,
    "lcoe_per_mwh": results["economics"]["lcoe_USD_per_MWh"] * _factor,
    "overnight_per_kw": _overnight * _factor,
}


# ===========================================================================
# Utility functions
# ===========================================================================

def print_results(p: OrbitalDipolePlantParams, r: dict):
    """Print full CAS-structured LCOE results."""
    pw = r["power"]
    ca = r["cas22"]
    co = r["costs"]
    ec = r["economics"]
    ge = r["geometry"]

    print("=" * 72)
    print("Orbital Levitated Dipole (D-He3) LCOE Model — 1cFE Free-Form")
    print("Zephyr Fusion | orbital spacecraft + ground rectenna")
    print("=" * 72)

    print("\n--- Key Input Parameters ---")
    print(f"  Fusion power (per spacecraft):      {p.p_fus_MW:.1f} MW")
    print(f"  Scientific Q:                       {p.Q_sci:.1f}")
    print(f"  Stage 1 DEC efficiency (eta_dec):   {p.eta_dec:.0%} [HIGH UNCERTAINTY]")
    print(f"  Stage 2 Transmitter (phased-array): {p.eta_transmitter:.0%} [HIGH UNCERTAINTY]")
    print(f"  Stage 3 Beam collection:            {p.eta_beam:.0%}")
    print(f"  Stage 4 Rectenna:                   {p.eta_rectenna:.0%}")
    print(f"  ICRH wall-plug efficiency:          {p.eta_icrh:.0%}")
    print(f"  Spacecraft mass (total):            {ge['m_spacecraft_total_kg']:,.0f} kg")
    print(f"  Launch cost:                        ${p.launch_cost_per_kg:,.0f}/kg")
    print(f"  He3 cost:                           ${p.he3_cost_per_kg/1e6:.1f}M/kg")
    print(f"  Plant availability:                 {p.plant_availability:.0%}")
    print(f"  Plant lifetime:                     {p.plant_lifetime_years:.0f} years")
    print(f"  FOAK/NOAK:                          {'NOAK' if p.noak else 'FOAK'}")
    print(f"  Interest rate:                      {p.interest_rate:.0%}")

    print("\n--- Power Balance (4-Stage Conversion Chain) ---")
    print(f"  Fusion power:                       {pw['p_fus']:.1f} MW")
    print(f"    Charged particle (14.7 MeV p):    {pw['p_charged']:.1f} MW ({p.f_charged_particle:.0%})")
    print(f"    DD neutrons (to space):            {pw['p_neutron_space']:.1f} MW ({p.f_neutron:.0%})")
    print(f"  [Stage 1] DEC output (DC):          {pw['p_dec_out_DC']:.2f} MW (eta={p.eta_dec:.0%})")
    print(f"  Recirculating loads:")
    print(f"    Heating (ICRH wall-plug):         {pw['p_heat_wall_MW']:.2f} MW")
    print(f"    Cryocooler:                       {p.p_cryo_MW:.2f} MW")
    print(f"    Housekeeping:                     {p.p_misc_MW:.2f} MW")
    print(f"    Total recirc:                     {pw['p_recirc']:.2f} MW ({pw['recirc_fraction']:.0%} of DEC output)")
    print(f"  Power available for beaming:        {pw['p_beam_in']:.2f} MW")
    print(f"  [Stage 2] After transmitter:        {pw['p_after_transmitter']:.2f} MW (eta={p.eta_transmitter:.0%})")
    print(f"  [Stage 3] After beam:               {pw['p_after_beam']:.2f} MW (eta={p.eta_beam:.0%})")
    print(f"  [Stage 4] Net delivered (AC grid):  {pw['p_net']:.3f} MW (eta={p.eta_rectenna:.0%})")
    print(f"  ─────────────────────────────────────────────────────────────")
    print(f"  Net plant output ({p.n_spacecraft} spacecraft):   {pw['p_net_plant']:.3f} MWe")
    print(f"  Engineering Q (p_fus/p_recirc):     {pw['Q_eng']:.1f}")
    print(f"  Full 4-stage efficiency:            {pw['eta_net_to_fus']:.1%} (p_net/p_fus)")
    print(f"  3-stage beaming efficiency:         {pw['eta_beaming_3stage']:.1%}")
    print(f"  Specific power:                     {ge['specific_power_W_kg']:.1f} W/kg spacecraft")

    print("\n--- He3 Fuel Balance ---")
    print(f"  He3 consumption rate:               {pw['he3_consumption_kg_per_yr']:.3f} kg/yr per spacecraft")
    print(f"  Annual He3 purchase:                {ec['annual_he3_kg']:.3f} kg/yr (fleet)")
    print(f"  Annual He3 cost:                    ${ec['annual_he3_cost_M']:.2f}M/yr")
    print(f"  He3 cost share of LCOE:             {ec.get('fuel_fraction', 0):.1%}")

    print("\n--- Spacecraft Mass Budget ---")
    for k, label in [
        ("m_hts_coil_kg", "HTS dipole coil + cryostat"),
        ("m_heating_kg", "ICRH/ECRH heating system"),
        ("m_dec_kg", "Direct energy converter"),
        ("m_transmitter_kg", "Phased-array transmitter"),
        ("m_bus_kg", "Spacecraft bus"),
        ("m_cryo_kg", "Cryocooler + thermal radiators"),
        ("m_fuel_system_kg", "He3/D fuel system"),
    ]:
        print(f"    {label:<36s} {ge[k]:>8,.0f} kg")
    print(f"    {'─' * 50}")
    print(f"    Total spacecraft mass              {ge['m_spacecraft_total_kg']:>8,.0f} kg")
    print(f"    Launch cost ({p.launch_cost_per_kg:,}/kg):              ${ge['launch_cost_M']:>6.1f}M")

    print("\n--- CAS22: Spacecraft Plant Equipment ---")
    cas22_labels = {
        "C220101": "First Wall/Blanket [N/A — no blanket]",
        "C220102": "Shield [N/A — no shielding needed]",
        "C220103": "HTS dipole coil system [override]",
        "C220104": "ICRH heating system [override]",
        "C220105": "Spacecraft bus + structure [override]",
        "C220106": "Vacuum system [N/A — space vacuum]",
        "C220107": "Power electronics + onboard I&C [override]",
        "C220108": "Target factory [N/A — steady-state]",
        "C220109": "Direct Energy Converter [1costingfe scaled]",
        "C220110": "Remote handling / integration [override]",
        "C220111": "Integration labor (14%)",
        "C220112": "He3 fuel system [override]",
        "C220113": "Phased-array transmitter fabrication [override]",
    }
    for code, label in cas22_labels.items():
        val = ca[code]
        print(f"    {code} {label:<42s} ${val:>6.1f}M")
    print(f"    {'─' * 60}")
    print(f"    Per-module subtotal:                         ${ca['CAS22_per_module']:>6.1f}M × {p.n_spacecraft}")

    print(f"  Plant-wide (ground infrastructure):")
    pw_labels = {
        "C220200": "Coolant systems [N/A]",
        "C220300": "Cryocooler + thermal radiators",
        "C220400": "Rad waste management [N/A]",
        "C220500": "He3 ground handling",
        "C220600": "Ground control systems",
        "C220700": "Instrumentation & control",
    }
    for code, label in pw_labels.items():
        val = ca[code]
        print(f"    {code} {label:<42s} ${val:>6.1f}M")
    print(f"    {'─' * 60}")
    print(f"    Plant-wide subtotal:                         ${ca['CAS22_plant_wide']:>6.1f}M")
    print(f"  CAS22 Total:                                   ${ca['CAS22']:>6.1f}M")

    print("\n--- Capital Costs (CAS10–60) ---")
    print(f"  CAS10 Pre-construction (licensing):  ${co['CAS10']:>8.1f}M")
    print(f"  CAS21 Ground station facility:       ${co['CAS21']:>8.1f}M")
    print(f"  CAS22 Spacecraft plant equipment:    ${co['CAS22']:>8.1f}M")
    print(f"  CAS23 Ground beaming management:     ${co['CAS23']:>8.1f}M")
    print(f"  CAS24 Rectenna + grid connection:    ${co['CAS24']:>8.1f}M")
    print(f"  CAS25 Misc ground equipment:         ${co['CAS25']:>8.1f}M")
    print(f"  CAS26 Spacecraft thermal ground:     ${co['CAS26']:>8.1f}M")
    print(f"  CAS27 He3 startup inventory:         ${co['CAS27']:>8.1f}M")
    print(f"  CAS28 Digital twin:                  ${co['CAS28']:>8.1f}M")
    print(f"  CAS29 Contingency (FOAK 10%):        ${co['CAS29']:>8.1f}M")
    print(f"  {'─' * 55}")
    print(f"  CAS20 Direct Costs:                  ${co['CAS20']:>8.1f}M")
    print(f"  CAS30 Integration / Indirect:        ${co['CAS30']:>8.1f}M")
    print(f"  CAS40 Owner's Costs:                 ${co['CAS40']:>8.1f}M")
    print(f"  CAS50 Launch + Supplementary:        ${co['CAS50']:>8.1f}M")
    print(f"    of which: Launch cost:             ${co['CAS50_launch']:>8.1f}M")
    print(f"    of which: Decommissioning:         ${co['CAS50_decom']:>8.1f}M")
    print(f"  {'─' * 55}")
    print(f"  Overnight Capital:                   ${co['overnight_capital']:>8.1f}M")
    print(f"  CAS60 IDC (f={co['f_IDC']:.3f}):           ${co['CAS60']:>8.1f}M")
    print(f"  {'═' * 55}")
    print(f"  Total Capital:                       ${co['total_capital']:>8.1f}M")
    print(f"  Specific Capital:                    ${co['specific_capital_USD_per_kWe']:>8,.0f} $/kWe")

    print("\n--- Annual Costs (CAS70–90) ---")
    print(f"  CAS90 Capital charge (CRF={ec['CRF']:.4f}): ${ec['CAS90']:>8.2f}M/yr")
    print(f"  CAS71 O&M ({p.orbital_om_frac_annual:.0%} of overnight cap): ${ec['CAS71']:>8.2f}M/yr")
    print(f"  CAS72 Scheduled replacement:         ${ec['CAS72']:>8.2f}M/yr ({ec['n_coil_replacements']} coil replacements)")
    print(f"  CAS70 Total O&M:                     ${ec['CAS70']:>8.2f}M/yr")
    print(f"  CAS80 He3 fuel cost:                 ${ec['CAS80']:>8.2f}M/yr")
    print(f"    He3: {ec['annual_he3_kg']:.3f} kg/yr × ${p.he3_cost_per_kg/1e6:.0f}M/kg = ${ec['CAS80_he3']:.2f}M/yr")

    print("\n--- LCOE ---")
    print(f"  Annual energy production:   {ec['annual_energy_MWh']:,.1f} MWh")
    print(f"  Annual revenue requirement: ${ec['annual_revenue_req']:.2f}M")
    print(f"  ╔══════════════════════════════════════════╗")
    lv = ec["lcoe_USD_per_MWh"]
    lc = ec["lcoe_cents_per_kWh"]
    print(f"  ║  LCOE = {lc:>10.1f} ¢/kWh               ║")
    print(f"  ║       = {lv:>10.1f} $/MWh               ║")
    print(f"  ╚══════════════════════════════════════════╝")
    print(f"  Capital (CAS90):    {ec.get('capital_fraction', 0):.1%}")
    print(f"  O&M (CAS70):        {ec.get('om_fraction', 0):.1%}")
    print(f"  Fuel (CAS80):       {ec.get('fuel_fraction', 0):.1%}")

    # Scaled headline
    fac = (_p_native / 1000.0) ** (1.0 - _ALPHA)
    print(f"\n--- Scaled to 1000 MWe Reference (alpha=0.6) ---")
    print(f"  Native p_net_plant:             {_p_native:.3f} MWe")
    print(f"  Scale factor:                   {fac:.4f}")
    print(f"  Scaled LCOE:                    ${scaled_headline['lcoe_per_mwh']:,.1f} /MWh")
    print(f"  Scaled overnight capital:       ${scaled_headline['overnight_per_kw']:,.0f} /kWe")

    print("\n--- Competitive Benchmarks ---")
    print(f"  Terrestrial fusion parity:      $50–150/MWh   → this concept: {lv/100:.0f}× over-parity")
    print(f"  SPS parity (orbital ref):       $200–500/MWh  → this concept: {lv/350:.0f}× over-SPS-parity")


def sensitivity_sweep(base_params: OrbitalDipolePlantParams, param_name: str,
                      values: list, label: str = "") -> list:
    """Sweep a single parameter and return LCOE for each value."""
    results_list = []
    for val in values:
        p_dict = {k: getattr(base_params, k)
                  for k in base_params.__dataclass_fields__}
        p_dict[param_name] = val
        p = OrbitalDipolePlantParams(**p_dict)
        r = p.compute()
        results_list.append({
            "param_value": float(val) if not isinstance(val, bool) else val,
            "lcoe_USD_per_MWh": r["economics"]["lcoe_USD_per_MWh"],
            "lcoe_cents_kWh": r["economics"]["lcoe_cents_per_kWh"],
            "p_net_plant_MW": r["power"]["p_net_plant"],
            "annual_he3_kg": r["economics"]["annual_he3_kg"],
        })
    return results_list


def spacecraft_capex_multiplier_sweep(base_params: OrbitalDipolePlantParams,
                                      multipliers: list) -> list:
    """Sweep spacecraft hardware CAPEX multiplier over CAS22 override accounts.

    Applies multiplier to: c_hts_coil_M (C220103), c_heating_M (C220104),
    c_bus_M (C220105), c_electronics_M (C220107), c_dec_M (C220109 floor),
    c_transmitter_M (C220113). Tests the viable CAPEX corridor: what maximum
    spacecraft manufacturing cost still allows SPS parity?
    """
    base_fields = {k: getattr(base_params, k)
                   for k in base_params.__dataclass_fields__}
    hw_params = ["c_hts_coil_M", "c_heating_M", "c_bus_M",
                 "c_electronics_M", "c_dec_M", "c_transmitter_M"]
    base_hw_vals = {k: base_fields[k] for k in hw_params}
    results_list = []
    for mult in multipliers:
        p_dict = dict(base_fields)
        for k in hw_params:
            p_dict[k] = base_hw_vals[k] * mult
        p = OrbitalDipolePlantParams(**p_dict)
        r = p.compute()
        results_list.append({
            "multiplier": mult,
            "lcoe_USD_per_MWh": r["economics"]["lcoe_USD_per_MWh"],
            "cas22_total_M": r["cas22"]["CAS22"],
            "p_net_plant_MW": r["power"]["p_net_plant"],
        })
    return results_list


def main():
    # =========================================================================
    # BASELINE SCENARIO
    # =========================================================================
    print("\n" + "#" * 72)
    print("# BASELINE: Orbital Levitated Dipole (D-He3) — Pessimistic")
    print("# Market-purchase He3 ($30M/kg), Falcon 9 launch ($2,700/kg),")
    print("# Phased-array beaming (15% transmitter efficiency)")
    print("#" * 72)

    baseline = OrbitalDipolePlantParams()
    r_base = baseline.compute()
    print_results(baseline, r_base)

    # =========================================================================
    # SENSITIVITY SWEEPS
    # =========================================================================
    print("\n" + "=" * 72)
    print("SENSITIVITY SWEEPS (from baseline)")
    print("=" * 72)
    base_lcoe = r_base["economics"]["lcoe_USD_per_MWh"]
    print(f"  Baseline LCOE: ${base_lcoe:,.0f}/MWh\n")

    sweeps = [
        ("he3_cost_per_kg",
         [0, 1e5, 1e6, 5e6, 10e6, 20e6, 30e6],
         "He3 cost ($/kg)   [Dominant lever — self-breed vs. market]"),
        ("eta_transmitter",
         [0.05, 0.10, 0.15, 0.20, 0.50, 0.75, 0.80],
         "Transmitter efficiency (DC-RF)  [phased-array <20%; no-steering ~75%]"),
        ("launch_cost_per_kg",
         [100, 200, 500, 1000, 2000, 2700, 5000],
         "Launch cost ($/kg)  [Starship ~$200; Falcon 9 ~$2,700]"),
        ("Q_sci",
         [2, 5, 10, 15, 20, 30],
         "Scientific Q  [D-He3 requires ~10× triple product vs D-T; Q=10 optimistic]"),
        ("eta_dec",
         [0.20, 0.30, 0.40, 0.50, 0.57, 0.65, 0.80],
         "DEC efficiency (proton deceleration)  [50–65% Venetian blind upper bound]"),
        ("p_fus_MW",
         [5, 10, 20, 30, 50, 100],
         "Fusion power per spacecraft (MW)  [He3 cost scales linearly with p_fus]"),
    ]

    for param_name, values, label in sweeps:
        print(f"  {label}:")
        sweep_results = sensitivity_sweep(baseline, param_name, values)
        for sr in sweep_results:
            v = sr["param_value"]
            lcoe = sr["lcoe_USD_per_MWh"]
            p_net = sr["p_net_plant_MW"]
            he3 = sr["annual_he3_kg"]
            if param_name == "he3_cost_per_kg":
                v_str = f"${v/1e6:.1f}M/kg"
            elif param_name.startswith("eta"):
                v_str = f"{v:.0%}"
            elif param_name == "launch_cost_per_kg":
                v_str = f"${v:,.0f}/kg"
            else:
                v_str = f"{v}"
            marker = " <<< SPS parity" if 200 <= lcoe <= 500 else ""
            marker = " <<< grid parity?" if lcoe <= 150 else marker
            print(f"    {v_str:>12s} → ${lcoe:>10,.0f}/MWh  "
                  f"(p_net={p_net:.2f} MWe, He3={he3:.2f} kg/yr){marker}")
        print()

    # =========================================================================
    # SCENARIO COMPARISON TABLE
    # =========================================================================
    print("=" * 72)
    print("SCENARIO COMPARISON")
    print("=" * 72)

    # Pessimistic: market He3, Falcon 9, phased-array
    pessimistic = OrbitalDipolePlantParams(
        he3_cost_per_kg=30.0e6,
        launch_cost_per_kg=2700.0,
        eta_transmitter=0.15,
        eta_dec=0.57,
        Q_sci=10.0,
        noak=False,
    )

    # Moderate: market He3, Falcon 9, improved beaming (no phased-array steering)
    moderate = OrbitalDipolePlantParams(
        he3_cost_per_kg=30.0e6,
        launch_cost_per_kg=2700.0,
        eta_transmitter=0.50,    # non-steering tube efficiency (aspirational)
        eta_dec=0.57,
        Q_sci=15.0,
        noak=False,
    )

    # Optimistic-A: self-bred He3 (~$0), Starship era, no phased-array
    optimistic_a = OrbitalDipolePlantParams(
        he3_cost_per_kg=0.0,       # self-bred (note: analysis shows this requires D-rich fuel)
        launch_cost_per_kg=200.0,  # Starship target
        eta_transmitter=0.50,      # high-efficiency tubes, no phased-array steering
        eta_dec=0.65,              # upper bound DEC
        Q_sci=20.0,
        eta_rectenna=0.90,
        interest_rate=0.06,
        plant_lifetime_years=15.0,
        noak=True,
    )

    # Optimistic-B: as above + aggressive Q and improved beaming
    optimistic_b = OrbitalDipolePlantParams(
        he3_cost_per_kg=0.0,
        launch_cost_per_kg=100.0,  # Starship mature pricing
        eta_transmitter=0.75,      # aspirational non-steering (not demonstrated)
        eta_dec=0.65,
        eta_beam=0.89,
        eta_rectenna=0.90,
        Q_sci=30.0,
        plant_availability=0.92,
        interest_rate=0.05,
        plant_lifetime_years=20.0,
        noak=True,
    )

    scenarios = {
        "Pessimistic (baseline)": pessimistic,
        "Moderate (better beaming)": moderate,
        "Optimistic-A (self-bred He3, Starship)": optimistic_a,
        "Optimistic-B (tech progress)": optimistic_b,
    }

    print(f"\n{'Scenario':<40} {'eta_total':>9} {'p_net':>7} "
          f"{'He3 cost':>12} {'Capital':>10} {'LCOE':>12}")
    print("-" * 92)

    for name, sc in scenarios.items():
        r = sc.compute()
        pw = r["power"]
        ec = r["economics"]
        co = r["costs"]
        eta_net = pw["eta_net_to_fus"]
        p_net = pw["p_net_plant"]
        he3_ann = ec["CAS80_he3"]
        cap_ann = ec["CAS90"]
        lcoe = ec["lcoe_USD_per_MWh"]
        print(f"  {name:<38} {eta_net:>8.1%} {p_net:>6.3f}MW "
              f"${he3_ann:>9.1f}M/yr ${cap_ann:>7.1f}M/yr ${lcoe:>10,.0f}/MWh")

    print()
    print("  Reference thresholds:")
    print("  Terrestrial fusion parity:   $50–150/MWh")
    print("  SPS (space solar parity):    $200–500/MWh")
    print("  Net energy gain only:        any positive LCOE")

    # =========================================================================
    # SPACECRAFT HARDWARE CAPEX MULTIPLIER SWEEP (F-1)
    # Tests maximum spacecraft manufacturing cost that preserves SPS parity
    # in the optimistic scenario (self-bred He3 $0, Starship $200/kg, 50% tx).
    # Multiplier applied to: C220103 HTS coil, C220104 heating, C220105 bus,
    #   C220107 electronics, C220109 DEC floor, C220113 transmitter.
    # =========================================================================
    print()
    print("=" * 72)
    print("SPACECRAFT HARDWARE CAPEX MULTIPLIER SWEEP")
    print("Scenario: Optimistic-A (self-bred He3 $0, Starship $200/kg, eta_tx=50%)")
    print("Accounts scaled: C220103 HTS, C220104 heating, C220105 bus,")
    print("  C220107 electronics, C220109 DEC floor, C220113 transmitter")
    print("SPS parity window: $200–500/MWh  |  Q: what max HW cost keeps parity?")
    print("=" * 72)

    base_hw_total = (optimistic_a.c_hts_coil_M + optimistic_a.c_heating_M
                     + optimistic_a.c_bus_M + optimistic_a.c_electronics_M
                     + optimistic_a.c_dec_M + optimistic_a.c_transmitter_M)
    print(f"\n  Baseline spacecraft hardware accounts: ${base_hw_total:.0f}M")
    print(f"    HTS coil ${optimistic_a.c_hts_coil_M:.0f}M  heating ${optimistic_a.c_heating_M:.0f}M"
          f"  bus ${optimistic_a.c_bus_M:.0f}M  electronics ${optimistic_a.c_electronics_M:.0f}M"
          f"  DEC ${optimistic_a.c_dec_M:.0f}M  transmitter ${optimistic_a.c_transmitter_M:.0f}M\n")

    mult_values_hw = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    hw_sweep = spacecraft_capex_multiplier_sweep(optimistic_a, mult_values_hw)

    print(f"  {'Mult':>6}  {'HW Cost':>9}  {'CAS22':>8}  {'LCOE $/MWh':>12}  Status")
    print(f"  {'-'*60}")
    prev_lcoe = None
    breakeven_lo_mult = None
    breakeven_hi_mult = None
    for res in hw_sweep:
        m = res["multiplier"]
        lcoe = res["lcoe_USD_per_MWh"]
        cas22 = res["cas22_total_M"]
        hw_cost = base_hw_total * m
        if 200.0 <= lcoe <= 500.0:
            status = "in SPS window"
        elif lcoe < 200.0:
            status = "below SPS floor"
        else:
            status = "ABOVE SPS parity"
        if prev_lcoe is not None and prev_lcoe <= 500.0 < lcoe and breakeven_hi_mult is None:
            breakeven_hi_mult = m
            breakeven_lo_mult = mult_values_hw[mult_values_hw.index(m) - 1]
        print(f"  {m:>5.1f}×  ${hw_cost:>7.0f}M  ${cas22:>6.1f}M  ${lcoe:>10,.0f}/MWh  {status}")
        prev_lcoe = lcoe

    print()
    if breakeven_hi_mult is not None:
        print(f"  Breakeven: SPS parity (≤$500/MWh) lost between "
              f"{breakeven_lo_mult:.1f}× and {breakeven_hi_mult:.1f}× baseline.")
        print(f"  This corresponds to spacecraft hardware cost between "
              f"${base_hw_total * breakeven_lo_mult:.0f}M and "
              f"${base_hw_total * breakeven_hi_mult:.0f}M.")
    print(f"  Note: Optimistic-A FOAK spacecraft fabrication cost ($50–70M baseline)")
    print(f"  could be 10–100× higher per analysis §Section 7. This sweep directly")
    print(f"  tests whether that uncertainty is binding independent of fuel/beaming bets.")
    print()

    # =========================================================================
    # KEY BINDING CONSTRAINTS
    # =========================================================================
    print("\n" + "=" * 72)
    print("KEY BINDING CONSTRAINTS (top 3 LCOE drivers)")
    print("=" * 72)

    print("""
  1. HE3 FUEL COST — Dominant in pessimistic scenario
     At market-purchase He3 ($30M/kg), fuel cost alone for 1 MWe delivered
     exceeds $6,000/MWh — roughly 40–120× terrestrial fusion parity.
     He3 consumption: p_fus × 0.054 kg/yr/MW. At 30 MW fusion → 1.6 kg/yr.
     Self-breeding feasibility (analysis §Section 2, hypothesis b): equimolar
     D:He3 self-breeding is only 7.5% of consumption rate; sufficiency requires
     13:1 D:He3 ratio that destroys the aneutronic advantage. The concept is
     either LCOE-blocking (market purchase) or fundamentally different
     (D-rich "breeding mode" that negates the core aneutronic premise).
     STATUS: Categorically insufficient at equimolar operation (cross-section arithmetic).

  2. END-TO-END BEAMING EFFICIENCY — Dominant revenue-side sensitivity
     Full 4-stage chain (F-3 corrected): DEC × transmitter × beam × rectenna.
     At realistic phased-array (<20% transmitter): ~6–9% end-to-end.
     Every MW of fusion power delivers only ~0.06–0.09 MWe to the grid.
     To reach SPS parity ($200–500/MWh), full-chain efficiency must exceed ~40%.
     No technology combination achieves this today; phased-array transmitters
     are the dominant bottleneck (4–6 dB phase shifter loss per element).
     STATUS: Below competitive threshold under all current technology assumptions.

  3. SPACECRAFT CAPITAL COST vs. DELIVERED POWER
     First-of-kind orbital fusion spacecraft: ~$65–120M total capital per unit.
     At 0.3–1 MWe delivered per spacecraft, specific capital is $65,000–400,000/kWe
     (vs. ~$5,000–15,000/kWe for terrestrial fusion concepts).
     Starship launch ($200/kg) reduces launch contribution from $27M to $2M,
     but spacecraft hardware ($47M) and He3 startup inventory dominate.
     Reduction in specific capital requires either (a) much higher delivered power
     per spacecraft (requires breakthrough in beaming efficiency + DEC), or
     (b) dramatic reduction in spacecraft manufacturing cost (NOAK serial production).
     STATUS: No near-term pathway to competitive specific capital at MW-class output.
""")

    print("NOTE: All estimates carry HIGH UNCERTAINTY. This model is intended for")
    print("first-pass corridor mapping only. The concept is physically plausible in")
    print("principle (net energy gain) but faces three independent LCOE-blocking")
    print("barriers that require simultaneous resolution at unprecedented technology")
    print("maturity levels. See analysis.md §Section 7 for detailed scenario discussion.")


if __name__ == "__main__":
    main()
