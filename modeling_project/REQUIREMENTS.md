# Modeling Requirements

Project-specific rules that all modeling work must follow. These extend the standard rules in [MODELING_GUIDE.md](MODELING_GUIDE.md) with rules discovered through this project's goals and domain knowledge.

> This file replaces the former LOCAL_GUIDE.md. LOCAL_GUIDE.md contained only template placeholders — no project-specific rules had been recorded there. The requirements below are extracted from research findings, implemented patterns, and work item specs.

## Requirements

| ID | Requirement | Source | Enforcement | Validation Method |
|----|-------------|--------|-------------|-------------------|
| PR-001 | All costed components SHALL specialize 'Costed Component' interface with capital_cost, raw_material_cost, fabrication_cost, installation_cost, idiot_index | DI-003 | Design review + future validation rule | AST check: part specializes 'Costed Component' and has required attributes |
| PR-002 | Calc defs SHALL cite source file:line in doc comment (Source and Reference fields) | DI-014 | Validation Level 6 | Doc comment parser checks for Source/Reference fields |
| PR-003 | Library definitions SHALL be concept-agnostic (no reactor-type-specific values in library/) | AD-002 | Design review | Grep library/ for design-specific parameter values |
| PR-004 | Enum values SHALL match PyFECONS naming exactly (e.g., ReactorType::MFE, FuelType::DT) | DI-010 | Test assertions | test_reactor_type_variants, test_all_expected_enums_exist |
| PR-005 | Material definitions SHALL include density, thermal_conductivity, and unit_cost attributes | DI-007 | Test assertions | test_all_materials_have_required_attributes |
| PR-006 | Cost rollup for multiplied parts SHALL use NumericalFunctions::sum with array notation | DI-004 | Design review | Pattern check: sum(parts[N].cost) syntax |
| PR-007 | Power balance calc defs SHALL be validated against PyFECONS numerical outputs within stated tolerance | DI-002 | Regression tests | TestNumericalValidation test class |
