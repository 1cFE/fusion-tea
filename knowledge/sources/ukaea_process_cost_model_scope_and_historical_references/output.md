---
source: "https://ukaea.github.io/PROCESS/cost-models/cost-models/"
source_type: "url"
extracted_at: "2026-09-19T01:16:27.372468+00:00"
content_hash_sha256: "cfe4932f30d7a6d445a2d3cc89964f44761d7651a1c2762308a160f34abf8d00"
backend: "pandoc-fallback"
---

[Skip to content](#cost-models){.md-skip}

[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEyIDhhMyAzIDAgMCAwIDMtMyAzIDMgMCAwIDAtMy0zIDMgMyAwIDAgMC0zIDMgMyAzIDAgMCAwIDMgM20wIDMuNTRDOS42NCA5LjM1IDYuNSA4IDMgOHYxMWMzLjUgMCA2LjY0IDEuMzUgOSAzLjU0IDIuMzYtMi4xOSA1LjUtMy41NCA5LTMuNTRWOGMtMy41IDAtNi42NCAxLjM1LTkgMy41NCI+PC9wYXRoPjwvc3ZnPg==)](../.. "PROCESS"){.md-header__button .md-logo aria-label="PROCESS" md-component="logo"} ![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTMgNmgxOHYySDN6bTAgNWgxOHYySDN6bTAgNWgxOHYySDN6Ij48L3BhdGg+PC9zdmc+)

PROCESS

Cost Models

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTkuNSAzQTYuNSA2LjUgMCAwIDEgMTYgOS41YzAgMS42MS0uNTkgMy4wOS0xLjU2IDQuMjNsLjI3LjI3aC43OWw1IDUtMS41IDEuNS01LTV2LS43OWwtLjI3LS4yN0E2LjUyIDYuNTIgMCAwIDEgOS41IDE2IDYuNSA2LjUgMCAwIDEgMyA5LjUgNi41IDYuNSAwIDAgMSA5LjUgM20wIDJDNyA1IDUgNyA1IDkuNVM3IDE0IDkuNSAxNCAxNCAxMiAxNCA5LjUgMTIgNSA5LjUgNSI+PC9wYXRoPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTkuNSAzQTYuNSA2LjUgMCAwIDEgMTYgOS41YzAgMS42MS0uNTkgMy4wOS0xLjU2IDQuMjNsLjI3LjI3aC43OWw1IDUtMS41IDEuNS01LTV2LS43OWwtLjI3LS4yN0E2LjUyIDYuNTIgMCAwIDEgOS41IDE2IDYuNSA2LjUgMCAwIDEgMyA5LjUgNi41IDYuNSAwIDAgMSA5LjUgM20wIDJDNyA1IDUgNyA1IDkuNVM3IDE0IDkuNSAxNCAxNCAxMiAxNCA5LjUgMTIgNSA5LjUgNSI+PC9wYXRoPjwvc3ZnPg==) ![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDExdjJIOGw1LjUgNS41LTEuNDIgMS40Mkw0LjE2IDEybDcuOTItNy45MkwxMy41IDUuNSA4IDExeiI+PC9wYXRoPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTE5IDYuNDEgMTcuNTkgNSAxMiAxMC41OSA2LjQxIDUgNSA2LjQxIDEwLjU5IDEyIDUgMTcuNTkgNi40MSAxOSAxMiAxMy40MSAxNy41OSAxOSAxOSAxNy41OSAxMy40MSAxMnoiPjwvcGF0aD48L3N2Zz4=)

Initializing search

[](https://github.com/UKAEA/PROCESS "Go to repository"){.md-source md-component="source"}

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgNDQ4IDUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48IS0tISBGb250IEF3ZXNvbWUgRnJlZSA3LjEuMCBieSBAZm9udGF3ZXNvbWUgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbSBMaWNlbnNlIC0gaHR0cHM6Ly9mb250YXdlc29tZS5jb20vbGljZW5zZS9mcmVlIChJY29uczogQ0MgQlkgNC4wLCBGb250czogU0lMIE9GTCAxLjEsIENvZGU6IE1JVCBMaWNlbnNlKSBDb3B5cmlnaHQgMjAyNSBGb250aWNvbnMsIEluYy4tLT48cGF0aCBkPSJNNDM5LjYgMjM2LjEgMjQ0IDQwLjVjLTUuNC01LjUtMTIuOC04LjUtMjAuNC04LjVzLTE1IDMtMjAuNCA4LjRMMTYyLjUgODFsNTEuNSA1MS41YzI3LjEtOS4xIDUyLjcgMTYuOCA0My40IDQzLjdsNDkuNyA0OS43YzM0LjItMTEuOCA2MS4yIDMxIDM1LjUgNTYuNy0yNi41IDI2LjUtNzAuMi0yLjktNTYtMzcuM0wyNDAuMyAxOTl2MTIxLjljMjUuMyAxMi41IDIyLjMgNDEuOCA5LjEgNTUtNi40IDYuNC0xNS4yIDEwLjEtMjQuMyAxMC4xcy0xNy44LTMuNi0yNC4zLTEwLjFjLTE3LjYtMTcuNi0xMS4xLTQ2LjkgMTEuMi01NnYtMTIzYy0yMC44LTguNS0yNC42LTMwLjctMTguNi00NUwxNDIuNiAxMDEgOC41IDIzNS4xQzMgMjQwLjYgMCAyNDcuOSAwIDI1NS41czMgMTUgOC41IDIwLjRsMTk1LjYgMTk1LjdjNS40IDUuNCAxMi43IDguNCAyMC40IDguNHMxNS0zIDIwLjQtOC40bDE5NC43LTE5NC43YzUuNC01LjQgOC40LTEyLjggOC40LTIwLjRzLTMtMTUtOC40LTIwLjQiPjwvcGF0aD48L3N2Zz4=)

