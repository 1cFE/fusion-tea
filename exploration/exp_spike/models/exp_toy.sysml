package exp_toy {
    doc /*
    exp() mini-spike toy (exploration/exp_spike/).

    Tests the last untested pipeline claim: calc defs using math outside
    the mechanical arithmetic envelope (+ - * / **) survive extraction +
    generation via the AI implementation pass.

    The KerML/SysML v2 standard library has NO exp/ln/log (verified against
    syside 0.8.3's shipped sysml.library and the spec function library,
    section 9.4 — see findings.md). The only way to spell them in a model
    is an uninterpreted user calc def, invoked inline. That is exactly the
    out-of-envelope shape under test.
    */

    private import ScalarValues::*;

    // === Uninterpreted math functions (no stdlib equivalent) ===

    calc def Exp {
        doc /*
        Natural exponential e^x. Uninterpreted: no body in SysML —
        the implementation must come from the AI pass (math.exp).
        */
        in attribute x : Real;
        out attribute y : Real;
    }

    calc def Ln {
        doc /*
        Natural logarithm. Uninterpreted, same as Exp.
        */
        in attribute x : Real;
        out attribute y : Real;
    }

    // === Calcs under test ===

    calc def BoschHaleReactivity {
        doc /*
        Bosch-Hale-flavored DT reactivity shape:
            sigma_v = C * exp(-B / T^(1/3)) / T^(2/3)
        (NRL-formulary-style approximation, valid ~10s of keV; toy
        coefficients, physically shaped so success is meaningful).
        Out-of-envelope: contains an inline invocation of Exp.
        */
        in attribute t_kev : Real;
        in attribute c_coeff : Real;
        in attribute b_gamow : Real;
        out attribute sigma_v : Real = c_coeff * Exp(-b_gamow / t_kev ** (1.0/3.0)) / t_kev ** (2.0/3.0);
    }

    calc def GainDoublings {
        doc /*
        Number of doublings in the target gain: log2(G) = ln(G)/ln(2).
        Out-of-envelope: two inline invocations of Ln.
        */
        in attribute target_gain : Real;
        out attribute doublings : Real = Ln(target_gain) / Ln(2.0);
    }

    calc def ExpControl {
        doc /*
        In-envelope control: e^x spelled with the power operator and a
        literal e. Mathematically the same function as Exp; should
        auto-implement mechanically. Distinguishes "pipeline handles **"
        (already proven) from "pipeline handles unknown functions"
        (the claim under test).
        */
        in attribute exponent_arg : Real;
        out attribute e_to_x : Real = 2.718281828459045 ** exponent_arg;
    }

    // === Part wiring (single part, no cross-part refs) ===

    part def ExpPlant {
        attribute plasma_t_kev : Real;
        attribute reactivity_coeff : Real;
        attribute gamow_const : Real;
        attribute design_gain : Real;

        calc reactivity_calc : BoschHaleReactivity {
            in t_kev = plasma_t_kev;
            in c_coeff = reactivity_coeff;
            in b_gamow = gamow_const;
        }

        calc doublings_calc : GainDoublings {
            in target_gain = design_gain;
        }

        calc exp_control_calc : ExpControl {
            in exponent_arg = plasma_t_kev;
        }
    }

    part exp_plant : ExpPlant {
        doc /*
        Concrete usage (template calcs are dropped without one).
        Toy DT-ish point: T = 10 keV, B = 19.98 keV^(1/3),
        C = 6.4e-14 (arbitrary toy units), G = 100.
        */
        attribute :>> plasma_t_kev = 10.0;
        attribute :>> reactivity_coeff = 6.4e-14;
        attribute :>> gamow_const = 19.98;
        attribute :>> design_gain = 100.0;
    }
}
