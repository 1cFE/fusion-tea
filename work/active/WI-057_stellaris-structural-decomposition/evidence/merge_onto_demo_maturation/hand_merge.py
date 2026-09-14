"""Apply feat/demo-maturation's remediation hunks (82c99091..2e9d7d81 on the two plant files) onto the
WI-057-restructured files from feat/model-viz, re-pointing referents to their WI-057 owners; write both trees."""
import sys
from pathlib import Path
SP = Path(sys.argv[1]); REPO = Path("/home/reid/1cfe/fusion-tea")
mv = {n: (SP / "mv" / n).read_text() for n in ("mfe_plant.sysml", "stellarator_plant.sysml", "mfe_subsystems.sysml", "mfe_power_core.sysml")}

def rep(text, old, new, count=1, label=""):
    n = text.count(old)
    assert n == count, f"{label}: expected {count} occurrence(s), found {n}: {old[:70]!r}"
    return text.replace(old, new)

# ------------------------------------------------------------------ mfe_plant.sysml
ps = mv["mfe_plant.sysml"]
# H1 plant doc
ps = rep(ps, "physics -> cost -> LCOE calc pipeline, and asserts the two viability\n        constraints. The MFE analogue of ife_plant's 'IFE Power Plant', one\n",
         "physics -> cost -> LCOE calc pipeline, and asserts power, heating,\n        magnet, primary-loop, cycle-domain and divertor viability constraints.\n        Instance-specific assertions extend these; the generated constraint\n        catalog records the executable set. The MFE analogue of ife_plant's 'IFE Power Plant', one\n", label="H1")
# H2 the coil's R0 rides with the plasma's R (remediation T-021; WI-057 puts R0 on 'Modular Coil', R on 'Plasma')
ps = rep(ps, "            :>> r_coil_centre = rb.r_coil_centre;\n        }\n",
         "            :>> r_coil_centre = rb.r_coil_centre;\n"
         "            // T-021 (2026-09-11): the coil's major radius rides with the plasma's. WI-057 owns R0 on\n"
         "            // 'Modular Coil' and R on 'Plasma', so the binding sits on the nested coil part.\n"
         "            part :>> coil {\n"
         "                :>> R0 = plasma.R {\n"
         "                    doc /*\n"
         "                    Major plasma/axis radius [m], owned by the plant's plasma part (WI-057; was the containing plant).\n"
         "\n"
         "                    Source: work/analysis/20260911-230953_radius-ownership-evidence/source-meaning.md\n"
         "                    Ref: ## Model and existing source interpretation; ## Assessment; revision 2f8856b7\n"
         "                    Basis: [INHERITED: T-021@2f8856b7] Existing model-intent interpretation: one shared plasma/axis scale. This does not equate real modular-coil surfaces; coil-bore and coil-centre minor radii remain distinct.\n"
         "                    Last Updated: 2026-09-11\n"
         "                    */\n"
         "                }\n"
         "            }\n"
         "        }\n", label="H2")
# H3 the operating-heat calc and the four heating-efficiency fences (WI-050), on the plant, reading the heating part's facts
ps = rep(ps, "        calc pb : 'MFE Power Balance Calc' {\n",
         "        // Generic legacy/direct behavior defaults to installed coupled capacity.\n"
         "        // A sustained concept overrides this exposed demand with its producer.\n"
         "        // (WI-050; the heating facts live on the heating part since WI-057.)\n"
         "        attribute p_operating_coupled_heat : Real default heating.p_coupled;\n"
         "        calc operating_heat : 'Operating Heating Power' {\n"
         "            in p_required_in = p_operating_coupled_heat;\n"
         "            in eta_source_in = heating.eta_source_heat;\n"
         "            in eta_couple_in = heating.eta_couple_heat;\n"
         "        }\n"
         "        assert constraint heating_source_positive_ok : 'Heating Efficiency Positive' {\n"
         "            in efficiency = heating.eta_source_heat;\n"
         "        }\n"
         "        assert constraint heating_source_upper_ok : 'Heating Efficiency Upper' {\n"
         "            in efficiency = heating.eta_source_heat;\n"
         "        }\n"
         "        assert constraint heating_couple_positive_ok : 'Heating Efficiency Positive' {\n"
         "            in efficiency = heating.eta_couple_heat;\n"
         "        }\n"
         "        assert constraint heating_couple_upper_ok : 'Heating Efficiency Upper' {\n"
         "            in efficiency = heating.eta_couple_heat;\n"
         "        }\n"
         "\n"
         "        calc pb : 'MFE Power Balance Calc' {\n", label="H3")
