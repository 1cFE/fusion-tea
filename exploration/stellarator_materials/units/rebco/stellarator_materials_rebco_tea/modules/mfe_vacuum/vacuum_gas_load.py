"""Vacuum_Gas_LoadModule Module Wrapper

TEAx module for Vacuum_Gas_Load calculation.

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

Inputs:
    - T_gas_in: T_gas_in parameter
    - p_exhaust_in: p_exhaust_in parameter
    - helium_rate_in: helium_rate_in parameter
    - exhaust_rate_T_in: exhaust_rate_T_in parameter
    - exhaust_rate_D_in: exhaust_rate_D_in parameter
    - k_B_in: k_B_in parameter

Outputs:
    - S_eff_required: S_eff_required result
    - Q_total: Q_total result
    - n_molecules: n_molecules result

SysML Source: root-0/analyses/mfe_vacuum.sysml:4

SysML Source: root-0/analyses/mfe_vacuum.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_vacuum/vacuum_gas_load_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.vacuum_gas_load_output import Vacuum_Gas_LoadOutput


class Vacuum_Gas_LoadInput(BaseModel):
    """Input model for Vacuum_Gas_LoadModule.

    Attributes:
        T_gas_in: T_gas_in input
        p_exhaust_in: p_exhaust_in input
        helium_rate_in: helium_rate_in input
        exhaust_rate_T_in: exhaust_rate_T_in input
        exhaust_rate_D_in: exhaust_rate_D_in input
        k_B_in: k_B_in input
    """
    T_gas_in: float = Field(..., description="T_gas_in input")
    p_exhaust_in: float = Field(..., description="p_exhaust_in input")
    helium_rate_in: float = Field(..., description="helium_rate_in input")
    exhaust_rate_T_in: float = Field(..., description="exhaust_rate_T_in input")
    exhaust_rate_D_in: float = Field(..., description="exhaust_rate_D_in input")
    k_B_in: float = Field(..., description="k_B_in input")


class Vacuum_Gas_LoadModule(ModuleBase[Vacuum_Gas_LoadInput, Vacuum_Gas_LoadOutput]):
    """TEAx module for Vacuum_Gas_Load calculation.

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

Inputs:
    - T_gas_in: T_gas_in parameter
    - p_exhaust_in: p_exhaust_in parameter
    - helium_rate_in: helium_rate_in parameter
    - exhaust_rate_T_in: exhaust_rate_T_in parameter
    - exhaust_rate_D_in: exhaust_rate_D_in parameter
    - k_B_in: k_B_in parameter

Outputs:
    - S_eff_required: S_eff_required result
    - Q_total: Q_total result
    - n_molecules: n_molecules result

SysML Source: root-0/analyses/mfe_vacuum.sysml:4

    SysML Source: root-0/analyses/mfe_vacuum.sysml:4

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_vacuum.vacuum_gas_load_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts S_eff_required, Q_total, n_molecules fields to separate channels.
    """

    name: str = "Vacuum_Gas_LoadModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, T_gas_in: float, p_exhaust_in: float, helium_rate_in: float, exhaust_rate_T_in: float, exhaust_rate_D_in: float, k_B_in: float    ) -> Vacuum_Gas_LoadInput:
        """Validate inputs and fill defaults.

        Args:
            T_gas_in: T_gas_in input
            p_exhaust_in: p_exhaust_in input
            helium_rate_in: helium_rate_in input
            exhaust_rate_T_in: exhaust_rate_T_in input
            exhaust_rate_D_in: exhaust_rate_D_in input
            k_B_in: k_B_in input

        Returns:
            Validated input model
        """
        return Vacuum_Gas_LoadInput(T_gas_in=T_gas_in, p_exhaust_in=p_exhaust_in, helium_rate_in=helium_rate_in, exhaust_rate_T_in=exhaust_rate_T_in, exhaust_rate_D_in=exhaust_rate_D_in, k_B_in=k_B_in)

    def run(
        self, T_gas_in: float, p_exhaust_in: float, helium_rate_in: float, exhaust_rate_T_in: float, exhaust_rate_D_in: float, k_B_in: float    ) -> ModuleResult[Vacuum_Gas_LoadOutput]:
        """Execute calculation.

        Args:
            T_gas_in: T_gas_in input
            p_exhaust_in: p_exhaust_in input
            helium_rate_in: helium_rate_in input
            exhaust_rate_T_in: exhaust_rate_T_in input
            exhaust_rate_D_in: exhaust_rate_D_in input
            k_B_in: k_B_in input

        Returns:
            Module result with Vacuum_Gas_LoadOutput (S_eff_required, Q_total, n_molecules)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(T_gas_in, p_exhaust_in, helium_rate_in, exhaust_rate_T_in, exhaust_rate_D_in, k_B_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_vacuum.vacuum_gas_load_impl import (
            run_vacuum_gas_load,
        )

        # Execute implementation - returns tuple of values
        S_eff_required, Q_total, n_molecules = run_vacuum_gas_load(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Vacuum_Gas_LoadOutput(
                S_eff_required=S_eff_required,
                Q_total=Q_total,
                n_molecules=n_molecules,
            )
        )
