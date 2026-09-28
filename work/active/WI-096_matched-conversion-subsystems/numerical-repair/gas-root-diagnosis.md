# Sealed gas-root numerical diagnosis

The unchanged sealed native network and bypass bodies replay bit-exact in all six selected cases. The JSON retains exact input tuples, native root brackets, and independent 70-digit roots. No model, oracle, tolerance, or historical receipt was changed.

| Case | Native minus exact hot margin (K) | Local bypass error (kg/s) | Propagated closure error (kg/s) | Accurate bypass minus oracle (kg/s) |
| --- | ---: | ---: | ---: | ---: |
| c0206 | 0.000000E-61 | 0.000000E-35 | 0.000000E-35 | 0.000000E-35 |
| c0480 | -4.216345E-10 | 3.814198E-9 | -2.115689E-8 | -1.450744E-10 |
| c0481 | -7.825870E-10 | 1.565678E-10 | -1.051313E-8 | 4.380142E-11 |
| c0482 | 3.414157E-10 | 6.578772E-10 | 7.480306E-9 | -1.183732E-9 |
| c0484 | -4.216345E-10 | 3.814198E-9 | -2.115689E-8 | -1.450744E-10 |
| c0485 | -7.825870E-10 | 1.565678E-10 | -1.051313E-8 | 4.380142E-11 |

## Interpretation

[AGENT] Diagnosis covers original c0480/c0484 and nearby efficiency variants c0481/c0482/c0485, plus engineering-failing c0206. Each contribution is computed independently: the controller is first solved with its exact native inlet, then with the accurate exchanger inlet. The hot-margin decomposition separately substitutes the full oracle input tuple. The original oracle is only evaluated; its stopping behavior is not copied into these roots.

Numerical interpretation and minimal repair rationale follow the values in the JSON; this evidence does not certify any future implementation.
