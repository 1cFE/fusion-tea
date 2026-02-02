#!/usr/bin/env python3
"""Test script to investigate syside multiplicity behavior."""

import syside
import tempfile
import os


def test_multiplicity(code, description, verbose=False):
    """Test a SysML model and report multiplicity bounds."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sysml', delete=False) as f:
        f.write(code)
        temp_file = f.name

    try:
        model, errs = syside.try_load_model([temp_file])

        if errs.contains_errors():
            print(f"{description}: PARSE ERROR")
            for e in errs.errors:
                print(f"  {e}")
            return

        # Find the part with parameterized multiplicity
        for pd in model.nodes(syside.PartDefinition, include_subtypes=True):
            if 'System' in (pd.declared_name or ''):
                for feat in pd.owned_features:
                    if feat.declared_name == 'heater':
                        mult = feat.declared_multiplicity
                        if mult:
                            print(f"{description}: cached=({mult.cached_lower_bound}, {mult.cached_upper_bound})")
                            if verbose:
                                print(f"  lower_bound expr: {mult.lower_bound}")
                                print(f"  upper_bound expr: {mult.upper_bound}")
                                print(f"  bounds list: {mult.bounds}")
                                # Try to get the actual value from expressions
                                if mult.lower_bound:
                                    lb = mult.lower_bound
                                    if hasattr(lb, 'value'):
                                        print(f"  lower_bound.value: {lb.value}")
                                if mult.upper_bound:
                                    ub = mult.upper_bound
                                    if hasattr(ub, 'value'):
                                        print(f"  upper_bound.value: {ub.value}")
                        else:
                            print(f"{description}: No multiplicity")
    finally:
        os.unlink(temp_file)


# Test 1: default := 2 (the coffee maker pattern)
test1 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        attribute heater_count : Integer default := 2;

        part heater : 'Heating Element' [heater_count];
    }
}
"""

# Test 2: := 2 (initial, no default)
test2 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        attribute heater_count : Integer := 2;

        part heater : 'Heating Element' [heater_count];
    }
}
"""

# Test 3: = 2 (bound/fixed)
test3 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        attribute heater_count : Integer = 2;

        part heater : 'Heating Element' [heater_count];
    }
}
"""

# Test 4: Literal [2] for comparison
test4 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        part heater : 'Heating Element' [2];
    }
}
"""

# Test 5: default := 3 to see if upper bound changes
test5 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        attribute heater_count : Integer default := 3;

        part heater : 'Heating Element' [heater_count];
    }
}
"""

# Test 6: literal [5] to confirm pattern
test6 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        part heater : 'Heating Element' [5];
    }
}
"""

# Test 7: literal [1]
test7 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        part heater : 'Heating Element' [1];
    }
}
"""

# Test 8: explicit range [2..2]
test8 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        part heater : 'Heating Element' [2..2];
    }
}
"""

# Test 9: explicit range [2..5]
test9 = """
package Test {
    private import ScalarValues::Integer;

    abstract part def 'Costed Component' {
        attribute capital_cost : Integer;
    }

    part def 'Heating Element' :> 'Costed Component' {
        attribute power_rating : Integer;
    }

    part def 'Brewing System' :> 'Costed Component' {
        part heater : 'Heating Element' [2..5];
    }
}
"""

print("=== Multiplicity Bound Tests ===\n")
test_multiplicity(test1, "default := 2")
test_multiplicity(test2, ":= 2 (initial)")
test_multiplicity(test3, "= 2 (bound)")
test_multiplicity(test4, "literal [2]")
test_multiplicity(test5, "default := 3")
test_multiplicity(test6, "literal [5]")
test_multiplicity(test7, "literal [1]")
test_multiplicity(test8, "explicit [2..2]")
test_multiplicity(test9, "explicit [2..5]")

print("\n=== Verbose Test for literal [2] ===\n")
test_multiplicity(test4, "literal [2]", verbose=True)

print("\n=== Verbose Test for explicit [2..2] ===\n")
test_multiplicity(test8, "explicit [2..2]", verbose=True)
