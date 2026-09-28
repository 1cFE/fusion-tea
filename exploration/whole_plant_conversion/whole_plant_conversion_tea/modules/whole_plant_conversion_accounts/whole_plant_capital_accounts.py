"""Whole_Plant_Capital_AccountsModule Module Wrapper

TEAx module for Whole_Plant_Capital_Accounts calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_capital_accounts_impl.py; reviewed equations in design/configuration.

Inputs:
    - construction_years_in: construction_years_in parameter
    - source_installation_allowance_in: source_installation_allowance_in parameter
    - primary_pipes_in: primary_pipes_in parameter
    - commissioning_rate_in: commissioning_rate_in parameter
    - tritium_initial_in: tritium_initial_in parameter
    - fuel_processing_in: fuel_processing_in parameter
    - capital_2_in: capital_2_in parameter
    - salt_vendor_in: salt_vendor_in parameter
    - capital_9_in: capital_9_in parameter
    - primary_helium_in: primary_helium_in parameter
    - remote_handling_in: remote_handling_in parameter
    - contingency_rate_in: contingency_rate_in parameter
    - miscellaneous_in: miscellaneous_in parameter
    - power_supplies_in: power_supplies_in parameter
    - capital_10_in: capital_10_in parameter
    - primary_spares_in: primary_spares_in parameter
    - vessel_in: vessel_in parameter
    - capital_3_in: capital_3_in parameter
    - general_spares_rate_in: general_spares_rate_in parameter
    - capital_7_in: capital_7_in parameter
    - steam_branch_in: steam_branch_in parameter
    - indirect_rate_in: indirect_rate_in parameter
    - controller_capital_in: controller_capital_in parameter
    - pbl_initial_in: pbl_initial_in parameter
    - capital_8_in: capital_8_in parameter
    - capital_4_in: capital_4_in parameter
    - magnet_in: magnet_in parameter
    - installation_in: installation_in parameter
    - shared_electrical_in: shared_electrical_in parameter
    - capital_5_in: capital_5_in parameter
    - insurance_rate_in: insurance_rate_in parameter
    - heating_in: heating_in parameter
    - divertor_in: divertor_in parameter
    - freight_rate_in: freight_rate_in parameter
    - other_reactor_in: other_reactor_in parameter
    - salt_spare_in: salt_spare_in parameter
    - auxiliary_rejection_in: auxiliary_rejection_in parameter
    - shield_in: shield_in parameter
    - facilities_in: facilities_in parameter
    - structure_in: structure_in parameter
    - primary_circulators_in: primary_circulators_in parameter
    - cryoplant_in: cryoplant_in parameter
    - blanket_in: blanket_in parameter
    - owner_in: owner_in parameter
    - land_in: land_in parameter
    - waste_in: waste_in parameter
    - capital_1_in: capital_1_in parameter
    - digital_twin_in: digital_twin_in parameter
    - reactor_controls_in: reactor_controls_in parameter
    - tax_rate_in: tax_rate_in parameter
    - capital_6_in: capital_6_in parameter

Outputs:
    - common_purchases: common_purchases result
    - nonfuel_commissioning: nonfuel_commissioning result
    - salvage_base: salvage_base result
    - equipment_base: equipment_base result
    - general_spares: general_spares result
    - indirect: indirect result
    - freight_base: freight_base result
    - cas50: cas50 result
    - freight: freight result
    - initial_capital: initial_capital result
    - direct_base: direct_base result
    - contingency: contingency result
    - branch_purchases: branch_purchases result
    - insurance: insurance result
    - tax: tax result
    - domain_supported: domain_supported result
    - reconciliation_residual: reconciliation_residual result
    - cas20: cas20 result
    - overhaul_base: overhaul_base result
    - general_spares_base: general_spares_base result
    - insurance_base: insurance_base result
    - cas30: cas30 result
    - tax_base: tax_base result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:178

SysML Source: root-0/whole_plant_conversion_accounts.sysml:178

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/whole_plant_conversion_accounts/whole_plant_capital_accounts_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.whole_plant_capital_accounts_output import Whole_Plant_Capital_AccountsOutput


class Whole_Plant_Capital_AccountsInput(BaseModel):
    """Input model for Whole_Plant_Capital_AccountsModule.

    Attributes:
        construction_years_in: construction_years_in input
        source_installation_allowance_in: source_installation_allowance_in input
        primary_pipes_in: primary_pipes_in input
        commissioning_rate_in: commissioning_rate_in input
        tritium_initial_in: tritium_initial_in input
        fuel_processing_in: fuel_processing_in input
        capital_2_in: capital_2_in input
        salt_vendor_in: salt_vendor_in input
        capital_9_in: capital_9_in input
        primary_helium_in: primary_helium_in input
        remote_handling_in: remote_handling_in input
        contingency_rate_in: contingency_rate_in input
        miscellaneous_in: miscellaneous_in input
        power_supplies_in: power_supplies_in input
        capital_10_in: capital_10_in input
        primary_spares_in: primary_spares_in input
        vessel_in: vessel_in input
        capital_3_in: capital_3_in input
        general_spares_rate_in: general_spares_rate_in input
        capital_7_in: capital_7_in input
        steam_branch_in: steam_branch_in input
        indirect_rate_in: indirect_rate_in input
        controller_capital_in: controller_capital_in input
        pbl_initial_in: pbl_initial_in input
        capital_8_in: capital_8_in input
        capital_4_in: capital_4_in input
        magnet_in: magnet_in input
        installation_in: installation_in input
        shared_electrical_in: shared_electrical_in input
        capital_5_in: capital_5_in input
        insurance_rate_in: insurance_rate_in input
        heating_in: heating_in input
        divertor_in: divertor_in input
        freight_rate_in: freight_rate_in input
        other_reactor_in: other_reactor_in input
        salt_spare_in: salt_spare_in input
        auxiliary_rejection_in: auxiliary_rejection_in input
        shield_in: shield_in input
        facilities_in: facilities_in input
        structure_in: structure_in input
        primary_circulators_in: primary_circulators_in input
        cryoplant_in: cryoplant_in input
        blanket_in: blanket_in input
        owner_in: owner_in input
        land_in: land_in input
        waste_in: waste_in input
        capital_1_in: capital_1_in input
        digital_twin_in: digital_twin_in input
        reactor_controls_in: reactor_controls_in input
        tax_rate_in: tax_rate_in input
        capital_6_in: capital_6_in input
    """
    construction_years_in: float = Field(..., description="construction_years_in input")
    source_installation_allowance_in: float = Field(..., description="source_installation_allowance_in input")
    primary_pipes_in: float = Field(..., description="primary_pipes_in input")
    commissioning_rate_in: float = Field(..., description="commissioning_rate_in input")
    tritium_initial_in: float = Field(..., description="tritium_initial_in input")
    fuel_processing_in: float = Field(..., description="fuel_processing_in input")
    capital_2_in: float = Field(..., description="capital_2_in input")
    salt_vendor_in: float = Field(..., description="salt_vendor_in input")
    capital_9_in: float = Field(..., description="capital_9_in input")
    primary_helium_in: float = Field(..., description="primary_helium_in input")
    remote_handling_in: float = Field(..., description="remote_handling_in input")
    contingency_rate_in: float = Field(..., description="contingency_rate_in input")
    miscellaneous_in: float = Field(..., description="miscellaneous_in input")
    power_supplies_in: float = Field(..., description="power_supplies_in input")
    capital_10_in: float = Field(..., description="capital_10_in input")
    primary_spares_in: float = Field(..., description="primary_spares_in input")
    vessel_in: float = Field(..., description="vessel_in input")
    capital_3_in: float = Field(..., description="capital_3_in input")
    general_spares_rate_in: float = Field(..., description="general_spares_rate_in input")
    capital_7_in: float = Field(..., description="capital_7_in input")
    steam_branch_in: float = Field(..., description="steam_branch_in input")
    indirect_rate_in: float = Field(..., description="indirect_rate_in input")
    controller_capital_in: float = Field(..., description="controller_capital_in input")
    pbl_initial_in: float = Field(..., description="pbl_initial_in input")
    capital_8_in: float = Field(..., description="capital_8_in input")
    capital_4_in: float = Field(..., description="capital_4_in input")
    magnet_in: float = Field(..., description="magnet_in input")
    installation_in: float = Field(..., description="installation_in input")
    shared_electrical_in: float = Field(..., description="shared_electrical_in input")
    capital_5_in: float = Field(..., description="capital_5_in input")
    insurance_rate_in: float = Field(..., description="insurance_rate_in input")
    heating_in: float = Field(..., description="heating_in input")
    divertor_in: float = Field(..., description="divertor_in input")
    freight_rate_in: float = Field(..., description="freight_rate_in input")
    other_reactor_in: float = Field(..., description="other_reactor_in input")
    salt_spare_in: float = Field(..., description="salt_spare_in input")
    auxiliary_rejection_in: float = Field(..., description="auxiliary_rejection_in input")
    shield_in: float = Field(..., description="shield_in input")
    facilities_in: float = Field(..., description="facilities_in input")
    structure_in: float = Field(..., description="structure_in input")
    primary_circulators_in: float = Field(..., description="primary_circulators_in input")
    cryoplant_in: float = Field(..., description="cryoplant_in input")
    blanket_in: float = Field(..., description="blanket_in input")
    owner_in: float = Field(..., description="owner_in input")
    land_in: float = Field(..., description="land_in input")
    waste_in: float = Field(..., description="waste_in input")
    capital_1_in: float = Field(..., description="capital_1_in input")
    digital_twin_in: float = Field(..., description="digital_twin_in input")
    reactor_controls_in: float = Field(..., description="reactor_controls_in input")
    tax_rate_in: float = Field(..., description="tax_rate_in input")
    capital_6_in: float = Field(..., description="capital_6_in input")


class Whole_Plant_Capital_AccountsModule(ModuleBase[Whole_Plant_Capital_AccountsInput, Whole_Plant_Capital_AccountsOutput]):
    """TEAx module for Whole_Plant_Capital_Accounts calculation.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_capital_accounts_impl.py; reviewed equations in design/configuration.

