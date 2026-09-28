# Return-condition check (owner direction 4)

Condition: the helium must return from the exchanger at the loop's compressor inlet temperature `T_comp_in` (561.94 K) so that the circulator delivers the blanket inlet the loop holds (573.15 K, Moscato et al. output.md:79). It is stated in the loop definition and not checked in the assembly. Residual = `T_comp_in` − `he_return`; it equals the stored `he_hot_bound_margin` at every case where all heat is removed (163 of 163).

| Case | Net MW | Unmet MW | Return K | Residual K | Bypass-equivalent | Passing |
|---|---|---|---|---|---|---|
| `ir-f2500-r1.5183` | 426.579 | 0.000 | 513.12 | +48.819 | 18.8% | yes |
| `ir-f2250-r1.5183` | 597.481 | 0.000 | 561.23 | +0.701 | 0.3% | yes |
| `ir-f2750-r1.3750` | 594.567 | 0.000 | 553.30 | +8.633 | 3.9% | yes |
| `ir-f3000-r1.3250` | 581.436 | 0.000 | 553.06 | +8.872 | 4.0% | yes |
| `ir-f2500-r1.4500` | 575.617 | 0.000 | 548.36 | +13.573 | 6.0% | yes |
| `ir-f2500-r1.4250` | 620.008 | 7.775 | 562.43 | -0.497 | 0.0% | no |
| `s6-hx75000-f2500-r1.4000` | 671.624 | 0.000 | 558.89 | +3.041 | 1.4% | yes |
| `s6-hx75000-f2250-r1.5000` | 632.540 | 0.000 | 551.69 | +10.248 | 4.6% | yes |

Passing I-R grid points (52): residual min 0.70 K (`ir-f2250-r1.5183`), median 67.0 K, max 125.4 K (`ir-f3500-r1.4250`); within 5 K: `ir-f2250-r1.5183`, `ir-f4000-r1.2000`; within 15 K: `ir-f2250-r1.5183`, `ir-f4000-r1.2000`, `ir-f3500-r1.2500`, `ir-f2750-r1.3750`, `ir-f3000-r1.3250`, `ir-f2500-r1.4500`.
