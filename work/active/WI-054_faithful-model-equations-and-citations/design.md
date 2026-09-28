---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts: spec.md
---

# Documentation impact and verification design

[AGENT] Keep the existing physical components, ownership, behavior and analysis graph. This item changes their explanations: Plasma Sustainment supplies radiation power to heating balance; Plasma Geometry supplies volume; Economic Parameter holds disconnected IFE metadata; Magnet Capital aggregates winding/structure accounts; the generic MFE plant owns generic assertions and Stellaris owns instance-specific inputs/assertions. Their connections and operating domains remain unchanged.

The bremsstrahlung coefficient is 5.35e-37 W m^3 keV^-1/2 (`/home/reid/1cfe/1costingfe/src/costingfe/layers/radiation.py:260,275`, pin 0254385); tungsten cooling is W m^3 (`:79-96`). With n_e in m^-3, T_e in keV, V in m^3, and dV' = dV/V = 2 rho d rho, both integrated products yield W. Multiply each by 1e-6 MW/W. Preserve the current piecewise cooling fit and profile approximations. A constant 4 keV, 1e20 m^-3 plasma with V=100 m^3, Z_eff=1 and f_W=1e-5 gives 1.07 MW bremsstrahlung and 5 MW line radiation; analytic integration of a nonuniform density profile tests the normalized measure independently.

The archived WI-006 spec MR-WI006-1 covers metadata, WI-035 design D6 and risks cover capital rollup/reference redefinitions, and WI-041 D1 covers the dormant additive calibration term. Update these exact references. A source legend in the Stellaris definition resolves existing relative shorthand to its exact text, image directory and registered raw PDF. Its old locators retain their meanings. This avoids pretending a line in one extraction is a line in another. Pierro registration does not replace the held Senatore-based 0.004 allowance.

Hawker's extraction headings and source narrative identify Tables 2/3 and section 3(b). Existing numerical metadata remains frozen. Source images must support any fresh quantitative transcription claim; missing original table representations remain explicit. The default/range/sensitivity roles must be separated even where no numbers change. The target-energy wording overlaps F18 but does not implement a metadata-to-runtime mapping or sampling semantics.

No new language capability or architecture is introduced, so a prototype or independent design critic would not address a material design uncertainty. Check source representations, then compare comment-stripped SysML and generated Python executable ASTs, exact public contracts, native outputs and source-family coherence. Regeneration can change document-bearing package identity. Capture entering package hashes, produce a new receipt and current metadata, and report any historical-receipt consumer failure for separately owned repair. Reuse WI-053 audited baseline/validation scope only where current identity supports it. Do not invoke historical metadata helpers against their evidence directories.
