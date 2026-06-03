"""1costingfe model: PB11 FRC (TAE Technologies) (TAE Technologies).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
#    Geometry / physics / power. NO library-default re-passing.
#
# TAE has not published reactor-scale parameters for Da Vinci. The December
# 2025 merger announcement specified only the 50 MWe net electric target and
# construction timeline. Every value below is INFERRED — scaled from C-2W
# experimental data, derived from p-B11 Rider/Nevins physics constraints, or
# taken as the midpoint of the analyst's Section 5 ranges. Confidence is LOW
# on every line. Despite that, populating spec is preferred over leaving it
# empty: an empty spec runs the cost model on pure mirror YAML defaults that
# have zero relationship to a 50 MWe FRC, while these midpoints at least
# size the model to TAE's design point. Per the low-archetype-fit guidance
# in model_setup_costingfe.md, geometry and performance estimates are
# welcome here even when archetype-fit is Low.
#
# Mapping from Section 5 ranges to canonical mirror-archetype kwargs (the
# library has no STEADY_FRC + PB11 calibration; MIRROR is the chosen
# stand-in, Archetype-Fit: Low):
spec = dict(
    chamber_length=4.5,  # FRC axial length [m] — Section 5 range 3-6, midpoint
                         # 4.5; inferred from C-2W L ≈ 2 m scaling × 2-3 for
                         # reactor scale, with Norm-style NBI-only formation
                         # reducing length vs. gun-formed FRCs.
    plasma_t=1.0,        # FRC separatrix radius [m] — Section 5 range 0.8-1.5,
                         # midpoint 1.0; scaled from C-2W r_s ≈ 0.4 m.
    b_center=0.35,       # External equilibrium field [T] — Section 5 range
                         # 0.2-0.5, midpoint 0.35. FRC near-unity beta means the
                         # external field is weak; this is the coil-axis field
                         # the library uses for magnet sizing (representing
                         # TAE's "simple geometry magnets" architecture).
    B=2.0,               # Internal FRC self-field [T] — Section 5 range 1-3,
                         # midpoint 2.0. Plasma poloidal field from FRC current.
                         # This is what enters the bremsstrahlung calc.
    n_e=1.0e21,          # Electron density [m^-3] — Section 5 range
                         # 5-20 × 10^20, midpoint 1.0 × 10^21. ~30x C-2W to
                         # achieve p-B11 fusion power density.
    T_e=75.0,            # Electron temperature [keV] — Section 5 range 50-100,
                         # midpoint 75. Note T_e < T_i ≈ 150-200 keV per the
                         # Rider/Nevins p-B11 constraint (bremsstrahlung losses
                         # rise rapidly if T_e approaches T_i for high-Z fuel).
    plasma_volume=15.0,  # Section 5 range 6-30 m^3, midpoint 15 (derived from
                         # π × r_s^2 × L with above midpoints; sanity-checks).
    eta_p=0.9,           # FRC plasma beta ≈ 0.9-1.0 (near-unity is the
                         # defining FRC property); midpoint 0.9.
    p_input=100.0,       # Total NBI wallplug [MW] — Section 5 range 50-200,
                         # midpoint 100. p_input/P_native = 100/50 = 2.0, well
                         # above the F9 ratio cap of 0.5. This reflects that
                         # a 50 MWe FRC with ~30% thermal efficiency and Q≈2-5
                         # plausibly recirculates very heavily through NBI;
                         # outside the F9 calibration band but honest. If F9
                         # rejects on re-analyze, follow up with either an
                         # archetype-specific cap or a smaller p_input choice
                         # at the analyst's discretion.
)
P_native = 50.0         # MWe — Da Vinci 50 MWe pilot plant design point

# 2. Model.
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
# NOTE: C220111 override from Section 5b analysis is omitted here because C220111
# is a derived rollup account (installation_frac × (C220101+...+C220110)), and
# the validator forbids overriding derived rollup accounts. To express TAE's "50%
# complexity reduction" claim, the correct approach would be to override
# installation_frac via costing_overrides, but the 50% claim lacks bottom-up
# grounding (marketing language, not quantified). The reduction is already
# partially captured by other overrides (lower blanket cost, simpler magnets,
# no divertor). Section 5b listed 9 override candidates; 7 are transcribed below
# (6 enabled, 1 disabled), with C220111 excluded per validator constraint.
overrides = [
    {
        "account": "C220101",
        "value": 0.50 * generic.cas22_detail["C220101"],
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "iter-01/sources/grokipedia-tae-technologies.md §Aneutronic Advantages",
        "rationale": (
            "p-B11 is aneutronic — no tritium breeding required, and secondary neutrons "
            "are <1% of fusion energy. The library's default first-wall/blanket cost "
            "assumes a tritium-breeding blanket with Li-6 enrichment, tritium extraction "
            "systems, and thick neutron shielding. TAE's blanket only needs to capture "
            "3 MeV alphas, X-rays, and trace secondary neutrons. Analogy to non-breeding "
            "test blankets in ITER suggests 40-60% cost reduction. Using 50% as mid-range "
            "estimate. This is a relative override (fraction of library's computation)."
        ),
    },
    {
        "account": "C220102",
        "value": 0.30 * generic.cas22_detail["C220102"],
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "iter-01/sources/grokipedia-tae-technologies.md §Neutron Management; iter-02/sources/tae-energy-conversion-clarification.md §Minimal Radioactivity",
        "rationale": (
            "p-B11 neutron wall loading is ~0.05-0.2 MW/m^2 (vs. 2-4 MW/m^2 for D-T). "
            "The library's default radiation shield is sized for 14.1 MeV D-T neutrons "
            "at high flux. TAE requires only thin shielding for secondary neutrons and "
            "X-rays (bremsstrahlung at 10-100 keV). Shielding thickness can be reduced "
            "by ~50-70%, and activation is minimal, potentially allowing contact "
            "maintenance. Using 70% cost reduction (30% of library value)."
        ),
    },
    {
        "account": "C220104",
        "value": 150.0,
        "enabled": False,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "iter-02/sources/tae-c2w-machine-details.md §NBI System; [ITER NBI cost analogy]",
        "rationale": (
            "NBI is TAE's dominant subsystem. C-2W uses 8 injectors at 21 MW total. "
            "Da Vinci plausibly requires 50-200 MW NBI (see Section 2). ITER's 33 MW "
            "NBI system is budgeted at ~$550M (~$17/W). At this scaling, 100 MW NBI "
            "would cost $1.7B, overwhelming the total plant budget. TAE claims 50% cost "
            "reduction from NBI-only formation, but this is relative to *reactor* "
            "complexity, not NBI unit cost. Conservative estimate: $10/W at volume "
            "production (learning curve from pulse power components) × 100 MW = $1B. "
            "Using $150M as floor estimate for optimistic mass production scenario. "
            "**DISABLED in baseline** because NBI power requirement itself is unknown "
            "(depends on Q). If Q=5 and NBI=80 MW, this override would apply. If Q=2 "
            "and NBI=200 MW, cost is 4x higher. Library default heating cost may "
            "already cover NBI adequately depending on archetype. Re-enable in "
            "sensitivity runs after Q is better constrained."
        ),
        "blocked_by": "1cFE/1costingfe#105",
    },
    {
        "account": "C220103",
        "value": 80.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "iter-02/sources/tae-c2w-machine-details.md §Magnet/Field Control; iter-01/sources/grokipedia-tae-technologies.md §Simple Geometry Magnets",
        "rationale": (
            "FRC near-unity beta (90-100%) means external magnetic field is weak "
            "(~0.2-0.5 T at Da Vinci scale, vs. 5-12 T for tokamak TF coils). C-2W "
            "uses copper resistive coils. TAE emphasizes 'simple geometry' magnets "
            "as a cost advantage. If Da Vinci uses copper, capital cost is low "
            "(~$50-100M for water-cooled copper coils at this scale) but resistive "
            "power is 10-20 MW continuous, costing $300-600M NPV over plant life. "
            "If HTS is used, capital is $150-300M but resistive losses drop to near "
            "zero. The economic optimum likely favors HTS at 30-year plant life. "
            "Using $80M as a conservative HTS estimate (lower than tokamak HTS due to "
            "simpler geometry and lower field). This is an absolute override, not "
            "relative, because the library's default HTS cost assumes complex 3D "
            "stellarator or high-field tokamak coils. FRC coils are axisymmetric "
            "solenoids (far simpler). If copper is used instead, cost drops to ~$50M "
            "but OPEX penalty via C220107 (power supplies running continuously)."
        ),
    },
    {
        "account": "C220108",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "direct",
        "source": "FRC geometry — axial end losses, not toroidal divertor",
        "rationale": (
            "The library's default C220108 assumes a toroidal divertor (W monoblock "
            "cassettes on CuCrZr heat sinks, as in ITER). FRC has axial end losses, "
            "not a toroidal divertor. The end regions require plasma-facing armor "
            "(likely tungsten tiles) but the geometry is open linear exhaust, not a "
            "complex cassette-based divertor. This hardware is better captured under "
            "C220105 (primary structure) or as part of the vacuum vessel (C220106). "
            "Setting C220108 to zero to avoid double-counting. If needed, add ~$20-50M "
            "to C220105 or C220106 for end-region armor in a separate override."
        ),
    },
    {
        "account": "CAS27",
        "value": 5.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "p-B11 fuel cycle — no tritium inventory; boron and hydrogen are commodity",
        "rationale": (
            "The library's CAS27 (special materials — initial reactor inventory) defaults "
            "to tritium startup inventory (~1-5 kg at $30k/g = $30-150M for D-T concepts). "
            "p-B11 requires no tritium. The initial fuel inventory is natural boron "
            "(80% B-11, ~$2/kg) and hydrogen (<$5/kg). At several kg inventory, fuel "
            "cost is <$100k. However, if beryllium is used in the blanket as neutron "
            "multiplier, that becomes the dominant CAS27 item. Assuming 5-10 tonnes Be "
            "at $800/kg = $4-8M. Using $5M as mid-range. If the blanket uses lithium "
            "or FLiBe instead of beryllium, cost drops to ~$1M (lithium is cheaper)."
        ),
    },
    {
        "account": "CAS80",
        "value": 0.05,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "p-B11 fuel consumption rate — grams/day scale",
        "rationale": (
            "The library's CAS80 (annualized fuel cost) defaults to D-T tritium breeding "
            "and D-D deuterium costs. p-B11 consumes protons and boron-11 at ~grams/day "
            "for a 50 MWe plant (fusion power 250-500 MW, reaction energy 8.7 MeV, "
            "yields ~10^20 reactions/s, or ~3-6 g/day total fuel). At commodity prices "
            "($2/kg boron, $5/kg H2), annual fuel cost is ~$5k-20k. Using $0.05M "
            "($50k/year) as upper bound. This is 100-1000x lower than D-T fuel cycle "
            "costs, a genuine advantage of p-B11. Note: if B-11 isotopic enrichment "
            "to >95% is required, fuel cost rises to $50-500/day or $20-200k/year — "
            "still negligible but 10x higher than natural boron."
        ),
    },
    {
        "account": "C220109",
        "value": 0.0,
        "enabled": True,
        "cost_basis": "noak",
        "provenance": "direct",
        "source": "iter-02/sources/tae-energy-conversion-clarification.md §Da Vinci uses thermal conversion",
        "rationale": (
            "Direct energy conversion (C220109) is not used in the Da Vinci design "
            "point. TAE's ICC technology is deferred to future plants. Da Vinci "
            "uses conventional thermal conversion, so C220109 = 0. The library "
            "default for this archetype may already be zero (DEC is rare for MFE), "
            "but setting it explicitly to ensure no DEC cost is included."
        ),
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
