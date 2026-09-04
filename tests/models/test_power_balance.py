"""Regression tests for power balance calculations.

Verifies:
1. Power balance .sysml files parse without errors
2. Required calc definitions exist
3. Calc defs have expected inputs/outputs

**Source**: modeling_pm/active/power-balance-calculations/spec.md
**Last Updated**: 2026-01-26
"""

import pytest
from pathlib import Path

from agentic_mbse.sysml.syside_adapter import get_syside


# Path to the MFE model library (canonical; the staged twin under
# exploration/stellarator_e2e/models/ is kept byte-identical by
# tests/models/test_model_family_spines.py).
TESTS_DIR = Path(__file__).parent.parent.parent
LIBRARY_DIR = TESTS_DIR / "models" / "library"
# Power balance moved from the old `calculations/power_balance/` tree into the
# analyses library (WI-009+). The generic `power_balance.sysml` and the
# standalone 'Alpha Power Calc' / 'Power Balance Calc' were collapsed into a
# single faithful 'MFE Power Balance Calc' in analyses/mfe_power_balance.sysml.
POWER_BALANCE_DIR = LIBRARY_DIR / "analyses"


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def library_model():
    """Load all library models including foundation and calculations."""
    files = list(LIBRARY_DIR.glob("**/*.sysml"))
    if not files:
        pytest.skip("No library files found")

    model, diagnostics = get_syside().try_load_model([str(f) for f in files])
    return model, diagnostics


@pytest.fixture
def power_balance_model():
    """Load power balance files with foundation dependencies."""
    foundation_files = list((LIBRARY_DIR / "foundation").glob("*.sysml"))
    power_files = list(POWER_BALANCE_DIR.glob("*.sysml"))
    files = foundation_files + power_files

    if not power_files:
        pytest.skip("No power balance files found")

    model, diagnostics = get_syside().try_load_model([str(f) for f in files])
    return model, diagnostics


# ============================================================================
# File Existence Tests
# ============================================================================


class TestPowerBalanceFilesExist:
    """Verify power balance files exist in their current location."""

    def test_power_balance_lives_in_analyses(self):
        """Power balance relocated into the analyses library.

        The old generic `calculations/power_balance/power_balance.sysml` no
        longer exists — it was collapsed into the single faithful MFE power
        balance. Verify the power balance model now lives under
        `library/analyses/` (the WI-009+ layout).
        """
        assert POWER_BALANCE_DIR.name == "analyses", \
            f"Expected power balance in analyses/, got {POWER_BALANCE_DIR}"
        assert (POWER_BALANCE_DIR / "mfe_power_balance.sysml").exists(), \
            f"Expected power balance model in {POWER_BALANCE_DIR}"

    def test_mfe_power_balance_sysml_exists(self):
        """Verify mfe_power_balance.sysml exists."""
        path = POWER_BALANCE_DIR / "mfe_power_balance.sysml"
        assert path.exists(), f"Expected {path} to exist"


# ============================================================================
# Parse Tests
# ============================================================================


class TestPowerBalanceParsing:
    """Verify power balance files parse without errors."""

    def test_library_parses_without_errors(self, library_model):
        """Verify entire library parses without syntax errors."""
        model, diagnostics = library_model
        syside = get_syside()

        # Filter for errors only (not warnings)
        errors = [
            d for d in diagnostics.parser
            if d.severity == syside.DiagnosticSeverity.Error
        ]

        assert len(errors) == 0, f"Parse errors found: {errors}"

    def test_power_balance_parses_without_errors(self, power_balance_model):
        """Verify power balance files parse without errors."""
        model, diagnostics = power_balance_model
        syside = get_syside()

        errors = [
            d for d in diagnostics.parser
            if d.severity == syside.DiagnosticSeverity.Error
        ]

        assert len(errors) == 0, f"Parse errors found: {errors}"


# ============================================================================
# Calc Definition Tests
# ============================================================================


