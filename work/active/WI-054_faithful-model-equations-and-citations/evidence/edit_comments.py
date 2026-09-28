"""Exact bounded documentation corrections; executable preservation checked separately."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from tests.model_families import FAMILIES,canonical_path

def edit(path,old,new):
    p=ROOT/path;t=p.read_text();assert old in t,(path,old);p.write_text(t.replace(old,new))
edit('models/library/foundation/economic_parameter.sysml','work/active/WI-006_ife-cost-structure-library/spec.md','work/completed/20260302_WI-006_ife-cost-structure-library/spec.md')
edit('models/library/analyses/mfe_magnet_cost.sysml','work/active/WI-035_magnet-closure/design.md','work/completed/20260901_WI-035_magnet-closure/design.md')
edit('models/designs/stellarator_09/stellarator_plant.sysml','work/active/WI-041_source-anchored-wall-load-fence/design.md','work/completed/20260905_WI-041_source-anchored-wall-load-fence/design.md')
edit('models/library/analyses/mfe_plasma_sustainment.sysml',"            p_brems = 5.35e-37 * Z_eff * V\n                      * int n_e(rho)^2 * sqrt(T_e(rho)) dV'             [MW]\n            p_line  = f_W * V * int n_e(rho)^2 * L_z_W(T_e(rho)) dV'    [MW]\n                      (L_z_W: piecewise coronal cooling-curve fit)","            dV' = dV/V = 2 rho d rho; integral_0^1 dV' = 1          [1]\n            p_brems = 1e-6 * 5.35e-37 * Z_eff * V\n                      * int_0^1 n_e(rho)^2 * sqrt(T_e(rho)) dV'       [MW]\n            p_line  = 1e-6 * f_W * V\n                      * int_0^1 n_e(rho)^2 * L_z_W(T_e(rho)) dV'      [MW]\n                      (n_e: m^-3; T_e: keV; V: m^3; Z_eff and f_W: 1;\n                      brems coefficient: W m^3 keV^-1/2; L_z_W: W m^3,\n                      piecewise coronal cooling-curve fit; 1e-6: MW/W)")
edit('models/library/analyses/mfe_plasma_scaling.sysml',"        volume. f_shape is a dimensionless shape/packing factor: 1.0 for a pure\n        torus (tokamak, and the 1costingFE torus geometry), < 1 for a shaped\n        stellarator plasma whose twisted, non-circular cross-section encloses\n        less volume than the torus of the same R, a, kappa. Concept-agnostic:","        volume. f_shape is the dimensionless ratio of the concept's plasma\n        volume to this reference torus volume. It is 1.0 for the pure torus\n        (including the 1costingFE torus geometry); a shaped plasma may have a\n        ratio above or below 1 for its chosen R, a and kappa. Concept-agnostic:")
edit('models/library/analyses/mfe_plasma_scaling.sysml','        // 1costingFE torus geometry). A shaped stellarator sets f_shape < 1.','        // 1costingFE torus geometry). Set from the concept/reference volume ratio.')
edit('models/designs/generic_mfe/mfe_plant.sysml','        physics -> cost -> LCOE calc pipeline, and asserts the two viability\n        constraints. The MFE analogue', '        physics -> cost -> LCOE calc pipeline, and asserts power, heating,\n        magnet, primary-loop, cycle-domain and divertor viability constraints.\n        Instance-specific assertions extend these; the generated constraint\n        catalog records the executable set. The MFE analogue')
edit('models/designs/stellarator_09/stellarator_plant.sysml','        Proxima Fusion "Stellaris" -- concept-09 QI stellarator HTS power plant,','''        SOURCE LOCATORS used throughout this definition:
          stellaris-design-details.md =
            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
          images/ = knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/
          raw.pdf / raw PDF / iter-02 raw PDF = the registered KIT witness,
            knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
        Bare line references refer to the iter-01 text above; PDF pages and
        sections refer to the KIT witness. Images/PDF govern quantitative
        readings where extraction is garbled. Availability of these sources
        does not establish unrecorded quantitative adoption.

        Proxima Fusion "Stellaris" -- concept-09 QI stellarator HTS power plant,''')
edit('models/designs/stellarator_09/stellarator_plant.sysml','(the one source measuring through 20 K, Pierro et al. 2019, is paywalled and recorded as a queued research gap)','(Pierro et al. 2019 is now registered at knowledge/sources/measurements_of_the_strain_dependence_of_critical_current/; its availability does not replace this retained Senatore-based allowable or establish a design allowable at the operating point)')
edit('models/library/cost_structure/ife_cost_parameters.sysml','        a default value, Monte Carlo range (min/max), and Pearson\n        sensitivity coefficient from 10M-sample Monte Carlo analysis.','        a retained default value, Monte Carlo range (min/max), and Pearson\n        sensitivity coefficient. Hawker Table 2 defines the parameters;\n        Table 3 reports sampled ranges and correlations from the filtered\n        10M-sample experiment; section 3(b) supplies the single-parameter-scan\n        defaults. These correlations describe that experiment, not universal\n        derivatives. Sampling-space and runtime-input mappings are not\n        represented by this metadata bundle.')
edit('models/library/cost_structure/ife_cost_parameters.sysml','**Ref**: Table 1 (parameter definitions), Figure 3 (sensitivity)','**Ref**: Table 2 (definitions); Table 3 (sampled ranges and Pearson correlations); section 3(b) (scan defaults)')
edit('models/library/cost_structure/ife_cost_parameters.sysml','Source: Hawker 2020 Table 1, parameter','Source: Hawker 2020 Table 2 (definition), Table 3 (range/correlation), parameter')
edit('models/library/cost_structure/ife_cost_parameters.sysml','            Driver bank energy (total stored energy per shot).','            Energy incident on the target per shot (Hawker section 2, text after Eq. 2.15).\n            The retained identifier driver_energy follows the source Table 2\n            label; the sampled range is target energy, not stored bank energy.')
for family in FAMILIES.values():
    for name in family.owned:
        source=canonical_path(name);target=family.twin/name
        if source.read_bytes()!=target.read_bytes():target.write_bytes(source.read_bytes())
print('Corrected seven canonical documentation files and family twins')
