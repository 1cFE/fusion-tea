from dataclasses import dataclass, field
from enum import Enum


class ConfinementFamily(Enum):
    STEADY_STATE = "steady_state"
    PULSED = "pulsed"


class ConfinementConcept(Enum):
    TOKAMAK = "tokamak"
    STELLARATOR = "stellarator"
    MIRROR = "mirror"
    STEADY_FRC = "steady_frc"
    DIPOLE = "dipole"
    LASER_IFE = "laser_ife"
    ZPINCH = "zpinch"
    HEAVY_ION = "heavy_ion"
    MAG_TARGET = "mag_target"
    PLASMA_JET = "plasma_jet"
    PULSED_FRC = "pulsed_frc"
    MAGLIF = "maglif"
    THETA_PINCH = "theta_pinch"
    DENSE_PLASMA_FOCUS = "dense_plasma_focus"
    STAGED_ZPINCH = "staged_zpinch"
    ORBITRON = "orbitron"
    POLYWELL = "polywell"


class PulsedConversion(Enum):
    THERMAL = "thermal"
    INDUCTIVE_DEC = "inductive_dec"


class LaserDriverType(Enum):
    """Laser-IFE driver architecture.

    Selects, for LASER_IFE, both the C220104 capital coefficient ($/MJ) and the
    CAS72 scheduled-replacement subsystem set. Chosen via the laser_driver_type
    parameter (concept-YAML default + per-run override), not a separate concept.

    DPSSL is the commercial baseline (LIFE / HiPER / Focused Energy / Marvel);
    KRF carries the NRL Electra / Xcimer heritage; NDGLASS (NIF-class) is
    flagged commercially marginal — flashlamp shot life is Xe-arc-limited.
    """

    DPSSL = "dpssl"  # diode-pumped solid-state
    KRF = "krf"  # KrF excimer
    NDGLASS = "nd_glass"  # flashlamp-pumped Nd:Glass (NIF-class)


CONCEPT_TO_FAMILY = {
    ConfinementConcept.TOKAMAK: ConfinementFamily.STEADY_STATE,
    ConfinementConcept.STELLARATOR: ConfinementFamily.STEADY_STATE,
    ConfinementConcept.MIRROR: ConfinementFamily.STEADY_STATE,
    ConfinementConcept.STEADY_FRC: ConfinementFamily.STEADY_STATE,
    ConfinementConcept.DIPOLE: ConfinementFamily.STEADY_STATE,
    ConfinementConcept.LASER_IFE: ConfinementFamily.PULSED,
    ConfinementConcept.ZPINCH: ConfinementFamily.PULSED,
    ConfinementConcept.HEAVY_ION: ConfinementFamily.PULSED,
    ConfinementConcept.MAG_TARGET: ConfinementFamily.PULSED,
    ConfinementConcept.PLASMA_JET: ConfinementFamily.PULSED,
    ConfinementConcept.PULSED_FRC: ConfinementFamily.PULSED,
    ConfinementConcept.MAGLIF: ConfinementFamily.PULSED,
    ConfinementConcept.THETA_PINCH: ConfinementFamily.PULSED,
    ConfinementConcept.DENSE_PLASMA_FOCUS: ConfinementFamily.PULSED,
    ConfinementConcept.STAGED_ZPINCH: ConfinementFamily.PULSED,
    ConfinementConcept.ORBITRON: ConfinementFamily.STEADY_STATE,
    ConfinementConcept.POLYWELL: ConfinementFamily.STEADY_STATE,
}

# Concepts whose plant power scales by REPLICATING a fixed module (n_mod), not by
# growing a single device (volume, like tokamak/mirror) or by rep-rate/yield.
# These support size_from_power via integer module-count solve (model._size_modular).
# Membership is published-developer-grounded; see docs/account_justification/
# concept_power_scaling.md. STAGED_ZPINCH is Zap's sheared-flow pinch (see its YAML).
N_MOD_SIZED_CONCEPTS = frozenset(
    {
        ConfinementConcept.ORBITRON,
        ConfinementConcept.DENSE_PLASMA_FOCUS,
        ConfinementConcept.STAGED_ZPINCH,
        ConfinementConcept.STEADY_FRC,
    }
)

CONCEPT_DEFAULT_CONVERSION = {
    ConfinementConcept.LASER_IFE: PulsedConversion.THERMAL,
    ConfinementConcept.ZPINCH: PulsedConversion.THERMAL,
    ConfinementConcept.HEAVY_ION: PulsedConversion.THERMAL,
    ConfinementConcept.MAG_TARGET: PulsedConversion.THERMAL,
    ConfinementConcept.PLASMA_JET: PulsedConversion.THERMAL,
    ConfinementConcept.PULSED_FRC: PulsedConversion.INDUCTIVE_DEC,
    ConfinementConcept.MAGLIF: PulsedConversion.THERMAL,
    ConfinementConcept.THETA_PINCH: PulsedConversion.INDUCTIVE_DEC,
    ConfinementConcept.DENSE_PLASMA_FOCUS: PulsedConversion.THERMAL,
    ConfinementConcept.STAGED_ZPINCH: PulsedConversion.THERMAL,
}