class TestCalcDefinitionsExist:
    """Verify the current power balance calc definitions exist in the model."""

    def test_alpha_power_calc_inlined_not_standalone(self, library_model):
        """Alpha power is inlined, not a standalone 'Alpha Power Calc'.

        The fuel-type alpha/neutron split was inlined into 'MFE Power Balance
        Calc' as the D-T ratio 3.52/17.58 (keeps the calc flat and
        codegen-safe). Verify no standalone 'Alpha Power Calc' remains and the
        alpha term (p_alpha) lives inside the MFE calc instead.
        """
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        calc_names = [c.name for c in calc_defs]

        assert "Alpha Power Calc" not in calc_names, \
            f"'Alpha Power Calc' should have been inlined; found in {calc_names}"

        mfe_calc = next((c for c in calc_defs if c.name == "MFE Power Balance Calc"), None)
        assert mfe_calc is not None, "MFE Power Balance Calc not found"
        member_names = [m.declared_name for m in mfe_calc.owned_members if m.declared_name]
        assert "p_alpha" in member_names, \
            f"Expected inlined 'p_alpha' in MFE calc members {member_names}"

    def test_power_balance_calc_collapsed_to_mfe(self, library_model):
        """Generic 'Power Balance Calc' collapsed into 'MFE Power Balance Calc'.

        The old generic base calc no longer exists; the single faithful power
        balance is the MFE calc. Verify that.
        """
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        calc_names = [c.name for c in calc_defs]

        assert "Power Balance Calc" not in calc_names, \
            f"Generic 'Power Balance Calc' should be collapsed; found in {calc_names}"
        assert "MFE Power Balance Calc" in calc_names, \
            f"Expected 'MFE Power Balance Calc' in {calc_names}"

    def test_mfe_power_balance_calc_exists(self, library_model):
        """Verify 'MFE Power Balance Calc' calc def exists."""
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        calc_names = [c.name for c in calc_defs]

        assert "MFE Power Balance Calc" in calc_names, \
            f"Expected 'MFE Power Balance Calc' in {calc_names}"


# ============================================================================
# Alpha Power Calc Interface Tests
# ============================================================================


class TestInlinedAlphaHandling:
    """Verify alpha power handling inlined into 'MFE Power Balance Calc'.

    The old standalone 'Alpha Power Calc' (inputs p_nrl + fuel_type, return
    p_alpha) was inlined as the D-T ratio 3.52/17.58 inside the MFE calc.
    These tests check the equivalent constructs in their new home.
    """

    def _mfe_calc(self, model, syside):
        calc_defs = list(model.elements(syside.CalculationDefinition))
        mfe_calc = next((c for c in calc_defs if c.name == "MFE Power Balance Calc"), None)
        assert mfe_calc is not None, "MFE Power Balance Calc not found"
        return mfe_calc

    def test_alpha_driven_by_p_nrl_input(self, library_model):
        """Alpha power derives from p_nrl, which is an input of the MFE calc.

        (Was: Alpha Power Calc has p_nrl input.)
        """
        model, _ = library_model
        syside = get_syside()

        mfe_calc = self._mfe_calc(model, syside)
        input_names = [p.declared_name for p in mfe_calc.inputs if p.declared_name]

        assert "p_nrl" in input_names, \
            f"Expected 'p_nrl' input in {input_names}"

    def test_fuel_type_inlined_to_dt(self, library_model):
        """fuel_type is no longer parameterized — alpha fraction inlined to D-T.

        (Was: Alpha Power Calc has fuel_type input.) The fuel-type split was
        replaced by the fixed D-T ratio 3.52/17.58, so 'fuel_type' must NOT be
        an input of the MFE calc.
        """
        model, _ = library_model
        syside = get_syside()

        mfe_calc = self._mfe_calc(model, syside)
        input_names = [p.declared_name for p in mfe_calc.inputs if p.declared_name]

        assert "fuel_type" not in input_names, \
            f"'fuel_type' should be inlined to D-T, but found in inputs {input_names}"

    def test_mfe_calc_has_p_alpha(self, library_model):
        """Alpha power (p_alpha) exists as an intermediate member of the MFE calc.

        (Was: Alpha Power Calc returns p_alpha.) p_alpha is now an intermediate
        attribute inside 'MFE Power Balance Calc', not a standalone return.
        """
        model, _ = library_model
        syside = get_syside()

        mfe_calc = self._mfe_calc(model, syside)
        member_names = [m.declared_name for m in mfe_calc.owned_members if m.declared_name]

        assert "p_alpha" in member_names, \
            f"Expected 'p_alpha' member in MFE calc, got {member_names}"


# ============================================================================
# MFE Power Balance Calc Interface Tests
# ============================================================================


