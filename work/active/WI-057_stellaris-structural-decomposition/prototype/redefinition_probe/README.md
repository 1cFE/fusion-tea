# Redefinition probe — how does a variant definition replace a template calc?

Six one-file models, each parsed with syside and (e, f) generated with `sysml-codegen`. Base: `part def Magnet` owning a template calc `structure_cost : BaseCost` and an EXPOSE `cost`; `part def VarMagnet :> Magnet`; a plant reading `magnet.cost`; an instance retyping `part :>> magnet : VarMagnet`.

| Variant | What the subtype writes | Result |
|---|---|---|
| a | `calc :>> structure_cost : VarCost { in f = f_markup; }` | refused — `feature-value-overriding: Cannot override a binding feature value` |
| b | `calc :>> structure_cost : VarCost { :>> f = f_markup; }` | refused — `redefinition-direction-conformance` |
| c | `calc :>> structure_cost : VarCost { in f : Real = f_markup; }` | refused — `feature-value-overriding` |
| d | a new calc plus `:>> cost = structure_cost_ni.cost;` against a base `attribute cost : Real = structure_cost.cost;` | refused — `feature-value-overriding` (the base EXPOSE is a binding) |
| e | base `attribute cost : Real default structure_cost.cost;`; subtype adds `calc structure_cost_ni : VarCost {…}` and `:>> cost = structure_cost_ni.cost;`; instance retyped | parses; generates; the plant's `total_calc.c` reads `…magnet__structure_cost_ni__cost` (`variant_e_wiring.txt`) |
| f | the same base, instance not retyped | parses; generates; `total_calc.c` reads `…magnet__structure_cost__cost` (`variant_f_wiring.txt`) |

Rule: a value bound with `=` in a definition is final — no subtype can re-bind a template calc's formals or a bound EXPOSE, and a redefining calc usage matches parameters positionally, so it cannot add one either. The overridable value in SysML v2 is `default`. A **swap seam** is therefore an EXPOSE declared `default <producer>.<output>` on the base definition; a variant definition adds its own calc and rebinds the seam with `:>>`; codegen routes every downstream consumer to whichever producer the seam names in that instance. Stage E applied this to the real magnet (`../README.md`).
