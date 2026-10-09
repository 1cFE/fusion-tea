"""Auto-generated implementation for Vacuum_Gas_Load.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_vacuum.sysml:4

SysML Expressions:
    k_B_in = 1.380649e-23
    n_molecules = (exhaust_rate_D_in + exhaust_rate_T_in) / 2.0 + helium_rate_in
    Q_total = n_molecules * k_B_in * T_gas_in
    S_eff_required = Q_total / p_exhaust_in
    
Documentation:
Torus exhaust gas load after recombination (WI-047):

  n_molecules    = (exhaust_rate_D + exhaust_rate_T) / 2 + helium_rate   [molecules/s]
  Q_total        = n_molecules * k_B * T_gas                            [Pa m^3/s]
  S_eff_required = Q_total / p_exhaust                                  [m^3/s]

Hydrogen isotopes leave as diatomic molecules (D2, T2 and DT each carry two
nuclei, so the molecule count is the atom count over two, whatever the
pairing); helium ash is atomic. The throughput is the ideal-gas pV rate at
the stated gas temperature; the required effective speed is that throughput
divided by the pressure at the exhaust boundary. The pressure is a boundary
condition at a stated location -- neither the plasma pressure nor the pre-shot
base vacuum -- and no admissible source prints it for this machine; a concept
that declares one says so at the binding. Pump-inlet speed and effective
speed differ by duct conductance (1/S_eff = 1/S_pump + 1/C in the molecular,
linear-conductance case); ducts, species-dependent speeds, regeneration duty,
puff and seeding bypass, leakage and outgassing are not modelled. Nothing
here maps a neutron load to a target load, and neither the vessel volume nor
the coolant pumping power stands in for the gas load.

Flat-Real (+ - * /) -- no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 124-130 (species-resolved throughput after recombination,
Q = dN k_B T, S_eff = Q / p, conductance in series; Franchetti, CERN
Vacuum I, slides 24-27 and 43-46, as cited there; ITER vacuum-system
scope separation)
*Basis**: Gas conservation at the exhaust boundary; ideal-gas throughput
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_nb3sn_tea.modules.mfe_vacuum.vacuum_gas_load import Vacuum_Gas_LoadInput


def run_vacuum_gas_load(inputs: Vacuum_Gas_LoadInput) -> tuple[float, float, float]:
    """Execute Vacuum_Gas_Load calculation.

Torus exhaust gas load after recombination (WI-047):

  n_molecules    = (exhaust_rate_D + exhaust_rate_T) / 2 + helium_rate   [molecules/s]
  Q_total        = n_molecules * k_B * T_gas                            [Pa m^3/s]
  S_eff_required = Q_total / p_exhaust                                  [m^3/s]

Hydrogen isotopes leave as diatomic molecules (D2, T2 and DT each carry two
nuclei, so the molecule count is the atom count over two, whatever the
pairing); helium ash is atomic. The throughput is the ideal-gas pV rate at
the stated gas temperature; the required effective speed is that throughput
divided by the pressure at the exhaust boundary. The pressure is a boundary
condition at a stated location -- neither the plasma pressure nor the pre-shot
base vacuum -- and no admissible source prints it for this machine; a concept
that declares one says so at the binding. Pump-inlet speed and effective
speed differ by duct conductance (1/S_eff = 1/S_pump + 1/C in the molecular,
linear-conductance case); ducts, species-dependent speeds, regeneration duty,
puff and seeding bypass, leakage and outgassing are not modelled. Nothing
here maps a neutron load to a target load, and neither the vessel volume nor
the coolant pumping power stands in for the gas load.

Flat-Real (+ - * /) -- no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 124-130 (species-resolved throughput after recombination,
Q = dN k_B T, S_eff = Q / p, conductance in series; Franchetti, CERN
Vacuum I, slides 24-27 and 43-46, as cited there; ITER vacuum-system
scope separation)
*Basis**: Gas conservation at the exhaust boundary; ideal-gas throughput

SysML Source: root-0/analyses/mfe_vacuum.sysml:4

SysML Expressions:
    k_B_in = 1.380649e-23
    n_molecules = (exhaust_rate_D_in + exhaust_rate_T_in) / 2.0 + helium_rate_in
    Q_total = n_molecules * k_B_in * T_gas_in
    S_eff_required = Q_total / p_exhaust_in
    
Documentation:
Torus exhaust gas load after recombination (WI-047):

  n_molecules    = (exhaust_rate_D + exhaust_rate_T) / 2 + helium_rate   [molecules/s]
  Q_total        = n_molecules * k_B * T_gas                            [Pa m^3/s]
  S_eff_required = Q_total / p_exhaust                                  [m^3/s]

Hydrogen isotopes leave as diatomic molecules (D2, T2 and DT each carry two
nuclei, so the molecule count is the atom count over two, whatever the
pairing); helium ash is atomic. The throughput is the ideal-gas pV rate at
the stated gas temperature; the required effective speed is that throughput
divided by the pressure at the exhaust boundary. The pressure is a boundary
condition at a stated location -- neither the plasma pressure nor the pre-shot
base vacuum -- and no admissible source prints it for this machine; a concept
that declares one says so at the binding. Pump-inlet speed and effective
speed differ by duct conductance (1/S_eff = 1/S_pump + 1/C in the molecular,
linear-conductance case); ducts, species-dependent speeds, regeneration duty,
puff and seeding bypass, leakage and outgassing are not modelled. Nothing
here maps a neutron load to a target load, and neither the vessel volume nor
the coolant pumping power stands in for the gas load.

Flat-Real (+ - * /) -- no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 124-130 (species-resolved throughput after recombination,
Q = dN k_B T, S_eff = Q / p, conductance in series; Franchetti, CERN
Vacuum I, slides 24-27 and 43-46, as cited there; ITER vacuum-system
scope separation)
*Basis**: Gas conservation at the exhaust boundary; ideal-gas throughput

Args:
    inputs: Input parameters validated against Vacuum_Gas_LoadInput schema

Returns:
    tuple[float, ...]: (S_eff_required, Q_total, n_molecules)

Example:
    >>> inputs = Vacuum_Gas_LoadInput(...)
    >>> S_eff_required, Q_total, n_molecules = run_vacuum_gas_load(inputs)
    """
    n_molecules = (((inputs.exhaust_rate_D_in + inputs.exhaust_rate_T_in) / 2.0) + inputs.helium_rate_in)
    Q_total = ((n_molecules * inputs.k_B_in) * inputs.T_gas_in)
    return (
        (Q_total / inputs.p_exhaust_in),  # S_eff_required
        Q_total,
        n_molecules,
    )
