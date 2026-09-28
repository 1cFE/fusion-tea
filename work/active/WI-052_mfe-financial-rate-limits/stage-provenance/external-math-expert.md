Expert consultation: `/root/wi052_math_expert`, fresh non-author mathematical consultation for WI-052; not an implementation audit.

**Evidence grade.** Source-inspected and independently derived from the isolated spec, alignment, three canonical definitions, and handwritten lifecycle. Executed standalone mathematical probes through the isolated `.codex-test/run`; no production helpers tested or files changed. External financial sources were not reverified.

Let \(i\) denote discount, \(g\) escalation, \(N>0\) operating duration, \(T>0\) construction duration, and \(\ell=\log1p(i)\). The following retain the inspected equations’ real-duration extensions.

- **CRF:** use \(i/[-\operatorname{expm1}(-N\ell)]\), with exact \(i=0\) returning \(1/N\). This avoids forming `1+i` and subtracting nearly equal powers. It also avoids positive-rate numerator overflow from the original positive exponential.
- **Growing annuity:** retain \(A_1=A\exp[T\log1p(g)]\). Define \(d=(g-i)/(1+i)\), \(z=N\log1p(d)\), \(E(z)=\operatorname{expm1}(z)/z\), and \(L(d)=\log1p(d)/d\), with both functions equal to 1 at zero. Then \(PV=A_1N E(z)L(d)/(1+i)\). Computing the rate difference before adding 1 preserves nearby unequal rates. At equality this gives \(PV=A_1N/(1+i)\); at \(i=g=0\), \(PV=AN\). At \(i=0,\ g\ne0\), it reproduces \(A_1[(1+g)^N-1]/g\). Levelization remains `CRF * PV`.
- **Reported IDC:** preserve \(f=[(1+i)^T-1]/(Ti)-1\). There are two cancellation sites: the exponential numerator, then the final subtraction of 1. `expm1` repairs only the first. Near zero use
  \[
  f=\frac{T-1}{2}i+\frac{(T-1)(T-2)}6i^2+\frac{(T-1)(T-2)(T-3)}{24}i^3+\cdots.
  \]
  Starting with \(a_1=(T-1)i/2\), generate \(a_{k+1}=a_k i(T-k-1)/(k+2)\). This directly computes the small result and preserves fractional \(T\). Exact \(i=0\) and exact \(T=1\) return zero. For \(0<T<1\), positive interest produces negative reported IDC under the existing equation; do not clamp it.
- **Held replacement PV:** preserve the existing clipped period \(p\) and count \(m=\max(0,\lceil N/p\rceil-1)\). With \(z=-p\ell\), use \(PV=C\exp(z)\operatorname{expm1}(mz)/\operatorname{expm1}(z)\). Return zero before financial evaluation when \(m=0\); return \(Cm\) at zero interest. The equivalent \(Cm\exp(z)E(mz)/E(z)\) handles very small exponential arguments more gracefully. Annualize with the same CRF.
- **Live replacement:** retain event dates and discount each payment as \(C\exp(-t_k\ell)\). Finance changes must leave the event walk, strict restart condition, downtime, and energy-bin timing intact. Headline midpoint finance remains \(\exp(T\ell/2)\), distinct from reported IDC.

**Executed probes.** Compared standalone binary64 formulas against Decimal references using the actual represented inputs. Rates were 0, 0.02, 0.08 and both signs of \(10^{-4},10^{-8},10^{-12},10^{-16},10^{-18}\); durations included 0.125, 1, 8, 8.5, 30, 30.5 and 100.

| Quantity | Cases | Largest relative error |
|---|---:|---:|
| CRF | 91 | \(2.35\times10^{-16}\) |
| IDC | 91 | \(1.48\times10^{-15}\) |
| Annuity | 455 | \(4.39\times10^{-16}\) |
| Held PV | 208 | \(2.68\times10^{-16}\) |

IDC used 40 series terms when \(|i|\max(1,T)<0.1\), otherwise the `expm1` expression. Inside that branch successive term magnitudes decrease by at least a factor of 0.1, giving a strong truncation margin. At \(T=8.5,\ i=\pm10^{-18}\), the series returns \(\pm3.75\times10^{-18}\); the `expm1` quotient followed by subtraction returns zero.

The annuity probe included adjacent representable rates, including subnormals around zero. An initial 100-digit reference lacked precision there. The corrected run used 420 digits and the factored expression above. This correction is reference development, not production evidence.

**Verification targets and remaining risks.**

- Use independent dated Decimal sums for integer annuities and replacements; the executed held references already used finite sums. Use high-precision analytic continuation for fractional durations.
- Test exact numerical switches and both neighboring sides, \(T=1\) and its neighbors, fractional replacement periods, zero events, and both sides of count/restart boundaries.
- Assert relative accuracy on tiny nonzero IDC itself. Final prices cannot detect its loss.
- Preserve held floor-then-cap order, the wall-load floor, and count arithmetic exactly. Compare all physical/calendar outputs separately from financial outputs.
- Attribute ordinary changes to stable evaluation against independent references; arbitrary bit-identical financial roundoff is unnecessary.
- These probes do not certify extreme horizons, overflow regimes, or all rates near −1. Small-argument factor functions need deliberate underflow handling. Construction \(T=0\) remains parked; none of these formulas supplies a timing-policy decision.