class WallMaterial(Enum):
    TUNGSTEN = "W"
    CARBON = "C"
    BERYLLIUM = "Be"
    MOLYBDENUM = "Mo"
    SIC = "SiC"
    LITHIUM = "Li"


@dataclass
class ImpurityMix:
    """Impurity species and concentrations (f_z = n_z/n_e)."""

    wall_derived: dict[str, float]
    seeded: dict[str, float]


class CoilMaterial(Enum):
    REBCO_HTS = "rebco_hts"
    NB3SN = "nb3sn"
    NBTI = "nbti"
    COPPER = "copper"

    @property
    def is_superconducting(self) -> bool:
        """True for superconductors, which require a cryogenic plant; COPPER
        (normal-conducting) does not."""
        return self is not CoilMaterial.COPPER


class BlanketForm(Enum):
    LIQUID_METAL = "liquid_metal"
    MOLTEN_SALT = "molten_salt"
    SOLID_BREEDER = "solid_breeder"
    NONE = "none"

    @property
    def structure_factor(self) -> float:
        """Multiplier on the per-fuel blanket_unit_cost_<fuel> in CAS22.01."""
        return _BLANKET_STRUCTURE_FACTOR[self]

    @property
    def valid_fills(self) -> set["BlanketFill"]:
        """Set of BlanketFill values physically compatible with this form."""
        return _BLANKET_FORM_VALID_FILLS[self]

    @property
    def default_fill(self) -> "BlanketFill":
        """The default BlanketFill to use when only the form is specified."""
        return _BLANKET_FORM_DEFAULT_FILL[self]


_BLANKET_STRUCTURE_FACTOR = {
    BlanketForm.LIQUID_METAL: 1.0,
    BlanketForm.MOLTEN_SALT: 1.3,
    BlanketForm.SOLID_BREEDER: 1.2,
    BlanketForm.NONE: 0.0,
}


class BlanketFill(Enum):
    PBLI = "pbli"
    LI = "li"
    FLIBE = "flibe"
    BE_CERAMIC = "be_ceramic"
    CERAMIC_ONLY = "ceramic_only"
    LI2O = "li2o"
    NONE = "none"

    # CAS27 cost is a volume-based mass build-up keyed on this fill via
    # cc.cas27_fill_materials[fill.value]; see costs.cas27_special_materials.


_BLANKET_FORM_VALID_FILLS = {
    BlanketForm.LIQUID_METAL: {BlanketFill.PBLI, BlanketFill.LI},
    BlanketForm.MOLTEN_SALT: {BlanketFill.FLIBE},
    # Li2O is a solid ceramic breeder (no Be multiplier needed when a separate
    # W neutron multiplier handles TBR, as in OpenStar / Simpson 2026).
    BlanketForm.SOLID_BREEDER: {
        BlanketFill.BE_CERAMIC,
        BlanketFill.CERAMIC_ONLY,
        BlanketFill.LI2O,
    },
    BlanketForm.NONE: {BlanketFill.NONE},
}

_BLANKET_FORM_DEFAULT_FILL = {
    BlanketForm.LIQUID_METAL: BlanketFill.PBLI,
    BlanketForm.MOLTEN_SALT: BlanketFill.FLIBE,
    BlanketForm.SOLID_BREEDER: BlanketFill.BE_CERAMIC,
    BlanketForm.NONE: BlanketFill.NONE,
}


class PowerCycle(Enum):
    RANKINE = "rankine"
    BRAYTON_SCO2 = "brayton_sco2"
    COMBINED = "combined"


class Fuel(Enum):
    DT = "dt"
    DD = "dd"
    DHE3 = "dhe3"
    PB11 = "pb11"


@dataclass
class PowerTable:
    """All power flow values computed by Layer 2 (physics)."""

    p_fus: float  # Fusion power [MW]
    p_ash: float  # Charged fusion product power [MW]
    p_neutron: float  # Neutron power [MW]
    p_rad: float  # Plasma radiation power [MW] (bremsstrahlung + synchrotron + line)
    p_wall: float  # Ash thermal on walls [MW]
    p_dee: float  # Direct energy extracted electric [MW]
    p_dec_waste: float  # DEC waste heat [MW]
    p_th: float  # Total thermal power [MW]
    p_the: float  # Thermal electric power [MW]
    p_et: float  # Gross electric power [MW]
    p_loss: float  # Lost power [MW]
    p_net: float  # Net electric power [MW]
    p_pump: float  # Pumping power [MW]
    p_sub: float  # Subsystem power [MW]
    p_aux: float  # Auxiliary power [MW]
    p_input: (
        float  # Effective heating power [MW] (may exceed user value if P_rad > P_ash)
    )
    p_coils: float  # Coil power [MW] (MFE)
    p_cool: float  # Cooling power [MW] (MFE)
    p_cryo: float  # Cryogenic system power [MW]
    p_target: float  # Target factory power [MW] (IFE/MIF)
    q_sci: float  # Scientific Q
    q_eng: float  # Engineering Q
    rec_frac: float  # Recirculating power fraction
    e_driver_mj: float = 0.0  # Per-pulse driver energy [MJ]
    e_stored_mj: float = 0.0  # Per-pulse cap bank energy [MJ]
    f_rep: float = 0.0  # Repetition rate [Hz]
    f_ch: float = 0.0  # Charged-particle fraction


