---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts: spec.md
---

# Design

[AGENT] Keep the existing representative helium circuit, inputs, thirteen outputs and physical dependency order. Its heat source owns q_source; generic MFE binds loop_cp and loop_dT_blanket directly into the component. Flow feeds hydraulic loss, compressor work, electrical draw and recovered heat. loop_live multiplies final contributions and does not bypass evaluation. No additional producer needs a guard for these two inputs.

Use the established native manual-required output-only pattern. Preserve all equations in the canonical documentation and remove their executable output assignments; the typed completion retains the entering generated body after two finite-positive ValueError checks. This prevents generation from replacing the executable restriction with an unchecked auto body. Output order remains the generated thirteen-output ABI. The internal k_isen may remain documented rather than become a new output. Assertions alone do not raise on this runtime.

The inputs have independent meanings: cp is energy per unit mass per K; dT is outlet minus inlet K. MW times 10^6 converts source heat to J/s, and division by cp*dT gives kg/s. Both must be finite positive in this supported heating calculation even when q_source is zero. No empirical bound follows from the source's example. Source heat reconstructed as mdot*cp*dT/10^6 must agree; doubling either denominator operand halves mdot, quarters the fixed-reference pressure loss, and changes compressor work according to the existing chain. IHX heat minus source heat is recovered fluid work; electrical draw times drive efficiency is fluid work. Dormant delivered power retains its direct terms exactly.

Source inspection: primary PDF section 2.1.1 was rendered and visually inspected. It prints 300°C inlet, 500°C outlet, 2025.7 kg/s mass flow and 2101.7 MW blanket heat. Their implied cp is approximately 5187.59 J/(kg K), consistent with the current 5193 ideal-helium anchor at the document's rounded precision. Neither this example nor finiteness implies a broad operating-window certification.

The integration risk is established and local: a thirteenth normative seed changes the checked generator inventory. Current consumer helpers must use the new item helper and frozen receipt. Generate from a fresh empty package seeded only with checked normative bodies; compare exact package hashes, including documentation. Preserve prior twelve seed hashes. Recompute native snapshot, executable identity and current manifest; public 246-input/158-scalar identities and census must stay stable. Independent completion audit is required; no distinct unresolved architectural question warrants another design review.