Inputs:
    - construction_years_in: construction_years_in parameter
    - source_installation_allowance_in: source_installation_allowance_in parameter
    - primary_pipes_in: primary_pipes_in parameter
    - commissioning_rate_in: commissioning_rate_in parameter
    - tritium_initial_in: tritium_initial_in parameter
    - fuel_processing_in: fuel_processing_in parameter
    - capital_2_in: capital_2_in parameter
    - salt_vendor_in: salt_vendor_in parameter
    - capital_9_in: capital_9_in parameter
    - primary_helium_in: primary_helium_in parameter
    - remote_handling_in: remote_handling_in parameter
    - contingency_rate_in: contingency_rate_in parameter
    - miscellaneous_in: miscellaneous_in parameter
    - power_supplies_in: power_supplies_in parameter
    - capital_10_in: capital_10_in parameter
    - primary_spares_in: primary_spares_in parameter
    - vessel_in: vessel_in parameter
    - capital_3_in: capital_3_in parameter
    - general_spares_rate_in: general_spares_rate_in parameter
    - capital_7_in: capital_7_in parameter
    - steam_branch_in: steam_branch_in parameter
    - indirect_rate_in: indirect_rate_in parameter
    - controller_capital_in: controller_capital_in parameter
    - pbl_initial_in: pbl_initial_in parameter
    - capital_8_in: capital_8_in parameter
    - capital_4_in: capital_4_in parameter
    - magnet_in: magnet_in parameter
    - installation_in: installation_in parameter
    - shared_electrical_in: shared_electrical_in parameter
    - capital_5_in: capital_5_in parameter
    - insurance_rate_in: insurance_rate_in parameter
    - heating_in: heating_in parameter
    - divertor_in: divertor_in parameter
    - freight_rate_in: freight_rate_in parameter
    - other_reactor_in: other_reactor_in parameter
    - salt_spare_in: salt_spare_in parameter
    - auxiliary_rejection_in: auxiliary_rejection_in parameter
    - shield_in: shield_in parameter
    - facilities_in: facilities_in parameter
    - structure_in: structure_in parameter
    - primary_circulators_in: primary_circulators_in parameter
    - cryoplant_in: cryoplant_in parameter
    - blanket_in: blanket_in parameter
    - owner_in: owner_in parameter
    - land_in: land_in parameter
    - waste_in: waste_in parameter
    - capital_1_in: capital_1_in parameter
    - digital_twin_in: digital_twin_in parameter
    - reactor_controls_in: reactor_controls_in parameter
    - tax_rate_in: tax_rate_in parameter
    - capital_6_in: capital_6_in parameter