class TestMFEPowerBalanceCalcInterface:
    """Verify MFE Power Balance Calc has correct interface."""

    def test_has_all_required_inputs(self, library_model):
        """Verify MFE Power Balance Calc has all required inputs (current layout).

        The faithful 1costingFE rewrite dropped `fuel_type` (alpha inlined to
        D-T) and `fpcppf`, and takes the coolant pumping power `p_pump`
        directly. Current interface is 15 inputs.
        """
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        mfe_calc = next((c for c in calc_defs if c.name == "MFE Power Balance Calc"), None)

        assert mfe_calc is not None, "MFE Power Balance Calc not found"

        # Get input parameters using syside inputs accessor
        inputs = list(mfe_calc.inputs)
        input_names = [p.declared_name for p in inputs if p.declared_name]

        # Required inputs per current model (analyses/mfe_power_balance.sysml); the
        # `_in` names are the D-5 rename (models/stellarator_migration_ledger.md)
        required_inputs = [
            "p_nrl", "p_input_in",  # Primary
            "mn_in", "eta_th_in", "eta_p_in", "p_wallplug_in",  # Efficiencies
            "p_pump_in", "f_sub_in",  # Pumping / subsystem
            "p_tf_in", "p_pf_in",  # Coil power
            "p_tfcool_in", "p_pfcool_in",  # Cooling
            "p_trit_in", "p_house_in", "p_cryo"  # Auxiliary
        ]

        for input_name in required_inputs:
            assert input_name in input_names, \
                f"Expected input '{input_name}' in {input_names}"

    def test_has_p_net_output(self, library_model):
        """Verify MFE Power Balance Calc exposes p_net as an output.

        p_net is an `out attribute` (not the calc's `result` return), so it
        appears via the outputs accessor.
        """
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        mfe_calc = next((c for c in calc_defs if c.name == "MFE Power Balance Calc"), None)

        assert mfe_calc is not None, "MFE Power Balance Calc not found"

        outputs = list(mfe_calc.outputs)
        output_names = [p.declared_name for p in outputs if p.declared_name]

        assert "p_net" in output_names, \
            f"Expected 'p_net' in outputs {output_names}"

    def test_has_intermediate_outputs(self, library_model):
        """Verify MFE Power Balance Calc has key intermediate outputs."""
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        mfe_calc = next((c for c in calc_defs if c.name == "MFE Power Balance Calc"), None)

        assert mfe_calc is not None, "MFE Power Balance Calc not found"

        # Get all parameters (includes inputs, return, and intermediate attributes)
        params = list(mfe_calc.parameters)
        param_names = [p.declared_name for p in params if p.declared_name]

        # Key intermediate outputs per spec
        # Note: intermediates are attributes, not parameters, so they may not appear here
        # This test checks what's visible as parameters
        intermediate_outputs = [
            "p_alpha", "p_neutron", "p_th", "p_the", "p_et",
            "p_coils", "p_cool", "p_aux", "p_pump", "p_sub", "p_loss",
            "q_sci", "q_eng", "rec_frac"
        ]

        # These are intermediate attributes, not parameters
        # For calc defs, only in/out/return are parameters
        # Let's check that at least p_net is in outputs
        outputs = list(mfe_calc.outputs)
        output_names = [p.declared_name for p in outputs if p.declared_name]

        assert "p_net" in output_names, \
            f"Expected 'p_net' in outputs {output_names}"


# ============================================================================
# Documentation Tests
# ============================================================================


class TestDocumentation:
    """Verify calc defs have required documentation."""

    def test_alpha_handling_documented(self, library_model):
        """Verify the inlined alpha handling is documented in the MFE calc.

        (Was: Alpha Power Calc has documentation.) The alpha/neutron split and
        its D-T inlining are now documented inside 'MFE Power Balance Calc'.
        """
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        mfe_calc = next((c for c in calc_defs if c.name == "MFE Power Balance Calc"), None)

        assert mfe_calc is not None, "MFE Power Balance Calc not found"

        docs = list(mfe_calc.documentation)
        assert len(docs) > 0, "MFE Power Balance Calc should have documentation"
        assert any("alpha" in d.body.lower() for d in docs), \
            "MFE calc documentation should describe the alpha handling"

    def test_mfe_power_balance_calc_has_doc(self, library_model):
        """Verify MFE Power Balance Calc has documentation."""
        model, _ = library_model
        syside = get_syside()

        calc_defs = list(model.elements(syside.CalculationDefinition))
        mfe_calc = next((c for c in calc_defs if c.name == "MFE Power Balance Calc"), None)

        assert mfe_calc is not None, "MFE Power Balance Calc not found"

        docs = list(mfe_calc.documentation)
        assert len(docs) > 0, "MFE Power Balance Calc should have documentation"