# H4 blanket and divertor read the OPERATING coupled power; the divertor also keeps the INSTALLED one (WI-050)
ps = rep(ps, "            :>> p_coupled = heating.p_coupled;\n", "            :>> p_coupled = operating_heat.p_coupled;   // WI-050: the operating demand\n", count=2, label="H4")
ps = rep(ps, "            :>> p_coupled = operating_heat.p_coupled;   // WI-050: the operating demand\n            :>> p_rad = plasma.p_rad;\n",
         "            :>> p_coupled = operating_heat.p_coupled;   // WI-050: the operating demand\n            :>> p_installed_coupled = heating.p_coupled;   // WI-050: the installed delivery\n            :>> p_rad = plasma.p_rad;\n", label="H4-div")
# H5 the power balance reads the operating heat
ps = rep(ps, "            in p_input_in = heating.p_coupled;\n            in mn_in = blanket.mn;\n", "            in p_input_in = operating_heat.p_coupled;\n            in mn_in = blanket.mn;\n", label="H5a")
ps = rep(ps, "            in p_wallplug_in = heating.p_wallplug_total;\n", "            in p_wallplug_in = operating_heat.p_wallplug;\n", label="H5b")
# H6 connection comments follow the rewiring
ps = rep(ps, "// heating.p_coupled: accounted at the blanket (source_heat.p_input_in), the divertor (divheat) and the balance (pb)",
         "// operating_heat.p_coupled (WI-050): accounted at the blanket (source_heat.p_input_in), the divertor (divheat) and the balance (pb)", label="H6a")
ps = rep(ps, "// pb.p_wallplug_in = heating.p_wallplug_total", "// pb.p_wallplug_in = operating_heat.p_wallplug (WI-050)", label="H6b")

# ------------------------------------------------------------------ mfe_subsystems.sysml
ss = mv["mfe_subsystems.sysml"]
ss = rep(ss, "        attribute p_coupled : Real;   // <- heating.p_coupled\n", "        attribute p_coupled : Real;   // <- operating_heat.p_coupled (WI-050: the operating demand)\n", label="S1")
ss = rep(ss, "        // Blanket (CAS22.1.1).\n        calc blanket_cost : 'Blanket Cost' {\n",
         "        // Blanket (CAS22.1.1).\n"
         "        // WI-050: retained power-scaled equipment costs are design-point sizing\n"
         "        // estimates, including blanket/shield/structure/vessel/supplies/divertor,\n"
         "        // turbine/electric/rejection/miscellaneous, buildings and CAS22 tail.\n"
         "        // Their operating-power operands are retained under the reviewed cost\n"
         "        // classification; heating procurement alone follows installed delivery.\n"
         "        calc blanket_cost : 'Blanket Cost' {\n", label="S2")

# ------------------------------------------------------------------ mfe_power_core.sysml (Divertor)
cs = mv["mfe_power_core.sysml"]
cs = rep(cs, "        attribute p_coupled : Real;   // <- heating.p_coupled\n        attribute p_rad : Real;   // <- plasma.p_rad\n",
         "        attribute p_coupled : Real;   // <- operating_heat.p_coupled (WI-050: the operating demand)\n        attribute p_installed_coupled : Real;   // <- heating.p_coupled (WI-050: the installed delivery)\n        attribute p_rad : Real;   // <- plasma.p_rad\n", label="P1a")
