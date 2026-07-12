# exp() mini-spike — findings

**Date**: 2026-07-05 · **Timebox**: half day (came in well under)
**Claim under test** (last untested pipeline claim): calc defs using functions outside the mechanical arithmetic envelope (`+ - * / **`) survive the pipeline via the AI implementation pass.

**Verdict: the claim is now tested and holds** — with one important reframing of *how* out-of-envelope math gets spelled, and two new codegen findings in the expression pretty-printer.

## 1. Syntax verdict — what SysML spelling works

**There is no `exp`, `ln`, or `log` anywhere in the KerML/SysML v2 standard library.** Verified two ways:

- Empirically: probes at `probes/probe_a_bare_exp.sysml` (bare `exp(x)`), `probe_b_realfunctions.sysml` (`private import RealFunctions::*;` then `exp`/`ln`), `probe_c_qualified.sysml` (`RealFunctions::exp(x)`) all fail `syside check` with `reference-error: No Type named 'exp' found`. The `RealFunctions` import itself resolves fine — the package exists, the functions don't.
- Against the shipped library and spec: syside 0.8.3's `sysml.library/Kernel Libraries/Kernel Function Library/RealFunctions.kerml` has only `abs sqrt floor round max min sum product re im arg` + conversions + operators. `TrigFunctions.kerml` is sin/cos/tan/cot/arc* + deg/rad/pi. The spec's function-library sections (9.4) have zero hits for exp/ln/log. No `%` on Real either.

**What works instead — the spelling this spike used**: declare an *uninterpreted* user calc def and invoke it inline:

```sysml
calc def Exp { in attribute x : Real; out attribute y : Real; }   // no body
...
out attribute sigma_v : Real = c_coeff * Exp(-b_gamow / t_kev ** (1.0/3.0)) / t_kev ** (2.0/3.0);
```

This parses and passes `syside check` clean (`models/exp_toy.sysml`, Level 1 PASS). The bodiless calc def is the model-side declaration; the Python body is the AI pass's job. That is exactly the out-of-envelope shape.

**Side finding**: e^x specifically has an in-envelope spelling — `2.718281828459045 ** x` — which codegen auto-implements mechanically (confirmed, see §2). So a Bosch-Hale fit *could* stay fully mechanical. ln/log cannot: there is no operator-based workaround for logarithms.

## 2. Extraction/generation verdict — what the extractor does with `Exp(...)`

Live syside extraction + `sysml-codegen generate` ran clean, no crash. The compiler's classification did exactly the right thing (generation log):

| Calc def | Body | Classification | Result |
|---|---|---|---|
| `BoschHaleReactivity` | inline `Exp(...)` | `manual_required` | module + NotImplementedError stencil + backlog row |
| `GainDoublings` | inline `Ln(...)` ×2 | `manual_required` | module + stencil + backlog row |
| `ExpControl` (control) | `2.718... ** x` | `fully_compilable` | `AUTO_IMPLEMENTED = True`, body `return (2.718281828459045 ** inputs.exponent_arg)` — literal intact (`generated/handwritten/exp_toy/expcontrol_impl.py:18,54`) |
| `Exp`, `Ln` (bodiless) | — | skipped ("no expressions") | no module generated — they exist only as names inside other expressions, which is the correct treatment |

So the unknown-function expression is **passed through, not translated, not dropped**: the invocation survives by name into the module docstring and stencil ("`sigma_v = c_coeff * Exp(-(b_gamow) / ...`"), the stencil raises NotImplementedError with an exact SysML `file:line` pointer, and `IMPLEMENTATION_BACKLOG.md` lists both functions with complexity ratings.

**Two new codegen findings — the docstring expression renderer is lossy** (display-only; the compiled path is unaffected):

1. **Literal values are dropped.** Every numeric literal renders as `LiteralRationalEvaluation()` — e.g. `t_kev ** LiteralRationalEvaluation() / LiteralRationalEvaluation()` for `t_kev ** (1.0/3.0)`. Cause: `reconstruct_expression` (`sysml-codegen/src/sysml_codegen/extraction/expression_utils.py:64`) keys literals on class names `LiteralInteger/LiteralReal/LiteralRational`, but syside's runtime node class is `LiteralRationalEvaluation`, so literals fall through to the `str(expr_node)` fallback at `expression_utils.py:79`. The auto-implement path is fine because `expression_compiler.py:394-396` uses `SysideAdapter.is_instance` instead of raw class-name matching.
2. **Parenthesization is lost.** `reconstruct_operator_expression` emits binary ops as `f"{left}{op_str}{right}"` with no parens (`expression_utils.py:96`), so `** (1.0/3.0)` renders as if it were `(t_kev ** 1.0) / 3.0`. An AI pass that trusted the rendered spec alone would implement the wrong exponent. The `file:line` source pointer is what saves it.

