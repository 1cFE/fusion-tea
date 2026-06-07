VERDICT: FINDINGS

### F-1: C220108 override uses absolute M$ value instead of Class-U relative form
- **Target:** Section 5b (Override Candidates) and model_setup.py overrides list
- **Category:** analysis
- **Finding:** The C220108 (target factory) override is authored as the absolute value `100.0` in both analysis.md and model_setup.py, rather than the required Class-U relative form `M * generic.cas22_detail["C220108"]`. The rationale notes "~45% reduction from the library default" but never states the multiplier explicitly. For Class-U accounts, the authoring shape must anchor to `generic.cas22_detail["C2201xx"]` so the override's relationship to the library default is traceable. With the generic at $183.7M, the equivalent relative expression is approximately `0.545 * generic.cas22_detail["C220108"]`.
- **Recommendation:** Rewrite the value in both artifacts as `0.545 * generic.cas22_detail["C220108"]` (or whatever M the stated arithmetic supports) and add the multiplier derivation to the rationale. If the intent is purely an absolute anchor (because the generic is judged unreliable as a reference), state that explicitly and explain why the relative form is not used.
- **Priority:** important

### F-2: CAS80 framework limitation inflates 1 GWe headline LCOE by ~$35/MWh — magnitude not stated
- **Target:** Section 5b override commentary (CAS80 disabled override block)
- **Category:** analysis
- **Finding:** The analysis correctly discloses that CAS80 is disabled and carries a DT-scale fuel cost ($154.5M/yr native, $309M/yr at 1 GWe), but does not quantify the LCOE impact. At 1 GWe (8.76 TWh/yr), CAS80 contributes $309M / 8,760,000 MWh ≈ $35/MWh to the headline — inflating the reported 79.3 $/MWh by roughly 44%. Without this quantification, the 79.3 $/MWh headline is misleading: a reader sees a competitive LCOE figure that is actually a significant overstatement of the model's intent. The analysis should state the implied corrected headline (~$44/MWh) so the number can be interpreted correctly.
- **Recommendation:** Add one sentence to the CAS80 rationale block quantifying the per-MWh LCOE impact at 1 GWe (approximately $35/MWh) and stating the intended headline under the framework-limited override (~$44/MWh). This does not require a model change — the disclosure belongs in the analysis narrative alongside the existing framework limitation note.
- **Priority:** important

### F-3: Section 7 family delta does not connect driver cost assumptions to the 10x LCOE gap vs. Marvel
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The family delta correctly identifies driver architecture as the primary cost divergence from Marvel Fusion and honestly flags the comparison as "speculative — neither concept has a published driver cost." However, the two models are already making different implicit driver cost assumptions: HB11's C220104 runs at the library default ($288.4M/module × 2 modules = $576.8M at 1 GWe), while Marvel's analysis applied a $2B driver override over 10 modules. This assumption difference, compounded by HB11's higher P_native yielding fewer modules, produces the 10x LCOE gap (79.3 vs. 793.2 $/MWh) between two concepts sharing the same fuel, the same physics gap, and the same archetype-fit grade. Without naming this, the family delta lacks a TEA consequence for its most-discussed differentiator, and a reader comparing the two model outputs cannot understand why they diverge so sharply.
- **Recommendation:** Add a paragraph in Section 7 stating that the 10x LCOE divergence from Marvel is driven by (1) HB11's library-default driver cost vs. Marvel's $2B override and (2) HB11's higher P_native reducing module count, and flag that HB11's driver cost at library default is likely understated for a 30 PW CPA system with no commercial supply chain. Both LCOEs should be read as model illustrations rather than comparable estimates until driver costs are grounded.
- **Priority:** important