cs = rep(cs, "            in p_aux_required_in = p_aux_required;\n            in p_rad_core_in = p_rad;\n",
         "            in p_aux_required_in = p_aux_required;\n            in p_installed_coupled_in = p_installed_coupled;\n            in p_rad_core_in = p_rad;\n", label="P1b")

# ------------------------------------------------------------------ stellarator_plant.sysml
ts = mv["stellarator_plant.sysml"]
ts = rep(ts, "    part stellaris : 'MFE Power Plant' {\n        doc /*\n        Proxima Fusion \"Stellaris\"",
         "    part stellaris : 'MFE Power Plant' {\n        doc /*\n"
         "        SOURCE LOCATORS used throughout this definition:\n"
         "          stellaris-design-details.md =\n"
         "            knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md\n"
         "          images/ = knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/\n"
         "          raw.pdf / raw PDF / iter-02 raw PDF = the registered KIT witness,\n"
         "            knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf\n"
         "        Bare line references refer to the iter-01 text above; PDF pages and\n"
         "        sections refer to the KIT witness. Images/PDF govern quantitative\n"
         "        readings where extraction is garbled. Availability of these sources\n"
         "        does not establish unrecorded quantitative adoption.\n"
         "\n"
         "        Proxima Fusion \"Stellaris\"", label="I1")
ts = rep(ts, "                // Major radius [m]. Source: stellaris-design-details.md Table 2 /\n                //   line 251 (R ~= 12.7 m).\n                :>> R0 = 12.7;\n", "", label="I2")
ts = rep(ts, "        part :>> heating {\n            // Power-balance inputs.\n",
         "        // WI-050: the operating coupled-heating demand is the plasma's sustainment requirement\n"
         "        // (the generic plant's default is the installed coupled capacity).\n"
         "        :>> p_operating_coupled_heat = plasma.p_aux_required;\n"
         "\n"
         "        part :>> heating {\n            // Power-balance inputs.\n", label="I3")
ts = rep(ts, "(the one source measuring through 20 K, Pierro et al. 2019, is paywalled and recorded as a queued research gap) */",
         "(Pierro et al. 2019 is now registered at knowledge/sources/measurements_of_the_strain_dependence_of_critical_current/; its availability does not replace this retained Senatore-based allowable or establish a design allowable at the operating point) */", label="I4a")
ts = rep(ts, "work/active/WI-041_source-anchored-wall-load-fence/design.md", "work/completed/20260905_WI-041_source-anchored-wall-load-fence/design.md", label="I4b")

# ------------------------------------------------------------------ write both trees
targets = {
    "mfe_plant.sysml": ("models/designs/generic_mfe/mfe_plant.sysml", "exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml"),
    "stellarator_plant.sysml": ("models/designs/stellarator_09/stellarator_plant.sysml", "exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml"),
    "mfe_subsystems.sysml": ("models/designs/generic_mfe/mfe_subsystems.sysml", "exploration/stellarator_e2e/models/designs/generic_mfe/mfe_subsystems.sysml"),
    "mfe_power_core.sysml": ("models/library/cost_structure/mfe_power_core.sysml", "exploration/stellarator_e2e/models/cost_structure/mfe_power_core.sysml"),
}
out = {"mfe_plant.sysml": ps, "stellarator_plant.sysml": ts, "mfe_subsystems.sysml": ss, "mfe_power_core.sysml": cs}
for n, paths in targets.items():
    for p in paths: (REPO / p).write_text(out[n])
for f in (SP / "mv" / "structure").glob("*.sysml"):
    for d in ("models/library/structure", "exploration/stellarator_e2e/models/structure"):
        (REPO / d).mkdir(exist_ok=True); (REPO / d / f.name).write_text(f.read_text())
print("written: 4 files x 2 trees + 5 structure files x 2 trees")
