"""WI-027 D7 capture-probe setup: build two scratch model trees with candidate
rewirings so the INV-2 snapshot capture can be run against each.

Candidate A: passthrough calc reads the literal-default design attribute
             (`in v = beta`); design attributes kept as single value source.
Candidate B: passthrough calc reads an inline literal (`in v = 0.0276`);
             the standalone design attributes are folded into the calc usage.

Only the stellarator_plant.sysml (beta/tbr forms) needs rewiring; mfe_plant.sysml
asserts already read calc outputs (pb.p_net / pb.rec_frac) and resolve.
"""
import shutil
from pathlib import Path

SRC = Path("exploration/stellarator_e2e/models")
A = Path("/tmp/wi027_probeA_models")
B = Path("/tmp/wi027_probeB_models")

for d in (A, B):
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(SRC, d)

# --- The passthrough calc def (concept-agnostic plumbing), appended into the
#     mfe_viability library package, just before its closing brace. ---
CALC_DEF = '''
    calc def 'Scalar Value' {
        doc /*
        Identity passthrough: carries a scalar through a calc so a modeled
        constraint actual resolves to a calc output (INV-2 strict resolution
        synthesizes no entry point for a literal-valued design attribute).
        Value-preserving representation plumbing; no physics.
        */
        in attribute v : Real;
        out attribute value : Real = v;
    }
'''

def patch_viability(tree: Path):
    f = tree / "analyses/mfe_viability.sysml"
    txt = f.read_text()
    # insert CALC_DEF before the final closing brace of the package
    idx = txt.rstrip().rfind("}")
    txt = txt[:idx] + CALC_DEF + "\n}\n"
    f.write_text(txt)

patch_viability(A)
patch_viability(B)

PLANT = "designs/stellarator_09/stellarator_plant.sysml"

# The three asserts, retargeted to read the passthrough calc outputs.
ASSERTS_RETARGETED = '''        // Asserted viability constraints.
        assert constraint beta_ok : 'Beta Limit' {
            in beta = beta_val.value;
            in beta_limit = beta_limit_val.value;
        }
        assert constraint wall_load_ok : 'Neutron Wall Load Limit' {
            in wall_load = wall_load_calc.wall_load;
            in wall_load_limit = wall_load_limit_val.value;
        }
        assert constraint tbr_ok : 'TBR Floor' {
            in tbr = tbr_val.value;
            in tbr_floor = tbr_floor_val.value;
        }'''

ASSERTS_ORIGINAL = '''        // Asserted viability constraints.
        assert constraint beta_ok : 'Beta Limit' {
            in beta = beta;
            in beta_limit = beta_limit;
        }
        assert constraint wall_load_ok : 'Neutron Wall Load Limit' {
            in wall_load = wall_load_calc.wall_load;
            in wall_load_limit = wall_load_limit;
        }
        assert constraint tbr_ok : 'TBR Floor' {
            in tbr = tbr;
            in tbr_floor = tbr_floor;
        }'''

# Candidate A: calc usages read the (kept) design attributes.
A_CALCS = '''
        // WI-027 D7 (candidate A): route each literal-valued design attribute
        // through a passthrough calc so the constraint actuals resolve.
        calc beta_val : 'Scalar Value' { in v = beta; }
        calc beta_limit_val : 'Scalar Value' { in v = beta_limit; }
        calc wall_load_limit_val : 'Scalar Value' { in v = wall_load_limit; }
        calc tbr_val : 'Scalar Value' { in v = tbr; }
        calc tbr_floor_val : 'Scalar Value' { in v = tbr_floor; }

'''

fa = A / PLANT
txt = fa.read_text()
assert ASSERTS_ORIGINAL in txt, "A: assert block not found verbatim"
txt = txt.replace(ASSERTS_ORIGINAL, A_CALCS + ASSERTS_RETARGETED)
fa.write_text(txt)

# Candidate B: calc usages read inline literals; standalone attrs folded away.
fb = B / PLANT
txt = fb.read_text()
assert ASSERTS_ORIGINAL in txt, "B: assert block not found verbatim"
B_CALCS = '''
        // WI-027 D7 (candidate B): carry each constant inline on a passthrough
        // calc input so the constraint actuals resolve (attrs folded).
        calc beta_val : 'Scalar Value' { in v = 0.0276; }
        calc beta_limit_val : 'Scalar Value' { in v = 0.05; }
        calc wall_load_limit_val : 'Scalar Value' { in v = 4.05; }
        calc tbr_val : 'Scalar Value' { in v = 1.074; }
        calc tbr_floor_val : 'Scalar Value' { in v = 1.05; }

'''
txt = txt.replace(ASSERTS_ORIGINAL, B_CALCS + ASSERTS_RETARGETED)
fb.write_text(txt)

print("probe A tree:", A)
print("probe B tree:", B)
print("patched:", PLANT, "+ analyses/mfe_viability.sysml in both")