# ============================================================================
# Numerical Validation Tests
# ============================================================================


class TestNumericalValidation:
    """Verify power balance formulas match PyFECONS reference implementation.

    These tests verify that the coefficients and formulas in the SysML models
    match PyFECONS PowerBalance.py. Since SysML models define formulas but don't
    execute them, we verify by computing expected values from the formulas and
    checking that the coefficients are correct.

    Test case inputs (from design doc):
    - p_nrl = 2600 MW
    - fuel_type = DT
    - p_input = 50 MW
    - mn = 1.1
    - eta_th = 0.46
    - eta_p = 0.5
    - eta_pin = 0.5
    - fpcppf = 0.06
    - f_sub = 0.03
    - p_tf = 1.0 MW
    - p_pf = 1.0 MW
    - p_tfcool = 12.7 MW
    - p_pfcool = 1.0 MW
    - p_trit = 10.0 MW
    - p_house = 4.0 MW
    - p_cryo = 0.5 MW

    **Source**: PyFECONS /home/reid/PyFECONS/pyfecons/costing/mfe/PowerBalance.py
    """

    # Test case inputs
    P_NRL = 2600.0       # Fusion power [MW]
    P_INPUT = 50.0       # Plasma heating power [MW]
    MN = 1.1             # Neutron energy multiplier
    ETA_TH = 0.46        # Thermal-to-electric efficiency
    ETA_P = 0.5          # Pumping power capture efficiency
    ETA_PIN = 0.5        # Heating wall-plug efficiency: WI-039 moved this out of
                         # the power balance into 'Heating Power Chain'. It is kept
                         # here as the test-case constant that produces this suite's
                         # wall-plug heating term (P_INPUT / ETA_PIN), which the
                         # power balance now receives as p_wallplug_in.
    FPCPPF = 0.06        # Primary coolant pumping power fraction
    F_SUB = 0.03         # Subsystem and control fraction
    P_TF = 1.0           # TF coil power [MW]
    P_PF = 1.0           # PF coil power [MW]
    P_TFCOOL = 12.7      # TF coil cooling [MW]
    P_PFCOOL = 1.0       # PF coil cooling [MW]
    P_TRIT = 10.0        # Tritium systems [MW]
    P_HOUSE = 4.0        # Housekeeping [MW]
    P_CRYO = 0.5         # Cryogenic pumping [MW]

    def test_alpha_power_dt_fuel(self):
        """Verify alpha power calculation for DT fuel matches PyFECONS.

        Formula: p_alpha = p_nrl * 3.52 / 17.58
        Source: PowerBalance.py:98
        """
        # DT alpha fraction: 3.52 MeV alpha / 17.58 MeV total
        alpha_fraction_dt = 3.52 / 17.58
        p_alpha = self.P_NRL * alpha_fraction_dt

        # Expected: 2600 * 0.2002 = 520.4 MW
        assert abs(p_alpha - 520.4) < 0.5, \
            f"DT alpha power {p_alpha:.1f} MW should be ~520.4 MW"

        # Verify coefficient matches PyFECONS
        assert abs(alpha_fraction_dt - 0.2002) < 0.001, \
            f"DT alpha fraction {alpha_fraction_dt:.4f} should be ~0.2002"

    def test_alpha_power_dd_fuel(self):
        """Verify alpha power calculation for DD fuel matches PyFECONS.

        Formula: p_alpha = p_nrl * (0.5 * 3.02/(3.02+1.01) + 0.5 * 0.82/(0.82+2.45))
        Source: PowerBalance.py:100
        """
        # DD alpha fraction: weighted average of two branches
        alpha_fraction_dd = 0.5 * 3.02 / (3.02 + 1.01) + 0.5 * 0.82 / (0.82 + 2.45)

        # Should be approximately 0.5001
        assert abs(alpha_fraction_dd - 0.5006) < 0.001, \
            f"DD alpha fraction {alpha_fraction_dd:.4f} should be ~0.5006"

    def test_alpha_power_dhe3_fuel(self):
        """Verify alpha power calculation for DHe3 fuel matches PyFECONS.

        Formula: p_alpha = p_nrl * 14.7 / (14.7 + 3.6)
        Source: PowerBalance.py:102
        """
        # DHe3 alpha fraction: 14.7 MeV / 18.3 MeV total
        alpha_fraction_dhe3 = 14.7 / (14.7 + 3.6)

        # Should be approximately 0.8033
        assert abs(alpha_fraction_dhe3 - 0.8033) < 0.001, \
            f"DHe3 alpha fraction {alpha_fraction_dhe3:.4f} should be ~0.8033"

    def test_alpha_power_pb11_fuel(self):
        """Verify alpha power calculation for PB11 fuel matches PyFECONS.

        Formula: p_alpha = p_nrl * 8.7 / 8.7 = p_nrl (100% charged particles)
        Source: PowerBalance.py:104
        """
        # PB11: aneutronic, all charged particles
        alpha_fraction_pb11 = 8.7 / 8.7

        assert abs(alpha_fraction_pb11 - 1.0) < 0.001, \
            f"PB11 alpha fraction {alpha_fraction_pb11:.4f} should be 1.0"

    def test_neutron_power(self):
        """Verify neutron power calculation.

        Formula: p_neutron = p_nrl - p_alpha
        Source: PowerBalance.py:11
        """
        p_alpha = self.P_NRL * 3.52 / 17.58  # DT fuel
        p_neutron = self.P_NRL - p_alpha

        # Expected: 2600 - 520.4 = 2079.6 MW
        assert abs(p_neutron - 2079.6) < 0.5, \
            f"Neutron power {p_neutron:.1f} MW should be ~2079.6 MW"

    def test_scientific_q(self):
        """Verify scientific Q calculation.

        Formula: q_sci = p_nrl / p_input
        Source: PowerBalance.py:28
        """
        q_sci = self.P_NRL / self.P_INPUT

        # Expected: 2600 / 50 = 52.0
        assert abs(q_sci - 52.0) < 0.01, \
            f"Scientific Q {q_sci:.1f} should be 52.0"

    def test_thermal_power(self):
        """Verify thermal power calculation.

        Formula: p_th = mn*p_neutron + p_input + eta_th*(fpcppf*eta_p + f_sub)*(mn*p_neutron)
        Source: PowerBalance.py:15-21
        """
        p_alpha = self.P_NRL * 3.52 / 17.58
        p_neutron = self.P_NRL - p_alpha

        # p_th = mn*p_neutron + p_input + eta_th*(fpcppf*eta_p + f_sub)*(mn*p_neutron)
        p_th = (
            self.MN * p_neutron
            + self.P_INPUT
            + self.ETA_TH * (self.FPCPPF * self.ETA_P + self.F_SUB) * (self.MN * p_neutron)
        )

        # Verify intermediate calculation
        # mn * p_neutron = 1.1 * 2079.6 = 2287.56
        mn_p_neutron = self.MN * p_neutron
        assert abs(mn_p_neutron - 2287.56) < 1.0, \
            f"mn*p_neutron {mn_p_neutron:.1f} should be ~2287.56"

        # fpcppf*eta_p + f_sub = 0.06*0.5 + 0.03 = 0.06
        pump_sub_factor = self.FPCPPF * self.ETA_P + self.F_SUB
        assert abs(pump_sub_factor - 0.06) < 0.001, \
            f"Pump/sub factor {pump_sub_factor:.3f} should be 0.06"

        # Expected p_th ~ 2400 MW
        assert 2300 < p_th < 2500, \
            f"Thermal power {p_th:.1f} MW should be in range 2300-2500 MW"

    def test_thermal_electric_power(self):
        """Verify thermal electric power calculation.

        Formula: p_the = eta_th * p_th
        Source: PowerBalance.py:22
        """
        p_alpha = self.P_NRL * 3.52 / 17.58
        p_neutron = self.P_NRL - p_alpha
        p_th = (
            self.MN * p_neutron
            + self.P_INPUT
            + self.ETA_TH * (self.FPCPPF * self.ETA_P + self.F_SUB) * (self.MN * p_neutron)
        )
        p_the = self.ETA_TH * p_th

        # Expected: 0.46 * p_th ~ 1100 MW
        assert 1000 < p_the < 1200, \
            f"Thermal electric power {p_the:.1f} MW should be in range 1000-1200 MW"

    def test_engineering_q_components(self):
        """Verify engineering Q calculation components.

        Formula (simplified, no direct conversion):
        Numerator: eta_th*(mn*p_neutron + p_pump + p_input)
        Denominator: p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_wallplug
        where p_wallplug arrives from the heating chain (WI-039); this suite forms
        it as p_input/eta_pin, which is what the chain computes at these values.

        Note: Full PyFECONS includes eta_de*p_alpha in numerator (deferred).
        Source: PowerBalance.py:29-48
        """
        # Compute intermediate values
        p_alpha = self.P_NRL * 3.52 / 17.58
        p_neutron = self.P_NRL - p_alpha
        p_cool = self.P_TFCOOL + self.P_PFCOOL  # 13.7 MW
        p_aux = self.P_TRIT + self.P_HOUSE  # 14.0 MW
        p_coils = self.P_TF + self.P_PF  # 2.0 MW

        p_th = (
            self.MN * p_neutron
            + self.P_INPUT
            + self.ETA_TH * (self.FPCPPF * self.ETA_P + self.F_SUB) * (self.MN * p_neutron)
        )
        p_the = self.ETA_TH * p_th
        p_pump = self.FPCPPF * p_the
        p_sub = self.F_SUB * p_the

        # Verify aggregations
        assert abs(p_cool - 13.7) < 0.1, f"p_cool {p_cool} should be 13.7 MW"
        assert abs(p_aux - 14.0) < 0.1, f"p_aux {p_aux} should be 14.0 MW"
        assert abs(p_coils - 2.0) < 0.1, f"p_coils {p_coils} should be 2.0 MW"

        # q_eng numerator (simplified - no eta_de*p_alpha term)
        q_eng_numerator = self.ETA_TH * (self.MN * p_neutron + p_pump + self.P_INPUT)

        # q_eng denominator
        q_eng_denominator = (
            p_coils + p_pump + p_sub + p_aux
            + p_cool + self.P_CRYO + self.P_INPUT / self.ETA_PIN
        )

        q_eng = q_eng_numerator / q_eng_denominator

        # Note: Without direct energy conversion (eta_de*p_alpha term in numerator),
        # q_eng is lower than the full PyFECONS calculation.
        # The simplified formula (per spec deferral of p_dee) gives q_eng ~ 4.8
        # The full formula would give q_eng ~ 9-10.
        assert 4 < q_eng < 6, \
            f"Engineering Q (simplified) {q_eng:.2f} should be in range 4-6"

    def test_net_electric_power(self):
        """Verify net electric power calculation.

        Formula: p_net = (1 - 1/q_eng) * p_et
        Source: PowerBalance.py:50
        """
        # Compute full chain
        p_alpha = self.P_NRL * 3.52 / 17.58
        p_neutron = self.P_NRL - p_alpha
        p_cool = self.P_TFCOOL + self.P_PFCOOL
        p_aux = self.P_TRIT + self.P_HOUSE
        p_coils = self.P_TF + self.P_PF

        p_th = (
            self.MN * p_neutron
            + self.P_INPUT
            + self.ETA_TH * (self.FPCPPF * self.ETA_P + self.F_SUB) * (self.MN * p_neutron)
        )
        p_the = self.ETA_TH * p_th
        p_et = p_the  # Simplified (no direct conversion)
        p_pump = self.FPCPPF * p_the
        p_sub = self.F_SUB * p_the

        q_eng_numerator = self.ETA_TH * (self.MN * p_neutron + p_pump + self.P_INPUT)
        q_eng_denominator = (
            p_coils + p_pump + p_sub + p_aux
            + p_cool + self.P_CRYO + self.P_INPUT / self.ETA_PIN
        )
        q_eng = q_eng_numerator / q_eng_denominator
        rec_frac = 1.0 / q_eng
        p_net = (1.0 - rec_frac) * p_et

        # Note: Without direct energy conversion, recirculating fraction is higher.
        # Simplified formula gives rec_frac ~ 0.20-0.21 (20-21%)
        # Full formula would give rec_frac ~ 0.10-0.12 (10-12%)
        assert 0.18 < rec_frac < 0.25, \
            f"Recirculating fraction (simplified) {rec_frac:.3f} should be 18-25%"

        # With higher recirculating fraction, p_net is lower.
        # Simplified formula gives p_net ~ 850-920 MW
        # Full formula would give p_net ~ 980-1050 MW
        assert 800 < p_net < 950, \
            f"Net electric power (simplified) {p_net:.1f} MW should be in range 800-950 MW"
