"""Fuel_Cycle_FlowsModule Module Wrapper

TEAx module for Fuel_Cycle_Flows calculation.

Tritium flows of a D-T plant, reduced to conservation (WI-047):

  E_fus_J         = q_eff * mev_to_joules                        [J]
  burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
  inject_rate     = burn_rate / burn_fraction                    [atoms/s]
  exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
  loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
  tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                    / (eta_extract * burn_rate)                  [1]
  tbr_margin      = tbr_available - tbr_required                 [1]
  burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

One D-T reaction burns one tritium atom; the fusion power fixes the burn,
the single-pass burn fraction fixes the circulating stream, and the recovery
of the unburned stream fixes the permanent loss. The required breeding ratio
is the tritium that must be bred per atom burned to replace burn, permanent
loss, decay of the held inventory and any stock growth, divided by the
extraction efficiency from breeder to usable supply. The margin against the
ACHIEVED ratio a concept binds is a reported margin. In the WI-066
stellarator, a separate adequacy calculation compares computed breeding
with this requirement and the retained design floor. Its validity flag
also governs interpretation of this raw margin when transport is undefined.
Recovery remains an explicit conditional scenario, not a measured efficiency.

Inventory is supplied through I_total. WI-069 computes the stellarator stock
through the separate Fuel Inventory calculation; other instances may retain
dormant held inventory. G_stock remains an explicit stock-growth input. A duty factor multiplies operating burns
and flows in the plant (the calendar's productive time); stock decays through
calendar time too -- the two clocks are the lifecycle calc's, not this one's.

This calc computes REQUIRED breeding; achieved neutronics comes through
the blanket-owned tbr interface. 'DT Fuel Cost' (mfe_account_costs)
keeps its own burn correction on the same burn_fraction and the same
recovery number read as a feedstock cost factor; the two calcs read the
same inputs and mean different things, and say so.

Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
58 (startup as a residence-time balance, not computed here), 60 (the
conditional 1.19 finding)
*Basis**: Tritium conservation on the burned, circulating and bred streams

Inputs:
    - eta_extract_in: eta_extract_in parameter
    - s_per_fpy_in: s_per_fpy_in parameter
    - tbr_available_in: tbr_available_in parameter
    - lambda_T_in: lambda_T_in parameter
    - p_fus_in: p_fus_in parameter
    - q_eff_in: q_eff_in parameter
    - burn_fraction_in: burn_fraction_in parameter
    - G_stock_in: G_stock_in parameter
    - t_recycle_in: t_recycle_in parameter
    - m_T_kg_in: m_T_kg_in parameter
    - mev_to_joules_in: mev_to_joules_in parameter
    - I_total_in: I_total_in parameter

Outputs:
    - burn_kg_per_fpy: burn_kg_per_fpy result
    - inject_rate: inject_rate result
    - burn_rate: burn_rate result
    - tbr_margin: tbr_margin result
    - tbr_required: tbr_required result
    - loss_rate: loss_rate result
    - exhaust_rate: exhaust_rate result

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:4

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_fuel_cycle/fuel_cycle_flows_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.fuel_cycle_flows_output import Fuel_Cycle_FlowsOutput


class Fuel_Cycle_FlowsInput(BaseModel):
    """Input model for Fuel_Cycle_FlowsModule.

    Attributes:
        eta_extract_in: eta_extract_in input
        s_per_fpy_in: s_per_fpy_in input
        tbr_available_in: tbr_available_in input
        lambda_T_in: lambda_T_in input
        p_fus_in: p_fus_in input
        q_eff_in: q_eff_in input
        burn_fraction_in: burn_fraction_in input
        G_stock_in: G_stock_in input
        t_recycle_in: t_recycle_in input
        m_T_kg_in: m_T_kg_in input
        mev_to_joules_in: mev_to_joules_in input
        I_total_in: I_total_in input
    """
    eta_extract_in: float = Field(..., description="eta_extract_in input")
    s_per_fpy_in: float = Field(..., description="s_per_fpy_in input")
    tbr_available_in: float = Field(..., description="tbr_available_in input")
    lambda_T_in: float = Field(..., description="lambda_T_in input")
    p_fus_in: float = Field(..., description="p_fus_in input")
    q_eff_in: float = Field(..., description="q_eff_in input")
    burn_fraction_in: float = Field(..., description="burn_fraction_in input")
    G_stock_in: float = Field(..., description="G_stock_in input")
    t_recycle_in: float = Field(..., description="t_recycle_in input")
    m_T_kg_in: float = Field(..., description="m_T_kg_in input")
    mev_to_joules_in: float = Field(..., description="mev_to_joules_in input")
    I_total_in: float = Field(..., description="I_total_in input")


class Fuel_Cycle_FlowsModule(ModuleBase[Fuel_Cycle_FlowsInput, Fuel_Cycle_FlowsOutput]):
    """TEAx module for Fuel_Cycle_Flows calculation.