UKAEA/PROCESS

-   [Getting Started](../..){.md-tabs__link}
-   [Development](../../development/git-usage/){.md-tabs__link}
-   [Models](../../physics-models/plasma_overview/){.md-tabs__link}
-   [Publications](../../publications/){.md-tabs__link}
-   [Source Documentation](../../source/reference/process/core/caller/){.md-tabs__link}

[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEyIDhhMyAzIDAgMCAwIDMtMyAzIDMgMCAwIDAtMy0zIDMgMyAwIDAgMC0zIDMgMyAzIDAgMCAwIDMgM20wIDMuNTRDOS42NCA5LjM1IDYuNSA4IDMgOHYxMWMzLjUgMCA2LjY0IDEuMzUgOSAzLjU0IDIuMzYtMi4xOSA1LjUtMy41NCA5LTMuNTRWOGMtMy41IDAtNi42NCAxLjM1LTkgMy41NCI+PC9wYXRoPjwvc3ZnPg==)](../.. "PROCESS"){.md-nav__button .md-logo aria-label="PROCESS" md-component="logo"} PROCESS

[](https://github.com/UKAEA/PROCESS "Go to repository"){.md-source md-component="source"}

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgNDQ4IDUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48IS0tISBGb250IEF3ZXNvbWUgRnJlZSA3LjEuMCBieSBAZm9udGF3ZXNvbWUgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbSBMaWNlbnNlIC0gaHR0cHM6Ly9mb250YXdlc29tZS5jb20vbGljZW5zZS9mcmVlIChJY29uczogQ0MgQlkgNC4wLCBGb250czogU0lMIE9GTCAxLjEsIENvZGU6IE1JVCBMaWNlbnNlKSBDb3B5cmlnaHQgMjAyNSBGb250aWNvbnMsIEluYy4tLT48cGF0aCBkPSJNNDM5LjYgMjM2LjEgMjQ0IDQwLjVjLTUuNC01LjUtMTIuOC04LjUtMjAuNC04LjVzLTE1IDMtMjAuNCA4LjRMMTYyLjUgODFsNTEuNSA1MS41YzI3LjEtOS4xIDUyLjcgMTYuOCA0My40IDQzLjdsNDkuNyA0OS43YzM0LjItMTEuOCA2MS4yIDMxIDM1LjUgNTYuNy0yNi41IDI2LjUtNzAuMi0yLjktNTYtMzcuM0wyNDAuMyAxOTl2MTIxLjljMjUuMyAxMi41IDIyLjMgNDEuOCA5LjEgNTUtNi40IDYuNC0xNS4yIDEwLjEtMjQuMyAxMC4xcy0xNy44LTMuNi0yNC4zLTEwLjFjLTE3LjYtMTcuNi0xMS4xLTQ2LjkgMTEuMi01NnYtMTIzYy0yMC44LTguNS0yNC42LTMwLjctMTguNi00NUwxNDIuNiAxMDEgOC41IDIzNS4xQzMgMjQwLjYgMCAyNDcuOSAwIDI1NS41czMgMTUgOC41IDIwLjRsMTk1LjYgMTk1LjdjNS40IDUuNCAxMi43IDguNCAyMC40IDguNHMxNS0zIDIwLjQtOC40bDE5NC43LTE5NC43YzUuNC01LjQgOC40LTEyLjggOC40LTIwLjRzLTMtMTUtOC40LTIwLjQiPjwvcGF0aD48L3N2Zz4=)

UKAEA/PROCESS

-   [Getting Started](../..){.md-nav__link}
    Getting Started
    -   Installation
        Installation
        -   [Installation](../../installation/installation/){.md-nav__link}
        -   [Visual Studio Code](../../installation/vs-code/){.md-nav__link}
    -   Usage
        Usage
        -   [Running PROCESS](../../usage/running-process/){.md-nav__link}
        -   Examples
            Examples
            -   [Examples of running PROCESS](../../usage/examples/){.md-nav__link}
            -   [Introduction to running PROCESS](../../examples/introduction.ex/){.md-nav__link}
            -   [Optimum solutions comparison notebook](../../examples/optimum_solutions_comparison.ex/){.md-nav__link}
            -   [Running and visualising a PROCESS scan](../../examples/scan.ex/){.md-nav__link}
            -   [Evaluating a single PROCESS model](../../examples/single_model_evaluation.ex/){.md-nav__link}
            -   [Demonstration of VaryRun](../../examples/vary_run_example.ex/){.md-nav__link}
        -   [Troubleshooting](../../usage/troubleshooting/){.md-nav__link}
        -   [Plotting](../../usage/plotting/){.md-nav__link}
        -   [Tracking](../../tracking.html){.md-nav__link}
    -   I/O
        I/O
        -   [Input](../../io/input-guide/){.md-nav__link}
        -   [Output](../../io/output-guide/){.md-nav__link}
        -   [Python Libraries](../../io/python-lib-guide/){.md-nav__link}
        -   [Utilities](../../io/utilities/){.md-nav__link}
-   Development
    Development
    -   Git
        Git
        -   [Usage](../../development/git-usage/){.md-nav__link}
        -   [Pre-commit](../../development/pre-commit/){.md-nav__link}
        -   [Continuous Integration](../../development/ci-guide/){.md-nav__link}
        -   [Versioning](../../development/versioning/){.md-nav__link}
    -   Maintenance
        Maintenance
        -   [Testing](../../development/testing/){.md-nav__link}
        -   [Debugging](../../development/debugging/){.md-nav__link}
    -   Code modification
        Code modification
        -   [Adding Variables & Constraints](../../development/add-vars/){.md-nav__link}
        -   [Python Optimisation and Numba](../../development/numba/){.md-nav__link}
    -   Style
        Style
        -   [Standards](../../development/standards/){.md-nav__link}
