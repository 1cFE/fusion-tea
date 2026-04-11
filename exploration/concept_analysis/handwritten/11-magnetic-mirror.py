"""Example: DT Magnetic Mirror — cost breakdown and sensitivity analysis.

Models a simple-mirror / tandem-mirror DT fusion power plant using the
generic MFE power balance with mirror-specific geometry (cylindrical),
coil cost model (solenoid coils, lower markup), and direct energy
conversion on end-loss ions.
"""

from costingfe import ConfinementConcept, CostModel, Fuel

model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)
result = model.forward(
    cost_overrides={"CAS21": 250.0},
    net_electric_mw=500.0,
    availability=0.85,
    lifetime_yr=30,
    n_mod=1,
    construction_time_yr=5.0,
    interest_rate=0.07,
    inflation_rate=0.02,
    noak=True,
    # Mirror geometry (cylindrical)
    axis_t=0.0,            # No axis offset for cylinder
    plasma_t=1.5,          # Plasma radius [m]
    chamber_length=20.0,   # Cylinder length [m]
    blanket_t=0.60,        # Thinner blanket (shorter neutron path)
    ht_shield_t=0.20,
    structure_t=0.15,
    vessel_t=0.10,
    # Mirror power balance
    p_input=40.0,          # NBI-dominated heating [MW]
    mn=1.1,                # Blanket neutron multiplier
    eta_th=0.50,           # Lower thermal efficiency 
    eta_p=0.5,             # Pumping efficiency
    eta_pin=0.5,           # Heating wall-plug efficiency
    eta_de=0.60,           # DEC efficiency on end-loss ions
    f_sub=0.03,            # BOP subsystem fraction
    f_dec=0.30,            # Fraction of transport power to DEC
    p_coils=5.0,           # Solenoid coil power [MW]
    p_cool=20.0,           # Cooling [MW]
    p_pump=1.5,            # Pumping [MW]
    p_trit=10.0,           # Tritium processing [MW]
    p_house=4.0,           # Housekeeping [MW]
    p_cryo=1.0,            # Cryogenic [MW]
)

# ── Results ───────────────────────────────────────────────────────────
c = result.costs
pt = result.power_table

print("DT Mirror — 500 MWe, 85% availability, 30 yr lifetime")
print(f"LCOE: {c.lcoe:.1f} $/MWh ({float(c.lcoe)/10:.2f} ¢/kWh) | Overnight: {c.overnight_cost:.0f} $/kW")
print(f"Fusion: {pt.p_fus:.0f} MW | Net: {pt.p_net:.0f} MW | Q_eng: {pt.q_eng:.1f}")
print(f"Recirculating fraction: {pt.rec_frac:.1%}")
print()

# ── Cost breakdown ────────────────────────────────────────────────────
cas = [
    ("CAS10", "Preconstruction", c.cas10),
    ("CAS21", "Buildings", c.cas21),
    ("CAS22", "Reactor Plant Equipment", c.cas22),
    ("CAS23", "Turbine Plant", c.cas23),
    ("CAS24", "Electrical Plant", c.cas24),
    ("CAS25", "Miscellaneous", c.cas25),
    ("CAS26", "Heat Rejection", c.cas26),
    ("CAS28", "Digital Twin", c.cas28),
    ("CAS29", "Contingency", c.cas29),
    ("CAS30", "Indirect Costs", c.cas30),
    ("CAS40", "Owner's Costs", c.cas40),
    ("CAS50", "Supplementary", c.cas50),
    ("CAS60", "IDC", c.cas60),
    ("CAS70", "O&M (annualized)", c.cas70),
    ("CAS80", "Fuel (annualized)", c.cas80),
    ("CAS90", "Financial", c.cas90),
]

print(f"{'Code':<8} {'Account':<28} {'M$':>10}")
print("-" * 48)
for code, name, val in cas:
    print(f"{code:<8} {name:<28} {float(val):>10.1f}")
print("-" * 48)
print(f"{'':8} {'Total Capital':<28} {float(c.total_capital):>10.1f}")

# ── CAS22 sub-account detail ─────────────────────────────────────────
print("\nCAS22 Reactor Plant Equipment Breakdown:")
print("-" * 48)
for k, v in sorted(result.cas22_detail.items()):
    if float(v) > 0:
        print(f"  {k:<28} {float(v):>10.1f} M$")

# ── Sensitivity Analysis ─────────────────────────────────────────────
sens = model.sensitivity(result.params)

print("\nSensitivity (elasticity = %LCOE / %param)")
print("-" * 48)

print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")

print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<28} {v:+.4f}")
    