Tritium flows of a D-T plant, reduced to conservation (WI-047):

  E_fus_J         = q_eff * mev_to_joules                        [J]
  burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
  inject_rate     = burn_rate / burn_fraction                    [atoms/s]
  exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
  loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
  tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                    / (eta_extract * burn_rate)                  [1]
  tbr_margin      = tbr_available - tbr_required                 [1]
  burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

One D-T reaction burns one tritium atom; the fusion power fixes the burn,
the single-pass burn fraction fixes the circulating stream, and the recovery
of the unburned stream fixes the permanent loss. The required breeding ratio
is the tritium that must be bred per atom burned to replace burn, permanent
loss, decay of the held inventory and any stock growth, divided by the
extraction efficiency from breeder to usable supply. The margin against the
ACHIEVED ratio a concept binds is a reported margin. In the WI-066
stellarator, a separate adequacy calculation compares computed breeding
with this requirement and the retained design floor. Its validity flag
also governs interpretation of this raw margin when transport is undefined.
Recovery remains an explicit conditional scenario, not a measured efficiency.

Inventory is supplied through I_total. WI-069 computes the stellarator stock
through the separate Fuel Inventory calculation; other instances may retain
dormant held inventory. G_stock remains an explicit stock-growth input. A duty factor multiplies operating burns
and flows in the plant (the calendar's productive time); stock decays through
calendar time too -- the two clocks are the lifecycle calc's, not this one's.

This calc computes REQUIRED breeding; achieved neutronics comes through
the blanket-owned tbr interface. 'DT Fuel Cost' (mfe_account_costs)
keeps its own burn correction on the same burn_fraction and the same
recovery number read as a feedstock cost factor; the two calcs read the
same inputs and mean different things, and say so.

Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
58 (startup as a residence-time balance, not computed here), 60 (the
conditional 1.19 finding)
*Basis**: Tritium conservation on the burned, circulating and bred streams

Inputs:
    - eta_extract_in: eta_extract_in parameter
    - s_per_fpy_in: s_per_fpy_in parameter
    - tbr_available_in: tbr_available_in parameter
    - lambda_T_in: lambda_T_in parameter
    - p_fus_in: p_fus_in parameter
    - q_eff_in: q_eff_in parameter
    - burn_fraction_in: burn_fraction_in parameter
    - G_stock_in: G_stock_in parameter
    - t_recycle_in: t_recycle_in parameter
    - m_T_kg_in: m_T_kg_in parameter
    - mev_to_joules_in: mev_to_joules_in parameter
    - I_total_in: I_total_in parameter

Outputs:
    - burn_kg_per_fpy: burn_kg_per_fpy result
    - inject_rate: inject_rate result
    - burn_rate: burn_rate result
    - tbr_margin: tbr_margin result
    - tbr_required: tbr_required result
    - loss_rate: loss_rate result
    - exhaust_rate: exhaust_rate result

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:4

    SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:4

    Calculation Specification:
        s_per_fpy_in = 31536000.0
        E_fus_J = q_eff_in * mev_to_joules_in
        burn_rate = p_fus_in * 1000000.0 / E_fus_J
        inject_rate = burn_rate / burn_fraction_in
        exhaust_rate = inject_rate - burn_rate
        loss_rate = (1.0 - t_recycle_in) * exhaust_rate
        tbr_required = (burn_rate + loss_rate + lambda_T_in * I_total_in + G_stock_in) / (eta_extract_in * burn_rate)
        tbr_margin = tbr_available_in - tbr_required
        burn_kg_per_fpy = burn_rate * m_T_kg_in * s_per_fpy_in
        
Documentation:
Tritium flows of a D-T plant, reduced to conservation (WI-047):

  E_fus_J         = q_eff * mev_to_joules                        [J]
  burn_rate       = p_fus * 1e6 / E_fus_J                       [atoms/s]
  inject_rate     = burn_rate / burn_fraction                    [atoms/s]
  exhaust_rate    = inject_rate - burn_rate                      [atoms/s]
  loss_rate       = (1 - t_recycle) * exhaust_rate               [atoms/s]
  tbr_required    = (burn_rate + loss_rate + lambda_T * I_total + G_stock)
                    / (eta_extract * burn_rate)                  [1]
  tbr_margin      = tbr_available - tbr_required                 [1]
  burn_kg_per_fpy = burn_rate * m_T_kg * s_per_fpy               [kg per full-power year]

One D-T reaction burns one tritium atom; the fusion power fixes the burn,
the single-pass burn fraction fixes the circulating stream, and the recovery
of the unburned stream fixes the permanent loss. The required breeding ratio
is the tritium that must be bred per atom burned to replace burn, permanent
loss, decay of the held inventory and any stock growth, divided by the
extraction efficiency from breeder to usable supply. The margin against the
ACHIEVED ratio a concept binds is a reported margin. In the WI-066
stellarator, a separate adequacy calculation compares computed breeding
with this requirement and the retained design floor. Its validity flag
also governs interpretation of this raw margin when transport is undefined.
Recovery remains an explicit conditional scenario, not a measured efficiency.

Inventory is supplied through I_total. WI-069 computes the stellarator stock
through the separate Fuel Inventory calculation; other instances may retain
dormant held inventory. G_stock remains an explicit stock-growth input. A duty factor multiplies operating burns
and flows in the plant (the calendar's productive time); stock decays through
calendar time too -- the two clocks are the lifecycle calc's, not this one's.

This calc computes REQUIRED breeding; achieved neutronics comes through
the blanket-owned tbr interface. 'DT Fuel Cost' (mfe_account_costs)
keeps its own burn correction on the same burn_fraction and the same
recovery number read as a feedstock cost factor; the two calcs read the
same inputs and mean different things, and say so.

Flat-Real (+ - * /) -- lowers to generated arithmetic; no manual stage.

*Source**: knowledge/research/pending/20260907-163520_demo-breadth-disposition-prework.md
*Ref**: lines 43-54 (the conservation equations in T atoms/s), 56 (the NIST
half-life 4500 +/- 8 d, Lucas and Unterweger, J. Res. NIST 105 (2000) 541),
58 (startup as a residence-time balance, not computed here), 60 (the
conditional 1.19 finding)
*Basis**: Tritium conservation on the burned, circulating and bred streams

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_fuel_cycle.fuel_cycle_flows_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts burn_kg_per_fpy, inject_rate, burn_rate, tbr_margin, tbr_required, loss_rate, exhaust_rate fields to separate channels.
    """

    name: str = "Fuel_Cycle_FlowsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, eta_extract_in: float, s_per_fpy_in: float, tbr_available_in: float, lambda_T_in: float, p_fus_in: float, q_eff_in: float, burn_fraction_in: float, G_stock_in: float, t_recycle_in: float, m_T_kg_in: float, mev_to_joules_in: float, I_total_in: float    ) -> Fuel_Cycle_FlowsInput:
        """Validate inputs and fill defaults.

        Args:
            eta_extract_in: eta_extract_in input
            s_per_fpy_in: s_per_fpy_in input
            tbr_available_in: tbr_available_in input
            lambda_T_in: lambda_T_in input
            p_fus_in: p_fus_in input
            q_eff_in: q_eff_in input
            burn_fraction_in: burn_fraction_in input
            G_stock_in: G_stock_in input
            t_recycle_in: t_recycle_in input
            m_T_kg_in: m_T_kg_in input
            mev_to_joules_in: mev_to_joules_in input
            I_total_in: I_total_in input

        Returns:
            Validated input model
        """
        return Fuel_Cycle_FlowsInput(eta_extract_in=eta_extract_in, s_per_fpy_in=s_per_fpy_in, tbr_available_in=tbr_available_in, lambda_T_in=lambda_T_in, p_fus_in=p_fus_in, q_eff_in=q_eff_in, burn_fraction_in=burn_fraction_in, G_stock_in=G_stock_in, t_recycle_in=t_recycle_in, m_T_kg_in=m_T_kg_in, mev_to_joules_in=mev_to_joules_in, I_total_in=I_total_in)

    def run(
        self, eta_extract_in: float, s_per_fpy_in: float, tbr_available_in: float, lambda_T_in: float, p_fus_in: float, q_eff_in: float, burn_fraction_in: float, G_stock_in: float, t_recycle_in: float, m_T_kg_in: float, mev_to_joules_in: float, I_total_in: float    ) -> ModuleResult[Fuel_Cycle_FlowsOutput]:
        """Execute calculation.

        Args:
            eta_extract_in: eta_extract_in input
            s_per_fpy_in: s_per_fpy_in input
            tbr_available_in: tbr_available_in input
            lambda_T_in: lambda_T_in input
            p_fus_in: p_fus_in input
            q_eff_in: q_eff_in input
            burn_fraction_in: burn_fraction_in input
            G_stock_in: G_stock_in input
            t_recycle_in: t_recycle_in input
            m_T_kg_in: m_T_kg_in input
            mev_to_joules_in: mev_to_joules_in input
            I_total_in: I_total_in input

        Returns:
            Module result with Fuel_Cycle_FlowsOutput (burn_kg_per_fpy, inject_rate, burn_rate, tbr_margin, tbr_required, loss_rate, exhaust_rate)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(eta_extract_in, s_per_fpy_in, tbr_available_in, lambda_T_in, p_fus_in, q_eff_in, burn_fraction_in, G_stock_in, t_recycle_in, m_T_kg_in, mev_to_joules_in, I_total_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_fuel_cycle.fuel_cycle_flows_impl import (
            run_fuel_cycle_flows,
        )

        # Execute implementation - returns tuple of values
        burn_kg_per_fpy, inject_rate, burn_rate, tbr_margin, tbr_required, loss_rate, exhaust_rate = run_fuel_cycle_flows(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Fuel_Cycle_FlowsOutput(
                burn_kg_per_fpy=burn_kg_per_fpy,
                inject_rate=inject_rate,
                burn_rate=burn_rate,
                tbr_margin=tbr_margin,
                tbr_required=tbr_required,
                loss_rate=loss_rate,
                exhaust_rate=exhaust_rate,
            )
        )