@dataclass
class CostResult:
    """Per-CAS cost breakdown in millions USD."""

    cas10: float = 0.0  # Pre-construction
    cas21: float = 0.0  # Buildings
    cas22: float = 0.0  # Reactor plant equipment
    cas23: float = 0.0  # Turbine plant equipment
    cas24: float = 0.0  # Electric plant equipment
    cas25: float = 0.0  # Misc plant equipment
    cas26: float = 0.0  # Heat rejection
    cas27: float = 0.0  # Special materials
    cas28: float = 0.0  # Digital twin
    cas29: float = 0.0  # Contingency
    cas20: float = 0.0  # Total direct costs (sum CAS21-29)
    cas30: float = 0.0  # Indirect service costs
    cas40: float = 0.0  # Owner's costs
    cas50: float = 0.0  # Supplementary costs
    cas60: float = 0.0  # Capitalized financial costs
    cas70: float = 0.0  # Annualized O&M + replacement (CAS71 + CAS72)
    cas71: float = 0.0  # Annualized O&M
    cas72: float = 0.0  # Annualized scheduled replacement
    cas80: float = 0.0  # Annualized fuel
    cas90: float = 0.0  # Annualized financial (capital)
    total_capital: float = 0.0  # CAS10-60 sum
    lcoe: float = 0.0  # $/MWh
    overnight_cost: float = 0.0  # CAS10-50 sum (M$, excludes IDC)
    capital_per_kw: float = 0.0  # $/kW (total_capital per net electric kW)

    _LABELS = {
        "cas10": ("CAS10", "Pre-construction"),
        "cas21": ("CAS21", "Buildings"),
        "cas22": ("CAS22", "Reactor plant equipment"),
        "cas23": ("CAS23", "Turbine plant equipment"),
        "cas24": ("CAS24", "Electric plant equipment"),
        "cas25": ("CAS25", "Misc plant equipment"),
        "cas26": ("CAS26", "Heat rejection"),
        "cas27": ("CAS27", "Special materials"),
        "cas28": ("CAS28", "Digital twin"),
        "cas29": ("CAS29", "Contingency"),
        "cas20": ("CAS20", "Total direct costs"),
        "cas30": ("CAS30", "Indirect service costs"),
        "cas40": ("CAS40", "Owner's costs"),
        "cas50": ("CAS50", "Supplementary costs"),
        "cas60": ("CAS60", "Interest during construction"),
        "cas70": ("CAS70", "O&M + replacement (ann.)"),
        "cas71": ("  71", "  O&M (ann.)"),
        "cas72": ("  72", "  Scheduled replacement (ann.)"),
        "cas80": ("CAS80", "Fuel (ann.)"),
        "cas90": ("CAS90", "Financial (ann.)"),
    }

    def __str__(self) -> str:
        lines = []
        lines.append(f"{'Code':<8} {'Account':<30} {'M$':>10}")
        lines.append("-" * 50)
        for attr, (code, label) in self._LABELS.items():
            val = float(getattr(self, attr))
            lines.append(f"{code:<8} {label:<30} {val:>10.1f}")
        lines.append("-" * 50)
        lines.append(
            f"{'':8} {'Overnight (M$)':<30} {float(self.overnight_cost):>10.1f}"
        )
        lines.append(f"{'':8} {'Total capital':<30} {float(self.total_capital):>10.1f}")
        lines.append(
            f"{'':8} {'Capital ($/kW)':<30} {float(self.capital_per_kw):>10.0f}"
        )
        lines.append(f"{'':8} {'LCOE ($/MWh)':<30} {float(self.lcoe):>10.1f}")
        return "\n".join(lines)


@dataclass
class ForwardResult:
    """Complete result from a forward costing run."""

    power_table: PowerTable
    costs: CostResult
    params: dict  # All input params (for sensitivity analysis)
    overridden: list[str] = field(default_factory=list)  # Keys that were overridden
    cas22_detail: dict[str, float] = field(default_factory=dict)  # CAS22 sub-accounts
    plasma_state: object = None  # PlasmaState when 0D model is active
    solved_n_mod: int | None = None  # module count solved by n_mod size_from_power
