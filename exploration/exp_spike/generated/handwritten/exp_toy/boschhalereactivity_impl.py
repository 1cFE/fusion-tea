from exp_toy_tea.modules.exp_toy.boschhalereactivity import BoschHaleReactivityInput


def run_boschhalereactivity(inputs: BoschHaleReactivityInput) -> float:
    """Execute BoschHaleReactivity calculation.

Bosch-Hale-flavored DT reactivity shape:
    sigma_v = C * exp(-B / T^(1/3)) / T^(2/3)
(NRL-formulary-style approximation, valid ~10s of keV; toy
coefficients, physically shaped so success is meaningful).
Out-of-envelope: contains an inline invocation of Exp.

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:39

SysML Expressions:
    sigma_v = c_coeff * Exp(-(b_gamow) / t_kev ** LiteralRationalEvaluation() / LiteralRationalEvaluation()) / t_kev ** LiteralRationalEvaluation() / LiteralRationalEvaluation()
    
Documentation:
Bosch-Hale-flavored DT reactivity shape:
    sigma_v = C * exp(-B / T^(1/3)) / T^(2/3)
(NRL-formulary-style approximation, valid ~10s of keV; toy
coefficients, physically shaped so success is meaningful).
Out-of-envelope: contains an inline invocation of Exp.

Args:
    inputs: Input parameters validated against BoschHaleReactivityInput schema

Returns:
    float: sigma_v

Example:
    >>> inputs = BoschHaleReactivityInput(...)
    >>> result = run_boschhalereactivity(inputs)

    Implementation Pattern:
        # Extract input fields from the validated Input model:
        t_kev = inputs.t_kev
        c_coeff = inputs.c_coeff
        b_gamow = inputs.b_gamow
        # Perform calculation using extracted values
        # Return result(s)
    """
    # AI-pass implementation (exp() spike). Faithful translation of the SysML
    # expression at models/exp_toy.sysml:51:
    #   sigma_v = c_coeff * Exp(-b_gamow / t_kev ** (1.0/3.0)) / t_kev ** (2.0/3.0)
    # Exp is the model's uninterpreted natural exponential -> math.exp.
    import math

    return (
        inputs.c_coeff
        * math.exp(-inputs.b_gamow / inputs.t_kev ** (1.0 / 3.0))
        / inputs.t_kev ** (2.0 / 3.0)
    )
