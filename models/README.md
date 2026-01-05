# SysML v2 Models

This directory contains SysML v2 textual models for fusion power plant techno-economic analysis.

## Structure

- `library/` - Reusable definitions
  - Part definitions (components, subsystems)
  - Calculation definitions (cost formulas, physics equations)
  - Material properties

- `designs/` - Specific fusion concept designs
  - CATF (Compact Advanced Tokamak Fusion)
  - Future: Stellarator, mirror machines, novel concepts

## Getting Started

Use `/design-model {feature}` to start creating models.

## Validation

Models are validated against PyFECONS calculations. Use `/audit-models` to check alignment.