Minor: the "Registry unresolved" warnings for part-attribute-backed calc inputs are cosmetic here — the design values (10.0, 6.4e-14, 19.98, 100.0) still landed correctly in `generated/inputs/exp_toy_params.json`.

## 3. AI-pass verdict

The AI pass (this session) implemented both `manual_required` stencils from the SysML source at the stencil's `file:line` pointer:

- `generated/handwritten/exp_toy/boschhalereactivity_impl.py` — `math.exp`, exact expression shape
- `generated/handwritten/exp_toy/gaindoublings_impl.py` — `math.log`

The information needed was fully available: the stencil carries the source pointer, the (degraded) expression text, the doc comment, and typed input/output signatures. **Caveat from §2**: the *rendered* expression alone was NOT sufficient (literals gone, parens gone) — faithfulness required reading the `.sysml` source. The pointer makes that a one-hop lookup, so the workflow holds, but the renderer bugs mean the docstring spec is currently a trap rather than an aid.

## 4. Execution verdict

Full teax execution (`run_exp_spike.py`, same executor venv as WI-013/WI-015) at 3 input points × 3 channels, asserted against an independent hand computation with `math.exp`/`math.log` (also re-verified separately via `uv run python` in the project venv):

| Point | sigma_v (executed = oracle) | doublings | e_to_x |
|---|---|---|---|
| T=10 keV, G=100, x=10 | 1.293933940453e-18 | 6.643856189775 | 2.202646579481e+04 |
| T=20 keV, G=350, x=2.5 | 5.522267633056e-18 | 8.451211111832 | 1.218249396070e+01 |
| T=5 keV, G=30, x=-1 | 3.169225535842e-19 | 4.906890595609 | 3.678794411714e-01 |

**ALL 9 ASSERTIONS PASSED**, relative deviation 0.0 (bit-exact; tolerance was 1e-12). Physics sanity: reactivity is monotonically increasing 5→10→20 keV as the Gamow suppression relaxes; log2(100)=6.644; e^-1=0.3679.

Executor gaps unchanged from WI-013: the ExitPoint's primitive types still need the explicit output-router registration workaround (`run_exp_spike.py`, `main()`).

## 5. Is the out-of-envelope claim now tested?

Yes — with a reframed mechanism. The original claim ("when a model uses e.g. exp(), the AI pass hand-writes the Python body") is confirmed end-to-end, but "a model uses exp()" necessarily means *the model declares its own uninterpreted calc def*, because the standard library has no transcendental functions to call — that spelling question was the real unknown, and the answer is that syside parses it clean, the codegen compiler correctly classifies such bodies as `manual_required` without crashing, the invocation survives by name into the stencil, the AI pass can implement it faithfully (from the source pointer — not from the lossy rendered spec, per the two renderer bugs above), and teax executes it bit-exactly. Still untested: conditionals (`if`/ternary in calc bodies), stdlib-but-unmapped functions like `sqrt`/`sin` (does the compiler translate them, classify them manual, or crash? — different code path from an unknown user symbol), multi-output manual stencils, and whether an uninterpreted calc def used as a *calc usage in a part* (rather than inline invocation) generates a broken empty module. The renderer literal/paren loss (expression_utils.py:64,79,96) should be fixed or the "Calculation Specification" block dropped from stencils before the AI pass is pointed at bigger models, since it actively misleads.

## Reproduce

```bash
# probes + toy parse (Level 1)
cd ~/1cfe/fusion-tea && uv run python -m syside check exploration/exp_spike/models/exp_toy.sysml
# live extraction + generation
cd ~/1cfe/sysml-codegen && uv run sysml-codegen generate \
  --models ~/1cfe/fusion-tea/exploration/exp_spike/models \
  --output ~/1cfe/fusion-tea/exploration/exp_spike/generated \
  --package-name exp_toy_tea --pipeline-name exp_toy --overwrite
# (re-apply AI-pass bodies in generated/handwritten/exp_toy/*_impl.py — generate overwrites)
# execute + assert
cd ~/1cfe/fusion-tea/exploration/exp_spike && ../pipeline_spike/.venv-exec/bin/python run_exp_spike.py
```

No quoted names in the toy, so the WI-015 sanitizer was not needed.