Outputs:
    - common_purchases: common_purchases result
    - nonfuel_commissioning: nonfuel_commissioning result
    - salvage_base: salvage_base result
    - equipment_base: equipment_base result
    - general_spares: general_spares result
    - indirect: indirect result
    - freight_base: freight_base result
    - cas50: cas50 result
    - freight: freight result
    - initial_capital: initial_capital result
    - direct_base: direct_base result
    - contingency: contingency result
    - branch_purchases: branch_purchases result
    - insurance: insurance result
    - tax: tax result
    - domain_supported: domain_supported result
    - reconciliation_residual: reconciliation_residual result
    - cas20: cas20 result
    - overhaul_base: overhaul_base result
    - general_spares_base: general_spares_base result
    - insurance_base: insurance_base result
    - cas30: cas30 result
    - tax_base: tax_base result

SysML Source: root-0/whole_plant_conversion_accounts.sysml:178

    SysML Source: root-0/whole_plant_conversion_accounts.sysml:178

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_capital_accounts_impl.py; reviewed equations in design/configuration.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.whole_plant_capital_accounts_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts common_purchases, nonfuel_commissioning, salvage_base, equipment_base, general_spares, indirect, freight_base, cas50, freight, initial_capital, direct_base, contingency, branch_purchases, insurance, tax, domain_supported, reconciliation_residual, cas20, overhaul_base, general_spares_base, insurance_base, cas30, tax_base fields to separate channels.
    """

    name: str = "Whole_Plant_Capital_AccountsModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, construction_years_in: float, source_installation_allowance_in: float, primary_pipes_in: float, commissioning_rate_in: float, tritium_initial_in: float, fuel_processing_in: float, capital_2_in: float, salt_vendor_in: float, capital_9_in: float, primary_helium_in: float, remote_handling_in: float, contingency_rate_in: float, miscellaneous_in: float, power_supplies_in: float, capital_10_in: float, primary_spares_in: float, vessel_in: float, capital_3_in: float, general_spares_rate_in: float, capital_7_in: float, steam_branch_in: float, indirect_rate_in: float, controller_capital_in: float, pbl_initial_in: float, capital_8_in: float, capital_4_in: float, magnet_in: float, installation_in: float, shared_electrical_in: float, capital_5_in: float, insurance_rate_in: float, heating_in: float, divertor_in: float, freight_rate_in: float, other_reactor_in: float, salt_spare_in: float, auxiliary_rejection_in: float, shield_in: float, facilities_in: float, structure_in: float, primary_circulators_in: float, cryoplant_in: float, blanket_in: float, owner_in: float, land_in: float, waste_in: float, capital_1_in: float, digital_twin_in: float, reactor_controls_in: float, tax_rate_in: float, capital_6_in: float    ) -> Whole_Plant_Capital_AccountsInput:
        """Validate inputs and fill defaults.

        Args:
            construction_years_in: construction_years_in input
            source_installation_allowance_in: source_installation_allowance_in input
            primary_pipes_in: primary_pipes_in input
            commissioning_rate_in: commissioning_rate_in input
            tritium_initial_in: tritium_initial_in input
            fuel_processing_in: fuel_processing_in input
            capital_2_in: capital_2_in input
            salt_vendor_in: salt_vendor_in input
            capital_9_in: capital_9_in input
            primary_helium_in: primary_helium_in input
            remote_handling_in: remote_handling_in input
            contingency_rate_in: contingency_rate_in input
            miscellaneous_in: miscellaneous_in input
            power_supplies_in: power_supplies_in input
            capital_10_in: capital_10_in input
            primary_spares_in: primary_spares_in input
            vessel_in: vessel_in input
            capital_3_in: capital_3_in input
            general_spares_rate_in: general_spares_rate_in input
            capital_7_in: capital_7_in input
            steam_branch_in: steam_branch_in input
            indirect_rate_in: indirect_rate_in input
            controller_capital_in: controller_capital_in input
            pbl_initial_in: pbl_initial_in input
            capital_8_in: capital_8_in input
            capital_4_in: capital_4_in input
            magnet_in: magnet_in input
            installation_in: installation_in input
            shared_electrical_in: shared_electrical_in input
            capital_5_in: capital_5_in input
            insurance_rate_in: insurance_rate_in input
            heating_in: heating_in input
            divertor_in: divertor_in input
            freight_rate_in: freight_rate_in input
            other_reactor_in: other_reactor_in input
            salt_spare_in: salt_spare_in input
            auxiliary_rejection_in: auxiliary_rejection_in input
            shield_in: shield_in input
            facilities_in: facilities_in input
            structure_in: structure_in input
            primary_circulators_in: primary_circulators_in input
            cryoplant_in: cryoplant_in input
            blanket_in: blanket_in input
            owner_in: owner_in input
            land_in: land_in input
            waste_in: waste_in input
            capital_1_in: capital_1_in input
            digital_twin_in: digital_twin_in input
            reactor_controls_in: reactor_controls_in input
            tax_rate_in: tax_rate_in input
            capital_6_in: capital_6_in input

        Returns:
            Validated input model
        """
        return Whole_Plant_Capital_AccountsInput(construction_years_in=construction_years_in, source_installation_allowance_in=source_installation_allowance_in, primary_pipes_in=primary_pipes_in, commissioning_rate_in=commissioning_rate_in, tritium_initial_in=tritium_initial_in, fuel_processing_in=fuel_processing_in, capital_2_in=capital_2_in, salt_vendor_in=salt_vendor_in, capital_9_in=capital_9_in, primary_helium_in=primary_helium_in, remote_handling_in=remote_handling_in, contingency_rate_in=contingency_rate_in, miscellaneous_in=miscellaneous_in, power_supplies_in=power_supplies_in, capital_10_in=capital_10_in, primary_spares_in=primary_spares_in, vessel_in=vessel_in, capital_3_in=capital_3_in, general_spares_rate_in=general_spares_rate_in, capital_7_in=capital_7_in, steam_branch_in=steam_branch_in, indirect_rate_in=indirect_rate_in, controller_capital_in=controller_capital_in, pbl_initial_in=pbl_initial_in, capital_8_in=capital_8_in, capital_4_in=capital_4_in, magnet_in=magnet_in, installation_in=installation_in, shared_electrical_in=shared_electrical_in, capital_5_in=capital_5_in, insurance_rate_in=insurance_rate_in, heating_in=heating_in, divertor_in=divertor_in, freight_rate_in=freight_rate_in, other_reactor_in=other_reactor_in, salt_spare_in=salt_spare_in, auxiliary_rejection_in=auxiliary_rejection_in, shield_in=shield_in, facilities_in=facilities_in, structure_in=structure_in, primary_circulators_in=primary_circulators_in, cryoplant_in=cryoplant_in, blanket_in=blanket_in, owner_in=owner_in, land_in=land_in, waste_in=waste_in, capital_1_in=capital_1_in, digital_twin_in=digital_twin_in, reactor_controls_in=reactor_controls_in, tax_rate_in=tax_rate_in, capital_6_in=capital_6_in)

    def run(
        self, construction_years_in: float, source_installation_allowance_in: float, primary_pipes_in: float, commissioning_rate_in: float, tritium_initial_in: float, fuel_processing_in: float, capital_2_in: float, salt_vendor_in: float, capital_9_in: float, primary_helium_in: float, remote_handling_in: float, contingency_rate_in: float, miscellaneous_in: float, power_supplies_in: float, capital_10_in: float, primary_spares_in: float, vessel_in: float, capital_3_in: float, general_spares_rate_in: float, capital_7_in: float, steam_branch_in: float, indirect_rate_in: float, controller_capital_in: float, pbl_initial_in: float, capital_8_in: float, capital_4_in: float, magnet_in: float, installation_in: float, shared_electrical_in: float, capital_5_in: float, insurance_rate_in: float, heating_in: float, divertor_in: float, freight_rate_in: float, other_reactor_in: float, salt_spare_in: float, auxiliary_rejection_in: float, shield_in: float, facilities_in: float, structure_in: float, primary_circulators_in: float, cryoplant_in: float, blanket_in: float, owner_in: float, land_in: float, waste_in: float, capital_1_in: float, digital_twin_in: float, reactor_controls_in: float, tax_rate_in: float, capital_6_in: float    ) -> ModuleResult[Whole_Plant_Capital_AccountsOutput]:
        """Execute calculation.

        Args:
            construction_years_in: construction_years_in input
            source_installation_allowance_in: source_installation_allowance_in input
            primary_pipes_in: primary_pipes_in input
            commissioning_rate_in: commissioning_rate_in input
            tritium_initial_in: tritium_initial_in input
            fuel_processing_in: fuel_processing_in input
            capital_2_in: capital_2_in input
            salt_vendor_in: salt_vendor_in input
            capital_9_in: capital_9_in input
            primary_helium_in: primary_helium_in input
            remote_handling_in: remote_handling_in input
            contingency_rate_in: contingency_rate_in input
            miscellaneous_in: miscellaneous_in input
            power_supplies_in: power_supplies_in input
            capital_10_in: capital_10_in input
            primary_spares_in: primary_spares_in input
            vessel_in: vessel_in input
            capital_3_in: capital_3_in input
            general_spares_rate_in: general_spares_rate_in input
            capital_7_in: capital_7_in input
            steam_branch_in: steam_branch_in input
            indirect_rate_in: indirect_rate_in input
            controller_capital_in: controller_capital_in input
            pbl_initial_in: pbl_initial_in input
            capital_8_in: capital_8_in input
            capital_4_in: capital_4_in input
            magnet_in: magnet_in input
            installation_in: installation_in input
            shared_electrical_in: shared_electrical_in input
            capital_5_in: capital_5_in input
            insurance_rate_in: insurance_rate_in input
            heating_in: heating_in input
            divertor_in: divertor_in input
            freight_rate_in: freight_rate_in input
            other_reactor_in: other_reactor_in input
            salt_spare_in: salt_spare_in input
            auxiliary_rejection_in: auxiliary_rejection_in input
            shield_in: shield_in input
            facilities_in: facilities_in input
            structure_in: structure_in input
            primary_circulators_in: primary_circulators_in input
            cryoplant_in: cryoplant_in input
            blanket_in: blanket_in input
            owner_in: owner_in input
            land_in: land_in input
            waste_in: waste_in input
            capital_1_in: capital_1_in input
            digital_twin_in: digital_twin_in input
            reactor_controls_in: reactor_controls_in input
            tax_rate_in: tax_rate_in input
            capital_6_in: capital_6_in input

        Returns:
            Module result with Whole_Plant_Capital_AccountsOutput (common_purchases, nonfuel_commissioning, salvage_base, equipment_base, general_spares, indirect, freight_base, cas50, freight, initial_capital, direct_base, contingency, branch_purchases, insurance, tax, domain_supported, reconciliation_residual, cas20, overhaul_base, general_spares_base, insurance_base, cas30, tax_base)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(construction_years_in, source_installation_allowance_in, primary_pipes_in, commissioning_rate_in, tritium_initial_in, fuel_processing_in, capital_2_in, salt_vendor_in, capital_9_in, primary_helium_in, remote_handling_in, contingency_rate_in, miscellaneous_in, power_supplies_in, capital_10_in, primary_spares_in, vessel_in, capital_3_in, general_spares_rate_in, capital_7_in, steam_branch_in, indirect_rate_in, controller_capital_in, pbl_initial_in, capital_8_in, capital_4_in, magnet_in, installation_in, shared_electrical_in, capital_5_in, insurance_rate_in, heating_in, divertor_in, freight_rate_in, other_reactor_in, salt_spare_in, auxiliary_rejection_in, shield_in, facilities_in, structure_in, primary_circulators_in, cryoplant_in, blanket_in, owner_in, land_in, waste_in, capital_1_in, digital_twin_in, reactor_controls_in, tax_rate_in, capital_6_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.whole_plant_conversion_accounts.whole_plant_capital_accounts_impl import (
            run_whole_plant_capital_accounts,
        )

        # Execute implementation - returns tuple of values
        common_purchases, nonfuel_commissioning, salvage_base, equipment_base, general_spares, indirect, freight_base, cas50, freight, initial_capital, direct_base, contingency, branch_purchases, insurance, tax, domain_supported, reconciliation_residual, cas20, overhaul_base, general_spares_base, insurance_base, cas30, tax_base = run_whole_plant_capital_accounts(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Whole_Plant_Capital_AccountsOutput(
                common_purchases=common_purchases,
                nonfuel_commissioning=nonfuel_commissioning,
                salvage_base=salvage_base,
                equipment_base=equipment_base,
                general_spares=general_spares,
                indirect=indirect,
                freight_base=freight_base,
                cas50=cas50,
                freight=freight,
                initial_capital=initial_capital,
                direct_base=direct_base,
                contingency=contingency,
                branch_purchases=branch_purchases,
                insurance=insurance,
                tax=tax,
                domain_supported=domain_supported,
                reconciliation_residual=reconciliation_residual,
                cas20=cas20,
                overhaul_base=overhaul_base,
                general_spares_base=general_spares_base,
                insurance_base=insurance_base,
                cas30=cas30,
                tax_base=tax_base,
            )
        )