-   Models
    Models
    -   Physics Models
        Physics Models
        -   Plasma
            Plasma
            -   [Overview](../../physics-models/plasma_overview/){.md-nav__link}
            -   [Geometry](../../physics-models/plasma_geometry/){.md-nav__link}
            -   Profiles
                Profiles
                -   [Overview](../../physics-models/profiles/plasma_profiles/){.md-nav__link}
                -   [Density Profile](../../physics-models/profiles/plasma_density_profile/){.md-nav__link}
                -   [Temperature Profile](../../physics-models/profiles/plasma_temperature_profile/){.md-nav__link}
                -   [Profile Base Class](../../physics-models/profiles/plasma_profiles_abstract_class/){.md-nav__link}
            -   Fusion Reactions
                Fusion Reactions
                -   [Overview](../../physics-models/fusion_reactions/plasma_reactions/){.md-nav__link}
                -   [Beam reactions](../../physics-models/fusion_reactions/beam_reactions/){.md-nav__link}
                -   [Bosch-Hale Methods](../../physics-models/fusion_reactions/plasma_bosch_hale/){.md-nav__link}
            -   [Magnetic Fields](../../physics-models/plasma_magnetic_fields/){.md-nav__link}
            -   Beta Limit
                Beta Limit
                -   [Overview](../../physics-models/plasma_beta/plasma_beta/){.md-nav__link}
                -   [Fast Alpha](../../physics-models/plasma_beta/plasma_alpha_beta_contribution/){.md-nav__link}
            -   [Density Limit](../../physics-models/plasma_density/){.md-nav__link}
            -   [Composition & Impurities](../../physics-models/plasma_composition/){.md-nav__link}
            -   [Radiation](../../physics-models/plasma_radiation/){.md-nav__link}
            -   Plasma Current
                Plasma Current
                -   [Overview](../../physics-models/plasma_current/plasma_current/){.md-nav__link}
                -   [Bootstrap Current](../../physics-models/plasma_current/bootstrap_current/){.md-nav__link}
                -   [Diamagnetic Current](../../physics-models/plasma_current/diamagnetic_current/){.md-nav__link}
                -   [Pfirsch-Schlüter Current](../../physics-models/plasma_current/pfirsch_schl%C3%BCter_current_drive/){.md-nav__link}
                -   Inductive Current
                    Inductive Current
                    -   [Inductive Current](../../physics-models/plasma_current/inductive_plasma_current/){.md-nav__link}
                    -   [Plasma Inductance](../../physics-models/plasma_current/plasma_inductance/){.md-nav__link}
                    -   [Plasma Resistive Heating](../../physics-models/plasma_current/plasma_resistive_heating/){.md-nav__link}
            -   [Confinement time](../../physics-models/plasma_confinement/){.md-nav__link}
            -   [L-H transition](../../physics-models/plasma_h_mode/){.md-nav__link}
            -   [Plasma Core Power Balance](../../physics-models/plasma_power_balance/){.md-nav__link}
            -   [Plasma Exhaust](../../physics-models/plasma_exhaust/){.md-nav__link}
            -   [Plasma Scrape-off Layer](../../physics-models/plasma_scrape_off_layer/){.md-nav__link}
            -   [Detailed Plasma Physics](../../physics-models/detailed_physics/){.md-nav__link}
        -   [Pulsed Plant Operation](../../physics-models/pulsed-plant/){.md-nav__link}
    -   Engineering Models
        Engineering Models
        -   [Machine Build](../../eng-models/machine-build/){.md-nav__link}
        -   [Structural Components](../../eng-models/structural-components/){.md-nav__link}
        -   [Buildings](../../eng-models/buildings/){.md-nav__link}
        -   First Wall/Blanket
            First Wall/Blanket
            -   [Overview](../../eng-models/fw-blanket/){.md-nav__link}
            -   Blanket
                Blanket
                -   [Overview](../../eng-models/blanket_overview/){.md-nav__link}
                -   [CCFE HCPB](../../eng-models/ccfe_hcpb/){.md-nav__link}
        -   TF Coil
            TF Coil
            -   [Overview](../../eng-models/tf-coil/){.md-nav__link}
            -   [Resistive TF Coil](../../eng-models/tf-coil-resistive/){.md-nav__link}
            -   [Superconducting TF Coil](../../eng-models/tf-coil-superconducting/){.md-nav__link}
        -   [PF Coil](../../eng-models/pf-coil/){.md-nav__link}
        -   [Superconductors](../../eng-models/superconductors/){.md-nav__link}
        -   [Central Solenoid](../../eng-models/central-solenoid/){.md-nav__link}
        -   [Shield](../../eng-models/shield/){.md-nav__link}
        -   [Divertor](../../eng-models/divertor/){.md-nav__link}
        -   [Heat transport](../../eng-models/power-conversion-and-heat-dissipation-systems/){.md-nav__link}
        -   Auxiliary Heating & Current Drive Systems
            Auxiliary Heating & Current Drive Systems
            -   [Overview](../../eng-models/heating_and_current_drive/heating-and-current-drive/){.md-nav__link}
            -   Radio Frequency
                Radio Frequency
                -   [Overview](../../eng-models/heating_and_current_drive/RF/rf_overview/){.md-nav__link}
                -   Lower Hybrid
                    Lower Hybrid
                    -   [Overview](../../eng-models/heating_and_current_drive/RF/lhcd_overview/){.md-nav__link}
                    -   [Fenstermacher Model](../../eng-models/heating_and_current_drive/RF/fenstermacher_lower_hybrid/){.md-nav__link}
                    -   [Ehst Model](../../eng-models/heating_and_current_drive/RF/ehst_lower_hybrid/){.md-nav__link}
                    -   [Culham Model](../../eng-models/heating_and_current_drive/RF/culham_lower_hybrid/){.md-nav__link}
                -   Electron Cyclotron
                    Electron Cyclotron
                    -   [Overview](../../eng-models/heating_and_current_drive/RF/ec_overview/){.md-nav__link}
                    -   [Fenstermacher Resonnance Model](../../eng-models/heating_and_current_drive/RF/fenstermacher_electron_cyclotron_resonance/){.md-nav__link}
                    -   [Culham Model](../../eng-models/heating_and_current_drive/RF/culham_electron_cyclotron/){.md-nav__link}
                    -   [User Input Gamma Model](../../eng-models/heating_and_current_drive/RF/ecrh_gamma/){.md-nav__link}
                    -   [Cutoff mode](../../eng-models/heating_and_current_drive/RF/cutoff_ecrh/){.md-nav__link}
                -   Ion Cyclotron
                    Ion Cyclotron
                    -   [Overview](../../eng-models/heating_and_current_drive/RF/ic_overview/){.md-nav__link}
                    -   [Ion cyclotron model](../../eng-models/heating_and_current_drive/RF/ic_model/){.md-nav__link}
                -   Electron Bernstein Wave
                    Electron Bernstein Wave
                    -   [Overview](../../eng-models/heating_and_current_drive/RF/ebw_overview/){.md-nav__link}
                    -   [EBW Model](../../eng-models/heating_and_current_drive/RF/ebw_freethy/){.md-nav__link}
            -   Neutral Beam Injection
                Neutral Beam Injection
                -   [Overview](../../eng-models/heating_and_current_drive/NBI/nbi_overview/){.md-nav__link}
                -   [ITER Model](../../eng-models/heating_and_current_drive/NBI/iter_nb/){.md-nav__link}
                -   [Culham Model](../../eng-models/heating_and_current_drive/NBI/culham_nb/){.md-nav__link}
        -   [Cryostat and vacuum system](../../eng-models/cryostat-and-vacuum-system/){.md-nav__link}
        -   [Plant Availability](../../eng-models/plant-availability/){.md-nav__link}
        -   [Power Requirements](../../eng-models/power-requirements/){.md-nav__link}
        -   [Vacuum Vessel](../../eng-models/vacuum-vessel/){.md-nav__link}
        -   Generic Engineering Methods
            Generic Engineering Methods
            -   [Pumping](../../eng-models/generic_methods/pumping/){.md-nav__link}
            -   [Materials](../../eng-models/generic_methods/materials/){.md-nav__link}
    -   Unique Models
        Unique Models
        -   [Water Use](../../unique-models/water_use/){.md-nav__link}
        -   [Power Plant Building Sizes](../../unique-models/buildings_sizes/){.md-nav__link}
        -   Cost Models [Cost Models](./){.md-nav__link .md-nav__link--active}
            Table of contents
            -   [1990 cost model (i_cost_model = 0)](#1990-cost-model-i_cost_model-0){.md-nav__link}
            -   [2015 Kovari model (i_cost_model = 1)](#2015-kovari-model-i_cost_model-1){.md-nav__link}
    -   Solver
        Solver
        -   [Solver Guide](../../solver/solver-guide/){.md-nav__link}
        -   [VMCON Optimisation Solver Explained](../../solver/optsolverdoc/){.md-nav__link}
        -   [Equation Solvers](../../solver/equation-solver/){.md-nav__link}
    -   Fusion Devices
        Fusion Devices
        -   [Spherical Tokamak](../../fusion-devices/spherical-tokamak/){.md-nav__link}
        -   [Stellarator Model](../../fusion-devices/stellarator/){.md-nav__link}
        -   [Inertial Fusion Energy Model](../../fusion-devices/inertial/){.md-nav__link}
-   [Publications](../../publications/){.md-nav__link}
-   Source Documentation
    Source Documentation
    -   process
        process
        -   core
            core
            -   [caller](../../source/reference/process/core/caller/){.md-nav__link}
            -   [constants](../../source/reference/process/core/constants/){.md-nav__link}
            -   [coolprop_interface](../../source/reference/process/core/coolprop_interface/){.md-nav__link}
            -   data_structure
                data_structure
                -   [base](../../source/reference/process/core/data_structure/base/){.md-nav__link}
                -   [dicts](../../source/reference/process/core/data_structure/dicts/){.md-nav__link}
                -   [obsolete_vars](../../source/reference/process/core/data_structure/obsolete_vars/){.md-nav__link}
                -   [variable_metadata](../../source/reference/process/core/data_structure/variable_metadata/){.md-nav__link}
            -   [exceptions](../../source/reference/process/core/exceptions/){.md-nav__link}
            -   [init](../../source/reference/process/core/init/){.md-nav__link}
            -   [input](../../source/reference/process/core/input/){.md-nav__link}
            -   io
                io
                -   [cli_tools](../../source/reference/process/core/io/cli_tools/){.md-nav__link}
                -   in_dat
                    in_dat
                    -   [base](../../source/reference/process/core/io/in_dat/base/){.md-nav__link}
                    -   [cli](../../source/reference/process/core/io/in_dat/cli/){.md-nav__link}
                    -   [create](../../source/reference/process/core/io/in_dat/create/){.md-nav__link}
                -   mfile
                    mfile
                    -   [base](../../source/reference/process/core/io/mfile/base/){.md-nav__link}
                    -   [cli](../../source/reference/process/core/io/mfile/cli/){.md-nav__link}
                    -   [comparison](../../source/reference/process/core/io/mfile/comparison/){.md-nav__link}
                -   plot
                    plot
                    -   [cli](../../source/reference/process/core/io/plot/cli/){.md-nav__link}
                    -   costs
                        costs
                        -   [cli](../../source/reference/process/core/io/plot/costs/cli/){.md-nav__link}
                        -   [costs_bar](../../source/reference/process/core/io/plot/costs/costs_bar/){.md-nav__link}
                        -   [costs_pie](../../source/reference/process/core/io/plot/costs/costs_pie/){.md-nav__link}
                    -   [sankey](../../source/reference/process/core/io/plot/sankey/){.md-nav__link}
                    -   [scans](../../source/reference/process/core/io/plot/scans/){.md-nav__link}
                    -   [solutions](../../source/reference/process/core/io/plot/solutions/){.md-nav__link}
                    -   [stress_tf](../../source/reference/process/core/io/plot/stress_tf/){.md-nav__link}
                    -   [summary](../../source/reference/process/core/io/plot/summary/){.md-nav__link}
                -   vary_run
                    vary_run
                    -   [config](../../source/reference/process/core/io/vary_run/config/){.md-nav__link}
                    -   [tools](../../source/reference/process/core/io/vary_run/tools/){.md-nav__link}
            -   [log](../../source/reference/process/core/log/){.md-nav__link}
            -   [model](../../source/reference/process/core/model/){.md-nav__link}
            -   [process_output](../../source/reference/process/core/process_output/){.md-nav__link}
            -   [repository](../../source/reference/process/core/repository/){.md-nav__link}
            -   [scan](../../source/reference/process/core/scan/){.md-nav__link}
            -   solver
                solver
                -   [constraints](../../source/reference/process/core/solver/constraints/){.md-nav__link}
                -   [evaluators](../../source/reference/process/core/solver/evaluators/){.md-nav__link}
                -   [iteration_variables](../../source/reference/process/core/solver/iteration_variables/){.md-nav__link}
                -   [objectives](../../source/reference/process/core/solver/objectives/){.md-nav__link}
                -   [solver](../../source/reference/process/core/solver/solver/){.md-nav__link}
                -   [solver_handler](../../source/reference/process/core/solver/solver_handler/){.md-nav__link}
        -   data_structure
            data_structure
            -   [blanket_variables](../../source/reference/process/data_structure/blanket_variables/){.md-nav__link}
            -   [build_variables](../../source/reference/process/data_structure/build_variables/){.md-nav__link}
            -   [buildings_variables](../../source/reference/process/data_structure/buildings_variables/){.md-nav__link}
            -   [ccfe_hcpb_variables](../../source/reference/process/data_structure/ccfe_hcpb_variables/){.md-nav__link}
            -   [constraint_variables](../../source/reference/process/data_structure/constraint_variables/){.md-nav__link}
            -   [cost_2015_variables](../../source/reference/process/data_structure/cost_2015_variables/){.md-nav__link}
            -   [cost_variables](../../source/reference/process/data_structure/cost_variables/){.md-nav__link}
            -   [cs_fatigue_variables](../../source/reference/process/data_structure/cs_fatigue_variables/){.md-nav__link}
            -   [current_drive_variables](../../source/reference/process/data_structure/current_drive_variables/){.md-nav__link}
            -   [dcll_variables](../../source/reference/process/data_structure/dcll_variables/){.md-nav__link}
            -   [divertor_variables](../../source/reference/process/data_structure/divertor_variables/){.md-nav__link}
            -   [first_wall_variables](../../source/reference/process/data_structure/first_wall_variables/){.md-nav__link}
            -   [fwbs_variables](../../source/reference/process/data_structure/fwbs_variables/){.md-nav__link}
            -   [global_variables](../../source/reference/process/data_structure/global_variables/){.md-nav__link}
            -   [heat_transport_variables](../../source/reference/process/data_structure/heat_transport_variables/){.md-nav__link}
            -   [ife_variables](../../source/reference/process/data_structure/ife_variables/){.md-nav__link}
            -   [impurity_radiation_variables](../../source/reference/process/data_structure/impurity_radiation_variables/){.md-nav__link}
            -   [neoclassics_variables](../../source/reference/process/data_structure/neoclassics_variables/){.md-nav__link}
            -   [numerics](../../source/reference/process/data_structure/numerics/){.md-nav__link}
            -   [pf_power_variables](../../source/reference/process/data_structure/pf_power_variables/){.md-nav__link}
            -   [pfcoil_variables](../../source/reference/process/data_structure/pfcoil_variables/){.md-nav__link}
            -   [physics_variables](../../source/reference/process/data_structure/physics_variables/){.md-nav__link}
            -   [power_variables](../../source/reference/process/data_structure/power_variables/){.md-nav__link}
            -   [primary_pumping_variables](../../source/reference/process/data_structure/primary_pumping_variables/){.md-nav__link}
            -   [pulse_variables](../../source/reference/process/data_structure/pulse_variables/){.md-nav__link}
            -   [rebco_variables](../../source/reference/process/data_structure/rebco_variables/){.md-nav__link}
            -   [reinke_variables](../../source/reference/process/data_structure/reinke_variables/){.md-nav__link}
            -   [scan_variables](../../source/reference/process/data_structure/scan_variables/){.md-nav__link}
            -   [stellarator_configuration](../../source/reference/process/data_structure/stellarator_configuration/){.md-nav__link}
            -   [stellarator_variables](../../source/reference/process/data_structure/stellarator_variables/){.md-nav__link}
            -   [structure_variables](../../source/reference/process/data_structure/structure_variables/){.md-nav__link}
            -   [superconducting_tf_coil_variables](../../source/reference/process/data_structure/superconducting_tf_coil_variables/){.md-nav__link}
            -   [tfcoil_variables](../../source/reference/process/data_structure/tfcoil_variables/){.md-nav__link}
            -   [times_variables](../../source/reference/process/data_structure/times_variables/){.md-nav__link}
            -   [vacuum_variables](../../source/reference/process/data_structure/vacuum_variables/){.md-nav__link}
            -   [water_usage_variables](../../source/reference/process/data_structure/water_usage_variables/){.md-nav__link}
        -   [main](../../source/reference/process/main/){.md-nav__link}
        -   models
            models
            -   [availability](../../source/reference/process/models/availability/){.md-nav__link}
            -   blankets
                blankets
                -   [blanket_library](../../source/reference/process/models/blankets/blanket_library/){.md-nav__link}
                -   [dcll](../../source/reference/process/models/blankets/dcll/){.md-nav__link}
                -   [hcpb](../../source/reference/process/models/blankets/hcpb/){.md-nav__link}
            -   [build](../../source/reference/process/models/build/){.md-nav__link}
            -   [buildings](../../source/reference/process/models/buildings/){.md-nav__link}
            -   costs
                costs
                -   [costs](../../source/reference/process/models/costs/costs/){.md-nav__link}
                -   [costs_2015](../../source/reference/process/models/costs/costs_2015/){.md-nav__link}
            -   [cryostat](../../source/reference/process/models/cryostat/){.md-nav__link}
            -   [cs_fatigue](../../source/reference/process/models/cs_fatigue/){.md-nav__link}
            -   [divertor](../../source/reference/process/models/divertor/){.md-nav__link}
            -   engineering
                engineering
                -   [ivc_functions](../../source/reference/process/models/engineering/ivc_functions/){.md-nav__link}
                -   [materials](../../source/reference/process/models/engineering/materials/){.md-nav__link}
                -   [pumping](../../source/reference/process/models/engineering/pumping/){.md-nav__link}
            -   [fw](../../source/reference/process/models/fw/){.md-nav__link}
            -   geometry
                geometry
                -   [blanket](../../source/reference/process/models/geometry/blanket/){.md-nav__link}
                -   [cryostat](../../source/reference/process/models/geometry/cryostat/){.md-nav__link}
                -   [firstwall](../../source/reference/process/models/geometry/firstwall/){.md-nav__link}
                -   [parameterisations](../../source/reference/process/models/geometry/parameterisations/){.md-nav__link}
                -   [pfcoil](../../source/reference/process/models/geometry/pfcoil/){.md-nav__link}
                -   [plasma](../../source/reference/process/models/geometry/plasma/){.md-nav__link}
                -   [shield](../../source/reference/process/models/geometry/shield/){.md-nav__link}
                -   [tfcoil](../../source/reference/process/models/geometry/tfcoil/){.md-nav__link}
                -   [utils](../../source/reference/process/models/geometry/utils/){.md-nav__link}
                -   [vacuum_vessel](../../source/reference/process/models/geometry/vacuum_vessel/){.md-nav__link}
            -   [ife](../../source/reference/process/models/ife/){.md-nav__link}
            -   [pfcoil](../../source/reference/process/models/pfcoil/){.md-nav__link}
            -   physics
                physics
                -   [bootstrap_current](../../source/reference/process/models/physics/bootstrap_current/){.md-nav__link}
                -   [confinement_time](../../source/reference/process/models/physics/confinement_time/){.md-nav__link}
                -   [current_drive](../../source/reference/process/models/physics/current_drive/){.md-nav__link}
                -   [density_limit](../../source/reference/process/models/physics/density_limit/){.md-nav__link}
                -   [exhaust](../../source/reference/process/models/physics/exhaust/){.md-nav__link}
                -   [fusion_reactions](../../source/reference/process/models/physics/fusion_reactions/){.md-nav__link}
                -   [impurity_radiation](../../source/reference/process/models/physics/impurity_radiation/){.md-nav__link}
                -   [l_h_transition](../../source/reference/process/models/physics/l_h_transition/){.md-nav__link}
                -   [physics](../../source/reference/process/models/physics/physics/){.md-nav__link}
                -   [plasma_current](../../source/reference/process/models/physics/plasma_current/){.md-nav__link}
                -   [plasma_fields](../../source/reference/process/models/physics/plasma_fields/){.md-nav__link}
                -   [plasma_geometry](../../source/reference/process/models/physics/plasma_geometry/){.md-nav__link}
                -   [plasma_profiles](../../source/reference/process/models/physics/plasma_profiles/){.md-nav__link}
                -   [profiles](../../source/reference/process/models/physics/profiles/){.md-nav__link}
                -   [radiation_power](../../source/reference/process/models/physics/radiation_power/){.md-nav__link}
                -   [scrape_off_layer](../../source/reference/process/models/physics/scrape_off_layer/){.md-nav__link}
            -   [power](../../source/reference/process/models/power/){.md-nav__link}
            -   [pulse](../../source/reference/process/models/pulse/){.md-nav__link}
            -   [shield](../../source/reference/process/models/shield/){.md-nav__link}
            -   stellarator
                stellarator
                -   [build](../../source/reference/process/models/stellarator/build/){.md-nav__link}
                -   coils
                    coils
                    -   [calculate](../../source/reference/process/models/stellarator/coils/calculate/){.md-nav__link}
                    -   [coils](../../source/reference/process/models/stellarator/coils/coils/){.md-nav__link}
                    -   [forces](../../source/reference/process/models/stellarator/coils/forces/){.md-nav__link}
                    -   [mass](../../source/reference/process/models/stellarator/coils/mass/){.md-nav__link}
                    -   [output](../../source/reference/process/models/stellarator/coils/output/){.md-nav__link}
                    -   [quench](../../source/reference/process/models/stellarator/coils/quench/){.md-nav__link}
                -   [density_limits](../../source/reference/process/models/stellarator/density_limits/){.md-nav__link}
                -   [divertor](../../source/reference/process/models/stellarator/divertor/){.md-nav__link}
                -   [heating](../../source/reference/process/models/stellarator/heating/){.md-nav__link}
                -   [initialization](../../source/reference/process/models/stellarator/initialization/){.md-nav__link}
                -   [neoclassics](../../source/reference/process/models/stellarator/neoclassics/){.md-nav__link}
                -   [preset_config](../../source/reference/process/models/stellarator/preset_config/){.md-nav__link}
                -   [stellarator](../../source/reference/process/models/stellarator/stellarator/){.md-nav__link}
            -   [structure](../../source/reference/process/models/structure/){.md-nav__link}
            -   [superconductors](../../source/reference/process/models/superconductors/){.md-nav__link}
            -   tfcoil
                tfcoil
                -   [base](../../source/reference/process/models/tfcoil/base/){.md-nav__link}
                -   [quench](../../source/reference/process/models/tfcoil/quench/){.md-nav__link}
                -   [resistive](../../source/reference/process/models/tfcoil/resistive/){.md-nav__link}
                -   [superconducting](../../source/reference/process/models/tfcoil/superconducting/){.md-nav__link}
            -   [vacuum](../../source/reference/process/models/vacuum/){.md-nav__link}
            -   [water_use](../../source/reference/process/models/water_use/){.md-nav__link}

Table of contents

-   [1990 cost model (i_cost_model = 0)](#1990-cost-model-i_cost_model-0){.md-nav__link}
-   [2015 Kovari model (i_cost_model = 1)](#2015-kovari-model-i_cost_model-1){.md-nav__link}

# Cost Models

Two cost models are available, determined by the switch `i_cost_model`.

## 1990 cost model (`i_cost_model = 0`)

This combines methods^[1](#fn:1){.footnote-ref}^ used in the TETRA code ^[2](#fn:2){.footnote-ref}^ and the Generomak^[3](#fn:3){.footnote-ref}^ scheme. The costs are split into accounting categories^[4](#fn:4){.footnote-ref}^. The best references for the algorithms used are^[5](#fn:5){.footnote-ref}^, and source file `costs.f90` in the code itself. The majority of the costed items have a unit cost associated with them. These values scale with (for example) power output, volume, component mass etc., and many are available to be changed via the input file. All costs and their algorithms correspond to 1990 dollars.

The unit costs of the components of the fusion power core are relevant to \"first-of-a-kind\" items. That is to say, the items are assumed to be relatively expensive to build as they are effectively prototypes and specialised tools and machines have perhaps been made specially to create them. However, if a \"production line\" has been set up, and R & D progress has allowed more experience to be gained in constructing the power core components, the cost will be reduced as a result. Variable `fkind` may be used to multiply the raw unit costs of the fusion power core items (by a factor less than one) to simulate this cost reduction for an *N^th^*-of-a-kind device. In other systems studies of fusion power plants^[6](#fn:6){.footnote-ref}^, values for this multiplier have ranged from 0.5 to 0.8.

Many of the unit costs have four possible choices, relating to the level of safety assurance^[7](#fn:7){.footnote-ref}^ flag `lsa`. A value `lsa = 1` corresponds to a plant with a full safety credit (i.e. is truly passively safe). Levels 2 and 3 lie between the two extremes, and level 4 corresponds to a present day fission reactor, with no safety credit.

The first wall, blanket, divertor, centrepost (if present) and current drive system have relatively short lifetimes because of their hostile environment, after which they must be replaced. Because of this frequent renewal they can be regarded as though they are \"fuel\" items, and be costed accordingly. Switch `ifueltyp` is used to control whether this option is used in the code. If `ifueltyp = 1`, the costs of the first wall, blanket, divertor and a fraction `fcdfuel` of the cost of the current drive system are treated as fuel costs. If `ifueltyp = 0`, these are treated as capital costs.

If the switch `ireactor = 0`, no cost of electricity calculation is performed. If `ireactor = 1`, then the cost of electricity is evaluated, with the value quoted in units of \$/MWh.

The net electric power is calculated in routine `POWER` It is possible that the net electric power can become negative due to a high recirculating power. Switch `ipnet` determines whether the net electric power is scaled to always remain positive (`ipnet = 0`, or whether it is allowed to become negative (`ipnet = 1`), in which case no cost of electricity calculation is performed.

## 2015 Kovari model (`i_cost_model = 1`)

This model^[8](#fn:8){.footnote-ref}^ provides only capital cost, and it is not currently suitable for estimating the cost of electricity. *N^th^*-of-a-kind factors, level of safety assurance factors, and blanket replacement costs are not included. The mean electric output is calculated using the capacity factor, which takes account of the availability and the dwell time for a pulsed reactor. The capital cost divided by the mean electric output is a useful comparison parameter.

------------------------------------------------------------------------

1.  ::: {#fn:1}
    R. L. Reid and Y-K. M. Peng, *\"Potential Minimum Cost of Electricity of Superconducting Coil Tokamak Power Reactors\"*, Proceedings of 13^th^ IEEE Symposium on Fusion Engineering, Knoxville, Tennessee, October 1989, p. 258 [↩](#fnref:1 "Jump back to footnote 1 in the text"){.footnote-backref}
    :::

2.  ::: {#fn:2}
    R. L. Reid et al., *\"ETR/ITER Systems Code\"*, Oak Ridge Report ORNL/FEDC-87/7 (1988) [↩](#fnref:2 "Jump back to footnote 2 in the text"){.footnote-backref}
    :::

3.  ::: {#fn:3}
    J. Sheeld et al., *\"Cost Assessment of a Generic Magnetic Fusion Reactor\"*, Fusion Technology **9** (1986) 199 [↩](#fnref:3 "Jump back to footnote 3 in the text"){.footnote-backref}
    :::

4.  ::: {#fn:4}
    S. Thompson, *\"Systems Code Cost Accounting\"*, memo FEDC-M-88-SE,-004 (1988) [↩](#fnref:4 "Jump back to footnote 4 in the text"){.footnote-backref}
    :::

5.  ::: {#fn:5}
    J. D. Galambos, *\"STAR Code : Spherical Tokamak Analysis and Reactor Code\"*, Unpublished internal Oak Ridge document. A copy exists in the `PROCESS` Project Work File ^[9](#fn:9){.footnote-ref}^. [↩](#fnref:5 "Jump back to footnote 5 in the text"){.footnote-backref}
    :::

6.  ::: {#fn:6}
    J. D. Galambos, L. J. Perkins, S. W. Haney and J. Mandrekas, *Nuclear Fusion*, **35** (1995) 551 [↩](#fnref:6 "Jump back to footnote 6 in the text"){.footnote-backref}
    :::

7.  ::: {#fn:7}
    J. P. Holdren et al., *\"Report of the Senior Committee on Environmental Safety and Economic Aspects of Magnetic Fusion Energy\"*, Fusion Technology, **13** (1988) 7 [↩](#fnref:7 "Jump back to footnote 7 in the text"){.footnote-backref}
    :::

8.  ::: {#fn:8}
    M. Kovari et al., *\"The cost of a fusion power plant: extrapolation from ITER\"*, in preparation (2015) [↩](#fnref:8 "Jump back to footnote 8 in the text"){.footnote-backref}
    :::

9.  ::: {#fn:9}
    P. J. Knight, *\"PROCESS Reactor Systems Code\"*, AEA Fusion Project Work File, F/RS/CIRE5523/PWF (1992) [↩](#fnref:9 "Jump back to footnote 9 in the text"){.footnote-backref}
    :::

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIxIDEzLjFjLS4xIDAtLjMuMS0uNC4ybC0xIDEgMi4xIDIuMSAxLTFjLjItLjIuMi0uNiAwLS44bC0xLjMtMS4zYy0uMS0uMS0uMi0uMi0uNC0uMm0tMS45IDEuOC02LjEgNlYyM2gyLjFsNi4xLTYuMXpNMTIuNSA3djUuMmw0IDIuNC0xIDFMMTEgMTNWN3pNMTEgMjEuOWMtNS4xLS41LTktNC44LTktOS45QzIgNi41IDYuNSAyIDEyIDJjNS4zIDAgOS42IDQuMSAxMCA5LjMtLjMtLjEtLjYtLjItMS0uMnMtLjcuMS0xIC4yQzE5LjYgNy4yIDE2LjIgNCAxMiA0Yy00LjQgMC04IDMuNi04IDggMCA0LjEgMy4xIDcuNSA3LjEgNy45bC0uMS4yeiI+PC9wYXRoPjwvc3ZnPg==) July 28, 2026 ![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTE0LjQ3IDE1LjA4IDExIDEzVjdoMS41djUuMjVsMy4wOCAxLjgzYy0uNDEuMjgtLjc5LjYyLTEuMTEgMW0tMS4zOSA0Ljg0Yy0uMzYuMDUtLjcxLjA4LTEuMDguMDgtNC40MiAwLTgtMy41OC04LThzMy41OC04IDgtOCA4IDMuNTggOCA4YzAgLjM3LS4wMy43Mi0uMDggMS4wOC42OS4xIDEuMzMuMzIgMS45Mi42NC4xLS41Ni4xNi0xLjEzLjE2LTEuNzIgMC01LjUtNC41LTEwLTEwLTEwUzIgNi41IDIgMTJzNC40NyAxMCAxMCAxMGMuNTkgMCAxLjE2LS4wNiAxLjcyLS4xNi0uMzItLjU5LS41NC0xLjIzLS42NC0xLjkyTTE4IDE1djNoLTN2MmgzdjNoMnYtM2gzdi0yaC0zdi0zeiI+PC9wYXRoPjwvc3ZnPg==) July 20, 2023

[](../../unique-models/buildings_sizes/){.md-footer__link .md-footer__link--prev aria-label="Previous: Power Plant Building Sizes"}

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDExdjJIOGw1LjUgNS41LTEuNDIgMS40Mkw0LjE2IDEybDcuOTItNy45MkwxMy41IDUuNSA4IDExeiI+PC9wYXRoPjwvc3ZnPg==)

Previous

Power Plant Building Sizes

[](../../solver/solver-guide/){.md-footer__link .md-footer__link--next aria-label="Next: Solver Guide"}

Next

Solver Guide

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTQgMTF2MmgxMmwtNS41IDUuNSAxLjQyIDEuNDJMMTkuODQgMTJsLTcuOTItNy45MkwxMC41IDUuNSAxNiAxMXoiPjwvcGF0aD48L3N2Zz4=)

Copyright © 2023 United Kingdom Atomic Energy Authority

Made with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/){rel="noopener" target="_blank"}
